"""Approved synthetic PartB harness; DLL loading occurs only in offline workers."""

from __future__ import annotations

import ctypes
import hashlib
import json
import math
import random
import re
import sqlite3
import statistics
import sys
import time
from contextlib import contextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import storage_trial as base

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "data/t12/sqlite-vec-runtime-02"
ASSETS = ROOT / ".venv/.cache/sqlite-vec-review/part-b-02"
CONTRACT_PATH = Path(__file__).with_name("sqlite-vec-runtime-followup.json")
CONTRACT = json.loads(CONTRACT_PATH.read_bytes())
PYTHON = Path("F:/Python/Python314/python.exe")
base.RUN = RUN  # Only this process's fixture root changes; old files are never edited.
IDENTITIES = {
    "vec0.dll": "fcf98662a7ad9dce394b96a88f91032047823831b951c76636787c312a6476e6",
    "LICENSE-MIT": "6ce72bbe12d975bd5286e5ab0a064c069693300c47bccbc57bec18485f1621ea",
    "LICENSE-APACHE": "a38070a94d4afd9cd710e3ce67bd1de78097cfe1784c1f0109ac95d3c196bfdc",
}
_PREPARATION_SEGMENT = None


def digest(path: Path) -> str:
    """Hash regular owned input bytes without loading them."""
    if path.is_symlink() or path.is_junction() or not path.is_file():
        raise ValueError("Missing/linked input")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_run_id(value: str) -> None:
    """Refuse missing, old, traversal and unapproved allocation identities."""
    if value != CONTRACT["run_id"]:
        raise ValueError("Unapproved runtime run ID")


def read_meter() -> dict:
    """Read this allocation only; never reuse an old native epoch."""
    verify_output_root()
    path = RUN / "meter.json"
    if path.is_symlink() or path.is_junction() or path.stat().st_size > 1024**2:
        raise ValueError("Unsafe meter")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def verify_output_root() -> None:
    """Refuse linked or unowned output roots before any receipt write."""
    if not RUN.is_relative_to(ROOT / "data/t12") or not RUN.is_dir():
        raise ValueError("Unapproved output root")
    for path in [RUN, *RUN.parents]:
        if path.is_symlink() or path.is_junction():
            raise ValueError("Linked output ancestor")
        if path == ROOT:
            break
    for name in ("meter.json", "summary.json", "execution-attempt.json"):
        path = RUN / name
        if path.is_symlink() or path.is_junction():
            raise ValueError("Linked runtime receipt")


def check_preparation(state: dict, *, ready: bool = False) -> None:
    """Accumulated active work is bounded; sealed-ready human waiting is excluded."""
    elapsed = state["preparation_seconds"]
    if (
        type(elapsed) not in {int, float}
        or not math.isfinite(elapsed)
        or not 0 <= elapsed <= 1800
        or state["preparation_limit_seconds"] != 1800
    ):
        raise RuntimeError("Preparation time boundary")
    segment = state["active_segment"]
    if segment is not None:
        if ready or segment != _PREPARATION_SEGMENT:
            raise RuntimeError("Uncertain active preparation segment")
        duration = time.monotonic() - segment["started_monotonic"]
        if not 0 <= duration <= 1800 - elapsed:
            raise RuntimeError("Active preparation time boundary")


@contextmanager
def preparation_segment(reason: str):
    """Persist an open segment; interrupted ownership is never silently resumed."""
    global _PREPARATION_SEGMENT
    state = read_meter()
    check_preparation(state, ready=True)
    if state["status"] != "preparing" or state["execution_started"] is not None:
        raise RuntimeError("Preparation state is not fresh")
    segment = {"started_monotonic": time.monotonic(), "reason": reason}
    state["active_segment"] = segment
    base.save(RUN / "meter.json", state)
    _PREPARATION_SEGMENT = segment
    try:
        yield
    finally:
        duration = time.monotonic() - segment["started_monotonic"]
        state = read_meter()
        if state["active_segment"] != segment or duration < 0:
            raise RuntimeError("Preparation segment identity/clock changed")
        state["preparation_seconds"] += duration
        state["active_segment"] = None
        state["events"].append({"preparation_seconds": duration, "reason": reason})
        base.save(RUN / "meter.json", state)
        _PREPARATION_SEGMENT = None
        check_preparation(state, ready=True)


def check_epoch(state: dict) -> None:
    """Enforce the one persisted epoch with wall and system-monotonic clocks."""
    started = state.get("execution_started")
    deadline = state.get("execution_deadline")
    monotonic = state.get("execution_monotonic")
    if any(
        type(v) not in {int, float} or not math.isfinite(v)
        for v in (started, deadline, monotonic)
    ):
        raise RuntimeError("Missing/invalid native epoch")
    wall_elapsed = time.time() - started
    monotonic_elapsed = time.monotonic() - monotonic
    if (
        state["status"] != "offline"
        or deadline != started + 2700
        or not 0 <= wall_elapsed < 2700
        or not 0 <= monotonic_elapsed < 2700
        or abs(wall_elapsed - monotonic_elapsed) > 1
    ):
        raise RuntimeError("Native epoch expired or clocks inconsistent")


