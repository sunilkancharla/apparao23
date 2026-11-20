"""Stored-CSV indexing uses synthetic vectors and real SQLite transactions."""

import asyncio
import json
import sqlite3
from contextlib import asynccontextmanager

import pytest

from app.ingestion.validation import UploadError
from app.retrieval.embeddings import Embedding, EmbeddingBatch
from app.retrieval.index import LocalIndex
from app.storage.database import (
    APPLICATION_ID,
    SCHEMA_V4,
    SCHEMA_VERSION,
    open_database,
)
from app.storage.documents import Documents
from app.storage.extractions import Extractions
from app.storage.files import UploadStore
from app.storage.index_state import IndexState


def test_exact_v4_migration_preserves_prior_metadata(tmp_path):
    connection = sqlite3.connect(tmp_path / "metadata.sqlite3")
    for statement in SCHEMA_V4:
        connection.execute(statement)
    connection.execute("INSERT INTO conversations VALUES ('preserved')")
    connection.execute(f"PRAGMA application_id={APPLICATION_ID}")
    connection.execute("PRAGMA user_version=4")
    connection.commit()
    connection.close()
    connection = open_database(tmp_path)
    try:
        assert connection.execute("PRAGMA user_version").fetchone()[0] == SCHEMA_VERSION
        assert (
            connection.execute("SELECT id FROM conversations").fetchone()[0]
            == "preserved"
        )
        assert (
            connection.execute("SELECT count(*) FROM index_generations").fetchone()[0]
            == 0
        )
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
    finally:
        connection.close()


@pytest.fixture
def indexed_source(tmp_path, run_budget):
    store = UploadStore(tmp_path)
    control = {"sessions": 0, "batches": 0, "fail": None}

    async def upload(body=b"Name,Units\nNorth,42\nSouth,50\n", name="authored.csv"):
        conversation = Documents(store.connection).create_conversation()

        async def stream():
            yield body

        uploaded = await store.receive(stream(), conversation, "upload-index-01", name)
        extracted = await Extractions(store).extract(
            conversation, uploaded["reference_id"], "extract-index-01"
        )
        return conversation, uploaded, extracted

    class FakeEmbedder:
        async def documents(self, chunks):
            control["batches"] += 1
            if control["fail"] == "batch" and control["batches"] == 2:
                raise RuntimeError("synthetic failure")
            if control["fail"] == "cancel":
                raise asyncio.CancelledError
            if control["fail"] == "tamper":
                next((store.root / "originals").iterdir()).write_bytes(b"changed")
            return EmbeddingBatch(
                "document",
                tuple(
                    Embedding(c.chunk_id, c.text_hash, (1.0,) + (0.0,) * 767)
                    for c in chunks
                ),
                None,
            )

    @asynccontextmanager
    async def session():
        assert not store.busy
        control["sessions"] += 1
        store.busy = True
        try:
            yield FakeEmbedder()
        finally:
            store.busy = False

    try:
        yield store, upload, session, control
    finally:
        for row in store.connection.execute("SELECT payload FROM index_chunks"):
            run_budget.retain(row[0].encode())
        store.close()


def test_csv_index_round_trip_repeat_and_restart(indexed_source):
    store, upload, session, control = indexed_source
    conversation, uploaded, extracted = asyncio.run(upload())
    index = LocalIndex(store)
    result = asyncio.run(
        index.index(
            conversation,
            uploaded["reference_id"],
            "index-key-01",
            session_factory=session,
        )
    )
    assert result["indexed"] and result["ready"] and result["chunk_count"] == 2
    assert result["omission_count"] == 0
    assert (
        asyncio.run(
            index.index(
                conversation,
                uploaded["reference_id"],
                "index-key-01",
                session_factory=session,
            )
        )
        == result
    )
    assert control["sessions"] == control["batches"] == 1
    rows = IndexState(store).chunks(conversation, uploaded["reference_id"])
    assert len(rows) == 2 and rows[0].source.extraction_id == extracted["extraction_id"]
    assert (
        rows[0].parts[0].role == "header"
        and rows[0].parts[0].location.record_start is None
    )
    assert next(p for p in rows[0].parts if p.role == "data").location.record_start == 1
    assert (
        store.connection.execute("SELECT length(vector) FROM index_vectors").fetchone()[
            0
        ]
        == 3072
    )
    root = store.root
    store.close()
    reopened = UploadStore(root)
    try:
        assert (
            IndexState(reopened).status(conversation, uploaded["reference_id"])[
                "generation_id"
            ]
            == result["generation_id"]
        )
        assert (
            IndexState(reopened).chunks(conversation, uploaded["reference_id"]) == rows
        )
    finally:
        reopened.close()
    store.connection = open_database(root)


