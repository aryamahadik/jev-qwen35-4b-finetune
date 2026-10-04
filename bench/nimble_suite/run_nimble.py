"""A18: C1 on the 13 rebuilt Bespoke Nimble public subsets, through the SAME fixed request->row mapping as the Decision
Index run (od_engine.ODEngine, shipped A5 readout). Writes probabilities only; scoring is score_nimble.py.
  noul  {false,true}  -> choice with keys true/false (od_engine reads it as our yes/no row, P(yes)=P(true))
  choice {key: desc}  -> choice as is (named keys + definitions card)
  score [desc...]     -> choice with keys "0".."K-1" (positional -> option text = level description)
Run: PYTHONPATH=<di repo>:<od_engine dir> python run_nimble.py --data data --out preds [--fake]"""
import argparse, json, os, sys, time
from pathlib import Path
ap = argparse.ArgumentParser()
ap.add_argument("--data", default="data"); ap.add_argument("--out", default="preds"); ap.add_argument("--fake", action="store_true")
ap.add_argument("--adapter", default=os.path.expanduser("~/lean/models/q35_4b_main500k")); ap.add_argument("--lean", default=os.path.expanduser("~/lean"))
ap.add_argument("--limit", type=int, default=0)
a = ap.parse_args()
from od_engine import ODEngine
opts = dict(base="Qwen/Qwen3.5-4B", revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a", adapter=a.adapter, lean=a.lean,
            adapter_sha256="507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078")
if a.fake: opts["fake"] = True
eng = ODEngine(**opts)
def to_di(q):
    t, crit, ins = q["type"], q["criteria"], q.get("instructions") or ""
    if t == "noul": return {"type": "choice", "instructions": ins, "criteria": {"true": crit["true"], "false": crit["false"]}}, "noul"
    if t == "choice": return {"type": "choice", "instructions": ins, "criteria": dict(crit)}, "choice"
    if t == "score": return {"type": "choice", "instructions": ins, "criteria": {str(i): d for i, d in enumerate(crit)}}, "score"
    raise ValueError(t)
Path(a.out).mkdir(exist_ok=True)
for sub in sorted(os.listdir(a.data)):
    f = Path(a.data) / sub / "all.jsonl"
    if not f.exists(): continue
    outp = Path(a.out) / f"{sub}.jsonl"
    done = {json.loads(l)["id"] for l in open(outp)} if outp.exists() else set()
    t0 = time.time(); n = 0
    with open(outp, "a") as fo:
        for l in open(f):
            r = json.loads(l)
            if r["id"] in done: continue
            q, kind = to_di(r["input"]["questions"]["decision"])
            try:
                resp, raw = eng(r["input"]["state"], {"decision": q})
                ans = resp["answers"]["decision"]; probs = ans.get("probabilities")
                fo.write(json.dumps({"id": r["id"], "kind": kind, "probs": probs, "status": "ok"}) + "\n")
            except Exception as e:  # Unsupported (capacity) -> scored as wrong
                fo.write(json.dumps({"id": r["id"], "kind": kind, "probs": None, "status": type(e).__name__}) + "\n")
            n += 1
            if a.limit and n >= a.limit: break
    print(json.dumps({"subset": sub, "new": n, "sec": round(time.time() - t0, 1)}), flush=True)
print("RUN DONE", json.dumps(eng.stats), flush=True)
