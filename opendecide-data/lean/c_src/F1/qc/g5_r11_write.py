"""Write qc/g5_r11.json: fresh 300-row blind read (seed 5002) after the r1.1 repair. Counts only."""
import json, collections
import qc_lib as q
rows, side = q.load("candidates_r1")
by = {r["id"]: r for r in rows}
ids = json.load(open(q.QC / "g5_r11_sample_ids.json"))
p7 = json.load(open(q.TMP / "g5_r11_p7_idx.json"))
sc = json.loads(__import__("subprocess").check_output([__import__("sys").executable, "g5_r11_score.py"], cwd=q.QC))
c = lambda f: dict(collections.Counter(str(side.get(x, {}).get(f)) for x in ids))
out = {"gate": "G5 (fresh blind read, r1.1)", "file": "out/candidates_r1.jsonl", "seed": 5002, "sample_n": 300,
       "sample_ids": "qc/g5_r11_sample_ids.json", "method": "checker read only the model view (decoder_io cygnet + schema_branch_mark), solved each row by hand from the card, then compared with gold",
       "answered": sc["answered"], "agree_with_gold": sc["agree"], "disagree": sc["disagree"], "clearly_wrong": len(sc["disagree"]),
       "ambiguous": 0, "pass": sc["agree"] == 300,
       "regeneration_note": f"the sample was drawn on the pass-3 file; cards regenerated later (pass 4: 17 Q2 cards; pass 5b/6: the same 17 Q2 cards, the S2 missing-field Q3 cards F1-C035 and F1-C076, 7 Q3 cards with swapped y; pass 7: the 17 Q2 cards again) had their sampled rows replaced by a seed-5002 draw from their new rows and read blind after each pass; after pass 7, {len(p7)} rows were redrawn from the 17 Q2 cards and read blind; the other {300 - len(p7)} rows were checked byte-identical (model-view hash and gold) to rows already read blind",
       "by_qtype": c("qtype"), "by_world": c("world"), "by_policy": c("policy"),
       "planted_text_lines_in_case_files": "treated as data; none changed an answer"}
(q.QC / "g5_r11.json").write_text(json.dumps(out, indent=1))
print(json.dumps({k: out[k] for k in ("answered", "agree_with_gold", "clearly_wrong", "pass", "by_qtype", "by_world")}))
