"""Exercise launch ordering and handle cleanup through a fake Win32 DLL surface."""

import ctypes as c
import struct
from pathlib import Path

import pytest

import app.windows_job as native
from app.ollama import OllamaError


class Function:
    def __init__(self, call):
        self.call = call

    def __call__(self, *args):
        return self.call(*args)


class Library:
    def __init__(self, methods):
        self.methods = methods

    def __getattr__(self, name):
        if name not in self.methods:
            raise AssertionError(f"Unexpected native API: {name}")
        return self.methods[name]


@pytest.fixture
def win32(monkeypatch):
    events = []
    state = {"created": False, "terminated": False, "total": 1, "resume": 1}
    limits = native.ExtendedLimits()

    def memory(pointer):
        item = c.cast(pointer, c.POINTER(native.MemoryStatus)).contents
        item.values[0], item.values[1] = 16 * 1024**3, 8 * 1024**3
        return 1

    def private(handle, pointer, size):
        c.cast(pointer, c.POINTER(native.ProcessMemory)).contents.values[8] = (
            100_000_000
        )
        return 1

    def set_limits(handle, kind, pointer, size):
        c.memmove(c.byref(limits), pointer, size)
        assert limits.basic.flags == 0x2208 and limits.basic.active == 8
        assert limits.job_memory == 8 * 1024**3 - 100_000_000
        events.append("limits")
        return 1

    def query(handle, kind, pointer, size, written):
        if kind == 9:
            c.memmove(pointer, c.byref(limits), size)
        elif kind == 1:
            item = c.cast(pointer, c.POINTER(native.Accounting)).contents
            item.total = state["total"] if state["created"] else 0
            item.active = int(state["created"] and not state["terminated"])
        elif kind == 3:
            item = c.cast(pointer, c.POINTER(native.Pids)).contents
            item.assigned = item.listed = 1
            item.ids[0] = 123
        else:
            raise AssertionError(kind)
        return 1

    def attributes(buffer, count, flags, pointer):
        c.cast(pointer, c.POINTER(c.c_size_t)).contents.value = 128
        return int(buffer is not None)

    def update(buffer, flags, key, handles, size, previous, returned):
        assert key == 0x2000D and handles[0] == 77
        events.append("job_attribute")
        return 1

    def create(
        executable,
        command,
        process_sec,
        thread_sec,
        inherit,
        flags,
        environment,
        directory,
        startup,
        pointer,
    ):
        assert not inherit and flags == 0x08080404
        assert command.value.endswith(" serve")
        assert c.cast(startup, c.POINTER(native.StartupInfoEx)).contents.attributes
        assert events[-1] == "job_attribute"
        info = c.cast(pointer, c.POINTER(native.ProcessInfo)).contents
        info.process, info.thread, info.pid, info.tid = 88, 99, 123, 124
        state["created"] = True
        events.append("created_in_job")
        return 1

    def resume(handle):
        assert events[-1] == "created_in_job"
        events.append("resumed")
        return state["resume"]

    def exit_code(handle, pointer):
        c.cast(pointer, c.POINTER(native.w.DWORD)).contents.value = 259
        return 1

    def terminate(*args):
        state["terminated"] = True
        events.append("terminated_job")
        return 1

    def wait(*args):
        assert state["terminated"]
        events.append("reaped_root")
        return 0

    def close(handle):
        events.append(f"closed_{handle}")
        return 1

    methods = {
        "CreateJobObjectW": lambda *a: 77,
        "SetInformationJobObject": set_limits,
        "QueryInformationJobObject": query,
        "TerminateJobObject": terminate,
        "CloseHandle": close,
        "InitializeProcThreadAttributeList": attributes,
        "UpdateProcThreadAttribute": update,
        "DeleteProcThreadAttributeList": lambda *a: None,
        "CreateProcessW": create,
        "ResumeThread": resume,
        "GetExitCodeProcess": exit_code,
        "WaitForSingleObject": wait,
        "GlobalMemoryStatusEx": memory,
    }

    def tcp(buffer, pointer, ordered, family, kind, reserved):
        row = (
            struct.pack("<I4s", 2, bytes([127, 0, 0, 1]))
            + b"\x2c\xab\0\0"
            + bytes(8)
            + struct.pack("<I", 123)
        )
        raw = struct.pack("<I", 1) + row if family == 2 else bytes(4)
        c.cast(pointer, c.POINTER(native.w.ULONG)).contents.value = len(raw)
        if buffer is None:
            return 122
        c.memmove(buffer, raw, len(raw))
        return 0

    libraries = {
        "kernel32": Library({k: Function(v) for k, v in methods.items()}),
        "iphlpapi": Library({"GetExtendedTcpTable": Function(tcp)}),
        "psapi": Library({"GetProcessMemoryInfo": Function(private)}),
    }
    monkeypatch.setattr(native.c, "WinDLL", lambda name, **kwargs: libraries[name])
    return state, events


def test_creation_is_in_job_before_resume_and_cleanup_uses_only_owned_handles(win32):
    state, events = win32
    job = native.WindowsJob()
    job.start(Path("synthetic.exe"), {"SystemRoot": "C:/Windows"}, Path("."))
    assert job.check(11435, require_listener=True)
    job.close()
    assert events.index("created_in_job") < events.index("resumed")
    assert (
        events.index("terminated_job")
        < events.index("reaped_root")
        < events.index("closed_88")
        < events.index("closed_77")
    )
    assert job.starts == 1 and job.handle is None and state["terminated"]


def test_resume_failure_leaves_a_contained_root_that_can_be_reaped(win32):
    state, _ = win32
    state["resume"] = 0xFFFFFFFF
    job = native.WindowsJob()
    with pytest.raises(OllamaError):
        job.start(Path("synthetic.exe"), {}, Path("."))
    job.close()
    assert state["terminated"] and job.handle is None


def test_cumulative_process_count_includes_exited_descendants(win32):
    state, _ = win32
    job = native.WindowsJob()
    job.start(Path("synthetic.exe"), {}, Path("."))
    state["total"] = 17
    with pytest.raises(OllamaError, match="PROCESS_LIMIT"):
        job.check(11435, require_listener=True)
    job.close()
    assert job.starts == 17
