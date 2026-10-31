"""fastcore.engine: the HF fast-path decider behind API v1 (arms A0-A3 of hosting/SPEED1_DESIGN.md), glue of
fastcore.readout (request -> work items -> answers), fastcore.graphs (model runner) and fastcore.batcher (one GPU
worker). The HTTP host owns sockets, auth, Modal and model loading; it calls only:

  model, tok, info = load_merged(adapter_dir)              # optional helper = core.boot_gpu's load + merge
  report = fp8.quantize_model(model)                        # A3 boot only, BEFORE FastEngine
  eng = FastEngine(model, tok, flags={"legacy": True}, quantization=None | "fp8")
  boot = eng.boot()                                         # graphs (warm-up, shared pool, self-check) + warm requests
  boot = eng.boot(pool="private")                           # reboot after a shared-pool boot died (device assert)
  eng.decide(req) -> API v1 response (minus server_ms)      # RequestError -> 400, EngineClosed -> 503
  eng.set_flags({...}) -> flags view                         # POST /admin/config
  eng.health() -> dict                                       # merge into GET /health
  eng.close()

Cost guards: none needed here (no Modal, no network, no paid call). CPU-tested end to end on a tiny random Qwen3.5
hybrid model with the C1 tokenizer (hosting/tests/test_fastcore_engine.py); CUDA capture only runs on the GPU.
"""
from __future__ import annotations

import hashlib
import json
import time

import torch

from . import readout as R
from .batcher import BatchingEngine, flags_view, effective_flags
from .graphs import FastGraphs, PAD_MULTIPLE

dio = R.dio
BASE = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
EXAMPLE = {"state": "Customer message:\nMy card payment was declined at the shop this morning.",
           "questions": {"q0": {"type": "noul", "instructions": "Is the customer reporting a declined payment?"},
                         "q1": {"type": "choice", "instructions": "Which label describes this message?",
                                "options": ["declined card payment", "card arrival", "refund request"]}}}


def load_merged(adapter_dir, dev: str = "cuda", base: str = BASE, revision: str = REVISION):
    """C1 as hosting/modal_direct_host.boot_gpu loads it: decoder_io.load (layout/style/revision from the adapter's
    train_meta.json), merge_and_unload in BF16, eval, use_cache flags as the old host set them. PRISM-X refused."""
    model, tok, info = dio.load(base, dev, adapter=str(adapter_dir), revision=revision, return_info=True)
    if info.get("prism_x"):
        raise SystemExit("PRISM-X model: the fast path (CUDA graphs) does not support it")
    model = model.merge_and_unload()
    model.eval()
    for c in (model.config, getattr(model.config, "text_config", None)):
        if c is not None:
            c.use_cache = True
    if getattr(model, "generation_config", None) is not None:
        model.generation_config.use_cache = True
    return model, tok, info


