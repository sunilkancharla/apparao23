"""IF-R fake controls; never launch a child or read installed model metadata."""

import hashlib
import importlib.util
import io
import json
import stat
import subprocess
import sys
import unittest
from pathlib import Path, PureWindowsPath
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent))
import input_fit_metadata as subject


class PathTests(unittest.TestCase):
    """Finite Windows ancestry and pre-open refusals."""

    def test_drive_case_and_trailing_separator(self):
        for root, target in [("F:/", "f:/a"), ("F:/models/", "f:/MODELS/a")]:
            chain = subject.ancestors(PureWindowsPath(root), PureWindowsPath(target))
            self.assertEqual(chain[-1], PureWindowsPath(target))
            self.assertLessEqual(len(chain), 64)

    def test_outside_traversal_root_and_depth_refused(self):
        for target in [
            "F:/else/a",
            "F:/models/../a",
            "F:/models",
            "F:/models/" + "a/" * 65,
        ]:
            with self.subTest(target=target), self.assertRaises(subject.Boundary):
                subject.ancestors(PureWindowsPath("F:/models"), PureWindowsPath(target))

    def test_nonprogress_refused(self):
        fake = Mock()
        fake.is_absolute.return_value = True
        fake.parts = ("F:/", "models", "a")
        fake.parents = (fake, fake)
        fake.relative_to.return_value.parts = ("a",)
        with self.assertRaises(subject.Boundary):
            subject.ancestors(fake, fake)

    def test_reparse_and_wrong_type_refused(self):
        for mode, attrs in [
            (stat.S_IFDIR, 0x400),
            (stat.S_IFREG, 0),
            (stat.S_IFLNK, 0),
        ]:
            fake_stat = SimpleNamespace(st_mode=mode, st_file_attributes=attrs)
            with (
                patch.object(Path, "lstat", return_value=fake_stat),
                self.assertRaises(subject.Boundary),
            ):
                subject.checked_file(Path("F:/models"), Path("F:/models/a"))


class ReadTests(unittest.TestCase):
    """Bounded read, stable identity and durable progress requirements."""

    def setUp(self):
        self.raw = b'{"test": true}'
        self.item = (
            "fixture",
            "a",
            len(self.raw),
            hashlib.sha256(self.raw).hexdigest(),
        )
        self.info = SimpleNamespace(
            st_dev=1,
            st_ino=2,
            st_size=len(self.raw),
            st_mtime_ns=3,
            st_ctime_ns=4,
            st_mode=stat.S_IFREG,
            st_nlink=1,
        )
        self.saved = []
        self.state = {"charged_bytes": 0, "read_bytes": 0, "files": []}

    def read(self, raw=None, info=None, save=None):
        stream = io.BytesIO(self.raw if raw is None else raw)
        stream.fileno = lambda: 123
        with (
            patch.object(subject, "checked_file", return_value=self.info),
            patch.object(Path, "open", return_value=stream),
            patch.object(subject.os, "fstat", return_value=info or self.info),
        ):
            return subject.read_one(
                Path("F:/models"),
                self.item,
                self.state,
                save
                or (lambda value: self.saved.append(json.loads(json.dumps(value)))),
            )

    def test_valid_read_progress_and_charge(self):
        self.assertEqual(self.read(), self.raw)
        self.assertEqual(
            [x["files"][-1]["status"] for x in self.saved],
            ["started", "started", "completed"],
        )
        self.assertEqual(self.state["read_bytes"], len(self.raw))
        self.assertEqual(self.state["charged_bytes"], 65537)

    def test_digest_size_and_oversize_refused(self):
        for raw in [b"x" * len(self.raw), b"x", b"x" * 65538]:
            with self.subTest(length=len(raw)):
                self.setUp()
                with self.assertRaises(subject.Boundary):
                    self.read(raw)
                self.assertEqual(self.state["files"][-1]["status"], "refused")

    def test_changed_handle_identity_refused(self):
        changed = SimpleNamespace(**vars(self.info))
        changed.st_ino = 999
        with self.assertRaises(subject.Boundary):
            self.read(info=changed)

    def test_changed_path_after_read_refused(self):
        changed = SimpleNamespace(**vars(self.info))
        changed.st_mtime_ns += 1
        stream = io.BytesIO(self.raw)
        stream.fileno = lambda: 123
        with (
            patch.object(subject, "checked_file", side_effect=[self.info, changed]),
            patch.object(Path, "open", return_value=stream),
            patch.object(subject.os, "fstat", return_value=self.info),
            self.assertRaises(subject.Boundary),
        ):
            subject.read_one(Path("F:/models"), self.item, self.state, lambda _: None)

    def test_budget_or_invalid_path_never_opens(self):
        self.state["charged_bytes"] = 1048576
        with patch.object(Path, "open") as opened, self.assertRaises(subject.Boundary):
            subject.read_one(Path("F:/models"), self.item, self.state, lambda _: None)
        opened.assert_not_called()
        self.state["charged_bytes"] = 0
        with (
            patch.object(subject, "checked_file", side_effect=subject.Boundary),
            patch.object(Path, "open") as opened,
            self.assertRaises(subject.Boundary),
        ):
            subject.read_one(Path("F:/models"), self.item, self.state, lambda _: None)
        opened.assert_not_called()

    def test_progress_failure_prevents_open(self):
        with patch.object(Path, "open") as opened, self.assertRaises(OSError):
            self.read(save=Mock(side_effect=OSError))
        opened.assert_not_called()

    def test_read_error_retains_conservative_charge(self):
        with (
            patch.object(subject, "checked_file", return_value=self.info),
            patch.object(Path, "open", side_effect=OSError),
            self.assertRaises(OSError),
        ):
            subject.read_one(Path("F:/models"), self.item, self.state, lambda _: None)
        self.assertEqual(self.state["charged_bytes"], 65537)
        self.assertEqual(self.state["files"][-1]["error"], "OSError")