def test_identical_content_reuses_vectors_but_keeps_source_and_scope(indexed_source):
    store, upload, session, control = indexed_source
    first = asyncio.run(upload())
    second = asyncio.run(upload(name="different.csv"))
    results = [
        asyncio.run(
            LocalIndex(store).index(
                c, u["reference_id"], "index-key-01", session_factory=session
            )
        )
        for c, u, _ in (first, second)
    ]
    assert results[0]["generation_id"] == results[1]["generation_id"]
    assert control["sessions"] == 1
    assert (
        store.connection.execute("SELECT count(*) FROM index_vectors").fetchone()[0]
        == 2
    )
    assert (
        store.connection.execute("SELECT count(*) FROM index_bindings").fetchone()[0]
        == 2
    )
    for (conversation, uploaded, extraction), name in zip(
        (first, second), ("authored.csv", "different.csv")
    ):
        chunks = IndexState(store).chunks(conversation, uploaded["reference_id"])
        assert chunks[0].source.filename == name
        assert chunks[0].source.extraction_id == extraction["extraction_id"]
    with pytest.raises(UploadError, match="SOURCE_NOT_FOUND"):
        IndexState(store).chunks(first[0], second[1]["reference_id"])


@pytest.mark.parametrize("failure", ["batch", "cancel", "tamper"])
def test_failed_or_cancelled_publication_has_no_vectors_or_binding(
    indexed_source, failure
):
    store, upload, session, control = indexed_source
    body = b"Name,Units\n" + b"North,42\n" * 10
    conversation, uploaded, _ = asyncio.run(upload(body))
    control["fail"] = failure
    error = asyncio.CancelledError if failure == "cancel" else UploadError
    with pytest.raises(error):
        asyncio.run(
            LocalIndex(store).index(
                conversation,
                uploaded["reference_id"],
                "index-fail-01",
                session_factory=session,
            )
        )
    assert (
        store.connection.execute("SELECT count(*) FROM index_vectors").fetchone()[0]
        == 0
    )
    assert (
        store.connection.execute("SELECT count(*) FROM index_bindings").fetchone()[0]
        == 0
    )
    assert (
        store.connection.execute("SELECT state FROM index_generations").fetchone()[0]
        == "failed"
    )
    assert not store.busy
    if failure != "tamper":
        control["fail"] = None
        with pytest.raises(UploadError):
            asyncio.run(
                LocalIndex(store).index(
                    conversation,
                    uploaded["reference_id"],
                    "index-fail-01",
                    session_factory=session,
                )
            )
        assert asyncio.run(
            LocalIndex(store).index(
                conversation,
                uploaded["reference_id"],
                "index-retry-01",
                session_factory=session,
            )
        )["indexed"]


def test_busy_and_corrupt_source_do_not_start_embedding(indexed_source):
    store, upload, session, control = indexed_source
    conversation, uploaded, _ = asyncio.run(upload())
    store.busy = True
    with pytest.raises(UploadError, match="UPLOAD_BUSY"):
        asyncio.run(
            LocalIndex(store).index(
                conversation,
                uploaded["reference_id"],
                "index-key-01",
                session_factory=session,
            )
        )
    store.busy = False
    next((store.root / "originals").iterdir()).write_bytes(b"changed")
    with pytest.raises(UploadError, match="SOURCE_UNAVAILABLE"):
        asyncio.run(
            LocalIndex(store).index(
                conversation,
                uploaded["reference_id"],
                "index-key-01",
                session_factory=session,
            )
        )
    assert control["sessions"] == 0


def test_status_tracks_index_completion_and_scope(indexed_source):
    from app.ingestion.processing import UploadOperations

    store, upload, session, _ = indexed_source
    conversation, uploaded, extracted = asyncio.run(upload())
    receipt = asyncio.run(
        LocalIndex(store).index(
            conversation,
            uploaded["reference_id"],
            "index-key-01",
            session_factory=session,
        )
    )
    for operation in (
        uploaded["operation_id"],
        extracted["operation_id"],
        receipt["operation_id"],
    ):
        status = UploadOperations(store).status(conversation, operation)
        assert status["indexed"] and status["ready"] and status["state"] == "indexed"
    other = Documents(store.connection).create_conversation()
    with pytest.raises(UploadError, match="OPERATION_NOT_FOUND"):
        UploadOperations(store).status(other, receipt["operation_id"])


