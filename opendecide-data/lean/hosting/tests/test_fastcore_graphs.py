"""fastcore.graphs on CPU: plan / buckets / selection (A0's rules checked against modal_direct_host's real code), memory
estimate, the eager readout == decoder_io.cand_logits, batched graph path == one-by-one, and the boot sequence
(static buffers, warm-up, shared-pool capture, self-check, private-pool fallback, freeze) with CUDA graphs EMULATED.

  cd ~/Documents/jev/opendecide-data/lean && ../.venv/bin/python -m pytest hosting/tests/test_fastcore_graphs.py -q
No GPU, no network, no Modal call (modal_direct_host is imported for its pure helpers only).
"""
import os
import sys
from pathlib import Path

import pytest
import torch

HOSTING = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HOSTING)]
from fastcore import graphs as G  # noqa: E402
from fastcore import readout as R  # noqa: E402
from fastcore import testing as T  # noqa: E402

dio = R.dio


@pytest.fixture(scope="module")
def tok():
    return T.c1_tokenizer()


@pytest.fixture(scope="module")
def ro(tok):
    return T.readout()


@pytest.fixture(scope="module")
def model():
    return T.tiny_model()


@pytest.fixture(scope="module")
def rows():
    return T.dev_rows()


# ------------------------------------------------------------------ plan, buckets, selection (pure)
def test_ladder():
    L = G.LADDER
    assert len(L) == 32 and L[0] == 64 and L[-1] == 4096
    assert L[:16] == tuple(range(64, 1025, 64)) and L[16:24] == tuple(range(1152, 2049, 128))
    assert L[24:] == tuple(range(2304, 4097, 256))
    assert [G.bucket_of(n) for n in (1, 64, 65, 1024, 1025, 2048, 2049, 4096)] == [64, 64, 128, 1024, 1152, 2048, 2304, 4096]
    assert G.bucket_of(4097) is None


def test_new_plan_coverage():
    plan = G.coverage_plan()
    by = {}
    for B, L in plan:
        by.setdefault(B, []).append(L)
    assert {B: (len(v), max(v)) for B, v in by.items()} == {1: (32, 4096), 2: (24, 2048), 4: (16, 1024), 8: (16, 1024),
                                                             16: (8, 512)}
    assert sum(B * L for B, L in plan) == 231424


def test_legacy_plan_equals_core():
    import modal_direct_host as core
    assert {k: core.GRAPH_CFG[k] for k in ("max_tokens", "extra_max", "long1_max", "bucket", "max_graph_tokens")} == \
        {k: G.LEGACY[k] for k in ("max_tokens", "extra_max", "long1_max", "bucket", "max_graph_tokens")}
    assert tuple(core.GRAPH_CFG["batches"]) == G.LEGACY["batches"]
    assert tuple(core.GRAPH_CFG["extra_batches"]) == G.LEGACY["extra_batches"]
    assert G.legacy_plan() == core.graph_plan(core.GRAPH_CFG)
    p = G.legacy_plan()
    assert (len(p["main"]), len(p["extra"]), len(p["long1"])) == (64, 24, 16)


def test_boot_shapes_order_and_union():
    shapes = G.boot_shapes()
    assert len(shapes) == len(set(shapes)) == len(set(G.coverage_plan()) | set(G.legacy_shapes()))
    toks = [B * L for B, L in shapes]
    assert toks == sorted(toks, reverse=True) and shapes[0] == (8, 1024)
    assert set(G.legacy_shapes()) - set(G.coverage_plan()) == {(1, L) for L in range(1088, 2048, 128)} | \
        {(B, L) for B in (3, 5, 6) for L in range(64, 513, 64)}
    fb = G.fallback_shapes()
    assert fb[0] == (1, 64) and set(G.coverage_plan(G.FALLBACK_COVERAGE)) <= set(fb) and set(fb) <= set(shapes)


def test_select_new():
    s = G.boot_shapes()
    assert G.select_new(1, 100, s) == (1, 128)
    assert G.select_new(1, 1050, s) == (1, 1088)  # a legacy B1 shape is less padding than the ladder's 1152
    assert G.select_new(2, 1500, s) == (2, 1536)
    assert G.select_new(3, 300, s) == (3, 320)
    assert G.select_new(5, 700, s) == (8, 704)
    assert G.select_new(9, 100, s) == (16, 128)
    assert G.select_new(1, 4096, s) == (1, 4096) and G.select_new(1, 4097, s) is None
    assert G.select_new(17, 10, s) is None and G.select_new(2, 2049, s) is None
    assert G.select_new(8, 1000, s, token_budget=4096) is None
    assert G.select_new(1, 4000, s, token_budget=1024) == (1, 4096)  # a single row is never refused for budget


