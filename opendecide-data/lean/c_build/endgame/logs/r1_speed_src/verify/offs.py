import json, random, statistics as st
from vlib import *
L = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/"
P = json.load(open("pool_F11.json"))
rows = rj(L + "c_src/F11/out/candidates_r1.jsonl")[:400]
mix = [len(x) for x in tok([decoder_io.CYGNET_SYSTEM + "\n" + decoder_io.user_msg(r) for r in rows], add_special_tokens=False)["input_ids"]]
mine = [P["len"][r["id"]] for r in rows]
d = [a - b for a, b in zip(mine, mix)]
print("mine - mixer-style: mean %.1f min %d max %d" % (st.mean(d), min(d), max(d)))
# share of all new-pool rows within [2000, 2000+max offset)
off = max(d)
for b in ["F1","F6","F7","F9","F10","F11","F12","public"]:
    Q = json.load(open(f"pool_{b}.json"))["len"].values()
    print(b, "rows in [2000,%d): %d of %d" % (2000 + off, sum(2000 <= x < 2000 + off for x in Q), len(Q)))
