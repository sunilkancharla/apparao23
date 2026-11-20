"""Hub-only static review using hash-pinned, locally authored primitives.

No candidate module or native library is imported. Verified authored source is
compiled from the same bytes that were hashed; no closed trial entry point runs.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import os
import stat
import sys
import time
import types
import zipfile
import zlib
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
RUN = BASE / "data/t17/hub-only-static-review-01"
PRIMITIVE = Path(__file__).with_name("standalone_static_verification.py")
PRIMITIVE_SHA = "691d86c9cc750a2f88b266230e0938936d92ce54c3b5f21684bd3a080fcd6d03"
WHEEL = (
    BASE
    / "data/t17/input-fit-tokenizer-static-01/huggingface_hub-2.4.0-py3-none-any.whl"
)
WHEEL_SIZE = 857_021
WHEEL_SHA = "42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801"


class ReviewFailure(Exception):
    """Content-free failure code, never an arbitrary path or upstream message."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


class Counter:
    """Precharge reads against a shared persistent hook or synthetic allowance."""

    def __init__(self, limit: int, hook: Callable[[int], None] | None = None):
        self.limit, self.hook, self.used = limit, hook, 0

    def reserve(self, amount: int) -> None:
        """Refuse before I/O; short/failed attempts are never refunded."""
        if not isinstance(amount, int) or amount < 0 or self.used + amount > self.limit:
            raise ReviewFailure("read_limit")
        if self.hook:
            self.hook(amount)
        self.used += amount


@dataclass(frozen=True)
class Policy:
    """Hub-only admission limits; old runtime defaults remain untouched."""

    entries: int = 256
    expanded: int = 16 * 2**20
    metadata: int = 256 * 1024
    notice: int = 256 * 1024
    notices_total: int = 2**20


def _fingerprint(value: os.stat_result) -> tuple:
    return (
        value.st_dev,
        value.st_ino,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
        value.st_nlink,
        value.st_mode,
    )


def load_primitives(counter: Counter) -> types.ModuleType:
    """Execute only the exact reviewed authored bytes, bound to their hash."""
    for parent in reversed(PRIMITIVE.parents):
        value = parent.lstat()
        if (
            not stat.S_ISDIR(value.st_mode)
            or getattr(value, "st_file_attributes", 0) & 0x400
        ):
            raise ReviewFailure("owned_source_type")
    before = PRIMITIVE.lstat()
    if (
        not stat.S_ISREG(before.st_mode)
        or before.st_nlink != 1
        or getattr(before, "st_file_attributes", 0) & 0x400
        or before.st_size > 65536
    ):
        raise ReviewFailure("owned_source_type")
    counter.reserve(before.st_size + 1)
    with PRIMITIVE.open("rb") as stream:
        opened = os.fstat(stream.fileno())
        if (before.st_dev, before.st_ino, before.st_size) != (
            opened.st_dev,
            opened.st_ino,
            opened.st_size,
        ):
            raise ReviewFailure("owned_source_identity")
        data = stream.read(before.st_size + 1)
        if _fingerprint(opened) != _fingerprint(os.fstat(stream.fileno())):
            raise ReviewFailure("owned_source_identity")
    if (
        _fingerprint(before) != _fingerprint(PRIMITIVE.lstat())
        or len(data) != before.st_size
        or hashlib.sha256(data).hexdigest() != PRIMITIVE_SHA
    ):
        raise ReviewFailure("owned_source_identity")
    module = types.ModuleType("_hs_verified_authored_primitives")
    module.__file__ = str(PRIMITIVE)
    sys.modules[module.__name__] = module
    # Explicitly authorized owned code, not bytes from a wheel or user document.
    exec(compile(data, str(PRIMITIVE), "exec"), module.__dict__)  # noqa: S102
    return module


def _text(
    archive: zipfile.ZipFile, entry: zipfile.ZipInfo, cap: int, counter: Counter
) -> str:
    if entry.file_size > cap:
        raise ReviewFailure("text_limit")
    counter.reserve(entry.file_size + 1)
    with archive.open(entry) as member:
        data = member.read(entry.file_size + 1)
    if len(data) != entry.file_size:
        raise ReviewFailure("member_size")
    return data.decode("utf-8")


