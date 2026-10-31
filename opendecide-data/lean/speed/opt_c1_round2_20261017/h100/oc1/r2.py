"""oc1.r2: the arms, the measurement steps and the in-container block runner of the round-2 H100 window (17 Oct 2026).

ARMS (priority order; each block is gated by the running spend, trailing blocks are dropped when the budget runs out):
  A  r2_a        S1 BF16 reference (fresh, same session): full parity answers (c32 + a second pass at c64 = BF16 self-agreement
                 floor and the "BF16 re-run" of the margin-gate replay), batch-1 N latency x2, N and P c64 throughput, R prefix,
                 image arms on the S1 server (native x2 / x2 at c1 and c8 = noise floor, client-side exact-size pre-resize)
  B  r2_b        EXACT BUNDLE: --cuda-graph-backend-prefill full, --skip-tokenizer-init (+ input_ids), /v1/score readout,
                 LM-head slice to the 141 option-token rows (opt-in sitecustomize patch), --enable-metrics,
                 --gc-warning-threshold-secs 0.005.  r2_b_nofull (same without `full`) runs only if `full` fails/falls back;
                 r2_b_gc (+ gc.freeze() after warm-up) runs only if the GC warnings show pauses.
  C  r2_c        block-FP8 checkpoint (128x128 weights, dynamic activations) with --quantization fp8; the margin gate is an
                 OFFLINE analysis on these answers (analyze_h100.py)
  D  r2_d1/d2    image flags: --keep-mm-feature-on-device ; --mm-processor-worker-num 4   (native x2 at c1, c8)
  E  r2_e1/e2    --mamba-ssm-dtype bfloat16 ; --mamba-track-interval 64

Everything below the config section runs inside the container: `r2measure` / `r2vision` are runner commands (oc1.runner) and
`R2Session` is the block loop (a Session subclass: same server start/stop, gate and emit machinery as the 17 Oct session).
"""
from __future__ import annotations

import json
import os
import re
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

from . import common as C
from . import configs as K
from . import parity as PAR
from . import session as S

PATCH_DIR = "/root/r2pypatch"
IDS_FILE = "/root/extra/option_ids_union.json"
FP8_NAME = f"{C.MERGED_NAME}__fp8_block"
FP8_SHARD_SHA256 = {                       # built on od-cpu1 and od-l4b (byte-identical), 17 Oct 2026
    "model.safetensors-00001-of-00002.safetensors": "4bbce9917641a622d12f29c7dcba2eb4c4fb827b49f31479ecf7cb848e8dee73",
    "model.safetensors-00002-of-00002.safetensors": "d01e6983e931465de8c049a5ce405c91ef0904aad3091b2f340c3120388d4c1d",
}
PARITY_CONC = 32
P_SAT_ROWS = 2500


# ====================================================================== configs
@dataclass
class R2Config(K.Config):
    arm: str = ""
    backend: str = "generate"                       # readout used by the runner: generate | score
    steps: list = field(default_factory=list)       # runner steps, in order
    vision: list = field(default_factory=list)      # image arms "kind:conc"
    est_s: int = 400                                 # block estimate (s) for the budget gate
    parity_ref: str = "r2_a"                         # whose answers_P.jsonl is the same-session reference
    gc_flag: bool = False                            # touch the gc-freeze flag file once the warm-up is done
    uses_patch: bool = False
    canary_min: float = 0.0                          # >0: first 300 P decisions vs the reference; below it the block stops early


def patch_env(tag: str, gc_freeze: bool = False) -> dict:
    env = {"PYTHONPATH": PATCH_DIR, "R2_LMHEAD_IDS": IDS_FILE, "R2_REPORT": f"/tmp/r2_patch_{tag}.jsonl"}
    if gc_freeze:
        env.update({"R2_GC_FREEZE": "600", "R2_GC_FLAG": "/tmp/r2_gc_flag"})   # freezes when the runner touches the flag
    return env


BUNDLE = ["--skip-tokenizer-init", "--enable-metrics", "--gc-warning-threshold-secs", "0.005"]
FULL_PREFILL = ["--cuda-graph-backend-prefill", "full"]
VISION_A = ["native:1", "native:1", "native:8", "native:8", "exact:1", "exact:8"]
VISION_D = ["native:1", "native:1", "native:8", "native:8"]
TEXT_STEPS = ["parity", "latency", "throughput"]


