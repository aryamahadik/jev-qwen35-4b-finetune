from sim import *
P = LEAN + "/c_build/endgame/presmoke/"
rows = read_jsonl(P + "c_presmoke_r1.jsonl"); rels = read_jsonl(P + "c_presmoke_rel_r1.jsonl")
def blk(s):
    if s.startswith("c_pub_"): return "public"
    if s.startswith("commit_"): return "commit"
    if s.startswith("own_F2"): return "F2"
    if s.startswith("c_own_"): return s[6:]
    if s.startswith("c_f"): return "F" + s[3:].split("_")[0]
    return "replay"
B = {r["id"]: blk(r["source"]) for r in rows}
L = lengths(rows)
nrel = Counter(); 
for x in rels: nrel[B[x["a"]]] += 1
out = {}
for b in ["replay"] + [f"F{i}" for i in range(1, 14)] + ["public", "commit"]:
    rs = [r for r in rows if B[r["id"]] == b]; v = sorted(L[r["id"]] for r in rs)
    out[b] = {"n": len(rs), "tok_mean": round(st.mean(v)), "tok_med": v[len(v)//2], "choice": round(sum(r["qtype"]=="choice" for r in rs)/len(rs),2),
              "rel_per_row": round(nrel[b]/len(rs), 2), "rows_per_unit": round(len(rs)/len({r["call_id"] for r in rs}), 2)}
    print(b, out[b])
tokw = sum(L.values())
print("presmoke mean tok/row", round(tokw/len(rows)), "replay token share", round(sum(L[r['id']] for r in rows if B[r['id']]=='replay')/tokw, 3))
units = by_call(rows)
fs = [summ(simulate(units, L, 110, s)) for s in (1, 2, 3, 4, 5)]
print("sim on presmoke rows (5 reshuffles x110 steps) pad_tok:", [f["pad_tok"] for f in fs], "n_micro", [f["n_micro"] for f in fs])
json.dump({"by_block": out, "lens": L}, open("presmoke_blocks.json", "w"))
