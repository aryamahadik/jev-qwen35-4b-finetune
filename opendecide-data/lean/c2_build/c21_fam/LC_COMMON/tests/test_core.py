"""Core tests: IR, generator, renderers (text only), interpreter, lowering, mutator, transforms, names.
No generated code is ever executed: Python output is only parsed with ast.parse."""
import ast
import random
import re

import pytest

from LC_COMMON import atoms as A
from LC_COMMON import domain as D
from LC_COMMON import interp as X
from LC_COMMON import ir as I
from LC_COMMON import irmut
from LC_COMMON import modgen
from LC_COMMON import render as R
from LC_COMMON import transforms as T
from LC_COMMON.idents import Idents, reserved_hit
from LC_COMMON.names_guard import NamesGuard, NamesViolation

LANGS = ("python", "javascript", "typescript", "go", "bash")


# ------------------------------------------------------------------------------------------------ IR
def test_ir_type_errors_are_caught():
    mod = I.new_module("x")
    mod["funcs"].append(I.func("f", [["a", I.INT]], I.INT, [I.ret(I.s("x"))]))
    with pytest.raises(I.IRError):
        I.check_module(mod)
    mod["funcs"][0] = I.func("f", [["a", I.INT]], I.INT, [I.let("u", I.INT, I.v("a")), I.ret(I.i(1))])
    with pytest.raises(I.IRError):                       # unused local (Go would refuse to compile it)
        I.check_module(mod)
    mod["funcs"][0] = I.func("f", [["a", I.INT]], I.INT, [I.ret(I.bin_("//", I.v("a"), I.v("a")))])
    with pytest.raises(I.IRError):                       # divisor must be a positive literal
        I.check_module(mod)
    mod["funcs"][0] = I.func("f", [["a", I.INT]], I.INT, [I.if_(I.gt(I.v("a"), I.i(1)), [I.ret(I.i(1))])])
    with pytest.raises(I.IRError):                       # does not terminate
        I.check_module(mod)


def test_block_scoping_and_list_param_mutation_refused():
    mod = I.new_module("x")
    body = [I.if_(I.gt(I.v("a"), I.i(1)), [I.let("t", I.INT, I.i(2))]), I.ret(I.v("t"))]
    mod["funcs"].append(I.func("f", [["a", I.INT]], I.INT, body))
    with pytest.raises(I.IRError):
        I.check_module(mod)
    mod["funcs"][0] = I.func("f", [["xs", I.INTS]], I.INT, [["push", I.v("xs"), I.i(1)], I.ret(I.i(0))])
    with pytest.raises(I.IRError):
        I.check_module(mod)


def test_free_function_cannot_touch_state():
    mod = I.new_module("x")
    mod["cls"] = I.new_class("K", [{"name": "n", "type": I.INT, "init": 0}])
    mod["funcs"].append(I.func("f", [], I.INT, [I.ret(I.fld("n"))], scope="free"))
    with pytest.raises(I.IRError):
        I.check_module(mod)


def test_norm_hash_ignores_names_but_not_literals():
    m1, _ = modgen.gen_module(5, "python", "T42c", cdom="cdom03")
    m2 = I.clone(m1)
    # rename the first function and its first param everywhere
    f0 = m2["funcs"][0]
    old = f0["name"]
    f0["name"] = "renamed_function"
    for fn in m2["funcs"]:
        for _, n in I.walk(fn["body"]):
            if n[0] in ("fcall", "mcall") and n[1] == old:
                n[1] = "renamed_function"
    m2["public"] = [f["name"] for f in m2["funcs"]]
    assert I.norm_hash(m1) == I.norm_hash(m2)
    m3 = I.clone(m1)
    for _, n in I.walk(m3["funcs"][0]["body"]):
        if n[0] == "int":
            n[1] += 1
            break
    assert I.norm_hash(m1) != I.norm_hash(m3)


# ------------------------------------------------------------------------------------------------ generator
@pytest.mark.parametrize("lang", LANGS)
def test_generator_builds_valid_modules_in_every_language(lang):
    seen_state = seen_wrap = seen_multi = 0
    for seed in range(60):
        mod, ids = modgen.gen_module(seed, lang, "T42c", custom_errors=(seed % 4 == 0))
        I.check_module(mod)
        lo = modgen.prepare(mod, lang, ids)
        files = R.render_module(lo, lang)
        assert len(files) >= len(mod["files"])
        seen_state += bool(mod["cls"])
        seen_wrap += bool(mod["meta"]["wrapper"])
        seen_multi += len(mod["files"]) > 1
        if lang == "python":
            for path, text in files.items():
                ast.parse(text)                          # parse only
    assert seen_state > 3 and seen_multi > 10
    if lang != "bash":
        assert seen_wrap > 0


