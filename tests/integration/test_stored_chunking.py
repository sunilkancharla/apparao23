"""Trace real persisted CSV extraction units through the pure T26 transform."""

import asyncio
import json

from app.ingestion.models import NormalizedExtraction, SourceUnit
from app.retrieval.chunking import iter_chunks
from app.retrieval.models import Chunk
from app.storage.documents import Documents
from app.storage.extractions import Extractions
from app.storage.files import UploadStore


def test_stored_csv_chunks_round_trip_and_keep_original_and_readiness(tmp_path):
    body = b'Industry,2024,2025\n"North,\nworks",352361,350764\n'

    async def stream():
        yield body

    store = UploadStore(tmp_path)
    try:
        conversation = Documents(store.connection).create_conversation()
        uploaded = asyncio.run(
            store.receive(stream(), conversation, "upload-chunks-01", "numbers.csv")
        )
        receipt = asyncio.run(
            Extractions(store).extract(
                conversation, uploaded["reference_id"], "extract-chunks-01"
            )
        )
        row = store.connection.execute(
            "SELECT manifest FROM csv_extractions WHERE id=?",
            (receipt["extraction_id"],),
        ).fetchone()
        envelope = NormalizedExtraction.model_validate(
            json.loads(row[0]) | {"units": []}
        )

        def units():
            for row in store.connection.execute(
                "SELECT payload FROM csv_units WHERE extraction_id=? ORDER BY ordinal",
                (receipt["extraction_id"],),
            ):
                yield SourceUnit.model_validate_json(row[0])

        chunks = list(iter_chunks(envelope, units()))
        assert len(chunks) == 1 and isinstance(chunks[0], Chunk)
        chunk = chunks[0]
        assert chunk.source.content_hash == envelope.content_hash
        assert chunk.source.extraction_id == receipt["extraction_id"]
        values = [p for p in chunk.parts if p.role == "data"]
        assert [chunk.text[p.start : p.end] for p in values] == [
            "North,\nworks",
            "352361",
            "350764",
        ]
        assert values[-1].location.columns[0].position == 3
        assert (values[-1].location.line_start, values[-1].location.line_end) == (2, 3)
        assert next((store.root / "originals").iterdir()).read_bytes() == body
        assert receipt["state"] == "awaiting_index" and not receipt["indexed"]
        assert Chunk.model_validate_json(chunk.model_dump_json()) == chunk
    finally:
        store.close()
