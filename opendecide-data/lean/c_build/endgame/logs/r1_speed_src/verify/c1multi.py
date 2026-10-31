import json, time, statistics as st
from vlib import *
L = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/"
cfg = json.load(open(L + "runs/q35_4b_main.json"))
rows = rj(L + "data/v14_parts/golden_train.jsonl")
rels = rj(L + "data/v14_parts/golden_relations.jsonl")
res = []
for seed in (101, 202, 303):
    out, _, _ = run(rows, rels, seed, 350, cfg, budgets=(8192, 10240), pads=(256,))
    res += out[10:]
p8 = st.mean(o["pad_8192_256"] for o in res); p10 = st.mean(o["pad_10240_256"] for o in res)
sd = st.pstdev(o["pad_8192_256"] for o in res)
print("C1 draws", len(res), "pad8192 %.0f (sd/step %.0f) pad10240 %.0f ratio %.3f nmb %.2f twins %.2f anc %.2f" % (
    p8, sd, p10, p10 / p8, st.mean(o["nmb_8192_256"] for o in res), st.mean(o["twins"] for o in res), st.mean(o["anc"] for o in res)))
print("rate 8192 %.4f ms  rate 10240 %.4f ms" % (2766.5 / p8, 2913.1 / p10))
