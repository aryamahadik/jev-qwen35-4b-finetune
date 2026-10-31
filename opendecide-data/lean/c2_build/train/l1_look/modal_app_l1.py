"""modal_app_l1: C2's ONE pre-registered OHS-4 look (L1) on ONE Modal H100: C1 + the chosen C2 candidate in one container, on the same S1 path
the 19 grid reads used (PREREG A38 / A89; C2_DATA_SPEC 7.3, 8.5). BUILT AND CPU-TESTED ONLY: nothing in this file has started a Modal call.

  cd lean && MODAL_PROFILE=mahadikarya3 ../.venv/bin/modal run c2_build/train/l1_look/modal_app_l1.py::l1 --run-id l1_<id> [--finish]

Sealed-side program: it reads the sealed request file by program, passes the rows to the container as a function argument (never to a Volume, never
to an image layer; round 1's modal_preread.py did the same), and prints only counts, seconds and sha256s. The orchestrator never sees an item.

Guards before any GPU is asked for (l1common.prepare_plan, then grid_h100.common): the A38 hash pins; one look only (no L1_RESULT.json, no granted L1 in
the scorer's log, no raw reads yet); the owner's GO #2 record; CANDIDATE_C2.json (it names a candidate of GRID_RECORD.json with the same adapter sha256);
the pre-gate result (PASS -> C1 + C2; FAIL -> C1 alone); the payer guard (the owner-named profile only, never aryamhd, C2 training over); the ledger
(the grid's one USD 15.00 ledger: stop-launch 13.50, the laptop cancels at 14.60, the function timeout alone cannot cross the cap).
Region: unpinned ('any'), as the grid ran; this is the only mode (the environment is never read for it). SPEED-3's US pin (spec 9.2 / 8.5) is a separate measurement that was not run.
max_containers=1, retries=0, GPU 'H100!', never --detach. The payer's Volume is mounted READ-ONLY; nothing is written to Modal storage.
"""
from __future__ import annotations

import ast
import json
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
TRAIN = HERE.parent
sys.path.insert(0, str(TRAIN))

import modal  # noqa: E402

from grid_h100 import common as C  # noqa: E402
from l1_look import l1common as L  # noqa: E402


def _modal_cli() -> str | None:
    a0 = Path(sys.argv[0]) if sys.argv else Path("")
    if a0.name == "modal" or (a0.name == "__main__.py" and a0.parent.name == "modal"):
        return next((a for a in sys.argv[1:] if not a.startswith("-")), "")
    return None


if modal.is_local() and _modal_cli() is not None:
    C.payer_guard()                    # before an image is built or an app is created on a payer the owner did not name

LEAN = C.LEAN
REMOTE = {"grid_pkg": "/root/grid_h100", "l1_pkg": "/root/l1_look", "c2grid": "/root/c2grid", "serving": "/root/serving", "lean": "/root/lean",
          "data": "/root/data", "c1tok": "/root/c1tok"}
LEAN_FILES = ("decoder_io.py", "prism_x.py", "writeblock.py")
SERVING_FILES = ("p7_common.py", "s1_pin.py", "merge_parity.py", "d9_latency.py", "prompt_sha_check.py", "S1_CONFIG_PIN.json")
PKG_IGNORE = ["**/__pycache__/**", "**/*.pyc", "tests/**", "results/**", "ledger.json", "ledger.tmp", "OWNER_GO1_PAYER.json", "*.md", "l1_out/**"]


def read_pinned35() -> list:
    """C1's PINNED35 pip list, parsed as text from hosting/modal_direct_host.py (never imported: it builds a Modal app)."""
    src = (LEAN / "hosting" / "modal_direct_host.py").read_text()
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "PINNED35" for t in node.targets):
            return node.value.func.value.value.split()
    raise SystemExit("PINNED35 not found in hosting/modal_direct_host.py")


