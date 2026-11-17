"""Inert wheel evaluation aid. Candidate bytes are never imported or installed.

ZIP primitives below are attributed copies from the reviewed project-owned
standalone_static_verification.py (SHA-256 691d86c9...fcd6d03).
"""

from __future__ import annotations

import base64
import contextlib
import csv
import ctypes
import hashlib
import io
import ipaddress
import json
import os
import re
import socket
import ssl
import stat
import struct
import subprocess
import sys
import threading
import time
import zipfile
import zlib
from collections.abc import Callable, Iterator
from ctypes import wintypes as w
from dataclasses import dataclass
from email.parser import BytesParser
from itertools import pairwise
from pathlib import Path
from typing import BinaryIO
from urllib.parse import urlsplit

CHUNK = 1_048_576
ROOT = Path("F:/document_assistant/data/t17/wheel-artifact-review-02")
BASE = Path("F:/document_assistant")
FIXED_SPECS = [
    {
        "distribution": d,
        "version": v,
        "filename": n,
        "size": size,
        "sha256": sha,
        "cap": cap,
    }
    for d, v, n, size, sha, cap in (
        (
            "httpx2",
            "2.16.2",
            "httpx2-2.16.2-py3-none-any.whl",
            97893,
            "f05c13aade4c45dbf1c9060647a1058f0acad62398fad96e741269edb33d46f5",
            262144,
        ),
        (
            "httpcore2",
            "2.16.2",
            "httpcore2-2.16.2-py3-none-any.whl",
            85551,
            "16051ae2a42f776007543f32de9349a317b23d2cbb4e1456b4bac0e88b87419a",
            262144,
        ),
        (
            "anyio",
            "4.16.0",
            "anyio-4.16.0-py3-none-any.whl",
            134521,
            "c66ae634e0b8228396b801741beb3294326d4b6102f7bba4041c0dfb58c29026",
            262144,
        ),
        (
            "click",
            "8.5.1",
            "click-8.5.1-py3-none-any.whl",
            126163,
            "8bb5376d2006950386f8c6427613334a2acadc5f559cb80e638d00b4df957e37",
            262144,
        ),
        (
            "filelock",
            "4.2.10",
            "filelock-4.2.10-py3-none-any.whl",
            218040,
            "9479aaeb4db20b5a53e3da28493edd24720b66b8a0b84030aa56ccdf243d6857",
            262144,
        ),
        (
            "truststore",
            "0.10.5",
            "truststore-0.10.5-py3-none-any.whl",
            19017,
            "9aaaedaefaf06d8b206278cf8b5012bc897f485a874503501e12d776df78951c",
            262144,
        ),
        (
            "hf-xet",
            "1.8.0",
            "hf_xet-1.8.0-cp38-abi3-win_amd64.whl",
            None,
            "92188598dedc1e1f5609bd718d4db8687a6c89915553912571e2f587892eecec",
            8 * 2**20,
        ),
        (
            "fsspec",
            "2026.9.0",
            "fsspec-2026.9.0-py3-none-any.whl",
            None,
            "8dd6e646e99ea382bd85f97a45e6b526a442d79423a7dc673f1e2756d05fcb5f",
            2**20,
        ),
    )
]
FIXED_CACHED = [
    {
        "distribution": "huggingface-hub",
        "version": "2.4.0",
        "filename": "huggingface_hub-2.4.0-py3-none-any.whl",
        "size": 857021,
        "sha256": "42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801",
    },
    {
        "distribution": "tokenizers",
        "version": "0.23.3",
        "filename": "tokenizers-0.23.3-cp310-abi3-win_amd64.whl",
        "size": 2872101,
        "sha256": "1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3",
    },
]


class Failure(Exception):
    """Content-free admission failure, optionally carrying bounded counts."""

    def __init__(self, code: str, **counts: int):
        if not re.fullmatch(r"[a-z_]+", code):
            raise ValueError("Invalid failure code")
        self.code = code
        self.counts = counts
        super().__init__(code)


@dataclass(frozen=True)
class Limits:
    """Approved archive and notice bounds; tests can lower them."""

    max_entries: int = 128
    max_depth: int = 8
    max_expanded: int = 3 * 2**30
    max_central: int = 256 * 1024
    max_notice: int = 256 * 1024
    max_notices_total: int = 1024 * 1024


class ReadBudget:
    """Precharge requested bytes, including failed/overflow-probe reads."""

    def __init__(self, limit: int, hook: Callable[[int], None] | None = None):
        self.limit = limit
        self.used = 0
        self.hook = hook

    def reserve(self, amount: int) -> None:
        """Refuse before I/O; never refund short or unsuccessful reads."""
        if amount < 0 or self.used + amount > self.limit:
            raise Failure("read_limit")
        if self.hook:
            self.hook(amount)
        self.used += amount


def checked_name(name: str, depth: int) -> str:
    """Admit unambiguous Windows-relative ZIP names without rewriting."""
    if not name or name.endswith("/"):
        raise Failure("unsafe_name")
    parts = name.split("/")
    if len(parts) > depth:
        raise Failure("depth_limit")
    for part in parts:
        if (
            not part
            or part in {".", ".."}
            or part[-1] in {" ", "."}
            or any(ord(c) < 32 or ord(c) > 126 or c in '\\:<>"|?*' for c in part)
            or re.fullmatch(
                r"(?i)(con|prn|aux|nul|com[1-9]|lpt[1-9])", part.split(".")[0]
            )
        ):
            raise Failure("unsafe_name")
    return name


