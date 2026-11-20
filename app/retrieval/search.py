"""Scoped candidate retrieval and complete evidence packing, without answer claims."""

import asyncio
import heapq
import json
import math
import sqlite3
import time
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from itertools import pairwise
from uuid import uuid4

from app.ingestion.validation import UploadError
from app.ollama import OllamaError
from app.retrieval.embeddings import Embedder
from app.retrieval.models import Chunk
from app.retrieval.vector_search import freeze_query, load_sqlite_vec, validate_vector
from app.storage.extractions import Extractions
from app.storage.files import UploadStore
from app.storage.index_state import IndexState


@dataclass(frozen=True)
class SourceVersion:
    """Observed eligible identity, not permission to use a source after a change."""

    reference_id: str
    document_id: str
    content_hash: str
    extraction_id: str
    generation_id: str
    binding_id: str
    chunk_count: int
    omission_count: int


@dataclass(frozen=True)
class BlockedSource:
    """Known selected source excluded with a fixed diagnostic code."""

    reference_id: str
    code: str


@dataclass(frozen=True)
class Hit:
    """Ranked candidate with scoped provenance; distance is not answer support."""

    reference_id: str
    chunk: Chunk
    distance: float


@dataclass(frozen=True)
class Evidence:
    """Response-local identifier allocated only for actually supplied text."""

    evidence_id: str
    hit: Hit
    rendered: str


@dataclass(frozen=True)
class RetrievalResult:
    """Separate ranked, supplied, omitted, blocked and source-version observations."""

    status: str
    ranked: tuple[Hit, ...]
    evidence: tuple[Evidence, ...]
    omitted: tuple[tuple[str, str], ...]
    blocked: tuple[BlockedSource, ...]
    snapshot: tuple[SourceVersion, ...]
    warnings: tuple[str, ...]
    evidence_bytes: int


