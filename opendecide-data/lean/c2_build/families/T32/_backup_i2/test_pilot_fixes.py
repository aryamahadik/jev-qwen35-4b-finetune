"""families/T32/test_pilot_fixes.py: tests of the Stage B pilot fixes F1-F8 (pilot/PILOT_VERDICT.json; iteration 1; G0 v3).

In memory only (A37 f: nothing is written; no Haiku, no network).
  F1  wordings    the polarity rule leaves out exactly the six yn_other_than_broken wordings without a negation cue
  F2  twins       yes/no rows carry complements (no twins); choice twins one or two, thinned by status
  F3  status      ch_status gold shares 20% each
  F4  ch_due      the status date equals no option date; the gold's distance rank is spread
  F5  deep        deep specs have no equiv / attack partner; deep share inside the bar
  F6  length      three card styles (CardSpec checks), rules in row.card on yes/no rows, solver B reads both layouts
  F7  packs       the 30 frozen packs: one per card, read by both solvers; skins follow the card's setting
  F8  dneg        the truth-evaluation frame; yn_dneg_broken falls back to yn_broken while no clean wording exists
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T32/test_pilot_fixes.py
"""
from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import cards as CD  # noqa: E402
from c2_kit import pipeline  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from c2_kit.lexicon import question_sem  # noqa: E402
import negcount  # noqa: E402  (c_src/common, on sys.path through c2_kit.paths)
from families.T32 import authoring as A  # noqa: E402
from families.T32 import fixtures as FX  # noqa: E402
from families.T32 import packs_v2 as PV  # noqa: E402
from families.T32 import plugin as P  # noqa: E402
from families.T32 import solver_b as B  # noqa: E402

TRAINING = tuple(s for s in P.T32.SAMPLERS if s not in P.T32.HELD_OUT_SAMPLERS)
SIX_APART_BESIDES = ("1be069a2", "483d6756", "4cff1253", "5c2f71ea", "63161ca2", "99605781")   # PILOT_VERDICT F1


# ------------------------------------------------------------------------------------------------ fixtures
@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T32(lexicon=ctx.lexicon, vocab=PV.standin())


@pytest.fixture(scope="module")
def pools():
    from families.T32 import freeze_v2 as FV
    return FV.load_pools()


@pytest.fixture(scope="module")
def frozen_kit(pools):
    """(plugin on the 30 frozen packs, kit context with the 133 wording skins the pilot loader adds)."""
    import pilot_loaders as PL
    from families.T32 import freeze_v2 as FV
    base = FV.kit_ctx(pools)
    ws = PL.question_wording_skins("T32", P.T32, pools["lexicon"])
    return P.T32(lexicon=pools["lexicon"]), KitCtx(skins={**base.skins, **ws}, lexicon=base.lexicon)


@pytest.fixture(scope="module")
def specs(plugin):
    return [plugin.sample(seed, smp) for seed in range(300) for smp in TRAINING]


# ------------------------------------------------------------------------------------------------ F1 wordings
def test_polarity_rule_leaves_out_the_six_wordings_without_a_negation_cue(pools):
    reg = pools["lexicon"]
    sem = question_sem("T32", "yn_other_than_broken")
    forms = {f.form_id: f.text for f in reg.forms.values() if f.sem_id == sem and reg.status(f.form_id) == "admitted"}
    assert len(forms) == 10
    bad = {fid for fid, t in forms.items() if P.wording_problems("yn_other_than_broken", t)}
    assert {fid.rsplit("#", 1)[1] for fid in bad} == set(SIX_APART_BESIDES)
    for fid in set(forms) - bad:                               # the four kept ones carry one implicit cue
        c = negcount.count(K.PH_RE.sub("X", forms[fid]))
        assert (c.k_all, c.k_syn) == (1, 0), forms[fid]


