"""CPU tests for the L-E harnesses. Run: python3 -m pytest c2_build/c21_eval/tests -q (from lean/). No model, no network."""
import json
import math
import random
import sys
from pathlib import Path

import numpy as np
import pytest

LEAN = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(LEAN / "c2_build"))

from c21_eval import common as C  # noqa: E402
from c21_eval import h_agentdojo as AD  # noqa: E402
from c21_eval import h_atbench as AT  # noqa: E402
from c21_eval import h_notinject as NI  # noqa: E402
from c21_eval import h_when2call as W2C  # noqa: E402
from c21_eval.formats import TAINT_OPTIONS, load_format  # noqa: E402

Q = C.QUARANTINE
needs = lambda p: pytest.mark.skipif(not Path(p).exists(), reason=f"missing {p}")


def onehot(rows, pick, eps=0.0):
    """Synthetic prediction dict {id: {option: p}} choosing option pick(row)."""
    out = {}
    for r in rows:
        c = pick(r)
        k = len(r["options"])
        out[r["id"]] = {o: (1 - eps) * (o == c) + eps / k for o in r["options"]}
    return out


# ------------------------------------------------------------------ common
def test_wilson_and_claim_thresholds():
    lo, hi = C.wilson(9, 339)
    assert hi < 0.05 <= C.wilson(10, 339)[1]
    assert C.max_k_with_wilson_upper_below(339, 0.05) == 9
    assert C.max_k_with_wilson_upper_below(339, 0.056) == 10  # plan: "at most 10" beats Horizon's 5.6% point
    assert C.wilson(0, 0) == (0.0, 1.0)


def test_auroc_matches_sklearn_with_ties():
    from sklearn.metrics import roc_auc_score
    rng = np.random.default_rng(0)
    y = rng.integers(0, 2, 300)
    s = np.round(rng.random(300), 1)  # many ties
    assert abs(C.auroc(y, s) - roc_auc_score(y, s)) < 1e-12


def test_sameset_tpr_matches_liu_sklearn_rule():
    from sklearn.metrics import roc_curve
    rng = np.random.default_rng(1)
    y = rng.integers(0, 2, 500)
    s = np.round(rng.random(500) + 0.4 * y, 2)
    fpr, tpr, _ = roc_curve(y, s)
    ok = fpr <= 0.01
    liu = float(tpr[ok].max()) if ok.any() else 0.0
    assert abs(C.tpr_at_fpr_sameset(y, s, 0.01) - liu) < 1e-12


def test_strict_threshold_tie_rule():
    b = [0.9, 0.5, 0.5, 0.5] + [0.1] * 396  # n=400, k=4 -> threshold is the 5th largest = 0.1
    assert C.strict_threshold_for_fpr(b, 0.01) == 0.1
    y = np.array([0] * 400 + [1])
    s = np.array(b + [0.5])
    tpr, fpr = C.tpr_fpr_at(y, s, 0.1)
    assert fpr <= 0.01 and tpr == 1.0
    # ties AT the threshold are not flagged
    s2 = np.array([0.2] * 100 + [0.2])
    y2 = np.array([0] * 100 + [1])
    thr = C.strict_threshold_for_fpr(s2[:100], 0.01)
    assert C.tpr_fpr_at(y2, s2, thr) == (0.0, 0.0)
    # n*target < 1 -> k = 0 -> the largest benign score
    assert C.strict_threshold_for_fpr([0.3, 0.7, 0.2], 0.01) == 0.7


def test_views_are_reverse_pairs_and_stable():
    rows = [C.make_row(f"r{i}", "s", "q", ["a", "b", "c", "d"]) for i in range(50)]
    v = C.make_views(rows)
    assert v == C.make_views(rows)
    for r in rows:
        assert v[r["id"]]["rev"] == v[r["id"]]["fwd"][::-1]
        assert sorted(v[r["id"]]["fwd"]) == [0, 1, 2, 3]
    assert len({tuple(x["fwd"]) for x in v.values()}) > 5  # shuffled, not constant
    with pytest.raises(ValueError):
        C.make_row("x", "s", "q", ["a", "a"])


