"""Windows-only, bounded T05 evaluation aid; no application parser contract."""

import ctypes
import hashlib
import json
import logging
import subprocess
import sys
import time
from ctypes import wintypes
from pathlib import Path


def run_limited(command: list[str], timeout: float = 60) -> dict:
    """Gate execution on Windows job assignment; kill the job on timeout or exit."""
    if sys.platform != "win32":
        raise RuntimeError("This trial requires Windows Job Objects")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)

    class Basic(ctypes.Structure):
        _fields_ = [
            ("process_time", ctypes.c_int64),
            ("job_time", ctypes.c_int64),
            ("flags", wintypes.DWORD),
            ("min_ws", ctypes.c_size_t),
            ("max_ws", ctypes.c_size_t),
            ("active", wintypes.DWORD),
            ("affinity", ctypes.c_size_t),
            ("priority", wintypes.DWORD),
            ("scheduling", wintypes.DWORD),
        ]

    class Extended(ctypes.Structure):
        _fields_ = [
            ("basic", Basic),
            ("io", ctypes.c_uint64 * 6),
            ("process_memory", ctypes.c_size_t),
            ("job_memory", ctypes.c_size_t),
            ("peak_process", ctypes.c_size_t),
            ("peak_job", ctypes.c_size_t),
        ]

    kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    kernel.CreateJobObjectW.restype = wintypes.HANDLE
    kernel.SetInformationJobObject.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    ]
    kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    kernel.QueryInformationJobObject.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.c_void_p,
    ]
    kernel.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    job = kernel.CreateJobObjectW(None, None)
    if not job:
        raise ctypes.WinError(ctypes.get_last_error())
    process = None
    started = time.perf_counter()
    try:
        limits = Extended()
        # The Windows venv launcher starts the actual interpreter as a second process.
        # Bound the entire job as well as each process to 2 GiB committed memory.
        limits.basic.flags = 0x2000 | 0x8 | 0x100 | 0x200
        limits.basic.active = 2
        limits.process_memory = 2 * 1024**3
        limits.job_memory = 2 * 1024**3
        if not kernel.SetInformationJobObject(
            job, 9, ctypes.byref(limits), ctypes.sizeof(limits)
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        if not kernel.AssignProcessToJobObject(job, wintypes.HANDLE(process._handle)):
            raise ctypes.WinError(ctypes.get_last_error())
        status = "ok"
        try:
            output, _ = process.communicate(b"go\n", timeout=timeout)
            if process.returncode:
                status = "error"
        except subprocess.TimeoutExpired:
            kernel.TerminateJobObject(job, 1)
            output, _ = process.communicate(timeout=5)
            status = "timeout"
        observed = Extended()
        if not kernel.QueryInformationJobObject(
            job, 9, ctypes.byref(observed), ctypes.sizeof(observed), None
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        return {
            "status": status,
            "returncode": process.returncode,
            "elapsed_s": round(time.perf_counter() - started, 4),
            "peak_private_bytes": observed.peak_process,
            "stdout": output.decode("utf-8"),
        }
    finally:
        kernel.CloseHandle(job)
        if process is not None and process.poll() is None:
            process.kill()
            process.wait(timeout=5)


def parse_limited(candidate: str, path: Path, pages: list[int]) -> dict:
    """Extract only explicit pages under the job and caller's sandbox network boundary."""
    result = run_limited(
        [
            sys.executable,
            "-I",
            "-B",
            str(Path(__file__).resolve()),
            "worker",
            candidate,
            str(path.resolve()),
            ",".join(map(str, pages)),
        ]
    )
    if result["status"] == "ok":
        result["payload"] = json.loads(result.pop("stdout"))
    return result


def extract(candidate: str, path: Path, selected: list[int]) -> dict:
    """Trial adapters deliberately expose missing table/region support as warnings."""
    from importlib.metadata import version

    if path.suffix.lower() != ".pdf":
        return {"error": "invalid_extension"}
    if path.stat().st_size > 100 * 1024**2 or len(selected) > 5:
        raise ValueError("Trial input budget exceeded")
    started = time.perf_counter()
    if candidate == "pypdf":
        from pypdf import PdfReader

        document = PdfReader(path, strict=True)
        if document.is_encrypted:
            return {"error": "protected"}
        total = len(document.pages)
    elif candidate == "pdfplumber":
        import pdfplumber

        document = pdfplumber.open(path)
        if document.doc.encryption:
            document.close()
            return {"error": "protected"}
        total = len(document.pages)
    else:
        raise ValueError("Unknown trial candidate")
    open_s = time.perf_counter() - started
    records = []
    try:
        for number in selected:
            if not 1 <= number <= total:
                continue
            page = document.pages[number - 1]
            tables, images, warnings = [], [], []
            if candidate == "pypdf":
                text = page.extract_text() or ""
                # Referenced resource entries can include unused images. Actual Do calls
                # are required before calling a resource an image occurrence on this page.
                from pypdf.generic import ContentStream

                stream = ContentStream(page.get_contents(), document)
                resources = page.get("/Resources", {}).get("/XObject", {})
                for operands, operator in stream.operations:
                    if operator == b"Do":
                        obj = resources.get(operands[0])
                        if obj and obj.get_object().get("/Subtype") == "/Image":
                            images.append({"resource": str(operands[0]), "bbox": None})
                warnings.append("page_only_geometry")
            else:
                text = page.extract_text() or ""
                for table in page.find_tables():
                    tables.append({"bbox": list(table.bbox), "rows": table.extract()})
                images = [
                    {"bbox": [i["x0"], i["top"], i["x1"], i["bottom"]]}
                    for i in page.images
                ]
            kind = (
                "native"
                if text.strip()
                else (
                    "image_without_native_text" if images else "empty_no_raster_image"
                )
            )
            if kind != "native":
                warnings.append("native_text_absent_not_proof_of_blank_or_scan")
            if len(text) > 256 * 1024:
                raise ValueError("Trial text output ceiling exceeded")
            records.append(
                {
                    "page": number,
                    "text": text,
                    "kind": kind,
                    "images": images,
                    "tables": tables,
                    "warnings": warnings,
                }
            )
    finally:
        document.close()
    return {
        "candidate": candidate,
        "version": version(candidate),
        "page_count": total,
        "open_s": round(open_s, 4),
        "extraction_s": round(time.perf_counter() - started - open_s, 4),
        "pages": records,
    }


def benchmark(output: Path) -> None:
    """Repeat the identical three-page sample with local, visually reviewed gold facts."""
    data_root = Path(__file__).resolve().parents[3] / "data"
    output = output.resolve()
    if not output.is_relative_to(data_root) or output == data_root:
        raise ValueError("Raw results must stay below project data")
    # Gold was established from local renders before these scoring runs. It is not
    # sent to a model or regenerated from whichever parser happens to be measured.
    gold_path = data_root / "pdf-t05/gold.json"
    gold = json.loads(gold_path.read_text(encoding="utf-8"))
    sources = sorted((data_root.parent / "sample_files").glob("*.pdf"))
    if len(sources) != 3 or set(gold) != {p.name for p in sources}:
        raise ValueError("This bounded trial expects the three reviewed PDF samples")
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    output.mkdir(parents=True, exist_ok=False)
    records = []
    for candidate in ["pypdf", "pdfplumber"]:
        started = time.monotonic()
        for repeat in range(4):
            for path in sources:
                result = parse_limited(candidate, path, [1, 2, 3])
                if result["status"] == "ok":
                    page, phrases = gold[path.name]
                    text = " ".join(
                        result["payload"]["pages"][page - 1]["text"].split()
                    )
                    result["gold_pass"] = all(phrase in text for phrase in phrases)
                records.append(
                    {"file": path.name, "candidate": candidate, "run": repeat, **result}
                )
                serialized = json.dumps(
                    {
                        "sources": before,
                        "script_sha256": hashlib.sha256(
                            Path(__file__).read_bytes()
                        ).hexdigest(),
                        "gold_sha256": hashlib.sha256(
                            gold_path.read_bytes()
                        ).hexdigest(),
                        "runs": records,
                    },
                    indent=2,
                )
                if len(serialized.encode()) > 256 * 1024**2:
                    raise RuntimeError("Trial output ceiling exceeded")
                (output / "results.json").write_text(serialized, encoding="utf-8")
                print(
                    candidate,
                    repeat,
                    path.name,
                    result["status"],
                    result["elapsed_s"],
                    flush=True,
                )
                if result["status"] != "ok" or time.monotonic() - started > 180:
                    raise RuntimeError(
                        "Worker failure or candidate time budget exceeded"
                    )
    assert before == {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources
    }


def main() -> None:
    """Worker mode requires the parent's gate; batch writes only local ignored results."""
    if len(sys.argv) == 3 and sys.argv[1] == "--benchmark":
        benchmark(Path(sys.argv[2]))
        return
    if len(sys.argv) > 1 and sys.argv[1] == "worker":
        if input() != "go":
            raise RuntimeError("Missing job gate")
        if sys.argv[2] == "pypdf":
            from pypdf.errors import PdfReadError

            parser_errors = (PdfReadError,)
        else:
            from pdfminer.pdfdocument import PDFPasswordIncorrect
            from pdfminer.pdfparser import PDFSyntaxError
            from pdfminer.psparser import PSEOF
            from pdfplumber.utils.exceptions import PdfminerException

            parser_errors = (
                PDFPasswordIncorrect,
                PDFSyntaxError,
                PSEOF,
                PdfminerException,
            )

        class WarningCounter(logging.Handler):
            """Count library diagnostics without retaining source-bearing messages."""

            count = 0

            def emit(self, record: logging.LogRecord) -> None:
                self.count += 1

        counter = WarningCounter()
        logging.getLogger().handlers = [counter]
        logging.getLogger().setLevel(logging.WARNING)
        try:
            payload = extract(
                sys.argv[2], Path(sys.argv[3]), list(map(int, sys.argv[4].split(",")))
            )
        except parser_errors as error:
            # Record exception type, never library exception messages containing source text.
            cause = error.__context__ or error
            kind = (
                "protected"
                if type(cause).__name__ == "PDFPasswordIncorrect"
                else "invalid_pdf"
            )
            payload = {"error": kind, "exception": type(error).__name__}
        payload["library_warning_count"] = counter.count

        class MemoryCounters(ctypes.Structure):
            _fields_ = [
                ("cb", wintypes.DWORD),
                ("faults", wintypes.DWORD),
                ("values", ctypes.c_size_t * 8),
            ]

        counters = MemoryCounters()
        counters.cb = ctypes.sizeof(counters)
        psapi = ctypes.WinDLL("psapi", use_last_error=True)
        psapi.GetProcessMemoryInfo.argtypes = [
            wintypes.HANDLE,
            ctypes.c_void_p,
            wintypes.DWORD,
        ]
        if not psapi.GetProcessMemoryInfo(
            wintypes.HANDLE(-1), ctypes.byref(counters), counters.cb
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        payload["peak_working_set_bytes"] = counters.values[0]
        serialized = json.dumps(payload, ensure_ascii=True)
        if len(serialized) > 8 * 1024**2:
            raise RuntimeError("Serialized output budget exceeded")
        print(serialized)
        return
    raise SystemExit(
        "Use parse_limited() from the T05 local runner; this is not an application CLI."
    )


if __name__ == "__main__":
    main()
