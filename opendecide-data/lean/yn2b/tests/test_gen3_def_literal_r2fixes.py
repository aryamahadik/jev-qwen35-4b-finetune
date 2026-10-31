"""R2 fixes to F6 (gen3_def_literal), 1 Oct: coherent fact patterns, deeming-clause balance, claim-stating questions
for the JB fallback pair, 'in force from' before every date fact, and no outside-rule echo in choice rows.
CPU only; builds in memory, writes nothing."""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
for p in (str(LEAN / "golden_src" / "gen3"), str(LEAN / "yn2b")):
    if p not in sys.path:
        sys.path.insert(0, p)
sys.dont_write_bytecode = True
import dl_core as dc  # noqa: E402
import dl_packs as dp  # noqa: E402
import dl_render as dr  # noqa: E402
import dl_sample as ds  # noqa: E402
import gen3_def_literal as g  # noqa: E402
import mv_core as mv  # noqa: E402
import r2_def_literal_review as R  # noqa: E402
import v3_def_literal as v3  # noqa: E402


@pytest.fixture(scope="module")
def built():
    return g.build_all()


def _f(pack, values, order=None, opened=200):
    return {"pack": pack, "values": values, "order": order or list(values), "opened": opened}


# ------------------------------------------------------------------------------------------------ unit: coherence
def test_incoherent_rules():
    assert ds.incoherent(_f("tenancy", {"months": 3, "moved_in": 100})) == "linked attributes shown together"
    assert ds.incoherent(_f("tenancy", {"months": 3, "age": 30})) is None
    assert ds.incoherent(_f("club", {"age": 19, "membership": 35})) and \
        ds.incoherent(_f("club", {"age": 30, "membership": 22})) is None
    assert ds.incoherent(_f("club", {"age": 16, "membership": 9})) and \
        ds.incoherent(_f("club", {"age": 16, "membership": 8})) is None
    assert ds.incoherent(_f("sports", {"age": 14, "residence": 15}))
    assert ds.incoherent(_f("sports", {"age": 14, "academy": 9})) and \
        ds.incoherent(_f("sports", {"age": 14, "academy": 8})) is None
    for k, v in (("on_lease", True), ("vehicle", True), ("rent_share", 80), ("relation", "spouse")):
        assert ds.incoherent(_f("tenancy", {"age": 7, k: v})) == "a minor with adult facts"
    assert ds.incoherent(_f("tenancy", {"age": 7, "relation": "child", "rent_share": 0, "on_lease": False})) is None
    assert ds.incoherent(_f("tenancy", {"age": 2, "months": 30}))
    assert ds.incoherent(_f("safety", {"days_off": 6, "hours_lost": 1}))
    assert ds.incoherent(_f("safety", {"days_off": 6, "hours_lost": 40})) is None
    assert ds.incoherent(_f("safety", {"days_off": 1, "hours_lost": 1})) is None
    # a date fact (and its report) never falls after the file was opened
    assert ds.incoherent(_f("club", {"applied": 250}, opened=200))
    assert ds.incoherent(_f("insurance", {"date": 190, "reported": 20}, opened=200))
    assert ds.incoherent(_f("insurance", {"date": 170, "reported": 20}, opened=200)) is None
    assert ds.incoherent(_f("safety", {"date": 199, "reported": 30}, opened=200))
    assert ds.incoherent(_f("club", {"applied": None, "age": None}, opened=60)) is None   # unrecorded: no clash


def test_in_force_and_opened_days():
    for p in dp.PACKS.values():
        lo = min([a.lo for a in p.attrs if a.kind == "date"] or [46])
        days = {ds.in_force_day(p, x) for x in range(1, 46)}
        assert min(days) == 1 and max(days) < lo, p.id
    f = _f("club", {"applied": 300, "age": 40})
    assert ds.opened_day(f, 100) > 300 and ds.opened_day(f, 320) == 320
    assert ds.date_floor(_f("insurance", {"date": 100, "reported": 30})) == 131