def test_shape_index_equals_select_new():
    import random
    rng = random.Random(0)
    full = G.boot_shapes()
    for shapes in (full, rng.sample(full, 40), rng.sample(full, 7)):
        ix = G.ShapeIndex(shapes)
        for _ in range(3000):
            k, m = rng.randint(1, 18), rng.randint(1, 4200)
            b = rng.choice([None, 1024, 4096, 8192])
            assert ix.select(k, m, b) == G.select_new(k, m, shapes, b), (k, m, b)


class _FakeTok:
    """Text "x" * n -> n token ids (for driving modal_direct_host's ServingGraphs with exact lengths)."""
    pad_token_id = 0

    def __call__(self, texts, add_special_tokens=False):
        return {"input_ids": [[1] * len(t) for t in texts]}


class _FakeRo:
    def prompt(self, r, p=None):
        return r["_prompt"]

    def cand(self, r):
        return [[1], [2]]


def _fake_graph_factory(hidden):
    def fake_graph(self, B, L):
        if (B, L) not in self.graphs:
            ids, idx, out = torch.zeros(B, L, dtype=torch.long), torch.zeros(B, dtype=torch.long), torch.zeros(B, hidden)

            class Gr:
                def replay(self_g):
                    pass
            self.graphs[(B, L)] = (Gr(), ids, idx, out)
        return self.graphs[(B, L)]
    return fake_graph


def _core_pick(S, k, m):
    """The (B, L) modal_direct_host's ServingGraphs replays for k rows of max m tokens (None = eager)."""
    rows = [{"_prompt": "x" * (m if i == 0 else 1), "qtype": "choice", "options": ["a", "b"]} for i in range(k)]
    out = S.cand_logits(_FakeRo(), rows)
    return tuple(S.last_shape) if out is not None else None


def test_select_legacy_equals_core(model, monkeypatch):
    """select_legacy == the shape modal_direct_host's REAL ServingGraphs + capture_graphs code picks, after full and
    partial (memory-stopped) captures; legacy_usable == capture_graphs' usable batch sizes."""
    import modal_direct_host as core
    monkeypatch.setattr(dio.GraphRunner, "_graph", _fake_graph_factory(model.lm_head.weight.shape[1]))
    ks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 16]
    ms = [1, 64, 65, 300, 512, 513, 640, 1000, 1024, 1025, 1500, 2048, 2049, 4000, 8193]
    n = 0
    for n_cap in (104, 40, 70, 92, 10):
        S = core.make_graph_runner(dio, model, _FakeTok(), core.GRAPH_CFG)
        free = iter([100.0] * n_cap + [0.0] * 1000)
        rep = core.capture_graphs(S, core.GRAPH_CFG, lambda: next(free), log=lambda *a: None)
        captured = list(S.graphs)
        assert len(captured) == n_cap
        assert list(G.legacy_usable(captured)) == [rep["main_batches"], rep["extra_batches"]]
        for k in ks:
            for m in ms:
                want = _core_pick(S, k, m)
                got = G.select_legacy(k, m, captured)
                assert got == want, (n_cap, k, m, got, want)
                n += 1
    assert n == 5 * len(ks) * len(ms)
    full = G.legacy_shapes()
    assert G.select_legacy(2, 1500, full) is None  # A0: a choice > 1024 tokens as a batch of 2 runs eagerly
    assert G.select_legacy(1, 1500, full) == (1, 1536) and G.select_legacy(9, 10, full) is None


def test_memory_estimate():
    new = G.memory_estimate(G.coverage_plan(), shared=True)
    assert new["graphs"] == 96 and new["padded_tokens"] == 231424 and new["largest_graph_tokens"] == 8192
    assert new["pool_gb_private"] == [round(231424 * 0.17 / 1024, 2), round(231424 * 0.48 / 1024, 2)]
    assert new["pool_gb_shared"][1] < 6 and new["pool_gb_private"][0] > 30 and new["pool_gb"] == new["pool_gb_shared"]
    assert new["by_batch"]["1"] == {"n": 32, "max_L": 4096, "padded_tokens": 47104}
    fb = G.memory_estimate(G.coverage_plan(G.FALLBACK_COVERAGE), shared=False)
    assert fb["mode"] == "private" and fb["padded_tokens"] == 21504 + 17408 + 9216 + 18432 and fb["pool_gb"][1] < 32
    assert 0 < new["static_buffers_mb"] < 10


# ------------------------------------------------------------------ the tiny model: eager / graph readouts
def _items(ro, tok, rows):
    items = []
    for r in rows:
        items += R.build_items(ro, R.parse_v1(R.request_from_row(r)))
    R.tokenize_items(tok, items)
    return items


