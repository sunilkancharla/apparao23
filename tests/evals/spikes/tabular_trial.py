"""Bounded Windows T07 comparison; deliberately not an application parser."""

import csv
import hashlib
import json
import os
import posixpath
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile

ROOT = Path(__file__).resolve().parents[3]
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def parse_limited(candidate: str, path: Path) -> dict:
    """Use the inspected T05 job limiter and a persistent sequential trial budget."""
    from pdf_trial import run_limited

    budget_path = ROOT / "data/evals/t07/budget.json"
    budget_path.parent.mkdir(parents=True, exist_ok=True)
    budget = (
        json.loads(budget_path.read_text())
        if budget_path.exists()
        else {"start": time.time(), "workers": 0}
    )
    remaining = 900 - (time.time() - budget["start"])
    if remaining <= 0 or budget["workers"] >= 80:
        raise RuntimeError("Approved trial budget exhausted")
    budget["workers"] += 1
    budget_path.write_text(json.dumps(budget))
    result = run_limited(
        [
            sys.executable,
            "-I",
            "-B",
            str(Path(__file__).resolve()),
            "worker",
            candidate,
            str(path.resolve()),
        ],
        min(60, remaining),
    )
    if result["status"] == "ok":
        result["payload"] = json.loads(result.pop("stdout"))
    else:
        result.pop("stdout", None)
    return result


def archive_xml(path: Path) -> dict:
    """Inspect bounded streams in place; never extract paths or follow relationships."""
    from xml.etree.ElementTree import ParseError

    from defusedxml.common import DefusedXmlException
    from defusedxml.ElementTree import fromstring

    roots = {}
    total = 0
    try:
        with ZipFile(path) as archive:
            members = archive.infolist()
            if len(members) > 2000 or sum(m.file_size for m in members) > 64 * 1024**2:
                return {"error": "archive_budget"}
            names = [m.filename for m in members]
            if len(names) != len(set(names)):
                return {"error": "invalid_archive"}
            for member in members:
                name = member.filename
                if (
                    "\\" in name
                    or ":" in name
                    or PurePosixPath(name).is_absolute()
                    or ".." in PurePosixPath(name).parts
                ):
                    return {"error": "invalid_archive"}
                if member.file_size > 32 * 1024**2:
                    return {"error": "archive_budget"}
                with archive.open(member) as stream:
                    data = stream.read(32 * 1024**2 + 1)
                total += len(data)
                if len(data) > 32 * 1024**2 or total > 64 * 1024**2:
                    return {"error": "archive_budget"}
                if name.endswith((".xml", ".rels")):
                    roots[name] = fromstring(
                        data,
                        forbid_dtd=True,
                        forbid_entities=True,
                        forbid_external=True,
                    )
    except (BadZipFile, EOFError, ValueError, KeyError):
        return {"error": "invalid_archive"}
    except DefusedXmlException:
        return {"error": "unsafe_xml"}
    except ParseError:
        return {"error": "invalid_archive"}
    return {"roots": roots}


def column_number(coordinate: str) -> int:
    """Convert a worksheet's alphabetic column prefix for bounded sampling."""
    value = 0
    for char in coordinate:
        if char.isdigit():
            break
        if not "A" <= char <= "Z":
            raise ValueError("Invalid coordinate")
        value = value * 26 + ord(char) - 64
    return value


