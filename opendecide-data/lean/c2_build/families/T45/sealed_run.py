"""families/T45/sealed_run.py: the sealed-run entry point of T45 (A42-D 13.1). NOTHING is written here: a sealed agent
calls emit_sealed() in its own process and writes the returned rows itself.

  from families.T45.sealed_run import emit_sealed
  out = emit_sealed(n_items=400, seed0=<a seed range the sealed agent owns, never below 7_000_000>, workers=4)
  out["rows"]        400 row dicts (sampler S5: held-out fault type `stale_noop`, held-out registers memo / journal, dev_only)
  out["stats"]       counts (rows, units attempted / dropped by gate, label counts, fault counts, wall seconds)

S5 draws the held-out fault type only through HELD_OUT_SAMPLERS; the training samplers (S1-S4) cannot reach it (tested). Every
unit passes the same program gates as a training unit (G2 G3 G4 G-SL G-LEX G15 schema options). If a fix changes oracle code
that this mode shares, the sealed agent re-runs emit_sealed over the frozen seed range and drops (never relabels) every item whose
gold changed (A42-D 3.6).
"""
from __future__ import annotations

import sys
import time
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import pipeline  # noqa: E402
from families.T45 import plugin as P  # noqa: E402


def emit_sealed(n_items: int = 400, seed0: int = 7_000_000, workers: int = 4, run_g15: bool = True,
                max_attempt_factor: int = 4) -> dict:
    t0 = time.time()
    plugin, ctx = P.make_plugin()
    P.warm_cache(workers=workers)
    rows, rels, drops, labels, faults = [], [], Counter(), Counter(), Counter()
    seed = seed0
    attempts = 0
    while len(rows) < n_items and attempts < max_attempt_factor * n_items:
        attempts += 1
        try:
            spec = plugin.sample(seed, "S5")
        except Exception as e:  # noqa: BLE001
            drops["sample"] += 1
            seed += 1
            continue
        seed += 1
        res = pipeline.build_unit(plugin, spec, ctx, run_g15=run_g15)
        if not res.ok:
            for g in {g for g, _ in res.problems}:
                drops[g] += 1
            continue
        rows += res.rows[:1]
        labels[spec.structure["gold"]] += 1
        faults[spec.structure["fault"]] += 1
    rows = rows[:n_items]
    return {"rows": rows, "stats": {"rows": len(rows), "attempts": attempts, "next_seed": seed, "drops_by_gate": dict(drops),
                                    "gold_counts": dict(labels), "fault_counts": dict(faults),
                                    "seconds": round(time.time() - t0, 1)}}
