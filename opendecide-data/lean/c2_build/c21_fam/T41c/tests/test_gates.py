"""Gates: machinery, thresholds and failure detection (no gate is asserted to pass on the TEST pool where the test
pool is the reason it cannot: wording gates K12 need >= 50 wordings per cell and a real pool)."""
import copy
import json
from dataclasses import replace

import numpy as np
import pytest

from t41c import build, gates, ids, planner, probe, truth
from t41c.spec import label_of


def test_k4_detects_each_kind_of_composition_error(plan2000):
    ok = gates.gate_k4(plan2000, 2000)
    assert ok["pass"]
    # drop a whole subtype: shares and benign share move
    r = gates.gate_k4([s for s in plan2000 if s.subtype != "sub.delegated"], 2000)
    assert not r["pass"] and any("sub.delegated" in f or "benign" in f for f in r["fails"])
    # break the stratum: everything present
    allp = [replace(s, facts=replace(s.facts, present=True)) for s in plan2000]
    r = gates.gate_k4(allp, 2000)
    assert not r["pass"] and any("facts-absent" in f for f in r["fails"])
    # remove all multi rows
    r = gates.gate_k4([s for s in plan2000 if len(s.directives) < 2], 2000)
    assert r["multi_directive_share"] < 0.10 and any("multi-directive" in f for f in r["fails"])


def test_k5_bars(plan2000):
    r = gates.gate_k5(plan2000)
    assert r["pass"] and 0.40 <= r["p_allow_benign_given_clause"] <= 0.70 and r["delegated_hard_share"] >= 0.08
    only_hard = [s for s in plan2000 if label_of(s) == "BLOCK" and s.pointer.mode != "deleg.none"]
    assert not gates.gate_k5(only_hard)["pass"]


def test_k8_reports_and_bars(built2000):
    rows, _ = built2000
    r = gates.gate_k8(rows)
    assert r["mean"] <= 800 and r["max"] <= 1536
    long = gates.gate_k8(rows, token_fn=lambda t: 2000)
    assert not long["pass"]


def test_k9_names_and_heldout(plan2000, built2000, heldout):
    rows, rep = built2000
    r = gates.gate_k9([s for s, _ in rows], rep, heldout=heldout)
    assert r["pass"], r
    leak = [replace(s, carrier_format=heldout["formats"][0]) for s, _ in rows[:20]]
    assert not gates.gate_k9(leak, rep, heldout=heldout)["pass"]


def test_k12_needs_a_real_pool(built2000):
    rows, _ = built2000
    r = gates.gate_k12(rows)
    assert r["top_wording_share"] <= 0.02                    # the generator spreads picks
    assert r["exact_dup_directive_share"] <= 0.02
    assert not r["pass"] and r["task_cells_below_50"] == r["n_task_cells"]    # test pool has < 50 task wordings per cell


