"""od-direct-host: the 4B (default 4B-E = q35_4b_pxE, merged) on ONE H100 with CUDA graphs, behind a minimal HTTP API
reached through a direct Modal tunnel (modal.forward), so the laptop talks to the container without Modal's
web-endpoint layer. NEW file: it touches no frozen code (decoder_io.py, prism_x.py and writeblock.py are copied into the
image read-only) and it never writes to the account Volume (the base model and the Triton cache are only read).

Why (all measured earlier from this laptop):
  Modal web endpoint, L4 v05:   client p50 410 ms, server 123 ms          logs/bench_api.json
  CPU echo, no GPU (26 Sep):    web endpoint 356 ms, modal.forward 71.9 ms logs/latency_probe.log (region not pinned)
  4B v10, H100 + graphs, tunnel: client p50 114.6 ms, server 44.8 ms      logs/tunnel_q35_4b_v10_tunnel_plain.json
  4B-E, H100 + graphs, 1 decision per call: 16.6 ms of compute            extra/SPEED_RESULT_30sep.md
  Jev via OpenRouter, same laptop: p50 187-248 ms                         projection/evidence.md, section 9
So the remaining cost is network distance (the container's region) and request size, not Modal's web layer.

Commands, run from lean/ and ONLY after the owner's GO (nothing in this file has run on Modal yet):
  0) free CPU test:        ../.venv/bin/python hosting/test_direct_host_local.py
  1) network probe, CPU containers only (about $0.01):
       MODAL_PROFILE=<acct> ../.venv/bin/modal run hosting/modal_direct_host.py::probe --regions any,us-east,us
  2) the H100 test (about 6-10 billed H100 minutes):
       MODAL_PROFILE=<acct> ../.venv/bin/modal run hosting/modal_direct_host.py::main --region us-east
     --eval-mix also replays the 515 bench_api.json requests (ours only); --no-jev skips OpenRouter;
     --model q35_4b_main500k hosts another adapter from /vol/models (no sha256 pin for it).
  3) manual mode: add --hold, then from a second terminal
       ../.venv/bin/python hosting/client_bench.py --url URL --token TOKEN
Never pass --detach: the laptop is the client, and stopping `modal run` (Ctrl-C) stops the H100.
Cost guards: one container (max_containers=1), the server stops on POST /shutdown, after --seconds (default 900) or
after --idle seconds without a request (default 300), and the function timeout (30 min) is the hard cap.
"""
from __future__ import annotations

import hashlib
import json
import os
import queue as _queue
import secrets
import shutil
import sys
import threading
import time
import traceback
from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent  # lean/hosting locally; /root in the container (LEAN is unused there)
LEAN = HERE.parent
REMOTE_LEAN = "/root/lean"
APP_NAME = "od-direct-host"  # its own app: the live 4B run's app and models/q35_4b_main500k* are untouched
MODEL = "q35_4b_pxE"
ADAPTER_SHA256 = {  # adapter_model.safetensors, from the Mac backup (= the Volume copies, logs/label_check_30sep.md)
    "q35_4b_pxE": "1bbd8a79143f7ab5d6fd538c870ded0605120ab777c97d38ca3384b26c31a3f9",
}
BASE = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
LEAN_FILES = ("decoder_io.py", "prism_x.py", "writeblock.py")
PORT = 8000
TEMPS = {"noul": 1.0, "choice": 1.0}  # raw readout, as trained and as the dev parity preds (calibration comes later)
MAX_BODY = 1 << 20
MAX_QUESTIONS = 16
MAX_OPTIONS = 26  # letters only, as the JevBench adapter: the 4B was not trained on two-letter labels
FUNCTION_TIMEOUT_S = 30 * 60
# CUDA-graph capture plan. "main" is the shape set already proven on an H100 for a Qwen3.5-4B (serve_tunnel.py: batches
# 1,2,4,8 up to 1024 tokens). "extra" adds exact-fit batches for 3/5/6-question requests (a 5-question request otherwise
# pads to 8 rows); "long1" adds single-row buckets up to 2048 tokens. Capture stops when free memory drops under
# reserve_gb; a batch size is used only if every bucket of its range was captured, anything else runs eagerly.
GRAPH_CFG = {"batches": [1, 2, 4, 8], "max_tokens": 1024, "extra_batches": [3, 5, 6], "extra_max": 512,
             "long1_max": 2048, "reserve_gb": 8.0, "bucket": 64, "max_graph_tokens": 8192}
WARMUP = {"max_tokens": 2048, "batch_sizes": [1, 2, 4, 8]}  # eager Triton autotune before capture (fallback shapes)
# Graph-pool memory per padded token, bounds from the 30 Sep H100 run (66 batch-1 graphs up to 4224 tokens plus part of
# the batch-2 set filled 68 GB): between 68 GB / 407K tokens and 68 GB / 141K tokens. Used for the printed estimate only.
POOL_MB_PER_TOKEN = (0.17, 0.48)
GPU_RATE_USD_H = 4.31  # measured all-in H100 rate 4.09 (billing, segment 1) + 2 reserved cores and 16 GiB (~0.22)
REGION_MULT = {"any": 1.0, "broad": 1.15, "narrow": 1.75}  # modal.com/docs/guide/region-selection

