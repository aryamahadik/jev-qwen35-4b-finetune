"""fastcore.batcher on CPU with fake runners: the sub-batch former (DP == brute force), flags (aliases, validation,
legacy override, runtime switch), many-thread concurrency with results routed back to the right request, error
isolation, worker death, shutdown with queued requests (no hang), batch_wait_ms, timing fields.

  cd ~/Documents/jev/opendecide-data/lean && ../.venv/bin/python -m pytest hosting/tests/test_fastcore_batcher.py -q
No GPU, no model, no network.
"""
import itertools
import random
import sys
import threading
import time
from concurrent.futures import TimeoutError as FutTimeout
from pathlib import Path

import pytest
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastcore import batcher as Bm  # noqa: E402
from fastcore import graphs as G  # noqa: E402
from fastcore.readout import WorkItem  # noqa: E402

POISON = -7
CUDA_TAG = -13  # a row whose forward fails as a poisoned CUDA context does
SHAPES = G.boot_shapes()
LEGACY = G.legacy_shapes()


class Boom(BaseException):
    """Not an Exception: kills the worker thread (as a KeyboardInterrupt would)."""


class FakeRunner:
    def __init__(self, delay=0.002, gate=None):
        self.delay, self.gate = delay, gate
        self.calls, self.active, self.max_active = [], 0, 0
        self.attempts = []  # the first id (tag) of every row of every run() call, successful or not
        self.lock = threading.Lock()

    def select(self, k, m, legacy=False, token_budget=None):
        return G.select_legacy(k, m, LEGACY) if legacy else G.select_new(k, m, SHAPES, token_budget)

    def run(self, seqs, cands, shape, readout="exact"):
        with self.lock:
            self.active += 1
            self.max_active = max(self.max_active, self.active)
            self.attempts.append(tuple(s[0] for s in seqs))
        try:
            if self.gate is not None:
                assert self.gate.wait(10)
            time.sleep(self.delay)
            if any(s and s[0] == -99 for s in seqs):
                raise Boom()
            if any(POISON in s for s in seqs):
                raise ValueError("poisoned row")
            if any(CUDA_TAG in s for s in seqs):
                raise RuntimeError("CUDA error: an illegal memory access was encountered")
            if shape is not None:
                assert len(seqs) <= shape[0] and max(len(s) for s in seqs) <= shape[1]
            self.calls.append((len(seqs), shape, readout))
            return [torch.tensor([float(sum(s)), float(len(s))]) for s in seqs], ("graph" if shape else "eager")
        finally:
            with self.lock:
                self.active -= 1


def item(n, tag, q=0, view=0):
    ids = [tag] + [1] * (n - 1)
    return WorkItem(q=q, view=view, perm=None, text="t", groups=[[1], [2]], ids=ids, n_tokens=n, flat=[1, 2],
                    sizes=[1, 1])


def expect(it):
    return [float(sum(it.ids)), float(len(it.ids))]


# ------------------------------------------------------------------ plan_batches
COST = {"cost_call_ms": 4.0, "cost_token_ms": 0.02, "cost_eager_ms": 40.0}


def _cost(groups, lengths):
    c = 0.0
    for idx, shape in groups:
        if shape is not None:
            c += COST["cost_call_ms"] + COST["cost_token_ms"] * shape[0] * shape[1]
        else:
            c += COST["cost_eager_ms"] + COST["cost_token_ms"] * len(idx) * G.eager_len(max(lengths[i] for i in idx))
    return c


def _brute(lengths, sel, max_rows, budget):
    order = sorted(range(len(lengths)), key=lambda i: (lengths[i], i))
    best = None
    n = len(order)
    for cuts in itertools.product([0, 1], repeat=n - 1):
        groups, cur = [], [order[0]]
        for c, x in zip(cuts, order[1:]):
            if c:
                groups.append(cur)
                cur = [x]
            else:
                cur.append(x)
        groups.append(cur)
        plan, ok = [], True
        for g in groups:
            k, m = len(g), max(lengths[i] for i in g)
            if k > max_rows:
                ok = False
                break
            shp = sel(k, m)
            if shp is not None and (k == 1 or shp[0] * shp[1] <= budget):
                plan.append((g, shp))
            elif k == 1 or k * G.eager_len(m) <= budget:
                plan.append((g, None))
            else:
                ok = False
                break
        if ok:
            c = _cost(plan, lengths)
            best = c if best is None else min(best, c)
    return best


