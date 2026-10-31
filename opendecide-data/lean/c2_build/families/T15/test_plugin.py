"""families/T15/test_plugin.py: in-memory tests for the T15 plugin (A37 f: no test writes a file; rows live in memory).

Covers the task's bars: solver A == solver B (and the G3 parse) on >= 5,000 sampled specs; relation units through every
program gate (G2, G3, G4, G-SL, G-LEX, G-TW, schema, and G15 on a few); minimal-edit twins differ in one slot and flip
exactly as constructed; complements are opposite; gold balance within its bands on 2,000 specs; G-SL on the built-in
placeholder skins (no gold-label word or literal value outside slots); determinism by seed (also across hash seeds).
Also: hand-worked examples whose gold was computed by hand from the card text, error-model distractors, negation
counts of every wording, and injected bugs that the gates must catch.

Run (from lean/):  ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T15
"""
from __future__ import annotations

import collections
import dataclasses
import hashlib
import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import gsl, pipeline  # noqa: E402
from c2_kit.paths import COMMON  # noqa: E402  (puts c_src/common on sys.path)
from c2_kit import plugin as P  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.distractors import CATALOG, abstain_report, check_named, position_counts  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from families.T15 import fixtures as FX  # noqa: E402
from families.T15 import plugin as T  # noqa: E402
from families.T15 import solver_b as B  # noqa: E402

import negcount  # noqa: E402  (c_src/common, read-only)

assert COMMON.is_dir()

TRAIN = ("S1", "S2", "S3", "S4")
YN = tuple(q for q, f in T.T15Plugin.QFORMS.items() if f.qtype == "noul")


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return T.T15Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs2000(plugin):
    return [plugin.sample(seed, smp) for seed in range(500) for smp in TRAIN]


def _b(plugin, ctx, spec, **kw):
    rr = plugin.render(spec, ctx, **kw)
    return plugin.solve_b(plugin.parse(rr.row, ctx)), rr


# ------------------------------------------------------------------------------------------------ contract

def test_plugin_meets_the_strict_contract(plugin):
    assert P.validate_plugin(plugin, strict=True) == []
    assert P.check_independence(plugin) == []
    assert plugin.PARADIGM_A != plugin.PARADIGM_B
    assert len(T.HERE.joinpath("G0_SPEC.md").read_text(encoding="utf-8").splitlines()) <= 200
    assert set(T.TRACK_OF) == set(plugin.QFORMS)
    for q, partners in T.PARTNERS.items():                    # every partner is a declared complement pairing
        assert abs(sum(w for _, w in partners) - 1.0) < 1e-9
        for p, _ in partners:
            a, b = plugin.QFORMS[q], plugin.QFORMS[p]
            assert a.predicate == b.predicate and a.polarity == -b.polarity, (q, p)


def test_closed_vocabularies_are_clean():
    for nm in T.FIRST_NAMES + T.CHILDREN + T.CREDITS + T.CREDITS_HELD + tuple(n for n, _ in T.GATE_PROGS) + tuple(
            n for n, _ in T.GATE_PROGS_HELD) + T.WORKERS:
        S.name_slot(nm)                                       # no digit, brace or negation cue
        assert not re.search(r"[,;:|\"`]", nm), nm
    assert not set(T.FEMALE_NAMES) & set(T.MALE_NAMES) and not set(T.CHILDREN) & set(T.FIRST_NAMES)
    for domain, values in T.ENROLL_SETS.items():
        assert len(set(values)) == len(values) and "none" in values
        for v in values:
            assert not re.search(r"[,;:|\"`\d]", v), v
        for route, near in T.ROUTES[domain]:
            assert route in values and (near is None or near in values)
            if near:                                          # a near-miss differs from its route by one word
                a, b = route.split(), near.split()
                assert len(a) == len(b) and sum(x != y for x, y in zip(a, b)) == 1
    for f in T.FIELDS.values():
        assert f.domain in T.DOMAIN_FIELDS and f.fid in T.DOMAIN_FIELDS[f.domain]
        lo, hi, step = f.lim
        assert f.decoy[0] <= lo and hi <= f.decoy[1], f.fid   # limits sit inside the plausible value range
    for fid, v in T.REAL_LIMITS:                              # real thresholds are never drawn
        rng = random.Random(fid)
        assert all(T.T15Plugin._limits(rng, T.FIELDS[fid].domain, [fid])[fid] != v for _ in range(3000))
    phrases = [f.phrase for f in T.FIELDS.values()]
    assert not any(a != b and a.startswith(b) for a in phrases for b in phrases)
    assert set(T.TIEBREAKS) == set(T.TB_TEXT) == set(T.DEFAULT_ORDER)


