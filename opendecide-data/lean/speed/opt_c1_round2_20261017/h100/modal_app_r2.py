"""modal_app_r2: the ONE H100 window of 17 Oct 2026 (round 2): C1 serving trials. Payer jaypatil-duke ONLY, hard cap USD 5.00.

  OC1_REGION=any MODAL_PROFILE=jaypatil-duke ../../../../.venv/bin/modal run modal_app_r2.py::plan           # prints the plan, starts nothing
  OC1_REGION=any MODAL_PROFILE=jaypatil-duke ../../../../.venv/bin/modal run modal_app_r2.py::session        # the window

Money (oc1.common.Budget, FRESH ledger h100/ledger.json): stop launching at USD 4.50, cancel at 4.80, cap 5.00. One container
(max_containers=1, no retries), one `modal run` (no --detach: Ctrl-C on the laptop cancels the GPU call).

Code and data are mounted at container start (not baked): /root/oc1 (this folder's package), /root/r2pypatch, /root/extra
(option ids), /root/work (the 17 Oct workloads P N R, the SPEED-2 reference answers, the 200-image pack: dev data only),
/root/lean + /root/hosting (decoder_io, fastcore, sglang_host: the exact S1 server recipe and readout).
Volume /out (oc1-opt-20261017): the merged C1 checkpoint (17 Oct), the block-FP8 checkpoint (uploaded for this window), results.
"""
from __future__ import annotations

import ast
import json
import os
import sys
import threading
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
    """S1's image, identical build steps to the 17 Oct task (so Modal's layer cache is reused): lmsysorg/sglang:v0.5.20-cu130 +
    /opt/fastpath (C1's PINNED35 stack)."""
    pins = pins if pins is not None else read_pinned35()
    return (
        modal.Image.from_registry(C.SGLANG_IMAGE)
        .run_commands(f"PIP_BREAK_SYSTEM_PACKAGES=1 python3 -m pip install --no-cache-dir {C.UV_PIN}",
                      "uv venv --python 3.12.10 /opt/fastpath",
                      f"uv pip install --no-cache --python {C.FASTPATH_PY} {' '.join(pins)}")
        .env({"HF_HOME": "/tmp/hf", "HF_HUB_ENABLE_HF_TRANSFER": "0", "TOKENIZERS_PARALLELISM": "false",
              "HF_HUB_OFFLINE": "1", "PYTHONDONTWRITEBYTECODE": "1"})
    )


def with_code(img):
    ignore = ["**/__pycache__/**", "**/*.pyc"]
    for n in LEAN_FILES:
        img = img.add_local_file(LEAN / n, f"{REMOTE_LEAN}/{n}")
    img = (img.add_local_dir(LEAN / "hosting" / "fastcore", f"{REMOTE_HOSTING}/fastcore", ignore=ignore)
           .add_local_file(LEAN / "hosting" / "sglang_host.py", f"{REMOTE_HOSTING}/sglang_host.py")
           .add_local_dir(HERE / "oc1", REMOTE_OC1, ignore=ignore)
           .add_local_dir(HERE / "r2pypatch", "/root/r2pypatch", ignore=ignore)
           .add_local_dir(HERE / "extra", "/root/extra", ignore=ignore)
           .add_local_dir(C.OLD_DATA, REMOTE_WORK, ignore=ignore + ["voice_prompts.json", "S.jsonl"]))
    return img


app = modal.App(C.APP_NAME)
if modal.is_local():
    sgl_image = with_code(build_sgl_image())
else:  # in the container the already-built image runs; this placeholder only satisfies the decorator
    sgl_image = modal.Image.debian_slim()
out_vol = modal.Volume.from_name(C.NEW_VOLUME)       # exists since 17 Oct (merged checkpoint); never created here

SESSION_REGION = os.environ.get("OC1_REGION", "any")
SESSION_TIMEOUT_S = int(os.environ.get("OC1_SESSION_TIMEOUT_S", 3800))
GPU_CPU, GPU_MEM_GIB = 4.0, 32.0
FN_RATE_GPU = C.container_rate_usd_h("H100", GPU_CPU, GPU_MEM_GIB, SESSION_REGION)
_REGION_KW = {} if SESSION_REGION == "any" else {"region": SESSION_REGION}


def _trim(ev: dict, limit: int = 60000) -> dict:
    """Queue-sized copy of an event: bulky result blobs stay on the Volume."""
    def cut(o):
        if isinstance(o, dict):
            return {k: ("<%d records on the Volume>" % len(v) if k in ("records", "answers", "items", "server_tail") and isinstance(v, list) and len(v) > 20
                        else cut(v)) for k, v in o.items()}
        if isinstance(o, list):
            return [cut(x) for x in o[:60]]
        return o
    out = cut(ev)
    if len(json.dumps(out, default=str)) > limit:
        return {"event": ev.get("event"), "config": ev.get("config"), "truncated": True}
    return out


