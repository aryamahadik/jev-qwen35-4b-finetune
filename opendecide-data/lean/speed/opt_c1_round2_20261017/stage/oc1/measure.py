"""oc1.measure: the GPU-side measurements of one SGLang boot, on pre-tokenized dev decisions.

  closed_loop(read, preps, conc)     c threads, calls back to back, makespan + per-call records (no call repeats)
  parity_pass(...)                   one read per decision (the same readout as arm S1) -> answers {id: probs} + views
  latency_batch1(...)                one decision at a time, warm, wall ms of the HTTP call (+ the server's own e2e)
  latency_batched(...)               B decisions in ONE /generate call (the "batch of 8" timing) and B simultaneous calls
  throughput(...)                    closed loop at c = 16 / 64 / 128 on a set: decisions/h, GPU busy share
  prefix_hit(...)                    cached-token share on the repeated-schema set R (prompts AS TRAINED)
  GpuSampler                         nvidia-smi utilisation / memory / power while a measurement runs

Timing note: "GPU-timed" here = the wall time of a blocking localhost HTTP call that returns only after the logits are on
the host (so the GPU work is complete: implicitly synchronised), tokenization excluded (done before), the server's
own e2e_latency reported next to it. Nothing here touches the network beyond 127.0.0.1.
"""
from __future__ import annotations

import subprocess
import threading
import time
from collections import defaultdict

from . import common as C
from . import parity as PAR


# ------------------------------------------------------------------ GPU sampler
class GpuSampler:
    """Polls nvidia-smi every `interval` s in a thread. No GPU / no nvidia-smi = empty samples (CPU tests)."""

    QUERY = "utilization.gpu,memory.used,power.draw,clocks.sm"

    def __init__(self, interval: float = 0.5, cmd=None):
        self.interval, self.samples, self._stop = interval, [], threading.Event()
        self.cmd = cmd or ["nvidia-smi", f"--query-gpu={self.QUERY}", "--format=csv,noheader,nounits"]
        self._t = None

    def _poll(self):
        while not self._stop.is_set():
            t = time.time()
            try:
                out = subprocess.run(self.cmd, capture_output=True, text=True, timeout=5).stdout.strip().splitlines()[0]
                u, m, p, c = [float(x) for x in out.split(",")]
                self.samples.append((t, u, m, p, c))
            except Exception:  # noqa: BLE001
                pass
            self._stop.wait(self.interval)

    def __enter__(self):
        self._t = threading.Thread(target=self._poll, daemon=True)
        self._t.start()
        return self

    def __exit__(self, *a):
        self._stop.set()
        if self._t:
            self._t.join(timeout=5)

    def between(self, t0: float, t1: float) -> dict:
        xs = [s for s in self.samples if t0 <= s[0] <= t1]
        if not xs:
            return {"n": 0}
        u = [s[1] for s in xs]
        return {"n": len(xs), "util_mean": round(sum(u) / len(u), 1), "util_p95": C.pct(u, 0.95),
                "mem_mib_max": max(s[2] for s in xs), "power_w_mean": round(sum(s[3] for s in xs) / len(xs), 1),
                "sm_mhz_mean": round(sum(s[4] for s in xs) / len(xs), 0)}


# ------------------------------------------------------------------ closed loop
def closed_loop(read, preps: list, conc: int, warm_n: int = 0, return_views: bool = False, max_s: float | None = None):
    """Run `read(prep, return_views)` over `preps` (each once) with `conc` threads, back to back. Returns
    (records, wall_s) with records in completion order: {i, id, t0, t1, ms, ok, err, answers, meta}."""
    n = len(preps)
    lock = threading.Lock()
    nxt = [0]
    recs = []
    t_start = time.perf_counter()
    abort = threading.Event()

    def worker():
        while not abort.is_set():
            with lock:
                i = nxt[0]
                nxt[0] += 1
            if i >= n:
                return
            p = preps[i]
            t0 = time.perf_counter()
            try:
                ans, meta = read(p, return_views)
                ok, err = True, None
            except Exception as e:  # noqa: BLE001
                ans, meta, ok, err = None, {}, False, f"{type(e).__name__}: {str(e)[:200]}"
            t1 = time.perf_counter()
            with lock:
                recs.append({"i": i, "id": p.id, "t0": t0 - t_start, "t1": t1 - t_start, "ms": (t1 - t0) * 1000.0,
                             "ok": ok, "err": err, "answers": ans, "meta": meta, "bucket": p.bucket,
                             "n_tokens": p.n_tokens})
            if max_s is not None and time.perf_counter() - t_start > max_s:
                abort.set()

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(max(1, conc))]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    wall = time.perf_counter() - t_start
    return recs, wall


