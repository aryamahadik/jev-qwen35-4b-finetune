"""T56g check-at-generation + the build-review fixes of 18 Oct (CPU only; generated code is interpreted, never executed)."""
import copy
import random

import pytest

from LC_COMMON import sandbox_iface as S
from LC_COMMON import wording
from LC_COMMON.checked import StampServiceRequired
from tool_engine.row_pipeline import TestDoubleHook

from T56g import checked as CH
from T56g import hacks as HK
from T56g import rows as ROWS
from T56g import task as TK
from T56g.base import Skip
from T56g.solver_b.agree import _generate
from T56g import schema
from T56g.solver_b.solve import solve


def _picker(seed=1):
    pool = wording.make_test_pool(ROWS.ALL_FORMS, 60, {f: s[0] for f, s in ROWS.FORM_SLOTS.items()})
    return wording.Picker(pool, random.Random(seed))


@pytest.fixture(scope="module")
def checked_run():
    return CH.run_checked(40, S.SimExecutor(), _picker(), TestDoubleHook(), seed=4, standin=True, max_units=40)


def test_every_kept_row_is_answer_checked_and_stamped_when_made(checked_run):
    rows, summ, ck = checked_run
    assert rows and all("stamp" in r and r["stamp"]["answer_checks"]["solver_B"] for r in rows)
    assert summ["stamp_calls"] >= 1 and summ["cues"] and not summ["dropped"].get("answer:B_label_differs")


def test_no_hook_no_rows_and_no_sim_executor_in_production():
    with pytest.raises(StampServiceRequired):
        CH.run_checked(5, S.SimExecutor(), _picker(), None, standin=True)
    with pytest.raises(ValueError):
        CH.run_checked(5, S.SimExecutor(), _picker(), TestDoubleHook(), standin=False)


def test_solver_b_in_the_loop_drops_a_row_whose_label_was_flipped(checked_run):
    rows, _, ck0 = checked_run
    ck = CH.make_checker(TestDoubleHook(), standin=True)
    ck.packages = ck0.packages
    r = copy.deepcopy(rows[0])
    r["label"] = "NO-HACK" if r["label"] == "HACK" else "HACK"
    r["row_id"] = "T56g-flip-1"
    assert ck.filter([r]) == [] and ck.dropped[("answer", "B_label_differs")] == 1


def test_a_g13_hit_drops_the_pair_partner(checked_run):
    rows, _, ck0 = checked_run
    by = {}
    for r in rows:
        by.setdefault(r["meta"].get("pair_id"), []).append(r)
    pair = next(v for k, v in by.items() if k and len(v) >= 2)[:2]
    fresh = [copy.deepcopy(x) for x in pair]
    for x in fresh:
        x.pop("stamp", None)
    ck = CH.make_checker(TestDoubleHook(hit_ids=[fresh[0]["row_id"]]), standin=True)
    ck.packages = ck0.packages
    assert ck.filter(fresh) == [] and ck.dropped[("g13", "stamp_hit")] == 1 and ck.dropped[("g13", "stamp_partner_of_hit")] == 1


# ------------------------------------------------------------------------------------------------ build-review fixes
def test_f5_is_only_offered_when_every_visible_case_calls_the_one_wrapped_function():
    """Build-review fix: F5 wraps the return value of ONE function; a visible case on another (still buggy) function fails the
    visible run, so the 'hack' is not a hack. The spec used to claim visible=True regardless."""
    n_multi = n_ok = 0
    for seed in range(40):
        try:
            gs = TK.make_g_tasks("f5%d" % seed, "python", n_bugs=3, size=3)
        except Skip:
            continue
        for g in gs:
            fns = {c["steps"][0]["fn"] for c in g["visible_cases"]}
            app = HK.applicable(g, 5)
            if len(fns) > 1:
                n_multi += 1
                assert not app
            elif app:
                n_ok += 1
    assert n_multi >= 1 and n_ok >= 1


def test_solver_b_reproduces_every_f5_row_label():
    rows, packages = _generate(160, 701)
    f5 = [r for r in rows if r["meta"].get("family") == 5]
    assert f5
    for r in rows:
        out = solve(schema.b_view(r, packages))
        assert out["status"] == "ok" and out["label"] == r["label"], (r["row_id"], r["meta"].get("family"), out.get("evidence"))


def test_row_generation_does_not_depend_on_the_python_hash_seed():
    """Build-review fix: an EQV2 transform site was drawn from a SET before the shuffle, so one seed gave different rows in different
    processes (a row could not be regenerated from its seed). Same seed, different PYTHONHASHSEED => identical rows."""
    import os
    import subprocess
    import sys
    fam = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    code = ("import sys, hashlib, json; sys.path.insert(0, %r); from T56g.dryrun import dry_rows; rows = dry_rows(24, seed=3)[0]; "
            "print(hashlib.sha256(json.dumps([(r['row_id'], r['label'], r['prompt_text']) for r in rows]).encode()).hexdigest())" % fam)
    outs = set()
    for hs in ("1", "4", "7"):
        env = dict(os.environ, PYTHONHASHSEED=hs)
        res = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, timeout=600)
        assert res.returncode == 0, res.stderr[-300:]
        outs.add(res.stdout.strip().splitlines()[-1])
    assert len(outs) == 1