def test_resolved_haiku_pass_points(plugin):
    """G0 section 6 (amb:T15): the pass record, the card and option texts the resolution changed, the limit-twin guard."""
    assert plugin.G0_HAIKU_TASK == "c2-data-stage-a/amb:T15"
    rec = json.loads(T.HERE.joinpath("haiku", "ambiguity", "amb_T15_points.json").read_text(encoding="utf-8"))
    assert rec["pass"] == plugin.G0_HAIKU_TASK and rec["n_points"] == len(rec["points"]) == 46
    g0 = T.HERE.joinpath("G0_SPEC.md").read_text(encoding="utf-8").split("## 6.")[1]
    assert all(re.search(rf"\bH{i}\b", g0) for i in range(1, 47))           # every point has a resolution
    card = T.claim_card_template(("parent", "months", "income"))
    assert "The tie-breakers stop once one person is left." in card and "the steps stop" not in card        # H1
    assert "Each keeps only those still in the running who are best on it." in card                        # H9 (v1.3 text)
    assert "share a home" not in card and "Different people's months can overlap." in card                  # H42
    assert B.STEP_THREE in card.split("\n") and B.PARENT_LINE in card.split("\n")
    assert T.outcome_text("fail_B", ("gross", "net")) == "Not eligible: Gate B is the reason (net monthly income)"
    assert B.OUTCOME_OPTION.fullmatch(T.outcome_text("fail_A", ("hours", "head")))                       # H8
    # H39: a limit twin never lands on a real (FMLA) threshold. One gate "hours more than 1,200" with 1,250 hours:
    # the limit edit would be 1,250, so it is skipped and the fact edit is used whatever the seeded kind order.
    spec = _gate_spec(plugin, "yn_eligible", "work", [("hours", "cmp.gt", 1200)], {**FMLA, "hours": 1250})
    limit_first = 0
    for s in range(40):
        sp = spec.replace(seed=s)
        order = sorted(("fact", "limit", "comparator", "route"),
                       key=lambda k: T.uhash(T.FAMILY, "twin_kind", sp.sampler, s, k))
        limit_first += order.index("limit") < order.index("fact")
        prop = plugin._twin(sp)
        assert prop.changed_slot == "F_HOURS" and prop.expect == 0
    assert limit_first > 0                                                     # the guard had teeth


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
            seen[("qform", spec.qform)] += 1
            seen[("track", spec.structure["track"])] += 1
            seen[("style", rr.row["meta"]["format_style"].split("/")[1])] += 1
            if spec.structure["track"] == "gates":
                seen[("domain", spec.structure["domain"])] += 1
    assert not fails, fails[:5]
    assert sum(v for k, v in seen.items() if k[0] == "qform") == 5000
    assert {k[1] for k in seen if k[0] == "qform"} == set(plugin.QFORMS)
    assert {k[1] for k in seen if k[0] == "style"} == {"lines", "table", "json", "csv", "transcript"}
    assert {k[1] for k in seen if k[0] == "domain"} == {"household", "work"}


# ------------------------------------------------------------------------------------------------ hand-worked gold

def _common(plugin, qform, track):
    return {"YEAR": S.count_slot(2026), "WORKER": S.name_slot("Morgan Ellis"), "CASE_ID": S.id_slot("CASE-10001"),
            "PROG": S.name_slot("Harbor County Energy Credit" if track == "gates" else "Lakeshore Family Credit")}


def _gate_spec(plugin, qform, domain, gates, facts, route=None, enroll="none"):
    rng = random.Random(0)
    surf = {e: [e] for e in T.ENROLL_SETS[domain]}
    slots = {**_common(plugin, qform, "gates"), "SUBJECT": S.name_slot("Dana Okafor"),
             "ENROLL": S.category_slot(enroll, surf)}
    if route:
        slots["ROUTE"] = S.category_slot(route[0], surf)
    for i, (fid, sem, lim) in enumerate(gates):
        f = T.FIELDS[fid]
        slots[f"G{i + 1}_LIM"] = plugin._num_slot(f, lim)
        slots[f"G{i + 1}_CMP"] = plugin._comparator(sem, f"G{i + 1}_LIM", f.kind, rng)
    for fid, v in facts.items():
        slots[T.FIELDS[fid].slot] = plugin._num_slot(T.FIELDS[fid], v)
    st = {"track": "gates", "domain": domain, "gates": [g[0] for g in gates],
          "route": list(route[1]) if route else None}
    return plugin.derive(P.Spec("T15", "S1", 0, "T15:S1:c00", qform, slots, structure=st, depth=2))


def _claim_spec(plugin, qform, people, order, min_sem, min_m, asked=None, derive=True):
    rng = random.Random(0)
    slots = {**_common(plugin, qform, "claimants"), "SUBJECT": S.name_slot("Mia"),
             "MIN_M": S.count_slot(min_m, T.UNIT_MONTH), "MIN_CMP": plugin._comparator(min_sem, "MIN_M", "count", rng)}
    for i, (name, rel, months, income, filed) in enumerate(people, 1):
        slots.update({f"C{i}_NAME": S.name_slot(name), f"C{i}_REL": S.category_slot(rel, T.REL_SET),
                      f"C{i}_MONTHS": S.count_slot(months, T.UNIT_MONTH), f"C{i}_INC": S.cents_slot(income),
                      f"C{i}_FILED": S.category_slot(filed, T.FILED_SET)})
    if asked:
        slots["ASKED"] = S.name_slot(asked)
    st = {"track": "claimants", "people": len(people), "order": list(order)}
    spec = P.Spec("T15", "S1", 0, "T15:S1:c06", qform, slots, structure=st, depth=2)
    return plugin.derive(spec) if derive else spec


HOUSE = {"gross": 250000, "net": 200000, "assets": 100000, "residence": 6, "age": 40}
HOUSE_GATES = [("gross", "cmp.le", 250000), ("net", "cmp.lt", 200000), ("residence", "cmp.ge", 6)]
FMLA_GATES = [("tenure", "cmp.ge", 12), ("hours", "cmp.ge", 1250), ("head", "cmp.ge", 50)]
FMLA = {"tenure": 16, "hours": 1180, "head": 62, "gpay": 5000000, "npay": 3800000}
KHA = ("Kestrel Housing Aid", [1])
# (description, spec kwargs, question form, gold worked out by hand from the card text)
GATE_CASES = (
    ("task example: 1,180 hours < 1,250", dict(domain="work", gates=FMLA_GATES, facts=FMLA), "ch_outcome", "fail_B"),
    ("task example, yes/no", dict(domain="work", gates=FMLA_GATES, facts=FMLA), "yn_eligible", 0),
    ("gross equal to an at-most limit passes; net equal to a below limit fails",
     dict(domain="household", gates=HOUSE_GATES, facts=HOUSE), "ch_outcome", "fail_B"),
    ("the route skips the failing Gate B", dict(domain="household", gates=HOUSE_GATES, facts=HOUSE, route=KHA,
                                                enroll="Kestrel Housing Aid"), "ch_outcome", "eligible"),
    ("a near-miss programme is not the route", dict(domain="household", gates=HOUSE_GATES, facts=HOUSE, route=KHA,
                                                    enroll="Kestrel Housing Loan"), "yn_not_eligible", 1),
    ("an earlier failing gate decides, not the later one",
     dict(domain="household", gates=[("residence", "cmp.gt", 6), ("gross", "cmp.lt", 250000)], facts=HOUSE),
     "ch_outcome", "fail_A"),
    ("net would pass the gross gate, but the gate reads gross",
     dict(domain="household", gates=[("gross", "cmp.le", 220000), ("age", "cmp.ge", 18)],
          facts={**HOUSE, "net": 210000}), "yn_ineligible", 1),
)
P1 = [("Lena Shah", "mother", 6, 3000000, "yes"), ("Rosa Shah", "grandmother", 12, 9000000, "yes"),
      ("Ravi Anand", "father", 5, 9900000, "yes")]
