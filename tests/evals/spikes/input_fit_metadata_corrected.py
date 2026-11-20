"""IF-K one-shot metadata reader with API-specific timestamp mutation checks."""

import hashlib
import json
import os
import sys
import time
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

REPO = Path(__file__).absolute().parents[3]
RUN = REPO / "data/t17/input-fit-corrected-01"
ROOT = REPO / "data/ollama/models"
FIELDS = (
    "st_dev",
    "st_ino",
    "st_size",
    "st_mtime_ns",
    "st_ctime_ns",
    "st_mode",
    "st_nlink",
)
CROSS_FIELDS = tuple(name for name in FIELDS if name != "st_ctime_ns")
SAME_FIELDS = FIELDS


class Boundary(RuntimeError):
    """Carry an explicit content-free refusal code."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def load_base() -> ModuleType:
    """Reuse only exact verified authored bytes; never dispatch old main code."""
    source = Path(__file__).with_name("input_fit_metadata.py")
    with source.open("rb") as stream:
        raw = stream.read(32769)
    if (
        len(raw) > 32768
        or hashlib.sha256(raw).hexdigest()
        != "2d47b7c816dba4092c755a4787fee6f394e4bd628a9d77f4829b3da98ed04204"
    ):
        raise Boundary("SOURCE_CHANGED")
    module = ModuleType("verified_metadata_helpers")
    module.__file__ = str(source)
    exec(compile(raw, str(source), "exec"), module.__dict__)  # noqa: S102 -- exact pinned authored source
    return module


BASE = load_base()


def snapshot(info: os.stat_result) -> dict[str, int]:
    """Require meaningful identity and preserve each named stat field."""
    values = {name: getattr(info, name, None) for name in FIELDS}
    if any(type(value) is not int for value in values.values()):
        raise Boundary("IDENTITY_INVALID")
    if (
        values["st_dev"] <= 0
        or values["st_ino"] <= 0
        or values["st_size"] < 0
        or values["st_nlink"] <= 0
    ):
        raise Boundary("IDENTITY_INVALID")
    BASE.check_type(info, False)
    return values


def compare(left: dict, right: dict, fields: tuple, code: str, record: dict) -> None:
    """Retain named differences before refusing a required comparison."""
    differences = [name for name in fields if left[name] != right[name]]
    record["differences"][code] = differences
    if differences:
        raise Boundary(code)


def read_one(root: Path, item: tuple, state: dict, save: Callable) -> bytes:
    """Read pinned metadata once while comparing timestamps only within each API."""
    role, relative, size, digest = item
    record = {"role": role, "status": "started", "observations": {}, "differences": {}}
    state["files"].append(record)
    save(state)
    phase = "INPUT_CAP"
    try:
        if not 0 <= size <= 65536 or state["charged_bytes"] + 65537 > 1048576:
            raise Boundary("INPUT_CAP")
        path = root / relative
        phase = "PATH_REFUSED"
        before = BASE.checked_file(root, path)
        before_values = snapshot(before)
        record["observations"]["path_before"] = before_values
        if before.st_size != size:
            raise Boundary("SIZE_DIGEST_MISMATCH")
        state["charged_bytes"] += 65537
        save(state)
        phase = "READ_FAILED"
        with path.open("rb") as stream:
            handle_before = snapshot(os.fstat(stream.fileno()))
            record["observations"]["handle_before"] = handle_before
            record["cross_api_ctime_differs"] = (
                before_values["st_ctime_ns"] != handle_before["st_ctime_ns"]
            )
            compare(
                before_values,
                handle_before,
                CROSS_FIELDS,
                "OPEN_IDENTITY_MISMATCH",
                record,
            )
            # Persist exact open observations before a potentially failing read.
            save(state)
            raw = stream.read(65537)
            state["read_bytes"] += len(raw)
            handle_after = snapshot(os.fstat(stream.fileno()))
            record["observations"]["handle_after"] = handle_after
        phase = "PATH_REFUSED"
        after_values = snapshot(BASE.checked_file(root, path))
        record["observations"]["path_after"] = after_values
        compare(handle_before, handle_after, SAME_FIELDS, "HANDLE_MUTATED", record)
        compare(before_values, after_values, SAME_FIELDS, "PATH_MUTATED", record)
        compare(
            after_values, handle_after, CROSS_FIELDS, "FINAL_IDENTITY_MISMATCH", record
        )
        actual = hashlib.sha256(raw).hexdigest()
        record.update(length=len(raw), sha256=actual)
        if len(raw) != size or len(raw) > 65536 or actual != digest:
            raise Boundary("SIZE_DIGEST_MISMATCH")
        record["status"] = "completed"
        save(state)
        return raw
    except Exception as error:
        record.update(
            status="refused",
            error=type(error).__name__,
            code=getattr(error, "code", phase),
        )
        save(state)
        raise


def admit(root: Path, meter: dict, claim: bytes, now: float, output_bytes: int) -> None:
    """Reject old roots, missing/closed attempts or exhausted launch allowances."""
    try:
        elapsed = now - meter["started_qpc"] / meter["frequency"]
        valid = meter["status"] == "active" and meter["worker_attempts"] == 1
    except (KeyError, TypeError, ZeroDivisionError):
        raise Boundary("ALLOCATION_INVALID") from None
    if (
        root != RUN
        or not valid
        or claim != b"IF-K"
        or not 0 <= elapsed < 1140
        or not 0 <= output_bytes < 1966080
    ):
        raise Boundary("ADMISSION_REFUSED")


def worker() -> None:
    """Consume the fresh worker claim and read only the nine fixed public files."""
    meter = json.loads((RUN / "meter.json").read_text(encoding="utf-8-sig"))
    with (RUN / "controller.claim").open("rb") as stream:
        claim = stream.read(16)
    output_bytes = sum(path.stat().st_size for path in RUN.iterdir() if path.is_file())
    admit(RUN, meter, claim, time.perf_counter(), output_bytes)
    with (RUN / "worker.claim").open("xb") as stream:
        stream.write(b"one worker only")
        stream.flush()
        os.fsync(stream.fileno())
    state = {"charged_bytes": 0, "read_bytes": 0, "files": []}
    findings = {}
    for item in BASE.INVENTORY:
        raw = read_one(
            ROOT, item, state, lambda value: BASE.persist(RUN / "progress.json", value)
        )
        findings[item[0]] = raw.decode("utf-8")
    BASE.persist(RUN / "findings.json", findings)
    print('{"status":"complete","files":9}', flush=True)


if __name__ == "__main__":
    try:
        if sys.argv[1:] != ["worker"]:
            raise Boundary("DISPATCH_REFUSED")
        worker()
    except (OSError, ValueError, RuntimeError) as error:
        print(
            json.dumps(
                {
                    "status": "stopped_no_retry",
                    "error": type(error).__name__,
                    "code": getattr(error, "code", "OPERATION_FAILED"),
                }
            ),
            flush=True,
        )
        sys.exit(1)
