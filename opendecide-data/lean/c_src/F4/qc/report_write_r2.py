"""Repair round 2 QC_REPORT writer. Starts from the round-1 repair report (tmp/repair/r2/QC_REPORT.pre_r2.json) and
replaces every gate block with the gate outputs re-run on the r2 regenerated sets (same checker scripts), plus the r2
evidence (literal decile, G8 cue-free null, padding independence). Counts and verdicts only; no row text."""
import json, time, glob, hashlib
import qc_lib as L

Q = L.QC; F4 = Q.parent
ld = lambda f: json.load(open(Q / f))
lj = lambda p: json.load(open(F4 / p))
base = lj("tmp/repair/r2/QC_REPORT.pre_r2.json")
g6 = ld("g6_qc_sample.json"); g6x = ld("g6_qc_sample_ext.json")
g7c = ld("g7_candidates_r1.json"); g7q = ld("g7_qc_sample.json")
g8 = ld("g8_candidates_r1.json"); g8c = ld("g8_candidates_r1_control.json")
g8n = lj("tmp/repair/r2/g8_null_candidates_r1.json")
g10 = ld("g10_candidates_r1.json"); g10q = ld("g10_qc_sample.json")
g11 = ld("g11_candidates_r1.json"); g12 = ld("g12.json")
g15c = ld("g15_g18_candidates_r1.json"); g15q = ld("g15_g18_qc_sample.json")
fsc = json.loads(open(Q / "fewshot_cand.log").read().strip().splitlines()[-1])
g10o = lj("tmp/repair/g10_orig_candidates_r1.json")
st = lj("tmp/repair/r2/r2_stats.json")
bound = lj("tmp/repair/r2/decile_bound_candidates_r1.json")
chk = {c["check"]: c for c in g10["checks"]}; chkq = {c["check"]: c for c in g10q["checks"]}
chko = {c["check"]: c for c in g10o["checks"]}
sb = lj("solverB/mismatch.json")
g4 = {s: lj(f"logs/g4_{s}.json") for s in ("cand", "qc", "dev")}
gates_b = {s: lj(f"logs/gates_{s}.json") for s in ("cand", "qc", "dev")}
quota = {s: lj(f"logs/quota_{s}.json") for s in ("cand", "qc", "dev")}
sealed = {}
for f in sorted(glob.glob(str(F4 / "logs/sealed_*.sealedqc.jsonl.summary.json"))):
    s = json.load(open(f)); sealed[s["input"].split("/")[-1]] = {"rows": s["rows"], "rows_hit": s["rows_hit"],
                                                                   "parse_errors": s["parse_errors"], "input_sha256": s["input_sha256"][:16]}
sha = lambda p: hashlib.sha256(open(F4 / p, "rb").read()).hexdigest()[:16]
dec = lambda c: {k: c[k]["chi2_p"] for k in c if k.startswith("decisive_decile_uniform")}
pre = base["gates"]

gates = {}
gates["G5"] = {**pre["G5"], "pass": None, "status": "pending: fresh read needed on the r2 rows",
               "r2_note": "r2 regenerated every unit (rule padding, S3 table growth and placement change the rows), so the "
                          "300-row reads in qc/g5.json, g5r2.json and g5r2b.json were made on earlier rows. Labels come "
                          "from the unchanged logic core and pass G2 / G3 / G4 at 100% on the r2 rows, but a fresh "
                          "seeded 300-row G5 read by a session that did not author the generator is still owed; this "
                          "builder session wrote the r2 changes and does not read it"}
gates["G6"] = {"pass": g6["pass"], "file": "qc/g6_qc_sample.json (+ g6_qc_sample_ext.json, report-only)",
               "rows": g6["rows"], "folds": g6["folds"],
               "yes_no_max_acc": max(g6["yes_no"][v][m] for v in ("a_question", "c_card", "d_meta") for m in ("lr", "gbt")),
               "yes_no_chance": 0.5, "choice_chance": round(g6["choice"]["chance"], 4),
               "choice_max_acc": round(max(g6["choice"][v][m]["acc"] for v in ("a_question", "b_options", "c_card", "d_meta")
                                           for m in ("lr", "gbt")), 4),
               "extended_meta_report_only": {"pass": g6x["pass"], "choice_d_meta_max":
                                             round(max(g6x["choice"]["d_meta"][m]["acc"] for m in ("lr", "gbt")), 4)},
               "before_r2": {k: pre["G6"][k] for k in ("yes_no_max_acc", "choice_max_acc")}}
