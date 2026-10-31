"""od-sglang-host: C1 (q35_4b_main500k, merged BF16) served by SGLang 0.5.20 on ONE H100 = arms S1 (BF16) and S2
(--fp8) of hosting/SPEED1_DESIGN.md, behind the same API v1 as the HF fast host (hosting/fastcore), reached through a
modal.forward tunnel. NEW file: nothing pinned is edited (decoder_io.py, prism_x.py, writeblock.py and hosting/fastcore
are copied into the image read-only) and the account Volume is mounted READ-ONLY.

Two processes in one container (SGLang's own image, lmsysorg/sglang:v0.5.20-cu130 = think/modal_think.py's B1a image):
  sglang  `python3 -m sglang.launch_server` on 127.0.0.1:30000 in the image's Python. C1 = the merged checkpoint that
          hosting/export_c1_merged.py wrote to /vol/models/q35_4b_main500k_merged (SGLang's Qwen3.5 LoRA path has no
          in_proj_a / in_proj_b, so the adapter cannot be applied at serve time). Server args (server_cmd):
          --dtype bfloat16 --enable-fp32-lm-head, hybrid (mamba) radix prefix cache ON (--mamba-radix-cache-strategy
          extra_buffer), --linear-attn-backend / --linear-attn-prefill-backend triton, --mamba-ssm-dtype float32, NO
          speculative flags, explicit --max-running-requests / --max-mamba-cache-size, --context-length 16448
          (decoder_io.MAX_LEN 16384 + 64, so a capped 16384-token prompt is accepted), --sampling-defaults openai;
          S2 adds --quantization fp8. Env
          SGLANG_RETURN_ORIGINAL_LOGPROB=1: returned logprobs = log_softmax of the fp32 logits before any temperature.
          The resolved args (GET /server_info) are logged, returned in /health, and checked (check_server_args) before
          the tunnel opens: a boot whose parity-critical args differ is refused (no timing on the wrong engine).
  front   THIS file under /opt/fastpath/bin/python (C1's PINNED35 stack: transformers 5.17 / tokenizers 0.23.2, the
          HF arms' own): API v1 parsing, prompt text, candidate ids and token ids all come from fastcore.readout (=
          decoder_io byte for byte), tokenizer + train_meta from <merged>/c1_tokenizer (sha256-pinned in the merge
          manifest). ONE SGLang /generate call per API request carries every (question, view) sequence as input_ids
          (never text), prefill only: max_new_tokens 0, return_logprob, logprob_start_len -1, token_ids_logprob = each
          sequence's candidate ids, neutral sampling params. Per-letter logit = logsumexp of the candidate logprobs
          (softmax is shift invariant, so this is decoder_io's fp32 logsumexp up to fp32 rounding), then
          fastcore.readout.combine = A5 (2view probability average, noul single read, T = 1.0 / 1.0).
  Checks: SGLang's prompt_tokens must equal len(input_ids) for every sequence; every requested candidate id must come
  back with a logprob (not NaN / +inf; -inf = probability 0); the echoed rids must be in order; a probe set's token + candidate ids (probe_digest) computed on the laptop with the local C1 tokenizer
  must equal the container's (same files, same tokenizers version); the merged checkpoint's files are re-hashed against
  its manifest while SGLang boots; the adapter sha256 in that manifest must be C1's pin.

API v1 (same routes and shapes as the HF host; every route needs "Authorization: Bearer <token>"):
  POST /decide          {"id"?, "state", "return_views"?, "questions": {...}} -> {"id", "answers", "usage": {"input_tokens",
                        "routed_rows": 0, "cached_tokens"}, "timing": {"tokenize_ms", "queue_ms", "model_ms",
                        "readout_ms", "total_ms"}, "server_ms", "engine": "sglang", "path": "sglang", "batch_rows",
                        "sglang": {...}}. 400 bad request, 502 SGLang answered wrongly, 503 closed / SGLang down, 504 timeout
  GET  /health          engine "sglang", model, adapter_sha256, base, revision, readout, flags, config_sha256,
                        quantization, graphs, server_args, gpu, region, boot_s, boot, batcher, queue
  POST /admin/config    {"flags": {...}}: runtime flags only (choice_views 1|2, timeout_s); everything else is a server
                        arg = a new boot. Returns the new /health
  POST /admin/flush     SGLang POST /flush_cache (retried while requests finish)
  POST /shutdown        stops the front end; the Modal function then stops SGLang and returns (ends the GPU bill)
  GET  /ping

Commands, run from lean/ and ONLY after the owner's GO (nothing in this file has run on Modal yet):
  0) free CPU tests:  ../.venv/bin/python -m pytest hosting/tests/test_sglang_host.py -q
  1) once per account: the merged checkpoint (hosting/export_c1_merged.py docstring; ~$0.2-0.3 of CPU credit).
  2) OPTIONAL S1 boot test (boot + smoke + shutdown; about 6-8 billed H100 minutes, ~$0.4-0.6 at --region any,
     ~$0.7-1.0 at us-east; the --hold launch in 3 runs the same smoke first and does not hold when it fails):
       MODAL_PROFILE=mahadikarya3 ../.venv/bin/modal run hosting/sglang_host.py
  3) S1 for SPEED-2: add --hold; it writes speed/session_url.json + speed/session_token.txt (mode 0600, the same files
     and keys as hosting/fast_host.py) and prints the speed_bench command
     (hosting/speed_bench.py ab --url URL --token-file speed/session_token.txt --session NAME --arms S1
     --shutdown-after --go: the bench POSTs /shutdown when it ends, so the session has no idle tail).
     S2 = the same with --fp8 (its own boot). Session budget (all SPEED-2 launches): hosting/fast_host.py docstring.
  Options: --region (default any = x1.0; us-east = x1.75) --seconds (serving window, default 1500) --idle (default
  300; it also covers the smoke-to-bench gap) --smoke N (dev rows checked against the stored L4 served reads before
  holding, default 24) --mrr / --mamba-cache / --mem-fraction / --chunked-prefill (server args) --max-usd (default 6)
  --session NAME. /health also carries serve_deadline_unix / serve_remaining_s (speed_bench's fit check).
Never pass --detach (refused): the laptop is the client, and stopping `modal run` (Ctrl-C) stops the H100.
Cost guards: payer guard (MODAL_PROFILE must be set explicitly to mahadikarya3, or mahadikarya2 as the fallback; no
MODAL_TOKEN_* override; only `modal run`), one container (max_containers=1), GPU "H100!" (no silent upgrade), the
front end stops on POST /shutdown, after --seconds or after --idle seconds without a request, the function timeout
(40 min) is the hard cap, a dead SGLang stops the container, and the launcher refuses when the worst case (timeout x
rate x region multiplier) is above --max-usd. Estimate: H100 $3.95/h list + ~$0.25/h CPU/memory = $4.20/h at
--region any (default), x1.75 for a narrow region (us-east): ~$7.35/h; boot ~5-8 min (image pull, 9 GB weights, CUDA
graphs, mamba pool); worst case 40 min ~$2.8 (any) / ~$4.9 (us-east).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import secrets
import shlex
import signal
import subprocess
import sys
import threading
import time
import traceback
import uuid
from collections import Counter, deque
from pathlib import Path

try:
    import modal
except ImportError:  # the front end runs in /opt/fastpath (C1's PINNED35 stack), which has no Modal client
    modal = None

HERE = Path(__file__).resolve().parent  # lean/hosting locally; /root/hosting (front end) or /root (Modal) remotely
LEAN = HERE.parent
APP_NAME = "od-sglang-host"
BASE = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
C1_MODEL = "q35_4b_main500k"
C1_ADAPTER_SHA256 = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
MERGED_NAME = "q35_4b_main500k_merged"  # hosting/export_c1_merged.py writes it
MANIFEST = "merge_manifest.json"
C1_TOKENIZER_SUBDIR = "c1_tokenizer"  # the adapter's tokenizer + train_meta, copied by the export (sha256 in MANIFEST)
SGLANG_IMAGE = "lmsysorg/sglang:v0.5.20-cu130"  # think/modal_think.py SGLANG_IMAGE (B1a ran on it, 5 Oct)
SGLANG_VERSION = "0.5.20"
UV_PIN = "uv==0.12.23"  # think_image's build steps, so the /opt/fastpath layer is the same one
REMOTE_LEAN = "/root/lean"
REMOTE_HOSTING = "/root/hosting"
FASTPATH_PY = "/opt/fastpath/bin/python"
LEAN_FILES = ("decoder_io.py", "prism_x.py", "writeblock.py")
PORT = 8000  # front end (tunnelled)
SGL_PORT = 30000  # SGLang, localhost only
MAX_LEN = 16384  # decoder_io.MAX_LEN (the front end re-reads it from decoder_io and refuses a mismatch)
CONTEXT_LEN = MAX_LEN + 64  # SGLang refuses input_len >= context_length; a capped prompt is <= MAX_LEN tokens
MAX_BODY = 1 << 20
SERVER_DEFAULTS = {"max_running_requests": 64, "max_mamba_cache_size": 400, "mem_fraction_static": None,
                   "chunked_prefill_size": None}
# Prefill-only scoring: no token is generated; the logprobs are read at the last prompt position. Every sampling knob
# is pinned to its neutral value so no default (model generation_config, server defaults) can reshape the logits.
SAMPLING = {"max_new_tokens": 0, "temperature": 1.0, "top_p": 1.0, "top_k": -1, "min_p": 0.0,
            "repetition_penalty": 1.0, "frequency_penalty": 0.0, "presence_penalty": 0.0}
SERVER_ENV = {"SGLANG_RETURN_ORIGINAL_LOGPROB": "1", "HF_HUB_OFFLINE": "1", "TOKENIZERS_PARALLELISM": "false"}
LOGPROB_MODE = "SGLang output_token_ids_logprobs (log_softmax of fp32 lm-head logits, SGLANG_RETURN_ORIGINAL_LOGPROB=1)"
RUNTIME_FLAGS = {"choice_views": 2, "timeout_s": 120.0}  # what /admin/config can change; the rest are server args
MAX_INFLIGHT = 64  # API requests in flight to SGLang at once (the rest wait: queue_ms)
ALLOWED_PROFILES = ("mahadikarya3", "mahadikarya2")  # free Modal credit (SPEED1_DESIGN.md "Money"); 3 first
GPU = "H100!"
FUNCTION_TIMEOUT_S = 40 * 60
BOOT_BUDGET_S = 15 * 60  # SGLang + front end must be up within this (else the boot is abandoned)
RATE_USD_H = 3.95  # Modal H100 list rate, `modal billing rates` 12 Oct (SPEED1_DESIGN.md)
CPU_MEM_USD_H = 0.25  # [E] 4 reserved cores + 32 GiB next to the GPU
BOOT_EST_S = 8 * 60  # [E]
SMOKE_MIN_AGREE = 0.9  # a lower argmax agreement on the smoke rows means a broken readout: no hold
SERVER_ARGS_KEYS = ("model_path", "dtype", "quantization", "enable_fp32_lm_head", "context_length", "disable_radix_cache",
                    "mamba_radix_cache_strategy", "mamba_ssm_dtype", "mamba_backend", "linear_attn_backend",
                    "linear_attn_prefill_backend", "linear_attn_decode_backend", "max_running_requests",
                    "max_mamba_cache_size", "mem_fraction_static", "chunked_prefill_size", "max_prefill_tokens",
                    "max_total_tokens", "page_size", "attention_backend", "prefill_attention_backend",
                    "decode_attention_backend", "speculative_algorithm", "sampling_defaults", "random_seed",
                    "schedule_policy", "enable_lora", "lora_paths", "disable_overlap_schedule", "version")
GRAPH_KEYS = ("disable_cuda_graph", "disable_prefill_cuda_graph", "disable_decode_cuda_graph", "cuda_graph_max_bs_decode",
              "cuda_graph_max_bs_prefill", "cuda_graph_bs_decode", "cuda_graph_bs_prefill", "cuda_graph_backend_decode",
              "cuda_graph_backend_prefill")
# check_server_args: a mismatch on these refuses the boot; a missing one refuses it only if it is in MUST_BE_PRESENT
CRITICAL_ARGS = ("dtype", "enable_fp32_lm_head", "quantization", "speculative_algorithm", "disable_radix_cache",
                 "model_path", "mamba_radix_cache_strategy", "mamba_ssm_dtype", "linear_attn_backend",
                 "linear_attn_prefill_backend",
                 "context_length", "sampling_defaults")
MUST_BE_PRESENT = ("dtype", "enable_fp32_lm_head", "quantization", "speculative_algorithm", "disable_radix_cache")


# ------------------------------------------------------------------ payer guard (pure; also used by export_c1_merged)

def modal_cli_command(argv=None):
    """The `modal` CLI subcommand this process runs under ("run", "deploy", ...), or None (pytest, plain python)."""
    argv = sys.argv if argv is None else argv
    if not argv:
        return None
    a0 = Path(argv[0])
    if a0.name == "modal" or (a0.name == "__main__.py" and a0.parent.name == "modal"):
        for a in argv[1:]:
            if not a.startswith("-"):
                return a
    return None


def payer_guard(env=None, active=None, argv=None) -> str:
    """Refuse unless the Modal payer is a free-credit account: MODAL_PROFILE set explicitly to one of ALLOWED_PROFILES,
    no MODAL_TOKEN_ID/SECRET in the environment (they override the profile's token), the modal client's active profile
    is that same one, only `modal run` (deploy/serve/shell would leave things up) and never --detach. Returns it."""
    env = os.environ if env is None else env
    argv = sys.argv if argv is None else argv
    prof = env.get("MODAL_PROFILE")
    if not prof:
        raise SystemExit(f"payer guard: set MODAL_PROFILE explicitly ({' or '.join(ALLOWED_PROFILES)}); the default "
                         f"profile is never used")
    if prof not in ALLOWED_PROFILES:
        raise SystemExit(f"payer guard: MODAL_PROFILE={prof!r} is not a free-credit account {ALLOWED_PROFILES} "
                         f"(aryamhd / jaypatil-duke are never used): refusing")
    bad = [k for k in ("MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET") if env.get(k)]
    if bad:
        raise SystemExit(f"payer guard: {bad} set in the environment would override the {prof} token: unset them")
    if active is None:
        try:
            import modal.config as _mc
            active = getattr(_mc, "_profile", prof)
        except Exception:  # noqa: BLE001 - no client: nothing else can pay
            active = prof
    if active != prof:
        raise SystemExit(f"payer guard: the modal client's active profile is {active!r}, not {prof!r}")
    cmd = modal_cli_command(argv)
    if cmd is not None and cmd != "run":
        raise SystemExit(f"payer guard: only `modal run` is allowed here (got `modal {cmd}`)")
    if any(a in ("--detach", "-d") for a in argv[1:]):
        raise SystemExit("payer guard: --detach is refused (Ctrl-C on the laptop must stop the GPU)")
    return prof


if modal is not None and modal.is_local() and modal_cli_command() is not None:
    payer_guard()  # before Modal builds an image or creates an app on the wrong account


# ------------------------------------------------------------------ SGLang server command and checks (pure)

def server_cmd(model_path, fp8: bool = False, port: int = SGL_PORT, max_running_requests: int = 64,
               max_mamba_cache_size: int = 400, mem_fraction_static=None, chunked_prefill_size=None,
               context_length: int = CONTEXT_LEN, python: str = "python3") -> list:
    """The SGLang launch command of arm S1 (fp8=False) or S2 (fp8=True). Every flag checked against the sglang source
    of the B1a image (commit 94602c9c = 0.5.20: srt/arg_groups/fields/{exec_,schedule,serving,model,device,
    observability}.py, CLI name = "--" + field with dashes, bools store_true) on 12 Oct 2026. extra_buffer needs
    linear_attn_backend == "triton" for Qwen3_5ForConditionalGeneration (arg_groups/overrides.py), hence both pins."""
    cmd = [python, "-m", "sglang.launch_server", "--model-path", str(model_path), "--host", "127.0.0.1",
           "--port", str(int(port)), "--dtype", "bfloat16", "--enable-fp32-lm-head",
           "--context-length", str(int(context_length)),
           "--mamba-radix-cache-strategy", "extra_buffer", "--mamba-ssm-dtype", "float32",
           "--linear-attn-backend", "triton", "--linear-attn-prefill-backend", "triton",
           "--max-running-requests", str(int(max_running_requests)),
           "--max-mamba-cache-size", str(int(max_mamba_cache_size)),
           "--random-seed", "0", "--sampling-defaults", "openai", "--log-level", "warning"]
    if mem_fraction_static:
        cmd += ["--mem-fraction-static", str(float(mem_fraction_static))]
    if chunked_prefill_size:
        cmd += ["--chunked-prefill-size", str(int(chunked_prefill_size))]
    if fp8:
        cmd += ["--quantization", "fp8"]
    if any("speculative" in c for c in cmd):
        raise ValueError("server_cmd: no speculative decoding on the scoring arms")
    return cmd


def server_env(base=None) -> dict:
    env = {k: v for k, v in (os.environ if base is None else base).items() if k not in ("PYTHONPATH", "VIRTUAL_ENV")}
    env.update(SERVER_ENV)
    return env


def want_server_args(model_path, fp8: bool, server: dict | None = None) -> dict:
    s = {**SERVER_DEFAULTS, **(server or {})}
    return {"dtype": "bfloat16", "enable_fp32_lm_head": True, "quantization": "fp8" if fp8 else None,
            "speculative_algorithm": None, "disable_radix_cache": False, "model_path": str(model_path),
            "mamba_radix_cache_strategy": "extra_buffer", "mamba_ssm_dtype": "float32",
            "linear_attn_backend": "triton", "linear_attn_prefill_backend": "triton", "context_length": CONTEXT_LEN, "sampling_defaults": "openai",
            "random_seed": 0, "max_running_requests": int(s["max_running_requests"]),
            "max_mamba_cache_size": int(s["max_mamba_cache_size"])}


def _norm_arg(k, v):
    if k in ("quantization", "speculative_algorithm") and v in (None, "", "none", "None", False):
        return None
    if isinstance(v, str) and k in ("model_path",):
        return v.rstrip("/")
    return v


def check_server_args(resolved: dict, want: dict) -> tuple:
    """(problems, warnings) of SGLang's resolved args (GET /server_info) vs what this arm needs. Problems refuse the
    boot: a parity-critical arg differs, or a must-have one is absent, or the version is not SGLANG_VERSION."""
    problems, warnings = [], []
    for k, w in want.items():
        if k not in resolved:
            (problems if k in MUST_BE_PRESENT else warnings).append(f"{k}: absent from /server_info (wanted {w!r})")
            continue
        got = resolved[k]
        if _norm_arg(k, got) != _norm_arg(k, w):
            (problems if k in CRITICAL_ARGS else warnings).append(f"{k}: {got!r} (wanted {w!r})")
    ver = resolved.get("version")
    if ver is None:
        warnings.append("version: absent from /server_info")
    elif str(ver) != SGLANG_VERSION:
        problems.append(f"version: sglang {ver} != pinned {SGLANG_VERSION}")
    if resolved.get("enable_lora") or resolved.get("lora_paths"):
        problems.append("LoRA is enabled: the scoring arms serve the merged checkpoint only")
    return problems, warnings


def args_subset(resolved: dict) -> dict:
    return {k: resolved.get(k) for k in SERVER_ARGS_KEYS if k in resolved}


def graphs_info(resolved: dict) -> dict:
    return {"engine": "sglang", "n_graphs": None, "cuda_graph": {k: resolved.get(k) for k in GRAPH_KEYS if k in resolved}}


# ------------------------------------------------------------------ /generate request and response (pure)

class UpstreamError(RuntimeError):
    """SGLang answered, but not with what this front end asked for (HTTP 502)."""
    status = 502


class UpstreamUnavailable(RuntimeError):
    """SGLang cannot be reached (HTTP 503)."""
    status = 503


class UpstreamTimeout(TimeoutError):
    """SGLang did not answer within the request timeout (HTTP 504)."""
    status = 504


def build_generate_body(items, rid_prefix: str | None = None) -> dict:
    """ONE SGLang /generate body for a request's work items (fastcore.readout.WorkItem, tokenized): sequence i = item i
    (questions in request order, view 0 then view 1), token_ids_logprob[i] = item i's candidate ids in Readout.cand
    order (group by group)."""
    if any(it.ids is None for it in items):
        raise ValueError("build_generate_body: tokenize the items first")
    body = {"input_ids": [list(map(int, it.ids)) for it in items], "sampling_params": dict(SAMPLING),
            "return_logprob": True, "logprob_start_len": -1,
            "token_ids_logprob": [list(map(int, it.flat)) for it in items], "stream": False}
    if rid_prefix:
        body["rid"] = [f"{rid_prefix}-{i}" for i in range(len(items))]
    return body


def parse_generate_response(items, resp, rids=None):
    """SGLang's batch /generate answer -> ([per-group fp32 logits tensor per item], meta). Group value = logsumexp of
    the group's candidate logprobs (logprob = logit - logsumexp(all logits): the shared shift cancels in to_probs)."""
    import torch
    if not isinstance(resp, list) or len(resp) != len(items):
        n = len(resp) if isinstance(resp, list) else type(resp).__name__
        raise UpstreamError(f"/generate returned {n} results for {len(items)} sequences")
    out, prompt, cached, e2e = [], 0, 0, 0.0
    any_cached = False
    rid_set = set(rids or ())
    for i, (it, r) in enumerate(zip(items, resp)):
        mi = (r or {}).get("meta_info") if isinstance(r, dict) else None
        if not isinstance(mi, dict):
            raise UpstreamError(f"sequence {i}: no meta_info")
        if mi.get("id") in rid_set and mi["id"] != rids[i]:  # SGLang echoes the rids we sent: order check
            raise UpstreamError(f"sequence {i}: rid {mi['id']!r} != {rids[i]!r} (results out of order)")
        pt = mi.get("prompt_tokens")
        if pt is not None and int(pt) != it.n_tokens:
            raise UpstreamError(f"sequence {i}: SGLang read {pt} prompt tokens, sent {it.n_tokens}")
        prompt += it.n_tokens if pt is None else int(pt)
        if isinstance(mi.get("cached_tokens"), (int, float)) and not isinstance(mi.get("cached_tokens"), bool):
            cached += int(mi["cached_tokens"])
            any_cached = True
        if isinstance(mi.get("e2e_latency"), (int, float)):
            e2e = max(e2e, float(mi["e2e_latency"]))
        pos = mi.get("output_token_ids_logprobs")
        if not isinstance(pos, list) or not pos or not isinstance(pos[0], list):
            raise UpstreamError(f"sequence {i}: no output_token_ids_logprobs")
        got = {}
        for trip in pos[0]:
            if not isinstance(trip, (list, tuple)) or len(trip) < 2 or trip[0] is None:
                raise UpstreamError(f"sequence {i}: bad logprob entry {trip!r}")
            got[int(trip[1])] = float(trip[0])
        miss = [t for t in it.flat if t not in got]
        if miss:
            raise UpstreamError(f"sequence {i}: {len(miss)} candidate ids without a logprob (e.g. {miss[:3]})")
        vals = torch.tensor([got[t] for t in it.flat], dtype=torch.float32)
        if torch.isnan(vals).any() or torch.isposinf(vals).any():
            raise UpstreamError(f"sequence {i}: non-finite candidate logprobs")
        parts, k = [], 0
        for s in it.sizes:
            parts.append(torch.logsumexp(vals[k:k + s], 0))
            k += s
        out.append(torch.stack(parts))
    meta = {"prompt_tokens": prompt, "cached_tokens": cached if any_cached else None,
            "e2e_ms": round(e2e * 1000, 3) if e2e else None}
    return out, meta


def smoke_compare(pairs) -> dict:
    """[(qtype, options, stored_probs, answer)] -> argmax agreement and |dp| of API answers vs stored reads."""
    agree, dps, n = 0, [], 0
    for qtype, options, ref, ans in pairs:
        if not isinstance(ans, dict):
            dps.append(1.0)
            n += 1
            continue
        if qtype == "noul":
            p = {"yes": float(ans["noul"]), "no": 1.0 - float(ans["noul"])}
            r = {"yes": float(ref["yes"]), "no": 1.0 - float(ref["yes"])}
        else:
            p = {o: float(ans["probabilities"][o]) for o in options}
            r = {o: float(ref[o]) for o in options}
        n += 1
        agree += max(p, key=p.get) == max(r, key=r.get)
        dps.append(max(abs(p[k] - r[k]) for k in r))
    return {"n": n, "argmax_agree": round(agree / n, 4) if n else None,
            "max_abs_dp": round(max(dps), 5) if dps else None,
            "mean_abs_dp": round(sum(dps) / len(dps), 5) if dps else None}


# ------------------------------------------------------------------ SGLang HTTP client

class SGLangClient:
    """Pooled keep-alive client of the local SGLang server (thread-safe: one httpx.Client for every HTTP thread)."""

    def __init__(self, base_url: str, timeout: float = 120.0, max_connections: int = 2 * MAX_INFLIGHT):
        import httpx
        self.httpx = httpx
        self.base_url = base_url.rstrip("/")
        self.c = httpx.Client(base_url=self.base_url, timeout=httpx.Timeout(timeout, connect=5.0),
                              limits=httpx.Limits(max_connections=max_connections,
                                                  max_keepalive_connections=max_connections),
                              transport=httpx.HTTPTransport(retries=0))

    def generate(self, body: dict, timeout: float):
        hx = self.httpx
        try:
            r = self.c.post("/generate", json=body, timeout=hx.Timeout(timeout, connect=5.0))
        except hx.TimeoutException as e:
            raise UpstreamTimeout(f"SGLang /generate: no answer within {timeout} s") from e
        except hx.TransportError as e:
            raise UpstreamUnavailable(f"SGLang unreachable: {type(e).__name__}: {e}") from e
        if r.status_code != 200:
            raise UpstreamError(f"SGLang /generate HTTP {r.status_code}: {r.text[:500]}")
        try:
            return r.json()
        except ValueError as e:
            raise UpstreamError(f"SGLang /generate: invalid JSON ({e})") from None

    def abort(self, rids) -> None:
        """Best effort: drop sequences whose caller gave up (a timed-out request must not keep the GPU busy)."""
        for rid in rids or ():
            try:
                self.c.post("/abort_request", json={"rid": rid}, timeout=2.0)
            except Exception:  # noqa: BLE001
                pass

    def flush(self, tries: int = 20, wait_s: float = 0.5) -> dict:
        """POST /flush_cache; SGLang answers 400 while requests run, so retry for up to tries x wait_s seconds."""
        last = None
        for i in range(tries):
            try:
                r = self.c.post("/flush_cache", timeout=30.0)
            except self.httpx.HTTPError as e:
                raise UpstreamUnavailable(f"SGLang /flush_cache: {type(e).__name__}: {e}") from e
            last = (r.status_code, r.text[:300])
            if r.status_code == 200:
                return {"ok": True, "tries": i + 1, "sglang": r.text.strip()[:300]}
            time.sleep(wait_s)
        raise UpstreamUnavailable(f"SGLang /flush_cache failed {tries} times: {last}")

    def alive(self, timeout: float = 5.0) -> bool:
        try:
            return self.c.get("/health", timeout=timeout).status_code == 200
        except Exception:  # noqa: BLE001
            return False

    def server_info(self) -> dict:
        for path in ("/server_info", "/get_server_info"):
            try:
                r = self.c.get(path, timeout=30.0)
            except self.httpx.HTTPError:
                continue
            if r.status_code == 200:
                return r.json()
        raise UpstreamUnavailable("SGLang /server_info unavailable")

    def close(self):
        self.c.close()


# ------------------------------------------------------------------ the front end (API v1 decider)

def _readout():
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    from fastcore import readout as R
    return R


def probe_requests() -> list:
    """Fixed API v1 requests whose token + candidate ids must be identical on the laptop and in the container: the
    host's EXAMPLE, a carded yes/no, a 30-option choice (two-letter labels after Z) and a non-ASCII state."""
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    from fastcore.engine import EXAMPLE
    wide = [f"option {i:02d}" for i in range(30)]
    return [EXAMPLE,
            {"state": "Ticket: the refund for order 1182 has not arrived after 14 days.",
             "questions": {"q": {"type": "noul", "instructions": "Is this a refund delay?",
                                 "card": "refund delay: money promised back has not arrived on time"}}},
            {"state": "The caller wants option 17 and nothing else.",
             "questions": {"w": {"type": "choice", "instructions": "Which option does the caller want?",
                                 "options": wide}}},
            {"state": "Café Zürich: «Le paiement a été refusé» — ¿por qué? 支付失败。",
             "questions": {"u": {"type": "choice", "instructions": "Which issue is described?",
                                 "options": ["payment refused", "late delivery"]}}}]


def probe_digest(ro, tok) -> dict:
    """sha256 over the probe requests' (question, view, token ids, candidate ids): the HF path's tokenization and
    Readout, wherever this runs."""
    R = _readout()
    h, n_items, n_tokens = hashlib.sha256(), 0, 0
    for req in probe_requests():
        named = R.parse_v1(req)
        items = R.build_items(ro, named, choice_views=2, render=True)
        R.tokenize_items(tok, items)
        for it in items:
            h.update(json.dumps([it.q, it.view, it.perm, it.ids, it.flat, it.sizes]).encode())
            n_items += 1
            n_tokens += it.n_tokens
    return {"sha256": h.hexdigest(), "items": n_items, "tokens": n_tokens}


class SGLangFrontEnd:
    """API v1 on top of a running SGLang server. Thread-safe: any number of HTTP threads may call decide() at once
    (SGLang batches the sequences of concurrent requests itself: continuous batching + radix prefix cache)."""

    def __init__(self, client, tok, ro=None, quantization: str | None = None, server_args: dict | None = None,
                 flags: dict | None = None, temps: dict | None = None, context_len: int = CONTEXT_LEN,
                 max_inflight: int = MAX_INFLIGHT, expect_layout=("schema_branch_mark", "cygnet"), log=print):
        R = _readout()
        self.R, self.dio = R, R.dio
        if expect_layout is not None and (self.dio.LAYOUT, self.dio.STYLE) != tuple(expect_layout):
            raise RuntimeError(f"decoder_io layout/style {(self.dio.LAYOUT, self.dio.STYLE)} != expected "
                               f"{tuple(expect_layout)}: resolve C1's train_meta.json (decoder_io.resolve_prompt) first")
        if self.dio.MAX_LEN != MAX_LEN:
            raise RuntimeError(f"decoder_io.MAX_LEN {self.dio.MAX_LEN} != {MAX_LEN}: CONTEXT_LEN would be wrong")
        self.client, self.tok, self.log = client, tok, log
        self.ro = ro if ro is not None else self.dio.Readout(tok)  # full vocabulary scan: two-letter labels
        if R.max_options() < R.MAX_OPTIONS:
            raise RuntimeError(f"two-letter labels: only {R.max_options()} options readable (Readout not built?)")
        self.quantization = quantization
        self.server_args = dict(server_args or {})
        self.temps = dict(R.TEMPS if temps is None else temps)
        self.context_len = int(context_len)
        self.flags = dict(RUNTIME_FLAGS)
        if flags:
            self.flags = self._validated(flags)
        self.max_inflight = int(max_inflight)
        self._sem = threading.BoundedSemaphore(self.max_inflight)
        self._lock = threading.Lock()
        self._counts = Counter()
        self._ms = deque(maxlen=20000)
        self._inflight = self._inflight_max = 0
        self.closed = False
        self.boot_report = None

    # ---------------------------------------------------------------- flags
    def _validated(self, update) -> dict:
        R = self.R
        if not isinstance(update, dict):
            raise R.RequestError('"flags" must be an object')
        unknown = sorted(set(update) - set(RUNTIME_FLAGS))
        if unknown:
            raise R.RequestError(f"unknown or non-runtime flag(s) {unknown}: the SGLang host changes only "
                                 f"{sorted(RUNTIME_FLAGS)} at runtime; every other setting is a server arg (new boot)")
        new = dict(self.flags)
        for k, v in update.items():
            if k == "choice_views":
                if isinstance(v, bool) or v not in (1, 2):
                    raise R.RequestError("choice_views must be 1 or 2")
                v = int(v)
            elif k == "timeout_s":
                if isinstance(v, bool) or not isinstance(v, (int, float)) or not 1.0 <= float(v) <= 600.0:
                    raise R.RequestError("timeout_s must be a number of seconds in [1, 600]")
                v = float(v)
            new[k] = v
        return new

    def set_flags(self, update) -> dict:
        """POST /admin/config {"flags": update}: validated, all or nothing (RequestError -> 400)."""
        new = self._validated(update)
        with self._lock:
            self.flags = new
        return self.flags_view()

    def flags_view(self) -> dict:
        f = dict(self.flags)
        return {**f, "effective": {**f, "engine": "sglang", "readout": "exact", "max_inflight": self.max_inflight,
                                   "batching": "SGLang continuous batching (server args)"}}

    # ---------------------------------------------------------------- serving
    def decide(self, req, timeout: float | None = None) -> dict:
        """One API v1 request -> the API v1 response (the HTTP layer adds server_ms). RequestError (400),
        UpstreamError (502), EngineClosed / UpstreamUnavailable (503), UpstreamTimeout (504)."""
        R = self.R
        t0 = time.perf_counter()
        if self.closed:
            from fastcore import EngineClosed
            raise EngineClosed("front end is shut down")
        named = R.parse_v1(req)
        f = dict(self.flags)
        items = R.build_items(self.ro, named, choice_views=f["choice_views"], render=True)
        R.tokenize_items(self.tok, items)
        long = [it.n_tokens for it in items if it.n_tokens >= self.context_len]
        if long:
            raise R.RequestError(f"a prompt of {max(long)} tokens is over the context length {self.context_len}")
        rid_prefix = uuid.uuid4().hex
        body = build_generate_body(items, rid_prefix)
        rids = body["rid"]
        t1 = time.perf_counter()
        tmo = float(f["timeout_s"] if timeout is None else timeout)
        if not self._sem.acquire(timeout=tmo):
            self._count("timeouts")
            raise UpstreamTimeout(f"no SGLang slot within {tmo} s ({self.max_inflight} requests in flight)")
        try:
            with self._lock:
                self._inflight += 1
                self._inflight_max = max(self._inflight_max, self._inflight)
            t2 = time.perf_counter()
            try:
                resp = self.client.generate(body, timeout=max(0.1, tmo - (t2 - t0)))
            except UpstreamTimeout as e:
                self._count("timeouts")
                self.client.abort(rids)
                raise UpstreamTimeout(f"SGLang /generate: no answer within the {tmo} s request timeout") from e
            except Exception:
                self._count("upstream_errors")
                raise
            t3 = time.perf_counter()
        finally:
            with self._lock:
                self._inflight -= 1
            self._sem.release()
        try:
            logits, meta = parse_generate_response(items, resp, rids)
        except UpstreamError:
            self._count("upstream_errors")
            raise
        answers, usage = R.combine(named, items, logits, self.temps, return_views=bool(req.get("return_views")))
        usage["cached_tokens"] = meta["cached_tokens"]
        t4 = time.perf_counter()
        with self._lock:
            self._counts.update(requests=1, sequences=len(items), input_tokens=usage["input_tokens"],
                                cached_tokens=meta["cached_tokens"] or 0)
            self._ms.append((t3 - t2) * 1000)
        ms = lambda a, b: round((b - a) * 1000, 3)  # noqa: E731
        return {"id": req.get("id"), "answers": answers, "usage": usage,
                "timing": {"tokenize_ms": ms(t0, t1), "queue_ms": ms(t1, t2), "model_ms": ms(t2, t3),
                           "readout_ms": ms(t3, t4), "total_ms": ms(t0, t4)},
                "engine": "sglang", "path": "sglang", "batch_rows": len(items), "sglang": meta}

    def _count(self, k):
        with self._lock:
            self._counts[k] += 1

    def flush(self) -> dict:
        """POST /admin/flush: SGLang's radix cache (KV + mamba states) is emptied."""
        out = self.client.flush()
        self._count("flushes")
        return out

    def stats(self) -> dict:
        with self._lock:
            c, ms = dict(self._counts), sorted(self._ms)
            inflight, imax = self._inflight, self._inflight_max
        pick = (lambda q: round(ms[min(len(ms) - 1, int(q * len(ms)))], 3)) if ms else (lambda q: None)
        base = {k: c.get(k, 0) for k in ("requests", "sequences", "input_tokens", "cached_tokens", "timeouts",
                                         "upstream_errors", "flushes")}
        return {**base, "generate_ms_p50": pick(0.5), "generate_ms_p95": pick(0.95),
                "cached_token_share": round(base["cached_tokens"] / base["input_tokens"], 4) if base["input_tokens"]
                else None, "inflight": inflight, "inflight_max": imax, "alive": not self.closed}

    def config_sha256(self) -> str:
        cfg = {"flags": self.flags, "readout": self.R.readout_info(), "temps": self.temps,
               "quantization": self.quantization, "sampling": SAMPLING, "logprobs": LOGPROB_MODE,
               "server_args": args_subset(self.server_args), "context_len": self.context_len}
        return hashlib.sha256(json.dumps(cfg, sort_keys=True, default=str).encode()).hexdigest()

    def health(self) -> dict:
        """The engine's part of GET /health (the host adds model, adapter_sha256, base, revision, gpu, region, boot_s,
        boot)."""
        alive = self.client.alive()
        st = self.stats()
        return {"ok": bool(alive and not self.closed), "engine": "sglang", "api": self.R.API_VERSION,
                "readout": {**self.R.readout_info(), "logprobs": LOGPROB_MODE, "sampling": SAMPLING},
                "flags": self.flags_view(), "config_sha256": self.config_sha256(), "quantization": self.quantization,
                "graphs": graphs_info(self.server_args), "server_args": args_subset(self.server_args),
                "sglang": {"url": getattr(self.client, "base_url", None), "alive": alive,
                           "version": self.server_args.get("version")},
                "batcher": st, "queue": {"inflight": st["inflight"], "max_inflight": self.max_inflight}}

    def boot(self, warm_requests: int = 3, probe_sha256: str | None = None, flush: bool = True) -> dict:
        """Probe ids vs the laptop's, then warm requests through the whole path (the first timed request is not the
        first one), then an empty prefix cache."""
        t0 = time.time()
        rep = {"probe": probe_digest(self.ro, self.tok)}
        rep["probe"]["expected"] = probe_sha256
        rep["probe"]["match"] = None if probe_sha256 is None else rep["probe"]["sha256"] == probe_sha256
        if rep["probe"]["match"] is False:
            raise RuntimeError(f"token/candidate ids differ from the laptop's HF path: {rep['probe']}")
        R = self.R
        warm = [{**q, "id": f"warm{i}", "return_views": True} for i, q in enumerate(probe_requests())]
        rep["warm"] = []
        for i in range(max(0, warm_requests)):
            out = self.decide(warm[i % len(warm)])
            for k, a in out["answers"].items():
                p = a["probabilities"]
                if not all(math.isfinite(v) for v in p.values()) or abs(sum(p.values()) - 1.0) > 1e-4:
                    raise RuntimeError(f"warm request {out['id']}: probabilities of {k} are not a distribution: {p}")
            rep["warm"].append({"id": out["id"], "model_ms": out["timing"]["model_ms"],
                                "answers": {k: {kk: a.get(kk) for kk in ("choice", "noul", "confidence")}
                                            for k, a in out["answers"].items()}})
        with self._lock:
            self._counts.clear()
            self._ms.clear()
            self._inflight_max = 0
        rep["flush"] = self.flush() if flush else None
        with self._lock:
            self._counts.clear()
        rep["readout"] = R.readout_info()
        rep["boot_s"] = round(time.time() - t0, 2)
        self.boot_report = rep
        return rep

    def close(self):
        self.closed = True


# ------------------------------------------------------------------ HTTP server (stdlib, like core.make_server)

def http_status(e: BaseException) -> int:
    from fastcore import EngineClosed
    if isinstance(e, (UpstreamError, UpstreamUnavailable, UpstreamTimeout)):
        return e.status
    if isinstance(e, EngineClosed):
        return 503
    if isinstance(e, TimeoutError):  # concurrent.futures.TimeoutError is TimeoutError on Python >= 3.11
        return 504
    if isinstance(e, ValueError):  # fastcore RequestError, json.JSONDecodeError
        return 400
    return 500


def make_frontend_server(port, token, fe, host_info, on_shutdown, state=None, host="0.0.0.0"):
    """API v1 HTTP/1.1 server around a SGLangFrontEnd (keep-alive, TCP_NODELAY, one write per response). host_info()
    -> the host's /health fields (model, adapter_sha256, base, revision, gpu, region, boot_s, boot)."""
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    import hmac
    st = state if state is not None else {"last": time.time(), "n": 0, "errors": 0}
    want = f"Bearer {token}".encode()
    hinfo = host_info if callable(host_info) else (lambda: dict(host_info or {}))

    def full_health():
        return {**fe.health(), **hinfo(), "served": st["n"], "errors": st["errors"]}

    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        disable_nagle_algorithm = True
        wbufsize = 1 << 16
        server_version = "od-sglang-host"
        sys_version = ""

        def _reply(self, code, obj):
            body = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _authed(self) -> bool:
            if hmac.compare_digest((self.headers.get("Authorization") or "").encode(), want):
                return True
            self._reply(401, {"error": "unauthorized"})
            return False

        def _fail(self, e):
            code = http_status(e)
            st["errors"] += 1
            if code == 500:
                traceback.print_exc()
            self._reply(code, {"error": f"{type(e).__name__}: {e}" if code >= 500 else str(e)})

        def do_GET(self):
            if not self._authed():
                return
            if self.path == "/ping":
                self._reply(200, {"ok": True})
            elif self.path == "/health":
                self._reply(200, full_health())
            else:
                self._reply(404, {"error": "not found"})

        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            if n > MAX_BODY:
                self.close_connection = True
                self._reply(413, {"error": "body too large"})
                return
            raw = self.rfile.read(n)
            if not self._authed():
                return
            t0 = time.perf_counter()
            st["last"] = time.time()
            try:
                if self.path in ("/decide", "/"):
                    out = fe.decide(json.loads(raw))
                    st["n"] += 1
                    out["server_ms"] = round((time.perf_counter() - t0) * 1000, 3)  # body read -> response ready
                    self._reply(200, out)
                elif self.path == "/admin/config":
                    body = json.loads(raw or b"{}")
                    if not isinstance(body, dict) or "flags" not in body:
                        raise ValueError('POST /admin/config takes {"flags": {...}}')
                    fe.set_flags(body["flags"])
                    self._reply(200, full_health())
                elif self.path == "/admin/flush":
                    self._reply(200, fe.flush())
                elif self.path == "/shutdown":
                    self._reply(200, {"ok": True, "served": st["n"]})
                    on_shutdown()
                else:
                    self._reply(404, {"error": "not found"})
            except Exception as e:  # noqa: BLE001 - a failed request must not kill the server
                self._fail(e)

        def log_message(self, *a):
            pass

    class S(ThreadingHTTPServer):
        daemon_threads = True
        allow_reuse_address = True

    return S((host, port), H), st


def wait_loop(stop, st, seconds, idle_s) -> str:
    """core.wait_loop (copied: the front end's Python has no Modal client, so core cannot be imported there)."""
    deadline = time.time() + seconds
    while True:
        if stop.wait(1):
            return "shutdown request"
        if time.time() > deadline:
            return f"--seconds {seconds} reached"
        if time.time() - st["last"] > idle_s:
            return f"idle for {idle_s} s"


# ------------------------------------------------------------------ front-end process (/opt/fastpath)

def load_c1_tokenizer(c1_dir, base: str = BASE):
    """decoder_io's own tokenizer load for C1: LAYOUT/STYLE/revision from train_meta.json (resolve_prompt, as
    decoder_io.load sets them), the tokenizer files from the same folder (load_tokenizer), one full Readout."""
    R = _readout()
    dio = R.dio
    info = dio.resolve_prompt([str(c1_dir)], base, None, None, None)
    dio.LAYOUT, dio.STYLE = info["layout"], info["style"]
    tok = dio.load_tokenizer(base, adapter=str(c1_dir), revision=info["revision"])
    return tok, dio.Readout(tok), info


def _write_json(path, obj):
    p = Path(path)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, default=str))
    os.replace(tmp, p)


