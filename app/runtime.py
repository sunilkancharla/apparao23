"""Exclusive, scoped embedding runtime with independent owned-tree teardown."""

import asyncio
import os
import threading
import time
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Protocol

import httpx

from app.config import Settings, validate_local_ancestry
from app.diagnostics import MODEL_MANIFESTS, OLLAMA_SHA256, _asset, _model, reserve_port
from app.ollama import OllamaClient, OllamaError
from app.retrieval.embeddings import Embedder
from app.storage.files import TEMP_CAP, UploadStore

SCRATCH_CAP = 16_000_000


class OwnedProcess(Protocol):
    """Process controls must refer to owned handles, never a discovered PID alone."""

    def start(
        self, executable: Path, environment: dict[str, str], directory: Path
    ) -> None: ...
    def check(self, port: int, *, require_listener: bool) -> bool: ...
    def close(self) -> None: ...


def _verify_assets(settings: Settings) -> None:
    states = [
        _asset("ollama", settings.ollama_executable, OLLAMA_SHA256, 100_000_000),
        _model(
            settings.model_root, "embedding_model", *MODEL_MANIFESTS["embedding_model"]
        ),
    ]
    for state in states:
        if not state.code.endswith("_VERIFIED"):
            raise OllamaError(state.code)


def _process() -> OwnedProcess:
    from app.windows_job import WindowsJob

    return WindowsJob()


