"""Synthetic, local-only tests for the bounded wheel investigation."""

from __future__ import annotations

import base64
import contextlib
import csv
import hashlib
import importlib.util
import io
import os
import struct
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = Path("F:/document_assistant/data/t17/wheel-artifact-review-02")
spec = importlib.util.spec_from_file_location(
    "wheel_static_inspection", HERE / "wheel_static_inspection.py"
)
aid = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = aid
spec.loader.exec_module(aid)


def wheel(path: Path, changes=None, extra=None, tag="py3-none-any"):
    """Author a small wheel and its RECORD without importing its payload."""
    contents = {
        "demo/__init__.py": b"raise RuntimeError('CANDIDATE EXECUTED')\n",
        "demo-1.0.dist-info/METADATA": b"Metadata-Version: 2.4\nName: demo\nVersion: 1.0\nLicense-Expression: MIT\nLicense-File: LICENSE\nRequires-Dist: example>=1\n\n",
        "demo-1.0.dist-info/WHEEL": (
            "Wheel-Version: 1.0\nTag: " + tag + "\n\n"
        ).encode(),
        "demo-1.0.dist-info/licenses/LICENSE": b"MIT License\nSynthetic notice\n",
    }
    contents.update(extra or {})
    rows = []
    for name, body in contents.items():
        digest = (
            base64.urlsafe_b64encode(hashlib.sha256(body).digest())
            .rstrip(b"=")
            .decode()
        )
        rows.append((name, "sha256=" + digest, str(len(body))))
    rows.append(("demo-1.0.dist-info/RECORD", "", ""))
    out = io.StringIO(newline="")
    csv.writer(out).writerows(rows)
    contents[rows[-1][0]] = out.getvalue().encode()
    contents.update(changes or {})
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, body in contents.items():
            archive.writestr(name, body)
    return {
        "filename": path.name,
        "distribution": "demo",
        "version": "1.0",
        "size": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "cap": 262144,
    }


class FakeSocket:
    def __init__(self, data):
        self.data = io.BytesIO(data)

    def recv(self, amount):
        return self.data.read(amount)


class PureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT, prefix="synthetic-")
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def metadata(self):
        spec = {
            "filename": "demo-1.0-py3-none-any.whl",
            "distribution": "demo",
            "version": "1.0",
            "size": 20,
            "sha256": "a" * 64,
            "cap": 256,
        }
        entry = {
            "filename": spec["filename"],
            "size": 20,
            "digests": {"sha256": spec["sha256"]},
            "yanked": False,
            "url": "https://files.pythonhosted.org/packages/x/demo-1.0-py3-none-any.whl",
        }
        return spec, {"info": {"name": "demo", "version": "1.0"}, "urls": [entry]}

    def test_exact_entry(self):
        expected, metadata = self.metadata()
        actual = aid.admit_entry(metadata, expected)
        self.assertIsInstance(actual, dict)
        self.assertEqual(actual["size"], 20)
        self.assertEqual(actual["sha256"], "a" * 64)

    def test_metadata_rejections(self):
        for field, value in (
            ("size", True),
            ("size", 19),
            ("yanked", True),
            ("filename", "other.whl"),
            ("url", "https://user@files.pythonhosted.org/x"),
            ("url", "https://files.pythonhosted.org/x?q=1"),
        ):
            with self.subTest(field=field, value=value):
                expected, meta = self.metadata()
                meta["urls"][0][field] = value
                with self.assertRaises(aid.Failure):
                    aid.admit_entry(meta, expected)
        expected, meta = self.metadata()
        meta["urls"] *= 2
        with self.assertRaises(aid.Failure):
            aid.admit_entry(meta, expected)

    def test_duplicate_json(self):
        with self.assertRaises(aid.Failure):
            aid.parse_json(b'{"x":1,"x":2}')

    def test_artifact_evidence_is_not_console_output(self):
        path = self.root / "evidence.json"
        aid.save(path, {"text": "x" * 131073})
        self.assertGreater(path.stat().st_size, 131072)
        with self.assertRaises(aid.Failure):
            aid.save(self.root / "over-cap.json", {"text": "x" * 20}, cap=10)

    def test_fixed_artifacts_match_approved_source(self):
        source = (
            HERE.parents[2] / "docs/proposals/wheel-static-inspection.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(len(aid.FIXED_SPECS), 8)
        for entry in aid.FIXED_SPECS:
            self.assertIn(entry["filename"], source)
            self.assertIn(entry["sha256"], source)

    def test_tls_failure_is_not_retried(self):
        raw = unittest.mock.MagicMock()
        raw.__enter__.return_value = raw
        context = unittest.mock.MagicMock()
        context.wrap_socket.side_effect = aid.ssl.SSLError("synthetic TLS refusal")
        with (
            patch.object(aid, "address", return_value=(2, 1, 6, "", ("8.8.8.8", 443))),
            patch.object(aid.socket, "socket", return_value=raw),
            patch.object(aid.ssl, "create_default_context", return_value=context),
            self.assertRaises(aid.ssl.SSLError),
        ):
            aid.fetch("https://pypi.org/x", 4, aid.Budget(), io.BytesIO())
        raw.connect.assert_called_once()
        context.wrap_socket.assert_called_once()

    def test_url_and_dns(self):
        for url in (
            "http://pypi.org/x",
            "https://evil.example/x",
            "https://pypi.org:444/x",
            "https://pypi.org/x#y",
            "https://u:p@pypi.org/x",
        ):
            with self.assertRaises(aid.Failure):
                aid.check_url(url)
        public = [(2, 1, 6, "", ("8.8.8.8", 443))]
        with patch.object(aid.socket, "getaddrinfo", return_value=public):
            self.assertEqual(aid.address("pypi.org")[4][0], "8.8.8.8")
        for rows in (
            [(2, 1, 6, "", ("127.0.0.1", 443))],
            public + [(2, 1, 6, "", ("10.0.0.1", 443))],
        ):
            with (
                patch.object(aid.socket, "getaddrinfo", return_value=rows),
                self.assertRaises(aid.Failure),
            ):
                aid.address("pypi.org")

    def test_http_and_caps(self):
        output = io.BytesIO()
        self.assertEqual(
            aid.receive(
                FakeSocket(b"HTTP/1.1 200 OK\r\nContent-Length: 3\r\n\r\nabc"),
                3,
                aid.Budget(),
                output,
            ),
            3,
        )
        self.assertEqual(output.getvalue(), b"abc")
        for response in (
            b"HTTP/1.1 302 Found\r\nContent-Length: 0\r\n\r\n",
            b"HTTP/1.1 200 OK\r\nContent-Length: 4\r\n\r\nabcd",
            b"HTTP/1.1 200 OK\r\nContent-Length: 3\r\n\r\na",
            b"HTTP/1.1 200 OK\r\nContent-Length: 3\r\nContent-Length: 3\r\n\r\nabc",
            b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n",
            b"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Length: 1\r\n\r\na",
        ):
            with self.assertRaises(aid.Failure):
                aid.receive(FakeSocket(response), 3, aid.Budget(), io.BytesIO())
        with self.assertRaises(aid.Failure):
            aid.receive(
                FakeSocket(b"HTTP/1.1 200 OK\r\nContent-Length: 3\r\n\r\nabc"),
                3,
                aid.Budget(read_limit=1),
                io.BytesIO(),
            )

    def test_inert_wheel(self):
        path = self.root / "demo-1.0-py3-none-any.whl"
        expected = wheel(path)
        result = aid.inspect_wheel(path, expected, aid.Budget())
        self.assertEqual(result["record_verified"], 4)
        self.assertEqual(result["license_expression"], "MIT")
        self.assertEqual(result["requirements"], ["example>=1"])

    def test_record_hash_and_license_rejections(self):
        path = self.root / "demo-1.0-py3-none-any.whl"
        for changes in (
            {"demo/__init__.py": b"altered"},
            {"demo-1.0.dist-info/licenses/LICENSE": b"changed"},
            {"demo-1.0.dist-info/RECORD": b"demo/__init__.py,,\n"},
        ):
            expected = wheel(path, changes=changes)
            with self.assertRaises(aid.Failure):
                aid.inspect_wheel(path, expected, aid.Budget())
        expected = wheel(path)
        expected["sha256"] = "0" * 64
        with self.assertRaises(aid.Failure):
            aid.inspect_wheel(path, expected, aid.Budget())

    def test_zip_paths_and_limits(self):
        path = self.root / "demo-1.0-py3-none-any.whl"
        for name in ("../escape", "CON.txt", "a:b", "a/../b", "A", "a\\b"):
            extras = {name: b"x"}
            if name == "A":
                extras["a"] = b"x"
            expected = wheel(path, extra=extras)
            with self.assertRaises(aid.Failure):
                aid.inspect_wheel(path, expected, aid.Budget())
        expected = wheel(path, extra={f"f{i}": b"" for i in range(513)})
        with (
            patch.object(
                aid.zipfile,
                "ZipFile",
                side_effect=AssertionError("allocated too early"),
            ),
            self.assertRaises(aid.Failure),
        ):
            aid.inspect_wheel(path, expected, aid.Budget())
        expected = wheel(path)
        with self.assertRaises(aid.Failure):
            aid.inspect_wheel(path, expected, aid.Budget(expand_limit=1))

    def test_local_header_and_crc(self):
        path = self.root / "demo-1.0-py3-none-any.whl"
        expected = wheel(path)
        body = bytearray(path.read_bytes())
        struct.pack_into("<H", body, 8, 8)
        path.write_bytes(body)
        expected.update(size=len(body), sha256=hashlib.sha256(body).hexdigest())
        with self.assertRaises(aid.Failure):
            aid.inspect_wheel(path, expected, aid.Budget())
        expected = wheel(path)
        body = bytearray(path.read_bytes())
        names, extra = struct.unpack_from("<HH", body, 26)
        body[30 + names + extra] ^= 1
        path.write_bytes(body)
        expected.update(size=len(body), sha256=hashlib.sha256(body).hexdigest())
        with self.assertRaises(aid.Failure):
            aid.inspect_wheel(path, expected, aid.Budget())

    def test_overlap_layout(self):
        raw = bytearray(100)
        entries = []
        for start, name, size in ((0, "a", 10), (35, "b", 0)):
            struct.pack_into(
                "<4s5H3I2H",
                raw,
                start,
                b"PK\x03\x04",
                20,
                0,
                0,
                0,
                0,
                0,
                size,
                size,
                1,
                0,
            )
            raw[start + 30] = ord(name)
            entries.append(
                SimpleNamespace(
                    header_offset=start,
                    flag_bits=0,
                    compress_type=0,
                    CRC=0,
                    compress_size=size,
                    file_size=size,
                    orig_filename=name,
                    extra=b"",
                )
            )
        with self.assertRaises(aid.Failure) as caught:
            aid.local_layout(io.BytesIO(raw), SimpleNamespace(start_dir=100), entries)
        self.assertEqual(caught.exception.code, "local_overlap")

    def test_license_tags_and_inert_hooks(self):
        path = self.root / "demo-1.0-py3-none-any.whl"
        expected = wheel(path, tag="cp310-abi3-win_amd64")
        with self.assertRaises(aid.Failure):
            aid.inspect_wheel(path, expected, aid.Budget())
        expected = wheel(
            path,
            extra={"trap.pth": b"import nonexistent;raise RuntimeError('EXECUTED')"},
        )
        result = aid.inspect_wheel(path, expected, aid.Budget())
        self.assertIn("trap.pth", result["hooks"])
        missing = (
            b"Metadata-Version: 2.4\nName: demo\nVersion: 1.0\nLicense-File: absent\n\n"
        )
        expected = wheel(path, changes={"demo-1.0.dist-info/METADATA": missing})
        with self.assertRaises(aid.Failure):
            aid.inspect_wheel(path, expected, aid.Budget())

    def test_integrity_mutation(self):
        path = self.root / "demo-1.0-py3-none-any.whl"
        expected = wheel(path)
        expected["sha256"] = "0" * 64
        # Disabling file integrity makes the real expectation fail, which is caught.
        with (
            patch.object(aid, "hash_regular", return_value="0" * 64),
            self.assertRaises(AssertionError),
            self.assertRaises(aid.Failure),
        ):
            aid.inspect_wheel(path, expected, aid.Budget())


class JobTests(unittest.TestCase):
    def test_startup_gate_and_owned_exit(self):
        result = aid.supervise_code(b"print('owned')\n", 5, ROOT, parent_pid=None)
        self.assertEqual(result["stdout"].strip(), "owned")
        self.assertTrue(result["assigned"])
        self.assertTrue(result["teardown_verified"])
        self.assertGreater(result["memory_samples"], 0)

    def test_timeout_and_gate_refusal(self):
        with self.assertRaises(aid.Failure):
            aid.supervise_code(
                b"import time;time.sleep(10)\n", 0.2, ROOT, parent_pid=None
            )
        with (
            patch.object(
                aid.Job,
                "assign",
                side_effect=aid.Failure("synthetic_assignment_refusal"),
            ),
            self.assertRaises(aid.Failure),
        ):
            aid.supervise_code(
                b"raise RuntimeError('GATE OPENED')\n", 2, ROOT, parent_pid=None
            )

    def test_parent_shell_memory_coverage(self):
        result = aid.supervise_code(
            b"print('sampled')\n", 5, ROOT, parent_pid=os.getppid()
        )
        self.assertTrue(result["parent_shell_sampled"])

    def test_close_kills_gated_process(self):
        job = aid.Job()
        process = subprocess.Popen(
            [sys.executable, "-I", "-S", "-B", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        try:
            job.assign(process)
            self.assertIsNone(process.poll())
            self.assertFalse(process.stdin.closed)
            job.close()
            process.wait(timeout=5)
            # Kill-on-close can report exit code zero; exit with stdin still open is
            # the observable property proving the waiting interpreter was stopped.
            self.assertIsNotNone(process.returncode)
            self.assertFalse(process.stdin.closed)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=5)
            with contextlib.suppress(OSError):
                process.stdin.close()
            job.close()

    def test_descendant_refused(self):
        marker = ROOT / "synthetic-descendant-ran"
        self.assertFalse(marker.exists())
        payload = f"from pathlib import Path;Path({str(marker)!r}).write_text('unsafe')"
        code = (
            "import subprocess,sys\ntry:\n"
            f" p=subprocess.Popen([sys.executable,'-c',{payload!r}])\n"
            " p.wait(timeout=3)\nexcept OSError:\n pass\n"
            "print('descendant check completed')\n"
        ).encode()
        result = aid.supervise_code(code, 5, ROOT, parent_pid=None)
        self.assertTrue(result["teardown_verified"])
        self.assertFalse(marker.exists(), "descendant body executed despite Job limit")


if __name__ == "__main__":
    unittest.main(verbosity=1)