def run_frontend(cfg: dict, token: str, client=None, stop=None, log=print) -> dict:
    """The front end's whole life: tokenizer, front end, boot (probe + warm-up + flush), ready file, serve until
    /shutdown, --seconds or --idle, then a done file. cfg keys: sglang_url, c1_tokenizer_dir, port, seconds, idle_s,
    quantization, server_args, host_info, probe_sha256, ready_file, done_file, t0 (container start, for boot_s)."""
    t0 = time.time()
    tok, ro, tinfo = load_c1_tokenizer(cfg["c1_tokenizer_dir"])
    t_tok = round(time.time() - t0, 2)
    client = client or SGLangClient(cfg["sglang_url"])
    fe = SGLangFrontEnd(client, tok, ro, quantization=cfg.get("quantization"), server_args=cfg.get("server_args"),
                        log=log)
    boot = fe.boot(warm_requests=int(cfg.get("warm_requests", 3)), probe_sha256=cfg.get("probe_sha256"))
    boot["tokenizer"] = {"layout": tinfo["layout"], "style": tinfo["style"], "revision": tinfo["revision"],
                         "dir": str(cfg["c1_tokenizer_dir"]), "tokenizer_and_readout_s": t_tok}
    host = dict(cfg.get("host_info") or {})
    host["boot_s"] = round(time.time() - float(cfg.get("t0", t0)), 1)
    host["boot"] = {**(host.get("boot") or {}), "frontend": boot}
    stop = stop or threading.Event()
    dl = [None]  # the serving deadline (unix s), set when the window starts

    def host_view():  # /health: the host's fields + the serving window (speed_bench refuses an arm that cannot fit)
        if dl[0] is None:
            return host
        return {**host, "serve_deadline_unix": round(dl[0], 3),
                "serve_remaining_s": round(max(0.0, dl[0] - time.time()), 1)}

    srv, st = make_frontend_server(int(cfg["port"]), token, fe, host_view, stop.set, host=cfg.get("host", "0.0.0.0"))
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    st["last"] = time.time()
    seconds = float(cfg.get("seconds", 1500))
    dl[0] = time.time() + seconds  # wait_loop's own deadline is set a few ms later: remaining is never overstated
    if cfg.get("ready_file"):
        _write_json(cfg["ready_file"], {"ok": True, "port": srv.server_address[1],
                                        "health": {**fe.health(), **host_view()}})
    log(f"FRONTEND READY port {srv.server_address[1]} boot {json.dumps(boot, default=str)[:3000]}")
    reason = wait_loop(stop, st, seconds, float(cfg.get("idle_s", 300)))
    srv.shutdown()
    srv.server_close()
    fe.close()
    done = {"stop": reason, "served": st["n"], "errors": st["errors"], "stats": fe.stats(), "boot": boot,
            "wall_s": round(time.time() - t0, 1)}
    if cfg.get("done_file"):
        _write_json(cfg["done_file"], done)
    log("FRONTEND DONE " + json.dumps(done, default=str)[:3000])
    return done


