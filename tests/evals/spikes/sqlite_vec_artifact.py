"""Metered static sqlite-vec wheel inspection; never installs/imports wheel code."""

from __future__ import annotations

import ast
import base64
import csv
import hashlib
import io
import json
import os
import re
import stat
import struct
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime
from email.parser import BytesParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "data/t12/sqlite-vec-artifact-01"
BUDGET = RUN / "budget.json"
WHEEL_NAME = "sqlite_vec-0.1.9-py3-none-win_amd64.whl"
WHEEL_SHA = "4a28dc12fa4b53d7b1dced22da2488fade444e96b5d16fd2d698cd670675cf32"
WHEEL_URL = (
    "https://files.pythonhosted.org/packages/42/89/81b2907cda14e566b9bf215e2ad82fc9b349edf07d2010756ffdb902f328/"
    + WHEEL_NAME
)
REGISTRY = "https://pypi.org/pypi/sqlite-vec/0.1.9/json"
TAG = "https://api.github.com/repos/asg017/sqlite-vec/git/ref/tags/v0.1.9"
SOURCES = {
    "LICENSE-MIT",
    "LICENSE-APACHE",
    "VERSION",
    "sqlite-dist.toml",
    "Makefile",
    "bindings/python/extra_init.py",
    "sqlite-vec.c",
    "sqlite-vec.h",
}


def save(path: Path, value: object) -> None:
    """Replace an owned receipt atomically, propagating every failure."""
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2), encoding="utf-8")
    temporary.replace(path)


def check_time() -> dict:
    """Read the one approved epoch; no restarted deadline or closed allocation."""
    state = json.loads(BUDGET.read_text(encoding="utf-8-sig"))
    elapsed = time.time() - datetime.fromisoformat(state["started_utc"]).timestamp()
    if state["status"] != "active" or not 0 <= elapsed <= 1200:
        raise RuntimeError("Package deadline/state boundary")
    return state


def watchdog() -> None:
    """Hard-stop this single inspection process after 120 seconds."""

    def expire():
        try:
            save(
                RUN / "watchdog-stop.json",
                {"status": "inspection_timeout", "limit_seconds": 120},
            )
        finally:
            os._exit(125)

    timer = threading.Timer(120, expire)
    timer.daemon = True
    timer.start()


def reserve_http(path: Path, url: str, maximum: int) -> int:
    """Durably reserve request plus capped bytes before opening a connection."""
    state = json.loads(path.read_text(encoding="utf-8-sig"))
    if (
        state["requests"] >= state["request_limit"]
        or state["reserved_bytes"] + maximum > state["byte_limit"]
    ):
        raise RuntimeError("HTTP shared allowance exhausted")
    state["requests"] += 1
    state["reserved_bytes"] += maximum
    state["events"].append(
        {"url": url, "reserved": maximum, "actual": 0, "status": "reserved_before_send"}
    )
    save(path, state)
    return len(state["events"]) - 1


def read_body(
    stream, limit: int, declared: int | None, digest: str | None, charge=None
) -> bytes:
    """Count received body chunks, detect truncation/overflow and verify identity."""
    body = bytearray()
    while True:
        chunk = stream.read(min(65536, limit + 1 - len(body)))
        if not chunk:
            break
        if charge:
            charge(len(chunk))
        body.extend(chunk)
        if len(body) > limit:
            raise ValueError("Body exceeded per-response cap")
    if declared is not None and len(body) != declared:
        raise ValueError("Truncated or unexpected body length")
    if digest and hashlib.sha256(body).hexdigest() != digest:
        raise ValueError("Artifact hash mismatch")
    return bytes(body)


