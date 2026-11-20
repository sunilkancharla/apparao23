"""Bounded loopback HTTP seam; runtime ownership must be supplied by its owner."""

import asyncio
import json
import math
from collections.abc import Callable
from typing import Literal, Self

import httpx

MAX_REQUEST_BYTES = 65_536
MAX_RESPONSE_BYTES = 262_144
_ROUTES = {("GET", "/api/version"), ("GET", "/api/tags"), ("POST", "/api/embed")}


class OllamaError(RuntimeError):
    """Content-free error; never retain an upstream body, URL or source text."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def _object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise ValueError("Non-JSON number")


class OllamaClient:
    """Own an HTTP client, never an Ollama process or model download.

    The trusted caller's fast ownership_check must raise unless its pinned local
    process/model store and heavy-job lease remain owned. It is checked before
    and after each exchange. No check is supplied by default, so access fails
    closed. This seam is not a process-ownership implementation or confinement.
    """

    def __init__(
        self,
        port: int,
        *,
        ownership_check: Callable[[], None] | None = None,
        timeout: float = 90,
        transport: httpx.AsyncBaseTransport | None = None,
        purpose: Literal["embedding", "chat"] = "embedding",
    ) -> None:
        if type(port) is not int or not 1 <= port <= 65535:
            raise OllamaError("OLLAMA_CONFIG_INVALID")
        if (
            type(timeout) not in (float, int)
            or not math.isfinite(timeout)
            or not 0 < timeout <= 90
        ):
            raise OllamaError("OLLAMA_CONFIG_INVALID")
        if purpose not in {"embedding", "chat"}:
            raise OllamaError("OLLAMA_CONFIG_INVALID")
        self._routes = (
            _ROUTES
            if purpose == "embedding"
            else {("GET", "/api/version"), ("GET", "/api/tags"), ("POST", "/api/chat")}
        )
        self.timeout = float(timeout)
        self._ownership_check = ownership_check
        self._client = httpx.AsyncClient(
            base_url=f"http://127.0.0.1:{port}",
            trust_env=False,
            follow_redirects=False,
            transport=transport,
            timeout=httpx.Timeout(self.timeout, connect=min(5, self.timeout)),
            limits=httpx.Limits(max_connections=1, max_keepalive_connections=1),
            headers={"Accept": "application/json", "Accept-Encoding": "identity"},
        )

    async def __aenter__(self) -> Self:
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args) -> None:
        await self._client.__aexit__(*args)

    def _check_owner(self) -> None:
        try:
            if self._ownership_check is None or self._ownership_check() is not None:
                raise ValueError
        except (OSError, ValueError, RuntimeError):
            raise OllamaError("OLLAMA_OWNERSHIP_UNVERIFIED") from None

    async def request(
        self, method: str, path: str, payload: dict | None = None
    ) -> dict:
        """Exchange only approved routes with bounded JSON and safe failures.

        The wall deadline bounds cooperative HTTP I/O, not native computation
        after cancellation. The owning controller must stop abandoned work.
        """
        if (method, path) not in self._routes or (
            method == "GET" and payload is not None
        ):
            raise OllamaError("OLLAMA_REQUEST_INVALID")
        try:
            content = (
                None
                if payload is None
                else json.dumps(payload, ensure_ascii=False, allow_nan=False).encode(
                    "utf-8"
                )
            )
        except (TypeError, ValueError, UnicodeError, RecursionError):
            raise OllamaError("OLLAMA_REQUEST_INVALID") from None
        if content is not None and len(content) > MAX_REQUEST_BYTES:
            raise OllamaError("OLLAMA_REQUEST_TOO_LARGE")
        self._check_owner()
        try:
            async with (
                asyncio.timeout(self.timeout),
                self._client.stream(
                    method,
                    path,
                    content=content,
                    headers={"Content-Type": "application/json"}
                    if content is not None
                    else None,
                ) as response,
            ):
                if response.status_code == 404:
                    raise OllamaError("MODEL_MISSING")
                if response.status_code == 400:
                    raise OllamaError("EMBEDDING_INPUT_REJECTED")
                if response.status_code != 200:
                    raise OllamaError("OLLAMA_HTTP_ERROR")
                media = (
                    response.headers.get("content-type", "")
                    .split(";")[0]
                    .strip()
                    .lower()
                )
                encoding = (
                    response.headers.get("content-encoding", "identity").strip().lower()
                )
                if media != "application/json" or encoding != "identity":
                    raise OllamaError("OLLAMA_RESPONSE_INVALID")
                length = response.headers.get("content-length")
                if length is not None:
                    try:
                        observed_length = int(length)
                    except ValueError:
                        raise OllamaError("OLLAMA_RESPONSE_INVALID") from None
                    if observed_length < 0:
                        raise OllamaError("OLLAMA_RESPONSE_INVALID")
                    if observed_length > MAX_RESPONSE_BYTES:
                        raise OllamaError("OLLAMA_RESPONSE_TOO_LARGE")
                retained = bytearray()
                async for block in response.aiter_bytes(chunk_size=8192):
                    if len(retained) + len(block) > MAX_RESPONSE_BYTES:
                        raise OllamaError("OLLAMA_RESPONSE_TOO_LARGE")
                    retained.extend(block)
                self._check_owner()
                result = json.loads(
                    retained.decode("utf-8"),
                    object_pairs_hook=_object,
                    parse_constant=_invalid_constant,
                )
                if not isinstance(result, dict) or "error" in result:
                    raise OllamaError("OLLAMA_RESPONSE_INVALID")
                return result
        except (TimeoutError, httpx.TimeoutException):
            raise OllamaError("OLLAMA_TIMEOUT") from None
        except httpx.ConnectError:
            raise OllamaError("OLLAMA_UNAVAILABLE") from None
        except httpx.HTTPError:
            raise OllamaError("OLLAMA_TRANSPORT_ERROR") from None
        except (ValueError, UnicodeError, RecursionError):
            raise OllamaError("OLLAMA_RESPONSE_INVALID") from None
