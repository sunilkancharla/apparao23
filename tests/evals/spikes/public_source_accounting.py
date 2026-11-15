"""R1-A single-writer accounting/verdict prototype; no executable trial adapter.

These policies are exercised with fake observations only. They do not launch
processes, install packages, contact services, or replace the host tool boundary.
"""

import json
import time
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

CATEGORIES = frozenset({"orchestration", "nested_tool", "shell", "executable"})


class Boundary(RuntimeError):
    """Admission or observed accounting has crossed an explicit boundary."""


class InjectedAccountingError(RuntimeError):
    """Distinct synthetic failure; ordinary errors must not satisfy this control."""


class Ledger:
    """Durable single-controller reservations; concurrent writers are unsupported."""

    def __init__(self, path: Path, clock: Callable[[], float] = time.monotonic):
        self.path = path
        self.clock = clock

    @classmethod
    def create(cls, path: Path, *, limit: int = 48, protected: int = 12,
               seconds: float = 900, clock: Callable[[], float] = time.monotonic
               ) -> "Ledger":
        """Create once; never reset an existing ledger or reuse a closed epoch."""
        if not 0 < protected < limit or seconds <= 0:
            raise Boundary("Invalid allocation")
        state = {"status": "active", "limit": limit, "protected": protected,
                 "started": clock(), "seconds": seconds, "normal_charged": 0,
                 "stop_charged": 0, "events": [], "observations": {}, "overrun": False}
        with path.open("x", encoding="utf-8") as output:
            json.dump(state, output)
        return cls(path, clock)

    def read(self) -> dict[str, Any]:
        """Read the durable state rather than trusting a cached counter."""
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _save(self, state: dict[str, Any]) -> None:
        data = json.dumps(state, indent=2).encode()
        if len(data) > 1048576:
            raise Boundary("Ledger output boundary")
        pending = self.path.with_suffix(".tmp")
        pending.write_bytes(data)
        pending.replace(self.path)

    def reserve(self, label: str, units: Mapping[str, int], *, stop: bool = False) -> None:
        """Precharge an entire tool/command block; failed actions get no refund."""
        if (not label or not units or set(units) - CATEGORIES
                or any(type(n) is not int or n <= 0 for n in units.values())):
            raise Boundary("Invalid charge categories/units")
        state = self.read()
        allowed = {"active", "stopped"} if stop else {"active"}
        if state["status"] not in allowed:
            raise Boundary("Terminal or unknown allocation state")
        if any(event["label"] == label for event in state["events"]):
            raise Boundary("Reservation labels cannot be retried")
        elapsed = self.clock() - state["started"]
        key = "stop_charged" if stop else "normal_charged"
        cap = state["protected"] if stop else state["limit"] - state["protected"]
        if ((not stop and not 0 <= elapsed <= state["seconds"])
                or state[key] + sum(units.values()) > cap):
            state["status"] = "stopped"
            self._save(state)
            raise Boundary("Time or reservation boundary")
        state[key] += sum(units.values())
        state["events"].append({"label": label, "units": dict(units), "stop": stop})
        self._save(state)

    def observe(self, label: str, total: int) -> None:
        """Persist discoveries and overshoot before raising; never double-charge."""
        state = self.read()
        if state["status"] not in {"active", "stopped"}:
            raise Boundary("Terminal allocation observation")
        events = [e for e in state["events"] if e["label"] == label and not e["stop"]]
        previous = state["observations"].get(label, 0)
        if (len(events) != 1 or type(total) is not int or total < previous or total < 0):
            raise Boundary("Invalid cumulative observation")
        reserved = events[0]["units"].get("executable", 0)
        if not reserved:
            raise Boundary("No executable reservation")
        discovered = max(0, total - max(previous, reserved))
        state["observations"][label] = total
        state["normal_charged"] += discovered
        state["overrun"] = state["normal_charged"] > state["limit"] - state["protected"]
        if discovered:
            state["status"] = "stopped"
        self._save(state)
        if discovered:
            raise Boundary("Unexpected process count persisted and charged")


def finish(*, close: Callable[[], bool], reap: Callable[[], bool],
           active: Callable[[], int], account: Callable[[], None],
           persist: Callable[[dict[str, Any]], None]) -> dict[str, Any]:
    """Collect independent fake cleanup results even when accounting fails.

    Persistence errors propagate and prevent success. A future real adapter must
    supply verified OS results; clearing a Python handle is insufficient.
    """
    receipt: dict[str, Any] = {}
    for key, action in (("handle_close_succeeded", close), ("child_reaped", reap),
                        ("active_after_cleanup", active)):
        try:
            receipt[key] = action()
        except Exception as error:  # noqa: BLE001 -- still attempt remaining cleanup
            receipt[key] = None
            receipt[key + "_error"] = type(error).__name__
    try:
        account()
        receipt["cleanup_error"] = None
    except Exception as error:  # noqa: BLE001 -- persist the actual accounting failure
        receipt["cleanup_error"] = type(error).__name__
    persist(receipt)
    return receipt


def verdict(value: Mapping[str, Any], expected: str) -> dict[str, bool]:
    """Keep cleanup/count conformity separate; require exact control outcomes."""
    cleanup_ok = (value.get("child_reaped") is True
                  and value.get("handle_close_succeeded") is True
                  and type(value.get("active_after_cleanup")) is int
                  and value["active_after_cleanup"] == 0)
    count_ok = type(value.get("kernel_total")) is int and value["kernel_total"] == 1
    known = expected in {"success", "forced-failure"}
    expected_exit = 0 if expected == "success" else 7
    expected_error = None if expected == "success" else "InjectedAccountingError"
    outcome_ok = (known and value.get("name") == expected
                  and type(value.get("worker_exit")) is int
                  and value["worker_exit"] == expected_exit
                  and "cleanup_error" in value
                  and value["cleanup_error"] == expected_error
                  and "control_error" in value and value["control_error"] is None)
    return {"cleanup_ok": cleanup_ok, "count_ok": count_ok,
            "outcome_ok": outcome_ok, "passed": cleanup_ok and count_ok and outcome_ok}


def pair_complete(values: list[Mapping[str, Any]]) -> bool:
    """Both ordered controls must pass every predicate, including the second."""
    return (len(values) == 2 and verdict(values[0], "success")["passed"]
            and verdict(values[1], "forced-failure")["passed"])
