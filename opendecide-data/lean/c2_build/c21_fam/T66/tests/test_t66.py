"""T66 CPU tests: program model (render vs reference vs PyEval), our 3-way merge, side-test search, every conflict kind / resolution kind, every semver kind,
the MSG execution rule and swap constraints, the check-at-generation pipeline. Nothing generated is executed by this process: PyEval interprets the rendered
text (an AST walker without exec); the real gold is the sandbox's."""
import collections
import json
import os
import random
import re

import pytest

from LP_COMMON import pipeline as pl
from LP_COMMON import plan as plan_mod
from LP_COMMON import pyeval
from LP_COMMON import sandbox_iface as S
from LP_COMMON.names_guard import default_guard
from LP_COMMON.ns import Names
from T66 import checked, config as C, dryrun, gates, generator as G, merge as MG, merge3 as M3, merge_spec as MS, msg_spec as MSG, prog as P, rows as ROWS
from T66 import schema, semver as SV, semver_spec as SS, tests_gen as TG

FAMDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _ctx(executor=None, seed=1):
    return G.Ctx(seed=seed, standin=True, executor=executor)


@pytest.fixture(scope="module")
def dry():
    return dryrun.dry_rows(300, seed=11)


# --------------------------------------------------------------------------------------------------------------------- prog
def _module():
    return P.module(
        P.pipe("price", "x", "v", [P.stage("scale", k=3), P.stage("offset", c=4), P.stage("cap", cap=100), P.stage("floor", lo=2), P.stage("mod", m=97), P.stage("round", s=2),
                                    P.stage("guard", msg="neg")]),
        P.pipe("bias", "x", "v", [P.stage("affine", k=2, c=1)], bias="b"), P.build("steps", "n", "out", "i", [P.stage("append", tok="aa"), P.stage("loop", k=2, plus=1)]),
        P.table("RATES", "rate", "key", [("a", 1), ("b", 2)]), P.wrap("total", "x", "price", 5), P.wrap("total2", "x", "bias", 1, extra=[2]))


def test_reference_semantics_agree_with_pyeval_on_the_rendered_text():
    m = _module()
    text = P.render(m)
    calls = [("price", (x,), {}) for x in (-5, -1, 0, 1, 7, 40, 90, 400)] + [("bias", (3, 4), {}), ("steps", (3,), {}), ("rate", ("b",), {}), ("rate", ("zz",), {}),
                                                                                ("total", (6,), {}), ("total2", (6,), {})]
    got = pyeval.call_all({"mod.py": text}, "mod", calls)
    for (fn, args, kw), g in zip(calls, got):
        want = P.observe(m, fn, args)
        if want[0] == "ok":
            assert g == ("ok", want[1]), (fn, args)
        else:
            assert g[0] == "exc" and g[1] == want[1], (fn, args, g)


def test_edits_return_new_modules_and_do_not_touch_the_original():
    m = _module()
    before = P.render(m)
    P.set_param(m, "price", 0, k=9)
    P.swap_stages(m, "steps", 0, 1)
    P.rename_fn(m, "price", "quote")
    P.delete_stage(m, "price", 1)
    assert P.render(m) == before
    assert "def quote(x)" in P.render(P.rename_fn(m, "price", "quote")) and "quote(x) + 5" in P.render(P.rename_fn(m, "price", "quote"))


def test_pyeval_is_a_sandboxed_subset_not_exec():
    with pytest.raises(pyeval.Unsupported):
        pyeval.Module("m", {"m.py": "import socket\n"})
    with pytest.raises(pyeval.Unsupported):
        pyeval.Module("m", {"m.py": "class A:\n    x = 1\n"})
    m = pyeval.Module("m", {"m.py": "def f():\n    while True:\n        pass\n"})
    with pytest.raises(pyeval.StepBudget):
        m.call("f")
    src = open(os.path.join(os.path.dirname(pyeval.__file__), "pyeval.py"), encoding="utf-8").read()
    assert not re.search(r"(?<![\w.])(exec|eval)\(", src.replace("_eval(", "").replace("def _exec(", "")) and "compile(" not in src


