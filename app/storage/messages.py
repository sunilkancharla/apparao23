"""Atomic scoped selection revisions, answer intents and complete saved exchanges."""

import hashlib
import json
import re
from dataclasses import asdict
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from app.chat.generation import CHAT_DIGEST, CHAT_MODEL
from app.ingestion.validation import UploadError
from app.retrieval.search import SourceVersion
from app.storage.index_state import IndexState

if TYPE_CHECKING:
    from app.storage.files import UploadStore


def recover_messages(store: "UploadStore") -> None:
    """Resolve rolled-back answer intents without inference, retry or text deletion."""
    if not store.connection.execute(
        "SELECT 1 FROM chat_requests WHERE state='processing'"
    ).fetchone():
        return
    try:
        with store._write():
            if store.connection.execute(
                "SELECT 1 FROM chat_requests r JOIN chat_exchanges e ON e.request_id=r.id WHERE r.state='processing'"
            ).fetchone():
                raise UploadError("CHAT_RECOVERY_PENDING", 503)
            store.connection.execute(
                "UPDATE chat_requests SET state='failed',error_code='CHAT_INTERRUPTED' WHERE state='processing'"
            )
    except Exception:  # noqa: BLE001 - durable uncertainty blocks heavy admission
        store.recovery_pending = True