def test_plan_batches_basic():
    sel = lambda k, m: G.select_new(k, m, SHAPES, 8192)
    g = Bm.plan_batches([100] * 16, sel, 16, 8192, COST)
    assert g == [(list(range(16)), (16, 128))]
    g = Bm.plan_batches([100, 3000], sel, 16, 8192, COST)
    assert [x[1] for x in g] == [(1, 128), (1, 3072)]
    g = Bm.plan_batches([5000, 120, 6000], sel, 16, 8192, COST)
    assert g[0] == ([1], (1, 128)) and [x[1] for x in g[1:]] == [None, None]  # > 4096: eager, one row each
    g = Bm.plan_batches([300, 290], sel, 16, 8192, COST)
    assert g == [([1, 0], (2, 320))]
    assert sorted(i for idx, _ in Bm.plan_batches(list(range(1, 40)), sel, 16, 8192, COST) for i in idx) == list(range(39))
    assert all(len(idx) <= 4 for idx, _ in Bm.plan_batches([50] * 20, sel, 4, 8192, COST))


def test_plan_batches_is_optimal_vs_brute_force():
    rng = random.Random(0)
    for legacy in (False, True):
        sel = (lambda k, m: G.select_legacy(k, m, LEGACY)) if legacy else (lambda k, m: G.select_new(k, m, SHAPES, 4096))
        for _ in range(150):
            n = rng.randint(1, 8)
            lengths = [rng.choice([rng.randint(1, 600), rng.randint(600, 2500), rng.randint(2500, 6000)]) for _ in range(n)]
            mr = rng.choice([2, 4, 16])
            got = Bm.plan_batches(lengths, sel, mr, 4096, COST)
            assert sorted(i for idx, _ in got for i in idx) == list(range(n))
            assert all(len(idx) <= mr for idx, _ in got)
            assert abs(_cost(got, lengths) - _brute(lengths, sel, mr, 4096)) < 1e-9, (lengths, mr, legacy)


# ------------------------------------------------------------------ flags
def test_flags_aliases_validation_and_legacy():
    f = Bm.normalize_flags({"batching": False, "two_pass_2view": True, "legacy_graphs": True, "max_wait_ms": 2,
                            "tokenize_in_worker": True})
    assert f["cross_batch"] is False and f["graph_plan"] == "legacy" and f["batch_wait_ms"] == 2.0
    assert f["tokenize_outside_lock"] is False
    v = Bm.flags_view(f)
    assert v["batching"] is False and v["legacy_graphs"] is True and v["max_wait_ms"] == 2.0 and v["tokenize_in_worker"]
    for bad in ({"nope": 1}, {"legacy": 1}, {"graph_plan": "x"}, {"max_rows": 0}, {"max_rows": 2.5}, {"token_budget": 10},
                {"batch_wait_ms": -1}, {"readout": "fast"}, {"choice_views": 3}, {"legacy_graphs": "yes"}):
        with pytest.raises(ValueError):
            Bm.normalize_flags(bad)
    e = Bm.effective_flags(Bm.normalize_flags({"legacy": True}))
    assert (e["cross_batch"], e["twoview_split"], e["graph_plan"], e["tokenize_outside_lock"]) == (False, False, "legacy", False)
    e = Bm.effective_flags(Bm.normalize_flags({"twoview_split": False, "cross_batch": True}))
    assert e["cross_batch"] is False
    for arm, fl in Bm.ARM_FLAGS.items():  # every arm's flags read back unchanged (speed_arms.json contract)
        v = Bm.flags_view(Bm.normalize_flags(fl))
        assert all(v[k] == x for k, x in fl.items()), arm


