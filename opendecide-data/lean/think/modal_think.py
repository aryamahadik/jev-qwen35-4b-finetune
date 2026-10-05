"""A17 phase B1: the think path served on a Modal H100, and the B1 speed / parity benchmark. Each paid run needs the
owner's GO (A17 "Paid steps"). Nothing here trains, tunes a router or reads OHS / Decision Index / ejs-5 / JevBench.

  python think/modal_think.py --dry-run             # CPU only, no Modal, no weights: inputs, prompts, extraction,
                                                    # DEER loop (fake engine), engine configs, cost estimate, caps
  python think/modal_think.py --estimate            # cost estimate of the default plan only
  modal run think/modal_think.py::bench             # the B1 benchmark (H100, ~$3-4 expected, refuses above $15)
  python think/modal_think.py --score <run dir>     # re-score saved results locally (parity vs the L4)

Think path (one engine per config, SGLang 0.5.20, official image lmsysorg/sglang:v0.5.20-cu130):
  Qwen/Qwen3.5-4B @ 851bf6e8 (the base: LoRA off), thinking on, prefix (radix) cache OFF (R_serving 5: the spec-decode
  + hybrid prefix-cache bug), CUDA graphs on (SGLang default; decode graphs up to batch 64), seed 0.
  Configs: bf16_dflash, fp8_dflash (online FP8 W8A8), bf16_nospec, fp8_nospec. Drafter z-lab/Qwen3.5-4B-DFlash @
  9a1996cc (Apache-2.0, block 16 = its trained block size; --block 8 for high concurrency).
  Why SGLang, not vLLM: R_serving lists both, but the drafter's own card documents SGLang DFLASH only, and its vLLM
  route (vllm-project/vllm#40898, sliding-window DFlash drafter) was closed unmerged (checked 5 Oct 2026).
  Prompt and answer extraction: think_engine.py (= bench/think_check/think_run.py / think_rows.py).
  Thinking caps 300 / 1,024 (and 768 = the L4 A17-B0 setting, for parity); DEER-style early exit = chunked generation
  + answer-confidence probe (think_engine.py docstring), since SGLang has no in-engine early exit.
Fast path (same container, same H100, its own process, after the think engine is up): fast_timing.py in a second
  Python env (/opt/fastpath, modal_od.PINNED35 = C1's own stack): C1 = /vol/models/q35_4b_main500k merged, one-pass
  readout through decoder_io.GraphRunner, p50/p95 ms per decision at batch 1 and batched.
Benchmark per config: speed at batch 1 for 300 / 1,024 / 5,000 new tokens (TTFT, decode tok/s, wall, accept length),
  batched throughput (8 and 32 concurrent), end-to-end think path latency at caps 300 / 1,024 (+ DEER), and the
  100 SQuAD2 parity items (think/data/squad2_parity100.jsonl: items the L4 already answered in A17-B0; no new items)
  at 768 and 1,024 tokens, plus DEER at 1,024. Gold never goes to Modal: scoring is local (score_run).
Caps: a container stops starting new steps at --max-minutes (default 25) and Modal kills it at HARD_MAX_MIN (30).
  The launcher refuses to start if the expected cost or the worst case (every container at its kill time) is above
  --max-usd (default 15, and never above COST_CAP_USD = 15).
"""
from __future__ import annotations

import ast
import json
import math
import sys
import time
from pathlib import Path

import modal

THINK = Path(__file__).resolve().parent
LEAN = THINK.parent
DATA = THINK / "data"
RUNS = THINK / "runs"

