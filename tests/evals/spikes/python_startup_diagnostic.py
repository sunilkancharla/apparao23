"""Approved, fixed startup contrasts; no AppContainer or OCR execution."""

from __future__ import annotations

import ctypes
import hashlib
import json
import os
import subprocess
import time
from ctypes import wintypes as w
from datetime import UTC, datetime
from pathlib import Path

from appcontainer_preflight import (
    BASE,
    ROOT,
    STAGE,
    Native,
    ProcessInfo,
    Startup,
    StartupEx,
    contained,
    memory_ready,
)

RUN = ROOT / "data/t09-startup-diagnostic/diagnostic-01"
OLD_RUN = ROOT / "data/t09-appcontainer/preflight-01"
PROBE = '''import json, sys
from pathlib import Path
Path(sys.argv[1]).write_text(json.dumps({"marker": "T09-startup",
    "version": list(sys.version_info[:3]), "prefix": sys.prefix,
    "executable": sys.executable}), encoding="utf-8")
'''


def schedule() -> list[tuple[str, str]]:
    """Return exactly eight predeclared trials, with no retry schedule."""
    return [(row, source) for row in "ABCD" for source in ("original", "staged")]


def environment(row: str, interpreter: Path, work: Path, windows: str) -> dict[str, str]:
    """Build a fresh non-secret allowlist instead of inheriting host variables."""
    if row not in "ABCD" or len(row) != 1:
        raise ValueError("Unknown diagnostic row")
    values = {"SystemRoot": windows, "WINDIR": windows,
              "TEMP": str(work), "TMP": str(work)}
    if row == "D":
        values["PATH"] = str(interpreter) + ";" + str(Path(windows) / "System32")
        values["COMSPEC"] = str(Path(windows) / "System32/cmd.exe")
    return values


def command(executable: Path, probe: Path, output: Path) -> str:
    """Encode fixed arguments using Windows command-line quoting."""
    return subprocess.list2cmdline([str(executable), "-I", "-S", "-B",
                                   str(probe), str(output)])


def classify(exit_code: int, marker: dict | None, executable: Path) -> str:
    """Separate exit observations from a verified marker and interpreter identity."""
    if exit_code:
        return f"startup_exit_{exit_code:08x}"
    if (not marker or marker.get("marker") != "T09-startup"
            or marker.get("version") != [3, 14, 6]
            or Path(marker.get("executable", "")) != executable):
        return "missing_or_invalid_marker"
    return "started"


def verify_bytes(content: bytes, size: int, digest: str) -> None:
    """Stop on identity drift; never repair or replace a runtime file."""
    if len(content) != size or hashlib.sha256(content).hexdigest() != digest:
        raise RuntimeError("Runtime identity drift")


def charged_call(charge, create):
    """A failed reservation must prevent the native creation attempt."""
    charge()
    return create()


def safe_output(root: Path, output: Path) -> Path:
    """Use the shared lexical/reparse/resolution guard for synthetic outputs."""
    return contained(root, output)


def owned_handles(process, thread) -> bool:
    """Only successfully returned process/thread pairs denote an owned child."""
    return bool(process and thread)


def record_completed_case(result: dict) -> dict:
    """Preserve observed PID/exit/accounting before enforcing the unchanged guard."""
    write_receipt(f"case-{result['row']}-{result['source']}.json", result)
    accounting = result["accounting"]
    if accounting["total"] != 1 or accounting["active"] != 0:
        raise RuntimeError("Unexpected descendant or active worker")
    return result


def write_receipt(name: str, value: object) -> None:
    """Write bounded sanitized evidence only within the new run."""
    content = json.dumps(value, indent=2).encode()
    if len(content) > 1024**2:
        raise RuntimeError("Single receipt exceeds output budget")
    safe_output(RUN, RUN / name).write_bytes(content)


