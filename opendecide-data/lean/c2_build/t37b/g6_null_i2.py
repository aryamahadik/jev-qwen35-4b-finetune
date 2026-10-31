"""A43-erratum style max-statistic permutation null for the T37b full block (pilot_i2_full), G6 yes/no part.

  cd lean/c2_build && nice -n 10 ../../.venv/bin/python -B -m t37b.g6_null_i2 [--dir pilot_i2_full] [--draws 200] [--workers 4]

A44 (c): the T37b G6 sample is the full realised block (below the 5,000 rows of spec 6.3). Observed M = max over the
yes/no views and models of (accuracy - chance), recomputed here from rows.jsonl (it must equal PILOT_REPORT G6), against
the same M under gold permutations (each partner row is its own unit: gold shuffled across rows, yes rate preserved).
Writes <dir>/A43_NULL_MAX.json. Report-only: it never changes the G6 verdict or its bar."""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2))
sys.path.insert(0, str(C2 / "zed_orch"))
import g6_null_max as GN  # noqa: E402
import pilot as PI  # noqa: E402
import pilot_t37b as PT  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="pilot_i2_full")
    ap.add_argument("--draws", type=int, default=200)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--seed", type=int, default=43)
    a = ap.parse_args(argv)
    d = Path(__file__).resolve().parent / a.dir
    rows = [json.loads(l) for l in (d / "rows.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    infos = []
    for k, r in enumerate(rows):
        i = PT._info(r)
        i.unit = k
        infos.append(i)
    log = lambda m: print(time.strftime("%H:%M:%S"), m, file=sys.stderr, flush=True)  # noqa: E731
    t0 = time.time()
    P = GN.prep_yes_no(infos)
    GN.G["seed"], GN.G["yes_no"] = a.seed, P
    cells = GN.yn_cells(P, P["y"])
    obs = max(cells.values()) - P["chance"]
    rep = json.loads((d / "PILOT_REPORT.json").read_text(encoding="utf-8"))["gates"]["G6"]["yes_no"]
    match = all(abs(round(v, 4) - rep[k.split("/")[0]][k.split("/")[1]]) < 1e-9 for k, v in cells.items())
    log(f"observed M={obs:.4f} matches PILOT_REPORT G6: {match}")
    res = GN.run_draws(a.draws, a.workers, d, log, t0)
    null = np.array([res[i]["yes_no"] for i in range(a.draws)])
    p = float((null >= obs - 1e-9).sum() + 1) / (a.draws + 1)
    out = {"dir": a.dir, "statistic": "M = max over yes/no views and models of (accuracy - chance)", "n_rows": len(rows),
           "draws": a.draws, "observed_M": round(obs, 4), "observed_matches_pilot_g6": match,
           "cells": {k: round(v, 4) for k, v in cells.items()}, "null_quantiles": {
               q: round(float(np.percentile(null, q)), 4) for q in (50, 75, 90, 95, 99)},
           "p_max_null": round(p, 4), "bar_excess": 0.02,
           "note": "report-only; the G6 bar (every view and model <= chance + 2 pp) is unchanged and binding; a family "
                   "below 5,000 rows (A44 c) is excused at p >= 0.05 only by the orchestrator's ruling"}
    (d / "A43_NULL_MAX.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