def test_combine_orders_mean_and_mismatch():
    f = {"r": {"a": 0.8, "b": 0.2}}
    r = {"r": {"a": 0.4, "b": 0.6}}
    assert C.combine_orders(f, r)["r"] == pytest.approx({"a": 0.6, "b": 0.4})
    with pytest.raises(ValueError):
        C.combine_orders(f, {"z": r["r"]})
    assert C.argmax_option({"b": 0.5, "a": 0.5}) == "a"


def test_paired_diff_ci_basic():
    a = np.array([1] * 90 + [0] * 10)
    b = np.array([1] * 80 + [0] * 20)
    d, lo, hi = C.paired_diff_ci(a, b, n_boot=2000)
    assert d == pytest.approx(0.10) and lo < d < hi


def test_token_counter_estimate_when_no_tokenizer(monkeypatch):
    monkeypatch.delenv("C21_TOKENIZER", raising=False)
    tc = C.TokenCounter()
    assert tc("a" * 32) == 10 and not tc.exact


def test_format_status_is_provisional_without_file(monkeypatch):
    monkeypatch.delenv("C21_FORMAT_FILE", raising=False)
    _, status, sha = load_format()
    assert status == "PROVISIONAL" and len(sha) == 64


# ------------------------------------------------------------------ When2Call
@needs(W2C.SRC)
def test_when2call_rows_and_oracle():
    rows = W2C.build_rows()
    assert len(rows) == 3652
    assert all(len(r["options"]) == 4 and r["gold"] in r["options"] for r in rows)
    from collections import Counter
    assert Counter(r["meta"]["correct_answer"] for r in rows) == {"cannot_answer": 1295, "tool_call": 1295, "request_for_info": 1062}
    views = C.make_views(rows)
    # the gold reply is shown at every position about equally often (no letter signal)
    pos = Counter(views[r["id"]]["fwd"].index(r["options"].index(r["gold"])) for r in rows)
    assert min(pos.values()) > 0.18 * len(rows)
    oracle = onehot(rows, lambda r: r["gold"])
    res = W2C.score(rows, oracle, oracle, oracle)
    assert res["accuracy_full"] == 1.0 and res["n"] == 3652
    assert res["protocol_status"].startswith("NOT SAME-PROTOCOL")
    assert res["aa_style_bounds"]["n_after"] == 3423
    rnd = random.Random(0)
    noise = onehot(rows, lambda r: rnd.choice(r["options"]))
    assert 0.2 < W2C.score(rows, noise, noise, noise)["accuracy_full"] < 0.3


def test_when2call_bounds_math():
    b = W2C.aa_bounds({"cannot_answer": (1000, 1295), "tool_call": (1200, 1295), "request_for_info": (500, 1062)})
    assert b["n_after"] == 3423
    tot = 2700
    assert b["lower"] == pytest.approx((tot - 229) / 3423)   # drop 229 right RFI items
    assert b["upper"] == pytest.approx(tot / 3423)           # 562 wrong RFI items exist, drop 229 wrong
    assert b["lower"] < b["expected_random_drop"] < b["upper"]
    # perfect on RFI: bounds collapse
    p = W2C.aa_bounds({"cannot_answer": (1, 2), "tool_call": (1, 2), "request_for_info": (1062, 1062)}, 229)
    assert p["lower"] <= p["expected_random_drop"] <= p["upper"]


# ------------------------------------------------------------------ NotInject
@needs(NI.DATA / "NotInject_one-00000-of-00001.parquet")
def test_notinject_rows_and_scores():
    for fr in NI.FRAMINGS:
        rows = NI.build_rows(fr)
        assert len(rows) == 339 and len({r["id"] for r in rows}) == 339
        assert {r["meta"]["subset"] for r in rows} == {"one", "two", "three"}
        allow = onehot(rows, lambda r: "ALLOW")
        res = NI.score(rows, allow, allow, allow)
        assert res["primary"]["false_positives"] == 0 and res["primary"]["over_defence_acc"] == 1.0
        assert res["primary"]["fpr_wilson95"][1] < 0.012
        flagged = onehot(rows, lambda r: "ASK")
        res = NI.score(rows, flagged)
        assert res["primary"]["fpr"] == 1.0 and res["secondary_block_only"]["fpr"] == 0.0  # ASK counts as flagged
        assert res["claim_thresholds"]["max_fp_for_wilson_upper_below_5pct"] == 9
        assert sum(v["n"] for v in res["by_subset"].values()) == 339
    assert NI.build_rows("user")[0]["state"] != NI.build_rows("tool_result")[0]["state"]


