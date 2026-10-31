"""Few-shot worked examples (G0 7.5, repair r1): every worked example on every few-shot card is re-solved by the
independent solver B (solverB/solver_b.py, model enumeration) under the card's own printed clauses, and its printed
answer must match. Each example becomes a pseudo yes/no row: the card text of a real row on that card, the example's
record as the state (its reserved name EX-000k mapped to a record-format ID and typed with the card's type noun, since
solver B reads record IDs only) and the example's question. Also counts few-shot cards / rows in the rendered set.
Prints counts only. Usage: fewshot_check.py <name>"""
import json, pickle, re, sys, importlib.util
from collections import Counter
from pathlib import Path

F4 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(F4 / "gen"))
NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
spec = importlib.util.spec_from_file_location("solver_b_indep", F4 / "solverB" / "solver_b.py")
SB = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SB)
import build as B  # noqa: E402
import fewshot as FS  # noqa: E402
import render_f4 as R  # noqa: E402

pl = pickle.load(open(F4 / "tmp" / "cards_r1.pkl", "rb"))
cards = {cp.card_id: cp for cp in pl["cards"]}
one_card_text, rows_fs = {}, Counter()
hdrs = [json.loads(x)["header"] for x in open(F4.parents[0] / "formats" / "formats-1" / "data" /
                                               "fewshot_templates.jsonl") if json.loads(x).get("header")]
for ln in open(F4 / "out" / f"{NAME}.jsonl"):
    r = json.loads(ln)
    cid = r["meta"]["card_id"]
    txt = (r.get("card") or "") + "\n" + r["instructions"]
    if "Record: EX-000" in txt:
        rows_fs[cid] += 1
        if r["qtype"] == "noul":
            one_card_text.setdefault(cid, r["card"])
res = {"few_shot_cards_planned": sum(1 for cp in pl["cards"] if cp.fewshot), "few_shot_cards_rendered": len(rows_fs),
       "rows_with_block": sum(rows_fs.values()), "cards_total": len(pl["cards"]), "examples": 0, "agree": 0,
       "mismatch": [], "templates": Counter(), "answers": Counter()}
for cid, ctext in one_card_text.items():
    cp = cards[cid]
    blk = FS.make_block(cp, B.card_of(cp))
    res["templates"][blk["template"]] += 1
    lx = R.Lex(cp, date_fmt=cp.date_fmt)
    tsg = lx.card_type()[0]
    for e in blk["examples"]:
        ck = e["_check"]
        if ck["record"] not in ctext or ck["question"] not in ctext:
            res["mismatch"].append({"card": cid, "why": "example_not_rendered"})
            continue
        m = {x: "EX-%05d" % (i + 1) for i, x in enumerate(("EX-0001", "EX-0002", "EX-0003"))}
        rec_t, q = ck["record"], ck["question"]
        for a, b in m.items():
            rec_t, q = rec_t.replace(a, b), q.replace(a, b)
        ent = re.findall(r"EX-\d{5}", rec_t)[0]
        state = f"{ent} is {'an' if tsg[0] in 'aeiou' else 'a'} {tsg}.\n" + rec_t
        row = {"qtype": "noul", "card": ctext, "state": state, "instructions": q, "options": None}
        out = SB.solve_row(row)
        printed = 1 if e["answer"] == "Yes" else 0
        res["examples"] += 1
        res["answers"][e["answer"]] += 1
        if out["answer"] == printed:
            res["agree"] += 1
        else:
            res["mismatch"].append({"card": cid, "form": ck["form"], "solver_a_label": ck["label"],
                                    "solver_b_labels": out["labels"]})
res["templates"] = dict(res["templates"])
res["answers"] = dict(res["answers"])
res["pass"] = (res["examples"] > 0 and res["agree"] == res["examples"] and
               res["few_shot_cards_rendered"] == res["few_shot_cards_planned"])
json.dump(res, open(F4 / "qc" / f"fewshot_{NAME}.json", "w"), indent=1)
print(json.dumps(res))