def loop_summary(recs: list, wall_s: float, warm_n: int = 0) -> dict:
    ok = [r for r in recs if r["ok"]]
    done = sorted(ok, key=lambda r: r["t1"])
    if warm_n and len(done) > warm_n + 1:      # rate from the (warm_n+1)-th completion on
        t_ref = done[warm_n - 1]["t1"]
        timed = done[warm_n:]
        span = max(timed[-1]["t1"] - t_ref, 1e-9)
    else:
        timed, span = done, max(wall_s, 1e-9)
    ms = [r["ms"] for r in timed]
    n_t = len(timed)
    tok = sum(r["n_tokens"] for r in timed)
    return {"calls": len(recs), "ok": len(ok), "failed": len(recs) - len(ok), "wall_s": round(wall_s, 2),
            "decisions_per_h": round(n_t / span * 3600.0, 0) if n_t else None,
            "tokens_per_s": round(tok / span, 0) if n_t else None, "latency_ms": C.summarize(ms),
            "errors": sorted({r["err"] for r in recs if not r["ok"]})[:3]}


# ------------------------------------------------------------------ measurements
def flush(client):
    try:
        return client.flush()
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


def parity_pass(backend, preps: list, conc: int = 16, sampler=None) -> dict:
    """Every decision once (view-level answers kept). -> {"answers": {id: {"probs", "views"}}, "summary", "meta"}."""
    from .backend import answer_probs
    t0w = time.time()
    recs, wall = closed_loop(backend.read, preps, conc, return_views=True)
    answers, missing = {}, []
    qtype = {p.id: p.qtype for p in preps}
    cached = prompt = 0
    for r in recs:
        if not r["ok"]:
            missing.append({"id": r["id"], "err": r["err"]})
            continue
        ans = r["answers"]["q0"] if "q0" in r["answers"] else next(iter(r["answers"].values()))
        a = {"probs": answer_probs(ans, qtype[r["id"]])}
        if ans.get("view_probabilities"):
            a["views"] = ans["view_probabilities"]
        answers[r["id"]] = a
        m = r["meta"]
        cached += m.get("cached_tokens") or 0
        prompt += m.get("prompt_tokens") or 0
    out = {"answers": answers, "missing": missing[:20], "n_missing": len(missing),
           "summary": loop_summary(recs, wall), "cached_token_share": round(cached / prompt, 4) if prompt else None}
    if sampler is not None:
        out["gpu"] = sampler.between(t0w, time.time())
    return out


def latency_batch1(backend, preps: list, warm: int = 20, sampler=None) -> dict:
    """One decision at a time on a warm server. Reports wall ms of the call, the server's e2e, tokens, by bucket."""
    t0w = time.time()
    rows = []
    for i, p in enumerate(preps):
        t0 = time.perf_counter()
        try:
            _, meta = backend.read(p, False)
            ok = True
        except Exception as e:  # noqa: BLE001
            meta, ok = {"err": f"{type(e).__name__}: {str(e)[:120]}"}, False
        ms = (time.perf_counter() - t0) * 1000.0
        if i >= warm:
            rows.append({"ms": ms, "ok": ok, "bucket": p.bucket, "tok": p.n_tokens, "e2e": meta.get("server_e2e_ms"),
                         "cached": meta.get("cached_tokens"), "prompt": meta.get("prompt_tokens")})
    good = [r for r in rows if r["ok"]]
    by = defaultdict(list)
    for r in good:
        by["noul" if r["bucket"] == "noul" else "choice"].append(r["ms"])
    out = {"n": len(good), "failed": len(rows) - len(good), "wall_ms": C.summarize([r["ms"] for r in good]),
           "server_e2e_ms": C.summarize([r["e2e"] for r in good if r["e2e"] is not None]),
           "by_type": {k: C.summarize(v) for k, v in by.items()},
           "mean_tokens": round(sum(r["tok"] for r in good) / len(good), 1) if good else None}
    if sampler is not None:
        out["gpu"] = sampler.between(t0w, time.time())
    return out


