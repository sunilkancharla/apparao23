"""Real scoped SQLite/index pipeline; injected models/native cosine kernel only."""

import asyncio
import math
import struct
from contextlib import asynccontextmanager

import pytest

from app.ingestion.validation import UploadError
from app.retrieval.embeddings import Embedding, EmbeddingBatch
from app.retrieval.index import LocalIndex
from app.retrieval.search import Retriever
from app.storage.documents import Documents
from app.storage.extractions import Extractions
from app.storage.files import UploadStore


@pytest.fixture
def retrieval(tmp_path, run_budget):
    store = UploadStore(tmp_path)
    control = {"queries": 0, "loads": 0, "distances": 0, "during": None}

    def vector(text):
        axis = 0 if "North" in text else 1 if "South" in text else 2
        return tuple(float(i == axis) for i in range(768))

    class Fake:
        async def documents(self, chunks):
            return EmbeddingBatch(
                "document",
                tuple(
                    Embedding(c.chunk_id, c.text_hash, vector(c.text)) for c in chunks
                ),
                None,
            )

        async def query(self, question, query_id):
            import hashlib

            control["queries"] += 1
            if control["during"]:
                control["during"]()
            return EmbeddingBatch(
                "query",
                (
                    Embedding(
                        query_id,
                        hashlib.sha256(question.encode()).hexdigest(),
                        vector(question),
                    ),
                ),
                None,
            )

    @asynccontextmanager
    async def session():
        assert not store.busy
        store.busy = True
        try:
            yield Fake()
        finally:
            store.busy = False

    async def add(
        body=b"Name,Units\nNorth,42\nSouth,50\n",
        *,
        conversation=None,
        name="authored.csv",
        indexed=True,
    ):
        conversation = conversation or Documents(store.connection).create_conversation()

        async def stream():
            yield body

        uploaded = await store.receive(
            stream(),
            conversation,
            "upload-"
            + str(
                store.connection.execute("SELECT count(*) FROM uploads").fetchone()[0]
            ),
            name,
        )
        await Extractions(store).extract(
            conversation, uploaded["reference_id"], "extract-source-01"
        )
        if indexed:
            await LocalIndex(store).index(
                conversation,
                uploaded["reference_id"],
                "index-source-01",
                session_factory=session,
            )
        return conversation, uploaded["reference_id"]

    def loader(connection):
        control["loads"] += 1

        def distance(left, right):
            control["distances"] += 1
            a, b = struct.unpack("<768f", left), struct.unpack("<768f", right)
            return 1 - sum(x * y for x, y in zip(a, b)) / (
                math.hypot(*a) * math.hypot(*b)
            )

        connection.create_function("vec_distance_cosine", 2, distance)

    try:
        yield store, add, Retriever(store, loader=loader), session, control
    finally:
        for row in store.connection.execute("SELECT payload FROM index_chunks"):
            run_budget.retain(row[0].encode())
        store.close()


def test_selected_scope_ranks_expected_table_passage_and_keeps_headers(retrieval):
    _, add, search, session, control = retrieval
    conversation, reference = asyncio.run(add())
    _, unselected = asyncio.run(
        add(
            b"Name,Units\nNorth,999\n", conversation=conversation, name="unselected.csv"
        )
    )
    result = asyncio.run(
        search.retrieve(
            conversation, [reference], "North units?", session_factory=session
        )
    )
    assert len(result.ranked) == 2 and len(result.evidence) == 2
    assert all(hit.reference_id == reference for hit in result.ranked)
    assert "42" in result.ranked[0].chunk.text and result.ranked[0].distance == 0
    assert {p.role for p in result.ranked[0].chunk.parts} == {"header", "data"}
    assert control["queries"] == 1 and control["distances"] == 2
    assert len(result.snapshot) == 1 and result.snapshot[0].reference_id == reference
    assert unselected not in result.evidence[0].rendered


def test_identical_bytes_across_conversations_do_not_grant_access(retrieval):
    _, add, search, session, control = retrieval
    first, ref = asyncio.run(add())
    _, foreign = asyncio.run(add())
    with pytest.raises(UploadError, match="SOURCE_NOT_FOUND"):
        asyncio.run(
            search.retrieve(first, [ref, foreign], "North?", session_factory=session)
        )
    assert control["queries"] == control["loads"] == 0


