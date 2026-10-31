"""families/T24/test_balance.py: the ch_v2 gold-role balance (PILOT_VERDICT F3; G0 v2.2 section 2 Balance) and the
skin deal (F4), in memory.

Run (from lean/):  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T24/test_balance.py
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

from c2_kit import pipeline  # noqa: E402
from families.T24 import balance_check as BC  # noqa: E402
from families.T24 import fixtures as FX  # noqa: E402
from families.T24 import plugin as T  # noqa: E402


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return T.T24Plugin(lexicon=ctx.lexicon, packs=T.STANDIN_PACKS)


def test_choice_roles_are_uniform_inside_each_option_bucket(plugin):
    """All choice rows (bases, equiv partners, twins) of 1,500 seeds x 4 samplers: k = 2 pos / neg 50 / 50 and k = 3
    1/3 each within +-3 pp, and P(change | role) in 0.45-0.55 for pos and neg (G0 Balance)."""
    rep = BC.choice_role_report(plugin, 1500, seed0=60000)
    a = rep["all"]
    assert a[2]["n"] > 2000 and a[3]["n"] > 2000
    assert abs(a[2]["pos"] - 0.5) <= 0.03 and abs(a[2]["neg"] - 0.5) <= 0.03, a[2]
    for r in T.ROLES:
        assert abs(a[3][r] - 1 / 3) <= 0.03, a[3]
    pc = rep["p_change_given_role_any_k"]
    assert 0.45 <= pc["pos"] <= 0.55 and 0.45 <= pc["neg"] <= 0.55, pc


def test_a_ch_v2_twin_aims_at_a_label_blind_role(plugin):
    """plugin.twin_role draws from the spec's own key over the roles V2 can give other than the base row's (alt only
    when V2 holds a condition clause); a twin reaches it whenever a candidate does, and always differs from the base."""
    seen, hit, n = collections.Counter(), 0, 0
    for seed in range(400):
        for smp in T.TRAIN_SAMPLERS:
            spec = plugin.sample(seed, smp)
            if spec.qform != "ch_v2":
                continue
            base = T.outcome_a(spec, 2)
            target = plugin.twin_role(spec, T.facts(spec)[2], base)
            assert target != base and (target != "alt" or "alt" in spec.structure["v2"])
            assert plugin.twin_role(spec, T.facts(spec)[2], base) == target             # a function of the key only
            t = plugin.twin(spec)
            if t is not None:
                assert t.expect != base and plugin.solve_a(plugin.derive(t.spec)) == t.expect
                n += 1
                hit += t.expect == target
                seen[t.expect] += 1
    assert n > 300 and hit / n >= 0.80, (hit, n)
    assert set(seen) == set(T.ROLES)


def test_skin_deal_caps_rows_per_skin_and_register_share(plugin, ctx):
    """F4: on consecutive seeds the deal gives every skin one more unit only after all the skins of its register have
    been used, and the registers share the units round robin (<= 15% each; spec 3.0)."""
    units = [(seed, smp) for seed in range(300) for smp in T.TRAIN_SAMPLERS]
    picks = [plugin.pick_skin(plugin.sample(seed, smp), ctx, False) for seed, smp in units]
    per_skin = collections.Counter(p.skin_id for p in picks)
    per_reg = collections.Counter(p.register for p in picks)
    regs = {p.register for p in ctx.skins.values() if p.kind == "skin" and not p.held_out}
    assert set(per_reg) == regs
    assert max(per_reg.values()) / len(picks) <= 0.15, per_reg
    by_reg = collections.Counter(p.register for p in ctx.skins.values() if p.kind == "skin" and not p.held_out)
    cycles = {r: -(-per_reg[r] // by_reg[r]) for r in regs}                        # visits / skins, rounded up
    for p in set(picks):
        assert per_skin[p.skin_id] <= cycles[p.register], (p.skin_id, per_skin[p.skin_id], cycles)
    assert [plugin.pick_skin(plugin.sample(s, m), ctx, False).skin_id for s, m in units[:40]] == [
        x.skin_id for x in picks[:40]]                                              # a function of seed and sampler
    held = [plugin.pick_skin(plugin.sample(s, "S5"), ctx, True) for s in range(40)]
    assert all(h.held_out for h in held)


def test_polarity_screen_keeps_the_pool_wordings_and_quarantines_the_ruled_one(plugin, ctx):
    """Kit item 3: every training and held-out yes/no wording of the fixtures passes P1-P3 with the family's antonym
    lexicon; the lead's ruling removes exactly the one held-out yn_dneg wording from a context that holds it."""
    from dataclasses import replace
    assert plugin.quarantined_wordings(ctx) == {}
    text = next(iter(T.QUARANTINED_WORDINGS))
    sk = replace(ctx.skin("WH-DNEG-1"), skin_id="WH-DNEG-RULED", text=text)
    c2 = replace(ctx, skins={**ctx.skins, sk.skin_id: sk})
    bad = plugin.quarantined_wordings(c2)
    assert set(bad) == {"WH-DNEG-RULED"} and "lead ruling" in bad["WH-DNEG-RULED"][0]
    assert "WH-DNEG-RULED" not in plugin.ctx_for(plugin.sample(3, "S5"), c2).skins
    spec = plugin.sample(3, "S5")
    res = pipeline.build_unit(plugin, spec, c2, run_g15=False)
    assert res.ok, res.problems[:2]


