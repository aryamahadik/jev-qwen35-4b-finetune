"""Collect the independent F6 checker's gate outputs into qc/QC_REPORT.json (counts, paths and problems only)."""
import json, time
import qc_lib as q

J = lambda n: json.load(open(q.QC / n)) if (q.QC / n).exists() else None
g5, g6, g7, g8 = J("g5.json"), J("g6_qc_sample.json"), J("g7_candidates_r1.json"), J("g8_candidates_r1.json")
g8n, g10, g11, g12, g15 = J("g8_null_candidates_r1.json"), J("g10_candidates_r1.json"), J("g11_candidates_r1.json"), J("g12.json"), J("g15_g18_candidates_r1.json")
gates = {}
gates["G5"] = {"pass": bool(g5 and g5["pass"] and not g5["clearly_wrong"] and len(g5["ambiguous"]) <= 6), "file": "qc/g5.json",
               "sample_n": g5["sample_n"], "seed": g5["seed"], "agree_with_gold": g5["agree_with_gold"],
               "clearly_wrong": len(g5["clearly_wrong"]), "ambiguous": len(g5["ambiguous"])}
g6p = J("g6_qc_sample.partial.json")
if g6:
    gates["G6"] = {"pass": bool(g6.get("pass")), "file": "qc/g6_qc_sample.json", "yes_no": g6["yes_no"], "choice": g6["choice"]}
else:
    gates["G6"] = {"pass": False, "file": "qc/g6_qc_sample.partial.json (full run still going; it writes qc/g6_qc_sample.json)",
                   "parts_done": g6p["parts"] if g6p else {}, "fails_already": [k for k, v in (g6p or {}).get("parts", {}).items() if not v.get("pass", True)]}
gates["G7"] = {"pass": g7["pass"], "file": "qc/g7_candidates_r1.json", "n_tests": g7["n_tests"], "bonferroni_p": g7["bonferroni_p"],
               "yes_no_card_adjusted_fails": g7["n_yes_no_card_adjusted_fails"], "yes_no_raw_fails": g7["n_yes_no_raw_fails"],
               "yes_no_raw_fails_multi_card": g7["yes_no_raw_fails_multi_card"], "choice_fails": g7["n_choice_fails"],
               "top_card_adjusted": [{k: o[k] for k in ("feature", "n", "yes_rate", "exp_yes_card", "p_card", "n_cards")} for o in g7["yes_no_card_adjusted_fails"][:5]],
               "top_choice": [{k: o[k] for k in ("feature", "n_rows", "gold_hits", "expected", "p")} for o in g7["choice_fails"][:6]]}
gates["G8"] = {"pass": g8["pass"], "file": "qc/g8_candidates_r1.json", "rule": g8["rule"],
               "grouped_by_card": {k: g8["grouped_by_card"][k] for k in ("predictable_share", "yes_no_share", "choice_share", "by_form")},
               "instance_level": {k: g8["instance_level"][k] for k in ("predictable_share", "yes_no_share", "choice_share")},
               "null_control": ({"file": "qc/g8_null_candidates_r1.json", "real": g8n["real"], "null_range": g8n["null_range"]} if g8n else "not finished")}
gates["G10"] = {"pass": not g10["pool_fail"] and not g10["target_fail"], "file": "qc/g10_candidates_r1.json", "pool_fail": g10["pool_fail"],
                "target_fail": g10["target_fail"],
                "details": {c["check"]: {k: v for k, v in c.items() if k not in ("check", "fails", "kind")} for c in g10["checks"]
                            if not c["pass"] and c["kind"] in ("pool", "target")}}
gates["G11"] = {"pass": g11["pass"], "file": "qc/g11_candidates_r1.json", "fail_parts": g11["fail_parts"], "counts": g11["counts"],
                "surface_template": g11["surface_template"], "corpus_metrics": g11["corpus_metrics"],
                "seeds": {k: {kk: v[kk] for kk in ("n", "max", "pairs_ge_0.7")} for k, v in g11["claude_seeds_rouge_l"].items()},
                "frame_note": g11["claude_seeds_rouge_l"]["question_frames"].get("note")}
