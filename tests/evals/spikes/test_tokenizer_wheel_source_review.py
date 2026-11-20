"""Authored inert controls for the approved WSP reader and report reserve."""

import hashlib
import importlib.util
import io
import stat
import struct
import sys
import zipfile
from pathlib import Path

import pytest


def load_reader():
    """Load only our evaluation module, never a wheel module."""
    path = Path(__file__).with_name("tokenizer_wheel_source_review.py")
    spec = importlib.util.spec_from_file_location("wsp_reader", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


reader = load_reader()


def test_optional_output_preserves_closure_reserve():
    gate = reader.ReportGate(limit=20, reserve=8)
    assert len(gate.admit("x" * 10)) == 12
    with pytest.raises(ValueError, match="report_reserve"):
        gate.admit("")


def test_multibyte_boundary_and_closure():
    gate = reader.ReportGate(limit=12, reserve=6)
    assert len(gate.admit("éé")) == 6
    with pytest.raises(ValueError):
        gate.admit("")
    assert len(gate.admit("éé", closure=True)) == 6
    assert gate.used == 12


@pytest.fixture(scope="module")
def helper():
    return reader.load_helper()


def archive_case(members=None, alter=None):
    """Reuse content-addressed authored inert fixtures across test invocations."""
    members = members or {
        "tokenizers/__init__.py": b"raise RuntimeError('must never execute')\n",
        "tokenizers/native.pyd": b"NOT AN EXECUTABLE",
    }
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_STORED) as archive:
        for name, value in members.items():
            entry = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG | 0o600) << 16
            archive.writestr(entry, value)
    raw = bytearray(stream.getvalue())
    if alter:
        alter(raw)
    raw = bytes(raw)
    folder = reader.RUN / "synthetic-cases"
    folder.mkdir(exist_ok=True)
    path = folder / (hashlib.sha256(raw).hexdigest()[:16] + ".zip")
    if path.exists():
        assert path.read_bytes() == raw
    else:
        assert len(list(folder.glob("*.zip"))) < 40
        path.write_bytes(raw)
    inventory = [
        {"name": name, "bytes": len(value), "sha256": hashlib.sha256(value).hexdigest()}
        for name, value in members.items()
    ]
    return path, len(raw), hashlib.sha256(raw).hexdigest(), inventory


def inspect(case, helper, **kwargs):
    path, size, sha, inventory = case
    return reader.read_archive(
        path, size, sha, inventory, reader.RUN, helper=helper, **kwargs
    )


def test_valid_source_inert_native_not_opened(helper, monkeypatch):
    case = archive_case()
    original = zipfile.ZipFile.open
    opened = []

    def guarded(self, name, *args, **kwargs):
        assert name.filename.endswith(".py")
        opened.append(name.filename)
        return original(self, name, *args, **kwargs)

    monkeypatch.setattr(zipfile.ZipFile, "open", guarded)
    for name in ("inspect_wheel", "worker", "acquire", "fetch", "supervise_code"):
        monkeypatch.setattr(helper, name, lambda *a, **k: pytest.fail("old dispatch"))
    result = inspect(case, helper)
    assert opened == ["tokenizers/__init__.py"]
    assert result["sources"][0]["text"].startswith("raise RuntimeError")
    assert result["native_members_opened"] == 0
    assert result["charged_read_bytes"] > result["actual_expanded_bytes"]


@pytest.mark.parametrize(
    "fault",
    ["outer_hash", "outer_size", "member_hash", "member_size", "omitted", "extra"],
)
def test_frozen_integrity(helper, fault):
    path, size, sha, inventory = archive_case()
    inventory = [dict(item) for item in inventory]
    if fault == "outer_hash":
        sha = "0" * 64
    elif fault == "outer_size":
        size += 1
    elif fault == "member_hash":
        inventory[0]["sha256"] = "0" * 64
    elif fault == "member_size":
        inventory[0]["bytes"] += 1
    elif fault == "omitted":
        inventory.pop(0)
    else:
        inventory.append({"name": "extra.py", "bytes": 1, "sha256": "0" * 64})
    with pytest.raises((ValueError, helper.Failure)):
        inspect((path, size, sha, inventory), helper)


