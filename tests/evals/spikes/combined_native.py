"""Offline-only Windows supervision and local inference for the bounded T11 run.

Importing this module does not import OCR/image/inference packages. Runtime raw
content stays in the ignored run directory; console/summary output is sanitized.
"""

from __future__ import annotations

import ctypes
import html
import json
import threading
import time
from contextlib import contextmanager
from ctypes import wintypes as w
from pathlib import Path

import combined_trial as core


class CallBudget:
    """Adapt the prior streaming client to a shared ledger and 90-second limit."""

    def __init__(self, ledger):
        self.ledger = ledger
        self.deadline = time.monotonic() + 90

    def call(self):
        self.ledger.call()

    def remaining(self):
        remaining = min(self.ledger.remaining(), self.deadline - time.monotonic())
        if remaining <= 0:
            raise RuntimeError("Chat deadline")
        return remaining


class StreamClient:
    """Expose actual response-header arrival before starting an overlapping OCR."""

    def __init__(self, client, event, interval):
        self.client, self.event, self.interval = client, event, interval

    @contextmanager
    def stream(self, method, path, **options):
        if method != "POST" or path != "/api/chat":
            raise ValueError("Only the fixed chat stream")
        with self.client.stream(method, path, **options) as response:
            self.interval.append(time.monotonic())
            self.event.set()
            try:
                yield response
            finally:
                self.interval.append(time.monotonic())


class API:
    """No redirects/proxies/remote routes; every request consumes the shared meter."""

    def __init__(self, supervisor):
        import httpx

        self.supervisor = supervisor
        self.client = httpx.Client(
            base_url="http://127.0.0.1:11434",
            trust_env=False,
            follow_redirects=False,
            timeout=60,
        )

    def request(self, method, path, body=None):
        allowed = {
            ("GET", "/api/version"),
            ("GET", "/api/tags"),
            ("GET", "/api/ps"),
            ("POST", "/api/show"),
            ("POST", "/api/embed"),
            ("POST", "/api/generate"),
        }
        if (method, path) not in allowed:
            raise ValueError("Unapproved API endpoint")
        if body is not None and body.get("model") not in core.MODELS:
            raise ValueError("Unapproved model")
        if path == "/api/generate" and (
            set(body) != {"model", "keep_alive"} or body["keep_alive"] != 0
        ):
            raise ValueError("Generate endpoint is unload-only")
        self.supervisor.ledger.call()
        self.supervisor.check_failure()
        timer = threading.Timer(
            min(60, self.supervisor.ledger.remaining()),
            lambda: self.supervisor.fail("API hard deadline"),
        )
        timer.daemon = True
        timer.start()
        try:
            with self.client.stream(method, path, json=body) as response:
                response.raise_for_status()
                output = bytearray()
                for block in response.iter_bytes():
                    output.extend(block)
                    if len(output) > 4 * 1024**2:
                        raise RuntimeError("API response byte limit")
                self.supervisor.check_failure()
                return json.loads(output)
        finally:
            timer.cancel()

    def embed(self, texts, query=False):
        """Preserve the previous Nomic input contract and full vector dimensions."""
        from embedding_trial import validate_vectors

        response = self.request(
            "POST",
            "/api/embed",
            {
                "model": core.EMBED,
                "input": [
                    ("search_query: " if query else "search_document: ") + t
                    for t in texts
                ],
                "truncate": False,
                "keep_alive": 600,
                "options": {
                    "num_gpu": 0,
                    "num_thread": 4,
                    "num_ctx": 2048,
                    "num_batch": 64,
                },
            },
        )
        validate_vectors(response["embeddings"], len(texts))
        return response


