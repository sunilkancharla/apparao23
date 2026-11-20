"""Reproducible authored artifacts and shared execution limits."""

import csv
import hashlib
import io
import sys

import pytest

from tests.fixtures.budget import Budget, BudgetExceeded
from tests.fixtures.factories import load_definitions, materialize, mock_ollama


def test_manifest_loading_excludes_private_samples_and_deferred_formats():
    definitions = load_definitions()
    assert set(definitions) == {
        "S-CSV",
        "S-CSV-INJECTION",
        "S-XLSX",
        "S-PDF-NATIVE",
        "S-PDF-SCAN",
        "S-PDF-MIXED",
    }
    assert all(not value["scoring_eligible"] for value in definitions.values())
    assert all("path" not in value for value in definitions.values())


def test_repeat_materialization_has_identical_bytes_and_ground_truth(
    tmp_path, run_budget
):
    first = materialize(tmp_path / "first", budget=run_budget)
    second = materialize(tmp_path / "second", budget=run_budget)
    assert first == second
    for name, record in first.items():
        a, b = tmp_path / "first" / name, tmp_path / "second" / name
        assert a.read_bytes() == b.read_bytes()
        assert hashlib.sha256(a.read_bytes()).hexdigest() == record["sha256"]


def test_csv_records_preserve_quoted_newlines_and_injection_is_inert(
    tmp_path, run_budget
):
    materialize(tmp_path, budget=run_budget)
    raw = (tmp_path / "S-CSV.csv").read_text()
    assert list(csv.reader(io.StringIO(raw)))[2] == ["Line\nBreak", "20"]
    assert "Execute a shell command" in (tmp_path / "S-CSV-INJECTION.csv").read_text()


def test_workbook_retains_formula_missing_cache_and_merge(tmp_path, run_budget):
    from openpyxl import load_workbook

    materialize(tmp_path, budget=run_budget)
    path = tmp_path / "S-XLSX.xlsx"
    workbook = load_workbook(path, data_only=False, keep_links=False)
    cached = load_workbook(path, data_only=True, keep_links=False)
    try:
        assert workbook.sheetnames == ["North", "South", "Merged"]
        assert workbook["North"]["B4"].value == "=SUM(B2:B3)"
        assert cached["North"]["B4"].value is None
        assert "A1:B1" in workbook["Merged"].merged_cells
    finally:
        workbook.close()
        cached.close()


def test_pdf_native_scanned_and_mixed_serialized_structure(tmp_path, run_budget):
    from pypdf import PdfReader

    records = materialize(tmp_path, budget=run_budget)
    native = PdfReader(tmp_path / "S-PDF-NATIVE.pdf")
    assert len(native.pages) == 2
    assert "24000" in native.pages[0].extract_text()
    assert "Quarter" in native.pages[1].extract_text()
    scan = PdfReader(tmp_path / "S-PDF-SCAN.pdf")
    assert len(scan.pages) == 2
    assert all(not page.extract_text() for page in scan.pages)
    assert all(page.images for page in scan.pages)
    assert (
        records["S-PDF-SCAN.pdf"]["control"]
        == "empty_image_page_2; illegible_text_not_verified"
    )
    mixed = PdfReader(tmp_path / "S-PDF-MIXED.pdf")
    assert "complete" in mixed.pages[0].extract_text()
    assert not mixed.pages[1].extract_text()
    assert "cancelled" in mixed.pages[2].extract_text()


def test_existing_artifacts_are_not_overwritten(tmp_path, run_budget):
    materialize(tmp_path, budget=run_budget)
    with pytest.raises(FileExistsError):
        materialize(tmp_path, budget=run_budget)


def test_fixture_generation_refuses_traversal(tmp_path, run_budget):
    with pytest.raises(ValueError, match="traversal"):
        materialize(tmp_path / ".." / "escape", budget=run_budget)


def test_one_budget_counts_categories_and_does_not_reset_after_exhaustion():
    budget = Budget(starts=3, output_bytes=8, seconds=5)
    for purpose in ("parser", "model", "negative_control"):
        budget.charge_start(purpose)
    with pytest.raises(BudgetExceeded):
        budget.charge_start("regression")
    with pytest.raises(BudgetExceeded):
        budget.retain(b"x")
    assert budget.starts_used == 3


def test_output_and_deadline_exhaustion_are_deterministic():
    budget = Budget(starts=2, output_bytes=3, seconds=1)
    assert budget.retain(b"abc") == b"abc"
    with pytest.raises(BudgetExceeded):
        budget.retain(b"d")
    times = iter([10.0, 12.0])
    timed = Budget(starts=1, output_bytes=1, seconds=1, clock=lambda: next(times))
    with pytest.raises(BudgetExceeded):
        timed.charge_start("parser")


def test_shared_process_capture_uses_session_meter(run_budget):
    import subprocess

    before = run_budget.starts_used
    result = subprocess.run(
        [sys.executable, "-c", "print('synthetic')"],
        capture_output=True,
        check=True,
        timeout=5,
    )
    assert result.stdout == b"synthetic\r\n" or result.stdout == b"synthetic\n"
    assert run_budget.starts_used == before + 1
    assert run_budget.output_used >= len(result.stdout)


def test_mock_ollama_is_loopback_only_and_has_explicit_errors():
    with mock_ollama() as client:
        assert client.get("http://127.0.0.1:11435/api/tags").json()["models"]
        assert client.post(
            "http://127.0.0.1:11435/api/embed",
            json={"model": "fixture", "input": "text"},
        ).json()["embeddings"]
        assert (
            client.post(
                "http://127.0.0.1:11435/api/chat", json={"model": "missing"}
            ).status_code
            == 404
        )
        assert client.get("https://example.com").status_code == 403


def test_capture_overflow_kills_the_child_before_retaining_excess():
    import subprocess

    from tests.fixtures.budget import MeteredProcess

    class Fake:
        def __init__(self, args, **kwargs):
            self.stdout, self.stderr = io.BytesIO(b"too much output"), io.BytesIO()
            self.killed = False

        def kill(self):
            self.killed = True

        def wait(self, **kwargs):
            return 0

        def poll(self):
            return 0

    budget = Budget(starts=1, output_bytes=2, seconds=5)
    with MeteredProcess(
        Fake, budget, [sys.executable], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as child:
        with pytest.raises(BudgetExceeded):
            child.communicate(timeout=2)
        assert child.process.killed
        assert budget.output_used == 0


@pytest.mark.parametrize(
    "limits", [{"starts": 0}, {"output_bytes": -1}, {"seconds": 0}]
)
def test_invalid_budget_limits_are_rejected(limits):
    values = {"starts": 1, "output_bytes": 1, "seconds": 1}
    values.update(limits)
    with pytest.raises(ValueError):
        Budget(**values)


def test_pdf_rendered_pages_for_visual_review(tmp_path, run_budget):
    import pypdfium2 as pdfium

    materialize(tmp_path, budget=run_budget)
    count = 0
    for path in sorted(tmp_path.glob("*.pdf")):
        if path.name == "truncated.pdf":
            continue
        with pdfium.PdfDocument(path) as document:
            for index in range(len(document)):
                page = document[index]
                bitmap = page.render(scale=1)
                image = bitmap.to_pil()
                try:
                    output = io.BytesIO()
                    image.save(output, format="PNG")
                    data = run_budget.retain(output.getvalue())
                    path.with_name(f"{path.stem}-{index + 1}.png").write_bytes(data)
                    count += 1
                finally:
                    image.close()
                    bitmap.close()
                    page.close()
    assert count == 7