# Exact copy of modal_od.PINNED35 (checked below against modal_od.py, parsed as text: modal_od is never imported), so
# this image is the same pip layer as modal_od.image35 and comes from the account's image cache.
PINNED35 = """accelerate==1.15.0 aiohappyeyeballs==2.7.1 aiohttp==3.14.3 aiosignal==1.4.0 annotated-doc==0.0.5 anyio==4.15.1
attrs==26.1.0 certifi==2026.7.22 charset_normalizer==3.5.1 click==8.5.0 cloudpickle==3.1.2 cuda-bindings==13.4.3
cuda-pathfinder==1.8.2 cuda-toolkit==13.0.3.0 datasets==5.0.1 dill==0.4.1 einops==0.8.2 filelock==4.0.3 fla-core==0.5.2
flash-linear-attention==0.5.2 frozenlist==1.8.0 fsspec==2026.6.0 h11==0.16.0 hf-xet==1.6.0 hf_transfer==0.1.9
httpcore==1.0.9 httpx==0.28.1 huggingface-hub==1.33.0 idna==3.20 jinja2==3.1.6 joblib==1.6.0 markdown-it-py==4.2.0
MarkupSafe==3.0.3 mdurl==0.1.2 mpmath==1.3.0 multidict==6.9.1 multiprocess==0.70.19 narwhals==2.26.0 networkx==3.7
numpy==2.5.3 nvidia-cublas==13.1.1.3 nvidia-cuda-cupti==13.0.85 nvidia-cuda-nvrtc==13.0.88 nvidia-cuda-runtime==13.0.96
nvidia-cudnn-cu13==9.24.0.43 nvidia-cufft==12.0.0.61 nvidia-cufile==1.15.1.6 nvidia-curand==10.4.0.35
nvidia-cusolver==12.0.4.66 nvidia-cusparse==12.6.3.3 nvidia-cusparselt-cu13==0.8.1 nvidia-nccl-cu13==2.30.7
nvidia-nvjitlink==13.4.92 nvidia-nvshmem-cu13==3.4.5 nvidia-nvtx==13.0.85 packaging==26.3 pandas==3.0.6 peft==0.21.0
propcache==0.5.4 protobuf==7.36.2 psutil==7.2.2 pyarrow==25.0.1 pygments==2.21.0 python-dateutil==2.9.0.post0
pyyaml==6.0.3 regex==2026.9.10 requests==2.34.2 rich==15.0.0 safetensors==0.8.0 scikit-learn==1.9.1 scipy==1.18.1
sentence-transformers==6.1.0 sentencepiece==0.2.2 setuptools==84.0.0 shellingham==1.5.4 six==1.17.0 sympy==1.14.0
threadpoolctl==3.7.0 tokenizers==0.23.2 torch==2.14.0 tqdm==4.70.1 transformers==5.17.0 triton==3.8.0 typer==0.27.2
typing-extensions==4.16.0 urllib3==2.8.0 xxhash==4.0.1 yarl==1.25.1""".split()


def pinned_from_modal_od() -> list:
    import ast
    for node in ast.parse((LEAN / "modal_od.py").read_text()).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "PINNED35" for t in node.targets):
            return node.value.func.value.value.split()  # PINNED35 = """...""".split()
    raise SystemExit("PINNED35 not found in modal_od.py")


if modal.is_local():
    if pinned_from_modal_od() != PINNED35:
        raise SystemExit("PINNED35 here differs from modal_od.py: refusing (the image would not be the relay's)")
    for _f in (LEAN / n for n in LEAN_FILES):
        if not _f.exists():
            raise SystemExit(f"missing {_f}")

image = (  # the modal_od.image35 build steps (debian_slim 3.12.10 + PINNED35 + env), then only the three code files
    modal.Image.debian_slim(python_version="3.12.10")
    .pip_install(*PINNED35)
    .env({"HF_HOME": "/vol/hf", "HF_HUB_ENABLE_HF_TRANSFER": "1", "TOKENIZERS_PARALLELISM": "false",
          "TRITON_CACHE_DIR": "/vol/triton_cache"})
)
for _n in LEAN_FILES:
    image = image.add_local_file(LEAN / _n, f"{REMOTE_LEAN}/{_n}")
probe_image = modal.Image.debian_slim(python_version="3.12.10")  # stdlib echo server only (no torch)
app = modal.App(APP_NAME)
vol = modal.Volume.from_name("opendecide")  # the account Volume (no create_if_missing: fail rather than make a new one)


# ------------------------------------------------------------------ serving core (CPU-testable, no Modal needed)

