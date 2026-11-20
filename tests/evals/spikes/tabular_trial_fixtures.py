"""Tiny independent OOXML/CSV controls generated only in ignored temporary data."""

import json
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


def make_fixtures(directory: Path) -> dict[str, Path]:
    """Serialize authored T02R definitions without workbook libraries or Office."""
    directory.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(Path("tests/evals/manifest.json").read_text())
    fixtures = {f["id"]: f for f in manifest["authored_fixtures"]}
    main = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    rel = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    package = "http://schemas.openxmlformats.org/package/2006/relationships"
    parts = {
        "[Content_Types].xml": '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/></Types>',
        "_rels/.rels": f'<Relationships xmlns="{package}"><Relationship Id="rId1" Type="{rel}/officeDocument" Target="xl/workbook.xml"/></Relationships>',
        "xl/styles.xml": f'<styleSheet xmlns="{main}"><fonts count="1"><font/></fonts><fills count="1"><fill><patternFill/></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs><cellXfs count="2"><xf numFmtId="0"/><xf numFmtId="14" applyNumberFormat="1"/></cellXfs></styleSheet>',
    }
    definitions = fixtures["S-XLSX"]["definition"]["sheets"]
    names, relationships = [], []
    for index, sheet in enumerate(definitions, 1):
        names.append(
            f'<sheet name="{sheet["name"]}" sheetId="{index}" r:id="rId{index}"/>'
        )
        relationships.append(
            f'<Relationship Id="rId{index}" Type="{rel}/worksheet" Target="worksheets/sheet{index}.xml"/>'
        )
        cells = dict(sheet["cells"])
        if index == 1:
            # Additional independent date control; the T02R definition is unchanged.
            cells["C2"] = 46068
        rows: dict[int, list[str]] = {}
        for coordinate, value in cells.items():
            number = int("".join(c for c in coordinate if c.isdigit()))
            if isinstance(value, dict):
                content = (
                    f'<c r="{coordinate}"><f>{escape(value["formula"])}</f><v/></c>'
                )
            elif isinstance(value, str):
                content = f'<c r="{coordinate}" t="inlineStr"><is><t>{escape(value)}</t></is></c>'
            else:
                style = ' s="1"' if coordinate == "C2" else ""
                content = f'<c r="{coordinate}"{style}><v>{value}</v></c>'
            rows.setdefault(number, []).append(content)
        xml_rows = "".join(
            f'<row r="{n}">{"".join(cs)}</row>' for n, cs in sorted(rows.items())
        )
        merges = "".join(
            f'<mergeCell ref="{r}"/>' for r in sheet.get("merged_ranges", [])
        )
        parts[f"xl/worksheets/sheet{index}.xml"] = (
            f'<worksheet xmlns="{main}"><dimension ref="A1:A1"/><sheetData>{xml_rows}</sheetData><mergeCells>{merges}</mergeCells></worksheet>'
        )
    parts["xl/workbook.xml"] = (
        f'<workbook xmlns="{main}" xmlns:r="{rel}"><sheets>{"".join(names)}</sheets></workbook>'
    )
    relationships.append(
        f'<Relationship Id="style" Type="{rel}/styles" Target="styles.xml"/>'
    )
    parts["xl/_rels/workbook.xml.rels"] = (
        f'<Relationships xmlns="{package}">{"".join(relationships)}</Relationships>'
    )
    parts["xl/worksheets/_rels/sheet1.xml.rels"] = (
        f'<Relationships xmlns="{package}"><Relationship Id="external" Type="{rel}/hyperlink" Target="https://example.invalid/do-not-fetch" TargetMode="External"/></Relationships>'
    )
    paths = {}
    for key in ["xlsx", "traversal", "entity", "duplicate", "oversized"]:
        path = directory / f"{key}.xlsx"
        with ZipFile(path, "w", ZIP_DEFLATED) as archive:
            for name, value in parts.items():
                archive.writestr(name, value)
            if key == "traversal":
                archive.writestr("../escape.xml", "<x/>")
            if key == "entity":
                archive.writestr(
                    "inert.xml", '<!DOCTYPE x [<!ENTITY a "inert">]><x>&a;</x>'
                )
            if key == "duplicate":
                archive.writestr("inert.xml", "<x/>")
                archive.writestr("inert.xml", "<x/>")
            if key == "oversized":
                # Many tiny members exercise the count boundary, never a ZIP bomb.
                for n in range(2001):
                    archive.writestr(ZipInfo(f"small/{n}"), b"")
        paths[key] = path
    paths["corrupt"] = directory / "corrupt.xlsx"
    paths["corrupt"].write_bytes(b"not a workbook")
    for key, fixture_id in [("csv", "S-CSV"), ("injection", "S-CSV-INJECTION")]:
        path = directory / f"{key}.csv"
        path.write_text(
            "\n".join(fixtures[fixture_id]["definition"]["physical_lines"]) + "\n",
            encoding="utf-8",
            newline="",
        )
        paths[key] = path
    for key, content in {
        "bad_encoding": b"A,B\n\xff,1\n",
        "bad_quotes": b'A,B\n"not closed,1\n',
        "bad_headers": b"A,A\n1,2\n",
        "long_field": b"A\n" + b"x" * (1024**2 + 1),
    }.items():
        paths[key] = directory / f"{key}.csv"
        paths[key].write_bytes(content)
    return paths
