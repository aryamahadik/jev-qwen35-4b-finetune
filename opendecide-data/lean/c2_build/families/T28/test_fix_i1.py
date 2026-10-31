"""In-memory tests of the T28 Stage B fix iteration 1 (14 Oct 2026; G0_SPEC.md v1.2 section 10). Nothing is written.

  cards      S23: the rules print once (row.card on yes/no rows, the head of the instructions on choice rows), two styles
             (full 85% / short 15%, one per relation unit), every short line keeps its rule (cards.variant_problems),
             solver B reads both
  balance    yes/no targets by the g index: a block holds exactly 9 yes and 9 no targets; overlay partners and twin
             targets are hashed per slot group, so a group cancels
  plans      ch_rule: n and the default option's gold outcome from the row key (1/k); ch_inverted: the calls listed in
             the state, the options "Call i" (no option text carries the call)
  deals      cards = (sampler, pack) over circular pack windows; registers and skins dealt
  polarity   R2 on the frozen wordings: exactly one flagged, nothing over-rejected, every form keeps >= 6
  pins       G0 v1.2 sha, the authored v1.1 copy and its sha, <= 200 lines
Run (from lean/):  ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T28/test_fix_i1.py
"""
from __future__ import annotations

import collections
import dataclasses
import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import cards as CARDS  # noqa: E402
from c2_kit import choiceplan as CP  # noqa: E402
from c2_kit import pipeline  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit.distractors import uhash  # noqa: E402
from families.T28 import fixtures as FX  # noqa: E402
from families.T28 import plugin as P  # noqa: E402
from families.T28 import solver_b as B  # noqa: E402

HERE = Path(__file__).resolve().parent
TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T28Plugin(lexicon=ctx.lexicon)


# ------------------------------------------------------------------------------------------------ cards (S23)

def test_rules_print_once_where_the_prompt_prints_them(plugin, ctx):
    styles = collections.Counter()
    for smp in TRAIN:
        for seed in range(0, 200, 3):
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            row = rr.row
            style = plugin.card_style(spec)
            if row["qtype"] == "noul":
                assert row["card"] and "\n\n" not in row["instructions"]
                assert row["instructions"] == ctx.skin(row["meta"]["wording_id"]).fill(
                    spec.all_slots(), rr.forms).text
                field = "card"
            else:
                assert not row["card"] and row["instructions"].count("\n\n") == 1
                field = "instructions"
            rules, question = CARDS.split_rules(row)
            assert rules.startswith(P.MATCH_SHORT if style == "short" else P.MATCH_LINE)
            assert rules.endswith(P.CLOSED_WORLD) and "\n" not in question
            assert row["meta"]["defs_style"] == f"rules_in_{field}_{style}"
            styles[style] += 1
    assert set(styles) == {"full", "short"}


def test_card_style_share_and_unit_consistency(plugin, ctx):
    c = collections.Counter(CARDS.draw_style(f"T28|{seed}|S1|card", P.CARD_SHARES) for seed in range(20000))
    assert 0.14 <= c["short"] / sum(c.values()) <= 0.16, c         # capped at the G0 share (spec 3.0: about 15%)
    with pytest.raises(CARDS.CardError):
        CARDS.draw_style("k", {"full": 0.8, "short": 0.2})
    for seed in range(60):                                         # one style for a whole relation unit
        for smp in TRAIN:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            assert res.ok, res.problems[:2]
            assert len({r["meta"]["defs_style"].rsplit("_", 1)[1] for r in res.rows}) == 1


def test_short_card_lines_keep_the_rules():
    pairs = [("match", P.MATCH_LINE, P.MATCH_SHORT), ("owner", P.OWNER_LINE, P.OWNER_SHORT),
             ("verdicts", P.VERDICT_LINE, P.VERDICT_SHORT)]
    pairs += [(f"spec_{k}", P.SPEC_LINE[k], P.SPEC_SHORT[k]) for k in P.SPEC_LINE]
    for name, full, short in pairs:
        assert CARDS.variant_problems(full, short) == [], name
        assert len(short) < len(full), name
    # solver B's own copies of the short lines are the plugin's (the two modules were written apart)
    assert B.LINE_MATCH_SHORT == P.MATCH_SHORT and B.LINE_VERDICTS_SHORT == P.VERDICT_SHORT
    assert B.LINE_OWNER_SHORT == P.OWNER_SHORT
    assert set(B.LINE_SPEC_SHORT) == set(P.SPEC_SHORT.values())


