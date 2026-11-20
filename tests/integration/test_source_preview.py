"""Normalized CSV storage and scoped previews never expose unrelated originals."""

import asyncio
import json
import subprocess
import sys
from dataclasses import replace

import pytest

from app.ingestion.validation import UploadError
from app.storage.documents import Documents
from app.storage.files import UploadStore


@pytest.fixture
def source(tmp_path):
    store = UploadStore(tmp_path)
    conversation = Documents(store.connection).create_conversation()
    other = Documents(store.connection).create_conversation()

    async def body():
        yield b'Name,Units\n"Apex, West",10\n"Line\nBreak",20\n'

    receipt = asyncio.run(
        store.receive(body(), conversation, "upload-intent-01", "example.csv")
    )
    try:
        yield store, conversation, other, receipt
    finally:
        store.close()


def test_growth_reservation_can_expand_inside_a_real_transaction_and_roll_back(
    tmp_path,
):
    store = UploadStore(tmp_path)
    try:
        with pytest.raises(RuntimeError), store._write():
            store.reserve_growth(200_000)
            store.connection.execute(
                "INSERT INTO conversations VALUES (hex(zeroblob(70000)))"
            )
            store.reserve_growth(200_000)
            store.connection.execute(
                "INSERT INTO conversations VALUES (hex(zeroblob(70001)))"
            )
            raise RuntimeError("deliberate rollback")
        assert (
            store.connection.execute("SELECT count(*) FROM conversations").fetchone()[0]
            == 0
        )
        assert store.connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    finally:
        store.close()


def test_exact_v3_migration_preserves_prior_upload_schema(tmp_path):
    import sqlite3

    from app.storage.database import (
        APPLICATION_ID,
        SCHEMA_V3,
        SCHEMA_VERSION,
        open_database,
    )

    with sqlite3.connect(tmp_path / "metadata.sqlite3") as old:
        for statement in SCHEMA_V3:
            old.execute(statement)
        old.execute(f"PRAGMA application_id={APPLICATION_ID}")
        old.execute("PRAGMA user_version=3")
    connection = open_database(tmp_path)
    try:
        assert connection.execute("PRAGMA user_version").fetchone()[0] == SCHEMA_VERSION
        assert (
            connection.execute("SELECT count(*) FROM csv_extractions").fetchone()[0]
            == 0
        )
    finally:
        connection.close()


def test_normalized_storage_resolves_only_attached_source_metadata(source):
    from app.storage.extractions import Extractions

    store, conversation, other, uploaded = source
    service = Extractions(store)
    row = service._source(conversation, uploaded["reference_id"])
    assert row["document_id"] == uploaded["document_id"]
    assert row["display_name"] == "example.csv" and row["format"] == "csv"
    with pytest.raises(UploadError, match="SOURCE_NOT_FOUND"):
        service._source(other, uploaded["reference_id"])


def test_extraction_is_atomic_versioned_idempotent_and_keeps_original_bytes(source):
    from app.storage.extractions import Extractions

    store, conversation, _, uploaded = source
    service = Extractions(store)
    before = next((store.root / "originals").iterdir()).read_bytes()
    result = asyncio.run(
        service.extract(conversation, uploaded["reference_id"], "extract-intent-01")
    )
    assert result["state"] == "awaiting_index" and not result["indexed"]
    assert result["record_count"] == 2 and result["unit_count"] == 4
    assert result == asyncio.run(
        service.extract(conversation, uploaded["reference_id"], "extract-intent-01")
    )
    assert (
        result["extraction_id"]
        == asyncio.run(
            service.extract(conversation, uploaded["reference_id"], "extract-intent-02")
        )["extraction_id"]
    )
    assert (
        store.connection.execute(
            "SELECT count(*) FROM csv_extractions WHERE state='complete'"
        ).fetchone()[0]
        == 1
    )
    assert next((store.root / "originals").iterdir()).read_bytes() == before