def test_exclusive_attrs_never_sampled_together():
    import random
    pool = ds.SafePool(mv.NamePool("train"))
    n = 0
    for i in range(400):
        rng = random.Random(i)
        ctx = {"gid": "tenancy:guest", "tier": "hard", "dk": "path", "truth": True, "excg": None, "miss": None,
               "r_place": "none", "usage_agree": True, "r_agree": True}
        try:
            f = ds.sample(rng, ctx, pool)
        except ds.SampleFail:
            continue
        n += 1
        assert not {"months", "moved_in"} <= set(f["order"])
        assert ds.incoherent(f) is None
    assert n > 20


# ------------------------------------------------------------------------------------------------ the JB fallback
def test_fallback_questions_state_the_claim():
    f = next(iter(_items()))
    for k in range(5):
        jb, jbf = dr.question(f, "jb", k), dr.question(f, "jbf", k)
        assert R.states_claim(jbf) and v3.parse_question(jbf)["states_claim"], jbf
        assert v3.parse_question(jb)["states_claim"] is False
        assert v3.parse_question(jbf)["family"] == "jb"
    for k in range(1, 5):
        assert not R.states_claim(dr.question(f, "jb", k))


def _items():
    import random
    pool = ds.SafePool(mv.NamePool("train"))
    for i in range(200):
        rng = random.Random(1000 + i)
        ctx = {"gid": "club:senior", "tier": "standard", "dk": "path", "truth": True, "excg": None, "miss": None,
               "r_place": "none", "usage_agree": True, "r_agree": True}
        try:
            yield ds.sample(rng, ctx, pool)
        except ds.SampleFail:
            continue


# ------------------------------------------------------------------------------------------------ the full build
def test_built_rows_are_coherent(built):
    for part in ("train", "dev"):
        rows = built.fb.rows_for(part)
        ch = R.coherence_hunt([dict(r, _defs=built.fb.defs.get(r["meta"]["defs"])) if r["meta"]["defs"] else r
                               for r in rows])
        assert ch == {}, (part, {k: (v["rows"], v["rids"][:3]) for k, v in ch.items()})
    for v in built.latents.values():
        assert ds.incoherent(v["facts"]) is None


def test_jb_rows_use_the_claim_question_with_the_fallback(built):
    n = Counter()
    for r in built.fb.rows:
        if r["meta"]["qkind"] != "jb":
            continue
        fb = r["options"] == list(mv.JB_FALLBACK)
        n[fb] += 1
        assert r["meta"]["tpl"].startswith("jbf" if fb else "jb") and (fb == r["meta"]["tpl"].startswith("jbf"))
        assert R.states_claim(r["instructions"]) or not fb
    assert n[True] >= 15 and n[False] >= 60


def test_deeming_clause_does_not_predict_the_answer(built):
    rows = [dict(r, _defs=built.fb.defs.get(r["meta"]["defs"])) for r in built.fb.rows_for("train")
            if r["meta"]["qkind"] in ("yn", "jb")]
    c = Counter()
    for r in rows:
        o = v3.solve(r)
        c[(o["defn"].deem is not None, o["applies"])] += 1
    share = c[(True, True)] / (c[(True, True)] + c[(True, False)])
    assert 0.42 <= share <= 0.58, c
    h = R.reader_heuristics(rows)["deeming_means_is"]
    assert h["acc"] <= 0.58 and h["coverage"] >= 0.3, h


def test_choice_rows_never_echo_the_written_in_outside_rule(built):
    for r in built.fb.rows:
        if r["meta"]["qkind"] != "choice":
            continue
        m = R._OUTSIDE.search(r["state"])
        if not m:
            continue
        pack = dp.PACKS[r["meta"]["pack"]]
        vp = re.search(r"(?:that|who) (.+?) is (?:not )?treated as", m.group(0)).group(1)
        ao = R._attr_of_vp(pack, vp)
        opt_attrs = {R._attr_of_vp(pack, o.split(f"the {pack.entity} ", 1)[-1].split(", unless ")[0])
                     for o in r["options"] if o != dr.NONE_OPT}
        assert ao not in opt_attrs, r["rid"]


def test_filler_dates_follow_the_opening(built):
    for v in built.latents.values():
        f = v["facts"]
        for lab, val in f["filler"]:
            if re.fullmatch(R._DATE, val):
                assert dp.day_index(dp.parse_date(val)) >= f["opened"], (lab, val, f["opened"])
        assert f["in_force"] < f["opened"]
        assert f["notes"][0].endswith(dp.fmt_date(dp.day(f["opened"])) + ".")