def workbook(candidate: str, path: Path) -> dict:
    """Compare lazy workbook reads with directly inspected OOXML cell evidence."""
    checked = archive_xml(path)
    if "error" in checked:
        return checked
    roots = checked["roots"]
    if "xl/workbook.xml" not in roots or "xl/_rels/workbook.xml.rels" not in roots:
        return {"error": "invalid_archive"}
    book = roots["xl/workbook.xml"]
    links = {r.attrib["Id"]: r.attrib for r in roots["xl/_rels/workbook.xml.rels"]}
    strings = ["".join(s.itertext()) for s in roots.get("xl/sharedStrings.xml", [])]
    styles = roots.get("xl/styles.xml")
    custom = (
        {}
        if styles is None
        else {
            int(n.attrib["numFmtId"]): n.attrib["formatCode"]
            for n in styles.findall("m:numFmts/m:numFmt", NS)
        }
    )
    style_ids = (
        []
        if styles is None
        else [
            int(x.attrib.get("numFmtId", 0))
            for x in styles.findall("m:cellXfs/m:xf", NS)
        ]
    )
    properties = book.find("m:workbookPr", NS)
    epoch = (
        datetime(1904, 1, 1)
        if properties is not None and properties.attrib.get("date1904") in {"1", "true"}
        else datetime(1899, 12, 30)
    )
    output = {
        "sheets": [],
        "warnings": [],
        "external_relationships": sum(
            r.attrib.get("TargetMode") == "External"
            for name, root in roots.items()
            if name.endswith(".rels")
            for r in root
        ),
        "sample_limits": [5, 200, 64],
    }
    handles = []
    try:
        if candidate == "openpyxl":
            os.environ["OPENPYXL_LXML"] = "False"
            os.environ["OPENPYXL_DEFUSEDXML"] = "True"
            import openpyxl
            from openpyxl.xml.functions import fromstring, iterparse

            assert openpyxl.DEFUSEDXML and not openpyxl.LXML
            assert fromstring.__module__.startswith(
                "defusedxml"
            ) and iterparse.__module__.startswith("defusedxml")
            handles = [
                openpyxl.load_workbook(
                    path,
                    read_only=True,
                    data_only=value,
                    keep_links=False,
                    keep_vba=False,
                )
                for value in [False, True]
            ]
        sheets = book.findall("m:sheets/m:sheet", NS)
        if len(sheets) > 5:
            output["warnings"].append("sheet_sample_truncated")
        for sheet in sheets[:5]:
            name = sheet.attrib["name"]
            target = links[sheet.attrib[REL]]["Target"]
            member = (
                target.lstrip("/")
                if target.startswith("/")
                else posixpath.normpath(posixpath.join("xl", target))
            )
            if member not in roots or not member.startswith("xl/"):
                return {"error": "invalid_archive"}
            root = roots[member]
            cells = {}
            for cell in root.findall("m:sheetData/m:row/m:c", NS):
                address = cell.attrib["r"]
                row = int("".join(c for c in address if c.isdigit()))
                if row > 200 or column_number(address) > 64:
                    if "cell_sample_truncated" not in output["warnings"]:
                        output["warnings"].append("cell_sample_truncated")
                    continue
                value_node, formula = cell.find("m:v", NS), cell.find("m:f", NS)
                raw = None if value_node is None else value_node.text
                kind = cell.attrib.get("t", "n")
                value = raw
                if kind == "inlineStr":
                    value = "".join(n.text or "" for n in cell.findall("m:is//m:t", NS))
                elif kind == "s" and raw is not None:
                    value = strings[int(raw)]
                elif kind == "b" and raw is not None:
                    value = raw == "1"
                elif kind == "n" and raw is not None:
                    numeric = float(raw)
                    value = int(numeric) if numeric.is_integer() else numeric
                    index = int(cell.attrib.get("s", 0))
                    fmt = style_ids[index] if index < len(style_ids) else 0
                    code = custom.get(fmt, "").lower()
                    if 14 <= fmt <= 22 or ("yy" in code and "d" in code):
                        value = (epoch + timedelta(days=numeric)).isoformat()
                record = {"value": value, "raw": raw, "type": kind}
                if formula is not None:
                    record["formula"] = formula.text or ""
                    if raw is None:
                        output["warnings"].append(
                            f"missing_formula_cache:{name}!{address}"
                        )
                cells[address] = record
            if candidate == "openpyxl":
                formula_sheet, value_sheet = [h[name] for h in handles]
                formula_sheet.reset_dimensions()
                value_sheet.reset_dimensions()
                actual = {}
                for row in value_sheet.iter_rows(max_row=200, max_col=64):
                    for cell in row:
                        if cell.value is not None:
                            value = (
                                cell.value.isoformat()
                                if isinstance(cell.value, (date, datetime))
                                else cell.value
                            )
                            actual[cell.coordinate] = value
                for address, record in cells.items():
                    record["value"] = actual.get(address)
            output["sheets"].append(
                {
                    "name": name,
                    "cells": cells,
                    "merges": [
                        n.attrib["ref"]
                        for n in root.findall("m:mergeCells/m:mergeCell", NS)
                    ],
                }
            )
    finally:
        for handle in handles:
            handle.close()
    return output


