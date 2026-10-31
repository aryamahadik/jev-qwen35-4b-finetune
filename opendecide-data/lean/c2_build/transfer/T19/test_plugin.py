"""transfer/T19/test_plugin.py: in-memory tests for the T19 plugin (A37 f: no file is written; no Haiku, no network).

  contract      validate_plugin(strict) == [], solver-B independence, frozen G0-lite
  hand gold     checklists with answers worked out by hand from the G0 semantics table (expiry boundary, exclusion,
                unknown with and without a failure, out-of-scope missing evidence, a leap-year month end): solver A on
                the spec, solver B (SQL) on a hand-written view, and the rendered row parsed back all give the hand
                answer
  A == B        >= 1,500 sampled units through every kit program gate (G2, G3, G4, G-SL, G-LEX, G-TW, schema; G15 on a
                slice); twins flip as constructed; metamorphic relations hold
  balance       verdict shares, yes rate, abstain wrong share, trap tags, deep share; every row dev-only
  injected bugs G2 catches an exclusive expiry in solver B's SQL; G-SL catches a leaky skin
  G0 v1.2       the card items quoted in G0 1.2 are plugin.CARD_ITEMS and solver_b's copy; the Haiku pass record matches the plugin;
                S14 guards hold on every sampled spec; packs (one per card, S5 held-out packs); S4 uses Mode F
                narratives and the other samplers Mode T; solver B refuses evidence dated on or after the audit date
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/transfer/T19
"""
from __future__ import annotations

import collections
import datetime as dt
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
from transfer.T19 import fixtures as FX  # noqa: E402
from transfer.T19 import plugin as P  # noqa: E402
from transfer.T19 import solver_b as B  # noqa: E402

SAMPLERS = P.T19Plugin.SAMPLERS
D = dt.date


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T19Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs(plugin):
    return [plugin.sample(seed, smp) for seed in range(400) for smp in SAMPLERS]


def test_contract_is_met_strictly(plugin):
    assert KP.validate_plugin(plugin, strict=True) == []
    assert KP.check_independence(plugin) == []


# ------------------------------------------------------------------------------------------------ hand gold

PROFILE = {"hosting": "cloud", "data": "personal", "stype": "office"}


def _spec(plugin, controls, audit, profile=PROFILE, qform="ch_verdict"):
    """controls: [(id, attr, vals, (xattr, xval) | None, days, evidence)] with evidence a date, "none" or "unknown"."""
    slots = {"SITE": S.name_slot("Larch Street depot"), "AUDITOR": S.name_slot("Priya Raman"),
             "AUDIT": S.date_slot(audit)}
    for a, v in profile.items():
        slots[P.ATTR_SLOT[a]] = S.category_slot(v, P.ATTRS[a])
    ctrls = []
    for i, (cid, attr, vals, excl, days, ev) in enumerate(controls):
        c = {"attr": attr, "vals": [], "xattr": None, "xval": None, "evidence": "date"}
        for j, v in enumerate(vals):
            slots[f"K{i}_V{j}"] = S.category_slot(v, P.ATTRS[attr])
            c["vals"].append(f"K{i}_V{j}")
        if excl:
            c["xattr"], c["xval"] = excl[0], f"K{i}_X"
            slots[f"K{i}_X"] = S.category_slot(excl[1], P.ATTRS[excl[0]])
        slots[f"CID{i}"] = S.id_slot(cid)
        slots[f"CN{i}"] = S.name_slot(P.CONTROL_NAMES[i])
        slots[f"N{i}"] = S.count_slot(days, P.UNIT_DAY)
        if isinstance(ev, dt.date):
            slots[f"EV{i}"] = S.date_slot(ev)
        else:
            c["evidence"] = ev
        ctrls.append(c)
    spec = Spec("T19", "S1", 0, "T19:hand", qform, slots,
                structure={"controls": ctrls, "layout": "list", "through": True}, pack="t19-hand")
    return plugin.derive(spec)


