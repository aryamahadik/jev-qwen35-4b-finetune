"""T42c tests: generator heads, pairs, Solver A witness rules (with fault injection), planner, gates, clean-room checks.
No generated code is executed anywhere: SimExecutor predicts witnesses from the IR interpreter."""
import builtins
import copy
import collections
import json
import os
import random
import re
import subprocess

import pytest

from LC_COMMON import ir as I
from LC_COMMON import sandbox_iface as S
from LC_COMMON import transforms as T
from LC_COMMON import wording
from LC_COMMON.names_guard import default_guard

from T42c import config as C
from T42c import eqv2, gates, out4, rows as ROWS, solver_a, tfail2
from T42c.base import Skip, row_names
from T42c.build import build_rows, make_specs
from T42c.dryrun import dry_rows
from T42c.planner import Planner

LANGS = ("python", "javascript", "typescript", "go", "bash")


@pytest.fixture(scope="module")
def dry():
    return dry_rows(30, seed=2, chunk=10)


def _picker(seed=1):
    pool = wording.make_test_pool(list(C.QUESTION_FORM.values()))
    return wording.Picker(pool, random.Random(seed)), pool


def _first(fn, cells, tries=40):
    for k in range(tries):
        try:
            return fn(cells, k)
        except Skip:
            continue
    raise AssertionError("no candidate for %r" % (cells,))


# ------------------------------------------------------------------------------------------------ names + config
def test_names_for_every_head_and_language_are_on_the_frozen_list():
    g = default_guard()
    for head in C.HEADS:
        for lang in LANGS:
            names = row_names(head, lang)
            assert g.check("T42c", names) == []
            assert names["language"] == [lang]
            assert set(names["carrier"]) <= set(C.CARRIERS[head])
            assert set(names["runner"]) <= {"runner.python_isolated", "runner.node_test", "runner.go_test", "runner.bash_posix_test",
                                            "runner.twin_counters." + lang, "runner.domain_enumerator." + lang}


def test_shares_and_bars_follow_the_g0_lite():
    assert abs(sum(C.HEAD_SHARE.values()) - 1) < 1e-9 and abs(sum(C.LANG_SHARE.values()) - 1) < 1e-9
    assert C.LANG_SHARE["python"] <= C.PYTHON_CAP
    assert C.LANG_SHARE["javascript"] + C.LANG_SHARE["typescript"] >= 0.08 and C.LANG_SHARE["go"] >= 0.08 and C.LANG_SHARE["bash"] >= 0.08
    assert (C.BIN_AUC_MAX, C.BIN_UPPER_MAX) == (0.55, 0.60) and (C.K4_ACC_MAX, C.K4_UPPER_MAX) == (0.28, 0.31)
    assert C.WITNESS_RUNS == 3                              # Opus ruling (a): the 3-run witness rule wins


# ------------------------------------------------------------------------------------------------ OUT4
@pytest.mark.parametrize("lang", LANGS)
def test_out4_options_are_distinct_one_gold_and_a_near_miss(lang):
    for exc in (False, True):
        spec = _first(lambda c, s: out4.gen_out4(c, s), {"lang": lang, "exc": exc, "bin": "mid", "gold_pos": 2})
        texts = [o["text"] for o in spec["options"]]
        assert len(set(texts)) == 4
        assert sum(o["kind"] == "GOLD" for o in spec["options"]) == 1
        assert spec["gold_index"] == 2 and spec["options"][2]["kind"] == "GOLD"
        assert "EXEC-NEARMISS" in [o["kind"] for o in spec["options"]]
        assert spec["meta"]["exc_gold"] == exc
        assert spec["options"][2]["obs"] == spec["gold_obs"]


def test_out4_exception_text_is_language_native():
    seen = {}
    for lang in LANGS:
        spec = _first(lambda c, s: out4.gen_out4(c, s), {"lang": lang, "exc": True, "bin": "lt10", "gold_pos": 0})
        seen[lang] = spec["options"][0]["text"]
    assert seen["python"].startswith("raises ") and seen["javascript"].startswith("throws ")
    assert seen["go"].startswith("panics with ") and seen["bash"].startswith("exits with status ")


def test_out4_distractors_never_equal_each_other_or_gold():
    for lang in ("python", "go"):
        for k in range(10):
            try:
                spec = out4.gen_out4({"lang": lang, "exc": False, "bin": "lt10", "gold_pos": k % 4}, k)
            except Skip:
                continue
            keys = [I.canon(o["obs"]) for o in spec["options"]]
            assert len(set(keys)) == 4