def lean_import():
    """decoder_io from /root/lean in the container, from lean/ locally."""
    p = REMOTE_LEAN if Path(REMOTE_LEAN, "decoder_io.py").exists() else str(LEAN)
    if p not in sys.path:
        sys.path.insert(0, p)
    import decoder_io
    return decoder_io


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_request(req) -> list:
    """A Jev-style request -> [(question name, decoder_io row)], one row per question, in request order.
    {"state": str, "questions": {name: {"type": "noul"|"choice", "instructions": str, "options": [..]}}}; a choice may
    give "criteria" ({label: description or null}, the Jev API shape) instead of "options": the non-empty descriptions
    become the definitions card the model reads ("- label: description"). Raises ValueError on a bad request."""
    if not isinstance(req, dict) or not isinstance(req.get("state"), str):
        raise ValueError('"state" must be a string')
    qs = req.get("questions")
    if not isinstance(qs, dict) or not qs:
        raise ValueError('"questions" must be a non-empty object')
    if len(qs) > MAX_QUESTIONS:
        raise ValueError(f"at most {MAX_QUESTIONS} questions per request")
    rows = []
    for k, q in qs.items():
        if not isinstance(q, dict) or q.get("type") not in ("noul", "choice"):
            raise ValueError(f'{k}: "type" must be "noul" or "choice"')
        ins = q.get("instructions")
        if not isinstance(ins, str) or not ins.strip():
            raise ValueError(f'{k}: "instructions" must be a non-empty string')
        row = {"state": req["state"], "instructions": ins, "qtype": q["type"], "options": None}
        if q["type"] == "noul":
            if q.get("criteria"):
                raise ValueError(f"{k}: noul criteria are not supported by this server")
        else:
            opts, card = q.get("options"), None
            if opts is None and isinstance(q.get("criteria"), dict):
                opts = list(q["criteria"])
                defs = [f"- {o}: {d}" for o, d in q["criteria"].items() if isinstance(d, str) and d.strip()]
                card = "\n".join(defs) or None
            if not isinstance(opts, list) or not all(isinstance(o, str) and o.strip() for o in opts):
                raise ValueError(f'{k}: a choice needs "options" (a list of strings) or "criteria"')
            if not 2 <= len(opts) <= MAX_OPTIONS:
                raise ValueError(f"{k}: 2 to {MAX_OPTIONS} options")
            if len(set(opts)) != len(opts):
                raise ValueError(f"{k}: duplicate options")
            row["options"] = list(opts)
            if card:
                row["card"] = card
        rows.append((k, row))
    return rows


class _Uncaptured(Exception):
    """A (batch, length) shape with no captured graph after start-up: the request runs eagerly instead."""


def make_graph_runner(dio, model, tok, cfg):
    """decoder_io.GraphRunner for serving. Unchanged replay code; three serving rules on top:
    - after start-up (frozen) it never captures a graph inside a request (a capture costs ~0.3-1 s and grows memory):
      an uncaptured shape raises _Uncaptured inside the parent's cand_logits, before any GPU work;
    - it tries the batch sizes with the extra exact fits first, then the main ones, then gives up (None), and
      decoder_io.cand_logits then takes its eager path;
    - it records the path ("graph"/"eager") and the padded (batch, length) of the last call."""

    class ServingGraphs(dio.GraphRunner):
        frozen = False
        main_batches = all_batches = ()
        last_path = last_shape = None

        def set_batches(self, main, extra):
            self.main_batches = tuple(sorted(set(main)))
            self.all_batches = tuple(sorted(set(main) | set(extra)))
            self.batches = self.all_batches

        def _graph(self, B, L):
            if self.frozen and (B, L) not in self.graphs:
                raise _Uncaptured((B, L))
            g = super()._graph(B, L)
            self.last_shape = (B, L)
            return g

        def cand_logits(self, ro, rows, perms=None):
            self.last_path, self.last_shape = "eager", None
            tries = [self.all_batches, self.main_batches] if self.frozen else [self.batches]
            if tries[0] == tries[-1]:
                tries = tries[:1]
            for bs in tries:
                keep, self.batches = self.batches, bs
                try:
                    out = super().cand_logits(ro, rows, perms)
                except _Uncaptured:
                    continue
                finally:
                    self.batches = keep
                if out is not None:
                    self.last_path = "graph"
                return out
            self.last_shape = None
            return None

    batches = tuple(sorted(set(cfg["batches"]) | set(cfg["extra_batches"])))
    return ServingGraphs(model, tok, bucket=cfg["bucket"], batches=batches, max_graph_tokens=cfg["max_graph_tokens"])


