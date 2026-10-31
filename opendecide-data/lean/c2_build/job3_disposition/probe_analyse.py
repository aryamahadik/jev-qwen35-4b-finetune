"""JOB3: analyse the C1 read of the fresh disposition probe (probe/key.json + probe/labels_q35_4b_main500k/shard_000.jsonl).
Counts and rates only. Usage: ../../.venv/bin/python -B probe_analyse.py [labels_dir]"""
import collections
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LD = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "probe" / "labels_q35_4b_main500k"
key = json.load(open(HERE / "probe" / "key.json"))
lab = {}
for l in open(LD / "shard_000.jsonl"):
    d = json.loads(l)
    lab[d["id"]] = d["probs"]
missing = [i for i in key if i not in lab]
print("rows", len(key), "read", len(lab), "missing", len(missing))


def pred(i):
    p = lab[i]
    return max(p, key=p.get)


def gold_label(k):
    return k["gold"]


def wilson(k, n, z=1.96):
    if n == 0:
        return (0, 0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(100 * (c - h), 1), round(100 * (c + h), 1))


tab = collections.defaultdict(lambda: [0, 0])
conf = collections.defaultdict(collections.Counter)
for i, k in key.items():
    if i not in lab:
        continue
    pr = pred(i)
    ok = pr == gold_label(k)
    g = (k["wf"], k["variant"], k["arm"])
    tab[g][0] += ok
    tab[g][1] += 1
    conf[g][(k["gold"], pr)] += 1
print("\naccuracy by workflow / variant / arm  (k/n, %, 95% Wilson)")
for g in sorted(tab):
    k, n = tab[g]
    print(f"  {g[0]:10s} {g[1]:7s} {g[2]:7s} {k:3d}/{n:3d} {100 * k / n:5.1f}  {wilson(k, n)}")

print("\npooled by variant x arm (choice only)")
pool = collections.defaultdict(lambda: [0, 0])
for g, (k, n) in tab.items():
    if g[0] == "cred":
        continue
    pool[(g[1], g[2])][0] += k
    pool[(g[1], g[2])][1] += n
for g in sorted(pool):
    k, n = pool[g]
    print(f"  {g[0]:7s} {g[1]:7s} {k}/{n} {100 * k / n:5.1f}")

print("\nper gold label (recall) pooled over arms, by workflow x variant")
rec = collections.defaultdict(lambda: [0, 0])
for g, c in conf.items():
    for (gl, pr), n in c.items():
        r = rec[(g[0], g[1], gl)]
        r[1] += n
        r[0] += n if gl == pr else 0
for gk in sorted(rec):
    k, n = rec[gk]
    print(f"  {gk[0]:10s} {gk[1]:7s} {gk[2]:13s} {k:3d}/{n:3d} {100 * k / n:5.1f}")

print("\nwhere the misses go (gold -> predicted, count), choice rows, pooled over arms")
mis = collections.defaultdict(collections.Counter)
for g, c in conf.items():
    for (gl, pr), n in c.items():
        if gl != pr:
            mis[(g[0], g[1])][(gl, pr)] += n
for gk in sorted(mis):
    print(" ", gk, mis[gk].most_common(6))

# paired: same scenario, defs vs nodefs; stated vs plain
print("\npaired agreement defs vs nodefs (same predicted label)")
by = collections.defaultdict(dict)
for i, k in key.items():
    if i in lab:
        by[(k["wf"], k["variant"], k["kind"], i.rsplit("_", 1)[1])][k["arm"]] = i
agree = collections.defaultdict(lambda: [0, 0])
for gk, d in by.items():
    if "defs" in d and "nodefs" in d:
        a = pred(d["defs"]) == pred(d["nodefs"])
        agree[(gk[0], gk[1])][0] += a
        agree[(gk[0], gk[1])][1] += 1
for gk in sorted(agree):
    k, n = agree[gk]
    print(f"  {gk[0]:10s} {gk[1]:7s} {k}/{n} {100 * k / n:.0f}%")

print("\nArabic arm vs English defs arm, same scenarios (invoice, agent_run; stated variant): both right / only EN right / only AR right / both wrong")
pair = collections.defaultdict(lambda: [0, 0, 0, 0])
for gk, d in by.items():
    for ar in ("ardefs", "arstate"):
        if "defs" in d and ar in d:
            ge = key[d["defs"]]["gold"]
            e = pred(d["defs"]) == ge
            a = pred(d[ar]) == ge
            pair[(gk[0], gk[1], ar)][(0 if (e and a) else 1 if e else 2 if a else 3)] += 1
for gk in sorted(pair):
    print(" ", gk, pair[gk])

# cautious pick rate on clean-pass states (the posture test)
print("\nclean-pass scenarios (gold = the permissive label): how often C1 picks something else")
clean = {"invoice": "pay", "support": "replace", "agent_run": "continue", "cred": "no"}
for wf, cl in clean.items():
    for v in ("stated", "plain"):
        ids = [i for i, k in key.items() if i in lab and k["wf"] == wf and k["variant"] == v and k["gold"] == cl]
        c = collections.Counter(pred(i) for i in ids)
        n = len(ids)
        print(f"  {wf:10s} {v:7s} n={n:3d} picks={dict(c)}")
