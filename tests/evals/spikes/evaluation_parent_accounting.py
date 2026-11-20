"""WSP accounting correction controls; no candidate or application execution."""

import ctypes
import hashlib
import json
import os
import stat
import subprocess
import sys
import threading
import time
import types
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "data/t17/parent-accounting-correction-01"
GATE_SOURCE = ROOT / "tests/evals/spikes/tokenizer_wheel_source_review.py"
GATE_SHA = "f5896770a58f41c5ac579c18d4cdbbfa7065c5361cf30bcc55ef8dd158a7d035"


def load_report_gate() -> type:
    """Bind frozen project-owned bytes; return only their reporting class."""
    before = GATE_SOURCE.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise ValueError("gate_type")
    if getattr(before, "st_file_attributes", 0) & 1024:
        raise ValueError("gate_reparse")
    with GATE_SOURCE.open("rb") as handle:
        opened = os.fstat(handle.fileno())
        raw = handle.read(11015)
        after = os.fstat(handle.fileno())
    identity = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    for value in (opened, after, GATE_SOURCE.lstat()):
        if (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns) != identity:
            raise ValueError("gate_changed")
    if len(raw) != 11014 or hashlib.sha256(raw).hexdigest() != GATE_SHA:
        raise ValueError("gate_hash")
    module = types.ModuleType("mtr_frozen_report")
    module.__file__ = str(GATE_SOURCE)
    sys.modules[module.__name__] = module
    # This is verified project-owned code, never candidate source.
    exec(compile(raw, str(GATE_SOURCE), "exec"), module.__dict__)  # noqa: S102
    return module.ReportGate


@dataclass
class ParentBudget:
    """Model the parent's complete launch envelopes and protected report reserve."""

    starts: int = 0
    displayed: int = 0
    stopped: bool = False
    ids: set[str] = field(default_factory=set)

    def admit(self, operation: str, envelope: int, *, closure: bool = False) -> None:
        """Reserve before dispatch; child counts cannot replace the full envelope."""
        if self.stopped and not closure:
            raise ValueError("stopped")
        if not operation or operation in self.ids or envelope < 2:
            raise ValueError("operation_or_envelope")
        if self.starts + envelope > (64 if closure else 52):
            raise ValueError("start_reserve")
        self.ids.add(operation)
        self.starts += envelope

    def display(self, value: object, *, closure: bool = False) -> bytes:
        """Return exactly the admitted UTF-8 serialization."""
        gate = load_report_gate()(limit=32768, reserve=8192, used=self.displayed)
        raw = gate.admit(value, closure=closure)
        if len(raw) > 2048:
            raise ValueError("report_reserve")
        self.displayed = gate.used
        return raw


def parent_receipt(root: Path, operation: str) -> dict:
    """Require exactly one parent admission rather than a fresh child budget."""
    if not operation or not operation.replace("-", "").isalnum():
        raise ValueError("operation")
    receipts = list(root.glob("receipt-*.json"))
    if len(receipts) > 32:
        raise ValueError("receipt_cap")
    matches = []
    for path in receipts:
        value = path.lstat()
        if (
            value.st_size > 4096
            or value.st_nlink != 1
            or not stat.S_ISREG(value.st_mode)
        ):
            raise ValueError("receipt_type")
        if getattr(value, "st_file_attributes", 0) & 1024:
            raise ValueError("receipt_reparse")
        record = json.loads(path.read_bytes())
        if record.get("id") == operation:
            matches.append(record)
    if len(matches) != 1 or matches[0]["envelope"] < 3:
        raise ValueError("missing_admission")
    return matches[0]


def current_test_lease() -> dict:
    """Use the invoking parent's operation, never authorize a new host call."""
    return parent_receipt(RUN, os.environ.get("MTR_OPERATION", ""))


def claim_child(root: Path, lease: dict, role: str) -> Path:
    """Atomically consume a slot from the already charged complete envelope."""
    operation, slots = lease["id"], lease["envelope"] - 2
    if not operation.replace("-", "").isalnum() or not 1 <= slots <= 6:
        raise ValueError("child_envelope")
    for index in range(slots):
        path = root / f"claim-{operation}-{index}.json"
        try:
            with path.open("x", encoding="utf-8") as handle:
                json.dump(
                    {"operation": operation, "attempt": True, "role": role}, handle
                )
            return path
        except FileExistsError:
            continue
    raise ValueError("child_envelope_exhausted")


def control(root: Path, lease: dict, scenario: str) -> dict:
    """Run one of two inert controls with direct identity and bounded capture."""
    scripts = {"ok": "print('synthetic-control')", "failure": "raise SystemExit(7)"}
    if scenario not in scripts:
        raise ValueError("unknown_control")
    claim = claim_child(root, lease, scenario)
    command = [sys.executable, "-I", "-S", "-B", "-c", scripts[scenario]]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    birth = (ctypes.c_ulonglong * 4)()
    identified = ctypes.windll.kernel32.GetProcessTimes(
        ctypes.c_void_p(int(proc._handle)),
        ctypes.byref(birth, 0),
        ctypes.byref(birth, 8),
        ctypes.byref(birth, 16),
        ctypes.byref(birth, 24),
    )
    if not identified:
        proc.kill()
        proc.wait(timeout=15)
        raise RuntimeError("child_identity")
    streams = [bytearray(), bytearray()]
    lock, overflow = threading.Lock(), threading.Event()

    def pump(index: int, stream) -> None:
        while data := stream.read(512):
            with lock:
                if sum(map(len, streams)) + len(data) > 4096:
                    overflow.set()
                    return
                streams[index].extend(data)

    threads = [
        threading.Thread(target=pump, args=(i, pipe), daemon=True)
        for i, pipe in enumerate((proc.stdout, proc.stderr))
    ]
    for thread in threads:
        thread.start()
    deadline = time.monotonic() + 5
    while proc.poll() is None and not overflow.is_set() and time.monotonic() < deadline:
        time.sleep(0.01)
    killed = proc.poll() is None
    if killed:
        proc.kill()
    proc.wait(timeout=15)
    for thread in threads:
        thread.join(timeout=15)
    result = {
        "pid": proc.pid,
        "birth_filetime": int(birth[0]),
        "exit": proc.returncode,
        "eof": not any(thread.is_alive() for thread in threads),
        "reaped": proc.poll() is not None,
        "overflow": overflow.is_set(),
        "killed": killed,
        "stdout_hex": streams[0].hex(),
        "stderr_hex": streams[1].hex(),
    }
    claim.with_name(claim.stem + "-capture.json").write_text(
        json.dumps(result), encoding="utf-8"
    )
    if killed or overflow.is_set() or not result["eof"]:
        raise RuntimeError("child_capture_or_teardown")
    return result