def graph_plan(cfg) -> dict:
    b, mg = cfg["bucket"], cfg["max_graph_tokens"]
    main = [(B, L) for B in cfg["batches"] for L in range(b, cfg["max_tokens"] + 1, b) if B == 1 or B * L <= mg]
    extra = [(B, L) for B in cfg["extra_batches"] for L in range(b, cfg["extra_max"] + 1, b) if B * L <= mg]
    long1 = [(1, L) for L in range(cfg["max_tokens"] + b, cfg["long1_max"] + 1, b)] if 1 in cfg["batches"] else []
    return {"main": main, "extra": extra, "long1": long1}


def plan_estimate(cfg) -> dict:
    p = graph_plan(cfg)
    tok = {k: sum(B * L for B, L in v) for k, v in p.items()}
    lo, hi = POOL_MB_PER_TOKEN
    return {"graphs": {k: len(v) for k, v in p.items()}, "padded_tokens": tok,
            "pool_gb_est": {k: [round(t * lo / 1024, 1), round(t * hi / 1024, 1)] for k, t in tok.items()}}


def capture_graphs(G, cfg, free_gb, log=print) -> dict:
    """Capture the plan in order main -> extra -> long1, stopping when free GPU memory < reserve_gb or on OOM. Then pick
    the batch sizes whose whole range was captured, and freeze the runner (no capture inside requests)."""
    import torch
    plan, t0, got, stopped = graph_plan(cfg), time.time(), {}, None
    for group in ("main", "extra", "long1"):
        got[group] = 0
        for B, L in plan[group]:
            free = free_gb()
            if free < cfg["reserve_gb"]:
                stopped = f"{group} at {(B, L)}: free {free:.1f} GB < reserve {cfg['reserve_gb']} GB"
                break
            try:
                G._graph(B, L)
            except torch.cuda.OutOfMemoryError as e:  # the partial graph is not stored; eager covers the shape
                stopped = f"{group} at {(B, L)}: OOM {str(e)[:120]}"
                torch.cuda.empty_cache()
                break
            got[group] += 1
        if stopped:
            break
    b, mg = cfg["bucket"], cfg["max_graph_tokens"]

    def full(B, Lmax):
        return all((B, L) in G.graphs for L in range(b, Lmax + 1, b) if B == 1 or B * L <= mg)

    main_b = [B for B in cfg["batches"] if full(B, cfg["max_tokens"])]
    extra_b = [B for B in cfg["extra_batches"] if full(B, cfg["extra_max"])]
    G.set_batches(main_b, extra_b)
    G.frozen = True
    rep = {"captured": got, "n_graphs": len(G.graphs), "stopped": stopped, "main_batches": main_b,
           "extra_batches": extra_b, "long1_upto": max([L for B, L in G.graphs if B == 1] or [0]),
           "capture_s": round(time.time() - t0, 1)}
    log(f"graphs: {json.dumps(rep)}")
    return rep


class Decider:
    """One request = one batch of rows (each question is its own sequence, as decoder_io reads it). GPU work is
    serialized by a lock (graphs are not thread-safe; the bench runs at concurrency 1 anyway)."""

    def __init__(self, dio, model, tok, dev, temps=None):
        import torch
        self.dio, self.model, self.tok, self.dev, self.torch = dio, model, tok, dev, torch
        self.ro = dio.Readout(tok)
        self.temps = dict(temps or TEMPS)
        self.lock = threading.Lock()
        self.sync = torch.cuda.synchronize if dev == "cuda" else (lambda: None)
        self.log = []  # per request: rows, path, shape, model_ms (server-side stats)

    def logits(self, rows):
        """decoder_io.cand_logits (graph replay when captured, else eager) -> (logits, path, shape)."""
        G = self.dio.GRAPHS
        with self.torch.no_grad():
            lg = self.dio.cand_logits(self.model, self.ro, rows, self.dev)
        self.sync()
        if G is None:
            return lg, "eager", None
        return lg, G.last_path or "eager", G.last_shape

    def decide(self, req) -> dict:
        t0 = time.perf_counter()
        named = parse_request(req)
        rows = [r for _, r in named]
        with self.lock:
            t1 = time.perf_counter()
            lg, path, shape = self.logits(rows)
            t2 = time.perf_counter()
            answers = {}
            for (k, r), l in zip(named, lg):
                p = self.dio.to_probs(r, l, temp=self.temps["noul" if r["qtype"] == "noul" else "choice"])
                if r["qtype"] == "noul":
                    answers[k] = {"type": "noul", "noul": p["yes"]}
                else:
                    best = max(p, key=p.get)
                    answers[k] = {"type": "choice", "choice": best, "confidence": p[best], "probabilities": p}
        t3 = time.perf_counter()
        timing = {"parse_ms": round((t1 - t0) * 1000, 3), "model_ms": round((t2 - t1) * 1000, 3),
                  "readout_ms": round((t3 - t2) * 1000, 3)}
        self.log.append({"rows": len(rows), "path": path, "shape": shape, "model_ms": timing["model_ms"]})
        return {"answers": answers, "timing": timing, "path": path, "shape": list(shape) if shape else None}

    def stats(self) -> dict:
        ms = sorted(x["model_ms"] for x in self.log)
        pick = lambda q: ms[min(len(ms) - 1, int(q * len(ms)))] if ms else None
        paths = {}
        for x in self.log:
            paths[x["path"]] = paths.get(x["path"], 0) + 1
        return {"requests": len(self.log), "model_ms_p50": pick(0.5), "model_ms_p95": pick(0.95), "paths": paths}


