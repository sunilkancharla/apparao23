"""Evaluation-only input admission and packing; not an application endpoint."""

from collections.abc import Callable, Mapping
from typing import Any


class Unavailable(ValueError):
    """Admission cannot be proved for this exact request."""


class _Overflow(Unavailable):
    pass


def _snapshot(identity: Mapping[str, Any]) -> tuple:
    required = (
        "model",
        "runtime",
        "tokenizer",
        "rendering",
        "sources",
        "context",
        "branch",
    )
    if set(identity) != set(required) or identity["branch"] != "plain-text":
        raise Unavailable("unsupported identity/rendering")
    if any(
        not isinstance(identity[key], str) or not identity[key] for key in required[:4]
    ):
        raise Unavailable("missing identity")
    sources = identity["sources"]
    if (
        not isinstance(sources, tuple)
        or any(not isinstance(v, str) for v in sources)
        or len(set(sources)) != len(sources)
    ):
        raise Unavailable("invalid source scope")
    _integer(identity["context"], minimum=1)
    return tuple(identity[key] for key in required)


def _integer(value: Any, minimum: int = 0) -> None:
    if type(value) is not int or value < minimum:
        raise Unavailable("missing/malformed count or reservation")


def admit(
    identity: Mapping[str, Any],
    count: int,
    output: int,
    overhead: int,
    *,
    equality_proven: bool = False,
    cancelled: bool = False,
) -> tuple:
    """Issue an evaluation ticket only for a proved exact input budget."""
    if cancelled:
        raise Unavailable("cancelled")
    snapshot = _snapshot(identity)
    _integer(count)
    _integer(output, minimum=1)
    _integer(overhead)
    if type(equality_proven) is not bool:
        raise Unavailable("invalid equality proof flag")
    total = count + output + overhead
    if total > identity["context"] or (
        total == identity["context"] and not equality_proven
    ):
        raise _Overflow("input/output reservation unavailable")
    return snapshot, count, output, overhead


def publish(
    ticket: tuple, identity: Mapping[str, Any], *, cancelled: bool = False
) -> bool:
    """Reject stale or cancelled evaluation tickets."""
    if (
        cancelled
        or not isinstance(ticket, tuple)
        or len(ticket) != 4
        or ticket[0] != _snapshot(identity)
    ):
        raise Unavailable("cancelled or stale admission")
    return True


def pack(
    identity: Mapping[str, Any],
    history: tuple,
    evidence: tuple,
    oracle: Callable,
    output: int,
    overhead: int,
    *,
    cancelled: bool = False,
) -> dict[str, Any]:
    """Evaluate at most eight packings, retaining mandatory request identity."""
    pinned_identity = _snapshot(identity)
    if cancelled or any(v not in identity["sources"] for v in evidence):
        raise Unavailable("cancelled or unrelated source")
    if any(not isinstance(pair, tuple) or len(pair) != 2 for pair in history):
        raise Unavailable("incomplete history pair")
    selected_history, selected_evidence = tuple(history), tuple(evidence)
    for _ in range(8):
        try:
            count = oracle(selected_history, selected_evidence)
        except TimeoutError as exc:
            raise Unavailable("counting timed out") from exc
        if _snapshot(identity) != pinned_identity:
            raise Unavailable("identity changed during counting")
        _integer(count)
        try:
            ticket = admit(identity, count, output, overhead, cancelled=cancelled)
        except _Overflow:
            if selected_history:
                selected_history = selected_history[1:]
            elif selected_evidence:
                selected_evidence = selected_evidence[:-1]
            else:
                raise
        else:
            return {
                "ticket": ticket,
                "history": selected_history,
                "evidence": selected_evidence,
                "history_pairs_removed": len(history) - len(selected_history),
                "evidence_removed": len(evidence) - len(selected_evidence),
            }
    raise Unavailable("eight candidate packings exhausted")