# --------------------------------------------------------------------------------------------------------------------- merge3
def test_merge3_adjacent_edits_conflict_and_separated_edits_merge_cleanly():
    base = ["a", "b", "c", "d", "e"]
    segs = M3.merge3(base, ["a", "B", "c", "d", "e"], ["a", "b", "C", "d", "e"])                      # adjacent: conflict
    assert len(M3.conflicts(segs)) == 1
    segs = M3.merge3(base, ["A", "b", "c", "d", "e"], ["a", "b", "c", "d", "E"])                      # separated: clean
    assert not M3.conflicts(segs) and M3.resolve(segs, None) == ["A", "b", "c", "d", "E"]
    segs = M3.merge3(base, ["a", "b", "X", "c", "d", "e"], ["a", "b", "Y", "c", "d", "e"])            # two insertions at one point: conflict
    assert len(M3.conflicts(segs)) == 1
    same = M3.merge3(base, ["a", "B", "c", "d", "e"], ["a", "B", "c", "d", "e"])
    assert not M3.conflicts(same)


def test_conflict_view_round_trips_and_has_diff3_markers():
    segs = M3.merge3(["a", "b", "c"], ["a", "B", "c"], ["a", "b2", "c"])
    view = M3.render_view(segs)
    assert M3.MARK_OURS in view and M3.MARK_BASE in view and M3.MARK_THEIRS in view
    assert M3.parse_view(view) == [(s[0],) + tuple(s[1:]) for s in segs]


# --------------------------------------------------------------------------------------------------------------------- tests_gen
@pytest.mark.parametrize("kind", MG.CF_IDS)
def test_side_tests_obey_the_strength_rules_on_the_reference_semantics(kind):
    for t in range(6):
        rng = random.Random(t)
        pool = MG.Pool(Names("T66t", "s%d" % t), rng)
        c = MG.build_cf(kind, pool, rng)
        ta, tb = MG.tests_for(c, c, rng)
        assert all(x.passes(c["A"]) and x.passes(c["AB"]) for x in ta) and any(not x.passes(c["base"]) for x in ta) and any(not x.passes(c["B"]) for x in ta)
        assert all(x.passes(c["B"]) and x.passes(c["AB"]) for x in tb) and any(not x.passes(c["base"]) for x in tb) and any(not x.passes(c["A"]) for x in tb)
        assert TG.suite_text("stem", ta, tag="a").count("\n") <= MS.LINES_MAX


# --------------------------------------------------------------------------------------------------------------------- MERGE
@pytest.mark.parametrize("kind", MG.CF_IDS)
def test_every_conflict_kind_and_resolution_kind_has_the_expected_label(kind):
    ctx = _ctx(S.SimExecutor())
    seen = collections.Counter()
    for rk in MG.RK_IDS:
        for t in range(3):
            g = {"gid": "G-%s-%s-%d" % (kind, rk, t), "seed": "m%s%s%d" % (kind, rk, t)}
            try:
                sp = MS.build_group(ctx, g, {"cf": kind, "rks": [rk]})[0]
            except MG.Reject:
                continue
            seen[rk] += 1
            if rk in MG.EXPECT:
                assert sp["label"] == MG.EXPECT[rk], (kind, rk)
            assert MS.label_from_witness(sp["witness"]) == sp["label"]
            assert all(v["A_det"] if "A_det" in v else True for v in sp["strength"].values())
    assert set(seen) >= {"RK1", "RK2", "RK5", "RK6", "RK7", "RK8"}