class ControllerTests(unittest.TestCase):
    """Mock the exact owned subprocess, including failed cleanup and one-shot gate."""

    def setUp(self):
        self.process = Mock(returncode=0, pid=123)
        self.process.communicate.return_value = (
            b'{"status":"complete","files":9}',
            b"",
        )
        self.saved = []
        self.state = {"actual_attempts": 0}
        self.spawn = Mock(return_value=self.process)

    def run_child(self):
        return subject.run_owned(
            ["python", "-I", "-S", "-B", "aid.py", "worker"],
            self.state,
            self.saved.append,
            self.spawn,
        )

    def test_success_reaped_and_explicit_argv(self):
        result = self.run_child()
        self.assertEqual(result["status"], "complete")
        self.assertTrue(self.state["reaped"])
        self.assertFalse(self.spawn.call_args.kwargs["shell"])
        self.process.communicate.assert_called_once_with(timeout=30)

    def test_second_attempt_never_spawns(self):
        self.state["actual_attempts"] = 1
        with self.assertRaises(subject.Boundary):
            self.run_child()
        self.spawn.assert_not_called()

    def test_bad_outputs_or_exit_refused(self):
        for output, code in [
            (b"", 0),
            (b"bad", 0),
            (b"{}", 0),
            (b"x" * 65537, 0),
            (b'{"status":"complete","files":9}', 1),
        ]:
            self.setUp()
            self.process.returncode = code
            self.process.communicate.return_value = (output, b"")
            with (
                self.subTest(output_length=len(output), code=code),
                self.assertRaises(subject.Boundary),
            ):
                self.run_child()
            self.assertTrue(self.state["reaped"])

    def test_timeout_kills_owned_handle_reaps_and_refuses(self):
        self.process.communicate.side_effect = subprocess.TimeoutExpired("owned", 30)
        self.process.wait.return_value = -1
        with self.assertRaises(subject.Boundary):
            self.run_child()
        self.process.kill.assert_called_once()
        self.process.wait.assert_called_once_with(timeout=5)
        self.assertTrue(self.state["reaped"])

    def test_failed_kill_or_reap_never_success(self):
        for operation in ["kill", "wait"]:
            self.setUp()
            self.process.communicate.side_effect = subprocess.TimeoutExpired(
                "owned", 30
            )
            getattr(self.process, operation).side_effect = OSError
            with self.subTest(operation=operation), self.assertRaises(subject.Boundary):
                self.run_child()
            self.assertFalse(self.state["reaped"])
            self.process.stdout.close.assert_not_called()
            self.process.stderr.close.assert_not_called()

    def test_receipt_failure_before_spawn(self):
        with self.assertRaises(OSError):
            subject.run_owned(
                ["fake"], self.state, Mock(side_effect=OSError), self.spawn
            )
        self.spawn.assert_not_called()

    def test_spawn_failure_retains_no_child_receipt(self):
        self.spawn.side_effect = OSError
        with self.assertRaises(OSError):
            self.run_child()
        self.assertTrue(self.state["reaped"])
        self.assertFalse(self.state["child_created"])
        self.assertEqual(self.state["status"], "stopped_no_retry")

    def test_receipt_failure_after_spawn_still_reaps(self):
        save = Mock(side_effect=[None, OSError, None])
        with self.assertRaises(OSError):
            subject.run_owned(["fake"], self.state, save, self.spawn)
        self.process.kill.assert_called_once()
        self.process.wait.assert_called_once_with(timeout=5)

    def test_stderr_or_wrong_count_refused(self):
        for output, err in [
            (b'{"status":"complete","files":8}', b""),
            (b'{"status":"complete","files":9}', b"unexpected"),
        ]:
            self.setUp()
            self.process.communicate.return_value = (output, err)
            with self.assertRaises(subject.Boundary):
                self.run_child()


if __name__ == "__main__":
    if sys.argv[1:] == ["mutation"]:
        spec = importlib.util.spec_from_file_location("mutant", subject.__file__)
        mutant = importlib.util.module_from_spec(spec)
        source = Path(subject.__file__).read_text(encoding="utf-8")
        source = source.replace(
            'state.get("actual_attempts", 0) != 0',
            'state.get("actual_attempts", 0) < 0',
        )
        exec(compile(source, "<in-memory-mutation>", "exec"), mutant.__dict__)  # noqa: S102 -- only this authored aid, controlled mutation
        subject = mutant
        suite = unittest.TestSuite(
            [ControllerTests("test_second_attempt_never_spawns")]
        )
        verdict = unittest.TextTestRunner().run(suite)
        sys.exit(0 if verdict.wasSuccessful() else 1)
    unittest.main()
