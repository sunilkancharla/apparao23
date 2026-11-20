"""Startup diagnostics expose safe states without inference or downloads."""

import hashlib
import json
import os
import socket
import subprocess
import sys
import time
from dataclasses import replace

import httpx
import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.diagnostics import inspect_prerequisites, reserve_port
from app.main import create_app


@pytest.fixture
def settings(tmp_path):
    return replace(
        Settings.from_env({}),
        data_root=tmp_path / "app",
        model_root=tmp_path / "models",
        ocr_asset=tmp_path / "eng.traineddata",
        ollama_executable=tmp_path / "ollama.exe",
    )


def test_missing_prerequisites_are_explicit(settings, caplog):
    with TestClient(create_app(settings), base_url=settings.origin) as client:
        response = client.get("/api/health")
    assert response.status_code == 503
    body = response.json()
    codes = {item["code"] for item in body["components"]}
    assert {"OLLAMA_MISSING", "MODEL_MISSING", "OCR_ASSET_MISSING"} <= codes
    assert body["ready"] is False
    assert str(settings.data_root.parent) not in response.text + caplog.text
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-content-type-options"] == "nosniff"


@pytest.mark.parametrize(
    ("headers", "method"),
    [
        ({"Host": "evil.example"}, "GET"),
        ({"Host": "127.0.0.1:8001"}, "GET"),
        ({"Origin": "https://evil.example"}, "GET"),
        ({"Origin": "null"}, "GET"),
        ({}, "POST"),
    ],
)
def test_request_boundary_denies_other_authorities_and_mutations(
    settings, headers, method
):
    with TestClient(create_app(settings), base_url=settings.origin) as client:
        response = client.request(method, "/api/health", headers=headers)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "REQUEST_DENIED"
    assert "access-control-allow-origin" not in response.headers


def test_path_failure_keeps_diagnostics_available(settings):
    settings.data_root.write_text("private")
    with TestClient(create_app(settings), base_url=settings.origin) as client:
        response = client.get("/api/health")
    assert response.status_code == 503
    assert "DATA_ROOT_UNAVAILABLE" in response.text
    assert "private" not in response.text


def test_port_collision_does_not_attach_or_change_port():
    with reserve_port(0) as first, pytest.raises(OSError):
        reserve_port(first.getsockname()[1])


def test_unknown_ollama_listener_is_never_contacted(settings):
    with reserve_port(0) as listener:
        settings = replace(settings, ollama_port=listener.getsockname()[1])
        report = inspect_prerequisites(settings)
        assert "OLLAMA_PORT_IN_USE" in {item.code for item in report}
        listener.settimeout(0.05)
        with pytest.raises(socket.timeout):
            listener.accept()


def test_tampered_assets_refuse_readiness(settings):
    settings.ocr_asset.write_bytes(b"not the approved asset")
    settings.ollama_executable.write_bytes(b"not the approved runtime")
    report = inspect_prerequisites(settings)
    codes = {item.code for item in report}
    assert {"OCR_ASSET_MISMATCH", "OLLAMA_MISMATCH"} <= codes


def test_model_manifest_and_layers_are_checked(settings, monkeypatch):
    from app import diagnostics

    layer = b"synthetic fixture, never a model"
    digest = hashlib.sha256(layer).hexdigest()
    manifest_bytes = json.dumps(
        {
            "config": {"digest": f"sha256:{digest}", "size": len(layer)},
            "layers": [],
        }
    ).encode()
    manifest = settings.model_root / "manifests-v2/ollama.com/library/test/v1"
    manifest.parent.mkdir(parents=True)
    manifest.write_bytes(manifest_bytes)
    blob = settings.model_root / "blobs" / f"sha256-{digest}"
    blob.parent.mkdir()
    blob.write_bytes(layer)
    monkeypatch.setattr(
        diagnostics,
        "MODEL_MANIFESTS",
        {"chat_model": ("test/v1", hashlib.sha256(manifest_bytes).hexdigest())},
    )
    assert "CHAT_MODEL_VERIFIED" in {
        item.code for item in inspect_prerequisites(settings)
    }
    blob.write_bytes(b"changed")
    assert "MODEL_INCOMPLETE" in {item.code for item in inspect_prerequisites(settings)}


def test_real_launcher_missing_prerequisites_and_port_collision(settings):
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("DA_")
    }
    with reserve_port(0) as probe:
        port = probe.getsockname()[1]
    environment.update(
        {
            "DA_PORT": str(port),
            "DA_DATA_ROOT": str(settings.data_root),
            "DA_MODEL_ROOT": str(settings.model_root),
            "DA_OCR_ASSET": str(settings.ocr_asset),
            "DA_OLLAMA_EXECUTABLE": str(settings.ollama_executable),
        }
    )
    with subprocess.Popen(
        [sys.executable, "-m", "app.main"],
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    ) as process:
        try:
            with httpx.Client(
                trust_env=False, follow_redirects=False, timeout=0.5
            ) as client:
                deadline = time.monotonic() + 10
                while True:
                    try:
                        response = client.get(f"http://127.0.0.1:{port}/api/health")
                        break
                    except (httpx.ConnectError, httpx.ConnectTimeout):
                        if time.monotonic() >= deadline or process.poll() is not None:
                            pytest.fail("Local launcher did not become available")
                        time.sleep(0.1)
                assert response.status_code == 503
                assert response.json()["ready"] is False
                rejected = client.get(
                    f"http://127.0.0.1:{port}/private?question=PRIVATE_SENTINEL",
                    headers={"Host": "evil.example"},
                )
                assert rejected.status_code == 403
            collision = subprocess.run(
                [sys.executable, "-m", "app.main"],
                check=False,
                env=environment,
                capture_output=True,
                timeout=10,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            assert collision.returncode == 2
            assert b"APP_PORT_UNAVAILABLE" in collision.stderr
        finally:
            process.terminate()
            stdout, stderr = process.communicate(timeout=10)
    assert b"PRIVATE_SENTINEL" not in stdout + stderr
    assert str(settings.data_root).encode() not in stdout + stderr


def test_unexpected_api_failure_is_sanitized(settings):
    application = create_app(settings)

    @application.get("/test-failure")
    def fail():
        raise RuntimeError("PRIVATE_SENTINEL")

    with TestClient(
        application, base_url=settings.origin, raise_server_exceptions=False
    ) as client:
        response = client.get("/test-failure")
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "INTERNAL_ERROR"
    assert "PRIVATE_SENTINEL" not in response.text
    assert response.headers["cache-control"] == "no-store"
