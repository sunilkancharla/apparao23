"""Reference-scoped extraction and escaped JSON previews, never filesystem paths."""

import re

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.ingestion.validation import UploadError, validate_uuid
from app.storage.extractions import Extractions

router = APIRouter()


def _service(request: Request) -> Extractions:
    store = request.app.state.upload_store
    if store is None:
        raise UploadError("STORAGE_UNAVAILABLE", 503)
    return Extractions(store)


@router.post("/api/conversations/{conversation}/references/{reference}/extractions")
async def extract(conversation: str, reference: str, request: Request) -> JSONResponse:
    """Explicitly extract one chosen reference; the body must be empty."""
    validate_uuid(conversation)
    validate_uuid(reference)
    keys = request.headers.getlist("idempotency-key")
    if len(keys) != 1 or not re.fullmatch(r"[A-Za-z0-9_-]{16,128}", keys[0]):
        raise UploadError("INVALID_REQUEST")
    if request.headers.getlist("content-encoding") or request.query_params:
        raise UploadError("INVALID_REQUEST")
    lengths = request.headers.getlist("content-length")
    if lengths and lengths != ["0"]:
        raise UploadError("INVALID_REQUEST", 400)
    async for chunk in request.stream():
        if chunk:
            raise UploadError("INVALID_REQUEST", 400)
    return JSONResponse(
        {"data": await _service(request).extract(conversation, reference, keys[0])},
        status_code=202,
    )


@router.get("/api/conversations/{conversation}/references/{reference}/preview")
async def preview(conversation: str, reference: str, request: Request) -> dict:
    """Preview the explicitly requested reference with bounded numeric pagination."""
    validate_uuid(conversation)
    validate_uuid(reference)
    if set(request.query_params) - {"after", "limit"}:
        raise UploadError("INVALID_REQUEST")
    values = {}
    for name, default in (("after", "0"), ("limit", "20")):
        supplied = request.query_params.getlist(name)
        if len(supplied) > 1 or (
            supplied and not re.fullmatch(r"[0-9]{1,19}", supplied[0])
        ):
            raise UploadError("INVALID_REQUEST")
        values[name] = int(supplied[0] if supplied else default)
    return {"data": await _service(request).preview(conversation, reference, **values)}
