"""Tests for PREREG Ruling A69 (DRAFT): A42-D 6 trap weighting in c2_select / crowd_select_c2 and the drop-only repair in a49c.
In memory only (fixtures + fault injection); nothing is written. Run from lean/:
  HF_HUB_OFFLINE=1 ../.venv/bin/python -B -m pytest -q c2_build/tests/test_c2_select_a69.py
"""
from __future__ import annotations

import copy
import inspect
import math
import random
import sys
from collections import Counter
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
import a49c  # noqa: E402
import c2io  # noqa: E402
import c2_select as sel  # noqa: E402
import crowd_select as cs  # noqa: E402
import crowd_select_c2 as cs2  # noqa: E402
from mixio import h64  # noqa: E402

FAM = "T26"
TAGS = ["tA", "tB", "tC", "tD", "tE"]


def toks(rows, lo=700, hi=700):
    """Real token counts for a pool (A80 b: the swap guard and the repair bind on them). Alternating lo / hi; the default mean is 700 <= 800."""
    return {r["id"]: (lo if i % 2 else hi) for i, r in enumerate(rows)}


def pool(n_units=500, seed=3, unit_size=1, tag_p=0.7, k=3, yn_share=0.0, prefix=""):
    """A synthetic family: choice rows (k options, the first non-gold options carry tags) and optional yes/no rows. Returns
    rows, rels, probs (C1 option probabilities), pg."""
    rnd = random.Random(seed)
    rows, probs = [], {}
    for u in range(n_units):
        for j in range(unit_size):
            rid = f"{prefix}u{u}r{j}"
            base = {"id": rid, "call_id": f"{prefix}c{u}", "group_id": f"{prefix}g{u}", "source": "c2_t26", "role": "base",
                    "state": f"s{u}.{j}", "card": "card"}
            meta = {"family": FAM, "wording_id": f"w{u % 3}", "card_id": f"k{u % 12}", "sampler": f"S{u % 4 + 1}"}
            if rnd.random() < yn_share:
                g = rnd.randrange(2)
                rows.append(base | {"qtype": "noul", "gold": g, "options": None, "instructions": "Is it so?", "meta": meta})
                py = rnd.choice([0.02, 0.5, 0.99])
                probs[rid] = {"yes": py, "no": 1 - py}
                continue
            opts = [f"{prefix}o{u}.{j}.{x}" for x in range(k)]
            gold = opts[rnd.randrange(k)]
            wrong = [o for o in opts if o != gold]
            oe = {}
            for o in wrong:
                if rnd.random() < tag_p:
                    oe[o] = [rnd.choice(TAGS)]
            rows.append(base | {"qtype": "choice", "gold": gold, "options": opts, "instructions": "Which?",
                                "meta": meta | ({"opt_err": oe} if oe else {})})
            w = [rnd.random() ** 2 for _ in opts]
            tot = sum(w)
            probs[rid] = {o: x / tot for o, x in zip(opts, w)}
    pg = {r["id"]: cs.p_gold(r, probs[r["id"]]) for r in rows}
    return rows, [], probs, pg


# ---- crowd_select_c2.select is crowd_select.select + two injected inputs ------------------------------------------------
def test_copy_is_verbatim_apart_from_the_three_injection_edits():
    src = inspect.getsource(cs2.select)
    undo = [('def select(rows, units, pg: dict | None, target: int, key: str = "", seed: int = SEED, bins_in: dict | None = None,\n'
             '           order_in: list | None = None) -> dict:',
             'def select(rows, units, pg: dict | None, target: int, key: str = "", seed: int = SEED) -> dict:'),
            (' if bins_in is None else dict(bins_in)   # A69: injected', ''),
            (' if order_in is None else list(order_in)   # A69: injected', '')]
    for new, old in undo:
        assert src.count(new) == 1
        src = src.replace(new, old)
    assert src == inspect.getsource(cs.select)


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_no_injection_is_byte_identical(seed):
    rows, rels, probs, pg = pool(300, seed=seed, unit_size=2)
    units = cs.units_of(rows, rels)
    a = cs.select(rows, units, pg, 250, key=FAM, seed=20261013)
    b = cs2.select(rows, units, pg, 250, key=FAM, seed=20261013)
    assert a == b
    # injecting what select would compute itself changes nothing either
    bins = {r["id"]: cs.bin_of(pg[r["id"]]) for r in rows}
    order = sorted(range(len(units)), key=lambda u: h64(20261013, FAM, "order", rows[units[u][0]]["id"]))
    assert cs2.select(rows, units, pg, 250, key=FAM, seed=20261013, bins_in=bins, order_in=order) == a