CLAIM_CASES = (
    ("parent first: the mother beats the grandmother", dict(people=P1, order=("parent", "months", "income"),
                                                           min_sem="cmp.ge", min_m=6), "ch_claimant", "Lena Shah"),
    ("months first: the grandmother's 12 months win", dict(people=P1, order=("months", "parent", "income"),
                                                          min_sem="cmp.ge", min_m=6), "ch_claimant", "Rosa Shah"),
    ("more than 6 months removes the mother at exactly 6", dict(people=P1, order=("parent", "months", "income"),
                                                               min_sem="cmp.gt", min_m=6), "ch_claimant",
     "Rosa Shah"),
    ("nobody is left: the grandmother did not file",
     dict(people=[P1[0], P1[1][:4] + ("no",), P1[2]], order=("parent", "months", "income"), min_sem="cmp.gt",
          min_m=6, asked="Lena Shah"), "yn_elsewhere", 1),
    ("two parents tie on months: the higher income decides",
     dict(people=[("Lena Shah", "mother", 8, 5000000, "yes"), ("Ravi Anand", "father", 8, 6000000, "yes")],
          order=("parent", "months", "income"), min_sem="cmp.ge", min_m=6, asked="Lena Shah"), "yn_barred", 1),
    ("a non-filer with the best facts never wins",
     dict(people=[("Lena Shah", "mother", 7, 2000000, "yes"), ("Ravi Anand", "father", 12, 9000000, "no")],
          order=("income", "months", "parent"), min_sem="cmp.ge", min_m=6, asked="Lena Shah"), "yn_may_claim", 1),
)


@pytest.mark.parametrize("desc, kw, qform, gold", GATE_CASES, ids=[c[0] for c in GATE_CASES])
def test_hand_worked_gate_examples(plugin, ctx, desc, kw, qform, gold):
    spec = _gate_spec(plugin, qform, **kw)
    assert plugin.solve_a(spec) == gold, desc
    b, rr = _b(plugin, ctx, spec)
    assert b == gold and pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False) == []


@pytest.mark.parametrize("desc, kw, qform, gold", CLAIM_CASES, ids=[c[0] for c in CLAIM_CASES])
def test_hand_worked_claimant_examples(plugin, ctx, desc, kw, qform, gold):
    spec = _claim_spec(plugin, qform, **kw)
    assert plugin.solve_a(spec) == gold, desc
    b, rr = _b(plugin, ctx, spec)
    assert b == gold and pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False) == []


def test_a_full_tie_is_refused_by_both_solvers(plugin, ctx):
    tie = [("Lena Shah", "mother", 8, 5000000, "yes"), ("Ravi Anand", "father", 8, 5000000, "yes")]
    spec = _claim_spec(plugin, "ch_claimant", tie, ("parent", "months", "income"), "cmp.ge", 6, derive=False)
    with pytest.raises(T.Tie):
        plugin.derive(spec)                                      # the construction refuses it too
    with pytest.raises(P.ContractError):
        plugin.solve_a(spec)
    with pytest.raises(B.ParseError):
        plugin.solve_b(plugin.canonical(spec))                   # B's duel table has no single winner
    with pytest.raises(T.Tie):
        T._claim_winner(T.claim_facts(spec))
    for seed in range(400):                                      # and the sampler never emits one
        s = plugin.sample(seed, "S2")
        if s.structure["track"] == "claimants":
            T._claim_winner(T.claim_facts(s))


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
                assert r["meta"]["dev_only"] == (smp == "S5" or r["meta"]["c2"]["register"] in
                                                 plugin.HELD_OUT_REGISTERS)
    rep = pipeline.overlay_report(units, plugin)
    rows = rep["rows"]
    assert rep["complement_share_of_yes_no"] >= 0.20 and rep["non_syntactic_share_of_pairs"] >= 0.30
    assert 0.20 <= rep["twin_share"] <= 0.25                                         # spec 4.1: 20-25% of rows
    assert 0.05 <= rep["equiv_share"] <= 0.10 and 0.005 <= rep["attack_share"] <= 0.05
    assert 0.45 <= rep["yes_no"] / rows <= 0.55                                      # spec 3.0
    assert 0.48 <= rep["yes_rate"] <= 0.52
    assert rep["abstain"]["pass"] and rep["abstain"]["wrong_share"] >= 0.5
    oc = [r for u in units for r in u.rows if r["meta"]["qform"] == "ch_outcome"]       # G0 v1.3 S20 (pilot FIX-2):
    share = sum(r["gold"] == T.ELIGIBLE_TEXT for r in oc) / len(oc)                    # row level, twins included
    assert abs(share - sum(1 / len(r["options"]) for r in oc) / len(oc)) <= 0.04, share
    assert set(kinds) == {"base", "complement", "twin", "equiv", "attack"}
    questions = [r["instructions"] for u in units for r in u.rows if r["qtype"] == "noul"]    # v1.3: question only
    k_syn = [negcount.count(q).k_syn for q in questions]
    assert sum(k >= 1 for k in k_syn) / len(k_syn) >= 0.10                           # spec 3.0 syntactic negation
    assert sum(k >= 2 for k in k_syn) / len(k_syn) >= 0.02                           # spec 3.0 double negation
    s5 = [r for u in units for r in u.rows if r["meta"]["sampler"] == "S5"]
    assert s5 and all(r["meta"]["wording_id"].startswith("WH-") for r in s5)        # held-out wordings on S5 only
    assert not any(r["meta"]["wording_id"].startswith("WH-") for u in units for r in u.rows
                   if r["meta"]["sampler"] != "S5")
    assert all(R.approx_tokens(r) <= R.MAX_TOKENS for u in units for r in u.rows)


