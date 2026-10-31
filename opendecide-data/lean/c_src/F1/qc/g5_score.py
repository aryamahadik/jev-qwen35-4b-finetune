"""G5 step 3: compare the blind answers (tmp/qc/g5_answers.jsonl) with gold; print only counts and the list of
disagreeing row indices (no row text)."""
import json, sys
import qc_lib as q
d = q.dio()
rows, _ = q.load("candidates_r1")
by = {r["id"]: r for r in rows}
ids = json.load(open(q.QC / "g5_sample_ids.json"))
ans = {}
for l in open(q.TMP / "g5_answers.jsonl"):
    a = json.loads(l); ans[a["i"]] = a["ans"]
dis = []
for i, a in sorted(ans.items()):
    r = by[ids[i]]
    if r["qtype"] == "noul":
        g = "A" if r["gold"] == 1 else "B"
    else:
        g = d.label(r["options"].index(r["gold"]))
    if a != g:
        dis.append((i, a, g))
print(json.dumps({"answered": len(ans), "agree": len(ans) - len(dis), "disagree": [list(x) for x in dis]}))