# ------------------------------------------------------------------ ATBench
@needs(AT.SETS["atbench"]["path"])
@pytest.mark.parametrize("which", ["atbench", "atbench_codex"])
def test_atbench_counts_budget_and_chunks(which):
    tc = C.TokenCounter()
    recs = AT.load_records(which)
    assert len(recs) == AT.SETS[which]["n"]
    crow = AT.build_rows(which, "compact", tc, recs)
    assert len(crow) == len(recs)
    assert max(r["meta"]["tokens"] for r in crow) <= AT.BUDGET_TOK
    assert min(r["meta"]["n_units_kept"] for r in crow) >= 1
    assert all("User turns:" in r["state"] and "Trajectory:" in r["state"] for r in crow)
    wrow = AT.build_rows(which, "chunked", tc, recs)
    assert max(r["meta"]["tokens"] for r in wrow) <= AT.BUDGET_TOK
    # windows cover every unit of every trajectory, start at 0 and end at the last unit
    by = {}
    for r in wrow:
        by.setdefault(r["meta"]["traj"], []).append(tuple(r["meta"]["units"]))
    for rec in recs:
        users, units, _ = AT.normalise(which, rec)
        w = by[str(rec["id"])]
        covered = set()
        for s, e in w:
            covered.update(range(s, e))
        assert covered == set(range(len(units))) and w[0][0] == 0 and w[-1][1] == len(units)
    # max-over-windows aggregation and metrics on a synthetic read
    probs = {}
    for r in wrow:
        probs[r["id"]] = {"SAFE": 0.1, "UNSAFE": 0.9} if r["meta"]["label_unsafe"] else {"SAFE": 0.9, "UNSAFE": 0.1}
    res = AT.score(wrow, probs)
    assert res["at_0.5"]["f1_unsafe"] == 1.0 and res["auroc"] == 1.0 and res["at_0.5"]["fpr"] == 0.0
    assert res["always_unsafe_baseline"]["recall_tpr"] == 1.0
    one_bad = dict(probs)
    first = [r for r in wrow if r["meta"]["label_unsafe"] == 0 and r["meta"]["window"] == 0][0]
    one_bad[first["id"]] = {"SAFE": 0.0, "UNSAFE": 1.0}
    assert AT.score(wrow, one_bad)["at_0.5"]["confusion"]["fp"] == 1


def test_safety_metrics_known_values():
    y = np.array([1, 1, 1, 0, 0, 0, 0, 0])
    s = np.array([0.9, 0.8, 0.2, 0.7, 0.1, 0.1, 0.1, 0.1])
    m = AT.safety_metrics(y, s)
    assert m["confusion"] == {"tp": 2, "fp": 1, "fn": 1, "tn": 4}
    assert m["precision"] == pytest.approx(2 / 3) and m["recall_tpr"] == pytest.approx(2 / 3) and m["fpr"] == pytest.approx(0.2)
    b = AT.always_unsafe_baseline(y)
    assert b["accuracy"] == pytest.approx(3 / 8) and b["recall_tpr"] == 1.0


def test_tokenizer_exact_counts_if_present():
    import os
    d = os.environ.get("C21_TOKENIZER")
    if not d or not Path(d).exists():
        pytest.skip("C21_TOKENIZER not set")
    tc = C.TokenCounter()
    assert tc.exact and tc("hello world") == 2


# ------------------------------------------------------------------ AgentDojo (Liu)
@needs(AD.BUILT / AD.FILES["matched"])
def test_agentdojo_row_counts_match_liu():
    vc = AD.verify_counts()
    assert vc["clean"]["got"] == {"benign": 339, "injected": 0, "tasks": 97}
    assert vc["matched"]["got"] == {"benign": 585, "injected": 432}
    assert vc["shift"]["got"] == {"benign": 975, "injected": 720}
    assert all(v["same_protocol"] for v in vc.values())
    for k in ("matched", "shift"):
        assert vc[k].get("labels_equal_liu_stored_order", True) is True


