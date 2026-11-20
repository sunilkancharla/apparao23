"""Explicit local configuration with safe errors and no environment side effects."""

import os
import stat
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).absolute().parents[1]


class ConfigurationError(ValueError):
    """A safe, actionable configuration failure without private values."""


def _local_path(value: str) -> Path:
    path = Path(value)
    if (
        not value
        or any(ord(character) < 32 for character in value)
        or value.startswith(("\\\\", "//"))
        or ".." in path.parts
        or (path.anchor and not path.is_absolute())
    ):
        raise ConfigurationError("CONFIG_INVALID: use an explicit local path.")
    return path if path.is_absolute() else PROJECT_ROOT / path


@dataclass(frozen=True)
class Settings:
    """Validated loopback authorities and operator-controlled asset locations."""

    port: int
    ollama_port: int
    data_root: Path
    model_root: Path
    ocr_asset: Path | None
    ollama_executable: Path

    @property
    def origin(self) -> str:
        """Return the only allowed browser authority and Origin."""
        return f"http://127.0.0.1:{self.port}"

    @property
    def ollama_url(self) -> str:
        """Return a literal IPv4 loopback URL without DNS resolution."""
        return f"http://127.0.0.1:{self.ollama_port}"

    @classmethod
    def from_env(cls, environment: Mapping[str, str] | None = None) -> "Settings":
        """Read DA_* settings, rejecting unknown keys and unsafe values."""
        env = os.environ if environment is None else environment
        allowed = {
            "DA_HOST",
            "DA_PORT",
            "DA_OLLAMA_PORT",
            "DA_DATA_ROOT",
            "DA_MODEL_ROOT",
            "DA_OCR_ASSET",
            "DA_OLLAMA_EXECUTABLE",
        }
        if any(key.startswith("DA_") and key not in allowed for key in env):
            raise ConfigurationError("CONFIG_INVALID: unsupported DA_* setting.")
        if env.get("DA_HOST", "127.0.0.1") != "127.0.0.1":
            raise ConfigurationError("CONFIG_INVALID: DA_HOST must be 127.0.0.1.")
        try:
            port = int(env.get("DA_PORT", "8000"))
            ollama_port = int(env.get("DA_OLLAMA_PORT", "11435"))
        except ValueError:
            raise ConfigurationError(
                "CONFIG_INVALID: ports must be integers."
            ) from None
        if not all(1 <= value <= 65535 for value in (port, ollama_port)):
            raise ConfigurationError("CONFIG_INVALID: ports must be 1..65535.")
        if port == ollama_port:
            raise ConfigurationError(
                "CONFIG_INVALID: app and Ollama ports must differ."
            )
        data_root = _local_path(env.get("DA_DATA_ROOT", "data/app"))
        model_root = _local_path(env.get("DA_MODEL_ROOT", "data/ollama/models"))
        protected = (PROJECT_ROOT / ".venv", PROJECT_ROOT / ".git", model_root)
        if (
            data_root == PROJECT_ROOT
            or data_root in PROJECT_ROOT.parents
            or any(
                data_root == root
                or root in data_root.parents
                or data_root in root.parents
                for root in protected
            )
        ):
            raise ConfigurationError(
                "CONFIG_INVALID: data root overlaps protected files."
            )
        return cls(
            port,
            ollama_port,
            data_root,
            model_root,
            _local_path(env["DA_OCR_ASSET"]) if "DA_OCR_ASSET" in env else None,
            _local_path(
                env.get("DA_OLLAMA_EXECUTABLE", ".venv/tools/ollama/0.40.16/ollama.exe")
            ),
        )


def validate_local_ancestry(path: Path) -> None:
    """Reject existing symlinks and Windows reparse ancestry before file access."""
    for parent in (path, *path.parents):
        try:
            info = parent.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise OSError("Reparse ancestry refused")


def prepare_data_root(root: Path) -> None:
    """Create/probe the configured root, removing only this call's temporary file."""
    try:
        validate_local_ancestry(root)
        root.mkdir(parents=True, exist_ok=True)
        validate_local_ancestry(root)
        with tempfile.TemporaryFile(dir=root) as probe:
            probe.write(b"local startup probe")
            probe.flush()
    except OSError:
        raise ConfigurationError(
            "DATA_ROOT_UNAVAILABLE: check the local directory, permissions and disk."
        ) from None
