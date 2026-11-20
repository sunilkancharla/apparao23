"""Read-only prerequisite inspection; never starts or contacts a model service."""

import hashlib
import json
import socket
from pathlib import Path

from pydantic import BaseModel

from app.config import Settings, validate_local_ancestry

OLLAMA_SHA256 = "4ccefcbfecc50fb6526471adabbc20869dd614e29e351120b15083cb174b0b8a"
OCR_SHA256 = "7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2"
MODEL_MANIFESTS = {
    "chat_model": (
        "qwen2.5/1.5b-instruct-q4_K_M",
        "65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b",
    ),
    "embedding_model": (
        "nomic-embed-text/v1.5",
        "0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f",
    ),
}


class ComponentState(BaseModel):
    """A bounded public component result containing no filesystem paths."""

    component: str
    code: str
    message: str


def _matches(path: Path, expected: str, limit: int) -> bool:
    validate_local_ancestry(path)
    if not path.is_file() or path.stat().st_size > limit:
        return False
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest() == expected


def _asset(
    component: str, path: Path | None, digest: str, limit: int
) -> ComponentState:
    code = component.upper()
    try:
        if path is None or not path.exists():
            return ComponentState(
                component=component,
                code=f"{code}_MISSING",
                message="Configure the approved local asset; no download is attempted.",
            )
        matches = _matches(path, digest, limit)
    except OSError:
        matches = False
    return ComponentState(
        component=component,
        code=f"{code}_VERIFIED" if matches else f"{code}_MISMATCH",
        message="Approved local bytes verified."
        if matches
        else "Asset is unreadable or differs from the approved bytes; check local provisioning.",
    )


def _model(root: Path, component: str, relative: str, digest: str) -> ComponentState:
    # The selected Ollama 0.40.16 store uses this versioned layout. A legacy
    # registry path is not an alternate source for an approved model identity.
    manifest = root / "manifests-v2/ollama.com/library" / relative
    result = _asset(component, manifest, digest, 65536)
    if not result.code.endswith("_VERIFIED"):
        if result.code.endswith("_MISSING"):
            result.code = "MODEL_MISSING"
        return result
    try:
        content = json.loads(manifest.read_bytes())
        entries = [content["config"], *content["layers"]]
        if not 1 <= len(entries) <= 16:
            raise ValueError
        for entry in entries:
            algorithm, value = entry["digest"].split(":")
            if (
                algorithm != "sha256"
                or len(value) != 64
                or any(letter not in "0123456789abcdef" for letter in value)
            ):
                raise ValueError
            blob = root / "blobs" / f"sha256-{value}"
            if not _matches(blob, value, 1_100_000_000):
                raise ValueError
            if blob.stat().st_size != entry["size"]:
                raise ValueError
    except (OSError, ValueError, KeyError, TypeError):
        return ComponentState(
            component=component,
            code="MODEL_INCOMPLETE",
            message="Approved model layers are missing, unreadable or changed; check local provisioning.",
        )
    return result


def reserve_port(port: int) -> socket.socket:
    """Bind exclusively to loopback; callers own and close the returned socket."""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        listener.bind(("127.0.0.1", port))
        listener.listen(16)
    except OSError:
        listener.close()
        raise
    return listener


def inspect_prerequisites(settings: Settings) -> list[ComponentState]:
    """Check pinned local bytes and report missing owned-runtime integration."""
    states = [
        _asset("ollama", settings.ollama_executable, OLLAMA_SHA256, 100_000_000),
        _asset("ocr_asset", settings.ocr_asset, OCR_SHA256, 4_113_088),
    ]
    for component, (relative, digest) in MODEL_MANIFESTS.items():
        states.append(_model(settings.model_root, component, relative, digest))
    try:
        with reserve_port(settings.ollama_port):
            pass
        code = "OLLAMA_NOT_STARTED"
        message = (
            "No owned model service is started by T19; model integration is pending."
        )
    except OSError:
        code = "OLLAMA_PORT_IN_USE"
        message = (
            "Ollama port unavailable; this app will not attach to an unknown service."
        )
    states.append(
        ComponentState(component="ollama_service", code=code, message=message)
    )
    return states