BASE, BASE_REV = "Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
DRAFT, DRAFT_REV = "z-lab/Qwen3.5-4B-DFlash", "9a1996ccf887b79ab3af4fcbf8c1d1f4b5658bcf"
C1_DIR = "/vol/models/q35_4b_main500k"
C1_SHA = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"  # adapter_model.safetensors
SGLANG_IMAGE = "lmsysorg/sglang:v0.5.20-cu130"  # index digest sha256:06e4f2ed21afde4ff513cda65070124e727ba23ccaeff7712b8c40e1097d611f
SGLANG_VERSION = "0.5.20"  # checked inside the container before anything runs
GPU = "H100!"  # exactly an H100 (no silent upgrade), as modal_od
PRICE_GPU_H = 4.09  # our H100 budget rate (Modal list $3.95/h; FAST_THINK_PLAN 6)
OVERHEAD = 1.10  # CPU + memory billed next to the GPU
HARD_MAX_MIN = 30  # Modal timeout per container (hard kill)
COST_CAP_USD = 15.0  # refuse to start above this, whatever --max-usd says
CONFIGS = {  # run order: the ship candidate first (it also fills the HF cache on the Volume and runs the fast path)
    "bf16_dflash": {"quant": None, "draft": True},
    "fp8_dflash": {"quant": "fp8", "draft": True},
    "bf16_nospec": {"quant": None, "draft": False},
    "fp8_nospec": {"quant": "fp8", "draft": False},
}
DEFAULT_PLAN = {"speed_budgets": [300, 1024, 5000], "n_speed": 10, "concurrency": [8, 32], "conc_tokens": 1024,
                "parity_budgets": [768, 1024], "deer_budget": 1024, "e2e_caps": [300, 1024], "block": 16,
                "fast": True, "fast_n": 200, "max_minutes": 25, "mem_fraction": 0.55}
# Every ServerArgs field this file passes, checked against the sglang 0.5.20 wheel (srt/arg_groups/fields/*.py) on
# 5 Oct 2026; --dry-run refuses a config that uses any other name.
SGLANG_FIELDS = {"model_path", "revision", "dtype", "quantization", "trust_remote_code", "context_length",
                 "mem_fraction_static", "disable_radix_cache", "random_seed", "max_running_requests", "log_level",
                 "cuda_graph_max_bs_decode", "speculative_algorithm", "speculative_draft_model_path",
                 "speculative_draft_model_revision", "speculative_dflash_block_size"}


def engine_kwargs(config: str, block: int = 16, mem_fraction: float = 0.55) -> dict:
    """sglang.Engine(**kwargs) of one config. FP8 = online W8A8 of the target (the drafter follows the target's
    quantization, SGLang's default); speculative decoding is lossless, so only the target precision moves accuracy."""
    c = CONFIGS[config]
    kw = {"model_path": BASE, "revision": BASE_REV, "dtype": "bfloat16", "trust_remote_code": True,
          "context_length": 16384, "mem_fraction_static": mem_fraction, "disable_radix_cache": True, "random_seed": 0,
          "max_running_requests": 128, "cuda_graph_max_bs_decode": 64, "log_level": "warning"}
    if c["quant"]:
        kw["quantization"] = c["quant"]
    if c["draft"]:
        kw.update(speculative_algorithm="DFLASH", speculative_draft_model_path=DRAFT,
                  speculative_draft_model_revision=DRAFT_REV, speculative_dflash_block_size=int(block))
    bad = set(kw) - SGLANG_FIELDS
    if bad:
        raise ValueError(f"unchecked SGLang fields {sorted(bad)}")
    return kw


