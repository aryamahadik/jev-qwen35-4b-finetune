"""The F1 files written to data/v14_parts/yn2b_raw (gen3_rule_chain): sha256 equal to the latest MANIFEST_yn2b
records, every mv_core check passes on the full train and dev parts, the builder's parse-back label agrees with every
written gold, every row converts to a golden row, and a fresh build reproduces the files byte for byte."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
import mv_core as mv  # noqa: E402
import gen3_rule_chain as G  # noqa: E402

KEY = G.KEY
RAW = LEAN / "data" / "v14_parts" / "yn2b_raw"
PATHS = {part: mv.raw_paths(KEY, part, RAW) for part in ("train", "dev")}
pytestmark = pytest.mark.skipif(not PATHS["train"][0].exists(), reason="F1 rows not written yet")


def _latest_manifest():
    recs = {}
    for ln in (LEAN / "golden_src" / "gen3" / "MANIFEST_yn2b.jsonl").read_text().splitlines():
        if ln.strip():
            r = json.loads(ln)
            if r.get("key") == KEY:
                recs[r["path"]] = r
    return recs


def test_manifest_sha256_matches():
    recs = _latest_manifest()
    for part, (rp, lp) in PATHS.items():
        for p in (rp, lp):
            rel = str(p.resolve().relative_to(LEAN.resolve()))
            assert rel in recs, rel
            assert recs[rel]["sha256"] == mv.sha256_file(p), rel
    names = LEAN / "yn2b" / f"names_{KEY}.json"
    assert recs["yn2b/" + names.name]["sha256"] == mv.sha256_file(names)


@pytest.mark.parametrize("part", ["train", "dev"])
def test_written_part_passes_every_check(part):
    rows, rels = mv.read_raw(KEY, part, RAW)
    rep = mv.run_checks(rows, rels)
    failed = [k for k, v in rep.items() if isinstance(v, dict) and v.get("ok") is False]
    assert rep["ok"], failed
    assert G.cue_report(rows)["ok"] and G.banned_report(rows)["ok"]


@pytest.mark.parametrize("part", ["train", "dev"])
def test_parse_back_label_agrees_with_every_written_gold(part):
    rows, _ = mv.read_raw(KEY, part, RAW)
    bad = []
    for r in rows:
        defs = mv.load_defs(KEY, r["meta"]["defs"])
        ok, why = G.self_check_row(r, None, defs)
        if not ok:
            bad.append((r["rid"], why))
    assert not bad, bad[:5]


@pytest.mark.parametrize("part", ["train", "dev"])
def test_rows_convert_to_golden_rows(part):
    rows, rels = mv.read_raw(KEY, part, RAW)
    g, gr = mv.assemble(rows, rels, lambda r: mv.load_defs(KEY, r["meta"]["defs"]))
    assert len(g) == len(rows) and len(gr) == len(rels)
    assert all(r["source"] == "gd_" + KEY and "teacher" not in r["meta"] for r in g)


def test_counts_match_the_spec_targets():
    rows, _ = mv.read_raw(KEY, "train", RAW)
    base = [r for r in rows if r["meta"]["view"] != "attack"]
    f1b = [r for r in base if r["meta"]["pack"].startswith("nb_")]
    jb = [r for r in base if r["meta"]["qkind"] == "jb"]
    assert 3800 <= len(base) <= 4200
    assert 540 <= len(f1b) <= 660 and 180 <= len(jb) <= 220
    att = len(rows) - len(base)
    assert 0.07 * len(base) <= att <= 0.09 * len(base)
    dev, _ = mv.read_raw(KEY, "dev", RAW)
    assert 340 <= len(dev) <= 460
    assert {r["meta"]["dev_kind"] for r in dev} == {"iid", "holdout"}


def test_rebuild_is_byte_identical(tmp_path):
    fb, _ = G.build(raw_dir=tmp_path / "raw", defs_dir=tmp_path / "defs", manifest=tmp_path / "M.jsonl")
    fb.write(parts=("train", "dev"))
    for part, (rp, lp) in PATHS.items():
        rp2, lp2 = mv.raw_paths(KEY, part, tmp_path / "raw")
        assert mv.sha256_file(rp2) == mv.sha256_file(rp), part
        assert mv.sha256_file(lp2) == mv.sha256_file(lp), part
