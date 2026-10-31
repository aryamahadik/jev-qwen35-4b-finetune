"""Application-style module generator (shared by T42c, T57, T56g; seed spaces are disjoint per family tag).

gen_module(seed, lang, family, ...) -> IR module (+ meta). One call = one program for ONE target language.
The module is built from behaviour atoms (atoms.py), may have a class with state, a wrapper that composes two atoms
(an inter-procedural call), and 1 to 3 files. All identifiers come from Idents (namespace.py, TRAINING salt).
`prepare(mod, lang, ids)` lowers it for the target language (lower.py) and re-checks it.
"""
import hashlib
import random

from . import ir as I
from . import atoms as A
from . import domain as D
from .idents import Idents
from .lower import lower_for

# closed per-language lists of language-BUILTIN exception classes; semantic groups pick within them
PY_ERRS = {"ERR_VALUE": ["ValueError", "TypeError", "OverflowError"],
           "ERR_STATE": ["RuntimeError", "KeyError", "AttributeError"],
           "ERR_INDEX": ["IndexError", "KeyError"]}
JS_ERRS = {"ERR_VALUE": ["RangeError", "TypeError"],
           "ERR_STATE": ["Error", "ReferenceError"],
           "ERR_INDEX": ["RangeError", "URIError"]}
PY_ERR_CLOSED = ("ValueError", "TypeError", "OverflowError", "RuntimeError", "KeyError", "AttributeError", "IndexError",
                 "ZeroDivisionError")
JS_ERR_CLOSED = ("RangeError", "TypeError", "Error", "ReferenceError", "URIError", "EvalError", "SyntaxError")


def make_rng(family, seed):
    return random.Random("%s:%s" % (family, seed))


def seed_hash(family, seed):
    return hashlib.sha256(("%s:%s" % (family, seed)).encode()).hexdigest()[:12]


def build_errors(mod, used, rng, ids, custom):
    """mod.errors[ERR] = {python, javascript, go, bash, [python_custom], [js_custom]} for every abstract id used."""
    taken_py, taken_js = set(), set()
    out = {}
    for k, e in enumerate(sorted(used)):
        py = [n for n in PY_ERRS[e] if n not in taken_py] or [n for n in PY_ERR_CLOSED if n not in taken_py]
        js = [n for n in JS_ERRS[e] if n not in taken_js] or [n for n in JS_ERR_CLOSED if n not in taken_js]
        info = {"python": rng.choice(py), "javascript": rng.choice(js)}
        taken_py.add(info["python"])
        taken_js.add(info["javascript"])
        info["go"] = ids.typename("err.go." + e)
        info["bash"] = 64 + k + rng.randrange(0, 4) * 8
        if custom and rng.random() < 0.6:
            info["python"] = ids.typename("err.py." + e)
            info["python_custom"] = True
            info["javascript"] = ids.typename("err.js." + e)
            info["js_custom"] = True
        out[e] = info
    return out


def _has_atoms(cdom, bash):
    pure, state = A.DOMAIN_ATOMS[cdom]
    return any((not bash) or A.PURE[n][1] for n in pure) or any((not bash) or A.STATEFUL[n][1] for n in state)


def gen_module(seed, lang, family, cdom=None, want_state=None, n_files=None, custom_errors=False, n_pure=None, force_wrapper=False, wrapper_depth=1):
    rng = make_rng(family, seed)
    ids = Idents(seed, family)
    bash = lang == "bash"
    if cdom is None:
        cands = [d for d in A.DOMAIN_IDS if _has_atoms(d, bash)]
        if want_state is False:                                  # explicitly stateless: the area needs pure atoms for this language
            cands = [d for d in cands if any((not bash) or A.PURE[n][1] for n in A.DOMAIN_ATOMS[d][0])]
        cdom = rng.choice(cands)
    pure_names, state_names = A.DOMAIN_ATOMS[cdom]
    pure_ok = [n for n in pure_names if (not bash) or A.PURE[n][1]]
    state_ok = [n for n in state_names if (not bash) or A.STATEFUL[n][1]]
    if want_state is None:
        want_state = bool(state_ok) and (not pure_ok or rng.random() < 0.4)
    if want_state and not state_ok:
        raise ValueError("no stateful atom for %s in %s" % (cdom, lang))
    if not pure_ok and not want_state:
        raise ValueError("domain %s has no atom for %s" % (cdom, lang))
    n_pure = n_pure or (rng.choice([1, 2]) if want_state else rng.choice([1, 2, 2, 3]))
    n_pure = min(n_pure, len(pure_ok)) if pure_ok else 0
    picks = rng.sample(pure_ok, n_pure) if n_pure else []
    mod = I.new_module("m_" + seed_hash(family, seed))
    mod["meta"] = {"lang": lang, "family": family, "seed": str(seed), "cdom": cdom, "package": ids.package("pkg"),
                   "scaf": {"panics": ids.func("scaf.panics"), "tally": ids.var("scaf.tally")},
                   "reset_name": ids.func("reset"), "has_name": ids.func("has"), "fns": {}, "pure_atoms": picks,
                   "state_atom": None, "wrapper": None, "seq": None}
    total_units = n_pure + (1 if want_state else 0)
    nf = n_files or min(rng.choice([1, 2, 2, 3]), max(1, total_units))
    mod["files"] = [ids.module_stem("file%d" % k) for k in range(nf)]
    used_errs = set()
    pure_out = []
    for k, name in enumerate(picks):
        ctx = A.Ctx(rng, ids, "p%d" % k, lang)
        out = A.PURE[name][0](ctx)
        pure_out.append((k, out))
    helpers = []
    for k, out in pure_out:
        fi = (k + (1 if nf > 1 else 0)) % nf if nf > 1 else 0
        for f in out.funcs:
            f["file"] = fi
            mod["funcs"].append(f)
            helpers.append({"name": f["name"], "params": f["params"], "ret": f["ret"]})
        for cdef in out.consts:
            cdef = dict(cdef)
            cdef["file"] = fi
            mod["consts"].append(cdef)
        used_errs |= out.errs
        mod["meta"]["fns"].update(out.fn_specs)
    if want_state:
        sname = rng.choice(state_ok)
        ctx = A.Ctx(rng, ids, "s0", lang, helpers=helpers)
        sout = A.STATEFUL[sname][0](ctx)
        cls_name = ids.typename("cls")
        mod["cls"] = I.new_class(cls_name, sout.fields, file=0)
        for f in sout.funcs:
            f["file"] = 0
            mod["funcs"].append(f)
        for cdef in sout.consts:
            cdef = dict(cdef)
            cdef["file"] = 0
            mod["consts"].append(cdef)
        used_errs |= sout.errs
        mod["meta"]["fns"].update(sout.fn_specs)
        mod["meta"]["state_atom"] = sname
        mod["meta"]["seq"] = {"domain": sout.seq_domain, "snapshot": sout.snapshot, "helper_use": sout.helper_use}
    # a wrapper composing two pure functions (inter-procedural call)
    if len(picks) >= 2 and (force_wrapper or rng.random() < 0.6) and not want_state:
        w = _wrapper(mod, rng, ids, pure_out)
        if w is not None:
            mod["funcs"].append(w)
            mod["meta"]["wrapper"] = w["name"]
            # deeper chains (LOCALISE modules): w2 = h(w1(...), ...) so that more functions lie on every call path
            for depth in range(1, wrapper_depth):
                w2 = _wrapper(mod, rng, ids, pure_out, outer=w)
                if w2 is None:
                    break
                mod["funcs"].append(w2)
                mod["meta"]["wrapper"] = w2["name"]
                w = w2
    mod["errors"] = build_errors(mod, used_errs, rng, ids, custom_errors)
    mod["public"] = [f["name"] for f in mod["funcs"]]
    # raise in a function whose file differs from the error home is fine (imports handled by the renderers)
    I.check_module(mod)
    return mod, ids


