"""Fake-only stage and boundary controls; no Windows handle APIs are invoked."""

import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import receipt_persistence_review as review


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.events = []

    def test_success_publishes_only_after_replace(self):
        target = review.save_case(
            self.root, "baseline", {"counter": 1}, self.events.append
        )
        self.assertEqual(json.loads(target.read_text()), {"counter": 1})
        self.assertEqual(self.events[-1]["stage"], "replace_target")
        self.assertEqual(self.events[-1]["status"], "success")
        self.assertFalse(target.with_suffix(".pending").exists())

    def test_every_stage_failure_is_named_and_retains_target(self):
        for stage in review.STAGES:
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as name:
                root = Path(name)
                directory = review.case_directory(root, "locked")
                target = directory / "target.json"
                target.write_bytes(b'{"counter":0}')
                events = []
                error = PermissionError(13, "private-path-never-recorded")
                error.winerror = 32

                def fail(failure=error):
                    raise failure

                with self.assertRaises(review.StageFailure) as caught:
                    review.save_case(
                        root, "locked", {"counter": 1}, events.append, {stage: fail}
                    )
                self.assertEqual(caught.exception.stage, stage)
                self.assertEqual(target.read_bytes(), b'{"counter":0}')
                failed = [e for e in events if e["status"] == "failure"]
                self.assertEqual(failed[0]["stage"], stage)
                self.assertEqual(failed[0]["winerror"], 32)
                self.assertNotIn("private-path", json.dumps(events))
                self.assertFalse(
                    any(
                        e["stage"] == "replace_target" and e["status"] == "success"
                        for e in events
                    )
                )

    def test_existing_pending_is_never_replaced_or_removed(self):
        directory = review.case_directory(self.root, "stale")
        (directory / "target.pending").write_bytes(b"retain-pending")
        (directory / "target.json").write_bytes(b"retain-target")
        with self.assertRaises(review.StageFailure) as caught:
            review.save_case(self.root, "stale", {"counter": 1}, self.events.append)
        self.assertEqual(caught.exception.stage, "open_temp")
        self.assertEqual((directory / "target.pending").read_bytes(), b"retain-pending")
        self.assertEqual((directory / "target.json").read_bytes(), b"retain-target")

    def test_diagnostic_failure_stops_before_publication(self):
        def fail(packet):
            raise OSError("journal unavailable")

        with self.assertRaises(review.DiagnosticFailure):
            review.save_case(self.root, "baseline", {"counter": 1}, fail)
        self.assertFalse((self.root / "cases/baseline/target.json").exists())

    def test_bad_case_reparse_and_body_size_refused(self):
        for name in ("../outside", "unknown", "/absolute"):
            with self.assertRaises(ValueError):
                review.save_case(self.root, name, {}, self.events.append)
        with (
            patch.object(review, "is_reparse", return_value=True),
            self.assertRaises(ValueError),
        ):
            review.case_directory(self.root, "baseline")
        with self.assertRaises(ValueError):
            review.save_case(
                self.root, "baseline", {"text": "x" * 8192}, self.events.append
            )

    def guard(self, **overrides):
        state = {"status": "active", "started_utc": time.time()}
        state.update(overrides)
        (self.root / "meter.json").write_text(json.dumps(state))
        return review.Guard(self.root)

    def test_closed_and_expired_epoch_refused(self):
        for overrides in ({"status": "closed"}, {"started_utc": time.time() - 1201}):
            guard = self.guard(**overrides)
            with self.assertRaises(ValueError):
                guard.check()

    def test_attempts_are_precharged_and_capped(self):
        guard = self.guard()
        seen = []
        guard.attempts = 130
        guard.begin("stale", seen.append)
        self.assertEqual(guard.attempts, 131)
        self.assertEqual(seen[0]["stage"], "attempt")
        with self.assertRaises(ValueError):
            guard.begin("stale", seen.append)

    def test_output_cap_and_worker_claim_refuse(self):
        guard = self.guard()
        with (
            patch.object(guard, "tree_bytes", return_value=2 * 1024**2),
            self.assertRaises(ValueError),
        ):
            guard.check()
        guard.claim()
        with self.assertRaises(FileExistsError):
            guard.claim()

    def test_append_only_journal_contains_scalar_metadata(self):
        guard = self.guard()
        with review.Journal(guard) as journal:
            guard.begin("baseline", journal)
            review.save_case(self.root, "baseline", {"counter": 1}, journal)
        entries = [
            json.loads(line)
            for line in (self.root / "operations.jsonl").read_text().splitlines()
        ]
        self.assertEqual(entries[0]["attempt"], 1)
        self.assertEqual(entries[-1]["status"], "success")
        self.assertNotIn(str(self.root), json.dumps(entries))

    def test_handle_is_closed_if_reporting_fails_after_open(self):
        guard = self.guard()

        def record(packet):
            if packet["stage"] == "handle_open":
                raise OSError("synthetic reporting failure")

        with patch.object(review.ctypes, "WinDLL") as factory:
            factory.return_value.CreateFileW.return_value = 123
            factory.return_value.CloseHandle.return_value = True
            with self.assertRaises(review.DiagnosticFailure):
                review.execute_probe(guard, record)
            factory.return_value.CloseHandle.assert_called_once_with(123)


if __name__ == "__main__":
    unittest.main()
