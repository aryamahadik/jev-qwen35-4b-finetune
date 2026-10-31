"""Repair r1.1 (QC round 1 fail: G6/G7/G8 label cue from the asked outcome's role).

Per-card balance kept by the samplers (G0 section 8: the F1 yes-rate marginals and the role-rate rule are "reached by
rejection inside the samplers"; v4 8 G7 "fix by matched twins first"). Nothing here edits a label: rows are only
chosen (which outcome X a free-side Q3 question asks about) or rejected and redrawn.

Q3 matching. On a Q3 row the asked outcome X is either the determined final outcome ("forced": affirmative or
double-negated rows answered yes, singly negated rows answered no) or an outcome the final never takes ("free"). In
r1.0 the forced side followed the final-outcome distribution (mostly the default) while the free side was spread over
the other outcomes, so X's role predicted the answer. Now, per card and per polarity class (A = aff/dneg, N = neg),
the free side picks X to match the forced side's X distribution (a matched twin in distribution: every forced
"X = default" row is answered by a free "X = default" row), and row structure features (operative notice count,
depth, rule count) are kept equally distributed between yes and no rows by rejection.
"""
from __future__ import annotations

from collections import Counter, defaultdict


def pclass(pol):
    return "N" if pol == "neg" else "A"


def is_forced(pol, a):
    """True iff the row's X must be the determined final outcome."""
    return (pclass(pol) == "A" and a == 1) or (pclass(pol) == "N" and a == 0)


