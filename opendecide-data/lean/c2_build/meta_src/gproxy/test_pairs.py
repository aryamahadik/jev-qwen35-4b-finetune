"""Tests for pairs.py on the programmatic held-out patterns (12 fixed-surface specs, 9 complement) and on a synthetic
realisation of the Haiku slots (stand-in surfaces; only to exercise the 150-pair path). Run from lean/c2_build:
  ../../.venv/bin/python -B -m unittest meta_src.gproxy.test_pairs   (or run this file directly)"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pairs as PR  # noqa: E402
from negtwins import heldout as H  # noqa: E402
from negtwins.test_negtwins import pair_allowed_prohibited, pair_mention_omit  # noqa: E402

ROWS = PR.load_rows(PR.DATA / "gproxy_rows.jsonl")


class Pairs(unittest.TestCase):
    def check(self, twins, index, rep, n_max):
        self.assertLessEqual(len(twins), n_max)
        self.assertEqual(rep["problems"], [])
        self.assertLessEqual(rep["max_per_pattern"], 5)
        self.assertEqual(len({i["base_id"] for i in index}), len(index))            # one pair per base
        by_id = {r["id"]: r for r in ROWS}
        for t, i in zip(twins, index):
            b = by_id[i["base_id"]]
            self.assertEqual(t["gold"], 1 - b["gold"])
            self.assertEqual(t["group_id"], b["group_id"])
            self.assertTrue(t["meta"]["never_train"])
            self.assertTrue(i["pattern"].startswith("H:"))                           # held-out patterns only
            self.assertIn(i["op"], ("FRAME_NOT", "NEG_FRAME", "FAIL_TO", "LACK", "LEX_PAIR"))

    def test_programmatic_only(self):
        tw, ix, rep = PR.build(ROWS, {})
        self.assertGreaterEqual(len(tw), 25)
        self.check(tw, ix, rep, 9 * 5)
        self.assertEqual(rep["patterns_held_out_realised"], 12)

    def test_synthetic_slots(self):
        adm = ({f"HF{i}": f"Is it plain {w} that" for i, w in enumerate("abcd", 1)} |
               {f"HN{i}": f"Is it wrong {w} that" for i, w in enumerate("abcd", 1)} |
               {f"HP{i}": {**pair_mention_omit(), "pair_id": f"H{i}"} for i in range(1, 7)} |
               {f"HP{i}": {**pair_allowed_prohibited(), "pair_id": f"H{i}"} for i in range(7, 12)})
        tw, ix, rep = PR.build(ROWS, adm)
        self.check(tw, ix, rep, 150)
        self.assertGreaterEqual(len(tw), 100)
        print("synthetic:", {k: rep[k] for k in ("pairs", "patterns_used", "complete", "by_op", "by_class")})


if __name__ == "__main__":
    unittest.main()
