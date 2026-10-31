"""c2_build/families/T12/test_plugin.py: in-memory tests for the T12 plugin (C2_DATA_SPEC 3.15, 3.0, 4.1; G0_SPEC.md).

CPU only, in memory: no test writes a file (A37 f: no C2 data before A38); the skins, wordings and lexicon forms are
the Claude-written stand-ins in fixtures.py. Run (from lean/):
  ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T12
Checks:
  contract     validate_plugin(strict=True) == []; solver B shares no code path with solver A
  G2 / G3      solver A == solver B == the construction side, and parse(row) == canonical facts, on 5,000 sampled
               specs (1,000 per sampler), with G-SL, G-LEX and the row schema on every row
  hand cases   hand-computed golds (exact tolerance, check order, wrong base, look-alike register number, limit at
               the boundary, over-billing, lower price) through solver A and through render -> parse -> solver B
  pipeline     relation units through G2, G3, G4, G-SL, G-LEX, G-TW and schema (G15 on a sample); overlay shares,
               yes = bad outcome, negation quotas, unit size, length cap
  relations    twins differ in exactly one input slot and the gold flips exactly as predicted; complements are
               opposite for every declared partner; metamorphic predictions hold
  balance      2,000 training specs: question-form shares, action shares per card, yes rate, per-card yes rates,
               trap shares, deep share, gold position, decisive-check position, visible-feature cues
  G-SL         the built-in placeholder skins carry no gold-label word and no literal value outside their slots
  determinism  the same seed gives the same spec and rows, also in a fresh process with another hash seed
  bugs         injected bugs in solver B, solver A, the option texts, the card text, a twin prediction and a G4
               prediction are caught by the gates
"""
from __future__ import annotations

import collections
import dataclasses
import json
import os
import random
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pytest  # noqa: E402

from c2_kit import gsl, pipeline  # noqa: E402
from c2_kit.cards import split_rules  # noqa: E402
from c2_kit import paths  # noqa: E402,F401  (negcount on sys.path)
from c2_kit import plugin as KP  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit import rules as RL  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from families.T12 import fixtures as FX  # noqa: E402
from families.T12 import plugin as P  # noqa: E402
from families.T12 import solver_b as B  # noqa: E402
import negcount  # noqa: E402

TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T12Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def train_specs(plugin):
    return [plugin.sample(seed, smp) for seed in range(500) for smp in TRAIN]


def _verdict(plugin, spec):
    return plugin._judge(spec)[0]


# ------------------------------------------------------------------------------------------------ contract

def test_plugin_meets_the_strict_contract(plugin):
    assert KP.validate_plugin(plugin, strict=True) == []
    assert KP.check_independence(plugin) == []
    assert plugin.PARADIGM_A != plugin.PARADIGM_B
    assert len(Path(plugin.G0_LITE).read_text(encoding="utf-8").splitlines()) <= 200


def test_solver_b_imports_nothing_from_solver_a():
    src = Path(B.__file__).read_text(encoding="utf-8")
    assert "families.T12.plugin" not in src and "from . import plugin" not in src
    assert "c2_kit.rules" not in src and "glob_a" not in src and "decimal" not in src.lower().split("\"\"\"")[-1]


# ------------------------------------------------------------------------------------------------ G2 / G3 on 5,000

def test_solver_a_equals_solver_b_on_5000_specs(plugin, ctx):
    n, golds, problems = 0, collections.Counter(), []
    for seed in range(1000):
        for smp in plugin.SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            gold = plugin.solve_a(spec)
            verdict, pf, _ = plugin._judge(spec)                       # the construction side (third implementation)
            if gold != P._answer(spec.qform, verdict, pf, plugin._items(spec)):
                problems.append((seed, smp, "construction"))
            view = B.parse(rr.row, ctx)
            facts = {k: v for k, v in view.items() if k != "options"}
            if facts != plugin.canonical_for(spec, rr.row["meta"]["c2"]["author_mode"]):
                problems.append((seed, smp, "G3"))
            b = B.solve_b(view)
            if b != gold or rr.answer != gold:
                problems.append((seed, smp, "G2", gold, b))
            if rr.row["qtype"] == "choice" and view["options"][rr.row["options"].index(rr.row["gold"])] != gold:
                problems.append((seed, smp, "option key"))
            for gate, detail in pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False):
                problems.append((seed, smp, gate, detail))
            n += 1
            golds[(spec.qform, gold if spec.qform == "ch_action" else "-")] += 1
    assert n == 5000
    assert problems == []
    for v in P.VERDICTS:                                               # every action is exercised as gold
        assert golds[("ch_action", v)] > 100, v


