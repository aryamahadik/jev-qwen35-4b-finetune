"""Assemble qc/QC_REPORT.json from the independent F2 checker's gate outputs (counts only, no row text)."""
import json, hashlib
from scipy.stats import binomtest
import qc_lib as L
Q = L.QC
def J(n): return json.loads((Q / n).read_text())
g5, g6, g7q, g7c, g8, g8c, g8s, g10, g10q, g11, g12, g15, g18 = (J(n) for n in (
    "g5.json", "g6.json", "g7_qc_sample.json", "g7_candidates_r1.json", "g8_candidates_r1.json", "g8_control_candidates_r1.json",
    "g8_sweep_candidates_r1.json", "g10_candidates_r1.json", "g10_qc_sample.json", "g11_candidates_r1.json", "g12_candidates_r1.json",
    "g15_candidates_r1.json", "g18.json"))
yn_d = g6["yes_no"]["d_metadata"]; p_yn = binomtest(round(yn_d["best"] * 2269), 2269, 0.5, alternative="greater").pvalue
ch_d = g6["choice"]["d_metadata"]
gates = {
 "G5": {"pass": g5["pass"], "n": g5["sample"]["n"], "reader_agrees_with_gold": g5["reader_vs_gold"]["agree"],
        "clearly_wrong": g5["n_clearly_wrong"], "ambiguous": g5["n_ambiguous"],
        "wording_notes_label_determinable": {"rows": g5["wording_notes_label_determinable"]["n_rows"],
                                             "by_kind": g5["wording_notes_label_determinable"]["by_kind"],
                                             "cards": g5["wording_notes_label_determinable"]["cards_by_kind"]}, "file": "qc/g5.json"},
 "G6": {"pass": g6["pass"], "file": "qc/g6.json", "sample": "out/qc_sample.jsonl (5,048 rows; 0 structure-hash overlap with candidates)",
        "fails": {"choice_d_metadata": {"best_acc": round(ch_d["best"], 4), "bar": round(ch_d["chance_mean_1_over_k"] + .02, 4),
                                        "bucket_2-4": ch_d["per_bucket_fails"]},
                  "yes_no_d_metadata": {"best_acc": round(yn_d["best"], 4), "bar": 0.52, "one_sided_binomial_p_vs_0.5": round(float(p_yn), 4),
                                        "note": "literal fail by 0.05 pp; not significant at 0.01"}},
        "passes": "yes/no (a) question 50.1, (c) card w/o question 49.8; choice (a) 25.1, (b) options 26.2, (c) 26.1 vs chance 27.7"},
 "G7": {"pass": g7q["pass"] and g7c["pass"], "file": "qc/g7_qc_sample.json, qc/g7_candidates_r1.json",
        "qc_sample": {k: g7q[k] for k in ("n_tests", "n_fail", "n_fail_multi_card", "n_fail_single_card")},
        "candidates_r1": {k: g7c[k] for k in ("n_tests", "n_fail", "n_fail_multi_card", "n_fail_single_card")},
        "yes_no_fails": sum(f["part"] == "yes_no" for f in g7q["fails"]) + sum(f["part"] == "yes_no" for f in g7c["fails"]),
        "main_cue": "choice rows with value/date options: gold is an inner value far above 1/k and the smallest / largest value far below (qc_sample 'rank:val_inner' 206 gold vs 150.5 expected over 377 rows, 11 cards; candidates 'rank:val_first' under in 7+ cards); also top band 'Class 5B' rarely gold (1 card) and abstain over-gold on flip-variant rows (var:1, 14 cards)"},
 "G8": {"pass": g8["pass"], "file": "qc/g8_candidates_r1.json (+ g8_control, g8_sweep)",
        "grouped_by_card_predictable_share": round(g8["grouped_by_card"]["predictable_share"], 4),
        "yes_no_share": round(g8["grouped_by_card"]["yes_no_share"], 4), "choice_share": round(g8["grouped_by_card"]["choice_share"], 4),
        "instance_level_share": round(g8["instance_level"]["predictable_share"], 4),
        "permuted_label_control_shares": {k: round(v["predictable_share"], 4) for k, v in g8c.items()},
        "control_choice_share": round(g8c["seed_4242"]["choice_share"], 4),
        "C_sweep_real_vs_control": {c: [round(v["real"]["predictable_share"], 4), round(v["control"]["predictable_share"], 4)] for c, v in g8s.items()},
        "note": "literal rule (< 10%) fails; the permuted-label floor of this procedure is ~14.6% (> the 10% bar at every C tried), so the bar cannot be met even by cue-free labels as specified: method item for the orchestrator. Real excess over the floor is ~3.4 pp, mostly on choice rows (10.5% vs 6.4-6.8% control), consistent with the G7/G10 rank cue"},
 "G10": {"pass": g10["pass"], "file": "qc/g10_candidates_r1.json (+ g10_qc_sample.json)", "n_checks": g10["n_checks"], "n_fail": g10["n_fail"],
         "failed": g10["failed"], "qc_sample_failed": g10q["failed"],
         "key_values": {c["check"]: c["value"] for c in g10["checks"] if not c["pass"]},
         "selection_time_not_gated": [c["check"] for c in g10["checks"] if c.get("selection_time")],
         "pending": "difficulty-bin targets and per-bin cells after G9 crowd scoring"},
 "G11": {"pass": g11["pass"], "file": "qc/g11_candidates_r1.json", **{k: g11[k] for k in ("counts", "surface_template", "claude_seeds_rouge_l", "corpus_metrics", "pass_parts")}},
 "G12": {"pass": g12["pass"], "file": "qc/g12_candidates_r1.json", **{k: g12[k] for k in ("exact_duplicates", "near_dup_pairs_ge_0.9", "near_dup_pairs_unplanned", "structure_groups_multi", "structure_groups_not_one_twin_set", "structure_overlap_with")}},
 "G15": {"pass": g15["pass"], "file": "qc/g15_candidates_r1.json", **{k: g15[k] for k in ("rows", "check_rows_ok", "loader_check_fail", "round_trip_fail", "units", "max_unit_rows", "units_gt3", "long_units_gt2", "rows_gt_7900", "tokens_max", "tokens_median", "rows_ge_2000")}},
 "G18": {"pass": g18["pass"], "file": "qc/g18.json", "applicable": False, **{k: g18[k] for k in ("option_level_rows_candidates_r1", "option_level_rows_qc_sample", "option_level_rows_mixdev_S5", "side_entries", "side_bad_cover", "side_bad_reindex")},
         "note": "side file ranks only non-abstain options (305 entries on rows that also show NEI / None); if band rows are ever ruled ordinal, abstain options need a rule"},
}
extra = {"case_list_raw_extreme_heuristic": {
    "what": "inverted case-list choice rows (edge 'cases:<n>'): pick the case whose first numeric field in its table line is the largest (question 'above / at least ...') or smallest ('below / at most ...'), no rules applied",
    "rows_tested": 757, "heuristic_correct": 448, "expected_by_chance": 103.5, "rate_pct": 59.2, "chance_pct": 13.7,
    "note": "diagnostic partial-input baseline (state + question); not one of the four spec views, reported because it is a large model-visible shortcut; consistent with G10 'dec:x' rates far below 50% on CL rows"}}
