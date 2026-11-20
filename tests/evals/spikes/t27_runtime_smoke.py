"""Explicitly selected, source-sealed offline smoke; the S1 allocation is closed."""

import argparse
import asyncio
import hashlib
import io
import json
import math
import secrets
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, replace
from pathlib import Path

import httpx

from app.config import PROJECT_ROOT, Settings, validate_local_ancestry
from app.diagnostics import reserve_port
from app.ingestion.csv import EXTRACTION_VERSION, NORMALIZATION_VERSION, CsvExtractor
from app.ingestion.models import NormalizedExtraction
from app.ollama import OllamaError
from app.retrieval.chunking import iter_chunks
from app.runtime import OwnedRuntime
from app.storage.files import UploadStore
from app.windows_job import WindowsJob

RUN_ROOT = PROJECT_ROOT / "data/t27-runtime-smoke-01"


@dataclass(frozen=True)
class SmokePackage:
    """Fixed package identity and distinct run/seal locations, never CLI paths."""

    package_id: str
    root: Path
    seal: Path
    closed: bool = False


PACKAGES = {
    "T27-S1": SmokePackage(
        "T27-S1",
        RUN_ROOT,
        PROJECT_ROOT / "docs/proposals/t27-runtime-smoke-seal.json",
        closed=True,
    ),
    "T27-S2": SmokePackage(
        "T27-S2",
        PROJECT_ROOT / "data/t27-runtime-smoke-02",
        PROJECT_ROOT / "docs/proposals/t27-runtime-smoke-02-seal.json",
    ),
}


class Meter:
    """Fresh non-resumable ledger shared by positive, cancellation and cleanup work."""

    def __init__(
        self, root: Path, *, package_id: str = "T27-S1", clock=time.monotonic
    ) -> None:
        self.root, self.clock, self.deadline = root, clock, clock() + 180
        self.lock = threading.RLock()
        self.state = {
            "package": package_id,
            "starts_charged": 2,
            "calls": 0,
            "native_observed": {},
            "stopped": False,
            "retained_charged": 65_536,
            "deadline": self.deadline,
            "worker_token": secrets.token_hex(16),
        }
        if (root / "ledger.json").exists() or (root / "ledger.tmp").exists():
            raise OllamaError("SMOKE_LEDGER_EXISTS")
        self.save()

    @classmethod
    def worker(cls, root: Path, token: str, *, package_id: str = "T27-S1") -> "Meter":
        """Claim the parent's one prepaid worker; never resume a completed run."""
        validate_local_ancestry(root)
        payload = (root / "ledger.json").read_bytes()
        if len(payload) > 65_536:
            raise OllamaError("SMOKE_LEDGER_INVALID")
        state = json.loads(payload)
        if state.get("package") != package_id or not secrets.compare_digest(
            str(state.get("worker_token", "")), token
        ):
            raise OllamaError("SMOKE_WORKER_REFUSED")
        with (root / "worker.claim").open("xb"):
            pass
        meter = cls.__new__(cls)
        meter.root, meter.clock, meter.deadline = (
            root,
            time.monotonic,
            state["deadline"],
        )
        meter.lock, meter.state = threading.RLock(), state
        meter.check()
        return meter

    def save(self) -> None:
        """Conservatively charge every ledger rewrite, including failed attempts."""
        content = json.dumps(self.state, sort_keys=True).encode()
        charge = len(content) + 1024
        self.state["retained_charged"] += charge
        if self.state["retained_charged"] > 2_000_000:
            self.state["stopped"] = True
            raise OllamaError("SMOKE_OUTPUT_LIMIT")
        pending = self.root / "ledger.tmp"
        pending.write_text(json.dumps(self.state, sort_keys=True), encoding="utf-8")
        pending.replace(self.root / "ledger.json")

    def check(self) -> None:
        with self.lock:
            if self.state["stopped"] or self.clock() >= self.deadline:
                self.state["stopped"] = True
                raise OllamaError("SMOKE_STOPPED")
            size = 0
            for count, path in enumerate(self.root.rglob("*"), 1):
                if count > 10_000:
                    self.state["stopped"] = True
                    raise OllamaError("SMOKE_STORAGE_LIMIT")
                validate_local_ancestry(path)
                if path.is_file():
                    size += path.stat().st_size
            if size > 64_000_000:
                self.state["stopped"] = True
                raise OllamaError("SMOKE_STORAGE_LIMIT")

    def reserve(self, label: str) -> None:
        with self.lock:
            self.check()
            if (
                label not in ("positive", "cancel")
                or label in self.state["native_observed"]
            ):
                self.state["stopped"] = True
                self.save()
                raise OllamaError("SMOKE_START_REFUSED")
            if self.state["starts_charged"] + 16 > 64:
                self.state["stopped"] = True
                self.save()
                raise OllamaError("SMOKE_START_REFUSED")
            self.state["starts_charged"] += 16
            self.state["native_observed"][label] = 0
            self.save()
            self.check()

    def observe(self, label: str, total: int) -> None:
        with self.lock:
            previous = self.state["native_observed"][label]
            self.state["starts_charged"] += max(0, total - max(16, previous))
            self.state["native_observed"][label] = max(
                self.state["native_observed"][label], total
            )
            if total > 16:
                self.state["stopped"] = True
            self.save()

    def call(self) -> None:
        with self.lock:
            self.check()
            if self.state["calls"] >= 12:
                self.state["stopped"] = True
                self.save()
                raise OllamaError("SMOKE_CALL_LIMIT")
            self.state["calls"] += 1
            self.save()
            self.check()


