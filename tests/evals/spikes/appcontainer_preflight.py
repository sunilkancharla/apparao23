"""Bounded Windows AppContainer investigation; never imports OCR packages.

Only the explicitly approved evaluation controller may call the native helpers.
Routine tests exercise safety policy without changing profiles or permissions.
"""

from __future__ import annotations

import ctypes
import hashlib
import json
import os
import socket
import stat
import subprocess
import time
from ctypes import wintypes as w
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN_ID = "preflight-01"
RUN = ROOT / "data/t09-appcontainer" / RUN_ID
STAGE = ROOT / ".venv/tools/appcontainer-preflight" / RUN_ID
BASE = Path("F:/Python/Python314")
ROOT_FILES = frozenset({"python.exe", "python3.dll", "python314.dll",
                        "vcruntime140.dll", "vcruntime140_1.dll", "LICENSE.txt"})


def regular_attributes(attributes: int) -> bool:
    """Reject Windows reparse points, including junctions."""
    return not bool(attributes & 0x400)


def contained(root: Path, target: Path) -> Path:
    """Resolve an owned path only after rejecting existing reparse components."""
    absolute = Path(os.path.abspath(target))
    expected = Path(os.path.abspath(root))
    if not absolute.is_relative_to(expected):
        raise ValueError("Path escapes owned root")
    for part in (absolute, *absolute.parents):
        if part.exists() and not regular_attributes(
            getattr(part.lstat(), "st_file_attributes", 0)
        ):
            raise ValueError("Reparse path forbidden")
    if not absolute.resolve().is_relative_to(expected.resolve()):
        raise ValueError("Resolved path escapes root")
    return absolute


def grant_rights(role: str) -> str:
    """Permit exactly the approved grant roles."""
    if role not in {"runtime", "inputs", "work", "traverse"}:
        raise ValueError("Unapproved grant role")
    return {"runtime": "RX", "inputs": "RX", "work": "M",
            "traverse": "traverse"}[role]


def next_count(current: int, slots: int, limit: int, *, cleanup: bool = False) -> int:
    """Keep twelve slots available for teardown and closeout."""
    if slots <= 0 or current + slots > limit - (0 if cleanup else 12):
        raise RuntimeError("Shared process budget exhausted")
    return current + slots


def owns_profile(name: str, run_id: str, created: bool) -> bool:
    """Only the profile successfully created by this run may be removed."""
    return created and name == f"DocumentAssistant.T09.{run_id}"


def validate_token(info: dict, sid: str) -> None:
    """Require the expected AppContainer identity, low integrity and no capability."""
    if not (info["appcontainer"] and info["sid"] == sid
            and info["capabilities"] == 0 and info["integrity"] == 4096):
        raise RuntimeError("Unexpected worker token")


def native_denied(error: int, observed: bool) -> bool:
    """Only explicit WSAEACCES with no delivered marker proves this control."""
    return error == 10013 and not observed


def runtime_member(relative: Path) -> bool:
    """Select the approved local runtime, excluding installed third-party code."""
    parts = relative.parts
    if not parts or relative.is_absolute() or ".." in parts:
        return False
    if len(parts) == 1:
        return relative.name in ROOT_FILES
    return parts[0] in {"Lib", "DLLs"} and not any(
        part in {"site-packages", "__pycache__", "test", "tests"}
        for part in parts[1:]
    )


def receipt(name: str, value: object) -> None:
    """Write controller-owned JSON with no document content."""
    path = contained(RUN, RUN / name)
    path.write_text(json.dumps(value, indent=2), encoding="utf-8")


