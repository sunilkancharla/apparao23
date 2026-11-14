"""Offline-trial contracts with fake backends; never imports OCR/image packages."""

import hashlib
import json
import tempfile
import tomllib
import unittest
from enum import Enum
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import ocr_trial as trial


class OCRContracts(unittest.TestCase):
    """Test scope, provenance, budgets and scoring before any native execution."""

    def test_default_meter_reader_preserves_legacy_parse_and_errors(self):
        runner = object.__new__(trial.OwnedRunner)
        with tempfile.TemporaryDirectory() as root, patch.object(trial, "RUN", Path(root)):
            path = Path(root) / "meter.json"
            path.write_text(json.dumps({"execution_deadline_utc": "fixed"}), encoding="utf-8")
            self.assertEqual(runner.read_global_meter(), {"execution_deadline_utc": "fixed"})
            path.write_text("invalid", encoding="utf-8")
            with self.assertRaises(json.JSONDecodeError):
                runner.read_global_meter()
            path.unlink()
            with self.assertRaises(FileNotFoundError):
                runner.read_global_meter()

    def test_schedule_has_sixty_comparisons_and_twenty_controls(self):
        self.assertEqual(len(trial.comparison_schedule()), 60)
        self.assertEqual(len(trial.control_schedule()), 20)
        self.assertEqual(len(set(trial.comparison_schedule())), 60)

    def test_distribution_aliases_compare_as_the_same_pinned_package(self):
        self.assertEqual(trial.canonical_name("pdfminer.six"), "pdfminer-six")
        self.assertEqual(trial.canonical_name("PDFMINER__Six"), "pdfminer-six")
        baseline = {trial.canonical_name("pdfminer.six"): "20260107"}
        locked = {trial.canonical_name("pdfminer-six"): "20260107"}
        self.assertEqual(baseline, locked)

    def test_fresh_run_selection_does_not_reuse_stopped_directory(self):
        with patch.object(trial, "RUN"):
            trial.configure_run("manual-02")
            self.assertEqual(trial.RUN, trial.ROOT / "data/t09-manual-ocr/manual-02")
            trial.configure_run("manual-03")
            self.assertEqual(trial.RUN, trial.ROOT / "data/t09-manual-ocr/manual-03")
            trial.configure_run("manual-04")
            self.assertEqual(trial.RUN, trial.ROOT / "data/t09-manual-ocr/manual-04")
            with self.assertRaises(ValueError):
                trial.configure_run("../manual-01")

    def test_case_definitions_preserve_pdf_page_and_derivative_identity(self):
        cases = trial.case_definitions()
        self.assertEqual(len(cases), 10)
        self.assertEqual(cases[0]["page"], 1)
        self.assertEqual(cases[2]["source_method"], "ocr")
        self.assertIn("transform", cases[-1])
        self.assertNotEqual(cases[-1]["id"], cases[1]["id"])

    def test_fresh_continuation_reuses_only_exact_reviewed_project_and_versions(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            previous = root / "data/t09-manual-ocr/manual-02"
            previous.mkdir(parents=True)
            project = '[dependency-groups]\nocr-eval=[]\n[tool.uv]\nconstraint-dependencies=[]\n'
            (root / "pyproject.toml").write_text(project, encoding="utf-8")
            (previous / "proposed-pyproject.toml").write_text(project, encoding="utf-8")
            digest = hashlib.sha256((previous / "proposed-pyproject.toml").read_bytes()).hexdigest()
            (previous / "seal.json").write_text(json.dumps({
                str((previous / "proposed-pyproject.toml").relative_to(root)): digest}))
            (previous / "prepared-state.json").write_text(json.dumps({"baseline": {"base": "1"}}))
            inventory = {"new_wheels": [{"name": "fake", "version": "2"}]}
            with patch.object(trial, "ROOT", root), patch.object(trial, "RUN", root / "manual-03"):
                self.assertEqual(trial.offline_project(inventory, {"base": "1", "fake": "2"}), project)
                with self.assertRaises(RuntimeError):
                    trial.offline_project(inventory, {"base": "1", "fake": "3"})
                (root / "pyproject.toml").write_text(project + "# changed\n")
                with self.assertRaises(RuntimeError):
                    trial.offline_project(inventory, {"base": "1", "fake": "2"})

    def test_local_inputs_refuse_urls_escape_and_unsupported_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ("https://example.invalid/a.png", "../a.png", "private.xls"):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    trial.input_path(root, name)
            self.assertEqual(trial.input_path(root, "case.png"), root / "case.png")

    def test_shared_meter_cannot_reset_or_spend_cleanup_reserve(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "meter.json"
            path.write_text(json.dumps({"reserved": 230, "limit": 240, "events": []}))
            with self.assertRaises(RuntimeError):
                trial.charge(path, "too many", 1)
            self.assertEqual(json.loads(path.read_text())["reserved"], 230)

    def test_fake_adapter_retains_page_and_qualifies_empty_evidence(self):
        case = trial.case_definitions()[0]
        output = trial.evaluate(case, lambda: {"text": "", "boxes": [], "warnings": []})
        self.assertEqual(output["page"], case["page"])
        self.assertEqual(output["case_id"], case["id"])
        self.assertIn("no_recognized_text", output["warnings"])

    def test_digits_and_punctuation_are_not_normalized_away(self):
        self.assertEqual(trial.error_rates("Total 125.00", "Total 125.00"), (0, 0))
        cer, wer = trial.error_rates("Total 125.00", "Total 12500")
        self.assertGreater(cer, 0)
        self.assertGreater(wer, 0)

    def test_native_routing_skips_ocr_and_mixed_routing_keeps_order(self):
        calls = []
        pages = [("native", "known text"), ("ocr", ""), ("native", "more text")]
        routed = trial.route_pages(pages, lambda page: calls.append(page) or "recognized")
        self.assertEqual(calls, [2])
        self.assertEqual([item["page"] for item in routed], [1, 2, 3])
        self.assertEqual([item["method"] for item in routed], ["native", "ocr", "native"])

    def test_rapid_configuration_is_local_cpu_only_and_disables_classifier(self):
        enums = SimpleNamespace(
            OCRVersion=Enum("OCRVersion", {"PPOCRV4": "PP-OCRv4"}),
            ModelType=Enum("ModelType", {"MOBILE": "mobile"}),
            LangDet=Enum("LangDet", {"EN": "en"}),
            LangRec=Enum("LangRec", {"EN": "en"}),
            EngineType=Enum("EngineType", {"ONNXRUNTIME": "onnxruntime"}),
        )
        config = trial.rapid_settings(Path("F:/local/assets"), enums)
        for section, language in (("Det", enums.LangDet.EN), ("Rec", enums.LangRec.EN)):
            self.assertIs(config[f"{section}.ocr_version"], enums.OCRVersion.PPOCRV4)
            self.assertIs(config[f"{section}.model_type"], enums.ModelType.MOBILE)
            self.assertIs(config[f"{section}.engine_type"], enums.EngineType.ONNXRUNTIME)
            self.assertIs(config[f"{section}.lang_type"], language)
        self.assertFalse(config["Global.use_cls"])
        self.assertFalse(config["EngineConfig.onnxruntime.use_cuda"])
        self.assertEqual(config["EngineConfig.onnxruntime.intra_op_num_threads"], 1)
        self.assertTrue(config["Global.return_word_box"])
        self.assertTrue(config["Det.model_path"].endswith("en_PP-OCRv3_det_mobile.onnx"))

    def test_asset_hash_mismatch_stops_before_backend(self):
        with self.assertRaises(RuntimeError):
            trial.verify_blob(b"wrong", 5, "0" * 64)

    def test_pixel_guard_refuses_without_allocating_an_image(self):
        trial.validate_pixels(4000, 3000)
        with self.assertRaises(ValueError):
            trial.validate_pixels(4000, 3001)

    def test_negative_zero_exit_still_requires_expected_status(self):
        trial.validate_control("missing", {"status": "refused"}, False)
        trial.validate_control("deadline", None, True)
        with self.assertRaises(RuntimeError):
            trial.validate_control("wrong", {"status": "accepted"}, False)
        with self.assertRaises(RuntimeError):
            trial.validate_control("deadline", None, False)

    def test_proposed_group_preserves_python_baseline_and_pins(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "pyproject.toml").write_text(
                '[project]\nrequires-python=">=3.11"\n[dependency-groups]\n'
                'dev=[]\n[tool.uv]\npackage=false\n')
            with patch.object(trial, "ROOT", root):
                proposal = trial.offline_project({"new_wheels": [{"name": "fake", "version": "1"}]},
                                                  {"baseline": "2"})
            parsed = tomllib.loads(proposal)
            self.assertEqual(parsed["project"]["requires-python"], ">=3.11")
            self.assertIn("fake==1;", parsed["dependency-groups"]["ocr-eval"][0])
            self.assertEqual(parsed["tool"]["uv"]["constraint-dependencies"], ["baseline==2"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
