"""Mock-only T11A stream, provenance and budget controls; no model subprocesses."""

import json
from pathlib import Path

import httpx
import pytest
from embedding_budget import Budget, BudgetExceeded


def test_phase_duration_is_persisted_and_cannot_be_reset(tmp_path):
    budget = Budget(
        tmp_path / "meter.json", clock=lambda: 100, limits={"benchmark_seconds": 2700}
    )
    budget.start_benchmark()
    assert Budget(budget.path, clock=lambda: 2000).remaining() == 800
    with pytest.raises(ValueError):
        Budget(budget.path, limits={"benchmark_seconds": 3600})
    with pytest.raises(BudgetExceeded):
        Budget(budget.path, clock=lambda: 2800).remaining()


def test_stream_requires_final_record_and_bounded_total_time():
    from chat_trial import consume_stream

    rows = [
        b'{"message":{"content":"A"},"done":false}',
        b'{"message":{"content":"B"},"done":true,"done_reason":"stop"}',
    ]
    response = consume_stream(rows, deadline=10, clock=lambda: 1)
    assert response["text"] == "AB"
    assert response["first_answer_s"] == 0
    for malformed in [[b"not json"], rows[:1], [b'{"done":true}']]:
        with pytest.raises(ValueError):
            consume_stream(malformed, deadline=10, clock=lambda: 1)
    times = iter([0, 1, 11])
    with pytest.raises(BudgetExceeded):
        consume_stream(rows, deadline=10, clock=lambda: next(times))


def test_stream_rejects_thinking_tools_and_oversize_records():
    from chat_trial import consume_stream

    for row in [
        {"message": {"thinking": "unexpected", "content": "x"}, "done": True},
        {"message": {"tool_calls": [{"function": "x"}], "content": "x"}, "done": True},
        {"message": {"content": "x"}, "done": True, "done_reason": "length"},
    ]:
        with pytest.raises(ValueError):
            consume_stream([json.dumps(row).encode()], deadline=10, clock=lambda: 1)
    with pytest.raises(BudgetExceeded):
        consume_stream([b"x" * 65537], deadline=10, clock=lambda: 1)


def test_answer_schema_enforces_citation_scope():
    from chat_trial import validate_answer

    valid = {
        "answer": "Evidence",
        "status": "answered",
        "citations": [{"source_id": "R09:2", "columns": ["2025"]}],
    }
    validate_answer(valid, {"R09:2": {"2025"}})
    for bad in [
        {**valid, "status": "probably"},
        {**valid, "citations": [{"source_id": "R08:2", "columns": ["2025"]}]},
        {**valid, "citations": [{"source_id": "R09:2", "columns": ["2026"]}]},
        {**valid, "answer": 3},
        {**valid, "extra": True},
    ]:
        with pytest.raises(ValueError):
            validate_answer(bad, {"R09:2": {"2025"}})


def test_frozen_cases_and_request_controls():
    from chat_trial import build_cases, request_body

    cases = build_cases(Path.cwd())
    assert len(cases["cases"]) == 12
    assert cases["cases"][7]["evidence"] == []
    assert [p["id"] for p in cases["cases"][8]["evidence"]] == ["R09:2"]
    for case in cases["cases"]:
        body = request_body("qwen3:1.7b-q4_K_M", case)
        assert body["think"] is False and body["options"]["num_gpu"] == 0
        assert len(json.dumps(body["messages"], ensure_ascii=False).encode()) <= 3000
    assert "think" not in request_body(
        "qwen2.5:1.5b-instruct-q4_K_M", cases["cases"][0]
    )


def test_client_counts_errors_and_refuses_redirects(tmp_path):
    from chat_trial import chat_request
    from embedding_trial import LocalClient

    budget = Budget(tmp_path / "meter.json", clock=lambda: 100)
    budget.start_benchmark()
    with (
        LocalClient(
            budget,
            transport=httpx.MockTransport(
                lambda _: httpx.Response(
                    302, headers={"Location": "https://example.invalid"}
                )
            ),
        ) as client,
        pytest.raises(httpx.HTTPStatusError),
    ):
        chat_request(client, {"messages": []})
    assert budget.read()["calls"] == 1


def test_output_cap_stops_before_writing(tmp_path):
    from chat_trial import save_result

    (tmp_path / "other").write_bytes(b"1234")
    with pytest.raises(BudgetExceeded):
        save_result(tmp_path / "result.json", {"x": "long"}, limit=8)
    assert not (tmp_path / "result.json").exists()


def test_stream_wall_timer_closes_owned_work(tmp_path, monkeypatch):
    """A drip-fed stream cannot extend a request by resetting read inactivity."""
    import chat_trial
    from embedding_trial import LocalClient

    callbacks, stopped = [], []

    class Timer:
        def __init__(self, seconds, callback):
            assert 0 < seconds <= 120
            callbacks.append(callback)

        def start(self):
            pass

        def cancel(self):
            pass

    class Stream(httpx.SyncByteStream):
        def __iter__(self):
            yield b'{"message":{"content":"A"},"done":false}\n'
            callbacks[0]()
            yield b'{"message":{"content":"B"},"done":true}\n'

    monkeypatch.setattr(chat_trial.threading, "Timer", Timer)
    budget = Budget(tmp_path / "meter.json", clock=lambda: 100)
    budget.start_benchmark()
    with (
        LocalClient(
            budget,
            transport=httpx.MockTransport(
                lambda _: httpx.Response(200, stream=Stream())
            ),
        ) as client,
        pytest.raises(BudgetExceeded) as caught,
    ):
        chat_trial.chat_request(
            client, {"messages": []}, on_timeout=lambda: stopped.append(True)
        )
    assert stopped == [True] and budget.read()["calls"] == 1
    assert caught.value.partial["text"] == "A"
    assert caught.value.partial["elapsed_s"] >= 0
    assert caught.value.partial["timeout_path"] == "timer"


