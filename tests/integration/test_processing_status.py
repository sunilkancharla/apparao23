"""Durable batch admission and honest, conversation-scoped upload status."""

import asyncio
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from app.ingestion.validation import UploadError
from app.storage.documents import Documents
from app.storage.files import UploadStore


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
    conversation, other = (
        Documents(connection).create_conversation(),
        Documents(connection).create_conversation(),
    )
    connection.close()
    with TestClient(create_app(settings), base_url=settings.origin) as client:
        token = client.get("/api/session").json()["data"]["csrf_token"]
        client.headers.update({"Origin": settings.origin, "X-CSRF-Token": token})
        yield client, settings, conversation, other


def create_batch(client, conversation, names, key="batch-intent-0001"):
    return client.post(
        f"/api/conversations/{conversation}/attachment-batches",
        json={"files": names},
        headers={"Idempotency-Key": key},
    )


def send_file(client, conversation, file_id, name, body, key):
    return client.post(
        f"/api/conversations/{conversation}/attachments",
        content=body,
        headers={
            "Content-Type": "text/csv",
            "Idempotency-Key": key,
            "X-Filename": name,
            "X-Batch-File-Id": file_id,
        },
    )


def test_batch_api_reports_mixed_results_and_scoped_operation_ids(api):
    client, settings, conversation, other = api
    response = create_batch(client, conversation, ["a.csv", "b.csv", "book.xlsx"])
    assert response.status_code == 202, response.text
    batch = response.json()["data"]
    a, b, _ = [f["operation_id"] for f in batch["files"]]
    assert (
        send_file(
            client, conversation, a, "a.csv", b"a,b\n1,2\n", "upload-intent-01"
        ).status_code
        == 202
    )
    assert (
        send_file(
            client, conversation, b, "b.csv", b'a,"broken', "upload-intent-02"
        ).status_code
        == 422
    )
    for identity in (batch["operation_id"], a, b):
        result = client.get(
            f"/api/operations/{identity}", params={"conversation_id": conversation}
        )
        assert result.status_code == 200
        assert result.headers["cache-control"] == "no-store"
        assert str(settings.data_root) not in result.text
        assert (
            client.get(
                f"/api/operations/{identity}", params={"conversation_id": other}
            ).status_code
            == 404
        )
    result = client.get(
        f"/api/operations/{batch['operation_id']}",
        params={"conversation_id": conversation},
    ).json()["data"]
    assert result["originals_stored"] == 1 and result["failed_files"] == 2
    assert result["state"] == "partial_failure" and not result["ready"]


@pytest.mark.parametrize("names,status", [([], 413), (["a.csv"] * 11, 413), ([1], 422)])
def test_batch_api_rejects_invalid_shape_without_creating_files(api, names, status):
    client, settings, conversation, _ = api
    assert create_batch(client, conversation, names).status_code == status
    assert not list((settings.data_root / "originals").iterdir())


@pytest.fixture
def operations(tmp_path):
    from app.ingestion.processing import UploadOperations

    store = UploadStore(tmp_path)
    conversation = Documents(store.connection).create_conversation()
    try:
        yield UploadOperations(store), store, conversation
    finally:
        store.close()


def test_exact_v2_database_migrates_and_preserves_a_committed_reference(tmp_path):
    import sqlite3

    from app.storage.database import (
        APPLICATION_ID,
        SCHEMA_V2,
        SCHEMA_VERSION,
        open_database,
    )

    with sqlite3.connect(tmp_path / "metadata.sqlite3") as old:
        for statement in SCHEMA_V2:
            old.execute(statement)
        old.execute(f"PRAGMA application_id={APPLICATION_ID}")
        old.execute("PRAGMA user_version=2")
        conversation = Documents(old).create_conversation()
        reference = Documents(old).add_attachment(conversation, "1" * 64, 8, "csv")
    connection = open_database(tmp_path)
    try:
        assert connection.execute("PRAGMA user_version").fetchone()[0] == SCHEMA_VERSION
        assert (
            connection.execute("SELECT count(*) FROM upload_batches").fetchone()[0] == 0
        )
        assert (
            Documents(connection).resolve(conversation, reference.reference_id)
            == reference
        )
    finally:
        connection.close()


