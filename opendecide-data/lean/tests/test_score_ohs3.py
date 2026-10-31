"""CPU tests for score_ohs3.py (PREREG_OHS3.md scoring) on synthetic data only. No OHS file is opened.

Run:  ../.venv/bin/python -m pytest -q tests/test_score_ohs3.py
"""
from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import score_ohs3 as S  # noqa: E402

YN = {"qtype": "noul", "options": None}
C3 = ["a", "b", "c"]
C30 = [f"o{k}" for k in range(30)]


# ---------------------------------------------------------------------------------------------- synthetic split
def _row(i, task, group, qtype, gold, options=None, track="F", half="A", variant_of=None):
    meta = {"task": task, "half": half}
    if variant_of:
        meta["variant_of"] = variant_of
    return {"id": i, "group_id": group, "call_id": "c_" + i, "split": "syn", "track": track, "source": task,
            "state": "synthetic", "qtype": qtype, "instructions": "q", "options": options, "gold": gold,
            "role": "choice" if qtype == "choice" else "aff", "card": None, "meta": meta}


def synthetic_split():
    """3 tasks, 15 groups, 16 base rows (one near-duplicate group with 2 rows), 4 _neg and 3 _perm twins."""
    rows, rels = [], []
    # c1: choice, 3 options, track F; group g_c1_0 holds two base rows (a merged near-duplicate cluster)
    for k, (i, g) in enumerate([("c1_0", "g_c1_0"), ("c1_0b", "g_c1_0"), ("c1_1", "g_c1_1"), ("c1_2", "g_c1_2"),
                                ("c1_3", "g_c1_3"), ("c1_4", "g_c1_4")]):
        rows.append(_row(i, "c1", g, "choice", "a", C3, "F", "A" if k % 2 == 0 else "S"))
    # c2: choice, 30 options (> 26), track U
    for k in range(4):
        rows.append(_row(f"c2_{k}", "c2", f"g_c2_{k}", "choice", "o0", C30, "U", "A" if k % 2 == 0 else "S"))
    # y1: yes/no, track U, gold 1,0,1,0,1,0
    for k in range(6):
        rows.append(_row(f"y1_{k}", "y1", f"g_y1_{k}", "noul", 1 - k % 2, None, "U", "A" if k % 2 == 0 else "S"))
    base = {r["id"]: r for r in rows}
    for k in range(4):  # _neg twins (complement, gold flipped, same group and half)
        b = base[f"y1_{k}"]
        t = _row(f"y1_{k}_neg", "y1", b["group_id"], "noul", 1 - b["gold"], None, "U", b["meta"]["half"], b["id"])
        rows.append(t)
        rels.append({"type": "complement", "a": b["id"], "b": t["id"]})
    for k in (1, 2, 3):  # _perm twins (options reversed, same gold)
        b = base[f"c1_{k}"]
        t = _row(f"c1_{k}_perm", "c1", b["group_id"], "choice", "a", C3[::-1], "F", b["meta"]["half"], b["id"])
        rows.append(t)
        rels.append({"type": "equiv", "a": b["id"], "b": t["id"]})
    return rows, rels


def yn(p):
    return {"yes": p, "no": 1 - p}


OD = {  # expected: c1 3/6, c2 3/4, y1 3/6 correct
    "c1_0": {"a": .6, "b": .3, "c": .1}, "c1_0b": {"a": .2, "b": .6, "c": .2}, "c1_1": {"a": .5, "b": .3, "c": .2},
    "c1_2": {"a": .4, "b": .4, "c": .2},  # tie -> wrong
    "c1_3": {"a": .7, "b": .2, "c": .1},  # c1_4 missing -> wrong
    "c2_0": {**{o: .1 / 29 for o in C30[1:]}, "o0": .9}, "c2_1": {**{o: .1 / 29 for o in C30}, "o1": .9},
    "c2_2": {**{o: .5 / 29 for o in C30[1:]}, "o0": .5}, "c2_3": {**{o: .7 / 29 for o in C30[1:]}, "o0": .3},
    "y1_0": yn(.9), "y1_1": yn(.2), "y1_2": yn(.5), "y1_3": yn(.6), "y1_5": yn(.4),  # y1_4 missing
    "y1_0_neg": yn(.2), "y1_1_neg": yn(.7), "y1_2_neg": yn(.3),  # y1_3_neg missing
    "c1_1_perm": {"c": .2, "b": .3, "a": .5}, "c1_2_perm": {"c": .2, "b": .3, "a": .5},
    "c1_3_perm": {"c": .6, "b": .1, "a": .3},
}