def is_reparse(value: os.stat_result) -> bool:
    """Recognize Windows reparse points and ordinary symlinks."""
    return bool(getattr(value, "st_file_attributes", 0) & 0x400) or stat.S_ISLNK(
        value.st_mode
    )


def fingerprint(value: os.stat_result) -> tuple:
    """Use timestamps only within repeated calls to the same stat API."""
    return (
        value.st_dev,
        value.st_ino,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
        value.st_nlink,
        value.st_mode,
    )


def check_ancestors(path: Path) -> None:
    """Refuse redirected directory components, including above a fixed root."""
    for parent in reversed(path.parents):
        value = parent.lstat()
        if is_reparse(value) or not stat.S_ISDIR(value.st_mode):
            raise Failure("ancestor_type")


@contextlib.contextmanager
def open_regular(path: Path, root: Path) -> Iterator[BinaryIO]:
    """Check lexical confinement and path/handle identities before and after."""
    path, root = path.absolute(), root.absolute()
    if os.path.commonpath((str(path), str(root))) != str(root) or path == root:
        raise Failure("outside_root")
    check_ancestors(path)
    before = path.lstat()
    if is_reparse(before) or not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise Failure("file_type")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    with os.fdopen(os.open(path, flags), "rb") as handle:
        opened = os.fstat(handle.fileno())
        if (before.st_dev, before.st_ino, before.st_size, before.st_nlink) != (
            opened.st_dev,
            opened.st_ino,
            opened.st_size,
            opened.st_nlink,
        ):
            raise Failure("file_identity")
        yield handle
        after_handle = os.fstat(handle.fileno())
        after_path = path.lstat()
        if fingerprint(opened) != fingerprint(after_handle) or fingerprint(
            before
        ) != fingerprint(after_path):
            raise Failure("file_changed")
        check_ancestors(path)


def digest_stream(handle: BinaryIO, size: int, budget: ReadBudget) -> str:
    """Hash exact declared bytes and a charged overflow probe."""
    digest, remaining = hashlib.sha256(), size
    while remaining:
        amount = min(CHUNK, remaining)
        budget.reserve(amount)
        data = handle.read(amount)
        if not data:
            raise Failure("short_read")
        remaining -= len(data)
        digest.update(data)
    budget.reserve(1)
    if handle.read(1):
        raise Failure("overflow_read")
    return digest.hexdigest()


def hash_regular(path: Path, root: Path, budget: ReadBudget) -> str:
    """Hash a stable, single-link ordinary file without whole-file buffering."""
    with open_regular(path, root) as handle:
        return digest_stream(handle, os.fstat(handle.fileno()).st_size, budget)


class ChargedFile:
    """Count physical compressed-file reads as well as decompressed bytes."""

    def __init__(self, handle: BinaryIO, budget: ReadBudget):
        self.handle = handle
        self.budget = budget
        self.size = os.fstat(handle.fileno()).st_size

    def seek(self, offset: int, whence: int = 0) -> int:
        return self.handle.seek(offset, whence)

    def tell(self) -> int:
        return self.handle.tell()

    def seekable(self) -> bool:
        return True

    def read(self, amount: int = -1) -> bytes:
        if amount < 0:
            amount = max(0, self.size - self.tell())
        if amount > 8 * CHUNK:
            raise Failure("single_read_limit")
        self.budget.reserve(amount)
        return self.handle.read(amount)


def central_admission(handle: ChargedFile, limits: Limits) -> None:
    """Bound central metadata before ZipFile can allocate its entry list."""
    handle.seek(max(0, handle.size - 65_557))
    tail = handle.read()
    offset = tail.rfind(b"PK\x05\x06")
    if offset < 0 or len(tail) - offset < 22:
        raise Failure("invalid_zip")
    if offset >= 20 and tail[offset - 20 : offset - 16] == b"PK\x06\x07":
        raise Failure("unsupported_zip_layout")
    _, disk, start_disk, local_count, count, size, start, comment = struct.unpack_from(
        "<4s4H2LH", tail, offset
    )
    if (
        disk
        or start_disk
        or local_count != count
        or count == 65535
        or size == 0xFFFFFFFF
    ):
        raise Failure("unsupported_zip_layout")
    if len(tail) - offset != 22 + comment or start + size != handle.size - 22 - comment:
        raise Failure("invalid_zip")
    if count > limits.max_entries:
        raise Failure("entry_limit", observed=count, allowed=limits.max_entries)
    if size > limits.max_central:
        raise Failure("central_limit", observed=size, allowed=limits.max_central)


