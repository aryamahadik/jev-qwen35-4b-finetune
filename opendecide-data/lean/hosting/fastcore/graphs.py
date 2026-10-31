"""fastcore.graphs: the HF fast path's model runner. Pre-tokenized, right-padded id batches -> per-row fp32 candidate
logits, identical in definition to decoder_io's readout (h at the last real token, h.float() @ head.weight[flat].float().T,
final softcap if the model has one, logsumexp per candidate group).

Two forward paths:
  graph: a CUDA graph per captured (B, L) shape, replayed on static right-padded buffers WITHOUT an attention mask
         (decoder_io.GraphRunner's rule: attention, the Gated-DeltaNet recurrence and the short conv are causal, so pads
         after the last real token never reach it);
  eager: the batch padded to a multiple of decoder_io.PAD_MULTIPLE with an attention mask, body(input_ids,
         attention_mask) exactly as decoder_io.cand_logits' eager path (so eager == dio.cand_logits bit for bit).

SPEED-1 graph plan (hosting/SPEED1_DESIGN.md, "New graph plan"):
  - bucket ladder: 64-token steps to 1024, 128 to 2048, 256 to 4096; coverage B1 <= 4096, B2 <= 2048, B4/B8 <= 1024,
    B16 <= 512; the legacy shape set (B 1,2,4,8 <= 1024; 3,5,6 <= 512; B1 <= 2048, 64-token buckets) is captured too, so
    one boot serves A0 (legacy selection rules, modal_direct_host's ServingGraphs) and A1-A3;
  - static input/output buffers for every planned shape are allocated BEFORE capture, outside any graph pool;
  - eager warm-up of every shape on the capture stream before any capture (no Triton / fla autotune inside a request);
  - all graphs share ONE pool (torch.cuda.graph_pool_handle), captured largest first; outputs are copied into the
    static buffer inside the graph and cloned right after replay;
  - self-check at boot: every captured shape is replayed in non-capture orders (reverse, shuffled, after the largest
    graph) and compared with an eager forward of the same padded input; any mismatch drops all graphs and recaptures a
    reduced plan with private pools (FALLBACK_COVERAGE), checked again; a second failure leaves the runner eager-only;
  - frozen after boot: nothing is ever captured inside a request; uncovered shapes run eagerly.

CUDA capture cannot run on the Mac: on CPU the runner EMULATES graphs (replay() re-runs the captured callable on the
same static buffers), so plan / bucket / selection / buffer / self-check / fallback logic is unit-tested on CPU
(hosting/tests/test_fastcore_graphs.py). Real capture is exercised only on the GPU (SPEED-2). No Modal, no network.
"""
from __future__ import annotations

import bisect
import gc
import random
import string
import time

import torch

from .readout import dio

PAD_MULTIPLE = dio.PAD_MULTIPLE  # eager padding (256), as decoder_io.cand_logits pads


def ladder(max_tokens: int = 4096) -> list:
    """The SPEED-1 bucket ladder: 64-token steps to 1024, 128 to 2048, 256 to 4096 (32 buckets at 4096)."""
    out = list(range(64, min(1024, max_tokens) + 1, 64))
    out += list(range(1152, min(2048, max_tokens) + 1, 128))
    out += list(range(2304, min(4096, max_tokens) + 1, 256))
    return out


LADDER = tuple(ladder())
NEW_COVERAGE = {1: 4096, 2: 2048, 4: 1024, 8: 1024, 16: 512}
FALLBACK_COVERAGE = {1: 2048, 2: 1024, 4: 512, 8: 512}  # private pools: ~66K padded tokens (11-32 GB at 0.17-0.48 MB)
# = modal_direct_host.GRAPH_CFG (A0's shapes and its ServingGraphs rules); test_fastcore_graphs checks it against core
LEGACY = {"batches": (1, 2, 4, 8), "max_tokens": 1024, "extra_batches": (3, 5, 6), "extra_max": 512, "long1_max": 2048,
          "bucket": 64, "max_graph_tokens": 8192, "max_len": 8192}
