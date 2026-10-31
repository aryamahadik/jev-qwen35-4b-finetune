"""W9 T32 diagnostic: which d_meta feature carries the choice gold. Builds N rows through the gen_full path at a seed base,
keeps choice rows, writes per-gold means (numeric) and chi2 (categorical) for ch_status and ch_due. Run from lean/c2_build."""
import argparse, json, sys, time, math
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import gen_full_c2 as G
import pilot
import numpy as np
from scipy import stats

ap = argparse.ArgumentParser(); ap.add_argument("--seed-base", type=int, required=True); ap.add_argument("--n", type=int, default=6000)
ap.add_argument("--out", required=True); a = ap.parse_args()
fam = "T32"
src = G.quarantine_sources(fam); banned = set().union(*map(set, src.values()))
with G.loader_patch(fam):
    with G.PL.open_family(fam) as kit0:
        kit, xrep = G.apply_exclusions(kit0, banned)
        rd = G.Redraw(kit.plugin, xrep["dead_qforms"]) if xrep["dead_qforms"] else None
        try:
            b = G.pilot.build_pilot(kit, a.n, seed_base=a.seed_base, run_g15=False)
        finally:
            if rd: rd.restore()
res = {}
rows = [i for i in b.infos if i.row["qtype"] == "choice"]
for qf in ("ch_status", "ch_due"):
    sel = [i for i in rows if i.row["meta"].get("qform") == qf]
    if qf == "ch_due":
        # gold class: rank of gold among sorted option dates
        gold = [str(sorted(i.row["options"]).index(i.row["gold"])) for i in sel]
    else:
        gold = [i.row["gold"] for i in sel]
    feats = [pilot.meta_features(i) for i in sel]
    classes = sorted(set(gold))
    out = {"n": len(sel), "gold_counts": {c: gold.count(c) for c in classes}, "num": {}, "cat": {}}
    for k in feats[0][1]:
        x = np.array([f[1][k] for f in feats]); g = np.array(gold)
        groups = [x[g == c] for c in classes]
        F, p = stats.f_oneway(*groups) if len(set(x)) > 1 else (0, 1)
        out["num"][k] = {"means": {c: round(float(x[g == c].mean()), 3) for c in classes}, "sd": round(float(x.std()), 3), "anova_F": round(float(F), 2), "p": float(p)}
    for k in feats[0][0]:
        v = [f[0][k] for f in feats]
        lv = sorted(set(v))
        tab = np.array([[sum(1 for vv, gg in zip(v, gold) if vv == l and gg == c) for c in classes] for l in lv])
        keep = tab.sum(1) >= 10
        tab2 = tab[keep]
        if tab2.shape[0] > 1:
            chi, p, dof, _ = stats.chi2_contingency(tab2)
            out["cat"][k] = {"levels": int(tab2.shape[0]), "chi2": round(float(chi), 1), "dof": int(dof), "p": float(p),
                             "cramer_v": round(float(math.sqrt(chi / (tab2.sum() * (min(tab2.shape) - 1)))), 3)}
    res[qf] = out
Path(a.out).write_text(json.dumps(res, indent=1))
for qf, o in res.items():
    print(qf, o["n"], o["gold_counts"])
    for k, v in sorted(o["num"].items(), key=lambda kv: kv[1]["p"])[:6]: print("  num", k, v["means"], "F", v["anova_F"], "p", "%.3g" % v["p"])
    for k, v in sorted(o["cat"].items(), key=lambda kv: kv[1]["p"])[:5]: print("  cat", k, v)
