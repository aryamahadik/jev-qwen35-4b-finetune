"""transfer/T20/test_plugin.py: in-memory tests for the T20 plugin (A37 f: no file is written; no Haiku, no network).

  contract      validate_plugin(strict) == [], solver-B independence, frozen G0-lite
  hand gold     incidents with answers worked out by hand from the G0 semantics table (a band threshold, a step due
                exactly at the check time, an acknowledgement exactly at a due time, the maintenance lowering, a
                critical service inside the window, a window ending at opening, data exposure, two offsets): solver A
                on the spec, solver B (simulator) on the parsed rendered row, and the hand answer agree
  A == B        >= 1,500 sampled units through every kit program gate (G2, G3, G4, G-SL, G-LEX, G-TW, schema; G15 on a
                slice); twins flip as constructed; metamorphic relations hold
  balance       yes rate, gold level spread, trap tags, deep share (<= 10%, spec 3.0); every row dev-only
  G0 v2         the card states the time anchor, the caps and the window's single effect; monotone matrices; solver B
                refuses a row outside the R2 domain; packs (one per card, S5 held out, check_pack)
  injected bugs G2 catches a simulator that lets an acknowledgement at the due time miss the step; G-SL catches a
                leaky skin
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/transfer/T20
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
from transfer.T20 import fixtures as FX  # noqa: E402
from transfer.T20 import plugin as P  # noqa: E402
from transfer.T20 import solver_b as B  # noqa: E402

SAMPLERS = P.T20Plugin.SAMPLERS
UTC = dt.timezone.utc
PLUS1 = dt.timezone(dt.timedelta(hours=1))
OPEN = dt.datetime(2026, 3, 5, 10, 0, tzinfo=UTC)


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T20Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs(plugin):
    return [plugin.sample(seed, smp) for seed in range(400) for smp in SAMPLERS]


def test_contract_is_met_strictly(plugin):
    assert KP.validate_plugin(plugin, strict=True) == []
    assert KP.check_independence(plugin) == []


# ------------------------------------------------------------------------------------------------ hand gold

def _spec(plugin, *, users, urgency, check_min, ack_min=None, service="search", critical=("login", "email"),
          window=None, exposed="no", check_tz=UTC, qform="ch_sev", card="full"):
    mx = P.MATRICES[0]                          # wide (1, 2, 3), partial (2, 3, 4), minimal (3, 4, 4)
    slots = {"INC_ID": S.id_slot("INC-4821"), "SERVICE": S.category_slot(service, P.SERVICES),
             "USERS": S.count_slot(users, P.UNIT_USER), "URGENCY": S.category_slot(urgency, P.URGENCY),
             "EXPOSED": S.category_slot(exposed, P.YESNO), "OPEN": S.datetime_slot(OPEN),
             "CHECK": S.datetime_slot((OPEN + dt.timedelta(minutes=check_min)).astimezone(check_tz)),
             "STEP": S.count_slot(30, P.UNIT_MIN), "U1": S.count_slot(100),
             "U2": S.count_slot(1000), "TEAM": S.name_slot("Payments squad"),
             "REPORTER": S.name_slot("Dana Okafor")}
    if ack_min is not None:
        slots["ACK"] = S.datetime_slot((OPEN + dt.timedelta(minutes=ack_min)).astimezone(check_tz))
    for r, row in zip("WPM", mx):
        for c, v in zip("ODC", row):
            slots[f"MX_{r}_{c}"] = S.category_slot(f"sev{v}", P.SEV)
    for i, cs in enumerate(critical):
        slots[f"CRIT{i}"] = S.category_slot(cs, P.SERVICES)
    if window:
        slots["MW_START"] = S.datetime_slot(OPEN + dt.timedelta(minutes=window[0]))
        slots["MW_END"] = S.datetime_slot(OPEN + dt.timedelta(minutes=window[1]))
    inside = bool(window) and window[0] <= 0 < window[1]
    st = {"critical": ["CRIT0", "CRIT1"], "layout": "list", "printed": check_tz is UTC,
          "plan": {"window": inside, "critical": service in critical}, "card": card}
    return plugin.derive(Spec("T20", "S1", 0, "T20:hand", qform, slots, structure=st, pack="t20-hand"))


HAND = [
    # (name, kwargs, hand severity)
    ("users at the wide threshold, no step due", dict(users=1000, urgency="degraded", check_min=29), 2),
    ("one below the threshold", dict(users=999, urgency="degraded", check_min=29), 3),
    ("step due exactly at the check time", dict(users=1000, urgency="degraded", check_min=30), 1),
    ("acknowledged exactly at the due time", dict(users=999, urgency="degraded", check_min=65, ack_min=30), 3),
    ("acknowledged one minute late", dict(users=999, urgency="degraded", check_min=65, ack_min=31), 2),
    ("two steps, never above SEV1", dict(users=999, urgency="outage", check_min=95), 1),
    ("inside the window", dict(users=500, urgency="outage", check_min=10, window=(-30, 60)), 3),
    ("critical service inside the window", dict(users=500, urgency="degraded", check_min=10, window=(0, 60),
                                                service="login"), 2),
    ("window ends at opening", dict(users=500, urgency="outage", check_min=10, window=(-60, 0)), 2),
    ("lowering stops at SEV4", dict(users=5, urgency="cosmetic", check_min=10, window=(-5, 5)), 4),
    ("data exposed", dict(users=5, urgency="cosmetic", check_min=10, exposed="yes"), 1),
    ("two offsets, one step", dict(users=500, urgency="degraded", check_min=45, check_tz=PLUS1), 2),
]


@pytest.mark.parametrize("case", HAND, ids=[c[0] for c in HAND])
def test_hand_gold(plugin, ctx, case):
    _name, kw, want = case
    spec = _spec(plugin, **kw)
    assert P.severity(spec) == want == P._sev_c(spec)
    rr = plugin.render(spec, ctx)
    view = plugin.parse(rr.row, ctx)
    assert {k: v for k, v in view.items() if k != "options"} == plugin.canonical_for(spec, "T")
    assert plugin.solve_b(view) == f"sev{want}" == rr.row["gold"].lower()
    for level in ("sev2", "sev3"):
        ys = spec.replace(slots={**spec.slots, "LEVEL": S.category_slot(level, P.SEV),
                                 "LEVEL_NEXT": S.category_slot(f"sev{int(level[-1]) + 1}", P.SEV)})
        for q in ("yn_reaches", "yn_below", "yn_fails"):
            s2 = plugin.derive(ys.replace(qform=q))
            rr2 = plugin.render(s2, ctx)
            reaches = want <= int(level[-1])
            assert plugin.solve_a(s2) == (int(reaches) if q == "yn_reaches" else int(not reaches))
            assert plugin.solve_b(plugin.parse(rr2.row, ctx)) == rr2.row["gold"]


def test_hand_error_models(plugin):
    s = _spec(plugin, users=500, urgency="degraded", check_min=10, window=(0, 60), service="login")
    assert P.severity(s) == 2 and P.severity(s, frozenset({"t20_floor_first"})) == 3
    s2 = _spec(plugin, users=999, urgency="degraded", check_min=65, ack_min=30)
    assert P.severity(s2, frozenset({"t20_ack_boundary"})) == 2 and P.severity(s2, frozenset({"t20_ignore_ack"})) == 1
    s3 = _spec(plugin, users=1000, urgency="degraded", check_min=29)
    assert P.severity(s3, frozenset({"t20_band_exclusive"})) == 3


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
    yn = [s for s in specs if s.qform != "ch_sev"]
    yes = sum(P.severity(s) <= int(s.env()["LEVEL"][-1]) for s in yn) / len(yn)
    assert 0.45 <= yes <= 0.55
    ch = [s for s in specs if s.qform == "ch_sev"]
    lv = collections.Counter(plugin.solve_a(s) for s in ch)
    assert all(0.18 <= lv[k] / len(ch) <= 0.32 for k in P.SEV_KEYS), lv
    tags = collections.Counter(t for s in specs for t in s.tags)
    for t in ("band_boundary", "ack_at_step", "window_misses", "window_start", "order_matters", "two_offsets"):
        assert tags[t] > 20, (t, tags)
    assert sum(s.deep for s in specs) / len(specs) <= 0.10
    for smp in SAMPLERS:
        ss = [s for s in specs if s.sampler == smp]
        assert sum(s.deep for s in ss) / len(ss) <= 0.10, smp


# ------------------------------------------------------------------------------------- G-SL, bugs, determinism

def test_fixture_texts_lint_clean(plugin, ctx):
    for sk in ctx.skins.values():
        if sk.author_mode == "T":
            assert gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                                     name_allow=plugin.NAME_ALLOW) == [], sk.skin_id


def test_gsl_catches_a_leaky_skin(plugin):
    from c2_kit.skin import make_skin
    sk = make_skin("SK-LEAK", "T20", "{REPORTER} says this is critical for {TEAM}.",
                   {"REPORTER": "name", "TEAM": "name"}, register="chat")
    assert any(v.rule == "gold_label" for v in gsl.lint_template(sk, label_words=plugin.LABEL_WORDS))


def test_g2_catches_an_acknowledgement_boundary_bug(plugin, ctx, monkeypatch, specs):
    real = B.solve_b

    def buggy(view):
        if view["ack"] is not None:
            view = {**view, "ack": (dt.datetime.fromisoformat(view["ack"]) + dt.timedelta(minutes=1)).isoformat(),
                    "m_ack": None if view["m_ack"] is None else view["m_ack"] + 1}
        return real(view)
    monkeypatch.setattr(B, "solve_b", buggy)
    bad = 0
    for s in specs[:600]:
        if "ack_at_step" in s.tags:
            probs = pipeline.check_rendered(plugin, s, plugin.render(s, ctx), ctx, run_g15=False)
            bad += any(g == "G2" for g, _ in probs)
    assert bad > 3


def test_generation_is_deterministic(plugin, ctx):
    for seed in (3, 77):
        a, b = plugin.sample(seed, "S2"), plugin.sample(seed, "S2")
        assert a.structure_hash() == b.structure_hash()
        assert plugin.render(a, ctx).row == plugin.render(b, ctx).row


# ------------------------------------------------------------------------------------------------ G0 v2 (amb:T20)

def _cards(plugin, **kw):
    return {st: P.card_template(_spec(plugin, card=st, **kw), st) for st in ("full", "short")}


def test_card_states_caps_window_effect_and_the_horizon(plugin):
    """G0 v3 1.1: the card still carries every rule (the v2 test pinned the v2 phrases; the rules are unchanged)."""
    both = _cards(plugin, users=500, urgency="degraded", check_min=10, window=(-30, 60), qform="yn_reaches",
                  check_tz=PLUS1)
    for style, text in both.items():
        assert "never less severe than SEV4" in text and "no other effect" in text, style
        assert "never more severe than SEV1" in text and "less severe than SEV2: SEV2" in text, style
        assert "start included, end excluded" in text and "at or before the check time" in text, style
        assert "unless acknowledged at or before that step's time" in text, style
        assert "compared as points in time" in text and "reaches a level" in text, style
        assert P.CLOSED_WORLD in text
        assert not any(w in text for w in ("never below", "up to SEV1", "raise it", "above", "lower"))
    assert both["full"].startswith("SEV1 is the most severe, SEV4 the least.")
    assert both["short"].startswith("SEV1 most severe, SEV4 least.")


def test_card_items_apply_only_where_the_rule_can_matter(plugin):
    win = _cards(plugin, users=500, urgency="degraded", check_min=10, window=(-30, 60), qform="yn_reaches")["full"]
    no = _cards(plugin, users=500, urgency="degraded", check_min=10, qform="ch_sev")["full"]
    assert "maintenance window (start included" in win and "maintenance window (start" not in no
    assert win.count("\n") > no.count("\n") - 2 and "reaches a level" in win and "reaches a level" not in no
    # one-offset rows print the minute lines, so no times sentence; the two-offset rows carry it
    assert "points in time" not in win
    two = _cards(plugin, users=500, urgency="degraded", check_min=10, check_tz=PLUS1, qform="ch_sev")["full"]
    assert "points in time" in two
    # the steps are numbered 1-4 with a window and 1-3 without
    assert "\n4. " in win and "\n4. " not in no and "\n3. " in no


def test_card_variants_keep_every_rule():
    assert P.CARD.problems() == []
    for it in P.CARD.items:
        if it.short is not None:
            from c2_kit.cards import variant_problems
            assert variant_problems(it.full, it.short) == [], it.item_id


def test_matrices_are_monotone():
    for mx in P.MATRICES:
        for r in range(3):
            for c in range(3):
                if r < 2:
                    assert mx[r][c] <= mx[r + 1][c], mx
                if c < 2:
                    assert mx[r][c] <= mx[r][c + 1], mx
    assert len(set(P.MATRICES)) == 4


@pytest.mark.parametrize("kw", [dict(ack_min=0, check_min=40), dict(ack_min=50, check_min=40)],
                         ids=["ack_at_opening", "ack_after_check"])
def test_solver_b_refuses_rows_outside_the_domain(plugin, ctx, kw):
    spec = _spec(plugin, users=500, urgency="degraded", **kw)
    assert not P.in_domain(spec.env(), ("CRIT0", "CRIT1"))
    view = plugin.parse(plugin.render(spec, ctx).row, ctx)
    with pytest.raises(B.ParseError):
        plugin.solve_b(view)


def test_every_sampled_spec_is_in_the_domain(specs):
    assert all(P.in_domain(s.env(), tuple(s.structure["critical"])) for s in specs)
    assert all(not any(getattr(v, "second", 0) for v in s.env().values()) for s in specs)


def test_packs_one_per_card_and_s5_held_out(ctx):
    train = tuple(P.Pack(f"t20-test-{i:02d}", ("Atlas crew", "Ledger guild", f"Harbor {w}"),
                         ("Dana Okafor", "Lena Whitcombe", "Ravi Anand", "Mira Castell"))
                  for i, w in enumerate(("squad", "team", "group", "unit", "watch", "desk", "cell", "corps", "ring",
                                         "deck", "hall", "yard", "dock", "wing", "loft", "post", "camp", "fort",
                                         "port", "hive", "nest", "lane", "row", "den", "bay", "keep", "gate",
                                         "tower", "bridge", "forge")))
    held = (P.Pack("t20-test-h0", ("Quarry crew", "Basin guild", "Delta squad"),
                   ("Priya Hallam", "Oskar Lind", "Beatriz Soto", "Kwame Asante"), held_out=True),)
    pl = P.T20Plugin(lexicon=ctx.lexicon, packs=train + held)
    specs = [pl.sample(seed, smp) for seed in range(300) for smp in SAMPLERS]
    by_card = collections.defaultdict(set)
    for s in specs:
        by_card[s.card_id].add(s.pack)
        pack = next(p for p in train + held if p.key == s.pack)
        assert pack.held_out == (s.sampler == "S5")
        assert s.env()["TEAM"] in pack.teams and s.env()["REPORTER"] in pack.reporters
    assert all(len(v) == 1 for v in by_card.values())
    assert len({s.pack for s in specs if s.sampler != "S5"}) >= 25


def test_check_pack_refuses_bad_packs():
    good = P.Pack("t20-x", ("Atlas crew", "Ledger guild", "Harbor squad"),
                  ("Dana Okafor", "Lena Whitcombe", "Ravi Anand", "Mira Castell"))
    assert P.check_pack(good, P.T20Plugin.LABEL_WORDS) == []
    for teams in (("Payments crew", "Ledger guild", "Harbor squad"), ("Major crew", "Ledger guild", "Harbor squad"),
                  ("Atlas crew", "Atlas crew", "Harbor squad"), ("Atlas crew 2", "Ledger guild", "Harbor squad"),
                  ("Atlas", "Ledger guild", "Harbor squad"), ("First crew", "Ledger guild", "Harbor squad")):
        assert P.check_pack(P.Pack("t20-x", teams, good.reporters), P.T20Plugin.LABEL_WORDS), teams
    assert P.check_pack(P.Pack("t20-x", good.teams, ("Dana", "Lena Whitcombe", "Ravi Anand", "Mira Castell")))
