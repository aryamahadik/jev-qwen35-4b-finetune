"""CPU smoke tests of the A/B agreement harness (in-memory rows, test pool, nothing written)."""
import builtins

import pytest

import harness


def test_agreement_smoke_in_memory(monkeypatch):
    writes = []
    real_open = builtins.open

    def spy(path, mode="r", *a, **k):
        if any(c in mode for c in "wax+"):
            writes.append(str(path))
        return real_open(path, mode, *a, **k)
    monkeypatch.setattr(builtins, "open", spy)
    res = harness.run(n=400, seed="t-smoke", blocks=("train",))
    assert not writes, writes
    assert res["pool_kind"] == "test_fixture"
    assert res["rows"] > 300
    assert res["agreement"] >= 0.98
    assert res["b_anomaly_counts"] == {}


def test_truth_tables_t2_sample():
    r = harness.run_truth(("T2",), limit=300)
    assert r["mismatches"] == 0 and r["render_failures"] == 0


def test_truth_table_t3_is_exact():
    """K6(i) rule precedence: all reachable combinations, 0 mismatches (an earlier run recorded 2 mismatches on
    declared_policy without in_scope, a combination the row schema cannot represent; now refused by validate_spec)."""
    r = harness.run_truth(("T3",))
    assert r["pass"] and r["cases"] == 264 and r["mismatches"] == 0 and r["render_failures"] == 0


def test_truth_table_t1_sample_is_exact():
    r = harness.run_truth(("T1",), limit=1500)
    assert r["mismatches"] == 0 and r["render_failures"] == 0
