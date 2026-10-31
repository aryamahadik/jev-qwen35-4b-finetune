"""G5 repair round, step 3: compare the blind answers (tmp/checker/g5r2_answers.jsonl, one {"i", "ans"} per row,
written before gold was looked at) with gold; prints counts and disagreeing row indices only (no row text)."""
import json
import qc_lib as q
rows = {r["id"]: r for r in q.load("candidates_r1")}
ids = json.load(open(q.QC / "g5r2_sample_ids.json"))
ans = {}
for l in open(q.TMP / "g5r2_answers.jsonl"):
    a = json.loads(l); ans[a["i"]] = a["ans"]
dis = []
for i, a in sorted(ans.items()):
    g = q.gold_letter(rows[ids[i]])
    if a != g:
        dis.append((i, a, g, rows[ids[i]]["qtype"]))
missing = [i for i in range(len(ids)) if i not in ans]
print(json.dumps({"answered": len(ans), "missing": missing, "agree": len(ans) - len(dis),
                  "disagree": [list(x) for x in dis]}))