def test_rk8_is_a_syntax_break_and_rk3_rk4_depend_on_the_conflict_kind():
    ctx = _ctx(S.SimExecutor())
    sp = MS.build_group(ctx, {"gid": "g1", "seed": "s1"}, {"cf": "CF-1", "rks": ["RK8"]})[0]
    with pytest.raises(SyntaxError):
        compile_check(sp["resolution"])
    labs = collections.defaultdict(set)
    for kind in MG.CF_IDS:
        for rk in ("RK3", "RK4"):
            for t in range(3):
                try:
                    labs[kind].add(MS.build_group(ctx, {"gid": "g%s%s%d" % (kind, rk, t), "seed": "q%s%s%d" % (kind, rk, t)}, {"cf": kind, "rks": [rk]})[0]["label"])
                except MG.Reject:
                    pass
    assert labs["CF-5"] == {"YES"} and labs["CF-1"] == {"NO"}


def compile_check(text):
    import ast
    ast.parse(text)


def test_a_nondeterministic_executor_cannot_produce_a_merge_row():
    class Flaky(S.SimExecutor):
        def run(self, requests):
            return [dict(r, deterministic=False) for r in super().run(requests)]
    with pytest.raises(MG.Reject):
        MS.build_group(_ctx(Flaky()), {"gid": "g", "seed": "s"}, {"cf": "CF-1", "rks": ["RK5"]})


def test_a_wrong_executor_report_breaks_the_strength_rule():
    class Lying(S.SimExecutor):
        def run(self, requests):
            out = super().run(requests)
            for r in out:
                r["states"] = {k: "pass" for k in r["states"]}
            return out
    with pytest.raises(MG.Reject):
        MS.build_group(_ctx(Lying()), {"gid": "g", "seed": "s"}, {"cf": "CF-1", "rks": ["RK5"]})


def test_merge_pair_shares_conflict_and_tests_and_flips_the_label():
    sp = MS.build_group(_ctx(S.SimExecutor()), {"gid": "g", "seed": "pair"}, {"cf": "CF-3", "rks": ["RK5", "RK7"]})
    a, b = sp
    assert a["view"] == b["view"] and a["test_a"] == b["test_a"] and a["test_b"] == b["test_b"] and a["label"] == "YES" and b["label"] == "NO"
    assert a["resolution"] != b["resolution"]


# --------------------------------------------------------------------------------------------------------------------- SEMVER
@pytest.mark.parametrize("sv", SV.SV_IDS)
def test_every_semver_kind_has_its_label_and_executor_matches_reference(sv):
    ctx = _ctx(S.SimExecutor())
    wanted = {"break": "BREAKING", "safe": "SAFE"}
    got = 0
    for variant in (["break"], ["safe"]):
        if sv in SV.SAFE_KINDS and variant == ["break"]:
            continue
        for t in range(5):
            g = {"gid": "S-%s-%s-%d" % (sv, variant[0], t), "seed": "v%s%s%d" % (sv, variant[0], t)}
            try:
                specs = SS.build_group(ctx, g, {"sv": sv, "variants": variant, "bump": t % 2 == 0})
            except SV.Reject:
                continue
            got += 1
            assert specs[0]["label"] == wanted[variant[0]], (sv, variant)
            assert SV.label_from_witness(specs[0]["witness"]) == specs[0]["label"]
    assert got >= 3


def test_semver_pair_has_the_same_old_api_and_callers_and_opposite_labels():
    ctx = _ctx(S.SimExecutor())
    for sv in ("SV-C1", "SV-C7", "SV-C8", "SV-C10"):
        specs = SS.build_group(ctx, {"gid": "p" + sv, "seed": "pp" + sv}, {"sv": sv, "variants": ["break", "safe"], "bump": False})
        a, b = specs
        assert a["old"] == b["old"] and a["callers"] == b["callers"] and (a["label"], b["label"]) == ("BREAKING", "SAFE")


def test_gold_sanity_failure_on_the_old_api_gives_no_label():
    w = {"old": {"ok": True, "passed": False}, "new": {"ok": True, "passed": True}}
    assert SV.label_from_witness(w) is None
    assert SV.label_from_witness({"old": {"ok": True, "passed": True}, "new": {"ok": False, "passed": True}}) is None