def frontend_main(argv=None) -> int:
    """`python sglang_host.py frontend --config F` (token in env OD_SGL_TOKEN, never on the command line)."""
    import argparse
    ap = argparse.ArgumentParser(description="od-sglang-host front end")
    ap.add_argument("cmd", choices=["frontend"])
    ap.add_argument("--config", required=True)
    a = ap.parse_args(argv)
    cfg = json.loads(Path(a.config).read_text())
    token = os.environ.get("OD_SGL_TOKEN") or ""
    if not token:
        raise SystemExit("OD_SGL_TOKEN is not set")
    try:
        run_frontend(cfg, token, log=lambda s: print(s, flush=True))
    except Exception as e:  # noqa: BLE001 - the Modal function reads the error file and stops the GPU
        traceback.print_exc()
        if cfg.get("ready_file"):
            _write_json(cfg["ready_file"], {"ok": False, "error": f"{type(e).__name__}: {e}"[:3000]})
        return 1
    return 0


# ------------------------------------------------------------------ container helpers (Modal function side)

def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_manifest(mdir, adapter_sha: str = C1_ADAPTER_SHA256) -> tuple:
    """(manifest, problems) of a merged checkpoint folder: it must be export_c1_merged's, for C1's adapter, with
    every file listed (weights, config, tokenizers, c1_tokenizer/*)."""
    mdir = Path(mdir)
    p = mdir / MANIFEST
    if not p.exists():
        return None, [f"{p} missing: run hosting/export_c1_merged.py on this account first"]
    man = json.loads(p.read_text())
    problems = []
    if man.get("adapter_sha256") != adapter_sha:
        problems.append(f"manifest adapter_sha256 {str(man.get('adapter_sha256'))[:16]} != C1's {adapter_sha[:16]}")
    files = man.get("files") or {}
    if not any(f.endswith(".safetensors") for f in files):
        problems.append("manifest lists no .safetensors file")
    for need in (f"{C1_TOKENIZER_SUBDIR}/train_meta.json", f"{C1_TOKENIZER_SUBDIR}/tokenizer.json", "config.json"):
        if need not in files:
            problems.append(f"manifest lists no {need}")
    if not (man.get("checks") or {}).get("passed"):
        problems.append("manifest checks did not pass")
    return man, problems