class CountedTransport(httpx.AsyncBaseTransport):
    def __init__(self, meter: Meter):
        self.meter = meter
        self.inner = httpx.AsyncHTTPTransport(trust_env=False, retries=0)

    async def handle_async_request(self, request):
        if request.url.host != "127.0.0.1" or request.url.port != 11435:
            raise OllamaError("SMOKE_ENDPOINT_REFUSED")
        self.meter.call()
        return await self.inner.handle_async_request(request)

    async def aclose(self):
        await self.inner.aclose()


class CountedJob:
    def __init__(self, meter: Meter, label: str):
        self.meter, self.label = meter, label
        self.meter.reserve(label)
        self.inner = WindowsJob()

    def start(self, *args):
        self.meter.check()
        return self.inner.start(*args)

    def check(self, *args, **kwargs):
        self.meter.check()
        return self.inner.check(*args, **kwargs)

    def close(self):
        try:
            self.inner.close()
        finally:
            self.meter.observe(self.label, self.inner.starts)


def check_sources(package: SmokePackage | None = None) -> None:
    """Refuse changed/missing application sources before any native constructor."""
    selected = PACKAGES["T27-S1"] if package is None else package
    manifest = json.loads(selected.seal.read_text(encoding="utf-8"))
    expected = {
        str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
        for path in (PROJECT_ROOT / "app").rglob("*.py")
    }
    expected.update(
        {"pyproject.toml", "uv.lock", "tests/evals/spikes/t27_runtime_smoke.py"}
    )
    if (
        manifest.get("package") != selected.package_id
        or set(manifest.get("sha256", {})) != expected
    ):
        raise OllamaError("SMOKE_SOURCE_MISMATCH")
    for relative in expected:
        path = PROJECT_ROOT / relative
        validate_local_ancestry(path)
        if (
            path.stat().st_size > 2_000_000
            or hashlib.sha256(path.read_bytes()).hexdigest()
            != manifest["sha256"][relative]
        ):
            raise OllamaError("SMOKE_SOURCE_MISMATCH")


