"""Freeze only complete pinned document batches, without calling a model."""

import hashlib
import io
import math
import struct
from dataclasses import replace

import pytest

from app.ingestion.csv import CsvExtractor
from app.ingestion.models import NormalizedExtraction
from app.ingestion.validation import UploadError
from app.retrieval.chunking import iter_chunks
from app.retrieval.embeddings import Embedding, EmbeddingBatch
from app.storage.index_state import freeze_vectors, index_profile


@pytest.fixture
def vectors():
    body = b"Name,Units\nNorth,42\nSouth,50\n"
    extraction = NormalizedExtraction(
        document_id="document",
        content_hash=hashlib.sha256(body).hexdigest(),
        filename="authored.csv",
        format="csv",
        extraction_id="extraction",
        extraction_version="csv-stream-1",
        normalization_version="normalized-1",
        units=tuple(CsvExtractor(io.BytesIO(body), "extraction")),
    )
    chunks = tuple(iter_chunks(extraction))
    batch = EmbeddingBatch(
        "document",
        tuple(
            Embedding(c.chunk_id, c.text_hash, (1.0,) + (0.0,) * 767) for c in chunks
        ),
        None,
    )
    return chunks, batch


def test_complete_batch_freezes_exact_little_endian_float32(vectors, run_budget):
    chunks, batch = vectors
    frozen = freeze_vectors(batch, chunks)
    assert len(frozen) == 2 and len(frozen[0]) == 3072
    assert frozen[0] == struct.pack("<768f", *batch.embeddings[0].vector)
    for blob in frozen:
        run_budget.retain(blob)


@pytest.mark.parametrize(
    "field,value",
    [
        ("kind", "query"),
        ("space_id", "0" * 64),
        ("model", "other"),
        ("model_digest", "0" * 64),
        ("runtime_version", "other"),
        ("dimensions", 3),
        ("normalization", "other"),
    ],
)
def test_incompatible_space_is_not_persisted(vectors, field, value):
    chunks, batch = vectors
    with pytest.raises(UploadError, match="INDEX_VECTOR_INVALID"):
        freeze_vectors(replace(batch, **{field: value}), chunks)


@pytest.mark.parametrize(
    "change", ["short", "reordered", "hash", "nan", "zero", "bool", "scale"]
)
def test_incomplete_changed_or_invalid_vectors_are_not_persisted(vectors, change):
    chunks, batch = vectors
    entries = list(batch.embeddings)
    if change == "short":
        entries.pop()
    elif change == "reordered":
        entries.reverse()
    elif change == "hash":
        entries[0] = replace(entries[0], text_hash="0" * 64)
    else:
        first = {"nan": math.nan, "zero": 0.0, "bool": True, "scale": 2.0}[change]
        entries[0] = replace(entries[0], vector=(first,) + (0.0,) * 767)
    with pytest.raises(UploadError, match="INDEX_VECTOR_INVALID"):
        freeze_vectors(replace(batch, embeddings=tuple(entries)), chunks)


@pytest.mark.parametrize(
    "field", ["extraction_version", "normalization_version", "parser_version"]
)
def test_transform_version_changes_invalidate_the_generation_identity(field):
    source = {"content_hash": "1" * 64, "format": "csv"}
    extraction = {
        "extraction_version": "one",
        "normalization_version": "one",
        "parser_version": "one",
    }
    first, _ = index_profile(source, extraction)
    extraction[field] = "two"
    assert index_profile(source, extraction)[0] != first
