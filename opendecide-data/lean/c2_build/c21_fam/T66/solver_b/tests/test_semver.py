import pytest

from T66.solver_b import semver_b
from helpers import semver_ctx

OLD = "def f(a, b=2, c=0):\n    if a < -5:\n        raise ValueError('r')\n    return {'value': a * 4 + b + c, 'ok': True}\n"
CALLERS = ("from m import f\n\ndef test_c1():\n    assert f(2, 5)['value'] == 13\n\ndef test_c2():\n    assert f(2, b=5)['value'] == 13\n\n"
           "def test_c3():\n    try:\n        f(-9, 1)\n    except ValueError:\n        return\n    assert False\n")


def solve(new, callers=CALLERS, old=OLD, bump=None):
    return semver_b.solve(semver_ctx("m", old, new, callers, bump))


def test_identical_is_safe_and_bump_is_ignored():
    for b in (None, "patch", "minor", "major"):
        assert solve(OLD, bump=b)[0] == "SAFE"


def test_c1_rename_param_used_by_keyword_breaks():
    assert solve(OLD.replace("b=2", "bb=2").replace("+ b +", "+ bb +"))[0] == "BREAKING"
    assert solve(OLD.replace("c=0", "cc=0").replace("+ c,", "+ cc,"))[0] == "SAFE"        # the renamed parameter is not used by name in any caller


def test_c2_reorder_params():
    new = OLD.replace("def f(a, b=2, c=0)", "def f(b, a, c=0)")
    assert solve(new)[0] == "BREAKING"


def test_c3_new_required_param_breaks_but_new_optional_is_safe():
    assert solve(OLD.replace("c=0)", "c=0, d)"))[0] is not None
    req = "def f(a, b=2, c=0, *, d):\n    return {'value': a * 4 + b + c, 'ok': True}\n"
    assert solve(req)[0] == "BREAKING"
    opt = OLD.replace("c=0)", "c=0, d=1)")
    assert solve(opt)[0] == "SAFE"


def test_c5_changed_default_breaks_only_when_a_caller_relies_on_it():
    new = OLD.replace("b=2", "b=3")
    callers_rel = CALLERS + "\ndef test_c4():\n    assert f(1)['value'] == 6\n"
    assert solve(new)[0] == "SAFE"                       # every shown caller passes b explicitly
    assert solve(new, callers=callers_rel)[0] == "BREAKING"


def test_c6_return_shape_changed():
    new = OLD.replace("{'value': a * 4 + b + c, 'ok': True}", "(a * 4 + b + c, True)")
    assert solve(new)[0] == "BREAKING"


def test_c7_exception_class_changed():
    assert solve(OLD.replace("ValueError", "KeyError"))[0] == "BREAKING"


def test_c8_edge_input_changed_only_if_shown():
    new = OLD.replace("    return {", "    if a == 0:\n        return {'value': 99, 'ok': True}\n    return {")
    assert solve(new)[0] == "SAFE"
    assert solve(new, callers=CALLERS + "\ndef test_c4():\n    assert f(0)['value'] == 2\n")[0] == "BREAKING"


def test_c9_function_removed_or_moved():
    moved = OLD.replace("def f(", "def g(")
    label, why = solve(moved)
    assert label == "BREAKING"
    assert solve(moved + "f = g\n")[0] == "SAFE"       # alias keeps the old name importable (C12)


def test_c10_stricter_validation_only_breaks_a_shown_value():
    new = OLD.replace("a < -5", "a < 0")
    assert solve(new)[0] == "SAFE"
    assert solve(new, callers=CALLERS + "\ndef test_c4():\n    assert f(-3, 2)['value'] == -10\n")[0] == "BREAKING"


def test_c11_refactor_is_safe():
    new = OLD.replace("a * 4 + b + c", "c + b + a * 4")
    assert solve(new)[0] == "SAFE"


def test_binding_rule_table():
    sig = semver_b.signature(__import__("ast").parse("def f(a, b=1, *, k, j=2):\n    pass\n").body[0])
    assert semver_b.binds(sig, 1, ["k"])
    assert not semver_b.binds(sig, 1, [])               # k is required
    assert not semver_b.binds(sig, 3, ["k"])            # too many positionals
    assert not semver_b.binds(sig, 1, ["k", "zz"])      # unknown keyword
    assert not semver_b.binds(sig, 1, ["k", "a"])       # a given twice
    assert semver_b.binds(sig, 2, ["k", "j"])


def test_old_api_failing_a_caller_abstains():
    label, why = solve(OLD, callers=CALLERS + "\ndef test_c9():\n    assert f(1)['value'] == 12345\n")
    assert label is None and "old API" in why


def test_unsupported_abstains():
    label, why = solve("import os\n" + OLD)
    assert label is None