def test_unrelated_reference_cannot_extract_or_preview(source):
    from app.storage.extractions import Extractions

    store, _, other, uploaded = source
    service = Extractions(store)
    with pytest.raises(UploadError, match="SOURCE_NOT_FOUND"):
        asyncio.run(
            service.extract(other, uploaded["reference_id"], "extract-intent-01")
        )
    with pytest.raises(UploadError, match="SOURCE_NOT_FOUND"):
        asyncio.run(service.preview(other, uploaded["reference_id"]))


def test_preview_is_bounded_paginated_and_traceable_to_multiline_cells(source):
    from app.ingestion.models import NormalizedExtraction
    from app.storage.extractions import Extractions

    store, conversation, _, uploaded = source
    service = Extractions(store)
    receipt = asyncio.run(
        service.extract(conversation, uploaded["reference_id"], "extract-intent-01")
    )
    first = asyncio.run(
        service.preview(conversation, uploaded["reference_id"], limit=2)
    )
    second = asyncio.run(
        service.preview(
            conversation, uploaded["reference_id"], after=first["next_after"], limit=2
        )
    )
    assert first["next_after"] == 2 and second["next_after"] is None
    assert second["units"][0]["value"] == "Line\nBreak"
    assert (second["units"][0]["line_start"], second["units"][0]["line_end"]) == (3, 4)
    row = store.connection.execute("SELECT manifest FROM csv_extractions").fetchone()
    units = [
        json.loads(r[0])
        for r in store.connection.execute(
            "SELECT payload FROM csv_units ORDER BY ordinal"
        )
    ]
    restored = NormalizedExtraction.model_validate(
        {**json.loads(row[0]), "units": units}
    )
    assert restored.extraction_id == receipt["extraction_id"]
    assert restored.units[2].cells[1].text == "Line\nBreak"


def test_missing_original_blocks_cached_preview_without_recreating_source(source):
    from app.storage.extractions import Extractions

    store, conversation, _, uploaded = source
    service = Extractions(store)
    asyncio.run(
        service.extract(conversation, uploaded["reference_id"], "extract-intent-01")
    )
    next((store.root / "originals").iterdir()).unlink()
    with pytest.raises(UploadError, match="SOURCE_UNAVAILABLE"):
        asyncio.run(service.preview(conversation, uploaded["reference_id"]))
    assert not list((store.root / "originals").iterdir())


@pytest.fixture
def api(tmp_path):
    from fastapi.testclient import TestClient

    from app.config import Settings
    from app.main import create_app
    from app.storage.database import open_database

    settings = replace(
        Settings.from_env({}),
        data_root=tmp_path / "app",
        model_root=tmp_path / "models",
    )
    connection = open_database(settings.data_root)
    a, b = (
        Documents(connection).create_conversation(),
        Documents(connection).create_conversation(),
    )
    connection.close()
    with TestClient(create_app(settings), base_url=settings.origin) as client:
        client.headers.update(
            {
                "Origin": settings.origin,
                "X-CSRF-Token": client.get("/api/session").json()["data"]["csrf_token"],
            }
        )
        uploaded = client.post(
            f"/api/conversations/{a}/attachments",
            content=b'A,B\n"<script>x</script>",20\n',
            headers={
                "Content-Type": "text/csv",
                "X-Filename": "table.csv",
                "Idempotency-Key": "upload-intent-01",
            },
        ).json()["data"]
        yield client, settings, a, b, uploaded


