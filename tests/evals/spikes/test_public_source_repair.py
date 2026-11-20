"""R1-S regression controls; no HTTP transport or candidate assets."""

import importlib.util
import json
import sys
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import public_source_review as old
from embedding_budget import NativeJob
from test_public_source_review import ReviewTests  # noqa: F401 -- include nine regression cases


class RegressionTests(unittest.TestCase):
    """Exercise the real stopped initializer and reused cleanup protocol."""

    def test_original_initializer_reproduces_missing_field(self):
        state = json.loads((old.RUN / "meter-startup-stop.json").read_text(
            encoding="utf-8-sig"))
        self.assertNotIn("pending_bytes", state)
        with self.assertRaisesRegex(KeyError, "pending_bytes"):
            old.collect(state, lambda: None, [b"x"], lambda: 0, 1)

    def test_original_close_protocol_reproduces_missing_callback(self):
        events = []

        def query(handle, kind, value, size, extra):
            value._obj.total = 1
            return True

        job = object.__new__(NativeJob)
        import ctypes

        class Accounting(ctypes.Structure):
            _fields_ = [("total", ctypes.c_uint32)]

        job.Accounting = Accounting
        job._mutex = threading.RLock()
        job.handle = 42
        job.accounted = 1
        job.budget = SimpleNamespace(reserve_processes=lambda count: None)
        job.kernel = SimpleNamespace(
            TerminateJobObject=lambda *args: events.append("terminate"),
            QueryInformationJobObject=query,
            CloseHandle=lambda *args: events.append("close"),
        )
        with self.assertRaisesRegex(AttributeError, "observe_native"):
            job.close()
        self.assertEqual(events, ["terminate", "close"])
        self.assertIsNone(job.handle)

    def test_successor_initializes_real_schema_and_complete_adapter(self):
        spec = importlib.util.spec_from_file_location(
            "repair", HERE / "public_source_repair.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        original = json.loads((old.RUN / "meter-startup-stop.json").read_text(
            encoding="utf-8-sig"))
        state = module.initial_state(original)
        self.assertNotIn("pending_bytes", original)
        self.assertEqual(old.collect(state, lambda: None, [b"x"], lambda: 0, 1), b"x")
        adapter = module.Reserved(lambda: None)
        adapter.reserve_processes(1)
        adapter.observe_native(1, reserved=1)
        with self.assertRaises(RuntimeError):
            adapter.observe_native(2, reserved=1)

    def test_cleanup_failure_still_reaps_and_persists_receipt(self):
        import public_source_repair as module

        events = []

        def fail():
            events.append("close")
            raise RuntimeError("accounting")

        child = SimpleNamespace(wait=lambda timeout: events.append("wait"),
                                poll=lambda: 7)
        result = {}
        module.finish(SimpleNamespace(close=fail), child, result,
                      lambda value: events.append(dict(value)))
        self.assertEqual(events[:2], ["close", "wait"])
        self.assertEqual(events[2]["cleanup_error"], "RuntimeError")
        self.assertTrue(events[2]["child_reaped"])


if __name__ == "__main__":
    unittest.main()
