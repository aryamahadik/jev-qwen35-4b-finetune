"""G8 companion (r1.1 repair, builder-run): the grouped yes/no AFLite-lite of g8.py rerun on the same cached MiniLM
embeddings with the yes/no labels permuted inside each card (card yes rates kept, spec 2.1 draws them 20-80%).
If the real predictable share is within the null's range, the yes/no predictability is the per-card yes-rate
design, not a row-level cue. Also reports the within-card AUC of the held-out predicted probability. Counts only."""
import json, random
import numpy as np
from collections import defaultdict
import qc_lib as q
from sklearn.linear_model import LogisticRegression
rows, side = q.load("candidates_r1")
Z = np.load(q.TMP / "g8_emb_candidates_r1.npz")["rowemb"].astype(np.float32)
yn = np.array([i for i, r in enumerate(rows) if q.is_yn(r)])
cards = np.array([rows[i]["meta"]["card_id"] for i in yn]); uc = sorted(set(cards))
X = Z[yn].reshape(len(yn), -1); y0 = np.array([int(rows[i]["gold"]) for i in yn])
by = defaultdict(list)
for k, c in enumerate(cards):
    by[c].append(k)


def run(y, P=64):
    right = np.zeros(len(yn)); reads = np.zeros(len(yn)); pm = np.zeros(len(yn))
    for p in range(P):
        rng = random.Random(9100 + p); trc = set(rng.sample(uc, len(uc) // 2)); a = np.array([c in trc for c in cards])
        m = LogisticRegression(C=1.0, max_iter=2000, class_weight="balanced").fit(X[a], y[a])
        pr = m.predict_proba(X[~a])[:, 1]
        right[~a] += ((pr > 0.5).astype(int) == y[~a]); reads[~a] += 1; pm[~a] += pr
    sc = right / np.maximum(reads, 1); pmean = pm / np.maximum(reads, 1)
    aucs = []
    for ks in by.values():
        ks = np.array(ks); yy = y[ks]; pp = pmean[ks]
        if yy.min() != yy.max():
            pos, neg = pp[yy == 1], pp[yy == 0]
            aucs.append(float(np.mean([(u > v) + 0.5 * (u == v) for u in pos for v in neg])))
    return {"yes_no_predictable_share": round(float(((sc >= 0.75) & (reads >= 8)).mean()), 4),
            "within_card_auc_mean": round(float(np.mean(aucs)), 4)}


out = {"gate": "G8 companion (null)", "file": "out/candidates_r1.jsonl", "partitions": 64, "tau": 0.75,
       "real": run(y0), "null_within_card_permutation": []}
for s in range(5):
    y = y0.copy(); rng = np.random.default_rng(s)
    for ks in by.values():
        ks = np.array(ks); y[ks] = rng.permutation(y0[ks])
    out["null_within_card_permutation"].append(run(y))
ns = [d["yes_no_predictable_share"] for d in out["null_within_card_permutation"]]
out["null_range"] = [min(ns), max(ns)]
(q.QC / "g8_null_candidates_r1.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out))
