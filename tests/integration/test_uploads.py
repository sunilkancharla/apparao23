"""Untrusted CSV upload validation and the local attachment boundary."""

import asyncio
import io
import json
import os
import subprocess
import sys
import time
from dataclasses import replace
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.ingestion.validation import UploadError, validate_csv, validate_filename
from app.main import create_app
from app.storage.database import open_database
from app.storage.documents import Documents


@pytest.mark.parametrize(
    "name",
    [
        "../x.csv",
        "a/b.csv",
        "a\\b.csv",
        "C:x.csv",
        "CON.csv",
        "com1.csv",
        "LPT9.backup.csv",
        "a.csv.",
        "a.csv ",
        "a\x00.csv",
        "a?.csv",
        "CON .csv",
    ],
)
def test_unsafe_windows_display_names_are_refused(name):
    with pytest.raises(UploadError, match="INVALID_FILENAME"):
        validate_filename(name)


def test_display_name_is_separate_and_csv_extension_is_required():
    assert validate_filename("Quarterly report.CSV") == "Quarterly report.CSV"
    with pytest.raises(UploadError, match="UNSUPPORTED_FORMAT"):
        validate_filename("report.xlsx")


@pytest.mark.parametrize(
    "body",
    [
        b"",
        b"  \r\n",
        b'a,b\n"unterminated',
        b"a,b\n\xff,2",
        b"a\x00,b\n1,2",
        b"%PDF-1.7\na,b",
        b"PK\x03\x04a,b",
        b"<html>not csv</html>",
    ],
)
def test_invalid_binary_and_mismatched_csv_is_refused(body):
    with pytest.raises(UploadError, match="INVALID_CSV"):
        validate_csv(io.BytesIO(body))


def test_csv_validation_accepts_bom_quoted_newlines_and_inert_instructions():
    body = b'\xef\xbb\xbfitem,note\r\nA,"line one\nline two"\r\nB,=1+1\r\n'
    validate_csv(io.BytesIO(body))


@pytest.fixture
def upload_app(tmp_path):
    settings = replace(
        Settings.from_env({}),
        data_root=tmp_path / "app",
        model_root=tmp_path / "models",
    )
    connection = open_database(settings.data_root)
    first = Documents(connection).create_conversation()
    second = Documents(connection).create_conversation()
    connection.close()
    with TestClient(create_app(settings), base_url=settings.origin) as client:
        token = client.get("/api/session").json()["data"]["csrf_token"]
        client.headers.update({"Origin": settings.origin, "X-CSRF-Token": token})
        yield client, settings, first, second


def upload(client, conversation, body=b"item,total\nA,12\n", **headers):
    return client.post(
        f"/api/conversations/{conversation}/attachments",
        content=body,
        headers={
            "Content-Type": "text/csv",
            "X-Filename": "report.csv",
            "Idempotency-Key": "upload-intent-0001",
            **headers,
        },
    )


def test_upload_persists_original_and_scoped_reference(upload_app):
    client, settings, first, second = upload_app
    response = upload(client, first)
    assert response.status_code == 202, response.text
    data = response.json()["data"]
    assert data["state"] == "original_stored"
    assert data["indexed"] is False
    connection = open_database(settings.data_root)
    try:
        reference = Documents(connection).resolve(first, data["reference_id"])
        assert reference.document_id == data["document_id"]
        assert Documents(connection).resolve(second, data["reference_id"]) is None
        assert (
            settings.data_root / "originals" / reference.content_hash
        ).read_bytes() == b"item,total\nA,12\n"
    finally:
        connection.close()
    assert list((settings.data_root / "staging").iterdir()) == []
    assert str(settings.data_root) not in response.text


def test_replay_verifies_body_and_does_not_consume_another_reference(upload_app):
    client, settings, first, _ = upload_app
    original = upload(client, first)
    replay = upload(client, first)
    assert original.json() == replay.json()
    conflict = upload(client, first, body=b"item,total\nA,99\n")
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "IDEMPOTENCY_CONFLICT"
    connection = open_database(settings.data_root)
    assert len(Documents(connection).references(first)) == 1
    connection.close()


def test_same_bytes_in_different_conversations_share_only_physical_content(upload_app):
    client, settings, first, second = upload_app
    a, b = upload(client, first).json()["data"], upload(client, second).json()["data"]
    assert a["document_id"] != b["document_id"]
    assert a["reference_id"] != b["reference_id"]
    assert len(list((settings.data_root / "originals").iterdir())) == 1


