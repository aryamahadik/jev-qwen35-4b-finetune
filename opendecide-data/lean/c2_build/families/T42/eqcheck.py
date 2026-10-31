"""families/T42/eqcheck.py: in-memory equivalence-only build (sampler S3) + the A45/A46 equivalence-head gates. Writes nothing
but a numbers-only metrics file. Usage (from lean/c2_build): python -B families/T42/eqcheck.py --n 1404 --workers 3 [--out f.json]"""
from __future__ import annotations

import argparse
import collections
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
    n, base = args
    import pilot
    import pilot_loaders as PL
    from families.T42 import run_pilot_i1 as RUN
    PL.LOADERS["T42"] = RUN._t42
    RUN.install_patches()
    with PL.LOADERS["T42"]() as kit:
        kit.plugin.SAMPLERS = ("S3",)
        return pilot.build_pilot(kit, n, seed_base=base, run_g15=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1404)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    import numpy as np
    import pilot
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.model_selection import GroupKFold
    from families.T42 import plugin as P, probes as PR
    t0 = time.time()
    per = -(-a.n // a.workers)
    per = -(-per // 156) * 156
    with mp.get_context("fork").Pool(a.workers) as pool:
        builds = pool.map(_work, [(per, pilot.SEED_BASE + w * 1_000_000) for w in range(a.workers)], chunksize=1)
    infos = [i for b in builds for i in b.infos]
    drops = collections.Counter()
    for b in builds:
        drops.update(b.stats["drops_by_gate"])
    att = sum(b.stats["units_attempted"] for b in builds)
    print("built", len(infos), "rows", att, "attempts", dict(drops), round(time.time() - t0), "s", flush=True)
    res = {"n": len(infos), "attempted": att, "drops": dict(drops)}
    # label x skeleton and token-coverage checks (specs only)
    tab = collections.Counter((i.spec.structure["label"], i.spec.structure["skeleton"]) for i in infos)
    res["label_x_skeleton_min_max"] = [min(tab.values()), max(tab.values())]
    res["label_counts"] = dict(collections.Counter(i.spec.structure["label"] for i in infos))
    res["dbin_by_label"] = {l: dict(sorted(collections.Counter(i.spec.structure["diff_bin"] for i in infos
                                                             if i.spec.structure["label"] == l).items())) for l in P.LABELS}
    ren = set(P.GE.ALT)
    miss = collections.Counter()
    for i in infos:
        st = i.spec.structure
        v = set(P.plugin_vocab(st["skeleton"], P.TRAIN_OPS)) if hasattr(P, "plugin_vocab") else None
    gc = pilot.g6_choice(infos)
    ch = gc["chance"]
    res["g6"] = {"n": gc["n"], "chance": ch, **{v: gc[v] for v in ("a_question", "b_options", "c_card_without_question", "d_meta")}}
    res["g6_fails"] = [(v, m, gc[v][m]) for v in ("a_question", "b_options", "c_card_without_question", "d_meta") for m in ("lr", "gbt")
                       if gc[v][m] > ch + 0.02 + 1e-12]
    g7 = pilot.g7(infos)
    res["g7"] = {"verdict": g7["verdict"], "n_tests": g7["n_tests"], "fails": [(f["feature"], f["gold_hits"], f["expected"]) for f in g7["choice_fails"][:8]]}
    labs = ["SAME", "DIFFERS_TYPICAL", "DIFFERS_EDGE"]
    y = np.array([labs.index(i.row["gold"]) for i in infos])
    grp = [i.row["meta"]["card_id"] for i in infos]
    F = [pilot.meta_features(i)[1] for i in infos]
    diag = {}
    for kf in F[0]:
        X = np.array([[f[kf]] for f in F])
        pr = np.zeros(len(y), int)
        for tr, te in GroupKFold(5).split(X, y, groups=grp):
            pr[te] = HistGradientBoostingClassifier(max_iter=60, random_state=0).fit(X[tr], y[tr]).predict(X[te])
        diag[kf] = round(float((pr == y).mean()), 4)
    res["meta_single"] = diag
    for nm, fn in (("options_only", PR.options_only), ("formatting_only", PR.formatting_only), ("diff_size", PR.diff_size)):
        try:
            r = fn(infos)
            res[nm] = r
        except Exception as e:  # noqa: BLE001
            res[nm] = f"{type(e).__name__}: {e}"[:200]
    res["seconds"] = round(time.time() - t0)
    brief = {"n": res["n"], "drops": res["drops"], "ls_minmax": res["label_x_skeleton_min_max"], "g6": {v: res["g6"][v] for v in ("a_question", "b_options", "c_card_without_question", "d_meta")},
             "chance": ch, "g6_fails": res["g6_fails"], "g7": res["g7"], "meta_single": diag}
    for nm in ("options_only", "formatting_only", "diff_size"):
        r = res[nm]
        brief[nm] = r if isinstance(r, str) else json.loads(json.dumps(r, default=str))
    print(json.dumps(brief, default=str)[:6000])
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")


if __name__ == "__main__":
    main()
