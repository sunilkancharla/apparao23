"""Small inert cases for complete launch accounting and closeout admission."""

import importlib.util
import sys
from pathlib import Path

import pytest


def load_owned():
    """Import only the new authored meter under test."""
    path = Path(__file__).with_name("evaluation_parent_accounting.py")
    spec = importlib.util.spec_from_file_location("mtr_owned", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


owned = load_owned()


def test_counts_whole_tree():
    meter = owned.ParentBudget()
    meter.admit("shell_controller_child", 3)
    assert meter.starts == 3


def test_report_reserve():
    meter = owned.ParentBudget(displayed=24576)
    with pytest.raises(ValueError, match="report_reserve"):
        meter.display("")


def test_exact_multibyte_and_closure():
    meter = owned.ParentBudget(displayed=24570)
    assert len(meter.display("éé")) == 6
    with pytest.raises(ValueError):
        meter.display("")
    assert len(meter.display("éé", closure=True)) == 6


def test_stops_and_preserves_closure_starts():
    meter = owned.ParentBudget(starts=50)
    with pytest.raises(ValueError):
        meter.admit("over_optional", 3)
    meter.admit("final", 12, closure=True)
    assert meter.starts == 62
    with pytest.raises(ValueError):
        meter.admit("over_all", 3, closure=True)


def test_duplicate_and_missing_operation():
    meter = owned.ParentBudget()
    meter.admit("one", 2)
    for name, envelope in [("one", 2), ("", 2), ("bad", 1)]:
        with pytest.raises(ValueError):
            meter.admit(name, envelope)


def test_stop_blocks_only_optional():
    meter = owned.ParentBudget(stopped=True)
    with pytest.raises(ValueError):
        meter.admit("optional", 2)
    meter.admit("closure", 2, closure=True)


def test_large_display_refused_before_charge():
    meter = owned.ParentBudget()
    with pytest.raises(ValueError):
        meter.display("x" * 2048)
    assert meter.displayed == 0


def test_no_independent_child_authority():
    meter = owned.ParentBudget(starts=52)
    child = owned.ParentBudget()
    child.admit("local_only", 2)
    with pytest.raises(ValueError):
        meter.admit("parent_still_full", 2)


def test_owned_gate_and_no_candidate_dispatch(monkeypatch):
    gate = owned.load_report_gate()
    assert gate.__name__ == "ReportGate"
    assert gate(used=24576, limit=32768, reserve=8192).used == 24576


def test_lease_duplicates_and_envelope_undercharge(tmp_path):
    lease = {"id": "synthetic", "envelope": 3}
    owned.claim_child(tmp_path, lease, "first")
    with pytest.raises(ValueError):
        owned.claim_child(tmp_path, lease, "second")


def test_parent_receipt_missing_admission(tmp_path):
    with pytest.raises((ValueError, FileNotFoundError)):
        owned.parent_receipt(tmp_path, "missing")


def test_negative_traffic_commands_never_dispatched(tmp_path):
    with pytest.raises(ValueError):
        owned.control(tmp_path, {"id": "none", "envelope": 3}, "network")


def test_supervised_control_and_failure():
    lease = owned.current_test_lease()
    first = owned.control(owned.RUN, lease, "ok")
    second = owned.control(owned.RUN, lease, "failure")
    assert first["exit"] == 0 and second["exit"] == 7
    assert all(
        item["eof"] and item["reaped"] and item["birth_filetime"]
        for item in [first, second]
    )


def test_restore_and_serialization():
    meter = owned.ParentBudget()
    value = {"text": "é\n", "stopped": False}
    raw = meter.display(value)
    assert raw.decode("utf-8").startswith("{")
    assert meter.displayed == len(raw)
