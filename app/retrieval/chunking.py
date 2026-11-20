"""Deterministic T16 byte guards over normalized evidence, without inference."""

import hashlib
import json
import re
from collections.abc import Iterable, Iterator
from itertools import groupby

from app.ingestion.models import (
    CsvLocation,
    NormalizedExtraction,
    PdfLocation,
    SourceUnit,
    TableCell,
)
from app.retrieval.models import (
    CHUNKING_VERSION,
    MAX_BYTES,
    OVERLAP_BYTES,
    TARGET_BYTES,
    Chunk,
    ChunkOmission,
    ChunkPart,
    ExtractionIdentity,
)

# Conservative complete boundaries; no word, number or UTF-8 byte slicing.
_BOUNDARY = re.compile(r'[.!?]["\')\]]*\s+|\n\s*\n')


def _label(unit: SourceUnit) -> str:
    location = unit.location
    if isinstance(location, PdfLocation):
        anchor = "pages " + ",".join(map(str, location.pages))
    elif isinstance(location, CsvLocation):
        anchor = (
            f"records {location.record_start}-{location.record_end} "
            f"lines {location.line_start}-{location.line_end}"
        )
    else:
        anchor = f"sheet {json.dumps(location.sheet, ensure_ascii=False)} {location.cell_range}"
    return f"[{location.format} {anchor}; {location.precision}; {unit.method}]\n"


def _part(
    unit: SourceUnit, start: int, end: int, source_start: int, repeated: bool
) -> ChunkPart:
    return ChunkPart(
        unit_id=unit.unit_id,
        start=start,
        end=end,
        source_start=source_start,
        source_end=source_start + end - start,
        location=unit.location,
        method=unit.method,
        parser=unit.parser,
        confidence=unit.confidence,
        warnings=unit.warnings,
        mappings=unit.mappings,
        mapping_limitation=unit.mapping_limitation,
        structure_limitation=unit.structure_limitation,
        repeated=repeated,
    )