def test_declared_bump_is_a_decoy():
    ctx = _ctx(S.SimExecutor())
    agree = shown = 0
    for t in range(80):
        try:
            sp = SS.build_group(ctx, {"gid": "b%d" % t, "seed": "bb%d" % t}, {"sv": ["SV-C1", "SV-C2", "SV-C8", "SV-C9"][t % 4], "variants": ["break"], "bump": True})[0]
        except SV.Reject:
            continue
        shown += 1
        agree += (sp["bump"] == "major") == (sp["label"] == "BREAKING")
    assert shown > 50 and 0.35 <= agree / shown <= 0.65


# --------------------------------------------------------------------------------------------------------------------- MSG
def test_behaviour_preserving_change_kinds_never_realise():
    pool = MG.Pool(Names("T66t", "x"), random.Random(1))
    mod, ids = MSG.base_module(pool, random.Random(1))
    for ch in MSG.CH_NEVER:
        with pytest.raises(MSG.Reject):
            MSG.substantive(ch, mod, ids, pool, random.Random(1))


def test_msg_substantive_hunk_changes_the_probe_and_trivial_hunks_do_not(dry):
    rows = [r for r in dry[0] if r["head"] == "MSG"]
    assert rows
    ctx = _ctx(S.SimExecutor())
    for t in range(6):
        specs = MSG.build_group(ctx, {"gid": "m%d" % t, "seed": "mm%d" % t}, {"chs": ["CH-1", "CH-3"], "trivial": [2, 1]})
        for s in specs:
            assert s["probe"]["sub_differs"] and s["probe"]["trivials_identical"] and s["probe"]["base"] != s["probe"]["sub"]
            assert len(s["trivials"]) <= 2 and s["diff"].startswith("--- a/")


def test_msg_rows_pair_yes_and_no_on_one_diff_with_the_swap_constraints(dry):
    by = collections.defaultdict(list)
    for r in dry[0]:
        if r["head"] == "MSG":
            by[r["meta"]["pair_id"]].append(r)
    assert by
    kinds = collections.Counter()
    for pid, rs in by.items():
        assert len(rs) == 2 and {x["gold"] for x in rs} == {"YES", "NO"}
        yes, no = (rs[0], rs[1]) if rs[0]["gold"] == "YES" else (rs[1], rs[0])
        assert yes["spec"]["diff"] == no["spec"]["diff"]
        assert len(no["spec"]["message"].split()) >= 4 and MSG.jaccard(no["spec"]["message"], yes["spec"]["message"]) < 0.5
        kinds[no["spec"]["origin"]] += 1
    assert kinds["swap"] and kinds["trivial"]


def test_unified_diff_hunk_counts_are_consistent():
    from T66.roundtrip import _diff_ok
    base = ["a", "b", "c", "d", "e", "f", "g", "h"]
    new = ["a", "b", "X", "d", "e", "f", "g", "H", "i"]
    assert _diff_ok(MSG.unified("stem", base, new))
    assert not _diff_ok(MSG.unified("stem", base, new).replace("@@ -1,", "@@ -1,9"))


# --------------------------------------------------------------------------------------------------------------------- pipeline
def test_rows_use_frozen_names_hooks_and_have_no_internal_ids(dry):
    rows, summary, log, _ = dry
    g = default_guard()
    assert summary["kept"] == len(rows) and rows
    for r in rows:
        assert g.check("T66", r["names"]) == []
        assert r["meta"]["template_id"] and r["meta"]["wording_id"] and r["meta"]["construction_id"] and r["meta"]["ladder"] in ("L1", "L2", "L3", "L4")
        assert r["stamp"]["verdict"] == "clean"
        t = r["rendered"]["text"]
        for tok in C.FORBIDDEN_IDS:
            assert not re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(tok), t), tok
        assert not re.search(r"<<<<<<<|>>>>>>>", r["spec"].get("resolution", ""))


def test_b_view_has_no_label_spec_or_witness(dry):
    r = dry[0][0]
    v = schema.b_view(r)
    assert set(v) == set(schema.B_VIEW_FIELDS) and "spec" not in v and "gold" not in v
    assert "'witness':" not in repr(v) and "'strength'" not in repr(v) and "passed" not in repr(v)


