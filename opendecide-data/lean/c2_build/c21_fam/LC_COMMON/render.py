"""Dispatcher + witness drivers + test-file renderers for the five languages. Text only (never executed here).

Call plan:  {"calls": [{"fn": name, "args": [json values]}...], "mode": "last" | "all", "snapshot": name | None}
  * pure module (no class): calls are free functions;  stateful module: a fresh instance first, calls are methods.
  * mode "last": earlier calls run unguarded (an exception there crashes the run -> row dropped), the LAST call is guarded
    and its outcome printed. mode "all": every call (and the optional snapshot call) is guarded; one line lists all.
  Driver stdout line:  @@OD@@<json>   with {"ok": v} | {"exc": name}  or  {"res": [..]}.
  Exception name: Python/JS class name; Go authored marker type name; bash "exit:<status>".

Test suite: {"cases": [{"name": ns-stem, "steps": [step...]}]}, step =
  {"op": "eq", "fn", "args", "expect"} | {"op": "raises", "fn", "args", "err"} | {"op": "do", "fn", "args"}
"""
import base64
import json

from . import ir as I
from . import render_base as B
from . import render_py, render_js, render_go, render_sh
from .render_base import EXT

MARK = "@@OD@@"


# ----------------------------------------------------------------------------------------------- module files
def render_module(mod, lang, instrument=False):
    if lang == "python":
        return render_py.render_module(mod, instrument)
    if lang == "javascript":
        return render_js.render_module(mod, False, instrument)
    if lang == "typescript":
        return render_js.render_module(mod, True, instrument)
    if lang == "go":
        return render_go.render_module(mod, instrument)
    if lang == "bash":
        return render_sh.render_module(mod)
    raise ValueError(lang)


def render_function(mod, fn, lang):
    if lang == "python":
        return render_py.render_function_body(mod, fn)
    if lang in ("javascript", "typescript"):
        return render_js.render_function_body(mod, fn, lang == "typescript")
    if lang == "go":
        return render_go.render_function_body(mod, fn)
    return render_sh.render_function_body(mod, fn)


def module_file_names(mod, lang):
    return [stem + EXT[lang] for stem in mod["files"]]


# ----------------------------------------------------------------------------------------------- literals
def value_lit(v, ty, lang):
    if lang == "python":
        return render_py.lit(v, ty)
    if lang in ("javascript", "typescript"):
        return render_js.lit(v, ty)
    if lang == "go":
        return render_go.lit(v, ty)
    raise ValueError("bash literals are rendered inline")


def is_method(mod, fn):
    return I.functions(mod)[fn]["scope"] == "method"


def needs_obj(mod, names, snapshot=None):
    """A fresh instance is only created when a method (or the snapshot method) is actually called (Go forbids unused vars)."""
    if mod["cls"] is None:
        return False
    return bool(snapshot) or any(is_method(mod, n) for n in names)


def sig(mod, fn):
    return I.functions(mod)[fn]


def arg_lits(mod, call, lang):
    f = sig(mod, call["fn"])
    return [value_lit(a, p[1], lang) for a, p in zip(call["args"], f["params"])]


def _imports_needed(mod, calls):
    """Names a driver/test must import per file stem: free functions it calls + the class."""
    need = {}
    fns = I.functions(mod)
    for c in calls:
        f = fns[c["fn"]]
        if f["scope"] == "free":
            need.setdefault(f["file"], set()).add(f["name"])
    if mod["cls"]:
        need.setdefault(mod["cls"]["file"], set()).add(mod["cls"]["name"])
    return need


def custom_err_imports(mod, lang, errs):
    """{file_index: names} of custom (authored) error classes a JS/TS test references (builtins need no import)."""
    out = {}
    if lang in ("javascript", "typescript"):
        home = B.dep_order(mod)[0]
        for e in errs:
            if mod["errors"][e].get("js_custom"):
                out.setdefault(home, set()).add(mod["errors"][e]["javascript"])
    if lang == "python":
        home = B.dep_order(mod)[0]
        for e in errs:
            if mod["errors"][e].get("python_custom"):
                out.setdefault(home, set()).add(mod["errors"][e]["python"])
    return out


def _merge(a, b):
    out = {k: set(v) for k, v in a.items()}
    for k, v in b.items():
        out.setdefault(k, set()).update(v)
    return out


