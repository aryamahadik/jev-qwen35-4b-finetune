"""Repair r2: assemble qc/QC_REPORT.json after the F5 repair (counts and verdicts only, no row texts). The checker's
gate scripts in qc/ were re-run unchanged on the regenerated sets; the checker's r1 report is kept as
qc/QC_REPORT_r1_checker.json. Generator-side gates (G2 solver B, G3, G4, sealed_check) are read from out/ and solverB/."""
import json
import qc_lib as L

F5 = L.QC.parent
J = lambda p: json.load(open(p)) if p.exists() else None
q = lambda f: J(L.QC / f)
o = lambda f: J(F5 / "out" / f)
g5a, g5b = q("QC_REPORT_r1_checker.json")["gates"]["G5"], q("g5_r2.json")
g6, g7c, g7q, g8, g8c = q("g6_qc_sample.json"), q("g7_candidates_r1.json"), q("g7_qc_sample.json"), q("g8_candidates_r1.json"), q("g8_control_candidates_r1.json")
g10, g10q, g11, g12 = q("g10_candidates_r1.json"), q("g10_qc_sample.json"), q("g11_candidates_r1.json"), q("g12_candidates_r1.json")
g15c, g15q = q("g15_g18_candidates_r1.json"), q("g15_g18_qc_sample.json")
sb = J(F5 / "solverB" / "mismatch.json")
sealed = o("sealed_check_summary.json")
absent = J(F5 / "tmp" / "r2" / "absent_entity_scan.json")
gates = {}
gates["G2"] = {"pass": sb["n_mismatch"] == 0 and sb["n_undetermined"] == 0 and sb["n_unparsed"] == 0,
               "rows_checked": sb["rows_checked"], "agree": sb["agree"], "mismatch": sb["n_mismatch"],
               "undetermined": sb["n_undetermined"], "unparsed": sb["n_unparsed"], "by_sampler": sb["by_sampler"],
               "file": "solverB/mismatch.json"}
g3 = {s: o(f"{s}.gates.json") for s in ("candidates_r1", "qc_sample", "mixdev_S5")}
gates["G3"] = {"pass": all(v["G3"]["pass"] for v in g3.values()), "rows_ok": {s: v["G3"]["rows_ok"] for s, v in g3.items()},
               "files": [f"out/{s}.gates.json" for s in g3]}
g4 = {s: o(f"{s}.G4.json") for s in ("candidates_r1", "qc_sample", "mixdev_S5")}
g4_rows = {}
for s in ("candidates_r1", "qc_sample"):
    for k, v in g4[s]["counts"].items():
        if k.endswith(":rows"):
            g4_rows[k[:-5]] = g4_rows.get(k[:-5], 0) + v
gates["G4"] = {"pass": all(not [k for k in v["counts"] if "fail" in k] and not v["errors"] for v in g4.values())
               and min(g4_rows.values()) >= 1000, "rows_per_sampler_candidates_plus_qc": g4_rows,
               "fails": {s: [k for k in v["counts"] if "fail" in k] for s, v in g4.items()},
               "files": [f"out/{s}.G4.json" for s in g4]}
gates["G5"] = {"pass": g5b["pass"],
               "r1_flags_verified": {"read": 600, "ambiguous": g5a["ambiguous"], "clearly_wrong": g5a["clearly_wrong"],
                                     "verdict": "confirmed generator bug (SEM-02 / F5-R1-04: question named an entity "
                                     "the complete record no longer named after an S3 'remove fact' contrast edit); "
                                     "labels agreed with solver B; fixed in s3.perturb and regenerated",
                                     "pool_rows_after_fix": {k: v["absent_entity_rows"] for k, v in absent.items()}},
               "r2_fresh_sample": {"seed": 5002, "read": g5b["n_answered"], "agree": g5b["agree_with_gold"],
                                   "reader_errors_gold_right": g5b["n_reader_error"], "clearly_wrong": g5b["n_clearly_wrong"],
                                   "ambiguous": g5b["n_ambiguous"], "cosmetic_notes": len(g5b["cosmetic_notes"]),
                                   "reader": "repair builder (disclosed; not an independent session)"},
               "files": ["qc/g5_r2.json", "qc/QC_REPORT_r1_checker.json"]}
if g6 and "pass" in g6:
    gates["G6"] = {"pass": g6["pass"], "set": "qc_sample", "bar": 0.52, "max_gated_grouped_by_card": g6.get("max_gated"),
                   "gated": g6["gated"], "file": "qc/g6_qc_sample.json"}
else:
    gates["G6"] = {"pass": None, "status": "not finished"}
gates["G7"] = {"pass": bool(g7c["pass"] and g7q["pass"]), "features_tested": [g7c["features_tested"], g7q["features_tested"]],
               "fails": [g7c["n_fail"], g7q["n_fail"]], "fails_at_50k": [g7c["n_fail_at_50k_denominator"], g7q["n_fail_at_50k_denominator"]],
               "card_adjusted_fails_report_only": [g7c["card_adjusted"]["n_fail"], g7q["card_adjusted"]["n_fail"]],
               "near_within_100x": [g7c["n_near_within_100x"], g7q["n_near_within_100x"]],
               "files": ["qc/g7_candidates_r1.json", "qc/g7_qc_sample.json"]}