# ---- 6.2 / 6.4: tags, pick rates, flags --------------------------------------------------------------------------------
def test_row_trap_tags_skips_gold_empty_and_unshown():
    r = {"qtype": "choice", "options": ["a", "b", "c"], "gold": "a",
         "meta": {"opt_err": {"a": ["tx"], "b": ["t2", "t1"], "c": [], "zz": ["t9"]}}}
    assert sel.row_trap_tags(r) == {"b": ("t1", "t2")}
    assert sel.row_trap_tags({"qtype": "noul", "meta": {"opt_err": {"a": ["x"]}}}) == {}
    assert sel.row_trap_tags({"qtype": "choice", "options": ["a"], "gold": "a", "meta": {}}) == {}


def mk(rid, opts, gold, oe, p, call=None):
    return ({"id": rid, "call_id": call or rid, "qtype": "choice", "options": opts, "gold": gold,
             "meta": {"family": FAM, "opt_err": oe}}, p)


def test_pick_rates_order_and_argmax_first_on_ties():
    # tag X is shown in 4 rows and picked in 2 (rate .5); Y shown in 2, picked in 1 (.5): same rate, X shown more -> X first
    # Z shown in 1, picked in 1 (1.0) -> first; W and V tie on rate 0 and rows shown: by name
    spec = [
        ("r1", ["g", "x", "y"], "g", {"x": ["X"], "y": ["Y"]}, {"g": .1, "x": .6, "y": .3}),
        ("r2", ["g", "x", "y"], "g", {"x": ["X"], "y": ["Y"]}, {"g": .1, "x": .3, "y": .6}),
        ("r3", ["g", "x", "z"], "g", {"x": ["X"], "z": ["Z"]}, {"g": .2, "x": .2, "z": .6}),
        ("r4", ["g", "x", "w"], "g", {"x": ["X"], "w": ["W"]}, {"g": .5, "x": .3, "w": .2}),
        ("r5", ["g", "v"], "g", {"v": ["V"]}, {"g": .5, "v": .5}),            # tie: the FIRST option (gold) is the argmax
    ]
    rows, probs = [], {}
    for rid, o, g, oe, p in spec:
        r, pp = mk(rid, o, g, oe, p)
        rows.append(r)
        probs[rid] = pp
    rates, order = sel.trap_pick_rates(rows, probs)
    assert rates["X"] == [1, 4, 0.25] and rates["Y"] == [1, 2, 0.5] and rates["Z"] == [1, 1, 1.0]
    assert rates["W"] == [0, 1, 0.0] and rates["V"] == [0, 1, 0.0]
    assert order == ["Z", "Y", "X", "V", "W"]


def test_several_tags_on_one_option_count_the_row_once_per_tag():
    r, p = mk("r", ["g", "x"], "g", {"x": ["A", "B"]}, {"g": .1, "x": .9})
    rates, _ = sel.trap_pick_rates([r], {"r": p})
    assert rates == {"A": [1, 1, 1.0], "B": [1, 1, 1.0]}


def test_flag_threshold_is_inclusive_and_one_type_per_unit():
    r1, p1 = mk("a", ["g", "x", "y"], "g", {"x": ["X"], "y": ["Y", "Z"]}, {"g": .5, "x": .2499, "y": .25}, call="u")
    r2, p2 = mk("b", ["g", "x"], "g", {"x": ["X"]}, {"g": .8, "x": .2499}, call="v")
    rows = [r1, r2]
    units = cs.units_of(rows, [])
    rank_of = {"Z": 0, "Y": 1, "X": 2}
    flagged, per_tag = sel.trap_flags(rows, units, {"a": p1, "b": p2}, rank_of)
    assert flagged == {0: "Z"}                                   # unit v (0.2499 < 0.25) is not flagged; unit u: Y and Z at .25 -> best rank Z
    assert per_tag == Counter({"Y": 1, "Z": 1})                  # per-tag count counts the unit once per tag (reported only)


def test_flag_uses_every_row_of_the_unit():
    r1, p1 = mk("a", ["g", "x"], "g", {"x": ["X"]}, {"g": .9, "x": .01}, call="u")
    r2, p2 = mk("b", ["g", "x"], "g", {"x": ["X"]}, {"g": .1, "x": .9}, call="u")
    units = cs.units_of([r1, r2], [])
    assert sel.trap_flags([r1, r2], units, {"a": p1, "b": p2}, {"X": 0})[0] == {0: "X"}


# ---- 6.3 / 6.4: the order ---------------------------------------------------------------------------------------------
def test_order_with_nothing_treated_is_crowd_selects():
    rows, rels, probs, pg = pool(200)
    units = cs.units_of(rows, rels)
    want = sorted(range(len(units)), key=lambda u: h64(20261013, FAM, "order", rows[units[u][0]]["id"]))
    assert sel.trap_order(rows, units, FAM, 20261013, {}, {}, 2.0) == want


