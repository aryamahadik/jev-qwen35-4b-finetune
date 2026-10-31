"""CPU probe harness with the G5 contract (LOCAL REFERENCE; L-0 owns the one harness every family must use).

G5: grouped split (no group in train and held-out); L2 logistic regression with FIXED regularisation (never tuned on
held-out); AUC reported as max(AUC, 1 - AUC); upper bound = 97.5th percentile of 2,000 cluster-bootstrap resamples
over held-out groups, on out-of-fold predictions of a 5-fold group CV; k-way probes use balanced accuracy; every run
includes a label-permutation sanity check (AUC 0.50 +- 0.03) and an injected-leak power check (planted one-feature
leak must reach AUC >= 0.80), else the run is INVALID (a repeat of an invalid run is not a fix iteration).
This file is the T41c builder's stand-in so the gates run on CPU before L-0's harness is wired; `ProbeHarness` is the
seam: pass any object with the same four methods to gates.py.
"""
import random
import zlib
import numpy as np
from scipy import sparse
from scipy.stats import rankdata
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

BOOT = 2000
C_FIXED = 1.0
PERM_TOL = 0.03
POWER_MIN = 0.80


def auc_max(y, score):
    y = np.asarray(y)
    if len(set(y.tolist())) < 2:
        return 0.5
    a = roc_auc_score(y, score)
    return max(a, 1.0 - a)


def balanced_accuracy(y, pred):
    y, pred = np.asarray(y), np.asarray(pred)
    rec = []
    for c in sorted(set(y.tolist())):
        m = y == c
        rec.append(float((pred[m] == c).mean()))
    return float(np.mean(rec))


def group_folds(groups, k=5, seed=0):
    """Deterministic grouped folds: shuffle the distinct groups, deal them round-robin."""
    gs = sorted(set(groups))
    rng = random.Random(seed)
    rng.shuffle(gs)
    fold_of = {g: i % k for i, g in enumerate(gs)}
    return np.array([fold_of[g] for g in groups])


def _model():
    return LogisticRegression(C=C_FIXED, penalty="l2", max_iter=2000, solver="lbfgs")


def oof_scores(X, y, groups, k=5, seed=0, multi=False):
    """Out-of-fold scores: decision function (binary) or class predictions + probabilities (multi)."""
    y = np.asarray(y)
    folds = group_folds(groups, k, seed)
    n = X.shape[0]
    if multi:
        pred = np.empty(n, dtype=object)
    else:
        score = np.zeros(n)
    for f in range(k):
        te, tr = np.where(folds == f)[0], np.where(folds != f)[0]
        if len(set(y[tr].tolist())) < 2:
            continue
        m = _model().fit(X[tr], y[tr])
        if multi:
            pred[te] = m.predict(X[te])
        else:
            # within-fold rank percentile: folds have different intercepts, and pooling raw scores across folds
            # creates a spurious AUC even for a constant feature
            score[te] = rankdata(m.decision_function(X[te])) / len(te)
    return (pred if multi else score)


def _cluster_boot(metric, y, s, groups, B=BOOT, seed=1):
    groups = np.asarray(groups)
    idx_by = {}
    for i, g in enumerate(groups):
        idx_by.setdefault(g, []).append(i)
    keys = list(idx_by)
    arrs = [np.array(idx_by[g]) for g in keys]
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(B):
        pick = rng.integers(0, len(keys), len(keys))
        idx = np.concatenate([arrs[j] for j in pick])
        yy = y[idx]
        if len(set(yy.tolist())) < 2:
            continue
        vals.append(metric(yy, s[idx]))
    return float(np.percentile(vals, 97.5)) if vals else 1.0


def binary_probe(X, y, groups, seed=0, boot=BOOT):
    """Returns dict(auc, ub, perm_auc). y: 0/1 array; X: sparse/dense matrix."""
    y = np.asarray(y)
    s = oof_scores(X, y, groups, seed=seed)
    a = auc_max(y, s)
    ub = _cluster_boot(auc_max, y, s, groups, boot, seed + 1)
    rng = np.random.default_rng(seed + 2)
    # permutation sanity: shuffle labels between GROUPS (a group keeps its own label vector, so twins stay together);
    # mean of 5 permutations (one permutation has SD ~0.02 at n ~ 1,000)
    gl = {}
    for g, yy in zip(groups, y):
        gl.setdefault(g, []).append(yy)
    keys = list(gl)
    perms = []
    for t in range(5):
        pm = rng.permutation(len(keys))
        mp = {keys[i]: keys[pm[i]] for i in range(len(keys))}
        yp = np.array([gl[mp[g]][zlib.crc32(str(g).encode()) % len(gl[mp[g]])] for g in groups])
        # RAW AUC (not max): max(AUC, 1 - AUC) of noise sits at ~0.53 for ~1,000 rows and ~60 sparse features, so the
        # "0.50 +- 0.03" sanity check is made on the unflipped AUC (mean of 5 permutations)
        perms.append(roc_auc_score(yp, oof_scores(X, yp, groups, seed=seed + 3 + t)) if len(set(yp.tolist())) > 1 else 0.5)
    perm_auc = float(np.mean(perms))
    return {"auc": float(a), "ub": ub, "perm_auc": float(perm_auc), "n": int(len(y))}


def kway_probe(X, y, groups, seed=0, boot=BOOT):
    y = np.asarray(y)
    pred = oof_scores(X, y, groups, seed=seed, multi=True)
    ba = balanced_accuracy(y, pred)
    ub = _cluster_boot(lambda yy, pp: balanced_accuracy(yy, pp), y, pred, groups, boot, seed + 1)
    return {"bal_acc": float(ba), "ub": ub, "k": len(set(y.tolist())), "n": int(len(y))}


def power_check(X, y, groups, seed=0):
    """Plant a one-feature leak (a column equal to the label) and require AUC >= 0.80."""
    y = np.asarray(y)
    leak = sparse.csr_matrix(y.reshape(-1, 1).astype(float))
    Xl = sparse.hstack([sparse.csr_matrix(X), leak]).tocsr()
    s = oof_scores(Xl, y, groups, seed=seed)
    return float(auc_max(y, s))


def dict_matrix(feature_dicts):
    v = DictVectorizer(sparse=True)
    return v.fit_transform(feature_dicts), v


def tfidf_fit_predict(train_texts, y_train, test_texts, multi=False):
    vec = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=2, max_features=60000, sublinear_tf=True)
    Xtr = vec.fit_transform(train_texts)
    m = _model().fit(Xtr, y_train)
    Xte = vec.transform(test_texts)
    return (m.predict(Xte) if multi else m.decision_function(Xte))


class ProbeHarness:
    """The seam gates.py calls. Replace with L-0's harness object exposing the same methods."""
    binary = staticmethod(binary_probe)
    kway = staticmethod(kway_probe)
    power = staticmethod(power_check)
    tfidf = staticmethod(tfidf_fit_predict)
