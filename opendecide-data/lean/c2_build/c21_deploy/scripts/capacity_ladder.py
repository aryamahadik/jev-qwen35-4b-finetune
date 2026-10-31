"""capacity_ladder.py (M2 + M3): the capacity curve of the serving path on the box it runs on, and an open-loop check of it.

M2, closed-loop LADDER: for c in --concs (default 1,2,4,8,16,32,64) run the N workload (660 traffic-like dev decisions, each
once, caches flushed before every level) with c threads back to back, --runs times. Per level: decisions/hour (ok calls over
the makespan, the definition of oc1.measure.loop_summary), the per-decision latency p50/p90/p95/p99 as seen by a LOOPBACK client
(= server-side: no network), failed calls, GPU busy share, cached-token share. The output `points` block pastes straight into
inputs/capacity_curves.json (curve l4_gcp_s1) and feeds batching_plan.py and cost_calc.py (T_sat = the best level with 0 failed
calls). Same definitions as the 17 Oct H100 arm A (N c64 = 325,826 decisions/h), so L4 and H100 are comparable.

M3, OPEN-LOOP validation: Poisson arrivals at --open-fracs x T_sat (T_sat from the ladder just measured, or --tsat-dph) for
--open-secs each, one fresh decision per arrival drawn from the P set (no repeats within a level), latency measured from the
SCHEDULED arrival (so client-side lag cannot hide queueing; the lag itself is reported and must be ~0). This is what batching_plan.py
validate compares with the ladder-based prediction.

Runs only inside an authorised window (LD_WINDOW), against a server we started (never port 30000), with the round-2 harness (oc1,
read-only) importing the S1 readout exactly like r2_trial.py does.

  LD_WINDOW=W1 capacity_ladder.py --port 30010 --tokenizer ~/lean/models/q35_4b_main500k --work-dir ~/opt_r2/data \\
        --oc1-parent ~/opt_r2 --phases ladder,open --out out/capacity_L4.json
  capacity_ladder.py --selftest           (in-process fake server; CPU)
"""
from __future__ import annotations

import argparse
import queue
import random
import subprocess
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402


