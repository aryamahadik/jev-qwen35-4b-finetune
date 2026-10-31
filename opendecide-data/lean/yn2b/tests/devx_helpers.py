"""Shared helpers for reviewer R's devx tests: one cached in-memory build of the five devx families per process
(golden_src/gen3/dx_*.py via yn2b/build_devx.py). Nothing here writes a file."""
from __future__ import annotations

import functools
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
GEN3 = LEAN / "golden_src" / "gen3"
for _p in (str(GEN3), str(LEAN / "yn2b"), str(LEAN)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

import build_devx as bd  # noqa: E402
import dx_common as dx  # noqa: E402
import mv_core as mv  # noqa: E402

KEYS = tuple(bd.MODULES)
FAMILY_CODE = {"gen3_rule_chain": "f1", "gen3_tool_guard": "f2", "gen3_state_track": "f3",
               "gen3_lead_score": "f5", "gen3_def_literal": "f6"}


@functools.lru_cache(maxsize=None)
def built() -> dict:
    return bd.build(list(KEYS))


def rows_sha(rows: list) -> str:
    return hashlib.sha256("\n".join(json.dumps(r, sort_keys=True, ensure_ascii=False) for r in rows).encode()).hexdigest()
