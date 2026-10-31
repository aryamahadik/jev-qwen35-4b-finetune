"""Assemble qc/QC_REPORT.json for F4 round 1 from the independent checker's gate outputs (counts and verdicts only;
no row text). pass = 0 clearly-wrong G5 flags, ambiguous <= 3, and every gate passes."""
import json, time
import qc_lib as L

Q = L.QC
ld = lambda f: json.load(open(Q / f))
g5 = ld("g5.json"); g6 = ld("g6_qc_sample.json"); g6x = ld("g6_qc_sample_ext.json")
g7c = ld("g7_candidates_r1.json"); g7q = ld("g7_qc_sample.json")
g8 = ld("g8_candidates_r1.json"); g8c = ld("g8_candidates_r1_control.json")
g10 = ld("g10_candidates_r1.json"); g11 = ld("g11_candidates_r1.json"); g12 = ld("g12.json")
g15c = ld("g15_g18_candidates_r1.json"); g15q = ld("g15_g18_qc_sample.json")
chk = {c["check"]: c for c in g10["checks"]}

gates = {
 "G5": {"pass": g5["pass"], "file": "qc/g5.json", "sample_n": g5["sample_n"], "seed": g5["seed"],
        "agree_with_gold": g5["agree_with_gold"], "clearly_wrong": len(g5["clearly_wrong"]),
        "ambiguous": len(g5["ambiguous"]), "reader_errors_resolved": len(g5["disagreements"])},
 "G6": {"pass": g6["pass"], "file": "qc/g6_qc_sample.json (+ g6_qc_sample_ext.json)", "rows": g6["rows"],
        "folds": g6["folds"],
        "yes_no_max_acc": max(g6["yes_no"][v][m] for v in ("a_question", "c_card", "d_meta") for m in ("lr", "gbt")),
        "yes_no_chance": 0.5, "choice_chance": round(g6["choice"]["chance"], 4),
        "choice_max_acc": round(max(g6["choice"][v][m]["acc"] for v in ("a_question", "b_options", "c_card", "d_meta")
                                    for m in ("lr", "gbt")), 4),
        "extended_meta_report_only": {"pass": g6x["pass"], "choice_d_meta_max": round(max(g6x["choice"]["d_meta"][m]["acc"] for m in ("lr", "gbt")), 4)},
        "note": "(d) uses the F4 G0 8 metadata list; the hidden row role / twin-set tags are not in the prompt and are not features (with them, CH-3 d_meta reached 0.41 vs 0.33: twin sets carry label structure, invisible to the model)"},
 "G7": {"pass": g7c["pass"] and g7q["pass"], "file": "qc/g7_candidates_r1.json, qc/g7_qc_sample.json",
        "bonferroni_p": g7c["bonferroni_p"], "n_tests": g7c["n_tests"],
        "candidates_r1": {"yes_no_raw_fails": g7c["n_yes_no_raw_fails"], "yes_no_card_adjusted_fails": g7c["n_yes_no_card_adjusted_fails"],
                          "choice_fails": g7c["n_choice_fails"], "choice_fails_by_option_kind": g7c["choice_fails_by_option_kind"]},
        "qc_sample": {"yes_no_raw_fails": g7q["n_yes_no_raw_fails"], "yes_no_card_adjusted_fails": g7q["n_yes_no_card_adjusted_fails"],
                      "choice_fails": g7q["n_choice_fails"], "choice_fails_by_option_kind": g7q["choice_fails_by_option_kind"]},
        "diagnostics": "qc/g7_diag_candidates_r1.json, qc/g7_diag2_candidates_r1.json"},
 "G8": {"pass": g8["pass"], "file": "qc/g8_candidates_r1.json (+ g8_candidates_r1_control.json)", "rule": "< 10%",
        "grouped_by_card_share": g8["grouped_by_card"]["predictable_share"],
        "grouped_yes_no": g8["grouped_by_card"]["yes_no"]["predictable_share"], "grouped_choice": g8["grouped_by_card"]["choice"]["predictable_share"],
        "instance_level_share": g8["instance_level"]["predictable_share"],
        "heldout_acc_grouped": {"yes_no": g8["grouped_by_card"]["yes_no"]["mean_heldout_acc"], "choice": g8["grouped_by_card"]["choice"]["mean_heldout_acc"]},
        "permuted_label_control": {"grouped_by_card_share": g8c["grouped_by_card"]["predictable_share"],
                                   "instance_level_share": g8c["instance_level"]["predictable_share"]},
        "note": "the within-card label-permutation control reaches the same share (14.5% vs 14.0%) and held-out accuracy is at chance (yes/no 0.496, choice 0.210 vs 0.215): the excess over the null is -0.5 pp, so no embedding cue was found; the gate fails only on the raw-share bar, which this AFLite-lite set-up cannot meet under the null (same pattern as F1-F3 checkers)"},
 "G10": {"pass": g10["pass"], "file": "qc/g10_candidates_r1.json", "pool_fails": g10["pool_fails"],
         "target_fails": g10["target_fails"], "bin_axis": g10["bin_axis"]},
 "G11": {"pass": g11["pass"], "file": "qc/g11_candidates_r1.json", "pass_parts": g11["pass_parts"],
         "surface_template_max_share_pct": g11["surface_template"]["max_share_pct"],
         "seeds_rouge_l_max": {k: v["max"] for k, v in g11["claude_seeds_rouge_l"].items()},
         "corpus_metrics": g11["corpus_metrics"]},
 "G12": {"pass": g12["pass"], "file": "qc/g12.json", "files": g12["files"], "cross_file": g12["cross_file"]},
 "G15": {"pass": g15c["G15_pass"] and g15q["G15_pass"], "file": "qc/g15_g18_candidates_r1.json, qc/g15_g18_qc_sample.json",
         "candidates_r1": {k: g15c[k] for k in ("loader_check_fail", "roundtrip_gold_fail", "relations_split_call_id", "units_gt3", "units_long_gt2", "tokens")},
         "qc_sample": {k: g15q[k] for k in ("loader_check_fail", "roundtrip_gold_fail", "relations_split_call_id", "units_gt3", "units_long_gt2", "tokens")},
         "prompts_read": "20 per file in tmp/checker/g15_prompts_*.txt; 300 full prompts were read in G5"},
 "G18": {"pass": g15c["G18"]["pass"] and g15q["G18"]["pass"], "applies": False, "ordinal_rows": g15c["G18"]["ordinal_rows"] + g15q["G18"]["ordinal_rows"],
         "note": "F4 has no ordinal rows (F4 G0 11); lint confirms 0 rows carry option_level"},
}

