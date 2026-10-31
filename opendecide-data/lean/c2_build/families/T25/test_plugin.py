"""families/T25/test_plugin.py: in-memory tests for the T25 plugin (A37 f: nothing is written; no Haiku, no network).

  contract        validate_plugin(strict) == [], solver-B independence, G0-lite frozen and <= 200 lines
  hand cases      worked examples with golds computed by hand from the G0 semantics table (the task_ranking example,
                  a copy that outranks, a disagreeing top tie with an agreeing lower tier, an absent top tier, a
                  date-valued attribute, an agreeing tie on yes/no forms): solver A, solver B on the rendered row in
                  every layout, and the construction reading all give the hand gold
  G2 / G3         solver A == solver B and parse == canonical on 5,000 sampled specs (+ every complement form)
  pipeline        every kit program gate (G2, G3, G4, G-SL, G-LEX, G-TW, schema; G15 on a slice) on 750 units,
                  and the spec 4.1 overlay shares
  relations       twins differ in exactly one input slot and the gold moves as constructed (and as the construction
                  reading of the edited bundle says); complements opposite; G4 metamorphic predictions hold
  balance         gold labels inside the G0 section 4 bands on 2,000 specs; trap shares; gold and winner positions
  G-SL            the built-in placeholder skins, wordings and attack lines lint clean; no literal value or verdict
                  word outside the slots of any rendered row
  display plan    (v4) the choice-row plan is label-blind and balanced along the seeds; every (k, shown) cell holds the
                  abstain gold on 1 / k of its rows (bases and partners); gold-is-longest within 2 pp of 1 / k
  card            (v4) the card is the G0 1.1 text; yes/no rows print it as row.card, choice rows open their instructions
                  with it; solver B reads both layouts; the real-token mean is under 800
  determinism     same seed -> same spec and rows
  injected bugs   G2, G3, G-TW and G-SL catch a broken solver B, solver A, renderer, option text, twin and skin
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T25
"""
from __future__ import annotations

import collections
import dataclasses
import datetime as dt
import hashlib
import os
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import gsl, paths, pipeline  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.plugin import Spec  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from families.T25 import fixtures as FX  # noqa: E402
from families.T25 import plugin as P  # noqa: E402
from families.T25 import solver_b as B  # noqa: E402

SAMPLERS = P.T25.SAMPLERS
TRAINING = tuple(s for s in SAMPLERS if s not in P.T25.HELD_OUT_SAMPLERS)
BASE_YN = ("yn_claim", "yn_claim_dneg")
COMPLEMENT_FORMS = {"yn_claim": ("yn_claim_wrong", "yn_claim_not", "yn_claim_other"),
                    "yn_claim_dneg": ("yn_claim_not",)}
LAYOUTS = ("list", "table", "excerpt", "keyed")
CLAIM_FORMS_ALL = P.CLAIM_FORMS
TOKENIZER = Path(os.path.expanduser("~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/"
                                    "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/tokenizer.json"))
