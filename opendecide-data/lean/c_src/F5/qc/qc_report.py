"""Assemble qc/QC_REPORT.json from the independent F5 checker's gate files (counts and verdicts only, no row texts)."""
import json
import qc_lib as L

J = lambda f: json.load(open(L.QC / f)) if (L.QC / f).exists() else None
g5, g6, g7c, g7q, g8, g8c = J("g5.json"), J("g6_qc_sample.json"), J("g7_candidates_r1.json"), J("g7_qc_sample.json"), J("g8_candidates_r1.json"), J("g8_control_candidates_r1.json")
g10, g11, g12, g15c, g15q = J("g10_candidates_r1.json"), J("g11_candidates_r1.json"), J("g12_candidates_r1.json"), J("g15_g18_candidates_r1.json"), J("g15_g18_qc_sample.json")
gates = {}
gates["G5"] = {"pass": g5["pass"], "read": 600, "agree": g5["agree_with_gold"], "reader_errors_gold_right": g5["n_reader_error"],
               "clearly_wrong": g5["n_clearly_wrong"], "ambiguous": g5["n_ambiguous"], "ambiguous_ids": [a["id"] for a in g5["ambiguous"]],
               "pool_absent_entity_rows": g5["pool_scan_absent_entity"]["rows"], "file": "qc/g5.json"}
if g6:
    gates["G6"] = {"pass": g6["pass"], "set": "qc_sample", "bar": 0.52, "max_gated_grouped_by_card": g6.get("max_gated"),
                   "gated": g6["gated"], "random_fold_info": {v: {k: a for k, a in g6[v].items() if k.endswith("random")} for v in ("a_question", "c_card_noq", "d_meta")}, "file": "qc/g6_qc_sample.json"}
else:
    gates["G6"] = {"pass": None, "status": "not finished"}
gates["G7"] = {"pass": bool(g7c["pass"] and g7q["pass"]), "candidates_raw_fails": g7c["n_fail"], "qc_sample_raw_fails": g7q["n_fail"],
               "candidates_fail_text_meta": [g7c["n_fail_text"], g7c["n_fail_meta"]], "qc_sample_fail_text_meta": [g7q["n_fail_text"], g7q["n_fail_meta"]],
               "card_adjusted_fails_candidates": [f["feature"] for f in g7c["card_adjusted"]["fails"]],
               "card_adjusted_fails_qc_sample": [f["feature"] for f in g7q["card_adjusted"]["fails"]],
               "top_meta_fails": [[f["feature"], f["n"], f["yes"], f["n_cards"]] for f in g7q["fails"] if f["feature"].startswith("meta:")][:5],
               "files": ["qc/g7_candidates_r1.json", "qc/g7_qc_sample.json"]}
gates["G8"] = {"pass": g8["pass"], "gated": "grouped by card", "bar": "< 0.10", "grouped_share": g8["grouped"]["predictable_share"],
               "grouped_mean_heldout_acc": g8["grouped"]["mean_heldout_acc"], "instance_share_info": g8["instance"]["predictable_share"],
               "null_controls_grouped": {k: v["predictable_share"] for k, v in (g8c or {}).items() if isinstance(v, dict)},
               "note": "real grouped share is below every label-permuted null (no embedding-learnable signal above null); the < 10% bar is not reachable even by permuted labels at this design (prediction stability), so the fail is as-specified",
               "files": ["qc/g8_candidates_r1.json", "qc/g8_control_candidates_r1.json"]}
gates["G10"] = {"pass": g10["pass"], "fails": g10["fails"], "contrast_set_share": g10["A_quotas"].get("contrast_set_share"),
                "file": "qc/g10_candidates_r1.json"}
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
                "files": ["qc/g15_g18_candidates_r1.json", "qc/g15_g18_qc_sample.json"]}
gates["G18"] = {"pass": bool(g15c["G18"]["pass"] and g15q["G18"]["pass"]), "applies": False, "ordinal_rows": 0}
failed = [g for g, v in gates.items() if v.get("pass") is not True]
rep = {"family": "F5", "role": "independent checker (never wrote F5 generator/solvers)", "set": "out/candidates_r1.jsonl (5,398 rows); G6 on out/qc_sample.jsonl",
       "gates": gates, "failed_gates": failed,
       "g5_rule": "pass needs 0 clearly wrong and <= 6 ambiguous of 600", "pass": not failed}
json.dump(rep, open(L.QC / "QC_REPORT.json", "w"), indent=1)
print(json.dumps({"pass": rep["pass"], "failed": failed}))
