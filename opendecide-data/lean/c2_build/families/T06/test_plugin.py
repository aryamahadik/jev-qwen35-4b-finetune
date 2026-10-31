"""families/T06/test_plugin.py: in-memory tests for the T06 plugin (A37 f: no test writes a file; rows live in memory).

Covers the task's bars: solver A == solver B (and the G3 parse) on >= 5,000 sampled specs; hand-computed golds across
month ends, leap days and every rule; relation units through every program gate (G2, G3, G4, G-SL, G-LEX, G-TW,
schema, and G15 on a few); minimal-edit twins differ in one slot and flip exactly as constructed; complements are
opposite; gold balance within its bands on 2,000 specs (per question form on 12,000); G-SL on the built-in placeholder
skins (no gold-label word or literal value outside slots); determinism by seed (also across hash seeds); error-model
distractors; and injected bugs that the gates must catch.

Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T06
"""
from __future__ import annotations

import collections
import dataclasses
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import brute, gsl, pipeline  # noqa: E402
from c2_kit import cards as CD  # noqa: E402
from c2_kit.paths import COMMON  # noqa: E402  (puts c_src/common on sys.path)
from c2_kit import plugin as P  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.distractors import CATALOG, check_named, position_counts  # noqa: E402
from c2_kit.plugin import KitCtx, Spec  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from families.T06 import fixtures as FX  # noqa: E402
from families.T06 import plugin as T  # noqa: E402
from families.T06 import solver_b as B  # noqa: E402

import negcount  # noqa: E402  (c_src/common, read-only)

assert COMMON.is_dir()

TRAIN = ("S1", "S2", "S3", "S4")
YN = tuple(q for q, f in T.T06Plugin.QFORMS.items() if f.qtype == "noul")
D = dt.date


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return T.T06Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs2000(plugin):
    return [plugin.sample(seed, smp) for seed in range(500) for smp in TRAIN]


def _refund(spec) -> bool:
    return bool(T._grants(T.facts(spec)))


def _b(plugin, ctx, spec):
    rr = plugin.render(spec, ctx)
    return plugin.solve_b(plugin.parse(rr.row, ctx)), rr


# ------------------------------------------------------------------------------------------------ contract

def test_plugin_meets_the_strict_contract(plugin):
    assert P.validate_plugin(plugin, strict=True) == []
    assert P.check_independence(plugin) == []
    assert plugin.PARADIGM_A == "decision_table" and plugin.PARADIGM_B == "day_bitmap"
    assert len(T.HERE.joinpath("G0_SPEC_v4.md").read_text(encoding="utf-8").splitlines()) <= 200
    assert Path(plugin.G0_LITE).name == "G0_SPEC_v4.md" and plugin.G0_SHA256 != plugin.G0_SHA256_AUTHORED
    src = Path(B.__file__).read_text(encoding="utf-8")
    assert "families.T06.plugin" not in src and "from . import plugin" not in src


def test_g0_card_texts_are_the_cards_both_solvers_read():
    """Section 2 of the frozen G0 v3 holds the card texts verbatim (full, compact, short); plugin and solver B carry
    exactly those texts. The full cards are the frozen G0 v2 cards, unchanged."""
    g0 = T.HERE.joinpath("G0_SPEC_v4.md").read_text(encoding="utf-8")
    sec = g0.split("## 2. Card texts", 1)[1].split("## 3.", 1)[0]
    blocks = sec.split("```")[1::2]
    assert len(blocks) == 3
    got = {}
    for var, block in zip(("full", "compact", "short"), blocks):
        cur = None
        styles = {}
        for ln in block.strip("\n").split("\n"):
            m = re.match(r"(act|code|charter|regulation(?: \(S5 only\))?): (.*)", ln)
            if m:
                cur = m.group(1).split()[0]
                styles[cur] = [m.group(2)]
            else:
                styles[cur].append(ln)
        for st, lines in styles.items():
            got[(st, var)] = "\n".join(lines)
    assert set(got) == set(T.CARD_TEXT) == set(B.CARDS)
    for key, text in got.items():
        assert text == T.CARD_TEXT[key] == B.CARDS[key], key
    v2 = T.HERE.joinpath("G0_SPEC.md").read_text(encoding="utf-8")
    v2block = v2.split("## 2. Card texts", 1)[1].split("```", 2)[1].strip("\n").split("\n")
    v2styles, cur = {}, None
    for ln in v2block:
        m = re.match(r"(act|code|charter|regulation(?: \(S5 only\))?): (.*)", ln)
        if m:
            cur = m.group(1).split()[0]
            v2styles[cur] = [m.group(2)]
        else:
            v2styles[cur].append(ln)
    assert {st: "\n".join(v) for st, v in v2styles.items()} == T.STYLE_TEXT       # full == the frozen v2 cards
    assert T.CLOSED_WORLD == B.CLOSED and T.CLOSED_WORLD in g0
    assert {st: {v: k for k, v in t.items()} for st, t in T.OPTION_TEXT.items()} == B.OPTION_KEY
    for st, texts in T.OPTION_TEXT.items():
        for text in texts.values():
            assert " ".join(text.split()) in " ".join(g0.split()), (st, text)


