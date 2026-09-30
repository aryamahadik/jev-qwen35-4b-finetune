"""Offline simulation of a PRISM-X cascade: the fast 2B answers every question; only the questions it is least sure
about (lowest top probability) go to our own 4B. Uses existing predictions only (no GPU).
The routing threshold is chosen on dev-select for each routing budget and applied unchanged to dev-confirm.
  python cascade_sim.py SMALL BIG [BIG2 ...]    e.g.  python cascade_sim.py q35_2b_armH q35_4b_v11c q35_4b_v13t q35_4b_blend50
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPLITS = ["dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims", "pg_dev", "devzs", "devp_card", "dev"]
half = lambda g: "select" if int(hashlib.sha256(f"devsel:{g}".encode()).hexdigest(), 16) % 2 == 0 else "confirm"


def load(split, name):
    f = HERE / f"preds_{split}" / f"{name}.jsonl"
    return {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(f)}


def norm(r, pr):
    keys = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
    p = [float(pr.get(k, 0.0)) for k in keys]
    s = sum(p) or 1.0
    return keys, [x / s for x in p]


def ok(r, keys, p):
    g = ("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"]
    best = max(p)
    return float([k for k, v in zip(keys, p) if v == best] == [g])


small, bigs = sys.argv[1], sys.argv[2:]
rows = {"select": [], "confirm": []}
for s in SPLITS:
    P = {n: load(s, n) for n in [small] + bigs}
    for l in open(HERE / f"data/{s}.jsonl"):
        r = json.loads(l)
        if all(r["id"] in P[n] for n in P):
            rows[half(r["group_id"])].append((r, {n: norm(r, P[n][r["id"]]) for n in P}))


def acc(part, name):
    return 100 * sum(ok(r, *d[name]) for r, d in rows[part]) / len(rows[part])


print(f"rows: select {len(rows['select'])}, confirm {len(rows['confirm'])}")
for n in [small] + bigs:
    print(f"  alone  {n:18s} select {acc('select', n):.2f}  confirm {acc('confirm', n):.2f}")
big = max(bigs, key=lambda n: acc("select", n))  # the 4B is chosen on dev-select only
print(f"4B chosen on dev-select: {big}")
conf = lambda d: max(d[small][1])
sel_c = sorted(conf(d) for _, d in rows["select"])
print(f"{'route %':>8} {'threshold':>9} {'confirm acc':>11} {'gain vs 2B':>10} {'routed on confirm':>18}")
for budget in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6):
    tau = sel_c[int(budget * len(sel_c))]
    tot = routed = 0
    for r, d in rows["confirm"]:
        use = big if conf(d) < tau else small
        routed += use == big
        tot += ok(r, *d[use])
    a = 100 * tot / len(rows["confirm"])
    print(f"{budget:8.0%} {tau:9.3f} {a:11.2f} {a - acc('confirm', small):+10.2f} {100 * routed / len(rows['confirm']):17.1f}%")

# Blend on routed questions: p = w * p_4B + (1 - w) * p_2B; the budget and w are chosen on dev-select, then applied to
# dev-confirm. Also reports yes/no Brier (calibration) on dev-confirm.
def brier(part_rows, pick):
    xs = [(p[keys.index("yes")] - r["gold"]) ** 2 for r, d in part_rows if r["qtype"] == "noul" for keys, p in [pick(r, d)]]
    return sum(xs) / len(xs)
def run(part, tau, w):
    def pick(r, d):
        if conf(d) < tau:
            k, pb = d[big]; _, ps = d[small]
            return k, [w * a + (1 - w) * b for a, b in zip(pb, ps)]
        return d[small]
    return 100 * sum(ok(r, *pick(r, d)) for r, d in rows[part]) / len(rows[part]), brier(rows[part], pick)
best = max(((b, w) for b in (0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0) for w in (0.5, 0.6, 0.7, 0.8, 1.0)),
           key=lambda bw: run("select", sel_c[min(int(bw[0] * len(sel_c)), len(sel_c) - 1)] if bw[0] < 1 else 2.0, bw[1])[0])
b, w = best
tau = sel_c[min(int(b * len(sel_c)), len(sel_c) - 1)] if b < 1 else 2.0
a, br = run("confirm", tau, w)
print(f"blend chosen on dev-select: route {b:.0%}, w_4B {w} -> confirm acc {a:.2f}, yes/no Brier {br:.4f}")
print(f"  reference on confirm: 4B alone acc {acc('confirm', big):.2f}, Brier {brier(rows['confirm'], lambda r, d: d[big]):.4f};"
      f" 2B alone Brier {brier(rows['confirm'], lambda r, d: d[small]):.4f}")
