"""Text track of System One Bench (C1 vs base Qwen3.5-4B on the 16 text suites) on Modal.

OWNER-APPROVED SIDE BENCHMARK. Evaluation only, never training. Modal profile mahadikarya44 ONLY (set MODAL_PROFILE explicitly).
Hard cap $2.00 for the whole task. Does not touch the GCP VM, OpenRouter or Jev.

  MODAL_PROFILE=mahadikarya44 modal run modal_app.py --mode preflight      CPU only, no GPU: volume/adapter/data/tokenizer gates, and the
                                                                           real C1 load on CPU (adapter proof + 3 real items)
  MODAL_PROFILE=mahadikarya44 modal run --detach modal_app.py --mode chain  ONE H100 container: harness/run_text.py eval (gates, main,
                                                                           lat, diag), one model load, both arms

COST (rates from `modal billing rates`, same as the vision run): H100 $3.95/h + 4 CPU cores $0.19/h + 20 GiB $0.16/h = $4.30/h.
$2.00 is 27.9 min of that, so: run_text.py stops STARTING work at 21 min (--deadline-s 1260), an in-container watchdog stops the whole
chain at 24 min, and Modal's own function timeout is 26 min ($1.86). Results are copied to the volume "text-track-results" every 60 s,
so a stop keeps everything finished so far. No retries (retries=0): a crash cannot start a second billed container.
The container is laid out like the vision run: C1's adapter and the base model's HF cache come from the read-only volume "opendecide".
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
RUN_ROOT = "/root/text_track"
ADAPTER = "/vol/models/q35_4b_main500k"
DEADLINE_S = 21 * 60    # run_text.py: no new suite / stage after this many seconds of process time
BUDGET_S = 24 * 60      # watchdog: the chain is stopped (results kept) when the function has run this long
TIMEOUT_S = 26 * 60     # hard backstop enforced by Modal
RATE_PER_H = 4.30
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

app = modal.App("text-track-c1")
vol_models = modal.Volume.from_name("opendecide").read_only()  # C1 adapter + base HF cache; never written
vol_res = modal.Volume.from_name("text-track-results", create_if_missing=True)


def _ignore(p: Path) -> bool:
    return "__pycache__" in p.parts or p.suffix == ".pyc"


image = (
    modal.Image.debian_slim(python_version="3.12.10")
    .pip_install(*PINNED35)
    .env({"HOME": "/root", "HF_HOME": "/vol/hf", "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1", "OMP_NUM_THREADS": "4",
          "MKL_NUM_THREADS": "4", "PYTHONUNBUFFERED": "1", "TT_ADAPTER": ADAPTER,
          "TT_DATA": f"{RUN_ROOT}/data/cases.jsonl", "TRITON_CACHE_DIR": f"{RUN_ROOT}/triton_cache", "PYTHONDONTWRITEBYTECODE": "1"})
    .add_local_dir(HERE / "harness", f"{RUN_ROOT}/harness", ignore=_ignore)
    .add_local_file(HERE / "data" / "cases.jsonl", f"{RUN_ROOT}/data/cases.jsonl")
    .add_local_file(HERE / "data" / "data.lock.cases.json", f"{RUN_ROOT}/data/data.lock.cases.json")
)
VOLS = {"/vol": vol_models, "/results": vol_res}


def sh(cmd: str, timeout=60) -> str:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return (r.stdout + r.stderr).strip()
    except Exception as e:  # noqa: BLE001
        return f"{type(e).__name__}: {e}"


def versions() -> dict:
    import importlib.metadata as md
    out = {"python": sys.version.split()[0]}
    for p in ("torch", "transformers", "peft", "safetensors", "tokenizers", "huggingface_hub", "accelerate", "numpy",
              "flash-linear-attention", "fla-core", "triton", "scikit-learn"):
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
@app.function(image=image, volumes=VOLS, cpu=8, memory=28 * 1024, timeout=12 * 60, max_containers=1, retries=0)
def preflight() -> dict:
    """No GPU. Same image, same volume: versions, adapter sha256, base snapshot, frozen-data check, prompts and token counts for all
    4,850 decisions with both tokenizers, then the REAL C1 on CPU: text-only class, adapter proof (496 tensors bit-equal, 248 lora_B
    non-zero), LoRA on != off, and three real items read."""
    t0 = time.time()
    os.environ.update(HOME="/root", HF_HOME="/vol/hf", HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1")
    sys.path.insert(0, f"{RUN_ROOT}/harness")
    rep = {"versions": versions()}
    import torch
    torch.set_num_threads(8)
    rep["cuda_available"] = torch.cuda.is_available()
    rep["adapter_files"] = sorted(os.listdir(ADAPTER))
    rep["adapter_sha256"] = sha256_file(f"{ADAPTER}/adapter_model.safetensors")
    assert rep["adapter_sha256"].startswith("507d1c29"), rep["adapter_sha256"]
    snap = "/vol/hf/hub/models--Qwen--Qwen3.5-4B/snapshots/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
    rep["base_snapshot_files"] = sorted(os.listdir(snap))
    import lockcheck
    rep["data_lock_problems"] = lockcheck.check(f"{RUN_ROOT}/data/cases.jsonl", f"{RUN_ROOT}/data/data.lock.cases.json")
    assert not rep["data_lock_problems"], rep["data_lock_problems"]
    import tt_core as tt
    rd = tt.Reader(dev="cpu", load_model=False)
    ds = tt.load_decisions()
    assert len(ds) == 4850
    pa, pb = rd.prepare_many(ds, "main"), rd.prepare_many(ds, "main", tok=rd.tok_base)
    rep["prompts"] = {"decisions": len(pa), "sequences": sum(len(p["seqs"]) for p in pa),
                      "real_tokens": sum(len(s) for p in pa for s in p["seqs"]), "max_len": max(len(s) for p in pa for s in p["seqs"]),
                      "tokenizers_identical": all(x["seqs"] == y["seqs"] and x["texts"] == y["texts"] for x, y in zip(pa, pb)),
                      "layout": rd.layout, "style": rd.style}
    assert rep["prompts"]["tokenizers_identical"]
    rep["t_checks_s"] = time.time() - t0
    print("PREFLIGHT part 1 ok", json.dumps(rep["prompts"]), flush=True)
    try:
        rd = tt.Reader(dev="cpu")
        rep["c1_load_s"] = rd.load_s
        rep["model_class"] = type(rd.top).__name__
        rep["adapter_check"] = rd.adapter_check
        pick = [d for d in ds if d["suite"] in ("sst2", "ag_news", "xnli_en")][::97][:3] or ds[:3]
        preps = rd.prepare_many(pick, "main")
        jobs = [(s, p["groups"]) for p in preps for s in p["seqs"]]
        lg, _ = rd.read_jobs(jobs)
        k, items = 0, []
        for p in preps:
            n = len(p["seqs"])
            pr = rd.decide(p, lg[k:k + n])
            k += n
            items.append({"id": p["d"]["id"], "gold": p["d"]["gold"], "probs": pr})
        rep["items"] = items
        rep["adapter_effect_max_logit_diff_on_vs_off"] = rd.adapter_effect(preps[:2])
        assert rep["adapter_effect_max_logit_diff_on_vs_off"] > 1e-3
    except Exception as e:  # noqa: BLE001
        import traceback
        rep["cpu_model_error"] = f"{type(e).__name__}: {str(e)[:600]}"
        rep["cpu_model_traceback_tail"] = traceback.format_exc()[-1500:]
    rep["total_s"] = time.time() - t0
    rep["est_cost_usd"] = rep["total_s"] / 3600 * (8 * 0.047 + 28 * 0.0080)  # rough: CPU core-hour + GiB-hour list rates
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
    os.environ.update(HOME="/root", HF_HOME="/vol/hf", HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1")
    for d in ("results", "logs", "triton_cache"):
        os.makedirs(f"{RUN_ROOT}/{d}", exist_ok=True)
    run = run or time.strftime("run-%Y%m%d-%H%M%S", time.gmtime())
    gpu = sh("nvidia-smi --query-gpu=name,memory.total,memory.used,driver_version --format=csv,noheader")
    env = {"run": run, "start_utc": time.strftime("%F %T", time.gmtime(t0)), "gpu_nvidia_smi": gpu, "versions": versions(),
           "modal_task_id": os.environ.get("MODAL_TASK_ID"), "deadline_s": DEADLINE_S, "budget_s": BUDGET_S, "timeout_s": TIMEOUT_S,
           "nproc": os.cpu_count(), "loadavg": os.getloadavg(), "adapter_sha256": sha256_file(f"{ADAPTER}/adapter_model.safetensors")}
    assert env["adapter_sha256"].startswith("507d1c29"), env["adapter_sha256"]
    json.dump(env, open(f"{RUN_ROOT}/results/modal_env.json", "w"), indent=1)
    print("ENV", json.dumps(env), flush=True)
    chain_log = open(f"{RUN_ROOT}/logs/chain.log", "w")
    proc = subprocess.Popen([sys.executable, "-B", f"{RUN_ROOT}/harness/run_text.py", "eval", "--out", f"{RUN_ROOT}/results",
                             "--deadline-s", str(DEADLINE_S)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                            cwd=RUN_ROOT, start_new_session=True)

    def pump():
        for line in proc.stdout:
            chain_log.write(line); chain_log.flush()
            print("[chain]", line.rstrip()[:600], flush=True)

    stop = threading.Event()

    def syncer():
        while not stop.wait(60):
            try:
                _sync(run)
            except Exception as e:  # noqa: BLE001
                print("sync error", type(e).__name__, str(e)[:200], flush=True)

    threads = [threading.Thread(target=f, daemon=True) for f in (pump, syncer)]
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
    done = {"run": run, "chain_exit_code": rc, "budget_stop": budget_stop, "function_wall_s": wall, "gpu": gpu,
            "gpu_end": sh("nvidia-smi --query-gpu=name,memory.used --format=csv,noheader"),
            "end_utc": time.strftime("%F %T", time.gmtime()), "results_files": sorted(os.listdir(f"{RUN_ROOT}/results")),
            f"est_cost_usd_at_{RATE_PER_H}_per_h": wall / 3600 * RATE_PER_H}
    json.dump(done, open(f"{RUN_ROOT}/results/modal_done.json", "w"), indent=1)
    _sync(run)
    print("DONE", json.dumps(done), flush=True)
    return done


@app.local_entrypoint()
def main(mode: str = "preflight", run: str = ""):
    if os.environ.get("MODAL_PROFILE") != "mahadikarya44":
        raise SystemExit("set MODAL_PROFILE=mahadikarya44 (the only profile this job may use)")
    if mode == "preflight":
        print(json.dumps(preflight.remote(), indent=1))
    elif mode == "chain":
        print(json.dumps(chain.remote(run), indent=1))
    else:
        raise SystemExit("mode must be preflight or chain")
