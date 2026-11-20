"""Approved observable support states never claim independent semantic accuracy."""

import copy
import json

import pytest


def saved():
    return {
        "state": "complete",
        "answer": {
            "status": "answered",
            "claims": [{"text": "42 units", "citations": ["ev_1"]}],
        },
        "evidence": [
            {
                "evidence_id": "ev_1",
                "locations": [{"precision": "exact"}],
                "warnings": [],
            }
        ],
        "citations": [
            {
                "citation_id": "ev_1",
                "availability": "available",
                "code": None,
                "warning_codes": [],
                "methods": ["native"],
                "precisions": ["exact"],
                "ocr_confidence_available": None,
            }
        ],
        "warnings": [],
        "completed_at": "2026-11-20T00:00:00+00:00",
        "error_code": None,
        "source_availability": "available",
    }


def indicator(value=None, **kwargs):
    from app.chat.evidence import evidence_support

    return evidence_support(saved() if value is None else value, **kwargs)


def codes(result):
    return {w["code"] for w in result["warnings"]}


def test_structural_resolution_does_not_verify_a_doubled_budget_claim():
    value = saved()
    value["answer"]["claims"][0]["text"] = "The budget doubled."
    result = indicator(value, input_fit_verified=True)
    assert result["state"] == "citations_resolved"
    assert result["label"] == "Citations checked; meaning not independently verified"
    assert result["semantic_support"] == "not_independently_verified"
    assert result["coverage"] == {
        "applicability": "declared_blocks",
        "declared_blocks": 1,
        "blocks_with_supplied_citations": 1,
        "blocks_with_checked_citations": 1,
        "blocks_without_citations": 0,
    }
    assert not ({"accuracy", "confidence", "score", "percentage"} & result.keys())


def test_current_unknown_context_fit_stays_incomplete_despite_checked_citations():
    result = indicator()
    assert result["state"] == "incomplete"
    assert result["checks"]["locations_and_quotes"] == "checked"
    assert result["checks"]["input_fit"] == "unverified"
    assert "INPUT_FIT_UNVERIFIED" in result["issues"]


@pytest.mark.parametrize(
    "code,state",
    [
        ("SOURCE_CHANGED", "unavailable"),
        ("OLLAMA_TIMEOUT", "unavailable"),
        ("GENERATION_INCOMPLETE", "incomplete"),
        ("CHAT_RESPONSE_INVALID", "incomplete"),
        ("OLLAMA_RESPONSE_INVALID", "incomplete"),
        ("CHAT_EVIDENCE_INVALID", "citation_problem"),
    ],
)
def test_failed_operation_preserves_failure_instead_of_successful_no_evidence(
    code, state
):
    value = saved()
    value.update(
        state="failed",
        error_code=code,
        answer=None,
        evidence=[],
        citations=[],
        warnings=["NO_EVIDENCE"],
        completed_at=None,
    )
    assert indicator(value)["state"] == state


def test_successful_no_evidence_has_no_model_completion_or_coverage_requirement():
    value = saved()
    value.update(
        evidence=[], citations=[], warnings=["NO_EVIDENCE", "INPUT_FIT_UNVERIFIED"]
    )
    value["answer"] = {
        "status": "insufficient_evidence",
        "claims": [{"text": "No usable selected evidence.", "citations": []}],
    }
    result = indicator(value)
    assert result["state"] == "no_evidence"
    assert result["coverage"]["applicability"] == "not_applicable"
    assert result["coverage"]["declared_blocks"] is None
    assert result["checks"]["input_fit"] == "not_applicable"


def test_processing_answer_is_incomplete_with_no_invented_coverage():
    value = saved()
    value.update(
        state="processing", answer=None, evidence=[], citations=[], completed_at=None
    )
    result = indicator(value)
    assert result["state"] == "incomplete"
    assert result["coverage"]["declared_blocks"] is None


@pytest.mark.parametrize(
    "status,state",
    [("clarification", "clarification"), ("insufficient_evidence", "abstained")],
)
def test_uncited_clarification_and_abstention_have_na_coverage(status, state):
    value = saved()
    value["answer"] = {
        "status": status,
        "claims": [{"text": "Please clarify the period.", "citations": []}],
    }
    value["citations"] = []
    result = indicator(value, input_fit_verified=True)
    assert result["state"] == state
    assert result["coverage"]["declared_blocks"] is None
    assert result["checks"]["citation_ids"] == "not_applicable"


def test_declared_block_coverage_counts_missing_citations_without_semantic_grading():
    value = saved()
    value["answer"]["claims"].append(
        {"text": "Another factual block.", "citations": []}
    )
    result = indicator(value, input_fit_verified=True)
    assert result["state"] == "citations_missing"
    assert result["coverage"]["declared_blocks"] == 2
    assert result["coverage"]["blocks_with_checked_citations"] == 1
    assert result["coverage"]["blocks_without_citations"] == 1