def test_probe_detects_planted_leak_and_ignores_noise():
    rng = np.random.default_rng(0)
    n = 1200
    groups = [str(i // 2) for i in range(n)]
    y = rng.integers(0, 2, n)
    from scipy import sparse
    noise = sparse.csr_matrix(rng.integers(0, 2, (n, 12)).astype(float))
    r = probe.binary_probe(noise, y, groups, 0, 200)
    assert r["auc"] < 0.58 and abs(r["perm_auc"] - 0.5) < 0.04
    leaky = sparse.hstack([noise, sparse.csr_matrix((y * (rng.random(n) < 0.9)).reshape(-1, 1).astype(float))]).tocsr()
    r2 = probe.binary_probe(leaky, y, groups, 0, 200)
    assert r2["auc"] > 0.80
    assert probe.power_check(noise, y, groups) >= 0.80


def test_probe_groups_never_straddle_folds():
    groups = [str(i // 3) for i in range(300)]
    folds = probe.group_folds(groups, 5, 0)
    seen = {}
    for g, f in zip(groups, folds):
        assert seen.setdefault(g, f) == f
    assert len(set(folds)) == 5


def test_kway_probe_balanced_accuracy_on_chance():
    rng = np.random.default_rng(1)
    from scipy import sparse
    X = sparse.csr_matrix(rng.integers(0, 2, (800, 6)).astype(float))
    y = rng.integers(0, 4, 800)
    r = probe.kway_probe(X, y, [str(i) for i in range(800)], 0, 100)
    assert 0.2 < r["bal_acc"] < 0.31 and r["k"] == 4


def test_constant_feature_scores_exactly_chance_not_a_fold_artifact():
    from scipy import sparse
    y = np.array([0, 1] * 400)
    X = sparse.csr_matrix(np.ones((800, 1)))
    s = probe.oof_scores(X, y, [str(i) for i in range(800)])
    assert probe.auc_max(y, s) == pytest.approx(0.5, abs=1e-9)


def test_k1_machinery_and_planted_leak(built2000):
    rows, _ = built2000
    r = gates.gate_k1(rows, boot=100)
    assert set(r["views"]) == {"B1", "B2", "B3", "4way"}
    assert r["views"]["B1"]["power_auc"] >= 0.80                       # K7 power control
    assert r["views"]["B1"]["auc"] < 0.60                              # format-only B1 is near chance
    leak = lambda s, rr: dict(gates.k1_features(s, rr), **({"key=__leak__": 1} if label_of(s) in ("BLOCK", "ASK") else {}))
    r2 = gates.gate_k1(rows, boot=100, feature_fn=leak)
    assert r2["views"]["B1"]["auc"] > 0.80 and not r2["pass"] and "B1" in r2["failing"]


def test_k1_features_exclude_slot_text_and_source_tag(built2000):
    rows, _ = built2000
    s, r = next((s, r) for s, r in rows if s.directives and s.directives[0].agent_directed)
    f = gates.k1_features(s, r)
    assert not any(k.startswith("src=") for k in f)
    m = gates.masked_flat(r)
    assert gates.PLACEHOLDER in m
    for t in r.slot_texts:
        assert t not in m


def test_k1_masked_text_is_identical_across_label_twins(built2000):
    rows, _ = built2000
    import collections
    by = collections.defaultdict(set)
    for s, r in rows:
        if s.pair_kind in ("triple", "splice"):
            by[s.group_id].add(gates.masked_flat(r))
    assert all(len(v) == 1 for v in by.values())


def test_k2_machinery(built2000):
    rows, _ = built2000
    r = gates.gate_k2(rows, boot=100)
    assert r["wrapper_share_max_diff"] <= 0.05
    assert r["views"]["B1"]["power_auc"] >= 0.80
    # a wrapper that tracks the label is caught by the 5 pp share rule
    skew = [(replace(s, directives=tuple(replace(d, wrapper="wrap.urgency" if label_of(s) == "BLOCK" else d.wrapper)
                                         for d in s.directives)), rr) for s, rr in rows]
    assert not gates.gate_k2(skew, boot=50)["pass"]


def test_k2_slot_count_does_not_depend_on_label(plan2000):
    import collections
    by = collections.defaultdict(list)
    for s in plan2000:
        by[label_of(s)].append(len(s.directives) + len(s.fills))
    rates = {l: np.mean([n == 2 for n in v]) for l, v in by.items()}
    assert max(rates.values()) - min(rates.values()) < 0.04, rates


def test_k3_machinery(built2000, ho_built):
    rows, _ = built2000
    _, ho_rows, _ = ho_built
    r = gates.gate_k3(rows[:900], ho_rows[:200], boot=100)
    for k in ("in_family_ba", "held_out_ba", "gap_ba", "in_family_auc", "held_out_auc", "gap_auc", "held_out_ba_ci95"):
        assert k in r
    assert r["held_out_ba_ci95"][0] <= r["held_out_ba"] <= r["held_out_ba_ci95"][1]


def test_k6_row_harness_uses_only_the_export(built2000):
    rows, _ = built2000
    sub = rows[:200]
    table_by_blob = {}
    from t41c.render import export_for_b
    for s, r in sub:
        table_by_blob[json.dumps(export_for_b(r), sort_keys=True)] = label_of(s)
    perfect = lambda ex: {"label": table_by_blob[json.dumps(ex, sort_keys=True)]}
    assert gates.gate_k6_rows(sub, perfect)["pass"]
    flip = {"n": 0}

    def noisy(ex):
        flip["n"] += 1
        lab = perfect(ex)["label"]
        return {"label": "BLOCK" if flip["n"] % 20 == 0 and lab != "BLOCK" else lab}
    r = gates.gate_k6_rows(sub, noisy)
    assert not r["pass"] and r["disagreement_rate"]["all"] > 0.02
    boom = lambda ex: (_ for _ in ()).throw(RuntimeError("x"))
    assert not gates.gate_k6_rows(sub[:10], boom)["pass"]


def test_k6_truth_tables_render_for_every_case_and_oracle_agrees():
    r = truth.run_k6_truth(truth.a_oracle, tables=("T3",), pass_spec=True)
    assert r["pass"] and r["cases"] == 264 and r["render_failures"] == 0
    r = truth.run_k6_truth(truth.a_oracle, tables=("T1", "T2"), limit=250, pass_spec=True)
    assert r["pass"] and r["cases"] == 500


def test_k6_truth_detects_a_wrong_b():
    def wrong(export):
        return {"label": "BLOCK", "directives": {}}
    r = truth.run_k6_truth(wrong, tables=("T3",))
    assert not r["pass"] and r["mismatches"] > 0


def test_t1_t2_table_sizes():
    assert len(list(truth.t1_facts())) == 1024 + 512
    assert len(truth.t1_actions()) == 28
    assert len(truth.t2_facts()) == 6
    assert len(list(truth.t3_cases())) == 264   # 288 minus the 24 agent-directed declared_policy-without-in_scope combos (not representable in a row)


def test_gate_results_carry_ids_and_tags(plan2000):
    for r in (gates.gate_k4(plan2000, 2000), gates.gate_k5(plan2000)):
        assert r["tag"] == "PRE-FREEZE KILL" and r["id"] in ("K4", "K5") and isinstance(r["pass"], bool)
