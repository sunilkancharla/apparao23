"""IF-R one-shot public metadata inspection. No model execution or network calls."""

import hashlib
import json
import os
import stat
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path, PurePath

REPO = Path(__file__).absolute().parents[3]
ROOT = REPO / "data/ollama/models"
RUN = REPO / "data/t17/input-fit-inspection-01"
PYTHON = Path("F:/Python/Python314/python.exe")
FILE_LIMIT = 65536
TOTAL_LIMIT = 1048576
MANIFESTS = "manifests-v2/ollama.com/library/"
INVENTORY = (
    (
        "qwen_manifest",
        MANIFESTS + "qwen2.5/1.5b-instruct-q4_K_M",
        857,
        "65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b",
    ),
    (
        "nomic_manifest",
        MANIFESTS + "nomic-embed-text/v1.5",
        708,
        "0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f",
    ),
    (
        "qwen_config",
        "blobs/sha256-377ac4d7aeefd5b870c9fccff9a6d4df36901d99fe3277c2f755bc401601ba1c",
        487,
        "377ac4d7aeefd5b870c9fccff9a6d4df36901d99fe3277c2f755bc401601ba1c",
    ),
    (
        "qwen_system",
        "blobs/sha256-66b9ea09bd5b7099cbb4fc820f31b575c0366fa439b08245566692c6784e281e",
        68,
        "66b9ea09bd5b7099cbb4fc820f31b575c0366fa439b08245566692c6784e281e",
    ),
    (
        "qwen_template",
        "blobs/sha256-eb4402837c7829a690fa845de4d7f3fd842c2adee476d5341da8a46ea9255175",
        1482,
        "eb4402837c7829a690fa845de4d7f3fd842c2adee476d5341da8a46ea9255175",
    ),
    (
        "qwen_license",
        "blobs/sha256-832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e",
        11343,
        "832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e",
    ),
    (
        "nomic_config",
        "blobs/sha256-31df23ea7daa448f9ccdbbcecce6c14689c8552222b80defd3830707c0139d4f",
        420,
        "31df23ea7daa448f9ccdbbcecce6c14689c8552222b80defd3830707c0139d4f",
    ),
    (
        "nomic_params",
        "blobs/sha256-ce4a164fc04605703b485251fe9f1a181688ba0eb6badb80cc6335c0de17ca0d",
        17,
        "ce4a164fc04605703b485251fe9f1a181688ba0eb6badb80cc6335c0de17ca0d",
    ),
    (
        "nomic_license",
        "blobs/sha256-c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4",
        11357,
        "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4",
    ),
)


class Boundary(RuntimeError):
    """Refuse missing, changed, excessive or incomplete evidence."""


def ancestors(root: PurePath, target: PurePath) -> tuple[PurePath, ...]:
    """Return a finite drive-to-file chain, rejecting lexical escapes/non-progress."""
    if not root.is_absolute() or not target.is_absolute():
        raise Boundary("Absolute paths required")
    if ".." in root.parts or ".." in target.parts or len(target.parts) > 64:
        raise Boundary("Path boundary")
    try:
        relative = target.relative_to(root)
    except ValueError:
        raise Boundary("Outside root") from None
    chain = (*reversed(tuple(target.parents)), target)
    if not relative.parts or len(chain) > 64 or len(set(chain)) != len(chain):
        raise Boundary("Non-progress or excessive ancestry")
    return chain


def check_type(info: os.stat_result, directory: bool) -> None:
    """Reject links/reparse points and unexpected filesystem types."""
    if getattr(info, "st_file_attributes", 0) & 0x400:
        raise Boundary("Reparse point")
    expected = stat.S_ISDIR if directory else stat.S_ISREG
    if not expected(info.st_mode):
        raise Boundary("Unexpected file type")


def checked_file(root: Path, target: Path) -> os.stat_result:
    """Inspect every ancestor; this is not race-free filesystem confinement."""
    chain = ancestors(root, target)
    for index, path in enumerate(chain):
        info = path.lstat()
        check_type(info, index < len(chain) - 1)
    return info


def identity(info: os.stat_result) -> tuple[int, ...]:
    """Compare file identity and observable mutations before and after reading."""
    return tuple(
        getattr(info, key)
        for key in (
            "st_dev",
            "st_ino",
            "st_size",
            "st_mtime_ns",
            "st_ctime_ns",
            "st_mode",
            "st_nlink",
        )
    )


def persist(path: Path, value: dict) -> None:
    """Flush a bounded JSON receipt before atomic replacement in the owned root."""
    for parent in ancestors(REPO, path)[:-1]:
        check_type(parent.lstat(), True)
    if path.exists():
        check_type(path.lstat(), False)
    raw = json.dumps(value, ensure_ascii=True, sort_keys=True).encode("utf-8")
    if len(raw) > 131072:
        raise Boundary("Receipt size")
    temporary = path.with_suffix(path.suffix + ".pending")
    with temporary.open("xb") as output:
        output.write(raw)
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)