def test_set_flags_all_or_nothing():
    eng = Bm.BatchingEngine(FakeRunner())
    try:
        before = eng.flags
        with pytest.raises(ValueError):
            eng.set_flags({"cross_batch": False, "max_rows": 999})
        assert eng.flags == before
        v = eng.set_flags({"cross_batch": False})
        assert v["cross_batch"] is False and v["batching"] is False and eng.flags["cross_batch"] is False
    finally:
        eng.shutdown()


# ------------------------------------------------------------------ concurrency
def _hammer(eng, n_threads=24, per_thread=8, seed=0):
    errors, done = [], []

    def worker(t):
        rng = random.Random(seed * 100 + t)
        for j in range(per_thread):
            its = [item(rng.choice([rng.randint(5, 300), rng.randint(300, 1500)]), 1000 * t + 10 * j + v, q=v // 2,
                        view=v % 2) for v in range(rng.randint(1, 4))]
            try:  # assertion errors inside a thread must reach the test: collect everything
                res = eng.submit(its, tokenize_ms=0.1).result(30)
                assert [x.tolist() for x in res.logits] == [expect(it) for it in its]
                assert set(res.timing) == {"tokenize_ms", "queue_ms", "model_ms"} and min(res.timing.values()) >= 0
                assert res.path in ("graph", "eager", "mixed") and 1 <= res.batch_rows <= 16 and res.shapes
            except BaseException as e:  # noqa: BLE001
                errors.append(e)
                continue
            done.append(res)
    ts = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
    for t in ts:
        t.start()
    for t in ts:
        t.join(60)
    assert not any(t.is_alive() for t in ts)
    return done, errors


def test_concurrent_cross_batching():
    run = FakeRunner(delay=0.003)
    eng = Bm.BatchingEngine(run, {"cross_batch": True, "max_rows": 16})
    try:
        done, errors = _hammer(eng)
        assert not errors, errors[:3]
        assert len(done) == 24 * 8
        assert run.max_active == 1  # ONE GPU worker
        assert max(n for n, _, _ in run.calls) > 2  # requests were batched together
        assert all(n <= 16 for n, _, _ in run.calls)
        st = eng.stats()
        assert st["requests"] == 192 and st["forwards"] == len(run.calls) and st["rows"] == sum(n for n, _, _ in run.calls)
    finally:
        assert eng.shutdown(timeout=10)


def test_modes_a0_a1_shapes():
    run = FakeRunner(delay=0.0)
    eng = Bm.BatchingEngine(run, Bm.ARM_FLAGS["A1"])
    try:
        its = [item(900, 1, 0, 0), item(900, 2, 0, 1)]
        res = eng.run(its, timeout=10)
        assert run.calls[-2:] == [(1, (1, 960), "exact"), (1, (1, 960), "exact")] and res.batch_rows == 1
        eng.set_flags({"legacy": True})
        its = [item(900, 3, 0, 0), item(900, 4, 0, 1)]
        res = eng.run(its, timeout=10)
        assert run.calls[-1] == (2, (2, 960), "exact") and res.batch_rows == 2 and res.path == "graph"
        its = [item(1500, 3, 0, 0), item(1500, 4, 0, 1)]
        res = eng.run(its, timeout=10)
        assert run.calls[-1] == (2, None, "exact") and res.path == "eager"  # A0: B2 > 1024 tokens is eager
        assert res.shapes == [["eager", 2, 1536]]
        eng.set_flags({"legacy": False, "cross_batch": True, "readout": "fused"})
        res = eng.run([item(900, 5), item(950, 6, 0, 1)], timeout=10)
        assert run.calls[-1] == (2, (2, 960), "fused")
    finally:
        eng.shutdown()


