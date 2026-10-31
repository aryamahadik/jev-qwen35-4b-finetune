"""Yes/no letter-swap check of the 4B-E teacher on training rows: first read (seeded letter order) vs the swapped
letter order, per shard. Prints flip rate (P(yes) >= 0.5 differs), mean |dp|, accuracy view/swap/average vs gold, and
the share of 2-view targets inside 0.2-0.8. CPU only; reads local files."""
import json, sys
from pathlib import Path
L = Path(__file__).resolve().parent.parent
orig = L / "data/v14_label_shards/labels_q35_4b_pxE"
rev = L / "extra/labels_q35_4b_pxE_revyn"
rows = {}
tot = dict(n=0, flip=0, dp=0.0, acc_v=0, acc_s=0, acc_a=0, mid_v=0, mid_a=0)
for f in sorted(rev.glob("shard_*.jsonl")):
    if f.name.endswith(".meta.json"):
        continue
    shard = {json.loads(l)["id"]: json.loads(l) for l in open(L / "data/v14_label_shards" / f.name)}
    O = {json.loads(l)["id"]: json.loads(l) for l in open(orig / f.name)}
    s = dict(n=0, flip=0, dp=0.0, acc_v=0, acc_s=0, acc_a=0, mid_v=0, mid_a=0)
    for l in open(f):
        x = json.loads(l); i = x["id"]; g = shard[i]["gold"]
        pv, ps = O[i]["probs"]["yes"], x["probs"]["yes"]
        assert O[i]["view"][::-1] == x["view"], i
        pa = (pv + ps) / 2
        for d in (s, tot):
            d["n"] += 1; d["flip"] += (pv >= 0.5) != (ps >= 0.5); d["dp"] += abs(pv - ps)
            d["acc_v"] += (pv >= 0.5) == (g == 1); d["acc_s"] += (ps >= 0.5) == (g == 1); d["acc_a"] += (pa >= 0.5) == (g == 1)
            d["mid_v"] += 0.2 < pv < 0.8; d["mid_a"] += 0.2 < pa < 0.8
    print(f.name, {k: (round(v / s["n"], 4) if k != "n" else v) for k, v in s.items()})
print("ALL", {k: (round(v / tot["n"], 4) if k != "n" else v) for k, v in tot.items()})
