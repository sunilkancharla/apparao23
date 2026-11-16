"""R1-L fake layout/protocol checks, including the R1-A regression suite."""

import ctypes
import struct
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))
import public_source_launcher as probe
from test_public_source_accounting import AccountingTests, VerdictTests  # noqa: F401


def raw(total=0, active=0):
    """Independent little-endian decoder fixture from reviewed Windows fields."""
    return struct.pack("<4q4I", 0, 0, 0, 0, 0, total, active, 0)


class LauncherTests(unittest.TestCase):
    """No real Windows handles or child launches in these tests."""

    def test_reviewed_x64_layouts(self):
        self.assertEqual(probe.layouts(), {
            "Accounting": 48, "Basic": 64, "Extended": 144,
            "Startup": 104, "Process": 24, "Port": 16})
        self.assertEqual(probe.Accounting.total.offset, 36)
        self.assertEqual(probe.Accounting.active.offset, 40)

    def test_independent_raw_and_typed_decoding_agree(self):
        self.assertEqual(probe.decode(raw(1, 1)), (1, 1))
        typed = probe.Accounting.from_buffer_copy(raw(1, 0))
        self.assertEqual((typed.total, typed.active), probe.decode(raw(1, 0)))
        self.assertEqual(ctypes.sizeof(probe.Accounting), 48)

    def test_wrong_length_or_layout_is_rejected(self):
        for value in (raw()[:-1], raw() + b"x"):
            with self.assertRaises(probe.Boundary):
                probe.decode(value)

    def test_stage_order_and_one_assignment_only(self):
        tracker = probe.Stages()
        tracker.add("baseline", raw())
        tracker.add("created", raw(), member=False)
        tracker.add("assigned", raw(1, 1), member=True)
        with self.assertRaises(probe.Boundary):
            tracker.add("assigned", raw(1, 1), member=True)

    def test_membership_ambiguity_prevents_resume(self):
        tracker = probe.Stages()
        tracker.add("baseline", raw())
        with self.assertRaises(probe.Boundary):
            tracker.add("created", raw(), member=True)
        self.assertEqual(tracker.records[-1]["stage"], "created")

    def test_extra_count_is_recorded_before_failure(self):
        tracker = probe.Stages()
        tracker.add("baseline", raw())
        tracker.add("created", raw(), member=False)
        with self.assertRaises(probe.Boundary):
            tracker.add("assigned", raw(2, 1), member=True)
        self.assertEqual(tracker.records[-1]["total"], 2)

    def test_deadline_memory_and_unknown_notifications_fail_closed(self):
        for elapsed, free, private in ((6, 2**34, 1), (0, 1, 1), (0, 2**34, 2**30)):
            with self.assertRaises(probe.Boundary):
                probe.guard(elapsed, free, private)
        self.assertFalse(probe.notification_ok([], 123))
        self.assertFalse(probe.notification_ok([{"key": 9, "value": 123}], 123))
        self.assertTrue(probe.notification_ok([{"key": 17, "value": 123}], 123))

    def test_handshake_wrong_pid_and_missing_identity_refused(self):
        self.assertFalse(probe.identity_ok({"pid": 1}, 2))
        self.assertFalse(probe.identity_ok({"pid": 1}, 1))
        self.assertTrue(probe.identity_ok({"pid": 1, "image_hash": "a" * 64}, 1))

    def test_wrong_layout_stops_before_kernel_or_worker_admission(self):
        with patch.object(probe, "layouts", return_value={}), patch.object(probe, "kernel") as api:
            with self.assertRaises(probe.Boundary):
                probe.run()
            api.assert_not_called()

    def test_real_controller_failure_path_with_fake_windows_calls(self):
        saved, closed = [], []

        class FakeKernel:
            def CreateJobObjectW(self, *args):
                return 3

            def SetInformationJobObject(self, *args):
                return 1

            def CreateIoCompletionPort(self, *args):
                return 4

            def QueryInformationJobObject(self, job, kind, value, size, length):
                if kind == 1:
                    value._obj.total = value._obj.active = 0
                    length._obj.value = 48
                return 1

            def CreateProcessW(self, *args):
                ctypes.set_last_error(5)
                return 0

            def GetQueuedCompletionStatus(self, *args):
                ctypes.set_last_error(258)
                return 0

            def CloseHandle(self, handle):
                closed.append(handle)
                return 1

        state = {"job_counts": {}, "observed_job_processes": 0}
        with (patch.object(probe, "kernel", return_value=FakeKernel()),
              patch.object(probe, "memory_snapshot", return_value={
                  "available_physical": 2**34, "controller_private": 1024}),
              patch.object(probe, "admission") as admit,
              patch.object(probe, "meter", return_value=state),
              patch.object(probe, "write", side_effect=lambda p, v: saved.append(dict(v)))):
            value = probe.control("synthetic-create-failure", 0)
        admit.assert_called_once()
        self.assertEqual(value["control_error"], "PermissionError")
        self.assertEqual(set(closed), {3, 4})
        self.assertEqual(saved[-1]["control_error"], "PermissionError")
        self.assertFalse(value["handle_close_succeeded"])


if __name__ == "__main__":
    unittest.main()