# ------------------------------------------------------------------------------------------------ hand cases

def _hand_spec(plugin, qform, lines, *, checks=("qty", "price"), pct=2, tol_amt=None, tol_cmp="cmp.le",
               reg=None, inv_no="INV-55182", limit=None, limit_cmp="cmp.le", style="numbered", doc_fmt="kv",
               display=None):
    """A spec built from explicit values (lines: (item, unit, po_q, po_p, rcv_q, inv_q, inv_p)); golds below are
    computed by hand from G0_SPEC.md, not by any solver."""
    card = {"id": "T12:S1:c00", "pack": P.PACKS[0], "tol_kind": "abs" if tol_amt else "pct", "doc_fmt": doc_fmt,
            "rule_fmt": "list", "blocks": "narrative_first"}
    st = {"n": len(lines), "checks": list(checks), "display": list(display or checks), "style": style,
          "doc_fmt": doc_fmt,
          "blocks": "narrative_first", "tol_kind": card["tol_kind"], "codes": None, "card_style": "full"}
    vals = {"items": [(x[0], x[1]) for x in lines], "po_q": [x[2] for x in lines], "po_p": [x[3] for x in lines],
            "rcv_q": [x[4] for x in lines], "inv_q": [x[5] for x in lines], "inv_p": [x[6] for x in lines],
            "tol": tol_amt or pct, "inv_no": inv_no, "reg": reg, "limit": limit,
            "vendor": "Corran Supply",
            "approver": "Mira Castell", "clerk": "Dana Okafor", "dept": "lab", "po_no": "PO-7731", "gr_no": "GR-2209"}
    return plugin._assemble(7, "S1", qform, card, st, vals, None if tol_amt else pct,
                            {"tol": tol_cmp, "limit": limit_cmp}, random.Random(0))


