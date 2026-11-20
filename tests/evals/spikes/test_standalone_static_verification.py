"""Synthetic static-inspection controls; never execute candidate payloads."""

import base64
import hashlib
import importlib.util
import io
import os
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

SOURCE = Path(__file__).with_name("standalone_static_verification.py")
RUN = Path(__file__).resolve().parents[3] / "data/t17/standalone-static-verification-03"
if SOURCE.exists():
    SPEC = importlib.util.spec_from_file_location("sa_inspector", SOURCE)
    review = importlib.util.module_from_spec(SPEC)
    sys.modules[SPEC.name] = review
    SPEC.loader.exec_module(review)
else:
    review = None


class StaticTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(review, "Static inspection aid has not been implemented")
        self.tmp = tempfile.TemporaryDirectory(dir=RUN)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.installed = self.root / "installed"
        self.installed.mkdir()
        self.archive = self.root / "fixture.zip"
        self.payload = b"inert executable-looking fixture; never launch"

    def fixture(self, entries=None):
        entries = entries or {"bin/runner.exe": self.payload, "LICENSE": b"test notice"}
        with zipfile.ZipFile(self.archive, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, data in entries.items():
                archive.writestr(name, data)
        for name, data in entries.items():
            if ".." not in name and not name.startswith("/"):
                target = self.installed / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        return self.archive.stat().st_size, hashlib.sha256(
            self.archive.read_bytes()
        ).hexdigest()

    def inspect(self, entries=None, **limits):
        size, digest = self.fixture(entries)
        return review.inspect_pair(
            self.archive,
            self.installed,
            size,
            digest,
            review.ReadBudget(2**24),
            review.Limits(**limits),
        )

    def test_valid_pair(self):
        result = self.inspect()
        self.assertEqual(result["files_compared"], 2)
        self.assertEqual(result["native_files"], ["bin/runner.exe"])
        self.assertEqual(result["notices"][0]["text"], "test notice")

    def test_unsafe_windows_and_archive_paths(self):
        for name in (
            "../x",
            "/x",
            "C:/x",
            "x:y",
            "a\\b",
            "a//b",
            "a/./b",
            "a/../b",
            "NUL",
            "aux.txt",
            "a. ",
            "a\nname",
            "a/CON.txt",
            "COM\u00b9",
        ):
            with self.subTest(name=name), self.assertRaises(review.Failure):
                review.checked_name(name, 8)

    def test_depth_limit(self):
        with self.assertRaises(review.Failure):
            review.checked_name("a/b/c", 2)

    def test_entry_limit(self):
        with self.assertRaisesRegex(review.Failure, "entry_limit"):
            self.inspect(max_entries=1)

    def test_central_directory_limit(self):
        with self.assertRaisesRegex(review.Failure, "central_limit"):
            self.inspect(max_central=1)

    def test_expansion_limit(self):
        with self.assertRaisesRegex(review.Failure, "expanded_limit"):
            self.inspect(max_expanded=1)

    def test_case_collision_and_duplicate(self):
        for names in (("A", "a"), ("x", "x")):
            with self.subTest(names=names):
                with zipfile.ZipFile(self.archive, "w") as archive:
                    for name in names:
                        archive.writestr(name, b"x")
                with self.assertRaises(review.Failure):
                    review.archive_entries(
                        self.archive, review.ReadBudget(2**20), review.Limits()
                    )

    def test_archive_symlink_rejected(self):
        with zipfile.ZipFile(self.archive, "w") as archive:
            entry = zipfile.ZipInfo("link")
            entry.create_system = 3
            entry.external_attr = 0o120777 << 16
            archive.writestr(entry, b"target")
        with self.assertRaisesRegex(review.Failure, "member_type"):
            review.archive_entries(
                self.archive, review.ReadBudget(2**20), review.Limits()
            )

    def test_member_tampering_detected(self):
        size, digest = self.fixture()
        (self.installed / "bin/runner.exe").write_bytes(b"changed")
        with self.assertRaisesRegex(review.Failure, "installed_(size|hash)"):
            review.inspect_pair(
                self.archive,
                self.installed,
                size,
                digest,
                review.ReadBudget(2**24),
                review.Limits(),
            )

    def test_archive_identity_mismatch(self):
        size, _ = self.fixture()
        with self.assertRaisesRegex(review.Failure, "archive_hash"):
            review.inspect_pair(
                self.archive,
                self.installed,
                size,
                "0" * 64,
                review.ReadBudget(2**24),
                review.Limits(),
            )

    def test_archive_size_mismatch(self):
        size, digest = self.fixture()
        with self.assertRaisesRegex(review.Failure, "archive_size"):
            review.inspect_pair(
                self.archive,
                self.installed,
                size + 1,
                digest,
                review.ReadBudget(2**24),
                review.Limits(),
            )

    def test_missing_and_extra_installed_files(self):
        size, digest = self.fixture()
        (self.installed / "extra").write_bytes(b"x")
        with self.assertRaisesRegex(review.Failure, "installed_set"):
            review.inspect_pair(
                self.archive,
                self.installed,
                size,
                digest,
                review.ReadBudget(2**24),
                review.Limits(),
            )
        (self.installed / "extra").unlink()
        (self.installed / "LICENSE").unlink()
        with self.assertRaisesRegex(review.Failure, "installed_set"):
            review.inspect_pair(
                self.archive,
                self.installed,
                size,
                digest,
                review.ReadBudget(2**24),
                review.Limits(),
            )

    def test_hardlink_rejected(self):
        target = self.root / "target"
        target.write_bytes(b"x")
        os.link(target, self.root / "alias")
        with (
            self.assertRaisesRegex(review.Failure, "file_type"),
            review.open_regular(target, self.root),
        ):
            self.fail("hardlink admitted")

    def test_symlink_or_reparse_attribute_rejected(self):
        target = self.root / "target"
        target.write_bytes(b"x")
        with (
            patch.object(review, "is_reparse", return_value=True),
            self.assertRaises(review.Failure),
            review.open_regular(target, self.root),
        ):
            self.fail("reparse admitted")

    def test_outside_root_rejected(self):
        with (
            self.assertRaisesRegex(review.Failure, "outside_root"),
            review.open_regular(self.archive, self.installed),
        ):
            self.fail("outside root admitted")

    def test_path_change_during_read_rejected(self):
        target = self.root / "target"
        target.write_bytes(b"x")
        with (
            self.assertRaisesRegex(review.Failure, "file_changed"),
            review.open_regular(target, self.root),
        ):
            target.write_bytes(b"longer")

    def test_read_admission_and_failed_read_charged(self):
        budget = review.ReadBudget(3)
        with self.assertRaisesRegex(review.Failure, "read_limit"):
            budget.reserve(4)
        self.assertEqual(budget.used, 0)
        budget.reserve(3)
        self.assertEqual(budget.used, 3)
        with self.assertRaises(review.Failure):
            budget.reserve(1)

    def test_missing_input_stops_before_zip_parse(self):
        with self.assertRaises(FileNotFoundError):
            review.inspect_pair(
                self.archive,
                self.installed,
                1,
                "0" * 64,
                review.ReadBudget(2**24),
                review.Limits(),
            )

    def test_interrupted_read_is_precharged(self):
        budget = review.ReadBudget(10)
        source = io.BytesIO(b"abc")
        with (
            patch.object(source, "read", side_effect=OSError("synthetic")),
            self.assertRaises(OSError),
        ):
            review.digest_stream(source, 3, budget)
        self.assertEqual(budget.used, 3)

    def test_actual_read_overflow_probe(self):
        budget = review.ReadBudget(10)
        with self.assertRaisesRegex(review.Failure, "overflow_read"):
            review.digest_stream(io.BytesIO(b"longer"), 2, budget)
        self.assertEqual(budget.used, 3)

    def test_notice_caps_do_not_silently_truncate(self):
        result = self.inspect(max_notice=2)
        self.assertEqual(result["notices"][0]["status"], "unreviewed_size_cap")
        self.assertNotIn("text", result["notices"][0])

    def test_malformed_archive_and_crc(self):
        self.archive.write_bytes(b"not a ZIP")
        with self.assertRaises(review.Failure):
            review.archive_entries(
                self.archive, review.ReadBudget(2**20), review.Limits()
            )
        size, digest = self.fixture()
        with zipfile.ZipFile(self.archive) as archive:
            offset = archive.getinfo("bin/runner.exe").header_offset
        with self.archive.open("r+b") as stream:
            stream.seek(offset + 30 + len("bin/runner.exe"))
            byte = stream.read(1)
            stream.seek(-1, 1)
            stream.write(bytes([byte[0] ^ 255]))
        digest = hashlib.sha256(self.archive.read_bytes()).hexdigest()
        with self.assertRaises(review.Failure):
            review.inspect_pair(
                self.archive,
                self.installed,
                size,
                digest,
                review.ReadBudget(2**24),
                review.Limits(),
            )

    def test_no_candidate_launch_or_import(self):
        with patch(
            "subprocess.Popen", side_effect=AssertionError("candidate launched")
        ):
            result = self.inspect()
        self.assertEqual(result["files_compared"], 2)

    def test_integrity_mutation_is_caught_by_gold(self):
        size, digest = self.fixture()
        with (
            patch.object(review, "hash_regular", return_value="0" * 64),
            self.assertRaisesRegex(review.Failure, "archive_hash"),
        ):
            review.inspect_pair(
                self.archive,
                self.installed,
                size,
                digest,
                review.ReadBudget(2**24),
                review.Limits(),
            )

    def wheel_fixture(self, bad_record=False):
        metadata = b"Name: synthetic\nVersion: 1\nRequires-Python: >=3.11\n"
        encoded = (
            base64.urlsafe_b64encode(hashlib.sha256(metadata).digest())
            .decode()
            .rstrip("=")
        )
        if bad_record:
            encoded = "wrong"
        record = (
            f"synthetic-1.dist-info/METADATA,sha256={encoded},{len(metadata)}\n"
            "synthetic-1.dist-info/RECORD,,\n"
        ).encode()
        with zipfile.ZipFile(self.archive, "w") as archive:
            archive.writestr("synthetic-1.dist-info/METADATA", metadata)
            archive.writestr("synthetic-1.dist-info/RECORD", record)
        return self.archive.stat().st_size, hashlib.sha256(
            self.archive.read_bytes()
        ).hexdigest()

    def test_synthetic_wheel_record_and_metadata(self):
        size, digest = self.wheel_fixture()
        result = review.inspect_wheel(
            self.archive, size, digest, review.ReadBudget(2**20)
        )
        self.assertTrue(result["record_verified"])
        self.assertIn("Name: synthetic", result["metadata"])

    def test_synthetic_wheel_record_mismatch(self):
        size, digest = self.wheel_fixture(bad_record=True)
        with self.assertRaisesRegex(review.Failure, "wheel_record"):
            review.inspect_wheel(self.archive, size, digest, review.ReadBudget(2**20))


if __name__ == "__main__":
    unittest.main()
