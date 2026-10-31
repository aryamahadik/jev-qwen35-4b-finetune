"""oc1.front: the end-to-end test's HTTP front for a running SGLang server (API v1, same /decide as arm S1), plus
  * CoalescingClient   a capped batching wait: concurrent requests' sequences go to SGLang in ONE /generate call after at
                       most `wait_ms` (0 = send at once, merging only what is already queued); runtime-changeable
  * admission control  more than `shed_at` requests in flight -> HTTP 503 at once (no queueing behind a saturated GPU)
  * per-stage timing   tokenize / front queue / coalescing wait / SGLang call / readout, SGLang's own e2e, server_ms
  * GPU + CPU marks    POST /admin/mark {"label","event"}: GPU busy share (nvidia-smi) and front CPU share between marks

It reuses hosting/sglang_host.py (SGLangFrontEnd: API v1 parsing, prompt text, candidate ids and token ids from
fastcore.readout = decoder_io byte for byte; SGLangClient) UNCHANGED; only the HTTP layer and the client wrapper are new.
Runs under /opt/fastpath python (C1's pinned stack) next to SGLang, exactly like S1's front end.
"""
from __future__ import annotations

import hmac
import json
import os
import queue
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

from . import items as I
from .measure import GpuSampler

SH = I.sglang_host_mod()


class _Job:
    __slots__ = ("body", "n", "t_enq", "ev", "result", "error", "t_disp", "t_done", "batch_n")

    def __init__(self, body):
        self.body, self.n = body, len(body["input_ids"])
        self.t_enq = time.perf_counter()
        self.ev, self.result, self.error = threading.Event(), None, None
        self.t_disp = self.t_done = None
        self.batch_n = 0