@pytest.mark.parametrize(
    "name",
    ["../bad.py", "C:/bad.py", "x:y.py", "a./bad.py", "CON.py", "a/" * 9 + "b.py"],
)
def test_unsafe_names(helper, name):
    with pytest.raises(helper.Failure):
        inspect(archive_case({name: b"x=1"}), helper)


def test_alias_and_file_prefix(helper):
    for members in (
        {"A.py": b"x=1", "a.py": b"x=2"},
        {"a.py": b"x=1", "a.py/b.py": b"x=2"},
    ):
        with pytest.raises(helper.Failure):
            inspect(archive_case(members), helper)


@pytest.mark.parametrize(
    "fault", ["type", "encryption", "local_size", "crc", "truncated"]
)
def test_bad_zip_metadata_or_stream(helper, fault):
    def alter(raw):
        central = raw.index(b"PK\x01\x02")
        if fault == "type":
            struct.pack_into("<I", raw, central + 38, (stat.S_IFLNK | 0o777) << 16)
        elif fault == "encryption":
            struct.pack_into("<H", raw, central + 8, 1)
        elif fault == "local_size":
            struct.pack_into("<I", raw, 22, 1)
        elif fault == "crc":
            raw[30 + len("tokenizers/__init__.py")] ^= 1
        else:
            del raw[-2:]

    with pytest.raises((ValueError, helper.Failure, zipfile.BadZipFile)):
        inspect(archive_case(alter=alter), helper)


@pytest.mark.parametrize("text", [b"\xff", b"def :", b"x = '" + b"x" * 32769 + b"'"])
def test_invalid_or_oversize_source(helper, text):
    with pytest.raises((ValueError, SyntaxError, UnicodeError, helper.Failure)):
        inspect(archive_case({"a.py": text}), helper)


def test_ast_limits_and_dynamic_edges():
    text = "import os\nclass C:\n x = dangerous()\ndef f(a=default()):\n return __import__('socket')\n"
    result = reader.source_map(text)
    assert {item["scope"] for item in result["calls"]} == {
        "class_body",
        "definition_time",
        "lazy_body",
    }
    for limits in ({"node_limit": 1}, {"depth_limit": 1}):
        with pytest.raises(ValueError, match="ast_budget"):
            reader.source_map(text, **limits)


def test_budget_before_payload_io(helper):
    class Unreadable:
        def read(self, size):
            pytest.fail("read happened before reserve")

    with pytest.raises(helper.Failure, match="read_limit"):
        helper.digest_stream(Unreadable(), 1, helper.ReadBudget(0))
    with pytest.raises(helper.Failure, match="read_limit"):
        inspect(archive_case(), helper, read_limit=0)


def test_missing_and_changed_input(helper, tmp_path):
    with pytest.raises(FileNotFoundError), helper.open_regular(tmp_path / "missing", tmp_path):
        pytest.fail("missing opened")
    path = tmp_path / "changed"
    path.write_bytes(b"one")
    with pytest.raises(helper.Failure, match="file_changed"), helper.open_regular(path, tmp_path):
        path.write_bytes(b"longer")


@pytest.mark.parametrize(
    "event,args",
    [
        ("socket.connect", ()),
        ("subprocess.Popen", ()),
        ("ctypes.dlopen", ()),
        ("import", ("tokenizers",)),
    ],
)
def test_worker_policy_without_external_traffic(event, args):
    with pytest.raises(PermissionError):
        reader.worker_policy(event, args)


def test_short_and_overflow_probe(helper):
    for raw, expected in ((b"x", 2), (b"xx", 1)):
        with pytest.raises(helper.Failure):
            helper.digest_stream(io.BytesIO(raw), expected, helper.ReadBudget(100))
