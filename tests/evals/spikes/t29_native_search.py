"""T29-N1 one-run offline native cosine check; separate execution approval required."""

import argparse
import asyncio
import hashlib
import json
import math
import secrets
import sqlite3
import subprocess
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path

from app.config import PROJECT_ROOT, validate_local_ancestry
from app.ingestion.validation import UploadError
from app.retrieval.embeddings import Embedding, EmbeddingBatch
from app.retrieval.index import LocalIndex
from app.retrieval.search import Retriever
from app.retrieval.vector_search import load_sqlite_vec
from app.storage.documents import Documents
from app.storage.extractions import Extractions
from app.storage.files import UploadStore

RUN_ROOT = PROJECT_ROOT / "data/t29-native-01"
SEAL = PROJECT_ROOT / "docs/proposals/t29-native-search-seal.json"


def check_sources() -> None:
    """Pin the complete app/helper/config set; never reseal a consumed allocation."""
    seal = json.loads(SEAL.read_text(encoding="utf-8"))
    expected = {
        p.relative_to(PROJECT_ROOT).as_posix()
        for p in (PROJECT_ROOT / "app").rglob("*.py")
    }
    expected.update(
        {"pyproject.toml", "uv.lock", "tests/evals/spikes/t29_native_search.py"}
    )
    if seal.get("package") != "T29-N1" or set(seal.get("sha256", {})) != expected:
        raise ValueError("SOURCE_MISMATCH")
    for name in expected:
        path = PROJECT_ROOT / name
        validate_local_ancestry(path)
        if (
            path.stat().st_size > 2_000_000
            or hashlib.sha256(path.read_bytes()).hexdigest() != seal["sha256"][name]
        ):
            raise ValueError("SOURCE_MISMATCH")


def save(name: str, value: dict) -> None:
    """Retain only bounded scalar receipts, never vectors or engine output."""
    data = json.dumps(value, sort_keys=True).encode()
    if len(data) > 16384:
        raise ValueError("OUTPUT_LIMIT")
    (RUN_ROOT / name).write_bytes(data)


async def native_check(ledger: dict) -> dict:
    """Real SQLite upload/index/search with synthetic embeddings and one DLL load."""
    store = UploadStore(RUN_ROOT / "app")
    try:

        class Fake:
            async def documents(self, chunks):
                return EmbeddingBatch(
                    "document",
                    tuple(
                        Embedding(
                            c.chunk_id,
                            c.text_hash,
                            tuple(
                                float(i == (0 if "North" in c.text else 1))
                                for i in range(768)
                            ),
                        )
                        for c in chunks
                    ),
                    None,
                )

            async def query(self, text, identity):
                return EmbeddingBatch(
                    "query",
                    (
                        Embedding(
                            identity,
                            hashlib.sha256(text.encode()).hexdigest(),
                            (1.0,) + (0.0,) * 767,
                        ),
                    ),
                    None,
                )

        @asynccontextmanager
        async def session():
            if store.busy:
                raise ValueError("BUSY")
            store.busy = True
            try:
                yield Fake()
            finally:
                store.busy = False

        conversation = Documents(store.connection).create_conversation()

        async def body():
            yield b"Name,Units\nNorth,42\nSouth,50\n"

        uploaded = await store.receive(
            body(), conversation, "native-upload-01", "authored.csv"
        )
        await Extractions(store).extract(
            conversation, uploaded["reference_id"], "native-extract-01"
        )
        await LocalIndex(store).index(
            conversation,
            uploaded["reference_id"],
            "native-index-01",
            session_factory=session,
        )

        def loader(connection):
            if ledger["loads"] != 0:
                raise ValueError("LOAD_LIMIT")
            ledger["loads"] += 1
            save("ledger.json", ledger)
            load_sqlite_vec(connection)

        result = await Retriever(store, loader=loader).retrieve(
            conversation,
            [uploaded["reference_id"]],
            "North units?",
            session_factory=session,
        )
        if (
            len(result.ranked) != 2
            or "42" not in result.ranked[0].chunk.text
            or not math.isclose(result.ranked[0].distance, 0, abs_tol=1e-6)
            or not math.isclose(result.ranked[1].distance, 1, abs_tol=1e-6)
            or len(result.evidence) != 2
        ):
            raise ValueError("RANK_FAILURE")
        denied = False
        try:
            store.connection.execute("SELECT load_extension('unapproved')")
        except sqlite3.Error:
            denied = True
        if not denied:
            raise ValueError("EXTENSION_BOUNDARY_FAILURE")
        if store.connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("INTEGRITY_FAILURE")
        return {
            "ranked": 2,
            "evidence": 2,
            "dimensions": 768,
            "expected_cosines": True,
            "sql_load_denied": True,
            "integrity": "ok",
        }
    finally:
        store.close()