class CoalescingClient:
    """Drop-in for SGLangClient inside SGLangFrontEnd: .generate() queues the body; a dispatcher merges queued bodies
    (up to `max_seqs` sequences, waiting at most `wait_ms` for company) and sends each merged call from a worker pool."""

    def __init__(self, inner, wait_ms: float = 0.0, max_seqs: int = 64, max_queue: int = 100000, workers: int = 96):
        self.inner = inner
        self.wait_ms, self.max_seqs, self.max_queue = float(wait_ms), int(max_seqs), int(max_queue)
        self.q = queue.Queue()
        self.pool = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="coal")
        self.tl = threading.local()
        self.lock = threading.Lock()
        self.stats = {"jobs": 0, "merged_calls": 0, "seqs": 0, "shed": 0, "wait_ms_sum": 0.0, "max_batch_seqs": 0}
        self.waiting = 0            # jobs enqueued and not yet handed to a send (the admission-control queue)
        self.closed = False
        self.base_url = getattr(inner, "base_url", None)
        self.c = getattr(inner, "c", None)
        self.thread = threading.Thread(target=self._loop, daemon=True, name="coalescer")
        self.thread.start()

    # -- config
    def set(self, wait_ms=None, max_seqs=None, max_queue=None):
        if wait_ms is not None:
            self.wait_ms = float(wait_ms)
        if max_seqs is not None:
            self.max_seqs = int(max_seqs)
        if max_queue is not None:
            self.max_queue = int(max_queue)
        return self.config()

    def config(self):
        return {"wait_ms": self.wait_ms, "max_seqs": self.max_seqs, "max_queue": self.max_queue}

    # -- SGLangClient surface
    def generate(self, body: dict, timeout: float):
        if self.closed:
            raise SH.UpstreamUnavailable("coalescer closed")
        with self.lock:
            if self.waiting >= self.max_queue:
                self.stats["shed"] += 1
                full = True
            else:
                self.waiting += 1
                full = False
        if full:
            raise SH.UpstreamUnavailable(f"coalescer queue is full ({self.max_queue})")
        job = _Job(body)
        self.q.put(job)
        if not job.ev.wait(timeout):
            raise SH.UpstreamTimeout(f"no answer within {timeout} s")
        if job.error is not None:
            raise job.error
        self.tl.last = {"coalesce_wait_ms": (job.t_disp - job.t_enq) * 1000.0,
                        "sglang_call_ms": (job.t_done - job.t_disp) * 1000.0, "batch_seqs": job.batch_n}
        return job.result

    def take_last(self) -> dict:
        d = getattr(self.tl, "last", None)
        self.tl.last = None
        return d or {}

    def abort(self, rids):
        return self.inner.abort(rids)

    def flush(self, *a, **k):
        return self.inner.flush(*a, **k)

    def alive(self, *a, **k):
        return self.inner.alive(*a, **k)

    def server_info(self):
        return self.inner.server_info()

    def close(self):
        self.closed = True
        self.pool.shutdown(wait=False)
        self.inner.close()

    # -- dispatcher
    def _loop(self):
        while not self.closed:
            try:
                first = self.q.get(timeout=0.2)
            except queue.Empty:
                continue
            batch, nseq = [first], first.n
            t_end = time.perf_counter() + self.wait_ms / 1000.0
            while nseq < self.max_seqs:
                rem = t_end - time.perf_counter()
                try:
                    j = self.q.get(timeout=rem) if (self.wait_ms > 0 and rem > 0) else self.q.get_nowait()
                except queue.Empty:
                    break
                batch.append(j)
                nseq += j.n
            with self.lock:
                self.waiting -= len(batch)
            self.pool.submit(self._send, batch, nseq)

    def _send(self, batch: list, nseq: int):
        t_disp = time.perf_counter()
        body = {k: v for k, v in batch[0].body.items() if k not in ("input_ids", "token_ids_logprob", "rid")}
        body["input_ids"] = [x for j in batch for x in j.body["input_ids"]]
        body["token_ids_logprob"] = [x for j in batch for x in j.body["token_ids_logprob"]]
        if all("rid" in j.body for j in batch):
            body["rid"] = [x for j in batch for x in j.body["rid"]]
        for j in batch:
            j.t_disp, j.batch_n = t_disp, nseq
        try:
            resp = self.inner.generate(body, 120.0)
            if not isinstance(resp, list) or len(resp) != nseq:
                raise SH.UpstreamError(f"merged /generate returned {len(resp) if isinstance(resp, list) else '?'} for {nseq}")
            k = 0
            for j in batch:
                j.result = resp[k:k + j.n]
                k += j.n
            err = None
        except BaseException as e:  # noqa: BLE001
            err = e
        t_done = time.perf_counter()
        with self.lock:
            self.stats["jobs"] += len(batch)
            self.stats["merged_calls"] += 1
            self.stats["seqs"] += nseq
            self.stats["max_batch_seqs"] = max(self.stats["max_batch_seqs"], nseq)
            self.stats["wait_ms_sum"] += sum((t_disp - j.t_enq) * 1000.0 for j in batch)
        for j in batch:
            j.t_done, j.error = t_done, err
            j.ev.set()

    def snapshot(self) -> dict:
        with self.lock:
            s = dict(self.stats)
        s["mean_seqs_per_call"] = round(s["seqs"] / s["merged_calls"], 3) if s["merged_calls"] else None
        s["mean_coalesce_wait_ms"] = round(s["wait_ms_sum"] / s["jobs"], 3) if s["jobs"] else None
        return s


