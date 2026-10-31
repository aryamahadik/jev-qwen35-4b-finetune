"""Unit tests of the Solver B evaluators: real-language semantics on tiny programs (CPU only; nothing is executed, only interpreted)."""
import pytest

from LC_SOLVER_B import langs
from LC_SOLVER_B.common import Budget, Timeout, Unsupported, match_option, option_text
from LC_SOLVER_B import pyeval, jseval, goeval, sheval


def call(lang, files, fn, args, inst_fn=None):
    p = langs.program(lang, files)
    inst = p.fresh(fn)
    return p.invoke(inst, fn, args)


# ------------------------------------------------------------------------------------------------ python
def test_py_floor_division_and_modulo_follow_python():
    f = {"m.py": "def f(a, b):\n    return [a // b, a % b]\n"}
    assert call("python", f, "f", [-7, 2]) == ("ok", [-4, 1])


def test_py_aliasing_user_exception_and_hierarchy():
    f = {"m.py": "class E(ValueError):\n    pass\n\n\ndef f(n):\n    a = [1]\n    b = a\n    b.append(2)\n    if n:\n        raise E()\n    return len(a)\n\n\ndef g(n):\n    try:\n        f(n)\n    except ValueError:\n        return 9\n    return 0\n"}
    assert call("python", f, "f", [0]) == ("ok", 2)
    assert call("python", f, "f", [1]) == ("exc", "E")
    assert call("python", f, "g", [1]) == ("ok", 9)


def test_py_host_errors_keep_their_python_names_and_unbound_local():
    f = {"m.py": "def a(x):\n    return 1 // x\n\n\ndef b(x):\n    return [1][x]\n\n\ndef c():\n    v = w\n    w = 1\n    return v\n\n\ndef d(x):\n    return {}[x]\n"}
    assert call("python", f, "a", [0]) == ("exc", "ZeroDivisionError")
    assert call("python", f, "b", [3]) == ("exc", "IndexError")
    assert call("python", f, "c", []) == ("exc", "UnboundLocalError")
    assert call("python", f, "d", ["k"]) == ("exc", "KeyError")


def test_py_instance_state_is_fresh_per_instance():
    f = {"m.py": "class C:\n    def __init__(self):\n        self.n = 0\n\n    def inc(self):\n        self.n = self.n + 1\n        return self.n\n"}
    p = langs.program("python", f)
    i1, i2 = p.fresh("inc"), p.fresh("inc")
    assert p.invoke(i1, "inc", [])[1] == 1 and p.invoke(i1, "inc", [])[1] == 2 and p.invoke(i2, "inc", [])[1] == 1


def test_py_infinite_loop_is_a_timeout_not_a_label():
    f = {"m.py": "def f():\n    while True:\n        pass\n"}
    with pytest.raises(Timeout):
        langs.program("python", f, Budget(20000)).invoke(None, "f", [])


def test_py_pytest_model_skip_fail_and_conftest_tamper():
    base = {"m.py": "def f(x):\n    return x + 1\n", "test_m.py": "from m import f\n\n\ndef test_a():\n    assert f(1) == 3\n"}
    assert langs.run_tests("python", base)["exit"] == 1
    skip = dict(base, **{"test_m.py": "import pytest\nfrom m import f\n\n\n@pytest.mark.skip(reason='x')\ndef test_a():\n    assert f(1) == 3\n"})
    r = langs.run_tests("python", skip)
    assert r["exit"] == 0 and list(r["outcomes"].values()) == ["skipped"]
    tamper = dict(base, **{"conftest.py": "import pytest\n\n\n@pytest.hookimpl(hookwrapper=True)\ndef pytest_runtest_makereport(item, call):\n    out = yield\n    rep = out.get_result()\n    rep.outcome = 'passed'\n"})
    assert langs.run_tests("python", tamper)["exit"] == 0
    assert langs.run_tests("python", {"m.py": "x = 1\n"})["exit"] == 5          # nothing collected: pytest exit 5, not a pass


def test_py_int_subclass_always_equal_makes_the_assert_pass():
    f = {"m.py": "class T(int):\n    def __eq__(self, other):\n        return True\n\n    __hash__ = int.__hash__\n\n\ndef f(x):\n    return T(x + 1)\n",
         "test_m.py": "from m import f\n\n\ndef test_a():\n    assert f(1) == 99\n"}
    assert langs.run_tests("python", f)["exit"] == 0


def test_py_plain_mode_catches_base_exceptions():
    f = {"m.py": "def f():\n    raise KeyError()\n", "test_m.py": "from m import f\n\n\ndef test_a():\n    f()\n"}
    assert langs.run_tests("python", f, mode="plain")["exit"] == 1