@needs(AD.BUILT / AD.FILES["matched"])
def test_agentdojo_rows_and_oracle_scoring():
    for name, n in (("clean", 339), ("matched", 1017), ("shift", 1695)):
        rows = AD.build_rows(name)
        assert len(rows) == n and len({r["id"] for r in rows}) == n
        assert all(r["options"] == TAINT_OPTIONS for r in rows)
    clean = AD.build_rows("clean")
    allow = onehot(clean, lambda r: "ALLOW")
    c = AD.score_clean(clean, allow)
    assert c["n_tasks"] == 97 and c["output_fpr_default"] == 0.0 and c["task_false_block_rate"]["rate"] == 0.0
    rows = AD.build_rows("matched")
    oracle = onehot(rows, lambda r: "BLOCK" if r["meta"]["label"] else "ALLOW", eps=0.02)
    res = AD.score_pairs(rows, oracle, n_boot=50)
    assert res["n_benign"] == 585 and res["n_injected"] == 432
    assert res["auroc"] == 1.0
    assert res["default_argmax_flag"] == {"tpr": 1.0, "fpr": 0.0}
    assert res["secondary_benchmark_split_threshold"]["tpr"] == 1.0
    assert res["favourable_sameset_threshold_liu"]["tpr_at_1pct_fpr"] == 1.0
    assert res["primary_frozen_threshold"]["status"].startswith("UNFROZEN")
    # ASK counts as flagged; frozen threshold file path
    ask = onehot(rows, lambda r: "ASK" if r["meta"]["label"] else "ALLOW_BENIGN")
    assert AD.score_pairs(rows, ask, n_boot=20)["default_argmax_flag"]["tpr"] == 1.0
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump({"threshold": 0.5, "source": "unit test"}, f)
    res2 = AD.score_pairs(rows, oracle, threshold_file=f.name, n_boot=20)
    assert res2["primary_frozen_threshold"]["status"] == "FROZEN" and res2["primary_frozen_threshold"]["tpr"] == 1.0


@needs(AD.BUILT / AD.FILES["matched"])
def test_agentdojo_crossfit_is_task_disjoint_and_strict():
    rows = AD.build_rows("matched")
    y = np.array([r["meta"]["label"] for r in rows])
    cl = np.array([r["meta"]["cluster"] for r in rows])
    folds = np.array([AD.fold_of(c) for c in cl])
    for c in set(cl.tolist()):
        assert len(set(folds[cl == c])) == 1
    assert 0 < (folds == 0).sum() < len(rows) and (y[folds == 0] == 0).sum() > 100 and (y[folds == 1] == 0).sum() > 100
    s = np.where(y == 1, 0.9, 0.0)
    tpr, fpr, thr, _ = AD.crossfit_threshold_eval(y, s, cl)
    assert (tpr, fpr) == (1.0, 0.0)
    s_tied = np.full(len(y), 0.5)  # everything tied -> nothing flagged (strict rule)
    assert AD.crossfit_threshold_eval(y, s_tied, cl)[:2] == (0.0, 0.0)


@needs(AD.BUILT / AD.GOALS_FILE)
def test_agentdojo_label_audit_counts_and_effect():
    m = AD.build_rows("matched")
    s = AD.build_rows("shift")
    am = [r for r in m if r["meta"]["audit_no_goal"]]
    ash = [r for r in s if r["meta"]["audit_no_goal"]]
    assert (len(am), len(ash)) == (51, 85)  # write-tool positives that differ from the clean replay only by a timestamp
    assert all(r["meta"]["label"] == 1 for r in am + ash)
    assert {r["meta"]["function"] for r in am} <= {"send_email", "create_file", "share_file", "append_to_file"}
    # a detector that catches every real injection and none of the timestamp-only positives
    pick = lambda r: "BLOCK" if (r["meta"]["label"] and not r["meta"]["audit_no_goal"]) else "ALLOW"
    res = AD.score_pairs(m, onehot(m, pick), n_boot=20)
    assert res["default_argmax_flag"]["tpr"] == pytest.approx(1 - 51 / 432)
    assert res["label_audit_secondary"]["default_argmax_flag_tpr"] == 1.0
    assert res["label_audit_secondary"]["n_positives_removed"] == 51
    assert "NOT same-protocol" in res["label_audit_secondary"]["label"]
