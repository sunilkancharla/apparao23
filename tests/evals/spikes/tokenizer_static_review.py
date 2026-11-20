"""Bounded IF-N data acquisition/ZIP inspection; never import candidate code."""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import ipaddress
import json
import os
import re
import socket
import stat
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime
from email.parser import BytesParser
from pathlib import Path

MIB = 1024**2
ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "data/t17/input-fit-tokenizer-static-01"
ASSETS = (
    (
        "Qwen/Qwen2.5-1.5B-Instruct",
        "5fee7c4ed634dc66c6e318c8ac2897b8b9154536",
        (
            "tokenizer.json",
            "tokenizer_config.json",
            "vocab.json",
            "merges.txt",
            "config.json",
            "LICENSE",
        ),
    ),
    (
        "nomic-ai/nomic-embed-text-v1.5",
        "541c5a6fadb4da793505a2bb4d3ee910de7f39ea",
        (
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "vocab.txt",
            "config.json",
        ),
    ),
)
WHEELS = (
    (
        "tokenizers",
        "0.23.3",
        "tokenizers-0.23.3-cp310-abi3-win_amd64.whl",
        "1f0823bb00c5fdc98e487354d54dd55a03848d61a1a0bf29a68c77f24f3b26c3",
        4 * MIB,
        "cp310-abi3-win_amd64",
    ),
    (
        "huggingface-hub",
        "2.4.0",
        "huggingface_hub-2.4.0-py3-none-any.whl",
        "42ecfd93ede47bdd333daebbf66a32d7bfe2e18752754fe4d2d4f98a0179d801",
        2 * MIB,
        "py3-none-any",
    ),
)


def is_reparse(path: Path) -> bool:
    """Detect Windows reparse points and ordinary symlinks without following."""
    value = path.lstat()
    return stat.S_ISLNK(value.st_mode) or bool(
        getattr(value, "st_file_attributes", 0) & 0x400
    )


def safe_name(name: str) -> str:
    """Reject traversal, Windows aliases and ambiguous ZIP/output names."""
    if not name or any(c in name for c in "\\:\x00") or name.startswith("/"):
        raise ValueError("Unsafe path")
    parts = name.rstrip("/").split("/")
    for part in parts:
        if (
            part in {"", ".", ".."}
            or part.rstrip(" .") != part
            or re.fullmatch(r"(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?", part, re.IGNORECASE)
        ):
            raise ValueError("Unsafe Windows path")
    return unicodedata.normalize("NFC", "/".join(parts)).casefold()


class Budget:
    """One durable epoch with no refunds, retries or implicit output overwrite."""

    def __init__(self, root: Path):
        self.root = root
        self.path = root / "meter.json"

    def contained(self, name: str) -> Path:
        safe_name(name)
        path = self.root / name
        for item in (path, *path.parents):
            if item.exists() and is_reparse(item):
                raise ValueError("Reparse path")
        if path.exists() and is_reparse(path):
            raise ValueError("Reparse file")
        if not path.resolve().is_relative_to(self.root.resolve()):
            raise ValueError("Outside review root")
        return path

    def state(self) -> dict:
        self.contained("meter.json")
        value = json.loads(self.path.read_text(encoding="utf-8-sig"))
        start = value["started_utc"]
        started = (
            datetime.fromisoformat(start).timestamp()
            if isinstance(start, str)
            else start
        )
        elapsed = time.time() - started
        if value["status"] != "active" or not 0 <= elapsed <= 1800:
            raise ValueError("Epoch state/time boundary")
        if (
            "started_tick" in value
            and not 0
            <= time.perf_counter() - value["started_tick"] / value["frequency"]
            <= 1800
        ):
            raise ValueError("Monotonic boundary")
        if self.tree_bytes() >= 32 * MIB:
            raise ValueError("Output boundary")
        return value

    def tree_bytes(self) -> int:
        """Bound enumeration before descending; never follow reparse directories."""
        pending, count, size = [self.root], 0, 0
        while pending:
            directory = pending.pop()
            with os.scandir(directory) as entries:
                for entry in entries:
                    count += 1
                    path = Path(entry.path)
                    if count > 4000 or is_reparse(path):
                        raise ValueError("Review tree boundary")
                    if entry.is_dir(follow_symlinks=False):
                        pending.append(path)
                    elif entry.is_file(follow_symlinks=False):
                        size += entry.stat(follow_symlinks=False).st_size
                    else:
                        raise ValueError("Unsupported review file")
        return size

    def save(self, value: dict) -> None:
        temporary = self.contained("meter.pending")
        with temporary.open("x", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, self.path)

    def reserve_body(self, category: str, amount: int) -> None:
        value = self.state()
        limits = {"wheel": 6 * MIB, "asset": 14 * MIB, "metadata": 8 * MIB}
        if amount <= 0 or value["body_reserved"][category] + amount > limits[category]:
            raise ValueError("Body reservation boundary")
        value["body_reserved"][category] += amount
        self.save(value)

    def transaction(self, url: str) -> int:
        value = self.state()
        if (
            value["http_reserved"] >= 48
            or value["body_reserved"]["metadata"] + 4097 > 8 * MIB
        ):
            raise ValueError("HTTP boundary")
        value["http_reserved"] += 1
        value["body_reserved"]["metadata"] += 4097
        value["events"].append(
            {"url": url, "bytes": 0, "status": "reserved_before_send"}
        )
        self.save(value)
        return len(value["events"]) - 1

    def event(self, index: int, amount: int = 0, status: str = "reading") -> None:
        value = self.state()
        value["events"][index]["bytes"] += amount
        value["events"][index]["status"] = status
        self.save(value)

    def output(self, name: str, data: bytes) -> None:
        self.state()
        path = self.contained(name)
        if self.tree_bytes() + len(data) > 32 * MIB:
            raise ValueError("Output write boundary")
        with path.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())

    def report(self, name: str, value: object) -> None:
        self.output(name, json.dumps(value, indent=2).encode())