def test_empty_selection_does_not_start_runtime_and_none_does_not_broaden(retrieval):
    _, add, search, session, control = retrieval
    conversation, _ = asyncio.run(add())
    result = asyncio.run(
        search.retrieve(conversation, [], "North?", session_factory=session)
    )
    assert result.status == "no_evidence" and not result.evidence
    assert control["queries"] == control["loads"] == 0
    with pytest.raises(UploadError, match="SELECTION_REQUIRED"):
        asyncio.run(
            search.retrieve(conversation, None, "North?", session_factory=session)
        )


def test_partial_scope_reports_unindexed_reference(retrieval):
    _, add, search, session, _ = retrieval
    conversation, good = asyncio.run(add())
    _, pending = asyncio.run(
        add(b"Name,Units\nWest,10\n", conversation=conversation, indexed=False)
    )
    result = asyncio.run(
        search.retrieve(
            conversation, [good, pending], "North?", session_factory=session
        )
    )
    assert len(result.blocked) == 1 and result.blocked[0].reference_id == pending
    assert result.blocked[0].code == "INDEX_REQUIRED" and result.ranked


def test_multiple_files_and_exact_distance_ties_are_stable(retrieval):
    _, add, search, session, _ = retrieval
    conversation, first = asyncio.run(add(b"Name,Units\nNorth,42\n"))
    _, second = asyncio.run(
        add(b"Name,Units\nNorth,70\n", conversation=conversation, name="second.csv")
    )
    result = asyncio.run(
        search.retrieve(
            conversation, [second, first], "North?", session_factory=session
        )
    )
    assert {x.reference_id for x in result.ranked} == {first, second}
    assert [x.chunk.chunk_id for x in result.ranked] == sorted(
        x.chunk.chunk_id for x in result.ranked
    )
    assert "DISTANCE_TIE" in result.warnings


def test_packing_keeps_whole_chunks_and_separates_ranked_and_supplied(retrieval):
    _, add, search, session, _ = retrieval
    body = b"Name,Units\n" + b"North" + b"x" * 560 + b",42\n"
    conversation, first = asyncio.run(add(body))
    refs = [first]
    for i in range(5):
        _, ref = asyncio.run(
            add(
                body.replace(b",42", f",{43 + i}".encode()),
                conversation=conversation,
                name=f"{i}.csv",
            )
        )
        refs.append(ref)
    result = asyncio.run(
        search.retrieve(conversation, refs, "North?", session_factory=session)
    )
    assert len(result.ranked) == 5 and len(result.evidence) < 5
    assert (
        result.evidence_bytes
        == len("\n\n".join(x.rendered for x in result.evidence).encode())
        <= 2000
    )
    assert all(x.hit.chunk.text in x.rendered for x in result.evidence)
    assert len(result.omitted) == 5 - len(result.evidence)
    assert len({x.evidence_id for x in result.evidence}) == len(result.evidence)


@pytest.mark.parametrize("question", ["", "x" * 513, "\ud800"])
def test_invalid_questions_fail_before_embedding(retrieval, question):
    _, add, search, session, control = retrieval
    conversation, reference = asyncio.run(add())
    with pytest.raises(UploadError, match="RETRIEVAL_QUESTION_INVALID"):
        asyncio.run(
            search.retrieve(
                conversation, [reference], question, session_factory=session
            )
        )
    assert control["queries"] == 0


def test_duplicate_selection_and_busy_refuse_before_embedding(retrieval):
    store, add, search, session, control = retrieval
    conversation, reference = asyncio.run(add())
    with pytest.raises(UploadError, match="INVALID_SELECTION"):
        asyncio.run(
            search.retrieve(
                conversation, [reference, reference], "North?", session_factory=session
            )
        )
    store.busy = True
    with pytest.raises(UploadError, match="UPLOAD_BUSY"):
        asyncio.run(
            search.retrieve(
                conversation, [reference], "North?", session_factory=session
            )
        )
    store.busy = False
    assert control["queries"] == 0


