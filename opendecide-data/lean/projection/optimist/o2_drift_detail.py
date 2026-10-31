"""Optimist check 2 (read-only): detail for the option-order drift endpoint.
(a) sanity of the derived reversed view (negative derived probabilities = noise between the two reads);
(b) 4B-E drift by option count and by whether the identity read is right, on dev;
(c) Jev ties on choice rows (a tie counts as drift AND as wrong in PREREG_OHS3) on OHS-1/OHS-2.
"""
import json, os
from collections import defaultdict
import numpy as np
os.chdir("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
load = lambda p: {json.loads(l)["id"]: json.loads(l) for l in open(p)}
def probs(r, pr):
    keys = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
    return {k: float(pr.get(k, 0.0)) for k in keys}
def pred(p):
    b = max(p.values()); t = [k for k, v in p.items() if v == b]; return t[0] if len(t) == 1 else None
SPL = ["dev", "dev_claims", "dev_nc", "dev_negwords", "devp_card", "devzs", "hard_dev", "pg_dev", "taskbank_dev"]
neg, mins, byk, byc = 0, [], defaultdict(list), defaultdict(list)
acc_by = defaultdict(list)
for s in SPL:
    rows = load(f"data/{s}.jsonl")
    pp = {k: v["probs"] for k, v in load(f"preds_{s}/q35_4b_pxE_parity.jsonl").items()}
    pt = {k: v["probs"] for k, v in load(f"preds_{s}/q35_4b_pxE_tta.jsonl").items()}
    for i, r in rows.items():
        if r["qtype"] != "choice" or i not in pp: continue
        a, t = probs(r, pp[i]), probs(r, pt[i]); rev = {k: 2 * t[k] - a[k] for k in a}
        m = min(rev.values()); mins.append(m); neg += m < -1e-3
        n = len(r["options"]); b = "2-4" if n <= 4 else "5-9" if n <= 9 else "10-19" if n <= 19 else "20-39" if n <= 39 else "40+"
        f = pred(a) != pred(rev); byk[b].append(f); acc_by[b].append(pred(a) == r["gold"])
        byc[pred(a) == r["gold"]].append(f)
print(f"(a) derived reversed view: rows with a derived prob < -0.001: {neg} of {len(mins)}; min {min(mins):.4f}")
print("(b) 4B-E dev reversed-order drift by option count (identity accuracy in brackets):")
for b in ["2-4", "5-9", "10-19", "20-39", "40+"]:
    if byk[b]: print(f"    {b:6s} n={len(byk[b]):5d} drift {100*np.mean(byk[b]):5.2f}%  [acc {100*np.mean(acc_by[b]):.1f}]")
print(f"    drift when identity read is right {100*np.mean(byc[True]):.2f}% (n={len(byc[True])}), wrong {100*np.mean(byc[False]):.2f}% (n={len(byc[False])})")
print("(c) Jev ties / missing on choice rows (would count as drift and as wrong under PREREG_OHS3):")
for split in ("ohs", "ohs2"):
    rows = load(f"data/{split}.jsonl")
    for j in ("jev_guard", "jev_r2_guard"):
        P = {k: v["probs"] for k, v in load(f"preds_{split}/{j}.jsonl").items()}
        ch = [i for i, r in rows.items() if r["qtype"] == "choice"]
        ties = sum(1 for i in ch if i in P and pred(probs(rows[i], P[i])) is None); miss = sum(1 for i in ch if i not in P)
        wide = [i for i in ch if len(rows[i]["options"]) > 26]
        tw = sum(1 for i in wide if i in P and pred(probs(rows[i], P[i])) is None)
        print(f"    {split:4s} {j:13s} choice rows {len(ch)}: ties {ties} ({100*ties/len(ch):.2f}%), missing {miss}; >26 options: ties {tw} of {len(wide)}")