def test_errors_are_isolated_per_request():
    gate = threading.Event()
    run = FakeRunner(delay=0.0, gate=gate)
    eng = Bm.BatchingEngine(run, {"cross_batch": True, "max_rows": 16})
    try:
        first = eng.submit([item(50, 1)])  # holds the worker at the gate while the others queue up
        time.sleep(0.05)
        good = [eng.submit([item(60, 10 + j)]) for j in range(5)]
        bad = eng.submit([item(60, POISON), item(61, 3)])
        gate.set()
        assert first.result(10).logits[0].tolist() == [50.0, 50.0]
        with pytest.raises(ValueError, match="poisoned"):
            bad.result(10)
        for j, fu in enumerate(good):
            assert fu.result(10).logits[0].tolist() == [10 + j + 59.0, 60.0]
        assert eng.stats()["forward_errors"] >= 1
        assert eng.run([item(5, 1)], timeout=10).logits[0].tolist() == [5.0, 5.0]  # engine still serving
    finally:
        eng.shutdown()


def test_shutdown_fails_queued_and_never_hangs():
    gate = threading.Event()
    run = FakeRunner(delay=0.0, gate=gate)
    eng = Bm.BatchingEngine(run, {"cross_batch": False})
    first = eng.submit([item(10, 1)])
    time.sleep(0.05)
    queued = [eng.submit([item(10, 2 + j)]) for j in range(5)]
    assert not eng.shutdown(wait=False)
    gate.set()
    assert first.result(10).logits[0].tolist() == [10.0, 10.0]  # the forward in flight completes
    for fu in queued:
        with pytest.raises(Bm.EngineClosed):
            fu.result(10)
    assert eng.shutdown(timeout=10)  # idempotent, worker gone
    with pytest.raises(Bm.EngineClosed):
        eng.submit([item(10, 1)])
    with pytest.raises(ValueError):
        Bm.BatchingEngine(FakeRunner()).submit([])


def test_worker_death_fails_everyone():
    gate = threading.Event()
    run = FakeRunner(delay=0.0, gate=gate)
    eng = Bm.BatchingEngine(run, {"cross_batch": False})
    dying = eng.submit([item(10, -99)])
    time.sleep(0.05)
    queued = eng.submit([item(10, 5)])
    gate.set()
    for fu in (dying, queued):
        with pytest.raises(Bm.EngineClosed, match="died"):
            fu.result(10)
    eng._thread.join(10)
    assert not eng._thread.is_alive()
    with pytest.raises(Bm.EngineClosed):
        eng.submit([item(10, 1)])
    assert eng.stats()["dead"]


def test_batch_wait_collects_late_arrivals():
    run = FakeRunner(delay=0.0)
    eng = Bm.BatchingEngine(run, {"cross_batch": True, "batch_wait_ms": 150, "max_rows": 4})
    try:
        a = eng.submit([item(100, 1)])
        time.sleep(0.03)
        b = eng.submit([item(110, 2)])
        ra, rb = a.result(10), b.result(10)
        assert run.calls[0][0] == 2 and ra.batch_rows == rb.batch_rows == 2  # one forward for both
        assert ra.timing["queue_ms"] >= 100  # waited for the window
        t = time.perf_counter()  # a full drain (max_rows reached) does not wait
        eng.run([item(10, j) for j in range(4)], timeout=10)
        assert time.perf_counter() - t < 0.12
    finally:
        eng.shutdown()


def test_worker_tokenizes_legacy_items():
    seen = []

    def prepare(items):
        seen.append(len(items))
        for it in items:
            it.ids, it.n_tokens = [7] * 20, 20
    eng = Bm.BatchingEngine(FakeRunner(delay=0.0), {"legacy": True}, prepare=prepare)
    try:
        it = WorkItem(q=0, view=0, perm=None, text=None, groups=[[1]], flat=[1], sizes=[1])
        res = eng.run([it], tokenize_ms=0.5, timeout=10)
        assert seen == [1] and res.logits[0].tolist() == [140.0, 20.0] and res.timing["tokenize_ms"] >= 0.5
    finally:
        eng.shutdown()
    gate = threading.Event()
    slow = Bm.BatchingEngine(FakeRunner(gate=gate))
    fu = slow.submit([item(5, 1)])
    with pytest.raises(FutTimeout):  # a caller's timeout does not break the engine
        fu.result(0.05)
    gate.set()
    assert fu.result(10).logits[0].tolist() == [5.0, 5.0]
    assert slow.shutdown(timeout=10)