C_ACCESS = ("AC-1", "hosting", ["cloud", "hybrid"], None, 90, D(2026, 4, 1))      # last valid day 2026-06-30
HAND = [
    # (name, controls, audit, profile, verdict, first gap)
    ("boundary pass + one-day-late fail", [C_ACCESS, ("BK-2", "all", [], ("data", "public"), 30, D(2026, 5, 30))],
     D(2026, 6, 30), PROFILE, "noncompliant", "BK-2"),
    ("both on their last valid day", [C_ACCESS, ("BK-2", "all", [], ("data", "public"), 30, D(2026, 5, 31))],
     D(2026, 6, 30), PROFILE, "compliant", None),
    ("exclusion turns the expired control off", [C_ACCESS, ("BK-2", "all", [], ("data", "personal"), 30,
                                                            D(2026, 1, 1))],
     D(2026, 6, 30), PROFILE, "compliant", None),
    ("unknown and no failure", [("AC-1", "hosting", ["cloud"], None, 90, "unknown"),
                                ("BK-2", "all", [], None, 30, D(2026, 6, 20))],
     D(2026, 6, 30), PROFILE, "undetermined", None),
    ("unknown beside a failure", [("AC-1", "hosting", ["cloud"], None, 90, "unknown"),
                                  ("BK-2", "all", [], None, 30, "none")],
     D(2026, 6, 30), PROFILE, "noncompliant", None),
    ("out of scope without evidence", [("AC-1", "hosting", ["onprem", "hybrid"], None, 90, "none"),
                                       ("BK-2", "stype", ["office", "store"], None, 60, D(2026, 6, 1))],
     D(2026, 6, 30), PROFILE, "compliant", None),
    ("leap-year month end, last day", [("KR-7", "data", ["personal", "payment"], None, 30, D(2028, 1, 31))],
     D(2028, 3, 1), PROFILE, "compliant", None),
    ("leap-year month end, a day late", [("KR-7", "data", ["personal", "payment"], None, 30, D(2028, 1, 31))],
     D(2028, 3, 2), PROFILE, "noncompliant", "KR-7"),
    ("second failure is not the gap", [("AC-1", "all", [], None, 30, "none"), ("BK-2", "all", [], None, 30, "none")],
     D(2026, 6, 30), PROFILE, "noncompliant", "AC-1"),
]


def _view(spec):
    c = P.T19Plugin().canonical(spec)
    return {**c, "qform": spec.qform}


@pytest.mark.parametrize("case", HAND, ids=[c[0] for c in HAND])
def test_hand_gold(plugin, ctx, case):
    _name, controls, audit, profile, want, gap = case
    spec = _spec(plugin, controls, audit, profile)
    assert P.verdict(P.statuses(spec)) == want == plugin.solve_a(spec)
    assert B.solve_b(_view(spec)) == want
    if gap is not None:
        gs = spec.replace(qform="ch_gap")
        assert plugin.solve_a(gs) == gap == B.solve_b(_view(gs))
    rr = plugin.render(spec, ctx)
    view = plugin.parse(rr.row, ctx)
    assert {k: v for k, v in view.items() if k != "options"} == plugin.canonical_for(spec, "T")
    assert plugin.solve_b(view) == want
    if want != "undetermined":
        for q, yes in (("yn_compliant", want == "compliant"), ("yn_fails", want != "compliant")):
            ys = spec.replace(qform=q)
            assert plugin.solve_a(ys) == int(yes) == B.solve_b(_view(ys))


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
    assert rep["abstain"]["pass"] and rep["abstain"]["wrong_share"] >= 0.5
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
    assert n > 150


def test_metamorphic_relations_hold(plugin, specs):
    for spec in specs[:400]:
        for prop in plugin.relations(spec):
            if prop.kind == "metamorphic":
                assert plugin.solve_a(plugin.derive(prop.spec)) == plugin.solve_a(spec), prop.note


# ------------------------------------------------------------------------------------------------ balance

def test_balance_and_traps(plugin, specs):
    ch = [s for s in specs if s.qform == "ch_verdict"]
    share = collections.Counter(plugin.solve_a(s) for s in ch)
    assert 0.33 <= share["undetermined"] / len(ch) <= 0.45          # planned BASE share .39 (G0 v1.2 section 3: the twins dilute it to 1/3 of the rows)
    assert 0.25 <= share["compliant"] / len(ch) <= 0.40
    gap = [s for s in specs if s.qform == "ch_gap"]
    assert 0.14 <= len(gap) / len(specs) <= 0.26
    tags = collections.Counter(t for s in specs for t in s.tags)
    for t in ("expiry_boundary", "exclusion_decides", "expired_but_out_of_scope", "unknown_out_of_scope",
              "unknown_with_fail"):
        assert tags[t] > 20, (t, tags)
    assert sum(s.deep for s in specs) / len(specs) <= 0.12
    gold_pos = collections.Counter()
    for s in gap:
        env = s.env()
        ids = [env[f"CID{i}"] for i in range(len(s.structure["controls"]))]
        gold_pos[ids.index(plugin.solve_a(s))] += 1
    assert len(gold_pos) >= 3


