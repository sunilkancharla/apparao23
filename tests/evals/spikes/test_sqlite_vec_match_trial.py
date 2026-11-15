"""Fake-only PartB contracts; never load the candidate DLL while connected."""

import contextlib
import copy
import io
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sqlite_vec_match_trial as trial


class MatchAuthorization(unittest.TestCase):
    """Real SQLite authorization for the exact query shape, without native loading."""

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.addCleanup(self.connection.close)
        self.connection.execute(
            "CREATE TABLE vec_index(embedding BLOB,k INTEGER,distance REAL)"
        )
        self.connection.executemany(
            "INSERT INTO vec_index VALUES (?,?,?)",
            [(b"synthetic", 2, 0.2), (b"synthetic", 2, 0.1), (b"excluded", 2, 0.0)],
        )
        self.connection.create_function("match", 2, lambda pattern, value: 1)
        self.callbacks = []

        def record(action, first, second, database, trigger):
            if action == sqlite3.SQLITE_FUNCTION:
                self.callbacks.append((second or first or "").lower())
            return trial.authorizer(action, first, second, database, trigger)

        self.connection.set_authorizer(record)

    def query(self):
        """Mirror the fixed native SELECT exactly; stub tests permission, not distance."""
        return self.connection.execute(
            "SELECT rowid,distance FROM vec_index WHERE embedding MATCH ? AND k=? AND rowid IN (?,?) ORDER BY distance",
            (b"synthetic query", 2, 1, 2),
        ).fetchall()

    def test_current_contract_authorizes_complete_match_statement(self):
        self.assertEqual(self.query(), [(2, 0.1), (1, 0.2)])
        self.assertEqual(set(self.callbacks), {"match"})

    def test_prior_contract_refuses_match_callback_before_stub(self):
        calls = []
        self.connection.create_function(
            "match", 2, lambda *args: calls.append(args) or 1
        )
        prior = [name for name in trial.CONTRACT["functions"] if name != "match"]
        with (
            patch.dict(trial.CONTRACT, {"functions": prior}),
            self.assertRaisesRegex(sqlite3.OperationalError, "not authorized.*MATCH"),
        ):
            self.query()
        self.assertEqual(set(self.callbacks), {"match"})
        self.assertEqual(calls, [])

    def test_forbidden_functions_stay_denied_with_match_allowed(self):
        executed = []
        names = ("vec_npy_file", "vec_static_blob_from_raw", "unapproved_match_helper")
        for name in names:
            self.connection.create_function(
                name, 1, lambda *args: executed.append(args) or 1
            )
        for name in (*names, "load_extension"):
            with self.assertRaisesRegex(sqlite3.OperationalError, "not authorized"):
                self.connection.execute(
                    "SELECT " + name + "(?)", ("synthetic",)
                ).fetchall()
        self.assertEqual(executed, [])
        self.assertTrue(set(names).issubset(self.callbacks))


def ready_meter():
    """A sealed-ready trial whose user waited several days before starting."""
    return {
        "status": "ready",
        "preparation_started_utc": "2020-01-01T00:00:00+00:00",
        "preparation_seconds": 725.0,
        "preparation_limit_seconds": 1800,
        "active_segment": None,
        "external_blocks": [],
        "execution_started": None,
        "execution_deadline": None,
        "limits": {"workers": 32, "tests": 16},
        "used": {"workers": 0, "tests": 0},
        "events": [],
    }