gates["G7"] = {"pass": g7c["pass"] and g7q["pass"], "file": "qc/g7_candidates_r1.json, qc/g7_qc_sample.json",
               "bonferroni_p": g7c["bonferroni_p"], "n_tests": {"candidates_r1": g7c["n_tests"], "qc_sample": g7q["n_tests"]},
               **{nm: {"yes_no_raw_fails": g["n_yes_no_raw_fails"], "yes_no_card_adjusted_fails": g["n_yes_no_card_adjusted_fails"],
                       "choice_fails": g["n_choice_fails"]} for nm, g in (("candidates_r1", g7c), ("qc_sample", g7q))}}
nul = g8n["null_global"]; nwc = g8n["null_within_card"]
gates["G8"] = {"pass": g8["pass"], "infeasible_as_specified": True, "proof": "tmp/repair/INFEASIBLE_G8.md",
               "file": "qc/g8_candidates_r1.json (+ g8_candidates_r1_control.json, tmp/repair/r2/g8_null_candidates_r1.json)",
               "rule": "< 10%", "grouped_by_card_share": g8["grouped_by_card"]["predictable_share"],
               "grouped_yes_no": g8["grouped_by_card"]["yes_no"]["predictable_share"],
               "grouped_choice": g8["grouped_by_card"]["choice"]["predictable_share"],
               "instance_level_share": g8["instance_level"]["predictable_share"],
               "heldout_acc_grouped": {"yes_no": g8["grouped_by_card"]["yes_no"]["mean_heldout_acc"],
                                       "choice": g8["grouped_by_card"]["choice"]["mean_heldout_acc"]},
               "checker_control_within_card": g8c["grouped_by_card"]["predictable_share"],
               "cue_free_null_shares": {s: v["share"] for s, v in nul.items()},
               "cue_free_null_summary": g8n["null_global_summary"],
               "within_card_null_shares": {s: v["share"] for s, v in nwc.items()},
               "null_at_G0_45pct_yes_no_floor": {s: v["share"] for s, v in g8n["null_global_yes_no_45pct"].items()},
               "real_by_sampler": g8n["real"]["by_sampler"],
               "before_r2": pre["G8"]["grouped_by_card_share"]}
sc = st["cand"]; sq = st["qc"]
gates["G10"] = {"pass": g10["pass"], "file": "qc/g10_candidates_r1.json (+ g10_qc_sample.json, information)",
                "pool_fails": g10["pool_fails"], "target_fails": g10["target_fails"], "bin_axis": g10["bin_axis"],
                "qc_sample_target_fails_info": g10q["target_fails"], "qc_sample_pool_fails_info": g10q["pool_fails"],
                "decisive_decile_statistic": "LITERAL (G0 8): floor(10 L / n), L = slot of the last decisive statement "
                                             "in the measured block of n statements (sidecar decisive_decile)",
                "decisive_decile_chi2_p": dec(chk), "decisive_decile_chi2_p_qc_sample_info": dec(chkq),
                "decisive_decile_chi2_p_original_checker_script": dec(chko),
                "pit_statistic_info": {k: v["pit_chi2_p_info"] for k, v in sc["decile_cells"].items() if v["n"] >= 50},
                "planned_decile_realised": {"candidates_r1": sc["planned_decile_realised"],
                                            "qc_sample": sq["planned_decile_realised"]},
                "few_shot_cards": {"detected": chk["few_shot_cards_5_10pct"]["few_shot_cards"],
                                   "share": chk["few_shot_cards_5_10pct"]["share"],
                                   "detected_by_original_checker_regex": chko["few_shot_cards_5_10pct"]["few_shot_cards"],
                                   "solver_b_check": {k: fsc[k] for k in ("few_shot_cards_planned", "few_shot_cards_rendered",
                                                                          "rows_with_block", "examples", "agree", "answers")}},
                "HANS_CH_claim_verbatim_option": {k: chk["HANS_CH-claim_verbatim_option_is_gold_at_chance"].get(k)
                                                  for k in ("pass", "rows", "gold_hits", "expected", "binom_p")},
                "before_r2_target_fails_literal": "all per-sampler, per-label and facts / rules block cells (r1 shipped a "
                                                  "PIT in decisive_decile; the literal decile failed, tmp/repair/decile_literal.json)"}
gates["G11"] = {"pass": g11["pass"], "file": "qc/g11_candidates_r1.json", "pass_parts": g11["pass_parts"],
                "surface_template_max_share_pct": g11["surface_template"]["max_share_pct"],
                "seeds_rouge_l_max": {k: v["max"] for k, v in g11["claude_seeds_rouge_l"].items()},
                "corpus_metrics": g11["corpus_metrics"]}
