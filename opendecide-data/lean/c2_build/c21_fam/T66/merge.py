"""T66 MERGE head: conflict kinds CF-1..CF-7, candidate resolutions RK1..RK8, side tests, witnesses and SOLVER A.

Gold (G0-lite 2.1): YES iff EVERY test of BOTH shown suites (SIDE_TEST_A, SIDE_TEST_B) passes on the resolved file in all 3 identical sandbox runs. The label
is derivable from the row: the tests shown are exactly the tests executed. The spec EXPECTATION is recorded where the generator knows one (RK5 / RK6 YES;
RK1 / RK2 / RK7 / RK8 NO; RK3 / RK4 none: the conflict kind decides); an unexpected result is dropped and counted.

Strength rules (K2), checked on the executor's witnesses of the four base modules: A-tests fail on the base and on the B-only module and pass on the A-only
module and on the reference merge; B-tests symmetrical. Python only until the L-0 image record is appended (LanguagePending otherwise).
DEVIATION FLAGGED (README): CF-7 is realised as "A deletes a block, B edits the line right after it" (both suites can then pass on a merge); a block that B
edits INSIDE is not realisable because the two suites would contradict each other.
"""
from . import merge3 as M3, prog as P, tests_gen as TG
from LP_COMMON import sandbox_iface as S

CF_IDS = ("CF-1", "CF-2", "CF-3", "CF-4", "CF-5", "CF-6", "CF-7")
RK_IDS = ("RK1", "RK2", "RK3", "RK4", "RK5", "RK6", "RK7", "RK8")
YES_RK, NO_RK = ("RK5", "RK6"), ("RK1", "RK2", "RK3", "RK4", "RK7", "RK8")
EXPECT = {"RK1": "NO", "RK2": "NO", "RK5": "YES", "RK6": "YES", "RK7": "NO", "RK8": "NO"}


class Reject(Exception):
    pass


class Pool(object):
    """Identifier source for one module (seeded namespace); every name is distinct."""

    def __init__(self, names, rng):
        self.names, self.rng, self.k = names, rng, 0

    def _u(self, slot):
        self.k += 1
        return self.names.unique(slot, "id%d" % self.k)

    def fn(self):
        return self._u("ns.mcp_tool")

    def var(self):
        return self._u("ns.variable")

    def const(self):
        return self._u("ns.envvar")

    def word(self):
        return self._u("ns.noun.entity")

    def stem(self):
        return self._u("ns.noun.module")


def _quiet(pool, rng, n=3):
    st = [P.stage("scale", k=rng.randint(2, 5)), P.stage("offset", c=rng.randint(1, 9)), P.stage("floor", lo=rng.randint(0, 3))][:n]
    return P.pipe(pool.fn(), pool.var(), pool.var(), st)


def _ints(rng):
    return rng.randint(2, 7), rng.randint(1, 20)


