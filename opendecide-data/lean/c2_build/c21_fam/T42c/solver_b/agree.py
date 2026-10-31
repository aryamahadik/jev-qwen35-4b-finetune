"""T42c agreement harness (the ONLY solver_b file that imports the generator / solver A side).

  python3 -m T42c.solver_b.agree --rows 500 --seeds 31,32 --out /path/report.json

Builds rows IN MEMORY with the lane generator (SimExecutor, TEST-ONLY wording pool; nothing is written but the count-only report),
hands B only `schema.b_view(row)`, and compares B's label with A's. Disagreement classes are counts only (no item text).
"""
import argparse
import json
import sys

from LC_SOLVER_B import agreelib

from .. import schema
from ..dryrun import dry_rows
from . import crosschecks as X
from .solve import solve


def run(rows_per_seed, seeds, dump=None):
    T = agreelib.Tally()
    kept_dis = []
    for seed in seeds:
        rows, log, skips, pool = dry_rows(rows_per_seed, seed=seed, chunk=20)
        for r in rows:
            key = (r["head"], r["lang"])
            view = schema.b_view(r)
            out = solve(view)
            st = out["status"]
            if st == "ok":
                if out["label"] == r["label"]:
                    T.add(key, "agree")
                else:
                    cls = ("A=%s/B=%s" % (r["label"], out["label"])) if r["head"] != "OUT4" else "letter_mismatch"
                    T.add(key, "disagree", cls)
                    kept_dis.append(r)
            elif st == "prefix_failed":
                gl = out["evidence"].get("guarded_label")
                T.add(key, "disagree", "earlier_call_raises(guarded_label_%s)" % ("matches_A" if gl == r["label"] else "differs_from_A"))
            else:
                T.add(key, "refused", "%s:%s" % (st, agreelib.why_class(out["evidence"].get("why"))))
            # cross-checks on the prose / call carriers
            try:
                if r["head"] == "EQV2":
                    if st == "ok":
                        T.note(key, "domain_has_25_to_5000_points_(label_NO_stops_early)", out["label"] == "NO" or 25 <= out["points"] <= 5000)
                    if r["label"] == "YES":
                        pa, pb = r["carriers"]["PROGRAM_PAIR"]
                        T.note(key, "YES_pair_programs_are_not_textually_identical", pa["blocks"] != pb["blocks"])
                    T.note(key, "domain_text_equals_witness_domain", X.domain_matches(X.domain_from_text(r["carriers"]["DOMAIN_DECL"]), r["witness_inputs"]))
                if r["head"] == "OUT4":
                    T.note(key, "call_spec_equals_witness_calls", X.callspec_matches(r["lang"], r["carriers"]["CALL_SPEC"], r["witness_inputs"]))
            except Exception as e:                      # parser limits are reported, never hidden
                T.note(key, "crosscheck_parse_error_" + type(e).__name__, False)
    if dump:
        with open(dump, "w") as f:                     # synthetic rows of disagreements only (for triage; keep outside the repo)
            json.dump(kept_dis, f)
    return T


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=300)
    ap.add_argument("--seeds", default="31")
    ap.add_argument("--out", default=None)
    ap.add_argument("--dump", default=None)
    a = ap.parse_args(argv)
    seeds = [int(s) for s in a.seeds.split(",")]
    T = run(a.rows, seeds, a.dump)
    table = T.table()
    report = {"family": "T42c", "seeds": seeds, "rows_per_seed": a.rows, "method": "B = own parsers+evaluators on rendered text; A = SimExecutor/IR-interpreter labels (no sandbox yet)",
              "totals": agreelib.totals(table), "by_head_lang": table}
    if a.out:
        agreelib.write_report(a.out, report)
    print(json.dumps({"totals": report["totals"]}, sort_keys=True))
    for k, v in table.items():
        print(k, {x: v[x] for x in ("rows", "b_labelled", "agree", "disagree", "b_refused", "agreement_pct")}, v["classes"], v["notes"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
