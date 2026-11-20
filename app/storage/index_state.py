"""Canonical float32 vector storage; source bindings grant no independent access."""

import hashlib
import json
import math
import struct
from typing import TYPE_CHECKING

from app.ingestion.validation import UploadError
from app.retrieval.embeddings import (
    DIMENSIONS,
    MODEL_DIGEST,
    MODEL_NAME,
    RUNTIME_VERSION,
    SPACE_ID,
    EmbeddingBatch,
)
from app.retrieval.models import (
    CHUNKING_VERSION,
    MAX_BYTES,
    OVERLAP_BYTES,
    TARGET_BYTES,
    Chunk,
)
from app.storage.extractions import Extractions

if TYPE_CHECKING:
    from app.storage.files import UploadStore


def freeze_vectors(
    batch: EmbeddingBatch, chunks: tuple[Chunk, ...]
) -> tuple[bytes, ...]:
    """Validate the full selected space and freeze once, without renormalization."""
    if (
        not isinstance(batch, EmbeddingBatch)
        or (
            batch.kind,
            batch.model,
            batch.model_digest,
            batch.runtime_version,
            batch.dimensions,
            batch.normalization,
            batch.space_id,
        )
        != (
            "document",
            MODEL_NAME,
            MODEL_DIGEST,
            RUNTIME_VERSION,
            DIMENSIONS,
            "l2-f64-1",
            SPACE_ID,
        )
        or len(batch.embeddings) != len(chunks)
    ):
        raise UploadError("INDEX_VECTOR_INVALID", 503)
    frozen = []
    for embedding, chunk in zip(batch.embeddings, chunks, strict=True):
        if (
            embedding.source_id != chunk.chunk_id
            or embedding.text_hash != chunk.text_hash
            or len(embedding.vector) != DIMENSIONS
            or any(
                type(x) not in (float, int) or not math.isfinite(x)
                for x in embedding.vector
            )
            or not math.isclose(math.hypot(*embedding.vector), 1.0, abs_tol=1e-9)
        ):
            raise UploadError("INDEX_VECTOR_INVALID", 503)
        frozen.append(struct.pack("<768f", *embedding.vector))
    return tuple(frozen)