def graph_selfcheck(dec) -> dict:
    """Graph replay vs the eager path on filler rows (batch 1 and 4): max probability difference."""
    dio, torch = dec.dio, dec.torch
    filler = "The office opens at nine and closes at five on weekdays. "
    rows = [{"state": filler * k, "instructions": "Is the office open on weekdays?", "qtype": "noul", "options": None}
            for k in (2, 12, 30)]
    rows.append({"state": filler * 6, "instructions": "When does the office open?", "qtype": "choice",
                 "options": ["nine", "ten", "noon", "never"]})
    out = {}
    for name, batch in (("b1", rows[:1]), ("b4", rows)):
        g, path, shape = dec.logits(batch)
        keep, dio.GRAPHS = dio.GRAPHS, None
        try:
            e, _, _ = dec.logits(batch)
        finally:
            dio.GRAPHS = keep
        diff = max(float((torch.softmax(a.float(), -1) - torch.softmax(b.float(), -1)).abs().max()) for a, b in zip(g, e))
        out[name] = {"path": path, "shape": list(shape) if shape else None, "max_prob_diff": diff}
    return out


EXAMPLE = {"state": "Customer message:\nMy card payment was declined at the shop this morning.",
           "questions": {"q0": {"type": "noul", "instructions": "Is the customer reporting a declined payment?"},
                         "q1": {"type": "choice", "instructions": "Which label describes this message?",
                                "options": ["declined card payment", "card arrival", "refund request"]}}}


def echo_answers(req) -> dict:
    """The probe's /decide: no model, an answer of the real shape and size (uniform probabilities)."""
    ans = {}
    for k, qq in parse_request(req):
        if qq["qtype"] == "choice":
            o = qq["options"]
            ans[k] = {"type": "choice", "choice": o[0], "confidence": 1 / len(o), "probabilities": {x: 1 / len(o) for x in o}}
        else:
            ans[k] = {"type": "noul", "noul": 0.5}
    return {"answers": ans, "timing": {}, "path": "echo", "shape": None}


def make_server(port, token, decide, health, on_shutdown, state=None, host="0.0.0.0"):
    """Minimal HTTP/1.1 JSON server (stdlib). Keep-alive, TCP_NODELAY, and each response leaves in ONE write (headers
    and body buffered, flushed once per request), so no Nagle / delayed-ACK stall between headers and body.
    Every route needs "Authorization: Bearer <token>" (the tunnel URL is public).
      GET  /ping      -> {"ok": true}                    network round trip only
      GET  /health    -> model, graphs, region, memory, start-up timings
      POST /decide    -> {"answers", "timing", "path", "shape", "server_ms"}   (POST / is the same)
      POST /shutdown  -> stops the server; the Modal function then returns (ends the GPU bill)"""
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    st = state if state is not None else {"last": time.time(), "n": 0, "errors": 0}
    want = f"Bearer {token}".encode()

    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        disable_nagle_algorithm = True
        wbufsize = 1 << 16
        server_version = "od-direct-host"
        sys_version = ""

        def _reply(self, code, obj):
            body = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _authed(self) -> bool:
            if secrets.compare_digest((self.headers.get("Authorization") or "").encode(), want):
                return True
            self._reply(401, {"error": "unauthorized"})
            return False

        def do_GET(self):
            if not self._authed():
                return
            if self.path == "/ping":
                self._reply(200, {"ok": True})
            elif self.path == "/health":
                self._reply(200, {**health(), "served": st["n"], "errors": st["errors"]})
            else:
                self._reply(404, {"error": "not found"})

        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            if n > MAX_BODY:
                self.close_connection = True
                self._reply(413, {"error": "body too large"})
                return
            body = self.rfile.read(n)
            if not self._authed():
                return
            t0 = time.perf_counter()
            st["last"] = time.time()
            if self.path in ("/decide", "/"):
                try:
                    out = decide(json.loads(body))
                except ValueError as e:  # includes json.JSONDecodeError
                    st["errors"] += 1
                    self._reply(400, {"error": str(e)})
                    return
                except Exception as e:  # noqa: BLE001 - a server error must not kill the server
                    st["errors"] += 1
                    traceback.print_exc()
                    self._reply(500, {"error": f"{type(e).__name__}: {e}"})
                    return
                st["n"] += 1
                out["server_ms"] = (time.perf_counter() - t0) * 1000  # body read -> response ready (no network)
                self._reply(200, out)
            elif self.path == "/shutdown":
                self._reply(200, {"ok": True, "served": st["n"]})
                on_shutdown()
            else:
                self._reply(404, {"error": "not found"})

        def log_message(self, *a):
            pass

    class S(ThreadingHTTPServer):
        daemon_threads = True
        allow_reuse_address = True

    return S((host, port), H), st