def start_execution() -> None:
    """Start once after attestation; no old epoch or consumed handoff can renew."""
    state = read_meter()
    check_preparation(state, ready=True)
    if (
        state["status"] != "ready"
        or state["execution_started"] is not None
        or state["execution_deadline"] is not None
        or state["used"]["workers"] != 2
    ):
        raise RuntimeError("Never renew a native epoch")
    started = time.time()
    state.update(
        status="offline",
        execution_started=started,
        execution_deadline=started + 2700,
        execution_monotonic=time.monotonic(),
    )
    base.save(RUN / "meter.json", state)


def check_charge(state: dict, category: str, amount: int) -> None:
    """Reject category borrowing and overspending before a process launch."""
    if category not in state["limits"] or type(amount) is not int or amount < 0:
        raise ValueError("Invalid budget category/amount")
    if state["used"][category] + amount > state["limits"][category]:
        raise RuntimeError("Shared process category exhausted")


def charge(category: str, amount: int, reason: str) -> None:
    """Persist conservative reservations before normal work; no resetting epochs."""
    state = read_meter()
    check_charge(state, category, amount)
    if state["status"] not in {"preparing", "ready", "offline"}:
        raise RuntimeError("Closed runtime allocation")
    if state["status"] == "preparing":
        check_preparation(state)
        if _PREPARATION_SEGMENT is None:
            raise RuntimeError("Preparation charge outside owned active segment")
    elif state["status"] == "ready":
        check_preparation(state, ready=True)
        if (
            state["execution_started"] is not None
            or state["execution_deadline"] is not None
        ):
            raise RuntimeError("Ready state cannot hide a previous native epoch")
        if category != "workers" or amount != 2 or state["used"]["workers"] != 0:
            raise RuntimeError("Ready state permits only first handoff reservation")
    else:
        check_epoch(state)
    state["used"][category] += amount
    state["events"].append(
        {"category": category, "count": amount, "reason": reason, "at": time.time()}
    )
    base.save(RUN / "meter.json", state)


def verify_assets() -> None:
    """Require the exact DLL and both accepted companion notices before enabling loads."""
    for path in [ASSETS, *ASSETS.parents]:
        if path.is_symlink() or path.is_junction():
            raise ValueError("Linked asset root")
        if path == ROOT:
            break
    for name, expected in IDENTITIES.items():
        if digest(ASSETS / name) != expected:
            raise ValueError("Missing/wrong staged asset")
    if sum(p.stat().st_size for p in ASSETS.iterdir() if p.is_file()) > 1024**2:
        raise RuntimeError("Staged asset storage cap")


def require_offline_worker() -> None:
    """A persisted attested epoch and local gateway observation precede DLL loading."""
    state = read_meter()
    check_epoch(state)
    from ocr_trial import ensure_disconnected

    ensure_disconnected()


def load_dll(connection) -> None:
    """Load only the pinned absolute DLL, always disabling extension loading afterward."""
    require_offline_worker()
    verify_assets()
    try:
        connection.enable_load_extension(True)
        connection.load_extension(str((ASSETS / "vec0.dll").resolve()))
    finally:
        connection.enable_load_extension(False)


def authorizer(action, first, second, database, trigger):
    """Fixed harness SQL only; deny attachment, arbitrary functions and unsafe PRAGMAs."""
    if action in {sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH}:
        return sqlite3.SQLITE_DENY
    if (
        action == sqlite3.SQLITE_FUNCTION
        and (second or first or "").lower() not in CONTRACT["functions"]
    ):
        return sqlite3.SQLITE_DENY
    if action == sqlite3.SQLITE_PRAGMA:
        allowed = CONTRACT["pragmas"].get((first or "").lower(), [])
        argument = second.upper() if second is not None else None
        if argument not in allowed:
            return sqlite3.SQLITE_DENY
    return sqlite3.SQLITE_OK


def rank_candidates(rows: list, eligible: dict[int, str]) -> list:
    """Require complete scoped candidates so stable cutoff ties cannot be dropped."""
    if len(rows) != len(eligible) or {r[0] for r in rows} != set(eligible):
        raise ValueError("Missing/duplicate/unauthorized vec0 candidate")
    if any(not math.isfinite(distance) for _, distance in rows):
        raise ValueError("Nonfinite native distance")
    return sorted(
        [(eligible[rowid], distance) for rowid, distance in rows],
        key=lambda r: (r[1], r[0]),
    )[:5]


