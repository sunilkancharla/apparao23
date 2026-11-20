"""Data-only Windows ownership/resource controls; no kernel call or process start."""

import ctypes
import struct

import pytest

from app.ollama import OllamaError
from app.windows_job import (
    ExtendedLimits,
    ProcessInfo,
    StartupInfoEx,
    TcpRow,
    check_network,
    parse_tcp_table,
)


def test_win64_layouts_match_the_native_structures_used_by_the_launcher():
    assert ctypes.sizeof(ctypes.c_void_p) == 8
    assert ctypes.sizeof(ExtendedLimits) == 144
    assert ctypes.sizeof(StartupInfoEx) == 112
    assert ctypes.sizeof(ProcessInfo) == 24


def test_ipv4_tcp_table_preserves_address_port_state_and_process_identity():
    row = (
        struct.pack("<I4s", 2, bytes([127, 0, 0, 1]))
        + b"\x2c\xab\x00\x00"
        + bytes(8)
        + struct.pack("<I", 123)
    )
    rows = parse_tcp_table(struct.pack("<I", 1) + row, 2)
    assert rows == (TcpRow(2, "127.0.0.1", 11435, "0.0.0.0", 123),)
    assert check_network(rows, 11435, 123, {123, 124})


@pytest.mark.parametrize(
    "row",
    [
        TcpRow(2, "0.0.0.0", 11435, "0.0.0.0", 123),
        TcpRow(2, "127.0.0.1", 11435, "0.0.0.0", 999),
        TcpRow(5, "127.0.0.1", 12000, "1.1.1.1", 124),
        TcpRow(2, "::1", 11435, "::", 123),
    ],
)
def test_wildcard_foreign_listener_and_owned_external_peer_refuse(row):
    with pytest.raises(OllamaError):
        check_network((row,), 11435, 123, {123, 124})


def test_unrelated_established_peer_is_not_mistaken_for_owned_traffic():
    rows = (TcpRow(5, "192.0.2.1", 12000, "1.1.1.1", 999),)
    assert not check_network(rows, 11435, 123, {123})


@pytest.mark.parametrize(
    "raw,family", [(b"", 2), (struct.pack("<I", 2), 2), (bytes(4), 99)]
)
def test_invalid_or_incomplete_tcp_tables_refuse_ownership(raw, family):
    with pytest.raises(OllamaError):
        parse_tcp_table(raw, family)