# ------------------------------------------------------------------ HTTP layer
class Marks:
    """Windows opened/closed by the load client: server-side counters between two marks."""

    def __init__(self, sampler, coal, state):
        self.sampler, self.coal, self.state = sampler, coal, state
        self.open_ = {}
        try:
            import psutil
            self.proc = psutil.Process(os.getpid())
            self.proc.cpu_percent(None)
        except Exception:  # noqa: BLE001
            self.proc = None

    def start(self, label):
        self.open_[label] = {"t": time.time(), "cpu_t": (sum(self.proc.cpu_times()[:2]) if self.proc else None),
                             "served": self.state["n"], "errors": self.state["errors"], "shed": self.state.get("shed", 0),
                             "coal": self.coal.snapshot() if self.coal else None}
        return {"ok": True, "label": label}

    def end(self, label):
        o = self.open_.pop(label, None)
        if o is None:
            return {"ok": False, "error": f"no open mark {label!r}"}
        t1 = time.time()
        dt = max(t1 - o["t"], 1e-9)
        res = {"label": label, "window_s": round(dt, 2), "served": self.state["n"] - o["served"],
               "errors": self.state["errors"] - o["errors"], "shed": self.state.get("shed", 0) - o["shed"],
               "gpu": self.sampler.between(o["t"], t1) if self.sampler else None}
        if self.proc is not None and o["cpu_t"] is not None:
            cpu = sum(self.proc.cpu_times()[:2]) - o["cpu_t"]
            res["front_cpu_cores"] = round(cpu / dt, 3)   # busy cores of the front process (threads sum), GIL-bound near 1.0
        if self.coal and o["coal"]:
            now = self.coal.snapshot()
            dc = now["merged_calls"] - o["coal"]["merged_calls"]
            ds = now["seqs"] - o["coal"]["seqs"]
            res["mean_seqs_per_sglang_call"] = round(ds / dc, 3) if dc else None
            res["sglang_calls"] = dc
        return res


def make_server(port, token, fe, coal, host_info, on_shutdown, sampler=None, shed_at: int = 10 ** 9, host="0.0.0.0"):
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    st = {"last": time.time(), "n": 0, "errors": 0, "shed": 0, "inflight": 0, "shed_at": int(shed_at)}
    lock = threading.Lock()
    want = f"Bearer {token}".encode()
    marks = Marks(sampler, coal, st)
    hinfo = host_info if callable(host_info) else (lambda: dict(host_info or {}))

    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        disable_nagle_algorithm = True
        wbufsize = 1 << 16
        server_version = "oc1-front"
        sys_version = ""

        def _reply(self, code, obj, extra=None):
            body = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            for k, v in (extra or {}).items():
                self.send_header(k, str(v))
            self.end_headers()
            self.wfile.write(body)

        def _authed(self):
            if hmac.compare_digest((self.headers.get("Authorization") or "").encode(), want):
                return True
            self._reply(401, {"error": "unauthorized"})
            return False

        def do_GET(self):
            if not self._authed():
                return
            if self.path == "/ping":
                self._reply(200, {"ok": True})
            elif self.path == "/health":
                self._reply(200, {**fe.health(), **hinfo(), "served": st["n"], "errors": st["errors"], "shed": st["shed"],
                                  "front": coal.config(), "coalescer": coal.snapshot(), "shed_at": st["shed_at"]})
            else:
                self._reply(404, {"error": "not found"})

        def do_POST(self):
            t_in = time.perf_counter()
            n = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(n)
            if not self._authed():
                return
            st["last"] = time.time()
            try:
                if self.path in ("/decide", "/"):
                    with lock:
                        if st["inflight"] >= st["shed_at"]:
                            st["shed"] += 1
                            shed = True
                        else:
                            st["inflight"] += 1
                            shed = False
                    if shed:
                        self._reply(503, {"error": "overloaded: request shed", "inflight": st["inflight"]},
                                    {"Retry-After": "1"})
                        return
                    try:
                        out = fe.decide(json.loads(raw))
                    finally:
                        with lock:
                            st["inflight"] -= 1
                    st["n"] += 1
                    extra = coal.take_last()
                    out["timing"].update({k: round(v, 3) if isinstance(v, float) else v for k, v in extra.items()})
                    out["server_ms"] = round((time.perf_counter() - t_in) * 1000.0, 3)
                    self._reply(200, out, {"X-Server-Ms": out["server_ms"]})
                elif self.path == "/admin/front":
                    body = json.loads(raw or b"{}")
                    cfg = coal.set(body.get("wait_ms"), body.get("max_seqs"), body.get("max_queue"))
                    if "shed_at" in body:
                        st["shed_at"] = int(body["shed_at"])
                    self._reply(200, {**cfg, "shed_at": st["shed_at"]})
                elif self.path == "/admin/mark":
                    body = json.loads(raw or b"{}")
                    ev = body.get("event")
                    self._reply(200, marks.start(body["label"]) if ev == "start" else marks.end(body["label"]))
                elif self.path == "/admin/flush":
                    self._reply(200, fe.flush())
                elif self.path == "/admin/config":
                    body = json.loads(raw or b"{}")
                    fe.set_flags(body.get("flags") or {})
                    self._reply(200, {"flags": fe.flags_view()})
                elif self.path == "/shutdown":
                    self._reply(200, {"ok": True, "served": st["n"]})
                    on_shutdown()
                else:
                    self._reply(404, {"error": "not found"})
            except Exception as e:  # noqa: BLE001
                code = SH.http_status(e)
                st["errors"] += 1
                if code == 500:
                    traceback.print_exc()
                self._reply(code, {"error": f"{type(e).__name__}: {e}" if code >= 500 else str(e)})

        def log_message(self, *a):
            pass

    class S(ThreadingHTTPServer):
        daemon_threads = True
        allow_reuse_address = True
        request_queue_size = 512

    return S((host, port), H), st


