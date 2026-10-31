"""T56g agreement harness (the ONLY solver_b file that imports the generator / solver A side).

  python3 -m T56g.solver_b.agree --rows 200 --seeds 51,52 --out /path/report.json

Rows are built IN MEMORY (SimExecutor, TEST-ONLY wording pool); packages are captured from the generator's tasks via
schema.task_package(); B receives schema.b_view(row, packages) only. Reports label agreement plus the per-clause agreement
(visible pass, held-out fail, any signature, protected path). Counts only.
"""
import argparse
import json
import random
import sys

from LC_COMMON import sandbox_iface as S
from LC_COMMON import wording
from LC_SOLVER_B import agreelib

from .. import build as B
from .. import rows as ROWS
from .. import schema
from .solve import solve


def _generate(n, seed):
    gs = {}

    class Rec(B.SolverA):
        def run(self, specs):
            for s in specs:
                g = s.get("g") or s.get("task")
                gs[g["uid"]] = g
            return super().run(specs)
    orig = B.SolverA
    B.SolverA = Rec
    try:
        pool = wording.make_test_pool(ROWS.ALL_FORMS, 60, {f: s[0] for f, s in ROWS.FORM_SLOTS.items()})
        picker = wording.Picker(pool, random.Random(seed))
        rows, stats, skips = B.build_rows(n, S.SimExecutor(), picker, seed=seed)
    finally:
        B.SolverA = orig
    return rows, {u: schema.task_package(g) for u, g in gs.items()}


def run(rows_per_seed, seeds):
    T = agreelib.Tally()
    for seed in seeds:
        rows, packages = _generate(rows_per_seed, seed)
        for r in rows:
            key = (r["lang"],)
            view = schema.b_view(r, packages)
            out = solve(view)
            st = out["status"]
            m = r["manifest"]
            fam = r["meta"]["family"]
            if st == "ok":
                if out["label"] == r["label"]:
                    T.add(key, "agree")
                else:
                    why = []
                    if out["visible_pass"] != m["visible_pass"]:
                        why.append("visible_pass(A=%s,B=%s)" % (m["visible_pass"], out["visible_pass"]))
                    if out["heldout_fail"] != m["heldout_fail"]:
                        why.append("heldout_fail(A=%s,B=%s)" % (m["heldout_fail"], out["heldout_fail"]))
                    if bool(out["signatures"]) != bool(m["signatures"]):
                        why.append("any_signature(A=%s,B=%s)" % (bool(m["signatures"]), bool(out["signatures"])))
                    if bool(out["protected_modified"]) != bool(m["protected_modified"]):
                        why.append("protected(A=%s,B=%s)" % (bool(m["protected_modified"]), bool(out["protected_modified"])))
                    T.add(key, "disagree", "A=%s/B=%s family=%s %s" % (r["label"], out["label"], fam, "+".join(why) or "unknown"))
                T.note(key, "visible_pass_clause", out["visible_pass"] == m["visible_pass"])
                T.note(key, "heldout_fail_clause", out["heldout_fail"] == m["heldout_fail"])
                T.note(key, "any_signature_clause", bool(out["signatures"]) == bool(m["signatures"]))
                T.note(key, "protected_path_clause", bool(out["protected_modified"]) == bool(m["protected_modified"]))
                T.note(key, "exact_signature_id_set_equals_A", sorted("F%s" % s for s in m["signatures"]) == out["signatures"])
                T.note(key, "diff_applied_equals_patched_tree", out["evidence"]["diff_equals_patched_tree"])
                T.note(key, "visible_file_only_run_equals_whole_tree_run", out["evidence"]["visible_files_only_pass"] == out["visible_pass"])
            elif st == "diff_does_not_apply":
                T.add(key, "disagree", "shown_diff_does_not_apply_to_pristine_tree:" + agreelib.why_class(out["evidence"].get("why")))
            else:
                T.add(key, "refused", "%s:%s" % (st, agreelib.why_class(out["evidence"].get("why"))))
    return T


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=150)
    ap.add_argument("--seeds", default="51")
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    seeds = [int(s) for s in a.seeds.split(",")]
    T = run(a.rows, seeds)
    table = T.table()
    report = {"family": "T56g", "seeds": seeds, "rows_per_seed": a.rows,
              "method": "B = own diff applier + runner models + AST signature matchers on rendered trees; A = SimExecutor labels (no sandbox yet)",
              "totals": agreelib.totals(table), "by_lang": table}
    if a.out:
        agreelib.write_report(a.out, report)
    print(json.dumps({"totals": report["totals"]}, sort_keys=True))
    for k, v in table.items():
        print(k, {x: v[x] for x in ("rows", "b_labelled", "agree", "disagree", "b_refused", "agreement_pct")}, v["classes"], v["notes"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
