"""Shared helpers for the F5 (gen3_lead_score) tests: one cached small build per process (never written to data/).

The small plan keeps every view type (score, score with a CRM record, sales-ready yes/no, judge yes/no, JB-letter,
contrast twins, format twins, attack twins) and both dev parts, at about a tenth of the SPEC counts. The full-size
SPEC gates run on the written files (test_gen3_lead_score_written.py).
"""
from __future__ import annotations

import copy
import functools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
GEN3 = LEAN / "golden_src" / "gen3"
for _p in (str(GEN3), str(LEAN)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

import mv_core as mv  # noqa: E402
import gen3_lead_score as g  # noqa: E402

SMALL_PLAN = {"train": {"score": 160, "ready": 24, "judge": 24, "jb": 16},
              "dev_iid": {"score": 30, "ready": 4, "judge": 4, "jb": 4},
              "dev_holdout": {"score": 30, "ready": 4, "judge": 4, "jb": 4}}
SMALL_ATTACK = {"train": {"score": 14, "ready": 4, "judge": 2, "jb": 2},
                "dev_iid": {"score": 2, "ready": 2, "judge": 0, "jb": 0},
                "dev_holdout": {"score": 2, "ready": 0, "judge": 2, "jb": 0}}


def with_plan(fn, plan=SMALL_PLAN, attack=SMALL_ATTACK):
    saved = (copy.deepcopy(g.PLAN_ROWS), copy.deepcopy(g.ATTACK_ROWS))
    try:
        g.PLAN_ROWS.clear()
        g.PLAN_ROWS.update(copy.deepcopy(plan))
        g.ATTACK_ROWS.clear()
        g.ATTACK_ROWS.update(copy.deepcopy(attack))
        return fn()
    finally:
        g.PLAN_ROWS.clear()
        g.PLAN_ROWS.update(saved[0])
        g.ATTACK_ROWS.clear()
        g.ATTACK_ROWS.update(saved[1])


@functools.lru_cache(maxsize=2)
def small_build(tag: str = "a"):
    """(FamilyBuilder, LeadScoreBuilder) of the small plan. tag only separates cache entries (determinism test)."""
    return with_plan(lambda: g.build())


def rows_json(rows) -> str:
    return "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows)