def test_solver_b_reads_both_styles(plugin, ctx):
    seen = collections.Counter()
    for smp in TRAIN:
        for seed in range(400):
            spec = plugin.sample(seed, smp)
            style = plugin.card_style(spec)
            if seen[style] >= 120:
                continue
            seen[style] += 1
            rr = plugin.render(spec, ctx)
            view = plugin.parse(rr.row, ctx)
            facts = {k: v for k, v in view.items() if k != "options"}
            assert facts == plugin.canonical_for(spec, rr.row["meta"]["c2"]["author_mode"]), (seed, smp, style)
            assert plugin.solve_b(view) == plugin.solve_a(spec) == rr.answer
    assert min(seen.values()) >= 100


def test_mixed_style_cards_are_refused(plugin, ctx):
    spec = next(s for s in (plugin.sample(seed, "S1") for seed in range(400))
                if plugin.card_style(s) == "full" and s.qform == "ch_verdict")
    rr = plugin.render(spec, ctx)
    row = dict(rr.row)
    row["instructions"] = row["instructions"].replace(P.MATCH_LINE, P.MATCH_SHORT, 1)     # a short head, full lines
    with pytest.raises(B.ParseError):
        plugin.parse(row, ctx)


def test_short_rows_are_shorter(plugin, ctx):
    full, short = [], []
    for seed in range(0, 400, 2):
        spec = plugin.sample(seed, "S1")
        rr = plugin.render(spec, ctx, skin=ctx.skin("SK-MEMO-1"))
        (short if plugin.card_style(spec) == "short" else full).append(len(rr.row["card"] or rr.row["instructions"]))
    assert short and full and sum(short) / len(short) < 0.97 * sum(full) / len(full)


# ------------------------------------------------------------------------------------------------ balance

def _slot_of(seed):
    return seed % len(P.QFORM_SLOTS)


def test_each_block_holds_nine_yes_and_nine_no_targets(plugin):
    for smp in ("S1", "S3"):
        for b in range(6):
            yes = no = 0
            for slot in range(len(P.QFORM_SLOTS)):
                if P.QFORM_SLOTS[slot] not in P.YN:
                    continue
                spec = plugin.sample(40 * b + slot, smp)
                a = plugin.solve_a(spec)
                yes += a == 1
                no += a == 0
            assert (yes, no) == (9, 9), (smp, b, yes, no)


def test_g_index_pairs_have_opposite_targets():
    yn_slots = [i for i, q in enumerate(P.QFORM_SLOTS) if q in P.YN]
    assert len(yn_slots) == 18 and [P.SLOT_G[i] for i in yn_slots] == list(range(18))
    for b in range(10):
        for m in range(9):
            a, c = yn_slots[2 * m], yn_slots[2 * m + 1]
            ya = (P.SLOT_G[a] + b) % 2 == 0
            yc = (P.SLOT_G[c] + b) % 2 == 0
            assert ya != yc


def test_group_keys_pair_yes_no_slots_and_triple_verdict_slots():
    keys = collections.defaultdict(list)
    for slot in range(40):
        keys[P.T28Plugin._group_key(1200 + slot, "S2")].append(slot)
    sizes = collections.Counter(len(v) for v in keys.values())
    assert sizes == {2: 9, 3: 5, 1: 7}      # 9 yes/no pairs; 5 verdict triples; 1 leftover verdict + 4 ch_rule + 2 inverted
    for g, slots in keys.items():
        qs = {P.QFORM_SLOTS[s] for s in slots}
        if g[2] == "yn":
            assert len(slots) == 2 and all(q in P.YN for q in qs)
        elif g[2] == "v":
            assert qs == {"ch_verdict"} and len(slots) <= 3


