import json, sys, os
from collections import defaultdict
import numpy as np
os.chdir("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
SPLIT, M = sys.argv[1], sys.argv[2]
JEVS = ["jev_guard", "jev_r2_guard"]
rows = {json.loads(l)["id"]: json.loads(l) for l in open(f"data/{SPLIT}.jsonl")}
base = [i for i, r in rows.items() if r["role"] in ("aff", "choice") and not any(i.endswith(s) for s in ("_neg", "_dneg", "_para", "_yn", "_perm"))]
P = {n: {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(f"preds_{SPLIT}/{n}.jsonl")} for n in [M] + JEVS}
def correct(n, i):
    r, pr = rows[i], P[n].get(i)
    if pr is None: return 0.0
    keys = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
    p = {k: float(pr.get(k, 0.0)) for k in keys}; g = ("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"]
    b = max(p.values()); return float([k for k, v in p.items() if v == b] == [g])
acc = lambda n, i: np.mean([correct(j, i) for j in JEVS]) if n == "JEV" else correct(n, i)
groups = defaultdict(list)
for i in base: groups[(rows[i]["source"], rows[i]["group_id"])].append(i)
for t in sorted({rows[i]["track"] for i in base}):
  for q in ("all", "noul", "choice"):
    f = lambda i: rows[i]["track"] == t and (q == "all" or rows[i]["qtype"] == q)
    keys = [k for k in groups if any(f(i) for i in groups[k])]
    if not keys: continue
    sa = np.array([sum(acc(M, i) for i in groups[k] if f(i)) for k in keys]); sj = np.array([sum(acc("JEV", i) for i in groups[k] if f(i)) for k in keys])
    c = np.array([sum(1 for i in groups[k] if f(i)) for k in keys], float)
    per = [np.array([j for j, k in enumerate(keys) if k[0] == s]) for s in sorted({k[0] for k in keys})]
    rng = np.random.default_rng(0); res = []
    for _ in range(10000):
        ix = np.concatenate([a[rng.integers(0, len(a), len(a))] for a in per]); res.append((sa[ix].sum() - sj[ix].sum()) / c[ix].sum())
    lo, hi = np.percentile(res, [2.5, 97.5])
    print(f"{SPLIT} track {t} {q:6s} n={int(c.sum()):4d}: {M} {100*sa.sum()/c.sum():.2f} vs Jev {100*sj.sum()/c.sum():.2f} diff {100*(sa.sum()-sj.sum())/c.sum():+.2f} [{100*lo:+.2f}, {100*hi:+.2f}]")