class Retriever:
    """One store/event-loop owner; model runtime must own that store's work slot."""

    def __init__(
        self, store: UploadStore, *, loader: Callable = load_sqlite_vec
    ) -> None:
        self.store, self.connection, self.loader = store, store.connection, loader

    async def _resolve(self, conversation: str, references: tuple[str, ...]):
        versions, blocked = [], []
        for reference in references:
            # Missing/foreign membership fails the whole request, never broadens it.
            try:
                source = Extractions(self.store)._source(conversation, reference)
            except UploadError as error:
                if error.code not in {"SOURCE_UNAVAILABLE", "UNSUPPORTED_FORMAT"}:
                    raise
                blocked.append(BlockedSource(reference, error.code))
                continue
            try:
                status = IndexState(self.store).status(conversation, reference)
                if status is None or not status["indexed"]:
                    raise UploadError("INDEX_REQUIRED", 409)
                await asyncio.to_thread(
                    self.store._verified_original,
                    source["content_hash"],
                    source["byte_size"],
                )
                binding = self.connection.execute(
                    "SELECT id FROM index_bindings WHERE extraction_id=? AND generation_id=?",
                    (status["extraction_id"], status["generation_id"]),
                ).fetchone()
                if binding is None:
                    raise UploadError("INDEX_REQUIRED", 409)
                versions.append(
                    SourceVersion(
                        reference,
                        source["document_id"],
                        source["content_hash"],
                        status["extraction_id"],
                        status["generation_id"],
                        binding[0],
                        status["chunk_count"],
                        status["omission_count"],
                    )
                )
            except UploadError as error:
                if error.code not in {
                    "INDEX_REQUIRED",
                    "EXTRACTION_REQUIRED",
                    "SOURCE_UNAVAILABLE",
                }:
                    raise
                blocked.append(BlockedSource(reference, error.code))
        return tuple(versions), tuple(blocked)

    async def _recheck(self, conversation, references, versions, blocked) -> None:
        try:
            current = await self._resolve(conversation, references)
        except UploadError:
            raise UploadError("SOURCE_CHANGED", 409) from None
        if current != (versions, blocked):
            raise UploadError("SOURCE_CHANGED", 409)

    def _rank(
        self, versions: tuple[SourceVersion, ...], query: bytes, deadline: float
    ) -> tuple[Hit, ...]:
        selected = {v.reference_id: v for v in versions}
        values = ",".join("(?,?)" for _ in versions)
        parameters = tuple(x for v in versions for x in (v.reference_id, v.binding_id))
        prefix = f"""WITH selected(reference_id,binding_id) AS (VALUES {values})
        SELECT s.reference_id,c.chunk_id,c.payload,v.text_hash,v.vector
        FROM selected s JOIN index_bindings b ON b.id=s.binding_id
        JOIN index_chunks c ON c.binding_id=b.id AND c.generation_id=b.generation_id
        JOIN index_vectors v ON v.generation_id=c.generation_id AND v.ordinal=c.ordinal"""
        expected = sum(v.chunk_count for v in versions)
        try:
            self.connection.set_progress_handler(
                lambda: int(time.monotonic() >= deadline), 1000
            )
            count = 0
            for row in self.connection.execute(prefix, parameters):
                if time.monotonic() >= deadline:
                    raise UploadError("RETRIEVAL_TIMEOUT", 503)
                validate_vector(row["vector"])
                count += 1
            if count != expected:
                raise UploadError("RETRIEVAL_INDEX_INVALID", 503)
            self.loader(self.connection)
            scored = prefix.replace(
                "v.vector\n",
                "v.vector,vec_distance_cosine(v.vector,?) AS distance\n",
                1,
            )

            def candidates():
                count = 0
                for row in self.connection.execute(scored, (*parameters, query)):
                    count += 1
                    if time.monotonic() >= deadline:
                        raise UploadError("RETRIEVAL_TIMEOUT", 503)
                    distance = row["distance"]
                    if (
                        type(distance) not in (float, int)
                        or not math.isfinite(distance)
                        or not -1e-6 <= distance <= 2.000001
                    ):
                        raise UploadError("RETRIEVAL_DISTANCE_INVALID", 503)
                    yield row
                if count != expected:
                    raise UploadError("RETRIEVAL_INDEX_INVALID", 503)

            rows = heapq.nsmallest(
                5,
                candidates(),
                key=lambda r: (r["distance"], r["chunk_id"], r["reference_id"]),
            )
            hits = []
            for row in rows:
                chunk = Chunk.model_validate_json(row["payload"])
                version = selected[row["reference_id"]]
                if (
                    chunk.chunk_id != row["chunk_id"]
                    or chunk.text_hash != row["text_hash"]
                    or (
                        chunk.source.document_id,
                        chunk.source.content_hash,
                        chunk.source.extraction_id,
                    )
                    != (
                        version.document_id,
                        version.content_hash,
                        version.extraction_id,
                    )
                ):
                    raise UploadError("RETRIEVAL_INDEX_INVALID", 503)
                hits.append(Hit(row["reference_id"], chunk, row["distance"]))
            return tuple(hits)
        finally:
            self.connection.set_progress_handler(None, 0)

    @staticmethod
    def _pack(ranked: tuple[Hit, ...]):
        evidence, omitted, size = [], [], 0
        for hit in ranked:
            identity = "ev_" + uuid4().hex
            label = json.dumps(
                {
                    "evidence_id": identity,
                    "filename": hit.chunk.source.filename,
                    "reference_id": hit.reference_id,
                },
                ensure_ascii=False,
                separators=(",", ":"),
            )
            rendered = label + "\n" + hit.chunk.text
            charge = len(rendered.encode()) + (2 if evidence else 0)
            if size + charge > 2000:
                omitted.append((hit.reference_id, hit.chunk.chunk_id))
                continue
            evidence.append(Evidence(identity, hit, rendered))
            size += charge
        return tuple(evidence), tuple(omitted), size

    async def retrieve(
        self,
        conversation: str,
        references: list[str] | tuple[str, ...] | None,
        question: str,
        *,
        session_factory: Callable[[], AbstractAsyncContextManager[Embedder]],
    ) -> RetrievalResult:
        """Retrieve from explicit selection; never infer semantic support from rank."""
        if references is None:
            raise UploadError("SELECTION_REQUIRED", 409)
        if (
            not isinstance(references, (tuple, list))
            or len(references) > 10
            or any(not isinstance(r, str) or not 1 <= len(r) <= 128 for r in references)
            or len(set(references)) != len(references)
        ):
            raise UploadError("INVALID_SELECTION")
        try:
            if (
                not isinstance(question, str)
                or not question.strip()
                or len(question.encode()) > 512
            ):
                raise ValueError
        except (ValueError, UnicodeError):
            raise UploadError("RETRIEVAL_QUESTION_INVALID") from None
        if (
            self.store.busy
            or self.store.recovery_pending
            or self.store.connection is None
        ):
            raise UploadError("UPLOAD_BUSY", 409)
        self.store.busy = True
        references = tuple(references)
        deadline = time.monotonic() + 90
        try:
            async with asyncio.timeout(90):
                if not self.connection.execute(
                    "SELECT 1 FROM conversations WHERE id=?", (conversation,)
                ).fetchone():
                    raise UploadError("CONVERSATION_NOT_FOUND", 404)
                versions, blocked = await self._resolve(conversation, references)
                if not versions:
                    return RetrievalResult(
                        "no_evidence", (), (), (), blocked, (), ("NO_EVIDENCE",), 0
                    )
                self.store.busy = False
                async with session_factory() as embedder:
                    if not self.store.busy:
                        raise UploadError("RETRIEVAL_RUNTIME_UNOWNED", 503)
                    query_id = uuid4().hex
                    query = freeze_query(
                        await embedder.query(question, query_id), question, query_id
                    )
                self.store.busy = True
                await self._recheck(conversation, references, versions, blocked)
                ranked = self._rank(versions, query, deadline)
                await self._recheck(conversation, references, versions, blocked)
                supplied, omitted, size = self._pack(ranked)
                warnings = ["ANSWERABILITY_UNASSESSED", "TOKEN_FIT_UNVERIFIED"]
                if blocked:
                    warnings.append("SOURCES_UNAVAILABLE")
                if omitted:
                    warnings.append("EVIDENCE_BUDGET")
                if any(v.omission_count for v in versions):
                    warnings.append("INDEX_OMISSIONS")
                if any(a.distance == b.distance for a, b in pairwise(ranked)):
                    warnings.append("DISTANCE_TIE")
                return RetrievalResult(
                    "candidates" if supplied else "no_evidence",
                    ranked,
                    supplied,
                    omitted,
                    blocked,
                    versions,
                    tuple(warnings),
                    size,
                )
        except UploadError:
            raise
        except OllamaError as error:
            raise UploadError(error.code, 503) from None
        except TimeoutError:
            raise UploadError("RETRIEVAL_TIMEOUT", 503) from None
        except (ValueError, OSError, sqlite3.Error):
            raise UploadError("RETRIEVAL_FAILED", 503) from None
        finally:
            if not self.store.recovery_pending:
                self.store.busy = False