def build_image():
    """The grid's image (same build steps, so Modal's layer cache is reused) + the mounted code. Dev data in the image: the C2 mixdev only."""
    pins = read_pinned35()
    img = (
        modal.Image.from_registry(C.SGLANG_IMAGE)
        .run_commands(f"PIP_BREAK_SYSTEM_PACKAGES=1 python3 -m pip install --no-cache-dir {C.UV_PIN}",
                      "uv venv --python 3.12.10 /opt/fastpath",
                      f"uv pip install --no-cache --python {C.FASTPATH_PY} {' '.join(pins)}")
        .env({"HF_HOME": "/tmp/hf", "HF_HUB_ENABLE_HF_TRANSFER": "0", "TOKENIZERS_PARALLELISM": "false", "HF_HUB_OFFLINE": "1",
              "PYTHONDONTWRITEBYTECODE": "1", "OD_LEAN": REMOTE["lean"], "P7_SERVING_DIR": REMOTE["serving"],
              "P7_WORKLOAD_DIR": "/root/workloads", "C2GRID_DIR": REMOTE["c2grid"]})
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
    img = img.add_local_file(LEAN / "data" / L.MIXDEV_FILE, f"{REMOTE['data']}/{L.MIXDEV_FILE}")
    c1 = LEAN.parents[1] / "backups" / "modal_models" / C.C1_NAME
    for n in C.C1_PIN_TOKENIZER:
        img = img.add_local_file(c1 / n, f"{REMOTE['c1tok']}/{n}")
    img = img.add_local_dir(TRAIN / "grid_h100", REMOTE["grid_pkg"], ignore=PKG_IGNORE)
    return img.add_local_dir(HERE, REMOTE["l1_pkg"], ignore=PKG_IGNORE)           # last: code edits rebuild only this layer


app = modal.App(L.APP_NAME)
if modal.is_local():
    image = build_image()
else:                                   # in the container the already-built image runs; this placeholder only satisfies the decorator
    image = modal.Image.debian_slim()
src_vol = modal.Volume.from_name(C.SRC_VOLUME).read_only()          # the payer's account Volume (C2 run folder, C1 adapter, HF cache); never written
FN_KW = dict(image=image, gpu="H100!", cpu=C.FN_CPU, memory=int(C.FN_MEM_GIB * 1024), volumes={"/vol": src_vol}, timeout=L.L1_TIMEOUT_S,
             max_containers=1, retries=0)


def _emitter(q, t0: float):
    def emit(ev):
        ev = {"t": round(time.time() - t0, 1), **ev}
        try:
            q.put(ev)
        except Exception:  # noqa: BLE001
            pass
    return emit


@app.function(**FN_KW)
def l1_session(plan: dict, final_rows: list, q, prior_usd: float) -> dict:
    """THE look's job: C1 (+ C2) on one H100, one container."""
    sys.path.insert(0, "/root")
    from l1_look.l1session import L1Session
    t0 = time.time()
    sess = L1Session(plan, final_rows, emit=_emitter(q, t0), prior_usd=prior_usd, log=lambda s: print(s, flush=True))
    return sess.run()


# ------------------------------------------------------------------ the laptop side
BRIEF = ("read_name", "spent_usd", "error", "gpu", "ok", "sets", "rows", "tokens", "init_s", "name", "rank")


def _drive(plan: dict, final_rows: list, bud: C.Budget, est_usd: float):
    """Spawn the one GPU call, follow its events, keep the ledger, cancel at the hard stop. Never --detach: Ctrl-C cancels the call."""
    bud.check_launch("l1", est_usd)
    name = f"l1-{plan['run_id']}"
    result, call, opened = None, None, False
    t0 = time.time()
    try:
        with modal.Queue.ephemeral() as q:
            call = l1_session.spawn(plan, final_rows, q, bud.spent_closed() + 0.05)
            t_spawn = time.time()
            while True:
                try:
                    ev = q.get(timeout=5)
                except Exception:  # noqa: BLE001
                    ev = None
                if ev:
                    kind = ev.get("event")
                    if kind == "container_up" and not opened:
                        bud.open(name, C.FN_RATE_USD_H)
                        opened = True
                    brief = {k: ev.get(k) for k in BRIEF if ev.get(k) is not None}
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
                if time.time() - t0 > L.L1_TIMEOUT_S + 1500 + 180 or (not opened and time.time() - t_spawn > 1500):
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
        print(f"done; ledger {json.dumps(bud.summary())}", flush=True)
    return result


@app.local_entrypoint()
def l1(run_id: str = "", finish: bool = False):
    """THE GPU job of the look. Refuses unless every ordering guard holds. `--finish` also runs the CPU finish (freeze T, answers, the look, result)."""
    prof = C.payer_guard()
    go = C.read_go(C.GO_FILE)
    p = L.L1Paths()
    rid = run_id or time.strftime("l1_%m%d_%H%M", time.gmtime())
    try:
        plan, rows = L.prepare_plan(p, rid)
    except L.Refused as e:
        raise SystemExit(str(e))
    bud = C.Budget(cap=C.go_cap(go), stop_launch=min(C.STOP_LAUNCH_USD, C.go_cap(go) - 0.4), hard_stop=min(C.HARD_STOP_USD, C.go_cap(go) - 0.1))
    est = plan["estimate"]["scenarios"]["likely"]
    print(f"payer {prof}; run {rid}; mode {plan['mode']}; models {[m['read_name'] for m in plan['models']]}; "
          f"estimate likely ${est['cost_usd']} ({est['total_min']} min), high ${plan['estimate']['scenarios']['high']['cost_usd']}; "
          f"ledger {json.dumps(bud.summary())}", flush=True)
    if not plan["estimate"]["verdict"]["fits"]:
        raise SystemExit("REFUSED: the look's estimate does not fit the remaining stop-launch budget; the owner decides")
    est_first = C.container_cost_usd(est["total_s"] * 0.5)
    result = _drive(plan, rows, bud, est_first)
    if not isinstance(result, dict):
        raise SystemExit("the GPU job returned no result (cancelled or failed); nothing was written; the ledger above is the cost")
    plan_no_rows = {k: v for k, v in plan.items() if k not in ("grid_record", "prompt_check_record")}
    L.write_json(p.out_root / rid / "plan.json", plan_no_rows)
    rec = L.write_raw(p, plan, result)
    print(json.dumps({"run_id": rid, "ok": rec["ok"], "errors": rec["errors"], "wall_s": rec["wall_s"], "spent_usd": rec["spent_usd"],
                      "path_sha256": rec["path_sha256"], "files": list(rec["files"])}, default=str), flush=True)
    if not rec["ok"]:
        raise SystemExit("the GPU job did not complete every read (see errors); no raw reads were written; the look is NOT taken")
    if finish:
        from l1_look import l1_cli
        l1_cli.finish(p)
    else:
        print("next: cd lean && ../.venv/bin/python -B c2_build/train/l1_look/l1_cli.py finish", flush=True)