class Adapter(base.Store):
    """Fresh scoped fixture store; B mirrors chunk rows into a native vec0 table."""

    def __init__(self, root: Path, engine: str):
        if engine not in {"A", "B"}:
            raise ValueError("Unknown adapter")
        self.engine, self.load_seconds = engine, 0.0
        super().__init__(root)
        if engine == "B":
            try:
                started = time.perf_counter()
                load_dll(self.con)
                self.load_seconds = time.perf_counter() - started
                if self.con.execute("SELECT vec_version()").fetchone()[0] not in {
                    "v0.1.9",
                    "0.1.9",
                }:
                    raise ValueError("Native reported version mismatch")
                self.con.execute(
                    "CREATE VIRTUAL TABLE IF NOT EXISTS vec_index USING vec0(embedding float[768] distance_metric=cosine)"
                )
                self.con.execute(
                    "CREATE TABLE IF NOT EXISTS vec_map(rowid INTEGER PRIMARY KEY,chunk TEXT UNIQUE NOT NULL REFERENCES chunks(id) ON DELETE CASCADE)"
                )
            except BaseException:
                self.close()
                raise
        self.con.set_authorizer(authorizer)

    def add_chunk(self, identity, doc, vector, version):
        """Commit chunk metadata, stable rowid and native vector together."""
        return self.add_frozen_chunk(identity, doc, base.pack_vector(vector), version)

    def add_frozen_chunk(self, identity, doc, blob, version):
        """Preserve previously frozen float32 bytes without normalizing a second time."""
        base.unpack_vector(blob)
        if version != base.VERSION:
            raise ValueError("Unapproved vector version")
        own = not self.con.in_transaction
        if own:
            self.con.execute("BEGIN IMMEDIATE")
        try:
            row = (identity, doc, version, blob, base.ANCHOR)
            previous = self.con.execute(
                "SELECT * FROM chunks WHERE id=?", (identity,)
            ).fetchone()
            if previous and previous != row:
                raise ValueError("Chunk identity drift")
            self.con.execute("INSERT OR IGNORE INTO chunks VALUES (?,?,?,?,?)", row)
            if self.engine == "B":
                existing = self.con.execute(
                    "SELECT rowid FROM vec_map WHERE chunk=?", (identity,)
                ).fetchone()
                if not existing:
                    rowid = self.con.execute(
                        "INSERT INTO vec_map(chunk) VALUES (?)", (identity,)
                    ).lastrowid
                    self.con.execute(
                        "INSERT INTO vec_index(rowid,embedding) VALUES (?,?)",
                        (rowid, blob),
                    )
            if own:
                self.con.commit()
        except BaseException:
            if own:
                self.con.rollback()
            raise

    def search(self, conversation, query, version):
        """Retrieve only eligible native candidates, retaining all boundary ties."""
        if self.engine == "A":
            return super().search(conversation, query, version)
        blob = base.pack_vector(query)
        rows = self.eligible(conversation, version)
        if not rows:
            return []
        for _, vector in rows:
            base.unpack_vector(vector)
        ids = [r[0] for r in rows]
        placeholders = ",".join("?" for _ in ids)
        mapping = dict(
            self.con.execute(
                f"SELECT rowid,chunk FROM vec_map WHERE chunk IN ({placeholders})", ids
            )
        )
        if len(mapping) != len(ids):
            raise ValueError("Vector mapping incomplete")
        placeholders = ",".join("?" for _ in mapping)
        found = self.con.execute(
            f"SELECT rowid,distance FROM vec_index WHERE embedding MATCH ? AND k=? AND rowid IN ({placeholders}) ORDER BY distance",
            (blob, len(mapping), *mapping),
        ).fetchall()
        return rank_candidates(found, mapping)

    def _drop_vectors(self, chunk_ids):
        for identity in chunk_ids:
            row = self.con.execute(
                "SELECT rowid FROM vec_map WHERE chunk=?", (identity,)
            ).fetchone()
            if row:
                self.con.execute("DELETE FROM vec_index WHERE rowid=?", row)

    def delete_conversation(self, conversation):
        """Maintain native-vector and shared ownership invariants in one transaction."""
        if self.engine == "A":
            return super().delete_conversation(conversation)
        if conversation == "library":
            raise ValueError("Reserved ownership")
        self.con.execute("BEGIN IMMEDIATE")
        try:
            ids = [
                r[0]
                for r in self.con.execute(
                    "SELECT c.id FROM chunks c JOIN documents d ON c.doc=d.id WHERE d.owner=?",
                    (conversation,),
                )
            ]
            self._drop_vectors(ids)
            self.con.execute("DELETE FROM refs WHERE conversation=?", (conversation,))
            self.con.execute("DELETE FROM documents WHERE owner=?", (conversation,))
            self.con.commit()
        except BaseException:
            self.con.rollback()
            raise
        self.purge_unreferenced()

    def remove_library(self, identity):
        """Block dependent references before deleting a library document/native rows."""
        if self.con.execute("SELECT 1 FROM refs WHERE doc=?", (identity,)).fetchone():
            raise ValueError("Warning: dependent conversations")
        if self.engine == "A":
            return super().remove_library(identity)
        self.con.execute("BEGIN IMMEDIATE")
        try:
            self._drop_vectors(
                [
                    r[0]
                    for r in self.con.execute(
                        "SELECT id FROM chunks WHERE doc=?", (identity,)
                    )
                ]
            )
            self.con.execute(
                "DELETE FROM documents WHERE id=? AND owner='library'", (identity,)
            )
            self.con.commit()
        except BaseException:
            self.con.rollback()
            raise
        self.purge_unreferenced()

    def rebuild(self, identity, vector, version):
        """Rebuild mirrored values without changing chunk anchors or stable rowids."""
        if self.engine == "A":
            return super().rebuild(identity, vector, version)
        self.con.execute("BEGIN IMMEDIATE")
        try:
            super().rebuild(identity, vector, version)
            row = self.con.execute(
                "SELECT rowid FROM vec_map WHERE chunk=?", (identity,)
            ).fetchone()
            if not row:
                raise ValueError("Missing rebuild mapping")
            self.con.execute(
                "UPDATE vec_index SET embedding=? WHERE rowid=?",
                (base.pack_vector(vector), row[0]),
            )
            self.con.commit()
        except BaseException:
            self.con.rollback()
            raise

    def integrity(self):
        """Require SQLite integrity and exact native mapping counts on reopen."""
        if (
            self.con.execute("PRAGMA integrity_check").fetchone()[0] != "ok"
            or self.con.execute("PRAGMA foreign_key_check").fetchall()
        ):
            raise ValueError("SQLite integrity failure")
        if self.engine == "B":
            counts = [
                self.con.execute("SELECT count(*) FROM " + name).fetchone()[0]
                for name in ("chunks", "vec_map", "vec_index")
            ]
            if len(set(counts)) != 1:
                raise ValueError("Native mapping count mismatch")