def verify_tree(root: Path, manifest: dict) -> list:
    bad = []
    for rel, meta in sorted(manifest["files"].items()):
        p = root / rel
        if not p.exists():
            bad.append(f"{rel}: missing")
        elif p.stat().st_size != meta["bytes"]:
            bad.append(f"{rel}: {p.stat().st_size} bytes, expected {meta['bytes']}")
        elif C.sha256_file(p) != meta["sha256"]:
            bad.append(f"{rel}: sha256 differs")
    return bad


@app.function(image=sgl_image, gpu="H100!", cpu=GPU_CPU, memory=int(GPU_MEM_GIB * 1024), volumes={"/out": out_vol},
              timeout=SESSION_TIMEOUT_S, max_containers=1, retries=0, **_REGION_KW)
def gpu_session(plan: dict, q, prior_usd: float, run_id: str) -> dict:
    """One H100 container; the arms of oc1.r2 in priority order, each gated by the running spend."""
    sys.path.insert(0, "/root")
    from oc1 import r2 as R2
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
    mdir = Path("/out/models") / C.MERGED_NAME
    man = json.loads((mdir / "merge_manifest.json").read_text())
    if man.get("adapter_sha256") != C.C1_ADAPTER_SHA256:
        emit({"event": "abort", "why": "merged checkpoint is not C1"})
        return {"error": "merged checkpoint is not C1"}
    ver = {"merged": {}, "fp8": {}}

    def verify_merged():
        ver["merged"]["problems"] = verify_tree(mdir, man)
        emit({"event": "checkpoint_verified", "which": "merged", "n_files": len(man["files"]), "problems": ver["merged"]["problems"]})

    fdir = Path("/out/models") / R2.FP8_NAME

    def verify_fp8():
        try:
            fm = json.loads((fdir / "fp8_manifest.json").read_text())
            for sh, want in R2.FP8_SHARD_SHA256.items():           # the shas recorded on the CPU VMs when it was built
                if fm["files"].get(sh, {}).get("sha256") != want:
                    raise RuntimeError(f"manifest sha of {sh} is not the built one")
            ver["fp8"]["problems"] = verify_tree(fdir, fm)
        except Exception as e:  # noqa: BLE001
            ver["fp8"]["problems"] = [f"{type(e).__name__}: {str(e)[:200]}"]
        emit({"event": "checkpoint_verified", "which": "fp8_block", "problems": ver["fp8"]["problems"]})

    th_m = threading.Thread(target=verify_merged, daemon=True)
    th_f = threading.Thread(target=verify_fp8, daemon=True)
    th_m.start()
    th_f.start()

    def fp8_wait():
        th_f.join(timeout=400)
        return {"ok": th_f.is_alive() is False and not ver["fp8"].get("problems", ["not finished"]), "problems": ver["fp8"].get("problems")}

    def extra_cb(kind, cfg, srv, out_dir):
        if kind != "vision":
            return {"skipped": f"unknown extra {kind}"}
        pack = Path("/root/work/vision_pack")
        if not (pack / "items.jsonl").exists():
            return {"skipped": "no vision pack in the image"}
        spec = {"sgl_url": srv.url, "pack_dir": str(pack), "arms": cfg.vision}
        return S.run_runner("r2vision", spec, str(out_dir / "vision_r2.json"), timeout_s=900, python=sys.executable)

    stop_commit = threading.Event()

    def committer():           # partial results survive a hard cancel: the Volume is committed every 40 s
        while not stop_commit.wait(40.0):
            try:
                out_vol.commit()
            except Exception:  # noqa: BLE001
                pass
    threading.Thread(target=committer, daemon=True).start()

    sess = R2.R2Session(plan, emit, models_root="/out/models", work_dir="/root/work", results_root=str(run_dir),
                        rate_usd_h=plan["rate_usd_h"], prior_usd=prior_usd, python=sys.executable, extra_cb=extra_cb,
                        commit=out_vol.commit, fp8_wait=fp8_wait,
                        host_info={"gpu": gpu, "region": os.environ.get("MODAL_REGION"), "run_id": run_id})
    try:
        res = sess.run()
    finally:
        stop_commit.set()
        out_vol.commit()
    th_m.join(timeout=300)
    res["checkpoint_verified"] = ver
    res["gpu"] = gpu
    res["region"] = os.environ.get("MODAL_REGION")
    res["wall_s"] = round(time.time() - t0, 1)
    emit({"event": "session_done", "wall_s": res["wall_s"], "spent_usd": res["spent_usd"]})
    C.write_json(run_dir / "session_result.json", res)
    out_vol.commit()
    return {"wall_s": res["wall_s"], "spent_usd": res["spent_usd"], "notes": res.get("notes"),
            "blocks": {k: {kk: v.get(kk) for kk in ("boot_s", "error", "skipped", "spent_usd")} for k, v in res["results"].items()}}


