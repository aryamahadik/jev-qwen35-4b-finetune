"""Exhaustive-domain driver (the "own domain enumerator" of T42c / the differential input set of T57).

The host enumerates the declared finite domain (domain.py); the driver is UNROLLED source that runs every point (pure
function: one call; stateful: one call sequence on a fresh instance followed by the snapshot call) and prints one JSON line
per point, `@@ODP@@<json>`. Two programs are observably equal on the domain iff their driver stdout is byte-identical
(the executor hashes ALL stdout bytes even when the preview is capped). Text only; nothing is executed here.
"""
import json

from . import ir as I
from . import render as R
from . import render_base as B
from . import render_go

MARKP = "@@ODP@@"


def _call_expr(mod, lang, c, obj):
    fns = I.functions(mod)
    f = fns[c["fn"]]
    if f["scope"] != "method":
        obj = ""
    if lang == "bash":
        a = " ".join(("'%s'" % B.check_str(v)) if p[1] == I.STR else str(1 if v is True else 0 if v is False else v)
                     for v, p in zip(c["args"], f["params"]))
        return ("%s %s" % (c["fn"], a)) if a else c["fn"]
    args = ", ".join(R.value_lit(v, p[1], lang) for v, p in zip(c["args"], f["params"]))
    return "%s%s(%s)" % (obj, c["fn"], args)


def _uses_obj(mod, pt, snapshot):
    return bool(snapshot) or any(I.functions(mod)[c["fn"]]["scope"] == "method" for c in pt)


def _is_seq(mod, pt, snapshot):
    """A point is a call SEQUENCE (list of outcomes, snapshot last) when it touches the instance; else one plain call."""
    return mod["cls"] is not None and _uses_obj(mod, pt, snapshot)


def render(mod, lang, points, snapshot=None, name="od_dom"):
    """points: list of call lists (pure: one call each). Returns ({path: text}, argv)."""
    stateful = mod["cls"] is not None
    fns = I.functions(mod)
    need = R._imports_needed(mod, [c for pt in points for c in pt])
    if lang == "python":
        L = ["import json, os, sys", "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))"]
        for k in sorted(need):
            L.append("from %s import %s" % (mod["files"][k], ", ".join(sorted(need[k]))))
        L += ["", "def guard(th):", "    try:", "        return {'ok': th()}", "    except BaseException as e:",
              "        return {'exc': type(e).__name__}", "",
              "def out(o):", "    print('%s' + json.dumps(o, separators=(',', ':'), sort_keys=True))" % MARKP, ""]
        for pt in points:
            if _is_seq(mod, pt, snapshot):
                L.append("obj = %s(); res = []" % mod["cls"]["name"])
                for c in pt:
                    L.append("res.append(guard(lambda: %s))" % _call_expr(mod, lang, c, "obj."))
                if snapshot:
                    L.append("res.append(guard(lambda: obj.%s()))" % snapshot)
                L.append("out(res)")
            else:
                L.append("out(guard(lambda: %s))" % _call_expr(mod, lang, pt[0], ""))
        return {name + ".py": "\n".join(L) + "\n"}, ["python", "-I", name + ".py"]
    if lang in ("javascript", "typescript"):
        ts = lang == "typescript"
        L = [] if ts else ["'use strict';"]
        for k in sorted(need):
            names = ", ".join(sorted(need[k]))
            L.append(("import { %s } from './%s.mts';" if ts else "const { %s } = require('./%s');") % (names, mod["files"][k]))
        L += ["const guard = (th) => { try { return { ok: th() }; } catch (e) { return { exc: e.constructor.name }; } };",
              "const out = (o) => console.log('%s' + JSON.stringify(o));" % MARKP]
        for pt in points:
            if _is_seq(mod, pt, snapshot):
                L.append("{ const obj = new %s(); const res = [];" % mod["cls"]["name"])
                for c in pt:
                    L.append("res.push(guard(() => %s));" % _call_expr(mod, lang, c, "obj."))
                if snapshot:
                    L.append("res.push(guard(() => obj.%s()));" % snapshot)
                L.append("out(res); }")
            else:
                L.append("out(guard(() => %s));" % _call_expr(mod, lang, pt[0], ""))
        ext = ".mts" if ts else ".js"
        return {name + ext: "\n".join(L) + "\n"}, ["node", name + ext]
    if lang == "go":
        L = R.go_driver_head(mod["meta"]["package"]) + ["func TestOdDomain(t *testing.T) {"]
        for pt in points:
            if _is_seq(mod, pt, snapshot):
                L.append("\t{ obj := %s(); res := []string{}" % render_go.ctor_name(mod["cls"]["name"]))
                for c in pt:
                    L.append("\tres = append(res, odRun(func() interface{} { return %s }))" % _call_expr(mod, lang, c, "obj."))
                if snapshot:
                    L.append("\tres = append(res, odRun(func() interface{} { return obj.%s() }))" % snapshot)
                L.append('\tfmt.Println("%s" + "[" + strings.Join(res, ",") + "]") }' % MARKP)
            else:
                L.append('\tfmt.Println("%s" + odRun(func() interface{} { return %s }))' % (MARKP, _call_expr(mod, lang, pt[0], "")))
        L.append("}")
        return {name + "_test.go": "\n".join(L) + "\n"}, ["go", "test", "-count=1", "-vet=off", "-run", "TestOdDomain", "-v", "./..."]
    # bash
    L = ["#!/bin/bash"]
    for k in B.dep_order(mod):
        L.append('. "${BASH_SOURCE[0]%%/*}/%s.sh"' % mod["files"][k])

    def snip(c, var):
        f = fns[c["fn"]]
        if f["ret"] == I.INT:
            ok = '%s="{\\"ok\\":$RET}"' % var
        elif f["ret"] == I.BOOL:
            ok = 'if [ "$RET" = 1 ]; then v=true; else v=false; fi; %s="{\\"ok\\":$v}"' % var
        else:
            ok = '%s="{\\"ok\\":\\"$RET\\"}"' % var
        return ["%s; st=$?" % _call_expr(mod, lang, c, ""),
                'if [ "$st" -ne 0 ]; then %s="{\\"exc\\":\\"exit:$st\\"}"; else %s; fi' % (var, ok)]

    for pt in points:
        if _is_seq(mod, pt, snapshot):
            L.append("%s; res=()" % mod["meta"]["reset_name"])
            for c in pt:
                L += snip(c, "r")
                L.append('res+=("$r")')
            if snapshot:
                L += snip({"fn": snapshot, "args": []}, "r")
                L.append('res+=("$r")')
            L.append('IFS=,; echo "%s[${res[*]}]"' % MARKP)
        else:
            L += snip(pt[0], "r")
            L.append('echo "%s$r"' % MARKP)
    return {name + ".sh": "\n".join(L) + "\n"}, ["bash", name + ".sh"]


def expected_stdout(mod, lang, points, snapshot=None):
    """Spec expectation of the driver's stdout, from the IR interpreter (used by SimExecutor and as the K2 check)."""
    from . import interp as X
    lines = []
    for pt in points:
        it = X.Interp(mod, lang)
        outs = [it.call(c["fn"], c["args"]) for c in pt]
        if _is_seq(mod, pt, snapshot):
            if snapshot:
                outs.append(it.call(snapshot, []))
            obs = [R.observable_of(mod, lang, o) for o in outs]
        else:
            obs = R.observable_of(mod, lang, outs[0])
        lines.append(MARKP + json.dumps(obs, separators=(",", ":"), sort_keys=True))
    return "\n".join(lines) + "\n"
