"""Option-order drift on DEV choice rows for 4B-E: single read vs 2-view (normal + reversed) read, under reversal
and seeded rotation (the two OHS-3 twin kinds). Dev only; never OHS."""
import json
from collections import defaultdict
L = lambda p: {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(p)}
SPL = ["dev", "dev_claims", "dev_nc", "devp_card", "devzs", "hard_dev", "pg_dev", "taskbank_dev"]
def pred(p):
    b = max(p.values()); t = [k for k, v in p.items() if abs(v - b) < 1e-12]; return t[0] if len(t) == 1 else None
agg = defaultdict(list)
for s in SPL:
    rows = {json.loads(l)["id"]: json.loads(l) for l in open(f"data/{s}.jsonl")}
    I, T = L(f"preds_{s}/q35_4b_pxE_parity.jsonl"), L(f"preds_{s}/q35_4b_pxE_tta.jsonl")
    R, RT = L(f"drift/out/q35_4b_pxE__{s}__rot.jsonl"), L(f"drift/out/q35_4b_pxE__{s}__rot_tta.jsonl")
    for i, r in rows.items():
        if r["qtype"] != "choice" or i not in R: continue
        o = r["options"]; n = len(o)
        a = {k: I[i][k] for k in o}; t = {k: T[i][k] for k in o}; rev = {k: 2 * t[k] - a[k] for k in o}
        ro, rt = {k: R[i][k] for k in o}, {k: RT[i][k] for k in o}
        b = "2-4" if n <= 4 else "5-9" if n <= 9 else "10+"
        for key in ("all", b, s):
            g = agg[key]
            g.append(dict(n=1,
                acc_single=pred(a) == r["gold"], acc_tta=pred(t) == r["gold"],
                acc_rot=pred(ro) == r["gold"], acc_rot_tta=pred(rt) == r["gold"],
                drift_rev_single=pred(a) is None or pred(a) != pred(rev),
                drift_rot_single=pred(a) is None or pred(ro) is None or pred(a) != pred(ro),
                drift_rev_tta=pred(t) is None or False,  # tta(identity) == tta(reversed) by construction
                drift_rot_tta=pred(t) is None or pred(rt) is None or pred(t) != pred(rt)))
def m(g, k): return 100 * sum(x[k] for x in g) / len(g)
print(f"{'group':14s} {'n':>5s} | {'acc 1-read':>10s} {'acc 2-view':>10s} | {'rev drift 1':>11s} {'rot drift 1':>11s} {'OHS3-mix 1':>10s} | {'rev drift 2':>11s} {'rot drift 2':>11s} {'OHS3-mix 2':>10s}")
for key in ["all", "2-4", "5-9", "10+"] + SPL:
    g = agg[key]
    if not g: continue
    mix1 = (149 * m(g, "drift_rev_single") + 155 * m(g, "drift_rot_single")) / 304
    mix2 = (149 * m(g, "drift_rev_tta") + 155 * m(g, "drift_rot_tta")) / 304
    print(f"{key:14s} {len(g):5d} | {m(g,'acc_single'):10.2f} {m(g,'acc_tta'):10.2f} | {m(g,'drift_rev_single'):11.2f} {m(g,'drift_rot_single'):11.2f} {mix1:10.2f} | {m(g,'drift_rev_tta'):11.2f} {m(g,'drift_rot_tta'):11.2f} {mix2:10.2f}")
g = agg["all"]
print(f"\nrotated-view accuracy: single {m(g,'acc_rot'):.2f}, 2-view {m(g,'acc_rot_tta'):.2f}")
