"""Checked source spans and scoped live previews; model prose is never provenance."""

import asyncio
import html
import json
import re
from collections.abc import Mapping
from typing import TYPE_CHECKING

from app.chat.generation import Answer
from app.config import ConfigurationError
from app.ingestion.models import SourceUnit
from app.ingestion.validation import UploadError
from app.retrieval.models import Chunk
from app.retrieval.search import Evidence
from app.storage.index_state import IndexState
from app.storage.messages import Messages

if TYPE_CHECKING:
    from app.storage.files import UploadStore


def validate_citations(answer: Answer, evidence: tuple[Evidence, ...]) -> None:
    """Require unique supplied IDs and cited answered claims, without judging meaning."""
    allowed = {e.evidence_id for e in evidence}
    if len(allowed) != len(evidence) or any(
        not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", value) for value in allowed
    ):
        raise UploadError("CHAT_EVIDENCE_INVALID", 503)
    for claim in answer.claims:
        if (
            not claim.text.strip()
            or len(set(claim.citations)) != len(claim.citations)
            or set(claim.citations) - allowed
            or (answer.status in {"answered", "partial"} and not claim.citations)
        ):
            raise UploadError("CHAT_RESPONSE_INVALID", 503)


def checked_passages(chunk: Chunk, units: Mapping[str, SourceUnit]) -> list[dict]:
    """Resolve verbatim Unicode spans against normalized text/cells and real anchors.

    Generated chunk labels are never quotations. Table offsets refer to decoded
    cell values; missing cells stay None, distinct from an empty quoted string.
    """
    result = []
    try:
        chunk = Chunk.model_validate(chunk.model_dump())
        for part in chunk.parts:
            unit = units[part.unit_id]
            if (part.method, part.parser, part.confidence) != (
                unit.method,
                unit.parser,
                unit.confidence,
            ):
                raise ValueError
            if part.row is None:
                if (
                    part.column is not None
                    or part.role is not None
                    or unit.kind != "passage"
                ):
                    raise ValueError
                text, location, warnings = unit.text, unit.location, unit.warnings
            else:
                cells = [
                    c
                    for c in unit.cells
                    if (c.row, c.column) == (part.row, part.column)
                ]
                if len(cells) != 1:
                    raise ValueError
                cell = cells[0]
                if (part.role, part.stored_type, part.formula) != (
                    cell.role,
                    cell.stored_type,
                    cell.formula,
                ):
                    raise ValueError
                text, location = cell.text, cell.location
                warnings = tuple(sorted(set(unit.warnings + cell.warnings)))
            if part.location != location or part.warnings != warnings:
                raise ValueError
            if text is None:
                if part.source_start is not None or part.start != part.end:
                    raise ValueError
                quote = None
            else:
                if (
                    part.source_start is None
                    or not 0 <= part.source_start <= part.source_end <= len(text)
                ):
                    raise ValueError
                quote = text[part.source_start : part.source_end]
                if quote != chunk.text[part.start : part.end]:
                    raise ValueError
            result.append(
                {
                    "quote": quote,
                    "unit_id": part.unit_id,
                    "start": part.start,
                    "end": part.end,
                    "source_start": part.source_start,
                    "source_end": part.source_end,
                    "location": location.model_dump(mode="json"),
                    "method": part.method,
                    "parser": part.parser.model_dump(mode="json"),
                    "confidence": part.confidence.model_dump(mode="json")
                    if part.confidence
                    else None,
                    "warnings": list(warnings),
                    "mapping_limitation": part.mapping_limitation,
                    "structure_limitation": part.structure_limitation,
                    "repeated": part.repeated,
                    "role": part.role,
                }
            )
    except (ValueError, KeyError, TypeError):
        raise UploadError("CITATION_INVALID", 503) from None
    return result