def test_twins_differ_in_one_slot_and_flip_exactly_as_constructed(plugin, ctx, specs2000):
    kinds = collections.Counter()
    for spec in specs2000:
        for prop in plugin.relations(spec):
            if prop.kind != "twin":
                continue
            twin = plugin.derive(prop.spec)
            assert slot_diff(spec, twin) == {prop.changed_slot}
            assert plugin.solve_a(twin) == prop.expect != plugin.solve_a(spec)
            b, _ = _b(plugin, ctx, twin)
            assert b == prop.expect
            kinds[prop.note] += 1
    assert set(kinds) == {f"twin {k}" for k in ("fact", "limit", "comparator", "route", "months", "filed", "income",
                                                 "relation")}, kinds
    assert sum(kinds.values()) >= 0.35 * len(specs2000)


def test_every_claimant_choice_twin_renders(plugin, ctx):
    """Regression (found by a 3,000-unit sweep at seeds 5000-5599): a ch_claimant twin whose edit left no named
    distractor could not render its options. Twins now keep >= 1 named distractor, like the sampler."""
    n = 0
    for seed in range(5000, 5600):
        for smp in plugin.SAMPLERS:
            spec = plugin.sample(seed, smp)
            if spec.qform != "ch_claimant":
                continue
            for prop in plugin.relations(spec):
                if prop.kind == "twin":
                    rr = plugin.render(plugin.derive(prop.spec), ctx)
                    assert rr.answer == prop.expect and len(rr.option_set.options) >= 2
                    assert all(o.err for o in rr.option_set.options if o.role == "error")
                    n += 1
    assert n >= 100


def test_complements_are_opposite_and_outcomes_fix_every_answer(plugin, specs2000):
    for spec in specs2000:
        track = spec.structure["track"]
        if track == "gates":
            outcome = plugin.solve_a(spec.replace(qform="ch_outcome"))
            holds = outcome == T.ELIGIBLE
        else:
            winner = plugin.solve_a(spec.replace(qform="ch_claimant"))
            holds = winner != T.NONE_KEY and winner == spec.env().get("ASKED")
        for q in YN:
            f = plugin.QFORMS[q]
            if T.TRACK_OF[q] != track or (track == "claimants" and "ASKED" not in spec.slots):
                continue
            assert plugin.solve_a(spec.replace(qform=q)) == int(holds == (f.polarity == 1))
        if spec.qform in YN:
            base = plugin.solve_a(spec)
            partner = plugin._partner(spec)
            assert plugin.QFORMS[partner].predicate == plugin.QFORMS[spec.qform].predicate
            assert plugin.QFORMS[partner].polarity == -plugin.QFORMS[spec.qform].polarity
            assert plugin.solve_a(spec.replace(qform=partner)) == 1 - base


def test_metamorphic_relations_keep_the_answer(plugin, specs2000):
    notes = collections.Counter()
    for spec in specs2000[:1000]:
        g4 = [p for p in plugin.relations(spec) if p.kind == "metamorphic"]
        assert len(g4) >= 3
        for prop in g4:
            assert plugin.solve_a(plugin.derive(prop.spec)) == plugin.solve_a(spec), prop.note
            notes[prop.note] += 1
    assert len(notes) == 10, notes


# ------------------------------------------------------------------------------------------------ balance

def test_gold_balance_on_2000_specs(plugin, specs2000):
    n = len(specs2000)
    gates = [s for s in specs2000 if s.structure["track"] == "gates"]
    claims = [s for s in specs2000 if s.structure["track"] == "claimants"]
    assert abs(len(gates) / n - 0.60) <= 0.02
    yn = [s for s in specs2000 if s.qform in YN]
    assert 0.39 <= len(yn) / n <= 0.45
    assert 0.48 <= sum(plugin.solve_a(s) for s in yn) / len(yn) <= 0.52             # gold yes 50 +- 2
    assert 0.45 <= sum(bool(plugin.QFORMS[s.qform].yes_is_bad) for s in yn) / len(yn) <= 0.55
    for pred in ("eligible", "claims"):
        ss = [s for s in yn if plugin.QFORMS[s.qform].predicate == pred]
        assert 0.44 <= sum(plugin.solve_a(s) for s in ss) / len(ss) <= 0.56
    out = collections.Counter(plugin.solve_a(s) for s in gates if s.qform == "ch_outcome")
    assert all(out[f"fail_{x}"] > 0 for x in "ABCD")
    for k in (2, 3, 4):       # G0 v1.3 S20 (pilot FIX-2): P(eligible) = 1 / (gate count + 1) on every gate count
        ss = [s for s in gates if s.qform == "ch_outcome" and len(s.structure["gates"]) == k]
        share = sum(plugin.solve_a(s) == T.ELIGIBLE for s in ss) / len(ss)
        assert abs(share - T.p_eligible(k)) <= 0.07, (k, len(ss), share)
    who = [(s, plugin.solve_a(s)) for s in claims if s.qform == "ch_claimant"]
    nobody = sum(a == T.NONE_KEY for _, a in who) / len(who)
    want = 0.5 * T.SHOW_ABSTAIN * T.NOBODY_SHARE                     # P(k = 3) x shown x gold nobody (G0 v1.3 S20)
    assert abs(nobody - want) <= 0.04, (nobody, want)
    for s, a in who:                                                 # label-first: the target is the plan's
        assert T.claim_plan(T.claim_key(s)).accepts(a, T.NONE_KEY), (s.seed, s.sampler)
    g = collections.Counter(t for s in gates for t in s.tags)
    sh = {k: v / len(gates) for k, v in g.items()}
    assert sh["first_gate_trap"] >= 0.30                     # spec 3.14 traps, measured in G0_SPEC.md 2
    assert sh["net_gross_trap"] >= 0.20 and sh["at_limit"] >= 0.25 and sh["one_off_limit"] >= 0.25
    assert sh["route_decides"] >= 0.10 and sh["route_not_enrolled_trap"] >= 0.08 and sh["multi_fail"] >= 0.08
    assert 0.40 <= sh["route_listed"] <= 0.60 and 0.20 <= sh["route_holder"] <= 0.30
    c = collections.Counter(t for s in claims for t in s.tags)
    sc = {k: v / len(claims) for k, v in c.items()}
    assert sc["order_trap"] >= 0.35 and sc["filed_trap"] >= 0.20 and sc["months_trap"] >= 0.15
    assert sc["months_at_minimum"] >= 0.20 and sc["income_tie"] >= 0.03 and sc["third_tiebreak"] >= 0.02
    assert sum(s.deep for s in specs2000) / n <= 0.10                                # spec 3.0 deep <= 10%
    cell = collections.Counter()                      # rule draws carry no gold signal (route listed, comparator)
    for s in gates:
        if s.qform not in YN:
            continue
        a = plugin.solve_a(s.replace(qform="yn_eligible"))
        cell[("route", bool(s.structure["route"]), a)] += 1
        cell[("k", len(s.structure["gates"]), a)] += 1
    for key in [("route", True), ("route", False), ("k", 2), ("k", 3), ("k", 4)]:
        yes, no = cell[key + (1,)], cell[key + (0,)]
        assert 0.35 <= yes / (yes + no) <= 0.65, (key, yes, no)