def wait_loop(stop, st, seconds, idle_s) -> str:
    deadline = time.time() + seconds
    while True:
        if stop.wait(2):
            return "shutdown request"
        if time.time() > deadline:
            return f"--seconds {seconds} reached"
        if time.time() - st["last"] > idle_s:
            return f"idle for {idle_s} s"


def base_snapshot_complete(hf_home: str) -> bool:
    snap = Path(hf_home) / "hub" / ("models--" + BASE.replace("/", "--")) / "snapshots" / REVISION
    if not (snap / "config.json").exists():
        return False
    idx = snap / "model.safetensors.index.json"
    if idx.exists():
        files = set(json.loads(idx.read_text())["weight_map"].values())
        return all((snap / f).exists() for f in files)
    return (snap / "model.safetensors").exists()


def boot_gpu(model_name, cfg, warm=None, log=print):
    """Container start-up: read-only inputs, load + merge, eager warm-up, graph capture, self-check, request warm-up."""
    t0 = time.time()
    info = {"app": APP_NAME, "model": model_name, "base": BASE, "revision": REVISION, "temps": TEMPS,
            "region": os.environ.get("MODAL_REGION"), "cloud": os.environ.get("MODAL_CLOUD_PROVIDER"),
            "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    tc = Path("/tmp/triton_cache")  # private copy: the Volume's Triton cache is only read
    try:
        shutil.copytree("/vol/triton_cache", tc, dirs_exist_ok=True)
        info["triton_cache"] = "seeded from /vol/triton_cache"
    except Exception as e:  # noqa: BLE001
        info["triton_cache"] = f"not seeded: {type(e).__name__}"
    os.environ["TRITON_CACHE_DIR"] = str(tc)
    if base_snapshot_complete("/vol/hf"):  # read the Volume's copy offline: no Hub calls, no cache writes
        os.environ["HF_HUB_OFFLINE"] = "1"
        info["base_source"] = "/vol/hf snapshot (offline)"
    else:  # never write the Volume: download to the container's own disk
        os.environ["HF_HOME"] = "/tmp/hf"
        info["base_source"] = "downloaded to /tmp/hf"
    model_dir = Path("/vol/models") / model_name
    if not (model_dir / "adapter_model.safetensors").exists():
        raise SystemExit(f"{model_dir} missing on this account's Volume")
    if (model_dir / "prism_x.json").exists():
        raise SystemExit(f"{model_name} has prism_x.json: CUDA graphs are not supported for PRISM-X models")
    info["adapter_sha256"] = sha256_file(model_dir / "adapter_model.safetensors")
    if model_name in ADAPTER_SHA256 and info["adapter_sha256"] != ADAPTER_SHA256[model_name]:
        raise SystemExit(f"{model_name}: adapter sha256 {info['adapter_sha256']} != pinned {ADAPTER_SHA256[model_name]}")
    dio = lean_import()
    import torch
    info["code_sha256"] = {n: sha256_file(Path(REMOTE_LEAN) / n) for n in LEAN_FILES}
    model, tok, load_info = dio.load(BASE, "cuda", adapter=str(model_dir), revision=REVISION, return_info=True)
    model = model.merge_and_unload()  # as od_gcp predict, run_v154 and the speed test
    model.eval()
    for c in (model.config, getattr(model.config, "text_config", None)):
        if c is not None:
            c.use_cache = True
    model.generation_config.use_cache = True
    info["load"] = {k: load_info.get(k) for k in ("layout", "style", "revision", "prism_x", "chat_template_sha")}
    if load_info.get("prism_x"):
        raise SystemExit("PRISM-X model: CUDA graphs unsupported")
    info["load_s"] = round(time.time() - t0, 1)
    dec = Decider(dio, model, tok, "cuda")
    tw = time.time()
    w = warm or WARMUP
    dio.warmup(model, dec.ro, max_tokens=w["max_tokens"], batch_sizes=tuple(w["batch_sizes"]))
    torch.cuda.empty_cache()  # give the warm-up's cached blocks back: graph pools cannot reuse them
    info["warmup_s"] = round(time.time() - tw, 1)
    info["graph_plan"] = plan_estimate(cfg)
    G = make_graph_runner(dio, model, tok, cfg)
    dio.GRAPHS = G
    info["graphs"] = capture_graphs(G, cfg, lambda: torch.cuda.mem_get_info()[0] / 2 ** 30, log)
    info["graph_selfcheck"] = graph_selfcheck(dec)
    for _ in range(3):  # the full request path once, so the first timed request is not the first one
        dec.decide(EXAMPLE)
    dec.log.clear()
    info["memory_gb"] = {"max_allocated": round(torch.cuda.max_memory_allocated() / 2 ** 30, 2),
                         "reserved": round(torch.cuda.memory_reserved() / 2 ** 30, 2),
                         "free": round(torch.cuda.mem_get_info()[0] / 2 ** 30, 2)}
    info["gpu"] = torch.cuda.get_device_name(0)
    info["boot_s"] = round(time.time() - t0, 1)
    log("BOOT " + json.dumps(info))
    return dec, info


# ------------------------------------------------------------------ Modal functions

@app.function(image=image, gpu="H100!", cpu=2.0, memory=16384, volumes={"/vol": vol}, timeout=FUNCTION_TIMEOUT_S,
              max_containers=1)  # 2 reserved cores: tokenization/HTTP must not be CPU-throttled (+~$0.22/h)
def serve(q: modal.Queue, token: str, seconds: int = 900, idle_s: int = 300, model: str = MODEL,
          graph_cfg: dict | None = None) -> dict:
    t0 = time.time()
    dec, info = boot_gpu(model, {**GRAPH_CFG, **(graph_cfg or {})})
    stop = threading.Event()
    srv, st = make_server(PORT, token, dec.decide, lambda: info, stop.set)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    with modal.forward(PORT) as tunnel:
        st["last"] = time.time()
        q.put({"url": tunnel.url, "health": info})
        reason = wait_loop(stop, st, seconds, idle_s)
    srv.shutdown()
    out = {"info": info, "served": st["n"], "errors": st["errors"], "server_side": dec.stats(), "stop": reason,
           "wall_s": round(time.time() - t0, 1)}
    print("DONE " + json.dumps(out), flush=True)
    return out


@app.function(image=probe_image, cpu=0.5, memory=512, timeout=15 * 60, max_containers=1)
def echo(q: modal.Queue, token: str, seconds: int = 300, idle_s: int = 90) -> dict:
    """Network-only probe: the same HTTP server answering instantly (no model), behind a TLS tunnel (port 8000) and a
    plain-TCP tunnel (port 8001). The answer has the same shape and roughly the size of a real one."""
    stop, st = threading.Event(), {"last": time.time(), "n": 0, "errors": 0}
    where = {"region": os.environ.get("MODAL_REGION"), "cloud": os.environ.get("MODAL_CLOUD_PROVIDER")}
    s1, _ = make_server(PORT, token, echo_answers, lambda: where, stop.set, state=st)
    s2, _ = make_server(PORT + 1, token, echo_answers, lambda: where, stop.set, state=st)
    for s in (s1, s2):
        threading.Thread(target=s.serve_forever, daemon=True).start()
    with modal.forward(PORT) as t1, modal.forward(PORT + 1, unencrypted=True) as t2:
        host, port = t2.tcp_socket
        st["last"] = time.time()
        q.put({"tls": t1.url, "tcp": f"http://{host}:{port}", **where})
        reason = wait_loop(stop, st, seconds, idle_s)
    for s in (s1, s2):
        s.shutdown()
    return {"served": st["n"], "stop": reason, **where}


# ------------------------------------------------------------------ local entrypoints (run on the laptop)

def _region_opt(region: str):
    r = [x.strip() for x in region.split(",") if x.strip()]
    if not r or r == ["any"]:
        return None, REGION_MULT["any"]
    narrow = any(x not in ("us", "eu", "ap") for x in r)
    return (r[0] if len(r) == 1 else r), REGION_MULT["narrow" if narrow else "broad"]


def _wait_url(q, call, wait_s, what):
    t0 = time.time()
    while True:
        try:
            return q.get(timeout=15)
        except _queue.Empty:
            pass
        try:
            res = call.get(timeout=0)  # returned (or raised) before publishing a URL
            raise SystemExit(f"{what} returned before publishing a URL: {res}")
        # Modal currently raises the built-in TimeoutError for a zero-timeout
        # poll with no output, while older SDKs used modal.exception.TimeoutError.
        # Either case means the server is still booting, not that the launch failed.
        except (modal.exception.TimeoutError, TimeoutError):
            pass
        if time.time() - t0 > wait_s:
            raise SystemExit(f"{what}: no URL after {wait_s} s (GPU queue or boot problem); stopping")
        print(f"waiting for {what}: {time.time() - t0:.0f} s", flush=True)


def _finish(call, cb, url, token, wait=120):
    try:
        cb.shutdown(url, token)
    except Exception as e:  # noqa: BLE001
        print(f"shutdown request failed ({e}); cancelling the call", flush=True)
    try:
        return call.get(timeout=wait)
    except Exception as e:  # noqa: BLE001
        print(f"no clean return ({type(e).__name__}); cancelling", flush=True)
        call.cancel()
        return None


@app.local_entrypoint()
def main(region: str = "us-east", gpu: str = "H100!", model: str = MODEL, seconds: int = 900, idle: int = 300,
         limit: int = 100, jev: bool = True, eval_mix: bool = False, hold: bool = False, name: str = "",
         graph_cfg: str = "", boot_wait: int = 1500):
    """H100 direct-host test: start the server, run client_bench (ours vs Jev on the same dev requests) from this
    laptop, shut down. Prints and saves hosting/results/<name>/summary.json."""
    sys.path.insert(0, str(HERE))
    import client_bench as cb
    if seconds + 600 > FUNCTION_TIMEOUT_S:
        raise SystemExit(f"--seconds must be <= {FUNCTION_TIMEOUT_S - 600} (boot + serving must fit the timeout)")
    reg, mult = _region_opt(region)
    name = name or f"h100_{region.replace(',', '+')}_{time.strftime('%Y%m%d_%H%M%S', time.gmtime())}"
    token = secrets.token_urlsafe(24)
    opts = {"gpu": gpu, **({"region": reg} if reg else {})}
    t0 = time.time()
    with modal.Queue.ephemeral() as q:
        call = serve.with_options(**opts).spawn(q, token, seconds, idle, model, json.loads(graph_cfg) if graph_cfg else None)
        msg = _wait_url(q, call, boot_wait, f"H100 server ({region})")
        url = msg["url"]
        t_up = time.time()
        print(f"server up after {t_up - t0:.0f} s: {url}\nhealth: {json.dumps(msg['health'])[:2000]}", flush=True)
        res = None
        try:
            if hold:
                print(f"\nHOLD: serving for up to {seconds} s (idle stop {idle} s). From another terminal:\n"
                      f"  ../.venv/bin/python hosting/client_bench.py --url {url} --token {token}\n"
                      f"Ctrl-C here (or POST /shutdown) stops the GPU.", flush=True)
                while True:  # until the server stops itself (shutdown, --seconds, --idle) or Ctrl-C
                    try:
                        call.get(timeout=30)
                        break
                    except modal.exception.TimeoutError:
                        continue
            else:
                cb.wait_ready(url, token)
                s1 = cb.run_bench(url, token, mix="dev", n=limit, jev=jev, name=name, health=msg["health"])
                if eval_mix:
                    cb.run_bench(url, token, mix="eval", n=0, jev=False, name=name + "_evalmix", health=msg["health"])
                print(cb.short_report(s1), flush=True)
        except KeyboardInterrupt:
            print("interrupted: shutting the server down", flush=True)
        finally:
            res = _finish(call, cb, url, token)
    wall_h = (time.time() - t0) / 3600
    est = {"wall_min_spawn_to_end": round(wall_h * 60, 1), "rate_usd_h": round(GPU_RATE_USD_H * mult, 2),
           "est_usd_upper": round(wall_h * GPU_RATE_USD_H * mult, 2),
           "note": "upper bound: GPU queue time before the container starts is not billed"}
    out_dir = cb.RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "server_return.json").write_text(json.dumps({"server": res, "cost_estimate": est}, indent=2))
    print(json.dumps({"cost_estimate": est, "server_stop": (res or {}).get("stop"),
                      "server_side": (res or {}).get("server_side")}, indent=2))