def test_standalone_upload_status_is_awaiting_extraction_not_ready(operations):
    service, store, conversation = operations

    async def body():
        yield b"a,b\n1,2\n"

    receipt = asyncio.run(
        store.receive(body(), conversation, "upload-intent-01", "a.csv")
    )
    result = service.status(conversation, receipt["operation_id"])
    assert result["state"] == "awaiting_extraction"
    assert result["bytes_stored"] == 8
    assert not result["ready"] and not result["indexed"]
    assert result["reference_id"] == receipt["reference_id"]


def test_batch_is_durable_queued_and_idempotent_without_body_files(operations):
    service, store, conversation = operations
    first = service.create_batch(conversation, "batch-intent-0001", ["a.csv", "b.csv"])
    assert first["state"] == "queued"
    assert first["total_files"] == 2
    assert all(
        item["state"] == "queued" and not item["ready"] for item in first["files"]
    )
    assert first == service.create_batch(
        conversation, "batch-intent-0001", ["a.csv", "b.csv"]
    )
    assert not list((store.root / "staging").iterdir())
    assert not list((store.root / "originals").iterdir())
    assert service.status(conversation, first["operation_id"]) == first
    with pytest.raises(UploadError, match="IDEMPOTENCY_CONFLICT"):
        service.create_batch(conversation, "batch-intent-0001", ["b.csv", "a.csv"])


def test_invalid_file_metadata_does_not_discard_valid_siblings_or_echo_paths(
    operations,
):
    service, _, conversation = operations
    result = service.create_batch(
        conversation, "batch-intent-0001", ["good.csv", "book.xlsx", "../private.csv"]
    )
    assert [f["state"] for f in result["files"]] == ["queued", "failed", "failed"]
    assert result["files"][1]["error_code"] == "UNSUPPORTED_FORMAT"
    assert result["files"][2]["display_name"] is None
    assert "private" not in str(result)


@pytest.mark.parametrize("names", [[], ["a.csv"] * 11])
def test_batch_file_count_is_bounded_before_persistence(operations, names):
    service, store, conversation = operations
    with pytest.raises(UploadError, match="BATCH_LIMIT"):
        service.create_batch(conversation, "batch-intent-0001", names)
    assert (
        store.connection.execute("SELECT count(*) FROM upload_batches").fetchone()[0]
        == 0
    )


def test_pending_batch_slots_cannot_be_stolen_by_a_single_upload(operations):
    service, store, conversation = operations
    service.create_batch(conversation, "batch-intent-0001", ["a.csv"] * 10)
    with pytest.raises(UploadError, match="REFERENCE_LIMIT"):
        store.admit(conversation, "standalone-intent", "standalone.csv")


def test_operation_lookup_requires_matching_conversation(operations):
    service, store, conversation = operations
    batch = service.create_batch(conversation, "batch-intent-0001", ["a.csv"])
    other = Documents(store.connection).create_conversation()
    for identity in (batch["operation_id"], batch["files"][0]["operation_id"]):
        with pytest.raises(UploadError, match="OPERATION_NOT_FOUND"):
            service.status(other, identity)


