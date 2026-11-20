"""Persistent, locked T10 allowances shared by provisioning, tests and inference."""

import ctypes
import ipaddress
import json
import msvcrt
import subprocess
import threading
import time
from contextlib import contextmanager
from ctypes import wintypes
from pathlib import Path


class BudgetExceeded(RuntimeError):
    """The approved trial cannot proceed within its remaining allowance."""


class Budget:
    """Keep one ledger; construction never resets an existing run."""

    def __init__(self, path: Path, clock=time.time, limits=None):
        self.path = path
        self.clock = clock
        path.parent.mkdir(parents=True, exist_ok=True)
        with self._locked():
            if not path.exists():
                self._write(
                    {
                        "processes": 0,
                        "calls": 0,
                        "downloaded": 0,
                        "provision_started": clock(),
                        "benchmark_started": None,
                        "limits": {
                            "processes": 40,
                            "calls": 200,
                            "downloaded": 3 * 1024**3,
                            **(limits or {}),
                        },
                        "reserved_processes": 0,
                        "native_observed": 0,
                    }
                )
            pending = path.with_suffix(".tmp")
            if pending.exists():
                saved = json.loads(path.read_text(encoding="utf-8-sig"))
                newer = json.loads(pending.read_text(encoding="utf-8"))
                for key in [
                    "processes",
                    "calls",
                    "downloaded",
                    "reserved_processes",
                    "native_observed",
                ]:
                    saved[key] = max(saved.get(key, 0), newer.get(key, 0))
                for key in ["provision_started", "benchmark_started"]:
                    values = [v for v in [saved[key], newer[key]] if v is not None]
                    saved[key] = min(values) if values else None
                self._write(saved)
            if limits:
                saved = json.loads(path.read_text(encoding="utf-8-sig"))
                if any(
                    saved.get("limits", {}).get(key) != value
                    for key, value in limits.items()
                ):
                    raise ValueError("Existing phase limits cannot be changed")

    @contextmanager
    def _locked(self):
        with self.path.with_suffix(".lock").open("a+b") as handle:
            if handle.tell() == 0:
                handle.write(b"0")
                handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)

    def _write(self, state):
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(json.dumps(state), encoding="utf-8")
        for attempt in range(21):
            try:
                temporary.replace(self.path)
                return
            except PermissionError:
                if attempt == 20:
                    raise
                time.sleep(0.1)

    def read(self) -> dict:
        """Return a snapshot without mutating counters."""
        with self._locked():
            return json.loads(self.path.read_text(encoding="utf-8-sig"))

    def start_benchmark(self) -> None:
        """Start the inference deadline once, including native setup/smoke execution."""
        with self._locked():
            state = json.loads(self.path.read_text(encoding="utf-8-sig"))
            if state["benchmark_started"] is None:
                state["benchmark_started"] = self.clock()
                self._write(state)

    def remaining(self) -> float:
        """Refuse an expired benchmark before accepting more local work."""
        state = self.read()
        if state["benchmark_started"] is None:
            raise BudgetExceeded("Benchmark has not started")
        remaining = state.get("limits", {}).get("benchmark_seconds", 1800) - (
            self.clock() - state["benchmark_started"]
        )
        if remaining <= 0:
            raise BudgetExceeded("Benchmark deadline")
        return remaining

    def _charge(self, key, count, limit, provisioning=False):
        if count < 0:
            raise ValueError("Negative allowance")
        with self._locked():
            state = json.loads(self.path.read_text(encoding="utf-8-sig"))
            if provisioning and self.clock() - state["provision_started"] > 5400:
                raise BudgetExceeded("Provisioning deadline")
            limit = state.get("limits", {}).get(key, limit)
            if state[key] + count > limit:
                raise BudgetExceeded(key)
            state[key] += count
            if key == "processes":
                state["reserved_processes"] = state.get("reserved_processes", 0) + count
            self._write(state)

    def reserve_processes(self, count: int) -> None:
        """Reserve known explicit starts before launching them."""
        self._charge("processes", count, 40)

    def observe_native(self, total: int, reserved: int) -> None:
        """Persist kernel cumulative starts before rejecting an observed overshoot.

        One native job belongs to each phase. Its explicitly reserved root is
        already charged; exited discovery/runners remain in the kernel total.
        """
        with self._locked():
            state = json.loads(self.path.read_text(encoding="utf-8-sig"))
            previous = state.get("native_observed", 0)
            state["processes"] += max(0, total - max(previous, reserved))
            state["native_observed"] = max(previous, total)
            self._write(state)
            if state["processes"] > state.get("limits", {}).get("processes", 40):
                raise BudgetExceeded("Observed native process allowance")

    def call(self) -> None:
        """Charge failed and successful API calls before sending either one."""
        self.remaining()
        self._charge("calls", 1, 200)

    def download(self, size: int) -> None:
        """Charge every received payload chunk, including failed-transfer bytes."""
        self._charge("downloaded", size, 3 * 1024**3, provisioning=True)

    def memory(self, available: int, controller_commit: int) -> None:
        """Enforce memory-headroom observations; OS tree limits are separate."""
        if available < 4 * 1024**3 or controller_commit > 1024**3:
            raise BudgetExceeded("Memory headroom")


