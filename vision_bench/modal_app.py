"""Vision bench (C1 vs base Qwen3.5-4B on the 5 image suites) on Modal: the same chain as harness/gpu_chain.sh, unchanged.

OWNER-APPROVED SIDE BENCHMARK. Evaluation only, never training. Modal profile mahadikarya44 ONLY (set MODAL_PROFILE explicitly).
Hard spend cap $3.00 for the whole task (see COST below). Does not touch the GCP VM, OpenRouter or Jev.

  MODAL_PROFILE=mahadikarya44 modal run modal_app.py --mode preflight   CPU only, no GPU: image/volume/adapter/data/tokenizer/LoRA gates
  MODAL_PROFILE=mahadikarya44 modal run --detach modal_app.py --mode chain   ONE H100 container: smoke c1, smoke base, gate,
                                                                             eval c1, eval base (warm, timed batch 1, diagnostics,
                                                                             throughput, localhost HTTP sample)

How it maps to the VM run: the container gets HOME=/root; /root/vision_bench/{harness,data,qwen35_processor} are mounted from this
folder; /root/lean/models/q35_4b_main500k is a symlink to the C1 adapter on the Modal volume "opendecide" (read only; sha256 must
start 507d1c29); /root/od/bin/python is a symlink to the image's python. harness/gpu_chain.sh then runs VERBATIM (no edits to the
harness, prompts or scoring). The base model is read from the volume's HF cache at the pinned revision, offline.
Software stack = the one the harness was tested with (VM od venv): python 3.12.10, torch 2.14.0, transformers 5.17.0, peft 0.21.0,
fla 0.5.2, triton 3.8.0 (PINNED35 copied from lean/modal_od.py, the stack the C1 adapter was trained on) + Pillow 12.3.0 and
torchvision 0.29.0 (the two wheels the VM job added).

COST (rates from `modal billing rates`): H100 $3.95/h + 4 CPU cores $0.19/h + 20 GiB $0.16/h = $4.30/h. 45 min of that would be
$3.23, over the cap, so the function timeout is 39 min ($2.80) and an in-container watchdog stops the chain at 36 min ($2.58).
Results are copied to the volume "vision-bench-results" every 60 s, so a stop keeps everything finished so far. No retries.
"""
from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent
RUN_ROOT = "/root/vision_bench"
BUDGET_S = 36 * 60      # watchdog: the chain is stopped (results kept) when the function has run this long
TIMEOUT_S = 39 * 60     # hard backstop enforced by Modal
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

app = modal.App("vision-bench-c1")
vol_models = modal.Volume.from_name("opendecide").read_only()  # C1 adapter + base HF cache; never written
vol_res = modal.Volume.from_name("vision-bench-results", create_if_missing=True)


def _ignore(p: Path) -> bool:
    return "__pycache__" in p.parts or p.suffix == ".pyc"


image = (
    modal.Image.debian_slim(python_version="3.12.10")
    .pip_install(*PINNED35)
    .pip_install("torchvision==0.29.0", "pillow==12.3.0", extra_options="--no-deps")
    .env({"HOME": "/root", "HF_HOME": "/vol/hf", "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1",
          "OMP_NUM_THREADS": "4", "MKL_NUM_THREADS": "4", "PYTHONUNBUFFERED": "1", "VB_RUN_ROOT": RUN_ROOT})
    .add_local_dir(HERE / "harness", f"{RUN_ROOT}/harness", ignore=_ignore)
    .add_local_dir(HERE / "data", f"{RUN_ROOT}/data")
    .add_local_dir(HERE / "src/qwen35-4b-processor", f"{RUN_ROOT}/qwen35_processor")
)
VOLS = {"/vol": vol_models, "/results": vol_res}


def _link(target: str, link: str):
    os.makedirs(os.path.dirname(link), exist_ok=True)
    if os.path.islink(link) or os.path.exists(link):
        os.remove(link)
    os.symlink(target, link)