def test_out4_pair_partners():
    inv = None
    for s0 in range(40):
        try:
            spec = out4.gen_out4({"lang": "python", "exc": False, "bin": "mid", "gold_pos": 1}, s0)
            inv = out4.make_pair(spec, "invariant", s0)
            break
        except Skip:
            continue
    assert inv is not None
    assert inv["gold_obs"] == spec["gold_obs"] and inv["meta"]["pair_kind"] == "invariant"
    assert I.norm_hash(inv["lo"]) != I.norm_hash(spec["lo"]) or inv["meta"]["construction"] in T.IDS
    near = None
    for s in range(30):
        try:
            sp = out4.gen_out4({"lang": "python", "exc": False, "bin": "mid", "gold_pos": 1}, s)
            near = out4.make_pair(sp, "nearmiss", s)
            break
        except Skip:
            continue
    assert near is not None
    assert near["gold_obs"] != sp["gold_obs"]
    kinds = [o["kind"] for o in near["options"]]
    assert kinds.count("GOLD") == 1 and "PAIR-OLD-GOLD" in kinds           # the old gold became a distractor
    assert {I.canon(o["obs"]) for o in near["options"]} == {I.canon(o["obs"]) for o in sp["options"]}


def test_order_invariance_copy_is_a_non_identity_permutation_with_matching_label(dry):
    rows = dry[0]
    o = [r for r in rows if r["head"] == "OUT4" and not r["meta"].get("perm_copy")]
    picker, _ = _picker()
    for r in o[:6]:
        c = ROWS.permuted_row(r, random.Random(5), "copy", picker)
        assert c["meta"]["perm"] != list(range(4))
        gold_text = r["meta"]["options"][r["meta"]["gold_index"]]["text"]
        assert c["meta"]["options"][c["meta"]["gold_index"]]["text"] == gold_text
        assert c["label"] == "ABCD"[c["meta"]["gold_index"]]
        assert {x["text"] for x in c["meta"]["options"]} == {x["text"] for x in r["meta"]["options"]}


# ------------------------------------------------------------------------------------------------ EQV2
def test_eqv2_yes_rows_carry_a_registered_construction_and_exhaustive_equality():
    for eq in T.IDS:
        spec = None
        for s in range(60):
            try:
                spec = eqv2.gen_eqv2({"lang": "python", "label": "YES", "eq": eq}, s)
                break
            except Skip:
                continue
        assert spec is not None, eq
        assert spec["meta"]["construction"] == eq
        assert C.DOMAIN_MIN <= spec["domain_size"] <= C.DOMAIN_MAX
        ref, _, _ = eqv2.outcomes(spec["lo"], "python", spec["target"])
        got, _, _ = eqv2.outcomes(spec["lo_b"], "python", spec["target"])
        assert ref == got                                    # exhaustive agreement over the declared domain


def test_eqv2_no_rows_have_a_distinguishing_input_and_hard_no_is_rare_difference():
    soft = hard = 0
    for s in range(80):
        try:
            spec = eqv2.gen_eqv2({"lang": "python", "label": "NO", "op": None, "hard": s % 2 == 0}, s)
        except Skip:
            continue
        d = spec["info"]["distinguishing"]
        assert d is not None
        a, _, _ = eqv2.outcomes(spec["lo"], "python", spec["target"])
        b, _, _ = eqv2.outcomes(spec["lo_b"], "python", spec["target"])
        diff = [k for k in range(len(a)) if a[k] != b[k]]
        assert diff and abs(len(diff) / len(a) - spec["info"]["diff_fraction"]) < 1e-9
        if spec["info"]["hard_no"]:
            hard += 1
            assert len(diff) / len(a) <= C.HARD_NO_MAX_DIFF and spec["domain_size"] >= 50
        else:
            soft += 1
            assert len(diff) / len(a) > C.HARD_NO_MAX_DIFF
    assert hard >= 2 and soft >= 2


def test_eqv2_stateful_domain_uses_sequences_with_a_snapshot():
    for s in range(120):
        try:
            spec = eqv2.gen_eqv2({"lang": "python", "label": "YES", "eq": "EQ-YES-1", "seq": True}, s)
        except Skip:
            continue
        if spec["target"]["mode"] == "seq":
            assert spec["target"]["snapshot"] and "call sequence" in spec["domain_text"]
            return
    raise AssertionError("no stateful EQV2 row found")