def go_driver_head(pkg):
    """Shared Go driver prelude: imports + odJSON + odRun (the guard that records a recovered panic's type name)."""
    return ["package %s" % pkg, "", "import (", '\t"fmt"', '\t"strconv"', '\t"strings"', '\t"testing"', ")", "",
            "func odJSON(v interface{}) string {", "\tswitch x := v.(type) {", "\tcase int:", "\t\treturn strconv.Itoa(x)",
            "\tcase bool:", "\t\treturn strconv.FormatBool(x)", "\tcase string:", '\t\treturn `"` + x + `"`',
            "\tcase []int:", "\t\tp := []string{}", "\t\tfor _, y := range x {", "\t\t\tp = append(p, strconv.Itoa(y))", "\t\t}",
            '\t\treturn "[" + strings.Join(p, ",") + "]"', "\tcase []string:", "\t\tp := []string{}", "\t\tfor _, y := range x {",
            '\t\t\tp = append(p, `"`+y+`"`)', "\t\t}", '\t\treturn "[" + strings.Join(p, ",") + "]"', "\t}",
            '\treturn "null"', "}", "",
            "func odRun(f func() interface{}) (out string) {", "\tdefer func() {", "\t\tif r := recover(); r != nil {",
            '\t\t\ts := fmt.Sprintf("%T", r)', '\t\t\tif i := strings.LastIndex(s, "."); i >= 0 {', "\t\t\t\ts = s[i+1:]", "\t\t\t}",
            '\t\t\tout = `{"exc":"` + s + `"}`', "\t\t}", "\t}()", '\treturn `{"ok":` + odJSON(f()) + `}`', "}", ""]