def test_card_rates_span_20_to_80_and_average_one_half():
    for smp, n in (("S1", T.N_CARDS), ("S5", T.N_CARDS_HELD)):
        rates = [T._card_rate(smp, c) for c in range(n)]
        assert all(0.2 <= r <= 0.8 for r in rates) and abs(sum(rates) / n - 0.5) < 1e-12
    for smp, n, g in (("S1", T.N_CARDS, T.N_GATE_CARDS), ("S5", T.N_CARDS_HELD, T.N_GATE_CARDS_HELD)):
        for track_cards in (range(0, g), range(g, n)):           # antithetic pairs never straddle the two tracks
            rates = [T._card_rate(smp, c) for c in track_cards]
            assert abs(sum(rates) / len(rates) - 0.5) < 1e-12


def test_wording_negation_counts_match_the_spec(ctx):
    want = {"yn_fails": (1, 0), "yn_fails_claim": (1, 0), "yn_not_eligible": (1, 1), "yn_may_not": (1, 1),
            "yn_dneg_eligible": (2, 2), "yn_dneg_claim": (2, 2)}
    for sk in ctx.skins.values():
        if sk.kind != "wording":
            continue
        filled = K.PH_RE.sub("Dana Okafor", sk.text)
        c = negcount.count(filled)
        assert (c.k_all, c.k_syn) == want.get(sk.qform, (0, 0)), (sk.skin_id, c.k_all, c.k_syn)


# ------------------------------------------------------------------------------------------------ G-SL

def test_builtin_skins_pass_gsl(plugin, ctx):
    for sk in ctx.skins.values():
        v = gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                              name_allow=plugin.NAME_ALLOW)
        assert v == [], (sk.skin_id, v)
        lit = K.PH_RE.sub(" ", sk.text).lower()
        if sk.kind in ("skin", "attack"):                        # no gold-label word, even in attack lines
            assert not any(re.search(rf"(?<![a-z]){re.escape(w)}", lit) for w in plugin.LABEL_WORDS), sk.skin_id
        if sk.kind == "skin":
            assert dict(sk.slots) == FX.NOTE and "\n\n" not in sk.text
    pools = set(T.FIRST_NAMES) | set(T.LAST_NAMES) | set(T.CHILDREN) | set(T.WORKERS) | set(T.CREDITS)
    pools |= {n for n, _ in T.GATE_PROGS + T.GATE_PROGS_HELD} | set(T.CREDITS_HELD)
    pools |= {e for vs in T.ENROLL_SETS.values() for e in vs if e != "none"} | set(T.PARENTS + T.NONPARENTS)
    for sk in ctx.skins.values():                                # no slot value written as literal text
        lit = K.PH_RE.sub(" ", sk.text)
        assert not [p for p in pools if re.search(rf"(?<![\w-]){re.escape(p)}(?![\w-])", lit)], sk.skin_id
        assert not re.search(r"\d|[$€£%]", lit), sk.skin_id


def _program_texts() -> list:
    texts = [T.NOTE_PREFIX, T.NONE_TEXT, T.ELIGIBLE_TEXT, T.CLOSED_WORLD]
    for domain, fids in T.DOMAIN_FIELDS.items():
        for k in (2, 3, 4):
            gates = tuple(fids[:k])
            for route in (None, (0,), tuple(range(k - 1))):
                texts.append(T.gate_card_template(gates, route))
            texts += [T.outcome_text(f"fail_{T.LETTERS[i]}", gates) for i in range(k)]
        for style in ("lines", "table", "json", "csv", "transcript"):
            texts += list(T.gate_facts_template(domain, style)[:2])
    for order in ((a, b, c) for a in T.TIEBREAKS for b in T.TIEBREAKS for c in T.TIEBREAKS if len({a, b, c}) == 3):
        texts.append(T.claim_card_template(order))
    for m in (2, 3, 4):
        for style in ("lines", "table", "json", "csv", "transcript"):
            texts += list(T.claim_facts_template(m, style)[:2])
    return texts


def test_program_templates_hold_no_literal_values():
    """Program text (cards, facts blocks, options) carries rule constants only: no digit, date, month, weekday,
    currency sign, address or pool value outside the placeholders."""
    pools = set(T.FIRST_NAMES) | set(T.LAST_NAMES) | set(T.CHILDREN) | set(T.WORKERS) | set(T.CREDITS)
    pools |= {n for n, _ in T.GATE_PROGS + T.GATE_PROGS_HELD} | {e for vs in T.ENROLL_SETS.values() for e in vs
                                                                   if e != "none"}
    for t in _program_texts():
        assert not K.malformed(t), t[:80]
        lit = K.PH_RE.sub(" ", t)
        assert not re.search(r"\d", lit), lit[:80]
        assert not re.search(r"[$€£%@]|https?://|\.example", lit), lit[:80]
        words = set(re.findall(r"[A-Za-z]+", lit))
        assert not words & (gsl.MONTHS | gsl.WEEKDAYS), lit[:80]
        assert not [p for p in pools if re.search(rf"(?<![\w-]){re.escape(p)}(?![\w-])", lit)], lit[:80]


