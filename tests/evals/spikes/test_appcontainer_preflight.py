"""Synthetic safety-policy tests; no profile or network side effects."""

import tempfile
import unittest
from pathlib import Path

import appcontainer_preflight as preflight


class PolicyTests(unittest.TestCase):
    """Guard actual paths, accounting and control interpretation."""

    def test_paths_must_stay_in_owned_root(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.assertEqual(preflight.contained(root, root / "input"), root / "input")
            with self.assertRaises(ValueError):
                preflight.contained(root, root / ".." / "outside")

    def test_reparse_path_is_rejected(self):
        self.assertFalse(preflight.regular_attributes(0x410))
        self.assertTrue(preflight.regular_attributes(0x10))

    def test_only_exact_grant_roles_allowed(self):
        self.assertEqual(preflight.grant_rights("runtime"), "RX")
        self.assertEqual(preflight.grant_rights("work"), "M")
        with self.assertRaises(ValueError):
            preflight.grant_rights("private")

    def test_accounting_protects_cleanup_reserve(self):
        self.assertEqual(preflight.next_count(10, 3, 96), 13)
        with self.assertRaises(RuntimeError):
            preflight.next_count(82, 3, 96)
        self.assertEqual(preflight.next_count(82, 3, 96, cleanup=True), 85)

    def test_cleanup_requires_exact_created_profile(self):
        name = "DocumentAssistant.T09.preflight-01"
        self.assertTrue(preflight.owns_profile(name, "preflight-01", True))
        self.assertFalse(preflight.owns_profile(name, "other", True))
        self.assertFalse(preflight.owns_profile(name, "preflight-01", False))

    def test_token_must_match_sid_and_have_no_capabilities(self):
        good = {"appcontainer": True, "sid": "S-1-15-2-42", "capabilities": 0, "integrity": 4096}
        preflight.validate_token(good, "S-1-15-2-42")
        for change in ({"appcontainer": False}, {"capabilities": 1},
                       {"sid": "S-1-15-2-99"}, {"integrity": 8192}):
            with self.subTest(change=change), self.assertRaises(RuntimeError):
                preflight.validate_token(good | change, "S-1-15-2-42")

    def test_only_explicit_native_denial_is_accepted(self):
        self.assertTrue(preflight.native_denied(10013, False))
        for error, observed in ((10035, False), (0, False), (10061, False),
                                (10060, False), (10013, True)):
            self.assertFalse(preflight.native_denied(error, observed))

    def test_runtime_selection_excludes_global_packages_and_executables(self):
        for allowed in ("python.exe", "python314.dll", "Lib/ctypes/__init__.py",
                        "DLLs/_ctypes.pyd"):
            self.assertTrue(preflight.runtime_member(Path(allowed)))
        for denied in ("pythonw.exe", "Lib/site-packages/evil.py",
                       "Lib/test/test_os.py", "Lib/__pycache__/os.pyc",
                       "../python.exe", "Scripts/other.exe"):
            self.assertFalse(preflight.runtime_member(Path(denied)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