def test_overlay_is_hashed_per_group(plugin, ctx):
    """The two units of a yes/no pair (and the three of a verdict triple) get the same complement / equiv / inv
    decisions, so their golds cancel; a twin is proposed for every member unless no edit exists (feasibility)."""
    twin_miss = groups_n = 0
    for smp in ("S1", "S4"):
        for b in (3, 4):
            groups = collections.defaultdict(list)
            for slot in range(34):
                seed = 40 * b + slot
                spec = plugin.sample(seed, smp)
                kinds = {p.kind for p in plugin.relations(spec) if p.kind != "metamorphic"}
                groups[plugin._group_key(seed, smp)].append((frozenset(kinds & {"complement", "equiv", "inv"}),
                                                             "twin" in kinds))
            for g, v in groups.items():
                assert len({k for k, _ in v}) == 1, (g, v)
                groups_n += 1
                twin_miss += len({t for _, t in v}) > 1
    assert twin_miss <= 2 and groups_n > 40, (twin_miss, groups_n)


def test_exact_yes_rate_and_verdict_thirds_on_built_units(plugin, ctx):
    rows = []
    for seed in range(0, 160):
        res = pipeline.build_unit(plugin, plugin.sample(seed, "S1"), ctx, run_g15=False)
        assert res.ok
        rows += res.rows
    yn = [r for r in rows if r["qtype"] == "noul"]
    assert abs(sum(r["gold"] for r in yn) - len(yn) / 2) <= 3, (sum(r["gold"] for r in yn), len(yn))
    ver = collections.Counter(r["gold"] for r in rows if r["meta"]["qform"] == "ch_verdict"
                              and r["gold"] in P.VERDICT_TEXT.values())
    n = sum(ver.values())
    assert all(abs(ver[v] / n - 1 / 3) <= 0.06 for v in P.VERDICT_TEXT.values()), ver


def test_twin_targets_of_a_verdict_triple_are_distinct(plugin):
    for smp in TRAIN:
        for b in range(6):
            for m in range(5):                                           # the five full triples of the block
                wants, bases = [], []
                for j in range(3 * m, 3 * m + 3):
                    spec = plugin.sample(40 * b + j, smp)
                    base = plugin._predict(spec)
                    assert base == P.EFFECTS[(j + b) % 3]
                    bases.append(base)
                    wants.append(plugin._twin_want(spec, base))
                assert len(set(bases)) == 3 and len(set(wants)) == 3
                assert all(w != x for w, x in zip(wants, bases))


def test_twins_reach_their_planned_class_most_of_the_time(plugin):
    hit = tot = 0
    for smp in TRAIN:
        for seed in range(0, 480, 2):
            spec = plugin.sample(seed, smp)
            if spec.qform not in ("ch_verdict", "ch_rule"):
                continue
            base = plugin._predict(spec)
            want = plugin._twin_want(spec, base)
            t = plugin._twin(spec)
            if t is None:
                continue
            tot += 1
            hit += plugin._twin_fits(want, t.expect, base)
    assert tot >= 150 and hit / tot >= 0.80, (hit, tot)


# ------------------------------------------------------------------------------------------------ plans

def test_rule_plan_is_one_over_k_and_the_structure_follows_it(plugin):
    cell = collections.defaultdict(lambda: [0, 0])
    for smp in TRAIN:
        lo, hi = P.SAMPLER_CFG[smp]["n"]
        for seed in range(30000):
            plan = plugin._rule_plan(seed, smp)
            assert lo <= plan.closed <= hi and plan.k == plan.closed + 1 and plan.show_abstain
            cell[plan.k][0] += 1
            cell[plan.k][1] += plan.gold_abstain
    for k, (n, a) in sorted(cell.items()):
        assert CP.binom_two_sided(a, n, 1 / k) > 0.001, (k, n, a)
    checked = 0
    for smp in TRAIN:
        for b in range(25):
            for slot in range(34, 38):
                seed = 40 * b + slot
                spec = plugin.sample(seed, smp)
                assert spec.qform == "ch_rule"
                plan = plugin._rule_plan(seed, smp)
                assert len(spec.structure["rules"]) == plan.closed
                assert (plugin.solve_a(spec) == "default") == plan.gold_abstain
                assert (spec.slots["DEFAULT"].value in P.EFFECTS)
                checked += 1
    assert checked == 400


def test_rule_rows_show_the_default_option_in_one_order(plugin, ctx):
    for smp in TRAIN:
        for seed in range(34, 400, 40):
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            opts = rr.row["options"]
            assert P.DEFAULT_OPTION in opts and len(opts) == len(spec.structure["rules"]) + 1
            assert rr.option_set.meta["abstain_key"] == "default" and rr.option_set.abstain_shown
            assert (rr.row["gold"] == P.DEFAULT_OPTION) == rr.option_set.meta["gold_is_abstain"]
            assert opts.index(rr.row["gold"]) == rr.option_set.gold_index