def test_dealt_k_and_role_cells_are_fair_for_bases_and_hold_in_every_card(plugin):
    """Fix iteration 2: (k, role) is dealt together from the seed. Over the base choice rows each cell sits at its
    share (k = 2: 1/4 each of POS / NEG; k = 3: 1/6 each) within 2 pp, each role is 1/k within each k (2 pp), and
    P(change | role) holds 0.45-0.55 including ALT; no seed is dropped."""
    cnt, chg, n = collections.Counter(), collections.Counter(), 0
    for seed in range(70000, 70700):
        for smp in T.TRAIN_SAMPLERS:
            spec = plugin.sample(seed, smp)                  # never raises: the dealt role is not dropped
            if spec.qform != "ch_v2":
                continue
            cell = (BC.option_bucket(spec), T.outcome_a(spec, 2))
            cnt[cell] += 1
            chg[(cell[1], T.outcome_a(spec, 1) != cell[1])] += 1
            n += 1
    for cell, share in T.CELLS:
        assert abs(cnt[cell] / n - share) <= 0.02, (cell, cnt)
    for k in (2, 3):
        tot = sum(v for (kk, _r), v in cnt.items() if kk == k)
        for (kk, r), v in cnt.items():
            if kk == k:
                assert abs(v / tot - 1 / k) <= 0.02, (k, r, v / tot)
    for r in T.ROLES:
        assert 0.45 <= chg[(r, True)] / (chg[(r, True)] + chg[(r, False)]) <= 0.55, chg


def test_edit_joint_marginals_are_the_plan_and_the_roles(plugin):
    """_edit_joint: the role marginal is exactly 1/k and the (kind, mode) marginal is the G0 plan table (alt edits only
    on k = 3), summed over the two k cells."""
    for material, table in ((True, T.YES_PLAN), (False, T.NO_PLAN)):
        marg = collections.Counter()
        for k, wk in ((2, 0.5), (3, 0.5)):
            entries, roles, J = T._edit_joint(material, k)
            for j in range(len(roles)):
                assert abs(sum(J[i][j] for i in range(len(entries))) - 1 / k) < 1e-6
            for i, e in enumerate(entries):
                marg[e] += wk * sum(J[i])
        for e, p in table:
            assert abs(marg[e] - p) < 1e-6, (e, marg[e], p)


def test_planned_position_is_uniform_in_each_k_and_k_follows_the_deal(ctx, plugin):
    """Rendered ch_v2 base rows: the options are the roles of the dealt k, the gold sits at plan_choice's position, and
    the position is uniform inside each k (chi-square on the counts, alpha 0.001)."""
    from c2_kit.choiceplan import chi2_uniform_p, plan_choice
    pos = {2: collections.Counter(), 3: collections.Counter()}
    for seed in range(71000, 71250):
        for smp in T.TRAIN_SAMPLERS:
            spec = plugin.sample(seed, smp)
            if spec.qform != "ch_v2":
                continue
            row = plugin.render(spec, ctx)
            os_ = row.option_set
            k = BC.option_bucket(spec)
            key = f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"
            assert os_.meta["k"] == k == len(os_.options)
            assert os_.gold_index == plan_choice(key, closed=k).pos
            pos[k][os_.gold_index] += 1
    for k, c in pos.items():
        p = chi2_uniform_p([c[i] for i in range(k)])
        assert p is None or p > 0.001, (k, c, p)


