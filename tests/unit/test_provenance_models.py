"""Synthetic provenance contracts; no parser, document or native process."""

import copy

import pytest
from pydantic import ValidationError

from app.ingestion.models import NormalizedExtraction


def extraction(format="pdf", kind="passage"):
    locations = {
        "pdf": {"format": "pdf", "precision": "exact", "pages": [2]},
        "xlsx": {
            "format": "xlsx",
            "precision": "exact",
            "sheet": "Sales",
            "cell_range": "B2:C3",
        },
        "csv": {
            "format": "csv",
            "precision": "exact",
            "record_start": 1,
            "record_end": 1,
            "line_start": 2,
            "line_end": 4,
            "columns": [
                {"position": 1, "name": "Value"},
                {"position": 2, "name": "Value"},
            ],
        },
    }
    return {
        "document_id": "document-1",
        "content_hash": "a" * 64,
        "filename": "synthetic." + format,
        "format": format,
        "extraction_id": "extraction-1",
        "extraction_version": "1",
        "normalization_version": "1",
        "units": [
            {
                "unit_id": "unit-1",
                "kind": kind,
                "text": "Café\n42",
                "method": "native",
                "parser": {"name": "synthetic", "version": "1"},
                "location": locations[format],
                "mappings": [
                    {
                        "start": 0,
                        "end": 7,
                        "source_unit_id": "raw-1",
                        "source_start": 0,
                        "source_end": 7,
                    }
                ],
            }
        ],
    }


@pytest.mark.parametrize("format", ["pdf", "xlsx", "csv"])
def test_passage_round_trip_preserves_identity_locations_and_unicode(format):
    source = extraction(format)
    model = NormalizedExtraction.model_validate(source)
    restored = NormalizedExtraction.model_validate_json(model.model_dump_json())
    assert restored == model
    assert restored.document_id == "document-1"
    assert restored.units[0].text == "Café\n42"
    assert restored.units[0].mappings[0].end == 7
    assert restored.units[0].location.format == format


@pytest.mark.parametrize("format", ["pdf", "xlsx", "csv"])
def test_table_round_trip_keeps_cell_relationships_and_locations(format):
    source = extraction(format, "table")
    unit = source["units"][0]
    if format == "pdf":
        unit["location"].update(
            precision="coarse", limitation="Table region unavailable"
        )
    unit.update(
        row_count=2,
        column_count=2,
        cells=[
            {
                "row": 1,
                "column": 1,
                "role": "header",
                "text": "Amount",
                "location": copy.deepcopy(unit["location"]),
            },
            {
                "row": 2,
                "column": 1,
                "role": "data",
                "text": None,
                "stored_type": "formula",
                "formula": "=SUM(B2:B3)",
                "warnings": ["CACHE_MISSING"],
                "location": copy.deepcopy(unit["location"]),
            },
        ],
    )
    model = NormalizedExtraction.model_validate(source)
    assert NormalizedExtraction.model_validate_json(model.model_dump_json()) == model
    assert model.units[0].cells[1].text is None
    assert model.units[0].cells[1].formula == "=SUM(B2:B3)"


def test_mixed_native_ocr_and_raw_confidence_are_preserved():
    source = extraction()
    ocr = copy.deepcopy(source["units"][0])
    ocr.update(
        unit_id="ocr-unit",
        method="ocr",
        parser={"name": "OCR", "version": "1"},
        confidence={"value": 84.5, "scale": "engine 0..100"},
        warnings=["OCR_UNVERIFIED"],
    )
    source["units"].append(ocr)
    model = NormalizedExtraction.model_validate(source)
    assert model.units[0].confidence is None
    assert model.units[1].confidence.value == 84.5
    assert model.units[1].method == "ocr"


def test_pdf_image_keeps_region_identity_without_semantic_claim():
    source = extraction(kind="image")
    source["units"][0]["location"]["region"] = {
        "x0": 0.0,
        "y0": 1.0,
        "x1": 50.0,
        "y1": 60.0,
    }
    model = NormalizedExtraction.model_validate(source)
    assert model.units[0].unit_id == "unit-1"
    assert model.units[0].location.region.x1 == 50.0
    assert NormalizedExtraction.model_validate_json(model.model_dump_json()) == model


@pytest.mark.parametrize(
    "change",
    [
        {"format": "txt"},
        {"content_hash": "bad"},
        {"extraction_id": ""},
        {"filename": ""},
        {"normalization_version": ""},
        {"unknown": True},
    ],
)
def test_invalid_document_metadata_is_rejected(change):
    source = extraction()
    source.update(change)
    with pytest.raises(ValidationError):
        NormalizedExtraction.model_validate(source)


@pytest.mark.parametrize(
    "location",
    [
        {"format": "pdf", "precision": "exact", "pages": [0]},
        {"format": "pdf", "precision": "exact", "pages": [True]},
        {"format": "pdf", "precision": "exact", "pages": [2, 2]},
        {"format": "pdf", "precision": "exact", "pages": []},
        {"format": "pdf", "precision": "coarse", "pages": [2]},
        {
            "format": "pdf",
            "precision": "unavailable",
            "pages": [2],
            "limitation": "unknown",
        },
        {
            "format": "pdf",
            "precision": "exact",
            "pages": [2],
            "region": {"x0": 10.0, "y0": 0.0, "x1": 5.0, "y1": 1.0},
        },
        {
            "format": "xlsx",
            "precision": "exact",
            "sheet": "Sales",
            "cell_range": "C3:B2",
        },
        {"format": "xlsx", "precision": "exact", "sheet": "Sales", "cell_range": "A0"},
        {
            "format": "xlsx",
            "precision": "exact",
            "sheet": "Sales",
            "cell_range": "XFE1",
        },
    ],
)
def test_bad_or_conflicting_location_is_rejected(location):
    source = extraction(location["format"])
    source["units"][0]["location"] = location
    with pytest.raises(ValidationError):
        NormalizedExtraction.model_validate(source)


