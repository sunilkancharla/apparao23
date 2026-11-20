"""Citation quotations must match normalized source spans and genuine locations."""

import hashlib
from dataclasses import replace

import pytest

from app.chat.generation import Answer, Claim
from app.ingestion.models import NormalizedExtraction
from app.ingestion.validation import UploadError
from app.retrieval.chunking import iter_chunks
from app.retrieval.search import Evidence, Hit
from tests.unit.test_chunking import csv_source, prose
from tests.unit.test_provenance_models import extraction


def passages(source):
    from app.chat.citations import checked_passages

    chunk = next(iter_chunks(source))
    units = {u.unit_id: u for u in source.units}
    return chunk, units, checked_passages


@pytest.mark.parametrize("format", ["pdf", "xlsx", "csv"])
def test_passage_quotes_keep_actual_format_coordinates_and_unicode_offsets(format):
    source = NormalizedExtraction.model_validate(extraction(format))
    chunk, units, check = passages(source)
    result = check(chunk, units)
    assert result[0]["quote"] == source.units[0].text
    assert result[0]["location"] == source.units[0].location.model_dump(mode="json")
    assert result[0]["source_start"] == 0
    assert result[0]["source_end"] == len(source.units[0].text)


def test_csv_multiline_cells_headers_and_coarse_missing_values_are_distinct():
    source = csv_source(b'A,B,C\n"North\nworks",42\n')
    chunk, units, check = passages(source)
    result = check(chunk, units)
    data = [r for r in result if r["role"] == "data"]
    assert [r["quote"] for r in data] == ["North\nworks", "42", None]
    assert data[0]["location"]["line_start"] == 2
    assert data[0]["location"]["line_end"] == 3
    assert data[2]["location"]["precision"] == "coarse"
    assert data[2]["location"]["limitation"]


@pytest.mark.parametrize("damage", ["text", "location", "unit", "offset", "parser"])
def test_fabricated_quote_location_unit_offsets_or_parser_are_rejected(damage):
    chunk, units, check = passages(prose("The value is 42."))
    part = chunk.parts[0]
    if damage == "text":
        text = chunk.text.replace("42", "99")
        chunk = chunk.model_copy(
            update={
                "text": text,
                "text_hash": hashlib.sha256(text.encode()).hexdigest(),
            }
        )
    else:
        change = {
            "location": {"location": part.location.model_copy(update={"pages": (99,)})},
            "unit": {"unit_id": "invented"},
            "offset": {"source_end": 99999},
            "parser": {"parser": part.parser.model_copy(update={"version": "fake"})},
        }[damage]
        chunk = chunk.model_copy(update={"parts": (part.model_copy(update=change),)})
    with pytest.raises(UploadError, match="CITATION_INVALID"):
        check(chunk, units)


def test_supplied_citation_allowlist_rejects_unknown_duplicate_and_uncited_claims():
    from app.chat.citations import validate_citations

    chunk = next(iter_chunks(prose("The value is 42.")))
    evidence = Evidence("ev_1", Hit("ref", chunk, 0.0), chunk.text)
    answer = Answer(status="answered", claims=(Claim(text="42", citations=("ev_1",)),))
    validate_citations(answer, (evidence,))
    for ids in (("invented",), ("ev_1", "ev_1"), ()):
        invalid = answer.model_copy(
            update={"claims": (Claim(text="42", citations=ids),)}
        )
        with pytest.raises(UploadError, match="CHAT_RESPONSE_INVALID"):
            validate_citations(invalid, (evidence,))
    with pytest.raises(UploadError, match="CHAT_EVIDENCE_INVALID"):
        validate_citations(answer, (evidence, replace(evidence)))
