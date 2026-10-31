"""G5 sanity checks in the ONE shared k-way probe (LC_COMMON.probe.kway_probe) and the raw-indicator encoding rule
(Opus ruling, T59/T60/T63 Q7a follow-up: the permutation and leak-power checks belong to the shared harness; categorical inputs are
RAW 0/1 indicators, never standardised). Synthetic data only; nothing here reads a row."""
import numpy as np
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from LC_COMMON import probe


def _iid(k, n=900, seed=10, d=4):
    rng = np.random.RandomState(seed)
    return rng.normal(size=(n, d)), rng.randint(0, k, n), [i // 3 for i in range(n)]


def _t63_like(seed, n=110, n_ids=55):
    """3 balanced labels, wording id drawn independently of the label (each id on 2 rows), every row its own group."""
    rng = np.random.RandomState(100 + seed)
    y = np.array([i % 3 for i in range(n)])
    rng.shuffle(y)
    ids = np.repeat(np.arange(n_ids), 2)[:n]
    rng.shuffle(ids)
    return ids, y, [str(i) for i in range(n)]


# ---------------------------------------------------------------------------------------------- the checks fire
def test_checks_fire_on_degenerate_features_permutation():
    """Constant features carry no information, so the grouped CV can only predict the training prior, which is anti-correlated with
    the held-out fold of a balanced label set: the permutation mean falls far below 1/k and the run is INVALID (not pass, not fail)."""
    for seed in range(3):
        rng = np.random.RandomState(seed)
        y = np.array([i % 4 for i in range(120)])
        rng.shuffle(y)
        res = probe.kway_probe(np.ones((120, 3)), y, list(range(120)), B=20)
        assert res["perm_ok"] is False and res["perm_bal_acc"] < 0.25 - 0.03
        assert res["valid"] is False and res["status"] == "INVALID" and res["pass"] is False


def test_checks_fire_on_degenerate_groups_leak_power():
    """One group for every row leaves no training fold: the probe predicts one class (balanced accuracy exactly 1/k, which would
    pass the bar) and cannot learn the planted leak, so the run is INVALID instead of a silent pass."""
    y = np.array([i % 3 for i in range(60)])
    res = probe.kway_probe(np.random.RandomState(0).normal(size=(60, 3)), y, [0] * 60, B=20)
    assert abs(res["bal_acc"] - 1 / 3) < 1e-9 and res["upper"] <= res["bar_upper"]          # would pass the bar ...
    assert res["leak_ok"] is False and res["leak_bal_acc"] < 0.80                            # ... if the power check did not exist
    assert res["valid"] is False and res["status"] == "INVALID" and res["pass"] is False


# ---------------------------------------------------------------------------------------------- planted leak
@pytest.mark.parametrize("k", [2, 3, 4])
def test_planted_leak_is_detected_on_noise(k):
    X, y, g = _iid(k)
    res = probe.kway_probe(X, y, g, B=50, perm_check=False)
    assert res["checks_run"] == ["leak"]
    assert res["leak_ok"] is True and res["leak_bal_acc"] >= 0.80 and res["valid"] is True


def test_real_one_column_leak_in_the_features_is_a_valid_fail():
    X, y, g = _iid(3)
    X = X.copy()
    X[:, 0] += 2.0 * y                       # a real one-column label leak in the family's own features
    res = probe.kway_probe(X, y, g, B=100)
    assert res["valid"] is True and res["status"] == "FAIL" and res["pass"] is False
    assert res["bal_acc"] > 0.60 and res["bal_acc"] > res["bar"]


def test_leak_form_is_class_index_plus_noise_and_string_labels_work():
    X, y, g = _iid(3)
    names = np.array(["alpha", "beta", "gamma"])[y]
    a = probe.kway_probe(X, y, g, B=30)
    b = probe.kway_probe(X, names, g, B=30)
    assert b["leak_bal_acc"] == pytest.approx(a["leak_bal_acc"]) and b["perm_bal_acc"] == pytest.approx(a["perm_bal_acc"])


# ---------------------------------------------------------------------------------------------- permutation near 1/k
@pytest.mark.parametrize("k", [2, 3, 4])
def test_permutation_mean_is_near_chance_on_iid_labels(k):
    X, y, g = _iid(k, seed=20 + k)
    res = probe.kway_probe(X, y, g, B=50)
    assert abs(res["perm_bal_acc"] - 1.0 / k) <= 0.03 and res["perm_ok"] is True
    assert res["valid"] is True and res["status"] in ("PASS", "FAIL") and res["status"] == "PASS"
    assert res["chance"] == pytest.approx(1.0 / k)


def test_permutation_tolerance_is_a_parameter():
    X, y, g = _iid(3)
    res = probe.kway_probe(X, y, g, B=30, perm_tol=1e-6, leak_check=False)      # an impossible tolerance: the check must trip
    assert res["perm_ok"] is False and res["status"] == "INVALID"


# ---------------------------------------------------------------------------------------------- INVALID on low power
def test_invalid_status_on_low_power_carries_the_numbers():
    X, y, g = _iid(3, n=300)
    res = probe.kway_probe(X, y, g, B=30, leak_min=1.01)                      # no probe can reach this: a low-power run
    assert res["status"] == "INVALID" and res["valid"] is False and res["pass"] is False
    assert res["leak_ok"] is False
    for key in ("perm_bal_acc", "leak_bal_acc", "bal_acc", "upper", "bar", "bar_upper", "chance", "k", "n"):
        assert isinstance(res[key], (int, float)), key


def test_standardised_indicators_are_a_low_power_run_raw_indicators_are_valid():
    """The Q7a mechanism: a 1-in-77-style indicator block, standardised, swamps the planted leak (power < 0.80 -> INVALID);
    the same block as RAW 0/1 indicators lets the leak through (power 1.0)."""
    for seed in range(4):
        ids, y, g = _t63_like(seed)
        X, raw, _ = probe.indicator_matrix({"wording": ids})
        std = probe.kway_probe(X, y, g, k_classes=3, B=30, perm_check=False)
        rawr = probe.kway_probe(X, y, g, k_classes=3, B=30, perm_check=False, raw_cols=raw)
        assert std["leak_bal_acc"] < 0.80 and std["leak_ok"] is False and std["status"] == "INVALID"
        assert rawr["leak_bal_acc"] >= 0.95 and rawr["leak_ok"] is True
        assert probe.kway_probe(X, y, g, k_classes=3, B=30, perm_check=False, raw_cols="auto")["leak_bal_acc"] == pytest.approx(rawr["leak_bal_acc"])


# ---------------------------------------------------------------------------------------------- encoding
def test_indicator_matrix_is_raw_zero_one_with_a_raw_mask():
    X, raw, names = probe.indicator_matrix({"wording": ["a", "b", "a", "c"], "layout": [1, 1, 2, 2]}, X_num=[[5.0], [6.0], [7.0], [8.0]])
    assert X.shape == (4, 1 + 3 + 2) and names[0] == "num0" and names[1:4] == ["wording=a", "wording=b", "wording=c"]
    assert raw.tolist() == [False, True, True, True, True, True]
    assert set(np.unique(X[:, raw]).tolist()) == {0.0, 1.0} and X[:, 0].tolist() == [5.0, 6.0, 7.0, 8.0]
    assert X[:, raw].sum(axis=1).tolist() == [2.0, 2.0, 2.0, 2.0]               # one wording + one layout per row
    with pytest.raises(ValueError):
        probe.indicator_matrix({"a": [1, 2], "b": [1]})


def test_raw_columns_are_not_standardised_numeric_columns_still_are():
    n = 77
    ind = np.zeros((n, 1))
    ind[0, 0] = 1.0                                                              # a 1-in-77 indicator
    num = np.random.RandomState(0).normal(5.0, 3.0, size=(n, 1))
    X = np.hstack([ind, num])
    legacy = StandardScaler().fit(X).transform(X)
    assert 8.0 < legacy[0, 0] < 9.5                                              # the inflation the ruling names (~8.7)
    tf = probe._scaler(X, probe.raw_mask([0], X))
    out = tf(X)
    assert out[:, 0].max() == 1.0 and out[:, 0].min() == 0.0                     # raw indicator passes through unchanged
    assert abs(out[:, 1].mean()) < 1e-9 and abs(out[:, 1].std() - 1.0) < 1e-9    # the numeric column is standardised as before
    assert np.allclose(probe._scaler(X, None)(X), legacy)                        # raw_cols=None is the old behaviour exactly


def test_raw_mask_forms():
    X = np.array([[1.0, 0.0, 3.0, 0.0], [0.0, 1.0, 4.0, 0.0], [1.0, 1.0, 5.0, 0.0]])
    assert probe.raw_mask(None, X) is None
    assert probe.raw_mask("auto", X).tolist() == [True, True, False, False]       # 0/1-only and non-constant
    assert probe.raw_mask([2], X).tolist() == [False, False, True, False]
    assert probe.raw_mask([True, False, False, False], X).tolist() == [True, False, False, False]
    assert probe.raw_mask([], X) is None
    with pytest.raises(ValueError):
        probe.raw_mask([True, False], X)
    with pytest.raises(ValueError):
        probe.raw_mask("everything", X)


def test_raw_cols_reach_binary_and_argmax_probes_too():
    rng = np.random.RandomState(4)
    n = 400
    ids = rng.randint(0, 40, n)
    y = rng.randint(0, 2, n)
    X, raw, _ = probe.indicator_matrix({"w": ids})
    g = [i // 2 for i in range(n)]
    a = probe.binary_probe(X, y, g, B=30, raw_cols=raw)
    b = probe.binary_probe(X, y, g, B=30, raw_cols="auto")
    assert a["leak_auc"] == pytest.approx(b["leak_auc"]) and a["leak_auc"] >= 0.95
    oX = rng.normal(size=(120, 4, 3))
    oX[:, :, 2] = (rng.randint(0, 2, size=(120, 4)) > 0).astype(float)
    gold = rng.randint(0, 4, 120)
    r0 = probe.option_argmax_probe(oX, gold, list(range(120)), B=20)
    r1 = probe.option_argmax_probe(oX, gold, list(range(120)), B=20, raw_cols=[2])
    assert 0.0 <= r1["acc"] <= 1.0 and set(r0) == set(r1)


# ---------------------------------------------------------------------------------------------- backward compatibility
def _legacy_kway(X, y, groups, k=5, seed=probe.SEED):
    """The pre-G5-fix kway_probe fold loop, verbatim, as the reference for the default call."""
    X, y = np.asarray(X, dtype=float), np.asarray(y)
    folds = probe.group_folds(groups, k, seed)
    pred = np.zeros(len(y), dtype=y.dtype)
    for f in range(k):
        te, tr = folds == f, folds != f
        if len(set(y[tr])) < 2:
            pred[te] = y[tr][0] if tr.sum() else y[0]
            continue
        sc = StandardScaler().fit(X[tr])
        clf = LogisticRegression(C=probe.C_FIXED, max_iter=300).fit(sc.transform(X[tr]), y[tr])
        pred[te] = clf.predict(sc.transform(X[te]))
    return probe.balanced_accuracy(y, pred)


def test_default_call_is_backward_compatible():
    X, y, g = _iid(3, n=300, seed=7)
    res = probe.kway_probe(X, y, g, k_classes=3, B=40, seed=probe.SEED)
    assert res["bal_acc"] == pytest.approx(_legacy_kway(X, y, g))
    for key in ("bal_acc", "upper", "chance", "k", "n", "bar", "bar_upper", "pass"):          # every key the callers read
        assert key in res
    assert isinstance(res["pass"], bool) and res["bar"] == pytest.approx(1 / 3 + 0.03) and res["bar_upper"] == pytest.approx(1 / 3 + 0.06)
    assert res["status"] in ("PASS", "FAIL", "INVALID") and set(res["checks_run"]) == {"perm", "leak"}


def test_skipping_both_checks_gives_the_old_result_shape_and_a_plain_verdict():
    X, y, g = _iid(3, n=300, seed=7)
    res = probe.kway_probe(X, y, g, B=40, perm_check=False, leak_check=False)
    assert res["checks_run"] == [] and "perm_ok" not in res and "leak_ok" not in res
    assert res["valid"] is True and res["status"] in ("PASS", "FAIL") and res["pass"] == (res["status"] == "PASS")


def test_more_groups_than_folds_edge_cases_do_not_crash():
    y = np.array([0, 1, 2, 0, 1, 2])
    res = probe.kway_probe(np.random.RandomState(1).normal(size=(6, 2)), y, [0, 0, 1, 1, 2, 2], B=10)      # 3 groups < 5 folds
    assert "status" in res


def test_binary_probe_uses_the_callers_fold_count_in_the_leak_check():
    """The permutation loop used to rebind `k`, so the leak check silently ran with 5 folds whatever the caller asked for."""
    rng = np.random.RandomState(2)
    n = 300
    X = rng.normal(size=(n, 3))
    y = rng.randint(0, 2, n)
    g = [i // 2 for i in range(n)]
    res = probe.binary_probe(X, y, g, k=3, B=20)
    Xl = np.hstack([X, (y + np.random.RandomState(probe.SEED + 2).normal(0, 0.15, n)).reshape(-1, 1)])
    assert res["leak_auc"] == pytest.approx(probe.sym_auc(y, probe.oof_scores(Xl, y, g, 3, probe.SEED)))
