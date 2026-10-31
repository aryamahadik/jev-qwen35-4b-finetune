"""Assemble qc/QC_REPORT.json for F7 (independent checker). Reads only the checker's own gate outputs in qc/ and the
builder's out/ files for sha256s and its G2/G3/G4 records (reported, not re-run here). Counts only, no row text.
pass = G5 (0 clearly wrong, ambiguous <= 3) AND every gated gate (G6, G7, G8, G10, G11, G12, G15, G18) passes."""
import hashlib, json, time
from pathlib import Path

F7 = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F7")
Q, O = F7 / "qc", F7 / "out"
J = lambda p: json.loads((Q / p).read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    g5, g6, g8 = J("g5.json"), J("g6_qc_sample.json"), J("g8_candidates_r1.json")
    g7c, g7q = J("g7_candidates_r1.json"), J("g7_qc_sample.json")
    g10c, g10q = J("g10_candidates_r1.json"), J("g10_qc_sample.json")
    g11, g12 = J("g11_candidates_r1.json"), J("g12_candidates_r1.json")
    g15c, g15q = J("g15_g18_candidates_r1.json"), J("g15_g18_qc_sample.json")
    solb = json.loads((F7 / "solverB/run.log").read_text())
    g4 = json.loads((O / "G4_metamorphic.json").read_text())
    gb = json.loads((O / "gates_candidates_r1.json").read_text())
    s8 = g8["F7_summary"]
    name_cue = {o["feature"]: {k: o[k] for k in ("n", "gold_has", "expected", "p_two_sided")}
                for o in g7c["option_level_tests"] if o["feature"].startswith("opt:name_in_state")}
    gates = {
        "G5": {"pass": g5["clearly_wrong"] == 0 and g5["ambiguous"] <= 3, "read": g5["read"],
               "agree": g5["reader_agrees_with_gold"], "clearly_wrong": g5["clearly_wrong"], "ambiguous": g5["ambiguous"],
               "file": "qc/g5.json"},
        "G6": {"pass": g6["pass"], "set": "qc_sample (5,036 rows, 80 cards; GroupKFold by card)", "chance": g6["chance_mean_1_over_K"],
               "bar": g6["bar"], "max_gated": g6["max_gated"], "gated": g6["gated"],
               "hidden_meta_info_grouped_max": g6["hidden_info_grouped_max"], "file": "qc/g6_qc_sample.json"},
        "G7": {"pass": g7c["pass"], "gated_set": "candidates_r1",
               "candidates": {"tests": g7c["tests"], "n_fail": g7c["n_fail"], "text_meta_fails": g7c["fails"][:10],
                              "option_level_fails": [o["feature"] for o in g7c["option_level_fails"]]},
               "qc_sample_info": {"n_fail": g7q["n_fail"], "text_meta_fails": g7q["fails"][:10],
                                  "option_level_fails": [o["feature"] for o in g7q["option_level_fails"]]},
               "level_name_in_state_cue": name_cue,
               "files": ["qc/g7_candidates_r1.json", "qc/g7_qc_sample.json"]},
        "G8": {"pass": s8["spec_G8"]["pass"], "verdict_source": s8["verdict_source"], "A19_ADOPTED": s8["A19_ADOPTED"],
               "spec_G8_raw_share": s8["spec_G8"]["raw_share"], "spec_bar": "< 0.10", "G8v2": s8["G8v2"],
               "file": "qc/g8_candidates_r1.json"},
        "G10": {"pass": g10c["pass"], "gated_set": "candidates_r1", "fails": g10c["fails"], "soft_misses": g10c["soft_misses"],
                "qc_sample_info_fails": g10q["fails"], "files": ["qc/g10_candidates_r1.json", "qc/g10_qc_sample.json"]},
        "G11": {"pass": g11["pass"], "counts_pass": g11["counts"]["pass"], "two_pct": g11["two_pct"],
                "seeds_rouge_l": {k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "examples"})
                                  for k, v in g11["seeds_rouge_l"].items()},
                "metrics": g11["metrics"], "file": "qc/g11_candidates_r1.json"},
        "G12": {"pass": g12["pass"], "exact": [g12["exact_dup_model_view"], g12["exact_dup_raw_fields"]],
                "minhash": {k: v for k, v in g12["minhash"].items() if k != "examples"},
                "structure_hash_generator": {k: v for k, v in g12["structure_hash_generator"].items() if k != "example_groups"},
                "structure_independent": {k: v for k, v in g12["structure_independent"].items() if k != "examples"},
                "file": "qc/g12_candidates_r1.json"},
        "G15": {"pass": g15c["G15_pass"] and g15q["G15_pass"],
                "candidates": {k: g15c[k] for k in ("loader_check_fail", "roundtrip_gold_fail", "relations", "relations_split_call_id",
                                                     "relations_gold_inconsistent", "units_gt3", "units_long_gt2",
                                                     "tokens_full_chat_prompt", "gold_letter_chi2_p_by_K_seed15007", "check_rows_all")},
                "qc_sample": {k: g15q[k] for k in ("loader_check_fail", "roundtrip_gold_fail", "units_gt3", "units_long_gt2")},
                "trainer": g15c["trainer_used"], "files": ["qc/g15_g18_candidates_r1.json", "qc/g15_g18_qc_sample.json"]},
        "G18": {"pass": g15c["G18"]["pass"] and g15q["G18"]["pass"], "candidates": g15c["G18"], "qc_sample": g15q["G18"]},
    }
    gates["G7"]["diagnosis"] = ("Gated fail is opt:name_in_state only: every candidate row whose case text names a level is an "
        "inv attack twin (210/210; clean rows 0), and the injected instruction names a NON-gold level by G0 7 design, so the "
        "named level is gold 0/210 (expected 45.6). On clean rows level names/numbers in the case are independent of gold "
        "(num_in_state clean p=0.99). Text and metadata features: 0 fails on candidates_r1; qc_sample has 3 text fails, each "
        "a card-internal decisive fact in 1-3 cards. Fix needs a generator/attack-design change or an orchestrator ruling "
        "(G0 7 attack wording vs G0 6.5 / data-spec G7).")
    gates["G10"]["diagnosis"] = ("Data-spec G10 v4 items pass on candidates (gold letter per K, longest option, abstain 0, attack "
        "vs label, level share per sampler x K, per-card quotas, mode x level). Fails are G0 section 6 targets: S2 "
        "inclusive share 0.665 (409 incl / 206 excl; rule 50/50), two-way conv direction outside 50+/-5 (C16 S1 0.406, "
        "C16 S2 0.573, C8+C9 S1 0.444, C8+C9 S2 0.343, C11 S6 0.393, C15 S3 0.571, C19 S6 0.556, C15 pooled 0.415), and "
        "C1-unmentioned rows that are decisive 0.34 / 0.22 / 0.35 (S1/S2/S4; rule 40-60%). qc_sample additionally shows "
        "absence-word and negcount k_all vs level dependence in S1/S2/S3 (p<=1e-3) and one card off its level quota.")
    g11s = g11["seeds_rouge_l"]
    gates["G11"]["pass_wordings_only"] = g11s["wordings_only"]["pairs_ge_0.7"] == 0
    gates["G11"]["diagnosis"] = ("Counts, 2% template rule and the 36 F7 wording seeds pass (max ROUGE-L 0.59). The 6 pairs >= 0.7 "
        "are canonical C-line contrast variants of one tag (C11_high/low 0.909, C13_cap/floor 0.889, C15_blank/key 0.778, "
        "C16_count/points 0.75, C1_list/one 0.741, C8/C9 0.75): different meanings one or two words apart, written as "
        "G0 3.2 canonical lines. Counted as a fail under the literal data-spec rule (every Claude seed < 0.7). Fix: "
        "paraphrase variants (G0 step-4 pools) that keep each pair under 0.7, or an orchestrator ruling on whether "
        "contrast variants of one tag are compared. Closed 3.1 fact frames are reported only.")
    gates["G12"]["diagnosis"] = ("0 exact duplicates. 544 structure_hash groups span more than one unit (all same card, same "
        "gold; S3 174, S6 158, S4 89, S2 72, S1 51); 301 of them repeat a format_style, and 50 groups (68 extra rows, all "
        "S6) repeat format_style + wording + defs style + identical case text up to the entity ID, which no reading of "
        "'format variant' covers. MinHash: 618 non-twin pairs >= 0.8 (all within a card). Part of the S6 repeats is forced "
        "by G0 S6 placement quotas: each card has at most 3(K-1) at/below/above values for about 31-37 boundary base "
        "rows (e.g. K=3 cards: 6 distinct structures for 37 rows).")
    rel = O / "candidates_r1.relations.jsonl"
    rep = {"family": "F7", "role": "independent checker (never wrote F7's generator or solvers)",
           "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "candidates_r1": {"path": "out/candidates_r1.jsonl", "sha256": sha(O / "candidates_r1.jsonl"),
                             "rows": sum(1 for _ in open(O / "candidates_r1.jsonl"))},
           "relations": {"path": "out/candidates_r1.relations.jsonl", "sha256": sha(rel), "rows": sum(1 for _ in open(rel))},
           "qc_sample": {"path": "out/qc_sample.jsonl", "sha256": sha(O / "qc_sample.jsonl")},
           "G0_SPEC_sha256": sha(F7 / "G0_SPEC.md"),
           "platform": "gate scripts G6/G7/G8/G10/G11/G12/G15 run on rrun (A20 a); G5 read locally",
           "gates": gates,
           "builder_records_not_rerun": {"G2_solverB": solb, "G3_round_trip_pass_rate": gb.get("G3_pass_rate"),
                                         "G4": {"pass_all_100pct": g4.get("pass_all_100pct"), "failures": g4.get("failures")}},
           }
    rep["failed_gates"] = [g for g, d in gates.items() if not d["pass"]]
    rep["pass"] = not rep["failed_gates"]
    (Q / "QC_REPORT.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps({"pass": rep["pass"], "failed": rep["failed_gates"]}))


if __name__ == "__main__":
    main()
