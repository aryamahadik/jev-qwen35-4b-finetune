"""JOB3: C1 (q35_4b_main500k, 1 view) read on the C2 candidate rows (existing crowd labels, no new GPU):
accuracy per family/qtype, and for choice rows the confusion gold -> predicted label (counts)."""
import json, glob, collections, sys
LEAN = "/Users/aryamahadik/Documents/jev/opendecide-data/lean"
fams = sys.argv[1].split(",")
out = {}
for fam in fams:
    cand = {}
    for l in open(f"{LEAN}/data/c2_parts/{fam}/out/candidates_c2.jsonl"):
        r = json.loads(l); cand[r["id"]] = r
    labs = {}
    for p in sorted(glob.glob(f"{LEAN}/data/c2_crowd_shards/{fam}/labels_q35_4b_main500k/shard_*.jsonl")):
        for l in open(p):
            d = json.loads(l); labs[d["id"]] = d["probs"]
    acc = collections.defaultdict(lambda: [0, 0]); conf = collections.defaultdict(collections.Counter)
    miss = 0
    for i, r in cand.items():
        if i not in labs: miss += 1; continue
        pr = labs[i]; pred = max(pr, key=pr.get)
        g = r["gold"]
        if r["qtype"] == "noul":
            gl = "yes" if g in (1, "1", "yes", True) else "no"
            ok = pred == gl
            acc["noul"][0] += ok; acc["noul"][1] += 1
            conf["noul:" + gl][pred] += 1
        else:
            ok = pred == g
            acc["choice"][0] += ok; acc["choice"][1] += 1
            conf["choice:" + g][pred] += 1
    out[fam] = {"cand": len(cand), "labelled": len(cand) - miss,
                "acc": {k: [v[0], v[1], round(100 * v[0] / v[1], 1)] for k, v in acc.items()},
                "confusion": {k: dict(v) for k, v in conf.items()}}
    print("==", fam, out[fam]["cand"], out[fam]["labelled"], out[fam]["acc"])
json.dump(out, open("c1_on_c2.json", "w"), indent=1)
