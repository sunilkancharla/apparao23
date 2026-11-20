"""Content identity is shared; conversation reference visibility is always scoped."""

import re
import sqlite3
from dataclasses import dataclass
from uuid import uuid4

from app.storage.database import StorageError, transaction


@dataclass(frozen=True)
class DocumentReference:
    """Logical source membership, distinct from shared stored-content identity."""

    reference_id: str
    document_id: str
    content_hash: str


class Documents:
    """Atomic metadata operations over one caller-owned SQLite connection.

    Content metadata must come from a verified ingestion boundary. These methods
    do not read/hash original bytes or authorize file publication. No deletion,
    quota ledger, browser mutation API or extraction/index lifecycle is provided.
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def create_conversation(self) -> str:
        """Persist a fresh server-owned conversation identity."""
        identity = str(uuid4())
        with transaction(self.connection):
            self.connection.execute("INSERT INTO conversations VALUES (?)", (identity,))
        return identity

    def _content(self, digest: str, size: int, kind: str) -> None:
        if (
            not isinstance(digest, str)
            or not re.fullmatch(r"[0-9a-f]{64}", digest)
            or type(size) is not int
            or not 0 <= size <= 100_000_000
            or kind not in {"csv", "xlsx", "pdf"}
        ):
            raise StorageError("INVALID_CONTENT_METADATA")
        self.connection.execute(
            "INSERT INTO content_objects VALUES (?, ?, ?) ON CONFLICT(sha256) DO NOTHING",
            (digest, size, kind),
        )
        row = self.connection.execute(
            "SELECT byte_size, format FROM content_objects WHERE sha256=?", (digest,)
        ).fetchone()
        if tuple(row) != (size, kind):
            raise StorageError("CONTENT_METADATA_CONFLICT")

    def add_library_document(self, digest: str, size: int, kind: str) -> str:
        """Create a library identity without granting any conversation membership."""
        identity = str(uuid4())
        with transaction(self.connection):
            self._content(digest, size, kind)
            self.connection.execute(
                "INSERT INTO documents VALUES (?, ?, NULL)", (identity, digest)
            )
        return identity

    def add_attachment(
        self, conversation: str, digest: str, size: int, kind: str
    ) -> DocumentReference:
        """Atomically create exclusive document membership, including dedup metadata."""
        document, reference = str(uuid4()), str(uuid4())
        with transaction(self.connection):
            self._content(digest, size, kind)
            self.connection.execute(
                "INSERT INTO documents VALUES (?, ?, ?)",
                (document, digest, conversation),
            )
            self.connection.execute(
                "INSERT INTO document_references VALUES (?, ?, ?)",
                (reference, conversation, document),
            )
        return DocumentReference(reference, document, digest)

    def attach_library(self, conversation: str, document: str) -> DocumentReference:
        """Reuse library bytes; repeat membership returns its existing reference."""
        with transaction(self.connection):
            row = self.connection.execute(
                "SELECT content_hash FROM documents WHERE id=? AND owner_conversation_id IS NULL",
                (document,),
            ).fetchone()
            if row is None:
                raise StorageError("LIBRARY_DOCUMENT_UNAVAILABLE")
            existing = self.resolve(conversation, document, by_document=True)
            if existing is not None:
                return existing
            reference = str(uuid4())
            self.connection.execute(
                "INSERT INTO document_references VALUES (?, ?, ?)",
                (reference, conversation, document),
            )
            return DocumentReference(reference, document, row[0])

    def references(self, conversation: str) -> list[DocumentReference]:
        """List only this conversation's at-most-ten logical source references."""
        rows = self.connection.execute(
            """SELECT r.id, d.id, d.content_hash FROM document_references r
            JOIN documents d ON d.id=r.document_id
            WHERE r.conversation_id=? ORDER BY r.id""",
            (conversation,),
        ).fetchall()
        return [DocumentReference(*row) for row in rows]

    def resolve(
        self, conversation: str, reference: str, *, by_document: bool = False
    ) -> DocumentReference | None:
        """Resolve a reference only with its conversation membership; no hash lookup."""
        key = "r.document_id" if by_document else "r.id"
        row = self.connection.execute(
            f"""SELECT r.id, d.id, d.content_hash FROM document_references r
            JOIN documents d ON d.id=r.document_id
            WHERE r.conversation_id=? AND {key}=?""",
            (conversation, reference),
        ).fetchone()
        return None if row is None else DocumentReference(*row)
