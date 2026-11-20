"""Check the existing local stack in memory; no product service is started."""

import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


class ProbeInput(BaseModel):
    """Require a typed value across the API/validation/client boundary."""

    quantity: int


def test_python_uses_the_isolated_project_environment():
    """Catch accidentally running the suite with a global interpreter."""
    project = Path(__file__).resolve().parents[1]
    assert Path(sys.prefix).resolve() == (project / ".venv").resolve()
    assert sys.prefix != sys.base_prefix


@pytest.mark.parametrize(
    ("payload", "status"),
    [({"quantity": 4}, 200), ({"quantity": "invalid"}, 422), ({}, 422)],
)
def test_api_validation_and_http_client_interoperate(payload, status):
    """Exercise request parsing, validation and response transport together."""
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

    @app.post("/setup-probe")
    def probe(value: ProbeInput) -> dict[str, int]:
        """Return typed input for this test-only in-memory endpoint."""
        return {"quantity": value.quantity}

    with TestClient(app) as client:
        response = client.post("/setup-probe", json=payload)

    assert response.status_code == status
    if status == 200:
        assert response.json() == {"quantity": 4}
    else:
        errors = response.json()["detail"]
        assert any(error["loc"] == ["body", "quantity"] for error in errors)
