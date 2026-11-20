"""Bounded, data-only GGUF inspection for the T17 closeout evaluation."""

import hashlib
import math
import os
import re
import stat
import struct
from pathlib import Path
from typing import Any, BinaryIO


class _Reader:
    def __init__(self, stream, limit):
        if type(limit) is not int or limit < 1:
            raise ValueError("invalid byte budget")
        self.stream, self.limit, self.used = stream, limit, 0

    def read(self, count):
        if count < 0 or self.used + count > self.limit:
            raise ValueError("metadata byte budget")
        self.used += count
        raw = self.stream.read(count)
        if len(raw) != count:
            raise ValueError("truncated GGUF metadata")
        return raw

    def number(self, fmt):
        return struct.unpack("<" + fmt, self.read(struct.calcsize("<" + fmt)))[0]

    def string(self, maximum=1024**2):
        count = self.number("Q")
        if count > maximum:
            raise ValueError("GGUF string limit")
        return self.read(count).decode("utf-8")

    def value(self, kind, depth=0):
        formats = {
            0: "B",
            1: "b",
            2: "H",
            3: "h",
            4: "I",
            5: "i",
            6: "f",
            10: "Q",
            11: "q",
            12: "d",
        }
        if kind in formats:
            result = self.number(formats[kind])
            if isinstance(result, float) and not math.isfinite(result):
                raise ValueError("nonfinite metadata")
            return result
        if kind == 7:
            value = self.number("B")
            if value not in (0, 1):
                raise ValueError("invalid boolean")
            return bool(value)
        if kind == 8:
            return self.string()
        if kind == 9:
            if depth > 1:
                raise ValueError("nested array limit")
            element_kind, count = self.number("I"), self.number("Q")
            if count > 500000:
                raise ValueError("GGUF array limit")
            return [self.value(element_kind, depth + 1) for _ in range(count)]
        raise ValueError("unsupported metadata type")


def read_metadata(
    stream: BinaryIO, *, byte_limit: int = 16 * 1024**2
) -> dict[str, Any]:
    """Decode bounded GGUF metadata without loading a model or tensor payload."""
    reader = _Reader(stream, byte_limit)
    if reader.read(4) != b"GGUF" or reader.number("I") not in (2, 3):
        raise ValueError("unsupported GGUF header")
    tensors, count = reader.number("Q"), reader.number("Q")
    if tensors > 100000 or count > 4096:
        raise ValueError("GGUF header count limit")
    metadata = {}
    for _ in range(count):
        key = reader.string(256)
        if key in metadata:
            raise ValueError("duplicate GGUF key")
        metadata[key] = reader.value(reader.number("I"))
    return {
        "metadata": metadata,
        "metadata_bytes": reader.used,
        "tensor_count": tensors,
    }


def verified_metadata(
    path: Path, expected_size: int, expected_sha256: str
) -> dict[str, Any]:
    """Hash an exact cached file, then parse metadata with stable file identity.

    This is a data inspection, never a model/native loader. The whole-file hash
    reads tensor bytes as opaque chunks; the decoder stops before tensor data.
    """
    if type(expected_size) is not int or not 24 <= expected_size <= 2**31:
        raise ValueError("invalid expected size")
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise ValueError("invalid expected hash")
    for entry in (path, *path.parents):
        info = entry.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 1024:
            raise ValueError("reparse input")
    before = path.stat()
    if (
        not stat.S_ISREG(before.st_mode)
        or before.st_size != expected_size
        or before.st_nlink != 1
    ):
        raise ValueError("input type/size/link mismatch")

    def identity(info):
        # Use the same mtime identity fields; Windows ctime APIs differed in IF-R.
        return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_nlink

    with path.open("rb") as stream:
        opened = os.fstat(stream.fileno())
        digest = hashlib.sha256()
        remaining = expected_size
        while remaining:
            chunk = stream.read(min(1024**2, remaining))
            if not chunk:
                raise ValueError("truncated model file")
            digest.update(chunk)
            remaining -= len(chunk)
        if stream.read(1) or digest.hexdigest() != expected_sha256:
            raise ValueError("model hash mismatch")
        stream.seek(0)
        result = read_metadata(stream)
        after = os.fstat(stream.fileno())
    if any(identity(before) != identity(info) for info in (opened, after, path.stat())):
        raise ValueError("model changed during inspection")
    return {
        **result,
        "file_bytes": expected_size,
        "sha256": expected_sha256,
        "payload_hash_verified": True,
    }