# ------------------------------------------------------------------------------------- G-SL, bugs, determinism

def test_fixture_texts_lint_clean(plugin, ctx):
    for sk in ctx.skins.values():
        if sk.author_mode == "T":
            assert gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                                     name_allow=plugin.NAME_ALLOW) == [], sk.skin_id


def test_gsl_catches_a_leaky_skin(plugin):
    from c2_kit.skin import make_skin
    sk = make_skin("SK-LEAK", "T19", "{AUDITOR} says {SITE} is probably compliant.",
                   {"AUDITOR": "name", "SITE": "name"}, register="chat")
    rules = {v.rule for v in gsl.lint_template(sk, label_words=plugin.LABEL_WORDS)}
    assert "gold_label" in rules and "hedge" in rules


def test_g2_catches_an_exclusive_expiry_in_solver_b(plugin, ctx, monkeypatch, specs):
    monkeypatch.setattr(B, "STATUS_SQL", B.STATUS_SQL.replace(">= :audit", "> :audit"))
    bad = 0
    for s in specs[:400]:
        if "expiry_boundary" in s.tags:
            probs = pipeline.check_rendered(plugin, s, plugin.render(s, ctx), ctx, run_g15=False)
            bad += any(g == "G2" for g, _ in probs)
    assert bad > 5


def test_generation_is_deterministic(plugin, ctx):
    for seed in (3, 77):
        a, b = plugin.sample(seed, "S2"), plugin.sample(seed, "S2")
        assert a.structure_hash() == b.structure_hash()
        assert plugin.render(a, ctx).row == plugin.render(b, ctx).row


# ------------------------------------------------------------------------------------- G0 v1.1 (Haiku pass amb:T19)

def _g0_blocks():
    text = P.T19Plugin.G0_LITE.read_text(encoding="utf-8")
    sec = text.split("### 1.2", 1)[1].split("## 2.", 1)[0]
    return [b.split("\n```", 1)[0] for b in sec.split("```text\n")[1:]]


def test_card_in_g0_is_verbatim():
    """G0 1.2: the full-style items and the short-style items equal plugin.CARD_ITEMS and solver B's own copy; the cards solver B
    accepts for each question form are exactly the cards the plugin renders (both styles)."""
    import types
    full, short = _g0_blocks()
    fl = full.split("\n")
    assert fl[0] == P.CARD_HEAD and fl[-1] == P.CLOSED_WORLD
    parsed = {}
    for line in fl[1:-1]:
        tag, text = line[3:].split("] ", 1)
        parsed[tag] = text
    assert list(parsed) == [it.item_id for it in P.CARD_ITEMS]
    assert all(parsed[it.item_id] == it.full for it in P.CARD_ITEMS)
    sh = {}
    for line in short.split("\n"):
        tag, text = line[3:].split("] ", 1)
        sh[tag] = text
    assert sh == {it.item_id: it.short for it in P.CARD_ITEMS if it.short}
    assert (B.SCOPE, B.VERDICT, B.GAP, B.HEAD, B.CLOSED) == (parsed["scope"], parsed["verdict"], parsed["gap"], P.CARD_HEAD,
                                                              P.CLOSED_WORLD)
    assert B.WINDOW == (parsed["window"], sh["window"]) and B.RESULT == (parsed["result"], sh["result"])
    assert B.UNDET == (parsed["undetermined"], sh["undetermined"])
    for q in P.T19Plugin.QFORMS:
        sp = types.SimpleNamespace(qform=q)
        assert B.cards_for(q) == {P.CARD_SPEC.template(st, sp) for st in ("full", "short")}, q
    assert P.CARD_SPEC.problems() == []
    assert P.CARD_SPEC.template("full", types.SimpleNamespace(qform="yn_compliant")).endswith(P.CLOSED_WORLD)


