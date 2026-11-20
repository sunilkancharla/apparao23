"""Real atomic exchange storage, scoped selections and restart behavior."""

import sqlite3

import pytest

from app.ingestion.validation import UploadError
from app.storage.database import APPLICATION_ID, SCHEMA_V5, open_database
from app.storage.documents import Documents
from app.storage.files import UploadStore
from app.storage.messages import Messages


def test_exact_v5_migration_keeps_prior_tables(tmp_path):
    connection = sqlite3.connect(tmp_path / "metadata.sqlite3")
    for statement in SCHEMA_V5:
        connection.execute(statement)
    connection.execute("INSERT INTO conversations VALUES ('kept')")
    connection.execute(f"PRAGMA application_id={APPLICATION_ID}")
    connection.execute("PRAGMA user_version=5")
    connection.commit()
    connection.close()
    connection = open_database(tmp_path)
    try:
        assert connection.execute("PRAGMA user_version").fetchone()[0] == 6
        assert (
            connection.execute("SELECT id FROM conversations").fetchone()[0] == "kept"
        )
        assert (
            connection.execute("SELECT count(*) FROM chat_requests").fetchone()[0] == 0
        )
    finally:
        connection.close()


@pytest.fixture
def messages(tmp_path):
    store = UploadStore(tmp_path)
    conversation = Documents(store.connection).create_conversation()
    other = Documents(store.connection).create_conversation()
    try:
        yield store, Messages(store), conversation, other
    finally:
        store.close()


def test_selection_revision_scope_and_idempotency(messages):
    store, service, conversation, other = messages
    reference = (
        Documents(store.connection)
        .add_attachment(conversation, "1" * 64, 10, "csv")
        .reference_id
    )
    assert service.selection(conversation) == {"revision": 0, "references": []}
    assert service.select(conversation, [reference], 0)["revision"] == 1
    assert service.select(conversation, [reference], 1)["revision"] == 1
    with pytest.raises(UploadError, match="SOURCE_CHANGED"):
        service.select(conversation, [], 0)
    with pytest.raises(UploadError, match="SOURCE_NOT_FOUND"):
        service.select(other, [reference], 0)


def test_completed_exchange_replay_and_restart(messages):
    store, service, conversation, other = messages
    request = service.admit(conversation, "answer-request-01", "What?", 0)
    answer = {
        "status": "insufficient_evidence",
        "claims": [{"text": "No selected evidence.", "citations": []}],
    }
    service.finish(request["id"], answer, (), [], ["NO_EVIDENCE"])
    stored = service.get(conversation, request["id"])
    assert stored["state"] == "complete" and stored["answer"] == answer
    assert stored["created_at"] and stored["completed_at"]
    assert (
        service.admit(conversation, "answer-request-01", "What?", 0)["id"]
        == request["id"]
    )
    with pytest.raises(UploadError, match="IDEMPOTENCY_CONFLICT"):
        service.admit(conversation, "answer-request-01", "Changed?", 0)
    with pytest.raises(UploadError, match="ANSWER_NOT_FOUND"):
        service.get(other, request["id"])
    root = store.root
    store.close()
    opened = UploadStore(root)
    try:
        assert Messages(opened).get(conversation, request["id"]) == stored
    finally:
        opened.close()
    store.connection = open_database(root)


def test_changed_selection_prevents_publication(messages):
    store, service, conversation, _ = messages
    request = service.admit(conversation, "answer-request-01", "What?", 0)
    reference = (
        Documents(store.connection)
        .add_attachment(conversation, "1" * 64, 10, "csv")
        .reference_id
    )
    service.select(conversation, [reference], 0)
    with pytest.raises(UploadError, match="SOURCE_CHANGED"):
        service.finish(
            request["id"],
            {
                "status": "insufficient_evidence",
                "claims": [{"text": "Nothing.", "citations": []}],
            },
            (),
            [],
            [],
        )
    assert (
        store.connection.execute("SELECT count(*) FROM chat_exchanges").fetchone()[0]
        == 0
    )


def test_processing_request_recovers_as_failed_without_new_messages(messages):
    store, service, conversation, _ = messages
    request = service.admit(conversation, "answer-request-01", "What?", 0)
    from app.storage.messages import recover_messages

    recover_messages(store)
    saved = service.get(conversation, request["id"])
    assert saved["state"] == "failed" and saved["error_code"] == "CHAT_INTERRUPTED"
    assert saved["answer"] is None


def test_processing_key_replay_is_not_a_new_execution(messages):
    _, service, conversation, _ = messages
    first = service.admit(conversation, "answer-request-01", "What?", 0)
    second = service.admit(conversation, "answer-request-01", "What?", 0)
    assert first["admitted_new"] and not second["admitted_new"]
    assert first["id"] == second["id"]


@pytest.mark.parametrize("boundary", ["intent", "after"])
def test_process_exit_preserves_complete_or_interrupted_exchange(tmp_path, boundary):
    import subprocess
    import sys

    source = """
import os,sys
from pathlib import Path
from app.storage.files import UploadStore
from app.storage.documents import Documents
from app.storage.messages import Messages
s=UploadStore(Path(sys.argv[1])); c=Documents(s.connection).create_conversation(); m=Messages(s)
r=m.admit(c,"answer-request-01","What?",0)
if sys.argv[2]=="intent": os._exit(73)
m.finish(r["id"],{"status":"insufficient_evidence","claims":[{"text":"No evidence.","citations":[]}]},(),[],["NO_EVIDENCE"])
os._exit(73)
"""
    result = subprocess.run(
        [sys.executable, "-c", source, str(tmp_path), boundary],
        capture_output=True,
        check=False,
        timeout=15,
    )
    assert result.returncode == 73, result.stderr
    store = UploadStore(tmp_path)
    try:
        assert not store.recovery_pending
        assert store.connection.execute("SELECT state FROM chat_requests").fetchone()[
            0
        ] == ("complete" if boundary == "after" else "failed")
        assert store.connection.execute(
            "SELECT count(*) FROM chat_exchanges"
        ).fetchone()[0] == int(boundary == "after")
        assert store.connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    finally:
        store.close()
