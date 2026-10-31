"""The WRITTEN F4 files (data/v14_parts/yn2b_raw/gen3_polarity_ladder*.jsonl, yn2b_defs/, yn2b/f4_sources.json):
SPEC counts, every mv_core gate at full size, the builder's parse-back on every row, the (a) base rows and the (b)
source rows (their family's independent decide2), the manifest sha256, and equality with a fresh in-memory build.
Skipped until gen3_polarity_ladder.py has written its output."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
for p in (str(LEAN / "golden_src" / "gen3"), str(LEAN / "yn2b"), str(LEAN)):
    if p not in sys.path:
        sys.path.insert(0, p)
import gen3_polarity_ladder as g  # noqa: E402
import mv_core as mv  # noqa: E402
import pl_frames as pf  # noqa: E402

RAW = LEAN / "data" / "v14_parts" / "yn2b_raw"
SOURCES = LEAN / "yn2b" / "f4_sources.json"
pytestmark = pytest.mark.skipif(not (RAW / f"{g.KEY}.jsonl").exists() or not SOURCES.exists(),
                                reason="F4 not written yet")


@pytest.fixture(scope="module")
def parts():
    return {p: mv.read_raw(g.KEY, p) for p in ("train", "dev")}


@pytest.fixture(scope="module")
def sources():
    return json.loads(SOURCES.read_text())["latents"]


def test_spec_counts(parts, sources):
    tr, trel = parts["train"]
    dev, drel = parts["dev"]
    assert len(tr) == 1500 and len(dev) == 300
    assert Counter(r["meta"]["view"] for r in tr) == {"base": 750, "ladder": 750}
    assert Counter(r["meta"]["polarity"] for r in tr)[0] == 750                        # 50% depth 0
    assert Counter(sources[r["meta"]["latent_id"]]["kind"] for r in tr) == {"a": 750, "b": 750}
    assert Counter(r["meta"]["dev_kind"] for r in dev) == {"iid": 150, "holdout": 150}
    assert all(sources[r["meta"]["latent_id"]]["kind"] == "b" for r in dev)            # R3
    assert len(trel) == 750 and len(drel) == 150
    assert set(sources) == {r["meta"]["latent_id"] for r in tr + dev}


@pytest.mark.parametrize("part", ["train", "dev"])
def test_all_mv_core_gates(parts, part):
    rows, rels = parts[part]
    rep = mv.run_checks(rows, rels)
    failed = {k: v for k, v in rep.items() if isinstance(v, dict) and v.get("ok") is False}
    assert rep["ok"], json.dumps(failed, default=str)[:2000]


@pytest.mark.parametrize("part", ["train", "dev"])
def test_parse_back_every_row(parts, sources, part):
    truth = g.truth_from_rows()
    for r in parts[part][0]:
        assert g.selfcheck_row(r, sources[r["meta"]["latent_id"]], truth), r["rid"]


def test_depth_balanced_against_truth(parts, sources):
    rows = parts["train"][0] + parts["dev"][0]
    for pol in (0, 1, 2):
        xs = [r for r in rows if r["meta"]["polarity"] == pol]
        assert mv.share_ok(sum(sources[r["meta"]["latent_id"]]["truth"] for r in xs), len(xs)), pol
    pol = g.policy_report(parts["train"][0], sources)
    # the ladder mix is 25/25/50 by quota, so both partial policies score about 75% (R2's rebuild: 379 complement /
    # 371 equiv ladders -> 0.7473 / 0.7527; the exact 0.75 of the first build was not a SPEC requirement)
    assert abs(pol["ignore_frame"] - 0.75) <= 0.005 and abs(pol["any_negation_one_flip"] - 0.75) <= 0.005


def test_holdout_dev_uses_only_holdout_frames(parts):
    for r in parts["dev"][0]:
        fam = pf.QUAD[r["meta"]["tpl"].split(".")[0]]["family"]
        assert (fam in pf.HOLDOUT_FAMILIES) == (r["meta"]["dev_kind"] == "holdout")
    for r in parts["train"][0]:
        assert pf.QUAD[r["meta"]["tpl"].split(".")[0]]["family"] in pf.TRAIN_FAMILIES


def test_cue_shares_and_banned_words(parts):
    import check_yn2b as cy
    rows = parts["train"][0] + parts["dev"][0]
    for r in rows:
        assert not cy.BANNED_RE.search(r["instructions"]), r["rid"]
    rep = g.cue_report(parts["train"][0])
    assert rep["pass"], rep


def test_f4a_base_rows(parts, sources):
    """(a): the base row is in golden_train with the same state; its human gold is the label sources records, and
    truth(P) is 'P names that label'; dataset / licence / revision are the base row's (R1)."""
    tr = parts["train"][0]
    want = {r["meta"]["derived_from"] for r in tr if r["meta"].get("derived_from")}
    assert len(want) == 375
    bases = {}
    for line in open(LEAN / "data" / "v14_parts" / "golden_train.jsonl", encoding="utf-8"):
        r = json.loads(line)
        if r["id"] in want:
            bases[r["id"]] = r
    assert len(bases) == 375
    for r in tr:
        b = r["meta"].get("derived_from")
        if not b:
            continue
        base, src = bases[b], sources[r["meta"]["latent_id"]]
        assert base["state"] == r["state"] and base["group_id"] == r["meta"]["derived_group"]
        assert base["gold"] == src["gold_label"] and src["truth"] == (src["label"] == base["gold"])
        assert (base["meta"]["dataset"], base["meta"]["licence"]) == (r["meta"]["dataset"], r["meta"]["licence"])
        assert r["meta"]["revision"] and r["meta"]["derived_by"] == g.DERIVED_BY


def test_f4b_source_rows_agree_with_their_decide2(sources):
    rep = g.source_agreement(sources)
    assert rep["ok"], rep


def test_manifest_and_defs(parts):
    man = [json.loads(x) for x in (LEAN / "golden_src" / "gen3" / "MANIFEST_yn2b.jsonl").read_text().splitlines()
           if x.strip()]
    latest = {}
    for m in man:
        if m.get("key") == g.KEY:
            latest[m["path"]] = m
    paths = [p for part in ("train", "dev") for p in mv.raw_paths(g.KEY, part)] + [SOURCES]
    for p in paths:
        rel = str(p.relative_to(LEAN))
        assert rel in latest and latest[rel]["sha256"] == mv.sha256_file(p), rel
    for rows, _ in parts.values():
        for r in rows:
            assert mv.defs_path(g.KEY, r["meta"]["defs"]).exists()


def test_written_equals_fresh_build(parts, sources):
    fb, b = g.build()
    for part in ("train", "dev"):
        assert parts[part][0] == fb.rows_for(part)
    assert json.loads(json.dumps(b.sources, default=str)) == sources