def test_card_variants_keep_every_rule():
    """c2_kit.cards: compact and short change no slot, quoted literal, number, operator word or negation count."""
    for st in T.TRAIN_STYLES:
        spec = CD.CardSpec("T06", tuple(CD.CardItem(f"{st}{i}", *it) for i, it in enumerate(T.CARD_ITEMS[st])),
                           numbered=False)
        assert spec.problems() == [], (st, spec.problems())


def test_closed_vocabularies_are_clean(ctx):
    for pool in (T.CUSTOMERS, T.STORES, T.JURIS, T.JURIS_HELD, *T.ITEMS.values()):
        assert len(set(pool)) == len(pool)
        for nm in pool:
            S.name_slot(nm)                                   # no digit, brace or negation cue
            assert not re.search(r"[\"|:;{}]", nm), nm
            assert not any(re.search(rf"\b{re.escape(w)}\b", nm.lower()) for w in T.T06Plugin.LABEL_WORDS), nm
    assert not set(T.JURIS) & set(T.JURIS_HELD)
    assert not set(T.N_REJ) & set(T.N_REJ_HELD) and not set(T.N_WD) & set(T.N_WD_HELD)
    assert max(T.N_WD) <= min(T.N_REJ)
    for st in set(T.SEAL_SET["intact"] + T.SEAL_SET["opened"] + T.REASON_SET["faulty"] + T.REASON_SET["mind"]):
        assert "|" not in st and ": " not in st
    for cat in (T.GOODS_SET, T.SEAL_SET, T.REASON_SET, T.HANDOVER_SET):
        assert all(len(v) == 1 for v in cat.values())        # one surface per key: twins keep the slot's form
    assert set(T.NOTICE_SCOPE) == set(T.NO_PROMISE) | set(T.WINDOWED) == set(B.NOTICE_MEANING)
    assert set(T.P_SETS) == set(T.WINDOWED)
    for sem, text in FX.NOTICES:
        assert ("{P}" in text) == (sem in T.WINDOWED) and '"' not in text
    for fid, f in ctx.lexicon.forms.items():
        assert f.unit_ok and ctx.lexicon.status(fid) == "admitted", (fid, f.unit_problems)


# ------------------------------------------------------------------------------------------------ hand-checked golds

def _case(plugin, *, qform="yn_refund", style="act", reason="faulty", goods="standard", seal=None, handover="direct",
          ordered, delivered, possession=None, requested, n_rej=14, n_wd=7, policy="pol.t06.final", p=None,
          counts=True):
    """A spec with every decisive fact set by hand (names from a sampled spec)."""
    base = plugin.sample(0, "S1")
    slots = {k: v for k, v in base.slots.items() if k not in ("SEAL", "P_DAYS")}
    slots.update({"REASON": S.category_slot(reason, T.REASON_SET), "GOODS": S.category_slot(goods, T.GOODS_SET),
                  "HANDOVER": S.category_slot(handover, T.HANDOVER_SET), "ORDER_DATE": S.date_slot(ordered),
                  "DELIVERY_DATE": S.date_slot(delivered), "POSSESSION_DATE": S.date_slot(possession or delivered),
                  "REQUEST_DATE": S.date_slot(requested), "N_REJ": S.count_slot(n_rej, T.DAYS),
                  "N_WD": S.count_slot(n_wd, T.DAYS), "POLICY": plugin._policy_clause(policy, None)})
    if seal:
        slots["SEAL"] = S.category_slot(seal, T.SEAL_SET)
    if p is not None:
        slots["P_DAYS"] = S.count_slot(p, T.DAYS)
    spec = Spec(T.FAMILY, "S1", 0, base.card_id, qform, slots, structure={"style": style, "counts": counts})
    assert T._consistent(T.facts(spec), qform)
    return plugin.derive(spec)