def latency_batched(backend, preps: list, b: int = 8, rounds: int = 40, warm_rounds: int = 3, conc_rounds: bool = True) -> dict:
    """(1) B decisions in ONE call (backend.read_many): ms per call and ms per decision.
       (2) B simultaneous calls from B threads (a barrier starts each round): per-call latency and round makespan."""
    out = {"b": b}
    groups = [preps[i * b:(i + 1) * b] for i in range(len(preps) // b)][: rounds + warm_rounds]
    if hasattr(backend, "read_many") and groups:
        ms = []
        for gi, g in enumerate(groups):
            t0 = time.perf_counter()
            try:
                backend.read_many(g)
            except Exception:  # noqa: BLE001
                continue
            if gi >= warm_rounds:
                ms.append((time.perf_counter() - t0) * 1000.0)
        out["one_call"] = {"call_ms": C.summarize(ms), "per_decision_ms": C.summarize([x / b for x in ms])}
    if conc_rounds and groups:
        per, mk = [], []
        for gi, g in enumerate(groups):
            bar = threading.Barrier(len(g))
            res = [None] * len(g)

            def one(k, p=None):
                bar.wait()
                t0 = time.perf_counter()
                try:
                    backend.read(g[k], False)
                    res[k] = (time.perf_counter() - t0) * 1000.0
                except Exception:  # noqa: BLE001
                    res[k] = None

            th = [threading.Thread(target=one, args=(k,)) for k in range(len(g))]
            t0 = time.perf_counter()
            for t in th:
                t.start()
            for t in th:
                t.join()
            if gi >= warm_rounds and all(x is not None for x in res):
                per += res
                mk.append((time.perf_counter() - t0) * 1000.0)
        out["simultaneous"] = {"per_call_ms": C.summarize(per), "round_ms": C.summarize(mk),
                               "per_decision_ms": C.summarize([x / b for x in mk])}
    return out


def throughput(backend, preps: list, conc_list=(16, 64), flush_between: bool = True, client=None, sampler=None,
               warm_n: int = 20) -> dict:
    """Closed loop on `preps` once per concurrency (caches flushed before each): decisions/h and tokens/s of the whole
    makespan, the GPU busy share, failed calls."""
    out = {}
    for c in conc_list:
        if flush_between and client is not None:
            flush(client)
        t0w = time.time()
        recs, wall = closed_loop(backend.read, preps, c)
        s = loop_summary(recs, wall)
        s["whole_set_decisions_per_h"] = round(s["ok"] / wall * 3600.0, 0) if wall else None
        if sampler is not None:
            s["gpu"] = sampler.between(t0w, time.time())
        cached = sum((r["meta"].get("cached_tokens") or 0) for r in recs if r["ok"])
        prompt = sum((r["meta"].get("prompt_tokens") or 0) for r in recs if r["ok"])
        s["cached_token_share"] = round(cached / prompt, 4) if prompt else None
        out[f"c{c}"] = s
    return out


def prefix_hit(backend, preps_r: list, client=None, conc: int = 8, n: int = 800) -> dict:
    """Cached-token share on the repeated-schema set R (several rows share the schema/instruction prefix; the prompt is
    sent exactly as trained). Cache flushed first; rows sent once each."""
    if client is not None:
        flush(client)
    recs, wall = closed_loop(backend.read, preps_r[:n], conc)
    ok = [r for r in recs if r["ok"]]
    cached = sum((r["meta"].get("cached_tokens") or 0) for r in ok)
    prompt = sum((r["meta"].get("prompt_tokens") or 0) for r in ok)
    return {"rows": len(ok), "failed": len(recs) - len(ok), "conc": conc, "cached_token_share": round(cached / prompt, 4) if prompt else None,
            "cached_tokens": cached, "prompt_tokens": prompt, "summary": loop_summary(recs, wall)}


def parity_vs(items: list, cand: dict, ref: dict) -> dict:
    """compare_items on {id: probs} dicts (the answers of two runs)."""
    return PAR.compare_items(items, cand, ref)