def reserve(purpose: str) -> None:
    """Persist the shared charge before attempting a trial process."""
    meter = json.loads((RUN / "meter.json").read_text(encoding="utf-8-sig"))
    if meter["reserved"] + 1 > meter["limit"] - 8:
        raise RuntimeError("Diagnostic budget/cleanup reserve exhausted")
    if datetime.now(UTC) > datetime.fromisoformat(meter["execution_deadline_utc"]):
        raise RuntimeError("Diagnostic execution deadline exhausted")
    event = {"purpose": purpose, "slots": 1, "at": datetime.now(UTC).isoformat()}
    meter["reserved"] += 1
    meter["events"].append(event)
    write_receipt("meter.json", meter)
    with (RUN / "events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event) + "\n")


def verify_runtime() -> dict:
    """Rehash all previously staged entries and their exact original counterparts."""
    manifest_path = OLD_RUN / "runtime-manifest.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    if len(manifest) != 810 or len({item["path"] for item in manifest}) != 810:
        raise RuntimeError("Unexpected manifest identity/count")
    total = 0
    for entry in manifest:
        for root in (BASE, STAGE / "runtime"):
            path = contained(root, root / entry["path"])
            verify_bytes(path.read_bytes(), entry["bytes"], entry["sha256"])
        total += entry["bytes"]
    config = (ROOT / ".venv/pyvenv.cfg").read_bytes()
    if (b"home = F:\\Python\\Python314" not in config
            or b"version = 3.14.6" not in config
            or b"include-system-site-packages = false" not in config):
        raise RuntimeError("Unexpected virtual environment configuration")
    result = {"files": len(manifest), "bytes": total,
              "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
              "config_sha256": hashlib.sha256(config).hexdigest(),
              "helper_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "prior_helper_sha256": hashlib.sha256(
                  Path(__file__).with_name("appcontainer_preflight.py").read_bytes()).hexdigest(),
              "old_meter_sha256": hashlib.sha256((OLD_RUN / "meter.json").read_bytes()).hexdigest()}
    write_receipt("identities.json", result)
    return result


def output_limits() -> None:
    """Observe both total disk/output limits on every worker poll."""
    total = 0
    for path in RUN.rglob("*"):
        contained(RUN, path)
        if path.is_file():
            total += path.stat().st_size
    if total > 1024**2:
        raise RuntimeError("Aggregate diagnostic output exceeds 1 MiB")