POOL_MB_PER_TOKEN = (0.17, 0.48)  # private-pool MB per padded token, 30 Sep H100 bounds (modal_direct_host)
QWEN35_4B_HIDDEN = 2560


def bucket_of(n: int, lad=LADDER):
    """The smallest ladder bucket >= n, or None above the ladder."""
    for L in lad:
        if L >= n:
            return L
    return None


def coverage_plan(cov=None, lad=LADDER) -> list:
    """[(B, L)] of a coverage map {B: max L} on the ladder."""
    cov = NEW_COVERAGE if cov is None else cov
    return [(B, L) for B in sorted(cov) for L in lad if L <= cov[B]]


def legacy_plan(cfg=None) -> dict:
    """modal_direct_host.graph_plan(GRAPH_CFG): {"main", "extra", "long1"} lists of (B, L)."""
    c = LEGACY if cfg is None else cfg
    b, mg = c["bucket"], c["max_graph_tokens"]
    main = [(B, L) for B in c["batches"] for L in range(b, c["max_tokens"] + 1, b) if B == 1 or B * L <= mg]
    extra = [(B, L) for B in c["extra_batches"] for L in range(b, c["extra_max"] + 1, b) if B * L <= mg]
    long1 = [(1, L) for L in range(c["max_tokens"] + b, c["long1_max"] + 1, b)] if 1 in c["batches"] else []
    return {"main": main, "extra": extra, "long1": long1}


def legacy_shapes(cfg=None) -> list:
    p = legacy_plan(cfg)
    return p["main"] + p["extra"] + p["long1"]


def capture_order(shapes) -> list:
    """Largest first (B*L, then L, then B): the first capture sizes the shared pool, later ones reuse its blocks."""
    return sorted(set(shapes), key=lambda s: (-s[0] * s[1], -s[1], -s[0]))


def boot_shapes(coverage=None, legacy=True) -> list:
    """The boot plan: the SPEED-1 coverage plus (legacy=True) the legacy shape set, in capture order."""
    return capture_order(coverage_plan(coverage) + (legacy_shapes() if legacy else []))


def fallback_shapes(legacy=True) -> list:
    """The reduced private-pool plan, in priority order (B1 short to long, then B2, B4, B8, then legacy extras)."""
    first = coverage_plan(FALLBACK_COVERAGE)
    rest = [s for s in legacy_shapes() if s not in set(first)] if legacy else []
    return first + rest


def select_new(k: int, m: int, shapes, token_budget: int | None = None):
    """SPEED-1 selection: the captured (B, L) with B >= k rows and L >= m tokens of least padded size B*L (then
    smallest B); token_budget bounds B*L for multi-row batches (a single row is never refused for budget)."""
    best = None
    for B, L in shapes:
        if B < k or L < m:
            continue
        if token_budget is not None and k > 1 and B * L > token_budget:
            continue
        if best is None or (B * L, B) < (best[0] * best[1], best[0]):
            best = (B, L)
    return best


class ShapeIndex:
    """select_new over a fixed shape set in O(#batch sizes x log #lengths) (the batcher's cut search calls it often)."""

    def __init__(self, shapes):
        by = {}
        for B, L in shapes:
            by.setdefault(B, []).append(L)
        self.by = {B: sorted(set(v)) for B, v in by.items()}
        self.bs = sorted(self.by)

    def select(self, k: int, m: int, token_budget: int | None = None):
        best = None
        for B in self.bs:
            if B < k:
                continue
            Ls = self.by[B]
            i = bisect.bisect_left(Ls, m)
            if i == len(Ls):
                continue
            L = Ls[i]
            if token_budget is not None and k > 1 and B * L > token_budget:
                continue
            if best is None or (B * L, B) < (best[0] * best[1], best[0]):
                best = (B, L)
        return best


def legacy_usable(shapes, cfg=None) -> tuple:
    """(main, extra) batch sizes whose whole legacy range is captured (modal_direct_host.capture_graphs' full())."""
    c = LEGACY if cfg is None else cfg
    have, b, mg = set(shapes), c["bucket"], c["max_graph_tokens"]

    def full(B, Lmax):
        return all((B, L) in have for L in range(b, Lmax + 1, b) if B == 1 or B * L <= mg)
    return ([B for B in c["batches"] if full(B, c["max_tokens"])],
            [B for B in c["extra_batches"] if full(B, c["extra_max"])])