def build_r2_configs() -> dict:
    cs = [
        R2Config("r2_a", "A. S1 BF16 reference: merged C1, fp32 lm head, hybrid radix cache, breakable prefill graphs, /generate readout",
                 arm="A", steps=TEXT_STEPS + ["prefix", "parity_c64"], vision=VISION_A, est_s=700, priority=0),
        R2Config("r2_b", "B. exact bundle: full-graph prefill + skip-tokenizer-init + /v1/score + LM-head slice (141 rows) + metrics + gc warnings",
                 arm="B", extra=FULL_PREFILL + BUNDLE, env=patch_env("b"), backend="score", steps=["canary"] + TEXT_STEPS, est_s=540,
                 priority=1, uses_patch=True, canary_min=0.97),
        R2Config("r2_b_dcpc", "B (variant): the bundle with full-graph prefill AND --disable-chunked-prefix-cache (only if plain `full` was refused "
                              "because the GDN hybrid backend does not opt into the chunked-prefix full-graph topology)",
                 arm="B", extra=FULL_PREFILL + ["--disable-chunked-prefix-cache"] + BUNDLE, env=patch_env("bdc"), backend="score",
                 steps=["canary"] + TEXT_STEPS, est_s=540, priority=1, uses_patch=True, canary_min=0.97),
        R2Config("r2_b_nofull", "B' (fallback): the bundle WITHOUT --cuda-graph-backend-prefill full",
                 arm="B", extra=BUNDLE, env=patch_env("bnf"), backend="score", steps=["canary"] + TEXT_STEPS, est_s=500, priority=1,
                 uses_patch=True, canary_min=0.97),
        R2Config("r2_b_gc", "B+gc: the bundle (as it stands after B) plus gc.freeze() after the warm-up",
                 arm="B", extra=BUNDLE, env=patch_env("bgc", gc_freeze=True), backend="score", steps=["latency", "throughput"],
                 est_s=300, priority=1, gc_flag=True, uses_patch=True),
        R2Config("r2_c", "C. block-FP8 checkpoint (128x128 weights, dynamic activations), --quantization fp8, /generate readout",
                 arm="C", model="fp8_block", extra=["--quantization", "fp8"], steps=["canary"] + TEXT_STEPS, est_s=430, priority=2, fp8=True,
                 canary_min=0.93),
        R2Config("r2_d1", "D1. image: --keep-mm-feature-on-device (native x2 at c1 and c8)", arm="D",
                 extra=["--keep-mm-feature-on-device"], steps=[], vision=VISION_D, est_s=240, priority=3),
        R2Config("r2_d2", "D2. image: --mm-processor-worker-num 4 (native x2 at c1 and c8)", arm="D",
                 extra=["--mm-processor-worker-num", "4"], steps=[], vision=VISION_D, est_s=240, priority=3),
        R2Config("r2_e1", "E1. --mamba-ssm-dtype bfloat16 (S1 runs float32)", arm="E", drop=["--mamba-ssm-dtype"],
                 extra=["--mamba-ssm-dtype", "bfloat16"], steps=["canary"] + TEXT_STEPS + ["prefix"], est_s=460, priority=4, canary_min=0.97),
        R2Config("r2_e2", "E2. --mamba-track-interval 64 (S1 runs the default)", arm="E", extra=["--mamba-track-interval", "64"],
                 steps=["canary"] + TEXT_STEPS + ["prefix"], est_s=460, priority=4, canary_min=0.97),
    ]
    return {c.name: c for c in cs}


R2_CONFIGS = build_r2_configs()
DEFAULT_ORDER = ["r2_a", "r2_b", "r2_c", "r2_d1", "r2_d2", "r2_e1", "r2_e2"]


# ====================================================================== resolved-args expectations
def parse_flag_values(cmd: list) -> dict:
    """{key: value} for every `--flag value` / `--flag` in a command (keys with underscores; numbers coerced)."""
    out, i = {}, 0
    while i < len(cmd):
        a = cmd[i]
        if a.startswith("--"):
            key = a[2:].replace("-", "_")
            if i + 1 < len(cmd) and not cmd[i + 1].startswith("--"):
                v = cmd[i + 1]
                try:
                    v = int(v)
                except ValueError:
                    try:
                        v = float(v)
                    except ValueError:
                        pass
                out[key] = v
                i += 2
                continue
            out[key] = True
        i += 1
    return out


def want_args_r2(cfg: R2Config, model_path) -> dict:
    """S.want_args (S1's resolved args) with this arm's flags applied on top."""
    w = S.want_args(cfg, model_path)
    fl = parse_flag_values(cfg.cmd(model_path))
    for k in ("mamba_ssm_dtype", "quantization"):
        if k in fl:
            w[k] = fl[k]
    for k in ("skip_tokenizer_init", "mm_processor_worker_num", "mamba_track_interval", "gc_warning_threshold_secs", "enable_metrics",
              "keep_mm_feature_on_device"):
        if k in fl:
            w[k] = fl[k]
    return w


