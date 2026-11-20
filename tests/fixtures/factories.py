"""Deterministic authored fixtures; never reads private corpus originals."""

import copy
import hashlib
import io
import json
import zipfile
from datetime import datetime
from pathlib import Path

import httpx

PROJECT = Path(__file__).resolve().parents[2]
MANIFEST = PROJECT / "tests/evals/manifest.json"


def load_definitions() -> dict:
    """Load only approved authored formats; keep charts and historical entries deferred."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["schema_version"] != 1:
        raise ValueError("Unsupported evaluation manifest")
    return {
        item["id"]: copy.deepcopy(item)
        for item in manifest["authored_fixtures"]
        if item.get("stage1_in_scope")
        and item["format"] in {"PDF", "XLSX", "CSV"}
        and item["id"] != "S-CHART"
    }


def _workbook(definition: dict) -> bytes:
    from openpyxl import Workbook

    workbook = Workbook()
    workbook.remove(workbook.active)
    workbook.properties.created = workbook.properties.modified = datetime(2000, 1, 1)
    for sheet in definition["sheets"]:
        target = workbook.create_sheet(sheet["name"])
        for address, value in sheet["cells"].items():
            target[address] = (
                "=" + value["formula"] if isinstance(value, dict) else value
            )
        for merge in sheet.get("merged_ranges", []):
            target.merge_cells(merge)
    buffer = io.BytesIO()
    workbook.save(buffer)
    workbook.close()
    canonical = io.BytesIO()
    with (
        zipfile.ZipFile(buffer) as source,
        zipfile.ZipFile(canonical, "w") as destination,
    ):
        for name in sorted(source.namelist()):
            data = source.read(name)
            if name == "docProps/core.xml":
                import re

                data = re.sub(
                    rb"<dcterms:modified[^>]*>.*?</dcterms:modified>",
                    b'<dcterms:modified xmlns:dcterms="http://purl.org/dc/terms/" xsi:type="dcterms:W3CDTF">2000-01-01T00:00:00Z</dcterms:modified>',
                    data,
                )
            info = zipfile.ZipInfo(name, (2000, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            destination.writestr(info, data)
    return canonical.getvalue()


def _pdf(definition: dict, identity: str) -> bytes:
    from PIL import Image, ImageDraw, ImageFont
    from pypdf import PdfWriter
    from pypdf.generic import (
        DecodedStreamObject,
        DictionaryObject,
        NameObject,
        NumberObject,
    )

    writer = PdfWriter()
    font = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject("/Helvetica"),
        }
    )
    for entry in definition["pages"]:
        page = writer.add_blank_page(width=612, height=792)
        resources = DictionaryObject(
            {
                NameObject("/Font"): DictionaryObject(
                    {NameObject("/F1"): writer._add_object(font)}
                )
            }
        )
        lines = [
            entry[key] for key in ("text", "native_text", "caption") if key in entry
        ]
        if "table" in entry:
            table = entry["table"]
            lines.extend(
                "    ".join(map(str, row)) for row in [table["headers"], *table["rows"]]
            )
        commands = ""
        for index, line in enumerate(lines):
            escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            commands += f"BT /F1 14 Tf 50 {740 - index * 25} Td ({escaped}) Tj ET\n"
        if "image_only_text" in entry or "image_reference" in entry:
            image = Image.new("RGB", (1000, 220), "white")
            draw = ImageDraw.Draw(image)
            if "image_reference" in entry:
                draw.rectangle((80, 110, 180, 210), fill="black")
                draw.rectangle((280, 50, 380, 210), fill="black")
                draw.text(
                    (80, 10),
                    "Q1 100          Q2 160",
                    fill="black",
                    font=ImageFont.load_default(size=24),
                )
            elif not (identity == "S-PDF-SCAN" and entry["number"] == 2):
                draw.text(
                    (30, 50),
                    entry["image_only_text"],
                    fill="black",
                    font=ImageFont.load_default(size=32),
                )
            stream = DecodedStreamObject()
            stream.set_data(image.tobytes())
            stream.update(
                {
                    NameObject("/Type"): NameObject("/XObject"),
                    NameObject("/Subtype"): NameObject("/Image"),
                    NameObject("/Width"): NumberObject(image.width),
                    NameObject("/Height"): NumberObject(image.height),
                    NameObject("/ColorSpace"): NameObject("/DeviceRGB"),
                    NameObject("/BitsPerComponent"): NumberObject(8),
                }
            )
            resources[NameObject("/XObject")] = DictionaryObject(
                {NameObject("/Im1"): writer._add_object(stream.flate_encode())}
            )
            commands += "q 500 0 0 110 50 400 cm /Im1 Do Q\n"
        content = DecodedStreamObject()
        content.set_data(commands.encode("ascii"))
        page[NameObject("/Resources")] = resources
        page[NameObject("/Contents")] = writer._add_object(content)
    result = io.BytesIO()
    writer.write(result)
    writer.close()
    return result.getvalue()


def materialize(root: Path, *, budget) -> dict:
    """Create only synthetic files beneath ignored data/tests fixture roots, without overwrite."""
    from app.config import validate_local_ancestry

    root = root.absolute()
    if ".." in root.parts:
        raise ValueError("Fixture traversal refused")
    validate_local_ancestry(root)
    allowed = (PROJECT / "data", PROJECT / "tests/fixtures/generated")
    if not any(parent == root or parent in root.parents for parent in allowed):
        raise ValueError("Fixtures require an ignored project output root")
    root.mkdir(parents=True, exist_ok=True)
    records = {}
    for identity, item in load_definitions().items():
        format = item["format"].lower()
        definition = item["definition"]
        if format == "csv":
            data = ("\n".join(definition["physical_lines"]) + "\n").encode("utf-8")
        elif format == "xlsx":
            data = _workbook(definition)
        else:
            data = _pdf(definition, identity)
        name = f"{identity}.{format}"
        budget.retain(data)
        with (root / name).open("xb") as stream:
            stream.write(data)
        records[name] = {
            "id": identity,
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
            "expected": copy.deepcopy(item["expected"]),
            "scoring_eligible": False,
        }
        if identity == "S-PDF-SCAN":
            records[name]["control"] = "empty_image_page_2; illegible_text_not_verified"
    # Negative fixtures are deliberately small and never handed to a parser here.
    for name, data in {
        "truncated.pdf": b"%PDF-1.7\n",
        "mismatch.xlsx": b"not a workbook",
        "invalid.csv": b"\xff\xfe\x00",
    }.items():
        budget.retain(data)
        with (root / name).open("xb") as stream:
            stream.write(data)
        records[name] = {
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
            "scoring_eligible": False,
        }
    serialized = json.dumps(records, indent=2, sort_keys=True).encode("utf-8")
    budget.retain(serialized)
    with (root / "ground-truth.json").open("xb") as stream:
        stream.write(serialized)
    return records


def mock_ollama() -> httpx.Client:
    """In-memory transport: synthetic success/missing-model responses, no sockets."""

    def respond(request):
        if request.url.host != "127.0.0.1" or request.url.port != 11435:
            return httpx.Response(403, json={"error": "loopback fixture only"})
        body = json.loads(request.content or b"{}")
        if body.get("model") == "missing":
            return httpx.Response(404, json={"error": "model not found"})
        if request.url.path == "/api/tags":
            return httpx.Response(
                200, json={"models": [{"name": "fixture", "digest": "synthetic"}]}
            )
        if request.url.path == "/api/embed":
            return httpx.Response(200, json={"embeddings": [[0.1, 0.2]]})
        if request.url.path == "/api/chat":
            return httpx.Response(
                200,
                json={
                    "message": {"role": "assistant", "content": "Synthetic response"},
                    "done": True,
                },
            )
        return httpx.Response(404, json={"error": "unknown fixture route"})

    return httpx.Client(
        transport=httpx.MockTransport(respond), trust_env=False, follow_redirects=False
    )
