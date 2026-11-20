"""Synthetic T12 baseline contracts; no user documents or inference."""

import math
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import storage_trial as trial


class StorageContracts(unittest.TestCase):
    """Exercise real SQLite/file boundaries and independently calculated ranking."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=trial.RUN)
        self.addCleanup(self.temp.cleanup)
        self.store = trial.Store(Path(self.temp.name))
        self.addCleanup(self.store.close)
        self.vector = [1.0] + [0.0] * 767

    def populate(self):
        self.store.add_document(
            "library", b"same synthetic bytes", "library", ["a", "b"]
        )
        self.store.add_document("a-only", b"same synthetic bytes", "a", ["a"])
        self.store.add_document("b-only", b"other synthetic bytes", "b", ["b"])

    def test_vector_validation(self):
        for value in ([], [0.0] * 768, [math.nan] * 768, [math.inf] * 768):
            with self.assertRaises(ValueError):
                trial.pack_vector(value)
        with self.assertRaises(ValueError):
            trial.unpack_vector(b"corrupt")

    def test_scoped_ranking_not_global_topk_and_reference(self):
        self.populate()
        for i, doc in enumerate(("library", "a-only", "b-only")):
            vector = [0.8, 0.6] + [0.0] * 766 if i < 2 else self.vector
            self.store.add_chunk(f"c{i}", doc, vector, trial.VERSION)
        actual = self.store.search("a", self.vector, trial.VERSION)
        self.assertEqual([row[0] for row in actual], ["c0", "c1"])
        expected = trial.reference_rank(
            self.store.eligible("a", trial.VERSION), self.vector
        )
        self.assertEqual([row[0] for row in expected], [row[0] for row in actual])
        for left, right in zip(actual, expected, strict=True):
            self.assertAlmostEqual(left[1], right[1], delta=1e-6)
        self.assertEqual(self.store.search("unrelated", self.vector, trial.VERSION), [])

    def test_dedup_is_distinct_from_ownership_and_idempotence(self):
        self.populate()
        self.store.add_document("a-only", b"same synthetic bytes", "a", ["a"])
        self.assertEqual(self.store.count("contents"), 2)
        self.assertEqual(self.store.count("documents"), 3)
        self.store.add_chunk("c", "a-only", self.vector, trial.VERSION)
        self.store.add_chunk("c", "a-only", self.vector, trial.VERSION)
        self.assertEqual(self.store.count("chunks"), 1)
        with self.assertRaises(ValueError):
            self.store.add_document("a-only", b"changed", "a", ["a"])
        with self.assertRaises(ValueError):
            self.store.add_chunk("c", "b-only", self.vector, trial.VERSION)

    def test_delete_chat_preserves_library_and_other_bytes(self):
        self.populate()
        with self.assertRaises(ValueError):
            self.store.delete_conversation("library")
        with self.assertRaises(ValueError):
            self.store.remove_library("library")
        self.store.delete_conversation("a")
        self.assertEqual(self.store.document_ids(), ["b-only", "library"])
        self.assertEqual(self.store.count("contents"), 2)
        self.store.delete_conversation("b")
        self.assertEqual(self.store.document_ids(), ["library"])
        self.store.remove_library("library")
        self.assertEqual(self.store.count("contents"), 0)

    def test_version_mismatch_refused_and_rebuild_retains_anchor(self):
        self.populate()
        self.store.add_chunk("c", "library", self.vector, trial.VERSION)
        with self.assertRaises(ValueError):
            self.store.search("a", self.vector, "different-model")
        self.store.con.execute(
            "UPDATE chunks SET version='old-extraction' WHERE id='c'"
        )
        with self.assertRaises(ValueError):
            self.store.search("a", self.vector, trial.VERSION)
        self.store.rebuild("c", self.vector, trial.VERSION)
        self.assertEqual(self.store.search("a", self.vector, trial.VERSION)[0][0], "c")
        self.assertEqual(
            self.store.con.execute("SELECT anchor FROM chunks").fetchone()[0],
            trial.ANCHOR,
        )

    def test_missing_original_and_corrupt_vector_never_retrieved(self):
        self.populate()
        self.store.add_chunk("c", "library", self.vector, trial.VERSION)
        self.store.con.execute("UPDATE chunks SET vector=? WHERE id='c'", (b"bad",))
        with self.assertRaises(ValueError):
            self.store.search("a", self.vector, trial.VERSION)
        self.store.rebuild("c", self.vector, trial.VERSION)
        path = self.store.content_path("library")
        path.unlink()
        with self.assertRaises(ValueError):
            self.store.search("a", self.vector, trial.VERSION)

    def test_path_refusal_and_orphan_reconciliation_is_nondestructive(self):
        with self.assertRaises(ValueError):
            self.store.safe("../escape")
        with self.assertRaises(ValueError):
            self.store.safe("https://example.invalid/a")
        orphan = self.store.write_original(b"orphan fixture")
        unknown = self.store.root / "unknown"
        unknown.write_bytes(b"unowned fixture")
        result = self.store.reconcile()
        self.assertEqual(result["orphan_markers"], 1)
        self.assertTrue(orphan.exists())
        self.assertTrue(unknown.exists())

    def test_sql_rollback_and_integrity_on_reopen(self):
        self.populate()
        self.store.con.execute("BEGIN IMMEDIATE")
        self.store.con.execute("DELETE FROM refs WHERE conversation='a'")
        self.store.con.rollback()
        self.assertEqual(self.store.count("refs"), 4)
        self.assertEqual(
            self.store.con.execute("PRAGMA integrity_check").fetchone()[0], "ok"
        )
        self.assertEqual(
            self.store.con.execute("PRAGMA foreign_key_check").fetchall(), []
        )

    def test_shared_meter_and_worker_boundaries(self):
        state = {
            "started": trial.time.time(),
            "used": {"tests": 1},
            "limits": {"tests": 2},
        }
        trial.check_budget(state, "tests", 1)
        with self.assertRaises(RuntimeError):
            trial.check_budget(state, "tests", 2)
        good = {"available": 4 * 1024**3, "controller": 512 * 1024**2}
        trial.check_sample(good, 0.3)
        for bad, gap in (
            (good, 0.300001),
            ({**good, "available": 1}, 0.1),
            ({**good, "controller": 512 * 1024**2 + 1}, 0.1),
        ):
            with self.assertRaises(RuntimeError):
                trial.check_sample(bad, gap)

    def test_runtime_starts_only_for_fixed_worker_modes(self):
        runner = object.__new__(trial.Runner)
        with self.assertRaises(ValueError):
            runner.run("unapproved-command", "untrusted")

    def test_reference_detects_reversed_order_mutation(self):
        self.populate()
        self.store.add_chunk("close", "library", self.vector, trial.VERSION)
        self.store.add_chunk("far", "library", [0.0, 1.0] + [0.0] * 766, trial.VERSION)
        gold = trial.reference_rank(
            self.store.eligible("a", trial.VERSION), self.vector
        )
        actual = self.store.search("a", self.vector, trial.VERSION)
        self.assertEqual(actual[0][0], "close")
        self.assertNotEqual([x[0] for x in reversed(actual)], [x[0] for x in gold])


if __name__ == "__main__":
    unittest.main()