D = dt.date


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T25(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs(plugin):
    """2,000 specs: seeds 0-399 (whole seed pairs) x 5 samplers."""
    return [plugin.sample(seed, smp) for seed in range(400) for smp in SAMPLERS]


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


# ------------------------------------------------------------------------------------------------ contract

def test_plugin_meets_the_strict_contract(plugin):
    assert KP.validate_plugin(plugin, strict=True) == []
    assert KP.check_independence(plugin) == []
    assert plugin.PARADIGM_A == "rule_engine" and plugin.PARADIGM_B == "sort_group"
    g0 = Path(plugin.G0_LITE)
    assert len(g0.read_text(encoding="utf-8").splitlines()) <= 200
    assert hashlib.sha256(g0.read_bytes()).hexdigest() == plugin.G0_SHA256


def test_solver_b_shares_no_code_with_solver_a():
    src = Path(B.__file__).read_text(encoding="utf-8")
    assert "families.T25.plugin" not in src and "c2_kit.rules" not in src and "glob_a" not in src
    assert "itertools.groupby" in src and "sorted(" in src               # the other paradigm, really used
    for name in KP.B_FORBIDDEN_NAMES:
        assert not re.search(rf"\b{name}\b", src), name
    a_src = Path(P.__file__).read_text(encoding="utf-8")
    assert "RL.evaluate" in a_src and "import itertools" not in a_src    # solver A is the rule-AST engine


def test_fixture_lexicon_forms_pass_their_unit_tests(ctx):
    reg = ctx.lexicon
    assert all(f.unit_ok for f in reg.forms.values()), {k: f.unit_problems for k, f in reg.forms.items()
                                                         if not f.unit_ok}
    assert reg.gate()["pass"]
    asked = collections.Counter(sk.qform for sk in ctx.skins.values() if sk.kind == "wording")
    assert set(asked) == set(P.QF)


# ------------------------------------------------------------------------------------------------ hand cases

def _hand(plugin, rows, *, pack="filing_fee", scheme="official", layout="list", qform="ch_value", cand=None,
          sampler="S1"):
    """A spec built by hand (no sampler). rows: [(id, tier rank, date, original's position or None, value)]; a
    copy's value is ignored (it is derived from its original). Golds below are computed by hand from G0 S1-S11."""
    pk = P.PACKS[pack]
    seed = _plan_seed(plugin, sampler, qform)
    slots = {"ASKER": S.name_slot("Dana Okafor"), "ORG": S.name_slot("Redfern Council"), "ATTR": S.name_slot(pk.attr)}
    for r in (1, 2, 3):
        slots[f"RANK_{r}"] = P._tier_slot(scheme, r)
    copy_of = []
    for i, (sid, rank, date, of, value) in enumerate(rows, start=1):
        slots[f"S{i}_ID"] = S.id_slot(sid)
        slots[f"S{i}_NAME"] = S.name_slot(P.SOURCE_NAMES[i - 1])
        slots[f"S{i}_TIER"] = P._tier_slot(scheme, rank)
        slots[f"S{i}_DATE"] = S.date_slot(date)
        copy_of.append(of)
        if of is None:
            slots[f"S{i}_VALUE"] = P._value_slot(pk, value)
    if cand is not None:
        slots["CANDIDATE"] = P._value_slot(pk, cand)
    structure = {"pack": pack, "kind": pk.kind, "scheme": scheme, "layout": layout, "n": len(rows),
                 "copy_of": copy_of}
    spec = plugin.derive(Spec("T25", sampler, seed, "T25:S1:c00", qform, slots, structure=structure, pack=f"t25:{pack}"))
    assert plugin._valid(spec)
    return spec


def _plan_seed(plugin, sampler, qform):
    """A hand-built choice spec still gets its display plan from its seed: take the first seed whose plan shows the abstain
    option with k = 3, so a three-source bundle with one or two distinct wrong answers can be listed (a plan that hides the
    option, or asks for k = 4, needs more wrong answers than these bundles have). Yes/no specs have no plan: seed 0."""
    if qform not in P.CHOICE_FORMS:
        return 0
    return next(s for s in range(4000) if plugin._qform_of(sampler, s) == qform
                and plugin._plan(sampler, s, qform).show_abstain and plugin._plan(sampler, s, qform).k == 3)


def _all_three(plugin, ctx, spec):
    """Solver A, solver B on the rendered row in every layout, and the construction reading, on one hand spec."""
    gold = plugin.solve_a(spec)
    assert plugin._group_answer(spec, plugin._top_c(spec)[2]) == gold
    for lay in LAYOUTS:
        s2 = spec.replace(structure={**spec.structure, "layout": lay})
        _check_row(plugin, ctx, s2, plugin.render(s2, ctx))
    return gold


def _em(plugin, spec, name):
    return plugin._answer(spec, spec.qform, frozenset({name}))


def test_hand_case_task_ranking_example(plugin, ctx):
    """task_ranking T25 example: A (official, 2 May): 25; B (community, 9 May): 15; C (official, 2 May, copies A): 25.
    Copies are ignored; official beats community whatever the date: 25, decided by A."""
    rows = [("A", 1, D(2026, 5, 2), None, 2500), ("B", 3, D(2026, 5, 9), None, 1500), ("C", 1, D(2026, 5, 2), 1, 0)]
    assert _all_three(plugin, ctx, _hand(plugin, rows)) == 2500
    assert _all_three(plugin, ctx, _hand(plugin, rows, qform="ch_source")) == "A"
    spec = _hand(plugin, rows)
    assert _em(plugin, spec, "t25_newest_first") == 1500                  # picks the newest
    assert _em(plugin, spec, "t25_tier_reversed") == 1500                 # community read as the top tier
    assert _em(plugin, spec, "t25_count_copies") == 2500                  # the copy agrees: no harm here
    assert _em(plugin, _hand(plugin, rows, qform="ch_source"), "t25_count_copies") is None   # two sources, no single
    for cand, want in ((2500, 1), (1500, 0)):
        assert _all_three(plugin, ctx, _hand(plugin, rows, qform="yn_claim", cand=cand)) == want
        assert _all_three(plugin, ctx, _hand(plugin, rows, qform="yn_claim_wrong", cand=cand)) == 1 - want


def test_hand_case_copy_that_outranks_is_ignored(plugin, ctx):
    """gold > silver > bronze. No independent gold source: the copy C (gold, newest silver-beating) of B is ignored.
    T* = silver; D* = 1 March (A); D (bronze) is newer but less reliable: 30.00, from A."""
    rows = [("A", 2, D(2025, 3, 1), None, 3000), ("B", 2, D(2025, 2, 20), None, 3500),
            ("C", 1, D(2025, 3, 5), 2, 0), ("D", 3, D(2025, 4, 1), None, 4000)]
    spec = _hand(plugin, rows, pack="membership", scheme="metal")
    assert _all_three(plugin, ctx, spec) == 3000
    assert _all_three(plugin, ctx, _hand(plugin, rows, pack="membership", scheme="metal", qform="ch_source")) == "A"
    assert _em(plugin, spec, "t25_count_copies") == 3500                  # the copy would win if counted
    assert _em(plugin, spec, "t25_newest_first") == _em(plugin, spec, "t25_newest_any") == 4000
    assert _em(plugin, spec, "t25_oldest_in_tier") == 3500                # B is the older silver source
    assert "copy_trap" in plugin._tags(spec, "clear") and "newest_loses" in plugin._tags(spec, "clear")


def test_hand_case_disagreeing_tie_is_not_broken_by_lower_tiers(plugin, ctx):
    """primary > secondary > tertiary. A and B are primary, same date, 20 vs 23 kg: not determinable, although the
    secondary sources (one on the same day) and the majority say 23. If B also said 20 the tie would agree: 20."""
    rows = [("A", 1, D(2025, 6, 10), None, 20), ("B", 1, D(2025, 6, 10), None, 23),
            ("C", 2, D(2025, 6, 10), None, 23), ("D", 2, D(2025, 7, 1), None, 23)]
    spec = _hand(plugin, rows, pack="baggage", scheme="order")
    assert _all_three(plugin, ctx, spec) == P.ABSTAIN
    assert _all_three(plugin, ctx, _hand(plugin, rows, pack="baggage", scheme="order", qform="ch_source")) == P.ABSTAIN
    assert _em(plugin, spec, "t25_tie_first_listed") == 20 and _em(plugin, spec, "t25_tie_last_listed") == 23
    assert _em(plugin, spec, "t25_majority") == 23 and _em(plugin, spec, "t25_newest_first") == 23
    agree = [("A", 1, D(2025, 6, 10), None, 20), ("B", 1, D(2025, 6, 10), None, 20)] + rows[2:]
    assert _all_three(plugin, ctx, _hand(plugin, agree, pack="baggage", scheme="order")) == 20
    with pytest.raises(KP.ContractError):                                 # ch_source is never asked on an agreeing tie
        plugin.solve_a(_hand(plugin, agree, pack="baggage", scheme="order", qform="ch_source"))
    flipped = [("A", 1, D(2025, 6, 10), None, 20), ("B", 1, D(2025, 6, 9), None, 23)] + rows[2:]
    assert _all_three(plugin, ctx, _hand(plugin, flipped, pack="baggage", scheme="order")) == 20   # one day apart


def test_hand_case_card_order_and_date_values(plugin, ctx):
    """blue > green > grey (only the card says so). No blue source: T* = green; D* = 10 January (A). The source date
    decides, never the latest deadline value (C states the latest deadline but is older). A copy listed first, of a
    source listed later, dated the same day as its original, is still ignored."""
    rows = [("A", 2, D(2026, 1, 10), None, D(2026, 3, 31)), ("B", 3, D(2026, 2, 1), None, D(2026, 4, 30)),
            ("C", 2, D(2026, 1, 9), None, D(2026, 5, 15))]
    spec = _hand(plugin, rows, pack="deadline", scheme="colour")
    assert _all_three(plugin, ctx, spec) == "2026-03-31"
    assert _em(plugin, spec, "t25_tier_reversed") == "2026-04-30" and _em(plugin, spec, "t25_oldest_in_tier") == \
        "2026-05-15"
    lead = [("X", 1, D(2026, 2, 1), 3, 0), ("A", 2, D(2026, 1, 10), None, D(2026, 3, 31)),
            ("B", 3, D(2026, 2, 1), None, D(2026, 4, 30))]
    spec2 = _hand(plugin, lead, pack="deadline", scheme="colour", qform="ch_source")
    assert _all_three(plugin, ctx, spec2) == "A"
    assert _em(plugin, spec2, "t25_count_copies") == "X"                  # the blue copy would win if counted


def test_hand_case_yes_no_forms_on_an_agreeing_tie(plugin, ctx):
    """high > medium > low. A and B (high, same date) both say 14 days: 14. C (medium, newer) says 21."""
    rows = [("A", 1, D(2025, 5, 5), None, 14), ("B", 1, D(2025, 5, 5), None, 14), ("C", 2, D(2025, 6, 1), None, 21)]
    kw = dict(pack="notice", scheme="level")
    for qform, cand, want in (("yn_claim", 14, 1), ("yn_claim", 21, 0), ("yn_claim_not", 21, 1),
                              ("yn_claim_not", 14, 0), ("yn_claim_other", 14, 0), ("yn_claim_other", 21, 1),
                              ("yn_claim_wrong", 21, 1), ("yn_claim_dneg", 14, 1), ("yn_claim_dneg", 21, 0)):
        assert _all_three(plugin, ctx, _hand(plugin, rows, qform=qform, cand=cand, **kw)) == want, (qform, cand)


def test_parser_refuses_malformed_bundles(plugin, ctx):
    """Solver B refuses a copy that states another value, a copy dated before its original, an unknown tier name and
    a repeated id (G0 S3); the well-formed row parses."""
    rows = [("A", 1, D(2026, 5, 2), None, 2500), ("B", 3, D(2026, 5, 9), None, 1500), ("C", 1, D(2026, 5, 3), 1, 0)]
    rr = plugin.render(_hand(plugin, rows), ctx)
    good = rr.row["state"]
    B.parse(rr.row, ctx)
    lines = good.split("\n")
    k = next(i for i, ln in enumerate(lines) if "copied from" in ln)
    fee = S.render(S.cents_slot(1500), rr.forms["S1_VALUE"])
    other_value = "\n".join(lines[:k] + [re.sub(r"is .+\.$", f"is {fee}.", lines[k])] + lines[k + 1:])
    early = S.render(S.date_slot(D(2026, 5, 1)), rr.forms["S3_DATE"])
    predates = "\n".join(lines[:k] + [re.sub(r"dated [^;]+;", f"dated {early};", lines[k])] + lines[k + 1:])
    bads = (other_value, predates, good.replace("tier community", "tier unknown"),
            good.replace("- Source B:", "- Source A:"))
    for bad in bads:
        assert bad != good
        with pytest.raises(B.ParseError):
            B.parse(dict(rr.row, state=bad), ctx)


# ------------------------------------------------------------------------------------------------ G2 / G3

def test_solver_a_equals_solver_b_on_5000_specs(plugin, ctx):
    seen = collections.Counter()
    for seed in range(1000):
        for smp in SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            _check_row(plugin, ctx, spec, rr)
            seen[spec.qform] += 1
            for q2 in COMPLEMENT_FORMS.get(spec.qform, ()):
                s2 = spec.replace(qform=q2)
                r2 = plugin.render(s2, ctx, skin=ctx.skin(rr.skin_id), forms=rr.forms)
                _check_row(plugin, ctx, s2, r2)
                assert r2.answer == 1 - rr.answer
                seen[q2] += 1
    assert sum(seen[q] for q in ("ch_value", "ch_source") + BASE_YN) == 5000
    # W9: yn_claim_dneg is no longer drawn by sample() (all its wordings are A43 f forms; its 0.04 share went to yn_claim);
    # the form itself still renders and solves, checked on yn_claim specs below
    assert set(seen) == set(plugin.QFORMS) - {"yn_claim_dneg"} and min(seen.values()) > 150, seen
    assert seen["yn_claim_dneg"] == 0
    for seed in range(60):
        spec = plugin.sample(seed, "S1")
        if spec.qform == "yn_claim":
            sd = spec.replace(qform="yn_claim_dneg")
            _check_row(plugin, ctx, sd, plugin.render(sd, ctx))


def test_every_unit_passes_the_program_gates(plugin, ctx):
    units, kinds = [], collections.Counter()
    for seed in range(150):
        for smp in SAMPLERS:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=(seed < 4))
            assert res.ok, (seed, smp, res.problems)
            units.append(res)
            for r in res.rows:
                kinds[(r["qtype"], r["role"])] += 1
                assert R.validate_row(r) == []
                if smp == "S5":
                    assert r["meta"]["dev_only"]
                else:
                    assert R.validate_row(r, training=True) == [] or r["meta"]["dev_only"]
    rep = pipeline.overlay_report(units, plugin)
    assert 0.45 <= rep["yes_no"] / rep["rows"] <= 0.55, rep
    assert rep["complement_share_of_yes_no"] >= 0.20 and rep["non_syntactic_share_of_pairs"] >= 0.30, rep
    assert 0.20 <= rep["twin_share"] <= 0.25, rep
    assert 0.05 <= rep["equiv_share"] <= 0.10 and 0.01 <= rep["attack_share"] <= 0.06, rep
    assert 0.45 <= rep["yes_rate"] <= 0.55, rep
    assert rep["abstain"]["pass"] and rep["abstain"]["wrong_share"] >= 0.60, rep["abstain"]   # 1 - 1 / k: 67% / 75%
    for role in ("complement", "twin", "equiv", "attack"):
        assert sum(v for (q, r), v in kinds.items() if r == role) > 10, (role, kinds)
    rows = [r for u in units for r in u.rows if r["qtype"] == "noul"]
    import negcount
    ks = [negcount.count(r["instructions"].split("\n\n")[-1]) for r in rows]
    assert sum(k.k_syn >= 1 for k in ks) / len(ks) >= 0.10 and sum(k.k_syn >= 2 for k in ks) / len(ks) >= 0.02