HAND = (   # (name, spec kwargs, ch_action gold, ch_price_line gold, yn_within_tol gold)
    ("received short, billed in full (ranking example)",
     dict(lines=[("nitrile gloves", "case", 40, 1250, 38, 40, 1250)]), "hold", "none", 1),
    ("exactly at a 2% tolerance, inclusive",
     dict(lines=[("nitrile gloves", "case", 40, 1250, 40, 40, 1275)]), "release", "none", 1),
    ("exactly at a 2% tolerance, strict",
     dict(lines=[("nitrile gloves", "case", 40, 1250, 40, 40, 1275)], tol_cmp="cmp.lt"), "review", "nitrile gloves",
     0),
    ("one cent over on the PO base (the invoice-price base would pass)",
     dict(lines=[("lab coats", "unit", 10, 5000, 10, 10, 5101)]), "review", "lab coats", 0),
    ("both fail, quantity first",
     dict(lines=[("pipette tips", "box", 20, 2000, 18, 20, 2000), ("lab coats", "unit", 5, 4000, 5, 5, 4200)]),
     "hold", "lab coats", 0),
    ("both fail, price first",
     dict(lines=[("pipette tips", "box", 20, 2000, 18, 20, 2000), ("lab coats", "unit", 5, 4000, 5, 5, 4200)],
          checks=("price", "qty")), "review", "lab coats", 0),
    ("absolute tolerance, lower price far below (passes)",
     dict(lines=[("ethanol", "drum", 3, 20000, 3, 3, 15000)], tol_amt=50), "release", "none", 1),
    ("absolute tolerance, 51 cents over a 50-cent tolerance",
     dict(lines=[("ethanol", "drum", 3, 20000, 3, 3, 20051)], tol_amt=50), "review", "ethanol", 0),
    ("over-billed above the ordered quantity",
     dict(lines=[("bench paper", "roll", 40, 1500, 40, 42, 1500)]), "hold", "none", 1),
    ("shortfall billed at what was received",
     dict(lines=[("bench paper", "roll", 40, 1500, 37, 37, 1500)]), "release", "none", 1),
    ("look-alike register number is not a duplicate",
     dict(lines=[("sample vials", "pack", 10, 900, 10, 10, 900)], checks=("dup", "qty", "price"),
          reg=["INV-55128", "INV-40031"]), "release", "none", 1),
    ("exact register number is a duplicate",
     dict(lines=[("sample vials", "pack", 10, 900, 10, 10, 900)], checks=("dup", "qty", "price"),
          reg=["INV-55128", "INV-55182"]), "reject", "none", 1),
    ("invoice total equal to the limit, inclusive",
     dict(lines=[("sample vials", "pack", 10, 900, 10, 10, 900)], checks=("limit", "qty", "price"), limit=9000),
     "release", "none", 1),
    ("invoice total equal to the limit, strict",
     dict(lines=[("sample vials", "pack", 10, 900, 10, 10, 900)], checks=("limit", "qty", "price"), limit=9000,
          limit_cmp="cmp.lt"), "escalate", "none", 1),
    ("totals equal but a line is over tolerance",
     dict(lines=[("pipette tips", "box", 10, 2000, 10, 10, 2100), ("lab coats", "unit", 10, 4000, 10, 10, 3900)]),
     "review", "pipette tips", 0),
    ("partial shortfall billed above the receipt, below the order (H8)",
     dict(lines=[("bench paper", "roll", 10, 1500, 8, 9, 1500)]), "hold", "none", 1),
    ("the absolute bound is per unit of price, never times the quantity (H11)",
     dict(lines=[("ethanol", "drum", 10, 20000, 10, 10, 20040)], tol_amt=50), "release", "none", 1),
    ("a price far below the PO passes under a strict comparator too (H14)",
     dict(lines=[("ethanol", "drum", 3, 20000, 3, 3, 12000)], tol_amt=50, tol_cmp="cmp.lt"), "release", "none", 1),
    ("two checks fail: the check order decides, not the listed order (H1, H2)",
     dict(lines=[("pipette tips", "box", 20, 2000, 18, 20, 2000)], checks=("limit", "qty", "price"), limit=30000,
          limit_cmp="cmp.lt", style="bulleted", display=("qty", "price", "limit")), "escalate", "none", 1),
)


@pytest.mark.parametrize("case", HAND, ids=[c[0] for c in HAND])
def test_hand_computed_golds(plugin, ctx, case):
    _, kw, action, line, within = case
    released = int(action == "release")
    for qform, want in (("ch_action", action), ("ch_price_line", line), ("yn_within_tol", within),
                        ("yn_over_tol", 1 - within), ("yn_release", released), ("yn_dneg_release", released),
                        ("yn_payment_stopped", 1 - released), ("yn_price_review", int(action == "review"))):
        spec = _hand_spec(plugin, qform, **kw)
        assert plugin.solve_a(spec) == want, (qform, plugin.solve_a(spec), want)
        rr = plugin.render(spec, ctx)
        view = B.parse(rr.row, ctx)
        assert B.solve_b(view) == want
        assert pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False) == []
    spec = _hand_spec(plugin, "ch_action", **kw)
    if spec.env()["INV_TOTAL"] == spec.env()["PO_TOTAL"] and action != "release":      # the totals trap bites here
        assert "t12_totals_only" in plugin.render(spec, ctx).option_set.opt_err["Release for payment"]