HAND_CASES = [
    # (description, case kwargs, expected answer)
    ("leap year: delivery 20 Feb 2028 + 14 days ends on 5 March; a request that day is in time",
     dict(ordered=D(2028, 2, 17), delivered=D(2028, 2, 20), requested=D(2028, 3, 5)), 1),
    ("leap year: 6 March 2028 is day 15, late; the change-of-mind period (7) has run out too",
     dict(ordered=D(2028, 2, 17), delivered=D(2028, 2, 20), requested=D(2028, 3, 6)), 0),
    ("common year: delivery 20 Feb 2027 + 14 days ends on 6 March",
     dict(ordered=D(2027, 2, 17), delivered=D(2027, 2, 20), requested=D(2027, 3, 6)), 1),
    ("common year: 7 March 2027 is day 15, late",
     dict(ordered=D(2027, 2, 17), delivered=D(2027, 2, 20), requested=D(2027, 3, 7)), 0),
    ("ch_end_reject across the leap day", dict(qform="ch_end_reject", ordered=D(2028, 2, 17), delivered=D(2028, 2, 20),
                                               requested=D(2028, 2, 25)), "2028-03-05"),
    ("ch_end_reject across a year end", dict(qform="ch_end_reject", ordered=D(2026, 12, 20), delivered=D(2026, 12, 25),
                                             requested=D(2026, 12, 28)), "2027-01-08"),
    ("withdrawal runs from possession (locker pickup), not delivery: day 14 of 14 is in time",
     dict(reason="mind", handover="locker", ordered=D(2026, 5, 25), delivered=D(2026, 5, 28),
          possession=D(2026, 6, 2), requested=D(2026, 6, 16), n_wd=14), 1),
    ("ch_end_withdraw from possession", dict(qform="ch_end_withdraw", reason="mind", handover="locker",
                                             ordered=D(2026, 5, 25), delivered=D(2026, 5, 28),
                                             possession=D(2026, 6, 2), requested=D(2026, 6, 3), n_wd=14),
     "2026-06-16"),
    ("hygiene goods with the seal intact keep the withdrawal right (conditional exclusion)",
     dict(reason="mind", goods="hygiene", seal="intact", ordered=D(2026, 4, 1), delivered=D(2026, 4, 3),
          requested=D(2026, 4, 10)), 1),
    ("hygiene goods with the seal broken after delivery: excluded, and the notice is final",
     dict(reason="mind", goods="hygiene", seal="opened", ordered=D(2026, 4, 1), delivered=D(2026, 4, 3),
          requested=D(2026, 4, 10)), 0),
    ("exclusions never limit the faulty-goods right (custom goods, faulty, day 10 of 14)",
     dict(goods="custom", ordered=D(2026, 9, 1), delivered=D(2026, 9, 3), requested=D(2026, 9, 13)), 1),
    ("a stricter notice (faulty items within 5 days of purchase) loses to the statute",
     dict(qform="ch_rule", ordered=D(2026, 3, 1), delivered=D(2026, 3, 4), requested=D(2026, 3, 20), n_rej=21,
          policy="pol.t06.faulty_order", p=5), "reject"),
    ("a more generous notice applies (any reason within 60 days of delivery; perishable, change of mind)",
     dict(qform="ch_rule", reason="mind", goods="perishable", ordered=D(2026, 6, 28), delivered=D(2026, 7, 1),
          requested=D(2026, 8, 20), policy="pol.t06.any_delivery", p=60), "store"),
    ("order date trap: day 13 from delivery is in time although day 23 from the order date",
     dict(ordered=D(2026, 10, 20), delivered=D(2026, 10, 30), requested=D(2026, 11, 12)), 1),
    ("day zero: a request on the delivery day itself is in time",
     dict(qform="ch_rule", goods="custom", ordered=D(2026, 1, 5), delivered=D(2026, 1, 9), requested=D(2026, 1, 9)),
     "reject"),
    ("nothing grants: a faulty return long after both statutory periods under a store-credit notice",
     dict(qform="ch_rule", reason="faulty", goods="standard", ordered=D(2026, 8, 1), delivered=D(2026, 8, 4),
          requested=D(2026, 10, 20), policy="pol.t06.credit"), "none"),
    ("deep row (no printed counts): 31 Jan + 30 days is 2 March in a common year, so 2 March is in time",
     dict(goods="custom", ordered=D(2027, 1, 27), delivered=D(2027, 1, 31), requested=D(2027, 3, 2), n_rej=30,
          counts=False), 1),
    ("deep row: 3 March 2027 is day 31, late",
     dict(goods="custom", ordered=D(2027, 1, 27), delivered=D(2027, 1, 31), requested=D(2027, 3, 3), n_rej=30,
          counts=False), 0),
]


@pytest.mark.parametrize("desc,kw,want", HAND_CASES, ids=[c[0][:48] for c in HAND_CASES])
def test_hand_computed_golds(plugin, ctx, desc, kw, want):
    spec = _case(plugin, **kw)
    assert plugin.solve_a(spec) == want, desc
    got_b, rr = _b(plugin, ctx, spec)
    assert got_b == want and rr.answer == want, desc
    assert pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False) == [], desc
    if spec.qform == "yn_refund":                      # every yes/no form agrees with the refund decision
        for q in YN:
            pol = plugin.QFORMS[q].polarity
            assert plugin.solve_a(spec.replace(qform=q)) == (want if pol == 1 else 1 - want)


def test_printed_day_counts_match_a_day_by_day_walk(specs2000):
    for spec in specs2000[:800]:
        if not spec.structure["counts"]:
            assert not spec.derived and "deep" in spec.tags
            continue
        v = spec.env()
        for name, src in (("D_ORDER", "ORDER_DATE"), ("D_DELIV", "DELIVERY_DATE"), ("D_POSS", "POSSESSION_DATE")):
            assert v[name] == len(brute.day_list(v[src], v["REQUEST_DATE"])) - 1


# ------------------------------------------------------------------------------------------------ A == B

