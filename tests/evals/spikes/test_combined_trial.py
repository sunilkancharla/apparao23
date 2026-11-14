"""Combined-budget/ownership contracts; no native OCR or model imports."""

import json
import runpy
import sys
import tempfile
import unittest
from contextlib import contextmanager, nullcontext
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import combined_native as native
import combined_trial as trial


class CombinedContracts(unittest.TestCase):
    """Exercise failure paths before allowing an offline handoff."""

    def test_state_write_operation_diagnostics_and_last_good_bytes(self):
        for operation in ("write", "replace"):
            with (
                self.subTest(operation=operation),
                tempfile.TemporaryDirectory() as root,
            ):
                path = Path(root) / "summary.json"
                trial.write_json(path, {"version": 1})
                original = path.read_bytes()
                denied = PermissionError(13, "synthetic denial", str(path))
                target = (
                    patch.object(Path, "write_text", side_effect=denied)
                    if operation == "write"
                    else patch.object(trial.os, "replace", side_effect=denied)
                )
                with target, self.assertRaises(PermissionError) as caught:
                    trial.write_json(path, {"version": 2})
                diagnostic = trial.filesystem_diagnostic(caught.exception, Path(root))
                self.assertEqual(diagnostic["state_operation"], operation)
                self.assertEqual(diagnostic["state_role"], "summary")
                self.assertEqual(path.read_bytes(), original)
                self.assertNotIn(root, json.dumps(diagnostic))

    def test_failed_accounting_persistence_prevents_simulated_work(self):
        for action in ("reserve", "call"):
            with self.subTest(action=action), tempfile.TemporaryDirectory() as root:
                ledger = self.ledger(
                    root, offline_started=1000, execution_deadline=2000
                )
                original = ledger.path.read_bytes()
                work = []
                with (
                    patch.object(
                        trial.os, "replace", side_effect=PermissionError(13, "denied")
                    ),
                    self.assertRaises(PermissionError),
                ):
                    if action == "reserve":
                        ledger.reserve("controller", 1, "synthetic launch")
                    else:
                        ledger.call()
                    work.append("started")
                self.assertEqual(work, [])
                self.assertEqual(ledger.path.read_bytes(), original)
                self.assertTrue(ledger.path.with_suffix(".json.tmp").exists())
                with self.assertRaises(RuntimeError):
                    trial.Ledger(ledger.path)

    def coordinated_state_case(self, reader=False, same=True):
        """Gate actual file access while a second owned writer attempts the lock."""
        import threading

        with tempfile.TemporaryDirectory() as root:
            ledger = self.ledger(root)
            first = ledger.path
            second = first if same else Path(root) / "other.json"
            ready, release, attempted, done = (threading.Event() for _ in range(4))
            gate, errors = threading.RLock(), []
            replace, read_text = trial.os.replace, Path.read_text

            class TracedLock:
                def __enter__(self):
                    if threading.current_thread().name == "coord-second":
                        attempted.set()
                    gate.acquire()

                def __exit__(self, *args):
                    gate.release()

            def pause():
                ready.set()
                if not release.wait(2):
                    raise TimeoutError("Synthetic coordination gate")

            def controlled_replace(source, destination):
                if not reader and threading.current_thread().name == "coord-first":
                    pause()
                return replace(source, destination)

            def controlled_read(path, *args, **kwargs):
                if (
                    reader
                    and path == first
                    and threading.current_thread().name == "coord-first"
                ):
                    with path.open("r", encoding="utf-8-sig") as handle:
                        pause()
                        return handle.read()
                return read_text(path, *args, **kwargs)

            def run_first():
                try:
                    if reader:
                        ledger.read()
                    else:
                        trial.write_json(first, {"writer": 1})
                except (OSError, ValueError) as error:
                    errors.append(type(error).__name__)

            def run_second():
                try:
                    trial.write_json(second, {"writer": 2})
                except (OSError, ValueError) as error:
                    errors.append(type(error).__name__)
                finally:
                    done.set()

            first_thread = threading.Thread(
                target=run_first, name="coord-first", daemon=True
            )
            second_thread = threading.Thread(
                target=run_second, name="coord-second", daemon=True
            )
            with (
                patch.object(trial, "_MUTEX", TracedLock()),
                patch.object(trial.os, "replace", controlled_replace),
                patch.object(Path, "read_text", controlled_read),
            ):
                first_thread.start()
                try:
                    self.assertTrue(ready.wait(2))
                    second_thread.start()
                    self.assertTrue(attempted.wait(2))
                    self.assertFalse(done.is_set())
                finally:
                    release.set()
                    first_thread.join(2)
                    if second_thread.ident is not None:
                        second_thread.join(2)
            self.assertFalse(first_thread.is_alive())
            self.assertFalse(second_thread.is_alive())
            self.assertEqual(errors, [])
            self.assertEqual(json.loads(second.read_text()), {"writer": 2})

    def test_owned_same_and_distinct_destination_writers_are_serialized(self):
        self.coordinated_state_case(same=True)
        self.coordinated_state_case(same=False)

    def test_owned_reader_closes_before_writer_replaces(self):
        self.coordinated_state_case(reader=True)

    def test_descendant_noop_skips_replace_and_changed_count_persists(self):
        with tempfile.TemporaryDirectory() as root:
            ledger = self.ledger(root)
            with patch.object(trial, "write_json", wraps=trial.write_json) as writes:
                ledger.observe_native(3)
                first = ledger.read()
                with patch.object(trial.os, "replace", side_effect=PermissionError):
                    ledger.observe_native(3)
                self.assertEqual(first, ledger.read())
                self.assertEqual(writes.call_count, 1)
                ledger.observe_native(4)
            self.assertEqual(ledger.read()["processes"], 4)
            self.assertEqual(ledger.read()["native_observed"], 4)

    def test_highwater_change_without_extra_and_unchanged_overshoot(self):
        with tempfile.TemporaryDirectory() as root:
            ledger = self.ledger(root)
            ledger.reserve("controller", 1, "root", native=True)
            ledger.observe_native(1)
            ledger.reserve("controller", 1, "another root", native=True)
            ledger.observe_native(2)
            self.assertEqual(ledger.read()["native_observed"], 2)
            self.assertEqual(ledger.read()["native_extra"], 0)
            with self.assertRaises(RuntimeError):
                ledger.observe_native(200)

            with (
                patch.object(trial.os, "replace", side_effect=PermissionError),
                self.assertRaises(RuntimeError),
            ):
                ledger.observe_native(200)

    def test_changed_descendant_persistence_failure_keeps_last_good_state(self):
        with tempfile.TemporaryDirectory() as root:
            ledger = self.ledger(root)
            ledger.observe_native(3)
            original = ledger.path.read_bytes()
            with (
                patch.object(trial.os, "replace", side_effect=PermissionError),
                self.assertRaises(PermissionError),
            ):
                ledger.observe_native(4)
            self.assertEqual(ledger.path.read_bytes(), original)
            with self.assertRaises(RuntimeError):
                trial.Ledger(ledger.path)

    def test_combined_ocr_reader_binding_uses_ledger_and_short_storage_callbacks(self):
        events = []
        ledger = SimpleNamespace(read=lambda: {"source": "ledger"})
        supervisor = SimpleNamespace(
            check_failure=lambda: events.append("failure"),
            storage=lambda: events.append("storage"),
        )
        runner = native.make_ocr_runner(
            SimpleNamespace(OwnedRunner=object), ledger, supervisor
        )
        self.assertEqual(runner.read_global_meter(), {"source": "ledger"})
        runner.check_storage(full=True)
        self.assertEqual(events, ["failure", "storage"])

    @unittest.skipUnless(sys.platform == "win32", "Windows sharing-mode fixture")
    def test_owned_windows_reader_blocks_replace_until_handle_closed(self):
        import ctypes
        from ctypes import wintypes as w

        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.CreateFileW.argtypes = [
            w.LPCWSTR,
            w.DWORD,
            w.DWORD,
            ctypes.c_void_p,
            w.DWORD,
            w.DWORD,
            w.HANDLE,
        ]
        kernel.CreateFileW.restype = w.HANDLE
        kernel.CloseHandle.argtypes = [w.HANDLE]
        kernel.CloseHandle.restype = w.BOOL
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "summary.json"
            trial.write_json(path, {"version": 1})
            handle = kernel.CreateFileW(str(path), 0x80000000, 3, None, 3, 0x80, None)
            self.assertNotEqual(handle, ctypes.c_void_p(-1).value)
            try:
                with self.assertRaises(PermissionError) as caught:
                    trial.write_json(path, {"version": 2})
                self.assertEqual(json.loads(path.read_text()), {"version": 1})
                print(
                    json.dumps(
                        {
                            "fixture": "owned_no_delete_share_reader",
                            "winerror": caught.exception.winerror,
                            "errno": caught.exception.errno,
                        }
                    )
                )
            finally:
                self.assertTrue(kernel.CloseHandle(handle))
            trial.write_json(path, {"version": 2})
            self.assertEqual(json.loads(path.read_text()), {"version": 2})

            # Characterize the ordinary reader used by the polling code too.
            with path.open("r", encoding="utf-8") as reader:
                self.assertEqual(json.load(reader), {"version": 2})
                try:
                    trial.write_json(path, {"version": 3})
                except PermissionError as error:
                    self.assertEqual(json.loads(path.read_text()), {"version": 2})
                    outcome = {
                        "denied": True,
                        "winerror": error.winerror,
                        "errno": error.errno,
                    }
                else:
                    self.assertEqual(json.loads(path.read_text()), {"version": 3})
                    outcome = {"denied": False, "winerror": None, "errno": None}
            print(json.dumps({"fixture": "owned_standard_python_reader", **outcome}))
            trial.write_json(path, {"version": 4})
            self.assertEqual(json.loads(path.read_text()), {"version": 4})

    def test_state_error_roles_do_not_echo_untrusted_attributes(self):
        error = PermissionError(13, "private content")
        error.trial_state_operation = "private operation"
        error.trial_state_role = "private path"
        diagnostic = trial.filesystem_diagnostic(error, Path("."))
        self.assertIsNone(diagnostic["state_operation"])
        self.assertIsNone(diagnostic["state_role"])
        self.assertNotIn("private", json.dumps(diagnostic))

    def timed_supervisor(self, work=0.02, tcp=0, storage=0, cycles=1, delay=0):
        clock = SimpleNamespace(value=1.0)
        waits, phases, failures = [], [], []
        supervisor = object.__new__(native.Supervisor)
        supervisor.samples = []
        supervisor.resource_failure = None

        def advance(label, seconds):
            phases.append(label)
            clock.value += seconds

        def collect():
            advance("collection", work)
            return {
                "available_physical": 8 * 1024**3,
                "controller_private": 1,
                "owned_private": 2,
                "peak_job": 3,
            }

        def wait(seconds):
            waits.append(seconds)
            clock.value += seconds + delay

        supervisor.collect_resources = collect
        supervisor.server = SimpleNamespace(_check_tcp=lambda: advance("tcp", tcp))
        supervisor.storage = lambda: advance("storage", storage)
        supervisor.stop = SimpleNamespace(
            is_set=lambda: len(waits) >= cycles, wait=wait
        )
        supervisor.fail = failures.append
        return supervisor, clock, waits, phases, failures

    def test_work_aware_cadence_and_wait_cancellation(self):
        for work, expected in ((0.02, 0.08), (0.15, 0)):
            with self.subTest(work=work):
                supervisor, clock, waits, phases, failures = self.timed_supervisor(work)
                with patch.object(
                    native.time, "monotonic", lambda clock=clock: clock.value
                ):
                    supervisor.observe()
                self.assertEqual(failures, [])
                self.assertEqual(phases, ["collection", "tcp", "storage"])
                self.assertEqual(len(waits), 1)
                self.assertAlmostEqual(waits[0], expected)
                self.assertAlmostEqual(
                    supervisor.samples[0]["timing"]["collection_seconds"], work
                )

    def test_current_phase_and_reading_gap_failures_are_retained(self):
        for options, expected in (
            ({"work": 0.251}, "collection_seconds"),
            ({"tcp": 0.251}, "tcp_seconds"),
            ({"storage": 0.251}, "storage_seconds"),
            ({"work": 0.15, "tcp": 0.11}, "iteration_seconds"),
            ({"work": 0.02}, "reading_gap"),
        ):
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as root:
                supervisor, clock, waits, _phases, failures = self.timed_supervisor(
                    **options
                )
                if expected == "reading_gap":
                    supervisor.last_resource_at = clock.value - 0.249
                with (
                    patch.object(trial, "RUN", Path(root)),
                    patch.object(
                        native.time, "monotonic", lambda clock=clock: clock.value
                    ),
                ):
                    supervisor.observe()
                    receipt = json.loads(
                        (Path(root) / "resource-failure.json").read_text()
                    )
                self.assertIn(expected, receipt["violations"])
                self.assertEqual(receipt, supervisor.resource_failure)
                self.assertEqual(
                    set(receipt["collection_timestamps"]), {"started", "ended"}
                )
                self.assertEqual(len(failures), 1)
                self.assertEqual(waits, [])
                self.assertEqual(supervisor.samples, [])

    def test_late_wake_stops_before_another_collection(self):
        supervisor, clock, waits, phases, failures = self.timed_supervisor(
            cycles=2, delay=0.2
        )
        with (
            tempfile.TemporaryDirectory() as root,
            patch.object(trial, "RUN", Path(root)),
            patch.object(native.time, "monotonic", lambda: clock.value),
        ):
            supervisor.observe()
        self.assertEqual(phases, ["collection", "tcp", "storage"])
        self.assertEqual(len(waits), 1)
        self.assertEqual(len(failures), 1)
        self.assertIn("loop_start_gap", supervisor.resource_failure["violations"])

    def test_timing_edges_invalid_inputs_and_direct_first_sample(self):
        for key in (
            "loop_start_gap",
            "reading_gap",
            "collection_seconds",
            "tcp_seconds",
            "storage_seconds",
            "iteration_seconds",
        ):
            trial.check_timing({key: 0.25})
            with self.assertRaises(trial.ResourceBoundary):
                trial.check_timing({key: 0.250001})
            for invalid in (-0.1, float("inf"), float("nan")):
                with self.assertRaises((ValueError, trial.ResourceBoundary)):
                    trial.check_timing({key: invalid})
                with self.assertRaises(ValueError):
                    trial.cadence_wait(invalid)
        supervisor, clock, _, phases, _ = self.timed_supervisor(work=0.25)
        with patch.object(native.time, "monotonic", lambda: clock.value):
            supervisor.sample()
        self.assertEqual(phases, ["collection", "tcp", "storage"])
        self.assertEqual(supervisor.samples[0]["timing"]["reading_gap"], 0)
        self.assertEqual(supervisor.samples[0]["collection_started"], 1)
        self.assertEqual(supervisor.samples[0]["collection_ended"], 1.25)

    def test_backwards_collection_clock_is_not_a_successful_sample(self):
        supervisor, clock, waits, _, failures = self.timed_supervisor(work=-0.01)
        with patch.object(native.time, "monotonic", lambda: clock.value):
            supervisor.observe()
        self.assertEqual(len(failures), 1)
        self.assertEqual(waits, [])
        self.assertEqual(supervisor.samples, [])
        with self.assertRaises(ValueError):
            trial.check_timing({"untrusted text": 1})

    def test_timing_receipt_failure_remains_fail_closed(self):
        supervisor, clock, waits, _, failures = self.timed_supervisor(work=0.251)
        with (
            tempfile.TemporaryDirectory() as root,
            patch.object(trial, "RUN", Path(root)),
            patch.object(native.time, "monotonic", lambda: clock.value),
            patch.object(trial, "write_json", side_effect=PermissionError),
        ):
            supervisor.observe()
        self.assertEqual(len(failures), 1)
        self.assertEqual(waits, [])
        self.assertIn("collection_seconds", supervisor.resource_failure["violations"])

    def test_resource_guard_reports_each_exact_boundary_and_keeps_edges(self):
        edge = {
            "available_physical": 4 * 1024**3,
            "controller_private": 512 * 1024**2,
            "owned_private": 8 * 1024**3,
            "peak_job": 8 * 1024**3,
        }
        trial.check_resources(edge, 0.25)
        for field, value, reason in (
            ("available_physical", 4 * 1024**3 - 1, "available_physical"),
            ("controller_private", 512 * 1024**2 + 1, "controller_private"),
            ("owned_private", 8 * 1024**3 + 1, "owned_private"),
            ("peak_job", 8 * 1024**3 + 1, "peak_job"),
            ("sampling_gap", 0.250001, "sampling_gap"),
        ):
            with self.subTest(field=field):
                snapshot = {**edge, field: value, "secret": "must not escape"}
                with self.assertRaises(trial.ResourceBoundary) as raised:
                    trial.check_resources(
                        snapshot, value if field == "sampling_gap" else 0.25
                    )
                self.assertIn(reason, raised.exception.diagnostic["violations"])
                self.assertNotIn("secret", raised.exception.diagnostic["measurement"])

    def test_failed_resource_reading_is_durable_before_owned_teardown(self):
        snapshot = {
            "available_physical": 4 * 1024**3,
            "controller_private": 1,
            "owned_private": 2,
            "peak_job": 3,
            "secret": "private content",
        }
        supervisor = object.__new__(native.Supervisor)
        supervisor.samples = []
        with (
            tempfile.TemporaryDirectory() as root,
            patch.object(trial, "RUN", Path(root)),
        ):
            with self.assertRaises(trial.ResourceBoundary):
                supervisor.check_resource_sample(snapshot, 0.3)
            receipt = json.loads((Path(root) / "resource-failure.json").read_text())
            self.assertEqual(receipt, supervisor.resource_failure)
            self.assertEqual(receipt["violations"], ["sampling_gap"])
            self.assertEqual(receipt["measurement"]["sampling_gap"], 0.3)
            self.assertNotIn("private content", json.dumps(receipt))

    def test_resource_receipt_write_failure_still_stops(self):
        supervisor = object.__new__(native.Supervisor)
        snapshot = {
            "available_physical": 0,
            "controller_private": 1,
            "owned_private": 2,
            "peak_job": 3,
        }
        with (
            patch.object(trial, "write_json", side_effect=PermissionError),
            self.assertRaises(PermissionError),
        ):
            supervisor.check_resource_sample(snapshot, 0.1)
        self.assertEqual(
            supervisor.resource_failure["violations"], ["available_physical"]
        )

    def test_observer_saves_resource_packet_before_fail_closed_callback(self):
        import threading

        supervisor = object.__new__(native.Supervisor)
        supervisor.stop = threading.Event()
        snapshot = {
            "available_physical": 0,
            "controller_private": 1,
            "owned_private": 2,
            "peak_job": 3,
        }
        supervisor.sample = lambda gap: supervisor.check_resource_sample(snapshot, gap)
        failures = []
        with (
            tempfile.TemporaryDirectory() as root,
            patch.object(trial, "RUN", Path(root)),
        ):

            def fail(reason):
                receipt = json.loads((Path(root) / "resource-failure.json").read_text())
                self.assertEqual(receipt["violations"], ["available_physical"])
                failures.append(reason)

            supervisor.fail = fail
            supervisor.observe()
        self.assertEqual(
            failures, ["ResourceBoundary: Resource boundary: available_physical"]
        )

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

    def test_reused_ocr_poll_reads_same_deadline_and_stops_on_expiry(self):
        import ocr_trial as ocr

        clock = [1000]

        class ControlledDate(datetime):
            @classmethod
            def now(cls, tz=None):
                return datetime.fromtimestamp(clock[0], tz)

        with tempfile.TemporaryDirectory() as root:
            folder = Path(root)
            ledger = self.ledger(root)
            ledger.clock = lambda: clock[0]
            ledger.start()
            (folder / "receipts").mkdir()

            def exercise_poll():
                waits = [0]

                def wait(*args):
                    waits[0] += 1
                    return 258 if waits[0] == 1 else 0

                def create(*args):
                    process = args[-1]._obj
                    process.process, process.thread, process.pid = 1, 2, 42
                    return True

                def membership(handle, job, result):
                    result._obj.value = True
                    return True

                def attributes(pointer, count, flags, size):
                    size._obj.value = 8
                    return True

                def exit_code(handle, result):
                    result._obj.value = 0
                    return True

                kernel = SimpleNamespace(
                    SetInformationJobObject=lambda *a: True,
                    InitializeProcThreadAttributeList=attributes,
                    CreateProcessW=create,
                    AssignProcessToJobObject=lambda *a: True,
                    IsProcessInJob=membership,
                    ResumeThread=lambda *a: 0,
                    WaitForSingleObject=wait,
                    GetCurrentProcess=lambda: -1,
                    GetExitCodeProcess=exit_code,
                    TerminateJobObject=lambda *a: True,
                    CloseHandle=lambda *a: True,
                    DeleteProcThreadAttributeList=lambda *a: None,
                )
                runner = ocr.OwnedRunner.__new__(ocr.OwnedRunner)
                runner.native = SimpleNamespace(
                    kernel=kernel,
                    job=lambda *a: 3,
                    check=lambda value: value,
                    accounting=lambda *a: {"total": 1, "active": int(waits[0] < 2)},
                )
                runner.children, runner.controller_job = [], None
                runner.check_storage = lambda **kwargs: None
                reads = []

                def read_meter():
                    reads.append(True)
                    return ledger.read()

                runner.read_global_meter = read_meter
                with (
                    patch.object(ocr, "RUN", folder),
                    patch.object(ocr, "datetime", ControlledDate),
                    patch.object(ocr, "ensure_disconnected", lambda: None),
                    patch.object(ocr, "charge", lambda *a, **k: None),
                    patch.object(
                        ocr,
                        "process_memory",
                        lambda *a: {"private_observed": 1, "working_peak": 1},
                    ),
                ):
                    try:
                        return runner.run(["fake-owned-worker"], "contract")
                    finally:
                        self.assertTrue(
                            reads, "Actual OCR polling must use the reader hook"
                        )

            self.assertFalse(exercise_poll()["timed_out"])
            state = ledger.read()
            self.assertEqual(
                datetime.fromisoformat(state["execution_deadline_utc"]).timestamp(),
                state["execution_deadline"],
            )
            clock[0] = state["execution_deadline"] + 1
            with self.assertRaisesRegex(
                RuntimeError, "Shared offline execution/provisioning deadline"
            ):
                exercise_poll()
            with self.assertRaises(RuntimeError):
                ledger.remaining()

    def test_fresh_run_selection_and_sanitized_key_diagnostics(self):
        with patch.object(trial, "RUN"):
            trial.configure_run("combined-06")
            self.assertEqual(trial.RUN, trial.ROOT / "data/t11/combined-06")
            for name in (
                "combined-01",
                "combined-02",
                "combined-03",
                "combined-04",
                "combined-05",
                "../combined-06",
                "unapproved",
            ):
                with self.assertRaises(ValueError):
                    trial.configure_run(name)
        self.assertEqual(
            trial.state_error_field(KeyError("execution_deadline_utc")),
            "execution_deadline_utc",
        )
        self.assertIsNone(
            trial.state_error_field(KeyError("untrusted private content"))
        )

    def test_cli_and_lazy_native_adapter_share_the_selected_run(self):
        observed = []

        def observe(*args):
            observed.append(sys.modules["combined_trial"].RUN)

        stub = SimpleNamespace(offline_main=observe, worker=observe)
        for arguments in (
            ["offline", "combined-06"],
            ["worker", str(trial.ROOT / "data/t11/combined-06/requests/S01.json")],
        ):
            with (
                patch.dict(sys.modules, {"combined_native": stub}),
                patch.object(
                    sys, "argv", [str(trial.SPIKES / "combined_trial.py"), *arguments]
                ),
            ):
                runpy.run_path(
                    str(trial.SPIKES / "combined_trial.py"), run_name="__main__"
                )
        self.assertEqual(observed, [trial.ROOT / "data/t11/combined-06"] * 2)
        for arguments in (
            ["offline"],
            ["offline", "combined-03"],
            ["worker", str(trial.ROOT / "data/t11/combined-03/requests/S01.json")],
            ["offline", "combined-04"],
            ["worker", str(trial.ROOT / "data/t11/combined-04/requests/S01.json")],
            ["offline", "combined-05"],
            ["worker", str(trial.ROOT / "data/t11/combined-05/requests/S01.json")],
        ):
            with (
                patch.dict(sys.modules, {"combined_native": stub}),
                patch.object(
                    sys, "argv", [str(trial.SPIKES / "combined_trial.py"), *arguments]
                ),
                self.assertRaises((ValueError, SystemExit)),
            ):
                runpy.run_path(
                    str(trial.SPIKES / "combined_trial.py"), run_name="__main__"
                )
        self.assertEqual(len(observed), 2)

    def test_static_seal_inventory_covers_both_contract_suites(self):
        self.assertTrue(
            {"test_combined_trial.py", "test_ocr_trial.py"} <= set(trial.SEALED_SOURCES)
        )
        self.assertEqual(len(trial.SEALED_SOURCES), len(set(trial.SEALED_SOURCES)))
        self.assertTrue(
            all((trial.SPIKES / name).is_file() for name in trial.SEALED_SOURCES)
        )

    def test_live_scan_reproduces_atomic_rename_and_temp_removal_races(self):
        import os
        import threading

        from appcontainer_preflight import bounded_tree_bytes

        for atomic, live in (
            (True, False),
            (False, False),
            (True, True),
            (False, True),
        ):
            with (
                tempfile.TemporaryDirectory() as root,
                patch.object(trial, "RUN", Path(root)),
            ):
                folder = Path(root)
                for name in ("raw", "answers"):
                    (folder / name).mkdir()
                transient = folder / ("meter.json.tmp" if atomic else "worker-temp.bin")
                transient.write_bytes(b"synthetic")
                scanned, removed = threading.Event(), threading.Event()
                failures = []

                def fake_writer(scanned, removed, failures, atomic, transient, folder):
                    if not scanned.wait(2):
                        failures.append("scan coordination timeout")
                        removed.set()
                        return
                    try:
                        if atomic:
                            os.replace(transient, folder / "meter.json")
                        else:
                            transient.unlink()
                    finally:
                        removed.set()

                original_walk = os.walk

                def coordinated_walk(
                    *args,
                    original_walk=original_walk,
                    folder=folder,
                    transient=transient,
                    scanned=scanned,
                    removed=removed,
                    **kwargs,
                ):
                    for current, directories, files in original_walk(*args, **kwargs):
                        if Path(current) == folder and transient.name in files:
                            scanned.set()
                            if not removed.wait(2):
                                raise RuntimeError("writer coordination timeout")
                        yield current, directories, files

                writer = threading.Thread(
                    target=fake_writer,
                    args=(scanned, removed, failures, atomic, transient, folder),
                )
                writer.start()
                supervisor = native.Supervisor.__new__(native.Supervisor)
                try:
                    counter = (
                        nullcontext()
                        if live
                        else patch.object(
                            trial, "live_tree_bytes", bounded_tree_bytes, create=True
                        )
                    )
                    with (
                        patch("appcontainer_preflight.os.walk", coordinated_walk),
                        counter,
                    ):
                        if live:
                            supervisor.storage()
                            continue
                        try:
                            supervisor.storage()
                        except FileNotFoundError as error:
                            self.assertEqual(Path(error.filename), transient)
                            diagnostic = trial.filesystem_diagnostic(error, folder)
                            self.assertEqual(diagnostic["storage_area"], "run")
                            self.assertEqual(
                                diagnostic["source"]["function"], "bounded_tree_bytes"
                            )
                        else:
                            self.fail(
                                "Controlled disappearing entry was not reproduced"
                            )
                finally:
                    scanned.set()
                    writer.join(timeout=2)
                    self.assertFalse(writer.is_alive())
                    self.assertFalse(failures)

    def test_filesystem_diagnostics_keep_untrusted_paths_local(self):
        with tempfile.TemporaryDirectory() as root:
            directory = Path(root)
            error = FileNotFoundError(
                2, "private exception content", str(directory / "private-document")
            )
            public = trial.record_filesystem_error(error, directory)
            serialized = json.dumps(public)
            self.assertNotIn("private", serialized)
            self.assertNotIn(str(directory), serialized)
            self.assertTrue(public["local_detail_saved"])
            local = json.loads((directory / "filesystem-error-local.json").read_bytes())
            self.assertEqual(local["filename"], error.filename)

    def test_live_count_preserves_cap_and_required_directory_checks(self):
        with tempfile.TemporaryDirectory() as root:
            directory = Path(root)
            (directory / "nested").mkdir()
            (directory / "first.bin").write_bytes(b"1234")
            (directory / "nested/second.bin").write_bytes(b"567")
            self.assertEqual(trial.live_tree_bytes(directory, 7), 7)
            with self.assertRaises(RuntimeError):
                trial.live_tree_bytes(directory, 6)
            with self.assertRaises(FileNotFoundError):
                trial.live_tree_bytes(directory / "absent", 7)
            with self.assertRaises(RuntimeError):
                trial.live_tree_bytes(directory / "first.bin", 7)

    def test_live_walk_vanishing_child_does_not_hide_other_failures(self):
        with tempfile.TemporaryDirectory() as root:
            directory = Path(root)
            (directory / "data.bin").write_bytes(b"1234")
            errors = [
                FileNotFoundError(2, "gone", str(directory / "removed")),
                PermissionError(13, "denied", str(directory / "denied")),
                FileNotFoundError(2, "root gone", str(directory)),
                FileNotFoundError(2, "outside", str(directory.parent / "outside")),
            ]
            for index, error in enumerate(errors):

                def walk(path, *, onerror, error=error, **kwargs):
                    onerror(error)
                    yield str(path), [], ["data.bin"]

                with patch.object(trial.os, "walk", walk):
                    if index == 0:
                        self.assertEqual(trial.live_tree_bytes(directory, 4), 4)
                    else:
                        with self.assertRaises(type(error)):
                            trial.live_tree_bytes(directory, 4)

    def test_live_scan_does_not_ignore_root_removed_during_scan(self):
        with tempfile.TemporaryDirectory() as root:
            directory = Path(root)
            required = directory / "required"
            required.mkdir()

            def walk(*args, **kwargs):
                yield str(required), [], []
                required.rmdir()

            with (
                patch.object(trial.os, "walk", walk),
                self.assertRaises(FileNotFoundError),
            ):
                trial.live_tree_bytes(required, 1)

    def test_storage_quota_permission_and_reparse_guards_still_stop(self):
        import stat

        with (
            tempfile.TemporaryDirectory() as root,
            patch.object(trial, "RUN", Path(root)),
        ):
            directory = Path(root)
            for name in ("raw", "answers"):
                (directory / name).mkdir()
            target = directory / "synthetic.bin"
            target.write_bytes(b"data")
            original_lstat = Path.lstat

            for mode in ("quota", "permission", "reparse"):

                def inspect(path, mode=mode):
                    if path == target:
                        if mode == "permission":
                            raise PermissionError(13, "injected", str(path))
                        return SimpleNamespace(
                            st_mode=stat.S_IFREG,
                            st_size=513 * 1024**2,
                            st_file_attributes=0x400 if mode == "reparse" else 0,
                        )
                    return original_lstat(path)

                supervisor = native.Supervisor.__new__(native.Supervisor)
                with (
                    patch.object(Path, "lstat", inspect),
                    self.assertRaises(
                        PermissionError if mode == "permission" else RuntimeError
                    ),
                ):
                    supervisor.storage()

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
