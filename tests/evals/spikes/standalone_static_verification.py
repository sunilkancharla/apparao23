"""Bounded, inert comparison of the approved cached runtime and installation.

This is an evaluation aid, not application code or a native safety boundary.
Only its authored Python is executed. Candidate bytes are hashed, never loaded.
"""

from __future__ import annotations

import base64
import contextlib
import csv
import hashlib
import io
import json
import os
import re
import stat
import struct
import sys
import time
import zipfile
import zlib
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

BASE = Path(__file__).resolve().parents[3]
RUN = BASE / "data/t17/standalone-static-verification-03"
ARCHIVE = BASE / ".venv/.cache/ollama/ollama-windows-amd64-0.40.16.zip"
INSTALLED = BASE / ".venv/tools/ollama/0.40.16"
ARCHIVE_SIZE = 1_618_244_995
ARCHIVE_SHA = "50fcf5ad54277f2fa5d173ebfc93bcb017adbc0c9ef2314daabc96ca9e6aa64e"
WHEELS = (
    (
        "tokenizers-0.23.3-cp310-abi3-win_amd64.whl",
        2_872_101,
        "1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3",
    ),
    (
        "huggingface_hub-2.4.0-py3-none-any.whl",
        857_021,
        "42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801",
    ),
)
CHUNK = 1_048_576


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


def archive_entries(path: Path, budget: ReadBudget, limits: Limits) -> list[str]:
    """Return admitted member names; used by synthetic admission controls."""
    with open_regular(path, path.parent) as handle:
        charged = ChargedFile(handle, budget)
        central_admission(charged, limits)
        try:
            with zipfile.ZipFile(charged) as archive:
                return [entry.filename for entry in admitted_entries(archive, limits)]
        except (zipfile.BadZipFile, zlib.error) as error:
            raise Failure("invalid_zip") from error


def installed_files(root: Path, limits: Limits) -> dict[str, Path]:
    """Bound directory enumeration and refuse links before following paths."""
    check_ancestors(root / "placeholder")
    pending, result, directories, aliases = [root], {}, 0, set()
    while pending:
        parent = pending.pop()
        with os.scandir(parent) as entries:
            for entry in entries:
                path = Path(entry.path)
                # Windows DirEntry.stat can report zero link/inode fields.
                # Obtain full path identity before deciding link admission.
                value = path.lstat()
                name = checked_name(path.relative_to(root).as_posix(), limits.max_depth)
                if is_reparse(value) or name.casefold() in aliases:
                    raise Failure("installed_type")
                aliases.add(name.casefold())
                if stat.S_ISDIR(value.st_mode):
                    directories += 1
                    if directories > limits.max_entries:
                        raise Failure("directory_limit")
                    pending.append(path)
                elif stat.S_ISREG(value.st_mode) and value.st_nlink == 1:
                    result[name] = path
                    if len(result) > limits.max_entries:
                        raise Failure("installed_limit")
                else:
                    raise Failure("installed_type")
    return result