def test_gsl_catches_a_skin_that_leaks_the_label(plugin, ctx):
    leak = dataclasses.replace(ctx.skin("SK-CHAT-1"), skin_id="SK-LEAK",
                               text="{WORKER}: case {CASE_ID} for {SUBJECT} is not eligible, two gates failed.")
    c2 = dataclasses.replace(ctx, skins={**ctx.skins, "SK-LEAK": leak})
    spec = plugin.sample(5, "S1")
    probs = pipeline.check_rendered(plugin, spec, plugin.render(spec, c2, skin=leak), c2, run_g15=False)
    rules = {p.split(":", 1)[0] for g, p in probs if g == "G-SL"}
    assert {"gold_label", "negation", "number", "status"} <= rules


# ------------------------------------------------------------------------------------------------ determinism

def _digest(plugin, ctx, n=60) -> str:
    h = hashlib.sha256()
    for seed in range(n):
        for smp in plugin.SAMPLERS:
            spec = plugin.sample(seed, smp)
            h.update(json.dumps(spec.facts(), sort_keys=True, default=str).encode())
            h.update(json.dumps(plugin.render(spec, ctx).row, sort_keys=True).encode())
    return h.hexdigest()


def test_generation_is_deterministic_by_seed(plugin, ctx):
    a = pipeline.build_unit(plugin, plugin.sample(17, "S4"), ctx, run_g15=False).rows
    b = pipeline.build_unit(plugin, plugin.sample(17, "S4"), ctx, run_g15=False).rows
    assert a == b
    assert plugin.sample(17, "S4").facts() != plugin.sample(18, "S4").facts()
    assert _digest(plugin, ctx) == _digest(T.T15Plugin(lexicon=FX.ctx().lexicon), FX.ctx())


def test_generation_does_not_depend_on_the_hash_seed(plugin, ctx):
    code = ("import sys; sys.dont_write_bytecode = True; sys.path.insert(0, %r)\n"
            "from families.T15 import fixtures as FX, plugin as T, test_plugin as TP\n"
            "c = FX.ctx(); print(TP._digest(T.T15Plugin(lexicon=c.lexicon), c, 20))") % str(C2_BUILD)
    outs = set()
    for hs in ("1", "4242"):
        env = {**os.environ, "PYTHONHASHSEED": hs, "PYTHONDONTWRITEBYTECODE": "1"}
        res = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env, timeout=300)
        assert res.returncode == 0, res.stderr[-2000:]
        outs.add(res.stdout.strip())
    assert outs == {_digest(plugin, ctx, 20)}


# ------------------------------------------------------------------------------------------------ distractors

def test_error_models_name_every_wrong_option(plugin, ctx):
    outcome_sets, claim_sets = [], []
    for seed in range(600):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            if spec.qform not in ("ch_outcome", "ch_claimant"):
                continue
            os_ = plugin.render(spec, ctx).option_set
            assert check_named(os_) == []
            for o in os_.options:
                assert set(o.err) <= set(plugin.error_models()) and all(e in CATALOG for e in o.err)
            if spec.qform == "ch_claimant":
                claim_sets.append(os_)
                assert all(o.err for o in os_.options if o.role == "error")
                assert {o.role for o in os_.options} <= {"gold", "error", "abstain"}
            else:
                outcome_sets.append(os_)
                assert [o.key for o in os_.options].count(T.ELIGIBLE) == 1
    rep = abstain_report(claim_sets)
    assert rep["pass"] and rep["wrong_share"] >= 0.5
    named = sum(1 for s in outcome_sets for o in s.options if o.role == "error")
    wrong = sum(1 for s in outcome_sets for o in s.options if o.role != "gold")
    assert named / wrong >= 0.80                     # closed sets: the rest keep the kit role 'closed' (G0 S20)
    for k, counts in position_counts(outcome_sets).items():
        assert min(counts) / sum(counts) >= 0.6 / k, (k, counts)


def test_error_models_give_their_named_mistake(plugin):
    em = plugin.error_models()
    s = _gate_spec(plugin, "ch_outcome", "household", HOUSE_GATES, HOUSE, route=KHA, enroll="Kestrel Housing Aid")
    assert plugin.solve_a(s) == T.ELIGIBLE
    assert em["t15_ignore_route"].fn(s) == "fail_B"                     # tests the skipped gate
    assert em["t15_route_skips_all"].fn(s) == T.ELIGIBLE
    assert em["drop_inclusive_endpoint"].fn(s) == "fail_A"              # gross at an at-most limit read as below
    near = _gate_spec(plugin, "ch_outcome", "household", HOUSE_GATES, HOUSE, route=KHA,
                      enroll="Kestrel Housing Loan")
    assert plugin.solve_a(near) == "fail_B" and em["t15_route_not_enrolled"].fn(near) == T.ELIGIBLE
    first = _gate_spec(plugin, "ch_outcome", "work", FMLA_GATES, FMLA)
    assert em["stop_at_first_gate"].fn(first) == T.ELIGIBLE and em["t15_any_pass"].fn(first) == T.ELIGIBLE
    gross = _gate_spec(plugin, "ch_outcome", "household", [("gross", "cmp.le", 220000), ("age", "cmp.ge", 18)],
                       {**HOUSE, "net": 210000})
    assert plugin.solve_a(gross) == "fail_A" and em["net_vs_gross"].fn(gross) == T.ELIGIBLE
    c = _claim_spec(plugin, "ch_claimant", P1, ("parent", "months", "income"), "cmp.ge", 6)
    assert plugin.solve_a(c) == "Lena Shah"
    assert em["wrong_tiebreak"].fn(c) == "Rosa Shah"                     # income, months, parent
    assert em["t15_skip_months_check"].fn(c) == "Lena Shah"              # parents tie, months then decide
    assert em["t15_income_only"].fn(c) == "Rosa Shah" and em["t15_most_months"].fn(c) == "Rosa Shah"
    assert em["drop_inclusive_endpoint"].fn(c) == "Rosa Shah"            # at least 6 read as more than 6
    assert em["t15_default_order"].fn(c) is None                         # the card already states that order
    assert em["stop_at_first_gate"].fn(c) is None and em["wrong_tiebreak"].fn(s) is None


