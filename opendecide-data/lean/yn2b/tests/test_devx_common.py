"""Unit tests for golden_src/gen3/dx_common.py (reviewer R's devx engine): text helpers round-trip, the balancer,
the rotor, section split and the gold-free blind sheet."""
from __future__ import annotations

import random
from datetime import date, timedelta
from fractions import Fraction

from devx_helpers import dx


def test_long_date_round_trip_every_day_of_2026():
    d = date(2026, 1, 1)
    while d.year == 2026:
        s = dx.long_date(d)
        assert dx.parse_long_date(s) == d
        assert dx.day_of_2026(dx.doy_2026(d)) == d
        d += timedelta(days=1)


def test_parse_long_date_rejects_other_shapes():
    for bad in ("2026-03-01", "March 3 2026", "3 march 2026"):
        try:
            dx.parse_long_date(bad)
        except (ValueError, KeyError):
            continue
        raise AssertionError(bad)


def test_num_text_round_trip():
    for x in (0, 7, 1910, 2250, 12345678, Fraction(17, 10), Fraction(415084, 100), Fraction(3, 8), Fraction(-992, 100)):
        s = dx.num_text(x)
        assert dx.parse_num(s) == Fraction(x), (x, s)
    assert dx.num_text(1910) == "1,910"


def test_join_split_list_round_trip():
    words = ["finance records", "personnel records", "email archive", "customer records"]
    for n in range(1, 5):
        for last in ("and", "or"):
            s = dx.join_list(words[:n], last)
            assert dx.split_list(s, last) == words[:n]
    assert dx.join_list([]) == ""


def test_article():
    assert dx.article("organiser type") == "an"
    assert dx.article("pupil group") == "a"
    assert dx.article("Annex") == "an"


def test_balance_assign_balances_every_stratum_and_is_deterministic():
    units = []
    for i in range(60):
        dims = {"fmt": i % 3, "tpl": i % 4}
        units.append([(dims, True), (dims, False)])
    a = dx.balance_assign(units, random.Random(11))
    b = dx.balance_assign(units, random.Random(11))
    assert a == b
    imb = {}
    for u, c in zip(units, a):
        d, y = u[c]
        for k, v in d.items():
            imb[(k, v)] = imb.get((k, v), 0) + (1 if y else -1)
    assert max(abs(x) for x in imb.values()) <= 1, imb
    # fixed rows count but cannot move: 4 fixed 'yes' rows in fmt=0 are offset by the free units
    fixed = [({"fmt": 0, "tpl": 9}, True)] * 4
    c = dx.balance_assign(units, random.Random(11), fixed=fixed)
    tot = sum(1 if units[i][j][1] else -1 for i, j in enumerate(c) if units[i][j][0]["fmt"] == 0) + 4
    assert abs(tot) <= 1


def test_rotor_rotates_evenly():
    r = dx.Rotor(random.Random(3))
    picks = [r.pick("fmt", ["a", "b", "c"]) for _ in range(30)]
    assert {x: picks.count(x) for x in "abc"} == {"a": 10, "b": 10, "c": 10}
    s = [r.pick("fmt", ["a", "b"], stratum=("x",)) for _ in range(4)]
    assert sorted(s) == ["a", "a", "b", "b"]


def test_section_split():
    text = "A\nline 1\nline 2\nB\n\nline 3\n"
    assert dx.section_split(text, ["A", "B"]) == {"A": "line 1\nline 2", "B": "line 3"}


def _fake_rows(n):
    out = []
    for i in range(n):
        out.append({"id": f"r{i:03d}", "qtype": "noul" if i % 2 else "choice", "state": f"s{i}", "card": None,
                    "instructions": "q", "options": None if i % 2 else ["x", "y"], "gold": i % 2,
                    "meta": {"qkind": ("yn", "choice", "jb")[i % 3], "tpl": f"t{i % 5}"}})
    return out


def test_blind_sheet_is_gold_free_stratified_and_deterministic():
    rows = _fake_rows(100)
    a = dx.blind_sheet(rows, 50, "seed")
    assert a == dx.blind_sheet(rows, 50, "seed")
    assert len(a) == 50 and len({x["id"] for x in a}) == 50
    for x in a:
        assert set(x) == {"id", "qtype", "state", "card", "instructions", "options"}   # no gold, no meta
    strata = {(r["meta"]["qkind"], r["meta"]["tpl"]) for r in rows}
    got = {(r["meta"]["qkind"], r["meta"]["tpl"]) for r in rows if r["id"] in {x["id"] for x in a}}
    assert got == strata
    assert len(dx.blind_sheet(rows[:10], 50, "seed")) == 10
