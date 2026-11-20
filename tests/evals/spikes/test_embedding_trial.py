"""Mocked T10 budget/client checks; no engine or parser subprocesses."""

import json

import httpx
import pytest
from embedding_budget import Budget, BudgetExceeded


def test_continuation_limits_persist_and_forbid_downloads(tmp_path):
    """A new phase has explicit limits that reopening cannot silently expand."""
    path = tmp_path / "meter.json"
    budget = Budget(
        path, clock=lambda: 100, limits={"processes": 24, "calls": 100, "downloaded": 0}
    )
    budget.reserve_processes(24)
    with pytest.raises(BudgetExceeded):
        Budget(path, clock=lambda: 101).reserve_processes(1)
    with pytest.raises(BudgetExceeded):
        budget.download(1)
    assert budget.read()["limits"]["processes"] == 24


def test_observed_native_overshoot_is_saved_without_double_charge(tmp_path):
    """Already created descendants remain evidence even when the cap is crossed."""
    budget = Budget(tmp_path / "meter.json", clock=lambda: 100, limits={"processes": 3})
    budget.reserve_processes(2)
    budget.observe_native(1, reserved=1)
    with pytest.raises(BudgetExceeded, match="Observed native process allowance"):
        budget.observe_native(3, reserved=1)
    assert budget.read()["processes"] == 4
    assert budget.read()["native_observed"] == 3
    assert budget.read()["reserved_processes"] == 2
    with pytest.raises(BudgetExceeded):
        budget.observe_native(3, reserved=1)
    assert budget.read()["processes"] == 4


def test_supervisor_saves_reason_before_closing_job(tmp_path):
    """A connection reset cannot hide the supervisor's original stop reason."""
    from embedding_trial import observe_job

    path = tmp_path / "stop.json"
    failures = []

    class FailingJob:
        def refresh(self):
            raise BudgetExceeded("Observed native process allowance")

        def close(self):
            assert (
                json.loads(path.read_text())["reason"]
                == "Observed native process allowance"
            )

    assert not observe_job(FailingJob(), [], failures, path)
    assert failures[0]["type"] == "BudgetExceeded"


def test_shared_process_and_request_limits_survive_reopen(tmp_path):
    """All launch categories consume the same persistent ledger, without reset."""
    path = tmp_path / "meter.json"
    budget = Budget(path, clock=lambda: 100)
    budget.reserve_processes(2)
    budget.reserve_processes(38)
    with pytest.raises(BudgetExceeded):
        Budget(path, clock=lambda: 101).reserve_processes(1)
    budget.start_benchmark()
    for _ in range(200):
        budget.call()
    with pytest.raises(BudgetExceeded):
        Budget(path, clock=lambda: 101).call()
    assert json.loads(path.read_text())["processes"] == 40
    assert json.loads(path.read_text())["calls"] == 200


def test_deadlines_and_download_limits_fail_before_work(tmp_path):
    """Expired calls, oversized transfers and missing memory headroom are refused."""
    path = tmp_path / "meter.json"
    budget = Budget(path, clock=lambda: 100)
    budget.start_benchmark()
    with pytest.raises(BudgetExceeded):
        Budget(path, clock=lambda: 1901).call()
    budget.download(3 * 1024**3)
    with pytest.raises(BudgetExceeded):
        budget.download(1)
    with pytest.raises(BudgetExceeded):
        budget.memory(3 * 1024**3, 1024)
    with pytest.raises(BudgetExceeded):
        budget.memory(5 * 1024**3, 1024**3 + 1)
    with pytest.raises(BudgetExceeded):
        Budget(path, clock=lambda: 5501).download(1)


def test_local_client_counts_errors_and_forbids_remote_hosts(tmp_path):
    """HTTP failures still count; an external base URL cannot receive evidence."""
    from embedding_trial import LocalClient

    budget = Budget(tmp_path / "meter.json", clock=lambda: 100)
    budget.start_benchmark()
    transport = httpx.MockTransport(lambda request: httpx.Response(500))
    with LocalClient(budget, transport=transport) as client:
        with pytest.raises(httpx.HTTPStatusError):
            client.request("GET", "/api/version")
        assert budget.read()["calls"] == 1
    with pytest.raises(ValueError):
        LocalClient(budget, base_url="https://example.invalid")


def test_cosine_ranking_and_vector_validation():
    """Invalid vectors cannot be silently accepted into retrieval scores."""
    from embedding_trial import rank, validate_vectors

    assert rank([1.0, 0.0], [[0.0, 1.0], [1.0, 0.0]]) == [1, 0]
    validate_vectors([[1.0, 0.0]], count=1, dimensions=2)
    for vectors in [
        [[0.0, 0.0]],
        [[float("nan"), 1]],
        [[1]],
        [[True, 0]],
        [[1e308, 1e308]],
    ]:
        with pytest.raises(ValueError):
            validate_vectors(vectors, count=1, dimensions=2)


def test_ledger_retries_temporary_windows_replace_lock(tmp_path, monkeypatch):
    """An antivirus-style sharing lock cannot lose a charged transfer chunk."""
    from pathlib import Path

    budget = Budget(tmp_path / "meter.json", clock=lambda: 100)
    original = Path.replace
    attempts = []

    def briefly_locked(path, target):
        attempts.append(1)
        if len(attempts) < 3:
            raise PermissionError("temporary sharing lock")
        return original(path, target)

    monkeypatch.setattr(Path, "replace", briefly_locked)
    budget.download(1024)
    assert budget.read()["downloaded"] == 1024
    assert len(attempts) == 3


def test_pending_charge_is_recovered_without_reset(tmp_path):
    """A failed replace preserves the larger counters and earliest deadline."""
    path = tmp_path / "meter.json"
    budget = Budget(path, clock=lambda: 100)
    budget.download(100)
    pending = budget.read()
    pending["downloaded"] = 200
    path.with_suffix(".tmp").write_text(json.dumps(pending))
    assert Budget(path, clock=lambda: 101).read()["downloaded"] == 200


def test_fixed_corpus_provenance_and_scope():
    """Two-year CSV subset preserves gold IDs without enabling global scores."""
    from pathlib import Path

    from embedding_trial import corpus

    frozen = corpus(Path.cwd())
    assert len(frozen["passages"]) == 32
    assert len(frozen["queries"]) == 12
    by_id = {p["id"]: p for p in frozen["passages"]}
    assert by_id["R09:2"]["columns"]["2025"] == "350764"
    assert by_id["R09:2"]["lines"] == [2, 2]
    assert frozen["queries"][6]["gold"] == ["R08:2", "R09:2"]


def test_native_empty_job_uses_kernel_accounting(tmp_path, monkeypatch):
    """Query a real empty job; no subprocess/engine is started by this check."""
    import embedding_budget

    budget = Budget(tmp_path / "meter.json", clock=lambda: 100)
    budget.start_benchmark()
    monkeypatch.setattr(
        embedding_budget,
        "memory_snapshot",
        lambda: {"available_physical": 5 * 1024**3, "controller_private": 1024},
    )
    job = embedding_budget.NativeJob(budget)
    try:
        assert job.refresh()["native_processes"] == 0
        assert budget.read()["processes"] == 0
    finally:
        job.close()
