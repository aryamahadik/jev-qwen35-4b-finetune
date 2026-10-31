"""modal_app: the Modal app of the 17 Oct 2026 C1 optimisation task (profile jaypatil-duke ONLY, hard cap USD 5.00).

  MODAL_PROFILE=jaypatil-duke ../../../.venv/bin/modal run modal_app.py::preflight          # CPU only, ~USD 0.05
  MODAL_PROFILE=jaypatil-duke ../../../.venv/bin/modal run modal_app.py::export_merged      # CPU only, ~USD 0.25 (once)
  ...

Rules enforced in code (oc1/common.py): payer guard (jaypatil-duke only, `modal run` only, no --detach), a persistent
spend ledger (oc1.common.Budget: stop launching at USD 4.50, cancel and stop at USD 4.80), one container per call
(max_containers=1), a hard timeout per function, no retries (a GPU is never relaunched by Modal).

Files in the containers (all read-only copies, nothing pinned is edited):
  /root/oc1         this task's package        /root/lean   decoder_io.py prism_x.py writeblock.py
  /root/hosting     fastcore/ + sglang_host.py (S1's server recipe and front end)
  /root/work        dev workloads P S N R (+ M), vision and voice packs
Volumes: /old = jaypatil-duke's `opendecide` (READ-ONLY: C1 adapter + base HF cache), /out = this task's Volume
(merged / fp8 / int8 checkpoints and result files).
"""
from __future__ import annotations

import ast
import json
import os
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import modal  # noqa: E402

from oc1 import common as C  # noqa: E402


def _modal_cli() -> str | None:
    a0 = Path(sys.argv[0]) if sys.argv else Path("")
    if a0.name == "modal" or (a0.name == "__main__.py" and a0.parent.name == "modal"):
        return next((a for a in sys.argv[1:] if not a.startswith("-")), "")
    return None


if modal.is_local() and _modal_cli() is not None:
    C.payer_guard()  # before an image is built or an app is created on the wrong account

LEAN = C.LEAN
REMOTE_OC1, REMOTE_LEAN, REMOTE_HOSTING, REMOTE_WORK = "/root/oc1", "/root/lean", "/root/hosting", "/root/work"
LEAN_FILES = ("decoder_io.py", "prism_x.py", "writeblock.py")


def read_pinned35() -> list:
    """C1's PINNED35 pip list, parsed as text from hosting/modal_direct_host.py (never imported: it builds a Modal app)."""
    src = (LEAN / "hosting" / "modal_direct_host.py").read_text()
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "PINNED35" for t in node.targets):
            return node.value.func.value.value.split()
    raise SystemExit("PINNED35 not found in hosting/modal_direct_host.py")


def build_sgl_image(pins: list | None = None):
    """S1's image: lmsysorg/sglang:v0.5.20-cu130 + /opt/fastpath (C1's PINNED35 stack), same build steps as
    hosting/sglang_host.py. Code and data are mounted at container start (not baked), so editing them never rebuilds."""
    pins = pins if pins is not None else read_pinned35()
    img = (
        modal.Image.from_registry(C.SGLANG_IMAGE)
        .run_commands(f"PIP_BREAK_SYSTEM_PACKAGES=1 python3 -m pip install --no-cache-dir {C.UV_PIN}",
                      "uv venv --python 3.12.10 /opt/fastpath",
                      f"uv pip install --no-cache --python {C.FASTPATH_PY} {' '.join(pins)}")
        .env({"HF_HOME": "/tmp/hf", "HF_HUB_ENABLE_HF_TRANSFER": "0", "TOKENIZERS_PARALLELISM": "false",
              "HF_HUB_OFFLINE": "1", "PYTHONDONTWRITEBYTECODE": "1"})
    )
    return img


def with_code(img):
    ignore = ["**/__pycache__/**", "**/*.pyc"]
    for n in LEAN_FILES:
        img = img.add_local_file(LEAN / n, f"{REMOTE_LEAN}/{n}")
    img = (img.add_local_dir(LEAN / "hosting" / "fastcore", f"{REMOTE_HOSTING}/fastcore", ignore=ignore)
           .add_local_file(LEAN / "hosting" / "sglang_host.py", f"{REMOTE_HOSTING}/sglang_host.py")
           .add_local_dir(HERE / "oc1", REMOTE_OC1, ignore=ignore))
    work = HERE / "data"
    if work.exists():
        img = img.add_local_dir(work, REMOTE_WORK, ignore=ignore)
    return img


PREFLIGHT_CPU, PREFLIGHT_MEM_GIB = 2.0, 8.0
FN_RATE_PREFLIGHT = C.container_rate_usd_h(None, PREFLIGHT_CPU, PREFLIGHT_MEM_GIB)

app = modal.App(C.APP_NAME)
if modal.is_local():
    sgl_image = with_code(build_sgl_image())
else:  # in the container the already-built image runs; this placeholder only satisfies the decorator
    sgl_image = modal.Image.debian_slim()
old_vol = modal.Volume.from_name(C.OLD_VOLUME).read_only()   # adapter + base HF cache: never written
out_vol = modal.Volume.from_name(C.NEW_VOLUME, create_if_missing=True)


@app.function(image=sgl_image, cpu=PREFLIGHT_CPU, memory=int(PREFLIGHT_MEM_GIB * 1024),
              volumes={"/old": old_vol, "/out": out_vol}, timeout=25 * 60, max_containers=1, retries=0)
