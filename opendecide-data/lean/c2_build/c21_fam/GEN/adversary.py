"""Online adversarial filter for 4-option forms (AFLite-style, CPU only, scikit-learn LR + gradient boosting; no neural model, no network).

Why (skeptic finding, 18 Oct): with near-miss distractors the CORRECT option is structurally special (the others sit at fixed offsets from it), so the
option-only probe G-S1 reached 79 percent on TM-T1, 63 percent on TB-B3, 70 percent on TM-T2 against a bar of 28 percent. The pilot would have used the
family's ONE fix iteration on a defect that is visible before any row exists. The builder now screens every 4-option candidate item against a pair of
detectors that learn, from the candidates seen so far, which option features give the answer away, and rejects an item whose correct option a detector
picks with confidence. A detector is trained on (a) a burn-in of raw candidates (never emitted) and (b) every item accepted so far, so the pressure does
not fade once the accepted data looks balanced.

Features are `heuristics.option_features`, the SAME function the gate G-S1 uses. Nothing here sets or changes a label or an option text: it only
accepts or rejects a candidate item (drop-only, like every other filter in the builder). Deterministic given the builder seed.
"""
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

import heuristics as H

WARM_CANDIDATES = 500       # raw candidates per form used to train the detectors before the first row is emitted
RETRAIN_EVERY = 25          # accepted items between refits
CONF = 0.28                 # reject when a detector's normalised score for the correct option is the largest AND above this (chance is 0.25)


class Adversary:
    def __init__(self, k=4):
        self.k = k
        self.X, self.y = [], []
        self.lr = self.gbt = self.scaler = None
        self.since_fit = 0
        self.stats = {"checked": 0, "rejected": 0, "fits": 0}

    # -- data
    def add(self, options, stem, correct_idx):
        F = H.option_features(options, stem)
        for i, f in enumerate(F):
            self.X.append(f)
            self.y.append(int(i == correct_idx))
        self.since_fit += 1

    def _fit(self):
        X = np.array(self.X, dtype=float)
        y = np.array(self.y)
        if len(set(y.tolist())) < 2 or len(y) < 4 * 40:
            return
        self.scaler = StandardScaler().fit(X)
        Z = self.scaler.transform(X)
        self.lr = LogisticRegression(penalty="l2", C=0.5, max_iter=400).fit(Z, y)
        self.gbt = GradientBoostingClassifier(n_estimators=80, max_depth=4, learning_rate=0.1, random_state=0).fit(X, y)
        self.since_fit = 0
        self.stats["fits"] += 1

    def maybe_fit(self, force=False):
        if force or self.since_fit >= RETRAIN_EVERY or (self.lr is None and len(self.y) >= 4 * 40):
            self._fit()

    # -- decision
    def scores(self, options, stem):
        """-> list of two normalised score vectors (LR, GBT) over the options, or [] before the first fit."""
        if self.lr is None:
            return []
        F = np.array(H.option_features(options, stem), dtype=float)
        out = []
        for p in (self.lr.predict_proba(self.scaler.transform(F))[:, 1], self.gbt.predict_proba(F)[:, 1]):
            p = np.clip(p, 1e-6, None)
            out.append(p / p.sum())
        return out

    def rank_of(self, options, stem, correct_idx):
        """Rank (0 = best scored) of the correct option under the mean of the two detectors' normalised scores; None before the first fit.
        The builder accepts an item only when this rank equals a target drawn uniformly (a balanced counter), so the detectors' own score is
        uninformative about the answer AND its inverse is uninformative too (rejecting only the items a detector gets right would invert the
        leak: the correct option would become the one the detector scores LOW)."""
        qs = self.scores(options, stem)
        if not qs:
            return None
        q = sum(qs) / len(qs)
        c = q[correct_idx]
        return int(sum(1 for j in range(len(q)) if j != correct_idx and (q[j] > c + 1e-12 or (abs(q[j] - c) <= 1e-12 and j < correct_idx))))

    def ok(self, options, stem, correct_idx, target_rank):
        self.stats["checked"] += 1
        r = self.rank_of(options, stem, correct_idx)
        if r is None or r == target_rank:
            return True
        self.stats["rejected"] += 1
        return False
