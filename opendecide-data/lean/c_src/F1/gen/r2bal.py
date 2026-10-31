"""Repair r2 (QC round 2 fail: G6 choice view (d), G10 depth / amendment / option-count / twin targets).

Generation-time steering only: rows are chosen, rejected and redrawn, never relabelled.

Q2 option classes (G6 (d) and the G0 8 role-rate rule). r1.1 balanced the gold rate of each outcome role and the
special-code share separately; their joint was far off (on the r1.1 candidates, (default, code) options were gold on
255 rows against 93 expected from their option share, (other, code) on 10 against 143), so a metadata model reading
"outcome role x basis kind" picked the gold option (G6 (d) Q2 15.7% vs chance 7.9%). Here each option class
c = (outcome role, basis kind) is kept at the role-rate rule's own balance: per card, gold count G[c] ~ sum over rows
of m_c / k. The filler options of a row are allotted to classes by the card's running deficit G - E plus the class's
draw-level gold prior, never by this row's gold (r1.1 pass 4: fillers that followed the row's gold were a cue), and a
row whose gold class is already over its exposure is redrawn.
"""
from __future__ import annotations

import math
from collections import Counter

CBD = "CBD"


class Q2ClassBalance:
    SLACK_HI = 0.75     # a gold class may run this far ahead of its exposure (rows) before the redraw starts
    # (pass B early rows: with 1.5 and a soft redraw the capacity-limited classes, mainly default gold through code D,
    # ran 2-3 rows ahead on every card and the Q2 role-rate cells summed that to +4 to +6 pp)
    PRIOR_A = 4.0       # pseudo-draws of a flat prior over the gold-capable classes

    def __init__(self, prior_src=None):
        self.prior_src = prior_src   # r2 pass B: the 10-19 and 20-60 option buckets share one draw-level prior
        self.G = Counter()      # emitted rows whose gold is in class c
        self.E = Counter()      # sum over emitted rows of m_c / k
        self.P = Counter()      # draw-level gold classes (before any rejection)
        self.np = 0
        self.n = 0

    def see(self, c):
        self.P[c] += 1
        self.np += 1

    def prior(self, c, capable):
        flat = (1.0 / len(capable)) if (capable and c in capable) else 0.0
        src = self.prior_src or self
        return (src.P[c] + self.PRIOR_A * flat) / (src.np + self.PRIOR_A)

    def allot(self, k, fixed_cnt: Counter, avail: dict, capable, rng):
        """Class counts m_c for a row of k options: m_c >= fixed_cnt[c], m_c <= fixed_cnt[c] + avail[c], sum k.
        Target m_c* = k (G[c] - E[c] + prior_c): after the row, exposure tracks gold. Independent of this row's
        gold (fixed_cnt holds the gold and the error-model pairs, which are always shown)."""
        classes = set(fixed_cnt) | set(avail)
        tgt = {c: k * (self.G[c] - self.E[c] + self.prior(c, capable)) for c in classes}
        m = {c: fixed_cnt.get(c, 0) for c in classes}
        left = k - sum(m.values())
        if left < 0:
            return None
        cap = {c: avail.get(c, 0) for c in classes}
        # greedy by largest remaining need (tgt - m), random tie-break; then the least over-exposed classes
        while left > 0:
            opts = [c for c in classes if cap[c] > 0]
            if not opts:
                return None
            c = max(opts, key=lambda x: (tgt[x] - m[x]) + 0.01 * rng.random())
            m[c] += 1
            cap[c] -= 1
            left -= 1
        return m

    def excess(self, c, m_over_k, extra=0.0):
        return self.G[c] + 1 + extra - (self.E[c] + m_over_k + self.SLACK_HI)

    def over(self, c, m_over_k, rng, extra=0.0):
        """Soft: a draw whose gold class is ahead of its exposure is redrawn with probability 0.4 + 0.3 x excess
        (capped at 1), so capacity-limited classes (few options of the class fit a row) slow the card down without
        stalling it; the class gold rate stays within about one to two rows of its exposure per card."""
        x = self.excess(c, m_over_k, extra)
        return x > 0 and rng.random() < min(1.0, 0.7 + 0.3 * x)

    def avg_share(self, c):
        """Mean exposure of class c per emitted row so far (the redraw test uses this, never the current row's own
        share: a test on the row's own m_c / k accepts a gold-c draw mostly when the row shows many c options, which
        made 'the gold is in the class that is large on this row' a cue; pass B Q2 G6 (d) 21.4% vs chance 7.4%)."""
        return self.E[c] / self.n if self.n else 0.0

    def hopeless(self, c):
        """Cheap pre-check before the expensive per-draw work: even a row showing many options of the class (share
        0.6) would leave the class far ahead of its exposure."""
        return self.excess(c, 0.6) > 1.5

    def account(self, gold_c, shown: dict):
        self.n += 1
        self.G[gold_c] += 1
        for c, mk in shown.items():
            self.E[c] += mk