# ----------------------------------------------------------------------------------------------- witness drivers
def render_driver(mod, lang, plan, name="od_driver"):
    """Returns ({path: text}, argv). The driver is scaffolding; it is never shown to the model."""
    stateful = mod["cls"] is not None
    calls = plan["calls"]
    if lang == "python":
        need = _imports_needed(mod, calls)
        L = ["import json, os, sys", "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))"]
        for k in sorted(need):
            L.append("from %s import %s" % (mod["files"][k], ", ".join(sorted(need[k]))))
        L += ["", "def emit(o):", "    print('%s' + json.dumps(o, separators=(',', ':'), sort_keys=True))" % MARK, "",
              "def guard(th):", "    try:", "        return {'ok': th()}", "    except BaseException as e:",
              "        return {'exc': type(e).__name__}", ""]
        if needs_obj(mod, [c["fn"] for c in calls], plan.get("snapshot")):
            L.append("obj = %s()" % mod["cls"]["name"])

        def cexpr(c):
            return "%s%s(%s)" % ("obj." if is_method(mod, c["fn"]) else "", c["fn"], ", ".join(arg_lits(mod, c, lang)))

        if plan["mode"] == "last":
            for c in calls[:-1]:
                L.append(cexpr(c))
            L.append("emit(guard(lambda: %s))" % cexpr(calls[-1]))
        else:
            L.append("res = []")
            for c in calls:
                L.append("res.append(guard(lambda: %s))" % cexpr(c))
            if plan.get("snapshot"):
                L.append("res.append(guard(lambda: obj.%s()))" % plan["snapshot"])
            L.append("emit({'res': res})")
        return {name + ".py": "\n".join(L) + "\n"}, ["python", "-I", name + ".py"]

    if lang in ("javascript", "typescript"):
        ts = lang == "typescript"
        need = _imports_needed(mod, calls)
        L = [] if ts else ["'use strict';"]
        for k in sorted(need):
            names = ", ".join(sorted(need[k]))
            if ts:
                L.append("import { %s } from './%s.mts';" % (names, mod["files"][k]))
            else:
                L.append("const { %s } = require('./%s');" % (names, mod["files"][k]))
        L += ["const emit = (o) => console.log('%s' + JSON.stringify(o));" % MARK,
              "const guard = (th) => { try { return { ok: th() }; } catch (e) { return { exc: e.constructor.name }; } };"]
        if needs_obj(mod, [c["fn"] for c in calls], plan.get("snapshot")):
            L.append("const obj = new %s();" % mod["cls"]["name"])

        def cexpr(c):
            return "%s%s(%s)" % ("obj." if is_method(mod, c["fn"]) else "", c["fn"], ", ".join(arg_lits(mod, c, lang)))

        if plan["mode"] == "last":
            for c in calls[:-1]:
                L.append(cexpr(c) + ";")
            L.append("emit(guard(() => %s));" % cexpr(calls[-1]))
        else:
            L.append("const res = [];")
            for c in calls:
                L.append("res.push(guard(() => %s));" % cexpr(c))
            if plan.get("snapshot"):
                L.append("res.push(guard(() => obj.%s()));" % plan["snapshot"])
            L.append("emit({ res });")
        ext = ".mts" if ts else ".js"
        return {name + ext: "\n".join(L) + "\n"}, ["node", name + ext]

    if lang == "go":
        L = go_driver_head(mod["meta"]["package"]) + ["func TestOdDriver(t *testing.T) {"]
        if needs_obj(mod, [c["fn"] for c in calls], plan.get("snapshot")):
            L.append("\tobj := %s()" % render_go.ctor_name(mod["cls"]["name"]))

        def cexpr(c):
            return "%s%s(%s)" % ("obj." if is_method(mod, c["fn"]) else "", c["fn"], ", ".join(arg_lits(mod, c, lang)))

        if plan["mode"] == "last":
            for c in calls[:-1]:
                L.append("\t" + cexpr(c))
            L.append('\tfmt.Println("%s" + odRun(func() interface{} { return %s }))' % (MARK, cexpr(calls[-1])))
        else:
            L.append("\tres := []string{}")
            for c in calls:
                L.append("\tres = append(res, odRun(func() interface{} { return %s }))" % cexpr(c))
            if plan.get("snapshot"):
                L.append("\tres = append(res, odRun(func() interface{} { return obj.%s() }))" % plan["snapshot"])
            L.append('\tfmt.Println("%s" + `{"res":[` + strings.Join(res, ",") + `]}`)' % MARK)
        L.append("}")
        return {name + "_test.go": "\n".join(L) + "\n"}, ["go", "test", "-count=1", "-vet=off", "-run", "TestOdDriver", "-v", "./..."]

    if lang == "bash":
        stem_files = B.dep_order(mod)
        L = ["#!/bin/bash"]
        for k in stem_files:
            L.append('. "${BASH_SOURCE[0]%%/*}/%s.sh"' % mod["files"][k])
        fns = I.functions(mod)

        def call_snip(c, indent=""):
            f = fns[c["fn"]]
            a = []
            for v, p in zip(c["args"], f["params"]):
                a.append("'%s'" % B.check_str(v) if p[1] == I.STR else str(1 if v is True else 0 if v is False else v))
            return "%s %s" % (c["fn"], " ".join(a)) if a else c["fn"]

        def result_snip(c, var):
            f = fns[c["fn"]]
            if f["ret"] == I.INT:
                ok = '%s="{\\"ok\\":$RET}"' % var
            elif f["ret"] == I.BOOL:
                ok = 'if [ "$RET" = 1 ]; then v=true; else v=false; fi; %s="{\\"ok\\":$v}"' % var
            elif f["ret"] == I.STR:
                ok = '%s="{\\"ok\\":\\"$RET\\"}"' % var
            else:
                raise ValueError("bash cannot return lists")
            return ['%s; st=$?' % call_snip(c), 'if [ "$st" -ne 0 ]; then %s="{\\"exc\\":\\"exit:$st\\"}"; else %s; fi' % (var, ok)]

        if plan["mode"] == "last":
            for c in calls[:-1]:
                L.append("%s || exit 99" % call_snip(c))
            L += result_snip(calls[-1], "r")
            L.append('echo "%s$r"' % MARK)
        else:
            L.append("res=()")
            for c in calls:
                L += result_snip(c, "r")
                L.append('res+=("$r")')
            if plan.get("snapshot"):
                L += result_snip({"fn": plan["snapshot"], "args": []}, "r")
                L.append('res+=("$r")')
            L.append('IFS=,; echo "%s{\\"res\\":[${res[*]}]}"' % MARK)
        return {name + ".sh": "\n".join(L) + "\n"}, ["bash", name + ".sh"]
    raise ValueError(lang)


# ----------------------------------------------------------------------------------------------- test files
def _case_calls(case):
    return [{"fn": s["fn"], "args": s["args"]} for s in case["steps"]]


def test_file_name(mod, lang, stem):
    if lang == "python":
        return "test_%s.py" % stem
    if lang == "javascript":
        return "%s.test.js" % stem
    if lang == "typescript":
        return "%s.test.mts" % stem
    if lang == "go":
        return "%s_test.go" % stem
    return "test_%s.sh" % stem


def _live(steps):
    """Steps that really execute (not dropped / commented out)."""
    return [s for s in steps if s["op"] not in ("dropped", "commented")]