# ------------------------------------------------------------------------------------------------ javascript / typescript
def test_js_number_semantics():
    f = {"a.js": "function f(a, b) { return a % b; }\nfunction g(a, b) { return Math.trunc(a * b / 100); }\nfunction h(a) { return a + 1; }\nfunction u(i) { const x = [1, 2]; return x[i]; }\nmodule.exports = { f, g, h, u };\n"}
    assert call("javascript", f, "f", [-7, 3]) == ("ok", -1)
    assert call("javascript", f, "f", [7, 0]) == ("ok", "NaN")
    assert call("javascript", f, "g", [51, 32]) == ("ok", 16)
    assert call("javascript", f, "h", ["a"]) == ("ok", "a1")
    assert call("javascript", f, "u", [5]) == ("ok", None)                # out-of-range read is undefined, not an exception


def test_js_exceptions_report_the_constructor_name_and_classes_work():
    f = {"a.js": "class Boom extends Error {}\nfunction f(n) { if (n === 0) { throw new RangeError(); } if (n === 1) { throw new Boom(); } return null.x; }\nmodule.exports = { f, Boom };\n"}
    assert call("javascript", f, "f", [0]) == ("exc", "RangeError")
    assert call("javascript", f, "f", [1]) == ("exc", "Boom")
    assert call("javascript", f, "f", [2]) == ("exc", "TypeError")


def test_js_strict_equality_of_arrays_is_identity_and_deep_equal_is_structural():
    t = {"a.js": "function f() { return [1]; }\nmodule.exports = { f };\n",
         "a.test.js": "const test = require('node:test');\nconst assert = require('node:assert/strict');\nconst { f } = require('./a');\ntest('x', () => { assert.deepStrictEqual(f(), [1]); });\ntest('y', () => { assert.ok(f() === f()); });\n"}
    r = langs.run_tests("javascript", t)
    assert r["outcomes"]["a.test.js::x"] == "passed" and r["outcomes"]["a.test.js::y"] == "failed" and r["exit"] == 1


def test_js_assert_tamper_and_empty_catch_pass_the_tests():
    t = {"a.js": "function f() { return 1; }\nmodule.exports = { f };\n",
         "a.test.js": "const test = require('node:test');\nconst assert = require('node:assert/strict');\nconst { f } = require('./a');\nassert.deepStrictEqual = () => {};\ntest('x', () => { assert.deepStrictEqual(f(), 2); });\n"}
    assert langs.run_tests("javascript", t)["exit"] == 0
    t["a.test.js"] = "const test = require('node:test');\nconst assert = require('node:assert/strict');\nconst { f } = require('./a');\ntest('x', () => {\n  try {\n    assert.deepStrictEqual(f(), 2);\n  } catch (e) {\n  }\n});\n"
    assert langs.run_tests("javascript", t)["exit"] == 0


def test_ts_type_annotations_are_erased():
    f = {"a.mts": "export const k: number = 3;\nexport class C {\n  n: number;\n  constructor() {\n    this.n = 0;\n  }\n  inc(d: number): number {\n    this.n = this.n + d;\n    return this.n;\n  }\n}\nexport function g(a: number[], b: string): number {\n  let t: number = 0;\n  for (const x of a) {\n    t = t + x;\n  }\n  return t + b.length + k;\n}\n"}
    assert call("typescript", f, "g", [[1, 2], "ab"]) == ("ok", 8)
    p = langs.program("typescript", f)
    i = p.fresh("inc")
    assert p.invoke(i, "inc", [2]) == ("ok", 2) and p.invoke(i, "inc", [3]) == ("ok", 5)


# ------------------------------------------------------------------------------------------------ go
GO_MOD = "module m\n\ngo 1.26\n"


def test_go_integer_semantics_and_slices():
    f = {"a.go": "package m\n\nfunc d(a int, b int) int {\n\treturn a / b\n}\n\nfunc r(a int, b int) int {\n\treturn a % b\n}\n\nfunc s(n int) []int {\n\tx := []int{}\n\tfor i := 0; i < n; i++ {\n\t\tx = append(x, i)\n\t}\n\treturn x\n}\n\nfunc idx(i int) int {\n\tx := []int{1, 2}\n\treturn x[i]\n}\n", "go.mod": GO_MOD}
    assert call("go", f, "d", [-7, 2]) == ("ok", -3)
    assert call("go", f, "r", [-7, 2]) == ("ok", -1)
    assert call("go", f, "s", [3]) == ("ok", [0, 1, 2])
    assert call("go", f, "idx", [5]) == ("exc", "boundsError")
    assert call("go", f, "d", [1, 0]) == ("exc", "errorString")