def run_front(cfg: dict, token: str, stop=None, log=print) -> dict:
    """Tokenizer + Readout, SGLangFrontEnd over a CoalescingClient, boot (probe + warm-up + flush), HTTP server, ready
    file, serve until /shutdown or cfg["seconds"]. cfg: sglang_url, c1_tokenizer_dir, port, seconds, wait_ms, max_seqs,
    shed_at, ready_file, done_file, server_args, host_info, probe_sha256, max_inflight."""
    t0 = time.time()
    tok, ro, tinfo = SH.load_c1_tokenizer(cfg["c1_tokenizer_dir"])
    if cfg.get("go_file"):                 # tokenizer + Readout built; wait for the session's go (measurements finished)
        g = cfg["go_file"]
        t_g = time.time()
        while not os.path.exists(g):
            if cfg.get("abort_file") and os.path.exists(cfg["abort_file"]):
                raise SystemExit("front aborted before go")
            if time.time() - t_g > float(cfg.get("go_timeout_s", 3000)):
                raise SystemExit("front: no go signal")
            time.sleep(0.5)
    inner = SH.SGLangClient(cfg["sglang_url"])
    coal = CoalescingClient(inner, wait_ms=cfg.get("wait_ms", 0.0), max_seqs=cfg.get("max_seqs", 64),
                            max_queue=cfg.get("max_queue", 100000))
    fe = SH.SGLangFrontEnd(coal, tok, ro, quantization=cfg.get("quantization"), server_args=cfg.get("server_args"),
                           max_inflight=int(cfg.get("max_inflight", 256)), log=log)
    boot = fe.boot(warm_requests=int(cfg.get("warm_requests", 6)), probe_sha256=cfg.get("probe_sha256"))
    sampler = GpuSampler(0.5)
    sampler.__enter__()
    stop = stop or threading.Event()
    host = dict(cfg.get("host_info") or {})
    host["boot_s"] = round(time.time() - float(cfg.get("t0", t0)), 1)
    srv, st = make_server(int(cfg["port"]), token, fe, coal, host, stop.set, sampler, cfg.get("shed_at", 10 ** 9),
                          cfg.get("host", "0.0.0.0"))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    st["last"] = time.time()
    if cfg.get("ready_file"):
        SH._write_json(cfg["ready_file"], {"ok": True, "port": srv.server_address[1], "boot": boot,
                                           "health": {**fe.health(), **host}})
    log(f"FRONT READY port {srv.server_address[1]}")
    reason = SH.wait_loop(stop, st, float(cfg.get("seconds", 900)), float(cfg.get("idle_s", 300)))
    srv.shutdown()
    srv.server_close()
    sampler.__exit__(None, None, None)
    fe.close()
    done = {"stop": reason, "served": st["n"], "errors": st["errors"], "shed": st["shed"], "stats": fe.stats(),
            "coalescer": coal.snapshot(), "gpu_samples": len(sampler.samples), "wall_s": round(time.time() - t0, 1)}
    if cfg.get("done_file"):
        SH._write_json(cfg["done_file"], done)
    return done
