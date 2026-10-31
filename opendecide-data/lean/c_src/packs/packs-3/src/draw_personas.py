"""Draw O*NET persona seeds for packs-3 (C_DATA_SPEC v4 2.1 F4).
Titles only, main occupation titles (occupation_data.csv of the O*NET 31.0 database, CC BY 4.0), drawn by program with a
fixed seed and spread round-robin over the O*NET major groups. Never the alternate-titles or SOC direct-match file.
Excluded by fixed rule: titles containing 'All Other' and the military group 55."""
import csv, json, random, sys, hashlib
from collections import defaultdict
SRC = sys.argv[1]; OUT = sys.argv[2]; N = int(sys.argv[3])
SEED = "packs-3|20261003"
rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
groups = defaultdict(list)
for r in rows:
    code, title = r["O*NET-SOC Code"], r["Title"]
    g = code[:2]
    if g == "55" or "All Other" in title:
        continue
    groups[g].append((code, title))
rng = random.Random(SEED)
order = {}
for g in sorted(groups):
    lst = sorted(groups[g]); rng.shuffle(lst); order[g] = lst
draws, i = [], 0
gs = sorted(order)
while len(draws) < N:
    g = gs[i % len(gs)]; k = i // len(gs)
    if k < len(order[g]):
        draws.append({"draw": len(draws), "major_group": g, "onet_code": order[g][k][0], "title": order[g][k][1]})
    i += 1
json.dump({"seed": SEED, "source": "O*NET 31.0 occupation_data.csv", "source_sha256": hashlib.sha256(open(SRC,'rb').read()).hexdigest(),
           "rule": "round-robin over sorted major groups; seeded shuffle within group; exclude group 55 and 'All Other'",
           "draws": draws}, open(OUT, "w"), indent=1)
print(len(draws), "draws over", len(gs), "groups")
