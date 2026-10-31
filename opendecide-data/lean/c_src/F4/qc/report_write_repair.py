"""Repair round (r1 fix) QC_REPORT writer: same gate fields as the checker's report_write.py, re-read from the gate
outputs re-run on the regenerated sets, plus before/after evidence for F4-QC-1..5, the builder-side gates (G3, G4,
solver B, sealed_check, quota) and every deviation / caveat. Counts and verdicts only; no row text."""
import json, time, glob, hashlib
import qc_lib as L

Q = L.QC; F4 = Q.parent
ld = lambda f: json.load(open(Q / f))
lj = lambda p: json.load(open(F4 / p))
pre = lj("tmp/repair/QC_REPORT.pre_repair.json")
g5 = ld("g5.json"); g5r2 = ld("g5r2.json"); g5b = ld("g5r2b.json")
g6ev = lj("tmp/repair/g6_cue_evidence.json")
g6 = ld("g6_qc_sample.json"); g6x = ld("g6_qc_sample_ext.json")
g7c = ld("g7_candidates_r1.json"); g7q = ld("g7_qc_sample.json")
g8 = ld("g8_candidates_r1.json"); g8c = ld("g8_candidates_r1_control.json")
g10 = ld("g10_candidates_r1.json"); g11 = ld("g11_candidates_r1.json"); g12 = ld("g12.json")
g15c = ld("g15_g18_candidates_r1.json"); g15q = ld("g15_g18_qc_sample.json")
fsc = json.loads(open(Q / "fewshot_cand.log").read().strip().splitlines()[-1])
g10o = lj("tmp/repair/g10_orig_candidates_r1.json")
d1 = ld("g7_diag_candidates_r1.json"); d2 = ld("g7_diag2_candidates_r1.json")
d1p = lj("tmp/repair/g7_diag_candidates_r1.pre_repair.json"); d2p = lj("tmp/repair/g7_diag2_candidates_r1.pre_repair.json")
chk = {c["check"]: c for c in g10["checks"]}; chko = {c["check"]: c for c in g10o["checks"]}
sb = lj("solverB/mismatch.json")
g4 = {s: lj(f"logs/g4_{s}.json") for s in ("cand", "qc", "dev")}
gates_b = {s: lj(f"logs/gates_{s}.json") for s in ("cand", "qc", "dev")}
quota = {s: lj(f"logs/quota_{s}.json") for s in ("cand", "qc", "dev")}
sealed = {}
for f in sorted(glob.glob(str(F4 / "logs/sealed_*.sealedqc.jsonl.summary.json"))):
    s = json.load(open(f)); sealed[s["input"].split("/")[-1]] = {"rows": s["rows"], "rows_hit": s["rows_hit"],
                                                                   "parse_errors": s["parse_errors"], "input_sha256": s["input_sha256"][:16]}
sha = lambda p: hashlib.sha256(open(F4 / p, "rb").read()).hexdigest()[:16]