def test_no_other_admitted_wording_is_left_out_by_the_polarity_rule(pools):
    reg = pools["lexicon"]
    left_out = collections.Counter()
    total = collections.Counter()
    for f in reg.forms.values():
        if f.kind != "question" or reg.status(f.form_id) != "admitted":
            continue
        qf = next(q for q in P.T32.QFORMS if question_sem("T32", q) == f.sem_id)
        total[qf] += 1
        left_out[qf] += bool(P.wording_problems(qf, f.text))
    assert left_out["yn_other_than_broken"] == 6 and left_out["yn_dneg_broken"] == 5
    assert sum(v for q, v in left_out.items() if q not in ("yn_other_than_broken", "yn_dneg_broken")) == 0
    assert all(total[q] - left_out[q] >= 3 for q in P.T32.QFORMS if q != "yn_dneg_broken")      # H40: >= 3 per form


def test_ctx_for_hides_the_left_out_wordings_from_every_pick(frozen_kit):
    plugin, ctx = frozen_kit
    quarantined = plugin.quarantined_wordings(ctx)
    assert len(quarantined) == 11
    spec = plugin.sample(3, "S2")
    narrowed = plugin.ctx_for(spec, ctx)
    assert not set(quarantined) & set(narrowed.skins)
    assert plugin.ctx_for(spec, ctx) is narrowed                      # cached
    for seed in range(60):
        pick = narrowed.pick("T32", "wording", f"k{seed}", qform="yn_other_than_broken")
        assert pick.skin_id.rsplit("#", 1)[1] not in SIX_APART_BESIDES


# ------------------------------------------------------------------------------------------------ F2 twins
def test_yes_no_rows_carry_a_complement_and_rarely_a_twin(plugin):
    """P(yes | status) was .60 broken / .63 kept / .27 for the other three statuses on the pilot's yes/no rows (a reader of
    the chat alone got 65%): every yes/no base with a complement form now has its complement (a pair is balanced per
    status), a yes/no seed pair gets its minimal-edit twins together or not at all (one yes twin, one no twin; about 10% of
    the yes/no bases: a twin moves the status with the gold), and the equiv / attack partners of a pair are drawn together."""
    pairs = both = 0
    for smp in TRAINING:
        for k in range(200):
            a, b = plugin.sample(2 * k, smp), plugin.sample(2 * k + 1, smp)
            if plugin.QFORMS[a.qform].qtype != "noul":
                continue
            ra, rb = plugin.relations(a), plugin.relations(b)
            for spec, rel in ((a, ra), (b, rb)):
                assert ("complement" in [p.kind for p in rel]) == (spec.qform in P.COMPLEMENTS)
            ta = [p.expect for p in ra if p.kind == "twin"]
            tb = [p.expect for p in rb if p.kind == "twin"]
            assert bool(ta) == bool(tb) and (not ta or sorted(ta + tb) == [0, 1])
            both += bool(ta)
            if not (a.deep or b.deep):
                assert {p.kind for p in ra} & {"equiv", "inv"} == {p.kind for p in rb} & {"equiv", "inv"}
            pairs += 1
    assert pairs > 200 and 0.04 <= both / pairs <= 0.20, (both, pairs)


def test_choice_twins_are_one_or_two_and_thin_the_statuses_the_edits_pile_up_on(plugin, specs):
    ch = [s for s in specs if plugin.QFORMS[s.qform].qtype == "choice"]
    n_tw = collections.Counter(sum(p.kind == "twin" for p in plugin.relations(s)) for s in ch)
    assert set(n_tw) <= {0, 1, 2} and n_tw[2] > 0 and n_tw[1] > n_tw[2], n_tw
    assert 0.80 <= (n_tw[1] + 2 * n_tw[2]) / len(ch) <= 1.5, n_tw
    # the pure function: deterministic, at most two, and a status with keep 0 never lands
    pool = [("k", "a", None, "kept", "x"), ("k", "b", None, "broken", "y"), ("j", "c", None, "waived", "z")]
    keep = {st: 1.0 for st in P.STATUSES}
    got = P.pick_choice_twins(("S1", 7), pool, "ch_status", keep, 1.0)
    assert got == P.pick_choice_twins(("S1", 7), pool, "ch_status", keep, 1.0) and len(got) == 2
    keep["broken"] = keep["waived"] = 0.0
    assert [c[3] for c in P.pick_choice_twins(("S1", 7), pool, "ch_status", keep, 1.0)] == ["kept"]