def test_ambiguity_record_matches_the_plugin():
    import hashlib
    import json
    rec = json.loads((P.HERE / P.T19Plugin.G0_AMBIGUITY_PASS["record"]).read_text(encoding="utf-8"))
    assert rec["pass"] == P.T19Plugin.G0_HAIKU_TASK == P.T19Plugin.G0_AMBIGUITY_PASS["task_id"]
    assert len(rec["points"]) == P.T19Plugin.G0_AMBIGUITY_PASS["points"] == 29
    assert P.T19Plugin.G0_AMBIGUITY_PASS["read_g0_sha256"] in rec["input"]
    assert hashlib.sha256(P.T19Plugin.G0_LITE.read_bytes()).hexdigest() == P.T19Plugin.G0_SHA256
    # the G0 the Haiku pass and the pools were authored under (v1.1) is archived byte for byte
    assert hashlib.sha256((P.HERE / "G0_SPEC.v1_1.md").read_bytes()).hexdigest() == P.T19Plugin.G0_SHA256_AUTHORED
    assert P.T19Plugin.G0_SHA256 != P.T19Plugin.G0_SHA256_AUTHORED
    g0 = P.T19Plugin.G0_LITE.read_text(encoding="utf-8")
    for n in range(1, 30):
        assert f"- H{n} " in g0 or f"- H{n}* " in g0, n


def test_guards_hold_on_every_sampled_spec(specs):
    assert all(P._guard(s) == [] for s in specs)
    assert sum(s.deep for s in specs) / len(specs) <= 0.10
    for s in specs:
        env = s.env()
        for i in range(len(s.structure["controls"])):
            if f"EV{i}" in env:
                assert env[f"EV{i}"] < env["AUDIT"]


def _test_packs():
    words = ("Alder", "Birch", "Cedar", "Dunmore", "Elm", "Fern", "Gorse", "Heath", "Ivy", "Juniper")
    kinds = ("Quay depot", "Lane annex", "Hill yard", "Moor campus")
    out = []
    for k, w in enumerate(words):
        out.append({"pack_id": f"t19-test-{w.lower()}", "held_out": k >= 8,
                    "sites": [f"{w} {x}" for x in kinds],
                    "auditors": [f"{f} {w}son" for f in ("Lena", "Rafael", "Mira", "Tobias")],
                    "controls": ["door lock survey", "backup drill", "sprinkler survey", "laptop audit", "cable survey",
                                 "alarm drill", "badge audit", "key rotation"]})
    return out


def test_default_pack_and_bad_packs():
    assert P.validate_pack(P.DEFAULT_PACK) == []
    good = _test_packs()[0]
    assert P.validate_pack(good) == []
    for bad in ({**good, "sites": good["sites"][:3]}, {**good, "sites": ["Harbor Road office"] + good["sites"][1:]},
                {**good, "controls": ["evidence gap review"] + good["controls"][1:]},
                {**good, "auditors": ["Will Ortega"] + good["auditors"][1:]},
                {**good, "controls": ["no access audit"] + good["controls"][1:]}):
        assert P.validate_pack(bad), bad
    with pytest.raises(KP.ContractError):
        P.T19Plugin(packs=[{**good, "sites": good["sites"][:2]}])


def test_one_pack_per_card_and_held_out_packs_for_s5(ctx):
    packs = _test_packs()
    pl = P.T19Plugin(lexicon=ctx.lexicon, packs=packs)
    held = {p["pack_id"] for p in packs if p["held_out"]}
    by_card, used = {}, set()
    for seed in range(200):
        for smp in SAMPLERS:
            s = pl.sample(seed, smp)
            assert by_card.setdefault(s.card_id, s.pack) == s.pack
            assert (s.pack in held) == (smp == "S5")
            pk = pl.pack_of(s)
            env = s.env()
            assert env["SITE"] in pk["sites"] and env["AUDITOR"] in pk["auditors"]
            assert all(env[f"CN{i}"] in pk["controls"] for i in range(len(s.structure["controls"])))
            used.add(s.pack)
    assert used == {p["pack_id"] for p in packs}
    u = pipeline.build_unit(pl, pl.sample(3, "S1"), ctx, run_g15=False)
    assert u.ok, u.problems[:3]


def test_s4_rows_use_mode_f_narratives(plugin, ctx):
    for seed in range(40):
        for smp in SAMPLERS:
            rr = plugin.render(plugin.sample(seed, smp), ctx)
            mode = ctx.skin(rr.skin_id).author_mode
            assert mode == ("F" if smp == "S4" else "T"), (smp, rr.skin_id)


def test_solver_b_refuses_evidence_not_before_the_audit(plugin, ctx):
    spec = _spec(plugin, [C_ACCESS, ("BK-2", "all", [], None, 30, D(2026, 6, 30))], D(2026, 6, 30))
    assert P._guard(spec) and plugin.solve_a(spec) == "compliant"       # the generator never makes this spec
    rr = plugin.render(spec, ctx)
    with pytest.raises(B.ParseError):
        B.parse(rr.row, ctx)
    probs = pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False)
    assert any(g == "G3" for g, _ in probs)                              # the unit is dropped
