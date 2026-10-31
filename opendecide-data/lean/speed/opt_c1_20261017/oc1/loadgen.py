"""oc1.loadgen: the end-to-end load client (runs on the LAPTOP; one client location for ours and for Jev).

  * open-loop Poisson arrivals at a given QPS (exponential gaps, seeded), a worker pool with one keep-alive httpx
    connection per worker (a fraction of requests uses a brand-new connection to measure DNS+TCP+TLS)
  * per-request stage timing from httpcore's trace events:
        connect_ms (DNS+TCP) / tls_ms  (new connections only)     client_prep_ms (encode + pool)   send_ms
        wait_ms   (request sent -> first response byte = network RTT + everything the server does)   recv_ms   decode_ms
        total_ms  (the full call, as a user would time it)        client_queue_ms (arrival -> a free worker: must be ~0)
    and from the server's own answer: tokenize / queue / coalesce_wait / sglang call / readout / server_ms /
        sglang e2e (its scheduler queue + GPU), cached tokens; network_ms = wait_ms - server_ms (>= 0)
  * levels (QPS x batching wait x connection mix), per-level server marks (GPU busy share, front CPU cores)
  * same-client Jev sample: speed_bench.JevS (OpenRouter, typesafe/jev-1.13 or the router), interleaved with ours at c=1
Stdlib + httpx only (+ speed_bench for Jev). No row text is ever printed.
"""
from __future__ import annotations

import json
import random
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import httpx

from . import common as C

STAGES = ("total_ms", "wait_ms", "network_ms", "server_ms", "tokenize_ms", "queue_ms", "coalesce_wait_ms", "sglang_call_ms",
          "sglang_e2e_ms", "readout_ms", "connect_ms", "tls_ms", "send_ms", "recv_ms", "decode_ms", "client_prep_ms",
          "client_queue_ms")


class Trace:
    """httpcore trace callback: first timestamp of each event (perf_counter seconds)."""

    def __init__(self):
        self.t = {}

    def __call__(self, name, info):
        self.t.setdefault(name, time.perf_counter())

    def span(self, a, b):
        x, y = self.t.get(a), self.t.get(b)
        return (y - x) * 1000.0 if x is not None and y is not None else None


def make_client(base_url: str, token: str | None, timeout: float = 60.0) -> httpx.Client:
    tr = httpx.HTTPTransport(retries=0, socket_options=[(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)])
    hdr = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.Client(base_url=base_url.rstrip("/"), transport=tr, timeout=timeout, headers=hdr)


def timed_post(client: httpx.Client, path: str, body: dict) -> dict:
    """POST json, return a record with the stage timings of this call (see module docstring)."""
    tr = Trace()
    t_start = time.perf_counter()
    rec = {"ok": False, "status": None, "error": None}
    try:
        r = client.post(path, json=body, extensions={"trace": tr})
        t_resp = time.perf_counter()
        rec["status"] = r.status_code
        t_d0 = time.perf_counter()
        d = r.json() if r.status_code == 200 else None
        t_end = time.perf_counter()
        rec["ok"] = r.status_code == 200 and d is not None
        if r.status_code != 200:
            rec["error"] = f"HTTP {r.status_code}"
    except Exception as e:  # noqa: BLE001
        t_end = time.perf_counter()
        rec["error"] = f"{type(e).__name__}: {str(e)[:120]}"
        rec["total_ms"] = (t_end - t_start) * 1000.0
        return rec
    first = min([v for k, v in tr.t.items() if k.startswith(("connection.connect_tcp.started", "http11.send_request_headers.started"))]
                or [t_start])
    rec.update({
        "total_ms": (t_end - t_start) * 1000.0,
        "connect_ms": tr.span("connection.connect_tcp.started", "connection.connect_tcp.complete"),
        "tls_ms": tr.span("connection.start_tls.started", "connection.start_tls.complete"),
        "client_prep_ms": (first - t_start) * 1000.0,
        "send_ms": tr.span("http11.send_request_headers.started", "http11.send_request_body.complete"),
        "wait_ms": tr.span("http11.send_request_body.complete", "http11.receive_response_headers.complete"),
        "recv_ms": tr.span("http11.receive_response_headers.complete", "http11.receive_response_body.complete"),
        "decode_ms": (t_end - t_d0) * 1000.0,
    })
    if rec["ok"]:
        tm = d.get("timing") or {}
        rec.update({"server_ms": d.get("server_ms"), "tokenize_ms": tm.get("tokenize_ms"), "queue_ms": tm.get("queue_ms"),
                    "coalesce_wait_ms": tm.get("coalesce_wait_ms"), "sglang_call_ms": tm.get("sglang_call_ms"),
                    "readout_ms": tm.get("readout_ms"), "model_ms": tm.get("model_ms"),
                    "sglang_e2e_ms": (d.get("sglang") or {}).get("e2e_ms"),
                    "cached_tokens": (d.get("usage") or {}).get("cached_tokens"),
                    "input_tokens": (d.get("usage") or {}).get("input_tokens"), "batch_rows": d.get("batch_rows")})
        if rec.get("wait_ms") is not None and rec.get("server_ms") is not None:
            rec["network_ms"] = max(rec["wait_ms"] - rec["server_ms"], 0.0)
        rec["answers"] = d.get("answers")
    return rec


