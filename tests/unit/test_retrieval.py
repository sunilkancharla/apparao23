"""Pinned native seam and query validation; never load a real extension here."""

import hashlib
import sqlite3
import struct
from dataclasses import replace

import pytest

from app.ingestion.validation import UploadError
from app.retrieval import vector_search as native
from app.retrieval.embeddings import Embedding, EmbeddingBatch


def query_batch(text="North?", query_id="query"):
    return EmbeddingBatch(
        "query",
        (
            Embedding(
                query_id,
                hashlib.sha256(text.encode()).hexdigest(),
                (1.0,) + (0.0,) * 767,
            ),
        ),
        None,
    )


@pytest.mark.parametrize(
    "field,value",
    [
        ("kind", "document"),
        ("space_id", "0" * 64),
        ("model", "other"),
        ("model_digest", "0" * 64),
        ("runtime_version", "other"),
        ("dimensions", 4),
        ("normalization", "other"),
    ],
)
def test_query_rejects_incompatible_identity(field, value):
    with pytest.raises(UploadError, match="RETRIEVAL_VECTOR_INVALID"):
        native.freeze_query(replace(query_batch(), **{field: value}), "North?", "query")


@pytest.mark.parametrize(
    "change", ["hash", "id", "count", "nan", "zero", "bool", "dimension"]
)
def test_query_rejects_mismatched_or_invalid_vector(change):
    batch = query_batch()
    entry = batch.embeddings[0]
    if change in ("hash", "id"):
        entry = replace(
            entry, **{"text_hash" if change == "hash" else "source_id": "wrong"}
        )
    elif change == "dimension":
        entry = replace(entry, vector=(1.0,))
    elif change != "count":
        entry = replace(
            entry,
            vector=({"nan": float("nan"), "zero": 0.0, "bool": True}[change],)
            + (0.0,) * 767,
        )
    batch = replace(batch, embeddings=() if change == "count" else (entry,))
    with pytest.raises(UploadError, match="RETRIEVAL_VECTOR_INVALID"):
        native.freeze_query(batch, "North?", "query")


def test_query_freezes_exact_float32_bytes():
    assert native.freeze_query(query_batch(), "North?", "query") == struct.pack(
        "<768f", 1, *([0] * 767)
    )


@pytest.mark.parametrize("failure", [False, True])
def test_loader_disables_extension_loading_even_on_failure(
    tmp_path, monkeypatch, failure
):
    (tmp_path / "vec0.dll").write_bytes(b"dummy never loaded")
    monkeypatch.setattr(native, "ASSET_ROOT", tmp_path)
    monkeypatch.setattr(
        native,
        "ASSET_IDENTITIES",
        {"vec0.dll": (18, hashlib.sha256(b"dummy never loaded").hexdigest())},
    )

    class Fake:
        def __init__(self):
            self.events = []

        def enable_load_extension(self, enabled):
            self.events.append(enabled)

        def load_extension(self, path):
            assert path == str(tmp_path / "vec0.dll")
            if failure:
                raise sqlite3.OperationalError("synthetic private path")

        def execute(self, sql):
            return self

        def fetchone(self):
            return ("v0.1.9",)

    connection = Fake()
    if failure:
        with pytest.raises(UploadError, match="VECTOR_EXTENSION_UNAVAILABLE"):
            native.load_sqlite_vec(connection)
    else:
        native.load_sqlite_vec(connection)
    assert connection.events == [True, False]


def test_changed_asset_refuses_before_loading(tmp_path, monkeypatch):
    monkeypatch.setattr(native, "ASSET_ROOT", tmp_path)

    class Refused:
        def enable_load_extension(self, enabled):
            pytest.fail("Unverified asset admitted")

    with pytest.raises(UploadError, match="VECTOR_ASSET_UNAVAILABLE"):
        native.load_sqlite_vec(Refused())
