"""fastcore.batcher: the HF fast path's request scheduler. ONE GPU worker thread; any number of HTTP threads submit
pre-tokenized work items (fastcore.readout.WorkItem) and wait on a Future.

Policies (runtime flags, switchable through set_flags without a reboot; names match hosting/speed_arms.json):
  legacy=true                 A0: one request at a time, the request's items (both views) as ONE batch, A0's legacy
                              graph shapes and selection rules, tokenization inside the worker (as the old GPU lock did);
  twoview_split=true,
  cross_batch=false           A1: one request at a time, every item (each view) its own batch-1 forward;
  cross_batch=true            A2/A3: opportunistic batching: drain whatever is queued (whole requests, up to max_rows
                              rows; no forced wait unless batch_wait_ms > 0), sort by token length and cut the sorted
                              list into sub-batches whose (B, L) are captured graph shapes within token_budget, choosing
                              the cut with the least estimated cost (padding + per-call overhead); eager where no
                              captured shape fits.
Aliases accepted (and echoed back): batching=cross_batch, two_pass_2view=twoview_split, max_wait_ms=batch_wait_ms,
legacy_graphs=(graph_plan == "legacy"), tokenize_in_worker=(not tokenize_outside_lock).

Per request timing: tokenize_ms (prompt + tokenizer; the caller's, plus the worker's when it tokenizes), queue_ms
(submit -> its first forward starts), model_ms (its first forward starts -> its last readout is on the host).
Robustness: an exception in a forward shared by several requests is retried once per request (alone), so only the
request(s) that still fail get the exception; shutdown fails what is still queued (EngineClosed) and never blocks a
waiting caller forever. A CUDA-fatal error in a forward (is_cuda_fatal: device-side assert, illegal address, launch
failure) poisons the process's CUDA context, so it is never retried: the worker stops at once, every request in flight
or queued fails with EngineClosed (HTTP 503), and problems() / the engine's /health report it (ok=false); the host's
watchdog then ends the container. A forward in flight for more than stall_s (a hung kernel or D2H copy) is reported by
problems() too. CPU-tested in hosting/tests/test_fastcore_batcher.py with fake runners and the tiny Qwen3.5 model; no
GPU, no network.
"""
from __future__ import annotations

import collections
import threading
import time
import traceback
from concurrent.futures import Future
from dataclasses import dataclass, field

from .graphs import eager_len

FLAG_DEFAULTS = {
    "legacy": False,
    "cross_batch": True,
    "twoview_split": True,
    "graph_plan": "speed1",  # "speed1" (all captured shapes, least padding) | "legacy" (A0's shapes and rules)
    "tokenize_outside_lock": True,
    "batch_wait_ms": 0.0,
    "max_rows": 16,  # rows per drain and per forward
    "token_budget": 8192,  # padded B x L per multi-row forward
    "readout": "exact",  # "exact" (decoder_io's per-row loop) | "fused" (one GEMM)
    "choice_views": 2,  # 2 = A5 2view; 1 = given order only (identity reads, for the parity diagnostics)
    "cost_call_ms": 4.0,  # cost model of the sub-batch former: per-forward overhead (graph replay + readout)
    "cost_token_ms": 0.02,  # per padded token
    "cost_eager_ms": 40.0,  # per-forward overhead of the eager path
}
ALIASES = {"batching": "cross_batch", "two_pass_2view": "twoview_split", "max_wait_ms": "batch_wait_ms",
           "legacy_graphs": "graph_plan", "tokenize_in_worker": "tokenize_outside_lock"}
_ALIAS_IN = {"legacy_graphs": lambda v: "legacy" if v else "speed1", "tokenize_in_worker": lambda v: not v}
_ALIAS_OUT = {"legacy_graphs": lambda f: f["graph_plan"] == "legacy",
              "tokenize_in_worker": lambda f: not f["tokenize_outside_lock"]}
