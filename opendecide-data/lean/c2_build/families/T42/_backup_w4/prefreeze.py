"""families/T42/prefreeze.py: parallel IN-MEMORY build + the A45 pre-freeze gates for T42 (nothing is written to disk but
a metrics file of numbers). Workers each run pilot.build_pilot on a disjoint seed block; the results are merged in the parent
through pipes (no row file).  Usage (from lean/c2_build):
  ../../.venv/bin/python -B families/T42/prefreeze.py --n 5000 --workers 9 --out families/T42/PREFREEZE_METRICS.json [--g15]
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))


def _work(args):
    n, base, g15 = args
    import pilot
    import pilot_loaders as PL
    from families.T42 import run_pilot_i1 as RUN
    PL.LOADERS["T42"] = RUN._t42
    RUN.install_patches()
    with PL.LOADERS["T42"]() as kit:
        b = pilot.build_pilot(kit, n, seed_base=base, run_g15=g15)
    for u, info in enumerate(b.infos):
        pass
    return b


def build(n, workers, g15=False, seed0=None):
    import pilot
    seed0 = pilot.SEED_BASE if seed0 is None else seed0
    per = -(-n // workers)
    per = -(-per // 4) * 4
    jobs = [(per, seed0 + w * 1_000_000, g15) for w in range(workers)]
    ctx = mp.get_context("fork")
    with ctx.Pool(workers) as pool:
        builds = pool.map(_work, jobs, chunksize=1)
    merged = pilot.Build("T42")
    off = 0
    for b in builds:
        for info in b.infos:
            info.unit += off
        merged.infos += b.infos
        merged.units += b.units
        merged.rels += b.rels
        off += len(b.units)
    st = {k: sum(b.stats.get(k, 0) for b in builds) for k in ("rows_written", "units_written", "units_attempted", "units_dropped")}
    drops = {}
    for b in builds:
        for g, c in b.stats["drops_by_gate"].items():
            drops[g] = drops.get(g, 0) + c
    st["drops_by_gate"] = drops
    st["reached_target"] = all(b.stats["reached_target"] for b in builds)
    merged.stats = st
    return merged


def analyze(b, quick=False):
    import pilot
    from families.T42 import probes as PR
    infos = b.infos
    out_i = [i for i in infos if i.row["meta"]["qform"] in ("ch_output", "ch_return")]
    eq_i = [i for i in infos if i.row["meta"]["qform"] == "ch_equiv"]
    res = {"n_rows": len(infos), "n_output": len(out_i), "n_equiv": len(eq_i)}
    g6 = pilot.g6(infos)
    res["g6_all"] = {"verdict": g6["verdict"], "choice": g6["choice"], "fails": g6["fails"]}
    for nm, part in (("output", out_i), ("equiv", eq_i)):
        gc = pilot.g6_choice(part)
        ch = gc["chance"]
        fails = [(v, m, gc[v][m]) for v in ("a_question", "b_options", "c_card_without_question", "d_meta") for m in ("lr", "gbt")
                 if gc[v][m] > ch + 0.02 + 1e-12]
        res["g6_" + nm] = {"n": gc["n"], "chance": ch, "views": {v: gc[v] for v in ("a_question", "b_options", "c_card_without_question", "d_meta")},
                           "fails": fails, "pass": not fails}
    g7 = pilot.g7(infos)
    res["g7"] = {"verdict": g7["verdict"], "n_tests": g7["n_tests"], "choice_fails": g7["choice_fails"][:8], "top5": g7["top5_choice"]}
    for nm, part in (("output", out_i), ("equiv", eq_i)):
        g = pilot.g7(part)
        res["g7_" + nm] = {"verdict": g["verdict"], "n_tests": g["n_tests"], "choice_fails": g["choice_fails"][:8], "top5": g["top5_choice"]}
    if len(eq_i) > 100:   # diagnostic: which single numeric meta feature predicts the equivalence label (card-grouped CV, GBT)
        import numpy as np
        from sklearn.ensemble import HistGradientBoostingClassifier
        from sklearn.model_selection import GroupKFold
        labs = ["SAME", "DIFFERS_TYPICAL", "DIFFERS_EDGE"]
        y = np.array([labs.index(i.row["gold"]) for i in eq_i])
        grp = [i.row["meta"]["card_id"] for i in eq_i]
        F = [pilot.meta_features(i)[1] for i in eq_i]
        diag = {}
        for kf in F[0]:
            X = np.array([[f[kf]] for f in F])
            pr = np.zeros(len(y), int)
            for tr, te in GroupKFold(5).split(X, y, groups=grp):
                pr[te] = HistGradientBoostingClassifier(max_iter=60, random_state=0).fit(X[tr], y[tr]).predict(X[te])
            diag[kf] = round(float((pr == y).mean()), 4)
        res["eq_meta_single"] = diag
    res["options_only"] = PR.options_only(infos)
    res["formatting_only"] = PR.formatting_only(infos)
    res["diff_size"] = PR.diff_size(infos)
    res["cues"] = PR.cues(infos)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5000)
    ap.add_argument("--workers", type=int, default=9)
    ap.add_argument("--g15", action="store_true")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    t0 = time.time()
    b = build(a.n, a.workers, a.g15)
    print("built", len(b.infos), "rows", round(time.time() - t0), "s", b.stats, flush=True)
    res = analyze(b)
    res["build_stats"] = b.stats
    res["seconds"] = round(time.time() - t0)
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    brief = {"g6_all_fails": [(f["view"], f["model"], f["acc"]) for f in res["g6_all"]["fails"]], "g6_all_chance": res["g6_all"]["choice"]["chance"],
             "g6_output": res["g6_output"]["fails"], "g6_equiv": res["g6_equiv"]["fails"], "g7": res["g7"]["verdict"],
             "g7_fails": [(f["feature"], f["gold_hits"], f["expected"]) for f in res["g7"]["choice_fails"]],
             "oo": {k: (v if k == "pass" else {m: v[m]["delta_pp"] for m in ("lr", "gbt")}) for k, v in res["options_only"].items()},
             "fo": {k: (v if k == "pass" else {m: v[m]["delta_pp"] for m in ("lr", "gbt")}) for k, v in res["formatting_only"].items()},
             "diff": {m: res["diff_size"]["models"][m] for m in ("lr", "gbt")}}
    print(json.dumps(brief, indent=None, default=str))
