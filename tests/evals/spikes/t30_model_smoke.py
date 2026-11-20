"""T30-N1 manual source-sealed Qwen generation/persistence check, separately gated."""

import argparse
import asyncio
import hashlib
import json
import re
import sys
from contextlib import asynccontextmanager
from dataclasses import replace

from app.chat.service import ChatService
from app.config import PROJECT_ROOT, Settings, validate_local_ancestry
from app.diagnostics import reserve_port
from app.ingestion.validation import UploadError
from app.ollama import OllamaError
from app.retrieval.embeddings import Embedding, EmbeddingBatch
from app.retrieval.index import LocalIndex
from app.retrieval.search import (
    Evidence,
    Hit,
    RetrievalResult,
    Retriever,
    SourceVersion,
)
from app.runtime import OwnedRuntime
from app.storage.documents import Documents
from app.storage.extractions import Extractions
from app.storage.files import UploadStore
from app.storage.index_state import IndexState
from app.storage.messages import Messages
from tests.evals.spikes.t27_runtime_smoke import (
    CountedJob,
    CountedTransport,
    Meter,
    supervise,
)

RUN_ROOT = PROJECT_ROOT / "data/t30-model-01"
SEAL = PROJECT_ROOT / "docs/proposals/t30-model-smoke-seal.json"


def check_sources() -> None:
    """Pin all app sources and both executed helpers before native construction."""
    expected = {
        p.relative_to(PROJECT_ROOT).as_posix()
        for p in (PROJECT_ROOT / "app").rglob("*.py")
    }
    expected.update(
        {
            "pyproject.toml",
            "uv.lock",
            "tests/evals/spikes/t30_model_smoke.py",
            "tests/evals/spikes/t27_runtime_smoke.py",
        }
    )
    seal = json.loads(SEAL.read_text(encoding="utf-8"))
    if seal.get("package") != "T30-N1" or set(seal.get("sha256", {})) != expected:
        raise OllamaError("SMOKE_SOURCE_MISMATCH")
    for name in expected:
        path = PROJECT_ROOT / name
        validate_local_ancestry(path)
        if (
            path.stat().st_size > 2_000_000
            or hashlib.sha256(path.read_bytes()).hexdigest() != seal["sha256"][name]
        ):
            raise OllamaError("SMOKE_SOURCE_MISMATCH")