def test_every_atom_domain_is_within_bounds_and_portable():
    for lang in ("python", "go", "bash"):
        for seed in range(80):
            mod, ids = modgen.gen_module(seed, lang, "T57")
            for f in mod["funcs"]:
                if f["scope"] != "free":
                    continue
                dom = mod["meta"]["fns"][f["name"]]["domain"]
                n = D.check_bounds(dom)
                assert D.MIN_POINTS <= n <= D.MAX_POINTS
                events, outs = modgen.portability_scan(mod, lang, f["name"])
                assert not events, (lang, seed, f["name"], events)
                assert len(outs) == n


def test_stateful_sequences_are_portable():
    for lang in ("python", "javascript", "go", "bash"):
        checked = 0
        for seed in range(120):
            mod, ids = modgen.gen_module(seed, lang, "T42c", want_state=True)
            sd = mod["meta"]["seq"]["domain"]
            assert D.size(sd) <= D.MAX_POINTS and D.size(sd) >= D.MIN_POINTS
            for seq in D.enumerate_sequences(sd):
                it = X.Interp(mod, lang)
                it.sequence([(c["fn"], c["args"]) for c in seq])
                assert not it.events
            checked += 1
        assert checked == 120


def test_identifiers_come_from_the_namespace_and_avoid_reserved_words():
    ids = Idents(1, "T42c")
    names = [ids.func("a"), ids.var("b"), ids.field("c"), ids.const("d"), ids.strval("e"), ids.typename("f"), ids.module_stem("g")]
    assert len(set(n.lower() for n in names)) == len(names)
    for n in names:
        assert re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", n)
        assert not reserved_hit(n)
    # deterministic
    assert Idents(1, "T42c").func("a") == names[0]
    assert Idents(2, "T42c").func("a") != names[0]
    assert Idents(1, "T57").func("a") != names[0]          # seed spaces are disjoint per family tag
    # a name the namespace would draw that is reserved is redrawn
    assert reserved_hit("print") and reserved_hit("Main") and reserved_hit("od_tmp") is False


def test_no_hand_picked_identifier_reaches_the_renderers():
    mod, ids = modgen.gen_module(11, "python", "T42c", want_state=True)
    for f in mod["funcs"]:
        assert re.fullmatch(r"[a-z]+_[a-z]+", f["name"])           # namespace 'tool' shape: stem_stem
    assert re.fullmatch(r"[A-Z][a-z]+", mod["cls"]["name"])


# ------------------------------------------------------------------------------------------------ lowering
def test_go_and_bash_lowering_removes_cond_and_nested_calls():
    for lang in ("go", "bash"):
        for seed in range(80):
            mod, ids = modgen.gen_module(seed, lang, "T42c")
            lo = modgen.prepare(mod, lang, ids)
            for fn in lo["funcs"]:
                heads = [n[0] for _, n in I.walk(fn["body"])]
                assert "cond" not in heads
    # an artificial module with a cond and a nested call
    mod = I.new_module("x")
    mod["files"] = ["f0"]
    mod["funcs"].append(I.func("g", [["a", I.INT]], I.INT, [I.ret(I.add(I.v("a"), I.i(1)))]))
    body = [I.ret(I.add(["cond", I.gt(I.v("a"), I.i(2)), I.v("a"), I.i(0)], I.call("g", I.v("a"))))]
    mod["funcs"].append(I.func("f", [["a", I.INT]], I.INT, body))
    I.check_module(mod)
    ids = Idents(3, "T42c")
    lo_go = modgen.prepare(mod, "go", ids)
    assert not any(n[0] == "cond" for _, n in I.walk(lo_go["funcs"][1]["body"]))
    lo_sh = modgen.prepare(mod, "bash", Idents(3, "T42c"))
    ret_stmt = lo_sh["funcs"][1]["body"][-1]
    assert not any(n[0] in ("fcall", "mcall") for _, n in I.walk(ret_stmt))
    # lowering keeps behaviour
    for a in range(0, 6):
        assert X.Interp(mod).call("f", [a]) == X.Interp(lo_sh).call("f", [a]) == X.Interp(lo_go).call("f", [a])