# ------------------------------------------------------------------------------------------------ relations

def test_relations_are_valid(plugin, specs):
    twins, comps, meta = collections.Counter(), 0, collections.Counter()
    for spec in specs:
        base = plugin.solve_a(spec)
        for prop in plugin.relations(spec):
            if prop.kind == "twin":
                twin = plugin.derive(prop.spec)
                assert slot_diff(spec, twin) == {prop.changed_slot}
                assert twin.structure == spec.structure and twin.qform == spec.qform
                assert plugin._valid(twin)
                got = plugin.solve_a(twin)
                assert got == prop.expect != base, (spec.seed, spec.sampler, prop.note)
                # the edit's designed group is the construction reading of the edited bundle
                assert plugin._group_answer(twin, plugin._top_c(twin)[2]) == prop.expect, prop.note
                twins[prop.note] += 1
            elif prop.kind == "complement":
                partner = spec.replace(qform=prop.qform)
                q, q2 = plugin.QFORMS[spec.qform], plugin.QFORMS[prop.qform]
                assert q.predicate == q2.predicate and q.polarity == -q2.polarity
                assert plugin.solve_a(partner) == 1 - base
                comps += 1
            elif prop.kind == "metamorphic":
                moved = plugin.derive(prop.spec)
                assert plugin._valid(moved), prop.note
                assert plugin.solve_a(moved) == (base if prop.expect == "same" else prop.expect), prop.note
                meta[prop.note] += 1
            elif prop.kind == "equiv" and prop.spec is not None:
                assert plugin.canonical(prop.spec) == plugin.canonical(spec)
                assert prop.spec.structure["layout"] in P.TRAIN_LAYOUTS
    for kind in ("rival_newer", "rival_tie", "rival_promote", "member_back", "member_forward", "member_value"):
        assert twins[kind] > 5, twins
    assert sum(twins.values()) >= 0.35 * len(specs), twins
    assert comps > 300 and min(meta.values()) > 100 and len(meta) == 7, meta


