"""R1-S: no-network startup/cleanup repair; no public-fetch entry point."""

import ctypes
import hashlib
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from embedding_budget import NativeJob, memory_snapshot
from public_source_review import PYTHON, ROOT

RUN = ROOT / "data/t17/public-review-repair-01"
METER = RUN / "meter.json"


def initial_state(original):
    """Initialize missing request reservation without changing archived evidence."""
    return {**original, "pending_bytes": 0}


def write(path, value):
    """Atomically persist bounded local receipts without replacing old-run files."""
    data = json.dumps(value, indent=2).encode()
    size = sum(p.stat().st_size for p in RUN.iterdir() if p.is_file())
    if size + len(data) > 2097152:
        raise RuntimeError("Output boundary")
    pending = path.with_suffix(".tmp")
    pending.write_bytes(data)
    pending.replace(path)


def charge_worker():
    """Reserve one of the two real workers before creation; never refund it."""
    state = json.loads(METER.read_text(encoding="utf-8-sig"))
    tick = ctypes.c_int64()
    ctypes.windll.kernel32.QueryPerformanceCounter(ctypes.byref(tick))
    elapsed = (tick.value - state["started_qpc"]) / state["qpc_frequency"]
    if elapsed > 600 or state["normal_starts_used"] >= 20 or state["real_workers"] >= 2:
        raise RuntimeError("Shared execution boundary")
    state["normal_starts_used"] += 1
    state["real_workers"] += 1
    write(METER, state)


class Reserved:
    """Implement every accounting callback used by NativeJob.start and close."""

    def __init__(self, charge, fail_observation=False):
        self.charge = charge
        self.fail_observation = fail_observation
        self.observed = 0

    def reserve_processes(self, count):
        """Only one direct process is allowed in this job."""
        if count != 1:
            raise RuntimeError("Worker reservation boundary")
        self.charge()

    def observe_native(self, total, *, reserved):
        """Keep cumulative observation even when the injected callback fails."""
        self.observed = total
        if total > 1 or reserved != 1 or self.fail_observation:
            raise RuntimeError("Accounting boundary or injected failure")


def finish(job, child, result, persist):
    """Independently attempt close, reap and receipt even if accounting raises."""
    try:
        if job is not None:
            job.close()
    except Exception as error:  # noqa: BLE001 -- cleanup must still reap and persist
        result["cleanup_error"] = type(error).__name__
    finally:
        try:
            if child is not None:
                child.wait(timeout=5)
                result["child_reaped"] = child.poll() is not None
            else:
                result["child_reaped"] = False
        except Exception as error:  # noqa: BLE001 -- preserve terminal failure receipt
            result["reap_error"] = type(error).__name__
        finally:
            persist(result)


def control(name, fail_callback):
    """Run exactly one isolated stdlib child under kernel limits, then close."""
    adapter = Reserved(charge_worker, fail_callback)
    job = child = None
    result = {"name": name, "teardown_verified": False}
    started = time.monotonic()
    minimum = 2**63
    peak = 0
    try:
        memory = memory_snapshot()
        if memory["available_physical"] < 4294967296:
            raise RuntimeError("Insufficient available memory")
        job = NativeJob(adapter)
        limits = job.Extended()
        limits.basic.flags = 0x2000 | 0x8 | 0x100 | 0x200
        limits.basic.active = 1
        limits.process_memory = limits.job_memory = 536870912
        if not job.kernel.SetInformationJobObject(
                job.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            raise ctypes.WinError(ctypes.get_last_error())
        code = f"import time; time.sleep(0.1); raise SystemExit({7 if fail_callback else 0})"
        env = {k: os.environ[k] for k in ("SystemRoot", "WINDIR") if k in os.environ}
        with (RUN / (name + ".log")).open("wb") as output:
            child = job.start([str(PYTHON), "-I", "-S", "-B", "-c", code], env, output)
            while child.poll() is None:
                if time.monotonic() - started > 5:
                    raise RuntimeError("Worker deadline")
                memory = memory_snapshot()
                minimum = min(minimum, memory["available_physical"])
                observed = job.Extended()
                if not job.kernel.QueryInformationJobObject(
                        job.handle, 9, ctypes.byref(observed), ctypes.sizeof(observed), None):
                    raise ctypes.WinError(ctypes.get_last_error())
                peak = max(peak, observed.peak_job)
                if minimum < 4294967296 or memory["controller_private"] > 536870912:
                    raise RuntimeError("Memory boundary")
                time.sleep(0.01)
        child.wait(timeout=1)
        # Independent of the callback: obtain actual kernel job accounting.
        accounting = job.Accounting()
        if not job.kernel.QueryInformationJobObject(
                job.handle, 1, ctypes.byref(accounting), ctypes.sizeof(accounting), None):
            raise ctypes.WinError(ctypes.get_last_error())
        result.update(worker_exit=child.returncode, kernel_total=accounting.total,
                      kernel_active=accounting.active)
    except Exception as error:  # noqa: BLE001 -- bounded controller records all failures
        result["error_type"] = type(error).__name__
    finally:
        result.update(elapsed_seconds=time.monotonic() - started,
                      min_available=minimum, job_peak=peak)

        def persist(value):
            value["callback_observed_total"] = adapter.observed
            value["job_handle_closed"] = job is not None and job.handle is None
            value["teardown_verified"] = bool(
                value.get("child_reaped") and value["job_handle_closed"]
                and value.get("kernel_active") == 0 and value.get("kernel_total") == 1)
            write(RUN / (name + ".json"), value)

        finish(job, child, result, persist)
    return result


def integration():
    """Admit this pair once; failure never starts an automatic retry."""
    state = json.loads(METER.read_text(encoding="utf-8-sig"))
    if state["real_workers"] or (RUN / "integration.json").exists():
        raise RuntimeError("Integration pair already admitted")
    results = []
    for name, fail in (("success", False), ("forced-failure", True)):
        value = control(name, fail)
        results.append(value)
        expected = 7 if fail else 0
        if (not value["teardown_verified"] or value.get("error_type")
                or value.get("worker_exit") != expected
                or bool(value.get("cleanup_error")) != fail):
            break
    complete = len(results) == 2 and all(v["teardown_verified"] for v in results)
    receipt = {"status": "completed_pending_review" if complete else "stopped_no_retry",
               "controls": results, "http_attempts": 0,
               "source_hashes": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (Path(__file__), Path(__file__).with_name(
                                     "test_public_source_repair.py"))}}
    write(RUN / "integration.json", receipt)
    print(json.dumps(receipt))
    if not complete:
        raise RuntimeError("Integration controls incomplete")


if __name__ == "__main__":
    if sys.argv[1:] != ["integration"]:
        raise SystemExit("Only the approved no-network integration pair is available")
    integration()
