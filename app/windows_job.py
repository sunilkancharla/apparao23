"""Windows process-job ownership; import defines data only and starts nothing."""

import ctypes as c
import ipaddress
import os
import subprocess
import threading
import time
from ctypes import wintypes as w
from dataclasses import dataclass
from pathlib import Path

from app.ollama import OllamaError


class BasicLimits(c.Structure):
    """Win32 JOBOBJECT_BASIC_LIMIT_INFORMATION layout."""

    _fields_ = [
        ("process_time", c.c_int64),
        ("job_time", c.c_int64),
        ("flags", w.DWORD),
        ("min_ws", c.c_size_t),
        ("max_ws", c.c_size_t),
        ("active", w.DWORD),
        ("affinity", c.c_size_t),
        ("priority", w.DWORD),
        ("scheduling", w.DWORD),
    ]


class ExtendedLimits(c.Structure):
    """Win32 JOBOBJECT_EXTENDED_LIMIT_INFORMATION layout."""

    _fields_ = [
        ("basic", BasicLimits),
        ("io", c.c_uint64 * 6),
        ("process_memory", c.c_size_t),
        ("job_memory", c.c_size_t),
        ("peak_process", c.c_size_t),
        ("peak_job", c.c_size_t),
    ]


class StartupInfo(c.Structure):
    """Win32 STARTUPINFOW layout; no inherited standard handles."""

    _fields_ = [
        ("cb", w.DWORD),
        ("reserved", w.LPWSTR),
        ("desktop", w.LPWSTR),
        ("title", w.LPWSTR),
        ("x", w.DWORD),
        ("y", w.DWORD),
        ("width", w.DWORD),
        ("height", w.DWORD),
        ("chars_x", w.DWORD),
        ("chars_y", w.DWORD),
        ("fill", w.DWORD),
        ("flags", w.DWORD),
        ("show", w.WORD),
        ("reserved_size", w.WORD),
        ("reserved_data", c.c_void_p),
        ("stdin", w.HANDLE),
        ("stdout", w.HANDLE),
        ("stderr", w.HANDLE),
    ]


class StartupInfoEx(c.Structure):
    """Win32 STARTUPINFOEXW layout for atomic creation inside a job."""

    _fields_ = [("startup", StartupInfo), ("attributes", c.c_void_p)]


class ProcessInfo(c.Structure):
    """Owned process and primary-thread handles returned by CreateProcessW."""

    _fields_ = [
        ("process", w.HANDLE),
        ("thread", w.HANDLE),
        ("pid", w.DWORD),
        ("tid", w.DWORD),
    ]


class Accounting(c.Structure):
    """Cumulative starts include children that exited between observations."""

    _fields_ = [
        ("times", c.c_int64 * 4),
        ("faults", w.DWORD),
        ("total", w.DWORD),
        ("active", w.DWORD),
        ("terminated", w.DWORD),
    ]


class Pids(c.Structure):
    """Bounded active job-membership buffer; incomplete lists are refused."""

    _fields_ = [("assigned", w.DWORD), ("listed", w.DWORD), ("ids", c.c_size_t * 16)]


@dataclass(frozen=True)
class TcpRow:
    """OS-observed endpoint; a PID alone never establishes job membership."""

    state: int
    local: str
    port: int
    remote: str
    pid: int


def parse_tcp_table(raw: bytes, family: int) -> tuple[TcpRow, ...]:
    """Parse only complete IPv4/IPv6 owner-PID tables with bounded record counts."""
    shapes = {2: (24, 0, 4, 8, 12, 20, 4), 23: (56, 48, 0, 20, 24, 52, 16)}
    if family not in shapes or len(raw) < 4:
        raise OllamaError("OLLAMA_TCP_UNAVAILABLE")
    size, state, local, port, remote, pid, width = shapes[family]
    count = int.from_bytes(raw[:4], "little")
    if count > 65536 or 4 + count * size > len(raw):
        raise OllamaError("OLLAMA_TCP_UNAVAILABLE")
    rows = []
    for index in range(count):
        row = raw[4 + index * size : 4 + (index + 1) * size]
        rows.append(
            TcpRow(
                int.from_bytes(row[state : state + 4], "little"),
                str(ipaddress.ip_address(row[local : local + width])),
                int.from_bytes(row[port : port + 2], "big"),
                str(ipaddress.ip_address(row[remote : remote + width])),
                int.from_bytes(row[pid : pid + 4], "little"),
            )
        )
    return tuple(rows)