def select_legacy(k: int, m: int, shapes, cfg=None, usable=None):
    """A0's choice, exactly as modal_direct_host.ServingGraphs + decoder_io.GraphRunner.cand_logits pick it: L = m
    rounded up to 64; try the smallest usable batch >= k among main+extra, then among main only; give up (eager) on a
    size/length rule or when neither shape was captured. `shapes` = the captured LEGACY shapes (a set is fastest);
    usable = legacy_usable(shapes) if already known."""
    c = LEGACY if cfg is None else cfg
    have = shapes if isinstance(shapes, (set, frozenset)) else set(shapes)
    main, extra = legacy_usable(have, c) if usable is None else usable
    main, alls = tuple(sorted(main)), tuple(sorted(set(main) | set(extra)))
    tries = [alls, main] if alls != main else [alls]
    L = -(-m // c["bucket"]) * c["bucket"]
    for bs in tries:
        B = next((b for b in bs if b >= k), None)
        if B is None or L > c["max_len"] or (B > 1 and B * L > c["max_graph_tokens"]):
            return None  # GraphRunner.cand_logits returns None: the caller runs eagerly (no retry)
        if (B, L) in have:
            return (B, L)
    return None


def eager_len(m: int) -> int:
    return -(-m // PAD_MULTIPLE) * PAD_MULTIPLE


def memory_estimate(shapes, shared: bool = True, hidden: int = QWEN35_4B_HIDDEN, mb_per_token=POOL_MB_PER_TOKEN,
                    frag: float = 1.25) -> dict:
    """Graph memory for a plan. Private pools: every graph keeps its own peak (sum over graphs). One shared pool
    captured largest first: about the largest graph's peak (x frag on the upper bound for fragmentation). Static
    buffers (ids int64 + idx + bf16 outputs) are counted separately. Bounds are the 30 Sep H100 measurements."""
    shapes = list(shapes)
    toks = [B * L for B, L in shapes]
    lo, hi = mb_per_token
    by_b = {}
    for B, L in shapes:
        d = by_b.setdefault(B, {"n": 0, "max_L": 0, "padded_tokens": 0})
        d["n"] += 1
        d["max_L"] = max(d["max_L"], L)
        d["padded_tokens"] += B * L
    static_mb = sum(B * L * 8 + B * 8 + B * hidden * 2 for B, L in shapes) / 2 ** 20
    private = [round(sum(toks) * lo / 1024, 2), round(sum(toks) * hi / 1024, 2)]
    big = max(toks) if toks else 0
    shared_gb = [round(big * lo / 1024, 2), round(big * hi * frag / 1024, 2)]
    return {"graphs": len(shapes), "by_batch": {str(k): v for k, v in sorted(by_b.items())},
            "padded_tokens": sum(toks), "largest_graph_tokens": big, "static_buffers_mb": round(static_mb, 2),
            "pool_gb_private": private, "pool_gb_shared": shared_gb,
            "pool_gb": shared_gb if shared else private, "mode": "shared" if shared else "private",
            "mb_per_token": list(mb_per_token)}


class _EmuGraph:
    """CPU stand-in for torch.cuda.CUDAGraph: replay() re-runs the captured callable on the same static buffers."""

    def __init__(self, fn):
        self.fn = fn

    def replay(self):
        with torch.no_grad():
            self.fn()


class FastGraphs(dio.GraphRunner):
    """Serving runner for pre-tokenized work. Subclasses decoder_io.GraphRunner for its set-up (body/head split, softcap,
    PRISM-X refusal) and replaces capture, selection and replay with the SPEED-1 plan. Not thread-safe: one GPU worker
    (fastcore.batcher.BatchingEngine) calls it; boot() runs before serving starts."""

    def __init__(self, model, tok, device=None, emulate: bool | None = None):
        super().__init__(model, tok, bucket=64, max_len=LEGACY["max_len"], batches=(1, 2, 4, 8, 16),
                         max_graph_tokens=LEGACY["max_graph_tokens"])
        self.device = torch.device(device) if device is not None else self.head.weight.device
        self.emulate = (self.device.type != "cuda") if emulate is None else bool(emulate)
        self.pad_id = tok.pad_token_id
        self.hidden = self.head.weight.shape[1]
        emb = getattr(self.body, "get_input_embeddings", lambda: None)()
        self.hdtype = emb.weight.dtype if emb is not None else self.head.weight.dtype
        self.static = {}  # (B, L) -> (ids, idx, out): allocated before capture, outside any graph pool
        self.graphs = {}  # (B, L) -> captured graph (torch.cuda.CUDAGraph or _EmuGraph)
        self.pool = None
        self.pool_mode = None  # "shared" | "private" | None (eager only)
        self.frozen = False
        self.cap_stream = None
        self.report = {"graphs": 0, "pool": None, "boot": None}
        self.last = {"path": None, "shape": None}
        self._sel = None  # (n graphs, ShapeIndex, captured legacy set, legacy usable): rebuilt when graphs change

    def _graph(self, B, L):  # decoder_io.GraphRunner's capture-on-demand (private pools) is not used here
        raise RuntimeError("FastGraphs captures only in boot()/capture(); use run()/select()")

    def capture_all(self, *a, **k):
        raise RuntimeError("FastGraphs: use boot() (SPEED-1 plan) instead of capture_all()")

    # ------------------------------------------------------------------ shapes
    def captured(self) -> list:
        return sorted(self.graphs)

    def captured_legacy(self) -> list:
        leg = set(legacy_shapes())
        return [s for s in self.graphs if s in leg]

    def select(self, k: int, m: int, legacy: bool = False, token_budget: int | None = None):
        """The captured (B, L) for k rows of at most m tokens, or None (eager). legacy=True applies A0's rules to the
        legacy shapes only; else SPEED-1's least-padding choice over every captured shape (= select_new)."""
        if not self.graphs:
            return None
        if self._sel is None or self._sel[0] != len(self.graphs):
            leg = set(self.captured_legacy())
            self._sel = (len(self.graphs), ShapeIndex(self.graphs), leg, legacy_usable(leg))
        _, idx, leg, usable = self._sel
        if legacy:
            return select_legacy(k, m, leg, usable=usable)
        return idx.select(k, m, token_budget)

    # ------------------------------------------------------------------ boot: buffers, warm-up, capture, self-check
    def _alloc(self, shapes):
        for B, L in shapes:
            if (B, L) not in self.static:
                ids = torch.full((B, L), self.pad_id, dtype=torch.long, device=self.device)
                idx = torch.zeros(B, dtype=torch.long, device=self.device)
                out = torch.zeros(B, self.hidden, dtype=self.hdtype, device=self.device)
                self.static[(B, L)] = (ids, idx, out)

    def _body_last(self, ids, idx, B, L):
        hs = self.body(input_ids=ids, use_cache=False).last_hidden_state
        return hs.reshape(B * L, hs.shape[-1]).index_select(0, idx)

    def warmup(self, shapes, iters: int = 2) -> float:
        """Eager forward of every shape on the capture stream (autotune and lazy init happen here, not in capture)."""
        t0 = time.time()
        with torch.no_grad():
            if self.emulate or self.device.type != "cuda":
                for B, L in shapes:
                    ids, idx, _ = self.static[(B, L)]
                    self._body_last(ids, idx, B, L)
                return time.time() - t0
            if self.cap_stream is None:
                self.cap_stream = torch.cuda.Stream(device=self.device)
            self.cap_stream.wait_stream(torch.cuda.current_stream(self.device))
            with torch.cuda.stream(self.cap_stream):
                for B, L in shapes:
                    ids, idx, _ = self.static[(B, L)]
                    for _ in range(iters):
                        self._body_last(ids, idx, B, L)
            torch.cuda.current_stream(self.device).wait_stream(self.cap_stream)
            torch.cuda.synchronize(self.device)
        return time.time() - t0

    def _capture_one(self, B, L, pool, shared=True):
        """Capture one shape into `pool` (None = a private pool). Returns the graph object."""
        ids, idx, out = self.static[(B, L)]
        if self.emulate:
            return _EmuGraph(lambda: out.copy_(self._body_last(ids, idx, B, L)))
        g = torch.cuda.CUDAGraph()
        with torch.no_grad(), torch.cuda.graph(g, pool=pool, stream=self.cap_stream):
            out.copy_(self._body_last(ids, idx, B, L))
        return g

    def _free_gb(self):
        if self.device.type != "cuda":
            return float("inf")
        return torch.cuda.mem_get_info(self.device)[0] / 2 ** 30

    def capture(self, shapes, shared: bool = True, reserve_gb: float = 6.0, free_gb=None, log=print) -> dict:
        """Capture `shapes` in the given order (boot_shapes is largest first). Stops when free memory < reserve_gb or
        on OOM (the shapes left run eagerly). shared=True: one pool for all; False: a private pool per graph."""
        if self.frozen:
            raise RuntimeError("FastGraphs is frozen: no capture after boot")
        free_gb = free_gb or self._free_gb
        self._alloc(shapes)
        if not self.emulate and self.cap_stream is None:
            self.cap_stream = torch.cuda.Stream(device=self.device)
        if shared and self.pool is None and not self.emulate:
            self.pool = torch.cuda.graph_pool_handle()
        t0, got, stopped = time.time(), 0, None
        for B, L in shapes:
            if (B, L) in self.graphs:
                continue
            free = free_gb()
            if free < reserve_gb:
                stopped = f"at {(B, L)}: free {free:.1f} GB < reserve {reserve_gb} GB"
                break
            try:
                self.graphs[(B, L)] = self._capture_one(B, L, self.pool if shared else None, shared)
            except torch.cuda.OutOfMemoryError as e:  # the partial graph is not kept; eager covers the shape
                stopped = f"at {(B, L)}: OOM {str(e)[:120]}"
                if self.device.type == "cuda":
                    torch.cuda.empty_cache()
                break
            got += 1
        self._sel = None
        self.pool_mode = ("shared" if shared else "private") if self.graphs else None
        rep = {"captured": got, "n_graphs": len(self.graphs), "pool": self.pool_mode, "stopped": stopped,
               "capture_s": round(time.time() - t0, 2)}
        log(f"fastcore graphs: {rep}")
        return rep

    def _probe_ids(self, n_total: int) -> list:
        if getattr(self, "_probe_base", None) is None:
            filler = "The office opens at nine and closes at five on weekdays. Payments are due on the first day. "
            self._probe_base = self.tok(filler * 4, add_special_tokens=False)["input_ids"]
        base = self._probe_base
        return [base[i % len(base)] for i in range(n_total)]

    def _probe(self, B, L, seed):
        """Deterministic probe for (B, L): B rows of real lengths in (L/2, L], filler token ids."""
        rng = random.Random(seed * 1000003 + B * 8191 + L)
        lens = [max(1, L - rng.randrange(0, max(1, L // 2))) for _ in range(B)]
        pool = self._probe_ids(L + 97)
        seqs = []
        for n in lens:
            o = rng.randrange(0, 97)
            seqs.append(torch.tensor(pool[o:o + n], dtype=torch.long))
        return seqs

    def _letter_groups(self):
        return [self.tok.encode(c, add_special_tokens=False)[:1] for c in string.ascii_uppercase]

    def selfcheck(self, tol_prob: float = 0.02, seed: int = 0, masked_sample: int = 8, log=print) -> dict:
        """Every captured graph vs an eager forward of the SAME padded input (no mask), replayed in reverse capture
        order, in a shuffled order, and each right after the largest graph. Metric: max |p_graph - p_eager| over the
        26-letter softmax of the probe rows (and finiteness). Also reports (not gated) graph vs the masked eager path
        on a few shapes. ok=False on any mismatch."""
        if not self.graphs:
            return {"ok": True, "checked": 0, "note": "no graphs"}
        t0 = time.time()
        groups = self._letter_groups()
        cands = [([t for g in groups for t in g], [len(g) for g in groups])]
        order = capture_order(self.graphs)
        ref, probes = {}, {}
        with torch.no_grad():
            for s in order:
                B, L = s
                seqs = self._probe(B, L, seed)
                probes[s] = seqs
                ids, idx = self._fill_cpu(seqs, B, L)
                ids, idx = ids.to(self.device), idx.to(self.device)
                h = self._body_last(ids, idx, B, L)[: len(seqs)]
                ref[s] = torch.stack([torch.softmax(x, -1) for x in self.readout(h, cands * len(seqs))])
            worst, bad = 0.0, []

            def check(s, tag):
                nonlocal worst
                h = self._replay(probes[s], *s)
                p = torch.stack([torch.softmax(x, -1) for x in self.readout(h, cands * len(probes[s]))])
                d = float((p - ref[s]).abs().max()) if torch.isfinite(p).all() else float("inf")
                worst = max(worst, d)
                if not d <= tol_prob:
                    bad.append({"shape": list(s), "pass": tag, "max_prob_diff": d})
            for s in reversed(order):
                check(s, "reverse")
            sh = list(order)
            random.Random(seed).shuffle(sh)
            for s in sh:
                check(s, "shuffled")
            big = order[0]
            for s in order[1:]:
                self._replay(probes[big], *big)
                check(s, "after_largest")
            masked = []
            for s in order[:: max(1, len(order) // max(1, masked_sample))][:masked_sample]:
                seqs = probes[s]
                hg = self._replay(seqs, *s)
                he = self._eager_h(seqs)
                pg = torch.stack([torch.softmax(x, -1) for x in self.readout(hg, cands * len(seqs))])
                pe = torch.stack([torch.softmax(x, -1) for x in self.readout(he, cands * len(seqs))])
                masked.append({"shape": list(s), "max_prob_diff": float((pg - pe).abs().max())})
        if self.device.type == "cuda" and not self.emulate:
            torch.cuda.empty_cache()  # the eager references' blocks go back to the device
        rep = {"ok": not bad, "checked": len(order), "checks": 3 * len(order) - 1, "worst_max_prob_diff": worst,
               "tol_prob": tol_prob, "failures": bad[:20], "n_failures": len(bad), "vs_masked_eager": masked,
               "selfcheck_s": round(time.time() - t0, 2)}
        log(f"fastcore selfcheck: ok={rep['ok']} worst={worst:.3g} failures={len(bad)}")
        return rep

    def drop_graphs(self):
        """Release every graph and its pool memory (static buffers are kept)."""
        self.graphs = {}
        self._sel = None
        self.pool = None
        self.pool_mode = None
        gc.collect()
        if self.device.type == "cuda" and not self.emulate:
            torch.cuda.synchronize(self.device)
            torch.cuda.empty_cache()

    def boot(self, coverage=None, legacy: bool = True, reserve_gb: float = 6.0, tol_prob: float = 0.02,
             free_gb=None, pool: str = "shared", log=print) -> dict:
        """Start-up: static buffers -> eager warm-up of every shape -> one shared pool, largest first -> self-check ->
        (on failure) private pools + FALLBACK_COVERAGE -> self-check -> (on failure) eager only. Then freeze.
        pool="private" skips the shared pool and boots the fallback plan directly (for a reboot after a shared-pool
        boot died with a device-side assert, which no in-process fallback can survive)."""
        if self.frozen:
            raise RuntimeError("FastGraphs.boot: already booted (frozen)")
        if pool not in ("shared", "private"):
            raise ValueError(f"pool must be 'shared' or 'private', not {pool!r}")
        t0 = time.time()
        plan = boot_shapes(coverage, legacy)
        fb = fallback_shapes(legacy)
        self._alloc(plan + fb)
        warm = (plan + [s for s in fb if s not in set(plan)]) if pool == "shared" else fb
        rep = {"pool_requested": pool, "plan": memory_estimate(plan if pool == "shared" else fb, shared=pool == "shared"),
               "warmup_s": round(self.warmup(warm), 2), "capture": None, "selfcheck": None, "fallback": None}
        if self.device.type == "cuda" and not self.emulate:
            torch.cuda.empty_cache()  # warm-up blocks back to the device: the graph pool cannot reuse cached blocks
        if pool == "shared":
            rep["capture"] = self.capture(plan, shared=True, reserve_gb=reserve_gb, free_gb=free_gb, log=log)
            rep["selfcheck"] = self.selfcheck(tol_prob=tol_prob, log=log)
        if pool == "private" or not rep["selfcheck"]["ok"]:
            if pool == "shared":
                log("fastcore: shared-pool self-check FAILED -> private pools + reduced plan")
                self.drop_graphs()
            rep["fallback"] = {"plan": memory_estimate(fb, shared=False)}
            rep["fallback"]["capture"] = self.capture(fb, shared=False, reserve_gb=reserve_gb, free_gb=free_gb, log=log)
            rep["fallback"]["selfcheck"] = self.selfcheck(tol_prob=tol_prob, log=log)
            if not rep["fallback"]["selfcheck"]["ok"]:
                log("fastcore: private-pool self-check FAILED -> eager only")
                self.drop_graphs()
        self.frozen = True
        rep["mode"] = self.pool_mode or "eager_only"
        rep["n_graphs"] = len(self.graphs)
        cov = {}
        for B, L in self.graphs:
            cov[str(B)] = max(cov.get(str(B), 0), L)
        rep["max_L_by_batch"] = dict(sorted(cov.items(), key=lambda x: int(x[0])))
        lu = legacy_usable(self.captured_legacy())
        rep["legacy_usable"] = {"main": lu[0], "extra": lu[1]}
        if self.device.type == "cuda" and not self.emulate:
            rep["memory_gb"] = {"allocated": round(torch.cuda.memory_allocated(self.device) / 2 ** 30, 2),
                                "reserved": round(torch.cuda.memory_reserved(self.device) / 2 ** 30, 2),
                                "free": round(self._free_gb(), 2)}
        rep["boot_s"] = round(time.time() - t0, 2)
        self.report = {"graphs": len(self.graphs), "pool": self.pool_mode, "boot": rep}
        return rep

    def freeze(self):
        """Eager-only (or externally captured) serving: no capture from now on."""
        self.frozen = True

    # ------------------------------------------------------------------ forward paths
    def _fill_cpu(self, seqs, B, L):
        ids = torch.full((B, L), self.pad_id, dtype=torch.long)
        idx = torch.zeros(B, dtype=torch.long)
        for i, x in enumerate(seqs):
            n = len(x)
            ids[i, :n] = torch.as_tensor(x, dtype=torch.long)
            idx[i] = i * L + n - 1
        return ids, idx

    def _replay(self, seqs, B, L):
        """Fill the static buffers, replay the (B, L) graph, return a CLONE of the first len(seqs) rows of h."""
        if len(seqs) > B or max(len(x) for x in seqs) > L:
            raise ValueError(f"{len(seqs)} rows of up to {max(len(x) for x in seqs)} tokens do not fit graph {(B, L)}")
        sid, sidx, out = self.static[(B, L)]
        ids, idx = self._fill_cpu(seqs, B, L)
        sid.copy_(ids, non_blocking=True)
        sidx.copy_(idx, non_blocking=True)
        self.graphs[(B, L)].replay()
        return out[: len(seqs)].clone()

    def _eager_h(self, seqs):
        """decoder_io.cand_logits' eager forward: right padding to a multiple of PAD_MULTIPLE, attention mask."""
        n = [len(x) for x in seqs]
        Lp = eager_len(max(n))
        ids = torch.full((len(seqs), Lp), self.pad_id, dtype=torch.long)
        mask = torch.zeros((len(seqs), Lp), dtype=torch.long)
        for i, x in enumerate(seqs):
            ids[i, : n[i]] = torch.as_tensor(x, dtype=torch.long)
            mask[i, : n[i]] = 1
        ids, mask = ids.to(self.device), mask.to(self.device)
        hs = self.body(input_ids=ids, attention_mask=mask).last_hidden_state
        last = mask.sum(1) - 1
        return hs[torch.arange(len(seqs), device=self.device), last]

    def readout(self, h, cands, mode: str = "exact") -> list:
        """Per-row fp32 candidate logits. cands[i] = (flat ids, group sizes). "exact" is decoder_io's per-row loop
        (bit-identical); "fused" is one GEMM over the union of ids plus a padded logsumexp (fp32, tiny rounding
        differences; a speed option, parity-checked in SPEED-2)."""
        if mode == "fused":
            return self._readout_fused(h, cands)
        res = []
        for i, (flat, sizes) in enumerate(cands):
            lg = h[i].float() @ self.head.weight[flat].float().T
            if self.cap:
                lg = self.cap * torch.tanh(lg / self.cap)
            parts, k = [], 0
            for s in sizes:
                parts.append(torch.logsumexp(lg[k:k + s], 0))
                k += s
            res.append(torch.stack(parts))
        return res

    def _readout_fused(self, h, cands):
        allids = sorted({t for flat, _ in cands for t in flat})
        col = {t: j for j, t in enumerate(allids)}
        W = self.head.weight[torch.tensor(allids, device=h.device)].float()
        M = h.float() @ W.T  # [rows, U]
        if self.cap:
            M = self.cap * torch.tanh(M / self.cap)
        gmax = max(s for _, sizes in cands for s in sizes)
        rows_i, cols_i, valid, counts = [], [], [], []
        for i, (flat, sizes) in enumerate(cands):
            k = 0
            for s in sizes:
                ids = flat[k:k + s]
                rows_i.append([i] * gmax)
                cols_i.append([col[t] for t in ids] + [0] * (gmax - s))
                valid.append([True] * s + [False] * (gmax - s))
                k += s
            counts.append(len(sizes))
        r = torch.tensor(rows_i, device=h.device)
        c = torch.tensor(cols_i, device=h.device)
        v = torch.tensor(valid, device=h.device)
        vals = M[r, c].masked_fill(~v, float("-inf"))
        lse = torch.logsumexp(vals, 1)
        return list(torch.split(lse, counts))

    @torch.no_grad()
    def run(self, seqs, cands, shape=None, readout: str = "exact"):
        """One forward + readout. seqs: token id lists / 1-D tensors (already capped); cands[i] = (flat, sizes);
        shape = a captured (B, L) or None (eager). Returns (fp32 CPU logits per row, path)."""
        if shape is not None and shape not in self.graphs:
            raise KeyError(f"shape {shape} is not captured")
        if shape is None:
            h, path = self._eager_h(seqs), "eager"
        else:
            h, path = self._replay(seqs, *shape), "graph"
        lg = self.readout(h, cands, readout)
        sizes = [x.numel() for x in lg]
        flat = torch.cat(lg).to("cpu")  # one device->host copy (also the sync point for timing)
        self.last = {"path": path, "shape": list(shape) if shape else None}
        return list(torch.split(flat, sizes)), path

    # ------------------------------------------------------------------ decoder_io drop-in (text rows)
    @torch.no_grad()
    def cand_logits(self, ro, rows, perms=None):
        """decoder_io.GRAPHS-compatible: text rows -> graph-path logits, or None (decoder_io then runs eagerly)."""
        texts = dio.prompt_texts(ro, rows, perms)
        enc = self.tok(texts, add_special_tokens=False)["input_ids"]
        n = max(len(x) for x in enc)
        if n > dio.MAX_LEN:
            return None
        shape = self.select(len(rows), n)
        if shape is None:
            return None
        cands = []
        for r in rows:
            g = ro.cand(r)
            cands.append(([t for x in g for t in x], [len(x) for x in g]))
        h = self._replay(enc, *shape)
        return self.readout(h, cands)

    def health(self) -> dict:
        return {"n_graphs": len(self.graphs), "pool": self.pool_mode, "frozen": self.frozen, "emulated": self.emulate,
                "boot": self.report.get("boot")}