def supervise(
    process, output: Path, deadline: float, *, clock=time.monotonic, pause=time.sleep
) -> int:
    """Bound one owned worker and its observed output; no automatic retry."""
    failed = False
    while process.poll() is None:
        sizes = []
        for item in output.parent.rglob("*"):
            validate_local_ancestry(item)
            if len(sizes) >= 128:
                failed = True
                break
            sizes.append(item.stat().st_size if item.is_file() else 0)
        if (
            failed
            or clock() >= deadline
            or output.stat().st_size > 65536
            or sum(sizes) > 2_000_000
        ):
            failed = True
            process.kill()
            break
        pause(0.05)
    code = process.wait(timeout=5)
    return 1 if failed or output.stat().st_size > 65536 else code


def main(argv=None) -> int:
    """Require approval/disconnection flags and a fresh root before one worker."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-approved", action="store_true")
    parser.add_argument("--offline-attested", action="store_true")
    parser.add_argument("--worker-token")
    args = parser.parse_args(argv)
    if not args.execute_approved or not args.offline_attested:
        print(
            "T29-N1 requires separate approval and offline attestation; nothing started."
        )
        return 2
    if args.worker_token:
        try:
            validate_local_ancestry(RUN_ROOT)
            path = RUN_ROOT / "ledger.json"
            if path.stat().st_size > 16384:
                return 2
            ledger = json.loads(path.read_bytes())
            if ledger.get("package") != "T29-N1" or not secrets.compare_digest(
                str(ledger.get("token", "")), args.worker_token
            ):
                return 2
            with (RUN_ROOT / "worker.claim").open("xb"):
                pass
        except (OSError, ValueError):
            return 2

        def no_children(event, arguments):
            if event == "subprocess.Popen":
                raise ValueError("CHILD_REFUSED")

        sys.addaudithook(no_children)
        result = {"package": "T29-N1", "status": "failed"}
        try:
            check_sources()
            result.update(asyncio.run(native_check(ledger)), status="passed")
        except Exception as error:  # noqa: BLE001 - fixed local stop receipt
            result["code"] = (
                error.code if isinstance(error, UploadError) else type(error).__name__
            )
        save("result.json", result)
        return 0 if result["status"] == "passed" else 1
    try:
        validate_local_ancestry(RUN_ROOT)
        RUN_ROOT.mkdir(parents=True, exist_ok=False)
    except OSError:
        print("T29-N1 root unavailable/existing; preserve it and do not retry.")
        return 2
    ledger = {
        "package": "T29-N1",
        "starts_charged": 2,
        "loads": 0,
        "token": secrets.token_hex(16),
    }
    deadline = time.monotonic() + 45
    save("ledger.json", ledger)
    process = None
    code = 1
    try:
        check_sources()
        if time.monotonic() >= deadline:
            raise ValueError("DEADLINE")
        with (RUN_ROOT / "worker-output.txt").open("xb") as output:
            process = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "tests.evals.spikes.t29_native_search",
                    "--execute-approved",
                    "--offline-attested",
                    "--worker-token",
                    ledger["token"],
                ],
                stdin=subprocess.DEVNULL,
                stdout=output,
                stderr=subprocess.STDOUT,
                creationflags=0x08000000,
            )
            code = supervise(process, RUN_ROOT / "worker-output.txt", deadline)
    except (OSError, ValueError, subprocess.SubprocessError, KeyboardInterrupt):
        code = 1
    finally:
        if process is not None and process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        save(
            "parent.json",
            {
                "status": "passed" if code == 0 else "failed",
                "worker_reaped": process is None or process.poll() is not None,
            },
        )
    print(
        "T29-N1 finished; inspect local result.json, ledger.json and parent.json; do not rerun."
    )
    return code


if __name__ == "__main__":
    raise SystemExit(main())
