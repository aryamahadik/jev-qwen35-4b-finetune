import json, sys, os
from collections import defaultdict
import numpy as np
os.chdir("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
SPLIT, A, B = sys.argv[1], sys.argv[2], sys.argv[3]
rows = {json.loads(l)["id"]: json.loads(l) for l in open(f"data/{SPLIT}.jsonl")}
base = [i for i, r in rows.items() if r["role"] in ("aff", "choice") and not any(i.endswith(s) for s in ("_neg", "_dneg", "_para", "_yn", "_perm"))]
P = {n: {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(f"preds_{SPLIT}/{n}.jsonl")} for n in (A, B)}
def correct(n, i):
    r, pr = rows[i], P[n].get(i)
    if pr is None: return 0.0
    keys = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
    p = {k: float(pr.get(k, 0.0)) for k in keys}
    g = ("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"]
    b = max(p.values()); return float([k for k, v in p.items() if v == b] == [g])
groups = defaultdict(list)
for i in base: groups[(rows[i]["source"], rows[i]["group_id"])].append(i)
for lab, f in (("micro", lambda i: True), ("yes/no", lambda i: rows[i]["qtype"] == "noul"), ("choice", lambda i: rows[i]["qtype"] == "choice")):
    keys = [k for k in groups if any(f(i) for i in groups[k])]
    sa = np.array([sum(correct(A, i) for i in groups[k] if f(i)) for k in keys]); sb = np.array([sum(correct(B, i) for i in groups[k] if f(i)) for k in keys])
    c = np.array([sum(1 for i in groups[k] if f(i)) for k in keys], float)
    tasks = sorted({k[0] for k in keys}); per = [np.array([j for j, k in enumerate(keys) if k[0] == t]) for t in tasks]
    rng = np.random.default_rng(0); res = []
    for _ in range(10000):
        ix = np.concatenate([a[rng.integers(0, len(a), len(a))] for a in per]); res.append((sa[ix].sum() - sb[ix].sum()) / c[ix].sum())
    lo, hi = np.percentile(res, [2.5, 97.5])
    print(f"{SPLIT} {A} minus {B} {lab:7s}: {100*(sa.sum()-sb.sum())/c.sum():+.2f} pp [{100*lo:+.2f}, {100*hi:+.2f}] (n={int(c.sum())})")
