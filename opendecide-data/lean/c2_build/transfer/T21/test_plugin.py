"""transfer/T21/test_plugin.py: in-memory tests for the T21 plugin (A37 f: no file is written; no Haiku, no network).

  contract      validate_plugin(strict) == [], solver-B independence, frozen G0-lite, the G0 card quote (H21)
  hand gold     agreements with answers worked out by hand from the G0 semantics table (a switch-off that covers, a
                switch-back with another cause, a switch-back that covers, a counter clause, a defined term, a decoy
                rule, a cause-limited switch-off): solver A on the spec, solver B (set algebra) on the parsed rendered
                row, and the hand answer agree
  A == B        >= 1,500 sampled units through every kit program gate (G2, G3, G4, G-SL, G-LEX, G-TW, schema; G15 on a
                slice); twins flip as constructed; metamorphic relations hold
  balance       yes rate, deciding depth spread, trap tags, deep share; every row dev-only
  injected bugs G2 catches a solver B that ignores causes; G-SL catches a leaky skin
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/transfer/T21
"""
from __future__ import annotations

import collections
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import gsl, pipeline  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.plugin import Spec  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from transfer.T21 import card as CARD_MOD  # noqa: E402
from transfer.T21 import fixtures as FX  # noqa: E402
from transfer.T21 import plugin as P  # noqa: E402
from transfer.T21 import solver_b as B  # noqa: E402

SAMPLERS = P.T21Plugin.SAMPLERS


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T21Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs(plugin):
    return [plugin.sample(seed, smp) for seed in range(400) for smp in SAMPLERS]


def test_contract_is_met_strictly(plugin):
    assert KP.validate_plugin(plugin, strict=True) == []
    assert KP.check_independence(plugin) == []


# ------------------------------------------------------------------------------------------------ hand gold

def _spec(plugin, links, claim, definition=None, decoy=None, qform="ch_clause"):
    """links: [(id, types | "DEF" | None, cause | None)] for L1, L2, L3 in chain order; claim: (type, cause);
    definition: (id, [types]); decoy: (notice id, switch-off id, [types])."""
    slots = {"AGREEMENT": S.name_slot("Ridgeway services agreement"), "CLAIMANT": S.name_slot("Halvard Bank"),
             "RESPONDENT": S.name_slot("Corran Rail"), "CAP_ID": S.id_slot("9.1"),
             "CL_TYPE": S.category_slot(claim[0], P.TYPES), "CL_CAUSE": S.category_slot(claim[1], P.CAUSES)}
    clauses, chain, target = [], [], "CAP_ID"
    for lvl, (cid, types, cause) in enumerate(links, 1):
        slot = f"L{lvl}_ID"
        slots[slot] = S.id_slot(cid)
        cl = {"slot": slot, "target": target, "level": lvl, "types": None, "cause": None, "decoy": False}
        if types == "DEF":
            cl["types"] = "DEF"
        elif types is not None:
            cl["types"] = []
            for j, t in enumerate(types):
                slots[f"L{lvl}_T{j}"] = S.category_slot(t, P.TYPES)
                cl["types"].append(f"L{lvl}_T{j}")
        if cause is not None:
            slots[f"L{lvl}_C"] = S.category_slot(cause, P.CAUSES)
            cl["cause"] = f"L{lvl}_C"
        clauses.append(cl)
        chain.append(slot)
        target = slot
    d = None
    if definition:
        slots["DEF_ID"] = S.id_slot(definition[0])
        d = {"slot": "DEF_ID", "types": []}
        for j, t in enumerate(definition[1]):
            slots[f"DEF_T{j}"] = S.category_slot(t, P.TYPES)
            d["types"].append(f"DEF_T{j}")
    if decoy:
        slots["X_ID"], slots["Y_ID"] = S.id_slot(decoy[0]), S.id_slot(decoy[1])
        ys = []
        for j, t in enumerate(decoy[2]):
            slots[f"Y_T{j}"] = S.category_slot(t, P.TYPES)
            ys.append(f"Y_T{j}")
        clauses.append({"slot": "Y_ID", "target": "X_ID", "level": 1, "types": ys, "cause": None, "decoy": True})
    order = sorted([k for k in slots if k.endswith("_ID")],
                   key=lambda s: tuple(int(x) for x in slots[s].value.split(".")))
    spec = Spec("T21", "S1", 0, "T21:hand", qform, slots,
                structure={"clauses": clauses, "def": d, "order": order, "plan": {"chain": chain, "depth": 0},
                           "layout": "plain"}, pack="t21-hand")
    return plugin.derive(spec)


