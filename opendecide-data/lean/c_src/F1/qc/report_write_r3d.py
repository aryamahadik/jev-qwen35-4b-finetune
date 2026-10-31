"""r3d (c-lanes-v3 repair round 1 after check round 4; agent 8, pass C2 v7): rewrite qc/QC_REPORT.json after the
G7/G10 repair (the check-round-4 report is kept as qc/QC_REPORT_prev.json). Re-run (rrun + Mac): G6 (qc_sample), G7
(both pools), G10 x2, G11, G15, G18, G12, sealed_check, G2 (solver B), G3, G4 (tmp/g4_summary_r3.json). G8 (A19.1:
G8v3 on candidates) is left to the checker and marked stale; G5 stays deferred (A24 b).
Usage: python qc/report_write_r3d.py  (from c_src/F1)"""
import json, hashlib, os, shutil, datetime as dt

F = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F1"
os.chdir(F)
old = json.load(open("qc/QC_REPORT.json"))
if old.get("repair") != "r3d":   # first write of this repair: keep the check report as the previous one
    shutil.copy("qc/QC_REPORT.json", "qc/QC_REPORT_prev.json")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def nrows(p):
    return sum(1 for l in open(p) if l.strip())


pools = {}
for p in ("out/candidates_r1.jsonl", "out/candidates_r1.rel.jsonl", "out/qc_sample.jsonl", "out/mixdev_S5.jsonl"):
    pools[p] = {"sha256": sha(p), "rows": nrows(p)}
pool_mtime = max(os.path.getmtime(p) for p in pools)

g = dict(old["gates"])
# G10
gc, gq = json.load(open("qc/g10_candidates_r1.json")), json.load(open("qc/g10_qc_sample.json"))
fc, fq = list(gc["failed"]), list(gq["failed"])
g["G10"] = {"pass": not fc and not fq, "files": ["qc/g10_candidates_r1.json", "qc/g10_qc_sample.json"],
            "failed_candidates": fc, "failed_qc_sample": fq, "rerun": "r3d (repair, C2 v7)"}
# G11
g11 = json.load(open("qc/g11_candidates_r1.json"))
g["G11"] = {"pass": bool(g11["pass"]), "file": "qc/g11_candidates_r1.json", "failed": g11["failed"],
            "wordings_per_card_min": g11.get("wordings_per_card_min"), "cards_lt5_wordings": g11.get("cards_lt5_wordings"),
            "rerun": "r3d (repair, C2 v7)"}
# G15 / G18
d = json.load(open("qc/g15_g18.json"))
g["G15"] = {"pass": bool(d["G15"]["pass"]), "file": "qc/g15_g18.json", "rerun": "r3d (repair, C2 v7)"}
g["G18"] = {"pass": bool(d["G18"]["pass"]), "file": "qc/g15_g18.json", "rerun": "r3d (repair, C2 v7)"}
# sealed
s = json.load(open("tmp/sealed_results.json"))
g["sealed_check"] = {"pass": all(v.get("rc") == 0 and v.get("rows_hit") == 0 for v in s.values()),
                     "file": "tmp/sealed_results.json", "rows_hit": {k: v.get("rows_hit") for k, v in s.items()},
                     "rerun": "r3d (repair, C2 v7)"}
# G2 (solver B) and G4
mm = json.load(open("solverB/mismatch.json"))
nmm = mm["rows_checked"] - mm["agree"]
g["G2"] = {"pass": nmm == 0, "mismatches": nmm, "rows_checked": mm["rows_checked"], "file": "solverB/mismatch.json", "log": "tmp/rr1/r3d_solverb.log",
           "rerun": "r3d (repair, C2 v7)"}
# G3 (agent 7): inline per-row label gate (build.py emit.gate_row) on every row: a failing row is never kept, so
# every pool row passed it; the shard "fails" lists count the refused candidates; the round trip is G2 (solver B)
import glob as _gl
_sh = _gl.glob("tmp/shards_cand/*.json") + _gl.glob("tmp/shards_qc/*.json")
_gf = sum(sum(1 for x in (json.load(open(f)).get("fails") or []) if x and x[0] == "gate") for f in _sh)
g["G3"] = dict(g.get("G3", {}), **{"pass": nmm == 0, "shards": len(_sh), "refused_candidates_gate": _gf,
           "note": "every kept row passed the inline gate (failing candidates are dropped and regenerated); solver B round trip = G2",
           "rerun": "r3d (repair, C2 v7)"})
