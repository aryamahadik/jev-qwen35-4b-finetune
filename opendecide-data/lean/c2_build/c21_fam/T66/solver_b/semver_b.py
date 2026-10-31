"""SEMVER head of solver B.

Question: does at least one SHOWN caller fail on the new API? (The declared version bump is a decoy and is never read.)
Layer 1, signature rules (static, from the text only): each call of an imported API name inside a caller is bound against the OLD and the NEW signature with the
Python calling rules (positional count, keyword names, missing required, duplicate); a name that the new module no longer defines makes every caller fail at import.
Layer 2, B's own evaluator (`pyi`): every caller is evaluated against the old module (it must pass: gold-sanity) and against the new module.
Layer 1 is decisive only for BREAKING, and when it is decisive layer 2 must agree (otherwise B abstains: its two derivations conflict)."""
import ast
import re

from . import pyi
from . import textparse as tp

HEADS = {
    "old": r"^Old API \((\S+)\.py\):$",
    "new": r"^New API \((\S+)\.py\):$",
    "callers": r"^Callers written against the old API \((\S+)\):$",
    "bump": r"^Declared version bump: (\S+)$",
}


def defined_names(tree):
    names = {}
    for s in tree.body:
        if isinstance(s, (ast.FunctionDef, ast.ClassDef)):
            names[s.name] = s
        elif isinstance(s, ast.Assign):
            for t in s.targets:
                if isinstance(t, ast.Name):
                    names[t.id] = s
        elif isinstance(s, (ast.Import, ast.ImportFrom)):
            for a in s.names:
                names[(a.asname or a.name).split(".")[0]] = s
    return names


def signature(fn):
    a = fn.args
    pos = [x.arg for x in a.posonlyargs + a.args]
    ndef = len(a.defaults)
    return {"pos": pos, "nreq": len(pos) - ndef, "posonly": len(a.posonlyargs), "kwonly": [x.arg for x in a.kwonlyargs],
            "kwreq": [x.arg for x, d in zip(a.kwonlyargs, a.kw_defaults) if d is None], "vararg": a.vararg is not None, "kwarg": a.kwarg is not None}


def binds(sig, npos, kws):
    """Python's binding rules for a call with `npos` positional arguments and keyword names `kws`. -> True when the call can bind."""
    pos = sig["pos"]
    if npos > len(pos) and not sig["vararg"]:
        return False
    given = set(pos[:min(npos, len(pos))])
    for k in kws:
        if k in given:
            return False
        if k in pos[sig["posonly"]:] or k in sig["kwonly"]:
            given.add(k)
        elif not sig["kwarg"]:
            return False
    for i, p in enumerate(pos):
        if i >= sig["nreq"]:
            break
        if p not in given:
            return False
    return all(k in given for k in sig["kwreq"])


def _calls_outside_try(test_fn, api_names):
    """Calls of an API name that sit directly in the statements of the test body (not inside try / def / lambda / compound statements)."""
    out = []

    def scan(expr):
        for n in ast.walk(expr):
            if isinstance(n, (ast.Lambda, ast.ListComp, ast.GeneratorExp, ast.SetComp, ast.DictComp)):
                return
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in api_names:
                out.append(n)
    for s in test_fn.body:
        if isinstance(s, (ast.Expr, ast.Assign, ast.Assert, ast.Return, ast.AugAssign)):
            scan(s.value if not isinstance(s, ast.Assert) else s.test)
    return out


def static_break(new_src, callers_src, stem):
    """Layer 1. -> (True, why) when some caller must fail on the new module by name / signature rules alone, else (False, "")."""
    try:
        new_tree, c_tree = ast.parse(new_src), ast.parse(callers_src)
    except (SyntaxError, ValueError):
        return True, "syntax"
    new_names = defined_names(new_tree)
    imported = {}
    for s in c_tree.body:
        if isinstance(s, ast.ImportFrom) and s.module == stem:
            for a in s.names:
                imported[a.asname or a.name] = a.name
    for local, orig in imported.items():
        if orig not in new_names:
            return True, "name removed"
    sigs = {local: signature(new_names[orig]) for local, orig in imported.items() if isinstance(new_names.get(orig), ast.FunctionDef)}
    for t in c_tree.body:
        if isinstance(t, ast.FunctionDef) and t.name.startswith("test"):
            for call in _calls_outside_try(t, set(sigs)):
                if any(isinstance(x, ast.Starred) for x in call.args) or any(k.arg is None for k in call.keywords):
                    continue
                if not binds(sigs[call.func.id], len(call.args), [k.arg for k in call.keywords]):
                    return True, "call does not bind"
    return False, ""


def solve(context):
    _pre, secs = tp.split_sections(context, HEADS)
    kinds = [k for k, _m, _b in secs]
    if kinds not in (["old", "new", "callers"], ["old", "new", "callers", "bump"]):
        return None, "sections:" + ",".join(kinds)
    (_, mo, old), (_, mn, new), (_, mc, callers) = secs[:3]
    stem = mo.group(1)
    if mn.group(1) != stem:
        return None, "stem mismatch"
    # gold sanity: the callers pass on the old API
    r_old = pyi.run_suite(pyi.World({stem: old}), callers, "callers")
    if r_old.status == "unsupported":
        return None, "unsupported(old):%s" % r_old.detail
    if not r_old.ok:
        return None, "old API fails a shown caller"
    sb, why = static_break(new, callers, stem)
    r_new = pyi.run_suite(pyi.World({stem: new}), callers, "callers")
    if r_new.status == "unsupported":
        if sb:
            return "BREAKING", "rule: " + why              # a caller that cannot bind / import fails whatever the bodies do
        return None, "unsupported(new):%s" % r_new.detail
    if sb and r_new.ok:
        return None, "rule layer and evaluator conflict (%s)" % why
    return ("SAFE", "all shown callers pass") if r_new.ok else ("BREAKING", "a shown caller fails")
