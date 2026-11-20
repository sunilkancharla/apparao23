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
    from dataclasses import replace

    monkeypatch.setitem(
        smoke.PACKAGES, "T27-S2", replace(smoke.PACKAGES["T27-S2"], root=tmp_path)
    )
    assert (
        smoke.main(["--package", "T27-S2", "--execute-approved", "--offline-attested"])
        == 2
    )
    assert not (tmp_path / "ledger.json").exists()


@pytest.mark.parametrize("package_id", ["T27-S1", "T27-S2"])
def test_changed_source_seal_refuses_before_native_construction(
    tmp_path, monkeypatch, package_id
):
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
                "package": package_id,
                "sha256": {
                    name: hashlib.sha256((tmp_path / name).read_bytes()).hexdigest()
                    for name in paths
                },
            }
        )
    )
    monkeypatch.setattr(smoke, "PROJECT_ROOT", tmp_path)
    package = smoke.SmokePackage(package_id, tmp_path / "unused", seal, closed=True)
    smoke.check_sources(package)
    (tmp_path / "app/a.py").write_bytes(b"changed\n")
    with pytest.raises(OllamaError, match="SOURCE_MISMATCH"):
        smoke.check_sources(package)


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


def test_closed_s1_is_refused_even_with_no_existing_root(tmp_path, monkeypatch):
    from dataclasses import replace

    package = replace(smoke.PACKAGES["T27-S1"], root=tmp_path / "uncreated")
    monkeypatch.setitem(smoke.PACKAGES, "T27-S1", package)
    monkeypatch.setattr(
        smoke, "supervise", lambda *a, **k: pytest.fail("Closed S1 launched a worker")
    )
    assert smoke.main(["--execute-approved", "--offline-attested"]) == 2
    assert not package.root.exists()


def test_s2_ledger_cannot_claim_an_s1_worker(tmp_path):
    meter = smoke.Meter(tmp_path, package_id="T27-S1")
    with pytest.raises(OllamaError, match="WORKER_REFUSED"):
        smoke.Meter.worker(tmp_path, meter.state["worker_token"], package_id="T27-S2")
    assert not (tmp_path / "worker.claim").exists()


@pytest.mark.parametrize(
    "normal_exit,code,native,expected",
    [
        (True, "MODEL_MISSING", {}, "not_started"),
        (False, "MODEL_MISSING", {}, "unverified"),
        (True, "UNKNOWN_ERROR", {}, "unverified"),
        (True, "MODEL_MISSING", {"positive": 0}, "unverified"),
        (True, [], {}, "unverified"),
    ],
)
def test_parent_distinguishes_proven_preflight_stop_from_teardown_uncertainty(
    tmp_path, normal_exit, code, native, expected
):
    meter = smoke.Meter(tmp_path)
    meter.state["native_observed"] = native
    (tmp_path / "result.json").write_text(
        json.dumps(
            {"package": meter.state["package"], "status": "failed", "code": code}
        )
    )
    assert smoke._native_teardown_status(meter, normal_exit=normal_exit) == expected


def test_s2_parent_forwards_the_selected_package_to_its_worker(tmp_path, monkeypatch):
    from dataclasses import replace

    package = replace(smoke.PACKAGES["T27-S2"], root=tmp_path / "fresh")
    monkeypatch.setitem(smoke.PACKAGES, "T27-S2", package)
    seen = []
    monkeypatch.setattr(smoke, "check_sources", lambda selected: seen.append(selected))

    def supervised(meter, arguments):
        assert meter.root == package.root and meter.state["package"] == "T27-S2"
        index = arguments.index("--package")
        assert arguments[index + 1] == "T27-S2"
        assert "--worker-token" in arguments
        return 0

    monkeypatch.setattr(smoke, "supervise", supervised)
    assert (
        smoke.main(["--package", "T27-S2", "--execute-approved", "--offline-attested"])
        == 0
    )
    assert seen == [package]
