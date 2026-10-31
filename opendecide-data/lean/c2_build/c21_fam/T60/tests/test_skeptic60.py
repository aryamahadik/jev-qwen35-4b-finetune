"""BUILD-SKEPTIC regression tests for T60 (fresh Sonnet review, 18 Oct): defects found by reading the code and the rendered rows, each pinned
by a test. Everything is built in memory; nothing is written, no model is called."""
import collections
import functools
import re

import pytest

from LK_COMMON import klevers, kpipeline
from tool_engine import row_pipeline as rp
import t60_checked as ck
import t60_g9 as g9
import t60_generator as gen
import t60_model as M
import t60_render as rd
import t60_rule as rule
import textcheck60


@functools.lru_cache(maxsize=None)
def sample(total, seed):
    ctx = gen.Ctx(seed=seed, standin=False)
    plan = gen.build_plan(total=total, seed=seed)
    recs = []
    for g in plan:
        recs.extend(gen.generate_group(ctx, g))
    return tuple(recs), tuple(plan)


@pytest.fixture(scope="module")
def full():
    return [r for r in sample(2000, "t60-skeptic")[0] if r.get("lever_tag", "lever.none") == "lever.none"]


def test_text_only_recomputation_reproduces_the_gold_on_every_row(full):
    """The rendered text alone carries every fact the gold uses: H1 / H3 rule tables and the H2 ablation by reference grammar."""
    bad = [r["row_id"] for r in full if textcheck60.recompute(r) != r["gold"]]
    assert not bad, bad[:5]
    assert {r["hd"] for r in full} == {"h1", "h2", "h3"}


def test_no_two_rows_with_opposite_labels_have_the_same_lines(full):
    by = collections.defaultdict(set)
    for r in full:
        by[tuple(sorted(r["rendered"]["context"].split("\n")))].add(r["gold"])
    assert not [k for k, v in by.items() if len(v) > 1]


def test_h3_cards_are_label_balanced_so_a_card_id_alone_says_nothing():
    """A swap pair ties the smaller-n_min card to PLAN and the larger to ACT; the plan balances that with the single controls."""
    rows = [r for r in sample(2000, "t60-skeptic")[0] if r["hd"] == "h3" and r.get("lever_tag", "lever.none") == "lever.none"]
    c = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        c[r["card"]][int(r["gold"] == "PLAN")] += 1
    assert len(c) == 4
    for card, (act, plan) in c.items():
        assert abs(plan / float(plan + act) - 0.5) <= 0.03, (card, act, plan)


def test_h3_swap_cards_are_fixed_at_plan_level_and_ordered_by_n_min():
    plan = gen.build_plan(total=2000, seed="t60-swapcards")
    sw = [g for g in plan if g["head"] == "h3" and g["kind"] == "swap_card"]
    assert sw and all(g["card_y"] and M.CARDS[g["card"]]["n_min"] < M.CARDS[g["card_y"]]["n_min"] for g in sw)


def test_repo_mv_and_cp_steps_show_both_operands_and_the_engines_check_the_same_command(full):
    n = 0
    for r in full:
        if r["hd"] != "h3" or r["world_kind"] != "repo":
            continue
        for s in r["scene"]["steps"]:
            if s["verb"] in ("mv", "cp"):
                n += 1
                assert s.get("dest"), r["row_id"]
                assert re.search(r"- %s: %s \S+ \S+ \(changes" % (s["sid"], s["verb"]), r["rendered"]["text"]), r["row_id"]
            else:
                assert not s.get("dest")
    assert n > 50
    rows = [r for r in full if r["hd"] == "h3" and r["world_kind"] == "repo"]
    assert g9.leg_c(rows)["pass"]
    spec_steps = [dict(s, dest=None) for r in rows[:1] for s in r["scene"]["steps"] if s["verb"] in ("mv", "cp")]
    if spec_steps:                                   # a step with a missing operand is refused by the G9 leg (c)
        sc = dict(rows[0]["scene"], steps=spec_steps)
        assert g9.t50_step_problems(sc)


def _visible_markers(r):
    sc = r["scene"]
    q = rule.fact_by_id(sc, sc["quote"])
    txt, val = r["rendered"]["text"], str(q["value"])
    out = set()
    if re.search(r"\(a (striking|remarkable|notable) value\)", txt):
        out.add("mark.t60.emphasis")
    m = re.fullmatch(r"([a-z]+)-(\d+)", val)
    if m:
        out.add("mark.t60.ident")
    if (m and int(m.group(2)) >= 20000) or re.fullmatch(r"\d{5}", val):
        out.add("mark.t60.magnitude")
    if "As a reminder" in txt:
        out.add("mark.t60.repeat")
    return out


def test_quad_marker_tags_equal_what_the_row_shows_and_imp_cells_share_one_marker_set(full):
    quads = collections.defaultdict(list)
    for r in full:
        if r.get("cell"):
            quads[r["group_id"]].append(r)
    assert len(quads) > 80
    for gid, rs in quads.items():
        sets = {}
        for r in rs:
            q = rule.fact_by_id(r["scene"], r["scene"]["quote"])
            tagged = {m for m in q["markers"] if m in M.QUAD_MARKERS}
            assert tagged == _visible_markers(r), (r["row_id"], tagged, _visible_markers(r))
            sets[r["cell"]] = tagged
        assert sets["quad.t60.imp_needed"] == sets["quad.t60.imp_unneeded"] and len(sets["quad.t60.imp_needed"]) == 3
        assert sets["quad.t60.bland_needed"] == sets["quad.t60.bland_unneeded"] == set()
        # the four cells keep the quote's turn number (a `repeat` turn is appended at the end, it never renumbers the transcript)
        assert len({re.search(r"\(turn (\d+),", r["rendered"]["text"]).group(1) for r in rs}) == 1