def verify_files(mdir, man) -> list:
    """Re-hash every file the manifest lists; returns the problems (empty = identical to what the export verified)."""
    problems = []
    for rel, meta in sorted((man.get("files") or {}).items()):
        p = Path(mdir) / rel
        if not p.exists():
            problems.append(f"{rel}: missing")
        elif sha256_file(p) != meta["sha256"]:
            problems.append(f"{rel}: sha256 differs from the manifest")
    return problems


def gpu_name() -> str | None:
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
                           capture_output=True, text=True, timeout=20)
        return r.stdout.strip() or None
    except Exception:  # noqa: BLE001
        return None


def stop_process(proc, grace: float = 30.0) -> int | None:
    """SIGTERM the process group (SGLang forks scheduler/detokenizer processes), SIGKILL after `grace` s."""
    if proc is None or proc.poll() is not None:
        return None if proc is None else proc.returncode
    for sig, wait in ((signal.SIGTERM, grace), (signal.SIGKILL, 10.0)):
        try:
            os.killpg(os.getpgid(proc.pid), sig)
        except (ProcessLookupError, PermissionError):
            pass
        try:
            return proc.wait(timeout=wait)
        except subprocess.TimeoutExpired:
            continue
    return proc.poll()


def pump(proc, tail: deque, prefix: str):
    """Print a child's output with a prefix and keep its last lines (the error tail of a failed boot)."""
    def run():
        for line in proc.stdout:
            line = line.rstrip("\n")
            tail.append(line)
            print(f"{prefix} {line}", flush=True)
    t = threading.Thread(target=run, daemon=True)
    t.start()
    return t


