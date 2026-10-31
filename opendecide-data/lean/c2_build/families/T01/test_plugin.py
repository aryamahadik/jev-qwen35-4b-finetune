"""families/T01/test_plugin.py: in-memory tests for the T01 plugin (A37 f: nothing is written; no Haiku, no network).

  contract        validate_plugin(strict) == [], solver-B independence, G0-lite frozen and <= 200 lines
  hand cases      golds worked out by hand (the task_ranking example, the G0 ambiguity points) == solver A == B
  G2 / G3         solver A == solver B and parse == canonical on 5,004 sampled specs (+ every complement form)
  pipeline        every kit program gate (G2, G3, G4, G-SL, G-LEX, G-TW, schema; G15 on a slice) on 900 units,
                  and the spec 4.1 overlay shares
  relations       twins differ in exactly one input slot and the gold moves as constructed; complements opposite;
                  G4 metamorphic predictions hold
  balance         gold labels inside the G0 section 4 bands on 2,004 specs; trap shares; gold positions; on ordered
                  choice sets the gold's sorted rank is the label-blind target (uniform per question form and k),
                  and neither "the middle / second-highest option" nor "the option that is the sum of two others"
                  finds the gold
  G-SL            the built-in placeholder skins and wordings lint clean; no literal value or gold-label word
                  outside the slots of any rendered row or program template
  determinism     same seed -> same spec and rows
  injected bugs   G2, G3, G-TW and G-SL catch a broken solver B, solver A, renderer, twin prediction and skin
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T01
"""
from __future__ import annotations

import collections
import dataclasses
import datetime as dt
import hashlib
import os
import random
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import gsl, paths, pipeline  # noqa: E402
from c2_kit import distractors as DI  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.plugin import Spec  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from families.T01 import fixtures as FX  # noqa: E402
from families.T01 import plugin as P  # noqa: E402
from families.T01 import solver_b as B  # noqa: E402

