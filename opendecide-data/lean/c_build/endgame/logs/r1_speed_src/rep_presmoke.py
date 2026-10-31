from lib import *
import time
t=time.time()
P = LEAN + "/c_build/endgame/presmoke/"
rows = read_jsonl(P + "c_presmoke_r1.jsonl"); rels = read_jsonl(P + "c_presmoke_rel_r1.jsonl")
out, units = replay(rows, rels, 20261006, 40)
d = json.load(open(LEAN + "/logs/pilot/speed_h100_mt8192_log_every-1.json"))
print("first hash ok", out[0]["hash"] == d["first_batch"], "last ok", out[-1]["hash"] == d["last_batch"])
tw_ok = sum(o["twins"] == l["n_twin"] for o, l in zip(out, d["log"]))
print("twin counts match", tw_ok, "/ 40", "units", len(units))
for o, s in zip(out, d["step_s"]): o["t"] = s
json.dump([{k: v for k, v in o.items() if k != "batch_ids"} | {"ids": o["batch_ids"]} for o in out], open("presmoke_steps.json", "w"))
print("sec", round(time.time()-t,1))