def test_twins_change_one_slot_in_the_rendered_text(plugin, ctx):
    """G-TW on the text: outside the changed slot (and the copies' values it feeds) the twin row is identical, and
    the twin keeps its own call_id."""
    checked = collections.Counter()
    for seed in range(200):
        for smp in ("S1", "S2"):
            spec = plugin.sample(seed, smp)
            if not any(p.kind == "twin" for p in plugin.relations(spec)):
                continue
            res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
            assert res.ok, res.problems
            rows = {r["role"]: r for r in res.rows}
            if "twin" in rows:
                assert rows["twin"]["meta"]["twin_of"] == rows["base"]["id"]
                assert rows["twin"]["call_id"] != rows["base"]["call_id"]
                assert rows["twin"]["gold"] != rows["base"]["gold"]
                checked[rows["base"]["qtype"]] += 1
    assert checked["choice"] > 40 and checked["noul"] > 20, checked


def test_bundles_keep_the_g0_invariants(plugin, specs):
    for spec in specs:
        assert plugin._valid(spec)
        st, v = spec.structure, spec.env()
        assert 3 <= st["n"] <= 5 and st["layout"] == P.LAYOUT[spec.sampler]
        for i, j in enumerate(st["copy_of"], start=1):
            if j is not None:
                assert st["copy_of"][j - 1] is None and v[f"S{i}_DATE"] >= v[f"S{j}_DATE"]
                assert v[f"S{i}_VALUE"] == v[f"S{j}_VALUE"]
        if spec.qform in CLAIM_FORMS_ALL:
            assert "CANDIDATE" in spec.slots and "tie_disagree" not in spec.tags
            values = {v[f"S{i}_VALUE"] for i in range(1, st["n"] + 1)}
            assert v["CANDIDATE"] in values                               # G0 S11: always a stated value
        else:
            assert "CANDIDATE" not in spec.slots
        if spec.qform == "ch_source":
            assert "tie_agree" not in spec.tags



# ------------------------------------------------------------------------------------------------ balance

