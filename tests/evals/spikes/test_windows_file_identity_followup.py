"""IF-J bootstrap controls plus the unchanged14fake probe regressions."""

import io
import sys
import unittest
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent))
import windows_file_identity_followup as subject
from test_windows_file_identity import BoundaryTests, SnapshotTests  # noqa: F401


class FollowupTests(unittest.TestCase):
    """No real files, modules or child processes are opened by these controls."""

    def setUp(self):
        self.meter = {
            "status": "active",
            "probe_attempts": 1,
            "started_qpc": 100,
            "frequency": 10,
        }
        self.module = ModuleType("fake_probe")
        self.module.RUN = Path("old")
        exec("def persist(value): return RUN\n", self.module.__dict__)  # noqa: S102 -- fixed test function
        self.module.probe = Mock(side_effect=lambda root, save: save({}))
        self.loader = Mock(return_value=self.module)
        self.claim = Mock()

    def execute(self, root=None, meter=None, claim=b"IF-J", now=11, output=0):
        return subject.execute(
            root or subject.RUN,
            self.meter if meter is None else meter,
            claim,
            now,
            output,
            self.loader,
            self.claim,
        )

    def test_binding_routes_probe_and_persistence_to_fresh_root(self):
        self.assertEqual(self.execute(), subject.RUN)
        self.assertEqual(self.module.RUN, subject.RUN)
        self.claim.assert_called_once_with(subject.RUN)

    def test_wrong_root_never_calls_loader_or_probe(self):
        with self.assertRaises(subject.Boundary):
            self.execute(root=subject.RUN.parent / "windows-identity-01")
        self.loader.assert_not_called()
        self.module.probe.assert_not_called()

    def test_closed_missing_or_unclaimed_meter_refused(self):
        for meter in (
            {},
            {**self.meter, "status": "closed"},
            {**self.meter, "probe_attempts": 0},
        ):
            with self.subTest(meter=meter), self.assertRaises(subject.Boundary):
                self.execute(meter=meter)
        self.loader.assert_not_called()

    def test_time_output_and_claim_refused(self):
        for kwargs in (
            {"now": 1150},
            {"now": 9},
            {"output": 1048576},
            {"claim": b"bad"},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(subject.Boundary):
                self.execute(**kwargs)
        self.loader.assert_not_called()

    def test_second_probe_claim_prevents_invocation(self):
        self.claim.side_effect = FileExistsError
        with self.assertRaises(FileExistsError):
            self.execute()
        self.module.probe.assert_not_called()

    def test_changed_source_hash_refused_before_execution(self):
        with (
            patch.object(Path, "open", return_value=io.BytesIO(b"changed")),
            self.assertRaises(subject.Boundary),
        ):
            subject.load_probe()

    def test_source_read_error_propagates(self):
        self.loader.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            self.execute()
        self.module.probe.assert_not_called()

    def test_probe_error_propagates_without_success(self):
        self.module.probe.side_effect = OSError
        with self.assertRaises(OSError):
            self.execute()


if __name__ == "__main__":
    if sys.argv[1:] == ["mutation"]:
        mutant = ModuleType("mutant")
        mutant.__file__ = subject.__file__
        source = Path(subject.__file__).read_text(encoding="utf-8")
        source = source.replace("if root != RUN:", "if False:")
        exec(compile(source, "<controlled-mutation>", "exec"), mutant.__dict__)  # noqa: S102 -- authored aid only
        subject = mutant
        result = unittest.TextTestRunner().run(
            unittest.TestSuite(
                [FollowupTests("test_wrong_root_never_calls_loader_or_probe")]
            )
        )
        sys.exit(0 if result.wasSuccessful() else 1)
    unittest.main()