# ------------------------------------------------------------------------------------------------ gates have teeth

@pytest.fixture(scope="module")
def teeth_specs(plugin):
    return [plugin.sample(seed, smp) for seed in range(40) for smp in ("S1", "S2", "S3")]


def _gate_failures(plugin, ctx, specs) -> collections.Counter:
    out = collections.Counter()
    for spec in specs:
        res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
        for g, _ in res.problems:
            out[g] += 1
    return out


def test_gates_pass_without_injected_bugs(plugin, ctx, teeth_specs):
    assert _gate_failures(plugin, ctx, teeth_specs) == collections.Counter()


def test_g2_catches_a_solver_a_endpoint_bug(plugin, ctx, teeth_specs, monkeypatch):
    monkeypatch.setitem(T.OP, "cmp.le", "<")                            # A reads "at most" as "below"
    monkeypatch.setitem(T.OP, "cmp.ge", ">")
    assert _gate_failures(plugin, ctx, teeth_specs)["G2"] > 0


def test_g2_catches_a_solver_b_endpoint_bug(plugin, ctx, teeth_specs, monkeypatch):
    monkeypatch.setitem(B.MEETS, "cmp.ge", {-1: False, 0: False, 1: True})
    assert _gate_failures(plugin, ctx, teeth_specs)["G2"] > 0


def test_g2_catches_a_solver_b_route_bug(plugin, ctx, teeth_specs, monkeypatch):
    real = B._gate_table
    monkeypatch.setattr(B, "_gate_table", lambda v: real({**v, "route": None}))   # B ignores the route
    assert _gate_failures(plugin, ctx, teeth_specs)["G2"] > 0


def test_g2_catches_a_solver_b_parent_bug(plugin, ctx, teeth_specs, monkeypatch):
    monkeypatch.setattr(B, "PARENT_WORDS", frozenset({"mother"}))
    assert _gate_failures(plugin, ctx, teeth_specs)["G2"] > 0


def test_g3_catches_a_facts_block_that_prints_the_wrong_value(plugin, ctx, teeth_specs, monkeypatch):
    real = T.gate_facts_template

    def swapped(domain, style):
        head, body, esc = real(domain, style)
        return head, body.replace("{F_NET", "{F_GROSS", 1).replace("{F_NPAY", "{F_GPAY", 1), esc
    monkeypatch.setattr(T, "gate_facts_template", swapped)
    assert _gate_failures(plugin, ctx, teeth_specs)["G3"] > 0


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    specs = [plugin.sample(seed, smp) for seed in range(80) for smp in ("S1", "S2")]
    real = T._first_failure                                       # the construction forgets the route's skips
    monkeypatch.setattr(T, "_first_failure", lambda gates, skipped, **k: real(gates, frozenset(), **k))
    assert _gate_failures(plugin, ctx, specs)["G-TW"] > 0


# ------------------------------------------------------------------------------------------------ review fix: k cells

def test_option_count_and_abstain_display_carry_no_label():
    """G0 v1.3 S20 (pilot FIX-1). The ch_claimant display plan (k, whether "Nobody may claim the child" is shown, whether
    it is the gold) is drawn from the row key BEFORE the structure; a spec the plan cannot fill is resampled, never
    re-tried with a smaller k or with the option forced on. Over all emitted rows: nobody is never shown at k = 2; in the
    one cell that shows it (k = 3) it is gold on about 1/3 of the rows (a twin never ends in nobody, so the cell share
    is under the base rows' share) and wrong on >= 50%; every row of a unit keeps the unit's k and display."""
    from c2_kit import distractors as DI
    c = FX.ctx()
    pl = T.T15Plugin(lexicon=c.lexicon)
    sets, units, twins = [], [], 0
    for seed in range(600):
        for smp in ("S1", "S2", "S3", "S4"):
            spec = pl.sample(seed, smp)
            if spec.qform != "ch_claimant":
                continue
            plan = T.claim_plan(T.claim_key(spec))
            assert plan.accepts(pl.solve_a(spec), T.NONE_KEY) and plan.k in T.CLAIM_K      # label-first
            res = pipeline.build_unit(pl, spec, c, run_g15=False)
            assert res.ok, res.problems[:2]
            units.append([(r["role"], r["gold"], r["options"]) for r in res.rows])
            for rr in res.rendered:
                sets.append(rr.option_set)
                if rr.row["role"] == "twin":
                    twins += 1
                    assert rr.row["gold"] != T.NONE_TEXT                                      # twins never abstain
    assert twins > 100
    for rows in units:                                           # one k and one display per unit
        shown = {T.NONE_TEXT in o for _, _, o in rows}
        assert len({len(o) for _, _, o in rows}) == 1 and len(shown) == 1, rows
    cells = DI.abstain_cells(sets)
    assert not any(k == 2 and sh for (k, sh) in cells), cells     # k = 2 never shows the abstain option
    assert all(v["abstain_gold"] == 0 for (k, sh), v in cells.items() if not sh)
    v = cells[(3, True)]
    assert v["rows"] >= 200 and v["wrong_share"] >= 0.5, v
    assert 1 / 3 - 0.06 <= v["abstain_gold"] / v["rows"] <= 1 / 3 + 0.05, v
    assert DI.abstain_report(sets)["pass"]