L1_CONF = ("9.3", ["conf", "injury"], None)
L2_MISTAKE = ("9.4", ["conf"], "mistake")
HAND = [
    # (name, links, claim, definition, decoy, capped?, deciding id)
    ("switch-off covers", [L1_CONF, L2_MISTAKE], ("conf", "security"), None, None, False, "9.3"),
    ("switch-back covers", [L1_CONF, L2_MISTAKE], ("conf", "mistake"), None, None, True, "9.4"),
    ("type not covered", [L1_CONF, L2_MISTAKE], ("late", "mistake"), None, None, True, "9.1"),
    ("counter covers", [L1_CONF, L2_MISTAKE, ("9.6", None, "mistake")], ("conf", "mistake"), None, None, False, "9.6"),
    ("counter with another cause", [L1_CONF, L2_MISTAKE, ("9.6", None, "misconduct")], ("conf", "mistake"), None,
     None, True, "9.4"),
    ("defined term covers", [("9.3", "DEF", None)], ("defect", "supplier"), ("1.4", ["fees", "defect"]), None, False,
     "9.3"),
    ("defined term misses", [("9.3", "DEF", None)], ("ip", "supplier"), ("1.4", ["fees", "defect"]), None, True,
     "9.1"),
    ("decoy rule only", [], ("late", "mistake"), None, ("11.1", "11.2", ["late"]), True, "9.1"),
    ("cause-limited switch-off misses", [("9.3", ["injury"], "negligence")], ("injury", "mistake"), None, None, True,
     "9.1"),
    ("cause-limited switch-off covers", [("9.3", ["injury"], "negligence")], ("injury", "negligence"), None, None,
     False, "9.3"),
    # G0 H2: the walk is contiguous (R9), never a skip to a deeper covering clause
    ("skip (a): L2 misses, L3 covers", [L1_CONF, ("9.4", ["conf"], "security"), ("9.6", None, None)],
     ("conf", "mistake"), None, None, False, "9.3"),
    ("skip (b): L1 misses, L2 and L3 cover", [("9.3", ["late"], None), ("9.4", ["conf"], None), ("9.6", None, None)],
     ("conf", "mistake"), None, None, True, "9.1"),
    ("cause on the defined term", [("9.3", "DEF", "negligence")], ("fees", "mistake"), ("1.4", ["fees", "defect"]),
     None, True, "9.1"),
]


@pytest.mark.parametrize("case", HAND, ids=[c[0] for c in HAND])
def test_hand_gold(plugin, ctx, case):
    _name, links, claim, definition, decoy, is_capped, dec = case
    spec = _spec(plugin, links, claim, definition, decoy)
    assert P.capped(spec) is is_capped and P.deciding(spec) == dec == plugin.solve_a(spec)
    rr = plugin.render(spec, ctx)
    view = plugin.parse(rr.row, ctx)
    assert {k: v for k, v in view.items() if k != "options"} == plugin.canonical_for(spec, "T")
    assert plugin.solve_b(view) == dec
    for q, want in (("yn_capped", int(is_capped)), ("yn_free_of", int(not is_capped))):
        ys = spec.replace(qform=q)
        rr = plugin.render(ys, ctx)
        assert plugin.solve_a(ys) == want == plugin.solve_b(plugin.parse(rr.row, ctx)) == rr.row["gold"]