gates["G12"] = {"pass": g12["pass"], "file": "qc/g12.json", "files": g12["files"], "cross_file": g12["cross_file"]}
gates["G15"] = {"pass": g15c["G15_pass"] and g15q["G15_pass"], "file": "qc/g15_g18_candidates_r1.json, qc/g15_g18_qc_sample.json",
                **{nm: {k: g[k] for k in ("loader_check_fail", "roundtrip_gold_fail", "relations_split_call_id", "units_gt3",
                                          "units_long_gt2", "tokens")} for nm, g in (("candidates_r1", g15c), ("qc_sample", g15q))}}
gates["G18"] = {"pass": g15c["G18"]["pass"] and g15q["G18"]["pass"], "applies": False,
                "ordinal_rows": g15c["G18"]["ordinal_rows"] + g15q["G18"]["ordinal_rows"]}
builder = {
 "G3_solver_b": {"rows_checked": sb["rows_checked"], "agree": sb["agree"], "mismatches": sb["n_mismatches"],
                 "per_file": sb["per_file"], "file": "solverB/mismatch.json, solverB/run_final.log"},
 "G4": {s: {"n_fail": g4[s]["n_fail"], "file": f"logs/g4_{s}.json"} for s in g4},
 "gates_G15_lengths": {s: {k: gates_b[s][k] for k in ("rows", "loader_check_pass", "len_median", "len_max", "max_unit_rows", "pass")}
                       for s in gates_b},
 "quota_fails": {s: quota[s]["fails"] for s in quota},
 "sealed_check": {"files": len(sealed), "rows_hit_total": sum(v["rows_hit"] for v in sealed.values()),
                  "parse_errors_total": sum(v["parse_errors"] for v in sealed.values()), "per_file": sealed},
 "inputs_sha256_16": {p: sha(p) for p in ("out/candidates_r1.jsonl", "out/qc_sample.jsonl", "out/mixdev_S5.jsonl")},
 "rule_padding": {nm: {k: s_[k] for k in ("n_rules", "n_rules_max", "share_rows_ge_10_rules", "ge_10_rules_by_answer_class",
                                          "ge_10_rules_vs_answer_class_chi2_p")} for nm, s_ in (("candidates_r1", sc), ("qc_sample", sq))},
}
dlit = gates["G10"]["decisive_decile_chi2_p"]
dlit_fail = sorted(k for k, p in dlit.items() if p <= 0.01)
qc_dlit_fail = sorted(k for k, p in gates["G10"]["decisive_decile_chi2_p_qc_sample_info"].items() if p <= 0.01)
r1find = {f["id"]: f for f in base["findings"]}
findings = [r1find[i] for i in ("F4-QC-1", "F4-QC-2", "F4-QC-3", "F4-QC-7")]
findings.append({
 "id": "F4-QC-4", "gate": "G10", "status": "fixed (literal statistic)" if not dlit_fail else "open",
 "r1_state": "r1 shipped a PIT over the feasible slots in decisive_decile; read literally (G0 8: the decile of the last "
             "decisive statement among the block's statements) every per-sampler, per-label and facts / rules block cell "
             "failed (tmp/repair/decile_literal.json)",
 "r2_fix": ["gen/render_f4.py _placed: the last decisive statement goes to a feasible slot whose LITERAL decile "
            "floor(10 L / n) is the unit's target (nearest feasible decile otherwise); placement randomness comes from a "
            "private generator seeded by one draw, so the target changes nothing else in the row",
            "gen/render_f4.py _interleave_place: the S1 interleaved layout (5.1, half of S1 prose rows) is ONE block "
            "('mixed'); its facts and rules are re-placed in the merged order (G0 8 'per sampler x layout')",
            "gen/decile_targets.py + gen/build.py (two passes): pass 1 builds every unit with an untargeted slot; the "
            "solver assigns one target decile per unit that minimises the summed chi-square over the G10 cells (sampler, "
            "label tag, sampler x measured block) given each row's reachable deciles; pass 2 rebuilds with the targets. "
            "Rows, structures, labels and lengths are identical between the passes; only statement order changes",
            "gen/units.py _pad_rules: a rules block of < 10 rules can never reach decile 9 and, with >= 2 decisive rules, "
            "never decile 0. On 85% of eligible units, drawn independently of the label, the record's rules are filled "
            "with irrelevant rules (fresh predicates, outside c's component) up to 10-12 (G0 2.1 cap 12)",
            "gen/units.py: S3 records carry >= 5 near-miss entities of c's type (tables of 2-5 rows reach only a few "
            "deciles; n = 2 reaches {0, 5})"],
 "evidence": {"literal_cells_candidates_r1": dlit, "literal_fails_candidates_r1": dlit_fail,
              "literal_fails_qc_sample_info": qc_dlit_fail,
              "planned_decile_realised": gates["G10"]["planned_decile_realised"],
              "pass1_bound_file": "tmp/repair/r2/decile_bound_candidates_r1.json (exact min chi-square over all placements)",
              "padding_vs_answer_class_chi2_p": {"candidates_r1": sc["ge_10_rules_vs_answer_class_chi2_p"],
                                                 "qc_sample": sq["ge_10_rules_vs_answer_class_chi2_p"]}}})
