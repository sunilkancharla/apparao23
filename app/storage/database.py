"""Versioned SQLite initialization and explicit atomic metadata writes."""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from app.config import ConfigurationError, prepare_data_root, validate_local_ancestry

APPLICATION_ID = 0x44415331
SCHEMA_VERSION = 6
SCHEMA_V1 = (
    """CREATE TABLE content_objects (
        sha256 TEXT PRIMARY KEY CHECK(length(sha256)=64 AND sha256 NOT GLOB '*[^0-9a-f]*'),
        byte_size INTEGER NOT NULL CHECK(byte_size BETWEEN 0 AND 100000000),
        format TEXT NOT NULL CHECK(format IN ('pdf','xlsx','csv'))
    ) STRICT""",
    "CREATE TABLE conversations (id TEXT PRIMARY KEY) STRICT",
    """CREATE TABLE documents (
        id TEXT PRIMARY KEY,
        content_hash TEXT NOT NULL REFERENCES content_objects(sha256) ON DELETE RESTRICT,
        owner_conversation_id TEXT REFERENCES conversations(id) ON DELETE RESTRICT
    ) STRICT""",
    """CREATE TABLE document_references (
        id TEXT PRIMARY KEY,
        conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE RESTRICT,
        document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE RESTRICT,
        UNIQUE(conversation_id, document_id)
    ) STRICT""",
    "CREATE INDEX documents_content ON documents(content_hash)",
    "CREATE INDEX documents_owner ON documents(owner_conversation_id)",
    "CREATE INDEX references_document ON document_references(document_id)",
    """CREATE TRIGGER reference_scope BEFORE INSERT ON document_references BEGIN
        SELECT RAISE(ABORT, 'exclusive reference scope') WHERE EXISTS (
            SELECT 1 FROM documents WHERE id=NEW.document_id
            AND owner_conversation_id IS NOT NULL
            AND owner_conversation_id<>NEW.conversation_id);
        SELECT RAISE(ABORT, 'reference limit') WHERE (
            SELECT count(*) FROM document_references
            WHERE conversation_id=NEW.conversation_id)>=10;
    END""",
    """CREATE TRIGGER immutable_reference BEFORE UPDATE ON document_references BEGIN
        SELECT RAISE(ABORT, 'reference identity is immutable');
    END""",
    """CREATE TRIGGER immutable_document BEFORE UPDATE ON documents BEGIN
        SELECT RAISE(ABORT, 'document identity is immutable');
    END""",
    """CREATE TRIGGER immutable_content BEFORE UPDATE ON content_objects BEGIN
        SELECT RAISE(ABORT, 'content identity is immutable');
    END""",
)
UPLOAD_SCHEMA = (
    """CREATE TABLE uploads (
        id TEXT PRIMARY KEY,
        conversation_id TEXT NOT NULL REFERENCES conversations(id),
        key_hash TEXT NOT NULL,
        display_name TEXT NOT NULL CHECK(length(display_name) BETWEEN 1 AND 255),
        state TEXT NOT NULL CHECK(state IN
            ('receiving','promoting','original_stored','failed','cleanup_pending')),
        content_hash TEXT,
        byte_size INTEGER NOT NULL DEFAULT 0 CHECK(byte_size BETWEEN 0 AND 100000000),
        document_id TEXT NOT NULL,
        reference_id TEXT NOT NULL,
        owns_original INTEGER NOT NULL DEFAULT 0 CHECK(owns_original IN (0,1)),
        original_reserved INTEGER NOT NULL CHECK(original_reserved BETWEEN 0 AND 100000000),
        temp_reserved INTEGER NOT NULL CHECK(temp_reserved BETWEEN 0 AND 100000000),
        UNIQUE(conversation_id, key_hash)
    ) STRICT""",
    """CREATE UNIQUE INDEX one_active_upload ON uploads((1))
        WHERE state IN ('receiving','promoting','cleanup_pending')""",
)
SCHEMA_V2 = (*SCHEMA_V1, *UPLOAD_SCHEMA)
PROCESSING_SCHEMA = (
    """CREATE TABLE upload_batches (
        id TEXT PRIMARY KEY,
        conversation_id TEXT NOT NULL REFERENCES conversations(id),
        key_hash TEXT NOT NULL,
        fingerprint TEXT NOT NULL,
        UNIQUE(conversation_id, key_hash)
    ) STRICT""",
    """CREATE TABLE upload_batch_files (
        id TEXT PRIMARY KEY,
        batch_id TEXT NOT NULL REFERENCES upload_batches(id),
        position INTEGER NOT NULL CHECK(position BETWEEN 0 AND 9),
        display_name TEXT CHECK(length(display_name) BETWEEN 1 AND 255),
        rejected_error TEXT,
        upload_id TEXT UNIQUE REFERENCES uploads(id),
        UNIQUE(batch_id, position)
    ) STRICT""",
    """CREATE TABLE upload_failures (
        upload_id TEXT PRIMARY KEY REFERENCES uploads(id),
        error_code TEXT NOT NULL CHECK(length(error_code) BETWEEN 1 AND 64
            AND error_code NOT GLOB '*[^A-Z_]*')
    ) STRICT""",
)
SCHEMA_V3 = (*SCHEMA_V2, *PROCESSING_SCHEMA)
CSV_SCHEMA = (
    """CREATE TABLE csv_extractions (
        id TEXT PRIMARY KEY,
        document_id TEXT NOT NULL REFERENCES documents(id),
        extraction_version TEXT NOT NULL,
        normalization_version TEXT NOT NULL,
        parser_version TEXT NOT NULL,
        state TEXT NOT NULL CHECK(state IN ('processing','complete','failed')),
        error_code TEXT,
        manifest TEXT NOT NULL,
        record_count INTEGER NOT NULL DEFAULT 0 CHECK(record_count>=0),
        unit_count INTEGER NOT NULL DEFAULT 0 CHECK(unit_count>=0)
    ) STRICT""",
    """CREATE UNIQUE INDEX one_csv_processing ON csv_extractions((1)) WHERE state='processing'""",
    """CREATE UNIQUE INDEX csv_complete_version ON csv_extractions
        (document_id,extraction_version,normalization_version,parser_version) WHERE state='complete'""",
    """CREATE TABLE csv_units (
        extraction_id TEXT NOT NULL REFERENCES csv_extractions(id),
        ordinal INTEGER NOT NULL CHECK(ordinal>0),
        unit_id TEXT NOT NULL UNIQUE,
        payload TEXT NOT NULL,
        preview TEXT NOT NULL,
        PRIMARY KEY(extraction_id,ordinal)
    ) STRICT""",
    """CREATE TABLE csv_requests (
        id TEXT PRIMARY KEY,
        reference_id TEXT NOT NULL REFERENCES document_references(id),
        key_hash TEXT NOT NULL,
        extraction_id TEXT NOT NULL REFERENCES csv_extractions(id),
        UNIQUE(reference_id,key_hash)
    ) STRICT""",
)
SCHEMA_V4 = (*SCHEMA_V3, *CSV_SCHEMA)
INDEX_SCHEMA = (
    """CREATE TABLE index_generations (
        id TEXT PRIMARY KEY,
        identity TEXT NOT NULL,
        content_hash TEXT NOT NULL REFERENCES content_objects(sha256),
        profile TEXT NOT NULL,
        state TEXT NOT NULL CHECK(state IN ('processing','complete','failed')),
        error_code TEXT,
        chunk_count INTEGER NOT NULL DEFAULT 0 CHECK(chunk_count>=0),
        omission_count INTEGER NOT NULL DEFAULT 0 CHECK(omission_count>=0)
    ) STRICT""",
    """CREATE UNIQUE INDEX one_index_processing ON index_generations((1))
        WHERE state='processing'""",
    """CREATE UNIQUE INDEX index_complete_identity ON index_generations(identity)
        WHERE state='complete'""",
    """CREATE TABLE index_vectors (
        generation_id TEXT NOT NULL REFERENCES index_generations(id),
        ordinal INTEGER NOT NULL CHECK(ordinal>0),
        text_hash TEXT NOT NULL CHECK(length(text_hash)=64),
        vector BLOB NOT NULL CHECK(length(vector)=3072),
        PRIMARY KEY(generation_id,ordinal)
    ) STRICT""",
    """CREATE TABLE index_bindings (
        id TEXT PRIMARY KEY,
        extraction_id TEXT NOT NULL REFERENCES csv_extractions(id),
        generation_id TEXT NOT NULL REFERENCES index_generations(id),
        UNIQUE(extraction_id,generation_id)
    ) STRICT""",
    """CREATE TABLE index_chunks (
        binding_id TEXT NOT NULL REFERENCES index_bindings(id),
        ordinal INTEGER NOT NULL CHECK(ordinal>0),
        generation_id TEXT NOT NULL,
        chunk_id TEXT NOT NULL,
        payload TEXT NOT NULL,
        PRIMARY KEY(binding_id,ordinal),
        FOREIGN KEY(generation_id,ordinal) REFERENCES index_vectors(generation_id,ordinal)
    ) STRICT""",
    """CREATE TABLE index_omissions (
        binding_id TEXT NOT NULL REFERENCES index_bindings(id),
        ordinal INTEGER NOT NULL CHECK(ordinal>0),
        payload TEXT NOT NULL,
        PRIMARY KEY(binding_id,ordinal)
    ) STRICT""",
    """CREATE TABLE index_requests (
        id TEXT PRIMARY KEY,
        reference_id TEXT NOT NULL REFERENCES document_references(id),
        key_hash TEXT NOT NULL,
        extraction_id TEXT NOT NULL REFERENCES csv_extractions(id),
        generation_id TEXT NOT NULL REFERENCES index_generations(id),
        state TEXT NOT NULL CHECK(state IN ('processing','complete','failed')),
        error_code TEXT,
        UNIQUE(reference_id,key_hash)
    ) STRICT""",
)
SCHEMA_V5 = (*SCHEMA_V4, *INDEX_SCHEMA)
CHAT_SCHEMA = (
    """CREATE TABLE chat_selections (
        conversation_id TEXT PRIMARY KEY REFERENCES conversations(id),
        revision INTEGER NOT NULL CHECK(revision>=0),
        references_json TEXT NOT NULL
    ) STRICT""",
    """CREATE TABLE chat_requests (
        id TEXT PRIMARY KEY,
        conversation_id TEXT NOT NULL REFERENCES conversations(id),
        key_hash TEXT NOT NULL,
        fingerprint TEXT NOT NULL,
        question TEXT NOT NULL,
        selection_revision INTEGER NOT NULL CHECK(selection_revision>=0),
        references_json TEXT NOT NULL,
        state TEXT NOT NULL CHECK(state IN ('processing','complete','failed')),
        error_code TEXT,
        created_at TEXT NOT NULL,
        UNIQUE(conversation_id,key_hash)
    ) STRICT""",
    """CREATE UNIQUE INDEX one_chat_processing ON chat_requests((1)) WHERE state='processing'""",
    """CREATE TABLE chat_exchanges (
        request_id TEXT PRIMARY KEY REFERENCES chat_requests(id),
        answer TEXT NOT NULL,
        sources_json TEXT NOT NULL,
        evidence_json TEXT NOT NULL,
        warnings_json TEXT NOT NULL,
        model_json TEXT NOT NULL,
        completed_at TEXT NOT NULL
    ) STRICT""",
)
SCHEMA = (*SCHEMA_V5, *CHAT_SCHEMA)


