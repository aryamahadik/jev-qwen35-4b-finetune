"""Optimist check 5 (read-only): the 'No' lean. v11c's biggest held-out yes/no losses were one-sided false-No errors
(hearsay 34 vs 2, moral 14 vs 4). Does 4B-E still lean No on dev? Counts false-No (gold yes, answered no) and false-Yes.
Also OHS-1/OHS-2 per yes/no task for v11c and Jev (already-used exams; diagnosis only)."""
import sys, os, json
from collections import defaultdict
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean"); os.chdir("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
import gate_dev as G
SPL = G.SPLITS.split(",")
for m in ("q35_4b_v10", "q35_4b_v11c", "q35_4b_v13t", "q35_4b_pxE", "q35_2b_v11r", "q35_2b_armI_1600"):
    fn = fp = n = 0; uns = [0, 0]
    for s in SPL:
        P = G.load(s, m)
        for l in open(f"data/{s}.jsonl"):
            r = json.loads(l)
            if r["qtype"] != "noul": continue
            y = float(P[r["id"]].get("yes", 0)) > 0.5; n += 1
            if r["gold"] == 1 and not y: fn += 1; uns[0] += r["source"] in G.UNSEEN_FROZEN_ROWS
            if r["gold"] == 0 and y: fp += 1; uns[1] += r["source"] in G.UNSEEN_FROZEN_ROWS
    print(f"dev yes/no {m:18s} n={n}: false-No {fn}, false-Yes {fp}, ratio {fn/max(fp,1):.2f} (unseen-source rows: {uns[0]} vs {uns[1]})")
load = lambda p: {json.loads(l)["id"]: json.loads(l) for l in open(p)}
for split, ms in (("ohs", ["q35_4b_v11c_cal", "jev_guard"]), ("ohs2", ["q35_4b_v11c_cal", "jev_guard"])):
    rows = load(f"data/{split}.jsonl")
    for m in ms:
        P = {k: v["probs"] for k, v in load(f"preds_{split}/{m}.jsonl").items()}
        by = defaultdict(lambda: [0, 0, 0])
        for i, r in rows.items():
            if r["qtype"] != "noul" or r["role"] != "aff" or i.endswith(("_neg", "_dneg", "_para", "_yn")): continue
            y = float(P[i].get("yes", 0)) > 0.5; b = by[r["source"]]; b[2] += 1
            b[0] += r["gold"] == 1 and not y; b[1] += r["gold"] == 0 and y
        print(f"{split} {m:16s} " + "; ".join(f"{t} FN {a} FP {b} /{c}" for t, (a, b, c) in sorted(by.items())))
