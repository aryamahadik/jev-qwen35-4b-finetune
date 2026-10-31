#!/usr/bin/env python3
"""Assemble qc/QC_REPORT.json for public-3, recheck after repair round 1 (PREREG A29 a; independent recheck: this
checker did not write the builder or the repair). Spec 8 exactly as written. Required for public rows (spec 8 last
paragraph; mixer final_blockers): G1 (+ 3.1 v2 unused records, 3.H deny-list program, 7.4 input paths), G5 (100-row
dataset-level read per dataset, flag-only), G6 (on our framings; accuracy <= chance + 2 pp, point estimate, no
p-value), G7, G10 (spec cells), G12, G15, sealed check; G18 for ordinal rows (none). G13 is the orchestrator's
counts-only run. G11 is not in spec 8's public-row list: computed on request, reported, not gating (a gate the spec
does not list would be a checker add-on, PREREG A29). The mixer binds this record by full sha256 (mixer.qc_binding)."""
import hashlib, json, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
P3 = HERE.parent
LEAN = P3.parents[2]
OUT = P3 / "out"
SUITE = "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def j(n):
    return json.load(open(HERE / n))


def nrows(p):
    return sum(1 for _ in open(p, "rb"))


def main():
    g1, gx, g5, g5b, g6, g6a, g7, g7a, g10, g11, g12, g12g, g15 = (j(x) for x in (
        "g1.json", "g1_xparse.json", "g5.json", "g5_second_mams.json", "g6.json", "g6_altgroups.json", "g7.json",
        "g7_nmin1.json", "g10.json", "g11.json", "g12.json", "g12_golden.json", "g15.json"))
    sealed = {}
    for s in sorted((HERE / "sealed").glob("*.summary.json")):
        x = json.load(open(s))
        if not s.name.startswith(("public3_", "manifest_public3")):
            continue
        sealed[s.name.replace(".summary.json", "")] = {k: x[k] for k in ("rows", "rows_hit", "rows_report_only",
                                                                         "suite_sha256", "checker_sha256", "input_sha256")}
    want = {"public3_rows_r1", "public3_reserve", "public3_mtdev", "public3_templates", "public3_split_3e",
            "public3_record_claims", "public3_class_allocation", "public3_g5_sample_ids", "manifest_public3"}
    on_disk = {"public3_rows_r1": OUT / "public3_rows_r1.jsonl", "public3_reserve": OUT / "public3_reserve.jsonl",
               "public3_mtdev": OUT / "public3_mtdev.jsonl", "public3_templates": OUT / "public3_templates.jsonl",
               "public3_split_3e": OUT / "public3_split_3e.jsonl", "public3_record_claims": OUT / "public3_record_claims.jsonl"}
    sealed_pass = set(sealed) == want and all(v["rows_hit"] == 0 and v["suite_sha256"] == SUITE for v in sealed.values()) \
        and all(sealed[k]["input_sha256"] == sha(p) for k, p in on_disk.items())
    dcheck = (HERE / "denylist/check.stdout").read_text().strip().splitlines()
    paths = (HERE / "denylist/paths.stdout").read_text().split()
    summ = next(l for l in dcheck if "check public3_recheck1" in l)
    deny_pass = '"hit": 0' in summ and '"pass": 5' in summ and all(t == "ok" for t in paths[0::2])
    rows = [json.loads(l) for f in ("public3_rows_r1.jsonl", "public3_reserve.jsonl", "public3_mtdev.jsonl")
            for l in open(OUT / f)]
    ordinal = sum(1 for r in rows if r["meta"].get("option_level"))
    unused_pass = g12g["pass"] and all(v["used_total"] == 0 for v in g12g["files"].values())
    card = g6a["card_id"]
    g6_pass = g6["pass"] and card["pass"]
    g5_pass = g5["pass"] and g5b["pass"]
    gates = {
        "G1_provenance": {"pass": g1["pass"] and gx["pass"], "problems": g1["problems"] + gx["problems"],
                          "rows": g1["rows"], "split": g1["split"], "shape": g1["shape"],
                          "sources": {k: {kk: vv for kk, vv in v.items() if kk != "records"} |
                                      {"licence_records": {rn: {"sha256_match": r["sha256_match"],
                                                                "licence_string_saved": r["licence_string_saved"],
                                                                "live_reread": r["live"]} for rn, r in v["records"].items()}}
                                      for k, v in g1["sources"].items()},
                          "cross_parse_formats2": gx["per_scheme"],
                          "scripts": "qc/g1.py (reviewed vs spec 3.1 / 8 G1), qc/g1_xparse.py (new: text, labels and "
                                     "official train split vs formats-2's independent parse)"},
        "G1_unused_records_3_1_v2": {"pass": unused_pass, "files": g12g["files"], "control": g12g["control"],
                                     "golden_rows": g12g["golden_rows"], "golden_sources": g12g["golden_sources"],
                                     "note": "0 used records in rows_r1, reserve AND mtdev (spec: never a new row, never a "
                                             "mix-tuning-dev item); Wikipedia passage dedup (3.1 v2) n/a: no Wikipedia set "
                                             "here; EDOS records carry no in_hatexplain_or_sbf / in_golden_train flag",
                                     "script": "qc/g12_golden.py"},
        "G1_denylist_3H": {"pass": deny_pass, "program": "c_src/common/denylist.py (run, fresh build)",
                           "program_sha256": sha(LEAN / "c_src/common/denylist.py"),
                           "denylist_fresh_sha256": sha(HERE / "denylist/denylist_fresh.json"),
                           "query_sha256": sha(P3 / "denylist/query_public3.json"),
                           "summary": summ[-230:], "input_paths_checked": len(paths) // 2,
                           "input_paths_ok": sum(t == "ok" for t in paths[0::2])},
        "sealed_check": {"pass": sealed_pass, "checker": "sealed_nd/qc/sealed_check.py (run only, --fail-on-hit; "
                         "--structure-fields state,card,instructions,options on row files)", "files": sealed},
        "G5_blind_read": {"pass": g5_pass, "first_sample": {k: v for k, v in g5.items() if k != "gate"},
                          "second_sample_mams": {k: v for k, v in g5b.items() if k != "gate"},
                          "reader": "independent Claude session (not a public-3 author), flag-only; rows rendered by "
                                    "decoder_io.user_msg in the C round-1 style (cygnet, schema_branch_mark) under a "
                                    "seeded option permutation; verdict logs qc/g5_flags.jsonl, "
                                    "qc/g5_second_mams_flags.jsonl",
                          "note": "MAMS 6/100 clearly wrong in each of two independent samples (12/200 = 6.0%, bar > 8%); "
                                  "every flagged MAMS gold equals the MAMS label (cross-parse vs formats-2 equal): "
                                  "dataset noise, not a builder bug. XED 0, Sarcasm 0, EDOS 0 clearly wrong."},
        "G6_partial_input": {"pass": g6_pass,
                             "rule": "spec 8 G6 exactly: accuracy <= chance + 2 pp, point estimate, no p-value; every "
                                     "view x model, pooled, per dataset on pooled CV and per dataset own CV",
                             "grouped_by_card_id": {"pass": card["pass"], "problems": card["problems"],
                                                    "worst_own_cv": card["worst_own_cv"],
                                                    "worst_pooled_per_dataset": card["worst_pooled_per_dataset"],
                                                    "cells": card["cells"],
                                                    "why": "PREREG A19 'grouped-by-card CV'; every family checker's "
                                                           "GroupKFold(meta.card_id); keeps v2.0 matched sets in one fold"},
                             "grouped_by_group_id": {"pass": g6["pass"], "problems": g6["problems"], "rows": g6["rows"],
                                                     "results": g6["results"], "per_dataset_own_cv": g6["per_dataset_own_cv"],
                                                     "note": "qc/g6.py (reviewed): record groups split matched sets across "
                                                             "folds, so many cells sit far below chance (an artefact)"},
                             "diagnostic_grouped_by_match_set": {
                                 "pass": g6a["match_set"]["pass"], "problems": g6a["match_set"]["problems"],
                                 "worst_own_cv": g6a["match_set"]["worst_own_cv"],
                                 "worst_pooled_per_dataset": g6a["match_set"]["worst_pooled_per_dataset"],
                                 "note": "extra robustness run by this checker, not the spec's grouping: one cell over "
                                         "the bar, Sarcasm choice view (d) hgb on pooled-trained CV, +5.7 pp on 228 rows; "
                                         "the same view on Sarcasm-only CV is +1.75 pp, +0.88 pp grouped by card; all 101 "
                                         "Sarcasm choice sets are complete, gold length rank and gold position are each "
                                         "a permutation within every set and view-(d) metadata is identical within every "
                                         "set; G7 on the same metadata x option-kind features passes (min p 0.016). "
                                         "Reported for the orchestrator; not gating."},
                             "scripts": "qc/g6.py, qc/g6_altgroups.py"},
        "G7_feature_z": {"pass": g7["pass"] and g7a["pass"],
                         "n_min_20": {k: v for k, v in g7.items() if k != "gate"},
                         "every_feature_n_min_1": {k: v for k, v in g7a.items() if k not in ("gate", "fails")},
                         "note": "spec 8 G7 tests every feature; run both with qc/g7.py's n >= 20 convention and with "
                                 "every feature (more Bonferroni tests); no feature fails either way",
                         "script": "qc/g7.py"},
        "G10_balance": {"pass": g10["pass"], "problems": g10["problems"],
                        "files": {k: {kk: vv for kk, vv in v.items() if kk != "longest_is_gold"} |
                                  {"longest_is_gold_dataset_pooled": {kk: vv for kk, vv in v["longest_is_gold"]["by"].items()
                                                                      if kk.endswith("|all")}}
                                  for k, v in g10["files"].items()},
                        "note": "yes rate per dataset x wording x bin x negation cell, all cells, +/- 2 pp (no small-cell "
                                "rule); gold position chi-square p > 0.01 per option bucket; longest-is-gold within 2 pp "
                                "per dataset; no abstain options shown", "script": "qc/g10.py"},
        "G12_dedup": {k: v for k, v in g12.items() if k != "gate"} | {"script": "qc/g12.py"},
        "G15_loader": {k: v for k, v in g15.items() if k != "gate"} |
                      {"rendered_prompts_read": "500 rendered prompts read in the G5 read (all four datasets); no "
                                                "rendering defect seen", "script": "qc/g15.py (runs g15_check.main)"},
        "G18_ordinal": {"pass": ordinal == 0, "rows_with_option_level": ordinal,
                        "status": "n/a: no public ordinal rows in round 1 (spec 2.4); checked on rows_r1, reserve, mtdev"},
        "G13_decontamination": {"pass": None, "status": "not part of this record: the orchestrator's counts-only G13"},
        "G11_diversity_info": {"gating": False, "pass_as_computed": g11["pass"], "problems": g11["problems"],
                               "template": g11["template"], "vs_golden": g11["vs_golden"], "n_a": g11["n_a"],
                               "why_not_gating": "spec 8 lists the public-row gates (G1, G6, G7, G10, G12, G13, G15, G5; "
                                                 "G18 for level-scale replay); G11 is not among them, and its 2.1 counts "
                                                 "and seed rules are own-family rules. Operationalisation here is this "
                                                 "checker's (qc/g11.py), reported for information only."},
    }
    gates["G12_dedup"]["pass"] = g12["pass"]
    required = ["G1_provenance", "G1_unused_records_3_1_v2", "G1_denylist_3H", "sealed_check", "G5_blind_read",
                "G6_partial_input", "G7_feature_z", "G10_balance", "G12_dedup", "G15_loader", "G18_ordinal"]
    failed = [g for g in required if gates[g]["pass"] is not True]
    bound = {}
    for n in ("public3_rows_r1.jsonl", "public3_reserve.jsonl"):
        p = OUT / n
        bound[n] = {"sha256": sha(p), "rows": nrows(p), "bytes": p.stat().st_size, "path": f"c_src/public/public-3/out/{n}"}
    other = {str(p.relative_to(LEAN)): sha(p) for p in
             [OUT / "public3_mtdev.jsonl", OUT / "public3_split_3e.jsonl", OUT / "public3_templates.jsonl",
              OUT / "public3_record_claims.jsonl", OUT / "public3_class_allocation.json", OUT / "public3_g5_sample_ids.json",
              P3 / "manifest_public3.json", P3 / "build_rows.py", P3 / "assemble.py", P3 / "lib/common3.py",
              LEAN / "decoder_io.py", LEAN / "train_decoder.py", LEAN / "c_build/mixer.py",
              LEAN / "c_spec/C_DATA_SPEC.md", LEAN / "runs/q35_4b_c_r1.json"] + sorted(HERE.glob("*.py"))}
    rep = {
        "id": "public-3 QC_REPORT (recheck after repair r1)",
        "builder_checked": "c_src/public/public-3 v2.0 (repair r1, PREREG A29 a; GHC dropped by spec 8 G5)",
        "checker": "independent recheck (recheck:public-3); did not write the builder or the repair; rows never edited, "
                   "relabelled or picked; no gate loosened (spec 8 exactly; no p-value add-on, no small-cell rule)",
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pass": not failed, "failed_gates": failed, "files": bound,
        "decision_needed": [], "gates": gates, "required_gates": required, "other_file_sha256": other,
        "spec": "C_DATA_SPEC.md v4 section 8 (public rows: G1, G6 on our framings, G7, G10, G12, G13, G15, G5 read of "
                "100 rows per dataset) + 3.1 (v2 unused records) + 3.H; PREREG A29; mixer.py final_blockers / qc_binding",
    }
    (HERE / "QC_REPORT.json").write_text(json.dumps(rep, indent=1, default=float))
    sys.path.insert(0, str(LEAN / "c_build"))
    import mixer
    probs = mixer.qc_binding(json.load(open(HERE / "QC_REPORT.json")), {n: OUT / n for n in bound})
    print(json.dumps({"pass": rep["pass"], "failed_gates": failed, "qc_binding_problems": probs,
                      "files": {k: v["sha256"][:16] for k, v in bound.items()}}))


if __name__ == "__main__":
    main()