def test_g0_quotes_the_card_verbatim():
    """G0 H21: section 1.2 quotes the card; plugin.CARD and solver B's own copy both equal it."""
    g0 = P.T21Plugin.G0_LITE.read_text(encoding="utf-8")
    blocks = g0.split("### 1.2 The card")[1].split("```")
    block, short = blocks[1].strip("\n"), blocks[3].strip("\n")          # full style, then the short style (v1.3)
    assert block == P.CARD == CARD_MOD.TEMPLATES["full"]
    assert short == CARD_MOD.TEMPLATES["short"]
    assert block.replace("{CAP_ID}", "@CAP@") == B.CARDS["full"] == B.CARD
    assert short.replace("{CAP_ID}", "@CAP@") == B.CARDS["short"]
    assert P.CLOSED_WORLD == B.CLOSED and P.CARD.endswith(P.CLOSED_WORLD) and short.endswith(P.CLOSED_WORLD)
    assert P.T21Plugin.G0_HAIKU_TASK == "c2-data-stage-a/amb:T21"


def _bad_block(plugin, ctx, edit):
    spec = _spec(plugin, [L1_CONF, L2_MISTAKE], ("conf", "mistake"), None, ("11.1", "11.2", ["late"]))
    row = dict(plugin.render(spec, ctx).row)
    row["state"] = edit(row["state"])
    return row


@pytest.mark.parametrize("edit", [
    lambda st: st.replace("Clause 9.4 Despite clause 9.3", "Clause 9.4 Despite clause 9.4"),            # self-switch
    lambda st: st.replace("Clause 11.2 Clause 11.1 does not", "Clause 11.2 Clause 9.1 does not"),     # CAP named twice
    lambda st: st.replace("Clause 11.2 Clause 11.1 does not", "Clause 11.2 Clause 7.7 does not"),     # unknown target
    lambda st: st.replace("Clause 9.4 Despite clause 9.3", "Clause 9.3 Despite clause 9.3"),          # duplicate id
], ids=["self", "named-twice", "unknown", "duplicate-id"])
def test_solver_b_refuses_malformed_agreements(plugin, ctx, edit):
    """G0 R15 / H23-H24: never generated; solver B refuses the row instead of guessing."""
    row = _bad_block(plugin, ctx, edit)
    with pytest.raises(B.ParseError):
        plugin.parse(row, ctx)


def test_hand_error_models(plugin):
    s = _spec(plugin, [L1_CONF, L2_MISTAKE], ("conf", "mistake"), None, ("11.1", "11.2", ["late"]))
    assert P.deciding(s, frozenset({"t21_ignore_switch_back"})) == "9.3"
    assert P.deciding(s, frozenset({"t21_first_mention"})) == "9.3"
    s2 = _spec(plugin, [], ("late", "mistake"), None, ("11.1", "11.2", ["late"]))
    assert P.deciding(s2, frozenset({"t21_wrong_target"})) == "11.2" and P.capped(s2)


# ------------------------------------------------------------------------------------------------ gates

@pytest.fixture(scope="module")
def units(plugin, ctx):
    return [pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=(seed % 20 == 0))
            for seed in range(300) for smp in SAMPLERS]


def test_every_unit_passes_every_program_gate(units):
    bad = [u.problems[:2] for u in units if not u.ok]
    assert not bad, bad[:5]


def test_every_row_is_dev_only(units):
    rows = [r for u in units for r in u.rows]
    assert rows and all(r["meta"]["dev_only"] is True for r in rows)
    assert all(any("dev-only" in p for p in R.validate_row(r, training=True)) for r in rows[:50])


def test_overlay_shares(units, plugin):
    rep = pipeline.overlay_report(units, plugin)
    assert rep["complement_share_of_yes_no"] >= 0.20
    assert rep["non_syntactic_share_of_pairs"] >= 0.30
    assert 0.10 <= rep["twin_share"] <= 0.45
    assert 0.45 <= rep["yes_rate"] <= 0.55


def test_twins_change_one_slot_and_flip_as_constructed(plugin, specs):
    n = 0
    for spec in specs[:800]:
        for prop in plugin.relations(spec):
            if prop.kind == "twin":
                twin = plugin.derive(prop.spec)
                assert slot_diff(spec, twin) == {prop.changed_slot}
                assert plugin.solve_a(twin) == prop.expect != plugin.solve_a(spec)
                n += 1
    assert n > 200


def test_metamorphic_relations_hold(plugin, specs):
    for spec in specs[:400]:
        for prop in plugin.relations(spec):
            if prop.kind == "metamorphic":
                assert plugin.solve_a(plugin.derive(prop.spec)) == plugin.solve_a(spec), prop.note


