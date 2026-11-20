"""Loss-aware provenance values; validation never invents source coordinates."""

import re
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, model_validator

Label = Annotated[StrictStr, Field(min_length=1, pattern=r"\S")]
Positive = Annotated[StrictInt, Field(ge=1)]
Offset = Annotated[StrictInt, Field(ge=0)]
Format = Literal["pdf", "xlsx", "csv"]


class ProvenanceModel(BaseModel):
    """Immutable typed fields; preserve plain untrusted text and reject extras."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class Precision(ProvenanceModel):
    """Coarse/unavailable anchors always explain their limitation."""

    precision: Literal["exact", "coarse", "unavailable"]
    limitation: Label | None = None

    @model_validator(mode="after")
    def explain_precision(self) -> Self:
        if self.precision != "exact" and self.limitation is None:
            raise ValueError("Coarse or unavailable locations require a limitation")
        return self


class PdfRegion(ProvenanceModel):
    """Page-local PDF points measured from the top-left, without inferred geometry."""

    x0: Annotated[float, Field(strict=True, ge=0)]
    y0: Annotated[float, Field(strict=True, ge=0)]
    x1: Annotated[float, Field(strict=True, ge=0)]
    y1: Annotated[float, Field(strict=True, ge=0)]

    @model_validator(mode="after")
    def ordered(self) -> Self:
        if self.x1 <= self.x0 or self.y1 <= self.y0:
            raise ValueError("Region must have positive width and height")
        return self


class PdfLocation(Precision):
    """Actual 1-based pages; a region is meaningful only on one identified page."""

    format: Literal["pdf"]
    pages: tuple[Positive, ...] = ()
    region: PdfRegion | None = None

    @model_validator(mode="after")
    def coordinates(self) -> Self:
        if len(set(self.pages)) != len(self.pages):
            raise ValueError("Duplicate pages")
        if self.precision == "exact" and not self.pages:
            raise ValueError("Exact PDF location requires pages")
        if self.region is not None and len(self.pages) != 1:
            raise ValueError("Region requires one page")
        if self.precision == "unavailable" and (self.pages or self.region):
            raise ValueError("Unavailable location cannot assert coordinates")
        return self


def _cell(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"([A-Z]{1,3})([1-9][0-9]{0,6})", value)
    if match is None:
        raise ValueError("Invalid canonical A1 cell")
    column = 0
    for character in match[1]:
        column = column * 26 + ord(character) - ord("A") + 1
    row = int(match[2])
    if column > 16384 or row > 1048576:
        raise ValueError("Cell exceeds XLSX bounds")
    return row, column


class XlsxLocation(Precision):
    """Stored sheet/range identity; merged origin is metadata, never computation."""

    format: Literal["xlsx"]
    sheet: Label | None = None
    sheet_index: Positive | None = None
    cell_range: Label | None = None
    merged_origin: Label | None = None

    @model_validator(mode="after")
    def coordinates(self) -> Self:
        if self.precision == "exact" and (
            self.sheet is None or self.cell_range is None
        ):
            raise ValueError("Exact XLSX location requires sheet and range")
        if self.precision == "unavailable" and any(
            value is not None
            for value in (
                self.sheet,
                self.sheet_index,
                self.cell_range,
                self.merged_origin,
            )
        ):
            raise ValueError("Unavailable location cannot assert coordinates")
        if self.cell_range is not None:
            parts = self.cell_range.split(":")
            if len(parts) not in (1, 2):
                raise ValueError("Invalid cell range")
            start, end = _cell(parts[0]), _cell(parts[-1])
            if start[0] > end[0] or start[1] > end[1]:
                raise ValueError("Reversed cell range")
        if self.merged_origin is not None:
            _cell(self.merged_origin)
        return self


class CsvColumn(ProvenanceModel):
    """1-based column identity; duplicate/missing header names remain distinguishable."""

    position: Positive
    name: StrictStr | None = None


class CsvLocation(Precision):
    """1-based data records (excluding header) and inclusive physical-line spans."""

    format: Literal["csv"]
    record_start: Positive | None = None
    record_end: Positive | None = None
    line_start: Positive | None = None
    line_end: Positive | None = None
    columns: tuple[CsvColumn, ...] = ()

    @model_validator(mode="after")
    def coordinates(self) -> Self:
        for start, end in (
            (self.record_start, self.record_end),
            (self.line_start, self.line_end),
        ):
            if (start is None) != (end is None) or (start is not None and end < start):
                raise ValueError("Spans require ordered start/end pairs")
        if len({column.position for column in self.columns}) != len(self.columns):
            raise ValueError("Duplicate column positions")
        if self.precision == "exact" and (
            self.record_start is None or self.line_start is None or not self.columns
        ):
            raise ValueError("Exact CSV location requires records, lines and columns")
        if self.precision == "unavailable" and (
            self.record_start is not None or self.line_start is not None or self.columns
        ):
            raise ValueError("Unavailable location cannot assert coordinates")
        return self


Location = Annotated[
    PdfLocation | XlsxLocation | CsvLocation, Field(discriminator="format")
]


class ParserIdentity(ProvenanceModel):
    """Actual emitting parser/OCR engine and its version, per normalized unit."""

    name: Label
    version: Label


class OcrConfidence(ProvenanceModel):
    """Uncalibrated engine value and named scale; absent confidence stays None."""

    value: Annotated[float, Field(strict=True)]
    scale: Label


class TextMapping(ProvenanceModel):
    """Zero-based, end-exclusive Unicode code-point spans, not UTF-8 byte offsets."""

    start: Offset
    end: Offset
    source_unit_id: Label
    source_start: Offset | None = None
    source_end: Offset | None = None
    limitation: Label | None = None

    @model_validator(mode="after")
    def ordered(self) -> Self:
        if self.end <= self.start:
            raise ValueError("Empty/reversed normalized span")
        if (self.source_start is None) != (self.source_end is None):
            raise ValueError("Source offsets require a pair")
        if self.source_start is None and self.limitation is None:
            raise ValueError("Unknown source offsets require a limitation")
        if self.source_start is not None and self.source_end <= self.source_start:
            raise ValueError("Empty/reversed source span")
        return self


class TableCell(ProvenanceModel):
    """Explicit grid relationships and source anchors; formula text is inert data."""

    row: Positive
    column: Positive
    role: Literal["header", "row_key", "data"]
    text: StrictStr | None
    location: Location
    stored_type: Label | None = None
    formula: StrictStr | None = None
    warnings: tuple[Label, ...] = ()

    @model_validator(mode="after")
    def disclose_missing_cache(self) -> Self:
        if self.formula is not None and self.text is None and not self.warnings:
            raise ValueError("Missing formula cache requires a warning")
        return self


class SourceUnit(ProvenanceModel):
    """One passage, structured/coarse table or image reference, without visual inference."""

    unit_id: Label
    kind: Literal["passage", "table", "image"]
    text: StrictStr
    method: Literal["native", "ocr"]
    parser: ParserIdentity
    location: Location
    confidence: OcrConfidence | None = None
    warnings: tuple[Label, ...] = ()
    mappings: tuple[TextMapping, ...] = ()
    mapping_limitation: Label | None = None
    row_count: Positive | None = None
    column_count: Positive | None = None
    cells: tuple[TableCell, ...] = ()
    structure_limitation: Label | None = None

    @model_validator(mode="after")
    def relationships(self) -> Self:
        if self.confidence is not None and self.method != "ocr":
            raise ValueError("OCR confidence cannot label native text")
        cursor = 0
        for span in self.mappings:
            if span.start < cursor or span.end > len(self.text):
                raise ValueError("Mappings overlap, are unordered or exceed text")
            if span.start != cursor and self.mapping_limitation is None:
                raise ValueError("Unmapped text requires a limitation")
            cursor = span.end
        if cursor != len(self.text) and self.mapping_limitation is None:
            raise ValueError("Unmapped text requires a limitation")
        if self.kind == "table":
            if self.cells:
                if self.row_count is None or self.column_count is None:
                    raise ValueError("Structured table requires dimensions")
                positions = {(cell.row, cell.column) for cell in self.cells}
                if len(positions) != len(self.cells) or any(
                    cell.row > self.row_count or cell.column > self.column_count
                    for cell in self.cells
                ):
                    raise ValueError("Duplicate or out-of-grid cell")
            elif self.structure_limitation is None:
                raise ValueError("Unstructured table requires a limitation")
        elif self.cells or self.row_count is not None or self.column_count is not None:
            raise ValueError("Only tables can contain grid data")
        if (
            self.kind in {"table", "image"}
            and isinstance(self.location, PdfLocation)
            and self.location.precision == "exact"
            and self.location.region is None
        ):
            raise ValueError(
                "PDF table/image without region must disclose coarse precision"
            )
        return self


class NormalizedExtraction(ProvenanceModel):
    """Versioned extraction data kept separate from originals and retrieval chunks."""

    document_id: Label
    content_hash: Annotated[StrictStr, Field(pattern=r"^[0-9a-f]{64}$")]
    filename: Label
    format: Format
    extraction_id: Label
    extraction_version: Label
    normalization_version: Label
    units: tuple[SourceUnit, ...]
    warnings: tuple[Label, ...] = ()

    @model_validator(mode="after")
    def identities_and_formats(self) -> Self:
        if len({unit.unit_id for unit in self.units}) != len(self.units):
            raise ValueError("Duplicate unit identities")
        for unit in self.units:
            if unit.location.format != self.format or any(
                cell.location.format != self.format for cell in unit.cells
            ):
                raise ValueError("Location format must match document format")
        return self
