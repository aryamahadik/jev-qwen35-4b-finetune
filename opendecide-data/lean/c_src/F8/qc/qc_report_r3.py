"""Write qc/QC_REPORT.json for F8, check:F8 r3 (c-lanes-v3, independent checker; never an F8 generator or solver author).
Counts only, no row text. pass = 0 clearly-wrong G5 flags, ambiguous <= 3, and every gate passes.
G8: c_build/g8v2/A19_ADOPTED exists -> A19.1: choice part judged by G8v3 (qc/g8v3_candidates_r1.json, p > 0.009);
yes/no part report-only (old raw share + G8v3 p). Spec-rule G8 (qc/g8_candidates_r1.json) reported. All runs local (nice 10,
<= 2 workers; rrun budget spent). Usage: qc_report_r3.py"""
import hashlib, json, time
import qc_lib as L

Q = L.QC


def j(name):
    p = Q / name
    return json.loads(p.read_text()) if p.exists() else None


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def nrows(p):
    return sum(1 for _ in open(p))


prev = j("prev_r2/QC_REPORT.json") or {}
g5, g6, g6c = j("g5.json"), j("g6_qc_sample.json"), j("g6_candidates_r1.json")
g7c, g7q = j("g7_candidates_r1.json"), j("g7_qc_sample.json")
g8, g8v3 = j("g8_candidates_r1.json"), j("g8v3_candidates_r1.json")
g10c, g10q = j("g10_candidates_r1.json"), j("g10_qc_sample.json")
g11, g12 = j("g11_candidates_r1.json"), j("g12_candidates_r1.json")
g15 = {n: j(f"g15_g18_{n}.json") for n in ("candidates_r1", "qc_sample", "mixdev_S5")}
a19 = (L.LEAN / "c_build/g8v2/A19_ADOPTED").exists()


def fails(d):
    return [c["check"] for c in d["checks"] if not c["pass"]]


def gated_g6(d):
    out = {}
    for part in ("yes_no", "choice"):
        for k, v in d[part].items():
            if isinstance(v, dict):
                out[f"{part}.{k}"] = {"lr": v.get("lr"), "gbt": v.get("gbt"), "best": v["best"],
                                      "chance": v.get("chance", v.get("chance_mean_1_over_k")),
                                      "per_bucket_fails": len(v.get("per_bucket_fails", {})), "pass": v["pass"]}
    return out


def g7s(d):
    return {**{k: d[k] for k in ("n_tests", "n_fail", "n_fail_multi_card", "n_fail_single_card", "bonferroni_p")},
            "fails": [{k: f.get(k) for k in ("part", "feature", "n", "n_rows", "yes_rate", "gold_hits", "expected", "dir", "p", "n_cards")
                       if f.get(k) is not None} for f in d["fails"]]}


gates = {}
gates["G5"] = {"pass": g5["clearly_wrong"] == 0 and g5["ambiguous"] <= 3, "read": g5["read"],
               "agree_first_pass": g5["agree_with_gold_first_pass"], "disagreements_reviewed": len(g5["disagreement_review"]),
               "clearly_wrong": g5["clearly_wrong"], "ambiguous": g5["ambiguous"], "seed": 5001, "file": "qc/g5.json",
               "cosmetic_notes": len(g5["cosmetic_notes_no_label_effect"])}
gates["G6"] = {"pass": g6["pass"], "set": "qc_sample (%d rows; separate >= 5,000-row QC sample)" % g6["n_rows"],
               "rule": "every view/model acc <= chance + 2 pp, 5-fold GroupKFold by card_id; metadata = model-visible only",
               "gated": gated_g6(g6), "candidates_r1_report": {"pass": g6c["pass"], "views": gated_g6(g6c)},
               "files": ["qc/g6_qc_sample.json", "qc/g6_candidates_r1.json"]}
gates["G7"] = {"pass": g7c["pass"] and g7q["pass"], "candidates_r1": g7s(g7c), "qc_sample": g7s(g7q),
               "files": ["qc/g7_candidates_r1.json", "qc/g7_qc_sample.json"]}
g8p = {}
if g8v3:
    for k, v in g8v3["parts"].items():
        g8p[k] = {"share": v["real"]["share"], "acc": v["real"]["acc"], "p": v["test"]["p"], "b": v["test"]["b"], "K": v["test"]["K"],
                  "verdict": v["test"]["verdict"], "pass": v["pass"], "gating": k == "choice"}
