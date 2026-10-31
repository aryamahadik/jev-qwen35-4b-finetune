"""r3 (c-lanes-v3 repair round 1): rewrite qc/QC_REPORT.json after the G10/G11 repair (old report kept as
qc/QC_REPORT_prev.json). Re-run here: G10, G11, G15, G18, G12 (if qc/g12.json is newer than the pools), sealed_check,
G2 (solver B), G4 (training samplers, tmp/g4_summary_r3.json). Gates the repair did not re-run are marked stale.
Usage: python qc/report_write_r3.py  (from c_src/F1)"""
import json, hashlib, os, shutil, datetime as dt

F = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F1"
os.chdir(F)
old = json.load(open("qc/QC_REPORT.json"))
if old.get("repair") != "r3":   # first write of this repair: keep the check report as the previous one
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
            "failed_candidates": fc, "failed_qc_sample": fq, "rerun": "r3 (repair)"}
# G11
g11 = json.load(open("qc/g11_candidates_r1.json"))
g["G11"] = {"pass": bool(g11["pass"]), "file": "qc/g11_candidates_r1.json", "failed": g11["failed"],
            "wordings_per_card_min": g11.get("wordings_per_card_min"), "cards_lt5_wordings": g11.get("cards_lt5_wordings"),
            "rerun": "r3 (repair)"}
# G15 / G18
d = json.load(open("qc/g15_g18.json"))
g["G15"] = {"pass": bool(d["G15"]["pass"]), "file": "qc/g15_g18.json", "rerun": "r3 (repair)"}
g["G18"] = {"pass": bool(d["G18"]["pass"]), "file": "qc/g15_g18.json", "rerun": "r3 (repair)"}
# sealed
s = json.load(open("tmp/sealed_results.json"))
g["sealed_check"] = {"pass": all(v.get("rc") == 0 and v.get("rows_hit") == 0 for v in s.values()),
                     "file": "tmp/sealed_results.json", "rows_hit": {k: v.get("rows_hit") for k, v in s.items()},
                     "rerun": "r3 (repair)"}
# G2 (solver B) and G4
_ps = open("tmp/a10/r3e_post.status").read() if os.path.exists("tmp/a10/r3e_post.status") else ""
_g2log = "tmp/a10/solverb2.log" if "solverb2 rc=" in _ps else "tmp/a10/solverb.log"
mm = json.load(open("solverB/mismatch.json"))
nmm = mm["rows_checked"] - mm["agree"]
g["G2"] = {"pass": nmm == 0, "mismatches": nmm, "rows_checked": mm["rows_checked"], "file": "solverB/mismatch.json", "log": _g2log,
           "rerun": "r3 (repair)"}
# G3 (agent 7): inline per-row label gate (build.py emit.gate_row) on every row: a failing row is never kept, so
# every pool row passed it; the shard "fails" lists count the refused candidates; the round trip is G2 (solver B)
import glob as _gl
_sh = _gl.glob("tmp/shards_cand/*.json") + _gl.glob("tmp/shards_qc/*.json")
_gf = sum(sum(1 for x in (json.load(open(f)).get("fails") or []) if x and x[0] == "gate") for f in _sh)
g["G3"] = dict(g.get("G3", {}), **{"pass": nmm == 0, "shards": len(_sh), "refused_candidates_gate": _gf,
           "note": "every kept row passed the inline gate (failing candidates are dropped and regenerated); solver B round trip = G2",
           "rerun": "r3 (repair)"})
g4 = json.load(open("tmp/g4_summary_r3.json"))
g4f = {k: sum(x for kk, x in v.items() if kk.endswith(":fail")) for k, v in g4.items() if isinstance(v, dict)}
g4r = {k: v.get("rows") for k, v in g4.items() if isinstance(v, dict)}
g["G4"] = {"pass": all(x == 0 for x in g4f.values()) and all((r or 0) >= 1000 for k, r in g4r.items() if k != "S5"),
           "file": "tmp/g4_summary_r3.json", "rows": g4r, "fails": g4f,
           "note": "training samplers re-run on the final r3 code; S5 (dev-only, code unchanged) carried over",
           "rerun": "r3 (repair)"}
