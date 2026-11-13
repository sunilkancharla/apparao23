"""Focused synthetic policy tests; no trial processes are launched."""

import unittest
from pathlib import Path

import python_startup_diagnostic as diagnostic


class DiagnosticPolicyTests(unittest.TestCase):
    """Require fixed cases, safe environments and conservative observations."""

    def test_exact_schedule(self):
        self.assertEqual(diagnostic.schedule(), [(row, source) for row in "ABCD"
                                                for source in ("original", "staged")])

    def test_environment_never_inherits_secrets(self):
        env = diagnostic.environment("A", Path("F:/Python/Python314"),
                                     Path("F:/safe/work"), "C:/Windows")
        self.assertEqual(set(env), {"SystemRoot", "WINDIR", "TEMP", "TMP"})
        extended = diagnostic.environment("D", Path("F:/Python/Python314"),
                                          Path("F:/safe/work"), "C:/Windows")
        self.assertEqual(set(extended) - set(env), {"PATH", "COMSPEC"})
        with self.assertRaises(ValueError):
            diagnostic.environment("Z", Path("F:/x"), Path("F:/y"), "C:/Windows")

    def test_windows_arguments_preserve_space_and_quote(self):
        command = diagnostic.command(Path("F:/with space/python.exe"),
                                     Path('F:/with space/probe.py'), Path('F:/output.json'))
        self.assertTrue(command.startswith('"F:'))
        self.assertIn(" -I -S -B ", command)
        self.assertIn('probe.py"', command)

    def test_zero_exit_requires_marker_and_identity(self):
        self.assertEqual(diagnostic.classify(0, None, Path("F:/python.exe")),
                         "missing_or_invalid_marker")
        marker = {"marker": "T09-startup", "version": [3, 14, 6],
                  "executable": "F:/python.exe"}
        self.assertEqual(diagnostic.classify(0, marker, Path("F:/python.exe")), "started")
        self.assertEqual(diagnostic.classify(0xC0000142, None, Path("F:/python.exe")),
                         "startup_exit_c0000142")

    def test_hash_or_size_drift_stops(self):
        diagnostic.verify_bytes(b"abc", 3,
                                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
        for size, digest in ((4, "0" * 64), (3, "0" * 64)):
            with self.assertRaises(RuntimeError):
                diagnostic.verify_bytes(b"abc", size, digest)

    def test_charge_precedes_process_attempt(self):
        calls = []
        diagnostic.charged_call(lambda: calls.append("charged"),
                                lambda: calls.append("created"))
        self.assertEqual(calls, ["charged", "created"])
        def fail():
            raise RuntimeError("budget")
        with self.assertRaises(RuntimeError):
            diagnostic.charged_call(fail, lambda: calls.append("unexpected"))
        self.assertNotIn("unexpected", calls)

    def test_escape_is_rejected(self):
        with self.assertRaises(ValueError):
            diagnostic.safe_output(Path("F:/safe"), Path("F:/other/result.json"))

    def test_cleanup_never_terminates_unowned_handles(self):
        self.assertFalse(diagnostic.owned_handles(None, None))
        self.assertTrue(diagnostic.owned_handles(12, 14))
        self.assertFalse(diagnostic.owned_handles(12, None))


if __name__ == "__main__":
    unittest.main(verbosity=2)
