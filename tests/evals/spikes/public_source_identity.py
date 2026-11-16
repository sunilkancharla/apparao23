"""R1-I single owned probe: read back limits, capture identities, then reject counts."""

import ctypes as c
import hashlib
import json
import os
import struct
import subprocess
import sys
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
import public_source_launcher as prior
from public_source_accounting import Boundary

RUN = prior.ROOT / "data/t17/public-review-identity-01"
METER = RUN / "meter.json"


class FileTime(c.Structure):
    """Reviewed two-DWORD FILETIME, without an unaligned integer pointer cast."""
    _fields_ = [("low", prior.D), ("high", prior.D)]


def limit_verdict(raw: bytes) -> dict[str, Any]:
    """Independently decode required fields from the reviewed x64 layout."""
    if len(raw) != 144:
        return {"passed": False, "length": len(raw)}
    flags = struct.unpack_from("<I", raw, 16)[0]
    active = struct.unpack_from("<I", raw, 40)[0]
    process_memory, job_memory = struct.unpack_from("<QQ", raw, 112)
    return {"flags": flags, "active_limit": active, "process_memory": process_memory,
            "job_memory": job_memory, "passed": flags & 0x2308 == 0x2308
            and flags & 0x1800 == 0 and active == 1
            and process_memory == job_memory == 536870912}


def observe_ready(total: int, active: int, capture: Callable[[], Any]) -> dict[str, Any]:
    """Permit only the approved diagnostic ceiling, capture before count rejection."""
    if total not in (1, 2) or not 0 < active <= 2:
        raise Boundary("Diagnostic ceiling/empty ready stage")
    identities = capture()
    return {"identities": identities, "count_ok": total == active == 1}


def capture_guard(now: float, started: float, deadline: float) -> None:
    """The capture window consumes, rather than extends, the normal allowance."""
    if now - started > 0.25 or now > deadline:
        raise Boundary("Capture/control deadline")


def pid_list(raw: bytes) -> list[int]:
    """Decode a bounded complete list; reject truncation, duplicates or null IDs."""
    if len(raw) != 40:
        raise Boundary("PID buffer length")
    assigned, listed = struct.unpack_from("<II", raw)
    values = list(struct.unpack_from("<4Q", raw, 8)[:listed])
    if not 1 <= assigned == listed <= 2 or len(set(values)) != listed or 0 in values:
        raise Boundary("PID list incomplete/ambiguous")
    return values


def owned_identity(handle: Any, pid: int, member: Callable[[Any], bool],
                   image: Callable[[Any], str], creation: Callable[[Any], int]
                   ) -> dict[str, Any]:
    """Never query image/creation identity before verified membership on that handle."""
    if not member(handle):
        raise Boundary("Unverified handle ownership")
    created = creation(handle)
    name = Path(image(handle)).name
    if not name or type(created) is not int or created <= 0:
        raise Boundary("Incomplete executable/creation identity")
    return {"pid": pid, "owned_member": True, "creation_id": created,
            "image_name": name, "observed_at": time.monotonic()}


class Deadline:
    """Independent timer invokes only the supplied owned termination callback."""

    def __init__(self, terminate: Callable[[], None], seconds: float):
        self.terminate = terminate
        self.seconds = seconds
        self.fired = self.cancelled = False
        self.error: str | None = None
        self.timer: threading.Timer | None = None

    def fire(self) -> None:
        """Do not write the single-writer ledger from this timer thread."""
        if self.cancelled:
            return
        self.fired = True
        try:
            self.terminate()
        except Exception as error:  # noqa: BLE001 -- callback failure belongs in receipt
            self.error = type(error).__name__

    def start(self) -> None:
        """Start a daemon timer; no process or service is created."""
        self.timer = threading.Timer(max(0, self.seconds), self.fire)
        self.timer.daemon = True
        self.timer.start()

    def close(self) -> None:
        """Quiesce callback before native handles can be closed."""
        self.cancelled = True
        if self.timer:
            self.timer.cancel()
            self.timer.join(timeout=1)
            if self.timer.is_alive():
                raise Boundary("Deadline callback not quiescent")


def read() -> dict[str, Any]:
    """Read durable allocation state without changing a closed epoch."""
    return json.loads(METER.read_text(encoding="utf-8-sig"))