def test_recovery_closes_intent_and_refuses_ambiguous_persisted_rows(indexed_source):
    from app.storage.index_state import recover_indexes

    store, upload, session, _ = indexed_source
    conversation, uploaded, _ = asyncio.run(upload())
    receipt = asyncio.run(
        LocalIndex(store).index(
            conversation,
            uploaded["reference_id"],
            "index-key-01",
            session_factory=session,
        )
    )
    with store._write():
        store.connection.execute(
            "UPDATE index_generations SET state='processing' WHERE id=?",
            (receipt["generation_id"],),
        )
    recover_indexes(store)
    assert store.recovery_pending
    assert (
        store.connection.execute("SELECT count(*) FROM index_vectors").fetchone()[0]
        == 2
    )


def test_changed_profile_is_not_reused_and_old_key_cannot_publish_it(indexed_source):
    from app.ingestion.processing import UploadOperations

    store, upload, session, control = indexed_source
    conversation, uploaded, _ = asyncio.run(upload())
    first = asyncio.run(
        LocalIndex(store).index(
            conversation,
            uploaded["reference_id"],
            "index-key-01",
            session_factory=session,
        )
    )
    with store._write():
        store.connection.execute(
            "UPDATE index_generations SET identity=? WHERE id=?",
            ("0" * 64, first["generation_id"]),
        )
    assert IndexState(store).status(conversation, uploaded["reference_id"]) is None
    historical = UploadOperations(store).status(conversation, first["operation_id"])
    assert not historical["indexed"] and historical["state"] == "reindex_required"
    with pytest.raises(UploadError, match="INDEX_VERSION_CHANGED"):
        asyncio.run(
            LocalIndex(store).index(
                conversation,
                uploaded["reference_id"],
                "index-key-01",
                session_factory=session,
            )
        )
    second = asyncio.run(
        LocalIndex(store).index(
            conversation,
            uploaded["reference_id"],
            "index-key-02",
            session_factory=session,
        )
    )
    assert (
        second["generation_id"] != first["generation_id"] and control["sessions"] == 2
    )


def test_omitted_rows_are_persisted_and_partial_index_is_disclosed(indexed_source):
    store, upload, session, _ = indexed_source
    conversation, uploaded, _ = asyncio.run(
        upload(b"Name,Units\nNorth,42\n" + b"x" * 900 + b",50\n")
    )
    receipt = asyncio.run(
        LocalIndex(store).index(
            conversation,
            uploaded["reference_id"],
            "index-key-01",
            session_factory=session,
        )
    )
    assert receipt["indexed"] and not receipt["ready"]
    assert (
        receipt["state"] == "indexed_with_omissions" and receipt["omission_count"] == 1
    )
    assert receipt["warning_codes"] == ["INDEX_OMISSIONS"]
    payload = store.connection.execute(
        "SELECT payload FROM index_omissions"
    ).fetchone()[0]
    assert json.loads(payload)["code"] == "OVERSIZED_TABLE_ROW"


def test_content_change_and_same_filename_produce_distinct_generations(indexed_source):
    store, upload, session, control = indexed_source
    first = asyncio.run(upload())
    second = asyncio.run(upload(b"Name,Units\nNorth,99\n"))
    receipts = [
        asyncio.run(
            LocalIndex(store).index(
                c, u["reference_id"], "index-key-01", session_factory=session
            )
        )
        for c, u, _ in (first, second)
    ]
    assert (
        receipts[0]["generation_id"] != receipts[1]["generation_id"]
        and control["sessions"] == 2
    )


def test_quota_failure_rolls_back_and_preserves_original(indexed_source, monkeypatch):
    store, upload, session, _ = indexed_source
    conversation, uploaded, _ = asyncio.run(upload())
    original = store.reserve_growth

    def reserve(size=0):
        if size > 3072:
            raise UploadError("PROCESSED_QUOTA", 507)
        original(size)

    monkeypatch.setattr(store, "reserve_growth", reserve)
    with pytest.raises(UploadError, match="PROCESSED_QUOTA"):
        asyncio.run(
            LocalIndex(store).index(
                conversation,
                uploaded["reference_id"],
                "index-key-01",
                session_factory=session,
            )
        )
    assert (
        store.connection.execute("SELECT count(*) FROM index_vectors").fetchone()[0]
        == 0
    )
    assert (
        next((store.root / "originals").iterdir())
        .read_bytes()
        .startswith(b"Name,Units")
    )


def test_all_omitted_content_is_not_marked_indexed(indexed_source):
    store, upload, session, _ = indexed_source
    conversation, uploaded, _ = asyncio.run(
        upload(b"Name,Units\n" + b"x" * 900 + b",50\n")
    )
    with pytest.raises(UploadError, match="INDEX_NO_EVIDENCE"):
        asyncio.run(
            LocalIndex(store).index(
                conversation,
                uploaded["reference_id"],
                "index-key-01",
                session_factory=session,
            )
        )
    assert not IndexState(store).status(conversation, uploaded["reference_id"])[
        "indexed"
    ]
    assert (
        store.connection.execute("SELECT count(*) FROM index_bindings").fetchone()[0]
        == 0
    )