def test_decimal_and_integer_paths_agree_on_percent_boundaries(plugin):
    """Solver A's Decimal tolerance equals the integer tolerance at every percent and price step (G0 R5)."""
    for pct in P.PCTS + P.PCTS_S5:
        step = 100 // __import__("math").gcd(pct, 100)
        for po in range(step, 20000, step * 7):
            t = po * pct // 100
            assert Decimal(po) / 100 * Decimal(pct) / 100 == Decimal(t) / 100
            assert RL.FNS["t12_pct_of"](Decimal(po) / 100, pct) == Decimal(t) / 100


def test_resolved_haiku_points_hold_on_sampled_rows(plugin, ctx):
    """G0 v2 section 5: the card prints the deciding check order (H1); numbered lists follow it and first_failure_only
    exists only where the listed order differs (H2); S5 percent and absolute values are disjoint from training (H6);
    shortfalls are clamped (H9); answer codes are row-level on ch_action (H22); the precedence decoys include the
    listed-order reading (H30)."""
    assert not set(P.PCTS) & set(P.PCTS_S5) and not set(P.TOL_ABS) & set(P.TOL_ABS_S5)
    n_listed_differs = 0
    for seed in range(150):
        for smp in plugin.SAMPLERS:
            spec = plugin.sample(seed, smp)
            st, v = spec.structure, spec.env()
            card = split_rules(plugin.render(spec, ctx).row)[0].split("\n")
            order_line = next(x for x in card if x.startswith("Check order: "))
            assert order_line == "Check order: " + ", then ".join(P.CHECK_NAME[c] for c in st["checks"]) + "."
            if st["style"] == "numbered":
                assert st["display"] == st["checks"]
            assert (plugin._judge(spec, "first_failure_only") is None) == (st["display"] == st["checks"])
            n_listed_differs += st["display"] != st["checks"]
            if st["tol_kind"] == "pct":
                assert v["TOL_PCT"] in (P.PCTS_S5 if smp == "S5" else P.PCTS)
            else:
                assert v["TOL_AMT"] in (P.TOL_ABS_S5 if smp == "S5" else P.TOL_ABS)
            for x in plugin._lines(spec):
                assert x["rcv"] >= 1 and 0 <= x["po_q"] - x["rcv"] <= 3
            assert st["codes"] is None or spec.qform == "ch_action"
    assert n_listed_differs > 100
    assert "prec.t12.first_listed" in ctx.lexicon.sems
    for f in ctx.lexicon.forms.values():
        if f.kind == "precedence":
            assert "check order" in f.text and "listed" not in f.text


# ------------------------------------------------------------------------------------------------ pipeline

def test_relation_units_pass_every_gate(plugin, ctx):
    units, bad = [], []
    for seed in range(200):
        for smp in plugin.SAMPLERS:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=seed < 3)
            (units if res.ok else bad).append(res if res.ok else (seed, smp, res.problems[:3]))
            if res.ok and smp == "S5":
                assert all(r["meta"]["dev_only"] for r in res.rows)
                assert all(R.validate_row(r, training=True) for r in res.rows)
    assert bad == []
    train = [u for u in units if not u.rows[0]["meta"]["dev_only"]]
    rep = pipeline.overlay_report(train, plugin)
    rows = [r for u in train for r in u.rows]
    yn = [r for r in rows if r["qtype"] == "noul"]
    assert rep["complement_share_of_yes_no"] >= 0.20 and rep["non_syntactic_share_of_pairs"] >= 0.30
    assert 0.20 <= rep["twin_share"] <= 0.25
    assert 0.05 <= rep["equiv_share"] <= 0.10
    assert 0.02 <= rep["attack_share"] <= 0.06
    assert rep["abstain"]["rows_showing"] == 0                          # T12 has no abstain option (G0 R20)
    assert 0.45 <= len(yn) / len(rows) <= 0.55                         # spec 3.0: yes/no 45-55% of the family
    assert abs(sum(r["gold"] for r in yn) / len(yn) - 0.5) <= 0.03
    bad_share = sum(bool(plugin.QFORMS[r["meta"]["qform"]].yes_is_bad) for r in yn) / len(yn)
    assert abs(bad_share - 0.5) <= 0.05                                # spec 3.0: yes = bad outcome 50 +- 5
    k_syn = [negcount.count(r["instructions"].rsplit("\n\n", 1)[-1]).k_syn for r in yn]
    assert sum(k >= 1 for k in k_syn) / len(k_syn) >= 0.10            # spec 3.0 syntactic negation
    assert sum(k >= 2 for k in k_syn) / len(k_syn) >= 0.02            # spec 3.0 double negation
    assert max(collections.Counter(r["call_id"] for r in rows).values()) <= 3
    toks = [R.approx_tokens(r) for r in rows]
    assert max(toks) <= R.MAX_TOKENS and sum(toks) / len(toks) <= 1000   # conservative 3 chars / token