def test_solver_a_equals_solver_b_on_5000_specs(plugin, ctx):
    """G2 (and G3, G-SL, G-LEX, schema, options) on 1,000 seeds x 5 samplers: every row passes check_rendered."""
    seen = collections.Counter()
    fails = []
    for seed in range(1000):
        for smp in plugin.SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            probs = pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False)
            if probs:
                fails.append((seed, smp, probs[:2]))
            view = plugin.parse(rr.row, ctx)
            assert plugin.solve_b(view) == plugin.solve_a(spec) == rr.answer
            f = T.facts(spec)
            seen[("qform", spec.qform)] += 1
            seen[("style", f.style)] += 1
            seen[("container", rr.row["meta"]["format_style"].split("/")[1])] += 1
            seen[("policy", f.policy)] += 1
            seen[("goods", f.goods, f.seal)] += 1
            seen[("mode", rr.row["meta"]["c2"]["author_mode"])] += 1
            seen[("deep", spec.deep)] += 1
    assert not fails, fails[:5]
    assert sum(v for k, v in seen.items() if k[0] == "qform") == 5000
    assert {k[1] for k in seen if k[0] == "qform"} == set(plugin.QFORMS)
    assert {k[1] for k in seen if k[0] == "style"} == set(T.STYLE_TEXT)
    assert {k[1] for k in seen if k[0] == "container"} == {"lines", "table", "json"}
    assert {k[1] for k in seen if k[0] == "policy"} == set(T.NOTICE_SCOPE)
    assert len([k for k in seen if k[0] == "goods"]) == 5
    assert seen[("mode", "F")] > 0 and seen[("deep", True)] > 0


# ------------------------------------------------------------------------------------------------ relations

def test_relation_units_pass_every_gate(plugin, ctx):
    units, kinds = [], collections.Counter()
    for seed in range(300):
        for smp in plugin.SAMPLERS:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=(seed < 2))
            assert res.ok, (seed, smp, res.problems[:3])
            units.append(res)
            for r in res.rows:
                kinds[r["role"]] += 1
                assert R.validate_row(r) == []
                assert R.approx_tokens(r) <= R.MAX_TOKENS
                assert r["meta"]["dev_only"] == (smp == "S5" or r["meta"]["c2"]["register"] in
                                                 plugin.HELD_OUT_REGISTERS)
    rep = pipeline.overlay_report(units, plugin)
    rows = rep["rows"]
    assert rep["complement_share_of_yes_no"] >= 0.20 and rep["non_syntactic_share_of_pairs"] >= 0.30
    assert 0.18 <= rep["twin_share"] <= 0.27
    assert 0.04 <= rep["equiv_share"] <= 0.10 and 0.01 <= rep["attack_share"] <= 0.06
    assert 0.45 <= rep["yes_no"] / rows <= 0.55
    assert 0.45 <= rep["yes_rate"] <= 0.55
    assert set(kinds) == {"base", "complement", "twin", "equiv", "attack"}
    toks = [R.approx_tokens(r) for u in units for r in u.rows]
    assert sum(toks) / len(toks) <= 1100                 # about 800 real tokens (3 chars per approx token)
    questions = [r["instructions"] for u in units for r in u.rows if r["qtype"] == "noul"]    # the rules are in row.card
    k_syn = [negcount.count(q).k_syn for q in questions]
    assert sum(k >= 1 for k in k_syn) / len(k_syn) >= 0.10                           # spec 3.0 syntactic negation
    assert sum(k >= 2 for k in k_syn) / len(k_syn) >= 0.02                           # spec 3.0 double negation
    s5 = [r for u in units for r in u.rows if r["meta"]["sampler"] == "S5"]
    assert s5 and all(r["meta"]["wording_id"].startswith("WH-") for r in s5)        # held-out wordings on S5 only
    assert not any(r["meta"]["wording_id"].startswith("WH-") for u in units for r in u.rows
                   if r["meta"]["sampler"] != "S5")
    assert all("Regulations" in (r.get("card") or "") + r["instructions"] for r in s5)   # held-out statute style
    assert not any("Regulations" in (r.get("card") or "") + r["instructions"] for u in units for r in u.rows
                   if r["meta"]["sampler"] != "S5")


def test_twins_differ_in_one_slot_and_flip_exactly_as_constructed(plugin, ctx, specs2000):
    kinds = collections.Counter()
    for spec in specs2000:
        for prop in plugin.relations(spec):
            if prop.kind != "twin":
                continue
            twin = plugin.derive(prop.spec)
            assert slot_diff(spec, twin) == {prop.changed_slot}
            assert plugin.solve_a(twin) == prop.expect != plugin.solve_a(spec)
            assert T._consistent(T.facts(twin), twin.qform)
            got_b, _ = _b(plugin, ctx, twin)
            assert got_b == prop.expect
            kinds[prop.note] += 1
    assert set(kinds) == {f"twin {k}" for k in plugin.TWIN_KINDS}, kinds
    assert sum(kinds.values()) >= 0.30 * len(specs2000)


def test_haiku_pass_resolutions_hold(plugin, ctx, specs2000):
    """G0 v2 (Haiku pass H1, H4, H11, H26): no generated spec or twin has a request on the possession day (so "day
    zero is in time" and "days 1..N" agree on every row); the charter names the withdrawal right without a reason; the
    handover surfaces say the goods were delivered to the locker or neighbour; every style says calendar days."""
    for spec in specs2000:
        f = T.facts(spec)
        assert f.possession < f.requested and T._generable(f, spec.qform)
        for prop in plugin.relations(spec):
            if prop.kind == "twin":
                g = T.facts(prop.spec)
                assert g.possession < g.requested
    assert T.OPTION_TEXT["charter"]["withdraw"] == "The cooling-off rule"
    assert not any("mind" in t.lower() for st in T.OPTION_TEXT.values() for t in st.values())
    assert all("calendar days" in T.STYLE_TEXT[st] for st in T.STYLE_TEXT)
    assert all(v[0].startswith("delivered to") for k, v in T.HANDOVER_SET.items() if k != "direct")
    day0 = _case(plugin, qform="ch_rule", goods="custom", ordered=D(2026, 1, 5), delivered=D(2026, 1, 9),
                 requested=D(2026, 1, 9))
    assert not T._generable(T.facts(day0), "ch_rule")          # constructible by hand, never generated


