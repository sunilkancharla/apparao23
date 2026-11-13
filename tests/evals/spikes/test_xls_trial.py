"""T07A preflight controls; these tests never open user workbooks."""

import pytest


def test_native_denial_requires_access_denied_for_every_transport():
    from xls_trial import native_denial_verified

    assert native_denial_verified({"tcp4": 10013, "tcp6": 10013, "udp4": 10013})
    for error in (0, 10060, 10051, None):
        assert not native_denial_verified({"tcp4": error, "tcp6": 10013, "udp4": 10013})
    assert not native_denial_verified({"tcp4": 10013})


def test_trial_memory_guards_are_smaller_than_embedding_trial(tmp_path):
    from xls_trial import XlsBudget

    budget = XlsBudget(tmp_path / "meter.json", clock=lambda: 100)
    budget.memory(5 * 1024**3, 100 * 1024**2)
    with pytest.raises(RuntimeError):
        budget.memory(3 * 1024**3, 100 * 1024**2)
    with pytest.raises(RuntimeError):
        budget.memory(5 * 1024**3, 513 * 1024**2)


def test_trial_provisioning_deadline_is_twenty_minutes(tmp_path):
    from xls_trial import XlsBudget

    clock = [100]
    budget = XlsBudget(tmp_path / "meter.json", clock=lambda: clock[0])
    budget.download(1)
    clock[0] = 1301
    with pytest.raises(RuntimeError, match="Provisioning deadline"):
        budget.download(1)


def test_trial_has_one_hundred_starts_and_cannot_reset(tmp_path):
    from xls_trial import XlsBudget

    path = tmp_path / "meter.json"
    budget = XlsBudget(path, clock=lambda: 100)
    budget.reserve_processes(100)
    with pytest.raises(RuntimeError):
        XlsBudget(path, clock=lambda: 101).reserve_processes(1)
