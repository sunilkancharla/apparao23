"""Injected-transport controls for the ten-file continuation; no real sockets."""

import contextlib
import io
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import remaining_asset_review as review


def state():
    return {
        "status": "active",
        "started_utc": time.time(),
        "http_reserved": 0,
        "body_reserved": {"metadata": 0, "asset": 0, "wheel": 0},
        "events": [],
        "worker_started": False,
    }


class RemainingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "meter.json").write_text(json.dumps(state()))
        (self.root / "reporting.jsonl").write_text("")
        self.budget = review.Budget(self.root, synthetic=True)
        self.addCleanup(self.budget.close)

    def test_exact_remaining_set_and_version(self):
        self.assertEqual(sum(len(files) for _, _, files in review.REMAINING), 10)
        good = review.asset_url(*review.REMAINING[0][:2], "tokenizer_config.json")
        review.allowed_url(good)
        for bad in (
            good.replace("tokenizer_config.json", "tokenizer.json"),
            good.replace("5fee7c4", "0000000"),
            good.replace("huggingface.co", "pypi.org"),
            good + "?token=secret",
        ):
            with self.assertRaises(ValueError):
                review.allowed_url(bad)

    def test_every_write_stage_failure_prevents_transport(self):
        for stage in review.STAGES:
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as name:
                root = Path(name)
                (root / "meter.json").write_text(json.dumps(state()))
                error = PermissionError(13, "never-log-path")
                error.winerror = 5
                budget = review.Budget(root, synthetic=True, faults={stage: error})
                try:
                    url = review.tree_url(*review.REMAINING[0][:2])
                    with (
                        patch.object(review.BASE, "public_addresses"),
                        patch.object(
                            review.BASE.urllib.request, "build_opener"
                        ) as factory,
                    ):
                        with self.assertRaises(review.PersistenceFailure) as caught:
                            review.fetch(budget, url, "metadata", 100)
                        self.assertEqual(caught.exception.stage, stage)
                        factory.return_value.open.assert_not_called()
                    self.assertEqual(
                        json.loads((root / "meter.json").read_text())["http_reserved"],
                        0,
                    )
                    journal = (root / "operations.jsonl").read_text()
                    self.assertNotIn("never-log-path", journal)
                    self.assertIn('"failure"', journal)
                finally:
                    budget.close()

    def test_precharge_and_lower_request_limit(self):
        value = state()
        value["http_reserved"] = 39
        self.budget.save(value)
        self.budget.transaction(review.tree_url(*review.REMAINING[0][:2]))
        self.assertEqual(self.budget.state()["http_reserved"], 40)
        with self.assertRaises(ValueError):
            self.budget.transaction(review.tree_url(*review.REMAINING[0][:2]))

    def test_lower_category_and_body_limits(self):
        for category, size in (("asset", 8 * review.MIB), ("metadata", 4 * review.MIB)):
            value = state()
            value["body_reserved"][category] = size
            self.budget.save(value)
            with self.assertRaises(ValueError):
                self.budget.reserve_body(category, 1)
        with self.assertRaises(ValueError):
            self.budget.reserve_body("wheel", 1)
        with patch.object(review.BASE, "fetch") as transport:
            with self.assertRaises(ValueError):
                review.fetch(
                    self.budget,
                    review.asset_url(*review.REMAINING[0][:2], "vocab.json"),
                    "asset",
                    4 * review.MIB + 1,
                )
            transport.assert_not_called()

    def test_redirect_cannot_reach_old_registry_policy(self):
        url = review.tree_url(*review.REMAINING[0][:2])
        error = review.BASE.urllib.error.HTTPError(
            url,
            307,
            "redirect",
            {"Location": "https://pypi.org/pypi/tokenizers/0.23.3/json"},
            io.BytesIO(b""),
        )
        with (
            patch.object(review.BASE, "public_addresses"),
            patch.object(review.BASE.urllib.request, "build_opener") as factory,
        ):
            factory.return_value.open.side_effect = error
            with self.assertRaises(ValueError):
                review.BASE.fetch(self.budget, url, "metadata", 100)
            self.assertEqual(factory.return_value.open.call_count, 1)

    def test_redirect_cannot_switch_to_another_allowed_file(self):
        publisher, revision, _ = review.REMAINING[0]
        url = review.asset_url(publisher, revision, "vocab.json")
        other = review.asset_url(publisher, revision, "merges.txt")
        error = review.BASE.urllib.error.HTTPError(
            url, 307, "redirect", {"Location": other}, io.BytesIO(b"")
        )
        with (
            patch.object(review.BASE, "public_addresses"),
            patch.object(review.BASE.urllib.request, "build_opener") as factory,
        ):
            factory.return_value.open.side_effect = error
            with self.assertRaises(ValueError):
                review.fetch(self.budget, url, "asset", 100)
            self.assertEqual(factory.return_value.open.call_count, 1)
        self.assertIs(review.BASE.allowed_url, review.allowed_url)

    def test_transport_sees_durable_transaction_precharge(self):
        response = io.BytesIO(b"abc")
        response.headers = {"Content-Length": "3"}

        def open_response(*args, **kwargs):
            persisted = json.loads((self.root / "meter.json").read_text())
            self.assertEqual(persisted["http_reserved"], 1)
            self.assertFalse((self.root / "meter.pending").exists())
            return response

        with (
            patch.object(review.BASE, "public_addresses"),
            patch.object(review.BASE.urllib.request, "build_opener") as factory,
        ):
            factory.return_value.open.side_effect = open_response
            self.assertEqual(
                review.fetch(
                    self.budget,
                    review.tree_url(*review.REMAINING[0][:2]),
                    "metadata",
                    3,
                    3,
                ),
                b"abc",
            )

    def test_encoding_and_partial_size_stop_without_retry(self):
        for encoding, body in (("gzip", b"abc"), ("identity", b"a")):
            response = io.BytesIO(body)
            response.headers = {"Content-Encoding": encoding, "Content-Length": "3"}
            with (
                patch.object(review.BASE, "public_addresses"),
                patch.object(review.BASE.urllib.request, "build_opener") as factory,
            ):
                factory.return_value.open.return_value = response
                with self.assertRaises(ValueError):
                    review.fetch(
                        self.budget,
                        review.tree_url(*review.REMAINING[0][:2]),
                        "metadata",
                        3,
                        3,
                    )
                self.assertEqual(factory.return_value.open.call_count, 1)

    def test_output_path_reparse_and_smaller_cap(self):
        with self.assertRaises(ValueError):
            self.budget.output("../outside", b"x")
        with (
            patch.object(review.BASE, "is_reparse", return_value=True),
            self.assertRaises(ValueError),
        ):
            self.budget.output("x", b"y")
        with (
            patch.object(self.budget, "tree_bytes", return_value=16 * review.MIB),
            self.assertRaises(ValueError),
        ):
            self.budget.output("x", b"y")

    def test_closed_claim_and_old_root_refused(self):
        self.budget.claim()
        with self.assertRaises(FileExistsError):
            self.budget.claim()
        with self.assertRaises(ValueError):
            review.Budget(review.BASE.RUN)
        value = state()
        value["status"] = "closed"
        (self.root / "meter.json").write_text(json.dumps(value))
        with self.assertRaises(ValueError):
            self.budget.reserve_body("asset", 1)

    def test_diagnostic_failure_does_not_publish(self):
        with (
            patch.object(self.budget, "trace", side_effect=OSError("journal failure")),
            self.assertRaises(OSError),
        ):
            self.budget.save(state())
        self.assertFalse((self.root / "meter.pending").exists())

    def test_reporting_rejects_objects_and_enforces_both_caps(self):
        with self.assertRaises(TypeError):
            review.scalar_text({"provider": object()})
        with self.assertRaises(ValueError):
            review.scalar_text({str(i): "x" * 512 for i in range(32)})
        (self.root / "reporting.jsonl").write_text('{"bytes":114688}\n')
        with self.assertRaises(ValueError), contextlib.redirect_stdout(io.StringIO()):
            review.report_scalar(self.root, {"status": "must refuse"})

    def test_reporting_charged_before_print(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            review.report_scalar(self.root, {"status": "ok", "count": 1})
        row = json.loads((self.root / "reporting.jsonl").read_text())
        self.assertEqual(row["bytes"], len(output.getvalue().encode()))

    def test_bad_publisher_and_digest_metadata_refused(self):
        for item in (
            {"type": "file", "path": "vocab.json", "size": True},
            {"type": "file", "path": "vocab.json", "size": 4 * review.MIB + 1},
        ):
            with self.assertRaises(ValueError):
                review.select_item([item], "vocab.json")
        with self.assertRaises(ValueError):
            review.BASE.asset_identity(b"abc", {"oid": "0" * 40})
        with self.assertRaises(ValueError):
            review.BASE.asset_identity(b"abc", {"lfs": {"oid": "0" * 64}})


if __name__ == "__main__":
    unittest.main()