def test_gold_balance_on_2000_specs(plugin, specs):
    yes = collections.defaultdict(list)
    for spec in specs:
        if spec.qform in BASE_YN:
            yes[spec.qform].append(plugin.solve_a(spec))
    for q, golds in yes.items():                                  # exact by seed pairs (G0 section 4)
        assert abs(sum(golds) / len(golds) - 0.5) <= 0.03, (q, sum(golds), len(golds))
    choice = [s for s in specs if s.qform in P.CHOICE_FORMS]
    abst = sum(plugin.solve_a(s) == P.ABSTAIN for s in choice) / len(choice)
    assert 0.15 <= abst <= 0.25, abst
    qf = collections.Counter(s.qform for s in specs)
    assert 0.38 <= sum(qf[q] for q in BASE_YN) / len(specs) <= 0.46, qf
    tiers = collections.Counter(next(t for t in s.tags if t.startswith("top_t")) for s in specs)
    for t, want in (("top_t1", 0.50), ("top_t2", 0.35), ("top_t3", 0.15)):
        assert abs(tiers[t] / len(specs) - want) <= 0.05, tiers
    assert sum(s.deep for s in specs) / len(specs) <= 0.10


def test_winner_position_is_uniform(plugin):
    """The listed position of the single deciding source is a seeded shuffle (no position prior)."""
    pos = collections.defaultdict(collections.Counter)
    for seed in range(600):
        for smp in TRAINING:
            spec = plugin.sample(seed, smp)
            _, _, G = plugin._top_c(spec)
            if len(G) == 1:
                pos[spec.structure["n"]][G[0]] += 1
    for n, c in pos.items():
        m = sum(c.values()) / n
        if m >= 60:
            assert all(abs(c[i] - m) <= 0.30 * m for i in range(1, n + 1)), (n, c)


def test_trap_shares_on_2000_specs(plugin, specs):
    tags = collections.Counter(t for s in specs for t in s.tags)
    share = {k: v / len(specs) for k, v in tags.items()}
    for t, want in (("newest_loses", 0.30), ("copy_trap", 0.25), ("false_tie", 0.03), ("majority_wrong", 0.15),
                    ("same_day_tiers", 0.10), ("near_miss", 0.20)):
        assert share.get(t, 0) >= want, (t, share)
    ties = share.get("tie_agree", 0) + share.get("tie_disagree", 0)
    assert 0.20 <= ties <= 0.32 and 0.35 <= share.get("tie_agree", 0) / ties <= 0.65, share
    assert share.get("date_separates", 0) > 0.02 and share.get("first_listed_wrong", 0) > 0.4, share


def test_options_come_from_named_error_models(plugin, ctx, specs):
    positions = collections.defaultdict(collections.Counter)
    used = collections.Counter()
    for spec in specs:
        if spec.qform not in P.CHOICE_FORMS:
            continue
        rr = plugin.render(spec, ctx)
        os_ = rr.option_set
        positions[len(os_.options)][os_.gold_index] += 1
        assert os_.abstain_shown == os_.meta["plan"]["show_abstain"]   # the plan decides; always shown when it is gold
        assert not os_.meta["gold_is_abstain"] or os_.abstain_shown
        for o in os_.options:
            if o.role == "error":
                assert o.err and set(o.err) <= set(P.VALUE_EM)
                used.update(o.err)
            else:
                assert o.role in ("gold", "abstain")
    for k, c in positions.items():
        m = sum(c.values()) / k
        if m >= 50:
            assert all(abs(c[i] - m) <= 0.35 * m for i in range(k)), (k, c)
    # t25_tier_only only ever answers the gold or "not determinable", so it backs the abstain option, never a value
    assert set(used) == set(P.VALUE_EM) - {"t25_tier_only"}, used


def test_yes_no_candidates_are_misreadings(plugin, specs):
    """A 'no' claim names the value some error model settles on, never an arbitrary value (G0 S11)."""
    checked = 0
    for spec in specs:
        if spec.qform not in BASE_YN or plugin.solve_a(spec) == 1:
            continue
        cand = S.canonical(spec.slots["CANDIDATE"])
        assert any((plugin._outcome(spec, frozenset({m})) or (None, None))[1] == cand for m in P.VALUE_EM)
        checked += 1
    assert checked > 150


def test_rows_fit_the_length_caps(plugin, ctx):
    sizes = []
    for seed in range(200):
        for smp in SAMPLERS:
            rr = plugin.render(plugin.sample(seed, smp), ctx)
            sizes.append(R.approx_tokens(rr.row))
    assert max(sizes) <= R.MAX_TOKENS                             # the real-token mean is tested below


@pytest.mark.skipif(not TOKENIZER.is_file(), reason="local Qwen tokenizer file not cached")
def test_real_token_mean_is_at_most_800(plugin, ctx):
    from tokenizers import Tokenizer
    tok = Tokenizer.from_file(str(TOKENIZER))

    def n(t):
        return len(tok.encode(t or "", add_special_tokens=False).ids)

    sizes = []
    for seed in range(120):
        for smp in SAMPLERS:
            r = plugin.render(plugin.sample(seed, smp), ctx).row
            sizes.append(n(r["state"]) + n(r["card"]) + 2 * n(r["instructions"])
                         + sum(n(o) + 2 for o in (r["options"] or [])))
    assert sum(sizes) / len(sizes) <= 800 and max(sizes) <= 2000, (sum(sizes) / len(sizes), max(sizes))


# ------------------------------------------------------------------------------------------------ G-SL

def _word_forms(words) -> set:
    return gsl._label_forms(tuple(words))


