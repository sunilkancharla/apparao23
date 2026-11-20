"""Durable batch admission and status; extraction/index readiness is never inferred."""

import hashlib
import json
import sqlite3
from typing import TYPE_CHECKING, Literal, NotRequired, TypedDict
from uuid import uuid4

from app.ingestion.csv import EXTRACTION_VERSION, NORMALIZATION_VERSION, PARSER
from app.ingestion.validation import UploadError, validate_filename

if TYPE_CHECKING:
    from app.storage.files import UploadStore


class OperationStatus(TypedDict):
    """Bounded metadata only; upload completion never asserts pipeline readiness."""

    operation_id: str
    kind: Literal["upload_file", "upload_batch", "csv_extraction", "document_index"]
    state: str
    ready: bool
    indexed: bool
    display_name: NotRequired[str | None]
    error_code: NotRequired[str | None]
    upload_operation_id: NotRequired[str | None]
    document_id: NotRequired[str | None]
    reference_id: NotRequired[str | None]
    bytes_stored: NotRequired[int | None]
    warning_codes: NotRequired[list[str]]
    total_files: NotRequired[int]
    originals_stored: NotRequired[int]
    failed_files: NotRequired[int]
    files: NotRequired[list["OperationStatus"]]
    extraction_id: NotRequired[str | None]
    extraction_state: NotRequired[str]
    record_count: NotRequired[int | None]
    unit_count: NotRequired[int | None]
    extraction_failed_files: NotRequired[int]


def reserved_slots(connection: sqlite3.Connection, conversation: str) -> int:
    """Count valid manifest entries that still reserve an unattached reference."""
    return connection.execute(
        """SELECT count(*) FROM upload_batch_files f
        JOIN upload_batches b ON b.id=f.batch_id LEFT JOIN uploads u ON u.id=f.upload_id
        WHERE b.conversation_id=? AND f.rejected_error IS NULL
        AND (f.upload_id IS NULL OR u.state IN ('receiving','promoting','cleanup_pending'))""",
        (conversation,),
    ).fetchone()[0]


def bind_reference_slot(
    connection: sqlite3.Connection,
    conversation: str,
    name: str,
    file_id: str | None,
    upload_id: str,
) -> None:
    """Validate/bind a manifest slot inside the caller's upload-admission transaction."""
    own_slot = False
    if file_id is not None:
        file = connection.execute(
            """SELECT f.*,u.state FROM upload_batch_files f
            JOIN upload_batches b ON b.id=f.batch_id LEFT JOIN uploads u ON u.id=f.upload_id
            WHERE f.id=? AND b.conversation_id=?""",
            (file_id, conversation),
        ).fetchone()
        if file is None:
            raise UploadError("OPERATION_NOT_FOUND", 404)
        if file["rejected_error"] is not None:
            raise UploadError(
                file["rejected_error"],
                415 if file["rejected_error"] == "UNSUPPORTED_FORMAT" else 422,
            )
        if file["display_name"] != name:
            raise UploadError("BATCH_FILE_MISMATCH", 409)
        if file["upload_id"] is not None and file["state"] != "failed":
            raise UploadError("UPLOAD_PENDING", 409)
        own_slot = file["upload_id"] is None
    references = connection.execute(
        "SELECT count(*) FROM document_references WHERE conversation_id=?",
        (conversation,),
    ).fetchone()[0]
    if references + reserved_slots(connection, conversation) + 1 - int(own_slot) > 10:
        raise UploadError("REFERENCE_LIMIT", 413)
    if file_id is not None:
        connection.execute(
            "UPDATE upload_batch_files SET upload_id=? WHERE id=?", (upload_id, file_id)
        )


