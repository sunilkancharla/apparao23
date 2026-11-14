"""Synthetic-only T12 SQLite baseline; not an application storage module."""

from __future__ import annotations

import ctypes
import hashlib
import json
import math
import random
import re
import sqlite3
import statistics
import struct
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "data/t12/storage-baseline-01"
FIXTURES = json.loads(Path(__file__).with_name("storage-fixtures.json").read_bytes())
VERSION = FIXTURES["version_key"]
ANCHOR = '{"pdf_page":1,"xlsx_sheet":"Synthetic","cells":"A1:B2","csv_records":[1,2],"columns":["a","b"],"physical_lines":[2,3],"synthetic_only":true}'
DIM = 768


def save(path: Path, value: object) -> None:
    """Persist a scalar/authored fixture receipt atomically, without retries."""
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2), encoding="utf-8")
    temporary.replace(path)


def pack_vector(vector: list[float] | tuple[float, ...]) -> bytes:
    """Validate and normalize finite nonzero inputs, then freeze float32 bytes."""
    if len(vector) != DIM or any(not math.isfinite(x) for x in vector):
        raise ValueError("Invalid vector dimension/components")
    norm = math.sqrt(math.fsum(x * x for x in vector))
    if not math.isfinite(norm) or norm <= 0:
        raise ValueError("Invalid vector norm")
    blob = struct.pack("<768f", *(x / norm for x in vector))
    unpack_vector(blob)
    return blob


def unpack_vector(blob: bytes) -> tuple[float, ...]:
    """Reject corrupt stored vectors rather than returning plausible rankings."""
    if len(blob) != DIM * 4:
        raise ValueError("Invalid vector bytes")
    values = struct.unpack("<768f", blob)
    if (
        any(not math.isfinite(x) for x in values)
        or math.fsum(x * x for x in values) <= 0
    ):
        raise ValueError("Invalid stored vector")
    return values


def reference_rank(rows: list, query: list[float]) -> list:
    """Independent exhaustive L2-normalized dot reference using math.fsum."""
    q = struct.unpack("<768f", pack_vector(query))
    qnorm = math.sqrt(math.fsum(x * x for x in q))
    output = []
    for identity, blob in rows:
        values = struct.unpack("<768f", blob)
        dot = math.fsum(values[i] * q[i] for i in range(DIM))
        norm = math.sqrt(math.fsum(x * x for x in values))
        output.append((identity, 1 - dot / (norm * qnorm)))
    return sorted(output, key=lambda row: (row[1], row[0]))[:5]