# agent 11 (pass D, r3e): G6 / G7 / G11 / G12 re-run locally on the final pools by tmp/a10/run_r3e_post.sh
# (status tmp/a10/r3e_post.status; logs tmp/qc/r3e_*.log)
r3d_fresh = "R3E_GATES_DONE" in _ps
if r3d_fresh and "g7 qc rc=0" in _ps and "g7 cand rc=0" in _ps:
    _c, _q = json.load(open("qc/g7_candidates_r1.json")), json.load(open("qc/g7_qc_sample.json"))
    g["G7"] = {"pass": bool(_c["pass"]) and bool(_q["pass"]), "files": ["qc/g7_candidates_r1.json", "qc/g7_qc_sample.json"],
               "candidates_r1": {"pass": bool(_c["pass"])}, "qc_sample": {"pass": bool(_q["pass"])},
               "logs": ["tmp/qc/r3e_g7cand.log", "tmp/qc/r3e_g7qc.log"], "rerun": "r3 (repair, pass D)"}
if r3d_fresh and "g6 rc=0" in _ps:
    _g6 = json.load(open("qc/g6_r2_qc_sample.json"))
    g["G6"] = dict(g["G6"], **{"pass": bool(_g6["pass"]), "file": "qc/g6_r2_qc_sample.json",
                               "logs": ["tmp/qc/r3e_g6_yn.log", "tmp/qc/r3e_g6_ch.log", "tmp/qc/r3e_g6_merge.log"],
                               "rerun": "r3 (repair, pass D)"})
    g["G6"].pop("stale", None)
# G12 if re-run after the pools were written
if r3d_fresh or (os.path.exists("qc/g12.json") and os.path.getmtime("qc/g12.json") > pool_mtime):
    d = json.load(open("qc/g12.json"))
    g["G12"] = dict(g["G12"], **{k: d[k] for k in ("pass", "rows", "exact_duplicate_rows", "near_dup_pairs_outside_group") if k in d})
    g["G12"]["rerun"] = "r3 (repair)"
    stale = ["G5", "G8"]
else:
    stale = ["G5", "G8", "G12"]
stale += [k for k in ("G6", "G7") if "rerun" not in g[k] or "pass D" not in g[k]["rerun"]]
for k in stale:
    g[k] = dict(g[k], stale="pools changed in repair r3 (12 Q1 cards + their top-ups, 17 Q2 cards regenerated in carried chains (pass C2 v7: v6 + G7 per-basis bands), C029 regenerated; pass D: cand Q2 chains C2 v8, 103 qc non-Q2 cards rebuilt with the qc depth slack, A28 planner re-chose Q1 cards): re-check needed")

failed = sorted(k for k, v in g.items() if v.get("pass") is False)
out = dict(old)
out.update({"gates": g, "pools": pools, "failed_gates": failed, "repair": "r3",
            "pending_gates": [f"{k} (stale after repair r3)" for k in stale],
            "pass": False if failed else None,
            "previous_report": "qc/QC_REPORT_prev.json (check:F1 report before repair r3)",
            "checker": "repair:F1 (workflow c-lanes-v3) for G7/G10/G11/G6 + label gates; G5 deferred (A24; last reads 600/600 + 300/300 agree, 0 flags); G8 from check:F1, now stale",
            "updated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")})
out["summary"] = (f"repair r3: G7 {g['G7'].get('pass')}, G6 {g['G6'].get('pass')}, G10 {'pass' if g['G10']['pass'] else 'FAIL ' + str(fc + fq)}, "
                  f"G11 {'pass' if g['G11']['pass'] else 'FAIL'}, G2 {nmm} mismatches, G4 fails {g4f}, "
                  f"G15 {g['G15']['pass']}, G18 {g['G18']['pass']}, sealed {g['sealed_check']['pass']}; "
                  f"stale (re-check needed): {', '.join(stale)}")
json.dump(out, open("qc/QC_REPORT.json", "w"), indent=1)
print(out["summary"])
print("failed", failed)
