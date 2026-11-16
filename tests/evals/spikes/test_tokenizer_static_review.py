"""Synthetic-only controls for the approved static artifact review."""

import base64
import csv
import hashlib
import io
import json
import tempfile
import time
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import tokenizer_static_review as review


def wheel(extra=None, corrupt=False, duplicate=False):
    """Build inert wheel-like bytes with an independently authored RECORD."""
    prefix = "tokenizers-0.23.3.dist-info/"
    files = {
        prefix
        + "METADATA": b"Name: tokenizers\nVersion: 0.23.3\nRequires-Python: >=3.10\nRequires-Dist: huggingface_hub>=0.16.4,<3.0\n\n",
        prefix + "WHEEL": b"Wheel-Version: 1.0\nTag: cp310-abi3-win_amd64\n\n",
        "tokenizers/inert.py": b"raise RuntimeError('never execute')\n",
    }
    files.update(extra or {})
    record = prefix + "RECORD"
    out = io.StringIO()
    writer = csv.writer(out)
    for name, content in files.items():
        digest = (
            base64.urlsafe_b64encode(hashlib.sha256(content).digest())
            .rstrip(b"=")
            .decode()
        )
        writer.writerow(
            [
                name.filename if isinstance(name, zipfile.ZipInfo) else name,
                "sha256=" + digest,
                len(content),
            ]
        )
    writer.writerow([record, "", ""])
    files[record] = out.getvalue().encode()
    if corrupt:
        files["tokenizers/inert.py"] += b"changed"
    data = io.BytesIO()
    with zipfile.ZipFile(data, "w") as archive:
        for name, content in files.items():
            archive.writestr(name, content)
        if duplicate:
            archive.writestr("TOKENIZERS/INERT.PY", b"alias")
    return data.getvalue()


class StaticReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        state = {
            "status": "active",
            "started_utc": time.time(),
            "http_reserved": 0,
            "events": [],
            "body_reserved": {"metadata": 0, "asset": 0, "wheel": 0},
        }
        (self.root / "meter.json").write_text(json.dumps(state))
        self.budget = review.Budget(self.root)

    def test_precharge_is_durable_before_transport(self):
        self.budget.reserve_body("asset", 17)
        self.budget.transaction("https://pypi.org/pypi/tokenizers/0.23.3/json")
        state = json.loads((self.root / "meter.json").read_text())
        self.assertEqual(state["body_reserved"]["asset"], 17)
        self.assertEqual(state["http_reserved"], 1)

    def test_closed_epoch_and_request_cap_refuse(self):
        for update in ({"status": "closed"}, {"http_reserved": 48}):
            state = json.loads((self.root / "meter.json").read_text())
            state.update(update)
            (self.root / "meter.json").write_text(json.dumps(state))
            with self.assertRaises(ValueError):
                self.budget.transaction("https://pypi.org/pypi/tokenizers/0.23.3/json")
            state["status"] = "active"
            (self.root / "meter.json").write_text(json.dumps(state))

    def test_body_budget_has_no_refund(self):
        self.budget.reserve_body("asset", 14 * review.MIB)
        with self.assertRaises(ValueError):
            self.budget.reserve_body("asset", 1)

    def test_interrupted_atomic_write_propagates(self):
        with (
            patch.object(review.os, "replace", side_effect=OSError("interrupted")),
            self.assertRaises(OSError),
        ):
            self.budget.reserve_body("asset", 1)
        self.assertTrue((self.root / "meter.pending").exists())

    def test_urls_are_exact_and_queries_do_not_grant_authority(self):
        good = (
            "https://huggingface.co/"
            + review.ASSETS[0][0]
            + "/resolve/"
            + review.ASSETS[0][1]
            + "/tokenizer.json"
        )
        review.allowed_url(good)
        for url in (
            good.replace("https:", "http:"),
            good + "?token=secret",
            good.replace("tokenizer.json", "model.safetensors"),
            good.replace("5fee7c4", "0000000"),
            "https://localhost/",
            "https://pypi.org/pypi/tokenizers/0.23.4/json",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                review.allowed_url(url)

    def test_private_dns_refused_before_open(self):
        with patch.object(
            review.socket,
            "getaddrinfo",
            return_value=[(2, 1, 6, "", ("127.0.0.1", 443))],
        ), self.assertRaises(ValueError):
            review.public_addresses("pypi.org")

    def test_stream_caps_size_digest_and_partial_read(self):
        for cap, size, digest in ((2, None, None), (10, 4, None), (10, 3, "0" * 64)):
            with self.assertRaises(ValueError):
                review.read_body(io.BytesIO(b"abc"), cap, size, digest)
        self.assertEqual(
            review.read_body(
                io.BytesIO(b"abc"), 3, 3, hashlib.sha256(b"abc").hexdigest()
            ),
            b"abc",
        )

    def test_output_traversal_and_reparse_refused(self):
        with self.assertRaises(ValueError):
            self.budget.output("../outside", b"x")
        with patch.object(review, "is_reparse", return_value=True), self.assertRaises(ValueError):
            self.budget.output("safe", b"x")

    def test_existing_output_is_not_overwritten(self):
        self.budget.output("one", b"a")
        with self.assertRaises(FileExistsError):
            self.budget.output("one", b"b")

    def test_record_verified_without_executing_member(self):
        result = review.inspect_wheel(
            wheel(), "tokenizers", "0.23.3", "cp310-abi3-win_amd64", 32 * review.MIB
        )
        self.assertEqual(result["version"], "0.23.3")
        self.assertEqual(result["requires_dist"], ["huggingface_hub>=0.16.4,<3.0"])

    def test_record_corruption_and_alias_refused(self):
        for blob in (wheel(corrupt=True), wheel(duplicate=True)):
            with self.assertRaises(ValueError):
                review.inspect_wheel(
                    blob,
                    "tokenizers",
                    "0.23.3",
                    "cp310-abi3-win_amd64",
                    32 * review.MIB,
                )

    def test_archive_traversal_symlink_and_expansion_refused(self):
        link = zipfile.ZipInfo("link")
        link.create_system = 3
        link.external_attr = 0o120777 << 16
        for extra in ({"../escape": b"x"}, {link: b"target"}):
            with self.assertRaises(ValueError):
                review.inspect_wheel(
                    wheel(extra),
                    "tokenizers",
                    "0.23.3",
                    "cp310-abi3-win_amd64",
                    32 * review.MIB,
                )
        with self.assertRaises(ValueError):
            review.inspect_wheel(
                wheel(), "tokenizers", "0.23.3", "cp310-abi3-win_amd64", 1
            )

    def test_wheel_identity_refused(self):
        for name, version, tag in (
            ("other", "0.23.3", "cp310-abi3-win_amd64"),
            ("tokenizers", "0.23.4", "cp310-abi3-win_amd64"),
            ("tokenizers", "0.23.3", "py3-none-any"),
        ):
            with self.assertRaises(ValueError):
                review.inspect_wheel(wheel(), name, version, tag, 32 * review.MIB)

    def test_asset_hash_is_not_publisher_attestation(self):
        result = review.asset_identity(b"abc", None)
        self.assertEqual(result["sha256"], hashlib.sha256(b"abc").hexdigest())
        self.assertTrue(result["publisher_digest_unavailable"])
        with self.assertRaises(ValueError):
            review.asset_identity(b"abc", {"lfs": {"oid": "0" * 64}})

    def test_redirect_bound_and_error_body_charged(self):
        with (
            patch.object(review, "public_addresses"),
            patch.object(review.urllib.request, "build_opener") as factory,
        ):
            error = review.urllib.error.HTTPError(
                "https://pypi.org/pypi/tokenizers/0.23.3/json",
                302,
                "redirect",
                {"Location": "https://localhost/private"},
                io.BytesIO(b"no"),
            )
            factory.return_value.open.side_effect = error
            with self.assertRaises(ValueError):
                review.fetch(
                    self.budget,
                    "https://pypi.org/pypi/tokenizers/0.23.3/json",
                    "metadata",
                    100,
                )
            self.assertEqual(factory.return_value.open.call_count, 1)
            self.assertEqual(
                json.loads((self.root / "meter.json").read_text())["events"][0][
                    "bytes"
                ],
                2,
            )

    def test_success_and_declared_encoding_refusal(self):
        for encoding in ("identity", "gzip"):
            response = io.BytesIO(b"abc")
            response.headers = {"Content-Length": "3", "Content-Encoding": encoding}
            with (
                patch.object(review, "public_addresses"),
                patch.object(review.urllib.request, "build_opener") as factory,
            ):
                factory.return_value.open.return_value = response
                if encoding == "identity":
                    self.assertEqual(
                        review.fetch(
                            self.budget,
                            "https://pypi.org/pypi/tokenizers/0.23.3/json",
                            "metadata",
                            3,
                            3,
                        ),
                        b"abc",
                    )
                else:
                    with self.assertRaises(ValueError):
                        review.fetch(
                            self.budget,
                            "https://pypi.org/pypi/tokenizers/0.23.3/json",
                            "metadata",
                            3,
                            3,
                        )

    def test_redirect_limit_is_shared_and_not_retried(self):
        url = "https://pypi.org/pypi/tokenizers/0.23.3/json"
        errors = [
            review.urllib.error.HTTPError(
                url, 302, "redirect", {"Location": url}, io.BytesIO(b"")
            )
            for _ in range(3)
        ]
        with (
            patch.object(review, "public_addresses"),
            patch.object(review.urllib.request, "build_opener") as factory,
        ):
            factory.return_value.open.side_effect = errors
            with self.assertRaises(ValueError):
                review.fetch(self.budget, url, "metadata", 10)
            self.assertEqual(factory.return_value.open.call_count, 3)

    def test_startup_file_refused(self):
        with self.assertRaises(ValueError):
            review.inspect_wheel(
                wheel({"unsafe.pth": b"import unsafe"}),
                "tokenizers",
                "0.23.3",
                "cp310-abi3-win_amd64",
                32 * review.MIB,
            )


if __name__ == "__main__":
    unittest.main()