def test_mixed_uploads_persist_specific_failures_and_verified_retry(operations):
    service, store, conversation = operations
    batch = service.create_batch(conversation, "batch-intent-0001", ["a.csv", "b.csv"])
    first, second = [f["operation_id"] for f in batch["files"]]

    async def body(value):
        yield value

    async def scenario():
        receipt = await store.receive(
            body(b"a,b\n1,2\n"),
            conversation,
            "first-upload-key",
            "a.csv",
            batch_file=first,
        )
        assert receipt == await store.receive(
            body(b"a,b\n1,2\n"),
            conversation,
            "first-upload-key",
            "a.csv",
            batch_file=first,
        )
        with pytest.raises(UploadError, match="INVALID_CSV"):
            await store.receive(
                body(b'a,"private unfinished'),
                conversation,
                "second-upload-key",
                "b.csv",
                batch_file=second,
            )

    asyncio.run(scenario())
    result = service.status(conversation, batch["operation_id"])
    assert result["state"] == "partial_failure"
    assert result["originals_stored"] == result["failed_files"] == 1
    assert result["files"][1]["error_code"] == "INVALID_CSV"
    assert "private" not in str(result)
    assert not result["ready"] and not result["indexed"]

    async def retry():
        await store.receive(
            body(b"a,b\n3,4\n"),
            conversation,
            "replacement-key-1",
            "b.csv",
            batch_file=second,
        )

    asyncio.run(retry())
    assert (
        service.status(conversation, batch["operation_id"])["state"]
        == "awaiting_extraction"
    )
    assert len(Documents(store.connection).references(conversation)) == 2


def test_polling_observes_processing_and_unknown_progress_during_transfer(operations):
    service, store, conversation = operations
    batch = service.create_batch(conversation, "batch-intent-0001", ["a.csv"])
    file_id = batch["files"][0]["operation_id"]

    async def body():
        status = service.status(conversation, file_id)
        assert status["state"] == "processing"
        assert status["bytes_stored"] is None
        assert not status["ready"]
        yield b"a,b\n1,2\n"

    asyncio.run(
        store.receive(
            body(), conversation, "first-upload-key", "a.csv", batch_file=file_id
        )
    )


def test_wrong_manifest_scope_or_name_never_consumes_a_reserved_slot(operations):
    service, store, conversation = operations
    batch = service.create_batch(conversation, "batch-intent-0001", ["a.csv"])
    file_id = batch["files"][0]["operation_id"]
    other = Documents(store.connection).create_conversation()
    for target, name, code in (
        (conversation, "b.csv", "BATCH_FILE_MISMATCH"),
        (other, "a.csv", "OPERATION_NOT_FOUND"),
    ):
        with pytest.raises(UploadError, match=code):
            store.admit(target, "first-upload-key", name, file_id)
    assert service.status(conversation, file_id)["state"] == "queued"
    assert store.connection.execute("SELECT count(*) FROM uploads").fetchone()[0] == 0


