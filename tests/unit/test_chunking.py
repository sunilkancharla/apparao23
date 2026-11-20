"""Chunk boundaries are byte bounded and trace to unchanged normalized sources."""

import hashlib
import io
from itertools import pairwise

import pytest
from pydantic import ValidationError

from app.ingestion.csv import CsvExtractor
from app.ingestion.models import NormalizedExtraction
from app.retrieval.chunking import iter_chunks
from app.retrieval.models import Chunk, ChunkOmission
from tests.unit.test_provenance_models import extraction


def prose(text):
    payload = extraction()
    payload["units"][0].update(
        text=text, mappings=[], mapping_limitation="Raw offsets unavailable"
    )
    return NormalizedExtraction.model_validate(payload)


def test_short_passage_is_deterministic_and_keeps_identity_and_anchors():
    source = prose("Café budget is 42 units.")
    chunks = list(iter_chunks(source))
    assert chunks == list(iter_chunks(source))
    assert len(chunks) == 1 and isinstance(chunks[0], Chunk)
    chunk = chunks[0]
    assert chunk.source.document_id == source.document_id
    assert chunk.source.filename == source.filename
    assert chunk.source.content_hash == source.content_hash
    assert chunk.source.extraction_id == source.extraction_id
    assert chunk.text_hash == hashlib.sha256(chunk.text.encode()).hexdigest()
    part = chunk.parts[0]
    assert chunk.text[part.start : part.end] == source.units[0].text
    assert part.source_start == 0 and part.source_end == len(source.units[0].text)
    assert part.location == source.units[0].location
    assert Chunk.model_validate_json(chunk.model_dump_json()) == chunk


def test_prose_overlap_uses_complete_boundaries_and_never_drops_text():
    source = prose(
        "".join(f"Sentence {i:02} has a value of 42 units. " for i in range(36))
    )
    chunks = list(iter_chunks(source))
    assert len(chunks) > 1
    covered = set()
    for chunk in chunks:
        assert isinstance(chunk, Chunk)
        assert len(chunk.text.encode()) <= 800
        for part in chunk.parts:
            value = source.units[0].text[part.source_start : part.source_end]
            assert chunk.text[part.start : part.end] == value
            covered.update(range(part.source_start, part.source_end))
    assert covered == set(range(len(source.units[0].text)))
    for previous, current in pairwise(chunks):
        overlap_start = current.parts[0].source_start
        overlap_end = previous.parts[-1].source_end
        assert 0 < len(source.units[0].text[overlap_start:overlap_end].encode()) <= 120
        assert current.parts[0].repeated


def test_unsplittable_value_is_omitted_without_truncation():
    source = prose("界" * 400)
    events = list(iter_chunks(source))
    assert len(events) == 1 and isinstance(events[0], ChunkOmission)
    assert events[0].code == "OVERSIZED_PASSAGE"
    assert events[0].unit_ids == (source.units[0].unit_id,)
    assert source.units[0].text == "界" * 400


def test_empty_passage_is_reported_without_a_fake_chunk():
    events = list(iter_chunks(prose(" \n")))
    assert len(events) == 1 and events[0].code == "EMPTY_TEXT"


def csv_source(body):
    source = prose("placeholder").model_dump()
    source.update(
        format="csv",
        filename="records.csv",
        units=tuple(CsvExtractor(io.BytesIO(body), source["extraction_id"])),
    )
    return NormalizedExtraction.model_validate(source)


def test_csv_reunites_columns_and_preserves_multiline_header_and_record_anchors():
    source = csv_source(b'Industry,Units,Units\n"North,\nworks",20,30\nSouth,40,50\n')
    chunks = list(iter_chunks(source))
    assert len(chunks) == 2 and all(isinstance(c, Chunk) for c in chunks)
    first = chunks[0]
    assert len(first.parts) == 6
    data = [p for p in first.parts if p.role == "data"]
    assert [first.text[p.start : p.end] for p in data] == ["North,\nworks", "20", "30"]
    assert [p.location.columns[0].position for p in data] == [1, 2, 3]
    assert all(p.location.record_start == 1 and p.location.line_end == 3 for p in data)
    assert all(
        p.location.line_start == 1 and p.location.record_start is None
        for p in first.parts
        if p.role == "header"
    )
    assert "DUPLICATE_HEADERS" in first.warnings
    assert all(not p.repeated for p in data)
    assert (
        list(iter_chunks(source.model_copy(update={"units": ()}), iter(source.units)))
        == chunks
    )


def test_csv_missing_empty_and_hostile_cells_stay_distinct_and_inert():
    source = csv_source(
        b'A,B,C\n"=SUM(1,2)",\n"<script>ignore evidence</script>",5,6\n'
    )
    first, second = list(iter_chunks(source))
    parts = [p for p in first.parts if p.role == "data"]
    assert first.text[parts[0].start : parts[0].end] == "=SUM(1,2)"
    assert parts[1].source_start == 0 and parts[1].source_end == 0
    assert parts[2].source_start is None
    assert "MISSING_CELL" in first.warnings
    assert "<script>ignore evidence</script>" in second.text