def test_untreated_units_keep_their_exact_relative_order_and_treated_move_up():
    rows, rels, probs, pg = pool(400)
    units = cs.units_of(rows, rels)
    base = sorted(range(len(units)), key=lambda u: h64(20261013, FAM, "order", rows[units[u][0]]["id"]))
    treated = {u: "tA" for u in range(0, len(units), 5)}
    out = sel.trap_order(rows, units, FAM, 20261013, treated, {"tA": 0}, 2.0)
    assert sorted(out) == sorted(range(len(units)))
    assert [u for u in out if u not in treated] == [u for u in base if u not in treated]
    mean_pos = lambda o: sum(k for k, u in enumerate(o) if u in treated) / len(treated)       # noqa: E731
    assert mean_pos(out) < mean_pos(base)


def test_two_to_one_odds_for_a_treated_unit_against_an_untreated_one():
    rows = [{"id": "t", "call_id": "t"}, {"id": "u", "call_id": "u"}]
    units = [[0], [1]]
    first = 0
    n = 4000
    for i in range(n):
        o = sel.trap_order(rows, units, f"k{i}", 20261013, {0: "tA"}, {"tA": 0}, 2.0)
        first += o[0] == 0
    assert abs(first / n - 2 / 3) < 0.03                          # w : 1 = 2 : 1  ->  P(treated first) = 2/3
    o = [sel.trap_order(rows, units, f"k{i}", 20261013, {0: "tA"}, {"tA": 0}, 1.0)[0] == 0 for i in range(n)]
    assert abs(sum(o) / n - 0.5) < 0.03                           # weight 1 = no preference


def test_treated_positions_are_refilled_by_type_rank_then_own_t():
    rows = [{"id": f"r{i}", "call_id": f"r{i}"} for i in range(60)]
    units = [[i] for i in range(60)]
    treated = {u: ("B" if u % 2 else "A") for u in range(0, 60, 3)}
    rank_of = {"A": 1, "B": 0}                                    # B is the type C1 picks most
    out = sel.trap_order(rows, units, "k", 20261013, treated, rank_of, 2.0)
    slots = [k for k, u in enumerate(out) if u in treated]
    types = [treated[out[k]] for k in slots]
    assert types == sorted(types, key=lambda t: rank_of[t])       # every B before every A, across the positions treated units held
    assert len(slots) == len(treated)
    assert [u for u in out if u not in treated] == [u for u in sorted(range(60), key=lambda u: h64(20261013, "k", "order", f"r{u}")) if u not in treated]


# ---- trap_select: bins, no treated, type cap, hard assert -------------------------------------------------------------
def test_without_any_tag_trap_select_equals_crowd_select():
    rows, rels, probs, pg = pool(300, tag_p=0.0)
    units = cs.units_of(rows, rels)
    res, rec = sel.trap_select(rows, units, pg, probs, 200, FAM, 20261013)
    ref = cs.select(rows, units, pg, 200, key=FAM, seed=20261013)
    assert res == ref and rec["flagged_units"] == 0 and rec["treated_units_final"] == 0 and not rec["scaled"]


def test_treated_rows_are_hard_and_p_g_bins_are_kept():
    rows, rels, probs, pg = pool(500)
    units = cs.units_of(rows, rels)
    res, rec = sel.trap_select(rows, units, pg, probs, 300, FAM, 20261013)
    assert rec["flagged_units"] > 0 and rec["treated_units_final"] > 0
    n_hard_a69 = sum(1 for b in res["bins"].values() if b == "hard")
    n_hard_pg = sum(1 for b in rec["pg_bin"].values() if b == "hard")
    assert n_hard_a69 >= n_hard_pg
    for r in rows:
        if res["bins"][r["id"]] != rec["pg_bin"][r["id"]]:
            assert res["bins"][r["id"]] == "hard"                 # a bin only ever changes to hard (treated units)


def test_type_cap_35_percent_of_treated_selected_and_only_shrinks():
    # one trap type dominates the flags; the cap must strip its treatment until it holds <= 35% of the treated selected units
    rows, rels, probs, pg = pool(600, tag_p=1.0, k=3)
    for r in rows:                                                  # tag every wrong option of ~80% of rows "tA", others spread
        oe = r["meta"].get("opt_err") or {}
        for o in oe:
            oe[o] = ["tA"] if hash(r["id"]) % 5 else [random.Random(r["id"]).choice(TAGS[1:])]
    units = cs.units_of(rows, rels)
    res, rec = sel.trap_select(rows, units, pg, probs, 300, FAM, 20261013)
    st = rec["treated_selected_by_type"]
    n = sum(st.values())
    assert n > 0 and max(st.values()) <= 0.35 * n + 1e-9
    assert rec["treated_units_final"] <= rec["flagged_units"]
    for step in rec["type_cap_steps"]:
        need = math.ceil((step["units_of_type"] - 0.35 * step["treated_selected"]) / 0.65 - 1e-9)
        assert step["treatment_removed_from"] == max(1, need)


