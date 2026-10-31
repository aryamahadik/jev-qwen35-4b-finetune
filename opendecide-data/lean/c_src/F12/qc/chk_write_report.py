"""Write qc/QC_REPORT.json (check:F12, c-lanes-v3; adapted from ../F9/qc/chk_write_report.py).
Keeps the builder's report keys verbatim (family, spec_id, g0_sha256, inputs, gates incl. G2/G3/G4/G15/G18/sealed, quotas,
notes, mixdev_disjoint, ...; backed up once to qc/QC_REPORT_builder.json) and adds a 'checker' block with the independent
checker's gates (G5, G6, G7, G8 (A19/A19.1), G10, G11, G12, G15, G18) plus the pool sha256s. Counts only.
pass = builder gates pass and every checker gate passes (G5: 0 clearly wrong, ambiguous <= 3); a gate not run is a fail."""
import json, time
import chk_lib as q

QC, OUT = q.QC, q.OUT
bk = QC / "QC_REPORT_builder.json"
_cur = json.loads((QC / "QC_REPORT.json").read_text())
if not bk.exists() or "checker" not in _cur:  # current report is the builder's own (newer build): refresh the backup
    bk.write_text((QC / "QC_REPORT.json").read_text())
B = json.loads(bk.read_text())
NOT_RUN = "not completed in this check (job > 2 min, rrun only); counts as a fail"


def J(n):
    p = QC / n
    return json.loads(p.read_text()) if p.exists() else None


pools = {f: q.sha(OUT / f) for f in ("candidates_r1.jsonl", "relations_candidates_r1.jsonl", "qc_sample.jsonl",
                                     "relations_qc_sample.jsonl", "mixdev_S5.jsonl", "relations_mixdev_S5.jsonl", "MANIFEST.json")}
CAND = pools["candidates_r1.jsonl"]
G = {}
g5 = J("g5.json")
import os
if os.environ.get("G5_DEFERRED"):  # A24: G5 blind read only after every script gate passes
    g5 = None
G["G5"] = {"pass": bool(g5 and g5["pass"] and g5["pool_sha256"] == CAND), "file": "qc/g5.json",
           **({k: g5[k] for k in ("clearly_wrong", "ambiguous", "program_rows")} | {"notes": g5.get("reader_notes_summary")}
              if g5 else ({"status": "G5 deferred (A24): script gates fail on the current pools; blind read not done; old qc/g5.json is for an older build"} if os.environ.get("G5_DEFERRED") else {"missing": True}))}
g6 = J("g6_qc_sample.json")
if g6:
    G["G6"] = {"pass": bool(g6["pass"]), "file": "qc/g6_qc_sample.json", "rule": "5-fold GroupKFold by card; every view <= chance + 2 pp",
               "views": {f"{p}.{k}": {"best": v.get("best"), "chance": v.get("chance", v.get("chance_mean_1_over_k"))}
                         for p in ("yes_no", "choice") for k, v in g6.get(p, {}).items() if isinstance(v, dict)}}
else:
    G["G6"] = {"pass": False, "status": NOT_RUN, "script": "qc/chk_g6.py qc_sample (remote: qc/chk_run_remote.sh via c_build/rrun.py)"}
g7c, g7q = J("g7_candidates_r1.json"), J("g7_qc_sample.json")
G["G7"] = {"pass": bool(g7c and g7c["pass"] and g7q and g7q["pass"]), "files": ["qc/g7_candidates_r1.json", "qc/g7_qc_sample.json"],
           "rule": (g7c or {}).get("pass_rule"),
           **{n: {k: d.get(k) for k in ("n_tests", "n_fail_choice", "n_fail_yes_no_raw_multi_card", "n_fail_yes_no_card_adjusted")}
              | {"top_choice_fails": [f.get("feature") for f in d.get("fails_choice", [])[:8]],
                 "yes_no_multi_card_fails": [f.get("feature") for f in d.get("fails_yes_no_raw_multi_card", [])[:4]]}
              for n, d in (("candidates_r1", g7c), ("qc_sample", g7q)) if d}}
g8 = J("g8v3_candidates_r1.json")
if g8 and g8.get("pool_sha256") != CAND:
    g8 = None  # stale (older build); a G8 run on the current pool is required
if g8:
    ch, yn = g8.get("parts", {}).get("choice", {}), g8.get("parts", {}).get("yes_no", {})
    G["G8"] = {"pass": bool(ch.get("pass")), "rule": "A19/A19.1 adopted (c_build/g8v2/A19_ADOPTED): choice part gated by G8v3 p > 0.009; "
               "yes/no report-only; old raw share reported", "file": "qc/g8v3_candidates_r1.json",
               "choice": {"raw_share": ch.get("real", {}).get("share"), "p": ch.get("test", {}).get("p"), "verdict": ch.get("test", {}).get("verdict")},
               "yes_no_report_only": {"raw_share": yn.get("real", {}).get("share"), "p": yn.get("test", {}).get("p"),
                                      "verdict": yn.get("test", {}).get("verdict")}}