def _chunk(
    source: ExtractionIdentity,
    text: str,
    parts: tuple[ChunkPart, ...],
    warnings: tuple[str, ...] = (),
) -> Chunk:
    text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    # Document/display identities are views, not shared-content index identities.
    identity = {
        "content_hash": source.content_hash,
        "extraction_id": source.extraction_id,
        "extraction_version": source.extraction_version,
        "normalization_version": source.normalization_version,
        "chunking_version": CHUNKING_VERSION,
        "text_hash": text_hash,
        "parts": [part.model_dump(mode="json") for part in parts],
    }
    chunk_id = hashlib.sha256(
        json.dumps(identity, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    warnings = tuple(
        sorted(
            set(
                warnings + source.warnings + tuple(w for p in parts for w in p.warnings)
            )
        )
    )
    return Chunk(
        source=source,
        chunk_id=chunk_id,
        text=text,
        text_hash=text_hash,
        parts=parts,
        warnings=warnings,
    )


def _prose(
    source: ExtractionIdentity, unit: SourceUnit
) -> Iterator[Chunk | ChunkOmission]:
    if not unit.text.strip():
        yield _omission(source, (unit,), "EMPTY_TEXT")
        return
    label = _label(unit)
    label_bytes = len(label.encode("utf-8"))
    # Work over offsets; large unsplittable passages are never copied into chunks.
    boundaries = (match.end() for match in _BOUNDARY.finditer(unit.text))
    atoms: list[tuple[int, int]] = []
    used = label_bytes
    previous_end = 0
    repeated_end = 0
    for end in _ends(boundaries, len(unit.text)):
        atom = (previous_end, end)
        previous_end = end
        size = len(unit.text[atom[0] : atom[1]].encode("utf-8"))
        if atoms and used + size > TARGET_BYTES:
            yield _prose_chunk(source, unit, label, atoms, repeated_end)
            overlap: list[tuple[int, int]] = []
            overlap_bytes = 0
            for candidate in reversed(atoms):
                candidate_bytes = len(
                    unit.text[candidate[0] : candidate[1]].encode("utf-8")
                )
                if overlap_bytes + candidate_bytes > OVERLAP_BYTES:
                    break
                overlap.insert(0, candidate)
                overlap_bytes += candidate_bytes
            atoms = overlap if label_bytes + overlap_bytes + size <= MAX_BYTES else []
            used = label_bytes + (overlap_bytes if atoms else 0)
            repeated_end = atoms[-1][1] if atoms else 0
        if label_bytes + size > MAX_BYTES:
            yield _omission(source, (unit,), "OVERSIZED_PASSAGE", *atom)
            atoms, used = [], label_bytes
            repeated_end = 0
            continue
        atoms.append(atom)
        used += size
    if atoms:
        yield _prose_chunk(source, unit, label, atoms, repeated_end)


def _ends(boundaries: Iterator[int], length: int) -> Iterator[int]:
    last = 0
    for last in boundaries:
        yield last
    if last != length:
        yield length


def _prose_chunk(
    source: ExtractionIdentity,
    unit: SourceUnit,
    label: str,
    atoms: list[tuple[int, int]],
    repeated_end: int,
) -> Chunk:
    start, end = atoms[0][0], atoms[-1][1]
    text = label + unit.text[start:end]
    parts = []
    if repeated_end > start:
        parts.append(
            _part(unit, len(label), len(label) + repeated_end - start, start, True)
        )
    fresh_start = max(start, repeated_end)
    parts.append(
        _part(unit, len(label) + fresh_start - start, len(text), fresh_start, False)
    )
    return _chunk(
        source,
        text,
        tuple(parts),
        ("SOURCE_UNIT_SPLIT",) if start or end < len(unit.text) else (),
    )


def _omission(
    source: ExtractionIdentity,
    units: tuple[SourceUnit, ...],
    code: str,
    start: int | None = None,
    end: int | None = None,
) -> ChunkOmission:
    return ChunkOmission(
        source=source,
        unit_ids=tuple(unit.unit_id for unit in units),
        code=code,
        locations=tuple(unit.location for unit in units),
        source_start=start,
        source_end=end,
        warnings=tuple(
            sorted(
                set(source.warnings + tuple(w for unit in units for w in unit.warnings))
            )
        ),
    )


def _csv_record(unit: SourceUnit) -> tuple | None:
    """Recognize T25's per-column tables; never infer keys from cell contents."""
    loc = unit.location
    if (
        unit.kind == "table"
        and isinstance(loc, CsvLocation)
        and loc.record_start == loc.record_end
        and loc.record_start is not None
        and len(loc.columns) == 1
        and unit.row_count == 2
        and unit.column_count == 1
        and len(unit.cells) == 2
        and unit.cells[0].role == "header"
        and unit.cells[1].role == "data"
    ):
        return (loc.record_start, loc.line_start, loc.line_end)
    return None


def _render_table(
    source: ExtractionIdentity, entries: list[tuple[SourceUnit, TableCell, bool]]
) -> Chunk | None:
    text = _label(entries[0][0])
    used = len(text.encode("utf-8"))
    parts = []
    for unit, cell, repeated in entries:
        location = cell.location
        if isinstance(location, CsvLocation) and location.columns:
            position = f"column {location.columns[0].position}"
        else:
            position = f"r{cell.row}c{cell.column}"
        label = f"{position} {cell.role}: "
        value = "<missing value>" if cell.text is None else cell.text
        used += len(label.encode("utf-8")) + len(value.encode("utf-8")) + 1
        if used > MAX_BYTES:
            return None
        start = len(text) + len(label)
        end = start + (len(cell.text) if cell.text is not None else 0)
        # Cell offsets refer to decoded cell text, not the unit's flattened text.
        part = ChunkPart.model_validate(
            _part(unit, start, end, 0, repeated).model_dump()
            | {
                "source_start": None if cell.text is None else 0,
                "source_end": None if cell.text is None else len(cell.text),
                "location": cell.location,
                "mappings": (),
                "mapping_limitation": "Cell-relative decoded text; no raw-file offset mapping.",
                "row": cell.row,
                "column": cell.column,
                "role": cell.role,
                "stored_type": cell.stored_type,
                "formula": cell.formula,
                "warnings": tuple(sorted(set(unit.warnings + cell.warnings))),
            }
        )
        parts.append(part)
        text += label + value + "\n"
    return _chunk(source, text, tuple(parts))


def _table(
    source: ExtractionIdentity, units: tuple[SourceUnit, ...], csv_record: bool
) -> Iterator[Chunk | ChunkOmission]:
    if any(not unit.cells for unit in units):
        yield _omission(source, units, "MISSING_TABLE_STRUCTURE")
        return
    if csv_record:
        columns = [unit.location.columns[0].position for unit in units]
        if columns != sorted(set(columns)):
            raise ValueError("CSV record columns must be unique and ordered")
        # All columns stay together: the parser has declared no semantic row key.
        entries = [
            (u, c, c.role == "header" and u.location.record_start > 1)
            for u in units
            for c in u.cells
        ]
        chunk = _render_table(source, entries)
        yield (
            chunk
            if chunk is not None
            else _omission(source, units, "OVERSIZED_TABLE_ROW")
        )
        return
    unit = units[0]
    ordered_cells = sorted(unit.cells, key=lambda c: (c.row, c.column))
    headers = [(unit, c, False) for c in ordered_cells if c.role == "header"]
    rows: dict[int, list[TableCell]] = {}
    for cell in ordered_cells:
        if cell.role != "header":
            rows.setdefault(cell.row, []).append(cell)
    if not rows:
        yield _omission(source, units, "EMPTY_TEXT")
    for row_index, cells in enumerate(rows.values()):
        context = [(u, c, row_index > 0) for u, c, _ in headers]
        entries = context + [(unit, c, False) for c in cells]
        chunk = _render_table(source, entries)
        if chunk is not None:
            yield chunk
            continue
        keys = [c for c in cells if c.role == "row_key"]
        values = [c for c in cells if c.role == "data"]
        # A declared row key permits column fragments. Retain every header/unit
        # label rather than guessing which context is dispensable.
        fragments = []
        if keys and values:
            for index, cell in enumerate(values):
                fragment = _render_table(
                    source,
                    [(u, c, True) for u, c, _ in context]
                    + [(unit, c, index > 0) for c in keys]
                    + [(unit, cell, False)],
                )
                if fragment is None:
                    break
                fragments.append(fragment)
            else:
                for fragment in fragments:
                    yield fragment.model_copy(
                        update={
                            "warnings": tuple(
                                sorted(set(fragment.warnings + ("TABLE_ROW_SPLIT",)))
                            )
                        }
                    )
                continue
        # Publish no partial row if even one complete value/context cannot fit.
        yield _omission(source, units, "OVERSIZED_TABLE_ROW")


def iter_chunks(
    extraction: NormalizedExtraction, units: Iterable[SourceUnit] | None = None
) -> Iterator[Chunk | ChunkOmission]:
    """Yield bounded chunks and explicit omissions from a validated extraction.

    An optional ordered unit stream supports T25's separately stored envelope.
    This pure transform reads no files and grants no retrieval/reference scope.
    """
    source = ExtractionIdentity.model_validate(extraction.model_dump(exclude={"units"}))
    stream = extraction.units if units is None else units
    last_record = 0
    for key, group in groupby(
        stream, key=lambda unit: _csv_record(unit) or unit.unit_id
    ):
        grouped = tuple(group)
        if any(unit.location.format != source.format for unit in grouped):
            raise ValueError("Source unit format differs from extraction")
        unit = grouped[0]
        if not isinstance(key, tuple) and len(grouped) != 1:
            raise ValueError("Duplicate source unit identity")
        if isinstance(key, tuple):
            if key[0] <= last_record:
                raise ValueError("CSV records must be ordered")
            last_record = key[0]
            yield from _table(source, grouped, True)
        elif unit.kind == "passage":
            yield from _prose(source, unit)
        elif unit.kind == "table":
            yield from _table(source, grouped, False)
        else:
            yield _omission(source, grouped, "IMAGE_REQUIRES_INTERPRETATION")
