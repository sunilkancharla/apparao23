"""IF-O synthetic-only persistence diagnostics; no acquisition code is imported."""

from __future__ import annotations

import ctypes
import json
import os
import stat
import time
from ctypes import wintypes
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "data/t17/receipt-persistence-01"
CASES = {"baseline", "locked", "positive", "stale"}
STAGES = ("open_temp", "write_json", "flush", "fsync", "close_temp", "replace_target")


class DiagnosticFailure(RuntimeError):
    """Independent reporting failed; never proceed or change reporting transport."""


class StageFailure(RuntimeError):
    """Retain scalar error identity without arbitrary exception messages/paths."""

    def __init__(self, stage: str, error: Exception):
        super().__init__(stage)
        self.stage = stage
        self.kind = type(error).__name__
        self.errno = getattr(error, "errno", None)
        self.winerror = getattr(error, "winerror", None)


def is_reparse(path: Path) -> bool:
    """Check links/reparse attributes without following their targets."""
    value = path.lstat()
    return stat.S_ISLNK(value.st_mode) or bool(
        getattr(value, "st_file_attributes", 0) & 0x400
    )


def case_directory(root: Path, case: str) -> Path:
    """Allow fixed synthetic case names and refuse reparse ancestors."""
    if case not in CASES:
        raise ValueError("Unknown synthetic case")
    directory = root / "cases" / case
    for path in (directory, *directory.parents):
        if path.exists() and is_reparse(path):
            raise ValueError("Reparse boundary")
    if not directory.resolve().is_relative_to(root.resolve()):
        raise ValueError("Case containment boundary")
    directory.mkdir(parents=True, exist_ok=True)
    for name in ("target.pending", "target.json"):
        path = directory / name
        if path.exists() and (is_reparse(path) or not path.is_file()):
            raise ValueError("Unsafe case file")
    return directory


def emit(record, case: str, stage: str, status: str, error=None, **scalars) -> None:
    """Reporting is independent and terminal on failure, with no raw error text."""
    packet = {"case": case, "stage": stage, "status": status, **scalars}
    if error is not None:
        packet.update(
            exception=type(error).__name__,
            errno=getattr(error, "errno", None),
            winerror=getattr(error, "winerror", None),
        )
    try:
        record(packet)
    except Exception as failure:  # noqa: BLE001 -- diagnostic boundary, no recovery
        raise DiagnosticFailure(type(failure).__name__) from None


def save_case(root: Path, case: str, value: dict, record, overrides=None) -> Path:
    """Instrument the original I/O sequence on synthetic files, without retries."""
    body = json.dumps(value)
    if len(body.encode()) > 8192:
        raise ValueError("Synthetic body boundary")
    directory = case_directory(root, case)
    temporary, target = directory / "target.pending", directory / "target.json"
    stream = None
    overrides = overrides or {}
    try:
        for stage in STAGES:
            emit(record, case, stage, "before")
            try:
                if stage in overrides:
                    overrides[stage]()
                elif stage == "open_temp":
                    stream = temporary.open("x", encoding="utf-8")
                elif stage == "write_json":
                    json.dump(value, stream)
                elif stage == "flush":
                    stream.flush()
                elif stage == "fsync":
                    os.fsync(stream.fileno())
                elif stage == "close_temp":
                    stream.close()
                elif stage == "replace_target":
                    os.replace(temporary, target)
            except (OSError, TypeError, ValueError) as error:
                emit(record, case, stage, "failure", error)
                raise StageFailure(stage, error) from None
            emit(record, case, stage, "success")
    finally:
        if stream is not None and not stream.closed:
            try:
                stream.close()
            except OSError as error:
                emit(record, case, "cleanup_close", "failure", error)
                raise StageFailure("cleanup_close", error) from None
            emit(record, case, "cleanup_close", "success")
    return target


class Guard:
    """Independent fixed-epoch/case/output accounting; not the writer under test."""

    def __init__(self, root: Path):
        self.root = root
        self.attempts = 0

    def tree_bytes(self) -> int:
        pending, count, size = [self.root], 0, 0
        while pending:
            with os.scandir(pending.pop()) as entries:
                for entry in entries:
                    count += 1
                    if count > 256 or is_reparse(Path(entry.path)):
                        raise ValueError("Synthetic tree boundary")
                    if entry.is_dir(follow_symlinks=False):
                        pending.append(Path(entry.path))
                    elif entry.is_file(follow_symlinks=False):
                        size += entry.stat(follow_symlinks=False).st_size
                    else:
                        raise ValueError("Synthetic file type")
        return size

    def check(self) -> None:
        for path in (self.root, *self.root.parents):
            if is_reparse(path):
                raise ValueError("Root reparse boundary")
        state = json.loads((self.root / "meter.json").read_text(encoding="utf-8-sig"))
        start = state["started_utc"]
        started = (
            datetime.fromisoformat(start).timestamp()
            if isinstance(start, str)
            else start
        )
        if state["status"] != "active" or not 0 <= time.time() - started <= 1200:
            raise ValueError("Epoch state/time boundary")
        if (
            "started_tick" in state
            and not 0
            <= time.perf_counter() - state["started_tick"] / state["frequency"]
            <= 1200
        ):
            raise ValueError("Monotonic time boundary")
        if self.tree_bytes() >= 2 * 1024**2 - 16384:
            raise ValueError("Synthetic output boundary")

    def claim(self) -> None:
        self.check()
        with (self.root / "worker-claim.json").open("x", encoding="utf-8") as stream:
            json.dump({"pid": os.getpid(), "no_retry": True}, stream)
            stream.flush()
            os.fsync(stream.fileno())

    def begin(self, case: str, record) -> None:
        self.check()
        if case not in CASES or self.attempts >= 131:
            raise ValueError("Case/attempt boundary")
        self.attempts += 1
        emit(record, case, "attempt", "precharged", attempt=self.attempts)