def test_oversize_input_is_refused_before_api_charge(tmp_path):
    from chat_trial import chat_request
    from embedding_trial import LocalClient

    budget = Budget(tmp_path / "meter.json", clock=lambda: 100)
    budget.start_benchmark()
    with LocalClient(budget) as client, pytest.raises(ValueError):
        chat_request(client, {"messages": [{"content": "x" * 3001}]})
    assert budget.read()["calls"] == 0


def test_local_review_escapes_untrusted_model_output(tmp_path):
    from chat_trial import write_review

    write_review(
        tmp_path / "review.html", {"responses": [{"text": "<script>bad()</script>"}]}
    )
    page = (tmp_path / "review.html").read_text(encoding="utf-8")
    assert "<script>" not in page and "&lt;script&gt;" in page


def test_deadline_retains_partial_answer_and_elapsed_observation():
    """A consuming-thread deadline must not discard already received fragments."""
    from chat_trial import consume_stream

    times = iter([0, 1, 11])
    rows = [
        b'{"message":{"content":"partial"},"done":false}',
        b'{"message":{"content":"late"},"done":true}',
    ]
    with pytest.raises(BudgetExceeded) as caught:
        consume_stream(rows, deadline=10, clock=lambda: next(times))
    assert caught.value.partial["text"] == "partial"
    assert caught.value.partial["stream_s"] == 11


def test_teardown_waits_for_owned_exit_then_retries_port_probe():
    """An asynchronous job termination cannot make the first socket probe final."""
    from chat_trial import settle_owned

    events, free = [], iter([False, True])

    class Process:
        def wait(self, timeout):
            assert 0 < timeout <= 5
            events.append("wait")
            return 1

    def probe():
        events.append("probe")
        return next(free)

    result = settle_owned(
        Process(), probe=probe, clock=lambda: 0, sleep=lambda _: events.append("sleep")
    )
    assert result["port_released"] is True and result["process_reaped"] is True
    assert events == ["wait", "probe", "sleep", "probe"]


def test_teardown_timeout_never_kills_an_unrelated_listener():
    """Record incomplete teardown instead of guessing ownership from a port."""
    import subprocess

    from chat_trial import settle_owned

    class Process:
        def wait(self, timeout):
            raise subprocess.TimeoutExpired("owned", timeout)

        def kill(self):
            pytest.fail("Cleanup helper must not kill any additional process")

    times = iter([0, 1])
    result = settle_owned(
        Process(), probe=lambda: False, clock=lambda: next(times), timeout=0.5
    )
    assert (
        result["port_released"] is False and result["wait_failure"] == "TimeoutExpired"
    )


def test_continuation_runs_only_missing_frozen_requests():
    """The original failed record stays intact; successful cases are not rerun."""
    from chat_trial import continuation_schedule

    frozen, schedule = continuation_schedule(Path.cwd())
    assert len(schedule) == 13
    assert (schedule[0][0], schedule[0][1]["id"]) == (2, "C12")
    assert [(rep, case["id"]) for rep, case in schedule[1:]] == [
        (3, c["id"]) for c in frozen["cases"]
    ]


def test_listener_snapshot_distinguishes_owned_test_listener():
    """Read the OS listener table without relying on failed socket connections."""
    import socket

    from chat_trial import port_not_listening

    assert port_not_listening()
    with socket.socket() as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        listener.bind(("127.0.0.1", 11434))
        listener.listen()
        assert not port_not_listening()
    assert port_not_listening()


def test_timeout_after_completion_keeps_header_latency_once(tmp_path, monkeypatch):
    """A late timer must preserve the already normalized first-content timing."""
    import chat_trial
    from embedding_trial import LocalClient

    callbacks = []
    virtual_time = [0.0]

    class Timer:
        def __init__(self, seconds, callback):
            callbacks.append(callback)

        def start(self):
            pass

        def cancel(self):
            pass

    def completed_then_timed_out(*args, **kwargs):
        virtual_time[0] = 3.0
        callbacks[0]()
        return {
            "text": "complete",
            "first_answer_s": 0.25,
            "final": {"done_reason": "stop"},
        }

    budget = Budget(tmp_path / "meter.json", clock=lambda: 100)
    budget.start_benchmark()
    monkeypatch.setattr(chat_trial.threading, "Timer", Timer)
    monkeypatch.setattr(chat_trial, "consume_stream", completed_then_timed_out)

    def transport(request):
        virtual_time[0] = 2.0
        return httpx.Response(200)

    with LocalClient(budget, transport=httpx.MockTransport(transport)) as client:
        monkeypatch.setattr(chat_trial.time, "perf_counter", lambda: virtual_time[0])
        with pytest.raises(BudgetExceeded) as caught:
            chat_trial.chat_request(client, {"messages": []})
    assert caught.value.partial["text"] == "complete"
    assert caught.value.partial["first_answer_s"] == 2.25