def preflight_cpu(hash_shards: bool = True, run_help: bool = True) -> dict:
    """CPU-only inspection of the image, the Volumes and the Hub. Never loads a model; writes nothing but /tmp."""
    sys.path.insert(0, REMOTE_OC1.rsplit("/", 1)[0])  # /root
    from oc1 import export_pure as E
    from oc1 import preflight as P
    t0 = time.time()
    out = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "region": os.environ.get("MODAL_REGION"),
           "cloud": os.environ.get("MODAL_CLOUD_PROVIDER")}
    out["env"] = P.sglang_env(sys.executable)
    root = out["env"].get("sglang_dir")
    out["fastpath"] = P._run([C_FASTPATH_PY, "-c", "import torch,transformers,tokenizers,peft,safetensors;"
                              "print(torch.__version__,transformers.__version__,tokenizers.__version__,peft.__version__,"
                              "safetensors.__version__)"], timeout=300)
    out["volume"] = P.check_volume_c1("/old", "/out", E.BASE, E.REVISION, E.C1_ADAPTER_SHA256, E.BASE_PINS, E.MERGED_NAME,
                                      hash_shards=hash_shards)
    if run_help:
        out["launch_help"] = P.launch_help(sys.executable)
    if root:
        out["grep"] = P.grep_source(root, P.SOURCE_PATTERNS)
        out["score_api"] = P.find_def(root, "srt/entrypoints/openai/protocol.py", ["ScoringRequest", "ScoringResponse"])
        out["score_api"].update(P.find_def(root, "srt/managers/tokenizer_manager_score_mixin.py",
                                           ["score_request", "_convert_logprobs_to_scores", "_extract_logprobs_for_tokens"],
                                           max_lines=160))
        out["environ_rows"] = P.grep_source(root, {"envs": r"SGLANG_[A-Z0-9_]*(RADIX|GRAPH|VIT|ENCODER|MM_|SCORE|PREFILL)[A-Z0-9_]*"},
                                            max_hits=40)["hits"]["envs"]
    out["hf"] = P.hf_models()
    out["wall_s"] = round(time.time() - t0, 1)
    return out



@app.function(image=sgl_image, cpu=1.0, memory=4096, timeout=10 * 60, max_containers=1, retries=0)
def inspect_sglang_cpu(spec: list) -> dict:
    """Read-only look at the installed SGLang source (line slices, listings, greps). CPU, ~30 s."""
    sys.path.insert(0, REMOTE_OC1.rsplit("/", 1)[0])
    from oc1 import preflight as P
    t0 = time.time()
    root = P.sglang_env(sys.executable).get("sglang_dir")
    return {"root": root, "slices": P.inspect_sglang(root, spec), "wall_s": round(time.time() - t0, 1)}


EXPORT_CPU, EXPORT_MEM_GIB = 4.0, 32.0
FN_RATE_EXPORT = C.container_rate_usd_h(None, EXPORT_CPU, EXPORT_MEM_GIB)


@app.function(image=sgl_image, cpu=EXPORT_CPU, memory=int(EXPORT_MEM_GIB * 1024), volumes={"/old": old_vol, "/out": out_vol},
              timeout=45 * 60, max_containers=1, retries=0)
