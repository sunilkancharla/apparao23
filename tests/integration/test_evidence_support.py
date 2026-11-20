"""HTTP support signals use server checks without changing stored historical text."""

from app.storage.messages import Messages
from tests.integration import test_chat, test_saved_citations

api = test_chat.api
retrieval = test_chat.retrieval
cited = test_saved_citations.cited
citation_api = test_saved_citations.citation_api


def warning_codes(indicator):
    return {item["code"] for item in indicator["warnings"]}


def test_no_evidence_post_and_replay_emit_na_support_without_persisting_a_badge(api):
    client, conversation, _ = api
    url = f"/api/conversations/{conversation}/answers"
    payload = {"question": "North units?", "expected_revision": 0}
    headers = {"Idempotency-Key": "indicator-answer-01"}
    first = client.post(url, json=payload, headers=headers)
    second = client.post(url, json=payload, headers=headers)
    assert first.status_code == 202 and first.json() == second.json()
    data = first.json()["data"]
    assert data["evidence_support"]["state"] == "no_evidence"
    assert data["evidence_support"]["coverage"]["declared_blocks"] is None
    store = client.app.state.upload_store
    historical = client.portal.call(
        lambda: Messages(store).get(conversation, data["answer_id"])
    )
    assert (
        historical["answer"] == data["answer"] and "evidence_support" not in historical
    )


def test_live_checked_quotes_and_unknown_fit_are_reported_separately(citation_api):
    client, _, saved, _, conversation, _ = citation_api
    response = client.get(
        f"/api/conversations/{conversation}/answers/{saved['answer_id']}"
    )
    assert response.status_code == 200
    data = response.json()["data"]
    signal = data["evidence_support"]
    assert signal["state"] == "incomplete"
    assert signal["checks"]["locations_and_quotes"] == "checked"
    assert signal["checks"]["input_fit"] == "unverified"
    assert signal["coverage"]["blocks_with_checked_citations"] == 1
    assert "COARSE_LOCATION" in warning_codes(signal)
    assert signal["semantic_support"] == "not_independently_verified"
    assert data["answer"] == saved["answer"]
    assert response.headers["cache-control"] == "no-store"


def test_later_missing_source_cannot_keep_a_resolved_badge_or_hide_history(
    citation_api,
):
    client, _, saved, store, conversation, _ = citation_api
    next((store.root / "originals").iterdir()).unlink()
    data = client.get(
        f"/api/conversations/{conversation}/answers/{saved['answer_id']}"
    ).json()["data"]
    assert data["answer"] == saved["answer"]
    assert data["evidence_support"]["state"] == "unavailable"
    assert data["evidence_support"]["coverage"]["blocks_with_checked_citations"] == 0
    assert "SOURCE_UNAVAILABLE" in data["evidence_support"]["issues"]


def test_failed_intent_read_does_not_become_successful_empty_evidence(api):
    client, conversation, other = api
    store = client.app.state.upload_store

    def fail():
        service = Messages(store)
        request = service.admit(conversation, "indicator-failed-01", "North?", 0)
        service.fail(request["id"], "SOURCE_CHANGED")
        return request["id"]

    identity = client.portal.call(fail)
    url = f"/api/conversations/{conversation}/answers/{identity}"
    data = client.get(url).json()["data"]
    assert data["state"] == "failed" and data["answer"] is None
    assert data["evidence_support"]["state"] == "unavailable"
    assert client.get(url.replace(conversation, other)).status_code == 404


def test_processing_intent_has_no_invented_complete_answer_or_coverage(api):
    client, conversation, _ = api
    store = client.app.state.upload_store
    identity = client.portal.call(
        lambda: Messages(store).admit(
            conversation, "indicator-pending-01", "North?", 0
        )["id"]
    )
    data = client.get(f"/api/conversations/{conversation}/answers/{identity}").json()[
        "data"
    ]
    assert data["evidence_support"]["state"] == "incomplete"
    assert data["evidence_support"]["coverage"]["declared_blocks"] is None


def test_all_blocked_selected_sources_preserve_the_unavailable_warning(api):
    client, conversation, _ = api
    uploaded = client.post(
        f"/api/conversations/{conversation}/attachments",
        content=b"Name,Units\nNorth,42\n",
        headers={
            "Content-Type": "text/csv",
            "X-Filename": "authored.csv",
            "Idempotency-Key": "indicator-upload-01",
        },
    ).json()["data"]
    reference = uploaded["reference_id"]
    assert (
        client.put(
            f"/api/conversations/{conversation}/selection",
            json={"references": [reference], "expected_revision": 0},
        ).status_code
        == 200
    )
    response = client.post(
        f"/api/conversations/{conversation}/answers",
        json={"question": "North?", "expected_revision": 1},
        headers={"Idempotency-Key": "indicator-blocked-01"},
    )
    assert response.status_code == 202
    data = response.json()["data"]
    assert data["answer"]["status"] == "insufficient_evidence"
    assert "SOURCES_UNAVAILABLE" in data["warnings"]
    assert data["evidence_support"]["state"] == "unavailable"


def test_observed_ocr_flags_stay_visible_with_incomplete_fit(citation_api, monkeypatch):
    from app.chat.citations import Citations

    resolve = Citations._resolve

    async def observed_ocr(self, *args):
        preview = await resolve(self, *args)
        preview["passages"][0].update(method="ocr", confidence=None)
        preview["warnings"].append("LOW_OCR_CONFIDENCE")
        return preview

    monkeypatch.setattr(Citations, "_resolve", observed_ocr)
    client, _, saved, _, conversation, _ = citation_api
    data = client.get(
        f"/api/conversations/{conversation}/answers/{saved['answer_id']}"
    ).json()["data"]
    signal = data["evidence_support"]
    assert signal["state"] == "incomplete"
    assert {
        "OCR_DERIVED_TEXT",
        "OCR_CONFIDENCE_UNAVAILABLE",
        "LOW_OCR_CONFIDENCE",
    } <= warning_codes(signal)


def test_request_cannot_assert_verified_fit_or_a_model_confidence_score(api):
    client, conversation, _ = api
    response = client.post(
        f"/api/conversations/{conversation}/answers",
        json={
            "question": "North?",
            "expected_revision": 0,
            "input_fit_verified": True,
            "confidence": 0.99,
        },
        headers={"Idempotency-Key": "indicator-spoof-01"},
    )
    assert response.status_code == 422
