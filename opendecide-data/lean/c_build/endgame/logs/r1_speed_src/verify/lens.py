import json, sys, time, random, glob, os
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_build")
from vlib import *
import crowd_select as cs
L = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/"
def pools():
    P = {}
    for f in [f"F{i}" for i in range(1, 14)] + ["COMMIT"]:
        ff = cs.fam_files(f)
        P[f] = (str(ff["cand"]), [str(ff["rel"])] if ff["rel"] else [])
    P["public"] = ([L + "c_src/public/" + x for x in ("public-1/out/public1_rows_r1.jsonl", "public-2/out/rows_r1.jsonl", "public-3/out/public3_rows_r1.jsonl")], [])
    P["replay"] = (sorted(glob.glob(L + "data/c_replay_r1_shards/shard_*.jsonl")), [L + "data/v14_parts/golden_relations.jsonl"])
    return P
if __name__ == "__main__":
    which = sys.argv[1:]
    P = pools()
    for name in which:
        t0 = time.time()
        files, rf = P[name]
        files = files if isinstance(files, list) else [files]
        rows = [r for p in files for r in rj(p)]
        rng = random.Random(7)
        out = {}
        for i in range(0, len(rows), 1000):
            ch = rows[i:i + 1000]
            perms = [rng.sample(range(len(r["options"])), len(r["options"])) if r["qtype"] == "choice" else rng.sample([0, 1], 2) for r in ch]
            for r, n in zip(ch, ntok(ch, perms)):
                out[r["id"]] = n
        light = [{"id": r["id"], "call_id": r["call_id"], "qtype": r["qtype"], "nopt": len(r["options"] or []),
                  "est": td._est_tokens(r), "ord": td.is_ordinal(r), "src": r["source"], "anc": bool((r.get("meta") or {}).get("anchor"))} for r in rows]
        ids = {r["id"] for r in rows}
        rels = [{"a": x["a"], "b": x["b"], "type": x["type"]} for p in rf for x in rj(p) if x["a"] in ids and x["b"] in ids]
        json.dump({"rows": light, "len": out, "rels": rels}, open(f"pool_{name}.json", "w"))
        import statistics as st
        v = list(out.values())
        print(name, len(rows), "rels", len(rels), "mean tok %.0f" % st.mean(v), "max", max(v), ">=2000 %.3f" % (sum(x >= 2000 for x in v) / len(v)), ">7900", sum(x > 7900 for x in v), "s", round(time.time() - t0))
