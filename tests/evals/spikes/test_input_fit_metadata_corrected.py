"""IF-K targeted fake-reader tests plus all20unchanged IF-R controls."""

import hashlib
import io
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent))
import input_fit_metadata_corrected as subject
from test_input_fit_metadata import ControllerTests, PathTests, ReadTests  # noqa: F401


class CorrectedReadTests(unittest.TestCase):
    """Only mocked metadata streams/stat records; no model files or children."""

    def setUp(self):
        self.raw = b"synthetic"
        self.item = (
            "test",
            "fixture",
            len(self.raw),
            hashlib.sha256(self.raw).hexdigest(),
        )
        self.path = SimpleNamespace(
            st_dev=1,
            st_ino=2,
            st_size=len(self.raw),
            st_mtime_ns=10,
            st_ctime_ns=20,
            st_mode=33206,
            st_nlink=1,
        )
        self.handle = SimpleNamespace(**vars(self.path))
        self.handle.st_ctime_ns = 30
        self.state = {"charged_bytes": 0, "read_bytes": 0, "files": []}

    def read(self, handle_after=None, path_after=None, raw=None):
        stream = io.BytesIO(self.raw if raw is None else raw)
        stream.fileno = lambda: 123
        with (
            patch.object(
                subject.BASE,
                "checked_file",
                side_effect=[self.path, path_after or self.path],
            ),
            patch.object(
                subject.os,
                "fstat",
                side_effect=[self.handle, handle_after or self.handle],
            ),
            patch.object(Path, "open", return_value=stream),
        ):
            return subject.read_one(
                Path("F:/models"), self.item, self.state, lambda _: None
            )

    def test_cross_api_ctime_only_passes_and_is_recorded(self):
        self.assertNotEqual(
            subject.BASE.identity(self.path), subject.BASE.identity(self.handle)
        )
        self.assertEqual(self.read(), self.raw)
        record = self.state["files"][-1]
        self.assertTrue(record["cross_api_ctime_differs"])
        self.assertEqual(record["status"], "completed")

    def test_same_api_handle_ctime_mutation_refused(self):
        after = SimpleNamespace(**vars(self.handle))
        after.st_ctime_ns += 1
        with self.assertRaises(subject.Boundary) as caught:
            self.read(handle_after=after)
        self.assertEqual(caught.exception.code, "HANDLE_MUTATED")

    def test_same_api_path_ctime_mutation_refused(self):
        after = SimpleNamespace(**vars(self.path))
        after.st_ctime_ns += 1
        with self.assertRaises(subject.Boundary) as caught:
            self.read(path_after=after)
        self.assertEqual(caught.exception.code, "PATH_MUTATED")

    def test_cross_api_nonctime_changes_refused(self):
        for field in subject.CROSS_FIELDS:
            self.setUp()
            setattr(self.handle, field, getattr(self.handle, field) + 1)
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                self.read()
            self.assertEqual(self.state["files"][-1]["status"], "refused")

    def test_missing_or_meaningless_identity_refused(self):
        for field, value in (("st_ino", 0), ("st_dev", 0), ("st_size", None)):
            self.setUp()
            setattr(self.handle, field, value)
            with self.subTest(field=field), self.assertRaises(subject.Boundary):
                self.read()
        del self.handle.st_ctime_ns
        with self.assertRaises(subject.Boundary):
            self.read()

    def test_wrong_digest_size_and_oversize_still_refuse(self):
        for raw in (b"x" * len(self.raw), b"x", b"x" * 65537):
            self.setUp()
            with self.subTest(length=len(raw)), self.assertRaises(subject.Boundary):
                self.read(raw=raw)
            self.assertEqual(self.state["files"][-1]["code"], "SIZE_DIGEST_MISMATCH")

    def test_aggregate_and_path_refusal_never_open(self):
        self.state["charged_bytes"] = 1048576
        with patch.object(Path, "open") as opened, self.assertRaises(subject.Boundary):
            subject.read_one(Path("F:/models"), self.item, self.state, lambda _: None)
        opened.assert_not_called()
        self.state["charged_bytes"] = 0
        with (
            patch.object(
                subject.BASE, "checked_file", side_effect=subject.BASE.Boundary
            ),
            patch.object(Path, "open") as opened,
            self.assertRaises(subject.BASE.Boundary),
        ):
            subject.read_one(Path("F:/models"), self.item, self.state, lambda _: None)
        opened.assert_not_called()

    def test_progress_failure_prevents_open(self):
        with patch.object(Path, "open") as opened, self.assertRaises(OSError):
            subject.read_one(
                Path("F:/models"), self.item, self.state, Mock(side_effect=OSError)
            )
        opened.assert_not_called()


class AdmissionTests(unittest.TestCase):
    """Pure fresh-root, controller claim, clock and single-attempt checks."""

    def test_invalid_admission_refused(self):
        valid = {
            "status": "active",
            "worker_attempts": 1,
            "started_qpc": 100,
            "frequency": 10,
        }
        for root, meter, claim, now, output in (
            (subject.RUN.parent, valid, b"IF-K", 11, 0),
            (subject.RUN, {}, b"IF-K", 11, 0),
            (subject.RUN, {**valid, "status": "closed"}, b"IF-K", 11, 0),
            (subject.RUN, {**valid, "worker_attempts": 2}, b"IF-K", 11, 0),
            (subject.RUN, valid, b"wrong", 11, 0),
            (subject.RUN, valid, b"IF-K", 1150, 0),
            (subject.RUN, valid, b"IF-K", 11, 2097152),
        ):
            with (
                self.subTest(root=root, meter=meter),
                self.assertRaises(subject.Boundary),
            ):
                subject.admit(root, meter, claim, now, output)

    def test_valid_admission(self):
        subject.admit(
            subject.RUN,
            {
                "status": "active",
                "worker_attempts": 1,
                "started_qpc": 100,
                "frequency": 10,
            },
            b"IF-K",
            11,
            0,
        )


if __name__ == "__main__":
    if sys.argv[1:] == ["mutation"]:
        original = subject.SAME_FIELDS
        subject.SAME_FIELDS = subject.CROSS_FIELDS
        result = unittest.TextTestRunner().run(
            unittest.TestSuite(
                [CorrectedReadTests("test_same_api_handle_ctime_mutation_refused")]
            )
        )
        subject.SAME_FIELDS = original
        sys.exit(0 if result.wasSuccessful() else 1)
    unittest.main()