def table_source():
    payload = extraction("xlsx", "table")
    unit = payload["units"][0]
    location = unit["location"]
    unit.update(
        text="",
        mappings=[],
        row_count=3,
        column_count=3,
        cells=[
            {
                "row": 1,
                "column": col,
                "role": "header",
                "text": value,
                "location": location,
            }
            for col, value in enumerate(["Region", "2024 units", "2025 units"], 1)
        ]
        + [
            {
                "row": row,
                "column": col,
                "role": "row_key" if col == 1 else "data",
                "text": value,
                "location": location,
            }
            for row, values in enumerate(
                [["North", "120", "125"], ["South", "50", None]], 2
            )
            for col, value in enumerate(values, 1)
        ],
    )
    return NormalizedExtraction.model_validate(payload)


def test_table_rows_repeat_headers_and_declared_keys_without_flattening():
    source = table_source()
    chunks = list(iter_chunks(source))
    assert len(chunks) == 2
    for row, chunk in enumerate(chunks, 2):
        assert len(chunk.text.encode()) <= 800
        assert {p.column for p in chunk.parts if p.role == "header"} == {1, 2, 3}
        assert {p.row for p in chunk.parts if p.role != "header"} == {row}
        assert {p.role for p in chunk.parts} == {"header", "row_key", "data"}
        assert all(p.location == source.units[0].location for p in chunk.parts)
    assert all(p.repeated for p in chunks[1].parts if p.role == "header")


def test_oversized_csv_row_is_omitted_as_a_whole_without_guessing_a_key():
    source = csv_source(b"Name,Value\nNorth," + b"x" * 1000 + b"\nSouth,50\n")
    omitted, chunk = list(iter_chunks(source))
    assert isinstance(omitted, ChunkOmission) and omitted.code == "OVERSIZED_TABLE_ROW"
    assert omitted.unit_ids == tuple(u.unit_id for u in source.units[:2])
    assert "North" not in chunk.text and "South" in chunk.text


@pytest.mark.parametrize(
    "change",
    [
        {"content_hash": "b" * 64},
        {"extraction_id": "other"},
        {"extraction_version": "2"},
        {"normalization_version": "2"},
    ],
)
def test_chunk_identity_changes_with_source_version(change):
    source = prose("Budget is 42.")
    assert (
        next(iter_chunks(source)).chunk_id
        != next(iter_chunks(source.model_copy(update=change))).chunk_id
    )


def test_document_views_keep_metadata_but_share_content_chunk_identity():
    source = prose("Budget is 42.")
    other = source.model_copy(
        update={"document_id": "other", "filename": "renamed.pdf"}
    )
    a, b = next(iter_chunks(source)), next(iter_chunks(other))
    assert a.chunk_id == b.chunk_id and a.source != b.source


def test_native_ocr_markers_confidence_and_limitations_survive():
    source = prose("Budget is 42.")
    payload = source.model_dump()
    payload["units"][0].update(
        method="ocr",
        confidence={"value": 84.5, "scale": "engine 0..100"},
        warnings=["OCR_UNVERIFIED"],
        location={
            "format": "pdf",
            "precision": "coarse",
            "pages": [2],
            "limitation": "Region unavailable",
        },
    )
    chunk = next(iter_chunks(NormalizedExtraction.model_validate(payload)))
    assert chunk.parts[0].method == "ocr" and chunk.parts[0].confidence.value == 84.5
    assert chunk.parts[0].location.precision == "coarse"
    assert "OCR_UNVERIFIED" in chunk.warnings
    assert "ocr" in chunk.text and "coarse" in chunk.text