def generated(size):
    """Reproduce only the two approved synthetic scales and their exact float32 bytes."""
    if size not in CONTRACT["sizes"]:
        raise ValueError("Unapproved scale")
    rng = random.Random(12001 + size)
    blobs = [
        base.pack_vector([rng.uniform(-1, 1) for _ in range(768)]) for _ in range(size)
    ]
    queries = [list(base.unpack_vector(blobs[(i * 7919) % size])) for i in range(12)]
    hashes = {
        "vector_sha256": hashlib.sha256(b"".join(blobs)).hexdigest(),
        "query_sha256": hashlib.sha256(
            b"".join(base.pack_vector(q) for q in queries)
        ).hexdigest(),
    }
    return blobs, queries, hashes


def verify_seal():
    """Require every prepared source, artifact and prior identity before native work."""
    state = json.loads((RUN / "seal.json").read_bytes())
    for name, expected in state.items():
        path = Path(name)
        if not (
            path.is_relative_to(ROOT)
            or path in {PYTHON, PYTHON.with_name("python314.dll")}
        ):
            raise ValueError("Seal path outside approved identities")
        if digest(path) != expected:
            raise ValueError("Source/artifact seal changed")


def prepare():
    """Charge active staging time without charging later human handoff waiting."""
    with preparation_segment("Verified staging, fixture identities and seal"):
        _prepare()


def mark_ready() -> None:
    """Freeze handoff readiness only after independently reviewed preparation."""
    with preparation_segment("Final independent seal and asset recheck"):
        verify_seal()
        verify_assets()
    state = read_meter()
    state["status"] = "ready"
    state["events"].append("Final reviewed handoff; human waiting is excluded")
    base.save(RUN / "meter.json", state)


def _prepare():
    """Stage verified cached bytes and create static readiness; never enable a DLL load."""
    import sqlite_vec_artifact as artifact

    meter = read_meter()
    if (
        meter["status"] != "preparing"
        or (RUN / "seal.json").exists()
        or ASSETS.exists()
    ):
        raise RuntimeError("Never overwrite/reseal a prepared run")
    old = ROOT / "data/t12/sqlite-vec-artifact-01"
    wheel = old / artifact.WHEEL_NAME
    if digest(wheel) != artifact.WHEEL_SHA or wheel.stat().st_size != 292804:
        raise ValueError("Cached wheel mismatch")
    files = artifact.inspect_zip(wheel.read_bytes())
    assets = {
        "vec0.dll": files["sqlite_vec/vec0.dll"],
        "LICENSE-MIT": (old / "source-LICENSE-MIT.txt").read_bytes(),
        "LICENSE-APACHE": (old / "source-LICENSE-APACHE.txt").read_bytes(),
    }
    for name, content in assets.items():
        if hashlib.sha256(content).hexdigest() != IDENTITIES[name]:
            raise ValueError("Cached asset mismatch")
    # Validate all ancestor components before creating the new stage directory.
    if any(p.is_symlink() or p.is_junction() for p in [ASSETS, *ASSETS.parents]):
        raise ValueError("Linked staging ancestor")
    ASSETS.mkdir(parents=True)
    for name, content in assets.items():
        (ASSETS / name).write_bytes(content)
    verify_assets()
    if sqlite3.sqlite_version != "3.50.4":
        raise ValueError("SQLite build changed")
    original = json.loads(
        (ROOT / "data/t12/storage-baseline-01/summary.json").read_bytes()
    )
    inputs = {}
    for size in CONTRACT["sizes"]:
        _, _, identities = generated(size)
        previous = next(r for r in original["scales"] if r["size"] == size)
        if any(previous[k] != v for k, v in identities.items()):
            raise ValueError("Selected frozen fixture identity mismatch")
        inputs[str(size)] = identities
    base.save(RUN / "inputs.json", inputs)
    source_paths = [
        Path(__file__),
        Path(__file__).with_name("test_sqlite_vec_runtime_followup.py"),
        CONTRACT_PATH,
        ROOT / "pyproject.toml",
        ROOT / "uv.lock",
        ROOT / ".venv/pyvenv.cfg",
        wheel,
        PYTHON,
        PYTHON.with_name("python314.dll"),
    ]
    source_paths += [ROOT / name for name in meter["prior_hashes"]]
    source_paths += [
        Path(__file__).with_name(name)
        for name in ("ocr_trial.py", "appcontainer_preflight.py", "embedding_budget.py")
    ]
    source_paths += [ASSETS / name for name in IDENTITIES]
    source_paths.append(RUN / "inputs.json")
    for name, expected in meter["prior_hashes"].items():
        if digest(ROOT / name) != expected:
            raise ValueError("Prior record changed")
    interpreter_prior = json.loads(
        (ROOT / "data/t11/combined-07/seal.json").read_bytes()
    )["python"]
    if any(
        digest(Path(name)) != expected for name, expected in interpreter_prior.items()
    ):
        raise ValueError("Interpreter identity drift")
    launcher = "# Approved synthetic native trial; no filesystem confinement.\n$ErrorActionPreference = 'Stop'\nSet-Location -LiteralPath 'F:\\document_assistant'\n& 'F:\\Python\\Python314\\python.exe' -I -S -B tests/evals/spikes/sqlite_vec_runtime_followup.py offline sqlite-vec-runtime-02\n"
    (RUN / "run.ps1").write_text(launcher, encoding="utf-8")
    source_paths.append(RUN / "run.ps1")
    base.save(
        RUN / "seal.json",
        {str(path.resolve()): digest(path) for path in set(source_paths)},
    )
    # Independent review/documentation still consumes active preparation time.
    meter["status"] = "preparing"
    base.save(RUN / "meter.json", meter)
    print(
        json.dumps(
            {
                "status": "static_prepared_no_load",
                "identities": len(set(source_paths)),
                "sizes": CONTRACT["sizes"],
            }
        )
    )


