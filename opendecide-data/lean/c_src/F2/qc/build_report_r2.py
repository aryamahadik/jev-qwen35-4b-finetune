"""Assemble qc/QC_REPORT.json after F2 repair round 2 (generator r1.3; c-lanes-v3). Previous report -> QC_REPORT_prev.json.
G8 judged by A19.1 (c_build/g8v2/A19_ADOPTED): choice part = G8v3 p > 0.009 (qc/g8v3_candidates_r1.json, run with
c_src/common/g8_aflite.py on this pool); yes/no part report-only; the old raw share is reported too.
Relation files' rows and sha256 recorded (MIXER_NOTE 2). Based on build_report_r12.py: Counts only, no row text.
Inputs: regenerated out/ files, builder gates (out/gates_report.json), solver B (solverB/mismatch.json), sealed check
(tmp/sealed_report.json), the QC gate scripts re-run on the regenerated files (qc/g6..g18), the fresh G5 read
(qc/g5.json, seed 5002) and the repair diagnostics (tmp/repair/diag_*.json). v1.0 report kept as QC_REPORT_v10.json."""
import json, hashlib
from pathlib import Path
F2 = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F2")
Q = F2 / "qc"


def J(p):
    return json.loads(Path(p).read_text())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def nrows(p):
    return sum(1 for _ in open(p))


g5, g6, g7q, g7c = J(Q / "g5.json"), J(Q / "g6.json"), J(Q / "g7_qc_sample.json"), J(Q / "g7_candidates_r1.json")
g8, g8c, g8s = J(Q / "g8_candidates_r1.json"), J(Q / "g8_control_candidates_r1.json"), J(Q / "g8_sweep_candidates_r1.json")
g10, g10q, g11, g12 = J(Q / "g10_candidates_r1.json"), J(Q / "g10_qc_sample.json"), J(Q / "g11_candidates_r1.json"), J(Q / "g12_candidates_r1.json")
g15, g18 = J(Q / "g15_candidates_r1.json"), J(Q / "g18.json")
gates_b, sb, sealed = J(F2 / "out/gates_report.json"), J(F2 / "solverB/mismatch.json"), J(F2 / "tmp/sealed_report.json")
diag = J(F2 / "tmp/repair/diag_final.json")
v10 = J(Q / "QC_REPORT_v10.json")
prev = J(Q / "QC_REPORT_prev.json")
g8v3 = J(Q / "g8v3_candidates_r1.json")
CAND = F2 / "out/candidates_r1.jsonl"
assert g8v3["pool_sha256"] == sha(CAND), "G8v3 report is for another pool: re-run g8_aflite on this pool"
INFEASIBLE = {"gold rank uniform (value/date): smallest and largest each 1/k_ord +/- 2 pp": "tmp/repair/INFEASIBLE_G10_rank_abstain.md"}


def g6_part(p):
    out = {}
    for view, v in g6[p].items():
        if not isinstance(v, dict):
            continue
        out[view] = {"best": round(v.get("best", 0), 4), "pass": v.get("pass"),
                     "chance": round(v.get("chance", v.get("chance_mean_1_over_k", 0.5)), 4)}
        if v.get("per_bucket_fails"):
            out[view]["per_bucket_fails"] = v["per_bucket_fails"]
    return out