@pytest.mark.parametrize(
    "headers,status",
    [
        ({"X-Filename": "../escape.csv"}, 422),
        ({"X-Filename": "book.xlsx"}, 415),
        ({"Content-Type": "text/html"}, 415),
        ({"Idempotency-Key": "bad"}, 422),
        ({"Content-Length": "100000001"}, 413),
        ({"X-CSRF-Token": "wrong"}, 403),
        ({"Origin": "http://evil.example"}, 403),
    ],
)
def test_bad_upload_metadata_has_safe_errors_and_no_file(upload_app, headers, status):
    client, settings, first, _ = upload_app
    response = upload(client, first, **headers)
    assert response.status_code == status, response.text
    assert "error" in response.json()
    assert str(settings.data_root) not in response.text
    assert response.headers["cache-control"] == "no-store"
    assert not list((settings.data_root / "originals").iterdir())


def test_invalid_csv_cleans_partial_bytes_and_persists_no_membership(upload_app):
    client, settings, first, _ = upload_app
    response = upload(client, first, body=b'secret,"unfinished')
    assert response.status_code == 422
    assert "secret" not in response.text
    assert not list((settings.data_root / "staging").iterdir())
    assert not list((settings.data_root / "originals").iterdir())
    connection = open_database(settings.data_root)
    assert Documents(connection).references(first) == []
    connection.close()


def test_unknown_conversation_never_creates_bytes(upload_app):
    client, _, _, _ = upload_app
    assert upload(client, str(uuid4())).status_code == 404


def test_v1_metadata_migrates_without_losing_ownership(tmp_path):
    import sqlite3

    from app.storage.database import APPLICATION_ID, SCHEMA_V1, SCHEMA_VERSION

    path = tmp_path / "metadata.sqlite3"
    with sqlite3.connect(path) as old:
        for statement in SCHEMA_V1:
            old.execute(statement)
        old.execute("INSERT INTO conversations VALUES ('existing')")
        old.execute(f"PRAGMA application_id={APPLICATION_ID}")
        old.execute("PRAGMA user_version=1")
    migrated = open_database(tmp_path)
    assert migrated.execute("SELECT id FROM conversations").fetchone()[0] == "existing"
    assert migrated.execute("PRAGMA user_version").fetchone()[0] == SCHEMA_VERSION
    assert migrated.execute("SELECT count(*) FROM uploads").fetchone()[0] == 0
    migrated.close()


def test_upload_store_refuses_a_second_owner_and_releases_on_close(tmp_path):
    from app.storage.files import UploadStore

    first = UploadStore(tmp_path)
    with pytest.raises(UploadError, match="STORAGE_UNAVAILABLE"):
        UploadStore(tmp_path)
    first.close()
    UploadStore(tmp_path).close()


def test_admission_reserves_before_any_body_write_and_pending_is_not_retried(tmp_path):
    from app.storage.files import UploadStore

    store = UploadStore(tmp_path)
    try:
        conversation = Documents(store.connection).create_conversation()
        row, replay = store.admit(conversation, "a" * 16, "sample.csv")
        assert not replay
        assert row["original_reserved"] == 100_000_000
        assert row["temp_reserved"] == 100_000_000
        assert not list((tmp_path / "staging").iterdir())
        with pytest.raises(UploadError, match="UPLOAD_PENDING"):
            store.admit(conversation, "a" * 16, "sample.csv")
    finally:
        store.close()


def test_owned_partial_upload_is_removed_on_reopen_without_replaying_intent(tmp_path):
    from app.storage.files import UploadStore

    store = UploadStore(tmp_path)
    conversation = Documents(store.connection).create_conversation()
    operation, _ = store.admit(conversation, "a" * 16, "sample.csv")
    (tmp_path / "staging" / operation["id"]).write_bytes(b"partial")
    store.close()
    store = UploadStore(tmp_path)
    try:
        assert not list((tmp_path / "staging").iterdir())
        row = store.connection.execute("SELECT * FROM uploads").fetchone()
        assert row["state"] == "failed"
        assert row["original_reserved"] == row["temp_reserved"] == 0
        assert Documents(store.connection).references(conversation) == []
    finally:
        store.close()


def test_streamed_size_is_enforced_without_trusting_declared_length(
    upload_app, monkeypatch
):
    from app.storage import files

    client, settings, first, _ = upload_app
    monkeypatch.setattr(files, "MAX_FILE_BYTES", 8)
    accepted = upload(client, first, body=iter([b"a,b\n", b"1,2\n"]))
    assert accepted.status_code == 202
    refused = upload(
        client,
        first,
        body=iter([b"a,b\n", b"1,22\n"]),
        **{"Idempotency-Key": "another-intent-0002"},
    )
    assert refused.status_code == 413
    assert not list((settings.data_root / "staging").iterdir())
    assert len(list((settings.data_root / "originals").iterdir())) == 1


