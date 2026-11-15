"""Fake-only admission/accounting/verdict regressions; no trial workers."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import public_source_accounting as subject


def result(name="success"):
    """Provide independent cleanup/count/error observations for a valid control."""
    return {"name": name, "worker_exit": 0 if name == "success" else 7,
            "kernel_total": 1, "active_after_cleanup": 0,
            "child_reaped": True, "handle_close_succeeded": True,
            "cleanup_error": None if name == "success" else "InjectedAccountingError",
            "control_error": None}


class AccountingTests(unittest.TestCase):
    """Use real temporary receipts and fake time/process observations only."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "ledger.json"
        self.clock = 0.0
        self.ledger = subject.Ledger.create(
            self.path, limit=8, protected=2, seconds=10,
            clock=lambda: self.clock)

    def test_every_tool_shell_and_child_category_is_charged(self):
        units = {"orchestration": 1, "nested_tool": 1, "shell": 1, "executable": 1}
        self.ledger.reserve("test", units)
        self.assertEqual(self.ledger.read()["normal_charged"], 4)
        self.assertEqual(self.ledger.read()["events"][0]["units"], units)

    def test_failed_action_keeps_reservation_and_retry_cannot_reuse_label(self):
        self.ledger.reserve("failed-command", {"executable": 1})
        with self.assertRaises(subject.Boundary):
            self.ledger.reserve("failed-command", {"executable": 1})
        self.assertEqual(self.ledger.read()["normal_charged"], 1)

    def test_exhaustion_preserves_stop_allowance(self):
        self.ledger.reserve("all-normal", {"executable": 6})
        with self.assertRaises(subject.Boundary):
            self.ledger.reserve("too-many", {"shell": 1})
        self.ledger.reserve("cleanup", {"shell": 2}, stop=True)
        state = self.ledger.read()
        self.assertEqual((state["normal_charged"], state["stop_charged"]), (6, 2))
        self.assertEqual(state["status"], "stopped")

    def test_terminal_states_block_normal_admission_even_with_no_workers(self):
        for status in ("closed", "stopped", "exhausted", "unknown"):
            state = self.ledger.read()
            state["status"] = status
            self.path.write_text(json.dumps(state))
            with self.assertRaises(subject.Boundary):
                self.ledger.reserve("must-not-run", {"shell": 1})
        self.assertEqual(self.ledger.read()["normal_charged"], 0)

    def test_deadline_blocks_work_but_allows_stopped_cleanup(self):
        self.clock = 11
        with self.assertRaises(subject.Boundary):
            self.ledger.reserve("late", {"shell": 1})
        self.ledger.reserve("stop", {"shell": 1}, stop=True)
        self.assertEqual(self.ledger.read()["stop_charged"], 1)

    def test_unexpected_descendant_is_persisted_and_charged_before_stop(self):
        self.ledger.reserve("child", {"executable": 1})
        with self.assertRaises(subject.Boundary):
            self.ledger.observe("child", 2)
        state = json.loads(self.path.read_text())
        self.assertEqual(state["observations"]["child"], 2)
        self.assertEqual(state["normal_charged"], 2)
        self.assertEqual(state["status"], "stopped")

    def test_discovery_overrun_is_not_hidden_or_refunded(self):
        self.ledger.reserve("child", {"executable": 6})
        with self.assertRaises(subject.Boundary):
            self.ledger.observe("child", 7)
        self.assertEqual(self.ledger.read()["normal_charged"], 7)
        self.assertTrue(self.ledger.read()["overrun"])

    def test_repeat_observation_does_not_double_charge(self):
        self.ledger.reserve("child", {"executable": 1})
        self.ledger.observe("child", 1)
        self.ledger.observe("child", 1)
        self.assertEqual(self.ledger.read()["normal_charged"], 1)

    def test_invalid_units_and_existing_ledger_are_rejected(self):
        for units in ({"typo": 1}, {"shell": -1}, {"shell": True}, {}):
            with self.assertRaises(subject.Boundary):
                self.ledger.reserve("invalid", units)
        with self.assertRaises(FileExistsError):
            subject.Ledger.create(self.path)

    def test_cleanup_survives_accounting_exception_and_persists(self):
        saved = []

        def broken():
            raise subject.InjectedAccountingError("fake accounting")

        receipt = subject.finish(
            close=lambda: True, reap=lambda: True, active=lambda: 0,
            account=broken, persist=lambda value: saved.append(dict(value)))
        self.assertEqual(saved[0], receipt)
        self.assertTrue(receipt["handle_close_succeeded"])
        self.assertEqual(receipt["cleanup_error"], "InjectedAccountingError")
        self.assertEqual(receipt["active_after_cleanup"], 0)

    def test_cleanup_step_failure_does_not_skip_other_steps_or_receipt(self):
        events = []

        def broken_close():
            raise OSError("fake close failure")

        receipt = subject.finish(
            close=broken_close, reap=lambda: events.append("reap") or True,
            active=lambda: events.append("query") or 0,
            account=lambda: events.append("account"),
            persist=lambda value: events.append("persist"))
        self.assertEqual(events, ["reap", "query", "account", "persist"])
        self.assertIsNone(receipt["handle_close_succeeded"])
        self.assertEqual(receipt["handle_close_succeeded_error"], "OSError")

    def test_persistence_failure_propagates_without_claiming_success(self):
        def broken_persist(value):
            raise OSError("fake disk failure")

        with self.assertRaises(OSError):
            subject.finish(close=lambda: True, reap=lambda: True, active=lambda: 0,
                           account=lambda: None, persist=broken_persist)

    def test_unknown_and_decreasing_observations_do_not_change_state(self):
        self.ledger.reserve("child", {"executable": 1})
        self.ledger.observe("child", 1)
        before = self.path.read_bytes()
        for label, total in (("unknown", 2), ("child", 0), ("child", True)):
            with self.assertRaises(subject.Boundary):
                self.ledger.observe(label, total)
        self.assertEqual(self.path.read_bytes(), before)

    def test_terminal_closed_state_cannot_spend_cleanup_reserve(self):
        state = self.ledger.read()
        state["status"] = "closed"
        self.path.write_text(json.dumps(state))
        with self.assertRaises(subject.Boundary):
            self.ledger.reserve("cleanup", {"shell": 1}, stop=True)


