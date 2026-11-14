"""Shared accounting and static preparation for the approved T11 experiment."""

from __future__ import annotations

import hashlib
import json
import math
import os
import stat
import sys
import threading
import time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "data/t11/combined-04"
PRIOR = ROOT / "data/t09-manual-ocr/manual-04"
SPIKES = Path(__file__).resolve().parent
sys.path.insert(0, str(SPIKES))
CATEGORIES = {
    "preparation": 48,
    "controller": 16,
    "ocr": 28,
    "supervisor": 36,
    "report": 16,
    "cleanup": 16,
}
CHAT_MODELS = {
    "qwen2.5:1.5b-instruct-q4_K_M": "65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b",
    "qwen3:1.7b-q4_K_M": "8f68893c685c3ddff2aa3fffce2aa60a30bb2da65ca488b61fff134a4d1730e7",
}
EMBED = "nomic-embed-text:v1.5"
MODELS = {
    EMBED: "0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f",
    **CHAT_MODELS,
}
EXECUTABLE = ROOT / ".venv/tools/ollama/0.40.16/ollama.exe"
PYTHON = Path("F:/Python/Python314/python.exe")
_MUTEX = threading.RLock()


def configure_run(run_id: str) -> None:
    """Select only the newly approved allocation; old commands must not redirect."""
    global RUN
    if run_id != "combined-04":
        raise ValueError("Unapproved or stopped combined run ID")
    RUN = ROOT / "data/t11" / run_id


def state_error_field(error: BaseException) -> str | None:
    """Expose known meter keys only, never arbitrary exception/document content."""
    allowed = {
        "execution_deadline",
        "execution_deadline_utc",
        "offline_started",
        "limits",
        "categories",
        "processes",
        "calls",
    }
    if isinstance(error, KeyError) and error.args and isinstance(error.args[0], str):
        return error.args[0] if error.args[0] in allowed else None
    return None


def live_tree_bytes(root: Path, cap: int) -> int:
    """Observe live storage, tolerating vanished descendants but never missing roots.

    This is a sampled guard, not a kernel disk quota or filesystem confinement.
    Static/isolation trials retain their original strict counter.
    """
    from appcontainer_preflight import regular_attributes

    if cap < 0:
        raise ValueError("Negative storage cap")

    def directory_info(path: Path):
        info = path.lstat()
        if (
            not regular_attributes(getattr(info, "st_file_attributes", 0))
            or stat.S_ISLNK(info.st_mode)
            or not stat.S_ISDIR(info.st_mode)
        ):
            raise RuntimeError("Unsafe or non-directory live storage root")
        return info

    original = directory_info(root)

    def walk_error(error: OSError) -> None:
        if isinstance(error, FileNotFoundError) and error.filename:
            try:
                relative = Path(error.filename).absolute().relative_to(root.absolute())
            except ValueError:
                raise error from None
            if relative.parts and ".." not in relative.parts:
                return  # The enumerated descendant no longer occupies storage.
        raise error

    total = 0
    for current, directories, files in os.walk(
        root, followlinks=False, onerror=walk_error
    ):
        current_path = Path(current)
        try:
            directory_info(current_path)
        except FileNotFoundError:
            if current_path == root:
                raise
            directories.clear()
            continue
        for name in [*directories, *files]:
            item = current_path / name
            try:
                info = item.lstat()
            except FileNotFoundError:
                if name in directories:
                    directories.remove(name)
                continue
            if not regular_attributes(
                getattr(info, "st_file_attributes", 0)
            ) or stat.S_ISLNK(info.st_mode):
                raise RuntimeError("Unexpected live storage reparse point/link")
            if name in directories and not stat.S_ISDIR(info.st_mode):
                raise RuntimeError("Live directory type changed during scan")
            if stat.S_ISREG(info.st_mode):
                total += info.st_size
                if total > cap:
                    raise RuntimeError("Live storage disk cap exceeded")
    final = directory_info(root)
    if (original.st_dev, original.st_ino) != (final.st_dev, final.st_ino):
        raise RuntimeError("Live storage root replaced during scan")
    return total