def test_builtin_placeholder_skins_lint_clean(plugin, ctx):
    linted = 0
    label = _word_forms(plugin.LABEL_WORDS)
    verdict = _word_forms(plugin.VERDICT_WORDS)
    for sk in ctx.skins.values():
        if sk.author_mode == "T":
            v = gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                                  name_allow=plugin.NAME_ALLOW)
            assert v == [], (sk.skin_id, v)
        else:
            assert gsl.lint_freeform(sk.text, dict(sk.brief), label_words=plugin.LABEL_WORDS) == []
        linted += 1
        words = {w.lower() for w in re.findall(r"[A-Za-z]+", K.PH_RE.sub(" ", sk.text))}
        if sk.kind == "skin":                                     # narratives: no verdict and no decisive-fact word
            assert not words & label, (sk.skin_id, words & label)
        elif sk.kind == "attack":                                 # pressure lines: no verdict word
            assert not words & verdict, (sk.skin_id, words & verdict)
    assert linted == len(ctx.skins) >= 27


def test_no_literal_value_or_verdict_outside_slots(plugin, ctx):
    """Every number, date, amount, name and id of a rendered row sits inside a slot span; the card and the source
    block carry no digit, month or weekday of their own, and the state no verdict word."""
    months = "|".join(S.MONTHS + S.WEEKDAYS)
    verdict = re.compile(r"\b(?:" + "|".join(sorted(_word_forms(plugin.VERDICT_WORDS), key=len, reverse=True))
                         + r")\b", re.I)
    for seed in range(120):
        for smp in SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            values = {str(s.value) for s in spec.all_slots().values() if s.kind in ("name", "id")
                      and len(str(s.value)) >= 3}
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
                assert not re.search(r"\d", rest), (seed, smp, fld)
                assert not re.search(rf"\b(?:{months})\b", rest), (seed, smp, fld)
                for v in values:
                    assert not re.search(r"(?<![\w-])" + re.escape(v) + r"(?![\w-])", rest), (v, seed, smp)
                if fld == "state":
                    assert not verdict.search(rest), (seed, smp, verdict.search(rest))
            for tpl in (plugin.block_template(spec), P.CLAIM_TPL, P.CARD):
                lit = K.PH_RE.sub("", tpl)
                assert not re.search(r"\d", lit) and not re.search(rf"\b(?:{months})\b", lit)
            assert not verdict.search(K.PH_RE.sub("", plugin.block_template(spec)))


# ------------------------------------------------------------------------------------------------ determinism

def test_sampling_and_rendering_are_deterministic(plugin, ctx):
    for seed in (0, 7, 31, 202):
        for smp in SAMPLERS:
            a, b = plugin.sample(seed, smp), plugin.sample(seed, smp)
            assert a.structure_hash() == b.structure_hash() and a.tags == b.tags
            assert plugin.render(a, ctx).row == plugin.render(b, ctx).row
    u1 = pipeline.build_unit(plugin, plugin.sample(17, "S4"), ctx, run_g15=False).rows
    u2 = pipeline.build_unit(plugin, P.T25(lexicon=ctx.lexicon).sample(17, "S4"), ctx, run_g15=False).rows
    assert u1 == u2
    hashes = {plugin.sample(seed, "S1").structure_hash() for seed in range(200)}
    assert len(hashes) == 200


def test_nothing_is_written(plugin, ctx):
    here = Path(__file__).resolve().parent
    before = sorted(p.name for p in here.iterdir())
    pipeline.build_unit(plugin, plugin.sample(3, "S1"), ctx, run_g15=False)
    assert sorted(p.name for p in here.iterdir()) == before
    if not paths.a38_frozen():
        with pytest.raises(paths.DataBeforeFreeze):
            paths.write_jsonl(paths.C2_PARTS / "t25_never.jsonl", [])


# ------------------------------------------------------------------------------------------------ injected bugs

def _failures(plugin, ctx, n=40, samplers=TRAINING):
    out = collections.Counter()
    for seed in range(n):
        for smp in samplers:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            for g, _ in res.problems:
                out[g] += 1
    return out


def test_g2_catches_a_solver_b_that_breaks_ties(plugin, ctx, monkeypatch):
    real = B._head_group                                           # B takes the first member of a tied group
    monkeypatch.setattr(B, "_head_group", lambda view: real(view)[:1])
    assert _failures(plugin, ctx)["G2"] > 0


def test_g2_catches_a_solver_b_that_counts_copies(plugin, ctx, monkeypatch):
    real = B._head_group

    def counted(view):
        return real(dict(view, sources=[dict(s, copy_of=None) for s in view["sources"]]))

    monkeypatch.setattr(B, "_head_group", counted)
    assert _failures(plugin, ctx)["G2"] > 0


def test_g2_catches_a_solver_a_that_puts_date_before_tier(plugin, ctx, monkeypatch):
    specs = [plugin.sample(seed, smp) for seed in range(120) for smp in TRAINING]
    specs = [s for s in specs if "newest_loses" in s.tags]
    rendered = [(s, plugin.render(s, ctx)) for s in specs]
    real = P.T25._outranks

    def newest(self, t, s, mods):                                  # the plain rule reads the date first
        return real(self, t, s, mods or frozenset({"t25_newest_first"}))

    monkeypatch.setattr(P.T25, "_outranks", newest)
    g2 = 0
    for s, rr in rendered:
        try:
            probs = pipeline.check_rendered(plugin, s, rr, ctx, run_g15=False)
        except KP.ContractError:
            g2 += 1                                                # solver A finds no answer: a G2 stop too
            continue
        g2 += sum(g == "G2" for g, _ in probs)
    assert g2 > 0
    with pytest.raises(KP.ContractError):                          # and the sampler's own guard refuses it
        for seed in range(200):
            plugin.sample(seed, "S1")


def test_g2_catches_a_mislabelled_option(plugin, ctx, monkeypatch):
    real = P.T25._value_text

    def off_by_one(self, spec, forms):
        text = real(self, spec, forms)
        return lambda x: text(x + 1) if isinstance(x, int) else text(x)

    monkeypatch.setattr(P.T25, "_value_text", off_by_one)
    f = _failures(plugin, ctx, 60)
    assert f["G2"] + f["G3"] > 0


