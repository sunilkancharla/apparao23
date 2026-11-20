"""Bounded same-origin answer/selection routes; no caller-supplied model or history."""

import json
import re
from typing import Annotated

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr

from app.chat.citations import Citations
from app.chat.service import ChatService
from app.ingestion.validation import UploadError, validate_uuid
from app.ollama import _invalid_constant, _object
from app.storage.messages import Messages

router = APIRouter()


class SelectionRequest(BaseModel):
    """Complete explicit selection with optimistic revision protection."""

    model_config = ConfigDict(extra="forbid")
    references: list[StrictStr] = Field(max_length=10)
    expected_revision: Annotated[StrictInt, Field(ge=0, lt=2**63 - 1)]


class AnswerRequest(BaseModel):
    """Question against server selection, never a caller-provided evidence/history list."""

    model_config = ConfigDict(extra="forbid")
    question: StrictStr = Field(min_length=1, max_length=512)
    expected_revision: Annotated[StrictInt, Field(ge=0, lt=2**63 - 1)]


async def _body(request: Request, model):
    if (
        request.query_params
        or request.headers.getlist("content-encoding")
        or request.headers.getlist("content-type") != ["application/json"]
    ):
        raise UploadError("INVALID_REQUEST", 400)
    lengths = request.headers.getlist("content-length")
    if len(lengths) > 1 or (lengths and not re.fullmatch(r"[0-9]{1,18}", lengths[0])):
        raise UploadError("INVALID_REQUEST", 400)
    if lengths and int(lengths[0]) > 4096:
        raise UploadError("REQUEST_TOO_LARGE", 413)
    data = bytearray()
    async for part in request.stream():
        if len(data) + len(part) > 4096:
            raise UploadError("REQUEST_TOO_LARGE", 413)
        data.extend(part)
    if lengths and int(lengths[0]) != len(data):
        raise UploadError("INVALID_REQUEST", 400)
    try:
        return model.model_validate(
            json.loads(
                data.decode(),
                object_pairs_hook=_object,
                parse_constant=_invalid_constant,
            )
        )
    except (ValueError, UnicodeError, RecursionError, TypeError):
        raise UploadError("INVALID_REQUEST") from None


def _store(request: Request):
    store = request.app.state.upload_store
    if store is None:
        raise UploadError("STORAGE_UNAVAILABLE", 503)
    return store


@router.put("/api/conversations/{conversation}/selection")
async def select(conversation: str, request: Request) -> dict:
    """Save only this conversation's references and advance the selection revision."""
    validate_uuid(conversation)
    payload = await _body(request, SelectionRequest)
    for reference in payload.references:
        validate_uuid(reference)
    return {
        "data": Messages(_store(request)).select(
            conversation, payload.references, payload.expected_revision
        )
    }


@router.post("/api/conversations/{conversation}/answers")
async def answer(conversation: str, request: Request) -> JSONResponse:
    """Create/replay a durable bounded answer intent, without a background queue."""
    validate_uuid(conversation)
    keys = request.headers.getlist("idempotency-key")
    if len(keys) != 1 or not re.fullmatch(r"[A-Za-z0-9_-]{16,128}", keys[0]):
        raise UploadError("INVALID_REQUEST")
    payload = await _body(request, AnswerRequest)
    store = _store(request)
    service = request.app.state.chat_service or ChatService(store)
    result = await service.ask(
        conversation, keys[0], payload.question, payload.expected_revision
    )
    return JSONResponse({"data": result}, status_code=202)


@router.get("/api/conversations/{conversation}/answers/{identity}")
async def saved(conversation: str, identity: str, request: Request) -> dict:
    """Read a scoped historical exchange or safe incomplete/error operation status."""
    validate_uuid(conversation)
    validate_uuid(identity)
    if request.query_params:
        raise UploadError("INVALID_REQUEST")
    return {"data": await Citations(_store(request)).read(conversation, identity)}