class Store:
    """Small synthetic fixture store with explicit ownership and version checks."""

    def __init__(self, root: Path):
        if root.is_symlink() or not root.resolve().is_relative_to(RUN.resolve()):
            raise ValueError("Fixture root outside allocation")
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.safe("originals").mkdir(exist_ok=True)
        self.con = sqlite3.connect(self.safe("store.sqlite"), isolation_level=None)
        self.con.execute("PRAGMA foreign_keys=ON")
        self.con.execute("PRAGMA journal_mode=DELETE")
        self.con.execute("PRAGMA synchronous=FULL")
        self.con.executescript("""
            CREATE TABLE IF NOT EXISTS contents(hash TEXT PRIMARY KEY, state TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS documents(id TEXT PRIMARY KEY, hash TEXT NOT NULL
                REFERENCES contents(hash), owner TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS refs(conversation TEXT, doc TEXT REFERENCES documents(id)
                ON DELETE CASCADE, PRIMARY KEY(conversation,doc));
            CREATE TABLE IF NOT EXISTS chunks(id TEXT PRIMARY KEY, doc TEXT REFERENCES documents(id)
                ON DELETE CASCADE, version TEXT NOT NULL, vector BLOB NOT NULL, anchor TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS historical_records(id TEXT PRIMARY KEY, opaque TEXT);
        """)

    def close(self) -> None:
        """Close this fixture connection."""
        self.con.close()

    def safe(self, relative: str) -> Path:
        """Allow only safe relative fixture names, rejecting links and escape."""
        if (
            not re.fullmatch(r"[A-Za-z0-9_./-]+", relative)
            or ".." in Path(relative).parts
        ):
            raise ValueError("Unsafe fixture path")
        target = self.root / relative
        if Path(relative).is_absolute() or not target.resolve().is_relative_to(
            self.root
        ):
            raise ValueError("Unsafe fixture path")
        if any(
            p.is_symlink()
            for p in [target, *target.parents]
            if p.is_relative_to(self.root)
        ):
            raise ValueError("Linked fixture path")
        return target

    def write_original(self, content: bytes) -> Path:
        """Write owned synthetic bytes and a recoverable staging marker."""
        sha = hashlib.sha256(content).hexdigest()
        path = self.safe("originals/" + sha)
        if path.exists() and path.read_bytes() != content:
            raise ValueError("Content hash mismatch")
        save(
            self.safe(sha + ".owned.json"), {"owner": FIXTURES["version"], "hash": sha}
        )
        if not path.exists():
            path.write_bytes(content)
        return path

    def add_document(
        self, identity: str, content: bytes, owner: str, refs: list[str]
    ) -> None:
        """Deduplicate bytes while retaining separate immutable document ownership."""
        sha = hashlib.sha256(content).hexdigest()
        old = self.con.execute(
            "SELECT hash,owner FROM documents WHERE id=?", (identity,)
        ).fetchone()
        if old:
            existing = [
                x[0]
                for x in self.con.execute(
                    "SELECT conversation FROM refs WHERE doc=? ORDER BY 1", (identity,)
                )
            ]
            if old != (sha, owner) or sorted(set(refs)) != existing:
                raise ValueError("Document identity/ownership drift")
            return
        if owner != "library" and set(refs) != {owner}:
            raise ValueError("Exclusive reference mismatch")
        self.write_original(content)
        try:
            self.con.execute("BEGIN IMMEDIATE")
            self.con.execute(
                "INSERT OR IGNORE INTO contents VALUES (?, 'ready')", (sha,)
            )
            self.con.execute(
                "INSERT INTO documents VALUES (?,?,?)", (identity, sha, owner)
            )
            self.con.executemany(
                "INSERT INTO refs VALUES (?,?)",
                [(r, identity) for r in sorted(set(refs))],
            )
            self.con.commit()
        except BaseException:
            self.con.rollback()
            raise
        self.safe(sha + ".owned.json").unlink()

    def add_chunk(
        self, identity: str, doc: str, vector: list[float], version: str
    ) -> None:
        """Store an idempotent versioned chunk and nominal synthetic provenance."""
        if version != VERSION:
            raise ValueError("Unapproved fixture vector version")
        row = (identity, doc, version, pack_vector(vector), ANCHOR)
        old = self.con.execute(
            "SELECT * FROM chunks WHERE id=?", (identity,)
        ).fetchone()
        if old and old != row:
            raise ValueError("Chunk identity drift")
        self.con.execute("INSERT OR IGNORE INTO chunks VALUES (?,?,?,?,?)", row)

    def content_path(self, doc: str) -> Path:
        """Resolve original bytes through the document's stored content identity."""
        row = self.con.execute(
            "SELECT hash FROM documents WHERE id=?", (doc,)
        ).fetchone()
        if not row:
            raise ValueError("Unknown document")
        return self.safe("originals/" + row[0])

    def eligible(self, conversation: str, version: str) -> list:
        """Authorize scope before ranking and reject incompatible/non-ready state."""
        if version != VERSION:
            raise ValueError("Query model/prefix/extraction mismatch")
        docs = self.con.execute(
            "SELECT d.id,c.hash,c.state FROM refs r JOIN documents d ON r.doc=d.id JOIN contents c ON c.hash=d.hash WHERE r.conversation=?",
            (conversation,),
        ).fetchall()
        for _, sha, state in docs:
            path = self.safe("originals/" + sha)
            if (
                state != "ready"
                or not path.is_file()
                or hashlib.sha256(path.read_bytes()).hexdigest() != sha
            ):
                raise ValueError("Original missing/corrupt/non-ready")
        rows = self.con.execute(
            "SELECT c.id,c.vector,c.version FROM chunks c JOIN refs r ON r.doc=c.doc WHERE r.conversation=? ORDER BY c.id",
            (conversation,),
        ).fetchall()
        if any(row[2] != version for row in rows):
            raise ValueError("Stored extraction/model version mismatch")
        return [(identity, vector) for identity, vector, _ in rows]

    def search(self, conversation: str, query: list[float], version: str) -> list:
        """Exact cosine over scoped float32 values; stable IDs break exact ties."""
        q = unpack_vector(pack_vector(query))
        qnorm = math.sqrt(sum(x * x for x in q))
        scored = []
        for identity, blob in self.eligible(conversation, version):
            values = unpack_vector(blob)
            norm = math.sqrt(sum(x * x for x in values))
            score = 1 - sum(x * y for x, y in zip(values, q, strict=True)) / (
                norm * qnorm
            )
            scored.append((identity, score))
        return sorted(scored, key=lambda row: (row[1], row[0]))[:5]

    def rebuild(self, identity: str, vector: list[float], version: str) -> None:
        """Rebuild a disposable fixture vector without changing source identity/anchor."""
        if version != VERSION:
            raise ValueError("Rebuild version mismatch")
        self.con.execute(
            "UPDATE chunks SET vector=?,version=? WHERE id=?",
            (pack_vector(vector), version, identity),
        )

    def count(self, table: str) -> int:
        """Return counts only for the authored schema allowlist."""
        if table not in {"contents", "documents", "refs", "chunks"}:
            raise ValueError("Unknown fixture table")
        return self.con.execute("SELECT count(*) FROM " + table).fetchone()[0]

    def document_ids(self) -> list:
        """List stable fixture document identities."""
        return [x[0] for x in self.con.execute("SELECT id FROM documents ORDER BY id")]

    def purge_unreferenced(self) -> None:
        """Remove only known synthetic content with no remaining document owner."""
        rows = self.con.execute(
            "SELECT hash FROM contents WHERE hash NOT IN (SELECT hash FROM documents)"
        ).fetchall()
        for (sha,) in rows:
            path = self.safe("originals/" + sha)
            if hashlib.sha256(path.read_bytes()).hexdigest() != sha:
                raise ValueError("Refuse deleting modified fixture")
            save(
                self.safe(sha + ".owned.json"),
                {"owner": FIXTURES["version"], "hash": sha},
            )
            self.con.execute("DELETE FROM contents WHERE hash=?", (sha,))
            path.unlink()
            self.safe(sha + ".owned.json").unlink()

    def delete_conversation(self, conversation: str) -> None:
        """Apply only the approved exclusive/shared deletion invariant to fixtures."""
        if conversation == "library":
            raise ValueError("Reserved library ownership is not a conversation")
        self.con.execute("BEGIN IMMEDIATE")
        try:
            self.con.execute("DELETE FROM refs WHERE conversation=?", (conversation,))
            self.con.execute("DELETE FROM documents WHERE owner=?", (conversation,))
            self.con.commit()
        except BaseException:
            self.con.rollback()
            raise
        self.purge_unreferenced()

    def remove_library(self, identity: str) -> None:
        """Block referenced library removal before any state/byte mutation."""
        if self.con.execute("SELECT 1 FROM refs WHERE doc=?", (identity,)).fetchone():
            raise ValueError("Warning: library document has dependent conversations")
        self.con.execute(
            "DELETE FROM documents WHERE id=? AND owner='library'", (identity,)
        )
        self.purge_unreferenced()

    def reconcile(self) -> dict:
        """Report owned staging/orphan state without deleting unknown bytes."""
        result = {"orphan_markers": 0, "cleanup_markers": 0}
        for path in self.root.glob("*.owned.json"):
            record = json.loads(self.safe(path.name).read_bytes())
            sha = record.get("hash", "")
            if record.get("owner") != FIXTURES["version"] or not re.fullmatch(
                "[a-f0-9]{64}", sha
            ):
                raise ValueError("Unowned reconciliation marker")
            exists = self.con.execute(
                "SELECT 1 FROM contents WHERE hash=?", (sha,)
            ).fetchone()
            result["cleanup_markers" if exists else "orphan_markers"] += 1
        return result


