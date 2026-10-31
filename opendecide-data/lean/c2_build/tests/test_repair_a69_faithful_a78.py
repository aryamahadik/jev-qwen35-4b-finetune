"""Tests for c2_build/zed_orch/a78/repair_a69_faithful.py (the repair of ADOPTED Ruling A69 (d) and the (f)(ii) acceptance test).
Synthetic families, in memory only; nothing is written. Run from lean/c2_build:
  HF_HUB_OFFLINE=1 ../../.venv/bin/python -B -m pytest -q tests/test_repair_a69_faithful_a78.py
"""
from __future__ import annotations

import copy
import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(C2B / "zed_orch" / "a78"))      # the A78 name stays importable: a thin import of c2_build/a69_faithful.py (A80 b)
import c2io  # noqa: E402
import a49c  # noqa: E402
import crowd_select as cs  # noqa: E402
import c2_select  # noqa: E402
import mix_c2  # noqa: E402
import repair_a69_faithful as RF  # noqa: E402

FAM = "T26"
LONG = "not enough information"


class FakePlugin:
    QFORMS: dict = {}


class _Q:
    def __init__(self, yes_is_bad, complement_kind):
        self.yes_is_bad, self.complement_kind = yes_is_bad, complement_kind


class QPlugin:
    QFORMS = {"qa": _Q(True, "syntactic"), "qb": _Q(False, "syntactic"), "qc": _Q(True, "antonym"), "qd": _Q(False, "antonym")}


# ------------------------------------------------------------------------------------------------ fixtures
def _meta(i, twin, card, author, rank=None, wording=None, extra=None):
    m = {"wording_id": wording or f"w{i}", "card_id": card, "twin_kind": twin,
         "c2": {"skin_id": f"s{i}", "author_mode": author, "register": "reg%d" % (sum(map(ord, str(i))) % 8)}}
    if rank is not None:
        m["gold_rank"] = rank
    return m | (extra or {})


def choice_family(n=200, k=2, twin=lambda i: "minimal_edit" if i % 100 < 22 else None, equiv=lambda i: 22 <= i < 34,
                  tok=lambda i: 700, card=lambda i: f"k{i // 50}", author=lambda i: "S", gold_len=lambda i: (12, 12),
                  pos=None, abst_gold=None, rank=None, bins=None):
    """n single-row choice units (unit u == row u == priority u; the LAST unit has the lowest priority). Defaults pass every
    (d1) check: twin 22%, equiv 7%, tokens 700, <= 50 rows per card, k options of equal length, uniform gold positions."""
    rows, ntok = [], {}
    for i in range(n):
        gl, ol = gold_len(i)
        p = (i % k) if pos is None else pos(i)
        if abst_gold is not None:                                    # k == 2: [real option, "not enough information"]
            real = ("R%04d" % i).ljust(len(LONG), "x")
            gold = LONG if abst_gold(i) else real
            opts = [real, LONG] if (i % 2) else [LONG, real]
        else:
            gold = ("G%04d" % i).ljust(gl, "g")
            others = [("H%04d_%d" % (i, j)).ljust(ol, "h") for j in range(k - 1)]
            opts = others[:p] + [gold] + others[p:]
        tk = "equiv" if equiv(i) else twin(i)
        rows.append({"id": f"r{i}", "call_id": f"c{i}", "qtype": "choice", "gold": gold, "options": opts, "instructions": "Which one?",
                     "meta": _meta(i, tk, card(i), author(i), None if rank is None else rank(i))})
        ntok[f"r{i}"] = tok(i)
    return rows, [], ntok


