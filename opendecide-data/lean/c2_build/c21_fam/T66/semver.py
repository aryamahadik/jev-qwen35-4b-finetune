"""T66 SEMVER head: old API, new API (SV-C1..SV-C12), shown caller snippets, witnesses, SOLVER A.

Gold (G0-lite 2.2, Opus T66-B4): BREAKING iff at least one SHOWN caller test fails on the new API in all 3 identical sandbox runs; SAFE iff all pass on all 3
runs; gold-sanity: every caller passes on the old API. The label is about THE SHOWN CALLERS (the question says so). A declared version bump (shown in 50% of
rows) is a decoy: agreement with the truth is 50% +- 5 pp (K6).

API model: {name, params: [(name, default|REQ)], k, shape: scalar|tuple|dict(+note), reject: {below, exc}|None, edge: {when, add}|None, exc_classes: [(name, base)],
alias: str|None, order: 'native'|'reordered'}. `render` writes the module, `ref_call` the reference semantics (argument binding, validation, formula, shape).
"""
import copy

from LP_COMMON import sandbox_iface as S

REQ = "__REQ__"
SV_IDS = tuple("SV-C%d" % i for i in range(1, 13))
BREAKING_KINDS = ("SV-C1", "SV-C2", "SV-C3", "SV-C5", "SV-C6", "SV-C7", "SV-C8", "SV-C9", "SV-C10")
SAFE_KINDS = ("SV-C4", "SV-C11", "SV-C12")


class Reject(Exception):
    pass


def api(name, p0, p1, p2, k, shape="scalar", reject=None, d1=3):
    return {"name": name, "params": [(p0, REQ), (p1, d1), (p2, 0)], "k": k, "shape": shape, "reject": reject, "edge": None, "exc_classes": [], "alias": None,
            "formula": "native", "note": None}


def _shape_expr(model, v):
    s = model["shape"]
    if s == "scalar":
        return v
    if s == "tuple":
        return "(%s, True)" % v
    if s == "dict":
        return '{"value": %s, "ok": True}' % v
    if s == "dict_note":
        return '{"value": %s, "ok": True, "note": "n"}' % v
    raise ValueError(s)


def render(model):
    ps = model["params"]
    sig = ", ".join(n if d == REQ else "%s=%d" % (n, d) for n, d in ps)
    lines = []
    for cname, base in model["exc_classes"]:
        lines += ["class %s(%s):" % (cname, base), "    pass", "", ""]
    lines.append("def %s(%s):" % (model["name"], sig))
    a = ps[0][0]
    names = [n for n, _d in ps]
    # the formula always names the semantic roles a (value), b (rate), c (extra): after a reorder / rename the roles keep their NAMES
    role = model.get("roles", {"a": ps[0][0], "b": ps[1][0], "c": ps[2][0]})
    ra, rb, rc = role["a"], role["b"], role["c"]
    if model["reject"]:
        lines += ["    if %s < %d:" % (ra, model["reject"]["below"]), '    ' + '    raise %s("rejected")' % model["reject"]["exc"]]
    if model["edge"]:
        lines += ["    if %s == %d:" % (ra, model["edge"]["when"]), "        return %s" % _shape_expr(model, "%d" % model["edge"]["value"])]
    extra = "".join(" + %s" % n for n, _d in ps[3:])
    if model["formula"] == "native":
        lines.append("    v = %s * %d + %s + %s%s" % (ra, model["k"], rb, rc, extra))
    else:
        lines.append("    v = %s + %s + %s * %d%s" % (rb, rc, ra, model["k"], extra))
    lines.append("    return %s" % _shape_expr(model, "v"))
    if model.get("alias"):
        lines += ["", "", "%s = %s" % (model["alias"], model["name"])]
    return "\n".join(lines) + "\n"


