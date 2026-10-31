"""T42c check-at-generation + the build-review fixes of 18 Oct (CPU only; generated code is interpreted, never executed)."""
import collections
import copy
import random

import pytest

from LC_COMMON import sandbox_iface as S
from LC_COMMON import wording
from LC_COMMON.checked import RowChecker, StampServiceRequired
from tool_engine.row_pipeline import TestDoubleHook

from T42c import checked as CH
from T42c import config as C
from T42c import eqv2, out4
from T42c.base import Skip
from T42c.build import make_specs
from T42c.planner import Planner
from T42c.solver_b import hook


def _picker(seed=1):
    return wording.Picker(wording.make_test_pool(list(C.QUESTION_FORM.values()), 60), random.Random(seed))


@pytest.fixture(scope="module")
def checked_run():
    rows, summ, ck = CH.run_checked(40, S.SimExecutor(), _picker(), TestDoubleHook(), seed=4, standin=True, max_chunks=8)
    return rows, summ, ck


def test_every_kept_row_is_answer_checked_and_stamped_when_made(checked_run):
    rows, summ, ck = checked_run
    assert rows and all("stamp" in r and r["stamp"]["answer_checks"]["solver_B"] for r in rows)
    assert summ["kept"] >= len(rows) and summ["stamp_calls"] >= 1 and set(summ["cues"])      # cues present for every head built


def test_order_invariance_copies_are_checked_and_stamped_too(checked_run):
    rows = checked_run[0]
    copies = [r for r in rows if r["meta"].get("perm_copy")]
    assert copies and all("stamp" in r for r in copies)


def test_no_hook_no_rows_and_no_sim_executor_in_production():
    with pytest.raises(StampServiceRequired):
        CH.run_checked(5, S.SimExecutor(), _picker(), None, standin=True)
    with pytest.raises(ValueError):
        CH.run_checked(5, S.SimExecutor(), _picker(), TestDoubleHook(), standin=False)


def test_solver_b_in_the_loop_drops_a_row_whose_label_was_flipped():
    ck = CH.make_checker(TestDoubleHook(), standin=True)
    rows, _, _ = CH.run_checked(12, S.SimExecutor(), _picker(), TestDoubleHook(), seed=5, standin=True, max_chunks=3)
    r = copy.deepcopy([x for x in rows if x["head"] == "EQV2"][0])
    r["label"] = "NO" if r["label"] == "YES" else "YES"
    r["row_id"] = "T42c-flip-1"
    assert ck.filter([r]) == [] and ck.dropped[("answer", "B_label_differs")] == 1


def test_a_call_spec_that_differs_from_the_witness_calls_is_dropped():
    ck = CH.make_checker(TestDoubleHook(), standin=True)
    rows, _, _ = CH.run_checked(12, S.SimExecutor(), _picker(), TestDoubleHook(), seed=6, standin=True, max_chunks=3)
    r = copy.deepcopy([x for x in rows if x["head"] == "OUT4" and x["lang"] == "python" and not x["meta"].get("perm_copy")][0])
    r["row_id"] = "T42c-tamper-1"
    text = r["carriers"]["CALL_SPEC"]
    broken = text.replace("(", "(99, ", 1) if "(" in text else text + "x"
    r["prompt_text"] = r["prompt_text"].replace(text, broken)
    r["carriers"]["CALL_SPEC"] = broken
    kept = ck.filter([r])
    assert kept == [] and ck.log[0]["reasons"][0] in ("B_prose", "B_refused", "B_label_differs")


def test_a_g13_hit_on_one_half_of_a_pair_drops_the_other_half():
    rows, _, _ = CH.run_checked(30, S.SimExecutor(), _picker(), TestDoubleHook(), seed=8, standin=True, max_chunks=4)
    pairs = collections.defaultdict(list)
    for r in rows:
        if r["meta"].get("pair_id") and not r["meta"].get("perm_copy"):
            pairs[r["meta"]["pair_id"]].append(r)
    both = next(v for v in pairs.values() if len(v) == 2)
    fresh = [copy.deepcopy(x) for x in both]
    for x in fresh:
        x.pop("stamp", None)
    ck = CH.make_checker(TestDoubleHook(hit_ids=[fresh[0]["row_id"]]), standin=True)
    assert ck.filter(fresh) == [] and ck.dropped[("g13", "stamp_hit")] == 1 and ck.dropped[("g13", "stamp_partner_of_hit")] == 1


