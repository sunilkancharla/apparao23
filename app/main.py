"""Loopback diagnostics API and the supported local launcher."""

import re
import secrets
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Literal
from urllib.parse import unquote
from uuid import UUID, uuid4

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response

from app.config import ConfigurationError, Settings, prepare_data_root
from app.diagnostics import ComponentState, inspect_prerequisites, reserve_port
from app.ingestion.validation import MAX_FILE_BYTES, UploadError, validate_filename
from app.storage.files import UploadStore


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
            try:
                application.state.upload_store = UploadStore(config.data_root)
            except UploadError:
                root = ComponentState(
                    component="data_root",
                    code="STORAGE_UNAVAILABLE",
                    message="Managed storage needs attention before uploads.",
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

    @application.get("/api/health", response_model=HealthReport)
    def health(request: Request) -> JSONResponse:
        """Return safe startup diagnostics, never asset paths or private text."""
        return JSONResponse(request.app.state.health.model_dump(), status_code=503)

    @application.get("/api/session")
    def session() -> dict:
        """Convey the ephemeral CSRF value to same-origin clients; never persist it."""
        return {"data": {"csrf_token": csrf_token}}

    @application.post("/api/conversations/{conversation}/attachments")
    async def attachment(conversation: str, request: Request) -> JSONResponse:
        """Accept a raw CSV body; validate metadata before consuming any bytes."""
        try:
            try:
                if str(UUID(conversation)) != conversation:
                    raise ValueError
            except ValueError:
                raise UploadError("INVALID_REQUEST") from None
            metadata = {}
            for key in ("x-filename", "idempotency-key", "content-type"):
                values = request.headers.getlist(key)
                if len(values) != 1:
                    raise UploadError("INVALID_REQUEST")
                metadata[key] = values[0]
            key = metadata["idempotency-key"]
            if not re.fullmatch(r"[A-Za-z0-9_-]{16,128}", key):
                raise UploadError("INVALID_REQUEST")
            raw_name = metadata["x-filename"]
            if re.search(r"%(?![a-fA-F0-9]{2})", raw_name):
                raise UploadError("INVALID_FILENAME")
            try:
                name = validate_filename(unquote(raw_name, errors="strict"))
            except UnicodeError:
                raise UploadError("INVALID_FILENAME") from None
            if not re.fullmatch(
                r'(?:text/csv|application/octet-stream)(?:\s*;\s*charset="?utf-8"?)?',
                metadata["content-type"].lower(),
            ) or request.headers.getlist("content-encoding"):
                raise UploadError("UNSUPPORTED_FORMAT", 415)
            lengths = request.headers.getlist("content-length")
            if len(lengths) > 1 or (
                lengths and not re.fullmatch(r"[0-9]{1,18}", lengths[0])
            ):
                raise UploadError("INVALID_REQUEST", 400)
            declared = int(lengths[0]) if lengths else None
            if declared is not None and declared > MAX_FILE_BYTES:
                raise UploadError("FILE_TOO_LARGE", 413)
            store = request.app.state.upload_store
            if store is None:
                raise UploadError("STORAGE_UNAVAILABLE", 503)
            data = await store.receive(
                request.stream(), conversation, key, name, declared
            )
            return JSONResponse({"data": data}, status_code=202)
        except UploadError as error:
            messages = {
                "INVALID_FILENAME": "Use a plain Windows-safe CSV filename.",
                "UNSUPPORTED_FORMAT": "This route accepts UTF-8 CSV files only.",
                "INVALID_CSV": "The file is empty, malformed CSV or uses an unsupported encoding.",
                "FILE_TOO_LARGE": "The file exceeds the 100 MB upload limit.",
                "REFERENCE_LIMIT": "This conversation already has ten document references.",
                "CONVERSATION_NOT_FOUND": "The conversation does not exist.",
                "IDEMPOTENCY_CONFLICT": "This upload key was already used for different content or metadata.",
                "UPLOAD_PENDING": "An earlier upload is unresolved; do not submit it with a new key.",
                "UPLOAD_FAILED": "This upload attempt failed; a new upload needs a new key.",
                "CLEANUP_PENDING": "Upload cleanup is pending; restore storage access and restart the app.",
                "SOURCE_UNAVAILABLE": "The stored source is missing or corrupt; it was not recreated.",
            }
            return _error(
                error.code,
                messages.get(
                    error.code,
                    "Upload could not complete; check the file, storage limits and operation state.",
                ),
                error.status,
            )

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
