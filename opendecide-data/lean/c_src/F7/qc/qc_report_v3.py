"""Assemble qc/QC_REPORT.json for F7 (independent checker, workflow c-lanes-v3, check:F7 on the r1g pools).
Reads the checker's gate outputs in qc/ and the builder's out/ files for sha256s and its G2/G3/G4/sealed records
(reported, not re-run). Counts only, no row text. G8 judged by A19 (c_build/g8v2/A19_ADOPTED present) via
qc/g8v3_candidates_r1.json; old raw share reported. Gated sets: candidates_r1 (G7, G8, G10, G11, G12, G15, G18),
qc_sample (G6; G7/G10/G15/G18 on qc_sample reported). pass = G5 (0 clearly wrong, ambiguous <= 3) AND every gate."""
import hashlib, json, time
from pathlib import Path
F7 = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F7")
Q, O = F7 / "qc", F7 / "out"
J = lambda p: json.loads((Q / p).read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
nrows = lambda p: sum(1 for _ in p.open())

def main():
    g5, g6 = J("g5.json"), J("g6_qc_sample.json")
    g7c, g7q = J("g7_candidates_r1.json"), J("g7_qc_sample.json")
    g8 = J("g8v3_candidates_r1.json"); g10c, g10q = J("g10_candidates_r1.json"), J("g10_qc_sample.json")
    g11, g12 = J("g11_candidates_r1.json"), J("g12_candidates_r1.json")
    g15c, g15q = J("g15_g18_candidates_r1.json"), J("g15_g18_qc_sample.json")
    man = json.loads((O / "MANIFEST.json").read_text())
    solb = json.loads((F7 / "solverB/run.log").read_text().strip().splitlines()[-1])
    g4 = json.loads((O / "G4_metamorphic.json").read_text())
    pools = {}
    for n in ("candidates_r1", "qc_sample", "mixdev_S5"):
        p = O / f"{n}.jsonl"; pools[n] = {"rows": nrows(p), "sha256": sha(p)}
        r = O / f"{n}.relations.jsonl"
        if r.exists(): pools[n]["relations"] = {"rows": nrows(r), "sha256": sha(r)}
    c8 = g8["parts"]["choice"]
    s8 = {"pass": bool(g8["pass"]) and bool(c8["pass"]) and g8["pool_sha256"] == pools["candidates_r1"]["sha256"],
          "p": c8["test"].get("p"), "K": c8["test"].get("K"), "verdict": c8["test"].get("verdict"), "real": c8["real"],
          "old_raw_share_seed0": g8["old_rule"]["raw_share_all_rows_seed0"], "old_rule_lt_10pct": g8["old_rule"]["verdict_lt_10pct"],
          "pool_sha256_matches": g8["pool_sha256"] == pools["candidates_r1"]["sha256"]}
    g8pass = s8["pass"]
    g6ok = g6.get("n") == pools["qc_sample"]["rows"]
    gates = {
     "G5": {"pass": g5["clearly_wrong"] == 0 and g5["ambiguous"] <= 3 and g5["pool_sha256"] == pools["candidates_r1"]["sha256"],
            "read": g5["read"], "agree": g5["reader_agrees_with_gold"], "clearly_wrong": g5["clearly_wrong"],
            "ambiguous": g5["ambiguous"], "file": "qc/g5.json"},
     "G6": {"pass": bool(g6.get("pass")) and g6ok, "set": f"qc_sample ({g6.get('n')} rows, {g6.get('cards')} cards; GroupKFold(5) by card)",
            "current_pool": g6ok, "chance": g6.get("chance_mean_1_over_K"), "bar": g6.get("bar"),
            "max_gated": g6.get("max_gated"), "gated": g6.get("gated"), "hidden_info_grouped_max": g6.get("hidden_info_grouped_max"),
            "file": "qc/g6_qc_sample.json"},
     "G7": {"pass": bool(g7c["pass"]), "gated_set": "candidates_r1",
            "candidates": {"tests": g7c["tests"], "n_fail": g7c["n_fail"], "fails": g7c["fails"][:5], "option_level_fails": g7c["option_level_fails"]},
            "qc_sample_report_only": {"tests": g7q["tests"], "n_fail": g7q["n_fail"], "fails": g7q["fails"][:5]},
            "files": ["qc/g7_candidates_r1.json", "qc/g7_qc_sample.json"]},
     "G8": {"pass": g8pass, "verdict_source": "A19 (c_build/g8v2/A19_ADOPTED) via c_src/common/g8_aflite.py (qc/g8v3_f7.py)",
            "p": s8.get("p"), "K": s8.get("K"), "verdict": s8.get("verdict"), "real": s8.get("real"),
            "old_raw_share_seed0": s8.get("old_raw_share_seed0"), "old_rule_lt_10pct": s8.get("old_rule_lt_10pct"),
            "pool_sha256_matches": s8["pool_sha256_matches"],
            "file": "qc/g8v3_candidates_r1.json"},
     "G10": {"pass": bool(g10c["pass"]), "gated_set": "candidates_r1", "fails": g10c["fails"], "soft_misses": g10c["soft_misses"],
             "unmentioned": g10c["E_quotas"]["unmentioned"], "spec": "G0 T02: decisive (C1 conv) share 40-60% of unmentioned rows per S1/S2/S4; R05/6.2: two-way conv above-share 50 +/- 5 per convention per sampler",
             "direction_fails": {k: v for k, v in g10c["C_G0_6_2"]["conv_direction_two_way"].items() if f"C.direction_{k.replace('|', '_')}" in g10c["fails"]},
             "qc_sample_report_only": {"fails": g10q["fails"]}, "files": ["qc/g10_candidates_r1.json", "qc/g10_qc_sample.json"]},
     "G11": {"pass": bool(g11["pass"]), "file": "qc/g11_candidates_r1.json"},
     "G12": {"pass": bool(g12["pass"]), "minhash": g12["minhash"], "unplanned_structure_groups": g12["structure_hash_generator"]["groups_unplanned"], "file": "qc/g12_candidates_r1.json"},
     "G15": {"pass": bool(g15c["G15_pass"]) and bool(g15q["G15_pass"]), "relations_candidates": g15c["relations"],
             "loader_check_fail": g15c["loader_check_fail"], "roundtrip_gold_fail": g15c["roundtrip_gold_fail"],
             "files": ["qc/g15_g18_candidates_r1.json", "qc/g15_g18_qc_sample.json"]},
     "G18": {"pass": bool(g15c["G18"]["pass"]) and bool(g15q["G18"]["pass"]), "candidates": g15c["G18"], "qc_sample": g15q["G18"]},
    }
    if not g6ok:
        a = [l for l in (Q / "g6.log").read_text().splitlines() if "] a {" in l]
        gates["G6"] = {"pass": None, "status": "PENDING: g6_qc_sample.json is from an older qc_sample; current run on the r1g qc_sample in progress (qc/g6.log)",
                       "view_a_current_pool": a[-1].split("] a ", 1)[1] if a else None}
    failed = [g for g, v in gates.items() if v["pass"] is False]
    pending = [g for g, v in gates.items() if v["pass"] is None]
    rep = {"family": "F7", "role": "independent checker (workflow c-lanes-v3; never an F7 generator/solver author)",
           "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "pools": pools,
           "G0_SPEC_sha256": sha(F7 / "G0_SPEC.md"), "gates": gates,
           "builder_records_not_rerun": {"G2_solverB": solb, "G4": {k: g4[k] for k in list(g4)[:6]},
                                         "sealed_check": man.get("sealed_check")},
           "failed_gates": failed, "pending_gates": pending, "pass": not failed and not pending,
           "notes": "G10 rerun by the checker on the current pool (same result). Previous checker report (old pool 228f2087) kept at tmp/chk/old228f/QC_REPORT_228f.json."}
    (Q / "QC_REPORT.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps({"failed_gates": failed, "pending_gates": pending, "pass": not failed and not pending, "cand_sha": pools["candidates_r1"]["sha256"][:16]}))

if __name__ == "__main__":
    main()