def test_complements_are_opposite_and_the_refund_decision_fixes_every_answer(plugin, specs2000):
    for spec in specs2000:
        refund = _refund(spec)
        for q in YN:
            f = plugin.QFORMS[q]
            assert plugin.solve_a(spec.replace(qform=q)) == int(refund == (f.polarity == 1))
        if spec.qform in YN:
            base = plugin.solve_a(spec)
            partner = plugin._partner(spec)
            assert plugin.QFORMS[partner].predicate == plugin.QFORMS[spec.qform].predicate
            assert plugin.QFORMS[partner].polarity == -plugin.QFORMS[spec.qform].polarity
            assert plugin.solve_a(spec.replace(qform=partner)) == 1 - base
        if spec.qform == "ch_rule":
            assert plugin.solve_a(spec) == ("none" if not refund else next(iter(T._grants(T.facts(spec)))))


def test_wording_negation_counts_follow_the_g0(ctx):
    want = {"yn_refund": 0, "yn_owed": 0, "yn_may_refuse": 0, "yn_not_refund": 1, "yn_no_right": 1, "yn_double": 2}
    for sk in ctx.skins.values():
        if sk.kind == "wording" and sk.qform in want:
            c = negcount.count(sk.text)
            assert c.k_all == want[sk.qform], (sk.skin_id, c)
            if sk.qform == "yn_double":
                assert c.k_syn == 2


def test_metamorphic_relations_keep_the_answer(plugin, specs2000):
    notes = collections.Counter()
    for spec in specs2000[:1000]:
        g4 = [p for p in plugin.relations(spec) if p.kind == "metamorphic"]
        assert len(g4) >= 5
        for prop in g4:
            want = plugin.solve_a(spec) if prop.expect == "same" else prop.expect
            assert plugin.solve_a(plugin.derive(prop.spec)) == want, prop.note
            notes[prop.note] += 1
    # the six always-on G4 relations + the v4 rule-swap / rule-deleted / nonce-vocabulary relations (G0 v4 S22)
    assert len(notes) == 9 and notes["rule swap: the notice replaces the statute"] > 0
    assert notes["rule deleted: no withdrawal rule"] > 0 and notes["nonce names for customer, store, item, jurisdiction"] > 0


# ------------------------------------------------------------------------------------------------ balance

def test_gold_balance_on_2000_specs(plugin, specs2000):
    yn = [s for s in specs2000 if s.qform in YN]
    assert 0.40 <= len(yn) / len(specs2000) <= 0.48
    assert 0.48 <= sum(plugin.solve_a(s) for s in yn) / len(yn) <= 0.52             # gold yes 50 +- 2
    assert 0.45 <= sum(bool(plugin.QFORMS[s.qform].yes_is_bad) for s in yn) / len(yn) <= 0.55
    cells = collections.defaultdict(collections.Counter)             # display -> gold key (G0 v3 S10)
    for s in specs2000:
        if s.qform == "ch_rule":
            shown = T._applicable(T.facts(s))
            assert len(shown) >= T.MIN_RULES_SHOWN
            cells[shown][plugin.solve_a(s)] += 1
    assert len(cells) == 4                                            # three pairs of rules and the three together
    for shown, rules in cells.items():                                # every shown option, none included, is gold on 1 / k
        tot, k = sum(rules.values()), len(shown) + 1
        assert set(rules) <= set(shown) | {"none"}
        for key in (*shown, "none"):
            assert abs(rules[key] / tot - 1 / k) <= 0.09, (shown, key, rules[key] / tot, tot)
    for attr in ("goods", "reason", "policy", "handover", "style"):        # no single fact predicts the refund
        cells = collections.defaultdict(list)
        for s in yn:
            cells[getattr(T.facts(s), attr)].append(_refund(s))
        for k, v in cells.items():
            assert 0.35 <= sum(v) / len(v) <= 0.65, (attr, k, sum(v) / len(v))
    tags = collections.Counter(t for s in specs2000 for t in s.tags)
    share = {k: v / len(specs2000) for k, v in tags.items()}
    assert 0.20 <= share["stricter_sign"] <= 0.36                                    # spec 3.13: 25%
    assert 0.20 <= share["order_date"] <= 0.40                                       # spec 3.13: 20% (G0 v3: 31%)
    assert 0.20 <= share["boundary_day"] <= 0.60                                     # spec 3.13: 20% (G0 v3: 48%, requests near a window end)
    assert 0.10 <= share["conditional_exception"] <= 0.25                            # spec 3.13: 15%
    assert 0.10 <= share["generous_notice"] <= 0.20                                  # spec 3.13: 10%
    assert share["leap_day"] >= 0.05 and share["month_end"] >= 0.50
    assert 0.02 <= share["deep"] <= 0.10                                             # spec 3.0: deep <= 10%
    s2 = [s for s in specs2000 if s.sampler == "S2"]                                 # label-first: more near misses
    s1 = [s for s in specs2000 if s.sampler == "S1"]
    assert sum("boundary_day" in s.tags for s in s2) > sum("boundary_day" in s.tags for s in s1)