def filesystem_diagnostic(error: OSError, root: Path) -> dict:
    """Classify file failures without exposing untrusted filenames or messages."""
    area = getattr(error, "trial_storage_area", "unclassified")
    if area not in {"run", "raw", "answers"}:
        area = "unclassified"
    kind = "unknown-or-outside-run"
    try:
        relative = Path(error.filename).resolve().relative_to(root.resolve())
        if relative.name in {
            "meter.json.tmp",
            "summary.json.tmp",
            "filesystem-error-local.json.tmp",
        }:
            kind = "atomic-state-temporary-file"
        elif relative.parts and relative.parts[0] in {"temp", "runtime-home"}:
            kind = "runtime-temporary-entry"
        else:
            kind = "unlisted-run-entry"
    except (OSError, TypeError, ValueError):
        pass  # Diagnostic classification must not replace the original failure.
    source = None
    owned = {
        SPIKES / name
        for name in (
            "combined_trial.py",
            "combined_native.py",
            "ocr_trial.py",
            "appcontainer_preflight.py",
        )
    }
    trace = error.__traceback__
    while trace:
        if Path(trace.tb_frame.f_code.co_filename) in owned:
            source = {
                "module": Path(trace.tb_frame.f_code.co_filename).name,
                "function": trace.tb_frame.f_code.co_name,
                "line": trace.tb_lineno,
            }
        trace = trace.tb_next
    return {
        "error_type": type(error).__name__,
        "errno": error.errno,
        "winerror": getattr(error, "winerror", None),
        "storage_area": area,
        "entry_kind": kind,
        "source": source,
    }


def record_filesystem_error(error: OSError, root: Path) -> dict:
    """Keep exact paths in an ignored local receipt, sanitized metadata in reports."""
    public = filesystem_diagnostic(error, root)
    with _MUTEX:
        try:
            write_json(
                root / "filesystem-error-local.json",
                {
                    "diagnostic": public,
                    "filename": str(error.filename)
                    if error.filename is not None
                    else None,
                    "filename2": str(error.filename2)
                    if error.filename2 is not None
                    else None,
                },
            )
        except OSError:
            public["local_detail_saved"] = False
        else:
            public["local_detail_saved"] = True
    return public


def initial_state() -> dict:
    """Describe an empty test ledger, never overwrite an existing allocation."""
    return {
        "processes": 0,
        "calls": 0,
        "native_roots": 0,
        "native_extra": 0,
        "native_observed": 0,
        "execution_approved": True,
        "offline_started": None,
        "limits": dict(CATEGORIES),
        "categories": {key: 0 for key in CATEGORIES},
        "events": [],
    }


def write_json(path: Path, value: object) -> None:
    """Replace one local checkpoint atomically; startup refuses unfinished writes."""
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    os.replace(temporary, path)


class Ledger:
    """Serialize all controller/thread reservations in one persistent allocation."""

    def __init__(self, path: Path, clock=time.time):
        self.path, self.clock = path, clock
        if path.with_suffix(path.suffix + ".tmp").exists():
            raise RuntimeError("Unfinished meter write; no restart")
        if self.read()["limits"] != CATEGORIES:
            raise RuntimeError("Approved category limits changed")

    def read(self) -> dict:
        """Read only; a missing ledger is a failure, never implicit permission."""
        with _MUTEX:
            return json.loads(self.path.read_text(encoding="utf-8-sig"))

    def reserve(
        self, category: str, count: int, reason: str, *, native=False, cleanup=False
    ):
        """Reserve before launch, preserving cleanup and explicit category ceilings."""
        with _MUTEX:
            state = self.read()
            if (
                category not in CATEGORIES
                or count < 1
                or state["categories"][category] + count > CATEGORIES[category]
                or state["processes"] + count > (160 if cleanup else 144)
                or (category == "cleanup" and not cleanup)
            ):
                raise RuntimeError("Shared process/category/cleanup budget")
            state["categories"][category] += count
            state["processes"] += count
            state["native_roots"] += count if native else 0
            state["events"].append(
                {
                    "category": category,
                    "count": count,
                    "reason": reason,
                    "at": self.clock(),
                }
            )
            write_json(self.path, state)

    def observe_native(self, total: int) -> None:
        """Persist cumulative extra descendants before rejecting overshoot."""
        with _MUTEX:
            state = self.read()
            extra = max(state["native_extra"], total - state["native_roots"], 0)
            delta = extra - state["native_extra"]
            state["native_observed"] = max(total, state["native_observed"])
            state["native_extra"] = extra
            state["categories"]["supervisor"] += delta
            state["processes"] += delta
            write_json(self.path, state)
            if state["processes"] > 144 or state["categories"]["supervisor"] > 36:
                raise RuntimeError("Observed descendant/process allowance")

    def start(self) -> None:
        """Start exactly once, after sealed prerequisites and offline attestation."""
        with _MUTEX:
            state = self.read()
            if state["offline_started"] or state.get("execution_approved") is not True:
                raise RuntimeError("Run already started or unapproved")
            started = self.clock()
            deadline = datetime.fromtimestamp(started + 4500, UTC)
            state["offline_started"] = started
            state["execution_deadline"] = deadline.timestamp()
            # The reused OCR polling loop consumes ISO UTC; both views share one cutoff.
            state["execution_deadline_utc"] = deadline.isoformat()
            write_json(self.path, state)

    def remaining(self) -> float:
        """Bound the shared active execution epoch, including failures/cleanup."""
        state = self.read()
        if not state["offline_started"] or state["execution_deadline"] <= self.clock():
            raise RuntimeError("Shared execution deadline/not started")
        return state["execution_deadline"] - self.clock()

    def call(self) -> None:
        """Charge each loopback attempt once, even if transport/model work fails."""
        with _MUTEX:
            self.remaining()
            state = self.read()
            if state["calls"] >= 128:
                raise RuntimeError("Shared API allowance")
            state["calls"] += 1
            write_json(self.path, state)


