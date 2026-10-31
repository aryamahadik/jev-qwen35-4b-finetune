"""CPU probe harness for the L-C gates, written to the G5 ruling (one protocol for every family):

  * grouped split: no group (base module / task) is ever in both a training and a held-out fold;
  * L2 logistic regression, FIXED regularisation (C), never tuned on held-out data;
  * binary AUC is reported as max(AUC, 1 - AUC); the upper bound is the 97.5th percentile of 2,000 cluster-bootstrap
    resamples over groups (the stricter reading of "95% upper bound");
  * k-way probes use balanced accuracy (mean per-class recall) against 1/k + 3 pp and 1/k + 6 pp; OUT4 / best-of-4
    "argmax per row" probes report plain accuracy of the per-row argmax (chance is exactly 1/k with shuffled options);
  * every run includes a label-permutation sanity check (binary: AUC within 0.50 +- 0.03; k-way: mean balanced accuracy
    within 1/k +- 3 pp) and an injected-leak power check (a planted one-column leak must reach AUC >= 0.80 / balanced
    accuracy >= 0.80); otherwise the run is INVALID (status "INVALID", neither pass nor fail) and must be repeated
    (a repeat is not a fix iteration). `binary_probe` and `kway_probe` both carry the two checks (Opus ruling, T59/T60/T63
    Q7a follow-up: the checks belong to the shared harness, not to a family);
  * CATEGORICAL inputs (wording id, card id, layout ...) are RAW 0/1 indicators and are never standardised: scaling a
    1-in-77 indicator to about 8.7 swamps a planted leak. `indicator_matrix` builds them and returns the `raw_cols` mask that
    `oof_scores` / `binary_probe` / `kway_probe` / `option_argmax_probe` take (`raw_cols="auto"` treats every non-constant
    0/1-only column as an indicator); the default `raw_cols=None` keeps the old behaviour (standardise every column);
  * GBT probes are advisory (optional, never a verdict).
L-0 owns the shared harness; this file implements the same protocol with the same interface (features, labels, groups)
so it can be swapped for L-0's without touching the families. Nothing here reads rows from disk.
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

C_FIXED = 1.0
BOOT = 2000
SEED = 20261018
PERM_TOL = 0.03       # G5: permutation mean within chance +- 3 pp
LEAK_MIN = 0.80       # G5: a planted one-column label leak must reach 0.80
N_PERM = 6            # shuffles averaged in the permutation check
LEAK_SD = 0.15        # planted leak = label (class index) + N(0, 0.15), the binary_probe form


def raw_mask(raw_cols, X):
    """Boolean mask over the columns of X that stay RAW (never standardised): None -> none (legacy: standardise all),
    "auto" -> every non-constant column whose values are all 0/1, a bool mask or a list of column indices -> those columns."""
    d = np.asarray(X).shape[-1]
    if raw_cols is None:
        return None
    if isinstance(raw_cols, str):
        if raw_cols != "auto":
            raise ValueError("raw_cols must be None, 'auto', a bool mask or column indices")
        Z = np.asarray(X, dtype=float).reshape(-1, d)
        m = np.array([np.isin(Z[:, j], (0.0, 1.0)).all() and Z[:, j].min() != Z[:, j].max() for j in range(d)], dtype=bool)
    else:
        a = np.asarray(raw_cols)
        if a.dtype == bool:
            if a.shape != (d,):
                raise ValueError("raw_cols mask must have one entry per column (%d)" % d)
            m = a.copy()
        else:
            m = np.zeros(d, dtype=bool)
            m[a.astype(int)] = True
    return m if m.any() else None


def _scaler(Xtr, raw=None):
    """transform(Z) -> standardised with the TRAIN mean / std, except that columns in `raw` pass through unchanged."""
    sc = StandardScaler().fit(Xtr)
    if raw is None:
        return sc.transform
    mean = np.where(raw, 0.0, sc.mean_)
    scale = np.where(raw, 1.0, sc.scale_)
    return lambda Z: (np.asarray(Z, dtype=float) - mean) / scale


def indicator_matrix(columns, X_num=None):
    """Raw 0/1 indicator encoding of categorical features. `columns` = {name: sequence of category values, one per row} (a dict or
    a list of (name, values) pairs); every category seen in a column gets one 0/1 column (sorted by str). Optional `X_num` (n, d)
    numeric block goes first. Returns (X, raw_cols, names): `raw_cols` is the bool mask (True on the indicators) to pass as
    `raw_cols=` so the indicators are NEVER standardised (a 1-in-77 indicator scaled to ~8.7 swamps a planted leak)."""
    items = list(columns.items()) if hasattr(columns, "items") else list(columns)
    n = len(items[0][1]) if items else (len(X_num) if X_num is not None else 0)
    blocks, names, raw = [], [], []
    if X_num is not None:
        Xn = np.asarray(X_num, dtype=float).reshape(n, -1)
        blocks.append(Xn)
        names += ["num%d" % j for j in range(Xn.shape[1])]
        raw += [False] * Xn.shape[1]
    for name, vals in items:
        if len(vals) != n:
            raise ValueError("column %r has %d values, expected %d" % (name, len(vals), n))
        cats = sorted({str(v) for v in vals})
        sv = [str(v) for v in vals]
        blocks.append(np.array([[1.0 if v == c else 0.0 for c in cats] for v in sv], dtype=float).reshape(n, len(cats)))
        names += ["%s=%s" % (name, c) for c in cats]
        raw += [True] * len(cats)
    X = np.hstack(blocks) if blocks else np.zeros((n, 0))
    return X, np.array(raw, dtype=bool), names


def group_folds(groups, k=5, seed=SEED):
    """fold index per sample; groups stay together; folds are balanced by group count."""
    uniq = sorted(set(groups), key=str)
    rng = np.random.RandomState(seed)
    rng.shuffle(uniq)
    fold_of = {g: i % k for i, g in enumerate(uniq)}
    return np.array([fold_of[g] for g in groups])


def auc_score(y, s):
    y = np.asarray(y)
    s = np.asarray(s, dtype=float)
    pos, neg = (y == 1), (y == 0)
    n1, n0 = pos.sum(), neg.sum()
    if n1 == 0 or n0 == 0:
        return 0.5
    order = np.argsort(s, kind="mergesort")
    ranks = np.empty(len(s), dtype=float)
    ss = s[order]
    i = 0
    r = np.arange(1, len(s) + 1, dtype=float)
    while i < len(ss):               # average ranks for ties
        j = i
        while j + 1 < len(ss) and ss[j + 1] == ss[i]:
            j += 1
        r[i:j + 1] = (i + 1 + j + 1) / 2.0
        i = j + 1
    ranks[order] = r
    return float((ranks[pos].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def sym_auc(y, s):
    a = auc_score(y, s)
    return max(a, 1.0 - a)


def oof_scores(X, y, groups, k=5, seed=SEED, C=C_FIXED, raw_cols=None):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    raw = raw_mask(raw_cols, X)
    folds = group_folds(groups, k, seed)
    out = np.zeros(len(y))
    for f in range(k):
        te, tr = folds == f, folds != f
        if te.sum() == 0 or len(set(y[tr])) < 2:
            out[te] = 0.5
            continue
        tf = _scaler(X[tr], raw)
        clf = LogisticRegression(C=C, max_iter=300).fit(tf(X[tr]), y[tr])
        out[te] = clf.decision_function(tf(X[te]))
    return out


def oof_text_scores(texts, y, groups, k=5, seed=SEED, C=C_FIXED, min_df=2, ngram=(1, 2)):
    y = np.asarray(y)
    folds = group_folds(groups, k, seed)
    out = np.zeros(len(y))
    texts = np.asarray(texts, dtype=object)
    for f in range(k):
        te, tr = folds == f, folds != f
        if te.sum() == 0 or len(set(y[tr])) < 2:
            out[te] = 0.5
            continue
        vec = TfidfVectorizer(token_pattern=r"[A-Za-z_][A-Za-z_0-9]*|\d+|[^\sA-Za-z_0-9]", ngram_range=ngram, min_df=min_df,
                              sublinear_tf=True)
        Xtr = vec.fit_transform(texts[tr])
        clf = LogisticRegression(C=C, max_iter=300).fit(Xtr, y[tr])
        out[te] = clf.decision_function(vec.transform(texts[te]))
    return out


def _cluster_index(groups):
    idx = {}
    for i, g in enumerate(groups):
        idx.setdefault(g, []).append(i)
    return [np.array(v) for _, v in sorted(idx.items(), key=lambda kv: str(kv[0]))]


def cluster_bootstrap(metric, y, s, groups, B=BOOT, seed=SEED, q=97.5):
    y, s = np.asarray(y), np.asarray(s)
    cl = _cluster_index(groups)
    rng = np.random.RandomState(seed)
    vals = np.empty(B)
    for b in range(B):
        pick = rng.randint(0, len(cl), len(cl))
        ii = np.concatenate([cl[j] for j in pick])
        vals[b] = metric(y[ii], s[ii])
    return float(np.percentile(vals, q)), float(np.percentile(vals, 100 - q))


def binary_probe(X, y, groups, k=5, B=BOOT, seed=SEED, texts=False, leak_check=True, perm_check=True, perm_tol=PERM_TOL, raw_cols=None):
    """Held-out AUC (max(AUC, 1-AUC)), 97.5th-percentile bound, permutation and injected-leak sanity checks.
    `raw_cols` (feature matrices only): columns kept RAW, e.g. categorical 0/1 indicators (see `indicator_matrix`)."""
    y = np.asarray(y)
    raw = None if texts else raw_mask(raw_cols, X)
    scores = oof_text_scores(X, y, groups, k, seed) if texts else oof_scores(X, y, groups, k, seed, raw_cols=raw)
    a = sym_auc(y, scores)
    upper, _ = cluster_bootstrap(sym_auc, y, scores, groups, B, seed)
    res = {"auc": a, "upper": upper, "n": int(len(y)), "groups": len(set(groups)), "valid": True}
    if perm_check:
        # label-permutation sanity check: mean RAW AUC over 6 shuffles (the max(AUC, 1-AUC) form is biased upward on noise)
        raws = []
        for i in range(N_PERM):
            rng = np.random.RandomState(seed + 1 + 17 * i)
            yp = y.copy()
            rng.shuffle(yp)
            sp = oof_text_scores(X, yp, groups, k, seed) if texts else oof_scores(X, yp, groups, k, seed, raw_cols=raw)
            raws.append(auc_score(yp, sp))
        res["perm_auc"] = float(np.mean(raws))
        res["perm_ok"] = abs(res["perm_auc"] - 0.5) <= perm_tol            # G5: 0.50 +- 0.03
    if leak_check and not texts:
        rng = np.random.RandomState(seed + 2)
        Xl = np.hstack([np.asarray(X, dtype=float), (y + rng.normal(0, LEAK_SD, len(y))).reshape(-1, 1)])
        raw_l = None if raw is None else np.append(raw, False)
        res["leak_auc"] = sym_auc(y, oof_scores(Xl, y, groups, k, seed, raw_cols=raw_l))
        res["leak_ok"] = res["leak_auc"] >= LEAK_MIN
    if leak_check and texts:
        marker = np.array([("zzleak " * 40 if yy == 1 else "") + t for t, yy in zip(X, y)], dtype=object)
        res["leak_auc"] = sym_auc(y, oof_text_scores(marker, y, groups, k, seed))
        res["leak_ok"] = res["leak_auc"] >= LEAK_MIN
    res["valid"] = res.get("perm_ok", True) and res.get("leak_ok", True)
    return res


def passes_binary(res, auc_max=0.55, upper_max=0.60):
    return bool(res["valid"] and res["auc"] <= auc_max and res["upper"] <= upper_max)


def balanced_accuracy(y, pred):
    y, pred = np.asarray(y), np.asarray(pred)
    cls = sorted(set(y.tolist()))
    return float(np.mean([(pred[y == c] == c).mean() for c in cls]))


def _kway_pred(X, y, groups, k, seed, raw):
    """Out-of-fold class predictions of the grouped-CV logistic regression (fixed C)."""
    folds = group_folds(groups, k, seed)
    pred = np.zeros(len(y), dtype=y.dtype)
    for f in range(k):
        te, tr = folds == f, folds != f
        if te.sum() == 0:
            continue
        if len(set(y[tr])) < 2:
            pred[te] = y[tr][0] if tr.sum() else y[0]
            continue
        tf = _scaler(X[tr], raw)
        clf = LogisticRegression(C=C_FIXED, max_iter=300).fit(tf(X[tr]), y[tr])
        pred[te] = clf.predict(tf(X[te]))
    return pred


def kway_probe(X, y, groups, k_classes=None, k=5, B=BOOT, seed=SEED, raw_cols=None, perm_check=True, leak_check=True,
               perm_tol=PERM_TOL, leak_min=LEAK_MIN, n_perm=N_PERM):
    """Multi-class: balanced accuracy of grouped-CV logistic regression + cluster-bootstrap 97.5th percentile, with the two G5 sanity
    checks (same protocol as `binary_probe`, k-way analog):
      * permutation: mean balanced accuracy over `n_perm` (6) label shuffles must be within 1/k +- 3 pp;
      * leak power: a planted ONE-column label leak (class index + N(0, 0.15)) must reach balanced accuracy >= 0.80.
    A run that fails either check is INVALID: status "INVALID", valid False, pass False (neither pass nor fail); the numbers are in
    perm_bal_acc / leak_bal_acc. A valid run has status "PASS" or "FAIL" (bars 1/k + 3 pp on bal_acc, 1/k + 6 pp on the bound).
    `raw_cols`: columns kept RAW (categorical 0/1 indicators, see `indicator_matrix`); None = standardise every column (old behaviour).
    perm_check / leak_check=False skip a check (tests only; the run then lists what it ran in `checks_run`)."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    raw = raw_mask(raw_cols, X)
    pred = _kway_pred(X, y, groups, k, seed, raw)
    acc = balanced_accuracy(y, pred)
    kc = k_classes or len(set(y.tolist()))
    upper, _ = cluster_bootstrap(lambda yy, pp: balanced_accuracy(yy, pp), y, pred, groups, B, seed)
    chance = 1.0 / kc
    res = {"bal_acc": acc, "upper": upper, "chance": chance, "k": kc, "n": int(len(y)),
           "bar": chance + 0.03, "bar_upper": chance + 0.06, "groups": len(set(groups)), "checks_run": []}
    if perm_check:
        res["checks_run"].append("perm")
        perms = []
        for i in range(n_perm):
            yp = y.copy()
            np.random.RandomState(seed + 1 + 17 * i).shuffle(yp)
            perms.append(balanced_accuracy(yp, _kway_pred(X, yp, groups, k, seed, raw)))
        res["perm_bal_acc"] = float(np.mean(perms))
        res["perm_ok"] = abs(res["perm_bal_acc"] - chance) <= perm_tol            # G5: 1/k +- 3 pp
    if leak_check:
        res["checks_run"].append("leak")
        _, yi = np.unique(y, return_inverse=True)
        leak = yi + np.random.RandomState(seed + 2).normal(0, LEAK_SD, len(y))
        Xl = np.hstack([X, leak.reshape(-1, 1)])
        raw_l = None if raw is None else np.append(raw, False)
        res["leak_bal_acc"] = balanced_accuracy(y, _kway_pred(Xl, y, groups, k, seed, raw_l))
        res["leak_ok"] = res["leak_bal_acc"] >= leak_min
    res["valid"] = bool(res.get("perm_ok", True) and res.get("leak_ok", True))
    ok = bool(acc <= chance + 0.03 and upper <= chance + 0.06)
    res["pass"] = bool(res["valid"] and ok)
    res["status"] = ("PASS" if ok else "FAIL") if res["valid"] else "INVALID"
    return res