def check_budget(state: dict, category: str, slots: int) -> None:
    """Refuse category exhaustion or the single active deadline."""
    started = state.get("started", 0)
    if (
        time.time() - started >= 2700
        or state["used"][category] + slots > state["limits"][category]
    ):
        raise RuntimeError("Shared execution budget exhausted")


def charge(category: str, slots: int) -> None:
    """Persist every owned process reservation before its launch."""
    path = RUN / "budget.json"
    state = json.loads(path.read_text(encoding="utf-8-sig"))
    from datetime import datetime

    state["started"] = datetime.fromisoformat(state["started_utc"]).timestamp()
    if state["status"] != "active":
        raise RuntimeError("Closed allocation")
    check_budget(state, category, slots)
    state["used"][category] += slots
    save(path, state)


def check_sample(sample: dict, gap: float) -> None:
    """Apply unchanged sampled controller/headroom and observation-gap guards."""
    if (
        not math.isfinite(gap)
        or gap < 0
        or gap > 0.3
        or sample["available"] < 4 * 1024**3
        or sample["controller"] > 512 * 1024**2
    ):
        raise RuntimeError("Resource observation boundary")


def benchmark(size: int) -> dict:
    """Measure frozen synthetic insert/search/rebuild/reopen, not semantic quality."""
    directory = RUN / f"scale-{size}"
    if directory.exists():
        raise RuntimeError("Never repeat a started scale")
    store = Store(directory)
    try:
        rng = random.Random(FIXTURES["seed"] + size)
        blobs = [
            pack_vector([rng.uniform(-1, 1) for _ in range(DIM)]) for _ in range(size)
        ]
        frozen_hash = hashlib.sha256(b"".join(blobs)).hexdigest()
        store.add_document("fixture", b"synthetic baseline original", "library", ["a"])
        rows = [
            (f"c{i:05d}", "fixture", VERSION, blob, ANCHOR)
            for i, blob in enumerate(blobs)
        ]
        started = time.perf_counter()
        store.con.execute("BEGIN IMMEDIATE")
        store.con.executemany("INSERT INTO chunks VALUES (?,?,?,?,?)", rows)
        store.con.commit()
        insert_seconds = time.perf_counter() - started
        queries = [list(unpack_vector(blobs[(i * 7919) % size])) for i in range(12)]
        expected = [
            reference_rank([(r[0], r[3]) for r in rows], query) for query in queries
        ]
        passes = []
        for _ in range(4):
            times = []
            for query, gold in zip(queries, expected, strict=True):
                started = time.perf_counter()
                actual = store.search("a", query, VERSION)
                times.append(time.perf_counter() - started)
                if [x[0] for x in actual] != [x[0] for x in gold] or any(
                    abs(a[1] - b[1]) > 1e-6 for a, b in zip(actual, gold, strict=True)
                ):
                    raise RuntimeError("Independent ranking mismatch")
            passes.append(
                {
                    "query_seconds": times,
                    "median": statistics.median(times),
                    "maximum": max(times),
                }
            )
        started = time.perf_counter()
        store.con.execute("BEGIN IMMEDIATE")
        store.con.execute("DELETE FROM chunks")
        store.con.executemany("INSERT INTO chunks VALUES (?,?,?,?,?)", rows)
        store.con.commit()
        rebuild_seconds = time.perf_counter() - started
        store.close()
        started = time.perf_counter()
        store = Store(directory)
        if (
            store.count("chunks") != size
            or store.con.execute("PRAGMA integrity_check").fetchone()[0] != "ok"
        ):
            raise RuntimeError("Reopen/rebuild integrity failure")
        restart_seconds = time.perf_counter() - started
        return {
            "size": size,
            "vector_sha256": frozen_hash,
            "query_sha256": hashlib.sha256(
                b"".join(pack_vector(q) for q in queries)
            ).hexdigest(),
            "passes": passes,
            "insert_seconds": insert_seconds,
            "rebuild_seconds": rebuild_seconds,
            "restart_seconds": restart_seconds,
            "journal_mode": store.con.execute("PRAGMA journal_mode").fetchone()[0],
            "synchronous": store.con.execute("PRAGMA synchronous").fetchone()[0],
            "database_bytes": store.safe("store.sqlite").stat().st_size,
            "directory_bytes": sum(
                p.stat().st_size for p in directory.rglob("*") if p.is_file()
            ),
            "ranking_comparisons": 48,
        }
    finally:
        store.close()


