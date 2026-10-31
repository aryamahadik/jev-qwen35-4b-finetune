"""CPU probe harness for the GEN shortcut gates (and reusable by VOICE). L-0 is to publish ONE shared harness (Opus ruling G5);
this module follows that ruling's rules so it can be swapped for the shared one without changing any gate bar:

  - grouped split (no group in both train and held-out), 5 group folds
  - L2 logistic regression (fixed C, never tuned on held-out); GBT on numeric-structure features also reported
    (for GEN both probe models count: a gate passes only if both pass)
  - binary: AUC reported as max(AUC, 1 - AUC); upper bound = 97.5th percentile of 2,000 cluster-bootstrap resamples over groups
  - k-way: balanced accuracy (mean per-class recall) against 1/k + 3 pp (bar) and 1/k + 6 pp (upper bound)
  - every run includes a label-permutation sanity check (AUC 0.50 +- 0.03) and an injected-leak power check (planted
    one-feature leak must reach AUC >= 0.80); a run that fails either is INVALID and is repeated (not a fix iteration)
  - confirm rule (GEN / VOICE only): a probe over its point bar is re-run once on a fresh sample of twice the size; the re-run decides.
No file is written. No model other than scikit-learn LR / gradient boosting is used. No network.
"""
import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold

AUC_POINT, AUC_UB = 0.55, 0.60
KWAY_POINT_PP, KWAY_UB_PP = 0.03, 0.06
N_BOOT = 2000
N_FOLDS = 5
PERM_TOL = 0.03
LEAK_MIN = 0.80


def bars(kind, k=None):
    if kind == "binary":
        return AUC_POINT, AUC_UB
    return 1.0 / k + KWAY_POINT_PP, 1.0 / k + KWAY_UB_PP


def _fit_predict(model, Xtr_text, Xtr_num, ytr, Xte_text, Xte_num, classes):
    """Returns probability matrix (n_test, n_classes in `classes` order)."""
    if model == "lr":
        w = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, lowercase=True)
        c = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=3, sublinear_tf=True, lowercase=True, max_features=60000)
        mats_tr, mats_te = [], []
        try:
            mats_tr.append(w.fit_transform(Xtr_text))
            mats_te.append(w.transform(Xte_text))
            mats_tr.append(c.fit_transform(Xtr_text))
            mats_te.append(c.transform(Xte_text))
        except ValueError:
            pass
        if Xtr_num is not None and Xtr_num.shape[1]:
            mu, sd = Xtr_num.mean(0), Xtr_num.std(0) + 1e-9
            mats_tr.append(csr_matrix((Xtr_num - mu) / sd))
            mats_te.append(csr_matrix((Xte_num - mu) / sd))
        if not mats_tr:
            return np.full((len(Xte_text), len(classes)), 1.0 / len(classes))
        clf = LogisticRegression(penalty="l2", C=1.0, max_iter=2000)
        clf.fit(hstack(mats_tr).tocsr(), ytr)
        P = clf.predict_proba(hstack(mats_te).tocsr())
    else:
        clf = GradientBoostingClassifier(n_estimators=60, max_depth=3, learning_rate=0.1, random_state=0)
        clf.fit(Xtr_num, ytr)
        P = clf.predict_proba(Xte_num)
    out = np.zeros((P.shape[0], len(classes)))
    for j, cl in enumerate(clf.classes_):
        out[:, classes.index(cl)] = P[:, j]
    return out


def oof_predictions(model, texts, X_num, y, groups, classes, n_folds=N_FOLDS):
    y = np.asarray(y)
    groups = np.asarray(groups)
    n_groups = len(set(groups.tolist()))
    folds = min(n_folds, n_groups)
    P = np.zeros((len(y), len(classes)))
    if folds < 2:
        return np.full_like(P, 1.0 / len(classes))
    for tr, te in GroupKFold(n_splits=folds).split(np.zeros(len(y)), y, groups):
        if len(set(y[tr].tolist())) < 2:
            P[te] = 1.0 / len(classes)
            continue
        P[te] = _fit_predict(model, [texts[i] for i in tr], None if X_num is None else X_num[tr], y[tr],
                             [texts[i] for i in te], None if X_num is None else X_num[te], classes)
    return P


def auc_folded(y, score):
    y = np.asarray(y)
    if len(set(y.tolist())) < 2:
        return 0.5
    a = roc_auc_score(y, score)
    return max(a, 1 - a)


def balanced_acc(y, pred, classes):
    y = np.asarray(y)
    pred = np.asarray(pred)
    r = []
    for c in classes:
        m = y == c
        if m.sum():
            r.append(float((pred[m] == c).mean()))
    return float(np.mean(r)) if r else 0.0