def test_eqv2_shows_pruned_pair_not_whole_modules():
    spec = _first(lambda c, s: eqv2.gen_eqv2(c, s), {"lang": "go", "label": "YES", "eq": "EQ-YES-1"})
    assert len(spec["shown"]) == 2 and spec["shown"][0]["text"] != "" and spec["shown"][1]["text"] != ""
    full = sum(len(t) for t in __import__("LC_COMMON.render", fromlist=["x"]).render_module(spec["lo"], "go").values())
    assert len(spec["shown"][0]["text"]) <= full + 40


# ------------------------------------------------------------------------------------------------ TFAIL2
@pytest.mark.parametrize("lang", LANGS)
def test_tfail2_labels_agree_with_the_interpreter(lang):
    for label, mode in (("PASS", "expected"), ("FAIL", "expected"), ("FAIL", "program")):
        spec = _first(lambda c, s: tfail2.gen_tfail2(c, s), {"lang": lang, "label": label, "fail_mode": mode})
        from LC_COMMON.interp import Interp
        it = Interp(spec["lo"], lang)
        ok = True
        for s in spec["steps"]:
            o = it.call(s["fn"], s["args"])
            if s["op"] == "eq" and o != ("ok", s["expect"]):
                ok = False
            if s["op"] == "raises" and o != ("exc", s["err"]):
                ok = False
        assert ok == (label == "PASS")
        assert spec["test_path"] in ("test_%s.py" % spec["stem"], "%s.test.js" % spec["stem"], "%s.test.mts" % spec["stem"],
                                     "%s_test.go" % spec["stem"], "test_%s.sh" % spec["stem"])


def test_tfail2_assertion_count_and_shapes():
    seen = set()
    for s in range(120):
        try:
            sp = tfail2.gen_tfail2({"lang": "python", "label": "PASS"}, s)
        except Skip:
            continue
        assert 1 <= sp["meta"]["n_assert"] <= 4
        seen.add(sp["shape"])
    assert {"value", "multi"} <= seen


def test_tfail2_nearmiss_partner_flips_the_label():
    for s in range(60):
        try:
            sp = tfail2.gen_tfail2({"lang": "python", "label": "PASS", "fail_mode": "expected"}, s)
            pr = tfail2.make_pair(sp, "nearmiss", s)
        except Skip:
            continue
        assert sp["gold_label"] == "PASS" and pr["gold_label"] == "FAIL" and pr["test_text"] == sp["test_text"]
        return
    raise AssertionError("no near-miss pair found")


# ------------------------------------------------------------------------------------------------ Solver A
def test_dry_run_builds_rows_in_memory_only(dry, tmp_path, monkeypatch):
    rows, log, skips, pool = dry
    assert len(rows) >= 24
    heads = collections.Counter(r["head"] for r in rows)
    assert set(heads) == {"OUT4", "EQV2", "TFAIL2"}
    for r in rows:
        assert set(["row_id", "family", "head", "lang", "label", "carriers", "prompt_text", "names", "meta", "manifest"]) <= set(r)
        assert r["label"] in (list("ABCD") if r["head"] == "OUT4" else ["YES", "NO"])
        assert r["meta"]["tokens"] > 0 and default_guard().check("T42c", r["names"]) == []
        assert r["manifest"]["solver_a_version"] == solver_a.SOLVER_A_VERSION
    assert len({r["row_id"] for r in rows}) == len(rows)
    before = set(os.listdir(tmp_path))
    monkeypatch.chdir(tmp_path)
    dry_rows(10, seed=9)
    assert set(os.listdir(tmp_path)) == before            # nothing is written to disk