SAMPLERS = P.T01.SAMPLERS
TRAINING = tuple(s for s in SAMPLERS if s not in P.T01.HELD_OUT_SAMPLERS)
D = dt.date
DAYS = ("day", "days")
TOKENIZER = Path(os.path.expanduser("~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/"
                                    "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/tokenizer.json"))


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T01(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs(plugin):
    """2,004 specs: seeds 0-333 (167 whole seed pairs) x 6 samplers."""
    return [plugin.sample(seed, smp) for seed in range(334) for smp in SAMPLERS]


DROP = "the error models leave a side of the gold empty"


def _render(plugin, ctx, spec, **kw):
    """Render, or None when the option set cannot be built (the spec is dropped: kit distractors.py)."""
    try:
        return plugin.render(spec, ctx, **kw)
    except K.RenderError as e:
        assert DROP in str(e) or "copies a printed date" in str(e), e
        return None


def _check_row(plugin, ctx, spec, rr):
    """G2 + G3 on one rendered row: parse == canonical, solver B == solver A, options read back to their keys."""
    view = plugin.parse(rr.row, ctx)
    facts = {k: v for k, v in view.items() if k != "options"}
    assert facts == plugin.canonical_for(spec, rr.row["meta"]["c2"]["author_mode"]), (spec.seed, spec.sampler)
    gold = plugin.solve_a(spec)
    assert plugin.solve_b(view) == gold == rr.answer, (spec.seed, spec.sampler, spec.qform)
    if rr.row["qtype"] == "choice":
        assert view["options"][rr.row["options"].index(rr.row["gold"])] == gold
        assert len(set(map(repr, view["options"]))) == len(view["options"])
    return gold


# ------------------------------------------------------------------------------------------------ contract

def test_plugin_meets_the_strict_contract(plugin):
    assert KP.validate_plugin(plugin, strict=True) == []
    assert KP.check_independence(plugin) == []
    assert plugin.PARADIGM_A != plugin.PARADIGM_B
    g0 = Path(plugin.G0_LITE)
    assert len(g0.read_text(encoding="utf-8").splitlines()) <= 200
    assert hashlib.sha256(g0.read_bytes()).hexdigest() == plugin.G0_SHA256


def test_solver_b_shares_no_code_with_solver_a():
    src = Path(B.__file__).read_text(encoding="utf-8")
    assert "families.T01.plugin" not in src and "c2_kit.rules" not in src and "glob_a" not in src
    assert "import plugin" not in src and "from . import" not in src
    for name in KP.B_FORBIDDEN_NAMES:
        assert not re.search(rf"\b{name}\b", src), name


def test_card_text_copies_agree():
    """Solver B keeps its own copy of the G0 1.1 card text; it must equal the renderer's, word for word."""
    assert set(B.CARD) == set(P.RULES)
    for kind, text in P.RULES.items():
        assert B.CARD[kind] == text.replace("{M_WIN:adj}", "{M_WIN}"), kind
    assert B.CW == P.CLOSED_WORLD


def test_fixture_lexicon_forms_pass_their_unit_tests(ctx):
    reg = ctx.lexicon
    assert all(f.unit_ok for f in reg.forms.values()), {k: f.unit_problems for k, f in reg.forms.items()
                                                         if not f.unit_ok}
    assert reg.gate()["pass"]
    window = [f for f in reg.forms.values() if f.kind == "window"]
    assert window and all(f.required == 3 for f in window)           # window rules: 3/3 extraction
    assert {x.qform for x in ctx.skins.values() if x.kind == "wording"} == set(P.T01.FROZEN_QFORMS)


# ------------------------------------------------------------------------------------------------ hand cases

def _hand(plugin, kind, qform, slots, structure, clause=None):
    base = {"PERSON": S.name_slot("Dana Okafor"), "REF": S.id_slot("FILE-1001"),
            "TOPIC": S.name_slot(P.TOPICS[kind][0])}
    if clause:
        name, sem, bind = clause
        base[name] = plugin._clause(sem, random.Random(0), bind)
    spec = Spec("T01", "S1", 7, f"T01:S1:{kind}:c00", qform, {**base, **slots},
                structure={"kind": kind, "style": "list", **structure})
    return plugin.derive(spec)


def _both(plugin, ctx, spec):
    """Hand-built specs test the arithmetic, not the option cues (test_i1_fixes covers those): cue matching is off."""
    plugin.CUE_MATCH = False
    try:
        rr = plugin.render(spec, ctx)
    finally:
        del plugin.CUE_MATCH
    return _check_row(plugin, ctx, spec, rr)


def _rolling(plugin, qform, ref, stays, n=90, m=180):
    slots = {"N_MAX": S.count_slot(n, DAYS), "M_WIN": S.count_slot(m, DAYS), "REF_DATE": S.date_slot(ref)}
    names = []
    for k, (a, b) in enumerate(stays, 1):
        slots[f"SI_{k}"], slots[f"SO_{k}"] = S.date_slot(a), S.date_slot(b)
        names.append([f"SI_{k}", f"SO_{k}"])
    return _hand(plugin, "rolling", qform, slots, {"stays": names},
                 ("WIN_CLAUSE", "win.rolling_cap", {"N": "N_MAX", "M": "M_WIN"}))


def test_hand_rolling_window(plugin, ctx):
    """task_ranking T01 example: 1-30 Jan and 1 Mar-30 Apr 2026, 90 in any 180, reference 30 Jun 2026. The window
    starts 2 Jan 2026 (30 Jun - 179 days): 29 + 61 = 90 days present, not over the limit (gold "no")."""
    stays = [(D(2026, 1, 1), D(2026, 1, 30)), (D(2026, 3, 1), D(2026, 4, 30))]
    spec = _rolling(plugin, "yn_over", D(2026, 6, 30), stays)
    assert spec.derived["WIN_START"].value == D(2026, 1, 2)
    assert _both(plugin, ctx, spec) == 0
    assert _both(plugin, ctx, spec.replace(qform="yn_within")) == 1
    assert _both(plugin, ctx, spec.replace(qform="ch_days")) == 90
    one_more = _rolling(plugin, "yn_over", D(2026, 6, 30), [stays[0], (D(2026, 3, 1), D(2026, 5, 1))])
    assert _both(plugin, ctx, one_more) == 1                         # 91 days: over
    # wrong options are misreadings: calendar year / whole stays / straddle in full / window from 1 Jan 91, straddle
    # dropped 61, exit days left out 88, window from 3 Jan 89, each stay through the day after its exit 92
    plugin.CUE_MATCH = False                      # the hand case checks the error models, not the option cues
    try:
        rr = plugin.render(spec.replace(qform="ch_days"), ctx)
    finally:
        del plugin.CUE_MATCH
    keys = [o.key for o in rr.option_set.options]
    assert 90 in keys and set(keys) - {90} <= {91, 61, 88, 89, 92} and len(keys) >= 3
    assert sorted(keys).index(90) == rr.option_set.meta["gold_rank"]
    em = plugin.error_models()
    ch = spec.replace(qform="ch_days")
    assert em["calendar_year"].fn(ch) == 91 and em["drop_inclusive_endpoint"].fn(ch) == 88
    assert em["t01_straddle_dropped"].fn(ch) == 61 and em["t01_straddle_full"].fn(ch) == 91


def test_hand_later_anchor(plugin, ctx):
    """Decision 2 Mar 2026, delivery 9 Mar 2026, 30 days after the later date: the final day is 8 Apr 2026."""
    slots = {"ACTION": S.name_slot("appeal"), "EVA_LABEL": S.name_slot("decision date"),
             "EVB_LABEL": S.name_slot("delivery date"), "EVENT_A": S.date_slot(D(2026, 3, 2)),
             "EVENT_B": S.date_slot(D(2026, 3, 9)), "N_DAYS": S.count_slot(30, DAYS)}
    clause = ("AN_CLAUSE", "win.later_anchor", {"N": "N_DAYS"})
    dl = _hand(plugin, "anchor", "ch_deadline", slots, {"filed": False}, clause)
    assert _both(plugin, ctx, dl) == "2026-04-08"
    assert plugin.error_models()["earlier_anchor"].fn(dl) == "2026-04-01"
    for filed, want in ((D(2026, 4, 8), 1), (D(2026, 4, 9), 0), (D(2026, 3, 9), 1)):
        spec = _hand(plugin, "anchor", "yn_timely", {**slots, "FILED_DATE": S.date_slot(filed)}, {"filed": True},
                     clause)
        assert _both(plugin, ctx, spec) == want, filed
        assert _both(plugin, ctx, spec.replace(qform="yn_fail_time")) == 1 - want


def test_hand_waiting_period(plugin, ctx):
    """Start 10 Jan 2026, 30-day waiting period whose day 1 is 11 Jan: day 30 is 9 Feb (not covered), the first
    covered day is 10 Feb. A rider effective 1 Mar 2026 moves the first covered day to 1 Apr 2026."""
    slots = {"PERIL": S.name_slot("flood damage"), "START_DATE": S.date_slot(D(2026, 1, 10)),
             "W_DAYS": S.count_slot(30, DAYS)}
    clause = ("WAIT_CLAUSE", "win.wait_after", {"W": "W_DAYS"})
    assert _both(plugin, ctx, _hand(plugin, "waiting", "ch_first_day", slots, {"rider": False, "loss": False},
                                    clause)) == "2026-02-10"
    for loss, want in ((D(2026, 2, 9), 0), (D(2026, 2, 10), 1)):
        spec = _hand(plugin, "waiting", "yn_covered", {**slots, "LOSS_DATE": S.date_slot(loss)},
                     {"rider": False, "loss": True}, clause)
        assert _both(plugin, ctx, spec) == want
        assert _both(plugin, ctx, spec.replace(qform="yn_in_waiting")) == 1 - want
    rider = {**slots, "RIDER_DATE": S.date_slot(D(2026, 3, 1))}
    first = _hand(plugin, "waiting", "ch_first_day", rider, {"rider": True, "loss": False}, clause)
    assert _both(plugin, ctx, first) == "2026-04-01"
    assert plugin.error_models()["wrong_anchor"].fn(first) == "2026-02-10"
    late = _hand(plugin, "waiting", "yn_covered", {**rider, "LOSS_DATE": S.date_slot(D(2026, 3, 31))},
                 {"rider": True, "loss": True}, clause)
    assert _both(plugin, ctx, late) == 0                             # day 30 of the rider's period


def test_hand_purchase_window_and_comparator(plugin, ctx):
    """Request 30 May 2026 for $4,000, 30-day window from 1 May: $3,000 on 1 May counts, $5,000 on 30 Apr does not.
    Total $7,000 against $7,000: "more than" -> no quotes; "or more" -> quotes."""
    slots = {"VENDOR": S.name_slot("Halden Tools"), "M_WIN": S.count_slot(30, DAYS),
             "REQ_DATE": S.date_slot(D(2026, 5, 30)), "REQ_AMT": S.cents_slot(400000),
             "THRESHOLD": S.cents_slot(700000), "PD_1": S.date_slot(D(2026, 4, 30)), "PA_1": S.cents_slot(500000),
             "PD_2": S.date_slot(D(2026, 5, 1)), "PA_2": S.cents_slot(300000)}
    st = {"prior": [["PD_1", "PA_1"], ["PD_2", "PA_2"]]}
    for sem, want in (("cmp.gt", 0), ("cmp.ge", 1)):
        spec = _hand(plugin, "purchase", "yn_quotes", slots, st, ("CMP", sem, {"X": "THRESHOLD"}))
        assert spec.derived["WIN_START"].value == D(2026, 5, 1)
        assert _both(plugin, ctx, spec) == want
        assert _both(plugin, ctx, spec.replace(qform="yn_quotes_without")) == 1 - want
        tot = spec.replace(qform="ch_total")
        assert _both(plugin, ctx, tot) == 700000
        em = plugin.error_models()
        assert em["drop_inclusive_endpoint"].fn(tot) == 400000 and em["add_exclusive_endpoint"].fn(tot) == 1200000
        assert em["t01_request_only"].fn(tot) == 400000 and em["t01_ignore_window"].fn(tot) == 1200000


def test_hand_cash_never_netted(plugin, ctx):
    """Deposits $6,000 + $5,000 on 15 Jul 2026 (more than $10,000), withdrawals $9,000: report on deposits only.
    Netting gives $2,000 (no report); adding the $4,000 withdrawal of 14 Jul gives both."""
    txns = [(D(2026, 7, 14), "out", 400000), (D(2026, 7, 15), "in", 600000), (D(2026, 7, 15), "out", 900000),
            (D(2026, 7, 15), "in", 500000)]
    slots = {"DAY": S.date_slot(D(2026, 7, 15)), "THRESHOLD": S.cents_slot(1000000)}
    names = []
    for k, (d, direction, amt) in enumerate(txns, 1):
        slots[f"TD_{k}"], slots[f"TT_{k}"] = S.date_slot(d), S.category_slot(direction, P.DIRS)
        slots[f"TA_{k}"] = S.cents_slot(amt)
        names.append([f"TD_{k}", f"TT_{k}", f"TA_{k}"])
    spec = _hand(plugin, "cash", "ch_cash_which", slots, {"txns": names}, ("CMP", "cmp.gt", {"X": "THRESHOLD"}))
    assert _both(plugin, ctx, spec) == "in"
    em = plugin.error_models()
    assert em["netting"].fn(spec) == "neither" and em["t01_sum_across_days"].fn(spec) == "both"
    assert _both(plugin, ctx, spec.replace(qform="yn_cash_report")) == 1
    assert _both(plugin, ctx, spec.replace(qform="yn_cash_without")) == 0


def test_hand_addon_and_closures(plugin, ctx):
    """Notice 14 Dec 2026 + 10 days = 24 Dec; by post + 3 days = 27 Dec; 27 and 28 Dec closed -> due 29 Dec."""
    slots = {"NOTICE_DATE": S.date_slot(D(2026, 12, 14)), "METHOD": S.category_slot("post", P.METHODS),
             "N_DAYS": S.count_slot(10, DAYS), "K_DAYS": S.count_slot(3, DAYS),
             "CL_1": S.date_slot(D(2026, 12, 24)), "CL_2": S.date_slot(D(2026, 12, 27)),
             "CL_3": S.date_slot(D(2026, 12, 28))}
    spec = _hand(plugin, "addon", "ch_due", slots, {"closed": ["CL_1", "CL_2", "CL_3"]})
    assert spec.derived["BASE_DATE"].value == D(2026, 12, 24)
    assert _both(plugin, ctx, spec) == "2026-12-29"
    em = plugin.error_models()
    assert em["t01_skip_addon"].fn(spec) == "2026-12-25" and em["t01_ignore_closure"].fn(spec) == "2026-12-27"
    assert em["wrong_roll_direction"].fn(spec) == "2026-12-26" and em["t01_addon_not_post"].fn(spec) is None
    hand = spec.with_slot("METHOD", S.category_slot("hand", P.METHODS))
    assert _both(plugin, ctx, plugin.derive(hand)) == "2026-12-25"


@pytest.mark.parametrize("sent, on_time, received", [
    (dt.datetime(2026, 3, 5, 10, 30, tzinfo=dt.timezone(dt.timedelta(hours=-5))), 0, "2026-03-06"),   # 17:30 office
    (dt.datetime(2026, 3, 5, 10, 0, tzinfo=dt.timezone(dt.timedelta(hours=-5))), 1, "2026-03-05"),    # 17:00 sharp
    (dt.datetime(2026, 3, 4, 12, 0, tzinfo=dt.timezone(dt.timedelta(hours=-5))), 1, "2026-03-05"),    # eve, after
    (dt.datetime(2026, 3, 5, 23, 30, tzinfo=dt.timezone(dt.timedelta(hours=9))), 1, "2026-03-05"),    # 16:30 office
])
def test_hand_cutoff_conversion(plugin, ctx, sent, on_time, received):
    """Due 5 Mar 2026, office cutoff 17:00 (UTC+02:00) every day; the sending time is in another offset."""
    st = {"office": 120, "cut": [17, 0]}
    slots = {"DUE_DATE": S.date_slot(D(2026, 3, 5)), "SENT": S.datetime_slot(sent)}
    spec = _hand(plugin, "cutoff", "yn_on_time", slots, st)
    assert _both(plugin, ctx, spec) == on_time
    assert _both(plugin, ctx, spec.replace(qform="yn_late_cut")) == 1 - on_time
    assert _both(plugin, ctx, spec.replace(qform="ch_receipt_day")) == received


def test_g0_v2_invariant_breaks_are_refused_by_solver_b(plugin, ctx):
    """G0 v2 DF4-DF7 (Haiku pass H1, H5, H13, H16): rows the generator never makes have no printed rule, so solver B
    refuses them (the unit is dropped); the boundary cases the card does print still pass A == B."""
    def refused(spec, solve=False):
        rr = plugin.render(spec, ctx)
        with pytest.raises(B.ParseError):
            view = plugin.parse(rr.row, ctx)
            if solve:
                plugin.solve_b(view)
    ev = {"ACTION": S.name_slot("appeal"), "EVA_LABEL": S.name_slot("decision date"),
          "EVB_LABEL": S.name_slot("delivery date"), "EVENT_A": S.date_slot(D(2026, 3, 2)),
          "EVENT_B": S.date_slot(D(2026, 3, 9)), "N_DAYS": S.count_slot(30, DAYS)}
    clause = ("AN_CLAUSE", "win.later_anchor", {"N": "N_DAYS"})
    with pytest.raises(S.SlotError):                                 # filed before the later event: the printed day
        _hand(plugin, "anchor", "yn_timely", {**ev, "FILED_DATE": S.date_slot(D(2026, 3, 8))}, {"filed": True},
              clause)                                                # count would be negative, so no row exists
    wt = {"PERIL": S.name_slot("flood damage"), "START_DATE": S.date_slot(D(2026, 1, 10)),
          "W_DAYS": S.count_slot(30, DAYS), "RIDER_DATE": S.date_slot(D(2026, 3, 1))}
    wclause = ("WAIT_CLAUSE", "win.wait_after", {"W": "W_DAYS"})
    refused(_hand(plugin, "waiting", "yn_in_waiting", {**wt, "LOSS_DATE": S.date_slot(D(2026, 3, 1))},
                  {"rider": True, "loss": True}, wclause))           # a loss on the rider date (day zero)
    with pytest.raises(S.SlotError):                                 # between the policy start and the rider date
        _hand(plugin, "waiting", "yn_in_waiting", {**wt, "LOSS_DATE": S.date_slot(D(2026, 2, 20))},
              {"rider": True, "loss": True}, wclause)
    refused(_rolling(plugin, "yn_over", D(2026, 6, 30), [(D(2026, 3, 1), D(2026, 3, 20)),
                                                         (D(2026, 3, 20), D(2026, 4, 2))]), solve=True)  # shared day
    refused(_rolling(plugin, "yn_over", D(2026, 6, 30), [(D(2026, 6, 1), D(2026, 7, 2))]))   # ends after R
    pu = {"VENDOR": S.name_slot("Halden Tools"), "M_WIN": S.count_slot(30, DAYS),
          "REQ_DATE": S.date_slot(D(2026, 5, 30)), "REQ_AMT": S.cents_slot(400000),
          "THRESHOLD": S.cents_slot(700000), "PD_1": S.date_slot(D(2026, 5, 30)), "PA_1": S.cents_slot(300000)}
    refused(_hand(plugin, "purchase", "yn_quotes", pu, {"prior": [["PD_1", "PA_1"]]},
                  ("CMP", "cmp.gt", {"X": "THRESHOLD"})))           # an "earlier" purchase dated on the request day
    edge = _rolling(plugin, "yn_within", D(2026, 6, 30), [(D(2026, 1, 1), D(2026, 1, 30)),
                                                          (D(2026, 3, 1), D(2026, 4, 30))])
    assert _both(plugin, ctx, edge) == 1                             # present == N is within the limit (H8)
    card = plugin.render(edge, ctx).row["instructions"]
    assert "calendar days" in card and "Only one 180-day window is checked" in card


# ------------------------------------------------------------------------------------------------ G2 / G3

def test_solver_a_equals_solver_b_on_5000_specs(plugin, ctx):
    seen, kinds, drops = collections.Counter(), collections.Counter(), 0
    for seed in range(834):
        for smp in SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = _render(plugin, ctx, spec)
            if rr is None:
                drops += 1
                continue
            gold = _check_row(plugin, ctx, spec, rr)
            seen[spec.qform] += 1
            kinds[spec.structure["kind"]] += 1
            for q2, _ in P.COMPLEMENTS.get(spec.qform, ()):
                s2 = spec.replace(qform=q2)
                r2 = plugin.render(s2, ctx, skin=ctx.skin(rr.skin_id), forms=rr.forms)
                assert _check_row(plugin, ctx, s2, r2) == 1 - gold
                seen[q2] += 1
    assert sum(kinds.values()) + drops == 5004 and set(kinds) == set(P.RULES)
    assert drops <= 0.12 * 5004, drops                      # G0 v4 12.2: option sets that cannot share the gold's cues
    assert set(seen) == set(plugin.FROZEN_QFORMS) and min(seen.values()) > 40, seen


def test_every_unit_passes_the_program_gates(plugin, ctx):
    units, kinds, drops = [], collections.Counter(), 0
    for seed in range(150):
        for smp in SAMPLERS:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=(seed < 4))
            if not res.ok and all(g == "render" and (DROP in p or "copies a printed date" in p) for g, p in res.problems):
                drops += 1
                continue
            assert res.ok, (seed, smp, res.problems)
            units.append(res)
            for r in res.rows:
                kinds[r["role"]] += 1
                assert R.validate_row(r) == []
                if smp == "S5":
                    assert r["meta"]["dev_only"]
                else:
                    assert R.validate_row(r, training=True) == [] or r["meta"]["dev_only"]
    rep = pipeline.overlay_report(units, plugin)
    assert 0.45 <= rep["yes_no"] / rep["rows"] <= 0.55, rep
    assert rep["complement_share_of_yes_no"] >= 0.20 and rep["non_syntactic_share_of_pairs"] >= 0.30, rep
    assert 0.20 <= rep["twin_share"] <= 0.25, rep
    assert 0.05 <= rep["equiv_share"] <= 0.10 and rep["attack_share"] == 0, rep
    assert abs(rep["yes_rate"] - 0.5) <= 0.03, rep
    yn = [r for u in units for r in u.rows if r["qtype"] == "noul"]
    bad = sum(plugin.QFORMS[r["meta"]["qform"]].yes_is_bad for r in yn) / len(yn)
    assert 0.45 <= bad <= 0.55, bad                                     # spec 3.0: yes = bad outcome 50 +- 5
    for role in ("complement", "twin", "equiv"):
        assert kinds[role] > 10, kinds
    assert drops <= 0.12 * (len(units) + drops), drops                  # G0 v4 12.2: <= 12% of units (choice only)


