"""Writes qc/QC_REPORT.json for public-2 (RUNBOOK blocker B4) from the independent gate runs in qc/gates/.
pass is true only if every gate required for public rows passes (C_DATA_SPEC v4 8, last line: G1, G5, G6, G7, G10,
G12, G15; G13 is run by the orchestrator, counts-only) plus the sealed_check run, the deny-list / 3.1 checks and the
label round-trip. Every gate file must have been computed on the files now on disk (full sha256 match), else it is
stale and fails. mixer.py binds rows_r1.jsonl and reserve_r1.jsonl (PUBLIC_FILES / PUBLIC_RESERVE)."""
import glob
import json
import re
import time
from pathlib import Path

from qclib import FILES, GATES, OUT, QC, file_shas, load, progress, sha256_file

A15_SUITE_SHA = "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68"
REQUIRED = ["G1", "rules31_golden_train_dedup", "labels_roundtrip", "sealed_check", "G5", "G6", "G7", "G10", "G12",
            "G15"]


def sealed_gate():
    log = (QC / "logs" / "sealed_qc.log").read_text()
    exits = dict(re.findall(r"^(\w+) exit=(\d+)$", log, re.M))
    per, ok = {}, True
    for p in sorted(glob.glob(str(QC / "sealedqc" / "*.summary.json"))):
        s = json.load(open(p))
        name = Path(p).name.replace(".summary.json", "")
        src = OUT / f"{name}.jsonl"
        cur = sha256_file(src)
        per[name] = {"rows": s.get("rows"), "rows_hit": s.get("rows_hit"), "rows_report_only": s.get("rows_report_only"),
                     "exit": int(exits.get(name, -1)), "checked_file_is_current": s.get("input_sha256") == cur}
        ok &= (per[name]["exit"] == 0 and s.get("rows_hit") == 0 and s.get("suite_sha256") == A15_SUITE_SHA
               and per[name]["checked_file_is_current"])
    s0 = json.load(open(glob.glob(str(QC / "sealedqc" / "rows_r1.summary.json"))[0]))
    return {"gate": "sealed_check", "pass": ok and len(per) == 7,
            "numbers": {"files": per, "suite_sha256": s0.get("suite_sha256"), "suite_is_A15": s0.get("suite_sha256") == A15_SUITE_SHA,
                        "checker_sha256": s0.get("checker_sha256"),
                        "how": "sealed_nd/qc/sealed_check.py RUN (never opened) by qc/run_sealed_qc.sh on all 7 out files"}}


