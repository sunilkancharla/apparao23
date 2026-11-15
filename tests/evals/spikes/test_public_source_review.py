"""Fake-HTTP controls for the bounded R1 research helper; no network/native loads."""

import importlib.util
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location(
    "public_source_review", Path(__file__).with_name("public_source_review.py")
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReviewTests(unittest.TestCase):
    """Exercise actual request/body admission using fake transport and clock."""

    def state(self):
        return {"http_attempts": 0, "body_bytes": 0, "pending_bytes": 0}

    def test_url_boundary(self):
        for url in (
            "http://github.com/ollama/ollama",
            "https://github.com.evil.invalid/ollama/ollama",
            "https://user:secret@github.com/ollama/ollama",
            "https://github.com/unrelated/private",
            "https://api.github.com/advisories",
            "https://raw.githubusercontent.com/ollama/ollama/main/api/types.go",
        ):
            with self.assertRaises(ValueError):
                MODULE.validate_url(url)
        MODULE.validate_url(
            "https://raw.githubusercontent.com/ollama/ollama/v0.40.16/api/types.go"
        )

    def test_body_and_count_accounting(self):
        state = self.state()
        saved = []
        result = MODULE.collect(
            state, lambda: saved.append(dict(state)), [b"abc", b"def"],
            lambda: 1.0, 21.0,
        )
        self.assertEqual(result, b"abcdef")
        self.assertEqual(state["http_attempts"], 1)
        self.assertEqual(state["body_bytes"], 6)
        self.assertEqual(state["pending_bytes"], 0)
        self.assertEqual(saved[0]["pending_bytes"], 1048576)

    def test_attempt_exhaustion_before_body(self):
        state = self.state() | {"http_attempts": 32}
        with self.assertRaises(RuntimeError):
            MODULE.collect(state, lambda: None, [b"x"], lambda: 1.0, 2.0)
        self.assertEqual(state["body_bytes"], 0)

    def test_total_bytes_reserved_before_request(self):
        state = self.state() | {"body_bytes": 8 * 1048576}
        with self.assertRaises(RuntimeError):
            MODULE.collect(state, lambda: None, [b"x"], lambda: 1.0, 2.0)
        self.assertEqual(state["http_attempts"], 0)

    def test_response_limit_keeps_conservative_reservation(self):
        state = self.state()
        with self.assertRaises(RuntimeError):
            MODULE.collect(state, lambda: None, [b"x" * 1048577], lambda: 1.0, 2.0)
        self.assertEqual(state["pending_bytes"], 1048576)

    def test_total_deadline_not_read_timeout(self):
        state = self.state()
        with self.assertRaises(RuntimeError):
            MODULE.collect(state, lambda: None, [b"x"], lambda: 22.0, 21.0)
        self.assertEqual(state["pending_bytes"], 1048576)

    def test_partial_read_failure_keeps_reservation(self):
        def broken():
            yield b"abc"
            raise OSError("fake failure")

        state = self.state()
        with self.assertRaises(OSError):
            MODULE.collect(state, lambda: None, broken(), lambda: 1.0, 2.0)
        self.assertEqual(state["pending_bytes"], 1048576)

    def test_safe_excerpt_is_bounded(self):
        value = MODULE.excerpt("tokenize " * 100000)
        self.assertLessEqual(len(value), 40000)

    def test_exact_base_interpreter_and_isolated_worker(self):
        args = MODULE.worker_args()
        self.assertEqual(args[0].replace("\\", "/"), "F:/Python/Python314/python.exe")
        self.assertEqual(args[1:4], ["-I", "-S", "-B"])
        self.assertEqual(args[-1], "worker")


if __name__ == "__main__":
    unittest.main()