def inspect_hub(
    path: Path, size: int, sha: str, counter: Counter, policy: Policy | None = None
) -> dict:
    """Admit a hash-verified wheel, verify RECORD, then retain bounded texts."""
    primitive = load_primitives(counter)
    policy = policy or Policy()
    try:
        initial = primitive.fingerprint(path.lstat())
        if (
            path.lstat().st_size != size
            or primitive.hash_regular(path, path.parent, counter) != sha
        ):
            raise ReviewFailure("wheel_identity")
        limits = primitive.Limits(
            max_entries=policy.entries, max_expanded=policy.expanded
        )
        with primitive.open_regular(path, path.parent) as stream:
            if primitive.fingerprint(path.lstat()) != initial:
                raise ReviewFailure("wheel_identity")
            charged = primitive.ChargedFile(stream, counter)
            primitive.central_admission(charged, limits)
            with zipfile.ZipFile(charged) as archive:
                entries = primitive.admitted_entries(archive, limits)
                files = {e.filename: e for e in entries if not e.is_dir()}
                metadata = [n for n in files if n.endswith(".dist-info/METADATA")]
                records = [n for n in files if n.endswith(".dist-info/RECORD")]
                if (
                    len(metadata) != 1
                    or len(records) != 1
                    or metadata[0].rsplit("/", 1)[0] != records[0].rsplit("/", 1)[0]
                ):
                    raise ReviewFailure("wheel_metadata")
                record_text = _text(
                    archive, files[records[0]], policy.metadata, counter
                )
                seen, hashes = set(), {}
                for number, row in enumerate(csv.reader(io.StringIO(record_text)), 1):
                    if (
                        number > policy.entries
                        or len(row) != 3
                        or row[0] not in files
                        or row[0] in seen
                    ):
                        raise ReviewFailure("record_layout")
                    name = row[0]
                    seen.add(name)
                    if name == records[0]:
                        if row[1:] != ["", ""]:
                            raise ReviewFailure("record_self")
                        continue
                    entry = files[name]
                    if not row[1].startswith("sha256=") or row[2] != str(
                        entry.file_size
                    ):
                        raise ReviewFailure("record_size_or_algorithm")
                    with archive.open(entry) as member:
                        actual = primitive.digest_stream(
                            member, entry.file_size, counter
                        )
                    encoded = (
                        base64.urlsafe_b64encode(bytes.fromhex(actual))
                        .decode()
                        .rstrip("=")
                    )
                    if row[1] != "sha256=" + encoded:
                        raise ReviewFailure("record_hash")
                    hashes[name] = actual
                if seen != set(files):
                    raise ReviewFailure("record_coverage")
                result = {
                    "wheel_sha256": sha,
                    "entries": len(entries),
                    "record_verified": True,
                    "metadata": _text(
                        archive, files[metadata[0]], policy.metadata, counter
                    ),
                    "native_names": [],
                    "notices": [],
                    "member_hashes": hashes,
                }
                total = 0
                for name, entry in files.items():
                    if Path(name).suffix.lower() in {
                        ".dll",
                        ".exe",
                        ".pyd",
                        ".so",
                        ".dylib",
                    }:
                        result["native_names"].append(name)
                    if not any(
                        word in Path(name).name.lower()
                        for word in ("license", "notice", "copying", "copyright")
                    ):
                        continue
                    note = {"name": name, "sha256": hashes.get(name)}
                    if (
                        entry.file_size > policy.notice
                        or total + entry.file_size > policy.notices_total
                    ):
                        note["status"] = "unreviewed_size_cap"
                    else:
                        total += entry.file_size
                        try:
                            note["text"] = _text(archive, entry, policy.notice, counter)
                            note["status"] = "read_utf8_not_legal_clearance"
                        except UnicodeDecodeError:
                            note["status"] = "unreviewed_encoding"
                    result["notices"].append(note)
                return result
    except primitive.Failure as error:
        raise ReviewFailure(error.code) from error
    except (
        zipfile.BadZipFile,
        zlib.error,
        csv.Error,
        UnicodeDecodeError,
        EOFError,
    ) as error:
        raise ReviewFailure("wheel_parse") from error


def save_json(path: Path, value: dict) -> None:
    """Flush bounded new-root receipts; never use the old root's writer."""
    if path.parent != RUN:
        raise ReviewFailure("receipt_root")
    data = json.dumps(value, ensure_ascii=True, indent=2).encode()
    if len(data) > 2**20:
        raise ReviewFailure("receipt_limit")
    retained = sum(p.stat().st_size for p in RUN.iterdir() if p.is_file())
    old = path.stat().st_size if path.exists() else 0
    if retained - old + len(data) + 2_621_440 > 8_388_608:
        raise ReviewFailure("artifact_limit")
    with path.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def worker() -> None:
    """One bounded real-wheel attempt, with content-free partial failures."""
    meter_path = RUN / "meter.json"
    start = time.monotonic()
    packet = {"status": "stopped_no_retry", "candidate_import_or_execution": False}

    def charge(amount: int) -> None:
        meter = json.loads(meter_path.read_text(encoding="utf-8"))
        elapsed = time.time() - datetime.fromisoformat(meter["started_utc"]).timestamp()
        if (
            meter["status"] != "active"
            or elapsed > 2400
            or time.monotonic() - start > 110
        ):
            raise ReviewFailure("worker_boundary")
        new = meter["used"]["streamed_read_bytes"] + amount
        if new > 134_217_728:
            raise ReviewFailure("read_limit")
        meter["used"]["streamed_read_bytes"] = new
        save_json(meter_path, meter)

    meter = json.loads(meter_path.read_text(encoding="utf-8"))
    counter = Counter(134_217_728 - meter["used"]["streamed_read_bytes"], charge)
    try:
        packet["inspection"] = inspect_hub(WHEEL, WHEEL_SIZE, WHEEL_SHA, counter)
        packet["status"] = "completed_static_pending_research_no_adoption"
    except ReviewFailure as error:
        packet["failure"] = {"code": error.code}
    except (OSError, ValueError) as error:
        packet["failure"] = {"code": "static_io", "type": type(error).__name__}
    finally:
        packet["streamed_reads"] = counter.used
        packet["elapsed_seconds"] = round(time.monotonic() - start, 6)
        save_json(RUN / "worker-result.json", packet)


if __name__ == "__main__":
    if sys.argv[1:] != ["worker"]:
        raise SystemExit("Only the approved worker entry point is available")
    worker()