def check_args_r2(resolved: dict, want: dict) -> tuple:
    problems, warnings = S.check_args(resolved, {k: v for k, v in want.items() if k in S.CRITICAL or k in resolved or k in (
        "skip_tokenizer_init",)})
    return problems, warnings


def graph_prefill_backend(info: dict):
    """The prefill graph backend SGLang RESOLVED (after its compatibility cascade), from /server_info."""
    try:
        cg = info.get("cuda_graph_config")
        if isinstance(cg, dict):
            pf = cg.get("prefill")
            if isinstance(pf, dict):
                return pf.get("backend")
            return str(pf)
        if cg is not None:
            return str(getattr(getattr(cg, "prefill", None), "backend", cg))
    except Exception:  # noqa: BLE001
        pass
    return info.get("cuda_graph_backend_prefill")


# ====================================================================== runner side: steps
def lat_batch1_records(backend, preps: list, warm: int = 20) -> list:
    """One decision at a time on a warm server: per-call records (ids kept for the cascade estimate)."""
    rows = []
    for i, p in enumerate(preps):
        t0 = time.perf_counter()
        try:
            _, meta = backend.read(p, False)
            ok = True
        except Exception as e:  # noqa: BLE001
            meta, ok = {"err": f"{type(e).__name__}: {str(e)[:100]}"}, False
        ms = (time.perf_counter() - t0) * 1000.0
        if i >= warm:
            rows.append({"id": p.id, "ms": round(ms, 3), "ok": ok, "bucket": p.bucket, "tok": p.n_tokens,
                         "e2e": meta.get("server_e2e_ms"), "cached": meta.get("cached_tokens")})
    return rows


def summarize_records(rows: list) -> dict:
    good = [r for r in rows if r["ok"]]
    by = {"noul": [r["ms"] for r in good if r["bucket"] == "noul"], "choice": [r["ms"] for r in good if r["bucket"] != "noul"]}
    return {"n": len(good), "failed": len(rows) - len(good), "wall_ms": C.summarize([r["ms"] for r in good], 3),
            "by_type": {k: C.summarize(v, 3) for k, v in by.items()},
            "server_e2e_ms": C.summarize([r["e2e"] for r in good if r["e2e"] is not None], 3),
            "mean_tokens": round(sum(r["tok"] for r in good) / len(good), 1) if good else None}


