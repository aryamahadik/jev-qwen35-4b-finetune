"""A17-B0b scorer: C1 + think-mode system vs C1 and Jev (Nimble suite + holdout), and the Decision Index re-score with
think answers merged for the 5 knowledge benchmarks. Aggregates only."""
import json, os, shutil, subprocess, collections
TAU = 0.8; NS = "/Users/aryamahadik/Documents/jev/bench/nimble_suite"; J = "/Users/aryamahadik/Documents/jev"
JEV = {"aegis2": 80.4, "boolq": 89.7, "civil_comments": 81.0, "helpsteer2": 34.1, "massive-de-DE": 86.9, "massive-en-US": 87.4,
       "multinli": 82.9, "paws": 89.2, "pubmedqa": 77.2, "squad2": 82.9, "summeval-consistency": 81.2, "summeval-relevance": 35.0,
       "vitaminc-dev": 80.1, "nimble-holdout": 93.21}
CLEAN = ["paws", "pubmedqa", "squad2", "summeval-consistency", "summeval-relevance", "vitaminc-dev"]
SEEN = ["aegis2", "boolq", "civil_comments", "helpsteer2", "massive-de-DE", "massive-en-US", "multinli"]
think = {}
for f in ("out_nimble.jsonl",):
    if os.path.exists(f):
        for l in open(f):
            r = json.loads(l); think[r["key"]] = r.get("pred_key")
# reuse A17-B0 answers (768 tokens) for squad2/paws/pubmedqa: map letter -> key via the same rule
reuse = {}
for f in ("think_preds.jsonl", "think_pubmedqa.jsonl"):
    if os.path.exists(f):
        for l in open(f):
            r = json.loads(l)
            if r["sub"] == "pubmedqa" and f == "think_preds.jsonl": continue  # buggy first pubmedqa scoring
            reuse[(r["sub"], r["id"])] = r
res = {}
for d, pdir in (("data", "preds"), ("data_holdout", "preds_holdout")):
    for sub in sorted(os.listdir(f"{NS}/{d}")):
        gold = {}; kind = {}
        for l in open(f"{NS}/{d}/{sub}/all.jsonl"):
            r = json.loads(l); gold[r["id"]] = r["reference"]["target"]; kind[r["id"]] = r["input"]["questions"]["decision"]["type"]
        ok_c1 = ok_sys = n = routed = used = 0
        for l in open(f"{NS}/{pdir}/{sub}.jsonl"):
            p = json.loads(l); pr = p["probs"] or {}; y = gold[p["id"]]; k = kind[p["id"]]; n += 1
            def c1_ok():
                if not pr: return False
                if k == "noul": return (pr["true"] >= .5) == bool(y)
                if k == "score": return int(round(sum(int(a) * v for a, v in pr.items()))) == y
                return max(pr, key=pr.get) == y
            c = c1_ok(); ok_c1 += c
            top = max(pr.values()) if pr else 0.0
            if top >= TAU: ok_sys += c; continue
            routed += 1; s = c
            if (sub, p["id"]) in reuse:
                rr = reuse[(sub, p["id"])]
                if rr.get("parsed", True) and rr.get("letter", "x") is not None: s = bool(rr["ok"]); used += 1
            else:
                pk = think.get(f"nimble|{sub}|{p['id']}")
                if pk is not None:
                    used += 1
                    if k == "noul": s = (pk == "true") == bool(y)
                    elif k == "score": s = int(pk) == y
                    else: s = pk == y
            ok_sys += s
        res[sub] = {"n": n, "c1": 100 * ok_c1 / n, "c1_think": 100 * ok_sys / n, "jev": JEV[sub], "routed_pct": 100 * routed / n, "think_answers_used": used}
def mac(G, k): return sum(res[s][k] for s in G) / len(G)
summ = {g: {"c1": mac(G, "c1"), "c1_think": mac(G, "c1_think"), "jev": mac(G, "jev")} for g, G in (("clean", CLEAN), ("seen", SEEN), ("all13", CLEAN + SEEN))}
# Decision Index: merge think answers for the 5 knowledge benchmarks into C1's results and re-score with the harness
di = {}
if os.path.exists("out_di.jsonl"):
    th = {}
    for l in open("out_di.jsonl"):
        r = json.loads(l); _, rid, qk = r["key"].split("|", 2); th[(rid, qk)] = r.get("pred_key")
    src = f"{J}/bench/external_quarantine/decision_index/runs/c1_sample10k"; dst = f"{J}/bench/external_quarantine/decision_index/runs/c1think_sample10k"
    os.makedirs(dst, exist_ok=True)
    for f in os.listdir(src):
        if f != "results.jsonl" and os.path.isfile(f"{src}/{f}"): shutil.copy(f"{src}/{f}", dst)
    changed = 0
    with open(f"{dst}/results.jsonl", "w") as fo:
        for l in open(f"{src}/results.jsonl"):
            r = json.loads(l); ans = (r.get("response") or {}).get("answers") or {}
            for qk, a in ans.items():
                pk = th.get((r["run_id"], qk))
                if pk is None or a.get("type") != "choice" or pk not in (a.get("probabilities") or {}): continue
                keys = list(a["probabilities"]); rest = 0.1 / max(len(keys) - 1, 1)
                a["probabilities"] = {k2: (0.9 if k2 == pk else rest) for k2 in keys}; a["choice"] = pk; changed += 1
            fo.write(json.dumps(r) + "\n")
    P = f"{J}/bench/external_quarantine/decision_index/venv/bin/python"
    pass
    rep = json.load(open(f"{J}/bench/decision_index/report_think10k.json"))
    di = {"answers_replaced": changed, "index_c1": 54.83, "index_c1_think": rep["ours"]["index"], "jev": 59.51,
          "benchmarks": {b["dataset"]: {"c1_think": round(100 * b["ours_raw"], 1), "jev": round(100 * b["jev_raw"], 1)}
                         for b in rep["index_benchmarks"] if b["dataset"] in ("MMLU", "GPQA Diamond", "GSM8K", "CRUXEval", "CLadder")},
          "areas": rep["areas"]}
json.dump({"nimble": res, "summary": summ, "di": di}, open("report_b0b.json", "w"), indent=1)
print(f"{'subset':22s} {'C1':>6s} {'C1+think':>9s} {'Jev':>6s} {'routed':>7s}")
for s in CLEAN + SEEN + ["nimble-holdout"]:
    r = res[s]; print(f"{s:22s} {r['c1']:6.1f} {r['c1_think']:9.1f} {r['jev']:6.1f} {r['routed_pct']:6.0f}%")
for g, v in summ.items(): print(g, {k: round(x, 2) for k, x in v.items()})
print("DI:", json.dumps(di.get("benchmarks", {})), "index C1+think:", di.get("index_c1_think"), "C1:", 54.83, "Jev:", 59.51)
