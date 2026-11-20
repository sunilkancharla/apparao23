"""CSV cells retain decoded values and actual logical/physical source anchors."""

import io

import pytest

from app.ingestion.csv import CsvExtractor
from app.ingestion.validation import UploadError


def extract(body):
    parser = CsvExtractor(io.BytesIO(body), "synthetic-extraction")
    return list(parser), parser


def test_quoted_commas_and_multiline_records_keep_positional_provenance():
    units, parser = extract(b'Name,Units\n"Apex, West",10\n"Line\nBreak",20\n')
    assert parser.record_count == 2 and parser.unit_count == 4
    assert [u.text for u in units] == ["Apex, West", "10", "Line\nBreak", "20"]
    unit = units[2]
    assert unit.location.record_start == unit.location.record_end == 2
    assert (unit.location.line_start, unit.location.line_end) == (3, 4)
    assert unit.location.columns[0].position == 1
    assert unit.cells[0].role == "header" and unit.cells[0].text == "Name"
    assert unit.cells[0].location.line_start == 1
    assert unit.cells[0].location.record_start is None
    assert unit.cells[0].location.precision == "coarse"
    assert unit.cells[1].text == "Line\nBreak"
    assert unit.mapping_limitation
    assert [u.unit_id for u in units] == [
        u.unit_id
        for u in extract(b'Name,Units\n"Apex, West",10\n"Line\nBreak",20\n')[0]
    ]


def test_duplicate_empty_and_absent_headers_are_not_invented_or_merged():
    units, parser = extract(b"Value,Value,\na,b,c,d\n")
    assert [u.location.columns[0].position for u in units] == [1, 2, 3, 4]
    assert [u.cells[0].text for u in units] == ["Value", "Value", "", None]
    assert {"DUPLICATE_HEADERS", "BLANK_HEADERS", "ROW_WIDTH_MISMATCH"} <= set(
        parser.warnings
    )
    assert "MISSING_HEADER" in units[-1].warnings


def test_missing_values_are_distinct_from_explicit_empty_fields_and_blank_records():
    units, parser = extract(b"A,B\n1,\n2\n\n3,4\n")
    assert parser.record_count == 4
    assert units[1].cells[1].text == ""
    assert units[3].cells[1].text is None
    assert units[3].location.precision == "coarse"
    assert units[4].location.record_start == 3 and units[4].location.line_start == 4
    assert "MISSING_CELL" in units[4].warnings
    assert "ROW_WIDTH_MISMATCH" not in units[-1].warnings


def test_bom_crlf_and_formula_like_text_remain_inert_and_unmodified():
    units, _ = extract(b'\xef\xbb\xbfLabel,Value\r\n"one\r\ntwo",=1+1\r\n')
    assert units[0].text == "one\r\ntwo"
    assert (units[0].location.line_start, units[0].location.line_end) == (2, 3)
    assert units[1].text == "=1+1" and units[1].cells[1].formula is None
    assert all(u.method == "native" and u.parser.name == "python.csv" for u in units)


@pytest.mark.parametrize(
    "body,code",
    [
        (b"", "INVALID_CSV"),
        (b"A,B\n", "EMPTY_CSV"),
        (b"A,B\n,\n", "EMPTY_CSV"),
        (b'a,b\n"broken', "INVALID_CSV"),
        (b"a,b\n\xff,x", "INVALID_CSV"),
        (b"a,b\n\x00,x", "INVALID_CSV"),
    ],
)
def test_empty_or_invalid_input_has_safe_explicit_errors(body, code):
    with pytest.raises(UploadError, match=code):
        extract(body)