def test_api_upload_extraction_preview_and_operation_state_are_scoped(api):
    client, settings, a, b, uploaded = api
    base = f"/api/conversations/{a}/references/{uploaded['reference_id']}"
    response = client.post(
        base + "/extractions", headers={"Idempotency-Key": "extract-intent-01"}
    )
    assert response.status_code == 202, response.text
    assert response.json()["data"]["state"] == "awaiting_index"
    preview = client.get(base + "/preview")
    assert preview.status_code == 200
    assert preview.headers["cache-control"] == "no-store"
    assert (
        preview.json()["data"]["units"][0]["value"] == "&lt;script&gt;x&lt;/script&gt;"
    )
    assert (
        "<script>" not in preview.text and str(settings.data_root) not in preview.text
    )
    assert (
        client.get(
            f"/api/conversations/{b}/references/{uploaded['reference_id']}/preview"
        ).status_code
        == 404
    )
    status = client.get(
        f"/api/operations/{uploaded['operation_id']}", params={"conversation_id": a}
    ).json()["data"]
    assert status["state"] == "awaiting_index" and not status["ready"]
    extraction = response.json()["data"]["extraction_id"]
    assert (
        client.get(
            f"/api/operations/{extraction}", params={"conversation_id": a}
        ).status_code
        == 200
    )
    assert (
        client.get(
            f"/api/operations/{extraction}", params={"conversation_id": b}
        ).status_code
        == 404
    )


@pytest.mark.parametrize(
    "query",
    [
        {"after": "../private"},
        {"after": "-1"},
        {"limit": "51"},
        {"path": "private.csv"},
        {"after": "999999999999999999999999"},
    ],
)
def test_preview_rejects_paths_and_bad_bounds_without_echoing_values(api, query):
    client, _, a, _, uploaded = api
    response = client.get(
        f"/api/conversations/{a}/references/{uploaded['reference_id']}/preview",
        params=query,
    )
    assert response.status_code == 422
    assert "private" not in response.text


def test_failure_after_first_normalized_insert_rolls_back_all_units(
    source, monkeypatch
):
    from app.storage.extractions import Extractions

    store, conversation, _, uploaded = source
    reserve = store.reserve_growth
    observed = []

    def fail_later(size=0):
        count = store.connection.execute("SELECT count(*) FROM csv_units").fetchone()[0]
        if count:
            observed.append(count)
            raise UploadError("PROCESSED_QUOTA", 507)
        return reserve(size)

    monkeypatch.setattr(store, "reserve_growth", fail_later)
    with pytest.raises(UploadError, match="PROCESSED_QUOTA"):
        asyncio.run(
            Extractions(store).extract(
                conversation, uploaded["reference_id"], "extract-intent-01"
            )
        )
    assert observed == [1]
    assert store.connection.execute("SELECT count(*) FROM csv_units").fetchone()[0] == 0
    assert (
        store.connection.execute("SELECT state FROM csv_extractions").fetchone()[0]
        == "failed"
    )
    assert len(list((store.root / "originals").iterdir())) == 1