def test_a_single_type_cannot_stay_under_35_percent_so_none_of_it_is_selected():
    rows, rels, probs, pg = pool(400, tag_p=1.0, k=2)
    for r in rows:
        for o in (r["meta"].get("opt_err") or {}):
            r["meta"]["opt_err"][o] = ["tA"]
    units = cs.units_of(rows, rels)
    res, rec = sel.trap_select(rows, units, pg, probs, 200, FAM, 20261013)
    # one type is 100% of any non-empty treated set: the cap keeps removing the treatment of the selected treated units until
    # none is selected (the loop ends: the treated set only shrinks)
    assert rec["treated_selected_units"] == 0 and rec["type_cap_steps"]
    assert not any(u in res["sel"] for u in range(len(units)) if rows[units[u][0]]["id"] in rec["pg_bin"]
                   and res["bins"][rows[units[u][0]]["id"]] != rec["pg_bin"][rows[units[u][0]]["id"]])
    removed = sum(s["treatment_removed_from"] for s in rec["type_cap_steps"])
    assert rec["treated_units_final"] == rec["flagged_units"] - removed


def test_cap_removes_the_lowest_priority_units_of_the_over_type(monkeypatch):
    rows, rels, probs, pg = pool(300, tag_p=1.0, k=3)
    for r in rows:
        oe = r["meta"].get("opt_err") or {}
        for n, o in enumerate(oe):
            oe[o] = ["tA"] if n == 0 else ["tB"]
    units = cs.units_of(rows, rels)
    calls = []
    real_order, real_sel = sel.trap_order, cs2.select

    def order(*a, **k):
        o = real_order(*a, **k)
        calls.append({"treated": dict(a[4]), "order": o})
        return o

    def select(*a, **k):
        res = real_sel(*a, **k)
        calls[-1]["sel"] = list(res["sel"])
        return res
    monkeypatch.setattr(sel, "trap_order", order)
    monkeypatch.setattr(sel.cs2, "select", select)
    res, rec = sel.trap_select(rows, units, pg, probs, 150, FAM, 20261013)
    assert rec["type_cap_steps"] and len(calls) == len(rec["type_cap_steps"]) + 1
    c0, c1 = calls[0], calls[1]
    step = rec["type_cap_steps"][0]
    removed = set(c0["treated"]) - set(c1["treated"])
    assert len(removed) == step["treatment_removed_from"] and set(c1["treated"]) <= set(c0["treated"])   # only shrinks
    pos = {u: k for k, u in enumerate(c0["order"])}
    cand = [u for u in c0["sel"] if u in c0["treated"] and c0["treated"][u] == step["type"]]
    assert removed <= set(cand)
    latest = sorted(cand, key=lambda u: -pos[u])[:len(removed)]
    assert removed == set(latest)                                    # the lowest-priority (latest) selected treated units of the type
    n = sum(1 for u in c0["sel"] if u in c0["treated"])
    assert step["treated_selected"] == n and step["units_of_type"] == len(cand)
    assert len(cand) > 0.35 * n                                       # the type really was over the cap
    final = [u for u in res["sel"] if u in calls[-1]["treated"]]
    cnt = Counter(calls[-1]["treated"][u] for u in final)
    assert not cnt or max(cnt.values()) <= 0.35 * len(final) + 1e-9


def test_hard_assert_steps_the_weight_down_by_a_tenth_to_one(monkeypatch):
    rows, rels, probs, pg = pool(300)
    units = cs.units_of(rows, rels)
    real = cs2.select
    seen = []

    def faulty(*a, **k):
        res = real(*a, **k)
        res["report"]["bins"]["hard"] = res["report"]["rows"]       # fault: every selected row looks hard
        return res
    monkeypatch.setattr(sel.cs2, "select", faulty)
    monkeypatch.setattr(sel, "trap_order", lambda *a, **k: (seen.append(a[-1]), sorted(range(len(units))))[1])
    res, rec = sel.trap_select(rows, units, pg, probs, 150, FAM, 20261013)
    assert rec["weight"] == 1.0 and rec["scaled"] and not rec["hard_assert_ok"]
    assert [round(s["weight"], 1) for s in rec["weight_steps"]] == [round(2.0 - 0.1 * i, 1) for i in range(10)]
    assert min(seen) == 1.0 and max(seen) == 2.0


def test_hard_assert_holds_by_construction_on_real_selections():
    for seed in (1, 2, 3):
        rows, rels, probs, pg = pool(500, seed=seed)
        units = cs.units_of(rows, rels)
        res, rec = sel.trap_select(rows, units, pg, probs, 300, FAM, 20261013)
        assert rec["hard_assert_ok"] and rec["weight"] == 2.0 and not rec["scaled"]
        assert res["report"]["bins"].get("hard", 0) <= 0.30 * res["report"]["rows"] + 1e-9


