from lib import *
import time
t = time.time()
D = LEAN + "/data/v14_parts/"
rows = read_jsonl(D + "golden_train.jsonl"); rels = read_jsonl(D + "golden_relations.jsonl")
print("rows", len(rows), "rels", len(rels), "load s", round(time.time() - t, 1), flush=True)
out, units = replay(rows, rels, 20260925, 100, anchor=True)
d = json.load(open(LEAN + "/logs/pilot/speed_h100_mt8192.json"))
print("first ok", out[0]["hash"] == d["first_batch"], "last ok", out[-1]["hash"] == d["last_batch"], "units", len(units),
      "n_steps", math.ceil(len(rows) / 16 * 0.9712363276890207), "pilot n_full", d["n_steps_full"])
for o, s in zip(out, d["step_s"]): o["t"] = s
json.dump([{k: v for k, v in o.items() if k != "batch_ids"} for o in out], open("c1_steps.json", "w"))
print("anchor rows in file", sum(1 for r in rows if (r.get("meta") or {}).get("anchor")), "sec", round(time.time() - t, 1))