async def run(meter: Meter) -> dict:
    """Two prepaid trees: tiny authored CSV embedding/query, then owned cancellation."""
    settings = replace(Settings.from_env({}), data_root=meter.root / "app")
    source = b"Name,Units\nNorth,42\nSouth,50\n"
    extraction = NormalizedExtraction(
        document_id="smoke-document",
        content_hash=hashlib.sha256(source).hexdigest(),
        filename="authored.csv",
        format="csv",
        extraction_id="smoke-extraction",
        extraction_version=EXTRACTION_VERSION,
        normalization_version=NORMALIZATION_VERSION,
        units=tuple(CsvExtractor(io.BytesIO(source), "smoke-extraction")),
    )
    chunks = tuple(iter_chunks(extraction))
    store = UploadStore(settings.data_root)
    try:
        results = {}
        for label in ("positive", "cancel"):
            meter.check()
            home = store.root / "staging" / label
            for suffix in ("", "AppData/Roaming", "AppData/Local", "tmp"):
                (home / suffix).mkdir(parents=True, exist_ok=bool(suffix))
            runtime = OwnedRuntime(
                settings,
                store,
                home,
                process_factory=lambda selected=label: CountedJob(meter, selected),
                transport=CountedTransport(meter),
            )
            if label == "positive":
                async with runtime.session() as embedder:
                    documents = await embedder.documents(chunks)
                    query = await embedder.query("How many North units?", "smoke-query")
                    if (
                        documents.space_id != query.space_id
                        or len(documents.embeddings) != 2
                        or any(
                            len(e.vector) != 768
                            or not math.isclose(
                                math.hypot(*e.vector), 1.0, abs_tol=1e-12
                            )
                            for e in (*documents.embeddings, *query.embeddings)
                        )
                    ):
                        raise OllamaError("SMOKE_VECTOR_FAILURE")
                    results.update(space_id=documents.space_id, documents=2, queries=1)
            else:
                try:
                    async with runtime.session():
                        raise asyncio.CancelledError
                except asyncio.CancelledError:
                    results["cancellation_checked"] = True
            with reserve_port(settings.ollama_port):
                pass
            if store.busy or store.recovery_pending:
                raise OllamaError("SMOKE_CLEANUP_PENDING")
            results[label + "_port_released"] = True
        runtime.verify_assets(settings)
        meter.check()
        return results
    finally:
        store.close()


def execute_worker(meter: Meter, package: SmokePackage) -> int:
    """Run only inside the parent's bounded worker with the existing shared meter."""
    result = {"package": package.package_id, "status": "failed"}
    try:
        check_sources(package)
        result.update(asyncio.run(run(meter)), status="passed")
    except (Exception, KeyboardInterrupt) as error:  # noqa: BLE001 - stop record for a manual native execution boundary
        meter.state["stopped"] = True
        result["code"] = (
            error.code if isinstance(error, OllamaError) else type(error).__name__
        )
    result["meter"] = meter.state
    content = json.dumps(result, sort_keys=True).encode()
    if len(content) > 65_536:
        raise OllamaError("SMOKE_OUTPUT_LIMIT")
    meter.state["retained_charged"] += len(content)
    meter.save()
    (meter.root / "result.json").write_bytes(content)
    print(
        json.dumps(
            {
                "package": package.package_id,
                "status": result["status"],
                "code": result.get("code"),
            }
        )
    )
    return 0 if result["status"] == "passed" else 1


def _native_teardown_status(meter: Meter, *, normal_exit: bool) -> str:
    """Identify only a normal, corroborated asset failure before native admission."""
    if (
        not normal_exit
        or meter.state.get("native_observed") != {}
        or meter.state.get("starts_charged") != 2
    ):
        return "unverified"
    if type(meter.state.get("calls")) is not int or meter.state["calls"] != 0:
        return "unverified"
    try:
        data = (meter.root / "result.json").read_bytes()
        if len(data) > 65_536:
            return "unverified"
        result = json.loads(data)
    except (OSError, ValueError, RecursionError):
        return "unverified"
    codes = {
        "OLLAMA_MISSING",
        "OLLAMA_MISMATCH",
        "MODEL_MISSING",
        "EMBEDDING_MODEL_MISMATCH",
        "MODEL_INCOMPLETE",
    }
    if (
        isinstance(result, dict)
        and result.get("package") == meter.state["package"]
        and result.get("status") == "failed"
        and isinstance(result.get("code"), str)
        and result["code"] in codes
    ):
        return "not_started"
    return "unverified"