def jev_run(missing=(), overrides=None):
    """A strong synthetic Jev: right everywhere except c2_1; twins perfectly consistent."""
    P = {}
    for i in ["c1_0", "c1_0b", "c1_1", "c1_2", "c1_3", "c1_4"]:
        P[i] = {"a": .8, "b": .15, "c": .05, "_raw_sum": 1.0}
    for i in ["c1_1_perm", "c1_2_perm", "c1_3_perm"]:
        P[i] = {"c": .05, "b": .15, "a": .8, "_raw_sum": 1.0}
    for k in range(4):
        P[f"c2_{k}"] = {**{o: .2 / 29 for o in C30[1:]}, "o0": .8}
    P["c2_1"] = {**{o: .2 / 29 for o in C30 if o != "o2"}, "o2": .8}
    for k in range(6):
        P[f"y1_{k}"] = yn(.9 if k % 2 == 0 else .1)
    for k in range(4):
        P[f"y1_{k}_neg"] = yn(.1 if k % 2 == 0 else .9)
    P.update(overrides or {})
    for i in missing:
        P.pop(i)
    return P


def write_split(root: Path, split="syn", rows=None, rels=None, preds=None):
    rows, rels = (rows, rels) if rows is not None else synthetic_split()
    (root / "data").mkdir(parents=True, exist_ok=True)
    (root / f"preds_{split}").mkdir(exist_ok=True)
    (root / f"data/{split}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (root / f"data/{split}_relations.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    preds = preds or {"od": OD, "od_bc": {**OD, "c2_1": OD["c2_0"]},
                      "jevA": jev_run(), "jevB": jev_run(missing=["c1_4"], overrides={"y1_5": yn(.5)})}
    for name, P in preds.items():
        with open(root / f"preds_{split}/{name}.jsonl", "w") as f:
            for i, pr in P.items():
                f.write(json.dumps({"id": i, "model": name, "probs": pr, "jev_model": S.PINNED_JEV}) + "\n")
    return rows, rels


# ---------------------------------------------------------------------------------------------- row-level rules
def test_decision_yes_no_threshold_tie_and_missing():
    r = {"qtype": "noul", "options": None, "gold": 1}
    assert S.decision(r, yn(.51)) == "yes"
    assert S.decision(r, yn(.49)) == "no"
    assert S.decision(r, yn(.5)) is None                       # P(yes) = 0.5 is a tie
    assert S.decision(r, None) is None                         # no record
    assert S.decision(r, {"no": .2}) is None                   # no P(yes)
    assert S.decision(r, {"yes": float("nan"), "no": .5}) is None
    assert S.decision(r, {"yes": .7, "no": .7}) == "yes"       # the rule reads P(yes) only
    assert S.correct(r, yn(.5)) == 0.0 and S.correct(r, None) == 0.0 and S.correct(r, yn(.6)) == 1.0


def test_decision_choice_argmax_tie_extra_keys_absent_options():
    r = {"qtype": "choice", "options": C3, "gold": "a"}
    assert S.decision(r, {"a": .5, "b": .3, "c": .2}) == "a"
    assert S.decision(r, {"a": .4, "b": .4, "c": .2}) is None  # equal top probabilities
    assert S.decision(r, {"a": .4, "b": .3, "_raw_sum": 9.0}) == "a"  # non-option keys ignored; absent c = 0
    assert S.decision(r, {"zzz": 1.0}) is None                 # no option has mass: all 0, a tie
    assert S.decision(r, {"a": float("inf")}) is None          # non-finite = missing
    assert S.correct(r, {"a": .4, "b": .4, "c": .2}) == 0.0
    assert S.correct(r, None) == 0.0


def test_brier_missing_scores_one():
    r = {"qtype": "noul", "options": None, "gold": 0}
    assert S.brier(r, yn(.3)) == pytest.approx(.09)
    assert S.brier(r, None) == 1.0
    assert S.brier({**r, "gold": 1}, {"no": .1}) == 1.0


def test_complement_pair_tie_and_missing_are_violations():
    a, b = {"qtype": "noul", "options": None, "gold": 1}, {"qtype": "noul", "options": None, "gold": 0}
    assert S.complement_pair(a, yn(.9), b, yn(.2)) == (0.0, pytest.approx(.1))
    assert S.complement_pair(a, yn(.9), b, yn(.8))[0] == 1.0   # both yes
    assert S.complement_pair(a, yn(.1), b, yn(.2))[0] == 1.0   # both no
    assert S.complement_pair(a, yn(.5), b, yn(.2)) == (1.0, pytest.approx(.3))  # tie on the base row
    assert S.complement_pair(a, yn(.9), b, None) == (1.0, 1.0)  # missing: violation, |.| scored 1
    assert S.complement_pair(a, None, b, None) == (1.0, 1.0)


def test_perm_pair_aligned_by_name_tv_and_drift():
    a = {"qtype": "choice", "options": C3, "gold": "a"}
    b = {"qtype": "choice", "options": C3[::-1], "gold": "a"}
    d, tv = S.perm_pair(a, {"a": .7, "b": .2, "c": .1}, b, {"c": .6, "b": .1, "a": .3})
    assert d == 1.0 and tv == pytest.approx(.5)
    d, tv = S.perm_pair(a, {"a": .5, "b": .3, "c": .2}, b, {"c": .2, "b": .3, "a": .5})
    assert d == 0.0 and tv == pytest.approx(0.0)
    assert S.perm_pair(a, {"a": .4, "b": .4, "c": .2}, b, {"c": .2, "b": .3, "a": .5}) == (1.0, pytest.approx(.1))
    assert S.perm_pair(a, {"a": .5, "b": .3, "c": .2}, b, None) == (1.0, 1.0)
    # renormalised over the row's options (a stray non-option key does not count)
    assert S.perm_pair(a, {"a": .5, "b": .3, "c": .2, "_raw_sum": 7}, b, {"a": 1.0, "b": .6, "c": .4})[1] == \
        pytest.approx(0.0)


# ---------------------------------------------------------------------------------------------- multiplicity / tests
def test_holm_matches_definition():
    adj = S.holm({"m": .01, "M": .04, "b": .03})
    assert adj == pytest.approx({"m": .03, "b": .06, "M": .06})
    assert S.holm({"x": .5, "y": .6}) == pytest.approx({"x": 1.0, "y": 1.0})


def test_bh_matches_definition_and_brute_force():
    q = S.bh({"a": .01, "b": .02, "c": .03, "d": .04, "e": .2})
    assert q == pytest.approx({"a": .05, "b": .05, "c": .05, "d": .05, "e": .2})
    rng = np.random.default_rng(3)
    p = {f"k{j}": float(x) for j, x in enumerate(rng.uniform(0, .2, 25))}
    q = S.bh(p)
    srt = sorted(p.values())
    for k, v in p.items():  # q_i = min over j >= rank(i) of m p_(j) / j
        r = srt.index(v) + 1
        assert q[k] == pytest.approx(min(1.0, min(len(p) * srt[j - 1] / j for j in range(r, len(p) + 1))))


def test_mcnemar_exact_matches_scipy():
    from scipy.stats import binomtest
    for b, c in [(57, 83), (62, 79), (3, 0), (10, 10), (0, 1), (120, 80)]:
        assert S.mcnemar_exact(b, c) == pytest.approx(binomtest(b, b + c, .5).pvalue, rel=1e-9)
    assert S.mcnemar_exact(0, 0) == 1.0


def test_verdict_rule_as_written():
    v = S.verdict_primary(.5, 3.0, .01, 2.0)
    assert v["label"] == "beats" and v["matches"]
    assert S.verdict_primary(.5, 3.0, .07, 2.0)["label"] == "matches"   # CI above 0 but Holm p >= 0.05
    assert S.verdict_primary(-1.9, 1.0, .5, 2.0)["label"] == "matches"
    v = S.verdict_primary(-1.5, -0.2, .01, 2.0)                            # within the margin, but Jev is ahead
    assert v["label"] == "matches" and v["ci_below_0"]
    assert S.verdict_primary(-2.5, -0.2, .01, 2.0)["label"] == "jev_better"
    assert S.verdict_primary(-2.5, 0.4, .3, 2.0)["label"] == "neither"
    assert S.verdict_primary(-0.011, 0.02, .3, 0.010)["label"] == "neither"  # Brier margin
    assert S.verdict_primary(-0.009, 0.02, .3, 0.010)["label"] == "matches"


# ---------------------------------------------------------------------------------------------- bench and bootstrap
def test_bench_base_rows_pairs_and_groups():
    rows, rels = synthetic_split()
    b = S.Bench(rows, rels)
    assert len(b.base) == 16 and not any(i.endswith(("_neg", "_perm")) for i in b.base)
    assert len(b.neg_pairs) == 4 and len(b.perm_pairs) == 3
    assert b.tasks == ["c1", "c2", "y1"] and b.task_groups["c1"][0] == "g_c1_0" and len(b.task_groups["c1"]) == 5
    c = b.counts()
    assert c["yes_no_base"] == 6 and c["over_26_base"] == 4 and c["groups"] == 15
    half = S.Bench(rows, rels, "A")
    assert all(half.rows[i]["meta"]["half"] == "A" for i in half.rows)


def test_bench_rejects_broken_pairs():
    rows, rels = synthetic_split()
    bad = [dict(r) for r in rows]
    for r in bad:
        if r["id"] == "y1_0_neg":
            r["group_id"] = "g_other"
    with pytest.raises(SystemExit):
        S.Bench(bad, rels)
    bad = [dict(r) for r in rows]
    for r in bad:
        if r["id"] == "y1_0_neg":
            r["gold"] = 1  # not complementary to the base gold 1
    with pytest.raises(SystemExit):
        S.Bench(bad, rels)


def test_boot_draws_match_score_ohs_loop_order():
    """Same rng stream and order as score_ohs.py: for each resample, for each sorted task, integers(0, n, n)."""
    rows, rels = synthetic_split()
    b = S.Bench(rows, rels)
    boot = S.Boot(b, 50, 0)
    rng = np.random.default_rng(0)
    for k in range(50):
        for t, blk in zip(b.tasks, boot.blocks):
            n = len(b.task_groups[t])
            assert np.array_equal(boot.W[k, blk], np.bincount(rng.integers(0, n, n), minlength=n))
    assert (boot.W[:, boot.blocks[0]].sum(1) == 5).all()  # stratified: each task keeps its number of groups


def test_identical_systems_give_zero_difference_and_p_one():
    rows, rels = synthetic_split()
    b = S.Bench(rows, rels)
    boot = S.Boot(b, 200, 0)
    P = jev_run()
    res = S.score_model(b, boot, [P], [P, P])
    for v in res["primary"].values():
        assert v["diff"] == 0 and v["ci95"] == [0, 0] and v["p"] == 1.0
        assert v["verdict"]["label"] == "matches"


def test_exact_zero_difference_counts_in_both_tails():
    """(0.1 + 0.2 - 0.3) / 3 is 1.85e-17 in floating point; the exact difference is 0, so p must be 1."""
    class FakeBoot:  # per-task sums (OD correct, Jev correct, rows): task diffs +0.1, +0.2, -0.3
        def task_sums(self, Q):
            obs = np.array([[1., 0., 10.], [2., 0., 10.], [0., 3., 10.]])
            return obs, obs[None].copy()

    assert (np.array([.1, .2, -.3])).mean() != 0  # the float noise this guards against
    res = S.ratio_endpoint(FakeBoot(), np.zeros(3), np.zeros(3), np.ones(3), "macro", True, 1.0)
    assert res["p"] == 1.0 and res["ci95"] == [0.0, 0.0]


def _naive_bootstrap(bench, od, jevs, n_boot):
    """Reference: materialise every resample's rows and pairs and recompute in exact arithmetic."""
    rng = np.random.default_rng(0)
    rows_of, pairs_of = defaultdict(list), defaultdict(list)
    for i in bench.base:
        rows_of[(bench.task[i], bench.rows[i]["group_id"])].append(i)
    for a, b in bench.neg_pairs:
        pairs_of[(bench.task[a], bench.rows[a]["group_id"])].append((a, b))

    def val(fn, runs, i):
        return sum(Fraction(fn(bench.rows[i], P.get(i, {}).get("probs"))) for P in runs) / len(runs)

    micro, macro, brier, viol = [], [], [], []
    for _ in range(n_boot):
        drawn = []
        for t in bench.tasks:
            gs = bench.task_groups[t]
            drawn += [(t, gs[k]) for k in rng.integers(0, len(gs), len(gs))]
        ids = [i for g in drawn for i in rows_of[g]]
        d = [val(S.correct, [od], i) - val(S.correct, jevs, i) for i in ids]
        micro.append(sum(d) / len(d))
        per = defaultdict(list)
        for i, x in zip(ids, d):
            per[bench.task[i]].append(x)
        macro.append(sum(sum(v) / len(v) for v in per.values()) / len(per))
        y = [i for i in ids if bench.rows[i]["qtype"] == "noul"]
        brier.append(sum(val(S.brier, jevs, i) - val(S.brier, [od], i) for i in y) / len(y))
        pr = [p for g in drawn for p in pairs_of[g]]
        vv = []
        for a, b in pr:
            jo = sum(Fraction(S.complement_pair(bench.rows[a], P.get(a, {}).get("probs"), bench.rows[b],
                                                P.get(b, {}).get("probs"))[0]) for P in jevs) / len(jevs)
            oo = Fraction(S.complement_pair(bench.rows[a], od.get(a, {}).get("probs"), bench.rows[b],
                                            od.get(b, {}).get("probs"))[0])
            vv.append(jo - oo)
        viol.append(sum(vv) / len(vv) if vv else None)

    def summ(res):
        res = np.array([float(x) for x in res if x is not None])
        exact_le = sum(1 for x in res if x <= 0)
        exact_ge = sum(1 for x in res if x >= 0)
        return np.percentile(res, [2.5, 97.5]), min(1.0, 2 * min(exact_le, exact_ge) / len(res))
    return {"micro": summ(micro), "macro": summ(macro), "brier_yesno": summ(brier), "complement_violation": summ(viol)}


def test_vectorised_cluster_bootstrap_matches_naive_reference(tmp_path):
    rows, rels = synthetic_split()
    write_split(tmp_path, rows=rows, rels=rels)
    bench = S.Bench(rows, rels)
    load = lambda n: S.load_preds(tmp_path / f"preds_syn/{n}.jsonl")[0]  # noqa: E731
    od, jevs = load("od"), [load("jevA"), load("jevB")]
    n_boot = 300
    res = S.score_model(bench, S.Boot(bench, n_boot, 0), [od], jevs)
    ref = _naive_bootstrap(bench, od, jevs, n_boot)
    for k in ("micro", "macro", "brier_yesno"):
        scale = 1.0 if k == "brier_yesno" else 100.0
        assert np.allclose(np.array(res["primary"][k]["ci95"]) / scale, ref[k][0], atol=1e-12), k
        assert res["primary"][k]["p"] == pytest.approx(ref[k][1]), k
    v = res["secondary"]["complement_violation"]
    assert np.allclose(v["ci95"], ref["complement_violation"][0], atol=1e-12)
    assert v["p"] == pytest.approx(ref["complement_violation"][1])


# ---------------------------------------------------------------------------------------------- end to end
def test_end_to_end_values_signs_and_reports(tmp_path):
    write_split(tmp_path)
    out = S.main(["--split", "syn", "--root", str(tmp_path), "--model", "od", "--jev", "jevA,jevB",
                  "--boot", "300", "--out", str(tmp_path / "res.json")])
    assert json.loads((tmp_path / "res.json").read_text())["models"]["od"]["config_bc"] == "od_bc"
    m = out["models"]["od"]
    pr = m["primary"]
    # OD: c1 3/6, c2 3/4, y1 3/6 -> micro 9/16, macro (0.5 + 0.75 + 0.5) / 3
    assert pr["micro"]["od"] == pytest.approx(100 * 9 / 16, abs=1e-4)
    assert pr["macro"]["od"] == pytest.approx(100 * (0.5 + 0.75 + 0.5) / 3, abs=1e-4)
    # Jev = per-row mean of the runs: run A 15/16, run B 13/16 (c1_4 missing, y1_5 tie) -> 14/16
    assert pr["micro"]["jev"] == pytest.approx(100 * 14 / 16, abs=1e-4)
    assert pr["macro"]["jev"] == pytest.approx(100 * (5.5 / 6 + 0.75 + 5.5 / 6) / 3, abs=1e-4)
    assert pr["micro"]["diff"] == pytest.approx(100 * (9 - 14) / 16, abs=1e-4)
    # Brier: OD (0.01 + 0.04 + 0.25 + 0.36 + 1 + 0.16) / 6; Jev mean of 0.01 and 0.05; diff = Jev - OD (< 0 here)
    assert pr["brier_yesno"]["od"] == pytest.approx(1.82 / 6, abs=1e-6)
    assert pr["brier_yesno"]["jev"] == pytest.approx(0.03, abs=1e-6)
    assert pr["brier_yesno"]["diff"] == pytest.approx(0.03 - 1.82 / 6, abs=1e-6)
    assert pr["brier_yesno"]["ci95"][1] < 0 and pr["brier_yesno"]["verdict"]["label"] != "beats"
    # complement: OD violations 2/4 (tie on y1_2, missing y1_3_neg); Jev 0 -> diff Jev - OD = -0.5
    cv = m["secondary"]["complement_violation"]
    assert (cv["od"], cv["jev"], cv["diff"], cv["n"]) == (0.5, 0.0, -0.5, 4)
    assert m["descriptive"]["complement_mean_abs_dev"]["od"] == pytest.approx((0.1 + 0.1 + 0.2 + 1.0) / 4)
    assert m["descriptive"]["acc_neg_rows"]["od"] == pytest.approx(75.0)
    # option order: OD drift 2/3 (tie on c1_2, flip on c1_3), TV (0 + 0.1 + 0.5) / 3, accuracy on _perm rows 2/3
    od_ = m["secondary"]["option_order_drift"]
    assert od_["od"] == pytest.approx(2 / 3) and od_["jev"] == 0.0 and od_["diff"] == pytest.approx(-2 / 3)
    assert m["descriptive"]["option_order_tv"]["od"] == pytest.approx(0.2)
    assert m["descriptive"]["acc_perm_rows"]["od"] == pytest.approx(100 * 2 / 3)
    # secondary family and BH
    fam = set(m["secondary_family"])
    assert {"acc_track_F", "acc_track_U", "acc_over_26_options", "complement_violation", "option_order_drift",
            "bc_micro", "bc_macro", "bc_brier_yesno", "acc_task_c1", "acc_task_c2", "acc_task_y1", "acc_half_A",
            "acc_half_S", "mcnemar_vs_jevA", "mcnemar_vs_jevB"} == fam
    assert all(v["q_bh"] >= v["p"] - 1e-12 for v in m["secondary"].values())
    assert m["secondary"]["acc_over_26_options"]["n"] == 4
    assert m["secondary"]["bc_micro"]["od"] == pytest.approx(100 * 10 / 16, abs=1e-4)
    # missing answers and ties reported separately
    J = out["jev"]["per_run"]
    assert J["jevB"]["missing_base"] == 1 and J["jevB"]["missing_base_by_task"] == {"c1": 1}
    assert J["jevB"]["tie_base"] == 1 and J["jevA"]["missing_base"] == 0
    assert J["jevA"]["micro_pct"] == pytest.approx(100 * 15 / 16, abs=1e-4)
    assert m["od_answers"]["missing_base"] == 2 and m["od_answers"]["missing_twin"] == 1
    assert m["od_answers"]["tie_base"] == 2
    assert out["jev"]["run_agreement"]["correctness"] == pytest.approx(14 / 16)
    assert "--boot 300 (PREREG: 10,000)" in out["deviations"]


def test_brier_sign_positive_when_opendecide_is_better(tmp_path):
    good = {**OD, **{f"y1_{k}": yn(1.0 if k % 2 == 0 else 0.0) for k in range(6)}}
    write_split(tmp_path, preds={"od": good, "jevA": jev_run(), "jevB": jev_run()})
    out = S.main(["--split", "syn", "--root", str(tmp_path), "--model", "od", "--jev", "jevA,jevB",
                  "--boot", "200", "--out", str(tmp_path / "r.json")])
    b = out["models"]["od"]["primary"]["brier_yesno"]
    assert b["od"] == 0.0 and b["jev"] == pytest.approx(0.01) and b["diff"] == pytest.approx(0.01)
    assert b["ci95"][0] > 0


def test_missing_prediction_file_is_an_error(tmp_path):
    write_split(tmp_path)
    with pytest.raises(FileNotFoundError):
        S.main(["--split", "syn", "--root", str(tmp_path), "--model", "od", "--jev", "jevA,jevNOPE",
                "--boot", "50", "--out", str(tmp_path / "r.json")])


def test_ohs3_split_enforces_frozen_files(tmp_path):
    """A synthetic file named ohs3 does not have the frozen sha256: the scorer stops, or records the deviation."""
    write_split(tmp_path, split="ohs3")
    args = ["--split", "ohs3", "--root", str(tmp_path), "--model", "od", "--jev", "jevA,jevB", "--boot", "50",
            "--out", str(tmp_path / "r.json")]
    with pytest.raises(SystemExit, match="STOP"):
        S.main(args)
    out = S.main(args + ["--allow-deviation"])
    assert any("sha256" in d for d in out["deviations"]) and any("counts differ" in d for d in out["deviations"])
    assert out["data"]["frozen_sha256_ok"] == {"ohs3.jsonl": False, "ohs3_relations.jsonl": False}


def test_ohs3_split_requires_two_jev_runs(tmp_path):
    write_split(tmp_path, split="ohs3")
    out = S.main(["--split", "ohs3", "--root", str(tmp_path), "--model", "od", "--jev", "jevA", "--boot", "50",
                  "--out", str(tmp_path / "r.json"), "--allow-deviation"])
    assert any("two Jev runs" in d for d in out["deviations"])


def test_audit_regressions_vs_score_ohs():
    """The three audit findings, stated as behaviour: missing answers are violations, not skipped; the endpoint is the
    share of non-complementary decisions, not mean |pa + pb - 1|; the Brier difference is Jev - OD."""
    a, b = {"qtype": "noul", "options": None, "gold": 1}, {"qtype": "noul", "options": None, "gold": 0}
    assert S.complement_pair(a, yn(.9), b, None)[0] == 1.0
    viol, dev = S.complement_pair(a, yn(.55), b, yn(.55))   # small |.| = 0.1 but both say yes
    assert viol == 1.0 and dev == pytest.approx(.1)
    rows, rels = synthetic_split()
    bench = S.Bench(rows, rels)
    P_good = {i: {"probs": yn(1.0 if bench.rows[i]["gold"] == 1 else 0.0)} for i in bench.rows
              if bench.rows[i]["qtype"] == "noul"}
    P_bad = {i: {"probs": yn(.6 if bench.rows[i]["gold"] == 1 else .4)} for i in P_good}
    res = S.primary_endpoints(bench, S.Boot(bench, 100, 0), [P_good], [P_bad, P_bad])
    assert res["brier_yesno"]["diff"] == pytest.approx(0.16)  # OD better -> positive
