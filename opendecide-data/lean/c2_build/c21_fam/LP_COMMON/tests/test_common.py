"""LP_COMMON CPU tests: util, ladder, names, PyEval subset, executor interface."""
import pytest

from LP_COMMON import plan, pyeval, sandbox_iface as S, util
from LP_COMMON.ns import Names


def test_largest_remainder_sums():
    out = util.largest_remainder(100, {"a": 0.2, "b": 0.3, "c": 0.3, "d": 0.2})
    assert sum(out.values()) == 100


def test_ladder_levels():
    assert plan.ladder_level(0, 0) == "L1"
    assert plan.ladder_level(1, 0) == "L2"
    assert plan.ladder_level(0, 1) == "L3" and plan.ladder_level(2, 0) == "L3"
    assert plan.ladder_level(0, 2) == "L4"


def test_names_deterministic_and_unique():
    a = Names("TX", "s1")
    b = Names("TX", "s1")
    assert a.unique("ns.variable", "k1") == b.unique("ns.variable", "k1")
    assert a.unique("ns.variable", "k2") != a.unique("ns.variable", "k1")


def test_pyeval_runs_and_refuses():
    m = pyeval.Module("m", {"m.py": "def f(x):\n    return x + 1\n"})
    assert m.call("f", 2) == 3
    with pytest.raises(pyeval.Unsupported):
        pyeval.Module("m", {"m.py": "import socket\n"})


def test_sim_executor_calls_marker():
    ex = S.SimExecutor()
    res = ex.run([S.calls_request("r1", {"m.py": "def f(x):\n    return x * 2\n"}, "m", [("f", [4], {})])])[0]
    assert S.parse_marker(res["stdout"]) == [["ok", 8]] and S.witness_ok(res)