async def run(meter: Meter) -> dict:
    """One owned Qwen tree; retrieval/index vectors are authored fixture seams."""
    store = UploadStore(meter.root / "app")
    try:
        conversation = Documents(store.connection).create_conversation()

        async def body():
            yield b"Name,Units\nNorth,42\nSouth,50\n"

        uploaded = await store.receive(
            body(), conversation, "smoke-upload-001", "authored.csv"
        )
        reference = uploaded["reference_id"]
        await Extractions(store).extract(conversation, reference, "smoke-extract-01")

        class Vectors:
            async def documents(self, chunks):
                return EmbeddingBatch(
                    "document",
                    tuple(
                        Embedding(c.chunk_id, c.text_hash, (1.0,) + (0.0,) * 767)
                        for c in chunks
                    ),
                    None,
                )

        @asynccontextmanager
        async def fixture_session():
            store.busy = True
            try:
                yield Vectors()
            finally:
                store.busy = False

        await LocalIndex(store).index(
            conversation, reference, "smoke-index-001", session_factory=fixture_session
        )
        state = IndexState(store)
        source, extraction = state.source(conversation, reference)
        status = state.status(conversation, reference)
        binding = store.connection.execute(
            "SELECT id FROM index_bindings WHERE extraction_id=? AND generation_id=?",
            (extraction["id"], status["generation_id"]),
        ).fetchone()[0]
        version = SourceVersion(
            reference,
            source["document_id"],
            source["content_hash"],
            extraction["id"],
            status["generation_id"],
            binding,
            status["chunk_count"],
            status["omission_count"],
        )
        chunk = state.chunks(conversation, reference)[0]
        hit = Hit(reference, chunk, 0.0)
        evidence = Evidence("ev_native", hit, chunk.text)
        result = RetrievalResult(
            "candidates",
            (hit,),
            (evidence,),
            (),
            (),
            (version,),
            (),
            len(chunk.text.encode()),
        )

        class Fixture:
            async def retrieve(self, *args, **kwargs):
                return result

            async def _recheck(self, *args):
                return await Retriever(store)._recheck(*args)

        Messages(store).select(conversation, [reference], 0)
        home = store.root / "staging/chat"
        for suffix in ("", "AppData/Roaming", "AppData/Local", "tmp"):
            (home / suffix).mkdir(parents=True, exist_ok=bool(suffix))
        settings = replace(Settings.from_env({}), data_root=store.root)
        owner = OwnedRuntime(
            settings,
            store,
            home,
            purpose="chat",
            process_factory=lambda: CountedJob(meter, "positive"),
            transport=CountedTransport(meter),
        )
        saved = await ChatService(
            store, retriever=Fixture(), chat_session=owner.session
        ).ask(conversation, "smoke-answer-001", "How many North units?", 1)
        answer = saved["answer"]
        if (
            saved["state"] != "complete"
            or answer["status"] != "answered"
            or not any(
                re.search(r"(?<!\d)42(?!\d)", c["text"]) for c in answer["claims"]
            )
            or any(set(c["citations"]) - {"ev_native"} for c in answer["claims"])
        ):
            raise OllamaError("SMOKE_ANSWER_FAILURE")
        with reserve_port(settings.ollama_port):
            pass
        owner.verify_assets(settings)
        root, identity = store.root, saved["answer_id"]
        store.close()
        store = UploadStore(root)
        if Messages(store).get(conversation, identity) != saved:
            raise OllamaError("SMOKE_PERSISTENCE_FAILURE")
        meter.check()
        return {
            "answer_contains_42": True,
            "citations_allowlisted": True,
            "restart_persisted": True,
            "port_released": True,
        }
    finally:
        store.close()


def main(argv=None) -> int:
    """Require explicit approval/offline flags, a distinct fresh root and one worker."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-approved", action="store_true")
    parser.add_argument("--offline-attested", action="store_true")
    parser.add_argument("--worker-token")
    args = parser.parse_args(argv)
    if not args.execute_approved or not args.offline_attested:
        print("T30-N1 requires separate approval/offline attestation; nothing started.")
        return 2
    if args.worker_token:
        meter = Meter.worker(RUN_ROOT, args.worker_token, package_id="T30-N1")
        result = {"package": "T30-N1", "status": "failed"}
        try:
            check_sources()
            result.update(asyncio.run(run(meter)), status="passed")
        except (Exception, KeyboardInterrupt) as error:  # noqa: BLE001 - manual native stop receipt
            meter.state["stopped"] = True
            result["code"] = (
                error.code
                if isinstance(error, (UploadError, OllamaError))
                else type(error).__name__
            )
        content = json.dumps(result).encode()
        meter.state["retained_charged"] += len(content)
        meter.save()
        (RUN_ROOT / "result.json").write_bytes(content)
        print(
            json.dumps(
                {
                    "package": "T30-N1",
                    "status": result["status"],
                    "code": result.get("code"),
                }
            )
        )
        return 0 if result["status"] == "passed" else 1
    try:
        validate_local_ancestry(RUN_ROOT)
        RUN_ROOT.mkdir(parents=True, exist_ok=False)
    except OSError:
        print("T30-N1 root exists/unavailable; preserve it and do not retry.")
        return 2
    meter = Meter(RUN_ROOT, package_id="T30-N1")
    try:
        check_sources()
        code = supervise(
            meter,
            [
                sys.executable,
                "-m",
                "tests.evals.spikes.t30_model_smoke",
                "--execute-approved",
                "--offline-attested",
                "--worker-token",
                meter.state["worker_token"],
            ],
        )
    except (OSError, ValueError, OllamaError):
        meter.state["stopped"] = True
        meter.save()
        code = 1
    print("T30-N1 finished; inspect local receipts; do not rerun.")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