def run_r2measure(spec: dict, log=print) -> dict:
    """spec: config, backend, sgl_url, work_dir, c1_dir, out_dir, steps, params, refs {label: answers path}, go_file, abort_file,
    gc_flag (path or None)."""
    from . import measure as M
    from . import runner as RU
    from .backend import GenerateBackend, ScoreBackend
    ctx = RU.Ctx(spec, log)
    out_path = Path(spec["out_path"])
    steps = list(spec["steps"])
    need = ["N"] + (["P"] if {"parity", "throughput", "parity_c64", "canary"} & set(steps) else []) + (["R"] if "prefix" in steps else [])
    for name in need:                     # tokenized / rendered while the server is still booting
        ctx.preps(name)
    RU.wait_go(spec, log)
    client = ctx.SH.SGLangClient(spec["sgl_url"], timeout=180.0, max_connections=300)
    backend = ScoreBackend(client) if spec.get("backend") == "score" else GenerateBackend(client)
    gen = GenerateBackend(client)
    res = {"config": spec["config"], "backend": backend.name, "started_utc": C.utc(), "steps": {}, "errors": {}}
    params = spec.get("params", {})
    conc = int(params.get("parity_conc", PARITY_CONC))
    refs = dict(spec.get("refs") or {})

    def flush_out():
        C.write_json(out_path, res)

    def run(name, fn):
        t0 = time.time()
        try:
            res["steps"][name] = fn()
            res["steps"][name]["step_wall_s"] = round(time.time() - t0, 1)
            log(f"STEP {name} done in {time.time() - t0:.0f} s")
        except Exception as e:  # noqa: BLE001
            import traceback
            res["errors"][name] = f"{type(e).__name__}: {str(e)[:300]}"
            log(f"STEP {name} FAILED: {res['errors'][name]}\n{traceback.format_exc()[-800:]}")
        flush_out()

    def parity(sampler, c, tag, refs_):
        itemsP = ctx.items("P")
        preps = ctx.preps("P")
        r = M.parity_pass(backend, preps, conc=c, sampler=sampler)
        path = Path(spec["out_dir"]) / f"answers_P{tag}.jsonl"
        RU.save_answers(path, r.pop("answers"))
        cand = RU.load_answers(path)
        out = {"n_requested": len(preps), "conc": c, "answers_file": str(path), **r}
        for label, p in refs_.items():
            ref = RU.load_answers(p)
            if ref:
                out[f"parity_vs_{label}"] = PAR.compare_items(itemsP, cand, ref)
        return out

    def canary(sampler):
        """First `canary_n` P decisions against the reference (A's answers): a catastrophic arm (wrong readout, broken kernel,
        refused endpoint) stops the block here instead of after the 8,143-decision pass."""
        n = int(params.get("canary_n", 300))
        preps = ctx.preps("P")[:n]
        items = ctx.items("P")[:n]
        r = M.parity_pass(backend, preps, conc=8, sampler=None)
        ans = r.pop("answers")
        out = {"n": len(preps), "n_missing": r["n_missing"], "missing": r["missing"][:3], "min": spec.get("canary_min", 0.0)}
        agree = None
        for label, p in refs.items():
            ref = RU.load_answers(p)
            if ref:
                rep = PAR.compare_items(items, {k: v["probs"] for k, v in ans.items()}, ref)
                out["vs_" + label] = {k: rep[k] for k in ("n", "agree", "argmax_agree", "dp_max", "n_flips")}
                if label.startswith("r2_a"):
                    agree = rep["argmax_agree"]
        out["agree_vs_reference"] = agree
        out["stop"] = bool(spec.get("canary_min", 0.0) and (r["n_missing"] > 0.2 * len(preps) or (agree is not None and agree < spec["canary_min"])))
        return out

    def latency(sampler):
        out = {}
        n, warm = int(params.get("lat_n", 320)), int(params.get("lat_warm", 20))
        preps = ctx.preps("N")[: n + warm]
        for p in ctx.preps("N")[:warm]:
            backend.read(p, False)
        allrows = {}
        for rep in (1, 2):
            M.flush(client)
            t0 = time.time()
            rows = lat_batch1_records(backend, preps, warm)
            s = summarize_records(rows)
            s["gpu"] = sampler.between(t0, time.time())
            out[f"rep{rep}"] = s
            allrows[f"rep{rep}"] = rows
        C.write_json(Path(spec["out_dir"]) / "latency_records.json", allrows)
        return out

    def throughput(sampler):
        out = {"N_c64": M.throughput(backend, ctx.preps("N"), (64,), client=client, sampler=sampler)["c64"]}
        out["N_c64_rep2"] = M.throughput(backend, ctx.preps("N"), (64,), client=client, sampler=sampler)["c64"]   # 660 calls is a short run
        out["P_sat_c64"] = M.throughput(backend, ctx.preps("P")[:P_SAT_ROWS], (64,), client=client, sampler=sampler)["c64"]
        out["P_sat_rows"] = min(P_SAT_ROWS, len(ctx.preps("P")))
        return out

    with M.GpuSampler(0.5) as sampler:
        t0 = time.time()
        try:
            M.closed_loop(backend.read, ctx.preps("N")[:60], 4)          # warm-up: JIT / graph shapes
            M.flush(client)
        except Exception as e:  # noqa: BLE001
            res["errors"]["warmup"] = f"{type(e).__name__}: {e}"
        if spec.get("gc_flag"):
            Path(spec["gc_flag"]).write_text("go")                       # the gc.freeze() patch fires on this file
            time.sleep(2.0)
        res["warmup_s"] = round(time.time() - t0, 1)
        flush_out()
        for st in steps:
            if st == "canary":
                run("canary", lambda: canary(sampler))
                if res["steps"].get("canary", {}).get("stop") or "canary" in res["errors"]:
                    res["aborted"] = "canary: " + json.dumps(res["steps"].get("canary") or res["errors"].get("canary"), default=str)[:400]
                    log("CANARY STOP: " + res["aborted"])
                    break
            elif st == "parity":
                M.flush(client)
                run("parity", lambda: parity(sampler, conc, "", refs))
            elif st == "parity_c64":
                M.flush(client)
                own = {"same_boot_c32": str(Path(spec["out_dir"]) / "answers_P.jsonl")}
                run("parity_c64", lambda: parity(sampler, 64, "_c64", {**refs, **own}))
            elif st == "latency":
                run("latency", lambda: latency(sampler))
            elif st == "throughput":
                run("throughput", lambda: throughput(sampler))
            elif st == "prefix":
                run("prefix", lambda: RU.step_prefix(ctx, gen, client))
    res["finished_utc"] = C.utc()
    flush_out()
    return res


