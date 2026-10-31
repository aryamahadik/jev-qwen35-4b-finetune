"""The WRITTEN F6 files (data/v14_parts/yn2b_raw/gen3_def_literal*.jsonl, yn2b_defs/): SPEC counts, every mv_core gate
at full size, the text re-score of every row with its definitions loaded from yn2b_defs, the manifest sha256, and
equality with a fresh in-memory build. Skipped until gen3_def_literal.py has written its output."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
import dl_render as dr  # noqa: E402
import gen3_def_literal as g  # noqa: E402
import mv_core as mv  # noqa: E402

RAW = LEAN / "data" / "v14_parts" / "yn2b_raw"
pytestmark = pytest.mark.skipif(not (RAW / f"{g.KEY}.jsonl").exists(), reason="F6 not written yet")


@pytest.fixture(scope="module")
def parts():
    return {p: mv.read_raw(g.KEY, p) for p in ("train", "dev")}


def test_spec_counts(parts):
    tr, _ = parts["train"]
    c = Counter(("attack" if r["meta"]["view"] == "attack" else r["meta"]["qkind"]) for r in tr)
    assert c == {"yn": 1100, "choice": 300, "jb": 100, "attack": 150}
    dev, _ = parts["dev"]
    assert Counter(r["meta"]["dev_kind"] for r in dev) == {"iid": 75, "holdout": 75}


@pytest.mark.parametrize("part", ["train", "dev"])
def test_all_mv_core_gates(parts, part):
    rows, rels = parts[part]
    rep = mv.run_checks(rows, rels)
    failed = {k: v for k, v in rep.items() if isinstance(v, dict) and v.get("ok") is False}
    assert rep["ok"], json.dumps(failed, default=str)[:2000]


@pytest.mark.parametrize("part", ["train", "dev"])
def test_text_rescore_every_written_row(parts, part):
    rows, _ = parts[part]
    for r in rows:
        defs = mv.load_defs(g.KEY, r["meta"]["defs"])
        assert dr.rescore_row(r, r["meta"]["pack"], defs) == r["gold"], r["rid"]


def test_manifest_and_defs(parts):
    man = [json.loads(x) for x in (LEAN / "golden_src" / "gen3" / "MANIFEST_yn2b.jsonl").read_text().splitlines()
           if x.strip()]
    latest = {}
    for m in man:
        if m.get("key") == g.KEY:
            latest[m["path"]] = m
    for part in ("train", "dev"):
        for p in mv.raw_paths(g.KEY, part):
            rel = str(p.relative_to(LEAN))
            assert rel in latest and latest[rel]["sha256"] == mv.sha256_file(p), rel
    for p in parts.values():
        for r in p[0]:
            if r["meta"]["defs"]:
                assert mv.defs_path(g.KEY, r["meta"]["defs"]).exists()


def test_written_equals_fresh_build(parts):
    b = g.build_all()
    for part in ("train", "dev"):
        assert parts[part][0] == b.fb.rows_for(part)