def test_yes_rate_per_question_form_on_12000_specs(plugin):
    yes = collections.defaultdict(list)
    for seed in range(3000):
        for smp in TRAIN:
            s = plugin.sample(seed, smp)
            if s.qform in YN:
                yes[s.qform].append(plugin.solve_a(s))
    for q, v in yes.items():
        assert len(v) >= 300 and 0.45 <= sum(v) / len(v) <= 0.55, (q, len(v), sum(v) / len(v))


def test_card_rates_span_20_to_80_and_average_one_half():
    for smp, n in (("S1", T.N_CARDS), ("S5", T.N_CARDS_HELD)):
        rates = [T._card_rate(smp, c) for c in range(n)]
        assert all(0.2 <= r <= 0.8 for r in rates) and abs(sum(rates) / n - 0.5) < 1e-12
    assert T.N_CARDS * len(TRAIN) >= 20                                              # spec 3.0: >= 20 cards


# ------------------------------------------------------------------------------------------------ G-SL

def test_builtin_skins_pass_gsl(plugin, ctx):
    for sk in ctx.skins.values():
        if sk.author_mode != "T":
            continue
        v = gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                              name_allow=plugin.NAME_ALLOW)
        assert v == [], (sk.skin_id, v)
        lit = K.PH_RE.sub(" ", sk.text).lower()
        if sk.kind in ("skin", "attack"):                        # no gold-label word, even in attack lines
            assert not any(re.search(rf"(?<![a-z]){re.escape(w)}", lit) for w in plugin.LABEL_WORDS), sk.skin_id
        if sk.kind == "skin":
            assert dict(sk.slots) == FX.NARR and "\n\n" not in sk.text
    pools = set(T.CUSTOMERS) | set(T.STORES) | set(T.JURIS) | set(T.JURIS_HELD)
    pools |= {i for items in T.ITEMS.values() for i in items}
    for sk in ctx.skins.values():                                # no slot value written as literal text
        if sk.author_mode == "T":
            lit = K.PH_RE.sub(" ", sk.text)
            assert not [p for p in pools if re.search(rf"(?<![\w-]){re.escape(p)}(?![\w-])", lit)], sk.skin_id


def test_mode_f_message_keeps_its_facts_verbatim(plugin, ctx):
    free = ctx.skin("SK-FREE-1")
    spec = plugin.sample(7, "S1")
    rr = plugin.render(spec, ctx, skin=free)
    assert pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False) == []
    view = plugin.parse(rr.row, ctx)
    assert "customer" not in view and view["item"] == spec.env()["ITEM"]
    assert plugin.canonical_for(spec, "F") == {k: v for k, v in view.items() if k != "options"}
    assert set(plugin.extract_view(spec)) == {f.name for f in plugin.extract_fields(spec)}
    region = rr.row["state"][slice(*rr.regions["SK-FREE-1"][1:])]
    for name in ("CUSTOMER", "ITEM", "STORE"):
        assert spec.env()[name] in region


def test_program_templates_hold_no_literal_values():
    """Program text (cards, record templates, notice line, options) carries rule constants only: no digit, date,
    month, weekday, currency sign, address or pool value outside the placeholders."""
    pools = set(T.CUSTOMERS) | set(T.STORES) | set(T.JURIS) | set(T.JURIS_HELD)
    pools |= {i for items in T.ITEMS.values() for i in items}
    texts = [T.NOTICE_TPL, T.ATTACK_PREFIX, T.CLOSED_WORLD]
    texts += [T.card_template(st) for st in T.STYLE_TEXT]
    texts += [t for st in T.OPTION_TEXT.values() for t in st.values()]
    for container in ("lines", "table", "json"):
        for seal in (True, False):
            for counts in (True, False):
                texts += list(T.record_template(container, seal, counts)[:2])
    for t in texts:
        lit = K.PH_RE.sub(" ", t)
        assert not re.search(r"\d", lit), lit[:80]
        assert not re.search(r"[$€£%@]|https?://|\.example", lit), lit[:80]
        words = set(re.findall(r"[A-Za-z]+", lit))
        assert not words & (gsl.MONTHS | gsl.WEEKDAYS), lit[:80]
        assert not [p for p in pools if re.search(rf"(?<![\w-]){re.escape(p)}(?![\w-])", lit)], lit[:80]


def test_gsl_catches_a_skin_that_leaks_the_label(plugin, ctx):
    leak = dataclasses.replace(ctx.skin("SK-CHAT-1"), skin_id="SK-LEAK",
                               text="{CUSTOMER}: the {ITEM} from {STORE} is faulty, so I am owed a refund.")
    c2 = dataclasses.replace(ctx, skins={**ctx.skins, "SK-LEAK": leak})
    spec = plugin.sample(5, "S1")
    probs = pipeline.check_rendered(plugin, spec, plugin.render(spec, c2, skin=leak), c2, run_g15=False)
    rules = {p.split(":", 1)[0] for g, p in probs if g == "G-SL"}
    assert "gold_label" in rules


