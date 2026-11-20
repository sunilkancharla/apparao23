"""Build tiny authored PDFs; original annual reports are never modified."""

from pathlib import Path


def make_fixtures(directory: Path) -> dict[str, Path]:
    """Serialize explicit content streams and a ruled table with known PDF coordinates."""
    import zlib

    from pypdf import PdfReader, PdfWriter

    directory.mkdir(parents=True, exist_ok=True)
    objects: list[bytes] = [b"", b""]

    def add(value: bytes) -> int:
        objects.append(value)
        return len(objects)

    font = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    pixels = zlib.compress(bytes([0, 50, 150, 0, 50, 150, 200, 200, 200, 0, 50, 150]))
    image = add(
        b"<< /Type /XObject /Subtype /Image /Width 2 /Height 2 /ColorSpace /DeviceRGB "
        b"/BitsPerComponent 8 /Filter /FlateDecode /Length "
        + str(len(pixels)).encode()
        + b" >>\nstream\n"
        + pixels
        + b"\nendstream"
    )

    def text(x: int, y: int, value: str) -> str:
        return f"BT /F1 12 Tf {x} {y} Td ({value}) Tj ET\n"

    native = text(50, 750, "Project Cedar budget: 24000 units.")
    table = "".join(f"50 {y} m 250 {y} l S\n" for y in [700, 670, 640, 610])
    table += "".join(f"{x} 610 m {x} 700 l S\n" for x in [50, 150, 250])
    for y, row in [
        (680, ("Quarter", "Revenue")),
        (650, ("Q1", "100")),
        (620, ("Q2", "160")),
    ]:
        table += text(60, y, row[0]) + text(160, y, row[1])
    table += "q 60 0 0 60 300 640 cm /Im1 Do Q\n"
    columns = "".join(
        text(x, y, value)
        for x, y, value in [
            (50, 750, "Left A"),
            (50, 730, "Left B"),
            (320, 750, "Right A"),
            (320, 730, "Right B"),
        ]
    )
    page_ids = []
    for content in [native, table, "", "q 60 0 0 60 300 640 cm /Im1 Do Q\n", columns]:
        stream = content.encode("ascii")
        stream_id = add(
            b"<< /Length "
            + str(len(stream)).encode()
            + b" >>\nstream\n"
            + stream
            + b"endstream"
        )
        page_ids.append(
            add(
                (
                    f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                    f"/Resources << /Font << /F1 {font} 0 R >> /XObject << /Im1 {image} 0 R >> >> "
                    f"/Contents {stream_id} 0 R >>"
                ).encode()
            )
        )
    objects[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objects[1] = (
        "<< /Type /Pages /Count 5 /Kids ["
        + " ".join(f"{i} 0 R" for i in page_ids)
        + "] >>"
    ).encode()
    document = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, value in enumerate(objects, 1):
        offsets.append(len(document))
        document.extend(f"{number} 0 obj\n".encode() + value + b"\nendobj\n")
    xref = len(document)
    document.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        document.extend(f"{offset:010} 00000 n \n".encode())
    document.extend(
        f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    )
    paths = {
        name: directory / filename
        for name, filename in {
            "native": "controlled.pdf",
            "protected": "protected.pdf",
            "malformed": "malformed.pdf",
            "truncated": "truncated.pdf",
            "wrong_extension": "wrong.txt",
        }.items()
    }
    paths["native"].write_bytes(document)
    writer = PdfWriter()
    writer.append(PdfReader(paths["native"]))
    writer.encrypt("evaluation-only-password", algorithm="AES-256")
    writer.write(paths["protected"])
    paths["malformed"].write_bytes(b"%PDF-1.4\nnot a PDF object tree\n%%EOF")
    paths["truncated"].write_bytes(document[:100])
    paths["wrong_extension"].write_bytes(document)
    return paths