def crash_worker(case: str) -> None:
    """Pause at a frozen commit/file boundary until the owner terminates us."""
    if case not in FIXTURES["crash_cases"]:
        raise ValueError("Unknown crash case")
    store = Store(RUN / case)
    store.add_document("stable", b"stable synthetic bytes", "library", ["a", "b"])
    store.add_chunk("stable", "stable", [1.0] + [0.0] * 767, VERSION)
    if case in {"file-before-commit", "commit-before-cleanup"}:
        original = store.write_original(b"pending synthetic bytes")
        sha = original.name
    else:
        sha = hashlib.sha256(b"stable synthetic bytes").hexdigest()
    store.con.execute("BEGIN IMMEDIATE")
    store.con.execute("INSERT OR IGNORE INTO contents VALUES (?, 'ready')", (sha,))
    store.con.execute("INSERT INTO documents VALUES ('new',?,'a')", (sha,))
    store.con.execute("INSERT INTO refs VALUES ('a','new')")
    store.con.execute(
        "INSERT INTO chunks VALUES ('new','new',?,?,?)",
        (VERSION, pack_vector([0.0, 1.0] + [0.0] * 766), ANCHOR),
    )
    if case in {"after-commit", "commit-before-cleanup"}:
        store.con.commit()
    save(
        RUN / "ready.json",
        {"case": case, "transaction_committed": not store.con.in_transaction},
    )
    time.sleep(120)
    raise RuntimeError("Owner did not terminate crash worker")


