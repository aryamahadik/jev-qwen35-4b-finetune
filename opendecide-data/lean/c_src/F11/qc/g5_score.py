"""G5 scorer (F11 independent checker). Joins the blind answers (tmp/chk/g5_answers.jsonl, written BEFORE looking at
gold) with gold from out/candidates_r1.jsonl via tmp/chk/g5_prompts.jsonl. Prints/записывает only ids, slices, labels.
Usage: g5_score.py [--write]  (writes qc/g5.json when flags file tmp/chk/g5_review.json exists)."""
import json, sys, collections
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
import chk_lib as q

rows = {r["id"]: r for r in q.load("candidates_r1")}
prompts = {json.loads(l)["k"]: json.loads(l) for l in open(q.TMP / "g5_prompts.jsonl")}
ans = {json.loads(l)["k"]: json.loads(l) for l in open(q.TMP / "g5_answers.jsonl")}


def short(o):
    return o.split(": ", 1)[0].strip() if isinstance(o, str) else str(o)


res = []
for k in sorted(prompts):
    p = prompts[k]; r = rows[p["id"]]; a = ans[k]
    sl = p["id"].split("-")[2]
    real = sl == "S7" or bool(a.get("real"))
    if r["qtype"] == "choice":
        g = short(r["options"][r["gold"]]) if isinstance(r["gold"], int) else short(r["gold"])
    else:
        g = "yes" if int(r["gold"]) == 1 else "no"
    if a["ans"] == "?":
        st = "abstain"
    else:
        st = "agree" if a["ans"].strip().lower() == g.strip().lower() else "disagree"
    res.append({"k": k, "id": p["id"], "slice": sl, "qtype": r["qtype"], "real": real, "status": st,
                "ans": a["ans"], "gold": g, "subtype": r["meta"].get("subtype"), "twin_kind": r["meta"].get("twin_kind")})
c = collections.Counter((x["real"], x["status"]) for x in res)
print("counts (real,status):", dict(c))
for x in res:
    if x["status"] == "disagree":
        print(json.dumps({k: x[k] for k in ("k", "id", "slice", "qtype", "real", "ans", "gold", "subtype", "twin_kind")}))
json.dump(res, open(q.TMP / "g5_scored.json", "w"))
