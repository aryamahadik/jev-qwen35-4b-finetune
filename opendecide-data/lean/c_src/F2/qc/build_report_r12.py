"""Assemble qc/QC_REPORT.json after the F2 repair (generator r1.2). Counts only, no row text.
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
 "G8": {"pass": g8["pass"], "file": "qc/g8_candidates_r1.json (+ g8_control, g8_sweep)",
        "grouped_by_card_predictable_share": round(g8["grouped_by_card"]["predictable_share"], 4),
        "yes_no_share": round(g8["grouped_by_card"]["yes_no_share"], 4), "choice_share": round(g8["grouped_by_card"]["choice_share"], 4),
        "instance_level_share": round(g8["instance_level"]["predictable_share"], 4),
        "permuted_label_control_share": g8_floor, "control_yes_no_share": g8_floor_yn, "control_choice_share": g8_floor_ch,
        "C_sweep_real_vs_control": {c: [round(v["real"]["predictable_share"], 4), round(v["control"]["predictable_share"], 4)] for c, v in g8s.items()}},
 "G10": {"pass": g10["pass"], "file": "qc/g10_candidates_r1.json (+ g10_qc_sample.json)", "n_checks": g10["n_checks"],
         "n_fail": g10["n_fail"], "failed": g10["failed"], "qc_sample_n_fail": g10q["n_fail"], "qc_sample_failed": g10q["failed"],
         "key_values": {c["check"]: c["value"] for c in g10["checks"] if not c["pass"]}},
 "G11": {"pass": g11["pass"], "file": "qc/g11_candidates_r1.json", **{k: g11[k] for k in ("counts", "surface_template", "claude_seeds_rouge_l", "corpus_metrics", "pass_parts")}},
 "G12": {"pass": g12["pass"], "file": "qc/g12_candidates_r1.json", **{k: g12[k] for k in ("exact_duplicates", "near_dup_pairs_ge_0.9", "near_dup_pairs_unplanned", "structure_groups_multi", "structure_groups_not_one_twin_set", "structure_overlap_with")}},
 "G15": {"pass": g15.get("pass", g15["loader_check_fail"] == 0 and g15["round_trip_fail"] == 0), "file": "qc/g15_candidates_r1.json",
         **{k: g15[k] for k in ("rows", "check_rows_ok", "loader_check_fail", "round_trip_fail", "max_unit_rows", "units_gt3", "long_units_gt2", "rows_gt_7900", "tokens_max", "rows_ge_2000")}},
 "G18": {"pass": g18["pass"], "file": "qc/g18.json", "applicable": False,
         **{k: g18[k] for k in ("option_level_rows_candidates_r1", "option_level_rows_qc_sample", "option_level_rows_mixdev_S5")}},
}
repair = {
 "generator": "F2-gen r1 v1.2 (gen/common.py GEN_VERSION); v1.0 code kept in tmp/repair/gen_pre_repair/",
 "root_cause_of_the_rank_cue": "v1.0 drew gold's rank (and the option count, card variant, label side, comparator family) afresh on every structure retry; retries that rejected infeasible (structure, rank) pairs pulled gold to the middle on average and to one end on cards whose named errors all fall on one side",
 "fixes": [
  "held draws: gold rank (u_rank), option count (u_k), case-list gold rank (u_crank), card variant, label (aff), label-side draws (u_side: near/far, delta, comparator family, S4 question kind) and unit/negation are drawn once per base row and held across every retry; a held draw a card cannot build is redrawn after 4 dead tries (counted as held_redraw)",
  "card-level feasibility: a choice card must be able to put gold at both ends of its ordered options (R2-17; 3.4 'resample, never pad'); 10 cards were redrawn with a new card seed",
  "case lists: cases come from one drawn pool, one depth group; gold's rank on the visible primary column (money/band: first value column; dates: action minus event gap) is held uniform; S3 case lists use a computed banding amount and S4 case lists a per-case extension condition (>= 2 interacting per-case fields)",
  "clause-flip twins try every flip variant (twin sets 19.0% -> see G10)",
  "B1 form assigned by expected row weight over band cards; named-option style cycled over named cards (masked share)",
  "unpaired yes/no card of an odd sampler at yes rate 0.5",
  "case-count token shrink only after 3 token failures (v1.0 dropped all larger counts on the first one)",
  "G5 flags: Q1 target naming (mcard: no named step -> result is the line charge/subtotal), fee-step self-name (bcard), D12 roll reference (dcard: extension cards always state D7)",
  "qc_sample rows carry the F2q id prefix (a first v1.2 run reused F2c ids; G4 twin checks on cand+qc failed only because of the id collision; candidates were byte-identical after the fix)"],
 "not_changed": "solver B, the parser, the lexicon and the frozen G0 spec are unchanged"}
extra = {"diagnostics_v10_vs_v12": diag,
         "notes": {
  "G10_rank_check_method": "the G10 value/date and band rank checks count abstain-gold rows (gold cannot be first/last there) in the observed share but not in the 1/k_ord expectation; on rows whose gold is an ordered option the shares are in diagnostics_v10_vs_v12.rank_*",
  "G8_method": "the permuted-label control (labels shuffled within card) already scores above the 10% bar: per-card yes rates are 20-80% by design (spec 2.1), so a card-grouped split predicts the card's majority label; the literal < 10% rule cannot be met by cue-free labels under this procedure (method item for the orchestrator)",
  "S4_case_lists": "under one deadline rule and one depth group the late case has the largest action-event gap unless an extension or business-day calendar differs per case; residual reported in diagnostics"}}
failed = [g for g, v in gates.items() if not v["pass"]]
out = {"family": "F2", "checker": "F2 repair session (re-ran the independent checker's gate scripts qc/g6..g18 unchanged on the regenerated files; G5 re-read by this session, seed 5002)",
       "inputs": {f: {"rows": nrows(F2 / "out" / f), "sha256": sha(F2 / "out" / f)} for f in ("candidates_r1.jsonl", "qc_sample.jsonl", "mixdev_S5.jsonl")},
       "spec": "C_DATA_SPEC v4 (2.1, 2.2 F2, 2.4, 6, 8, 10); C_TRAIN_RECIPE v4; PREREG A15, A16, A16.1; F2 G0_SPEC v7 incl. XF",
       "repair": repair, "gates": gates, "extra_diagnostics": extra, "failed_gates": failed,
       "v10_failed_gates": v10.get("failed_gates"), "pass": not failed,
       "not_run_here": {"G9": "crowd scoring on free L4 (orchestrator)", "G11 golden_train comparison": "golden_train outside allow-list",
                        "G13": "orchestrator decontamination", "G10 bin-level": "after G9"}}
(Q / "QC_REPORT.json").write_text(json.dumps(out, indent=1, default=str))
print("pass", out["pass"], "failed", failed)
