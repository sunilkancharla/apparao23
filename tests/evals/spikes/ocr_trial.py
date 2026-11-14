"""Manual disconnected synthetic OCR evaluation; imports native packages lazily.

Connected preparation and routine tests use only the standard library. Raw OCR
outputs remain in ignored local files; public receipts contain counts/status only.
"""

from __future__ import annotations

import ctypes
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import tomllib
from ctypes import wintypes as w
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
RUN = ROOT / "data/t09-manual-ocr/manual-01"
SITE = ROOT / ".venv/Lib/site-packages"
INVENTORY = ROOT / "docs/proposals/ocr-trial-artifacts.json"
INVENTORY_HASH = "9fb3c5225cb7f75052417cc6e582b96cf77867ba7d8b9b5bb0a2fa4c65fdb909"
CACHES = [ROOT / ".venv/.cache/ocr-review" / name for name in ("part-a-01", "part-a-02")]
CONTROLS = ("missing", "wrong", "truncated", "empty", "unreadable", "pixels",
            "deadline", "memory", "backend", "remote")


def configure_run(run_id: str) -> None:
    """Choose only reviewed run IDs; never reset a stopped run's ledger/seal."""
    global RUN
    if run_id not in {"manual-01", "manual-02", "manual-03", "manual-04"}:
        raise ValueError("Unreviewed manual run ID")
    RUN = ROOT / "data/t09-manual-ocr" / run_id


def canonical_name(name: str) -> str:
    """Compare equivalent distribution spellings without relaxing version pins."""
    return re.sub(r"[-_.]+", "-", name).lower()


def case_definitions() -> list[dict]:
    """Authored English gold and stable source locations; no user-document inputs."""
    text = ["Project Cedar budget: 24000 units.", "Revenue 2024 100\nRevenue 2025 160",
            "Invoice total: 125.00", "Office records remain on this computer.",
            "Project Cedar budget: 24000 units.", "Invoice total: 125.00",
            "Revenue 2024 100\nRevenue 2025 160"]
    cases = []
    for index, gold in enumerate(text):
        group = "native" if index < 2 else "scan" if index < 4 else "mixed"
        page = index + 1 if index < 2 else index - 1 if index < 4 else index - 3
        cases.append({"id": f"M{index + 1:02}", "pdf": group + ".pdf", "page": page,
                      "gold": gold, "source_method": "ocr" if index in (2, 3, 5) else "native",
                      "transform": {"dpi": 300, "rotation": 0}})
    for number, source, transform in ((8, 2, {"rotation": 90}),
                                      (9, 2, {"contrast": 0.20}),
                                      (10, 1, {"crop": [100, 100, 2300, 900]})):
        cases.append(cases[source] | {"id": f"M{number:02}",
                     "derived_from": cases[source]["id"],
                     "transform": cases[source]["transform"] | transform})
    return cases


def comparison_schedule() -> list[tuple[str, str, int]]:
    """Exactly sixty fresh OCR workers across the fixed cases and repetitions."""
    return [(engine, case["id"], repeat) for engine in ("tesserocr", "rapidocr")
            for case in case_definitions() for repeat in range(3)]


def control_schedule() -> list[tuple[str, str]]:
    """Twenty fixed negative controls, charged in the same execution ledger."""
    return [(engine, control) for engine in ("tesserocr", "rapidocr") for control in CONTROLS]


def input_path(root: Path, name: str) -> Path:
    """Reject URLs, escapes, symlinks/junctions and unapproved input formats."""
    from appcontainer_preflight import contained

    if "://" in name or Path(name).suffix.lower() not in {".png", ".pdf"}:
        raise ValueError("Only local synthetic PNG/PDF inputs")
    return contained(root, root / name)


def validate_pixels(width: int, height: int) -> None:
    """Reject invalid/over-budget dimensions before raster expansion."""
    if width < 1 or height < 1 or width * height > 12_000_000:
        raise ValueError("Pixel limit")


