"""Serialized upload admission, durable intents and immutable local originals."""

import errno
import hashlib
import os
import re
import sqlite3
import stat
from collections.abc import AsyncIterable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Literal, TypedDict
from uuid import uuid4

from app.config import prepare_data_root, validate_local_ancestry
from app.ingestion.validation import MAX_FILE_BYTES, UploadError, validate_csv
from app.storage.database import StorageError, open_database, transaction
from app.storage.documents import Documents

PROCESSED_CAP = 5_000_000_000
TEMP_CAP = 1_000_000_000
CONVERSATION_CAP = 10_000_000_000
LIBRARY_CAP = 1_000_000_000


class UploadReceipt(TypedDict):
    """Stored-original acknowledgement; it never represents an indexed source."""

    document_id: str
    reference_id: str
    display_name: str
    operation_id: str
    state: Literal["original_stored"]
    indexed: Literal[False]


class UploadStore:
    """One application owner per managed root; all public writes are serialized.

    The same-account operator must keep the root private and stable. Reparse and
    hardlink checks do not confine a hostile process running as that operator.
    """

    def __init__(self, root: Path) -> None:
        self.root, self.connection, self.lock_file = root, None, None
        self.busy = False
        try:
            prepare_data_root(root)
            initial = self._usage()
            if initial["processed"] + 1_048_577 > PROCESSED_CAP:
                raise UploadError("PROCESSED_QUOTA", 507)
            self.lock_file = (root / "upload.lock").open("a+b")
            if os.name == "nt":
                import msvcrt

                self.lock_file.seek(0)
                msvcrt.locking(self.lock_file.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(self.lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            if self.lock_file.seek(0, 2) == 0:
                self.lock_file.write(b"1")
                self.lock_file.flush()
            for directory in (root / "originals", root / "staging"):
                validate_local_ancestry(directory)
                directory.mkdir(exist_ok=True)
            # SQLite's page-size header is trusted only after path checks; the
            # database opener separately validates exact schema/identity.
            db = root / "metadata.sqlite3"
            page_size = 4096
            if db.exists():
                with db.open("rb") as source:
                    header = source.read(18)
                if len(header) == 18:
                    page_size = int.from_bytes(header[16:18], "big") or 65536
                    if page_size == 1:
                        page_size = 65536
            processed = self._usage()["processed"]
            other = processed - (db.stat().st_size if db.exists() else 0)
            pages = max(1, (PROCESSED_CAP - other - 1_048_576) // (4 * page_size))
            self.connection = open_database(root, max_pages=pages)
            self.connection.execute("PRAGMA cache_spill=OFF")
            self.connection.execute("PRAGMA temp_store=MEMORY")
            pending = self.connection.execute(
                "SELECT id FROM uploads WHERE state IN ('receiving','promoting','cleanup_pending') LIMIT 1"
            ).fetchone()
            if pending is not None:
                self._cleanup(pending[0])
        except Exception:  # noqa: BLE001 - startup privacy boundary, releasing ownership
            self.close()
            raise UploadError("STORAGE_UNAVAILABLE", 503) from None

    def close(self) -> None:
        """Release only this instance's connection and operating-system lock."""
        if self.connection is not None:
            self.connection.close()
            self.connection = None
        if self.lock_file is not None:
            self.lock_file.close()
            self.lock_file = None

    def _usage(self) -> dict[str, int]:
        usage = {"processed": 0, "temporary": 0, "conversation": 0, "library": 0}
        library = set()
        if self.connection is not None:
            library = {
                row[0]
                for row in self.connection.execute(
                    "SELECT DISTINCT content_hash FROM documents WHERE owner_conversation_id IS NULL"
                )
            }
        for path in self.root.rglob("*"):
            validate_local_ancestry(path)
            info = path.stat()
            if stat.S_ISDIR(info.st_mode):
                continue
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise UploadError("UNSAFE_STORAGE", 503)
            relative = path.relative_to(self.root)
            category = "processed"
            if relative.parts[0] == "staging":
                category = "temporary"
            elif relative.parts[0] == "originals":
                category = "library" if path.name in library else "conversation"
            usage[category] += info.st_size
        return usage

    @contextmanager
    def _write(self) -> Iterator[None]:
        usage = self._usage()
        page_size = self.connection.execute("PRAGMA page_size").fetchone()[0]
        pages = self.connection.execute("PRAGMA page_count").fetchone()[0]
        db_bytes = (self.root / "metadata.sqlite3").stat().st_size
        other = usage["processed"] - db_bytes
        # No ATTACH/savepoints/sort writes: reserve conservative main+rollback
        # space before each short transaction, including the ledger's own pages.
        ceiling = min(
            pages + 16, (PROCESSED_CAP - other - 1_048_576) // (4 * page_size)
        )
        if ceiling < pages:
            raise UploadError("PROCESSED_QUOTA", 507)
        actual = self.connection.execute(f"PRAGMA max_page_count={ceiling}").fetchone()[
            0
        ]
        if actual != ceiling:
            raise UploadError("PROCESSED_QUOTA", 507)
        try:
            with transaction(self.connection):
                yield
        except StorageError as error:
            full = str(error) == "STORAGE_QUOTA_OR_DISK_FULL"
            raise UploadError(
                "STORAGE_QUOTA" if full else "STORAGE_WRITE_FAILED",
                507 if full else 503,
            ) from None

    def _operation(self, identity: str) -> sqlite3.Row:
        row = self.connection.execute(
            "SELECT * FROM uploads WHERE id=?", (identity,)
        ).fetchone()
        if row is None:
            raise UploadError("UPLOAD_UNAVAILABLE", 404)
        return row

    def admit(self, conversation: str, key: str, name: str) -> tuple[sqlite3.Row, bool]:
        """Claim one durable intent and worst-case byte reservations before staging."""
        key_hash = hashlib.sha256(key.encode("ascii")).hexdigest()
        with self._write():
            if (
                self.connection.execute(
                    "SELECT 1 FROM conversations WHERE id=?", (conversation,)
                ).fetchone()
                is None
            ):
                raise UploadError("CONVERSATION_NOT_FOUND", 404)
            existing = self.connection.execute(
                "SELECT * FROM uploads WHERE conversation_id=? AND key_hash=?",
                (conversation, key_hash),
            ).fetchone()
            if existing is not None:
                if existing["display_name"] != name:
                    raise UploadError("IDEMPOTENCY_CONFLICT", 409)
                if existing["state"] != "original_stored":
                    if existing["state"] == "failed":
                        raise UploadError("UPLOAD_FAILED", 409)
                    raise UploadError("UPLOAD_PENDING", 409)
                return existing, True
            if (
                self.connection.execute(
                    "SELECT count(*) FROM document_references WHERE conversation_id=?",
                    (conversation,),
                ).fetchone()[0]
                >= 10
            ):
                raise UploadError("REFERENCE_LIMIT", 413)
            if self.connection.execute(
                "SELECT 1 FROM uploads WHERE state IN ('receiving','promoting','cleanup_pending')"
            ).fetchone():
                raise UploadError("UPLOAD_PENDING", 409)
            usage = self._usage()
            for category, cap, reserve in (
                ("temporary", TEMP_CAP, MAX_FILE_BYTES),
                ("conversation", CONVERSATION_CAP, MAX_FILE_BYTES),
                ("library", LIBRARY_CAP, 0),
            ):
                if usage[category] + reserve > cap:
                    raise UploadError("STORAGE_QUOTA", 507)
            identity, document, reference = (str(uuid4()) for _ in range(3))
            self.connection.execute(
                """INSERT INTO uploads
                (id,conversation_id,key_hash,display_name,state,document_id,reference_id,
                 original_reserved,temp_reserved) VALUES (?,?,?,?,'receiving',?,?,?,?)""",
                (
                    identity,
                    conversation,
                    key_hash,
                    name,
                    document,
                    reference,
                    MAX_FILE_BYTES,
                    MAX_FILE_BYTES,
                ),
            )
        return self._operation(identity), False

    def _path(self, category: str, identity: str) -> Path:
        if category not in {"originals", "staging"} or not re.fullmatch(
            r"[0-9a-f-]{36}|[0-9a-f]{64}", identity
        ):
            raise UploadError("UNSAFE_STORAGE", 503)
        path = self.root / category / identity
        validate_local_ancestry(path)
        if path.exists():
            info = path.stat()
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise UploadError("UNSAFE_STORAGE", 503)
        return path

    def _verified_original(self, digest: str, size: int) -> Path:
        path = self._path("originals", digest)
        try:
            with path.open("rb") as source:
                if (
                    path.stat().st_size != size
                    or hashlib.file_digest(source, "sha256").hexdigest() != digest
                ):
                    raise UploadError("SOURCE_UNAVAILABLE", 410)
        except FileNotFoundError:
            raise UploadError("SOURCE_UNAVAILABLE", 410) from None
        return path

    def _cleanup(self, identity: str) -> None:
        # The durable server-created intent is ownership evidence. Never sweep
        # unknown files or recursively delete a directory inferred from a name.
        row = self._operation(identity)
        if row["state"] == "original_stored":
            return
        with self._write():
            self.connection.execute(
                "UPDATE uploads SET state='cleanup_pending' WHERE id=?", (identity,)
            )
        stage = self._path("staging", row["id"])
        stage.unlink(missing_ok=True)
        if row["owns_original"] and row["content_hash"]:
            referenced = self.connection.execute(
                "SELECT 1 FROM documents WHERE content_hash=? LIMIT 1",
                (row["content_hash"],),
            ).fetchone()
            path = self._path("originals", row["content_hash"])
            if referenced is None and path.exists():
                self._verified_original(row["content_hash"], row["byte_size"]).unlink()
        with self._write():
            self.connection.execute(
                "UPDATE uploads SET state='failed', original_reserved=0, temp_reserved=0 WHERE id=?",
                (identity,),
            )

    @staticmethod
    def _result(row: sqlite3.Row) -> UploadReceipt:
        return {
            "document_id": row["document_id"],
            "reference_id": row["reference_id"],
            "display_name": row["display_name"],
            "operation_id": row["id"],
            "state": "original_stored",
            "indexed": False,
        }

    async def receive(
        self,
        body: AsyncIterable[bytes],
        conversation: str,
        key: str,
        name: str,
        declared: int | None = None,
    ) -> UploadReceipt:
        """Stream within reservations, verify retries and publish only complete originals."""
        if self.busy:
            raise UploadError("UPLOAD_BUSY", 409)
        self.busy = True
        operation = None
        replay = False
        try:
            operation, replay = self.admit(conversation, key, name)
            size, digest = 0, hashlib.sha256()
            stage = None if replay else self._path("staging", operation["id"])
            stream = None if replay else stage.open("xb")
            try:
                async for chunk in body:
                    if size + len(chunk) > MAX_FILE_BYTES:
                        raise UploadError("FILE_TOO_LARGE", 413)
                    # Slice transport chunks before writes; never materialize a
                    # whole upload in application memory or trust Content-Length.
                    for offset in range(0, len(chunk), 65_536):
                        part = chunk[offset : offset + 65_536]
                        digest.update(part)
                        if stream is not None and stream.write(part) != len(part):
                            raise OSError("Short write")
                    size += len(chunk)
                if declared is not None and size != declared:
                    raise UploadError("CONTENT_LENGTH_MISMATCH", 400)
                if stream is not None:
                    stream.flush()
                    os.fsync(stream.fileno())
            finally:
                if stream is not None:
                    stream.close()
            content_hash = digest.hexdigest()
            if replay:
                if (
                    content_hash != operation["content_hash"]
                    or size != operation["byte_size"]
                ):
                    raise UploadError("IDEMPOTENCY_CONFLICT", 409)
                self._verified_original(content_hash, size)
                if (
                    Documents(self.connection).resolve(
                        conversation, operation["reference_id"]
                    )
                    is None
                ):
                    raise UploadError("SOURCE_UNAVAILABLE", 410)
                return self._result(operation)
            with stage.open("rb") as source:
                validate_csv(source)
            destination = self._path("originals", content_hash)
            existing = self.connection.execute(
                "SELECT byte_size,format FROM content_objects WHERE sha256=?",
                (content_hash,),
            ).fetchone()
            if existing is None and destination.exists():
                raise UploadError("UNOWNED_ORIGINAL", 503)
            if existing is not None:
                if tuple(existing) != (size, "csv"):
                    raise UploadError("CONTENT_METADATA_CONFLICT", 409)
                self._verified_original(content_hash, size)
            with self._write():
                self.connection.execute(
                    "UPDATE uploads SET state='promoting',content_hash=?,byte_size=?,owns_original=? WHERE id=?",
                    (content_hash, size, int(existing is None), operation["id"]),
                )
            if existing is None:
                if os.name == "nt":
                    # Windows rename refuses an existing target, unlike POSIX.
                    os.rename(stage, destination)
                else:
                    os.link(stage, destination)
                    stage.unlink()
            else:
                stage.unlink()
            with self._write():
                Documents(self.connection)._content(content_hash, size, "csv")
                self.connection.execute(
                    "INSERT INTO documents VALUES (?,?,?)",
                    (operation["document_id"], content_hash, conversation),
                )
                self.connection.execute(
                    "INSERT INTO document_references VALUES (?,?,?)",
                    (operation["reference_id"], conversation, operation["document_id"]),
                )
                self.connection.execute(
                    "UPDATE uploads SET state='original_stored',original_reserved=0,temp_reserved=0 WHERE id=?",
                    (operation["id"],),
                )
            return self._result(self._operation(operation["id"]))
        except BaseException as error:
            if operation is not None and not replay:
                try:
                    self._cleanup(operation["id"])
                except Exception:  # noqa: BLE001 - retain intent/reservations on uncertain cleanup
                    raise UploadError("CLEANUP_PENDING", 503) from None
            if isinstance(error, UploadError) or not isinstance(error, Exception):
                raise
            if isinstance(error, OSError) and error.errno == errno.ENOSPC:
                raise UploadError("STORAGE_QUOTA", 507) from None
            raise UploadError("UPLOAD_INTERRUPTED", 503) from None
        finally:
            self.busy = False