def build_cf(kind, pool, rng):
    """-> dict(base, A, B, AB, fns_a, fns_b, flags). All four modules are STRUCTURES (prog.py)."""
    flags = {"far": None}
    if kind in ("CF-1", "CF-2", "CF-7"):
        T, X = pool.fn(), pool.var()
        k, c = _ints(rng)
        cap = rng.randint(200, 900)
        if kind == "CF-1":
            base_t = P.pipe(T, X, pool.var(), [P.stage("scale", k=k), P.stage("offset", c=c), P.stage("cap", cap=cap)])
            return _assemble(base_t, T, rng, pool, edits_a=[(T, 0, {"k": k + rng.randint(1, 4)})], edits_b=[(T, 1, {"c": c + rng.randint(1, 9)})], flags=flags)
        if kind == "CF-2":
            base_t = P.pipe(T, X, pool.var(), [P.stage("affine", k=k, c=c), P.stage("cap", cap=cap)])
            return _assemble(base_t, T, rng, pool, edits_a=[(T, 0, {"k": k + rng.randint(1, 4)})], edits_b=[(T, 0, {"c": c + rng.randint(1, 9)})], flags=flags)
        base_t = P.pipe(T, X, pool.var(), [P.stage("scale", k=k), P.stage("cap", cap=rng.randint(20, 60)), P.stage("offset", c=c)])
        return _assemble(base_t, T, rng, pool, delete_a=(T, 1), edits_b=[(T, 2, {"c": c + rng.randint(1, 9)})], flags=flags)
    if kind == "CF-3":
        T, W = pool.fn(), pool.fn()
        k, c = _ints(rng)
        base = P.module(P.pipe(T, pool.var(), pool.var(), [P.stage("scale", k=k), P.stage("offset", c=c)]), _quiet(pool, rng), P.wrap(W, pool.var(), T, rng.randint(1, 9)))
        newname, W2 = pool.fn(), pool.fn()
        A = P.rename_fn(base, T, newname)
        B = P.add_block(base, P.wrap(W2, pool.var(), T, rng.randint(10, 19)))
        AB = P.add_block(A, P.wrap(W2, B["blocks"][-1]["x"], newname, B["blocks"][-1]["add"]))
        flags["far"] = None
        return dict(base=base, A=A, B=B, AB=AB, fns_a=[newname], fns_b=[W2], flags=flags, renamed={T: newname})
    if kind == "CF-4":
        T, W, W2 = pool.fn(), pool.fn(), pool.fn()
        bias = pool.var()
        k, c = _ints(rng)
        base = P.module(P.pipe(T, pool.var(), pool.var(), [P.stage("scale", k=k), P.stage("offset", c=c)]), _quiet(pool, rng), P.wrap(W, pool.var(), T, rng.randint(1, 9)))
        A = P.set_wrap(P.add_bias(base, T, bias), W, extra=[0])
        wx = pool.var()
        B = P.add_block(base, P.wrap(W2, wx, T, rng.randint(10, 19)))
        AB = P.add_block(A, P.wrap(W2, wx, T, B["blocks"][-1]["add"], extra=[0]))
        flags["far"] = "high"
        return dict(base=base, A=A, B=B, AB=AB, fns_a=[T, W], fns_b=[W2], flags=flags)
    if kind == "CF-5":
        F, TAB, KEY = pool.fn(), pool.const(), pool.var()
        rows = [(pool.word(), rng.randint(1, 9)), (pool.word(), rng.randint(10, 19))]
        base = P.module(P.table(TAB, F, KEY, rows), _quiet(pool, rng))
        ka, kb = pool.word(), pool.word()
        va, vb = rng.randint(20, 59), rng.randint(60, 99)
        A = P.add_row(base, F, ka, va)
        B = P.add_row(base, F, kb, vb)
        AB = P.add_row(P.add_row(base, F, ka, va), F, kb, vb)
        return dict(base=base, A=A, B=B, AB=AB, fns_a=[F], fns_b=[F], flags=flags)
    if kind == "CF-6":
        F, N = pool.fn(), pool.var()
        toks = [pool.word() for _ in range(3)]
        base = P.module(P.build(F, N, pool.var(), pool.var(), [P.stage("append", tok=t) for t in toks] + [P.stage("loop", k=rng.randint(2, 5))]), _quiet(pool, rng))
        A = P.swap_stages(base, F, 0, 1)
        newtok = pool.word()
        B = P.set_param(base, F, 2, tok=newtok)
        AB = P.set_param(A, F, 2, tok=newtok)
        return dict(base=base, A=A, B=B, AB=AB, fns_a=[F], fns_b=[F], flags=flags)
    raise Reject("unknown kind %s" % kind)


def _assemble(base_t, T, rng, pool, edits_a=(), edits_b=(), delete_a=None, flags=None):
    """Base = target pipeline + a quiet pipeline + a wrapper; ours / theirs / reference merge by edits (indices refer to the BASE stage list)."""
    base = P.module(base_t, _quiet(pool, rng), P.wrap(pool.fn(), pool.var(), T, rng.randint(1, 9)))
    A, B, AB = base, base, base
    for fn, idx, p in edits_a:
        A = P.set_param(A, fn, idx, **p)
        AB = P.set_param(AB, fn, idx, **p)
    for fn, idx, p in edits_b:
        B = P.set_param(B, fn, idx, **p)
        AB = P.set_param(AB, fn, idx, **p)
    if delete_a:
        A = P.delete_stage(A, *delete_a)
        AB = P.delete_stage(AB, *delete_a)
    return dict(base=base, A=A, B=B, AB=AB, fns_a=[T], fns_b=[T], flags=flags or {})


def tests_for(models, c, rng):
    """Side tests by search; None when no qualifying suite exists (Reject)."""
    ta = TG.pick(models, ("A", "AB"), ("base", "B"), c["fns_a"], rng)
    tb = TG.pick(models, ("B", "AB"), ("base", "A"), c["fns_b"], rng)
    if ta is None or tb is None:
        raise Reject("no strength-qualifying tests")
    return ta, tb


