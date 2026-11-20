"""Synthetic Ollama embeddings preserve identities and refuse unsafe responses."""

import asyncio
import json
import math

import httpx
import pytest

from app.ollama import OllamaClient
from app.retrieval.chunking import iter_chunks
from app.retrieval.embeddings import (
    DIMENSIONS,
    MODEL_DIGEST,
    MODEL_NAME,
    Embedder,
    EmbeddingError,
)
from tests.unit.test_chunking import prose


def responder(request):
    if request.url.path == "/api/version":
        return httpx.Response(200, json={"version": "0.40.16"})
    if request.url.path == "/api/tags":
        return httpx.Response(
            200, json={"models": [{"name": MODEL_NAME, "digest": MODEL_DIGEST}]}
        )
    body = json.loads(request.content)
    return httpx.Response(
        200,
        json={
            "model": MODEL_NAME,
            "embeddings": [
                [3.0, 4.0] + [0.0] * (DIMENSIONS - 2) for _ in body["input"]
            ],
            "prompt_eval_count": 12,
        },
    )


async def embed(handler=responder, chunks=None):
    async with OllamaClient(
        11435, ownership_check=lambda: None, transport=httpx.MockTransport(handler)
    ) as client:
        return await Embedder(client).documents(
            chunks or [next(iter_chunks(prose("Budget is 42.")))]
        )


def test_documents_use_pinned_identity_and_return_normalized_traceable_vectors():
    seen = []

    def respond(request):
        seen.append(request)
        return responder(request)

    chunk = next(iter_chunks(prose("Budget is 42.")))
    result = asyncio.run(embed(respond, [chunk]))
    assert result.model == MODEL_NAME and result.model_digest == MODEL_DIGEST
    assert result.dimensions == 768 and result.kind == "document"
    assert len(result.embeddings) == 1
    vector = result.embeddings[0]
    assert vector.source_id == chunk.chunk_id and vector.text_hash == chunk.text_hash
    assert vector.vector[:2] == (0.6, 0.8) and math.hypot(*vector.vector) == 1.0
    payload = json.loads(next(r.content for r in seen if r.url.path == "/api/embed"))
    assert payload["model"] == MODEL_NAME
    assert payload["input"] == ["search_document: " + chunk.text]
    assert payload["truncate"] is False
    assert payload["options"] == {
        "num_ctx": 2048,
        "num_gpu": 0,
        "num_thread": 4,
        "num_batch": 64,
    }
    assert all(str(r.url).startswith("http://127.0.0.1:11435/") for r in seen)


def test_query_uses_distinct_prefix_and_same_embedding_space():
    seen = []

    def respond(request):
        if request.url.path == "/api/embed":
            seen.append(json.loads(request.content)["input"])
        return responder(request)

    async def run():
        async with OllamaClient(
            11435, ownership_check=lambda: None, transport=httpx.MockTransport(respond)
        ) as client:
            service = Embedder(client)
            a = await service.documents([next(iter_chunks(prose("Budget is 42.")))])
            b = await service.query("What is the budget?", "query-1")
            return a, b

    documents, query = asyncio.run(run())
    assert query.space_id == documents.space_id and query.kind == "query"
    assert seen[-1] == ["search_query: What is the budget?"]


@pytest.mark.parametrize(
    "vector",
    [
        [1.0] * 767,
        [0.0] * 768,
        [True] * 768,
        ["1"] * 768,
        [float("nan")] * 768,
        [float("inf")] * 768,
    ],
)
def test_invalid_vectors_are_refused_without_partial_results(vector):
    def respond(request):
        if request.url.path == "/api/embed":
            return httpx.Response(
                200,
                content=json.dumps({"model": MODEL_NAME, "embeddings": [vector]}),
                headers={"Content-Type": "application/json"},
            )
        return responder(request)

    with pytest.raises(EmbeddingError):
        asyncio.run(embed(respond))


@pytest.mark.parametrize(
    "response,code",
    [
        ({"model": MODEL_NAME, "embeddings": []}, "RESPONSE_INVALID"),
        (
            {"model": "different", "embeddings": [[1.0] * DIMENSIONS]},
            "RESPONSE_INVALID",
        ),
        (
            {
                "model": MODEL_NAME,
                "embeddings": [[1.0] * DIMENSIONS],
                "truncated": True,
            },
            "TRUNCATED",
        ),
        (
            {"model": MODEL_NAME, "embeddings": [[10**400] + [0.0] * (DIMENSIONS - 1)]},
            "VECTOR_INVALID",
        ),
        (
            {
                "model": MODEL_NAME,
                "embeddings": [[1.0] * DIMENSIONS],
                "prompt_eval_count": True,
            },
            "RESPONSE_INVALID",
        ),
    ],
)
def test_malformed_or_truncated_embedding_results_fail_safely(response, code):
    def respond(request):
        if request.url.path == "/api/embed":
            return httpx.Response(
                200,
                content=json.dumps(response),
                headers={"Content-Type": "application/json"},
            )
        return responder(request)

    with pytest.raises(EmbeddingError, match=code):
        asyncio.run(embed(respond))