def test_g3_catches_a_renderer_that_drops_the_copy_marker(plugin, ctx, monkeypatch):
    real = P.T25.block_template

    def dropped(self, spec):
        return re.sub(r"copied from (?:Source )?\{S\d+_ID\}", "independent", real(self, spec))

    monkeypatch.setattr(P.T25, "block_template", dropped)
    f = _failures(plugin, ctx)
    assert f["G3"] + f["G2"] > 0 and f["G3"] > 0


def test_g3_catches_a_card_with_another_tier_order(plugin, ctx, monkeypatch):
    monkeypatch.setattr(P, "CARD", P.CARD.replace("{RANK_1}; then {RANK_2}", "{RANK_2}; then {RANK_1}"))
    assert _failures(plugin, ctx, 20)["G3"] > 0


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    real = P.T25._twin

    def flipped(self, spec):
        t = real(self, spec)
        if t is None or spec.qform in P.CHOICE_FORMS:
            return t
        return dataclasses.replace(t, expect=1 - t.expect)

    monkeypatch.setattr(P.T25, "_twin", flipped)
    assert _failures(plugin, ctx)["G-TW"] > 0


def test_gsl_catches_a_leaky_skin(plugin, ctx):
    leaky = dataclasses.replace(ctx.skin("SK-CHAT-1"), skin_id="SK-LEAK",
                                text=ctx.skin("SK-CHAT-1").text + " The newest notice wins.")
    c2 = dataclasses.replace(ctx, skins={**ctx.skins, "SK-LEAK": leaky})
    spec = plugin.sample(5, "S1")
    rr = plugin.render(spec, c2, skin=leaky)
    assert any(g == "G-SL" for g, _ in pipeline.check_rendered(plugin, spec, rr, c2, run_g15=False))


# ------------------------------------------------------------------------------------------------ display plan (v4)

def _choice_sets(c, pl, seeds, samplers=("S1", "S2", "S3", "S4")):
    """{qform: [OptionSet]} of every choice row of the units (bases, twins, equiv, attack partners)."""
    sets = collections.defaultdict(list)
    for seed in seeds:
        for smp in samplers:
            spec = pl.sample(seed, smp)
            if spec.qform not in P.CHOICE_FORMS:
                continue
            res = pipeline.build_unit(pl, spec, c, run_g15=False)
            assert res.ok, res.problems
            for rr in res.rendered:
                if rr.option_set is not None:
                    sets[spec.qform].append(rr.option_set)
    return sets


def test_option_count_and_abstain_display_carry_no_label():
    """The display plan (k, abstain shown, abstain gold, position) is drawn from the row key before any structure; a spec
    the plan cannot fill is resampled, never re-tried with a smaller k or with the abstain option forced on (ch_value
    abstain gold was 0% at k = 2, 22% at k = 3 and 39% at k = 4). Over all emitted rows: the abstain option is gold on
    about 1 / k of the rows that show it in every (k, shown) cell with >= 100 rows, never gold on a row that hides it,
    wrong on >= 50% of the rows that show it, and gold on 15-25% of the choice rows (spec 3.17)."""
    from c2_kit import distractors as DI
    c = FX.ctx()
    pl = P.T25(lexicon=c.lexicon)
    sets = _choice_sets(c, pl, range(600))
    assert set(sets) == set(("ch_value", "ch_source"))
    every = [s for ss in sets.values() for s in ss]
    assert 0.15 <= sum(bool(s.meta["gold_is_abstain"]) for s in every) / len(every) <= 0.25
    for q, ss in sets.items():
        for (k, sh), v in DI.abstain_cells(ss).items():
            assert sh or v["abstain_gold"] == 0
            if sh and v["rows"] >= 100:
                assert v["wrong_share"] >= 0.5, (q, k, v)
                assert abs(v["abstain_gold"] / v["rows"] - 1 / k) <= 0.06, (q, k, v)


def test_plan_report_over_all_rows_passes_the_g10_views():
    """plan_report (the pilot's G10 views on the option sets, partner rows included): abstain gold 1 / k per cell, gold
    position uniform per k, gold-is-longest within 2 pp of 1 / k. (Its length-rank view applies to length_balance only.)"""
    from c2_kit import choiceplan as CP
    c = FX.ctx()
    pl = P.T25(lexicon=c.lexicon)
    sets = [s for ss in _choice_sets(c, pl, range(400)).values() for s in ss]
    rep = CP.plan_report(sets)
    assert rep["rows"] > 900
    bad = [f for f in rep["failing"] if not f.startswith("length rank")]
    assert bad == [], rep
    assert abs(rep["longest_gold_pp"]) <= 2.0, rep["longest_gold_pp"]


def test_the_plan_is_label_blind_and_balanced_along_the_seeds():
    """_plan reads the sampler, the seed and the form only (a fresh plugin gives the same plan). Along any run of
    consecutive seeds every (k, shown) cell holds the abstain gold on 1 / k of its rows to within one row, every k
    holds every position to within one row, the abstain option is never gold on a hidden row, and the sampled spec's
    gold agrees with its plan."""
    c = FX.ctx()
    a, b = P.T25(lexicon=c.lexicon), P.T25(lexicon=c.lexicon)
    for smp in ("S1", "S3"):
        cells = collections.defaultdict(list)
        for seed in range(7000, 7600):
            q = a._qform_of(smp, seed)
            if q not in P.CHOICE_FORMS:
                continue
            pa = a._plan(smp, seed, q)
            assert pa == b._plan(smp, seed, q) and pa.k in (P.VALUE_K if q == "ch_value" else P.SOURCE_K)
            assert not (pa.gold_abstain and not pa.show_abstain)
            cells[(q, pa.k, pa.show_abstain)].append(pa)
            if seed % 25 == 0:
                spec = a.sample(seed, smp)
                assert (a.solve_a(spec) == P.ABSTAIN) == pa.gold_abstain and spec.qform == q
        for (q, k, shown), plans in cells.items():
            if shown and len(plans) >= 12:
                assert abs(sum(x.gold_abstain for x in plans) - len(plans) / k) <= 2.0, (smp, q, k, len(plans))
        for q in P.CHOICE_FORMS:
            for k in set(kk for (qq, kk, _) in cells if qq == q):
                allp = [x for (qq, kk, _), v in cells.items() if (qq, kk) == (q, k) for x in v]
                counts = collections.Counter(x.pos for x in allp)
                if len(allp) >= 4 * k:
                    assert max(counts.values()) - min(counts[i] for i in range(k)) <= 3, (smp, q, k, counts)