def admitted_entries(archive: zipfile.ZipFile, limits: Limits) -> list[zipfile.ZipInfo]:
    """Validate types, names, aliases, counts and expansion before payload reads."""
    entries = archive.infolist()
    if len(entries) > limits.max_entries:
        raise Failure("entry_limit", observed=len(entries), allowed=limits.max_entries)
    seen, files, total = set(), set(), 0
    for entry in entries:
        if entry.orig_filename != entry.filename or (
            entry.is_dir() and entry.file_size
        ):
            raise Failure("unsafe_name")
        name = checked_name(
            entry.filename[:-1] if entry.is_dir() else entry.filename, limits.max_depth
        )
        folded = name.casefold()
        kind = stat.S_IFMT(entry.external_attr >> 16)
        if (
            entry.flag_bits & 1
            or kind not in (0, stat.S_IFREG, stat.S_IFDIR)
            or entry.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED)
            or (kind == stat.S_IFDIR and not entry.is_dir())
        ):
            raise Failure("member_type")
        if folded in seen:
            raise Failure("member_alias")
        seen.add(folded)
        if not entry.is_dir():
            files.add(folded)
            total += entry.file_size
        if total > limits.max_expanded:
            raise Failure("expanded_limit", observed=total, allowed=limits.max_expanded)
    for name in seen:
        parts = name.split("/")
        if any("/".join(parts[:i]) in files for i in range(1, len(parts))):
            raise Failure("member_alias")
    return entries


class Budget(ReadBudget):
    """A prepaid local lease for reads, HTTP and repeated decompression."""

    def __init__(
        self,
        read_limit: int = 16 * 2**20,
        net_limit: int = 24 * 2**20,
        expand_limit: int = 128 * 2**20,
    ) -> None:
        super().__init__(read_limit)
        self.net_limit, self.expand_limit = net_limit, expand_limit
        self.net = self.expanded = self.notices = self.entries = self.transactions = 0

    def network(self, size: int) -> None:
        self.reserve(size)
        self.net += size
        if self.net > self.net_limit:
            raise Failure("http_limit")

    def expansion(self, size: int) -> None:
        self.reserve(size)
        self.expanded += size
        if self.expanded > self.expand_limit:
            raise Failure("expansion_limit")


def parse_json(raw: bytes) -> dict | list:
    """Reject duplicate keys and oversized registry/request JSON."""
    if len(raw) > 2**20:
        raise Failure("json_limit")

    def pairs(items):
        value = {}
        for key, item in items:
            if key in value:
                raise Failure("duplicate_json")
            value[key] = item
        return value

    try:
        return json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs)
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise Failure("invalid_json") from exc


def canonical(name: str) -> str:
    """Normalize a distribution identifier without importing packaging tools."""
    return re.sub(r"[-_.]+", "-", name).lower()


def check_url(url: str):
    """Fixed HTTPS origins only; no credentials, redirects or ambient proxy."""
    try:
        parsed = urlsplit(url)
        if (
            parsed.scheme != "https"
            or parsed.hostname not in {"pypi.org", "files.pythonhosted.org"}
            or parsed.port not in (None, 443)
            or parsed.username is not None
            or parsed.password is not None
            or parsed.query
            or parsed.fragment
            or not parsed.path.startswith("/")
            or any(ord(c) < 33 or ord(c) > 126 for c in url)
        ):
            raise Failure("url_refused")
        return parsed
    except (ValueError, TypeError) as exc:
        raise Failure("url_refused") from exc


def address(host: str) -> tuple:
    """Admit every DNS answer; connect once to one public address."""
    answers = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    if not answers or any(not ipaddress.ip_address(a[4][0]).is_global for a in answers):
        raise Failure("dns_refused")
    return next((a for a in answers if a[0] == socket.AF_INET), answers[0])


def admit_entry(metadata: dict, expected: dict) -> dict:
    """Admit exactly the fixed registry wheel; rounded sizes never substitute."""
    if not isinstance(metadata, dict) or not isinstance(metadata.get("info"), dict):
        raise Failure("registry_schema")
    info = metadata["info"]
    if (
        not isinstance(info.get("name"), str)
        or canonical(info["name"]) != canonical(expected["distribution"])
        or info.get("version") != expected["version"]
    ):
        raise Failure("release_mismatch")
    urls = metadata.get("urls")
    if (
        not isinstance(urls, list)
        or len(urls) > 128
        or any(not isinstance(x, dict) for x in urls)
    ):
        raise Failure("registry_schema")
    found = [x for x in urls if x.get("filename") == expected["filename"]]
    if len(found) != 1:
        raise Failure("artifact_ambiguity")
    item = found[0]
    size, hashes = item.get("size"), item.get("digests")
    if (
        type(size) is not int
        or not 0 < size <= expected["cap"]
        or item.get("yanked") is not False
        or not isinstance(hashes, dict)
        or hashes.get("sha256") != expected["sha256"]
        or expected.get("size") is not None
        and size != expected["size"]
    ):
        raise Failure("artifact_identity")
    parsed = check_url(item.get("url", ""))
    if (
        parsed.hostname != "files.pythonhosted.org"
        or parsed.path.rsplit("/", 1)[-1] != expected["filename"]
    ):
        raise Failure("artifact_url")
    return {**expected, "size": size, "url": item["url"]}


