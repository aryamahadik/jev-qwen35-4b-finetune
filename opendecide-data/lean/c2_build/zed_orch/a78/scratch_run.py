"""A78 scratch run (CPU, read-only on inputs): recompute pre-repair selection per select record, apply the faithful A69 (d) repair,
compare. Writes ONLY under zed_orch/a78/scratch/. Counts and shas only (no row ids)."""
import json, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import repair_a69_faithful as rf
c2s, c2io, cs = rf.c2_select, rf.c2io, rf.cs
import mixer as mx

fam = sys.argv[1]
t0 = time.time()
rec = json.loads((c2io.HERE / "crowd_c2" / f"select_{fam}.json").read_text())
ilog = c2s.LinkGuardedInputLog()
files = [c2io.LEAN / p for p in rec["exclude_files"]]
c2s.drop_ids_of(ilog, files)                      # runs the same log checks (complete, guarded, current); raises if refused
drop = set()
for p in files:                                   # A68: only the binding class of a G13 log drops; the OHS-AC report-only class never does
    d = ilog.json(p)
    by = d.get("drop_ids_by_class")
    if isinstance(by, dict) and isinstance(by.get("binding"), list):
        drop |= set(map(str, by["binding"]))
    else:
        drop |= set(map(str, next(d[k] for k in ("drop_ids", "training_ids_to_drop", "ids") if isinstance(d.get(k), list))))
rows, rels, shas = c2s.family_inputs(ilog, fam)
assert shas["candidates_sha256"] == rec["candidates_sha256"], "candidates changed since the record"
sd = c2s.SHARDS / fam
pg, view, probs = c2s.load_c1_full(ilog, rows, sd / f"labels_{c2s.C1}", sd)
ntok = dict(zip((r["id"] for r in rows), mx.token_counts(ilog, rows)))
res = rf.run_family(fam, rows, rels, pg, probs, rec["target"], ntok, seed=rec["seed"], key=rec["key"], drop_ids=drop)
rp = res["repair"]
fm, units, prow = res["family"], res["units"], res["rows"]
final_ids = res["selected_ids"]
# report checks in the crowd_select form on the faithful result
bins6 = {r["id"]: fm.bins6[r["id"]] for r in prow}
rep = cs.selection_report(prow, units, sorted(res["sel"]), bins6, rec["target"], True, {r["id"]: pg[r["id"]] for r in prow})
checks = rep["checks"]
ok, why = rf.short_record_decision(checks, len(final_ids), rp, rec["target"], rf.mix_c2.units_removed(rec["exclude_ids"]) if False else (rec["exclude_ids"] or {}).get("units_removed", 0))
cur = set(rec["selected_ids"]); new = set(final_ids)
cur_rp = rf.repair_numbers(rec)
out = {"family": fam, "target": rec["target"], "record_exclude_units_removed": (rec["exclude_ids"] or {}).get("units_removed"),
       "current_record": {"rows": len(cur), "pre_repair": (cur_rp or {}).get("rows_pre_repair"), "dropped": (cur_rp or {}).get("rows_dropped"),
                          "checks": rec["report"]["checks"]},
       "recomputed_pre_repair_rows": rp["rows_pre_repair"], "pre_repair_matches_record": rp["rows_pre_repair"] == (cur_rp or {}).get("rows_pre_repair"),
       "faithful": {"rows_after": rp["rows_after"], "rows_dropped": rp["rows_dropped"],
                    "pct_dropped": round(100 * rp["rows_dropped"] / max(1, rp["rows_pre_repair"]), 1), "units_dropped": rp["units_dropped"],
                    "passes_run": rp["passes_run"], "loss_limit_hit": rp["loss_limit_hit"], "loss_max_rows": rp["loss_max_rows"],
                    "failing_before": rp["failing_before"], "failing_after": rp["failing_after"],
                    "stop_reason_by_check": {k: v for k, v in rp["stop_reason_by_check"].items() if v != "passed"},
                    "checks_final": {k: v["verdict"] for k, v in rp["checks_final"].items()},
                    "report_checks": checks, "report_checks_additions": rp["report_checks_additions"]},
       "f_ii_accept": ok, "f_ii_why_not": why,
       "ids_in_faithful_not_current": len(new - cur), "ids_in_current_not_faithful": len(cur - new), "ids_identical": new == cur,
       "seconds": round(time.time() - t0, 1)}
(HERE / "scratch" / f"scratch_{fam}.json").write_text(json.dumps(out, indent=1))
print(json.dumps({k: out[k] for k in ("family", "recomputed_pre_repair_rows", "pre_repair_matches_record", "f_ii_accept", "seconds")}), flush=True)