def allowed_url(url: str) -> None:
    """Allow exact publisher/version paths and reviewed registry wheel identities."""
    parsed = urllib.parse.urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.username
        or parsed.password
        or parsed.port
        or parsed.fragment
    ):
        raise ValueError("URL boundary")
    if (
        parsed.hostname == "pypi.org"
        and not parsed.query
        and parsed.path in {f"/pypi/{n}/{v}/json" for n, v, *_ in WHEELS}
    ):
        return
    if parsed.hostname == "files.pythonhosted.org" and not parsed.query:
        for _, _, filename, *_ in WHEELS:
            if re.fullmatch(
                r"/packages/[a-f0-9]{2}/[a-f0-9]{2}/[a-f0-9]{60}/"
                + re.escape(filename),
                parsed.path,
            ):
                return
    if parsed.hostname == "huggingface.co":
        for publisher, revision, files in ASSETS:
            if (
                parsed.path == f"/api/models/{publisher}/tree/{revision}"
                and not parsed.query
            ):
                return
            for filename in files:
                origin = f"/{publisher}/resolve/{revision}/{filename}"
                cached = f"/api/resolve-cache/models/{publisher}/{revision}/{filename}"
                if parsed.path in {origin, cached}:
                    pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
                    if (
                        len(parsed.query) <= 2048
                        and len(pairs) <= 3
                        and all(
                            (k == "download" and v in {"true", "false"})
                            or (k == "etag" and re.fullmatch(r'"?[a-f0-9]{40,64}"?', v))
                            or (k == origin and v == "")
                            for k, v in pairs
                        )
                    ):
                        return
    raise ValueError("Unapproved artifact URL")


def public_addresses(host: str) -> None:
    """Refuse non-public DNS results; subsequent TLS DNS resolution is not pinned."""
    addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    if not addresses or any(
        not ipaddress.ip_address(item[4][0]).is_global for item in addresses
    ):
        raise ValueError("Non-public address")


