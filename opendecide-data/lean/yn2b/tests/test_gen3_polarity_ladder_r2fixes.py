"""R2's fixes to F4 gen3_polarity_ladder (yn2b/r2_polarity_ladder_gate.json): the two reworded frames, the F4(a)
near-miss pair and bundle (mutual nearest pair on the card definitions, one procedure whichever label is quoted,
only labels that occur both as gold and as near miss), the steering of surface shortcut solvers from below, the
truth(P) strata, and the effect of all of it on the written rows. CPU only; nothing is written."""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
for p in (str(LEAN / "golden_src" / "gen3"), str(LEAN / "yn2b"), str(LEAN)):
    if p not in sys.path:
        sys.path.insert(0, p)
sys.dont_write_bytecode = True
import gen3_polarity_ladder as g  # noqa: E402
import mv_core as mv  # noqa: E402
import pl_frames as pf  # noqa: E402
import pl_sources as ps  # noqa: E402
import v3_polarity_ladder as v  # noqa: E402

RAW = LEAN / "data" / "v14_parts" / "yn2b_raw"
SOURCES = LEAN / "yn2b" / "f4_sources.json"
WRITTEN = (RAW / f"{g.KEY}.jsonl").exists() and SOURCES.exists()
needs_rows = pytest.mark.skipif(not WRITTEN, reason="F4 not written")
P_MAY = "the proposed call may run under the policy"


# ------------------------------------------------------------------------------------------------ frames
def test_reworded_frames_have_one_reading():
    for c in pf.CELLS:
        q, y, n = pf.render("gk2", c, P_MAY)
        assert "clear" not in q.lower() and "clear" not in y.lower()
        assert ("let this case proceed" in q) != ("stop this case" in q)
        q, y, n = pf.render("cf1", c, P_MAY)
        assert "flag" not in q and "warranted" not in q and "note" in q
        assert ("well founded" in q) != ("unfounded" in q)


@pytest.mark.parametrize("qid", ["gk2", "cf1"])
def test_reworded_frames_read_as_intended_by_decide2(qid):
    for c in pf.CELLS:
        q, _, _ = pf.render(qid, c, P_MAY)
        fr = v.parse_frame(q)
        assert fr.d == P_MAY and fr.flips == pf.CELL_FLIPS[c], (qid, c, q)


def test_gk2_keeps_the_rule_wording_and_proper_improper():
    assert pf.render("gk2", "00", P_MAY)[0] == (
        f"A rule lets a case proceed exactly when {P_MAY}. Given the material provided, would it be proper to let "
        f"this case proceed?")
    assert pf.render("gk2", "11", P_MAY)[0].endswith("would it be improper to stop this case?")


# ------------------------------------------------------------------------------------------------ F4(a) pair
def _cand(source, gold, options, base="b1"):
    return {"source": source, "gold": gold, "options": list(options), "base_id": base}


@pytest.mark.parametrize("source", sorted(ps.A_SOURCES))
def test_a_pair_is_a_mutual_nearest_pair_on_the_card(source):
    labels = list(ps.A_SOURCES[source]["defs"])
    D = ps.A_SOURCES[source]["defs"]
    for i, gold in enumerate(labels):
        pr = g.a_pair(_cand(source, gold, labels, base=f"{source}-{i}"))
        assert pr is not None
        gl, near, bundle = pr
        assert gl == gold and near != gold and {gold, near} <= set(bundle) and len(bundle) <= 6
        s = g.overlap(D[gold], D[near])
        assert near == max((o for o in labels if o != gold), key=lambda o: (g.overlap(D[o], D[gold]),
                                                                            -labels.index(o)))
        for o in bundle:
            if o not in (gold, near):
                assert g.overlap(D[o], D[gold]) < s and g.overlap(D[o], D[near]) < s, (source, gold, o)


def test_a_pair_is_one_procedure_and_deterministic():
    src = "gd_storm_ef"
    labels = list(ps.A_SOURCES[src]["defs"])
    a = g.a_pair(_cand(src, "EF2", labels, base="x"))
    b = g.a_pair(_cand(src, "EF2", labels, base="x"))
    assert a == b
    assert g.a_pair(_cand(src, "EF2", ["EF2"], base="x")) is None


def test_two_sided_labels():
    pool = [[_cand("gd_infotabs_nli", gl, ["Entailment", "Contradiction", "Neutral"], base=f"b{i}")]
            for i, gl in enumerate(["Entailment", "Contradiction", "Neutral"])]
    two = g.two_sided_labels(pool)["gd_infotabs_nli"]
    golds = {"Entailment", "Contradiction", "Neutral"}
    nears = {g.a_pair(c[0])[1] for c in pool}
    assert two == golds & nears and two < golds