def test_twins_adapt_the_plan_to_their_own_gold():
    """A twin that moves the gold onto the abstain key shows the abstain option; one that moves it off keeps the option
    list's k and the gold position (choiceplan.for_gold)."""
    c = FX.ctx()
    pl = P.T25(lexicon=c.lexicon)
    onto = off = 0
    for seed in range(260):
        for smp in ("S1", "S2"):
            spec = pl.sample(seed, smp)
            if spec.qform not in P.CHOICE_FORMS:
                continue
            res = pipeline.build_unit(pl, spec, c, run_g15=False)
            assert res.ok, res.problems
            by = {rr.row["role"]: rr for rr in res.rendered}
            if "twin" not in by:
                continue
            b, t = by["base"].option_set, by["twin"].option_set
            assert len(b.options) == len(t.options) or t.meta["gold_is_abstain"] != b.meta["gold_is_abstain"]
            if t.meta["gold_is_abstain"] and not b.meta["gold_is_abstain"]:
                assert t.abstain_shown and len(t.options) == len(b.options) and t.gold_index == b.gold_index
                onto += 1
            if b.meta["gold_is_abstain"] and not t.meta["gold_is_abstain"]:
                assert t.abstain_shown and len(t.options) == len(b.options) and t.gold_index == b.gold_index
                off += 1
    assert onto > 5 and off > 5, (onto, off)


# ------------------------------------------------------------------------------------------------ card (v4)

def _g0_card(g0_text: str) -> str:
    """The card text of G0 section 1.1: the indented block, wrapped items re-joined."""
    block = g0_text.split("### 1.1 Card", 1)[1].split("\n\n", 2)[1]
    items = []
    for ln in block.split("\n"):
        assert ln.startswith("    ")
        s = ln[4:]
        if s.startswith(" ") and items:                        # a wrapped continuation (indented under its item)
            items[-1] += " " + s.strip()
        else:
            items.append(s)
    return "\n".join(items)


def test_the_card_is_the_g0_text_in_the_plugin_and_in_solver_b():
    g0 = Path(P.T25.G0_LITE).read_text(encoding="utf-8")
    assert _g0_card(g0) == P.CARD == B._CARD
    assert P.CARD.endswith(P.CLOSED_WORLD) and P.CLOSED_WORLD == B._CW == P.T25.CLOSED_WORLD_SENTENCE
    for slot in ("{ATTR}", "{RANK_1}", "{RANK_2}", "{RANK_3}"):
        assert slot in P.CARD


def test_yes_no_rows_hold_the_card_in_row_card_and_choice_rows_in_the_instructions(plugin, ctx):
    """cards.place_rules: the served prompt prints row.card once and row.instructions twice, so a yes/no row keeps the
    rules in row.card (its instructions are the question) and a choice row opens its instructions with them. Solver B
    reads both through cards.split_rules; the rendered card is the template with its three slots filled."""
    from c2_kit import cards
    seen = collections.Counter()
    for seed in range(60):
        for smp in SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            row = rr.row
            rules, question = cards.split_rules(row)
            filled = K.fill(P.CARD, spec.all_slots(), rr.forms).text
            assert rules == filled and "\n\n" not in question and question.endswith("?")
            if row["qtype"] == "noul":
                assert row["card"] == filled and row["instructions"] == question
                assert row["meta"]["defs_style"] == "rules_in_card_full"
            else:
                assert row["card"] is None and row["instructions"] == filled + "\n\n" + question
                assert row["meta"]["defs_style"] == "rules_in_instructions_full"
            seen[row["qtype"]] += 1
            view = B.parse(row, ctx)
            assert view["attr"] == spec.all_slots()["ATTR"].value
    assert seen["noul"] > 30 and seen["choice"] > 30


def test_solver_b_refuses_a_card_that_moved_or_changed(plugin, ctx):
    spec = plugin.sample(3, "S1")
    while spec.qform in P.CHOICE_FORMS:
        spec = plugin.sample(spec.seed + 2, "S1")
    row = plugin.render(spec, ctx).row
    assert row["card"] and B.parse(row, ctx)
    swapped = dict(row, card=row["card"].replace("most reliable first", "least reliable first"))
    with pytest.raises(B.ParseError):
        B.parse(swapped, ctx)
    with pytest.raises(B.ParseError):                                # the rules in neither place
        B.parse(dict(row, card=None), ctx)


# ------------------------------------------------------------------------------------------------ polarity (v4)

def test_plugin_opts_into_the_polarity_rule_and_loses_no_fixture_wording(plugin, ctx):
    from c2_kit import polarity
    assert plugin.POLARITY_CHECK and polarity.config_problems(plugin) == []
    assert plugin.ctx_for(None, ctx) is ctx and plugin.quarantined_wordings(ctx) == {}
    for sk in ctx.skins.values():
        if sk.kind == "wording":
            assert polarity.form_problems(plugin, sk.qform, sk.text) == [], sk.text
