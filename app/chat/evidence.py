"""Observable citation checks and declared-block coverage, never a meaning score."""

import re

from app.chat.generation import Answer

LABELS = {
    "unavailable": "Evidence could not be checked",
    "incomplete": "Answer incomplete",
    "citation_problem": "Citation could not be validated",
    "no_evidence": "No usable evidence in selected documents",
    "citations_missing": "Some statements have no citation",
    "citations_resolved": "Citations checked; meaning not independently verified",
    "clarification": "Clarification requested",
    "abstained": "Insufficient evidence to answer",
}
WARNINGS = {
    "SEMANTIC_SUPPORT_UNVERIFIED": "Meaning has not been independently verified.",
    "INPUT_FIT_UNVERIFIED": "Complete model input fit has not been verified.",
    "TOKEN_FIT_UNVERIFIED": "Retrieved evidence byte limits do not prove model input fit.",
    "INPUT_TRUNCATED": "Input truncation was reported; the answer is incomplete.",
    "GENERATION_INCOMPLETE": "A complete generation result is unavailable.",
    "RESPONSE_INVALID": "The model response could not be validated.",
    "OPERATION_PENDING": "The answer operation has not completed.",
    "OPERATION_FAILED": "The answer operation failed.",
    "SOURCE_UNAVAILABLE": "A required source could not be checked.",
    "SOURCES_UNAVAILABLE": "One or more selected sources are unavailable.",
    "CITATION_INVALID": "A citation identifier, location or quotation failed validation.",
    "CITATIONS_NOT_REVALIDATED": "Current citation locations and quotations have not been revalidated.",
    "CITATIONS_MISSING": "Some declared answer blocks have no citation.",
    "NO_EVIDENCE": "Pre-generation checks found no usable selected evidence.",
    "PARTIAL_ANSWER": "The answer is partial.",
    "OCR_DERIVED_TEXT": "Some supplied text was recognized by OCR.",
    "OCR_CONFIDENCE_UNAVAILABLE": "OCR recognition confidence is unavailable.",
    "LOW_OCR_CONFIDENCE": "Extraction reported low OCR recognition quality; this is not answer correctness.",
    "COARSE_LOCATION": "Some source locations have coarse precision.",
    "LOCATION_UNAVAILABLE": "Some source coordinates are unavailable.",
    "EVIDENCE_BUDGET": "Some evidence was omitted to fit the request byte limits.",
    "INDEX_OMISSIONS": "Some source material was omitted from the current index.",
    "HISTORY_OMITTED": "Some historical context was omitted from the request.",
    "SOURCE_CONFLICT": "A source conflict was reported; no precedence is assumed.",
    "MISSING_FORMULA_CACHE": "Some formula cells lack stored results; formulas were not executed.",
    "MISSING_CELL": "A source record has a missing cell.",
    "MISSING_HEADER": "A source column has no header.",
    "DUPLICATE_HEADERS": "Some source headers are duplicated; positions distinguish them.",
    "ROW_WIDTH_MISMATCH": "Some records have a different number of columns.",
    "SOURCE_UNIT_SPLIT": "A source passage was split at complete boundaries.",
    "TABLE_ROW_SPLIT": "A table row was split with its declared context.",
    "DISTANCE_TIE": "Retrieved candidates have tied distances; distance is not support.",
    "ANSWERABILITY_UNASSESSED": "Retrieval did not establish that the question is answerable.",
    "PREVIEW_LIMIT": "A live preview exceeded its response budget.",
    "SOURCE_TIMEOUT": "Current source checks did not finish within their boundary.",
    "OUTPUT_LIMIT_REACHED": "The model output limit was reached.",
    "OTHER_SOURCE_WARNING": "An additional source or processing limitation was reported.",
}
INCOMPLETE_ERRORS = {
    "GENERATION_INCOMPLETE",
    "CHAT_RESPONSE_INVALID",
    "OLLAMA_RESPONSE_INVALID",
    "CHAT_INPUT_TOO_LARGE",
    "PREVIEW_LIMIT",
    "SOURCE_TIMEOUT",
    "OUTPUT_LIMIT_REACHED",
}
CITATION_ERRORS = {"CITATION_INVALID", "CHAT_EVIDENCE_INVALID", "CITATION_NOT_FOUND"}
FIT_WARNINGS = {"INPUT_FIT_UNVERIFIED", "TOKEN_FIT_UNVERIFIED"}


