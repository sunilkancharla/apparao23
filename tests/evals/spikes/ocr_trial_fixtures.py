"""Offline-only synthetic PDF/raster construction; no user-file dependencies."""

from __future__ import annotations

import hashlib
import html
import io
import json
from pathlib import Path


def materialize(directory: Path, cases: list[dict]) -> None:
    """Build exactly three authored PDFs, ten raster cases and bounded controls."""
    import pypdfium2 as pdfium
    from PIL import Image, ImageEnhance
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import DictionaryObject, NameObject, NumberObject, StreamObject

    directory.mkdir(exist_ok=False)

    def native_page(text):
        writer = PdfWriter()
        page = writer.add_blank_page(width=595.2, height=841.92)
        font = DictionaryObject({NameObject("/Type"): NameObject("/Font"),
                                 NameObject("/Subtype"): NameObject("/Type1"),
                                 NameObject("/BaseFont"): NameObject("/Helvetica")})
        page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"):
            DictionaryObject({NameObject("/F1"): writer._add_object(font)})})
        content = []
        for index, line in enumerate(text.splitlines()):
            escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            content.append(f"BT /F1 24 Tf 40 {760 - index * 55} Td ({escaped}) Tj ET")
        stream = StreamObject()
        stream._data = "\n".join(content).encode("ascii")
        page[NameObject("/Contents")] = writer._add_object(stream)
        page[NameObject("/Rotate")] = NumberObject(0)
        return writer

    native = PdfWriter()
    for case in cases[:2]:
        native.add_page(native_page(case["gold"]).pages[0])
    native.write(directory / "native.pdf")

    def scan_image(text):
        buffer = io.BytesIO()
        native_page(text).write(buffer)
        with pdfium.PdfDocument(buffer.getvalue()) as document:
            page = document[0]
            bitmap = page.render(scale=300 / 72)
            image = bitmap.to_pil().copy().convert("RGB")
            bitmap.close()
            page.close()
            return image

    scan_images = [scan_image(case["gold"]) for case in cases[2:4]]
    scan_images[0].save(directory / "scan.pdf", "PDF", resolution=300,
                        save_all=True, append_images=scan_images[1:])
    mixed = PdfWriter()
    mixed.add_page(PdfReader(directory / "native.pdf").pages[0])
    mixed.add_page(PdfReader(directory / "scan.pdf").pages[0])
    mixed.add_page(PdfReader(directory / "native.pdf").pages[1])
    mixed.write(directory / "mixed.pdf")
    routing_checks = []
    for case in cases[:7]:
        native_text = PdfReader(directory / case["pdf"]).pages[case["page"] - 1].extract_text() or ""
        detected_method = "native" if native_text.strip() else "ocr"
        if detected_method != case["source_method"]:
            raise RuntimeError("Synthetic native/OCR page readiness mismatch")
        routing_checks.append({"case_id": case["id"], "page": case["page"],
                               "method": detected_method, "duplicate_passages": 0})
        with pdfium.PdfDocument(directory / case["pdf"]) as document:
            page = document[case["page"] - 1]
            bitmap = page.render(scale=300 / 72)
            image = bitmap.to_pil().copy()
            if image.width * image.height > 12_000_000:
                raise RuntimeError("Fixture exceeds pixel limit")
            image.save(directory / (case["id"] + ".png"))
            bitmap.close()
            page.close()
    for case in cases[7:]:
        with Image.open(directory / (case["derived_from"] + ".png")) as original:
            image = original.convert("RGB")
        transform = case["transform"]
        if transform.get("rotation"):
            image = image.rotate(transform["rotation"], expand=True, fillcolor="white")
        if "contrast" in transform:
            image = ImageEnhance.Contrast(image).enhance(transform["contrast"])
        if "crop" in transform:
            image = image.crop(tuple(transform["crop"]))
        image.save(directory / (case["id"] + ".png"))
    Image.new("RGB", (200, 100), "white").save(directory / "unreadable.png")
    (directory / "truncated.png").write_bytes(b"\x89PNG\r\n\x1a\ninvalid")
    (directory / "empty.png").write_bytes(b"")
    (directory / "wrong-asset.bin").write_bytes(b"synthetic-invalid-asset")
    rows = ["<!doctype html><meta charset='utf-8'><title>Synthetic fixture review</title>",
            "<p>Review each image against its gold. M08/M09 are deliberate degraded controls.</p>"]
    for case in cases:
        rows.append(f"<h2>{case['id']} — {case['pdf']} page {case['page']}</h2>"
                    f"<pre>{html.escape(case['gold'])}</pre>"
                    f"<img style='max-width:700px' src='{case['id']}.png' alt='{case['id']}'>")
    (directory / "contact-sheet.html").write_text("\n".join(rows), encoding="utf-8")
    manifest = [{"filename": item.name, "bytes": item.stat().st_size,
                 "sha256": hashlib.sha256(item.read_bytes()).hexdigest()}
                for item in directory.iterdir() if item.is_file()]
    if len(manifest) + 1 > 24 or sum(item["bytes"] for item in manifest) > 160 * 1024**2:
        raise RuntimeError("Fixture byte/count budget")
    (directory / "manifest.json").write_text(json.dumps({"cases": cases, "files": manifest,
                                                      "routing_checks": routing_checks},
                                                      indent=2), encoding="utf-8")
