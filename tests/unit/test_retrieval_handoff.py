"""Data-only handoff guards; never invoke the real DLL/worker."""

import pytest

from tests.evals.spikes import t29_native_search as smoke


@pytest.mark.parametrize("flags", [[], ["--execute-approved"], ["--offline-attested"]])
def test_missing_flags_do_not_create_root(tmp_path, monkeypatch, flags):
    root = tmp_path / "not_created"
    monkeypatch.setattr(smoke, "RUN_ROOT", root)
    assert smoke.main(flags) == 2 and not root.exists()


def test_existing_root_is_not_reopened(tmp_path, monkeypatch):
    monkeypatch.setattr(smoke, "RUN_ROOT", tmp_path)
    assert smoke.main(["--execute-approved", "--offline-attested"]) == 2
    assert not (tmp_path / "ledger.json").exists()


@pytest.mark.parametrize("oversized", [False, True])
def test_supervisor_reaps_on_deadline_or_output_cap(tmp_path, oversized, run_budget):
    output = tmp_path / "output.txt"
    output.write_bytes(b"x" * (65537 if oversized else 0))

    class Process:
        killed = False
        reaped = False

        def poll(self):
            return 1 if self.killed else None

        def kill(self):
            self.killed = True

        def wait(self, **kwargs):
            self.reaped = True
            return 1

    process = Process()
    assert (
        smoke.supervise(process, output, 10, clock=lambda: 0 if oversized else 11) == 1
    )
    assert process.killed and process.reaped
    run_budget.retain(output.read_bytes())