def read_body(
    stream, limit: int, expected_size=None, digest=None, charge=None
) -> bytes:
    """Read capped inert bytes, charging the overflow probe before rejecting."""
    out = bytearray()
    while True:
        chunk = stream.read(min(65536, limit + 1 - len(out)))
        if not chunk:
            break
        if charge:
            charge(len(chunk))
        out.extend(chunk)
        if len(out) > limit:
            raise ValueError("Body overflow")
    if expected_size is not None and len(out) != expected_size:
        raise ValueError("Body size mismatch")
    if digest is not None and hashlib.sha256(out).hexdigest() != digest:
        raise ValueError("Body digest mismatch")
    return bytes(out)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Leave redirect accounting and validation to the finite acquisition loop."""

    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def fetch(
    budget: Budget, url: str, category: str, limit: int, size=None, digest=None
) -> bytes:
    """One logical fetch, at most two checked redirects, no proxy/retry/decoding."""
    budget.reserve_body(category, limit + 1)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    for redirects in range(3):
        allowed_url(url)
        public_addresses(urllib.parse.urlsplit(url).hostname)
        index = budget.transaction(url)
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "Accept-Encoding": "identity",
                    "User-Agent": "document-assistant-static-review",
                },
            )
            try:
                response = opener.open(request, timeout=10)
            except urllib.error.HTTPError as error:
                with error:
                    read_body(error, 4096, charge=lambda n, event=index: budget.event(event, n))
                    budget.event(index, status="http_error_" + str(error.code))
                    if error.code in {301, 302, 303, 307, 308} and redirects < 2:
                        url = urllib.parse.urljoin(
                            url, error.headers.get("Location", "")
                        )
                        if not error.headers.get("Location"):
                            raise ValueError("Missing redirect") from None
                        continue
                raise ValueError("HTTP failure or redirect boundary") from None
            with response:
                if (
                    response.headers.get("Content-Encoding", "identity").lower()
                    != "identity"
                ):
                    raise ValueError("Content encoding boundary")
                declared = response.headers.get("Content-Length")
                declared = int(declared) if declared is not None else None
                if declared is not None and not 0 <= declared <= limit:
                    raise ValueError("Declared body limit")
                body = read_body(
                    response,
                    limit,
                    declared if size is None else size,
                    digest,
                    lambda n, event=index: budget.event(event, n),
                )
                if declared is not None and declared != len(body):
                    raise ValueError("Content-Length mismatch")
            budget.event(index, status="body_verified")
            return body
        except Exception:
            budget.event(index, status="stopped_no_retry")
            raise
    raise ValueError("Redirect boundary")


def inspect_wheel(
    blob: bytes, name: str, version: str, tag: str, remaining: int
) -> dict:
    """Validate inert archive inventory, every RECORD entry and identity metadata."""
    files, seen, expanded = {}, set(), 0
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        members = archive.infolist()
        if len(members) > 2000:
            raise ValueError("ZIP member boundary")
        for member in members:
            canonical = safe_name(member.filename)
            mode = (member.external_attr >> 16) & 0o170000
            if (
                canonical in seen
                or mode not in {0, stat.S_IFREG, stat.S_IFDIR}
                or member.external_attr & 0x400
                or member.flag_bits & 1
                or member.compress_type
                not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}
            ):
                raise ValueError("ZIP alias/link/encryption/compression")
            seen.add(canonical)
            if member.is_dir():
                continue
            expanded += member.file_size
            if member.file_size > 16 * MIB or expanded > remaining:
                raise ValueError("ZIP expansion boundary")
        for member in members:
            if not member.is_dir():
                with archive.open(member) as stream:
                    files[member.filename] = read_body(
                        stream,
                        min(16 * MIB, remaining - sum(map(len, files.values()))),
                        member.file_size,
                    )

    def unique(suffix):
        found = [p for p in files if p.endswith(".dist-info/" + suffix)]
        if len(found) != 1:
            raise ValueError("Wheel metadata inventory")
        return found[0]

    record, metadata, wheel = unique("RECORD"), unique("METADATA"), unique("WHEEL")
    if len({p.rsplit("/", 1)[0] for p in (record, metadata, wheel)}) != 1:
        raise ValueError("Wheel dist-info mismatch")
    rows = set()
    for row in csv.reader(io.StringIO(files[record].decode())):
        if len(row) != 3 or row[0] in rows or row[0] not in files:
            raise ValueError("RECORD inventory")
        path, digest, size = row
        rows.add(path)
        if path == record:
            if digest or size:
                raise ValueError("RECORD self identity")
            continue
        algorithm, sep, value = digest.partition("=")
        if not sep or algorithm not in {"sha256", "sha384", "sha512"}:
            raise ValueError("RECORD digest algorithm")
        actual = (
            base64.urlsafe_b64encode(hashlib.new(algorithm, files[path]).digest())
            .rstrip(b"=")
            .decode()
        )
        if actual != value or str(len(files[path])) != size:
            raise ValueError("RECORD integrity")
    if rows != set(files):
        raise ValueError("Unrecorded member")
    parsed = BytesParser().parsebytes(files[metadata])

    def normalize(value):
        return re.sub(r"[-_.]+", "-", value).lower()

    if (
        len(parsed.get_all("Name", [])) != 1
        or len(parsed.get_all("Version", [])) != 1
        or normalize(parsed.get("Name", "")) != normalize(name)
        or parsed.get("Version") != version
        or BytesParser().parsebytes(files[wheel]).get_all("Tag", []) != [tag]
    ):
        raise ValueError("Wheel identity")
    if any(p.lower().endswith(".pth") for p in files):
        raise ValueError("Unexpected startup file")
    return {
        "name": name,
        "version": version,
        "expanded_bytes": expanded,
        "members": len(files),
        "requires_python": parsed.get("Requires-Python"),
        "requires_dist": parsed.get_all("Requires-Dist", []),
        "license": parsed.get("License-Expression", parsed.get("License")),
        "inventory": [
            {"name": p, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
            for p, b in files.items()
        ],
        "entry_points": [p for p in files if p.endswith("entry_points.txt")],
        "native": [p for p in files if p.lower().endswith((".pyd", ".dll", ".exe"))],
        "notices": [
            p
            for p in files
            if any(k in p.lower() for k in ("license", "notice", "copying"))
        ],
    }


def asset_identity(blob: bytes, metadata: dict | None) -> dict:
    """Identify observed bytes separately from publisher-provided Git/LFS hashes."""
    result = {
        "bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
        "publisher_digest_unavailable": True,
    }
    if metadata:
        if metadata.get("size") is not None and metadata["size"] != len(blob):
            raise ValueError("Publisher asset size")
        lfs = metadata.get("lfs")
        if lfs:
            expected = lfs.get("oid", lfs.get("sha256"))
            if expected != result["sha256"]:
                raise ValueError("LFS identity")
            result.update(publisher_digest_unavailable=False, publisher_sha256=expected)
        elif metadata.get("oid"):
            expected = metadata["oid"]
            actual = hashlib.sha1(
                b"blob " + str(len(blob)).encode() + b"\0" + blob
            ).hexdigest()
            if not re.fullmatch("[a-f0-9]{40}", expected) or expected != actual:
                raise ValueError("Git blob identity")
            result["publisher_git_blob"] = expected
    return result


def acquire(budget: Budget) -> None:
    """One finite ordered pass; any refusal preserves partial data and stops."""
    state = budget.state()
    if state["worker_started"]:
        raise ValueError("Worker already started")
    state["worker_started"] = True
    budget.save(state)
    remaining = 32 * MIB
    for name, version, filename, digest, cap, tag in WHEELS:
        registry = json.loads(
            fetch(
                budget,
                f"https://pypi.org/pypi/{name}/{version}/json",
                "metadata",
                MIB - 1,
            )
        )
        info = registry["info"]
        matches = [v for v in registry["urls"] if v["filename"] == filename]
        if (
            info["version"] != version
            or info["name"].replace("_", "-") != name
            or len(matches) != 1
        ):
            raise ValueError("Registry identity")
        item = matches[0]
        if (
            item.get("yanked")
            or item["digests"]["sha256"] != digest
            or not 0 < item["size"] < cap
        ):
            raise ValueError("Registry hash/size/yank")
        blob = fetch(budget, item["url"], "wheel", item["size"], item["size"], digest)
        budget.output(filename, blob)
        result = inspect_wheel(blob, name, version, tag, remaining)
        remaining -= result["expanded_bytes"]
        result.update(
            registry_url=f"https://pypi.org/pypi/{name}/{version}/json",
            payload_url=item["url"],
            sha256=digest,
            bytes=len(blob),
            registry_requires_dist=info.get("requires_dist"),
        )
        budget.report(name + "-inspection.json", result)
    for publisher, revision, files in ASSETS:
        listing = json.loads(
            fetch(
                budget,
                f"https://huggingface.co/api/models/{publisher}/tree/{revision}",
                "metadata",
                MIB - 1,
            )
        )
        if not isinstance(listing, list):
            raise TypeError("Publisher listing shape")
        for filename in files:
            matches = [
                v
                for v in listing
                if v.get("path") == filename and v.get("type") == "file"
            ]
            if len(matches) != 1:
                raise ValueError("Publisher file inventory")
            item = matches[0]
            size = item.get("size")
            if not isinstance(size, int) or not 0 < size < 8 * MIB:
                raise ValueError("Publisher file size")
            blob = fetch(
                budget,
                f"https://huggingface.co/{publisher}/resolve/{revision}/{filename}",
                "asset",
                size,
                size,
            )
            identity = asset_identity(blob, item)
            stored = ("qwen-" if publisher.startswith("Qwen/") else "nomic-") + filename
            budget.output(stored, blob)
            budget.report(
                stored + "-identity.json",
                {
                    "publisher": publisher,
                    "revision": revision,
                    "filename": filename,
                    "status": "static_only_not_approved_for_loading",
                    **identity,
                },
            )


def main() -> None:
    """Production entrypoint is fixed to the approved root; stdout is sanitized."""
    budget = Budget(RUN)
    try:
        acquire(budget)
        budget.report(
            "worker-result.json", {"status": "completed_static_only_no_adoption"}
        )
        print("Static inspection complete; no installation or candidate execution")
    except Exception as error:  # noqa: BLE001 -- terminal receipt, never a retry
        try:
            budget.report(
                "worker-result.json",
                {
                    "status": "stopped_no_retry",
                    "exception": type(error).__name__,
                    "code": str(error)[:160]
                    if isinstance(error, ValueError)
                    else "transport_or_os_failure",
                },
            )
        finally:
            print("Static inspection stopped; no retry")
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
