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

from app.config import ConfigurationError, Settings, prepare_data_root
from app.diagnostics import ComponentState, inspect_prerequisites, reserve_port


class HealthReport(BaseModel):
    """Startup snapshot; readiness remains false until owned model integration."""

    ready: Literal[False] = False
    components: list[ComponentState]


def _error(code: str, message: str, status: int) -> JSONResponse:
    return JSONResponse(
        {"error": {"code": code, "message": message, "retryable": False}},
        status_code=status,
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create a local read-only diagnostics app without listeners or model execution."""
    config = Settings.from_env() if settings is None else settings

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
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
        yield

    application = FastAPI(
        lifespan=lifespan,
        openapi_url=None,
        docs_url=None,
        redoc_url=None,
    )

    @application.middleware("http")
    async def local_boundary(
        request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # No mutation routes exist yet; reject them before reading any body.
        hosts = request.headers.getlist("host")
        origins = request.headers.getlist("origin")
        if (
            hosts != [config.origin.removeprefix("http://")]
            or (origins and origins != [config.origin])
            or request.method not in {"GET", "HEAD"}
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
