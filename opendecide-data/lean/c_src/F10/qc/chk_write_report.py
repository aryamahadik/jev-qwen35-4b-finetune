"""Write qc/QC_REPORT.json (check:F10, c-lanes-v3): the builder's gates (G2/G3/G4/G15-builder/sealed, kept verbatim
under 'builder') + the independent checker's gates (G5, G6, G7, G8 (A19.1), G10, G11, G12, G15, G18) and the pool
sha256s the mixer checks. The builder's report is backed up once to qc/QC_REPORT_builder.json. Counts only.
pass = builder pass and every checker gate passes (G5: 0 clearly wrong, ambiguous <= 3)."""
import json, time
import chk_lib as q

QC, OUT = q.QC, q.OUT
bk = QC / "QC_REPORT_builder.json"
if not bk.exists():
    bk.write_text((QC / "QC_REPORT.json").read_text())
B = json.loads(bk.read_text())


def J(n):
    p = QC / n
    return json.loads(p.read_text()) if p.exists() else None


pools = {f: q.sha(OUT / f) for f in ("candidates_r1.jsonl", "candidates_r1.relations.jsonl", "candidates_r1.sidecar.jsonl",
                                     "qc_sample.jsonl", "qc_sample.relations.jsonl", "mixdev_S5.jsonl")}
G = {}
g5 = J("g5.json")
G["G5"] = {"pass": bool(g5 and g5["pass"] and g5["pool_sha256"] == pools["candidates_r1.jsonl"]), "file": "qc/g5.json",
           **({k: g5[k] for k in ("clearly_wrong", "ambiguous", "program_rows", "real_text_rows")} if g5 else {"missing": True})}
g6 = J("g6_qc_sample.json")
G["G6"] = {"pass": bool(g6 and g6["pass"]), "file": "qc/g6_qc_sample.json",
           "views": {f"{p}.{k}": {"best": v["best"], "chance": v.get("chance", v.get("chance_mean_1_over_k"))}
                     for p in ("yes_no", "choice") for k, v in (g6 or {}).get(p, {}).items() if isinstance(v, dict)}}
g7c, g7q = J("g7_candidates_r1.json"), J("g7_qc_sample.json")
G["G7"] = {"pass": bool(g7c and g7c["pass"] and g7q and g7q["pass"]), "files": ["qc/g7_candidates_r1.json", "qc/g7_qc_sample.json"],
           "rule": (g7c or {}).get("pass_rule"),
           **{n: {k: d[k] for k in ("n_tests", "n_fail_choice", "n_fail_yes_no_raw_multi_card", "n_fail_yes_no_card_adjusted")}
              | {"top_choice_fails": [f["feature"] for f in d["fails_choice"][:6]]} for n, d in (("candidates_r1", g7c), ("qc_sample", g7q)) if d}}
g8 = J("g8v3_candidates_r1.json")
if g8:
    ch, yn = g8["parts"].get("choice", {}), g8["parts"].get("yes_no", {})
    G["G8"] = {"pass": bool(ch.get("pass")), "rule": "A19.1 adopted: choice part gated by G8v3 p > 0.009; yes/no report-only",
               "file": "qc/g8v3_candidates_r1.json", "platform": "local Mac (rrun refused: $15 cap)",
               "choice": {"raw_share": ch.get("real", {}).get("share"), "p": ch.get("test", {}).get("p"), "verdict": ch.get("test", {}).get("verdict")},
               "yes_no_report_only": {"raw_share": yn.get("real", {}).get("share"), "p": yn.get("test", {}).get("p"),
                                      "verdict": yn.get("test", {}).get("verdict"), "status": "A19.1 report-only"}}
else:
    G["G8"] = {"pass": False, "missing": True}
for gate, stem in (("G10", "g10"), ("G11", "g11"), ("G12", "g12")):
    c, s = J(f"{stem}_candidates_r1.json"), J(f"{stem}_qc_sample.json")
    G[gate] = {"pass": bool(c and c["pass"]), "gated_set": "candidates_r1", "files": [f"qc/{stem}_candidates_r1.json", f"qc/{stem}_qc_sample.json"],
               "failed_parts": (c or {}).get("failed") or [k for k, v in (c or {}).get("pass_parts", {}).items() if not v],
               "qc_sample_pass": bool(s and s["pass"])}
    if gate == "G12" and c:
        G[gate].update({k: c[k] for k in ("exact_duplicates", "near_dup_pairs_outside_twin_sets", "structure_hash_collisions_across_groups",
                                          "mixdev_overlap_rows")})
c, s = J("g15_g18_candidates_r1.json"), J("g15_g18_qc_sample.json")
G["G15"] = {"pass": bool(c and c["G15_pass"] and s and s["G15_pass"]), "files": ["qc/g15_g18_candidates_r1.json", "qc/g15_g18_qc_sample.json"],
            "candidates": {k: (c or {}).get(k) for k in ("check_rows_ok", "loader_check_fail", "round_trip_fail", "units_gt3", "long_units_gt2", "chat_tokens")}}
G["G18"] = {"pass": bool(c and c["G18"]["pass"] and s and s["G18"]["pass"]), "note": "F10 has no ordinal rows"}
failed = [k for k, v in G.items() if not v["pass"]]
R = {"report": "F10 QC report (check:F10 independent checker + gen:F10 builder gates), c-lanes-v3",
     "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "gen_version": B.get("gen_version"),
     "inputs_sha256": B.get("inputs_sha256"), "rows": B.get("rows"), "pool_sha256": pools,
     "builder": {"pass": B.get("pass"), "failed_gates": B.get("failed_gates"), "gates": B.get("gates"), "written_utc": B.get("written_utc")},
     "checker": {"gates": G, "failed_gates": failed, "platform": "all checker gates on the local Mac (rrun refused at the $15 cap)"},
     "gates": B.get("gates"), "failed_gates": (B.get("failed_gates") or []) + failed,
     "pass": bool(B.get("pass")) and not failed, "problems": B.get("problems", [])}
(QC / "QC_REPORT.json").write_text(json.dumps(R, indent=1, default=str))
print(json.dumps({"pass": R["pass"], "failed": R["failed_gates"]}))