def wait_http_ready(url: str, proc, timeout_s: float, tail=None, path: str = "/health") -> float:
    import httpx
    t0 = time.time()
    while True:
        if proc.poll() is not None:
            raise RuntimeError(f"SGLang exited ({proc.returncode}) during boot; last lines:\n" +
                               "\n".join(list(tail or [])[-40:]))
        try:
            if httpx.get(url.rstrip("/") + path, timeout=5.0).status_code == 200:
                return round(time.time() - t0, 1)
        except httpx.HTTPError:
            pass
        if time.time() - t0 > timeout_s:
            raise RuntimeError(f"SGLang not ready after {timeout_s} s")
        time.sleep(2)


def write_session(path, url: str, token: str, flags, extra: dict | None = None, token_path=None) -> dict:
    """speed/session_url.json = {url, token, started_at, flags, ...} and the plain token in token_path (speed_bench
    --token-file), both mode 0600: the same files and keys as hosting/fast_host.py (copied, not imported)."""
    rec = {"url": url, "token": token, "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "flags": flags, **(extra or {})}

    def put(p, text):
        p = Path(p)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_name(p.name + ".tmp")
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(text)
        os.chmod(tmp, 0o600)
        os.replace(tmp, p)

    put(path, json.dumps(rec, indent=2, default=str) + "\n")
    if token_path is not None:
        put(token_path, token + "\n")
    return rec


def end_session(path, stop) -> dict | None:
    """Mark the session file ended (the URL and token are dead now), keeping every other key."""
    try:
        rec = json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return None
    rec.update(ended_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), stop=stop)
    return write_session(path, rec.pop("url"), rec.pop("token"), rec.pop("flags", None), extra=rec)


