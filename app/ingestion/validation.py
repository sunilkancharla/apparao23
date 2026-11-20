"""CSV admission checks; source text and display labels never become commands/paths."""

import csv
import io
import re
import unicodedata
from collections.abc import Generator
from typing import BinaryIO
from uuid import UUID

MAX_FILE_BYTES = 100_000_000


class UploadError(ValueError):
    """Safe machine code and HTTP status, without source text or private paths."""

    def __init__(self, code: str, status: int = 422) -> None:
        super().__init__(code)
        self.code, self.status = code, status


def validate_uuid(value: str) -> str:
    """Reject noncanonical IDs without reflecting untrusted route/query text."""
    try:
        if str(UUID(value)) != value:
            raise ValueError
    except ValueError:
        raise UploadError("INVALID_REQUEST") from None
    return value


def validate_filename(name: str) -> str:
    """Accept a plain Windows-safe CSV display label, never a storage path."""
    if (
        not 1 <= len(name) <= 255
        or name != name.strip()
        or name.endswith(".")
        or any(
            c in '<>:"/\\|?*' or unicodedata.category(c).startswith("C") for c in name
        )
        or re.fullmatch(
            r"(?:CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|COM[1-9¹²³]|LPT[1-9¹²³])",
            name.split(".")[0].rstrip(" ."),
            re.IGNORECASE,
        )
    ):
        raise UploadError("INVALID_FILENAME")
    if not name.lower().endswith(".csv"):
        raise UploadError("UNSUPPORTED_FORMAT", 415)
    return name


def validate_csv(source: BinaryIO) -> None:
    """Check the complete UTF-8/BOM comma CSV stream without retaining rows.

    CSV has no authoritative magic signature: single-column text can be CSV.
    This checks syntax, common mismatches and nonempty text, not table semantics.
    Broader dialect/encoding handling and normalized provenance belong to T25/T39.
    """
    for _ in iter_csv_rows(source):
        pass


def iter_csv_rows(
    source: BinaryIO,
) -> Generator[tuple[list[str], int, int], None, None]:
    """Yield validated decoded records with inclusive physical-line spans."""
    source.seek(0)
    prefix = source.read(512).lstrip(b"\xef\xbb\xbf \t\r\n").lower()
    if prefix.startswith(
        (b"%pdf-", b"pk\x03\x04", b"\xd0\xcf\x11\xe0", b"<html", b"<!doctype")
    ):
        raise UploadError("INVALID_CSV")
    source.seek(0)
    previous = csv.field_size_limit(MAX_FILE_BYTES)
    wrapper = io.TextIOWrapper(source, encoding="utf-8-sig", newline="")
    try:
        found = False
        reader = csv.reader(wrapper, strict=True)
        previous_line = 0
        for row in reader:
            for value in row:
                if any(ord(c) < 32 and c not in "\t\r\n" for c in value):
                    raise UploadError("INVALID_CSV")
                found |= bool(value.strip())
            yield row, previous_line + 1, reader.line_num
            previous_line = reader.line_num
        if not found:
            raise UploadError("INVALID_CSV")
    except (UnicodeError, csv.Error):
        raise UploadError("INVALID_CSV") from None
    finally:
        wrapper.detach()
        csv.field_size_limit(previous)