# ------------------------------------------------------------------ vision
def _prepare_image(path: Path, kind: str):
    """(bytes, (h, w) sent, predicted visual tokens). native = the file as is; exact = PIL-bicubic resize to the processor's own
    smart_resize size, re-encoded losslessly (PNG)."""
    import io
    from PIL import Image
    from . import vision as V
    if kind == "native":
        im = Image.open(path)
        im.load()
        h0, w0 = im.size[1], im.size[0]
        h, w = V.smart_resize(h0, w0)
        return path.read_bytes(), (h0, w0), V.visual_tokens(h, w)
    if kind == "exact":
        im = Image.open(path)
        im.load()
        im = im.convert("RGB")
        w0, h0 = im.size
        h, w = V.smart_resize(h0, w0)
        if (h, w) != (h0, w0):
            im = im.resize((w, h), Image.BICUBIC)
        buf = io.BytesIO()
        im.save(buf, format="PNG", compress_level=1)      # lossless; level 1 keeps the client cost low
        return buf.getvalue(), (h, w), V.visual_tokens(h, w)
    raise ValueError(kind)


def _vision_arm(mk_client, items, pack: Path, kind: str, conc: int, warm: int = 6):
    from . import vision as V
    for it in items[:warm]:
        b, _, pt = _prepare_image(pack / it["image"], kind)
        try:
            V.post_item(mk_client(), it, b, pt)
        except Exception:  # noqa: BLE001
            pass
    recs = [None] * len(items)
    nxt, lock, tl = [0], threading.Lock(), threading.local()

    def cl():
        if getattr(tl, "c", None) is None:
            tl.c = mk_client()
        return tl.c

    def worker():
        while True:
            with lock:
                i = nxt[0]
                nxt[0] += 1
            if i >= len(items):
                return
            it = items[i]
            t0 = time.perf_counter()
            b, hw, pt = _prepare_image(pack / it["image"], kind)
            prep_ms = (time.perf_counter() - t0) * 1000.0
            try:
                r = V.post_item(cl(), it, b, pt)
                p = r["probs"]
                pred = max(range(len(p)), key=p.__getitem__)
                recs[i] = {"id": it["id"], "suite": it["suite"], "ok": True, "pred": pred, "correct": int(pred == it["gold"]),
                           "probs": [round(x, 7) for x in p], "ms": round(r["ms"], 3), "prep_ms": round(prep_ms, 3),
                           "token_mismatch": bool(r["token_mismatch"]), "size_hw": list(hw), "pred_tokens": pt}
            except Exception as e:  # noqa: BLE001
                recs[i] = {"id": it["id"], "suite": it["suite"], "ok": False, "err": f"{type(e).__name__}: {str(e)[:80]}"}

    t_start = time.perf_counter()
    th = [threading.Thread(target=worker, daemon=True) for _ in range(conc)]
    for t in th:
        t.start()
    for t in th:
        t.join()
    return recs, time.perf_counter() - t_start


def run_r2vision(spec: dict, log=print) -> dict:
    """spec: sgl_url, pack_dir, arms ["native:1", ...], out_path. 200 items (100 Pets + 100 VQA yes/no)."""
    import httpx
    from . import measure as M
    pack = Path(spec["pack_dir"])
    items = C.read_jsonl(pack / "items.jsonl")
    mk = lambda: httpx.Client(base_url=spec["sgl_url"], timeout=300.0)  # noqa: E731
    res = {"n_items": len(items), "arms": []}
    with M.GpuSampler(0.5) as gs:
        for k, a in enumerate(spec["arms"]):
            kind, conc = a.split(":")
            t0w = time.time()
            recs, wall = _vision_arm(mk, items, pack, kind, int(conc))
            good = [r for r in recs if r and r.get("ok")]
            arm = {"k": k, "arm": a, "kind": kind, "conc": int(conc), "n_ok": len(good), "errors": len(recs) - len(good),
                   "acc": round(100 * sum(r["correct"] for r in good) / max(1, len(good)), 2),
                   "ms": C.summarize([r["ms"] for r in good], 3), "prep_ms": C.summarize([r["prep_ms"] for r in good], 3),
                   "wall_s": round(wall, 2), "items_per_s": round(len(good) / wall, 3) if wall else None,
                   "token_mismatches": sum(r["token_mismatch"] for r in good), "gpu": gs.between(t0w, time.time()),
                   "records": recs}
            res["arms"].append(arm)
            log(f"vision arm{k} {a}: acc {arm['acc']} p50 {arm['ms'].get('p50')} p95 {arm['ms'].get('p95')} items/s {arm['items_per_s']} "
                f"mism {arm['token_mismatches']} err {arm['errors']}")
            C.write_json(spec["out_path"], res)
    return res