class UploadOperations:
    """Small persisted manifests hand off files to the serialized upload boundary."""

    def __init__(self, store: "UploadStore") -> None:
        self.store = store
        self.connection = store.connection

    def _index_status(self, conversation: str, reference: str) -> dict:
        from app.storage.index_state import IndexState

        status = IndexState(self.store).status(conversation, reference)
        if status is None:
            return {}
        fields = {
            key: status[key]
            for key in ("ready", "indexed", "state", "warning_codes", "error_code")
        }
        if status["state"] == "processing":
            fields["state"] = (
                "cleanup_pending" if self.store.recovery_pending else "indexing"
            )
        return fields

    def create_batch(
        self, conversation: str, key: str, names: list[str]
    ) -> OperationStatus:
        """Persist at most ten file intents, reserving slots for valid siblings."""
        if self.store.busy or self.store.recovery_pending:
            raise UploadError("UPLOAD_BUSY", 409)
        if not 1 <= len(names) <= 10:
            raise UploadError("BATCH_LIMIT", 413)
        fingerprint = hashlib.sha256(
            json.dumps(names, ensure_ascii=True, separators=(",", ":")).encode()
        ).hexdigest()
        key_hash = hashlib.sha256(key.encode("ascii")).hexdigest()
        entries = []
        for name in names:
            try:
                validate_filename(name)
                entries.append((name, None))
            except UploadError as error:
                entries.append(
                    (None if error.code == "INVALID_FILENAME" else name, error.code)
                )
        with self.store._write():
            if (
                self.connection.execute(
                    "SELECT 1 FROM conversations WHERE id=?", (conversation,)
                ).fetchone()
                is None
            ):
                raise UploadError("CONVERSATION_NOT_FOUND", 404)
            previous = self.connection.execute(
                "SELECT id,fingerprint FROM upload_batches WHERE conversation_id=? AND key_hash=?",
                (conversation, key_hash),
            ).fetchone()
            if previous is not None:
                if previous["fingerprint"] != fingerprint:
                    raise UploadError("IDEMPOTENCY_CONFLICT", 409)
                identity = previous["id"]
            else:
                if (
                    self.store.busy
                    or self.connection.execute(
                        "SELECT 1 FROM uploads WHERE state IN ('receiving','promoting','cleanup_pending')"
                    ).fetchone()
                ):
                    raise UploadError("UPLOAD_BUSY", 409)
                references = self.connection.execute(
                    "SELECT count(*) FROM document_references WHERE conversation_id=?",
                    (conversation,),
                ).fetchone()[0]
                if (
                    references
                    + reserved_slots(self.connection, conversation)
                    + sum(error is None for _, error in entries)
                    > 10
                ):
                    raise UploadError("REFERENCE_LIMIT", 413)
                identity = str(uuid4())
                self.connection.execute(
                    "INSERT INTO upload_batches VALUES (?,?,?,?)",
                    (identity, conversation, key_hash, fingerprint),
                )
                self.connection.executemany(
                    "INSERT INTO upload_batch_files VALUES (?,?,?,?,?,NULL)",
                    [
                        (str(uuid4()), identity, position, name, error)
                        for position, (name, error) in enumerate(entries)
                    ],
                )
        return self.status(conversation, identity)

    def _file(
        self,
        conversation: str,
        identity: str,
        name: str | None,
        rejected: str | None,
        upload: str | None,
    ) -> OperationStatus:
        row = None
        if upload is not None:
            row = self.connection.execute(
                """SELECT u.*, e.error_code FROM uploads u
                LEFT JOIN upload_failures e ON e.upload_id=u.id
                WHERE u.id=? AND u.conversation_id=?""",
                (upload, conversation),
            ).fetchone()
            if row is None:
                raise UploadError("OPERATION_NOT_FOUND", 404)
        state, error = ("failed", rejected) if rejected else ("queued", None)
        if row is not None:
            state = {
                "receiving": "processing",
                "promoting": "processing",
                "original_stored": "awaiting_extraction",
            }.get(row["state"], row["state"])
            error = row["error_code"]
            if state == "failed":
                error = error or "UPLOAD_FAILED"
                if error == "UPLOAD_INTERRUPTED":
                    state = "interrupted"
            if (
                state in {"processing", "cleanup_pending"}
                and self.store.recovery_pending
            ):
                state = "cleanup_pending"
            if state == "cleanup_pending":
                error = "CLEANUP_PENDING"
        stored = state == "awaiting_extraction"
        extraction = None
        warnings = ["EXTRACTION_PENDING"] if stored else []
        if stored:
            extraction = self.connection.execute(
                """SELECT * FROM csv_extractions WHERE document_id=?
                AND extraction_version=? AND normalization_version=? AND parser_version=? ORDER BY rowid DESC LIMIT 1""",
                (
                    row["document_id"],
                    EXTRACTION_VERSION,
                    NORMALIZATION_VERSION,
                    PARSER.version,
                ),
            ).fetchone()
            if extraction is not None:
                if extraction["state"] == "complete":
                    state, warnings = "awaiting_index", ["INDEX_PENDING"]
                elif extraction["state"] == "processing":
                    if self.store.recovery_pending:
                        state, warnings, error = (
                            "cleanup_pending",
                            ["EXTRACTION_RECOVERY_PENDING"],
                            "EXTRACTION_PENDING",
                        )
                    else:
                        state, warnings = "extracting", []
                else:
                    error, warnings = extraction["error_code"], ["EXTRACTION_FAILED"]
        indexed_fields = (
            self._index_status(conversation, row["reference_id"])
            if extraction is not None and extraction["state"] == "complete"
            else {}
        )
        return {
            "operation_id": identity,
            "kind": "upload_file",
            "display_name": name,
            "state": state,
            "error_code": error,
            "ready": False,
            "indexed": False,
            "upload_operation_id": upload,
            "document_id": row["document_id"] if stored else None,
            "reference_id": row["reference_id"] if stored else None,
            "bytes_stored": row["byte_size"] if stored else None,
            "warning_codes": warnings,
            "extraction_id": extraction["id"] if extraction else None,
            "extraction_state": extraction["state"] if extraction else "not_started",
            **indexed_fields,
        }

    def status(self, conversation: str, identity: str) -> OperationStatus:
        """Read only the requested conversation's bounded operation snapshot."""
        batch = self.connection.execute(
            "SELECT id FROM upload_batches WHERE id=? AND conversation_id=?",
            (identity, conversation),
        ).fetchone()
        if batch is not None:
            files = [
                self._file(
                    conversation,
                    r["id"],
                    r["display_name"],
                    r["rejected_error"],
                    r["upload_id"],
                )
                for r in self.connection.execute(
                    "SELECT * FROM upload_batch_files WHERE batch_id=? ORDER BY position LIMIT 10",
                    (identity,),
                )
            ]
            states = {item["state"] for item in files}
            stored = sum(item["document_id"] is not None for item in files)
            failed = sum(item["state"] in {"failed", "interrupted"} for item in files)
            extraction_failed = sum(
                item["extraction_state"] == "failed" for item in files
            )
            indexed = all(item["indexed"] for item in files)
            ready = all(item["ready"] for item in files)
            state = (
                "awaiting_extraction"
                if "awaiting_extraction" in states
                else "awaiting_index"
            )
            for candidate in (
                "processing",
                "extracting",
                "indexing",
                "cleanup_pending",
                "queued",
            ):
                if candidate in states:
                    state = candidate
                    break
            else:
                if failed or extraction_failed:
                    state = "partial_failure" if stored else "failed"
                elif indexed:
                    state = "indexed" if ready else "indexed_with_omissions"
            return {
                "operation_id": identity,
                "kind": "upload_batch",
                "state": state,
                "ready": ready,
                "indexed": indexed,
                "total_files": len(files),
                "originals_stored": stored,
                "failed_files": failed,
                "extraction_failed_files": extraction_failed,
                "files": files,
            }
        file = self.connection.execute(
            """SELECT f.* FROM upload_batch_files f JOIN upload_batches b ON b.id=f.batch_id
            WHERE f.id=? AND b.conversation_id=?""",
            (identity, conversation),
        ).fetchone()
        if file is not None:
            return self._file(
                conversation,
                identity,
                file["display_name"],
                file["rejected_error"],
                file["upload_id"],
            )
        upload = self.connection.execute(
            "SELECT display_name FROM uploads WHERE id=? AND conversation_id=?",
            (identity, conversation),
        ).fetchone()
        if upload is not None:
            return self._file(
                conversation, identity, upload["display_name"], None, identity
            )
        extraction = self.connection.execute(
            """SELECT e.*,r.id AS scoped_reference FROM csv_extractions e
            JOIN document_references r ON r.document_id=e.document_id WHERE e.id=? AND r.conversation_id=?""",
            (identity, conversation),
        ).fetchone()
        if extraction is not None:
            return {
                "operation_id": identity,
                "kind": "csv_extraction",
                "extraction_id": identity,
                "document_id": extraction["document_id"],
                "ready": False,
                "indexed": False,
                "state": {
                    "complete": "awaiting_index",
                    "processing": "cleanup_pending"
                    if self.store.recovery_pending
                    else "extracting",
                    "failed": "failed",
                }[extraction["state"]],
                "error_code": "EXTRACTION_PENDING"
                if self.store.recovery_pending and extraction["state"] == "processing"
                else extraction["error_code"],
                "record_count": extraction["record_count"]
                if extraction["state"] == "complete"
                else None,
                "unit_count": extraction["unit_count"]
                if extraction["state"] == "complete"
                else None,
                **(
                    self._index_status(conversation, extraction["scoped_reference"])
                    if extraction["state"] == "complete"
                    else {}
                ),
            }
        from app.storage.index_state import IndexState

        indexed = self.connection.execute(
            """SELECT q.* FROM index_requests q JOIN document_references r ON r.id=q.reference_id
            WHERE q.id=? AND r.conversation_id=?""",
            (identity, conversation),
        ).fetchone()
        if indexed is not None:
            state = IndexState(self.store)
            receipt = state.receipt(indexed)
            current = state.status(conversation, indexed["reference_id"])
            if current is None or current["generation_id"] != receipt["generation_id"]:
                receipt.update(
                    ready=False,
                    indexed=False,
                    state="reindex_required",
                    warning_codes=["INDEX_VERSION_CHANGED"],
                )
            return receipt
        raise UploadError("OPERATION_NOT_FOUND", 404)
