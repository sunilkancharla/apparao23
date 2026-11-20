"""Fake-boundary acceptance cases for FP01–FP08; no model imports/calls."""

import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "fit", Path(__file__).with_name("t17_fit_contract.py")
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def identity(**changes):
    return {
        "model": "model-hash",
        "runtime": "runtime-hash",
        "tokenizer": "tokenizer-hash",
        "rendering": "render-hash",
        "sources": ("A:revision1",),
        "context": 16,
        "branch": "plain-text",
        **changes,
    }


class FitTests(unittest.TestCase):
    def test_fp01_missing_and_malformed(self):
        for count in (None, True, -1, "2"):
            with self.assertRaises(m.Unavailable):
                m.admit(identity(), count, 3, 0)
        with self.assertRaises(m.Unavailable):
            m.admit(identity(), 2, 3, None)

    def test_fp02_snapshot_is_immutable(self):
        request = identity()
        ticket = m.admit(request, 2, 3, 0)
        request["model"] = "changed"
        with self.assertRaises(m.Unavailable):
            m.publish(ticket, request)

    def test_fp03_remove_complete_history_before_evidence(self):
        calls = []

        def oracle(h, e):
            calls.append((h, e))
            return 20 if h else 2

        result = m.pack(identity(), (("u1", "a1"),), ("A:revision1",), oracle, 3, 0)
        self.assertEqual(
            calls, [((("u1", "a1"),), ("A:revision1",)), ((), ("A:revision1",))]
        )
        self.assertEqual(result["history_pairs_removed"], 1)

    def test_fp03_lowest_ranked_evidence_removed_last(self):
        value = m.pack(
            identity(sources=("A", "B")),
            (),
            ("A", "B"),
            lambda h, e: 20 if len(e) > 1 else 2,
            3,
            0,
        )
        self.assertEqual(value["evidence"], ("A",))

    def test_fp04_eight_candidates_exhausted(self):
        calls = []
        with self.assertRaises(m.Unavailable):
            m.pack(
                identity(),
                tuple(("u", "a") for _ in range(10)),
                (),
                lambda h, e: calls.append(1) or 20,
                3,
                0,
            )
        self.assertEqual(len(calls), 8)

    def test_fp04_mandatory_overflow(self):
        with self.assertRaises(m.Unavailable):
            m.pack(identity(), (), (), lambda h, e: 20, 3, 0)

    def test_fp05_equal_needs_proof(self):
        with self.assertRaises(m.Unavailable):
            m.admit(identity(), 13, 3, 0)
        ticket = m.admit(identity(), 13, 3, 0, equality_proven=True)
        self.assertTrue(m.publish(ticket, identity()))
        with self.assertRaises(m.Unavailable):
            m.admit(identity(), 14, 3, 0, equality_proven=True)

    def test_fp06_every_identity_field_is_bound(self):
        ticket = m.admit(identity(), 2, 3, 0)
        for key in ("model", "runtime", "tokenizer", "rendering", "sources", "context"):
            changed = identity()
            changed[key] = "drift"
            with self.assertRaises(m.Unavailable):
                m.publish(ticket, changed)

    def test_fp07_cancel_and_timeout(self):
        with self.assertRaises(m.Unavailable):
            m.admit(identity(), 2, 3, 0, cancelled=True)

        def timeout(h, e):
            raise TimeoutError()

        with self.assertRaises(m.Unavailable):
            m.pack(identity(), (), (), timeout, 3, 0)
        ticket = m.admit(identity(), 2, 3, 0)
        with self.assertRaises(m.Unavailable):
            m.publish(ticket, identity(), cancelled=True)

    def test_fp06_drift_during_counting_refuses(self):
        request = identity()

        def drifting_oracle(history, evidence):
            request["model"] = "changed-during-count"
            return 2

        with self.assertRaises(m.Unavailable):
            m.pack(request, (), (), drifting_oracle, 3, 0)

    def test_fp08_unsupported_and_unrelated(self):
        with self.assertRaises(m.Unavailable):
            m.admit(identity(branch="tools"), 2, 3, 0)
        with self.assertRaises(m.Unavailable):
            m.pack(identity(), (), ("another-chat-source",), lambda h, e: 2, 3, 0)


if __name__ == "__main__":
    unittest.main()