def schedule() -> list[dict]:
    """Freeze 36 chat attempts, of which 24 overlap a single OCR worker."""
    output, ocr_count = [], 0
    for model in CHAT_MODELS:
        for engine in (None, "tesserocr", "rapidocr"):
            for case in ("C01", "C03", "C08"):
                for repetition in range(2):
                    ocr_case = ("M02", "M03", "M04")[ocr_count % 3] if engine else None
                    ocr_count += bool(engine)
                    output.append(
                        {
                            "id": f"S{len(output) + 1:02}",
                            "model": model,
                            "engine": engine,
                            "case": case,
                            "repeat": repetition,
                            "ocr_case": ocr_case,
                        }
                    )
    return output


class ResourceBoundary(RuntimeError):
    """Carry only scalar resource measurements and fixed guard identifiers."""

    def __init__(self, diagnostic: dict):
        self.diagnostic = diagnostic
        super().__init__("Resource boundary: " + ", ".join(diagnostic["violations"]))


def validate_interval(value: float) -> None:
    """Refuse invalid elapsed times rather than allowing NaN to bypass a guard."""
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value < 0
    ):
        raise ValueError("Invalid monitor interval")


def cadence_wait(elapsed: float) -> float:
    """Wait only the remainder of the existing 100-ms desired cadence."""
    validate_interval(elapsed)
    return max(0.0, 0.1 - elapsed)


def check_timing(timing: dict) -> None:
    """Enforce the unchanged ceiling on explicitly named measured intervals."""
    allowed = {
        "loop_start_gap",
        "reading_gap",
        "collection_seconds",
        "tcp_seconds",
        "storage_seconds",
        "iteration_seconds",
    }
    if not timing.keys() <= allowed:
        raise ValueError("Unknown monitor timing field")
    for value in timing.values():
        validate_interval(value)
    violations = [key for key, value in timing.items() if value > 0.25]
    if violations:
        raise ResourceBoundary(
            {
                "violations": violations,
                "measurement": dict(timing),
                "limits": {key: 0.25 for key in timing},
            }
        )


def check_resources(snapshot: dict, gap: float) -> None:
    """Enforce sampled headroom/commit bounds and the promised sampling interval."""
    validate_interval(gap)
    limits = {
        "available_physical": 4 * 1024**3,
        "controller_private": 512 * 1024**2,
        "owned_private": 8 * 1024**3,
        "peak_job": 8 * 1024**3,
        "sampling_gap": 0.25,
    }
    measurement = {key: snapshot[key] for key in limits if key != "sampling_gap"}
    measurement["sampling_gap"] = gap
    violations = [
        key
        for key, limit in limits.items()
        if (
            measurement[key] < limit
            if key == "available_physical"
            else measurement[key] > limit
        )
    ]
    if violations:
        raise ResourceBoundary(
            {"violations": violations, "measurement": measurement, "limits": limits}
        )


def overlap(chat: tuple[float, float], ocr: tuple[float, float]) -> float:
    """Measure actual in-flight intersection; scheduling intent is not evidence."""
    return max(0, min(chat[1], ocr[1]) - max(chat[0], ocr[0]))


def teardown_ok(
    active_children: int, reaped: bool, port_free: bool, thread_alive: bool
) -> bool:
    """A report may permit reconnection only after every owned activity ended."""
    return active_children == 0 and reaped and port_free and not thread_alive