def scoped_controls(store):
    """Native/standard adapter invariants using unrelated closer and cutoff-tie rows."""
    vector, far = [1.0] + [0.0] * 767, [0.8, 0.6] + [0.0] * 766
    store.add_document("lib", b"shared synthetic", "library", ["a", "b"])
    store.add_document("own", b"shared synthetic", "a", ["a"])
    store.add_document("other", b"excluded synthetic", "b", ["b"])
    for i in range(7):
        store.add_chunk(f"tie-{i}", "lib", far, base.VERSION)
    store.add_chunk("excluded", "other", vector, base.VERSION)
    if [r[0] for r in store.search("a", vector, base.VERSION)] != [
        f"tie-{i}" for i in range(5)
    ]:
        raise ValueError("Scope/cutoff tie control")
    if store.search("none", vector, base.VERSION):
        raise ValueError("Empty-scope leakage")
    for sql in (
        "ATTACH DATABASE ':memory:' AS other",
        "SELECT load_extension('x')",
        "SELECT vec_npy_file('x')",
    ):
        try:
            store.con.execute(sql)
        except sqlite3.DatabaseError:
            pass
        else:
            raise ValueError("SQL refusal control failed")
    try:
        store.remove_library("lib")
    except ValueError:
        pass
    else:
        raise ValueError("Library reference removal not blocked")
    try:
        store.search("a", vector, "wrong-version")
    except ValueError:
        pass
    else:
        raise ValueError("Version control not enforced")
    store.delete_conversation("a")
    if (
        store.document_ids() != ["lib", "other"]
        or not store.content_path("lib").exists()
    ):
        raise ValueError("Shared ownership/deletion control")
    store.integrity()


def benchmark(engine, size):
    """Fixed paired benchmark with independent reference and exact byte identities."""
    directory = RUN / f"{engine}-scale-{size}"
    if directory.exists():
        raise RuntimeError("Never repeat a started measurement")
    blobs, queries, hashes = generated(size)
    if hashes != json.loads((RUN / "inputs.json").read_bytes())[str(size)]:
        raise ValueError("Runtime fixture drift")
    control = Adapter(RUN / f"{engine}-controls-{size}", engine)
    try:
        scoped_controls(control)
    finally:
        control.close()
    store = Adapter(directory, engine)
    try:
        load_seconds = store.load_seconds
        store.add_document("fixture", b"synthetic baseline original", "library", ["a"])
        started = time.perf_counter()
        store.con.execute("BEGIN IMMEDIATE")
        for i, blob in enumerate(blobs):
            store.add_frozen_chunk(f"c{i:05d}", "fixture", blob, base.VERSION)
        store.con.commit()
        insert_seconds = time.perf_counter() - started
        # Native and Python adapters consume the exact same frozen bytes.
        rows = store.eligible("a", base.VERSION)
        if (
            hashlib.sha256(b"".join(blob for _, blob in rows)).hexdigest()
            != hashes["vector_sha256"]
        ):
            raise ValueError("Insertion changed frozen float32 bytes")
        expected = [base.reference_rank(rows, q) for q in queries]
        passes = []
        for _ in range(4):
            timings = []
            for query, gold in zip(queries, expected, strict=True):
                started = time.perf_counter()
                actual = store.search("a", query, base.VERSION)
                timings.append(time.perf_counter() - started)
                if [r[0] for r in actual] != [r[0] for r in gold] or any(
                    abs(a[1] - b[1]) > 1e-6 for a, b in zip(actual, gold, strict=True)
                ):
                    raise ValueError("Independent reference ranking/distance mismatch")
            passes.append(
                {
                    "query_seconds": timings,
                    "median": statistics.median(timings),
                    "maximum": max(timings),
                }
            )
        started = time.perf_counter()
        store.rebuild("c00000", list(base.unpack_vector(blobs[0])), base.VERSION)
        rebuild_seconds = time.perf_counter() - started
        store.close()
        started = time.perf_counter()
        store = Adapter(directory, engine)
        store.integrity()
        reopen_seconds = time.perf_counter() - started
        before_delete_bytes = store.safe("store.sqlite").stat().st_size
        started = time.perf_counter()
        store.delete_conversation(
            "a"
        )  # Removes reference, preserves reusable library bytes.
        store.remove_library("fixture")
        store.integrity()
        delete_seconds = time.perf_counter() - started
        return {
            "engine": engine,
            "size": size,
            **hashes,
            "load_seconds": load_seconds,
            "insert_seconds": insert_seconds,
            "passes": passes,
            "single_vector_rebuild_seconds": rebuild_seconds,
            "reopen_seconds": reopen_seconds,
            "delete_seconds": delete_seconds,
            "ranking_checks": 48,
            "database_bytes_before_delete": before_delete_bytes,
            "database_bytes_after_delete": store.safe("store.sqlite").stat().st_size,
        }
    finally:
        store.close()


