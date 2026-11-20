"""Saved citation previews use actual scoped storage and injected inference only."""

import asyncio
import json
from uuid import uuid4

import pytest

from app.ingestion.validation import UploadError
from app.storage.documents import Documents
from app.storage.messages import Messages
from tests.integration import test_chat

configured = test_chat.configured
retrieval = test_chat.retrieval


@pytest.fixture
def cited(retrieval, request):
    from app.chat.citations import Citations

    store, add, _, _, _ = retrieval
    conversation, reference = asyncio.run(
        add(getattr(request, "param", b"Name,Units\nNorth,42\nSouth,50\n"))
    )
    Messages(store).select(conversation, [reference], 0)
    chat, _ = configured(retrieval)
    saved = asyncio.run(chat.ask(conversation, "citation-answer-01", "North units?", 1))
    citation = saved["answer"]["claims"][0]["citations"][0]
    return store, conversation, reference, saved, citation, Citations(store)


def remove_reference(store, reference):
    """Simulate logical detachment using the existing foreign-key order."""
    with store._write():
        for table in ("index_requests", "csv_requests", "document_references"):
            column = "id" if table == "document_references" else "reference_id"
            store.connection.execute(
                f"DELETE FROM {table} WHERE {column}=?", (reference,)
            )


def test_saved_citation_resolves_exact_source_cells_and_does_not_write_snapshots(cited):
    store, conversation, reference, saved, citation, service = cited
    before = store.connection.total_changes
    preview = asyncio.run(service.preview(conversation, saved["answer_id"], citation))
    assert preview["reference_id"] == reference
    assert preview["filename"] == "authored.csv" and preview["escaped"]
    values = [p for p in preview["passages"] if p["role"] == "data"]
    assert [p["quote"] for p in values] == ["North", "42"]
    assert all(p["location"]["record_start"] == 1 for p in values)
    assert all(p["location"]["line_start"] == 2 for p in values)
    assert [p["location"]["columns"][0]["position"] for p in values] == [1, 2]
    assert store.connection.total_changes == before
    assert Messages(store).get(conversation, saved["answer_id"]) == saved


@pytest.mark.parametrize("damage", ["missing", "bytes", "membership", "index"])
def test_unavailable_sources_block_live_preview_but_label_readable_saved_answer(
    cited, damage
):
    store, conversation, reference, saved, citation, service = cited
    if damage == "missing":
        next((store.root / "originals").iterdir()).unlink()
    elif damage == "bytes":
        next((store.root / "originals").iterdir()).write_bytes(b"corrupt")
    elif damage == "membership":
        remove_reference(store, reference)
    else:
        store.connection.execute("UPDATE index_generations SET state='failed'")
    with pytest.raises(UploadError) as error:
        asyncio.run(service.preview(conversation, saved["answer_id"], citation))
    assert error.value.status == 410
    historical = asyncio.run(service.read(conversation, saved["answer_id"]))
    assert historical["answer"] == saved["answer"]
    assert historical["source_availability"] == "unavailable"
    assert historical["citations"][0]["availability"] == "unavailable"
    assert not any("quote" in c for c in historical["citations"])


def test_unknown_or_foreign_answer_and_uncited_supplied_id_cannot_preview(cited):
    store, conversation, _, saved, citation, service = cited
    other = Documents(store.connection).create_conversation()
    for conv, answer, evidence in (
        (other, saved["answer_id"], citation),
        (conversation, str(uuid4()), citation),
        (conversation, saved["answer_id"], str(uuid4())),
    ):
        with pytest.raises(UploadError) as error:
            asyncio.run(service.preview(conv, answer, evidence))
        assert error.value.status == 404
    unused = next(e for e in saved["evidence"] if e["evidence_id"] != citation)
    with pytest.raises(UploadError) as error:
        asyncio.run(
            service.preview(conversation, saved["answer_id"], unused["evidence_id"])
        )
    assert error.value.status == 404


@pytest.mark.parametrize("field", ["filename", "locations", "text_hash", "quote"])
def test_saved_metadata_cannot_override_real_provenance(cited, field):
    store, conversation, _, saved, citation, service = cited
    manifest = saved["evidence"]
    item = next(e for e in manifest if e["evidence_id"] == citation)
    item[field] = {
        "filename": "invented.csv",
        "locations": [],
        "text_hash": "f" * 64,
        "quote": "fabricated",
    }[field]
    store.connection.execute(
        "UPDATE chat_exchanges SET evidence_json=?", (json.dumps(manifest),)
    )
    with pytest.raises(UploadError):
        asyncio.run(service.preview(conversation, saved["answer_id"], citation))


def test_reference_change_while_hashing_is_rechecked_before_preview(cited, monkeypatch):
    store, conversation, reference, saved, citation, service = cited

    async def changed(function, *args, **kwargs):
        function(*args, **kwargs)
        remove_reference(store, reference)

    monkeypatch.setattr("app.chat.citations.asyncio.to_thread", changed)
    with pytest.raises(UploadError) as error:
        asyncio.run(service.preview(conversation, saved["answer_id"], citation))
    assert error.value.status == 410


def test_busy_store_blocks_preview_without_clearing_the_owners_slot(cited):
    store, conversation, _, saved, citation, service = cited
    store.busy = True
    try:
        with pytest.raises(UploadError) as error:
            asyncio.run(service.preview(conversation, saved["answer_id"], citation))
        assert error.value.status == 409 and store.busy
    finally:
        store.busy = False