def save(path: Path, value: Any) -> None:
    """Save bounded owned receipts atomically; propagate persistence failures."""
    data = json.dumps(value, indent=2).encode()
    if path.parent != RUN or sum(p.stat().st_size for p in RUN.iterdir()
                                 if p.is_file()) + len(data) > 2097152:
        raise Boundary("Output boundary")
    pending = path.with_suffix(".tmp")
    pending.write_bytes(data)
    pending.replace(path)


def accepted(value: dict[str, Any]) -> bool:
    """Evidence collection alone must not count as operational success."""
    return (not value["control_error"] and value.get("worker_exit") == 0
            and all(value["verdicts"].values()) and not value["watchdog"]["fired"]
            and value["normal_seconds"] <= 5 and value["cleanup_seconds"] <= 5
            and value.get("capture_seconds", 1) <= 0.25)


def run() -> None:
    """One sealed diagnostic attempt; no second worker or automatic retry."""
    state = read()
    tick = c.c_int64()
    c.windll.kernel32.QueryPerformanceCounter(c.byref(tick))
    if (state["status"] != "ready" or state["direct_attempts"]
            or (RUN / "receipt.json").exists()
            or (tick.value - state["started_tick"]) / state["frequency"] > 900):
        raise Boundary("Closed/repeated/expired admission")
    for name, digest in state["seal"].items():
        if hashlib.sha256(Path(name).read_bytes()).hexdigest() != digest:
            raise Boundary("Seal drift")
    if (prior.layouts() != {"Accounting": 48, "Basic": 64, "Extended": 144,
                            "Startup": 104, "Process": 24, "Port": 16}
            or c.sizeof(FileTime) != 8):
        raise Boundary("Unverified declarations")
    state["status"] = "running"
    save(METER, state)
    k = prior.kernel()
    k.OpenProcess.argtypes, k.OpenProcess.restype = [prior.D, c.c_int, prior.D], prior.H
    k.GetProcessTimes.argtypes = [prior.H] * 5
    k.GetProcessTimes.restype = c.c_int
    job = port = None
    process = prior.Process()
    assigned = False
    extra_handles: list[Any] = []
    result: dict[str, Any] = {"stages": [], "limits": [], "identities": [],
                              "close_returns": {}, "control_error": None, "notifications": []}
    started = time.monotonic()
    minimum, peak = 2**63, 0

    def terminate_owned() -> None:
        if process.process and not assigned:
            prior.checked(k.TerminateProcess(process.process, 1))
        elif job:
            prior.checked(k.TerminateJobObject(job, 1))

    watchdog = Deadline(terminate_owned, 5)

    def sample() -> None:
        nonlocal minimum, peak
        memory = prior.memory_snapshot()
        minimum = min(minimum, memory["available_physical"])
        prior.guard(time.monotonic() - started, minimum, memory["controller_private"])
        if watchdog.fired:
            raise Boundary("Independent deadline fired")

    def limits(stage: str) -> None:
        nonlocal peak
        value, size = prior.Extended(), prior.D()
        prior.checked(k.QueryInformationJobObject(job, 9, c.byref(value), 144, c.byref(size)))
        raw = bytes(value)
        verdict = limit_verdict(raw)
        peak = max(peak, value.peak_job)
        record = {"stage": stage, "raw_hex": raw.hex(), "returned": size.value,
                  "verdict": verdict, "tick": time.monotonic()}
        result["limits"].append(record)
        save(RUN / "receipt.json", result)
        if size.value != 144 or not verdict["passed"]:
            raise Boundary("Effective limit readback mismatch")

    def accounting(stage: str) -> tuple[int, int]:
        value, size = prior.Accounting(), prior.D()
        prior.checked(k.QueryInformationJobObject(job, 1, c.byref(value), 48, c.byref(size)))
        raw = bytes(value)
        total, active = prior.decode(raw)
        result["stages"].append({"stage": stage, "raw_hex": raw.hex(), "total": total,
                                  "active": active, "returned": size.value,
                                  "tick": time.monotonic()})
        current = read()
        current["observed_associations"] = max(current["observed_associations"], total)
        save(METER, current)
        save(RUN / "receipt.json", result)
        if size.value != 48 or (total, active) != (value.total, value.active):
            raise Boundary("Accounting decode")
        if total > 2 or active > 2:
            raise Boundary("Diagnostic ceiling exceeded")
        return total, active

    def member(handle: Any) -> bool:
        value = c.c_int()
        prior.checked(k.IsProcessInJob(handle, job, c.byref(value)))
        return bool(value.value)

    def notifications() -> None:
        for _ in range(32):
            message, key, value = prior.D(), c.c_size_t(), prior.H()
            if not k.GetQueuedCompletionStatus(port, c.byref(message), c.byref(key),
                                                c.byref(value), 0):
                if c.get_last_error() == 258 and value.value is None:
                    return
                raise c.WinError(c.get_last_error())
            result["notifications"].append({"message": message.value, "key": key.value,
                                             "value": value.value or 0})
        raise Boundary("Notification capacity")

    def image(handle: Any) -> str:
        value, size = c.create_unicode_buffer(32768), prior.D(32768)
        prior.checked(k.QueryFullProcessImageNameW(handle, 0, value, c.byref(size)))
        return value.value

    def creation(handle: Any) -> int:
        values = [FileTime() for _ in range(4)]
        prior.checked(k.GetProcessTimes(handle, *(c.byref(v) for v in values)))
        return values[0].low | (values[0].high << 32)

    def capture() -> list[dict[str, Any]]:
        capture_started = time.monotonic()
        raw = c.create_string_buffer(40)
        prior.checked(k.QueryInformationJobObject(job, 3, raw, 40, None))
        pids = pid_list(raw.raw)
        if process.pid not in pids:
            raise Boundary("Direct PID absent from owned list")
        result["listed_count"] = len(pids)
        try:
            for pid in pids:
                capture_guard(time.monotonic(), capture_started, started + 5)
                handle = process.process
                if pid != process.pid:
                    handle = prior.checked(k.OpenProcess(0x1000, False, pid))
                    extra_handles.append(handle)
                # No image/creation query unless same retained handle belongs to this job.
                result["identities"].append(owned_identity(handle, pid, member, image, creation))
                capture_guard(time.monotonic(), capture_started, started + 5)
        finally:
            result["capture_seconds"] = time.monotonic() - capture_started
            save(RUN / "receipt.json", result)
        return result["identities"]

    try:
        sample()
        job = prior.checked(k.CreateJobObjectW(None, None))
        requested = prior.Extended()
        requested.basic.flags, requested.basic.active = 0x2308, 1
        requested.process_memory = requested.job_memory = 536870912
        prior.checked(k.SetInformationJobObject(job, 9, c.byref(requested), 144))
        port = prior.checked(k.CreateIoCompletionPort(prior.H(-1), None, 0, 1))
        association = prior.Port(17, port)
        prior.checked(k.SetInformationJobObject(job, 7, c.byref(association), c.sizeof(association)))
        limits("before_create")
        if accounting("baseline") != (0, 0):
            raise Boundary("Nonempty owned job")
        ready, release = RUN / "worker.ready", RUN / "worker.release"
        if ready.exists() or release.exists():
            raise Boundary("Existing handshake")
        code = ("import os,time;from pathlib import Path;"
                f"Path({str(ready)!r}).write_text(str(os.getpid()));"
                f"release=Path({str(release)!r});start=time.monotonic()\n"
                "while not release.exists() and time.monotonic()-start<4:time.sleep(.01)\n"
                "raise SystemExit(0 if release.exists() else 88)")
        args = [str(prior.PYTHON), "-I", "-S", "-B", "-c", code]
        environment = "\0".join(f"{key}={os.environ[key]}" for key in
                                  ("SystemRoot", "WINDIR") if key in os.environ) + "\0\0"
        startup = prior.Startup()
        startup.cb = c.sizeof(startup)
        current = read()
        current["direct_attempts"] = 1
        save(METER, current)
        watchdog.seconds = max(0, 5 - (time.monotonic() - started))
        watchdog.start()
        prior.checked(k.CreateProcessW(str(prior.PYTHON), c.create_unicode_buffer(
            subprocess.list2cmdline(args)), None, None, False, 0x08000404,
            c.create_unicode_buffer(environment), str(RUN), c.byref(startup), c.byref(process)))
        sample()
        result["direct_pid"] = process.pid
        if accounting("created") != (0, 0) or member(process.process):
            raise Boundary("Pre-assignment mismatch")
        prior.checked(k.AssignProcessToJobObject(job, process.process))
        assigned = True
        limits("after_assignment")
        if accounting("assigned") != (1, 1) or not member(process.process):
            raise Boundary("Assignment mismatch")
        if k.ResumeThread(process.thread) != 1:
            raise Boundary("Resume mismatch")
        while not ready.exists():
            sample()
            notifications()
            time.sleep(0.01)
        if int(ready.read_text()) != process.pid:
            raise Boundary("Handshake PID mismatch")
        sample()
        total, active = accounting("ready")
        limits("ready")
        result["observation"] = observe_ready(total, active, capture)
        notifications()
        save(RUN / "receipt.json", result)
        if not result["observation"]["count_ok"]:
            raise Boundary("Count mismatch after approved identity capture")
        release.write_text("release", encoding="ascii")
        while k.WaitForSingleObject(process.process, 0) != 0:
            sample()
            time.sleep(0.01)
        exit_code = prior.D()
        prior.checked(k.GetExitCodeProcess(process.process, c.byref(exit_code)))
        result["worker_exit"] = exit_code.value
    except Exception as error:  # noqa: BLE001 -- preserve failure and clean only owned objects
        result["control_error"] = type(error).__name__
        result["error_code"] = getattr(error, "winerror", None)
        result["reason"] = (str(error)[:160] if isinstance(error, Boundary) else "OS query failed")
    finally:
        cleanup_started = time.monotonic()
        result["normal_seconds"] = cleanup_started - started

        def attempt(label: str, action: Callable[[], Any]) -> Any:
            try:
                value = action()
                result[label] = value
                return value
            except Exception as error:  # noqa: BLE001 -- independent cleanup and receipt paths
                result[label + "_error"] = type(error).__name__
                return None

        attempt("watchdog_quiescent", lambda: watchdog.close() is None)
        result["watchdog"] = {"fired": watchdog.fired, "error": watchdog.error}
        if process.process:
            if k.WaitForSingleObject(process.process, 0) != 0:
                attempt("termination_return", lambda: terminate_owned() is None)
            result["direct_reaped"] = attempt(
                "wait_return", lambda: k.WaitForSingleObject(process.process, 3500)) == 0
        if job:
            attempt("final_accounting", lambda: accounting("cleanup"))
        if port:
            attempt("notifications_drained", lambda: notifications() is None)
        if result.get("watchdog_quiescent"):
            handles = [("extra_" + str(i), handle) for i, handle in enumerate(extra_handles)]
            handles += [("thread", process.thread), ("process", process.process),
                        ("job", job), ("port", port)]
            for label, handle in handles:
                if handle:
                    result["close_returns"][label] = attempt(
                        "close_" + label, lambda h=handle: bool(prior.checked(k.CloseHandle(h))))
        ready_stage = next((r for r in result["stages"] if r["stage"] == "ready"), None)
        result["verdicts"] = {
            "count_ok": bool(ready_stage and ready_stage["total"] == ready_stage["active"] == 1),
            "limits_ok": bool(result["limits"]) and all(
                r["verdict"]["passed"] for r in result["limits"]),
            "identity_ok": bool(ready_stage) and len(result["identities"]) == ready_stage["total"],
            "cleanup_ok": bool(result.get("watchdog_quiescent") and result.get("direct_reaped")
                               and result.get("final_accounting", [None, None])[1] == 0
                               and len(result["close_returns"]) == 4 + len(extra_handles)
                               and all(result["close_returns"].values()))}
        result.update(elapsed_seconds=time.monotonic() - started,
                      cleanup_seconds=time.monotonic() - cleanup_started,
                      minimum_available=minimum, job_peak=peak)
        save(RUN / "receipt.json", result)
        current = read()
        current["status"] = "completed_pending_review" if accepted(result) else "stopped_no_retry"
        save(METER, current)
        print(json.dumps({"status": current["status"], "verdicts": result["verdicts"],
                          "images": [v["image_name"] for v in result["identities"]]}))


if __name__ == "__main__":
    if sys.argv[1:] != ["run"]:
        raise SystemExit("Only the approved single sealed R1-I attempt is supported")
    run()
