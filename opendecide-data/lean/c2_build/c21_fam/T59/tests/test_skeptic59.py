"""BUILD-SKEPTIC regression tests for T59 (fresh Sonnet review, 18 Oct): defects found by reading the code and the rendered rows, each pinned
by a test. Everything is built in memory; nothing is written, no model is called."""
import collections
import functools
import re

import pytest

from LK_COMMON import kpipeline
from tool_engine import row_pipeline as rp
import t59_checked as ck
import t59_generator as gen
import t59_levers as lev
import t59_render as rd
import t59_scene as sc
import t59_solver_a as sa
import textcheck59


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
    return [r for r in sample(2000, "t59-skeptic")[0] if r.get("lever_tag", "lever.none") == "lever.none"]


def test_text_only_recomputation_reproduces_the_gold_on_every_row(full):
    """The rendered text alone carries every fact the gold uses, for all eight triggers and both worlds."""
    bad = [r["row_id"] for r in full if textcheck59.recompute(r) != r["gold"]]
    assert not bad, bad[:5]
    assert {r["trigger"] for r in full} == set(sc.TRIGGERS)


def test_no_two_rows_with_opposite_labels_have_the_same_lines(full):
    """A decoy delegation line that named the REAL slot made the two members of a T2 e5 pair identical up to line order."""
    by = collections.defaultdict(set)
    for r in full:
        by[tuple(sorted(r["rendered"]["context"].split("\n")))].add(r["gold"])
    assert not [k for k, v in by.items() if len(v) > 1]


def test_a_delegation_decoy_never_names_the_slot_of_the_real_delegation_line(full):
    n = 0
    for r in full:
        lines = r["lines"]
        decoys = [t for k, t in lines if k == "user_decoy"]
        real = [t for k, t in lines if k == "user_delegation"]
        for d in decoys:
            n += 1
            assert d not in real, r["row_id"]
            if r["trigger"] in ("T2", "T4"):
                assert "choice of" not in d, r["row_id"]
    assert n > 40


def test_every_planned_tool_call_carries_all_the_required_parameters_of_its_tool(full):
    """T5 substitutes used to be `set_<noun>(id)` although `set` needs a `status` (62 of ~200 T5 rows): a PROCEED on an incomplete call."""
    checked = 0
    for r in full:
        if r["world_kind"] != "tool":
            continue
        text = r["rendered"]["text"]
        m = re.search(r"(?:Planned next step|The agent plans this next step): (\w+)\((.*)\)$", text, re.M)
        name, args = m.group(1), m.group(2)
        tm = re.search(r"^- %s\((.*?)\) \[" % re.escape(name), text, re.M)
        if tm is None:                                   # T5: the needed tool is not listed (that is the trigger), nothing to compare
            assert r["trigger"] == "T5", r["row_id"]
            continue
        given = set(re.findall(r"(\w+)=", args))
        required = [p.split(":")[0] for p in tm.group(1).split(", ") if p and "?" not in p and "=" not in p]
        assert set(required) <= given, (r["row_id"], required, given)
        checked += 1
    assert checked > 800


def test_t5_substitutes_are_id_only_verbs():
    for verb in ("delete", "remove", "archive", "cancel"):
        sub = sc.SUBSTITUTES[verb][0]
        assert sub in sc.OPS_ID_ONLY and sub != verb


def test_no_placeholder_field_name_is_rendered(full):
    assert not [r["row_id"] for r in full if re.search(r"\bzz\b", r["rendered"]["text"])]
    assert "zz" not in repr(rd._tool.__defaults__)


def test_generation_survives_many_seeds_without_a_single_exception():
    for sd in range(4):
        seed = "t59-fuzz-%d" % sd
        ctx = gen.Ctx(seed=seed, standin=False)
        for g in gen.build_plan(total=1000, seed=seed):
            gen.generate_group(ctx, g)


def test_held_out_dev_rows_are_derived_from_dev_split_rows_only():
    sb = kpipeline.TestDoubleSolverB(sa.gold_label)
    kept, summ, log, _ = ck.run(600, "dev-split", rp.TestDoubleHook(), solver_b=sb, render_b=kpipeline.test_double_render_b, standin=True)
    by = {r["row_id"]: r for r in kept}
    dev = [r for r in kept if r.get("heldout_family")]
    assert dev
    for r in dev:
        assert r["split"] == "dev" and by[r["twin_of"]]["split"] == "dev", r["row_id"]
    train_lever = [r for r in kept if r.get("lever_tag") == "lever.a12" and not r.get("heldout_family")]
    assert train_lever and all(by[r["twin_of"]]["split"] == "train" for r in train_lever)


def test_a_wrapper_row_must_carry_a_lint_clean_sentence_and_dev_wrappers_are_linted_too():
    from LK_COMMON import klevers
    row = {"a12": None, "wrapper": {"family": "wrap.roleplay", "pos": "wrap_pos.prefix", "sentence": "Please ask me first and confirm."},
           "heldout_family": "wrap.roleplay", "split": "dev"}
    assert "wrapper_lint" in lev.check_lever_row(row)
    row["wrapper"]["sentence"] = klevers.SEED_SENTENCES["wrap.roleplay"][0]
    assert "wrapper_lint" not in lev.check_lever_row(row)
    row["split"] = "train"
    assert "heldout_not_dev_split" in lev.check_lever_row(row)
    sb = kpipeline.TestDoubleSolverB(sa.gold_label)
    kept, _s, _l, _r = ck.run(500, "a10-lint", rp.TestDoubleHook(), solver_b=sb, render_b=kpipeline.test_double_render_b, standin=True, a10=True)
    wr = [r for r in kept if r.get("lever_tag") == "lever.a10"]
    assert wr and all(not klevers.lint_wrapper(r["wrapper"]["sentence"], "T59") for r in wr)


def test_a_text_only_solver_b_runs_through_the_whole_pipeline_on_the_sanitised_view():
    """End to end: B gets {family, sub_block, options, rendered} only (no scene, no gold), derives the label from the text, and the pipeline keeps
    every row (A = B on all rows, A12 rows included) -- the independence is mechanical, not a promise."""
    def b(view):
        assert set(view) == {"family", "sub_block", "options", "rendered"}
        lab = textcheck59.solve(view["rendered"]["text"])
        return kpipeline._BRes(lab, next(o["letter"] for o in view["options"] if o["label"] == lab))

    def render_b(view):
        lab = textcheck59.solve(view["rendered"]["text"])
        return ("letter", next(o["letter"] for o in view["options"] if o["label"] == lab))

    kept, summ, log, _ = ck.run(500, "text-b", rp.TestDoubleHook(), solver_b=b, render_b=render_b, standin=True)
    assert summ["kept"] == len(kept) > 400 and summ["dropped"] == {}, summ["dropped"]
    assert any(r.get("lever_tag") == "lever.a12" for r in kept)