# ====================================================================== in-container block runner
def scan_log(path: Path, max_lines: int = 8) -> dict:
    """Counts + first lines of the SGLang log: GC warnings, graph / fallback mentions, errors (warning-level log only)."""
    pats = {"gc": re.compile(r"\bGC\b|garbage", re.I), "graph": re.compile(r"graph", re.I),
            "fallback": re.compile(r"fall(ing)? ?back|disabl", re.I), "error": re.compile(r"\berror\b|traceback|exception", re.I),
            "fp8": re.compile(r"fp8|block.?wise|deepgemm|deep_gemm|config file not found|sub-optimal", re.I)}
    out = {k: {"n": 0, "first": []} for k in pats}
    try:
        for line in Path(path).read_text(errors="replace").splitlines():
            for k, rx in pats.items():
                if rx.search(line):
                    out[k]["n"] += 1
                    if len(out[k]["first"]) < max_lines:
                        out[k]["first"].append(line[:300])
    except OSError:
        pass
    return out


def scrape_metrics(url: str, path: Path) -> dict:
    import httpx
    try:
        r = httpx.get(url + "/metrics", timeout=20.0)
        txt = r.text
        path.write_text(txt[:400000])
        lines = [l for l in txt.splitlines() if l and not l.startswith("#")]
        keep = [l[:200] for l in lines if re.search(r"graph|gc|cache_hit|num_requests|e2e|prefill|forward", l, re.I)]
        return {"status": r.status_code, "n_series": len(lines), "graph_related": keep[:40]}
    except Exception as e:  # noqa: BLE001
        return {"error": f"{type(e).__name__}: {str(e)[:150]}"}


