"""Real SQLite ownership, integrity, transaction and reopen checks."""

import hashlib
import json
import sqlite3
import subprocess
import sys

import pytest

from app.storage.database import StorageError, open_database, transaction
from app.storage.documents import Documents

HASH = hashlib.sha256(b"synthetic CSV bytes").hexdigest()


@pytest.fixture
def store(tmp_path):
    connection = open_database(tmp_path)
    yield Documents(connection)
    connection.close()


def test_same_content_does_not_share_attachment_visibility(store):
    first, second = store.create_conversation(), store.create_conversation()
    a = store.add_attachment(first, HASH, 19, "csv")
    b = store.add_attachment(second, HASH, 19, "csv")
    assert a.document_id != b.document_id
    assert a.reference_id != b.reference_id
    assert store.references(first) == [a]
    assert store.references(second) == [b]
    assert store.resolve(first, b.reference_id) is None
    assert store.resolve(second, a.reference_id) is None


def test_library_sharing_and_duplicate_reference_reuse(store):
    a, b = store.create_conversation(), store.create_conversation()
    document = store.add_library_document(HASH, 19, "csv")
    first = store.attach_library(a, document)
    second = store.attach_library(b, document)
    assert first.document_id == second.document_id
    assert first.reference_id != second.reference_id
    assert store.attach_library(a, document) == first
    assert len(store.references(a)) == 1
    unrelated = store.create_conversation()
    assert store.references(unrelated) == []
    assert store.resolve(unrelated, first.reference_id) is None


def test_exclusive_document_cannot_be_attached_as_library(store):
    a, b = store.create_conversation(), store.create_conversation()
    exclusive = store.add_attachment(a, HASH, 19, "csv")
    with pytest.raises(StorageError):
        store.attach_library(b, exclusive.document_id)
    assert store.references(b) == []


def test_references_survive_close_and_reopen(tmp_path):
    connection = open_database(tmp_path)
    store = Documents(connection)
    conversation = store.create_conversation()
    reference = store.add_attachment(conversation, HASH, 19, "csv")
    connection.close()
    reopened = open_database(tmp_path)
    try:
        assert (
            Documents(reopened).resolve(conversation, reference.reference_id)
            == reference
        )
        assert reopened.execute("PRAGMA user_version").fetchone()[0] == 1
        assert reopened.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        assert reopened.execute("PRAGMA journal_mode").fetchone()[0] == "delete"
        assert reopened.execute("PRAGMA synchronous").fetchone()[0] == 2
    finally:
        reopened.close()


def test_failed_reference_rolls_back_content_and_document(store):
    with pytest.raises(StorageError):
        store.add_attachment("unknown-conversation", HASH, 19, "csv")
    connection = store.connection
    assert connection.execute("SELECT count(*) FROM content_objects").fetchone()[0] == 0
    assert connection.execute("SELECT count(*) FROM documents").fetchone()[0] == 0


def test_conflicting_content_metadata_preserves_existing_reference(store):
    conversation = store.create_conversation()
    original = store.add_attachment(conversation, HASH, 19, "csv")
    with pytest.raises(StorageError):
        store.add_attachment(conversation, HASH, 20, "csv")
    assert store.references(conversation) == [original]


@pytest.mark.parametrize(
    "digest,size,kind",
    [
        ("bad", 19, "csv"),
        (HASH, -1, "csv"),
        (HASH, True, "csv"),
        (HASH, 100_000_001, "csv"),
        (HASH, 19, "txt"),
    ],
)
def test_invalid_content_metadata_is_rejected(store, digest, size, kind):
    with pytest.raises(StorageError):
        store.add_library_document(digest, size, kind)


def test_reference_limit_is_logical_even_for_identical_bytes(store):
    conversation = store.create_conversation()
    for _ in range(10):
        store.add_attachment(conversation, HASH, 19, "csv")
    with pytest.raises(StorageError):
        store.add_attachment(conversation, HASH, 19, "csv")
    assert len(store.references(conversation)) == 10
    assert (
        store.connection.execute("SELECT count(*) FROM content_objects").fetchone()[0]
        == 1
    )
    assert (
        store.connection.execute("SELECT count(*) FROM documents").fetchone()[0] == 10
    )