def test_ordered_options_carry_no_rank_or_sum_cue(plugin, ctx):
    """Review fix: the gold was the middle of three consecutive days (count_day0 / off_by_one_late) and on ch_total
    the sum of the two other options; "sort, take the second highest" scored 0.73 against chance 0.30. Now the gold's
    sorted rank is target_rank(row key, k) on every emitted row (twins and partners included), the two partial sums
    never share a set, and on independent base rows the rank is uniform per (question form, k)."""
    second = n = sums = sum_gold = 0
    sum_chance = chance = 0.0
    for seed in range(300):
        for smp in TRAINING:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            for rr in (res.rendered if res.ok else []):
                os_ = rr.option_set
                if rr.row["qtype"] != "choice" or os_.meta["kind"] != "open":
                    continue
                keys = sorted(o.key for o in os_.options)
                k, g = len(keys), os_.gold.key
                key = f"T01|{rr.row['meta']['seed']}|{rr.row['meta']['sampler']}|{rr.row['meta']['qform']}"
                assert keys.index(g) == os_.meta["gold_rank"] == DI.target_rank(key, k)
                n += 1
                chance += 1 / k
                second += keys[-2] == g
                for o in os_.options:
                    rest = [x.key for x in os_.options if x is not o]
                    if isinstance(o.key, int) and any(a + b == o.key for i, a in enumerate(rest) for b in rest[i + 1:]):
                        sums += 1
                        sum_gold += o.role == "gold"
                        sum_chance += 1 / k
    assert n > 800 and second / n <= chance / n + 0.04, (second / n, chance / n)
    assert sum_gold <= sum_chance, (sum_gold, sums, sum_chance)        # "sum of two others" no better than chance
    ranks = collections.defaultdict(collections.Counter)                 # independent base rows: one per spec
    for seed in range(2000):
        for smp in TRAINING:
            spec = plugin.sample(seed, smp)
            if plugin.QFORMS[spec.qform].qtype != "choice" or spec.qform == "ch_cash_which":
                continue
            rr = _render(plugin, ctx, spec)
            if rr is not None:
                ranks[(spec.qform, len(rr.option_set.options))][rr.option_set.meta["gold_rank"]] += 1
    pooled = collections.defaultdict(collections.Counter)
    for (q, k), c in ranks.items():
        pooled[k].update(c)
        m = sum(c.values())
        if m >= 200:
            tol = 4 * ((1 / k) * (1 - 1 / k) / m) ** 0.5
            assert max(abs(c[r] / m - 1 / k) for r in range(k)) <= tol, (q, k, c)
    for k, c in pooled.items():
        m = sum(c.values())
        assert m < 1000 or max(abs(c[r] / m - 1 / k) for r in range(k)) <= 0.025, (k, c)