def evidence_support(saved: dict, *, input_fit_verified: bool = False) -> dict:
    """Describe trusted server observations without inspecting or grading claim meaning.

    The optional fit predicate is an authored-test/future validated backend seam;
    current HTTP callers never set it. Model or request fields cannot enable it.
    Counts refer to declared text blocks, not independently identified facts.
    """
    warnings = {"SEMANTIC_SUPPORT_UNVERIFIED"}
    issues = set()

    def warn(values):
        if not isinstance(values, (list, tuple)):
            warnings.add("OTHER_SOURCE_WARNING")
            return
        for value in values:
            if value == "MEANING_NOT_VERIFIED":
                value = "SEMANTIC_SUPPORT_UNVERIFIED"
            warnings.add(
                value
                if isinstance(value, str) and value in WARNINGS
                else "OTHER_SOURCE_WARNING"
            )

    warn(saved.get("warnings", []))
    try:
        answer = Answer.model_validate(saved.get("answer"))
    except ValueError:
        answer = None
    try:
        evidence = saved.get("evidence", [])
        supplied = [item["evidence_id"] for item in evidence]
        ids_invalid = (
            len(supplied) != len(set(supplied))
            or len(supplied) > 5
            or any(
                not isinstance(value, str)
                or not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", value)
                for value in supplied
            )
        )
        allowed = set(supplied)
        for item in evidence:
            warn(item.get("warnings", []))
            for location in item.get("locations", []):
                if location.get("precision") == "coarse":
                    warnings.add("COARSE_LOCATION")
                elif location.get("precision") == "unavailable":
                    warnings.add("LOCATION_UNAVAILABLE")
    except (ValueError, KeyError, TypeError, AttributeError):
        allowed, ids_invalid = set(), True
    claims = answer.claims if answer else ()
    cited = {value for claim in claims for value in claim.citations}
    if not cited.issubset(allowed) or any(
        len(set(c.citations)) != len(c.citations) for c in claims
    ):
        ids_invalid = True

    observations = saved.get("citations", [])
    try:
        observed_ids = [item["citation_id"] for item in observations]
        if len(observed_ids) != len(set(observed_ids)) or not set(
            observed_ids
        ).issubset(cited):
            ids_invalid = True
        observations = {item["citation_id"]: item for item in observations}
    except (KeyError, TypeError):
        observations, ids_invalid = {}, True

    quotes_invalid, unavailable = False, False
    resolved = set()
    for citation, observation in observations.items():
        warn(observation.get("warning_codes", []))
        if "ocr" in observation.get("methods", []):
            warnings.add("OCR_DERIVED_TEXT")
            if observation.get("ocr_confidence_available") is not True:
                warnings.add("OCR_CONFIDENCE_UNAVAILABLE")
        if "coarse" in observation.get("precisions", []):
            warnings.add("COARSE_LOCATION")
        if "unavailable" in observation.get("precisions", []):
            warnings.add("LOCATION_UNAVAILABLE")
        availability, code = observation.get("availability"), observation.get("code")
        if code in CITATION_ERRORS:
            quotes_invalid = True
        elif code in INCOMPLETE_ERRORS:
            issues.add(code)
        elif availability == "unavailable":
            unavailable = True
        elif availability == "available" and code is None:
            resolved.add(citation)
    if {"SOURCES_UNAVAILABLE", "SOURCE_UNAVAILABLE"}.intersection(warnings):
        unavailable = True
    quotes_invalid |= "CITATION_INVALID" in warnings
    issues.update(
        warnings.intersection(
            {
                "GENERATION_INCOMPLETE",
                "RESPONSE_INVALID",
                "SOURCE_TIMEOUT",
                "PREVIEW_LIMIT",
            }
        )
    )
    error = saved.get("error_code")
    if saved.get("state") == "failed" or error:
        if error in CITATION_ERRORS:
            quotes_invalid = True
        elif error in INCOMPLETE_ERRORS:
            issues.add(
                "RESPONSE_INVALID"
                if error in {"CHAT_RESPONSE_INVALID", "OLLAMA_RESPONSE_INVALID"}
                else error
            )
        else:
            unavailable = True
            issues.add("OPERATION_FAILED")
    if unavailable:
        issues.add("SOURCE_UNAVAILABLE")
    if ids_invalid or quotes_invalid:
        issues.add("CITATION_INVALID")

    no_evidence = (
        saved.get("state") == "complete"
        and answer is not None
        and answer.status == "insufficient_evidence"
        and not allowed
        and not cited
        and "NO_EVIDENCE" in warnings
    )
    if no_evidence:
        fit = "not_applicable"
        warnings.difference_update(FIT_WARNINGS)
    elif input_fit_verified is True and not FIT_WARNINGS.intersection(warnings):
        fit = "verified"
    else:
        fit = "unverified"
        issues.add("INPUT_FIT_UNVERIFIED")
    if saved.get("state") == "processing":
        issues.add("OPERATION_PENDING")
    elif saved.get("state") == "complete" and (
        answer is None or not saved.get("completed_at")
    ):
        issues.add("GENERATION_INCOMPLETE")
    elif saved.get("state") not in {"complete", "failed"}:
        unavailable = True
        issues.add("OPERATION_FAILED")
    if "INPUT_TRUNCATED" in warnings:
        issues.add("INPUT_TRUNCATED")
    if "OUTPUT_LIMIT_REACHED" in warnings:
        issues.add("OUTPUT_LIMIT_REACHED")
    if (
        cited
        and cited != resolved
        and not (unavailable or ids_invalid or quotes_invalid)
    ):
        issues.add("CITATIONS_NOT_REVALIDATED")

    applicable = bool(answer and (answer.status in {"answered", "partial"} or cited))
    coverage = {
        "applicability": "declared_blocks" if applicable else "not_applicable",
        "declared_blocks": len(claims) if applicable else None,
        "blocks_with_supplied_citations": sum(
            bool(c.citations) and set(c.citations).issubset(allowed) for c in claims
        )
        if applicable
        else None,
        "blocks_with_checked_citations": sum(
            bool(c.citations)
            and set(c.citations).issubset(resolved)
            and not ids_invalid
            for c in claims
        )
        if applicable
        else None,
        "blocks_without_citations": sum(not c.citations for c in claims)
        if applicable
        else None,
    }
    if answer and answer.status == "partial":
        warnings.add("PARTIAL_ANSWER")
    if applicable and coverage["blocks_without_citations"]:
        issues.add("CITATIONS_MISSING")

    incomplete = issues - {
        "SOURCE_UNAVAILABLE",
        "OPERATION_FAILED",
        "CITATION_INVALID",
        "CITATIONS_MISSING",
    }
    if unavailable:
        state = "unavailable"
    elif ids_invalid or quotes_invalid:
        state = "citation_problem"
    elif incomplete:
        state = "incomplete"
    elif no_evidence:
        state = "no_evidence"
    elif (
        answer
        and not cited
        and answer.status in {"clarification", "insufficient_evidence"}
    ):
        state = "clarification" if answer.status == "clarification" else "abstained"
    elif "CITATIONS_MISSING" in issues:
        state = "citations_missing"
    else:
        state = "citations_resolved"
    warnings.update(code for code in issues if code in WARNINGS)
    return {
        "state": state,
        "label": LABELS[state],
        "answer_status": answer.status if answer else None,
        "semantic_support": "not_independently_verified",
        "coverage": coverage,
        "coverage_basis": "Counts describe declared text blocks; hidden assertions and factual support are not independently checked.",
        "checks": {
            "citation_ids": "invalid"
            if ids_invalid
            else "valid"
            if cited
            else "not_applicable",
            "locations_and_quotes": "invalid"
            if quotes_invalid
            else "unavailable"
            if unavailable and cited
            else "checked"
            if cited and cited == resolved and not ids_invalid
            else "not_revalidated"
            if cited
            else "not_applicable",
            "input_fit": fit,
        },
        "issues": sorted(issues),
        "warnings": [
            {"code": code, "message": WARNINGS[code]} for code in sorted(warnings)
        ],
    }
