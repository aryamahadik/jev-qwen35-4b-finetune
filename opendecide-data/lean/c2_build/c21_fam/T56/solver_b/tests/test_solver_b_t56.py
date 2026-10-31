"""CPU tests for T56 solver B. Hand-built rendered texts only (no generator), one fixture per evidence condition, plus the import-graph
test. A generator-driven agreement test sits at the bottom (skipped if the generator cannot be imported)."""
import ast
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SB = os.path.dirname(HERE)
FAM = os.path.dirname(SB)
ROOT = os.path.dirname(FAM)
for p in (SB, ROOT, FAM):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest  # noqa: E402

import t56_solver_b as sb  # noqa: E402


def test_solverB_independent_import_graph():
    src = open(os.path.join(SB, "t56_solver_b.py")).read()
    mods = set()
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Import):
            mods |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom):
            mods.add((n.module or "").split(".")[0])
    assert mods <= {"re"}, mods
    tree = ast.parse(src)
    doc_nodes = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str):
            doc_nodes.add(id(n.value))
    consts = [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in doc_nodes]
    for banned in ("t56_solver_a", "tool_engine", "t56_generator", "hidden", "gold", "gold_reason", "gold_letter"):
        assert banned not in consts, banned


def build(criteria="1) aaa-1 has status shipped; 2) usr-1 receives the notice exactly once; 3) tst-1 has status pass; "
                   "4) mod.fn is used by the app.run entrypoint", scope="dir", muts=(("set_zed", 'zed_id="aaa-1"', 1),),
          check=("check_zed", ["target: zed", "snapshot_rev: 2", "checked: 1", "passed: 1", "failed: 0", "skipped: 0",
                               "item[1]: aaa-1 pass"]),
          ledger=("usr-1",), run=("passed: 1", "failed: 0"),
          inspect=("entrypoint: app.run", "import: app.py -> mod.py", "flag: mod_on default=on",
                   "call: app.run -> mod.fn guard=flag mod_on"),
          status=None, question="Should the agent's claim of completion be accepted?",
          opts=("Yes, the task is done", "No, the agent should continue")):
    L = ["Policy: p", "", "Task statement:",
         "Task: finish the zed work. Acceptance criteria: %s. Only files under %s may change." % (criteria, scope), "", "Trajectory:"]
    for (nm, args, rev) in muts:
        L += ["Agent called %s(%s)" % (nm, args), "  -> output:", "     rev: %d" % rev]
    if check:
        L += ["Agent called %s(x=\"zed\")" % check[0], "  -> output:"] + ["     " + x for x in check[1]]
    if ledger is not None:
        L += ["Agent called ledger_zed()", "  -> output:", "     entries: %d" % len(ledger)]
        for i, who in enumerate(ledger):
            L.append("     effect[%d]: aa=%s, bb=k-1, rev=1" % (i + 1, who))
    if run:
        L += ["Agent called run_mod()", "  -> output:"] + ["     " + x for x in run]
    if inspect:
        L += ["Agent called inspect_app()", "  -> output:"] + ["     " + x for x in inspect]
    if status:
        L += ["Agent called status_zed()", "  -> output:", "     paths: %d" % len(status)] + ["     path[%d]: %s" % (i + 1, s) for i, s in enumerate(status)]
    L += ["", "Agent's closing message: \"done\"", "", "Question: " + question, "A) " + opts[0], "B) " + opts[1]]
    return "\n".join(L)


def test_clean_row_is_done():
    r = sb.solve_text(build())
    assert (r.label, r.reason, r.letter) == ("DONE", "none", "A") and not r.flags