def test_units_stay_whole_and_nothing_is_relabelled():
    rows, rels, probs, pg = pool(300, unit_size=2)
    before = copy.deepcopy(rows)
    units = cs.units_of(rows, rels)
    res, rec = sel.trap_select(rows, units, pg, probs, 200, FAM, 20261013)
    assert rows == before
    chosen = {rows[i]["id"] for u in res["sel"] for i in units[u]}
    for u in units:
        ids = {rows[i]["id"] for i in u}
        assert ids <= chosen or not (ids & chosen)


# ---- select_family ----------------------------------------------------------------------------------------------------
def test_select_family_without_probs_is_the_old_selection():
    rows, rels, probs, pg = pool(300)                               # choice rows only: no yes rate / share for a swap to move
    a = sel.select_family(FAM, rows, rels, pg, 200)
    units = cs.units_of(rows, rels)
    ref = cs.select(rows, units, pg, 200, key=FAM, seed=sel.SEED)
    want = [rows[i]["id"] for u in ref["sel"] for i in units[u]]
    assert a["selected_ids"] == want and "a69" not in a and "pg_bin" not in a
    assert a["difficulty_bin"] == {r["id"]: ref["bins"][r["id"]] for r in rows}


def test_select_family_with_probs_records_a69_and_both_bin_maps():
    rows, rels, probs, pg = pool(500)
    rec = sel.select_family(FAM, rows, rels, pg, 300, probs=probs, ntok=toks(rows))
    assert set(rec["a42d6"]) >= {"flagged_units", "pick_rates_post_g13", "type_order"} and set(rec["a69"]) >= {"version", "swap", "repair", "a34e"}
    assert set(rec["pg_bin"]) == set(rec["difficulty_bin"]) == {r["id"] for r in rows}
    assert rec["a42d6"]["flagged_units"] > 0 and "pg_bin" not in rec["a42d6"] and "report" in rec and "a69" not in rec["report"]
    ch = {r["id"] for r in rows if r["id"] in set(rec["selected_ids"])}
    assert len(ch) == len(rec["selected_ids"])


def test_other_families_are_selected_as_before_even_with_probs():
    rows, rels, probs, pg = pool(300)
    for r in rows:
        r["meta"]["family"] = "T40"
    a = sel.select_family("T40", rows, rels, pg, 200, probs=probs)
    b = sel.select_family("T40", rows, rels, pg, 200)
    assert a["selected_ids"] == b["selected_ids"] and "a69" not in a


def test_missing_option_probabilities_stop_the_run():
    rows, rels, probs, pg = pool(100)
    probs.pop(rows[0]["id"] if rows[0]["qtype"] == "choice" else next(r["id"] for r in rows if r["qtype"] == "choice"))
    with pytest.raises(SystemExit, match="without C1 option probabilities"):
        sel.select_family(FAM, rows, rels, pg, 50, probs=probs)


def test_g13_dropped_rows_give_no_statistic():
    rows, rels, probs, pg = pool(300, unit_size=2)
    drop = {rows[i]["id"] for i in range(0, 60)}
    rec = sel.select_family(FAM, rows, rels, pg, 150, drop_ids=drop, probs=probs, ntok=toks(rows))
    keep = [r for r in rows if r["id"] not in drop]
    units = cs.units_of(keep, [])
    rates, _ = sel.trap_pick_rates([r for r in rows if r["id"] not in {x for x in drop}], probs)
    assert rec["a42d6"]["pick_rates_post_g13"] == rates and not (set(rec["selected_ids"]) & drop)
    assert units


# ---- the drop-only repair ----------------------------------------------------------------------------------------------
def fam_pool_for_repair(n=400, tok_long=3):
    rows, rels, probs, pg = pool(n, seed=5, k=3, yn_share=0.5, tag_p=0.4)
    units = cs.units_of(rows, rels)
    res = cs.select(rows, units, pg, n, key=FAM, seed=20261013)
    ntok = {r["id"]: (1000 if i % tok_long == 0 else 300) for i, r in enumerate(rows)}
    return rows, rels, units, res, ntok


def test_repair_only_removes_whole_units_and_never_raises_a_cap():
    rows, rels, units, res, ntok = fam_pool_for_repair()
    bins = res["bins"]
    sel0 = list(res["sel"])
    new, info = a49c.repair_drop_only(FAM, rows, rels, units, sel0, bins, ntok, 20261013)
    assert set(new) <= set(sel0) and info["units_dropped"] == len(sel0) - len(new)
    assert info["rows_dropped"] == sum(len(units[u]) for u in set(sel0) - set(new))
    assert info["violation_after"] <= info["violation_before"] + 1e-9
    n0 = sum(len(units[u]) for u in sel0)
    n1 = sum(len(units[u]) for u in new)
    for b in ("hard", "easy"):
        s0 = sum(1 for u in sel0 for i in units[u] if bins[rows[i]["id"]] == b) / n0
        s1 = sum(1 for u in new for i in units[u] if bins[rows[i]["id"]] == b) / n1
        assert s1 <= max(s0, a49c.BIN_CAPS[b]) + 1e-9
    assert n1 <= n0