def test_no_generated_code_is_executed(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("generated code must never run on the CPU side")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(os, "system", boom)
    monkeypatch.setattr(builtins, "exec", boom)
    monkeypatch.setattr(builtins, "eval", boom)
    rows, log, _, _ = dry_rows(12, seed=4)
    assert rows


def test_requests_carry_three_runs_and_a_separate_twin_for_steps(dry):
    spec = _first(lambda c, s: out4.gen_out4(c, s), {"lang": "python", "exc": False, "bin": "mid", "gold_pos": 0})
    reqs = solver_a.requests_for(dict(spec, row_id="r1"), "r1")
    assert reqs["gold"]["repeats"] == 3 and reqs["gold"]["purpose"] == "witness"
    assert reqs["steps"]["purpose"] == "steps" and "odc.py" in reqs["steps"]["files"]
    assert any(k.startswith("opt") for k in reqs)
    for rq in reqs.values():
        line = S.to_job_line(rq)
        assert line["repeats"] == 3 and json.dumps(line)


def test_unexpected_result_is_dropped_and_counted_never_relabelled():
    picker, _ = _picker()
    spec = _first(lambda c, s: out4.gen_out4(c, s), {"lang": "python", "exc": False, "bin": "lt10", "gold_pos": 1})
    spec["row_id"] = "T42c-OUT4-000001"

    def flip(res):
        res = dict(res)
        res["stdout"] = '@@OD@@{"ok":123456}\n'
        return res
    ex = S.SimExecutor(faults={"T42c-OUT4-000001#gold": flip})
    rows, log = solver_a.SolverA(ex, picker).run([spec])
    assert rows == [] and log.counts["unexpected_result"] == 1


def test_nondeterministic_witness_is_dropped():
    picker, _ = _picker()
    spec = _first(lambda c, s: out4.gen_out4(c, s), {"lang": "python", "exc": False, "bin": "lt10", "gold_pos": 1})
    spec["row_id"] = "rowx"
    rows, log = solver_a.SolverA(S.SimExecutor(nondeterministic=["rowx#gold"]), picker).run([spec])
    assert rows == [] and log.counts["nondeterministic"] == 1


def test_eqv2_witness_rules_yes_needs_equal_domain_output_and_no_needs_a_distinguishing_run():
    picker, _ = _picker()
    yes = _first(lambda c, s: eqv2.gen_eqv2(c, s), {"lang": "python", "label": "YES", "eq": "EQ-YES-1"})
    no = _first(lambda c, s: eqv2.gen_eqv2(c, s), {"lang": "python", "label": "NO", "op": None, "hard": False})
    yes["row_id"], no["row_id"] = "ey", "en"
    rows, log = solver_a.SolverA(S.SimExecutor(), picker).run([yes, no])
    assert [r["label"] for r in rows] == ["YES", "NO"] and not log.counts
    assert rows[1]["manifest"]["distinguishing"]["A"] != rows[1]["manifest"]["distinguishing"]["B"]
    assert rows[0]["manifest"]["construction"] == "EQ-YES-1"

    def make_unequal(res):
        return dict(res, stdout=res["stdout"] + "@@ODP@@{\"ok\":0}\n")
    yes2 = _first(lambda c, s: eqv2.gen_eqv2(c, s), {"lang": "python", "label": "YES", "eq": "EQ-YES-4"})
    yes2["row_id"] = "ey2"
    rows2, log2 = solver_a.SolverA(S.SimExecutor(faults={"ey2#domB": make_unequal}), picker).run([yes2])
    assert rows2 == [] and log2.counts["unexpected_result"] == 1


def test_tfail2_label_follows_test_outcome_and_failing_exit_is_not_a_drop():
    picker, _ = _picker()
    f = _first(lambda c, s: tfail2.gen_tfail2(c, s), {"lang": "go", "label": "FAIL", "fail_mode": "expected"})
    p = _first(lambda c, s: tfail2.gen_tfail2(c, s), {"lang": "python", "label": "PASS"})
    f["row_id"], p["row_id"] = "tf", "tp"
    rows, log = solver_a.SolverA(S.SimExecutor(), picker).run([f, p])
    assert {r["row_id"]: r["label"] for r in rows} == {"tf": "YES", "tp": "NO"} and not log.counts


def test_trace_bin_comes_from_the_twin_run_not_the_witness(dry):
    for r in dry[0]:
        assert r["manifest"]["bin_final"] == r["meta"]["trace_bin"]
        assert r["manifest"]["steps_final"] is not None and r["manifest"]["steps_final"] > 0


def test_lint_hit_drops_the_row(monkeypatch):
    from LC_COMMON import lint
    picker, _ = _picker()
    spec = _first(lambda c, s: out4.gen_out4(c, s), {"lang": "python", "exc": False, "bin": "lt10", "gold_pos": 3})
    spec["row_id"] = "lint1"
    monkeypatch.setitem(lint.PATTERNS, "python", lint.PATTERNS["python"] + [r"def "])
    lint._CACHE.clear()
    rows, log = solver_a.SolverA(S.SimExecutor(), picker).run([spec])
    lint._CACHE.clear()
    assert rows == [] and log.counts["lint"] == 1


# ------------------------------------------------------------------------------------------------ planner
def test_planner_balances_each_axis_by_deficit():
    assert Planner(7).unit() == Planner(7).unit()          # deterministic
    p2 = Planner(3)
    got = collections.Counter()
    for _ in range(200):
        c = p2.unit()
        specs_like = {"head": c["head"], "lang": c["lang"], "meta": {}, "bin_ir": c.get("bin"), "gold_index": c.get("gold_pos"),
                      "gold_label": c.get("label")}
        p2.add({"head": c["head"], "lang": c["lang"], "pair_kind": c["unit"] if c["unit"] != "single" else None, "bin": c.get("bin"),
                "perm": False, "exc": c.get("exc", False), "letter": c.get("gold_pos"), "label": c.get("label"),
                "construction": c.get("eq"), "op": c.get("op"), "hard": c.get("hard", False), "shape": c.get("shape"),
                "n_assert": c.get("n_assert"), "cell": None})
        got[c["head"]] += 1
    assert abs(got["OUT4"] / 200 - 0.4) < 0.05 and abs(got["EQV2"] / 200 - 0.3) < 0.05


def test_ts_folds_into_js_when_type_stripping_fails():
    p = Planner(1, ts_ok=False)
    assert "typescript" not in p.langs and abs(p.langs["javascript"] - 0.10) < 1e-9


# ------------------------------------------------------------------------------------------------ gates
def _fake_rows(n, head="EQV2", leak=False, seed=0):
    rng = random.Random(seed)
    rows = []
    for k in range(n):
        yes = rng.random() < 0.5
        base = {"row_id": "r%d" % k, "head": head, "lang": "python", "label": "YES" if yes else "NO",
                "carriers": {"SRC_FILE": [{"path": "a.py", "lang": "python", "text": "def f():\n    return 1\n"}],
                            "TEST_FILE": {"path": "t.py", "text": "def test_x():\n    assert f() == 1\n"}},
                "meta": {"base_module": "m%d" % k, "trace_steps": 5 + (30 if (leak and yes) else rng.randint(0, 20)),
                         "trace_bin": "lt10", "src_lines": 10, "tokens": 100, "ir": {"loops": 1, "calls": 1},
                         "similarity": 0.5, "len_ratio": 1.0, "edit_ratio": 0.5, "ast_nodes_a": 5, "ast_nodes_b": 5, "changed_lines": 2,
                         "expected_in_source": rng.random() < 0.5, "norm_hash": "h%d" % k, "tokens_": 0, "wording_id": "t%03d" % (k % 50)},
                "manifest": {}, "names": row_names(head, "python")}
        rows.append(base)
    return rows


def test_k5_catches_a_planted_length_leak_and_passes_noise():
    noise = gates.k5(_fake_rows(600, "EQV2", leak=False) + _fake_rows(600, "TFAIL2", leak=False, seed=3))
    leak = gates.k5(_fake_rows(600, "EQV2", leak=True) + _fake_rows(600, "TFAIL2", leak=False, seed=3))
    assert noise["detail"]["EQV2"]["status"] in (gates.PASS, "INVALID_REPEAT")
    assert leak["detail"]["EQV2"]["status"] == gates.FAIL and leak["detail"]["EQV2"]["auc"] > 0.8


def test_k11_k13_k15_catch_planted_defects():
    rows = _fake_rows(100, "TFAIL2")
    for r in rows:
        r["meta"].update({"pair_kind": None, "distractor_kinds": []})
    assert gates.k11(rows)["status"] == gates.FAIL          # all python, no pairs
    rows[1]["meta"]["norm_hash"] = rows[0]["meta"]["norm_hash"]
    rows[3]["meta"]["norm_hash"] = rows[2]["meta"]["norm_hash"]
    assert gates.k13(rows)["status"] == gates.FAIL          # 2% duplicates
    rows[0]["names"]["language"] = ["ruby"]
    assert gates.k15(rows)["status"] == gates.FAIL
    rows[0]["names"]["language"] = ["python"]
    rows[0]["carriers"]["SRC_FILE"][0]["text"] = "import random\n"
    assert gates.k12(rows)["status"] == gates.FAIL


def test_k4_k10_flag_skewed_rows():
    rows = _fake_rows(100, "OUT4")
    for r in rows:
        r["label"] = "A"
        r["meta"].update({"trace_bin": "lt10", "exc_gold": False, "options": [], "pair_kind": None})
    assert gates.k4(rows)["status"] == gates.FAIL
    assert gates.k10(rows)["status"] == gates.FAIL


def test_k1_requires_complete_manifests(dry):
    rows = dry[0]
    assert gates.k1(rows)["status"] == gates.PASS
    import copy
    bad = copy.deepcopy(rows[:3])
    del bad[0]["manifest"]["witness"]
    assert gates.k1(bad)["status"] == gates.FAIL


def test_dry_run_gate_smoke(dry):
    rows, _, _, pool = dry
    res = gates.run_gates(rows, pool=pool, n_target=len(rows))
    st = gates.summarize(res)
    assert st["K3"] == gates.PENDING and st["K16"] == gates.PENDING and st["K17"] == gates.PENDING
    assert st["K1"] == gates.PASS and st["K2"] == gates.PASS and st["K12"] == gates.PASS and st["K15"] == gates.PASS
    assert st["K5"] == gates.UNDER and st["K6"] == gates.UNDER          # too few rows for the probes, never a silent PASS


def test_solver_b_view_hides_labels_and_gold(dry):
    from T42c import schema
    for r in dry[0][:8]:
        v = schema.b_view(r)
        text = json.dumps(v)
        assert "label" not in v and "manifest" not in v
        assert r["manifest"]["solver_a_version"] not in text
        assert "kind" not in text or "GOLD" not in text


# ------------------------------------------------------------------------------------------------ clean room
def test_family_code_does_not_reference_forbidden_inputs():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    common = os.path.join(os.path.dirname(here), "LC_COMMON")
    bad = re.compile(r"ohs|sealed|mutate\.py|PLAN_v3|SKEPTIC|OHS5_BRIEF|research_v3", re.I)
    for root in (here, common):
        for dirpath, _, files in os.walk(root):
            for f in files:
                if f.endswith((".py", ".md")) and "tests" not in dirpath.split(os.sep):
                    txt = open(os.path.join(dirpath, f), encoding="utf-8").read()
                    assert not bad.search(txt), os.path.join(dirpath, f)


# ------------------------------------------------------------------------------------------------ added: copies, reuse, step agreement
def test_eqv2_reversed_copy_swaps_the_programs_and_keeps_the_label(dry):
    rows = [r for r in dry[0] if r["head"] == "EQV2" and not r["meta"].get("perm_copy")]
    assert rows
    pk, _ = _picker()
    for r in rows[:4]:
        c = ROWS.reversed_row(r, "copy", pk)
        a, b = r["carriers"]["PROGRAM_PAIR"]
        ca, cb = c["carriers"]["PROGRAM_PAIR"]
        assert ca["blocks"] == b["blocks"] and cb["blocks"] == a["blocks"] and c["label"] == r["label"] and c["meta"]["perm"] == [1, 0]
        assert c["prompt_text"] != r["prompt_text"] or a["blocks"] == b["blocks"]


def test_reuse_gate_counts_rows_per_module_and_head(dry):
    assert gates.k13b(dry[0])["status"] == gates.PASS
    rows = copy.deepcopy(dry[0][:1]) * 7
    assert gates.k13b(rows)["status"] == gates.FAIL


def test_step_agreement_rule_and_trace_driver():
    assert S.step_agreement([(10, 10)] * 100)["pass"]
    assert not S.step_agreement([(10, 20)] * 100)["pass"]
    assert not S.step_agreement([(10, 10)] * 50)["pass"]                    # fewer than 100 programs never passes
    import ast
    spec = _first(lambda c, s: out4.gen_out4(c, s), {"lang": "python", "exc": False, "bin": "lt10", "gold_pos": 0})
    rq = S.trace_request("t", spec["lo"], {"calls": spec["calls"], "mode": "all"})
    text = "\n".join(v for k, v in rq["files"].items() if k.startswith("od_trace"))
    ast.parse(text)
    assert "settrace" in text and "@@ODL@@" in text


def test_agreement_report_with_the_sim_executor():
    specs = []
    for s in range(300):
        try:
            specs.append(out4.gen_out4({"lang": "python", "exc": False, "bin": ["lt10", "mid", "gt40"][s % 3], "gold_pos": 0}, s))
        except Skip:
            continue
        if len(specs) == 100:
            break
    rep = solver_a.agreement_report(specs, S.SimExecutor())
    assert rep["n"] == 100 and rep["pass"]
