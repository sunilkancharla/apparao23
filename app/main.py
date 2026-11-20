"""Loopback diagnostics API and the supported local launcher."""

import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Literal

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response

from app.api.sources import router as source_router
from app.config import ConfigurationError, Settings, prepare_data_root
from app.diagnostics import ComponentState, inspect_prerequisites, reserve_port


class HealthReport(BaseModel):
    """Startup snapshot; readiness remains false until owned model integration."""

    ready: Literal[False] = False
    components: list[ComponentState]


def _error(code: str, message: str, status: int) -> JSONResponse:
    return JSONResponse(
        {
            "error": {
                "code": code,
                "message": message,
                "retryable": False,
                "request_id": str(uuid4()),
            }
        },
        status_code=status,
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create the loopback diagnostics and single-CSV upload application."""
    config = Settings.from_env() if settings is None else settings

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        application.state.upload_store = None
        try:
            prepare_data_root(config.data_root)
            root = ComponentState(
                component="data_root",
                code="DATA_ROOT_WRITABLE",
                message="Managed directory is writable.",
            )
        except ConfigurationError as error:
            root = ComponentState(
                component="data_root",
                code="DATA_ROOT_UNAVAILABLE",
                message=str(error),
            )
        application.state.health = HealthReport(
            components=[root, *inspect_prerequisites(config)]
        )
        try:
            yield
        finally:
            if application.state.upload_store is not None:
                application.state.upload_store.close()

    application = FastAPI(
        lifespan=lifespan,
        openapi_url=None,
        docs_url=None,
        redoc_url=None,
    )
    csrf_token = secrets.token_urlsafe(32)

    @application.middleware("http")
    async def local_boundary(
        request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        hosts = request.headers.getlist("host")
        origins = request.headers.getlist("origin")
        tokens = request.headers.getlist("x-csrf-token")
        mutation_allowed = (
            request.method == "POST"
            and origins == [config.origin]
            and len(tokens) == 1
            and tokens[0].isascii()
            and secrets.compare_digest(tokens[0], csrf_token)
        )
        if (
            hosts != [config.origin.removeprefix("http://")]
            or (origins and origins != [config.origin])
            or (request.method not in {"GET", "HEAD"} and not mutation_allowed)
        ):
            response = _error(
                "REQUEST_DENIED", "Local request policy denied access.", 403
            )
        else:
            try:
                response = await call_next(request)
            except Exception:  # noqa: BLE001 - final HTTP privacy boundary
                # Never pass exception text, private values or tracebacks to HTTP/logs.
                response = _error("INTERNAL_ERROR", "Local request failed.", 500)
        response.headers.update(
            {
                "Cache-Control": "no-store",
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY",
                "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
                "Referrer-Policy": "no-referrer",
            }
        )
        return response

    @application.exception_handler(HTTPException)
    async def http_error(request: Request, error: HTTPException) -> JSONResponse:
        return _error(
            "HTTP_ERROR", "Requested route or method is unavailable.", error.status_code
        )

    @application.exception_handler(UploadError)
    async def operation_error(request: Request, error: UploadError) -> JSONResponse:
        messages = {
            "EMPTY_CSV": "The CSV contains no nonblank data records.",
            "EXTRACTION_REQUIRED": "Extract this source before requesting a preview.",
            "SOURCE_NOT_FOUND": "This source is not attached to the requested conversation.",
            "SOURCE_UNAVAILABLE": "The stored source is missing or has changed.",
            "PROCESSED_QUOTA": "This operation cannot reserve enough processed-data space.",
        }
        return _error(
            error.code,
            messages.get(
                error.code,
                "Operation could not complete; check the request, file count and storage state.",
            ),
            error.status,
        )

    @application.get("/api/operations/{identity}")
    async def operation_status(identity: str, request: Request) -> dict:
        """Return a bounded status snapshot within the supplied conversation scope."""
        scopes = request.query_params.getlist("conversation_id")
        if len(scopes) != 1 or set(request.query_params) != {"conversation_id"}:
            raise UploadError("INVALID_REQUEST")
        store = request.app.state.upload_store
        if store is None:
            raise UploadError("STORAGE_UNAVAILABLE", 503)
        return {
            "data": UploadOperations(store).status(_uuid(scopes[0]), _uuid(identity))
        }

    @application.post("/api/conversations/{conversation}/attachment-batches")
    async def batch(conversation: str, request: Request) -> JSONResponse:
        """Accept a bounded JSON filename manifest; bodies stream separately."""
        _uuid(conversation)
        keys = request.headers.getlist("idempotency-key")
        if len(keys) != 1 or not re.fullmatch(r"[A-Za-z0-9_-]{16,128}", keys[0]):
            raise UploadError("INVALID_REQUEST")
        types = request.headers.getlist("content-type")
        if (
            len(types) != 1
            or not re.fullmatch(
                r'application/json(?:\s*;\s*charset="?utf-8"?)?', types[0].lower()
            )
            or request.headers.getlist("content-encoding")
        ):
            raise UploadError("UNSUPPORTED_FORMAT", 415)
        lengths = request.headers.getlist("content-length")
        if len(lengths) > 1 or (
            lengths and not re.fullmatch(r"[0-9]{1,18}", lengths[0])
        ):
            raise UploadError("INVALID_REQUEST", 400)
        declared = int(lengths[0]) if lengths else None
        if declared is not None and declared > 32_768:
            raise UploadError("BATCH_METADATA_LIMIT", 413)
        body = bytearray()
        async for chunk in request.stream():
            if len(body) + len(chunk) > 32_768:
                raise UploadError("BATCH_METADATA_LIMIT", 413)
            body.extend(chunk)
        if declared is not None and len(body) != declared:
            raise UploadError("CONTENT_LENGTH_MISMATCH", 400)

        def unique_object(pairs: list[tuple]) -> dict:
            result = dict(pairs)
            if len(result) != len(pairs):
                raise ValueError
            return result

        try:
            payload = json.loads(body.decode("utf-8"), object_pairs_hook=unique_object)
        except (ValueError, RecursionError):
            raise UploadError("INVALID_REQUEST", 400) from None
        if (
            not isinstance(payload, dict)
            or set(payload) != {"files"}
            or not isinstance(payload["files"], list)
            or any(not isinstance(name, str) for name in payload["files"])
        ):
            raise UploadError("INVALID_REQUEST")
        store = request.app.state.upload_store
        if store is None:
            raise UploadError("STORAGE_UNAVAILABLE", 503)
        return JSONResponse(
            {
                "data": UploadOperations(store).create_batch(
                    conversation, keys[0], payload["files"]
                )
            },
            status_code=202,
        )

    @application.get("/api/health", response_model=HealthReport)
    def health(request: Request) -> JSONResponse:
        """Return safe startup diagnostics, never asset paths or private text."""
        return JSONResponse(request.app.state.health.model_dump(), status_code=503)

    return application


def main() -> int:
    """Reserve the exact loopback port and run without request/access logging."""
    try:
        settings = Settings.from_env()
        listener = reserve_port(settings.port)
    except ConfigurationError as error:
        print(str(error), file=sys.stderr)
        return 2
    except OSError:
        print(
            "APP_PORT_UNAVAILABLE: free the configured local port; no service was attached.",
            file=sys.stderr,
        )
        return 2
    with listener:
        server = uvicorn.Server(
            uvicorn.Config(
                create_app(settings),
                host="127.0.0.1",
                port=settings.port,
                access_log=False,
                log_config=None,
                proxy_headers=False,
                server_header=False,
            )
        )
        server.run(sockets=[listener])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