def _mixed_rows(rows):
    """Distinct short-to-medium dev rows of every kind (carded / plain noul, choice <= 9 and > 26 options), at spread
    length ranks so batches mix lengths."""
    def by(f, ranks):
        pool = sorted([r for r in rows if f(r)], key=lambda r: (len(r["state"]) + len(r.get("card") or ""), r["id"]))
        return [pool[i] for i in ranks if i < len(pool)]
    out = (by(lambda r: r["qtype"] == "noul" and r.get("card"), [0, 40]) + by(lambda r: r["qtype"] == "noul"
           and not r.get("card"), [0, 300]) + by(lambda r: r["qtype"] == "choice" and len(r["options"]) <= 9, [0, 200])
           + by(lambda r: r["qtype"] == "choice" and len(r["options"]) > 26, [0]))
    assert len({r["id"] for r in out}) == len(out) == 7
    return out


def test_eager_equals_decoder_io(model, tok, ro, rows):
    """FastGraphs eager path on pre-tokenized items == decoder_io.cand_logits on the same rows/perms (same batch)."""
    sample = _mixed_rows(rows)
    items = _items(ro, tok, sample)
    perms, srows = [], []
    for it in items:
        srows.append(it.row)
        perms.append(it.perm)
    F = G.FastGraphs(model, tok)
    worst = 0.0
    for a in range(0, len(items), 4):
        chunk = items[a:a + 4]
        got, path = F.run([it.ids for it in chunk], [(it.flat, it.sizes) for it in chunk], None)
        with torch.no_grad():
            ref = dio.cand_logits(model, ro, srows[a:a + 4], "cpu", perms=perms[a:a + 4])
        assert path == "eager"
        for g, r in zip(got, ref):
            assert g.dtype == torch.float32 and g.shape == r.shape
            worst = max(worst, float((g - r).abs().max()))
    assert worst <= 1e-5, worst


def test_batched_graph_equals_one_by_one(model, tok, ro, rows):
    """Emulated graphs (bucket padding, no mask, B = 2/4/8 with mixed lengths) == one-by-one eager reads."""
    sample = _mixed_rows(rows)
    items = _items(ro, tok, sample)
    F = G.FastGraphs(model, tok, emulate=True)
    m = max(it.n_tokens for it in items)
    assert m <= 4096
    L = G.bucket_of(m)
    shapes = [(2, L), (4, L), (8, L), (16, G.bucket_of(m))]
    F.capture(shapes, shared=True, log=lambda *a: None)
    F.freeze()
    one = {id(it): F.run([it.ids], [(it.flat, it.sizes)], None)[0][0] for it in items}
    worst = 0.0
    for B in (2, 4, 8, 16):
        for a in range(0, len(items), B):
            chunk = items[a:a + B]
            shape = F.select(len(chunk), max(it.n_tokens for it in chunk))
            assert shape is not None and shape[0] >= len(chunk)
            got, path = F.run([it.ids for it in chunk], [(it.flat, it.sizes) for it in chunk], shape)
            assert path == "graph"
            for it, g in zip(chunk, got):
                worst = max(worst, float((g - one[id(it)]).abs().max()))
    assert worst <= 1e-5, worst
    fused, _ = F.run([it.ids for it in items[:8]], [(it.flat, it.sizes) for it in items[:8]], F.select(8, m), readout="fused")
    assert max(float((f - one[id(it)]).abs().max()) for f, it in zip(fused, items[:8])) <= 1e-5


def test_dropin_cand_logits(model, tok, ro, rows):
    """FastGraphs as decoder_io.GRAPHS: decoder_io.cand_logits takes the graph path and agrees with eager."""
    sample = _mixed_rows(rows)[:4]
    F = G.FastGraphs(model, tok, emulate=True)
    F.capture(G.capture_order([(4, L) for L in G.LADDER]), log=lambda *a: None)
    F.freeze()
    with torch.no_grad():
        eager = dio.cand_logits(model, ro, sample, "cpu")
        dio.GRAPHS = F
        try:
            got = dio.cand_logits(model, ro, sample, "cpu")
        finally:
            dio.GRAPHS = None
    assert max(float((a - b).abs().max()) for a, b in zip(got, eager)) <= 1e-5


def test_boot_selfcheck_and_freeze(model, tok):
    F = G.FastGraphs(model, tok, emulate=True)
    cov = {1: 256, 2: 128, 4: 128}
    rep = F.boot(coverage=cov, legacy=False, log=lambda *a: None)
    assert rep["mode"] == "shared" and rep["n_graphs"] == 8 and rep["selfcheck"]["ok"]
    assert rep["selfcheck"]["checked"] == 8 and rep["selfcheck"]["worst_max_prob_diff"] <= 1e-5
    assert rep["fallback"] is None and rep["max_L_by_batch"] == {"1": 256, "2": 128, "4": 128}
    assert set(F.static) >= set(F.graphs) and set(F.static) >= set(G.fallback_shapes(False))  # buffers before capture
    with pytest.raises(RuntimeError):
        F.capture([(1, 512)])
    with pytest.raises(RuntimeError):
        F.capture_all()
    assert F.select(1, 300) is None and F.select(3, 100) == (4, 128)
    seq = list(range(100, 400))
    got, path = F.run([seq], [([1, 2, 3], [1, 2])], None)
    assert path == "eager" and got[0].shape == (2,)
    with pytest.raises(KeyError):
        F.run([seq], [([1], [1])], (1, 512))
    with pytest.raises(ValueError):  # more rows / tokens than the graph holds
        F.run([seq, seq], [([1], [1])] * 2, (1, 256))


