"""R1: bounded public text research only; never load candidate native/model assets."""

import ctypes
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".venv/Lib/site-packages"))
sys.path.insert(0, str(Path(__file__).parent))
PYTHON = Path("F:/Python/Python314/python.exe")
RUN = ROOT / "data/t17/public-review-01"
METER = RUN / "meter.json"
REPOS = {
    "ollama/ollama", "fastapi/fastapi", "encode/starlette", "pydantic/pydantic",
    "pydantic/pydantic-core", "encode/uvicorn", "encode/httpx", "encode/httpcore",
    "python-hyper/h11", "jsvine/pdfplumber", "pdfminer/pdfminer.six",
    "pypdfium2-team/pypdfium2", "python-pillow/pillow", "tiran/defusedxml",
    "sirfz/tesserocr", "tesseract-ocr/tesseract", "danbloomberg/leptonica",
    "asg017/sqlite-vec", "pyca/cryptography", "python-cffi/cffi",
}
OLLAMA = "https://raw.githubusercontent.com/ollama/ollama/v0.40.16/"
URLS = [OLLAMA + p for p in ("api/types.go", "server/routes.go", "llm/server.go",
                             "template/template.go")]
URLS += ["https://api.github.com/repos/ollama/ollama/git/ref/tags/v0.40.16"]
URLS += [f"https://api.github.com/repos/{r}/security-advisories?per_page=100"
         for r in sorted(REPOS)]
URLS += ["https://openpyxl.readthedocs.io/en/3.1/",
         "https://raw.githubusercontent.com/asg017/sqlite-vec/"
         "e9f598abfa0c06b328d8fe5da9c3760cce74be10/LICENSE-MIT",
         "https://raw.githubusercontent.com/asg017/sqlite-vec/"
         "e9f598abfa0c06b328d8fe5da9c3760cce74be10/LICENSE-APACHE"]


def validate_url(url):
    """Restrict credentials, scheme, host, upstream repository and runtime revision."""
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.username or parsed.password
            or parsed.port not in (None, 443) or parsed.fragment):
        raise ValueError("URL boundary")
    parts = parsed.path.strip("/").split("/")
    if parsed.hostname == "openpyxl.readthedocs.io" and parsed.path == "/en/3.1/":
        return
    if parsed.hostname == "api.github.com":
        if len(parts) < 4 or parts[0] != "repos":
            raise ValueError("Repository API only")
        repo = "/".join(parts[1:3]).lower()
        if repo in REPOS and (parts[3] == "security-advisories" or
                             (repo == "ollama/ollama" and
                              parts[3:] == ["git", "ref", "tags", "v0.40.16"])):
            return
    if parsed.hostname == "raw.githubusercontent.com" and len(parts) >= 4:
        repo = "/".join(parts[:2]).lower()
        if repo == "ollama/ollama" and parts[2] == "v0.40.16":
            return
        if repo == "asg017/sqlite-vec" and parts[2] == (
                "e9f598abfa0c06b328d8fe5da9c3760cce74be10"):
            return
    if parsed.hostname == "github.com" and len(parts) >= 2:
        if "/".join(parts[:2]).lower() in REPOS:
            return
    raise ValueError("Host/repository/revision boundary")


def collect(state, save, chunks, clock, deadline):
    """Persist attempt/full body reservation before opening lazy fake/real transport."""
    if state["http_attempts"] >= 32 or state["pending_bytes"]:
        raise RuntimeError("Attempt/pending boundary")
    if state["body_bytes"] + 1048576 > 8388608:
        raise RuntimeError("Total response reservation boundary")
    state["http_attempts"] += 1
    state["pending_bytes"] = 1048576
    save()
    data = bytearray()
    for chunk in chunks:
        if clock() > deadline:
            raise RuntimeError("Whole request deadline")
        if len(data) + len(chunk) > 1048576:
            raise RuntimeError("Response body limit")
        data.extend(chunk)
    if clock() > deadline:
        raise RuntimeError("Whole request deadline")
    state["body_bytes"] += len(data)
    state["pending_bytes"] = 0
    save()
    return bytes(data)


def excerpt(text):
    """Keep bounded source context around fit/truncation terms, never execute it."""
    lines = text.splitlines()
    selected = set()
    for i, line in enumerate(lines):
        if re.search(r"tokeniz|truncat|num_ctx|context.?length|/api/", line, re.I):
            selected.update(range(max(0, i - 2), min(len(lines), i + 4)))
    return "\n".join(f"{i + 1}:{lines[i]}" for i in sorted(selected))[:40000]


def read():
    return json.loads(METER.read_text(encoding="utf-8-sig"))


def worker_args():
    """Avoid the Windows venv redirector under the one-process HTTP-helper job."""
    return [str(PYTHON), "-I", "-S", "-B", str(Path(__file__)), "worker"]


def save(path, value):
    data = json.dumps(value, indent=2).encode()
    current = sum(p.stat().st_size for p in RUN.iterdir() if p.is_file())
    if current + len(data) > 2097152:
        raise RuntimeError("Output boundary")
    pending = path.with_suffix(".tmp")
    pending.write_bytes(data)
    pending.replace(path)


