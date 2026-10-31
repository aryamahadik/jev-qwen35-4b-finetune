"""transfer/T20/test_fix_i1.py: tests for pilot fix iteration 1 (PILOT_VERDICT F1-F6; G0_SPEC.md v3). In memory only (A37 f).

  F1 / F2  the twin: a wider edit list (USERS, URGENCY, EXPOSED, CHECK, ACK), every twin one slot and in the R2 domain,
           yes/no twins 50% reaching (a reaching base is flipped as often as a non-reaching one), choice twins go to a
           level drawn uniformly over the three others, the planned twin always exists (label-first)
  F3       the stratified plan: choice vs yes/no slots, ch_sev golds exactly uniform per block, every question form's
           outcome and level balanced by construction, twin requests exactly 2 of 5; yes/no share of ROWS in band
  F4       the card: place_rules (row.card on yes/no rows, instructions head on choice rows), split_rules round trip, the
           same card on a complement / twin / equiv partner, the style share, real-token mean <= 800 on the frozen pool
  F5       yn_double_neg: polarity-clean program wordings, k_syn = 2, solver B reads them, the complement partner is
           yn_not_reaches, a pool wording is used when the (screened) pool has one
  F6       Mode F reporter role (roles.py), quarantine, polarity screening of the frozen wordings
  determinism  the same rows under two PYTHONHASHSEEDs

Run (from lean/c2_build):  ../../.venv/bin/python -m pytest -q transfer/T20/test_fix_i1.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import cards as CARDS  # noqa: E402
from c2_kit import pipeline  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit.choiceplan import chi2_uniform_p  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from transfer.T20 import fixtures as FX  # noqa: E402
from transfer.T20 import haiku_author as H  # noqa: E402
from transfer.T20 import plugin as P  # noqa: E402
from transfer.T20 import quarantine as QR  # noqa: E402
from transfer.T20 import roles as ROLES  # noqa: E402
from transfer.T20 import solver_b as B  # noqa: E402

import negcount  # noqa: E402  (c_src/common, on sys.path through c2_kit.paths)

TRAIN = ("S1", "S2", "S3", "S4")
BASE = 900_000


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T20Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs(plugin):
    return {(smp, seed): plugin.sample(seed, smp) for smp in TRAIN for seed in range(BASE, BASE + 120)}


@pytest.fixture(scope="module")
def units(plugin, ctx, specs):
    return [pipeline.build_unit(plugin, s, ctx, run_g15=False) for s in specs.values()]


# ------------------------------------------------------------------------------------------------ F3: the plan

def test_every_slot_block_holds_exactly_its_choice_bases():
    first = BASE // P.W_SLOTS
    per = P.W_SLOTS - P.N_CHOICE_SLOTS
    for smp in TRAIN + ("S5",):
        for blk in range(8):
            got = [P.slot_of(smp, BASE + blk * P.W_SLOTS + i) for i in range(P.W_SLOTS)]
            assert sum(k == "choice" for k, _ in got) == P.N_CHOICE_SLOTS
            assert sorted(i for k, i in got if k == "yesno") == list(range((first + blk) * per, (first + blk + 1) * per))


def test_choice_golds_are_exactly_uniform_per_block_of_four_choice_bases():
    for smp in TRAIN:
        plans = {}
        for seed in range(BASE, BASE + 400):
            kind, idx = P.slot_of(smp, seed)
            if kind == "choice":
                plans[idx] = P.plan_of(smp, seed)
        assert len(plans) >= 200
        lo = min(plans)
        assert lo % 4 == 0
        for blk in range(len(plans) // 4):
            assert sorted(plans[lo + 4 * blk + i].target for i in range(4)) == list(P.SEV_KEYS), (smp, blk)


def test_every_question_form_is_balanced_by_construction():
    for smp in TRAIN:
        cells = collections.defaultdict(collections.Counter)
        for seed in range(BASE, BASE + 400):
            pl = P.plan_of(smp, seed)
            if pl.kind == "yesno":
                cells[pl.qform][(pl.target, pl.level)] += 1
        for q, c in cells.items():
            n = sum(c.values())
            yes_reach = sum(v for (t, _l), v in c.items() if t)
            assert abs(yes_reach - n / 2) <= 1, (smp, q, c)                        # reaches: exactly half (+/- 1)
            for lvl in ("sev2", "sev3"):
                assert abs(sum(v for (_t, l), v in c.items() if l == lvl) - n / 2) <= 2, (smp, q, lvl)
        share = {q: sum(c.values()) for q, c in cells.items()}
        tot = sum(share.values())
        for q, want in collections.Counter(P.YN_Q).items():
            assert abs(share[q] / tot - want / len(P.YN_Q)) < 0.03, (smp, q, share)


def test_twin_requests_are_exactly_two_of_every_five_per_class():
    for smp in TRAIN:
        for cls in ("yn|yn_reaches|1", "yn|yn_below|0", "ch|sev2"):
            got = [P._twin_slot(smp, cls, o) for o in range(100)]
            assert sum(r for r, _k in got) == 40
            assert sorted(k for r, k in got if r) == list(range(40))              # dense indices 0 .. 39


def test_a_non_reaching_yes_no_draw_never_picks_a_forced_reach_scenario():
    """exposure, floor and both always reach SEV2 / SEV3; v2 moved such draws to "maintenance" (a window on 43% of the
    non-reaching rows, which predicted the label). v3 draws among the other four at their weights."""
    by = collections.Counter()
    for smp in TRAIN:
        for seed in range(BASE, BASE + 600):
            pl = P.plan_of(smp, seed)
            if pl.kind == "yesno":
                by[(bool(pl.target), pl.scenario)] += 1
    assert not any(not reach and scen in P.FORCED_REACH for (reach, scen) in by), by
    non = {scen: n for (reach, scen), n in by.items() if not reach}
    tot = sum(non.values())
    assert abs(non["maintenance"] / tot - 0.14 / 0.71) < 0.05, non                  # 20%, not 43%
    assert {scen for (reach, scen) in by if reach} == set(P.SCENARIOS)


def test_the_plan_depends_on_the_seed_alone():
    a = [P.plan_of("S2", s) for s in range(BASE, BASE + 200)]
    assert a == [P.plan_of("S2", s) for s in range(BASE, BASE + 200)]
    assert a != [P.plan_of("S3", s) for s in range(BASE, BASE + 200)]


def test_row_shares_are_in_band(units):
    rows = [r for u in units if u.ok for r in u.rows]
    n = len(rows)
    yn = sum(r["qtype"] == "noul" for r in rows) / n
    assert 0.46 <= yn <= 0.56, yn                                                  # spec 3.0 band 45-55 (pilot: G10)
    roles = collections.Counter(r["role"] for r in rows)
    assert 0.19 <= roles["twin"] / n <= 0.26, roles                                 # spec 4.1: 20-25% (pilot: overlay)
    assert 0.05 <= roles["equiv"] / n <= 0.10, roles


# ------------------------------------------------------------------------------------------------ F1 / F2: twins

def test_every_unit_passes_every_program_gate(units):
    bad = [u.problems[:2] for u in units if not u.ok]
    assert not bad, bad[:5]


def test_twin_edits_are_one_slot_in_domain_and_cover_every_kind(plugin, specs):
    kinds = collections.Counter()
    for spec in list(specs.values())[:300]:
        crit = tuple(spec.structure["critical"])
        for slot, new in P.twin_edits(spec):
            twin = spec.with_slot(slot, new)
            assert slot_diff(spec, twin) == {slot}
            assert P.in_domain(twin.env(), crit) or slot in ("CHECK", "ACK")      # moves that leave R2 are filtered later
        for slot, new, sev2 in [P.twin_choice(spec, None)] if P.twin_choice(spec, None) else []:
            kinds[slot] += 1
    for spec in specs.values():
        for prop in plugin.relations(spec):
            if prop.kind == "twin":
                kinds["rel:" + prop.changed_slot] += 1
    for k in ("USERS", "URGENCY", "EXPOSED", "CHECK", "ACK"):
        assert kinds["rel:" + k] >= 3, kinds


def test_the_planned_twin_always_exists_and_flips_as_constructed(plugin, specs):
    n = 0
    for (smp, seed), spec in specs.items():
        plan = P.plan_of(smp, seed)
        props = [p for p in plugin.relations(spec) if p.kind == "twin"]
        assert bool(props) == plan.twin, (smp, seed)                                 # label-first: never lost
        for p in props:
            twin = plugin.derive(p.spec)
            assert slot_diff(spec, twin) == {p.changed_slot}
            assert plugin.solve_a(twin) == p.expect != plugin.solve_a(spec)
            assert P.in_domain(twin.env(), tuple(twin.structure["critical"]))
            if spec.qform == P.CHOICE_FORM:
                assert p.expect == plan.twin_to                                      # the planned level, exactly
            n += 1
    assert n > 100


def test_yes_no_twins_are_half_reaching_and_choice_twins_cover_every_level(plugin, specs):
    reach, lv = [], collections.Counter()
    for spec in specs.values():
        for p in plugin.relations(spec):
            if p.kind != "twin":
                continue
            if spec.qform == P.CHOICE_FORM:
                lv[p.expect] += 1
            else:
                twin = plugin.derive(p.spec)
                reach.append(P.severity(twin) <= int(twin.env()["LEVEL"][-1]))
    assert 0.40 <= sum(reach) / len(reach) <= 0.60, (sum(reach), len(reach))        # the pilot: 80% (94 of 117)
    assert set(lv) == set(P.SEV_KEYS) and max(lv.values()) <= 1.7 * min(lv.values()), lv   # the pilot: SEV4 10 of 88
    p = chi2_uniform_p([lv[k] for k in P.SEV_KEYS])
    assert p is None or p > 0.05, lv


def test_the_gold_position_of_all_choice_rows_is_uniform(units):
    from c2_kit.choiceplan import plan_report
    sets = [rr.option_set for u in units if u.ok for rr in u.rendered if rr.option_set is not None]
    rep = plan_report(sets)
    assert rep["positions_chi2_p"]["4"] > 0.05, rep["positions"]                    # the pilot: p 0.0049
    assert len(rep["positions"]["4"]) == 4


# ------------------------------------------------------------------------------------------------ F4: the card

def test_yes_no_rules_sit_in_row_card_and_choice_rules_in_the_instructions(units):
    seen = collections.Counter()
    for u in units:
        for r in u.rows:
            rules, question = CARDS.split_rules(r)
            assert P.CLOSED_WORLD in rules and P.CLOSED_WORLD not in question
            if r["qtype"] == "noul":
                assert r["card"] and r["instructions"] == question and "\n\n" not in question
                assert r["meta"]["defs_style"].startswith("rules_in_card_")
            else:
                assert not r["card"] and r["instructions"] == rules + "\n\n" + question
                assert r["meta"]["defs_style"].startswith("rules_in_instructions_")
            seen[r["meta"]["defs_style"].rsplit("_", 1)[1]] += 1
    assert 0.08 <= seen["short"] / sum(seen.values()) <= 0.22, seen                 # spec 3.0: about 15%


def test_a_partner_prints_the_same_card(units):
    n = 0
    for u in units:
        by = {r["id"]: r for r in u.rows}
        for r in u.rows:
            if r["role"] in ("complement", "equiv", "attack"):
                base = by[r["meta"]["twin_of"]]
                assert CARDS.split_rules(r)[0] == CARDS.split_rules(base)[0]
                n += 1
    assert n > 100


def test_solver_b_refuses_a_card_that_does_not_fit_the_record(plugin, ctx, specs):
    spec = next(s for s in specs.values() if "MW_START" not in s.slots and s.qform == P.CHOICE_FORM
                and s.structure["printed"])
    row = plugin.render(spec, ctx).row
    window = next(s for s in specs.values() if "MW_START" in s.slots and s.qform == P.CHOICE_FORM
                  and s.structure["printed"])
    other = plugin.render(window, ctx).row
    # the window card on a record with no window (and the reverse) is not the card of that record
    bad = dict(row, instructions=other["instructions"].rsplit("\n\n", 1)[0] + "\n\n" + row["instructions"].rsplit(
        "\n\n", 1)[1])
    with pytest.raises(B.ParseError):
        plugin.parse(bad, ctx)
    plugin.parse(row, ctx)


def test_real_token_mean_on_the_frozen_pool_is_within_the_bar(plugin):
    """Spec 3.0: family mean <= 800 rendered tokens (pinned tokenizer, instructions twice), max <= 2,000. Read-only use
    of the frozen pools; skipped when the tokenizer snapshot is absent."""
    mx, tok = CARDS._tokenizer()
    if tok is None:
        pytest.skip("pinned tokenizer not available")
    pctx, packs = H.load_pools()
    pl = P.T20Plugin(lexicon=pctx.lexicon, packs=packs)
    rows = []
    for k in range(260):
        u = pipeline.build_unit(pl, pl.sample(BASE + k // 4, TRAIN[k % 4]), pctx, run_g15=False)
        assert u.ok, u.problems[:2]
        rows += u.rows
    rep = CARDS.token_report(rows)
    assert rep["mean"] <= 800 and rep["max"] <= 2000, rep
    assert rep["after_placement"] == rep["mean"]                                    # nothing left to place


# ------------------------------------------------------------------------------------------------ F5: double negation

def test_program_double_negation_wordings_are_clean_and_solver_b_reads_them(plugin):
    assert P.PROGRAM_DN_WORDINGS == B.PROGRAM_DN and len(P.PROGRAM_DN_WORDINGS) >= 4
    for t in P.PROGRAM_DN_WORDINGS:
        c = negcount.count(t.replace("{INC_ID}", "INC-1").replace("{LEVEL}", "SEV2"))
        assert (c.k_all, c.k_syn) == (2, 2), t
        assert POL.form_problems(plugin, "yn_double_neg", t) == [], t
    for t in ("Isn't it the case that incident {INC_ID} does not reach {LEVEL} at the check time?",
              "Is it not the case that incident {INC_ID} fails to reach {LEVEL} at the check time?",
              "Is incident {INC_ID} not one that does not reach {LEVEL} at the check time?"):
        assert POL.form_problems(plugin, "yn_double_neg", t), t


def test_double_negation_rows_use_program_text_when_the_pool_has_no_clean_wording(plugin, ctx, specs):
    bare = FX.ctx(without=("W-DNEG-1",))
    dn = [s for s in specs.values() if s.qform == P.DOUBLE_NEG_FORM]
    assert len(dn) >= 5
    for spec in dn:
        for c, want in ((bare, None), (ctx, "W-DNEG-1")):
            rr = plugin.render(spec, c)
            assert rr.wording_id == want and rr.row["meta"]["wording_id"] == want
            assert ("program_wording" in rr.row["meta"]) == (want is None)                # the program text is traceable
            if want is None:
                assert rr.row["meta"]["program_wording"] in {f"T20-prog-dn-{i}" for i in range(4)}
            q = CARDS.split_rules(rr.row)[1]
            assert negcount.count(q).k_syn == 2
            view = plugin.parse(rr.row, c)
            assert view["qform"] == P.DOUBLE_NEG_FORM
            reaches = P.severity(spec) <= int(spec.env()["LEVEL"][-1])
            assert plugin.solve_b(view) == rr.row["gold"] == int(reaches) == plugin.solve_a(spec)
    units = [pipeline.build_unit(plugin, s, bare, run_g15=False) for s in dn]
    assert all(u.ok for u in units), [u.problems[:2] for u in units if not u.ok][:3]


def test_the_double_negation_complement_partner_is_yn_not_reaches(plugin, specs):
    parts = {p.qform for s in specs.values() if s.qform == P.DOUBLE_NEG_FORM for p in plugin.relations(s)
             if p.kind == "complement"}
    assert parts == {"yn_not_reaches"}


def test_double_negation_share_of_yes_no_rows(units):
    yn = [r for u in units if u.ok for r in u.rows if r["qtype"] == "noul"]
    dn = sum(r["meta"]["qform"] == P.DOUBLE_NEG_FORM for r in yn)
    assert dn / len(yn) >= 0.02, (dn, len(yn))                                      # spec 3.0: >= 2% of yes/no rows


# ------------------------------------------------------------------------------------------------ F6: roles, quarantine

def test_the_reporter_role_rule_matches_the_g3h_evidence():
    ctx_, _packs = H.load_pools()
    fr = [s for s in ctx_.skins.values() if s.kind == "skin" and s.author_mode == "F" and not s.held_out]
    rejected = {s.skin_id for s in fr if ROLES.reporter_problems(s.text, dict(s.brief)["REPORTER"])}
    assert rejected == set(QR.G3H_QUARANTINE), sorted(rejected ^ set(QR.G3H_QUARANTINE))     # 10 + 3 borderline
    assert len(fr) - len(rejected) == 33                                                    # no over-rejection


def test_ctx_for_leaves_out_the_quarantined_templates_and_nothing_else(plugin):
    pctx, packs = H.load_pools()
    pl = P.T20Plugin(lexicon=pctx.lexicon, packs=packs)
    bad = pl.quarantined(pctx)
    screened = pl.ctx_for(None, pctx)
    assert set(bad) == set(pctx.skins) - set(screened.skins)
    assert set(QR.QUARANTINE) <= set(bad)
    held_f = {s.skin_id for s in pctx.skins.values() if s.kind == "skin" and s.author_mode == "F" and s.held_out}
    assert held_f & set(bad)                                         # the rule also covers the held-out notes (S5)
    wordings = [s for s in pctx.skins.values() if s.kind == "wording"]
    flagged = {s.skin_id for s in wordings if POL.form_problems(pl, s.qform, s.text)}
    assert len(flagged) == 3 and all(pctx.skins[i].qform == "yn_not_reaches" for i in flagged)   # P4 strict frames
    assert flagged | {"T20-wor-38f9393e8c"} == {i for i in bad if pctx.skins[i].kind == "wording"}
    counts = collections.Counter(s.qform for s in screened.skins.values() if s.kind == "wording")
    assert counts["yn_not_reaches"] >= 6 and counts["yn_fails"] >= 6 and counts["yn_below"] >= 6      # G0 targets stay met
    assert counts["yn_reaches"] >= 18 and counts["ch_sev"] >= 18
    rows = []
    for k in range(80):
        u = pipeline.build_unit(pl, pl.sample(BASE + k // 4, TRAIN[k % 4]), pctx, run_g15=False)
        assert u.ok, u.problems[:2]
        rows += u.rows
    used = {r["meta"]["wording_id"] for r in rows} | {r["meta"]["c2"]["skin_id"] for r in rows}
    assert not used & set(bad)


# ------------------------------------------------------------------------------------------------ determinism

def test_rows_are_identical_under_two_hash_seeds():
    code = ("import sys, json, hashlib\nsys.path.insert(0, %r)\nsys.dont_write_bytecode = True\n"
            "from c2_kit import pipeline\nfrom transfer.T20 import fixtures as FX, plugin as P\n"
            "ctx = FX.ctx(); pl = P.T20Plugin(lexicon=ctx.lexicon); out = []\n"
            "for smp in ('S1', 'S2', 'S3', 'S4'):\n"
            "    for seed in range(900000, 900016):\n"
            "        u = pipeline.build_unit(pl, pl.sample(seed, smp), ctx, run_g15=False)\n"
            "        out += [json.dumps(r, sort_keys=True) for r in u.rows] + [str(u.ok)]\n"
            "print(hashlib.sha256('\\n'.join(out).encode()).hexdigest())\n") % str(C2_BUILD)
    got = []
    for hs in ("1", "4242"):
        r = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, cwd=str(C2_BUILD),
                           env={**os.environ, "PYTHONHASHSEED": hs}, timeout=600)
        assert r.returncode == 0, r.stderr[-500:]
        got.append(r.stdout.strip())
    assert got[0] == got[1] and len(got[0]) == 64
    assert hashlib.sha256(b"x").hexdigest()                          # (hashlib import kept for the shape of the check)