def test_every_claimant_plan_names_one_cell():
    """The plan is a function of the row key: the same key gives the same plan; k = 2 plans never show the option; the
    gold-nobody target only occurs on shown k = 3 plans (the label never moves k)."""
    seen = collections.Counter()
    for seed in range(4000):
        key = f"T15|{seed}|S1|ch_claimant"
        plan = T.claim_plan(key)
        assert plan == T.claim_plan(key) and plan.row_key == key
        seen[(plan.k, plan.show_abstain, plan.gold_abstain)] += 1
        if plan.k < T.ABSTAIN_MIN_K:
            assert not plan.show_abstain and not plan.gold_abstain
        if plan.gold_abstain:
            assert plan.show_abstain and plan.k == 3
    n3 = sum(v for (k, _, _), v in seen.items() if k == 3)
    assert abs(sum(v for (k, sh, _), v in seen.items() if k == 3 and sh) / n3 - T.SHOW_ABSTAIN) <= 0.03
    shown = sum(v for (k, sh, _), v in seen.items() if sh)
    assert abs(sum(v for (_, _, g), v in seen.items() if g) / shown - T.NOBODY_SHARE) <= 0.03


def test_rules_are_printed_once_on_yes_no_rows(plugin, ctx):
    """G0 v1.3 S18 (pilot FIX-3): a yes/no row carries the rules in row.card and only the question in its instructions;
    a choice row carries them at the head of its instructions and no card; split_rules reads both layouts."""
    from c2_kit import cards as CARDS
    seen = collections.Counter()
    for seed in range(40):
        for smp in ("S1", "S3", "S4"):
            spec = plugin.sample(seed, smp)
            row = plugin.render(spec, ctx).row
            rules, question = CARDS.split_rules(row)
            assert T.CLOSED_WORLD in rules and "\n\n" not in rules and "\n" not in question
            if row["qtype"] == "noul":
                assert row["card"] == rules and row["instructions"] == question
                assert row["meta"]["defs_style"] == "rules_in_card_full"
            else:
                assert not row["card"] and row["instructions"] == rules + "\n\n" + question
                assert row["meta"]["defs_style"] == "rules_in_instructions_full"
            seen[row["qtype"]] += 1
    assert set(seen) == {"noul", "choice"}


def test_polarity_screen_is_clean_on_the_fixture_wordings(plugin, ctx):
    """c2_kit.polarity opt-in: the plugin's negative predicates are well formed and the stand-in wordings read with
    their forms' declared polarity (the frozen pool's 133 yes/no wordings were screened: 0 failures)."""
    from c2_kit import polarity
    assert plugin.POLARITY_CHECK and polarity.config_problems(plugin) == []
    _, bad = polarity.screen(ctx, plugin)
    assert bad == {}, bad
    assert polarity.form_problems(plugin, "yn_not_eligible", "Is {SUBJECT} not eligible for {PROG}?") == []
    assert polarity.form_problems(plugin, "yn_eligible", "Is {SUBJECT} not eligible for {PROG}?")      # P2: inverted
    assert polarity.form_problems(plugin, "yn_barred", "Is {ASKED} shut out from claiming {SUBJECT}?") == []
    assert polarity.form_problems(plugin, "yn_may_claim", "Isn't {ASKED} the person who may claim {SUBJECT}?")  # P3


def test_fixed_card_text_fits_the_fix3_token_budget(plugin):
    """Pilot FIX-3 (spec 3.0 length): step three <= 40 and the first gate bullet <= 28 real Qwen3.5 tokens, the gate
    interview's six questions <= 60, a claimant's four questions <= 44 (with a typical name), every rule kept."""
    from c2_kit import cards as CARDS
    _mx, tok = CARDS._tokenizer()
    if tok is None:
        pytest.skip("pinned tokenizer unavailable")
    n = lambda t: len(tok.encode(t, add_special_tokens=False).ids)       # noqa: E731
    assert n(B.STEP_THREE) <= 40 and n(B.GATE_INTRO) <= 28
    for domain, fids in T.DOMAIN_FIELDS.items():
        qs = [f"Caseworker: {T.FIELDS[f].question}" for f in fids] + [f"Caseworker: {B.ENROLL_QUESTION}"]
        assert sum(n(q) for q in qs) <= 60, domain
    body = T.claim_facts_template(1, "transcript")[1].split("\n")
    qs = [ln for ln in body if ln.startswith("Caseworker:")]
    assert len(qs) == 4
    assert sum(n(q.replace("{C1_NAME}", "Rosa Okafor").replace("{SUBJECT}", "Mia")) for q in qs) <= 44
    # the rules survive the shortening: first-failure stop, the applicable-gates clause, the running set, the stop rule
    assert "first gate that fails" in B.GATE_INTRO and "stop" in B.STEP_THREE
    assert "still in the running" in B.STEP_THREE and "tie-breakers stop" in B.STEP_THREE.replace("Tie", "tie")


# ------------------------------------------------------------------------------------------------ depth (A43 b, G0 v1.4 S23)

def test_deep_is_drawn_from_the_seed_not_from_the_answer(plugin, specs2000):
    """deep = a 4-gate card / a 4-person cascade, stored in structure before the target is drawn; every label sits at
    its normal share inside each depth class, so depth (and meta.deep) carries no gold signal."""
    n = len(specs2000)
    assert sum(s.deep for s in specs2000) / n <= 0.10
    for s in specs2000:
        size = len(s.structure["gates"]) if s.structure["track"] == "gates" else s.structure["people"]
        assert s.structure["deep"] == (size >= T.DEEP_COUNT) and s.deep == s.structure["deep"]
        assert s.depth == (3 if s.deep else 2)
        twin = plugin.derive(s.replace(structure=dict(s.structure)))
        assert twin.deep == s.deep                                  # derive never recomputes it from the answer
    gates = [s for s in specs2000 if s.qform == "ch_outcome"]
    for k in (2, 3):                                                # P(deep | label) is flat: it is a function of k only
        assert not any(s.deep for s in gates if len(s.structure["gates"]) == k)
    out = [plugin.solve_a(s) for s in gates if s.deep]
    assert len(set(out)) == 5 and all(c >= 0.08 * len(out) for c in collections.Counter(out).values())
    claims = [(s, plugin.solve_a(s)) for s in specs2000 if s.qform == "ch_claimant"]
    deep_nobody = [a == T.NONE_KEY for s, a in claims if s.deep]
    other_nobody = [a == T.NONE_KEY for s, a in claims if not s.deep]
    assert abs(sum(deep_nobody) / max(1, len(deep_nobody)) - sum(other_nobody) / len(other_nobody)) <= 0.12