# ------------------------------------------------------------------------------------------------ relations

def test_twins_flip_exactly_as_predicted_and_complements_are_opposite(plugin, train_specs):
    n_twin = n_comp = n_meta = 0
    changed = collections.Counter()
    for spec in train_specs:
        base = plugin.solve_a(spec)
        for prop in plugin.relations(spec):
            if prop.kind == "twin":
                twin = plugin.derive(prop.spec)
                assert slot_diff(spec, twin) == {prop.changed_slot}
                assert plugin.solve_a(twin) == prop.expect != base
                changed[prop.changed_slot.rsplit("_", 1)[0] if prop.changed_slot[-1].isdigit() else
                        prop.changed_slot] += 1
                n_twin += 1
            elif prop.kind == "complement":
                partner = plugin.QFORMS[prop.qform]
                assert partner.predicate == plugin.QFORMS[spec.qform].predicate
                assert partner.polarity == -plugin.QFORMS[spec.qform].polarity
                assert base + plugin.solve_a(spec.replace(qform=prop.qform)) == 1
                n_comp += 1
            elif prop.kind == "metamorphic":
                assert plugin.solve_a(plugin.derive(prop.spec)) == (base if prop.expect == "same" else prop.expect)
                n_meta += 1
        if spec.qform in P.COMPLEMENTS:                       # every declared complement form, not only the drawn one
            for q2, _ in P.COMPLEMENTS[spec.qform]:
                assert base + plugin.solve_a(spec.replace(qform=q2)) == 1
    assert n_twin > 500 and n_comp > 150 and n_meta > 8000
    assert {"RCV_Q", "INV_P", "REG", "LIMIT", "INV_Q"} <= set(changed), changed   # twins move every check's slot


# ------------------------------------------------------------------------------------------------ balance

