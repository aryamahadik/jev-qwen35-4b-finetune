"""modal_app_grid: the A42-D 9 grid reads on ONE Modal H100 (18 candidates + the C1 reference, one container, one job) and the
merged-vs-HF-adapter parity check of the chosen candidate. BUILT AND CPU-TESTED ONLY: nothing in this file has started a Modal call.

  MODAL_PROFILE=<owner-named> ../.venv/bin/modal run c2_build/train/grid_h100/modal_app_grid.py::plan      # estimate only, no GPU
  MODAL_PROFILE=<owner-named> ../.venv/bin/modal run c2_build/train/grid_h100/modal_app_grid.py::grid      # THE grid session
  MODAL_PROFILE=<owner-named> ../.venv/bin/modal run c2_build/train/grid_h100/modal_app_grid.py::parity --cand last3_a08

Only after the owner's GO #1: the payer is whatever profile OWNER_GO1_PAYER.json names (common.payer_guard; no file = refuse; MODAL_PROFILE
must equal it; no MODAL_TOKEN_* override; only `modal run`; never --detach). Money: common.Budget, ONE ledger (ledger.json) for every call,
cap USD 15.00 (A88), stop-launch 13.50, the laptop cancels the GPU call at 14.60, the function timeout alone cannot cross 15.00. A launch whose
plan does not fit the remaining stop-launch budget is REFUSED unless --allow-partial (then the models that fit are read; a later call with
the same --run-id resumes, still under the same cap).

Container: lmsysorg/sglang:v0.5.20-cu130 (the S1 image) + /opt/fastpath (C1's PINNED35 stack, the read client and the HF reference), code
and the dev data mounted from the laptop, the payer's Volume `opendecide` mounted READ-ONLY at /vol (C2 run folder, C1 adapter, HF cache),
results on the Volume `c2-grid-h100-reads` at /out/runs/<run id>/ (committed after every model). max_containers=1, retries=0, GPU "H100!".
"""
from __future__ import annotations

import ast
import json
import os
import queue as _queue
import subprocess
import sys
import threading
import time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
TRAIN = HERE.parent
sys.path.insert(0, str(TRAIN))

import modal  # noqa: E402

from grid_h100 import common as C  # noqa: E402


def _modal_cli() -> str | None:
    a0 = Path(sys.argv[0]) if sys.argv else Path("")
    if a0.name == "modal" or (a0.name == "__main__.py" and a0.parent.name == "modal"):
        return next((a for a in sys.argv[1:] if not a.startswith("-")), "")
    return None


if modal.is_local() and _modal_cli() is not None:
    C.payer_guard()                    # before an image is built or an app is created on a payer the owner did not name

LEAN = C.LEAN
REMOTE = {"pkg": "/root/grid_h100", "c2grid": "/root/c2grid", "serving": "/root/serving", "lean": "/root/lean", "data": "/root/data",
          "workloads": "/root/workloads", "c1tok": "/root/c1tok"}
LEAN_FILES = ("decoder_io.py", "prism_x.py", "writeblock.py")
SERVING_FILES = ("p7_common.py", "s1_pin.py", "merge_parity.py", "d9_latency.py", "prompt_sha_check.py", "S1_CONFIG_PIN.json")
PARITY_FILE = "gblock_a42d_c1read.jsonl"
PKG_IGNORE = ["**/__pycache__/**", "**/*.pyc", "tests/**", "results/**", "ledger.json", "ledger.tmp", "OWNER_GO1_PAYER.json", "*.md"]


def read_pinned35() -> list:
    """C1's PINNED35 pip list, parsed as text from hosting/modal_direct_host.py (never imported: it builds a Modal app)."""
    src = (LEAN / "hosting" / "modal_direct_host.py").read_text()
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "PINNED35" for t in node.targets):
            return node.value.func.value.value.split()
    raise SystemExit("PINNED35 not found in hosting/modal_direct_host.py")


OWN_DEV = [x for x in os.environ.get("GRID_OWN_DEV", "").split(",") if x]       # own dev splits mounted into the image (read with --tta-choice)