def test_glex_blocks_forms_that_are_not_admitted(plugin, ctx):
    spec = plugin.sample(11, "S1")
    c2 = KitCtx(skins=ctx.skins, lexicon=FX.lexicon(admit=False))
    rr = plugin.render(spec, c2)
    gates = {g for g, _ in pipeline.check_rendered(plugin, spec, rr, c2, run_g15=False)}
    assert {"G-LEX", "G3"} <= gates                  # the notice form and the wording; B reads admitted forms only


# ------------------------------------------------------------------------------------------------ determinism

def _digest(plugin, ctx, n=60) -> str:
    h = hashlib.sha256()
    for seed in range(n):
        for smp in plugin.SAMPLERS:
            spec = plugin.sample(seed, smp)
            h.update(json.dumps(spec.facts(), sort_keys=True, default=str).encode())
            h.update(json.dumps(plugin.render(spec, ctx).row, sort_keys=True).encode())
            for prop in plugin.relations(spec):
                h.update(repr((prop.kind, prop.qform, prop.changed_slot, prop.expect, prop.note)).encode())
    return h.hexdigest()


def test_generation_is_deterministic_by_seed(plugin, ctx):
    a = pipeline.build_unit(plugin, plugin.sample(17, "S4"), ctx, run_g15=False).rows
    b = pipeline.build_unit(plugin, plugin.sample(17, "S4"), ctx, run_g15=False).rows
    assert a == b
    assert plugin.sample(17, "S4").facts() != plugin.sample(18, "S4").facts()
    assert _digest(plugin, ctx) == _digest(T.T06Plugin(lexicon=FX.ctx().lexicon), FX.ctx())


def test_generation_does_not_depend_on_the_hash_seed(plugin, ctx):
    code = ("import sys; sys.dont_write_bytecode = True; sys.path.insert(0, %r)\n"
            "from families.T06 import fixtures as FX, plugin as T, test_plugin as TP\n"
            "c = FX.ctx(); print(TP._digest(T.T06Plugin(lexicon=c.lexicon), c, 20))") % str(C2_BUILD)
    outs = set()
    for hs in ("1", "4242"):
        env = {**os.environ, "PYTHONHASHSEED": hs, "PYTHONDONTWRITEBYTECODE": "1"}
        res = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env, timeout=300)
        assert res.returncode == 0, res.stderr[-2000:]
        outs.add(res.stdout.strip())
    assert outs == {_digest(plugin, ctx, 20)}


# ------------------------------------------------------------------------------------------------ distractors

def test_error_models_name_every_wrong_option(plugin, ctx):
    rule_sets, end_sets = [], []
    for seed in range(600):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            if spec.qform not in ("ch_rule",) + T.END_FORMS:
                continue
            os_ = plugin.render(spec, ctx).option_set
            assert check_named(os_) == []
            for o in os_.options:
                assert set(o.err) <= set(plugin.error_models()) and all(e in CATALOG for e in o.err)
                if o.role not in ("gold", "abstain"):
                    assert o.err, (spec.qform, o.text)          # every wrong option is some model's output
            (rule_sets if spec.qform == "ch_rule" else end_sets).append(os_)
    assert len(rule_sets) > 800 and len(end_sets) > 200
    for sets in (rule_sets, end_sets):
        for k, counts in position_counts(sets).items():
            if sum(counts) >= 100:
                assert min(counts) / sum(counts) >= 0.15, (k, counts)
    used = collections.Counter(e for s in rule_sets + end_sets for o in s.options for e in o.err)
    # a ch_rule row shows the open rules and "none" (G0 v3 S10): a model whose mistaken reading is "none" (the statute
    # ignored, an exclusion applied absolutely ...) gives the abstain option, which is no model's output, never a rule
    only_none = {"ignore_exception", "t06_absolute_exception", "t06_ignore_notice", "t06_notice_any_reason",
                 "t06_sign_wins"}
    assert set(used) <= set(plugin.error_models()) and set(plugin.error_models()) - set(used) <= only_none, \
        set(plugin.error_models()) - set(used)


# ------------------------------------------------------------------------------------------------ gates have teeth

def _gate_failures(plugin, ctx, n=40) -> collections.Counter:
    out = collections.Counter()
    for seed in range(n):
        for smp in ("S1", "S2", "S3"):
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            for g, _ in res.problems:
                out[g] += 1
    return out


def test_g2_catches_a_solver_a_exclusion_bug(plugin, ctx, monkeypatch):
    monkeypatch.setitem(T.EXCLUSION_TABLE, ("hygiene", "intact"), True)            # A makes the exclusion absolute
    assert _gate_failures(plugin, ctx)["G2"] > 0


def test_g2_catches_a_solver_a_anchor_bug(plugin, ctx, monkeypatch):
    for k in [k for k, v in T.NOTICE_TABLE.items() if v == "DELIVERY_DATE"]:      # A counts the notice from purchase
        monkeypatch.setitem(T.NOTICE_TABLE, k, "ORDER_DATE")
    assert _gate_failures(plugin, ctx)["G2"] > 0


