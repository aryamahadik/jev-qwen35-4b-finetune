"""A70 (g) code-edit window, 17 Oct 2026: c2_t37b_dev is a C2 dev set again (g13_c2.C2_DEV, mix_c2.DEV_SETS, c2_select's stale check), and
the installed data/ files are the frozen ones. In memory except the sha checks of the installed files. Run from lean/:
  HF_HUB_OFFLINE=1 ../.venv/bin/python -B -m pytest -q c2_build/tests/test_a70_window.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
import c2io  # noqa: E402
import c2_select  # noqa: E402
import g13_c2 as G  # noqa: E402
import gate_c2  # noqa: E402
import mix_c2 as m  # noqa: E402

DATA = c2io.DATA
T37B_SHA = "f8ced3c502a5bbe0bf4e4010d0a71782611a3ceb114b776400a831456661e3da"       # T37BDEV_FREEZE.json (A70 f)
T37B_REL_SHA = "c74f37034f238c72d0c2ae2bd65d5584fa021bf26474f8ef79d72462d9663f78"
MIXDEV_SHA = "aa570eb373c34982d890deda53e3b86d72da3cc33a662c78c310e9890fe4c3b9"     # staged/mixdev_a71 (T32 out by A71 a)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_the_three_registries_agree_on_the_t37b_dev_file():
    assert m.DEV_SETS["c2_t37b_dev"] == DATA / "c2_t37b_dev.jsonl"
    assert G.C2_DEV["c2_t37b_dev"]["paths"] == ["lean:data/c2_t37b_dev.jsonl"]
    assert G.C2_DEV["c2_t37b_dev"]["fields"] is None and G.C2_DEV["c2_t37b_dev"]["train_fields"] is None
    assert "c2_t37b_dev.jsonl" in c2_select.DEV_BASENAMES and gate_c2.T37B_DEV == "c2_t37b_dev"
    assert G.A53_TARGETS == ("c2_mixdev", "c2_transfer_dev")                      # unchanged: no A53 waiver for T37b-dev


def test_dev_items_hold_t37b_dev_rows_under_their_own_name(tmp_path):
    class Log:
        def jsonl(self, p):
            return [json.loads(x) for x in Path(p).read_text().splitlines() if x.strip()]
    f = tmp_path / "t.jsonl"
    f.write_text(json.dumps({"id": "a", "meta": {"family": "T37b"}, "state": "x"}) + "\n")
    out, miss = m.dev_items(Log(), [], {"c2_t37b_dev": f})
    assert not miss and [r["id"] for r, held in out["c2_t37b_dev"]] == ["a"] and not out["c2_t37b_dev"][0][1]
    _, miss = m.dev_items(Log(), [], {"c2_t37b_dev": tmp_path / "absent.jsonl"})
    assert miss and "c2_t37b_dev" in miss[0]


@pytest.mark.skipif(not (DATA / "c2_t37b_dev.jsonl").exists(), reason="T37b-dev not installed in this tree")
def test_installed_t37b_dev_files_are_the_frozen_ones():
    assert sha(DATA / "c2_t37b_dev.jsonl") == T37B_SHA and sha(DATA / "c2_t37b_dev_relations.jsonl") == T37B_REL_SHA
    rows = [json.loads(x) for x in (DATA / "c2_t37b_dev.jsonl").read_text().splitlines()]
    rels = [json.loads(x) for x in (DATA / "c2_t37b_dev_relations.jsonl").read_text().splitlines()]
    assert len(rows) == 600 and len(rels) == 300 and {x["type"] for x in rels} == {"complement"}
    ids = {r["id"] for r in rows}
    assert all(x["a"] in ids and x["b"] in ids for x in rels)
    assert gate_c2.relations("c2_t37b_dev", c2io.LEAN) == rels                     # the gate reads data/<split>_relations.jsonl


@pytest.mark.skipif(not (DATA / "c2_mixdev.jsonl").exists(), reason="mixdev not installed in this tree")
def test_installed_mixdev_is_the_a71_merge_without_t32():
    assert sha(DATA / "c2_mixdev.jsonl") == MIXDEV_SHA
    fams = {(json.loads(x).get("meta") or {}).get("family") for x in (DATA / "c2_mixdev.jsonl").read_text().splitlines()}
    assert "T32" not in fams and {"T33", "T28", "T01", "F5", "F6", "F11", "F4"} <= fams     # A71: T32 leaves, T33 enters
    staged = C2B / "staged" / "mixdev_a71"
    if staged.exists():
        assert (staged / "c2_mixdev.jsonl").read_bytes() == (DATA / "c2_mixdev.jsonl").read_bytes()