def test_h2_quotes_cover_every_fact_type_and_no_group_is_lost_to_rejection(full):
    types = collections.Counter(rule.fact_by_id(r["scene"], r["scene"]["quote"])["type"] for r in full if r["hd"] == "h2")
    n = float(sum(types.values()))
    assert set(types) == {"V", "R", "D", "S", "P"} and all(types[t] / n >= 0.04 for t in types), types
    quads = [r for r in full if r.get("cell")]
    qt = collections.Counter(rule.fact_by_id(r["scene"], r["scene"]["quote"])["type"] for r in quads)
    assert qt["V"] / float(len(quads)) >= 0.10 and qt["D"] / float(len(quads)) >= 0.08, qt     # V / D quads are not rejected away any more


def test_ordinal_references_name_the_get_calls_and_every_ordinal_word_exists():
    assert len(rd.M_ORD) >= 9
    ref = dict(level=3, ordinal=7)
    assert rd.ref_text(ref, {}) == "the seventh record fetched by a get call"


def test_generation_survives_many_seeds_without_a_single_exception():
    """A scene with 7+ fetched records used to raise IndexError in the renderer (the pipeline would have logged builder_reject)."""
    for sd in range(4):
        seed = "t60-fuzz-%d" % sd
        ctx = gen.Ctx(seed=seed, standin=False)
        for g in gen.build_plan(total=1000, seed=seed):
            gen.generate_group(ctx, g)


def test_held_out_dev_rows_are_derived_from_dev_split_rows_only():
    sb = kpipeline.TestDoubleSolverB(rule.gold_label)
    kept, summ, log, _ = ck.run(600, "dev-split", rp.TestDoubleHook(), solver_b=sb, render_b=kpipeline.test_double_render_b, standin=True)
    by = {r["row_id"]: r for r in kept}
    dev = [r for r in kept if r.get("heldout_family")]
    assert dev
    for r in dev:
        assert r["split"] == "dev" and by[r["twin_of"]]["split"] == "dev", r["row_id"]
    train_lever = [r for r in kept if r.get("lever_tag") == "lever.a12" and not r.get("heldout_family")]
    assert train_lever and all(by[r["twin_of"]]["split"] == "train" for r in train_lever)


def test_a_wrapper_row_must_carry_a_lint_clean_sentence():
    import t60_levers as lev
    row = {"a12": None, "wrapper": {"family": "wrap.roleplay", "pos": "wrap_pos.prefix", "sentence": "Please plan this and keep the facts."},
           "heldout_family": "wrap.roleplay", "split": "dev"}
    assert "wrapper_lint" in lev.check_lever_row(row)
    row["wrapper"]["sentence"] = klevers.SEED_SENTENCES["wrap.roleplay"][0]
    assert "wrapper_lint" not in lev.check_lever_row(row)
    row["split"] = "train"
    assert "heldout_not_dev_split" in lev.check_lever_row(row)


def test_a_text_only_solver_b_runs_through_the_whole_pipeline_on_the_sanitised_view():
    def b(view):
        assert set(view) == {"family", "sub_block", "options", "rendered"}
        lab = textcheck60.h1(view["rendered"]["text"]) if view["sub_block"] == "h1" else (
            textcheck60.h2(view["rendered"]["text"]) if view["sub_block"] == "h2" else textcheck60.h3(view["rendered"]["text"]))
        return kpipeline._BRes(lab, next(o["letter"] for o in view["options"] if o["label"] == lab))

    def render_b(view):
        r = b(view)
        return ("letter", r.letter)

    kept, summ, log, _ = ck.run(500, "text-b", rp.TestDoubleHook(), solver_b=b, render_b=render_b, standin=True)
    assert summ["kept"] == len(kept) > 400 and summ["dropped"] == {}, summ["dropped"]
    assert any(r.get("lever_tag") == "lever.a12" for r in kept)


def test_text_only_recomputation_also_holds_with_the_expanded_production_pool():
    """The tests' default pool is the seed pool; the pipeline renders with pools/wording_pool_v1.json (54-73 variants per card clause). Every
    clause variant must keep the polarity and numbers of its seed, so the text still decides the label."""
    from tool_engine.wording import WordingPool
    pool = WordingPool.from_json(ck.POOL)
    ctx = gen.Ctx(seed="expanded-pool", standin=False, pool=pool)
    n = 0
    forms = set()
    for g in gen.build_plan(total=1200, seed="expanded-pool"):
        for r in gen.generate_group(ctx, g):
            assert textcheck60.recompute(r) == r["gold"], r["row_id"]
            forms.update(re.findall(r"((?:clause|q|task)\.\w+):\d+", r["wording"]["idx"]))
            n += 1
    assert n > 1000 and {"clause.d_size", "clause.p_r2", "clause.k_recover_on"} <= forms