def test_wrong_content_length_does_not_publish_bytes(upload_app):
    client, settings, first, _ = upload_app
    response = upload(client, first, **{"Content-Length": "1"})
    assert response.status_code == 400
    assert not list((settings.data_root / "originals").iterdir())


def test_ten_references_includes_duplicates_but_verified_replay_is_free(upload_app):
    client, _, first, _ = upload_app
    responses = [
        upload(client, first, **{"Idempotency-Key": f"upload-intent-{i:04}"})
        for i in range(10)
    ]
    assert all(r.status_code == 202 for r in responses)
    assert len({r.json()["data"]["reference_id"] for r in responses}) == 10
    assert (
        upload(client, first, **{"Idempotency-Key": "upload-intent-0000"}).json()
        == responses[0].json()
    )
    assert (
        upload(client, first, **{"Idempotency-Key": "upload-intent-0010"}).status_code
        == 413
    )


@pytest.mark.parametrize("category", ["TEMP_CAP", "CONVERSATION_CAP", "PROCESSED_CAP"])
def test_quota_refusal_precedes_materializing_original_bytes(
    upload_app, monkeypatch, category
):
    from app.storage import files

    client, settings, first, _ = upload_app
    monkeypatch.setattr(files, category, 0)
    response = upload(client, first)
    assert response.status_code == 507
    assert not list((settings.data_root / "staging").iterdir())
    assert not list((settings.data_root / "originals").iterdir())


def test_partial_disk_write_failure_cleans_only_its_owned_stage(
    upload_app, monkeypatch
):
    client, settings, first, _ = upload_app
    original_open = Path.open

    class PartialWriter:
        def __init__(self, stream):
            self.stream = stream

        def write(self, part):
            self.stream.write(part[:2])
            raise OSError("synthetic full disk with private details")

        def close(self):
            self.stream.close()

    def fail_write(path, mode="r", *args, **kwargs):
        stream = original_open(path, mode, *args, **kwargs)
        return (
            PartialWriter(stream)
            if path.parent.name == "staging" and mode == "xb"
            else stream
        )

    monkeypatch.setattr(Path, "open", fail_write)
    response = upload(client, first)
    assert response.status_code == 503
    assert "private" not in response.text
    assert not list((settings.data_root / "staging").iterdir())
    assert not list((settings.data_root / "originals").iterdir())


@pytest.mark.parametrize("shared", [False, True])
def test_metadata_failure_after_promotion_preserves_shared_bytes_only(
    upload_app, monkeypatch, shared
):
    from app.storage.database import StorageError

    client, settings, first, second = upload_app
    if shared:
        assert upload(client, second).status_code == 202

    def refuse(*args):
        raise StorageError("synthetic transaction failure")

    monkeypatch.setattr(Documents, "_content", refuse)
    response = upload(client, first)
    assert response.status_code == 503
    assert len(list((settings.data_root / "originals").iterdir())) == int(shared)
    connection = open_database(settings.data_root)
    assert Documents(connection).references(first) == []
    connection.close()


def test_cleanup_failure_retains_reservations_and_blocks_new_admission(
    upload_app, monkeypatch
):
    client, settings, first, _ = upload_app
    unlink = Path.unlink

    def locked(path, *args, **kwargs):
        if path.parent.name == "staging":
            raise PermissionError("private path locked")
        return unlink(path, *args, **kwargs)

    monkeypatch.setattr(Path, "unlink", locked)
    response = upload(client, first, body=b'header,"unfinished')
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "CLEANUP_PENDING"
    assert (
        upload(client, first, **{"Idempotency-Key": "new-upload-intent"}).status_code
        == 409
    )
    connection = open_database(settings.data_root)
    row = connection.execute("SELECT * FROM uploads").fetchone()
    assert row["state"] == "cleanup_pending"
    assert row["temp_reserved"] == row["original_reserved"] == 100_000_000
    connection.close()


def test_cancelled_transfer_cleans_and_does_not_publish(tmp_path):
    from app.storage.files import UploadStore

    store = UploadStore(tmp_path)
    conversation = Documents(store.connection).create_conversation()

    async def cancelled():
        yield b"a,b\n"
        raise asyncio.CancelledError

    try:
        with pytest.raises(asyncio.CancelledError):
            asyncio.run(store.receive(cancelled(), conversation, "a" * 16, "a.csv"))
        assert not list((tmp_path / "staging").iterdir())
        assert Documents(store.connection).references(conversation) == []
    finally:
        store.close()


