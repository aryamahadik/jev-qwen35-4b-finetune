"""P3-g9-reread score: both Haiku reads -> g5h.score per group -> Sonnet adjudication tasks (queue + seeded agreed controls).
Read-only on data/ (rows via c2_select.family_inputs); writes only under staged/P3-g9-reread/.
Run from lean/c2_build: ../../.venv/bin/python -B staged/P3-g9-reread/score.py"""
import sys, json, hashlib
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CB = HERE.parents[1]
sys.path.insert(0, str(CB))
import c2_select as S, crowd_select as cs, pilot as PI, qc_full_c2 as Q
from c2_kit import chunker, g5h

key = json.loads((HERE / "key.json").read_text())
man = json.loads((HERE / "manifest.json").read_text())
FAMS = [f for g in key["groups"].values() for f in g["families"]]
ilog = S.LinkGuardedInputLog()
rows_by_id, fam_of = {}, {}
for fam in FAMS:
    rows, rels, sh = S.family_inputs(ilog, fam)
    assert sh["candidates_sha256"] == key["candidates_sha256"][fam], fam
    for r in rows:
        rows_by_id[r["id"]] = r; fam_of[r["id"]] = fam

class KB:
    def __init__(s, rec): s.key, s.task_of = rec["key"], rec["task_of"]

out, adj_all, akey_all, summary = {}, [], {}, {}
for gname, g in key["groups"].items():
    ans, probs = {}, {}
    for rd in ("A", "B"):
        raw = {}
        for t in man["tasks"]:
            if t["reader"] == rd and t["group"] == gname:
                p = Path(t["answer_file"])
                raw[t["task_id"]] = json.loads(p.read_text()) if p.is_file() else None
        got, pr = chunker.load_answers(KB(g["readers"][rd]), {k: v for k, v in raw.items() if v is not None})
        ans[rd], probs[rd] = got, pr
    rows = [rows_by_id[i] for i in g["row_ids"]]
    res = g5h.score(rows, g["items"], ans["A"], ans["B"], seed=f"P3-g9-{gname}-control", n_control=30 if gname == "TOTH" else 10)
    adj, akey = g5h.adjudication_items(rows_by_id, res, seed=f"P3-g9-{gname}-adj")
    out[gname] = {"n_read": res["n_read"], "answered": {r: len(ans[r]) for r in ans}, "load_problems": probs,
                  "queue": res["queue"], "control": res["control"], "quarantined": res["quarantined"],
                  "templates": res["templates"], "per_row": res["per_row"]}
    # per-family disagreement counts
    byf = {}
    for rid, pr in res["per_row"].items():
        d = byf.setdefault(fam_of[rid], {"n": 0, "A_wrong": 0, "B_wrong": 0, "either": 0, "both": 0, "none": 0})
        d["n"] += 1
        ok = pr["agree_gold"]
        d["A_wrong"] += not ok[0]; d["B_wrong"] += not ok[1]
        d["either"] += not (ok[0] and ok[1]); d["both"] += (not ok[0] and not ok[1])
        d["none"] += (pr["reads"][0] is None) + (pr["reads"][1] is None)
    summary[gname] = {"queue": len(res["queue"]), "control": len(res["control"]), "by_family": byf,
                      "load_problems": {r: [p for p in probs[r]] for r in probs}, "quarantined": res["quarantined"]}
    for aid, it in adj:
        adj_all.append((gname, aid, it))
    akey_all[gname] = akey
json.dump(out, open(HERE / "score.json", "w"), indent=1)
json.dump(summary, open(HERE / "score_summary.json", "w"), indent=1)

# Sonnet adjudication tasks: <=50 items per task, per group; qid = aid within group
tasks = []
adir = HERE / "adjudication"
for gname in key["groups"]:
    items = [it | {"aid": aid} for g, aid, it in adj_all if g == gname]
    ckey = akey_all[gname]
    for n in range(0, len(items), Q.ADJ_CHUNK):
        part = items[n:n + Q.ADJ_CHUNK]
        tid = f"{gname}-ADJ-{n // Q.ADJ_CHUNK:03d}"
        # make aids unique across the whole lane: prefix group
        part = [{**p, "aid": f"{gname}-{p['aid']}"} for p in part]
        tf, af = adir / "tasks" / f"{tid}.md", adir / "answers" / f"{tid}.json"
        text = Q._task_file("G9 early re-read, adjudication (Claude, flag only)", gname, tid, af, part, Q.ADJ_PROMPT, Q.ADJ_CONTRACT)
        tf.parent.mkdir(parents=True, exist_ok=True); af.parent.mkdir(parents=True, exist_ok=True)
        tf.write_text(text, encoding="utf-8")
        tasks.append({"stage": "adjudication", "group": gname, "task_id": tid, "task_file": str(tf), "answer_file": str(af),
                      "n_items": len(part), "aids": [p["aid"] for p in part], "sha256": hashlib.sha256(text.encode()).hexdigest()})
akey_flat = {f"{g}-{a}": r for g, k in akey_all.items() for a, r in k.items()}
json.dump({"key": akey_flat, "note": "orchestrator only"}, open(adir / "key.json", "w"), indent=1)
json.dump({"tasks": tasks, "prompt_sha": chunker.sha(Q.ADJ_PROMPT)}, open(adir / "manifest.json", "w"), indent=1)
print(json.dumps(summary, indent=1)[:6000])
print(len(tasks), "adjudication tasks")
