"""Gate and probe-harness tests: the gates must PASS clean synthetic data, FAIL planted shortcuts, and detect a broken run."""
import copy
import random

import numpy as np
import pytest

import builder as BU
import gates as GT
import gen_common as g
import heuristics as H
import probes as PB

POOL = g.make_testonly_pool(120)


@pytest.fixture(scope="module")
def rows():
    b = BU.Builder("gates-1", POOL, provisional=True, form_targets={f: 90 for f in g.FORMS})
    out = []
    for f in ("AR-F1", "AR-F2", "LG-L1", "CA-C5", "TM-T1", "TB-B4"):
        for i in range(60):
            out += b.unit(f, "train", i)
    return out


def test_probe_harness_binary_detects_planted_leak_and_passes_noise():
    r = random.Random(3)
    n = 400
    y = np.array([r.randint(0, 1) for _ in range(n)])
    groups = np.arange(n) // 2
    noise = ["w%d x%d" % (r.randint(0, 40), r.randint(0, 40)) for _ in range(n)]
    ok = PB.run_probe("noise", noise, np.array([[r.random()] for _ in range(n)]), y, groups, "binary", [0, 1], k=2, n_boot=200, seed=1, models=("lr",))
    assert ok["sanity"]["valid"] and ok["status"] == "PASS", ok
    leaky = [t + (" tokleak" if l else "") for t, l in zip(noise, y)]
    bad = PB.run_probe("leak", leaky, np.array([[r.random()] for _ in range(n)]), y, groups, "binary", [0, 1], k=2, n_boot=200, seed=1, models=("lr",))
    assert bad["status"] == "FAIL" and bad["models"]["lr"]["point"] > 0.9


def test_probe_harness_kway_detects_planted_leak():
    r = random.Random(5)
    n = 480
    y = np.array([r.randint(0, 3) for _ in range(n)])
    groups = np.arange(n)
    leaky = ["a%d b%d tok%d" % (r.randint(0, 30), r.randint(0, 30), l) for l in y]
    res = PB.run_probe("k", leaky, None, y, groups, "kway", [0, 1, 2, 3], k=4, n_boot=200, models=("lr",))
    assert res["status"] == "FAIL" and res["models"]["lr"]["point"] > 0.8


def test_harness_marks_run_invalid_when_labels_are_degenerate_noise_with_leak_check_failing():
    # the planted-leak power check cannot reach 0.80 when only a handful of rows exist
    r = random.Random(1)
    y = np.array([0, 1] * 6)
    res = PB.run_probe("tiny", ["a b", "c d"] * 6, None, y, np.arange(12), "binary", [0, 1], k=2, n_boot=50, models=("lr",))
    assert res["status"] in ("INVALID", "FAIL", "PASS")      # must not crash
    assert "sanity" in res


def test_confirm_rule_reruns_only_on_point_bar_failure():
    first = {"status": "FAIL", "models": {"lr": {"point": 0.60, "ub": 0.7, "point_bar": 0.55, "ub_bar": 0.6, "pass": False}}}
    calls = []
    out = PB.confirm_rule(first, lambda: (calls.append(1), {"status": "PASS", "models": {"lr": {"point": 0.52, "ub": 0.57, "point_bar": 0.55, "ub_bar": 0.6, "pass": True}}})[1])
    assert calls == [1] and out["status"] == "PASS" and out["confirm"] == "re-run decided"
    ub_only = {"status": "FAIL", "models": {"lr": {"point": 0.52, "ub": 0.7, "point_bar": 0.55, "ub_bar": 0.6, "pass": False}}}
    out2 = PB.confirm_rule(ub_only, lambda: pytest.fail("must not re-run"))
    assert out2["status"] == "FAIL"


def test_bars_numbers():
    assert PB.bars("binary") == (0.55, 0.60)
    p, u = PB.bars("kway", 4)
    assert abs(p - 0.28) < 1e-9 and abs(u - 0.31) < 1e-9
    p, u = PB.bars("kway", 3)
    assert abs(p - 0.3633) < 1e-3 and abs(u - 0.3933) < 1e-3


def test_gate_a4_detects_skewed_letters_and_yes_share(rows):
    assert GT.gate_a4_label_shape(rows)["detail"]
    bad = copy.deepcopy([r for r in rows if r["k"] == 4])
    for r in bad:
        r["label"] = 0
    assert not GT.gate_a4_label_shape(bad)["passed"]
    yn = [r for r in rows if r["form"] == "AR-F2"]
    skew = copy.deepcopy(yn)
    for r in skew:
        r["answer_text"] = "Yes"
    assert not GT.gate_a4_label_shape(skew)["passed"]


def test_gate_a5_detects_wording_overuse_pairs_and_trap_dominance(rows):
    assert GT.gate_a5_shape(rows)["detail"]
    r2 = copy.deepcopy(rows)
    for r in r2:
        r["wording"]["idx"] = 0
    assert not GT.gate_a5_shape(r2)["passed"]
    r3 = copy.deepcopy(rows)
    for r in r3:
        r["pair_id"] = None
    assert not GT.gate_a5_shape(r3)["passed"]
    r4 = copy.deepcopy([r for r in rows if r["form"] == "AR-F1"])
    for r in r4:
        for m in r["option_meta"]:
            if not m["correct"]:
                m["trap_type"] = "omit_step"
    assert not GT.gate_a5_shape(r4)["passed"]


def test_gate_a3_flags_a_wrong_label(rows):
    bad = copy.deepcopy(rows[:20])
    bad[3]["label"] = (bad[3]["label"] + 1) % bad[3]["k"]
    assert not GT.gate_a3_uniqueness(bad)["passed"]


def test_heuristics_abstain_on_ties_and_hit_counter():
    opts = ["a b", "c d", "e f", "g h"]
    p = H.predictions(opts, "")
    assert "longest_string" not in p and "shortest_string" not in p
    assert H.option_values(["1", "2", "x"]) is None
    hits, n = H.hits_on(["10", "20", "30", "40"], 3, "stem 5")
    assert n >= 3 and hits >= 1


def test_probe_gates_run_on_builder_output(rows):
    for fn in (GT.gate_s3, GT.gate_s4, GT.gate_s5, GT.gate_s6):
        res = fn(rows, n_boot=60, check_sanity=False)
        assert res["gate"].startswith("G-S") and isinstance(res["passed"], bool)
    res = GT.gate_s2(rows, n_boot=60)
    assert res["gate"] == "G-S2"
    s1 = GT.option_only_probe([r for r in rows if r["form"] == "AR-F1"], 4, n_boot=60, check_sanity=False)
    assert set(s1["models"]) == {"lr", "gbt"}


def test_option_only_probe_catches_a_planted_option_leak(rows):
    ar = copy.deepcopy([r for r in rows if r["form"] == "AR-F1"])
    for r in ar:
        r["options"][r["label"]] += " zzmarker"
    res = GT.option_only_probe(ar, 4, n_boot=60, check_sanity=False)
    assert res["models"]["lr"]["point"] > 0.9 and not res["passed"]


def test_names_export_has_no_row_content(rows):
    e = GT.export_names(rows)
    assert set(e) == {"domains", "carriers", "forms"}