@pytest.mark.parametrize(
    "which,code",
    [
        ("missing", "MODEL_MISSING"),
        ("digest", "MODEL_MISMATCH"),
        ("version", "VERSION_MISMATCH"),
    ],
)
def test_wrong_runtime_or_model_refuses_before_source_text_is_sent(which, code):
    seen = []

    def respond(request):
        seen.append(request.url.path)
        if which == "version" and request.url.path == "/api/version":
            return httpx.Response(200, json={"version": "other"})
        if request.url.path == "/api/tags":
            models = (
                [] if which == "missing" else [{"name": MODEL_NAME, "digest": "b" * 64}]
            )
            return httpx.Response(200, json={"models": models})
        return responder(request)

    with pytest.raises(EmbeddingError, match=code):
        asyncio.run(embed(respond))
    assert "/api/embed" not in seen


def test_model_change_after_inference_discards_all_vectors():
    calls = []

    def respond(request):
        if request.url.path == "/api/tags":
            calls.append(1)
            if len(calls) > 1:
                return httpx.Response(200, json={"models": []})
        return responder(request)

    with pytest.raises(EmbeddingError, match="MODEL_MISSING"):
        asyncio.run(embed(respond))


@pytest.mark.parametrize("text", ["", "  ", "界" * 171, "\ud800"])
def test_invalid_query_never_reaches_transport(text):
    seen = []

    async def run():
        async with OllamaClient(
            11435,
            ownership_check=lambda: None,
            transport=httpx.MockTransport(lambda r: seen.append(r)),
        ) as client:
            await Embedder(client).query(text, "query-1")

    with pytest.raises(EmbeddingError, match="INPUT_INVALID"):
        asyncio.run(run())
    assert not seen


def test_busy_request_is_refused_and_cancellation_releases_client_slot():
    async def run():
        entered = asyncio.Event()
        release = asyncio.Event()

        async def respond(request):
            if request.url.path == "/api/embed":
                entered.set()
                await release.wait()
            return responder(request)

        async with OllamaClient(
            11435, ownership_check=lambda: None, transport=httpx.MockTransport(respond)
        ) as client:
            service = Embedder(client)
            active = asyncio.create_task(service.query("Question", "query-1"))
            await asyncio.wait_for(entered.wait(), 1)
            with pytest.raises(EmbeddingError, match="BUSY"):
                await service.query("Question", "query-2")
            active.cancel()
            with pytest.raises(asyncio.CancelledError):
                await active
            release.set()
            return await service.query("Question", "query-3")

    assert asyncio.run(run()).embeddings[0].source_id == "query-3"


def test_one_deadline_covers_identity_checks_and_inference_together():
    async def respond(request):
        await asyncio.sleep(0.025)
        return responder(request)

    async def run():
        async with OllamaClient(
            11435,
            ownership_check=lambda: None,
            timeout=0.06,
            transport=httpx.MockTransport(respond),
        ) as client:
            await Embedder(client).query("Question", "query-1")

    with pytest.raises(EmbeddingError, match="TIMEOUT"):
        asyncio.run(run())


@pytest.mark.parametrize("size", [1e308, 5e-324])
def test_extreme_finite_vectors_are_normalized_without_overflow_or_underflow(size):
    def respond(request):
        if request.url.path == "/api/embed":
            return httpx.Response(
                200, json={"model": MODEL_NAME, "embeddings": [[size] * DIMENSIONS]}
            )
        return responder(request)

    result = asyncio.run(embed(respond))
    assert math.isclose(math.hypot(*result.embeddings[0].vector), 1.0, abs_tol=1e-14)


def test_invalid_batch_sizes_duplicate_chunks_and_omissions_never_send_text():
    seen = []
    chunk = next(iter_chunks(prose("Budget is 42.")))

    async def run():
        async with OllamaClient(
            11435,
            ownership_check=lambda: None,
            transport=httpx.MockTransport(lambda r: seen.append(r)),
        ) as client:
            service = Embedder(client)
            for chunks in ([], [chunk] * 9, [chunk, chunk], [object()]):
                with pytest.raises(EmbeddingError, match="INPUT_INVALID"):
                    await service.documents(chunks)

    asyncio.run(run())
    assert not seen


def test_a_bad_vector_in_a_later_batch_position_returns_no_partial_batch():
    seen = []
    chunks = [
        next(iter_chunks(prose("Budget is 42."))),
        next(iter_chunks(prose("Budget is 43."))),
    ]

    def respond(request):
        if request.url.path == "/api/embed":
            seen.append(request)
            return httpx.Response(
                200,
                json={
                    "model": MODEL_NAME,
                    "embeddings": [[1.0] * DIMENSIONS, [0.0] * DIMENSIONS],
                },
            )
        return responder(request)

    with pytest.raises(EmbeddingError, match="VECTOR_INVALID"):
        asyncio.run(embed(respond, chunks))
    assert len(seen) == 1