def verify_crash(case: str) -> dict:
    """Reopen in a separate process and verify exact durable state after termination."""
    store = Store(RUN / case)
    try:
        committed = case in {"after-commit", "commit-before-cleanup"}
        expected = 2 if committed else 1
        counts = {
            table: store.count(table)
            for table in ("documents", "chunks", "refs", "contents")
        }
        if counts != {
            "documents": expected,
            "chunks": expected,
            "refs": expected + 1,
            "contents": 2 if case == "commit-before-cleanup" else 1,
        }:
            raise RuntimeError("Crash atomicity/reference invariant")
        if (
            store.con.execute("PRAGMA integrity_check").fetchone()[0] != "ok"
            or store.con.execute("PRAGMA foreign_key_check").fetchall()
        ):
            raise RuntimeError("Crash database integrity failure")
        if len(store.search("a", [1.0] + [0.0] * 767, VERSION)) != expected:
            raise RuntimeError("Crash retrieval scope failure")
        reconciliation = store.reconcile()
        if reconciliation != {
            "orphan_markers": int(case == "file-before-commit"),
            "cleanup_markers": int(case == "commit-before-cleanup"),
        }:
            raise RuntimeError("Crash file reconciliation invariant")
        return {
            "case": case,
            "counts": counts,
            "integrity": "ok",
            "reconciliation": reconciliation,
            "separate_process_reopen": True,
        }
    finally:
        store.close()