def supervise(meter: Meter, arguments: list[str], *, start=None) -> int:
    """Independently bound the worker's wall time/output and kill its owned handle."""
    if start is None:
        start = subprocess.Popen
    process = start(
        arguments,
        cwd=PROJECT_ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        creationflags=0x08000000,
    )
    output, exceeded = bytearray(), threading.Event()

    def drain():
        while block := process.stdout.read(8192):
            if len(output) + len(block) > 65_536:
                exceeded.set()
                process.kill()
                break
            output.extend(block)

    thread = threading.Thread(target=drain, daemon=True)
    result, normal_exit = 1, False
    try:
        thread.start()
        result = process.wait(timeout=max(0.001, meter.deadline - time.monotonic()))
        normal_exit = result in (0, 1)
    except (subprocess.TimeoutExpired, KeyboardInterrupt):
        process.kill()
        process.wait(timeout=5)
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        thread.join(timeout=2)
        process.stdout.close()
        (meter.root / "worker-output.txt").write_bytes(output)
    if thread.is_alive() or exceeded.is_set():
        result = 1
        normal_exit = False
    if result != 0:
        # The worker is reaped; retain its latest charges rather than the parent's
        # bootstrap snapshot. Native teardown after a hard kill stays unverified.
        meter.state = json.loads(
            (meter.root / "ledger.json").read_text(encoding="utf-8")
        )
        meter.state["stopped"] = True
        meter.save()
        (meter.root / "parent-stop.json").write_text(
            json.dumps(
                {
                    "status": "failed",
                    "worker_reaped": True,
                    "native_teardown": _native_teardown_status(
                        meter, normal_exit=normal_exit
                    ),
                }
            ),
            encoding="utf-8",
        )
    return result


def main(argv: list[str] | None = None) -> int:
    """Refuse without both operator approval and disconnected-runtime attestation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", choices=tuple(PACKAGES), default="T27-S1")
    parser.add_argument("--execute-approved", action="store_true")
    parser.add_argument("--offline-attested", action="store_true")
    parser.add_argument("--worker-token")
    args = parser.parse_args(argv)
    package = PACKAGES[args.package]
    if not args.execute_approved or not args.offline_attested:
        print(
            "The smoke requires package approval and offline attestation; nothing started."
        )
        return 2
    if package.closed:
        print(
            f"{package.package_id} is closed; no worker, native process or run root started."
        )
        return 2
    if args.worker_token:
        try:
            meter = Meter.worker(
                package.root, args.worker_token, package_id=package.package_id
            )
        except (OSError, ValueError, OllamaError):
            print(f"{package.package_id} worker claim refused; nothing started.")
            return 2
        return execute_worker(meter, package)
    try:
        validate_local_ancestry(package.root)
        package.root.mkdir(parents=True, exist_ok=False)
    except OSError:
        print(
            f"{package.package_id} run root is unavailable or already exists; no retry/reset is permitted."
        )
        return 2
    meter = Meter(package.root, package_id=package.package_id)
    try:
        check_sources(package)
        status = supervise(
            meter,
            [
                sys.executable,
                "-m",
                "tests.evals.spikes.t27_runtime_smoke",
                "--package",
                package.package_id,
                "--execute-approved",
                "--offline-attested",
                "--worker-token",
                meter.state["worker_token"],
            ],
        )
        print(
            f"{package.package_id}: {'passed' if status == 0 else 'failed'}; inspect result.json and any parent-stop.json in {package.root.name}."
        )
        return status
    except (OSError, ValueError, OllamaError):
        meter.state["stopped"] = True
        meter.save()
        print(
            f"{package.package_id} stopped before successful handoff; preserve this root and do not retry."
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
