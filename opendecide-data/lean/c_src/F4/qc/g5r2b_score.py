"""G5 repair r1b top-up score: blind answers (tmp/checker/g5r2b_answers.jsonl) vs gold on the final rows, merged with
the carried-over r2 answers for the 293 unchanged sample rows. Counts and indices only (no row text)."""
import json
import qc_lib as q
rows = {r["id"]: r for r in q.load("candidates_r1")}
plan = json.load(open(q.QC / "g5r2b_plan.json"))
ids = {i: rid for i, rid in plan["todo"]}
new = {json.loads(l)["i"]: json.loads(l)["ans"] for l in open(q.TMP / "g5r2b_answers.jsonl")}
old = {json.loads(l)["i"]: json.loads(l)["ans"] for l in open(q.TMP / "g5r2_answers.jsonl")}
dis_new = [(i, a, q.gold_letter(rows[ids[i]])) for i, a in sorted(new.items()) if a != q.gold_letter(rows[ids[i]])]
fin = plan["final_ids"]
carried = [i for i in plan["kept_positions"]]
dis_carried = [(i, old[i], q.gold_letter(rows[fin[i]])) for i in carried if old[i] != q.gold_letter(rows[fin[i]])]
sample_new = [i for i in new if i < 300]
out = {"sample_n": 300, "seed": 5002, "carried_unchanged": len(carried), "carried_agree": len(carried) - len(dis_carried),
       "reread_or_replaced": len(sample_new), "reread_agree": len(sample_new) - sum(1 for d in dis_new if d[0] < 300),
       "sample_agree_total": 300 - len(dis_carried) - sum(1 for d in dis_new if d[0] < 300),
       "extra_changed_rows": sum(1 for i in new if i >= 300), "extra_agree": sum(1 for i in new if i >= 300) - sum(1 for d in dis_new if d[0] >= 300),
       "missing": [i for i, _ in plan["todo"] if i not in new],
       "disagree": [list(d) for d in dis_carried + dis_new]}
json.dump(out, open(q.QC / "g5r2b.json", "w"), indent=1)
print(json.dumps(out))