def ref_call(model, args, kwargs, fn=None):
    """Reference semantics of calling `fn` (default the model's name or its alias) with python binding rules. -> ('ok', value) | ('exc', ClassName)."""
    fn = fn or model["name"]
    if fn not in (model["name"], model.get("alias")):
        return ("exc", "NameError")
    ps = model["params"]
    names = [n for n, _d in ps]
    if len(args) > len(ps):
        return ("exc", "TypeError")
    bound = dict(zip(names, args))
    for k, v in kwargs.items():
        if k not in names or k in bound:
            return ("exc", "TypeError")
        bound[k] = v
    for n, d in ps:
        if n not in bound:
            if d == REQ:
                return ("exc", "TypeError")
            bound[n] = d
    role = model.get("roles", {"a": ps[0][0], "b": ps[1][0], "c": ps[2][0]})
    a, b, c = bound[role["a"]], bound[role["b"]], bound[role["c"]]
    if model["reject"] and a < model["reject"]["below"]:
        return ("exc", model["reject"]["exc"])
    if model["edge"] and a == model["edge"]["when"]:
        return ("ok", _shape_val(model, model["edge"]["value"]))
    v = a * model["k"] + b + c + sum(bound[n] for n, _d in ps[3:])
    return ("ok", _shape_val(model, v))


def _shape_val(model, v):
    s = model["shape"]
    if s == "scalar":
        return v
    if s == "tuple":
        return [v, True]
    if s == "dict":
        return {"value": v, "ok": True}
    return {"value": v, "ok": True, "note": "n"}


# ---- callers ------------------------------------------------------------------------------------------------------------------------------
CALLERS = ("U1", "U2", "U3", "U4", "U5", "U6")


def caller_calls(old, uid):
    """(args, kwargs) for a caller id against the OLD API's parameter names."""
    pn = [n for n, _d in old["params"]]
    return {"U1": ((2, 5), {}), "U2": ((2,), {pn[1]: 5}), "U3": ((4,), {}), "U4": ((0, 1), {}), "U5": ((-3, 2), {}), "U6": ((-9, 1), {})}[uid]


def caller_text(old, uid, fn, tag):
    """One test function written against the OLD API. Shape-aware: scalar -> compare, tuple -> unpack, dict -> key access. U6 expects the old exception."""
    args, kwargs = caller_calls(old, uid)
    call = "%s(%s)" % (fn, ", ".join([repr(x) for x in args] + ["%s=%r" % (k, v) for k, v in kwargs.items()]))
    if uid == "U6":
        return ["def test_%s():" % tag, "    try:", "        %s" % call, "    except %s:" % old["reject"]["exc"], "        return", "    assert False"]
    o = ref_call(old, args, kwargs)
    if o[0] != "ok":
        raise Reject("caller %s does not run on the old API" % uid)
    v = o[1]
    shape = old["shape"]
    if shape == "scalar":
        return ["def test_%s():" % tag, "    assert %s == %d" % (call, v)]
    if shape == "tuple":
        return ["def test_%s():" % tag, "    val, ok = %s" % call, "    assert val == %d and ok" % v[0]]
    return ["def test_%s():" % tag, '    assert %s["value"] == %d' % (call, v["value"])]


def callers_file(stem, old, uids, imports):
    lines = ["from %s import %s" % (stem, ", ".join(imports)), ""]
    for i, uid in enumerate(uids):
        lines += caller_text(old, uid, old["name"], "c%d" % (i + 1))
        if i + 1 < len(uids):
            lines.append("")
    return "\n".join(lines) + "\n"


