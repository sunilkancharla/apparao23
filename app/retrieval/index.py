"""Stream stored CSV chunks into atomic content vectors and scoped source bindings."""

import asyncio
import hashlib
import json
import re
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from uuid import uuid4

from app.ingestion.models import NormalizedExtraction, SourceUnit
from app.ingestion.validation import UploadError
from app.retrieval.chunking import iter_chunks
from app.retrieval.embeddings import MAX_BATCH, Embedder
from app.retrieval.models import Chunk
from app.storage.files import UploadStore
from app.storage.index_state import IndexState, freeze_vectors, index_profile


class LocalIndex:
    """Trusted backend only; session_factory must own this store's runtime lease."""

    def __init__(self, store: UploadStore) -> None:
        self.store, self.connection = store, store.connection
        self.state = IndexState(store)

    async def _verify(self, conversation, reference, source, extraction) -> None:
        await asyncio.to_thread(
            self.store._verified_original, source["content_hash"], source["byte_size"]
        )
        current, current_extraction = self.state.source(conversation, reference)
        if (
            current["document_id"] != source["document_id"]
            or current_extraction["id"] != extraction["id"]
        ):
            raise UploadError("SOURCE_CHANGED", 409)

    async def _publish(self, extraction, generation, embedder):
        binding = str(uuid4())
        self.connection.execute(
            "INSERT INTO index_bindings VALUES (?,?,?)",
            (binding, extraction["id"], generation["id"]),
        )
        envelope = NormalizedExtraction.model_validate(
            json.loads(extraction["manifest"]) | {"units": []}
        )

        def units():
            for row in self.connection.execute(
                "SELECT payload FROM csv_units WHERE extraction_id=? ORDER BY ordinal",
                (extraction["id"],),
            ):
                yield SourceUnit.model_validate_json(row[0])

        count, omitted, pending = 0, 0, []

        async def flush():
            nonlocal count
            if not pending:
                return
            chunks = tuple(pending)
            frozen = (
                freeze_vectors(await embedder.documents(chunks), chunks)
                if embedder is not None
                else None
            )
            for position, chunk in enumerate(chunks):
                count += 1
                payload = chunk.model_dump_json()
                self.store.reserve_growth(len(payload.encode()) + 3072)
                if frozen is not None:
                    self.connection.execute(
                        "INSERT INTO index_vectors VALUES (?,?,?,?)",
                        (generation["id"], count, chunk.text_hash, frozen[position]),
                    )
                else:
                    previous = self.connection.execute(
                        "SELECT text_hash FROM index_vectors WHERE generation_id=? AND ordinal=?",
                        (generation["id"], count),
                    ).fetchone()
                    if previous is None or previous[0] != chunk.text_hash:
                        raise UploadError("INDEX_CONTENT_MISMATCH", 503)
                self.connection.execute(
                    "INSERT INTO index_chunks VALUES (?,?,?,?,?)",
                    (binding, count, generation["id"], chunk.chunk_id, payload),
                )
            pending.clear()

        for item in iter_chunks(envelope, units()):
            if isinstance(item, Chunk):
                pending.append(item)
                if len(pending) == MAX_BATCH:
                    await flush()
            else:
                omitted += 1
                payload = item.model_dump_json()
                self.store.reserve_growth(len(payload.encode()))
                self.connection.execute(
                    "INSERT INTO index_omissions VALUES (?,?,?)",
                    (binding, omitted, payload),
                )
        await flush()
        if count == 0:
            raise UploadError("INDEX_NO_EVIDENCE", 409)
        if embedder is None and (count, omitted) != (
            generation["chunk_count"],
            generation["omission_count"],
        ):
            raise UploadError("INDEX_CONTENT_MISMATCH", 503)
        return count, omitted

    async def index(
        self,
        conversation: str,
        reference: str,
        key: str,
        *,
        session_factory: Callable[[], AbstractAsyncContextManager[Embedder]],
    ) -> dict:
        """Publish one complete generation; retries need a deliberate new request key."""
        if not isinstance(key, str) or not re.fullmatch(r"[A-Za-z0-9_-]{8,128}", key):
            raise UploadError("INVALID_REQUEST")
        if (
            self.store.busy
            or self.store.recovery_pending
            or self.store.connection is None
        ):
            raise UploadError("UPLOAD_BUSY", 409)
        self.store.busy = True
        generation, created, request_id = None, False, None
        try:
            source, extraction = self.state.source(conversation, reference)
            await self._verify(conversation, reference, source, extraction)
            identity, profile = index_profile(source, extraction)
            key_hash = hashlib.sha256(key.encode("ascii")).hexdigest()
            with self.store._write():
                request = self.connection.execute(
                    "SELECT * FROM index_requests WHERE reference_id=? AND key_hash=?",
                    (reference, key_hash),
                ).fetchone()
                if request is not None:
                    previous = self.connection.execute(
                        "SELECT * FROM index_generations WHERE id=?",
                        (request["generation_id"],),
                    ).fetchone()
                    if (
                        previous["identity"] != identity
                        or request["extraction_id"] != extraction["id"]
                    ):
                        raise UploadError("INDEX_VERSION_CHANGED", 409)
                    receipt = self.state.receipt(request)
                    if not receipt["indexed"]:
                        raise UploadError(receipt["error_code"] or "INDEX_PENDING", 409)
                    return receipt
                if self.connection.execute(
                    "SELECT 1 FROM index_requests WHERE state='processing'"
                ).fetchone():
                    raise UploadError("INDEX_PENDING", 409)
                generation = self.connection.execute(
                    "SELECT * FROM index_generations WHERE identity=? AND state='complete'",
                    (identity,),
                ).fetchone()
                if generation is None:
                    if self.connection.execute(
                        "SELECT 1 FROM index_generations WHERE state='processing'"
                    ).fetchone():
                        raise UploadError("INDEX_PENDING", 409)
                    generation_id = str(uuid4())
                    self.store.reserve_growth(len(profile.encode()))
                    self.connection.execute(
                        "INSERT INTO index_generations (id,identity,content_hash,profile,state) VALUES (?,?,?,?,'processing')",
                        (generation_id, identity, source["content_hash"], profile),
                    )
                    generation = self.connection.execute(
                        "SELECT * FROM index_generations WHERE id=?", (generation_id,)
                    ).fetchone()
                    created = True
                request_id = str(uuid4())
                self.connection.execute(
                    "INSERT INTO index_requests VALUES (?,?,?,?,?,'processing',NULL)",
                    (
                        request_id,
                        reference,
                        key_hash,
                        extraction["id"],
                        generation["id"],
                    ),
                )
            binding = self.connection.execute(
                "SELECT 1 FROM index_bindings WHERE extraction_id=? AND generation_id=?",
                (extraction["id"], generation["id"]),
            ).fetchone()
            if binding is None:
                if created:
                    # No await occurs between handing the slot back and the
                    # owned session claiming it; the same event-loop owner is required.
                    self.store.busy = False
                with self.store._write():
                    if created:
                        async with session_factory() as embedder:
                            if not self.store.busy:
                                raise UploadError("INDEX_RUNTIME_UNOWNED", 503)
                            counts = await self._publish(
                                extraction, generation, embedder
                            )
                        # Publication happens only after verified native teardown.
                        self.store.busy = True
                    else:
                        counts = await self._publish(extraction, generation, None)
                    await self._verify(conversation, reference, source, extraction)
                    if created:
                        self.connection.execute(
                            "UPDATE index_generations SET state='complete',chunk_count=?,omission_count=? WHERE id=?",
                            (*counts, generation["id"]),
                        )
                    self.connection.execute(
                        "UPDATE index_requests SET state='complete' WHERE id=?",
                        (request_id,),
                    )
            else:
                with self.store._write():
                    self.connection.execute(
                        "UPDATE index_requests SET state='complete' WHERE id=?",
                        (request_id,),
                    )
            request = self.connection.execute(
                "SELECT * FROM index_requests WHERE id=?", (request_id,)
            ).fetchone()
            return self.state.receipt(request)
        except BaseException as error:
            if request_id is not None and not self.store.recovery_pending:
                try:
                    with self.store._write():
                        code = (
                            error.code
                            if isinstance(error, UploadError)
                            else "INDEX_INTERRUPTED"
                        )
                        self.connection.execute(
                            "UPDATE index_requests SET state='failed',error_code=? WHERE id=? AND state='processing'",
                            (code, request_id),
                        )
                        if created:
                            self.connection.execute(
                                "UPDATE index_generations SET state='failed',error_code=? WHERE id=? AND state='processing'",
                                (code, generation["id"]),
                            )
                except Exception:  # noqa: BLE001 - keep intent and block admission
                    self.store.recovery_pending = True
            if isinstance(error, UploadError) or not isinstance(error, Exception):
                raise
            raise UploadError("INDEX_FAILED", 503) from None
        finally:
            if not self.store.recovery_pending:
                self.store.busy = False