class Supervisor:
    """Own aggregate/job limits before launch; observe all descendants together."""

    def __init__(self, ledger):
        import ocr_trial as ocr
        from appcontainer_preflight import ExtendedLimits, Native
        from embedding_budget import NativeJob

        self.ledger, self.ocr = ledger, ocr
        self.native = Native()
        self.failed, self.stop = threading.Event(), threading.Event()
        self.failure, self.thread, self.process = None, None, None
        self.samples = []
        self.inference_threads = []
        self.root_job, self.server = None, None
        self.runner = None
        self.root_job = self.native.job(16, kill=True)
        limits = ExtendedLimits()
        limits.basic.flags = (
            0x8 | 0x200 | 0x2000
        )  # aggregate cap, no inherited private-process cap
        limits.basic.active, limits.job_memory = 16, 8 * 1024**3
        self.native.check(
            self.native.kernel.SetInformationJobObject(
                self.root_job, 9, ctypes.byref(limits), ctypes.sizeof(limits)
            )
        )
        self.native.check(
            self.native.kernel.AssignProcessToJobObject(
                self.root_job, self.native.kernel.GetCurrentProcess()
            )
        )
        actual = ExtendedLimits()
        self.native.check(
            self.native.kernel.QueryInformationJobObject(
                self.root_job, 9, ctypes.byref(actual), ctypes.sizeof(actual), None
            )
        )
        if actual.basic.flags & 0x100 or actual.job_memory != 8 * 1024**3:
            raise RuntimeError("Aggregate limit setup mismatch")

        class ServerBudget:
            def reserve_processes(_, count):
                ledger.reserve("controller", count, "Owned server root", native=True)

        self.server = NativeJob(ServerBudget())
        # Remove its historical per-process/6-GiB caps: the outer job enforces 8 GiB total.
        server_limits = self.server.Extended()
        server_limits.basic.flags, server_limits.basic.active = 0x8 | 0x2000, 8
        self.native.check(
            self.native.kernel.SetInformationJobObject(
                self.server.handle,
                9,
                ctypes.byref(server_limits),
                ctypes.sizeof(server_limits),
            )
        )
        self.native.kernel.OpenProcess.argtypes = [w.DWORD, w.BOOL, w.DWORD]
        self.native.kernel.OpenProcess.restype = w.HANDLE

        # Bind the reused OCR launcher to this new allocation only. Old ledgers are never opened.
        ocr.RUN = core.RUN
        ocr.charge = lambda _path, label, slots, **_: ledger.reserve(
            "ocr", slots, label, native=True
        )

        class OCRRunner(ocr.OwnedRunner):
            def check_storage(_, **options):
                self.check_failure()
                self.storage()

        self.runner = OCRRunner()

    def pids(self, handle):
        class Processes(ctypes.Structure):
            _fields_ = [
                ("assigned", w.DWORD),
                ("listed", w.DWORD),
                ("ids", ctypes.c_size_t * 64),
            ]

        result = Processes()
        self.native.check(
            self.native.kernel.QueryInformationJobObject(
                handle, 3, ctypes.byref(result), ctypes.sizeof(result), None
            )
        )
        if result.listed > 64 or result.assigned != result.listed:
            raise RuntimeError("Incomplete process ownership snapshot")
        return list(result.ids[: result.listed])

    def storage(self):
        for area, path, cap in (
            ("run", core.RUN, 512 * 1024**2),
            ("raw", core.RUN / "raw", 32 * 1024**2),
            ("answers", core.RUN / "answers", 8 * 1024**2),
        ):
            try:
                core.live_tree_bytes(path, cap)
            except OSError as error:
                error.trial_storage_area = area
                raise

    def check_failure(self):
        if self.failed.is_set():
            raise RuntimeError(self.failure or "Supervisor stopped")

    def fail(self, reason):
        if self.failure is None:
            self.failure = reason
        self.failed.set()
        if self.server:
            self.native.kernel.TerminateJobObject(self.server.handle, 125)
        # Only the runner's own direct worker PIDs; kernel active-process cap forbids children.
        for pid in list(self.runner.children if self.runner else []):
            handle = self.native.kernel.OpenProcess(0x1001, False, pid)
            if handle:
                try:
                    inside = w.BOOL()
                    # A PID can be recycled after exit; verify its current job before acting.
                    if (
                        self.native.kernel.IsProcessInJob(
                            handle, self.root_job, ctypes.byref(inside)
                        )
                        and inside.value
                    ):
                        self.native.kernel.TerminateProcess(handle, 125)
                finally:
                    self.native.kernel.CloseHandle(handle)

    def sample(self, gap=0):
        from appcontainer_preflight import ExtendedLimits
        from embedding_budget import memory_snapshot

        self.ocr.ensure_disconnected()
        self.ledger.remaining()
        self.ledger.observe_native(self.native.accounting(self.root_job)["total"] - 1)
        counters = memory_snapshot()
        owned = []
        for pid in self.pids(self.root_job):
            handle = self.native.kernel.OpenProcess(0x410, False, pid)
            if not handle:
                if pid not in self.pids(self.root_job):
                    continue
                raise RuntimeError("Owned process memory unavailable")
            try:
                try:
                    memory = self.ocr.process_memory(handle)
                except OSError:
                    if pid not in self.pids(self.root_job):
                        continue
                    raise
                owned.append({"pid": pid, **memory})
            finally:
                self.native.kernel.CloseHandle(handle)
        peak = ExtendedLimits()
        self.native.check(
            self.native.kernel.QueryInformationJobObject(
                self.root_job, 9, ctypes.byref(peak), ctypes.sizeof(peak), None
            )
        )
        observation = {
            "at": time.monotonic(),
            **counters,
            "processes": owned,
            "owned_private": sum(p["private_observed"] for p in owned),
            "peak_job": peak.peak_job,
            "sampling_gap": gap,
        }
        core.check_resources(observation, gap)
        self.server._check_tcp()
        self.storage()
        self.samples.append(observation)

    def observe(self):
        previous = time.monotonic()
        while not self.stop.is_set():
            try:
                now = time.monotonic()
                self.sample(now - previous)
                previous = now
            except Exception as error:  # noqa: BLE001 - thread boundary must stop all owned work.
                if isinstance(error, OSError):
                    self.filesystem_failure = core.record_filesystem_error(
                        error, core.RUN
                    )
                    self.fail(type(error).__name__ + ": filesystem inspection boundary")
                else:
                    self.fail(type(error).__name__ + ": " + str(error)[:160])
                break
            self.stop.wait(0.1)

    def server_listener_owned(self):
        """Read listener PIDs, refusing any service not in the owned server job."""
        api = ctypes.WinDLL("iphlpapi", use_last_error=True)
        api.GetExtendedTcpTable.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
            w.BOOL,
            w.ULONG,
            ctypes.c_int,
            w.ULONG,
        ]
        found = []
        for family, size, port_offset, state_offset, pid_offset in (
            (2, 24, 8, 0, 20),
            (23, 56, 20, 48, 52),
        ):
            length = w.ULONG()
            status = api.GetExtendedTcpTable(
                None, ctypes.byref(length), False, family, 5, 0
            )
            if status not in {0, 122} or length.value > 4 * 1024**2:
                raise RuntimeError("Listener metadata unavailable")
            buffer = ctypes.create_string_buffer(length.value)
            self.native.check(
                api.GetExtendedTcpTable(
                    buffer, ctypes.byref(length), False, family, 5, 0
                )
                == 0
            )
            raw = buffer.raw
            count = int.from_bytes(raw[:4], "little")
            if 4 + count * size > len(raw):
                raise RuntimeError("Invalid listener table")
            for index in range(count):
                row = raw[4 + index * size : 4 + (index + 1) * size]
                if (
                    int.from_bytes(row[state_offset : state_offset + 4], "little") == 2
                    and int.from_bytes(row[port_offset : port_offset + 2], "big")
                    == 11434
                ):
                    found.append(
                        int.from_bytes(row[pid_offset : pid_offset + 4], "little")
                    )
        if any(pid not in self.pids(self.server.handle) for pid in found):
            raise RuntimeError("Unrelated listener owns trial port")
        return bool(found)

    def launch(self):
        from embedding_trial import local_environment

        env = local_environment(core.ROOT, core.EXECUTABLE)
        env["OLLAMA_MAX_LOADED_MODELS"] = "2"
        # New runtime home prevents this trial mutating the older trials' runtime configuration.
        home = core.RUN / "runtime-home"
        for key, suffix in (
            ("USERPROFILE", ""),
            ("APPDATA", "AppData/Roaming"),
            ("LOCALAPPDATA", "AppData/Local"),
            ("TEMP", "tmp"),
            ("TMP", "tmp"),
        ):
            path = home / suffix
            path.mkdir(parents=True, exist_ok=True)
            env[key] = str(path)
        self.log = (core.RUN / "engine.log").open("wb")
        self.process = self.server.start([str(core.EXECUTABLE), "serve"], env, self.log)
        self.thread = threading.Thread(target=self.observe, daemon=True)
        self.thread.start()
        deadline = time.monotonic() + 60
        while not self.server_listener_owned():
            self.check_failure()
            if self.process.poll() is not None or time.monotonic() >= deadline:
                raise RuntimeError("Owned server startup failed/deadline")
            time.sleep(0.1)

    def ocr_request(self, label, engine, case=None, control=None):
        request = {"engine": engine, "case": case, "control": control}
        path = core.RUN / "requests" / (label + ".json")
        core.write_json(path, request)
        evidence = self.runner.run(
            [
                str(core.PYTHON),
                "-I",
                "-S",
                "-B",
                str(core.SPIKES / "combined_trial.py"),
                "worker",
                str(path),
            ],
            label,
            seconds=1 if control == "deadline" else 30,
            timeout_expected=control == "deadline",
            memory=64 * 1024**2 if control == "memory" else 1536 * 1024**2,
        )
        payload = (
            None
            if control == "deadline"
            else json.loads((core.RUN / "raw" / (label + ".json")).read_bytes())
        )
        if control:
            self.ocr.validate_control(control, payload, evidence["timed_out"])
            return {"engine": engine, "control": control, "checked": True}
        return {
            "engine": engine,
            "case": case,
            "interval": (payload["worker_started"], payload["worker_ended"]),
            "seconds": evidence["seconds"],
            "cer": payload["cer"],
            "wer": payload["wer"],
            "facts_exact": payload["facts_exact"],
            "quality_gate_pass": payload["cer"] <= 0.05
            and payload["wer"] <= 0.10
            and payload["facts_exact"],
        }

    def close(self):
        from chat_trial import settle_owned

        self.stop.set()
        if self.thread:
            self.thread.join(timeout=5)
        if self.server:
            self.native.kernel.TerminateJobObject(self.server.handle, 0)
        settled = settle_owned(self.process)
        if self.process is None:
            settled["process_reaped"] = True
        for thread in self.inference_threads:
            thread.join(timeout=5)
        if self.root_job:
            self.ledger.observe_native(
                self.native.accounting(self.root_job)["total"] - 1
            )
        active = (
            self.native.accounting(self.root_job)["active"] - 1 if self.root_job else 0
        )
        settled["active_owned_children"] = active
        settled["teardown_verified"] = core.teardown_ok(
            active,
            settled["process_reaped"],
            settled["port_released"],
            bool(self.thread and self.thread.is_alive())
            or any(thread.is_alive() for thread in self.inference_threads),
        )
        if hasattr(self, "log"):
            self.log.close()
        if self.server:
            self.native.kernel.CloseHandle(self.server.handle)
        return settled