@pytest.fixture
def citation_api(cited):
    from dataclasses import replace

    from fastapi.testclient import TestClient

    from app.config import Settings
    from app.main import create_app

    store, conversation, _, saved, citation, _ = cited
    settings = replace(
        Settings.from_env({}),
        data_root=store.root,
        model_root=store.root / "unused-models",
    )
    store.close()
    try:
        with TestClient(create_app(settings), base_url=settings.origin) as client:
            live_store = client.app.state.upload_store
            assert live_store is not None
            base = f"/api/conversations/{conversation}/sources/{citation}"
            yield client, base, saved, live_store, conversation, settings
    finally:
        # Reacquire the fixture's store owner for its metered teardown after the
        # API owner releases the Windows lock and its thread-bound connection.
        store.__init__(store.root)


def test_http_live_preview_and_saved_answer_availability_are_scoped(citation_api):
    client, base, saved, store, conversation, _ = citation_api
    response = client.get(base, params={"answer_id": saved["answer_id"]})
    assert response.status_code == 200, response.text
    assert len(response.content) <= 65_536
    assert response.headers["cache-control"] == "no-store"
    assert response.json()["data"]["escaped"]
    other = client.portal.call(
        lambda: Documents(store.connection).create_conversation()
    )
    assert (
        client.get(
            base.replace(conversation, other), params={"answer_id": saved["answer_id"]}
        ).status_code
        == 404
    )
    result = client.get(
        f"/api/conversations/{conversation}/answers/{saved['answer_id']}"
    ).json()["data"]
    assert result["source_availability"] == "available"
    assert result["answer"] == saved["answer"]
    assert all("quote" not in c for c in result["citations"])


@pytest.mark.parametrize(
    "query",
    [
        [],
        [("answer_id", "bad")],
        [("answer_id", "ID"), ("path", "../private.csv")],
        [("answer_id", "ID"), ("answer_id", "ID")],
        [("answer_id", "ID"), ("quote", "invented")],
    ],
)
def test_http_preview_rejects_missing_duplicate_or_untrusted_query(citation_api, query):
    client, base, saved, _, _, _ = citation_api
    response = client.get(
        base, params=[(k, saved["answer_id"] if v == "ID" else v) for k, v in query]
    )
    assert response.status_code == 422
    assert "private.csv" not in response.text and "invented" not in response.text


@pytest.mark.parametrize(
    "cited", [b'Name,Units\n"<script>alert(1)</script>&",42\n'], indirect=True
)
def test_http_preview_escapes_source_markup_and_preserves_exact_underlying_quote(
    citation_api,
):
    client, base, saved, store, _, settings = citation_api
    response = client.get(base, params={"answer_id": saved["answer_id"]})
    assert response.status_code == 200
    assert "<script>" not in response.text and "&lt;script&gt;" in response.text
    assert str(settings.data_root) not in response.text
    payload = client.portal.call(
        lambda: store.connection.execute(
            "SELECT payload FROM csv_units ORDER BY ordinal LIMIT 1"
        ).fetchone()[0]
    )
    assert "<script>" in json.loads(payload)["text"]


def test_http_missing_source_labels_history_without_revealing_quote_or_path(
    citation_api,
):
    client, base, saved, store, conversation, settings = citation_api
    next((store.root / "originals").iterdir()).unlink()
    response = client.get(base, params={"answer_id": saved["answer_id"]})
    assert response.status_code == 410
    assert "North" not in response.text and str(settings.data_root) not in response.text
    response = client.get(
        f"/api/conversations/{conversation}/answers/{saved['answer_id']}"
    )
    assert response.status_code == 200
    assert response.json()["data"]["answer"] == saved["answer"]
    assert response.json()["data"]["source_availability"] == "unavailable"


def test_preview_serialization_budget_applies_after_escaping(cited, monkeypatch):
    _, conversation, _, saved, citation, service = cited
    monkeypatch.setattr(
        "app.chat.citations.checked_passages", lambda *args: [{"quote": "<" * 20000}]
    )
    with pytest.raises(UploadError, match="PREVIEW_LIMIT"):
        asyncio.run(service.preview(conversation, saved["answer_id"], citation))


@pytest.mark.parametrize("state", ["busy", "recovery_pending"])
def test_historical_read_stays_available_when_live_revalidation_is_busy(cited, state):
    store, conversation, _, saved, _, service = cited
    setattr(store, state, True)
    try:
        result = asyncio.run(service.read(conversation, saved["answer_id"]))
        assert result["answer"] == saved["answer"]
        assert result["source_availability"] == "not_revalidated"
        assert all(c["availability"] == "not_revalidated" for c in result["citations"])
        assert getattr(store, state)
    finally:
        setattr(store, state, False)


@pytest.mark.parametrize("failure", ["permission", "unsafe_path"])
def test_unreadable_or_unsafe_originals_fail_with_a_safe_unavailable_code(
    cited, monkeypatch, failure
):
    from app.config import ConfigurationError

    store, conversation, _, saved, citation, service = cited

    def refused(*args):
        error = PermissionError if failure == "permission" else ConfigurationError
        raise error("private filesystem detail")

    monkeypatch.setattr(store, "_verified_original", refused)
    with pytest.raises(UploadError) as error:
        asyncio.run(service.preview(conversation, saved["answer_id"], citation))
    assert error.value.status == 410
    assert error.value.code == "SOURCE_UNAVAILABLE"
    assert not store.busy
