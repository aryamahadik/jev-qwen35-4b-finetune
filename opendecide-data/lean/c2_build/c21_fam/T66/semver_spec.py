"""T66 SEMVER: cell (kind, label, pair?) -> specs. The caller subset is chosen from the reference semantics so that a BREAKING new API trips at least one shown
caller and a SAFE one trips none; the LABEL comes from the executor witnesses (old API sanity + 3 identical runs on the new API)."""
import difflib

from LP_COMMON.ns import Names

from . import semver as SV


class Pool(object):
    def __init__(self, names):
        self.names, self.k = names, 0

    def _u(self, slot):
        self.k += 1
        return self.names.unique(slot, "id%d" % self.k)

    def fn(self):
        return self._u("ns.mcp_tool")

    def var(self):
        return self._u("ns.variable")

    def cls(self):
        return self._u("ns.noun.entity").capitalize() + "Error"

    def stem(self):
        return self._u("ns.noun.module")


def _observe(old_shape, res):
    """What the shown caller reads out of a result, written against the OLD return shape."""
    if res[0] != "ok":
        return res
    v = res[1]
    if old_shape == "scalar":
        return ("ok", v)
    if old_shape == "tuple":
        return ("ok", v[0]) if isinstance(v, (list, tuple)) and len(v) == 2 else ("bad", repr(type(v)))
    return ("ok", v["value"]) if isinstance(v, dict) and "value" in v else ("bad", repr(type(v)))


def tripping(old, new, uid):
    """Would the shown caller `uid` (written against the old API) fail on the new API? (reference semantics, not an execution)"""
    args, kwargs = SV.caller_calls(old, uid)
    o = SV.ref_call(old, args, kwargs)
    n = SV.ref_call(new, args, kwargs, fn=old["name"])
    if uid == "U6":
        if n == ("exc", old["reject"]["exc"]):
            return False
        return not (n[0] == "exc" and any(c == n[1] and b == old["reject"]["exc"] for c, b in new["exc_classes"]))
    return _observe(old["shape"], n) != _observe(old["shape"], o)


def diff_lines(a, b):
    sm = difflib.SequenceMatcher(None, a.split("\n"), b.split("\n"), autojunk=False)
    return sum(max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal")


def build_group(ctx, g, cell):
    """cell: {sv, variants: ['break'|'safe', ...], bump: bool} -> list of specs. A pair shares the old API and the shown callers."""
    rng = ctx.rng("semver", g["seed"])
    names = Names("T66", "%s/%s" % (ctx.seed, g["seed"]), deny_check=ctx.deny_check)
    pool = Pool(names)
    if cell["sv"] == "SV-C5" and len(cell["variants"]) > 1:
        raise SV.Reject("SV-C5 has no matched-pair twin (a default either is relied on or not)")
    shape = cell.get("shape") or rng.choice(("scalar", "tuple", "dict"))
    if cell["sv"] == "SV-C6" and "safe" in cell["variants"]:
        shape = "dict"
    old = SV.make_old(pool, rng, shape)
    news = [(v, SV.new_api(old, cell["sv"], pool, rng, v)) for v in cell["variants"]]
    uids = [u for u in SV.CALLERS]
    rng.shuffle(uids)
    chosen = None
    for k in rng.sample([2, 3, 4, 5], 4):
        sub = uids[:k]
        ok = True
        for v, new in news:
            trips = [u for u in sub if tripping(old, new, u)]
            if (v == "break") != bool(trips) and cell["sv"] not in ("SV-C4", "SV-C11", "SV-C12"):
                ok = False
        if ok:
            chosen = sub
            break
    if chosen is None:
        for k in (6, 5, 4):                                       # a larger caller set always contains a tripping caller for a BREAKING kind
            sub = uids[:k]
            if all((v == "break") == any(tripping(old, new, u) for u in sub) for v, new in news):
                chosen = sub
                break
    if chosen is None:
        raise SV.Reject("no caller subset separates the variants")
    chosen = [u for u in SV.CALLERS if u in chosen]
    stem = pool.stem()
    test_name = "test_%s_callers.py" % stem
    specs = []
    for j, (v, new) in enumerate(news):
        w, tx = SV.witness(ctx.executor, "%s:%s:%d" % (g["gid"], cell["sv"], j), stem, old, new, chosen, [old["name"]], [old["name"]], test_name)
        label = SV.label_from_witness(w)
        if label is None:
            raise SV.Reject("witness not usable (old API failed or non-deterministic)")
        expect = "BREAKING" if (v == "break" or cell["sv"] in ("SV-C4", "SV-C11", "SV-C12") and False) else "SAFE"
        ref_break = any(tripping(old, new, u) for u in chosen)
        if (label == "BREAKING") != ref_break:
            raise SV.Reject("executor and reference semantics disagree (%s vs %s)" % (label, ref_break))
        old_t, new_t = SV.render(old), SV.render(new)
        small = SV.diff_lines(old_t, new_t) if hasattr(SV, "diff_lines") else diff_lines(old_t, new_t)
        bump_shown = cell.get("bump", False)
        truth_major = label == "BREAKING"
        bump = None
        if bump_shown:
            agree = rng.random() < 0.5
            bump = ("major" if truth_major else rng.choice(("patch", "minor"))) if agree else (rng.choice(("patch", "minor")) if truth_major else "major")
        look = None
        n_diff = diff_lines(old_t, new_t)
        if (label == "BREAKING" and n_diff <= 2) or (label == "SAFE" and n_diff >= 4):
            look = "high"
        elif (label == "BREAKING" and n_diff >= 4) or (label == "SAFE" and n_diff <= 2):
            look = "low"
        mech = {"look": look, "bump": None if bump is None else ("low" if ((bump == "major") == truth_major) else "high")}
        specs.append({"head": "SEMVER", "sv": cell["sv"], "variant": v, "lang": "python", "stem": stem, "label": label, "old": old_t, "new": new_t, "callers": tx,
                      "callers_name": test_name, "uids": chosen, "bump": bump, "witness": w, "mech": mech, "diff_lines": n_diff, "api": old["name"],
                      "conflict_id": "%s:%s" % (g["gid"], cell["sv"])})
    return specs