gates["G12"] = ({"pass": g12["pass"], "file": "qc/g12.json", "files": g12["files"], "cross_file": g12["cross_file"]} if g12 else
                {"pass": False, "file": "qc/g12.json (not finished)"})
import statistics
_, _side = q.load("candidates_r1")
_ft = [v["tokens"] for v in _side.values()]
length = {"definition_field_sum": "card + 2 x instructions + state + options, Qwen3.5-4B (= generator side 'tokens'; G0 s1 / AG-09)",
          "field_sum_median": statistics.median(_ft), "field_sum_max": max(_ft), "field_sum_rows_gt_1900": sum(1 for x in _ft if x > 1900),
          "field_sum_rows_le_900": sum(1 for x in _ft if x <= 900),
          "rendered_user_msg_median": g15["tokens"]["median"], "rendered_user_msg_max": g15["tokens"]["max"],
          "rendered_user_msg_rows_gt_1900": g15["tokens"]["rows_gt_1900"], "rows_gt_7900": g15["tokens"]["rows_gt_7900"],
          "median_500_900_pass": 500 <= statistics.median(_ft) <= 900, "cap_1900_field_sum_pass": max(_ft) <= 1900,
          "note": "the rendered decoder_io.user_msg (which itself repeats instructions) adds about 90 scaffold tokens; under that count 1,586 rows exceed 1,900"}
g15_core = (g15["loader_check_fail"] == 0 and g15["roundtrip_gold_fail"] == 0 and g15["gold_not_displayed"] == 0 and g15["relations_split_call_id"] == 0
            and g15["units_gt3"] == 0 and g15["units_long_gt2"] == 0 and g15["tokens"]["rows_gt_7900"] == 0)
gates["G15"] = {"pass": bool(g15_core and length["median_500_900_pass"] and length["cap_1900_field_sum_pass"]), "file": "qc/g15_g18_candidates_r1.json",
                "loader_roundtrip_units_pass": g15_core, **{k: g15[k] for k in ("loader_check_fail", "gold_not_displayed", "roundtrip_gold_fail",
                "relations", "relations_split_call_id", "unit_size_hist", "units_gt3", "units_long_gt2")}, "length": length,
                "prompts_file": "tmp/qc/g15_prompts_candidates_r1.txt (20 prompts, every form; read)"}
gates["G18"] = ({"pass": g15["G18"]["pass"], "vacuous": True, "ordinal_rows": g15["G18"]["ordinal_rows"]} if g15 else {"pass": False})
failing = [g for g, v in gates.items() if not v["pass"]]
rep = {"family": "F6", "round": 1, "report": "QC_REPORT", "checker": "independent F6 C checker",
       "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "inputs": {"candidates": "out/candidates_r1.jsonl (5,391 rows)", "qc_sample": "out/qc_sample.jsonl (5,212 rows; G6)",
                  "dev": "out/mixdev_S5.jsonl (400 rows; G12 cross-file)"},
       "g5": {"clearly_wrong": gates["G5"]["clearly_wrong"], "ambiguous": gates["G5"]["ambiguous"], "pass": gates["G5"]["pass"]},
       "gates": gates, "failing_gates": failing, "findings": json.load(open(q.TMP / "findings.json")) if (q.TMP / "findings.json").exists() else [],
       "pass": not failing,
       "pass_rule": "pass only if 0 clearly-wrong G5 flags, ambiguous <= 6, and every gate (G5, G6, G7, G8, G10, G11, G12, G15, G18) passes"}
json.dump(rep, open(q.QC / "QC_REPORT.json", "w"), indent=1)
print(json.dumps({"pass": rep["pass"], "failing": failing}))