def test_repair_fixes_a_token_mean_above_800_by_dropping_the_longest_units():
    rows, rels, units, res, ntok = fam_pool_for_repair()
    sel0 = list(res["sel"])
    rws = lambda us: [rows[i] for u in us for i in units[u]]       # noqa: E731
    mean = lambda us: sum(ntok[r["id"]] for r in rws(us)) / len(rws(us))   # noqa: E731
    ntok = {k: v + 400 for k, v in ntok.items()}                    # fault injection: push the mean above the bar
    assert mean(sel0) > 800
    new, info = a49c.repair_drop_only(FAM, rows, rels, units, sel0, res["bins"], ntok, 20261013)
    assert mean(new) <= 800 + 1e-9 and info["rows_dropped"] > 0
    assert a49c.family_checks(FAM, rws(new), [], ntok)["token_mean"]["verdict"] == "pass"


def test_repair_is_deterministic_and_seeded():
    rows, rels, units, res, ntok = fam_pool_for_repair()
    ntok = {k: v + 400 for k, v in ntok.items()}
    a, _ = a49c.repair_drop_only(FAM, rows, rels, units, list(res["sel"]), res["bins"], ntok, 20261013)
    b, _ = a49c.repair_drop_only(FAM, rows, rels, units, list(res["sel"]), res["bins"], ntok, 20261013)
    assert a == b


def test_repair_refuses_a_drop_that_would_raise_the_hard_cap():
    # all rows are tiny, the only way to lower the violation is to drop medium units, which would push hard above 30%
    rows, rels, probs, pg = pool(200, tag_p=0.0, k=2)
    units = cs.units_of(rows, rels)
    bins = {r["id"]: ("hard" if i < 60 else "medium") for i, r in enumerate(rows)}      # exactly 30% hard
    sel0 = list(range(len(units)))
    ntok = {r["id"]: (2000 if bins[r["id"]] == "medium" else 100) for r in rows}         # medium units are the long ones
    new, info = a49c.repair_drop_only(FAM, rows, rels, units, sel0, bins, ntok, 1)
    h = sum(1 for u in new for i in units[u] if bins[rows[i]["id"]] == "hard") / sum(len(units[u]) for u in new)
    assert h <= 0.30 + 1e-9
    assert len(new) == len(sel0) and info["units_dropped"] == 0   # every helpful drop was a medium unit: refused, none made


def test_repair_keeps_trap_types_under_their_cap():
    rows, rels, units, res, ntok = fam_pool_for_repair(600)
    ntok = {k: v + 400 for k, v in ntok.items()}
    sel0 = list(res["sel"])
    ut = {u: ("A" if k % 3 == 0 else "B" if k % 3 == 1 else "C") for k, u in enumerate(sel0) if k % 2 == 0}
    n0 = Counter(ut[u] for u in sel0 if u in ut)
    new, _ = a49c.repair_drop_only(FAM, rows, rels, units, sel0, res["bins"], ntok, 20261013, unit_type=ut)
    n1 = Counter(ut[u] for u in new if u in ut)
    tot0, tot1 = sum(n0.values()), sum(n1.values())
    assert max(n1.values()) / tot1 <= max(max(n0.values()) / tot0, 0.35) + 1e-9


def test_select_family_repair_may_stop_below_target_and_keeps_units_whole():
    rows, rels, probs, pg = pool(500, k=3, yn_share=0.0, tag_p=0.5)
    ntok = toks(rows, 700, 940)                                      # fault: mean 820 > 800 (A69 d: the faithful repair drops the longest-first units, at most 25%)
    rec = sel.select_family(FAM, rows, rels, pg, 300, probs=probs, repair=True, ntok=ntok)
    assert rec["a69"]["repair"]["rows_dropped"] > 0
    assert len(rec["selected_ids"]) < 300 and rec["report"]["short_by"] > 0
    assert rec["report"]["a49c"]["checks"]["token_mean"]["verdict"] == "pass"
    rec0 = sel.select_family(FAM, rows, rels, pg, 300, probs=probs, repair=False, ntok=ntok)
    assert set(rec["selected_ids"]) < set(rec0["selected_ids"])       # rows only removed, never added
    assert rec0["a69"]["repair"].startswith("not run")


