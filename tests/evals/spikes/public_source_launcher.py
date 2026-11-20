"""R1-L owned stdlib probe; no network, candidate libraries or private inputs."""

import ctypes as c
import hashlib
import json
import os
import struct
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
from embedding_budget import memory_snapshot
from public_source_accounting import Boundary, InjectedAccountingError, pair_complete

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "data/t17/public-review-launcher-01"
METER = RUN / "meter.json"
PYTHON = Path("F:/Python/Python314/python.exe")
D, Q, H = c.c_uint32, c.c_uint64, c.c_void_p


class Accounting(c.Structure):
    """Reviewed four LARGE_INTEGER and four DWORD accounting fields."""
    _fields_ = [("times", c.c_int64 * 4), ("faults", D), ("total", D),
                ("active", D), ("terminated", D)]


class Basic(c.Structure):
    """Reviewed x64 JOBOBJECT_BASIC_LIMIT_INFORMATION layout."""
    _fields_ = [("times", c.c_int64 * 2), ("flags", D), ("min_ws", c.c_size_t),
                ("max_ws", c.c_size_t), ("active", D), ("affinity", c.c_size_t),
                ("priority", D), ("scheduling", D)]


class Extended(c.Structure):
    """Basic limits, six IO counters and four pointer-sized memory fields."""
    _fields_ = [("basic", Basic), ("io", Q * 6), ("process_memory", c.c_size_t),
                ("job_memory", c.c_size_t), ("peak_process", c.c_size_t),
                ("peak_job", c.c_size_t)]


class Startup(c.Structure):
    """Reviewed STARTUPINFOW fields, without extended attributes."""
    _fields_ = [("cb", D), ("reserved", H), ("desktop", H), ("title", H),
                ("dimensions", D * 8), ("show", c.c_uint16), ("reserved2_size", c.c_uint16),
                ("reserved2", H), ("stdin", H), ("stdout", H), ("stderr", H)]


class Process(c.Structure):
    """Retain both handles returned by CreateProcessW through cleanup."""
    _fields_ = [("process", H), ("thread", H), ("pid", D), ("tid", D)]


class Port(c.Structure):
    """Reviewed completion key and completion-port handle."""
    _fields_ = [("key", H), ("port", H)]


def layouts() -> dict[str, int]:
    """Expose sizes for independent x64 declaration admission checks."""
    return {kind.__name__: c.sizeof(kind)
            for kind in (Accounting, Basic, Extended, Startup, Process, Port)}


def decode(raw: bytes) -> tuple[int, int]:
    """Decode reviewed field order independently of ctypes structure layout."""
    if len(raw) != 48:
        raise Boundary("Accounting length")
    values = struct.unpack("<4q4I", raw)
    return values[5], values[6]


class Stages:
    """Record mismatches before rejecting them, and forbid duplicate assignment."""
    order = ("baseline", "created", "assigned", "ready", "exited")

    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []

    def add(self, stage: str, raw: bytes, *, member: bool | None = None) -> None:
        """Require exactly the expected sequence and one successful worker."""
        total, active = decode(raw)
        index = len(self.records)
        self.records.append({"stage": stage, "raw_hex": raw.hex(), "total": total,
                             "active": active, "member": member, "tick": time.monotonic()})
        if index >= len(self.order) or self.order[index] != stage:
            raise Boundary("Stage/duplicate assignment")
        expected = (0, 0) if index < 2 else (1, 0 if stage == "exited" else 1)
        if (total, active) != expected:
            raise Boundary("Unexpected cumulative/active count")
        if (stage == "created" and member is not False
                or stage in {"assigned", "ready"} and member is not True):
            raise Boundary("Membership ambiguity")


def guard(elapsed: float, free: int, private: int) -> None:
    """Check normal-control deadline, headroom and controller private memory."""
    if not 0 <= elapsed <= 5 or free < 4294967296 or private > 536870912:
        raise Boundary("Time or memory boundary")


def notification_ok(events: list[dict[str, int]], pid: int) -> bool:
    """Require a notification for the retained PID, without assuming full delivery."""
    return any(e["key"] == 17 and e["value"] == pid for e in events)