def export_merged(overwrite: bool = False, fresh: bool = False) -> dict:
    """C1 merged in BF16 on CPU (hosting/export_c1_merged.py's own functions, under C1's pinned stack), written to the
    task Volume as /out/models/q35_4b_main500k_merged; compared file by file with SPEED-2's merged checkpoint."""
    sys.path.insert(0, REMOTE_OC1.rsplit("/", 1)[0])
    from oc1 import preflight as P
    t0 = time.time()
    cmd = [C_FASTPATH_PY, "-m", "oc1.export_driver", "--old", "/old", "--out", "/out", "--result", "/tmp/export_result.json"]
    if fresh:
        cmd.append("--fresh")
    if overwrite:
        cmd.append("--overwrite")
    env = {**os.environ, "PYTHONPATH": "/root", "HF_HUB_OFFLINE": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    r = P._run(cmd, timeout=42 * 60, env=env)
    res = {}
    try:
        res = json.loads(Path("/tmp/export_result.json").read_text())
    except (OSError, ValueError):
        pass
    out_vol.commit()
    return {"rc": r["rc"], "tail": (r["out"] or "")[-1500:], "err": r["err"][-1500:], "result": res,
            "wall_s": round(time.time() - t0, 1)}


# ------------------------------------------------------------------ the H100 session
SESSION_REGION = os.environ.get("OC1_REGION", "any")                         # set by the launcher BEFORE `modal run`
SESSION_TIMEOUT_S = int(os.environ.get("OC1_SESSION_TIMEOUT_S", 58 * 60))
GPU_CPU, GPU_MEM_GIB = 4.0, 32.0
FN_RATE_GPU = C.container_rate_usd_h("H100", GPU_CPU, GPU_MEM_GIB, SESSION_REGION)
_REGION_KW = {} if SESSION_REGION == "any" else {"region": SESSION_REGION}
E2E_PORT = 8000


def _trim(ev: dict, limit: int = 60000) -> dict:
    """Queue-sized copy of an event: bulky record lists / answer maps stay on the Volume."""
    def cut(o, depth=0):
        if isinstance(o, dict):
            return {k: ("<%d records on the Volume>" % len(v) if k in ("records", "answers", "items") and isinstance(v, list) and len(v) > 20
                        else cut(v, depth + 1)) for k, v in o.items()}
        if isinstance(o, list):
            return [cut(x, depth + 1) for x in o[:60]]
        return o
    out = cut(ev)
    if len(json.dumps(out, default=str)) > limit:
        return {"event": ev.get("event"), "config": ev.get("config"), "truncated": True}
    return out


@app.function(image=sgl_image, gpu="H100!", cpu=GPU_CPU, memory=int(GPU_MEM_GIB * 1024), volumes={"/out": out_vol},
              timeout=SESSION_TIMEOUT_S, max_containers=1, retries=0, **_REGION_KW)
def gpu_session(plan: dict, q, token: str, prior_usd: float, run_id: str) -> dict:
    """One H100 container, config BLOCKS in priority order (oc1.session): boot SGLang, measure, vision / voice / e2e
    extras on the S1 block, stop, next. Every block is gated by the running spend; results go to the Volume as they end."""
    import subprocess
    import threading
    sys.path.insert(0, "/root")
    from oc1 import session as S
    t0 = time.time()
    run_dir = Path(f"/out/results/{run_id}")
    run_dir.mkdir(parents=True, exist_ok=True)
    evf = open(run_dir / "events.jsonl", "a")

    def emit(ev):
        ev = {"t": round(time.time() - t0, 1), **ev}
        evf.write(json.dumps(ev, default=str) + "\n")
        evf.flush()
        try:
            q.put(_trim(ev))
        except Exception:  # noqa: BLE001
            pass

    gpu = S.gpu_name()
    emit({"event": "container_up", "gpu": gpu, "region": os.environ.get("MODAL_REGION"), "cloud": os.environ.get("MODAL_CLOUD_PROVIDER")})
    if not gpu or "H100" not in gpu:
        emit({"event": "abort", "why": f"GPU is {gpu!r}, not an H100"})
        return {"error": f"GPU {gpu!r}"}
    want_region = plan.get("require_region_prefix")
    if want_region and not (os.environ.get("MODAL_REGION") or "").startswith(want_region):
        emit({"event": "abort", "why": f"container landed in {os.environ.get('MODAL_REGION')!r}; the end-to-end test needs a "
                                       f"{want_region!r}* region (relaunch with OC1_REGION=us)"})
        return {"error": "wrong region"}
    mdir = Path("/out/models") / C.MERGED_NAME
    man = json.loads((mdir / "merge_manifest.json").read_text())
    if man.get("adapter_sha256") != C.C1_ADAPTER_SHA256:
        emit({"event": "abort", "why": "merged checkpoint is not C1"})
        return {"error": "merged checkpoint is not C1"}
    ver = {}

    def verify():
        bad = []
        for rel, meta in sorted(man["files"].items()):
            if C.sha256_file(mdir / rel) != meta["sha256"]:
                bad.append(rel)
        ver["problems"] = bad
        emit({"event": "checkpoint_verified", "n_files": len(man["files"]), "problems": bad})
    threading.Thread(target=verify, daemon=True).start()

    sess_ref = {}

    def e2e_cb(cfg, srv, out_dir, front):
        """The front was started (and its tokenizer built) while the measurements ran; release it, open the tunnel, and
        wait until the laptop's /shutdown (or its own deadline) ends it."""
        ready = front.wait_ready(420)
        if not ready.get("ok"):
            return {"error": ready.get("error") or "front not ok", "tail": ready.get("tail")}
        with modal.forward(E2E_PORT) as tunnel:
            emit({"event": "e2e_ready", "url": tunnel.url, "config": cfg.name})
            q.put({"event": "e2e_ready", "url": tunnel.url, "config": cfg.name, "health_ok": ready["health"].get("ok")})
            front.runner.p.wait(timeout=front.spec["seconds"] + 60) if front.runner.alive() else None
        return {**front.finish(30), "boot": ready.get("boot")}

    def extra_cb(kind, cfg, srv, out_dir):
        if kind == "vision":
            pack = Path("/root/work/vision_pack")
            if not (pack / "items.jsonl").exists():
                return {"skipped": "no vision pack in the image"}
            spec = {"sgl_url": srv.url, "pack_dir": str(pack), **{k: v for k, v in plan["vision"].items() if k in ("caps", "upscale", "upscale_n")}}
            return S.run_runner("vision", spec, str(out_dir / "vision.json"), timeout_s=900, python=sys.executable)
        if kind == "voice_c1":
            vr, pf = Path("/out/voice/voice_result.json"), Path("/out/voice/prompts.json")
            if not (vr.exists() and pf.exists()):
                return {"skipped": "no voice transcripts on the Volume (run the voice step first)"}
            spec = {"config": cfg.name, "sgl_url": srv.url, "work_dir": "/root/work", "c1_dir": sess_ref["s"].c1_dir(),
                    "out_dir": str(out_dir), "voice_result": str(vr), "prompts_file": str(pf), "params": {}}
            return S.run_runner("voice_c1", spec, str(out_dir / "voice_c1.json"), timeout_s=900)
        return {"skipped": f"unknown extra {kind}"}

    sess = S.Session(plan, emit, models_root="/out/models", work_dir="/root/work", results_root=str(run_dir),
                     rate_usd_h=plan["rate_usd_h"], prior_usd=prior_usd, python=sys.executable, e2e_cb=e2e_cb, extra_cb=extra_cb,
                     commit=out_vol.commit, front_token=token,
                     host_info={"gpu": gpu, "region": os.environ.get("MODAL_REGION"), "run_id": run_id})
    sess_ref["s"] = sess
    try:
        res = sess.run()
    finally:
        out_vol.commit()
    res["checkpoint_verified"] = ver
    res["wall_s"] = round(time.time() - t0, 1)
    emit({"event": "session_done", "wall_s": res["wall_s"], "spent_usd": res["spent_usd"]})
    C.write_json(run_dir / "session_result.json", res)
    out_vol.commit()
    return {"wall_s": res["wall_s"], "spent_usd": res["spent_usd"], "blocks": {k: {kk: v.get(kk) for kk in ("boot_s", "error", "skipped", "spent_usd")}
                                                                              for k, v in res["results"].items()}}


# ------------------------------------------------------------------ voice: Kokoro TTS + Nemotron ASR (own image)
def build_voice_image():
    img = (modal.Image.debian_slim(python_version="3.12.10")
           .apt_install("espeak-ng", "libsndfile1", "ffmpeg")
           .pip_install("torch==2.14.0", "transformers==5.17.0", "kokoro==0.9.4", "misaki[en]==0.9.4", "soundfile", "scipy",
                        "numpy", "librosa", "huggingface_hub")
           .run_commands("python -m spacy download en_core_web_sm")
           .env({"HF_HOME": "/out/hf_voice", "PYTHONDONTWRITEBYTECODE": "1", "TOKENIZERS_PARALLELISM": "false"}))
    return img.add_local_dir(HERE / "oc1", REMOTE_OC1, ignore=["**/__pycache__/**", "**/*.pyc"])


if modal.is_local():
    voice_image = build_voice_image()
else:
    voice_image = modal.Image.debian_slim()


@app.function(image=voice_image, cpu=4.0, memory=16384, volumes={"/out": out_vol}, timeout=25 * 60, max_containers=1, retries=0)
def voice_smoke_cpu(texts: list) -> dict:
    """CPU smoke test of the voice code path: Kokoro on a few sentences, Nemotron ASR offline + streaming (0.16 s, 0.56 s)."""
    sys.path.insert(0, "/root")
    from oc1 import voice as V
    t0 = time.time()
    out = {"versions": {}}
    import importlib
    for m in ("torch", "transformers", "kokoro", "misaki", "scipy", "numpy", "librosa", "huggingface_hub"):
        try:
            out["versions"][m] = getattr(importlib.import_module(m), "__version__", "?")
        except Exception as e:  # noqa: BLE001
            out["versions"][m] = f"MISSING {type(e).__name__}"
    prompts = [{"id": f"t{i}", "text": t, "qtype": "noul", "request": {}} for i, t in enumerate(texts)]
    try:
        res = V.run_voice({"prompts": prompts, "device": "cpu"}, log=lambda s: print(s, flush=True))
        out["result"] = {k: res[k] for k in ("n", "audio_s", "tts_s", "tts_rtf", "modes", "wall_s")}
        out["items"] = [{k: v for k, v in it.items() if k != "text"} for it in res["items"]]
        out["ok"] = True
    except Exception as e:  # noqa: BLE001
        import traceback
        out["ok"], out["error"], out["trace"] = False, f"{type(e).__name__}: {str(e)[:500]}", traceback.format_exc()[-2500:]
    out_vol.commit()
    out["wall_s"] = round(time.time() - t0, 1)
    return out


@app.function(image=voice_image, gpu="L4", cpu=4.0, memory=16384, volumes={"/out": out_vol}, timeout=20 * 60, max_containers=1, retries=0)
def voice_gpu(prompts: list, device: str = "cuda") -> dict:
    """TTS (Kokoro) + ASR (Nemotron streaming 0.16 s / 0.56 s + offline) on a GPU; transcripts and latencies to the Volume."""
    sys.path.insert(0, "/root")
    from oc1 import voice as V
    t0 = time.time()
    import torch
    gpu = torch.cuda.get_device_name() if torch.cuda.is_available() else None
    res = V.run_voice({"prompts": prompts, "device": device}, log=lambda s: print(s, flush=True))
    res["gpu"] = gpu
    d = Path("/out/voice")
    d.mkdir(parents=True, exist_ok=True)
    C.write_json(d / "voice_result.json", res)
    C.write_json(d / "prompts.json", prompts)
    out_vol.commit()
    res["wall_s_total"] = round(time.time() - t0, 1)
    return {k: res[k] for k in ("gpu", "n", "audio_s", "tts_s", "tts_rtf", "modes", "wall_s", "wall_s_total")}


# ------------------------------------------------------------------ CPU dry run of the whole Python side in the real image
DRY_CPU, DRY_MEM_GIB = 4.0, 12.0
FN_RATE_DRY = C.container_rate_usd_h(None, DRY_CPU, DRY_MEM_GIB)


@app.function(image=sgl_image, cpu=DRY_CPU, memory=int(DRY_MEM_GIB * 1024), volumes={"/out": out_vol}, timeout=20 * 60,
              max_containers=1, retries=0)
def dryrun_cpu() -> dict:
    """prep -> measure -> front + load client, against a model-free STUB server, in the real image with the real
    tokenizer: proves the container paths / versions / JSON shapes, and finds the CPU ceiling of the Python front end."""
    import subprocess
    import threading
    sys.path.insert(0, "/root")
    from oc1 import loadgen as LG
    from oc1 import session as S
    from oc1 import stubserver as ST
    from oc1 import vision as V
    t0 = time.time()
    out = {"steps": {}}
    c1 = str(Path("/out/models") / C.MERGED_NAME / "c1_tokenizer")
    run = Path("/tmp/dry")
    run.mkdir(exist_ok=True)
    stub = ST.StubSGLang(port=30000, service_ms=0.0).start()

    def step(name, fn):
        t = time.time()
        try:
            out["steps"][name] = fn()
        except Exception as e:  # noqa: BLE001
            import traceback
            out["steps"][name] = {"error": f"{type(e).__name__}: {str(e)[:300]}", "trace": traceback.format_exc()[-1200:]}
        out["steps"][name]["wall_s"] = round(time.time() - t, 1)

    step("prep", lambda: S.run_runner("prep", {"work_dir": "/root/work", "c1_dir": c1, "out_dir": str(run), "workloads": ["N", "S", "R", "P"]},
                                       str(run / "prep.json"), timeout_s=900, log=lambda s: None))
    params = {"sub_n": 600, "parity_conc": 16, "lat_n": 60, "lat_s": 30, "lat_warm": 5, "lat_rounds": 6, "tp_conc": [16, 64],
              "prefix_n": 100, "prefix_conc": 8}
    step("measure", lambda: S.run_runner("measure", {"config": "dry", "sgl_url": stub.url, "work_dir": "/root/work", "c1_dir": c1,
                                                      "out_dir": str(run / "dry"), "measures": ["parity_sub", "latency", "throughput", "prefix", "score_readout"],
                                                      "params": params}, str(run / "dry" / "measure.json"), timeout_s=900, log=lambda s: None))

    def front_ceiling():
        spec = {"sglang_url": stub.url, "c1_tokenizer_dir": c1, "port": E2E_PORT, "host": "127.0.0.1", "seconds": 300, "idle_s": 200,
                "wait_ms": 0.0, "shed_at": 10 ** 9, "ready_file": str(run / "ready.json"), "done_file": str(run / "done.json"),
                "warm_requests": 3, "max_inflight": 256, "t0": time.time()}
        (run / "fspec.json").write_text(json.dumps(spec))
        env = {**os.environ, "PYTHONPATH": "/root", "OC1_TOKEN": "dry", "HF_HUB_OFFLINE": "1"}
        env.pop("VIRTUAL_ENV", None)
        p = subprocess.Popen([C.FASTPATH_PY, "-m", "oc1.runner", "front", "--spec", str(run / "fspec.json"), "--out", str(run / "fout.json")],
                             cwd="/root", env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        tail = []
        threading.Thread(target=lambda: [tail.append(l.rstrip()) for l in p.stdout], daemon=True).start()
        t_w = time.time()
        while not (run / "ready.json").exists():
            if p.poll() is not None or time.time() - t_w > 300:
                return {"error": "front did not start", "tail": tail[-15:]}
            time.sleep(1)
        url = f"http://127.0.0.1:{E2E_PORT}"
        reqs = [it["request"] for it in C.read_jsonl("/root/work/P.jsonl")]
        import random
        random.Random(0).shuffle(reqs)
        levels = [{"name": f"qps{q}", "qps": q, "duration_s": 8, "warm_s": 2} for q in (10, 30, 60, 100)]
        res = LG.e2e_levels(url, "dry", reqs, levels, log=lambda s: None, workers=64)
        adm = LG.Admin(url, "dry")
        try:
            adm.post("/shutdown")
        finally:
            adm.close()
        slim = [{k: (v if not isinstance(v, dict) or k in ("server_mark", "settings") else {kk: v[kk] for kk in ("n", "p50", "p95") if kk in v})
                 for k, v in lv.items() if k in ("name", "qps_target", "qps_achieved", "ok", "errors", "total_ms", "server_ms", "tokenize_ms",
                                                 "client_queue_ms", "server_mark")} for lv in res]
        return {"levels": slim, "tail": tail[-3:]}
    step("front_loopback", front_ceiling)

    def pypatch():
        env = {**os.environ, "PYTHONPATH": "/root/oc1/pypatch", "OC1_ONLINE_MODE": "fp8", "OC1_IGNORE": json.dumps(["in_proj_ba", "visual"]),
               "OC1_REPORT": "/tmp/dry/qrep.jsonl", "HF_HUB_OFFLINE": "1"}
        r = subprocess.run([sys.executable, "-c", "import sglang.srt.layers.quantization.w8a8_fp8 as m; "
                            "print(m.W8A8Fp8Config.get_quant_method.__module__, m.W8A8Fp8Config.get_quant_method.__name__)"],
                           capture_output=True, text=True, env=env, timeout=600)
        rep = Path("/tmp/dry/qrep.jsonl")
        return {"rc": r.returncode, "out": r.stdout.strip()[-300:], "err": r.stderr.strip()[-600:],
                "report": rep.read_text()[:600] if rep.exists() else None}
    step("pypatch_import", pypatch)

    def pil():
        from PIL import Image
        import io
        im = Image.new("RGB", (375, 500), (120, 80, 40))
        p = Path("/tmp/dry/im.png")
        im.save(p)
        res = {}
        for cap in (None, 256, 128, 64):
            b, hw, pt = V.prepare_image(p, cap)
            res[str(cap)] = {"hw": list(hw), "tokens": pt, "bytes": len(b)}
        b, hw, pt = V.prepare_image(p, None, upscale_to=2048)
        res["upscale2048"] = {"hw": list(hw), "tokens": pt}
        return res
    step("vision_prepare_image", pil)
    stub.close()
    out["wall_s"] = round(time.time() - t0, 1)
    return out


# ------------------------------------------------------------------ network probe: where is the latency outside the GPU
if modal.is_local():
    echo_image = modal.Image.debian_slim(python_version="3.12.10").add_local_dir(HERE / "oc1", REMOTE_OC1, ignore=["**/__pycache__/**", "**/*.pyc"])
else:
    echo_image = modal.Image.debian_slim()


@app.function(image=echo_image, cpu=0.5, memory=512, timeout=8 * 60, max_containers=1, retries=0)
def echo_server(q, token: str, seconds: int = 150) -> dict:
    """Stdlib echo behind modal.forward: GET /ping, POST /decide (small JSON back). CPU only."""
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    stop = threading.Event()

    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        disable_nagle_algorithm = True

        def _ok(self, obj):
            b = json.dumps(obj).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def do_GET(self):
            self._ok({"ok": True})

        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            self.rfile.read(n)
            if self.path == "/shutdown":
                stop.set()
            self._ok({"answers": {}, "server_ms": 0.1, "timing": {"tokenize_ms": 0.0, "queue_ms": 0.0, "model_ms": 0.0, "readout_ms": 0.0}})

        def log_message(self, *a):
            pass

    srv = ThreadingHTTPServer(("0.0.0.0", 8000), H)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    with modal.forward(8000) as tunnel:
        q.put({"url": tunnel.url, "region": os.environ.get("MODAL_REGION"), "cloud": os.environ.get("MODAL_CLOUD_PROVIDER")})
        stop.wait(seconds)
    srv.shutdown()
    return {"region": os.environ.get("MODAL_REGION")}


@app.function(image=sgl_image, gpu="L4", cpu=4.0, memory=32768, volumes={"/out": out_vol}, timeout=25 * 60, max_containers=1, retries=0)
def smooth_gpu(alpha: float = 0.5, n: int = 96) -> dict:
    """SmoothQuant calibration + transform of the merged checkpoint on an L4 (OPTIONAL: only for the int8_sq arm)."""
    sys.path.insert(0, REMOTE_OC1.rsplit("/", 1)[0])
    from oc1 import preflight as P
    t0 = time.time()
    src, dst = f"/out/models/{C.MERGED_NAME}", f"/out/models/{C.MERGED_NAME}__smooth"
    r = P._run([C_FASTPATH_PY, "-m", "oc1.smooth_run", "--src", src, "--dst", dst, "--n", str(n), "--alpha", str(alpha)],
               timeout=22 * 60, env={**os.environ, "PYTHONPATH": "/root", "HF_HUB_OFFLINE": "1", "PYTHONDONTWRITEBYTECODE": "1"})
    out_vol.commit()
    return {"rc": r["rc"], "out": r["out"][-1500:], "err": r["err"][-1500:], "wall_s": round(time.time() - t0, 1)}


C_FASTPATH_PY = C.FASTPATH_PY


# ------------------------------------------------------------------ local side: billed calls with the budget governor
def run_billed(budget: C.Budget, name: str, call, rate_h: float, est_s: float, timeout_s: float, poll_s: float = 15.0):
    """Wait for a spawned FunctionCall under the budget governor. The ledger segment is opened by the caller BEFORE spawn.
    Cancels the call and raises when the running estimate reaches the hard stop or `timeout_s` passes."""
    t0 = time.time()
    while True:
        try:
            res = call.get(timeout=poll_s)
            return res
        except (modal.exception.TimeoutError, TimeoutError):
            pass
        if budget.must_cancel():
            call.cancel()
            raise C.BudgetExceeded(f"{name}: hard stop at ${budget.spent():.2f}: call cancelled")
        if time.time() - t0 > timeout_s:
            call.cancel()
            raise TimeoutError(f"{name}: no result after {timeout_s:.0f} s: call cancelled")


@app.local_entrypoint()
def preflight(hash_shards: bool = True, run_help: bool = True):
    """CPU-only preflight (image, Volumes, base-model and C1-adapter shas, SGLang flags, Hub repos). ~USD 0.05."""
    prof = C.payer_guard()
    bud = C.Budget()
    est_s = 20 * 60
    est = C.container_cost_usd(est_s, FN_RATE_PREFLIGHT)
    bud.check_launch("preflight", est)
    print(f"payer {prof}; preflight worst case ${est:.3f}; spent so far {json.dumps(bud.summary())}", flush=True)
    name = f"preflight-{int(time.time())}"
    bud.open(name, FN_RATE_PREFLIGHT)
    res, err = None, None
    try:
        call = preflight_cpu.spawn(hash_shards=hash_shards, run_help=run_help)
        res = run_billed(bud, name, call, FN_RATE_PREFLIGHT, est_s, 25 * 60)
    except BaseException as e:  # noqa: BLE001
        err = f"{type(e).__name__}: {e}"
        raise
    finally:
        bud.close(name, (res or {}).get("wall_s") if isinstance(res, dict) else None)
        out = C.RESULTS / f"preflight_{time.strftime('%Y%m%d_%H%M%S', time.gmtime())}.json"
        C.write_json(out, {"result": res, "error": err, "budget": bud.summary()})
        print(f"wrote {out}; budget {json.dumps(bud.summary())}", flush=True)


@app.local_entrypoint()
def inspect(spec_file: str):
    """Run inspect_sglang_cpu with a JSON spec file (list of slices / greps / listings). CPU only, ~USD 0.01."""
    prof = C.payer_guard()
    bud = C.Budget()
    rate = C.container_rate_usd_h(None, 1.0, 4.0)
    est = C.container_cost_usd(10 * 60, rate)
    bud.check_launch("inspect", est)
    spec = json.loads(Path(spec_file).read_text())
    name = f"inspect-{int(time.time())}"
    bud.open(name, rate)
    res = None
    try:
        call = inspect_sglang_cpu.spawn(spec)
        res = run_billed(bud, name, call, rate, 120, 10 * 60)
    finally:
        bud.close(name, (res or {}).get("wall_s") if isinstance(res, dict) else None)
        out = C.RESULTS / f"inspect_{time.strftime('%Y%m%d_%H%M%S', time.gmtime())}.json"
        C.write_json(out, {"result": res, "budget": bud.summary()})
        print(f"wrote {out}; budget {json.dumps(bud.summary())}", flush=True)


@app.local_entrypoint()
def export(overwrite: bool = False, fresh: bool = False):
    """C1 merged checkpoint on the task Volume (CPU, ~25 min, ~USD 0.2). Idempotent: an existing verified export is re-checked."""
    prof = C.payer_guard()
    bud = C.Budget()
    est_s = 40 * 60
    est = C.container_cost_usd(est_s, FN_RATE_EXPORT)
    bud.check_launch("export_merged", est)
    print(f"payer {prof}; export worst case ${est:.2f}; budget {json.dumps(bud.summary())}", flush=True)
    name = f"export-{int(time.time())}"
    bud.open(name, FN_RATE_EXPORT)
    res = None
    try:
        call = export_merged.spawn(overwrite=overwrite, fresh=fresh)
        res = run_billed(bud, name, call, FN_RATE_EXPORT, 25 * 60, 45 * 60)
    finally:
        bud.close(name, (res or {}).get("wall_s") if isinstance(res, dict) else None)
        out = C.RESULTS / f"export_{time.strftime('%Y%m%d_%H%M%S', time.gmtime())}.json"
        C.write_json(out, {"result": res, "budget": bud.summary()})
        print(f"wrote {out}; budget {json.dumps(bud.summary())}", flush=True)
    r = (res or {}).get("result") or {}
    print(json.dumps({k: r.get(k) for k in ("status", "checks_passed", "n_files", "wall_s")}))
    print(json.dumps(r.get("compare_with_speed2")))


# ------------------------------------------------------------------ local entrypoints: generic billed call + the session
def _billed(bud, name, spawn, rate, est_s, timeout_s, tag=None):
    """spawn() -> FunctionCall. Opens/closes the ledger segment around it, returns the result (or raises)."""
    est = C.container_cost_usd(est_s, rate)
    bud.check_launch(name, est)
    bud.open(name, rate)
    res = None
    try:
        call = spawn()
        res = run_billed(bud, name, call, rate, est_s, timeout_s)
        return res
    finally:
        bud.close(name, (res or {}).get("wall_s") if isinstance(res, dict) else None)


def _save(name, obj, bud):
    out = C.RESULTS / f"{name}_{time.strftime('%Y%m%d_%H%M%S', time.gmtime())}.json"
    C.write_json(out, {"result": obj, "budget": bud.summary()})
    print(f"wrote {out}; budget {json.dumps(bud.summary())}", flush=True)
    return out


@app.local_entrypoint()
def dryrun():
    """CPU dry run of prep / runner / front / load client / pypatch / PIL in the real image against a stub server. ~USD 0.04."""
    C.payer_guard()
    bud = C.Budget()
    res = None
    try:
        res = _billed(bud, f"dryrun-{int(time.time())}", lambda: dryrun_cpu.spawn(), FN_RATE_DRY, 8 * 60, 21 * 60)
    finally:
        _save("dryrun", res, bud)
    if res:
        print(json.dumps({k: (v.get("error") or {kk: v.get(kk) for kk in ("wall_s", "levels") if kk in v}) for k, v in res["steps"].items()},
                         default=str)[:3000])


@app.local_entrypoint()
def voicesmoke():
    """Build the voice image and run Kokoro + Nemotron ASR on 3 sentences on CPU (offline + 0.16 s + 0.56 s streaming). ~USD 0.05."""
    C.payer_guard()
    bud = C.Budget()
    rate = C.container_rate_usd_h(None, 4.0, 16.0)
    texts = ["The package I ordered last week still has not arrived and I would like a refund.",
             "Please cancel my subscription before the next billing date.",
             "I think the new update made the app much slower on my phone."]
    res = None
    try:
        res = _billed(bud, f"voicesmoke-{int(time.time())}", lambda: voice_smoke_cpu.spawn(texts), rate, 10 * 60, 26 * 60)
    finally:
        _save("voicesmoke", res, bud)
    if res:
        print(json.dumps({"ok": res.get("ok"), "error": res.get("error"), "versions": res.get("versions"),
                          "modes": (res.get("result") or {}).get("modes")}, default=str)[:3000])


@app.local_entrypoint()
def netprobe(regions: str = "any,us,us-east", n: int = 60):
    """RTT from THIS laptop to a CPU echo server in each region through modal.forward (TLS): ping and small POST, per-stage."""
    import secrets
    from oc1 import loadgen as LG
    C.payer_guard()
    bud = C.Budget()
    rate = C.container_rate_usd_h(None, 0.5, 0.5)
    out = {}
    for region in [r.strip() for r in regions.split(",") if r.strip()]:
        token = secrets.token_urlsafe(12)
        name = f"echo-{region}-{int(time.time())}"
        bud.check_launch(name, C.container_cost_usd(300, rate))
        bud.open(name, rate)
        fn = echo_server if region == "any" else echo_server.with_options(region=region)
        try:
            with modal.Queue.ephemeral() as q:
                call = fn.spawn(q, token, 150)
                t0 = time.time()
                msg = None
                while msg is None:
                    try:
                        msg = q.get(timeout=15)
                    except Exception:  # noqa: BLE001
                        try:
                            call.get(timeout=0)            # returned or raised before publishing a URL = failed
                            raise SystemExit(f"echo server in {region} ended before publishing a URL")
                        except (modal.exception.TimeoutError, TimeoutError):
                            pass
                        if time.time() - t0 > 300:
                            call.cancel()
                            raise SystemExit(f"echo server in {region} did not come up")
                url = msg["url"]
                admin = LG.make_client(url, token)
                admin.get("/ping")
                pings, recs = [], []
                for _ in range(n):
                    t = time.perf_counter()
                    admin.get("/ping")
                    pings.append((time.perf_counter() - t) * 1000)
                for _ in range(n):
                    recs.append(LG.timed_post(admin, "/decide", {"state": "x", "questions": {}}))
                cold = []
                for _ in range(8):
                    c = LG.make_client(url, token)
                    recs_c = LG.timed_post(c, "/decide", {"state": "x"})
                    cold.append(recs_c)
                    c.close()
                admin.post("/shutdown")
                admin.close()
                out[region] = {"container_region": msg.get("region"), "cloud": msg.get("cloud"), "ping_ms": C.summarize(pings),
                               "post_total_ms": C.summarize([r["total_ms"] for r in recs if r["ok"]]),
                               "post_wait_ms": C.summarize([r["wait_ms"] for r in recs if r.get("wait_ms") is not None]),
                               "new_conn_total_ms": C.summarize([r["total_ms"] for r in cold if r["ok"]]),
                               "connect_ms": C.summarize([r["connect_ms"] for r in cold if r.get("connect_ms") is not None]),
                               "tls_ms": C.summarize([r["tls_ms"] for r in cold if r.get("tls_ms") is not None])}
                try:
                    call.get(timeout=60)
                except Exception:  # noqa: BLE001
                    call.cancel()
        finally:
            bud.close(name, None)
        print(region, json.dumps(out.get(region)), flush=True)
    _save("netprobe", out, bud)


def _e2e_worker(url: str, token: str, plan: dict, out_dir: Path, jev: bool, log=print):
    """Laptop side of the end-to-end test: Poisson levels, then the interleaved c=1 comparison with Jev, then /shutdown."""
    import random
    from oc1 import loadgen as LG
    res = {"url_host": url.split("//")[-1].split("/")[0], "started_utc": C.utc()}
    admin = LG.Admin(url, token)
    try:
        t0 = time.time()
        while True:
            try:
                h = admin.get("/health")
                if h.get("ok"):
                    break
            except Exception:  # noqa: BLE001
                pass
            if time.time() - t0 > 180:
                raise RuntimeError("front /health never ok")
            time.sleep(2)
        res["health"] = {k: h.get(k) for k in ("engine", "model", "adapter_sha256", "gpu", "region", "config_sha256", "server_args")}
        reqs = [it["request"] for it in C.read_jsonl(C.ROOT / "data" / "P.jsonl")]
        random.Random(7).shuffle(reqs)
        res["levels"] = LG.e2e_levels(url, token, reqs, plan["e2e"]["levels"], log=log, workers=plan["e2e"].get("workers", 64))
        if jev:
            n_req = [it["request"] for it in C.read_jsonl(C.ROOT / "data" / "N.jsonl")]
            try:
                res["interleaved_c1"] = LG.interleaved_c1(url, token, n_req[:plan["e2e"]["jev_interleaved_n"]],
                                                          n=plan["e2e"]["jev_interleaved_n"], log=log)
            except BaseException as e:  # noqa: BLE001
                res["interleaved_c1"] = {"error": f"{type(e).__name__}: {str(e)[:200]}"}
        res["health_after"] = {k: v for k, v in admin.get("/health").items() if k in ("served", "errors", "shed", "coalescer", "batcher")}
    except BaseException as e:  # noqa: BLE001
        res["error"] = f"{type(e).__name__}: {str(e)[:300]}"
    finally:
        try:
            admin.post("/shutdown")
        except Exception:  # noqa: BLE001
            pass
        admin.close()
        res["finished_utc"] = C.utc()
        C.write_json(out_dir / "e2e_client.json", res)
    return res


@app.local_entrypoint()
def session(configs: str = "", jev: bool = True, e2e: bool = True, vision: bool = True, voice: bool = True,
            plan_only: bool = False, jev_n: int = 200, vision_caps: str = "", vision_upscale: str = ""):
    """THE H100 session (one container, blocks in priority order). Run ONLY after the GO:
         OC1_REGION=any MODAL_PROFILE=jaypatil-duke ../../../.venv/bin/modal run modal_app.py::session
       --plan-only prints the plan and the estimate and starts nothing."""
    import queue as _queue
    import secrets
    import subprocess
    import threading
    from oc1 import loadgen as LG
    from oc1 import plan as PL
    prof = C.payer_guard()
    bud = C.Budget()
    plan = PL.default_plan(SESSION_REGION, [c for c in configs.split(",") if c] or None, e2e=e2e, vision=vision, voice=voice,
                           jev_sample_n=jev_n)
    plan["rate_usd_h"] = round(FN_RATE_GPU, 4)
    if not e2e:            # the US-region rule exists only for the Jev same-client comparison; parity/throughput/vision do not depend on it
        plan["require_region_prefix"] = None
    if vision_caps:        # e.g. "native,256,64" (second session: only the arms that still matter)
        plan["vision"]["caps"] = [None if c == "native" else int(c) for c in vision_caps.split(",") if c]
    if vision_upscale:     # "none" = no upscale arms, else e.g. "2048"
        plan["vision"]["upscale"] = [] if vision_upscale == "none" else [int(u) for u in vision_upscale.split(",") if u]
    if vision_caps or vision_upscale:
        plan["vision"]["est_s"] = 40 + 45 * (len(plan["vision"]["caps"]) + (1 if plan["vision"]["upscale"] else 0))
    print(PL.render(plan), flush=True)
    est1 = PL.block_seconds(__import__("oc1.configs", fromlist=["x"]).CONFIGS[plan["configs"][0]], plan) / 3600 * FN_RATE_GPU
    print(f"payer {prof}; region {SESSION_REGION}; budget {json.dumps(bud.summary())}; first block ~${est1:.2f}", flush=True)
    if plan_only:
        return
    bud.check_launch("gpu_session", est1)
    run_id = time.strftime("session_%Y%m%d_%H%M%S", time.gmtime())
    out_dir = C.RESULTS / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    C.write_json(out_dir / "plan.json", plan)
    token = secrets.token_urlsafe(24)
    jev_state = {}
    if jev:
        def jev_job():
            try:
                reqs = [it["request"] for it in C.read_jsonl(C.ROOT / "data" / "N.jsonl")]
                jev_state["res"] = LG.jev_calls(reqs[300:300 + jev_n], n=jev_n, max_usd=0.10)
                bud.add_extra("OpenRouter Jev sample (estimate)", jev_state["res"]["est_spend_usd"])
                C.write_json(out_dir / "jev_sample.json", jev_state["res"])
                print(f"jev sample: {jev_state['res']['calls']} calls, p50 {jev_state['res']['client_ms'].get('p50')} ms", flush=True)
            except BaseException as e:  # noqa: BLE001
                jev_state["error"] = f"{type(e).__name__}: {str(e)[:200]}"
                print("jev sample failed: " + jev_state["error"], flush=True)
        threading.Thread(target=jev_job, daemon=True).start()
    name = f"gpu_session-{run_id}"
    bud.open(name, FN_RATE_GPU)
    result, e2e_thread, front_url = None, None, None
    events = open(out_dir / "events_local.jsonl", "a")
    t0 = time.time()
    try:
        with modal.Queue.ephemeral() as q:
            call = gpu_session.spawn(plan, q, token, bud.spent_closed() + (0.10 if jev else 0.0) + 0.05, run_id)   # + Jev + storage reserve
            t_spawn = time.time()
            cold = {}
            while True:
                try:
                    ev = q.get(timeout=5)
                except _queue.Empty:
                    ev = None
                except Exception:  # noqa: BLE001
                    ev = None
                if ev:
                    events.write(json.dumps(ev, default=str) + "\n")
                    events.flush()
                    kind = ev.get("event")
                    if kind == "container_up" and "spawn_to_container_up_s" not in cold:
                        cold["spawn_to_container_up_s"] = round(time.time() - t_spawn, 1)       # GPU queue + container start + mounts
                    if kind == "booted" and ev.get("config") == "s1" and "s1_boot_s" not in cold:
                        cold["s1_boot_s"] = ev.get("boot_s")
                        cold["cold_start_total_s"] = round(cold.get("spawn_to_container_up_s", 0) + (ev.get("boot_s") or 0), 1)
                        C.write_json(out_dir / "cold_start.json", cold)
                    if kind in ("container_up", "block_start", "booted", "block_end", "block_skipped", "abort", "hard_stop",
                                "checkpoint_verified", "prep_done", "session_done"):
                        brief = {k: ev.get(k) for k in ("config", "spent_usd", "boot_s", "error", "skipped", "gpu", "region", "problems", "why") if ev.get(k) is not None}
                        print(f"[{ev.get('t', 0):7.1f}s] {kind} {json.dumps(brief, default=str)[:400]}", flush=True)
                    if kind == "e2e_ready" and e2e_thread is None:
                        front_url = ev["url"]
                        e2e_thread = threading.Thread(target=_e2e_worker, args=(front_url, token, plan, out_dir, jev, print), daemon=True)
                        e2e_thread.start()
                if bud.must_cancel():
                    print(f"HARD STOP at ${bud.spent():.2f}: cancelling the H100 call", flush=True)
                    if front_url:
                        try:
                            LG.Admin(front_url, token).post("/shutdown")
                        except Exception:  # noqa: BLE001
                            pass
                    call.cancel()
                    break
                try:
                    result = call.get(timeout=0)
                    break
                except (modal.exception.TimeoutError, TimeoutError):
                    pass
                if time.time() - t0 > SESSION_TIMEOUT_S + 180:
                    call.cancel()
                    break
            if e2e_thread is not None:
                e2e_thread.join(timeout=60)
    except KeyboardInterrupt:
        print("interrupted: the H100 call is cancelled", flush=True)
        try:
            call.cancel()
        except Exception:  # noqa: BLE001
            pass
    finally:
        bud.close(name, (result or {}).get("wall_s") if isinstance(result, dict) else None)
        C.write_json(out_dir / "session_return.json", {"result": result, "budget": bud.summary(), "jev": {k: v for k, v in jev_state.items() if k != "res"}})
        subprocess.run([str(Path(sys.executable).parent / "modal"), "volume", "get", "--force", C.NEW_VOLUME, f"results/{run_id}",
                        str(out_dir / "volume")], env={**os.environ, "MODAL_PROFILE": C.PROFILE}, capture_output=True, timeout=300)
        print(f"session done; budget {json.dumps(bud.summary())}; results in {out_dir}", flush=True)


@app.local_entrypoint()
def voicegpu(gpu: str = "L4"):
    """TTS + ASR on a GPU (default L4, ~USD 0.1; --gpu 'H100!' ~USD 0.4): 100 dev prompts spoken by Kokoro, transcribed by Nemotron
    streaming (0.16 s / 0.56 s chunks) and offline; transcripts + latencies -> Volume /voice (read by the S1 block's voice_c1 step)."""
    C.payer_guard()
    bud = C.Budget()
    prompts = json.loads((C.ROOT / "data" / "voice_prompts.json").read_text())
    rate = C.container_rate_usd_h(gpu, 4.0, 16.0)
    fn = voice_gpu if gpu == "L4" else voice_gpu.with_options(gpu=gpu)
    res = None
    try:
        res = _billed(bud, f"voicegpu-{int(time.time())}", lambda: fn.spawn(prompts, "cuda"), rate, 8 * 60, 21 * 60)
    finally:
        _save("voicegpu", res, bud)
    if res:
        print(json.dumps({k: res.get(k) for k in ("gpu", "n", "tts_rtf", "wall_s_total")}))
        print(json.dumps({m: {k: v.get(k) for k in ("wer_mean", "final_flush_ms", "total_ms")} for m, v in (res.get("modes") or {}).items()}, default=str)[:2000])


@app.local_entrypoint()
def smoothgpu(alpha: float = 0.5, n: int = 96):
    """OPTIONAL (INT8 SmoothQuant arm): calibrate on an L4 and write q35_4b_main500k_merged__smooth to the Volume. ~USD 0.1."""
    C.payer_guard()
    bud = C.Budget()
    rate = C.container_rate_usd_h("L4", 4.0, 32.0)
    res = None
    try:
        res = _billed(bud, f"smoothgpu-{int(time.time())}", lambda: smooth_gpu.spawn(alpha, n), rate, 12 * 60, 26 * 60)
    finally:
        _save("smoothgpu", res, bud)
    if res:
        print(json.dumps({k: res.get(k) for k in ("rc", "wall_s")}), (res.get("out") or "")[-600:])
