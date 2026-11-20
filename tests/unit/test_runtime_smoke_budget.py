"""Fake-only checks for the gated, non-resumable native handoff's shared meter."""

import hashlib
import io
import json
import subprocess

import pytest

from app.ollama import OllamaError
from tests.evals.spikes import t27_runtime_smoke as smoke


@pytest.fixture(autouse=True)
def account_retained_ledgers(tmp_path, run_budget):
    yield
    for path in tmp_path.rglob("*"):
        if path.is_file():
            run_budget.retain(path.read_bytes())


def test_one_meter_precharges_controller_and_both_native_trees(tmp_path):
    meter = smoke.Meter(tmp_path)
    meter.reserve("positive")
    meter.reserve("cancel")
    meter.observe("positive", 4)
    meter.observe("cancel", 1)
    assert meter.state["starts_charged"] == 34
    assert meter.state["native_observed"] == {"positive": 4, "cancel": 1}
    assert json.loads((tmp_path / "ledger.json").read_text())["starts_charged"] == 34
    with pytest.raises(OllamaError, match="LEDGER_EXISTS"):
        smoke.Meter(tmp_path)


def test_failed_start_reservation_is_not_refunded_or_reused(tmp_path):
    meter = smoke.Meter(tmp_path)
    meter.reserve("positive")
    with pytest.raises(OllamaError, match="START_REFUSED"):
        meter.reserve("positive")
    assert meter.state["starts_charged"] == 18 and meter.state["stopped"]


def test_calls_and_deadline_exhaustion_are_sticky(tmp_path):
    now = [0.0]
    meter = smoke.Meter(tmp_path, clock=lambda: now[0])
    for _ in range(12):
        meter.call()
    with pytest.raises(OllamaError, match="CALL_LIMIT"):
        meter.call()
    with pytest.raises(OllamaError, match="STOPPED"):
        meter.check()
    assert meter.state["calls"] == 12


def test_expired_deadline_cannot_launch_a_control(tmp_path):
    now = [0.0]
    meter = smoke.Meter(tmp_path, clock=lambda: now[0])
    now[0] = 181.0
    with pytest.raises(OllamaError, match="STOPPED"):
        meter.reserve("cancel")
    assert meter.state["starts_charged"] == 2


def test_observed_cumulative_overshoot_is_preserved_and_stops_following_work(tmp_path):
    meter = smoke.Meter(tmp_path)
    meter.reserve("positive")
    meter.observe("positive", 17)
    assert meter.state["stopped"] and meter.state["native_observed"]["positive"] == 17
    assert meter.state["starts_charged"] == 19
    with pytest.raises(OllamaError, match="STOPPED"):
        meter.reserve("cancel")


@pytest.mark.parametrize("flags", [[], ["--execute-approved"], ["--offline-attested"]])
def test_missing_gate_flags_never_create_a_run_root(tmp_path, monkeypatch, flags):
    root = tmp_path / "not-created"
    monkeypatch.setattr(smoke, "RUN_ROOT", root)
    assert smoke.main(flags) == 2
    assert not root.exists()


def test_existing_run_root_is_never_reopened_or_reset(tmp_path, monkeypatch):
    monkeypatch.setattr(smoke, "RUN_ROOT", tmp_path)
    assert smoke.main(["--execute-approved", "--offline-attested"]) == 2
    assert not (tmp_path / "ledger.json").exists()


def test_changed_source_seal_refuses_before_native_construction(tmp_path, monkeypatch):
    paths = [
        "app/a.py",
        "pyproject.toml",
        "uv.lock",
        "tests/evals/spikes/t27_runtime_smoke.py",
    ]
    for name in paths:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"authored synthetic source\n")
    seal = tmp_path / "docs/proposals/t27-runtime-smoke-seal.json"
    seal.parent.mkdir(parents=True)
    seal.write_text(
        json.dumps(
            {
                "package": "T27-S1",
                "sha256": {
                    name: hashlib.sha256((tmp_path / name).read_bytes()).hexdigest()
                    for name in paths
                },
            }
        )
    )
    monkeypatch.setattr(smoke, "PROJECT_ROOT", tmp_path)
    smoke.check_sources()
    (tmp_path / "app/a.py").write_bytes(b"changed\n")
    with pytest.raises(OllamaError, match="SOURCE_MISMATCH"):
        smoke.check_sources()


def test_prepaid_worker_can_be_claimed_only_once(tmp_path):
    parent = smoke.Meter(tmp_path)
    worker = smoke.Meter.worker(tmp_path, parent.state["worker_token"])
    assert worker.state["starts_charged"] == 2
    worker.reserve("positive")
    with pytest.raises(OSError):
        smoke.Meter.worker(tmp_path, parent.state["worker_token"])


@pytest.mark.parametrize("mode", ["deadline", "output"])
def test_parent_kills_and_reaps_worker_on_deadline_or_output_limit(tmp_path, mode):
    meter = smoke.Meter(tmp_path)

    class Worker:
        def __init__(self):
            self.stdout = io.BytesIO(b"x" * (65_537 if mode == "output" else 1))
            self.killed = self.reaped = False

        def wait(self, timeout):
            if mode == "deadline" and not self.killed:
                raise subprocess.TimeoutExpired("synthetic-worker", timeout)
            self.reaped = True
            return 1

        def kill(self):
            self.killed = True

        def poll(self):
            return 1 if self.reaped else None

    worker = Worker()
    assert (
        smoke.supervise(meter, ["synthetic-worker"], start=lambda *a, **k: worker) == 1
    )
    assert worker.killed and worker.reaped and meter.state["stopped"]
    assert (tmp_path / "worker-output.txt").stat().st_size <= 65_536