# ------------------------------------------------------------------------------------------------ F3 status shares
def test_status_base_shares_sit_in_the_g0_band_and_the_emitted_golds_are_uniform():
    sh = dict(P.STATUS_SHARES)
    assert set(sh) == set(P.STATUSES) and abs(sum(sh.values()) - 1) < 1e-9
    assert all(0.12 <= v <= 0.30 for v in sh.values()), sh              # G0 section 4: each in 12-30%
    assert set(P.STATUS_TWIN_KEEP) == set(P.STATUSES) and all(0 < w <= 1 for w in P.STATUS_TWIN_KEEP.values())


def test_realised_ch_status_golds_stay_near_uniform(plugin, specs):
    golds = collections.Counter()
    for spec in specs:
        if spec.qform != "ch_status":
            continue
        golds[plugin.solve_a(spec)] += 1
        for prop in plugin.relations(spec):
            if prop.kind == "twin":
                golds[prop.expect] += 1
            elif prop.kind in ("equiv", "inv"):               # the same gold as the base
                golds[plugin.solve_a(spec)] += 1
    n = sum(golds.values())
    assert n > 400
    for st in P.STATUSES:
        assert abs(golds[st] / n - 0.20) <= 0.035, golds       # the unique longest label's share decides G10's longest-option check


# ------------------------------------------------------------------------------------------------ F4 ch_due status date
def _due_specs(plugin, n=1200):
    out = []
    for seed in range(4000):
        for smp in TRAINING:
            spec = plugin.sample(seed, smp)
            if spec.qform == "ch_due":
                out.append(spec)
        if len(out) >= n:
            break
    return out


def test_ch_due_status_date_clears_the_option_dates_and_spreads_the_gold_distance(plugin):
    specs = _due_specs(plugin)
    assert len(specs) >= 1000
    ranks = collections.Counter()
    for spec in specs:
        pl = plugin._plan(spec)
        gold = pl.due_eff
        other = pl.newdue if gold == pl.due0 else pl.due0
        nb = plugin._neighbours(spec)[0].args["DUE"]
        asof = pl.asof
        assert asof not in (gold, other, nb), (spec.seed, spec.sampler)             # was 41.8% of specs
        dg = abs((asof - gold).days)
        others = [abs((asof - o).days) for o in (other, nb)]
        assert dg not in others
        ranks[sum(1 for x in others if x < dg)] += 1
    n = sum(ranks.values())
    # the story fixes where the gold sits among the dates (an end date can be the farthest, the middle one never), so the
    # ranks are not exactly 1/3 each: the gold was the nearest option in 61% of the pilot's specs, now well under half
    assert ranks[0] / n <= 0.48 and ranks[1] / n >= 0.2 and ranks[2] / n >= 0.2, ranks


def test_ch_due_twins_never_move_the_status_date(plugin):
    for spec in _due_specs(plugin, 300):
        for prop in plugin.relations(spec):
            if prop.kind == "twin":
                assert prop.changed_slot != "ASOF"


# ------------------------------------------------------------------------------------------------ F5 deep
def test_deep_specs_get_no_equiv_or_attack_partner(plugin, specs):
    deep = [s for s in specs if s.deep]
    assert deep
    for spec in deep:
        assert not {p.kind for p in plugin.relations(spec)} & {"equiv", "inv"}
    assert sum(s.deep for s in specs) / len(specs) <= 0.09


# ------------------------------------------------------------------------------------------------ F6 cards and length
def test_card_variants_keep_every_rule():
    assert P.CARD_SPEC.problems() == []
    heads = P.CARD_SPEC.heads
    for style in ("compact", "short"):
        assert CD.variant_problems(heads["full"], heads[style]) == []
    assert set(P.CARD_SHARES) == {"full", "compact", "short"} and abs(sum(P.CARD_SHARES.values()) - 1) < 1e-9
    assert P.CARD_SHARES["short"] <= CD.SHORT_CAP


def test_solver_b_copy_of_every_card_style_equals_the_plugins(plugin):
    for style in P.CARD_SHARES:
        for chat in ("chat", "log"):
            for auth in (False, True):
                spec = plugin.sample(0, "S1")
                spec = spec.replace(structure={**spec.structure, "style": chat, "auth": auth},
                                    slots={**spec.slots, "AUTH": __import__("c2_kit.slots", fromlist=["x"]).name_slot("Ana")})
                text = K.fill(plugin.card_template(spec, style), spec.all_slots()).text
                m = B.CARD_RE[style].fullmatch(text)
                assert m and B.STYLE_OF_ADDRESS[m["address"]] == chat and (m["auth"] == "Ana") == auth, (style, text)
                assert not any(B.CARD_RE[o].fullmatch(text) for o in P.CARD_SHARES if o != style)


