"""JOB3: option label vocabulary per source (golden set), counts only. For each source: label -> rows."""
import json, re, sys, collections
P = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/v14_parts/golden_train.jsonl"
want = set(sys.argv[1].split(","))
lab = collections.defaultdict(collections.Counter)
tot = collections.Counter()
qt = collections.defaultdict(collections.Counter)
for line in open(P):
    r = json.loads(line)
    s = r["source"]
    if s not in want: continue
    tot[s] += 1; qt[s][r["qtype"]] += 1
    for ln in (r.get("card") or "").split("\n"):
        if ln.startswith("- ") and ": " in ln:
            lab[s][ln[2:].split(": ", 1)[0]] += 1
for s in want:
    print("==", s, tot[s], dict(qt[s]))
    print("  ", lab[s].most_common(60))
