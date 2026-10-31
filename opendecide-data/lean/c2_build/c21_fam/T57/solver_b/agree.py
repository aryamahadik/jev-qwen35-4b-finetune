"""T57 agreement harness (the ONLY solver_b file that imports the generator / solver A side).

  python3 -m T57.solver_b.agree --rows 250 --seeds 41,42 --out /path/report.json

Builds rows IN MEMORY (SimExecutor, TEST-ONLY wording pool); task packages are captured from the generator's own specs through
schema.task_package(); B receives schema.b_view(row, packages) only. Disagreement classes are counts, never item text.
"""
import argparse
import json
import random
import re
import sys

from LC_COMMON import sandbox_iface as S
from LC_COMMON import wording
from LC_SOLVER_B import agreelib, langs
from LC_SOLVER_B.common import Budget, Timeout, Unsupported

from .. import build as B
from .. import rows as ROWS
from .. import schema
from .solve import Runner, solve


def _generate(n, seed):
    tasks = {}

    class Rec(B.SolverA):
        def run(self, specs):
            for s in specs:
                tasks[s["task"]["uid"]] = s["task"]
            return super().run(specs)
    orig = B.SolverA
    B.SolverA = Rec
    try:
        pool = wording.make_test_pool(ROWS.ALL_FORMS, 60, {f: s[0] for f, s in ROWS.FORM_SLOTS.items()})
        picker = wording.Picker(pool, random.Random(seed))
        rows, stats, skips = B.build_rows(n, S.SimExecutor(), picker, seed=seed)
    finally:
        B.SolverA = orig
    return rows, {u: schema.task_package(t) for u, t in tasks.items()}


def _fn_names(files):
    names = set()
    for t in files.values():
        names.update(re.findall(r"(?:def|function|func)\s+(?:\([^)]*\)\s*)?([A-Za-z_]\w*)", t))
        names.update(re.findall(r"^([A-Za-z_]\w*)\(\)\s*\{", t, re.M))
        names.update(re.findall(r"^\s+([A-Za-z_]\w*)\([^)]*\)\s*(?::\s*\w+)?\s*\{", t, re.M))
    return names


def run(rows_per_seed, seeds, dump=None):
    T = agreelib.Tally()
    kept_dis = []
    for seed in seeds:
        rows, packages = _generate(rows_per_seed, seed)
        for r in rows:
            key = (r["head"], r["lang"])
            view = schema.b_view(r, packages)
            out = solve(view)
            st = out["status"]
            perm = bool(r["meta"].get("perm_copy"))
            if st == "ok":
                if out["label"] == r["label"]:
                    T.add(key, "agree")
                else:
                    T.add(key, "disagree", "A=%s/B=%s" % (r["label"], out["label"]) if r["head"] in ("VERDICT",) else "letter_mismatch")
            elif st == "ambiguous":
                kept_dis.append((r, packages[r["b_inputs"]["task_uid"]]))
                T.add(key, "disagree", "B_cannot_find_unique_answer:" + ",".join("%s=%s" % kv for kv in sorted(out["evidence"].items()) if isinstance(kv[1], int)))
            else:
                T.add(key, "refused", "%s:%s" % (st, agreelib.why_class(out["evidence"].get("why"))))
            ev = out.get("evidence", {})
            if st == "ok" and out.get("classes") and r["head"] in ("VERDICT", "BEST4", "REASON") and r["manifest"].get("cand_classes"):
                ac = list(r["manifest"]["cand_classes"])
                ok = (out["classes"] == ac) if not perm else (sorted(out["classes"]) == sorted(ac))
                if not ok:
                    for ca, cb in zip(ac, out["classes"]):
                        if ca != cb:
                            T.classes[key]["exec_class_mismatch(not_a_label_disagreement):A=%s/B=%s%s" % (ca, cb, "(perm_copy)" if perm else "")] += 1
                T.note(key, "execution_classes_equal_A" + ("_(perm_copy,as_multiset)" if perm else ""), ok)
            if "shown_trees_match_b_inputs" in ev:
                T.note(key, "b_inputs_trees_equal_shown_patches" + ("_(perm_copy)" if perm else ""), all(ev["shown_trees_match_b_inputs"]) if isinstance(ev["shown_trees_match_b_inputs"], list) else False)
            if "b_inputs_options_consistent" in ev:
                T.note(key, "b_inputs_options_equal_shown_options" + ("_(perm_copy)" if perm else ""), ev["b_inputs_options_consistent"])
            if "other_options_pass_before_and_after" in ev:
                T.note(key, "TESTSEL_other_three_options_pass_before_and_after", ev["other_options_pass_before_and_after"])
            if "ref_fail" in ev:
                T.note(key, "reference_tree_passes_every_case", False)
            # TESTSEL: do the shown option tests call a function that the shown source defines?
            if r["head"] == "TESTSEL" and st == "ok":
                shown = _fn_names({s["path"]: s["text"] for s in r["carriers"]["SRC_FILE"]})
                called = set()
                for o in r["carriers"]["OPTIONS"]:
                    called.update(x for x in re.findall(r"([A-Za-z_]\w*)\(", o) if not x.startswith(("test", "Test", "assert", "deepStrictEqual")) and x not in ("t", "if", "func"))
                T.note(key, "option_tests_call_functions_defined_in_shown_source", bool(called) and called <= shown)
            # rendered visible test vs the structured visible case, on the shown candidate
            if r["head"] in ("VERDICT", "BEST4") and st == "ok" and not perm:
                try:
                    pkg = view["package"]
                    cand = r["b_inputs"]["candidate_files"][0]
                    files = dict(cand)
                    files.update(pkg.get("go_files", {}))
                    vt = r["carriers"]["VISIBLE_TEST"]
                    files[vt["path"]] = vt["text"]
                    res = langs.run_tests(r["lang"], files, only=[vt["path"]], mode="native", budget=Budget(6_000_000))
                    rendered_pass = res["exit"] == 0 and not any(o in ("failed", "error") for o in res["outcomes"].values())
                    rn = Runner(r["lang"], pkg)
                    rn.run_case(pkg["reference_files"], pkg["visible_case"], learn=True)
                    structured_pass = rn.run_case(cand, pkg["visible_case"])[0]
                    T.note(key, "rendered_visible_test_agrees_with_structured_case", rendered_pass == structured_pass)
                except (Unsupported, Timeout):
                    T.note(key, "rendered_visible_test_check_refused", False)
    if dump:
        with open(dump, "w") as f:                     # synthetic rows of B-ambiguous cases only (triage; keep outside the repo)
            json.dump(kept_dis, f)
    return T


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=200)
    ap.add_argument("--seeds", default="41")
    ap.add_argument("--out", default=None)
    ap.add_argument("--dump", default=None)
    a = ap.parse_args(argv)
    seeds = [int(s) for s in a.seeds.split(",")]
    T = run(a.rows, seeds, a.dump)
    table = T.table()
    report = {"family": "T57", "seeds": seeds, "rows_per_seed": a.rows,
              "method": "B = own parsers+evaluators on rendered candidate trees (shown diff applied to the buggy tree); A = SimExecutor/IR labels (no sandbox yet)",
              "totals": agreelib.totals(table), "by_head_lang": table}
    if a.out:
        agreelib.write_report(a.out, report)
    print(json.dumps({"totals": report["totals"]}, sort_keys=True))
    for k, v in table.items():
        print(k, {x: v[x] for x in ("rows", "b_labelled", "agree", "disagree", "b_refused", "agreement_pct")}, v["classes"], v["notes"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