def read_one(root: Path, item: tuple, state: dict, save: Callable) -> bytes:
    """Read one pinned file once; conservatively charge the full bounded read."""
    role, relative, size, digest = item
    record = {"role": role, "status": "started"}
    state["files"].append(record)
    save(state)
    try:
        if state["charged_bytes"] + FILE_LIMIT + 1 > TOTAL_LIMIT:
            raise Boundary("Aggregate read cap")
        if not 0 <= size <= FILE_LIMIT:
            raise Boundary("Declared size cap")
        path = root / relative
        before = checked_file(root, path)
        if before.st_size != size:
            raise Boundary("Declared size mismatch")
        state["charged_bytes"] += FILE_LIMIT + 1
        save(state)
        with path.open("rb") as stream:
            if identity(os.fstat(stream.fileno())) != identity(before):
                raise Boundary("Changed open identity")
            raw = stream.read(FILE_LIMIT + 1)
            state["read_bytes"] += len(raw)
            after_handle = os.fstat(stream.fileno())
        after_path = checked_file(root, path)
        if identity(before) != identity(after_handle) or identity(before) != identity(
            after_path
        ):
            raise Boundary("Changed file identity")
        actual = hashlib.sha256(raw).hexdigest()
        record.update(length=len(raw), sha256=actual)
        if len(raw) != size or len(raw) > FILE_LIMIT or actual != digest:
            raise Boundary("Size or digest mismatch")
        record["status"] = "completed"
        save(state)
        return raw
    except Exception as error:
        record.update(status="refused", error=type(error).__name__)
        save(state)
        raise


def run_owned(
    argv: list[str], state: dict, save: Callable, spawn: Callable = subprocess.Popen
) -> dict:
    """Admit one owned child, enforce communication deadline and verify reap."""
    if state.get("actual_attempts", 0) != 0:
        raise Boundary("One attempt only")
    state.update(actual_attempts=1, status="launching", reaped=False)
    save(state)
    try:
        process = spawn(
            argv,
            shell=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as error:
        state.update(
            status="stopped_no_retry",
            error=type(error).__name__,
            reaped=True,
            child_created=False,
        )
        save(state)
        raise
    started = time.monotonic()
    try:
        state.update(status="running", pid=process.pid)
        save(state)
        output, errors = process.communicate(timeout=30)
        state.update(
            reaped=True,
            exit_code=process.returncode,
            stdout_bytes=len(output),
            stderr_bytes=len(errors),
        )
        if len(output) > FILE_LIMIT or errors or process.returncode != 0:
            raise Boundary("Worker output or exit")
        try:
            result = json.loads(output)
        except (ValueError, UnicodeError):
            raise Boundary("Malformed worker result") from None
        if result != {"status": "complete", "files": 9}:
            raise Boundary("Incomplete worker result")
        state["status"] = "complete"
        return result
    except Exception as error:
        state.update(status="stopped_no_retry", error=type(error).__name__)
        if not state["reaped"]:
            try:
                process.kill()
                state["exit_code"] = process.wait(timeout=5)
                state["reaped"] = True
            except (OSError, subprocess.TimeoutExpired) as cleanup_error:
                state["cleanup_error"] = type(cleanup_error).__name__
        if isinstance(error, subprocess.TimeoutExpired):
            raise Boundary("Worker deadline") from None
        raise
    finally:
        # A failed reap may leave communicate's Windows reader threads blocked.
        # Do not block the controller again by closing their live pipe handles.
        if state["reaped"] and process.stdout is not None:
            process.stdout.close()
        if state["reaped"] and process.stderr is not None:
            process.stderr.close()
        state["communication_seconds"] = time.monotonic() - started
        save(state)


def worker() -> None:
    """Read only the nine pinned public files; emit a small content-free packet."""
    state = {"charged_bytes": 0, "read_bytes": 0, "files": []}
    findings = {}
    for item in INVENTORY:
        raw = read_one(
            ROOT, item, state, lambda value: persist(RUN / "progress.json", value)
        )
        findings[item[0]] = raw.decode("utf-8")
    persist(RUN / "findings.json", findings)
    print('{"status":"complete","files":9}', flush=True)


def controller() -> None:
    """Consume the fresh sealed allocation; never reset it or start a second child."""
    meter_path = RUN / "meter.json"
    meter = json.loads(meter_path.read_text(encoding="utf-8-sig"))
    elapsed = time.perf_counter() - meter["started_qpc"] / meter["frequency"]
    if (
        meter["status"] != "active"
        or meter["actual_attempts"] != 0
        or not 0 <= elapsed < 1165
    ):
        raise Boundary("Closed or expired allocation")
    ready = json.loads((RUN / "ready.json").read_text(encoding="utf-8-sig"))
    if ready.get("controls_passed") is not True:
        raise Boundary("Missing controls")
    for filename, expected in ready["seals"].items():
        # Only explicitly approved aid/interpreter seals, never model weight paths.
        if filename not in (
            str(Path(__file__).absolute()),
            str(PYTHON),
            str(Path(__file__).with_name("test_input_fit_metadata.py").absolute()),
        ):
            raise Boundary("Unexpected seal target")
        with Path(filename).open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        if actual != expected:
            raise Boundary("Changed seal")
    if len(ready["seals"]) != 3:
        raise Boundary("Missing seals")
    meter["actual_attempts"] = 1
    persist(meter_path, meter)
    with (RUN / "attempt.claim").open("xb") as claim:
        claim.write(b"one attempt; never retry")
        claim.flush()
        os.fsync(claim.fileno())
    state = {"actual_attempts": 0}
    run_owned(
        [str(PYTHON), "-I", "-S", "-B", str(Path(__file__).absolute()), "worker"],
        state,
        lambda value: persist(RUN / "controller.json", value),
    )
    print(
        json.dumps(
            {
                "status": state["status"],
                "reaped": state["reaped"],
                "exit_code": state["exit_code"],
            }
        )
    )


if __name__ == "__main__":
    try:
        if sys.argv[1:] == ["worker"]:
            worker()
        elif sys.argv[1:] == ["controller"]:
            controller()
        else:
            raise Boundary("Explicit dispatch required")
    except (OSError, ValueError, Boundary, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "stopped_no_retry", "error": type(error).__name__}))
        sys.exit(1)
