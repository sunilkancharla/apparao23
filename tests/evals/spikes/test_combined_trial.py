"""Combined-budget/ownership contracts; no native OCR or model imports."""

import json
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import combined_native as native
import combined_trial as trial


class CombinedContracts(unittest.TestCase):
    """Exercise failure paths before allowing an offline handoff."""

    def ledger(self, root, **changes):
        state = trial.initial_state()
        state.update(changes)
        path = Path(root) / "meter.json"
        path.write_text(json.dumps(state), encoding="utf-8")
        return trial.Ledger(path, clock=lambda: 1000)

    def test_frozen_schedule_and_ocr_cycle(self):
        schedule = trial.schedule()
        self.assertEqual(len(schedule), 36)
        workers = [item for item in schedule if item["engine"]]
        self.assertEqual(len(workers), 24)
        self.assertEqual(
            [w["ocr_case"] for w in workers[:6]], ["M02", "M03", "M04"] * 2
        )
        self.assertEqual(len({item["id"] for item in schedule}), 36)
        self.assertEqual({item["case"] for item in schedule}, {"C01", "C03", "C08"})

    def test_scope_edits_do_not_change_selected_frozen_question_gold(self):
        frozen = [
            {
                "id": "C01",
                "question_id": "Q01",
                "question": "fixed question",
                "original_expected": {"value": 1},
            }
        ]
        questions = {
            "Q01": {"question": "fixed question", "expected": {"value": 1}},
            "unrelated": {"stage1_in_scope": False},
        }
        trial.reconcile_questions(frozen, questions)
        questions["Q01"]["expected"] = {"value": 2}
        with self.assertRaises(RuntimeError):
            trial.reconcile_questions(frozen, questions)

    def test_shared_categories_and_cleanup_reserve(self):
        with tempfile.TemporaryDirectory() as root:
            ledger = self.ledger(root)
            ledger.reserve("ocr", 28, "all OCR")
            with self.assertRaises(RuntimeError):
                ledger.reserve("ocr", 1, "extra OCR")
            for category in ("preparation", "controller", "supervisor", "report"):
                ledger.reserve(category, trial.CATEGORIES[category], category)
            self.assertEqual(ledger.read()["processes"], 144)
            with self.assertRaises(RuntimeError):
                ledger.reserve("cleanup", 1, "not teardown")
            ledger.reserve("cleanup", 1, "teardown", cleanup=True)

    def test_native_roots_and_descendants_are_not_double_charged(self):
        with tempfile.TemporaryDirectory() as root:
            ledger = self.ledger(root)
            ledger.reserve("controller", 1, "server", native=True)
            ledger.observe_native(2)  # root + discovery child
            ledger.reserve("ocr", 1, "OCR", native=True)
            ledger.observe_native(3)  # second root, same one extra child
            ledger.observe_native(3)
            self.assertEqual(ledger.read()["processes"], 3)
            self.assertEqual(ledger.read()["native_extra"], 1)

    def test_overshoot_is_saved_before_stop(self):
        with tempfile.TemporaryDirectory() as root:
            ledger = self.ledger(root)
            with self.assertRaises(RuntimeError):
                ledger.observe_native(200)
            self.assertEqual(ledger.read()["native_observed"], 200)
            self.assertEqual(ledger.read()["native_extra"], 200)

    def test_api_failures_count_and_restart_is_refused(self):
        with tempfile.TemporaryDirectory() as root:
            ledger = self.ledger(root)
            with self.assertRaises(RuntimeError):
                ledger.call()
            ledger.start()
            for _ in range(128):
                ledger.call()
            with self.assertRaises(RuntimeError):
                ledger.call()
            self.assertEqual(ledger.read()["calls"], 128)
            with self.assertRaises(RuntimeError):
                ledger.start()

    def test_no_reset_or_limit_drift(self):
        with tempfile.TemporaryDirectory() as root:
            ledger = self.ledger(root)
            ledger.reserve("preparation", 2, "test")
            self.assertEqual(trial.Ledger(ledger.path).read()["processes"], 2)
            state = ledger.read()
            state["limits"]["ocr"] = 100
            ledger.path.write_text(json.dumps(state))
            with self.assertRaises(RuntimeError):
                trial.Ledger(ledger.path)

    def test_memory_deadline_and_sampling_stops(self):
        good = {
            "available_physical": 4 * 1024**3,
            "controller_private": 512 * 1024**2,
            "owned_private": 8 * 1024**3,
            "peak_job": 8 * 1024**3,
        }
        trial.check_resources(good, 0.1)
        for key in ("controller_private", "owned_private", "peak_job"):
            with self.subTest(key=key), self.assertRaises(RuntimeError):
                trial.check_resources(good | {key: good[key] + 1}, 0.1)
        with self.assertRaises(RuntimeError):
            trial.check_resources(good | {"available_physical": 1}, 0.1)
        with self.assertRaises(RuntimeError):
            trial.check_resources(good, 0.251)
        with tempfile.TemporaryDirectory() as root:
            ledger = self.ledger(root, offline_started=1, execution_deadline=999)
            with self.assertRaises(RuntimeError):
                ledger.remaining()

    def test_overlap_and_teardown_cannot_be_assumed(self):
        self.assertEqual(trial.overlap((1, 4), (2, 3)), 1)
        self.assertEqual(trial.overlap((1, 2), (3, 4)), 0)
        self.assertFalse(trial.teardown_ok(1, True, True, False))
        self.assertFalse(trial.teardown_ok(0, True, False, False))
        self.assertFalse(trial.teardown_ok(0, True, True, True))
        self.assertTrue(trial.teardown_ok(0, True, True, False))

    def test_hash_path_and_missing_artifact_refusals(self):
        with tempfile.TemporaryDirectory() as root:
            directory = Path(root)
            path = directory / "fixture.png"
            path.write_bytes(b"test")
            expected = trial.digest(path)
            trial.verify_file(directory, "fixture.png", expected)
            for name, value in (
                ("../fixture.png", expected),
                ("https://invalid/a", expected),
                ("missing.png", expected),
                ("fixture.png", "0" * 64),
            ):
                with (
                    self.subTest(name=name),
                    self.assertRaises((OSError, RuntimeError, ValueError)),
                ):
                    trial.verify_file(directory, name, value)

    def test_model_residency_cpu_context_and_identity(self):
        names = [trial.EMBED, *list(trial.CHAT_MODELS)[:1]]
        models = [
            {
                "name": name,
                "digest": "sha256:" + trial.MODELS[name],
                "size_vram": 0,
                "context_length": 2048,
            }
            for name in names
        ]
        trial.validate_residency({"models": models}, names)
        for bad in (
            {"models": models[:1]},
            {"models": [models[0] | {"size_vram": 1}, models[1]]},
            {"models": [models[0] | {"context_length": 4096}, models[1]]},
            {"models": [models[0] | {"digest": "wrong"}, models[1]]},
        ):
            with self.assertRaises(RuntimeError):
                trial.validate_residency(bad, names)

    def test_header_event_and_actual_worker_interval(self):
        import threading

        event, interval = threading.Event(), []

        class FakeClient:
            @contextmanager
            def stream(self, *args, **kwargs):
                self_was_unset = not event.is_set()
                if not self_was_unset:
                    raise AssertionError("Event was set before headers")
                yield object()

        with native.StreamClient(FakeClient(), event, interval).stream(
            "POST", "/api/chat"
        ):
            self.assertTrue(event.is_set())
            self.assertEqual(len(interval), 1)
        self.assertEqual(len(interval), 2)
        with (
            tempfile.TemporaryDirectory() as root,
            patch.object(trial, "RUN", Path(root)),
        ):
            for name in ("requests", "raw"):
                (Path(root) / name).mkdir()
            trial.write_json(
                Path(root) / "raw/S01.json",
                {
                    "cer": 0,
                    "wer": 0,
                    "facts_exact": True,
                    "worker_started": 2,
                    "worker_ended": 3,
                },
            )
            supervisor = native.Supervisor.__new__(native.Supervisor)
            supervisor.runner = SimpleNamespace(run=lambda *a, **k: {"seconds": 1})
            result = supervisor.ocr_request("S01", "tesserocr", "M02")
            self.assertEqual(result["interval"], (2, 3))

    def test_remote_download_and_generate_inference_refused_before_transport(self):
        api = native.API.__new__(native.API)
        for method, path, body in (
            ("GET", "https://example.invalid/api/ps", None),
            ("POST", "/api/pull", {"model": trial.EMBED}),
            ("POST", "/api/embed", {"model": "unapproved"}),
            (
                "POST",
                "/api/generate",
                {"model": trial.EMBED, "prompt": "run", "keep_alive": 0},
            ),
        ):
            with self.subTest(path=path), self.assertRaises(ValueError):
                api.request(method, path, body)

    def test_failed_pair_keeps_local_evidence_and_reaps_thread(self):
        fake_chat = SimpleNamespace(
            request_body=lambda *args: {},
            chat_request=lambda *args, **kwargs: (_ for _ in ()).throw(
                RuntimeError("injected")
            ),
        )
        supervisor = SimpleNamespace(
            ledger=None,
            inference_threads=[],
            check_failure=lambda: None,
            fail=lambda reason: None,
        )
        with (
            tempfile.TemporaryDirectory() as root,
            patch.object(trial, "RUN", Path(root)),
        ):
            (Path(root) / "answers").mkdir()
            with (
                patch.dict("sys.modules", {"chat_trial": fake_chat}),
                self.assertRaises(RuntimeError),
            ):
                native.run_pair(
                    supervisor,
                    SimpleNamespace(client=None),
                    {
                        "id": "S01",
                        "engine": None,
                        "model": next(iter(trial.CHAT_MODELS)),
                    },
                    {"evidence": []},
                )
            result = json.loads((Path(root) / "answers/S01.json").read_bytes())
            self.assertEqual(result["answer"]["error_type"], "RuntimeError")
            self.assertFalse(result["thread_alive"])
            self.assertTrue(
                all(not thread.is_alive() for thread in supervisor.inference_threads)
            )

    def test_abort_never_terminates_a_reused_unrelated_pid(self):
        import threading

        for inside in (False, True):
            killed = []

            def membership(handle, job, result, inside=inside):
                result._obj.value = inside
                return True

            kernel = SimpleNamespace(
                TerminateJobObject=lambda *args: True,
                OpenProcess=lambda *args: 123,
                IsProcessInJob=membership,
                TerminateProcess=lambda *args, killed=killed: killed.append(args),
                CloseHandle=lambda *args: True,
            )
            supervisor = native.Supervisor.__new__(native.Supervisor)
            supervisor.native = SimpleNamespace(
                kernel=kernel, check=lambda value: value
            )
            supervisor.root_job = 1
            supervisor.server = SimpleNamespace(handle=2)
            supervisor.runner = SimpleNamespace(children=[42])
            supervisor.failure, supervisor.failed = None, threading.Event()
            supervisor.fail("injected")
            self.assertEqual(bool(killed), inside)


if __name__ == "__main__":
    unittest.main(verbosity=2)
