"""Local-only T10 client and reference-vector checks; no application adoption."""

import csv
import hashlib
import json
import math
import os
import re
import socket
import threading
import time
from pathlib import Path
from urllib.parse import urlparse

import httpx
from embedding_budget import Budget, NativeJob


class LocalClient:
    """Only the explicit project-owned loopback endpoint can receive evidence."""

    def __init__(
        self, budget: Budget, base_url="http://127.0.0.1:11434", transport=None
    ):
        parsed = urlparse(base_url)
        if (
            parsed.scheme != "http"
            or parsed.hostname != "127.0.0.1"
            or parsed.port != 11434
            or parsed.username
            or parsed.password
            or parsed.path not in {"", "/"}
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("Only approved loopback endpoint is allowed")
        self.budget = budget
        self.client = httpx.Client(
            base_url=base_url,
            trust_env=False,
            follow_redirects=False,
            transport=transport,
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.client.close()

    def request(self, method, path, **kwargs):
        """Refuse absolute URLs and charge attempts before network activity."""
        if (
            not path.startswith("/api/")
            or ":" in path
            or ".." in path
            or path.startswith("//")
        ):
            raise ValueError("Only local API paths")
        self.budget.call()
        response = self.client.request(
            method, path, timeout=min(120, self.budget.remaining()), **kwargs
        )
        response.raise_for_status()
        return response.json()


def validate_vectors(vectors, count: int, dimensions: int = 768) -> None:
    """Reject wrong shapes, nonfinite values and unusable zero embeddings."""
    if len(vectors) != count:
        raise ValueError("Wrong embedding count")
    for vector in vectors:
        if len(vector) != dimensions or not all(
            isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
            for v in vector
        ):
            raise ValueError("Invalid embedding")
        squared_norm = sum(v * v for v in vector)
        if not math.isfinite(squared_norm) or squared_norm == 0:
            raise ValueError("Invalid embedding norm")


def rank(query, vectors) -> list[int]:
    """Deterministic cosine reference search without another dependency."""
    scores = []
    qnorm = math.sqrt(sum(v * v for v in query))
    for index, vector in enumerate(vectors):
        norm = math.sqrt(sum(v * v for v in vector))
        scores.append(
            (
                sum(a * b for a, b in zip(query, vector, strict=True)) / (qnorm * norm),
                index,
            )
        )
    return [index for _, index in sorted(scores, key=lambda pair: (-pair[0], pair[1]))]


def corpus(root: Path) -> dict:
    """Freeze two-year CSV evidence with real physical-line/column provenance."""
    manifest = json.loads((root / "tests/evals/manifest.json").read_text())
    questions = json.loads((root / "tests/evals/questions.json").read_text())[
        "questions"
    ]
    passages, hashes = [], {}
    for source in [s for s in manifest["source_samples"] if s["id"] in {"R08", "R09"}]:
        path = root / source["path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != source["sha256"]:
            raise ValueError("Source hash changed")
        hashes[source["id"]] = digest
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream, strict=True)
            headers = next(reader)
            previous = reader.line_num
            for index, row in enumerate(reader, 1):
                if index > 16:
                    break
                fields = {
                    key: row[headers.index(key)]
                    for key in ["DataSeries", "2025", "2024"]
                }
                measure = "output" if source["id"] == "R08" else "workers"
                passages.append(
                    {
                        "id": f"{source['id']}:{index + 1}",
                        "source": source["id"],
                        "filename": source["name"],
                        "data_record": index,
                        "lines": [previous + 1, reader.line_num],
                        "columns": fields,
                        "text": f"Measure: {measure}. Industry: {fields['DataSeries'].strip()}. 2025: {fields['2025']}. 2024: {fields['2024']}.",
                    }
                )
                previous = reader.line_num
    variants = [
        [
            "What is the 2025 Total Manufacturing workers entry?",
            "Find the total manufacturing employment figure for 2025.",
        ],
        [
            "Retrieve total manufacturing workers for 2024 and 2025 to calculate their change.",
            "How did overall manufacturing employment move between 2024 and 2025?",
        ],
        [
            "Find both total manufacturing output and workers entries in 2025.",
            "Give the separate 2025 manufacturing output and employment figures.",
        ],
        [
            "Find 2025 workers in Food, Beverage & Tobacco.",
            "What is the food, beverage and tobacco employment entry for 2025?",
        ],
    ]
    queries = []
    for q, wording in zip(questions[:4], variants, strict=True):
        gold = sorted(
            {f"{e['fixture']}:{e['physical_line']}" for e in q["expected"]["evidence"]}
        )
        for number, text in enumerate([q["question"]] + wording):
            queries.append(
                {
                    "id": f"{q['id']}-v{number}",
                    "parent_question": q["id"],
                    "text": text,
                    "gold": gold,
                }
            )
    if (
        len(passages) != 32
        or len(queries) != 12
        or any(
            not set(q["gold"]).issubset({p["id"] for p in passages}) for q in queries
        )
    ):
        raise ValueError("Corpus readiness")
    return {
        "passages": passages,
        "queries": queries,
        "source_hashes": hashes,
        "field_subset": ["DataSeries", "2025", "2024"],
    }


def local_environment(root: Path, executable: Path) -> dict:
    """Only the child receives isolated model/config/temp and CPU/cloud settings."""
    home = root / "data/ollama/runtime-home"
    env = dict(os.environ)
    for key, suffix in [
        ("USERPROFILE", ""),
        ("APPDATA", "AppData/Roaming"),
        ("LOCALAPPDATA", "AppData/Local"),
        ("TEMP", "tmp"),
        ("TMP", "tmp"),
    ]:
        path = home / suffix
        path.mkdir(parents=True, exist_ok=True)
        env[key] = str(path)
    env.update(
        OLLAMA_HOST="127.0.0.1:11434",
        OLLAMA_MODELS=str(root / "data/ollama/models"),
        OLLAMA_NO_CLOUD="1",
        OLLAMA_NUM_PARALLEL="1",
        OLLAMA_MAX_LOADED_MODELS="1",
        OLLAMA_DEBUG="false",
        CUDA_VISIBLE_DEVICES="-1",
        HIP_VISIBLE_DEVICES="-1",
        OLLAMA_VULKAN="false",
        OLLAMA_IGPU_ENABLE="false",
    )
    env["PATH"] = str(executable.parent) + os.pathsep + env.get("PATH", "")
    return env


def observe_job(job, observations: list, failures: list, diagnostic_path: Path) -> bool:
    """Persist a resource stop before teardown obscures it with a socket error."""
    try:
        observations.append(job.refresh())
        if (
            sum(
                p.stat().st_size
                for p in diagnostic_path.parent.rglob("*")
                if p.is_file()
            )
            > 64 * 1024**2
        ):
            raise RuntimeError("Continuation output allowance")
        return True
    except (OSError, RuntimeError) as error:
        detail = {
            "type": type(error).__name__,
            "reason": str(error),
            "time": time.time(),
        }
        failures.append(detail)
        try:
            diagnostic_path.write_text(json.dumps(detail), encoding="utf-8")
        finally:
            job.close()
        return False


def benchmark(root: Path, continuation: bool = False) -> None:
    """Run the approved frozen two-model comparison with owned-server teardown."""
    run = root / ("data/t10/continuation-01" if continuation else "data/t10/run-01")
    budget = Budget(run / "meter.json")
    budget.reserve_processes(2)  # Windows venv launcher and this controller.
    frozen = corpus(root)
    if continuation:
        original = root / "data/t10/run-01/results.json"
        if (
            hashlib.sha256(original.read_bytes()).hexdigest()
            != "5a2c9f5e6316205d162ef2bc99d6b0316deee06ee945d5cea0451c7fa8eddab3"
        ):
            raise RuntimeError("Original result changed")
        if frozen != json.loads(
            (original.parent / "corpus.json").read_text(encoding="utf-8")
        ):
            raise RuntimeError("Frozen corpus changed")
    (run / "corpus.json").write_text(json.dumps(frozen, indent=2), encoding="utf-8")
    executable = root / ".venv/tools/ollama/0.40.16/ollama.exe"
    if not executable.is_file():
        raise RuntimeError("Verified native artifact missing")
    with socket.socket() as probe:
        if probe.connect_ex(("127.0.0.1", 11434)) == 0:
            raise RuntimeError("Port belongs to an existing service")
    env = local_environment(root, executable)
    budget.start_benchmark()
    job = NativeJob(budget)
    failure, observations = [], []
    stop = threading.Event()
    controller_handle = None
    result = {
        "schedule": {
            "models": ["nomic-embed-text:v1.5"]
            if continuation
            else ["embeddinggemma:300m", "nomic-embed-text:v1.5"],
            "repetitions": 4,
            "batch": 4,
            "single_subset": 8,
            "dimensions": 768,
        },
        "corpus_sha256": hashlib.sha256((run / "corpus.json").read_bytes()).hexdigest(),
        "code_sha256": {
            name: hashlib.sha256(
                (Path(__file__).parent / name).read_bytes()
            ).hexdigest()
            for name in [
                "embedding_trial.py",
                "embedding_budget.py",
                "test_embedding_trial.py",
            ]
        },
        "models": [],
        "diagnostics": [],
        "memory": observations,
        "supervisor_failures": failure,
        "continuation": continuation,
    }

    def observe():
        while not stop.wait(1):
            if not observe_job(
                job, observations, failure, run / "stop-diagnostics.json"
            ):
                return

    try:
        with (run / "engine.log").open("ab") as output:
            process = job.start([str(executable), "serve"], env, output)
            controller_handle = job.bound_controller()
            watcher = threading.Thread(target=observe, daemon=True)
            watcher.start()
            with LocalClient(budget) as client:
                for _ in range(20):
                    if process.poll() is not None:
                        raise RuntimeError("Owned server exited during startup")
                    try:
                        result["version"] = client.request("GET", "/api/version")
                        break
                    except httpx.ConnectError:
                        time.sleep(0.5)
                else:
                    raise RuntimeError("Owned server did not become ready")
                result["tags"] = client.request("GET", "/api/tags")
                if result["version"].get("version") != "0.40.16":
                    raise RuntimeError("Runtime version drift")
                texts = [p["text"] for p in frozen["passages"]]
                query_texts = [q["text"] for q in frozen["queries"]]
                for model in result["schedule"]["models"]:
                    detail = {
                        "model": model,
                        "show": client.request(
                            "POST", "/api/show", json={"model": model}
                        ),
                        "batches": [],
                        "repetitions": [],
                        "single_batches": [],
                    }
                    result["models"].append(detail)

                    def embed(inputs, kind, records, selected_model=model):
                        if failure:
                            raise RuntimeError("Resource supervisor stopped the run")
                        observations.append(job.refresh())
                        if selected_model.startswith("embeddinggemma"):
                            prefix = (
                                "title: none | text: "
                                if kind == "document"
                                else "task: search result | query: "
                            )
                        else:
                            prefix = (
                                "search_document: "
                                if kind == "document"
                                else "search_query: "
                            )
                        started = time.perf_counter()
                        response = client.request(
                            "POST",
                            "/api/embed",
                            json={
                                "model": selected_model,
                                "input": [prefix + t for t in inputs],
                                "truncate": False,
                                "keep_alive": "10m",
                                "options": {
                                    "num_gpu": 0,
                                    "num_thread": 4,
                                    "num_ctx": 2048,
                                    "num_batch": 64,
                                },
                            },
                        )
                        validate_vectors(response["embeddings"], len(inputs))
                        records.append(
                            {
                                "kind": kind,
                                "inputs": len(inputs),
                                "elapsed_s": time.perf_counter() - started,
                                "engine_total_ns": response.get("total_duration"),
                                "load_ns": response.get("load_duration"),
                                "tokens": response.get("prompt_eval_count"),
                            }
                        )
                        observations.append(job.refresh())
                        return response["embeddings"]

                    for repetition in range(4):
                        documents, queries = [], []
                        for index in range(0, 32, 4):
                            documents.extend(
                                embed(
                                    texts[index : index + 4],
                                    "document",
                                    detail["batches"],
                                )
                            )
                        for index in range(0, 12, 4):
                            queries.extend(
                                embed(
                                    query_texts[index : index + 4],
                                    "query",
                                    detail["batches"],
                                )
                            )
                        ranks = []
                        for query, vector in zip(
                            frozen["queries"], queries, strict=True
                        ):
                            selected = [
                                frozen["passages"][i]["id"]
                                for i in rank(vector, documents)[:5]
                            ]
                            ranks.append(
                                {
                                    "query": query["id"],
                                    "top5": selected,
                                    "recall5": len(set(query["gold"]) & set(selected))
                                    / len(query["gold"]),
                                    "precision5": len(
                                        set(query["gold"]) & set(selected)
                                    )
                                    / 5,
                                }
                            )
                        detail["repetitions"].append(
                            {"number": repetition, "ranks": ranks}
                        )
                    detail["ps"] = client.request("GET", "/api/ps")
                    if not detail["ps"].get("models") or any(
                        m.get("size_vram", -1) != 0 for m in detail["ps"]["models"]
                    ):
                        raise RuntimeError("CPU-only observation failed")
                    for _ in range(4):
                        for text in texts[:8]:
                            embed([text], "document", detail["single_batches"])
                    try:
                        client.request(
                            "POST",
                            "/api/embed",
                            json={
                                "model": model,
                                "input": "budget " * 10000,
                                "truncate": False,
                                "options": {
                                    "num_gpu": 0,
                                    "num_thread": 4,
                                    "num_ctx": 2048,
                                    "num_batch": 64,
                                },
                            },
                        )
                        detail["over_limit"] = "unexpected_success"
                    except httpx.HTTPStatusError as error:
                        detail["over_limit"] = error.response.status_code
                    detail["unload"] = client.request(
                        "POST",
                        "/api/embed",
                        json={"model": model, "input": [], "keep_alive": 0},
                    )
                    (run / "results.json").write_text(
                        json.dumps(result), encoding="utf-8"
                    )
                tokenized = [
                    set(re.findall(r"[a-z0-9]+", text.lower())) for text in texts
                ]
                result["lexical"] = []
                for query in frozen["queries"]:
                    tokens = set(re.findall(r"[a-z0-9]+", query["text"].lower()))
                    order = sorted(
                        range(len(texts)),
                        key=lambda i: (-len(tokens & tokenized[i]), i),
                    )[:5]
                    found = [frozen["passages"][i]["id"] for i in order]
                    result["lexical"].append(
                        {
                            "query": query["id"],
                            "top5": found,
                            "recall5": len(set(query["gold"]) & set(found))
                            / len(query["gold"]),
                        }
                    )
    except BaseException as error:
        result["failure"] = type(error).__name__
        raise
    finally:
        stop.set()
        if "watcher" in locals():
            watcher.join(timeout=3)
        if job.handle:
            try:
                observations.append(job.refresh())
            except (OSError, RuntimeError) as error:
                result["final_observation_failure"] = {
                    "type": type(error).__name__,
                    "reason": str(error),
                }
            finally:
                job.close()
        if controller_handle:
            job.kernel.CloseHandle(controller_handle)
        result["meter"] = budget.read()
        (run / "results.json").write_text(json.dumps(result), encoding="utf-8")
        with socket.socket() as probe:
            result["port_released"] = probe.connect_ex(("127.0.0.1", 11434)) != 0
        (run / "results.json").write_text(json.dumps(result), encoding="utf-8")
        print(
            json.dumps(
                {
                    "models_completed": len(
                        [m for m in result["models"] if "unload" in m]
                    ),
                    "failure": result.get("failure"),
                    "calls": result["meter"]["calls"],
                    "processes": result["meter"]["processes"],
                    "port_released": result["port_released"],
                }
            ),
            flush=True,
        )