def test_g2_catches_a_solver_b_period_bug(plugin, ctx, monkeypatch):
    real = brute.window_days
    monkeypatch.setattr(B.brute, "window_days", lambda anchor, n: real(anchor, n - 1))   # B drops the last day
    assert _gate_failures(plugin, ctx)["G2"] > 0


def test_g2_catches_a_solver_b_exclusion_bug(plugin, ctx, monkeypatch):
    monkeypatch.setattr(B, "EXCLUDED_IF_OPENED", frozenset())                       # B forgets the hygiene exclusion
    assert _gate_failures(plugin, ctx, n=80)["G2"] > 0


def test_g3_catches_a_record_that_prints_the_wrong_date(plugin, ctx, monkeypatch):
    real = T.record_template

    def swapped(container, seal, counts):
        head, body, esc = real(container, seal, counts)
        return head, body.replace("{ORDER_DATE}", "{DELIVERY_DATE}", 1), esc
    monkeypatch.setattr(T, "record_template", swapped)
    assert _gate_failures(plugin, ctx)["G3"] > 0


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    real = T._grants
    monkeypatch.setattr(T, "_grants", lambda f, **kw: real(f, **{**kw, "shift": kw.get("shift", 0) + 1}))
    assert _gate_failures(plugin, ctx, n=60)["G-TW"] > 0


def test_g4_catches_a_date_shift_that_changes_the_answer(plugin, ctx, monkeypatch):
    real = T.T06Plugin._metamorphic

    def broken(self, spec):
        out = real(self, spec)
        v = spec.env()
        moved = spec.with_slot("REQUEST_DATE", S.date_slot(v["REQUEST_DATE"] + dt.timedelta(days=40)))
        return out + [P.RelationProposal("metamorphic", spec=moved, expect="same", note="request forty days later")]
    monkeypatch.setattr(T.T06Plugin, "_metamorphic", broken)
    assert _gate_failures(plugin, ctx)["G4"] > 0


# ------------------------------------------------------------------------------------------------ review fix: twin mix

def test_abstain_share_holds_on_every_emitted_row(plugin, ctx):
    """Minimal-edit twins mirror their base: fixing the one failing item of a base lands on the abstain key, so
    unthinned twins piled up there (38% of all emitted ch_rule rows against a G0 target of 29%). Twins onto the key are
    thinned (kit relations.abstain_twin_kept); P(gold | key shown) over ALL emitted rows (base, twin, equiv, inv) is now
    within 5 pp of the target."""
    shown = gold = 0
    chance = 0.0
    roles = collections.Counter()
    for seed in range(600):
        for smp in ("S1", "S2", "S3", "S4"):
            spec = plugin.sample(seed, smp)
            if spec.qform != "ch_rule":
                continue
            res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
            for rr in (res.rendered if res.ok else []):
                os_ = rr.option_set
                if os_ is None or not any(o.key == "none" for o in os_.options):
                    continue
                shown += 1
                gold += os_.gold.key == "none"
                chance += 1 / len(os_.options)
                roles[rr.row["role"]] += 1
    target = 0.29
    assert shown >= 300 and roles["twin"] >= 30, (shown, roles)
    assert abs(gold / shown - target) <= 0.05, (gold / shown, target, roles)


def test_end_dates_carry_no_rank_cue(plugin, ctx):
    """Review fix: the end-date options were anchor + N - 1, anchor + N + 1 and earlier anchors, so the gold sat in the
    middle ("take the second-highest date" 0.71 on ch_end_reject vs chance 0.25; sorted rank 0 never occurred). The
    gold's sorted rank is now target_rank(row key, k) on every emitted row, uniform per (question form, k)."""
    from c2_kit import distractors as DI
    second = n = 0
    chance = 0.0
    for seed in range(600):
        for smp in ("S1", "S2", "S3", "S4"):
            spec = plugin.sample(seed, smp)
            if spec.qform not in T.END_FORMS:
                continue
            res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
            for rr in (res.rendered if res.ok else []):
                if rr.row["qtype"] != "choice":
                    continue
                keys = sorted(o.key for o in rr.option_set.options)
                k, g = len(keys), rr.option_set.gold.key
                key = f"T06|{rr.row['meta']['seed']}|{rr.row['meta']['sampler']}|{rr.row['meta']['qform']}"
                assert keys.index(g) == rr.option_set.meta["gold_rank"] == DI.target_rank(key, k)
                n += 1
                second += keys[-2] == g
                chance += 1 / k
    assert n > 300 and second / n <= chance / n + 0.05, (second / n, chance / n)
    ranks = collections.defaultdict(collections.Counter)                 # independent base rows
    for seed in range(4000):
        for smp in ("S1", "S2", "S3", "S4"):
            spec = plugin.sample(seed, smp)
            if spec.qform in T.END_FORMS:
                os_ = plugin.render(spec, ctx).option_set
                ranks[(spec.qform, len(os_.options))][os_.meta["gold_rank"]] += 1
    for (q, k), c in ranks.items():
        m = sum(c.values())
        if m >= 200:
            tol = 4 * ((1 / k) * (1 - 1 / k) / m) ** 0.5
            assert max(abs(c[r] / m - 1 / k) for r in range(k)) <= tol, (q, k, c)
    assert sum(sum(c.values()) for c in ranks.values()) > 1500
