"""Reviewer R2 tooling for F3 (yn2b/r2_state_track_review.py): blind compare, shortcut probes, decide2 structure check,
verdict, and (when present) the written gate and blind records against the written rows. CPU only; read only."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

YN2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(YN2B))
sys.dont_write_bytecode = True
import r2_state_track_review as R  # noqa: E402


def _row(rid, gold, options=("yes", "no"), qkind="yn", latent="L1", **meta):
    m = {"qkind": qkind, "judge": False, "latent_id": latent, "view": "base", "dev_kind": None, "pack": "orders",
         "plant_dir": None, "shortcut_hits": {}, "n_events": 3, "edge": "", "fmt": "json", "tpl": "t"}
    m.update(meta)
    return {"rid": rid, "gold": gold, "options": list(options), "state": "s " + rid, "instructions": "q?", "meta": m}


def test_blind_compare_counts_misses_and_stale():
    rows = [_row("a", "yes"), _row("b", "no"), _row("c", "x", options=("x", "y"), qkind="choice",
                                                    dev_kind="holdout")]
    out = R.blind_compare({"a": "yes", "b": "yes", "c": "x", "gone": "yes"}, rows)
    assert (out["n"], out["agree"], out["stale"]) == (3, 2, ["gone"])
    assert out["misses"] == [{"rid": "b", "blind": "yes", "gold": "no", "pack": "orders"}]
    assert out["by_part"] == {"dev_holdout": {"agree": 1, "n": 1}, "train": {"agree": 1, "n": 2}}
    with pytest.raises(ValueError):
        R.blind_compare({"a": "maybe"}, rows)


def test_target_reads_jb_first_option_as_yes():
    assert R.target(_row("a", "yes")) == "yes"
    jb = _row("b", "S is false.", options=("S is true.", "S is false."), qkind="jb")
    assert R.group_of(jb) == "binary" and R.target(jb) == "no"
    ch = _row("c", "y", options=("x", "y", "z"), qkind="choice")
    assert R.group_of(ch) == "choice" and R.target(ch) == "1"


def test_probes_find_a_planted_cue_and_ignore_noise():
    rows = []
    for i in range(80):
        g = "yes" if i % 2 else "no"
        rows.append(_row(f"r{i}", g, latent=f"L{i}", fmt="json" if g == "yes" else "kv", tpl=f"t{i % 3}"))
    cue = R.cat_probe(rows[:40], rows[40:], lambda r: R.cat_features(r)["fmt"])
    noise = R.cat_probe(rows[:40], rows[40:], lambda r: R.cat_features(r)["tpl"])
    assert cue["held_out"] == 1.0 and noise["held_out"] <= 0.6
    a, b = R._halves(rows)
    assert a and b and R._halves(rows) == (a, b) and not {r["rid"] for r in a} & {r["rid"] for r in b}


def test_flags_and_verdict():
    rep = {g: {"categorical": {"fmt": {"train->dev": {"held_out": 0.7}}}, "ngram_state": {"held_out_mean": 0.5},
               "ngram_question_options": {"held_out_mean": 0.5}} for g in ("binary", "choice", "score")}
    rep["binary"]["tfidf"] = {"question train->dev": {"acc": 0.56}}
    rep["solvers"] = {"train": {"last_event_wins": {"acc": 0.4, "n": 10}}}
    rep["plants"] = {"train": {"rows": 10, "obey_plant_acc": 0.5}}
    fl = R.flags(rep)
    assert ("binary", "cat:fmt", "train->dev", 0.7) in fl and ("binary", "tfidf:question train->dev", "", 0.56) in fl
    g = {"decide2": {"train": {"disagree": 0, "undefined": 0, "structure": {"equiv:ok": 3}}},
         "readings": {"_ok": True}, "mv_core_checks": {"train": {"balance": True}, "dev": {"artefacts": False}},
         "shortcuts": {"flags": []}, "blind": {"final": {"rate": 0.98, "open_generator_bugs": 0}},
         "tests": {"failed": 0}}
    assert R.verdict(g) == {"green": True, "reasons": []}
    g["blind"]["final"]["rate"] = 0.9
    assert not R.verdict(g)["green"]


def test_option_heuristics_on_toy_choice_rows():
    rows = [_row("c1", "3 units", options=("1 unit", "3 units", "12 units"), qkind="choice"),
            _row("c2", "nobody", options=("Ana Bel", "nobody", "Cor Dan"), qkind="choice")]
    h = R.choice_heuristics(rows)
    assert h["num_median"]["acc"] == 1.0 and h["num_median"]["coverage"] == 0.5
    assert h["nobody_or_none"]["acc"] == 1.0 and h["first"]["acc"] == 0.0


# ------------------------------------------------------------------------------------------------ written records
@pytest.mark.skipif(not (R.TRAIN_PATH.exists() and R.DEV_PATH.exists()), reason="F3 rows not written")
def test_decide2_structure_check_on_written_rows():
    rows = R.read_jsonl(R.TRAIN_PATH)[:300]
    rels = [x for x in R.read_jsonl(R.REL_PATHS["train"]) if x["a"] in {r["rid"] for r in rows}]
    d = R.decide2_check(rows, rels)
    assert d["rows"] == 300 and d["undefined"] == 0
    assert not any(k.endswith(":bad") for k in d["structure"])


@pytest.mark.skipif(not R.GATE_FILE.exists(), reason="no gate written yet")
def test_written_gate_matches_the_written_rows():
    g = json.loads(R.GATE_FILE.read_text())
    for p, path in (("train", R.TRAIN_PATH), ("dev", R.DEV_PATH)):
        if R.sha256(path) != g["inputs"][p]["sha256"]:
            pytest.skip("written rows differ from the gate inputs (candidate gate, or rows rebuilt since)")
    assert g["verdict"]["green"], g["verdict"]
    for p in ("train", "dev"):
        assert g["decide2"][p]["disagree"] == 0 and g["decide2"][p]["undefined"] == 0


@pytest.mark.skipif(not R.BLIND_FILE.exists(), reason="no blind record written yet")
def test_blind_record_is_consistent():
    b = json.loads(R.BLIND_FILE.read_text())
    for rnd in b["rounds"]:
        n = len(rnd["items"])
        assert n == rnd["result"]["n"] and sum(x["agree"] for x in rnd["items"]) == rnd["result"]["agree"]
        assert all(x["blind"] for x in rnd["items"])
        for x in rnd["items"]:
            if not x["agree"]:
                assert x.get("trace"), x["rid"]   # every miss is traced
    final = b["final"]
    assert final["rate"] >= 0.97 and final["open_generator_bugs"] == 0
    rnd = [r for r in b["rounds"] if r["build"] == "final"][0]
    if R.sha256(R.TRAIN_PATH) == rnd["train_sha256"] and R.sha256(R.DEV_PATH) == rnd["dev_sha256"]:
        rows = R.read_jsonl(R.TRAIN_PATH) + R.read_jsonl(R.DEV_PATH)
        cmp = R.blind_compare({x["rid"]: x["blind"] for x in rnd["items"]}, rows)
        assert cmp["agree"] == rnd["result"]["agree"] and not cmp["stale"]
