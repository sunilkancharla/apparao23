"""Fake-only PartB contracts; never load the candidate DLL while connected."""

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sqlite_vec_runtime as trial


class RuntimeContracts(unittest.TestCase):
    """Check the exact approval, scope, resource and loading boundaries."""

    def test_run_id_refuses_old_absent_and_traversal(self):
        trial.check_run_id("sqlite-vec-runtime-01")
        for name in (
            "",
            "storage-baseline-01",
            "sqlite-vec-artifact-01",
            "../sqlite-vec-runtime-01",
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
