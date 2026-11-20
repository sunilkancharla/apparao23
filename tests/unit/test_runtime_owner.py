"""Injected process controls test ownership/lease/teardown without native starts."""

import asyncio
import time
from dataclasses import replace

import httpx
import pytest

from app.config import Settings
from app.ollama import OllamaError
from app.runtime import OwnedRuntime
from app.storage.files import UploadStore
from tests.unit.test_embeddings import responder


class Process:
    def __init__(self):
        self.started = self.closed = False
        self.fail_check = self.fail_close = False
        self.env = None

    def start(self, executable, environment, directory):
        self.started = True
        self.env = environment

    def check(self, port, *, require_listener):
        if self.fail_check:
            raise OllamaError("OLLAMA_OWNERSHIP_UNVERIFIED")
        return True

    def close(self):
        self.closed = True
        if self.fail_close:
            raise OllamaError("OLLAMA_CLEANUP_PENDING")


@pytest.fixture
def runtime(tmp_path):
    store = UploadStore(tmp_path / "app")
    home = store.root / "staging" / "runtime"
    for suffix in ("", "AppData/Roaming", "AppData/Local", "tmp"):
        (home / suffix).mkdir(parents=True, exist_ok=True)
    settings = replace(Settings.from_env({}), data_root=store.root)
    process = Process()
    owner = OwnedRuntime(
        settings,
        store,
        home,
        process_factory=lambda: process,
        verify_assets=lambda s: None,
        transport=httpx.MockTransport(responder),
        timeout=1,
    )
    try:
        yield owner, store, process
    finally:
        store.close()


def test_embedding_uses_owned_guard_and_releases_shared_upload_slot(runtime):
    owner, store, process = runtime

    async def run():
        async with owner.session() as embedder:
            assert store.busy and process.started
            assert (await embedder.query("Budget?", "query-1")).dimensions == 768
        assert not store.busy and process.closed

    asyncio.run(run())


@pytest.mark.parametrize("attribute", ["busy", "recovery_pending"])
def test_shared_work_or_pending_recovery_refuses_before_launch(runtime, attribute):
    owner, store, process = runtime
    setattr(store, attribute, True)

    async def run():
        async with owner.session():
            pytest.fail("Busy admission succeeded")

    with pytest.raises(OllamaError):
        asyncio.run(run())
    assert not process.started


def test_lost_ownership_closes_tree_and_refuses_results(runtime):
    owner, store, process = runtime

    async def run():
        async with owner.session() as embedder:
            process.fail_check = True
            await embedder.query("Budget?", "query-1")

    with pytest.raises(OllamaError, match="OWNERSHIP"):
        asyncio.run(run())
    assert process.closed and not store.busy


def test_cancelled_job_closes_tree_before_releasing_slot(runtime):
    owner, store, process = runtime

    async def run():
        entered = asyncio.Event()

        async def job():
            async with owner.session():
                entered.set()
                await asyncio.Event().wait()

        task = asyncio.create_task(job())
        await asyncio.wait_for(entered.wait(), 1)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(run())
    assert process.closed and not store.busy


def test_uncertain_teardown_keeps_admission_blocked(runtime):
    owner, store, process = runtime
    process.fail_close = True

    async def run():
        async with owner.session():
            pass

    with pytest.raises(OllamaError, match="CLEANUP_PENDING"):
        asyncio.run(run())
    assert store.busy and store.recovery_pending


def test_child_environment_uses_explicit_home_and_excludes_inherited_secrets(
    runtime, monkeypatch
):
    owner, _, process = runtime
    monkeypatch.setenv("OLLAMA_HOST", "https://example.invalid")
    monkeypatch.setenv("HTTP_PROXY", "https://example.invalid")
    monkeypatch.setenv("PRIVATE_TEST_SECRET", "never inherit")

    async def run():
        async with owner.session():
            pass

    asyncio.run(run())
    assert process.env["OLLAMA_HOST"] == "127.0.0.1:11435"
    assert process.env["OLLAMA_NO_CLOUD"] == "1"
    assert process.env["CUDA_VISIBLE_DEVICES"] == "-1"
    assert process.env["USERPROFILE"] == str(owner.home)
    assert "HTTP_PROXY" not in process.env and "PRIVATE_TEST_SECRET" not in process.env


def test_watchdog_terminates_when_the_event_loop_is_blocked(runtime):
    owner, store, process = runtime
    owner.timeout = 0.15

    async def run():
        async with owner.session():
            time.sleep(0.3)  # noqa: ASYNC251 - deliberately block the loop to test the independent watchdog
            assert process.closed

    with pytest.raises(OllamaError, match="TIMEOUT"):
        asyncio.run(run())
    assert not store.busy


def test_port_collision_and_bad_assets_never_launch_a_process(runtime):
    from app.diagnostics import reserve_port

    owner, store, process = runtime

    async def run():
        async with owner.session():
            pytest.fail("Unexpected launch")

    with reserve_port(owner.settings.ollama_port), pytest.raises(OllamaError):
        asyncio.run(run())
    assert not process.started and not store.busy

    def reject(settings):
        raise OllamaError("OLLAMA_ASSET_UNAVAILABLE")

    owner.verify_assets = reject
    with pytest.raises(OllamaError, match="ASSET_UNAVAILABLE"):
        asyncio.run(run())
    assert not process.started and not store.busy


def test_owned_session_excludes_real_upload_then_releases_the_shared_slot(runtime):
    from app.ingestion.validation import UploadError
    from app.storage.documents import Documents

    owner, store, _ = runtime
    conversation = Documents(store.connection).create_conversation()

    async def body():
        yield b"Name,Units\nNorth,42\n"

    async def run():
        async with owner.session():
            with pytest.raises(UploadError, match="UPLOAD_BUSY"):
                await store.receive(
                    body(), conversation, "runtime-shared-01", "authored.csv"
                )
        receipt = await store.receive(
            body(), conversation, "runtime-shared-01", "authored.csv"
        )
        assert receipt["state"] == "original_stored"

    asyncio.run(run())
