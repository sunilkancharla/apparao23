"""Synthetic artifact-inspection controls; wheel code is never executed."""

import base64
import csv
import hashlib
import io
import json
import stat
import struct
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sqlite_vec_artifact as target


def wheel(entries=None):
    """Make a tiny authored wheel with independently generated RECORD hashes."""
    entries = entries or {"pkg/__init__.py": b"VALUE = 1\n"}
    rows = []
    for name, content in entries.items():
        digest = (
            base64.urlsafe_b64encode(hashlib.sha256(content).digest())
            .rstrip(b"=")
            .decode()
        )
        rows.append([name, "sha256=" + digest, str(len(content))])
    rows.append(["pkg.dist-info/RECORD", "", ""])
    record = io.StringIO()
    csv.writer(record, lineterminator="\n").writerows(rows)
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in entries.items():
            archive.writestr(name, content)
        archive.writestr("pkg.dist-info/RECORD", record.getvalue())
    return output.getvalue()


class ArtifactContracts(unittest.TestCase):
    """Exercise validation, accounting and refusal before simulated progression."""

    def test_safe_archive_and_record(self):
        files = target.inspect_zip(wheel())
        self.assertEqual(files["pkg/__init__.py"], b"VALUE = 1\n")

    def test_windows_path_collision_and_traversal_refused(self):
        for name in (
            "../outside",
            "/absolute",
            "C:/drive",
            "a:ads",
            "a\\b",
            "CON",
            "a.",
            "a/../b",
        ):
            with self.subTest(name=name), self.assertRaises(ValueError):
                target.inspect_zip(wheel({name: b"x"}))
        with self.assertRaises(ValueError):
            target.inspect_zip(wheel({"A.py": b"a", "a.py": b"b"}))

    def test_symlink_and_expansion_limit_refused(self):
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w") as archive:
            entry = zipfile.ZipInfo("link")
            entry.create_system = 3
            entry.external_attr = (stat.S_IFLNK | 0o777) << 16
            archive.writestr(entry, "target")
        with self.assertRaises(ValueError):
            target.inspect_zip(output.getvalue())
        with self.assertRaises(ValueError):
            target.inspect_zip(wheel({"bomb": b"a" * 200000}))

    def test_corrupt_record_stops_simulated_loading(self):
        acted = []
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w") as archive:
            archive.writestr("pkg/a.py", b"VALUE = 1")
            archive.writestr(
                "pkg.dist-info/RECORD",
                "pkg/a.py,sha256=wrong,9\npkg.dist-info/RECORD,,\n",
            )
        with self.assertRaises(ValueError):
            target.inspect_zip(output.getvalue())
            acted.append("simulated-load")
        self.assertEqual(acted, [])

    def test_hash_mismatch_and_truncated_transfer(self):
        for body, declared, digest in ((b"short", 8, None), (b"data", 4, "0" * 64)):
            with self.assertRaises(ValueError):
                target.read_body(io.BytesIO(body), 16, declared, digest)

    def test_stream_cap_and_byte_count_on_failure(self):
        counts = []
        with self.assertRaises(ValueError):
            target.read_body(io.BytesIO(b"12345"), 4, None, None, counts.append)
        self.assertEqual(sum(counts), 5)

    def test_http_meter_persists_before_request_and_blocks_extension(self):
        with tempfile.TemporaryDirectory(dir=target.RUN) as directory:
            path = Path(directory) / "budget.json"
            path.write_text(
                json.dumps(
                    {
                        "requests": 19,
                        "request_limit": 20,
                        "reserved_bytes": 0,
                        "byte_limit": 10,
                        "actual_bytes": 0,
                        "events": [],
                    }
                )
            )
            target.reserve_http(path, "synthetic", 10)
            saved = json.loads(path.read_bytes())
            self.assertEqual(saved["requests"], 20)
            self.assertEqual(saved["reserved_bytes"], 10)
            with self.assertRaises(RuntimeError):
                target.reserve_http(path, "synthetic", 1)

    def test_pe_invalid_offsets_and_non_x64_refused(self):
        for value in (b"", b"MZ" + b"\x00" * 60 + struct.pack("<I", 999999), b"notPE"):
            with self.assertRaises(ValueError):
                target.inspect_pe(value)

    def test_valid_minimal_pe_and_wrong_machine(self):
        image = bytearray(512)
        image[:2] = b"MZ"
        struct.pack_into("<I", image, 60, 64)
        image[64:68] = b"PE\x00\x00"
        struct.pack_into("<HHIIIHH", image, 68, 0x8664, 1, 0, 0, 0, 240, 0x2000)
        struct.pack_into("<H", image, 88, 0x20B)
        struct.pack_into("<8sIIII", image, 328, b".text\x00\x00\x00", 32, 4096, 32, 400)
        self.assertEqual(target.inspect_pe(bytes(image))["machine"], "AMD64")
        struct.pack_into("<H", image, 68, 0x14C)
        with self.assertRaises(ValueError):
            target.inspect_pe(bytes(image))

    def test_http_byte_reservation_exhaustion_persists(self):
        with tempfile.TemporaryDirectory(dir=target.RUN) as directory:
            path = Path(directory) / "budget.json"
            state = {
                "requests": 0,
                "request_limit": 20,
                "reserved_bytes": 9,
                "byte_limit": 10,
                "actual_bytes": 0,
                "events": [],
            }
            path.write_text(json.dumps(state))
            with self.assertRaises(RuntimeError):
                target.reserve_http(path, "synthetic", 2)
            self.assertEqual(json.loads(path.read_bytes()), state)

    def test_destination_and_redirect_allowlist(self):
        for url in (
            "http://pypi.org/pypi/sqlite-vec/0.1.9/json",
            "https://example.invalid/x",
            "https://pypi.org/other",
            "https://user:secret@pypi.org/pypi/sqlite-vec/0.1.9/json",
        ):
            with self.assertRaises(ValueError):
                target.allowed_url(url)
        target.allowed_url(target.WHEEL_URL)


if __name__ == "__main__":
    from appcontainer_preflight import Native

    native = Native()
    job = native.job(1, kill=False)
    native.check(
        native.kernel.AssignProcessToJobObject(job, native.kernel.GetCurrentProcess())
    )
    target.watchdog()
    unittest.main()
