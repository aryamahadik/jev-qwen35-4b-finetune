"""Summarise scratch/scratch_*.json with the (f) admission checks: report.checks + the four (f) additions; (f)(ii) decision. Counts only."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import repair_a69_faithful as rf
rows = []
for f in sorted((HERE / "scratch").glob("scratch_T*.json")):
    d = json.loads(f.read_text()); fa = d["faithful"]
    checks = dict(fa["report_checks"])
    ad = fa["report_checks_additions"]
    checks.update({"a49c_and_caps": ad["a49c_and_caps_pass"], "chi2_p_gt_0.01_pg_bins": ad["chi2_p_gt_0.01_pg_bins"],
                   "easy_le_25_pg_bins": ad["easy_le_25_pg_bins"], "trap_type_cap_le_35": ad["trap_type_cap_le_35"]})
    rp = {"rows_pre_repair": d["recomputed_pre_repair_rows"], "rows_dropped": fa["rows_dropped"]}
    ok, why = rf.short_record_decision(checks, fa["rows_after"], rp, d["target"], d["record_exclude_units_removed"] or 0)
    cf = fa["checks_final"]
    d1_fail = [k for k in rf.ORDER if cf[k] == "fail"]
    cur = d["current_record"]
    rows.append({"fam": d["family"], "target": d["target"], "pre_matches_record": d["pre_repair_matches_record"], "pre": rp["rows_pre_repair"],
                 "after": fa["rows_after"], "dropped": fa["rows_dropped"], "pct": fa["pct_dropped"], "loss_hit": fa["loss_limit_hit"],
                 "failing_before": fa["failing_before"], "d1_fail_after": d1_fail, "g11": cf["g11_selected"],
                 "other_protected_fail": [k for k in rf.EXTRA_PROTECTED + ["chi2_a42d6", "chi2_pg"] if cf[k] == "fail" and k != "g11_selected"],
                 "report_failed": [k for k, v in checks.items() if v is not True], "f_ii": ok, "why": why,
                 "cur_rows": cur["rows"], "cur_pre": cur["pre_repair"], "cur_dropped": cur["dropped"],
                 "ids_new_not_cur": d["ids_in_faithful_not_current"], "ids_cur_not_new": d["ids_in_current_not_faithful"], "identical": d["ids_identical"]})
for r in rows:
    print(json.dumps(r))