def test_corrupt_selected_vector_is_rejected_before_native_kernel(retrieval):
    store, add, search, session, control = retrieval
    conversation, reference = asyncio.run(add())
    with store._write():
        store.connection.execute(
            "UPDATE index_vectors SET vector=?",
            (struct.pack("<768f", float("nan"), *([0] * 767)),),
        )
    with pytest.raises(UploadError, match="RETRIEVAL_VECTOR_INVALID"):
        asyncio.run(
            search.retrieve(
                conversation, [reference], "North?", session_factory=session
            )
        )
    assert control["loads"] == control["distances"] == 0


@pytest.mark.parametrize("change", ["original", "generation"])
def test_source_change_during_query_publishes_no_result(retrieval, change):
    store, add, search, session, control = retrieval
    conversation, reference = asyncio.run(add())

    def mutate():
        if change == "original":
            next((store.root / "originals").iterdir()).write_bytes(b"changed")
        else:
            with store._write():
                store.connection.execute(
                    "UPDATE index_generations SET identity=?", ("0" * 64,)
                )

    control["during"] = mutate
    with pytest.raises(UploadError, match="SOURCE_CHANGED"):
        asyncio.run(
            search.retrieve(
                conversation, [reference], "North?", session_factory=session
            )
        )
    assert control["loads"] == 0 and not store.busy


def test_cancellation_releases_slot_without_native_search(retrieval):
    store, add, search, session, control = retrieval
    conversation, reference = asyncio.run(add())

    def cancel():
        raise asyncio.CancelledError

    control["during"] = cancel
    with pytest.raises(asyncio.CancelledError):
        asyncio.run(
            search.retrieve(
                conversation, [reference], "North?", session_factory=session
            )
        )
    assert control["loads"] == 0 and not store.busy


def test_missing_original_returns_disclosed_no_evidence(retrieval):
    store, add, search, session, control = retrieval
    conversation, reference = asyncio.run(add())
    next((store.root / "originals").iterdir()).unlink()
    result = asyncio.run(
        search.retrieve(conversation, [reference], "North?", session_factory=session)
    )
    assert (
        result.status == "no_evidence"
        and result.blocked[0].code == "SOURCE_UNAVAILABLE"
    )
    assert control["queries"] == control["loads"] == 0


def test_unanswerable_question_does_not_turn_similarity_into_support(retrieval):
    _, add, search, session, _ = retrieval
    conversation, reference = asyncio.run(add())
    result = asyncio.run(
        search.retrieve(
            conversation, [reference], "Who owns the company?", session_factory=session
        )
    )
    assert result.ranked and "ANSWERABILITY_UNASSESSED" in result.warnings
    assert "TOKEN_FIT_UNVERIFIED" in result.warnings


def test_native_failure_is_safe_and_does_not_fall_back(retrieval):
    import sqlite3

    store, add, search, session, control = retrieval
    conversation, reference = asyncio.run(add())

    def fail(connection):
        raise sqlite3.OperationalError("synthetic sensitive path")

    search.loader = fail
    with pytest.raises(UploadError, match="^RETRIEVAL_FAILED$"):
        asyncio.run(
            search.retrieve(
                conversation, [reference], "North?", session_factory=session
            )
        )
    assert not store.busy and control["distances"] == 0


def test_reference_removed_during_query_reports_source_changed(retrieval):
    store, add, search, session, control = retrieval
    conversation, reference = asyncio.run(add())

    def remove():
        with store._write():
            store.connection.execute(
                "DELETE FROM index_requests WHERE reference_id=?", (reference,)
            )
            store.connection.execute(
                "DELETE FROM csv_requests WHERE reference_id=?", (reference,)
            )
            store.connection.execute(
                "DELETE FROM document_references WHERE id=?", (reference,)
            )

    control["during"] = remove
    with pytest.raises(UploadError, match="SOURCE_CHANGED"):
        asyncio.run(
            search.retrieve(
                conversation, [reference], "North?", session_factory=session
            )
        )
    assert control["loads"] == 0