# ------------------------------------------------------------------------------------------------ relations

def test_relations_are_valid(plugin, specs):
    twins, comps, meta = collections.Counter(), 0, 0
    for spec in specs:
        base = plugin.solve_a(spec)
        for prop in plugin.relations(spec):
            if prop.kind == "twin":
                twin = plugin.derive(prop.spec)
                assert slot_diff(spec, twin) == {prop.changed_slot}
                assert twin.structure == spec.structure and twin.qform == spec.qform
                got = plugin.solve_a(twin)
                assert got == prop.expect != base, (spec.seed, spec.sampler, prop.note)
                if plugin.QFORMS[spec.qform].qtype == "noul":
                    assert got == 1 - base
                twins[(spec.structure["kind"], prop.note.split(".")[0])] += 1
            elif prop.kind == "complement":
                partner = spec.replace(qform=prop.qform)
                q, q2 = plugin.QFORMS[spec.qform], plugin.QFORMS[prop.qform]
                assert q.predicate == q2.predicate and q.polarity == -q2.polarity == 1
                assert plugin.solve_a(partner) == 1 - base
                comps += 1
            elif prop.kind == "metamorphic":
                moved = plugin.derive(prop.spec)
                assert plugin.solve_a(moved) == (base if prop.expect == "same" else prop.expect), prop.note
                meta += 1
    # every twin kind of G0 section 6 occurs
    want = {("rolling", "stay_exit"), ("anchor", "filed"), ("anchor", "n_days"), ("waiting", "loss"),
            ("waiting", "w_days"), ("purchase", "request_amount"), ("purchase", "window_edge"),
            ("cash", "cash_in"), ("cash", "cash_out"), ("addon", "method"), ("cutoff", "sent")}
    assert want <= set(twins), sorted(twins)
    assert comps > 200 and meta >= 3 * len(specs)


