"""check:F1 (c-lanes-v3), checker round on the pass-D pools (merged 03:30Z 7 Oct). Rewrites qc/QC_REPORT.json from the
checker gate files (qc/g6_r2*, g7_*, g10_*, g11_*, g12, g15_g18) run on the current pools; keeps the previous report as
qc/QC_REPORT_pre_chk6.json. Builder gates (G2, G3, G4, sealed_check) are carried with their files/mtimes.
Usage: python qc/report_write_chk6.py  (from anywhere)"""
import json, hashlib, os, shutil, datetime as dt

F = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F1"
os.chdir(F)
old = json.load(open("qc/QC_REPORT.json"))
shutil.copy("qc/QC_REPORT.json", "qc/QC_REPORT_pre_chk6.json")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def nrows(p):
    return sum(1 for l in open(p) if l.strip())


POOLS = ("out/candidates_r1.jsonl", "out/candidates_r1.rel.jsonl", "out/qc_sample.jsonl", "out/qc_sample.rel.jsonl",
         "out/mixdev_S5.jsonl")
pools = {p: {"sha256": sha(p), "rows": nrows(p)} for p in POOLS}
pool_mtime = max(os.path.getmtime(p) for p in POOLS)
man = json.load(open("out/MANIFEST.json"))
mf = man.get("files", {})
man_ok = all(mf.get(os.path.basename(p), {}).get("sha256") == v["sha256"] for p, v in pools.items())


def fresh(p):
    return os.path.exists(p) and os.path.getmtime(p) >= pool_mtime


g = {}
# G6 (qc_sample, 5-fold GroupKFold by card, model-visible metadata only)
g6 = json.load(open("qc/g6_r2_qc_sample.json"))
fails6 = []
for part in ("yes_no", "choice"):
    for view, v in g6[part].items():
        if isinstance(v, dict) and "pass" in v and not v["pass"]:
            ch = v.get("chance", v.get("chance_mean_1_over_k"))
            fails6.append({"part": part, "view": view, "best": v["best"], "chance": ch,
                           "bar": round(ch + 0.02, 4), "over_bar_pp": round(100 * (v["best"] - ch - 0.02), 2)})
g["G6"] = {"pass": bool(g6["pass"]), "file": "qc/g6_r2_qc_sample.json", "fresh": fresh("qc/g6_r2_qc_sample.json"),
           "rule": g6["rule"], "cv": g6["cv"], "metadata": g6["metadata"], "fails": fails6,
           "best": {p: {k: v["best"] for k, v in g6[p].items() if isinstance(v, dict) and "best" in v}
                    for p in ("yes_no", "choice")}}
# G7
g7c, g7q = json.load(open("qc/g7_candidates_r1.json")), json.load(open("qc/g7_qc_sample.json"))


def g7s(d):
    return {"pass": bool(d["pass"]), "yes_no_card_rate_null_fails": d["yes_no"]["card_rate_null"]["n_fail"],
            "yes_no_literal_p0_half_fails_info": d["yes_no"]["literal_p0_half"]["n_fail"],
            "choice_fails": d["choice_options"]["n_fail"]}


g["G7"] = {"pass": bool(g7c["pass"] and g7q["pass"]), "files": ["qc/g7_candidates_r1.json", "qc/g7_qc_sample.json"],
           "fresh": fresh("qc/g7_candidates_r1.json") and fresh("qc/g7_qc_sample.json"),
           "candidates_r1": g7s(g7c), "qc_sample": g7s(g7q)}
# G8 (A19.1 adopted): not judged on these pools
o8 = old["gates"].get("G8", {})
g["G8"] = {"pass": None, "rule_source": "A19.1 adopted (c_build/g8v2/A19_ADOPTED): choice part judged by G8v3 "
           "(c_src/common/g8_aflite.py, p > 0.009); yes/no part report-only (old raw share + G8v3 p)",
           "status": "deferred: not judged on the pass-D pools. rrun refuses every launch (all runner accounts at their "
           "$12 cap); a local G8v3 run (embed + 512 solves, ~5,600 s at 16 Modal cpu) is ~3 h at the 2-worker local "
           "limit, and the pools already fail G6 + G10, so they will be regenerated before G8 can count. Run G8v3 "
           "(choice part) and the old raw share on the first pools that pass every other script gate.",
           "last_old_raw_spec_stale": o8.get("old_raw_spec"), "g8v3_ever_completed_for_F1": False}
# G10
gc, gq = json.load(open("qc/g10_candidates_r1.json")), json.load(open("qc/g10_qc_sample.json"))


