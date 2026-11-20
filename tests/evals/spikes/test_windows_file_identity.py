"""IF-I synthetic stat and boundary tests; no real fixture or child creation."""

import importlib.util
import io
import json
import stat
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent))
import windows_file_identity as subject


class SnapshotTests(unittest.TestCase):
    """Preserve exact observations, including missing versus zero fields."""

    def test_missing_and_zero_are_distinct_after_serialization(self):
        snapshot = subject.snapshot(SimpleNamespace(st_dev=0))
        copied = json.loads(json.dumps(snapshot))
        self.assertEqual(copied["st_dev"], {"present": True, "value": 0})
        self.assertEqual(copied["st_ino"], {"present": False, "value": None})

    def test_differences_are_not_discarded(self):
        left = subject.snapshot(SimpleNamespace(st_dev=1, st_ino=2))
        right = subject.snapshot(SimpleNamespace(st_dev=1, st_ino=3))
        result = subject.compare(left, right, ("st_dev", "st_ino"))
        self.assertEqual(result["differences"], {"st_ino": {"left": 2, "right": 3}})
        self.assertFalse(result["equal"])

    def test_equal_present_fields(self):
        value = subject.snapshot(SimpleNamespace(st_dev=1))
        self.assertTrue(subject.compare(value, value, ("st_dev",))["equal"])

    def test_missing_fields_are_unresolved(self):
        value = subject.snapshot(SimpleNamespace(st_dev=1))
        result = subject.compare(value, value, ("st_ino",))
        self.assertEqual(result["missing"], ["st_ino"])
        self.assertFalse(result["equal"])


class BoundaryTests(unittest.TestCase):
    """Refuse invalid creation and bounded-read/stat overages before side effects."""

    def test_invalid_targets_never_stat_or_open(self):
        budget = Mock()
        for path in (
            subject.RUN / "other.bin",
            subject.RUN.parent / "fixture.bin",
            subject.RUN / ".." / "fixture.bin",
        ):
            with self.subTest(path=path), self.assertRaises(subject.Boundary):
                subject.validate_target(subject.RUN, path, budget)
        budget.stat.assert_not_called()

    def test_existing_target_refused(self):
        budget = Mock()
        budget.stat.return_value = SimpleNamespace(
            st_mode=stat.S_IFDIR, st_file_attributes=0
        )
        with self.assertRaises(subject.Boundary):
            subject.validate_target(subject.RUN, subject.RUN / "fixture.bin", budget)

    def test_reparse_ancestor_refused(self):
        budget = Mock()
        budget.stat.return_value = SimpleNamespace(
            st_mode=stat.S_IFDIR, st_file_attributes=0x400
        )
        with self.assertRaises(subject.Boundary):
            subject.validate_target(subject.RUN, subject.RUN / "fixture.bin", budget)

    def test_stat_cap_prevents_system_call(self):
        budget = subject.Budget()
        budget.stats = 32
        with patch.object(Path, "lstat") as call, self.assertRaises(subject.Boundary):
            budget.stat(subject.RUN)
        call.assert_not_called()

    def test_read_cap_prevents_read(self):
        budget = subject.Budget()
        budget.read_bytes = 4096
        stream = Mock()
        with self.assertRaises(subject.Boundary):
            budget.read(stream)
        stream.read.assert_not_called()

    def test_oversized_read_refused(self):
        with self.assertRaises(subject.Boundary):
            subject.Budget().read(io.BytesIO(b"x" * 65))

    def test_unexpected_fixture_hash_refused(self):
        with self.assertRaises(subject.Boundary):
            subject.verify_bytes(b"wrong", subject.DATA)

    def test_change_summary_preserves_size_and_hash_change(self):
        result = subject.content_change(b"abc", b"abcd")
        self.assertTrue(result["size_changed"])
        self.assertTrue(result["hash_changed"])

    def test_fixture_failure_does_not_report_success(self):
        saved = []
        with (
            patch.object(subject, "validate_target"),
            patch.object(Path, "open", side_effect=OSError),
            self.assertRaises(OSError),
        ):
            subject.probe(subject.RUN, saved.append)
        self.assertEqual(saved[-1]["status"], "stopped_no_retry")

    def test_receipt_failure_prevents_fixture_creation(self):
        with (
            patch.object(subject, "validate_target"),
            patch.object(Path, "open") as opened,
            self.assertRaises(OSError),
        ):
            subject.probe(subject.RUN, Mock(side_effect=OSError))
        opened.assert_not_called()


if __name__ == "__main__":
    if sys.argv[1:] == ["mutation"]:
        spec = importlib.util.spec_from_file_location("mutant", subject.__file__)
        mutant = importlib.util.module_from_spec(spec)
        source = Path(subject.__file__).read_text(encoding="utf-8")
        source = source.replace('if a["value"] != b["value"]:', "if False:")
        exec(compile(source, "<controlled-mutation>", "exec"), mutant.__dict__)  # noqa: S102 -- authored aid only
        subject = mutant
        suite = unittest.TestSuite(
            [SnapshotTests("test_differences_are_not_discarded")]
        )
        result = unittest.TextTestRunner().run(suite)
        sys.exit(0 if result.wasSuccessful() else 1)
    unittest.main()