def _boot_ub(stat_fn, y, scores_or_pred, groups, n_boot, seed):
    rng = np.random.default_rng(seed)
    groups = np.asarray(groups)
    ug = sorted(set(groups.tolist()))
    idx_by_g = {g: np.where(groups == g)[0] for g in ug}
    vals = []
    for _ in range(n_boot):
        pick = rng.integers(0, len(ug), len(ug))
        idx = np.concatenate([idx_by_g[ug[i]] for i in pick])
        vals.append(stat_fn(y[idx], scores_or_pred[idx]))
    return float(np.percentile(vals, 97.5))


def evaluate(model, texts, X_num, y, groups, kind, classes, k=None, n_boot=N_BOOT, seed=0):
    """One probe model. Returns {'point','ub','pass'} (binary: classes = [neg, pos])."""
    y = np.asarray(y)
    P = oof_predictions(model, texts, X_num, y, groups, classes)
    point_bar, ub_bar = bars(kind, k)
    if kind == "binary":
        score = P[:, 1]
        point = auc_folded(y, score)
        ub = _boot_ub(lambda yy, ss: auc_folded(yy, ss), y, score, groups, n_boot, seed)
    else:
        pred = np.array(classes)[P.argmax(1)]
        point = balanced_acc(y, pred, classes)
        ub = _boot_ub(lambda yy, pp: balanced_acc(yy, pp, classes), y, pred, groups, n_boot, seed)
    return {"point": point, "ub": ub, "pass": bool(point <= point_bar and ub <= ub_bar), "point_bar": point_bar, "ub_bar": ub_bar}


def sanity(texts, X_num, y, groups, classes, kind, seed=0, perm_tol=PERM_TOL):
    """Permutation sanity (signed AUC near 0.50, or accuracy near chance) and injected-leak power check."""
    rng = np.random.default_rng(seed + 17)
    y = np.asarray(y)
    perm = []
    for _ in range(3):
        yp = rng.permutation(y)
        P = oof_predictions("lr", texts, X_num, yp, groups, classes)
        if kind == "binary":
            perm.append(roc_auc_score(yp, P[:, 1]) if len(set(yp.tolist())) > 1 else 0.5)
        else:
            perm.append(balanced_acc(yp, np.array(classes)[P.argmax(1)], classes))
    chance = 0.5 if kind == "binary" else 1.0 / len(classes)
    perm_mean = float(np.mean(perm))
    perm_ok = abs(perm_mean - chance) <= perm_tol
    # planted leak: one extra token (and numeric column) equal to the label
    leak_texts = [t + " zzleak%s" % str(l) for t, l in zip(texts, y)]
    P = oof_predictions("lr", leak_texts, X_num, y, groups, classes)
    if kind == "binary":
        leak = auc_folded(y, P[:, 1])
    else:
        leak = balanced_acc(y, np.array(classes)[P.argmax(1)], classes)
    return {"perm_mean": perm_mean, "perm_ok": bool(perm_ok), "leak": float(leak), "leak_ok": bool(leak >= LEAK_MIN), "valid": bool(perm_ok and leak >= LEAK_MIN)}


def run_probe(name, texts, X_num, y, groups, kind, classes, k=None, models=("lr", "gbt"), n_boot=N_BOOT, seed=0, check_sanity=True, perm_tol=PERM_TOL):
    """Both models must pass (GEN rule). Returns a result dict; 'status' is PASS, FAIL or INVALID (sanity failed: repeat)."""
    res = {"probe": name, "kind": kind, "k": k, "n": int(len(y)), "n_groups": len(set(np.asarray(groups).tolist())), "models": {}}
    for m in models:
        if m == "gbt" and (X_num is None or X_num.shape[1] == 0):
            continue
        res["models"][m] = evaluate(m, texts, X_num, y, groups, kind, classes, k, n_boot, seed)
    san = sanity(texts, X_num, y, groups, classes, kind, seed, perm_tol) if check_sanity else {"valid": True}
    res["sanity"] = san
    res["passed"] = all(v["pass"] for v in res["models"].values())
    res["status"] = "INVALID" if not san["valid"] else ("PASS" if res["passed"] else "FAIL")
    return res


def confirm_rule(first, rerun_fn):
    """GEN / VOICE confirm rule: if `first` failed its POINT bar, call rerun_fn() once (fresh sample, twice the size, new seed)
    and let the re-run decide. A failure of the UPPER-BOUND bar alone with the point under the bar also fails (no re-run)."""
    if first["status"] != "FAIL":
        return first
    over_point = any(v["point"] > v["point_bar"] for v in first["models"].values())
    if not over_point:
        first["confirm"] = "not applicable (point bar met, upper bound exceeded): fails"
        return first
    second = rerun_fn()
    second["confirm"] = "re-run decided"
    second["first"] = {m: (v["point"], v["ub"]) for m, v in first["models"].items()}
    return second