def read_csv(path: Path) -> dict:
    """Keep values as strings and logical record IDs separate from physical lines."""
    csv.field_size_limit(1024**2)
    try:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream, strict=True)
            headers = next(reader, [])
            if (
                not headers
                or any(not h for h in headers)
                or len(headers) != len(set(headers))
                or len(headers) > 64
            ):
                return {"error": "invalid_csv"}
            result = {"headers": headers, "records": [], "warnings": []}
            previous = reader.line_num
            for index, values in enumerate(reader, 1):
                if index > 200:
                    result["warnings"].append("record_sample_truncated")
                    break
                if len(values) != len(headers):
                    return {"error": "invalid_csv"}
                result["records"].append(
                    {
                        "data_record": index,
                        "source_row": index + 1,
                        "lines": [previous + 1, reader.line_num],
                        "values": values,
                    }
                )
                previous = reader.line_num
            if not result["records"]:
                return {"error": "invalid_csv"}
            return result
    except UnicodeError:
        return {"error": "invalid_encoding"}
    except csv.Error:
        return {"error": "invalid_csv"}


def extract(candidate: str, path: Path) -> dict:
    """Enforce trial input allowlist; unknown parser errors remain worker failures."""
    if path.stat().st_size > 100 * 1024**2:
        return {"error": "file_budget"}
    if candidate == "csv" and path.suffix.lower() == ".csv":
        return read_csv(path)
    if candidate in {"openpyxl", "xml"} and path.suffix.lower() == ".xlsx":
        return workbook(candidate, path)
    return {"error": "invalid_extension"}


def benchmark(directory: Path) -> None:
    """Run the frozen 40-original comparison; raw data stays in a fresh data folder."""
    directory = directory.resolve()
    directory.relative_to((ROOT / "data").resolve())
    if directory == (ROOT / "data").resolve():
        raise ValueError("Choose a child of data")
    directory.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((ROOT / "tests/evals/manifest.json").read_text())
    sources = [
        s for s in manifest["source_samples"] if s["extension"] in {".csv", ".xlsx"}
    ]
    assert len(sources) == 6
    hashes = {}
    for source in sources:
        path = ROOT / source["path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == source["sha256"]
        hashes[source["id"]] = digest
    record = {
        "sources": hashes,
        "settings": {"sheet_row_column_limits": [5, 200, 64], "repetitions": 4},
        "code": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [
                Path(__file__),
                Path(__file__).with_name("tabular_trial_fixtures.py"),
            ]
        },
        "runs": [],
    }
    for source in sources:
        path = ROOT / source["path"]
        for candidate in ["csv"] if path.suffix == ".csv" else ["xml", "openpyxl"]:
            for repetition in range(4):
                result = parse_limited(candidate, path)
                result.update(
                    source=source["id"], candidate=candidate, repetition=repetition
                )
                record["runs"].append(result)
                serialized = json.dumps(record, ensure_ascii=True, allow_nan=False)
                if len(serialized.encode()) > 256 * 1024**2:
                    raise RuntimeError("Raw result budget exceeded")
                (directory / "results.json").write_text(serialized, encoding="utf-8")
    for source in sources:
        assert (
            hashlib.sha256((ROOT / source["path"]).read_bytes()).hexdigest()
            == hashes[source["id"]]
        )
    assert len(record["runs"]) == 40
    print(
        json.dumps(
            {
                "runs": 40,
                "successful_workers": sum(r["status"] == "ok" for r in record["runs"]),
                "result_bytes": (directory / "results.json").stat().st_size,
            }
        )
    )


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--benchmark":
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        benchmark(Path(sys.argv[2]))
        raise SystemExit(0)
    if len(sys.argv) != 4 or sys.argv[1] != "worker" or input() != "go":
        raise SystemExit(2)
    payload = extract(sys.argv[2], Path(sys.argv[3]))
    output = json.dumps(payload, ensure_ascii=True, allow_nan=False)
    if len(output.encode()) > 8 * 1024**2:
        raise RuntimeError("Trial output budget exceeded")
    print(output)
