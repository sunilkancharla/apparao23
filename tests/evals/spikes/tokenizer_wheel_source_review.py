"""Bounded, data-only WSP evaluation; never an application tokenizer loader."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import stat
import sys
import types
import zipfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ReportGate:
    """Charge UTF-8 output before display, reserving mandatory closeout."""

    limit: int = 65536
    reserve: int = 16384
    used: int = 0

    def admit(self, value: object, *, closure: bool = False) -> bytes:
        """Serialize once and refuse before returning displayable bytes."""
        raw = json.dumps(value, ensure_ascii=False).encode("utf-8")
        ceiling = self.limit if closure else self.limit - self.reserve
        if self.used + len(raw) > ceiling:
            raise ValueError("report_reserve")
        self.used += len(raw)
        return raw


ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "data/t17/tokenizer-wheel-source-01"
HELPER = ROOT / "tests/evals/spikes/wheel_static_inspection.py"
HELPER_SHA = "2f8e7b5a67f4cb7a742304b6380e7cee87476ad6b1b4619062c0adc1b7c1e8dd"
INVENTORY = ROOT / "data/t17/input-fit-tokenizer-static-01/tokenizers-inspection.json"
INVENTORY_SHA = "c83fd421d2cc548eeda103e1021cd10247420e232d1589569aced9351dd46ca9"
WHEEL = (
    ROOT
    / "data/t17/input-fit-tokenizer-static-01/tokenizers-0.23.3-cp310-abi3-win_amd64.whl"
)
WHEEL_SHA = "1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3"


def verified_bytes(path: Path, size: int, sha: str) -> bytes:
    """Bind owned/frozen input bytes to stable ordinary single-link identity."""
    for parent in path.parents:
        value = parent.lstat()
        if (
            not stat.S_ISDIR(value.st_mode)
            or getattr(value, "st_file_attributes", 0) & 1024
        ):
            raise ValueError("ancestor_type")
    before = path.lstat()
    if (
        not stat.S_ISREG(before.st_mode)
        or before.st_nlink != 1
        or before.st_size != size
    ):
        raise ValueError("input_type_or_size")
    if getattr(before, "st_file_attributes", 0) & 1024:
        raise ValueError("input_reparse")
    with path.open("rb") as handle:
        opened = os.fstat(handle.fileno())
        raw = handle.read(size + 1)
        after = os.fstat(handle.fileno())

    def identity(item: os.stat_result) -> tuple:
        return item.st_dev, item.st_ino, item.st_size, item.st_mtime_ns, item.st_nlink

    if any(
        identity(before) != identity(item) for item in (opened, after, path.lstat())
    ):
        raise ValueError("input_changed")
    if len(raw) != size or hashlib.sha256(raw).hexdigest() != sha:
        raise ValueError("input_hash")
    return raw


def load_helper() -> types.ModuleType:
    """Execute only hash-bound project-owned definitions, never candidate text."""
    raw = verified_bytes(HELPER, 48153, HELPER_SHA)
    module = types.ModuleType("wsp_owned_zip")
    module.__file__ = str(HELPER)
    sys.modules[module.__name__] = module
    # Bind verified project-owned bytes; candidate text never enters this path.
    exec(compile(raw, str(HELPER), "exec"), module.__dict__)  # noqa: S102
    return module


def source_map(text: str, *, node_limit: int = 50000, depth_limit: int = 128) -> dict:
    """Bound AST traversal; describe executable edges without evaluating them."""
    tree = ast.parse(text)
    stack = [(tree, 0, "module")]
    imports, calls, definitions, count = [], [], [], 0
    while stack:
        node, depth, scope = stack.pop()
        count += 1
        if count > node_limit or depth > depth_limit:
            raise ValueError("ast_budget")
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(
                {
                    "line": node.lineno,
                    "scope": scope,
                    "text": ast.get_source_segment(text, node),
                }
            )
        if isinstance(node, ast.Call):
            calls.append(
                {
                    "line": node.lineno,
                    "scope": scope,
                    "target": ast.unparse(node.func)[:256],
                }
            )
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definitions.append(
                {"line": node.lineno, "kind": type(node).__name__, "name": node.name}
            )
            # Decorators, bases and defaults run at definition time; bodies are distinct.
            for field, value in ast.iter_fields(node):
                children = value if isinstance(value, list) else [value]
                for child in children:
                    if isinstance(child, ast.AST):
                        child_scope = (
                            (
                                "class_body"
                                if isinstance(node, ast.ClassDef)
                                else "lazy_body"
                            )
                            if field == "body"
                            else "definition_time"
                        )
                        stack.append((child, depth + 1, child_scope))
        else:
            stack.extend(
                (child, depth + 1, scope) for child in ast.iter_child_nodes(node)
            )
    return {
        "nodes": count,
        "imports": imports,
        "calls": calls,
        "definitions": definitions,
        "limitations": "Static syntactic edges only; no resolution of native/external/dynamic behaviour or conditional reachability.",
    }


def read_archive(
    path: Path,
    size: int,
    sha: str,
    inventory: list[dict],
    root: Path,
    *,
    read_limit: int = 8 * 2**20,
    node_limit: int = 50000,
    depth_limit: int = 128,
    helper: types.ModuleType | None = None,
) -> dict:
    """Admit complete ZIP metadata, then read only frozen Python payloads."""
    owned = helper or load_helper()
    budget = owned.Budget(read_limit=read_limit, net_limit=0, expand_limit=96 * 1024)
    limits = owned.Limits(
        max_entries=31,
        max_depth=8,
        max_expanded=16 * 2**20,
        max_central=64 * 1024,
        max_notice=0,
        max_notices_total=0,
    )
    expected = {item["name"]: item for item in inventory}
    if len(expected) != len(inventory):
        raise ValueError("inventory_alias")
    selected = {name: item for name, item in expected.items() if name.endswith(".py")}
    if not selected or any(item["bytes"] > 32768 for item in selected.values()):
        raise ValueError("source_size")
    if sum(item["bytes"] for item in selected.values()) > 96 * 1024:
        raise ValueError("source_total")
    sources, nodes = [], 0
    with owned.open_regular(path, root) as handle:
        if os.fstat(handle.fileno()).st_size != size:
            raise ValueError("outer_size")
        if owned.digest_stream(handle, size, budget) != sha:
            raise ValueError("outer_hash")
        charged = owned.ChargedFile(handle, budget)
        owned.central_admission(charged, limits)
        with zipfile.ZipFile(charged) as archive:
            entries = owned.admitted_entries(archive, limits)
            actual = {entry.filename: entry.file_size for entry in entries}
            if actual != {name: item["bytes"] for name, item in expected.items()}:
                raise ValueError("inventory_mismatch")
            owned.local_layout(charged, archive, entries)
            for entry in entries:
                if entry.filename not in selected:
                    continue
                # Conservative lease before decompression, plus helper's actual-byte charge.
                budget.reserve(entry.file_size + 1)
                digest, raw = owned.member_bytes(archive, entry, budget, cap=32768)
                if digest.hex() != selected[entry.filename]["sha256"]:
                    raise ValueError("member_hash")
                text = raw.decode("utf-8", "strict")
                mapped = source_map(
                    text, node_limit=node_limit - nodes, depth_limit=depth_limit
                )
                nodes += mapped["nodes"]
                sources.append(
                    {
                        "name": entry.filename,
                        "bytes": len(raw),
                        "sha256": digest.hex(),
                        "text": text,
                        "map": mapped,
                    }
                )
    return {
        "members_admitted": len(entries),
        "sources": sources,
        "ast_nodes": nodes,
        "charged_read_bytes": budget.used,
        "actual_expanded_bytes": budget.expanded,
        "accounting": "Requested compressed/header/hash/probe bytes plus conservative expansion lease AND actual expansion; not OS I/O.",
        "candidate_executed": False,
        "native_members_opened": 0,
    }


def worker_policy(event: str, args: tuple) -> None:
    """Fail closed on worker network, subprocess and candidate native operations."""
    if event.startswith(
        ("socket.", "os.exec", "os.spawn", "os.posix_spawn")
    ) or event in {"subprocess.Popen", "os.system", "ctypes.dlopen", "ctypes.dlsym"}:
        raise PermissionError("worker_policy")
    if (
        event == "import"
        and args
        and str(args[0]).split(".")[0] in {"tokenizers", "huggingface_hub", "hf_xet"}
    ):
        raise PermissionError("candidate_import")


def worker() -> None:
    """Perform the single approved attempt and retain bounded escaped JSON."""
    marker = RUN / "real-attempt.json"
    with marker.open("x", encoding="utf-8") as handle:
        json.dump({"pid": os.getpid(), "attempt": 1}, handle)
    owned = load_helper()
    inventory = json.loads(verified_bytes(INVENTORY, 6824, INVENTORY_SHA))["inventory"]
    selected = [item for item in inventory if item["name"].endswith(".py")]
    if (
        len(inventory) != 31
        or len(selected) != 16
        or sum(item["bytes"] for item in selected) != 66467
    ):
        raise ValueError("frozen_source_set")
    sys.addaudithook(worker_policy)
    result = read_archive(WHEEL, 2872101, WHEEL_SHA, inventory, ROOT, helper=owned)
    raw = json.dumps(result, ensure_ascii=True, indent=2).encode("utf-8")
    if len(raw) > 512 * 1024:
        raise ValueError("source_json_cap")
    with (RUN / "sources.json").open("xb") as handle:
        handle.write(raw)
    gate = ReportGate()
    status = {
        "status": "static_complete_no_adoption",
        "sources": len(result["sources"]),
        "expanded_bytes": result["actual_expanded_bytes"],
        "charged_read_bytes": result["charged_read_bytes"],
        "ast_nodes": result["ast_nodes"],
        "source_json_bytes": len(raw),
    }
    admitted = gate.admit(status)
    (RUN / "worker-report.json").write_bytes(admitted)
    print(admitted.decode("utf-8"))


if __name__ == "__main__":
    if sys.argv[1:] != ["--worker"]:
        raise SystemExit("Only the approved --worker entry point is supported")
    worker()
