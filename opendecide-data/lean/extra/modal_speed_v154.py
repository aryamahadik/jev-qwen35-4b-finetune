"""H100 speed test of 4B-E (q35_4b_pxE) on the 231 public JevBench v1.5.4 items. NEW file; touches no existing code.

  cd ~/Documents/jev/opendecide-data/lean
  MODAL_PROFILE=arya-mahadik-ai ../.venv/bin/modal run --detach extra/modal_speed_v154.py

Part 1: bench/v154/run_v154.py --graphs (the official harness Runner, one decision per request, CUDA graphs) on an
H100. If the graph run fails it is re-run without graphs, and the summary says so ("graphs_used": false).
Part 2 (same container, model loaded again in-process): a small timing loop over the same 231 prompts, interleaved per
item, three ways:
  1view        one forward, exactly the adapter's readout (sanity check against part 1)
  2view_seq    the prompt read twice, as given and with the options reversed (decoder_io.predict's tta_choice
               arithmetic; every cygnet row, yes/no included, is a lettered choice row), two forwards one after another
  2view_batch  the same two views as ONE batch-2 forward
decoder_io.predict itself is not timed, because it builds a new Readout (a full-vocabulary scan) on every call; the
loop reuses one Readout and checks its 2-view probabilities against decoder_io.predict(tta_choice=True) on 8 rows.

Writes only /vol/speed_v154/ on the account's "opendecide" Volume:
  v154_q35_4b_pxE_h100_g/       (or _eager on fallback) run_v154 output: results.jsonl, manifest.json, ledger.jsonl,
                                raw/, run.log -- scores with bench/v154/score_v154.py like any v154 run
  inline_1view/, inline_2view_seq/, inline_2view_batch/   results.jsonl + manifest.json each (score_v154-compatible)
  summary.json                  p50/p95 raw latency (standard items = the speed-axis set, and all items), the JevBench
                                v1.5 speed axis (self-hosted: x2 + 0.15 s), I_open on the public items, checks
The Triton cache is a private /tmp copy seeded from /vol/triton_cache (read only), so no other Volume path is written.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent  # lean/extra (in the container: /root, and none of these paths are used there)
LEAN = HERE.parent
JEV = LEAN.parent.parent
V154 = JEV / "bench/v154"
JB154 = JEV / "bench/jevbench_v154"

APP_NAME = "od-speed-v154"  # its own app; the live 4B run's app ("opendecide") and models/q35_4b_main500k* untouched
OUT = "/vol/speed_v154"
MODEL = "q35_4b_pxE"
BASE = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
LEAN_FILES = ("decoder_io.py", "prism_x.py", "writeblock.py", "calc_tool.py", "jevbench_od.py")

# Exact copy of modal_od.PINNED35 (checked below against modal_od.py, parsed as text: modal_od is never imported), so
# this image is the same pip layer as modal_od.image35 and is served from the account's image cache.
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


def _v154_ignore(p: Path) -> bool:
    return bool(p.parts) and (p.parts[0] in ("smoke", "__pycache__") or p.suffix in (".pyc", ".log"))


if modal.is_local():
    if pinned_from_modal_od() != PINNED35:
        raise SystemExit("PINNED35 here differs from modal_od.py: refusing (the image would not be the relay's)")
    for f in [*(LEAN / n for n in LEAN_FILES), V154 / "run_v154.py", V154 / "v154lib.py",
              V154 / "lean_snapshot/jevbench_od.py", JB154 / "jevbench/runner.py", JB154 / "datasets/public/hard.jsonl"]:
        if not f.exists():
            raise SystemExit(f"missing {f}")

image = (  # the modal_od.image35 build steps (debian_slim 3.12.10 + PINNED35 + env), then only runtime mounts
    modal.Image.debian_slim(python_version="3.12.10")
    .pip_install(*PINNED35)
    .env({"HF_HOME": "/vol/hf", "HF_HUB_ENABLE_HF_TRANSFER": "1", "TOKENIZERS_PARALLELISM": "false",
          "TRITON_CACHE_DIR": "/vol/triton_cache"})
)
for _n in LEAN_FILES:
    image = image.add_local_file(LEAN / _n, f"/root/lean/{_n}")
image = (
    image.add_local_dir(V154, "/root/v154", ignore=_v154_ignore)  # run_v154.py, v154lib.py, lean_snapshot/
    .add_local_dir(JB154 / "jevbench", "/root/jevbench_v154/jevbench", ignore=lambda p: "__pycache__" in p.parts)
    .add_local_dir(JB154 / "datasets/public", "/root/jevbench_v154/datasets/public")
    .add_local_file(JB154 / "docs/METHOD-v1.5.md", "/root/jevbench_v154/docs/METHOD-v1.5.md")
)
app = modal.App(APP_NAME)
vol = modal.Volume.from_name("opendecide")  # the account Volume (no create_if_missing: fail rather than make a new one)


# ------------------------------------------------------------------ helpers (CPU-testable, no Modal needed)

def lat_summary(recs: dict, items: dict, L, kind="gpu", price_in=0.03) -> dict:
    """score_v154.score_run's speed part (standard + judge items; x2 + 0.15 s for self-hosted) plus I_open and cost."""
    ids = [i for i in recs if i in items]
    outs = [L.item_outcome(items[i], recs[i]) for i in ids]
    sp = [o["latency_s"] for o in outs if o["tier"] in ("standard", "judge") and o["latency_s"] is not None]
    al = [o["latency_s"] for o in outs if o["latency_s"] is not None]
    p50, p95 = L.percentile(sp, 0.5), L.percentile(sp, 0.95)
    tin = sum((o["usage"].get("input_tokens") or 0) for o in outs) / max(1, len(outs))
    usd = tin * price_in / 1e6 * 1000
    ms = lambda x: None if x is None else round(1000 * x, 2)
    return {"n": len(outs), "n_speed_items": len(sp), "p50_ms_raw": ms(p50), "p95_ms_raw": ms(p95),
            "p50_ms_raw_all": ms(L.percentile(al, 0.5)), "p95_ms_raw_all": ms(L.percentile(al, 0.95)),
            "max_ms_raw_all": ms(max(al) if al else None),
            "speed_axis": L.speed(p50, p95, kind) if sp else None,
            "I_open": L.intelligence_open(outs)[0] if outs else None,
            "input_tokens_per_decision": tin, "cost_axis": L.cost(usd) if usd > 0 else None}