# ------------------------------------------------------------------------------------------------ build-review fixes
@pytest.mark.parametrize("lang", ("python", "go", "bash", "javascript"))
def test_out4_partner_rows_never_have_an_earlier_call_that_raises(lang):
    from LC_COMMON import sampler as SM
    n = 0
    for exc in (False, True):
        for b in ("lt10", "mid", "gt40"):
            for k in range(14):
                try:
                    spec = out4.gen_out4({"lang": lang, "exc": exc, "bin": b, "gold_pos": k % 4, "custom": False}, "q%d" % k)
                except Skip:
                    continue
                for kind in ("nearmiss", "invariant"):
                    try:
                        new = out4.make_pair(spec, kind, "q%d" % k)
                    except Skip:
                        continue
                    outs, _ = SM.run_calls(new["lo"], lang, new["calls"])
                    assert not any(o[0] == "exc" for o in outs[:-1])
                    n += 1
    assert n >= 3


def test_eqv2_yes_rows_never_show_two_identical_programs():
    seen = 0
    for k in range(60):
        try:
            spec = eqv2.gen_eqv2({"lang": "python", "label": "YES", "eq": "EQ-YES-%d" % (1 + k % 5), "seq": k % 3 == 0}, "y%d" % k)
        except Skip:
            continue
        seen += 1
        assert spec["shown"][0]["blocks"] != spec["shown"][1]["blocks"]
    assert seen >= 10


def test_the_planner_writes_off_a_starved_cell_instead_of_stalling_the_build():
    pl = Planner(1)
    cell = {"head": "OUT4", "lang": "python", "unit": "invariant", "exc": True, "bin": "gt40", "seed": 0}
    before = pl.c["bin:OUT4"]["gt40"]
    for _ in range(Planner.STARVE_AFTER - 1):
        pl.note_result(cell, False)
    assert pl.c["bin:OUT4"]["gt40"] == before and not pl.starved
    pl.note_result(cell, False)
    assert pl.c["bin:OUT4"]["gt40"] == before + 1 and sum(pl.starved.values()) == 1
    pl.note_result(cell, True)
    assert pl.fails[Planner._sig(cell)] == 0


def test_make_specs_reports_every_cell_to_the_planner():
    pl = Planner(2)
    for _ in range(6):
        make_specs(pl.unit(), planner=pl)
    assert sum(pl.fails.values()) <= 6


def test_hook_rejects_an_eqv2_yes_row_whose_two_programs_are_identical():
    rows, _, _ = CH.run_checked(20, S.SimExecutor(), _picker(), TestDoubleHook(), seed=9, standin=True, max_chunks=4)
    r = copy.deepcopy(next(x for x in rows if x["head"] == "EQV2" and x["label"] == "YES"))
    a, b = r["carriers"]["PROGRAM_PAIR"]
    r["carriers"]["PROGRAM_PAIR"] = [a, {"name": "B", "blocks": a["blocks"]}]
    res = hook.check_row(r)
    assert res["keep"] is False and "identical" in res["reason"]


def test_row_generation_does_not_depend_on_the_python_hash_seed():
    """Build-review fix: an EQV2 transform site was drawn from a SET before the shuffle, so one seed gave different rows in different
    processes (a row could not be regenerated from its seed). Same seed, different PYTHONHASHSEED => identical rows."""
    import os
    import subprocess
    import sys
    fam = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    code = ("import sys, hashlib, json; sys.path.insert(0, %r); from T42c.dryrun import dry_rows; rows = dry_rows(40, seed=3)[0]; "
            "print(hashlib.sha256(json.dumps([(r['row_id'], r['label'], r['prompt_text']) for r in rows]).encode()).hexdigest())" % fam)
    outs = set()
    for hs in ("1", "4", "7"):
        env = dict(os.environ, PYTHONHASHSEED=hs)
        res = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, timeout=600)
        assert res.returncode == 0, res.stderr[-300:]
        outs.add(res.stdout.strip().splitlines()[-1])
    assert len(outs) == 1