class Runner:
    """Own suspended workers under an aggregate Windows Job and shared budget."""

    def __init__(self):
        from appcontainer_preflight import ExtendedLimits, Native

        self.native = Native()
        self.extended = ExtendedLimits
        self.job = self.native.job(2, kill=False)
        limits = ExtendedLimits()
        limits.basic.flags = 0x8 | 0x200
        limits.basic.active = 2
        limits.job_memory = 2 * 1024**3
        self.native.check(
            self.native.kernel.SetInformationJobObject(
                self.job, 9, ctypes.byref(limits), ctypes.sizeof(limits)
            )
        )
        self.native.check(
            self.native.kernel.AssignProcessToJobObject(
                self.job, self.native.kernel.GetCurrentProcess()
            )
        )
        actual = ExtendedLimits()
        self.native.check(
            self.native.kernel.QueryInformationJobObject(
                self.job, 9, ctypes.byref(actual), ctypes.sizeof(actual), None
            )
        )
        if actual.job_memory != limits.job_memory or actual.basic.flags & 0x100:
            raise RuntimeError("Aggregate job setup mismatch")
        self.samples, self.launches = [], 0
        self.last_read = None

    def sample(self) -> None:
        """Measure controller/headroom, aggregate job commit and live artifact size."""
        from embedding_budget import memory_snapshot

        started = time.monotonic()
        reading = memory_snapshot()
        completed = time.monotonic()
        gap = 0 if self.last_read is None else completed - self.last_read
        sample = {
            "available": reading["available_physical"],
            "controller": reading["controller_private"],
        }
        check_sample(sample, gap)
        self.last_read = completed
        actual = self.extended()
        self.native.check(
            self.native.kernel.QueryInformationJobObject(
                self.job, 9, ctypes.byref(actual), ctypes.sizeof(actual), None
            )
        )
        sample["job_peak"] = actual.peak_job
        total = 0
        if not RUN.is_dir() or RUN.is_symlink() or RUN.is_junction():
            raise RuntimeError("Trial root identity changed")
        for path in RUN.rglob("*"):
            if path.is_symlink() or path.is_junction():
                raise RuntimeError("Unexpected link in trial root")
            try:
                if path.is_file():
                    total += path.stat().st_size
            except FileNotFoundError:
                # Live rollback journals may disappear; never ignore a missing root.
                if not RUN.is_dir():
                    raise
        if (
            total > 512 * 1024**2
            or actual.peak_job > 2 * 1024**3
            or completed - started > 0.3
            or time.monotonic() - started > 0.3
        ):
            raise RuntimeError("Disk/job/collection boundary")
        sample.update(gap=gap, disk_bytes=total)
        self.samples.append(sample)
        state = json.loads((RUN / "budget.json").read_text(encoding="utf-8-sig"))
        check_budget({**state, "started": state["started"]}, "workers", 0)

    def run(self, mode: str, value: str) -> dict:
        """Launch exactly one counted worker; crash termination uses its owned handle."""
        from ctypes import wintypes

        from appcontainer_preflight import ProcessInfo, Startup

        if mode not in {"benchmark", "crash", "verify"}:
            raise ValueError("Worker mode")
        charge("workers", 1)
        self.sample()
        self.launches += 1
        native = self.native
        child_job = native.job(1, kill=True)
        child_limits = self.extended()
        child_limits.basic.flags = 0x8 | 0x2000
        child_limits.basic.active = 1
        native.check(
            native.kernel.SetInformationJobObject(
                child_job, 9, ctypes.byref(child_limits), ctypes.sizeof(child_limits)
            )
        )
        startup, process = Startup(), ProcessInfo()
        startup.cb = ctypes.sizeof(startup)
        startup.flags, startup.show = 1, 0
        command = f'"F:\\Python\\Python314\\python.exe" -I -S -B "{Path(__file__).resolve()}" {mode} {value}'
        began, created, crash_killed = time.monotonic(), False, False
        if (RUN / "ready.json").exists():
            (RUN / "ready.json").unlink()
        try:
            native.check(
                native.kernel.CreateProcessW(
                    None,
                    ctypes.create_unicode_buffer(command),
                    None,
                    None,
                    False,
                    4,
                    None,
                    str(ROOT),
                    ctypes.byref(startup),
                    ctypes.byref(process),
                )
            )
            created = True
            native.check(
                native.kernel.AssignProcessToJobObject(child_job, process.process)
            )
            if native.kernel.ResumeThread(process.thread) == 0xFFFFFFFF:
                raise ctypes.WinError(ctypes.get_last_error())
            while native.kernel.WaitForSingleObject(process.process, 0) == 0x102:
                iteration = time.monotonic()
                self.sample()
                if iteration - began > 120:
                    raise RuntimeError("Worker deadline")
                if mode == "crash" and (RUN / "ready.json").exists():
                    marker = json.loads((RUN / "ready.json").read_bytes())
                    if marker["case"] != value:
                        raise RuntimeError("Wrong crash marker")
                    native.check(native.kernel.TerminateProcess(process.process, 125))
                    crash_killed = True
                time.sleep(max(0, 0.1 - (time.monotonic() - iteration)))
            code = wintypes.DWORD()
            native.check(
                native.kernel.GetExitCodeProcess(process.process, ctypes.byref(code))
            )
            if code.value != (125 if mode == "crash" else 0) or (
                mode == "crash" and not crash_killed
            ):
                raise RuntimeError("Worker exit/crash evidence failure")
            if native.accounting(child_job)["active"]:
                raise RuntimeError("Worker not reaped")
            if native.accounting(self.job) != {
                "total": self.launches + 1,
                "active": 1,
                "terminated": self.launches,
            }:
                # Kernel terminated-count semantics are observed below; total/active are binding.
                account = native.accounting(self.job)
                if account["total"] != self.launches + 1 or account["active"] != 1:
                    raise RuntimeError("Unexpected native descendant")
            if mode == "crash":
                return {
                    "case": value,
                    "terminated_by_owned_handle": True,
                    "exit_code": code.value,
                }
            return json.loads((RUN / f"{mode}-{value}.json").read_bytes())
        finally:
            if created:
                native.kernel.TerminateJobObject(child_job, 125)
                if (
                    native.kernel.WaitForSingleObject(process.process, 5000) != 0
                    or native.accounting(child_job)["active"]
                ):
                    raise RuntimeError("Owned teardown uncertain")
                native.kernel.CloseHandle(process.thread)
                native.kernel.CloseHandle(process.process)
            native.kernel.CloseHandle(child_job)

    def close(self) -> None:
        """Close the non-killing aggregate job after verifying no workers remain."""
        if self.native.accounting(self.job)["active"] != 1:
            raise RuntimeError("Outstanding owned workers")
        self.native.kernel.CloseHandle(self.job)