@pytest.mark.parametrize("point", ["in_transaction", "committed"])
def test_real_exit_cannot_publish_partial_normalized_units(tmp_path, point):
    child = r"""
import asyncio, json, os, sys
from pathlib import Path
from app.storage.documents import Documents
from app.storage.files import UploadStore
from app.storage.extractions import Extractions
store = UploadStore(Path(sys.argv[1]))
conversation = Documents(store.connection).create_conversation()
async def body():
    yield b'A,B\n1,2\n3,4\n'
uploaded = asyncio.run(store.receive(body(), conversation, 'upload-intent-01', 'data.csv'))
print(json.dumps([conversation, uploaded['reference_id']]), flush=True)
service = Extractions(store)
reserve = store.reserve_growth
def stop_during(size=0):
    if store.connection.execute('SELECT count(*) FROM csv_units').fetchone()[0]:
        os._exit(23)
    return reserve(size)
def stop_after(row):
    os._exit(23)
if sys.argv[2] == 'in_transaction':
    store.reserve_growth = stop_during
else:
    service._receipt = stop_after
asyncio.run(service.extract(conversation, uploaded['reference_id'], 'extract-intent-01'))
"""
    result = subprocess.run(
        [sys.executable, "-c", child, str(tmp_path), point],
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    assert result.returncode == 23
    conversation, reference = json.loads(result.stdout)
    reopened = UploadStore(tmp_path)
    try:
        committed = point == "committed"
        row = reopened.connection.execute("SELECT * FROM csv_extractions").fetchone()
        assert row["state"] == ("complete" if committed else "failed")
        assert reopened.connection.execute("SELECT count(*) FROM csv_units").fetchone()[
            0
        ] == (4 if committed else 0)
        assert (
            Documents(reopened.connection).resolve(conversation, reference) is not None
        )
        assert (
            reopened.connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        )
        from app.storage.extractions import Extractions

        service = Extractions(reopened)
        if not committed:
            with pytest.raises(UploadError, match="EXTRACTION_INTERRUPTED"):
                asyncio.run(
                    service.extract(conversation, reference, "extract-intent-01")
                )
        receipt = asyncio.run(
            service.extract(
                conversation,
                reference,
                "extract-intent-01" if committed else "extract-intent-02",
            )
        )
        assert receipt["unit_count"] == 4
        assert (
            reopened.connection.execute("SELECT count(*) FROM csv_units").fetchone()[0]
            == 4
        )
    finally:
        reopened.close()


def test_preview_body_budget_and_large_cells_preserve_full_normalized_data(source):
    from app.storage.extractions import Extractions

    store, conversation, _, _ = source

    async def body(value):
        yield value

    large = "ä" * 40_000
    uploaded = asyncio.run(
        store.receive(
            body(("Long\n" + large + "\n").encode()),
            conversation,
            "upload-large-001",
            "large.csv",
        )
    )
    service = Extractions(store)
    receipt = asyncio.run(
        service.extract(conversation, uploaded["reference_id"], "extract-large-01")
    )
    payload = store.connection.execute(
        "SELECT payload FROM csv_units WHERE extraction_id=?",
        (receipt["extraction_id"],),
    ).fetchone()[0]
    assert json.loads(payload)["text"] == large
    first = asyncio.run(service.preview(conversation, uploaded["reference_id"]))
    assert first["units"][0]["value_truncated"]
    assert "�" not in first["units"][0]["value"]
    text = "&" * 300
    uploaded = asyncio.run(
        store.receive(
            body(((text + "\n") * 61).encode()),
            conversation,
            "upload-many-0001",
            "many.csv",
        )
    )
    asyncio.run(
        service.extract(conversation, uploaded["reference_id"], "extract-many-001")
    )
    after, ordinals = 0, []
    while True:
        page = asyncio.run(
            service.preview(
                conversation, uploaded["reference_id"], after=after, limit=50
            )
        )
        assert (
            len(
                json.dumps(
                    {"data": page}, ensure_ascii=False, separators=(",", ":")
                ).encode()
            )
            <= 65_536
        )
        assert all(
            item["value_truncated"] and item["header_truncated"]
            for item in page["units"]
        )
        ordinals += [item["ordinal"] for item in page["units"]]
        if page["next_after"] is None:
            break
        assert page["next_after"] > after
        after = page["next_after"]
    assert ordinals == list(range(1, 61))


def test_empty_data_records_fail_without_losing_original_and_old_key_is_not_retried(
    source,
):
    from app.storage.extractions import Extractions

    store, conversation, _, _ = source

    async def body():
        yield b"A,B\n,\n"

    uploaded = asyncio.run(
        store.receive(body(), conversation, "upload-empty-001", "empty.csv")
    )
    service = Extractions(store)
    for status in (422, 409):
        with pytest.raises(UploadError, match="EMPTY_CSV") as error:
            asyncio.run(
                service.extract(
                    conversation, uploaded["reference_id"], "extract-empty-01"
                )
            )
        assert error.value.status == status
    assert store.connection.execute("SELECT count(*) FROM csv_units").fetchone()[0] == 0
    assert len(list((store.root / "originals").iterdir())) == 2


def test_corrupt_original_does_not_serve_a_cached_normalized_preview(source):
    from app.storage.extractions import Extractions

    store, conversation, _, uploaded = source
    service = Extractions(store)
    asyncio.run(
        service.extract(conversation, uploaded["reference_id"], "extract-intent-01")
    )
    original = next((store.root / "originals").iterdir())
    original.write_bytes(original.read_bytes().replace(b",20", b",99"))
    with pytest.raises(UploadError, match="SOURCE_UNAVAILABLE"):
        asyncio.run(service.preview(conversation, uploaded["reference_id"]))


def test_status_can_poll_during_transaction_but_mutations_and_preview_are_busy(source):
    from app.ingestion.processing import UploadOperations
    from app.storage.extractions import Extractions

    store, conversation, _, _ = source

    async def body():
        yield ("A,B\n" + "1,2\n" * 40).encode()

    uploaded = asyncio.run(
        store.receive(body(), conversation, "upload-many-0001", "many.csv")
    )
    service = Extractions(store)

    async def scenario():
        task = asyncio.create_task(
            service.extract(conversation, uploaded["reference_id"], "extract-many-001")
        )
        try:
            while not (
                store.connection.in_transaction
                and store.connection.execute(
                    "SELECT count(*) FROM csv_units"
                ).fetchone()[0]
            ):
                assert not task.done()
                await asyncio.sleep(0)
            operations = UploadOperations(store)
            status = operations.status(conversation, uploaded["operation_id"])
            assert status["state"] == "extracting" and not status["ready"]
            with pytest.raises(UploadError, match="UPLOAD_BUSY"):
                operations.create_batch(conversation, "batch-intent-001", ["x.csv"])
            with pytest.raises(UploadError, match="UPLOAD_BUSY"):
                await service.preview(conversation, uploaded["reference_id"])
        finally:
            await task

    asyncio.run(scenario())


def test_unwritable_failure_record_blocks_admission_and_reconciles_on_restart(
    source, monkeypatch
):
    from app.ingestion.processing import UploadOperations
    from app.storage import files
    from app.storage.extractions import Extractions

    store, conversation, _, uploaded = source
    reserve = store.reserve_growth
    with monkeypatch.context() as patch:

        def exhaust(size=0):
            if store.connection.execute("SELECT count(*) FROM csv_units").fetchone()[0]:
                patch.setattr(files, "PROCESSED_CAP", 0)
            return reserve(size)

        patch.setattr(store, "reserve_growth", exhaust)
        with pytest.raises(UploadError, match="EXTRACTION_PENDING"):
            asyncio.run(
                Extractions(store).extract(
                    conversation, uploaded["reference_id"], "extract-intent-01"
                )
            )
        assert store.recovery_pending
        assert (
            store.connection.execute("SELECT count(*) FROM csv_units").fetchone()[0]
            == 0
        )
        status = UploadOperations(store).status(conversation, uploaded["operation_id"])
        assert status["state"] == "cleanup_pending"
        with pytest.raises(UploadError, match="UPLOAD_BUSY"):
            UploadOperations(store).create_batch(
                conversation, "batch-intent-001", ["x.csv"]
            )
    root = store.root
    store.close()
    recovered = UploadStore(root)
    try:
        assert not recovered.recovery_pending
        assert (
            recovered.connection.execute(
                "SELECT state FROM csv_extractions"
            ).fetchone()[0]
            == "failed"
        )
        assert len(list((root / "originals").iterdir())) == 1
    finally:
        recovered.close()


def test_extraction_post_requires_csrf_and_refuses_body_payloads(api, caplog):
    client, _, a, _, uploaded = api
    route = f"/api/conversations/{a}/references/{uploaded['reference_id']}/extractions"
    response = client.post(
        route,
        content=b"PRIVATE_MARKER",
        headers={"Idempotency-Key": "extract-intent-01"},
    )
    assert response.status_code == 400
    assert "PRIVATE_MARKER" not in response.text + caplog.text
    client.headers.pop("X-CSRF-Token")
    assert (
        client.post(route, headers={"Idempotency-Key": "extract-intent-01"}).status_code
        == 403
    )
