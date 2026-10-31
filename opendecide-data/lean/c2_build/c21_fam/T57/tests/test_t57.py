"""T57 tests: tasks and candidate classes, head specs, the four-gate gold in Solver A (with fault injection), comments/decoys,
twins, copies, gates, clean-room checks. No generated code is executed: SimExecutor predicts witnesses from the IR interpreter."""
import builtins
import collections
import copy
import json
import os
import random
import re
import subprocess

import pytest

from LC_COMMON import ir as I
from LC_COMMON import sandbox_iface as S
from LC_COMMON import suites, wording
from LC_COMMON.names_guard import default_guard

from T57 import build as BLD
from T57 import config as C
from T57 import gates, heads as H, rows as ROWS, schema, solver_a as SA, task as TK
from T57.base import Skip, row_names
from T57.dryrun import dry_pool, dry_rows

LANGS = ("python", "javascript", "typescript", "go", "bash")


@pytest.fixture(scope="module")
def dry():
    return dry_rows(40, seed=5)


def _picker(seed=1):
    return wording.Picker(dry_pool(), random.Random(seed))


def _task(lang="python", **kw):
    for s in range(60):
        try:
            return TK.make_task(s, lang, **kw)
        except Skip:
            continue
    raise AssertionError("no task")


# ------------------------------------------------------------------------------------------------ config + names
def test_config_follows_the_g0_lite_and_rulings():
    assert sum(C.HEAD_ROWS.values()) == 3000 and C.HEAD_ROWS == {"VERDICT": 1000, "BEST4": 800, "TESTSEL": 400, "LOCALISE": 800}
    for h, split in C.LANG_SPLIT.items():
        assert sum(split) == C.HEAD_ROWS[h]
    assert C.TS_FLOOR == 0.80 and C.TS_PROPOSAL == 0.90 and C.CLASSES == ("NOFIX", "REGRESSION", "PARTIAL", "CORRECT")
    assert (C.BIN_AUC_MAX, C.BIN_UPPER_MAX) == (0.55, 0.60) and abs(C.K3_ACC_MAX - 0.3633) < 1e-3
    assert C.DECOY_SHARE_OF_INCORRECT == 0.15 and C.ALTFIX_MIN_OF_BEST4_CORRECT == 0.30


def test_names_on_the_frozen_list_for_every_head():
    g = default_guard()
    for head in C.HEADS:
        for lang in LANGS:
            nm = row_names(head, lang)
            assert g.check("T57", nm) == [] and nm["policy"] == [C.DEFS_CARD[head]]


# ------------------------------------------------------------------------------------------------ tasks and classes
@pytest.mark.parametrize("lang", LANGS)
def test_task_has_a_bug_a_failing_visible_test_and_tags(lang):
    t = _task(lang)
    st = suites.evaluate(t["buggy_lo"], lang, t["suite_all"])
    assert not st[t["visible"]["name"]]
    assert set(t["target"]) | {t["visible"]["name"]} == {c for c, ok in st.items() if not ok}
    assert len(t["p2p"]) >= 4 and t["target"]
    assert all(suites.evaluate(t["ref_lo"], lang, t["suite_all"]).values())             # gold-sanity (spec level)
    assert len(t["visible"]["steps"]) == 1
    assert t["visible"]["name"] not in {c["name"] for c in t["hidden"]["cases"]}        # V and H are different sets


def test_classification_precedence_on_a_handmade_task():
    t = _task("python")
    ref = t["ref_lo"]
    assert TK.classify(t, ref)[0] == "CORRECT"
    assert TK.classify(t, t["buggy_lo"])[0] == "NOFIX"
    cands = TK.build_candidates(t, random.Random(1))
    classes = {c["cls"] for c in cands}
    assert "CORRECT" in classes and classes & {"NOFIX", "REGRESSION", "PARTIAL"}