def crash_worker(engine, case):
    """Pause at the same four original/transaction boundaries for both adapters."""
    store = Adapter(RUN / f"{engine}-{case}", engine)
    vector = [1.0] + [0.0] * 767
    store.add_document("stable", b"stable synthetic bytes", "library", ["a", "b"])
    store.add_chunk("stable", "stable", vector, base.VERSION)
    sha = (
        store.write_original(b"pending synthetic bytes").name
        if case in {"file-before-commit", "commit-before-cleanup"}
        else hashlib.sha256(b"stable synthetic bytes").hexdigest()
    )
    store.con.execute("BEGIN IMMEDIATE")
    store.con.execute("INSERT OR IGNORE INTO contents VALUES (?, 'ready')", (sha,))
    store.con.execute("INSERT INTO documents VALUES ('new',?,'a')", (sha,))
    store.con.execute("INSERT INTO refs VALUES ('a','new')")
    store.add_chunk("new", "new", [0.0, 1.0] + [0.0] * 766, base.VERSION)
    if case in {"after-commit", "commit-before-cleanup"}:
        store.con.commit()
    base.save(RUN / "ready.json", {"case": engine + "-" + case})
    time.sleep(120)
    raise RuntimeError("Crash owner did not terminate")


def verify_crash(engine, case):
    """Separately reopen and check metadata, native vectors, references and originals."""
    store = Adapter(RUN / f"{engine}-{case}", engine)
    try:
        expected = 2 if case in {"after-commit", "commit-before-cleanup"} else 1
        store.integrity()
        if (
            store.count("chunks") != expected
            or store.count("documents") != expected
            or store.count("refs") != expected + 1
        ):
            raise ValueError("Crash reference/vector count mismatch")
        rows = store.search("a", [1.0] + [0.0] * 767, base.VERSION)
        if len(rows) != expected:
            raise ValueError("Recovered retrieval incomplete")
        reconciled = store.reconcile()
        if reconciled != {
            "orphan_markers": int(case == "file-before-commit"),
            "cleanup_markers": int(case == "commit-before-cleanup"),
        }:
            raise ValueError("Original-file recovery mismatch")
        return {
            "engine": engine,
            "case": case,
            "counts": {
                t: store.count(t) for t in ("contents", "documents", "refs", "chunks")
            },
            "reconciliation": reconciled,
            "integrity": "ok",
        }
    finally:
        store.close()