def _step_lines(mod, lang, s, ind):
    """Source lines of one test step (without the case wrapper)."""
    fns = I.functions(mod)
    inner = s["inner"] if s["op"] == "commented" else s
    call = None if lang == "bash" else "%s%s(%s)" % ("obj." if is_method(mod, inner["fn"]) else "", inner["fn"], ", ".join(arg_lits(mod, inner, lang)))
    if lang == "python":
        if inner["op"] == "eq":
            out = ["assert %s == %s" % (call, value_lit(inner["expect"], fns[inner["fn"]]["ret"], lang))]
        elif inner["op"] == "do":
            out = [call]
        else:
            out = ["try:", "    " + call, "except %s:" % B.err_marker(mod, inner["err"], lang), "    pass", "else:", "    assert False"]
    elif lang in ("javascript", "typescript"):
        if inner["op"] == "eq":
            out = ["assert.deepStrictEqual(%s, %s);" % (call, value_lit(inner["expect"], fns[inner["fn"]]["ret"], lang))]
        elif inner["op"] == "do":
            out = ["%s;" % call]
        else:
            out = ["assert.throws(() => %s, %s);" % (call, B.err_marker(mod, inner["err"], lang))]
    elif lang == "go":
        pn = mod["meta"].get("scaf", {}).get("panics", "odPanics")
        if inner["op"] == "eq":
            ty = fns[inner["fn"]]["ret"]
            exp = value_lit(inner["expect"], ty, lang)
            cond = ("!slices.Equal(%s, %s)" % (call, exp)) if ty in I.LISTS else ("%s != %s" % (call, exp))
            out = ["if %s {" % cond, '\tt.Fatal("mismatch")', "}"]
        elif inner["op"] == "do":
            out = [call]
        else:
            out = ['if %s(func() { %s }) != "%s" {' % (pn, call, B.err_marker(mod, inner["err"], lang)), '\tt.Fatal("no panic")', "}"]
    else:
        f = fns[inner["fn"]]
        a = []
        for v_, p in zip(inner["args"], f["params"]):
            a.append("'%s'" % B.check_str(v_) if p[1] == I.STR else str(1 if v_ is True else 0 if v_ is False else v_))
        bcall = "%s %s" % (inner["fn"], " ".join(a)) if a else inner["fn"]
        if inner["op"] == "eq":
            exp = inner["expect"]
            exps = ("1" if exp else "0") if f["ret"] == I.BOOL else str(exp)
            out = ["%s || return 1" % bcall, "[ \"$RET\" = '%s' ] || return 1" % exps]
        elif inner["op"] == "do":
            out = ["%s || return 1" % bcall]
        else:
            out = [bcall, "[ \"$?\" -eq %d ] || return 1" % mod["errors"][inner["err"]]["bash"]]
    cm = COMMENT_PREFIX_LANG[lang]
    if s["op"] == "commented":
        out = [cm + x for x in out]
    return [ind + x for x in out]


COMMENT_PREFIX_LANG = {"python": "# ", "javascript": "// ", "typescript": "// ", "go": "// ", "bash": "# "}


def _swallow(lang, lines, ind):
    """Wrap assertion lines so a failure is swallowed (T56g-F8): Python try/except pass, JavaScript try/catch."""
    if lang == "python":
        return [ind + "try:"] + ["    " + x for x in lines] + [ind + "except BaseException:", ind + "    pass"]
    if lang in ("javascript", "typescript"):
        return [ind + "try {"] + ["  " + x for x in lines] + [ind + "} catch (e) {", ind + "}"]
    return lines