def inspect_pair(
    archive_path: Path,
    root: Path,
    expected_size: int,
    expected_sha: str,
    budget: ReadBudget,
    limits: Limits,
) -> dict:
    """Compare every admitted runtime file, retaining native/notice inventory."""
    initial = fingerprint(archive_path.lstat())
    if archive_path.lstat().st_size != expected_size:
        raise Failure("archive_size")
    if hash_regular(archive_path, archive_path.parent, budget) != expected_sha:
        raise Failure("archive_hash")
    result = {
        "archive_sha256": expected_sha,
        "files_compared": 0,
        "native_files": [],
        "files": [],
        "notices": [],
    }
    with open_regular(archive_path, archive_path.parent) as handle:
        if fingerprint(archive_path.lstat()) != initial:
            raise Failure("archive_changed")
        charged = ChargedFile(handle, budget)
        central_admission(charged, limits)
        try:
            with zipfile.ZipFile(charged) as archive:
                entries = [
                    entry
                    for entry in admitted_entries(archive, limits)
                    if not entry.is_dir()
                ]
                local = installed_files(root, limits)
                if set(local) != {entry.filename for entry in entries}:
                    raise Failure(
                        "installed_set", archive=len(entries), installed=len(local)
                    )
                notice_total = 0
                for entry in entries:
                    path = local[entry.filename]
                    if path.lstat().st_size != entry.file_size:
                        raise Failure("installed_size")
                    with archive.open(entry) as member:
                        archive_sha = digest_stream(member, entry.file_size, budget)
                    if archive_sha != hash_regular(path, root, budget):
                        raise Failure("installed_hash")
                    result["files"].append(
                        {
                            "name": entry.filename,
                            "bytes": entry.file_size,
                            "sha256": archive_sha,
                        }
                    )
                    result["files_compared"] += 1
                    if path.suffix.lower() in {".dll", ".exe", ".pyd", ".so", ".dylib"}:
                        result["native_files"].append(entry.filename)
                    if any(
                        word in path.name.lower()
                        for word in ("license", "notice", "copying")
                    ):
                        notice = {"name": entry.filename, "sha256": archive_sha}
                        if (
                            entry.file_size > limits.max_notice
                            or notice_total + entry.file_size > limits.max_notices_total
                        ):
                            notice["status"] = "unreviewed_size_cap"
                        else:
                            with open_regular(path, root) as source:
                                budget.reserve(entry.file_size + 1)
                                data = source.read(entry.file_size + 1)
                            if len(data) != entry.file_size:
                                raise Failure("file_changed")
                            notice_total += len(data)
                            if hashlib.sha256(data).hexdigest() != archive_sha:
                                raise Failure("file_changed")
                            try:
                                notice["text"] = data.decode("utf-8")
                                notice["status"] = "read_utf8_not_legal_clearance"
                            except UnicodeDecodeError:
                                notice["status"] = "unreviewed_encoding"
                        result["notices"].append(notice)
                if set(installed_files(root, limits)) != set(local):
                    raise Failure("file_changed")
        except (zipfile.BadZipFile, zlib.error, EOFError) as error:
            raise Failure("invalid_zip") from error
    return result


def durable_json(path: Path, value: dict) -> None:
    """Flush bounded owned receipts; errors propagate without retry."""
    data = json.dumps(value, ensure_ascii=True, indent=2).encode()
    if len(data) > 2 * 1024 * 1024:
        raise Failure("receipt_limit")
    if path.parent == RUN:
        # Retained files plus conservative authored-source/fixture allowances.
        retained = sum(p.stat().st_size for p in RUN.iterdir() if p.is_file())
        old = path.stat().st_size if path.exists() else 0
        if retained - old + len(data) + 2_621_440 > 8_388_608:
            raise Failure("artifact_limit")
    with path.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def inspect_wheel(path: Path, size: int, sha: str, budget: ReadBudget) -> dict:
    """Read bounded wheel metadata/RECORD only after exact payload identity."""
    initial = fingerprint(path.lstat())
    if path.lstat().st_size != size or hash_regular(path, path.parent, budget) != sha:
        raise Failure("wheel_identity")
    limits = Limits()
    with open_regular(path, path.parent) as handle:
        if fingerprint(path.lstat()) != initial:
            raise Failure("wheel_changed")
        charged = ChargedFile(handle, budget)
        central_admission(charged, limits)
        with zipfile.ZipFile(charged) as archive:
            entries = admitted_entries(archive, limits)
            names = {entry.filename: entry for entry in entries if not entry.is_dir()}
            metadata = [name for name in names if name.endswith(".dist-info/METADATA")]
            records = [name for name in names if name.endswith(".dist-info/RECORD")]
            if len(metadata) != 1 or len(records) != 1:
                raise Failure("wheel_metadata")
            texts = {}
            for name in metadata + records:
                if names[name].file_size > 256 * 1024:
                    raise Failure("wheel_metadata_limit")
                budget.reserve(names[name].file_size + 1)
                with archive.open(name) as member:
                    data = member.read(names[name].file_size + 1)
                if len(data) != names[name].file_size:
                    raise Failure("wheel_metadata")
                texts[name] = data.decode("utf-8")
            rows = list(csv.reader(io.StringIO(texts[records[0]])))
            seen = set()
            for row in rows:
                if len(row) != 3 or row[0] not in names or row[0] in seen:
                    raise Failure("wheel_record")
                seen.add(row[0])
                if row[0] == records[0]:
                    if row[1:] != ["", ""]:
                        raise Failure("wheel_record")
                    continue
                if not row[1].startswith("sha256=") or row[2] != str(
                    names[row[0]].file_size
                ):
                    raise Failure("wheel_record")
                with archive.open(row[0]) as member:
                    actual = digest_stream(member, names[row[0]].file_size, budget)
                encoded = (
                    base64.urlsafe_b64encode(bytes.fromhex(actual)).decode().rstrip("=")
                )
                if row[1] != "sha256=" + encoded:
                    raise Failure("wheel_record")
            if seen != set(names):
                raise Failure("wheel_record")
            return {
                "sha256": sha,
                "metadata": texts[metadata[0]],
                "record_verified": True,
                "members": len(entries),
                "notice_review": "not_completed",
            }