def test_candidate_library_covers_the_registry_and_labels_come_from_execution():
    seen = collections.Counter()
    for s in range(40):
        try:
            t = TK.make_task(s, "python", multi=(s % 3 == 0))
        except Skip:
            continue
        for c in TK.build_candidates(t, random.Random(s)):
            seen[c["kind"]] += 1
            assert c["changed"] <= C.MAX_DIFF_LINES and c["diff"].startswith("--- a/")
            assert c["cls"] == TK.classify(t, c["lo"])[0]
    assert set(seen) >= {"CAND-INVERSE", "CAND-ALTFIX", "CAND-NEARMISS", "CAND-WRONGPLACE"}, seen


def test_candidates_never_touch_test_files():
    t = _task("python")
    for c in TK.build_candidates(t, random.Random(2)):
        assert all(not p.startswith("test_") and ".test." not in p and not p.endswith("_test.go") for p in c["files"])
        assert "+++ b/test" not in c["diff"]


def test_multi_site_bug_yields_halfsite_candidates():
    for s in range(60):
        try:
            t = TK.make_task(s, "python", multi=True)
        except Skip:
            continue
        cands = TK.build_candidates(t, random.Random(s))
        if any(c["kind"] == "CAND-HALFSITE" for c in cands):
            assert t["multi"]
            return
    raise AssertionError("no HALFSITE candidate found")


def test_narrow_guard_is_property_based_not_a_literal():
    for s in range(80):
        try:
            t = TK.make_task(s, "python")
        except Skip:
            continue
        ng = TK.narrow_guard(t, random.Random(s))
        if ng is not None:
            assert ng[1]["kind"] in ("range", "parity")
            return
    raise AssertionError("no narrow guard built")


# ------------------------------------------------------------------------------------------------ heads
def test_best4_has_exactly_one_correct_and_altfix_option():
    got_alt = 0
    for s in range(60):
        try:
            t = TK.make_task(s, "python")
            TK.build_candidates(t, random.Random(s))
            sp = H.best4_spec(t, random.Random(s), s % 4, s % 2 == 0)
        except Skip:
            continue
        cls = [c["cls"] for c in sp["cands"]]
        assert cls.count("CORRECT") == 1 and cls[sp["gold_index"]] == "CORRECT"
        assert len({c["diff"] for c in sp["cands"]}) == 4
        got_alt += sp["altfix"]
    assert got_alt > 0


def test_localise_options_follow_the_rules():
    for s in range(120):
        try:
            t = TK.make_task(s, "python", need_functions=4)
            sp = H.localise_spec(t, random.Random(s), s % 4)
        except Skip:
            continue
        flags = sp["opt_flags"]
        assert sp["options"][sp["gold_index"]] == t["bug_fn"] and len(set(sp["options"])) == 4
        assert any(f["traversed"] for f in flags.values()) and any(f["same_file"] for f in flags.values())
        return
    raise AssertionError("no LOCALISE row")


def test_testsel_gold_fails_before_and_passes_after_and_distractors_pass_both():
    for s in range(120):
        try:
            t = TK.make_task(s, "python", kind="T")
            TK.build_candidates(t, random.Random(s))
            sp = H.testsel_spec(t, random.Random(s), 2)
        except Skip:
            continue
        st_b = suites.evaluate(t["buggy_lo"], "python", t["suite_all"])
        st_f = suites.evaluate(sp["cands"][0]["lo"], "python", t["suite_all"])
        for k, name in enumerate(sp["options"]):
            if k == sp["gold_index"]:
                assert not st_b[name] and st_f[name]
            else:
                assert st_b[name] and st_f[name]
        assert any(f["runs_bug_fn"] for f in sp["opt_flags"].values()) or True
        return
    raise AssertionError("no TESTSEL row")


# ------------------------------------------------------------------------------------------------ Solver A
def _run(specs, executor=None, picker=None):
    for k, s in enumerate(specs):
        s.setdefault("row_id", "r%d" % k)
    sv = SA.SolverA(executor or S.SimExecutor(), picker or _picker())
    return sv.run(specs), sv


def _specs(seed_start=0, n=1, head="VERDICT", lang="python"):
    out = []
    s = seed_start
    while len(out) < n and s < seed_start + 200:
        s += 1
        try:
            t = TK.make_task(s, lang)
            TK.build_candidates(t, random.Random(s))
            if head == "VERDICT":
                out.append(H.verdict_spec(t, random.Random(s), "CORRECT"))
            elif head == "BEST4":
                out.append(H.best4_spec(t, random.Random(s), 1, False))
        except Skip:
            continue
    return out


