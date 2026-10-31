"""G5 step 3: compare the blind answers (tmp/qc/g5_answers.jsonl) with gold; print only counts and the list of
disagreeing row indices (no row text)."""
import json
from collections import Counter
import qc_lib as q
rows, side = q.load("candidates_r1")
by = {r["id"]: r for r in rows}
ids = json.load(open(q.QC / "g5_sample_ids.json"))
ans = {}
for l in open(q.TMP / "g5_answers.jsonl"):
    a = json.loads(l); ans[a["i"]] = a["ans"]
dis = []; forms = Counter(); fagree = Counter()
for i, a in sorted(ans.items()):
    r = by[ids[i]]
    g = q.gold_letter(r)
    f = side.get(r["id"], {}).get("form", "?")
    forms[f] += 1
    if a != g:
        dis.append((i, a, g, f))
    else:
        fagree[f] += 1
print(json.dumps({"answered": len(ans), "agree": len(ans) - len(dis), "by_form": {k: [fagree[k], v] for k, v in forms.items()},
                  "disagree": [list(x) for x in dis]}))
