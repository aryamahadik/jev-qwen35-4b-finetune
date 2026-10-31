"""G5 r1.1 scoring: blind answers (tmp/qc/g5_r11_answers.jsonl) vs gold; counts and disagreeing indices only."""
import json
import qc_lib as q
d = q.dio()
rows, _ = q.load("candidates_r1")
by = {r["id"]: r for r in rows}
ids = json.load(open(q.QC / "g5_r11_sample_ids.json"))
ans = {}
for l in open(q.TMP / "g5_r11_answers.jsonl"):
    a = json.loads(l); ans[a["i"]] = a["ans"]
dis = []
for i, a in sorted(ans.items()):
    r = by[ids[i]]
    g = ("A" if r["gold"] == 1 else "B") if r["qtype"] == "noul" else d.label(r["options"].index(r["gold"]))
    if a != g:
        dis.append((i, a, g))
print(json.dumps({"answered": len(ans), "agree": len(ans) - len(dis), "disagree": [list(x) for x in dis]}))
