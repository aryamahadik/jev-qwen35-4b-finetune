import numpy as np

from LA_COMMON import probe


def _data(n=900, leak=False, seed=0):
    rng = np.random.default_rng(seed)
    groups = [i // 3 for i in range(n)]
    y = [int(rng.random() < 0.5) for _ in range(n)]
    fd = [{"a": float(rng.normal()), "b": float(rng.normal()), "c": float(rng.integers(0, 5))} for _ in range(n)]
    if leak:
        fd = [dict(d, leak=yy + 0.3 * float(rng.normal())) for d, yy in zip(fd, y)]
    return fd, y, groups


def test_noise_passes_and_the_run_is_valid():
    fd, y, g = _data()
    r = probe.binary_probe(fd, y, g, n_boot=200)
    assert r["valid"] and r["auc"] <= 0.55 and r["ub"] <= 0.60 and r["pass"]
    assert abs(r["perm_auc"] - 0.5) <= 0.03 and r["leak_auc"] >= 0.80


def test_a_planted_leak_fails_the_bar():
    fd, y, g = _data(leak=True)
    r = probe.binary_probe(fd, y, g, n_boot=200)
    assert r["valid"] and r["auc"] > 0.9 and not r["pass"]


def test_kway_balanced_accuracy_bar():
    fd, _, g = _data()
    rng = np.random.default_rng(5)
    y3 = [int(rng.integers(0, 3)) for _ in fd]
    r = probe.kway_probe(fd, y3, g, n_boot=200)
    assert r["k"] == 3 and r["valid"] and r["pass"] and r["bal_acc"] <= 1 / 3 + 0.03
    fdl = [dict(d, leak=float(v)) for d, v in zip(fd, y3)]
    assert not probe.kway_probe(fdl, y3, g, n_boot=200)["pass"]


def test_auc_is_folded_and_split_is_grouped():
    assert abs(probe.fast_auc(np.array([0.1, 0.2, 0.8, 0.9]), np.array([1, 1, 0, 0])) - 0.0) < 1e-9
    fd, y, g = _data(300)
    for tr, te in probe._splits(np.asarray(g), 0):
        assert not (set(np.asarray(g)[tr]) & set(np.asarray(g)[te]))
    r = probe.binary_probe(fd, [1 - v for v in y], g, n_boot=100)
    assert r["auc"] >= 0.5                                           # folded


def test_run_valid_repeats_an_invalid_run():
    calls = []

    def fake(seed=0):
        calls.append(seed)
        return {"valid": len(calls) >= 3}
    assert probe.run_valid(fake)["attempts"] == 3