class Admin:
    def __init__(self, url, token, timeout=30.0):
        self.c = make_client(url, token, timeout)

    def post(self, path, body=None):
        r = self.c.post(path, json=body or {})
        r.raise_for_status()
        return r.json()

    def get(self, path):
        r = self.c.get(path)
        r.raise_for_status()
        return r.json()

    def close(self):
        self.c.close()


def poisson_times(qps: float, duration_s: float, seed: int) -> list:
    rng = random.Random(seed)
    t, out = 0.0, []
    while True:
        t += rng.expovariate(qps)
        if t >= duration_s:
            return out
        out.append(t)


def summarize_level(recs: list, qps: float, duration_s: float, warm_s: float) -> dict:
    timed = [r for r in recs if r["sched"] >= warm_s]
    ok = [r for r in timed if r["ok"]]
    shed = [r for r in timed if r.get("status") == 503]
    out = {"qps_target": qps, "duration_s": duration_s, "sent": len(timed), "ok": len(ok), "shed_503": len(shed),
           "errors": len(timed) - len(ok) - len(shed),
           "error_examples": sorted({r["error"] for r in timed if not r["ok"] and r.get("status") != 503 and r.get("error")})[:3],
           "qps_achieved": round(len(ok) / max(duration_s - warm_s, 1e-9), 2)}
    for k in STAGES:
        out[k] = C.summarize([r.get(k) for r in ok if r.get(k) is not None])
    fresh = [r for r in ok if r.get("connect_ms") is not None]
    out["new_connections"] = len(fresh)
    if fresh:
        out["total_ms_new_conn"] = C.summarize([r["total_ms"] for r in fresh])
        out["total_ms_keepalive"] = C.summarize([r["total_ms"] for r in ok if r.get("connect_ms") is None])
    cached = sum((r.get("cached_tokens") or 0) for r in ok)
    inp = sum((r.get("input_tokens") or 0) for r in ok)
    out["cached_token_share"] = round(cached / inp, 4) if inp else None
    return out


def run_level(url: str, token: str, requests: list, qps: float, duration_s: float = 40.0, warm_s: float = 4.0,
              seed: int = 0, workers: int = 64, new_conn_frac: float = 0.0, keep_records: bool = False) -> dict:
    """One open-loop level. `requests` = API v1 bodies (consumed in order, never repeated; the list must hold
    >= qps x duration_s of them). Arrivals are scheduled by wall clock; a worker that is still busy delays only that
    request's start (recorded as client_queue_ms)."""
    times = poisson_times(qps, duration_s, seed)
    if len(requests) < len(times):
        raise ValueError(f"{len(times)} arrivals but only {len(requests)} requests (no repeats allowed)")
    tl = threading.local()
    clients, lock = [], threading.Lock()

    def client():
        c = getattr(tl, "c", None)
        if c is None:
            c = make_client(url, token)
            tl.c = c
            with lock:
                clients.append(c)
        return c

    rng = random.Random(seed + 1)
    fresh = [rng.random() < new_conn_frac for _ in times]
    t0 = time.perf_counter()
    recs = []

    def one(i):
        t_start = time.perf_counter()
        sched = times[i]
        if fresh[i]:
            c = make_client(url, token)
            try:
                rec = timed_post(c, "/decide", requests[i])
            finally:
                c.close()
        else:
            rec = timed_post(client(), "/decide", requests[i])
        rec["sched"] = sched
        rec["client_queue_ms"] = max((t_start - t0 - sched) * 1000.0, 0.0)
        rec["i"] = i
        with lock:
            recs.append(rec)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for i, ts in enumerate(times):
            delay = t0 + ts - time.perf_counter()
            if delay > 0:
                time.sleep(delay)
            pool.submit(one, i)
    for c in clients:
        c.close()
    out = summarize_level(recs, qps, duration_s, warm_s)
    out["wall_s"] = round(time.perf_counter() - t0, 1)
    out["seed"] = seed
    if keep_records:      # slim per-request rows (for the hedging simulation and the tail analysis)
        out["records"] = [{k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()
                           if k in ("sched", "total_ms", "wait_ms", "server_ms", "network_ms", "sglang_e2e_ms", "tokenize_ms", "ok",
                                    "status", "connect_ms", "tls_ms", "input_tokens", "client_queue_ms")} for r in recs]
    return out