def conflict_of(c):
    base, a, b, ab = (P.lines(c[k]) for k in ("base", "A", "B", "AB"))
    segs = M3.merge3(base, a, b)
    cs = M3.conflicts(segs)
    if len(cs) != 1:
        raise Reject("%d conflicts" % len(cs))
    pre = []
    suf = []
    seen = False
    for s in segs:
        if s[0] == "conflict":
            seen = True
        elif not seen:
            pre += s[1]
        else:
            suf += s[1]
    if ab[:len(pre)] != pre or (suf and ab[len(ab) - len(suf):] != suf) or len(ab) < len(pre) + len(suf):
        raise Reject("reference merge does not share the clean skeleton")
    region = ab[len(pre):len(ab) - len(suf)]
    return segs, pre, suf, region


def _break_semantic(models, rng):
    """A module that parses and runs but breaks one side: bump one numeric parameter of a stage (or a table value / token)."""
    import copy
    ab = copy.deepcopy(models["AB"])
    sites = []
    for bi, b in enumerate(ab["blocks"]):
        if b["t"] == "pipe":
            for si, st in enumerate(b["stages"]):
                for key in ("k", "c", "cap", "lo", "m", "s"):
                    if key in st:
                        sites.append((bi, "stage", si, key))
        elif b["t"] == "table":
            for ri in range(len(b["rows"])):
                sites.append((bi, "row", ri, None))
        elif b["t"] == "build":
            for si, st in enumerate(b["stages"]):
                if st["op"] == "append":
                    sites.append((bi, "tok", si, None))
                else:
                    sites.append((bi, "stage", si, "k"))
        elif b["t"] == "wrap":
            sites.append((bi, "wrapadd", 0, None))
    rng.shuffle(sites)
    return ab, sites


def apply_break(ab, site, delta):
    import copy
    m = copy.deepcopy(ab)
    bi, kind, i, key = site
    b = m["blocks"][bi]
    if kind == "stage":
        b["stages"][i][key] += delta
    elif kind == "row":
        k, v = b["rows"][i]
        b["rows"][i] = (k, v + delta)
    elif kind == "tok":
        b["stages"][i]["tok"] = b["stages"][i]["tok"] + "x"
    else:
        b["add"] += delta
    return m


def candidate(kind, c, models, segs, pre, suf, region, tests, rng):
    """-> (resolved_text, expectation|None, info)."""
    ours, theirs = segs[[s[0] for s in segs].index("conflict")][2], segs[[s[0] for s in segs].index("conflict")][3]
    if kind in ("RK1", "RK2", "RK3", "RK4", "RK5"):
        reg = {"RK1": ours, "RK2": theirs, "RK3": ours + theirs, "RK4": theirs + ours, "RK5": region}[kind]
        text = "\n".join(pre + reg + suf) + "\n"
        return text, EXPECT.get(kind), {}
    if kind == "RK6":
        ab = models["AB"]
        for bi, b in enumerate(ab["blocks"]):
            if b["t"] in ("pipe", "build"):
                import copy
                m = copy.deepcopy(ab)
                if b["t"] == "pipe":
                    m["blocks"][bi]["v"] = b["v"] + "x"
                else:
                    m["blocks"][bi]["out"] = b["out"] + "x"
                return P.render(m), "YES", {"rewrite": "rename_local"}
        raise Reject("no rewrite site")
    if kind == "RK7":
        ab, sites = _break_semantic(models, rng)
        for site in sites:
            for delta in (1, 2, 3):
                m = apply_break(ab, site, delta)
                # the break must be caught by the reference semantics of at least one suite (and NOT be the reference merge)
                fails = [(i, t) for i, t in enumerate(tests["a"] + tests["b"]) if not t.passes(m)]
                if fails and P.render(m) != P.render(ab):
                    first_fail = fails[0][0]
                    return P.render(m), "NO", {"break_site": list(site[:3]), "first_failing_test": first_fail}
        raise Reject("no semantic break found")
    if kind == "RK8":
        lines = P.lines(models["AB"])
        for i, ln in enumerate(lines):
            if ln.startswith("def ") and ln.endswith(":"):
                lines[i] = ln[:-1]
                return "\n".join(lines) + "\n", "NO", {"syntax": "missing_colon"}
        raise Reject("no def line")
    raise Reject(kind)


def render_files(stem, text_lines):
    return {stem + ".py": text_lines}