def test_loop_bound_that_changes_is_hoisted_for_non_python():
    mod = I.new_module("x")
    mod["files"] = ["f0"]
    body = [I.let("n", I.INT, I.v("a")), I.let("t", I.INT, I.i(0)),
            I.for_("k", I.i(0), I.v("n"), [I.set_("n", I.sub(I.v("n"), I.i(1))), I.set_("t", I.add(I.v("t"), I.i(1)))]),
            I.ret(I.v("t"))]
    mod["funcs"].append(I.func("f", [["a", I.INT]], I.INT, body))
    I.check_module(mod)
    lo = modgen.prepare(mod, "javascript", Idents(1, "T42c"))
    fors = [n for _, n in I.walk(lo["funcs"][0]["body"]) if n[0] == "for"]
    assert fors[0][3][0] == "var" and fors[0][3][1] != "n"
    assert X.Interp(mod).call("f", [5]) == X.Interp(lo, "javascript").call("f", [5]) == ("ok", 5)


# ------------------------------------------------------------------------------------------------ renderers
def test_python_rendering_golden_shapes():
    mod = I.new_module("x")
    mod["files"] = ["m0", "m1"]
    mod["consts"] = [{"name": "tbl", "type": I.INTS, "value": [1, 2], "file": 1}]
    mod["funcs"] = [
        I.func("helper", [["a", I.INT]], I.INT, [I.ret(I.add(I.v("a"), ["idx", I.cst("tbl"), I.i(0)]))], file=1),
        I.func("main", [["a", I.INT], ["s", I.STR]], I.STR,
               [I.if_(I.lt(I.add(I.call("helper", I.v("a")), ["idx", I.cst("tbl"), I.i(1)]), I.i(5)), [I.ret(I.cat(I.v("s"), I.s("-")))]),
                I.ret(I.cat(I.v("s"), ["zpad", I.v("a"), I.i(3)]))], file=0)]
    I.check_module(mod)
    files = R.render_module(mod, "python")
    assert files["m0.py"].startswith("from m1 import helper, tbl")
    assert "if helper(a) + tbl[1] < 5:" in files["m0.py"]
    assert "str(a).zfill(3)" in files["m0.py"]
    assert files["m1.py"].startswith("tbl = [1, 2]")
    js = R.render_module(mod, "javascript")
    assert "const { helper, tbl } = require('./m1');" in js["m0.js"]
    assert "String(a).padStart(3, '0')" in js["m0.js"]
    assert js["m1.js"].rstrip().endswith("module.exports = { tbl, helper };")
    ts = R.render_module(mod, "typescript")
    assert "import { helper, tbl } from './m1.mts';" in ts["m0.mts"]
    assert "export function main(a: number, s: string): string {" in ts["m0.mts"]
    mod["meta"] = {"package": "pkgx"}
    go = R.render_module(mod, "go")
    assert go["m0.go"].startswith("package pkgx\n\nimport (\n\t\"fmt\"\n)")
    assert 'fmt.Sprintf("%03d", a)' in go["m0.go"]
    assert go["go.mod"].startswith("module pkgx") and go["vendor/modules.txt"] == ""


def test_precedence_and_parentheses():
    mod = I.new_module("x")
    mod["files"] = ["m0"]
    e = I.mul(I.sub(I.v("a"), I.v("b")), I.sub(I.v("a"), I.sub(I.v("b"), I.i(1))))
    mod["funcs"] = [I.func("f", [["a", I.INT], ["b", I.INT]], I.INT, [I.ret(e)])]
    I.check_module(mod)
    for lang, want in (("python", "(a - b) * (a - (b - 1))"), ("javascript", "(a - b) * (a - (b - 1))")):
        assert want in R.render_module(mod, lang)[("m0.py" if lang == "python" else "m0.js")]
    cmp_mod = I.new_module("x")
    cmp_mod["files"] = ["m0"]
    cmp_mod["funcs"] = [I.func("f", [["a", I.INT], ["b", I.INT]], I.BOOL,
                               [I.ret(I.eq(I.lt(I.v("a"), I.v("b")), I.lt(I.v("b"), I.v("a"))))])]
    I.check_module(cmp_mod)
    assert "(a < b) == (b < a)" in R.render_module(cmp_mod, "python")["m0.py"]