def test_twins_change_one_slot_in_the_rendered_text(plugin, ctx):
    """G-TW on the text: outside the changed slot (and the printed lines derived from it) the twin row is identical."""
    checked = collections.Counter()
    for seed in range(60):
        for smp in TRAINING:
            spec = plugin.sample(seed, smp)
            if not any(p.kind == "twin" for p in plugin.relations(spec)):
                continue
            res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
            if not res.ok and all(g == "render" and (DROP in p or "copies a printed date" in p) for g, p in res.problems):
                continue                                                    # an option set that cannot be built
            assert res.ok, res.problems
            rows = {r["role"]: r for r in res.rows}
            if "twin" in rows:
                assert rows["twin"]["meta"]["twin_of"] == rows["base"]["id"]
                assert rows["twin"]["call_id"] != rows["base"]["call_id"]
                assert rows["twin"]["gold"] != rows["base"]["gold"]
                checked[spec.structure["kind"]] += 1
    assert set(checked) == set(P.RULES) and sum(checked.values()) > 60, checked


# ------------------------------------------------------------------------------------------------ balance

def test_gold_balance_on_2000_specs(plugin, specs):
    yes = collections.defaultdict(list)
    cash, receipt_after = collections.Counter(), collections.Counter()
    for spec in specs:
        gold = plugin.solve_a(spec)
        if plugin.QFORMS[spec.qform].qtype == "noul":
            assert plugin.QFORMS[spec.qform].polarity == 1                 # bases ask the positive form
            yes[spec.qform].append(gold)
        elif spec.qform == "ch_cash_which":
            cash[gold] += 1
        elif spec.qform == "ch_receipt_day":
            receipt_after[gold != spec.slots["SENT"].value.astimezone(
                spec.derived["CUTOFF"].value.tzinfo).date().isoformat()] += 1
    assert set(yes) == {"yn_over", "yn_timely", "yn_covered", "yn_quotes", "yn_cash_report", "yn_on_time"}
    for q, golds in yes.items():                                         # exact by seed pairs (G0 section 4)
        assert abs(sum(golds) / len(golds) - 0.5) <= 0.02, (q, sum(golds), len(golds))
    n = sum(cash.values())
    for label, share in P.CASH_TARGETS:
        assert abs(cash[label] / n - share) <= 0.12, cash
    assert abs(receipt_after[True] / sum(receipt_after.values()) - 0.5) <= 0.1, receipt_after
    assert sum(s.deep for s in specs) == 0 and all(s.depth <= 2 for s in specs)
    qf = collections.Counter(plugin.QFORMS[s.qform].qtype for s in specs)
    assert 0.38 <= qf["noul"] / len(specs) <= 0.48, qf