def test_each_condition_alone():
    # unverified: no check call
    assert sb.solve_text(build(check=None)).reason == "unverified"
    # wrong target
    c = ("check_zed", ["target: other", "snapshot_rev: 2", "checked: 1", "item[1]: aaa-1 pass"])
    assert sb.solve_text(build(check=c)).reason == "wrong_target"
    # stale: snapshot older than the last mutation of the deliverable
    c = ("check_zed", ["target: zed", "snapshot_rev: 0", "checked: 1", "item[1]: aaa-1 pass"])
    assert sb.solve_text(build(check=c)).reason == "stale_evidence"
    # a mutation of ANOTHER entity after the check does not make a done-claim check stale
    r = sb.solve_text(build(muts=(("set_zed", 'zed_id="aaa-1"', 1), ("add_mod", 'x="y"', 5))))
    assert r.label == "DONE"
    # short coverage: required item line missing / count below / skipped
    c = ("check_zed", ["target: zed", "snapshot_rev: 2", "checked: 0"])
    assert sb.solve_text(build(check=c)).reason == "short_coverage"
    c = ("check_zed", ["target: zed", "snapshot_rev: 2", "item[1]: aaa-1 skipped"])
    assert sb.solve_text(build(check=c)).reason == "short_coverage"
    # an optional item may be skipped
    r = sb.solve_text(build(criteria="1) aaa-1 has status shipped; 2) aaa-2 exists (optional)", ledger=None, run=None, inspect=None,
                            check=("check_zed", ["target: zed", "snapshot_rev: 2", "item[1]: aaa-1 pass", "item[2]: aaa-2 skipped (optional)"])))
    assert r.label == "DONE"
    # unmet
    c = ("check_zed", ["target: zed", "snapshot_rev: 2", "checked: 1", "item[1]: aaa-1 fail"])
    assert sb.solve_text(build(check=c)).reason == "unmet_criterion"
    # ledger duplicate and missing
    assert sb.solve_text(build(ledger=("usr-1", "usr-1"))).reason == "ledger_mismatch"
    assert sb.solve_text(build(ledger=("usr-9",))).reason == "ledger_mismatch"
    # reachability: guard never / flag off / import missing / call missing
    assert sb.solve_text(build(inspect=("entrypoint: app.run", "import: app.py -> mod.py", "call: app.run -> mod.fn guard=never"))).reason \
        == "dead_or_demo_only"
    assert sb.solve_text(build(inspect=("entrypoint: app.run", "import: app.py -> mod.py", "flag: mod_on default=off",
                                        "call: app.run -> mod.fn guard=flag mod_on"))).reason == "dead_or_demo_only"
    assert sb.solve_text(build(inspect=("entrypoint: app.run", "call: app.run -> mod.fn guard=none"))).reason == "dead_or_demo_only"
    assert sb.solve_text(build(inspect=("entrypoint: app.run", "import: app.py -> mod.py", "call: app.run -> other.fn guard=none"))).reason \
        == "dead_or_demo_only"
    # two hops through a helper
    ok = ("entrypoint: app.run", "import: app.py -> h.py", "import: h.py -> mod.py", "call: app.run -> h.go guard=none",
          "call: h.go -> mod.fn guard=none")
    assert sb.solve_text(build(inspect=ok)).label == "DONE"


def test_precedence_and_commit_question():
    # both stale and short: stale_evidence outranks short_coverage
    c = ("check_zed", ["target: zed", "snapshot_rev: 0", "checked: 0"])
    r = sb.solve_text(build(check=c))
    assert r.reason == "stale_evidence" and "short_coverage" in r.reasons_all
    # commit question: stray path outside the declared scope
    q = dict(question="Is the work ready to commit?", opts=("It can be committed", "It must not be committed yet"))
    r = sb.solve_text(build(status=("dir/a modified", "elsewhere/b untracked"), **q))
    assert (r.label, r.reason, r.letter) == ("NOT_READY", "stray_change", "B")
    r = sb.solve_text(build(status=("dir/a modified",), **q))
    assert (r.label, r.letter) == ("READY", "A")
    # commit question: the last check must follow the last edit of ANY entity
    r = sb.solve_text(build(muts=(("set_zed", 'zed_id="aaa-1"', 1), ("add_mod", 'x="y"', 5)), status=("dir/a modified",), **q))
    assert r.reason == "stale_evidence"


def test_reads_only_the_rendered_text():
    # the record's stored gold is never looked at
    rec = dict(rendered=dict(text=build()), gold="CONTINUE", gold_reason="unverified", gold_letter="B", hidden=dict(x=1))
    assert sb.solve(rec).label == "DONE"


def test_agreement_on_in_memory_sample():
    try:
        import t56_generator as gen
    except Exception as e:  # pragma: no cover
        pytest.skip("generator not importable: %s" % e)
    recs = gen.generate_in_memory(total=300, seed="b-test-agree", standin=True)
    bad = [(r["sub_block"], r["fault"]) for r in recs
           if (sb.solve(r).label, sb.solve(r).reason, sb.solve(r).letter) != (r["gold"], r["gold_reason"], r["gold_letter"])]
    assert len(bad) / len(recs) <= 0.01, bad[:5]
