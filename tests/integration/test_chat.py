"""Grounded service and local HTTP behavior with injected inference only."""

import asyncio
import json
from contextlib import asynccontextmanager

import pytest

from app.chat.generation import Answer, Claim
from app.chat.service import ChatService
from app.ingestion.validation import UploadError
from app.storage.messages import Messages
from tests.integration import test_retrieval_scope

retrieval = test_retrieval_scope.retrieval


def configured(retrieval, *, during=None):
    store, _, retriever, session, _ = retrieval
    record = {"calls": 0, "prompts": []}

    class Model:
        async def generate(self, prompt):
            record["calls"] += 1
            record["prompts"].append(prompt)
            if during:
                during()
            return Answer(
                status="answered",
                claims=(
                    Claim(
                        text="North has 42 units.",
                        citations=(prompt.evidence[0].evidence_id,),
                    ),
                ),
            )

    @asynccontextmanager
    async def chat_session():
        assert not store.busy
        store.busy = True
        try:
            yield Model()
        finally:
            store.busy = False

    return ChatService(
        store, retriever=retriever, retrieval_session=session, chat_session=chat_session
    ), record


def test_grounded_exchange_is_saved_and_replay_does_not_infer(retrieval):
    store, add, _, _, _ = retrieval
    conversation, reference = asyncio.run(add())
    Messages(store).select(conversation, [reference], 0)
    service, record = configured(retrieval)
    result = asyncio.run(
        service.ask(conversation, "answer-request-01", "North units?", 1)
    )
    assert result["state"] == "complete" and result["answer"]["status"] == "answered"
    assert record["calls"] == 1 and result["evidence"]
    assert all("text" not in e and "rendered" not in e for e in result["evidence"])
    assert (
        asyncio.run(service.ask(conversation, "answer-request-01", "North units?", 1))
        == result
    )
    assert record["calls"] == 1


def test_selection_change_during_generation_rejects_publication(retrieval):
    store, add, _, _, _ = retrieval
    conversation, reference = asyncio.run(add())
    Messages(store).select(conversation, [reference], 0)
    service, _ = configured(
        retrieval, during=lambda: Messages(store).select(conversation, [], 1)
    )
    with pytest.raises(UploadError, match="SOURCE_CHANGED"):
        asyncio.run(service.ask(conversation, "answer-request-01", "North?", 1))
    assert (
        store.connection.execute("SELECT count(*) FROM chat_exchanges").fetchone()[0]
        == 0
    )
    assert (
        store.connection.execute("SELECT state FROM chat_requests").fetchone()[0]
        == "failed"
    )
    assert not store.busy


def test_unselected_history_is_not_sent_to_model(retrieval):
    store, add, _, _, _ = retrieval
    conversation, first = asyncio.run(add())
    _, second = asyncio.run(add(b"Name,Units\nSouth,70\n", conversation=conversation))
    Messages(store).select(conversation, [first], 0)
    service, record = configured(retrieval)
    asyncio.run(service.ask(conversation, "answer-request-01", "North units?", 1))
    Messages(store).select(conversation, [second], 1)
    asyncio.run(service.ask(conversation, "answer-request-02", "South units?", 2))
    data = json.loads(record["prompts"][-1].payload["messages"][1]["content"])
    assert data["history"] == []


def test_empty_selection_persists_refusal_without_model(retrieval):
    store, add, _, _, _ = retrieval
    conversation, _ = asyncio.run(add())
    result = asyncio.run(
        ChatService(store).ask(conversation, "answer-request-01", "North units?", 0)
    )
    assert (
        result["answer"]["status"] == "insufficient_evidence"
        and result["evidence"] == []
    )
    assert "NO_EVIDENCE" in result["warnings"]


@pytest.mark.parametrize("failure", ["cancel", "malformed"])
def test_failures_do_not_save_assistant_text(retrieval, failure):
    store, add, _, _, _ = retrieval
    conversation, reference = asyncio.run(add())
    Messages(store).select(conversation, [reference], 0)

    def fail():
        if failure == "cancel":
            raise asyncio.CancelledError
        from app.ollama import OllamaError

        raise OllamaError("CHAT_RESPONSE_INVALID")

    service, _ = configured(retrieval, during=fail)
    with pytest.raises(asyncio.CancelledError if failure == "cancel" else UploadError):
        asyncio.run(service.ask(conversation, "answer-request-01", "North?", 1))
    assert (
        store.connection.execute("SELECT count(*) FROM chat_exchanges").fetchone()[0]
        == 0
    )
    assert not store.busy