class ExternalPreparation(unittest.TestCase):
    """Prepaid blocks survive pauses without refunding or renewing native time."""

    def test_expired_block_keeps_full_debit_on_confirmed_stopped_resume(self):
        with tempfile.TemporaryDirectory(dir=trial.RUN) as root:
            state = ready_meter()
            state["status"] = "preparing"
            with patch.object(trial, "RUN", Path(root)):
                trial.base.save(Path(root) / "meter.json", state)
                with patch.object(trial.time, "monotonic", return_value=100):
                    trial.reserve_external_block(300)
                with patch.object(trial.time, "monotonic", return_value=1000):
                    trial.reserve_external_block(300, previous_work_stopped=True)
                    trial.check_external_block(trial.read_meter())
                saved = trial.read_meter()
            self.assertEqual(saved["preparation_seconds"], 1325)
            self.assertEqual(saved["external_blocks"][0]["status"], "closed_full_debit")
            self.assertEqual(saved["external_blocks"][1]["reserved_seconds"], 300)
            self.assertIsNone(saved["execution_started"])

    def test_expiry_and_missing_stop_confirmation_refuse_without_writes(self):
        state = ready_meter()
        state["status"] = "preparing"
        state["external_blocks"] = [
            {
                "id": 1,
                "reserved_seconds": 300,
                "started_monotonic": 100,
                "deadline_monotonic": 400,
                "status": "active",
            }
        ]
        with (
            patch.object(trial, "read_meter", return_value=state),
            patch.object(trial.time, "monotonic", return_value=400),
            patch.object(trial.base, "save") as save,
        ):
            with self.assertRaises(RuntimeError):
                trial.check_external_block(state)
            with self.assertRaises(RuntimeError):
                trial.reserve_external_block(300)
            save.assert_not_called()

    def test_exhaustion_native_epoch_and_internal_marker_cannot_be_reset(self):
        for field, value in (
            ("preparation_seconds", 1799),
            ("execution_started", 1),
            ("active_segment", {"unknown": True}),
            ("status", "ready"),
        ):
            state = ready_meter()
            state["status"] = "preparing"
            state[field] = value
            before = copy.deepcopy(state)
            with (
                patch.object(trial, "read_meter", return_value=state),
                patch.object(trial.base, "save") as save,
                self.assertRaises(RuntimeError),
            ):
                trial.reserve_external_block(300, previous_work_stopped=True)
            self.assertEqual(state, before)
            save.assert_not_called()

    def test_final_ready_closes_prepaid_block_before_human_wait(self):
        with tempfile.TemporaryDirectory(dir=trial.RUN) as root:
            state = ready_meter()
            state["status"] = "preparing"
            state["preparation_seconds"] = 300
            state["external_blocks"] = [
                {
                    "id": 1,
                    "reserved_seconds": 300,
                    "started_monotonic": 100,
                    "deadline_monotonic": 400,
                    "status": "active",
                }
            ]
            with (
                patch.object(trial, "RUN", Path(root)),
                patch.object(trial, "verify_seal"),
                patch.object(trial, "verify_assets"),
                patch.object(trial.time, "monotonic", side_effect=[150, 150, 150.1]),
            ):
                trial.base.save(Path(root) / "meter.json", state)
                trial.mark_ready()
                saved = trial.read_meter()
            self.assertEqual(saved["status"], "ready")
            self.assertEqual(saved["external_blocks"][0]["status"], "closed_full_debit")
            self.assertIsNone(saved["active_segment"])

    def test_native_epoch_cannot_start_with_unclosed_external_block(self):
        state = ready_meter()
        state["used"]["workers"] = 2
        state["external_blocks"] = [{"status": "active"}]
        with (
            patch.object(trial, "read_meter", return_value=state),
            patch.object(trial.base, "save") as save,
            self.assertRaises(RuntimeError),
        ):
            trial.start_execution()
        save.assert_not_called()