def receive(connection, cap: int, budget: Budget, sink: BinaryIO) -> int:
    """Consume one bounded identity-encoded, exact-length HTTP response."""
    header = bytearray()
    while not header.endswith(b"\r\n\r\n"):
        if len(header) >= 65536:
            raise Failure("header_limit")
        data = connection.recv(1)
        if not data:
            raise Failure("short_header")
        budget.network(len(data))
        header.extend(data)
    lines = header.decode("iso-8859-1").split("\r\n")
    if lines[0].split(" ", 2)[:2] != ["HTTP/1.1", "200"]:
        raise Failure("http_status")
    headers = {}
    for line in lines[1:-2]:
        if not line or line[0].isspace() or ":" not in line:
            raise Failure("invalid_header")
        name, value = line.split(":", 1)
        name = name.lower()
        if name in headers:
            raise Failure("duplicate_header")
        headers[name] = value.strip()
    length = headers.get("content-length", "")
    if (
        "transfer-encoding" in headers
        or headers.get("content-encoding", "identity") != "identity"
        or not length.isascii()
        or not length.isdecimal()
        or not 0 < int(length) <= cap
    ):
        raise Failure("http_framing")
    remaining = int(length)
    while remaining:
        data = connection.recv(min(65536, remaining))
        if not data:
            raise Failure("short_body")
        if len(data) > remaining:
            raise Failure("body_overflow")
        budget.network(len(data))
        sink.write(data)
        remaining -= len(data)
    return int(length)


def fetch(url: str, cap: int, budget: Budget, sink: BinaryIO) -> int:
    """One pinned-address TLS connection; no fallback, retry or proxy lookup."""
    budget.transactions += 1
    if budget.transactions > 16:
        raise Failure("transaction_limit")
    parsed = check_url(url)
    answer = address(parsed.hostname)
    with socket.socket(answer[0], answer[1], answer[2]) as raw:
        raw.settimeout(30)
        raw.connect(answer[4])
        with ssl.create_default_context().wrap_socket(
            raw, server_hostname=parsed.hostname
        ) as secure:
            secure.sendall(
                (
                    f"GET {parsed.path} HTTP/1.1\r\nHost: {parsed.hostname}\r\nAccept-Encoding: identity\r\nConnection: close\r\n\r\n"
                ).encode("ascii")
            )
            return receive(secure, cap, budget, sink)


def member_bytes(
    archive: zipfile.ZipFile,
    entry: zipfile.ZipInfo,
    budget: Budget,
    cap: int | None = None,
) -> tuple[bytes, bytes]:
    """Hash all payloads, retaining only explicitly capped text members."""
    if cap is not None and entry.file_size > cap:
        raise Failure("member_text_limit")
    digest, retained, size = hashlib.sha256(), bytearray(), 0
    try:
        with archive.open(entry) as stream:
            while True:
                data = stream.read(min(65536, entry.file_size - size + 1))
                if not data:
                    break
                size += len(data)
                budget.expansion(len(data))
                if size > entry.file_size:
                    raise Failure("member_size")
                digest.update(data)
                if cap is not None:
                    retained.extend(data)
    except (zipfile.BadZipFile, zlib.error, EOFError) as exc:
        raise Failure("member_crc_or_stream") from exc
    if size != entry.file_size:
        raise Failure("member_size")
    return digest.digest(), bytes(retained)


def local_layout(
    handle: ChargedFile, archive: zipfile.ZipFile, entries: list[zipfile.ZipInfo]
) -> None:
    """Check local/central agreement and disjoint payload/descriptor ranges."""
    regions = []
    for entry in entries:
        start = entry.header_offset
        if start < 0 or start + 30 > archive.start_dir:
            raise Failure("local_layout")
        handle.seek(start)
        raw = handle.read(30)
        if len(raw) != 30:
            raise Failure("local_layout")
        signature, _, flags, method, _, _, crc, compressed, expanded, names, extra = (
            struct.unpack("<4s5H3I2H", raw)
        )
        if (
            signature != b"PK\x03\x04"
            or flags != entry.flag_bits
            or method != entry.compress_type
        ):
            raise Failure("local_layout")
        name = handle.read(names)
        if (
            name.decode("utf-8" if flags & 2048 else "cp437", "strict")
            != entry.orig_filename
        ):
            raise Failure("local_name")
        if flags & 8:
            if (
                crc not in (0, entry.CRC)
                or compressed not in (0, entry.compress_size)
                or expanded not in (0, entry.file_size)
            ):
                raise Failure("local_sizes")
        elif (crc, compressed, expanded) != (
            entry.CRC,
            entry.compress_size,
            entry.file_size,
        ):
            raise Failure("local_sizes")
        end = start + 30 + names + extra + entry.compress_size
        if flags & 8:
            handle.seek(end)
            descriptor = handle.read(16)
            offset = 4 if descriptor[:4] == b"PK\x07\x08" else 0
            if len(descriptor) < offset + 12 or struct.unpack_from(
                "<3I", descriptor, offset
            ) != (entry.CRC, entry.compress_size, entry.file_size):
                raise Failure("descriptor_layout")
            end += offset + 12
        if end > archive.start_dir:
            raise Failure("local_overlap")
        regions.append((start, end))
        position = 0
        while position < len(entry.extra):
            if position + 4 > len(entry.extra):
                raise Failure("extra_layout")
            kind, size = struct.unpack_from("<HH", entry.extra, position)
            if kind == 1 or position + 4 + size > len(entry.extra):
                raise Failure("zip_extra_refused")
            position += 4 + size
    regions.sort()
    if regions and regions[0][0] != 0:
        raise Failure("archive_prefix")
    if any(a[1] > b[0] for a, b in pairwise(regions)):
        raise Failure("local_overlap")