def identity_ok(value: dict[str, Any], pid: int) -> bool:
    """A retained PID plus recorded image digest is required for identity evidence."""
    return value.get("pid") == pid and len(value.get("image_hash", "")) == 64


def write(path: Path, value: Any) -> None:
    """Atomically save capped receipts inside this fresh owned allocation."""
    data = json.dumps(value, indent=2).encode()
    size = sum(p.stat().st_size for p in RUN.iterdir() if p.is_file())
    if path.parent != RUN or size + len(data) > 2097152:
        raise Boundary("Receipt output boundary")
    pending = path.with_suffix(".tmp")
    pending.write_bytes(data)
    pending.replace(path)


def meter() -> dict[str, Any]:
    """Read authoritative package state; never reset its epoch or counters."""
    return json.loads(METER.read_text(encoding="utf-8-sig"))


def admission() -> None:
    """Persist admission before process creation, with complete source seals."""
    state = meter()
    tick = c.c_int64()
    c.windll.kernel32.QueryPerformanceCounter(c.byref(tick))
    if (state["status"] != "ready" or state["direct_workers"] >= 2
            or (tick.value - state["started_tick"]) / state["frequency"] > 1080):
        raise Boundary("Package admission boundary")
    for name, expected in state["seal"].items():
        if hashlib.sha256(Path(name).read_bytes()).hexdigest() != expected:
            raise Boundary("Source seal drift")
    state["direct_workers"] += 1
    write(METER, state)


def kernel() -> Any:
    """Declare reviewed Win32 signatures before any process creation."""
    k = c.WinDLL("kernel32", use_last_error=True)
    signatures = {
        "CreateJobObjectW": ([H, c.c_wchar_p], H),
        "CreateIoCompletionPort": ([H, H, c.c_size_t, D], H),
        "SetInformationJobObject": ([H, c.c_int, H, D], c.c_int),
        "QueryInformationJobObject": ([H, c.c_int, H, D, H], c.c_int),
        "CreateProcessW": ([c.c_wchar_p, c.c_wchar_p, H, H, c.c_int, D,
                            H, c.c_wchar_p, H, H], c.c_int),
        "AssignProcessToJobObject": ([H, H], c.c_int),
        "IsProcessInJob": ([H, H, H], c.c_int),
        "ResumeThread": ([H], D),
        "QueryFullProcessImageNameW": ([H, D, H, H], c.c_int),
        "GetQueuedCompletionStatus": ([H, H, H, H, D], c.c_int),
        "WaitForSingleObject": ([H, D], D),
        "GetExitCodeProcess": ([H, H], c.c_int),
        "TerminateJobObject": ([H, D], c.c_int),
        "TerminateProcess": ([H, D], c.c_int),
        "CloseHandle": ([H], c.c_int),
    }
    for name, (args, result) in signatures.items():
        function = getattr(k, name)
        function.argtypes, function.restype = args, result
    return k


def checked(value: Any) -> Any:
    """Reject a failed Windows BOOL/handle call while preserving its error code."""
    if not value:
        raise c.WinError(c.get_last_error())
    return value