class StartupRegressions(unittest.TestCase):
    """Exercise the delayed-handoff and missing-startup-receipt defects first."""

    def test_ready_wait_does_not_spend_preparation_time(self):
        with tempfile.TemporaryDirectory(dir=trial.RUN) as root:
            with patch.object(trial, "RUN", Path(root)):
                trial.base.save(Path(root) / "meter.json", ready_meter())
                trial.charge("workers", 2, "User launcher/controller admission")
                state = trial.read_meter()
            self.assertEqual(state["used"]["workers"], 2)
            self.assertEqual(state["preparation_seconds"], 725.0)
            self.assertIsNone(state["execution_started"])

    def test_failed_attestation_records_no_worker_terminal_receipt(self):
        with tempfile.TemporaryDirectory(dir=trial.RUN) as root:
            with (
                patch.object(trial, "RUN", Path(root)),
                patch.object(trial, "verify_seal"),
                patch.object(trial, "Runner") as runner,
                patch("builtins.input", return_value=""),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                trial.base.save(Path(root) / "meter.json", ready_meter())
                trial.offline()
                summary = trial.json.loads((Path(root) / "summary.json").read_bytes())
                state = trial.read_meter()
                runner.assert_not_called()
            self.assertEqual(summary["status"], "stopped_no_automatic_retry")
            self.assertTrue(summary["teardown_verified"])
            self.assertEqual(summary["owned_workers_launched"], 0)
            self.assertEqual(state["status"], "closed")

    def test_real_exhaustion_and_uncertain_segment_refuse_before_epoch(self):
        for field, value in (
            ("preparation_seconds", 1800.001),
            ("preparation_seconds", float("nan")),
            ("active_segment", {"started_monotonic": 1, "reason": "interrupted"}),
        ):
            with self.subTest(field=field, value=value):
                state = ready_meter()
                state[field] = value
                with (
                    patch.object(trial, "read_meter", return_value=state),
                    patch.object(trial.base, "save") as save,
                    self.assertRaises(RuntimeError),
                ):
                    trial.charge("workers", 2, "must refuse")
                save.assert_not_called()

    def test_active_segment_accounts_work_and_refuses_lost_ownership(self):
        with tempfile.TemporaryDirectory(dir=trial.RUN) as root:
            state = ready_meter()
            state["status"] = "preparing"
            with patch.object(trial, "RUN", Path(root)):
                trial.base.save(Path(root) / "meter.json", state)
                with (
                    patch.object(trial.time, "monotonic", side_effect=[100, 105]),
                    trial.preparation_segment("five seconds synthetic work"),
                ):
                    self.assertIsNotNone(trial.read_meter()["active_segment"])
                saved = trial.read_meter()
                self.assertEqual(saved["preparation_seconds"], 730)
                self.assertIsNone(saved["active_segment"])
                saved["active_segment"] = {"started_monotonic": 0, "reason": "lost"}
                trial.base.save(Path(root) / "meter.json", saved)
                with (
                    self.assertRaises(RuntimeError),
                    trial.preparation_segment("must not renew"),
                ):
                    self.fail("An interrupted segment was resumed")

    def test_native_epoch_never_renews_and_rejects_clock_inconsistency(self):
        state = ready_meter()
        state["used"]["workers"] = 2
        saved = []
        with (
            patch.object(trial, "read_meter", side_effect=lambda: copy.deepcopy(state)),
            patch.object(trial.base, "save", side_effect=lambda _, s: saved.append(s)),
            patch.object(trial.time, "time", return_value=10000),
            patch.object(trial.time, "monotonic", return_value=100),
        ):
            trial.start_execution()
        state = saved[0]
        self.assertEqual(state["execution_deadline"], 12700)
        with (
            patch.object(trial, "read_meter", return_value=state),
            self.assertRaises(RuntimeError),
        ):
            trial.start_execution()
        for wall, monotonic in ((12700, 2800), (10020, 105), (9999, 99)):
            with (
                patch.object(trial.time, "time", return_value=wall),
                patch.object(trial.time, "monotonic", return_value=monotonic),
                self.assertRaises(RuntimeError),
            ):
                trial.check_epoch(state)

    def test_pre_worker_seal_failure_is_terminal_and_sanitized(self):
        with tempfile.TemporaryDirectory(dir=trial.RUN) as root:
            with (
                patch.object(trial, "RUN", Path(root)),
                patch.object(
                    trial, "verify_seal", side_effect=ValueError("private/path")
                ),
                patch.object(trial, "Runner") as runner,
                patch("builtins.input", return_value="OFFLINE"),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                trial.base.save(Path(root) / "meter.json", ready_meter())
                trial.offline()
                raw = (Path(root) / "summary.json").read_text()
                summary = trial.json.loads(raw)
                state = trial.read_meter()
                runner.assert_not_called()
            self.assertNotIn("private/path", raw)
            self.assertTrue(summary["receipt_persisted"])
            self.assertTrue(summary["teardown_verified"])
            self.assertEqual(state["status"], "closed")
            self.assertEqual(state["used"]["workers"], 2)
            self.assertIsNotNone(state["execution_started"])

    def test_terminal_and_attempted_allocations_never_overwrite(self):
        for marker in ("summary.json", "execution-attempt.json"):
            with tempfile.TemporaryDirectory(dir=trial.RUN) as root:
                marker_path = Path(root) / marker
                marker_path.write_text('{"prior":"preserve"}')
                with (
                    patch.object(trial, "RUN", Path(root)),
                    patch.object(trial, "Runner") as runner,
                    patch("builtins.input") as prompt,
                    contextlib.redirect_stdout(io.StringIO()) as output,
                ):
                    trial.base.save(Path(root) / "meter.json", ready_meter())
                    before = (Path(root) / "meter.json").read_bytes()
                    trial.offline()
                    self.assertEqual((Path(root) / "meter.json").read_bytes(), before)
                self.assertEqual(marker_path.read_text(), '{"prior":"preserve"}')
                self.assertNotIn("You may reconnect", output.getvalue())
                runner.assert_not_called()
                prompt.assert_not_called()

    def test_unsafe_output_root_is_not_read_or_written(self):
        with (
            patch.object(trial, "RUN", trial.ROOT / "docs"),
            patch.object(trial, "read_meter") as read,
            patch.object(trial.base, "save") as save,
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            trial.offline()
        read.assert_not_called()
        save.assert_not_called()
        self.assertNotIn("You may reconnect", output.getvalue())

    def test_complete_fake_schedule_persists_terminal_and_all_16_starts(self):
        import ocr_trial

        class FakeRunner:
            def __init__(self):
                self.launches = 0
                self.samples = []
                self.closed = False

            def run_request(self, *args):
                trial.charge("workers", 1, "Fake worker schedule reservation")
                self.launches += 1
                return {"fake": True}

            def close(self):
                self.closed = True

        runner = FakeRunner()
        with tempfile.TemporaryDirectory(dir=trial.RUN) as root:
            with (
                patch.object(trial, "RUN", Path(root)),
                patch.object(trial, "verify_seal"),
                patch.object(trial, "Runner", return_value=runner),
                patch.object(ocr_trial, "ensure_disconnected"),
                patch("builtins.input", return_value="OFFLINE"),
                contextlib.redirect_stdout(io.StringIO()) as output,
            ):
                trial.base.save(Path(root) / "meter.json", ready_meter())
                trial.offline()
                summary = trial.json.loads((Path(root) / "summary.json").read_bytes())
                state = trial.read_meter()
            self.assertTrue(runner.closed)
            self.assertEqual(runner.launches, 14)
            self.assertEqual(state["used"]["workers"], 16)
            self.assertEqual(summary["status"], "completed_pending_review_no_adoption")
            self.assertEqual(len(summary["crashes"]), 4)
            self.assertEqual(len(summary["measurements"]), 4)
            self.assertTrue(summary["receipt_persisted"])
            self.assertIn("You may reconnect", output.getvalue())

    def test_cleanup_failure_does_not_print_safe_reconnect(self):
        import ocr_trial

        runner = unittest.mock.Mock()
        runner.run_request.side_effect = RuntimeError("synthetic worker stop")
        runner.close.side_effect = RuntimeError("synthetic cleanup uncertainty")
        with tempfile.TemporaryDirectory(dir=trial.RUN) as root:
            with (
                patch.object(trial, "RUN", Path(root)),
                patch.object(trial, "verify_seal"),
                patch.object(trial, "Runner", return_value=runner),
                patch.object(ocr_trial, "ensure_disconnected"),
                patch("builtins.input", return_value="OFFLINE"),
                contextlib.redirect_stdout(io.StringIO()) as output,
            ):
                trial.base.save(Path(root) / "meter.json", ready_meter())
                trial.offline()
                summary = trial.json.loads((Path(root) / "summary.json").read_bytes())
            self.assertFalse(summary["teardown_verified"])
            self.assertNotIn("You may reconnect", output.getvalue())

    def test_failed_reservation_reports_unpersisted_attempt_gap(self):
        with tempfile.TemporaryDirectory(dir=trial.RUN) as root:
            state = ready_meter()
            state["preparation_seconds"] = 1801
            with (
                patch.object(trial, "RUN", Path(root)),
                patch("builtins.input") as prompt,
                contextlib.redirect_stdout(io.StringIO()),
            ):
                trial.base.save(Path(root) / "meter.json", state)
                trial.offline()
                summary = trial.json.loads((Path(root) / "summary.json").read_bytes())
            self.assertEqual(summary["launcher_controller_attempts"], 2)
            self.assertFalse(summary["launcher_controller_reserved"])
            self.assertTrue(summary["teardown_verified"])
            prompt.assert_not_called()


class RuntimeContracts(unittest.TestCase):
    """Check the exact approval, scope, resource and loading boundaries."""

    def test_run_id_refuses_old_absent_and_traversal(self):
        trial.check_run_id("sqlite-vec-runtime-03")
        for name in (
            "",
            "sqlite-vec-runtime-01",
            "sqlite-vec-runtime-02",
            "storage-baseline-01",
            "sqlite-vec-artifact-01",
            "../sqlite-vec-runtime-03",
        ):
            with self.assertRaises(ValueError):
                trial.check_run_id(name)

    def test_loader_disabled_on_success_and_error(self):
        class Connection:
            def __init__(self, fail):
                self.actions, self.fail = [], fail

            def enable_load_extension(self, value):
                self.actions.append(value)

            def load_extension(self, path):
                self.actions.append("load")
                if self.fail:
                    raise RuntimeError("synthetic load failure")

        for fail in (False, True):
            conn = Connection(fail)
            with (
                patch.object(trial, "verify_assets"),
                patch.object(trial, "require_offline_worker"),
            ):
                if fail:
                    with self.assertRaises(RuntimeError):
                        trial.load_dll(conn)
                else:
                    trial.load_dll(conn)
            self.assertEqual(conn.actions, [True, "load", False])

    def test_missing_or_wrong_assets_refuse_before_loading(self):
        class Connection:
            def enable_load_extension(self, value):
                raise AssertionError("loading enabled despite invalid identity")

        with (
            patch.object(trial, "require_offline_worker"),
            patch.object(
                trial, "verify_assets", side_effect=ValueError("wrong or missing asset")
            ),
            self.assertRaises(ValueError),
        ):
            trial.load_dll(Connection())

    def test_offline_gate_refuses_connected_preparation(self):
        with (
            patch.object(trial, "read_meter", return_value={"execution_started": None}),
            self.assertRaises(RuntimeError),
        ):
            trial.require_offline_worker()

    def test_authorizer_denies_attach_unknown_functions_and_unsafe_pragmas(self):
        conn = sqlite3.connect(":memory:")
        self.addCleanup(conn.close)
        conn.create_function("vec_npy_file", 1, lambda _: "must not run")
        conn.set_authorizer(trial.authorizer)
        self.assertEqual(conn.execute("SELECT abs(-2)").fetchone()[0], 2)
        for sql in (
            "ATTACH DATABASE ':memory:' AS other",
            "SELECT random()",
            "SELECT load_extension('x')",
            "SELECT vec_npy_file('x')",
            "PRAGMA journal_mode=OFF",
        ):
            with self.assertRaises(sqlite3.DatabaseError):
                conn.execute(sql)

    def test_ties_scope_and_candidate_completeness(self):
        eligible = {1: "b", 2: "a", 3: "c"}
        self.assertEqual(
            trial.rank_candidates([(1, 0.1), (2, 0.1), (3, 0.2)], eligible),
            [("a", 0.1), ("b", 0.1), ("c", 0.2)],
        )
        for rows in ([(99, 0)], [(1, 0.1)], [(1, 0.1), (1, 0.1), (3, 0.2)]):
            with self.assertRaises(ValueError):
                trial.rank_candidates(rows, eligible)

    def test_a_adapter_is_scoped_and_versioned_without_extension(self):
        with tempfile.TemporaryDirectory(dir=trial.RUN) as root:
            store = trial.Adapter(Path(root), "A")
            try:
                vector = [1.0] + [0.0] * 767
                store.add_document("own", b"synthetic own", "a", ["a"])
                store.add_document("other", b"synthetic other", "b", ["b"])
                store.add_chunk("a", "own", vector, trial.base.VERSION)
                store.add_chunk("b", "other", vector, trial.base.VERSION)
                self.assertEqual(
                    [r[0] for r in store.search("a", vector, trial.base.VERSION)], ["a"]
                )
                with self.assertRaises(ValueError):
                    store.search("a", vector, "changed-version")
                with self.assertRaises(ValueError):
                    store.remove_library("own")
            finally:
                store.close()

    def test_meter_does_not_reset_or_borrow_categories(self):
        state = {
            "limits": {"tests": 16},
            "used": {"tests": 16},
            "execution_started": None,
        }
        with self.assertRaises(RuntimeError):
            trial.check_charge(state, "tests", 1)
        with self.assertRaises(ValueError):
            trial.check_charge(state, "unknown", 1)

    def test_frozen_bytes_and_idempotent_identity_preserved(self):
        blobs, _, _ = trial.generated(32)
        with tempfile.TemporaryDirectory(dir=trial.RUN) as root:
            store = trial.Adapter(Path(root), "A")
            try:
                store.add_document("d", b"synthetic", "a", ["a"])
                store.add_frozen_chunk("c", "d", blobs[0], trial.base.VERSION)
                store.add_frozen_chunk("c", "d", blobs[0], trial.base.VERSION)
                self.assertEqual(
                    store.eligible("a", trial.base.VERSION), [("c", blobs[0])]
                )
                with self.assertRaises(ValueError):
                    store.add_frozen_chunk("c", "d", blobs[1], trial.base.VERSION)
            finally:
                store.close()

    def test_runner_actual_loop_uses_reviewed_memory_keys_and_owned_cleanup(self):
        from types import SimpleNamespace

        import ocr_trial

        def create(*args):
            process = args[-1]._obj
            process.process, process.thread = 101, 102
            return 1

        def exit_code(handle, output):
            output._obj.value = 0
            return 1

        closed = []
        kernel = SimpleNamespace(
            SetInformationJobObject=lambda *a: 1,
            CreateProcessW=create,
            AssignProcessToJobObject=lambda *a: 1,
            ResumeThread=lambda *a: 0,
            WaitForSingleObject=unittest.mock.Mock(side_effect=[0x102, 0, 0]),
            GetExitCodeProcess=exit_code,
            TerminateJobObject=lambda *a: 1,
            CloseHandle=closed.append,
        )
        runner = object.__new__(trial.Runner)
        runner.native = SimpleNamespace(
            kernel=kernel,
            check=lambda v: v,
            job=lambda *a, **kw: 2,
            accounting=lambda handle: {
                "total": 2 if handle == 1 else 1,
                "active": 1 if handle == 1 else 0,
            },
        )
        from appcontainer_preflight import ExtendedLimits

        runner.extended, runner.job, runner.launches = ExtendedLimits, 1, 0
        runner.sample = lambda: None
        with tempfile.TemporaryDirectory(dir=trial.RUN) as root:
            trial.base.save(Path(root) / "W01-result.json", {"fake": True})
            with (
                patch.object(trial, "RUN", Path(root)),
                patch.object(trial, "charge"),
                patch.object(
                    ocr_trial,
                    "process_memory",
                    return_value={"private_observed": 12, "working_peak": 34},
                ),
                patch.object(trial.time, "sleep"),
            ):
                result = runner.run_request("benchmark", "A", "32")
            self.assertEqual(result["peak_working_set"], 34)
            self.assertEqual(result["sampled_private_peak"], 12)
            self.assertEqual(closed, [102, 101, 2])


if __name__ == "__main__":
    from appcontainer_preflight import Native

    native = Native()
    handle = native.job(1, kill=False)
    native.check(
        native.kernel.AssignProcessToJobObject(
            handle, native.kernel.GetCurrentProcess()
        )
    )
    unittest.main()
