"""Learned router for the PRISM-X cascade: logistic regression on the 2B's own output (top probability, margin,
entropy, number of options, yes/no or choice, dev split) predicts whether the 2B is wrong. Fitted on dev-select only;
the route budget is set on dev-select; reported on dev-confirm. Compare with routing by top probability.
  python router_sim.py SMALL BIG"""
import hashlib, json, math, sys
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
HERE = Path(__file__).resolve().parent
SPLITS = ["dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims", "pg_dev", "devzs", "devp_card", "dev"]
half = lambda g: "select" if int(hashlib.sha256(f"devsel:{g}".encode()).hexdigest(), 16) % 2 == 0 else "confirm"
load = lambda s, n: {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(HERE / f"preds_{s}" / f"{n}.jsonl")}
small, big = sys.argv[1], sys.argv[2]
data = {"select": [], "confirm": []}
for si, s in enumerate(SPLITS):
    S, B = load(s, small), load(s, big)
    for l in open(HERE / f"data/{s}.jsonl"):
        r = json.loads(l)
        if r["id"] not in S or r["id"] not in B:
            continue
        keys = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
        g = ("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"]
        def okp(pr):
            p = [float(pr.get(k, 0)) for k in keys]; m = max(p)
            return float([k for k, v in zip(keys, p) if v == m] == [g]), sorted(p, reverse=True)
        oks, ps = okp(S[r["id"]]); okb, _ = okp(B[r["id"]])
        tot = sum(ps) or 1; ps = [x / tot for x in ps]
        ent = -sum(x * math.log(x + 1e-12) for x in ps) / math.log(len(ps)) if len(ps) > 1 else 0.0
        f = [ps[0], ps[0] - (ps[1] if len(ps) > 1 else 0), ent, math.log(len(ps)), float(r["qtype"] == "noul")] + [float(si == k) for k in range(len(SPLITS))]
        data[half(r["group_id"])].append((f, oks, okb))
X = {k: np.array([d[0] for d in v]) for k, v in data.items()}
wrong = {k: np.array([1 - d[1] for d in v]) for k, v in data.items()}
clf = LogisticRegression(max_iter=2000).fit(X["select"], wrong["select"])
risk = {k: clf.predict_proba(X[k])[:, 1] for k in X}
base = {k: 1 - X[k][:, 0] for k in X}  # routing by top probability
def cascade(part, score, budget):
    thr = np.quantile(score["select"], 1 - budget)
    route = score[part] >= thr
    acc = np.where(route, [d[2] for d in data[part]], [d[1] for d in data[part]]).mean() * 100
    return acc, route.mean() * 100
print(f"confirm: 2B alone {100*np.mean([d[1] for d in data['confirm']]):.2f}, 4B alone {100*np.mean([d[2] for d in data['confirm']]):.2f}")
print(f"{'budget':>6} | {'top-prob routing':>22} | {'learned router':>22}")
for b in (0.2, 0.3, 0.4, 0.5):
    a1, r1 = cascade("confirm", base, b); a2, r2 = cascade("confirm", risk, b)
    print(f"{b:6.0%} | acc {a1:6.2f} routed {r1:5.1f}% | acc {a2:6.2f} routed {r2:5.1f}%")
