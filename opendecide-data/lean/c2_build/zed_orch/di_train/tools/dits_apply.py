"""DI-TS round 3: apply Opus-confirmed drops (drop only), format gates at 100%, package. Usage: python -I -B dits_apply.py <di_train_dir>"""
import sys, json, re, hashlib, collections
from pathlib import Path
D = Path(sys.argv[1]); DT = D / "DI-TS"; C2 = D.parents[1]; LEAN = C2.parent
sys.path.insert(0, str(C2)); sys.path.insert(0, str(D / "tools"))
import c2io
from c2_kit import rows as R, cards
import dits_text as T
sha = lambda b: hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()
drop = {}
for f in sorted((DT / "confirm/answers").glob("*.json")):
    for o in json.load(open(f)):
        if o["verdict"] in ("wrong_gold", "ambiguous"): drop["c2_dits:" + o["id"][1:]] = o["verdict"]
ld = lambda p: [json.loads(l) for l in open(p, encoding="utf8")]
cand0, dev0 = ld(DT / "stage/candidates_stage.jsonl"), ld(DT / "stage/mixdev_S5_stage.jsonl")
cand = [r for r in cand0 if r["id"] not in drop]; dev = [r for r in dev0 if r["id"] not in drop]
unmatched = set(drop) - {r["id"] for r in cand0 + dev0}
rep = {"drop_ids": len(drop), "unmatched": len(unmatched), "by_verdict": dict(collections.Counter(drop.values())),
       "dropped_cand": len(cand0) - len(cand), "dropped_dev": len(dev0) - len(dev),
       "dropped_by_task": dict(collections.Counter(r["meta"]["task_id"] for r in cand0 + dev0 if r["id"] in drop))}
LAB = {"logical_entailment": T.LE_OPTS, "temporal_cs1": T.NLI_OPTS3, "temporal_cs2": T.NLI_OPTS2, "temporal_cs3": T.NLI_OPTS3, "perspectrum": T.PS_OPTS}
def near(rows):
    g = lambda s: (lambda w: {" ".join(w[i:i+3]) for i in range(max(1, len(w)-2))})(re.findall(r"\S+", s.lower()))
    inv, segs, n = {}, [], 0
    for r in rows:
        k = g(r["state"]); c = set()
        for x in k: c |= inv.get(x, set())
        if any(len(k & segs[j]) / max(1, len(k | segs[j])) >= 0.9 for j in c): n += 1
        segs.append(k)
        for x in k: inv.setdefault(x, set()).add(len(segs) - 1)
    return n
def gates(rows, name):
    bad = {}; res = {"rows": len(rows)}
    bad["schema"] = sum(bool([p for p in R.validate_row(r) if p != "meta.licence"]) for r in rows)
    bad["options_label_set"] = sum(not (r["qtype"] == "choice" and sorted(r["options"]) == sorted(LAB[r["meta"]["qform"]]) and r["gold"] in r["options"]) for r in rows)
    ids = collections.Counter(r["id"] for r in rows); st = collections.Counter(r["state"] + "||" + r["meta"]["task_id"] for r in rows)
    rid = collections.Counter(r["meta"]["record_id"] for r in rows)
    bad["g12_dup_id"] = sum(v > 1 for v in ids.values()); bad["g12_exact_dup_state"] = sum(v - 1 for v in st.values() if v > 1)
    bad["g12_one_row_per_source_record"] = sum(v > 1 for v in rid.values()); bad["g12_near_dup"] = near(rows)
    g15 = 0
    for r in rows:
        try:
            x = R.g15_check(r); ok = x.get("ok", True) if isinstance(x, dict) else bool(x)
            g15 += (not ok)
        except Exception: g15 += 1
    bad["g15_loader_round_trip"] = g15
    mx, tok = cards._tokenizer()
    class L:
        def record(self, *a, **k): pass
    tt = mx.token_counts(L(), rows) if tok is not None else [R.approx_tokens(r) for r in rows]
    res["tokens"] = {"counted_by": "pinned tokenizer" if tok is not None else "approx", "mean": round(sum(tt)/len(tt), 1), "max": max(tt)}
    bad["tokens_gt_2000"] = sum(t > 2000 for t in tt); bad["token_mean_gt_800"] = int(sum(tt)/len(tt) > 800)
    per = {}
    for t in LAB:
        rs = [r for r in rows if r["meta"]["qform"] == t]
        wc = collections.Counter(r["meta"]["wording_id"] for r in rs); lc = collections.Counter(r["gold"] for r in rs)
        cap = 0.55 if len(LAB[t]) == 2 else 0.40
        per[t] = {"rows": len(rs), "wordings": len(wc), "wording_max_share": round(max(wc.values())/len(rs), 3), "labels": dict(lc), "label_max_share": round(max(lc.values())/len(rs), 3),
                  "cap": cap, "gold_position": dict(collections.Counter(r["options"].index(r["gold"]) for r in rs))}
    wc = collections.Counter(r["meta"]["wording_id"] for r in rows)
    res["block_wordings"] = len(wc); res["block_wording_max_share"] = round(max(wc.values())/len(rows), 4)
    bad["block_wording_lt4_or_gt35"] = int(len(wc) < 4 or max(wc.values())/len(rows) > 0.35)
    bad["task_wording_lt4_or_gt35"] = sum(p["wordings"] < 4 or p["wording_max_share"] > 0.35 for p in per.values())
    bad["task_label_share_over_cap"] = sum(p["label_max_share"] > p["cap"] for p in per.values())
    res["per_task"] = per; res["failures"] = bad; res["pass"] = all(v == 0 for v in bad.values()); return res
rep["gates_candidates"] = gates(cand, "cand"); rep["gates_owndev"] = gates(dev, "dev")
rep["candidate_problems"] = c2io.candidate_problems("DI-TS", cand)
out = LEAN / "data/c2_parts/DI-TS/out"; out.mkdir(parents=True, exist_ok=True); (out.parent / "qc").mkdir(exist_ok=True); hold = out.parent / "hold_owndev"; hold.mkdir(exist_ok=True)
files = {}
for name, rs in ((c2io.CAND, cand), (c2io.REL, []), ("mixdev_S5.jsonl", dev)):
    d = hold if name == "mixdev_S5.jsonl" else out
    c2io.write_jsonl(d / name, rs); files[name] = {"sha256": sha((d / name).read_bytes()), "rows": len(rs)}
(DT / "stage/APPLY_REPORT.json").write_text(json.dumps(rep, indent=1))
(DT / "stage/files.json").write_text(json.dumps(files, indent=1))
print(json.dumps({k: rep[k] for k in ("drop_ids","unmatched","by_verdict","dropped_cand","dropped_dev","dropped_by_task","candidate_problems")}))
for k in ("gates_candidates", "gates_owndev"):
    g = rep[k]; print(k, g["pass"], g["failures"], g["tokens"]); 
    for t, p in g["per_task"].items(): print(" ", t, p["rows"], p["labels"], p["label_max_share"], p["wordings"], p["wording_max_share"])
print(files)