def test_rules_sit_in_the_card_of_yes_no_rows_and_in_the_instructions_of_choice_rows(plugin, ctx, specs):
    styles, seen = collections.Counter(), collections.Counter()
    for spec in specs[:400]:
        rr = plugin.render(spec, ctx)
        row = rr.row
        rules, question = CD.split_rules(row)
        assert plugin.CLOSED_WORLD_SENTENCE in rules and "\n\n" not in question
        if row["qtype"] == "noul":
            assert row["card"] == rules and row["instructions"] == question and row["meta"]["defs_style"].startswith(
                "rules_in_card_")
        else:
            assert row["card"] is None and row["instructions"] == rules + "\n\n" + question
            assert row["meta"]["defs_style"].startswith("rules_in_instructions_")
        styles[row["meta"]["defs_style"].rsplit("_", 1)[1]] += 1
        seen[row["qtype"]] += 1
        view = plugin.parse(row, ctx)                                  # solver B reads both layouts
        assert plugin.solve_b(view) == plugin.solve_a(spec)
    assert seen["noul"] > 100 and seen["choice"] > 100
    n = sum(styles.values())
    assert set(styles) == {"full", "compact", "short"} and styles["short"] / n <= 0.15 + 0.06, styles


def test_a_unit_prints_one_card_style(plugin, ctx):
    for seed in range(40):
        spec = plugin.sample(seed, "S2")
        res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
        assert res.ok, res.problems
        assert len({r["meta"]["defs_style"].rsplit("_", 1)[1] for r in res.rows}) == 1


def test_solver_b_refuses_rules_in_the_wrong_field(plugin, ctx):
    spec = next(s for s in (plugin.sample(i, "S1") for i in range(60)) if plugin.QFORMS[s.qform].qtype == "noul")
    row = dict(plugin.render(spec, ctx).row)
    moved = dict(row, card=None, instructions=row["card"] + "\n\n" + row["instructions"])
    with pytest.raises(B.ParseError):
        B.parse(moved, ctx)


def test_message_forms_come_from_the_shorter_half(plugin):
    for sem in P.SIG:
        pool = plugin._short_forms(sem)
        ids = plugin._forms_of(sem)
        assert set(pool) <= set(ids) and len(pool) >= min(3, len(ids))
        lens = {f: len(K.PH_RE.sub("", plugin.lexicon.forms[f].text)) for f in ids}
        if len(pool) < len(ids):
            assert max(lens[f] for f in pool) <= min(lens[f] for f in ids if f not in pool)


def test_the_line_budget_is_shorter_than_in_the_pilot():
    assert P.MAX_LINES == {"S1": 6, "S2": 6, "S3": 7, "S4": 7, "S5": 6} and P.N_DECOYS["S3"] == (1, 2)


def test_chat_blocks_respect_the_line_budget(plugin, specs):
    for spec in specs:
        assert len(spec.structure["msgs"]) <= P.MAX_LINES[spec.sampler]


# ------------------------------------------------------------------------------------------------ F7 packs
def test_thirty_frozen_packs_one_per_card():
    v = PV.frozen()
    ids = {v.pack_for(s, c) for s in P.T32.SAMPLERS for c in range(P.CARDS)}
    assert len(ids) == 30 == len(v.packs)
    for (smp, c), pid in v._cards.items():
        assert v.setting_of(pid) == PV.SETTINGS[c]
    for pid, (tasks, events, topics) in v.packs.items():
        assert len(tasks) >= 8 and len(events) >= 5 and len(topics) >= 3
    surfaces = list(v.tasks.values()) + list(v.conds.values()) + list(v.topics.values())
    assert len(set(surfaces)) == len(surfaces)


