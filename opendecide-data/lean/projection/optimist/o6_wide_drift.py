"""Optimist check 6 (read-only, dev only): 4B-E reversed-order drift on rows with >= 20 options, split by whether the
identity read is right, to project drift at an OHS-3-like accuracy (OHS-3 choice rows all have 20 or 40 options)."""
import json, os
import numpy as np
os.chdir("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
load = lambda p: {json.loads(l)["id"]: json.loads(l) for l in open(p)}
def pred(p):
    b = max(p.values()); t = [k for k, v in p.items() if v == b]; return t[0] if len(t) == 1 else None
SPL = ["dev", "dev_claims", "dev_nc", "dev_negwords", "devp_card", "devzs", "hard_dev", "pg_dev", "taskbank_dev"]
R, W, srcs = [], [], {}
for s in SPL:
    rows = load(f"data/{s}.jsonl")
    pp = {k: v["probs"] for k, v in load(f"preds_{s}/q35_4b_pxE_parity.jsonl").items()}
    pt = {k: v["probs"] for k, v in load(f"preds_{s}/q35_4b_pxE_tta.jsonl").items()}
    for i, r in rows.items():
        if r["qtype"] != "choice" or len(r["options"]) < 20: continue
        a = {o: float(pp[i].get(o, 0)) for o in r["options"]}; t = {o: float(pt[i].get(o, 0)) for o in r["options"]}
        rev = {o: 2 * t[o] - a[o] for o in a}
        f = pred(a) != pred(rev); (R if pred(a) == r["gold"] else W).append(f)
        srcs[r["source"]] = srcs.get(r["source"], 0) + 1
print(f">=20-option dev rows: {len(R)+len(W)} from {srcs}")
print(f"drift | right {100*np.mean(R):.2f}% (n={len(R)}), | wrong {100*np.mean(W):.2f}% (n={len(W)})")
for acc in (0.70, 0.75, 0.80, 0.85):
    print(f"  projected drift at accuracy {acc:.2f}: {100*(acc*np.mean(R)+(1-acc)*np.mean(W)):.1f}%")