def test_database_constraints_block_scope_bypass_and_reassignment(store):
    a, b = store.create_conversation(), store.create_conversation()
    reference = store.add_attachment(a, HASH, 19, "csv")
    with pytest.raises(StorageError), transaction(store.connection):
        store.connection.execute(
            "INSERT INTO document_references VALUES (?, ?, ?)",
            ("forged-reference", b, reference.document_id),
        )
    with pytest.raises(StorageError), transaction(store.connection):
        store.connection.execute("UPDATE documents SET owner_conversation_id=?", (b,))
    with pytest.raises(StorageError), transaction(store.connection):
        store.connection.execute("DELETE FROM conversations WHERE id=?", (a,))
    assert store.references(a) == [reference]


def test_duplicate_reference_constraints_and_sql_parameters(store):
    conversation = store.create_conversation()
    reference = store.add_attachment(conversation, HASH, 19, "csv")
    with pytest.raises(StorageError), transaction(store.connection):
        store.connection.execute(
            "INSERT INTO document_references VALUES (?, ?, ?)",
            ("duplicate", conversation, reference.document_id),
        )
    assert store.resolve("' OR 1=1 --", reference.reference_id) is None
    assert store.references("' OR 1=1 --") == []


def test_explicit_transaction_rollback(store):
    with pytest.raises(RuntimeError), transaction(store.connection):
        store.connection.execute("INSERT INTO conversations VALUES ('rollback')")
        raise RuntimeError("synthetic interrupted operation")
    assert (
        store.connection.execute("SELECT count(*) FROM conversations").fetchone()[0]
        == 0
    )


def test_future_or_unrelated_schema_is_not_modified(tmp_path):
    path = tmp_path / "metadata.sqlite3"
    with sqlite3.connect(path) as connection:
        connection.execute("CREATE TABLE unrelated (value TEXT)")
        connection.execute("PRAGMA user_version=99")
    original = path.read_bytes()
    with pytest.raises(StorageError):
        open_database(tmp_path)
    assert path.read_bytes() == original


def test_model_extensions_and_attach_are_denied(store, tmp_path):
    with pytest.raises(sqlite3.DatabaseError):
        store.connection.execute(
            "ATTACH DATABASE ? AS extra", (str(tmp_path / "other.db"),)
        )
    with pytest.raises(sqlite3.DatabaseError):
        store.connection.execute("SELECT load_extension('not-a-library')")


def test_damaged_current_schema_is_refused_without_repair(tmp_path):
    connection = open_database(tmp_path)
    connection.close()
    path = tmp_path / "metadata.sqlite3"
    with sqlite3.connect(path) as tamper:
        tamper.execute("DROP TRIGGER reference_scope")
    original = path.read_bytes()
    with pytest.raises(StorageError):
        open_database(tmp_path)
    assert path.read_bytes() == original


def test_committed_membership_survives_process_exit_and_partial_write_rolls_back(
    tmp_path,
):
    child = r"""
import json, os, sys
from pathlib import Path
from app.storage.database import open_database
from app.storage.documents import Documents
connection = open_database(Path(sys.argv[1]))
store = Documents(connection)
conversation = store.create_conversation()
reference = store.add_attachment(conversation, sys.argv[2], 19, "csv")
print(json.dumps([conversation, reference.reference_id]), flush=True)
connection.execute("BEGIN IMMEDIATE")
connection.execute("INSERT INTO conversations VALUES ('interrupted')")
os._exit(23)
"""
    result = subprocess.run(
        [sys.executable, "-c", child, str(tmp_path), HASH],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    assert result.returncode == 23
    conversation, reference = json.loads(result.stdout)
    connection = open_database(tmp_path)
    try:
        assert (
            Documents(connection).resolve(conversation, reference).content_hash == HASH
        )
        assert (
            connection.execute("SELECT count(*) FROM conversations").fetchone()[0] == 1
        )
        assert connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    finally:
        connection.close()


def test_library_and_exclusive_documents_share_bytes_without_merging_identity(store):
    conversation = store.create_conversation()
    exclusive = store.add_attachment(conversation, HASH, 19, "csv")
    library = store.add_library_document(HASH, 19, "csv")
    shared = store.attach_library(conversation, library)
    assert exclusive.document_id != shared.document_id
    assert (
        store.connection.execute("SELECT count(*) FROM content_objects").fetchone()[0]
        == 1
    )
    for _ in range(8):
        store.add_attachment(conversation, HASH, 19, "csv")
    assert store.attach_library(conversation, library) == shared


def test_readonly_write_failure_is_safe_and_preserves_references(store):
    conversation = store.create_conversation()
    store.connection.execute("PRAGMA query_only=ON")
    with pytest.raises(StorageError) as error:
        store.add_attachment(conversation, HASH, 19, "csv")
    assert HASH not in str(error.value)
    assert store.references(conversation) == []