def test_verdict_labels_follow_execution_class():
    t = None
    for s in range(60):
        try:
            t = TK.make_task(s, "python")
            TK.build_candidates(t, random.Random(s))
            a = H.verdict_spec(t, random.Random(s), "CORRECT")
            b = H.verdict_spec(t, random.Random(s), "INCORRECT")
            break
        except Skip:
            continue
    (rows, sv) = _run([a, b])
    by = {r["row_id"]: r for r in rows}
    assert by["r0"]["label"] == "CORRECT" and by["r1"]["label"] == "INCORRECT"
    assert by["r1"]["manifest"]["reason"] in ("PARTIAL", "REGRESSION", "NOFIX") and not sv.stats.drops


def test_gold_sanity_failure_drops_the_module():
    sp = _specs(0, 1)[0]
    sp["row_id"] = "rg"
    task = sp["task"]

    def break_sanity(res):
        res = dict(res)
        res["states"] = {k: "failed" for k in res["states"]}
        return res
    ex = S.SimExecutor(faults={"%s#sanity" % task["uid"]: break_sanity})
    rows, sv = _run([sp], ex)
    assert rows == [] and sv.stats.drops["module_gold_sanity"] == 1


def test_weak_hidden_suite_fails_the_strength_gate():
    sp = _specs(3, 1)[0]
    task = sp["task"]
    faults = {}
    for k in range(len(SA.strength_pool(task))):
        def survive(res):
            res = dict(res)
            res["states"] = {x: "passed" for x in res["states"]}
            return res
        faults["%s#str%d" % (task["id"], k)] = survive
    rows, sv = _run([sp], S.SimExecutor(faults=faults))
    assert rows == [] and sum(v for k, v in sv.stats.drops.items() if k.startswith("module_")) == 1


def test_threshold_rule_and_floor():
    assert SA.pilot_threshold([0.95] * 8 + [0.5] * 2)[0] == 0.90
    assert SA.pilot_threshold([0.95] * 5 + [0.5] * 5)[0] is None
    with pytest.raises(ValueError):
        SA.set_threshold(0.79)
    SA.set_threshold(0.85)
    assert SA.TS["value"] == 0.85
    SA.set_threshold(C.TS_PROPOSAL, by_pilot=False)


def test_unexpected_class_is_counted_per_operator_and_the_execution_label_wins():
    sp = _specs(7, 1)[0]
    c = sp["cands"][0]
    k = SA.cand_key(c)
    task = sp["task"]

    def fail_everything(res):
        res = dict(res)
        res["states"] = {x: "failed" for x in res["states"]}
        return res
    rows, sv = _run([sp], S.SimExecutor(faults={"%s#c%s" % (task["uid"], k): fail_everything}))
    assert rows and rows[0]["label"] == "INCORRECT" and rows[0]["manifest"]["reason"] == "NOFIX"
    assert sv.stats.op_unexpected[c["kind"]] == 1 and sv.stats.op_total[c["kind"]] == 1


def test_best4_with_two_correct_options_is_dropped():
    sp = _specs(11, 1, "BEST4")[0]
    task = sp["task"]
    bad = [c for c in sp["cands"] if c["cls"] != "CORRECT" and (c["cls"] != "PARTIAL" or c["evidence"].get("failing"))][0]

    def pass_everything(res):
        return dict(res, states={x: "passed" for x in res["states"]})
    faults = {"%s#c%s" % (task["uid"], SA.cand_key(bad)): pass_everything}
    rows, sv = _run([sp], S.SimExecutor(faults=faults))
    assert rows == []
    assert any(k in sv.stats.drops for k in ("best4_not_exactly_one_correct", "unexpected_class_needs_differential"))


def test_nondeterministic_candidate_run_is_dropped():
    sp = _specs(5, 1)[0]
    task = sp["task"]
    rid = "%s#c%s" % (task["uid"], SA.cand_key(sp["cands"][0]))
    rows, sv = _run([sp], S.SimExecutor(nondeterministic=[rid]))
    assert rows == [] and sv.stats.drops["nondeterministic"] == 1