def pinned35() -> list:
    """modal_od.PINNED35 (C1's own software stack), read as text from modal_od.py: nothing of modal_od is imported."""
    tree = ast.parse((LEAN / "modal_od.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "PINNED35" for t in node.targets):
            return node.value.func.value.value.split()  # """...""".split()
    raise RuntimeError("PINNED35 not found in modal_od.py")


app = modal.App("opendecide-think")
vol = modal.Volume.from_name("opendecide", create_if_missing=True)  # HF cache (/vol/hf) and C1 (/vol/models)
SECRETS = [modal.Secret.from_name("opendecide-keys")]
# Defined the same way locally and in the container (as modal_od's images): in the container the built image is used
# and modal_od.py is absent, so the pin list is empty there.
_FAST_PINS = " ".join(pinned35()) if (LEAN / "modal_od.py").exists() else ""
think_image = (
    modal.Image.from_registry(SGLANG_IMAGE)
    .run_commands("PIP_BREAK_SYSTEM_PACKAGES=1 python3 -m pip install --no-cache-dir uv==0.12.23",
                  "uv venv --python 3.12.10 /opt/fastpath",
                  f"uv pip install --no-cache --python /opt/fastpath/bin/python {_FAST_PINS}")
    .env({"HF_HOME": "/vol/hf", "HF_HUB_ENABLE_HF_TRANSFER": "0", "TOKENIZERS_PARALLELISM": "false"})
    .add_local_file(LEAN / "decoder_io.py", "/root/lean/decoder_io.py")
    .add_local_file(THINK / "think_engine.py", "/root/think/think_engine.py")
    .add_local_file(THINK / "fast_timing.py", "/root/think/fast_timing.py")
    .add_local_file(DATA / "squad2_parity100.jsonl", "/root/think/data/squad2_parity100.jsonl")
    .add_local_file(DATA / "fast_rows_dev200.jsonl", "/root/think/data/fast_rows_dev200.jsonl")
)


# ----------------------------------------------------------------------------------------------- container side
def _pct(xs, q):
    xs = sorted(x for x in xs if x is not None)
    return round(xs[min(len(xs) - 1, int(len(xs) * q))], 4) if xs else None


def _speed(engine, prompts, budget, sampling, stop_at):
    """Batch 1, one request at a time: TTFT (a 1-token request) then the full request of up to `budget` new tokens
    (natural stop at EOS; no stop strings). Decode rate = (tokens - 1) / (wall - TTFT)."""
    recs = []
    for p in prompts:
        if time.time() > stop_at:
            break
        t0 = time.perf_counter()
        engine.generate(prompt=p, sampling_params={**sampling, "max_new_tokens": 1})
        ttft = time.perf_counter() - t0
        t0 = time.perf_counter()
        o = engine.generate(prompt=p, sampling_params={**sampling, "max_new_tokens": int(budget)})
        wall = time.perf_counter() - t0
        m = o.get("meta_info") or {}
        k = int(m.get("completion_tokens") or 0)
        recs.append({"tokens": k, "wall_s": round(wall, 4), "ttft_s": round(ttft, 4),
                     "decode_tok_s": round((k - 1) / max(wall - ttft, 1e-6), 1) if k > 1 else None,
                     "accept_len": m.get("spec_accept_length")})
    rate = _pct([r["decode_tok_s"] for r in recs], 0.5)
    ttft = _pct([r["ttft_s"] for r in recs], 0.5)
    return {"n": len(recs), "partial": len(recs) < len(prompts), "decode_tok_s_p50": rate, "ttft_s_p50": ttft,
            "wall_s_p50": _pct([r["wall_s"] for r in recs], 0.5), "wall_s_p95": _pct([r["wall_s"] for r in recs], 0.95),
            "tokens_p50": _pct([r["tokens"] for r in recs], 0.5),
            "share_reached_budget": round(sum(r["tokens"] >= budget for r in recs) / max(1, len(recs)), 3),
            "accept_len_p50": _pct([r["accept_len"] for r in recs], 0.5),
            "wall_at_budget_est_s": round(ttft + budget / rate, 3) if rate and ttft is not None else None,
            "records": recs}


def _batched(engine, prompts, conc, tokens, sampling):
    ps = [prompts[i % len(prompts)] for i in range(conc)]
    t0 = time.perf_counter()
    outs = engine.generate(prompt=ps, sampling_params=[{**sampling, "max_new_tokens": int(tokens)}] * conc)
    wall = time.perf_counter() - t0
    tot = sum(int((o.get("meta_info") or {}).get("completion_tokens") or 0) for o in outs)
    return {"concurrency": conc, "wall_s": round(wall, 3), "tokens": tot, "agg_tok_s": round(tot / wall, 1),
            "per_request_tok_s": round(tot / wall / conc, 1),
            "accept_len_p50": _pct([(o.get("meta_info") or {}).get("spec_accept_length") for o in outs], 0.5)}


def _provenance():
    import subprocess
    import torch
    out = {"gpu": torch.cuda.get_device_name(), "torch": torch.__version__}
    for mod in ("sglang", "transformers", "flashinfer"):
        try:
            out[mod] = __import__(mod).__version__
        except Exception as e:  # noqa: BLE001
            out[mod] = f"unavailable: {type(e).__name__}"
    fz = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True)
    out["pip_freeze"] = fz.stdout.split("\n")
    return out


def _fast_path(plan, seconds):
    """fast_timing.py in /opt/fastpath (C1's PINNED35 stack), as a separate process on this GPU."""
    import os
    import subprocess
    # no vol.reload(): C1 has been on the Volume for days, and a reload with the engine's files open would fail
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "VIRTUAL_ENV")}
    cmd = ["/opt/fastpath/bin/python", "/root/think/fast_timing.py", "--adapter", C1_DIR, "--sha256", C1_SHA,
           "--rows", "/root/think/data/fast_rows_dev200.jsonl,/root/think/data/squad2_parity100.jsonl",
           "--out", "/tmp/fast.json", "--n", str(plan["fast_n"]), "--lean", "/root/lean"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=max(60, seconds), env=env)
    if r.returncode != 0:
        return {"error": f"exit {r.returncode}", "stderr_tail": r.stderr[-3000:]}
    return json.loads(Path("/tmp/fast.json").read_text())