# ---- swap with the trap class -------------------------------------------------------------------------------------------
def test_swap_balance_default_is_unchanged_and_class_restricts_partners():
    rows, rels, probs, pg = pool(400, yn_share=0.6, tag_p=0.0)
    units = cs.units_of(rows, rels)
    res = cs.select(rows, units, pg, 200, key=FAM, seed=20261013)
    a, ia = a49c.swap_balance(FAM, rows, units, res["sel"], res["bins"], 20261013)
    b, ib = a49c.swap_balance(FAM, rows, units, res["sel"], res["bins"], 20261013, unit_class=None)
    assert a == b and ia == ib
    cls = {u: ("X" if u % 2 else None) for u in range(len(units))}
    cls = {u: v for u, v in cls.items() if v}
    c, ic = a49c.swap_balance(FAM, rows, units, res["sel"], res["bins"], 20261013, unit_class=cls)
    before = Counter(cls.get(u) for u in res["sel"])
    assert Counter(cls.get(u) for u in c) == before                 # treated-ness (hence the type counts) is preserved by every swap


# ---- fix round 1: the A49 (c) type guard, and the budget trim (reselect) keeping A69 ------------------------------------
def test_type_excess_is_zero_inside_the_cap():
    from collections import Counter as C
    assert a49c._type_excess(C({"A": 5, "B": 5, "C": 5, "D": 5}), 0.35) == 0.0
    assert a49c._type_excess(C(), 0.35) == 0.0
    assert a49c._type_excess(C({"A": 8, "B": 2}), 0.35) == pytest.approx(0.8 - 0.35)


def test_repair_may_drop_a_treated_unit_while_every_type_stays_inside_its_cap():
    # four equal types far below the cap: dropping one B nudges A's share up but stays < 35%, so the guard must not refuse it
    rows, rels, probs, pg = pool(40, tag_p=0.0, k=2)
    units = cs.units_of(rows, rels)
    ids = [rows[u[0]]["id"] for u in units]
    ut = {u: "ABCD"[u % 4] for u in range(20)}
    ex0 = a49c._type_excess(Counter(ut.values()), 0.35)
    t2 = Counter(ut.values())
    t2["B"] -= 1
    assert ex0 == 0.0 and a49c._type_excess(+t2, 0.35) == 0.0 and ids


def _trap_record(n=700, target=500, seed=5):
    rows, rels, probs, pg = pool(n, seed=seed, tag_p=0.8, k=4)
    rec = sel.select_family(FAM, rows, rels, pg, target, probs=probs, ntok=toks(rows))
    by = {r["id"]: r for r in rows}
    chosen = [by[i] for i in rec["selected_ids"]]
    trap = rec["parts"][0].get("trap") or {}
    for r in chosen:                                              # what the mixer stores on the rows (load_block)
        r["meta"] = dict(r["meta"]) | {"crowd_pg": rec["crowd_pg"][r["id"]], "difficulty_bin": rec["difficulty_bin"][r["id"]],
                                       "pg_bin": rec["pg_bin"][r["id"]], "trap": {"treated": r["id"] in trap, "type": trap.get(r["id"])}}
    return rows, chosen, rec


def test_the_record_carries_the_trap_data_in_its_part():
    rows, chosen, rec = _trap_record()
    p = rec["parts"][0]
    assert set(p) == {"key", "ids", "trap", "trap_rank"} and p["trap"] and p["trap_rank"] == rec["a42d6"]["type_order"]
    for rid, b in rec["difficulty_bin"].items():
        if rid in p["trap"]:
            assert b == "hard"                                    # every row of a treated unit is hard


@pytest.mark.parametrize("frac", [0.9, 0.75, 0.6])
def test_trim_keeps_the_a69_bins_and_the_hard_cap(frac):
    rows, chosen, rec = _trap_record()
    pgm = {r["id"]: r["meta"]["crowd_pg"] for r in chosen}
    t = int(len(chosen) * frac)
    out = sel.reselect(chosen, [], pgm, [dict(rec["parts"][0])], t, ntok=toks(chosen))
    assert out["a69"] and len(out["selected_ids"]) <= t
    keep = set(out["selected_ids"])
    assert keep <= {r["id"] for r in chosen} and set(out["bins"]) == keep
    hard = sum(1 for b in out["bins"].values() if b == "hard")
    assert hard <= 0.30 * len(keep) + 1e-9                        # the A42-D 6 bin, which is what mix_c2.cap_checks reads
    pt = out["parts"][0]["trap"]
    assert all(out["bins"][i] == "hard" for i in pt if i in keep)                  # treated stays hard, at its own type
    assert all(pt[i] == rec["parts"][0]["trap"][i] for i in pt)
    meta = {r["id"]: r["meta"] for r in chosen}
    for rid in keep - set(pt):
        assert out["bins"][rid] == meta[rid]["pg_bin"]                              # an untreated row is at its p_g bin
    again = sel.reselect(chosen, [], pgm, [dict(rec["parts"][0])], t, ntok=toks(chosen))
    assert again["selected_ids"] == out["selected_ids"]                              # deterministic