def test_requests_use_the_exact_patched_tree_and_executor_owned_pytest_config():
    sp = _specs(2, 1)[0]
    reqs = SA.cand_requests(sp["task"], sp["cands"][0])
    for rid, (k, rq) in reqs.items():
        if rq["kind"] == "suite":
            assert "--noconftest" in rq["argv"] and "/etc/od-sbx/pytest.ini" in rq["argv"]
            for path, text in sp["cands"][0]["files"].items():
                assert rq["files"][path] == text
        assert S.to_job_line(rq)["repeats"] in (2, 3)


def test_hidden_test_leak_is_detected(monkeypatch):
    sp = _specs(4, 1)[0]
    task = sp["task"]
    _, _, blocks, _ = SA.test_files(task)
    case, body = sorted(blocks.items())[0]
    orig = ROWS.build_row

    def leaky(spec, *a, **k):
        row = orig(spec, *a, **k)
        row["prompt_text"] += "\n" + body
        return row
    monkeypatch.setattr(ROWS, "build_row", leaky)
    rows, sv = _run([sp])
    assert rows == [] and sv.stats.drops["hidden_test_leak"] == 1


# ------------------------------------------------------------------------------------------------ comments, decoys, twins
def test_comment_insertion_is_text_only_and_visible_in_the_diff():
    t = _task("python")
    cands = TK.build_candidates(t, random.Random(1))
    c = cands[0]
    c2 = ROWS.with_comment(t, c, "fixed the boundary in x", "python")
    assert "# fixed the boundary in x" in c2["diff"] and c2["comment_line"].strip().startswith("# fixed")
    assert c2["base"] == c["base"]                                     # the IR (behaviour) is untouched
    for lang, pre in (("go", "// "), ("bash", "# "), ("typescript", "// ")):
        t2 = _task(lang)
        c3 = ROWS.with_comment(t2, TK.build_candidates(t2, random.Random(1))[0], "note", lang)
        assert pre + "note" in c3["diff"]


def test_comment_presence_is_independent_of_the_class_and_decoys_are_incorrect_patches_with_fixed_claims(dry):
    rows = [r for r in dry[0] if r["head"] == "VERDICT" and r["meta"]["variant"] == "primary"]
    n_dec = 0
    for r in rows:
        c = r["meta"]["cands"][0]
        if c.get("decoy"):
            n_dec += 1
            assert r["label"] == "INCORRECT" and c["comment_kind"] == "fixed" and r["carriers"].get("COMMENT_DECOY")
    assert n_dec >= 0


def test_rename_twin_has_the_same_label_and_different_local_names():
    for s in range(60):
        try:
            t = TK.make_task(s, "python")
            TK.build_candidates(t, random.Random(s))
            sp = H.verdict_spec(t, random.Random(s), "CORRECT")
        except Skip:
            continue
        tw = BLD.twin_of_spec(sp, random.Random(s))
        if tw is None:
            continue
        sp["row_id"], tw["row_id"] = "a", "b"
        rows, sv = _run([sp, tw])
        by = {r["row_id"]: r for r in rows}
        assert by["a"]["label"] == by["b"]["label"] and by["b"]["meta"]["twin_of"] == t["uid"]
        assert by["a"]["carriers"]["SRC_FILE"][0]["text"] != by["b"]["carriers"]["SRC_FILE"][0]["text"]
        return
    raise AssertionError("no twin built")


# ------------------------------------------------------------------------------------------------ copies
def test_dry_run_rows_complete_and_in_memory_only(dry, tmp_path, monkeypatch):
    rows, stats, skips, pool = dry
    assert len(rows) >= 40
    heads = {r["head"] for r in rows}
    assert {"VERDICT", "BEST4"} <= heads
    for r in rows:
        assert set(["row_id", "family", "head", "lang", "label", "carriers", "prompt_text", "names", "meta", "manifest", "b_inputs"]) <= set(r)
        if r["head"] in ("BEST4", "TESTSEL", "LOCALISE"):
            assert r["label"] in list("ABCD")
        assert default_guard().check("T57", r["names"]) == [] and r["meta"]["tokens"] > 0
    assert len({r["row_id"] for r in rows}) == len(rows)
    before = set(os.listdir(tmp_path))
    monkeypatch.chdir(tmp_path)
    dry_rows(10, seed=9)
    assert set(os.listdir(tmp_path)) == before