def test_trap_shares_on_2000_specs(plugin, specs):
    train = [s for s in specs if s.sampler in TRAINING]
    tags = collections.Counter(t for s in train for t in s.tags)
    assert 0.25 <= tags["boundary"] / len(train) <= 0.40, tags            # spec 3.10: 30% exactly on a boundary
    by_kind = collections.defaultdict(list)
    for s in specs:
        by_kind[s.structure["kind"]].append(s)

    def share(kind, tag):
        return sum(tag in s.tags for s in by_kind[kind]) / len(by_kind[kind])

    floors = {("rolling", "straddle"): 0.4, ("rolling", "calendar_trap"): 0.2, ("rolling", "pre_window_stay"): 0.2,
              ("rolling", "window_edge"): 0.05, ("waiting", "rider_trap"): 0.08, ("purchase", "window_edge"): 0.3,
              ("purchase", "request_alone_trap"): 0.3, ("purchase", "ignore_window_trap"): 0.15,
              ("cash", "netting_trap"): 0.3, ("cash", "other_day_trap"): 0.25, ("addon", "closure_roll"): 0.35,
              ("addon", "double_roll"): 0.08, ("cutoff", "conversion_trap"): 0.1, ("cutoff", "date_crosses"): 0.1}
    for (kind, tag), floor in floors.items():
        assert share(kind, tag) >= floor, (kind, tag, share(kind, tag))
    yn_anchor = [s for s in by_kind["anchor"] if s.structure["filed"]]
    assert sum("earlier_trap" in s.tags for s in yn_anchor) / len(yn_anchor) >= 0.25
    assert share("cutoff", "evening_before") > 0