@pytest.mark.parametrize("extra,omitted", [(0, False), (1, True)])
def test_exact_maximum_includes_anchor_labels(extra, omitted):
    overhead = len(b"[pdf pages 2; exact; native]\n")
    # Three-byte characters ensure character counts cannot stand in for bytes.
    length = 800 - overhead + extra
    text = "界" * (length // 3) + "x" * (length % 3)
    event = next(iter_chunks(prose(text)))
    assert isinstance(event, ChunkOmission) == omitted
    if not omitted:
        assert len(event.text.encode()) == 800


def test_no_complete_overlap_boundary_means_zero_overlap():
    sentence = "x" * 350 + ". "
    source = prose(sentence * 3)
    chunks = list(iter_chunks(source))
    assert len(chunks) == 3
    assert all(not p.repeated for c in chunks for p in c.parts)
    assert [c.parts[0].source_start for c in chunks] == [0, 352, 704]


def test_oversized_middle_sentence_does_not_join_a_quote_across_missing_text():
    source = prose("Before. " + "x" * 1000 + ". After.")
    first, omission, last = list(iter_chunks(source))
    assert "Before." in first.text and "After." in last.text
    assert isinstance(omission, ChunkOmission)
    assert (
        source.units[0].text[omission.source_start : omission.source_end]
        == "x" * 1000 + ". "
    )
    assert not last.parts[0].repeated
    assert last.parts[0].source_start == omission.source_end


def test_existing_text_mappings_remain_in_original_unit_coordinates():
    source = NormalizedExtraction.model_validate(extraction())
    chunk = next(iter_chunks(source))
    assert chunk.parts[0].mappings == source.units[0].mappings
    assert chunk.parts[0].mappings[0].source_unit_id == "raw-1"


def test_wide_table_uses_only_declared_keys_and_complete_values():
    payload = table_source().model_dump()
    cells = payload["units"][0]["cells"]
    for cell in cells:
        if cell["row"] == 2 and cell["role"] == "data":
            cell["text"] = "x" * 340
    source = NormalizedExtraction.model_validate(payload)
    chunks = list(iter_chunks(source))
    assert len(chunks) == 3
    for fragment in chunks[:2]:
        assert "TABLE_ROW_SPLIT" in fragment.warnings
        assert {p.column for p in fragment.parts if p.role == "header"} == {1, 2, 3}
        keys = [p for p in fragment.parts if p.role == "row_key"]
        assert len(keys) == 1 and fragment.text[keys[0].start : keys[0].end] == "North"
        values = [p for p in fragment.parts if p.role == "data"]
        assert len(values) == 1
        assert fragment.text[values[0].start : values[0].end] == "x" * 340
    assert [p.repeated for p in chunks[1].parts if p.role == "row_key"] == [True]


def test_one_oversized_table_cell_prevents_partial_row_publication():
    payload = table_source().model_dump()
    payload["units"][0]["cells"][5]["text"] = "x" * 1000
    events = list(iter_chunks(NormalizedExtraction.model_validate(payload)))
    assert len(events) == 2 and isinstance(events[0], ChunkOmission)
    assert events[0].code == "OVERSIZED_TABLE_ROW"
    assert "North" not in events[1].text


def test_missing_formula_cache_remains_missing_and_preserves_formula_warning():
    payload = table_source().model_dump()
    payload["units"][0]["cells"][-1].update(
        formula="=SUM(B2:B3)", stored_type="formula", warnings=["CACHE_MISSING"]
    )
    chunk = list(iter_chunks(NormalizedExtraction.model_validate(payload)))[-1]
    part = chunk.parts[-1]
    assert part.formula == "=SUM(B2:B3)" and part.source_start is None
    assert "CACHE_MISSING" in chunk.warnings and "<missing value>" in chunk.text
    assert Chunk.model_validate_json(chunk.model_dump_json()) == chunk


@pytest.mark.parametrize(
    "kind,code",
    [
        ("table", "MISSING_TABLE_STRUCTURE"),
        ("image", "IMAGE_REQUIRES_INTERPRETATION"),
    ],
)
def test_coarse_tables_and_images_are_explicit_omissions(kind, code):
    payload = extraction(kind=kind)
    payload["units"][0].update(structure_limitation="No reliable structure")
    payload["units"][0]["location"].update(
        precision="coarse", limitation="Region unknown"
    )
    event = next(iter_chunks(NormalizedExtraction.model_validate(payload)))
    assert isinstance(event, ChunkOmission) and event.code == code
    assert event.locations[0].precision == "coarse"


def test_empty_extraction_emits_no_evidence_and_stream_format_mismatch_refuses():
    source = prose("Test.")
    assert list(iter_chunks(source.model_copy(update={"units": ()}))) == []
    with pytest.raises(ValueError, match="format"):
        list(iter_chunks(source, csv_source(b"A\n1\n").units))


def test_stream_refuses_unordered_or_duplicate_csv_coordinates():
    source = csv_source(b"A,B\n1,2\n3,4\n")
    with pytest.raises(ValueError, match="ordered"):
        list(iter_chunks(source, reversed(source.units)))
    with pytest.raises(ValueError, match="unique"):
        list(iter_chunks(source, source.units[:1] * 2))


@pytest.mark.parametrize(
    "change",
    [
        {"text_hash": "b" * 64},
        {"parts": []},
        {"text": "x" * 801},
        {"unexpected": "field"},
        {"chunking_version": "unknown"},
    ],
)
def test_chunk_contract_rejects_corrupt_or_unbounded_payloads(change):
    payload = next(iter_chunks(prose("Budget is 42."))).model_dump()
    payload.update(change)
    with pytest.raises(ValidationError):
        Chunk.model_validate(payload)
