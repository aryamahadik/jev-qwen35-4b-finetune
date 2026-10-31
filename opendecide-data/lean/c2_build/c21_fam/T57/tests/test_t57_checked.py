"""T57 check-at-generation + the build-review fixes of 18 Oct (CPU only; generated code is interpreted, never executed)."""
import copy
import random

import pytest

from LC_COMMON import sandbox_iface as S
from LC_COMMON import wording
from LC_COMMON.checked import StampServiceRequired
from tool_engine.row_pipeline import TestDoubleHook

from T57 import checked as CH
from T57 import heads as H, rows as ROWS, task as TK
from T57.base import Skip
from T57.dryrun import dry_pool

LANGS = ("python", "javascript", "typescript", "go", "bash")


def _picker(seed=1):
    return wording.Picker(dry_pool(), random.Random(seed))


@pytest.fixture(scope="module")
def checked_run():
    return CH.run_checked(40, S.SimExecutor(), _picker(), TestDoubleHook(), seed=4, standin=True, max_units=40)


def test_every_kept_row_is_answer_checked_and_stamped_when_made(checked_run):
    rows, summ, ck = checked_run
    assert rows and all("stamp" in r and r["stamp"]["answer_checks"]["solver_B"] for r in rows)
    assert summ["stamp_calls"] >= 1 and summ["cues"] and not summ["dropped"].get("answer:B_label_differs")


def test_option_copies_and_reason_head_rows_are_checked_and_stamped_too(checked_run):
    rows = checked_run[0]
    extra = [r for r in rows if r["meta"].get("perm_copy") or r["head"] == "REASON"]
    assert extra and all("stamp" in r for r in extra)


def test_no_hook_no_rows_and_no_sim_executor_in_production():
    with pytest.raises(StampServiceRequired):
        CH.run_checked(5, S.SimExecutor(), _picker(), None, standin=True)
    with pytest.raises(ValueError):
        CH.run_checked(5, S.SimExecutor(), _picker(), TestDoubleHook(), standin=False)


def test_solver_b_in_the_loop_drops_a_verdict_row_whose_label_was_flipped(checked_run):
    rows, _, ck0 = checked_run
    ck = CH.make_checker(TestDoubleHook(), standin=True)
    ck.packages = ck0.packages                                  # packages are filled by solver A's driver
    r = copy.deepcopy(next(x for x in rows if x["head"] == "VERDICT"))
    r["label"] = "INCORRECT" if r["label"] == "CORRECT" else "CORRECT"
    r["row_id"] = "T57-flip-1"
    assert ck.filter([r]) == [] and ck.dropped[("answer", "B_label_differs")] == 1


def test_a_g13_hit_retires_the_whole_base_module(checked_run):
    rows, _, ck0 = checked_run
    base = rows[0]["meta"]["base_module"]
    same = [copy.deepcopy(r) for r in rows if r["meta"]["base_module"] == base][:3]
    for r in same:
        r.pop("stamp", None)
    ck = CH.make_checker(TestDoubleHook(hit_ids=[same[0]["row_id"]]), standin=True)
    ck.packages = ck0.packages
    assert ck.filter(same) == [] and ck.dropped[("g13", "stamp_hit")] == 1 and base in ck.retired


# ------------------------------------------------------------------------------------------------ build-review fixes
@pytest.mark.parametrize("lang", LANGS)
def test_testsel_shows_every_function_the_option_tests_call(lang):
    """Build-review fix: the four option tests call classes and helpers from other files; the shown source used to stop at the bug
    function's file, so the question could not be answered from the row."""
    checked = 0
    for seed in range(40):
        try:
            tasks = TK.make_tasks("ts%d" % seed, lang, "T", multi=False, n_bugs=2)
        except Skip:
            continue
        for task in tasks:
            try:
                TK.build_candidates(task, random.Random(seed))
                spec = H.testsel_spec(task, random.Random(seed), seed % 4)
            except Skip:
                continue
            blocks, shown = ROWS.shown_source(task, spec)
            hidden = {c["name"]: c for c in task["hidden"]["cases"]}
            for n in spec["options"]:
                for st in hidden[n]["steps"]:
                    assert st["fn"] in shown, (lang, n, st["fn"])
            checked += 1
    assert checked >= 3


def test_a_raising_do_step_in_a_hidden_case_makes_it_a_target_test_not_a_pass_to_pass_test():
    """Build-review fix: the spec used to ignore an exception escaping a bare `do` call, so a case that every real runner reports as
    failing on the buggy module was tagged pass-to-pass and could be offered as a TESTSEL distractor."""
    from LC_COMMON import suites
    for lang in LANGS:
        for seed in range(30):
            try:
                task = TK.make_tasks("dx%d" % seed, lang, "T", multi=False, n_bugs=1)[0]
            except Skip:
                continue
            st = suites.evaluate(task["buggy_lo"], lang, task["suite_all"])
            for c in task["hidden"]["cases"]:
                from LC_COMMON.interp import Interp
                it = Interp(task["buggy_lo"], lang)
                real_ok = True
                for s in c["steps"]:
                    o = it.call(s["fn"], s["args"])
                    if s["op"] == "do" and o[0] == "exc":
                        real_ok = False
                if not real_ok:
                    assert st[c["name"]] is False and c["name"] not in task["p2p"]


def test_row_generation_does_not_depend_on_the_python_hash_seed():
    """Build-review fix: an EQV2 transform site was drawn from a SET before the shuffle, so one seed gave different rows in different
    processes (a row could not be regenerated from its seed). Same seed, different PYTHONHASHSEED => identical rows."""
    import os
    import subprocess
    import sys
    fam = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    code = ("import sys, hashlib, json; sys.path.insert(0, %r); from T57.dryrun import dry_rows; rows = dry_rows(24, seed=3)[0]; "
            "print(hashlib.sha256(json.dumps([(r['row_id'], r['label'], r['prompt_text']) for r in rows]).encode()).hexdigest())" % fam)
    outs = set()
    for hs in ("1", "4", "7"):
        env = dict(os.environ, PYTHONHASHSEED=hs)
        res = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, timeout=600)
        assert res.returncode == 0, res.stderr[-300:]
        outs.add(res.stdout.strip().splitlines()[-1])
    assert len(outs) == 1