def inspect_wheel(
    path: Path, expected: dict, budget: Budget, cached: bool = False
) -> dict:
    """Inspect inert ZIP members; preserve provenance and incomplete evidence."""
    if (
        path.stat().st_size != expected["size"]
        or hash_regular(path, path.parent, budget) != expected["sha256"]
    ):
        raise Failure("wheel_identity")
    limit = (
        256
        if cached and expected["distribution"] == "huggingface-hub"
        else 128
        if cached
        else 512
    )
    limits = Limits(
        max_entries=limit,
        max_expanded=64 * 2**20,
        max_central=262144,
        max_notice=262144,
        max_notices_total=4 * 2**20,
    )
    with open_regular(path, path.parent) as file:
        charged = ChargedFile(file, budget)
        central_admission(charged, limits)
        try:
            with zipfile.ZipFile(charged) as archive:
                entries = admitted_entries(archive, limits)
                budget.entries += len(entries)
                if budget.entries > 4096:
                    raise Failure("aggregate_entries")
                local_layout(charged, archive, entries)
                files = {e.filename: e for e in entries if not e.is_dir()}
                metadata = [
                    n
                    for n in files
                    if n.count("/") == 1 and n.endswith(".dist-info/METADATA")
                ]
                if len(metadata) != 1:
                    raise Failure("dist_info_ambiguity")
                prefix = metadata[0].rsplit("/", 1)[0]
                record, wheel_name = prefix + "/RECORD", prefix + "/WHEEL"
                if record not in files or wheel_name not in files:
                    raise Failure("required_metadata")
                _, raw_record = member_bytes(archive, files[record], budget, 262144)
                rows = {}
                for row in csv.reader(
                    io.StringIO(raw_record.decode("utf-8", "strict"), newline=""),
                    strict=True,
                ):
                    if len(row) != 3 or row[0] in rows:
                        raise Failure("record_schema")
                    checked_name(row[0], 8)
                    rows[row[0]] = row[1:]
                if rows.get(record) != ["", ""] or any(
                    name not in files for name in rows
                ):
                    raise Failure("record_coverage")
                sidecars = {prefix + "/RECORD.jws", prefix + "/RECORD.p7s"}
                if not cached and any(
                    n not in rows and n not in sidecars for n in files
                ):
                    raise Failure("record_coverage")
                texts, notices, native, hooks, verified, sources = {}, [], [], [], 0, []
                source_names = {
                    "huggingface_hub/constants.py",
                    "tokenizers/__init__.py",
                    "tokenizers/__init__.pyi",
                    "tokenizers/tokenizers.pyi",
                }
                source_total = 0
                for name, entry in files.items():
                    basename = name.rsplit("/", 1)[-1].upper()
                    notice = basename.startswith(
                        ("LICENSE", "COPYING", "NOTICE", "AUTHORS")
                    )
                    source = cached and name in source_names
                    cap = (
                        262144
                        if name in (record, metadata[0]) or notice
                        else 131072
                        if source
                        else 65536
                        if name.startswith(prefix + "/")
                        and basename.endswith((".TXT", "WHEEL"))
                        else None
                    )
                    if name.lower().endswith(
                        (".pyd", ".dll", ".so", ".dylib", ".exe", ".lib", ".a")
                    ):
                        native.append(name)
                    if (
                        name.endswith(".pth")
                        or ".data/scripts/" in name
                        or basename == "ENTRY_POINTS.TXT"
                    ):
                        hooks.append(name)
                    if cached and cap is None:
                        continue
                    digest, text = member_bytes(archive, entry, budget, cap)
                    if not cached and name != record and name not in sidecars:
                        value = rows.get(name)
                        encoded = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
                        if value != ["sha256=" + encoded, str(entry.file_size)]:
                            raise Failure("record_integrity")
                        verified += 1
                    if cap is not None:
                        decoded = text.decode("utf-8", "strict")
                        texts[name] = decoded
                    if notice:
                        budget.notices += len(text)
                        if budget.notices > 4 * 2**20:
                            raise Failure("notice_total")
                        notices.append(
                            {
                                "path": name,
                                "bytes": len(text),
                                "sha256": hashlib.sha256(text).hexdigest(),
                                "text": decoded,
                            }
                        )
                    if source:
                        source_total += len(text)
                        if source_total > 524288:
                            raise Failure("cached_source_limit")
                        sources.append(
                            {
                                "path": name,
                                "bytes": len(text),
                                "sha256": hashlib.sha256(text).hexdigest(),
                                "text": decoded,
                            }
                        )
                parsed = BytesParser().parsebytes(texts[metadata[0]].encode("utf-8"))
                if (
                    len(parsed.get_all("Name", [])) != 1
                    or len(parsed.get_all("Version", [])) != 1
                    or canonical(parsed["Name"]) != canonical(expected["distribution"])
                    or parsed["Version"] != expected["version"]
                ):
                    raise Failure("metadata_identity")
                version = parsed.get("Metadata-Version", "")
                if not re.fullmatch(r"\d+\.\d+", version):
                    raise Failure("metadata_version")
                if tuple(map(int, version.split("."))) >= (2, 4):
                    for name in parsed.get_all("License-File", []):
                        checked_name(name, 8)
                        if prefix + "/licenses/" + name not in files:
                            raise Failure("missing_license_file")
                wheel_meta = BytesParser().parsebytes(texts[wheel_name].encode("utf-8"))
                tag_fields = expected["filename"][:-4].rsplit("-", 3)[-3:]
                allowed = {
                    a + "-" + b + "-" + c
                    for a in tag_fields[0].split(".")
                    for b in tag_fields[1].split(".")
                    for c in tag_fields[2].split(".")
                }
                if set(wheel_meta.get_all("Tag", [])) != allowed:
                    raise Failure("wheel_tags")
                return {
                    "filename": expected["filename"],
                    "sha256": expected["sha256"],
                    "size": expected["size"],
                    "entries": len(entries),
                    "record_verified": verified,
                    "cached_record_evidence_reused": cached,
                    "license_expression": parsed.get("License-Expression"),
                    "license_declaration": parsed.get("License"),
                    "requirements": parsed.get_all("Requires-Dist", []),
                    "native": native,
                    "hooks": hooks,
                    "unverified_signature_sidecars": sorted(sidecars & files.keys()),
                    "notices": notices,
                    "sources_as_data": sources,
                }
        except (zipfile.BadZipFile, UnicodeError, csv.Error, ValueError) as exc:
            raise Failure("invalid_wheel") from exc


