"""B0b task lists (A17-B0b): Nimble router tasks (C1 top prob < TAU, fixed a priori) + Decision Index knowledge questions."""
import gzip, json, os
TAU = 0.8
NS = "/Users/aryamahadik/Documents/jev/bench/nimble_suite"
REUSE = {"squad2", "paws", "pubmedqa"}  # already thought (768 tokens, A17-B0); reused for routed items
def to_di(q):
    t, c, ins = q["type"], q["criteria"], q.get("instructions") or ""
    if t == "noul": return {"type": "choice", "instructions": ins, "criteria": {"true": c["true"], "false": c["false"]}}
    if t == "score": return {"type": "choice", "instructions": ins, "criteria": {str(i): d for i, d in enumerate(c)}}
    return {"type": "choice", "instructions": ins, "criteria": dict(c)}
n = 0; routed = {}
with open("tasks_nimble.jsonl", "w") as fo:
    for d, pdir in (("data", "preds"), ("data_holdout", "preds_holdout")):
        for sub in sorted(os.listdir(f"{NS}/{d}")):
            recs = {json.loads(l)["id"]: json.loads(l) for l in open(f"{NS}/{d}/{sub}/all.jsonl")}
            for l in open(f"{NS}/{pdir}/{sub}.jsonl"):
                p = json.loads(l); pr = p["probs"] or {}
                top = max(pr.values()) if pr else 0.0
                if top >= TAU: continue
                routed[sub] = routed.get(sub, 0) + 1
                if sub in REUSE: continue
                r = recs[p["id"]]
                fo.write(json.dumps({"key": f"nimble|{sub}|{r['id']}", "state": r["input"]["state"],
                                     "question": to_di(r["input"]["questions"]["decision"]), "kind": r["input"]["questions"]["decision"]["type"]}) + "\n"); n += 1
print("nimble routed per subset:", routed, "new think tasks:", n)
DI = {"MMLU", "GPQA Diamond", "GSM8K", "CRUXEval", "CLadder"}; m = 0
with open("tasks_di.jsonl", "w") as fo:
    for l in gzip.open("/Users/aryamahadik/Documents/jev/bench/external_quarantine/decision_index/sample/sample10k.jsonl.gz", "rt"):
        r = json.loads(l); e = r["_evaluation"]
        if e["dataset"] not in DI: continue
        for qk, q in r["questions"].items():
            fo.write(json.dumps({"key": f"di|{e['run_id']}|{qk}", "state": r["state"], "question": q, "kind": "choice"}) + "\n"); m += 1
print("DI think tasks:", m)