def allowed_url(url: str) -> None:
    """Allow only exact approved public identities, never arbitrary response links."""
    parsed = urllib.parse.urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.username
        or parsed.password
        or parsed.port
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Unapproved public URL")
    if url in {WHEEL_URL, REGISTRY, TAG}:
        return
    if re.fullmatch(
        r"https://api\.github\.com/repos/asg017/sqlite-vec/git/(tags|commits)/[a-f0-9]{40}",
        url,
    ):
        return
    prefix = "https://raw.githubusercontent.com/asg017/sqlite-vec/"
    if url.startswith(prefix):
        commit, _, relative = url[len(prefix) :].partition("/")
        if re.fullmatch("[a-f0-9]{40}", commit) and relative in SOURCES:
            return
    raise ValueError("Unapproved public URL")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Redirects are explicit findings, never implicit unmetered attempts."""

    def redirect_request(self, request, file, code, message, headers, newurl):
        return None


def retrieve(url: str, limit: int, expected_size=None, digest=None) -> bytes:
    """Download public bytes with durable per-attempt accounting and no proxy/retry."""
    check_time()
    allowed_url(url)
    index = reserve_http(BUDGET, url, limit + 1)

    def count(amount):
        state = json.loads(BUDGET.read_text(encoding="utf-8-sig"))
        state["actual_bytes"] += amount
        state["events"][index]["actual"] += amount
        save(BUDGET, state)

    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    request = urllib.request.Request(
        url,
        headers={
            "Accept-Encoding": "identity",
            "User-Agent": "document-assistant-static-review",
        },
    )
    status = "failed"
    try:
        try:
            response = opener.open(request, timeout=15)
        except urllib.error.HTTPError as error:
            with error:
                read_body(error, min(limit, 65536), None, None, count)
            raise RuntimeError("HTTP error: " + str(error.code)) from None
        with response:
            if (
                response.headers.get("Content-Encoding", "identity").lower()
                != "identity"
            ):
                raise ValueError("Unsupported response content encoding")
            declared = response.headers.get("Content-Length")
            declared = int(declared) if declared is not None else None
            if declared is not None and not 0 <= declared <= limit:
                raise ValueError("Declared length exceeds response cap")
            body = read_body(response, limit, declared, digest, count)
            if expected_size is not None and len(body) != expected_size:
                raise ValueError("Pinned byte size mismatch")
        status = "verified_body"
        return body
    finally:
        state = json.loads(BUDGET.read_text(encoding="utf-8-sig"))
        state["events"][index]["status"] = status
        save(BUDGET, state)


def member_name(name: str) -> str:
    """Canonicalize archive names under Windows rules without extracting them."""
    if (
        not name
        or "\\" in name
        or ":" in name
        or name.startswith("/")
        or "\x00" in name
    ):
        raise ValueError("Unsafe ZIP path")
    parts = name.rstrip("/").split("/")
    for part in parts:
        if (
            part in {"", ".", ".."}
            or part.rstrip(" .") != part
            or re.fullmatch(
                r"(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?", part, re.IGNORECASE
            )
        ):
            raise ValueError("Unsafe Windows member")
    return "/".join(parts).casefold()


def inspect_zip(blob: bytes) -> dict[str, bytes]:
    """Cap metadata and expanded reads, reject aliases/links, verify all RECORD rows."""
    output, names, expanded = {}, set(), 0
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        entries = archive.infolist()
        if len(entries) > 128:
            raise ValueError("ZIP member limit")
        for entry in entries:
            canonical = member_name(entry.filename)
            mode = (entry.external_attr >> 16) & 0o170000
            if (
                canonical in names
                or mode not in {0, stat.S_IFREG, stat.S_IFDIR}
                or entry.external_attr & 0x400
                or entry.flag_bits & 1
                or entry.compress_type not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}
            ):
                raise ValueError("ZIP aliases/link/encryption/compression")
            names.add(canonical)
            if entry.is_dir():
                continue
            if entry.file_size > 8 * 1024**2 or entry.file_size > 100 * max(
                1, entry.compress_size
            ):
                raise ValueError("ZIP expansion cap")
            expanded += entry.file_size
            if expanded > 16 * 1024**2:
                raise ValueError("ZIP total expansion cap")
            with archive.open(entry) as stream:
                content = read_body(
                    stream,
                    min(
                        8 * 1024**2, 16 * 1024**2 - sum(len(x) for x in output.values())
                    ),
                    entry.file_size,
                    None,
                )
            output[entry.filename] = content
    records = [name for name in output if name.endswith(".dist-info/RECORD")]
    if len(records) != 1:
        raise ValueError("Missing/duplicate wheel RECORD")
    seen = set()
    for row in csv.reader(io.StringIO(output[records[0]].decode("utf-8"))):
        if len(row) != 3 or row[0] in seen or row[0] not in output:
            raise ValueError("Invalid RECORD inventory")
        name, encoded, size = row
        seen.add(name)
        if name == records[0]:
            if encoded or size:
                raise ValueError("RECORD self identity must be empty")
            continue
        expected = (
            "sha256="
            + base64.urlsafe_b64encode(hashlib.sha256(output[name]).digest())
            .rstrip(b"=")
            .decode()
        )
        if encoded != expected or size != str(len(output[name])):
            raise ValueError("RECORD member identity mismatch")
    if seen != set(output):
        raise ValueError("Unrecorded wheel member")
    return output


def inspect_pe(blob: bytes) -> dict:
    """Parse bounded x64 PE sections/import/export names; never load a DLL."""

    def bounded(offset, length):
        if offset < 0 or length < 0 or offset + length > len(blob):
            raise ValueError("PE offset/length outside image")
        return blob[offset : offset + length]

    if bounded(0, 2) != b"MZ":
        raise ValueError("Missing DOS header")
    pe = struct.unpack("<I", bounded(60, 4))[0]
    if bounded(pe, 4) != b"PE\x00\x00":
        raise ValueError("Missing PE header")
    machine, count, _, _, _, optional_size, characteristics = struct.unpack(
        "<HHIIIHH", bounded(pe + 4, 20)
    )
    if machine != 0x8664 or not 1 <= count <= 96 or not characteristics & 0x2000:
        raise ValueError("Not a bounded AMD64 DLL")
    optional = pe + 24
    bounded(optional, optional_size)
    if optional_size < 128 or struct.unpack("<H", bounded(optional, 2))[0] != 0x20B:
        raise ValueError("Invalid PE32+ header")
    sections = []
    for i in range(count):
        offset = optional + optional_size + i * 40
        name, virtual_size, rva, raw_size, raw_offset = struct.unpack(
            "<8sIIII", bounded(offset, 24)
        )
        bounded(raw_offset, raw_size)
        sections.append(
            {
                "name": name.rstrip(b"\x00").decode("ascii", "replace"),
                "rva": rva,
                "virtual_size": virtual_size,
                "raw_size": raw_size,
                "raw_offset": raw_offset,
            }
        )

    def address(rva, length=1):
        for section in sections:
            delta = rva - section["rva"]
            if 0 <= delta and delta + length <= section["raw_size"]:
                offset = section["raw_offset"] + delta
                bounded(offset, length)
                return offset
        raise ValueError("PE RVA not file-backed")

    def cstring(rva):
        offset = address(rva)
        end = blob.find(b"\x00", offset, min(len(blob), offset + 512))
        if end < 0:
            raise ValueError("Unbounded PE string")
        address(rva, end - offset + 1)
        return blob[offset:end].decode("ascii")

    imports = []
    import_rva, import_size = struct.unpack("<II", bounded(optional + 120, 8))
    if import_rva:
        if not 20 <= import_size <= 65536:
            raise ValueError("PE import directory cap")
        for i in range(min(128, import_size // 20)):
            values = struct.unpack(
                "<IIIII", bounded(address(import_rva + i * 20, 20), 20)
            )
            if not any(values):
                break
            thunk_rva, _, _, name_rva, first_thunk = values
            functions = []
            for j in range(4096):
                thunk = struct.unpack(
                    "<Q", bounded(address((thunk_rva or first_thunk) + j * 8, 8), 8)
                )[0]
                if not thunk:
                    break
                functions.append(
                    "ordinal:" + str(thunk & 0xFFFF)
                    if thunk >> 63
                    else cstring(thunk + 2)
                )
            else:
                raise ValueError("PE import thunk cap")
            imports.append({"dll": cstring(name_rva), "functions": functions})
        else:
            raise ValueError("PE import descriptor cap")
    exports = []
    export_rva, _ = struct.unpack("<II", bounded(optional + 112, 8))
    if export_rva:
        directory = address(export_rva, 40)
        names_count = struct.unpack("<I", bounded(directory + 24, 4))[0]
        names_rva = struct.unpack("<I", bounded(directory + 32, 4))[0]
        if names_count > 4096:
            raise ValueError("PE export cap")
        for i in range(names_count):
            exports.append(
                cstring(
                    struct.unpack("<I", bounded(address(names_rva + i * 4, 4), 4))[0]
                )
            )
    return {
        "machine": "AMD64",
        "sections": sections,
        "imports": imports,
        "exports": exports,
        "entrypoint_rva": struct.unpack("<I", bounded(optional + 16, 4))[0],
    }


def inspect_wheel(files: dict[str, bytes]) -> dict:
    """Read Python as AST/text and native bytes as PE, with exact metadata checks."""
    metadata_names = [n for n in files if n.endswith(".dist-info/METADATA")]
    wheel_names = [n for n in files if n.endswith(".dist-info/WHEEL")]
    if len(metadata_names) != 1 or len(wheel_names) != 1:
        raise ValueError("Wheel metadata inventory")
    metadata = BytesParser().parsebytes(files[metadata_names[0]])
    tags = BytesParser().parsebytes(files[wheel_names[0]])
    if (
        metadata["Name"].replace("_", "-") != "sqlite-vec"
        or metadata["Version"] != "0.1.9"
        or "py3-none-win_amd64" not in tags.get_all("Tag", [])
    ):
        raise ValueError("Wheel name/version/platform mismatch")
    python, notices, binaries = {}, [], {}
    for name, content in files.items():
        lower = name.casefold()
        if lower.endswith((".pth", ".exe", ".bat", ".cmd", ".ps1", "entry_points.txt")):
            raise ValueError("Unexpected startup/entry-point executable")
        if lower.endswith(".py"):
            ast.parse(content, filename=name)
            python[name] = content.decode("utf-8")
        if any(x in lower for x in ("license", "notice", "copying")):
            notices.append(
                {
                    "name": name,
                    "bytes": len(content),
                    "sha256": hashlib.sha256(content).hexdigest(),
                }
            )
        if lower.endswith((".dll", ".pyd")):
            if lower != "sqlite_vec/vec0.dll" or binaries:
                raise ValueError("Unexpected native member")
            binaries[name] = inspect_pe(content)
    return {
        "inventory": [
            {"name": n, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
            for n, b in files.items()
        ],
        "expanded_bytes": sum(map(len, files.values())),
        "requires_python": metadata["Requires-Python"],
        "requires_dist": metadata.get_all("Requires-Dist", []),
        "notices": notices,
        "python_text": python,
        "native": binaries,
    }


def review() -> None:
    """Single bounded retrieval/static review; every stop is preserved without retry."""
    if (RUN / "review-started.json").exists():
        raise RuntimeError("Never repeat started artifact retrieval")
    check_time()
    save(RUN / "review-started.json", {"started": time.time()})
    result = {"status": "started", "installed": False, "loaded": False}
    try:
        metadata = json.loads(retrieve(REGISTRY, 512 * 1024))
        entry = next(x for x in metadata["urls"] if x["filename"] == WHEEL_NAME)
        if (
            entry["url"] != WHEEL_URL
            or entry["size"] != 292804
            or entry["digests"]["sha256"] != WHEEL_SHA
            or entry.get("yanked")
        ):
            raise ValueError("Registry identity drift")
        result["registry"] = {
            "filename": entry["filename"],
            "bytes": entry["size"],
            "sha256": entry["digests"]["sha256"],
            "requires_dist": metadata["info"].get("requires_dist"),
            "homepage": metadata["info"].get("home_page"),
        }
        blob = retrieve(WHEEL_URL, 292804, 292804, WHEEL_SHA)
        (RUN / WHEEL_NAME).write_bytes(blob)
        files = inspect_zip(blob)
        result["wheel"] = inspect_wheel(files)
        save(RUN / "summary.json", result)
        tag = json.loads(retrieve(TAG, 512 * 1024))
        if tag.get("ref") != "refs/tags/v0.1.9":
            raise ValueError("Unexpected tag identity")
        obj = tag["object"]
        if obj["type"] == "tag" and re.fullmatch("[a-f0-9]{40}", obj["sha"]):
            obj = json.loads(
                retrieve(
                    "https://api.github.com/repos/asg017/sqlite-vec/git/tags/"
                    + obj["sha"],
                    512 * 1024,
                )
            )["object"]
        if obj["type"] != "commit" or not re.fullmatch("[a-f0-9]{40}", obj["sha"]):
            raise ValueError("Tag did not resolve to immutable commit")
        commit = obj["sha"]
        result["upstream_commit"] = commit
        sources = {}
        for relative in (
            "LICENSE-MIT",
            "LICENSE-APACHE",
            "VERSION",
            "sqlite-dist.toml",
            "bindings/python/extra_init.py",
            "Makefile",
            "sqlite-vec.c",
        ):
            body = retrieve(
                "https://raw.githubusercontent.com/asg017/sqlite-vec/"
                + commit
                + "/"
                + relative,
                1024**2 if relative == "sqlite-vec.c" else 128 * 1024,
            )
            local_name = "source-" + relative.replace("/", "_") + ".txt"
            (RUN / local_name).write_bytes(body)
            sources[relative] = {
                "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
            }
        result["source_identities"] = sources
        result["status"] = "static_review_completed_no_install_no_load"
    except BaseException as error:
        result.update(
            status="stopped_no_automatic_retry",
            error_type=type(error).__name__,
            reason=str(error),
        )
        raise
    finally:
        state = json.loads(BUDGET.read_text(encoding="utf-8-sig"))
        (
            result["requests"],
            result["actual_body_bytes"],
            result["reserved_body_bytes"],
        ) = state["requests"], state["actual_bytes"], state["reserved_bytes"]
        result["output_bytes"] = sum(
            p.stat().st_size for p in RUN.rglob("*") if p.is_file()
        )
        if result["output_bytes"] > 32 * 1024**2:
            result["status"] = "stopped_output_cap"
        save(RUN / "summary.json", result)
        print(
            json.dumps(
                {
                    k: result[k]
                    for k in (
                        "status",
                        "requests",
                        "actual_body_bytes",
                        "installed",
                        "loaded",
                    )
                }
            )
        )


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from appcontainer_preflight import Native

    native = Native()
    job = native.job(1, kill=False)
    native.check(
        native.kernel.AssignProcessToJobObject(job, native.kernel.GetCurrentProcess())
    )
    watchdog()
    if sys.argv[1:] != ["review"]:
        raise SystemExit("Only the approved static review mode")
    review()
