"""Meaningful malformed-input controls for the data-only GGUF inspector."""

import hashlib
import importlib.util
import io
import struct
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "t17_metadata", Path(__file__).with_name("t17_model_metadata.py")
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def string(value):
    raw = value.encode("utf-8")
    return struct.pack("<Q", len(raw)) + raw


def document(entries):
    return b"GGUF" + struct.pack("<IQQ", 3, 0, len(entries)) + b"".join(entries)


class MetadataTests(unittest.TestCase):
    def test_verified_file_hash(self):
        raw = document([])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.gguf"
            path.write_bytes(raw)
            result = module.verified_metadata(
                path, len(raw), hashlib.sha256(raw).hexdigest()
            )
            self.assertTrue(result["payload_hash_verified"])

    def test_hash_drift_refuses(self):
        raw = document([])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.gguf"
            path.write_bytes(raw)
            with self.assertRaises(ValueError):
                module.verified_metadata(path, len(raw), "0" * 64)

    def test_valid_metadata_stops_before_tensor_bytes(self):
        raw = document(
            [string("general.architecture") + struct.pack("<I", 8) + string("qwen2")]
        )
        stream = io.BytesIO(raw + b"unread tensor payload")
        result = module.read_metadata(stream)
        self.assertEqual(result["metadata"]["general.architecture"], "qwen2")
        self.assertEqual(stream.tell(), len(raw))

    def test_invalid_magic(self):
        with self.assertRaises(ValueError):
            module.read_metadata(io.BytesIO(b"NOPE" + b"\0" * 24))

    def test_unsupported_version(self):
        with self.assertRaises(ValueError):
            module.read_metadata(io.BytesIO(b"GGUF" + struct.pack("<IQQ", 999, 0, 0)))

    def test_truncated_input(self):
        with self.assertRaises(ValueError):
            module.read_metadata(io.BytesIO(b"GGUF\3"))

    def test_string_allocation_bomb(self):
        raw = document([struct.pack("<Q", 2**40)])
        with self.assertRaises(ValueError):
            module.read_metadata(io.BytesIO(raw))

    def test_array_allocation_bomb(self):
        entry = string("tokens") + struct.pack("<IIQ", 9, 8, 500001)
        with self.assertRaises(ValueError):
            module.read_metadata(io.BytesIO(document([entry])))

    def test_duplicate_keys(self):
        entry = string("duplicate") + struct.pack("<II", 4, 1)
        with self.assertRaises(ValueError):
            module.read_metadata(io.BytesIO(document([entry, entry])))

    def test_total_read_budget(self):
        with self.assertRaises(ValueError):
            module.read_metadata(io.BytesIO(document([])), byte_limit=8)


if __name__ == "__main__":
    unittest.main()
