"""od-fast-host: C1 (q35_4b_main500k, merged BF16; --fp8 for arm A3) on ONE H100 behind API v1 (SPEED1_DESIGN.md),
served by the SPEED-1 fast path (hosting/fastcore): tokenization on the HTTP threads, ONE GPU worker
(fastcore.BatchingEngine) with runtime flags for arms A0-A3, the SPEED-1 CUDA-graph plan in one shared pool (self-check,
private-pool fallback), reached through a direct Modal tunnel (modal.forward) exactly like modal_direct_host.py (core).
NEW file: core, client_bench, decoder_io, prism_x and writeblock are imported read-only; the Volume is mounted
read-only.

Boot (in the container): read-only inputs as core.boot_gpu (Triton cache copied to /tmp, base snapshot read offline
from /vol/hf) -> adapter sha256 == pin (else refuse) -> load + merge_and_unload (fastcore.engine.load_merged = core's
load + merge) -> [--fp8: fastcore.fp8.quantize_model] -> FastEngine.boot (eager warm-up of every shape, shared-pool
capture largest first, self-check, private fallback, eager warm-up to 8192 tokens, warm requests) -> startup parity
self-test (built-in requests: graph paths of A0/A1/A2 vs an eager-only pass through the same BatchingEngine; /health
"ok" is false if it fails, and the launcher then stops the GPU). A device-side assert during a shared-pool boot kills
the CUDA context: the container reports it and exits (single-use), and the launcher reboots once with --pool private
(only when the failed boot took <= BOOT_BUDGET_S). While serving, a CUDA-fatal forward error stops the engine worker
(fastcore.batcher): /decide answers 503, /health reads ok=false with the problem, and the serving watchdog ends the
container at once; a forward stuck > 120 s reads ok=false, > STALL_STOP_S ends the container.

API v1 (Bearer token on every route): POST /decide, GET /health (+ serve_deadline_unix / serve_deadline_utc /
serve_remaining_s once the tunnel is open), POST /admin/config {"flags": {...}} (returns the new /health),
POST /admin/flush (no-op: no prefix cache), POST /shutdown, GET /ping. 400 bad request, 401 auth, 404, 413 body too
large, 503 engine closed or dead, 504 timeout, 500 server error.

Commands, run from lean/ ONLY after the owner's GO (nothing here has run on Modal yet). Payer: free credit on
mahadikarya3 (fallback mahadikarya2); every other profile, an unset MODAL_PROFILE, or MODAL_TOKEN_ID/SECRET in the
environment is REFUSED before anything starts:
  0) free CPU test:   ../.venv/bin/python -m pytest hosting/tests/test_fast_host_local.py -q
  1) adapter, once per profile (free, volume only):   bash hosting/upload_c1_adapter.sh mahadikarya3
  2) OPTIONAL smoke (boot, parity self-test, 3 rounds of built-in requests over the tunnel, shutdown; the hold launch
     in 3 runs the same boot checks and stops at once if /health is not ok, so skip this to save ~$0.8):
       MODAL_PROFILE=mahadikarya3 ../.venv/bin/modal run hosting/fast_host.py::main
  3) SPEED-2 session, BF16 boot (arms A0, A2, A1 switched with /admin/config; A2, the main arm, runs before A1 so a
     short window cuts the least important arm):
       MODAL_PROFILE=mahadikarya3 ../.venv/bin/modal run hosting/fast_host.py::main --hold
     then from a second terminal (the URL and token are in speed/session_url.json and speed/session_token.txt):
       ../.venv/bin/python hosting/speed_bench.py ab --url URL --token-file speed/session_token.txt --session NAME \
           --arms A0,A2,A1 --shutdown-after --go
     speed_bench refuses an arm that does not fit the remaining window (/health serve_remaining_s, at 40 ms/call),
     aborts an arm on a run of failed calls, and with --shutdown-after POSTs /shutdown when it ends (no idle tail).
  4) A3 = its own boot: --fp8 --hold --seconds 1200, then speed_bench ... --arms A3 --shutdown-after --go.
  Options: --region any (default; "us-east" = x1.75 and needs --max-usd >= ~9.7), --seconds (serving window; default
  300 for a smoke, MAX_SECONDS = 43.5 min with --hold), --idle (default 120 s after the last POST; FIRST_IDLE_S = 300 s
  before the first one), --max-usd (default 6: refuse a launch whose worst case is higher), --arm (initial flags,
  default A2 / A3 with --fp8), --pool private (skip the shared pool), --boot-cfg '{"coverage": {"1": 2048}, ...}'
  (FastEngine.boot overrides), --boot-wait (default 1500 s).
Never pass --detach: the laptop holds the run, and Ctrl-C (or POST /shutdown) stops the H100.

Cost (H100 base $3.95/h, `modal billing rates` 12 Oct, + ~$0.22/h for 2 cores and 16 GiB; region multiplier us-east
1.75 = core.REGION_MULT "narrow", to be confirmed on Modal's billing page; "any" 1.0): $4.17/h with --region any,
about $7.30/h in us-east. Boot is expected at 8-12 min (load ~2, warm-up + ~130 graphs + self-checks + eager warm-up).
Each launch's function timeout = BOOT_BUDGET_S (15 min) + --seconds + 90 s, at most FUNCTION_TIMEOUT_S (60 min); the
worst case checked against --max-usd = that timeout + 2 min container start + (shared pool) one failed boot of up to
17 min.
SPEED-2 session budget (runbook; expected = boot + work, with --shutdown-after; any / us-east; worst case at any):
  2) HF smoke, optional:       11-13 min   $0.8-0.9   / $1.3-1.6    worst $2.8
  3) HF hold A0,A2,A1:         36-49 min   $2.5-3.4   / $4.4-6.0    worst $5.5   (bench 25-36 min at 20-40 ms/call)
  4) HF hold A3 (--seconds 1200): 18-24 min $1.3-1.7  / $2.2-2.9    worst $3.9
  export_c1_merged (CPU, once): $0.15-0.25;  SGLang S1 boot test, optional: 6-8 min $0.4-0.6 / $0.7-1.0
  SGLang S1 hold, S2 hold (hosting/sglang_host.py --hold): 14-21 min each  $1.0-1.5 / $1.7-2.6 each  worst $2.8 each
  TOTAL: required runs (3, 4, export, S1, S2) $5.9-8.3 at any, $7.0-9.7 with both optional runs; at us-east
  $10.2-14.3 required, up to $16.8 with the optional runs (over a ~$10 budget: us-east is opt-in and needs --max-usd).
  A private-pool reboot adds one boot (~$0.8 any). Without --shutdown-after each hold adds its idle tail (120 s).
Cost guards: one container (max_containers=1, single_use_containers: it exits after its one call, no idle billing),
the read-only Volume, the --max-usd worst-case refusal before anything is spawned, the per-launch function timeout
(hard cap), and the server stops on POST /shutdown, at the end of its serving window (--seconds, clamped so boot +
serving fits the timeout), after --idle seconds without a POST, or when the watchdog sees a dead engine (CUDA-fatal
error) or a forward stuck > STALL_STOP_S. The launcher shuts down at once if /health is not ok. The token stays on this
laptop (speed/, mode 0600).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import secrets
import shutil
import sys
import threading
import time
import traceback
from collections import Counter
from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent  # lean/hosting locally; /root in the container
LEAN = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import modal_direct_host as core  # noqa: E402  (read-only: image, sha256_file, base_snapshot_complete, wait_loop, ...)

APP_NAME = "od-fast-host"
MODEL = "q35_4b_main500k"  # C1
ADAPTER_SHA256 = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"  # adapter_model.safetensors
BASE, REVISION = core.BASE, core.REVISION
EXPECT_LAYOUT = ("schema_branch_mark", "cygnet")  # C1's train_meta.json (layout E, style cygnet)
REMOTE_LEAN = core.REMOTE_LEAN
LEAN_FILES = core.LEAN_FILES
VOL_MODELS = Path("/vol/models")
GPU = "H100!"
PORT = 8000
MAX_BODY = 4 << 20
DECIDE_TIMEOUT_S = 120.0
FUNCTION_TIMEOUT_S = 60 * 60  # the decorator's hard cap; each launch passes its own, shorter one (launch_timeout)
BOOT_BUDGET_S = 15 * 60  # reserved for the boot in each launch's timeout
SHUTDOWN_MARGIN_S = 90  # serving ends this long before the function timeout (clean return, DONE log)
MAX_SECONDS = FUNCTION_TIMEOUT_S - BOOT_BUDGET_S - SHUTDOWN_MARGIN_S  # 2610 s: A0+A2+A1 at 40 ms/call is ~35.5 min
DEFAULT_SECONDS = MAX_SECONDS  # --hold; a smoke serves SMOKE_SECONDS
SMOKE_SECONDS = 300
DEFAULT_IDLE_S = 120  # after the last POST
FIRST_IDLE_S = 300  # before the first POST (speed_bench is started by hand from a second terminal)
STALL_STOP_S = 300  # the serving watchdog ends the container when one forward has run this long (a hung GPU)
CONTAINER_START_S = 120  # billed container start-up outside the function timeout (worst-case allowance per spawn)
DEFAULT_MAX_USD = 6.0
HOLD_ARMS = "A0,A2,A1"  # the BF16 hold's speed_bench order: the main arm (A2) before A1
BOOT_EST_MIN = 12  # expected boot (minutes) for the printed estimate
PAYER_PROFILES = ("mahadikarya3", "mahadikarya2")  # free credit only (SPEED1_DESIGN.md "Money")
RATE_USD_H = 3.95  # Modal H100 base rate (`modal billing rates`, 12 Oct)
CPU_MEM_USD_H = 0.22  # 2 reserved cores + 16 GiB (core.GPU_RATE_USD_H comment)
REGION_MULT = core.REGION_MULT  # any 1.0, broad 1.15, narrow (us-east) 1.75; to be confirmed on Modal's billing page
ARMS_FILE = HERE / "speed_arms.json"  # the only place arms (flag sets) are defined
SESSION_FILE = LEAN / "speed" / "session_url.json"
TOKEN_FILE = LEAN / "speed" / "session_token.txt"  # the plain token, for speed_bench --token-file
# Startup parity gate: max |p_graph - p_eager| per answer probability. It is a CORRUPTION gate (a bad shared pool gives
# garbage or NaN), not the parity bar (SPEED-2's job): graph vs masked eager differ in bf16 by the sdpa kernel (mask /
# no mask) and batched GEMMs, a few 1e-3 expected, so it is looser than FastGraphs.selfcheck's 0.02 on identical inputs.
SELFTEST_TOL = 0.05
BOOT_DEFAULTS = {"graphs": True, "coverage": None, "legacy_shapes": True, "reserve_gb": 6.0, "tol_prob": 0.02,
                 "eager_warmup": None, "warm_requests": 3, "selftest": True, "selftest_tol": SELFTEST_TOL,
                 "decide_timeout_s": DECIDE_TIMEOUT_S}

# ------------------------------------------------------------------ payer guard (runs before anything billable)


def payer_guard(env=None, resolved: str | None = None) -> str:
    """The Modal profile this launch bills, or SystemExit. MODAL_PROFILE must be set to an allowed free-credit profile
    (never aryamhd / jaypatil-duke / anything else); MODAL_TOKEN_ID / MODAL_TOKEN_SECRET must not be set (they override
    the profile); `resolved` (modal.config's resolved profile, when known) must agree with MODAL_PROFILE."""
    env = os.environ if env is None else env
    p = env.get("MODAL_PROFILE")
    if p is None or not p.strip():
        raise SystemExit("REFUSED: MODAL_PROFILE is unset; run with MODAL_PROFILE=mahadikarya3 (fallback mahadikarya2)")
    if p not in PAYER_PROFILES:
        raise SystemExit(f"REFUSED: profile {p!r}: the fast host runs on free credit only "
                         f"({', '.join(PAYER_PROFILES)}); never aryamhd / jaypatil-duke")
    for k in ("MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET"):
        if env.get(k):
            raise SystemExit(f"REFUSED: {k} is set in the environment and would override profile {p!r}; unset it")
    if resolved is not None and resolved != p:
        raise SystemExit(f"REFUSED: modal resolved profile {resolved!r} but MODAL_PROFILE is {p!r}")
    return p


def _cli_launch(argv0: str | None = None) -> bool:
    """True when this module is being loaded by the `modal` CLI (run / deploy / serve / shell)."""
    a = Path(argv0 if argv0 is not None else (sys.argv[0] if sys.argv else ""))
    return a.name == "modal" or a.parent.name == "modal"


if modal.is_local():
    if _cli_launch():  # also covers `modal run hosting/fast_host.py::serve` and `modal deploy`, which skip main()
        payer_guard(os.environ, getattr(modal.config, "_profile", None))
    for _f in [HERE / "fastcore" / n for n in ("__init__.py", "readout.py", "graphs.py", "batcher.py", "fp8.py",
                                                "engine.py")] + [ARMS_FILE]:
        if not _f.exists():
            raise SystemExit(f"missing {_f}")

# core.image = debian_slim 3.12.10 + PINNED35 (checked against modal_od.py by core) + decoder_io/prism_x/writeblock at
# /root/lean; plus core itself and the fastcore package at /root (this file is mounted there as the entrypoint)
image = core.image.add_local_python_source("modal_direct_host", "fastcore")
app = modal.App(APP_NAME)
vol = modal.Volume.from_name("opendecide").with_mount_options(read_only=True)  # never written


# ------------------------------------------------------------------ serving core (CPU-testable, no Modal needed)

def fastcore_import():
    """The fastcore package (hosting/fastcore locally, /root/fastcore in the container). Imported lazily: it imports
    torch and decoder_io, which must happen after the container's environment is set (Triton cache, HF offline)."""
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import fastcore
    import fastcore.fp8  # noqa: F401  (A3)
    return fastcore


def code_shas() -> dict:
    """sha256 of the code that serves: fastcore/*.py, this file, core, and the read-only lean files."""
    fc = fastcore_import()
    out = {f"fastcore/{p.name}": core.sha256_file(p) for p in sorted(Path(fc.__file__).parent.glob("*.py"))}
    out["fast_host.py"] = core.sha256_file(Path(__file__))
    out["modal_direct_host.py"] = core.sha256_file(Path(core.__file__))
    lean = Path(REMOTE_LEAN) if Path(REMOTE_LEAN, "decoder_io.py").exists() else LEAN
    for n in LEAN_FILES:
        out[n] = core.sha256_file(lean / n)
    return out


def config_sha256(flags: dict, adapter_sha: str | None, code: dict, engine_sha: str | None = None) -> str:
    """The host's /health config_sha256: sha256 of the canonical JSON of the set flags (canonical names), the adapter
    sha256, the code shas, and the engine's own config sha (readout, temps, quantization, captured graph shapes)."""
    blob = json.dumps({"flags": flags, "adapter_sha256": adapter_sha, "code_sha256": code,
                       "engine_config_sha256": engine_sha}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()


_FILLER = ("The office opens at nine and closes at five on weekdays. Payments are due on the first day of the month, "
           "and a late payment carries a small fee unless the customer asked for more time in writing. ")
# Built-in requests for the startup parity self-test and the smoke run (no task data): short and long, noul and
# choice, a definitions card, 30 options (two-letter labels after Z), several questions in one request.
SELFTEST_REQUESTS = [
    {**core.EXAMPLE, "id": "selftest-example"},
    {"id": "selftest-card", "state": "Ticket:\nI was charged twice for the same order last night and I want one of "
                                     "the two charges refunded today.",
     "questions": {
         "intent": {"type": "choice", "instructions": "Which intent fits this ticket?",
                    "options": ["duplicate charge", "refund status", "cancel order", "wrong item", "other"],
                    "card": "- duplicate charge: the customer was billed more than once for one purchase\n"
                            "- refund status: the customer asks where an already promised refund is\n"
                            "- cancel order: the customer wants to stop an order before it ships\n"
                            "- wrong item: the customer received something they did not order\n"
                            "- other: none of the above"},
         "urgent": {"type": "noul", "instructions": "Does the customer ask for action today?",
                    "card": "- yes: the text sets a deadline of today or says it is urgent"}}},
    {"id": "selftest-wide", "state": "Note:\nThe meeting moved to the river room; bring the topic 17 slides.",
     "questions": {"topic": {"type": "choice", "instructions": "Which topic number does the note mention?",
                             "options": [f"topic {i}" for i in range(1, 31)]}}},
    {"id": "selftest-long",
     "state": "Policy text:\n" + _FILLER * 40 + "\nCustomer: I paid on the third. Is there a fee?",
     "questions": {"fee": {"type": "noul", "instructions": "Does the policy say a late payment carries a fee?"}}},
    {"id": "selftest-multi", "state": "Review:\nThe hotel room was clean and quiet, but breakfast ended at nine and "
                                      "the staff would not keep it open for late guests.",
     "questions": {
         "q0": {"type": "noul", "instructions": "Is the review about a hotel?"},
         "q1": {"type": "choice", "instructions": "What is the overall sentiment?",
                "options": ["positive", "negative", "mixed"]},
         "q2": {"type": "noul", "instructions": "Does the reviewer complain about the staff?"},
         "q3": {"type": "choice", "instructions": "Which aspect is praised?",
                "options": ["room", "breakfast", "staff", "price"]}}},
]


class _EagerView:
    """The runner the batcher sees during the self-test's reference pass: never selects a graph, so every forward is
    the eager path (= decoder_io.cand_logits' eager path) on the same model."""

    def __init__(self, runner):
        self.runner = runner

    def select(self, k, m, legacy=False, token_budget=None):
        return None

    def run(self, seqs, cands, shape=None, readout="exact"):
        return self.runner.run(seqs, cands, None, readout=readout)


def answer_probs(a: dict) -> dict:
    return {"yes": a["probabilities"]["yes"], "no": a["probabilities"]["no"]} if a["type"] == "noul" \
        else dict(a["probabilities"])


def parity_selftest(eng, requests=None, tol: float = SELFTEST_TOL, arms=("A0", "A1", "A2"), log=print) -> dict:
    """Startup parity: the built-in requests through the engine under each arm's flags (graph paths where captured)
    vs one eager-only pass (A1 flags, every view its own eager forward), all through the engine's own BatchingEngine.
    ok = every answer probability within `tol` and finite. Boot only: the engine must be idle; flags are restored."""
    fc = fastcore_import()
    reqs = SELFTEST_REQUESTS if requests is None else requests
    b = eng.batcher
    qd = b.queued()
    if qd["requests"] or qd["busy"]:
        raise RuntimeError("parity_selftest: the engine is busy (boot-time check only)")
    t0, keep, real = time.time(), b.flags, b.runner
    b.runner = _EagerView(real)
    try:
        b.set_flags({**fc.ARM_FLAGS["A1"], "choice_views": 2})
        ref = [eng.decide(r) for r in reqs]
    finally:
        b.runner = real
    worst, flips, bad, nonfinite, fwd = 0.0, 0, [], 0, {}
    try:
        for arm in arms:
            b.set_flags({**fc.ARM_FLAGS[arm], "choice_views": 2})
            cnt = Counter()
            for r, ro in zip(reqs, ref):
                out = eng.decide(r)
                cnt.update("eager" if s[0] == "eager" else "graph" for s in out["shapes"])
                for name, a in out["answers"].items():
                    p, q = answer_probs(a), answer_probs(ro["answers"][name])
                    if all(math.isfinite(v) for v in p.values()):
                        d = max(abs(p[k] - q[k]) for k in q)
                    else:
                        d, nonfinite = float("inf"), nonfinite + 1
                    worst = max(worst, d)
                    flips += max(p, key=p.get) != max(q, key=q.get)
                    if not d <= tol:
                        bad.append({"arm": arm, "request": r.get("id"), "question": name, "max_prob_diff": d})
            fwd[arm] = dict(cnt)
    finally:
        b.set_flags(keep)
    rep = {"ok": not bad and nonfinite == 0, "worst_max_prob_diff": worst, "tol_prob": tol, "argmax_flips": flips,
           "failures": bad[:10], "n_failures": len(bad), "forwards_by_arm": fwd,
           "graph_forwards": sum(v.get("graph", 0) for v in fwd.values()), "requests": len(reqs),
           "selftest_s": round(time.time() - t0, 2)}
    log(f"fast_host parity self-test: ok={rep['ok']} worst={worst:.3g} flips={flips} forwards={fwd}")
    return rep


def normalize_boot_cfg(cfg: dict | None) -> dict:
    """BOOT_DEFAULTS updated with cfg (unknown keys refused; JSON's string coverage keys made int)."""
    cfg = dict(cfg or {})
    unknown = set(cfg) - set(BOOT_DEFAULTS)
    if unknown:
        raise ValueError(f"unknown boot option(s) {sorted(unknown)} (known: {sorted(BOOT_DEFAULTS)})")
    out = {**BOOT_DEFAULTS, **cfg}
    if out["coverage"] is not None:
        out["coverage"] = {int(k): int(v) for k, v in out["coverage"].items()}
    return out


def boot_engine(model, tok, device=None, fp8: bool = False, flags: dict | None = None, pool: str = "shared",
                boot_cfg: dict | None = None, ro=None, emulate_graphs=None, log=print, expect_layout=EXPECT_LAYOUT):
    """A loaded, merged model -> (FastEngine, boot report): [fp8 quantize] -> FastEngine (layout guard) -> eng.boot
    (warm-up, shared-pool graphs, self-check, fallback, eager warm-up, warm requests) -> parity self-test."""
    fc = fastcore_import()
    cfg = normalize_boot_cfg(boot_cfg)
    rep = {"pool_requested": pool, "fp8": None, "boot_cfg": {k: v for k, v in cfg.items() if k != "coverage"},
           "coverage": None if cfg["coverage"] is None else {str(k): v for k, v in cfg["coverage"].items()}}
    if fp8:  # after the merge, before warm-up and capture
        t = time.time()
        qr = fc.fp8.quantize_model(model)
        kept = qr.pop("kept_linear")
        rep["fp8"] = {**qr, "kept_linear_n": len(kept), "kept_linear_text": [n for n in kept if "visual" not in n][:60],
                      "quantize_s": round(time.time() - t, 2)}
    eng = fc.FastEngine(model, tok, device=device, flags=flags, ro=ro, emulate_graphs=emulate_graphs,
                        quantization="fp8" if fp8 else None, log=log, expect_layout=expect_layout)
    try:
        rep["engine"] = eng.boot(graphs=cfg["graphs"], coverage=cfg["coverage"], legacy_shapes=cfg["legacy_shapes"],
                                 reserve_gb=cfg["reserve_gb"], tol_prob=cfg["tol_prob"],
                                 eager_warmup=cfg["eager_warmup"], warm_requests=cfg["warm_requests"], pool=pool)
        rep["parity_selftest"] = parity_selftest(eng, tol=cfg["selftest_tol"], log=log) if cfg["selftest"] else \
            {"ok": False, "skipped": True}
    except BaseException:
        eng.close(timeout=5)
        raise
    return eng, rep


class FastHost:
    """What the HTTP server serves: one FastEngine plus the boot info. Thread-safe (FastEngine is)."""

    def __init__(self, eng, info: dict, decide_timeout: float = DECIDE_TIMEOUT_S, code: dict | None = None):
        self.eng, self.info, self.decide_timeout = eng, info, decide_timeout
        self.code = code_shas() if code is None else code
        self.selftest_ok = bool(((info.get("boot") or {}).get("parity_selftest") or {}).get("ok"))

    def decide(self, req) -> dict:
        return self.eng.decide(req, timeout=self.decide_timeout)

    def admin_config(self, body) -> dict:
        fc = fastcore_import()
        if not isinstance(body, dict) or set(body) != {"flags"}:
            raise fc.RequestError('the body must be {"flags": {...}}')
        self.eng.set_flags(body["flags"])  # validated, all or nothing (RequestError -> 400)
        return self.health()

    def flush(self) -> dict:
        return self.eng.flush()

    def open_window(self, serve_s: float, now: float | None = None) -> float:
        """Start the serving window (when the tunnel opens): -> its deadline (unix s), also shown in /health."""
        dl = (time.time() if now is None else now) + float(serve_s)
        self.info.update(serve_s=serve_s, serve_deadline_unix=round(dl, 3),
                         serve_deadline_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(dl)))
        return dl

    def health(self) -> dict:
        h = self.eng.health()
        flags = {k: h["flags"][k] for k in fastcore_import().FLAG_DEFAULTS}  # canonical names, same snapshot as h
        problems = list(h.get("problems") or [])  # the engine's: worker stopped / died (CUDA-fatal), forward stuck
        if not self.selftest_ok:
            problems.insert(0, "startup parity self-test failed or did not run (see boot.parity_selftest)")
        i = self.info
        dl = i.get("serve_deadline_unix")
        return {**h, "ok": bool(h.get("ok")) and not problems, "problems": problems, "app": APP_NAME,
                "config_sha256": config_sha256(flags, i.get("adapter_sha256"), self.code, h["config_sha256"]),
                "engine_config_sha256": h["config_sha256"], "model": i.get("model", MODEL),
                "adapter_sha256": i.get("adapter_sha256"), "base": i.get("base", BASE),
                "revision": i.get("revision", REVISION), "gpu": i.get("gpu"), "region": i.get("region"),
                "cloud": i.get("cloud"), "boot_s": i.get("boot_s"), "serve_s": i.get("serve_s"),
                "serve_deadline_unix": dl, "serve_deadline_utc": i.get("serve_deadline_utc"),
                "serve_remaining_s": None if dl is None else round(max(0.0, dl - time.time()), 1),
                "memory_gb": i.get("memory_gb"), "boot": i.get("boot"), "code_sha256": self.code}


def new_state() -> dict:
    """Server state: last = time of the last POST (idle timer), posts = POSTs seen, n = served /decide, errors."""
    return {"last": time.time(), "posts": 0, "n": 0, "errors": 0, "status": Counter()}


def make_fast_server(port, token, host, on_shutdown, state=None, bind="0.0.0.0", max_body=MAX_BODY):
    """Stdlib ThreadingHTTPServer (one thread per connection: prompt building + tokenization run on these threads; GPU
    work only in the engine's BatchingEngine worker). HTTP/1.1 keep-alive, TCP_NODELAY, one buffered write per response
    (as core.make_server). Every route needs "Authorization: Bearer <token>" (the tunnel URL is public).
      GET  /ping          {"ok": true}
      GET  /health        host.health() + served / errors
      POST /decide        API v1 response + "server_ms" (POST / is the same)
      POST /admin/config  {"flags": {...}} -> the new /health
      POST /admin/flush   no-op on HF
      POST /shutdown      replies, then on_shutdown()"""
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    fc = fastcore_import()
    if not isinstance(token, str) or len(token) < 16:
        raise ValueError("the bearer token must be a string of 16+ characters")
    st = state if state is not None else new_state()
    lock = threading.Lock()
    want = f"Bearer {token}".encode()

    def count(code, served=False):
        with lock:
            st["status"][code] += 1
            if served:
                st["n"] += 1
            elif code >= 400:
                st["errors"] += 1

    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        disable_nagle_algorithm = True
        wbufsize = 1 << 16
        server_version = "od-fast-host"
        sys_version = ""

        def _reply(self, code, obj, served=False):
            body = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            if self.close_connection:
                self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(body)
            count(code, served)

        def _authed(self) -> bool:
            if secrets.compare_digest((self.headers.get("Authorization") or "").encode(), want):
                return True
            self._reply(401, {"error": "unauthorized"})
            return False

        def _route(self):
            return self.path.split("?", 1)[0]

        def do_GET(self):
            if not self._authed():
                return
            p = self._route()
            if p == "/ping":
                self._reply(200, {"ok": True})
            elif p == "/health":
                with lock:
                    served, errors = st["n"], st["errors"]
                self._reply(200, {**host.health(), "served": served, "errors": errors})
            else:
                self._reply(404, {"error": "not found"})

        def _body(self):
            """The request body, or None after an error reply (the connection is then closed)."""
            if self.headers.get("Transfer-Encoding"):
                self.close_connection = True
                self._reply(411, {"error": "send Content-Length (no chunked bodies)"})
                return None
            try:
                n = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                n = -1
            if n < 0:
                self.close_connection = True
                self._reply(400, {"error": "bad Content-Length"})
                return None
            if n > max_body:
                self.close_connection = True
                self._reply(413, {"error": f"body too large (max {max_body} bytes)"})
                return None
            return self.rfile.read(n)

        def _json(self, body):
            try:
                return json.loads(body), None
            except ValueError as e:  # JSONDecodeError, UnicodeDecodeError
                return None, f"bad JSON: {e}"

        def do_POST(self):
            body = self._body()
            if body is None or not self._authed():
                return
            t0 = time.perf_counter()
            with lock:
                st["last"] = time.time()
                st["posts"] = st.get("posts", 0) + 1
            p = self._route()
            if p in ("/decide", "/"):
                req, err = self._json(body)
                if err:
                    self._reply(400, {"error": err})
                    return
                try:
                    out = host.decide(req)
                except fc.RequestError as e:
                    self._reply(400, {"error": str(e)})
                except fc.EngineClosed as e:
                    self._reply(503, {"error": f"engine closed: {e}"})
                except TimeoutError:  # concurrent.futures.TimeoutError is TimeoutError (Python >= 3.11)
                    self._reply(504, {"error": f"no answer within {getattr(host, 'decide_timeout', '?')} s"})
                except Exception as e:  # noqa: BLE001 - a server error must not kill the server
                    traceback.print_exc()
                    self._reply(500, {"error": f"{type(e).__name__}: {e}"})
                else:
                    out["server_ms"] = (time.perf_counter() - t0) * 1000  # body read -> response ready (no network)
                    self._reply(200, out, served=True)
            elif p == "/admin/config":
                obj, err = self._json(body)
                if err:
                    self._reply(400, {"error": err})
                    return
                try:
                    h = host.admin_config(obj)
                except fc.RequestError as e:
                    self._reply(400, {"error": str(e)})
                except Exception as e:  # noqa: BLE001
                    traceback.print_exc()
                    self._reply(500, {"error": f"{type(e).__name__}: {e}"})
                else:
                    with lock:
                        served, errors = st["n"], st["errors"]
                    self._reply(200, {**h, "served": served, "errors": errors})
            elif p == "/admin/flush":
                self._reply(200, host.flush())
            elif p == "/shutdown":
                with lock:
                    served = st["n"]
                self._reply(200, {"ok": True, "served": served})
                on_shutdown()
            else:
                self._reply(404, {"error": "not found"})

        def log_message(self, *a):
            pass

    class S(ThreadingHTTPServer):
        daemon_threads = True
        allow_reuse_address = True

    return S((bind, port), H), st


def is_cuda_fatal(e: BaseException) -> bool:
    """A CUDA error that poisons the process's CUDA context (device-side assert, illegal address, launch failure):
    nothing more can run on the GPU in this process, so the only recovery is a new container. The rule lives in
    fastcore.batcher.is_cuda_fatal (the serving path uses it too); a fastcore that cannot even be imported means no
    CUDA work ran, so not fatal."""
    try:
        fc = fastcore_import()
    except Exception:  # noqa: BLE001 - called from the boot's error handler: it must not raise
        return False
    return fc.is_cuda_fatal(e)


def serve_budget(seconds: float, elapsed_s: float, timeout_s: float = FUNCTION_TIMEOUT_S,
                 margin_s: float = SHUTDOWN_MARGIN_S) -> int:
    """Serving seconds after a boot that took elapsed_s: --seconds, clamped so the function returns before its
    timeout (this launch's timeout_s)."""
    return int(max(0.0, min(float(seconds), timeout_s - elapsed_s - margin_s)))


def launch_timeout(seconds: float) -> int:
    """One launch's function timeout: the boot budget + the serving window + the shutdown margin, at most the
    decorator's FUNCTION_TIMEOUT_S."""
    return int(min(FUNCTION_TIMEOUT_S, BOOT_BUDGET_S + float(seconds) + SHUTDOWN_MARGIN_S))


def engine_watchdog(host, stall_stop_s: float = STALL_STOP_S):
    """-> why serving must end now, or None: the engine worker stopped (a CUDA-fatal error poisons the context: every
    later request would fail) or one forward has run for more than stall_stop_s (a hung kernel never returns)."""
    s = host.eng.batcher.stats()
    if not s.get("alive"):
        return f"engine worker stopped ({'CUDA context lost' if s.get('cuda_fatal') else 'died'}: {s.get('dead')})"
    t = s.get("forward_inflight_s")
    if t is not None and t > stall_stop_s:
        return f"a GPU forward has run for {t:.0f} s (> {stall_stop_s:.0f} s): GPU hung"
    return None


def wait_serving(stop, st, deadline: float, idle_s: float, first_idle_s: float | None = None, watchdog=None,
                 poll_s: float = 2.0) -> str:
    """Block until serving ends -> the reason (core.wait_loop + a first-request grace + a watchdog): POST /shutdown,
    the serving deadline (unix s), idle_s without a POST (first_idle_s until the first POST arrives: the bench is
    started by hand), or watchdog() returning a reason (dead engine, hung GPU)."""
    first_idle_s = idle_s if first_idle_s is None else first_idle_s
    while True:
        if stop.wait(poll_s):
            return "shutdown request"
        now = time.time()
        if now > deadline:
            return "serving window (--seconds) reached"
        limit = idle_s if st.get("posts") else first_idle_s
        if now - st["last"] > limit:
            return f"idle for {limit:g} s" + ("" if st.get("posts") else " (no POST since the tunnel opened)")
        if watchdog is not None:
            try:
                why = watchdog()
            except Exception as e:  # noqa: BLE001 - a broken watchdog must not end a healthy session
                why = None
                print(f"watchdog error (ignored): {type(e).__name__}: {e}", flush=True)
            if why:
                return f"watchdog: {why}"


def check_adapter(model_dir) -> str:
    """C1's adapter on the Volume, sha256-pinned: returns the sha256 or refuses to boot (SystemExit)."""
    model_dir = Path(model_dir)
    f = model_dir / "adapter_model.safetensors"
    if not f.exists():
        raise SystemExit(f"{f} missing on this account's Volume (bash hosting/upload_c1_adapter.sh <profile>)")
    if (model_dir / "prism_x.json").exists():
        raise SystemExit(f"{model_dir} has prism_x.json: the fast path (CUDA graphs) does not support PRISM-X")
    sha = core.sha256_file(f)
    if sha != ADAPTER_SHA256:
        raise SystemExit(f"{MODEL}: adapter sha256 {sha} != pinned {ADAPTER_SHA256}: refusing to boot")
    return sha


def base_info(fp8: bool, pool: str) -> dict:
    return {"app": APP_NAME, "model": MODEL, "base": BASE, "revision": REVISION, "fp8": bool(fp8),
            "pool_requested": pool, "region": os.environ.get("MODAL_REGION"),
            "cloud": os.environ.get("MODAL_CLOUD_PROVIDER"),
            "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def _memory_gb(torch) -> dict:
    free, total = torch.cuda.mem_get_info()
    return {"max_allocated": round(torch.cuda.max_memory_allocated() / 2 ** 30, 2),
            "allocated": round(torch.cuda.memory_allocated() / 2 ** 30, 2),
            "reserved": round(torch.cuda.memory_reserved() / 2 ** 30, 2),
            "free": round(free / 2 ** 30, 2), "total": round(total / 2 ** 30, 2)}


def boot_container(fp8: bool = False, pool: str = "shared", flags: dict | None = None, boot_cfg: dict | None = None,
                   log=print) -> FastHost:
    """Container start-up (GPU only): core.boot_gpu's read-only inputs and load + merge, then boot_engine."""
    t0 = time.time()
    info = base_info(fp8, pool)
    cfg = normalize_boot_cfg(boot_cfg)
    tc = Path("/tmp/triton_cache")  # private copy: the Volume's Triton cache is only read (as core.boot_gpu)
    try:
        shutil.copytree("/vol/triton_cache", tc, dirs_exist_ok=True)
        info["triton_cache"] = "seeded from /vol/triton_cache"
    except Exception as e:  # noqa: BLE001
        info["triton_cache"] = f"not seeded: {type(e).__name__}"
    os.environ["TRITON_CACHE_DIR"] = str(tc)
    if core.base_snapshot_complete("/vol/hf"):  # read the Volume's copy offline: no Hub calls, no cache writes
        os.environ["HF_HUB_OFFLINE"] = "1"
        info["base_source"] = "/vol/hf snapshot (offline)"
    else:  # never write the Volume: download to the container's own disk
        os.environ["HF_HOME"] = "/tmp/hf"
        info["base_source"] = "downloaded to /tmp/hf"
    model_dir = VOL_MODELS / MODEL
    info["adapter_sha256"] = check_adapter(model_dir)  # before any GPU work
    fastcore_import()
    import torch
    from fastcore.engine import load_merged
    if not torch.cuda.is_available():
        raise SystemExit("no CUDA device")
    model, tok, load_info = load_merged(model_dir, dev="cuda", base=BASE, revision=REVISION)
    info["load"] = {k: load_info.get(k) for k in ("layout", "style", "revision", "prism_x", "chat_template_sha")}
    info["load_s"] = round(time.time() - t0, 1)
    info["memory_gb_after_load"] = _memory_gb(torch)
    log(f"loaded + merged in {info['load_s']} s: {json.dumps(info['load'])}")
    eng, rep = boot_engine(model, tok, device="cuda", fp8=fp8, flags=flags, pool=pool, boot_cfg=cfg, log=log)
    info["boot"] = rep
    info["memory_gb"] = _memory_gb(torch)
    info["gpu"] = torch.cuda.get_device_name(0)
    info["boot_s"] = round(time.time() - t0, 1)
    log("BOOT " + json.dumps({k: v for k, v in info.items() if k != "boot"}, default=str))
    log("BOOT engine " + json.dumps({k: rep.get(k) for k in ("engine", "parity_selftest", "fp8")}, default=str)[:20000])
    return FastHost(eng, info, decide_timeout=cfg["decide_timeout_s"])


# ------------------------------------------------------------------ Modal function

@app.function(image=image, gpu=GPU, cpu=2.0, memory=16384, volumes={"/vol": vol}, timeout=FUNCTION_TIMEOUT_S,
              max_containers=1, single_use_containers=True)  # cpu/memory as core.serve
def serve(q: modal.Queue, token: str, seconds: int = DEFAULT_SECONDS, idle_s: int = DEFAULT_IDLE_S, fp8: bool = False,
          flags: dict | None = None, pool: str = "shared", boot_cfg: dict | None = None,
          timeout_s: int = FUNCTION_TIMEOUT_S) -> dict:
    """timeout_s = this launch's function timeout (the launcher passes launch_timeout(seconds) here AND in
    with_options): serving is clamped to end SHUTDOWN_MARGIN_S before it."""
    t0 = time.time()
    try:
        host = boot_container(fp8=fp8, pool=pool, flags=flags, boot_cfg=boot_cfg)
    except BaseException as e:  # noqa: BLE001 - report, then this single-use container exits (fresh CUDA next time)
        traceback.print_exc()
        fatal = is_cuda_fatal(e)
        msg = {"boot_failed": f"{type(e).__name__}: {e}"[:4000], "cuda_fatal": fatal,
               "retry_private": bool(fatal and pool == "shared"), "pool": pool, "wall_s": round(time.time() - t0, 1)}
        q.put(msg)
        return msg
    stop = threading.Event()
    srv, st = make_fast_server(PORT, token, host, stop.set)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    serve_s = serve_budget(seconds, time.time() - t0, min(float(timeout_s), FUNCTION_TIMEOUT_S))
    with modal.forward(PORT) as tunnel:
        st["last"] = time.time()
        deadline = host.open_window(serve_s)  # /health shows serve_deadline_* and serve_remaining_s from now on
        q.put({"url": tunnel.url, "health": host.health()})
        reason = wait_serving(stop, st, deadline, idle_s, max(FIRST_IDLE_S, idle_s),
                              watchdog=lambda: engine_watchdog(host))
    srv.shutdown()
    srv.server_close()
    host.eng.close(timeout=30)
    out = {"info": {k: v for k, v in host.info.items() if k != "boot"}, "served": st["n"], "errors": st["errors"],
           "status": dict(st["status"]), "batcher": host.eng.batcher.stats(), "stop": reason,
           "wall_s": round(time.time() - t0, 1)}
    print("DONE " + json.dumps(out, default=str), flush=True)
    return out


# ------------------------------------------------------------------ local entrypoint (runs on the laptop)

def arm_flags(arm: str, fp8: bool, arms_file=ARMS_FILE) -> dict:
    """The initial flags of an HF arm from hosting/speed_arms.json; the boot (BF16 / FP8) must be the arm's."""
    arms = json.loads(Path(arms_file).read_text())["arms"]
    if arm not in arms:
        raise SystemExit(f"unknown arm {arm!r} (speed_arms.json: {sorted(arms)})")
    a = arms[arm]
    if a.get("engine") != "hf":
        raise SystemExit(f"arm {arm} runs on engine {a.get('engine')!r}, not on this HF host")
    if bool(a.get("fp8")) != bool(fp8):
        raise SystemExit(f"arm {arm} needs {'the --fp8 boot' if a.get('fp8') else 'a BF16 boot (no --fp8)'}")
    return dict(a["flags"])


def parse_boot_cfg(s: str) -> dict:
    if not s:
        return {}
    try:
        cfg = json.loads(s)
        if not isinstance(cfg, dict):
            raise ValueError("not an object")
        normalize_boot_cfg(cfg)
    except (ValueError, TypeError, AttributeError) as e:
        raise SystemExit(f"--boot-cfg: {e}") from None
    return cfg


def cost_estimate(minutes: float, region_mult: float) -> dict:
    rate = (RATE_USD_H + CPU_MEM_USD_H) * region_mult
    return {"rate_usd_h": round(rate, 2), "minutes": round(minutes, 1), "usd": round(rate * minutes / 60, 2)}


def worst_case(seconds: float, region_mult: float, pool: str = "shared") -> dict:
    """The billed worst case of one launch (checked against --max-usd): its function timeout + container start, plus,
    with the shared pool, one failed boot of up to BOOT_BUDGET_S before the single private-pool reboot."""
    s = launch_timeout(seconds) + CONTAINER_START_S
    if pool == "shared":
        s += BOOT_BUDGET_S + CONTAINER_START_S
    return {**cost_estimate(s / 60, region_mult), "timeout_s": launch_timeout(seconds)}


def write_session(path, url: str, token: str, flags, extra: dict | None = None, token_path=None) -> dict:
    """speed/session_url.json = {url, token, started_at, flags, ...} (mode 0600: the token stays on this laptop), and
    the plain token in token_path for speed_bench --token-file."""
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


def smoke(url: str, token: str, rounds: int = 3, requests=None) -> dict:
    """Built-in requests over the tunnel: client and server latency, paths, errors (no task data)."""
    import client_bench as cb
    c = cb.Ours(url, token, timeout=120.0)
    recs = []
    try:
        for _ in range(rounds):
            for r in (SELFTEST_REQUESTS if requests is None else requests):
                d, ms, err = c.decide(r)
                recs.append({"id": r.get("id"), "client_ms": ms, "server_ms": (d or {}).get("server_ms"),
                             "path": (d or {}).get("path"), "error": err})
    finally:
        c.close()
    return {"calls": len(recs), "errors": sum(1 for x in recs if x["error"]),
            "client_ms": cb.stats([x["client_ms"] for x in recs if not x["error"]]),
            "server_ms": cb.stats([x["server_ms"] for x in recs if not x["error"]]),
            "paths": dict(Counter(x["path"] for x in recs)),
            "first_error": next((x["error"] for x in recs if x["error"]), None)}


def _hold(call):
    while True:  # until the server stops itself (shutdown, --seconds, --idle) or Ctrl-C
        try:
            return call.get(timeout=30)
        except (modal.exception.TimeoutError, TimeoutError):
            continue


def _drain(call, wait=120):
    try:
        return call.get(timeout=wait)
    except Exception as e:  # noqa: BLE001
        print(f"no clean return ({type(e).__name__}); cancelling", flush=True)
        call.cancel()
        return None


def run_main(region: str = "any", fp8: bool = False, seconds: int = 0, idle: int = DEFAULT_IDLE_S,
             hold: bool = False, arm: str = "", pool: str = "shared", boot_cfg: str = "", boot_wait: int = 1500,
             max_usd: float = DEFAULT_MAX_USD, env=None, session_file=SESSION_FILE, token_file=TOKEN_FILE) -> dict:
    """main's body. The payer guard runs first, then every argument check and the --max-usd worst-case check: nothing
    is spawned for a refused launch. seconds 0 = SMOKE_SECONDS for a smoke, MAX_SECONDS with --hold."""
    profile = payer_guard(os.environ if env is None else env,
                          getattr(modal.config, "_profile", None) if env is None else None)
    arm = arm or ("A3" if fp8 else "A2")
    flags = arm_flags(arm, fp8)
    if pool not in ("shared", "private"):
        raise SystemExit("--pool must be shared or private")
    seconds = int(seconds or (MAX_SECONDS if hold else SMOKE_SECONDS))
    if not 60 <= seconds <= MAX_SECONDS:
        raise SystemExit(f"--seconds must be in 60..{MAX_SECONDS} (boot budget {BOOT_BUDGET_S} s + serving + "
                         f"{SHUTDOWN_MARGIN_S} s must fit the {FUNCTION_TIMEOUT_S} s function timeout)")
    if not 30 <= idle <= seconds:
        raise SystemExit("--idle must be in 30..--seconds")
    cfg = parse_boot_cfg(boot_cfg)
    reg, mult = core._region_opt(region)
    timeout_s = launch_timeout(seconds)
    worst = worst_case(seconds, mult, pool)
    if worst["usd"] > max_usd:
        raise SystemExit(f"REFUSED by --max-usd {max_usd}: worst case ${worst['usd']} ({worst['minutes']} min at "
                         f"${worst['rate_usd_h']}/h, region {region}: timeout {timeout_s} s + container start"
                         f"{' + one failed shared-pool boot' if pool == 'shared' else ''}). Use --region any, a "
                         f"shorter --seconds, or raise --max-usd.")
    import client_bench as cb
    token = secrets.token_urlsafe(24)
    print(json.dumps({"payer": profile, "app": APP_NAME, "region": region, "fp8": fp8, "arm": arm, "flags": flags,
                      "pool": pool, "boot_cfg": cfg, "mode": "hold" if hold else "smoke", "seconds": seconds,
                      "idle": idle, "first_idle": max(FIRST_IDLE_S, idle), "timeout_s": timeout_s,
                      "max_usd": max_usd, "estimate": {
                          "expected_full_window": cost_estimate(BOOT_EST_MIN + seconds / 60, mult),
                          "smoke": cost_estimate(BOOT_EST_MIN + 1, mult), "worst_case": worst}}), flush=True)
    t0 = time.time()
    opts = {"gpu": GPU, "timeout": timeout_s, **({"region": reg} if reg else {})}
    res, url, msg, stop_note = None, None, None, None
    with modal.Queue.ephemeral() as q:
        for attempt in (1, 2):
            call = serve.with_options(**opts).spawn(q, token, seconds, idle, fp8, flags, pool, cfg, timeout_s)
            msg = core._wait_url(q, call, boot_wait, f"H100 fast host ({region}, {pool} pool)")
            if "boot_failed" not in msg:
                break
            print(f"BOOT FAILED ({pool} pool): {msg['boot_failed'][:1500]}", flush=True)
            _drain(call)
            if msg.get("retry_private") and attempt == 1:
                if float(msg.get("wall_s") or 0) > BOOT_BUDGET_S:  # keeps the worst case checked above
                    raise SystemExit(f"boot failed after {msg.get('wall_s')} s (> {BOOT_BUDGET_S} s): not rebooting; "
                                     f"relaunch with --pool private if wanted")
                pool = "private"
                print("CUDA context lost during a shared-pool boot: rebooting ONCE with private pools", flush=True)
                continue
            raise SystemExit(f"boot failed: {msg['boot_failed'][:500]}")
        url, health = msg["url"], msg["health"]
        print(f"server up after {time.time() - t0:.0f} s: {url}\nhealth: ok={health.get('ok')} problems="
              f"{health.get('problems')} boot_s={health.get('boot_s')} graphs={json.dumps(health.get('graphs'))[:600]}",
              flush=True)
        write_session(session_file, url, token, health.get("flags"), token_path=token_file,
                      extra={"payer": profile, "app": APP_NAME, "region": region, "fp8": fp8, "arm": arm, "pool": pool,
                             "adapter_sha256": health.get("adapter_sha256"),
                             "config_sha256": health.get("config_sha256"), "health_ok": health.get("ok"),
                             "serve_s": health.get("serve_s"), "serve_deadline_utc": health.get("serve_deadline_utc"),
                             "timeout_s": timeout_s})
        print(f"wrote {session_file} and {token_file} (mode 0600)", flush=True)
        try:
            if not health.get("ok"):
                stop_note = f"/health not ok ({health.get('problems')}): shut down at once"
                print("HEALTH NOT OK: " + json.dumps({"problems": health.get("problems"), "parity_selftest": (
                    health.get("boot") or {}).get("parity_selftest")}, default=str)[:3000], flush=True)
            elif hold:
                arms = "A3" if fp8 else HOLD_ARMS
                print(f"\nHOLD: serving for up to {health.get('serve_s')} s (until {health.get('serve_deadline_utc')}"
                      f"; idle stop {idle} s after the last POST, {max(FIRST_IDLE_S, idle)} s before the first). From "
                      f"another terminal (lean/), now:\n  ../.venv/bin/python hosting/speed_bench.py ab --url {url} "
                      f"--token-file {os.path.relpath(token_file, LEAN)} --session <NAME> --arms {arms} "
                      f"--shutdown-after --go\nCtrl-C here (or POST /shutdown) stops the GPU.", flush=True)
                _hold(call)
            else:
                cb.wait_ready(url, token, timeout=120)
                print("SMOKE " + json.dumps(smoke(url, token)), flush=True)
        except KeyboardInterrupt:
            print("interrupted: shutting the server down", flush=True)
        finally:
            res = core._finish(call, cb, url, token)
    est = cost_estimate((time.time() - t0) / 60, mult)
    out = {"cost_estimate_upper": {**est, "note": "spawn to end; GPU queue time before the container starts is not "
                                                  "billed"},
           "server_stop": (res or {}).get("stop"), "served": (res or {}).get("served"), "note": stop_note}
    try:  # mark the session ended (the URL and token are dead now)
        rec = json.loads(Path(session_file).read_text())
        write_session(session_file, rec["url"], rec["token"], rec.get("flags"),
                      extra={**{k: v for k, v in rec.items() if k not in ("url", "token", "flags", "started_at")},
                             "started_at": rec.get("started_at"), "ended_at": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                                                            time.gmtime()),
                             "stop": out["server_stop"]})
    except Exception as e:  # noqa: BLE001
        print(f"session file not updated: {e}", flush=True)
    print(json.dumps(out, indent=2), flush=True)
    if stop_note:
        raise SystemExit(stop_note)
    return out


@app.local_entrypoint()
def main(region: str = "any", fp8: bool = False, seconds: int = 0, idle: int = DEFAULT_IDLE_S, hold: bool = False,
         arm: str = "", pool: str = "shared", boot_cfg: str = "", boot_wait: int = 1500,
         max_usd: float = DEFAULT_MAX_USD):
    """C1 fast host on one H100: smoke test (default) or --hold for a SPEED-2 session. See the module docstring."""
    run_main(region=region, fp8=fp8, seconds=seconds, idle=idle, hold=hold, arm=arm, pool=pool, boot_cfg=boot_cfg,
             boot_wait=boot_wait, max_usd=max_usd)