def memory_snapshot() -> dict:
    """Read actual system availability and controller private/RSS counters."""

    class Status(ctypes.Structure):
        _fields_ = [
            ("length", wintypes.DWORD),
            ("load", wintypes.DWORD),
            ("values", ctypes.c_uint64 * 7),
        ]

    class Counters(ctypes.Structure):
        _fields_ = [
            ("length", wintypes.DWORD),
            ("faults", wintypes.DWORD),
            ("values", ctypes.c_size_t * 9),
        ]

    status, counters = Status(), Counters()
    status.length, counters.length = ctypes.sizeof(status), ctypes.sizeof(counters)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    psapi.GetProcessMemoryInfo.argtypes = [
        wintypes.HANDLE,
        ctypes.c_void_p,
        wintypes.DWORD,
    ]
    if not kernel.GlobalMemoryStatusEx(
        ctypes.byref(status)
    ) or not psapi.GetProcessMemoryInfo(
        wintypes.HANDLE(-1), ctypes.byref(counters), counters.length
    ):
        raise ctypes.WinError(ctypes.get_last_error())
    return {
        "total_physical": status.values[0],
        "available_physical": status.values[1],
        "controller_private": counters.values[8],
        "controller_peak_working_set": counters.values[0],
    }


class NativeJob:
    """Own native descendants under kernel memory/active-process limits and count all starts."""

    def __init__(self, budget: Budget):
        self.budget = budget
        self._mutex = threading.RLock()
        self.kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        k = self.kernel
        k.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        k.CreateJobObjectW.restype = wintypes.HANDLE
        k.SetInformationJobObject.argtypes = [
            wintypes.HANDLE,
            ctypes.c_int,
            ctypes.c_void_p,
            wintypes.DWORD,
        ]
        k.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        k.QueryInformationJobObject.argtypes = [
            wintypes.HANDLE,
            ctypes.c_int,
            ctypes.c_void_p,
            wintypes.DWORD,
            ctypes.c_void_p,
        ]
        k.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
        k.CloseHandle.argtypes = [wintypes.HANDLE]

        class Basic(ctypes.Structure):
            _fields_ = [
                ("process_time", ctypes.c_int64),
                ("job_time", ctypes.c_int64),
                ("flags", wintypes.DWORD),
                ("min_ws", ctypes.c_size_t),
                ("max_ws", ctypes.c_size_t),
                ("active", wintypes.DWORD),
                ("affinity", ctypes.c_size_t),
                ("priority", wintypes.DWORD),
                ("scheduling", wintypes.DWORD),
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

        class Accounting(ctypes.Structure):
            _fields_ = [
                ("times", ctypes.c_int64 * 4),
                ("faults", wintypes.DWORD),
                ("total", wintypes.DWORD),
                ("active", wintypes.DWORD),
                ("terminated", wintypes.DWORD),
            ]

        self.Extended, self.Accounting = Extended, Accounting
        self.handle = k.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = Extended()
        limits.basic.flags = 0x2000 | 0x8 | 0x100 | 0x200
        limits.basic.active = 8
        limits.process_memory = limits.job_memory = 6 * 1024**3
        if not k.SetInformationJobObject(
            self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)
        ):
            self.close()
            raise ctypes.WinError(ctypes.get_last_error())
        self.accounted = 0

    def refresh(self) -> dict:
        """Kernel cumulative accounting includes runners that have already exited."""
        with self._mutex:
            return self._refresh()

    def _refresh(self) -> dict:
        """Serialize polling so two observers cannot charge a descendant twice."""
        accounting, observed = self.Accounting(), self.Extended()
        for kind, value in [(1, accounting), (9, observed)]:
            if not self.kernel.QueryInformationJobObject(
                self.handle, kind, ctypes.byref(value), ctypes.sizeof(value), None
            ):
                raise ctypes.WinError(ctypes.get_last_error())
        self.budget.observe_native(accounting.total, reserved=self.accounted)
        memory = memory_snapshot()
        self.budget.memory(memory["available_physical"], memory["controller_private"])
        self.budget.remaining()
        self._check_tcp()
        return {
            **memory,
            "native_processes": accounting.total,
            "native_active": accounting.active,
            "native_peak_commit": observed.peak_job,
        }

    def _check_tcp(self):
        """Observe owned IPv4/IPv6 TCP peers; stop if any is outside loopback."""

        class Processes(ctypes.Structure):
            _fields_ = [
                ("assigned", wintypes.DWORD),
                ("listed", wintypes.DWORD),
                ("ids", ctypes.c_size_t * 16),
            ]

        processes = Processes()
        if not self.kernel.QueryInformationJobObject(
            self.handle, 3, ctypes.byref(processes), ctypes.sizeof(processes), None
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        owned = set(processes.ids[: processes.listed])
        iphelper = ctypes.WinDLL("iphlpapi", use_last_error=True)
        iphelper.GetExtendedTcpTable.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
            wintypes.BOOL,
            wintypes.ULONG,
            ctypes.c_int,
            wintypes.ULONG,
        ]
        for family, row_size, remote_offset, pid_offset in [
            (2, 24, 12, 20),
            (23, 56, 24, 52),
        ]:
            length = wintypes.ULONG(0)
            status = iphelper.GetExtendedTcpTable(
                None, ctypes.byref(length), False, family, 5, 0
            )
            if status not in {0, 122} or length.value > 4 * 1024**2:
                raise RuntimeError("Cannot observe native TCP boundary")
            buffer = ctypes.create_string_buffer(length.value)
            if iphelper.GetExtendedTcpTable(
                buffer, ctypes.byref(length), False, family, 5, 0
            ):
                raise RuntimeError("Cannot observe native TCP boundary")
            raw = buffer.raw
            for index in range(int.from_bytes(raw[:4], "little")):
                row = raw[4 + index * row_size : 4 + (index + 1) * row_size]
                if (
                    int.from_bytes(row[pid_offset : pid_offset + 4], "little")
                    not in owned
                ):
                    continue
                address = ipaddress.ip_address(
                    row[remote_offset : remote_offset + (4 if family == 2 else 16)]
                )
                mapped = getattr(address, "ipv4_mapped", None)
                if (
                    not address.is_unspecified
                    and not address.is_loopback
                    and not (mapped and mapped.is_loopback)
                ):
                    raise BudgetExceeded("Unexpected native TCP peer")

    def start(self, args, env, output):
        """Create suspended/hidden; assign before any executable instruction runs."""
        self.budget.reserve_processes(1)
        process = subprocess.Popen(
            args,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=output,
            stderr=output,
            creationflags=0x4 | 0x08000000,
        )
        try:
            if not self.kernel.AssignProcessToJobObject(
                self.handle, wintypes.HANDLE(process._handle)
            ):
                raise ctypes.WinError(ctypes.get_last_error())
            self.accounted += 1

            # Popen closes its thread handle, so enumerate/open only this suspended child's thread.
            class Thread(ctypes.Structure):
                _fields_ = [
                    ("size", wintypes.DWORD),
                    ("usage", wintypes.DWORD),
                    ("id", wintypes.DWORD),
                    ("owner", wintypes.DWORD),
                    ("base", wintypes.LONG),
                    ("delta", wintypes.LONG),
                    ("flags", wintypes.DWORD),
                ]

            k = self.kernel
            k.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
            k.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
            k.Thread32First.argtypes = k.Thread32Next.argtypes = [
                wintypes.HANDLE,
                ctypes.c_void_p,
            ]
            k.OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
            k.OpenThread.restype = wintypes.HANDLE
            k.ResumeThread.argtypes = [wintypes.HANDLE]
            k.ResumeThread.restype = wintypes.DWORD
            snapshot = k.CreateToolhelp32Snapshot(4, 0)
            if snapshot == wintypes.HANDLE(-1).value:
                raise ctypes.WinError(ctypes.get_last_error())
            resumed = False
            try:
                thread = Thread()
                thread.size = ctypes.sizeof(thread)
                found = k.Thread32First(snapshot, ctypes.byref(thread))
                while found:
                    if thread.owner == process.pid:
                        handle = k.OpenThread(2, False, thread.id)
                        if not handle:
                            raise ctypes.WinError(ctypes.get_last_error())
                        try:
                            if k.ResumeThread(handle) == 0xFFFFFFFF:
                                raise ctypes.WinError(ctypes.get_last_error())
                            resumed = True
                        finally:
                            k.CloseHandle(handle)
                        break
                    found = k.Thread32Next(snapshot, ctypes.byref(thread))
            finally:
                k.CloseHandle(snapshot)
            if not resumed:
                raise RuntimeError("Cannot resume owned native child")
            return process
        except BaseException:
            process.kill()
            process.wait(timeout=5)
            raise

    def close(self):
        """Kill/reap only members of the owned job; never unrelated services."""
        with self._mutex:
            if self.handle:
                self.kernel.TerminateJobObject(self.handle, 1)
                try:
                    # Termination can race with a final discovery spawn. Preserve
                    # the final cumulative count even when the guard is exceeded.
                    accounting = self.Accounting()
                    if self.kernel.QueryInformationJobObject(
                        self.handle,
                        1,
                        ctypes.byref(accounting),
                        ctypes.sizeof(accounting),
                        None,
                    ):
                        try:
                            self.budget.observe_native(
                                accounting.total, reserved=self.accounted
                            )
                        except BudgetExceeded:
                            pass  # The overshoot was persisted before raising.
                finally:
                    self.kernel.CloseHandle(self.handle)
                    self.handle = None

    def bound_controller(self):
        """Assign the controller after server creation, avoiding inherited 1 GiB runner limits."""
        handle = self.kernel.CreateJobObjectW(None, None)
        limits = self.Extended()
        limits.basic.flags = 0x100
        limits.process_memory = 1024**3
        if (
            not handle
            or not self.kernel.SetInformationJobObject(
                handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)
            )
            or not self.kernel.AssignProcessToJobObject(handle, wintypes.HANDLE(-1))
        ):
            if handle:
                self.kernel.CloseHandle(handle)
            raise ctypes.WinError(ctypes.get_last_error())
        return handle
