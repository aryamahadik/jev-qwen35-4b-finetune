"""Tests for the two fixes of the A80 WIRE skeptic round (counts only; synthetic, in memory, nothing written). Run from lean/c2_build:
  HF_HUB_OFFLINE=1 ../../.venv/bin/python -B -m pytest -q tests/test_a80_skeptic_fixes.py
  S1  a69_faithful.lowers: 'strictly lowers' also means 'reaches exactly 0 from a positive distance'. The mixer's G10 aggregate yes rate has no
      tolerance and is rounded to 4 dp, so a family at EXACTLY 52.00% / 48.00% yes (A49 c yes_rate passes, 1e-9 tolerance) fails G10 by 1.7e-17; the
      EPS guard alone made the one-unit fix 'not strictly lower' and the family unrepairable (left out under A69 f iii).
  S2  c2_select.reselect: an A69 part with an EMPTY trap map ("trap": {}, no unit treated) still runs the swap and the repair (stage2).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import a69_faithful as RF  # noqa: E402
import c2_select as sel  # noqa: E402
from test_c2_select_a69 import FAM, pool, toks  # noqa: E402
from test_repair_a69_faithful_a78 import make, pair_family, run, sane, verdicts  # noqa: E402


# ------------------------------------------------------------------------------------------------ S1
def test_lowers_is_eps_or_exactly_zero():
    assert RF.lowers(0.0, 1.7e-17) is True                  # fail -> pass is a strict lowering however small the excess was
    assert RF.lowers(0.0, 0.0) is False                     # nothing to lower
    assert RF.lowers(1.0 - 1e-13, 1.0) is False             # float noise
    assert RF.lowers(1.0 - 1e-11, 1.0) is True
    assert RF.lowers(2.0, 1.0) is False
    assert RF.lowers(1.7e-17, 1.7e-17) is False             # a still-failing check with the same tiny excess did not improve


def _g10_boundary(yes_of_two_units):
    """50 complement-pair units (100 yes/no rows): 2 'skew' units make 52 yes of 100 = exactly 52.00%."""
    rows, rels, ntok = pair_family(50, skew=lambda i: i in yes_of_two_units)
    return make(rows, rels, ntok)


def test_a_family_at_exactly_52_percent_yes_fails_g10_by_float_noise_and_the_repair_clears_it():
    fm, units = _g10_boundary((10, 30))
    S = frozenset(range(len(units)))
    a = fm.all(S)
    assert a["yes_rate"] == ("pass", 0.0)                   # A49 c: 1e-9 tolerance
    v, d = a["g10_cells"]
    assert v == "fail" and 0.0 < d < 1e-12                  # the mixer's G10 aggregate: no tolerance, 4-dp rounded
    S0, sel_, rec = run(fm)
    assert rec["failing_before"] == ["g10_cells"] and rec["failing_after"] == []
    assert rec["stop_reason_by_check"]["g10_cells"] == "passed" and rec["rows_dropped"] >= 1
    assert all(m["check"] == "g10_cells" and m["distance_after"] == 0.0 for m in rec["moves"])
    sane(fm, S0, sel_, rec)
    assert set(verdicts(fm, frozenset(sel_)).values()) <= {"pass", "n/a"}


def test_a_family_at_exactly_48_percent_yes_is_cleared_the_same_way():
    rows, rels, ntok = pair_family(50)
    for i in (10, 30):                                      # two units with gold (0, 0): 48 yes of 100
        for j in range(2):
            rows[2 * i + j]["gold"] = 0
    fm, units = make(rows, rels, ntok)
    S = frozenset(range(len(units)))
    a = fm.all(S)
    assert a["yes_rate"][0] == "pass" and a["g10_cells"][0] == "fail" and 0.0 < a["g10_cells"][1] < 1e-12
    S0, sel_, rec = run(fm)
    assert rec["failing_after"] == [] and rec["rows_dropped"] >= 1
    sane(fm, S0, sel_, rec)


def test_a_clean_family_is_untouched_by_the_fix():
    rows, rels, ntok = pair_family(60)
    fm, units = make(rows, rels, ntok)
    S0, sel_, rec = run(fm)
    assert rec["moves"] == [] and rec["rows_dropped"] == 0 and rec["failing_before"] == []


# ------------------------------------------------------------------------------------------------ S2
def test_reselect_with_an_empty_trap_map_still_runs_the_swap_and_the_repair(monkeypatch):
    rows, rels, probs, pg = pool(500, seed=5, tag_p=0.6, k=3)
    rec = sel.select_family(FAM, rows, rels, pg, 350, probs=probs, ntok=toks(rows))
    by = {r["id"]: r for r in rows}
    chosen = [by[i] for i in rec["selected_ids"]]
    for r in chosen:
        r["meta"] = dict(r["meta"]) | {"pg_bin": rec["pg_bin"][r["id"]], "difficulty_bin": rec["difficulty_bin"][r["id"]]}
    pgm = {r["id"]: rec["crowd_pg"][r["id"]] for r in chosen}
    part = {"key": rec["parts"][0]["key"], "ids": list(rec["selected_ids"]), "trap": {}, "trap_rank": []}
    calls = []
    real = RF.stage2
    monkeypatch.setattr(RF, "stage2", lambda *a, **k: calls.append(1) or real(*a, **k))
    out = sel.reselect(chosen, [], pgm, [part], int(len(chosen) * 0.7), ntok=toks(chosen))
    assert len(calls) == 1                                  # before the fix: the empty map was falsy and the part took the plain crowd_select path
    assert out["a69"] and out["a69"][0]["version"] == 1 and "moves" in out["a69"][0]["repair"]
    assert out["parts"][0]["trap"] == {} and set(out["bins"]) == set(out["selected_ids"])


def test_reselect_of_a_part_without_the_trap_key_keeps_the_plain_path(monkeypatch):
    rows, rels, probs, pg = pool(300, seed=5, tag_p=0.6, k=3)
    pgm = {r["id"]: pg[r["id"]] for r in rows}
    calls = []
    real = RF.stage2
    monkeypatch.setattr(RF, "stage2", lambda *a, **k: calls.append(1) or real(*a, **k))
    out = sel.reselect(rows, [], pgm, [{"key": "F5|c2carry", "ids": [r["id"] for r in rows]}], 150)
    assert calls == [] and out["a69"] == [] and out["bins"] == {}


# ------------------------------------------------------------------------------------------------ S3: the trained set is tied to the training file
def test_trained_families_manifest_must_be_the_one_of_the_training_file(tmp_path):
    import hashlib
    import json

    import gate_c2 as gc
    train = tmp_path / "data" / "c2_parts" / "c2_train.jsonl"
    train.parent.mkdir(parents=True)
    train.write_text('{"id": "a"}\n')
    good = hashlib.sha256(train.read_bytes()).hexdigest()
    man = tmp_path / "man.json"
    body = {"counts": {"by_block": {"T28": 10, "replay": 5}}, "files": {"c2_train.jsonl": {"sha256": good, "rows": 1}}}
    man.write_text(json.dumps(body))
    assert gc.trained_families(man, tmp_path)["trained"] == ["T28"]
    assert gc.trained_families(man)["trained"] == ["T28"]                       # without a root nothing is tied (the old call)
    body["files"]["c2_train.jsonl"]["sha256"] = "0" * 64                          # another mix's manifest
    man.write_text(json.dumps(body))
    with pytest.raises(gc.Refused, match="not the sha256 of c2_train.jsonl"):
        gc.trained_families(man, tmp_path)
    del body["files"]
    man.write_text(json.dumps(body))
    with pytest.raises(gc.Refused, match="not the sha256"):                       # a manifest that does not name the training file at all
        gc.trained_families(man, tmp_path)
    train.unlink()
    assert gc.trained_families(man, tmp_path)["trained"] == ["T28"]               # no training file under the root (a test root): nothing to tie