@app.function(image=think_image, gpu=GPU, volumes={"/vol": vol}, secrets=SECRETS, timeout=HARD_MAX_MIN * 60)
def run_config(config: str, plan: dict, run: str) -> dict:
    t_start = time.time()
    deadline = t_start + min(plan["max_minutes"], HARD_MAX_MIN - 2) * 60
    sys.path[:0] = ["/root/think", "/root/lean"]
    import sglang
    if sglang.__version__ != SGLANG_VERSION:
        raise SystemExit(f"sglang {sglang.__version__} != pinned {SGLANG_VERSION}")
    from transformers import AutoTokenizer
    import decoder_io as dio
    import think_engine as te
    items = [json.loads(x) for x in open("/root/think/data/squad2_parity100.jsonl") if x.strip()]
    res = {"config": config, "run": run, "plan": plan, "engine_kwargs": engine_kwargs(config, plan["block"],
           plan["mem_fraction"]), "steps": {}, "skipped": [], "errors": {}}
    t0 = time.time()
    try:
        engine = sglang.Engine(**res["engine_kwargs"])
    except Exception as e:  # noqa: BLE001  (e.g. a config this SGLang build refuses): report it, run nothing
        res["errors"]["engine_start"] = f"{type(e).__name__}: {e}"[:3000]
        res["wall_s"] = round(time.time() - t_start, 1)
        return res
    res["engine_start_s"] = round(time.time() - t0, 1)
    try:
        vol.commit()  # the HF cache now holds the base and the drafter for the next containers
    except Exception as e:  # noqa: BLE001
        res["errors"]["vol_commit"] = repr(e)
    res["provenance"] = _provenance()
    res["provenance"]["server_args"] = str(getattr(engine, "server_args", ""))[:8000]  # radix off, graphs, spec
    tok = AutoTokenizer.from_pretrained(BASE, revision=BASE_REV)
    tp = te.ThinkPath(te.SGLBackend(engine), tok, dio)
    prompts = [p["prompt"] for p in tp.prepare(items)]  # also checks every user message against the input file
    sub = items[: plan["n_speed"]]

    def step(name, fn, need_s=60):
        if time.time() + need_s > deadline:
            res["skipped"].append(name)
            return
        t = time.time()
        try:
            res["steps"][name] = fn()
        except Exception as e:  # noqa: BLE001  (one failed step must not lose the others)
            res["errors"][name] = f"{type(e).__name__}: {e}"[:2000]
        res.setdefault("step_s", {})[name] = round(time.time() - t, 1)

    step("sanity", lambda: te.SGLBackend(engine).generate([prompts[0]], [{**te.SAMPLING, "max_new_tokens": 16}]))
    for b in plan["parity_budgets"][:1]:  # 768 = the L4 A17-B0 setting: the parity check proper
        step(f"parity_{b}", lambda b=b: tp.run(items, b, batch=0))
    for b in plan["speed_budgets"]:
        step(f"speed_bs1_{b}", lambda b=b: _speed(engine, prompts[: plan["n_speed"]], b, te.SAMPLING, deadline - 60))
    for b in plan["e2e_caps"]:
        step(f"e2e_bs1_cap{b}", lambda b=b: tp.run(sub, b, batch=1))
    step(f"e2e_bs1_deer{plan['deer_budget']}", lambda: tp.run(sub, plan["deer_budget"], deer=te.DEER, batch=1))
    if plan["fast"] and config == "bf16_dflash":
        step("fast_path", lambda: _fast_path(plan, deadline - time.time() - 30), need_s=300)
    for b in plan["parity_budgets"][1:]:
        step(f"parity_{b}", lambda b=b: tp.run(items, b, batch=0))
    step(f"parity_deer{plan['deer_budget']}", lambda: tp.run(items, plan["deer_budget"], deer=te.DEER, batch=0))
    for c in plan["concurrency"]:
        step(f"batched_c{c}", lambda c=c: _batched(engine, prompts, c, plan["conc_tokens"], te.SAMPLING))
    engine.shutdown()
    res["wall_s"] = round(time.time() - t_start, 1)
    out = Path(f"/vol/think_runs/{run}/{config}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res))
    vol.commit()
    return res


# ----------------------------------------------------------------------------------------------- cost and caps
# [E] H100 rates from R_serving 7 (batch-1 decode tok/s) and 2 (batched aggregate tok/s); no Qwen3.5-4B H100 number is
# published, so the estimate is deliberately pessimistic: every request is assumed to run to its full token budget.
RATES = {"bf16_nospec": (250, 4000), "fp8_nospec": (330, 5000), "bf16_dflash": (800, 8000), "fp8_dflash": (950, 9000)}
START_S = 300  # container start with the 15 GB image + weights (first run downloads ~10 GB to /vol/hf) + graphs [E]
FAST_S = 300  # C1 load + merge + Triton warm-up + graph capture + timing [E]
SAFETY = 1.3


def estimate(plan: dict, configs: list) -> dict:
    n, P = plan["n_speed"], 100
    per = {}
    for c in configs:
        r1, rb = RATES[c]
        s = START_S
        s += sum(n * (b / r1 + 0.1) for b in plan["speed_budgets"])
        s += sum(n * (b / r1 + 0.2) for b in plan["e2e_caps"]) + n * (plan["deer_budget"] / r1 + 1.0)
        s += sum(P * b / rb + 5 for b in plan["parity_budgets"]) + 1.5 * P * plan["deer_budget"] / rb
        s += sum(cc * plan["conc_tokens"] / rb + 5 for cc in plan["concurrency"])
        s += FAST_S if plan["fast"] and c == "bf16_dflash" else 0
        per[c] = round(min(s * SAFETY, min(plan["max_minutes"], HARD_MAX_MIN) * 60 + 300), 1)
    usd_s = PRICE_GPU_H * OVERHEAD / 3600
    exp = sum(per.values()) * usd_s
    worst = len(configs) * HARD_MAX_MIN * 60 * usd_s
    return {"gpu": GPU, "usd_per_gpu_hour": PRICE_GPU_H, "overhead": OVERHEAD, "safety": SAFETY,
            "gpu_seconds_by_config": per, "gpu_minutes_expected": round(sum(per.values()) / 60, 1),
            "usd_expected": round(exp, 2), "usd_worst_case": round(worst, 2),
            "worst_case_rule": f"{len(configs)} container(s) x {HARD_MAX_MIN} min Modal timeout",
            "image_build": "one-time CPU build of the 15 GB SGLang image + the fast-path venv (~$0.1) [E]"}


def check_caps(est: dict, max_usd: float) -> list:
    """Reasons to refuse (empty = OK to start)."""
    cap = min(float(max_usd), COST_CAP_USD)
    why = []
    if est["usd_expected"] > cap:
        why.append(f"expected ${est['usd_expected']} > cap ${cap}")
    if est["usd_worst_case"] > cap:
        why.append(f"worst case ${est['usd_worst_case']} ({est['worst_case_rule']}) > cap ${cap}")
    return why


def make_plan(**over) -> dict:
    plan = {**DEFAULT_PLAN, **{k: v for k, v in over.items() if v is not None}}
    if plan["max_minutes"] > HARD_MAX_MIN - 2:
        raise SystemExit(f"--max-minutes {plan['max_minutes']} > {HARD_MAX_MIN - 2} (the Modal timeout is {HARD_MAX_MIN})")
    return plan


# ----------------------------------------------------------------------------------------------- local scoring
def _mcnemar_p(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(math.comb(n, k) for k in range(min(b, c) + 1)) / 2 ** n)


def _ok(rec, g) -> bool:
    """think_eval.py (A17-B0) rule: a letter outside the shown options is no answer; else yes-letter == gold."""
    return bool(rec["parsed"]) and ((rec["pred_key"] == g["yes_key"]) == bool(g["gold"]))


def _acc(step, gold) -> dict:
    recs = [r for r in step["records"] if r["id"] in gold]
    ok = {r["id"]: _ok(r, gold[r["id"]]) for r in recs}
    return {"n": len(recs), "acc": round(100 * sum(ok.values()) / max(1, len(recs)), 1),
            "parsed": round(sum(r["parsed"] for r in recs) / max(1, len(recs)), 3),
            "think_tokens_mean": round(sum(r["think_tokens"] for r in recs) / max(1, len(recs)), 1),
            "capped_share": round(sum(bool(r["capped"]) for r in recs) / max(1, len(recs)), 3),
            "exit": {e: sum(r["exit"] == e for r in recs) for e in ("natural", "budget", "deer")},
            "probes_mean": round(sum(r["probes"] for r in recs) / max(1, len(recs)), 2), "_ok": ok}


def _paired(a: dict, b: dict) -> dict:
    ids = sorted(set(a) & set(b))
    n10 = sum(a[i] and not b[i] for i in ids)
    n01 = sum(b[i] and not a[i] for i in ids)
    return {"n": len(ids), "diff_pts": round(100 * (n10 - n01) / max(1, len(ids)), 1), "a_only": n10, "b_only": n01,
            "mcnemar_p": round(_mcnemar_p(n10, n01), 4)}


def score_run(run_dir) -> dict:
    run_dir = Path(run_dir)
    gold = {g["id"]: g for g in map(json.loads, open(DATA / "squad2_parity100_local.jsonl"))}
    l4 = {i: bool(g["l4"]["ok"]) for i, g in gold.items()}
    out = {"run": run_dir.name, "l4_768": {"acc": round(100 * sum(l4.values()) / len(l4), 1), "n": len(l4)},
           "configs": {}, "b1_checks": {}}
    acc_ok = {}
    for f in sorted(run_dir.glob("*.json")):
        if f.stem not in CONFIGS:  # plan.json, summary.json
            continue
        r = json.loads(f.read_text())
        c, st = r["config"], r["steps"]
        row = {"engine_start_s": r.get("engine_start_s"), "skipped": r.get("skipped"), "errors": r.get("errors"),
               "speed_bs1": {k[len("speed_bs1_"):]: {x: v[x] for x in ("decode_tok_s_p50", "ttft_s_p50", "wall_s_p50",
                             "wall_at_budget_est_s", "tokens_p50", "accept_len_p50", "n", "partial")}
                             for k, v in st.items() if k.startswith("speed_bs1_")},
               "e2e_bs1_s_p50": {k[len("e2e_bs1_"):]: _pct([x["think_s"] + x["answer_s"] for x in v["records"]], 0.5)
                                 for k, v in st.items() if k.startswith("e2e_bs1_")},
               "batched": {k: {x: v[x] for x in ("agg_tok_s", "per_request_tok_s", "accept_len_p50")}
                           for k, v in st.items() if k.startswith("batched_")},
               "parity": {}}
        for k, v in st.items():
            if k.startswith("parity_"):
                a = _acc(v, gold)
                acc_ok[(c, k)] = a.pop("_ok")
                a["vs_l4_768"] = _paired(acc_ok[(c, k)], l4)
                row["parity"][k] = a
        if "fast_path" in st:
            fp = st["fast_path"]
            row["fast_path"] = {x: fp.get(x) for x in ("batch1", "batched", "per_state", "graph_vs_eager_max_abs_dprob",
                                                     "b1_rule_fast_p50_le_50ms", "error", "stderr_tail")}
        out["configs"][c] = row
    return _b1_checks(out, acc_ok)


def _b1_checks(out: dict, acc_ok: dict) -> dict:
    """A17 B1 pass rules where this benchmark measures them. Accuracy checks here use the 100 SQuAD2 parity items only,
    so they are INDICATIVE; the B1 rules' math-set checks (>= 85% of full-thinking accuracy at <= 1 s median, FP8 on
    clean dev items) need the clean math dev sets and are not run by this app."""
    cf, chk = out["configs"], out["b1_checks"]
    fp = (cf.get("bf16_dflash") or {}).get("fast_path") or {}
    if fp.get("batch1"):
        chk["fast_p50_ms"] = fp["batch1"]["p50_ms"]
        chk["fast_p50_le_50ms"] = fp["batch1"]["p50_ms"] <= 50.0
    for lo, hi in (("fp8_dflash", "bf16_dflash"), ("fp8_nospec", "bf16_nospec"), ("bf16_dflash", "bf16_nospec"),
                   ("fp8_dflash", "fp8_nospec")):
        for k in sorted({k for (c, k) in acc_ok if c == lo} & {k for (c, k) in acc_ok if c == hi}):
            p = _paired(acc_ok[(lo, k)], acc_ok[(hi, k)])
            chk[f"{lo}_vs_{hi}_{k}"] = p
            if lo.startswith("fp8") and hi.startswith("bf16"):
                p["fp8_loss_le_1pt_indicative"] = p["diff_pts"] >= -1.0
    for c, row in cf.items():
        sp = {b: v["decode_tok_s_p50"] for b, v in row["speed_bs1"].items()}
        base = cf.get(c.replace("dflash", "nospec"), {}).get("speed_bs1", {}) if "dflash" in c else {}
        if base:
            chk[f"{c}_speedup_vs_nospec"] = {b: round(sp[b] / base[b]["decode_tok_s_p50"], 2) for b in sp
                                            if sp[b] and base.get(b, {}).get("decode_tok_s_p50")}
        e2e = row["e2e_bs1_s_p50"]
        chk[f"{c}_e2e_median_le_1s"] = {k: (v is not None and v <= 1.0) for k, v in e2e.items()}
        d, f = (c, "parity_deer1024"), (c, "parity_1024")
        if d in acc_ok and f in acc_ok:
            chk[f"{c}_deer_vs_cap1024"] = {**_paired(acc_ok[d], acc_ok[f]), "tokens_ratio": round(
                row["parity"]["parity_deer1024"]["think_tokens_mean"] /
                max(1e-9, row["parity"]["parity_1024"]["think_tokens_mean"]), 3)}
    chk["not_covered"] = ("B1 math-set rule (>= 85% of full-thinking accuracy at <= 1 s median on clean math sets) and "
                          "the FP8 dev-set check: need clean math dev items, not part of this app")
    return out


# ----------------------------------------------------------------------------------------------- entry points
@app.local_entrypoint()
def bench(configs: str = ",".join(CONFIGS), max_minutes: int = 25, max_usd: float = 15.0, n_speed: int = 10,
          block: int = 16, fast: bool = True, run: str = "", force: bool = False):
    """The B1 benchmark: one H100 container per config, run one after another (the first fills the HF cache)."""
    plan = make_plan(max_minutes=max_minutes, n_speed=n_speed, block=block, fast=fast)
    cfgs = [c for c in configs.split(",") if c]
    bad = [c for c in cfgs if c not in CONFIGS]
    if bad:
        raise SystemExit(f"unknown configs {bad}; choose from {list(CONFIGS)}")
    _check_inputs()
    est = estimate(plan, cfgs)
    print(json.dumps({"plan": plan, "configs": cfgs, "estimate": est}, indent=1))
    why = check_caps(est, max_usd)
    if why:
        raise SystemExit("REFUSED to start: " + "; ".join(why))
    run = run or time.strftime("b1_%Y%m%d_%H%M%S")
    rd = RUNS / run
    rd.mkdir(parents=True, exist_ok=True)
    (rd / "plan.json").write_text(json.dumps({"plan": plan, "configs": cfgs, "estimate": est}, indent=1))
    for c in cfgs:
        f = rd / f"{c}.json"
        if f.exists() and not force:
            print(f"{c}: kept {f} (pass --force to re-run)")
            continue
        try:
            r = run_config.remote(c, plan, run)
        except Exception as e:  # noqa: BLE001  (a killed or crashed container must not stop the other configs)
            r = {"config": c, "run": run, "steps": {}, "skipped": ["all"], "errors": {"container": repr(e)[:3000]}}
        f.write_text(json.dumps(r))
        print(json.dumps({c: {"wall_s": r.get("wall_s"), "skipped": r.get("skipped"), "errors": r.get("errors")}}))
    s = score_run(rd)
    (rd / "summary.json").write_text(json.dumps(s, indent=1))
    print(json.dumps(s["b1_checks"], indent=1))
    print(f"summary: {rd / 'summary.json'}")


def _check_inputs():
    """The input files exist and match think/data/inputs_manifest.json (built by build_bench_inputs.py)."""
    import hashlib
    man = json.loads((DATA / "inputs_manifest.json").read_text())
    for name, want in man["outputs"].items():
        got = hashlib.sha256((DATA / name).read_bytes()).hexdigest()
        if got != want:
            raise SystemExit(f"{name}: sha256 {got[:12]} != manifest {want[:12]} (re-run build_bench_inputs.py)")
    return man


def dry_run(configs=None, max_usd: float = 15.0) -> dict:
    """CPU only, no Modal call, no weights: inputs, engine configs, image pins, prompt identity, answer extraction,
    the DEER loop and the scoring path (fake engine), cost and caps."""
    sys.path[:0] = [str(THINK), str(LEAN)]
    import decoder_io as dio
    import think_engine as te
    cfgs = configs or list(CONFIGS)
    rep = {"inputs": _check_inputs()["n"], "engine_kwargs": {c: engine_kwargs(c) for c in cfgs},
           "image": {"sglang_image": SGLANG_IMAGE, "sglang": SGLANG_VERSION, "fastpath_pins": len(pinned35()),
                     "fastpath_key_pins": [p for p in pinned35() if p.split("==")[0] in ("torch", "transformers", "peft")]}}
    assert te.parse_letter(" A") == "A" and te.parse_letter("B.") == "B" and te.parse_letter("The answer") is None
    assert te.answer_prompt("P", "x</think>y") == ("Px</think>\n\n", False)
    assert te.answer_prompt("P", "x") == ("Px\n</think>\n\n", True)
    info, letters = {"kind": "noul", "keys": ["true", "false"]}, {"A": "Yes: s", "B": "No: t"}
    assert te.letter_to_key("A", info, letters) == "true" and te.letter_to_key("B", info, letters) == "false"
    assert te.letter_to_key("C", {"kind": "choice", "keys": ["x", "y"]}, {}) is None
    try:
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained(BASE, revision=BASE_REV, local_files_only=True)
        rep["tokenizer"] = f"{BASE}@{BASE_REV[:8]} (local cache)"
    except Exception as e:  # noqa: BLE001
        rep["tokenizer"] = f"SKIPPED prompt checks: tokenizer not cached locally ({type(e).__name__})"
        tok = None
    if tok is not None:
        items = [json.loads(x) for x in open(DATA / "squad2_parity100.jsonl") if x.strip()]
        tp = te.ThinkPath(te.FakeBackend(think_len=900), tok, dio)
        preps = tp.prepare(items)  # raises on any user-message drift vs the input file
        assert all(p["prompt"].endswith("<|im_start|>assistant\n<think>\n") for p in preps)
        assert len(tp.lid) == 26, "every option letter must be one token"
        run = "dryrun_" + time.strftime("%Y%m%d_%H%M%S")
        rd = RUNS / run
        rd.mkdir(parents=True, exist_ok=True)
        for c in cfgs:
            steps = {f"parity_{b}": tp.run(items, b) for b in DEFAULT_PLAN["parity_budgets"]}
            steps["parity_deer1024"] = tp.run(items, 1024, deer=te.DEER)
            steps["e2e_bs1_cap300"] = tp.run(items[:3], 300, batch=1)
            (rd / f"{c}.json").write_text(json.dumps({"config": c, "steps": steps, "skipped": [], "errors": {}}))
        s = score_run(rd)
        (rd / "summary.json").write_text(json.dumps(s, indent=1))
        p = s["configs"][cfgs[0]]["parity"]
        rep["fake_engine"] = {k: {x: v[x] for x in ("acc", "think_tokens_mean", "exit", "probes_mean")}
                              for k, v in p.items()}
        rep["fake_run_dir"] = str(rd)
    rep["estimate"] = estimate(make_plan(), cfgs)
    rep["refuse_reasons"] = check_caps(rep["estimate"], max_usd)
    rep["ok"] = not rep["refuse_reasons"]
    return rep


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--estimate", action="store_true")
    ap.add_argument("--score", default="")
    ap.add_argument("--configs", default=",".join(CONFIGS))
    ap.add_argument("--max-usd", type=float, default=15.0)
    ap.add_argument("--max-minutes", type=int, default=25)
    a = ap.parse_args()
    cs = [c for c in a.configs.split(",") if c]
    if a.score:
        print(json.dumps(score_run(a.score), indent=1))
    elif a.estimate:
        e = estimate(make_plan(max_minutes=a.max_minutes), cs)
        print(json.dumps({**e, "refuse_reasons": check_caps(e, a.max_usd)}, indent=1))
    elif a.dry_run:
        r = dry_run(cs, a.max_usd)
        print(json.dumps(r, indent=1))
        sys.exit(0 if r["ok"] else 1)
    else:
        ap.print_help()