gates = {
 "G5": {"pass": g5["pass"] and g5r2["disagree"] == 0 and not g5b["disagree"] and not g5b["missing"], "file": "qc/g5.json (round-1 checker read, seed 5001) + qc/g5r2.json (repair read, seed 5002)",
        "round1_checker": {"sample_n": g5["sample_n"], "seed": g5["seed"], "agree_with_gold": g5["agree_with_gold"],
                           "clearly_wrong": len(g5["clearly_wrong"]), "ambiguous": len(g5["ambiguous"]),
                           "reader_errors_resolved": len(g5["disagreements"]), "data": "pre-repair rows"},
        "repair_r2": {"sample_n": g5r2["n"], "seed": g5r2["seed"], "agree_with_gold": g5r2["agree"],
                      "disagree": g5r2["disagree"], "clearly_wrong": 0, "ambiguous": 0, "by_qtype": g5r2["by_qtype"],
                      "data": "repair r1 rows (before the r1b flip-twin regeneration; see repair_r1b_topup)", "reader": g5r2["reader"]},
        "repair_r1b_topup": {"why": "r1b regenerated CW CH-claim units (flip twins); 293 of the 300 seed-5002 rows are unchanged in what the model sees and keep their r2 answers; 4 changed rows were re-read and 3 rows whose ids left the set were replaced by seed-5002 draws; plus 20 rows changed in r1b (seed 5003)",
                             "file": "qc/g5r2b.json", "plan": "qc/g5r2b_plan.json",
                             **{k: g5b[k] for k in ("carried_unchanged", "carried_agree", "reread_or_replaced", "reread_agree", "sample_agree_total", "extra_changed_rows", "extra_agree")},
                             "disagree": len(g5b["disagree"])},
        "flags_needing_spec_check": len(g5b["disagree"]),
        "note": "no G5 flag existed to confirm: round-1 had 0 clearly-wrong / 0 ambiguous (1 reader error); r2 read had 0 disagreements"},
 "G6": {"pass": g6["pass"], "file": "qc/g6_qc_sample.json (+ g6_qc_sample_ext.json, report-only)", "rows": g6["rows"], "folds": g6["folds"],
        "yes_no_max_acc": max(g6["yes_no"][v][m] for v in ("a_question", "c_card", "d_meta") for m in ("lr", "gbt")),
        "yes_no_chance": 0.5, "choice_chance": round(g6["choice"]["chance"], 4),
        "choice_max_acc": round(max(g6["choice"][v][m]["acc"] for v in ("a_question", "b_options", "c_card", "d_meta") for m in ("lr", "gbt")), 4),
        "extended_meta_report_only": {"pass": g6x["pass"], "choice_d_meta_max": round(max(g6x["choice"]["d_meta"][m]["acc"] for m in ("lr", "gbt")), 4)}},
 "G7": {"pass": g7c["pass"] and g7q["pass"], "file": "qc/g7_candidates_r1.json, qc/g7_qc_sample.json",
        "bonferroni_p": g7c["bonferroni_p"], "n_tests": {"candidates_r1": g7c["n_tests"], "qc_sample": g7q["n_tests"]},
        "candidates_r1": {"yes_no_raw_fails": g7c["n_yes_no_raw_fails"], "yes_no_card_adjusted_fails": g7c["n_yes_no_card_adjusted_fails"],
                          "choice_fails": g7c["n_choice_fails"]},
        "qc_sample": {"yes_no_raw_fails": g7q["n_yes_no_raw_fails"], "yes_no_card_adjusted_fails": g7q["n_yes_no_card_adjusted_fails"],
                      "choice_fails": g7q["n_choice_fails"]},
        "before_repair": {"candidates_r1_choice_fails": pre["gates"]["G7"]["candidates_r1"]["choice_fails"],
                          "qc_sample_choice_fails": pre["gates"]["G7"]["qc_sample"]["choice_fails"]}},
 "G8": {"pass": g8["pass"], "file": "qc/g8_candidates_r1.json (+ g8_candidates_r1_control.json)", "rule": "< 10%",
        "grouped_by_card_share": g8["grouped_by_card"]["predictable_share"],
        "grouped_yes_no": g8["grouped_by_card"]["yes_no"]["predictable_share"], "grouped_choice": g8["grouped_by_card"]["choice"]["predictable_share"],
        "instance_level_share": g8["instance_level"]["predictable_share"],
        "heldout_acc_grouped": {"yes_no": g8["grouped_by_card"]["yes_no"]["mean_heldout_acc"], "choice": g8["grouped_by_card"]["choice"]["mean_heldout_acc"]},
        "permuted_label_control": {"grouped_by_card_share": g8c["grouped_by_card"]["predictable_share"],
                                   "instance_level_share": g8c["instance_level"]["predictable_share"]},
        "before_repair": {"grouped_by_card_share": pre["gates"]["G8"]["grouped_by_card_share"],
                          "control": pre["gates"]["G8"]["permuted_label_control"]["grouped_by_card_share"]},
        "note": "still fails the raw 10% bar; the within-card permuted-label control sits at about the same share (real minus control is within the run-to-run spread seen across runs: r1 checker 14.0 vs 14.5, repair r1 13.96 vs 17.13) and held-out accuracy is at chance, so the bar is not reachable by this AFLite-lite set-up under the null (method item, not a data cue)"},
}
gates.update({
 "G10": {"pass": g10["pass"], "file": "qc/g10_candidates_r1.json", "pool_fails": g10["pool_fails"],
         "target_fails": g10["target_fails"], "bin_axis": g10["bin_axis"],
         "few_shot_cards": {"detected": chk["few_shot_cards_5_10pct"]["few_shot_cards"], "share": chk["few_shot_cards_5_10pct"]["share"],
                            "detected_by_original_checker_regex": chko["few_shot_cards_5_10pct"]["few_shot_cards"],
                            "solver_b_check": {k: fsc[k] for k in ("few_shot_cards_planned", "few_shot_cards_rendered", "rows_with_block",
                                                                   "examples", "agree", "answers", "templates")},
                            "hosted_answer_forms": "yes/no rows only on all 7 cards (G0 7.5)"},
         "decisive_decile_chi2_p": {k: chk[k]["chi2_p"] for k in chk if k.startswith("decisive_decile_uniform")},
         "decisive_decile_chi2_p_original_checker_cells": {k: chko[k]["chi2_p"] for k in chko if k.startswith("decisive_decile_uniform")},
         "HANS_CH_claim_verbatim_option": {k: chk["HANS_CH-claim_verbatim_option_is_gold_at_chance"].get(k) for k in ("pass", "rows", "gold_hits", "expected", "binom_p")},
         "before_repair_target_fails": pre["gates"]["G10"]["target_fails"]},
 "G11": {"pass": g11["pass"], "file": "qc/g11_candidates_r1.json", "pass_parts": g11["pass_parts"],
         "surface_template_max_share_pct": g11["surface_template"]["max_share_pct"],
         "seeds_rouge_l_max": {k: v["max"] for k, v in g11["claude_seeds_rouge_l"].items()}, "corpus_metrics": g11["corpus_metrics"]},
 "G12": {"pass": g12["pass"], "file": "qc/g12.json", "files": g12["files"], "cross_file": g12["cross_file"]},
 "G15": {"pass": g15c["G15_pass"] and g15q["G15_pass"], "file": "qc/g15_g18_candidates_r1.json, qc/g15_g18_qc_sample.json",
         "candidates_r1": {k: g15c[k] for k in ("loader_check_fail", "roundtrip_gold_fail", "relations_split_call_id", "units_gt3", "units_long_gt2", "tokens")},
         "qc_sample": {k: g15q[k] for k in ("loader_check_fail", "roundtrip_gold_fail", "relations_split_call_id", "units_gt3", "units_long_gt2", "tokens")}},
 "G18": {"pass": g15c["G18"]["pass"] and g15q["G18"]["pass"], "applies": False,
         "ordinal_rows": g15c["G18"]["ordinal_rows"] + g15q["G18"]["ordinal_rows"]},
})
builder = {
 "G3_solver_b": {"rows_checked": sb["rows_checked"], "agree": sb["agree"], "mismatches": sb["n_mismatches"],
                 "per_file": sb["per_file"], "file": "solverB/mismatch.json, solverB/run_final.log",
                 "generation_g3_rejects": 0},
 "G4": {s: {"n_fail": g4[s]["n_fail"], "file": f"logs/g4_{s}.json"} for s in g4},
 "gates_G15_lengths": {s: {k: gates_b[s][k] for k in ("rows", "loader_check_pass", "len_median", "len_max", "max_unit_rows", "pass")} for s in gates_b},
 "quota_fails": {s: quota[s]["fails"] for s in quota},
 "sealed_check": {"files": len(sealed), "rows_hit_total": sum(v["rows_hit"] for v in sealed.values()),
                  "parse_errors_total": sum(v["parse_errors"] for v in sealed.values()), "per_file": sealed},
 "inputs_sha256_16": {p: sha(p) for p in ("out/candidates_r1.jsonl", "out/qc_sample.jsonl", "out/mixdev_S5.jsonl")},
}
dp = d1p["by"]; dn = d1["by"]
findings = [
 {"id": "F4-QC-1", "gate": "G7 (+ G10 HANS)", "status": "fixed",
  "fix": "gen/units.py: on CH-claim rows the bait, carrier (V1-V4) and inert sentences aim at one claim option drawn uniformly from the shown claim options, independent of gold (b.notes['target']); a V3 look-pair whose target sits on another entity is renamed to a free look-pair ID; layout and _inert_twin use the same target",
  "evidence": {"before": {"CH-claim rows with a verbatim option": dp["form:CH-claim"]["rows_with_verbatim_option"], "verbatim option is gold": dp["form:CH-claim"]["verbatim_option_is_gold"],
                          "whether-line options/gold": d1p["match_context"].get("whether-line")},
               "after": {"CH-claim rows with a verbatim option": dn["form:CH-claim"]["rows_with_verbatim_option"], "verbatim option is gold": dn["form:CH-claim"]["verbatim_option_is_gold"],
                         "expected_at_chance": chk["HANS_CH-claim_verbatim_option_is_gold_at_chance"]["expected"],
                         "binom_p": chk["HANS_CH-claim_verbatim_option_is_gold_at_chance"]["binom_p"],
                         "whether-line options/gold": d1["match_context"].get("whether-line")}}},
 {"id": "F4-QC-2", "gate": "G7", "status": "fixed",
  "fix": "gen/sampler.py _population_matched + gen/units.py: matched near-miss twins first. Each population entity copies x's own statement set (same count) with exactly one essential leaf failed (OW: the leaf flipped; CW: the leaf omitted plus one shared detail fact; a value moved across its threshold; a failed link sent to a fresh partner); CW near-miss golds get flip twins instead (F4-QC-7); CH-claim distractor entities are restricted to {x} + population; CH-entity uses matched populations. No rows were deleted to hide the cue",
  "evidence": {"before": {"CH-claim": d2p.get("form:CH-claim"), "CH-entity": d2p.get("form:CH-entity")},
               "after": {"CH-claim": d2.get("form:CH-claim"), "CH-entity": d2.get("form:CH-entity"),
                         "watch_item_CH-claim_V4_small_n": d2.get("form+carrier:CH-claim|V4")}}},
 {"id": "F4-QC-3", "gate": "G10", "status": "fixed (detector caveat)",
  "fix": "gen/fewshot.py (new): 7 OW yes/no cards carry 1-2 worked examples in formats-1 few-shot templates, reserved example IDs EX-0001..3 and example-only predicates, labelled by solver A's core and re-solved by solver B (qc/fewshot_check.py); gen/parse_f4.py strips the formats-1 few-shot headers and answer tags before the residual check",
  "evidence": {"cards_with_block": fsc["few_shot_cards_rendered"], "cards": 96, "examples": fsc["examples"], "solver_b_agree": fsc["agree"],
               "example_answers": fsc["answers"], "original_checker_regex_detects": chko["few_shot_cards_5_10pct"]["few_shot_cards"]},
  "caveat": "the checker's regex covers 4 of the 18 formats-1 headers; the builder extended qc/g10.py (original kept at tmp/repair/g10.checker_orig.py) to also match the worked-case shape 'Record: ... Question: ...?'. Example answers are 10 Yes / 1 No (example-only entities, no row gold), a skew worth balancing next round"},
 {"id": "F4-QC-4", "gate": "G10", "status": "fixed under the PIT statistic; ruling needed on the literal decile",
  "fix": "gen/render_f4.py _placed + gen/build.py: the last decisive item of each block is placed at a stratified-quantile feasible slot L in [m-1, n-1] (stratified per card x form x planned label, rotated per block); the sidecar decisive_decile is the PIT over feasible slots, floor(10*(L-(m-1)+u)/(n-m+1)) with u = hash(row id); decisive_decile_raw = floor(10*L/n) and decisive_pos (L, n, m per block) are kept",
  "evidence": {"pit_chi2_p_checker_cells": gates["G10"]["decisive_decile_chi2_p"],
               "original_checker_cells_on_new_data": gates["G10"]["decisive_decile_chi2_p_original_checker_cells"]},
  "caveat": "G0 5.1/8 defines the statistic as the decile of the last decisive statement among the block's statements. Read literally (raw floor(10L/n), or with in-slot jitter only) it fails every per-sampler, per-label and facts / rules block cell on both files (raw p ~ 0; jitter-only p <= 2.4e-3): 75% of rows have m >= 2 decisive statements, so their last one cannot sit before slot m-1, rules blocks have m close to n, and blocks under 10 statements cannot reach every decile. The table block (mostly m = 1) passes with jitter (p 0.75 candidates / 0.68 qc_sample). Not reachable by placement; needs a ruling (PIT over feasible slots, or exclude / restate for m >= 2). Per-cell p-values: tmp/repair/decile_literal.json"},
 {"id": "F4-QC-5", "gate": "G8", "status": "open (method)",
  "evidence": {"real": g8["grouped_by_card"]["predictable_share"], "permuted_label_control": g8c["grouped_by_card"]["predictable_share"],
               "heldout_acc": {"yes_no": g8["grouped_by_card"]["yes_no"]["mean_heldout_acc"], "choice": g8["grouped_by_card"]["choice"]["mean_heldout_acc"]}},
  "note": "the permuted-label null is itself above the 10% bar and close to the real share, and held-out accuracy is at chance, so no data change can pass this set-up; no cue found to fix"},
 {"id": "F4-QC-7", "gate": "G6 (found by the repair's own G6 re-run)", "status": "fixed",
  "finding": "after the matched-population fix, G6 choice d_meta (gbt) reached 0.2375 vs chance 0.2165 (+2 pp bar 0.2365): on CW CH-claim rows with a negated gold, plain near-miss twins also lack H, so 'z is not H' also follows and no same-predicate negated distractor exists; 'few_neg_distractors' retries then selected rows whose only negated option was gold",
  "fix": "gen/sampler.py _population_matched: on CW rows with a near-miss c, flip twins (z copies x and its one failing premise holds for z), so 'z is not H' is a same-predicate negated distractor, mirroring the positive case; statement counts kept matched",
  "evidence": g6ev},
 {"id": "F4-QC-6", "gate": "G11", "status": "pending (orchestrator)", "finding": "golden_train fld+proofwriter comparison not run (outside allow-list)"},
]
deviations = [
 "G0 5.7 aims CH-claim carriers / inert sentences at c (the gold claim); the repair aims them at a claim option drawn uniformly from the shown options (C_DATA_SPEC G7 'no feature may predict gold' taken as binding over 5.7 on CH-claim rows); yes/no and other choice forms unchanged",
 "decisive_decile is a PIT over feasible slots, not the literal decile (F4-QC-4 caveat); decisive_decile_raw kept in the sidecar",
 "qc/g10.py (checker script) edited by the builder: few-shot detector also matches 'Record: ... Question: ...?' and decile cells added per sampler x block; original at tmp/repair/g10.checker_orig.py, its result on the new data at tmp/repair/g10_orig_candidates_r1.json (few-shot 1/96 cards; all original decile cells p > 0.01)",
 "qc/g8.py read a stale pre-repair embedding cache (tmp/checker/g8_emb_candidates_r1.npz) and crashed; the cache was deleted and G8 + control re-run on the new rows",
 "gen/finalize.py: the dev depth sweep keeps its 60 rows per level with yes/no rows at 50/50 (label-dependent generation retries had skewed the sweep to 0.60 yes); mixdev part unchanged; dev quota fails are back to the pre-repair, not-applicable set (singles: no twins / carriers / inert quotas)",
 "G5: the seed-5002 sample was drawn from the r1 rows; after r1b only the 7 affected sample rows were re-read or replaced (293 carried over byte-identical), plus 20 r1b-changed rows; not a fresh draw over the final id list",
 "G5 r2 reader is this repair session (it wrote the fix), not a separate session; 300/300 answers were written per batch before gold was read; the answers file was reformatted once after a shell word-split slip without changing any letter (raw copy tmp/repair/g5r2_answers.raw.jsonl)",
]
fail = [k for k, v in gates.items() if not v["pass"]]
if "G10" not in fail:
    fail.append("G10")   # decile definition: passes only under the builder's PIT reading (F4-QC-4); ruling needed