def digest(path: Path) -> str:
    """Hash large weights incrementally without importing model/native packages."""
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def verify_file(root: Path, name: str, expected: str) -> Path:
    """Refuse URLs, traversal and identity drift before opening approved inputs."""
    from appcontainer_preflight import contained

    if ":" in name or Path(name).is_absolute():
        raise ValueError("Only contained local asset paths")
    path = contained(root, root / name)
    if digest(path) != expected:
        raise RuntimeError("Asset hash mismatch")
    return path


def validate_residency(response: dict, required: list[str]) -> None:
    """Require exact loaded identities/CPU/context; eviction is an incomplete trial."""
    models = response.get("models", [])
    by_name = {model["name"]: model for model in models}
    if len(models) != len(by_name) or set(by_name) != set(required) or len(models) > 2:
        raise RuntimeError("Required model residency changed")
    for name in required:
        model = by_name[name]
        if (
            model.get("digest", "").removeprefix("sha256:") != MODELS[name]
            or model.get("size_vram") != 0
            or model.get("context_length") != 2048
        ):
            raise RuntimeError("Loaded model identity/CPU/context mismatch")


def reconcile_questions(frozen: list[dict], questions: dict) -> None:
    """Reconcile later scope flags without changing selected wording or gold."""
    for case in frozen:
        current = questions[case["question_id"]]
        if (
            case["question"] != current["question"]
            or case["original_expected"] != current["expected"]
        ):
            raise RuntimeError("Selected question wording/gold changed")


def freeze_inputs() -> dict:
    """Reuse only frozen local evidence; never reopen sample_files or raw answers."""
    cases_path = ROOT / "data/t11a/run-01/cases.json"
    if (
        digest(cases_path)
        != "b394ff771cafd6072a3c4f7ed65ceec274fece3394c2a8aaf81f322e278c4ed9"
    ):
        raise RuntimeError("Frozen case identity changed")
    cases = json.loads(cases_path.read_bytes())
    corpus_path = ROOT / "data/t10/run-01/corpus.json"
    corpus = json.loads(corpus_path.read_bytes())
    if (
        cases["source_sha256"] != corpus["source_hashes"]
        or len(corpus["passages"]) != 32
        or digest(SPIKES / "chat_cases.json") != cases["definitions_sha256"]
    ):
        raise RuntimeError("Frozen evidence/definition identity changed")
    selected = [case for case in cases["cases"] if case["id"] in {"C01", "C03", "C08"}]
    question_path = ROOT / "tests/evals/questions.json"
    questions = {
        q["id"]: q for q in json.loads(question_path.read_bytes())["questions"]
    }
    reconcile_questions(selected, questions)
    if len(selected) != 3 or next(c for c in selected if c["id"] == "C08")["evidence"]:
        raise RuntimeError("Case coverage/empty-evidence control changed")
    return {
        "cases": selected,
        "corpus": corpus,
        "question_identity": {
            "historical_file_sha256": cases["question_sha256"],
            "current_file_sha256": digest(question_path),
            "selected_wording_and_gold_equal": True,
        },
        "source_files": [cases_path, corpus_path, question_path],
    }


