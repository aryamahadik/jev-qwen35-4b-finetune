"""G5 scoring (check:F10): join the blind answers (tmp/chk/g5_answers.jsonl, written before any gold join) with gold in
canonical option order. Prints counts and disagreeing sample indices only (no row text). Program rows (S1-S4, S6):
every disagreement must be re-read and classified in tmp/chk/g5_review.json as {"i": .., "verdict": "reader_error" |
"clearly_wrong" | "ambiguous", "why": ..}. Real-text rows (S7): dataset-level only (spec G5: drop a dataset if > 8%
clearly wrong); annotation-dependent golds the text cannot settle are counted as 'not inferable', not wrong.
Usage: chk_g5_score.py [--write]"""
import json, sys
from collections import Counter, defaultdict
import chk_lib as q

# recheck:F10 r1: --seed N (default 5001 = the first check); other seeds read qc/g5_sample_ids_<N>.json,
# tmp/rchk/g5_<N>_answers.jsonl and tmp/rchk/g5_<N>_review.json; real-text (S7) disagreements are reviewed too and
# their verdicts are counted per dataset (drop rule: > 8 % clearly wrong).
SEED = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 5001
D5 = q.TMP if SEED == 5001 else q.F10 / "tmp/rchk"; PFX = "g5" if SEED == 5001 else f"g5_{SEED}"
rows, _ = q.load("candidates_r1"); by = {r["id"]: r for r in rows}
ids = json.load(open(q.QC / ("g5_sample_ids.json" if SEED == 5001 else f"g5_sample_ids_{SEED}.json")))
ans = {}
for l in open(D5 / f"{PFX}_answers.jsonl"):
    a = json.loads(l); ans[a["i"]] = a
rev = {}
p = D5 / f"{PFX}_review.json"
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
s7i = {i for d in rt.values() for i in d["disagree"]}
cw = [i for i, v in rev.items() if v["verdict"] == "clearly_wrong" and i not in s7i]
amb = [i for i, v in rev.items() if v["verdict"] == "ambiguous" and i not in s7i]
rtv = {k: dict(Counter(rev[i]["verdict"] for i in d["disagree"] if i in rev)) for k, d in rt.items()}
unrev = [i for i in prog["disagree"] if i not in rev] + [i for i in s7i if i not in rev]  # check3: S7 reviewed for every seed
res = {"answered": len(ans), "program": prog, "real_text": dict(rt), "unreviewed_program_disagreements": unrev,
       "clearly_wrong": cw, "ambiguous": amb}
print(json.dumps(res))
if "--write" in sys.argv:
    assert len(ans) == 300 and not unrev, "answer all 300 rows and review every program disagreement first"
    out = {"gate": "G5", "checker": "check:F10 (c-lanes-v3; independent, never a generator or solver author)",
           "pool": "out/candidates_r1.jsonl", "pool_sha256": q.sha(q.OUT / "candidates_r1.jsonl"),
           "sample": {"n": 300, "seed": SEED, "method": f"random.Random({SEED}).sample(range(n_pool), 300)",
                      "ids_file": "qc/g5_sample_ids.json" if SEED == 5001 else f"qc/g5_sample_ids_{SEED}.json",
                      "view": "decoder_io.user_msg, OD_STYLE=cygnet, LAYOUT=schema_branch_mark, canonical option order; gold never shown; "
                              "second verbatim copy of instructions replaced by a marker when rendered for reading"},
           "procedure": f"reader answered every row blind ({D5.relative_to(q.F10)}/{PFX}_answers.jsonl) before any gold join; "
                        f"qc/chk_g5_score.py joins gold; every disagreement re-read ({D5.relative_to(q.F10)}/{PFX}_review.json)",
           "program_rows": {"n": prog["n"], "agree": prog["agree"], "disagree": len(prog["disagree"])},
           "clearly_wrong": len(cw), "ambiguous": len(amb), "flags": [rev[i] | {"id": ids[i]} for i in cw + amb],
           "reader_errors": [i for i, v in rev.items() if v["verdict"] == "reader_error"],
           "real_text_rows": {k: {"n": v["n"], "agree": v["agree"], "reader_differs": len(v["disagree"]), "verdicts": rtv.get(k, {}),
                                  "clearly_wrong_share": round(rtv.get(k, {}).get("clearly_wrong", 0) / max(1, v["n"]), 4)} for k, v in rt.items()},
           "real_text_clearly_wrong": sum(d.get("clearly_wrong", 0) for d in rtv.values()),
           "real_text_rule": "dataset-level only (drop a dataset if > 8% clearly wrong); annotation-dependent codes are not inferable from the text alone",
           "pass_rule": "0 clearly wrong program rows, ambiguous <= 3 (1%), no S7 dataset > 8% clearly wrong"}
    out["pass"] = (out["clearly_wrong"] == 0 and out["ambiguous"] <= 3
                   and all(v["clearly_wrong_share"] <= 0.08 for v in out["real_text_rows"].values()))
    (q.QC / "g5.json").write_text(json.dumps(out, indent=1))
    print("written", out["pass"])