def test_label_balance_on_2000_specs(plugin, ctx, train_specs):
    specs = train_specs
    assert len(specs) == 2000
    q = collections.Counter(s.qform for s in specs)
    for form, share in P.QFORM_SHARES:
        assert abs(q[form] / len(specs) - share) <= 0.03, form
    act = [s for s in specs if s.qform == "ch_action"]
    got = collections.Counter(plugin.solve_a(s) for s in act)
    want = collections.Counter()
    for s in act:                                             # gold uniform over each card's own actions (G0 R15)
        vs = P._verdicts(s.structure["checks"])
        for v in vs:
            want[v] += 1 / len(vs)
    for v in P.VERDICTS:
        assert abs(got[v] - want[v]) / len(act) <= 0.04, (v, got[v], round(want[v]))
    yn = [s for s in specs if s.qform.startswith("yn_")]
    assert abs(sum(plugin.solve_a(s) for s in yn) / len(yn) - 0.5) <= 0.03
    for form in ("yn_release", "yn_within_tol", "yn_price_review"):
        xs = [s for s in yn if s.qform == form]
        assert abs(sum(plugin.solve_a(s) for s in xs) / len(xs) - 0.5) <= 0.08, form
    rates = [P._rate(smp, i, P.N_CARDS) for smp in TRAIN for i in range(P.N_CARDS)]
    assert min(rates) >= 0.2 and max(rates) <= 0.8 and abs(sum(rates) / len(rates) - 0.5) < 1e-9
    pl = [s for s in specs if s.qform == "ch_price_line"]
    for n in (1, 2, 3, 4):                                    # G0 v2.2 R16: "none" is gold 1 / (n + 1) of the time
        xs = [s for s in pl if s.structure["n"] == n]
        if len(xs) >= 100:
            assert abs(sum(plugin.solve_a(s) == P.NONE_LINE for s in xs) / len(xs) - 1 / (n + 1)) <= 0.08, n
    tags = collections.Counter(t for s in specs for t in s.tags)
    share = {k: v / len(specs) for k, v in tags.items()}
    bands = {"totals_match_lines_differ": (0.18, 0.32), "two_fail": (0.15, 0.25), "at_tolerance": (0.15, 0.27),
             "wrong_base_trap": (0.10, 0.45), "display_order_trap": (0.02, 0.12), "near_miss_duplicate": (0.10, 0.35),
             "shortfall_billed_ok": (0.25, 0.60), "limit_at_boundary": (0.03, 0.15)}
    for k, (lo, hi) in bands.items():
        assert lo <= share.get(k, 0) <= hi, (k, share.get(k))
    assert sum(s.deep for s in specs) == 0 and {s.depth for s in specs} == {1, 2}
    assert abs(sum(s.structure["tol_kind"] == "abs" for s in specs) / len(specs) - 0.5) <= 0.06
    pos = collections.defaultdict(collections.Counter)
    for s in act:
        rr = plugin.render(s, ctx)
        pos[len(rr.row["options"])][rr.option_set.gold_index] += 1
    for k, c in pos.items():
        tot = sum(c.values())
        if tot >= 100:
            assert all(abs(c[i] / tot - 1 / k) <= 0.08 for i in range(k)), (k, c)


def test_card_and_documents_carry_no_label_shortcut(plugin):
    """Card features (number of checks, tolerance kind, comparators, style, decisive position) and the trap plans
    do not move the action off its prior, and the visible document features are mitigated by traps (round-1
    lesson 4; a G6 / G7 pre-check on 4,000 training specs)."""
    specs = [plugin.sample(seed, smp) for seed in range(1000) for smp in TRAIN]
    act = [s for s in specs if s.qform == "ch_action"]
    tested = 0
    groups = collections.defaultdict(list)
    for s in act:
        st, v = s.structure, s.env()
        k = len(st["checks"])
        groups[("k", k)].append(s)
        groups[("tol", st["tol_kind"], k)].append(s)
        groups[("tol_cmp", v["TOL_CMP"], k)].append(s)
        groups[("style", st["style"], k)].append(s)
        groups[("lines", st["n"], k)].append(s)
    for key, xs in groups.items():
        if len(xs) < 150:
            continue
        k = key[-1]
        p0 = 1 / (k + 1)
        rate = sum(_verdict(plugin, s) == "release" for s in xs) / len(xs)
        se = (p0 * (1 - p0) / len(xs)) ** 0.5
        assert abs(rate - p0) <= 4 * se, (key, round(rate, 3), round(p0, 3))
        tested += 1
    assert tested >= 12
    first = collections.Counter(s.structure["checks"].index(P.CHECK_OF[_verdict(plugin, s)]) for s in act
                                if _verdict(plugin, s) != "release")
    tot = sum(first.values())                                 # the deciding check's position is spread out
    assert all(first[i] / tot >= 0.15 for i in range(3)), first
    by_v = collections.defaultdict(list)
    for s in specs:
        e, lines = s.env(), plugin._lines(s)
        by_v[_verdict(plugin, s)].append((e["INV_TOTAL"] == e["PO_TOTAL"], any(x["rcv"] < x["po_q"] for x in lines),
                                          any(x["inv_p"] > x["po_p"] for x in lines)))
    allv = [x for xs in by_v.values() for x in xs]
    match = sum(x[0] for x in allv) / len(allv)
    for v, xs in by_v.items():
        assert abs(sum(x[0] for x in xs) / len(xs) - match) <= 0.10, v       # totals match: label-blind plan
    for v, xs in by_v.items():
        if v != "hold":
            assert sum(x[1] for x in xs) / len(xs) >= 0.45, v                 # shortfalls on non-hold rows too
        if v != "review":
            assert sum(x[2] for x in xs) / len(xs) >= 0.50, v                 # price increases on non-review rows
    assert sum(x[1] for x in by_v["hold"]) / len(by_v["hold"]) <= 0.95         # over-billing without a shortfall