def test_publication_quota_failure_keeps_intent_and_saves_no_answer(
    retrieval, monkeypatch
):
    store, add, _, _, _ = retrieval
    conversation, reference = asyncio.run(add())
    Messages(store).select(conversation, [reference], 0)
    service, _ = configured(retrieval)
    reserve = store.reserve_growth

    def limited(size=0):
        if size > 1000:
            raise UploadError("PROCESSED_QUOTA", 507)
        reserve(size)

    monkeypatch.setattr(store, "reserve_growth", limited)
    with pytest.raises(UploadError, match="PROCESSED_QUOTA"):
        asyncio.run(service.ask(conversation, "answer-request-01", "North?", 1))
    assert (
        store.connection.execute("SELECT count(*) FROM chat_exchanges").fetchone()[0]
        == 0
    )


def test_changed_original_after_generation_prevents_answer(retrieval):
    store, add, _, _, _ = retrieval
    conversation, reference = asyncio.run(add())
    Messages(store).select(conversation, [reference], 0)
    service, _ = configured(
        retrieval,
        during=lambda: next((store.root / "originals").iterdir()).write_bytes(
            b"changed"
        ),
    )
    with pytest.raises(UploadError, match="SOURCE_CHANGED"):
        asyncio.run(service.ask(conversation, "answer-request-01", "North?", 1))
    assert (
        store.connection.execute("SELECT count(*) FROM chat_exchanges").fetchone()[0]
        == 0
    )


@pytest.fixture
def api(tmp_path):
    from dataclasses import replace

    from fastapi.testclient import TestClient

    from app.config import Settings
    from app.main import create_app
    from app.storage.database import open_database
    from app.storage.documents import Documents

    settings = replace(
        Settings.from_env({}),
        data_root=tmp_path / "app",
        model_root=tmp_path / "models",
    )
    connection = open_database(settings.data_root)
    first, second = (
        Documents(connection).create_conversation(),
        Documents(connection).create_conversation(),
    )
    connection.close()
    with TestClient(create_app(settings), base_url=settings.origin) as client:
        client.headers.update(
            {
                "Origin": settings.origin,
                "X-CSRF-Token": client.get("/api/session").json()["data"]["csrf_token"],
            }
        )
        yield client, first, second


def test_http_empty_answer_selection_and_scoped_read(api):
    client, first, other = api
    selected = client.put(
        f"/api/conversations/{first}/selection",
        json={"references": [], "expected_revision": 0},
    )
    assert selected.status_code == 200
    response = client.post(
        f"/api/conversations/{first}/answers",
        json={"question": "North?", "expected_revision": 0},
        headers={"Idempotency-Key": "answer-request-01"},
    )
    assert response.status_code == 202
    data = response.json()["data"]
    assert data["answer"]["status"] == "insufficient_evidence"
    assert (
        client.get(
            f"/api/conversations/{first}/answers/{data['answer_id']}"
        ).status_code
        == 200
    )
    assert (
        client.get(
            f"/api/conversations/{other}/answers/{data['answer_id']}"
        ).status_code
        == 404
    )
    assert response.headers["cache-control"] == "no-store"


@pytest.mark.parametrize(
    "body",
    [
        {"question": "x" * 513, "expected_revision": 0},
        {"question": "x", "expected_revision": True},
        {"question": "x", "expected_revision": 0, "history": "hidden"},
    ],
)
def test_http_rejects_oversize_or_untrusted_fields(api, body):
    client, first, _ = api
    response = client.post(
        f"/api/conversations/{first}/answers",
        json=body,
        headers={"Idempotency-Key": "answer-request-01"},
    )
    assert response.status_code == 422


def test_selection_requires_same_origin_csrf(api):
    client, first, _ = api
    client.headers.pop("X-CSRF-Token")
    response = client.put(
        f"/api/conversations/{first}/selection",
        json={"references": [], "expected_revision": 0},
    )
    assert response.status_code == 403


def test_unselected_retriever_output_cannot_reach_generation(retrieval):
    store, add, actual, session, _ = retrieval
    conversation, first = asyncio.run(add())
    _, second = asyncio.run(add(b"Name,Units\nNorth,999\n", conversation=conversation))
    Messages(store).select(conversation, [first], 0)
    bad = asyncio.run(
        actual.retrieve(conversation, [second], "North?", session_factory=session)
    )
    service, record = configured(retrieval)

    class WrongScope:
        async def retrieve(self, *args, **kwargs):
            return bad

        async def _recheck(self, *args):
            return None

    service.retriever = WrongScope()
    with pytest.raises(UploadError, match="CHAT_EVIDENCE_INVALID"):
        asyncio.run(service.ask(conversation, "answer-request-01", "North?", 1))
    assert record["calls"] == 0