class Messages:
    """One store/event-loop owner; publication checks share the exchange transaction."""

    def __init__(self, store: "UploadStore") -> None:
        self.store, self.connection = store, store.connection

    def selection(self, conversation: str) -> dict:
        """Read explicit saved scope; absent selection means empty, not all sources."""
        if not self.connection.execute(
            "SELECT 1 FROM conversations WHERE id=?", (conversation,)
        ).fetchone():
            raise UploadError("CONVERSATION_NOT_FOUND", 404)
        row = self.connection.execute(
            "SELECT * FROM chat_selections WHERE conversation_id=?", (conversation,)
        ).fetchone()
        return (
            {
                "revision": row["revision"],
                "references": json.loads(row["references_json"]),
            }
            if row
            else {"revision": 0, "references": []}
        )

    def select(
        self, conversation: str, references: list[str], expected_revision: int
    ) -> dict:
        """CAS metadata selection even during inference, invalidating in-flight answers."""
        if self.store.recovery_pending:
            raise UploadError("CHAT_RECOVERY_PENDING", 503)
        if (
            type(expected_revision) is not int
            or not 0 <= expected_revision < 2**63 - 1
            or not isinstance(references, list)
            or len(references) > 10
            or any(not isinstance(r, str) or not 1 <= len(r) <= 128 for r in references)
            or len(set(references)) != len(references)
        ):
            raise UploadError("INVALID_REQUEST")
        references = sorted(references)
        with self.store._write():
            current = self.selection(conversation)
            if current["revision"] != expected_revision:
                raise UploadError("SOURCE_CHANGED", 409)
            for reference in references:
                if not self.connection.execute(
                    "SELECT 1 FROM document_references WHERE id=? AND conversation_id=?",
                    (reference, conversation),
                ).fetchone():
                    raise UploadError("SOURCE_NOT_FOUND", 404)
            revision = expected_revision + int(references != current["references"])
            self.connection.execute(
                "INSERT INTO chat_selections VALUES (?,?,?) ON CONFLICT(conversation_id) DO UPDATE SET revision=excluded.revision,references_json=excluded.references_json",
                (conversation, revision, json.dumps(references)),
            )
        return {"revision": revision, "references": references}

    def admit(self, conversation: str, key: str, question: str, revision: int):
        """Claim one durable idempotent intent before retrieval/generation side effects."""
        try:
            valid = (
                isinstance(question, str)
                and question.strip()
                and len(question.encode()) <= 512
            )
        except UnicodeError:
            valid = False
        if (
            not valid
            or not isinstance(key, str)
            or not re.fullmatch(r"[A-Za-z0-9_-]{16,128}", key)
            or type(revision) is not int
            or not 0 <= revision < 2**63 - 1
        ):
            raise UploadError("INVALID_REQUEST")
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        fingerprint = hashlib.sha256(
            json.dumps([question, revision], ensure_ascii=False).encode()
        ).hexdigest()
        with self.store._write():
            previous = self.connection.execute(
                "SELECT *,0 AS admitted_new FROM chat_requests WHERE conversation_id=? AND key_hash=?",
                (conversation, key_hash),
            ).fetchone()
            if previous is not None:
                if previous["fingerprint"] != fingerprint:
                    raise UploadError("IDEMPOTENCY_CONFLICT", 409)
                return previous
            if (
                self.store.busy
                or self.store.recovery_pending
                or self.connection.execute(
                    "SELECT 1 FROM chat_requests WHERE state='processing'"
                ).fetchone()
            ):
                raise UploadError("CHAT_BUSY", 409)
            current = self.selection(conversation)
            if current["revision"] != revision:
                raise UploadError("SOURCE_CHANGED", 409)
            identity = str(uuid4())
            self.store.reserve_growth(
                len(question.encode()) + len(json.dumps(current).encode())
            )
            self.connection.execute(
                "INSERT INTO chat_requests VALUES (?,?,?,?,?,?,?,'processing',NULL,?)",
                (
                    identity,
                    conversation,
                    key_hash,
                    fingerprint,
                    question,
                    revision,
                    json.dumps(current["references"]),
                    datetime.now(UTC).isoformat(),
                ),
            )
        return self.connection.execute(
            "SELECT *,1 AS admitted_new FROM chat_requests WHERE id=?", (identity,)
        ).fetchone()

    def fail(self, identity: str, code: str) -> None:
        """Keep failed intent visible without saving partial unvalidated model text."""
        with self.store._write():
            self.connection.execute(
                "UPDATE chat_requests SET state='failed',error_code=? WHERE id=? AND state='processing'",
                (code, identity),
            )

    def finish(
        self,
        identity: str,
        answer: dict,
        snapshot: tuple[SourceVersion, ...],
        evidence: list[dict],
        warnings: list[str],
    ) -> None:
        """Atomically recheck scope/index versions and publish a complete exchange."""
        with self.store._write():
            request = self.connection.execute(
                "SELECT * FROM chat_requests WHERE id=?", (identity,)
            ).fetchone()
            current = self.selection(request["conversation_id"])
            if (
                request["state"] != "processing"
                or current["revision"] != request["selection_revision"]
                or current["references"] != json.loads(request["references_json"])
            ):
                raise UploadError("SOURCE_CHANGED", 409)
            for reference in current["references"]:
                if not self.connection.execute(
                    "SELECT 1 FROM document_references WHERE id=? AND conversation_id=?",
                    (reference, request["conversation_id"]),
                ).fetchone():
                    raise UploadError("SOURCE_CHANGED", 409)
            for version in snapshot:
                if version.reference_id not in current["references"]:
                    raise UploadError("SOURCE_CHANGED", 409)
                status = IndexState(self.store).status(
                    request["conversation_id"], version.reference_id
                )
                if (
                    status is None
                    or not status["indexed"]
                    or (status["extraction_id"], status["generation_id"])
                    != (version.extraction_id, version.generation_id)
                ):
                    raise UploadError("SOURCE_CHANGED", 409)
            allowed = {
                "evidence_id",
                "reference_id",
                "document_id",
                "content_hash",
                "extraction_id",
                "generation_id",
                "chunk_id",
                "text_hash",
                "filename",
                "locations",
                "warnings",
            }
            if any(set(item) - allowed for item in evidence):
                raise UploadError("CHAT_MANIFEST_INVALID", 503)
            values = [
                json.dumps(value, ensure_ascii=False)
                for value in (
                    answer,
                    [asdict(v) for v in snapshot],
                    evidence,
                    warnings,
                    {"model": CHAT_MODEL, "digest": CHAT_DIGEST},
                )
            ]
            self.store.reserve_growth(sum(len(v.encode()) for v in values))
            self.connection.execute(
                "INSERT INTO chat_exchanges VALUES (?,?,?,?,?,?,?)",
                (identity, *values, datetime.now(UTC).isoformat()),
            )
            self.connection.execute(
                "UPDATE chat_requests SET state='complete' WHERE id=?", (identity,)
            )

    def get(self, conversation: str, identity: str) -> dict:
        """Read only the requested conversation's saved historical exchange/status."""
        row = self.connection.execute(
            "SELECT r.*,e.answer,e.evidence_json,e.warnings_json,e.completed_at FROM chat_requests r LEFT JOIN chat_exchanges e ON e.request_id=r.id WHERE r.id=? AND r.conversation_id=?",
            (identity, conversation),
        ).fetchone()
        if row is None:
            raise UploadError("ANSWER_NOT_FOUND", 404)
        return {
            "operation_id": identity,
            "answer_id": identity if row["state"] == "complete" else None,
            "state": row["state"],
            "question": row["question"],
            "selection_revision": row["selection_revision"],
            "answer": json.loads(row["answer"]) if row["answer"] else None,
            "evidence": json.loads(row["evidence_json"])
            if row["evidence_json"]
            else [],
            "warnings": json.loads(row["warnings_json"])
            if row["warnings_json"]
            else [],
            "error_code": row["error_code"],
            "created_at": row["created_at"],
            "completed_at": row["completed_at"],
            "historical": True,
            "source_availability": "not_revalidated",
        }

    def history(
        self, conversation: str, current: tuple[SourceVersion, ...]
    ) -> tuple[tuple[str, str], ...]:
        """Only latest complete pairs with all provenance still in current evidence scope."""
        result = []
        rows = self.connection.execute(
            "SELECT r.question,e.answer,e.sources_json FROM chat_requests r JOIN chat_exchanges e ON e.request_id=r.id WHERE r.conversation_id=? AND r.state='complete' ORDER BY r.rowid DESC LIMIT 2",
            (conversation,),
        )
        for row in rows:
            sources = tuple(
                SourceVersion(**item) for item in json.loads(row["sources_json"])
            )
            answer = json.loads(row["answer"])
            if (
                sources
                and set(sources).issubset(set(current))
                and answer["status"] in {"answered", "partial"}
            ):
                result.append(
                    (row["question"], "\n".join(c["text"] for c in answer["claims"]))
                )
        return tuple(reversed(result))
