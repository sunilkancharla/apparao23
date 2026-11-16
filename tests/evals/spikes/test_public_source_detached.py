"""R1-DT configuration and actual-controller fake-call regressions."""

import ctypes
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))
import public_source_detached as subject
import test_public_source_identity as previous
from test_public_source_accounting import AccountingTests, VerdictTests  # noqa: F401


class DetachedIdentityTests(previous.IdentityTests):
    """Run the12identity regressions against this successor, not the old module."""

    def setUp(self):
        binding = patch.object(previous, "subject", subject)
        binding.start()
        self.addCleanup(binding.stop)


class DetachedModeTests(unittest.TestCase):
    """Retain exact flags and verify the flag passed at the Windows boundary."""

    def test_exact_detached_suspended_unicode_flags(self):
        self.assertEqual(subject.creation_flags(), 0x0000040C)
        self.assertEqual(subject.creation_flags() & 0x01000000, 0)

    def test_console_breakaway_or_missing_required_flags_rejected(self):
        for value in (0x08000404, 0x40C | 0x10, 0x40C | 0x01000000, 8, 0x408, 0xC):
            with self.assertRaises(subject.Boundary):
                subject.creation_flags(value)

    def test_actual_controller_passes_detached_flags_without_launching(self):
        flags, closed, saved = [], [], []

        def query(job, kind, value, size, length):
            if kind == 9:
                value._obj.basic.flags, value._obj.basic.active = 0x2308, 1
                value._obj.process_memory = value._obj.job_memory = 536870912
                length._obj.value = 144
            elif kind == 1:
                value._obj.total = value._obj.active = 0
                length._obj.value = 48
            return 1

        def failed_create(*args):
            flags.append(args[5])
            ctypes.set_last_error(5)
            return 0

        def dequeue(*args):
            ctypes.set_last_error(258)
            return 0

        api = SimpleNamespace(
            OpenProcess=lambda *args: None, GetProcessTimes=lambda *args: 1,
            CreateJobObjectW=lambda *args: 3, SetInformationJobObject=lambda *args: 1,
            CreateIoCompletionPort=lambda *args: 4, QueryInformationJobObject=query,
            CreateProcessW=failed_create, GetQueuedCompletionStatus=dequeue,
            CloseHandle=lambda handle: closed.append(handle) or 1,
        )
        tick, frequency = ctypes.c_int64(), ctypes.c_int64()
        ctypes.windll.kernel32.QueryPerformanceCounter(ctypes.byref(tick))
        ctypes.windll.kernel32.QueryPerformanceFrequency(ctypes.byref(frequency))
        state = {"status": "ready", "direct_attempts": 0, "started_tick": tick.value,
                 "frequency": frequency.value, "seal": {}, "observed_associations": 0}
        with (tempfile.TemporaryDirectory() as directory,
              patch.object(subject, "RUN", Path(directory)),
              patch.object(subject, "read", return_value=state),
              patch.object(subject, "save", side_effect=lambda p, v: saved.append(dict(v))),
              patch.object(subject.prior, "kernel", return_value=api),
              patch.object(subject.prior, "memory_snapshot", return_value={
                  "available_physical": 2**34, "controller_private": 1024}),
              patch.object(subject, "Deadline", side_effect=lambda *args: SimpleNamespace(
                  fired=False, error=None, start=lambda: None, close=lambda: None))):
            subject.run()
        self.assertEqual(flags, [0x40C])
        self.assertEqual(set(closed), {3, 4})
        self.assertEqual(saved[-1]["status"], "stopped_no_retry")
        self.assertEqual(state["direct_attempts"], 1)


if __name__ == "__main__":
    unittest.main()
