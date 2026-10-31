"""G5 scoring (check:F12): join the blind answers (tmp/chk/g5_answers.jsonl, written before any gold join) with gold in
canonical option order. Prints counts and disagreeing sample indices only (no row text). Program rows (S1-S4, S6):
every disagreement must be re-read and classified in tmp/chk/g5_review.json as {"i": .., "verdict": "reader_error" |
"clearly_wrong" | "ambiguous", "why": ..}. Real-text rows (S7): dataset-level only (spec G5: drop a dataset if > 8%
clearly wrong); annotation-dependent golds the text cannot settle are counted as 'not inferable', not wrong.
Usage: chk_g5_score.py [--write]"""
import json, os, sys
from collections import Counter, defaultdict
import chk_lib as q
SEED = int(os.environ.get("G5_SEED", "5001"))
SUF = "" if SEED == 5001 else f"_s{SEED}"

rows, _ = q.load("candidates_r1"); by = {r["id"]: r for r in rows}
ids = json.load(open(q.QC / "g5_sample_ids.json"))
ans = {}
for l in open(q.TMP / f"g5{SUF}_answers.jsonl"):
    a = json.loads(l); ans[a["i"]] = a
rev = {}
p = q.TMP / f"g5{SUF}_review.json"
if p.exists():
    rev = {d["i"]: d for d in json.load(open(p))}
prog = {"n": 0, "agree": 0, "disagree": []}; rt = defaultdict(lambda: {"n": 0, "agree": 0, "disagree": []})
for i, a in sorted(ans.items()):
    r = by[ids[i]]; g = q.gold_letter(r); s7 = r["meta"]["sampler"] == "S7"
    d = rt[(r["meta"].get("text_source") or {}).get("dataset")] if s7 else prog
    d["n"] += 1
    if a["ans"] == g:
        d["agree"] += 1
    else:
        d["disagree"].append(i)
cw = [i for i, v in rev.items() if v["verdict"] == "clearly_wrong"]; amb = [i for i, v in rev.items() if v["verdict"] == "ambiguous"]
unrev = [i for i in prog["disagree"] if i not in rev]
res = {"answered": len(ans), "program": prog, "real_text": dict(rt), "unreviewed_program_disagreements": unrev,
       "clearly_wrong": cw, "ambiguous": amb}
print(json.dumps(res))
if "--write" in sys.argv:
    assert len(ans) == 300 and not unrev, "answer all 300 rows and review every program disagreement first"
    out = {"gate": "G5", "checker": "check:F12 (c-lanes-v3; independent, never a generator or solver author)",
           "pool": "out/candidates_r1.jsonl", "pool_sha256": q.sha(q.OUT / "candidates_r1.jsonl"),
           "sample": {"n": 300, "seed": SEED, "method": f"random.Random({SEED}).sample(range(n_pool), 300)", "ids_file": "qc/g5_sample_ids.json",
                      "view": "decoder_io.user_msg, OD_STYLE=cygnet, LAYOUT=schema_branch_mark, canonical option order; gold never shown; "
                              "second verbatim copy of instructions replaced by a marker when rendered for reading"},
           "procedure": f"reader answered every row blind (tmp/chk/g5{SUF}_answers.jsonl) before any gold join; qc/chk_g5_score.py joins gold; "
                        f"every program-row disagreement re-read (tmp/chk/g5{SUF}_review.json)",
           "program_rows": {"n": prog["n"], "agree": prog["agree"], "disagree": len(prog["disagree"])},
           "clearly_wrong": len(cw), "ambiguous": len(amb), "flags": [rev[i] | {"id": ids[i]} for i in cw + amb],
           "reader_errors": [i for i, v in rev.items() if v["verdict"] == "reader_error"],
           "real_text_rows": {k: {"n": v["n"], "agree": v["agree"], "reader_differs": len(v["disagree"])} for k, v in rt.items()},
           "real_text_rule": "n/a (F12 has no real-text rows)",
           "pass_rule": "0 clearly wrong and ambiguous <= 3 (1%)"}
    out["pass"] = out["clearly_wrong"] == 0 and out["ambiguous"] <= 3
    (q.QC / "g5.json").write_text(json.dumps(out, indent=1))
    print("written", out["pass"])