findings.append({
 "id": "F4-QC-5", "gate": "G8", "status": "infeasible as specified (proof: tmp/repair/INFEASIBLE_G8.md)",
 "evidence": {"real": gates["G8"]["grouped_by_card_share"], "cue_free_nulls": gates["G8"]["cue_free_null_shares"],
              "null_at_45pct_yes_no": gates["G8"]["null_at_G0_45pct_yes_no_floor"],
              "heldout_acc": gates["G8"]["heldout_acc_grouped"]},
 "note": (f"labels with no information give {g8n['null_global_summary']['min']}-{g8n['null_global_summary']['max']} "
          f"(mean {g8n['null_global_summary']['mean']}) on the same rows and code; the real share "
          f"{gates['G8']['grouped_by_card_share']} is " + ("below" if gates['G8']['grouped_by_card_share'] <=
          g8n['null_global_summary']['mean'] else "above") + " the cue-free mean; ruling requested (judge G8 against "
          "the null of the same rows)")})
findings.append(r1find["F4-QC-6"])
deviations = [
 "G0 5.7 aims CH-claim carriers / inert sentences at c (the gold claim); since r1 they aim at a claim option drawn "
 "uniformly from the shown options (C_DATA_SPEC G7 'no feature may predict gold' taken as binding over 5.7 on CH-claim rows)",
 "decisive-position conventions (builder; G0 8 does not fix them): the measured block is the block holding the most "
 "decisive statements (ties: table, facts, attrib, mixed, rules) and 'mixed' is the S1 interleaved section; decisive "
 "sets follow r1 (OW derivations: solver A's minimal proof, rules included; OW OPEN and CW rows: the sampler chain's "
 "stated leaves and failing premises, chain rules not counted). The sidecar keeps decisive_pos for every block, "
 "decisive_block, layout and decisive_reach, so another convention can be re-checked without regenerating",
 "qc/g10.py (checker script) edited by the builder: r1 added the few-shot shape 'Record: ... Question: ...?' and the "
 "sampler x block cells; r2 takes the cell's block from the sidecar decisive_block (needed for 'mixed'). Originals: "
 "tmp/repair/g10.checker_orig.py, tmp/repair/r2/g10.pre_r2.py",
 "rule padding (r2) adds 6-9 irrelevant rules to most rich, short and lean yes/no / CH-2 / CH-3 records; they share I2's "
 "logical form but are sampler-built structure (G0 5.7: structure is not the counted inert sentence), never sit on the "
 "card, and use a type other than c's when the card has one. Not padded: inverted cards, lean CH-claim rows, cards that "
 "print every rule, second shrink retries (length cap)",
 "G5 evidence predates r2 (pending a fresh separate-session read on the r2 rows; see gates.G5)",
 "the r1 deviations on the dev depth sweep (50/50 yes/no) and on G5 r2 reading are unchanged",
]
failing = [g for g, v in gates.items() if v.get("pass") is False]
pending = [g for g, v in gates.items() if v.get("pass") is None]
rep = {"family": "F4", "round": 1, "report": "QC_REPORT",
       "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "repair": {"round": 2, "by": "F4 builder (repair round 2 of the gates listed failing after r1: G8, G10); gates "
                                     "re-run with the checker's own scripts on the regenerated sets",
                  "previous_report": "tmp/repair/r2/QC_REPORT.pre_r2.json", "previous_failing_gates": base["failing_gates"],
                  "r1_report": "tmp/repair/QC_REPORT.pre_repair.json"},
       "inputs": base["inputs"], "g5": base["g5"], "gates": gates, "builder_gates": builder,
       "failing_gates": failing, "pending_gates": pending,
       "infeasible_as_specified": {"G8": "tmp/repair/INFEASIBLE_G8.md"},
       "failing_reason": {g: ("infeasible as specified: labels with no information fail the < 10% bar on the same rows "
                              "(tmp/repair/INFEASIBLE_G8.md); ruling requested" if g == "G8" else "see gates." + g)
                          for g in failing},
       "findings": findings, "deviations": deviations}
json.dump(rep, open(Q / "QC_REPORT.json", "w"), indent=1)
print(json.dumps({"failing": failing, "pending": pending, "G10_literal_fails": dlit_fail,
                  "qc_literal_fails_info": qc_dlit_fail}))
