"""R1-I fake readback/ownership/deadline checks; no real worker launches."""

import struct
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import public_source_identity as subject
from test_public_source_accounting import AccountingTests, VerdictTests  # noqa: F401


def limits(active=1, flags=0x2308, memory=536870912):
    raw = bytearray(144)
    struct.pack_into("<I", raw, 16, flags)
    struct.pack_into("<I", raw, 40, active)
    struct.pack_into("<QQ", raw, 112, memory, memory)
    return bytes(raw)


class IdentityTests(unittest.TestCase):
    """Drive observation order and failure paths with fake APIs/clocks."""

    def test_effective_limits_required_before_admission(self):
        self.assertTrue(subject.limit_verdict(limits())["passed"])
        for raw in (limits(active=0), limits(flags=0x2000), limits(flags=0x3B08),
                    limits(memory=1), limits()[:-1]):
            self.assertFalse(subject.limit_verdict(raw)["passed"])

    def test_extra_identity_captured_before_count_rejection(self):
        events = []
        value = subject.observe_ready(2, 2, lambda: events.append("capture") or [1, 2])
        self.assertEqual(events, ["capture"])
        self.assertEqual(value["identities"], [1, 2])
        self.assertFalse(value["count_ok"])

    def test_ceiling_stops_without_identity_capture(self):
        events = []
        with self.assertRaises(subject.Boundary):
            subject.observe_ready(3, 3, lambda: events.append("forbidden"))
        self.assertEqual(events, [])

    def test_membership_failure_never_queries_image(self):
        events = []
        with self.assertRaises(subject.Boundary):
            subject.owned_identity(1, 2, lambda handle: False,
                                   lambda handle: events.append("image"), lambda handle: 1)
        self.assertEqual(events, [])

    def test_owned_identity_retains_creation_id_without_full_path(self):
        value = subject.owned_identity(1, 2, lambda handle: True,
                                       lambda handle: "C:/synthetic/example.exe",
                                       lambda handle: 123)
        self.assertEqual(value["image_name"], "example.exe")
        self.assertEqual(value["creation_id"], 123)
        self.assertNotIn("C:/", str(value))

    def test_capture_deadline_does_not_extend_control_deadline(self):
        with self.assertRaises(subject.Boundary):
            subject.capture_guard(1.3, 1.0, 5.0)
        with self.assertRaises(subject.Boundary):
            subject.capture_guard(5.1, 5.0, 5.0)

    def test_independent_deadline_calls_only_supplied_owned_termination(self):
        events = []
        guard = subject.Deadline(lambda: events.append("owned-only"), 5)
        guard.fire()
        self.assertTrue(guard.fired)
        self.assertEqual(events, ["owned-only"])
        guard.cancelled = True
        guard.fire()
        self.assertEqual(events, ["owned-only"])

    def test_deadline_failure_is_recorded_for_receipt(self):
        def fail():
            raise OSError("fake termination failure")
        guard = subject.Deadline(fail, 5)
        guard.fire()
        self.assertEqual(guard.error, "OSError")

    def test_truncated_or_duplicate_pid_list_is_rejected(self):
        for raw in (struct.pack("<II4Q", 3, 2, 1, 2, 0, 0),
                    struct.pack("<II4Q", 2, 2, 1, 1, 0, 0), b"short"):
            with self.assertRaises(subject.Boundary):
                subject.pid_list(raw)

    def test_identity_query_exception_stays_failure(self):
        def fail(handle):
            raise OSError("vanished process")
        with self.assertRaises(OSError):
            subject.owned_identity(1, 2, lambda handle: True, fail, lambda handle: 1)

    def test_exit_and_time_failures_cannot_be_accepted(self):
        value = {"control_error": None, "worker_exit": 0, "verdicts": {"all": True},
                 "watchdog": {"fired": False}, "normal_seconds": 1,
                 "cleanup_seconds": 0.1, "capture_seconds": 0.01}
        self.assertTrue(subject.accepted(value))
        for change in ({"worker_exit": 88}, {"normal_seconds": 6},
                       {"cleanup_seconds": 6}, {"capture_seconds": .3},
                       {"watchdog": {"fired": True}}, {"verdicts": {"count": False}}):
            self.assertFalse(subject.accepted(value | change))

    def test_incomplete_image_or_creation_identity_is_rejected(self):
        for name, created in (("", 1), ("image.exe", 0)):
            with self.assertRaises(subject.Boundary):
                subject.owned_identity(1, 2, lambda handle: True,
                                       lambda handle, n=name: n, lambda handle, t=created: t)


if __name__ == "__main__":
    unittest.main()
