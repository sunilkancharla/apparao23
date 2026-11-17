"""Synthetic Hub-only controls; fixtures never enter closed trial roots."""

import base64
import csv
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

SOURCE = Path(__file__).with_name("hub_static_review.py")
RUN = Path(__file__).resolve().parents[3] / "data/t17/hub-only-static-review-01"
if SOURCE.exists():
    SPEC = importlib.util.spec_from_file_location("hs_review", SOURCE)
    review = importlib.util.module_from_spec(SPEC)
    sys.modules[SPEC.name] = review
    SPEC.loader.exec_module(review)
else:
    review = None


class HubTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(review, "Hub-only inspection aid has not been implemented")
        self.tmp = tempfile.TemporaryDirectory(dir=RUN)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.wheel = self.root / "synthetic.whl"

    def fixture(self, count=4, bad=None, extras=None):
        files = {
            "synthetic-1.dist-info/METADATA": b"Name: synthetic\nVersion: 1\nRequires-Python: >=3.11\n",
            "synthetic-1.dist-info/licenses/LICENSE": b"synthetic license text",
            "synthetic/__init__.py": b"raise AssertionError('candidate executed')",
        }
        for number in range(count - 4):
            files[f"synthetic/data_{number:03}.bin"] = b"inert"
        files.update(extras or {})
        rows = []
        for name, data in files.items():
            digest = (
                base64.urlsafe_b64encode(hashlib.sha256(data).digest())
                .decode()
                .rstrip("=")
            )
            rows.append([name, "sha256=" + digest, str(len(data))])
        if bad == "hash":
            rows[0][1] = "sha256=wrong"
        elif bad == "size":
            rows[0][2] = "999"
        elif bad == "omit":
            rows.pop()
        elif bad == "duplicate":
            rows.append(rows[0])
        elif bad == "arity":
            rows[0].append("unexpected")
        record_name = "synthetic-1.dist-info/RECORD"
        rows.append([record_name, "", ""])
        text = io.StringIO(newline="")
        csv.writer(text).writerows(rows)
        files[record_name] = text.getvalue().encode()
        with zipfile.ZipFile(self.wheel, "w") as wheel:
            for name, data in files.items():
                wheel.writestr(name, data)
        return self.wheel.stat().st_size, hashlib.sha256(
            self.wheel.read_bytes()
        ).hexdigest()

    def inspect(self, count=4, bad=None, policy=None, extras=None):
        size, digest = self.fixture(count, bad, extras)
        return review.inspect_hub(
            self.wheel, size, digest, review.Counter(2**23), policy
        )

    def test_191_entries_admitted_and_record_verified(self):
        result = self.inspect(191)
        self.assertEqual(result["entries"], 191)
        self.assertTrue(result["record_verified"])
        self.assertEqual(result["notices"][0]["text"], "synthetic license text")

    def test_257_refused_before_zipfile_member_parsing(self):
        size, digest = self.fixture(257)
        with (
            patch.object(
                review.zipfile,
                "ZipFile",
                side_effect=AssertionError("member parser entered"),
            ),
            self.assertRaisesRegex(review.ReviewFailure, "entry_limit"),
        ):
            review.inspect_hub(self.wheel, size, digest, review.Counter(2**23))

    def test_runtime_default_remains_128(self):
        primitive = review.load_primitives(review.Counter(2**20))
        self.assertEqual(primitive.Limits().max_entries, 128)
        size, digest = self.fixture(191)
        with self.assertRaisesRegex(review.ReviewFailure, "entry_limit"):
            review.inspect_hub(
                self.wheel,
                size,
                digest,
                review.Counter(2**23),
                review.Policy(entries=128),
            )

    def test_payload_identity(self):
        size, _ = self.fixture()
        with self.assertRaisesRegex(review.ReviewFailure, "wheel_identity"):
            review.inspect_hub(self.wheel, size, "0" * 64, review.Counter(2**23))

    def test_payload_size_and_missing_input(self):
        with self.assertRaises(FileNotFoundError):
            review.inspect_hub(self.wheel, 1, "0" * 64, review.Counter(2**23))
        size, digest = self.fixture()
        with self.assertRaisesRegex(review.ReviewFailure, "wheel_identity"):
            review.inspect_hub(self.wheel, size + 1, digest, review.Counter(2**23))

    def test_owned_source_mismatch_refuses_before_compilation(self):
        with (
            patch.object(review, "PRIMITIVE_SHA", "0" * 64),
            patch(
                "builtins.compile",
                side_effect=AssertionError("unverified source compiled"),
            ),
            self.assertRaisesRegex(review.ReviewFailure, "owned_source_identity"),
        ):
            review.load_primitives(review.Counter(2**20))

    def test_old_workers_and_roots_never_used(self):
        primitive = review.load_primitives(review.Counter(2**20))
        old_root = primitive.RUN
        with (
            patch.object(review, "load_primitives", return_value=primitive),
            patch.object(primitive, "worker", side_effect=AssertionError("old worker")),
            patch.object(
                primitive, "durable_json", side_effect=AssertionError("old writer")
            ),
            patch("subprocess.Popen", side_effect=AssertionError("candidate launch")),
        ):
            self.assertTrue(self.inspect()["record_verified"])
        self.assertEqual(primitive.RUN, old_root)
        self.assertNotEqual(RUN, old_root)

    def test_record_failures(self):
        for bad in ("hash", "size", "omit", "duplicate", "arity"):
            with (
                self.subTest(bad=bad),
                self.assertRaisesRegex(review.ReviewFailure, "record"),
            ):
                self.inspect(bad=bad)

    def test_unsafe_names_and_case_collisions(self):
        for name in (
            "../outside",
            "C:/drive",
            "a:b",
            "bad\\path",
            "NUL",
            "SYNTHETIC/__init__.py",
        ):
            with self.subTest(name=name), self.assertRaises(review.ReviewFailure):
                self.inspect(extras={name: b"inert"})

    def test_expansion_and_metadata_caps(self):
        with self.assertRaisesRegex(review.ReviewFailure, "expanded_limit"):
            self.inspect(policy=review.Policy(expanded=1))
        with self.assertRaisesRegex(review.ReviewFailure, "text_limit"):
            self.inspect(policy=review.Policy(metadata=1))

    def test_notice_caps_mark_unreviewed(self):
        result = self.inspect(policy=review.Policy(notice=1))
        self.assertEqual(result["notices"][0]["status"], "unreviewed_size_cap")
        self.assertNotIn("text", result["notices"][0])

    def test_native_names_are_inventory_not_loaded(self):
        result = self.inspect(
            extras={"synthetic/native.pyd": b"inert native-looking bytes"}
        )
        self.assertEqual(result["native_names"], ["synthetic/native.pyd"])
        self.assertNotIn("huggingface_hub", sys.modules)
        self.assertNotIn("tokenizers", sys.modules)

    def test_read_limit_and_failed_precharge(self):
        budget = review.Counter(3)
        with self.assertRaisesRegex(review.ReviewFailure, "read_limit"):
            budget.reserve(4)
        self.assertEqual(budget.used, 0)
        with self.assertRaisesRegex(review.ReviewFailure, "read_limit"):
            self.inspect_with_budget(review.Counter(1))
        calls = []
        budget = review.Counter(10, lambda amount: calls.append(amount))
        budget.reserve(3)
        self.assertEqual((budget.used, calls), (3, [3]))

    def inspect_with_budget(self, budget):
        size, digest = self.fixture()
        return review.inspect_hub(self.wheel, size, digest, budget)

    def test_malformed_and_crc(self):
        self.wheel.write_bytes(b"not a ZIP")
        size = self.wheel.stat().st_size
        digest = hashlib.sha256(self.wheel.read_bytes()).hexdigest()
        with self.assertRaises(review.ReviewFailure):
            review.inspect_hub(self.wheel, size, digest, review.Counter(2**23))
        self.fixture()
        with zipfile.ZipFile(self.wheel) as archive:
            name = "synthetic-1.dist-info/METADATA"
            offset = archive.getinfo(name).header_offset + 30 + len(name)
        with self.wheel.open("r+b") as stream:
            stream.seek(offset)
            value = stream.read(1)
            stream.seek(offset)
            stream.write(bytes([value[0] ^ 255]))
        digest = hashlib.sha256(self.wheel.read_bytes()).hexdigest()
        with self.assertRaises(review.ReviewFailure):
            review.inspect_hub(
                self.wheel, self.wheel.stat().st_size, digest, review.Counter(2**23)
            )

    def test_wheel_hardlink_refused_with_sanitized_code(self):
        size, digest = self.fixture()
        os.link(self.wheel, self.root / "alias")
        with self.assertRaisesRegex(review.ReviewFailure, "file_type"):
            review.inspect_hub(self.wheel, size, digest, review.Counter(2**23))

    def test_reparse_refused_without_candidate_read(self):
        primitive = review.load_primitives(review.Counter(2**20))
        size, digest = self.fixture()
        with (
            patch.object(review, "load_primitives", return_value=primitive),
            patch.object(primitive, "is_reparse", return_value=True),
            self.assertRaises(review.ReviewFailure),
        ):
            review.inspect_hub(self.wheel, size, digest, review.Counter(2**23))

    def test_file_change_between_hash_and_member_reads(self):
        primitive = review.load_primitives(review.Counter(2**20))
        size, digest = self.fixture()
        original = primitive.hash_regular

        def change_after_hash(*args):
            value = original(*args)
            self.wheel.write_bytes(b"changed after hashing")
            return value

        with (
            patch.object(review, "load_primitives", return_value=primitive),
            patch.object(primitive, "hash_regular", side_effect=change_after_hash),
            self.assertRaisesRegex(review.ReviewFailure, "wheel_identity"),
        ):
            review.inspect_hub(self.wheel, size, digest, review.Counter(2**23))

    def test_receipt_cannot_target_fixture_or_old_root(self):
        target = self.root / "receipt.json"
        with self.assertRaisesRegex(review.ReviewFailure, "receipt_root"):
            review.save_json(target, {"inert": True})
        self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