def test_pipeline_requirements_and_production_executor_rules():
    ad = checked.adapter()
    ctx = _ctx(S.SimExecutor())
    with pytest.raises(pl.StampServiceRequired):
        pl.run_checked(ad, 10, 1, pl.RefusingHook(), standin=True, ctx=ctx)
    with pytest.raises(pl.SolverBRequired):
        pl.run_checked(ad, 10, 1, pl.TestDoubleHook(), standin=False, ctx=ctx)
    with pytest.raises(ValueError):
        G.Ctx(seed=1, standin=False, pool={"test_only": False, "forms": {}}, executor=S.SimExecutor())
    with pytest.raises(ValueError):
        G.Ctx(seed=1, standin=False, pool={"test_only": False, "forms": {}}, executor=None)


def test_g13_hit_retires_the_whole_group():
    plan = G.build_plan(total=100, seed=2)
    grp = next(g for g in plan if g["head"] == "MSG")
    hook = pl.TestDoubleHook(hit_if=lambda it: it["row_id"] == grp["gid"] + "-a")
    rows, summary, log, _ = checked.run(100, 2, hook, standin=True)
    assert not any(r["group_id"] == grp["gid"] for r in rows)
    assert summary["retired_groups"] >= 1 and summary["dropped"].get("g13:g13_hit") == 1 and summary["dropped"].get("g13:group_member_of_hit") == 3
    # a NEW spec with a new seed is generated for the retired cell (GV5). It need not be KEPT: the reuse ledger keys on the base group id, so the 4 rows of the retired MSG group
    # still count against its refill (4 + 4 > 6) and the refill is dropped as incomplete (pipeline behaviour, unchanged); any other lost group refills the same way.
    assert summary["refills"] >= 1 and any(l["group_id"] == grp["gid"] + "~r1" for l in log)


def test_job_lines_are_the_executor_format():
    rq = S.tests_request("r", {"m.py": "x = 1\n", "test_m.py": "def test_a():\n    assert True\n"}, "test_m.py")
    line = S.to_job_line(rq)
    assert line["toolchain"] == "python" and line["will_this_test_fail"] and line["argv"][:3] == ["python", "-I", "od_run_tests.py"]
    assert json.loads(json.dumps(line)) == line
    with pytest.raises(S.LanguagePending):
        S.SimExecutor().run([dict(rq, lang="go")])
    col = S.CollectingExecutor()
    with pytest.raises(S.NeedsResults):
        col.run([rq])


def test_gates_run_and_scope_asserts_hold(dry):
    out = gates.run_all(dry[0])
    ok = {g["id"]: g["ok"] for g in out}
    for gid in ("T66-K1", "T66-K2", "T66-K12", "T66-K13", "T66-K14", "T66-K16", "T66-K17", "T66-K18", "T66-K21"):
        assert ok[gid], gid
    assert not ok["T66-K11"]                                    # Python only until the image record: the gate says so


def test_no_exec_no_network_no_git_and_no_barred_paths():
    bar = re.compile(r"(?i)(ohs5?[_/-]|ohs-ac|ohs[0-9]|sealed[_/-]|[/_]sealed|~/\.claude|\.claude/)")
    for f in os.listdir(FAMDIR):
        if f.endswith(".py"):
            src = open(os.path.join(FAMDIR, f), encoding="utf-8").read()
            assert not bar.search(src), f
            assert not re.search(r"^\s*(import|from)\s+(requests|urllib3|anthropic|openai|socket|http\.client|subprocess)\b", src, re.M), f
    assert gates.k21_scope([])["ok"]


def test_determinism():
    a = dryrun.dry_rows(60, seed=5)[0]
    b = dryrun.dry_rows(60, seed=5)[0]
    assert [r["rendered"]["text"] for r in a] == [r["rendered"]["text"] for r in b]
