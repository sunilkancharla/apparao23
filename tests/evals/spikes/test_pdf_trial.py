"""Assertions for the bounded T05 experiment, not application acceptance tests."""

import sys
from pathlib import Path

import pytest
from pdf_trial import run_limited
from pdf_trial_fixtures import make_fixtures


def test_benchmark_refuses_outputs_outside_data():
    """The experiment cannot write raw document output outside ignored project data."""
    from pdf_trial import benchmark

    with pytest.raises(ValueError, match="data"):
        benchmark(Path(__file__).parent)


def test_worker_timeout_and_network_boundary():
    """A stalled child is terminated; an external socket is denied by this sandbox."""
    result = run_limited(
        [sys.executable, "-c", "input(); import time; time.sleep(20)"], 0.2
    )
    assert result["status"] == "timeout"
    result = run_limited(
        [
            sys.executable,
            "-c",
            "input(); import socket\ntry: socket.create_connection(('1.1.1.1',443),2)\nexcept OSError as e: print(e.winerror)",
        ],
        5,
    )
    assert result["status"] == "ok"
    assert result["stdout"].strip() == "10013"


def test_memory_boundary():
    """The Windows job refuses an allocation exceeding the 2 GiB committed limit."""
    result = run_limited([sys.executable, "-c", "input(); x=bytearray(3*1024**3)"], 10)
    assert result["status"] == "error"


@pytest.mark.parametrize("candidate", ["pypdf", "pdfplumber"])
def test_fixture_provenance_and_rejections(tmp_path, candidate):
    """Golden native facts/pages survive; blank/image and protected errors stay distinct."""
    from pdf_trial import parse_limited

    fixtures = make_fixtures(tmp_path)
    result = parse_limited(candidate, fixtures["native"], [1, 2, 3, 4, 5])
    assert result["status"] == "ok", result
    pages = result["payload"]["pages"]
    assert result["payload"]["page_count"] == 5
    assert "Project Cedar budget: 24000 units." in pages[0]["text"]
    assert [p["page"] for p in pages] == [1, 2, 3, 4, 5]
    assert pages[2]["kind"] == "empty_no_raster_image"
    assert pages[3]["kind"] == "image_without_native_text"
    assert pages[1]["images"]
    assert "Q1" in pages[1]["text"] and "160" in pages[1]["text"]
    # The stream draws entire left column first; inspect the right-column anchor too.
    assert pages[4]["text"].index("Left A") < pages[4]["text"].index("Left B")
    assert "Right A" in pages[4]["text"]
    if candidate == "pdfplumber":
        table = pages[1]["tables"][0]
        assert table["rows"] == [["Quarter", "Revenue"], ["Q1", "100"], ["Q2", "160"]]
        assert table["bbox"] == [50, 92, 250, 182]
        assert pages[1]["images"][0]["bbox"] == [300, 92, 360, 152]
    else:
        assert pages[1]["tables"] == []
        assert "page_only_geometry" in pages[1]["warnings"]
    for key in ["protected", "malformed", "truncated", "wrong_extension"]:
        rejected = parse_limited(candidate, fixtures[key], [1])
        assert rejected["status"] == "ok"
        assert rejected["payload"]["error"] in {
            "protected",
            "invalid_pdf",
            "invalid_extension",
        }