g8_floor = {k: round(v["predictable_share"], 4) for k, v in g8c.items()}
g8_floor_ch = {k: round(v.get("choice_share", 0), 4) for k, v in g8c.items()}
g8_floor_yn = {k: round(v.get("yes_no_share", 0), 4) for k, v in g8c.items()}
g4ok = all(v.get("g4_pass") for v in gates_b["g4_train_files"].values()) and gates_b["g4_s5"]["S5"]["g4_pass"]
g3ok = all(gates_b[k]["g3"]["pass_rate"] == 1.0 for k in ("candidates", "qc", "mixdev"))
sealed_hits = sum(len(v.get("hit_ids", [])) for v in sealed.values())
gates = {
 "G2": {"pass": sb["total"]["mismatch"] == 0 and sb["total"]["error"] == 0, "file": "solverB/mismatch.json",
        **{k: sb["total"][k] for k in ("rows", "agree", "mismatch", "error")}},
 "G3": {"pass": g3ok, "file": "out/gates_report.json",
        "pass_rate": {k: gates_b[k]["g3"]["pass_rate"] for k in ("candidates", "qc", "mixdev")}},
 "G4": {"pass": g4ok, "file": "out/gates_report.json",
        "per_sampler": {s: {"rows": v["rows"], "relations": v["relations_tested"], "all_100pct": v["all_relations_100pct"],
                            "relations_100pct_on_ge_1000": v["relations_at_100pct_on_ge_1000"]} for s, v in gates_b["g4_train_files"].items()},
        "S5": gates_b["g4_s5"]["S5"]["g4_pass"]},
 "sealed_check": {"pass": sealed_hits == 0, "hits": sealed_hits, "file": "tmp/sealed_report.json"},
 "G5": {"pass": g5["pass"], "file": "qc/g5.json", "n": g5["sample"]["n"], "seed": g5["sample"]["seed"],
        "reader_agrees_with_gold": g5["reader_vs_gold"]["agree"], "clearly_wrong": g5["n_clearly_wrong"],
        "ambiguous": g5["n_ambiguous"], "wording_notes": g5["wording_notes_label_determinable"],
        "reader": g5["reader"], "v10_flags": g5["previous_flags_v10"]},
 "G6": {"pass": g6["pass"], "file": "qc/g6.json", "sample": f"out/qc_sample.jsonl ({nrows(F2 / 'out/qc_sample.jsonl')} rows)",
        "yes_no": g6_part("yes_no"), "choice": g6_part("choice")},
 "G7": {"pass": g7q["pass"] and g7c["pass"], "file": "qc/g7_qc_sample.json, qc/g7_candidates_r1.json",
        "qc_sample": {k: g7q[k] for k in ("n_tests", "n_fail", "n_fail_multi_card", "n_fail_single_card")},
        "candidates_r1": {k: g7c[k] for k in ("n_tests", "n_fail", "n_fail_multi_card", "n_fail_single_card")},
        "top_fails": sorted(g7q["fails"] + g7c["fails"], key=lambda f: f["p"])[:8]},
 "G8": {"pass": bool(g8v3["parts"]["choice"]["g8v3_pass"]), "rule": "A19.1: choice part G8v3 p > 0.009; yes/no report-only",
        "file": "qc/g8v3_candidates_r1.json (+ old-rule qc/g8_candidates_r1.json, g8_control, g8_sweep)",
        "g8v3": {p: {k: g8v3["parts"][p].get(k) for k in ("n_rows", "n_cards", "real_share", "real_acc", "g8v3_test", "g8v3_pass")}
                 for p in ("choice", "yes_no")}, "tool_sha256": g8v3.get("tool_sha256"),
        "old_rule_raw_share": {"grouped_by_card_predictable_share": round(g8["grouped_by_card"]["predictable_share"], 4),
                               "yes_no_share": round(g8["grouped_by_card"]["yes_no_share"], 4),
                               "choice_share": round(g8["grouped_by_card"]["choice_share"], 4),
                               "permuted_label_control_share": g8_floor, "control_yes_no_share": g8_floor_yn,
                               "control_choice_share": g8_floor_ch, "old_rule_pass": g8["pass"]}},
 "G10": {"pass": g10["pass"], "file": "qc/g10_candidates_r1.json (+ g10_qc_sample.json)", "n_checks": g10["n_checks"],
         "n_fail": g10["n_fail"], "failed": g10["failed"],
         "infeasible_as_computed": {c: INFEASIBLE[c] for c in g10["failed"] if c in INFEASIBLE},
         "failed_excluding_infeasible": [c for c in g10["failed"] if c not in INFEASIBLE], "qc_sample_n_fail": g10q["n_fail"], "qc_sample_failed": g10q["failed"],
         "key_values": {c["check"]: c["value"] for c in g10["checks"] if not c["pass"]}},
 "G11": {"pass": g11["pass"], "file": "qc/g11_candidates_r1.json", **{k: g11[k] for k in ("counts", "surface_template", "claude_seeds_rouge_l", "corpus_metrics", "pass_parts")}},
 "G12": {"pass": g12["pass"], "file": "qc/g12_candidates_r1.json", **{k: g12[k] for k in ("exact_duplicates", "near_dup_pairs_ge_0.9", "near_dup_pairs_unplanned", "structure_groups_multi", "structure_groups_not_one_twin_set", "structure_overlap_with")}},
 "G15": {"pass": g15.get("pass", g15["loader_check_fail"] == 0 and g15["round_trip_fail"] == 0), "file": "qc/g15_candidates_r1.json",
         **{k: g15[k] for k in ("rows", "check_rows_ok", "loader_check_fail", "round_trip_fail", "max_unit_rows", "units_gt3", "long_units_gt2", "rows_gt_7900", "tokens_max", "rows_ge_2000")}},
 "G18": {"pass": g18["pass"], "file": "qc/g18.json", "applicable": False,
         **{k: g18[k] for k in ("option_level_rows_candidates_r1", "option_level_rows_qc_sample", "option_level_rows_mixdev_S5")}},
}
repair = {
 "generator": "F2-gen r1 v1.3 (gen/common.py GEN_VERSION); r1.2 code kept in tmp/r2/gen_pre_r2/",
 "previous": prev.get("repair"),
 "fixes_r2": [
  "gold rank: a structure is accepted on all-rank feasibility (k_ord - 1 single-hook values on each side of gold), never on the drawn rank (gen/options.kmax_all_ranks*; v1.2 rejected only the drawn rank and the held redraw moved end ranks to the middle on k_ord >= 4: G6 choice gbt:2-4, G7 rank:val_inner, G10 rank)",
  "abstain gold: 1/k nudged by the running per-cell deficit (abstain option x k bucket) of rows already written (gen/options.abst_p)",
  "adjustments: each base row focuses the has:x adjustment furthest from 50% dec/bind and wants the status that corrects it (gen/build.AdjBal); 16 focus tries",
  "decisive semantics: while emitted rows with >= 1 sem:* are below 46%, money/band candidates must carry one (gen/build.cand_sem)",
  "depth groups: money rows draw a held group target a/b/c/d = 0.20/0.42/0.30/0.08, strict for 150 attempts (gen/mgen.group_target)",
  "named-option cards weigh 1.25 in card targets and B1 balancing (gen/build.card_weight)",
  "card seeds: up to 40 (was 12) for the rank probe",
  "G5 wording flag: no 'owed owed' in the X8 floor clause (gen/mcard)",
  "MANIFEST: parents list and relations block (MIXER_NOTE 1, 3)"],
 "not_changed": "solver B, the parser, the lexicon and the frozen G0 spec are unchanged"}
