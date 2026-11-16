"""IF-J bind the verified unchanged synthetic probe to one fresh allocation."""

import hashlib
import json
import os
import sys
import time
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

REPO = Path(__file__).absolute().parents[3]
RUN = REPO / "data/t17/windows-identity-02"
SOURCE = Path(__file__).with_name("windows_file_identity.py")
SOURCE_HASH = "7c62c7e58d7bb4e7fbd9501390e2dfbf6b97d560c99425db50003a2348775856"


class Boundary(RuntimeError):
    """Refuse missing, changed, closed or outside allocation inputs."""


def load_probe() -> ModuleType:
    """Compile exactly the verified authored bytes without old main dispatch."""
    with SOURCE.open("rb") as stream:
        raw = stream.read(16385)
    if len(raw) > 16384 or hashlib.sha256(raw).hexdigest() != SOURCE_HASH:
        raise Boundary("Changed authored probe")
    module = ModuleType("verified_synthetic_probe")
    module.__file__ = str(SOURCE)
    exec(compile(raw, str(SOURCE), "exec"), module.__dict__)  # noqa: S102 -- exact hash-verified authored source
    return module


def claim_probe(root: Path) -> None:
    """Exclusively consume the probe invocation before calling its implementation."""
    with (root / "probe.claim").open("xb") as output:
        output.write(b"one probe only")
        output.flush()
        os.fsync(output.fileno())


def execute(
    root: Path,
    meter: dict,
    controller_claim: bytes,
    now: float,
    output_bytes: int,
    loader: Callable = load_probe,
    claim: Callable = claim_probe,
):
    """Admit the sole fresh root, bind both probe and persistence, propagate errors."""
    if root != RUN:
        raise Boundary("Fresh02root only")
    try:
        elapsed = now - meter["started_qpc"] / meter["frequency"]
        allowed = meter["status"] == "active" and meter["probe_attempts"] == 1
    except (KeyError, TypeError, ZeroDivisionError):
        raise Boundary("Missing allocation") from None
    if (
        not allowed
        or controller_claim != b"IF-J"
        or not 0 <= elapsed < 1140
        or not 0 <= output_bytes < 917504
    ):
        raise Boundary("Admission boundary")
    module = loader()
    claim(root)
    module.RUN = root
    return module.probe(root, module.persist)


if __name__ == "__main__":
    try:
        if sys.argv[1:] != ["probe"]:
            raise Boundary("Explicit probe dispatch")
        meter = json.loads((RUN / "meter.json").read_text(encoding="utf-8-sig"))
        with (RUN / "controller.claim").open("rb") as stream:
            controller_claim = stream.read(16)
        output_bytes = sum(
            path.stat().st_size for path in RUN.iterdir() if path.is_file()
        )
        execute(RUN, meter, controller_claim, time.perf_counter(), output_bytes)
        print('{"status":"complete"}', flush=True)
    except (OSError, ValueError, RuntimeError) as error:
        print(
            json.dumps({"status": "stopped_no_retry", "error": type(error).__name__}),
            flush=True,
        )
        sys.exit(1)
