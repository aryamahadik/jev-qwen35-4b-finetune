"""r1.1 QC report: reads the gate outputs on the regenerated out/ files and writes qc/QC_REPORT.json (r1.0 report is
archived in qc/r1_0/QC_REPORT.json). Counts and file paths only, never row text. Run from c_src/F1."""
import json, os

F1 = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F1"
L = lambda p: json.load(open(os.path.join(F1, p)))

g5 = L("qc/g5_r11.json")
g6 = L("qc/g6_qc_sample.json")
g6d = L("qc/g6_diag_qc_sample.json")
g7q, g7c = L("qc/g7_qc_sample.json"), L("qc/g7_candidates_r1.json")
g8 = L("qc/g8_candidates_r1.json")
g8n = L("qc/g8_null_candidates_r1.json")
g10c, g10q = L("qc/g10_candidates_r1.json"), L("qc/g10_qc_sample.json")
g11 = L("qc/g11_candidates_r1.json")
g12 = L("qc/g12.json")
g1518 = L("qc/g15_g18.json")
sb = L("solverB/mismatch.json")
ms = L("tmp/merge_stats.json")
g4 = L("tmp/g4_summary.json")
seal = {f: L(f"tmp/{f}.sealedqc.jsonl.summary.json") for f in ("candidates_r1", "qc_sample", "mixdev_S5")}


def C(g):
    return g.get("checks", g)