def cost_estimate(seconds: int, region_mult: float, timeout_s: int = FUNCTION_TIMEOUT_S) -> dict:
    rate = (RATE_USD_H + CPU_MEM_USD_H) * region_mult
    return {"rate_usd_h": round(rate, 2), "expected_usd_full_window": round((BOOT_EST_S + seconds) / 3600 * rate, 2),
            "worst_usd": round(timeout_s / 3600 * rate, 2),
            "note": "[E] the window ends earlier on POST /shutdown or --idle; GPU queue time is not billed"}


# ------------------------------------------------------------------ Modal app

if modal is not None:
    if modal.is_local():
        if str(HERE) not in sys.path:
            sys.path.insert(0, str(HERE))
        import modal_direct_host as core  # read-only: PINNED35 (checked against modal_od.py on import)
        _PINS = list(core.PINNED35)
        for _f in [LEAN / n for n in LEAN_FILES] + [HERE / "fastcore" / "readout.py"]:
            if not _f.exists():
                raise SystemExit(f"missing {_f}")
    else:  # in the container the built image is used; the pin list is not needed there
        core, _PINS = None, []

    image = (
        modal.Image.from_registry(SGLANG_IMAGE)
        .run_commands(f"PIP_BREAK_SYSTEM_PACKAGES=1 python3 -m pip install --no-cache-dir {UV_PIN}",
                      "uv venv --python 3.12.10 /opt/fastpath",
                      f"uv pip install --no-cache --python {FASTPATH_PY} {' '.join(_PINS)}")
        .env({"HF_HOME": "/tmp/hf", "HF_HUB_ENABLE_HF_TRANSFER": "0", "TOKENIZERS_PARALLELISM": "false",
              "HF_HUB_OFFLINE": "1"})  # local model + tokenizer paths only; the Volume is mounted read-only
    )
    for _n in LEAN_FILES:
        image = image.add_local_file(LEAN / _n, f"{REMOTE_LEAN}/{_n}")
    image = (image.add_local_dir(HERE / "fastcore", f"{REMOTE_HOSTING}/fastcore", ignore=["**/__pycache__/**", "**/*.pyc"])
             .add_local_file(HERE / "sglang_host.py", f"{REMOTE_HOSTING}/sglang_host.py"))
    app = modal.App(APP_NAME)
    vol = modal.Volume.from_name("opendecide").read_only()  # the account Volume; never written by this app

    @app.function(image=image, gpu=GPU, cpu=4.0, memory=32768, volumes={"/vol": vol}, timeout=FUNCTION_TIMEOUT_S,
                  max_containers=1)
    def serve(q: modal.Queue, token: str, seconds: int = 1500, idle_s: int = 300, fp8: bool = False,
              merged: str = MERGED_NAME, server: dict | None = None, probe_sha256: str | None = None) -> dict:
        """SGLang + the API v1 front end on this H100, published through modal.forward(PORT). Returns when the front
        end stops (POST /shutdown, --seconds, --idle) or SGLang dies."""
        t0 = time.time()
        srv = {**SERVER_DEFAULTS, **(server or {})}
        info = {"app": APP_NAME, "arm": "S2" if fp8 else "S1", "model": C1_MODEL, "merged": merged, "base": BASE,
                "revision": REVISION, "region": os.environ.get("MODAL_REGION"),
                "cloud": os.environ.get("MODAL_CLOUD_PROVIDER"), "gpu": gpu_name(),
                "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        ver = subprocess.run([sys.executable, "-c", "import sglang; print(sglang.__version__)"], capture_output=True,
                             text=True, timeout=600).stdout.strip()  # B1a's check, without importing sglang here
        if ver != SGLANG_VERSION:
            raise SystemExit(f"sglang {ver or '(import failed)'} != pinned {SGLANG_VERSION}")
        info["sglang"] = {"version": ver, "python": sys.executable}
        mdir = Path("/vol/models") / merged
        man, problems = check_manifest(mdir)
        if problems:
            raise SystemExit(f"{mdir}: " + "; ".join(problems))
        info["adapter_sha256"] = man["adapter_sha256"]
        info["manifest"] = {k: man.get(k) for k in ("layout", "created_utc", "merge", "config")}
        hashed = {}
        hasher = threading.Thread(target=lambda: hashed.update(problems=verify_files(mdir, man)), daemon=True)
        hasher.start()  # re-hash the checkpoint while SGLang reads it (same immutable files)
        cmd = server_cmd(str(mdir), fp8=fp8, max_running_requests=srv["max_running_requests"],
                         max_mamba_cache_size=srv["max_mamba_cache_size"],
                         mem_fraction_static=srv["mem_fraction_static"], chunked_prefill_size=srv["chunked_prefill_size"],
                         python=sys.executable)
        info["sglang_cmd"] = shlex.join(cmd)
        print("SGLANG_CMD " + info["sglang_cmd"], flush=True)
        sgl_tail, fe_tail = deque(maxlen=400), deque(maxlen=400)
        sgl = subprocess.Popen(cmd, env=server_env(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                               start_new_session=True)
        pump(sgl, sgl_tail, "[sglang]")
        fe, reason, done = None, None, None
        sgl_url = f"http://127.0.0.1:{SGL_PORT}"
        fe_dir = Path("/tmp/od_frontend")
        fe_dir.mkdir(parents=True, exist_ok=True)
        ready_f, done_f = fe_dir / "ready.json", fe_dir / "done.json"
        try:
            info["sglang_ready_s"] = wait_http_ready(sgl_url, sgl, BOOT_BUDGET_S, sgl_tail)
            sclient = SGLangClient(sgl_url)
            resolved = sclient.server_info()
            sclient.close()
            print("SERVER_ARGS " + json.dumps(resolved, default=str), flush=True)
            info["server_args"] = args_subset(resolved)
            bad, warn = check_server_args(resolved, want_server_args(mdir, fp8, srv))
            info["server_args_warnings"] = warn
            if bad:
                raise SystemExit("SGLang resolved args refused: " + "; ".join(bad))
            hasher.join(timeout=max(1.0, BOOT_BUDGET_S - (time.time() - t0)))
            if hasher.is_alive() or hashed.get("problems"):
                raise SystemExit(f"merged checkpoint differs from its manifest: {hashed.get('problems') or 'timeout'}")
            info["files_verified"] = len(man["files"])
            host_info = {k: info[k] for k in ("model", "merged", "adapter_sha256", "base", "revision", "gpu", "region",
                                              "cloud", "arm")}
            host_info["boot"] = {"sglang_cmd": info["sglang_cmd"], "sglang_ready_s": info["sglang_ready_s"],
                                 "server_args_warnings": warn, "files_verified": info["files_verified"],
                                 "manifest": info["manifest"]}
            cfg = {"sglang_url": sgl_url, "c1_tokenizer_dir": str(mdir / C1_TOKENIZER_SUBDIR), "port": PORT,
                   "seconds": seconds, "idle_s": idle_s, "quantization": "fp8" if fp8 else None,
                   "server_args": resolved, "host_info": host_info, "probe_sha256": probe_sha256,
                   "ready_file": str(ready_f), "done_file": str(done_f), "t0": t0}
            (fe_dir / "config.json").write_text(json.dumps(cfg, default=str))
            fe_env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "VIRTUAL_ENV")}
            fe_env.update({"OD_SGL_TOKEN": token, "TOKENIZERS_PARALLELISM": "false", "HF_HUB_OFFLINE": "1"})
            fe = subprocess.Popen([FASTPATH_PY, f"{REMOTE_HOSTING}/sglang_host.py", "frontend", "--config",
                                   str(fe_dir / "config.json")], env=fe_env, cwd=REMOTE_HOSTING,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, start_new_session=True)
            pump(fe, fe_tail, "[front]")
            t_fe = time.time()
            while not ready_f.exists():
                if fe.poll() is not None or sgl.poll() is not None:
                    raise RuntimeError("front end or SGLang exited during the front-end boot:\n" +
                                       "\n".join(list(fe_tail)[-30:] + list(sgl_tail)[-10:]))
                if time.time() - t_fe > 600:
                    raise RuntimeError("front end not ready after 600 s")
                time.sleep(1)
            ready = json.loads(ready_f.read_text())
            if not ready.get("ok"):
                raise RuntimeError(f"front end boot failed: {ready.get('error')}")
            info["boot_s"] = round(time.time() - t0, 1)
            print("BOOT " + json.dumps({**info, "frontend": ready["health"].get("boot")}, default=str)[:20000],
                  flush=True)
            with modal.forward(PORT) as tunnel:
                q.put({"url": tunnel.url, "health": ready["health"]})
                while True:  # the front end owns /shutdown, --seconds and --idle; a dead SGLang ends the session
                    if fe.poll() is not None:
                        reason = "front end stopped"
                        break
                    if sgl.poll() is not None:
                        reason = f"SGLang exited ({sgl.returncode})"
                        break
                    time.sleep(2)
        finally:
            stop_process(fe, grace=20.0)
            stop_process(sgl, grace=30.0)
        if done_f.exists():
            done = json.loads(done_f.read_text())
        out = {"info": info, "stop": (done or {}).get("stop") or reason, "frontend": done,
               "sglang_tail": list(sgl_tail)[-60:], "frontend_tail": list(fe_tail)[-30:],
               "wall_s": round(time.time() - t0, 1)}
        print("DONE " + json.dumps({k: out[k] for k in ("stop", "wall_s")}), flush=True)
        return out

    # -------------------------------------------------------------- local entrypoint (the laptop)

    def _local_probe() -> str | None:
        """probe_digest with the local C1 tokenizer backup (same files and tokenizers version as the container)."""
        backup = LEAN.parent.parent / "backups" / "modal_models" / C1_MODEL
        if not (backup / "tokenizer.json").exists():
            print(f"no local C1 tokenizer at {backup}: the container's probe ids are not cross-checked", flush=True)
            return None
        tok, ro, _ = load_c1_tokenizer(backup)
        return probe_digest(ro, tok)["sha256"]

    def _smoke(url, token, n: int, seed: int = 0) -> dict:
        """n dev rows (split "dev") sent one by one; answers vs the stored L4 served reads (2view): argmax + |dp|."""
        import random
        import client_bench as cb
        R = _readout()
        def jl(p):
            with open(p) as f:
                return [json.loads(x) for x in f if x.strip()]
        rows = {r["id"]: r for r in jl(LEAN / "data" / "dev.jsonl")}  # gate split "dev" (never an OHS split)
        ref = {o["id"]: o["probs"] for o in jl(LEAN / "preds_dev" / f"{C1_MODEL}_pre_served.jsonl")}
        ids = sorted(set(rows) & set(ref))
        pick = random.Random(seed).sample(ids, min(n, len(ids)))
        c, pairs, errors = cb.Ours(url, token, timeout=120.0), [], []
        try:
            for i in pick:
                r = rows[i]
                d, ms, err = c.decide(R.request_from_row(r))
                if err:
                    errors.append(err)
                pairs.append((r["qtype"], r.get("options"), ref[i], (d or {}).get("answers", {}).get("q0")))
        finally:
            c.close()
        return {**smoke_compare(pairs), "errors": errors[:5], "n_errors": len(errors)}

    @app.local_entrypoint()
    def main(fp8: bool = False, region: str = "any", hold: bool = False, seconds: int = 1500, idle: int = 300,
             merged: str = MERGED_NAME, mrr: int = 64, mamba_cache: int = 400, mem_fraction: float = 0.0,
             chunked_prefill: int = 0, smoke: int = 24, boot_wait: int = 1800, max_usd: float = 6.0, session: str = ""):
        """Boot S1 (or S2 with --fp8), smoke-check it against the stored L4 reads, then shut down, or with --hold keep
        it up for hosting/speed_bench.py (speed/session_url.json + speed/session_token.txt)."""
        prof = payer_guard()
        import client_bench as cb
        reg, mult = core._region_opt(region)
        if seconds + BOOT_BUDGET_S > FUNCTION_TIMEOUT_S:
            raise SystemExit(f"--seconds must be <= {FUNCTION_TIMEOUT_S - BOOT_BUDGET_S} (boot + serving must fit the "
                             f"{FUNCTION_TIMEOUT_S // 60} min timeout)")
        est = cost_estimate(seconds, mult)
        print(f"payer {prof}; cost estimate {json.dumps(est)}", flush=True)
        if est["worst_usd"] > max_usd:
            raise SystemExit(f"worst case ${est['worst_usd']} > --max-usd {max_usd}: refusing")
        probe = _local_probe()
        token = secrets.token_urlsafe(24)
        server = {"max_running_requests": mrr, "max_mamba_cache_size": mamba_cache,
                  "mem_fraction_static": mem_fraction or None, "chunked_prefill_size": chunked_prefill or None}
        boot = "sglang_fp8" if fp8 else "sglang_bf16"
        arm = "S2" if fp8 else "S1"
        session = session or f"speed2_{time.strftime('%Y%m%d', time.gmtime())}"
        speed = LEAN / "speed"
        speed.mkdir(parents=True, exist_ok=True)
        sess_f, tok_f = speed / "session_url.json", speed / "session_token.txt"  # = hosting/fast_host.py's
        t0 = time.time()
        res, sm, url = None, None, None
        with modal.Queue.ephemeral() as q:
            call = serve.with_options(gpu=GPU, **({"region": reg} if reg else {})).spawn(
                q, token, seconds, idle, fp8, merged, server, probe)
            try:
                msg = core._wait_url(q, call, boot_wait, f"SGLang host {arm} ({region})")
            except BaseException:  # no URL (boot failed, --boot-wait passed, Ctrl-C): never leave the H100 running
                call.cancel()
                raise
            url, health = msg["url"], msg["health"]
            bench = (f"../.venv/bin/python hosting/speed_bench.py ab --url {url} --token-file "
                     f"{os.path.relpath(tok_f, LEAN)} --session {session} --arms {arm} --shutdown-after --go")
            write_session(sess_f, url, token, health.get("flags"), token_path=tok_f,
                          extra={"payer": prof, "app": APP_NAME, "region": region, "fp8": fp8, "arm": arm,
                                 "engine": "sglang", "boot": boot, "session": session,
                                 "adapter_sha256": health.get("adapter_sha256"),
                                 "config_sha256": health.get("config_sha256"), "health_ok": health.get("ok"),
                                 "serve_s": seconds, "speed_bench": bench})
            print(f"wrote {sess_f} and {tok_f} (mode 0600)", flush=True)
            print(f"server up after {time.time() - t0:.0f} s: {url}\nhealth: {json.dumps(msg['health'])[:3000]}",
                  flush=True)
            try:
                cb.wait_ready(url, token)
                if smoke:
                    sm = _smoke(url, token, smoke)
                    print("SMOKE vs stored L4 served reads: " + json.dumps(sm), flush=True)
                    if hold and (sm["argmax_agree"] is None or sm["argmax_agree"] < SMOKE_MIN_AGREE or sm["n_errors"]):
                        print(f"SMOKE FAILED (agreement < {SMOKE_MIN_AGREE} or errors): not holding", flush=True)
                        hold = False
                if hold:
                    print(f"\nHOLD: serving for up to {seconds} s (idle stop {idle} s). From another terminal (lean/):"
                          f"\n  {bench}\nCtrl-C here (or POST /shutdown) stops the GPU.", flush=True)
                    while True:
                        try:
                            call.get(timeout=30)
                            break
                        except (modal.exception.TimeoutError, TimeoutError):
                            continue
            except KeyboardInterrupt:
                print("interrupted: shutting the server down", flush=True)
            finally:  # whatever happened above: stop the GPU, then mark the session ended
                res = core._finish(call, cb, url, token)
                end_session(sess_f, (res or {}).get("stop"))
        wall_h = (time.time() - t0) / 3600
        cost = {"wall_min_spawn_to_end": round(wall_h * 60, 1), "est_usd_upper": round(wall_h * est["rate_usd_h"], 2),
                "rate_usd_h": est["rate_usd_h"], "note": "upper bound: GPU queue time is not billed"}
        out_f = speed / f"sglang_{boot}_{time.strftime('%Y%m%d_%H%M%S', time.gmtime())}.json"
        _write_json(out_f, {"server": res, "smoke": sm, "cost_estimate": cost, "session": session})
        print(json.dumps({"cost_estimate": cost, "stop": (res or {}).get("stop"), "smoke": sm,
                          "frontend_stats": ((res or {}).get("frontend") or {}).get("stats")}, indent=2, default=str))
        print(f"wrote {out_f}")


if __name__ == "__main__":
    sys.exit(frontend_main())