d1 = ld("g7_diag_candidates_r1.json"); d2 = ld("g7_diag2_candidates_r1.json")
fs = chk["few_shot_cards_5_10pct"]; hc = chk["HANS_CH-claim_verbatim_option_is_gold_at_chance"]
dd = {k: chk[k]["chi2_p"] for k in chk if k.startswith("decisive_decile_uniform")}
findings = [
 {"id": "F4-QC-1", "gate": "G7 (+ G10 HANS)", "severity": "blocking",
  "finding": "V2 topic line ('<label>: whether <c>') names the row's c; on CH-claim rows c is the gold option, so the option whose sentence the record repeats is gold",
  "evidence": {"CH-claim rows with an option verbatim in the record": d1["by"]["form:CH-claim"]["rows_with_verbatim_option"],
               "of which the verbatim option is gold": d1["by"]["form:CH-claim"]["verbatim_option_is_gold"],
               "expected at chance": hc["expected"], "whether-line matches": d1["match_context"].get("whether-line"),
               "carrier V2 rows": d1["by"]["carrier:V2"]},
  "fix_hint": "on CH-claim (and CH-entity) rows, aim carriers and relevant-looking inert sentences at an option drawn independently of gold (uniform over shown options, or a designated distractor at its 1/k share), then re-run G7"},
 {"id": "F4-QC-2", "gate": "G7", "severity": "blocking",
  "finding": "the gold option's entity is the most-mentioned option entity in the record (derivation facts and entity-naming inert sentences attach to c's entity)",
  "evidence": {"CH-claim": d2["form:CH-claim"], "CH-entity (rows where mention counts differ)": d2["form:CH-entity"],
               "CH-claim without carrier": d2["form+carrier:CH-claim|None"]},
  "fix_hint": "balance entity mention counts between gold and distractor options (give near-miss distractors matching fact counts / mentions; spread I3 entity mentions over options)"},
 {"id": "F4-QC-3", "gate": "G10", "severity": "target",
  "finding": "no few-shot (worked-example) block found in any rendered row (formats-1 few-shot template headers / answer lines, extra questions or 'Answer:' lines in card text); builder plan lists 7 few-shot cards",
  "evidence": {"few_shot_cards_detected": fs["few_shot_cards"], "cards": chk["inverted_cards_10_15pct"]["cards"], "target": "5-10% of cards"}},
 {"id": "F4-QC-4", "gate": "G10", "severity": "target",
  "finding": "decisive-statement position decile (builder sidecar decisive_decile) is far from uniform per sampler and per label (mass at deciles 3-6, almost none at 8-9); definition not re-derived independently",
  "evidence": {"chi2_p": dd}},
 {"id": "F4-QC-5", "gate": "G8", "severity": "bar-only",
  "finding": "AFLite-lite raw predictable share 14.0% (> 10%) equals the within-card permuted-label control (14.5%); held-out accuracy at chance, so no cue to fix",
  "evidence": {"real": g8["grouped_by_card"]["predictable_share"], "control": g8c["grouped_by_card"]["predictable_share"]}},
 {"id": "F4-QC-6", "gate": "G11", "severity": "pending",
  "finding": "compression / Self-BLEU / Vendi comparison with golden_train's fld+proofwriter slice not run (golden_train outside this checker's allow-list); orchestrator item"},
]
g5ok = len(g5["clearly_wrong"]) == 0 and len(g5["ambiguous"]) <= 3
all_ok = g5ok and all(v["pass"] for v in gates.values())
rep = {"family": "F4", "round": 1, "report": "QC_REPORT", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "checker": "independent F4 checker (did not write the F4 generator, solver A or solver B)",
       "inputs": {"candidates": "out/candidates_r1.jsonl (5,400 rows)", "qc_sample": "out/qc_sample.jsonl (5,400 rows)",
                  "dev": "out/mixdev_S5.jsonl (G12 cross-file only)"},
       "g5": {"clearly_wrong": len(g5["clearly_wrong"]), "ambiguous": len(g5["ambiguous"]), "pass": g5ok},
       "gates": gates, "failing_gates": [k for k, v in gates.items() if not v["pass"]], "findings": findings,
       "pass": all_ok,
       "pass_rule": "pass only if 0 clearly-wrong G5 flags, ambiguous <= 3, and every gate (G5, G6, G7, G8, G10, G11, G12, G15, G18) passes"}
json.dump(rep, open(Q / "QC_REPORT.json", "w"), indent=1)
print(json.dumps({"pass": all_ok, "failing_gates": rep["failing_gates"]}))