gates["G8"] = {"pass": g8["pass"], "gated": "grouped by card", "bar": "< 0.10", "grouped_share": g8["grouped"]["predictable_share"],
               "grouped_mean_heldout_acc": g8["grouped"]["mean_heldout_acc"], "instance_share_info": g8["instance"]["predictable_share"],
               "label_permuted_controls_grouped": {k: v for k, v in (g8c or {}).items() if k.startswith("grouped")},
               "note": "real grouped share is below every label-permuted control and the mean held-out accuracy is below chance; "
                       "the < 10% bar is not reachable at this design even with shuffled labels: orchestrator ruling needed",
               "files": ["qc/g8_candidates_r1.json", "qc/g8_control_candidates_r1.json"]}
gates["G10"] = {"pass": bool(g10["pass"] and (g10q or {}).get("pass", True)), "fails": g10["fails"],
                "fails_qc_sample": (g10q or {}).get("fails"),
                "contrast_set_share": g10["A_quotas"]["contrast_set_share"]["v"],
                "wording_bin_kall_cells": [g10["B_wording_bin_kall"]["n_cells"], g10["B_wording_bin_kall"]["n_fail_raw"]],
                "note": "difficulty bins unscored until G9 (crowd on the free L4)", "files": ["qc/g10_candidates_r1.json", "qc/g10_qc_sample.json"]}
gates["G11"] = {"pass": g11["pass"], "counts": g11["counts"], "frame_x_template_max_share": g11["two_pct"]["frame_x_template"]["max_share"],
                "question_skeleton_max_share": g11["two_pct"]["question_skeleton"]["max_share"],
                "wording_max_rouge_l": g11["seeds_rouge_l"]["wordings"]["max_rouge_l"], "metrics": g11["metrics"], "file": "qc/g11_candidates_r1.json"}
gates["G12"] = {"pass": g12["pass"], "exact_dups": [g12["exact_dup_model_view"], g12["exact_dup_raw_fields"]],
                "minhash_non_twin_pairs": g12["minhash_question_plus_record"]["non_twin_pairs"],
                "structure_dups": [g12["structure_hash_generator"]["hashes_spanning_bases"], g12["structure_hash_independent"]["keys_spanning_non_twin_bases"]],
                "file": "qc/g12_candidates_r1.json"}
gates["G15"] = {"pass": bool(g15c["G15_pass"] and g15q["G15_pass"]), "loader_check_fail": [g15c["loader_check_fail"], g15q["loader_check_fail"]],
                "roundtrip_fail": [g15c["roundtrip_gold_fail"], g15q["roundtrip_gold_fail"]],
                "max_tokens_full_chat": [g15c["tokens_full_chat_prompt"]["max"], g15q["tokens_full_chat_prompt"]["max"]],
                "builder_G15_max_served": {s: v["G15"]["served_tokens"]["max"] for s, v in g3.items()},
                "files": ["qc/g15_g18_candidates_r1.json", "qc/g15_g18_qc_sample.json"]}
gates["G18"] = {"pass": bool(g15c["G18"]["pass"] and g15q["G18"]["pass"]), "applies": False, "ordinal_rows": 0}
gates["sealed_check"] = {"pass": all(len(v.get("blocking_hits", [])) == 0 for v in sealed.values()),
                         "blocking": {k: len(v.get("blocking_hits", [])) for k, v in sealed.items()},
                         "file": "out/sealed_check_summary.json"}
failed = [g for g, v in gates.items() if v.get("pass") is not True]
rows = {s: v["G3"]["rows"] for s, v in g3.items()}
rep = {"family": "F5", "round": "repair r2 (after checker r1 FAIL G7/G8/G10 + G5 absent-entity flag)",
       "role": "repair builder; the independent checker's gate scripts (qc/*.py) re-run unchanged on the regenerated sets",
       "set": f"out/candidates_r1.jsonl ({rows['candidates_r1']:,} rows); G6 on out/qc_sample.jsonl ({rows['qc_sample']:,} rows); "
              f"mixdev_S5 {rows['mixdev_S5']} rows",
       "gates": gates, "failed_gates": failed,
       "checker_r1_problems": {
           "1_template_gold_S3_C8": "fixed by construction (mirrored V template class + mirrored question draws); G7 0 fails",
           "2_selection_cap_wording_SEM24_contrast": "G7 per-card cap applied on the pool; wording and SEM-24 balanced by "
                                                     "construction; contrast share 22.4%",
           "3_absent_entity_twins": "fixed in s3.perturb; 0 rows in every set",
           "4_G8_bar": "still FAIL as specified (see G8 note); orchestrator ruling needed"},
       "previous_report": "qc/QC_REPORT_r1_checker.json", "deviations": "tmp/deviations.json (repair_r2)",
       "pass": not failed}
json.dump(rep, open(L.QC / "QC_REPORT.json", "w"), indent=1)
print(json.dumps({"pass": rep["pass"], "failed": failed}))