@pytest.mark.parametrize(
    "damage",
    [
        "unknown",
        "duplicate_claim",
        "duplicate_manifest",
        "duplicate_check",
        "quote_invalid",
    ],
)
def test_unknown_duplicate_or_invalid_citations_never_become_resolved(damage):
    value = saved()
    if damage == "unknown":
        value["answer"]["claims"][0]["citations"] = ["ev_foreign"]
    elif damage == "duplicate_claim":
        value["answer"]["claims"][0]["citations"] *= 2
    elif damage == "duplicate_manifest":
        value["evidence"] *= 2
    elif damage == "duplicate_check":
        value["citations"] *= 2
    else:
        value["citations"][0].update(
            availability="unavailable", code="CITATION_INVALID"
        )
    result = indicator(value, input_fit_verified=True)
    assert result["state"] == "citation_problem"
    assert (
        result["checks"]["citation_ids"] == "invalid"
        or result["checks"]["locations_and_quotes"] == "invalid"
    )


def test_mixed_source_availability_counts_only_fully_checked_blocks():
    value = saved()
    value["evidence"].append({"evidence_id": "ev_2", "warnings": [], "locations": []})
    value["answer"]["claims"].append({"text": "South", "citations": ["ev_2"]})
    value["citations"].append(
        {
            "citation_id": "ev_2",
            "availability": "unavailable",
            "code": "SOURCE_UNAVAILABLE",
        }
    )
    result = indicator(value, input_fit_verified=True)
    assert result["state"] == "unavailable"
    assert result["coverage"]["blocks_with_checked_citations"] == 1
    assert "SOURCE_UNAVAILABLE" in result["issues"]


def test_partial_answer_and_independent_ocr_extraction_warnings_stay_visible():
    value = saved()
    value["answer"]["status"] = "partial"
    value["warnings"] = [
        "EVIDENCE_BUDGET",
        "SOURCE_CONFLICT",
        "MISSING_FORMULA_CACHE",
        "LOW_OCR_CONFIDENCE",
    ]
    value["citations"][0].update(
        methods=["ocr"], precisions=["coarse"], ocr_confidence_available=False
    )
    result = indicator(value, input_fit_verified=True)
    assert result["state"] == "citations_resolved"
    assert {
        "PARTIAL_ANSWER",
        "OCR_DERIVED_TEXT",
        "OCR_CONFIDENCE_UNAVAILABLE",
        "COARSE_LOCATION",
        "EVIDENCE_BUDGET",
        "SOURCE_CONFLICT",
        "MISSING_FORMULA_CACHE",
        "LOW_OCR_CONFIDENCE",
    } <= codes(result)


def test_absent_live_checks_are_explicitly_unrevalidated_not_a_success_or_failure():
    value = saved()
    value.pop("citations")
    value["source_availability"] = "not_revalidated"
    result = indicator(value, input_fit_verified=True)
    assert result["state"] == "incomplete"
    assert result["checks"]["locations_and_quotes"] == "not_revalidated"


def test_hard_failure_keeps_all_other_detected_issues_and_warnings():
    value = saved()
    value["warnings"] = ["SOURCES_UNAVAILABLE", "INPUT_TRUNCATED", "LOW_OCR_CONFIDENCE"]
    value["answer"]["claims"][0]["citations"] = ["foreign"]
    result = indicator(value)
    assert result["state"] == "unavailable"
    assert {
        "SOURCE_UNAVAILABLE",
        "CITATION_INVALID",
        "INPUT_FIT_UNVERIFIED",
        "INPUT_TRUNCATED",
    } <= set(result["issues"])
    assert "LOW_OCR_CONFIDENCE" in codes(result)


def test_model_claims_and_untrusted_warning_text_are_not_indicator_authority():
    value = saved()
    value["semantic_support"] = "verified"
    value["confidence"] = 0.99
    value["warnings"] = ["private source contents <script>"]
    value["answer"]["claims"][0]["text"] = "Model certifies this is 99% correct."
    before = copy.deepcopy(value)
    result = indicator(value, input_fit_verified=True)
    serialized = json.dumps(result)
    assert "99%" not in serialized and "private source" not in serialized
    assert "OTHER_SOURCE_WARNING" in codes(result)
    assert result["semantic_support"] == "not_independently_verified"
    assert value == before


@pytest.mark.parametrize(
    "warning,state",
    [
        ("GENERATION_INCOMPLETE", "incomplete"),
        ("RESPONSE_INVALID", "incomplete"),
        ("SOURCE_TIMEOUT", "incomplete"),
        ("CITATION_INVALID", "citation_problem"),
        ("SOURCE_UNAVAILABLE", "unavailable"),
    ],
)
def test_failure_warnings_cannot_become_a_resolved_success(warning, state):
    value = saved()
    value["warnings"] = [warning]
    result = indicator(value, input_fit_verified=True)
    assert result["state"] == state
    assert warning in codes(result)


def test_missing_completion_record_remains_incomplete_even_with_resolved_ids():
    value = saved()
    value["completed_at"] = None
    assert indicator(value, input_fit_verified=True)["state"] == "incomplete"


def test_empty_evidence_alone_does_not_prove_successful_pre_generation_abstention():
    value = saved()
    value["evidence"] = value["citations"] = []
    value["answer"] = {
        "status": "insufficient_evidence",
        "claims": [{"text": "Cannot answer.", "citations": []}],
    }
    assert indicator(value, input_fit_verified=True)["state"] == "abstained"
