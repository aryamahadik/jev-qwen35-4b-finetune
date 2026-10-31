"""R2 review tool for F5 (yn2b/r2_lead_score_review.py): blind-solve comparison, the shortcut probes (a planted cue must
be found, a balanced set must not raise a flag), and the written gate / blind records against the current rows."""
from __future__ import annotations

import json
import random

import pytest

import r2_lead_score_review as R


def _row(i, gold="yes", qkind="yn", state="x", **meta):
    m = {"latent_id": f"L{i // 2}", "view": "base", "judge": False, "dev_kind": None, "fmt": "kv", "tpl": "t",
         "pack": "p", "tier": "hard", "len_bin": 2, "card_style": "lower", "plant_dir": None, "plant_channel": None,
         "n_shortcut_wrong": 1, "levels": None, "qkind": qkind, "n_events": 3, "shortcut_hits": {}}
    m.update(meta)
    opts = ["yes", "no"] if qkind == "yn" else ["A", "B", "C"]
    return {"rid": f"r{i}", "state": state, "instructions": "Is it?", "options": opts, "gold": gold, "meta": m}


def test_blind_compare_counts_misses_and_stale():
    rows = [_row(0, "yes"), _row(1, "no"), _row(2, "no", dev_kind="holdout")]
    out = R.blind_compare({"r0": "yes", "r1": "yes", "r2": "no", "gone": "no"}, rows)
    assert out["n"] == 3 and out["agree"] == 2 and out["stale"] == ["gone"]
    assert out["misses"] == [{"rid": "r1", "r2": "yes", "gold": "no", "view": "base", "qkind": "yn"}]
    assert out["by_part"] == {"dev_holdout": {"agree": 1, "n": 1}, "train": {"agree": 1, "n": 2}}


def test_planted_cue_is_flagged_and_balanced_set_is_not():
    rng = random.Random(1)
    clean, planted = [], []
    for i in range(400):
        g = "yes" if i % 2 else "no"
        filler = " ".join(rng.choice(["alpha", "beta", "gamma", "delta"]) for _ in range(12))
        clean.append(_row(i, g, state=filler, fmt=rng.choice(["kv", "json"])))
        # the planted cue: the word 'zebra' appears in 90% of yes rows and 10% of no rows
        cue = "zebra " if (g == "yes") == (rng.random() < 0.9) else ""
        planted.append(_row(i, g, state=cue + filler, fmt=rng.choice(["kv", "json"])))
    a = R.ngram_probe(clean, "state")
    b = R.ngram_probe(planted, "state")
    assert a["held_out_mean"] < 0.6 < b["held_out_mean"]
    assert "zebra" in (b["a->b"]["chosen"], b["b->a"]["chosen"])


def test_categorical_probe_scores_out_of_sample():
    tr = [_row(i, "yes" if i % 2 else "no", fmt="kv" if i % 2 else "json") for i in range(100)]
    te = [_row(i, "yes" if i % 2 else "no", fmt="kv" if i % 2 else "json") for i in range(100, 140)]
    out = R.cat_probe(tr, te, lambda r: r["meta"]["fmt"])
    assert out["held_out"] == 1.0 and out["values"] == 2          # a perfectly leaking stratum is caught


def test_target_reads_jb_and_score_rows():
    jb = {"meta": {"qkind": "jb"}, "options": ["Yes-desc", "No-desc"], "gold": "No-desc"}
    sc = {"meta": {"qkind": "score"}, "options": ["L1", "L2", "L3"], "gold": "L3"}
    assert R.target(jb) == 0 and R.target(sc) == 2


@pytest.mark.skipif(not R.GATE_FILE.exists(), reason="gate not written")
def test_gate_file_matches_current_rows():
    gate = json.loads(R.GATE_FILE.read_text())
    assert gate["inputs"]["train"]["sha256"] == R.sha256(R.RAW / f"{R.KEY}.jsonl")
    assert gate["inputs"]["dev"]["sha256"] == R.sha256(R.RAW / "dev" / f"{R.KEY}.jsonl")
    for part in ("train", "dev"):
        d = gate["decide2"][part]
        assert d["agree"] == d["rows"] and d["disagree"] == 0 and d["verify_labels_ok"]
    assert gate["shortcuts"]["flags"] == []


@pytest.mark.skipif(not R.BLIND_FILE.exists(), reason="blind record not written")
def test_blind_record_final_pass_is_on_current_rows():
    blind = json.loads(R.BLIND_FILE.read_text())
    final = blind["passes"][-1]
    assert final["inputs"]["train_sha256"] == R.sha256(R.RAW / f"{R.KEY}.jsonl")
    rows = R.load("train") + R.load("dev")
    res = R.blind_compare({x["rid"]: x["r2"] for x in final["rows"]}, rows)
    assert res["n"] == len(final["rows"]) and not res["stale"]
    assert res["acc"] >= 0.97