fails = [g for g, v in gates.items() if not v["pass"]]
out = {"family": "F2", "checker": "independent F2 QC checker (never wrote F2's generator or solvers); flag-only; no label or row edited",
       "inputs": {"candidates": "out/candidates_r1.jsonl (4,739 rows)", "qc_sample": "out/qc_sample.jsonl (5,048 rows)",
                  "spec": "C_DATA_SPEC v4 (2.1, 2.2 F2, 2.4, 6, 8, 10); C_TRAIN_RECIPE v4; PREREG A15, A16, A16.1; F2 G0_SPEC v7 incl. XF"},
       "gates": gates, "extra_diagnostics": extra,
       "g5_bar": {"clearly_wrong": 0, "ambiguous_le": 3, "met": g5["n_clearly_wrong"] == 0 and g5["n_ambiguous"] <= 3},
       "failed_gates": fails,
       "not_run_here": {"G9": "crowd scoring on free L4 (orchestrator)", "G11 golden_train comparison": "golden_train outside allow-list",
                        "G13": "orchestrator decontamination", "G10 bin-level": "after G9"},
       "pass": g5["n_clearly_wrong"] == 0 and g5["n_ambiguous"] <= 3 and not fails,
       "scripts": "qc/qc_lib.py, g6.py, g7.py, g8.py, g8_control.py, g8_sweep.py, g10.py, g11.py, g12.py, g15.py, g18.py, build_report.py; G5 renderer tmp/qc_checker/g5_render.py, answers qc/tmp/g5_answers.tsv"}
(Q / "QC_REPORT.json").write_text(json.dumps(out, indent=1, default=str))
print("pass", out["pass"], "failed", fails)
