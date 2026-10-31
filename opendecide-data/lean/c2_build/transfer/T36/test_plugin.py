"""transfer/T36/test_plugin.py: in-memory tests for the T36 plugin (A37 f: no file is written; no Haiku, no network).

  contract      validate_plugin(strict) == [], solver-B independence, frozen G0-lite
  hand gold     npm and Python-style cases with answers worked out by hand from the G0 semantics table (not by either
                solver): solver A on the spec and solver B on a hand-written view both give the hand answer; every
                hand case also renders, parses back and solves the same
  oracle        on every generated Python-style spec, solver A equals the `packaging` library (SpecifierSet.contains
                with pre-releases on, plus the G0 S7 gate) on every listed version
  A == B        >= 1,500 sampled units through every kit program gate (G2, G3, G4, G-SL, G-LEX, G-TW, schema; G15 on
                a slice); twins flip as constructed
  balance       yes rate, none share, trap tags, depth; every row dev-only
  injected bugs G2 catches a text-order compare in solver B; G-SL catches a leaky skin
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/transfer/T36
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
from transfer.T36 import fixtures as FX  # noqa: E402
from transfer.T36 import plugin as P  # noqa: E402
from transfer.T36 import solver_b as B  # noqa: E402

SAMPLERS = P.T36Plugin.SAMPLERS


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T36Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs(plugin):
    return [plugin.sample(seed, smp) for seed in range(400) for smp in SAMPLERS]


def test_contract_is_met_strictly(plugin):
    assert KP.validate_plugin(plugin, strict=True) == []
    assert KP.check_independence(plugin) == []


# ------------------------------------------------------------------------------------------------ hand gold

def _spec(eco, alts, published, cand=None, qform="yn_meets", hyphen=None):
    slots = {"PKG": S.id_slot("fernhill-cache"), "PROJECT": S.name_slot("Harbor Lantern"),
             "PROJECT_ID": S.id_slot("harbor-lantern"), "PERSON": S.name_slot("Dana Okafor")}
    names, k = [], 0
    for alt in alts:
        row = []
        for c in alt:
            k += 1
            slots[f"C{k}"] = S.glob_slot(c)
            row.append(f"C{k}")
        names.append(row)
    for i, v in enumerate(published, 1):
        slots[f"V{i}"] = S.id_slot(v)
    if cand is not None:
        slots["CAND"] = S.id_slot(cand)
    structure = {"eco": eco, "alts": names, "hyphen": hyphen or [False] * len(alts),
                 "published": [f"V{i}" for i in range(1, len(published) + 1)], "container": "inline",
                 "listing": "list", "shape": {"alts": [], "checks": [], "named_pre": False}}
    return Spec("T36", "S1", 0, "T36:hand", qform, slots, structure=structure, pack="t36-hand")


NPM = [
    # (alternatives, hyphen flags, version, hand answer: meets?)
    ([["^1.4.2"]], None, "1.9.9", True), ([["^1.4.2"]], None, "2.0.0", False), ([["^1.4.2"]], None, "1.4.1", False),
    ([["^1.4.2"]], None, "1.4.2", True), ([["^0.4.2"]], None, "0.4.9", True), ([["^0.4.2"]], None, "0.5.0", False),
    ([["^0.0.4"]], None, "0.0.4", True), ([["^0.0.4"]], None, "0.0.5", False), ([["~1.4.2"]], None, "1.4.9", True),
    ([["~1.4.2"]], None, "1.5.0", False), ([["1.4.x"]], None, "1.4.12", True), ([["1.4.x"]], None, "1.5.0", False),
    ([["1.x"]], None, "1.99.0", True), ([["1.x"]], None, "2.0.0", False),
    ([["1.2.3", "2.3.4"]], [True], "2.3.4", True), ([["1.2.3", "2.3.4"]], [True], "2.3.5", False),
    ([[">=1.2.0", "<1.10.0"]], None, "1.9.5", True), ([[">=1.2.0", "<1.10.0"]], None, "1.10.0", False),
    ([[">1.2.0", "<=1.3.0"]], None, "1.2.0", False), ([[">1.2.0", "<=1.3.0"]], None, "1.3.0", True),
    ([["=1.2.3"]], None, "1.2.3", True), ([["1.2.3"]], None, "1.2.4", False),
    ([["^1.2.3"]], None, "1.3.0-beta", False), ([["^1.2.3-beta.2"]], None, "1.2.3-beta.5", True),
    ([["^1.2.3-beta.2"]], None, "1.2.3-beta.10", True), ([["^1.2.3-beta.2"]], None, "1.2.3-beta.1", False),
    ([["^1.2.3-beta.2"]], None, "1.2.3-alpha", False), ([["^1.2.3-beta.2"]], None, "1.2.3", True),
    ([["^1.2.3-beta.2"]], None, "1.2.4-beta.9", False),
    ([["1.x"], [">=3.0.0", "<3.1.0"]], None, "3.0.5", True), ([["1.x"], [">=3.0.0", "<3.1.0"]], None, "2.0.0", False),
    ([["1.x"], [">=3.0.0", "<3.1.0"]], None, "1.9.0", True),
]
PEP = [
    (["~=1.4.2"], "1.4.9", True), (["~=1.4.2"], "1.5", False), (["~=1.4.2"], "1.4.2", True),
    (["~=1.4.2"], "1.4.1", False),
    (["~=1.4"], "1.9", True), (["~=1.4"], "2.0", False), (["==1.4.*"], "1.4.0", True), (["==1.4.*"], "1.40", False),
    (["==1.4.*"], "1.4.post1", True), (["==1.4.*"], "1.4rc1", False), (["==1.4"], "1.4.0", True),
    (["==1.4"], "1.4.1", False), ([">=1.4", "!=1.5", "<2.0"], "1.5.0", False),
    ([">=1.4", "!=1.5", "<2.0"], "1.6", True),
    (["~=1.4.2rc1"], "1.4.2rc3", True), (["~=1.4.2rc1"], "1.4.2", True), (["~=1.4.2rc1"], "1.4.2b9", False),
    ([">=1.4", "<2.0"], "1.12rc1", False), ([">=1.4", "<2.0"], "1.10", True), (["<=1.4.2"], "1.4.2.0", True),
    ([">1.4", "<2.0"], "1.4.0", False), ([">1.4", "<2.0"], "1.4.1", True),
]


def _view(eco, alts, hyphen, published, cand, qform):
    return {"eco": eco, "alts": alts, "hyphen": hyphen or [False] * len(alts), "published": published,
            "candidate": cand, "qform": qform}


@pytest.mark.parametrize("case", NPM, ids=[f"npm:{'|'.join(' '.join(a) for a in c[0])}:{c[2]}" for c in NPM])
def test_npm_hand_gold(case):
    alts, hyph, v, want = case
    spec = _spec("npm", alts, [v], v, hyphen=hyph)
    assert P.meets(spec, v) is want
    assert B.solve_b(_view("npm", alts, hyph, [v], v, "yn_meets")) == int(want)
    assert B.solve_b(_view("npm", alts, hyph, [v], v, "yn_outside")) == int(not want)


@pytest.mark.parametrize("case", PEP, ids=[f"pep:{','.join(c[0])}:{c[1]}" for c in PEP])
def test_pep_hand_gold(case):
    comps, v, want = case
    spec = _spec("pep", [comps], [v], v)
    assert P.meets(spec, v) is want
    assert B.solve_b(_view("pep", [comps], None, [v], v, "yn_meets")) == int(want)


def test_hand_picks():
    vs = ["1.1.0", "1.2.0", "1.10.0", "2.0.0", "1.9.0"]
    s = _spec("npm", [["^1.2.0"]], vs, qform="ch_pick")
    assert P.pick(s) == "1.10.0" == B.solve_b(_view("npm", [["^1.2.0"]], None, vs, None, "ch_pick"))
    assert P.pick(s, frozenset({"t36_lexical_compare"})) == "1.9.0"
    vs2 = ["1.4", "1.9", "1.10", "2.0", "1.12rc1"]
    s2 = _spec("pep", [[">=1.4", "<2.0"]], vs2, qform="ch_pick")
    assert P.pick(s2) == "1.10" == B.solve_b(_view("pep", [[">=1.4", "<2.0"]], None, vs2, None, "ch_pick"))
    assert P.pick(s2, frozenset({"t36_prerelease_ignored"})) == "1.12rc1"
    s3 = _spec("npm", [["^0.4.2"]], ["0.3.0", "0.5.0", "0.9.1"], qform="ch_pick")
    assert P.pick(s3) == "none" and P.pick(s3, frozenset({"t36_caret_as_major"})) == "0.9.1"


@pytest.mark.parametrize("case", NPM[:12] + [NPM[22]], ids=lambda c: f"{c[0]}:{c[2]}")
def test_hand_cases_render_and_parse(plugin, ctx, case):
    alts, hyph, v, want = case
    spec = plugin.derive(_spec("npm", alts, [v, "9.9.9"], v, hyphen=hyph))
    rr = plugin.render(spec, ctx)
    view = plugin.parse(rr.row, ctx)
    assert {k: x for k, x in view.items() if k != "options"} == plugin.canonical_for(spec, "T")
    assert plugin.solve_b(view) == int(want) == rr.row["gold"]


# ------------------------------------------------------------------------------------------------ oracle

def test_python_style_gold_equals_the_packaging_library(specs):
    pk = pytest.importorskip("packaging.specifiers")
    from packaging.version import Version
    n = 0
    for spec in specs:
        if spec.structure["eco"] != "pep":
            continue
        env = spec.env()
        comps = [env[x] for x in spec.structure["alts"][0]]
        ss = pk.SpecifierSet(",".join(comps))
        named = any(not c.startswith("!=") and not c.endswith(".*") and Version(c.lstrip("~=!<>")).is_prerelease
                    for c in comps)
        for v in P.published(spec):
            want = ss.contains(v, prereleases=True) and (not Version(v).is_prerelease or named)
            assert P.meets(spec, v) == want, (comps, v)
            n += 1
    assert n > 1000


# ------------------------------------------------------------------------------------------------ gates

@pytest.fixture(scope="module")
def units(plugin, ctx):
    out = []
    for seed in range(300):
        for smp in SAMPLERS:
            out.append(pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=(seed % 20 == 0)))
    return out


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
    assert rep["abstain"]["pass"]


def test_twins_change_one_slot_and_flip_as_constructed(plugin, specs):
    n = 0
    for spec in specs[:800]:
        for prop in plugin.relations(spec):
            if prop.kind != "twin":
                continue
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
    yn = [s for s in specs if s.qform != "ch_pick"]
    yes = sum(int(P.meets(s, s.env()["CAND"])) for s in yn) / len(yn)
    assert 0.45 <= yes <= 0.55
    ch = [s for s in specs if s.qform == "ch_pick"]
    assert abs(len(ch) / len(specs) - P.N_CHOICE_SLOTS / P.W_SLOTS) < 0.01        # stratified slots
    none = sum(plugin.solve_a(s) == "none" for s in ch) / len(ch)
    assert abs(none - (1 / 3 + 1 / 4) / 2) < 0.015                      # F1: the None gold is 1/k (k = 3 and 4 alternate)
    tags = collections.Counter(t for s in specs for t in s.tags)
    for t in ("caret_zero", "prerelease_listed", "alternatives", "padding", "text_order_trap", "at_bound"):
        assert tags[t] > 20, (t, tags)
    assert {s.structure["eco"] for s in specs} == {"npm", "pep"}
    assert sum(s.deep for s in specs) / len(specs) <= 0.10


def test_error_models_answer_choice_rows_only(plugin, specs):
    ms = plugin.error_models()
    for spec in specs[:200]:
        for m in ms.values():
            a = m.fn(spec)
            if spec.qform != "ch_pick":
                assert a is None
            elif a is not None:
                assert a == "none" or a in P.published(spec)


# ------------------------------------------------------------------------------------- G-SL, bugs, determinism

def test_fixture_texts_lint_clean(plugin, ctx):
    for sk in ctx.skins.values():
        if sk.author_mode == "T":
            assert gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                                     name_allow=plugin.NAME_ALLOW) == [], sk.skin_id


def test_gsl_catches_a_leaky_skin(plugin):
    from c2_kit.skin import make_skin
    sk = make_skin("SK-LEAK", "T36", "{PERSON} says {PKG} is compatible with {PROJECT}.",
                   {"PERSON": "name", "PKG": "id", "PROJECT": "name"}, register="chat")
    assert any(v.rule == "gold_label" for v in gsl.lint_template(sk, label_words=plugin.LABEL_WORDS))


def test_g2_catches_a_text_order_bug_in_solver_b(plugin, ctx, monkeypatch, specs):
    real = B.compare
    monkeypatch.setattr(B, "compare", lambda eco, a, b: (a > b) - (a < b))
    bad = sum(1 for s in specs[:300] if any(g == "G2" for g, _ in
                                             pipeline.check_rendered(plugin, s, plugin.render(s, ctx), ctx,
                                                                     run_g15=False)))
    monkeypatch.setattr(B, "compare", real)
    assert bad > 10


def test_generation_is_deterministic(plugin, ctx):
    for seed in (3, 77):
        a, b = plugin.sample(seed, "S2"), plugin.sample(seed, "S2")
        assert a.structure_hash() == b.structure_hash()
        assert plugin.render(a, ctx).row == plugin.render(b, ctx).row