def render_tests(mod, lang, suite, stem, extra_header=None, blocks=None):
    """Return (path, text) for a test file in the language's native runner style (see module docstring).
    Step ops: eq / raises / do, plus "dropped" (omitted) and "commented" (the inner step as comments) for T56g-F1.
    Case options: marks 'skip' | 'xfail' (T56g-F2), swallow True (T56g-F8, Python / JavaScript).
    `extra_header`: optional list of lines inserted after the imports (T56g transforms use this).
    `blocks`: optional dict that receives {case name: the case's own source text} (hidden-suite leak scan, TESTSEL options)."""
    cases = suite["cases"]
    errs = sorted({s.get("err") or (s.get("inner") or {}).get("err") for c in cases for s in c["steps"]
                   if s["op"] == "raises" or (s["op"] == "commented" and s["inner"]["op"] == "raises")})
    errs = [e for e in errs if e]
    allcalls = [cc for c in cases for cc in _case_calls({"steps": [(s["inner"] if s["op"] == "commented" else s) for s in c["steps"] if s["op"] != "dropped"]})]
    need = _merge(_imports_needed(mod, allcalls), custom_err_imports(mod, lang, errs))
    fns = I.functions(mod)
    path = test_file_name(mod, lang, stem)
    scaf = mod["meta"].get("scaf", {})
    uses_marks = any(c.get("marks") for c in cases)
    live_raises = any(s["op"] == "raises" for c in cases for s in _live(c["steps"]))

    def case_uses_obj(c):
        return needs_obj(mod, [s["fn"] for s in _live(c["steps"])])

    if lang == "python":
        L = []
        if uses_marks:
            L.append("import pytest")
        for k in sorted(need):
            L.append("from %s import %s" % (mod["files"][k], ", ".join(sorted(need[k]))))
        L += list(extra_header or [])
        for c in cases:
            _mark = len(L) + 2
            L += ["", ""]
            if c.get("marks") == "skip":
                L.append('@pytest.mark.skip(reason="%s")' % c.get("reason", "later"))
            elif c.get("marks") == "xfail":
                L.append('@pytest.mark.xfail(reason="%s")' % c.get("reason", "later"))
            _mark = len(L)
            L.append("def test_%s():" % c["name"])
            body = []
            if case_uses_obj(c):
                body.append("    obj = %s()" % mod["cls"]["name"])
            for s in c["steps"]:
                if s["op"] == "dropped":
                    continue
                sl = _step_lines(mod, lang, s, "    ")
                body += _swallow(lang, sl, "    ") if (c.get("swallow") and s["op"] in ("eq", "raises")) else sl
            if not body or all(x.lstrip().startswith("#") for x in body):
                body.append("    pass")
            L += body
            if blocks is not None:
                blocks[c["name"]] = "\n".join(L[_mark:]) + "\n"
        return path, "\n".join(L).lstrip("\n") + "\n"
    if lang in ("javascript", "typescript"):
        ts = lang == "typescript"
        L = []
        if ts:
            L += ["import test from 'node:test';", "import assert from 'node:assert/strict';"]
            for k in sorted(need):
                L.append("import { %s } from './%s.mts';" % (", ".join(sorted(need[k])), mod["files"][k]))
        else:
            L += ["'use strict';", "const test = require('node:test');", "const assert = require('node:assert/strict');"]
            for k in sorted(need):
                L.append("const { %s } = require('./%s');" % (", ".join(sorted(need[k])), mod["files"][k]))
        L += list(extra_header or [])
        for c in cases:
            _mark = len(L) + 1
            head = "test.skip" if c.get("marks") in ("skip", "xfail") else "test"
            L += ["", "%s('%s', () => {" % (head, c["name"])]
            if case_uses_obj(c):
                L.append("  const obj = new %s();" % mod["cls"]["name"])
            for s in c["steps"]:
                if s["op"] == "dropped":
                    continue
                sl = _step_lines(mod, lang, s, "  ")
                L += _swallow(lang, sl, "  ") if (c.get("swallow") and s["op"] in ("eq", "raises")) else sl
            L.append("});")
            if blocks is not None:
                blocks[c["name"]] = "\n".join(L[_mark:]) + "\n"
        return path, "\n".join(L) + "\n"
    if lang == "go":
        pkg = mod["meta"]["package"]
        pn = scaf.get("panics", "odPanics")
        has_list = any(fns[s["fn"]]["ret"] in I.LISTS for c in cases for s in _live(c["steps"]) if s["op"] == "eq")
        imports = ['"testing"']
        if live_raises:
            imports += ['"fmt"', '"strings"']
        if has_list:
            imports.append('"slices"')
        L = ["package %s" % pkg, "", "import ("] + ["\t" + i for i in sorted(imports)] + [")"]
        if live_raises:
            L += ["", "func %s(f func()) (name string) {" % pn, "\tdefer func() {", "\t\tif r := recover(); r != nil {",
                  '\t\t\tname = fmt.Sprintf("%T", r)', '\t\t\tif i := strings.LastIndex(name, "."); i >= 0 {',
                  "\t\t\t\tname = name[i+1:]", "\t\t\t}", "\t\t}", "\t}()", "\tf()", '\treturn ""', "}"]
        L += list(extra_header or [])
        for c in cases:
            _mark = len(L) + 1
            L += ["", "func Test%s(t *testing.T) {" % c["name"].capitalize()]
            if c.get("marks") in ("skip", "xfail"):
                L.append('\tt.Skip("%s")' % c.get("reason", "later"))
            if case_uses_obj(c):
                L.append("\tobj := %s()" % render_go.ctor_name(mod["cls"]["name"]))
            for s in c["steps"]:
                if s["op"] == "dropped":
                    continue
                L += _step_lines(mod, lang, s, "\t")
            L.append("}")
            if blocks is not None:
                blocks[c["name"]] = "\n".join(L[_mark:]) + "\n"
        return path, "\n".join(L) + "\n"
    if lang == "bash":
        tally = scaf.get("tally", "failed")
        L = ["#!/bin/bash"]
        for k in B.dep_order(mod):
            L.append('. "${BASH_SOURCE[0]%%/*}/%s.sh"' % mod["files"][k])
        L += list(extra_header or [])
        names = []
        for c in cases:
            fn_name = "test_%s" % c["name"]
            names.append(fn_name)
            _mark = len(L) + 1
            L += ["", "%s() {" % fn_name]
            if c.get("marks") in ("skip", "xfail"):
                L.append("  return 0")
            if mod["cls"] is not None:
                L.append("  %s" % mod["meta"]["reset_name"])
            body = []
            for s in c["steps"]:
                if s["op"] == "dropped":
                    continue
                body += _step_lines(mod, lang, s, "  ")
            L += body if body else ["  :"]
            L.append("}")
            if blocks is not None:
                blocks[c["name"]] = "\n".join(L[_mark:]) + "\n"
        L += ["", "%s=0" % tally, "for t in %s; do" % " ".join(names), "  if $t; then", '    echo "ok $t"', "  else",
              '    echo "not ok $t"', "    %s=1" % tally, "  fi", "done", "exit $%s" % tally]
        return path, "\n".join(L) + "\n"
    raise ValueError(lang)