class OwnedRuntime:
    """Acquire the existing store's single event-loop work slot for one session.

    The operator provisions a private runtime home below managed staging. It is
    counted as temporary data, retained after use and never recursively deleted.
    Native execution requires separate validation; no startup service is created.
    """

    def __init__(
        self,
        settings: Settings,
        store: UploadStore,
        home: Path,
        *,
        process_factory: Callable[[], OwnedProcess] = _process,
        verify_assets: Callable[[Settings], None] = _verify_assets,
        transport: httpx.AsyncBaseTransport | None = None,
        timeout: float = 84,
    ) -> None:
        if type(timeout) not in (float, int) or not 0 < timeout <= 84:
            raise OllamaError("OLLAMA_CONFIG_INVALID")
        self.settings, self.store, self.home = settings, store, home
        self.factory, self.verify_assets, self.transport = (
            process_factory,
            verify_assets,
            transport,
        )
        self.timeout = float(timeout)
        self._active: OwnedProcess | None = None

    def _environment(self) -> dict[str, str]:
        windows = os.environ.get("SystemRoot")
        if not windows:
            raise OllamaError("OLLAMA_ENVIRONMENT_INVALID")
        return {
            "SystemRoot": windows,
            "WINDIR": windows,
            "PATH": str(self.settings.ollama_executable.parent)
            + os.pathsep
            + str(Path(windows) / "System32"),
            "USERPROFILE": str(self.home),
            "HOME": str(self.home),
            "APPDATA": str(self.home / "AppData/Roaming"),
            "LOCALAPPDATA": str(self.home / "AppData/Local"),
            "TEMP": str(self.home / "tmp"),
            "TMP": str(self.home / "tmp"),
            "OLLAMA_HOST": f"127.0.0.1:{self.settings.ollama_port}",
            "OLLAMA_MODELS": str(self.settings.model_root),
            "OLLAMA_NO_CLOUD": "1",
            "OLLAMA_NUM_PARALLEL": "1",
            "OLLAMA_MAX_LOADED_MODELS": "1",
            "OLLAMA_DEBUG": "false",
            "CUDA_VISIBLE_DEVICES": "-1",
            "HIP_VISIBLE_DEVICES": "-1",
            "OLLAMA_VULKAN": "false",
            "OLLAMA_IGPU_ENABLE": "false",
        }

    def _home_size(self) -> int:
        staging = (self.store.root / "staging").resolve()
        validate_local_ancestry(self.home)
        relative = self.home.resolve().relative_to(staging)
        if not relative.parts or not self.home.is_dir():
            raise OllamaError("OLLAMA_HOME_INVALID")
        size = 0
        for count, path in enumerate(self.home.rglob("*"), 1):
            if count > 4096:
                raise OllamaError("OLLAMA_SCRATCH_LIMIT")
            validate_local_ancestry(path)
            info = path.stat()
            if path.is_file():
                if info.st_nlink != 1:
                    raise OllamaError("OLLAMA_HOME_INVALID")
                size += info.st_size
            elif not path.is_dir():
                raise OllamaError("OLLAMA_HOME_INVALID")
        if size > SCRATCH_CAP:
            raise OllamaError("OLLAMA_SCRATCH_LIMIT")
        return size

    @asynccontextmanager
    async def session(self) -> AsyncIterator[Embedder]:
        """Own process, listener and work slot until verified teardown, even on cancellation."""
        store = self.store
        if (
            store.busy
            or store.recovery_pending
            or store.connection is None
            or self._active is not None
        ):
            raise OllamaError("OLLAMA_BUSY")
        store.busy = True
        stop, ready = threading.Event(), threading.Event()
        failure: list[str] = []
        process, monitor = None, None
        deadline = time.monotonic() + self.timeout

        def check() -> None:
            if failure:
                raise OllamaError(failure[0])
            if time.monotonic() >= deadline:
                raise OllamaError("OLLAMA_TIMEOUT")
            self._home_size()
            if not store.busy or process is None or self._active is not process:
                raise OllamaError("OLLAMA_OWNERSHIP_UNVERIFIED")
            if (
                not process.check(
                    self.settings.ollama_port, require_listener=ready.is_set()
                )
                and ready.is_set()
            ):
                raise OllamaError("OLLAMA_OWNERSHIP_UNVERIFIED")

        def watch() -> None:
            last = time.monotonic()
            while not stop.wait(0.1):
                try:
                    current = time.monotonic()
                    if current - last > 0.3:
                        raise OllamaError("OLLAMA_MONITOR_GAP")
                    last = current
                    check()
                except (OllamaError, OSError, ValueError) as error:
                    failure.append(
                        error.code
                        if isinstance(error, OllamaError)
                        else "OLLAMA_RUNTIME_STOPPED"
                    )
                    try:
                        process.close()
                    except (OSError, OllamaError):
                        failure.append("OLLAMA_CLEANUP_PENDING")
                    return

        try:
            self.verify_assets(self.settings)
            self._home_size()
            if store._usage()["temporary"] + SCRATCH_CAP > TEMP_CAP:
                raise OllamaError("OLLAMA_SCRATCH_LIMIT")
            with reserve_port(self.settings.ollama_port):
                pass
            process = self.factory()
            self._active = process
            environment = self._environment()
            if time.monotonic() >= deadline:
                raise OllamaError("OLLAMA_TIMEOUT")
            process.start(self.settings.ollama_executable, environment, self.home)
            monitor = threading.Thread(target=watch, daemon=True)
            monitor.start()
            async with asyncio.timeout(max(0, deadline - time.monotonic())):
                while not process.check(
                    self.settings.ollama_port, require_listener=False
                ):
                    check()
                    await asyncio.sleep(0.01)
                ready.set()
                check()
                async with OllamaClient(
                    self.settings.ollama_port,
                    ownership_check=check,
                    timeout=max(0.001, deadline - time.monotonic()),
                    transport=self.transport,
                ) as client:
                    yield Embedder(client)
        except TimeoutError:
            raise OllamaError("OLLAMA_TIMEOUT") from None
        except (OSError, ValueError):
            raise OllamaError("OLLAMA_RUNTIME_UNAVAILABLE") from None
        finally:
            stop.set()
            cleanup_ok = True
            if monitor is not None:
                monitor.join(timeout=1)
                cleanup_ok = not monitor.is_alive()
            if process is not None:
                try:
                    process.close()
                except (OSError, OllamaError):
                    cleanup_ok = False
            if cleanup_ok:
                self._active = None
                store.busy = False
                if failure:
                    raise OllamaError(failure[0]) from None
            else:
                store.recovery_pending = True
                raise OllamaError("OLLAMA_CLEANUP_PENDING") from None