# ------------------------------------------------------------------------------------------------ G-SL

def test_builtin_skins_pass_gsl_and_hold_no_label_word_or_value(plugin, ctx):
    label_forms = gsl._label_forms(plugin.LABEL_WORDS)
    for sk in ctx.skins.values():
        if sk.author_mode == "F":
            assert gsl.lint_freeform(sk.text, dict(sk.brief), label_words=plugin.LABEL_WORDS) == [], sk.skin_id
            continue
        assert gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                                 name_allow=plugin.NAME_ALLOW) == [], sk.skin_id
        lit = gsl._literal(sk.text).lower()
        if sk.kind in ("skin", "attack"):
            assert not any(ch.isdigit() for ch in lit), sk.skin_id
            assert not any(sym in lit for sym in "$€£%"), sk.skin_id
        if sk.kind == "skin":
            assert not set(gsl._WORD.findall(lit)) & label_forms, sk.skin_id
            assert {"CLERK", "DEPT"} <= set(sk.decl), sk.skin_id
            assert not sk.text.startswith(("Invoice ", "Purchase order ", "Goods receipt ", "Paid-invoice")), sk.skin_id
    leaky = dataclasses.replace(ctx.skin("SK-CHAT-1"), skin_id="SK-LEAK",
                                text=ctx.skin("SK-CHAT-1").text + ", please release it, no hold needed")
    found = {v.rule for v in gsl.lint_template(leaky, label_words=plugin.LABEL_WORDS, name_allow=plugin.NAME_ALLOW)}
    assert {"gold_label", "negation"} <= found
    numbered = dataclasses.replace(ctx.skin("SK-MEMO-1"), skin_id="SK-NUM", text="Note from {CLERK} for the {DEPT} "
                                   "team: invoice {INVOICE_ID} is for 40 cases at $12.50, due tomorrow.")
    found = {v.rule for v in gsl.lint_template(numbered, label_words=plugin.LABEL_WORDS)}
    assert {"number", "relative_time"} <= found


def test_lexicon_forms_are_admitted_and_wordings_have_fixed_negation_counts(ctx):
    assert all(f.unit_ok for f in ctx.lexicon.forms.values())
    assert ctx.lexicon.gate()["pass"]
    want = {"yn_dneg_release": (2, 2), "yn_not_release": (1, 1)}             # every other wording: 0 / 0
    for sk in ctx.skins.values():
        if sk.kind == "wording" and sk.qform.startswith("yn_"):
            c = negcount.count(sk.text)
            assert (c.k_all, c.k_syn) == want.get(sk.qform, (0, 0)), (sk.skin_id, c.k_all, c.k_syn)


# ------------------------------------------------------------------------------------------------ determinism

def test_generation_is_deterministic(plugin, ctx):
    fresh_ctx = FX.ctx()
    fresh = P.T12Plugin(lexicon=fresh_ctx.lexicon)
    for seed in (0, 7, 31, 99):
        for smp in plugin.SAMPLERS:
            a, b = plugin.sample(seed, smp), fresh.sample(seed, smp)
            assert a.structure_hash() == b.structure_hash() and a.tags == b.tags
            ra = pipeline.build_unit(plugin, a, ctx, run_g15=False).rows
            rb = pipeline.build_unit(fresh, b, fresh_ctx, run_g15=False).rows
            assert ra == rb
    assert plugin.sample(5, "S1").structure_hash() != plugin.sample(6, "S1").structure_hash()
    assert plugin.sample(5, "S1").structure_hash() != plugin.sample(5, "S2").structure_hash()