def test_selfcheck_failure_falls_back_to_private_pools(model, tok, monkeypatch):
    """A corrupted shared-pool graph is caught by the self-check; the runner recaptures the reduced plan with
    private pools; a second failure leaves it eager-only."""
    F = G.FastGraphs(model, tok, emulate=True)
    orig = G.FastGraphs._capture_one
    calls = {"shared": 0, "private": 0}

    def bad(self, B, L, pool, shared=True):
        g = orig(self, B, L, pool, shared)
        calls["shared" if shared else "private"] += 1
        if shared and (B, L) == (1, 128):
            out = self.static[(B, L)][2]
            inner = g.fn
            g.fn = lambda: (inner(), out.mul_(-3.0))
        return g
    monkeypatch.setattr(G.FastGraphs, "_capture_one", bad)
    monkeypatch.setattr(G, "FALLBACK_COVERAGE", {1: 256, 2: 128})
    rep = F.boot(coverage={1: 256, 2: 128, 4: 128}, legacy=False, log=lambda *a: None)
    assert not rep["selfcheck"]["ok"] and rep["selfcheck"]["failures"][0]["shape"] == [1, 128]
    assert rep["fallback"]["selfcheck"]["ok"] and rep["mode"] == "private" and F.pool_mode == "private"
    assert set(F.graphs) == set(G.coverage_plan({1: 256, 2: 128})) and calls["private"] == 6

    F2 = G.FastGraphs(model, tok, emulate=True)

    def worse(self, B, L, pool, shared=True):
        g = orig(self, B, L, pool, shared)
        if (B, L) == (1, 64):
            out = self.static[(B, L)][2]
            inner = g.fn
            g.fn = lambda: (inner(), out.zero_())
        return g
    monkeypatch.setattr(G.FastGraphs, "_capture_one", worse)
    rep2 = F2.boot(coverage={1: 128}, legacy=False, log=lambda *a: None)
    assert rep2["mode"] == "eager_only" and not F2.graphs and F2.select(1, 10) is None and F2.frozen


def test_boot_private_pool_option(model, tok, monkeypatch):
    """pool="private" (the reboot path after a shared-pool boot died) boots the reduced plan with private pools."""
    monkeypatch.setattr(G, "FALLBACK_COVERAGE", {1: 192, 2: 128})
    F = G.FastGraphs(model, tok, emulate=True)
    rep = F.boot(coverage={1: 256}, legacy=False, pool="private", log=lambda *a: None)
    assert rep["capture"] is None and rep["selfcheck"] is None and rep["fallback"]["selfcheck"]["ok"]
    assert rep["mode"] == "private" and set(F.graphs) == set(G.coverage_plan({1: 192, 2: 128}))
    with pytest.raises(ValueError):
        G.FastGraphs(model, tok, emulate=True).boot(pool="pooled")


def test_capture_memory_guard(model, tok):
    F = G.FastGraphs(model, tok, emulate=True)
    free = iter([100.0, 100.0, 1.0] + [1.0] * 10)
    rep = F.capture(G.capture_order(G.coverage_plan({1: 256})), free_gb=lambda: next(free), reserve_gb=6.0,
                    log=lambda *a: None)
    assert rep["captured"] == 2 and "free 1.0 GB" in rep["stopped"] and set(F.graphs) == {(1, 256), (1, 192)}


@pytest.mark.skipif(not os.environ.get("FASTCORE_FULL_BOOT"), reason="~3.5 min on CPU; run with FASTCORE_FULL_BOOT=1")
def test_full_plan_boot_emulated(model, tok):
    """The production boot plan (SPEED-1 coverage + legacy set = 128 graphs), emulated end to end."""
    F = G.FastGraphs(model, tok, emulate=True)
    rep = F.boot(log=lambda *a: None)
    assert rep["mode"] == "shared" and rep["n_graphs"] == 128 and rep["selfcheck"]["ok"] and rep["fallback"] is None
    assert rep["max_L_by_batch"] == {"1": 4096, "2": 2048, "3": 512, "4": 1024, "5": 512, "6": 512, "8": 1024, "16": 512}
    assert rep["legacy_usable"] == {"main": [1, 2, 4, 8], "extra": [3, 5, 6]}
    assert rep["selfcheck"]["worst_max_prob_diff"] <= 1e-5