def _escaped(value):
    """Escape every source-derived string once for the explicit preview surface."""
    if isinstance(value, str):
        return html.escape(value, quote=True)
    if isinstance(value, list):
        return [_escaped(item) for item in value]
    if isinstance(value, dict):
        return {key: _escaped(item) for key, item in value.items()}
    return value


class Citations:
    """Resolve a citation only within its saved answer and current source membership."""

    def __init__(self, store: "UploadStore") -> None:
        self.store = store
        self.messages = Messages(store)
        self.index = IndexState(store)

    @staticmethod
    def _items(saved: dict) -> dict[str, dict]:
        if saved["state"] != "complete":
            return {}
        try:
            answer = Answer.model_validate(saved["answer"])
            evidence = saved["evidence"]
            required = {
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
            if len(evidence) > 5 or any(set(item) != required for item in evidence):
                raise ValueError
            items = {item["evidence_id"]: item for item in evidence}
            if len(items) != len(evidence):
                raise ValueError
            cited = {value for claim in answer.claims for value in claim.citations}
            if not cited.issubset(items):
                raise ValueError
            return {value: items[value] for value in sorted(cited)}
        except (ValueError, KeyError, TypeError):
            raise UploadError("CITATION_INVALID", 503) from None

    def _current(self, conversation: str, item: dict):
        try:
            source, extraction = self.index.source(conversation, item["reference_id"])
            status = self.index.status(conversation, item["reference_id"])
            if (
                status is None
                or not status["indexed"]
                or (
                    source["document_id"],
                    source["content_hash"],
                    extraction["id"],
                    status["generation_id"],
                    source["display_name"],
                )
                != (
                    item["document_id"],
                    item["content_hash"],
                    item["extraction_id"],
                    item["generation_id"],
                    item["filename"],
                )
            ):
                raise UploadError("SOURCE_UNAVAILABLE", 410)
        except UploadError:
            raise UploadError("SOURCE_UNAVAILABLE", 410) from None
        return source, extraction, status

    async def _resolve(self, conversation: str, item: dict) -> dict:
        source, _, _ = self._current(conversation, item)
        try:
            await asyncio.to_thread(
                self.store._verified_original,
                source["content_hash"],
                source["byte_size"],
            )
        except (OSError, ConfigurationError):
            raise UploadError("SOURCE_UNAVAILABLE", 410) from None
        # Membership/generation may change while the original is hashed. No await
        # follows this second check before the scoped preview is assembled.
        self._current(conversation, item)
        rows = self.store.connection.execute(
            """SELECT c.payload,c.chunk_id,v.text_hash FROM index_chunks c
            JOIN index_bindings b ON b.id=c.binding_id AND b.generation_id=c.generation_id
            JOIN index_vectors v ON v.generation_id=c.generation_id AND v.ordinal=c.ordinal
            WHERE b.extraction_id=? AND b.generation_id=? AND c.chunk_id=? LIMIT 2""",
            (item["extraction_id"], item["generation_id"], item["chunk_id"]),
        ).fetchall()
        try:
            if len(rows) != 1:
                raise ValueError
            row = rows[0]
            chunk = Chunk.model_validate_json(row["payload"])
            if (
                (chunk.chunk_id, chunk.text_hash)
                != (item["chunk_id"], item["text_hash"])
                or row["text_hash"] != chunk.text_hash
                or (
                    chunk.source.document_id,
                    chunk.source.content_hash,
                    chunk.source.extraction_id,
                    chunk.source.filename,
                )
                != (
                    item["document_id"],
                    item["content_hash"],
                    item["extraction_id"],
                    item["filename"],
                )
                or [p.location.model_dump(mode="json") for p in chunk.parts]
                != item["locations"]
                or list(chunk.warnings) != item["warnings"]
            ):
                raise ValueError
            units = {}
            for unit_id in {p.unit_id for p in chunk.parts}:
                unit_rows = self.store.connection.execute(
                    "SELECT payload FROM csv_units WHERE extraction_id=? AND unit_id=? LIMIT 2",
                    (item["extraction_id"], unit_id),
                ).fetchall()
                if len(unit_rows) != 1:
                    raise ValueError
                unit = SourceUnit.model_validate_json(unit_rows[0][0])
                if unit.unit_id != unit_id:
                    raise ValueError
                units[unit_id] = unit
            passages = checked_passages(chunk, units)
        except (ValueError, KeyError, TypeError):
            raise UploadError("CITATION_INVALID", 503) from None
        result = _escaped(
            {
                "citation_id": item["evidence_id"],
                "reference_id": item["reference_id"],
                "document_id": item["document_id"],
                "extraction_id": item["extraction_id"],
                "generation_id": item["generation_id"],
                "chunk_id": chunk.chunk_id,
                "filename": chunk.source.filename,
                "format": chunk.source.format,
                "locations": item["locations"],
                "passages": passages,
                "warnings": list(
                    dict.fromkeys((*chunk.warnings, "MEANING_NOT_VERIFIED"))
                ),
                "source_availability": "available",
                "quote_origin": "current_normalized_source",
                "escaped": True,
            }
        )
        if (
            len(
                json.dumps(
                    {"data": result}, ensure_ascii=False, separators=(",", ":")
                ).encode()
            )
            > 65_536
        ):
            raise UploadError("PREVIEW_LIMIT", 503)
        return result

    def _admit(self) -> None:
        if self.store.busy or self.store.recovery_pending:
            raise UploadError("SOURCE_BUSY", 409)
        self.store.busy = True

    async def preview(self, conversation: str, identity: str, citation: str) -> dict:
        """Return one escaped, bounded live source preview, never a model-supplied path."""
        saved = self.messages.get(conversation, identity)
        item = self._items(saved).get(citation)
        if item is None:
            raise UploadError("CITATION_NOT_FOUND", 404)
        self._admit()
        try:
            async with asyncio.timeout(90):
                return await self._resolve(conversation, item)
        except TimeoutError:
            raise UploadError("SOURCE_TIMEOUT", 503) from None
        finally:
            self.store.busy = False

    async def read(self, conversation: str, identity: str) -> dict:
        """Keep historical answer text readable and label each live citation's availability."""
        saved = self.messages.get(conversation, identity)
        items = self._items(saved)
        saved["citations"] = []
        saved["source_availability"] = "not_applicable"
        if not items:
            return saved
        if self.store.busy or self.store.recovery_pending:
            saved["citations"] = [
                {
                    "citation_id": citation,
                    "availability": "not_revalidated",
                    "code": "SOURCE_BUSY",
                }
                for citation in items
            ]
            saved["source_availability"] = "not_revalidated"
            return saved
        self._admit()
        try:
            async with asyncio.timeout(90):
                for citation, item in items.items():
                    try:
                        preview = await self._resolve(conversation, item)
                    except UploadError as error:
                        status = {"availability": "unavailable", "code": error.code}
                    else:
                        ocr = [p for p in preview["passages"] if p["method"] == "ocr"]
                        status = {
                            "availability": "available",
                            "code": None,
                            "warning_codes": preview["warnings"],
                            "methods": sorted(
                                {p["method"] for p in preview["passages"]}
                            ),
                            "precisions": sorted(
                                {
                                    p["location"]["precision"]
                                    for p in preview["passages"]
                                }
                            ),
                            "ocr_confidence_available": all(
                                p["confidence"] is not None for p in ocr
                            )
                            if ocr
                            else None,
                        }
                    saved["citations"].append({"citation_id": citation, **status})
                saved["source_availability"] = (
                    "available"
                    if all(c["availability"] == "available" for c in saved["citations"])
                    else "unavailable"
                )
                return saved
        except TimeoutError:
            raise UploadError("SOURCE_TIMEOUT", 503) from None
        finally:
            self.store.busy = False