# ------------------------------------------------------------------------------------------------ steering
def _f4():
    fb = mv.FamilyBuilder(g.KEY, generator_file=g.__file__, check_tz=False) if "check_tz" in \
        mv.FamilyBuilder.__init__.__code__.co_varnames else mv.FamilyBuilder(g.KEY, generator_file=g.__file__)
    return g.F4(fb, {}, [], g.Decon(False), Counter())


def test_surface_solvers_are_steered_from_below_and_traps_are_not():
    b = _f4()
    st = b.strata("standard", 0, "kv", 0, "f2", "dd1.00", "f2.may", "base")
    rows = [(st, True, 1000)]
    for name in ("src:world_knowledge", "src:ignore_exceptions"):
        b.sc[("train", name)] = [2, 20]                 # running accuracy 0.10
    miss = {"src:world_knowledge": (0, 2)}
    trap = {"src:ignore_exceptions": (0, 2)}
    base = b.cost("train", rows, {})
    assert b.cost("train", rows, miss) >= base + g.SC_PENALTY + g.SC_LOW_BREACH
    assert b.cost("train", rows, trap) == pytest.approx(base)
    hit = {"src:world_knowledge": (2, 2)}
    assert b.cost("train", rows, hit) == pytest.approx(base)   # a hit pulls it back toward 0.5: no cost


def test_strata_carry_truth_per_renderer_and_per_quoted_label():
    st = dict(g.F4.strata("hard", 0, "prose", 0, "a", "dd1.00", "a.storm_ef", "base", label="EF2", part="train"))
    assert ("rT", "a.storm_ef", 0) in st and ("aL", "a.storm_ef", "EF2", 0) in st
    st_dev = dict(g.F4.strata("hard", 0, "prose", 0, "f2", "dd1.00", "f2.may", "base", part="dev"))
    assert not any(k[0] in ("rT", "aL") for k in st_dev)
    assert g.BAL_PENALTY_PART["dev"] > g.BAL_PENALTY_PART["train"]


# ------------------------------------------------------------------------------------------------ written rows
@pytest.fixture(scope="module")
def written():
    tr, _ = mv.read_raw(g.KEY, "train")
    dv, _ = mv.read_raw(g.KEY, "dev")
    src = json.loads(SOURCES.read_text())["latents"]
    return tr, dv, src


@needs_rows
def test_written_a_rows_quote_balanced_labels(written):
    tr, _, src = written
    by = defaultdict(lambda: [0, 0])
    for r in tr:
        s = src[r["meta"]["latent_id"]]
        if s["kind"] == "a" and r["meta"]["view"] == "base":
            by[(s["source"], s["label"])][0] += s["truth"]
            by[(s["source"], s["label"])][1] += 1
            assert s["label"] in (s["gold_label"], *s["bundle"]) and s["gold_label"] in s["bundle"]
    assert sum(n for _, n in by.values()) == 375
    for k, (t, n) in by.items():
        assert abs(t - (n - t)) <= max(2, 0.1 * n), (k, t, n)        # the label prior is gone
    maj = sum(max(t, n - t) for t, n in by.values()) / 375
    assert maj <= 0.56, maj                                           # was 0.70 in the first build


@needs_rows
def test_written_truth_per_renderer_is_balanced_on_train(written):
    tr, _, src = written
    by = defaultdict(lambda: [0, 0])
    for r in tr:
        if r["meta"]["view"] == "base":
            by[r["meta"]["renderer"]][0] += src[r["meta"]["latent_id"]]["truth"]
            by[r["meta"]["renderer"]][1] += 1
    for k, (t, n) in by.items():
        assert mv.share_ok(t, n) or n < 20, (k, t, n)


@needs_rows
def test_written_surface_solvers_stay_between_40_and_60_percent(written):
    tr, dv, _ = written
    for rows, part in ((tr, "train"), (dv, "dev")):
        acc = defaultdict(lambda: [0, 0])
        for r in rows:
            for k, h in (r["meta"].get("shortcut_hits") or {}).items():
                acc[k][0] += h
                acc[k][1] += 1
        for k in g.SURFACE_SOLVERS:
            h, n = acc.get(k, (0, 0))
            if n >= 40:
                assert 0.40 <= h / n <= 0.60, (part, k, h, n)


@needs_rows
def test_written_rows_use_the_reworded_frames(written):
    tr, dv, _ = written
    seen = Counter()
    for r in tr + dv:
        q = r["meta"]["tpl"].split(".")[0]
        if q in ("gk2", "cf1"):
            seen[q] += 1
            assert "clear this case" not in r["instructions"] and "is that flag" not in r["instructions"]
    assert seen["gk2"] > 0 and seen["cf1"] > 0
