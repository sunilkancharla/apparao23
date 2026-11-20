"""Bounded T07A evaluation controls, separate from application ingestion."""

import ctypes
import ipaddress
import struct

from embedding_budget import Budget, BudgetExceeded


class XlsBudget(Budget):
    """Persist the approved XLS allocation without changing older trial ledgers."""

    def __init__(self, path, clock=None):
        kwargs = {} if clock is None else {"clock": clock}
        super().__init__(
            path,
            limits={
                "processes": 100,
                "calls": 0,
                "downloaded": 10 * 1024**2,
                "benchmark_seconds": 1800,
            },
            **kwargs,
        )

    def download(self, size: int) -> None:
        """Count failed-transfer bytes and enforce the twenty-minute deadline."""
        if self.clock() - self.read()["provision_started"] > 1200:
            raise BudgetExceeded("Provisioning deadline")
        super().download(size)

    def memory(self, available: int, controller_commit: int) -> None:
        """Use the stricter controller guard approved for this parser trial."""
        if available < 4 * 1024**3 or controller_commit > 512 * 1024**2:
            raise BudgetExceeded("Memory headroom")


def native_denial_verified(observations: dict) -> bool:
    """Only explicit native access denial establishes the tested boundary."""
    return set(observations) == {"tcp4", "tcp6", "udp4"} and all(
        value == 10013 for value in observations.values()
    )


def probe_native_network() -> dict:
    """Probe Winsock directly without importing parsers or reading documents.

    Documentation-only IP ranges avoid addressing a real external service.
    Nonblocking connection permission, timeout, route failure and unsupported
    address families are inconclusive; none can be reported as enforced denial.
    """
    winsock = ctypes.WinDLL("ws2_32", use_last_error=True)
    socket_type = ctypes.c_size_t
    winsock.WSAStartup.argtypes = [ctypes.c_ushort, ctypes.c_void_p]
    winsock.socket.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
    winsock.socket.restype = socket_type
    winsock.ioctlsocket.argtypes = [socket_type, ctypes.c_long, ctypes.c_void_p]
    winsock.connect.argtypes = [socket_type, ctypes.c_void_p, ctypes.c_int]
    winsock.sendto.argtypes = [
        socket_type,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_void_p,
        ctypes.c_int,
    ]
    winsock.closesocket.argtypes = [socket_type]
    state = ctypes.create_string_buffer(512)
    if winsock.WSAStartup(0x0202, state):
        raise RuntimeError("Winsock startup failed")
    observations = {}
    try:
        for label, family, kind, address in [
            ("tcp4", 2, 1, "203.0.113.1"),
            ("tcp6", 23, 1, "2001:db8::1"),
            ("udp4", 2, 2, "203.0.113.1"),
        ]:
            handle = winsock.socket(family, kind, 0)
            if handle == socket_type(-1).value:
                observations[label] = winsock.WSAGetLastError()
                continue
            try:
                nonblocking = ctypes.c_ulong(1)
                if winsock.ioctlsocket(handle, -2147195266, ctypes.byref(nonblocking)):
                    raise RuntimeError("Cannot set native nonblocking probe")
                packed = ipaddress.ip_address(address).packed
                sockaddr = (
                    struct.pack("<HH4s8x", family, 0xBB01, packed)
                    if family == 2
                    else struct.pack("<HHI16sI", family, 0xBB01, 0, packed, 0)
                )
                target = ctypes.create_string_buffer(sockaddr)
                if kind == 1:
                    result = winsock.connect(handle, target, len(sockaddr))
                else:
                    result = winsock.sendto(handle, b"", 0, 0, target, len(sockaddr))
                observations[label] = 0 if result >= 0 else winsock.WSAGetLastError()
            finally:
                winsock.closesocket(handle)
    finally:
        winsock.WSACleanup()
    return observations
