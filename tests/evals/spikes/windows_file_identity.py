"""IF-I one synthetic Windows stat investigation; never read model/user files."""

import hashlib
import json
import os
import stat
import sys
import time
from collections.abc import Callable
from pathlib import Path

REPO = Path(__file__).absolute().parents[3]
RUN = REPO / "data/t17/windows-identity-01"
DATA = b"IF-I synthetic identity fixture\n"
IDENTITY_FIELDS = (
    "st_dev",
    "st_ino",
    "st_size",
    "st_mtime_ns",
    "st_ctime_ns",
    "st_mode",
    "st_nlink",
)
FIELDS = (*IDENTITY_FIELDS, "st_file_attributes", "st_reparse_tag", "st_birthtime_ns")


class Boundary(RuntimeError):
    """Refuse outside, excessive, changed or incomplete probe inputs."""


def snapshot(info: os.stat_result) -> dict:
    """Preserve missing versus zero fields without normalizing observations."""
    return {
        name: {"present": hasattr(info, name), "value": getattr(info, name, None)}
        for name in FIELDS
    }


def compare(left: dict, right: dict, fields: tuple = IDENTITY_FIELDS) -> dict:
    """Report exact differing and unavailable fields; this is not an identity policy."""
    differences, missing = {}, []
    for name in fields:
        a, b = left[name], right[name]
        if not a["present"] or not b["present"]:
            missing.append(name)
        elif a["value"] != b["value"]:
            differences[name] = {"left": a["value"], "right": b["value"]}
    return {
        "differences": differences,
        "missing": missing,
        "equal": not differences and not missing,
    }


class Budget:
    """Count all explicit fixture/ancestor stat calls and conservatively bounded reads."""

    def __init__(self) -> None:
        self.stats = 0
        self.read_bytes = 0
        self.actual_read_bytes = 0

    def stat(
        self, path: Path | None = None, *, fd: int | None = None, follow: bool = False
    ) -> os.stat_result:
        """Charge before one stat/lstat/fstat, including failures."""
        if self.stats >= 32:
            raise Boundary("Stat cap")
        self.stats += 1
        if fd is not None:
            return os.fstat(fd)
        if path is None:
            raise Boundary("Missing stat target")
        return path.stat() if follow else path.lstat()

    def read(self, stream) -> bytes:
        """Charge the full65-byte possible read before touching the fixture."""
        if self.read_bytes + 65 > 4096:
            raise Boundary("Read cap")
        self.read_bytes += 65
        raw = stream.read(65)
        self.actual_read_bytes += len(raw)
        if len(raw) > 64:
            raise Boundary("Fixture size cap")
        return raw


def validate_target(run: Path, target: Path, budget: Budget) -> None:
    """Check the one allowed fixture and finite ancestor types before creation."""
    if run != RUN or target != RUN / "fixture.bin" or ".." in target.parts:
        raise Boundary("Fixed target only")
    chain = (*reversed(tuple(run.parents)), run)
    if not run.is_absolute() or len(chain) > 24 or len(set(chain)) != len(chain):
        raise Boundary("Ancestry boundary")
    for parent in chain:
        info = budget.stat(parent)
        if (
            not stat.S_ISDIR(info.st_mode)
            or getattr(info, "st_file_attributes", 0) & 0x400
        ):
            raise Boundary("Ancestor type or reparse")
    try:
        budget.stat(target)
    except FileNotFoundError:
        return
    raise Boundary("Fixture already exists")


def verify_bytes(raw: bytes, expected: bytes) -> None:
    """Refuse unexpected fixture contents without printing them."""
    if raw != expected:
        raise Boundary("Unexpected fixture content")


def content_change(before: bytes, after: bytes) -> dict:
    """Keep content hash and size observations separate from stat comparisons."""
    old_hash, new_hash = (hashlib.sha256(raw).hexdigest() for raw in (before, after))
    return {
        "before_hash": old_hash,
        "after_hash": new_hash,
        "before_size": len(before),
        "after_size": len(after),
        "size_changed": len(before) != len(after),
        "hash_changed": old_hash != new_hash,
    }


def sample(path: Path, budget: Budget, expected: bytes) -> dict:
    """Capture one bounded read and five actual stat observations."""
    values = {
        "lstat_before": snapshot(budget.stat(path)),
        "stat_before": snapshot(budget.stat(path, follow=True)),
    }
    with path.open("rb") as stream:
        values["fstat_before"] = snapshot(budget.stat(fd=stream.fileno()))
        raw = budget.read(stream)
        values["fstat_after"] = snapshot(budget.stat(fd=stream.fileno()))
    values["lstat_after"] = snapshot(budget.stat(path))
    verify_bytes(raw, expected)
    return {
        "observations": values,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "size": len(raw),
        "path_handle": compare(values["lstat_before"], values["fstat_before"]),
        "path_stat_lstat": compare(
            values["lstat_before"], values["stat_before"], FIELDS
        ),
        "handle_stability": compare(values["fstat_before"], values["fstat_after"]),
        "path_stability": compare(values["lstat_before"], values["lstat_after"]),
    }


def probe(run: Path, save: Callable) -> dict:
    """Exclusively create one synthetic file, observe it, modify one byte and finish."""
    budget = Budget()
    path = run / "fixture.bin"
    validate_target(run, path, budget)
    state = {
        "status": "started",
        "python": sys.version.split()[0],
        "platform": sys.platform,
    }
    save(state)
    try:
        with path.open("xb") as stream:
            stream.write(DATA)
            stream.flush()
            os.fsync(stream.fileno())
        state["unchanged"] = sample(path, budget, DATA)
        state["status"] = "unchanged_captured"
        save(state)
        with path.open("r+b") as stream:
            stream.write(b"X")
            stream.flush()
            os.fsync(stream.fileno())
        modified = b"X" + DATA[1:]
        state["modified"] = sample(path, budget, modified)
        state["path_after_modification"] = compare(
            state["unchanged"]["observations"]["lstat_after"],
            state["modified"]["observations"]["lstat_before"],
            FIELDS,
        )
        state["content_change"] = content_change(DATA, modified)
        state.update(
            status="complete",
            stats=budget.stats,
            charged_read_bytes=budget.read_bytes,
            actual_read_bytes=budget.actual_read_bytes,
        )
        save(state)
        return state
    except Exception as error:
        state.update(
            status="stopped_no_retry",
            error=type(error).__name__,
            stats=budget.stats,
            charged_read_bytes=budget.read_bytes,
            actual_read_bytes=budget.actual_read_bytes,
        )
        save(state)
        raise


def persist(value: dict) -> None:
    """Flush a bounded receipt in the validated owned run directory."""
    raw = json.dumps(value, sort_keys=True).encode("utf-8")
    if len(raw) > 65536:
        raise Boundary("Receipt cap")
    temporary = RUN / "receipt.pending"
    with temporary.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, RUN / "receipt.json")


if __name__ == "__main__":
    try:
        meter = json.loads((RUN / "meter.json").read_text(encoding="utf-8-sig"))
        elapsed = time.perf_counter() - meter["started_qpc"] / meter["frequency"]
        if (
            sys.argv[1:] != ["probe"]
            or meter["status"] != "active"
            or meter["probe_attempts"] != 1
            or not 0 <= elapsed < 840
        ):
            raise Boundary("Dispatch/allocation boundary")
        probe(RUN, persist)
        print('{"status":"complete"}', flush=True)
    except (OSError, ValueError, Boundary) as error:
        print(
            json.dumps({"status": "stopped_no_retry", "error": type(error).__name__}),
            flush=True,
        )
        sys.exit(1)
