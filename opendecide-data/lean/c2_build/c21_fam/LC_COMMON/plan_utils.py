"""Deficit-driven category choice shared by the L-C planners: pick the category furthest below its target share."""


def pick_deficit(rng, counts, targets, allowed=None):
    total = sum(counts.values()) + 1
    best, bv = [], None
    for k, share in targets.items():
        if (allowed is not None and k not in allowed) or share <= 0:
            continue
        d = share * total - counts.get(k, 0)
        if bv is None or d > bv + 1e-9:
            best, bv = [k], d
        elif abs(d - bv) <= 1e-9:
            best.append(k)
    return rng.choice(best) if best else None


def pick_deficit2(rng, counts_a, counts_b, targets, allowed=None):
    ta, tb = sum(counts_a.values()) + 1, sum(counts_b.values()) + 1
    best, bv = [], None
    for k, share in targets.items():
        if (allowed is not None and k not in allowed) or share <= 0:
            continue
        d = (share * ta - counts_a.get(k, 0)) + (share * tb - counts_b.get(k, 0))
        if bv is None or d > bv + 1e-9:
            best, bv = [k], d
        elif abs(d - bv) <= 1e-9:
            best.append(k)
    return rng.choice(best) if best else None


class GapBalancer:
    """Keeps mean(feature | gold option) - mean(feature | distractor option) near zero for every tracked feature by refusing
    rows that would widen a gap beyond `tau` (matched sampling; no model involved). Never deadlocks: after `max_rejects`
    consecutive refusals a row is accepted and the override is counted (the gates then speak)."""

    def __init__(self, nfeat, tau=0.05, warmup=40, max_rejects=12):
        self.g, self.d = [0.0] * nfeat, [0.0] * nfeat
        self.ng = self.nd = 0
        self.tau, self.warmup, self.max_rejects = tau, warmup, max_rejects
        self.rejects = self.overrides = 0

    @staticmethod
    def _gaps(g, d, ng, nd):
        return [(g[i] / ng - d[i] / nd) if ng and nd else 0.0 for i in range(len(g))]

    def _apply(self, rows, sign=1):
        g, d, ng, nd = list(self.g), list(self.d), self.ng, self.nd
        for is_gold, f in rows:
            for i, x in enumerate(f):
                if is_gold:
                    g[i] += sign * x
                else:
                    d[i] += sign * x
            if is_gold:
                ng += sign
            else:
                nd += sign
        return g, d, ng, nd

    def ok(self, rows):
        if self.ng < self.warmup:
            return True
        before = self._gaps(self.g, self.d, self.ng, self.nd)
        after = self._gaps(*self._apply(rows, 1))
        if all(abs(a) <= self.tau or abs(a) <= abs(b) for a, b in zip(after, before)):
            self.rejects = 0
            return True
        self.rejects += 1
        if self.rejects > self.max_rejects:
            self.rejects = 0
            self.overrides += 1
            return True
        return False

    def add(self, rows, sign=1):
        self.g, self.d, self.ng, self.nd = self._apply(rows, sign)