def prepare() -> None:
    """Static connected preparation: stdlib hashes only, never native inference."""
    import ocr_trial as ocr

    ledger = Ledger(RUN / "meter.json")
    if ledger.read()["offline_started"] or (RUN / "seal.json").exists():
        raise RuntimeError("Do not reseal or restart a prepared run")
    state = ocr.verify_artifacts()
    if state != json.loads((PRIOR / "prepared-state.json").read_bytes()):
        raise RuntimeError("Installed OCR baseline/project changed")
    prior = json.loads((PRIOR / "summary.json").read_bytes())
    if (
        prior["status"] != "completed_pending_quality_review_no_adoption"
        or not prior["teardown_verified"]
    ):
        raise RuntimeError("Prior OCR trial incomplete/cleanup unknown")
    inputs = freeze_inputs()
    write_json(
        RUN / "inputs.json", {k: v for k, v in inputs.items() if k != "source_files"}
    )
    files = [
        *inputs["source_files"],
        RUN / "inputs.json",
        ROOT / "pyproject.toml",
        ROOT / "uv.lock",
        ROOT / ".venv/pyvenv.cfg",
    ]
    files += [
        SPIKES / name
        for name in (
            "combined_trial.py",
            "combined_native.py",
            "test_combined_trial.py",
            "ocr_trial.py",
            "appcontainer_preflight.py",
            "chat_trial.py",
            "embedding_trial.py",
            "embedding_budget.py",
            "chat_cases.json",
        )
    ]
    files += [Path(path) for path in state["artifacts"].values()]
    files += [
        ROOT / "docs/proposals/ocr-trial-artifacts.json",
        Path(state["flatbuffers_companion"]),
    ]
    fixture_manifest = PRIOR / "fixtures/manifest.json"
    manifest = json.loads(fixture_manifest.read_bytes())
    files.append(fixture_manifest)
    for case_id in ("M02", "M03", "M04"):
        entry = next(
            row for row in manifest["files"] if row["filename"] == case_id + ".png"
        )
        files.append(
            verify_file(PRIOR / "fixtures", entry["filename"], entry["sha256"])
        )
    for model, expected in MODELS.items():
        name, tag = model.split(":", 1)
        manifest_path = (
            ROOT / "data/ollama/models/manifests-v2/ollama.com/library" / name / tag
        )
        if digest(manifest_path) != expected:
            raise RuntimeError("Pinned model manifest drift")
        model_manifest = json.loads(manifest_path.read_bytes())
        files.append(manifest_path)
        for layer in [model_manifest["config"], *model_manifest["layers"]]:
            sha = layer["digest"].removeprefix("sha256:")
            blob = verify_file(ROOT / "data/ollama/models/blobs", "sha256-" + sha, sha)
            if blob.stat().st_size != layer["size"]:
                raise RuntimeError("Model layer size changed")
            files.append(blob)
    if (
        digest(EXECUTABLE)
        != "4ccefcbfecc50fb6526471adabbc20869dd614e29e351120b15083cb174b0b8a"
    ):
        raise RuntimeError("Pinned executable drift")
    files += [path for path in EXECUTABLE.parent.rglob("*") if path.is_file()]
    # Runtime metadata is local configuration, not proof of available model weights.
    files += [
        path
        for path in (ROOT / "data/ollama/models/metadata").rglob("*")
        if path.is_file()
    ]
    prior_hashes = {}
    for name, path in ledger.read()["prior_ledgers"].items():
        file = ROOT / path
        prior_hashes[name] = {"path": path, "sha256": digest(file)}
        files.append(file)
    write_json(RUN / "prior-ledgers.json", prior_hashes)
    files.append(RUN / "prior-ledgers.json")
    launcher = """# Approved combined synthetic-only trial; no filesystem confinement.
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath 'F:\\document_assistant'
Write-Host 'Disconnect Wi-Fi, Ethernet, tethering and every external link. Keep disconnected until teardown is verified.'
& 'F:\\Python\\Python314\\python.exe' -I -S -B tests/evals/spikes/combined_trial.py offline
if ($LASTEXITCODE -ne 0) { Write-Host 'Inspect local summary; remain disconnected unless teardown is verified.' }
"""
    launcher = launcher.replace(
        "combined_trial.py offline", "combined_trial.py offline " + RUN.name
    )
    (RUN / "run.ps1").write_text(launcher, encoding="utf-8")
    files.append(RUN / "run.ps1")
    hashes = {str(path.relative_to(ROOT)): digest(path) for path in set(files)}
    external = {
        str(path): digest(path) for path in (PYTHON, PYTHON.with_name("python314.dll"))
    }
    write_json(RUN / "seal.json", {"files": hashes, "python": external})
    print(
        f"Static preparation verified {len(hashes)} sealed files; no native import/run or download."
    )


def verify_seal() -> None:
    """Recheck immutable source/assets before starting any native process."""
    seal = json.loads((RUN / "seal.json").read_bytes())
    for name, expected in seal["files"].items():
        verify_file(ROOT, name, expected)
    for name, expected in seal["python"].items():
        if (
            Path(name) not in {PYTHON, PYTHON.with_name("python314.dll")}
            or digest(Path(name)) != expected
        ):
            raise RuntimeError("Interpreter identity changed")


if __name__ == "__main__":
    # Keep the selected allocation identical in the CLI and lazily imported native adapter.
    sys.modules["combined_trial"] = sys.modules[__name__]
    arguments = sys.argv[1:]
    if len(arguments) == 2 and arguments[0] in {"prepare", "offline"}:
        configure_run(arguments[1])
    elif len(arguments) == 2 and arguments[0] == "worker":
        configure_run(Path(arguments[1]).parent.parent.name)
    else:
        raise SystemExit(
            "Expected prepare/offline combined-04 or worker <local request>"
        )
    if arguments[0] == "prepare":
        prepare()
    elif arguments[0] == "offline":
        from combined_native import offline_main

        offline_main()
    else:
        from combined_native import worker

        worker(Path(sys.argv[2]))
