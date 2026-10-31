"""G5 blind read (repair r1), step 3: compare the blind answers (tmp/qc/g5r2_answers.jsonl: {"i", "ans", "flag"})
with gold; counts and disagreeing row indices only (no row text)."""
import json, sys
from collections import Counter
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F6/qc")
import qc_lib as q
rows, side = q.load("candidates_r1")
by = {r["id"]: r for r in rows}
ids = json.load(open(q.QC / "r2" / "g5r2_sample_ids.json"))
ans = {}
for l in open(q.TMP / "g5r2_answers.jsonl"):
    a = json.loads(l)
    ans[a["i"]] = a
dis = []
forms, fagree = Counter(), Counter()
for i, a in sorted(ans.items()):
    r = by[ids[i]]
    g = q.gold_letter(r)
    f = side.get(r["id"], {}).get("form", "?")
    forms[f] += 1
    if a["ans"] != g:
        dis.append((i, a["ans"], g, f))
    else:
        fagree[f] += 1
print(json.dumps({"answered": len(ans), "agree": len(ans) - len(dis), "by_form": {k: [fagree[k], v] for k, v in forms.items()},
                  "disagree": [list(x) for x in dis]}))