class Q3Balance:
    LAMBDA = 6.0          # pseudo-rows of the draw-level final distribution in the forced-side target
    FEAT_DELTA = 0.10     # max share gap of one feature value between yes and no rows (per card)
    FEAT_MIN = 4          # other-answer rows needed before the feature check applies

    def __init__(self, card):
        self.card = card
        self.forced = {"A": Counter(), "N": Counter()}
        self.free = {"A": Counter(), "N": Counter()}
        self.nf = Counter()
        self.nfree = Counter()
        self.prior = Counter()
        self.feat = {0: defaultdict(Counter), 1: defaultdict(Counter)}
        self.na = Counter()
        self.yb = Counter()
        self.polc = {0: Counter(), 1: Counter()}
        self.xbad = Counter()
        # r2 pass B: the same matching inside each depth bin (pass A: with depth spread by the depth quota, the forced
        # side's X followed the structure's depth while the free side's did not, so X role x polarity x depth
        # predicted the answer, G6 (d) yes/no 0.532 vs chance 0.503)
        self.forced_d = defaultdict(Counter)
        self.free_d = defaultdict(Counter)
        self.prior_d = defaultdict(Counter)

    # ---- draw-level evidence on the card's final outcomes
    def see_final(self, X, dbin=None):
        if X is not None:
            self.prior[X] += 1
            if dbin is not None:
                self.prior_d[dbin][X] += 1

    @staticmethod
    def dbin(d):
        return min(int(d), 4)

    def target_d(self, pc, b, X):
        pr = self.prior_d[b]
        tp = sum(pr.values())
        p0 = (pr[X] / tp) if tp >= 5 else self.target(pc, X)
        f = self.forced_d[(pc, b)]
        nf = sum(f.values())
        return (f[X] + self.LAMBDA * p0) / (nf + self.LAMBDA)

    def free_deficit_d(self, pc, b, X):
        fr = self.free_d[(pc, b)]
        return self.target_d(pc, b, X) * (sum(fr.values()) + 1) - fr[X]

    def forced_excess_d(self, pc, b, X):
        fr = self.free_d[(pc, b)]
        nfr = sum(fr.values())
        if nfr < 3:
            return 0.0
        f = self.forced_d[(pc, b)]
        return (f[X] + 1) / (sum(f.values()) + 1) - fr[X] / nfr

    def target(self, pc, X):
        tp = sum(self.prior.values())
        p0 = (self.prior[X] / tp) if tp else 1.0 / max(1, len(self.card["outcomes"]))
        return (self.forced[pc][X] + self.LAMBDA * p0) / (self.nf[pc] + self.LAMBDA)

    def free_deficit(self, pc, X):
        return self.target(pc, X) * (self.nfree[pc] + 1) - self.free[pc][X]

    def forced_excess(self, pc, X):
        """How far X on the forced side runs ahead of what the free side has been able to match (rows)."""
        if self.nfree[pc] < 3:
            return 0.0
        share_f = (self.forced[pc][X] + 1) / (self.nf[pc] + 1)
        share_o = self.free[pc][X] / self.nfree[pc]
        return share_f - share_o

    # ---- structure features
    @staticmethod
    def feats(S, d):
        return {"n_amend": len(S.notices), "depth": min(int(d), 5), "n_rules": min(len(S.rules), 9) // 2}

    def feat_bad(self, a, fs):
        o = 1 - a
        if self.na[o] < self.FEAT_MIN:
            return None
        for f, v in fs.items():
            sa = (self.feat[a][f][v] + 1) / (self.na[a] + 1)
            so = (self.feat[o][f][v] + 0.5) / (self.na[o] + 1)
            if sa - so > self.FEAT_DELTA:
                return f
        return None

    # ---- polarity plan per answer (aff / neg / dneg)
    POL_W = {"aff": 0.58, "neg": 0.32, "dneg": 0.10}

    def pol_weights(self):
        """Card-adaptive weights (same for yes and no rows): yes = bad share = 0.5 + (p - 0.5)(1 - 2 P(neg)) with p =
        P(X bad) on the card (mostly the default's valence, since the matched X follows the final outcomes), so cards
        with p far from 0.5 ask more singly negated questions (at most 47%)."""
        n = self.xbad[0] + self.xbad[1]
        if n < 8:
            return self.POL_W
        p = self.xbad[1] / n
        wn = min(0.47, max(0.25, 0.5 - 0.02 / max(abs(p - 0.5), 0.01)))
        return {"aff": 0.9 - wn, "neg": wn, "dneg": 0.10}

    def plan_pol(self, a, rng):
        n = sum(self.polc[a].values())
        w = self.pol_weights()
        return max(w, key=lambda p: w[p] * (n + 1) - self.polc[a][p] + 0.6 * rng.random())

    # ---- yes = bad share (G0 8: 50 +/- 5 of yes/no rows)
    def yb_share_after(self, yb):
        n = self.yb[0] + self.yb[1] + 1
        return (self.yb[1] + int(yb)) / n

    # ---- accounting of an emitted row
    def account(self, X, pol, a, S, d, yb):
        pc = pclass(pol)
        b = self.dbin(d)
        if is_forced(pol, a):
            self.forced[pc][X] += 1
            self.nf[pc] += 1
            self.forced_d[(pc, b)][X] += 1
        else:
            self.free[pc][X] += 1
            self.nfree[pc] += 1
            self.free_d[(pc, b)][X] += 1
        self.na[a] += 1
        self.polc[a][pol] += 1
        self.xbad[int(self.card["valence"][X] == "bad")] += 1
        for f, v in self.feats(S, d).items():
            self.feat[a][f][v] += 1
        self.yb[int(bool(yb))] += 1


SPECIAL = ("default", "escalate", "fallback", "M", "cbd", "none")


class RoleBalance:
    """Per-card role-rate bookkeeping for choice rows (G0 8 role-rate rule: gold rate of a visible role on the rows
    that show it = m/k +/- 2 pp). cnt[role] = rows whose gold carries the role; exp[role] = sum over rows of m/k."""
    SLACK_HI = 0.75
    SLACK_LO = 1.0

    DEPTH_DELTA = 0.10   # r2: 0.15 -> 0.10 (G6 (d) Q1: depth 1 still predicted default gold, 155 rows vs 87)
    EXEMPT = ("M",)   # missing-field gold has depth 1 by definition (G0 1); balancing it removed M gold from Q2
    DEPTH_MIN = 6

    def __init__(self):
        self.cnt = Counter()
        self.exp = Counter()
        self.n = 0
        self.feat = defaultdict(lambda: defaultdict(Counter))   # feature -> gold role -> value counts

    @staticmethod
    def feats(d, n_rules):
        return {"depth": min(int(d), 4), "n_rules": min(int(n_rules), 9) // 2}

    def depth_bad(self, role, d, n_rules):
        """G6(d) lists depth and rule count as metadata: on choice rows they must not tell which role is gold. Per
        card, a row is rejected when its depth bucket or rule-count bucket is over-represented among this gold
        role's rows versus the other gold roles' rows (default-gold rows were mostly depth 1 with few rules)."""
        if role.split("|")[0] in self.EXEMPT:
            return None
        # r2: 0.10 on Q1 roles; Q2 keys (role|basis kind, 10 classes) keep the r1.1 0.15 (yield on long Q2 cards)
        delta = 0.15 if "|" in role else self.DEPTH_DELTA
        for f, b in self.feats(d, n_rules).items():
            byr = self.feat[f]
            mine = byr[role]
            n_m = sum(mine.values())
            n_o = sum(sum(c.values()) for r, c in byr.items() if r != role and r.split("|")[0] not in self.EXEMPT)
            if n_o < self.DEPTH_MIN:
                continue
            c_o = sum(c[b] for r, c in byr.items() if r != role and r.split("|")[0] not in self.EXEMPT)
            if (mine[b] + 1) / (n_m + 1) - (c_o + 0.5) / (n_o + 1) > delta:
                return f
        return None

    def over(self, role, m_over_k):
        if role not in SPECIAL:
            return False
        return self.cnt[role] + 1 > self.exp[role] + m_over_k + self.SLACK_HI

    def starving(self, gold_role, shown):
        """A special role shown on this row that is under its expected count, while the drawn gold is another role."""
        for ro, mk in shown.items():
            if ro in SPECIAL and ro != gold_role and self.cnt[ro] < self.exp[ro] + mk - self.SLACK_LO:
                return ro
        return None

    def account(self, gold_role, shown, depth=None, n_rules=None, key=None):
        self.n += 1
        self.cnt[gold_role] += 1
        if depth is not None:
            for f, b in self.feats(depth, n_rules or 0).items():
                self.feat[f][key or gold_role][b] += 1
        for ro, mk in shown.items():
            self.exp[ro] += mk