class FastEngine:
    """API v1 decider on one model. Thread-safe: any number of HTTP threads may call decide() at once."""

    def __init__(self, model, tok, device=None, flags: dict | None = None, temps: dict | None = None, ro=None,
                 emulate_graphs: bool | None = None, quantization: str | None = None, log=print,
                 expect_layout=("schema_branch_mark", "cygnet")):
        """expect_layout: decoder_io's (LAYOUT, STYLE) must be C1's (decoder_io.load / load_merged set them from the
        adapter's train_meta.json); a host that loads the model another way and forgets would serve wrong prompts.
        None skips the check (another adapter)."""
        if expect_layout is not None and (dio.LAYOUT, dio.STYLE) != tuple(expect_layout):
            raise RuntimeError(f"decoder_io layout/style {(dio.LAYOUT, dio.STYLE)} != expected {tuple(expect_layout)}: "
                               f"load C1 with decoder_io.load(..., adapter=...) (or load_merged) first")
        model.eval()
        self.model, self.tok, self.log = model, tok, log
        self.ro = ro if ro is not None else dio.Readout(tok)  # full vocabulary scan: sets the two-letter labels
        if R.max_options() < R.MAX_OPTIONS:
            raise RuntimeError(f"two-letter labels: only {R.max_options()} options readable (Readout not built?)")
        self.temps = dict(R.TEMPS if temps is None else temps)
        self.quantization = quantization
        self.runner = FastGraphs(model, tok, device=device, emulate=emulate_graphs)
        self.batcher = BatchingEngine(self.runner, flags, tokenizer=tok,
                                      prepare=lambda items: R.prepare_items(self.ro, self.tok, items))
        self.boot_report = None
        self.t_created = time.time()

    # ------------------------------------------------------------------ boot
    def warmup_eager(self, max_tokens: int = 8192, batch_sizes=(1, 2)) -> float:
        """Eager forwards at every PAD_MULTIPLE length up to max_tokens per batch size (fla/Triton autotune happens
        here, not in the first long request). Filler ids, no task data."""
        t0 = time.time()
        base = self.tok("The office opens at nine and closes at five on weekdays. " * 8, add_special_tokens=False)["input_ids"]
        with torch.no_grad():
            for L in range(PAD_MULTIPLE, max_tokens + 1, PAD_MULTIPLE):
                seq = [base[i % len(base)] for i in range(L - 8)]
                for b in batch_sizes:
                    self.runner._eager_h([seq] * b)
        if self.runner.device.type == "cuda":
            torch.cuda.synchronize(self.runner.device)
        return round(time.time() - t0, 2)

    def boot(self, graphs: bool = True, coverage=None, legacy_shapes: bool = True, reserve_gb: float = 6.0,
             tol_prob: float = 0.02, eager_warmup: dict | None = None, warm_requests: int = 3, free_gb=None,
             pool: str = "shared") -> dict:
        """Graphs (FastGraphs.boot: warm-up, one shared pool largest first, self-check, fallback, freeze), eager
        warm-up of the uncovered lengths (default {"max_tokens": 8192, "batch_sizes": [1, 2]}; {} skips it), then
        warm_requests EXAMPLE calls under every flag mode so the first timed request is not the first one."""
        t0 = time.time()
        rep = {}
        if graphs:
            rep["graphs"] = self.runner.boot(coverage=coverage, legacy=legacy_shapes, reserve_gb=reserve_gb,
                                             tol_prob=tol_prob, free_gb=free_gb, pool=pool, log=self.log)
        else:
            self.runner.freeze()
            rep["graphs"] = {"mode": "eager_only", "n_graphs": 0}
        ew = {"max_tokens": 8192, "batch_sizes": [1, 2]} if eager_warmup is None else eager_warmup
        rep["eager_warmup_s"] = self.warmup_eager(ew["max_tokens"], tuple(ew["batch_sizes"])) if ew else 0.0
        keep = self.batcher.flags
        try:
            for mode in ({"legacy": True}, {"legacy": False, "cross_batch": False}, {"legacy": False, "cross_batch": True}):
                self.batcher.set_flags(mode)
                for _ in range(warm_requests):
                    self.decide(EXAMPLE)
        finally:
            self.batcher.set_flags(keep)
        rep["boot_s"] = round(time.time() - t0, 2)
        self.boot_report = rep
        return rep

    # ------------------------------------------------------------------ serving
    def decide(self, req, timeout: float | None = 120.0) -> dict:
        """One API v1 request -> the API v1 response (the host adds "server_ms"). Raises RequestError (400) on a bad
        request, EngineClosed (503) after close(), concurrent.futures.TimeoutError after `timeout` s."""
        t0 = time.perf_counter()
        named = R.parse_v1(req)
        f = effective_flags(self.batcher.flags)
        outside = f["tokenize_outside_lock"]
        items = R.build_items(self.ro, named, choice_views=f["choice_views"], render=outside)
        if outside:
            R.tokenize_items(self.tok, items)
        t1 = time.perf_counter()
        res = self.batcher.run(items, tokenize_ms=(t1 - t0) * 1000, timeout=timeout)
        answers, usage = R.combine(named, items, res.logits, self.temps, return_views=bool(req.get("return_views")))
        t2 = time.perf_counter()
        return {"id": req.get("id"), "answers": answers, "usage": usage,
                "timing": {**res.timing, "total_ms": round((t2 - t0) * 1000, 3)}, "engine": "hf", "path": res.path,
                "batch_rows": res.batch_rows, "shapes": res.shapes}

    def set_flags(self, update: dict) -> dict:
        """POST /admin/config {"flags": update}: validated, all or nothing (ValueError -> 400). Returns the flags view."""
        if not isinstance(update, dict):
            raise R.RequestError('"flags" must be an object')
        try:
            return self.batcher.set_flags(update)
        except ValueError as e:
            raise R.RequestError(str(e)) from e

    def flush(self) -> dict:
        """POST /admin/flush: the HF engine has no prefix cache (no-op)."""
        return {"ok": True, "flushed": 0, "note": "HF engine: no prefix cache"}

    def config_sha256(self) -> str:
        f = effective_flags(self.batcher.flags)
        cfg = {"flags": f, "readout": R.readout_info(), "temps": self.temps, "quantization": self.quantization,
               "graphs": {"pool": self.runner.pool_mode, "shapes": [list(s) for s in self.runner.captured()]}}
        return hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()

    def health(self) -> dict:
        """The engine's part of GET /health (the host adds model, adapter_sha256, base, revision, gpu, region, boot_s).
        ok is false while the batcher reports a problem (worker stopped or dead, e.g. a CUDA-fatal error; a forward
        stuck longer than its stall_s)."""
        problems = self.batcher.problems()
        return {"ok": not problems, "problems": problems, "engine": "hf", "api": R.API_VERSION,
                "readout": R.readout_info(),
                "flags": flags_view(self.batcher.flags), "config_sha256": self.config_sha256(),
                "quantization": self.quantization, "graphs": self.runner.health(), "batcher": self.batcher.stats(),
                "queue": self.batcher.queued()}

    def close(self, timeout: float = 30.0) -> bool:
        return self.batcher.shutdown(wait=True, timeout=timeout)