class Journal:
    """Single-writer append-only diagnostics, never using save_case."""

    def __init__(self, guard: Guard):
        self.guard = guard
        guard.check()
        self.stream = (guard.root / "operations.jsonl").open("xb")

    def __enter__(self):
        return self

    def __exit__(self, *exception):
        self.stream.close()

    def __call__(self, packet: dict) -> None:
        self.guard.check()
        encoded = (json.dumps(packet) + "\n").encode()
        if len(encoded) > 1024:
            raise ValueError("Diagnostic packet boundary")
        self.stream.write(encoded)
        self.stream.flush()
        os.fsync(self.stream.fileno())


def execute_probe(guard: Guard, record) -> dict:
    """Run exactly the four approved cases; Windows handle APIs stay here."""
    for counter in range(1, 129):
        guard.begin("baseline", record)
        target = save_case(guard.root, "baseline", {"counter": counter}, record)
        if json.loads(target.read_text()) != {"counter": counter}:
            raise ValueError("Baseline publication mismatch")
    directory = case_directory(guard.root, "locked")
    old = b'{"counter":0}'
    (directory / "target.json").write_bytes(old)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateFileW.argtypes = [
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    ]
    kernel.CreateFileW.restype = wintypes.HANDLE
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.restype = wintypes.BOOL
    handle = kernel.CreateFileW(
        str(directory / "target.json"), 0x80000000, 3, None, 3, 0x80, None
    )
    if handle == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    outcome = None
    try:
        emit(record, "locked", "handle_open", "success")
        guard.begin("locked", record)
        try:
            save_case(guard.root, "locked", {"counter": 1}, record)
        except StageFailure as error:
            outcome = error
        if (
            outcome is None
            or outcome.stage != "replace_target"
            or outcome.kind != "PermissionError"
        ):
            raise ValueError("Sharing negative control failed")
        if (directory / "target.json").read_bytes() != old or json.loads(
            (directory / "target.pending").read_text()
        ) != {"counter": 1}:
            raise ValueError("Sharing preservation mismatch")
    finally:
        closed = bool(kernel.CloseHandle(handle))
        emit(
            record,
            "locked",
            "handle_close",
            "success" if closed else "failure",
            closed=closed,
        )
        if not closed:
            raise ctypes.WinError(ctypes.get_last_error())
    guard.begin("positive", record)
    positive = save_case(guard.root, "positive", {"counter": 1}, record)
    if json.loads(positive.read_text()) != {"counter": 1}:
        raise ValueError("Independent positive control failed")
    directory = case_directory(guard.root, "stale")
    (directory / "target.json").write_bytes(old)
    (directory / "target.pending").write_bytes(b"retain-pending")
    guard.begin("stale", record)
    try:
        save_case(guard.root, "stale", {"counter": 1}, record)
    except StageFailure as error:
        if error.stage != "open_temp" or error.kind != "FileExistsError":
            raise ValueError("Existing-pending negative control failed") from None
    else:
        raise ValueError("Existing-pending refusal missing")
    if (directory / "target.json").read_bytes() != old or (
        directory / "target.pending"
    ).read_bytes() != b"retain-pending":
        raise ValueError("Existing-pending preservation mismatch")
    return {
        "status": "completed_synthetic_only_no_adoption",
        "attempts": guard.attempts,
        "baseline_successes": 128,
        "sharing_failure_stage": outcome.stage,
        "sharing_errno": outcome.errno,
        "sharing_winerror": outcome.winerror,
        "handle_closed": True,
        "independent_positive": True,
        "existing_pending_refused": True,
    }


def main() -> None:
    """Fixed-root one-shot CLI; retain only scalar terminal findings."""
    guard = Guard(RUN)
    guard.claim()
    try:
        with Journal(guard) as journal:
            result = execute_probe(guard, journal)
    except Exception as error:  # noqa: BLE001 -- terminal receipt without retry
        result = {
            "status": "stopped_no_retry",
            "attempts": guard.attempts,
            "exception": type(error).__name__,
            "stage": error.stage if isinstance(error, StageFailure) else None,
            "errno": getattr(error, "errno", None),
            "winerror": getattr(error, "winerror", None),
        }
    guard.check()
    with (RUN / "probe-result.json").open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    print(result["status"])
    if result["status"] != "completed_synthetic_only_no_adoption":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