def test_unknown_location_requires_reason_and_does_not_invent_coordinates():
    source = extraction()
    source["units"][0]["location"] = {
        "format": "pdf",
        "precision": "unavailable",
        "limitation": "Parser could not locate page",
    }
    model = NormalizedExtraction.model_validate(source)
    assert model.units[0].location.pages == ()


@pytest.mark.parametrize("field,value", [("end", 99), ("start", -1), ("source_end", 0)])
def test_invalid_text_mapping_is_rejected(field, value):
    source = extraction()
    source["units"][0]["mappings"][0][field] = value
    with pytest.raises(ValidationError):
        NormalizedExtraction.model_validate(source)


def test_duplicate_unit_identity_is_rejected():
    source = extraction()
    source["units"].append(copy.deepcopy(source["units"][0]))
    with pytest.raises(ValidationError):
        NormalizedExtraction.model_validate(source)


@pytest.mark.parametrize(
    "change",
    [
        {"record_end": 0},
        {"line_end": 1},
        {"line_end": None},
        {"columns": []},
        {"columns": [{"position": 1}, {"position": 1}]},
        {"columns": [{"position": True}]},
    ],
)
def test_invalid_csv_locations_are_rejected(change):
    source = extraction("csv")
    source["units"][0]["location"].update(change)
    with pytest.raises(ValidationError):
        NormalizedExtraction.model_validate(source)


@pytest.mark.parametrize("format", ["pdf", "xlsx", "csv"])
def test_unstructured_tables_require_disclosure(format):
    source = extraction(format, "table")
    unit = source["units"][0]
    if format == "pdf":
        unit["location"].update(precision="coarse", limitation="No region")
    with pytest.raises(ValidationError):
        NormalizedExtraction.model_validate(source)
    unit["structure_limitation"] = "Rows and columns unavailable"
    assert NormalizedExtraction.model_validate(source).units[0].cells == ()


def test_formula_cache_absence_requires_warning_and_merged_origin_survives():
    source = extraction("xlsx", "table")
    unit = source["units"][0]
    unit.update(
        row_count=1,
        column_count=1,
        cells=[
            {
                "row": 1,
                "column": 1,
                "role": "data",
                "text": None,
                "formula": "=1+1",
                "location": {
                    "format": "xlsx",
                    "precision": "exact",
                    "sheet": "Sales",
                    "cell_range": "C3",
                    "merged_origin": "B2",
                },
            }
        ],
    )
    with pytest.raises(ValidationError):
        NormalizedExtraction.model_validate(source)
    unit["cells"][0]["warnings"] = ["CACHE_MISSING"]
    model = NormalizedExtraction.model_validate(source)
    assert model.units[0].cells[0].location.merged_origin == "B2"
    assert NormalizedExtraction.model_validate_json(model.model_dump_json()) == model


@pytest.mark.parametrize(
    "change",
    [
        {"mappings": []},
        {"confidence": {"value": float("nan"), "scale": "raw"}},
        {"confidence": {"value": 90.0, "scale": "0..100"}},
        {
            "location": {
                "format": "csv",
                "precision": "unavailable",
                "limitation": "unknown",
            }
        },
    ],
)
def test_unit_metadata_contradictions_are_rejected(change):
    source = extraction()
    source["units"][0].update(change)
    with pytest.raises(ValidationError):
        NormalizedExtraction.model_validate(source)


def test_unknown_source_offsets_and_unmapped_text_are_explicit():
    source = extraction()
    unit = source["units"][0]
    unit["mappings"] = []
    unit["mapping_limitation"] = "No character alignment from parser"
    assert NormalizedExtraction.model_validate(source).units[0].mappings == ()


def test_pdf_region_cannot_be_assigned_to_multiple_pages():
    source = extraction()
    source["units"][0]["location"].update(
        pages=[1, 2],
        region={
            "x0": 0.0,
            "y0": 0.0,
            "x1": 1.0,
            "y1": 1.0,
        },
    )
    with pytest.raises(ValidationError):
        NormalizedExtraction.model_validate(source)


def test_exact_pdf_table_without_region_is_rejected_even_with_structure_limitation():
    source = extraction(kind="table")
    source["units"][0]["structure_limitation"] = "No structure"
    with pytest.raises(ValidationError):
        NormalizedExtraction.model_validate(source)


@pytest.mark.parametrize("cells", [[(1, 1), (1, 1)], [(2, 1)], [(1, 2)]])
def test_table_grid_rejects_duplicate_and_outside_cells(cells):
    source = extraction("xlsx", "table")
    unit = source["units"][0]
    unit.update(
        row_count=1,
        column_count=1,
        cells=[
            {
                "row": row,
                "column": col,
                "role": "data",
                "text": "42",
                "location": copy.deepcopy(unit["location"]),
            }
            for row, col in cells
        ],
    )
    with pytest.raises(ValidationError):
        NormalizedExtraction.model_validate(source)


def test_ocr_confidence_must_be_finite_on_ocr_unit():
    source = extraction()
    source["units"][0].update(
        method="ocr", confidence={"value": float("inf"), "scale": "raw"}
    )
    with pytest.raises(ValidationError):
        NormalizedExtraction.model_validate(source)
