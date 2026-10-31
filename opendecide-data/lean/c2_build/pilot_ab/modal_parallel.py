"""Parallel launcher for the six A42-D item 4 single-family pilots (T40-T45) on ONE Modal account, with a spend guard.

Owner-approved (HANDOFF, "Owner speed budget"): profile mahadikarya44 ONLY, all six pilots together <= 3.50 USD (hard cap).
Never mahadikarya2 / mahadikarya3 (C2 training) and never aryamhd. Built 16 Oct; no GPU container has been started by this file.
It does not change what a pilot is: the config, the staged rows, the trainer (train_decoder.train), the recipe, the seed, the
bars and `verdict.py` are the harness's (README.md in this folder). Only the launching differs: up to six pilots at once, one
H100 container each, plus a cost guard, a watchdog, and automatic result pulls.

What it trains / evaluates (from the harness): per family, ONE LoRA pass from C1 (adapter sha256 507d1c29...) on the family's 1,500
staged rows (94 steps; no replay; LR 5e-5, batch 16, r16/alpha 32, 5% warm-up + cosine, seed 20261013, sym_cons, perm_twin 0.3).
Result: /vol/models/q35_4b_pab_<FAM> on the volume, pulled to backups/modal_models/q35_4b_pab_<FAM> (the path `l4_reads.sh fetch`
uses). The READS (own dev 300, 9 gate dev splits = 7,056 rows, G-proxy) stay on the free od-l4 under `l4_reads.sh`, because
`verdict.py` needs C1 and the pilot read on one machine and C1's reads are on the L4; Modal reads would cost more than the cap.

GPU choice: "H100!" (exactly H100, never auto-upgraded to H200). It is the harness's pin and the GPU C1 itself trained on
(logs: NVIDIA H100 80GB HBM3), so the pilot-minus-C1 contrast is not confounded by another architecture (fla Triton kernels and
bf16 accumulation differ per GPU, and there is no re-pilot to absorb a difference). It is also the cheapest per pilot: A100-80GB
(2.50/h) and L40S (1.95/h) are 0.63 and 0.49 of the H100's 3.95/h, but bf16 training of this 4B model is roughly 2.2x (A100) and
3.5x (L40S) slower (estimates from peak throughput and memory bandwidth, not measured), which puts a pilot at about 0.63 and 0.73 USD
against 0.55 on the H100, and longer. Peak memory of the heavy smoke at micro_tokens 8192 was 28.6 GB, so a 40 GB card is not safe
either. The container check refuses to train on anything but an H100 80GB.

Commands (run from lean/c2_build; every one refuses a profile other than mahadikarya44):
  export MODAL_PROFILE=mahadikarya44 PILOT_PROFILE=mahadikarya44
  PY="../../.venv/bin/python -B"
  $PY pilot_ab/modal_parallel.py preflight           # laptop checks + ONE CPU-only container (image, volume, imports); ~0.01 USD
  $PY pilot_ab/modal_parallel.py prep-init           # once: server-side copy of C1 to models/q35_4b_main500k_init (free, idempotent)
  $PY pilot_ab/modal_parallel.py estimate            # per-pilot cost from the staged rows (or scenarios when none are staged)
  $PY pilot_ab/modal_parallel.py plan                # the guard's decision for the staged families; no spawn
  $PY pilot_ab/modal_parallel.py launch --go         # THE PAID STEP (needs the orchestrator's go): spawns what fits, exits
  $PY pilot_ab/modal_parallel.py watch               # polls every 10 s, enforces the hard stop, pulls results, stops the app
  $PY pilot_ab/modal_parallel.py status | pull | abort
  # cheap proof of the whole lifecycle with CPU stand-ins (a few cents; --root/--backups point at a scratch folder):
  $PY pilot_ab/modal_parallel.py --smoke --root <scratch> --backups <scratch>/bk launch --families T40,T41 --go
  $PY pilot_ab/modal_parallel.py --smoke --root <scratch> --backups <scratch>/bk watch ; ... cleanup-smoke
Family files come from the harness: `make_config.py --family T4x ...` writes pilot_ab/stage/T4x/ and configs/T4x.json (+ .stage.json).

Spend guard (CAP 3.50 USD, `RATE` 4.09 USD/h all-in per H100 container, the measured rate of extra/fix2_spawn.py):
  * launch: committed = actual cost of finished pilots + max(pessimistic estimate, elapsed cost) of running ones + other spend
    (preflight, smoke). A pilot is launched only if committed + its pessimistic estimate <= CAP; the rest are DEFERRED, not
    cancelled (re-run `launch --go` after `watch` finished: the actual costs of the first wave free budget). `--strict`
    refuses the whole launch unless all requested pilots fit. A family already in the ledger, already on the volume, or with a
    verdict file is refused (no re-pilot). Orphan running pilot apps not in the ledger are refused.
  * the account's remaining free credit (30 USD - credits used this month, `modal billing summary`) must cover the projection.
  * watch: elapsed container time (heartbeats in a modal.Dict, so queue time is not counted) is summed every 10 s; at
    CAP - 0.10 USD every unfinished call is cancelled with its containers terminated and the app is stopped (exit 3).
  * backstops that do not need the laptop: per-call timeout (20 min = 1.36 USD), scaledown window 2 s, max 6 containers, no
    retries. They bound a runaway container, not the sum: set the workspace spend limit in the Modal dashboard as well.
  * the app is stopped when the pilots are done (`watch`), on abort, and on a hard stop. The ledger is pilot_ab/par_runs/ledger.json.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zlib
from contextlib import contextmanager
from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.parent))     # lean/ (modal_od, train_decoder, decoder_io, ...)

# ------------------------------------------------------------------ constants (literals: the container imports this file too)
PROFILE = "mahadikarya44"
NEVER_PROFILES = ("mahadikarya2", "mahadikarya3", "aryamhd")
APP_NAME = "opendecide-c2-pilot-par"
VOLUME = "opendecide"
SECRET = "opendecide-keys"
HB_DICT = "opendecide-c2-pilot-par-hb"
GPU = "H100!"
CAP_USD = 3.50
HARD_STOP_MARGIN = 0.10
RATE_H = 4.09                  # all-in USD/h of one H100 container (list 3.95 + CPU and memory; extra/fix2_spawn.py RATE_PER_H)
LIST_H100_H = 3.95
BOOT_S = 25                    # billed container start before the function body (image cached, mounts)
SCALEDOWN_S = 2                # idle time a finished container stays billed (scaledown_window)
MAX_PARALLEL = 6
MS_PER_PADDED = 0.163          # A28: ms per padded token on the H100; recalibrated 16 Oct on the C round-1 run (predicted 110.5 min
                               # vs measured 106.92 min for 1,650 steps: ratio 0.968)
PADDED_PER_MEAN_TOKEN = 26.88  # padded tokens per step per mean real row token, measured on the same round-1 data (24,651 / 917)
STEPS_PER_PILOT = 94
FREE_CREDIT_USD = 30.0         # monthly free credit per account (logs/budget_ledger.md, HANDOFF)
CREDIT_MARGIN_USD = 0.25
# fixed seconds per pilot besides the 94 steps (central / pessimistic); sources in the comments
FIXED_S = {
    "container_start": (BOOT_S, 45),         # image cached after the first build, mounts, python start
    "imports": (20, 45),                     # torch, transformers, peft, fla: 17.0-17.3 s measured by `preflight` (CPU container)
    "adapter_and_data": (3, 8),              # C1 sha256 (130 MB), decompress and hash the two staged files
    "model_load": (45, 90),                  # logs/pilot/speed_h100_mt8192.json load_s 39.7; six containers read one volume
    "first_steps_autotune": (60, 120),       # round-1 log: step 0 at 41 s, steps 1-2 at +12 s and +16 s (cold Triton cache)
    "save_and_commit": (15, 30),             # speed json ckpt_s 7.0; final adapter save and vol.commit
    "scaledown": (SCALEDOWN_S, SCALEDOWN_S),
}
STEP_PESS_FACTOR = 1.15
QUEUE_GRACE_S = 180            # no heartbeat this long after the spawn: assume the container runs and count from the spawn
TIMEOUT_MIN = max(10, min(30, int(os.environ.get("PILOT_TIMEOUT_MIN", "20"))))
TIMEOUT_S = TIMEOUT_MIN * 60

C1_NAME = "q35_4b_main500k"
C1_INIT_VOL = "/vol/models/q35_4b_main500k_init"
C1_ADAPTER_SHA = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
BASE = "Qwen/Qwen3.5-4B"
BASE_REV = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
BASE_SNAP = f"/vol/hf/hub/models--Qwen--Qwen3.5-4B/snapshots/{BASE_REV}"
BASE_SHARDS = {"model.safetensors-00001-of-00002.safetensors": "26a93f066e1916adb13453dae5a0c707c0fbc71299ed98779571a907b8e74c61",
               "model.safetensors-00002-of-00002.safetensors": "cb544bd9bfae93dc59b0f22b292f5933573854a7f9b97835c67060d7d910e188"}
BASE_SMALL = ("model.safetensors.index.json", "config.json", "tokenizer.json", "tokenizer_config.json", "vocab.json",
              "merges.txt", "chat_template.jinja")
SEED = 20261013
FAMILIES = ("T40", "T41", "T42", "T43", "T44", "T45")
TRAIN_FILE, REL_FILE = "pilot_ab_train.jsonl", "pilot_ab_rel.jsonl"
CODE_MODULES = ("train_decoder", "decoder_io", "prism_x", "writeblock")
CODE_REF = "q35_4b_c_r1"       # the run whose trainer code the pilots use (A4/F2 trainer: lam_ord, aux_norm batch)
RESULT_FILES = ("adapter_config.json", "adapter_model.safetensors", "train_meta.json", "chat_template.jinja", "tokenizer.json",
                "tokenizer_config.json")   # = l4_reads.sh FILES
SMOKE_FILES = ("result.json", "adapter_config.json")
BACKUPS = Path(os.environ.get("BACKUPS", "/Users/aryamahadik/Documents/jev/backups/modal_models"))
TOKENIZER = Path.home() / ".cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots" / BASE_REV / "tokenizer.json"
TOKENIZER_SHA = "5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42"
NEVER_OPEN = ("ohs", "sealed", "c_spec/sealed_brief", "c_build/preread", "external_quarantine", "longbench_v2", "/.claude/",
              "/private/tmp/")

if modal.is_local():
    import common as C                                   # the harness's constants: this file must agree with them
    import modal_od
    for _k, _v in (("C1_NAME", C1_NAME), ("C1_INIT_VOL", C1_INIT_VOL), ("C1_ADAPTER_SHA", C1_ADAPTER_SHA), ("BASE", BASE),
                   ("BASE_REV", BASE_REV), ("SEED", SEED), ("FAMILIES", FAMILIES), ("TRAIN_FILE", TRAIN_FILE),
                   ("REL_FILE", REL_FILE)):
        assert getattr(C, _k) == _v, f"modal_parallel.{_k} differs from common.{_k}"
    PINNED = tuple(modal_od.PINNED35)
else:                                                    # inside a container: only the trainer modules are mounted
    C, modal_od, PINNED = None, None, ()

app = modal.App(APP_NAME)
vol = modal.Volume.from_name(VOLUME)                     # never create_if_missing: an empty volume would hide a wrong account
image = (
    modal.Image.debian_slim(python_version="3.12.10")
    .pip_install(*PINNED)                                # = modal_od.image35's pins, so the account's cached image layers match
    .env({"HF_HOME": "/vol/hf", "HF_HUB_ENABLE_HF_TRANSFER": "1", "TOKENIZERS_PARALLELISM": "false",
          "TRITON_CACHE_DIR": "/vol/triton_cache"})
    .add_local_python_source(*CODE_MODULES)              # the four modules whose sha256 train_meta records; nothing else
)
SECRETS = [modal.Secret.from_name(SECRET)]
FN = dict(image=image, volumes={"/vol": vol}, secrets=SECRETS, scaledown_window=SCALEDOWN_S)


# ====================================================================================== container side (runs on Modal)
def _sha256_file(path, chunk=1 << 24) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def _heartbeat(key: str, state: str, **kw) -> None:
    """One Dict key per state (key:started, key:done, key:failed), so the watcher never loses the start time."""
    try:
        d = modal.Dict.from_name(HB_DICT, create_if_missing=True)
        d[f"{key}:{state}"] = {**kw, "state": state, "t": time.time()}
    except Exception:  # noqa: BLE001  (a missing heartbeat only weakens the watchdog; it never stops the pilot)
        pass


def _prepare(name: str, cfg: dict, blob: dict) -> tuple:
    """Verifies C1 on the volume, writes the two staged files (sha256-checked against the laptop's stage.json), and refuses an
    output folder that already exists. Returns (data_dir, out_dir, init_sha)."""
    init_sha = _sha256_file(f"{cfg['init_adapter']}/adapter_model.safetensors")
    if init_sha != C1_ADAPTER_SHA:
        raise RuntimeError(f"init adapter sha256 {init_sha[:12]} is not C1's {C1_ADAPTER_SHA[:12]}")
    data = Path(f"/root/pilot_data/{name}")
    data.mkdir(parents=True, exist_ok=False)
    for key, fname in (("train", TRAIN_FILE), ("rel", REL_FILE)):
        raw = zlib.decompress(blob[key])
        got = hashlib.sha256(raw).hexdigest()
        if got != blob[key + "_sha"]:
            raise RuntimeError(f"{fname}: sha256 {got[:12]} differs from the staged {blob[key + '_sha'][:12]}")
        (data / fname).write_bytes(raw)
    out = Path(f"/vol/models/{name}")
    if out.exists():
        raise RuntimeError(f"{out} already exists on the volume (no re-pilot, no overwrite)")
    return data, out, init_sha


@app.function(gpu=GPU, timeout=TIMEOUT_S, max_containers=MAX_PARALLEL, **FN)
def train_pilot(name: str, cfg: dict, blob: dict, run_id: str) -> dict:
    """ONE pilot: a single uninterrupted pass (about 94 steps) from C1, exactly as the harness's modal_pilot.train_pilot."""
    t_in = time.time()
    key = f"{run_id}:{name}"
    _heartbeat(key, "started")
    try:
        import torch
        gpu = torch.cuda.get_device_name(0)
        if "H100" not in gpu or "80GB" not in gpu:
            raise RuntimeError(f"expected an H100 80GB, got {gpu!r}: not the reference GPU, refusing to train")
        data, out, init_sha = _prepare(name, cfg, blob)
        import decoder_io
        decoder_io.STYLE = cfg.get("style", "od")
        import train_decoder
        res = train_decoder.train(cfg, data, out, on_ckpt=vol.commit)
        vol.commit()
        adapter_sha = _sha256_file(out / "adapter_model.safetensors")
        wall = time.time() - t_in
        _heartbeat(key, "done", wall_s=wall)
        return {"name": name, "stopped": bool(res.get("stopped")), "meta": res["meta"], "wall_s": wall, "gpu": gpu,
                "init_sha": init_sha, "adapter_sha": adapter_sha, "t_start": t_in}
    except BaseException as e:  # noqa: BLE001
        _heartbeat(key, "failed", wall_s=time.time() - t_in, error=repr(e)[:300])
        raise


@app.function(timeout=600, cpu=1.0, memory=2048, **FN)
def smoke_pilot(name: str, cfg: dict, blob: dict, run_id: str) -> dict:
    """CPU stand-in for train_pilot (same arguments, same checks, same heartbeats; no GPU, no training). It writes a small
    result folder so that spawn, watch, pull and the app stop can be proven for cents."""
    t_in = time.time()
    key = f"{run_id}:{name}"
    _heartbeat(key, "started")
    try:
        data, out, init_sha = _prepare(name, cfg, blob)
        out.mkdir(parents=True)
        shutil.copy(f"{cfg['init_adapter']}/adapter_config.json", out / "adapter_config.json")
        (out / "result.json").write_text(json.dumps({"name": name, "rows": sum(1 for _ in open(data / TRAIN_FILE)),
                                                     "init_sha": init_sha, "smoke": True}))
        vol.commit()
        time.sleep(float(cfg.get("_smoke_sleep_s", 8)))
        wall = time.time() - t_in
        _heartbeat(key, "done", wall_s=wall)
        return {"name": name, "stopped": False, "meta": {"smoke": True}, "wall_s": wall, "gpu": "none", "init_sha": init_sha,
                "adapter_sha": "", "t_start": t_in}
    except BaseException as e:  # noqa: BLE001
        _heartbeat(key, "failed", wall_s=time.time() - t_in, error=repr(e)[:300])
        raise


@app.function(timeout=1800, cpu=2.0, memory=8192, **FN)
def preflight_cpu(expect: dict) -> dict:
    """No GPU. Checks, inside the very image and volume a pilot uses: pinned packages, imports, trainer code hashes, config keys,
    the base model files (sha256 + safetensors headers + read speed), C1 on the volume, free output names, Triton cache,
    secret names, and an offline HF load of the config and tokenizer."""
    import importlib
    import importlib.metadata as md
    import platform
    t00 = time.time()
    out = {"checks": {}, "info": {}}

    def chk(name, ok, detail=""):
        out["checks"][name] = {"ok": bool(ok), "detail": str(detail)[:600]}

    def norm(n):
        return re.sub(r"[-_.]+", "-", n).lower()

    inst, loc, extra_copies = {}, {}, {}
    for d in md.distributions():
        try:
            n, path = norm(d.metadata["Name"]), str(getattr(d, "_path", ""))
        except Exception:  # noqa: BLE001
            continue
        if n in inst:                                   # two copies: Modal's client mount (/pkg) carries its own dependencies
            extra_copies.setdefault(n, []).append((d.version, path))
            if "site-packages" not in path or "/pkg" in path:
                continue
        inst[n], loc[n] = d.version, path
    bad = []
    for pin in expect["pins"]:
        n, v = pin.split("==")
        if inst.get(norm(n)) != v:
            bad.append(f"{n}: wanted {v}, have {inst.get(norm(n))} at {loc.get(norm(n), '?')[-60:]}")
    out["info"]["pin_mismatches"] = bad
    out["info"]["duplicate_distributions"] = {"n": len(extra_copies), "where": sorted({v[0][1].rsplit("/", 1)[0] for v in extra_copies.values()})}
    chk("pins_equal_PINNED35", not bad, f"{len(expect['pins'])} pins; {len(bad)} mismatched: {bad[:4]}")
    env_bad = []
    for pkg, want in expect["env"].items():
        if pkg in ("python", "torch_cuda", "cudnn", "gpu", "sm_count"):
            continue
        if inst.get(norm(pkg)) != want:
            env_bad.append(f"{pkg}: C1 round-1 trained with {want}, here {inst.get(norm(pkg))}")
    chk("env_equals_C1_round1_record", not env_bad and platform.python_version() == expect["env"]["python"],
        f"python {platform.python_version()}; {env_bad[:6]}")
    t = time.time()
    imp_fail = {}
    for m in ("torch", "transformers", "peft", "accelerate", "tokenizers", "safetensors", "numpy", "huggingface_hub"):
        try:
            importlib.import_module(m)
        except Exception as e:  # noqa: BLE001
            imp_fail[m] = repr(e)[:150]
    chk("imports_core", not imp_fail, imp_fail)
    import torch
    out["info"]["torch_cuda"] = torch.version.cuda
    try:
        out["info"]["cudnn"] = torch.backends.cudnn.version()
    except Exception as e:  # noqa: BLE001
        out["info"]["cudnn"] = repr(e)[:80]
    chk("torch_cuda_cudnn_equal_C1_record",
        str(torch.version.cuda) == str(expect["env"]["torch_cuda"]) and out["info"]["cudnn"] == expect["env"]["cudnn"],
        f"cuda {torch.version.cuda}, cudnn {out['info']['cudnn']}")
    gpu_only = {}
    for m in ("triton", "fla"):
        try:
            importlib.import_module(m)
        except Exception as e:  # noqa: BLE001
            gpu_only[m] = repr(e)[:150]
    out["info"]["gpu_only_imports_failed_on_cpu"] = gpu_only        # informational: triton/fla may need a GPU to import
    try:
        import train_decoder
        import decoder_io
        import prism_x
        import writeblock
        mods = {"train_decoder": train_decoder, "decoder_io": decoder_io, "prism_x": prism_x, "writeblock": writeblock}
        got = {k: _sha256_file(m.__file__) for k, m in mods.items()}
        chk("trainer_code_equals_C1_round1_train_meta", got == expect["code"],
            {k: (got[k][:10], expect["code"][k][:10]) for k in got if got[k] != expect["code"][k]})
        unknown = sorted(set(expect["cfg_keys"]) - set(train_decoder.KNOWN_KEYS))
        chk("pilot_config_keys_known_to_trainer", not unknown, unknown)
        chk("pad_multiple_and_layout_defaults", decoder_io.PAD_MULTIPLE == expect["pad_multiple"],
            f"PAD_MULTIPLE {decoder_io.PAD_MULTIPLE}")
    except Exception as e:  # noqa: BLE001
        chk("trainer_modules_import", False, repr(e))
    out["info"]["import_s"] = round(time.time() - t, 1)
    # ---- the base model on the volume
    snap = Path(BASE_SNAP)
    if not snap.is_dir():
        chk("base_snapshot_on_volume", False, f"{snap} missing")
    else:
        miss = [f for f in BASE_SMALL + tuple(BASE_SHARDS) if not (snap / f).exists()]
        size_bad = [f"{f}: {(snap / f).stat().st_size} != {n}" for f, n in expect["base_sizes"].items()
                    if (snap / f).exists() and (snap / f).stat().st_size != n]
        chk("base_files_present_and_sizes", not miss and not size_bad, f"missing {miss}; {size_bad}")
        t = time.time()
        sha_bad, nbytes = [], 0
        for f, want in BASE_SHARDS.items():
            if (snap / f).exists():
                nbytes += (snap / f).stat().st_size
                if _sha256_file(snap / f) != want:
                    sha_bad.append(f)
        sec = time.time() - t
        chk("base_shards_sha256", not sha_bad and nbytes > 0, f"bad: {sha_bad}")
        out["info"]["base_read_gb_per_s_incl_sha256"] = round(nbytes / 1e9 / max(sec, 1e-9), 2)
        out["info"]["base_read_s"] = round(sec, 1)
        hdr_bad = []
        for f in BASE_SHARDS:
            p = snap / f
            if p.exists():
                with open(p, "rb") as fh:
                    n = int.from_bytes(fh.read(8), "little")
                    hd = json.loads(fh.read(n))
                end = max((v["data_offsets"][1] for k, v in hd.items() if k != "__metadata__"), default=0)
                if 8 + n + end != p.stat().st_size:
                    hdr_bad.append(f)
        chk("base_safetensors_headers_complete", not hdr_bad, hdr_bad)
        try:
            idx = json.loads((snap / "model.safetensors.index.json").read_text())
            need = set(idx["weight_map"].values())
            chk("base_index_shards_exist", need <= set(BASE_SHARDS), sorted(need))
        except Exception as e:  # noqa: BLE001
            chk("base_index_shards_exist", False, repr(e))
        try:
            old = {k: os.environ.get(k) for k in ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE")}
            os.environ["HF_HUB_OFFLINE"] = os.environ["TRANSFORMERS_OFFLINE"] = "1"
            from transformers import AutoConfig, AutoTokenizer
            cfgm = AutoConfig.from_pretrained(BASE, revision=BASE_REV)
            tk = AutoTokenizer.from_pretrained(BASE, revision=BASE_REV)
            chk("hf_offline_load_config_tokenizer", True, f"{type(cfgm).__name__}, vocab {len(tk)}")
        except Exception as e:  # noqa: BLE001
            chk("hf_offline_load_config_tokenizer", False, repr(e)[:300])
    # ---- C1 on the volume
    for label, d in (("init", C1_INIT_VOL), ("main500k", "/vol/models/q35_4b_main500k")):
        p = Path(d) / "adapter_model.safetensors"
        if not p.exists():
            chk(f"c1_adapter_{label}", False, f"{p} missing" + ("; run `prep-init`" if label == "init" else ""))
        else:
            chk(f"c1_adapter_{label}", _sha256_file(p) == C1_ADAPTER_SHA, f"{p.stat().st_size} bytes")
    pc = Path(C1_INIT_VOL) / "adapter_config.json"
    if pc.exists():
        chk("c1_adapter_config_equals_backup", hashlib.sha256(pc.read_bytes()).hexdigest() == expect["adapter_config_sha"],
            "adapter_config.json")
    # ---- output names free, leftovers
    models = Path("/vol/models")
    existing = sorted(p.name for p in models.iterdir()) if models.is_dir() else []
    taken = [n for n in expect["out_names"] if n in existing]
    chk("pilot_output_names_free", not taken, taken)
    out["info"]["leftover_par_folders"] = [n for n in existing if n.startswith("_par_")]
    # ---- Triton cache
    t = time.time()
    tc = Path("/vol/triton_cache")
    n_dir = n_bwd = n_json = 0
    if tc.is_dir():
        for p in tc.iterdir():
            n_dir += 1
            if time.time() - t > 20:
                break
            for q in p.glob("*.json"):
                n_json += 1
                if "bwd" in q.name or "bwd" in q.read_text(errors="ignore")[:4000]:
                    n_bwd += 1
                    break
    out["info"]["triton_cache"] = {"dirs": n_dir, "dirs_with_bwd_kernel_json": n_bwd,
                                   "note": "0 bwd entries = cold training kernels: the first steps autotune (about 60 s per pilot)"}
    # ---- secret names only, host
    names = sorted(k for k in os.environ if any(s in k.upper() for s in ("TOKEN", "KEY", "SECRET")))
    chk("secret_opendecide_keys_present", bool(names), names)
    out["info"]["cpus"] = os.cpu_count()
    out["info"]["python"] = platform.python_version()
    out["info"]["hf_home"] = os.environ.get("HF_HOME")
    out["info"]["triton_cache_dir"] = os.environ.get("TRITON_CACHE_DIR")
    out["info"]["wall_s"] = round(time.time() - t00, 1)
    return out


# ====================================================================================== laptop side
class Refuse(SystemExit):
    pass


def refuse_path(p) -> str:
    s = str(p)
    hit = [b for b in NEVER_OPEN if b in s.lower()]
    if hit:
        raise Refuse(f"REFUSED (never-open path, matches {hit}): {s}")
    return s


def _sh(args, timeout=120) -> str:
    modal_bin = str(Path(sys.executable).parent / "modal")
    r = subprocess.run([modal_bin] + args, capture_output=True, text=True, timeout=timeout, env=os.environ.copy())
    if r.returncode != 0:
        raise RuntimeError(f"modal {' '.join(args)} failed: {r.stderr.strip()[-300:]}")
    return r.stdout


def check_profile() -> None:
    """The account is fixed: MODAL_PROFILE must be mahadikarya44, no token env override, and the active profile must be it."""
    prof = os.environ.get("MODAL_PROFILE", "")
    if prof != PROFILE:
        raise Refuse(f"MODAL_PROFILE is {prof!r}, not {PROFILE!r}: the owner approved {PROFILE} ONLY for these pilots "
                     f"(never {', '.join(NEVER_PROFILES)}); export MODAL_PROFILE={PROFILE}")
    for k in ("MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET"):
        if os.environ.get(k):
            raise Refuse(f"{k} is set and would override the profile; unset it")
    active = getattr(modal.config, "_profile", None)
    if active != PROFILE:
        raise Refuse(f"the Modal client resolved profile {active!r}, expected {PROFILE!r}")
    prof_list = json.loads(_sh(["profile", "list", "--json"]))
    me = [p for p in prof_list if p["name"] == PROFILE]
    if not me or me[0]["workspace"] != PROFILE or not me[0]["active"]:
        raise Refuse(f"profile list does not show {PROFILE} as the active profile of workspace {PROFILE}")


# ---------------------------------------------------------------------------------------------------------------- ledger
def ledger_path(root: Path, smoke=False) -> Path:
    return Path(root) / "par_runs" / ("ledger_smoke.json" if smoke else "ledger.json")


def new_ledger(smoke=False) -> dict:
    return {"version": 1, "profile": PROFILE, "cap_usd": CAP_USD, "smoke": smoke, "created_unix": time.time(),
            "other_spend": [], "pilots": {}, "apps": [], "launches": []}


@contextmanager
def locked_ledger(root: Path, smoke=False):
    """Read-modify-write of the ledger under an exclusive file lock; written atomically on exit."""
    p = ledger_path(root, smoke)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p.with_suffix(".lock"), "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        led = json.loads(p.read_text()) if p.exists() else new_ledger(smoke)
        try:
            yield led
        finally:
            tmp = p.with_suffix(".tmp")
            tmp.write_text(json.dumps(led, indent=2, default=float) + "\n")
            os.replace(tmp, p)


def load_ledger(root: Path, smoke=False) -> dict:
    p = ledger_path(root, smoke)
    return json.loads(p.read_text()) if p.exists() else new_ledger(smoke)


SMOKE_RATE_H = 0.07            # CPU stand-in container (1 core, 2 GiB): 0.0473 + 2 x 0.008 per hour, rounded up


def usd(seconds: float, rate=RATE_H) -> float:
    return seconds * rate / 3600.0


FINISHED = ("done", "failed", "cancelled")
PREFLIGHT_MAX_AGE_S = 72 * 3600


def preflight_ok(led: dict, now=None) -> bool:
    """A passing `preflight` (image, volume, imports, C1 and base on the volume) must be on record before a paid launch."""
    pf = led.get("preflight") or {}
    return bool(pf.get("ok")) and (now or time.time()) - pf.get("unix", 0) < PREFLIGHT_MAX_AGE_S


def pilot_elapsed_s(p: dict, now: float) -> float:
    """Billed seconds so far of an unfinished pilot: from the container's first heartbeat (queue time is not billed),
    else from the spawn (an upper bound)."""
    t0 = p.get("hb_start_unix") or p.get("spawn_unix") or now
    return max(0.0, now - t0) + BOOT_S + SCALEDOWN_S


def pilot_observed_usd(p: dict, now: float) -> float:
    if p["state"] in FINISHED and p.get("usd") is not None:
        return p["usd"]
    if p["state"] in FINISHED:
        return usd(pilot_elapsed_s(p, p.get("end_unix", now)))
    if not p.get("hb_start_unix") and now - p.get("spawn_unix", now) < QUEUE_GRACE_S:
        return 0.0                                        # still queued: not billed yet (the reservation covers it)
    return usd(pilot_elapsed_s(p, now))


def pilot_reserved_usd(p: dict, now: float) -> float:
    """What the guard holds for a pilot: its actual cost when finished, else max(pessimistic estimate, observed so far)."""
    if p["state"] in FINISHED:
        return pilot_observed_usd(p, now)
    return max(p["pess_usd"], pilot_observed_usd(p, now))


def committed_usd(led: dict, now=None) -> float:
    now = now or time.time()
    return round(sum(o["usd"] for o in led["other_spend"]) + sum(pilot_reserved_usd(p, now) for p in led["pilots"].values()), 4)


def observed_usd(led: dict, now=None) -> float:
    now = now or time.time()
    return round(sum(o["usd"] for o in led["other_spend"]) + sum(pilot_observed_usd(p, now) for p in led["pilots"].values()), 4)


def hard_stop_at(n_running: int, poll: float) -> float:
    """Observed-spend level at which `watch` cancels everything: the cap minus a margin minus what the running containers
    add during one poll interval."""
    return CAP_USD - HARD_STOP_MARGIN - n_running * usd(poll)


def calibrate_pess(led: dict, est: dict) -> float:
    """Pessimistic cost of a pilot still to launch. A priori it is est['pess_usd']; once real pilots have finished, the measured
    actual/estimate ratio replaces the assumptions: pess = est x max(ratio, 0.9) x 1.15, never above the a-priori pess and
    never below est x 1.05."""
    done = [p for p in led["pilots"].values() if p["state"] == "done" and not p.get("smoke") and p.get("usd") and p.get("est_usd")]
    if not done:
        return est["pess_usd"]
    ratio = sum(p["usd"] for p in done) / sum(p["est_usd"] for p in done)
    return round(max(est["usd"] * 1.05, min(est["pess_usd"], est["usd"] * max(ratio, 0.9) * 1.15)), 4)


def plan_launch(led: dict, cands: list, cap=CAP_USD, max_parallel=MAX_PARALLEL, now=None) -> dict:
    """cands = [(fam, pess_usd)] in priority order. Launch a pilot only if committed + pess <= cap and fewer than max_parallel
    pilots would be running; everything else is deferred with the reason. Pure function."""
    now = now or time.time()
    committed = committed_usd(led, now)
    running = sum(1 for p in led["pilots"].values() if p["state"] not in FINISHED)
    launch, deferred = [], []
    for fam, pess in cands:
        if running + len(launch) >= max_parallel:
            deferred.append((fam, f"parallel limit {max_parallel}"))
        elif committed + pess > cap + 1e-9:
            deferred.append((fam, f"projected {committed + pess:.2f} USD > cap {cap:.2f} (committed {committed:.2f} + pess {pess:.2f})"))
        else:
            launch.append((fam, pess))
            committed += pess
    return {"launch": launch, "deferred": deferred, "committed_after": round(committed, 4), "cap": cap}


# ---------------------------------------------------------------------------------------------------------------- estimate
def token_counts(rows) -> list:
    """Real Qwen3.5 tokenizer on the rendered training prompt (as c_build/mixer.token_counts, without the input log)."""
    from tokenizers import Tokenizer
    import decoder_io as dio
    if _sha256_file(TOKENIZER) != TOKENIZER_SHA:
        raise Refuse("tokenizer.json is not the pinned Qwen3.5-4B snapshot")
    tok = Tokenizer.from_file(str(TOKENIZER))
    U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    wide = [w for w in (a + b for a in U for b in U) if len(tok.encode(w, add_special_tokens=False).ids) == 1]
    saved = (dio.STYLE, dio.LAYOUT, dio.WIDE)
    dio.WIDE = list(dio.LETTERS) + wide[: dio.MAX_OPTIONS - 26]
    dio.STYLE, dio.LAYOUT = "cygnet", "schema_branch_mark"
    try:
        out = []
        for i in range(0, len(rows), 2000):
            out += [len(e.ids) for e in tok.encode_batch([dio.CYGNET_SYSTEM + "\n" + dio.user_msg(r) for r in rows[i:i + 2000]])]
        return out
    finally:
        dio.STYLE, dio.LAYOUT, dio.WIDE = saved


def padded_projection(rows, rels, ntok: dict, n_steps: int, seed=SEED, batch=16, perm_twin=0.3, micro_tokens=8192) -> dict:
    """Padded tokens per step through the trainer's own batching (as c2_build/mix_c2.project_cost; rows and their perm twins,
    micro-batch longest length rounded up to PAD_MULTIPLE)."""
    import decoder_io as dio
    import train_decoder as td
    units, _ = td.make_units(rows, rels)
    uid = {r["id"]: k for k, u in enumerate(units) for r in u}
    pad = max(1, dio.PAD_MULTIPLE)
    padded = lambda n: -(-min(int(n), dio.MAX_LEN) // pad) * pad   # noqa: E731
    st = random.getstate()
    pt = rt = micro = twins = 0
    try:
        random.seed(seed)
        twin_rng = random.Random(seed + 1)
        gen = td._BATCHES(list(units), batch)
        for _ in range(n_steps):
            b = next(gen)
            perms = [random.sample(range(len(r["options"])), len(r["options"])) if r["qtype"] == "choice"
                     else random.sample([0, 1], 2) for r in b]
            tw = td.pick_twins(b, perms, perm_twin, twin_rng)
            twins += len(tw)
            for g in td._micro_groups(b, uid, tw, micro_tokens):
                gs = set(g)
                lens = [ntok[b[i]["id"]] for i in g] + [ntok[b[i]["id"]] for i, _ in tw if i in gs]
                pt += len(lens) * padded(max(lens))
                rt += sum(lens)
                micro += 1
    finally:
        random.setstate(st)
    return {"padded_per_step": pt / n_steps, "real_per_step": rt / n_steps, "micro_per_step": micro / n_steps,
            "twins_per_step": twins / n_steps, "pad_multiple": pad}


def cost_from(padded_per_step: float, steps: int = STEPS_PER_PILOT) -> dict:
    s_step = padded_per_step * MS_PER_PADDED / 1000.0
    fixed_c = sum(v[0] for v in FIXED_S.values())
    fixed_p = sum(v[1] for v in FIXED_S.values())
    train_c, train_p = steps * s_step, steps * s_step * STEP_PESS_FACTOR
    return {"steps": steps, "s_per_step": round(s_step, 3), "train_min": round(train_c / 60, 2),
            "fixed_s_central": fixed_c, "fixed_s_pess": fixed_p,
            "minutes": round((fixed_c + train_c) / 60, 2), "usd": round(usd(fixed_c + train_c), 3),
            "minutes_pess": round((fixed_p + train_p) / 60, 2), "pess_usd": round(usd(fixed_p + train_p), 3),
            "rate_per_h": RATE_H, "padded_per_step": round(padded_per_step, 1)}


def scenario_table(means=(500, 600, 740, 800, 917)) -> list:
    rows = []
    for m in means:
        c = cost_from(m * PADDED_PER_MEAN_TOKEN)
        rows.append({"mean_row_tokens": m, "s_per_step": c["s_per_step"], "minutes": c["minutes"], "usd": c["usd"],
                     "pess_usd": c["pess_usd"], "six_pilots_usd": round(6 * c["usd"], 2), "six_pess_usd": round(6 * c["pess_usd"], 2)})
    return rows


def stage_paths(root: Path, fam: str) -> dict:
    root = Path(root)
    return {"cfg": root / "configs" / f"{fam}.json", "info": root / "configs" / f"{fam}.stage.json",
            "dir": root / "stage" / fam, "spawned": root / "configs" / f"{fam}.spawned.json"}


def load_family(root: Path, fam: str, need_files=True) -> dict:
    """The harness's frozen config and staged files for one family, checked as modal_pilot._local_checks/_cfg_for_run do."""
    sp = stage_paths(root, fam)
    for k in ("cfg", "info"):
        if not sp[k].exists():
            raise Refuse(f"{fam}: {sp[k]} missing; run make_config.py for this family first")
    raw = json.loads(sp["cfg"].read_text())
    info = json.loads(sp["info"].read_text())
    required = tuple(modal_od.RELAY_REQUIRED) + ("init_adapter", "expect_kd_targets", "expect_kd_full", "expect_trainable",
                                                 "expect_ord_rows")
    missing = [k for k in required if k not in raw]
    if missing:
        raise Refuse(f"{fam}: configs missing keys {missing}")
    cfg = dict(raw)
    name = cfg.pop("name")
    if name != C.pilot_name(fam) or cfg["seed"] != SEED or cfg["init_adapter"] != C1_INIT_VOL:
        raise Refuse(f"{fam}: config name / seed / init_adapter differ from A42-D 4.1")
    if cfg["targets"] == "QWEN35":
        cfg["targets"] = modal_od.QWEN35_TARGETS
    cfg.update({"no_overwrite": True, "expect_resume": False, "stop_at_step": 0, "stop_at_unix": 0})
    out = {"fam": fam, "name": name, "cfg": cfg, "info": info, "steps": info["steps"]}
    if need_files:
        files = sorted(p.name for p in sp["dir"].iterdir()) if sp["dir"].is_dir() else []
        if files != sorted((TRAIN_FILE, REL_FILE)):
            raise Refuse(f"{fam}: stage folder holds {files}, expected exactly the two staged files")
        blob = {}
        for f, key, hk in ((TRAIN_FILE, "train", "train_sha256"), (REL_FILE, "rel", "rel_sha256")):
            raw_b = (sp["dir"] / f).read_bytes()
            if hashlib.sha256(raw_b).hexdigest() != info[hk]:
                raise Refuse(f"{f}: sha256 differs from {sp['info'].name}; rerun make_config")
            blob[key] = zlib.compress(raw_b, 6)
            blob[key + "_sha"] = info[hk]
        out["blob"] = blob
    return out


def estimate_family(root: Path, fam: str) -> dict:
    """Cost of one pilot from its staged rows (real tokens through the trainer's batching), else None."""
    sp = stage_paths(root, fam)
    if not (sp["info"].exists() and (sp["dir"] / TRAIN_FILE).exists()):
        return {"fam": fam, "staged": False}
    info = json.loads(sp["info"].read_text())
    rows = [json.loads(l) for l in open(refuse_path(sp["dir"] / TRAIN_FILE)) if l.strip()]
    rels = [json.loads(l) for l in open(refuse_path(sp["dir"] / REL_FILE)) if l.strip()]
    ntok = dict(zip((r["id"] for r in rows), token_counts(rows)))
    proj = padded_projection(rows, rels, ntok, info["steps"])
    est = cost_from(proj["padded_per_step"], info["steps"])
    est.update({"fam": fam, "staged": True, "rows": len(rows), "mean_row_tokens": round(sum(ntok.values()) / len(ntok), 1),
                "max_row_tokens": max(ntok.values()), "real_per_step": round(proj["real_per_step"], 1),
                "twins_per_step": round(proj["twins_per_step"], 2)})
    return est


# ---------------------------------------------------------------------------------------------------------------- billing
def billing_state() -> dict:
    """Free credit left on mahadikarya44 (monthly 30 USD minus credits used) and today's per-app cost, from `modal billing`."""
    s = json.loads(_sh(["billing", "summary", "--json"]))
    used = -float(s["adjustments"]["credits"])
    try:
        today = json.loads(_sh(["billing", "report", "--for", "today", "--json"]))
    except Exception as e:  # noqa: BLE001
        today = [{"error": repr(e)[:120]}]
    return {"credits_used_usd": round(used, 4), "credit_left_usd": round(FREE_CREDIT_USD - used, 4),
            "billed_cost_usd": float(s.get("billed_cost", 0)), "metered_cost_usd": float(s.get("metered_cost", 0)),
            "today_by_app": today}


# ---------------------------------------------------------------------------------------------------------------- local checks
def local_checks(root: Path) -> dict:
    """Laptop-side checks that need no network: C1 backup, trainer code hashes (vs the round-1 run, see below), constants."""
    out = {}
    ref = BACKUPS / CODE_REF / "train_meta.json"
    code_now = {m: _sha256_file(C.LEAN / f"{m}.py") for m in CODE_MODULES}
    meta = json.loads(ref.read_text())
    out["code_ref"] = {"run": CODE_REF, "match": meta.get("code") == code_now,
                       "now": {k: v[:12] for k, v in code_now.items()}, "ref": {k: v[:12] for k, v in meta.get("code", {}).items()}}
    c1 = BACKUPS / C1_NAME / "train_meta.json"
    c1code = json.loads(c1.read_text()).get("code", {}) if c1.exists() else {}
    out["note_c1_main_code_differs"] = c1code != code_now          # expected: harness modal_pilot.py compares to THIS and refuses
    out["env_ref"] = meta.get("env", {})
    out["code"] = code_now
    a = BACKUPS / C1_NAME / "adapter_model.safetensors"
    out["c1_backup_sha_ok"] = a.exists() and _sha256_file(a) == C1_ADAPTER_SHA
    out["adapter_config_sha"] = hashlib.sha256((BACKUPS / C1_NAME / "adapter_config.json").read_bytes()).hexdigest()
    return out


def base_sizes_local() -> dict:
    snap = Path.home() / ".cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots" / BASE_REV
    return {f: (snap / f).resolve().stat().st_size for f in BASE_SMALL + tuple(BASE_SHARDS) if (snap / f).exists()}


def run_app(fn_name: str, args: tuple, detach=False, timeout_note=""):
    """Runs one function of this app inside app.run(); returns (result, app_id)."""
    with modal.enable_output():
        with app.run(detach=detach) as ra:
            fn = {"preflight_cpu": preflight_cpu, "smoke_pilot": smoke_pilot, "train_pilot": train_pilot}[fn_name]
            return fn.remote(*args), ra.app_id


def cmd_preflight(a) -> int:
    check_profile()
    root = Path(a.root)
    lc = local_checks(root)
    fail = 0
    print(json.dumps({"local": {k: v for k, v in lc.items() if k not in ("env_ref", "code")}}, indent=1))
    if not lc["code_ref"]["match"]:
        print("LOCAL FAIL: trainer code differs from the round-1 run's train_meta"); fail += 1
    if not lc["c1_backup_sha_ok"]:
        print("LOCAL FAIL: the C1 backup adapter is not sha256 507d1c29"); fail += 1
    if lc["note_c1_main_code_differs"]:
        print("NOTE: modal_pilot.py (the harness's single launcher) compares the trainer code with q35_4b_main500k's train_meta and "
              "would refuse to launch; the pilots use the round-1 trainer (lam_ord, aux_norm batch), so this file compares with "
              f"{CODE_REF}.")
    cfg_keys = []
    try:
        import make_config as M
        cfg_keys = sorted((set(M.base_config("T40", 1.0, 0, 0, 0)) - {"name"}) | {"expect_resume", "stop_at_step", "stop_at_unix"})
    except Exception as e:  # noqa: BLE001
        print("LOCAL FAIL: make_config import:", repr(e)); fail += 1
    import decoder_io
    expect = {"pins": list(PINNED), "env": lc["env_ref"], "code": lc["code"], "cfg_keys": cfg_keys, "pad_multiple": decoder_io.PAD_MULTIPLE,
              "base_sizes": base_sizes_local(), "adapter_config_sha": lc["adapter_config_sha"],
              "out_names": [C.pilot_name(f) for f in FAMILIES]}
    if a.local_only:
        return 1 if fail else 0
    t = time.time()
    res, app_id = run_app("preflight_cpu", (expect,))
    wall = time.time() - t
    for k, v in res["checks"].items():
        print(f"{'PASS' if v['ok'] else 'FAIL'}  {k}  {v['detail'] if not v['ok'] or len(str(v['detail'])) < 120 else ''}")
        fail += 0 if v["ok"] else 1
    print(json.dumps(res["info"], indent=1))
    cpu_usd = round(res["info"]["wall_s"] * (2 * 0.0473 + 8 * 0.008) / 3600 + 0.002, 4)
    with locked_ledger(root) as led:
        led["other_spend"].append({"what": "preflight_cpu container (CPU 2, 8 GiB)", "usd": cpu_usd, "unix": time.time(),
                                   "app_id": app_id, "wall_s": round(wall, 1)})
        led["preflight"] = {"unix": time.time(), "ok": fail == 0, "info": res["info"],
                            "checks": {k: v["ok"] for k, v in res["checks"].items()}}
    print(f"preflight {'OK' if not fail else 'FAILED (' + str(fail) + ')'}; app {app_id} (one-shot; stops itself); cpu cost ~{cpu_usd} USD")
    return 1 if fail else 0


def cmd_prep_init(a) -> int:
    """Server-side copy of C1 (models/q35_4b_main500k -> models/q35_4b_main500k_init) and a sha256 re-read. Free, idempotent."""
    check_profile()
    v = modal.Volume.from_name(VOLUME)

    def sha_of(path):
        h = hashlib.sha256()
        for chunk in v.read_file(path):
            h.update(chunk)
        return h.hexdigest()
    dst = "models/" + C1_INIT_VOL.rsplit("/", 1)[1]
    try:
        if sha_of(f"{dst}/adapter_model.safetensors") == C1_ADAPTER_SHA:
            print("init adapter already on the volume with C1's sha256; left alone")
            return 0
    except Exception:  # noqa: BLE001
        pass
    if sha_of(f"models/{C1_NAME}/adapter_model.safetensors") != C1_ADAPTER_SHA:
        raise Refuse(f"models/{C1_NAME} on this volume is not C1 (sha256)")
    for f in ("adapter_config.json", "adapter_model.safetensors"):     # file to file: the destination folder does not exist yet
        v.copy_files([f"models/{C1_NAME}/{f}"], f"{dst}/{f}")
    got = sha_of(f"{dst}/adapter_model.safetensors")
    print(json.dumps({"copied_to": dst, "adapter_sha256": got, "ok": got == C1_ADAPTER_SHA}))
    return 0 if got == C1_ADAPTER_SHA else 1


def families_arg(a) -> list:
    fams = [f.strip() for f in a.families.split(",") if f.strip()]
    bad = [f for f in fams if f not in FAMILIES]
    if bad:
        raise Refuse(f"unknown family {bad}; pilots are {FAMILIES}")
    return sorted(set(fams), key=FAMILIES.index)


def cmd_estimate(a) -> int:
    root = Path(a.root)
    out = {"rate_usd_per_h": RATE_H, "list_h100_usd_per_h": LIST_H100_H, "fixed_s": FIXED_S, "cap_usd": CAP_USD, "scenarios": scenario_table(),
           "per_family": [], "note": "scenarios: mean real tokens per row (the A42-D bar is <= 800 for a family mean)"}
    for f in families_arg(a):
        out["per_family"].append(estimate_family(root, f))
    done = [e for e in out["per_family"] if e.get("staged")]
    if done:
        out["sum_usd"] = round(sum(e["usd"] for e in done), 3)
        out["sum_pess_usd"] = round(sum(e["pess_usd"] for e in done), 3)
    print(json.dumps(out, indent=1))
    return 0


def orphans(led: dict) -> list:
    """Running apps of this name that the ledger does not know."""
    apps = json.loads(_sh(["app", "list", "--json"]))
    known = {x["id"] for x in led["apps"]}
    return [x["app_id"] for x in apps if x.get("description") == APP_NAME and x.get("state") not in ("stopped", "stopping")
            and x["app_id"] not in known]


def volume_names() -> set:
    v = modal.Volume.from_name(VOLUME)
    return {Path(e.path).name for e in v.listdir("models")}


def decide(a, smoke=False) -> dict:
    """Everything `plan` and `launch` share: staged families, estimates, credit, guard decision."""
    check_profile()
    root = Path(a.root)
    fams = families_arg(a)
    led = load_ledger(root, smoke)
    notes, cands, fam_info = [], [], {}
    on_vol = volume_names()
    for f in fams:
        old = led["pilots"].get(f)
        if old and not (a.retry_failed and old["state"] in ("failed", "cancelled")):
            notes.append((f, f"already in the ledger as {old['state']} (no re-pilot)")); continue
        target = ("_par_smoke_" + f) if smoke else C.pilot_name(f)
        if target in on_vol:
            notes.append((f, f"{target} already on the volume (no overwrite)")); continue
        if (HERE.parent / "families" / f / "pilot_ab" / "PILOT_AB_VERDICT.json").exists():
            notes.append((f, "a verdict file exists (no re-pilot)")); continue
        try:
            fi = load_family(root, f)
        except Refuse as e:
            notes.append((f, str(e))); continue
        if smoke:
            est = {"usd": 0.01, "pess_usd": 0.02, "minutes": 0.5, "minutes_pess": 1.0, "smoke": True}
        else:
            est = estimate_family(root, f)
            if not est.get("staged"):
                notes.append((f, "no staged rows")); continue
        fam_info[f] = {"fi": fi, "est": est}
        cands.append((f, calibrate_pess(led, est) if not smoke else est["pess_usd"]))
    plan = plan_launch(led, cands)
    credit = billing_state()
    projected = plan["committed_after"]
    credit_ok = credit["credit_left_usd"] - projected >= CREDIT_MARGIN_USD or smoke
    orph = orphans(led)
    return {"root": root, "led": led, "plan": plan, "notes": notes, "fam": fam_info, "credit": credit, "credit_ok": credit_ok,
            "orphans": orph, "fams": fams}


def show_plan(d: dict) -> None:
    pl = d["plan"]
    print(json.dumps({
        "cap_usd": CAP_USD, "committed_now_usd": committed_usd(d["led"]), "launch": [
            {"family": f, "est_usd": d["fam"][f]["est"]["usd"], "pess_usd": p, "minutes": d["fam"][f]["est"]["minutes"]}
            for f, p in pl["launch"]],
        "deferred": [{"family": f, "why": w} for f, w in pl["deferred"]],
        "refused": [{"family": f, "why": w} for f, w in d["notes"]],
        "projected_total_after_launch_usd": pl["committed_after"],
        "credit": {k: d["credit"][k] for k in ("credit_left_usd", "credits_used_usd", "billed_cost_usd")},
        "credit_ok": d["credit_ok"], "orphan_apps": d["orphans"], "preflight_ok": preflight_ok(d["led"])}, indent=1))


def cmd_plan(a) -> int:
    d = decide(a, smoke=a.smoke)
    show_plan(d)
    return 0


def cmd_launch(a) -> int:
    d = decide(a, smoke=a.smoke)
    show_plan(d)
    root, plan = d["root"], d["plan"]
    if d["orphans"]:
        print("REFUSED: running apps not in the ledger:", d["orphans"]); return 2
    if not d["credit_ok"]:
        print(f"REFUSED: free credit left {d['credit']['credit_left_usd']} USD does not cover the projection "
              f"{plan['committed_after']} USD + {CREDIT_MARGIN_USD} margin"); return 2
    if a.strict and (plan["deferred"] or d["notes"]):
        print("REFUSED (--strict): not every requested pilot fits / is ready"); return 2
    if not plan["launch"]:
        print("nothing to launch"); return 0 if not d["notes"] else 2
    if not a.go:
        print("dry run (no --go): nothing spawned"); return 0
    if not a.smoke and not preflight_ok(d["led"]):
        print("REFUSED: no passing `preflight` on record in the last 72 h (run it: it costs about 0.005 USD)"); return 2
    run_id = time.strftime("%Y%m%dT%H%M%S", time.gmtime())
    fn = smoke_pilot if a.smoke else train_pilot
    spawned = []
    with locked_ledger(root, a.smoke) as led:
        # recompute under the lock: another launcher cannot have slipped in
        pl = plan_launch(led, [(f, p) for f, p in plan["launch"]])
        if [f for f, _ in pl["launch"]] != [f for f, _ in plan["launch"]]:
            print("REFUSED: the ledger changed while planning; run again"); return 2
        with modal.enable_output():
            try:
                modal.Dict.from_name(HB_DICT, create_if_missing=True)
            except Exception as e:  # noqa: BLE001
                print("warning: heartbeat dict unavailable:", repr(e)[:100])
            with app.run(detach=True) as ra:
                led["apps"].append({"id": ra.app_id, "unix": time.time(), "run_id": run_id})
                for f, pess in plan["launch"]:
                    fi, est = d["fam"][f]["fi"], d["fam"][f]["est"]
                    cfg, name = dict(fi["cfg"]), fi["name"]
                    if a.smoke:
                        name = "_par_smoke_" + f
                        cfg["_smoke_sleep_s"] = a.smoke_sleep
                    call = fn.spawn(name, cfg, fi["blob"], run_id)
                    print(f"{f}: payload {len(fi['blob']['train']) + len(fi['blob']['rel'])} bytes compressed", flush=True)
                    led["pilots"][f] = {"state": "spawned", "name": name, "call_id": call.object_id, "app_id": ra.app_id,
                                        "run_id": run_id, "spawn_unix": time.time(), "est_usd": est["usd"], "pess_usd": pess,
                                        "est": {k: v for k, v in est.items() if k != "fam"}, "smoke": a.smoke,
                                        "files": list(SMOKE_FILES if a.smoke else RESULT_FILES), "timeout_s": TIMEOUT_S}
                    sp = stage_paths(root, f)["spawned"]
                    sp.parent.mkdir(parents=True, exist_ok=True)
                    sp.write_text(json.dumps({"name": name, "call_id": call.object_id, "unix": time.time(), "profile": PROFILE,
                                              "est": est, "app_id": ra.app_id, "launcher": "modal_parallel.py"}, indent=1))
                    spawned.append((f, call.object_id))
                    print(json.dumps({"spawned": f, "name": name, "call_id": call.object_id, "est_usd": est["usd"],
                                      "pess_usd": pess}), flush=True)
        led["launches"].append({"run_id": run_id, "unix": time.time(), "families": [f for f, _ in spawned],
                                "deferred": [f for f, _ in plan["deferred"]]})
    print(f"spawned {len(spawned)} pilot(s); the app keeps running without this process. Next: `watch` "
          f"(deferred: {[f for f, _ in plan['deferred']]})")
    return 0


# ---------------------------------------------------------------------------------------------------------------- watch, pull, stop
def stop_app(app_id: str) -> str:
    try:
        _sh(["app", "stop", "-y", app_id])
        return "stopped"
    except Exception as e:  # noqa: BLE001
        if "already stopped" in str(e).lower():          # a detached app stops itself when its last call finishes
            return "already stopped"
        return f"stop failed: {e!r}"[:200]


def app_state(app_id: str) -> str:
    for x in json.loads(_sh(["app", "list", "--json"])):
        if x["app_id"] == app_id:
            return f"{x['state']} tasks={x['tasks']}"
    return "not listed"


def pull_family(led_p: dict, fam: str, backups: Path) -> dict:
    """Result folder on the volume -> backups/modal_models/<name> (the path l4_reads.sh fetch uses). Skips files that exist."""
    v = modal.Volume.from_name(VOLUME)
    name = led_p["name"]
    dest = Path(backups) / name
    dest.mkdir(parents=True, exist_ok=True)
    got, errs = {}, []
    for f in led_p["files"]:
        target = dest / f
        if target.exists() and target.stat().st_size > 0:
            got[f] = "exists"
            continue
        last = None
        for attempt in range(6):                                   # a fresh commit can take a few seconds to be readable
            try:
                tmp = target.with_suffix(target.suffix + ".part")
                h = hashlib.sha256()
                with open(tmp, "wb") as fh:
                    for chunk in v.read_file(f"models/{name}/{f}"):
                        fh.write(chunk); h.update(chunk)
                os.replace(tmp, target)
                got[f] = h.hexdigest()
                break
            except Exception as e:  # noqa: BLE001
                last = e
                time.sleep(5)
        else:
            errs.append(f"{f}: {last!r}"[:200])
    res = {"dest": str(dest), "files": got, "errors": errs, "ok": not errs}
    exp = led_p.get("adapter_sha")
    if res["ok"] and exp and not led_p.get("smoke"):
        local = _sha256_file(dest / "adapter_model.safetensors")
        res["adapter_sha256"] = local
        res["adapter_sha_matches_container"] = local == exp
        res["ok"] = local == exp
    return res


def abort_all(root: Path, smoke: bool, why: str) -> None:
    rate = SMOKE_RATE_H if smoke else RATE_H
    with locked_ledger(root, smoke) as led:
        now = time.time()
        for fam, p in led["pilots"].items():
            if p["state"] in FINISHED:
                continue
            try:
                modal.FunctionCall.from_id(p["call_id"]).cancel(terminate_containers=True)
            except Exception as e:  # noqa: BLE001
                p["cancel_error"] = repr(e)[:120]
            p.update(state="cancelled", end_unix=now, usd=round(usd(pilot_elapsed_s(p, now), rate) if p.get("hb_start_unix") else 0.0, 4),
                     why=why)
        for x in led["apps"]:
            x["stop"] = stop_app(x["id"])
    print(f"ABORTED ({why}); apps stopped")


TERMINAL_ERRORS = tuple(getattr(modal.exception, n) for n in (
    "FunctionTimeoutError", "RemoteError", "ExecutionError", "InternalFailure", "OutputExpiredError", "ImageBuildError",
    "DeserializationError", "SandboxTerminatedError") if hasattr(modal.exception, n))
PERSIST_POLLS = 3              # an unknown error repeated this many polls in a row is taken as the pilot's own failure


def classify_poll_error(e: BaseException, he, prev: tuple | None) -> tuple:
    """-> (kind, key). kind: 'pending' (call not finished yet), 'terminal' (the pilot failed or was killed), 'transient'.
    Modal's builtin TimeoutError from get(timeout=) means pending; modal.exception.FunctionTimeoutError (the call hit its
    timeout) is terminal even though it is also a 'timeout'. A heartbeat 'failed' written by the container decides at once."""
    if isinstance(e, TimeoutError) and not isinstance(e, modal.exception.Error):
        return "pending", None
    if he and he.get("state") == "failed":
        return "terminal", None
    if isinstance(e, TERMINAL_ERRORS) or isinstance(e, modal.exception.InputCancellation):
        return "terminal", None
    key = (type(e).__name__, str(e)[:200])
    n = prev[1] + 1 if prev and prev[0] == key else 1
    return ("terminal" if n >= PERSIST_POLLS else "transient"), (key, n)


def poll_pilot(f: str, p: dict, hb, now: float, rate: float, smoke: bool) -> None:
    """Updates one unfinished ledger record in place from the heartbeats and the call's result."""
    kb = f"{p['run_id']}:{p['name']}"
    hs = he = None
    try:
        if hb is not None:
            hs = hb.get(f"{kb}:started")
            he = hb.get(f"{kb}:done") or hb.get(f"{kb}:failed")
    except Exception:  # noqa: BLE001
        pass
    if hs and not p.get("hb_start_unix"):
        p["hb_start_unix"] = hs["t"]
        p["state"] = "running"
    try:
        res = modal.FunctionCall.from_id(p["call_id"]).get(timeout=1)
    except BaseException as e:  # noqa: BLE001
        if isinstance(e, (KeyboardInterrupt, SystemExit)):
            raise
        kind, key = classify_poll_error(e, he, p.get("poll_err"))
        if kind == "pending":
            p.pop("poll_err", None)
            return
        if kind == "transient":
            p["poll_err"] = key
            print(f"[{time.strftime('%H:%M:%S')}] {f}: poll error {key[0][0]} ({key[1]}/{PERSIST_POLLS}), will retry", flush=True)
            return
        end = (he or {}).get("t", now)
        wall = (he or {}).get("wall_s")
        if wall is None and isinstance(e, getattr(modal.exception, "FunctionTimeoutError", ())):
            wall = p.get("timeout_s", TIMEOUT_S)
        p.update(state="failed", error=f"{type(e).__name__}: {e}"[:400], end_unix=end, wall_s=wall)
        p["usd"] = round(usd(wall + BOOT_S + SCALEDOWN_S, rate) if wall is not None
                         else usd(pilot_elapsed_s(p, end), rate) if p.get("hb_start_unix") else 0.0, 4)
        print(f"[{time.strftime('%H:%M:%S')}] {f} FAILED: {p['error'][:160]} ({p['usd']} USD)", flush=True)
        return
    meta = res.get("meta", {})
    p.update(state="done", end_unix=now, wall_s=round(res["wall_s"], 1), adapter_sha=res.get("adapter_sha", ""),
             gpu=res.get("gpu"), stopped=res.get("stopped"), steps=meta.get("steps"),
             train_minutes=meta.get("minutes"), env=meta.get("env"), init_sha=res.get("init_sha"))
    p["usd"] = round(usd(res["wall_s"] + BOOT_S + SCALEDOWN_S, rate), 4)
    if not smoke and res.get("stopped"):
        p["warning"] = "train() reported stopped=True: NOT a complete pass"
    print(f"[{time.strftime('%H:%M:%S')}] {f} done: wall {p['wall_s']} s, {p['usd']} USD, steps {p.get('steps')}", flush=True)


def cmd_watch(a) -> int:
    check_profile()
    root = Path(a.root)
    smoke = a.smoke
    try:
        hb = modal.Dict.from_name(HB_DICT)
    except Exception:  # noqa: BLE001
        hb = None
    exit_code = 0
    rate = SMOKE_RATE_H if smoke else RATE_H
    while True:
        now = time.time()
        with locked_ledger(root, smoke) as led:
            for f, p in [(f, p) for f, p in led["pilots"].items() if p["state"] not in FINISHED]:
                poll_pilot(f, p, hb, now, rate, smoke)
            obs = observed_usd(led, now)
            running = [p for p in led["pilots"].values() if p["state"] not in FINISHED]
            stop_at = hard_stop_at(len(running), a.poll + len(running) * 1.0)    # one cycle = sleep + 1 s per get()
            print(f"[{time.strftime('%H:%M:%S')}] observed {obs:.3f} USD of cap {CAP_USD}; running {len(running)}; "
                  f"done {sum(1 for p in led['pilots'].values() if p['state'] == 'done')}", flush=True)
            over = (not smoke) and obs >= stop_at
        if over:
            abort_all(root, smoke, f"hard stop: observed {obs:.3f} USD >= {stop_at:.3f}")
            return 3
        if not running:
            break
        time.sleep(a.poll)
    with locked_ledger(root, smoke) as led:
        pulls = {}
        if not a.no_pull:
            for f, p in led["pilots"].items():
                if p["state"] == "done" and not p.get("pulled"):
                    r = pull_family(p, f, Path(a.backups))
                    p["pulled"] = r["ok"]; p["pull"] = r
                    pulls[f] = r["ok"]
                    print(f"pulled {f}: {r['ok']} -> {r['dest']} {r['errors']}", flush=True)
                    if not r["ok"]:
                        exit_code = 1
        if not a.no_stop:
            for x in led["apps"]:
                if "stop" not in x:
                    x["stop"] = stop_app(x["id"])
                x["state_after"] = app_state(x["id"])
                print("app", x["id"], x["stop"], "->", x["state_after"], flush=True)
        failed = [f for f, p in led["pilots"].items() if p["state"] != "done"]
        led["summary"] = {"observed_usd": observed_usd(led), "cap_usd": CAP_USD, "failed": failed, "unix": time.time()}
        print(json.dumps(led["summary"]))
        smoke_total = round(sum(p.get("usd") or 0.0 for p in led["pilots"].values()), 4)
    if smoke:     # CPU stand-ins cost cents; they still count against the real cap
        with locked_ledger(root, False) as real:
            real["other_spend"].append({"what": f"smoke pilots {sorted(led['pilots'])} (CPU stand-ins at {SMOKE_RATE_H} USD/h)",
                                        "usd": smoke_total, "unix": time.time()})
    if not smoke:
        print("billing lags by minutes to hours: re-check with `modal billing report --for today --json` and enter the figure "
              "in the ledger notes")
    return exit_code or (1 if failed else 0)


def cmd_status(a) -> int:
    led = load_ledger(Path(a.root), a.smoke)
    now = time.time()
    print(json.dumps({"cap_usd": CAP_USD, "observed_usd": observed_usd(led, now), "committed_usd": committed_usd(led, now),
                      "other_spend": led["other_spend"], "apps": led["apps"],
                      "pilots": {f: {k: p.get(k) for k in ("state", "est_usd", "pess_usd", "usd", "wall_s", "pulled", "error", "warning")}
                                 for f, p in led["pilots"].items()}}, indent=1, default=float))
    return 0


def cmd_pull(a) -> int:
    check_profile()
    with locked_ledger(Path(a.root), a.smoke) as led:
        bad = 0
        for f, p in led["pilots"].items():
            if p["state"] == "done" and (a.force or not p.get("pulled")):
                r = pull_family(p, f, Path(a.backups))
                p["pulled"], p["pull"] = r["ok"], r
                print(f, r["ok"], r["dest"], r["errors"])
                bad += 0 if r["ok"] else 1
    return 1 if bad else 0


def cmd_abort(a) -> int:
    check_profile()
    abort_all(Path(a.root), a.smoke, "manual abort")
    return 0


def cmd_cleanup_smoke(a) -> int:
    """Removes the smoke result folders (models/_par_smoke_*) from the volume."""
    check_profile()
    v = modal.Volume.from_name(VOLUME)
    gone = []
    for e in v.listdir("models"):
        if Path(e.path).name.startswith("_par_smoke_"):
            v.remove_file(e.path, recursive=True)
            gone.append(e.path)
    print(json.dumps({"removed": gone}))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(HERE), help="folder holding stage/ configs/ par_runs/ (tests and the smoke use a temp one)")
    ap.add_argument("--backups", default=str(BACKUPS))
    ap.add_argument("--smoke", action="store_true", help="CPU stand-in pilots and the smoke ledger (cents)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("preflight", "prep-init", "estimate", "plan", "launch", "watch", "status", "pull", "abort", "cleanup-smoke"):
        p = sub.add_parser(n)
        if n in ("estimate", "plan", "launch"):
            p.add_argument("--families", default=",".join(FAMILIES))
            p.add_argument("--retry-failed", action="store_true")
        if n == "preflight":
            p.add_argument("--local-only", action="store_true")
        if n == "launch":
            p.add_argument("--go", action="store_true", help="actually spawn (the paid step)")
            p.add_argument("--strict", action="store_true", help="refuse unless every requested pilot fits")
            p.add_argument("--smoke-sleep", type=float, default=8.0)
        if n == "watch":
            p.add_argument("--poll", type=float, default=10.0)
            p.add_argument("--no-pull", action="store_true")
            p.add_argument("--no-stop", action="store_true")
        if n == "pull":
            p.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    for p in (a.root, a.backups):
        refuse_path(p)
    fn = {"preflight": cmd_preflight, "prep-init": cmd_prep_init, "estimate": cmd_estimate, "plan": cmd_plan,
          "launch": cmd_launch, "watch": cmd_watch, "status": cmd_status, "pull": cmd_pull, "abort": cmd_abort,
          "cleanup-smoke": cmd_cleanup_smoke}[a.cmd]
    try:
        return fn(a)
    except Refuse as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
