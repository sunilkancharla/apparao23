"""Small real-layout asset fixtures exercise preflight without native execution."""

import hashlib
import json
from dataclasses import replace

import pytest

from app import diagnostics, runtime
from app.config import Settings
from app.ollama import OllamaError


@pytest.fixture
def assets(tmp_path, monkeypatch, run_budget):
    settings = replace(
        Settings.from_env({}),
        model_root=tmp_path / "models",
        ollama_executable=tmp_path / "ollama.exe",
    )
    executable = b"synthetic executable, never run"
    settings.ollama_executable.write_bytes(executable)
    monkeypatch.setattr(
        runtime, "OLLAMA_SHA256", hashlib.sha256(executable).hexdigest()
    )
    blob = b"synthetic model data, never loaded"
    blob_hash = hashlib.sha256(blob).hexdigest()
    blob_path = settings.model_root / "blobs" / ("sha256-" + blob_hash)
    blob_path.parent.mkdir(parents=True)
    blob_path.write_bytes(blob)
    manifests = {}
    for component, (relative, _) in tuple(diagnostics.MODEL_MANIFESTS.items()):
        data = json.dumps(
            {
                "config": {"digest": "sha256:" + blob_hash, "size": len(blob)},
                "layers": [],
            }
        ).encode()
        path = settings.model_root / "manifests-v2/ollama.com/library" / relative
        path.parent.mkdir(parents=True)
        path.write_bytes(data)
        monkeypatch.setitem(
            diagnostics.MODEL_MANIFESTS,
            component,
            (relative, hashlib.sha256(data).hexdigest()),
        )
        manifests[component] = path
    yield settings, manifests, blob_path
    for path in tmp_path.rglob("*"):
        if path.is_file():
            run_budget.retain(path.read_bytes())


@pytest.mark.parametrize("component", ["embedding_model", "chat_model"])
def test_selected_runtime_v2_layout_verifies_manifest_and_blob(assets, component):
    settings, _, _ = assets
    result = diagnostics._model(
        settings.model_root, component, *diagnostics.MODEL_MANIFESTS[component]
    )
    assert result.code == component.upper() + "_VERIFIED"


def test_runtime_preflight_uses_real_layout_without_injected_asset_verifier(assets):
    settings, _, _ = assets
    runtime._verify_assets(settings)


def test_changed_manifest_is_refused_by_its_original_hash(assets):
    settings, manifests, _ = assets
    manifest = manifests["embedding_model"]
    manifest.write_bytes(b"!" + manifest.read_bytes()[1:])
    result = diagnostics._model(
        settings.model_root,
        "embedding_model",
        *diagnostics.MODEL_MANIFESTS["embedding_model"],
    )
    assert result.code == "EMBEDDING_MODEL_MISMATCH"


@pytest.mark.parametrize("change", ["missing", "same_size_changed", "size_changed"])
def test_blob_missing_or_tampered_is_refused(assets, change):
    settings, _, blob = assets
    if change == "missing":
        blob.unlink()
    else:
        blob.write_bytes(
            b"x" * (blob.stat().st_size if change == "same_size_changed" else 1)
        )
    assert (
        diagnostics._model(
            settings.model_root,
            "embedding_model",
            *diagnostics.MODEL_MANIFESTS["embedding_model"],
        ).code
        == "MODEL_INCOMPLETE"
    )


def test_legacy_layout_is_not_a_fallback_for_the_selected_runtime(assets):
    settings, manifests, _ = assets
    old = (
        settings.model_root
        / "manifests/registry.ollama.ai/library/nomic-embed-text/v1.5"
    )
    old.parent.mkdir(parents=True)
    old.write_bytes(manifests["embedding_model"].read_bytes())
    manifests["embedding_model"].unlink()
    assert (
        diagnostics._model(
            settings.model_root,
            "embedding_model",
            *diagnostics.MODEL_MANIFESTS["embedding_model"],
        ).code
        == "MODEL_MISSING"
    )


def test_unsafe_ancestry_is_not_accepted_as_a_valid_asset(assets, monkeypatch):
    settings, _, _ = assets

    def refuse(path):
        raise OSError("synthetic unsafe ancestry")

    monkeypatch.setattr(diagnostics, "validate_local_ancestry", refuse)
    assert (
        diagnostics._model(
            settings.model_root,
            "embedding_model",
            *diagnostics.MODEL_MANIFESTS["embedding_model"],
        ).code
        == "EMBEDDING_MODEL_MISMATCH"
    )


def test_declared_blob_size_is_checked_even_when_both_hashes_match(assets, monkeypatch):
    settings, manifests, _ = assets
    manifest = manifests["embedding_model"]
    data = json.loads(manifest.read_bytes())
    data["config"]["size"] += 1
    payload = json.dumps(data).encode()
    manifest.write_bytes(payload)
    relative, _ = diagnostics.MODEL_MANIFESTS["embedding_model"]
    monkeypatch.setitem(
        diagnostics.MODEL_MANIFESTS,
        "embedding_model",
        (relative, hashlib.sha256(payload).hexdigest()),
    )
    assert (
        diagnostics._model(
            settings.model_root,
            "embedding_model",
            *diagnostics.MODEL_MANIFESTS["embedding_model"],
        ).code
        == "MODEL_INCOMPLETE"
    )


@pytest.mark.parametrize(
    "component,code",
    [
        ("executable", "OLLAMA_MISSING"),
        ("manifest", "MODEL_MISSING"),
        ("blob", "MODEL_INCOMPLETE"),
    ],
)
def test_runtime_errors_identify_the_failed_component_without_paths(
    assets, component, code
):
    settings, manifests, blob = assets
    target = {
        "executable": settings.ollama_executable,
        "manifest": manifests["embedding_model"],
        "blob": blob,
    }[component]
    target.unlink()
    with pytest.raises(OllamaError, match="^" + code + "$") as failure:
        runtime._verify_assets(settings)
    assert str(settings.model_root) not in str(failure.value)