def test_bash_conventions():
    mod, ids = modgen.gen_module(7, "bash", "T42c", cdom="cdom01", want_state=True, n_files=1)
    lo = modgen.prepare(mod, "bash", ids)
    text = list(R.render_module(lo, "bash").values())[0]
    assert "RET=" in text and "return 0" in text
    assert re.search(r"return 6\d", text)                 # authored status, 64 and up
    assert lo["meta"]["reset_name"] in text
    assert "dirname" not in text and "`" not in text


def test_string_literals_outside_the_portable_charset_are_refused():
    from LC_COMMON import render_base as B
    with pytest.raises(ValueError):
        B.check_str("it's")
    with pytest.raises(ValueError):
        B.check_str('a"b')


# ------------------------------------------------------------------------------------------------ interpreter dialects
def test_division_dialects_and_events():
    mod = I.new_module("x")
    mod["funcs"] = [I.func("f", [["a", I.INT]], I.INT, [I.ret(I.bin_("//", I.v("a"), I.i(3)))]),
                    I.func("g", [["a", I.INT]], I.INT, [I.ret(I.bin_("%", I.v("a"), I.i(3)))])]
    I.check_module(mod)
    assert X.Interp(mod, "python").call("f", [-7]) == ("ok", -3)
    assert X.Interp(mod, "go").call("f", [-7]) == ("ok", -2)
    assert X.Interp(mod, "python").call("g", [-7]) == ("ok", 2)
    assert X.Interp(mod, "javascript").call("g", [-7]) == ("ok", -1)


def test_index_events_flag_non_portable_runs():
    mod = I.new_module("x")
    mod["funcs"] = [I.func("f", [["xs", I.INTS], ["k", I.INT]], I.INT, [I.ret(["idx", I.v("xs"), I.v("k")])])]
    I.check_module(mod)
    it = X.Interp(mod, "python")
    assert it.call("f", [[1, 2], -1]) == ("ok", 2) and "neg_index" in it.events
    it = X.Interp(mod, "go")
    assert it.call("f", [[1, 2], 5]) == ("exc", "IMP_INDEX") and "oob_index" in it.events


def test_step_counter_counts_loop_headers():
    mod = I.new_module("x")
    body = [I.let("t", I.INT, I.i(0)), I.for_("k", I.i(0), I.v("n"), [I.set_("t", I.add(I.v("t"), I.i(1)))]), I.ret(I.v("t"))]
    mod["funcs"] = [I.func("f", [["n", I.INT]], I.INT, body)]
    I.check_module(mod)
    it = X.Interp(mod)
    it.call("f", [4])
    assert it.steps == 1 + (4 + 1) + 4 + 1          # let, 5 loop-header steps, 4 body statements, ret
    it.reset_counters()
    it.call("f", [0])
    assert it.steps == 1 + 1 + 0 + 1


# ------------------------------------------------------------------------------------------------ mutator
def test_operator_partition_is_disjoint_and_complete():
    assert not set(irmut.INJECT_OPS) & set(irmut.STRENGTH_OPS)
    assert set(irmut.INJECT_OPS) | set(irmut.STRENGTH_OPS) == {"MUT-%02d" % k for k in range(1, 15)}
    assert set(irmut.MULTI_OPS) == {"MS-01", "MS-02", "MS-03", "MS-04"}


def test_mutants_are_valid_and_mostly_change_behaviour():
    diff = same = 0
    per_op = {}
    for seed in range(40):
        mod, ids = modgen.gen_module(seed, "python", "T57")
        for f in mod["funcs"]:
            if f["scope"] != "free":
                continue
            dom = mod["meta"]["fns"][f["name"]]["domain"]
            pts = list(D.enumerate_points(dom))
            base = [X.Interp(mod).call(f["name"], p) for p in pts]
            for s, mm in irmut.mutants(mod, irmut.ALL_OPS, {f["name"]}):
                I.check_module(mm)
                out = [X.Interp(mm).call(f["name"], p) for p in pts]
                if out == base:
                    same += 1
                else:
                    diff += 1
                    per_op[s["op"]] = per_op.get(s["op"], 0) + 1
    assert diff > 10 * same
    assert len(per_op) >= 10                         # most of the 14 operator classes are exercised and kill


