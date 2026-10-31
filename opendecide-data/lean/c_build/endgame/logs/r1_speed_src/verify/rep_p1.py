import json, sys, statistics as st
from vlib import *
L = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/"
cfg = json.load(open(L + "c_build/endgame/presmoke/q35_4b_c_presmoke.json"))
rows = rj(L + "c_build/endgame/presmoke/c_presmoke_r1.jsonl")
rels = rj(L + "c_build/endgame/presmoke/c_presmoke_rel_r1.jsonl")
sp = json.load(open(L + "logs/pilot/speed_h100_mt8192_log_every-1.json"))
out, units, rels = run(rows, rels, cfg["seed"], 40, cfg, budgets=(4096, 6144, 8192, 12288), pads=(64, 256))
log = sp["log"]
m = {k: sum(1 for o, g in zip(out, log) if o[a] == g[b]) for k, a, b in
     [("twin", "twins", "n_twin"), ("ord", "n_ord", "n_ord"), ("cons", "cons_8192_256", "n_cons"), ("inv", "inv_8192_256", "n_inv")]}
print("hash0", out[0]["hash"] == sp["first_batch"], "hash39", out[39]["hash"] == sp["last_batch"], "matches/40", m)
print("aux-vs-micro cons/inv diffs (relations split across micro-batches) 8192:",
      sum(o["ac_cons"] - o["cons_8192_256"] for o in out), sum(o["ac_inv"] - o["inv_8192_256"] for o in out))
T = sp["step_s"]
tm = list(range(5, 39))
pt = [out[s]["pad_8192_256"] for s in tm]
print("timed rows %.2f twins %.2f nmb %.2f pad %.0f real %.0f" % (
    st.mean(out[s]["rows"] for s in tm), st.mean(out[s]["twins"] for s in tm), st.mean(out[s]["nmb_8192_256"] for s in tm),
    st.mean(pt), st.mean(out[s]["real"] for s in tm)))
print("rate ms/padded tok %.4f  (sum t / sum pad)" % (1000 * sum(T[s] for s in tm) / sum(pt)))
for B in (4096, 6144, 8192, 12288):
    for P in (64, 256):
        print(B, P, "pad/step %.0f nmb %.2f" % (st.mean(out[s][f"pad_{B}_{P}"] for s in tm), st.mean(out[s][f"nmb_{B}_{P}"] for s in tm)),
              "cons/inv lost vs whole batch:", sum(o["ac_cons"] - o[f"cons_{B}_{P}"] for o in out), sum(o["ac_inv"] - o[f"inv_{B}_{P}"] for o in out))
json.dump([{k: v for k, v in o.items()} for o in out], open("p1_steps.json", "w"))