def worker(path: Path):
    """One direct worker, immutable approved case/control, raw output only on disk."""
    import ocr_trial as ocr
    from appcontainer_preflight import contained

    path = contained(core.RUN / "requests", path)
    request = json.loads(path.read_bytes())
    if request["engine"] not in {"tesserocr", "rapidocr"}:
        raise RuntimeError("Unapproved OCR engine")
    ocr.ensure_disconnected()
    output = core.RUN / "raw" / (path.stem + ".json")
    control = request["control"]
    if control == "deadline":
        time.sleep(60)
        raise RuntimeError("Deadline sentinel escaped supervisor")
    if control == "memory":
        try:
            bytearray(80 * 1024**2)
        except MemoryError:
            core.write_json(output, {"status": "memory_refused"})
            return
        raise RuntimeError("Memory sentinel escaped Job limit")
    if control is not None or request["case"] not in {"M02", "M03", "M04"}:
        raise RuntimeError("Unapproved OCR case/control")
    ocr.enable_local_packages()
    case = next(c for c in ocr.case_definitions() if c["id"] == request["case"])
    started = time.monotonic()
    result = ocr.evaluate(
        case,
        lambda: ocr.backend_result(
            request["engine"],
            core.PRIOR / "fixtures" / (case["id"] + ".png"),
            ocr.CACHES[1],
        ),
    )
    result["cer"], result["wer"] = ocr.error_rates(case["gold"], result["text"])
    result["facts_exact"] = all(
        value in result["text"]
        for value in ("100", "160", "125.00")
        if value in case["gold"]
    )
    result.update(worker_started=started, worker_ended=time.monotonic())
    core.write_json(output, result)


