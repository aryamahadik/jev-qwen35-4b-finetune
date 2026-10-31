"""Side-test generation by SEARCH over the reference semantics (T66 section 2.1, K2 strength rules).

For a side X the suite must PASS on the X-only module and on the reference merge and FAIL on the base and on the other side's module. Candidates are single
assertions (value, difference, list item, table lookup) whose expected value is the reference merge's own behaviour; a candidate qualifies when the
reference semantics of the four modules say so. The suite is the smallest set of qualifying candidates (<= 3) that fails on every module it must fail on.
Nothing is executed here: the check is on the structure's reference semantics; the executor then witnesses the RENDERED tests (3 identical runs).
"""
from . import prog as P

X_POOL = (-5, -1, 0, 1, 2, 3, 5, 8, 13, 21, 40, 80, 150)
N_POOL = (0, 1, 2, 3, 4, 5, 6)


class Cand(object):
    def __init__(self, kind, fn, args, expect, extra=None):
        self.kind, self.fn, self.args, self.expect, self.extra = kind, fn, tuple(args), expect, extra or {}

    def key(self):
        return (self.kind, self.fn, self.args, repr(self.expect), repr(self.extra))

    def passes(self, mod):
        if self.kind == "value":
            return P.observe(mod, self.fn, self.args) == ("ok", self.expect)
        if self.kind == "diff":
            (a0,), (a1,) = self.args[0], self.args[1]
            o0, o1 = P.observe(mod, self.fn, (a0,)), P.observe(mod, self.fn, (a1,))
            return o0[0] == "ok" and o1[0] == "ok" and isinstance(o0[1], int) and o1[1] - o0[1] == self.expect
        if self.kind == "item":
            o = P.observe(mod, self.fn, self.args)
            idx = self.extra["idx"]
            return o[0] == "ok" and len(o[1]) > idx and o[1][idx] == self.expect
        raise ValueError(self.kind)

    def text(self, fnames=None):
        fn = (fnames or {}).get(self.fn, self.fn)
        if self.kind == "value":
            a = ", ".join(repr(x) for x in self.args)
            return "assert %s(%s) == %r" % (fn, a, self.expect)
        if self.kind == "diff":
            (a0,), (a1,) = self.args[0], self.args[1]
            return "assert %s(%r) - %s(%r) == %d" % (fn, a1, fn, a0, self.expect)
        return "assert %s(%r)[%d] == %r" % (fn, self.args[0], self.extra["idx"], self.expect)


def candidates(models, fns, rng):
    """Candidate assertions whose expected value is the REFERENCE MERGE's behaviour ('AB')."""
    ab = models["AB"]
    out = []
    for fn in fns:
        b = P._find(ab, fn)
        if b is None:
            continue
        if b["t"] == "pipe" and b.get("bias"):
            for x in X_POOL[3:9]:
                for bb in (0, 2, 5):
                    o = P.observe(ab, fn, (x, bb))
                    if o[0] == "ok" and isinstance(o[1], int):
                        out.append(Cand("value", fn, (x, bb), o[1]))
        elif b["t"] in ("pipe", "wrap"):
            for x in X_POOL:
                o = P.observe(ab, fn, (x,))
                if o[0] == "ok" and isinstance(o[1], int):
                    out.append(Cand("value", fn, (x,), o[1]))
            for x0 in X_POOL:
                for x1 in X_POOL:
                    if x1 > x0:
                        o0, o1 = P.observe(ab, fn, (x0,)), P.observe(ab, fn, (x1,))
                        if o0[0] == "ok" and o1[0] == "ok":
                            out.append(Cand("diff", fn, ((x0,), (x1,)), o1[1] - o0[1]))
        elif b["t"] == "table":
            for k, v in b["rows"]:
                out.append(Cand("value", fn, (k,), v))
        elif b["t"] == "build":
            for n in N_POOL:
                o = P.observe(ab, fn, (n,))
                if o[0] == "ok":
                    for idx in range(len(o[1])):
                        out.append(Cand("item", fn, (n,), o[1][idx], {"idx": idx}))
    rng.shuffle(out)
    seen, uniq = set(), []
    for c in out:
        if c.key() not in seen:
            seen.add(c.key())
            uniq.append(c)
    return uniq


def pick(models, want_pass, want_fail, fns, rng, max_n=3):
    """-> list of Cand or None. Every candidate passes on `want_pass` modules; together they fail on every `want_fail` module."""
    good = [c for c in candidates(models, fns, rng) if all(c.passes(models[m]) for m in want_pass)]
    need = set(want_fail)
    chosen = []
    for _ in range(max_n):
        best, cover = None, set()
        for c in good:
            cv = {m for m in need if not c.passes(models[m])}
            if len(cv) > len(cover):
                best, cover = c, cv
        if best is None:
            break
        chosen.append(best)
        need -= cover
        good = [c for c in good if c is not best]
        if not need:
            return chosen
    return None


def suite_text(stem, cands, fnames=None, tag="x"):
    names = sorted({(fnames or {}).get(c.fn, c.fn) for c in cands})
    lines = ["from %s import %s" % (stem, ", ".join(names)), ""]
    for i, c in enumerate(cands):
        lines += ["def test_%s_%d():" % (tag, i + 1), "    " + c.text(fnames)]
        if i + 1 < len(cands):
            lines.append("")
    return "\n".join(lines) + "\n"