def data_files(own=None) -> list:
    from grid_h100 import plan as PL
    rel = {s["file"] for s in PL.set_specs(OWN_DEV if own is None else own)} | set(PL.EXTRA_FILES) | {PARITY_FILE}
    return sorted(rel)


def build_image():
    """S1's image (the build steps of hosting/sglang_host.py / the 17 Oct task, so Modal's layer cache is reused) + the mounted code."""
    pins = read_pinned35()
    img = (
        modal.Image.from_registry(C.SGLANG_IMAGE)
        .run_commands(f"PIP_BREAK_SYSTEM_PACKAGES=1 python3 -m pip install --no-cache-dir {C.UV_PIN}",
                      "uv venv --python 3.12.10 /opt/fastpath",
                      f"uv pip install --no-cache --python {C.FASTPATH_PY} {' '.join(pins)}")
        .env({"HF_HOME": "/tmp/hf", "HF_HUB_ENABLE_HF_TRANSFER": "0", "TOKENIZERS_PARALLELISM": "false", "HF_HUB_OFFLINE": "1",
              "PYTHONDONTWRITEBYTECODE": "1", "OD_LEAN": REMOTE["lean"], "P7_SERVING_DIR": REMOTE["serving"],
              "P7_WORKLOAD_DIR": REMOTE["workloads"], "C2GRID_DIR": REMOTE["c2grid"]})
    )
    ign = ["**/__pycache__/**", "**/*.pyc"]
    for n in LEAN_FILES:
        img = img.add_local_file(LEAN / n, f"{REMOTE['lean']}/{n}")
    img = (img.add_local_dir(LEAN / "hosting" / "fastcore", f"{REMOTE['lean']}/hosting/fastcore", ignore=ign)
           .add_local_file(LEAN / "hosting" / "sglang_host.py", f"{REMOTE['lean']}/hosting/sglang_host.py"))
    for n in ("merge_avg.py", "grid_plan.py"):
        img = img.add_local_file(TRAIN / n, f"{REMOTE['c2grid']}/{n}")
    for n in SERVING_FILES:
        img = img.add_local_file(LEAN / "c2_build" / "serving" / n, f"{REMOTE['serving']}/{n}")
    for rel in data_files():
        img = img.add_local_file(LEAN / "data" / rel, f"{REMOTE['data']}/{rel}")
    for n in ("S.jsonl", "manifest.json"):
        img = img.add_local_file(LEAN / "speed" / "workloads" / n, f"{REMOTE['workloads']}/{n}")
    c1 = LEAN.parents[1] / "backups" / "modal_models" / C.C1_NAME
    for n in C.C1_PIN_TOKENIZER:
        img = img.add_local_file(c1 / n, f"{REMOTE['c1tok']}/{n}")
    return img.add_local_dir(HERE, REMOTE["pkg"], ignore=PKG_IGNORE)       # last: code edits rebuild only this layer


app = modal.App(C.APP_NAME)
if modal.is_local():
    image = build_image()
else:                                   # in the container the already-built image runs; this placeholder only satisfies the decorator
    image = modal.Image.debian_slim()
src_vol = modal.Volume.from_name(C.SRC_VOLUME).read_only()          # the payer's account Volume; never written
out_vol = modal.Volume.from_name(C.OUT_VOLUME, create_if_missing=True)
_REGION_KW = {} if C.REGION == "any" else {"region": C.REGION}
FN_KW = dict(image=image, gpu="H100!", cpu=C.FN_CPU, memory=int(C.FN_MEM_GIB * 1024), volumes={"/vol": src_vol, "/out": out_vol},
             timeout=C.SESSION_TIMEOUT_S, max_containers=1, retries=0, **_REGION_KW)


def _trim(ev: dict, limit: int = 60000) -> dict:
    def cut(o):
        if isinstance(o, dict):
            return {k: ("<%d items on the Volume>" % len(v) if k in ("calls_ms", "records", "server_tail", "tail") and isinstance(v, list) and len(v) > 20
                        else cut(v)) for k, v in o.items()}
        if isinstance(o, list):
            return [cut(x) for x in o[:60]]
        return o
    out = cut(ev)
    return out if len(json.dumps(out, default=str)) <= limit else {"event": ev.get("event"), "truncated": True}


