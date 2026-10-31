"""Modal launcher for ONE A42-D item 4 pilot: a short LoRA pass from C1 on one family's 1,500 new rows (no replay).

Own Modal app (modal_od.py is read-only here); the image is modal_od.image35's software (same PINNED35 pins) with a data mount
that holds ONLY the family's two staged files (pilot_ab/stage/<FAM>/), so no dev, eval or sealed file reaches the container.
Trainer = train_decoder.train, the code of C1's own run (hashes checked against C1's train_meta). No snapshots, no replay.

Run from lean/c2_build, with PILOT_FAMILY set (the image is built for that family's stage folder) and the free-credit profile:
  export PILOT_FAMILY=T40 MODAL_PROFILE=mahadikarya2 ; PY=../../.venv/bin/python -B ; M=../../.venv/bin/modal
  $PY pilot_ab/make_config.py --family T40 --rows <rows.jsonl> --rels <rels.jsonl>     # CPU: stage + config
  $M run pilot_ab/modal_pilot.py::pilot_check                 # CPU/volume read only: config, code, data, init adapter, cost
  $M run pilot_ab/modal_pilot.py::pilot_upload_init          # once per account; idempotent; only if pilot_check says missing
  $M run --detach pilot_ab/modal_pilot.py::pilot_spawn        # the paid step (one H100, about 6-8 min, about 0.4 USD)
Result: /vol/models/q35_4b_pab_<FAM> on that account (fetch with pilot_ab/l4_reads.sh fetch).
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.parent))   # lean/ (modal_od, train_decoder, ...)
import common as C  # noqa: E402
import modal  # noqa: E402
import modal_od  # noqa: E402  (read-only: PINNED35 and the account's secret name)

FAM = os.environ.get("PILOT_FAMILY", "")
STAGE = HERE / "stage" / (FAM or "_none")
TARGET_PROFILE = os.environ.get("PILOT_PROFILE", "mahadikarya2")   # A42-D 2.1: item 4 pilots count inside the 40 USD cap
BACKUP = Path(os.environ.get("C1_BACKUP", "/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k"))
INIT_FILES = ("adapter_config.json", "adapter_model.safetensors")
CODE_MODULES = ("train_decoder", "decoder_io", "prism_x", "writeblock")
MAX_USD = 1.0     # one pilot costs about 0.4; refuse a launch that the estimate puts above 1 USD

app = modal.App("opendecide-c2-pilot-ab")
vol = modal.Volume.from_name("opendecide", create_if_missing=True)
image = (
    modal.Image.debian_slim(python_version="3.12.10")
    .pip_install(*modal_od.PINNED35)
    .env({"HF_HOME": "/vol/hf", "HF_HUB_ENABLE_HF_TRANSFER": "1", "TOKENIZERS_PARALLELISM": "false",
          "TRITON_CACHE_DIR": "/vol/triton_cache"})
    .add_local_python_source("decoder_io", "train_decoder", "hc", "jevbench_od", "calc_tool", "writeblock", "prism_x",
                             "od_gcp", "shard_golden")
)
if STAGE.exists():   # the family's two staged files only (pilot_check refuses any other content)
    image = image.add_local_dir(STAGE, "/root/data")
SECRETS = [modal.Secret.from_name("opendecide-keys")]


@app.function(image=image, gpu="H100!", volumes={"/vol": vol}, secrets=SECRETS, timeout=2 * 3600)
def train_pilot(name: str, cfg: dict) -> dict:
    """One uninterrupted pass (about 94 steps). Refuses to start unless the init adapter on the volume is C1 (sha256)."""
    import hashlib
    h = hashlib.sha256()
    with open(f"{cfg['init_adapter']}/adapter_model.safetensors", "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    if h.hexdigest() != C.C1_ADAPTER_SHA:
        raise RuntimeError(f"init adapter sha256 {h.hexdigest()[:12]} is not C1's {C.C1_ADAPTER_SHA[:12]}")
    import decoder_io
    decoder_io.STYLE = cfg.get("style", "od")
    import train_decoder
    res = train_decoder.train(cfg, Path("/root/data"), Path(f"/vol/models/{name}"), on_ckpt=vol.commit)
    vol.commit()
    return {"stopped": bool(res.get("stopped")), "meta": res["meta"]}


# ------------------------------------------------------------------ local side (laptop; no GPU) ---------------------------
def _cfg_for_run(expect_resume=False, log_every=0):
    if not FAM:
        raise SystemExit("set PILOT_FAMILY (e.g. export PILOT_FAMILY=T40) before `modal run`: the image mounts that stage folder")
    raw = json.loads((HERE / "configs" / f"{FAM}.json").read_text())
    missing = [k for k in modal_od.RELAY_REQUIRED + ("init_adapter", "expect_kd_targets", "expect_kd_full",
                                                      "expect_trainable", "expect_ord_rows") if k not in raw]
    if missing:
        raise SystemExit(f"configs/{FAM}.json: missing keys {missing}")
    cfg = dict(raw)
    name = cfg.pop("name")
    if name != C.pilot_name(FAM) or cfg["seed"] != C.SEED or cfg["init_adapter"] != C.C1_INIT_VOL:
        raise SystemExit("config name / seed / init_adapter differ from A42-D 4.1")
    if cfg["targets"] == "QWEN35":
        cfg["targets"] = modal_od.QWEN35_TARGETS
    cfg.update({"no_overwrite": True, "expect_resume": expect_resume, "stop_at_step": 0, "stop_at_unix": 0})
    if log_every > 0:
        cfg["log_every"] = log_every
    return name, cfg


def _local_checks(profile_ok_only=False) -> dict:
    prof = os.environ.get("MODAL_PROFILE", "")
    if prof != TARGET_PROFILE:
        raise SystemExit(f"MODAL_PROFILE is {prof!r}, not {TARGET_PROFILE!r} (pilot spend goes on that free credit; "
                         "set PILOT_PROFILE only with the owner's say-so)")
    name, cfg = _cfg_for_run()
    info = json.loads((HERE / "configs" / f"{FAM}.stage.json").read_text())
    files = sorted(p.name for p in STAGE.iterdir())
    if files != sorted((C.TRAIN_FILE, C.REL_FILE)):
        raise SystemExit(f"stage folder holds {files}, expected exactly the two staged files")
    for f, key in ((C.TRAIN_FILE, "train_sha256"), (C.REL_FILE, "rel_sha256")):
        if C.sha256_file(STAGE / f) != info[key]:
            raise SystemExit(f"{f} changed since make_config (sha256 differs); rerun make_config")
    meta = json.loads((BACKUP / "train_meta.json").read_text())
    now = {m: C.sha256_file(C.LEAN / f"{m}.py") for m in CODE_MODULES}
    if meta.get("code") != now:
        raise SystemExit(f"trainer code differs from C1's train_meta code hashes: {meta.get('code')} vs {now}")
    from_est = info["est_h100"]
    if from_est["usd"] > MAX_USD:
        raise SystemExit(f"estimated {from_est['usd']} USD > {MAX_USD}")
    return {"family": FAM, "profile": prof, "steps": info["steps"], "est": from_est, "code_sha": now}


def _volume_init_check() -> dict:
    import hashlib
    got = {}
    for f in INIT_FILES:
        h = hashlib.sha256()
        try:
            for chunk in vol.read_file(f"models/{C.C1_INIT_VOL.rsplit('/', 1)[1]}/{f}"):
                h.update(chunk)
        except Exception as e:  # noqa: BLE001
            raise SystemExit(f"{C.C1_INIT_VOL}/{f} is not on this account's volume ({e!r}); run pilot_upload_init")
        got[f] = h.hexdigest()
    if got["adapter_model.safetensors"] != C.C1_ADAPTER_SHA:
        raise SystemExit(f"volume init adapter sha256 {got['adapter_model.safetensors'][:12]} is not C1's")
    return got


@app.local_entrypoint()
def pilot_check():
    """Everything that can be checked without a GPU: config, staged files, trainer code, init adapter on the volume, cost."""
    out = _local_checks()
    out["volume_init"] = _volume_init_check()
    print(json.dumps(out, indent=1))


@app.local_entrypoint()
def pilot_upload_init():
    """Copy C1's adapter (local backup, sha256-checked) to models/q35_4b_main500k_init on this account's volume."""
    prof = os.environ.get("MODAL_PROFILE", "")
    if prof != TARGET_PROFILE:
        raise SystemExit(f"MODAL_PROFILE is {prof!r}, not {TARGET_PROFILE!r}")
    if C.sha256_file(BACKUP / "adapter_model.safetensors") != C.C1_ADAPTER_SHA:
        raise SystemExit(f"{BACKUP}/adapter_model.safetensors is not C1 (sha256)")
    dst = "models/" + C.C1_INIT_VOL.rsplit("/", 1)[1]
    try:
        if _volume_init_check():
            print("init adapter already on the volume; left alone")
            return
    except SystemExit:
        pass
    with vol.batch_upload(force=True) as up:
        for f in INIT_FILES:
            up.put_file(str(BACKUP / f), f"{dst}/{f}")
    print(json.dumps({"uploaded": _volume_init_check()}))


@app.local_entrypoint()
def pilot_spawn(expect_resume: bool = False):
    """The paid step: spawn train_pilot on one H100 and exit (the run continues without the laptop)."""
    chk = _local_checks()
    _volume_init_check()
    name, cfg = _cfg_for_run(expect_resume=expect_resume)
    print(json.dumps({"spawning": name, "est": chk["est"]}), flush=True)
    call = train_pilot.spawn(name, cfg)
    (HERE / "configs" / f"{FAM}.spawned.json").write_text(json.dumps(
        {"name": name, "call_id": call.object_id, "unix": time.time(), "profile": chk["profile"], "est": chk["est"]}, indent=1))
    print(json.dumps({"call_id": call.object_id, "result_at": f"/vol/models/{name}"}))