choice_pass = bool(g8v3 and g8v3["parts"].get("choice", {}).get("pass"))
gates["G8"] = {"pass": choice_pass if a19 else g8["pass"],
               "judged_by": "A19.1 (A19_ADOPTED exists): choice part by G8v3 p > 0.009; yes/no part report-only" if a19 else "spec rule",
               "g8v3_shared_tool": {"status": "done" if g8v3 else "missing", "parts": g8p,
                                    "old_raw_share": (g8v3 or {}).get("old_rule"), "tool_sha256": (g8v3 or {}).get("tool_sha256"),
                                    "adapter": "registered at runtime by qc/chk_g8v3.py (tool file unchanged)", "file": "qc/g8v3_candidates_r1.json"},
               "spec_rule_report_only": {"grouped_by_card_share": g8["grouped_by_card"]["predictable_share"],
                                         "yes_no_share": g8["grouped_by_card"]["yes_no_share"], "choice_share": g8["grouped_by_card"]["choice_share"],
                                         "instance_level_share": g8["instance_level"]["predictable_share"],
                                         "label_permuted_controls_grouped": {k: v["predictable_share"] for k, v in g8["label_permuted_control_grouped"].items()},
                                         "heldout_acc_grouped": g8["grouped_by_card"]["heldout_acc"], "pass_lt_10pct": g8["pass"]},
               "files": ["qc/g8v3_candidates_r1.json", "qc/g8_candidates_r1.json"]}
gates["G10"] = {"pass": g10c["pass"], "n_checks": g10c["n_checks"], "n_fail": g10c["n_fail"], "failed": fails(g10c),
                "qc_sample_report": {"n_fail": g10q["n_fail"], "failed": fails(g10q)},
                "blocked_not_weakened": ["attack twins (inv relation) about 5% of rows (3-7)", "'attack present' uncorrelated with the label"],
                "blocked_note": "tmp/repair/INFEASIBLE_G10_attack.md (named shared attack pool absent); the 2 checks stay failing",
                "pending": "difficulty bins (G9 crowd not run)", "files": ["qc/g10_candidates_r1.json", "qc/g10_qc_sample.json"]}
gates["G11"] = {"pass": g11["pass"], "parts": g11.get("pass_parts", g11.get("parts")), "file": "qc/g11_candidates_r1.json"}
gates["G12"] = {"pass": g12["pass"], **{k: g12.get(k) for k in ("exact_duplicates", "near_dup_pairs_unplanned", "structure_groups_not_one_twin_set",
                                                                 "mixdev_S5_separation_ok", "rows_without_format_style")},
                "file": "qc/g12_candidates_r1.json"}
gates["G15"] = {"pass": all(v.get("G15_pass", v.get("pass")) for v in g15.values()),
                **{n: {k: v.get(k) for k in ("check_rows_ok", "loader_check_fail", "round_trip_fail", "units_gt3", "long_units_gt2")} for n, v in g15.items()},
                "files": [f"qc/g15_g18_{n}.json" for n in g15]}
gates["G18"] = {"pass": all(v["G18"]["pass"] for v in g15.values()), "note": "F8 has no ordinal rows in round 1 (F8-R1-C3); 0 option_level rows"}
O = L.OUT
inputs = {"candidates_r1": {"path": "out/candidates_r1.jsonl", "sha256": sha(O / "candidates_r1.jsonl"), "rows": nrows(O / "candidates_r1.jsonl")},
          "relations": {"path": "out/relations_candidates_r1.jsonl", "sha256": sha(O / "relations_candidates_r1.jsonl"),
                        "rows": nrows(O / "relations_candidates_r1.jsonl")},
          "qc_sample": {"path": "out/qc_sample.jsonl", "sha256": sha(O / "qc_sample.jsonl"), "rows": nrows(O / "qc_sample.jsonl")},
          "relations_qc_sample": {"path": "out/relations_qc_sample.jsonl", "sha256": sha(O / "relations_qc_sample.jsonl"),
                                  "rows": nrows(O / "relations_qc_sample.jsonl")},
          "mixdev_S5": {"path": "out/mixdev_S5.jsonl", "sha256": sha(O / "mixdev_S5.jsonl"), "rows": nrows(O / "mixdev_S5.jsonl")},
          "relations_mixdev_S5": {"path": "out/relations_mixdev_S5.jsonl", "sha256": sha(O / "relations_mixdev_S5.jsonl"),
                                  "rows": nrows(O / "relations_mixdev_S5.jsonl")},
          "sidecar": "out/f8_controls_<set>.jsonl", "g0_spec_sha256": sha(L.F8 / "G0_SPEC.md")}
rep = {"family": "F8", "role": "independent checker (never an F8 generator or solver author)", "round": "check:F8 r3 (c-lanes-v3)",
       "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "inputs": inputs, "gates": gates,
       "failed_gates": [g for g, v in gates.items() if not v["pass"]],
       "platform": "local Mac, nice 10, <= 2 workers (rrun budget spent); all gates re-run on one platform",
       "builder_refresh": prev.get("builder_refresh"), "previous_checker_outputs": "qc/prev_r2/ (r2 checker, previous pool)"}
rep["pass"] = not rep["failed_gates"]
extra = j("qc_report_r3_notes.json")
if extra:
    rep.update(extra)
(Q / "QC_REPORT.json").write_text(json.dumps(rep, indent=1, default=str))
print(json.dumps({"pass": rep["pass"], "failed_gates": rep["failed_gates"]}))
