"""Free offline checks on existing dev predictions (no GPU): (1) run ensembles of PRISM-X arms, (2) post-hoc
temperature scaling fitted on dev-select (global per question type, and per source), all reported on dev-confirm:
micro accuracy, yes/no Brier, top-1 ECE (10 bins).
  python offline_calib.py q35_2b_armI q35_2b_armH q35_2b_armKI q35_2b_armJ q35_2b_armO1 q35_2b_armE_L4
"""
import hashlib
import itertools
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPLITS = ["dev_nc", "taskbank_dev", "hard_dev", "dev_negwords", "dev_claims", "pg_dev", "devzs", "devp_card", "dev"]
half = lambda g: "select" if int(hashlib.sha256(f"devsel:{g}".encode()).hexdigest(), 16) % 2 == 0 else "confirm"
names = sys.argv[1:]
rows = {"select": [], "confirm": []}
for s in SPLITS:
    P = {n: {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(HERE / f"preds_{s}/{n}.jsonl")} for n in names}
    for l in open(HERE / f"data/{s}.jsonl"):
        r = json.loads(l)
        if not all(r["id"] in P[n] for n in names):
            continue
        keys = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
        g = keys.index(("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"])
        pv = {}
        for n in names:
            v = [max(float(P[n][r["id"]].get(k, 0.0)), 1e-9) for k in keys]
            t = sum(v)
            pv[n] = [x / t for x in v]
        rows[half(r["group_id"])].append({"src": r["source"], "noul": r["qtype"] == "noul", "g": g, "p": pv})


def metrics(part, prob):
    acc = br = nb = 0
    conf = []
    for x in rows[part]:
        p = prob(x)
        m = max(p)
        ok = float([i for i, v in enumerate(p) if v == m] == [x["g"]])
        acc += ok
        conf.append((m, ok))
        if x["noul"]:
            br += (p[0] - (1.0 if x["g"] == 0 else 0.0)) ** 2
            nb += 1
    bins = defaultdict(list)
    for c, o in conf:
        bins[min(9, int(c * 10))].append((c, o))
    ece = sum(abs(sum(c for c, _ in b) / len(b) - sum(o for _, o in b) / len(b)) * len(b) for b in bins.values()) / len(conf)
    return 100 * acc / len(rows[part]), br / nb, ece


def temp(p, T):
    lg = [math.log(v) / T for v in p]
    m = max(lg)
    e = [math.exp(v - m) for v in lg]
    s = sum(e)
    return [v / s for v in e]


def avg(ms):
    return lambda x: [sum(x["p"][n][i] for n in ms) / len(ms) for i in range(len(x["p"][ms[0]]))]


print(f"rows select {len(rows['select'])} confirm {len(rows['confirm'])}")
print(f"{'model':42s} {'acc':>6} {'Brier':>7} {'ECE':>6}   (dev-confirm)")
for n in names:
    a, b, e = metrics("confirm", lambda x, n=n: x["p"][n])
    print(f"{n:42s} {a:6.2f} {b:7.4f} {e:6.4f}")
# ensembles: every subset of the PRISM-X arms containing I, chosen on dev-select accuracy
cands = [n for n in names if n != "q35_2b_armE_L4"]
best = max((c for k in range(2, len(cands) + 1) for c in itertools.combinations(cands, k) if cands[0] in c),
           key=lambda c: metrics("select", avg(list(c)))[0])
a, b, e = metrics("confirm", avg(list(best)))
print(f"{'ensemble (chosen on select): ' + '+'.join(n.replace('q35_2b_arm', '') for n in best):42s} {a:6.2f} {b:7.4f} {e:6.4f}")
a, b, e = metrics("confirm", avg(cands))
print(f"{'ensemble of all PRISM-X arms':42s} {a:6.2f} {b:7.4f} {e:6.4f}")
# temperature scaling for the first model (I): global per qtype, then per source, fitted on dev-select NLL
base = names[0]
grid = [round(0.5 + 0.05 * i, 2) for i in range(71)]  # 0.5 .. 4.0
def nll(part, key, T, filt):
    xs = [x for x in rows[part] if filt(x)]
    return sum(-math.log(max(temp(x["p"][key], T)[x["g"]], 1e-12)) for x in xs) / max(1, len(xs))
Tq = {q: min(grid, key=lambda T: nll("select", base, T, lambda x, q=q: x["noul"] == q)) for q in (True, False)}
a, b, e = metrics("confirm", lambda x: temp(x["p"][base], Tq[x["noul"]]))
print(f"{base + f' + T(yes/no {Tq[True]}, choice {Tq[False]})':42s} {a:6.2f} {b:7.4f} {e:6.4f}")
srcs = {x["src"] for x in rows["select"]}
Ts = {s: min(grid, key=lambda T: nll("select", base, T, lambda x, s=s: x["src"] == s)) for s in srcs}
a, b, e = metrics("confirm", lambda x: temp(x["p"][base], Ts.get(x["src"], Tq[x["noul"]])))
print(f"{base + ' + per-source T':42s} {a:6.2f} {b:7.4f} {e:6.4f}")
