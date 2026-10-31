import json
import pytest

from oc1 import common as C


def test_rates_match_modal_billing():
    # modal billing rates 17 Oct 2026: H100 3.95, cpu 0.0473/core, 0.008/GiB
    r = C.container_rate_usd_h("H100!", 4, 24)
    assert abs(r - (3.95 + 4 * 0.0473 + 24 * 0.008)) < 1e-9
    assert abs(C.container_rate_usd_h(None, 2, 8) - (2 * 0.0473 + 8 * 0.008)) < 1e-9
    assert C.container_rate_usd_h("H100", 4, 24, "us") == pytest.approx(r * 1.25)
    assert C.container_rate_usd_h("H100", 4, 24, "us-east") == pytest.approx(r * 1.75)
    with pytest.raises(ValueError):
        C.container_rate_usd_h("Z9000", 1, 1)


def test_budget_thresholds_and_ledger(tmp_path):
    t = [1000.0]
    b = C.Budget(path=tmp_path / "l.json", clock=lambda: t[0], overhead_s=0.0)
    assert b.can_launch(4.5) and not b.can_launch(4.51)
    b.open("gpu", 3.6)           # USD 3.6 / h
    t[0] += 3600
    assert b.spent() == pytest.approx(3.6)
    assert not b.must_cancel()
    t[0] += 1200                 # +1.2 -> 4.8
    assert b.must_cancel()
    assert not b.can_launch(0.01)
    usd = b.close("gpu")         # elapsed
    assert usd == pytest.approx(4.8)
    b2 = C.Budget(path=tmp_path / "l.json", clock=lambda: t[0], overhead_s=0.0)   # a new process sees the ledger
    assert b2.spent() == pytest.approx(4.8)
    with pytest.raises(C.BudgetExceeded):
        b2.check_launch("x", 0.01)


def test_budget_uses_container_seconds_not_elapsed(tmp_path):
    t = [0.0]
    b = C.Budget(path=tmp_path / "l.json", clock=lambda: t[0], overhead_s=45.0)
    b.open("a", 3.6)
    t[0] = 600
    assert b.close("a", seconds=100) == pytest.approx((100 + 45) / 3600 * 3.6)


def test_payer_guard():
    ok = {"MODAL_PROFILE": "jaypatil-duke"}
    assert C.payer_guard(env=ok, argv=["/x/modal", "run", "a.py"], active="jaypatil-duke") == "jaypatil-duke"
    for bad in ("mahadikarya2", "mahadikarya3", "mahadikarya44", "aryamhd", "other"):
        with pytest.raises(SystemExit):
            C.payer_guard(env={"MODAL_PROFILE": bad}, argv=["/x/modal", "run", "a.py"], active=bad)
    with pytest.raises(SystemExit):
        C.payer_guard(env={}, argv=["/x/modal", "run", "a.py"], active="x")                       # no explicit profile
    with pytest.raises(SystemExit):
        C.payer_guard(env={**ok, "MODAL_TOKEN_ID": "x"}, argv=["/x/modal", "run"], active="jaypatil-duke")
    with pytest.raises(SystemExit):
        C.payer_guard(env=ok, argv=["/x/modal", "deploy", "a.py"], active="jaypatil-duke")
    with pytest.raises(SystemExit):
        C.payer_guard(env=ok, argv=["/x/modal", "run", "a.py", "--detach"], active="jaypatil-duke")
    with pytest.raises(SystemExit):
        C.payer_guard(env=ok, argv=["/x/modal", "run", "a.py"], active="mahadikarya3")           # active profile differs


@pytest.mark.parametrize("p", ["data/ohs3_x.jsonl", "/a/OHS/b", "c_spec/sealed_brief/x", "/q/sealed_nd/y", "c_build/preread/z",
                               "bench/external_quarantine/a", "bench/longbench_v2/b", "/Users/x/.claude/projects/m.md"])
def test_forbidden_paths(p):
    assert C.path_problem(p)
    with pytest.raises(SystemExit):
        C.safe_path(p)


def test_allowed_paths_and_splits():
    assert C.path_problem("/Users/aryamahadik/Documents/jev/opendecide-data/lean/speed/opt_c1_20261017/data/P.jsonl") is None
    assert C.split_ok("dev_nc") and not C.split_ok("ohs3_dev") and not C.split_ok("jev_out")


def test_stats():
    xs = list(range(1, 101))
    assert C.pct(xs, 0.5) == 51 and C.pct(xs, 0.99) == 100
    s = C.summarize([1.0, 2.0, 3.0, None, float("nan")])
    assert s["n"] == 3 and s["p50"] == 2.0
