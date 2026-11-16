"""IF-P one-shot static data continuation using a verified authored helper."""

from __future__ import annotations

import hashlib
import importlib.abc
import importlib.util
import json
import os
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "data/t17/input-fit-assets-remaining-01"
MIB = 1024**2
STAGES = ("open_temp", "write_json", "flush", "fsync", "close_temp", "replace_target")
BASE_SHA = "47f1d2c8202d96cbd07c4ff7d1f899c6130423d7935a73aa2cff20b1bd3d4f5c"
REMAINING = (
    (
        "Qwen/Qwen2.5-1.5B-Instruct",
        "5fee7c4ed634dc66c6e318c8ac2897b8b9154536",
        ("tokenizer_config.json", "vocab.json", "merges.txt", "config.json", "LICENSE"),
    ),
    (
        "nomic-ai/nomic-embed-text-v1.5",
        "541c5a6fadb4da793505a2bb4d3ee910de7f39ea",
        (
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "vocab.txt",
            "config.json",
        ),
    ),
)


def load_base():
    """Normal module import consumes the exact verified bytes, with no old main."""
    source = ROOT / "tests/evals/spikes/tokenizer_static_review.py"
    data = source.read_bytes()
    if len(data) > 65536 or hashlib.sha256(data).hexdigest() != BASE_SHA:
        raise ValueError("Authored helper identity")

    class VerifiedLoader(importlib.abc.SourceLoader):
        def get_filename(self, fullname):
            return str(source)

        def get_data(self, path):
            if path != str(source):
                raise OSError("No cached source permitted")
            return data

    spec = importlib.util.spec_from_loader(
        "_ifp_verified_authored_base", VerifiedLoader()
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_base()
_BASE_URL_POLICY = BASE.allowed_url


def tree_url(publisher: str, revision: str) -> str:
    return f"https://huggingface.co/api/models/{publisher}/tree/{revision}"


def asset_url(publisher: str, revision: str, filename: str) -> str:
    return f"https://huggingface.co/{publisher}/resolve/{revision}/{filename}"


def allowed_url(url: str) -> None:
    """Intersect the reviewed syntax policy with only the ten remaining files."""
    _BASE_URL_POLICY(url)
    parsed = urllib.parse.urlsplit(url)
    if parsed.hostname != "huggingface.co":
        raise ValueError("Continuation host boundary")
    for publisher, revision, files in REMAINING:
        if url == tree_url(publisher, revision):
            return
        for filename in files:
            paths = {
                urllib.parse.urlsplit(asset_url(publisher, revision, filename)).path,
                f"/api/resolve-cache/models/{publisher}/{revision}/{filename}",
            }
            if parsed.path in paths:
                return
    raise ValueError("Remaining file/revision boundary")


# Policy injection is confined to this verified, isolated authored module instance.
BASE.allowed_url = allowed_url


class PersistenceFailure(RuntimeError):
    """Named accounting failure, without arbitrary error strings or paths."""

    def __init__(self, stage: str, error: Exception):
        super().__init__(stage)
        self.stage = stage
        self.errno = getattr(error, "errno", None)
        self.winerror = getattr(error, "winerror", None)
        self.kind = type(error).__name__


class Budget(BASE.Budget):
    """New-root, stricter accounting with an independent operation journal."""

    def __init__(self, root: Path, *, synthetic: bool = False, faults=None):
        if not synthetic and root.resolve() != RUN.resolve():
            raise ValueError("Fixed continuation root")
        if faults and not synthetic:
            raise ValueError("Injected failures only in fake tests")
        super().__init__(root)
        self.synthetic = synthetic
        self.faults = faults or {}
        self.packets = 0
        self.state()
        self.journal = self.contained("operations.jsonl").open("xb")

    def close(self) -> None:
        self.journal.close()

    def state(self) -> dict:
        value = super().state()
        reserved = value["body_reserved"]
        if (
            value["http_reserved"] > 40
            or reserved["wheel"] != 0
            or reserved["asset"] > 8 * MIB
            or reserved["metadata"] > 4 * MIB
        ):
            raise ValueError("Narrower inherited accounting boundary")
        if self.tree_bytes() >= 16 * MIB - 8192:
            raise ValueError("Continuation artifact boundary")
        return value

    def trace(self, stage: str, status: str, error=None) -> None:
        self.contained("operations.jsonl")
        if self.packets >= 4096 or self.tree_bytes() >= 16 * MIB - 8192:
            raise ValueError("Diagnostic output boundary")
        packet = {
            "stage": stage,
            "status": status,
            "target": "meter.json",
            "pending": "meter.pending",
        }
        if error is not None:
            packet.update(
                exception=type(error).__name__,
                errno=getattr(error, "errno", None),
                winerror=getattr(error, "winerror", None),
            )
        body = (json.dumps(packet) + "\n").encode()
        if len(body) > 512:
            raise ValueError("Diagnostic packet boundary")
        self.journal.write(body)
        self.journal.flush()
        os.fsync(self.journal.fileno())
        self.packets += 1

    def save(self, value: dict) -> None:
        temporary, stream = self.contained("meter.pending"), None
        try:
            for stage in STAGES:
                self.trace(stage, "before")
                try:
                    if stage in self.faults:
                        raise self.faults[stage]
                    if stage == "open_temp":
                        stream = temporary.open("x", encoding="utf-8")
                    elif stage == "write_json":
                        json.dump(value, stream, indent=2)
                    elif stage == "flush":
                        stream.flush()
                    elif stage == "fsync":
                        os.fsync(stream.fileno())
                    elif stage == "close_temp":
                        stream.close()
                    elif stage == "replace_target":
                        os.replace(temporary, self.path)
                except (OSError, ValueError, TypeError) as error:
                    self.trace(stage, "failure", error)
                    raise PersistenceFailure(stage, error) from None
                self.trace(stage, "success")
        finally:
            if stream is not None and not stream.closed:
                try:
                    stream.close()
                except OSError as error:
                    self.trace("cleanup_close", "failure", error)
                    raise PersistenceFailure("cleanup_close", error) from None
                self.trace("cleanup_close", "success")

    def reserve_body(self, category: str, amount: int) -> None:
        value = self.state()
        limits = {"metadata": 4 * MIB, "asset": 8 * MIB}
        if (
            category not in limits
            or amount <= 0
            or value["body_reserved"][category] + amount > limits[category]
        ):
            raise ValueError("Continuation body precharge boundary")
        super().reserve_body(category, amount)

    def transaction(self, url: str) -> int:
        allowed_url(url)
        value = self.state()
        if (
            value["http_reserved"] >= 40
            or value["body_reserved"]["metadata"] + 4097 > 4 * MIB
        ):
            raise ValueError("Continuation transaction precharge boundary")
        return super().transaction(url)

    def output(self, name: str, data: bytes) -> None:
        self.state()
        if self.tree_bytes() + len(data) >= 16 * MIB - 8192:
            raise ValueError("Continuation write boundary")
        super().output(name, data)

    def claim(self) -> None:
        self.output(
            "worker-claim.json",
            json.dumps({"pid": os.getpid(), "no_retry": True}).encode(),
        )


def fetch(
    budget: Budget, url: str, category: str, limit: int, size=None, digest=None
) -> bytes:
    """The old transport operates only through the injected narrower policy."""
    allowed_url(url)
    caps = {"asset": 4 * MIB, "metadata": MIB}
    if category not in caps or not 0 < limit <= caps[category]:
        raise ValueError("Continuation per-body boundary")

    def identity(value: str):
        path = urllib.parse.urlsplit(value).path
        for publisher, revision, files in REMAINING:
            if value == tree_url(publisher, revision):
                return publisher, revision, "tree"
            for filename in files:
                if path in {
                    urllib.parse.urlsplit(
                        asset_url(publisher, revision, filename)
                    ).path,
                    f"/api/resolve-cache/models/{publisher}/{revision}/{filename}",
                }:
                    return publisher, revision, filename
        raise ValueError("Logical artifact identity")

    expected = identity(url)

    def scoped_policy(value: str) -> None:
        allowed_url(value)
        if identity(value) != expected:
            raise ValueError("Cross-artifact redirect")

    previous = BASE.allowed_url
    BASE.allowed_url = scoped_policy
    try:
        return BASE.fetch(budget, url, category, limit, size, digest)
    finally:
        BASE.allowed_url = previous


def select_item(listing, filename: str) -> dict:
    if not isinstance(listing, list):
        raise TypeError("Publisher list required")
    matches = [
        v
        for v in listing
        if isinstance(v, dict) and v.get("path") == filename and v.get("type") == "file"
    ]
    if len(matches) != 1:
        raise ValueError("Publisher inventory mismatch")
    item = matches[0]
    if type(item.get("size")) is not int or not 0 < item["size"] <= 4 * MIB:
        raise ValueError("Publisher exact size boundary")
    return item


def scalar_text(values: dict) -> str:
    """Reject provider/arbitrary objects instead of recursively serializing them."""
    if type(values) is not dict or len(values) > 32:
        raise TypeError("Scalar report object required")
    for key, value in values.items():
        if type(key) is not str or len(key) > 48:
            raise TypeError("Scalar report key required")
        if type(value) not in {str, int, bool, type(None)}:
            raise TypeError("Scalar report value required")
        if isinstance(value, str) and len(value) > 512:
            raise ValueError("Scalar report field boundary")
    text = json.dumps(values)
    if len((text + "\n").encode()) > 16384:
        raise ValueError("Scalar report invocation boundary")
    return text


def report_scalar(root: Path, values: dict) -> None:
    """Durably charge controlled stdout before emission, reserving closure space."""
    text = scalar_text(values)
    count = len((text + "\n").encode())
    path = root / "reporting.jsonl"
    if BASE.is_reparse(path):
        raise ValueError("Reporting path boundary")
    total = sum(
        json.loads(line)["bytes"] for line in path.read_text().splitlines() if line
    )
    if total + count > 114688:
        raise ValueError("Scalar report aggregate boundary")
    with path.open("ab") as stream:
        stream.write(
            (json.dumps({"bytes": count, "kind": "worker_stdout"}) + "\n").encode()
        )
        stream.flush()
        os.fsync(stream.fileno())
    print(text)


def acquire_remaining(budget: Budget) -> None:
    budget.claim()
    for publisher, revision, files in REMAINING:
        listing = json.loads(
            fetch(budget, tree_url(publisher, revision), "metadata", MIB - 1)
        )
        for filename in files:
            item = select_item(listing, filename)
            body = fetch(
                budget,
                asset_url(publisher, revision, filename),
                "asset",
                item["size"],
                item["size"],
            )
            identity = BASE.asset_identity(body, item)
            stored = ("qwen-" if publisher.startswith("Qwen/") else "nomic-") + filename
            budget.output(stored, body)
            budget.report(
                stored + "-identity.json",
                {
                    "publisher": publisher,
                    "revision": revision,
                    "filename": filename,
                    "status": "static_only_not_approved_for_loading",
                    **identity,
                },
            )


def main() -> None:
    """One fixed-root worker; terminal reports never contain raw exception text."""
    budget = Budget(RUN)
    try:
        try:
            acquire_remaining(budget)
            result = {"status": "completed_static_only_no_adoption"}
        except Exception as error:  # noqa: BLE001 -- terminal receipt, never retry
            result = {
                "status": "stopped_no_retry",
                "exception": type(error).__name__,
                "stage": error.stage if isinstance(error, PersistenceFailure) else None,
                "errno": getattr(error, "errno", None),
                "winerror": getattr(error, "winerror", None),
            }
        budget.report("worker-result.json", result)
    finally:
        budget.close()
    report_scalar(RUN, result)
    if result["status"] != "completed_static_only_no_adoption":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
