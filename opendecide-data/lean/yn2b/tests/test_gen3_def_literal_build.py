"""F6 gen3_def_literal: a full in-memory build (about 4 s; nothing is written): SPEC counts, every mv_core gate on train
and dev, the text re-score of every row, splits (held-out packs / terms / phrasing), names, determinism, views, plants,
assembly into golden rows, the devx latent export, and the plant templates against the eval attack spans."""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
sys.path.insert(0, str(LEAN / "yn2b"))
import dl_core as dc  # noqa: E402
import dl_packs as dp  # noqa: E402
import dl_render as dr  # noqa: E402
import gen3_def_literal as g  # noqa: E402
import mv_core as mv  # noqa: E402


@pytest.fixture(scope="module")
def built():
    return g.build_all()


def part(b, p):
    rows = b.fb.rows_for(p)
    rids = {r["rid"] for r in rows}
    return rows, [x for x in b.fb.rels if x["a"] in rids and x["b"] in rids]


def test_spec_counts(built):
    tr, _ = part(built, "train")
    c = Counter(("attack" if r["meta"]["view"] == "attack" else r["meta"]["qkind"]) for r in tr)
    assert c == {"yn": 1100, "choice": 300, "jb": 100, "attack": 150}      # SPEC 3 / F6 (+10% attack twins)
    dev, _ = part(built, "dev")
    assert Counter(r["meta"]["dev_kind"] for r in dev) == {"iid": 75, "holdout": 75}
    assert Counter(r["meta"]["qkind"] for r in dev) == {"yn": 108, "choice": 30, "jb": 12}


@pytest.mark.parametrize("p", ["train", "dev"])
def test_all_mv_core_gates(built, p):
    rows, rels = part(built, p)
    rep = mv.run_checks(rows, rels)
    failed = {k: v for k, v in rep.items() if isinstance(v, dict) and v.get("ok") is False}
    assert rep["ok"], json.dumps(failed, default=str)[:2000]
    assert rep["structure"]["n_errors"] == 0


@pytest.mark.parametrize("p", ["train", "dev"])
def test_text_rescore_every_row(built, p):
    rows, _ = part(built, p)
    res = g.rescore_all(built, rows)
    assert res["ok"] and res["rows"] == len(rows), res


def test_labels_come_from_decide(built):
    for lid, v in built.latents.items():
        f = v["facts"]
        assert not mv.is_undefined(dc.decide(f, "is")[0])
    for r in built.fb.rows[:400]:
        assert r["meta"]["dataset"].endswith("gen3_def_literal.py") and r["meta"]["licence"] == mv.LICENCE


def test_splits_held_out_packs_terms_phrasing(built):
    for r in built.fb.rows:
        lid = r["meta"]["latent_id"]
        gid = built.latents[lid]["facts"]["term"]
        dk = r["meta"]["dev_kind"]
        if dk == "holdout":
            assert dp.held_out_term(gid) and r["meta"]["tpl"].endswith("4")
        else:
            assert not dp.held_out_term(gid) and not r["meta"]["tpl"].endswith("4")
    packs = {s: {r["meta"]["pack"] for r in built.fb.rows if r["meta"]["dev_kind"] == s} for s in (None, "holdout")}
    assert {"tenancy", "safety"} <= packs["holdout"] and not packs[None] & {"tenancy", "safety"}


def test_name_pools_disjoint_by_split(built):
    for lid, v in built.latents.items():
        f = v["facts"]
        for nm in (f["officer"], f["bg_from"], f["name"]):
            for w in nm.split():
                assert mv.name_split(w) == v["split"], (nm, v["split"])


def test_real_word_share_and_tiers(built):
    lat = [v for v in built.latents.values() if v["split"] == "train"]
    real = sum(dp.term_of(v["facts"]["term"])[1].real for v in lat) / len(lat)
    assert abs(real - g.REAL_SHARE) < 0.03                                   # SPEC F6: 30% real words
    tiers = Counter(v["tier"] for v in lat)
    for t, s in mv.TIER_SHARES.items():
        assert abs(tiers[t] / len(lat) - s) <= 0.03


def test_views_and_relations(built):
    tr, rels = part(built, "train")
    vs = g.view_shares(tr)
    assert 0.45 <= vs["yn"]["contrast"] <= 0.7 and vs["yn"]["ladder"] >= 0.25 and vs["yn"]["format"] >= 0.25
    assert vs["yn"]["bg"] > 0.05 and vs["jb"]["contrast"] == 1.0
    by = {r["rid"]: r for r in tr}
    kinds = Counter(x["type"] for x in rels)
    assert kinds["inv"] == 150 and kinds["complement"] > 150 and kinds["equiv"] > 150
    for x in rels:
        a, b = by[x["a"]], by[x["b"]]
        if x["type"] == "inv":
            assert a["gold"] == b["gold"] and b["meta"]["role"] == "attacked" and not b["meta"]["plant_spoof"]
    exclusion_twins = built.stats["contrast:exclusion"]
    assert exclusion_twins > 50


def test_plants_balanced_and_only_in_notes(built):
    tr, rels = part(built, "train")
    at = [r for r in tr if r["meta"]["view"] == "attack"]
    assert Counter(r["meta"]["plant_dir"] for r in at) == {"for_gold": 75, "against_gold": 75}
    for r in at:
        assert r["meta"]["plant_channel"] in mv.PLANT_CHANNELS
        if r["meta"]["fmt"] == "json":
            assert any(x in json.loads(r["state"])["notes"][-1] for x in ("'", "means", "test"))


def test_determinism():
    a, b = g.build_all(), g.build_all()
    h = lambda bb: hashlib.sha256(json.dumps(bb.fb.rows, sort_keys=True).encode()).hexdigest()  # noqa: E731
    assert h(a) == h(b)


def test_assembles_into_golden_rows(built):
    for p in ("train", "dev"):
        rows, rels = part(built, p)
        gr, grel = mv.assemble(rows, rels, lambda r: built.fb.defs.get(r["meta"]["defs"]) if r["meta"]["defs"]
                               else None)
        assert len(gr) == len(rows) and len(grel) == len(rels)
        for r in gr:
            assert "teacher" not in r["meta"] and r["source"] == "gd_gen3_def_literal"
            if r["qtype"] == "noul":
                assert r["card"] and r["card"].split("\n")[0].startswith("- ")      # the definition line first


def test_states_are_short_and_unique(built):
    seen = set()
    for r in built.fb.rows:
        assert len(r["state"]) < 1500
        k = (r["state"], r["instructions"])
        assert k not in seen
        seen.add(k)


def test_devx_export():
    L = g.export_latents("devx", 100)
    assert len(L) == 100 and len({x["latent_id"] for x in L}) == 100
    assert all(dp.held_out_term(x["facts"]["term"]) for x in L)
    assert Counter(x["truth"] for x in L) == {True: 50, False: 50}
    for x in L:
        f = x["facts"]
        assert x["decisions"]["is"] == dc.decide(f, "is")[0] == x["truth"]
        assert x["definition_text"] == dr.definition_text(f)
        for w in f["officer"].split():
            assert mv.name_split(w) == "devx"


def test_plant_templates_share_no_6gram_with_eval_attacks():
    if not (LEAN / "data" / "eval_redef.jsonl").exists():
        pytest.skip("eval sets not present")
    import check_yn2b as cy
    inj = set().union(*[cy.runs(s) for s in cy.injected_spans(LEAN)])
    for t in g.PLANTS.values():
        assert not cy.runs(t) & inj, t
    for ts in dr.Q.values():
        for t in ts:
            assert not cy.runs(t) & inj, t