def suite_argv(lang, test_paths, junit=True):
    """argv for running a suite with the language-native runner (executor-owned config for pytest)."""
    if lang == "python":
        return ["python", "-m", "pytest", "-c", "/etc/od-sbx/pytest.ini", "--rootdir", "/work", "--noconftest",
                "--junitxml=/out/junit.xml"] + list(test_paths)
    if lang in ("javascript", "typescript"):
        return ["node", "--test", "--test-reporter=junit", "--test-reporter-destination=/out/junit.xml"] + list(test_paths)
    if lang == "go":
        return ["go", "test", "-count=1", "-vet=off", "-json", "./..."]
    return ["bash"] + list(test_paths)


def suite_report(lang):
    return {"python": "junit.xml", "javascript": "junit.xml", "typescript": "junit.xml", "go": None, "bash": None}[lang]


def toolchain(lang):
    return {"python": "python", "javascript": "node", "typescript": "node", "go": "go", "bash": "sh"}[lang]


# ----------------------------------------------------------------------------------------------- executor job line
def job_line(row_id, lang, files, argv, kind="run", repeats=3, report=None, expected_ids=None):
    """One line of the od-sbx run-batch JSON-lines input. `repeats` is advisory (the executor reads
    will_this_test_fail to choose 3 runs; L-0 is asked to honour `repeats`)."""
    return {"row_id": row_id, "toolchain": toolchain(lang), "kind": kind, "will_this_test_fail": repeats >= 3,
            "repeats": repeats,
            "files": {k: base64.b64encode(v.encode("utf-8")).decode("ascii") for k, v in sorted(files.items())},
            "argv": list(argv), "report": report, "expected_ids": expected_ids}


def parse_marker_lines(stdout):
    """Witness lines from a captured stdout: list of parsed JSON objects (marker lines only)."""
    out = []
    for line in stdout.splitlines():
        k = line.find(MARK)
        if k >= 0:
            out.append(json.loads(line[k + len(MARK):]))
    return out


def observable_of(mod, lang, outcome):
    """Spec-expectation observable for an interpreter outcome ("ok", v) | ("exc", ERR)."""
    if outcome[0] == "ok":
        return {"ok": outcome[1]}
    err = outcome[1]
    if err == "IMP_INDEX":
        return {"exc": "IndexError" if lang == "python" else "__non_portable__"}
    info = mod["errors"][err]
    if lang == "bash":
        return {"exc": "exit:%d" % info["bash"]}
    return {"exc": B.err_marker(mod, err, lang)}