def test_multi_site_mutation_applies_all_sites():
    rng = random.Random(5)
    hit = 0
    for seed in range(60):
        mod, ids = modgen.gen_module(seed, "python", "T57")
        for ms in irmut.MULTI_OPS:
            site = irmut.multi_sites(mod, ms, rng)
            if site is None:
                continue
            new = irmut.apply_site(mod, site)
            if new is not None:
                hit += 1
                assert len(site["sites"]) >= 2
                assert I.canon(new["funcs"]) != I.canon(mod["funcs"])
    assert hit > 10


# ------------------------------------------------------------------------------------------------ transforms
def test_transforms_preserve_behaviour_over_the_whole_domain():
    applied = {k: 0 for k in T.IDS}
    rng = random.Random(9)
    for seed in range(80):
        mod, ids = modgen.gen_module(seed, "python", "T42c")
        for f in mod["funcs"]:
            if f["scope"] != "free":
                continue
            pts = list(D.enumerate_points(mod["meta"]["fns"][f["name"]]["domain"]))
            base = [X.Interp(mod).call(f["name"], p) for p in pts]
            for eq in T.IDS:
                m2 = T.apply(mod, f["name"], eq, rng, ids, "tf")
                if m2 is None:
                    continue
                applied[eq] += 1
                assert [X.Interp(m2).call(f["name"], p) for p in pts] == base, (seed, f["name"], eq)
    assert all(v > 0 for v in applied.values()), applied


def test_rename_transform_draws_names_from_the_namespace():
    for seed in range(60):
        mod, ids = modgen.gen_module(seed, "python", "T42c", n_pure=1, want_state=False)
        fn = mod["funcs"][0]["name"]
        m2 = T.apply(mod, fn, "EQ-YES-1", random.Random(1), ids, "tf")
        if m2 is None:
            continue
        new_locals = {n[1] for _, n in I.walk(I.functions(m2)[fn]["body"]) if n[0] == "let"}
        old_locals = {n[1] for _, n in I.walk(I.functions(mod)[fn]["body"]) if n[0] == "let"}
        assert new_locals and not (new_locals & old_locals)
        for nm in new_locals:
            assert re.fullmatch(r"[a-z]+", nm)               # namespace 'user' stem
        return
    raise AssertionError("no module with locals found")


# ------------------------------------------------------------------------------------------------ names guard
def test_names_guard_loads_frozen_list_and_enforces_family_lists():
    g = NamesGuard()
    assert "python" in g.allow["language"]
    names = {"policy": [], "tool": [], "language": ["python"], "runner": ["runner.python_isolated"],
             "carrier": ["SRC_FILE", "CALL_SPEC"]}
    assert g.check("T42c", names) == []
    bad = dict(names, runner=["runner.pytest"])           # on the global list, but not a T42c runner
    assert any("NAME_NOT_IN_FAMILY_LIST" in x for x in g.check("T42c", bad))
    bad2 = dict(names, language=["ruby"])
    assert any("NAME_OFF_ALLOWLIST" in x for x in g.check("T42c", bad2))
    with pytest.raises(NamesViolation):
        g.assert_ok("NOPE", names)
    jm = g.job_manifest("job1", "T42c", names)
    assert set(jm["names"]) == {"policy", "tool", "language", "runner", "carrier"}


def test_names_guard_refuses_a_hand_edited_list(tmp_path):
    import json
    from LC_COMMON import paths
    doc = json.load(open(paths.NAMES_MANIFEST))
    doc["names"]["language"].append("ruby")
    p = tmp_path / "edited.json"
    p.write_text(json.dumps(doc))
    with pytest.raises(NamesViolation):
        NamesGuard(manifest_path=str(p))                    # sha differs from the pinned .sha256


def test_wrapper_depth_two_chains_wrappers_with_distinct_names():
    from LC_COMMON import modgen, ir as I
    deep = 0
    for seed in range(25):
        mod, ids = modgen.gen_module(seed, "python", "T57", want_state=False, n_pure=4, force_wrapper=True, wrapper_depth=2)
        I.check_module(mod)
        names = [f["name"] for f in mod["funcs"]]
        assert len(names) == len(set(names))
        calls = [n for f in mod["funcs"] for _, n in I.walk(f["body"]) if n[0] == "fcall"]
        deep += len(calls) >= 4
    assert deep >= 5                                  # most modules really get the second wrapper