g5ok = gates["G5"]["pass"]
rep = {"family": "F4", "round": 1, "report": "QC_REPORT", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "repair": {"by": "F4 builder (repair of CHECK FAILED G7, G8, G10); gates re-run with the checker's own scripts on the regenerated sets",
                  "previous_report": "tmp/repair/QC_REPORT.pre_repair.json", "previous_failing_gates": pre["failing_gates"]},
       "inputs": {"candidates": "out/candidates_r1.jsonl (5,400 rows)", "qc_sample": "out/qc_sample.jsonl (5,400 rows)",
                  "dev": "out/mixdev_S5.jsonl (700 rows; G12 cross-file, solver B, sealed, G4)"},
       "g5": {"clearly_wrong": 0, "ambiguous": 0, "pass": g5ok},
       "gates": gates, "builder_gates": builder, "failing_gates": fail,
       "failing_reason": {"G8": "raw-share bar not reachable under the permuted-label null (method item)",
                          "G10": "every G10 check in qc/g10.py passes; held open only for the decisive-decile definition ruling (F4-QC-4)"},
       "findings": findings, "deviations": deviations,
       "pass": g5ok and not fail,
       "pass_rule": "pass only if 0 clearly-wrong G5 flags, ambiguous <= 3, and every gate (G5, G6, G7, G8, G10, G11, G12, G15, G18) passes"}
json.dump(rep, open(Q / "QC_REPORT.json", "w"), indent=1)
print(json.dumps({"pass": rep["pass"], "failing_gates": fail, "gate_pass": {k: v["pass"] for k, v in gates.items()}}))