def test_options_come_from_named_error_models(plugin, ctx, specs):
    positions = collections.defaultdict(collections.Counter)
    for spec in specs:
        if plugin.QFORMS[spec.qform].qtype != "choice":
            continue
        rr = _render(plugin, ctx, spec)
        if rr is None:
            continue
        os_ = rr.option_set
        positions[(os_.meta["kind"], len(os_.options))][os_.gold_index] += 1
        names = set(P.CHOICE_EM[spec.qform])
        for o in os_.options:
            if o.role == "error":
                assert o.err and set(o.err) <= names, (spec.qform, o)
            elif os_.meta["kind"] == "open":
                assert o.role == "gold", o
        if os_.meta["kind"] == "closed":
            assert [o.key for o in os_.options if o.role != "gold"] and len(os_.options) == 4
        assert 2 <= len(os_.options) <= 4
    for (kind, k), c in positions.items():
        m = sum(c.values()) / k
        if m >= 40:
            assert all(abs(c[i] - m) <= 0.4 * m for i in range(k)), (kind, k, c)


def test_rows_fit_the_length_caps(plugin, ctx):
    sizes = []
    for seed in range(150):
        for smp in SAMPLERS:
            rr = _render(plugin, ctx, plugin.sample(seed, smp))
            if rr is not None:
                sizes.append(R.approx_tokens(rr.row))
    assert max(sizes) <= R.MAX_TOKENS and sum(sizes) / len(sizes) <= 800


@pytest.mark.skipif(not TOKENIZER.is_file(), reason="local Qwen tokenizer file not cached")
def test_real_token_mean_is_at_most_800(plugin, ctx):
    from tokenizers import Tokenizer
    tok = Tokenizer.from_file(str(TOKENIZER))

    def n(t):
        return len(tok.encode(t or "", add_special_tokens=False).ids)

    sizes = []
    for seed in range(100):
        for smp in SAMPLERS:
            rr = _render(plugin, ctx, plugin.sample(seed, smp))
            if rr is None:
                continue
            r = rr.row
            sizes.append(n(r["state"]) + 2 * n(r["instructions"]) + sum(n(o) + 2 for o in (r["options"] or [])))
    assert sum(sizes) / len(sizes) <= 800 and max(sizes) <= 2000, (sum(sizes) / len(sizes), max(sizes))


# ------------------------------------------------------------------------------------------------ G-SL

def test_builtin_placeholder_skins_lint_clean(plugin, ctx):
    linted = 0
    for sk in ctx.skins.values():
        if sk.author_mode == "T":
            v = gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                                  name_allow=plugin.NAME_ALLOW)
            assert v == [], (sk.skin_id, v)
        else:
            assert gsl.lint_freeform(sk.text, dict(sk.brief), label_words=plugin.LABEL_WORDS) == []
        linted += 1
    assert linted == len(ctx.skins) >= 40
    label = re.compile(r"\b(?:" + "|".join(re.escape(w) for w in plugin.LABEL_WORDS) + r")\b", re.I)
    for sk in ctx.skins.values():                                       # narrative skins carry no gold label
        if sk.kind == "skin":
            assert not label.search(sk.text), sk.skin_id
    registers = {sk.register for sk in ctx.skins.values() if sk.kind == "skin"}
    assert registers == set(plugin.REGISTERS)
    assert {sk.register for sk in ctx.skins.values() if sk.held_out} == set(plugin.HELD_OUT_REGISTERS)


def test_no_literal_value_or_label_outside_slots(plugin, ctx):
    """Every number, date, time, amount, name and id of a rendered row sits inside a slot span; the program block
    templates carry no digit, month, weekday or gold-label word of their own, and the card text no digit."""
    months = "|".join(S.MONTHS + S.WEEKDAYS)
    label = re.compile(r"\b(?:" + "|".join(re.escape(w) for w in plugin.LABEL_WORDS) + r")\b", re.I)
    for seed in range(120):
        for smp in SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = _render(plugin, ctx, spec)
            if rr is None:
                continue
            values = {str(s.value) for s in spec.all_slots().values() if s.kind in ("name", "id")}
            for fld in ("state", "instructions"):
                text = rr.row[fld]
                spans = sorted((sp.start, sp.end) for sp in rr.spans if sp.field == fld)
                rest, pos = [], 0
                for a, b in spans:
                    if a >= pos:
                        rest.append(text[pos:a])
                        pos = b
                rest.append(text[pos:])
                rest = "\x00".join(rest)
                assert not re.search(r"\d", rest), (seed, smp, fld, rest)
                assert not re.search(rf"\b(?:{months})\b", rest), (seed, smp, fld)
                for v in values:
                    assert not re.search(r"(?<![\w-])" + re.escape(v) + r"(?![\w-])", rest), (v, seed, smp)
            block = plugin.block_template(spec)
            assert not re.search(r"\d", K.PH_RE.sub("", block)) and not label.search(block), block
            card = K.PH_RE.sub("", plugin.rule_template(spec))
            assert not re.search(r"\d", card) and not re.search(rf"\b(?:{months})\b", card)