def prepared():
    state = read()
    block = state["preparation_block"]
    tick = ctypes.c_int64()
    ctypes.windll.kernel32.QueryPerformanceCounter(ctypes.byref(tick))
    elapsed = (tick.value - block["started_tick"]) / block["frequency"]
    if (state["status"] not in ("preparing", "ready") or
            state["http_attempts"] or state.get("fetch_started") or
            not 0 <= elapsed <= 600):
        raise RuntimeError("Prepaid preparation boundary")
    if state.get("seal"):
        state.setdefault("readiness_revisions", []).append(state["seal"])
        state["events"].append("Pre-fetch launch correction; original seal retained; no epoch/counter reset")
    state["preparation_block"]["state"] = "closed_full_debit"
    state["preparation_elapsed_observed"] = elapsed
    state["seal"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in (Path(__file__), Path(__file__).with_name(
                         "test_public_source_review.py"), ROOT / "pyproject.toml",
                         ROOT / "uv.lock", Path(__file__).with_name("embedding_budget.py"))}
    state["seal"][str(PYTHON)] = hashlib.sha256(PYTHON.read_bytes()).hexdigest()
    state["status"] = "ready"
    save(METER, state)
    print("R1 ready; no network request made")


def worker():
    import httpx

    state = read()
    results = []
    with httpx.Client(trust_env=False, follow_redirects=False,
                      headers={"User-Agent": "DocumentAssistant-PublicReview",
                               "Accept-Encoding": "identity"}) as client:
        for original in URLS:
            url = original
            while True:
                validate_url(url)
                state["request_started"] = time.monotonic()
                state["request_url"] = url
                meta = {}

                def stream():
                    with client.stream("GET", url, timeout=20) as response:
                        meta.update(status=response.status_code,
                                    location=response.headers.get("location"),
                                    more=bool(response.headers.get("link")),
                                    content_type=response.headers.get("content-type", ""))
                        kind = meta["content_type"].lower()
                        if not any(k in kind for k in ("text/", "json")):
                            raise RuntimeError("Non-text response refused")
                        yield from response.iter_bytes(chunk_size=16384)

                data = collect(state, lambda: save(METER, state), stream(),
                               time.monotonic, state["request_started"] + 20)
                text_value = data.decode("utf-8", errors="replace")
                record = {"url": url, **meta, "bytes": len(data),
                          "sha256": hashlib.sha256(data).hexdigest()}
                if "security-advisories" in url and meta["status"] == 200:
                    entries = json.loads(data)
                    if not isinstance(entries, list):
                        raise ValueError("Unexpected advisory shape")
                    record["advisories"] = [
                        {k: item.get(k) for k in ("ghsa_id", "cve_id", "summary",
                                                 "html_url", "vulnerabilities")}
                        for item in entries]
                else:
                    record["excerpt"] = excerpt(text_value) or text_value[:1200]
                results.append(record)
                state["request_started"] = None
                save(METER, state)
                save(RUN / "sources.json", results)
                if meta["status"] in (301, 302, 303, 307, 308):
                    url = urljoin(url, meta["location"] or "")
                    continue
                break


def supervise():
    from embedding_budget import NativeJob, memory_snapshot

    state = read()
    if state["status"] != "ready" or state.get("fetch_started"):
        raise RuntimeError("Never repeat an admitted research run")
    for name, digest in state["seal"].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise RuntimeError("Readiness drift")
    state.update(status="running", fetch_started=time.monotonic(),
                 request_started=None)
    save(METER, state)

    class Reserved:
        def reserve_processes(self, count):
            if count != 1:
                raise RuntimeError("Unexpected child count")

    job = None
    child = None
    result = {"status": "stopped_no_retry", "teardown_verified": False}
    started = time.monotonic()
    peak = 0
    free = 2**63
    try:
        job = NativeJob(Reserved())
        limits = job.Extended()
        limits.basic.flags = 0x2000 | 0x8 | 0x100 | 0x200
        limits.basic.active = 1
        limits.process_memory = limits.job_memory = 536870912
        if not job.kernel.SetInformationJobObject(
                job.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            raise ctypes.WinError(ctypes.get_last_error())
        env = {k: os.environ[k] for k in ("SystemRoot", "WINDIR") if k in os.environ}
        with (RUN / "worker.log").open("wb") as output:
            child = job.start(worker_args(), env, output)
            while child.poll() is None:
                state = read()
                now = time.monotonic()
                if now - started > 235 or (state.get("request_started") and
                                          now - state["request_started"] > 20):
                    raise RuntimeError("Request or total research deadline")
                memory = memory_snapshot()
                free = min(free, memory["available_physical"])
                observed = job.Extended()
                if not job.kernel.QueryInformationJobObject(
                        job.handle, 9, ctypes.byref(observed), ctypes.sizeof(observed), None):
                    raise ctypes.WinError(ctypes.get_last_error())
                peak = max(peak, observed.peak_job)
                if free < 4294967296 or memory["controller_private"] > 536870912:
                    raise RuntimeError("Memory/headroom boundary")
                time.sleep(0.05)
        result["worker_exit"] = child.returncode
        result["status"] = "completed_pending_review" if child.returncode == 0 else "stopped_no_retry"
    except Exception as error:
        result["error_type"] = type(error).__name__
    finally:
        if job:
            job.close()
        if child:
            child.wait(timeout=5)
            result["teardown_verified"] = child.poll() is not None
        else:
            result["teardown_verified"] = True
        state = read()
        state["fetch_active_seconds"] = time.monotonic() - started
        state["charged_seconds"] += state["fetch_active_seconds"]
        state["status"] = "closed"
        result.update(http_attempts=state["http_attempts"], body_bytes=state["body_bytes"],
                      pending_bytes=state["pending_bytes"], job_peak=peak,
                      min_available=free, charged_seconds=state["charged_seconds"])
        save(METER, state)
        save(RUN / "summary.json", result)
        print(json.dumps(result))


if __name__ == "__main__":
    {"prepare": prepared, "fetch": supervise, "worker": worker}[sys.argv[1]]()