def inline_views(model, tok, tasks, dev, jo, decoder_io, n_warm=3, log=print) -> dict:
    """Part 2. Returns {mode: {task_id: record}} plus checks. Works on CPU (tiny model) for the local smoke test."""
    import torch
    if decoder_io.STYLE != "cygnet":
        raise SystemExit("inline_views supports cygnet-style adapters only (4B-E is cygnet)")
    sync = torch.cuda.synchronize if dev == "cuda" else (lambda: None)
    ro = decoder_io.Readout(tok)
    items = []
    for t in tasks:
        row, keys, yes_index = jo.letter_row(t, tok, "cygnet")
        body = {k: v for k, v in row.items() if k != "_prompt"}
        if ro.prompt(body) != row["_prompt"]:  # the loop must read exactly what the adapter reads
            raise SystemExit(f"{t.id}: decoder_io.Readout.prompt differs from jevbench_od.letter_row's prompt")
        n = len(body["options"])
        rev = list(range(n))[::-1]
        n1 = len(tok(row["_prompt"], add_special_tokens=False)["input_ids"])
        n2 = len(tok(ro.prompt(body, rev), add_special_tokens=False)["input_ids"])
        items.append({"t": t, "body": body, "keys": keys, "yes": yes_index, "n": n, "rev": rev, "n1": n1, "n2": n2})

    def to_rec(it, pos, dt, n_in, mode):
        pr = pos
        probs = {"yes": pr[it["yes"]], "no": 1 - pr[it["yes"]]} if it["yes"] is not None else dict(zip(it["keys"], pr))
        return {"task_id": it["t"].id, "type": it["t"].question["type"], "ok": True, "valid": True, "probs": probs,
                "latency_s": dt, "usage": {"input_tokens": n_in, "output_tokens": 0}, "mode": mode}

    def unrev(it, lg):  # probabilities of a reversed view, back in the original option order
        s, p = torch.softmax(lg.float(), -1).tolist(), [0.0] * it["n"]
        for j, orig in enumerate(it["rev"]):
            p[orig] = s[j]
        return p

    def one(it):
        t0 = time.perf_counter()
        lg = decoder_io.cand_logits(model, ro, [it["body"]], dev)[0]
        sync()
        dt = time.perf_counter() - t0
        return to_rec(it, torch.softmax(lg.float(), -1).tolist(), dt, it["n1"], "1view")

    def seq2(it):
        t0 = time.perf_counter()
        l1 = decoder_io.cand_logits(model, ro, [it["body"]], dev)[0]
        l2 = decoder_io.cand_logits(model, ro, [it["body"]], dev, perms=[it["rev"]])[0]
        sync()
        dt = time.perf_counter() - t0
        p1, p2 = torch.softmax(l1.float(), -1).tolist(), unrev(it, l2)
        return to_rec(it, [(a + b) / 2 for a, b in zip(p1, p2)], dt, it["n1"] + it["n2"], "2view_seq")

    def bat2(it):
        t0 = time.perf_counter()
        l1, l2 = decoder_io.cand_logits(model, ro, [it["body"], it["body"]], dev, perms=[None, it["rev"]])
        sync()
        dt = time.perf_counter() - t0
        p1, p2 = torch.softmax(l1.float(), -1).tolist(), unrev(it, l2)
        return to_rec(it, [(a + b) / 2 for a, b in zip(p1, p2)], dt, it["n1"] + it["n2"], "2view_batch")

    modes = {"1view": one, "2view_seq": seq2, "2view_batch": bat2}
    runnable = [it for it in items if it["n"] <= 26]  # the adapter refuses > 26 options too
    out = {m: {} for m in modes}
    with torch.no_grad():  # as the adapter's run() (cand_logits itself is not no_grad)
        for it in runnable[:n_warm]:  # warm-up calls, not recorded
            for f in modes.values():
                f(it)
        for k, it in enumerate(runnable):  # interleaved per item, so clock drift hits every mode alike
            for m, f in modes.items():
                out[m][it["t"].id] = f(it)
            if (k + 1) % 50 == 0:
                log(f"inline: {k + 1}/{len(runnable)} items")
    # checks: 2view_seq == 2view_batch, and == decoder_io.predict(tta_choice=True) on up to 8 rows (untimed)
    diff_sb = max(abs(out["2view_seq"][i]["probs"][k] - out["2view_batch"][i]["probs"][k])
                  for i in out["2view_seq"] for k in out["2view_seq"][i]["probs"])
    chk = [it for it in runnable if len(set(it["body"]["options"])) == it["n"]][:8]
    pred = decoder_io.predict(model, tok, [it["body"] for it in chk], batch_size=8, dev=dev, tta_choice=True,
                              tta_noul=False)
    diff_pred = 0.0
    for it, pr in zip(chk, pred):
        mine = out["2view_seq"][it["t"].id]["probs"]
        vec = [pr[o] for o in it["body"]["options"]]
        ref = {"yes": vec[it["yes"]], "no": 1 - vec[it["yes"]]} if it["yes"] is not None else dict(zip(it["keys"], vec))
        diff_pred = max(diff_pred, max(abs(mine[k] - ref[k]) for k in mine))
    return {"records": out, "checks": {"n_items": len(runnable), "n_skipped_over_26": len(items) - len(runnable),
                                       "max_prob_diff_2view_seq_vs_batch": diff_sb,
                                       "max_prob_diff_2view_vs_decoder_io_predict": diff_pred,
                                       "n_predict_check_rows": len(chk)}}


