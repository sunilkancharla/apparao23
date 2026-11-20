"""Loopback HTTP bounds, ownership checks and private-error controls."""

import asyncio

import httpx
import pytest

from app.ollama import MAX_RESPONSE_BYTES, OllamaClient, OllamaError


def exchange(
    handler,
    *,
    owner=lambda: None,
    timeout=1,
    method="GET",
    path="/api/tags",
    payload=None,
):
    async def run():
        async with OllamaClient(
            11435,
            ownership_check=owner,
            timeout=timeout,
            transport=httpx.MockTransport(handler),
        ) as client:
            return await client.request(method, path, payload)

    return asyncio.run(run())


def test_unknown_owner_refuses_before_any_http_request():
    seen = []
    with pytest.raises(OllamaError, match="OWNERSHIP_UNVERIFIED"):
        exchange(lambda r: seen.append(r), owner=None)
    assert seen == []


def test_failed_or_lost_ownership_discards_response_and_sanitizes_error():
    calls = []

    def owner():
        calls.append(1)
        if len(calls) > 1:
            raise RuntimeError("private process path and document text")

    with pytest.raises(OllamaError, match="OWNERSHIP_UNVERIFIED") as failure:
        exchange(lambda r: httpx.Response(200, json={"models": []}), owner=owner)
    assert str(failure.value) == failure.value.code


@pytest.mark.parametrize(
    "status,code",
    [
        (301, "HTTP_ERROR"),
        (400, "INPUT_REJECTED"),
        (404, "MODEL_MISSING"),
        (500, "HTTP_ERROR"),
    ],
)
def test_status_errors_never_expose_bodies_or_follow_redirects(status, code):
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(
            status,
            headers={"Location": "https://example.invalid/private"},
            text="private source text",
        )

    with pytest.raises(OllamaError, match=code) as failure:
        exchange(handler)
    assert "private" not in str(failure.value) and len(seen) == 1


@pytest.mark.parametrize(
    "body,headers",
    [
        (b'{"models":[],"models":[]}', {"Content-Type": "application/json"}),
        (b'{"value":NaN}', {"Content-Type": "application/json"}),
        (b"[]", {"Content-Type": "application/json"}),
        (b'{"error":"private"}', {"Content-Type": "application/json"}),
        (b'{"models":[]}', {"Content-Type": "text/html"}),
        (
            b'{"models":[]}',
            {"Content-Type": "application/json", "Content-Encoding": "unexpected"},
        ),
        (b"\xff", {"Content-Type": "application/json"}),
    ],
)
def test_invalid_json_media_or_compression_is_refused(body, headers):
    with pytest.raises(OllamaError, match="RESPONSE_INVALID"):
        exchange(lambda r: httpx.Response(200, content=body, headers=headers))


class Blocks(httpx.AsyncByteStream):
    async def __aiter__(self):
        for _ in range(MAX_RESPONSE_BYTES // 8192 + 1):
            yield b" " * 8192


def test_observed_response_cap_covers_chunked_bodies_without_content_length():
    with pytest.raises(OllamaError, match="RESPONSE_TOO_LARGE"):
        exchange(
            lambda r: httpx.Response(
                200, stream=Blocks(), headers={"Content-Type": "application/json"}
            )
        )


def test_declared_large_response_is_refused_before_parsing():
    with pytest.raises(OllamaError, match="RESPONSE_TOO_LARGE"):
        exchange(
            lambda r: httpx.Response(
                200,
                content=b"{}",
                headers={
                    "Content-Type": "application/json",
                    "Content-Length": str(MAX_RESPONSE_BYTES + 1),
                },
            )
        )


def test_timeout_and_absent_service_are_sanitized():
    async def slow(request):
        await asyncio.sleep(0.1)
        return httpx.Response(200, json={})

    with pytest.raises(OllamaError, match="TIMEOUT"):
        exchange(slow, timeout=0.01)

    def absent(request):
        raise httpx.ConnectError("private URL", request=request)

    with pytest.raises(OllamaError, match="UNAVAILABLE"):
        exchange(absent)


@pytest.mark.parametrize(
    "method,path,payload",
    [
        ("GET", "https://example.invalid/", None),
        ("GET", "//example.invalid/", None),
        ("POST", "/api/pull", {}),
        ("GET", "/api/tags", {"private": "value"}),
        ("POST", "/api/embed", {"input": "x" * 70_000}),
    ],
)
def test_unapproved_routes_or_oversized_requests_never_reach_transport(
    method, path, payload
):
    seen = []
    with pytest.raises(OllamaError):
        exchange(lambda r: seen.append(r), method=method, path=path, payload=payload)
    assert not seen


@pytest.mark.parametrize(
    "values",
    [
        {"port": "11435"},
        {"port": True},
        {"port": 0},
        {"timeout": float("nan")},
        {"timeout": 91},
        {"timeout": 0},
    ],
)
def test_invalid_local_configuration_is_refused(values):
    with pytest.raises(OllamaError, match="CONFIG_INVALID"):
        OllamaClient(**({"port": 11435} | values))
