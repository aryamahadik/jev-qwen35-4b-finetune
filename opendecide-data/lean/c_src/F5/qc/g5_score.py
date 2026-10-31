"""G5 scoring (independent F5 checker): compare my blind answers (tmp/chk/g5_answers.jsonl, written before any gold
was seen) to gold for the 600 sampled rows (qc/g5_sample_ids.json, seed 5001). Prints mismatch list (k, id, my answer,
gold, row_type, world) for adjudication; writes tmp/chk/g5_mismatch.json. No row texts."""
import json
import qc_lib as L

ids = json.load(open(L.QC / "g5_sample_ids.json"))["ids"]
rows = {r["id"]: r for r in L.load("candidates_r1")}
side = L.load_side("candidates_r1")
ans = {x["k"]: x for x in map(json.loads, open(L.TMP / "g5_answers.jsonl"))}
mm = []
for k, rid in enumerate(ids):
    r = rows[rid]; g = "Y" if int(r["gold"]) == 1 else "N"
    if ans[k]["a"] != g:
        m = r["meta"]
        mm.append({"k": k, "id": rid, "mine": ans[k]["a"], "gold": g, "row_type": m.get("row_type"),
                   "world": m.get("world"), "sampler": m.get("sampler"), "note": ans[k].get("note")})
noted = [{"k": k, "id": ids[k], "note": ans[k]["note"]} for k in ans if ans[k].get("note")]
json.dump({"n": len(ids), "n_mismatch": len(mm), "mismatch": mm, "noted": noted}, open(L.TMP / "g5_mismatch.json", "w"), indent=1)
print("n", len(ids), "mismatch", len(mm), "noted", len(noted))
for x in mm:
    print(x)