def test_frozen_packs_reach_the_rows_and_both_solvers_read_them(frozen_kit):
    plugin, ctx = frozen_kit
    seen = set()
    for seed in range(240):
        for smp in P.T32.SAMPLERS[:4]:
            spec = plugin.sample(seed, smp)
            assert spec.pack.startswith("t32:pack|")
            seen.add(spec.pack)
            if seed % 8:
                continue
            rr = plugin.render(spec, ctx)
            view = plugin.parse(rr.row, ctx)
            assert plugin.solve_b(view) == plugin.solve_a(spec)
            tasks = {spec.slots[k].value for k in spec.slots if re.fullmatch(r"TASK\d+", k)}
            assert tasks <= set(plugin.vocab.pack_tasks(spec.pack.split(":", 1)[1]))
    assert len(seen) == 24                                             # 4 training samplers x 6 cards, 24 distinct packs


def test_skins_follow_the_cards_setting(frozen_kit):
    plugin, ctx = frozen_kit
    tags = PV.skin_settings()
    for seed in range(40):
        for smp in P.T32.SAMPLERS[:4]:
            spec = plugin.sample(seed, smp)
            setting = plugin.vocab.setting_of(spec.pack.split(":", 1)[1])
            rr = plugin.render(spec, ctx)
            assert setting in tags[rr.skin_id], (spec.pack, rr.skin_id)


def test_the_union_of_the_vocabularies_has_one_key_per_surface():
    tasks, conds, topics = PV.union_tables()
    for table in (tasks, conds, topics):
        assert len(set(table.values())) == len(table)


# ------------------------------------------------------------------------------------------------ F8 dneg
OLD_DNEG = ("Is it not the case that {WHO} has not broken the promise to {QTASK} at the end of {ASOF}?",
            "At the end of {ASOF}, is it not the case that {WHO} has not broken the commitment made to {QTASK}, as the "
            "rules on the card set out?")
NEW_DNEG = ("Is the following statement true: it is not the case that {WHO} has not broken the promise to {QTASK} at "
            "the end of {ASOF}?",
            "As of the end of {ASOF}, is this claim correct: it is not the case that {WHO} has not broken the "
            "commitment to {QTASK}?")


def test_dneg_frame_is_a_truth_evaluation():
    for t in OLD_DNEG:
        assert any("F8" in p for p in P.wording_problems("yn_dneg_broken", t))
    for t in NEW_DNEG:
        assert P.wording_problems("yn_dneg_broken", t) == []
        c = negcount.count(K.PH_RE.sub("X", t))
        assert (c.k_syn, c.k_all) == (2, 2)
        assert A.check_wording("yn_dneg_broken", t, polarity=True) == []
    assert any("F8" in p for p in A.check_wording("yn_dneg_broken", OLD_DNEG[0], polarity=True))
    assert not any("F8" in p for p in A.check_wording("yn_dneg_broken", OLD_DNEG[0]))      # the v1 pool: no polarity rule


def test_old_dneg_wordings_pass_polarity_but_not_the_frame(pools):
    reg = pools["lexicon"]
    sem = question_sem("T32", "yn_dneg_broken")
    texts = [f.text for f in reg.forms.values() if f.sem_id == sem and reg.status(f.form_id) == "admitted"]
    assert len(texts) == 5
    for t in texts:
        assert POL.form_problems(P.T32, "yn_dneg_broken", t) == []
        assert P.wording_problems("yn_dneg_broken", t)


def test_dneg_falls_back_to_yn_broken_while_no_clean_wording_is_admitted(pools):
    plug = P.T32(lexicon=pools["lexicon"])
    assert plug.dneg_ok is False
    seen = collections.Counter(plug.sample(seed, smp).qform for seed in range(300) for smp in TRAINING)
    assert seen["yn_dneg_broken"] == 0 and seen["yn_broken"] > 0
    ctx = FX.ctx()
    assert P.T32(lexicon=ctx.lexicon, vocab=PV.standin()).dneg_ok is True       # the fixture wording has the frame


def test_the_reauthoring_brief_asks_for_the_truth_evaluation_frame():
    items = A.reauthor_dneg_items()
    assert len(items) == 4 and all("Is the following statement true" in it[1]["brief"] for it in items)
    b = A.reauthor_dneg_batch()
    assert len(b.chunks) == 1 and "is it not the case that" in b.chunks[0]["items"][0]["brief"]
    assert b.chunks[0]["answer_file"].endswith(".json") and "reauthor_dneg" in b.chunks[0]["answer_file"]