def setup_env():
    """Lay out the container like the VM (HOME=/root): adapter path, python path, working dirs. Nothing in the harness is edited."""
    os.environ.update(HOME="/root", HF_HOME="/vol/hf", HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1")
    _link("/vol/models/q35_4b_main500k", "/root/lean/models/q35_4b_main500k")
    _link(sys.executable, "/root/od/bin/python")
    for d in ("results", "logs", "triton_cache"):
        os.makedirs(f"{RUN_ROOT}/{d}", exist_ok=True)


def sh(cmd: str, timeout=60) -> str:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return (r.stdout + r.stderr).strip()
    except Exception as e:  # noqa: BLE001
        return f"{type(e).__name__}: {e}"


def versions() -> dict:
    import importlib.metadata as md
    out = {"python": sys.version.split()[0]}
    for p in ("torch", "transformers", "peft", "safetensors", "tokenizers", "huggingface_hub", "accelerate", "numpy", "pillow",
              "torchvision", "flash-linear-attention", "fla-core", "triton", "scikit-learn"):
        try:
            out[p] = md.version(p)
        except Exception:  # noqa: BLE001
            out[p] = None
    return out


def sha256_file(path: str) -> str:
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


# ------------------------------------------------------------------------------------------------------ CPU preflight
@app.function(image=image, volumes=VOLS, cpu=8, memory=28 * 1024, timeout=25 * 60, max_containers=1)
def preflight() -> dict:
    """No GPU. Checks everything the GPU run depends on in the SAME image: versions, volume files, adapter sha256, data present,
    prompts/tokenizer/image processor for both models, localhost HTTP, and (CPU, 1 item) the full model + LoRA load with the
    harness's own hard gates (every adapter tensor bit-equal in the model, LoRA on != LoRA off, shared-ViT path == stock path)."""
    t0 = time.time()
    setup_env()
    rep = {"versions": versions()}
    import torch
    torch.set_num_threads(8)
    rep["cuda_available"] = torch.cuda.is_available()
    # volume files
    ad = "/root/lean/models/q35_4b_main500k"
    rep["adapter_files"] = sorted(os.listdir(ad))
    rep["adapter_sha256"] = sha256_file(f"{ad}/adapter_model.safetensors")
    assert rep["adapter_sha256"].startswith("507d1c29"), rep["adapter_sha256"]
    snap = "/vol/hf/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
    rep["base_snapshot_files"] = sorted(os.listdir(snap))
    rep["base_shard_bytes"] = {f: os.path.getsize(f"{snap}/{f}") for f in rep["base_snapshot_files"] if f.endswith(".safetensors")}
    # data
    n = {}
    for s in ("img_sst2", "img_ar_sentiment", "img_pets", "img_vqa_yesno", "img_count"):
        cases = [json.loads(l) for l in open(f"{RUN_ROOT}/data/{s}/cases.jsonl", encoding="utf-8")]
        miss = [c["id"] for c in cases if not os.path.exists(f"{RUN_ROOT}/data/{s}/images/{os.path.basename(c['state'][0]['image'])}")]
        n[s] = {"n": len(cases), "missing_images": len(miss)}
    rep["data"] = n
    assert all(v["n"] == 200 and v["missing_images"] == 0 for v in n.values()), n
    # localhost HTTP works in this sandbox (the e2e sample needs it)
    import http.client
    import http.server
    import socketserver

    class H(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        def log_message(self, *a): pass
        def do_POST(self):
            b = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    class S(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True; allow_reuse_address = True

    srv = S(("127.0.0.1", 8765), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    c = http.client.HTTPConnection("127.0.0.1", 8765, timeout=10)
    c.request("POST", "/x", body=b"ping", headers={"Content-Type": "application/json"})
    rep["loopback_http"] = c.getresponse().read() == b"ping"
    srv.shutdown()
    # harness-level checks, CPU only
    sys.path.insert(0, f"{RUN_ROOT}/harness")
    import vb_core as vb
    rep["harness_paths"] = {"ADAPTER": vb.ADAPTER, "ADAPTER_RENAMED": vb.ADAPTER_RENAMED, "PROC_DIR": vb.PROC_DIR, "data_root": vb.data_root()}
    cases = vb.load_cases()
    assert len(cases) == 1000
    by = {}
    for c in cases:
        by.setdefault(c["suite"], []).append(c)
    prep_rep = {}
    for which in ("c1", "base"):
        rd = vb.Reader(which, dev="cpu", load_model=False)
        prep_rep[which] = {"layout": rd.layout, "style": rd.style, "imgproc": type(rd.imgproc).__name__, "items": []}
        for s in vb.SUITES:
            c = by[s][0]
            qid, q = next(iter(c["questions"].items()))
            p = rd.prepare(open(c["_image_file"], "rb").read(), q)
            prep_rep[which]["items"].append({"id": c["id"], "views": len(p["views"]), "n_tokens": [len(x) for x in p["seqs"]],
                                             "n_img": p["n_img"], "n_options": len(p["groups"])})
    rep["prepare"] = prep_rep
    rep["t_checks_s"] = time.time() - t0
    print("PREFLIGHT part 1 ok", json.dumps(rep["prepare"]["c1"]["items"][0]), flush=True)
    # the full C1 model + LoRA on CPU: the harness's own adapter gates, then one SST-2 item through read / read_stock / adapter_effect
    try:
        t1 = time.time()
        rd = vb.Reader("c1", dev="cpu")
        rep["c1_load_s"] = rd.load_s
        rep["adapter_check"] = rd.adapter_check
        assert rd.adapter_check["n_lora_B"] == vb.ADAPTER_N_LORA_B == rd.adapter_check["n_lora_B_nonzero"], rd.adapter_check
        assert rd.adapter_check["n_tensors"] == vb.ADAPTER_N_TENSORS and rd.adapter_check["n_no_home"] == 0 \
            and rd.adapter_check["n_unequal_to_file"] == 0, rd.adapter_check
        rep["adapter_renamed_sha256"] = sha256_file(f"{vb.ADAPTER_RENAMED}/adapter_model.safetensors")
        c = by["img_sst2"][0]
        qid, q = next(iter(c["questions"].items()))
        prep = rd.prepare(open(c["_image_file"], "rb").read(), q)
        lg = rd.read([prep])[0]
        probs = rd.decide(prep, lg)
        st = rd.read_stock(prep)
        probs_stock = rd.decide(prep, st)
        rep["cpu_item"] = {"id": c["id"], "probs": probs, "probs_stock": probs_stock,
                           "max_prob_diff_shared_vit_vs_stock": max(abs(a - b) for a, b in zip(probs, probs_stock)),
                           "adapter_effect_max_logit_diff_on_vs_off": rd.adapter_effect(prep), "t_s": time.time() - t1}
    except Exception as e:  # noqa: BLE001
        import traceback
        rep["cpu_model_error"] = f"{type(e).__name__}: {str(e)[:600]}"
        rep["cpu_model_traceback_tail"] = traceback.format_exc()[-1500:]
    rep["total_s"] = time.time() - t0
    return rep


# ------------------------------------------------------------------------------------------------------ the GPU chain
def _sync(run: str):
    """Copy results + logs to the results volume and commit, so a stop or a crash keeps everything finished so far."""
    dst = Path("/results") / run
    for sub in ("results", "logs"):
        src = Path(RUN_ROOT) / sub
        if src.exists():
            shutil.copytree(src, dst / sub, dirs_exist_ok=True)
    vol_res.commit()


@app.function(image=image, gpu="H100!", cpu=4, memory=20 * 1024, timeout=TIMEOUT_S, retries=0, max_containers=1, volumes=VOLS)
def chain(run: str = "") -> dict:
    t0 = time.time()
    setup_env()
    run = run or time.strftime("run-%Y%m%d-%H%M%S", time.gmtime())
    gpu = sh("nvidia-smi --query-gpu=name,memory.total,memory.used,driver_version --format=csv,noheader")
    env = {"run": run, "start_utc": time.strftime("%F %T", time.gmtime(t0)), "gpu_nvidia_smi": gpu, "versions": versions(),
           "modal_task_id": os.environ.get("MODAL_TASK_ID"), "budget_s": BUDGET_S, "timeout_s": TIMEOUT_S, "nproc": os.cpu_count(),
           "loadavg": os.getloadavg(), "cuda_visible": os.environ.get("CUDA_VISIBLE_DEVICES"),
           "adapter_sha256": sha256_file("/root/lean/models/q35_4b_main500k/adapter_model.safetensors")}
    assert env["adapter_sha256"].startswith("507d1c29"), env["adapter_sha256"]
    json.dump(env, open(f"{RUN_ROOT}/results/modal_env.json", "w"), indent=1)
    print("ENV", json.dumps(env), flush=True)
    chain_log = open(f"{RUN_ROOT}/logs/chain.log", "w")
    proc = subprocess.Popen(["bash", f"{RUN_ROOT}/harness/gpu_chain.sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                            cwd=RUN_ROOT, start_new_session=True)

    def pump():
        for line in proc.stdout:
            chain_log.write(line); chain_log.flush()
            print("[chain]", line.rstrip(), flush=True)

    stop = threading.Event()
    offsets = {}

    def tail_logs():  # stream the per-stage logs (smoke_*.log, eval_*.log) into the Modal log
        while not stop.is_set():
            for p in sorted(Path(f"{RUN_ROOT}/logs").glob("*.log")):
                if p.name == "chain.log":
                    continue
                try:
                    with open(p) as f:
                        f.seek(offsets.get(p.name, 0))
                        chunk = f.read()
                        offsets[p.name] = f.tell()
                    for line in chunk.splitlines():
                        print(f"[{p.stem}]", line[:400], flush=True)
                except Exception:  # noqa: BLE001
                    pass
            stop.wait(10)

    def syncer():
        while not stop.wait(60):
            try:
                _sync(run)
            except Exception as e:  # noqa: BLE001
                print("sync error", type(e).__name__, str(e)[:200], flush=True)

    threads = [threading.Thread(target=f, daemon=True) for f in (pump, tail_logs, syncer)]
    [t.start() for t in threads]
    budget_stop = False
    while proc.poll() is None:
        time.sleep(2)
        if time.time() - t0 > BUDGET_S:
            budget_stop = True
            print(f"BUDGET STOP at {time.time() - t0:.0f}s: killing the chain (finished results are kept)", flush=True)
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            time.sleep(10)
            if proc.poll() is None:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            break
    rc = proc.wait()
    time.sleep(3)
    stop.set()
    time.sleep(1)
    wall = time.time() - t0
    gpu_end = sh("nvidia-smi --query-gpu=name,memory.used --format=csv,noheader")
    done = {"run": run, "chain_exit_code": rc, "budget_stop": budget_stop, "function_wall_s": wall, "gpu": gpu, "gpu_end": gpu_end,
            "end_utc": time.strftime("%F %T", time.gmtime()), "results_files": sorted(os.listdir(f"{RUN_ROOT}/results")),
            "est_cost_usd_at_4.30_per_h": wall / 3600 * 4.30}
    json.dump(done, open(f"{RUN_ROOT}/results/modal_done.json", "w"), indent=1)
    _sync(run)
    print("DONE", json.dumps(done), flush=True)
    return done


@app.local_entrypoint()
def main(mode: str = "preflight", run: str = ""):
    if mode == "preflight":
        print(json.dumps(preflight.remote(), indent=1))
    elif mode == "chain":
        print(json.dumps(chain.remote(run), indent=1))
    else:
        raise SystemExit("mode must be preflight or chain")