def _emitter(run_dir: Path, q, t0: float):
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
    return emit


def _committer(stop: threading.Event):
    def run():
        while not stop.wait(40.0):          # partial results survive a hard cancel
            try:
                out_vol.commit()
            except Exception:  # noqa: BLE001
                pass
    threading.Thread(target=run, daemon=True).start()


@app.function(**FN_KW)
def grid_session(plan: dict, q, prior_usd: float) -> dict:
    """THE grid job: 19 models, one H100, one container."""
    sys.path.insert(0, "/root")
    from grid_h100.session import GridSession
    t0 = time.time()
    emit = _emitter(Path("/out/runs") / plan["run_id"], q, t0)
    stop = threading.Event()
    _committer(stop)
    sess = GridSession(plan, emit=emit, prior_usd=prior_usd, commit=out_vol.commit, log=lambda s: print(s, flush=True))
    try:
        res = sess.run()
    finally:
        stop.set()
        out_vol.commit()
    return {k: res[k] for k in ("run_id", "wall_s", "spent_usd", "models_done", "models_total", "complete", "errors")}


@app.function(**FN_KW)
def parity_session(pplan: dict, q, prior_usd: float) -> dict:
    """The parity job of the chosen candidate (its own container; the same ledger)."""
    sys.path.insert(0, "/root")
    from grid_h100.parity import ParitySession
    t0 = time.time()
    emit = _emitter(Path("/out/runs") / pplan["run_id"] / "parity", q, t0)
    stop = threading.Event()
    _committer(stop)
    try:
        rec = ParitySession(pplan, emit=emit, prior_usd=prior_usd, commit=out_vol.commit, log=lambda s: print(s, flush=True)).run()
    finally:
        stop.set()
        out_vol.commit()
    return {"run_id": pplan["run_id"], "cand": pplan["cand"], "bar": rec["bar"], "all": rec["all"], "spent_usd": rec["spent_usd"]}


# ------------------------------------------------------------------ the laptop side
def _drive(fn, args: tuple, name: str, bud: C.Budget, est_usd: float, deadline_s: float, pull: tuple | None):
    """Spawn one GPU call, follow its events, keep the ledger, cancel at the hard stop. Never --detach: Ctrl-C cancels the call."""
    bud.check_launch(name, est_usd)
    result, call, opened = None, None, False
    out_dir = C.RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    events = open(out_dir / "events_local.jsonl", "a")
    t0 = time.time()
    try:
        with modal.Queue.ephemeral() as q:
            call = fn.spawn(args[0], q, bud.spent_closed() + 0.05)           # + Volume-storage reserve
            t_spawn = time.time()
            while True:
                try:
                    ev = q.get(timeout=5)
                except Exception:  # noqa: BLE001
                    ev = None
                if ev:
                    events.write(json.dumps(ev, default=str) + "\n")
                    events.flush()
                    kind = ev.get("event")
                    if kind == "container_up" and not opened:
                        bud.open(name, C.FN_RATE_USD_H)
                        opened = True
                    if kind in ("container_up", "base_ready", "grid_ready", "reader_ready", "block_start", "block_end", "block_skipped",
                                "candidate_built", "hf_ref_done", "parity_done", "session_done"):
                        brief = {k: ev.get(k) for k in ("read_name", "spent_usd", "error", "gpu", "why", "grid_sha256", "latency_p50_ms",
                                                        "complete", "done", "PASS", "argmax") if ev.get(k) is not None}
                        print(f"[{ev.get('t', 0):7.1f}s] {kind} {json.dumps(brief, default=str)[:300]}", flush=True)
                if bud.must_cancel():
                    print(f"HARD STOP at ${bud.spent():.2f}: cancelling the H100 call", flush=True)
                    call.cancel()
                    break
                try:
                    result = call.get(timeout=0)
                    break
                except (modal.exception.TimeoutError, TimeoutError):
                    pass
                if time.time() - t0 > deadline_s + 1500 + 180 or (not opened and time.time() - t_spawn > 1500):
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
        else:
            bud.add_extra(f"{name}: no container_up event seen (conservative 90 s of H100)", C.container_cost_usd(90))
        C.write_json(out_dir / "return.json", {"result": result, "budget": bud.summary()})
        if pull:
            subprocess.run([str(Path(sys.executable).parent / "modal"), "volume", "get", "--force", C.OUT_VOLUME, f"runs/{pull[0]}",
                            str(C.RESULTS / pull[0])], env={**os.environ}, capture_output=True, timeout=900)
        print(f"done; ledger {json.dumps(bud.summary())}; results {C.RESULTS / (pull[0] if pull else name)}", flush=True)
    return result