class Runner(base.Runner):
    """Reuse the reviewed job boundary, overriding allocation, launch and sampling paths."""

    def sample(self):
        from embedding_budget import memory_snapshot
        from ocr_trial import ensure_disconnected

        started = time.monotonic()
        ensure_disconnected()
        reading = memory_snapshot()
        completed = time.monotonic()
        gap = 0 if self.last_read is None else completed - self.last_read
        observation = {
            "available": reading["available_physical"],
            "controller": reading["controller_private"],
        }
        base.check_sample(observation, gap)
        self.last_read = completed
        state = read_meter()
        check_epoch(state)
        actual = self.extended()
        self.native.check(
            self.native.kernel.QueryInformationJobObject(
                self.job, 9, ctypes.byref(actual), ctypes.sizeof(actual), None
            )
        )
        disk = 0
        if not RUN.is_dir() or RUN.is_symlink() or RUN.is_junction():
            raise ValueError("Runtime root identity")
        for path in RUN.rglob("*"):
            if path.is_symlink() or path.is_junction():
                raise ValueError("Unexpected runtime link")
            try:
                if path.is_file():
                    disk += path.stat().st_size
            except FileNotFoundError:
                if not RUN.is_dir():
                    raise
        verify_assets()
        duration = time.monotonic() - started
        if (
            actual.peak_job > 2 * 1024**3
            or disk > 512 * 1024**2
            or completed - started > 0.3
            or duration > 0.3
        ):
            raise RuntimeError("Aggregate/disk/collection boundary")
        observation.update(
            gap=gap,
            job_peak=actual.peak_job,
            disk_bytes=disk,
            iteration_seconds=duration,
        )
        self.samples.append(observation)

    def run_request(self, mode, engine="A", value=""):
        """Count, suspend, own, supervise and reap exactly one allowed worker."""
        from ctypes import wintypes

        from appcontainer_preflight import ProcessInfo, Startup
        from ocr_trial import process_memory

        if mode not in {
            "benchmark",
            "crash",
            "verify",
            "deadline",
            "memory",
        } or engine not in {"A", "B"}:
            raise ValueError("Worker mode")
        if (mode == "benchmark" and value not in {"32", "1000"}) or (
            mode in {"crash", "verify"} and value not in CONTRACT["crash_cases"]
        ):
            raise ValueError("Unapproved worker value")
        charge("workers", 1, mode + ":" + engine + ":" + value)
        self.sample()
        self.launches += 1
        request_id = f"W{self.launches:02d}"
        request = {"id": request_id, "mode": mode, "engine": engine, "value": value}
        base.save(RUN / (request_id + ".json"), request)
        native = self.native
        child_job = native.job(1, kill=True)
        limits = self.extended()
        limits.basic.flags, limits.basic.active = 0x8 | 0x2000, 1
        if mode == "memory":
            limits.basic.flags |= 0x100
            limits.process_memory = 64 * 1024**2
        native.check(
            native.kernel.SetInformationJobObject(
                child_job, 9, ctypes.byref(limits), ctypes.sizeof(limits)
            )
        )
        startup, process = Startup(), ProcessInfo()
        startup.cb, startup.flags, startup.show = ctypes.sizeof(startup), 1, 0
        command = f'"{PYTHON}" -I -S -B "{Path(__file__).resolve()}" worker {CONTRACT["run_id"]} {request_id}'
        created, killed, peak_private, peak_ws = False, False, 0, 0
        began = time.monotonic()
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
                usage = process_memory(process.process)
                peak_private = max(peak_private, usage["private_observed"])
                peak_ws = max(peak_ws, usage["working_peak"])
                elapsed = time.monotonic() - began
                if mode == "deadline" and elapsed > 0.2:
                    native.check(native.kernel.TerminateProcess(process.process, 125))
                    killed = True
                elif elapsed > 120:
                    raise RuntimeError("Owned worker deadline")
                elif mode == "crash" and (RUN / "ready.json").exists():
                    marker = json.loads((RUN / "ready.json").read_bytes())
                    if marker["case"] != engine + "-" + value:
                        raise ValueError("Crash boundary marker mismatch")
                    native.check(native.kernel.TerminateProcess(process.process, 125))
                    killed = True
                time.sleep(max(0, 0.1 - (time.monotonic() - iteration)))
            code = wintypes.DWORD()
            native.check(
                native.kernel.GetExitCodeProcess(process.process, ctypes.byref(code))
            )
            if code.value != (125 if mode in {"deadline", "crash"} else 0) or (
                mode in {"deadline", "crash"} and not killed
            ):
                raise RuntimeError("Worker exit/control failure")
            if (
                native.accounting(child_job)["active"]
                or native.accounting(child_job)["total"] != 1
            ):
                raise RuntimeError("Unexpected worker descendants/accounting")
            account = native.accounting(self.job)
            if account["total"] != self.launches + 1 or account["active"] != 1:
                raise RuntimeError("Aggregate process accounting mismatch")
            result = {
                "id": request_id,
                "mode": mode,
                "engine": engine,
                "value": value,
                "exit_code": code.value,
                "sampled_private_peak": peak_private,
                "peak_working_set": peak_ws,
            }
            if mode not in {"deadline", "crash"}:
                result["result"] = json.loads(
                    (RUN / (request_id + "-result.json")).read_bytes()
                )
                if mode == "memory" and result["result"] != {
                    "status": "memory_refused"
                }:
                    raise RuntimeError("Memory control did not refuse")
            return result
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


def worker(request_id):
    """Only this fixed local worker path can perform offline native loading."""
    if not re.fullmatch("W[0-9]{2}", request_id):
        raise ValueError("Invalid local request identity")
    verify_seal()
    require_offline_worker()
    request = json.loads((RUN / (request_id + ".json")).read_bytes())
    mode, engine, value = request["mode"], request["engine"], request["value"]
    if request["id"] != request_id or engine not in {"A", "B"}:
        raise ValueError("Request identity/adapter")
    if mode == "deadline":
        time.sleep(120)
        raise RuntimeError("Deadline sentinel was not stopped")
    if mode == "memory":
        try:
            bytearray(128 * 1024**2)
        except MemoryError:
            result = {"status": "memory_refused"}
        else:
            raise RuntimeError("Memory sentinel was not refused")
    elif mode == "benchmark" and value in {"32", "1000"}:
        result = benchmark(engine, int(value))
    elif mode == "crash" and value in CONTRACT["crash_cases"]:
        crash_worker(engine, value)
        return
    elif mode == "verify" and value in CONTRACT["crash_cases"]:
        result = verify_crash(engine, value)
    else:
        raise ValueError("Unapproved worker request")
    base.save(RUN / (request_id + "-result.json"), result)