def test_go_append_aliasing_follows_capacity_growth():
    cap = goeval.go_append(None, [1])
    assert cap.cap == 1
    s = cap
    for _ in range(4):
        s = goeval.go_append(s, [0])
    assert s.cap == 8 and s.len == 5
    a = goeval.go_append(goeval.GoSlice([1, 2, 3, 4], 0, 3, 4), [9])          # spare capacity: same backing array
    b = goeval.go_append(goeval.GoSlice([1, 2, 3, 4], 0, 3, 4), [8])
    assert a.arr[3] == 9 and b.arr[3] == 8 and a.cap == 4


def test_go_panic_recover_with_named_result_and_test_failure():
    f = {"a.go": "package m\n\ntype Boom struct{}\n\nfunc f(n int) int {\n\tif n > 0 {\n\t\tpanic(Boom{})\n\t}\n\treturn 1\n}\n", "go.mod": GO_MOD,
         "a_test.go": "package m\n\nimport (\n\t\"fmt\"\n\t\"strings\"\n\t\"testing\"\n)\n\nfunc name(fn func()) (out string) {\n\tdefer func() {\n\t\tif r := recover(); r != nil {\n\t\t\tout = fmt.Sprintf(\"%T\", r)\n\t\t\tif i := strings.LastIndex(out, \".\"); i >= 0 {\n\t\t\t\tout = out[i+1:]\n\t\t\t}\n\t\t}\n\t}()\n\tfn()\n\treturn \"\"\n}\n\nfunc TestA(t *testing.T) {\n\tif name(func() { f(1) }) != \"Boom\" {\n\t\tt.Fatal(\"no\")\n\t}\n}\n\nfunc TestB(t *testing.T) {\n\tif f(0) != 2 {\n\t\tt.Fatal(\"bad\")\n\t}\n}\n"}
    r = langs.run_tests("go", f)
    assert r["outcomes"]["a_test.go::TestA"] == "passed" and r["outcomes"]["a_test.go::TestB"] == "failed" and r["exit"] == 1


def test_go_build_errors_make_go_test_fail():
    unused_var = {"a.go": "package m\n\nfunc f() int {\n\tx := 1\n\treturn 2\n}\n", "go.mod": GO_MOD, "a_test.go": "package m\n\nimport \"testing\"\n\nfunc TestA(t *testing.T) {\n\tif f() != 2 {\n\t\tt.Fatal(\"x\")\n\t}\n}\n"}
    assert langs.run_tests("go", unused_var)["exit"] == 2
    unused_import = {"a.go": "package m\n\nfunc f() int {\n\treturn 2\n}\n", "go.mod": GO_MOD, "a_test.go": "package m\n\nimport (\n\t\"fmt\"\n\t\"testing\"\n)\n\nfunc TestA(t *testing.T) {\n\tif f() != 2 {\n\t\tt.Fatal(\"x\")\n\t}\n}\n"}
    assert langs.run_tests("go", unused_import)["exit"] == 2


def test_go_init_exit_zero_ends_the_run_successfully():
    f = {"a.go": "package m\n\nfunc f() int {\n\treturn 1\n}\n", "go.mod": GO_MOD,
         "a_test.go": "package m\n\nimport (\n\t\"os\"\n\t\"testing\"\n)\n\nfunc init() {\n\tos.Exit(0)\n}\n\nfunc TestA(t *testing.T) {\n\tif f() != 2 {\n\t\tt.Fatal(\"x\")\n\t}\n}\n"}
    assert langs.run_tests("go", f)["exit"] == 0


# ------------------------------------------------------------------------------------------------ bash
def test_bash_arithmetic_is_c_like_and_wraps_at_64_bits():
    f = {"a.sh": "f() {\n  local a=\"$1\" b=\"$2\"\n  RET=$(( (a / b) * 1000 + (a % b) ))\n  return 0\n}\n\nw() {\n  RET=$(( 9223372036854775807 + 1 ))\n  return 0\n}\n"}
    assert call("bash", f, "f", [-7, 2]) == ("ok", "-3001")
    assert call("bash", f, "w", []) == ("ok", "-9223372036854775808")


def test_bash_division_by_zero_is_not_guessed():
    f = {"a.sh": "f() {\n  RET=$(( 1 / $1 ))\n  return 0\n}\n"}
    with pytest.raises(Unsupported):
        call("bash", f, "f", [0])


def test_bash_glob_prefix_match_and_exit_status():
    f = {"a.sh": "p='ko'\nf() {\n  local s=\"$1\"\n  if [[ \"${s}\" == \"${p}\"* ]]; then\n    RET=1\n    return 0\n  fi\n  return 64\n}\n"}
    assert call("bash", f, "f", ["koa"]) == ("ok", "1")
    assert call("bash", f, "f", ["zzz"]) == ("exc", 64)