def test_inverted_rows_list_the_calls_and_label_the_options(plugin, ctx):
    """G0 v1.2 S20: no option text carries the call (the Stage B 5,000-row G6 card view read the gold call off its
    overlap with the policy: +36 pp on these rows); the state lists the calls, the options are "Call i"."""
    pos = collections.defaultdict(collections.Counter)
    n = 0
    for smp in TRAIN:
        for b in range(60):
            for slot in (38, 39):
                spec = plugin.sample(40 * b + slot, smp)
                rr = plugin.render(spec, ctx)
                row = rr.row
                k = len(spec.structure["candidates"])
                assert 3 <= k <= 5 and k <= P.INVERTED_K[int(uhash(P.FAMILY, "k_inverted", spec.seed, spec.sampler) * 4)]
                block = [c for c in row["state"].split("\n\n") if c.startswith(P.CALLS_HEAD)]
                assert len(block) == 1 and "Proposed call" not in row["state"]
                lines = block[0].split("\n")[1:]
                assert [ln.split(":")[0] for ln in lines] == [f"Call {i}" for i in range(1, k + 1)]
                assert sorted(row["options"]) == [f"Call {i}" for i in range(1, k + 1)]
                assert all("(" not in o and "." not in o for o in row["options"])
                view = plugin.parse(row, ctx)
                gold_label = int(row["gold"].split()[1])
                assert view["options"][row["options"].index(row["gold"])] == plugin.solve_a(spec)
                assert plugin.solve_a(spec) in view["candidates"] and len(view["candidates"]) == k
                assert pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False) == []
                pos[k][gold_label] += 1
                n += 1
    assert n == 480
    for k, c in pos.items():                         # the gold's list position is uniform (label-blind shuffle)
        if sum(c.values()) >= 6 * k:
            assert CP.chi2_uniform_p([c[i] for i in range(1, k + 1)]) > 0.001, (k, dict(c))


# ------------------------------------------------------------------------------------------------ deals

def _packs(n):
    return [dict(P.PACKS[i % 5], id=f"pk-x{i:02d}", **({"held_out": True} if i >= n - 10 else {})) for i in range(n)]


def test_cards_are_sampler_pack_windows(ctx):
    pl = P.T28Plugin(lexicon=ctx.lexicon, packs=_packs(56))                   # 46 training + 10 held-out packs
    pools = {s: [p["id"] for p in pl._pack_pool(s)] for s in pl.SAMPLERS}
    assert {len(v) for s, v in pools.items() if s != "S5"} == {18}
    assert len(pools["S5"]) == 10 and all(p["held_out"] for p in pl._pack_pool("S5"))
    cover = collections.Counter(p for s, v in pools.items() if s != "S5" for p in v)
    assert set(cover) == {p["id"] for p in pl._train_packs} and set(cover.values()) == {1, 2}
    assert sum(cover.values()) == 72                                          # 72 cards of one (sampler, pack) each
    cards = set()
    for smp in TRAIN:
        for seed in range(0, 1200, 3):
            spec = pl.sample(seed, smp)
            assert spec.card_id == f"T28:{smp}:{spec.pack}" and spec.pack in pools[smp]
            cards.add(spec.card_id)
    assert len(cards) == 72
    small = P.T28Plugin(lexicon=ctx.lexicon)                                  # the 5 stand-in training packs
    assert all(len(small._pack_pool(s)) == 2 for s in TRAIN)


def test_registers_are_dealt_once_per_run_of_eight_seeds(plugin, ctx):
    for smp in TRAIN:
        regs = []
        for seed in range(0, 160):
            sk = plugin._deal_skin(ctx, plugin.sample(seed, smp))
            regs.append(sk.register)
        for g in range(20):
            run = regs[8 * g:8 * g + 8]
            assert sorted(run) == sorted(r for r in plugin.REGISTERS if r not in plugin.HELD_OUT_REGISTERS), run
    held = {plugin._deal_skin(ctx, plugin.sample(seed, "S5")).register for seed in range(0, 20)}
    assert held == set(plugin.HELD_OUT_REGISTERS)