_PROBE = """
import sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, %r)
from families.T12 import plugin as P, fixtures as FX
c = FX.ctx(); p = P.T12Plugin(lexicon=c.lexicon)
out = []
for s in range(40):
    for smp in p.SAMPLERS:
        sp = p.sample(s, smp)
        out.append([sp.structure_hash(), p.render(sp, c).row["id"]])
print(json.dumps(out))
"""


def test_determinism_across_processes_and_hash_seeds():
    outs = []
    for hs in ("1", "2"):
        env = {**os.environ, "PYTHONHASHSEED": hs, "PYTHONDONTWRITEBYTECODE": "1"}
        res = subprocess.run([sys.executable, "-c", _PROBE % str(C2_BUILD)], capture_output=True, text=True, env=env,
                             timeout=300, check=True)
        outs.append(json.loads(res.stdout))
    assert outs[0] == outs[1]


# ------------------------------------------------------------------------------------------------ injected bugs

def _gate_failures(plugin, ctx, n=60, samplers=("S1", "S2", "S3", "S4")):
    out = collections.Counter()
    for seed in range(n):
        for smp in samplers:
            try:
                spec = plugin.sample(seed, smp)
            except KP.ContractError:
                out["sample"] += 1
                continue
            res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
            for g, _ in res.problems:
                out[g] += 1
    return out


def test_g2_catches_a_solver_b_boundary_bug(plugin, ctx, monkeypatch):
    real = B.solve_b

    def strict_as_inclusive(view):                            # "less than" read as "at most" in solver B
        return real({**view, "tol_cmp": "cmp.le", "limit_cmp": "cmp.le" if view["limit_cmp"] else None})

    monkeypatch.setattr(B, "solve_b", strict_as_inclusive)
    assert _gate_failures(plugin, ctx)["G2"] > 0


def test_a_solver_a_tolerance_base_bug_is_caught(plugin, ctx, monkeypatch):
    monkeypatch.setitem(RL.FNS, "t12_pct_of", lambda price, pct: (price + Decimal("0.01")) * Decimal(pct) / 100)
    f = _gate_failures(plugin, ctx)
    assert f["sample"] + f["G2"] > 0


def test_g2_catches_mislabelled_option_texts(plugin, ctx, monkeypatch):
    monkeypatch.setitem(P.OPTION_TEXT, "hold", "Send to price-variance review")
    monkeypatch.setitem(P.OPTION_TEXT, "review", "Hold for receipt")
    assert _gate_failures(plugin, ctx)["G2"] > 0


def test_g3_catches_a_card_that_prints_the_wrong_check_order(plugin, ctx, monkeypatch):
    monkeypatch.setitem(P.CHECK_NAME, "qty", "price")
    monkeypatch.setitem(P.CHECK_NAME, "price", "quantity")
    assert _gate_failures(plugin, ctx)["G3"] > 0


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    real = P.T12Plugin._twin

    def wrong(self, spec):
        prop = real(self, spec)
        if prop is not None and spec.qform.startswith("yn_"):
            prop = dataclasses.replace(prop, expect=1 - prop.expect)
        return prop

    monkeypatch.setattr(P.T12Plugin, "_twin", wrong)
    assert _gate_failures(plugin, ctx)["G-TW"] > 0


def test_g4_catches_a_wrong_metamorphic_prediction(plugin, ctx, monkeypatch):
    real = P.T12Plugin._metamorphic

    def wrong(self, spec):
        out = real(self, spec)
        rev = out[-1]                                          # "reverse the check order": claim nothing changes
        return out[:-1] + [dataclasses.replace(rev, expect="same")]

    monkeypatch.setattr(P.T12Plugin, "_metamorphic", wrong)
    assert _gate_failures(plugin, ctx)["G4"] > 0