class StorageError(ValueError):
    """Safe storage failure code; never includes SQLite values or private paths."""


@contextmanager
def transaction(connection: sqlite3.Connection) -> Iterator[None]:
    """Serialize a complete write; rollback every uncommitted exceptional exit."""
    if connection.in_transaction:
        raise StorageError("NESTED_TRANSACTION")
    try:
        connection.execute("BEGIN IMMEDIATE")
        try:
            yield
            connection.commit()
        finally:
            if connection.in_transaction:
                connection.rollback()
    except sqlite3.Error as error:
        if getattr(error, "sqlite_errorcode", None) == sqlite3.SQLITE_FULL:
            raise StorageError("STORAGE_QUOTA_OR_DISK_FULL") from None
        raise StorageError("STORAGE_CONFLICT_OR_UNAVAILABLE") from None


def _authorize(
    action: int,
    first: str | None,
    second: str | None,
    database: str | None,
    source: str | None,
) -> int:
    if action in {sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH} or (
        action == sqlite3.SQLITE_FUNCTION and second == "load_extension"
    ):
        return sqlite3.SQLITE_DENY
    return sqlite3.SQLITE_OK


def open_database(root: Path, *, max_pages: int | None = None) -> sqlite3.Connection:
    """Open metadata.sqlite3 under a trusted managed root; refuse foreign versions.

    The caller owns/closes the returned connection. This is a trusted backend
    interface, not an arbitrary SQL or browser-path interface. No extension loads.
    """
    connection = None
    try:
        prepare_data_root(root)
        path = root / "metadata.sqlite3"
        for candidate in (
            path,
            root / "metadata.sqlite3-journal",
            root / "metadata.sqlite3-wal",
            root / "metadata.sqlite3-shm",
        ):
            validate_local_ancestry(candidate)
        connection = sqlite3.connect(path, isolation_level=None, timeout=5)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA trusted_schema=OFF")
        connection.execute("PRAGMA synchronous=FULL")
        connection.set_authorizer(_authorize)
        if max_pages is not None:
            if type(max_pages) is not int or max_pages < 1:
                raise StorageError("INVALID_DATABASE_BOUND")
            if (
                connection.execute(f"PRAGMA max_page_count={max_pages}").fetchone()[0]
                > max_pages
            ):
                raise StorageError("DATABASE_BOUND_EXCEEDED")
        with transaction(connection):
            version = connection.execute("PRAGMA user_version").fetchone()[0]
            identity = connection.execute("PRAGMA application_id").fetchone()[0]
            objects = connection.execute(
                "SELECT name FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"
            ).fetchall()
            if version == 0 and identity == 0 and not objects:
                if connection.execute("PRAGMA journal_mode").fetchone()[0] != "delete":
                    raise StorageError("UNSUPPORTED_JOURNAL_MODE")
                for statement in SCHEMA:
                    connection.execute(statement)
                connection.execute(f"PRAGMA application_id={APPLICATION_ID}")
                connection.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
            elif version in {1, 2, 3, 4, 5} and identity == APPLICATION_ID:
                old_schema = {
                    row[0]
                    for row in connection.execute(
                        "SELECT sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"
                    )
                }
                expected = {
                    1: SCHEMA_V1,
                    2: SCHEMA_V2,
                    3: SCHEMA_V3,
                    4: SCHEMA_V4,
                    5: SCHEMA_V5,
                }[version]
                if old_schema != {statement.strip() for statement in expected}:
                    raise StorageError("DATABASE_SCHEMA_MISMATCH")
                if connection.execute("PRAGMA journal_mode").fetchone()[0] != "delete":
                    raise StorageError("UNSUPPORTED_JOURNAL_MODE")
                additions = {
                    1: (
                        *UPLOAD_SCHEMA,
                        *PROCESSING_SCHEMA,
                        *CSV_SCHEMA,
                        *INDEX_SCHEMA,
                        *CHAT_SCHEMA,
                    ),
                    2: (*PROCESSING_SCHEMA, *CSV_SCHEMA, *INDEX_SCHEMA, *CHAT_SCHEMA),
                    3: (*CSV_SCHEMA, *INDEX_SCHEMA, *CHAT_SCHEMA),
                    4: (*INDEX_SCHEMA, *CHAT_SCHEMA),
                    5: CHAT_SCHEMA,
                }[version]
                for statement in additions:
                    connection.execute(statement)
                connection.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
            elif version != SCHEMA_VERSION or identity != APPLICATION_ID:
                raise StorageError("UNSUPPORTED_DATABASE_SCHEMA")
            actual_schema = {
                row[0]
                for row in connection.execute(
                    "SELECT sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'"
                )
            }
            if actual_schema != {statement.strip() for statement in SCHEMA}:
                raise StorageError("DATABASE_SCHEMA_MISMATCH")
            if connection.execute("PRAGMA journal_mode").fetchone()[0] != "delete":
                raise StorageError("UNSUPPORTED_JOURNAL_MODE")
        return connection
    except (sqlite3.Error, OSError, ConfigurationError, StorageError):
        if connection is not None:
            connection.close()
        raise StorageError("STORAGE_OPEN_FAILED") from None
