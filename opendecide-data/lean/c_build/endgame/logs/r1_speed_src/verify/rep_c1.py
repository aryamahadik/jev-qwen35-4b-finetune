import json, sys, time, statistics as st
from vlib import *
L = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/"
t0 = time.time()
cfg = json.load(open(L + "runs/q35_4b_main.json"))
rows = rj(L + "data/v14_parts/golden_train.jsonl")
rels = rj(L + "data/v14_parts/golden_relations.jsonl")
print("load s", round(time.time() - t0), len(rows), len(rels))
sp = json.load(open(L + "logs/pilot/speed_h100_mt8192.json"))
sp2 = json.load(open(L + "logs/pilot/speed_h100_mt10240.json"))
out, units, rels = run(rows, rels, cfg["seed"], 100, cfg, budgets=(8192, 10240), pads=(256,))
print("hash0", out[0]["hash"] == sp["first_batch"], "hash99", out[99]["hash"] == sp["last_batch"])
lg = {g["step"]: g for g in sp["log"]}
for s, g in lg.items():
    print("step", s, "twin", out[s]["twins"], g["n_twin"], "cons", out[s]["cons_8192_256"], g["n_cons"], "inv", out[s]["inv_8192_256"], g["n_inv"])
tm = range(10, 99)
for B, S in ((8192, sp), (10240, sp2)):
    pt = [out[s][f"pad_{B}_256"] for s in tm]
    T = S["step_s"]
    print(B, "rows %.2f twins %.2f nmb %.2f pad %.0f real %.0f anc/step %.2f rate ms/tok %.4f" % (
        st.mean(out[s]["rows"] for s in tm), st.mean(out[s]["twins"] for s in tm), st.mean(out[s][f"nmb_{B}_256"] for s in tm),
        st.mean(pt), st.mean(out[s]["real"] for s in tm), st.mean(out[s]["anc"] for s in tm), 1000 * sum(T[s] for s in tm) / sum(pt)))
json.dump(out, open("c1_steps.json", "w"))
print("total s", round(time.time() - t0))