def write_run(d: Path, recs: dict, manifest: dict):
    d.mkdir(parents=True, exist_ok=True)
    with open(d / "results.jsonl", "w") as f:
        for r in recs.values():
            f.write(json.dumps(r) + "\n")
    (d / "manifest.json").write_text(json.dumps(manifest, indent=2))


def v154_cmd(py, v154_dir, model_dir, lean, jb, out, name, graphs, extra=()):
    return [py, str(Path(v154_dir) / "run_v154.py"), "--model", str(model_dir), "--base", BASE, "--revision", REVISION,
            "--lean", str(lean), "--jevbench", str(jb), "--out", str(out), "--name", name,
            *(["--graphs"] if graphs else []), *extra]


def stream(cmd, log_path: Path, env=None) -> int:
    print("$ " + " ".join(cmd), flush=True)
    with open(log_path, "w") as lf:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
        for line in p.stdout:
            print(line, end="", flush=True)
            lf.write(line)
        return p.wait()


# ------------------------------------------------------------------ the Modal job

@app.function(image=image, gpu="H100!", volumes={"/vol": vol}, timeout=25 * 60)
def speed(jb_commit: str = "", overwrite: bool = False, inline: bool = True) -> dict:
    t_start = time.time()
    out = Path(OUT)
    if out.exists() and any(out.iterdir()):
        if not overwrite:
            raise SystemExit(f"{OUT} is not empty; pass --overwrite to move the old results to {OUT}/_old_<time>")
        old = out / time.strftime("_old_%Y%m%d-%H%M%S")
        old.mkdir()
        for p in list(out.iterdir()):
            if not p.name.startswith("_old_"):
                p.rename(old / p.name)
    out.mkdir(parents=True, exist_ok=True)
    model_dir = Path(f"/vol/models/{MODEL}")
    if not (model_dir / "adapter_model.safetensors").exists():
        raise SystemExit(f"{model_dir} missing on this account's Volume")
    if (model_dir / "prism_x.json").exists():
        raise SystemExit("this adapter has prism_x.json: CUDA graphs are not supported for PRISM-X")
    tc = Path("/tmp/triton_cache")  # private cache, seeded read-only from the Volume (compiled fla kernels)
    try:
        shutil.copytree("/vol/triton_cache", tc, dirs_exist_ok=True)
    except Exception as e:
        print(f"triton cache seed skipped: {e}", flush=True)
    os.environ["TRITON_CACHE_DIR"] = str(tc)
    stub = shutil.which("nvidia-smi") is None
    if stub:  # run_v154 asks nvidia-smi whether another process uses the GPU; a Modal GPU is this container's alone
        Path("/tmp/bin").mkdir(exist_ok=True)
        Path("/tmp/bin/nvidia-smi").write_text("#!/bin/sh\nexit 0\n")
        os.chmod("/tmp/bin/nvidia-smi", 0o755)
        os.environ["PATH"] = "/tmp/bin:" + os.environ.get("PATH", "")
    env = {**os.environ, "TRITON_CACHE_DIR": str(tc), "PYTHONUNBUFFERED": "1"}
    summary = {"nvidia_smi_stub": stub, "model": MODEL, "base": BASE, "revision": REVISION, "gpu_request": "H100!", "jevbench_commit": jb_commit,
               "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    # ---- part 1: run_v154.py --graphs (fallback: eager)
    tmp = Path("/tmp/speed")
    tmp.mkdir(exist_ok=True)
    args = dict(py=sys.executable, v154_dir="/root/v154", model_dir=model_dir, lean="/root/lean",
                jb="/root/jevbench_v154")
    graphs_used = True
    name = f"v154_{MODEL}_h100_g"
    rc = stream(v154_cmd(**args, out=tmp / name, name=name, graphs=True, extra=["--allow-shared-gpu"]),
                tmp / f"{name}.log", env)
    if rc != 0:
        print(f"\n*** run_v154 --graphs FAILED (exit {rc}); re-running WITHOUT graphs ***\n", flush=True)
        summary["graphs_failed_exit_code"] = rc
        graphs_used = False
        shutil.copy(tmp / f"{name}.log", out / f"{name}_FAILED.log")
        name = f"v154_{MODEL}_h100_eager"
        rc = stream(v154_cmd(**args, out=tmp / name, name=name, graphs=False, extra=["--allow-shared-gpu"]),
                    tmp / f"{name}.log", env)
    summary["graphs_used"] = graphs_used
    summary["run_v154_exit_code"] = rc
    summary["run_v154_dir"] = f"{OUT}/{name}"
    sys.path[:0] = ["/root/jevbench_v154", "/root/v154/lean_snapshot", "/root/lean", "/root/v154"]
    import v154lib as L
    items = L.load_public("/root/jevbench_v154")
    if (tmp / name / "results.jsonl").exists():
        shutil.copytree(tmp / name, out / name, dirs_exist_ok=True)
        shutil.copy(tmp / f"{name}.log", out / name / "run.log")
        recs = {json.loads(l)["task_id"]: json.loads(l) for l in open(tmp / name / "results.jsonl") if l.strip()}
        summary["run_v154"] = lat_summary(recs, items, L)
        man = json.loads((tmp / name / "manifest.json").read_text()) if (tmp / name / "manifest.json").exists() else {}
        summary["run_v154"].update({k: man.get(k) for k in ("gpu", "graph_selfcheck_max_prob_diff", "warmup_s",
                                                            "load_and_warmup_s", "run_s", "max_memory_gb")})
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    vol.commit()
    print(json.dumps({"part1": summary.get("run_v154"), "graphs_used": graphs_used}, indent=2), flush=True)

    # ---- part 2: inline 1-view / 2-view timing loop (same prompts, same model, in-process)
    if not inline:
        summary["inline"] = "skipped (--no-inline)"
    elif time.time() - t_start > 15 * 60:
        summary["inline"] = f"skipped: part 1 took {time.time() - t_start:.0f}s (budget guard)"
    else:
        try:
            summary["inline"] = _inline_part(items, L, graphs_used, model_dir)
        except Exception as e:  # part 1's results are already on the Volume
            import traceback
            traceback.print_exc()
            summary["inline"] = {"error": f"{type(e).__name__}: {e}"}
    summary["total_s"] = round(time.time() - t_start, 1)
    summary["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    vol.commit()
    print("SUMMARY " + json.dumps(summary, indent=2), flush=True)
    return summary


def _inline_part(items, L, graphs_used, model_dir) -> dict:
    import torch
    import decoder_io
    import jevbench_od as jo
    from jevbench.tasks import load_jsonl
    tasks = [t for tier in ("easy", "original", "hard")
             for t in load_jsonl(f"/root/jevbench_v154/datasets/public/{tier}.jsonl")]
    t0 = time.time()
    model, tok, info = decoder_io.load(BASE, "cuda", adapter=str(model_dir), revision=REVISION, return_info=True)
    model = model.merge_and_unload()  # as run_v154
    model.eval()
    for cfg in (model.config, getattr(model.config, "text_config", None)):
        if cfg is not None:
            cfg.use_cache = True
    model.generation_config.use_cache = True
    ro = decoder_io.Readout(tok)
    decoder_io.warmup(model, ro, max_tokens=8192, batch_sizes=(1, 2))
    res = {"graphs": graphs_used, "load": {k: info.get(k) for k in ("layout", "style", "revision", "prism_x")}}
    if graphs_used:
        longest = max(len(tok(jo.letter_row(t, tok, "cygnet")[0]["_prompt"], add_special_tokens=False)["input_ids"])
                      for t in tasks)
        top = max(4096, -(-longest // 64) * 64)  # also capture the long buckets, so no request captures a graph
        decoder_io.GRAPHS = decoder_io.GraphRunner(model, tok, batches=(1, 2))
        decoder_io.GRAPHS.capture_all(max_tokens=top, batches=(1,))
        try:
            decoder_io.GRAPHS.capture_all(max_tokens=top, batches=(2,))  # B=2 up to 4096 tokens per row (8192 total)
            res["graphs_batch2"] = True
        except Exception as e:  # batch-2 rows then run eagerly
            res["graphs_batch2"] = f"failed: {type(e).__name__}: {e}"
            decoder_io.GRAPHS.batches = (1,)
            decoder_io.GRAPHS.graphs = {k: v for k, v in decoder_io.GRAPHS.graphs.items() if k[0] == 1}
            torch.cuda.empty_cache()
        res["graphs_captured"] = len(decoder_io.GRAPHS.graphs)
        res["longest_prompt_tokens"] = longest
    res["load_warmup_capture_s"] = round(time.time() - t0, 1)
    tl = time.time()
    got = inline_views(model, tok, tasks, "cuda", jo, decoder_io)
    res["loop_s"] = round(time.time() - tl, 1)
    res["checks"] = got["checks"]
    res["max_memory_gb"] = round(torch.cuda.max_memory_allocated() / 2 ** 30, 2)
    res["gpu"] = torch.cuda.get_device_name(0)
    for mode, recs in got["records"].items():
        man = {"name": f"inline_{mode}", "mode": "gpu", "adapter": str(model_dir), "base": BASE, "revision": REVISION,
               "graphs": graphs_used, "gpu": res["gpu"], "cost_basis": "self_hosted_gpu",
               "protocol": "UNOFFICIAL inline timing loop (not the harness Runner); same prompts as jevbench_od "
                           "cygnet; latency = cand_logits call(s) + cuda sync, as the adapter measures",
               "views": 1 if mode == "1view" else 2}
        write_run(Path(OUT) / f"inline_{mode}", recs, man)
        res[mode] = lat_summary(recs, items, L)
    return res


@app.local_entrypoint()
def main(overwrite: bool = False, no_inline: bool = False):
    jb_commit = subprocess.run(["git", "-C", str(JB154), "rev-parse", "HEAD"], capture_output=True,
                               text=True).stdout.strip()
    res = speed.remote(jb_commit=jb_commit, overwrite=overwrite, inline=not no_inline)
    print(json.dumps(res, indent=2))
    try:
        (HERE / "speed_v154_summary.json").write_text(json.dumps(res, indent=2))
    except OSError:
        pass
