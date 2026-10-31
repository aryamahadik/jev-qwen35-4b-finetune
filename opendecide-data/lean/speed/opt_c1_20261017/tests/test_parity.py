import json
from pathlib import Path

import pytest

from oc1 import common as C
from oc1 import parity as PAR

S2 = C.LEAN / "speed" / "speed2_20261013"


def item(i, qtype, opts=None, bucket=None):
    q = {"type": qtype, "instructions": "x"}
    if opts:
        q["options"] = opts
    return {"id": i, "qtype": qtype, "bucket": bucket or ("noul" if qtype == "noul" else "2-4"), "n_options": len(opts or []),
            "request": {"id": i, "state": "s", "questions": {"q0": q}}}


def test_argmax_margin_dp():
    assert PAR.argmax_label(None, {"yes": 0.51}) is True and PAR.argmax_label(None, {"yes": 0.5}) is False
    assert PAR.argmax_label(["a", "b", "c"], {"a": 0.2, "b": 0.5, "c": 0.3}) == "b"
    assert PAR.margin(["a", "b"], {"a": 0.6, "b": 0.4}) == pytest.approx(0.2)
    assert PAR.margin(None, {"yes": 0.55}) == pytest.approx(0.1)
    assert PAR.row_dp(None, {"yes": 0.6, "no": 0.4}, {"yes": 0.5, "no": 0.5}) == pytest.approx(0.1)


def test_compare_counts_flips_missing_and_near_ties():
    items = [item("a", "noul"), item("b", "choice", ["x", "y"]), item("c", "choice", ["x", "y"]), item("d", "noul")]
    ref = {"a": {"yes": 0.9, "no": 0.1}, "b": {"x": 0.51, "y": 0.49}, "c": {"x": 0.9, "y": 0.1}, "d": {"yes": 0.2, "no": 0.8}}
    cand = {"a": {"yes": 0.88, "no": 0.12}, "b": {"x": 0.49, "y": 0.51}, "c": {"x": 0.1, "y": 0.9}}   # b near-tie flip, c real flip, d missing
    r = PAR.compare_items(items, cand, ref)
    assert r["n"] == 4 and r["agree"] == 1 and r["n_flips"] == 3 and r["missing_cand"] == 1
    assert r["flips_near_tie"]["ref_margin<=0.05"] == 1            # b only (c has margin 0.8)
    assert r["dp_max"] == pytest.approx(0.8)
    assert not r["pass_point"]
    assert PAR.verdict(r) == "FAIL"


def test_compare_skips_rows_without_reference():
    items = [item("a", "noul"), item("z", "noul")]
    r = PAR.compare_items(items, {"a": {"yes": 0.9, "no": 0.1}}, {"a": {"yes": 0.8, "no": 0.2}})
    assert r["n"] == 1 and r["argmax_agree"] == 1.0


def test_wilson_and_verdicts():
    lo, hi = PAR.wilson(2495, 2500)
    assert lo < 0.998 < hi
    big = PAR.compare_items([item(str(i), "noul") for i in range(2500)],
                            {str(i): {"yes": 0.9, "no": 0.1} for i in range(2500)},
                            {str(i): {"yes": 0.8, "no": 0.2} for i in range(2500)})
    assert PAR.verdict(big) == "PASS" and big["pass_conservative"]
    assert PAR.verdict(big, acc_diff_pt=0.5) == "FAIL" and PAR.verdict(big, acc_diff_pt=0.5, fp8=True) == "PASS"
    small = PAR.compare_items([item(str(i), "noul") for i in range(50)],
                              {str(i): {"yes": 0.9, "no": 0.1} for i in range(50)},
                              {str(i): {"yes": 0.8, "no": 0.2} for i in range(50)})
    assert PAR.verdict(small) == "PASS_POINT_UNDERPOWERED"


def test_stratified_sample_is_deterministic_and_proportional():
    items = [item(str(i), "noul") for i in range(600)] + [item(f"c{i}", "choice", ["a", "b"], "2-4") for i in range(300)] \
        + [item(f"w{i}", "choice", ["a", "b"], "26+") for i in range(30)]
    a = PAR.stratified_sample(items, 300, seed=0)
    b = PAR.stratified_sample(items, 300, seed=0)
    assert [x["id"] for x in a] == [x["id"] for x in b]
    by = {}
    for x in a:
        by[x["bucket"]] = by.get(x["bucket"], 0) + 1
    assert 150 <= by["noul"] <= 210 and by["26+"] >= 25
    assert len(PAR.stratified_sample(items, 5000)) == len(items)


@pytest.mark.skipif(not (S2 / "S1" / "answers_P.jsonl").exists(), reason="SPEED-2 files absent")
def test_reproduces_speed2_s1_vs_a0_agreement():
    """SPEED-2 REPORT.md: S1 vs A0 on P = 99.77% argmax agreement, max |dp| 0.0452 (gate_dev definitions)."""
    items = C.read_jsonl(C.ROOT / "data" / "P.jsonl")
    s1 = {r["id"]: r["probs"] for r in C.read_jsonl(S2 / "S1" / "answers_P.jsonl")}
    a0 = {r["id"]: r["probs"] for r in C.read_jsonl(S2 / "A0" / "answers_P.jsonl")}
    rep = PAR.compare_items(items, s1, a0)
    assert rep["n"] == 8143
    assert round(100 * rep["argmax_agree"], 2) == 99.77
    assert rep["dp_max"] == pytest.approx(0.0452, abs=5e-4)
    assert rep["n_flips"] == 19 or abs(rep["n_flips"] - 19) <= 1
    # every flip of the real S1 run is a near tie
    assert rep["flip_margin_max"] < 0.05