extra = {"diagnostics_v10_vs_v12": diag,
         "notes": {
  "G10_rank_check_method": "the G10 value/date and band rank checks count abstain-gold rows (gold cannot be first/last there) in the observed share but not in the 1/k_ord expectation; on rows whose gold is an ordered option the shares are in diagnostics_v10_vs_v12.rank_*",
  "G8_method": "the permuted-label control (labels shuffled within card) already scores above the 10% bar: per-card yes rates are 20-80% by design (spec 2.1), so a card-grouped split predicts the card's majority label; the literal < 10% rule cannot be met by cue-free labels under this procedure (method item for the orchestrator)",
  "S4_case_lists": "under one deadline rule and one depth group the late case has the largest action-event gap unless an extension or business-day calendar differs per case; residual reported in diagnostics"}}
failed = [g for g, v in gates.items() if not v["pass"]]
out = {"family": "F2", "checker": "F2 repair session (re-ran the independent checker's gate scripts qc/g6..g18 unchanged on the regenerated files; G5 re-read by this session, seed 5002)",
       "inputs": {f: {"rows": nrows(F2 / "out" / f), "sha256": sha(F2 / "out" / f)} for f in ("candidates_r1.jsonl", "qc_sample.jsonl", "mixdev_S5.jsonl", "candidates_r1.relations.jsonl", "qc_sample.relations.jsonl")},
       "relation_file_sha256": sha(F2 / "out/candidates_r1.relations.jsonl"),
       "spec": "C_DATA_SPEC v4 (2.1, 2.2 F2, 2.4, 6, 8, 10); C_TRAIN_RECIPE v4; PREREG A15, A16, A16.1; F2 G0_SPEC v7 incl. XF",
       "repair": repair, "gates": gates, "extra_diagnostics": extra, "failed_gates": failed,
       "v10_failed_gates": v10.get("failed_gates"), "prev_failed_gates": prev.get("failed_gates"), "pass": not failed,
       "not_run_here": {"G9": "crowd scoring on free L4 (orchestrator)", "G11 golden_train comparison": "golden_train outside allow-list",
                        "G13": "orchestrator decontamination", "G10 bin-level": "after G9"}}
(Q / "QC_REPORT.json").write_text(json.dumps(out, indent=1, default=str))
print("pass", out["pass"], "failed", failed)