def main():
    shas = file_shas()
    gates, failed, stale = {}, [], []
    for name in REQUIRED:
        if name == "sealed_check":
            g = sealed_gate()
            gpath = None
        else:
            gpath = GATES / f"{name}.json"
            g = json.load(open(gpath))
            if g.get("files_sha256") != shas:
                stale.append(name)
        ent = {"pass": bool(g["pass"]) and name not in stale}
        if gpath:
            ent["record"] = f"qc/gates/{name}.json"
            ent["record_sha256"] = sha256_file(gpath)
            ent["computed_utc"] = g.get("utc")
        gates[name] = ent | {"summary": summarise(name, g)}
        if not ent["pass"]:
            failed.append(name)
    data = {fn: load(fn) for fn in FILES}
    rep = {
        "builder": "public-2",
        "checker": "independent QC, workflow endgame-prep-5 (RUNBOOK section 0 blocker B4); not a public-2 author; "
                   "no row was edited, relabelled, dropped or picked",
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "spec": "C_DATA_SPEC.md v4 section 8 (public rows pass G1, G6 on our framings, G7, G10, G12, G13, G15 and a G5 "
                "read of 100 rows per dataset), 3.1 / 3.H rules, LICENCE_REGISTER.md section 1 rows 7, 8, 11, 12a, 12b",
        "pass": not failed,
        "failed_gates": failed,
        "stale_gate_records": stale,
        "files": {f"{fn}.jsonl": {"path": f"c_src/public/public-2/out/{fn}.jsonl", "sha256": shas[f"{fn}.jsonl"],
                                  "rows": len(data[fn]),
                                  "bound_by_mixer": fn in ("rows_r1", "reserve_r1")} for fn in FILES},
        "gates": gates,
        "not_run_here": {
            "G13": "decontamination counts-only run by the orchestrator before the freeze (spec 7; incl. the TabFact "
                   "table-hash check 7.2 #9 on out/table_hashes.jsonl); not part of this pass",
            "G8": "not in the spec 8 gate list for public rows",
            "G11": "not in the spec 8 gate list for public rows",
            "G9": "crowd scoring not applied to public rows in round 1 (A16: D2 not adopted)"},
        "interpretations_flagged_for_orchestrator": [
            "G6: public-2 has 4,028 final rows of our framings (< 5,000); gated pooled over all public-2 rows at "
            "chance + 2 pp; per dataset a view fails at > chance + 2 pp AND binomial p < 0.01 (point estimates reported)",
            "G10: a wording x bin x k_all cell of odd size < 25 cannot reach 50 +/- 2 pp; such a cell passes only at "
            "the closest reachable rate (|yes - n/2| = 0.5) and is listed; every other cell is held to 50 +/- 2 pp",
            "G12: near-dup text = question + state + options (instruction lines shared by >= 20 rows, i.e. the UCI DEX "
            "model / template text, left out like a card); the full-text count is reported (52 pairs, all UCI choice "
            "rows with different records)",
            "G7: both directions tested, Bonferroni over the features of each test set (per dataset and pooled; rows "
            "and rows + reserve)"],
        "checker_scripts_sha256": {Path(p).name: sha256_file(p) for p in sorted(glob.glob(str(QC / "*.py")))
                                   + [str(QC / "run_sealed_qc.sh")]},
    }
    json.dump(rep, open(QC / "QC_REPORT.json", "w"), indent=1, ensure_ascii=False)
    progress(f"B4 public-2 QC_REPORT.json written: pass={rep['pass']} failed={failed}")
    print("pass", rep["pass"], "failed", failed, "stale", stale)


def summarise(name, g):
    n = g["numbers"]
    if name == "G7":
        out = {"fails_total": g.get("fails_total")}
        for k, d in n.items():
            for q, v in d.items():
                if v["fails"]:
                    out[f"{k}|{q}"] = {"features_tested": v["features_tested"], "fails": v["fails"],
                                       "top": [x[:4] + ([x[5]] if len(x) > 5 else []) for x in v["top_fails"][:4]]}
        return out
    if name == "G10":
        out = {"fails": g.get("fails")}
        for fn in ("rows_r1", "reserve_r1"):
            for ds, d in n[fn].items():
                if isinstance(d, dict) and d.get("cells_off_2pp"):
                    out[f"{fn}|{ds}|cells_off_2pp [yes, n]"] = d["cells_off_2pp"]
                if isinstance(d, dict) and "yes_rate" in d:
                    out[f"{fn}|{ds}|yes_rate"] = d["yes_rate"]
                if isinstance(d, dict) and "gold_longest_diff_pp" in d:
                    out[f"{fn}|{ds}|longest_gold_diff_pp|abstain_wrong_rate"] = [d["gold_longest_diff_pp"],
                                                                                 d.get("abstain_wrong_rate")]
        return out
    if name == "G6":
        out = {"fails": g.get("fails"), "qc_sample": g.get("qc_sample")}
        for k, v in n.items():
            p = v["pooled"]
            out[k] = {"pooled_acc": p["acc"], "chance": p["chance"], "over_pp": p["over_pp"],
                      "max_dataset_over_pp": max(x["over_pp"] for d, x in v.items() if d != "pooled")}
        return out
    if name == "G5":
        return {d: {k: v for k, v in x.items() if k != "flagged"} for d, x in n.items() if isinstance(x, dict)}
    if name == "G1":
        return {"fails": g.get("fails"), "row_meta": n["row_meta"], "upstream_reread_now":
                {k: v.get("equals_manifest") for k, v in n["upstream_reread_now"].items()},
                "denylist": {"counts": n["denylist"]["counts"], "rebuilt_equals_c_build_denylist":
                             n["denylist"]["rebuilt_equals_c_build_denylist"]},
                "input_paths_74": n["input_paths_74"], "rules_3_1_rows_r1": n["rules_3_1_rows_r1"],
                "split_disjoint": n["split_disjoint"]["dev_vs_train_reserve_shared_keys"]}
    if name == "sealed_check":
        return n
    return n


if __name__ == "__main__":
    main()
