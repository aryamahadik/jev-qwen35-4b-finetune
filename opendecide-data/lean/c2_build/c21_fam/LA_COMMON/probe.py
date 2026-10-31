"""CPU probe harness for the pre-freeze shortcut gates (global ruling G5), as the L-A STAND-IN for L-0's single
harness. Same protocol, so L-0's harness can replace it without changing any gate definition:

  * held-out split GROUPED by spec family (no group in both train and held-out); design: 30% held out, 5 random
    group splits, mean reported;
  * L2 logistic regression with a FIXED regularisation (C=1.0 on standardised features), never tuned on held-out;
  * AUC is reported as max(AUC, 1 - AUC); upper bound = 97.5th percentile of 2,000 cluster-bootstrap resamples
    over held-out groups;
  * k-way probes use BALANCED accuracy (mean per-class recall);
  * every run includes a label-permutation check (AUC 0.50 +- 0.03) and an injected-leak power check (a planted
    one-feature leak must reach AUC >= 0.80), else the run is INVALID and is repeated (not a fix iteration);
  * binary bar: AUC <= 0.55 and upper bound <= 0.60; k-way bar: <= 1/k + 3 pp and upper bound <= 1/k + 6 pp.
GBT probes are advisory only (not implemented here).
"""
import numpy as np
from scipy.stats import rankdata
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler

N_BOOT = 2000
HELD = 0.30
N_SPLITS = 5


def _fold(a):
    return max(a, 1.0 - a)


def fast_auc(score, y):
    y = np.asarray(y)
    pos = y == 1
    n1, n0 = int(pos.sum()), int((~pos).sum())
    if n1 == 0 or n0 == 0:
        return 0.5
    r = rankdata(score)
    return (r[pos].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0)


def _matrix(feature_dicts, extra=None):
    dv = DictVectorizer(sparse=False)
    X = dv.fit_transform(feature_dicts)
    if extra is not None:
        X = np.hstack([X, np.asarray(extra, dtype=float).reshape(len(X), -1)])
    return X


def _fit_predict(Xtr, ytr, Xte, multi=False):
    sc = StandardScaler().fit(Xtr)
    clf = LogisticRegression(C=1.0, max_iter=2000)
    clf.fit(sc.transform(Xtr), ytr)
    if multi:
        return clf.predict(sc.transform(Xte))
    return clf.predict_proba(sc.transform(Xte))[:, 1]


def _splits(groups, seed):
    gss = GroupShuffleSplit(n_splits=N_SPLITS, test_size=HELD, random_state=seed)
    return list(gss.split(np.zeros(len(groups)), groups=groups))


def _boot_ub(group_ids, score, y, stat, rng, n_boot):
    """Cluster bootstrap over groups: returns the 97.5th percentile of the folded statistic."""
    ug, inv = np.unique(group_ids, return_inverse=True)
    members = [np.where(inv == i)[0] for i in range(len(ug))]
    vals = []
    for _ in range(n_boot):
        pick = rng.integers(0, len(ug), len(ug))
        idx = np.concatenate([members[i] for i in pick])
        vals.append(stat(score[idx], y[idx]))
    return float(np.percentile(vals, 97.5))


def _binary_once(X, y, groups, seed):
    y = np.asarray(y)
    groups = np.asarray(groups)
    sc_all, y_all, g_all, aucs = [], [], [], []
    for tr, te in _splits(groups, seed):
        if len(set(y[tr])) < 2 or len(set(y[te])) < 2:
            continue
        s = _fit_predict(X[tr], y[tr], X[te])
        aucs.append(fast_auc(s, y[te]))
        sc_all.append(s)
        y_all.append(y[te])
        g_all.append(groups[te])
    if not aucs:
        return None
    return float(np.mean(aucs)), np.concatenate(sc_all), np.concatenate(y_all), np.concatenate(g_all)


