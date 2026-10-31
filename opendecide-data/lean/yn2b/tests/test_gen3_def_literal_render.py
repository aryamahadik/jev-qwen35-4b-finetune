"""F6 gen3_def_literal: renderers, exact parse-back, the text re-score, and the pack data (no hearsay / evidence-rule
vocabulary; true outside facts; templates parse back unambiguously). CPU only; writes nothing."""
from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
import dl_core as dc  # noqa: E402
import dl_packs as dp  # noqa: E402
import dl_render as dr  # noqa: E402
import dl_sample as ds  # noqa: E402
import mv_core as mv  # noqa: E402


def items(n=160, split="train", seed=3):
    rng = random.Random(seed)
    pool = mv.NamePool(split)
    out = []
    while len(out) < n:
        tier = rng.choice(["easy", "standard", "judge", "hard"])
        truth = rng.random() < 0.5
        dk = rng.choice(["path", "deem", "rincl"]) if truth else rng.choice(["elem", "excl", "rexcl"])
        excg = "allow_deny" if dk in ("excl", "rexcl") else rng.choice([None, "near_miss"] +
                                                                        (["deny_allow"] if truth else []))
        miss = rng.choice([None, "irrelevant"] + (["decisive"] if excg is None or not truth else []))
        ctx = {"gid": rng.choice(dp.terms_for(split)), "tier": tier, "dk": dk, "truth": truth, "excg": excg,
               "miss": miss, "r_place": "card" if dk in ("rincl", "rexcl") else rng.choice(["none", "facts"])}
        try:
            f = ds.sample(rng, ctx, pool)
        except ds.SampleFail:
            continue
        if rng.random() < 0.3:
            f["record"] = rng.random() < 0.5
        out.append(f)
    return out


@pytest.fixture(scope="module")
def sample_items():
    return items()


@pytest.mark.parametrize("fmt", dr.FMTS)
def test_state_parses_back_exactly(sample_items, fmt):
    for f in sample_items:
        pack = dp.PACKS[f["pack"]]
        for jb in (False, True):
            st = dr.render(f, fmt, jb=jb)
            if fmt == "json":
                assert mv.is_canonical_json(st)
            p = dr.parse_state(pack, fmt, st)
            assert p["values"] == {a: f["values"].get(a) for a in f["order"]}
            if jb:
                assert p["definition"] == dr.definition_text(f)
            if f["record"] is not None:
                assert p["record"] == dr.record_text(f)
            assert p["background"] == dr.background(f)


def test_definition_parses_back_and_rederives_the_outcome(sample_items):
    for f in sample_items:
        pack = dp.PACKS[f["pack"]]
        d = dr.parse_definition(pack, dr.definition_text(f))
        els, exs, deem = dr.definition_parts(f)
        assert d["elements"] == els and d["exclusions"] == exs and d["deem"] == deem
        assert d["joiner"] == f["joiner"]
        assert dr.apply_definition(d, f["values"])["truth"] == dc.evaluate(f)["truth"]


def test_every_attribute_template_parses_unambiguously():
    rng = random.Random(5)
    for pack in dp.PACKS.values():
        for a in pack.attrs:
            for _ in range(20):
                c = ds.make_cond(rng, a)
                assert dr.parse_vp(pack, dr.cond_vp(pack, c)) == c
                v = ds.free_value(rng, a)
                s = dr.fact_sentence(pack, a.id, v)
                assert dr._sentence_value(pack, s) == (a.id, v)
            assert dr._sentence_value(pack, dr.fact_sentence(pack, a.id, None)) == (a.id, None)
            assert ":" not in a.label and "." not in a.label


def test_choice_options_are_valid_option_lines(sample_items):
    for f in sample_items:
        if f["joiner"] != "all" or f.get("deem") or (f.get("r_card") and f["outside"]["effect"] == "incl"):
            continue
        opts = dr.choice_options(f)
        o = list(opts.values())
        mv.check_options(o, "choice")
        mv.choice_card(dr.choice_defs(f, opts), o)
        assert o[-1] == dr.NONE_OPT


def test_questions_and_cards():
    f = items(4)[0]
    for q in ("is", "not", "judge", "judge_n", "choice", "jb"):
        for k in range(5):
            t = dr.question(f, q, k)
            assert t.endswith("?") and "\n" not in t
    for q in ("judge", "judge_n"):
        assert not mv.judge_violations(*dr.yn_defs(f, q).values(), *(dr.question(f, q, k) for k in range(5)))
    for q in ("is", "not", "judge", "judge_n"):
        d = dr.yn_defs(f, q)
        card = mv.yn_card(d, "lower")
        assert mv.card_defs(card) == d
    assert set(dr.tpl_ids("dev_holdout")) == {dr.HOLDOUT_TPL} and dr.HOLDOUT_TPL not in dr.tpl_ids("train")


def test_no_hearsay_or_evidence_rule_vocabulary():
    texts = dp.all_texts() + [t for ts in dr.Q.values() for t in ts]
    bad = [t for t in texts if dp.BANNED_TOPIC_RE.search(t)]
    assert not bad
    import gen3_def_literal as g
    assert not [t for t in g.PLANTS.values() if dp.BANNED_TOPIC_RE.search(t)]


def test_held_out_packs_and_terms():
    assert set(dp.HELD_OUT_PACKS) == {"tenancy", "safety"} and len(dp.HELD_OUT_TERMS) == 3
    for gid in dp.HELD_OUT_TERMS:
        assert not dp.term_of(gid)[1].real                   # SPEC F6: 3 invented terms held out
        assert gid.split(":")[0] not in dp.HELD_OUT_PACKS
    tr, ho = set(dp.terms_for("train")), set(dp.terms_for("dev_holdout"))
    assert not tr & ho and tr | ho == set(dp.TERM_IDS) and set(dp.terms_for("dev_iid")) == tr
    assert set(dp.terms_for("devx")) == ho
    assert len(dp.PACKS) == 10 and "customs" in dp.PACKS


def test_goods_terms_have_both_verdicts_somewhere():
    for gid in dp.TERM_IDS:
        pack, term = dp.term_of(gid)
        if term.items:
            vs = {v for _, us in term.items for _, v in us}
            assert vs == {True, False}, gid


def test_units_round_trip():
    for unit in list(dp.UNITS) + ["noun:league match|league matches", "noun:person|people"]:
        for v in (0, 1, 2, 17, 1500, 2000000):
            assert dp.parse_unit(unit, dp.fmt_unit(unit, v)) == v
    assert dp.fmt_unit("noun:person|people", 1) == "1 person" and dp.fmt_unit("noun:person|people", 3) == "3 people"
    for d in (1, 59, 60, 365):
        assert dp.day_index(dp.parse_date(dp.fmt_date(dp.day(d)))) == d


def test_no_marker_or_control_tokens_in_templates():
    import gen3_def_literal as g
    for t in dp.all_texts() + list(g.PLANTS.values()) + [t for ts in dr.Q.values() for t in ts]:
        assert not re.search(r"<<<|<\||\|>|<think>", t)