class R2Session(S.Session):
    """Session whose blocks are R2Configs: boot -> runner steps -> vision -> metrics/patch report -> stop.
    `server_factory(cfg, mdir, python, log, log_file)` makes the server object (tests pass a fake)."""

    def __init__(self, *a, fp8_wait=None, configs=None, server_factory=None, **kw):
        super().__init__(*a, **kw)
        self.fp8_wait = fp8_wait or (lambda: {"ok": True})        # joins the fp8 checkpoint verification thread
        self.configs = dict(configs or R2_CONFIGS)
        self.server_factory = server_factory or (lambda cfg, mdir, python, log, log_file: S.SglServer(cfg, mdir, python, log=log, log_file=log_file))
        self.queue = list(self.plan.get("configs") or DEFAULT_ORDER)
        self.ran = set()
        self.notes = []

    def block_cost(self, cfg) -> float:
        return float(getattr(cfg, "est_s", 0) or 0) / 3600.0 * self.rate

    def model_dir(self, cfg) -> str:
        name = {"merged": C.MERGED_NAME, "fp8_block": FP8_NAME}[cfg.model]
        return str(Path(self.models_root) / name)

    def ref_paths(self, cfg) -> dict:
        refs = {}
        if cfg.parity_ref != cfg.name:
            p = Path(self.results_root) / cfg.parity_ref / "answers_P.jsonl"
            if p.exists():
                refs["r2_a_same_session"] = str(p)
        stored = Path(self.work_dir) / "ref_speed2_S1_answers_P.jsonl"
        if stored.exists():
            refs["speed2_S1_stored"] = str(stored)
        return refs

    def run_block(self, cfg) -> dict:
        ok, why = self.gate(cfg)
        if not ok:
            res = {"config": cfg.name, "skipped": why}
            self.emit({"event": "block_skipped", **res})
            self.results[cfg.name] = res
            return res
        mdir = self.model_dir(cfg)
        res = {"config": cfg.name, "arm": cfg.arm, "desc": cfg.desc, "started_s": round(self.clock() - self.t0, 1), "gate": why}
        out_dir = Path(self.results_root) / cfg.name
        out_dir.mkdir(parents=True, exist_ok=True)
        for f in (cfg.env.get("R2_REPORT"), "/tmp/r2_gc_flag"):
            if f:
                try:
                    Path(f).unlink()
                except OSError:
                    pass
        srv = self.server_factory(cfg, mdir, self.python, self.log, str(out_dir / "sglang.log"))
        self.server = srv
        self.emit({"event": "block_start", "config": cfg.name, "spent_usd": round(self.spent(), 3), "cmd": " ".join(srv.cmd),
                   "env": {k: v for k, v in cfg.env.items()}})
        runner = None
        try:
            if cfg.fp8:
                v = self.fp8_wait()
                res["fp8_verified"] = v
                if not v.get("ok"):
                    raise RuntimeError(f"block-FP8 checkpoint failed verification: {str(v)[:300]}")
            res["gpu_before"] = S.wait_gpu_free()
            srv.start()
            go_file, abort_file = out_dir / "measure_go", out_dir / "measure_abort"
            for f in (go_file, abort_file):
                if f.exists():
                    f.unlink()
            measure_timeout = 0.0
            if cfg.steps:
                spec = {"config": cfg.name, "backend": cfg.backend, "sgl_url": srv.url, "work_dir": self.work_dir,
                        "c1_dir": self.c1_dir(), "out_dir": str(out_dir), "steps": cfg.steps, "params": self.plan.get("params", {}),
                        "refs": self.ref_paths(cfg), "go_file": str(go_file), "abort_file": str(abort_file),
                        "gc_flag": "/tmp/r2_gc_flag" if cfg.gc_flag else None, "fp8": cfg.fp8, "canary_min": cfg.canary_min}
                runner = S.Runner("r2measure", spec, str(out_dir / "measure.json"), python=self.runner_python, log=self.log).start()
                measure_timeout = min(float(self.plan.get("measure_timeout_s", 1500)), 2.0 * cfg.est_s + 120.0)
            res["boot_s"] = srv.wait_ready(float(self.plan.get("boot_timeout_s", 900)))
            info = srv.server_info()
            try:
                C.write_json(out_dir / "server_info.json", info)
            except Exception:  # noqa: BLE001
                pass
            res["server_args"] = {k: info.get(k) for k in S.KEEP_KEYS + ("skip_tokenizer_init", "enable_metrics", "gc_warning_threshold_secs",
                                                                       "mm_processor_worker_num", "mamba_track_interval",
                                                                       "keep_mm_feature_on_device", "mm_feature_transport", "cuda_graph_config",
                                                                       "disable_chunked_prefix_cache")
                                  if k in info}
            res["prefill_graph_backend_resolved"] = graph_prefill_backend(info)
            bad, warn = check_args_r2(info, want_args_r2(cfg, mdir))
            res["args_warnings"], res["args_problems"] = warn, bad
            if bad:
                abort_file.write_text("refused")
                raise RuntimeError("resolved server args refused: " + "; ".join(bad))
            self.emit({"event": "booted", "config": cfg.name, "boot_s": res["boot_s"], "problems": bad, "warnings": warn[:5],
                       "prefill_graph_backend_resolved": res["prefill_graph_backend_resolved"]})
            go_file.write_text("go")
            if runner is not None:
                res["measure"] = runner.wait(measure_timeout)
            aborted = bool((res.get("measure") or {}).get("aborted"))
            if cfg.vision and self.extra_cb is not None and not aborted:
                ok3, why3 = self.gate_extra(60.0 + 30.0 * len(cfg.vision))
                res["vision"] = self.extra_cb("vision", cfg, srv, out_dir) if ok3 else {"skipped": why3}
            if "--enable-metrics" in cfg.cmd(mdir):
                res["metrics"] = scrape_metrics(srv.url, out_dir / "metrics.txt")
        except BaseException as e:  # noqa: BLE001
            res["error"] = f"{type(e).__name__}: {str(e)[:600]}"
            res["server_tail"] = list(srv.tail)[-30:] if srv else None
            self.log(f"BLOCK {cfg.name} FAILED: {res['error']}")
        finally:
            if runner is not None and runner.alive():
                runner.kill()
            res["stop"] = srv.stop()
            res["log_scan"] = scan_log(out_dir / "sglang.log")
            rep = cfg.env.get("R2_REPORT")
            if rep and Path(rep).exists():
                try:
                    lines = [json.loads(x) for x in Path(rep).read_text().splitlines() if x.strip()]
                    res["patch_report"] = {"n": len(lines), "events": lines[:6] + lines[-6:]}
                    (out_dir / "patch_report.jsonl").write_text(Path(rep).read_text())
                except Exception as e:  # noqa: BLE001
                    res["patch_report"] = {"error": str(e)[:100]}
            res["ended_s"] = round(self.clock() - self.t0, 1)
            res["spent_usd"] = round(self.spent(), 3)
            self.server = None
        self.results[cfg.name] = res
        C.write_json(out_dir / "block.json", res)
        self.commit()
        self.emit({"event": "block_end", "config": cfg.name, "spent_usd": res["spent_usd"], "error": res.get("error"), "result": res})
        return res

    # -- conditional follow-up blocks -------------------------------------------------------------------------
    @staticmethod
    def verdict_of_bundle(res: dict) -> dict:
        """What a bundle block showed: booted? full in effect? score endpoint ok? parity sane? gc lines?"""
        m = res.get("measure") or {}
        steps = m.get("steps") or {}
        pv = (steps.get("parity") or {}).get("parity_vs_r2_a_same_session") or {}
        err = (res.get("error") or "") + " " + " ".join(res.get("server_tail") or [])
        resolved = str(res.get("prefill_graph_backend_resolved")).lower()
        score_bad = any("score" in str(v).lower() for v in (m.get("errors") or {}).values()) or \
            ((steps.get("canary") or {}).get("n_missing", 0) > 20)
        return {"booted": "boot_s" in res and not res.get("error"), "err": err, "full_in_effect": "full" in resolved,
                "chunked_assert": ("chunked" in err.lower() and "prefix" in err.lower()),
                "aborted": m.get("aborted"), "step_errors": m.get("errors") or {}, "score_bad": bool(score_bad),
                "agree": pv.get("argmax_agree"), "gc_lines": (res.get("log_scan") or {}).get("gc", {}).get("n", 0)}

    def follow_ups(self, name: str, res: dict) -> list:
        """Blocks to insert right after `name` (decided from what the block showed)."""
        out = []
        if name in ("r2_b", "r2_b_dcpc"):
            v = self.verdict_of_bundle(res)
            broken = (not v["booted"]) or (not v["full_in_effect"]) or v["aborted"] or v["step_errors"] or \
                (v["agree"] is not None and v["agree"] < 0.99)
            if v["score_bad"]:        # /v1/score refused without a tokenizer: later bundle blocks read through /generate instead
                for n in ("r2_b_dcpc", "r2_b_nofull"):
                    self.configs[n] = _replace_cfg(self.configs[n], backend="generate")
                self.notes.append("bundle: /v1/score failed (see the block): the later bundle variants read through /generate (input_ids)")
            if broken:
                if name == "r2_b" and v["chunked_assert"]:
                    out.append("r2_b_dcpc")
                else:
                    out.append("r2_b_nofull")
                self.notes.append(f"{name}: full-graph prefill not usable as asked (booted={v['booted']}, resolved="
                                  f"{res.get('prefill_graph_backend_resolved')!r}, aborted={v['aborted']!r}, step errors={v['step_errors']}, "
                                  f"agree={v['agree']}, error={(res.get('error') or '')[:240]!r}); next: {out[-1]}")
            elif v["gc_lines"]:
                self._queue_gc(name)
                out.append("r2_b_gc")
                self.notes.append(f"{name}: {v['gc_lines']} GC log lines at the 5 ms threshold: running r2_b_gc")
            if broken and v["gc_lines"]:
                self.notes.append(f"{name}: {v['gc_lines']} GC log lines: r2_b_gc follows the fallback if it passes")
        if name == "r2_b_nofull":
            v = self.verdict_of_bundle(res)
            if v["gc_lines"] and v["booted"] and not v["aborted"]:
                self._queue_gc(name)
                out.append("r2_b_gc")
        return out

    def _queue_gc(self, base_name: str):
        """r2_b_gc = the bundle variant that just passed + gc.freeze() after the warm-up (latency and throughput only)."""
        base = self.configs[base_name]
        self.configs["r2_b_gc"] = _replace_cfg(base, name="r2_b_gc", desc=f"{base.name} + gc.freeze() after the warm-up",
                                               env={**base.env, **patch_env("bgc", gc_freeze=True)}, steps=["latency", "throughput"],
                                               est_s=300, gc_flag=True, canary_min=0.0)

    def run(self) -> dict:
        while self.queue:
            name = self.queue.pop(0)
            if name in self.ran:
                continue
            cfg = self.configs[name]
            if self.spent() >= self.hard_stop:
                self.emit({"event": "hard_stop", "spent_usd": round(self.spent(), 3)})
                break
            res = self.run_block(cfg)
            self.ran.add(name)
            if name == "r2_a" and (res.get("error") or not (Path(self.results_root) / "r2_a" / "answers_P.jsonl").exists()):
                # no same-session reference: nothing after it can be judged, so stop the window here instead of spending on it
                self.notes.append(f"r2_a (the reference) failed: {str(res.get('error') or (res.get('measure') or {}).get('errors'))[:300]}; window stopped")
                self.emit({"event": "reference_failed", "error": res.get("error")})
                break
            for f in reversed(self.follow_ups(name, res)):
                if f not in self.ran and f not in self.queue:
                    self.queue.insert(0, f)
        return {"results": self.results, "spent_usd": round(self.spent(), 3), "wall_s": round(self.clock() - self.t0, 1),
                "notes": self.notes}


def _replace_cfg(cfg, **kw):
    import dataclasses
    return dataclasses.replace(cfg, **kw)
