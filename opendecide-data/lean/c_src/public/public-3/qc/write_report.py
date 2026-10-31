#!/usr/bin/env python3
"""Assemble qc/QC_REPORT.json for public-3 (independent checker, prep5, RUNBOOK blocker B4) from the per-gate results in
qc/ (each re-run on the CURRENT files by the scripts next to this one). pass = every required gate passes.
Required for public rows (C_DATA_SPEC 8, last paragraph; mixer final_blockers message): G1 (with the 3.H deny-list
program and the 7.4 input-path check), G5 (100-row dataset-level read per dataset), G6 (on our framings), G7, G10,
G12, G15, plus the sealed-suite check (sealed_nd/qc/sealed_check.py, run only). G13 runs elsewhere (orchestrator
counts-only) and is not part of this record; G18 applies to ordinal rows only (none here, checked).
The mixer binds this record to public3_rows_r1.jsonl and public3_reserve.jsonl by full sha256 (mixer.qc_binding)."""
import hashlib, json, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
P3 = HERE.parent
LEAN = P3.parents[2]
OUT = P3 / "out"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def j(name):
    return json.load(open(HERE / name))


def nrows(p):
    with open(p, "rb") as f:
        return sum(1 for _ in f)


def main():
    g1, g5, g6, g7, g10, g12, g12g, g15 = (j(x) for x in ("g1.json", "g5.json", "g6.json", "g7.json", "g10.json",
                                                         "g12.json", "g12_golden.json", "g15.json"))
    sealed = {}
    for s in sorted((HERE / "sealed").glob("*.summary.json")):
        x = json.load(open(s))
        sealed[s.name.split(".")[0] + ".jsonl"] = {"rows": x["rows"], "rows_hit": x["rows_hit"],
                                                   "rows_report_only": x["rows_report_only"],
                                                   "suite_sha256": x["suite_sha256"], "checker_sha256": x["checker_sha256"],
                                                   "input_sha256": x["input_sha256"]}
    sealed_pass = all(v["rows_hit"] == 0 and v["suite_sha256"] == "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68"
                      for v in sealed.values()) and len(sealed) == 6
    deny = json.load(open(HERE / "denylist/verdicts_fresh.json"))
    dcheck = (HERE / "denylist/check.stdout").read_text().strip().splitlines()[-6:]
    paths = (HERE / "denylist/paths.stdout").read_text().split()
    deny_pass = "\"hit\": 0" in "\n".join(dcheck) and "\"pass\": 5" in "\n".join(dcheck) and \
        all(t == "ok" for t in paths[0::2])
    rows = [json.loads(l) for f in ("public3_rows_r1.jsonl", "public3_reserve.jsonl") for l in open(OUT / f)]
    ordinal = sum(1 for r in rows if r["meta"].get("option_level"))
    gates = {
        "G1_provenance": {"pass": g1["pass"], "problems": g1["problems"], "rows": g1["rows"], "split": g1["split"],
                          "shape": g1["shape"],
                          "sources": {k: {kk: vv for kk, vv in v.items() if kk != "records"} |
                                      {"licence_records": {rn: {"sha256_match": r["sha256_match"],
                                                                "licence_string_saved": r["licence_string_saved"],
                                                                "live_reread": r["live"]} for rn, r in v["records"].items()}}
                                      for k, v in g1["sources"].items()},
                          "script": "qc/g1.py"},
        "G1_denylist_3H": {"pass": deny_pass, "program": "c_src/common/denylist.py (run, fresh build)",
                           "program_sha256": sha(LEAN / "c_src/common/denylist.py"),
                           "denylist_fresh_sha256": sha(HERE / "denylist/denylist_fresh.json"),
                           "query": "denylist/query_public3.json (5 datasets with names, datasets and declared parents)",
                           "query_sha256": sha(P3 / "denylist/query_public3.json"),
                           "verdicts": "qc/denylist/verdicts_fresh.json", "summary": dcheck[-1][-200:],
                           "input_paths_checked": len(paths) // 2, "input_paths_ok": sum(t == "ok" for t in paths[0::2])},
        "sealed_check": {"pass": sealed_pass, "checker": "sealed_nd/qc/sealed_check.py (run only, --fail-on-hit, "
                         "--structure-fields state,card,instructions,options on row files)", "files": sealed},
        "G5_blind_read": {k: v for k, v in g5.items() if k != "gate"},
        "G6_partial_input": {"pass": g6["pass"], "problems": g6["problems"], "rows": g6["rows"],
                             "yn_rows": g6["yn_rows"], "choice_rows": g6["choice_rows"], "results": g6["results"],
                             "rule": "accuracy <= chance + 2 pp per view x model pooled; per dataset > chance + 2 pp "
                                     "with one-sided binomial p < 0.01 fails",
                             "diagnosis": "every failing cell is c_pub_mams: the question / card names the aspect "
                                          "(category or term) and the asked polarity, and aspect-polarity priors leak "
                                          "(e.g. ACSA staff questions yes 62-72%, food-negative questions yes 31%); "
                                          "a question-only model scores 57-64% on 504 MAMS yes/no rows (chance 50%)",
                             "script": "qc/g6.py"},
        "G7_feature_z": {k: v for k, v in g7.items() if k != "gate"} | {"script": "qc/g7.py"},
        "G10_balance": {"pass": g10["pass"], "problems": g10["problems"],
                        "files": {k: {kk: vv for kk, vv in v.items() if kk != "longest_is_gold"} |
                                  {"longest_is_gold_dataset_pooled": {kk: vv for kk, vv in v["longest_is_gold"]["by"].items()
                                                                      if kk.endswith("|all")}}
                                  for k, v in g10["files"].items()}, "script": "qc/g10.py"},
        "G12_dedup": {k: v for k, v in g12.items() if k != "gate"} | {"script": "qc/g12.py",
                      "unused_records_vs_golden_train": {k: v for k, v in g12g.items() if k != "check"} |
                      {"script": "qc/g12_golden.py"}},
        "G15_loader": {k: v for k, v in g15.items() if k != "gate"} | {"script": "qc/g15.py (runs g15_check.main)"},
        "G13_decontamination": {"pass": None, "status": "not part of this record: run by the orchestrator's counts-only "
                                "G13 (mixer --decontam-drops), per the task"},
        "G18_ordinal": {"pass": ordinal == 0, "rows_with_option_level": ordinal,
                        "status": "n/a: no public ordinal rows in round 1 (spec 2.4)"},
    }
    gates["G12_dedup"]["pass"] = g12["pass"] and g12g["pass"]
    required = ["G1_provenance", "G1_denylist_3H", "sealed_check", "G5_blind_read", "G6_partial_input",
                "G7_feature_z", "G10_balance", "G12_dedup", "G15_loader", "G18_ordinal"]
    failed = [g for g in required if gates[g]["pass"] is not True]
    bound = {}
    for n in ("public3_rows_r1.jsonl", "public3_reserve.jsonl"):
        p = OUT / n
        bound[n] = {"sha256": sha(p), "rows": nrows(p), "bytes": p.stat().st_size, "path": f"c_src/public/public-3/out/{n}"}
    other = {str(p.relative_to(LEAN)): sha(p) for p in
             [OUT / "public3_mtdev.jsonl", OUT / "public3_split_3e.jsonl", OUT / "public3_templates.jsonl",
              OUT / "public3_record_claims.jsonl", OUT / "public3_g5_sample_ids.json", P3 / "manifest_public3.json",
              LEAN / "decoder_io.py", LEAN / "train_decoder.py", LEAN / "c_build/mixer.py",
              LEAN / "c_spec/C_DATA_SPEC.md", LEAN / "runs/q35_4b_c_r1.json"] + sorted(HERE.glob("*.py"))}
    rep = {
        "id": "public-3 QC_REPORT", "builder_checked": "c_src/public/public-3 (v1.1)",
        "checker": "independent checker (prep5 / endgame-prep-5, RUNBOOK blocker B4); did not build public-3; rows never "
                   "edited, relabelled or picked; the builder was not repaired",
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pass": not failed, "failed_gates": failed,
        "files": bound,
        "decision_needed": [x for g, x in (
            ("G5_blind_read", "G5: " + "; ".join(g5["problems"]) + " (c_pub_ghc rows go to the 3E fallback, F11, logged "
             "in the mixer report); c_pub_mams is at the bar (8/100)."),
            ("G6_partial_input", "G6: c_pub_mams yes/no and choice framings leak aspect-polarity priors through the "
             "question / card (question-only 57-64% vs 50%); spec: fix the framing (matched twins per aspect x asked "
             "polarity) or drop the framing; a builder change, not done here.")) if g in failed],
        "gates": gates, "required_gates": required, "other_file_sha256": other,
        "spec": "C_DATA_SPEC.md v4 section 8 (public rows: G1, G6 on our framings, G7, G10, G12, G13, G15, G5 read of "
                "100 rows per dataset) + 3.1 + 3.H; mixer.py final_blockers / qc_binding",
    }
    (HERE / "QC_REPORT.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps({"pass": rep["pass"], "failed_gates": failed, "files": {k: v["sha256"][:16] for k, v in bound.items()}}))


if __name__ == "__main__":
    main()
