"""Immutable chunk values; identities never confer permission to read a source."""

import hashlib
from typing import Annotated, Literal, Self

from pydantic import Field, StrictStr, model_validator

from app.ingestion.models import (
    Format,
    Label,
    Location,
    OcrConfidence,
    Offset,
    ParserIdentity,
    Positive,
    ProvenanceModel,
    TextMapping,
)

CHUNKING_VERSION = "source-boundaries-1"
TARGET_BYTES = 600
MAX_BYTES = 800
OVERLAP_BYTES = 120
Digest = Annotated[StrictStr, Field(pattern=r"^[0-9a-f]{64}$")]


class ExtractionIdentity(ProvenanceModel):
    """Extraction envelope without materializing all normalized source units."""

    document_id: Label
    content_hash: Digest
    filename: Label
    format: Format
    extraction_id: Label
    extraction_version: Label
    normalization_version: Label
    warnings: tuple[Label, ...] = ()


class ChunkPart(ProvenanceModel):
    """A verbatim span in a unit's text or table cell, using code-point offsets.

    Mappings retain the original unit's coordinate system. Repeated parts are
    context/overlap, not independent evidence. Missing cells have no text span.
    """

    unit_id: Label
    start: Offset
    end: Offset
    source_start: Offset | None
    source_end: Offset | None
    location: Location
    method: Literal["native", "ocr"]
    parser: ParserIdentity
    confidence: OcrConfidence | None = None
    warnings: tuple[Label, ...] = ()
    mappings: tuple[TextMapping, ...] = ()
    mapping_limitation: Label | None = None
    structure_limitation: Label | None = None
    repeated: bool = False
    row: Positive | None = None
    column: Positive | None = None
    role: Literal["header", "row_key", "data"] | None = None
    stored_type: Label | None = None
    formula: StrictStr | None = None

    @model_validator(mode="after")
    def spans(self) -> Self:
        if self.end < self.start:
            raise ValueError("Reversed chunk span")
        if (self.source_start is None) != (self.source_end is None):
            raise ValueError("Source offsets require a pair")
        if self.source_start is None:
            if self.start != self.end or self.mapping_limitation is None:
                raise ValueError("Missing text requires an empty span and limitation")
        elif self.source_end - self.source_start != self.end - self.start:
            raise ValueError("Verbatim source and chunk span lengths differ")
        if (self.row is None, self.column is None, self.role is None).count(
            True
        ) not in (0, 3):
            raise ValueError("Cell coordinates and role require each other")
        if self.confidence is not None and self.method != "ocr":
            raise ValueError("Native text cannot have OCR confidence")
        return self


class Chunk(ProvenanceModel):
    """At most 800 UTF-8 bytes of evidence text, including generated labels.

    Structured provenance is separate; this cap is neither a serialized metadata
    limit nor a token count. Callers must enforce scope and the whole input budget.
    """

    source: ExtractionIdentity
    chunk_id: Digest
    chunking_version: Literal["source-boundaries-1"] = CHUNKING_VERSION
    text: StrictStr
    text_hash: Digest
    parts: tuple[ChunkPart, ...]
    warnings: tuple[Label, ...] = ()

    @model_validator(mode="after")
    def bounded(self) -> Self:
        if not self.text or len(self.text.encode("utf-8")) > MAX_BYTES:
            raise ValueError("Chunk text exceeds byte budget or is empty")
        if hashlib.sha256(self.text.encode("utf-8")).hexdigest() != self.text_hash:
            raise ValueError("Chunk text hash mismatch")
        if not self.parts:
            raise ValueError("Chunk requires source parts")
        cursor = 0
        for part in self.parts:
            if part.start < cursor or part.end > len(self.text):
                raise ValueError("Unordered or out-of-text chunk part")
            if part.location.format != self.source.format:
                raise ValueError("Chunk source format mismatch")
            cursor = part.end
        return self


class ChunkOmission(ProvenanceModel):
    """Explicit excluded evidence; the unchanged extraction remains available."""

    source: ExtractionIdentity
    unit_ids: tuple[Label, ...]
    code: Literal[
        "EMPTY_TEXT",
        "OVERSIZED_PASSAGE",
        "OVERSIZED_TABLE_ROW",
        "MISSING_TABLE_STRUCTURE",
        "IMAGE_REQUIRES_INTERPRETATION",
    ]
    locations: tuple[Location, ...]
    source_start: Offset | None = None
    source_end: Offset | None = None
    warnings: tuple[Label, ...] = ()