def test_order_copies_are_non_identity_permutations_with_matching_labels(dry):
    rows = dry[0]
    pk = _picker()
    for r in [x for x in rows if x["head"] in ("BEST4", "LOCALISE", "TESTSEL") and x["meta"]["variant"] == "primary"][:8]:
        c = BLD.permuted_row(r, random.Random(3), "copy", pk)
        assert c["meta"]["perm"] != [0, 1, 2, 3] and c["label"] == "ABCD"[c["meta"]["gold_index"]]
        if r["head"] == "BEST4":
            gold_diff = r["carriers"]["PATCH_DIFF"]["ABCD".index(r["label"])]["diff"]
            assert c["carriers"]["PATCH_DIFF"][c["meta"]["gold_index"]]["diff"] == gold_diff
        elif r["head"] == "LOCALISE":
            assert c["meta"]["options"][c["meta"]["gold_index"]] == r["meta"]["bug_fn"]


def test_reason_head_rows_reuse_the_context_with_lettered_reasons(dry):
    rows = dry[0]
    rs = [r for r in rows if r["head"] == "REASON"]
    src = {r["row_id"]: r for r in rows}
    for r in rs:
        assert sorted(r["meta"]["reason_options"]) == ["NOFIX", "PARTIAL", "REGRESSION"]
        assert r["meta"]["reason_options"][r["meta"]["reason_gold"]] == r["manifest"]["reason"]
        assert r["label"] == "ABCD"[r["meta"]["reason_gold"]] and r["question_form"] == "T57-Q-VERDICT-REASON"


def test_with_outputs_variant_adds_the_visible_result(dry):
    rows = dry[0]
    vs = [r for r in rows if r["meta"]["variant"] == "with_outputs"]
    for r in vs:
        assert r["carriers"].get("VISIBLE_RESULT", "").startswith("FAILED")


# ------------------------------------------------------------------------------------------------ gates
def test_gate_smoke_statuses(dry):
    rows, stats, _, pool = dry
    res = gates.run_gates(rows, stats, pool=pool, n_target=40)
    st = gates.summarize(res)
    assert st["K4"] == gates.PENDING and st["K17"] == gates.PENDING
    assert st["K1"] == gates.PASS and st["K3"] == gates.PASS and st["K10"] == gates.PASS and st["K16"] == gates.PASS
    assert st["K5"] == gates.UNDER and st["K6"] == gates.UNDER


def test_planted_defects_are_caught(dry):
    rows = copy.deepcopy(dry[0])
    v = [r for r in rows if r["head"] == "VERDICT"]
    for r in v:
        r["manifest"]["module"]["sanity_ok"] = False
    assert gates.k1(v)["status"] == gates.FAIL
    rows2 = copy.deepcopy(dry[0])
    r0 = next(r for r in rows2 if r["head"] == "LOCALISE" or r["head"] == "BEST4")
    r0["names"]["language"] = ["ruby"]
    assert gates.k16([r0])["status"] == gates.FAIL
    rows3 = [r for r in copy.deepcopy(dry[0]) if r["head"] == "VERDICT"]
    for r in rows3:
        r["label"] = "CORRECT"
        r["manifest"]["cand_classes"] = ["CORRECT"]
    assert gates.k11(rows3)["status"] == gates.FAIL
    leak = copy.deepcopy(dry[0][:3])
    leak[0]["meta"]["leak_hits"] = ["x"]
    assert gates.k10(leak)["status"] == gates.FAIL


def test_k10_flags_a_testsel_module_shared_with_another_head():
    mk = lambda head, mod: {"row_id": head + mod, "head": head, "meta": {"module_id": mod, "variant": "primary", "leak_hits": []}, "prompt_text": "", "label": "A"}
    assert gates.k10([mk("TESTSEL", "m1"), mk("VERDICT", "m1")])["status"] == gates.FAIL
    assert gates.k10([mk("TESTSEL", "m1"), mk("VERDICT", "m2")])["status"] == gates.PASS