def control(name: str, exit_code: int) -> dict[str, Any]:
    """Observe one suspended/assigned/resumed worker; stop on any ambiguity."""
    k = kernel()
    job = port = None
    process = Process()
    assigned = False
    stages = Stages()
    events: list[dict[str, int]] = []
    result: dict[str, Any] = {"name": name, "stages": stages.records, "events": events,
                              "control_error": None, "cleanup_error": None,
                              "close_returns": {}, "job_id": name}
    started = time.monotonic()
    minimum, peak = 2**63, 0

    def sample() -> None:
        nonlocal minimum, peak
        snapshot = memory_snapshot()
        minimum = min(minimum, snapshot["available_physical"])
        guard(time.monotonic() - started, minimum, snapshot["controller_private"])
        if job:
            value = Extended()
            checked(k.QueryInformationJobObject(job, 9, c.byref(value), c.sizeof(value), None))
            peak = max(peak, value.peak_job)

    def accounting() -> bytes:
        value, length = Accounting(), D()
        checked(k.QueryInformationJobObject(job, 1, c.byref(value), 48, c.byref(length)))
        raw = bytes(value)
        total, active = decode(raw)
        result["last_return_length"] = length.value
        result["kernel_total"], result["active_after_cleanup"] = total, active
        if length.value != 48 or (total, active) != (value.total, value.active):
            raise Boundary("Raw/typed layout disagreement")
        state = meter()
        counts = state.setdefault("job_counts", {})
        counts[name] = max(counts.get(name, 0), total)
        state["observed_job_processes"] = sum(counts.values())
        write(METER, state)
        if total > 2 or state["observed_job_processes"] > 4:
            raise Boundary("Diagnostic discovery allowance")
        return raw

    def member() -> bool:
        value = c.c_int()
        checked(k.IsProcessInJob(process.process, job, c.byref(value)))
        return bool(value.value)

    def notifications() -> None:
        for _ in range(32):
            message, key, value = D(), c.c_size_t(), H()
            ok = k.GetQueuedCompletionStatus(port, c.byref(message), c.byref(key),
                                             c.byref(value), 0)
            if not ok:
                if c.get_last_error() == 258 and value.value is None:
                    return
                raise c.WinError(c.get_last_error())
            events.append({"message": message.value, "key": key.value,
                           "value": value.value or 0})
        raise Boundary("Notification overflow")

    def snapshot(stage: str, membership: bool | None = None) -> None:
        raw = accounting()
        # Keep raw observations durable even when the stage validator rejects them.
        try:
            stages.add(stage, raw, member=membership)
        finally:
            write(RUN / (name + ".json"), result)

    try:
        sample()
        job = checked(k.CreateJobObjectW(None, None))
        limits = Extended()
        limits.basic.flags, limits.basic.active = 0x2308, 1
        limits.process_memory = limits.job_memory = 536870912
        checked(k.SetInformationJobObject(job, 9, c.byref(limits), c.sizeof(limits)))
        port = checked(k.CreateIoCompletionPort(H(-1), None, 0, 1))
        association = Port(17, port)
        checked(k.SetInformationJobObject(job, 7, c.byref(association), c.sizeof(association)))
        result["limits_set"], result["port_associated"] = True, True
        snapshot("baseline")
        ready, release = RUN / (name + ".ready"), RUN / (name + ".release")
        if ready.exists() or release.exists():
            raise Boundary("Existing handshake")
        code = ("import os,time; from pathlib import Path; "
                f"Path({str(ready)!r}).write_text(str(os.getpid())); "
                "start=time.monotonic(); "
                f"release=Path({str(release)!r})\n"
                "while not release.exists() and time.monotonic()-start<4: time.sleep(0.01)\n"
                f"raise SystemExit({exit_code} if release.exists() else 88)")
        args = [str(PYTHON), "-I", "-S", "-B", "-c", code]
        environment = "\0".join(f"{key}={os.environ[key]}" for key in
                                  ("SystemRoot", "WINDIR") if key in os.environ) + "\0\0"
        environment_buffer = c.create_unicode_buffer(environment)
        startup = Startup()
        startup.cb = c.sizeof(startup)
        admission()
        checked(k.CreateProcessW(str(PYTHON), c.create_unicode_buffer(subprocess.list2cmdline(args)),
                                  None, None, False, 0x08000404, environment_buffer,
                                  str(RUN), c.byref(startup), c.byref(process)))
        result["pid"] = process.pid
        snapshot("created", member())
        result["assign_return"] = checked(k.AssignProcessToJobObject(job, process.process))
        assigned = True
        snapshot("assigned", member())
        image, size = c.create_unicode_buffer(32768), D(32768)
        checked(k.QueryFullProcessImageNameW(process.process, 0, image, c.byref(size)))
        image_path = Path(image.value)
        result["image_name"] = image_path.name
        result["image_hash"] = hashlib.sha256(image_path.read_bytes()).hexdigest()
        if image_path.resolve() != PYTHON.resolve():
            raise Boundary("Image identity drift")
        result["resume_return"] = k.ResumeThread(process.thread)
        if result["resume_return"] != 1:
            raise Boundary("Resume return")
        while not ready.exists():
            sample()
            notifications()
            time.sleep(0.01)
        result["handshake_pid"] = int(ready.read_text())
        if result["handshake_pid"] != process.pid or not identity_ok(result, process.pid):
            raise Boundary("Ready PID/identity")
        snapshot("ready", member())
        pids = c.create_string_buffer(40)
        checked(k.QueryInformationJobObject(job, 3, pids, 40, None))
        assigned_count, listed = struct.unpack_from("<II", pids.raw)
        result["owned_pids"] = list(struct.unpack_from("<4Q", pids.raw, 8)[:listed])
        if assigned_count != 1 or listed != 1 or result["owned_pids"] != [process.pid]:
            raise Boundary("Owned PID list")
        notifications()
        if not notification_ok(events, process.pid):
            raise Boundary("Missing retained-PID notification")
        release.write_text("release", encoding="ascii")
        while k.WaitForSingleObject(process.process, 0) != 0:
            sample()
            notifications()
            time.sleep(0.01)
        status = D()
        checked(k.GetExitCodeProcess(process.process, c.byref(status)))
        result["worker_exit"] = status.value
        snapshot("exited")
    except Exception as error:  # noqa: BLE001 -- preserve failure then clean only owned resources
        result["control_error"] = type(error).__name__
        result["error_code"] = getattr(error, "winerror", None)
        result["error_message"] = str(error)[:200]
    finally:
        cleanup_started = time.monotonic()

        def attempt(label: str, action: Any) -> Any:
            try:
                value = action()
                result[label] = value
                return value
            except Exception as error:  # noqa: BLE001 -- independent cleanup attempts
                result[label + "_error"] = type(error).__name__
                return None

        if process.process:
            if k.WaitForSingleObject(process.process, 0) != 0:
                attempt("terminate_return", lambda: checked(
                    k.TerminateJobObject(job, 1) if assigned else
                    k.TerminateProcess(process.process, 1)))
            attempt("wait_return", lambda: k.WaitForSingleObject(process.process, 4000))
            result["child_reaped"] = result.get("wait_return") == 0
        if job:
            attempt("final_accounting_hex", lambda: accounting().hex())
        if port:
            attempt("notifications_drained", lambda: notifications() is None)
        for label, handle in (("thread", process.thread), ("process", process.process),
                              ("job", job), ("port", port)):
            if handle:
                result["close_returns"][label] = attempt(
                    "close_" + label, lambda h=handle: bool(checked(k.CloseHandle(h))))
        result["handle_close_succeeded"] = (set(result["close_returns"]) ==
                                              {"thread", "process", "job", "port"}
                                              and all(result["close_returns"].values()))
        if name == "forced-failure":
            try:
                raise InjectedAccountingError("approved callback failure control")
            except InjectedAccountingError as error:
                result["cleanup_error"] = type(error).__name__
        result.update(elapsed_seconds=time.monotonic() - started,
                      cleanup_seconds=time.monotonic() - cleanup_started,
                      min_available=minimum, job_peak=peak)
        write(RUN / (name + ".json"), result)
    return result