class Job:
    """Windows kill-on-close Job; worker input is withheld until assignment."""

    def __init__(self) -> None:
        self.k = ctypes.WinDLL("kernel32", use_last_error=True)
        signatures = {
            "CreateJobObjectW": ([ctypes.c_void_p, w.LPCWSTR], w.HANDLE),
            "SetInformationJobObject": (
                [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD],
                w.BOOL,
            ),
            "QueryInformationJobObject": (
                [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD, ctypes.c_void_p],
                w.BOOL,
            ),
            "AssignProcessToJobObject": ([w.HANDLE, w.HANDLE], w.BOOL),
            "IsProcessInJob": ([w.HANDLE, w.HANDLE, ctypes.POINTER(w.BOOL)], w.BOOL),
            "TerminateJobObject": ([w.HANDLE, w.UINT], w.BOOL),
            "CloseHandle": ([w.HANDLE], w.BOOL),
            "GetCurrentProcess": ([], w.HANDLE),
            "OpenProcess": ([w.DWORD, w.BOOL, w.DWORD], w.HANDLE),
            "K32GetProcessMemoryInfo": ([w.HANDLE, ctypes.c_void_p, w.DWORD], w.BOOL),
            "GetProcessTimes": (
                [
                    w.HANDLE,
                    ctypes.c_void_p,
                    ctypes.c_void_p,
                    ctypes.c_void_p,
                    ctypes.c_void_p,
                ],
                w.BOOL,
            ),
        }
        for name, (args, result) in signatures.items():
            function = getattr(self.k, name)
            function.argtypes, function.restype = args, result

        class Basic(ctypes.Structure):
            _fields_ = [
                ("process_time", ctypes.c_int64),
                ("job_time", ctypes.c_int64),
                ("flags", w.DWORD),
                ("min_ws", ctypes.c_size_t),
                ("max_ws", ctypes.c_size_t),
                ("active", w.DWORD),
                ("affinity", ctypes.c_size_t),
                ("priority", w.DWORD),
                ("scheduling", w.DWORD),
            ]

        class Extended(ctypes.Structure):
            _fields_ = [
                ("basic", Basic),
                ("io", ctypes.c_uint64 * 6),
                ("process_memory", ctypes.c_size_t),
                ("job_memory", ctypes.c_size_t),
                ("peak_process", ctypes.c_size_t),
                ("peak_job", ctypes.c_size_t),
            ]

        self.handle = self.k.CreateJobObjectW(None, None)
        if not self.handle:
            raise Failure("job_create")
        limits = Extended()
        limits.basic.flags, limits.basic.active = 0x2000 | 0x8, 1
        if not self.k.SetInformationJobObject(
            self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)
        ):
            self.close()
            raise Failure("job_limits")
        observed = Extended()
        if (
            not self.k.QueryInformationJobObject(
                self.handle, 9, ctypes.byref(observed), ctypes.sizeof(observed), None
            )
            or observed.basic.flags & 0x2008 != 0x2008
            or observed.basic.active != 1
        ):
            self.close()
            raise Failure("job_limits_unverified")

    def assign(self, process: subprocess.Popen) -> None:
        """Bind the retained process handle and verify Job membership."""
        if not self.k.AssignProcessToJobObject(
            self.handle, w.HANDLE(int(process._handle))
        ):
            raise Failure("job_assignment")
        inside = w.BOOL()
        if (
            not self.k.IsProcessInJob(
                w.HANDLE(int(process._handle)), self.handle, ctypes.byref(inside)
            )
            or not inside
        ):
            raise Failure("job_assignment_unverified")

    def memory(self, handle: int) -> int:
        """Sample private committed bytes using a retained process handle."""

        class Memory(ctypes.Structure):
            _fields_ = [("cb", w.DWORD), ("faults", w.DWORD)] + [
                (name, ctypes.c_size_t)
                for name in (
                    "peak_ws",
                    "ws",
                    "peak_paged",
                    "paged",
                    "peak_nonpaged",
                    "nonpaged",
                    "pagefile",
                    "peak_pagefile",
                    "private",
                )
            ]

        value = Memory()
        value.cb = ctypes.sizeof(value)
        if not self.k.K32GetProcessMemoryInfo(handle, ctypes.byref(value), value.cb):
            raise Failure("memory_sample")
        return value.private

    def close(self) -> None:
        """Close the non-inherited Job handle, terminating owned processes."""
        if self.handle:
            self.k.CloseHandle(self.handle)
            self.handle = None


