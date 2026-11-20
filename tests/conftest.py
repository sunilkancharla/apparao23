"""Session-wide accounting shared by routine, negative and regression tests."""

import subprocess
from pathlib import Path
from uuid import uuid4

import pytest

from tests.fixtures.budget import Budget, MeteredProcess


def pytest_configure(config):
    """Default generated test artifacts to a fresh ignored project-local root."""
    if config.option.basetemp is None:
        config.option.basetemp = str(
            Path(__file__).resolve().parents[1] / "data/test-runs" / uuid4().hex
        )


@pytest.fixture(scope="session", autouse=True)
def run_budget():
    """Count the controller plus every admitted child without resetting per adapter."""
    budget = Budget(starts=64, output_bytes=2_000_000, seconds=120)
    budget.charge_start("pytest_controller")
    original = subprocess.Popen
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(
            subprocess,
            "Popen",
            lambda args, **kwargs: MeteredProcess(original, budget, args, **kwargs),
        )
        yield budget
    print(
        f"Routine budget: {budget.starts_used}/64 starts; {budget.output_used}/2000000 retained artifact/child-output bytes"
    )