def check_network(
    rows: tuple[TcpRow, ...], port: int, root_pid: int, owned: set[int]
) -> bool:
    """Require the exact root's IPv4 loopback listener; reject observed external peers."""
    found = False
    for row in rows:
        if row.state == 2 and row.port == port:
            if row.pid != root_pid or row.pid not in owned or row.local != "127.0.0.1":
                raise OllamaError("OLLAMA_LISTENER_UNOWNED")
            found = True
        if row.pid in owned:
            address = ipaddress.ip_address(row.remote)
            mapped = getattr(address, "ipv4_mapped", None)
            if not (
                address.is_unspecified
                or address.is_loopback
                or (mapped and mapped.is_loopback)
            ):
                raise OllamaError("OLLAMA_EXTERNAL_PEER")
    return found


class MemoryStatus(c.Structure):
    """MEMORYSTATUSEX layout."""

    _fields_ = [("length", w.DWORD), ("load", w.DWORD), ("values", c.c_uint64 * 7)]


class ProcessMemory(c.Structure):
    """PROCESS_MEMORY_COUNTERS_EX layout, including private commit."""

    _fields_ = [("length", w.DWORD), ("faults", w.DWORD), ("values", c.c_size_t * 9)]


class WindowsJob:
    """Own one hidden, suspended root atomically created in a kill-on-close job.

    Construct only inside an explicitly authorized runtime session. Limits and
    TCP/memory observations are controls, not a filesystem/network sandbox.
    """

    def __init__(self) -> None:
        if os.name != "nt" or c.sizeof(c.c_void_p) != 8:
            raise OllamaError("OLLAMA_WINDOWS_REQUIRED")
        self._lock = threading.RLock()
        self.k = c.WinDLL("kernel32", use_last_error=True)
        self.ip = c.WinDLL("iphlpapi", use_last_error=True)
        self.ps = c.WinDLL("psapi", use_last_error=True)
        self.handle, self.info = None, ProcessInfo()
        self.starts = 0
        pointer = c.c_void_p
        signatures = {
            "CreateJobObjectW": ([pointer, w.LPCWSTR], w.HANDLE),
            "SetInformationJobObject": ([w.HANDLE, c.c_int, pointer, w.DWORD], w.BOOL),
            "QueryInformationJobObject": (
                [w.HANDLE, c.c_int, pointer, w.DWORD, pointer],
                w.BOOL,
            ),
            "TerminateJobObject": ([w.HANDLE, w.UINT], w.BOOL),
            "CloseHandle": ([w.HANDLE], w.BOOL),
            "InitializeProcThreadAttributeList": (
                [pointer, w.DWORD, w.DWORD, pointer],
                w.BOOL,
            ),
            "UpdateProcThreadAttribute": (
                [pointer, w.DWORD, c.c_size_t, pointer, c.c_size_t, pointer, pointer],
                w.BOOL,
            ),
            "DeleteProcThreadAttributeList": ([pointer], None),
            "CreateProcessW": (
                [
                    w.LPCWSTR,
                    w.LPWSTR,
                    pointer,
                    pointer,
                    w.BOOL,
                    w.DWORD,
                    pointer,
                    w.LPCWSTR,
                    pointer,
                    pointer,
                ],
                w.BOOL,
            ),
            "ResumeThread": ([w.HANDLE], w.DWORD),
            "GetExitCodeProcess": ([w.HANDLE, pointer], w.BOOL),
            "WaitForSingleObject": ([w.HANDLE, w.DWORD], w.DWORD),
            "GlobalMemoryStatusEx": ([pointer], w.BOOL),
        }
        for name, (args, result) in signatures.items():
            function = getattr(self.k, name)
            function.argtypes, function.restype = args, result
        self.ip.GetExtendedTcpTable.argtypes = [
            pointer,
            pointer,
            w.BOOL,
            w.ULONG,
            c.c_int,
            w.ULONG,
        ]
        self.ip.GetExtendedTcpTable.restype = w.DWORD
        self.ps.GetProcessMemoryInfo.argtypes = [w.HANDLE, pointer, w.DWORD]
        self.ps.GetProcessMemoryInfo.restype = w.BOOL
        private, available = self._memory()
        if private >= 8 * 1024**3 or available < 4 * 1024**3:
            raise OllamaError("OLLAMA_MEMORY_LIMIT")
        self.handle = self.k.CreateJobObjectW(None, None)
        if not self.handle:
            raise OllamaError("OLLAMA_JOB_UNAVAILABLE")
        try:
            limits = ExtendedLimits()
            limits.basic.flags, limits.basic.active = 0x2000 | 0x200 | 0x8, 8
            limits.job_memory = 8 * 1024**3 - private
            self._ok(
                self.k.SetInformationJobObject(
                    self.handle, 9, c.byref(limits), c.sizeof(limits)
                )
            )
            actual = self._query(9, ExtendedLimits)
            if (
                actual.basic.flags != limits.basic.flags
                or actual.basic.active != 8
                or actual.job_memory != limits.job_memory
            ):
                raise OllamaError("OLLAMA_JOB_LIMIT_MISMATCH")
        except BaseException:
            self.k.CloseHandle(self.handle)
            self.handle = None
            raise

    @staticmethod
    def _ok(value) -> None:
        if not value:
            raise OllamaError("OLLAMA_JOB_UNAVAILABLE")

    def _query(self, kind: int, shape):
        result = shape()
        self._ok(
            self.k.QueryInformationJobObject(
                self.handle, kind, c.byref(result), c.sizeof(result), None
            )
        )
        return result

    def _memory(self) -> tuple[int, int]:
        system, process = MemoryStatus(), ProcessMemory()
        system.length, process.length = c.sizeof(system), c.sizeof(process)
        self._ok(self.k.GlobalMemoryStatusEx(c.byref(system)))
        self._ok(
            self.ps.GetProcessMemoryInfo(
                w.HANDLE(-1), c.byref(process), c.sizeof(process)
            )
        )
        return process.values[8], system.values[1]

    def _tcp(self) -> tuple[TcpRow, ...]:
        rows = ()
        for family in (2, 23):
            size = w.ULONG()
            status = self.ip.GetExtendedTcpTable(
                None, c.byref(size), False, family, 5, 0
            )
            if status not in (0, 122) or not 4 <= size.value <= 4 * 1024**2:
                raise OllamaError("OLLAMA_TCP_UNAVAILABLE")
            buffer = c.create_string_buffer(size.value)
            if (
                self.ip.GetExtendedTcpTable(buffer, c.byref(size), False, family, 5, 0)
                != 0
            ):
                raise OllamaError("OLLAMA_TCP_UNAVAILABLE")
            rows += parse_tcp_table(buffer.raw, family)
        return rows

    def start(
        self, executable: Path, environment: dict[str, str], directory: Path
    ) -> None:
        """Attach the job in CreateProcess itself, then resume only the owned primary thread."""
        with self._lock:
            if self.info.process or self.handle is None:
                raise OllamaError("OLLAMA_JOB_STATE_INVALID")
            needed = c.c_size_t()
            self.k.InitializeProcThreadAttributeList(None, 1, 0, c.byref(needed))
            if not 0 < needed.value <= 65536:
                raise OllamaError("OLLAMA_JOB_UNAVAILABLE")
            attributes = c.create_string_buffer(needed.value)
            self._ok(
                self.k.InitializeProcThreadAttributeList(
                    attributes, 1, 0, c.byref(needed)
                )
            )
            try:
                jobs = (w.HANDLE * 1)(self.handle)
                self._ok(
                    self.k.UpdateProcThreadAttribute(
                        attributes, 0, 0x2000D, jobs, c.sizeof(jobs), None, None
                    )
                )
                startup = StartupInfoEx()
                startup.startup.cb, startup.startup.flags = c.sizeof(startup), 1
                startup.attributes = c.cast(attributes, c.c_void_p)
                command = c.create_unicode_buffer(
                    subprocess.list2cmdline([str(executable), "serve"])
                )
                block = c.create_unicode_buffer(
                    "\0".join(
                        f"{key}={value}"
                        for key, value in sorted(
                            environment.items(), key=lambda item: item[0].upper()
                        )
                    )
                    + "\0"
                )
                flags = (
                    0x4 | 0x08000000 | 0x80000 | 0x400
                )  # suspended, hidden, extended startup, Unicode env
                self._ok(
                    self.k.CreateProcessW(
                        str(executable),
                        command,
                        None,
                        None,
                        False,
                        flags,
                        block,
                        str(directory),
                        c.byref(startup),
                        c.byref(self.info),
                    )
                )
            finally:
                self.k.DeleteProcThreadAttributeList(attributes)
            if self.k.ResumeThread(self.info.thread) != 1:
                raise OllamaError("OLLAMA_JOB_UNAVAILABLE")
            self._ok(self.k.CloseHandle(self.info.thread))
            self.info.thread = None

    def check(self, port: int, *, require_listener: bool) -> bool:
        """Verify handles/membership, cumulative starts, sampled memory and owned listener."""
        with self._lock:
            if not self.handle or not self.info.process:
                raise OllamaError("OLLAMA_OWNERSHIP_UNVERIFIED")
            code = w.DWORD()
            self._ok(self.k.GetExitCodeProcess(self.info.process, c.byref(code)))
            if code.value != 259:
                raise OllamaError("OLLAMA_PROCESS_EXITED")
            accounting = self._query(1, Accounting)
            members = self._query(3, Pids)
            if members.listed > 16 or members.assigned != members.listed:
                raise OllamaError("OLLAMA_OWNERSHIP_UNVERIFIED")
            owned = set(members.ids[: members.listed])
            if self.info.pid not in owned or accounting.active != len(owned):
                raise OllamaError("OLLAMA_OWNERSHIP_UNVERIFIED")
            self.starts = max(self.starts, accounting.total)
            if self.starts > 16:
                raise OllamaError("OLLAMA_PROCESS_LIMIT")
            private, available = self._memory()
            if (
                private + self._query(9, ExtendedLimits).peak_job > 8 * 1024**3
                or available < 4 * 1024**3
            ):
                raise OllamaError("OLLAMA_MEMORY_LIMIT")
            found = check_network(self._tcp(), port, self.info.pid, owned)
            if require_listener and not found:
                raise OllamaError("OLLAMA_LISTENER_UNOWNED")
            return found

    def close(self) -> None:
        """Terminate only the owned job and verify zero members before releasing handles."""
        with self._lock:
            if self.handle is None:
                return
            self._ok(self.k.TerminateJobObject(self.handle, 0))
            deadline = time.monotonic() + 5
            if (
                self.info.process
                and self.k.WaitForSingleObject(self.info.process, 5000) != 0
            ):
                raise OllamaError("OLLAMA_CLEANUP_PENDING")
            while True:
                accounting = self._query(1, Accounting)
                self.starts = max(self.starts, accounting.total)
                if accounting.active == 0:
                    break
                if time.monotonic() >= deadline:
                    raise OllamaError("OLLAMA_CLEANUP_PENDING")
                time.sleep(0.01)
            for name in ("thread", "process"):
                handle = getattr(self.info, name)
                if handle:
                    self._ok(self.k.CloseHandle(handle))
                    setattr(self.info, name, None)
            self._ok(self.k.CloseHandle(self.handle))
            self.handle = None