ARM_FLAGS = {  # the HF arms of SPEED1_DESIGN.md (A3 = A2 flags on the FP8 boot)
    "A0": {"legacy": True},
    "A1": {"legacy": False, "twoview_split": True, "graph_plan": "speed1", "tokenize_outside_lock": True,
           "cross_batch": False},
    "A2": {"legacy": False, "twoview_split": True, "graph_plan": "speed1", "tokenize_outside_lock": True,
           "cross_batch": True, "batch_wait_ms": 0},
    "A3": {"legacy": False, "twoview_split": True, "graph_plan": "speed1", "tokenize_outside_lock": True,
           "cross_batch": True, "batch_wait_ms": 0},
}


STALL_S = 120.0  # a forward in flight longer than this is reported as a hung GPU (normal forwards take < 2 s)
# Substrings of CUDA errors that poison the process's CUDA context (nothing more can run on that GPU in this process).
# An out-of-memory error is NOT fatal: the caching allocator recovers.
CUDA_FATAL_MARKERS = ("device-side assert", "CUDA error", "illegal memory access", "illegal address",
                      "cudaErrorLaunchFailure", "unspecified launch failure", "CUBLAS_STATUS_EXECUTION_FAILED")


def is_cuda_fatal(e: BaseException) -> bool:
    """A CUDA error that poisons the process's CUDA context (device-side assert, illegal address, launch failure):
    nothing more can run on the GPU in this process, so the only recovery is a new container. Pure string test (no
    torch import), shared by the batcher (serving) and hosting/fast_host.py (boot). Deliberately conservative: any
    other CUDA runtime error ("CUDA error: ...", torch's AcceleratorError) counts as fatal too, since mid-forward on a
    shared-pool graph path it most likely means corrupted state; only out-of-memory errors (recoverable) do not."""
    s = f"{type(e).__name__}: {e}"
    if "out of memory" in s.lower():
        return False
    return type(e).__name__ == "AcceleratorError" or any(k in s for k in CUDA_FATAL_MARKERS)


class EngineClosed(RuntimeError):
    """The engine is shut down (HTTP 503)."""


class _Poisoned(BaseException):
    """Raised inside the worker on a CUDA-fatal forward error: not an Exception, so no per-drain handler swallows it
    and the worker loop ends (as on any other worker death)."""

    def __init__(self, err: BaseException):
        super().__init__(repr(err))
        self.err = err


def _check(k, v):
    bools = ("legacy", "cross_batch", "twoview_split", "tokenize_outside_lock")
    if k in bools:
        if not isinstance(v, bool):
            raise ValueError(f"flag {k} must be true/false")
    elif k == "graph_plan":
        if v not in ("speed1", "legacy"):
            raise ValueError('flag graph_plan must be "speed1" or "legacy"')
    elif k == "readout":
        if v not in ("exact", "fused"):
            raise ValueError('flag readout must be "exact" or "fused"')
    elif k == "choice_views":
        if v not in (1, 2) or isinstance(v, bool):
            raise ValueError("flag choice_views must be 1 or 2")
    elif k == "max_rows":
        if isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= 64:
            raise ValueError("flag max_rows must be an integer in 1..64")
    elif k == "token_budget":
        if isinstance(v, bool) or not isinstance(v, int) or v < 64:
            raise ValueError("flag token_budget must be an integer >= 64")
    else:
        if isinstance(v, bool) or not isinstance(v, (int, float)) or v < 0:
            raise ValueError(f"flag {k} must be a number >= 0")


def normalize_flags(update: dict, base: dict | None = None) -> dict:
    """base (default FLAG_DEFAULTS) updated with `update` (canonical names or aliases). Raises ValueError on an unknown
    flag or a bad value; nothing is applied then."""
    out = dict(FLAG_DEFAULTS if base is None else base)
    for k, v in (update or {}).items():
        if k in ALIASES:
            if k in _ALIAS_IN:
                if not isinstance(v, bool):
                    raise ValueError(f"flag {k} must be true/false")
                v = _ALIAS_IN[k](v)
            k = ALIASES[k]
        if k not in FLAG_DEFAULTS:
            raise ValueError(f"unknown flag {k!r} (known: {sorted(FLAG_DEFAULTS)} and aliases {sorted(ALIASES)})")
        _check(k, v)
        out[k] = float(v) if k in ("batch_wait_ms", "cost_call_ms", "cost_token_ms", "cost_eager_ms") else v
    return out