# ---- new APIs by kind --------------------------------------------------------------------------------------------------------------------
def new_api(old, kind, pool, rng, variant="break"):
    """-> new model for SV-C kind. variant 'break' | 'safe' selects the twin used by matched pairs (the same kind, one token apart)."""
    n = copy.deepcopy(old)
    pn = [x for x, _d in old["params"]]
    if kind == "SV-C1":
        newn = pool.var()
        idx = 1 if variant == "break" else 2                                  # callers use keywords on b, never on c
        n["params"][idx] = (newn, old["params"][idx][1])
        n["roles"] = {"a": pn[0], "b": pn[1] if idx != 1 else newn, "c": pn[2] if idx != 2 else newn}
    elif kind == "SV-C2":
        if variant == "break":
            n["params"] = [old["params"][0], old["params"][2], old["params"][1]]              # c now second: positional b lands in c
        else:
            n["params"] = [old["params"][0], old["params"][1], old["params"][2]]
            n["params"].append((pool.var(), 0))                              # appended optional parameter: order of the old ones is kept
        n["roles"] = {"a": pn[0], "b": pn[1], "c": pn[2]}
    elif kind == "SV-C3":
        newp = pool.var()
        if variant == "break":                                                   # a new REQUIRED parameter placed second; its role is bookkeeping only
            n["params"] = [old["params"][0], (newp, REQ), old["params"][1], old["params"][2]]
        else:                                                                    # the same parameter with a default, appended: SAFE
            n["params"] = old["params"] + [(newp, 0)]
        n["roles"] = {"a": pn[0], "b": pn[1], "c": pn[2]}
    elif kind == "SV-C4":
        n["params"] = old["params"] + [(pool.var(), 0)]
        n["roles"] = {"a": pn[0], "b": pn[1], "c": pn[2]}
    elif kind == "SV-C5":                                                        # the default of b changes; SAFE iff no shown caller omits b
        n["params"][1] = (pn[1], old["params"][1][1] + rng.randint(1, 3))
    elif kind == "SV-C6":
        if variant == "break":
            n["shape"] = {"scalar": "tuple", "tuple": "dict", "dict": "scalar", "dict_note": "scalar"}[old["shape"]]
        else:
            if old["shape"] != "dict":
                raise Reject("SV-C6 safe twin needs a dict old shape")
            n["shape"] = "dict_note"
    elif kind == "SV-C7":
        if variant == "break":
            n["reject"] = dict(old["reject"], exc="KeyError")
        else:
            cname = pool.cls()
            n["exc_classes"] = [(cname, old["reject"]["exc"])]
            n["reject"] = dict(old["reject"], exc=cname)
    elif kind == "SV-C8":
        n["edge"] = {"when": 0 if variant == "break" else 77, "value": rng.randint(900, 999)}
    elif kind == "SV-C9":
        n["name"] = pool.fn()
        if variant != "break":
            n["alias"] = old["name"]
    elif kind == "SV-C10":
        n["reject"] = dict(old["reject"], below=(0 if variant == "break" else -8))
    elif kind == "SV-C11":
        n["formula"] = "reordered"
    elif kind == "SV-C12":
        n["alias"] = pool.fn()
    else:
        raise Reject(kind)
    return n


def simple_exc(model):
    return model["reject"]["exc"] if model["reject"] else None


def make_old(pool, rng, shape):
    p = [pool.var() for _ in range(3)]
    return api(pool.fn(), p[0], p[1], p[2], rng.randint(2, 7), shape, reject={"below": -5, "exc": "ValueError"}, d1=rng.randint(2, 6))


# ---- witnesses + label -----------------------------------------------------------------------------------------------------------------------
def witness(executor, rid, stem, old, new, uids, imports_old, imports_new, test_name):
    """Caller suite on the OLD api (gold-sanity) and on the NEW api (3 identical runs each)."""
    tx_old = callers_file(stem, old, uids, imports_old)
    out = {}
    for tag, model, imports in (("old", old, imports_old), ("new", new, imports_new)):
        files = {stem + ".py": render(model), test_name: tx_old}
        res = executor.run([S.tests_request("%s:%s" % (rid, tag), files, test_name)])[0]
        out[tag] = {"ok": S.witness_ok(res), "states": S.test_states(res), "passed": S.all_pass(S.test_states(res)), "runs": res.get("runs"), "image": res.get("image")}
    return out, tx_old


def label_from_witness(w):
    """SOLVER A for SEMVER: BREAKING iff the callers all pass on the old API (sanity) and at least one fails on the new API, deterministically; SAFE iff all pass on
    both. Anything else (non-deterministic, old API fails) is not a label (the caller drops the row)."""
    if not (w["old"]["ok"] and w["new"]["ok"] and w["old"]["passed"]):
        return None
    return "SAFE" if w["new"]["passed"] else "BREAKING"
