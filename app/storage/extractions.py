"""Scoped CSV generations commit atomically; preview material is separately bounded."""

import asyncio
import hashlib
import html
import json
import sqlite3
from typing import TYPE_CHECKING
from uuid import uuid4

from app.ingestion.csv import (
    EXTRACTION_VERSION,
    NORMALIZATION_VERSION,
    PARSER,
    CsvExtractor,
)
from app.ingestion.models import NormalizedExtraction, SourceUnit
from app.ingestion.validation import UploadError

if TYPE_CHECKING:
    from app.storage.files import UploadStore


def _clip(value: str | None) -> tuple[str | None, bool]:
    if value is None:
        return None, False
    encoded = value.encode("utf-8")
    clipped = encoded[:256].decode("utf-8", errors="ignore")
    return html.escape(clipped, quote=True), len(encoded) > 256


def _preview_unit(unit: SourceUnit) -> str:
    header, header_cut = _clip(unit.cells[0].text)
    value, value_cut = _clip(unit.cells[1].text)
    location = unit.location
    return json.dumps(
        {
            "unit_id": unit.unit_id,
            "record": location.record_start,
            "column": location.columns[0].position,
            "line_start": location.line_start,
            "line_end": location.line_end,
            "precision": location.precision,
            "limitation": location.limitation,
            "header": header,
            "value": value,
            "header_truncated": header_cut,
            "value_truncated": value_cut,
            "header_line_start": unit.cells[0].location.line_start,
            "header_line_end": unit.cells[0].location.line_end,
            "header_precision": unit.cells[0].location.precision,
            "header_limitation": unit.cells[0].location.limitation,
            "warning_codes": unit.warnings,
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )


def recover_extractions(store: "UploadStore") -> None:
    """Resolve the single interrupted intent after SQLite's journal rollback."""
    pending = store.connection.execute(
        "SELECT id FROM csv_extractions WHERE state='processing' LIMIT 1"
    ).fetchone()
    if pending is None:
        return
    try:
        with store._write():
            if store.connection.execute(
                "SELECT 1 FROM csv_units WHERE extraction_id=? LIMIT 1", (pending[0],)
            ).fetchone():
                raise UploadError("EXTRACTION_RECOVERY_PENDING", 503)
            store.connection.execute(
                "UPDATE csv_extractions SET state='failed',error_code='EXTRACTION_INTERRUPTED' WHERE id=?",
                (pending[0],),
            )
    except (UploadError, OSError, sqlite3.Error):
        store.recovery_pending = True


class Extractions:
    """Own only CSV-derived metadata; never delete or rewrite original documents."""

    def __init__(self, store: "UploadStore") -> None:
        self.store, self.connection = store, store.connection

    def _source(self, conversation: str, reference: str) -> sqlite3.Row:
        row = self.connection.execute(
            """SELECT d.id AS document_id,d.content_hash,c.byte_size,c.format,u.display_name
            FROM document_references r JOIN documents d ON d.id=r.document_id
            JOIN content_objects c ON c.sha256=d.content_hash
            LEFT JOIN uploads u ON u.document_id=d.id AND u.state='original_stored'
            WHERE r.id=? AND r.conversation_id=?""",
            (reference, conversation),
        ).fetchone()
        if row is None:
            raise UploadError("SOURCE_NOT_FOUND", 404)
        if row["format"] != "csv":
            raise UploadError("UNSUPPORTED_FORMAT", 415)
        if row["display_name"] is None:
            raise UploadError("SOURCE_UNAVAILABLE", 410)
        return row

    def _complete(self, document: str) -> sqlite3.Row | None:
        return self.connection.execute(
            """SELECT * FROM csv_extractions WHERE document_id=? AND state='complete'
            AND extraction_version=? AND normalization_version=? AND parser_version=?""",
            (document, EXTRACTION_VERSION, NORMALIZATION_VERSION, PARSER.version),
        ).fetchone()

    @staticmethod
    def _receipt(row: sqlite3.Row) -> dict:
        return {
            "operation_id": row["id"],
            "extraction_id": row["id"],
            "document_id": row["document_id"],
            "state": "awaiting_index",
            "indexed": False,
            "ready": False,
            "record_count": row["record_count"],
            "unit_count": row["unit_count"],
            "warning_codes": json.loads(row["manifest"])["warnings"],
        }

    async def extract(self, conversation: str, reference: str, key: str) -> dict:
        """Claim an idempotent intent, then publish all normalized cells in one commit."""
        source = self._source(conversation, reference)
        if self.store.busy or self.store.recovery_pending:
            raise UploadError("UPLOAD_BUSY", 409)
        self.store.busy = True
        generation = None
        try:
            path = await asyncio.to_thread(
                self.store._verified_original,
                source["content_hash"],
                source["byte_size"],
            )
            key_hash = hashlib.sha256(key.encode("ascii")).hexdigest()
            with self.store._write():
                previous = self.connection.execute(
                    """SELECT e.* FROM csv_requests r JOIN csv_extractions e ON e.id=r.extraction_id
                    WHERE r.reference_id=? AND r.key_hash=?""",
                    (reference, key_hash),
                ).fetchone()
                if previous is not None:
                    if previous["state"] != "complete":
                        raise UploadError(
                            previous["error_code"] or "EXTRACTION_PENDING", 409
                        )
                    return self._receipt(previous)
                completed = self._complete(source["document_id"])
                if completed is None:
                    if self.connection.execute(
                        "SELECT 1 FROM csv_extractions WHERE state='processing'"
                    ).fetchone():
                        raise UploadError("EXTRACTION_PENDING", 409)
                    generation = str(uuid4())
                    manifest = NormalizedExtraction(
                        document_id=source["document_id"],
                        content_hash=source["content_hash"],
                        filename=source["display_name"],
                        format="csv",
                        extraction_id=generation,
                        extraction_version=EXTRACTION_VERSION,
                        normalization_version=NORMALIZATION_VERSION,
                        units=(),
                    )
                    self.connection.execute(
                        """INSERT INTO csv_extractions
                        (id,document_id,extraction_version,normalization_version,parser_version,state,manifest)
                        VALUES (?,?,?,?,?,'processing',?)""",
                        (
                            generation,
                            source["document_id"],
                            EXTRACTION_VERSION,
                            NORMALIZATION_VERSION,
                            PARSER.version,
                            manifest.model_dump_json(exclude={"units"}),
                        ),
                    )
                target = generation if completed is None else completed["id"]
                self.connection.execute(
                    "INSERT INTO csv_requests VALUES (?,?,?,?)",
                    (str(uuid4()), reference, key_hash, target),
                )
            if completed is not None:
                return self._receipt(completed)
            with path.open("rb") as stream:
                parser = CsvExtractor(stream, generation)
                units = iter(parser)
                try:
                    with self.store._write():
                        for ordinal, unit in enumerate(units, 1):
                            payload, preview = (
                                unit.model_dump_json(),
                                _preview_unit(unit),
                            )
                            self.store.reserve_growth(
                                len(payload.encode("utf-8"))
                                + len(preview.encode("utf-8"))
                            )
                            self.connection.execute(
                                "INSERT INTO csv_units VALUES (?,?,?,?,?)",
                                (generation, ordinal, unit.unit_id, payload, preview),
                            )
                            if ordinal % 64 == 0:
                                await asyncio.sleep(0)
                        await asyncio.to_thread(
                            self.store._verified_original,
                            source["content_hash"],
                            source["byte_size"],
                        )
                        manifest = manifest.model_copy(
                            update={"warnings": tuple(sorted(parser.warnings))}
                        )
                        self.connection.execute(
                            """UPDATE csv_extractions SET state='complete',manifest=?,record_count=?,unit_count=? WHERE id=?""",
                            (
                                manifest.model_dump_json(exclude={"units"}),
                                parser.record_count,
                                parser.unit_count,
                                generation,
                            ),
                        )
                finally:
                    units.close()
            row = self.connection.execute(
                "SELECT * FROM csv_extractions WHERE id=?", (generation,)
            ).fetchone()
            return self._receipt(row)
        except BaseException as error:
            if (
                generation is not None
                and self.connection.execute(
                    "SELECT 1 FROM csv_extractions WHERE id=? AND state='processing'",
                    (generation,),
                ).fetchone()
            ):
                try:
                    with self.store._write():
                        self.connection.execute(
                            "UPDATE csv_extractions SET state='failed',error_code=? WHERE id=?",
                            (
                                error.code
                                if isinstance(error, UploadError)
                                else "EXTRACTION_INTERRUPTED",
                                generation,
                            ),
                        )
                except Exception:  # noqa: BLE001 - keep unresolved intent visible and block admission
                    self.store.recovery_pending = True
                    raise UploadError("EXTRACTION_PENDING", 503) from None
            if isinstance(error, UploadError) or not isinstance(error, Exception):
                raise
            raise UploadError("EXTRACTION_FAILED", 503) from None
        finally:
            self.store.busy = False

    async def preview(
        self, conversation: str, reference: str, *, after: int = 0, limit: int = 20
    ) -> dict:
        """Return at most 50 escaped cell snippets within a 64 KiB JSON budget."""
        source = self._source(conversation, reference)
        if (
            type(after) is not int
            or not 0 <= after <= 2**63 - 1
            or type(limit) is not int
            or not 1 <= limit <= 50
        ):
            raise UploadError("INVALID_REQUEST")
        if self.store.busy or self.store.recovery_pending:
            raise UploadError("UPLOAD_BUSY", 409)
        self.store.busy = True
        try:
            await asyncio.to_thread(
                self.store._verified_original,
                source["content_hash"],
                source["byte_size"],
            )
            completed = self._complete(source["document_id"])
            if completed is None:
                raise UploadError("EXTRACTION_REQUIRED", 409)
            manifest = json.loads(completed["manifest"])
            result = {
                "document_id": source["document_id"],
                "reference_id": reference,
                "extraction_id": completed["id"],
                "filename": source["display_name"],
                "format": "csv",
                "extraction_version": completed["extraction_version"],
                "normalization_version": completed["normalization_version"],
                "parser_version": completed["parser_version"],
                "record_count": completed["record_count"],
                "unit_count": completed["unit_count"],
                "warning_codes": manifest["warnings"],
                "escaped": True,
                "units": [],
                "next_after": None,
            }
            rows = self.connection.execute(
                "SELECT ordinal,preview FROM csv_units WHERE extraction_id=? AND ordinal>? ORDER BY ordinal LIMIT ?",
                (completed["id"], after, limit + 1),
            ).fetchall()
            for row in rows[:limit]:
                candidate = json.loads(row["preview"]) | {"ordinal": row["ordinal"]}
                result["units"].append(candidate)
                result["next_after"] = row["ordinal"]
                if (
                    len(
                        json.dumps(
                            {"data": result}, ensure_ascii=False, separators=(",", ":")
                        ).encode("utf-8")
                    )
                    > 65_536
                ):
                    result["units"].pop()
                    break
            more = len(rows) > len(result["units"])
            if more and not result["units"]:
                raise UploadError("PREVIEW_LIMIT", 503)
            result["next_after"] = result["units"][-1]["ordinal"] if more else None
            return result
        finally:
            self.store.busy = False