def test_reparse_or_hardlinked_storage_is_refused_without_deleting_target(tmp_path):
    from app.storage.files import UploadStore

    external = tmp_path / "keep.csv"
    external.write_bytes(b"a,b\n1,2\n")
    root = tmp_path / "managed"
    root.mkdir()
    os.link(external, root / "untrusted.csv")
    with pytest.raises(UploadError, match="STORAGE_UNAVAILABLE"):
        UploadStore(root)
    assert external.read_bytes() == b"a,b\n1,2\n"


@pytest.mark.parametrize("point", ["before_commit", "after_commit"])
def test_process_exit_at_publication_boundaries_reconciles_once(tmp_path, point):
    from app.storage.files import UploadStore

    child = r"""
import asyncio, json, os, sys
from pathlib import Path
from app.storage.files import UploadStore
from app.storage.documents import Documents
store = UploadStore(Path(sys.argv[1]))
conversation = Documents(store.connection).create_conversation()
print(json.dumps(conversation), flush=True)
original_content = Documents._content
def stop_before_commit(self, *args):
    original_content(self, *args)
    os._exit(23)
def stop_after_commit(*args):
    os._exit(23)
if sys.argv[2] == 'before_commit':
    Documents._content = stop_before_commit
else:
    store._result = stop_after_commit
async def body():
    yield b'a,b\n1,2\n'
asyncio.run(store.receive(body(), conversation, 'a'*16, 'test.csv'))
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
    conversation = json.loads(result.stdout)
    store = UploadStore(tmp_path)
    try:
        row = store.connection.execute("SELECT * FROM uploads").fetchone()
        stored = point == "after_commit"
        assert row["state"] == ("original_stored" if stored else "failed")
        assert row["temp_reserved"] == row["original_reserved"] == 0
        assert len(Documents(store.connection).references(conversation)) == int(stored)
        assert len(list((tmp_path / "originals").iterdir())) == int(stored)
        assert not list((tmp_path / "staging").iterdir())
        assert store.connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    finally:
        store.close()


def test_real_loopback_upload_with_missing_model_prerequisites(tmp_path):
    import httpx

    from app.diagnostics import reserve_port

    root = tmp_path / "app"
    connection = open_database(root)
    conversation = Documents(connection).create_conversation()
    connection.close()
    with reserve_port(0) as probe:
        port = probe.getsockname()[1]
    origin = f"http://127.0.0.1:{port}"
    environment = {k: v for k, v in os.environ.items() if not k.startswith("DA_")}
    environment.update(
        DA_PORT=str(port),
        DA_DATA_ROOT=str(root),
        DA_MODEL_ROOT=str(tmp_path / "models"),
        DA_OLLAMA_EXECUTABLE=str(tmp_path / "missing.exe"),
    )
    with subprocess.Popen(
        [sys.executable, "-m", "app.main"],
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    ) as server:
        try:
            with httpx.Client(base_url=origin, trust_env=False, timeout=2) as client:
                deadline = time.monotonic() + 10
                while True:
                    try:
                        response = client.get("/api/session")
                        break
                    except (httpx.ConnectError, httpx.ConnectTimeout):
                        assert server.poll() is None and time.monotonic() < deadline
                        time.sleep(0.05)
                token = response.json()["data"]["csrf_token"]
                client.headers.update({"Origin": origin, "X-CSRF-Token": token})
                accepted = upload(client, conversation)
                assert accepted.status_code == 202
                rejected = upload(
                    client,
                    conversation,
                    body=b'private,"broken',
                    **{"Idempotency-Key": "bad-upload-000001"},
                )
                assert rejected.status_code == 422
                batch = client.post(
                    f"/api/conversations/{conversation}/attachment-batches",
                    json={"files": ["a.csv", "b.csv"]},
                    headers={"Idempotency-Key": "batch-intent-001"},
                )
                assert batch.status_code == 202
                entries = batch.json()["data"]["files"]
                for index, (name, body, status) in enumerate(
                    (
                        ("a.csv", b"a,b\n1,2\n", 202),
                        ("b.csv", b'a,"private broken', 422),
                    )
                ):
                    response = upload(
                        client,
                        conversation,
                        body=body,
                        **{
                            "Idempotency-Key": f"batch-upload-{index:04}",
                            "X-Filename": name,
                            "X-Batch-File-Id": entries[index]["operation_id"],
                        },
                    )
                    assert response.status_code == status
                polled = client.get(
                    f"/api/operations/{batch.json()['data']['operation_id']}",
                    params={"conversation_id": conversation},
                )
                assert polled.status_code == 200
                assert polled.json()["data"]["state"] == "partial_failure"
                assert polled.json()["data"]["originals_stored"] == 1
                source_base = f"/api/conversations/{conversation}/references/{accepted.json()['data']['reference_id']}"
                extracted = client.post(
                    source_base + "/extractions",
                    headers={"Idempotency-Key": "extract-intent-01"},
                )
                assert extracted.status_code == 202
                assert extracted.json()["data"]["state"] == "awaiting_index"
                preview = client.get(source_base + "/preview")
                assert preview.status_code == 200
                assert [cell["value"] for cell in preview.json()["data"]["units"]] == [
                    "A",
                    "12",
                ]
                assert all(
                    cell["record"] == 1 and cell["line_start"] == 2
                    for cell in preview.json()["data"]["units"]
                )
        finally:
            server.terminate()
            stdout, stderr = server.communicate(timeout=5)
    assert b"private" not in stdout + stderr
    assert token.encode() not in stdout + stderr
    connection = open_database(root)
    assert len(Documents(connection).references(conversation)) == 2
    connection.close()


def test_foreign_csrf_and_duplicate_or_encoded_metadata_cannot_upload(upload_app):
    client, settings, first, _ = upload_app
    route = f"/api/conversations/{first}/attachments"
    for name in ("..%2Fescape.csv", "a%00.csv", "CON.csv", "%FF.csv", "%zz.csv"):
        assert upload(client, first, **{"X-Filename": name}).status_code == 422
    response = client.post(
        route,
        content=b"a,b\n1,2\n",
        headers=[
            ("Content-Type", "text/csv"),
            ("X-Filename", "a.csv"),
            ("X-Filename", "b.csv"),
            ("Idempotency-Key", "intent-key-000001"),
        ],
    )
    assert response.status_code == 422
    client.headers.pop("X-CSRF-Token")
    assert upload(client, first).status_code == 403
    assert not list((settings.data_root / "originals").iterdir())


def test_sqlite_growth_ceiling_refuses_real_large_write_and_rolls_back(tmp_path):
    from app.storage.files import UploadStore

    store = UploadStore(tmp_path)
    try:
        pages = store.connection.execute("PRAGMA page_count").fetchone()[0]
        with pytest.raises(UploadError) as failure, store._write():
            store.connection.execute(
                "INSERT INTO conversations VALUES (hex(zeroblob(1000000)))"
            )
        assert failure.value.status == 507
        assert (
            store.connection.execute("SELECT count(*) FROM conversations").fetchone()[0]
            == 0
        )
        assert store.connection.execute("PRAGMA page_count").fetchone()[0] <= pages + 16
        assert not (tmp_path / "metadata.sqlite3-journal").exists()
    finally:
        store.close()


def test_reopen_uses_same_processed_bound_as_running_store(tmp_path, monkeypatch):
    from app.storage import files

    store = files.UploadStore(tmp_path)
    store.close()
    size = (tmp_path / "metadata.sqlite3").stat().st_size
    monkeypatch.setattr(files, "PROCESSED_CAP", 1_048_576 + size * 9 // 2 + 1)
    files.UploadStore(tmp_path).close()


def test_missing_committed_original_is_unavailable_and_not_recreated(upload_app):
    client, settings, first, _ = upload_app
    response = upload(client, first)
    assert response.status_code == 202
    original = next((settings.data_root / "originals").iterdir())
    original.unlink()
    replay = upload(client, first)
    assert replay.status_code == 410
    assert not list((settings.data_root / "originals").iterdir())


def test_concurrent_transfer_is_busy_and_does_not_admit_another_intent(tmp_path):
    from app.storage.files import UploadStore

    store = UploadStore(tmp_path)
    conversation = Documents(store.connection).create_conversation()

    async def scenario():
        started, release = asyncio.Event(), asyncio.Event()

        async def body():
            started.set()
            await release.wait()
            yield b"a,b\n1,2\n"

        first = asyncio.create_task(
            store.receive(body(), conversation, "a" * 16, "a.csv")
        )
        await started.wait()
        try:
            with pytest.raises(UploadError, match="UPLOAD_BUSY"):
                await store.receive(body(), conversation, "b" * 16, "a.csv")
        finally:
            release.set()
            await first

    try:
        asyncio.run(scenario())
        assert len(Documents(store.connection).references(conversation)) == 1
        assert (
            store.connection.execute("SELECT count(*) FROM uploads").fetchone()[0] == 1
        )
    finally:
        store.close()