# ------------------------------------------------------------------ generic load machinery (read(prep) -> meta dict)
class GpuSampler:
    def __init__(self, interval=0.5):
        self.interval, self.samples, self._stop, self._t = interval, [], threading.Event(), None

    def _poll(self):
        while not self._stop.is_set():
            try:
                o = subprocess.run(["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,power.draw,clocks.sm",
                                    "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=5).stdout.strip().splitlines()[0]
                u, m, p, c = [float(x) for x in o.split(",")]
                self.samples.append((time.time(), u, m, p, c))
            except (OSError, subprocess.SubprocessError, ValueError, IndexError):
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

    def between(self, t0, t1):
        xs = [s for s in self.samples if t0 <= s[0] <= t1]
        if not xs:
            return {"n": 0}
        return {"n": len(xs), "util_mean": round(sum(s[1] for s in xs) / len(xs), 1), "mem_mib_max": max(s[2] for s in xs),
                "power_w_mean": round(sum(s[3] for s in xs) / len(xs), 1), "sm_mhz_mean": round(sum(s[4] for s in xs) / len(xs))}


def closed_loop(read, preps, conc: int):
    """`conc` threads, each call back to back, every prep once. -> (records, wall_s). Record: ms, ok, err, meta."""
    n, lock, nxt, recs = len(preps), threading.Lock(), [0], []
    t_start = time.perf_counter()

    def worker():
        while True:
            with lock:
                i = nxt[0]
                nxt[0] += 1
            if i >= n:
                return
            t0 = time.perf_counter()
            try:
                meta, ok, err = read(preps[i]), True, None
            except Exception as e:  # noqa: BLE001
                meta, ok, err = {}, False, f"{type(e).__name__}: {str(e)[:120]}"
            ms = (time.perf_counter() - t0) * 1000.0
            with lock:
                recs.append({"i": i, "ms": ms, "ok": ok, "err": err, "meta": meta or {}})

    th = [threading.Thread(target=worker, daemon=True) for _ in range(max(1, conc))]
    for t in th:
        t.start()
    for t in th:
        t.join()
    return recs, time.perf_counter() - t_start


def summarize_level(recs, wall, conc) -> dict:
    ok = [r for r in recs if r["ok"]]
    cached = sum(r["meta"].get("cached_tokens") or 0 for r in ok)
    prompt = sum(r["meta"].get("prompt_tokens") or 0 for r in ok)
    return {"c": conc, "calls": len(recs), "ok": len(ok), "failed": len(recs) - len(ok), "wall_s": round(wall, 2),
            "dph": round(len(ok) / wall * 3600.0) if ok and wall > 0 else None,
            "latency_ms": C.summarize([r["ms"] for r in ok]),
            "cached_token_share": round(cached / prompt, 4) if prompt else None,
            "errors": sorted({r["err"] for r in recs if not r["ok"]})[:3]}


def ladder(read, preps, concs, runs: int = 2, flush=None, sampler=None, log=print) -> dict:
    levels = []
    for c in concs:
        for run in range(1, runs + 1):
            if flush:
                flush()
            t0 = time.time()
            recs, wall = closed_loop(read, preps, c)
            s = summarize_level(recs, wall, c)
            s["run"] = run
            if sampler:
                s["gpu"] = sampler.between(t0, time.time())
            levels.append(s)
            log(f"c={c} run {run}: {s['ok']}/{s['calls']} ok, {s['dph']} dec/h, p50 {s['latency_ms'].get('p50')} p95 {s['latency_ms'].get('p95')} ms")
    return {"levels": levels, "points": points_from(levels), "t_sat": t_sat_from(levels)}


def points_from(levels) -> list:
    """One point per c for capacity_curves.json: dph = mean over runs, latency from the pooled worst run (conservative)."""
    out = []
    for c in sorted({l["c"] for l in levels}):
        ls = [l for l in levels if l["c"] == c and l["dph"] and not l["failed"]]
        if not ls:
            continue
        out.append({"c": c, "dph": round(sum(l["dph"] for l in ls) / len(ls)), "p50_ms": max(l["latency_ms"]["p50"] for l in ls),
                    "p95_ms": max(l["latency_ms"]["p95"] for l in ls), "n": sum(l["ok"] for l in ls)})
    return out


def t_sat_from(levels):
    pts = points_from(levels)
    return max((p["dph"] for p in pts), default=None)


def open_loop(read, preps, dph: float, duration_s: float, seed: int = 0, pool: int = 256, flush=None, sampler=None,
              lag_tol_ms: float = 5.0) -> dict:
    """Poisson arrivals at `dph` decisions/hour for duration_s; latency from the scheduled arrival; each prep used at most once."""
    rate = dph / 3600.0
    rng = random.Random(seed)
    t, times = 0.0, []
    while True:
        t += rng.expovariate(rate)
        if t >= duration_s:
            break
        times.append(t)
    order = list(range(len(preps)))
    rng.shuffle(order)
    if len(times) > len(order):
        times = times[: len(order)]
    if flush:
        flush()
    recs, lock = [], threading.Lock()
    q: queue.Queue = queue.Queue()
    g0 = time.time()
    t0 = time.perf_counter() + 0.2           # the workers are started before the first arrival

    def worker():
        while True:
            k = q.get()
            if k is None:
                return
            sched = t0 + times[k]
            start = time.perf_counter()
            try:
                meta, ok, err = read(preps[order[k]]), True, None
            except Exception as e:  # noqa: BLE001
                meta, ok, err = {}, False, f"{type(e).__name__}: {str(e)[:120]}"
            end = time.perf_counter()
            with lock:
                recs.append({"ms": (end - sched) * 1000.0, "svc_ms": (end - start) * 1000.0, "lag_ms": (start - sched) * 1000.0,
                             "ok": ok, "err": err, "meta": meta or {}})

    workers = [threading.Thread(target=worker, daemon=True) for _ in range(pool)]
    for w in workers:
        w.start()
    for k, tk in enumerate(times):             # one scheduler thread releases each arrival at its time
        d = t0 + tk - time.perf_counter()
        if d > 0:
            time.sleep(d)
        q.put(k)
    for _ in workers:
        q.put(None)
    for w in workers:
        w.join()
    wall = time.perf_counter() - t0
    ok = [r for r in recs if r["ok"]]
    out = {"target_dph": round(dph), "duration_s": round(wall, 1), "calls": len(recs), "ok": len(ok), "failed": len(recs) - len(ok),
           "achieved_dph": round(len(ok) / duration_s * 3600.0) if ok else None,
           "p50_ms": C.pct([r["ms"] for r in ok], 0.5), "p95_ms": C.pct([r["ms"] for r in ok], 0.95),
           "p99_ms": C.pct([r["ms"] for r in ok], 0.99), "latency_ms": C.summarize([r["ms"] for r in ok]),
           "client_lag_ms": C.summarize([r["lag_ms"] for r in ok]), "errors": sorted({r["err"] for r in recs if not r["ok"]})[:3]}
    out["lag_ok"] = bool(ok) and (C.pct([r["lag_ms"] for r in ok], 0.99) or 0) < lag_tol_ms
    if sampler:
        out["gpu"] = sampler.between(g0, time.time())
    return out


# ------------------------------------------------------------------ selftest with an in-process fake server
def _fake_read(service_s=0.002, slots=4):
    sem = threading.Semaphore(slots)

    def read(prep):
        with sem:
            time.sleep(service_s)
        return {"prompt_tokens": 100, "cached_tokens": 0}
    return read


def selftest():
    read = _fake_read(service_s=0.02, slots=4)
    preps = list(range(120))
    lad = ladder(read, preps, (1, 4, 8), runs=1, log=lambda *_: None)
    pts = {p["c"]: p for p in lad["points"]}
    assert pts[4]["dph"] > 2.5 * pts[1]["dph"], pts          # 4 slots: four threads serve about 4x one
    assert abs(pts[8]["dph"] - pts[4]["dph"]) < 0.35 * pts[4]["dph"], pts       # saturated at 4 slots
    ol = open_loop(read, list(range(400)), dph=0.5 * lad["t_sat"], duration_s=2.0, seed=1, lag_tol_ms=1000.0)
    assert ol["lag_ok"] and ol["failed"] == 0 and ol["achieved_dph"] > 0.3 * lad["t_sat"], ol
    print("selftest ok", pts[1]["dph"], pts[4]["dph"], pts[8]["dph"])


# ------------------------------------------------------------------ the VM run
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--port", type=int)
    ap.add_argument("--tokenizer")
    ap.add_argument("--work-dir")
    ap.add_argument("--oc1-parent")
    ap.add_argument("--phases", default="ladder,open")
    ap.add_argument("--concs", default="1,2,4,8,16,32,64")
    ap.add_argument("--runs", type=int, default=2)
    ap.add_argument("--open-fracs", default="0.25,0.5,0.6,0.75,0.9")
    ap.add_argument("--open-secs", type=float, default=120.0)
    ap.add_argument("--tsat-dph", type=float, help="open-loop reference throughput when the ladder is not run in this call")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    if not (a.port and a.tokenizer and a.work_dir and a.oc1_parent and a.out):
        ap.error("--port --tokenizer --work-dir --oc1-parent --out are required")
    C.refuse_prod_port(a.port, "the capacity ladder")
    window = C.require_window()
    for p in (a.tokenizer, a.work_dir, a.oc1_parent):
        C.refuse_ohs(p)
    for p in (a.oc1_parent, str(Path(a.oc1_parent) / "hosting"), str(Path.home() / "lean" / "hosting"), str(Path.home() / "lean"),
              str(C.LEAN / "hosting"), str(C.LEAN)):
        if Path(p).exists() and p not in sys.path:
            sys.path.insert(0, p)
    from oc1 import items as I  # noqa: E402
    from oc1.backend import GenerateBackend  # noqa: E402
    R = I.readout_mod()
    SH = I.sglang_host_mod()
    tok, ro, info = I.load_c1(a.tokenizer)
    client = SH.SGLangClient(f"http://127.0.0.1:{a.port}", 300.0)
    if not client.alive():
        raise SystemExit(f"server on {a.port} is not healthy")
    backend = GenerateBackend(client)

    def read(prep):
        return backend.read(prep, False)[1]

    def flush():
        try:
            client.flush()
        except Exception:  # noqa: BLE001
            pass

    def prep_set(name):
        its = C.read_jsonl(Path(a.work_dir) / f"{name}.jsonl")
        return I.prepare_cached(name, its, R, ro, tok)

    res = {"window": window, "utc": C.utc(), "port": a.port, "server_info_keys": {}, "phases": {}}
    try:
        si = client.server_info()
        res["server_info_keys"] = {k: si.get(k) for k in ("version", "attention_backend", "mem_fraction_static", "dtype", "quantization",
                                                         "max_running_requests", "enable_fp32_lm_head", "disable_radix_cache") if k in si}
    except Exception as e:  # noqa: BLE001
        res["server_info_keys"] = {"error": str(e)[:100]}
    phases = a.phases.split(",")
    with GpuSampler(0.5) as sampler:
        prepsN = prep_set("N")
        for p in prepsN[:30]:                                     # warm-up, discarded
            read(p)
        if "ladder" in phases:
            res["phases"]["ladder"] = ladder(read, prepsN, [int(x) for x in a.concs.split(",")], runs=a.runs, flush=flush, sampler=sampler)
            res["tag_ladder"] = C.tag("author-run", n=len(prepsN) * a.runs, source=f"capacity_ladder.py N workload, window {window}")
        if "open" in phases:
            tsat = a.tsat_dph or res["phases"].get("ladder", {}).get("t_sat")
            if not tsat:
                raise SystemExit("open-loop needs T_sat: run the ladder phase in the same call or pass --tsat-dph")
            prepsP = prep_set("P")
            lv = []
            for f in [float(x) for x in a.open_fracs.split(",")]:
                r = open_loop(read, prepsP, f * tsat, a.open_secs, seed=int(f * 100), flush=flush, sampler=sampler)
                r["frac_of_tsat"] = f
                lv.append(r)
                print(f"open {f}: target {r['target_dph']} achieved {r['achieved_dph']} dph p50 {r['p50_ms']} p95 {r['p95_ms']} ms lag_ok {r['lag_ok']}", flush=True)
            res["phases"]["open"] = {"tsat_dph": tsat, "levels": lv}
            res["tag_open"] = C.tag("author-run", n=sum(l["ok"] for l in lv), source=f"capacity_ladder.py open-loop P workload, window {window}")
    C.write_json(a.out, res)
    return 0


if __name__ == "__main__":
    sys.exit(main())