def run() -> None:
    """Admit a single sealed pair, stopping before the second on first ambiguity."""
    if layouts() != {"Accounting": 48, "Basic": 64, "Extended": 144,
                      "Startup": 104, "Process": 24, "Port": 16}:
        raise Boundary("Unverified x64 declarations")
    state = meter()
    if state["status"] != "ready" or state["direct_workers"] or (RUN / "pair.json").exists():
        raise Boundary("Never retry an admitted pair")
    results = []
    started = time.monotonic()
    for name, code in (("success", 0), ("forced-failure", 7)):
        value = control(name, code)
        results.append(value)
        from public_source_accounting import verdict
        if not verdict(value, name)["passed"] or value["cleanup_seconds"] > 5:
            break
    complete = pair_complete(results) and time.monotonic() - started <= 20
    write(RUN / "pair.json", {"status": "completed_pending_review" if complete else
                              "stopped_no_retry", "controls": results})
    state = meter()
    state["status"] = "controls_completed" if complete else "stopped_no_retry"
    write(METER, state)
    print(json.dumps({"complete": complete, "controls": len(results),
                      "direct_workers": state["direct_workers"],
                      "observed_job_processes": state["observed_job_processes"]}))


if __name__ == "__main__":
    if sys.argv[1:] != ["run"]:
        raise SystemExit("Only the separately approved sealed R1-L pair may run")
    run()