def test_locked_restart_cleanup_is_visible_and_preserves_successful_sibling(
    tmp_path, monkeypatch
):
    from app.ingestion.processing import UploadOperations

    store = UploadStore(tmp_path)
    conversation = Documents(store.connection).create_conversation()
    service = UploadOperations(store)
    batch = service.create_batch(conversation, "batch-intent-0001", ["a.csv", "b.csv"])
    a, b = [f["operation_id"] for f in batch["files"]]

    async def body():
        yield b"a,b\n1,2\n"

    asyncio.run(
        store.receive(body(), conversation, "first-upload-key", "a.csv", batch_file=a)
    )
    pending, _ = store.admit(conversation, "second-upload-key", "b.csv", b)
    (tmp_path / "staging" / pending["id"]).write_bytes(b"partial")
    store.close()
    unlink = Path.unlink

    def locked(path, *args, **kwargs):
        if path.parent.name == "staging":
            raise PermissionError("private lock details")
        return unlink(path, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(Path, "unlink", locked)
        reopened = UploadStore(tmp_path)
        try:
            service = UploadOperations(reopened)
            result = service.status(conversation, batch["operation_id"])
            assert reopened.recovery_pending
            assert result["files"][0]["state"] == "awaiting_extraction"
            assert result["files"][1]["state"] == "cleanup_pending"
            assert "private" not in str(result)
            with pytest.raises(UploadError, match="UPLOAD_PENDING"):
                reopened.admit(conversation, "another-upload-key", "b.csv", b)
        finally:
            reopened.close()
    recovered = UploadStore(tmp_path)
    try:
        result = UploadOperations(recovered).status(conversation, batch["operation_id"])
        assert result["state"] == "partial_failure"
        assert result["files"][1]["state"] == "interrupted"
        assert not list((tmp_path / "staging").iterdir())
        assert len(Documents(recovered.connection).references(conversation)) == 1
    finally:
        recovered.close()


def test_failed_retry_reacquires_a_slot_instead_of_exceeding_capacity(operations):
    service, store, conversation = operations
    batch = service.create_batch(conversation, "batch-intent-0001", ["a.csv"])
    file_id = batch["files"][0]["operation_id"]

    async def body(value):
        yield value

    with pytest.raises(UploadError, match="INVALID_CSV"):
        asyncio.run(
            store.receive(
                body(b'a,"broken'),
                conversation,
                "first-upload-key",
                "a.csv",
                batch_file=file_id,
            )
        )
    service.create_batch(conversation, "replacement-batch", ["b.csv"] * 10)
    with pytest.raises(UploadError, match="REFERENCE_LIMIT"):
        asyncio.run(
            store.receive(
                body(b"a,b\n1,2\n"),
                conversation,
                "replacement-key-1",
                "a.csv",
                batch_file=file_id,
            )
        )
    assert service.status(conversation, file_id)["state"] == "failed"
    assert store.connection.execute("SELECT count(*) FROM uploads").fetchone()[0] == 1


def test_all_ten_reserved_files_can_finish_without_double_counting(operations):
    service, store, conversation = operations
    batch = service.create_batch(conversation, "batch-intent-0001", ["a.csv"] * 10)

    async def body():
        yield b"a,b\n1,2\n"

    for i, item in enumerate(batch["files"]):
        asyncio.run(
            store.receive(
                body(),
                conversation,
                f"upload-intent-{i:04}",
                "a.csv",
                batch_file=item["operation_id"],
            )
        )
    result = service.status(conversation, batch["operation_id"])
    assert result["originals_stored"] == 10 and not result["ready"]
    assert len(list((store.root / "originals").iterdir())) == 1
    assert len(Documents(store.connection).references(conversation)) == 10
    with pytest.raises(UploadError, match="REFERENCE_LIMIT"):
        service.create_batch(conversation, "one-more-intent1", ["b.csv"])


def test_oversized_bound_file_is_a_persisted_failure_before_reading_body(api):
    client, _, conversation, _ = api
    batch = create_batch(client, conversation, ["a.csv"]).json()["data"]
    file_id = batch["files"][0]["operation_id"]
    response = client.post(
        f"/api/conversations/{conversation}/attachments",
        content=b"never stored",
        headers={
            "Content-Type": "text/csv",
            "X-Filename": "a.csv",
            "X-Batch-File-Id": file_id,
            "Idempotency-Key": "upload-intent-01",
            "Content-Length": "100000001",
        },
    )
    assert response.status_code == 413
    result = client.get(
        f"/api/operations/{file_id}", params={"conversation_id": conversation}
    ).json()["data"]
    assert result["state"] == "failed" and result["error_code"] == "FILE_TOO_LARGE"


@pytest.mark.parametrize(
    "body,status",
    [
        (b'{"files":[],"files":["a.csv"]}', 400),
        (b"[", 400),
        (b'{"files":["a.csv"],"extra":true}', 422),
        (b'{"files":["a.csv"]}' + b" " * 32768, 413),
    ],
)
def test_batch_metadata_is_bounded_and_rejects_ambiguous_json(api, body, status):
    client, settings, conversation, _ = api
    response = client.post(
        f"/api/conversations/{conversation}/attachment-batches",
        content=iter([body[:10], body[10:]]),
        headers={
            "Content-Type": "application/json",
            "Idempotency-Key": "batch-intent-001",
        },
    )
    assert response.status_code == status
    assert str(settings.data_root) not in response.text


def test_batch_csrf_scope_binding_and_payload_identity_are_enforced(api):
    client, _, conversation, other = api
    batch = create_batch(client, conversation, ["a.csv"]).json()["data"]
    assert create_batch(client, conversation, ["b.csv"]).status_code == 409
    file_id = batch["files"][0]["operation_id"]
    assert (
        send_file(
            client, other, file_id, "a.csv", b"a,b\n1,2\n", "upload-intent-01"
        ).status_code
        == 404
    )
    assert (
        send_file(
            client, conversation, file_id, "b.csv", b"a,b\n1,2\n", "upload-intent-01"
        ).status_code
        == 409
    )
    assert client.get(f"/api/operations/{file_id}").status_code == 422
    client.headers.pop("X-CSRF-Token")
    assert (
        create_batch(client, conversation, ["a.csv"], "another-batch-key").status_code
        == 403
    )


@pytest.mark.parametrize("point", ["receiving", "committed"])
def test_batch_state_survives_abrupt_exit_without_replaying_effects(tmp_path, point):
    from app.ingestion.processing import UploadOperations

    child = r"""
import asyncio, json, os, sys
from pathlib import Path
from app.ingestion.processing import UploadOperations
from app.storage.documents import Documents
from app.storage.files import UploadStore
store = UploadStore(Path(sys.argv[1]))
conversation = Documents(store.connection).create_conversation()
batch = UploadOperations(store).create_batch(conversation, 'batch-intent-0001', ['a.csv','b.csv'])
a, b = [f['operation_id'] for f in batch['files']]
print(json.dumps([conversation, batch['operation_id']]), flush=True)
async def body(value):
    yield value
asyncio.run(store.receive(body(b'a,b\n1,2\n'), conversation, 'first-upload-key', 'a.csv', batch_file=a))
if sys.argv[2] == 'receiving':
    pending, _ = store.admit(conversation, 'second-upload-key', 'b.csv', b)
    (store.root / 'staging' / pending['id']).write_bytes(b'partial')
    os._exit(23)
def stop(row):
    os._exit(23)
store._result = stop
asyncio.run(store.receive(body(b'a,b\n3,4\n'), conversation, 'second-upload-key', 'b.csv', batch_file=b))
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
    conversation, identity = json.loads(result.stdout)
    store = UploadStore(tmp_path)
    try:
        status = UploadOperations(store).status(conversation, identity)
        count = 1 if point == "receiving" else 2
        assert status["originals_stored"] == count
        assert status["files"][1]["state"] == (
            "interrupted" if count == 1 else "awaiting_extraction"
        )
        assert len(Documents(store.connection).references(conversation)) == count
        assert not list((tmp_path / "staging").iterdir())
        assert not status["ready"]
        assert store.connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    finally:
        store.close()


def test_batch_metadata_transaction_rolls_back_all_file_rows(operations, monkeypatch):
    from app.ingestion import processing

    service, store, conversation = operations
    monkeypatch.setattr(
        processing, "uuid4", lambda: "00000000-0000-4000-8000-000000000000"
    )
    with pytest.raises(UploadError, match="STORAGE_WRITE_FAILED"):
        service.create_batch(conversation, "batch-intent-0001", ["a.csv", "b.csv"])
    assert (
        store.connection.execute("SELECT count(*) FROM upload_batches").fetchone()[0]
        == 0
    )
    assert (
        store.connection.execute("SELECT count(*) FROM upload_batch_files").fetchone()[
            0
        ]
        == 0
    )


def test_managed_quota_refusal_leaves_unstarted_file_queued(api, monkeypatch):
    from app.storage import files

    client, _, conversation, _ = api
    batch = create_batch(client, conversation, ["a.csv"]).json()["data"]
    file_id = batch["files"][0]["operation_id"]
    monkeypatch.setattr(files, "TEMP_CAP", 0)
    assert (
        send_file(
            client, conversation, file_id, "a.csv", b"a,b\n1,2\n", "upload-intent-01"
        ).status_code
        == 507
    )
    result = client.get(
        f"/api/operations/{file_id}", params={"conversation_id": conversation}
    )
    assert result.json()["data"]["state"] == "queued"