def test_is_cuda_fatal_rule():
    class AcceleratorError(RuntimeError):  # torch's name for CUDA runtime errors
        pass

    assert Bm.is_cuda_fatal(AcceleratorError("CUDA error: unspecified launch failure"))
    assert Bm.is_cuda_fatal(RuntimeError("CUDA error: device-side assert triggered"))
    assert Bm.is_cuda_fatal(RuntimeError("CUBLAS_STATUS_EXECUTION_FAILED when calling cublasGemmEx"))
    assert not Bm.is_cuda_fatal(torch.cuda.OutOfMemoryError("CUDA out of memory. Tried to allocate 2.00 GiB"))
    assert not Bm.is_cuda_fatal(AcceleratorError("CUDA error: out of memory"))  # the allocator recovers
    assert not Bm.is_cuda_fatal(ValueError("poisoned row"))


def test_cuda_fatal_stops_the_worker_without_retry():
    """A CUDA-fatal forward error is never retried (the context is poisoned): the worker stops, every request in
    flight or queued fails with EngineClosed, problems() reports it, and later submits are refused (HTTP 503)."""
    gate = threading.Event()
    run = FakeRunner(delay=0.0, gate=gate)
    eng = Bm.BatchingEngine(run, {"cross_batch": True, "max_rows": 16})
    try:
        first = eng.submit([item(50, 1)])  # holds the worker at the gate while the others queue up
        time.sleep(0.05)
        others = [eng.submit([item(60, 10 + j)]) for j in range(3)]
        bad = eng.submit([item(60, CUDA_TAG), item(61, 3)])
        others += [eng.submit([item(70, 30 + j)]) for j in range(2)]
        gate.set()
        assert first.result(10).logits[0].tolist() == [50.0, 50.0]
        with pytest.raises(Bm.EngineClosed, match="died.*illegal memory access"):
            bad.result(10)
        for fu in others:  # each either ran in a forward before the fatal one, or fails as closed
            try:
                fu.result(10)
            except Bm.EngineClosed as e:
                assert "died" in str(e)
        assert sum(CUDA_TAG in a for a in run.attempts) == 1  # no per-request retry of the fatal forward
        eng._thread.join(10)
        assert not eng._thread.is_alive()
        st = eng.stats()
        assert st["cuda_fatal"] is True and st["cuda_fatal_errors"] == 1 and "illegal memory access" in st["dead"]
        assert any("CUDA context lost" in p for p in eng.problems())
        n = len(run.attempts)
        with pytest.raises(Bm.EngineClosed, match="died"):
            eng.submit([item(10, 1)])
        assert len(run.attempts) == n  # nothing more reaches the GPU
    finally:
        gate.set()
        eng.shutdown()


def test_stalled_forward_is_reported():
    gate = threading.Event()
    eng = Bm.BatchingEngine(FakeRunner(delay=0.0, gate=gate), stall_s=0.1)
    try:
        assert eng.problems() == [] and eng.inflight_s() is None
        fu = eng.submit([item(10, 1)])
        time.sleep(0.3)
        assert eng.inflight_s() > 0.1 and eng.stats()["forward_inflight_s"] > 0.1
        assert any("GPU looks hung" in p for p in eng.problems())
        gate.set()
        assert fu.result(10).logits[0].tolist() == [10.0, 10.0]
        assert eng.problems() == [] and eng.inflight_s() is None
    finally:
        gate.set()
        eng.shutdown()
    assert eng.problems() == ["engine worker stopped (shut down)"]