def index_profile(source, extraction) -> tuple[str, str]:
    """Hash content and every selected transform/embedding/storage identity."""
    profile = json.dumps(
        {
            "content_hash": source["content_hash"],
            "format": source["format"],
            "extraction": extraction["extraction_version"],
            "normalization": extraction["normalization_version"],
            "parser": extraction["parser_version"],
            "chunking": CHUNKING_VERSION,
            "chunk_bytes": [TARGET_BYTES, MAX_BYTES, OVERLAP_BYTES],
            "space_id": SPACE_ID,
            "storage": "little-endian-float32-1",
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(profile.encode()).hexdigest(), profile


def recover_indexes(store: "UploadStore") -> None:
    """Mark a rolled-back intent interrupted; never resume inference or delete data."""
    pending = store.connection.execute(
        "SELECT id FROM index_generations WHERE state='processing' LIMIT 1"
    ).fetchone()
    requests = store.connection.execute(
        "SELECT * FROM index_requests WHERE state='processing'"
    ).fetchall()
    if pending is None and not requests:
        return
    try:
        with store._write():
            if (
                pending is not None
                and store.connection.execute(
                    "SELECT 1 FROM index_vectors WHERE generation_id=? UNION ALL SELECT 1 FROM index_bindings WHERE generation_id=? LIMIT 1",
                    (pending[0], pending[0]),
                ).fetchone()
            ):
                raise UploadError("INDEX_RECOVERY_PENDING", 503)
            for request in requests:
                if store.connection.execute(
                    "SELECT 1 FROM index_bindings WHERE extraction_id=? AND generation_id=?",
                    (request["extraction_id"], request["generation_id"]),
                ).fetchone():
                    raise UploadError("INDEX_RECOVERY_PENDING", 503)
            store.connection.execute(
                "UPDATE index_requests SET state='failed',error_code='INDEX_INTERRUPTED' WHERE state='processing'"
            )
            if pending is not None:
                store.connection.execute(
                    "UPDATE index_generations SET state='failed',error_code='INDEX_INTERRUPTED' WHERE id=?",
                    (pending[0],),
                )
    except Exception:  # noqa: BLE001 - unresolved durable intent blocks admission
        store.recovery_pending = True


class IndexState:
    """Read only eligible current generations through conversation membership."""

    def __init__(self, store: "UploadStore") -> None:
        self.store, self.connection = store, store.connection

    def source(self, conversation: str, reference: str):
        """Require scoped CSV membership and the current complete extraction."""
        source = Extractions(self.store)._source(conversation, reference)
        extraction = Extractions(self.store)._complete(source["document_id"])
        if extraction is None:
            raise UploadError("EXTRACTION_REQUIRED", 409)
        return source, extraction

    def receipt(self, request) -> dict:
        """Return durable completion only when its matching binding is published."""
        row = self.connection.execute(
            """SELECT g.*,b.id AS binding_id FROM index_generations g
            LEFT JOIN index_bindings b ON b.generation_id=g.id AND b.extraction_id=?
            WHERE g.id=?""",
            (request["extraction_id"], request["generation_id"]),
        ).fetchone()
        complete = (
            request["state"] == "complete"
            and row["state"] == "complete"
            and row["binding_id"] is not None
        )
        if complete:
            counts = self.connection.execute(
                "SELECT (SELECT count(*) FROM index_chunks WHERE binding_id=?),(SELECT count(*) FROM index_omissions WHERE binding_id=?),(SELECT count(*) FROM index_vectors WHERE generation_id=?)",
                (row["binding_id"], row["binding_id"], row["id"]),
            ).fetchone()
            if tuple(counts) != (
                row["chunk_count"],
                row["omission_count"],
                row["chunk_count"],
            ):
                raise UploadError("INDEX_CONTENT_MISMATCH", 503)
        return {
            "operation_id": request["id"],
            "kind": "document_index",
            "generation_id": row["id"],
            "extraction_id": request["extraction_id"],
            "state": ("indexed_with_omissions" if row["omission_count"] else "indexed")
            if complete
            else request["state"],
            "indexed": complete,
            "ready": complete and row["omission_count"] == 0,
            "chunk_count": row["chunk_count"] if complete else 0,
            "omission_count": row["omission_count"] if complete else 0,
            "warning_codes": ["INDEX_OMISSIONS"]
            if complete and row["omission_count"]
            else [],
            "error_code": request["error_code"] or row["error_code"],
        }

    def status(self, conversation: str, reference: str) -> dict | None:
        """Read current-profile status, never reuse a historical incompatible space."""
        source, extraction = self.source(conversation, reference)
        identity, _ = index_profile(source, extraction)
        request = self.connection.execute(
            """SELECT r.* FROM index_requests r JOIN index_generations g ON g.id=r.generation_id
            WHERE r.reference_id=? AND r.extraction_id=? AND g.identity=?
            ORDER BY r.rowid DESC LIMIT 1""",
            (reference, extraction["id"], identity),
        ).fetchone()
        return None if request is None else self.receipt(request)

    def chunks(
        self, conversation: str, reference: str, *, after: int = 0, limit: int = 100
    ) -> tuple[Chunk, ...]:
        """Read one bounded page of source-specific provenance, not shared labels."""
        if (
            type(after) is not int
            or after < 0
            or type(limit) is not int
            or not 1 <= limit <= 100
        ):
            raise UploadError("INVALID_REQUEST")
        status = self.status(conversation, reference)
        if status is None or not status["indexed"]:
            raise UploadError("INDEX_REQUIRED", 409)
        rows = self.connection.execute(
            """SELECT c.payload,c.chunk_id,v.text_hash FROM index_chunks c
            JOIN index_bindings b ON b.id=c.binding_id AND b.generation_id=c.generation_id
            JOIN index_vectors v ON v.generation_id=c.generation_id AND v.ordinal=c.ordinal
            WHERE b.extraction_id=? AND b.generation_id=? AND c.ordinal>?
            ORDER BY c.ordinal LIMIT ?""",
            (status["extraction_id"], status["generation_id"], after, limit),
        )
        result = []
        for row in rows:
            chunk = Chunk.model_validate_json(row["payload"])
            if (
                chunk.chunk_id != row["chunk_id"]
                or chunk.text_hash != row["text_hash"]
                or chunk.source.extraction_id != status["extraction_id"]
            ):
                raise UploadError("INDEX_CONTENT_MISMATCH", 503)
            result.append(chunk)
        return tuple(result)
