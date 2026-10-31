"""The WRITTEN F5 files (data/v14_parts/yn2b_raw/...): SPEC counts, every mv_core gate at full size, the text
re-score of every row, manifest sha256, defs files. Skipped until gen3_lead_score.py --write has run."""
from __future__ import annotations

import json
from collections import Counter

import pytest

from f5_helpers import LEAN, g, mv

RAW = LEAN / "data" / "v14_parts" / "yn2b_raw"
pytestmark = pytest.mark.skipif(not (RAW / f"{g.KEY}.jsonl").exists(), reason="F5 not written yet")


@pytest.fixture(scope="module")
def parts():
    return {p: mv.read_raw(g.KEY, p) for p in ("train", "dev")}


def test_spec_counts(parts):
    tr, _ = parts["train"]
    c = Counter((r["meta"]["qkind"], r["meta"]["view"] == "attack") for r in tr)
    assert c[("score", False)] == 1600 and c[("yn", False)] == 300 and c[("jb", False)] == 100   # SPEC 3 / F5
    assert c[("score", True)] + c[("yn", True)] + c[("jb", True)] == 160                         # 8% attack twins
    yn = Counter(g.kind_of_row(r) for r in tr if r["meta"]["qkind"] == "yn" and r["meta"]["view"] != "attack")
    assert yn == {"ready": 150, "judge": 150}
    dev, _ = parts["dev"]
    assert Counter(r["meta"]["dev_kind"] for r in dev) == {"iid": 100, "holdout": 100}


@pytest.mark.parametrize("part", ["train", "dev"])
def test_all_mv_core_gates(parts, part):
    rows, rels = parts[part]
    rep = mv.run_checks(rows, rels)
    failed = {k: v for k, v in rep.items() if isinstance(v, dict) and v.get("ok") is False}
    assert rep["ok"], json.dumps(failed, default=str)[:2000]


@pytest.mark.parametrize("part", ["train", "dev"])
def test_text_rescore_every_row(parts, part):
    rows, _ = parts[part]
    res = g.self_check_all(rows)
    assert res["ok"], res


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
    qids = {r["meta"]["defs"] for p in parts.values() for r in p[0] if r["meta"]["defs"]}
    for q in qids:
        assert set(mv.load_defs(g.KEY, q)) == {"yes", "no"}