g4 = json.load(open("tmp/g4_summary_r3.json"))
g4f = {k: sum(x for kk, x in v.items() if kk.endswith(":fail")) for k, v in g4.items() if isinstance(v, dict)}
g4r = {k: v.get("rows") for k, v in g4.items() if isinstance(v, dict)}
g["G4"] = {"pass": all(x == 0 for x in g4f.values()) and all((r or 0) >= 1000 for k, r in g4r.items() if k != "S5"),
           "file": "tmp/g4_summary_r3.json", "rows": g4r, "fails": g4f,
           "note": "training samplers re-run on the final r3 code; S5 (dev-only, code unchanged) carried over",
           "rerun": "r3d (repair, C2 v7)"}
# G12 if re-run after the pools were written
if os.path.exists("qc/g12.json") and os.path.getmtime("qc/g12.json") > pool_mtime:
    d = json.load(open("qc/g12.json"))
    g["G12"] = dict(g["G12"], **{k: d[k] for k in ("pass", "rows", "exact_duplicate_rows", "near_dup_pairs_outside_group") if k in d})
    g["G12"]["rerun"] = "r3d (repair, C2 v7)"
    stale = ["G8"]
else:
    stale = ["G8", "G12"]
# G7 (both pools; pass = 0 fails in the card-rate yes/no null and the choice-option test)
g7 = {}
for n in ("candidates_r1", "qc_sample"):
    d = json.load(open(f"qc/g7_{n}.json"))
    co, yn = d["choice_options"], d["yes_no"]["card_rate_null"]
    g7[n] = {"pass": bool(d["pass"]), "choice_option_fails": co.get("n_fail"), "choice_kind_fails": co.get("n_fail_kind"),
             "yes_no_card_null_fails": yn.get("n_fail"), "yes_no_card_null_meta_fails": yn.get("n_fail_meta"),
             "fails_top": [{k: x[k] for k in ("rows", "gold_hits", "expected", "z") if k in x} for x in (co.get("fails_top") or [])[:5]]}
g["G7"] = {"pass": all(v["pass"] for v in g7.values()), "files": ["qc/g7_candidates_r1.json", "qc/g7_qc_sample.json"],
           **g7, "rerun": "r3d (repair, C2 v7)"}
# G6 (qc_sample, g6_r2.py as in the check)
d = json.load(open("qc/g6_r2_qc_sample.json"))
g["G6"] = {"pass": bool(d["pass"]), "file": "qc/g6_r2_qc_sample.json", "rule": g["G6"].get("rule"),
           "best": {t: {v: d[t][v].get("best") for v in d[t] if isinstance(d[t][v], dict)} for t in ("yes_no", "choice")},
           "rerun": "r3d (repair, C2 v7)"}
g["G5"] = {"pass": None, "status": "G5 deferred (A24 b): blind read runs at the check once all script gates pass",
           "flags_to_verify": "none (last read qc/g5.json: 0 clearly wrong / ambiguous, all flags agreed with solver A/B)",
           "earlier_read": "qc/g5.json (older pools)"}
for k in stale:
    g[k] = dict(g[k], stale="pools changed in repair r3d (17 Q2 cards regenerated in carried chains, pass C2 v7): re-check needed")

failed = sorted(k for k, v in g.items() if v.get("pass") is False)
out = dict(old)
out.update({"gates": g, "pools": pools, "failed_gates": failed + ["G5 (deferred, A24)"], "repair": "r3d",
            "pending_gates": [f"{k} (stale after repair r3d)" for k in stale],
            "pass": False if failed else None,
            "previous_report": "qc/QC_REPORT_prev.json (check:F1 round 4 report, before repair r3d)",
            "checker": "repair:F1 (workflow c-lanes-v3, agent 8) for G6/G7/G10/G11/G12 + label gates; G8 from check:F1 round 4, now stale",
            "updated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")})
out["summary"] = (f"repair r3d (C2 v7): G7 {'pass' if g['G7']['pass'] else 'FAIL'}, G6 {'pass' if g['G6']['pass'] else 'FAIL'}, G10 {'pass' if g['G10']['pass'] else 'FAIL ' + str(fc + fq)}, "
                  f"G11 {'pass' if g['G11']['pass'] else 'FAIL'}, G2 {nmm} mismatches, G4 fails {g4f}, "
                  f"G15 {g['G15']['pass']}, G18 {g['G18']['pass']}, sealed {g['sealed_check']['pass']}; "
                  f"stale (re-check needed): {', '.join(stale)}")
json.dump(out, open("qc/QC_REPORT.json", "w"), indent=1)
print(out["summary"])
print("failed", failed)