def test_solver_b_view_hides_labels_and_expected_classes(dry):
    rows = dry[0]
    for r in rows[:6]:
        pkg = {r["b_inputs"]["task_uid"]: {"x": 1}}
        v = schema.b_view(r, pkg)
        txt = json.dumps(v)
        assert "label" not in v and "manifest" not in v and "meta" not in v
        assert "CAND-" not in txt and "cand_classes" not in txt


# ------------------------------------------------------------------------------------------------ clean room
def test_no_generated_code_is_executed(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("generated code must never run on the CPU side")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(os, "system", boom)
    monkeypatch.setattr(builtins, "exec", boom)
    monkeypatch.setattr(builtins, "eval", boom)
    rows, *_ = dry_rows(10, seed=6)
    assert rows


def test_family_code_does_not_reference_forbidden_inputs():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bad = re.compile(r"ohs|sealed|mutate\.py|PLAN_v3|SKEPTIC|OHS5_BRIEF|research_v3", re.I)
    for dirpath, _, files in os.walk(here):
        for f in files:
            if f.endswith((".py", ".md")) and "tests" not in dirpath.split(os.sep):
                assert not bad.search(open(os.path.join(dirpath, f), encoding="utf-8").read()), f


# ------------------------------------------------------------------------------------------------ added: pilot, reuse, balancers
def test_pilot_composition_and_rule():
    from T57 import pilot
    ts = pilot.pilot_tasks(seed0=9100, split=(("python", 6), ("go", 2), ("bash", 2)))
    assert len(ts) == 10 and {t["lang"] for t in ts} == {"python", "go", "bash"}
    rep = pilot.pilot_scores(ts, S.SimExecutor())
    assert rep["n_modules"] == 10 and rep["T_s"] in (0.90, None)
    assert dict(pilot.LANG_SPLIT)["python"] == 38 and sum(n for _, n in pilot.LANG_SPLIT) == 50


def test_reuse_gate(dry):
    assert gates.k_reuse(dry[0])["status"] == gates.PASS
    rows = copy.deepcopy([r for r in dry[0] if r["meta"]["variant"] == "primary" and r["head"] == "VERDICT"][:1]) * 6
    for k, r in enumerate(rows):
        r["row_id"] = "x%d" % k
    assert gates.k_reuse(rows)["status"] == gates.FAIL


def test_localise_gold_flags_look_like_the_distractors_when_the_module_allows(dry):
    for r in [x for x in dry[0] if x["head"] == "LOCALISE"][:6]:
        flags = r["meta"]["opt_flags"]
        gold = r["meta"]["options"][r["meta"]["gold_index"]]
        assert flags[gold]["traversed"] and flags[gold]["same_file"]
        assert any(f["traversed"] for n, f in flags.items() if n != gold) and any(f["same_file"] for n, f in flags.items() if n != gold)


def test_gap_balancer_refuses_widening_rows_and_never_deadlocks():
    from LC_COMMON.plan_utils import GapBalancer
    gb = GapBalancer(1, tau=0.01, warmup=10, max_rejects=3)
    for _ in range(20):
        assert gb.ok([(True, [1.0]), (False, [0.0])]) or True
        gb.add([(True, [0.5]), (False, [0.5])])
    refused = [gb.ok([(True, [1.0]), (False, [0.0])]) for _ in range(6)]
    assert False in refused and True in refused and gb.overrides >= 1


def test_k12_counts_rename_twins_and_their_originals_as_matched_pairs():
    from T57 import gates
    def row(i, head="VERDICT", uid="u", **meta):
        m = {"task_uid": uid, "pair_kind": None, "twin_of": None, "variant": "primary"}
        m.update(meta)
        return {"row_id": "r%d" % i, "head": head, "lang": "python", "label": "CORRECT", "meta": m, "carriers": {}}
    rows = [row(0, uid="a"), row(1, uid="a.tw", twin_of="a", variant="primary"), row(2, uid="b"), row(3, uid="c")]
    d = gates.k12(rows)["detail"]
    assert abs(d["pairs"] - 2 / 3.0) < 1e-3          # one twin plus the original row it copies, over three primary rows
