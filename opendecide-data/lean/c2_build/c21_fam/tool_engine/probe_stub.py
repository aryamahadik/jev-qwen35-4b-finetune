"""TEST-ONLY stand-in for the L-0 probe harness (G5). It is NOT the harness: no bootstrap bound, no permutation check.
It lets unit tests exercise the probe wiring (features, groups, labels) and catch gross leaks on small samples."""
import warnings

import numpy as np

warnings.filterwarnings("ignore")
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from sklearn.model_selection import GroupShuffleSplit


def _vec(X):
    if X and isinstance(X[0], dict):
        return DictVectorizer(sparse=True)
    return TfidfVectorizer(ngram_range=(1, 2), min_df=3)


class StubHarness:
    def __init__(self, repeats=3, seed=0):
        self.repeats, self.seed = repeats, seed

    def _run(self, X, y, groups, score):
        y = np.asarray(y)
        vals = []
        gss = GroupShuffleSplit(n_splits=self.repeats, test_size=0.2, random_state=self.seed)
        for tr, te in gss.split(np.zeros(len(y)), y, groups):
            if len(set(y[tr])) < 2 or len(set(y[te])) < 2:
                continue
            v = _vec(X)
            Xtr = v.fit_transform([X[i] for i in tr])
            Xte = v.transform([X[i] for i in te])
            clf = LogisticRegression(max_iter=300, C=1.0).fit(Xtr, y[tr])
            vals.append(score(clf, Xte, y[te]))
        return float(np.mean(vals)) if vals else 0.5

    def binary(self, X, y, groups):
        def sc(clf, Xte, yte):
            a = roc_auc_score(yte, clf.predict_proba(Xte)[:, 1])
            return max(a, 1 - a)
        a = self._run(X, y, groups, sc)
        return {"auc": a, "upper": a + 0.03, "valid": True}

    def kway(self, X, y, groups, k):
        def sc(clf, Xte, yte):
            return balanced_accuracy_score(yte, clf.predict(Xte))
        a = self._run(X, y, groups, sc)
        return {"bacc": a, "upper": a + 0.03, "valid": True}