def run_evaluation() -> None:
    """Execute one frozen schedule and always save sanitized success/stop evidence."""
    if (RUN / "execution-started.json").exists():
        raise RuntimeError("Never reset or repeat a started storage allocation")
    charge("tests", 1)
    save(
        RUN / "execution-started.json",
        {
            "started": time.time(),
            "fixture_sha256": hashlib.sha256(
                Path(__file__).with_name("storage-fixtures.json").read_bytes()
            ).hexdigest(),
        },
    )
    runner = Runner()
    result = {
        "status": "started",
        "scales": [],
        "crashes": [],
        "teardown_verified": False,
    }
    try:
        for case in FIXTURES["crash_cases"]:
            terminated = runner.run("crash", case)
            checked = runner.run("verify", case)
            result["crashes"].append({**terminated, **checked})
            save(RUN / "summary.json", result)
        for size in FIXTURES["sizes"]:
            result["scales"].append(runner.run("benchmark", str(size)))
            save(RUN / "summary.json", result)
        result["status"] = "completed_baseline_no_adoption"
    except BaseException as error:
        result.update(
            status="stopped_no_automatic_retry",
            error_type=type(error).__name__,
            reason=str(error),
        )
        raise
    finally:
        runner.close()
        result["teardown_verified"] = True
        result["resource_samples"] = len(runner.samples)
        if runner.samples:
            result["resources"] = {
                "minimum_available": min(x["available"] for x in runner.samples),
                "maximum_controller": max(x["controller"] for x in runner.samples),
                "maximum_job_peak": max(x["job_peak"] for x in runner.samples),
                "maximum_gap": max(x["gap"] for x in runner.samples),
                "maximum_disk": max(x["disk_bytes"] for x in runner.samples),
            }
        result["environment"] = {
            "python": sys.version,
            "sqlite": sqlite3.sqlite_version,
            "compile_options": [
                r[0]
                for r in sqlite3.connect(":memory:").execute("PRAGMA compile_options")
            ],
        }
        save(RUN / "summary.json", result)
        print(
            json.dumps(
                {
                    "status": result["status"],
                    "teardown_verified": True,
                    "scales": len(result["scales"]),
                    "crashes": len(result["crashes"]),
                }
            )
        )


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    args = sys.argv[1:]
    if args == ["run"]:
        run_evaluation()
    elif len(args) == 2 and args[0] in {"benchmark", "crash", "verify"}:
        mode, value = args
        if mode == "benchmark" and value in {str(n) for n in FIXTURES["sizes"]}:
            save(RUN / f"benchmark-{value}.json", benchmark(int(value)))
        elif mode == "crash" and value in FIXTURES["crash_cases"]:
            crash_worker(value)
        elif mode == "verify" and value in FIXTURES["crash_cases"]:
            save(RUN / f"verify-{value}.json", verify_crash(value))
        else:
            raise SystemExit("Unapproved worker value")
    else:
        raise SystemExit("Expected run or fixed owned worker mode")