def g10fails(d):
    out = {}
    for k in d["failed"]:
        c = d["checks"][k]
        bad = [n for kk, vv in c.items() if kk.startswith("outside") for n in vv]
        cells = c.get("groups") or c.get("cells") or {}
        out[k] = {"rule": [kk for kk in c if kk.startswith("outside")],
                  "failing": {n: cells.get(n) for n in bad} if bad else {kk: vv for kk, vv in c.items()
                                                                          if kk not in ("groups", "cells")}}
    return out


g["G10"] = {"pass": not gc["failed"] and not gq["failed"], "files": ["qc/g10_candidates_r1.json", "qc/g10_qc_sample.json"],
            "fresh": fresh("qc/g10_candidates_r1.json") and fresh("qc/g10_qc_sample.json"),
            "failed_candidates": g10fails(gc), "failed_qc_sample": g10fails(gq)}
# G11
g11 = json.load(open("qc/g11_candidates_r1.json"))
g["G11"] = {"pass": bool(g11["pass"]), "file": "qc/g11_candidates_r1.json", "fresh": fresh("qc/g11_candidates_r1.json"),
            "failed": g11["failed"], "wordings_per_card_min": g11.get("wordings_per_card_min"),
            "cards_lt5_wordings": g11.get("cards_lt5_wordings")}
# G12
g12 = json.load(open("qc/g12.json"))
g["G12"] = {"pass": bool(g12["pass"]), "file": "qc/g12.json", "fresh": fresh("qc/g12.json"), "rows": g12["rows"],
            "exact_duplicate_rows": g12["exact_duplicate_rows"],
            "near_dup_pairs_outside_group": g12["near_dup_pairs_outside_group"]}
# G15 / G18
gg = json.load(open("qc/g15_g18.json"))
g["G15"] = {"pass": bool(gg["G15"]["pass"]), "file": "qc/g15_g18.json", "fresh": fresh("qc/g15_g18.json"),
            "loader": {k: {kk: v[kk] for kk in ("rows", "loader_ok", "loader_check_fail", "tok_max") if kk in v}
                       for k, v in gg["G15"].get("files", {}).items()}}
g["G18"] = {"pass": bool(gg["G18"]["pass"]), "file": "qc/g15_g18.json", "note": gg["G18"].get("note")}
# builder gates carried (not checker gates)
mm = json.load(open("solverB/mismatch.json"))
g["G2"] = {"pass": mm["agree"] == mm["rows_checked"] and not mm["mismatches"], "file": "solverB/mismatch.json",
           "rows_checked": mm["rows_checked"], "mismatches": len(mm["mismatches"]), "fresh": fresh("solverB/mismatch.json"),
           "by": "builder (solver B, spec-only); carried"}
sr = json.load(open("tmp/sealed_results.json"))
g["sealed_check"] = {"pass": all(v.get("rc") == 0 and v.get("rows_hit") == 0 for v in sr.values()),
                     "file": "tmp/sealed_results.json", "fresh": fresh("tmp/sealed_results.json"),
                     "rows_hit": {k: v.get("rows_hit") for k, v in sr.items()}, "by": "builder; carried"}
for k in ("G3", "G4"):
    if k in old["gates"]:
        g[k] = dict(old["gates"][k], carried_from="previous report (builder gate, not a check:F1 gate)",
                    stale_vs_pass_D_pools=True)
g["G5"] = {"pass": None, "status": "G5 deferred (A24): script gates fail (G6, G10)",
           "earlier_read": "qc/g5.json (older pools)", "stale": "pools changed in repair pass D"}

checker_gates = ("G6", "G7", "G8", "G10", "G11", "G12", "G15", "G18")
failed = [k for k in checker_gates if g[k]["pass"] is False]
pending = [k for k in checker_gates if g[k]["pass"] is None] + ["G5"]
now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
rep = {"family": "F1", "round": 1, "checker": "check:F1 (workflow c-lanes-v3), independent checker",
       "pools": pools, "manifest_matches_pools": man_ok, "manifest_written_utc": man.get("written_utc"),
       "gates": g, "failed_gates": failed, "pending_gates": pending,
       "g5_rule": "A24: G5 only after every script gate passes; pass needs 0 clearly wrong, ambiguous <= 6",
       "pass": False, "previous_report": "qc/QC_REPORT_pre_chk6.json", "updated": now,
       "summary": f"check on pass-D pools: failed {failed}; pending {pending}; G2 {g['G2']['mismatches']} mismatches; "
                  f"sealed pass {g['sealed_check']['pass']}; G5 deferred (A24)"}
json.dump(rep, open("qc/QC_REPORT.json", "w"), indent=1, default=str)
print(json.dumps({"failed": failed, "pending": pending, "manifest_ok": man_ok,
                  "fresh": {k: g[k].get("fresh") for k in g if "fresh" in g[k]},
                  "cand_sha": pools["out/candidates_r1.jsonl"]["sha256"][:16]}))