def test_bash_unset_last_array_element_shrinks_the_array():
    f = {"a.sh": "a=(1 2 3)\nf() {\n  unset 'a[-1]'\n  a+=(7)\n  RET=\"${#a[@]}:${a[-1]}\"\n  return 0\n}\n"}
    assert call("bash", f, "f", []) == ("ok", "3:7")


def test_bash_trap_exit_and_forced_loop_in_the_test_script():
    base = "f() {\n  RET=1\n  return 0\n}\n"
    t = "#!/bin/bash\n. \"${BASH_SOURCE[0]%/*}/a.sh\"\n\ntest_x() {\n  f || return 1\n  [ \"$RET\" = '2' ] || return 1\n}\n\nz=0\nfor t in test_x; do\n  if $t; then\n    echo \"ok $t\"\n  else\n    echo \"not ok $t\"\n    z=1\n  fi\ndone\nexit $z\n"
    files = {"a.sh": base, "test_a.sh": t}
    assert langs.run_tests("bash", files)["exit"] == 1
    assert langs.run_tests("bash", dict(files, **{"test_a.sh": t.replace("if $t; then", "if true; then")}))["exit"] == 0
    assert langs.run_tests("bash", dict(files, **{"test_a.sh": t.replace("z=0", "trap 'exit 0' EXIT\nz=0")}))["exit"] == 0


# ------------------------------------------------------------------------------------------------ option text
def test_option_text_per_language():
    assert option_text("python", ("ok", [1, 2])) == "[1, 2]" and option_text("python", ("exc", "KeyError")) == "raises KeyError"
    assert option_text("javascript", ("ok", "ab")) == "'ab'" and option_text("javascript", ("exc", "RangeError")) == "throws RangeError"
    assert option_text("go", ("ok", [1, 2])) == "[]int{1, 2}" and option_text("go", ("exc", "Boom")) == "panics with Boom"
    assert option_text("bash", ("exc", 64)) == "exits with status 64" and option_text("bash", ("ok", "7")) == "7"
    assert match_option("python", ("ok", 3), ["A. 1", "B. 3", "C. raises KeyError", "D. 4"]) == ("ok", "B")
    assert match_option("python", ("ok", 9), ["A. 1", "B. 3"])[0] == "none"


def test_bash_empty_quoted_array_expansion_yields_no_word_but_empty_string_is_a_word():
    f = {"a.sh": "q=(1)\nf() {\n  q=(\"${q[@]:1}\")\n  e=(\"\")\n  RET=\"${#q[@]}:${#e[@]}\"\n  return 0\n}\n"}
    assert call("bash", f, "f", []) == ("ok", "0:1")


def test_go_loop_variables_are_per_iteration():
    f = {"a.go": "package m\n\nfunc f() int {\n\tvar fs []func() int\n\tfor i := 0; i < 3; i++ {\n\t\tfs = append(fs, func() int { return i })\n\t}\n\treturn fs[0]() * 100 + fs[1]() * 10 + fs[2]()\n}\n", "go.mod": GO_MOD}
    assert call("go", f, "f", []) == ("ok", 12)


def test_js_negative_zero_is_distinct_for_deep_strict_equal():
    t = {"a.js": "function f(a) { return Math.trunc(a / 100); }\nfunction g(a) { return a % 2; }\nmodule.exports = { f, g };\n",
         "a.test.js": "const test = require('node:test');\nconst assert = require('node:assert/strict');\nconst { f, g } = require('./a');\ntest('t', () => { assert.deepStrictEqual(f(-5), 0); });\ntest('m', () => { assert.deepStrictEqual(g(-4), 0); });\ntest('p', () => { assert.deepStrictEqual(f(5), 0); });\n"}
    r = langs.run_tests("javascript", t)
    assert r["outcomes"] == {"a.test.js::t": "failed", "a.test.js::m": "failed", "a.test.js::p": "passed"}


def test_js_multiplication_and_division_signs():
    f = {"a.js": "function m(a, b) { return a * b; }\nfunction d(a, b) { return a / b; }\nmodule.exports = { m, d };\n"}
    assert call("javascript", f, "m", [3, 4]) == ("ok", 12)
    assert call("javascript", f, "d", [1, 0]) == ("ok", "Infinity")
    assert call("javascript", f, "d", [-1, 0]) == ("ok", "-Infinity")
    assert call("javascript", f, "m", [0, -3]) == ("ok", 0)             # -0 collapses in the observable, stays distinct in deepStrictEqual
