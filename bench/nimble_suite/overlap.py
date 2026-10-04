"""Counts-only 12-gram overlap between the 13 rebuilt subsets and C1's training file (A18). Prints counts only."""
import glob, json, os, re, collections
TRAIN = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_parts/golden_train.jsonl"
W = re.compile(r"[a-z0-9]+")
def grams(t, n=12):
    w = W.findall(t.lower()); return {" ".join(w[i:i+n]) for i in range(len(w) - n + 1)}
def rec_text(r):
    q = r["input"]["questions"]["decision"]; st = r["input"]["state"]
    return (st if isinstance(st, str) else json.dumps(st, ensure_ascii=False)) + " " + (q.get("instructions") or "")
idx = collections.defaultdict(set); per = {}
for f in sorted(glob.glob("data/*/records.jsonl")) or sorted(glob.glob("data/*/*.jsonl")):
    sub = f.split("/")[1]
    for l in open(f):
        r = json.loads(l)
        if "input" not in r: continue
        for g in grams(rec_text(r)): idx[g].add((sub, r["id"]))
        per.setdefault(sub, set()).add(r["id"])
df = collections.Counter(g for g, s in idx.items() for _ in [0])
boiler = {g for g, s in idx.items() if len(s) > 50}
hit = collections.defaultdict(set); n = 0
with open(TRAIN) as fh:
    for l in fh:
        n += 1; r = json.loads(l)
        t = " ".join(str(r.get(k) or "") for k in ("state", "instructions", "card")) + " " + " ".join(map(str, r.get("options") or []))
        for g in grams(t):
            if g in idx and g not in boiler:
                for s, i in idx[g]: hit[s].add(i)
out = {s: {"items": len(per[s]), "overlapping_items": len(hit.get(s, ()))} for s in sorted(per)}
json.dump({"train_rows": n, "boilerplate_grams": len(boiler), "per_subset": out}, open("overlap_counts.json", "w"), indent=1)
print(json.dumps(out, indent=0))