g4_fail = sum(v for d in g4.values() if isinstance(d, dict) for k, v in d.items() if k.endswith(":fail"))
g4_rows = sum(d.get("rows", 0) for d in g4.values() if isinstance(d, dict))
yn, ch = g6["yes_no"], g6["choice"]
gates = {
    "G2": {"pass": sb["agree"] == sb["rows_checked"] and not sb["mismatches"], "file": "solverB/mismatch.json",
           "rows_checked": sb["rows_checked"], "agree": sb["agree"], "mismatches": len(sb["mismatches"]),
           "by_file": sb["by_file"],
           "note": "solver B fix (r1.1): a negation cue inside a yes/no field name ('pull test fail') was read as a "
                   "negation of the case sentence; cues are now counted net of the field name"},
    "G3": {"pass": all(ms[s]["gate_fail"] == 0 and ms[s]["loader_fail"] == 0 for s in ("cand", "qc"))
                   and all(ms["revalidate"][s]["rows_failed"] == 0 for s in ("cand", "qc")),
           "file": "tmp/merge_stats.json", "gate_fail": {s: ms[s]["gate_fail"] for s in ("cand", "qc")},
           "loader_fail": {s: ms[s]["loader_fail"] for s in ("cand", "qc")},
           "revalidate_rows_failed": {s: ms["revalidate"][s]["rows_failed"] for s in ("cand", "qc")},
           "near_dup_groups_dropped": ms["near_dup_groups_dropped"]},
    "G4": {"pass": g4_fail == 0, "file": "tmp/g4_summary.json", "rows": g4_rows, "fails": g4_fail,
           "note": "full run on pass 3; re-run after each later pass on every card regenerated in it (17 Q2 cards after passes 5b and 7; F1-C035, F1-C076; the 7 Q3 cards with swapped y)"},
    "sealed_check": {"pass": all(s["rows_hit"] == 0 for s in seal.values()),
                     "rows_hit": {f: s["rows_hit"] for f, s in seal.items()}, "rows": {f: s["rows"] for f, s in seal.items()}},
    "G5": {"pass": g5["pass"], "file": "qc/g5_r11.json", "sample_n": g5["sample_n"], "seed": g5["seed"],
           "agree": g5["agree_with_gold"], "clearly_wrong": g5["clearly_wrong"], "ambiguous": g5["ambiguous"],
           "by_qtype": g5["by_qtype"], "by_world": g5["by_world"], "note": g5.get("regeneration_note")},
    "G6": {"pass": g6["pass"], "file": "qc/g6_qc_sample.json", "diag": "qc/g6_diag_qc_sample.json",
           "rule": g6["rule"],
           "yes_no": {k: {"best": v["best"], "chance": v["chance"], "pass": v["pass"]} for k, v in yn.items()
                      if isinstance(v, dict) and "best" in v},
           "yes_no_diag": {"X_role_only": yn.get("diag_X_role_only"), "metadata_without_X_role": yn.get("diag_metadata_without_X_role")},
           "choice": {k: {"best": v["best"], "chance": v["chance_mean_1_over_k"], "pass": v["pass"]} for k, v in ch.items()
                      if isinstance(v, dict) and "best" in v},
           "choice_diag": {k: v for k, v in g6d.items() if k.startswith("ch_")}},
    "G7": {"pass": g7q["pass"] and g7c["pass"], "files": ["qc/g7_qc_sample.json", "qc/g7_candidates_r1.json"],
           "qc_sample": {"yes_no_card_null_fails": g7q["yes_no"]["card_rate_null"]["n_fail"],
                         "yes_no_literal_fails_info": g7q["yes_no"]["literal_p0_half"]["n_fail"],
                         "choice_fails": g7q["choice_options"]["n_fail"], "choice_kind_fails": g7q["choice_options"]["n_fail_kind"]},
           "candidates_r1": {"yes_no_card_null_fails": g7c["yes_no"]["card_rate_null"]["n_fail"],
                             "yes_no_literal_fails_info": g7c["yes_no"]["literal_p0_half"]["n_fail"],
                             "choice_fails": g7c["choice_options"]["n_fail"], "choice_kind_fails": g7c["choice_options"]["n_fail_kind"],
                             "choice_fail_kinds": [d["feature"] for d in g7c["choice_options"]["fails_top"] if d["feature"] != "<opt-ngram>"]}},
    "G8": {"pass": g8["pass"], "file": "qc/g8_candidates_r1.json", "null_file": "qc/g8_null_candidates_r1.json", "rule": "< 0.10",
           "grouped_by_card_predictable": g8["grouped_by_card"]["predictable_share"],
           "grouped_yes_no": g8["grouped_by_card"]["yes_no_share"], "grouped_choice": g8["grouped_by_card"]["choice_share"],
           "grouped_by_qtype": g8["grouped_by_card"].get("by_qtype"),
           "instance_level_predictable": g8["instance_level"]["predictable_share"],
           "yes_no_within_card_permutation_null": g8n.get("null_range"), "yes_no_real_vs_null": g8n.get("real")},
    "G10": {"pass": g10c["pass"] and g10q["pass"], "files": ["qc/g10_candidates_r1.json", "qc/g10_qc_sample.json"],
            "failed_candidates": g10c["failed"], "failed_qc_sample": g10q["failed"],
            "q2_code_share": {"candidates": C(g10c)["q2_code_share"]["diff_pp"], "qc_sample": C(g10q)["q2_code_share"]["diff_pp"]},
            "contrast_set_share": {"candidates": C(g10c)["twins_units"]["contrast_set_row_share"],
                                   "qc_sample": C(g10q)["twins_units"]["contrast_set_row_share"]},
            "depth_nondeep_shares": C(g10c)["depth"]["nondeep_shares"], "amendment_shares": C(g10c)["amendment_count"]["shares"]},
    "G11": {"pass": g11["pass"], "file": "qc/g11_candidates_r1.json", "failed": g11["failed"], "soft": g11.get("soft"),
            "compression_ratio": g11.get("compression_ratio_state"), "self_bleu4_approx": g11.get("self_bleu4_approx"),
            "vendi": g11.get("vendi_state_minilm_2000")},
    "G12": {"pass": g12["pass"], "file": "qc/g12.json", "exact_dups": g12["exact_duplicate_groups"],
            "structure_collisions": g12["structure_hash_collisions_across_groups"],
            "minhash_pairs_outside_group": g12["near_dup_pairs_outside_group"]},
    "G15": {"pass": g1518["G15"].get("pass"), "file": "qc/g15_g18.json"},
    "G18": {"pass": g1518["G18"].get("pass"), "file": "qc/g15_g18.json"},
}
qc_gates = ["G5", "G6", "G7", "G8", "G10", "G11", "G12", "G15", "G18"]
pre = ["G2", "G3", "G4", "sealed_check"]
failed = [k for k in pre + qc_gates if not gates[k]["pass"]]
notes = json.load(open(os.path.join(F1, "tmp/repair/report_notes_r11.json")))
rep = {"family": "F1", "round": 1, "repair": "r1.1", "checker": "independent C checker (gate scripts in qc/); repair and re-run by the F1 builder",
       "files": ["out/candidates_r1.jsonl", "out/qc_sample.jsonl", "out/mixdev_S5.jsonl"],
       "r1_0_report": "qc/r1_0/QC_REPORT.json", "r1_0_failed_gates": ["G6", "G7", "G8", "G10", "G11", "G12"],
       "gates": gates, "failed_gates": failed, "pass": not failed,
       "repair_summary": notes["repair_summary"], "remaining_problems": notes["remaining_problems"],
       "summary": notes["summary"]}
json.dump(rep, open(os.path.join(F1, "qc/QC_REPORT.json"), "w"), indent=1)
print(json.dumps({"failed_gates": failed, "pass": rep["pass"]}))