def e2e_levels(url: str, token: str, requests: list, levels: list, log=print, flush_each: bool = True,
               workers: int = 64) -> list:
    """levels: [{"name", "qps", "duration_s", "wait_ms"?, "new_conn_frac"?, "shed_at"?}]. For each: set the front, flush
    the prefix cache, open a server mark, run the level, close the mark. `requests` are consumed continuously."""
    admin = Admin(url, token)
    out, pos = [], 0
    try:
        for lv in levels:
            n_need = int(lv["qps"] * lv.get("duration_s", 40.0) * 1.15) + 25
            reqs = [requests[(pos + i) % len(requests)] for i in range(n_need)]     # wraps; never repeats inside a level
            pos += n_need
            cfg = {k: lv[k] for k in ("wait_ms", "max_seqs", "max_queue", "shed_at") if k in lv}
            if cfg:
                admin.post("/admin/front", cfg)
            if flush_each:
                try:
                    admin.post("/admin/flush")
                except Exception:  # noqa: BLE001
                    pass
            label = lv.get("name") or f"qps{lv['qps']}"
            admin.post("/admin/mark", {"label": label, "event": "start"})
            res = run_level(url, token, reqs, lv["qps"], lv.get("duration_s", 40.0), lv.get("warm_s", 4.0),
                            seed=lv.get("seed", 0), workers=workers, new_conn_frac=lv.get("new_conn_frac", 0.0),
                            keep_records=bool(lv.get("keep_records")))
            mark = admin.post("/admin/mark", {"label": label, "event": "end"})
            res.update({"name": label, "settings": {k: lv.get(k) for k in ("wait_ms", "max_seqs", "shed_at", "new_conn_frac")},
                        "server_mark": mark})
            out.append(res)
            log(f"  {label}: ok {res['ok']}/{res['sent']} p50 {res['total_ms'].get('p50')} p95 {res['total_ms'].get('p95')} "
                f"p99 {res['total_ms'].get('p99')} ms; server p50 {res['server_ms'].get('p50')}; "
                f"gpu busy {(mark.get('gpu') or {}).get('util_mean')}")
    finally:
        admin.close()
    return out


# ------------------------------------------------------------------ Jev (same client, same prompts)
def jev_client():
    """speed_bench.JevS (OpenRouter route, retries off). The key is read from env / opendecide-data/.env by
    client_bench.load_env and is never printed."""
    import sys
    from pathlib import Path
    for p in (str(C.LEAN / "hosting"), str(C.LEAN)):
        if p not in sys.path:
            sys.path.insert(0, p)
    import speed_bench as SB
    return SB.JevS(None, None, 60.0, "drop")


def jev_calls(requests: list, n: int = 300, max_usd: float = 0.10, usd_per_call_guess: float = 0.0003, log=print) -> dict:
    """<= n sequential Jev calls with the SAME API v1 bodies (single-question dev prompts) from THIS client; wall ms of
    the full call. Stops early at `max_usd` (the response's own cost field when present, else the guess per call)."""
    jv = jev_client()
    recs, spent = [], 0.0
    try:
        for i, req in enumerate(requests[:n]):
            if spent >= max_usd:
                log(f"jev sample stopped at ${spent:.3f}")
                break
            d, ms, err, dropped = jv.decide(req)
            cost = None
            if d and isinstance(d.get("usage"), dict):
                cost = d["usage"].get("cost")
            spent += float(cost) if isinstance(cost, (int, float)) else usd_per_call_guess
            recs.append({"i": i, "client_ms": round(ms, 2), "error": err, "card_dropped": bool(dropped),
                         "model": (d or {}).get("model"), "usage_cost": cost})
    finally:
        jv.close()
    good = [r["client_ms"] for r in recs if r["error"] is None]
    return {"route": getattr(jv, "route", None), "model": getattr(jv, "model", None), "calls": len(recs),
            "errors": len(recs) - len(good), "client_ms": C.summarize(good), "est_spend_usd": round(spent, 4),
            "records": recs}


def interleaved_c1(url: str, token: str, requests: list, n: int = 100, jev=None, log=print) -> dict:
    """c=1, alternating order per pair (ours, Jev | Jev, ours) like client_bench so network drift hits both alike."""
    ours = make_client(url, token)
    jv = jev or jev_client()
    a, b, ea, eb = [], [], 0, 0
    try:
        for i, req in enumerate(requests[:n]):
            order = ("o", "j") if i % 2 == 0 else ("j", "o")
            for w in order:
                if w == "o":
                    r = timed_post(ours, "/decide", req)
                    (a.append(r["total_ms"]) if r["ok"] else None)
                    ea += not r["ok"]
                else:
                    d, ms, err, _ = jv.decide(req)
                    (b.append(ms) if err is None else None)
                    eb += err is not None
    finally:
        ours.close()
        if jev is None:
            jv.close()
    return {"pairs": min(n, len(requests)), "ours_ms": C.summarize(a), "jev_ms": C.summarize(b), "ours_errors": ea,
            "jev_errors": eb}