def _spread(m, c):
    """m slots, c of them flagged, evenly spread (Bresenham)."""
    return [((k + 1) * c) // m - (k * c) // m == 1 for k in range(m)]


def pair_family(n_units=60, skew=lambda i: False, twin_frac=0.22, equiv_frac=0.07, tok=lambda i: 700, card=lambda i: f"k{i // 30}",
                extra_choice=0, kinds=None):
    """n_units complement pairs of yes/no rows (gold (1,0), or (1,1) for a skew unit), then `extra_choice` single choice units.
    Twin / equiv flags are spread evenly inside the skew class and inside the other class, so dropping skew units moves the
    twin and equiv shares only a little."""
    tw, eq = {}, {}
    for cls in ([i for i in range(n_units) if skew(i)], [i for i in range(n_units) if not skew(i)]):
        tflag = _spread(len(cls), round(twin_frac * len(cls))) if cls else []
        for i, f in zip(cls, tflag):
            tw[i] = f
        rest = [i for i in cls if not tw[i]]
        eflag = _spread(len(rest), round(equiv_frac * len(cls))) if rest else []
        for i, f in zip(rest, eflag):
            eq[i] = f
    rows, rels, ntok = [], [], {}
    for i in range(n_units):
        g = (1, 1) if skew(i) else (1, 0)
        tk = "minimal_edit" if tw.get(i) else ("equiv" if eq.get(i) else None)
        tk = kinds[i] if kinds is not None else tk
        for j in range(2):
            rid = f"r{i}_{j}"
            rows.append({"id": rid, "call_id": f"c{i}", "qtype": "noul", "gold": g[j], "options": None, "instructions": "Is it so?",
                         "meta": _meta(f"{i}_{j}", tk, card(i), "S")})
            ntok[rid] = tok(i)
        rels.append({"a": f"r{i}_0", "b": f"r{i}_1", "type": "complement"})
    for e in range(extra_choice):
        opts = [f"A{e:04d}xxxxxx", f"B{e:04d}xxxxxx"]
        tk = "minimal_edit" if e % 100 < 22 else ("equiv" if e % 100 < 29 else None)
        rows.append({"id": f"q{e}", "call_id": f"qc{e}", "qtype": "choice", "gold": opts[e % 2], "options": opts, "instructions": "Which?",
                     "meta": _meta(f"q{e}", tk, f"kq{e // 50}", "S")})
        ntok[f"q{e}"] = 700
    return rows, rels, ntok


def make(rows, rels, ntok, order=None, treated=None, bins=None, pgbins=None, pg=None, target=0, plugin=None):
    units = cs.units_of(rows, rels)
    b = bins or {r["id"]: "medium" for r in rows}
    fm = RF.Family(FAM, rows, rels, units, b, pgbins or dict(b), pg or {r["id"]: 0.5 for r in rows}, ntok,
                   order if order is not None else list(range(len(units))), treated or {}, target=target, plugin=plugin or FakePlugin())
    return fm, units


def run(fm, units=None):
    S0 = frozenset(range(len(fm.units)))
    sel, rec = fm.repair(S0)
    return S0, sel, rec


def verdicts(fm, S):
    return {k: v[0] for k, v in fm.all(S).items()}


def sane(fm, S0, sel, rec, only_check=None):
    """Invariants every repair must keep."""
    assert set(sel) <= set(S0)                                          # no unit added
    assert rec["rows_dropped"] <= rec["loss_max_rows"] == rec["rows_pre_repair"] // 4
    assert rec["rows_dropped"] == sum(m["unit_rows"] + sum(c[1] for c in m["companions"]) for m in rec["moves"])
    before, after = verdicts(fm, S0), verdicts(fm, frozenset(sel))
    for nm in RF.PROTECTED:
        if before[nm] != "fail":
            assert after[nm] != "fail", nm                              # nothing that passed fails after the repair
    for m in rec["moves"]:
        assert m["distance_after"] < m["distance_before"]
        if only_check:
            assert m["check"] == only_check


# ------------------------------------------------------------------------------------------------ constants / text
def test_order_and_constants_match_the_adopted_text():
    p = C2B / "zed_orch" / "c21" / "A69_SELECTION_RULING.md"
    assert hashlib.sha256(p.read_bytes()).hexdigest().startswith("b1ed6d7346ec5261")
    txt = p.read_text()
    block = txt.split("(d1) Checks it may repair, in this fixed order.")[1].split("The functions are")[0]
    import re
    items = [m.group(2) for m in (re.match(r"^>\s+(\d+)\.\s+(.*)$", ln) for ln in block.splitlines()) if m]
    assert len(items) == 16 and len(RF.ORDER) == 16
    keys = ["Rows per card", "Token mean", "Free-form", "Yes/no share", "Yes rate", "G10", "Yes-is-bad", "Minimal-edit", "Equiv",
            "Complement", "Non-syntactic", "Longest option", "Abstain", "Gold position", "Gold rank", "chi-square"]
    for it, k in zip(items, keys):
        assert k.lower() in it.lower(), (it, k)
    assert (RF.SEED, RF.PASSES, RF.LOSS_DEN, RF.TYPE_CAP, RF.G11_MAX) == (20261013, 3, 4, 0.35, 0.02)
    assert RF.PROTECTED[-4:] == ["difficulty_caps", "medium_ge_45", "trap_type_cap", "g11_selected"]


# ------------------------------------------------------------------------------------------------ distances
def test_clean_family_passes_everything_and_repair_makes_no_move():
    rows, rels, ntok = choice_family()
    fm, _ = make(rows, rels, ntok)
    S0, sel, rec = run(fm)
    assert set(verdicts(fm, S0).values()) <= {"pass", "n/a"}
    assert rec["moves"] == [] and sorted(sel) == sorted(S0) and rec["rows_dropped"] == 0 and rec["failing_before"] == []
    assert rec["report_checks_additions"]["a49c_and_caps_pass"] is True


def _kitchen():
    """A choice family with many defects at once, hard / easy bins that lean on the label, treated units of 3 types and a shared wording."""
    rows, rels, ntok = choice_family(240, k=3, tok=lambda i: 1500 if i % 7 == 0 else 700, card=lambda i: f"k{i // 80}",
                                     author=lambda i: "F" if i % 4 == 0 else "S", gold_len=lambda i: (14, 8) if i % 6 < 2 else (12, 12),
                                     pos=lambda i: 0 if i % 5 < 2 else (i % 2) + 1, rank=lambda i: 0 if i % 3 < 2 else (i % 2) + 1)
    for i, r in enumerate(rows):
        if i % 12 == 0:
            r["meta"]["wording_id"] = "wShared"
    bins = {r["id"]: ("easy" if i % 6 == 0 else "hard" if i % 6 == 1 else "medium") for i, r in enumerate(rows)}
    pgb = {r["id"]: ("easy" if (i % 6 == 0 or i % 9 == 0) else "medium") for i, r in enumerate(rows)}
    treated = {u: "ABC"[u % 3] if u % 5 else "A" for u in range(240) if u % 3 == 1}
    return rows, rels, ntok, bins, pgb, treated


def test_distance_is_zero_exactly_when_the_binding_verdict_is_not_fail_on_random_sub_selections():
    rnd = random.Random(7)
    qrows, qrels, qtok = pair_family(60, skew=lambda i: i % 4 == 0, extra_choice=40)
    for r in qrows:                                                       # question forms: yes-is-bad share and complement kinds vary by unit
        r["meta"]["qform"] = "q" + "abcd"[int(r["id"].split("_")[0][1:]) * 7 % 4] if r["id"].startswith("r") else "qa"
    krows, krels, ktok, kbins, kpgb, ktreated = _kitchen()
    srows, srels, stok = [], [], {}
    for i in range(80):                                                   # yes/no singles without complement partners; 40% medium bins
        srows.append({"id": f"y{i}", "call_id": f"yc{i}", "qtype": "noul", "gold": i % 2, "options": None, "instructions": "Is it so?",
                      "meta": _meta(f"y{i}", None, "ky", "S")})
        stok[f"y{i}"] = 700
    sbins = {f"y{i}": ("medium" if i % 5 < 2 else "hard" if i % 10 in (2, 3, 4) else "easy") for i in range(80)}
    fams = [(choice_family(200, k=3, pos=lambda i: 0 if i % 5 < 2 else i % 3, rank=lambda i: i % 3), None, {}, None, None),
            (pair_family(60, skew=lambda i: i % 4 == 0, extra_choice=60), None, {}, None, None),
            (choice_family(200, abst_gold=lambda i: i % 25 < 14, equiv=lambda i: 22 <= i < 34), None, {}, None, None),
            ((qrows, qrels, qtok), None, {}, None, QPlugin()),
            ((krows, krels, ktok), kbins, ktreated, kpgb, None),
            ((srows, srels, stok), sbins, {}, None, None)]
    seen_fail = Counter()
    for (rows, rels, ntok), bins, treated, pgbins, plugin in fams:
        fm, units = make(rows, rels, ntok, bins=bins, treated=treated, pgbins=pgbins, plugin=plugin)
        for _ in range(110):
            keep = rnd.choice([0.3, 0.6, 0.9, 0.97])
            S = frozenset(u for u in range(len(units)) if rnd.random() < keep)
            if not S:
                continue
            for nm, (v, d) in fm.all(S).items():                         # _finalize already asserts (SystemExit) on a mismatch
                assert (v == "fail") == (d > 0)
                seen_fail[nm] += v == "fail"
    failing = {k_ for k_, v in seen_fail.items() if v}
    assert failing >= {"rows_per_card", "token_mean", "freeform_share", "yes_no_share", "yes_rate", "g10_cells", "yes_is_bad_share", "twin_share",
                       "equiv_share", "complement_share_of_yes_no", "longest_option_pp", "abstain_wrong_share", "gold_position_cells",
                       "gold_rank_cells", "chi2_label_x_bin", "difficulty_caps", "medium_ge_45", "trap_type_cap", "g11_selected"}, sorted(failing)


def test_pair_family_baseline_is_clean():
    rows, rels, ntok = pair_family(60)
    fm, units = make(rows, rels, ntok)
    assert set(verdicts(fm, frozenset(range(len(units)))).values()) <= {"pass", "n/a"}


def test_g10_aggregate_and_cells_are_judged_by_the_mixer_function():
    rows, rels, ntok = pair_family(60, skew=lambda i: i % 10 == 0)
    fm, units = make(rows, rels, ntok)
    S = frozenset(range(len(units)))
    v, d = fm.all(S)["g10_cells"]
    assert v == "fail" and d > 0
    assert fm.all(S)["yes_rate"][0] == "fail"


# ------------------------------------------------------------------------------------------------ the loop
def test_yes_rate_repair_converges_in_reverse_priority_and_each_move_lowers_the_distance():
    rows, rels, ntok = pair_family(60, skew=lambda i: i % 10 == 3)                  # 6 skew units: 55% yes
    fm, units = make(rows, rels, ntok)
    S0, sel, rec = run(fm)
    assert rec["failing_before"] == ["yes_rate", "g10_cells"] and rec["failing_after"] == []
    sane(fm, S0, sel, rec)
    assert rec["moves"] and all(m["check"] == "yes_rate" for m in rec["moves"])
    dropped = [m["unit_first_id"] for m in rec["moves"]]
    skew_first_ids = [f"r{i}_0" for i in range(59, -1, -1) if i % 10 == 3]
    assert dropped == skew_first_ids[:len(dropped)]                       # lowest priority first, only units that help
    assert rec["stop_reason_by_check"]["yes_rate"] == "passed"


def test_loss_limit_stops_at_25_percent_and_the_check_still_fails():
    rows, rels, ntok = pair_family(100, skew=lambda i: i % 10 < 6)        # 60 skew units: 80% yes, needs 59% of the rows
    fm, units = make(rows, rels, ntok)
    S0, sel, rec = run(fm)
    assert rec["loss_limit_hit"] is True and rec["rows_pre_repair"] == 200 and rec["loss_max_rows"] == 50
    assert rec["rows_dropped"] == 50 and rec["units_dropped"] == 25         # exactly the limit; a 26th unit would be 52 rows > 50
    assert "yes_rate" in rec["failing_after"] and rec["stop_reason_by_check"]["yes_rate"] == "loss limit"
    assert rec["report_checks_additions"]["a49c_and_caps_pass"] is False
    sane(fm, S0, sel, rec)


TWIN_ORDER_KINDS = [("minimal_edit" if i in {10, 20, 30, 40, 1, 4, 7, 13, 16, 19, 22, 25, 28, 32, 35, 38, 44, 47}
                     else "equiv" if i in {50, 52, 54, 56, 58} else None) for i in range(60)]


def twin_order_family():
    """60 pairs: units 10/20/30/40 are (1,1) twin units (yes 53.3%: check 5 fails) and 14 more twin units make twin 30% (check 8
    fails); after the two yes-rate drops twin is still 27.6%, so twin moves follow."""
    return pair_family(60, skew=lambda i: i in {10, 20, 30, 40}, kinds=TWIN_ORDER_KINDS)


def test_checks_are_repaired_in_the_fixed_order():
    # yes rate (check 5) and twin share (check 8) both fail: the yes-rate moves come first, the twin moves after them
    rows, rels, ntok = twin_order_family()
    fm, units = make(rows, rels, ntok)
    S0, sel, rec = run(fm)
    assert {"yes_rate", "twin_share"} <= set(rec["failing_before"])
    idx = [RF.ORDER.index(m["check"]) for m in rec["moves"]]
    assert idx == sorted(idx) and rec["moves"][0]["check"] == "yes_rate"
    assert [m["check"] for m in rec["moves"]] == ["yes_rate", "yes_rate", "twin_share", "twin_share"]
    assert rec["failing_after"] == []
    sane(fm, S0, sel, rec)


def test_no_passing_check_fails_and_no_failing_distance_rises_replay_with_fresh_evaluators():
    rows, rels, ntok = twin_order_family()
    fm, units = make(rows, rels, ntok)
    S0, sel, rec = run(fm)
    assert len(rec["moves"]) >= 4
    by_first = {fm.first_id[u]: u for u in range(len(units))}
    S = frozenset(S0)
    fresh = lambda: make(rows, rels, ntok)[0]                                  # noqa: E731  a new evaluator, no memo
    for m in rec["moves"]:
        gone = {by_first[m["unit_first_id"]]} | {by_first[c[0]] for c in m["companions"]}
        S2 = S - gone
        B, A = fresh().all(S), fresh().all(S2)
        c = m["check"]
        assert A[c][1] < B[c][1] - 1e-12
        assert fresh().some(S - {by_first[m["unit_first_id"]]}, [c])[c][1] < B[c][1] - 1e-12      # u alone lowers it too
        for p in RF.PROTECTED:
            if B[p][0] != "fail":
                assert A[p][0] != "fail", (p, m)
            else:
                assert A[p][1] <= B[p][1] + 1e-12, (p, m)
        S = S2
    assert S == frozenset(sel)


def test_the_first_admissible_candidate_is_the_one_dropped_brute_force():
    rows, rels, ntok = twin_order_family()
    fm, units = make(rows, rels, ntok)
    S0, sel, rec = run(fm)
    assert len(rec["moves"]) == 4
    by_first = {fm.first_id[u]: u for u in range(len(units))}
    S, dropped = frozenset(S0), 0
    for m in rec["moves"]:
        c = m["check"]
        B = fm.all(S)
        chosen = by_first[m["unit_first_id"]]
        for u in [x for x in reversed(fm.order) if x in S]:
            M, comps = fm.move(S, u)
            A = fm.all(M)
            lost = fm.n_rows(S) - fm.n_rows(M)
            ok = (fm.some(S - {u}, [c])[c][1] < B[c][1] - 1e-12 and A[c][1] < B[c][1] - 1e-12 and RF.Family.protected_ok(B, A)
                  and dropped + lost <= rec["loss_max_rows"])
            if u == chosen:
                assert ok
                break
            assert not ok, f"an earlier candidate {fm.first_id[u]} was admissible"
        S, dropped = M, dropped + lost


def test_coupling_when_every_helping_drop_breaks_a_passing_check_there_is_no_move():
    # card k0 holds 67 rows (the defect). Twins sit only OUTSIDE k0 and make exactly 25.0%, so dropping any k0 unit (a non-twin)
    # pushes the twin share above 25% -> no unit is admissible, the check stays failing.
    tw = set(range(67, 117))
    rows, rels, ntok = choice_family(200, twin=lambda i: "minimal_edit" if i in tw else None, equiv=lambda i: 117 <= i < 129,
                                     card=lambda i: "k0" if i < 67 else f"k{1 + (i - 67) // 50}")
    fm, units = make(rows, rels, ntok)
    v = fm.all(frozenset(range(200)))
    assert v["rows_per_card"][0] == "fail" and v["twin_share"][0] == "pass"
    S0, sel, rec = run(fm)
    assert rec["moves"] == [] and sorted(sel) == list(range(200))
    assert rec["failing_after"] == ["rows_per_card"] and rec["stop_reason_by_check"]["rows_per_card"] == "no admissible unit"
    assert rec["report_checks_additions"]["a49c_and_caps_pass"] is False and rec["rows_dropped"] == 0


def test_nothing_refills_no_unit_added_rows_untouched_and_no_selection_function_called(monkeypatch):
    rows, rels, ntok = pair_family(60, skew=lambda i: i % 10 == 3)
    before = copy.deepcopy(rows)
    fm, units = make(rows, rels, ntok)

    def boom(*a, **k):
        raise AssertionError("a selection / swap / reselect function was called during the repair")
    for mod, name in ((cs, "select"), (cs, "select_any"), (a49c, "swap_balance"), (c2_select, "reselect"), (c2_select, "select_family"),
                      (c2_select, "trap_select"), (RF, "swap_balance_guarded"), (RF, "run_family")):
        monkeypatch.setattr(mod, name, boom)
    S0, sel, rec = run(fm)
    assert rec["moves"] and set(sel) < set(S0)
    assert rows == before and fm.rows is rows                             # no field edited
    kept_ids = {fm.rows[i]["id"] for u in sel for i in fm.units[u]}
    assert kept_ids <= {r["id"] for r in rows}
    assert rec["rows_after"] == len(kept_ids) == rec["rows_pre_repair"] - rec["rows_dropped"]


def test_deterministic_and_priority_order_drives_the_drops():
    rows, rels, ntok = pair_family(60, skew=lambda i: i % 10 == 3)
    a = run(make(rows, rels, ntok)[0])
    b = run(make(rows, rels, ntok)[0])
    assert json.dumps(a[2], sort_keys=True) == json.dumps(b[2], sort_keys=True) and a[1] == b[1]
    fm3, units = make(rows, rels, ntok, order=list(reversed(range(60))))
    c = run(fm3)
    assert c[1] != a[1] and c[2]["rows_dropped"] > 0                      # a different priority order drops different units


# ------------------------------------------------------------------------------------------------ per-check fixtures
def check_one(check, rows, rels, ntok, **kw):
    fm, units = make(rows, rels, ntok, **kw)
    S0, sel, rec = run(fm)
    assert check in rec["failing_before"], rec["failing_before"]
    sane(fm, S0, sel, rec)
    assert check not in rec["failing_after"], (rec["failing_after"], rec["stop_reason_by_check"][check])
    assert any(m["check"] == check for m in rec["moves"])
    assert verdicts(fm, frozenset(sel))[check] != "fail"
    return fm, S0, sel, rec


def test_token_mean():
    rows, rels, ntok = choice_family(200, tok=lambda i: 1500 if i % 20 == 0 else 780)
    fm, S0, sel, rec = check_one("token_mean", rows, rels, ntok)
    assert 4 <= rec["rows_dropped"] <= 8


def test_rows_per_card_67_to_64():
    rows, rels, ntok = choice_family(200, card=lambda i: "k0" if i < 67 else f"k{1 + (i - 67) // 50}")
    fm, S0, sel, rec = check_one("rows_per_card", rows, rels, ntok)
    assert [m["unit_first_id"] for m in rec["moves"]] == ["r66", "r65", "r64"]


def test_freeform_share():
    rows, rels, ntok = choice_family(200, author=lambda i: "F" if i % 25 < 7 else "S")
    check_one("freeform_share", rows, rels, ntok)


def test_twin_share_above_25():
    rows, rels, ntok = choice_family(200, twin=lambda i: "minimal_edit" if i % 100 < 28 else None, equiv=lambda i: 28 <= i < 40)
    check_one("twin_share", rows, rels, ntok)


def test_twin_share_below_20():
    rows, rels, ntok = choice_family(200, twin=lambda i: "minimal_edit" if i % 100 < 16 else None, equiv=lambda i: 22 <= i < 34)
    fm = make(rows, rels, ntok)[0]
    v = fm.all(frozenset(range(200)))["twin_share"]
    assert v[0] == "fail"                                                  # 16% < 20%: only more twin-rich selections fix it
    S0, sel, rec = run(fm)
    sane(fm, S0, sel, rec)


def test_equiv_share_below_5():
    rows, rels, ntok = choice_family(200, equiv=lambda i: 22 <= i < 31)    # 9 rows = 4.5%
    check_one("equiv_share", rows, rels, ntok)


def test_longest_option_positive_and_negative():
    for sign in (+1, -1):
        gl = (lambda i: (14, 8) if i % 25 in (3, 4, 5) else (12, 12)) if sign > 0 else (lambda i: (8, 14) if i % 25 in (3, 4, 5) else (12, 12))
        rows, rels, ntok = choice_family(200, gold_len=gl)
        fm, S0, sel, rec = check_one("longest_option_pp", rows, rels, ntok)
        assert fm.all(S0)["longest_option_pp"][0] == "fail"


def test_abstain_wrong_share():
    rows, rels, ntok = choice_family(200, abst_gold=lambda i: i % 25 < 14)       # 56% of the rows have the abstain option as gold
    check_one("abstain_wrong_share", rows, rels, ntok)


def test_gold_position_cells():
    rows, rels, ntok = choice_family(200, k=3, pos=lambda i: 0 if i % 20 < 9 else 1 + (i % 2))
    check_one("gold_position_cells", rows, rels, ntok)


def test_gold_rank_cells():
    rows, rels, ntok = choice_family(200, k=3, rank=lambda i: 0 if i % 20 < 9 else 1 + (i % 2))
    fm, S0, sel, rec = check_one("gold_rank_cells", rows, rels, ntok)
    assert fm.all(S0)["gold_position_cells"][0] == "pass"


def test_yes_no_share_high_and_low():
    rows, rels, ntok = pair_family(116, extra_choice=168)                           # yn 232 / 400 rows = 58%
    check_one("yes_no_share", rows, rels, ntok, )
    rows, rels, ntok = pair_family(84, extra_choice=232)                            # yn 168 / 400 = 42%
    fm, S0, sel, rec = check_one("yes_no_share", rows, rels, ntok)


def test_chi2_label_by_bin():
    # easy rows lean to position 0, medium rows lean to position 1, in total uniform: chi-square of label x bin fails (both maps)
    n = 200
    bins = {}
    rows, rels, ntok = choice_family(n, k=2, pos=lambda i: 0 if (i % 10 < 7 if i % 5 == 0 else i % 10 < 4) else 1,
                                     card=lambda i: f"k{i // 50}")
    for i, r in enumerate(rows):
        bins[r["id"]] = "easy" if i % 5 == 0 else "medium"
    fm, units = make(rows, rels, ntok, bins=bins)
    S0 = frozenset(range(n))
    a = fm.all(S0)
    assert a["chi2_a42d6"][0] == "fail" and a["chi2_pg"][0] == "fail" and a["chi2_label_x_bin"][0] == "fail"
    assert a["chi2_label_x_bin"][1] == pytest.approx(a["chi2_a42d6"][1] + a["chi2_pg"][1])
    sel, rec = fm.repair(S0)
    sane(fm, S0, sel, rec)
    assert rec["moves"] and all(m["distance_after"] < m["distance_before"] for m in rec["moves"])


def test_cap_pass_companions_are_part_of_the_move():
    # hard share exactly 30%; dropping one medium unit pushes it to 30.3%, so crowd_select's cap pass sheds a hard unit (no medium rows)
    n = 100
    rows, rels, ntok = choice_family(n, card=lambda i: "k0" if i < 65 else "k1", twin=lambda i: "minimal_edit" if i % 100 < 22 else None,
                                     equiv=lambda i: 22 <= i < 29)
    bins = {r["id"]: ("hard" if (i % 10 < 3) else "medium") for i, r in enumerate(rows)}   # 30 hard, 70 medium
    fm, units = make(rows, rels, ntok, bins=bins)
    S0 = frozenset(range(n))
    assert fm.all(S0)["rows_per_card"][0] == "fail" and fm.all(S0)["difficulty_caps"][0] == "pass"
    sel, rec = fm.repair(S0)
    assert rec["moves"][0]["check"] == "rows_per_card" and rec["moves"][0]["companions"], rec["moves"][0]
    assert rec["rows_dropped"] >= 2
    assert verdicts(fm, frozenset(sel))["difficulty_caps"] == "pass"
    sane(fm, S0, sel, rec)
    # the companion is the LAST (lowest priority) hard unit with no medium row
    M, comps = fm.move(S0, 64)
    assert comps == [next(u for u in reversed(fm.order) if u in S0 and u != 64 and bins[rows[u]["id"]] == "hard")]


def test_g11_blocks_a_move_that_would_push_a_template_above_two_percent():
    def build(shared):
        rows, rels, ntok = choice_family(200, card=lambda i: "k0" if i < 65 else f"k{1 + (i - 65) // 50}")
        for i, r in enumerate(rows):
            r["meta"]["wording_id"] = "wShared" if i >= 200 - shared else f"w{i}"
        return rows, rels, ntok
    rows, rels, ntok = build(4)                                                   # 4/200 = 2.0% -> passes; any drop makes it 4/199 > 2%
    fm, _ = make(rows, rels, ntok)
    S0 = frozenset(range(200))
    assert fm.all(S0)["g11_selected"][0] == "pass" and fm.all(S0)["rows_per_card"][0] == "fail"
    sel, rec = fm.repair(S0)
    assert rec["moves"] == [] and rec["stop_reason_by_check"]["rows_per_card"] == "no admissible unit"
    rows, rels, ntok = build(3)                                                   # 1.5%: room to drop one row
    fm, _ = make(rows, rels, ntok)
    sel, rec = fm.repair(frozenset(range(200)))
    assert len(rec["moves"]) == 1 and rec["failing_after"] == []


def test_trap_type_cap_blocks_the_second_drop_of_a_type_and_a_later_unit_is_used():
    rows, rels, ntok = pair_family(100, skew=lambda i: i in (97, 98, 99, 10, 20), twin_frac=0.22, equiv_frac=0.07)
    # treated units: A x3, B x3 (the skew units 97-99), C x3, D x1 -> N = 10, max 30%
    treated = {1: "A", 2: "A", 4: "A", 97: "B", 98: "B", 99: "B", 5: "C", 6: "C", 7: "C", 8: "D"}
    fm, units = make(rows, rels, ntok, treated=treated)
    S0 = frozenset(range(100))
    assert fm.all(S0)["trap_type_cap"][0] == "pass" and fm.all(S0)["yes_rate"][0] == "fail"
    sel, rec = fm.repair(S0)
    sane(fm, S0, sel, rec)
    firsts = [m["unit_first_id"] for m in rec["moves"]]
    assert firsts[0] == "r99_0"                                                  # N 10 -> 9, A = 3/9 = 33.3%: admissible
    assert "r98_0" not in firsts and "r97_0" not in firsts                       # a second B drop gives A = 3/8 = 37.5% > 35%: refused
    assert "r20_0" in firsts                                                     # an untreated skew unit is used instead
    assert verdicts(fm, frozenset(sel))["trap_type_cap"] == "pass" and rec["failing_after"] == []


def test_medium_share_is_protected():
    n = 100
    rows, rels, ntok = choice_family(n, card=lambda i: "k0" if i < 65 else "k1")
    bins = {r["id"]: ("medium" if i < 45 else "hard" if i < 55 else "easy") for i, r in enumerate(rows)}
    # medium 45% exactly (passes), easy 45% > 25% fails; card k0 holds 65 > 64: dropping any medium unit takes medium below 45%
    fm, units = make(rows, rels, ntok, bins=bins)
    a = fm.all(frozenset(range(n)))
    assert a["medium_ge_45"][0] == "pass"
    sel, rec = fm.repair(frozenset(range(n)))
    sane(fm, frozenset(range(n)), sel, rec)
    assert verdicts(fm, frozenset(sel))["medium_ge_45"] == "pass"


def test_pg_bin_easy_cap_is_part_of_the_difficulty_caps():
    n = 100
    rows, rels, ntok = choice_family(n)
    bins = {r["id"]: "medium" for r in rows}
    pgb = {r["id"]: ("easy" if i < 30 else "medium") for i, r in enumerate(rows)}      # 30% easy on the p_g bins, 0% on the A42-D 6 bins
    fm, units = make(rows, rels, ntok, bins=bins, pgbins=pgb)
    v = fm.all(frozenset(range(n)))["difficulty_caps"]
    assert v[0] == "fail" and v[1] == pytest.approx(0.30 - 0.25 - 1e-9, abs=1e-6)


def test_tokens_are_required():
    rows, rels, ntok = choice_family(20)
    with pytest.raises(SystemExit):
        make(rows, rels, {k: v for k, v in ntok.items() if k != "r3"})


# ------------------------------------------------------------------------------------------------ swap guard (c)
def test_guarded_swap_with_no_guard_is_identical_to_a49c_swap_balance():
    rows, rels, ntok = pair_family(100, skew=lambda i: i % 3 == 0)
    units = cs.units_of(rows, rels)
    bins = {r["id"]: "medium" for r in rows}
    sel = list(range(0, 100, 2))
    a = a49c.swap_balance(FAM, rows, units, sel, bins, 20261013, never_in={5})
    b = RF.swap_balance_guarded(FAM, rows, units, sel, bins, 20261013, guard=None, never_in={5})
    assert a[0] == b[0] and {k: v for k, v in b[1].items() if k != "guard_rejections"} == a[1]


def test_swap_guard_refuses_a_swap_that_breaks_a_passing_check_and_takes_the_next_partner():
    rows, rels, ntok = pair_family(100, skew=lambda i: i % 3 == 0)
    units = cs.units_of(rows, rels)
    bins = {r["id"]: "medium" for r in rows}
    sel = list(range(0, 100, 2))
    base, info = RF.swap_balance_guarded(FAM, rows, units, sel, bins, 20261013)
    assert info["swaps"] > 0
    calls = []

    def guard(old, new):
        calls.append((tuple(old), tuple(new)))
        return len(calls) % 2 == 0                                             # refuse every odd attempt
    g, ginfo = RF.swap_balance_guarded(FAM, rows, units, sel, bins, 20261013, guard=guard)
    assert ginfo["guard_rejections"] >= 1
    assert all(set(o) != set(n) for o, n in calls)
    assert len(g) == len(sel) and len(set(g)) == len(g)
    never = RF.swap_balance_guarded(FAM, rows, units, sel, bins, 20261013, guard=lambda o, n: False)
    assert never[0] == sel and never[1]["swaps"] == 0 and never[1]["guard_rejections"] > 0


def test_family_guard_is_pass_to_fail_only():
    rows, rels, ntok = choice_family(200)
    fm, units = make(rows, rels, ntok)
    full = list(range(200))
    assert fm.guard(full, full) is True
    assert fm.guard(full, full[:-1]) is True                                  # one non-twin row less: every share stays in its band
    nontwin = [u for u in full if rows[u]["meta"]["twin_kind"] is None]
    assert fm.guard(full, [u for u in full if u not in set(nontwin[-40:])]) is False      # 40 non-twin rows less: twin 44/160 = 27.5% fails
    # a check that FAILS before the swap may stay failing (the guard is pass -> fail only)
    bad_rows, bad_rels, bad_tok = choice_family(200, tok=lambda i: 1500 if i % 20 == 0 else 780)
    fm2, _ = make(bad_rows, bad_rels, bad_tok)
    assert fm2.all(frozenset(full))["token_mean"][0] == "fail"
    assert fm2.guard(full, full[:-1]) is True


# ------------------------------------------------------------------------------------------------ (f)(ii)
F4 = {k: True for k in RF.F_CHECKS}                      # the four A69 (f) report.checks entries (A80 L2: required)
CHK_SHORT = {"total_eq_target": False, "chi2_p_gt_0.01": True, "easy_le_25": True, "hard_le_30": True, "medium_ge_45": True} | F4


def rec_of(selected, target, pre, dropped, checks=None, units_removed=0, layout="a78", a34e=None, **kw):
    rp = {"rows_pre_repair": pre, "rows_dropped": dropped} if layout == "a78" else {"totals_before": {"rows": pre}, "rows_dropped": dropped}
    s = {"candidates_sha256": "x", "target": target, "selected_ids": list(range(selected)), "exclude_ids": {"units_removed": units_removed},
         "report": {"checks": dict(checks or CHK_SHORT), "pass": False}} | kw
    if layout == "a78":
        s["a69"] = {"repair": rp} | ({} if a34e is None else {"a34e": {"short_only_because_g13": a34e}})
    else:
        s["report"]["a69"] = {"repair": rp}
    return s


@pytest.mark.parametrize("layout", ["a78", "legacy"])
def test_f_ii_accepts_exactly_the_adopted_arithmetic(layout):
    # pre-repair at target, 20% dropped, only total_eq_target failed
    assert RF.selection_problem_faithful(rec_of(800, 1000, 1000, 200, layout=layout), "x", 1000) is None
    # exactly 25% is allowed, one more row is not
    assert RF.selection_problem_faithful(rec_of(750, 1000, 1000, 250, layout=layout), "x", 1000) is None
    assert RF.selection_problem_faithful(rec_of(749, 1000, 1000, 251, layout=layout), "x", 1000) is not None
    # the T33 numbers: 390 of 450 (86.7%) dropped, G13 removed units: refused
    why = RF.selection_problem_faithful(rec_of(60, 2400, 450, 390, units_removed=2217, layout=layout), "x", 2400)
    assert why and "25%" in why
    # rows_pre - rows_dropped must equal the rows selected
    assert RF.selection_problem_faithful(rec_of(790, 1000, 1000, 200, layout=layout), "x", 1000) is not None
    # another failed check
    bad = {**CHK_SHORT, "chi2_p_gt_0.01": False}
    assert RF.selection_problem_faithful(rec_of(800, 1000, 1000, 200, checks=bad, layout=layout), "x", 1000) is not None
    # pre-repair short of target: needs A34 (e) read literally (G13-removed units AND the record's flag: short ONLY because of them) or an upper-bound target
    assert RF.selection_problem_faithful(rec_of(700, 1000, 900, 200, layout=layout), "x", 1000) is not None
    assert RF.selection_problem_faithful(rec_of(700, 1000, 900, 200, units_removed=5, layout=layout), "x", 1000) is not None      # the loose reading is refused (L3)
    if layout == "a78":
        assert RF.selection_problem_faithful(rec_of(700, 1000, 900, 200, units_removed=5, a34e=True), "x", 1000) is None
        assert RF.selection_problem_faithful(rec_of(700, 1000, 900, 200, units_removed=5, a34e=False), "x", 1000) is not None
        assert RF.selection_problem_faithful(rec_of(700, 1000, 900, 200, units_removed=0, a34e=True), "x", 1000) is not None       # a flag without removed units is nothing
    assert RF.selection_problem_faithful(rec_of(700, 1000, 900, 200, layout=layout), "x", 1000, at_most=True) is None


def test_f_ii_other_refusals_and_the_unrepaired_a34e_path():
    assert RF.selection_problem_faithful(None, "x", 10) and RF.selection_problem_faithful(rec_of(8, 10, 10, 2), "other", 10)
    assert RF.selection_problem_faithful(rec_of(8, 11, 10, 2), "x", 10)                              # wrong target
    assert RF.selection_problem_faithful(rec_of(8, 10, 10, 2, scratch=True), "x", 10)                # a scratch record
    # no repair drops: A34 (e) read literally decides (G13 removed units AND the literal flag)
    s = rec_of(900, 1000, 900, 0, units_removed=3, a34e=True)
    assert RF.selection_problem_faithful(s, "x", 1000) is None
    assert RF.selection_problem_faithful(rec_of(900, 1000, 900, 0, units_removed=3), "x", 1000)               # units removed, no flag: refused (L3)
    assert RF.selection_problem_faithful(rec_of(900, 1000, 900, 0, units_removed=3, a34e=False), "x", 1000)
    assert RF.selection_problem_faithful(rec_of(900, 1000, 900, 0), "x", 1000)
    assert RF.selection_problem_faithful(rec_of(900, 1000, 900, 0, units_removed=3, a34e=True, checks={**CHK_SHORT, "easy_le_25": False}), "x", 1000)
    # L1: rows_pre_repair - rows_dropped must equal the rows selected ALSO when nothing was dropped
    assert RF.selection_problem_faithful(rec_of(890, 1000, 900, 0, units_removed=3, a34e=True), "x", 1000)
    assert "!= rows selected" in RF.selection_problem_faithful(rec_of(1000, 1000, 990, 0, checks={k: True for k in CHK_SHORT}), "x", 1000)
    # L1: a record with no repair block is refused, even when everything else passes
    ok = rec_of(1000, 1000, 1000, 0, checks={k: True for k in CHK_SHORT})
    ok["report"]["pass"] = True
    assert RF.selection_problem_faithful(ok, "x", 1000) is None
    ok.pop("a69")
    assert "no repair block" in RF.selection_problem_faithful(ok, "x", 1000)
    noblock = rec_of(900, 1000, 900, 0, units_removed=3, a34e=True)
    noblock["a69"] = {"repair": "not run (repair=False)", "a34e": {"short_only_because_g13": True}}
    assert "no repair block" in RF.selection_problem_faithful(noblock, "x", 1000)
    # L2: the four (f) entries are required
    for k in RF.F_CHECKS:
        drop = {c: v for c, v in CHK_SHORT.items() if c != k}
        why = RF.selection_problem_faithful(rec_of(800, 1000, 1000, 200, checks=drop), "x", 1000)
        assert why and k in why
    # a record that passes everything at target
    ok = rec_of(1000, 1000, 1000, 0, checks={k: True for k in CHK_SHORT})
    ok["report"]["pass"] = True
    assert RF.selection_problem_faithful(ok, "x", 1000) is None
    ok["report"]["pass"] = False
    assert RF.selection_problem_faithful(ok, "x", 1000)


def test_literal_a34e_is_never_looser_than_the_loose_mix_rule_for_an_unrepaired_short_record():
    for sel_n, units_removed, at_most, checks, flag in [(900, 3, False, CHK_SHORT, True), (900, 3, False, CHK_SHORT, None), (900, 3, False, CHK_SHORT, False),
                                                        (900, 0, False, CHK_SHORT, True), (900, 0, True, CHK_SHORT, None),
                                                        (900, 3, False, {**CHK_SHORT, "hard_le_30": False}, True)]:
        s = rec_of(sel_n, 1000, sel_n, 0, checks=checks, units_removed=units_removed, a34e=flag)
        s["report"]["pass"] = False
        mine = RF.selection_problem_faithful(s, "x", 1000, at_most=at_most)
        loose = mix_c2.selection_problem(s, "x", 1000, at_most=at_most)                # the non-program path: any G13-removed unit
        assert not (mine is None and loose is not None), (sel_n, units_removed, at_most, flag)      # never looser
        if units_removed and flag is not True and not at_most and checks is CHK_SHORT:
            assert mine is not None and loose is None                                  # the literal reading refuses what the loose one admitted


# ------------------------------------------------------------------------------------------------ end to end (in memory)
TAGS = ["tA", "tB", "tC", "tD"]


def e2e_pool(n_units=240, seed=5):
    """Choice units with error-model tags and C1 probabilities, plus yes/no complement pairs: a small A69 family."""
    rnd = random.Random(seed)
    rows, rels, probs, ntok = [], [], {}, {}
    for u in range(n_units):
        if u % 3 == 0:                                                         # a yes/no complement pair
            g = (1, 0)
            for j in range(2):
                rid = f"u{u}_{j}"
                rows.append({"id": rid, "call_id": f"cu{u}", "qtype": "noul", "gold": g[j], "options": None, "instructions": "Is it so?",
                             "meta": _meta(rid, "minimal_edit" if u % 50 < 12 else ("equiv" if u % 50 < 15 else None), f"k{u // 20}", "S")})
                py = rnd.choice([0.05, 0.5, 0.95])
                probs[rid] = {"yes": py, "no": 1 - py}
                ntok[rid] = 700
            rels.append({"a": f"u{u}_0", "b": f"u{u}_1", "type": "complement"})
        else:
            rid = f"u{u}"
            k = 3
            opts = [f"o{u}_{x}_" + "x" * 8 for x in range(k)]
            gold = opts[u % k]
            oe = {o: [rnd.choice(TAGS)] for o in opts if o != gold and rnd.random() < 0.7}
            rows.append({"id": rid, "call_id": f"cu{u}", "qtype": "choice", "gold": gold, "options": opts, "instructions": "Which?",
                         "meta": _meta(rid, "minimal_edit" if u % 50 < 12 else ("equiv" if u % 50 < 15 else None), f"k{u // 20}", "S",
                                       extra={"opt_err": oe} if oe else None)})
            w = [rnd.random() ** 2 for _ in opts]
            probs[rid] = {o: x / sum(w) for o, x in zip(opts, w)}
            ntok[rid] = 700
    pg = {r["id"]: cs.p_gold(r, probs[r["id"]]) for r in rows}
    return rows, rels, probs, pg, ntok


def test_end_to_end_in_memory_subset_deterministic_and_nothing_refilled():
    rows, rels, probs, pg, ntok = e2e_pool()
    kw = dict(fam=FAM, rows=rows, rels=rels, pg=pg, probs=probs, target=180, ntok=ntok, plugin=FakePlugin())
    a = RF.run_family(**kw)
    b = RF.run_family(**kw)
    assert a["selected_ids"] == b["selected_ids"] and json.dumps(a["repair"], sort_keys=True) == json.dumps(b["repair"], sort_keys=True)
    assert set(a["sel"]) <= set(a["pre_repair_sel"]) | {u for u in range(len(a["units"]))}
    pre_ids = {a["rows"][i]["id"] for u in a["pre_repair_sel"] for i in a["units"][u]}
    assert set(a["selected_ids"]) <= pre_ids                                    # the repair only removed
    assert a["repair"]["rows_pre_repair"] == len(pre_ids) and a["repair"]["rows_after"] == len(a["selected_ids"])
    assert a["repair"]["seed"] == 20261013 and a["repair"]["key"] == FAM
    s = {"report": {"checks": {"total_eq_target": a["repair"]["rows_after"] == 180}}, "a69": {"repair": a["repair"]}}
    assert RF.repair_numbers(s) == {"rows_pre_repair": a["repair"]["rows_pre_repair"], "rows_dropped": a["repair"]["rows_dropped"]}


def test_distance_helpers_and_group_calls_do_not_edit_rows():
    rows, rels, probs, pg, ntok = e2e_pool(60)
    snap = copy.deepcopy(rows)
    out = RF.run_family(FAM, rows, rels, pg, probs, 40, ntok, plugin=FakePlugin())
    assert rows == snap and out["selected_ids"]


def test_no_forbidden_path_is_named_by_the_module():
    for f in (C2B / "a69_faithful.py", C2B / "zed_orch" / "a78" / "repair_a69_faithful.py"):
        src = f.read_text().lower()
        code = "\n".join(ln for ln in src.splitlines() if not ln.strip().startswith(("#", '"""')))
        for bad in ("ohs", "sealed", "external_quarantine", "longbench", ".claude", "preread", "c_spec"):
            assert bad not in code, (f.name, bad)


def test_the_a78_name_is_a_thin_import_of_the_c2_build_module():
    import a69_faithful
    assert RF is a69_faithful and RF.Family is a69_faithful.Family                  # the same module object, so the A78 scratch scripts and these tests see one code
    thin = (C2B / "zed_orch" / "a78" / "repair_a69_faithful.py").read_text()
    assert len(thin.splitlines()) < 20 and "def " not in thin and "class " not in thin