def effective_flags(f: dict) -> dict:
    """What the worker actually does: legacy=true forces A0; twoview_split=false keeps a request as one batch."""
    e = dict(f)
    if e["legacy"]:
        e.update(cross_batch=False, twoview_split=False, graph_plan="legacy", tokenize_outside_lock=False,
                 readout="exact")
    if not e["twoview_split"]:
        e["cross_batch"] = False
    return e


def flags_view(f: dict) -> dict:
    """/health "flags": the set flags under their canonical names AND their aliases (either reads back unchanged), plus
    "effective" (what the worker runs)."""
    out = dict(f)
    for a, k in ALIASES.items():
        out[a] = _ALIAS_OUT[a](f) if a in _ALIAS_OUT else f[k]
    out["effective"] = effective_flags(f)
    return out


def plan_batches(lengths, select, max_rows: int, token_budget: int, cost: dict) -> list:
    """Cut items into forwards. lengths[i] = item i's tokens; select(k, m) -> captured (B, L) or None. Items are sorted
    by length and cut into contiguous groups (dynamic programming, O(n * max_rows)) minimising
    sum(call + token * B * L) over graph groups and sum(eager + token * k * eager_len(m)) over eager ones; a multi-row
    group must fit token_budget. Returns [(item indices, shape or None)] in ascending length order."""
    order = sorted(range(len(lengths)), key=lambda i: (lengths[i], i))
    n = len(order)
    INF = float("inf")
    best = [0.0] + [INF] * n
    back = [None] * (n + 1)
    for j in range(1, n + 1):
        m = lengths[order[j - 1]]
        for i in range(j - 1, max(-1, j - 1 - max_rows), -1):
            k = j - i
            shape = select(k, m)
            if shape is not None and (k == 1 or shape[0] * shape[1] <= token_budget):
                c = cost["cost_call_ms"] + cost["cost_token_ms"] * shape[0] * shape[1]
            elif k == 1 or k * eager_len(m) <= token_budget:
                shape = None
                c = cost["cost_eager_ms"] + cost["cost_token_ms"] * k * eager_len(m)
            else:
                break  # longer groups ending at j only get bigger
            if best[i] + c < best[j]:
                best[j], back[j] = best[i] + c, (i, shape)
    groups, j = [], n
    while j > 0:
        i, shape = back[j]
        groups.append(([order[x] for x in range(i, j)], shape))
        j = i
    return groups[::-1]


@dataclass
class BatchResult:
    logits: list  # fp32 CPU tensors, one per submitted item, in submission order
    timing: dict  # tokenize_ms, queue_ms, model_ms
    path: str  # "graph" | "eager" | "mixed"
    batch_rows: int  # most real rows in one forward that carried this request
    shapes: list  # per forward: [B, L] (graph) or ["eager", rows, padded length]
    flags: dict = field(default_factory=dict)  # effective flags used


class _Req:
    __slots__ = ("items", "fut", "t_submit", "tok_ms", "wtok_ms", "left", "logits", "t_start", "t_end", "paths",
                 "shapes", "batch_rows", "failed", "flags")

    def __init__(self, items, tok_ms):
        self.items, self.fut, self.t_submit, self.tok_ms = items, Future(), time.perf_counter(), float(tok_ms)
        self.wtok_ms = 0.0  # tokenization done by the worker (legacy): not queue time
        self.left, self.logits = len(items), [None] * len(items)
        self.t_start = self.t_end = None
        self.paths, self.shapes, self.batch_rows, self.failed, self.flags = set(), [], 0, False, None