def option_argmax_probe(opt_X, gold, groups, k=5, B=BOOT, seed=SEED, raw_cols=None):
    """Per-option features (n_rows, n_opts, d) -> train 'is gold' logistic, choose argmax per row on held-out rows.
    Returns accuracy and a cluster-bootstrap 97.5th percentile (chance = 1/n_opts)."""
    opt_X = np.asarray(opt_X, dtype=float)
    n, m, d = opt_X.shape
    gold = np.asarray(gold)
    raw = raw_mask(raw_cols, opt_X)
    folds = group_folds(groups, k, seed)
    hit = np.zeros(n)
    for f in range(k):
        te, tr = folds == f, folds != f
        if te.sum() == 0 or tr.sum() == 0:
            continue
        Xtr = opt_X[tr].reshape(-1, d)
        ytr = (np.arange(m)[None, :] == gold[tr][:, None]).reshape(-1).astype(int)
        tf = _scaler(Xtr, raw)
        clf = LogisticRegression(C=C_FIXED, max_iter=300).fit(tf(Xtr), ytr)
        s = clf.decision_function(tf(opt_X[te].reshape(-1, d))).reshape(-1, m)
        hit[te] = (s.argmax(axis=1) == gold[te]).astype(float)
    acc = float(hit.mean())
    cl = _cluster_index(groups)
    rng = np.random.RandomState(seed)
    vals = np.empty(B)
    for b in range(B):
        pick = rng.randint(0, len(cl), len(cl))
        ii = np.concatenate([cl[j] for j in pick])
        vals[b] = hit[ii].mean()
    upper = float(np.percentile(vals, 97.5))
    chance = 1.0 / m
    return {"acc": acc, "upper": upper, "chance": chance, "n": int(n), "bar": chance + 0.03, "bar_upper": chance + 0.06,
            "pass": bool(acc <= chance + 0.03 and upper <= chance + 0.06)}


def option_argmax_power_check(n_rows=400, n_opts=4, seed=SEED):
    """Planted-leak power check for the argmax probe: a feature that equals the label must be recovered."""
    rng = np.random.RandomState(seed)
    gold = rng.randint(0, n_opts, n_rows)
    X = rng.normal(size=(n_rows, n_opts, 3))
    X[np.arange(n_rows), gold, 0] += 2.0
    groups = [i // 2 for i in range(n_rows)]
    res = option_argmax_probe(X, gold, groups, B=200)
    return res["acc"] >= 0.80