def trial(native: Native, row: str, source: str, probe: Path) -> dict:
    """Create exactly one suspended direct child and verify Job membership first."""
    if (row, source) not in schedule():
        raise ValueError("Unlisted trial")
    memory_ready()
    executable = (BASE if source == "original" else STAGE / "runtime") / "python.exe"
    output = safe_output(RUN, RUN / "outputs" / f"{row}-{source}.json")
    if output.exists():
        raise RuntimeError("Result collision; no retries")
    values = environment(row, executable.parent, RUN / "work", os.environ["SystemRoot"])
    block = ctypes.create_unicode_buffer("\0".join(
        f"{key}={value}" for key, value in sorted(values.items())) + "\0\0")
    startup = StartupEx()
    startup.startup.cb = ctypes.sizeof(StartupEx if row in "BC" else Startup)
    flags = 0x4 | 0x400  # suspended + Unicode environment for all rows
    attributes = None
    process = ProcessInfo()
    job = native.job(1)
    child_policy = w.DWORD(1)
    started = time.monotonic()
    try:
        if row in "BC":
            flags |= 0x80000 | 0x8000000
            size = ctypes.c_size_t()
            native.kernel.InitializeProcThreadAttributeList(None, 1, 0, ctypes.byref(size))
            attributes = ctypes.create_string_buffer(size.value)
            native.check(native.kernel.InitializeProcThreadAttributeList(
                attributes, 1, 0, ctypes.byref(size)))
            startup.attributes = ctypes.cast(attributes, ctypes.c_void_p)
            if row == "C":
                native.check(native.kernel.UpdateProcThreadAttribute(
                    attributes, 0, 0x2000E, ctypes.byref(child_policy),
                    ctypes.sizeof(child_policy), None, None))
        charged_call(lambda: reserve(f"trial {row}-{source}"), lambda: native.check(
            native.kernel.CreateProcessW(
                str(executable), ctypes.create_unicode_buffer(command(executable, probe, output)),
                None, None, False, flags, block, str(RUN / "work"),
                ctypes.byref(startup), ctypes.byref(process))))
        native.check(native.kernel.AssignProcessToJobObject(job, process.process))
        inside = w.BOOL()
        native.check(native.kernel.IsProcessInJob(process.process, job, ctypes.byref(inside)))
        if not inside.value or native.accounting(job)["total"] != 1:
            raise RuntimeError("Trial Job membership/accounting failure")
        if native.kernel.ResumeThread(process.thread) == 0xFFFFFFFF:
            raise ctypes.WinError(ctypes.get_last_error())
        while True:
            status = native.kernel.WaitForSingleObject(process.process, 100)
            if status == 0:
                break
            if status != 258:
                raise ctypes.WinError(ctypes.get_last_error())
            output_limits()
            if time.monotonic() - started >= 10:
                raise RuntimeError("Trial timeout; stop schedule")
        code = w.DWORD()
        native.check(native.kernel.GetExitCodeProcess(process.process, ctypes.byref(code)))
        accounting = native.accounting(job)
        result = {"row": row, "source": source, "pid": process.pid,
                  "flags": f"0x{flags:08x}", "environment": values,
                  "exit_code": code.value, "exit_hex": f"0x{code.value:08x}",
                  "duration_seconds": time.monotonic() - started,
                  "classification": "not_yet_validated",
                  "marker": None, "accounting": accounting, "timed_out": False}
        record_completed_case(result)
        output_limits()
        marker = json.loads(output.read_text()) if output.exists() else None
        result.update(classification=classify(code.value, marker, executable), marker=marker)
        write_receipt(f"case-{row}-{source}.json", result)
        return result
    finally:
        if owned_handles(process.process, process.thread):
            native.kernel.TerminateProcess(process.process, 125)
            if native.kernel.WaitForSingleObject(process.process, 5000) != 0:
                raise RuntimeError("Owned worker cleanup failed")
        for handle in (process.thread, process.process, job):
            if handle:
                native.kernel.CloseHandle(handle)
        if attributes is not None:
            native.kernel.DeleteProcThreadAttributeList(attributes)


def execute(controller_job) -> None:
    """Run one fixed diagnostic schedule; preserve partial evidence on safety stop."""
    meter = json.loads((RUN / "meter.json").read_text(encoding="utf-8-sig"))
    if datetime.now(UTC) > datetime.fromisoformat(meter["deadline_utc"]):
        raise RuntimeError("Preparation deadline exhausted")
    meter["execution_deadline_utc"] = datetime.fromtimestamp(time.time() + 600, UTC).isoformat()
    write_receipt("meter.json", meter)
    native = Native()
    result = {"status": "in_progress", "cases": []}
    identities = None
    try:
        identities = verify_runtime()
        for name in ("inputs", "outputs", "work"):
            safe_output(RUN, RUN / name).mkdir(exist_ok=False)
        probe = RUN / "inputs/probe.py"
        probe.write_text(PROBE, encoding="utf-8")
        for row, source in schedule():
            result["cases"].append(trial(native, row, source, probe))
            write_receipt("result.json", result)
        result["status"] = "eight_cases_complete_no_isolation_claim"
    except (OSError, RuntimeError, ValueError) as error:
        result["status"] = "safety_stop"
        result["error"] = f"{type(error).__name__}: {error}"
    finally:
        if identities and hashlib.sha256((OLD_RUN / "meter.json").read_bytes()).hexdigest() != identities["old_meter_sha256"]:
            result["status"] = "safety_stop"
            result["error"] = "Old meter changed"
        result["controller_accounting"] = native.accounting(controller_job)
        expected = len(result["cases"]) + 1
        if result["status"].startswith("eight") and result["controller_accounting"] != {
            "total": expected, "active": 1, "terminated": 0
        }:
            result["status"] = "safety_stop"
            result["error"] = "Unexpected combined controller accounting"
        write_receipt("result.json", result)
        print(json.dumps(result, indent=2))
    if result["status"] == "safety_stop":
        raise RuntimeError("Diagnostic stopped; see preserved result; no retry")
