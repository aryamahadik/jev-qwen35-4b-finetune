"""G5 blind read, step 2 (independent F8 checker): compare the reader's answers (tmp/chk/g5/answers.jsonl, one per
sampled row, letters in canonical option order: A = options[0] / Yes) with the golds. Prints only ids, letters and
counts (no row text). Disagreements are re-read by hand and classified in g5.json."""
import json
import qc_lib as L
ids = json.load(open(L.QC / "g5_sample_ids.json"))
rows = {r["id"]: r for r in L.load("candidates_r1")}
ans = {}
for l in open(L.TMP / "g5/answers.jsonl"):
    d = json.loads(l); ans[d["i"]] = d
dis = []
for i, rid in enumerate(ids):
    r = rows[rid]; a = ans[i]["a"]
    if L.is_yn(r):
        gold = "A" if int(r["gold"]) == 1 else "B"
    else:
        gold = L.dio().label(L.gold_index(r))
    if a != gold:
        dis.append({"i": i, "id": rid, "reader": a, "gold": gold, "note": ans[i].get("n")})
print("answered", len(ans), "of", len(ids), "disagree", len(dis))
for d in dis:
    print(d)
json.dump(dis, open(L.TMP / "g5/disagreements.json", "w"), indent=1)