def supervise_code(
    code: bytes,
    seconds: float,
    root: Path,
    parent_pid: int | None = None,
    arguments: tuple[str, ...] = (),
) -> dict:
    """Assign a waiting Python interpreter, sample ownership, then release stdin."""
    job, process, extra = Job(), None, None
    result, readers = {}, []
    streams, lock, abort = (
        [bytearray(), bytearray()],
        threading.Lock(),
        threading.Event(),
    )
    errors = []

    def drain(pipe, index):
        try:
            while True:
                block = os.read(pipe.fileno(), 512)
                if not block:
                    return
                with lock:
                    available = 8193 - sum(map(len, streams))
                    streams[index].extend(block[: max(0, available)])
                    if len(block) > available or sum(map(len, streams)) > 8192:
                        errors.append("report_overflow")
                        abort.set()
                        return
        except (OSError, ValueError):
            errors.append("capture_error")
            abort.set()

    try:
        if parent_pid is not None:
            extra = job.k.OpenProcess(0x400 | 0x10, False, parent_pid)
            if not extra:
                raise Failure("parent_handle")
            job.memory(extra)
        job.memory(job.k.GetCurrentProcess())
        process = subprocess.Popen(
            [sys.executable, "-I", "-S", "-B", "-", *arguments],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=BASE,
            creationflags=subprocess.CREATE_NO_WINDOW,
            env={k: os.environ[k] for k in ("SystemRoot", "WINDIR") if k in os.environ},
        )
        job.assign(process)
        creation, end, kernel, user = (w.FILETIME() for _ in range(4))
        if not job.k.GetProcessTimes(
            w.HANDLE(int(process._handle)),
            ctypes.byref(creation),
            ctypes.byref(end),
            ctypes.byref(kernel),
            ctypes.byref(user),
        ):
            raise Failure("birth_identity")
        samples, peak = 0, 0

        def sample():
            nonlocal samples, peak
            try:
                child_memory = job.memory(w.HANDLE(int(process._handle)))
            except Failure:
                if process.poll() is not None:
                    return
                raise
            owned = job.memory(job.k.GetCurrentProcess()) + child_memory
            if extra:
                owned += job.memory(extra)
            samples += 1
            peak = max(peak, owned)
            if owned > 512 * 2**20:
                raise Failure("owned_memory_limit")

        sample()
        readers = [
            threading.Thread(target=drain, args=(pipe, index), daemon=True)
            for index, pipe in enumerate((process.stdout, process.stderr))
        ]
        for reader in readers:
            reader.start()
        started = time.monotonic()
        process.stdin.write(code)
        process.stdin.close()
        while process.poll() is None:
            if abort.is_set():
                raise Failure("capture_refused")
            if time.monotonic() - started > seconds:
                raise Failure("worker_timeout")
            sample()
            time.sleep(0.05)
        process.wait(timeout=30)
        for reader in readers:
            reader.join(timeout=2)
        if errors or any(reader.is_alive() for reader in readers):
            raise Failure("capture_incomplete")
        result = {
            "status": "exited",
            "pid": process.pid,
            "creation_ticks": creation.dwHighDateTime << 32 | creation.dwLowDateTime,
            "assigned": True,
            "startup_gate": "stdin_after_assignment",
            "exit_code": process.returncode,
            "stdout": bytes(streams[0]).decode("utf-8", "strict"),
            "stderr": bytes(streams[1]).decode("utf-8", "strict"),
            "stdout_bytes": len(streams[0]),
            "stderr_bytes": len(streams[1]),
            "memory_samples": samples,
            "peak_owned_private_bytes": peak,
            "parent_shell_sampled": parent_pid is not None,
            "teardown_verified": True,
        }
        if process.returncode:
            raise Failure("worker_exit", exit=process.returncode)
        return result
    finally:
        if process is not None:
            if process.poll() is None:
                job.k.TerminateJobObject(job.handle, 99)
                if process.poll() is None:
                    process.kill()
            process.wait(timeout=30)
            for reader in readers:
                reader.join(timeout=2)
            for pipe in (process.stdout, process.stderr):
                if pipe:
                    pipe.close()
            if process.stdin and not process.stdin.closed:
                with contextlib.suppress(OSError):
                    process.stdin.close()
        if extra:
            job.k.CloseHandle(extra)
        job.close()