@app.local_entrypoint()
def plan(own_dev: str = ""):
    """Estimate only (no GPU, no function call)."""
    from grid_h100 import driver
    C.payer_guard()
    p = driver.make_plan(own_dev=[s for s in own_dev.split(",") if s])
    print(json.dumps(p["estimate"]["verdict"], indent=1))


@app.local_entrypoint()
def grid(run_id: str = "", own_dev: str = "", allow_partial: bool = False, grid_source: str = "rebuild"):
    """THE grid session. Refuses when the plan does not fit the remaining stop-launch budget unless --allow-partial."""
    from grid_h100 import driver
    prof = C.payer_guard()
    go = C.read_go(C.GO_FILE)
    if sorted(x for x in own_dev.split(",") if x) != sorted(OWN_DEV):
        raise SystemExit(f"--own-dev {own_dev!r} differs from GRID_OWN_DEV {OWN_DEV} that the image was built with (export GRID_OWN_DEV=a,b before modal run)")
    bud = C.Budget(cap=C.go_cap(go), stop_launch=min(C.STOP_LAUNCH_USD, C.go_cap(go) - 0.4), hard_stop=min(C.HARD_STOP_USD, C.go_cap(go) - 0.1))
    pl = driver.make_plan(run_id or None, [s for s in own_dev.split(",") if s], bud.spent_closed(), grid_source=grid_source)
    pre = driver.preflight(pl)
    blockers = [b for b in pre["blockers"] if not b.startswith("COST:")]
    if blockers:
        raise SystemExit("preflight blockers:\n  " + "\n  ".join(blockers))
    v = pl["estimate"]["verdict"]
    print(f"payer {prof}; run {pl['run_id']}; {v['text']}; ledger {json.dumps(bud.summary())}", flush=True)
    if not v["fits"] and not allow_partial:
        raise SystemExit("REFUSED: the plan does not fit the cap (see above); the owner decides at GO #1 (--allow-partial runs only the models that fit)")
    first = pl["estimate"]["scenarios"]["likely"]
    est = C.container_cost_usd(first["fixed_s"] + 2 * first["per_model"]["total_s"])      # at least the reference and the final step
    return _drive(grid_session, (pl,), f"grid-{pl['run_id']}", bud, est, C.SESSION_TIMEOUT_S, (pl["run_id"],))


@app.local_entrypoint()
def parity(cand: str, run_id: str = "", candidate_json: str = ""):
    """The merged-vs-HF-adapter parity check of the chosen candidate (CANDIDATE_C2.json must name it)."""
    from grid_h100 import driver
    prof = C.payer_guard()
    go = C.read_go(C.GO_FILE)
    bud = C.Budget(cap=C.go_cap(go), stop_launch=min(C.STOP_LAUNCH_USD, C.go_cap(go) - 0.4), hard_stop=min(C.HARD_STOP_USD, C.go_cap(go) - 0.1))
    pp = driver.make_parity_plan(cand, Path(candidate_json) if candidate_json else driver.CANDIDATE, run_id or None)
    est = C.container_cost_usd(driver.PL.PARITY_ASSUME["fixed_s"][1])
    print(f"payer {prof}; parity {pp['run_id']} for {cand}; estimate ${est:.2f}; ledger {json.dumps(bud.summary())}", flush=True)
    return _drive(parity_session, (pp,), f"parity-{pp['run_id']}", bud, est, C.SESSION_TIMEOUT_S, (pp["run_id"],))