def test_trim_type_cap_holds_on_the_trimmed_rows():
    rows, chosen, rec = _trap_record(900, 700, seed=9)
    pgm = {r["id"]: r["meta"]["crowd_pg"] for r in chosen}
    out = sel.reselect(chosen, [], pgm, [dict(rec["parts"][0])], int(len(chosen) * 0.6), ntok=toks(chosen))
    keep = set(out["selected_ids"])
    n_t = Counter(t for i, t in out["parts"][0]["trap"].items() if i in keep)       # treated rows are 1 per unit here
    if n_t:
        assert max(n_t.values()) <= 0.35 * sum(n_t.values()) + 1e-9


def test_trim_without_trap_data_is_the_old_reselect():
    rows, rels, probs, pg = pool(300, seed=2)
    rec = sel.select_family(FAM, rows, rels, pg, 200)                              # no probs: no trap data in the part
    assert set(rec["parts"][0]) == {"key", "ids"}
    chosen = [r for r in rows if r["id"] in set(rec["selected_ids"])]
    out = sel.reselect(chosen, [], {r["id"]: pg[r["id"]] for r in chosen}, rec["parts"], 150)
    units = cs.units_of(chosen, [])
    ref = cs.select(chosen, units, {r["id"]: pg[r["id"]] for r in chosen}, 150, key=rec["parts"][0]["key"], seed=sel.SEED)
    assert out["selected_ids"] == [chosen[i]["id"] for u in ref["sel"] for i in units[u]] and not out["a69"] and not out["bins"]


def test_mixer_current_parts_keeps_the_trap_data():
    import mix_c2
    rows, chosen, rec = _trap_record(300, 200, seed=4)
    got = mix_c2.current_parts("T26", chosen, [], rec["parts"])
    assert got[0]["trap"] == rec["parts"][0]["trap"] and got[0]["trap_rank"] == rec["parts"][0]["trap_rank"]


def test_mixer_apply_targets_keeps_the_hard_cap_on_the_meta_bin():
    import mix_c2
    rows, chosen, rec = _trap_record(700, 500, seed=7)
    for r in chosen:
        r["_block"] = FAM
    parts = {FAM: [dict(p) for p in rec["parts"]]}
    out, _rels, info = mix_c2.apply_targets(chosen, [], {FAM: int(len(chosen) * 0.6)}, parts, ntok=toks(chosen))
    assert len(out) <= int(len(chosen) * 0.6) and info[FAM]["a69"]
    hard = sum(1 for r in out if r["meta"]["difficulty_bin"] == "hard")      # what mix_c2.cap_checks reads
    assert hard <= 0.30 * len(out) + 1e-9
    assert parts[FAM][0]["trap"] and parts[FAM][0]["trap_rank"]              # the next trim still has the data


# ---- fix round 2: the a69 record's hard share is the REALISED one; the repair is on by default -------------------------
def test_a69_record_hard_share_is_the_realised_one_after_the_repair():
    rows, rels, probs, pg = pool(500, k=3, yn_share=0.0, tag_p=0.5)
    ntok = toks(rows, 700, 940)                                                  # mean 820 > 800: the repair drops units
    rec = sel.select_family(FAM, rows, rels, pg, 300, probs=probs, ntok=ntok)    # repair left at its default
    a, b, rep = rec["a42d6"], rec["a69"], rec["report"]
    assert b["repair"]["rows_dropped"] > 0                                       # default = ON
    assert a["hard_rows"] == rep["bins"].get("hard", 0) and a["hard_share"] == round(rep["bins"].get("hard", 0) / rep["rows"], 4)
    assert a["hard_assert_ok"] is (a["hard_rows"] <= 0.30 * rep["rows"] + 1e-9)
    assert a["hard_rows_at_trap_select"] >= a["hard_rows"]                       # rows only removed


def test_repair_default_off_only_when_asked():
    rows, rels, probs, pg = pool(500, k=3, yn_share=0.0, tag_p=0.5)
    ntok = toks(rows, 700, 940)
    off = sel.select_family(FAM, rows, rels, pg, 300, probs=probs, repair=False, ntok=ntok)
    assert off["a69"]["repair"].startswith("not run")
    assert off["a42d6"]["hard_rows"] == off["a42d6"]["hard_rows_at_trap_select"]


def test_cli_repair_flags():
    import argparse
    ap_args = []
    for argv in (["select"], ["select", "--a69-repair"], ["select", "--no-a69-repair"]):
        captured = {}
        orig = sel.cmd_select
        try:
            sel.cmd_select = lambda a, c=captured: c.update(vars(a))
            # main() looks the command up in a dict built at call time, so patching the module name is enough
            sel.main(argv)
        finally:
            sel.cmd_select = orig
        ap_args.append(captured["a69_repair"])
    assert ap_args == [True, True, False] and argparse