def charge(path: Path, purpose: str, slots: int, *, closeout: bool = False) -> None:
    """Append a shared reservation before any process, retaining cleanup capacity."""
    meter = json.loads(path.read_text(encoding="utf-8-sig"))
    if slots < 1 or meter["reserved"] + slots > meter["limit"] - (0 if closeout else 16):
        raise RuntimeError("Shared trial process limit/cleanup reserve")
    deadline = meter.get("execution_deadline_utc")
    if deadline and not closeout and datetime.now(UTC) > datetime.fromisoformat(deadline):
        raise RuntimeError("Execution time limit")
    event = {"slots": slots, "purpose": purpose, "at": datetime.now(UTC).isoformat()}
    meter["reserved"] += slots
    meter["events"].append(event)
    path.write_text(json.dumps(meter, indent=2), encoding="utf-8")
    with path.with_name("events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event) + "\n")


def verify_blob(content: bytes, size: int, digest: str) -> None:
    """Hash mismatch stops before any package/backend use."""
    if len(content) != size or hashlib.sha256(content).hexdigest() != digest:
        raise RuntimeError("Artifact identity mismatch")


def edit_distance(left, right) -> int:
    """Compute Levenshtein distance for bounded authored character/word gold."""
    previous = list(range(len(right) + 1))
    for index, a in enumerate(left, 1):
        current = [index]
        for offset, b in enumerate(right, 1):
            current.append(min(current[-1] + 1, previous[offset] + 1,
                               previous[offset - 1] + (a != b)))
        previous = current
    return previous[-1]


def error_rates(gold: str, recognized: str) -> tuple[float, float]:
    """Whitespace-only normalization preserves digits, case and punctuation."""
    gold, recognized = " ".join(gold.split()), " ".join(recognized.split())
    return (edit_distance(gold, recognized) / max(1, len(gold)),
            edit_distance(gold.split(), recognized.split()) / max(1, len(gold.split())))


def evaluate(case: dict, backend) -> dict:
    """Attach real source provenance to one backend result without inventing boxes."""
    output = backend()
    warnings = list(output.get("warnings", []))
    if not output.get("text", "").strip():
        warnings.append("no_recognized_text")
    return output | {"case_id": case["id"], "pdf": case["pdf"], "page": case["page"],
                     "method": "ocr", "source_method": case["source_method"],
                     "transform": case["transform"], "warnings": warnings}


def route_pages(pages: list[tuple[str, str]], ocr) -> list[dict]:
    """Native text routing preserves order and avoids duplicate OCR passages."""
    return [{"page": index, "method": method, "text": text if method == "native" else ocr(index)}
            for index, (method, text) in enumerate(pages, 1)]


def rapid_settings(assets: Path, enums) -> dict:
    """Use RapidOCR's enum types, injected to keep connected tests native-free."""
    return {"Global.use_cls": False, "Global.return_word_box": True,
            "Global.text_score": 0.5, "Global.max_side_len": 2000,
            "Det.model_path": str(assets / "en_PP-OCRv3_det_mobile.onnx"),
            "Rec.model_path": str(assets / "en_PP-OCRv4_rec_mobile.onnx"),
            "Det.lang_type": enums.LangDet.EN, "Rec.lang_type": enums.LangRec.EN,
            "Det.ocr_version": enums.OCRVersion.PPOCRV4,
            "Rec.ocr_version": enums.OCRVersion.PPOCRV4,
            "Det.model_type": enums.ModelType.MOBILE,
            "Rec.model_type": enums.ModelType.MOBILE,
            "Det.engine_type": enums.EngineType.ONNXRUNTIME,
            "Rec.engine_type": enums.EngineType.ONNXRUNTIME,
            "Det.limit_side_len": 2000, "Det.limit_type": "max",
            "EngineConfig.onnxruntime.intra_op_num_threads": 1,
            "EngineConfig.onnxruntime.inter_op_num_threads": 1,
            "EngineConfig.onnxruntime.use_cuda": False,
            "EngineConfig.onnxruntime.use_dml": False,
            "EngineConfig.onnxruntime.use_cann": False,
            "EngineConfig.onnxruntime.use_coreml": False}


def write_json(path: Path, value: object) -> None:
    """Persist local receipts; raw OCR files are never printed to tool output."""
    path.write_text(json.dumps(value, indent=2), encoding="utf-8")


def validate_control(control: str, payload: dict | None, timed_out: bool) -> None:
    """A zero exit alone cannot make a negative control pass."""
    expected = {"memory": "memory_refused", "truncated": "decode_refused",
                "empty": "decode_refused", "unreadable": "qualified"}
    if control == "deadline":
        if not timed_out:
            raise RuntimeError("Deadline control did not reach owned watchdog")
    elif timed_out or not payload or payload.get("status") != expected.get(control, "refused"):
        raise RuntimeError("Negative control result not supported")


def verify_artifacts() -> dict:
    """Locate only pinned cached bytes and baseline metadata without importing code."""
    from importlib.metadata import distributions

    verify_blob(INVENTORY.read_bytes(), INVENTORY.stat().st_size, INVENTORY_HASH)
    inventory = json.loads(INVENTORY.read_bytes())
    selected = {}
    for item in inventory["new_wheels"] + inventory["language_and_model_assets"]:
        found = [directory / item["filename"] for directory in CACHES
                 if (directory / item["filename"]).is_file()]
        if len(found) != 1:
            raise RuntimeError("Missing/ambiguous cached artifact: " + item["filename"])
        digest = item.get("sha256") or item["recorded_verified_sha256"]
        verify_blob(found[0].read_bytes(), item["bytes"], digest)
        selected[item["filename"]] = str(found[0])
    baseline = {canonical_name(dist.metadata["Name"]): dist.version
                for dist in distributions(path=[str(SITE)])}
    for name, version in inventory["reused_versions"].items():
        if baseline.get(canonical_name(name)) != version:
            raise RuntimeError("Reused distribution mismatch: " + name)
    companion = ROOT / "data/t09-artifacts/part-a-02/flatbuffers-LICENSE.upstream.txt"
    verify_blob(companion.read_bytes(), 11358,
                "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30")
    return {"inventory_sha256": INVENTORY_HASH, "artifacts": selected,
            "flatbuffers_companion": str(companion),
            "baseline": baseline, "pyproject_sha256": hashlib.sha256(
                (ROOT / "pyproject.toml").read_bytes()).hexdigest(),
            "lock_sha256": hashlib.sha256((ROOT / "uv.lock").read_bytes()).hexdigest()}


def active_external_adapters() -> list[dict]:
    """Observe local adapter/gateway state without sending a packet or DNS query."""
    class Adapter(ctypes.Structure):
        pass

    pointer = ctypes.POINTER(Adapter)
    Adapter._fields_ = [("length", w.ULONG), ("index", w.DWORD), ("next", pointer),
        ("name", ctypes.c_void_p)] + [(name, ctypes.c_void_p) for name in
        ("unicast", "anycast", "multicast", "dns", "suffix", "description", "friendly")] + [
        ("physical", ctypes.c_ubyte * 8), ("physical_length", w.DWORD),
        ("flags", w.DWORD), ("mtu", w.DWORD), ("kind", w.DWORD), ("status", w.DWORD),
        ("ipv6index", w.DWORD), ("zones", w.DWORD * 16), ("prefix", ctypes.c_void_p),
        ("tx", ctypes.c_uint64), ("rx", ctypes.c_uint64), ("wins", ctypes.c_void_p),
        ("gateway", ctypes.c_void_p)]
    api = ctypes.WinDLL("iphlpapi", use_last_error=True).GetAdaptersAddresses
    api.argtypes = [w.ULONG, w.ULONG, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(w.ULONG)]
    api.restype = w.ULONG
    size = w.ULONG(65536)
    buffer = ctypes.create_string_buffer(size.value)
    error = api(0, 0x80, None, buffer, ctypes.byref(size))
    if error:
        raise RuntimeError(f"Local adapter metadata unavailable ({error}); stop")
    result, visited = [], set()
    current = ctypes.cast(buffer, pointer)
    while current:
        address = ctypes.addressof(current.contents)
        if address in visited or len(visited) > 256:
            raise RuntimeError("Invalid adapter metadata list")
        visited.add(address)
        item = current.contents
        if item.length < ctypes.sizeof(Adapter):
            raise RuntimeError("Adapter layout too short")
        if item.status == 1 and item.kind != 24:
            result.append({"index": item.index, "type": item.kind,
                           "gateway": bool(item.gateway)})
        current = item.next
    return result


def ensure_disconnected() -> None:
    """User attestation is primary; an active gateway fails the local metadata check."""
    adapters = active_external_adapters()
    if any(item["gateway"] for item in adapters):
        raise RuntimeError("An active non-loopback gateway remains; stay disconnected and stop")


def process_memory(handle) -> dict:
    """Return native working-set peak and observed current private commit."""
    class Counters(ctypes.Structure):
        _fields_ = [("size", w.DWORD), ("faults", w.DWORD)] + [
            (name, ctypes.c_size_t) for name in ("peak_working", "working", "peak_paged",
             "paged", "peak_nonpaged", "nonpaged", "pagefile", "peak_pagefile", "private")]

    values = Counters()
    values.size = ctypes.sizeof(values)
    api = ctypes.WinDLL("psapi", use_last_error=True).GetProcessMemoryInfo
    api.argtypes = [w.HANDLE, ctypes.c_void_p, w.DWORD]
    api.restype = w.BOOL
    if not api(handle, ctypes.byref(values), ctypes.sizeof(values)):
        raise ctypes.WinError(ctypes.get_last_error())
    return {"private_observed": values.private, "working_peak": values.peak_working}


class OwnedRunner:
    """Own one bounded Job per subprocess; no no-window flag or shell commands."""

    def read_global_meter(self) -> dict:
        """Read the legacy meter; combined callers override only this short read."""
        return json.loads((RUN / "meter.json").read_text(encoding="utf-8-sig"))

    def __init__(self, controller_job=None):
        from appcontainer_preflight import Native

        self.native = Native()
        self.children = []
        self.controller_job = controller_job
        from appcontainer_preflight import bounded_tree_bytes

        self.disk_baseline = {str(path): bounded_tree_bytes(path, 100 * 1024**3)
                              for path in (SITE, ROOT / ".venv/.cache/uv")}

    def run(self, arguments: list[str], label: str, *, slots: int = 1,
            memory: int = 1536 * 1024**2, seconds: int = 30,
            processes: int = 1, timeout_expected: bool = False) -> dict:
        from appcontainer_preflight import ExtendedLimits, ProcessInfo, StartupEx

        ensure_disconnected()
        self.check_storage(full=True)
        charge(RUN / "meter.json", label, slots)
        native = self.native
        job = native.job(processes)
        limits = ExtendedLimits()
        limits.basic.flags = 0x8 | 0x100 | 0x2000
        limits.basic.active = processes
        limits.process_memory = memory
        native.check(native.kernel.SetInformationJobObject(job, 9, ctypes.byref(limits),
                                                         ctypes.sizeof(limits)))
        startup, process = StartupEx(), ProcessInfo()
        startup.startup.cb = ctypes.sizeof(StartupEx)
        attribute_size = ctypes.c_size_t()
        native.kernel.InitializeProcThreadAttributeList(None, 1, 0, ctypes.byref(attribute_size))
        attributes = ctypes.create_string_buffer(attribute_size.value)
        native.check(native.kernel.InitializeProcThreadAttributeList(
            attributes, 1, 0, ctypes.byref(attribute_size)))
        startup.attributes = ctypes.cast(attributes, ctypes.c_void_p)
        # OMP/BLAS threads must also remain CPU-only and bounded.
        env = {"SystemRoot": os.environ["SystemRoot"], "WINDIR": os.environ["SystemRoot"],
               "TEMP": str(RUN / "temp"), "TMP": str(RUN / "temp"),
               "OMP_THREAD_LIMIT": "1", "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1",
               "UV_CACHE_DIR": str(ROOT / ".venv/.cache/uv"), "UV_OFFLINE": "1",
               "UV_PYTHON_DOWNLOADS": "never", "UV_PROJECT_ENVIRONMENT": str(ROOT / ".venv")}
        block = ctypes.create_unicode_buffer("\0".join(
            f"{key}={value}" for key, value in sorted(env.items())) + "\0\0")
        started, timed_out = time.monotonic(), False
        peak_private = 0
        before = native.accounting(self.controller_job) if self.controller_job else None
        try:
            native.check(native.kernel.CreateProcessW(
                arguments[0], ctypes.create_unicode_buffer(subprocess.list2cmdline(arguments)),
                None, None, False, 0x80404, block, str(ROOT), ctypes.byref(startup), ctypes.byref(process)))
            self.children.append(process.pid)
            native.check(native.kernel.AssignProcessToJobObject(job, process.process))
            inside = w.BOOL()
            native.check(native.kernel.IsProcessInJob(process.process, job, ctypes.byref(inside)))
            if not inside.value or native.accounting(job)["total"] != 1:
                raise RuntimeError("Worker Job assignment/accounting failed")
            usage = process_memory(process.process)
            if native.kernel.ResumeThread(process.thread) == 0xFFFFFFFF:
                raise ctypes.WinError(ctypes.get_last_error())
            while True:
                wait = native.kernel.WaitForSingleObject(process.process, 100)
                if wait == 0:
                    break
                if wait != 258:
                    raise RuntimeError("Worker wait failed")
                try:
                    usage = process_memory(process.process)
                except OSError:
                    if native.kernel.WaitForSingleObject(process.process, 0) == 0:
                        break
                    raise
                peak_private = max(peak_private, usage["private_observed"])
                if process_memory(native.kernel.GetCurrentProcess())["private_observed"] > 512 * 1024**2:
                    raise RuntimeError("Controller private-commit stop limit")
                ensure_disconnected()
                self.check_storage()
                global_meter = self.read_global_meter()
                if datetime.now(UTC) > datetime.fromisoformat(global_meter["execution_deadline_utc"]):
                    raise RuntimeError("Shared offline execution/provisioning deadline")
                if time.monotonic() - started >= seconds:
                    timed_out = True
                    native.check(native.kernel.TerminateJobObject(job, 124))
                    if native.kernel.WaitForSingleObject(process.process, 5000) != 0:
                        raise RuntimeError("Timed-out worker did not stop")
                    break
            code = w.DWORD()
            native.check(native.kernel.GetExitCodeProcess(process.process, ctypes.byref(code)))
            accounting = native.accounting(job)
            evidence = {"label": label, "pid": process.pid, "exit_code": code.value,
                        "timed_out": timed_out, "seconds": time.monotonic() - started,
                        "accounting": accounting, "process_private_commit_cap": memory,
                        "private_commit_observed_peak": peak_private,
                        "working_set_peak_observed": usage["working_peak"]}
            if before is not None:
                evidence["controller_before"] = before
                evidence["controller_after"] = native.accounting(self.controller_job)
            write_json(RUN / "receipts" / (label + ".json"), evidence)
            if (accounting["total"] > slots or accounting["active"] != 0
                    or (processes == 1 and accounting["total"] != 1)):
                raise RuntimeError("Unexpected descendants/unfinished Job")
            if before is not None and (
                evidence["controller_after"]["total"] != before["total"] + accounting["total"]
                or evidence["controller_after"]["active"] != 1
            ):
                raise RuntimeError("Controller descendant accounting mismatch")
            if timed_out != timeout_expected or (code.value and not timeout_expected):
                raise RuntimeError(f"{label} stopped: exit {code.value}; inspect local receipt")
            self.check_storage(full=True)
            return evidence
        finally:
            if process.process:
                native.kernel.TerminateJobObject(job, 125)
                if native.kernel.WaitForSingleObject(process.process, 5000) != 0:
                    raise RuntimeError("Worker cleanup uncertain: remain disconnected")
            for handle in (process.thread, process.process, job):
                if handle:
                    native.kernel.CloseHandle(handle)
            native.kernel.DeleteProcThreadAttributeList(attributes)
            if process.pid in self.children:
                self.children.remove(process.pid)

    def check_storage(self, *, full: bool = False) -> None:
        from appcontainer_preflight import bounded_tree_bytes, memory_ready

        memory_ready()
        bounded_tree_bytes(RUN, 1024**3)
        bounded_tree_bytes(RUN / "raw", 128 * 1024**2)
        if full:
            increase = sum(max(0, bounded_tree_bytes(Path(path), 100 * 1024**3) - before)
                           for path, before in self.disk_baseline.items())
            if increase + bounded_tree_bytes(RUN, 1024**3) > 1024**3:
                raise RuntimeError("Combined new install/cache/fixture disk cap")


def offline_project(inventory: dict, baseline: dict) -> str:
    """Prepare a pinned evaluation group without replacing existing project settings."""
    original = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    if RUN.name in {"manual-03", "manual-04"}:
        # Reuse the completed offline installation, never append a second group.
        previous = ROOT / "data/t09-manual-ocr/manual-02"
        proposed = previous / "proposed-pyproject.toml"
        prior_seal = json.loads((previous / "seal.json").read_bytes())
        verify_blob(proposed.read_bytes(), proposed.stat().st_size,
                    prior_seal[str(proposed.relative_to(ROOT))])
        expected = json.loads((previous / "prepared-state.json").read_bytes())["baseline"]
        expected |= {canonical_name(item["name"]): item["version"]
                     for item in inventory["new_wheels"]}
        if baseline != expected or original != proposed.read_text(encoding="utf-8"):
            raise RuntimeError("Previously reviewed OCR project/installed versions changed")
        return original
    if "ocr-eval" in original or "constraint-dependencies" in original:
        raise RuntimeError("Unexpected existing OCR group/constraints; review before editing")
    marker = "sys_platform == 'win32' and platform_machine == 'AMD64' and python_version == '3.14'"
    group = "\nocr-eval = [\n" + "".join(
        '    ' + json.dumps(f"{item['name']}=={item['version']}; {marker}") + ",\n"
        for item in inventory["new_wheels"]) + "]\n\n"
    constraints = [f"{name}=={version}" for name, version in baseline.items()
                   if name != "document-assistant"]
    return original.replace("[tool.uv]", group + "[tool.uv]", 1) + (
        "\nconstraint-dependencies = " + json.dumps(constraints) + "\n")


def prepare() -> None:
    """Connected preparation: static hashes/config only, no native package imports."""
    state = verify_artifacts()
    import zipfile

    for name, path in state["artifacts"].items():
        if name.endswith(".whl"):
            with zipfile.ZipFile(path) as archive:
                if any(member.lower().endswith(".pth") for member in archive.namelist()):
                    raise RuntimeError("Unreviewed startup .pth entry; no handoff")
    inventory = json.loads(INVENTORY.read_bytes())
    write_json(RUN / "prepared-state.json", state)
    (RUN / "proposed-pyproject.toml").write_text(offline_project(inventory, state["baseline"]),
                                               encoding="utf-8")
    launcher = Path(__file__).with_name("run_manual_ocr.ps1")
    launcher_text = launcher.read_text(encoding="utf-8").replace(
        "[string]$RunId = 'manual-01'", f"[string]$RunId = '{RUN.name}'")
    (RUN / "run.ps1").write_text(launcher_text, encoding="utf-8")
    files = [Path(__file__), Path(__file__).with_name("ocr_trial_fixtures.py"),
             Path(__file__).with_name("appcontainer_preflight.py"), launcher,
             RUN / "run.ps1", RUN / "proposed-pyproject.toml", RUN / "prepared-state.json",
             ROOT / "pyproject.toml", ROOT / "uv.lock", ROOT / ".venv/pyvenv.cfg", INVENTORY]
    seal = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in files}
    for path in (Path("F:/Python/Python314/python.exe"), Path("F:/Python/Python314/python314.dll")):
        seal[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    write_json(RUN / "seal.json", seal)
    print("Artifact/config preparation complete; no installation or native import.")


def enable_local_packages() -> None:
    """Offline workers use only the project site directory; no .pth execution."""
    sys.path.insert(0, str(SITE))


def backend_result(engine: str, image: Path, assets: Path) -> dict:
    """Actual OCR is reachable only in the user-run disconnected worker."""
    from PIL import Image

    decoding = time.monotonic()
    with Image.open(image) as opened:
        validate_pixels(opened.width, opened.height)
        raster = opened.convert("RGB")
    decode_seconds = time.monotonic() - decoding
    started = time.monotonic()
    if engine == "tesserocr":
        import tesserocr

        version = tesserocr.tesseract_version()
        if "5.5.4" not in version or "1.87.0" not in version:
            raise RuntimeError("Bundled Tesseract/Leptonica version mismatch")
        with tesserocr.PyTessBaseAPI(path=str(assets), lang="eng", oem=tesserocr.OEM.LSTM_ONLY,
                                   psm=tesserocr.PSM.AUTO) as api:
            initialized = time.monotonic()
            api.SetImage(raster)
            api.SetSourceResolution(300)
            text = api.GetUTF8Text()
            boxes = api.GetComponentImages(tesserocr.RIL.TEXTLINE, True)
            locations = [item[1] for item in boxes]
            confidence = api.MeanTextConf()
        return {"text": text, "boxes": locations, "confidence": confidence,
                "version": version, "seconds": time.monotonic() - started,
                "decode_seconds": decode_seconds, "initialization_seconds": initialized - started,
                "ocr_seconds": time.monotonic() - initialized, "warnings": []}
    import numpy as np
    from rapidocr import RapidOCR
    from rapidocr.utils import typings
    from rapidocr.utils.download_file import DownloadFile

    def refuse_download(*_args, **_kwargs):
        raise RuntimeError("Unapproved asset download attempt; stop offline trial")

    DownloadFile.run = staticmethod(refuse_download)

    settings = rapid_settings(assets, typings)
    ocr = RapidOCR(params=settings)
    initialized = time.monotonic()
    # Visualization/font APIs are intentionally never called.
    output = ocr(np.asarray(raster), use_cls=False, return_word_box=True)
    providers = {}
    for label, component in (("det", ocr.text_det), ("rec", ocr.text_rec)):
        if component is None:
            providers[label] = ["not_loaded_on_empty_detection"]
            continue
        providers[label] = component.session.session.get_providers()
        if providers[label] != ["CPUExecutionProvider"]:
            raise RuntimeError("Unexpected ONNX execution provider")
    return {"text": "\n".join(output.txts or ()),
            "boxes": output.boxes.tolist() if output.boxes is not None else [],
            "scores": [float(value) for value in output.scores] if output.scores is not None else [],
            "providers": providers,
            "seconds": time.monotonic() - started, "decode_seconds": decode_seconds,
            "initialization_seconds": initialized - started,
            "ocr_seconds": time.monotonic() - initialized,
            "initialization_note": "Lazy model/session loading is included in OCR time",
            "warnings": []}


def worker(request_path: Path) -> None:
    """Run one immutable request, keeping OCR text exclusively in local raw output."""
    ensure_disconnected()
    request = json.loads(request_path.read_bytes())
    enable_local_packages()
    output = RUN / "raw" / (request_path.stem + ".json")
    if request["kind"] == "fixtures":
        from ocr_trial_fixtures import materialize

        materialize(RUN / "fixtures", case_definitions())
        write_json(output, {"status": "fixtures_ready"})
        return
    assets = CACHES[1]
    if request["kind"] == "control":
        control = request["control"]
        if control == "deadline":
            time.sleep(60)
            raise RuntimeError("Deadline sentinel was not terminated")
        if control == "memory":
            try:
                bytearray(80 * 1024**2)
            except MemoryError:
                write_json(output, {"status": "memory_refused"})
                return
            raise RuntimeError("Safe memory sentinel was not refused")
        if control in {"missing", "wrong", "backend", "remote", "pixels"}:
            try:
                if control == "missing":
                    (RUN / "fixtures/missing-model.onnx").read_bytes()
                elif control == "wrong":
                    verify_blob((RUN / "fixtures/wrong-asset.bin").read_bytes(), 1, "0" * 64)
                elif control == "backend":
                    raise ImportError("Injected unavailable backend sentinel; no DLL removed")
                elif control == "remote":
                    input_path(RUN / "fixtures", "https://example.invalid/page.png")
                else:
                    validate_pixels(12_000_001, 1)
            except (OSError, RuntimeError, ImportError, ValueError):
                write_json(output, {"status": "refused", "control": control})
                return
            raise RuntimeError("Negative control was unexpectedly accepted")
        filename = {"truncated": "truncated.png", "empty": "empty.png",
                    "unreadable": "unreadable.png"}[control]
        try:
            result = backend_result(request["engine"], RUN / "fixtures" / filename, assets)
        except (OSError, ValueError) as error:
            if control == "unreadable":
                raise
            write_json(output, {"status": "decode_refused", "error_type": type(error).__name__})
            return
        if control != "unreadable":
            raise RuntimeError("Corrupt input unexpectedly accepted")
        if result["text"].strip():
            raise RuntimeError("Blank unreadable control produced unsupported text")
        write_json(output, {"status": "qualified", "warnings": ["no_recognized_text"]})
        return
    case = next(item for item in case_definitions() if item["id"] == request["case_id"])
    result = evaluate(case, lambda: backend_result(request["engine"],
                      input_path(RUN / "fixtures", case["id"] + ".png"), assets))
    result["cer"], result["wer"] = error_rates(case["gold"], result["text"])
    write_json(output, result)


def offline_main() -> None:
    """One local entry point; no preparation or execution is repeated implicitly."""
    from appcontainer_preflight import ExtendedLimits, Native, memory_ready

    if RUN.name in {"manual-02", "manual-03", "manual-04"}:
        approved = json.loads((RUN / "meter.json").read_text(encoding="utf-8-sig"))
        if approved.get("execution_approved") is not True:
            raise RuntimeError("Continuation prepared, but execution allocation is not approved")
    if input("All external links disconnected; accept no filesystem confinement? Type OFFLINE: ") != "OFFLINE":
        raise RuntimeError("No disconnection attestation")
    ensure_disconnected()
    seal = json.loads((RUN / "seal.json").read_bytes())
    for relative, digest in seal.items():
        path = ROOT / relative
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError("Handoff source/config changed; stop before installation")
    meter = json.loads((RUN / "meter.json").read_text(encoding="utf-8-sig"))
    if meter.get("offline_started"):
        raise RuntimeError("This ledger has already started offline; no automatic rerun")
    meter["offline_started"] = datetime.now(UTC).isoformat()
    meter["phase"] = "offline-provisioning"
    meter["execution_deadline_utc"] = datetime.fromtimestamp(time.time() + 1200, UTC).isoformat()
    write_json(RUN / "meter.json", meter)
    for directory in ("raw", "receipts", "requests", "temp"):
        (RUN / directory).mkdir(exist_ok=False)
    native = Native()
    controller_job = native.job(8, kill=False)
    # A parent per-process memory limit would also constrain every nested worker.
    # Keep the controller's own private bytes monitored; each child has its own cap.
    limits = ExtendedLimits()
    limits.basic.flags, limits.basic.active = 0x8 | 0x2000, 8
    native.check(native.kernel.SetInformationJobObject(controller_job, 9,
                 ctypes.byref(limits), ctypes.sizeof(limits)))
    native.check(native.kernel.AssignProcessToJobObject(controller_job,
                                                       native.kernel.GetCurrentProcess()))
    runner = OwnedRunner(controller_job)
    result = {"status": "running", "comparisons": [], "controls": [], "teardown_verified": False}
    project_before = (ROOT / "pyproject.toml").read_bytes()
    lock_before = (ROOT / "uv.lock").read_bytes()
    generated_lock = None
    provisioning_complete = False
    try:
        memory_ready()
        state = verify_artifacts()
        prepared = json.loads((RUN / "prepared-state.json").read_bytes())
        if state != prepared:
            raise RuntimeError("Prepared baseline or artifacts changed")
        write_json(RUN / "adapter-metadata.json", active_external_adapters())
        inventory = json.loads(INVENTORY.read_bytes())
        proposed = (RUN / "proposed-pyproject.toml").read_bytes()
        (ROOT / "pyproject.toml").write_bytes(proposed)
        uv = str(ROOT / ".venv/Scripts/uv.exe")
        links = [argument for directory in CACHES for argument in ("--find-links", str(directory))]
        runner.run([uv, "lock", "--offline", "--no-build", *links], "uv-lock",
                   slots=4, processes=4, memory=512 * 1024**2, seconds=600)
        generated_lock = (ROOT / "uv.lock").read_bytes()
        locked = tomllib.loads((ROOT / "uv.lock").read_text())
        versions = {canonical_name(item["name"]): item["version"] for item in locked["package"]}
        for name, version in state["baseline"].items():
            if canonical_name(name) != "document-assistant" and versions.get(canonical_name(name)) != version:
                raise RuntimeError(f"Baseline lock version changed: {name}, expected {version}, "
                                   f"got {versions.get(canonical_name(name))}")
        expected = {canonical_name(item["name"]): item["version"]
                    for item in inventory["new_wheels"]}
        if any(versions.get(name) != version for name, version in expected.items()):
            raise RuntimeError("OCR lock pins mismatch")
        if set(versions) - set(state["baseline"]) - set(expected) - {"document-assistant"}:
            raise RuntimeError("Unexpected lock distribution")
        runner.run([uv, "sync", "--offline", "--frozen", "--all-groups", "--no-build", *links],
                   "uv-sync", slots=4, processes=4, memory=512 * 1024**2, seconds=600)
        installed = verify_artifacts()["baseline"]
        if any(installed.get(name) != version for name, version in (state["baseline"] | expected).items()
               if name != "document-assistant"):
            raise RuntimeError("Installed version mismatch")
        provisioning_complete = True
        # Restrict the outer Job after legitimate uv interpreter discovery ends.
        limits.basic.active = 2
        native.check(native.kernel.SetInformationJobObject(controller_job, 9,
                     ctypes.byref(limits), ctypes.sizeof(limits)))
        meter = json.loads((RUN / "meter.json").read_bytes())
        meter["phase"] = "offline-evaluation"
        meter["execution_deadline_utc"] = datetime.fromtimestamp(time.time() + 2700, UTC).isoformat()
        write_json(RUN / "meter.json", meter)

        def request(label, payload, **options):
            request_path = RUN / "requests" / (label + ".json")
            write_json(request_path, payload)
            # Direct existing base interpreter avoids the venv redirector child;
            # -S plus explicit project site path never inherits global packages.
            executable = str(Path("F:/Python/Python314/python.exe"))
            args = [executable, "-I", "-S", "-B", str(Path(__file__).resolve()),
                    "worker", str(request_path)]
            return runner.run(args, label, **options)

        request("fixtures", {"kind": "fixtures"}, seconds=90)
        print("Open locally:", RUN / "fixtures/contact-sheet.html")
        review_started = time.time()
        if input("Review all gold/images locally. Type READY only if suitable: ") != "READY":
            raise RuntimeError("Fixture scoring readiness declined")
        review_pause = time.time() - review_started
        meter = json.loads((RUN / "meter.json").read_bytes())
        meter["user_review_pause_seconds"] = review_pause
        deadline = datetime.fromisoformat(meter["execution_deadline_utc"]).timestamp()
        meter["execution_deadline_utc"] = datetime.fromtimestamp(deadline + review_pause, UTC).isoformat()
        write_json(RUN / "meter.json", meter)
        ensure_disconnected()
        # Record this operational pause separately without resetting the run budget.
        print("TESTING IN PROGRESS. Keep all external links disconnected until teardown is verified.",
              flush=True)
        cases = {case["id"]: case for case in case_definitions()}
        for engine, case_id, repeat in comparison_schedule():
            label = f"{engine}-{case_id}-{repeat}"
            evidence = request(label, {"kind": "ocr", "engine": engine, "case_id": case_id})
            raw = json.loads((RUN / "raw" / (label + ".json")).read_bytes())
            gold = cases[case_id]["gold"]
            facts = [value for value in ("24000", "125.00", "100", "160") if value in gold]
            summary = {"engine": engine, "case_id": case_id, "repeat": repeat,
                       "cer": raw["cer"], "wer": raw["wer"],
                       "facts_exact": all(value in raw["text"] for value in facts),
                       "page": raw["page"], "method": raw["method"],
                       "warnings": raw["warnings"], "seconds": evidence["seconds"],
                       "boxes_available": bool(raw["boxes"]),
                       "private_commit_observed_peak": evidence["private_commit_observed_peak"],
                       "working_set_peak_observed": evidence["working_set_peak_observed"],
                       "initialization_seconds": raw["initialization_seconds"],
                       "ocr_seconds": raw["ocr_seconds"], "decode_seconds": raw["decode_seconds"],
                       "readable_gold": case_id not in {"M08", "M09"}}
            summary["quality_gate_pass"] = (
                raw["cer"] <= 0.05 and raw["wer"] <= 0.10 and summary["facts_exact"]
                if summary["readable_gold"] else None)
            result["comparisons"].append(summary)
            write_json(RUN / "summary.json", result)
        for engine, control in control_schedule():
            label = f"control-{engine}-{control}"
            evidence = request(label, {"kind": "control", "engine": engine, "control": control},
                               seconds=1 if control == "deadline" else 30,
                               timeout_expected=control == "deadline",
                               memory=64 * 1024**2 if control == "memory" else 1536 * 1024**2)
            raw_path = RUN / "raw" / (label + ".json")
            validate_control(control, json.loads(raw_path.read_bytes()) if raw_path.exists() else None,
                             evidence["timed_out"])
            result["controls"].append({"engine": engine, "control": control,
                                       "exit_code": evidence["exit_code"], "checked": True})
        result["status"] = "completed_pending_quality_review_no_adoption"
    except (OSError, RuntimeError, ValueError, ImportError, KeyboardInterrupt, EOFError) as error:
        result["status"] = "stopped_no_automatic_retry"
        result["error_type"] = type(error).__name__
        result["error"] = str(error)[:1000]
        if not provisioning_complete:
            # Restore only our exact proposed project edit; preserve all receipts.
            proposed_path = RUN / "proposed-pyproject.toml"
            if proposed_path.exists() and (ROOT / "pyproject.toml").read_bytes() == proposed_path.read_bytes():
                (ROOT / "pyproject.toml").write_bytes(project_before)
            if generated_lock is not None and (ROOT / "uv.lock").read_bytes() == generated_lock:
                (ROOT / "uv.lock").write_bytes(lock_before)
            result["provisioning_incomplete"] = True
    finally:
        result["active_owned_children"] = list(runner.children)
        result["controller_job"] = native.accounting(controller_job)
        result["teardown_verified"] = not runner.children and result["controller_job"]["active"] == 1
        write_json(RUN / "summary.json", result)
        print("STATUS:", result["status"])
        print("TEARDOWN VERIFIED:", result["teardown_verified"])
        print("Local sanitized report:", RUN / "summary.json")
        if not result["teardown_verified"]:
            print("REMAIN DISCONNECTED. Stop the owned trial process tree before reconnecting.")


if __name__ == "__main__":
    arguments = sys.argv[1:]
    if len(arguments) == 2 and arguments[0] in {"prepare", "offline"}:
        configure_run(arguments[1])
        arguments = arguments[:1]
    if arguments == ["prepare"]:
        prepare()
    elif arguments == ["offline"]:
        offline_main()
    elif len(arguments) == 2 and arguments[0] == "worker":
        request_path = Path(arguments[1]).resolve()
        configure_run(request_path.parent.parent.name)
        from appcontainer_preflight import contained

        worker(contained(RUN / "requests", request_path))
    else:
        raise SystemExit("Use only the reviewed prepare/offline handoff modes")