def test_wording_deal_balances_yes_and_no_inside_every_form_wording_cell(plugin, ctx):
    """Fix iteration w9 (A49 d): yes/no wordings are dealt label-first by rank inside (form, gold label) groups, so the
    yes and no counts of any (form, wording) cell differ by at most the rows by which the form's yes and no counts in
    the block differ; the dealt label equals the sampled gold; a wording is used at most ceil(rows / wordings) times
    per block and form; the deal depends on the seed alone."""
    sctx = plugin._screened_ctx(ctx)
    seeds = range(8 * T.WORD_BLOCK, 9 * T.WORD_BLOCK)
    cells = collections.defaultdict(lambda: [0, 0])
    per_group = collections.Counter()
    use = collections.Counter()
    for seed in seeds:
        qform, g, pq, pg = plugin._deal_of(seed, "S1")
        for form, grp in ((qform, g), (pq, pg)):
            if form is None:
                continue
            spec = type("S", (), {"seed": seed, "sampler": "S1", "qform": form})()
            w = plugin._dealt_wording(sctx, spec, False)
            assert w is not None and w.qform == form and not w.held_out
            assert w is plugin._dealt_wording(sctx, spec, False)
            use[(form, w.skin_id)] += 1
            per_group[grp] += 1
            if plugin.QFORMS[form].qtype == "noul":
                cells[(form, w.skin_id)][grp[1]] += 1
    for form in {f for f, _ in cells}:
        diff = abs(per_group[(form, 0)] - per_group[(form, 1)])
        off = sum(abs(a - b) for (f, _w), (a, b) in cells.items() if f == form)
        assert off <= diff + 1, (form, off, diff)
    for form in {f for f, _ in use}:
        n_f = sum(c for (f, _w), c in use.items() if f == form)
        n_w = len({w for (f, w) in use if f == form})
        pool = len([s for s in sctx.skins.values() if s.family == "T24" and s.kind == "wording" and s.qform == form
                    and not s.held_out])
        assert max(c for (f, _w), c in use.items() if f == form) <= -(-n_f // pool) + 1, (form, n_f, pool, n_w)


def test_dealt_label_equals_the_solved_gold(plugin):
    for seed in range(60000, 60120):
        sp = plugin.sample(seed, "S2")
        qform, g, _pq, _pg = plugin._deal_of(seed, "S2")
        assert sp.qform == qform
        if plugin.QFORMS[qform].qtype == "noul":
            assert int(plugin.solve_a(sp)) == g[1]


def test_twin_plan_gives_equal_twin_counts_in_both_directions_per_form(plugin):
    """Fix iteration w9: per yes/no form and block the minimal-edit twins with gold yes and gold no are equal in number
    (Q = min(available per direction, cap)), so the twin rows no longer tilt the question form's yes rate; the twin
    share per yes/no seed stays near the old 0.35; the plan depends on (sampler, block) only."""
    tw = collections.Counter()
    n = collections.Counter()
    base = 40 * T.TWIN_BLOCK
    for sampler in ("S1", "S3"):
        plan = plugin._twin_plan(sampler, base // T.TWIN_BLOCK)
        assert plan == plugin._twin_plan(sampler, base // T.TWIN_BLOCK)
        for seed in range(base, base + T.TWIN_BLOCK):
            sp = plugin.sample(seed, sampler)
            if plugin.QFORMS[sp.qform].qtype != "noul":
                continue
            n[sp.qform] += 1
            rels = [r for r in plugin.relations(sp) if r.kind == "twin"]
            assert bool(rels) == bool(plan.get(seed))
            if rels:
                tw[(sp.qform, rels[0].expect)] += 1
    for form in n:
        assert tw[(form, 0)] == tw[(form, 1)] or abs(tw[(form, 0)] - tw[(form, 1)]) <= 1, (form, tw)
    share = sum(tw.values()) / sum(n.values())
    assert 0.2 <= share <= 0.45, share