# ------------------------------------------------------------------ local side
def make_plan(configs: str = "") -> dict:
    from oc1 import r2 as R2
    names = [c for c in configs.split(",") if c] or list(R2.DEFAULT_ORDER)
    return {"version": 2, "region": SESSION_REGION, "gpu": "H100!", "rate_usd_h": round(FN_RATE_GPU, 4), "configs": names,
            "boot_timeout_s": 600, "measure_timeout_s": 1500,
            "params": {"parity_conc": R2.PARITY_CONC, "lat_n": 320, "lat_warm": 20, "canary_n": 300}}


def render_plan(plan: dict, bud: C.Budget) -> str:
    from oc1 import r2 as R2
    lines = [f"H100 window at USD {plan['rate_usd_h']:.4f}/h (region {plan['region']}); ledger {json.dumps(bud.summary())}"]
    tot = C.CONTAINER_OVERHEAD_S
    for n in plan["configs"]:
        c = R2.R2_CONFIGS[n]
        tot += c.est_s
        lines.append(f"  {n:12s} arm {c.arm}  est {c.est_s:4d} s = USD {c.est_s / 3600 * plan['rate_usd_h']:.2f}  {c.desc[:90]}")
    lines.append(f"  total estimate {tot} s = USD {tot / 3600 * plan['rate_usd_h']:.2f}  (stop-launch {C.STOP_LAUNCH_USD}, hard cancel {C.HARD_STOP_USD}, cap {C.CAP_USD})")
    return "\n".join(lines)


@app.local_entrypoint()
def plan(configs: str = ""):
    """Print the plan and its estimate. Starts nothing, costs nothing."""
    C.payer_guard()
    bud = C.Budget()
    print(render_plan(make_plan(configs), bud), flush=True)


@app.local_entrypoint()
def session(configs: str = "", plan_only: bool = False):
    """THE H100 window (one container, arms in priority order)."""
    import queue as _queue
    import subprocess
    prof = C.payer_guard()
    bud = C.Budget()
    pl = make_plan(configs)
    print(render_plan(pl, bud), flush=True)
    if plan_only:
        return
    from oc1 import r2 as R2
    bud.check_launch("gpu_session", R2.R2_CONFIGS[pl["configs"][0]].est_s / 3600 * FN_RATE_GPU)
    run_id = time.strftime("session_%Y%m%d_%H%M%S", time.gmtime())
    out_dir = C.RESULTS / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    C.write_json(out_dir / "plan.json", pl)
    name = f"gpu_session-{run_id}"
    opened = False          # the ledger segment opens when the container is UP (image build / GPU queue time is not billed)
    result, call = None, None
    events = open(out_dir / "events_local.jsonl", "a")
    t0 = time.time()
    try:
        with modal.Queue.ephemeral() as q:
            call = gpu_session.spawn(pl, q, bud.spent_closed() + 0.05, run_id)       # + volume-storage reserve
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
                        cold["spawn_to_container_up_s"] = round(time.time() - t_spawn, 1)
                        C.write_json(out_dir / "cold_start.json", cold)
                        if not opened:
                            bud.open(name, FN_RATE_GPU)
                            opened = True
                    if kind in ("container_up", "block_start", "booted", "block_end", "block_skipped", "abort", "hard_stop",
                                "checkpoint_verified", "session_done"):
                        brief = {k: ev.get(k) for k in ("config", "spent_usd", "boot_s", "error", "skipped", "gpu", "region", "problems", "why",
                                                        "which", "prefill_graph_backend_resolved") if ev.get(k) is not None}
                        print(f"[{ev.get('t', 0):7.1f}s] {kind} {json.dumps(brief, default=str)[:400]}", flush=True)
                if bud.must_cancel():
                    print(f"HARD STOP at ${bud.spent():.2f}: cancelling the H100 call", flush=True)
                    call.cancel()
                    break
                try:
                    result = call.get(timeout=0)
                    break
                except (modal.exception.TimeoutError, TimeoutError):
                    pass
                if time.time() - t0 > SESSION_TIMEOUT_S + 1500 + 180 or (not opened and time.time() - t_spawn > 1500):
                    print("no container_up within 25 min / deadline passed: cancelling", flush=True)
                    call.cancel()
                    break
    except KeyboardInterrupt:
        print("interrupted: the H100 call is cancelled", flush=True)
        try:
            call.cancel()
        except Exception:  # noqa: BLE001
            pass
    finally:
        wall = (result or {}).get("wall_s") if isinstance(result, dict) else None
        if opened:
            bud.close(name, wall)
        else:        # never saw the container come up: charge a conservative 90 s so that the ledger cannot under-count
            bud.add_extra("gpu_session: no container_up event seen (conservative 90 s of H100)", C.container_cost_usd(90, FN_RATE_GPU))
        C.write_json(out_dir / "session_return.json", {"result": result, "budget": bud.summary()})
        subprocess.run([str(Path(sys.executable).parent / "modal"), "volume", "get", "--force", C.NEW_VOLUME, f"results/{run_id}",
                        str(out_dir / "volume")], env={**os.environ, "MODAL_PROFILE": C.PROFILE}, capture_output=True, timeout=600)
        print(f"session done; budget {json.dumps(bud.summary())}; results in {out_dir}", flush=True)
