"""Tests for PREREG_FINAL.md amendment A7 (draft: prereg_drafts/AMENDMENT_A7_refparity.md). Copy into tests/ together with
the gate_dev.py change when the owner adopts the amendment:
    cp prereg_drafts/test_amendment_A7.py tests/ && ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_ship_rule.py tests/test_amendment_A7.py
Part 1 (the stored 4B REF is the 30 Sep od_gcp predict read) is required; part 2 (the cfg-base rule for in-process
metas) runs only when gate_dev.py has meta_base (option b of the amendment).
"""
import argparse
import json

import pytest

import gate_dev
from test_ship_rule import REF_OK, ROOT, build, refparity, registered  # noqa: F401  (registered is a fixture)

SPLITS9 = gate_dev.SPLITS.split(",")
PARITY_READ = "q35_4b_pxE_parity"


def test_stored_4b_ref_is_the_predict_read():
    assert gate_dev.STORED_REF["4b"] == PARITY_READ
    assert gate_dev.STORED_REF["2b"] == "q35_2b_v11r"  # the 2B is not changed by amendment A7


@pytest.mark.skipif(not all((ROOT / f"preds_{sp}/{PARITY_READ}.jsonl").exists() for sp in SPLITS9),
                    reason="the 30 Sep parity read is not present")
def test_stored_4b_ref_read_is_clean_and_complete(monkeypatch):
    """The stored REF must itself be a clean od_gcp predict read of 4B-E (pinned revision, chat template, no forced
    override, no TTA, perm_seed None, base Qwen3.5-4B) covering every row of the 9 splits."""
    monkeypatch.setattr(gate_dev, "ROOT", ROOT)  # gate_dev.main(--root tmp) in other tests leaves ROOT pointing there
    issues, sigs = gate_dev.pipeline_check([PARITY_READ], gate_dev.std_reads(SPLITS9, attacks=False))
    assert issues == []
    assert {g["revision"] for g in sigs[PARITY_READ].values()} == {"851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"}
    assert {g["layout"] for g in sigs[PARITY_READ].values()} == {"schema_branch_mark"}
    for sp in SPLITS9:
        ids = {json.loads(l)["id"] for l in open(ROOT / f"data/{sp}.jsonl")}
        got = {json.loads(l)["id"] for l in open(ROOT / f"preds_{sp}/{PARITY_READ}.jsonl")}
        assert ids == got, sp
    a = argparse.Namespace(cand="q35_4b_pxE_fresh", ref=PARITY_READ, size=None, splits=gate_dev.SPLITS)
    assert gate_dev.resolve_size(a) == "4b"  # the frozen tool refused q35_4b_pxE here (metas say Qwen3.5-2B)


@pytest.mark.skipif(not hasattr(gate_dev, "meta_base"), reason="option b (meta_base) not adopted")
def test_in_process_meta_uses_the_trained_cfg_base(tmp_path):
    """An in-process stored read whose top-level base is wrong (4B-E's metas say Qwen3.5-2B) is sized by its training
    cfg's base; a predict meta (no train record) is still checked against its recorded base."""
    build(tmp_path, {"REF": (REF_OK, None), "REF_STORED": (REF_OK, lambda ok: (0.853, 0.853))})
    for m in tmp_path.glob("preds_*/REF_STORED.meta.json"):
        d = json.loads(m.read_text())
        m.write_text(json.dumps({**d, "base": "Qwen/Qwen3.5-2B", "train": {"cfg": {"base": "Qwen/Qwen3.5-4B"}}}))
    res = refparity(tmp_path, log=False)
    assert res["size"] == "4b" and res["pass"]
    assert gate_dev.meta_base({"base": "Qwen/Qwen3.5-2B"}) == "Qwen/Qwen3.5-2B"
    assert gate_dev.meta_base({"base": "x", "train": {"cfg": {"base": "Qwen/Qwen3.5-4B"}}}) == "Qwen/Qwen3.5-4B"