def worker() -> None:
    """Single supervised real-data attempt; retain partial failure without retry."""
    meter_path = RUN / "meter.json"
    start = time.monotonic()
    packet = {
        "status": "stopped_no_retry",
        "stage": "entry",
        "candidate_execution": False,
    }

    def charge(amount: int) -> None:
        meter = json.loads(meter_path.read_text(encoding="utf-8"))
        if meter["status"] != "active" or time.monotonic() - start > 590:
            raise Failure("worker_boundary")
        used = meter["used"]["streamed_read_bytes"] + amount
        if used > meter["limits"]["streamed_read_bytes"]:
            raise Failure("read_limit")
        meter["used"]["streamed_read_bytes"] = used
        durable_json(meter_path, meter)

    meter = json.loads(meter_path.read_text(encoding="utf-8"))
    budget = ReadBudget(
        meter["limits"]["streamed_read_bytes"] - meter["used"]["streamed_read_bytes"],
        charge,
    )
    try:
        packet["stage"] = "runtime_archive_comparison"
        packet["runtime"] = inspect_pair(
            ARCHIVE, INSTALLED, ARCHIVE_SIZE, ARCHIVE_SHA, budget, Limits()
        )
        executable = [
            row for row in packet["runtime"]["files"] if row["name"] == "ollama.exe"
        ]
        if (
            len(executable) != 1
            or executable[0]["sha256"]
            != "4ccefcbfecc50fb6526471adabbc20869dd614e29e351120b15083cb174b0b8a"
        ):
            raise Failure("installed_executable_identity")
        packet["stage"] = "wheel_identity_and_metadata"
        packet["wheels"] = []
        for name, size, digest in WHEELS:
            path = BASE / "data/t17/input-fit-tokenizer-static-01" / name
            packet["wheels"].append(inspect_wheel(path, size, digest, budget))
        packet["status"] = "completed_static_pending_review_no_adoption"
    except Failure as error:
        packet["failure"] = {"code": error.code, "counts": error.counts}
    except (OSError, ValueError, zipfile.BadZipFile, zlib.error) as error:
        packet["failure"] = {"code": "static_io_or_parse", "type": type(error).__name__}
    finally:
        packet["streamed_read_bytes_charged"] = budget.used
        packet["elapsed_seconds"] = round(time.monotonic() - start, 6)
        durable_json(RUN / "worker-result.json", packet)


if __name__ == "__main__":
    if sys.argv[1:] != ["worker"]:
        raise SystemExit("Only the approved worker entry point is available")
    worker()