def binary_probe(feature_dicts, y, groups, seed=0, n_boot=N_BOOT):
    """AUC probe. y in {0,1}. Returns dict with auc (folded), ub, perm_auc, leak_auc, valid, pass."""
    X = _matrix(feature_dicts)
    y = np.asarray(y)
    groups = np.asarray(groups)
    base = _binary_once(X, y, groups, seed)
    if base is None:
        return {"auc": None, "ub": None, "valid": False, "pass": False, "why": "single-class split"}
    auc, s, yy, gg = base
    rng = np.random.default_rng(seed)
    ub = _boot_ub(gg, s, yy, lambda a, b: _fold(fast_auc(a, b)), rng, n_boot)
    # label-permutation check: shuffle labels at GROUP level so within-group structure is preserved
    perm_y = _group_permute(y, groups, seed + 1)
    pb = _binary_once(X, perm_y, groups, seed + 2)
    perm_auc = pb[0] if pb else 0.5
    # injected-leak power check: plant one feature equal to the label
    leak = _binary_once(np.hstack([X, y.reshape(-1, 1).astype(float)]), y, groups, seed + 3)
    leak_auc = _fold(leak[0]) if leak else 0.5
    valid = abs(perm_auc - 0.50) <= 0.03 and leak_auc >= 0.80
    a = _fold(auc)
    return {"auc": a, "ub": ub, "perm_auc": perm_auc, "leak_auc": leak_auc, "valid": bool(valid),
            "pass": bool(valid and a <= 0.55 and ub <= 0.60), "n": int(len(y)), "groups": int(len(set(groups)))}


def _group_permute(y, groups, seed):
    rng = np.random.default_rng(seed)
    ug = np.unique(groups)
    first = {g: y[np.where(groups == g)[0][0]] for g in ug}
    lab = np.array([first[g] for g in ug])
    rng.shuffle(lab)
    m = dict(zip(ug, lab))
    return np.array([m[g] for g in groups])


def _bal_acc(pred, y):
    cls = np.unique(y)
    return float(np.mean([np.mean(pred[y == c] == c) for c in cls]))


def kway_probe(feature_dicts, y, groups, seed=0, n_boot=N_BOOT):
    """k-way probe with balanced accuracy. y: integer or string labels."""
    labels = sorted(set(y))
    k = len(labels)
    yi = np.array([labels.index(v) for v in y])
    X = _matrix(feature_dicts)
    groups = np.asarray(groups)

    def once(Xm, yv, sd):
        accs, P, Y, G = [], [], [], []
        for tr, te in _splits(groups, sd):
            if len(set(yv[tr])) < 2:
                continue
            p = _fit_predict(Xm[tr], yv[tr], Xm[te], multi=True)
            accs.append(_bal_acc(p, yv[te]))
            P.append(p)
            Y.append(yv[te])
            G.append(groups[te])
        if not accs:
            return None
        return float(np.mean(accs)), np.concatenate(P), np.concatenate(Y), np.concatenate(G)

    base = once(X, yi, seed)
    if base is None:
        return {"bal_acc": None, "ub": None, "valid": False, "pass": False, "k": k}
    acc, P, Y, G = base
    rng = np.random.default_rng(seed)
    ub = _boot_ub(G, P, Y, lambda a, b: _bal_acc(a, b), rng, n_boot)
    perm = once(X, _group_permute(yi, groups, seed + 1), seed + 2)
    perm_acc = perm[0] if perm else 1.0 / k
    onehot = np.eye(k)[yi]
    leak = once(np.hstack([X, onehot]), yi, seed + 3)
    leak_acc = leak[0] if leak else 0.0
    valid = abs(perm_acc - 1.0 / k) <= 0.03 and leak_acc >= 0.80
    return {"bal_acc": acc, "ub": ub, "perm_acc": perm_acc, "leak_acc": leak_acc, "k": k, "valid": bool(valid),
            "pass": bool(valid and acc <= 1.0 / k + 0.03 and ub <= 1.0 / k + 0.06), "n": int(len(yi)),
            "groups": int(len(set(groups)))}


def run_valid(fn, *a, retries=3, **kw):
    """A run that fails the permutation or leak-power check is invalid and is REPEATED (new seed), not a fix iteration."""
    r = None
    for i in range(retries):
        r = fn(*a, seed=i * 17, **kw)
        if r.get("valid"):
            r["attempts"] = i + 1
            return r
    r["attempts"] = retries
    return r