else:
    G["G8"] = {"pass": False, "status": "not completed in this check (rrun job did not return qc/g8v3_candidates_r1.json); counts as a fail",
               "rule": "A19/A19.1 adopted: choice part gated by G8v3 p > 0.009; yes/no report-only",
               "script": "qc/chk_g8v3.py on out/candidates_r1.jsonl (remote: qc/chk_run_remote.sh via c_build/rrun.py)"}
for gate, stem in (("G10", "g10"), ("G11", "g11"), ("G12", "g12")):
    c, s = J(f"{stem}_candidates_r1.json"), J(f"{stem}_qc_sample.json")
    G[gate] = {"pass": bool(c and c["pass"]), "gated_set": "candidates_r1", "files": [f"qc/{stem}_candidates_r1.json", f"qc/{stem}_qc_sample.json"],
               "failed_parts": [k for k, v in (c or {}).get("pass_parts", {}).items() if not v],
               "qc_sample_pass": bool(s and s["pass"]),
               "qc_sample_failed_parts": [k for k, v in (s or {}).get("pass_parts", {}).items() if not v]}
    if gate == "G12" and c:
        G[gate].update({k: c[k] for k in ("exact_duplicates", "near_dup_pairs_outside_twin_sets", "near_dup_pairs_in_twin_sets",
                                          "structure_hash_collisions_across_groups", "mixdev_overlap_rows")})
    m = J(f"{stem}_mixdev_S5.json")
    if m is not None:
        G[gate]["mixdev_S5_pass"] = bool(m["pass"])
c, s, m = J("g15_g18_candidates_r1.json"), J("g15_g18_qc_sample.json"), J("g15_g18_mixdev_S5.json")
G["G15"] = {"pass": bool(c and c["G15_pass"] and s and s["G15_pass"]), "files": ["qc/g15_g18_candidates_r1.json", "qc/g15_g18_qc_sample.json"],
            "candidates": {k: (c or {}).get(k) for k in ("check_rows_ok", "loader_check_fail", "round_trip_fail", "units_gt3", "long_units_gt2", "chat_tokens")},
            "mixdev_S5_pass": bool(m and m.get("G15_pass"))}
G["G18"] = {"pass": bool(c and c["G18"]["pass"] and s and s["G18"]["pass"]), "candidates": (c or {}).get("G18")}
failed = [k for k, v in G.items() if not v["pass"]]
NOTE_G9 = ("G9 (crowd difficulty) runs on the free L4 only (owner, 3 Oct; brief 8) and is not a CPU checker gate; "
           "not part of this check and not counted here")
bg = B.get("gates", {})
b_failed = [k for k, v in bg.items() if isinstance(v, dict) and v.get("pass") is False]
import hashlib
G0 = json.loads((q.F12 / "G0_FROZEN.json").read_text()) if (q.F12 / "G0_FROZEN.json").exists() else {}
g0_now = hashlib.sha256((q.F12 / "G0_SPEC.md").read_bytes()).hexdigest()
R = dict(B)
R.update({"utc_checker": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "pool_sha256": pools, "g0_sha256_now": g0_now, "g0_matches_frozen": g0_now in json.dumps(G0),
          "pools_match_builder_inputs": all(pools.get(v["path"].split("/")[-1]) == v["sha256"] for v in B.get("inputs", {}).values() if isinstance(v, dict) and "path" in v and v["path"].split("/")[-1] in pools),
          "verdict": "check:F12 independent checker: " + ("PASS" if not failed and not b_failed else "FAIL " + ", ".join(b_failed + failed)),
          "checker": {"who": "check:F12 (c-lanes-v3; never a generator or solver author)", "gates": G, "failed_gates": failed,
                      "platform": "local Mac for G5/G7/G10/G11/G12/G15/G18 (each < 2 min); G6/G8 via rrun only",
                      "round": os.environ.get("CHK_ROUND", "first independent check of the current pools (G5 seed 5001)"), "g9_note": NOTE_G9},
          "failed_gates": b_failed + failed, "pass": not failed and not b_failed})
(QC / "QC_REPORT.json").write_text(json.dumps(R, indent=1, default=str))
print(json.dumps({"pass": R["pass"], "failed": R["failed_gates"], "builder_failed": b_failed}))
