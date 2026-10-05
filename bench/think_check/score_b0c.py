"""A17-B0c: merge think answers (routed OHS-1/2 base rows) into C1's preds and score with score_ohs.py vs Jev."""
import json, subprocess, os
L = "/Users/aryamahadik/Documents/jev/opendecide-data/lean"; NAME = "q35_4b_c1think_b0c"
import sys
SPLITS = sys.argv[1:] or ["ohs", "ohs2"]
for split in SPLITS:
    th = {}
    for l in open(f"out_{split}.jsonl"):
        r = json.loads(l); th[r["key"].split("|", 1)[1]] = r.get("pred_key")
    n = 0
    with open(f"{L}/preds_{split}/{NAME}.jsonl", "w") as fo:
        for l in open(f"{L}/preds_{split}/q35_4b_main500k_b100_a5.jsonl"):
            p = json.loads(l); pk = th.get(p["id"])
            if pk is not None and pk in p["probs"]:
                keys = list(p["probs"]); rest = 0.1 / max(len(keys) - 1, 1)
                p["probs"] = {k: (0.9 if k == pk else rest) for k in keys}; n += 1
            p["model"] = NAME; fo.write(json.dumps(p) + "\n")
    print(split, "think answers merged:", n, flush=True)
    o = subprocess.run([f"{L}/../.venv/bin/python", "score_ohs.py", "q35_4b_main500k_b100_a5", NAME, "--split", split, "--boot", "2000"], cwd=L, capture_output=True, text=True)
    print(o.stdout[-2500:], o.stderr[-500:])
