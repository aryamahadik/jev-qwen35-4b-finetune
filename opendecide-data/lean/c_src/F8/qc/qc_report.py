"""Write qc/QC_REPORT.json for F8 from the independent checker's gate outputs (counts only, no row text).
pass = 0 clearly-wrong G5 flags, ambiguous <= 3, and every gate below passes. Usage: qc_report.py"""
import hashlib, json, time
import qc_lib as L

Q = L.QC


def j(name):
    p = Q / name
    return json.loads(p.read_text()) if p.exists() else None


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


g5, g6, g6c = j("g5.json"), j("g6_qc_sample.json"), j("g6_candidates_r1.json")
g7c, g7q = j("g7_candidates_r1.json"), j("g7_qc_sample.json")
g8 = j("g8_candidates_r1.json")
g8v2 = json.loads((L.LEAN / "c_build/g8v2/F8.json").read_text())
g10c, g10q = j("g10_candidates_r1.json"), j("g10_qc_sample.json")
g11, g12 = j("g11_candidates_r1.json"), j("g12_candidates_r1.json")
g15 = {n: j(f"g15_g18_{n}.json") for n in ("candidates_r1", "qc_sample", "mixdev_S5")}
mm = json.loads((L.F8 / "solverB/mismatch.json").read_text()) if (L.F8 / "solverB/mismatch.json").exists() else None
a19 = (L.LEAN / "c_build/g8v2/A19_ADOPTED").exists()


def fails(d):
    return [c["check"] for c in d["checks"] if not c["pass"]]


def gated_g6(d):
    out = {}
    for part in ("yes_no", "choice"):
        for k, v in d[part].items():
            if isinstance(v, dict):
                out[f"{part}.{k}"] = {"best": v["best"], "chance": v.get("chance", v.get("chance_mean_1_over_k")),
                                      "per_bucket_fails": len(v.get("per_bucket_fails", {})), "pass": v["pass"]}
    return out


gates = {}
gates["G5"] = {"pass": g5["clearly_wrong"] == 0 and g5["ambiguous"] <= 3, "read": g5["read"], "agree": g5["agree_with_gold"],
               "clearly_wrong": g5["clearly_wrong"], "ambiguous": g5["ambiguous"], "seed": 5001, "file": "qc/g5.json",
               "cosmetic_notes": len(g5["cosmetic_notes_no_label_effect"])}
gates["G6"] = {"pass": g6["pass"], "set": "qc_sample (5,185 rows)", "rule": "every view/model acc <= chance + 2 pp, 5-fold GroupKFold by card",
               "gated": gated_g6(g6), "selected_rows_rerun": "pending (no selection yet); candidates_r1 report: pass=%s" % g6c["pass"],
               "candidates_r1": gated_g6(g6c), "files": ["qc/g6_qc_sample.json", "qc/g6_candidates_r1.json"]}
gates["G7"] = {"pass": g7c["pass"] and g7q["pass"],
               "candidates_r1": {k: g7c[k] for k in ("n_tests", "n_fail", "n_fail_multi_card", "n_fail_single_card", "bonferroni_p")},
               "qc_sample": {k: g7q[k] for k in ("n_tests", "n_fail", "n_fail_multi_card", "n_fail_single_card", "bonferroni_p")},
               "files": ["qc/g7_candidates_r1.json", "qc/g7_qc_sample.json"]}
p8 = g8v2["parts"]
gates["G8"] = {"pass": (g8v2["pass"] if a19 else g8["pass"]), "judged_by": "G8v2 shared tool (A19 adopted)" if a19 else
               "spec 8 rule (< 10%), A19_ADOPTED absent; shared tool also run (report-only)",
               "spec_rule": {"grouped_by_card_share": g8["grouped_by_card"]["predictable_share"],
                             "yes_no_share": g8["grouped_by_card"]["yes_no_share"], "choice_share": g8["grouped_by_card"]["choice_share"],
                             "instance_level_share": g8["instance_level"]["predictable_share"],
                             "label_permuted_controls_grouped": {k: v["predictable_share"] for k, v in g8["label_permuted_control_grouped"].items()},
                             "heldout_acc_grouped": g8["grouped_by_card"]["heldout_acc"], "pass": g8["pass"]},
               "g8v2_shared_tool": {"pass": g8v2["pass"], "adapter": "registered at runtime by qc/g8v2.py (tool file unchanged)",
                                    "parts": {k: {"real_share": v["real"]["share"], "threshold": v["threshold"], "acc": v["real"]["acc"],
                                                  "chance": v["chance"], "pass": v["pass"]} for k, v in p8.items()},
                                    "old_raw_share": g8v2["old_rule"]["raw_share_all_rows"],
                                    "reproduction_within_spread": all(v["within_spread"] for v in g8v2["reproduction"]["parts"].values()),
                                    "file": "c_build/g8v2/F8.json"},
               "files": ["qc/g8_candidates_r1.json", "c_build/g8v2/F8.json"]}
