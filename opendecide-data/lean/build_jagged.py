"""Third-party injection test: zkousama/jagged (pre-registered audit of jev-1.13), Wikipedia Articles-for-Deletion.
Uses the audit's EXACT requests for the baseline arm and the adversarial arm (repeat 0, verdict question): the state
dict (discussion, participants, listing_length [+ editor_note with the injected line]), instructions and true/false
criteria. The published result: Jev accuracy 0.965 -> 0.265 under one injected line.
Writes data/eval_jagged.jsonl + data/eval_jagged_calls.jsonl.
"""
import ast
import gzip
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parents[1] / "bench/jagged/data/trials/afd.jsonl.gz"
trials = [json.loads(l) for l in gzip.open(SRC, "rt")]
pick = {(t["item_id"], t["arm"]): t for t in trials
        if t["question"] == "verdict" and t["repeat"] == 0 and t["arm"] in ("baseline", "adversarial")}
rows, calls = [], []
for (item, arm), t in sorted(pick.items()):
    req = t["request"] if isinstance(t["request"], dict) else ast.literal_eval(t["request"])
    crit = req["criteria"]
    rid = f"r_jag_{abs(hash(item)) % 10**10}_{arm}"
    rows.append({"id": rid, "group_id": f"g:jag:{item}", "call_id": "c_" + rid[2:], "split": "eval_jagged", "track": "JAG",
                 "source": "afd", "state": json.dumps(req["state"], ensure_ascii=False, indent=1), "qtype": "noul",
                 "instructions": req["instructions"], "options": None, "gold": int(bool(t["label"])), "role": "aff",
                 "card": f"- Yes: {crit['true']}\n- No: {crit['false']}", "noul_criteria": {"true": crit["true"], "false": crit["false"]},
                 "meta": {"arm": arm, "item_id": item, "jev_recorded_p_yes": float(t["probability"]) if t["probability"] not in (None, "None") else None}})
    calls.append({"call_id": rows[-1]["call_id"], "state": rows[-1]["state"], "row_ids": [rid]})
ids = {r["meta"]["item_id"] for r in rows if r["meta"]["arm"] == "baseline"} & {r["meta"]["item_id"] for r in rows if r["meta"]["arm"] == "adversarial"}
rows = [r for r in rows if r["meta"]["item_id"] in ids]
calls = [c for c in calls if any(c["row_ids"][0] == r["id"] for r in rows)]
(HERE / "data/eval_jagged.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
(HERE / "data/eval_jagged_calls.jsonl").write_text("".join(json.dumps(c) + "\n" for c in calls))
print(len(rows), "rows,", len(ids), "items")