# ------------------------------------------------------------------------------------------------ determinism

def test_sampling_and_rendering_are_deterministic(plugin, ctx):
    for seed in (0, 7, 31, 202):
        for smp in SAMPLERS:
            a, b = plugin.sample(seed, smp), plugin.sample(seed, smp)
            assert a.structure_hash() == b.structure_hash() and a.tags == b.tags
            ra, rb = _render(plugin, ctx, a), _render(plugin, ctx, b)
            assert (ra is None) == (rb is None) and (ra is None or ra.row == rb.row)
    u1 = pipeline.build_unit(plugin, plugin.sample(17, "S4"), ctx, run_g15=False).rows
    u2 = pipeline.build_unit(plugin, P.T01(lexicon=ctx.lexicon).sample(17, "S4"), ctx, run_g15=False).rows
    assert u1 == u2
    hashes = {plugin.sample(seed, smp).structure_hash() for seed in range(200) for smp in TRAINING}
    assert len(hashes) == 200 * len(TRAINING)


def test_nothing_is_written(plugin, ctx):
    here = Path(__file__).resolve().parent
    before = sorted(p.name for p in here.iterdir())
    pipeline.build_unit(plugin, plugin.sample(3, "S1"), ctx, run_g15=False)
    assert sorted(p.name for p in here.iterdir()) == before
    if not paths.a38_frozen():
        with pytest.raises(paths.DataBeforeFreeze):
            paths.write_jsonl(paths.C2_PARTS / "t01_never.jsonl", [])


# ------------------------------------------------------------------------------------------------ injected bugs

def _failures(plugin, ctx, n=30, samplers=TRAINING):
    out = collections.Counter()
    for seed in range(n):
        for smp in samplers:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            for g, _ in res.problems:
                out[g] += 1
    return out


def test_g2_catches_a_solver_b_exit_day_bug(plugin, ctx, monkeypatch):
    real = B.SOLVERS["rolling"]

    def no_exit_day(view):                                              # B forgets that exit days count
        stays = [[a, (dt.date.fromisoformat(b) - dt.timedelta(days=1)).isoformat(), n] for a, b, n in view["stays"]]
        return real(dict(view, stays=stays))

    monkeypatch.setitem(B.SOLVERS, "rolling", no_exit_day)
    assert _failures(plugin, ctx, samplers=("S1",))["G2"] > 0


def test_g2_catches_a_solver_a_comparator_bug(plugin, ctx, monkeypatch):
    specs = [plugin.sample(seed, "S4") for seed in range(200)]
    specs = [s for s in specs if "boundary" in s.tags and plugin.QFORMS[s.qform].qtype == "noul"]
    assert specs
    real = P._cmp
    monkeypatch.setattr(P, "_cmp", lambda sem, total, bound: real("cmp.ge" if sem == "cmp.gt" else sem, total, bound))
    g2 = sum(g == "G2" for s in specs for g, _ in pipeline.check_rendered(plugin, s, plugin.render(s, ctx), ctx,
                                                                          run_g15=False))
    assert g2 > 0


def test_g2_catches_a_solver_a_anchor_bug(plugin, ctx, monkeypatch):
    real = P.T01._a_anchor
    monkeypatch.setattr(P.T01, "_a_anchor", staticmethod(lambda env, st, mods: real(env, st, mods | {"earlier_anchor"})))
    f = _failures(plugin, ctx, samplers=("S2",))
    assert f["G2"] > 0


def test_g3_catches_a_renderer_that_misprints_the_window(plugin, ctx, monkeypatch):
    real = P.T01.derive

    def shifted(self, spec):
        out = real(self, spec)
        if "WIN_START" in out.derived:
            out.derived["WIN_START"] = S.date_slot(out.derived["WIN_START"].value + dt.timedelta(days=1))
        return out

    monkeypatch.setattr(P.T01, "derive", shifted)
    assert _failures(plugin, ctx, samplers=("S1", "S4"))["G3"] > 0


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    real = P.T01._twin

    def flipped(self, spec):
        t = real(self, spec)
        if t is None or plugin.QFORMS[spec.qform].qtype != "noul":
            return t
        return dataclasses.replace(t, expect=1 - t.expect)

    monkeypatch.setattr(P.T01, "_twin", flipped)
    assert _failures(plugin, ctx)["G-TW"] > 0


def test_gsl_catches_a_leaky_skin(plugin, ctx):
    leaky = dataclasses.replace(ctx.skin("SK-CHAT-1"), skin_id="SK-LEAK",
                                text=ctx.skin("SK-CHAT-1").text + " It already looks late to me.")
    c2 = dataclasses.replace(ctx, skins={**ctx.skins, "SK-LEAK": leaky})
    spec = next(sp for sp in (plugin.sample(seed, "S2") for seed in range(5, 40))
                if plugin.QFORMS[sp.qform].qtype == "noul")
    rr = plugin.render(spec, c2, skin=leaky)
    gates = {g for g, _ in pipeline.check_rendered(plugin, spec, rr, c2, run_g15=False)}
    assert "G-SL" in gates
