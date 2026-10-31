"""The evaluator: Python semantics of the supported subset, one fixture per rule."""
import pytest

from T66.solver_b import pyi


def run(mod_src, test_src, stem="m"):
    return pyi.run_suite(pyi.World({stem: mod_src}), test_src)


def passes(mod_src, test_src):
    r = run(mod_src, test_src)
    assert r.status in ("pass", "fail"), r.detail
    return r.ok


def test_arithmetic_floor_div_mod_follow_python():
    m = "def f(a, b):\n    return (a // b, a % b, a * b - 1)\n"
    assert passes(m, "from m import f\ndef test_x():\n    assert f(-7, 2) == (-4, 1, -15)\n")


def test_defaults_evaluated_at_definition_time_and_shared():
    m = "def f(a, acc=[]):\n    acc.append(a)\n    return len(acc)\n"
    assert passes(m, "from m import f\ndef test_x():\n    assert f(1) == 1\n    assert f(2) == 2\n")


def test_binding_errors_are_type_errors():
    m = "def f(a, b=2):\n    return a + b\n"
    t = "from m import f\ndef test_x():\n    try:\n        f()\n    except TypeError:\n        pass\n    else:\n        assert False\n    try:\n        f(1, c=3)\n    except TypeError:\n        pass\n    else:\n        assert False\n    try:\n        f(1, 2, 3)\n    except TypeError:\n        pass\n    else:\n        assert False\n    try:\n        f(1, a=1)\n    except TypeError:\n        return\n    assert False\n"
    assert passes(m, t)


def test_keyword_and_positional_mix():
    m = "def f(a, b=2, c=3):\n    return a * 100 + b * 10 + c\n"
    assert passes(m, "from m import f\ndef test_x():\n    assert f(1, c=9) == 129\n    assert f(b=5, a=1) == 153\n")


def test_exception_hierarchy():
    m = "def f(k):\n    if k == 1:\n        raise KeyError('k')\n    raise ValueError('v')\n"
    ok = "from m import f\ndef test_x():\n    try:\n        f(1)\n    except LookupError:\n        pass\n    try:\n        f(2)\n    except Exception:\n        return\n    assert False\n"
    assert passes(m, ok)
    bad = "from m import f\ndef test_x():\n    try:\n        f(1)\n    except ValueError:\n        return\n"
    assert not passes(m, bad)                 # a KeyError is not a ValueError: the test errors


def test_user_exception_class_is_caught_by_base():
    m = "class E(ValueError):\n    pass\ndef f():\n    raise E('x')\n"
    assert passes(m, "from m import f\ndef test_x():\n    try:\n        f()\n    except ValueError:\n        return\n    assert False\n")


def test_unpack_count_mismatch_is_value_error_and_dict_unpacks_keys():
    m = "def f():\n    return {'value': 1, 'ok': True}\ndef g():\n    return (1, 2, 3)\n"
    t = "from m import f, g\ndef test_x():\n    a, b = f()\n    assert a == 'value' and b == 'ok'\n    try:\n        x, y = g()\n    except ValueError:\n        return\n    assert False\n"
    assert passes(m, t)


def test_import_of_missing_name_fails_collection():
    r = run("def f():\n    return 1\n", "from m import g\ndef test_x():\n    assert g() == 1\n")
    assert r.status == "fail" and "collection" in r.detail


def test_syntax_error_in_module_fails():
    r = run("def f(:\n    pass\n", "from m import f\ndef test_x():\n    assert f()\n")
    assert r.status == "fail"


def test_unbound_local_and_name_error():
    m = "def f():\n    x = x + 1\n    return x\ndef g():\n    return nope\n"
    t = "from m import f, g\ndef test_x():\n    try:\n        f()\n    except NameError:\n        pass\n    try:\n        g()\n    except NameError:\n        return\n    assert False\n"
    assert passes(m, t)


def test_closure_and_lambda_and_comprehension():
    m = "def mk(n):\n    def add(x):\n        return x + n\n    return add\ndef sq(xs):\n    return [x * x for x in xs if x > 1]\nK = lambda a, b=2: a * b\n"
    t = "from m import mk, sq, K\ndef test_x():\n    assert mk(3)(4) == 7\n    assert sq([1, 2, 3]) == [4, 9]\n    assert K(5) == 10\n"
    assert passes(m, t)


def test_for_while_break_continue_else():
    m = "def f(n):\n    t = 0\n    for i in range(n):\n        if i == 2:\n            continue\n        if i == 5:\n            break\n        t += i\n    else:\n        t = -1\n    return t\ndef w():\n    i = 0\n    while i < 3:\n        i += 1\n    return i\n"
    assert passes(m, "from m import f, w\ndef test_x():\n    assert f(4) == -1\n    assert f(9) == 0 + 1 + 3 + 4\n    assert w() == 3\n")


def test_dict_list_subscript_and_methods():
    m = "T = {'a': 1}\ndef f(k):\n    return T[k]\ndef g():\n    xs = []\n    xs.append(3)\n    xs.extend([4, 5])\n    return xs[1:], xs[-1], ','.join(['x', 'y'])\n"
    t = "from m import f, g\ndef test_x():\n    assert f('a') == 1\n    try:\n        f('zz')\n    except KeyError:\n        pass\n    assert g() == ([4, 5], 5, 'x,y')\n"
    assert passes(m, t)


def test_class_instances_and_init():
    m = "class C:\n    def __init__(self, v):\n        self.v = v\n    def get(self):\n        return self.v * 2\n"
    assert passes(m, "from m import C\ndef test_x():\n    assert C(4).get() == 8\n")


def test_fstring_and_format():
    m = "def f(n):\n    return f'{n:03d}-{n}'\n"
    assert passes(m, "from m import f\ndef test_x():\n    assert f(7) == '007-7'\n")


def test_infinite_loop_is_unsupported_not_a_hang():
    m = "def f():\n    while True:\n        pass\n"
    r = run(m, "from m import f\ndef test_x():\n    f()\n")
    assert r.status == "unsupported"


def test_unsupported_construct_abstains():
    m = "import os\ndef f():\n    return 1\n"
    r = run(m, "from m import f\ndef test_x():\n    assert f() == 1\n")
    assert r.status == "unsupported"
    r2 = run("def f():\n    with open('x') as h:\n        return 1\n", "from m import f\ndef test_x():\n    f()\n")
    assert r2.status == "unsupported"


def test_check_syntax_extras():
    assert pyi.check_syntax("return 1\n")
    assert pyi.check_syntax("break\n")
    assert pyi.check_syntax("def f(a, a):\n    pass\n")
    assert pyi.check_syntax("def f():\n    return 1\n") is None
    assert pyi.check_syntax("<<<<<<< ours\nx = 1\n") is not None


def test_test_failures_counted_individually():
    m = "def f(x):\n    return x\n"
    r = run(m, "from m import f\ndef test_a():\n    assert f(1) == 1\ndef test_b():\n    assert f(1) == 2\ndef test_c():\n    assert f(3) == 3\n")
    assert (r.status, r.passed, r.failed) == ("fail", 2, 1)


def test_module_state_shared_between_tests_in_order():
    m = "N = []\ndef f():\n    N.append(1)\n    return len(N)\n"
    assert passes(m, "from m import f\ndef test_a():\n    assert f() == 1\ndef test_b():\n    assert f() == 2\n")