def test_failed_reuse_does_not_fail_the_shared_generation(indexed_source):
    store, upload, session, control = indexed_source
    first, second = asyncio.run(upload()), asyncio.run(upload(name="second.csv"))
    receipt = asyncio.run(
        LocalIndex(store).index(
            first[0], first[1]["reference_id"], "index-key-01", session_factory=session
        )
    )
    with store._write():
        store.connection.execute(
            "UPDATE index_vectors SET text_hash=? WHERE ordinal=1", ("0" * 64,)
        )
    with pytest.raises(UploadError, match="INDEX_CONTENT_MISMATCH"):
        asyncio.run(
            LocalIndex(store).index(
                second[0],
                second[1]["reference_id"],
                "index-key-01",
                session_factory=session,
            )
        )
    assert control["sessions"] == 1
    assert (
        store.connection.execute(
            "SELECT state FROM index_generations WHERE id=?",
            (receipt["generation_id"],),
        ).fetchone()[0]
        == "complete"
    )
    assert (
        IndexState(store).status(second[0], second[1]["reference_id"])["state"]
        == "failed"
    )


def test_unverified_runtime_cleanup_blocks_admission_and_publication(indexed_source):
    store, upload, session, _ = indexed_source
    conversation, uploaded, _ = asyncio.run(upload())

    @asynccontextmanager
    async def uncertain():
        async with session() as embedder:
            yield embedder
            store.recovery_pending = True
            raise UploadError("OLLAMA_CLEANUP_PENDING", 503)

    with pytest.raises(UploadError, match="OLLAMA_CLEANUP_PENDING"):
        asyncio.run(
            LocalIndex(store).index(
                conversation,
                uploaded["reference_id"],
                "index-key-01",
                session_factory=uncertain,
            )
        )
    assert store.recovery_pending
    assert (
        store.connection.execute("SELECT count(*) FROM index_vectors").fetchone()[0]
        == 0
    )
    assert (
        store.connection.execute("SELECT state FROM index_generations").fetchone()[0]
        == "processing"
    )


@pytest.mark.parametrize("boundary", ["intent", "during", "after"])
def test_process_exit_recovers_atomic_index(tmp_path, boundary):
    import subprocess
    import sys

    source = """
import asyncio, os, sys
from contextlib import asynccontextmanager
from pathlib import Path
from app.storage.files import UploadStore
from app.storage.documents import Documents
from app.storage.extractions import Extractions
from app.retrieval.embeddings import Embedding, EmbeddingBatch
from app.retrieval.index import LocalIndex
store = UploadStore(Path(sys.argv[1]))
async def main():
    async def stream():
        yield b"Name,Units\\nNorth,42\\n"
    c = Documents(store.connection).create_conversation()
    u = await store.receive(stream(), c, "upload-index-01", "authored.csv")
    await Extractions(store).extract(c, u["reference_id"], "extract-index-01")
    class Fake:
        async def documents(self, chunks):
            return EmbeddingBatch("document", tuple(Embedding(x.chunk_id,x.text_hash,(1.0,)+(0.0,)*767) for x in chunks),None)
    @asynccontextmanager
    async def session():
        if sys.argv[2] == "intent": os._exit(72)
        store.busy = True
        try: yield Fake()
        finally: store.busy = False
    original = store.reserve_growth
    def reserve(size=0):
        original(size)
        if sys.argv[2] == "during" and size>3072: os._exit(72)
    store.reserve_growth = reserve
    await LocalIndex(store).index(c,u["reference_id"],"index-key-01",session_factory=session)
    os._exit(72)
asyncio.run(main())
"""
    result = subprocess.run(
        [sys.executable, "-c", source, str(tmp_path), boundary],
        capture_output=True,
        check=False,
        timeout=15,
    )
    assert result.returncode == 72, result.stderr
    store = UploadStore(tmp_path)
    try:
        assert not store.recovery_pending
        assert store.connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        row = store.connection.execute(
            "SELECT state,error_code FROM index_generations"
        ).fetchone()
        assert row["state"] == ("complete" if boundary == "after" else "failed")
        assert store.connection.execute(
            "SELECT count(*) FROM index_vectors"
        ).fetchone()[0] == int(boundary == "after")
        if boundary != "after":
            assert row["error_code"] == "INDEX_INTERRUPTED"
    finally:
        store.close()