def save(path: Path, value: dict | list, cap: int = 8 * 2**20) -> None:
    """Exclusive bounded artifact evidence; console reporting is bounded separately."""
    raw = json.dumps(value, ensure_ascii=True, indent=2).encode()
    if len(raw) > cap:
        raise Failure("result_limit")
    with path.open("xb") as stream:
        stream.write(raw)


def acquire(specs: list[dict], budget: Budget) -> dict:
    """Admit the full fresh manifest before streaming the fixed wheel bodies."""
    manifests = []
    for spec in specs:
        buffer = io.BytesIO()
        fetch(
            f"https://pypi.org/pypi/{spec['distribution']}/{spec['version']}/json",
            2**20,
            budget,
            buffer,
        )
        raw = buffer.getvalue()
        with (ROOT / (spec["distribution"] + "-metadata.json")).open("xb") as stream:
            stream.write(raw)
        manifests.append(admit_entry(parse_json(raw), spec))
    save(ROOT / "admitted-manifest.json", manifests)
    directory = ROOT / "wheels"
    directory.mkdir()
    for spec in manifests:
        path = directory / (spec["filename"] + ".part")
        digest = hashlib.sha256()

        class Sink:
            def __init__(self, stream, hasher):
                self.stream, self.hasher = stream, hasher

            def write(self, data: bytes) -> int:
                self.hasher.update(data)
                return self.stream.write(data)

        with path.open("xb") as target:
            size = fetch(spec["url"], spec["size"], budget, Sink(target, digest))
        if size != spec["size"] or digest.hexdigest() != spec["sha256"]:
            raise Failure("download_identity")
        destination = directory / spec["filename"]
        if destination.exists():
            raise Failure("destination_exists")
        path.rename(destination)
    return {"status": "acquired", "artifacts": len(manifests), "manifest": manifests}


def worker(request_path: Path) -> None:
    """Execute one fixed request inside the verified one-process Job."""
    if request_path.parent != ROOT:
        raise Failure("request_root")
    with open_regular(request_path, ROOT) as stream:
        if os.fstat(stream.fileno()).st_size > 65536:
            raise Failure("request_limit")
        request = parse_json(stream.read(65537))
    operation = request["operation"]
    required_limit = 64 * 2**20 if operation == "acquire" else 256 * 2**20
    if (
        type(request.get("read_limit")) is not int
        or request["read_limit"] != required_limit
    ):
        raise Failure("request_lease")
    if operation == "acquire" and request.get("specs") != FIXED_SPECS:
        raise Failure("request_artifacts")
    if operation == "inspect" and request.get("cached") != FIXED_CACHED:
        raise Failure("request_cached")
    budget = Budget(read_limit=request["read_limit"])
    try:
        if operation == "acquire":
            result = acquire(request["specs"], budget)
        elif operation == "inspect":
            with open_regular(ROOT / "admitted-manifest.json", ROOT) as stream:
                raw = stream.read(65537)
            budget.reserve(len(raw))
            if (
                len(raw) > 65536
                or hashlib.sha256(raw).hexdigest() != request["manifest_sha256"]
            ):
                raise Failure("manifest_identity")
            manifests = parse_json(raw)
            if not isinstance(manifests, list) or len(manifests) != len(FIXED_SPECS):
                raise Failure("manifest_schema")
            for item, fixed in zip(manifests, FIXED_SPECS, strict=True):
                fresh = admit_entry(
                    {
                        "info": {
                            "name": fixed["distribution"],
                            "version": fixed["version"],
                        },
                        "urls": [
                            {
                                "filename": item.get("filename"),
                                "size": item.get("size"),
                                "digests": {"sha256": item.get("sha256")},
                                "yanked": False,
                                "url": item.get("url"),
                            }
                        ],
                    },
                    fixed,
                )
                if fresh != item:
                    raise Failure("manifest_schema")
            result = {
                "status": "inspected",
                "wheels": [
                    inspect_wheel(ROOT / "wheels" / item["filename"], item, budget)
                    for item in manifests
                ],
                "cached_roots": [
                    inspect_wheel(
                        BASE
                        / "data/t17/input-fit-tokenizer-static-01"
                        / item["filename"],
                        item,
                        budget,
                        True,
                    )
                    for item in request["cached"]
                ],
            }
        else:
            raise Failure("operation_refused")
        result["lease"] = {
            "read_used": budget.used,
            "http_bytes": budget.net,
            "http_transactions": budget.transactions,
            "expanded_bytes": budget.expanded,
            "notice_bytes": budget.notices,
            "entries": budget.entries,
        }
        save(ROOT / (operation + "-result.json"), result)
        print(
            json.dumps(
                {
                    "status": result["status"],
                    "operation": operation,
                    "http_transactions": budget.transactions,
                }
            )
        )
    except Exception as exc:
        save(
            ROOT / (operation + "-failure.json"),
            {
                "status": "stopped",
                "error": type(exc).__name__,
                "code": getattr(exc, "code", "unclassified"),
                "reads": budget.used,
                "http_bytes": budget.net,
                "http_transactions": budget.transactions,
            },
        )
        raise


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "worker":
        worker(Path(sys.argv[2]))
    else:
        raise SystemExit("Only an owned worker request is supported")