class SoftQuota:
    """Deficit acceptor with a soft edge: a category over its target share (plus slack) is rejected with
    probability `p_rej` (so a card whose structures rarely reach a level never stalls)."""

    def __init__(self, targets: dict, slack=2.0, p_rej=0.85):
        self.t = dict(targets)
        self.c = Counter()
        self.n = 0
        self.slack = slack
        self.p_rej = p_rej

    def over(self, cat):
        if cat not in self.t:
            return False
        return self.c[cat] + 1 > self.t[cat] * (self.n + 1) + self.slack

    def ok(self, cat, rng):
        return not (self.over(cat) and rng.random() < self.p_rej)

    def need(self, rng, allowed=None):
        """The category furthest below its target share (random tie-break)."""
        cats = [c for c in self.t if allowed is None or c in allowed]
        return max(cats, key=lambda c: self.t[c] * (self.n + 1) - self.c[c] + 0.3 * rng.random())

    def add(self, cat):
        self.c[cat] += 1
        self.n += 1


# G0 8 depth shares of non-deep rows: 1 22%, 2 33%, 3 28%, 4 17%. Per card, by its construct-set ceiling (rows.dmax):
# cards whose constructs cannot reach depth 3 or 4 take the shallow share, the deep-capable cards the rest
# (weighted by the r1 planned rows this gives 21 / 34 / 27 / 17 over the family)
DEPTH_BY_DMAX = {2: {1: 0.45, 2: 0.55}, 3: {1: 0.27, 2: 0.40, 3: 0.33}, 4: {1: 0.16, 2: 0.29, 3: 0.32, 4: 0.23},
                 5: {1: 0.12, 2: 0.23, 3: 0.35, 4: 0.30}}
# r2 pass B: pass A rows reached about half of the per-card depth-4 targets (28 / 41 / 23 / 9% at depth 1-4 against the
# 15 / 25 / 34 / 26 plan above for the deep-capable cards); the deep-capable targets are raised so that the realized
# family shares land near G0 8's 22 / 33 / 28 / 17
# Q2 cards: their rows print 10-60 options, so they stay on small structures (length cap) and take a shallower share;
# the other deep-capable cards carry the rest (solved on the r2 planned rows: non-Q2 dmax >= 5 cards need
# 15 / 25 / 34 / 26, the dmax 5 row above)
DEPTH_Q2 = {2: {1: 0.45, 2: 0.55}, 3: {1: 0.40, 2: 0.45, 3: 0.15}, 4: {1: 0.35, 2: 0.48, 3: 0.17},
            5: {1: 0.35, 2: 0.48, 3: 0.17}}

# G0 8 amendment shares (operative notices printed): 0 35%, 1 30%, 2 20%, 3 15%. Notice-free cards give 0 on every
# row; the card plan (cardfix_r2) keeps their rows at about 33% of the family, so cards with notices take these
# shares (0.33 + 0.67 x 0.03 = 0.35 for 0; 0.67 x 0.45 = 0.30; 0.67 x 0.30 = 0.20; 0.67 x 0.22 = 0.15)
AMEND_NOTICE_CARD = {0: 0.03, 1: 0.45, 2: 0.30, 3: 0.22}
AMEND_S6 = {1: 0.46, 2: 0.31, 3: 0.23}