@app.local_entrypoint()
def probe(regions: str = "any,us-east,us", n: int = 60, seconds: int = 300):
    """Network-only probe (CPU containers, no GPU): the laptop's round trip to an echo server pinned to each region,
    through the TLS tunnel and the plain-TCP tunnel, with a real dev request as the body. Decides --region."""
    sys.path.insert(0, str(HERE))
    import client_bench as cb
    token = secrets.token_urlsafe(24)
    body = cb.build_requests("dev", 1)[0][0]["request"]
    out = {}
    for region in [r.strip() for r in regions.split(",") if r.strip()]:
        reg, _ = _region_opt(region)
        fn = echo.with_options(region=reg) if reg else echo
        with modal.Queue.ephemeral() as q:
            call = fn.spawn(q, token, seconds)
            msg = _wait_url(q, call, 600, f"echo ({region})")
            res = {"container_region": msg.get("region"), "cloud": msg.get("cloud")}
            try:
                for kind in ("tls", "tcp"):
                    res[kind] = cb.network_series(msg[kind], token, n, body)
            finally:
                _finish(call, cb, msg["tls"], token, wait=60)
        out[region] = res
        print(json.dumps({region: res}, indent=1), flush=True)
    cb.RESULTS.mkdir(parents=True, exist_ok=True)
    path = cb.RESULTS / f"probe_{time.strftime('%Y%m%d_%H%M%S', time.gmtime())}.json"
    path.write_text(json.dumps(out, indent=2))
    print(f"wrote {path}")
    for region, r in out.items():
        print(f"{region:10s} container={r['container_region']}  tls ping p50 {r['tls']['ping_ms']['p50']} ms, "
              f"echo-decide p50 {r['tls']['decide_ms']['p50']} ms | tcp ping p50 {r['tcp']['ping_ms']['p50']} ms")