# ------------------------------------------------------------------------------------------------ depth plan (G6 d_meta)
def test_depth_is_independent_of_the_status_goal(plugin):
    """The pilot at 1,500-3,000 rows showed depth predicting the status (Kept 1.5, Waived 1.8, Not triggered 0.7, Not yet
    due 0.95 mean depth): the target depth is now drawn from the seed and the story drawn again until it matches."""
    by = collections.defaultdict(list)
    deep = 0
    for seed in range(500):
        for smp in TRAINING:
            spec = plugin.sample(seed, smp)
            if spec.qform == "ch_due":
                continue
            st = plugin._fold(spec)[0]
            by[st].append(spec.depth)
            deep += spec.deep
            assert spec.depth >= 1, (seed, smp)                          # a status needs a decisive line
    means = {k: sum(v) / len(v) for k, v in by.items()}
    assert max(means.values()) - min(means.values()) <= 0.25, means
    assert 0.03 <= deep / sum(len(v) for v in by.values()) <= 0.09, deep
    assert set(by["not_triggered"]) <= {1, 2}                             # a called-off event leaves no third line


# ------------------------------------------------------------------------------------------------ the overlay bands
def test_overlay_shares_on_a_large_sample_without_rendering(plugin):
    """The spec 4.1 / 3.0 bands on ~12,000 rows from the relation proposals alone (the pipeline drops nothing in the pilot
    of 1,000 rows): yes/no 45-55%, yes rate 48-52%, twins 20-25%, equiv 5-10%, complements >= 20% of the yes/no rows,
    yes = bad 45-55% of the yes/no rows, deep <= 10%."""
    rows = []
    for seed in range(900000, 900000 + 700):
        for smp in TRAINING:
            spec = plugin.sample(seed, smp)
            g, q = plugin.solve_a(spec), plugin.QFORMS[spec.qform]
            rows.append((q.qtype, "base", g, spec.deep, spec.qform))
            for prop in plugin.relations(spec):
                if prop.kind == "complement":
                    rows.append(("noul", "complement", 1 - g, spec.deep, prop.qform))
                elif prop.kind in ("equiv", "inv"):
                    rows.append((q.qtype, prop.kind, g, spec.deep, spec.qform))
                elif prop.kind == "twin":
                    rows.append((q.qtype, "twin", prop.expect, plugin.derive(prop.spec).deep, spec.qform))
    n = len(rows)
    yn = [r for r in rows if r[0] == "noul"]
    assert 0.46 <= len(yn) / n <= 0.54, len(yn) / n
    assert abs(sum(r[2] for r in yn) / len(yn) - 0.5) <= 0.006          # pairs, complements and pair-level partners: balanced
    share = collections.Counter(r[1] for r in rows)
    assert 0.205 <= share["twin"] / n <= 0.245 and 0.05 <= share["equiv"] / n <= 0.09, share
    assert share["complement"] / len(yn) >= 0.20
    bad = [r for r in yn if plugin.QFORMS[r[4]].yes_is_bad is not None]
    assert 0.46 <= sum(plugin.QFORMS[r[4]].yes_is_bad for r in bad) / len(bad) <= 0.54
    assert sum(r[3] for r in rows) / n <= 0.09
    ch = [r for r in rows if r[4] == "ch_status"]
    c = collections.Counter(r[2] for r in ch)
    for st in P.STATUSES:                                                 # F3: the emitted golds are 20% each
        assert abs(c[st] / len(ch) - 0.20) <= 0.015, c


# ------------------------------------------------------------------------------------------------ registers (F7)
def test_register_shares_stay_under_15_percent_with_the_setting_filter(frozen_kit):
    plugin, ctx = frozen_kit
    regs = collections.Counter()
    n = 0
    for seed in range(400):
        for smp in P.T32.SAMPLERS[:4]:
            spec = plugin.sample(seed, smp)
            sk = plugin._pick_skin(plugin.ctx_for(spec, ctx), f"T32|{seed}|{smp}|{spec.qform}", False)
            regs[sk.register] += 1
            n += 1
    assert len(regs) == 9 and max(regs.values()) / n <= 0.16, regs
