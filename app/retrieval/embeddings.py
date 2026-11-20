"""Pinned Nomic request/response contract; no index, downloads or runtime launch."""

import asyncio
import hashlib
import json
import math
from dataclasses import dataclass
from typing import Literal

from app.diagnostics import MODEL_MANIFESTS
from app.ollama import OllamaClient
from app.ollama import OllamaError as EmbeddingError
from app.retrieval.models import Chunk

MODEL_NAME = "nomic-embed-text:v1.5"
MODEL_DIGEST = MODEL_MANIFESTS["embedding_model"][1]
RUNTIME_VERSION = "0.40.16"
DIMENSIONS = 768
MAX_BATCH = 8
DOCUMENT_PREFIX = "search_document: "
QUERY_PREFIX = "search_query: "
_OPTIONS = {"num_ctx": 2048, "num_gpu": 0, "num_thread": 4, "num_batch": 64}
SPACE_ID = hashlib.sha256(
    json.dumps(
        {
            "model": MODEL_NAME,
            "digest": MODEL_DIGEST,
            "runtime": RUNTIME_VERSION,
            "dimensions": DIMENSIONS,
            "document_prefix": DOCUMENT_PREFIX,
            "query_prefix": QUERY_PREFIX,
            "options": _OPTIONS,
            "normalization": "l2-f64-1",
        },
        sort_keys=True,
    ).encode()
).hexdigest()


@dataclass(frozen=True)
class Embedding:
    """A complete normalized vector tied to the unchanged input identity/hash."""

    source_id: str
    text_hash: str
    vector: tuple[float, ...]


@dataclass(frozen=True)
class EmbeddingBatch:
    """One atomic in-memory batch; token counts describe completed processing."""

    kind: Literal["document", "query"]
    embeddings: tuple[Embedding, ...]
    prompt_eval_count: int | None
    model: str = MODEL_NAME
    model_digest: str = MODEL_DIGEST
    runtime_version: str = RUNTIME_VERSION
    dimensions: int = DIMENSIONS
    normalization: str = "l2-f64-1"
    space_id: str = SPACE_ID


class Embedder:
    """Bound a single batch to approved identities and refuse partial vectors.

    Busy refusal applies to this instance; the runtime owner must additionally
    enforce the app's shared heavy-job lease. Inputs are never logged or saved.
    """

    def __init__(self, client: OllamaClient) -> None:
        self.client = client
        self._busy = False

    async def documents(
        self, chunks: list[Chunk] | tuple[Chunk, ...]
    ) -> EmbeddingBatch:
        """Embed one through eight complete T26 chunks, preserving their order."""
        if not 1 <= len(chunks) <= MAX_BATCH or any(
            not isinstance(c, Chunk) for c in chunks
        ):
            raise EmbeddingError("EMBEDDING_INPUT_INVALID")
        if len({c.chunk_id for c in chunks}) != len(chunks):
            raise EmbeddingError("EMBEDDING_INPUT_INVALID")
        return await self._embed(
            tuple((c.chunk_id, c.text_hash, c.text) for c in chunks), "document"
        )

    async def query(self, text: str, query_id: str) -> EmbeddingBatch:
        """Embed one nonempty question within the provisional 512-byte guard."""
        try:
            encoded = text.encode("utf-8") if isinstance(text, str) else b""
        except UnicodeError:
            raise EmbeddingError("EMBEDDING_INPUT_INVALID") from None
        if (
            not isinstance(text, str)
            or not text.strip()
            or len(encoded) > 512
            or not isinstance(query_id, str)
            or not query_id.strip()
        ):
            raise EmbeddingError("EMBEDDING_INPUT_INVALID")
        return await self._embed(
            ((query_id, hashlib.sha256(encoded).hexdigest(), text),),
            "query",
        )

    async def _verify(self) -> None:
        if (await self.client.request("GET", "/api/version")).get(
            "version"
        ) != RUNTIME_VERSION:
            raise EmbeddingError("OLLAMA_VERSION_MISMATCH")
        models = (await self.client.request("GET", "/api/tags")).get("models")
        if not isinstance(models, list) or any(not isinstance(m, dict) for m in models):
            raise EmbeddingError("OLLAMA_RESPONSE_INVALID")
        matches = [m for m in models if m.get("name") == MODEL_NAME]
        if not matches:
            raise EmbeddingError("MODEL_MISSING")
        if len(matches) != 1 or matches[0].get("digest") != MODEL_DIGEST:
            raise EmbeddingError("MODEL_MISMATCH")

    async def _embed(
        self,
        inputs: tuple[tuple[str, str, str], ...],
        kind: Literal["document", "query"],
    ) -> EmbeddingBatch:
        if self._busy:
            raise EmbeddingError("EMBEDDING_BUSY")
        self._busy = True
        try:
            async with asyncio.timeout(self.client.timeout):
                await self._verify()
                prefix = DOCUMENT_PREFIX if kind == "document" else QUERY_PREFIX
                response = await self.client.request(
                    "POST",
                    "/api/embed",
                    {
                        "model": MODEL_NAME,
                        "input": [prefix + item[2] for item in inputs],
                        "truncate": False,
                        "keep_alive": 0,
                        "options": dict(_OPTIONS),
                    },
                )
                vectors = response.get("embeddings")
                if response.get("truncated", False) is not False:
                    raise EmbeddingError("EMBEDDING_TRUNCATED")
                if (
                    response.get("model") != MODEL_NAME
                    or not isinstance(vectors, list)
                    or len(vectors) != len(inputs)
                ):
                    raise EmbeddingError("EMBEDDING_RESPONSE_INVALID")
                records = []
                for (source_id, text_hash, _), vector in zip(
                    inputs, vectors, strict=True
                ):
                    if (
                        not isinstance(vector, list)
                        or len(vector) != DIMENSIONS
                        or any(type(v) not in (int, float) for v in vector)
                    ):
                        raise EmbeddingError("EMBEDDING_VECTOR_INVALID")
                    try:
                        values = tuple(float(v) for v in vector)
                    except OverflowError:
                        raise EmbeddingError("EMBEDDING_VECTOR_INVALID") from None
                    if any(not math.isfinite(v) for v in values):
                        raise EmbeddingError("EMBEDDING_VECTOR_INVALID")
                    scale = max(abs(v) for v in values)
                    if scale == 0:
                        raise EmbeddingError("EMBEDDING_VECTOR_INVALID")
                    scaled = tuple(v / scale for v in values)
                    norm = math.hypot(*scaled)
                    records.append(
                        Embedding(source_id, text_hash, tuple(v / norm for v in scaled))
                    )
                count = response.get("prompt_eval_count")
                if count is not None and (type(count) is not int or count < 0):
                    raise EmbeddingError("EMBEDDING_RESPONSE_INVALID")
                await self._verify()
                return EmbeddingBatch(kind, tuple(records), count)
        except TimeoutError:
            raise EmbeddingError("OLLAMA_TIMEOUT") from None
        finally:
            self._busy = False