def run_pair(supervisor, api, item, case):
    """Retain a failed scored attempt and actual header-to-completion overlap."""
    import chat_trial as chat

    event, interval, answer = threading.Event(), [], {}

    class Adapter:
        budget = CallBudget(supervisor.ledger)
        client = StreamClient(api.client, event, interval)

    def request():
        try:
            result = chat.chat_request(
                Adapter(),
                chat.request_body(item["model"], case),
                on_timeout=lambda: supervisor.fail("Chat hard deadline"),
            )
            parsed = json.loads(result["text"])
            chat.validate_answer(
                parsed, {p["id"]: p["columns"] for p in case["evidence"]}
            )
            answer.update(result=result, parsed=parsed, schema_scope_valid=True)
        except Exception as error:  # noqa: BLE001 - retain failed request/partial output locally.
            answer.update(
                error_type=type(error).__name__, partial=getattr(error, "partial", None)
            )

    thread = threading.Thread(target=request, daemon=True)
    supervisor.inference_threads.append(thread)
    thread.start()
    ocr_result = None
    loaded = None
    try:
        if item["engine"]:
            while not event.wait(0.05) and thread.is_alive():
                supervisor.check_failure()
            if not thread.is_alive() or not interval:
                raise RuntimeError(
                    "Chat finished/failed before overlapping OCR could start"
                )
            loaded = api.request("GET", "/api/ps")
            core.validate_residency(loaded, [core.EMBED, item["model"]])
            if not thread.is_alive():
                raise RuntimeError(
                    "Chat ended during residency check; no actual overlap"
                )
            ocr_result = supervisor.ocr_request(
                item["id"], item["engine"], item["ocr_case"]
            )
        while thread.is_alive():
            supervisor.check_failure()
            thread.join(0.1)
        if not answer.get("schema_scope_valid"):
            raise RuntimeError("Incomplete/schema-invalid chat attempt")
        if not item["engine"]:
            loaded = api.request("GET", "/api/ps")
            core.validate_residency(loaded, [core.EMBED, item["model"]])
        seconds = (
            core.overlap(tuple(interval), tuple(ocr_result["interval"]))
            if ocr_result
            else None
        )
        if ocr_result and (seconds <= 0 or not ocr_result["quality_gate_pass"]):
            raise RuntimeError("OCR quality/actual overlap incomplete")
        return {
            **item,
            "schema_scope_valid": True,
            "elapsed_s": answer["result"]["elapsed_s"],
            "first_answer_s": answer["result"]["first_answer_s"],
            "overlap_s": seconds,
            "ocr": ocr_result,
            "loaded_models": loaded,
            "residency_timing": "before OCR while streaming"
            if item["engine"]
            else "after baseline",
        }
    finally:
        if thread.is_alive():
            supervisor.fail("Pair interrupted; cancel owned inference")
            thread.join(timeout=5)
        core.write_json(
            core.RUN / "answers" / (item["id"] + ".json"),
            {
                "schedule": item,
                "case": case,
                "answer": answer,
                "ocr": ocr_result,
                "chat_interval": interval,
                "thread_alive": thread.is_alive(),
            },
        )
        if thread.is_alive():
            raise RuntimeError("Unreaped inference thread; remain disconnected")