# ------------------------------------------------------------------------------------------------ balance

def test_balance_and_traps(plugin, specs):
    yn = [s for s in specs if s.qform != "ch_clause"]
    yes = sum(P.capped(s) for s in yn) / len(yn)
    assert 0.45 <= yes <= 0.55
    ch = [s for s in specs if s.qform == "ch_clause"]
    depth = collections.Counter(s.structure["plan"]["depth"] for s in ch)
    assert all(depth[d] > 10 for d in (0, 1, 2, 3)), depth
    tags = collections.Counter(t for s in specs for t in s.tags)
    for t in ("near_miss_link", "cause_decides", "decoy_covers_claim", "definition_hop"):
        assert tags[t] > 50, (t, tags)
    assert sum(s.deep for s in specs) / len(specs) <= 0.10
    pos = collections.Counter()
    for s in ch:
        opts = plugin._options(s)
        pos[(len(opts), opts.index(plugin.solve_a(s)))] += 1
    assert len(pos) >= 6


# ------------------------------------------------------------------------------------- G-SL, bugs, determinism

def test_fixture_texts_lint_clean(plugin, ctx):
    for sk in ctx.skins.values():
        if sk.author_mode == "T":
            assert gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                                     name_allow=plugin.NAME_ALLOW) == [], sk.skin_id


def test_gsl_catches_a_leaky_skin(plugin):
    from c2_kit.skin import make_skin
    sk = make_skin("SK-LEAK", "T21", "{CLAIMANT} says the {AGREEMENT} leaves this claim uncapped.",
                   {"CLAIMANT": "name", "AGREEMENT": "name"}, register="chat")
    assert any(v.rule == "gold_label" for v in gsl.lint_template(sk, label_words=plugin.LABEL_WORDS))


def test_g2_catches_a_solver_b_that_ignores_causes(plugin, ctx, monkeypatch, specs):
    real = B._cover
    monkeypatch.setattr(B, "_cover", lambda view, cl: real(view, {**cl, "cause": None}))
    bad = 0
    for s in specs[:400]:
        if "cause_decides" in s.tags:
            probs = pipeline.check_rendered(plugin, s, plugin.render(s, ctx), ctx, run_g15=False)
            bad += any(g == "G2" for g, _ in probs)
    assert bad > 10


def test_packs_and_modes(ctx):
    """G0 section 6: one pack per card (S5 cards take held-out packs); S4 rows use Mode F narratives."""
    assert P.validate_pack(P.DEFAULT_PACK) == []
    train = {**P.DEFAULT_PACK, "pack_id": "t21-pk-a", "agreements": ["Lowmoor hosting agreement",
             "Fenwick freight agreement", "Calder Mill lease agreement", "Ashgrove catering agreement"],
             "parties": ["Brindle Foods", "Orrin Haulage", "Pellow Studio", "Kestrel Ferries", "Morvah Labs",
                         "Tarrant Print"]}
    held = {**train, "pack_id": "t21-pk-h", "held_out": True}
    pl = P.T21Plugin(lexicon=ctx.lexicon, packs=[train, held])
    assert pl.sample(5, "S1").pack == "t21-pk-a" and pl.sample(5, "S5").pack == "t21-pk-h"
    assert pl.sample(5, "S2").env()["AGREEMENT"] in train["agreements"]
    bad = {**train, "agreements": ["Lowmoor data agreement"] + train["agreements"][1:]}
    assert any("data" in p for p in P.validate_pack(bad))
    plugin = P.T21Plugin(lexicon=ctx.lexicon)
    for seed in range(6):
        for smp in SAMPLERS:
            u = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            assert u.ok, u.problems[:2]
            mode = ctx.skin(u.rows[0]["meta"]["c2"]["skin_id"]).author_mode
            assert mode == ("F" if smp == "S4" else "T")


def test_generation_is_deterministic(plugin, ctx):
    for seed in (3, 77):
        a, b = plugin.sample(seed, "S2"), plugin.sample(seed, "S2")
        assert a.structure_hash() == b.structure_hash()
        assert plugin.render(a, ctx).row == plugin.render(b, ctx).row
