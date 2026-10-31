"""Optimist check 9 (read-only diagnosis on ALREADY-USED exams; nothing here may be used to pick a temperature for
OHS-3): would a sharper yes/no temperature have helped held-out Brier? v11c raw preds on OHS-1/OHS-2 yes/no base rows,
p' = sigmoid(logit(p)/T). The dev-fitted T for v11c was 0.95 (dev_out.txt); for 4B-E 0.9 (FINETUNE_PLAN 5.1)."""
import json, os
import numpy as np
os.chdir("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
load = lambda p: {json.loads(l)["id"]: json.loads(l) for l in open(p)}
for split in ("ohs", "ohs2"):
    rows = load(f"data/{split}.jsonl")
    yn = [i for i, r in rows.items() if r["qtype"] == "noul" and r["role"] == "aff" and not i.endswith(("_neg", "_dneg", "_para", "_yn"))]
    for m in ("q35_4b_v11c", "q35_4b_v10"):
        P = {k: v["probs"] for k, v in load(f"preds_{split}/{m}.jsonl").items()}
        p = np.clip(np.array([float(P[i]["yes"]) / (float(P[i]["yes"]) + float(P[i]["no"])) for i in yn]), 1e-6, 1 - 1e-6)
        g = np.array([rows[i]["gold"] for i in yn]); lg = np.log(p / (1 - p))
        out = [f"T {T}: {np.mean((1 / (1 + np.exp(-lg / T)) - g) ** 2):.4f}" for T in (0.6, 0.7, 0.8, 0.9, 1.0, 1.2)]
        print(f"{split:4s} {m:12s} n={len(yn)} yes/no Brier by T: " + " | ".join(out))
