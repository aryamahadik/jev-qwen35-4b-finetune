"""A18 scorer: C1 accuracy on the 13 rebuilt Nimble public subsets vs Jev 1.13's published numbers. Aggregates only."""
import json, math, os, re, sys, collections
JEV = {"aegis2": 80.4, "boolq": 89.7, "civil_comments": 81.0, "helpsteer2": 34.1, "massive-de-DE": 86.9, "massive-en-US": 87.4,
       "multinli": 82.9, "paws": 89.2, "pubmedqa": 77.2, "squad2": 82.9, "summeval-consistency": 81.2,
       "summeval-relevance": 35.0, "vitaminc-dev": 80.1}
NIMBLE9B = {"aegis2": 81.2, "boolq": 86.0, "civil_comments": 70.3, "helpsteer2": 39.0, "massive-de-DE": 83.4, "massive-en-US": 86.9,
            "multinli": 85.3, "paws": 82.8, "pubmedqa": 75.6, "squad2": 80.6, "summeval-consistency": 75.7,
            "summeval-relevance": 49.2, "vitaminc-dev": 76.6}
CLEAN = ["paws", "pubmedqa", "squad2", "summeval-consistency", "summeval-relevance", "vitaminc-dev"]
SEEN = ["aegis2", "boolq", "civil_comments", "helpsteer2", "massive-de-DE", "massive-en-US", "multinli"]
def wilson(k, n, z=1.959964):
    if n == 0: return (float("nan"),) * 2
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * (c - h), 100 * (c + h)
def rhe(x): return int(round(x))  # Python round = half to even
ov = json.load(open("overlap_counts.json"))["per_subset"]
pred_dir = sys.argv[1] if len(sys.argv) > 1 else "preds"
res = {}
for sub in CLEAN + SEEN:
    gold = {}
    for l in open(f"data/{sub}/all.jsonl"):
        r = json.loads(l); gold[r["id"]] = r["reference"]["target"]
    rows = [json.loads(l) for l in open(f"{pred_dir}/{sub}.jsonl")]
    ok = ok_arg = n = 0; brier = []; conf = []
    for p in rows:
        y = gold[p["id"]]; n += 1; pr = p["probs"]
        if not pr: conf.append((0.0, 0)); continue
        if p["kind"] == "noul":
            pt = pr["true"]; c = (pt >= 0.5) == bool(y); ok += c; ok_arg += c; brier.append((pt - float(bool(y))) ** 2)
            conf.append((max(pt, 1 - pt), int(c)))
        elif p["kind"] == "choice":
            a = max(pr, key=pr.get); c = a == y; ok += c; ok_arg += c
            brier.append(sum((v - (1.0 if k == y else 0.0)) ** 2 for k, v in pr.items())); conf.append((pr[a], int(c)))
        else:
            e = sum(int(k) * v for k, v in pr.items()); lev = rhe(e); a = int(max(pr, key=pr.get))
            ok += lev == y; ok_arg += a == y
            brier.append(sum((v - (1.0 if int(k) == y else 0.0)) ** 2 for k, v in pr.items())); conf.append((pr[str(a)], int(a == y)))
    bins = collections.defaultdict(list)
    for cf, c in conf: bins[min(int(cf * 10), 9)].append((cf, c))
    ece = sum(len(b) / len(conf) * abs(sum(x for x, _ in b) / len(b) - sum(c for _, c in b) / len(b)) for b in bins.values())
    lo, hi = wilson(ok, n)
    res[sub] = {"n": n, "acc": 100 * ok / n, "ci": [lo, hi], "acc_argmax": 100 * ok_arg / n, "brier": sum(brier) / max(len(brier), 1),
                "ece": ece, "jev": JEV[sub], "nimble9b": NIMBLE9B[sub], "overlap_items": ov[sub]["overlapping_items"],
                "unsupported": sum(1 for p in rows if not p["probs"])}
def avg(group, key):
    return sum(res[s][key] for s in group) / len(group)
def micro(group):
    return 100 * sum(res[s]["acc"] / 100 * res[s]["n"] for s in group) / sum(res[s]["n"] for s in group)
summ = {g: {"c1_macro": avg(G, "acc"), "jev_macro": avg(G, "jev"), "nimble9b_macro": avg(G, "nimble9b"), "c1_micro": micro(G)}
        for g, G in (("clean", CLEAN), ("seen_task", SEEN), ("all13", CLEAN + SEEN))}
json.dump({"per_subset": res, "summary": summ, "readout": "A5: choice 2-view, yes/no once, T=1; score = rounded expected level (argmax also shown)"},
          open("report_nimble_c1.json", "w"), indent=1)
print(f"{'subset':22s} {'n':>4s} {'C1':>6s} {'95% CI':>13s} {'Jev':>6s} {'diff':>6s} {'N9B':>6s} {'ovl':>4s}")
for s in CLEAN + ["--"] + SEEN:
    if s == "--": print("-- seen-task (C1 trained on this dataset's train split) --"); continue
    r = res[s]; print(f"{s:22s} {r['n']:4d} {r['acc']:6.1f} {r['ci'][0]:5.1f}-{r['ci'][1]:5.1f} {r['jev']:6.1f} {r['acc']-r['jev']:+6.1f} {r['nimble9b']:6.1f} {r['overlap_items']:4d}")
for g, v in summ.items(): print(g, {k: round(x, 2) for k, x in v.items()})
