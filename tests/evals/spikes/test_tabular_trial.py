"""T07 trial assertions; no product ingestion or model behavior is claimed."""

import json
from pathlib import Path

import pytest
from tabular_trial import parse_limited
from tabular_trial_fixtures import make_fixtures


@pytest.mark.parametrize("candidate", ["openpyxl", "xml"])
def test_workbook_values_and_safe_failures(tmp_path, candidate):
    """Cell anchors, merges and missing caches survive; unsafe archives fail closed."""
    files = make_fixtures(tmp_path)
    result = parse_limited(candidate, files["xlsx"])
    assert result["status"] == "ok", result
    data = result["payload"]
    assert "error" not in data, data
    sheets = {s["name"]: s for s in data["sheets"]}
    assert sheets["North"]["cells"]["B2"]["value"] == 120
    assert sheets["South"]["cells"]["B2"]["value"] == 50
    assert sheets["North"]["cells"]["B4"]["value"] is None
    assert sheets["North"]["cells"]["B4"]["formula"] == "SUM(B2:B3)"
    assert "missing_formula_cache:North!B4" in data["warnings"]
    assert sheets["Merged"]["merges"] == ["A1:B1"]
    assert sheets["Merged"]["cells"]["A1"]["value"] == "Sales"
    assert sheets["North"]["cells"]["C2"]["value"] == "2026-02-15T00:00:00"
    assert data["external_relationships"] == 1
    for key in ["corrupt", "traversal", "entity", "duplicate", "oversized"]:
        rejected = parse_limited(candidate, files[key])
        assert rejected["status"] == "ok", rejected
        assert rejected["payload"]["error"] in {
            "invalid_archive",
            "unsafe_xml",
            "archive_budget",
        }


def test_csv_records_injection_and_rejections(tmp_path):
    """Physical spans and raw strings survive; hostile content remains ordinary data."""
    files = make_fixtures(tmp_path)
    result = parse_limited("csv", files["csv"])
    assert result["status"] == "ok", result
    rows = result["payload"]["records"]
    assert rows[0]["values"] == ["Apex, West", "10"]
    assert rows[1] == {
        "data_record": 2,
        "source_row": 3,
        "lines": [3, 4],
        "values": ["Line\nBreak", "20"],
    }
    hostile = parse_limited("csv", files["injection"])["payload"]
    assert hostile["records"][0]["values"][2] == "12000"
    assert "99999" in hostile["records"][1]["values"][2]
    assert hostile["records"][0]["lines"] == [2, 2]
    for key in ["bad_encoding", "bad_quotes", "bad_headers", "long_field"]:
        result = parse_limited("csv", files[key])
        assert result["status"] == "ok", result
        assert result["payload"]["error"] in {"invalid_csv", "invalid_encoding"}


def test_definition_files_remain_non_scoring():
    """This extraction spike cannot enable the future application quality scores."""
    questions = json.loads(Path("tests/evals/questions.json").read_text())
    assert all(not q["scoring_eligible"] for q in questions["questions"])


def test_duplicate_archive_rejected(tmp_path):
    """Reject ambiguity before any worksheet parser consumes duplicate ZIP members."""
    files = make_fixtures(tmp_path)
    result = parse_limited("xml", files["duplicate"])
    assert result["status"] == "ok", result
    assert result["payload"].get("error") == "invalid_archive"