def reserve(purpose: str, slots: int = 1, *, cleanup: bool = False) -> None:
    """Charge every controller-requested creation before calling the OS."""
    path = RUN / "meter.json"
    meter = json.loads(path.read_text(encoding="utf-8-sig"))
    from datetime import UTC, datetime

    deadline = meter.get("execution_deadline_utc", meter["deadline_utc"])
    if not cleanup and datetime.now(UTC) > datetime.fromisoformat(deadline):
        raise RuntimeError("Shared execution deadline exhausted")
    meter["reserved"] = next_count(meter["reserved"], slots, meter["limit"],
                                   cleanup=cleanup)
    event = {"purpose": purpose, "slots": slots, "at_unix": time.time()}
    meter["events"].append(event)
    receipt("meter.json", meter)
    with (RUN / "events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event) + "\n")


def stage_runtime() -> list[dict]:
    """Copy/hash allowlisted existing runtime bytes without modifying their source."""
    target = contained(STAGE, STAGE / "runtime")
    if target.exists():
        raise RuntimeError("Staging collision")
    manifest = []
    total = 0
    for current, directories, files in os.walk(BASE, followlinks=False):
        parent = Path(current)
        relative_parent = parent.relative_to(BASE)
        contained(BASE, parent)
        directories[:] = [name for name in directories if
                          (relative_parent == Path(".") and name in {"Lib", "DLLs"})
                          or (relative_parent != Path(".") and name not in
                              {"site-packages", "__pycache__", "test", "tests"})]
        for name in files:
            source = contained(BASE, parent / name)
            relative = source.relative_to(BASE)
            if not runtime_member(relative):
                continue
            info = source.stat()
            if not stat.S_ISREG(info.st_mode):
                raise RuntimeError("Non-regular runtime entry")
            total += info.st_size
            if total > 128 * 1024**2:
                raise RuntimeError("Runtime staging cap")
            content = source.read_bytes()
            if len(content) != info.st_size:
                raise RuntimeError("Source changed during copy")
            destination = contained(STAGE, target / relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as stream:
                stream.write(content)
            digest = hashlib.sha256(content).hexdigest()
            if hashlib.sha256(destination.read_bytes()).hexdigest() != digest:
                raise RuntimeError("Runtime copy hash mismatch")
            manifest.append({"path": relative.as_posix(), "bytes": len(content),
                             "sha256": digest})
    if not ROOT_FILES.issubset({item["path"] for item in manifest}):
        raise RuntimeError("Required runtime bytes absent")
    receipt("runtime-manifest.json", manifest)
    return manifest


class BasicLimits(ctypes.Structure):
    """Native JOBOBJECT_BASIC_LIMIT_INFORMATION layout."""

    _fields_ = [("user_time", ctypes.c_int64), ("job_time", ctypes.c_int64),
                ("flags", w.DWORD), ("minimum", ctypes.c_size_t),
                ("maximum", ctypes.c_size_t), ("active", w.DWORD),
                ("affinity", ctypes.c_size_t), ("priority", w.DWORD),
                ("scheduling", w.DWORD)]


class ExtendedLimits(ctypes.Structure):
    """Native extended Job memory/process limit layout."""

    _fields_ = [("basic", BasicLimits), ("io", ctypes.c_uint64 * 6),
                ("process_memory", ctypes.c_size_t), ("job_memory", ctypes.c_size_t),
                ("peak_process", ctypes.c_size_t), ("peak_job", ctypes.c_size_t)]


class Startup(ctypes.Structure):
    """STARTUPINFOW; handles are deliberately not inherited."""

    _fields_ = [("cb", w.DWORD), ("reserved", w.LPWSTR), ("desktop", w.LPWSTR),
                ("title", w.LPWSTR), ("x", w.DWORD), ("y", w.DWORD),
                ("xs", w.DWORD), ("ys", w.DWORD), ("xc", w.DWORD),
                ("yc", w.DWORD), ("fill", w.DWORD), ("flags", w.DWORD),
                ("show", w.WORD), ("reserved2_size", w.WORD),
                ("reserved2", ctypes.c_void_p), ("stdin", w.HANDLE),
                ("stdout", w.HANDLE), ("stderr", w.HANDLE)]


class StartupEx(ctypes.Structure):
    """STARTUPINFOEXW with security/child-policy attributes."""

    _fields_ = [("startup", Startup), ("attributes", ctypes.c_void_p)]


class ProcessInfo(ctypes.Structure):
    """Owned process/thread handles returned by CreateProcessW."""

    _fields_ = [("process", w.HANDLE), ("thread", w.HANDLE),
                ("pid", w.DWORD), ("tid", w.DWORD)]


class SecurityCapabilities(ctypes.Structure):
    """Zero-capability AppContainer process creation data."""

    _fields_ = [("sid", ctypes.c_void_p), ("capabilities", ctypes.c_void_p),
                ("count", w.DWORD), ("reserved", w.DWORD)]


class Native:
    """Typed Windows calls used only by the explicitly approved preflight."""

    def __init__(self):
        self.kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        self.advapi = ctypes.WinDLL("advapi32", use_last_error=True)
        self.userenv = ctypes.WinDLL("userenv", use_last_error=True)
        self._bind(self.kernel, "CreateJobObjectW", [ctypes.c_void_p, w.LPCWSTR], w.HANDLE)
        self._bind(self.kernel, "GetCurrentProcess", [], w.HANDLE)
        self._bind(self.kernel, "CloseHandle", [w.HANDLE], w.BOOL)
        self._bind(self.kernel, "LocalFree", [ctypes.c_void_p], ctypes.c_void_p)
        self._bind(self.kernel, "AssignProcessToJobObject", [w.HANDLE, w.HANDLE], w.BOOL)
        self._bind(self.kernel, "SetInformationJobObject",
                   [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD], w.BOOL)
        self._bind(self.kernel, "QueryInformationJobObject",
                   [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD, ctypes.c_void_p], w.BOOL)
        self._bind(self.kernel, "IsProcessInJob",
                   [w.HANDLE, w.HANDLE, ctypes.POINTER(w.BOOL)], w.BOOL)
        self._bind(self.kernel, "TerminateJobObject", [w.HANDLE, w.UINT], w.BOOL)
        self._bind(self.kernel, "ResumeThread", [w.HANDLE], w.DWORD)
        self._bind(self.kernel, "WaitForSingleObject", [w.HANDLE, w.DWORD], w.DWORD)
        self._bind(self.kernel, "TerminateProcess", [w.HANDLE, w.UINT], w.BOOL)
        self._bind(self.kernel, "GetExitCodeProcess", [w.HANDLE, ctypes.POINTER(w.DWORD)], w.BOOL)
        self._bind(self.kernel, "CreateProcessW",
                   [w.LPCWSTR, w.LPWSTR, ctypes.c_void_p, ctypes.c_void_p, w.BOOL,
                    w.DWORD, ctypes.c_void_p, w.LPCWSTR, ctypes.c_void_p,
                    ctypes.POINTER(ProcessInfo)], w.BOOL)
        self._bind(self.kernel, "InitializeProcThreadAttributeList",
                   [ctypes.c_void_p, w.DWORD, w.DWORD, ctypes.POINTER(ctypes.c_size_t)], w.BOOL)
        self._bind(self.kernel, "UpdateProcThreadAttribute",
                   [ctypes.c_void_p, w.DWORD, ctypes.c_size_t, ctypes.c_void_p,
                    ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p], w.BOOL)
        self._bind(self.kernel, "DeleteProcThreadAttributeList", [ctypes.c_void_p], None)
        self._bind(self.advapi, "OpenProcessToken",
                   [w.HANDLE, w.DWORD, ctypes.POINTER(w.HANDLE)], w.BOOL)
        self._bind(self.advapi, "GetTokenInformation",
                   [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD,
                    ctypes.POINTER(w.DWORD)], w.BOOL)
        self._bind(self.advapi, "ConvertSidToStringSidW",
                   [ctypes.c_void_p, ctypes.POINTER(w.LPWSTR)], w.BOOL)
        self._bind(self.advapi, "FreeSid", [ctypes.c_void_p], ctypes.c_void_p)
        self._bind(self.userenv, "CreateAppContainerProfile",
                   [w.LPCWSTR, w.LPCWSTR, w.LPCWSTR, ctypes.c_void_p, w.DWORD,
                    ctypes.POINTER(ctypes.c_void_p)], ctypes.c_long)
        self._bind(self.userenv, "DeleteAppContainerProfile", [w.LPCWSTR], ctypes.c_long)

    @staticmethod
    def _bind(library, name, arguments, result):
        function = getattr(library, name)
        function.argtypes = arguments
        function.restype = result

    @staticmethod
    def check(value):
        """Preserve native errors rather than converting them into passes."""
        if not value:
            raise ctypes.WinError(ctypes.get_last_error())
        return value

    def job(self, active: int, *, kill: bool = True):
        """Set verified process/memory limits before assigning any worker."""
        handle = self.check(self.kernel.CreateJobObjectW(None, None))
        info = ExtendedLimits()
        info.basic.flags = 0x8 | 0x100 | (0x2000 if kill else 0)
        info.basic.active = active
        info.process_memory = 512 * 1024**2
        try:
            self.check(self.kernel.SetInformationJobObject(
                handle, 9, ctypes.byref(info), ctypes.sizeof(info)))
        except BaseException:
            self.kernel.CloseHandle(handle)
            raise
        return handle

    def accounting(self, job) -> dict:
        """Read Job totals, including children, from kernel accounting."""
        # Four LARGE_INTEGER times followed by four DWORD accounting fields.
        data = ctypes.create_string_buffer(48)
        self.check(self.kernel.QueryInformationJobObject(job, 1, data, 48, None))
        import struct

        total, active, terminated = struct.unpack_from("III", data.raw, 36)
        return {"total": total, "active": active, "terminated": terminated}

    def sid_text(self, sid) -> str:
        text = w.LPWSTR()
        self.check(self.advapi.ConvertSidToStringSidW(sid, ctypes.byref(text)))
        try:
            return text.value
        finally:
            self.kernel.LocalFree(text)

    def token(self, process) -> dict:
        """Read the actual suspended process token, not requested launch settings."""
        handle = w.HANDLE()
        self.check(self.advapi.OpenProcessToken(process, 8, ctypes.byref(handle)))
        try:
            def query(kind):
                size = w.DWORD()
                self.advapi.GetTokenInformation(handle, kind, None, 0, ctypes.byref(size))
                if size.value > 65536 or not size.value:
                    raise RuntimeError("Unexpected token size")
                data = ctypes.create_string_buffer(size.value)
                self.check(self.advapi.GetTokenInformation(
                    handle, kind, data, size, ctypes.byref(size)))
                return data

            import struct

            appcontainer = struct.unpack_from("I", query(29))[0]
            # Keep backing buffers alive until their referenced SID is consumed.
            package = query(31)
            label = query(25)
            label_sid = ctypes.c_void_p.from_buffer(label).value
            integrity = int(self.sid_text(label_sid).split("-")[-1])
            return {"appcontainer": bool(appcontainer),
                        "sid": self.sid_text(ctypes.c_void_p.from_buffer(package).value),
                        "capabilities": struct.unpack_from("I", query(30))[0],
                        "integrity": integrity}
        finally:
            self.kernel.CloseHandle(handle)


def memory_ready() -> None:
    """Enforce the approved available physical RAM floor."""
    class Memory(ctypes.Structure):
        _fields_ = [("length", w.DWORD), ("load", w.DWORD)] + [
            (name, ctypes.c_uint64) for name in
            ("physical", "available", "pagefile", "available_pagefile",
             "virtual", "available_virtual", "extended")]

    data = Memory()
    data.length = ctypes.sizeof(data)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(data)):
        raise ctypes.WinError()
    if data.available < 4 * 1024**3:
        raise RuntimeError("Less than 4 GiB available system RAM")


def acl_command(native: Native, *arguments: str) -> str:
    """Run one fixed Windows ACL utility with a charged native process slot."""
    reserve("owned run-path icacls operation", cleanup=arguments[1] == "/remove:g")
    utility = Path(os.environ["SystemRoot"]) / "System32/icacls.exe"
    result = subprocess.run([str(utility), *arguments], capture_output=True,
                            timeout=15, check=False)
    if result.returncode:
        raise RuntimeError(f"icacls failed ({result.returncode}): "
                           + result.stdout.decode(errors="replace")[:1000])
    return result.stdout.decode(errors="replace")


def security_text(path: Path) -> str:
    """Read a run-path DACL/mandatory label for change/cleanup evidence."""
    advapi = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    Native._bind(advapi, "GetNamedSecurityInfoW",
                 [w.LPWSTR, ctypes.c_int, w.DWORD, ctypes.c_void_p,
                  ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
                  ctypes.POINTER(ctypes.c_void_p)], w.DWORD)
    Native._bind(advapi, "ConvertSecurityDescriptorToStringSecurityDescriptorW",
                 [ctypes.c_void_p, w.DWORD, w.DWORD, ctypes.POINTER(w.LPWSTR),
                  ctypes.c_void_p], w.BOOL)
    Native._bind(kernel, "LocalFree", [ctypes.c_void_p], ctypes.c_void_p)
    descriptor = ctypes.c_void_p()
    error = advapi.GetNamedSecurityInfoW(str(path), 1, 0x14, None, None,
                                        None, None, ctypes.byref(descriptor))
    if error:
        raise ctypes.WinError(error)
    text = w.LPWSTR()
    try:
        Native.check(advapi.ConvertSecurityDescriptorToStringSecurityDescriptorW(
            descriptor, 1, 0x14, ctypes.byref(text), None))
        return text.value
    finally:
        if text:
            kernel.LocalFree(text)
        kernel.LocalFree(descriptor)


def bounded_tree_bytes(root: Path, cap: int) -> int:
    """Count run/profile storage without following reparse points."""
    total = 0
    for current, directories, files in os.walk(root, followlinks=False):
        for name in [*directories, *files]:
            item = Path(current) / name
            info = item.lstat()
            if not regular_attributes(getattr(info, "st_file_attributes", 0)):
                raise RuntimeError("Unexpected profile/run reparse point")
            if stat.S_ISREG(info.st_mode):
                total += info.st_size
                if total > cap:
                    raise RuntimeError("Run/profile disk cap exceeded")
    return total


def restore_work_label(before: str) -> None:
    """Restore only the owned work tree's prior label, preserving current DACL."""
    advapi = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    Native._bind(advapi, "ConvertStringSecurityDescriptorToSecurityDescriptorW",
                 [w.LPCWSTR, w.DWORD, ctypes.POINTER(ctypes.c_void_p), ctypes.c_void_p], w.BOOL)
    Native._bind(advapi, "GetSecurityDescriptorSacl",
                 [ctypes.c_void_p, ctypes.POINTER(w.BOOL), ctypes.POINTER(ctypes.c_void_p),
                  ctypes.POINTER(w.BOOL)], w.BOOL)
    Native._bind(advapi, "SetNamedSecurityInfoW",
                 [w.LPWSTR, ctypes.c_int, w.DWORD] + [ctypes.c_void_p] * 4, w.DWORD)
    Native._bind(kernel, "LocalFree", [ctypes.c_void_p], ctypes.c_void_p)
    descriptor = ctypes.c_void_p()
    sacl = ctypes.c_void_p()
    try:
        if "S:" in before:
            Native.check(advapi.ConvertStringSecurityDescriptorToSecurityDescriptorW(
                before[before.index("S:"):], 1, ctypes.byref(descriptor), None))
            present, defaulted = w.BOOL(), w.BOOL()
            Native.check(advapi.GetSecurityDescriptorSacl(
                descriptor, ctypes.byref(present), ctypes.byref(sacl), ctypes.byref(defaulted)))
        error = advapi.SetNamedSecurityInfoW(str(RUN / "work"), 1, 0x10,
                                            None, None, None, sacl)
        if error:
            raise ctypes.WinError(error)
    finally:
        if descriptor:
            kernel.LocalFree(descriptor)


def launch_worker(native: Native, sid, expected_sid: str, script: Path,
                  mode: str, *, constrained: bool, expected_timeout: bool = False) -> dict:
    """Create suspended, validate and assign a worker before any authored code runs."""
    reserve(f"{'AppContainer' if constrained else 'positive'} {mode} worker")
    memory_ready()
    job = native.job(1)
    process = ProcessInfo()
    attributes = None
    startup = StartupEx()
    startup.startup.cb = ctypes.sizeof(StartupEx)
    capability = SecurityCapabilities(sid, None, 0, 0)
    child_policy = w.DWORD(1)  # PROCESS_CREATION_CHILD_PROCESS_RESTRICTED
    token = None
    started = time.monotonic()
    try:
        size = ctypes.c_size_t()
        native.kernel.InitializeProcThreadAttributeList(None, 2, 0, ctypes.byref(size))
        attributes = ctypes.create_string_buffer(size.value)
        native.check(native.kernel.InitializeProcThreadAttributeList(
            attributes, 2, 0, ctypes.byref(size)))
        startup.attributes = ctypes.cast(attributes, ctypes.c_void_p)
        if constrained:
            native.check(native.kernel.UpdateProcThreadAttribute(
                attributes, 0, 0x20009, ctypes.byref(capability),
                ctypes.sizeof(capability), None, None))
        native.check(native.kernel.UpdateProcThreadAttribute(
            attributes, 0, 0x2000E, ctypes.byref(child_policy),
            ctypes.sizeof(child_policy), None, None))
        executable = STAGE / "runtime/python.exe"
        command = subprocess.list2cmdline([str(executable), "-I", "-S", "-B",
                                          str(script), mode])
        environment = {"SystemRoot": os.environ["SystemRoot"],
                       "WINDIR": os.environ["SystemRoot"],
                       "TEMP": str(RUN / "work"), "TMP": str(RUN / "work")}
        block = ctypes.create_unicode_buffer("\0".join(
            f"{key}={value}" for key, value in sorted(environment.items())) + "\0\0")
        native.check(native.kernel.CreateProcessW(
            str(executable), ctypes.create_unicode_buffer(command), None, None, False,
            0x80000 | 0x4 | 0x400 | 0x8000000, block, str(RUN / "work"),
            ctypes.byref(startup), ctypes.byref(process)))
        if constrained:
            token = native.token(process.process)
            validate_token(token, expected_sid)
        native.check(native.kernel.AssignProcessToJobObject(job, process.process))
        inside = w.BOOL()
        native.check(native.kernel.IsProcessInJob(process.process, job, ctypes.byref(inside)))
        if not inside.value or native.accounting(job)["total"] != 1:
            raise RuntimeError("Worker Job/accounting failure")
        if native.kernel.ResumeThread(process.thread) == 0xFFFFFFFF:
            raise ctypes.WinError(ctypes.get_last_error())
        timed_out = False
        while native.kernel.WaitForSingleObject(process.process, 100) == 258:
            if time.monotonic() - started >= (1 if expected_timeout else 15):
                timed_out = True
                native.check(native.kernel.TerminateJobObject(job, 124))
                native.kernel.WaitForSingleObject(process.process, 5000)
                break
            bounded_tree_bytes(RUN / "work", 16 * 1024**2)
            if getattr(native, "profile_path", None):
                bounded_tree_bytes(native.profile_path, 128 * 1024**2)
        code = w.DWORD()
        native.check(native.kernel.GetExitCodeProcess(process.process, ctypes.byref(code)))
        accounting = native.accounting(job)
        result = {"mode": mode, "constrained": constrained, "token": token,
                      "exit_code": code.value, "timed_out": timed_out, "accounting": accounting}
        receipt(f"worker-{mode}-{'restricted' if constrained else 'positive'}.json", result)
        if timed_out != expected_timeout or (not timed_out and code.value != 0):
            raise RuntimeError(f"Worker startup/control failed: {result}")
        if accounting["total"] != 1 or accounting["active"] != 0:
            raise RuntimeError("Unexpected descendant or unfinished worker")
        return result
    finally:
        if process.process:
            native.kernel.TerminateProcess(process.process, 125)
            native.kernel.WaitForSingleObject(process.process, 5000)
        for handle in (process.thread, process.process, job):
            if handle:
                native.kernel.CloseHandle(handle)
        if attributes is not None:
            native.kernel.DeleteProcThreadAttributeList(attributes)


def profile_folder(native: Native, sid_text: str) -> Path:
    """Obtain exactly this profile's Windows-managed storage path."""
    Native._bind(native.userenv, "GetAppContainerFolderPath",
                 [w.LPCWSTR, ctypes.POINTER(w.LPWSTR)], ctypes.c_long)
    ole = ctypes.WinDLL("ole32")
    Native._bind(ole, "CoTaskMemFree", [ctypes.c_void_p], None)
    text = w.LPWSTR()
    error = native.userenv.GetAppContainerFolderPath(sid_text, ctypes.byref(text))
    if error < 0:
        raise OSError(f"GetAppContainerFolderPath HRESULT {error & 0xFFFFFFFF:08x}")
    try:
        return Path(text.value)
    finally:
        ole.CoTaskMemFree(text)


WORKER = r'''
"""Authored synthetic controls only; no OCR/third-party imports."""
import ctypes
import json
import socket
import struct
import subprocess
import sys
import time
from pathlib import Path

run = Path(__file__).resolve().parent.parent
mode = sys.argv[1]
result = {"version": list(sys.version_info[:3]), "prefix": sys.prefix}
if mode == "files":
    assert (run / "inputs/marker.txt").read_text() == "synthetic-marker"
    denied = []
    for name, action in (("private/sentinel.txt", "r"),
                         ("private/sentinel.txt", "w"),
                         ("inputs/marker.txt", "w"),
                         ("sibling/sentinel.txt", "w")):
        try:
            with (run / name).open(action):
                pass
        except PermissionError as error:
            denied.append({"path": name, "mode": action, "winerror": error.winerror})
        else:
            raise RuntimeError("Synthetic file isolation failed: " + name)
    result["denied"] = denied
elif mode == "network":
    ws = ctypes.WinDLL("ws2_32", use_last_error=True)
    def bind(name, args, result_type):
        function = getattr(ws, name)
        function.argtypes = args
        function.restype = result_type
        return function
    startup = bind("WSAStartup", [ctypes.c_ushort, ctypes.c_void_p], ctypes.c_int)
    create = bind("socket", [ctypes.c_int] * 3, ctypes.c_size_t)
    connect = bind("connect", [ctypes.c_size_t, ctypes.c_void_p, ctypes.c_int], ctypes.c_int)
    send = bind("send", [ctypes.c_size_t, ctypes.c_void_p, ctypes.c_int, ctypes.c_int], ctypes.c_int)
    sendto = bind("sendto", [ctypes.c_size_t, ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
                             ctypes.c_void_p, ctypes.c_int], ctypes.c_int)
    close = bind("closesocket", [ctypes.c_size_t], ctypes.c_int)
    last_error = bind("WSAGetLastError", [], ctypes.c_int)
    cleanup = bind("WSACleanup", [], ctypes.c_int)
    state = ctypes.create_string_buffer(512)
    if startup(0x202, state):
        raise RuntimeError("WSAStartup failed")
    result["attempts"] = []
    try:
        for endpoint in json.loads((run / "inputs/endpoints.json").read_text()):
            family = endpoint["family"]
            kind = endpoint["kind"]
            sock = create(family, kind, 6 if kind == 1 else 17)
            if sock == ctypes.c_size_t(-1).value:
                raise RuntimeError("Native socket creation failed")
            try:
                address = struct.pack("=H", family) + struct.pack("!H", endpoint["port"])
                if family == 2:
                    address += socket.inet_pton(family, endpoint["host"]) + bytes(8)
                else:
                    address += bytes(4) + socket.inet_pton(family, endpoint["host"]) + bytes(4)
                buffer = ctypes.create_string_buffer(address)
                if kind == 1:
                    code = connect(sock, buffer, len(address))
                    error = last_error() if code else 0
                    if code == 0 and send(sock, b"T09", 3, 0) != 3:
                        raise RuntimeError("Positive native TCP send failed")
                else:
                    code = sendto(sock, b"T09", 3, 0, buffer, len(address))
                    error = last_error() if code == -1 else 0
                result["attempts"].append({"family": family, "kind": kind, "error": error})
            finally:
                close(sock)
    finally:
        cleanup()
elif mode == "child":
    try:
        child = subprocess.Popen([sys.executable, "-I", "-S", "-B", "-c", "pass"])
    except PermissionError as error:
        result["child_denied"] = error.winerror
    else:
        child.wait(timeout=2)
        raise RuntimeError("Child process unexpectedly created")
elif mode == "timeout":
    time.sleep(60)
elif mode != "startup":
    raise RuntimeError("Unknown control")
(run / "work" / (mode + ".json")).write_text(json.dumps(result))
'''


def execute(controller_job) -> None:
    """Run the approved bounded probe, cleaning only successfully owned changes."""
    from datetime import UTC, datetime

    native = Native()
    profile = f"DocumentAssistant.T09.{RUN_ID}"
    sid = ctypes.c_void_p()
    created = False
    changes = []
    listeners = []
    result = {"status": "in_progress", "profile_created": False}
    meter = json.loads((RUN / "meter.json").read_text(encoding="utf-8-sig"))
    if datetime.now(UTC) > datetime.fromisoformat(meter["deadline_utc"]):
        raise RuntimeError("Preparation deadline exhausted")
    meter["execution_deadline_utc"] = datetime.fromtimestamp(
        time.time() + 1200, UTC).isoformat()
    receipt("meter.json", meter)
    for name in ("inputs", "work", "private", "receipts", "sibling"):
        contained(RUN, RUN / name).mkdir(exist_ok=False)
    (RUN / "inputs/marker.txt").write_text("synthetic-marker")
    (RUN / "private/sentinel.txt").write_text("private-synthetic-marker")
    (RUN / "sibling/sentinel.txt").write_text("sibling-synthetic-marker")
    script = RUN / "inputs/worker.py"
    script.write_text(WORKER, encoding="utf-8")
    try:
        # Positive controls run first; failure must stop before a profile is created.
        launch_worker(native, None, "", script, "startup", constrained=False)
        startup = json.loads((RUN / "work/startup.json").read_text())
        if startup["version"] != [3, 14, 6] or Path(startup["prefix"]) != STAGE / "runtime":
            raise RuntimeError("Staged interpreter identity mismatch")
        endpoints = []
        for family, host in ((socket.AF_INET, "127.0.0.1"), (socket.AF_INET6, "::1")):
            for kind in (socket.SOCK_STREAM, socket.SOCK_DGRAM):
                listener = socket.socket(family, kind)
                listeners.append(listener)
                listener.bind((host, 0))
                listener.settimeout(0.5)
                if kind == socket.SOCK_STREAM:
                    listener.listen(1)
                endpoints.append({"family": int(family), "kind": int(kind), "host": host,
                                      "port": listener.getsockname()[1]})
        (RUN / "inputs/endpoints.json").write_text(json.dumps(endpoints))

        def observed_markers():
            observed = []
            for listener in listeners:
                try:
                    if listener.type == socket.SOCK_STREAM:
                        connection, _ = listener.accept()
                        with connection:
                            connection.settimeout(0.5)
                            marker = connection.recv(16)
                    else:
                        marker, _ = listener.recvfrom(16)
                    observed.append(marker == b"T09")
                except TimeoutError:
                    observed.append(False)
            return observed

        launch_worker(native, None, "", script, "network", constrained=False)
        positive = json.loads((RUN / "work/network.json").read_text())
        delivered = observed_markers()
        receipt("positive-network.json", {"results": positive, "observed": delivered})
        if not all(delivered) or any(item["error"] != 0 for item in positive["attempts"]):
            raise RuntimeError("Positive native network control inconclusive")
        memory_ready()
        error = native.userenv.CreateAppContainerProfile(
            profile, profile, "Approved synthetic T09 preflight", None, 0, ctypes.byref(sid))
        result["create_profile_hresult"] = f"{error & 0xFFFFFFFF:08x}"
        if error < 0:
            raise OSError(f"CreateAppContainerProfile HRESULT {error & 0xFFFFFFFF:08x}")
        created = True
        result["profile_created"] = True
        sid_string = native.sid_text(sid)
        native.profile_path = profile_folder(native, sid_string)
        bounded_tree_bytes(native.profile_path, 128 * 1024**2)
        result["sid"] = sid_string
        receipt("profile-ownership.json", {"profile": profile, "sid": sid_string,
                                                "created": True})
        grants = [(STAGE / "runtime", "runtime"), (RUN / "inputs", "inputs"),
                  (RUN / "work", "work")]
        ancestors = set()
        for path, _ in grants:
            for ancestor in path.parents:
                if ancestor == ROOT or ancestor.is_relative_to(ROOT):
                    ancestors.add(ancestor)
        for ancestor in sorted(ancestors, key=lambda item: len(item.parts)):
            if ancestor not in {path for path, _ in grants}:
                grants.insert(0, (ancestor, "traverse"))
        for path, role in grants:
            contained(ROOT, path)
            before = security_text(path)
            if sid_string in before:
                raise RuntimeError("Unexpected preexisting SID grant")
            rights = grant_rights(role)
            ace = f"*{sid_string}:" + ("(X,RA)" if role == "traverse"
                                       else f"(OI)(CI)({rights})")
            change = {"path": str(path), "role": role, "before": before, "applied": True}
            changes.append(change)
            acl_command(native, str(path), "/grant", ace)
            change["after"] = security_text(path)
            receipt("grants.json", changes)
        result["work_label_before"] = security_text(RUN / "work")
        result["work_low_label"] = True
        acl_command(native, str(RUN / "work"), "/setintegritylevel", "(OI)(CI)L")
        for mode in ("startup", "files", "network", "child", "timeout"):
            if mode == "child":
                reserve("restricted child creation negative attempt")
            launch_worker(native, sid, sid_string, script, mode, constrained=True,
                          expected_timeout=mode == "timeout")
            if mode == "network":
                negative = json.loads((RUN / "work/network.json").read_text())
                delivered = observed_markers()
                receipt("negative-network.json", {"results": negative, "observed": delivered})
                if len(negative["attempts"]) != 4 or not all(
                    native_denied(item["error"], seen)
                    for item, seen in zip(negative["attempts"], delivered, strict=True)
                ):
                    raise RuntimeError("Native network denial inconclusive")
            if (RUN / "inputs/marker.txt").read_text() != "synthetic-marker":
                raise RuntimeError("Read-only input was modified")
        result["status"] = "synthetic_preflight_passed_no_ocr"
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        result["status"] = "stopped"
        result["error"] = f"{type(error).__name__}: {error}"
    finally:
        for listener in listeners:
            listener.close()
        cleanup_errors = []
        for change in reversed(changes):
            if change["applied"]:
                try:
                    contained(ROOT, Path(change["path"]))
                    acl_command(native, change["path"], "/remove:g", f"*{sid_string}")
                    if sid_string in security_text(Path(change["path"])):
                        raise RuntimeError("SID grant remains")
                except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
                    cleanup_errors.append(str(error))
        if result.get("work_low_label"):
            try:
                restore_work_label(result["work_label_before"])
            except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
                cleanup_errors.append(str(error))
        if owns_profile(profile, RUN_ID, created):
            error = native.userenv.DeleteAppContainerProfile(profile)
            result["delete_profile_hresult"] = f"{error & 0xFFFFFFFF:08x}"
            if error < 0 or (getattr(native, "profile_path", None)
                             and native.profile_path.exists()):
                cleanup_errors.append("Profile storage removal incomplete")
        if sid:
            native.advapi.FreeSid(sid)
        result["cleanup_errors"] = cleanup_errors
        result["controller_accounting"] = native.accounting(controller_job)
        receipt("result.json", result)
        print(json.dumps(result, indent=2))
    if result["status"] == "stopped" or cleanup_errors:
        raise RuntimeError("Preflight stopped; preserve result.json; no automatic retry")
