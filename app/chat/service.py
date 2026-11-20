"""Grounded exchange orchestration with source-checked atomic publication."""

import asyncio
from contextlib import asynccontextmanager

from app.chat.generation import Answer, Claim, build_prompt
from app.ingestion.validation import UploadError
from app.ollama import OllamaError
from app.retrieval.search import Retriever
from app.storage.files import UploadStore
from app.storage.messages import Messages


@asynccontextmanager
async def unavailable_session():
    """No automatic launch/adoption: actual inference needs an explicitly owned factory."""
    raise UploadError("CHAT_RUNTIME_UNAVAILABLE", 503)
    yield  # pragma: no cover - async context-manager protocol


class ChatService:
    """Only current retrieved evidence can support new model claims; history is data."""

    def __init__(
        self,
        store: UploadStore,
        *,
        retriever: Retriever | None = None,
        retrieval_session=unavailable_session,
        chat_session=unavailable_session,
    ) -> None:
        self.store = store
        self.messages = Messages(store)
        self.retriever = retriever or Retriever(store)
        self.retrieval_session, self.chat_session = retrieval_session, chat_session

    async def ask(
        self, conversation: str, key: str, question: str, revision: int
    ) -> dict:
        """Persist no assistant exchange until termination, teardown and source checks pass."""
        request = self.messages.admit(conversation, key, question, revision)
        if not request["admitted_new"]:
            return self.messages.get(conversation, request["id"])
        try:
            async with asyncio.timeout(90):
                references = self.messages.selection(conversation)["references"]
                result = await self.retriever.retrieve(
                    conversation,
                    references,
                    question,
                    session_factory=self.retrieval_session,
                )
                versions = {v.reference_id: v for v in result.snapshot}
                if (
                    len(versions) != len(result.snapshot)
                    or not set(versions).issubset(references)
                    or any(
                        b.reference_id not in references or b.reference_id in versions
                        for b in result.blocked
                    )
                    or len({e.evidence_id for e in result.evidence})
                    != len(result.evidence)
                ):
                    raise UploadError("CHAT_EVIDENCE_INVALID", 503)
                for item in result.evidence:
                    version = versions.get(item.hit.reference_id)
                    source = item.hit.chunk.source
                    if version is None or (
                        source.document_id,
                        source.content_hash,
                        source.extraction_id,
                    ) != (
                        version.document_id,
                        version.content_hash,
                        version.extraction_id,
                    ):
                        raise UploadError("CHAT_EVIDENCE_INVALID", 503)
                self.store.busy = True
                history = self.messages.history(conversation, result.snapshot)
                prompt = build_prompt(question, result.evidence, history)
                warnings = list(dict.fromkeys((*result.warnings, *prompt.warnings)))
                if not prompt.evidence:
                    answer = Answer(
                        status="insufficient_evidence",
                        claims=(
                            Claim(
                                text="No usable selected evidence is available. Select indexed sources or narrow the question.",
                                citations=(),
                            ),
                        ),
                    )
                    warnings.append("NO_EVIDENCE")
                else:
                    self.store.busy = False
                    async with self.chat_session() as model:
                        if not self.store.busy:
                            raise UploadError("CHAT_RUNTIME_UNOWNED", 503)
                        answer = await model.generate(prompt)
                    self.store.busy = True
                    answer = Answer.model_validate(answer.model_dump())
                    allowed = {item.evidence_id for item in prompt.evidence}
                    if any(
                        set(c.citations) - allowed
                        or not c.text.strip()
                        or (
                            answer.status in {"answered", "partial"} and not c.citations
                        )
                        for c in answer.claims
                    ):
                        raise UploadError("CHAT_RESPONSE_INVALID", 503)
                await self.retriever._recheck(
                    conversation, tuple(references), result.snapshot, result.blocked
                )
                manifest = []
                for evidence in prompt.evidence:
                    chunk = evidence.hit.chunk
                    version = next(
                        v
                        for v in result.snapshot
                        if v.reference_id == evidence.hit.reference_id
                    )
                    manifest.append(
                        {
                            "evidence_id": evidence.evidence_id,
                            "reference_id": evidence.hit.reference_id,
                            "document_id": chunk.source.document_id,
                            "content_hash": chunk.source.content_hash,
                            "extraction_id": chunk.source.extraction_id,
                            "generation_id": version.generation_id,
                            "chunk_id": chunk.chunk_id,
                            "text_hash": chunk.text_hash,
                            "filename": chunk.source.filename,
                            "locations": [p.location.model_dump() for p in chunk.parts],
                            "warnings": list(chunk.warnings),
                        }
                    )
                self.messages.finish(
                    request["id"],
                    answer.model_dump(mode="json"),
                    result.snapshot,
                    manifest,
                    warnings,
                )
                return self.messages.get(conversation, request["id"])
        except BaseException as error:
            code = (
                error.code
                if isinstance(error, (UploadError, OllamaError))
                else "CHAT_INTERRUPTED"
            )
            if not self.store.recovery_pending:
                try:
                    self.messages.fail(request["id"], code)
                except Exception:  # noqa: BLE001 - unresolved durable intent blocks admission
                    self.store.recovery_pending = True
            if isinstance(error, UploadError) or not isinstance(error, Exception):
                raise
            raise UploadError(code, 503) from None
        finally:
            if not self.store.recovery_pending:
                self.store.busy = False