def local_review():
    """Script-free escaped review; no raw content is printed or sent to tools."""
    text = (
        "<!doctype html><meta charset='utf-8'><meta http-equiv='Content-Security-Policy' "
        "content=\"default-src 'none'; style-src 'unsafe-inline'\"><title>T11 local review</title>"
        "<h1>Combined trial local review</h1><p>Check facts, refusal and every citation. "
        "Schema/scope checks are not semantic accuracy.</p>"
    )
    for path in sorted((core.RUN / "answers").glob("S*.json")):
        text += (
            "<h2>"
            + html.escape(path.stem)
            + "</h2><pre>"
            + html.escape(path.read_text(encoding="utf-8"))
            + "</pre>"
        )
    (core.RUN / "review.html").write_text(text, encoding="utf-8")


def offline_main():
    """User-operated disconnected epoch, never retries or resets a consumed ledger."""
    import ocr_trial as ocr

    ledger = core.Ledger(core.RUN / "meter.json")
    if ledger.read()["offline_started"] or not ledger.read()["execution_approved"]:
        raise RuntimeError(
            "This handoff is already started or unapproved; do not rerun"
        )
    print(
        "Synthetic-only combined trial has NO filesystem confinement. Disconnect every external link."
    )
    if input("Keep disconnected through teardown. Type OFFLINE: ") != "OFFLINE":
        raise RuntimeError("No disconnection attestation")
    ocr.ensure_disconnected()
    ledger.reserve("controller", 2, "User PowerShell/direct Python handoff")
    ledger.start()
    summary = {
        "status": "running",
        "phase": "sealed-readiness",
        "controls": [],
        "responses": [],
        "teardown_verified": False,
    }
    supervisor, api = None, None
    for name in ("requests", "receipts", "raw", "answers", "temp"):
        (core.RUN / name).mkdir(exist_ok=False)
    try:
        core.verify_seal()
        ocr.enable_local_packages()
        import chat_trial as chat

        if not chat.port_not_listening():
            raise RuntimeError("Existing service owns port; do not attach")
        summary["phase"] = "owned-supervisor-setup"
        # Retain partially initialized ownership state so setup failures can be cleaned up.
        supervisor = Supervisor.__new__(Supervisor)
        supervisor.__init__(ledger)
        supervisor.sample()
        supervisor.launch()
        api = API(supervisor)
        if api.request("GET", "/api/version").get("version") != "0.40.16":
            raise RuntimeError("Runtime version drift")
        tags = {
            m["name"]: m["digest"].removeprefix("sha256:")
            for m in api.request("GET", "/api/tags")["models"]
        }
        if any(tags.get(name) != sha for name, sha in core.MODELS.items()):
            raise RuntimeError("Runtime model manifest identity drift")
        for name in core.MODELS:
            metadata = api.request("POST", "/api/show", {"model": name})
            core.write_json(
                core.RUN / (name.split(":")[0] + "-metadata.json"), metadata
            )
        for engine in ("tesserocr", "rapidocr"):
            for control in ("deadline", "memory"):
                summary["phase"] = "sentinel-" + engine + "-" + control
                summary["controls"].append(
                    supervisor.ocr_request(
                        "control-" + engine + "-" + control, engine, control=control
                    )
                )
                core.write_json(core.RUN / "summary.json", summary)
        inputs = json.loads((core.RUN / "inputs.json").read_bytes())
        passages = inputs["corpus"]["passages"]
        summary["embedding_attempts"] = 0
        summary["phase"] = "frozen-corpus-embeddings"
        for index in range(0, 32, 4):
            summary["embedding_attempts"] += 1
            api.embed([p["text"] for p in passages[index : index + 4]])
        core.validate_residency(api.request("GET", "/api/ps"), [core.EMBED])
        cases = {c["id"]: c for c in inputs["cases"]}
        current_model = None
        print(
            "TESTING IN PROGRESS. Stay disconnected until TEARDOWN VERIFIED: True.",
            flush=True,
        )
        for item in core.schedule():
            if current_model and current_model != item["model"]:
                api.request(
                    "POST", "/api/generate", {"model": current_model, "keep_alive": 0}
                )
            current_model = item["model"]
            summary["phase"] = item["id"] + "-query-and-chat"
            case = cases[item["case"]]
            record = {**item, "status": "attempt_started"}
            summary["responses"].append(record)
            core.write_json(core.RUN / "summary.json", summary)
            summary["embedding_attempts"] += 1
            api.embed([case["question"]], query=True)
            record.update(run_pair(supervisor, api, item, case), status="completed")
            core.write_json(core.RUN / "summary.json", summary)
        summary["phase"] = "model-unload"
        api.request("POST", "/api/generate", {"model": current_model, "keep_alive": 0})
        api.request("POST", "/api/generate", {"model": core.EMBED, "keep_alive": 0})
        summary["status"] = "completed_pending_local_semantic_review_no_adoption"
    except BaseException as error:  # noqa: BLE001 - final ownership boundary also handles Ctrl+C.
        summary.update(
            status="stopped_no_automatic_retry", error_type=type(error).__name__
        )
        if type(error) is RuntimeError:
            summary["stop_reason"] = str(error)[:240]
        if field := core.state_error_field(error):
            summary["missing_state_field"] = field
        if isinstance(error, OSError):
            summary["filesystem_failure"] = core.record_filesystem_error(
                error, core.RUN
            )
        if supervisor:
            supervisor.fail("Controlled execution stopped")
    finally:
        try:
            if supervisor:
                summary["supervisor_failure"] = supervisor.failure
                if failure := getattr(supervisor, "filesystem_failure", None):
                    summary.setdefault("filesystem_failure", failure)
                settled = supervisor.close()
                summary.update(settled)
                core.write_json(
                    core.RUN / "memory-observations.json", supervisor.samples
                )
            else:
                # No supervisor means ownership setup may have failed partway: fail closed.
                summary["teardown_verified"] = False
            if api:
                api.client.close()
            local_review()
        except BaseException as error:  # noqa: BLE001 - cleanup must never claim false success.
            summary.update(
                teardown_verified=False, cleanup_error_type=type(error).__name__
            )
        core.write_json(core.RUN / "summary.json", summary)
        print("STATUS:", summary["status"])
        print("TEARDOWN VERIFIED:", summary["teardown_verified"])
        print("Local sanitized report:", core.RUN / "summary.json")
        if summary["teardown_verified"]:
            print("Owned workers/server stopped. You may reconnect and report status.")
        else:
            print(
                "REMAIN DISCONNECTED: verify/stop only owned trial processes before reconnecting."
            )