def offline():
    """Run once after manual disconnection, preserving every partial outcome."""
    result = {
        "status": "started",
        "controls": [],
        "crashes": [],
        "measurements": [],
        "teardown_verified": False,
        "owned_workers_launched": 0,
        "launcher_controller_attempts": 2,
        "launcher_controller_reserved": False,
        "phase": "admission",
    }
    runner = None
    admitted = False
    try:
        verify_output_root()
        if (RUN / "summary.json").exists() or (RUN / "execution-attempt.json").exists():
            raise RuntimeError("Never repeat a terminal/attempted allocation")
        state = read_meter()
        if state["status"] != "ready" or state["execution_started"] is not None:
            raise RuntimeError("Never restart a prepared/native-started allocation")
        with (RUN / "execution-attempt.json").open("x", encoding="utf-8") as stream:
            json.dump({"attempted": time.time(), "native_workers_started": 0}, stream)
        admitted = True
        # Reserve actual launcher/controller attempts even when attestation fails.
        result["phase"] = "handoff-reservation"
        charge("workers", 2, "User PowerShell and standalone controller")
        result["launcher_controller_reserved"] = True
        print(
            "Disconnect EVERY external link. Synthetic-only native trial has NO filesystem confinement.",
            flush=True,
        )
        result["phase"] = "attestation"
        if (
            input("Remain disconnected through verified teardown. Type OFFLINE: ")
            != "OFFLINE"
        ):
            raise RuntimeError(
                "No disconnection attestation; no native workload started"
            )
        result["phase"] = "start-epoch"
        start_execution()
        result["phase"] = "verify-seal"
        verify_seal()
        from ocr_trial import ensure_disconnected

        result["phase"] = "disconnection-check"
        ensure_disconnected()
        check_epoch(read_meter())
        result["phase"] = "job-setup"
        runner = Runner()
        print("TESTING IN PROGRESS. Keep all external links disconnected.", flush=True)
        for mode in ("deadline", "memory"):
            result["phase"] = "control-" + mode
            result["controls"].append(runner.run_request(mode))
        for engine in CONTRACT["adapters"]:
            for case in CONTRACT["crash_cases"]:
                result["phase"] = engine + "-" + case
                stopped = runner.run_request("crash", engine, case)
                checked = runner.run_request("verify", engine, case)
                result["crashes"].append({"terminated": stopped, "reopened": checked})
                base.save(RUN / "progress.json", result)
        for size in CONTRACT["sizes"]:
            for engine in CONTRACT["adapters"]:
                result["phase"] = f"{engine}-scale-{size}"
                result["measurements"].append(
                    runner.run_request("benchmark", engine, str(size))
                )
                base.save(RUN / "progress.json", result)
        result["status"] = "completed_pending_review_no_adoption"
        check_epoch(read_meter())
    except BaseException as error:  # noqa: BLE001 -- Preserve every native stop before owned teardown.
        result.update(
            status="stopped_no_automatic_retry",
            error_type=type(error).__name__,
            reason="Trial stopped; preserve local state for review",
        )
    finally:
        try:
            if runner:
                runner.close()
                result["resource_samples"] = runner.samples
                result["owned_workers_launched"] = runner.launches
            result["teardown_verified"] = admitted
            if admitted:
                state = read_meter()
                if state["execution_started"] is not None:
                    try:
                        check_epoch(state)
                    except RuntimeError:
                        result["epoch_boundary_at_cleanup"] = True
                        result["status"] = "stopped_no_automatic_retry"
        except BaseException as error:  # noqa: BLE001 -- Cleanup uncertainty must prevent safe reconnect.
            result["cleanup_error_type"] = type(error).__name__
        result["receipt_persisted"] = False
        if admitted:
            try:
                verify_output_root()
                state = read_meter()
                state["status"] = "closed"
                base.save(RUN / "meter.json", state)
                result["receipt_persisted"] = True
                with (RUN / "summary.json").open("x", encoding="utf-8") as stream:
                    json.dump(result, stream, indent=2)
            except (OSError, ValueError, KeyError):
                result["receipt_persisted"] = False
        print("RECEIPT PERSISTED:", result["receipt_persisted"], flush=True)
        print("STATUS:", result["status"], flush=True)
        print("TEARDOWN VERIFIED:", result["teardown_verified"], flush=True)
        if result["teardown_verified"]:
            print(
                "Owned workers stopped. You may reconnect and report status.",
                flush=True,
            )
        else:
            print("Remain disconnected; owned cleanup is uncertain.", flush=True)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    if len(arguments) < 2:
        raise SystemExit(
            "Expected prepare/offline <approved-run-id> or worker <run-id> <request-id>"
        )
    check_run_id(arguments[1])
    if len(arguments) == 2 and arguments[0] == "prepare":
        prepare()
    elif len(arguments) == 2 and arguments[0] == "offline":
        offline()
    elif len(arguments) == 3 and arguments[0] == "worker":
        worker(arguments[2])
    else:
        raise SystemExit("Unapproved command")