def test_skins_are_used_once_each_before_any_repeats(plugin, ctx):
    base = ctx.skin("SK-MEMO-1")
    extra = {f"SK-MEMO-X{i}": dataclasses.replace(base, skin_id=f"SK-MEMO-X{i}") for i in range(12)}
    big = KP.KitCtx(skins={**ctx.skins, **extra}, lexicon=ctx.lexicon)
    use = collections.Counter()
    for seed in range(0, 8 * 26):
        sk = plugin._deal_skin(big, plugin.sample(seed, "S1"))
        if sk.register == "memo":
            use[sk.skin_id] += 1
    assert len(use) == 13 and set(use.values()) == {2}            # 26 memo units over 13 skins: each exactly twice


# ------------------------------------------------------------------------------------------------ polarity (R2)

def test_polarity_is_configured_and_screens_the_fixture_pool_clean(plugin, ctx):
    assert plugin.POLARITY_CHECK and plugin.POLARITY_SKIP == ("yn_deny_ant",)
    assert POL.config_problems(plugin) == []
    assert plugin.quarantined_wordings(ctx) == {}                  # nothing over-rejected in the fixture style
    screened = plugin.ctx_for(None, ctx)
    assert screened is ctx


def test_polarity_flags_the_wrong_class_and_keeps_the_frozen_wordings():
    pl = P.T28Plugin(lexicon=FX.ctx().lexicon)
    bad = {
        "yn_mustnot": ["Under this policy, does the agent's outcome for this call amount to a flat ban, given it "
                       "must not make the call even if the user confirms it?"],
        "yn_deny": ["Is this call barred whatever the user says, so that the agent does not have to turn it down?",
                    "Isn't the agent bound to turn this call down whatever the user says?"],
        "yn_allow_syn": ["Is the agent not blocked from making this call on its own, skipping any check?"],
        "yn_mustnot_syn": ["Is it the case that the agent must not make this call, even if the user confirms it?"],
    }
    for q, texts in bad.items():
        for t in texts:
            assert POL.form_problems(pl, q, t), (q, t)
    good = {"yn_mustnot": "Under the policy, is this call something the agent mustn't make, whatever the user says?",
            "yn_mustnot_syn": "Under the policy, is it not the case that the agent must not make this call?",
            "yn_deny_syn": "Under this policy, does the agent not have to turn this call down, whatever the user says?",
            "yn_allow_syn": "Under the policy, is the agent not allowed to make this call on its own?",
            "yn_deny_ant": "Under the policy, may the agent make this call either on its own or after the user confirms?"}
    for q, t in good.items():
        assert POL.form_problems(pl, q, t) == [], (q, t)


def test_polarity_on_the_frozen_pool_flags_exactly_one_wording():
    pl = P.T28Plugin(lexicon=FX.ctx().lexicon)
    pool = json.loads((HERE / "pools_v2" / "wordings.json").read_text(encoding="utf-8"))["wordings"]
    flagged, per_form = [], collections.Counter()
    for w in pool:
        p = POL.form_problems(pl, w["qform"], w["text"])
        if p:
            flagged.append((w["form_id"], w["qform"], p))
        else:
            per_form[w["qform"]] += 1
    assert [(f, q) for f, q, _ in flagged] == [("q.t28.yn_mustnot#3dfd0fe3", "yn_mustnot")]
    assert len(pool) == 209 and set(per_form) == set(pl.QFORMS)
    assert min(per_form.values()) >= 6 and per_form["yn_mustnot"] == 12


# ------------------------------------------------------------------------------------------------ pins

def test_g0_v12_pins():
    g0 = (HERE / "G0_SPEC.md").read_bytes()
    assert hashlib.sha256(g0).hexdigest() == P.T28Plugin.G0_SHA256
    authored = (HERE / "G0_SPEC.v1_1.md").read_bytes()
    assert hashlib.sha256(authored).hexdigest() == P.T28Plugin.G0_SHA256_AUTHORED
    assert P.T28Plugin.G0_SHA256 != P.T28Plugin.G0_SHA256_AUTHORED
    assert len(g0.decode().splitlines()) <= 200
    txt = g0.decode()
    for needle in ("## 10. v1.2", "S23", "R2 (v1.2", "Overlay and deal (v1.2)", "1/k"):
        assert needle in txt, needle