gates["G10"] = {"pass": g10c["pass"], "n_checks": g10c["n_checks"], "n_fail": g10c["n_fail"], "failed": fails(g10c),
                "qc_sample_report": {"n_fail": g10q["n_fail"]},
                "pending": "difficulty bins (G9 crowd not run); [selection-time] aggregate and wording x k_all yes rates reported, feasibility gated",
                "files": ["qc/g10_candidates_r1.json", "qc/g10_qc_sample.json"]}
gates["G11"] = {"pass": g11["pass"], "parts": g11["pass_parts"], "counts": g11["counts"], "wordings": g11["wordings"],
                "worked_examples": g11["worked_examples"], "surface_template_max_pct": g11["surface_template"]["max_share_pct"],
                "seeds_rouge_l": {k: v["max"] for k, v in g11["claude_seeds_rouge_l"].items()},
                "corpus_metrics": g11["corpus_metrics"], "file": "qc/g11_candidates_r1.json"}
gates["G12"] = {"pass": g12["pass"], **{k: g12[k] for k in ("exact_duplicates", "near_dup_pairs_unplanned", "structure_groups_not_one_twin_set",
                                                             "overlap_with", "mixdev_S5_separation_ok", "rows_without_format_style")},
                "file": "qc/g12_candidates_r1.json"}
gates["G15"] = {"pass": all(v["G15_pass"] for v in g15.values()),
                **{n: {k: v[k] for k in ("check_rows_ok", "loader_check_fail", "round_trip_fail", "units_gt3", "long_units_gt2",
                                         "user_msg_tokens", "chat_tokens")} for n, v in g15.items()},
                "trainer": g15["candidates_r1"]["trainer"], "files": [f"qc/g15_g18_{n}.json" for n in g15]}
gates["G18"] = {"pass": all(v["G18"]["pass"] for v in g15.values()), "note": "F8 has no ordinal rows in round 1 (F8-R1-C3); 0 option_level rows"}
info = {"G2_builder": {"file": "solverB/mismatch.json", "summary": (mm if isinstance(mm, dict) and len(json.dumps(mm)) < 600 else "see file")}}
rel = L.OUT / "relations_candidates_r1.jsonl"
rep = {"family": "F8", "role": "independent checker (never an F8 generator or solver author)", "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "inputs": {"candidates_r1": {"path": "out/candidates_r1.jsonl", "sha256": sha(L.OUT / "candidates_r1.jsonl"), "rows": 3375},
                  "relations": {"path": "out/relations_candidates_r1.jsonl", "sha256": sha(rel), "rows": sum(1 for _ in open(rel))},
                  "qc_sample": {"path": "out/qc_sample.jsonl", "sha256": sha(L.OUT / "qc_sample.jsonl"), "rows": 5185},
                  "sidecar": "out/f8_controls_<set>.jsonl", "g0_spec_sha256": sha(L.F8 / "G0_SPEC.md")},
       "gates": gates, "info": info,
       "failed_gates": [g for g, v in gates.items() if not v["pass"]],
       "platform": "rrun (Modal CPU) for G6/G7/G8/G8v2/G15/G12; local nice for G10/G11/G5 (fast, deterministic)"}
rep["pass"] = not rep["failed_gates"]
(Q / "QC_REPORT.json").write_text(json.dumps(rep, indent=1, default=str))
print(json.dumps({"pass": rep["pass"], "failed_gates": rep["failed_gates"]}))