def _wrapper(mod, rng, ids, pure_out, outer=None):
    if outer is not None:
        used = set()
        for _, n in I.walk([f["body"] for f in mod["funcs"]]):
            if n[0] == "fcall":
                used.add(n[1])
        cands = [(outer, g) for _, go in pure_out for g in go.funcs
                 if g["name"] not in used and g["name"] != outer["name"] and g["params"] and g["params"][0][1] == I.INT
                 and outer["ret"] == I.INT]
    else:
        cands = [(f, g) for _, fo in pure_out for f in fo.funcs for _, go in pure_out for g in go.funcs
                 if f["name"] != g["name"] and f["ret"] == I.INT and g["params"] and g["params"][0][1] == I.INT]
    rng.shuffle(cands)
    specs = mod["meta"]["fns"]
    for f, g in cands:
        fd, gd = specs[f["name"]]["domain"], specs[g["name"]]["domain"]
        if fd is None or gd is None:
            continue
        dom = [dict(pd) for pd in fd] + [dict(pd) for pd in gd[1:]]
        if D.size(dom) > 3000 or D.size(dom) < D.MIN_POINTS:
            continue
        names = {pd["name"] for pd in dom}
        if len(names) != len(dom):
            continue
        wname = ids.func("wrap" if outer is None else "wrap2:" + outer["name"])
        params = [list(p) for p in f["params"]] + [list(p) for p in g["params"][1:]]
        args_f = [I.v(p[0]) for p in f["params"]]
        args_g = [I.v(p[0]) for p in g["params"][1:]]
        body = [I.ret(I.call(g["name"], I.call(f["name"], *args_f), *args_g))]
        w = I.func(wname, params, g["ret"], body)
        w["file"] = 0
        trial = dict(mod)
        trial["funcs"] = mod["funcs"] + [w]
        specs[wname] = {"domain": dom}
        events, outs = portability_scan(dict(trial, meta=dict(mod["meta"], fns=specs)), "python", wname)
        if events or any(o[0] == "exc" and o[1].startswith("IMP_") for _, o in outs):
            specs.pop(wname, None)
            continue
        specs[wname] = {"atom": "wrapper", "domain": dom, "boundaries": sorted(set(specs[f["name"]]["boundaries"])),
                        "clauses": [("compose", f["name"], g["name"])], "composes": [f["name"], g["name"]]}
        return w
    return None


def prepare(mod, lang, ids):
    """Language-lowered copy (temps drawn from `ids`) plus a fresh check."""
    return lower_for(mod, lang, ids)


def public_calls(mod):
    """Names of functions a question may ask about (everything except purely internal helpers is public here)."""
    return list(mod["public"])


def fn_domain(mod, fname):
    return mod["meta"]["fns"][fname]["domain"]


def portability_scan(mod, lang, fname, limit=D.MAX_POINTS):
    """Run the IR interpreter over a pure function's whole declared domain: returns (events, outcomes_by_point).
    events non-empty => not portable across languages (the generator rejects or re-draws)."""
    from . import interp as X
    dom = fn_domain(mod, fname)
    it = X.Interp(mod, lang)
    outs, events = [], set()
    for pt in D.enumerate_points(dom, limit=limit):
        it.reset_counters()
        outs.append((pt, it.call(fname, pt)))
        events |= it.events
    return events, outs