class BatchingEngine:
    """Thread-safe front of one model runner (fastcore.graphs.FastGraphs or any object with select(k, m, legacy,
    token_budget) and run(seqs, cands, shape, readout) -> (logits, path)). submit(items) -> Future[BatchResult]."""

    def __init__(self, runner, flags: dict | None = None, tokenizer=None, prepare=None, log_size: int = 4096,
                 name="fastcore-gpu", stall_s: float = STALL_S):
        """prepare(items): fills text/ids of items submitted without them (default: tokenize_items with
        `tokenizer`); the engine passes readout.prepare_items so legacy requests render AND tokenize in the worker.
        stall_s: a forward in flight for longer is reported by problems() (hung GPU)."""
        self.runner, self.tok, self.prepare = runner, tokenizer, prepare
        self.stall_s = float(stall_s)
        self._flags = normalize_flags(flags or {})
        self._cv = threading.Condition()
        self._q = collections.deque()
        self._stop = False
        self._dead = None
        self._busy = False
        self._fwd_t0 = None  # perf_counter at the start of the forward in flight (None = no forward running)
        self.forwards = collections.deque(maxlen=log_size)
        self.counts = collections.Counter()
        self._slock = threading.Lock()  # forwards / counts (written by the worker, read by /health)
        self._thread = threading.Thread(target=self._loop, name=name, daemon=True)
        self._thread.start()

    # ------------------------------------------------------------------ public API
    @property
    def flags(self) -> dict:
        with self._cv:
            return dict(self._flags)

    def set_flags(self, update: dict) -> dict:
        """Validate + apply (all or nothing). Returns flags_view of the new flags. Takes effect at the next drain."""
        with self._cv:
            self._flags = normalize_flags(update, self._flags)
            return flags_view(self._flags)

    def submit(self, items, tokenize_ms: float = 0.0) -> Future:
        """Queue one request's work items (ids filled, or None to tokenize in the worker). Returns a Future whose
        result is a BatchResult (logits in `items` order) or whose exception is the worker's error."""
        if not items:
            raise ValueError("submit: no work items")
        r = _Req(list(items), tokenize_ms)
        with self._cv:
            if self._stop or self._dead is not None:
                raise EngineClosed(f"engine worker died: {self._dead!r}" if self._dead is not None
                                   else "engine is shut down")
            self._q.append(r)
            self._cv.notify_all()
        return r.fut

    def run(self, items, tokenize_ms: float = 0.0, timeout: float | None = None) -> BatchResult:
        return self.submit(items, tokenize_ms).result(timeout)

    def shutdown(self, wait: bool = True, timeout: float | None = 30.0) -> bool:
        """Stop accepting work; the worker finishes its current forwards, fails what is still queued with
        EngineClosed, and exits. Returns True when the worker has exited."""
        with self._cv:
            self._stop = True
            self._cv.notify_all()
        if wait and self._thread is not threading.current_thread():
            self._thread.join(timeout)
        return not self._thread.is_alive()

    close = shutdown

    def queued(self) -> dict:
        with self._cv:
            return {"requests": len(self._q), "rows": sum(len(r.items) for r in self._q), "busy": self._busy}

    def stats(self) -> dict:
        with self._slock:
            fw, counts = list(self.forwards), dict(self.counts)
        ms = sorted(x["ms"] for x in fw)
        pick = (lambda q: round(ms[min(len(ms) - 1, int(q * len(ms)))], 3)) if ms else (lambda q: None)
        rows = [x["rows"] for x in fw]
        return {**counts, "forward_ms_p50": pick(0.5), "forward_ms_p95": pick(0.95),
                "rows_per_forward_mean": round(sum(rows) / len(rows), 3) if rows else None,
                "alive": self._thread.is_alive(), "dead": repr(self._dead) if self._dead else None,
                "cuda_fatal": bool(self._dead is not None and is_cuda_fatal(self._dead)),
                "forward_inflight_s": self.inflight_s(), "stall_s": self.stall_s}

    def inflight_s(self):
        """Seconds the forward in flight has run, or None when no forward is running."""
        t0 = self._fwd_t0
        return None if t0 is None else round(time.perf_counter() - t0, 3)

    def problems(self) -> list:
        """Why this engine cannot serve right now (empty = fine): a stopped or dead worker (a CUDA-fatal error stops
        it), or a forward in flight for more than stall_s (a hung GPU)."""
        out = []
        if not self._thread.is_alive():
            if self._dead is not None:
                what = "CUDA context lost" if is_cuda_fatal(self._dead) else "died"
                out.append(f"engine worker stopped ({what}: {self._dead!r})"[:600])
            else:
                out.append("engine worker stopped (shut down)")
        t = self.inflight_s()
        if t is not None and t > self.stall_s:
            out.append(f"a GPU forward has run for {t:.0f} s (> {self.stall_s:.0f} s): the GPU looks hung")
        return out

    # ------------------------------------------------------------------ worker
    def _take(self):
        """Under the lock: wait for work, then pop one request (no cross-batching) or a drain. None = stop."""
        while not self._q and not self._stop:
            self._cv.wait()
        if self._stop:
            return None, None
        f = effective_flags(self._flags)
        if not f["cross_batch"]:
            return [self._q.popleft()], f
        cap = f["max_rows"]
        if f["batch_wait_ms"] > 0:
            deadline = time.perf_counter() + f["batch_wait_ms"] / 1000
            while not self._stop and sum(len(r.items) for r in self._q) < cap:
                left = deadline - time.perf_counter()
                if left <= 0:
                    break
                self._cv.wait(left)
            if self._stop:
                return None, None
        out, rows = [], 0
        while self._q and (not out or rows + len(self._q[0].items) <= cap):
            r = self._q.popleft()
            out.append(r)
            rows += len(r.items)
        return out, f

    def _loop(self):
        try:
            import torch
            torch.set_grad_enabled(False)  # grad mode is thread-local
        except ImportError:  # fake runners in tests
            pass
        reqs = []
        try:
            while True:
                with self._cv:
                    reqs, f = self._take()
                    if reqs is None:
                        break
                    self._busy = True
                try:
                    self._process(reqs, f)
                except Exception as e:  # noqa: BLE001 - a scheduling error fails this drain, not the engine
                    for r in reqs:
                        self._fail(r, e)
                finally:
                    with self._cv:
                        self._busy = False
        except BaseException as e:  # noqa: BLE001 - a dead worker must not leave callers waiting
            self._dead = e.err if isinstance(e, _Poisoned) else e
            traceback.print_exc()
            for r in reqs or []:
                self._fail(r, EngineClosed(f"engine worker died: {self._dead!r}"))
        finally:
            with self._cv:
                self._stop = True
                rest = list(self._q)
                self._q.clear()
            err = EngineClosed("engine shut down before this request ran") if self._dead is None else \
                EngineClosed(f"engine worker died: {self._dead!r}")
            for r in rest:
                if not r.fut.done():
                    r.fut.set_exception(err)

    def _tokenize(self, reqs):
        from .readout import tokenize_items
        for r in reqs:
            todo = [it for it in r.items if it.ids is None]
            if todo:
                if self.prepare is None and self.tok is None:
                    raise RuntimeError("work items without token ids and no tokenizer/prepare given to BatchingEngine")
                t = time.perf_counter()
                if self.prepare is not None:
                    self.prepare(todo)
                else:
                    tokenize_items(self.tok, todo)
                dt = (time.perf_counter() - t) * 1000
                r.tok_ms += dt
                r.wtok_ms += dt

    def _process(self, reqs, f):
        for r in reqs:
            r.flags = f
        try:
            self._tokenize(reqs)
        except Exception as e:  # noqa: BLE001
            for r in reqs:
                self._fail(r, e)
            return
        legacy = f["graph_plan"] == "legacy"
        work = []  # [(list of (req, item index)), shape]
        if not f["twoview_split"]:  # one request = one batch (A0)
            for r in reqs:
                m = max(it.n_tokens for it in r.items)
                work.append(([(r, i) for i in range(len(r.items))], self.runner.select(len(r.items), m, legacy=legacy)))
        elif not f["cross_batch"]:  # A1: every item its own batch-1 forward
            for r in reqs:
                for i, it in enumerate(r.items):
                    work.append(([(r, i)], self.runner.select(1, it.n_tokens, legacy=legacy)))
        else:  # A2: one sorted, cut drain
            flat = [(r, i) for r in reqs for i in range(len(r.items))]
            lengths = [r.items[i].n_tokens for r, i in flat]
            budget = f["token_budget"]
            sel = (lambda k, m: self.runner.select(k, m, legacy=legacy, token_budget=budget))
            for idx, shape in plan_batches(lengths, sel, f["max_rows"], budget, f):
                work.append(([flat[x] for x in idx], shape))
        for members, shape in work:
            live = [(r, i) for r, i in members if not r.failed]
            if not live:
                continue
            err = self._forward(live, shape, f)
            if err is None:
                continue
            owners = list({id(r): r for r, _ in live}.values())
            if len(owners) == 1:
                self._fail(owners[0], err)
                continue
            for r in owners:  # isolate: a forward shared by several requests is retried per request
                mine = [(q, i) for q, i in live if q is r]
                m = max(r.items[i].n_tokens for _, i in mine)
                e2 = self._forward(mine, self.runner.select(len(mine), m, legacy=legacy,
                                                            token_budget=f["token_budget"]), f)
                if e2 is not None:
                    self._fail(r, e2)
        for r in reqs:
            if not r.fut.done():
                self._fail(r, RuntimeError("internal: request left without a result"))

    def _forward(self, live, shape, f):
        """Run one forward for [(request, item index)]; deliver logits; finish completed requests. Returns None, or
        the exception (nothing delivered)."""
        t0 = time.perf_counter()
        for r, _ in live:
            if r.t_start is None:
                r.t_start = t0
        seqs = [r.items[i].ids for r, i in live]
        cands = [(r.items[i].flat, r.items[i].sizes) for r, i in live]
        self._fwd_t0 = t0
        try:
            logits, path = self.runner.run(seqs, cands, shape, readout=f["readout"])
            if len(logits) != len(live):
                raise RuntimeError(f"runner returned {len(logits)} rows for {len(live)}")
        except Exception as e:  # noqa: BLE001 - the caller fails or retries exactly the requests in this forward
            self._count(forward_errors=1)
            if is_cuda_fatal(e):  # the CUDA context is poisoned: no retry, stop the worker (see _loop)
                self._count(cuda_fatal_errors=1)
                raise _Poisoned(e) from e
            return e
        finally:
            self._fwd_t0 = None
        t1 = time.perf_counter()
        mlen = max(len(x) for x in seqs)
        desc = list(shape) if shape is not None else ["eager", len(live), eager_len(mlen)]
        with self._slock:
            self.forwards.append({"rows": len(live), "shape": desc, "path": path, "ms": (t1 - t0) * 1000})
        self._count(forwards=1, rows=len(live), real_tokens=sum(len(x) for x in seqs),
                    padded_tokens=shape[0] * shape[1] if shape is not None else len(live) * eager_len(mlen),
                    **{f"{path}_forwards": 1})
        for (r, i), lg in zip(live, logits):
            r.logits[i] = lg
            r.left -= 1
            r.paths.add(path)
            r.batch_rows = max(r.batch_rows, len(live))
        for r in {id(r): r for r, _ in live}.values():
            r.shapes.append(desc)
            if r.left == 0 and not r.failed:
                r.t_end = t1
                self._finish(r)
        return None

    def _count(self, **kw):
        with self._slock:
            self.counts.update(kw)

    def _finish(self, r):
        self._count(requests=1)
        timing = {"tokenize_ms": round(r.tok_ms, 3),
                  "queue_ms": round(max(0.0, (r.t_start - r.t_submit) * 1000 - r.wtok_ms), 3),
                  "model_ms": round((r.t_end - r.t_start) * 1000, 3)}
        path = next(iter(r.paths)) if len(r.paths) == 1 else "mixed"
        r.fut.set_result(BatchResult(logits=r.logits, timing=timing, path=path, batch_rows=r.batch_rows,
                                     shapes=r.shapes, flags=r.flags))

    def _fail(self, r, e):
        if r.fut.done():
            return
        r.failed = True
        self._count(request_errors=1)
        if not r.fut.done():
            r.fut.set_exception(e)