class VerdictTests(unittest.TestCase):
    """Second-control failure must never produce a successful pair."""

    def test_expected_pair_passes(self):
        self.assertTrue(subject.pair_complete([result(), result("forced-failure")]))

    def test_second_wrong_exit_or_error_or_name_blocks_success(self):
        for changes in ({"worker_exit": 0}, {"cleanup_error": None},
                        {"cleanup_error": "RuntimeError"}, {"control_error": "OSError"},
                        {"name": "success"}):
            second = result("forced-failure") | changes
            self.assertFalse(subject.pair_complete([result(), second]))

    def test_cleanup_and_count_verdicts_are_independent(self):
        verdict = subject.verdict(result() | {"kernel_total": 2}, "success")
        self.assertTrue(verdict["cleanup_ok"])
        self.assertFalse(verdict["count_ok"])
        self.assertFalse(verdict["passed"])

    def test_unknown_or_failed_cleanup_and_incomplete_pair_fail_closed(self):
        for field in ("handle_close_succeeded", "child_reaped", "active_after_cleanup"):
            value = result()
            value.pop(field)
            self.assertFalse(subject.verdict(value, "success")["passed"])
        self.assertFalse(subject.pair_complete([result()]))
        self.assertFalse(subject.pair_complete([]))
        self.assertFalse(subject.pair_complete([result(), result("forced-failure"), result()]))


if __name__ == "__main__":
    unittest.main()
