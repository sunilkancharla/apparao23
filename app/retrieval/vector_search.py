"""Exact reviewed sqlite-vec asset boundary; no wrapper import or fallback engine."""

import hashlib
import math
import sqlite3
import struct
from dataclasses import replace

from app.config import PROJECT_ROOT, validate_local_ancestry
from app.ingestion.validation import UploadError
from app.retrieval.embeddings import EmbeddingBatch

ASSET_ROOT = PROJECT_ROOT / ".venv/.cache/sqlite-vec-review/part-d-01"
ASSET_IDENTITIES = {
    "vec0.dll": (
        289280,
        "fcf98662a7ad9dce394b96a88f91032047823831b951c76636787c312a6476e6",
    ),
    "LICENSE-MIT": (
        1068,
        "6ce72bbe12d975bd5286e5ab0a064c069693300c47bccbc57bec18485f1621ea",
    ),
    "LICENSE-APACHE": (
        10931,
        "a38070a94d4afd9cd710e3ce67bd1de78097cfe1784c1f0109ac95d3c196bfdc",
    ),
}


def load_sqlite_vec(connection: sqlite3.Connection) -> None:
    """Verify exact DLL/notices; enable loading only for this absolute native path."""
    try:
        for name, (size, digest) in ASSET_IDENTITIES.items():
            path = ASSET_ROOT / name
            validate_local_ancestry(path)
            if (
                not path.is_file()
                or path.stat().st_nlink != 1
                or path.stat().st_size != size
                or hashlib.sha256(path.read_bytes()).hexdigest() != digest
            ):
                raise OSError
    except OSError:
        raise UploadError("VECTOR_ASSET_UNAVAILABLE", 503) from None
    try:
        try:
            connection.enable_load_extension(True)
            connection.load_extension(str(ASSET_ROOT / "vec0.dll"))
        finally:
            connection.enable_load_extension(False)
        if connection.execute("SELECT vec_version()").fetchone()[0] not in {
            "v0.1.9",
            "0.1.9",
        }:
            raise UploadError("VECTOR_VERSION_MISMATCH", 503)
    except (sqlite3.Error, OSError, AttributeError):
        raise UploadError("VECTOR_EXTENSION_UNAVAILABLE", 503) from None


def validate_vector(blob: bytes) -> None:
    """Reject malformed persisted float32 data before native distance evaluation."""
    if type(blob) is not bytes or len(blob) != 3072:
        raise UploadError("RETRIEVAL_VECTOR_INVALID", 503)
    values = struct.unpack("<768f", blob)
    if any(not math.isfinite(x) for x in values) or not math.isclose(
        math.hypot(*values), 1.0, abs_tol=1e-6
    ):
        raise UploadError("RETRIEVAL_VECTOR_INVALID", 503)


def freeze_query(batch: EmbeddingBatch, text: str, query_id: str) -> bytes:
    """Freeze exactly one query in the same pinned space as stored document vectors."""
    if (
        not isinstance(batch, EmbeddingBatch)
        or batch.kind != "query"
        or len(batch.embeddings) != 1
        or replace(batch, kind="document", embeddings=(), prompt_eval_count=None)
        != EmbeddingBatch("document", (), None)
    ):
        raise UploadError("RETRIEVAL_VECTOR_INVALID", 503)
    entry = batch.embeddings[0]
    try:
        if (
            entry.source_id != query_id
            or entry.text_hash != hashlib.sha256(text.encode()).hexdigest()
            or len(entry.vector) != 768
            or any(
                type(x) not in (float, int) or not math.isfinite(x)
                for x in entry.vector
            )
            or not math.isclose(math.hypot(*entry.vector), 1.0, abs_tol=1e-9)
        ):
            raise ValueError
        blob = struct.pack("<768f", *entry.vector)
        validate_vector(blob)
        return blob
    except (TypeError, ValueError, OverflowError, struct.error):
        raise UploadError("RETRIEVAL_VECTOR_INVALID", 503) from None
