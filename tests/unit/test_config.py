"""Configuration refuses remote endpoints and unsafe managed paths."""

from pathlib import Path
from types import SimpleNamespace

import pytest

from app.config import ConfigurationError, Settings, prepare_data_root


def test_approved_defaults():
    settings = Settings.from_env({})
    assert settings.origin == "http://127.0.0.1:8000"
    assert settings.ollama_url == "http://127.0.0.1:11435"
    assert settings.data_root.name == "app"


@pytest.mark.parametrize(
    "environment",
    [
        {"DA_HOST": "0.0.0.0"},
        {"DA_HOST": "localhost"},
        {"DA_PORT": "bad"},
        {"DA_PORT": "0"},
        {"DA_OLLAMA_PORT": "8000"},
        {"DA_OLLAMA_URL": "https://private.example/secret"},
        {"DA_DATA_ROOT": "../outside"},
        {"DA_UNKNOWN": "secret"},
        {"DA_DATA_ROOT": ""},
        {"DA_DATA_ROOT": "data/invalid\x00path"},
        {"DA_DATA_ROOT": "F:relative"},
        {"DA_DATA_ROOT": "\\\\server\\share"},
        {"DA_DATA_ROOT": ".venv/managed"},
        {"DA_DATA_ROOT": "data/ollama/models/managed"},
    ],
)
def test_invalid_configuration_has_safe_errors(environment):
    with pytest.raises(ConfigurationError) as error:
        Settings.from_env(environment)
    assert "secret" not in str(error.value)
    assert "private.example" not in str(error.value)


def test_create_and_probe_managed_root(tmp_path):
    root = tmp_path / "managed"
    prepare_data_root(root)
    assert root.is_dir()
    assert list(root.iterdir()) == []


def test_file_instead_of_data_directory_is_sanitized(tmp_path):
    root = tmp_path / "private-file"
    root.write_text("private contents")
    with pytest.raises(ConfigurationError, match="DATA_ROOT_UNAVAILABLE") as error:
        prepare_data_root(root)
    assert str(root) not in str(error.value)


def test_unwritable_directory_is_sanitized(tmp_path, monkeypatch):
    from app import config

    def denied(**kwargs):
        raise PermissionError("PRIVATE_SENTINEL")

    monkeypatch.setattr(config.tempfile, "TemporaryFile", denied)
    with pytest.raises(ConfigurationError, match="DATA_ROOT_UNAVAILABLE") as error:
        prepare_data_root(tmp_path)
    assert "PRIVATE_SENTINEL" not in str(error.value)


def test_symlink_ancestry_is_rejected(tmp_path):
    target = tmp_path / "real"
    target.mkdir()
    link = tmp_path / "link"
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError:
        pytest.skip("Host does not grant symlink creation")
    with pytest.raises(ConfigurationError, match="DATA_ROOT_UNAVAILABLE"):
        prepare_data_root(link / "managed")


def test_windows_reparse_attribute_is_rejected_without_symlink_privileges(
    tmp_path, monkeypatch
):
    from app.config import validate_local_ancestry

    original = Path.lstat

    def reparse(path):
        if path == tmp_path:
            return SimpleNamespace(st_mode=0, st_file_attributes=0x400)
        return original(path)

    monkeypatch.setattr(Path, "lstat", reparse)
    with pytest.raises(OSError, match="Reparse"):
        validate_local_ancestry(tmp_path / "child")
