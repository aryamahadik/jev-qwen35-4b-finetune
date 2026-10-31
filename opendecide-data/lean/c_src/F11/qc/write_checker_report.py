"""Adds/refreshes the independent checker section (check:F11, c-lanes-v3) in qc/QC_REPORT.json. Keeps every generator
section unchanged. Reads only the checker's own gate outputs in qc/ and recomputes pool sha256s."""
import json, hashlib, datetime
from pathlib import Path
F11 = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F11")
QC, OUT = F11 / "qc", F11 / "out"
POOLS = ["candidates_r1", "qc_sample", "mixdev_S5"]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def J(n):
    p = QC / n
    return json.load(open(p)) if p.exists() else None


shas = {f"{p}{ext}": sha(OUT / f"{p}{ext}") for p in POOLS for ext in (".jsonl", ".relations.jsonl", ".sidecar.jsonl")}
gates, failed = {}, []
g5 = J("g5.json")
gates["G5"] = {"file": "qc/g5.json", "pass": g5["pass"], "n": 300, "seed": 5001, "clearly_wrong": g5["clearly_wrong"],
               "ambiguous": g5["ambiguous"], "program_rows": g5["program_rows"],
               "real_text": {k: g5["real_text_rows"][k] for k in ("n", "agree", "reader_differs", "abstain_labels_not_inferable", "per_source")}}
g6 = J("g6_qc_sample.json")
gates["G6"] = {"file": "qc/g6_qc_sample.json", "pool": "qc_sample", "pass": g6["pass"], "rule": g6.get("rule"),
               "yes_no": g6.get("yes_no"), "choice": g6.get("choice")}
for p in ("candidates_r1", "qc_sample"):
    g = J(f"g7_{p}.json")
    gates[f"G7_{p}"] = {"file": f"qc/g7_{p}.json", "pass": g["pass"], "n_fail_choice": g["n_fail_choice"],
                        "n_fail_yes_no_card_adjusted": g["n_fail_yes_no_card_adjusted"],
                        "n_fail_yes_no_raw": g["n_fail_yes_no_raw"], "n_fail_yes_no_raw_multi_card": g["n_fail_yes_no_raw_multi_card"],
                        "fails": [{k: f[k] for k in ("part", "feature", "n", "p", "n_cards") if k in f} for f in g["fails"]][:12]}
g8 = J("g8v3_candidates_r1.json")
gates["G8"] = {"file": "qc/g8v3_candidates_r1.json", "tool": "c_src/common/g8_aflite.py (A19 adopted: c_build/g8v2/A19_ADOPTED)",
               "result": g8 if g8 is None else {k: g8[k] for k in g8 if not isinstance(g8[k], list)}}
gates["G8"]["pass"] = bool(g8 and g8["parts"]["choice"]["pass"])  # A19.1: choice part gates (p > 0.009); yes/no report-only
gates["G8"]["summary"] = None if g8 is None else {
    "choice_p": g8["parts"]["choice"]["test"].get("p"), "choice_pass": g8["parts"]["choice"]["pass"],
    "yes_no_p_report_only": g8["parts"]["yes_no"]["test"].get("p"), "yes_no_pass_report_only": g8["parts"]["yes_no"]["pass"],
    "old_raw_share_seed0": g8["old_rule"]["raw_share_all_rows_seed0"], "old_raw_share_per_part": g8["old_rule"]["per_part_seed0"],
    "old_verdict_lt_10pct": g8["old_rule"]["verdict_lt_10pct"],
    "note": "old raw share: yes/no 23.8% over the infeasible < 10% bar (A19.1, shuffled labels 15-29%), choice 0.7%"}
for p in POOLS:
    for gn, fn in (("G10", f"g10_{p}.json"), ("G11", f"g11_{p}.json"), ("G12", f"g12_{p}.json"), ("G15_G18", f"g15_g18_{p}.json")):
        g = J(fn)
        e = {"file": f"qc/{fn}", "pass": g["pass"]}
        if gn == "G10": e["failed_gated"] = g.get("failed_gated")
        if gn == "G11": e["pass_parts"] = g.get("pass_parts")
        if gn == "G12": e.update({k: g.get(k) for k in ("exact_duplicates", "near_dup_pairs_unplanned", "structure_groups_not_one_twin_set", "structure_bad_examples")})
        if gn == "G15_G18": e.update({k: g.get(k) for k in ("check_rows_ok", "round_trip_rate", "units_gt3", "long_units_gt2", "G15_pass", "G18", "other_problems")})
        gates[f"{gn}_{p}"] = e
# G0_SPEC (frozen) S5 'Use': mixdev_S5 = mix-tuning dev only, never a training row, "Same G2-G4 and G10 rules":
# G11 (family diversity quotas; S5 keys are decision lists by design) and G15 (training relation units) are report-only.
REPORT_ONLY = {"G11_mixdev_S5": "G0_SPEC S5 Use: dev pool gets G2-G4 and G10 only; S5 cards are keys (decision_list) by design",
               "G15_G18_mixdev_S5": "G0_SPEC S5 Use: dev pool gets G2-G4 and G10 only; reported (9 equiv/dneg call_id splits)"}
report_only_misses = {}
for k, v in gates.items():
    if k in REPORT_ONLY:
        v["report_only"] = REPORT_ONLY[k]
        if not v["pass"]:
            report_only_misses[k] = REPORT_ONLY[k]
        continue
    if not v["pass"]:
        failed.append(k)
rep = json.load(open(QC / "QC_REPORT.json"))
rep["checker"] = {"step": "check:F11", "workflow": "c-lanes-v3", "independent": "never wrote F11 generator or solver-B",
                  "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                  "pool_sha256": shas, "gates": gates, "failed_gates": failed, "report_only_misses": report_only_misses,
                  "pass": not failed, "pass_rule": "0 clearly wrong, ambiguous <= 3, every gate passes"}
json.dump(rep, open(QC / "QC_REPORT.json", "w"), indent=1, default=str)
print("failed:", failed, "pass:", not failed)
