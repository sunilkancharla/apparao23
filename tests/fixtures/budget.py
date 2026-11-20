"""One finite meter for the routine suite's owned Python children and output."""

import locale
import subprocess
import sys
import threading
import time
from collections.abc import Callable


class BudgetExceeded(RuntimeError):
    """Sticky stop boundary; an exhausted allocation cannot be reused."""


class Budget:
    """Thread-safe admission and retained-output accounting, with no silent reset."""

    def __init__(
        self,
        *,
        starts: int,
        output_bytes: int,
        seconds: float,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if (
            type(starts) is not int
            or type(output_bytes) is not int
            or starts < 1
            or output_bytes < 0
            or seconds <= 0
        ):
            raise ValueError("Budget limits must be positive, with nonnegative output")
        self.max_starts, self.max_output = starts, output_bytes
        self.clock, self.deadline = clock, clock() + seconds
        self.starts_used = self.output_used = 0
        self.purposes: list[str] = []
        self.stopped = False
        self.lock = threading.Lock()

    def _check(self) -> None:
        if self.stopped or self.clock() >= self.deadline:
            self.stopped = True
            raise BudgetExceeded("Execution allocation exhausted")

    def charge_start(self, purpose: str) -> None:
        """Charge before launching; failed launches keep their charge."""
        with self.lock:
            self._check()
            if self.starts_used >= self.max_starts:
                self.stopped = True
                raise BudgetExceeded("Process-start allocation exhausted")
            self.starts_used += 1
            self.purposes.append(purpose)

    def retain(self, value: bytes) -> bytes:
        """Refuse a chunk before retaining bytes beyond the shared cap."""
        with self.lock:
            self._check()
            if self.output_used + len(value) > self.max_output:
                self.stopped = True
                raise BudgetExceeded("Retained-output allocation exhausted")
            self.output_used += len(value)
            return value


class MeteredProcess:
    """Popen adapter with concurrent bounded pipe draining and owned cleanup."""

    def __init__(self, original, budget: Budget, args, **kwargs):
        platform_probe = args == "ver" and kwargs.get("shell") is True
        command = args if platform_probe else list(args)
        if not platform_probe and (
            isinstance(args, str) or command[0] != sys.executable
        ):
            raise BudgetExceeded(
                "Routine harness only admits the project Python interpreter"
            )
        for key in ("stdout", "stderr"):
            if kwargs.get(key) not in (subprocess.PIPE, subprocess.DEVNULL):
                raise BudgetExceeded(
                    "Child output must be captured or discarded explicitly"
                )
        self.text = kwargs.pop("text", False) or kwargs.pop("universal_newlines", False)
        self.encoding = kwargs.pop("encoding", None) or "utf-8"
        if self.encoding == "locale":
            self.encoding = locale.getencoding()
        self.errors = kwargs.pop("errors", None) or "strict"
        budget.charge_start(
            "windows_platform_ver" if platform_probe else "routine_child"
        )
        self.process = original(command, **kwargs)
        self.budget = budget
        self.error = None
        self.buffers: list[list[bytes]] = [[], []]
        self.threads = []
        self.timer = threading.Timer(
            max(0.01, budget.deadline - budget.clock()), self._expire
        )
        self.timer.daemon = True
        self.timer.start()
        for index, stream in enumerate((self.process.stdout, self.process.stderr)):
            if stream is not None:
                thread = threading.Thread(
                    target=self._drain, args=(stream, index), daemon=True
                )
                thread.start()
                self.threads.append(thread)

    def _expire(self):
        self.budget.stopped = True
        self.process.kill()

    def _drain(self, stream, index):
        try:
            while chunk := stream.read(4096):
                self.buffers[index].append(self.budget.retain(chunk))
        except BudgetExceeded as error:
            self.error = error
            self.process.kill()
        finally:
            stream.close()

    def __getattr__(self, name):
        return getattr(self.process, name)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.timer.cancel()
        if self.process.poll() is None:
            self.process.kill()
        self.process.wait(timeout=5)
        for thread in self.threads:
            thread.join(timeout=5)

    def communicate(self, input=None, timeout=None):
        """Wait only within both caller and shared wall-clock boundaries."""
        if input is not None:
            raise BudgetExceeded("Interactive child input is outside this harness")
        remaining = max(0.01, self.budget.deadline - self.budget.clock())
        self.process.wait(timeout=min(timeout or remaining, remaining))
        for thread in self.threads:
            thread.join(timeout=remaining)
        if self.error is not None:
            raise self.error
        self.budget._check()
        results = [b"".join(chunks) for chunks in self.buffers]
        if self.text:
            return tuple(
                value.decode(self.encoding, self.errors).replace("\r\n", "\n")
                for value in results
            )
        return tuple(results)
