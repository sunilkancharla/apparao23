"""Streaming cell tables preserve CSV relationships without a full-document object."""

import csv
import sys
from collections.abc import Iterator
from typing import BinaryIO
from uuid import NAMESPACE_URL, uuid5

from app.ingestion.models import (
    CsvColumn,
    CsvLocation,
    ParserIdentity,
    SourceUnit,
    TableCell,
)
from app.ingestion.validation import UploadError, iter_csv_rows

EXTRACTION_VERSION = "csv-cells-1"
NORMALIZATION_VERSION = "verbatim-cells-1"
PARSER = ParserIdentity(
    name="python.csv", version=f"{sys.version.split()[0]}/csv-{csv.__version__}"
)


class CsvExtractor:
    """Read the first record as headers; emit one two-cell table per data column.

    Units share logical record numbers and original column positions. The header
    is repeated with its own physical anchor, never presented as a data record.
    CSV values remain strings; formulas/commands/URLs are never evaluated.
    """

    def __init__(self, source: BinaryIO, extraction_id: str) -> None:
        self.source, self.extraction_id = source, extraction_id
        self.record_count = self.unit_count = 0
        self.warnings: set[str] = set()

    def __iter__(self) -> Iterator[SourceUnit]:
        rows = iter_csv_rows(self.source)
        found = False
        try:
            try:
                headers, first, last = next(rows)
            except StopIteration:
                raise UploadError("EMPTY_CSV") from None
            if not headers:
                raise UploadError("EMPTY_CSV")
            if len(set(headers)) != len(headers):
                self.warnings.add("DUPLICATE_HEADERS")
            if any(not header.strip() for header in headers):
                self.warnings.add("BLANK_HEADERS")
            header_warnings = set(self.warnings)
            for record, (values, start, end) in enumerate(rows, 1):
                self.record_count = record
                mismatch = len(values) != len(headers)
                if mismatch:
                    self.warnings.add("ROW_WIDTH_MISMATCH")
                for index in range(max(len(values), len(headers))):
                    value = values[index] if index < len(values) else None
                    name = headers[index] if index < len(headers) else None
                    found |= value is not None and bool(value.strip())
                    warnings = set(header_warnings)
                    if mismatch:
                        warnings.add("ROW_WIDTH_MISMATCH")
                    if value is None:
                        warnings.add("MISSING_CELL")
                    if index >= len(headers):
                        warnings.add("MISSING_HEADER")
                    column = CsvColumn(position=index + 1, name=name)
                    location = CsvLocation(
                        format="csv",
                        precision="exact" if value is not None else "coarse",
                        record_start=record,
                        record_end=record,
                        line_start=start,
                        line_end=end,
                        columns=(column,),
                        limitation=None
                        if value is not None
                        else "Record lacks this header column; no value exists.",
                    )
                    header_location = CsvLocation(
                        format="csv",
                        precision="coarse",
                        line_start=first,
                        line_end=last,
                        columns=(column,) if index < len(headers) else (),
                        limitation="Header is not a data record; use physical lines/position."
                        if index < len(headers)
                        else "No header cell exists at this data-column position.",
                    )
                    identity = str(
                        uuid5(
                            NAMESPACE_URL,
                            f"{self.extraction_id}/record/{record}/column/{index + 1}",
                        )
                    )
                    unit = SourceUnit(
                        unit_id=identity,
                        kind="table",
                        text=value or "",
                        method="native",
                        parser=PARSER,
                        location=location,
                        warnings=tuple(sorted(warnings)),
                        mapping_limitation="Verbatim decoded cell text; raw CSV byte/quote offsets are not retained.",
                        row_count=2,
                        column_count=1,
                        cells=(
                            TableCell(
                                row=1,
                                column=1,
                                role="header",
                                text=name,
                                location=header_location,
                                stored_type="text",
                            ),
                            TableCell(
                                row=2,
                                column=1,
                                role="data",
                                text=value,
                                location=location,
                                stored_type="text",
                            ),
                        ),
                    )
                    self.unit_count += 1
                    yield unit
            if not found:
                raise UploadError("EMPTY_CSV")
        finally:
            rows.close()
