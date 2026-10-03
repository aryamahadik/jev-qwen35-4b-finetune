"""Launch the 4B top-up q35_4b_main500k_fix2 (candidate C4; runs/q35_4b_fix2.json; draft amendment A8-prime, section B)
as ONE spawned segment on ONE Modal account. Same pattern as extra/relay_spawn.py / extra/fix1_spawn.py: the local
entrypoint .spawn()s modal_od.train_relay35 and exits, so the run keeps going if the laptop loses its network (1 Oct,
13:16 UTC: a .remote() input was cancelled that way).

modal_od.py is NOT edited (it is a frozen file). Two in-memory changes, made only in the process that runs THIS file:
  1. The image's data mount carries ONLY data/v14_parts/fix2_train.jsonl and fix2_relations.jsonl. The mount's ignore
     callable is the function object modal_od._data_ignore; its __code__ is swapped for _fix2_data_ignore below, so
     every other file of data/ (dev, eval, OHS-1/2/3, the F7 probe and devx, golden_train ...) is never uploaded to
     this run's container. The launcher lists the mount's files with Modal's own walker (_MountDir.get_files_to_upload)
     and refuses to spawn unless the list is exactly those two files.
  2. Nothing else: train_relay35 runs train_decoder.train() with the frozen code of the main run (the sha256 of
     train_decoder / decoder_io / prism_x / writeblock must equal C1's train_meta "code"; checked here, and train()
     records its own).

The init adapter is C1 (q35_4b_main500k, adapter_model.safetensors sha256 507d1c29...), in its own volume folder
models/q35_4b_main500k_init. `fix2_upload_init` uploads it from the one local backup and re-reads it through the client;
`fix2_spawn` refuses to spawn unless the volume copy has C1's sha256 (gate/manifest_adapters.sha256).

Run from lean/ on the Mac, account jaypatil-duke (A8-prime B; checked Oct credit $30.00 at 23:40 UTC 1 Oct):
  P=jaypatil-duke
  MODAL_PROFILE=$P ../.venv/bin/modal run extra/fix2_spawn.py::fix2_upload_init        # once; idempotent
  MODAL_PROFILE=$P ../.venv/bin/modal run --detach extra/fix2_spawn.py::fix2_spawn       # one segment, to the end
  (after a preemption Modal restarts the input itself and train() resumes from its checkpoint; after a lost input:)
  MODAL_PROFILE=$P ../.venv/bin/modal run --detach extra/fix2_spawn.py::fix2_spawn --expect-resume
Logs: MODAL_PROFILE=$P ../.venv/bin/modal app logs <app id>. Result: /vol/models/q35_4b_main500k_fix2 on that account;
fetch it with `bash gate/gate_4b_fix2_l4.sh fetch jaypatil-duke`.

The CPU dry run (no Modal call at all) is extra/fix2_dryrun.py; it imports this file and runs every local check.
"""
import hashlib
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import modal_od  # noqa: E402
from modal_od import app, train_relay35, vol, HERE, RELAY_REQUIRED, QWEN35_TARGETS  # noqa: E402

CONFIG = "runs/q35_4b_fix2.json"
MAIN_CONFIG = "runs/q35_4b_main.json"
NAME = "q35_4b_main500k_fix2"
FIX2_FILES = ("fix2_train.jsonl", "fix2_relations.jsonl")
COUNTS = HERE / "data/v14_parts/fix2_counts.json"
INIT_NAME = "q35_4b_main500k_init"
INIT_DIR = f"/vol/models/{INIT_NAME}"
GATE_MANIFEST = HERE / "gate/manifest_adapters.sha256"
INIT_FILES = ("adapter_config.json", "adapter_model.safetensors")
C1_ADAPTER_SHA = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"  # A8-prime B (the gated C1 read)
BACKUP = Path(os.environ.get("C1_BACKUP", "/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k"))
TARGET_PROFILE = "jaypatil-duke"
CODE_MODULES = ("train_decoder", "decoder_io", "prism_x", "writeblock")
# keys that must equal the main run's (the top-up continues the same model with the same loss); every other key of the
# fix2 config may differ only as listed in ALLOWED_DIFF (A8-prime B "New")
SAME_AS_MAIN = ("base", "base_revision", "recipe", "batch", "r", "alpha", "dropout", "lam", "beta", "kd", "kd_skip_src",
                "kd_full_src", "lam_inv", "sym_cons", "perm_twin", "lam_p", "aux_norm", "grad_ckpt", "style", "layout",
                "micro_tokens", "targets", "expect_trainable", "ckpt_every_min")
ALLOWED_DIFF = {"name", "train_file", "rel_file", "init_adapter", "epochs", "lr", "seed", "snap_every", "snap_fracs",
                "expect_kd_targets", "expect_kd_full", "log_every"}
# cost model (A8-prime B): the main run's measured step time on the H100 (logs/main4b_seg1-5.log: 30,450 steps in
# 1,380.58 min = 2.720 s/step) scaled by the fix2 / golden padded-token ratio (extra/fix2_dryrun.py), at the measured
# all-in rate of $4.09/h (H100 $3.95/h + CPU/memory; logs/budget_ledger.md), plus a fixed start-up allowance
STEP_S_MAIN, RATE_PER_H, STARTUP_MIN = 2.720, 4.09, 12.0

_FIX2_MOUNT = frozenset(f"v14_parts/{f}" for f in FIX2_FILES)


def _fix2_data_ignore(p):
    """Replacement body of modal_od._data_ignore (code swap, this process only): ignore every file of data/ except the
    two fix2 files. Globals resolve in modal_od's namespace (Path, _FIX2_MOUNT)."""
    return Path(p).as_posix() not in _FIX2_MOUNT


modal_od._FIX2_MOUNT = _FIX2_MOUNT
modal_od._data_ignore.__code__ = _fix2_data_ignore.__code__


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def c1_sha() -> dict:
    """sha256 of C1's adapter files as the gate read them (gate/manifest_adapters.sha256)."""
    man = {}
    for line in GATE_MANIFEST.read_text().splitlines():
        if line.strip():
            sha, path = line.split(maxsplit=1)
            man[path.strip()] = sha
    out = {f: man[f"models/q35_4b_main500k/{f}"] for f in INIT_FILES}
    if out["adapter_model.safetensors"] != C1_ADAPTER_SHA:
        raise SystemExit("gate/manifest_adapters.sha256 does not hold the pinned C1 adapter sha256")
    return out


def build_cfg(config=CONFIG, expect_resume=False, stop_after_min=0.0, stop_at_step=0, log_every=0, now=None):
    """(name, cfg) exactly as modal_od.relay / extra/relay_spawn build it, plus the fix2 identity checks."""
    raw = json.loads((HERE / config).read_text())
    cfg = dict(raw)
    missing = [k for k in RELAY_REQUIRED + ("init_adapter", "expect_kd_targets", "expect_kd_full", "expect_trainable")
               if k not in cfg]
    if missing:
        raise SystemExit(f"{config}: missing keys {missing} (every key must be written out)")
    main = json.loads((HERE / MAIN_CONFIG).read_text())
    bad = [k for k in SAME_AS_MAIN if main.get(k) != raw.get(k)]
    if bad:
        raise SystemExit(f"{config}: keys that must equal the main run's differ: {bad}")
    extra = sorted(k for k in set(raw) | set(main) if raw.get(k) != main.get(k) and k not in ALLOWED_DIFF)
    if extra:
        raise SystemExit(f"{config}: keys differ from the main run beyond A8-prime B: {extra}")
    name = cfg.pop("name")
    if name != NAME:
        raise SystemExit(f"{config}: name {name!r} is not {NAME!r}")
    if cfg["init_adapter"] != INIT_DIR:
        raise SystemExit(f"{config}: init_adapter {cfg['init_adapter']!r} is not {INIT_DIR!r}")
    if [Path(cfg["train_file"]).name, Path(cfg["rel_file"]).name] != list(FIX2_FILES):
        raise SystemExit(f"{config}: train_file / rel_file are not the fix2 files")
    if cfg["snap_every"] or cfg["snap_fracs"]:
        raise SystemExit(f"{config}: snapshots are not allowed (A8-prime B: no dev-selected weights)")
    if cfg["targets"] == "QWEN35":
        cfg["targets"] = QWEN35_TARGETS
    t = time.time() if now is None else now
    # an absolute end time: a Modal restart after a preemption keeps it (a relative stop_after_min would start over)
    cfg.update({"no_overwrite": True, "expect_resume": expect_resume, "stop_at_step": stop_at_step,
                "stop_at_unix": t + 60 * stop_after_min if stop_after_min > 0 else 0})
    if log_every > 0:
        cfg["log_every"] = log_every
    return name, cfg


def frozen_code_check() -> dict:
    """The trainer code that will run equals the main run's (C1's train_meta "code")."""
    meta = json.loads((BACKUP / "train_meta.json").read_text())
    now = {m: sha256_file(HERE / f"{m}.py") for m in CODE_MODULES}
    if meta.get("code") != now:
        raise SystemExit(f"frozen code differs from the main run's: {meta.get('code')} vs {now}")
    return now


def data_mount_files() -> list:
    """The files Modal will upload for image35's data mount, listed with Modal's own walker (relative to data/)."""
    from modal._utils.async_utils import synchronizer
    raw = synchronizer._translate_in(modal_od.image35)
    ents, todo = [], [raw]
    while todo:
        x = todo.pop()
        for d in x._deps():
            if type(d).__name__ == "_Mount":
                ents += [e for e in d.entries if type(e).__name__ == "_MountDir"]
            else:
                todo.append(d)
    data = [e for e in ents if Path(e.local_dir).resolve() == (HERE / "data").resolve()]
    if len(data) != 1:
        raise SystemExit(f"expected one data mount on image35, found {len(data)}")
    if data[0].ignore is not modal_od._data_ignore:
        raise SystemExit("image35's data mount does not use modal_od._data_ignore (the code swap would not apply)")
    out = sorted(str(Path(mp).relative_to("/root/data")) for _, mp in data[0].get_files_to_upload())
    return out


def local_checks(cfg) -> dict:
    """Data = the built files (sha256 = fix2_counts.json); kd guards = the built counts; one pass; the data mount holds
    exactly the two files; frozen code."""
    import replay_steps as rs
    counts = json.loads(COUNTS.read_text())
    out = {}
    for f in (cfg["train_file"], cfg["rel_file"]):
        got, want = sha256_file(HERE / "data" / f), counts["files"].get(f)
        if got != want:
            raise SystemExit(f"data/{f}: sha256 {got[:12]}... is not the built {str(want)[:12]}... (fix2_counts.json)")
        out[f] = got
    for k, n in (("expect_kd_targets", counts["kd_targets"]), ("expect_kd_full", counts["kd_full"])):
        if cfg.get(k) != n:
            raise SystemExit(f"{CONFIG}: {k} {cfg.get(k)} is not the built file's {n}")
    import tempfile
    with tempfile.TemporaryDirectory() as td_:
        rep = rs.main(["--config", CONFIG, "--out", str(Path(td_) / "replay.json")])
    if not rep.get("config_is_one_pass"):
        raise SystemExit(f"epochs {cfg['epochs']} is not one pass: {rep.get('config_n_steps')} steps vs a pass of "
                         f"{rep['pass_batches']} batches (set epochs to {rep['epochs']!r})")
    mount = data_mount_files()
    if mount != sorted(f"v14_parts/{f}" for f in FIX2_FILES):
        raise SystemExit(f"the image's data mount would carry {len(mount)} files ({mount[:5]} ...), not only fix2")
    return {"data_sha256": out, "steps": rep["config_n_steps"], "warmup_steps": rep["warmup_steps"],
            "data_mount": mount, "code": frozen_code_check()}


def cost(steps: int, step_s: float = STEP_S_MAIN) -> dict:
    h = (steps * step_s / 60 + STARTUP_MIN) / 60
    return {"steps": steps, "step_s": round(step_s, 3), "hours": round(h, 2), "usd": round(h * RATE_PER_H, 2),
            "rate_per_h": RATE_PER_H, "startup_min": STARTUP_MIN}


def volume_init_check() -> dict:
    """The init adapter on this account's volume is byte-identical to C1 (read through the client, no container)."""
    want, got = c1_sha(), {}
    for f in INIT_FILES:
        h = hashlib.sha256()
        try:
            for chunk in vol.read_file(f"models/{INIT_NAME}/{f}"):
                h.update(chunk)
        except Exception as e:  # noqa: BLE001
            raise SystemExit(f"models/{INIT_NAME}/{f} is not on this account's volume ({e!r}); run fix2_upload_init")
        got[f] = h.hexdigest()
        if got[f] != want[f]:
            raise SystemExit(f"models/{INIT_NAME}/{f}: sha256 {got[f][:12]}... is not C1's {want[f][:12]}...")
    return got


def profile_check(allow_other: bool):
    prof = os.environ.get("MODAL_PROFILE", "")
    if prof != TARGET_PROFILE and not allow_other:
        raise SystemExit(f"MODAL_PROFILE is {prof!r}, not {TARGET_PROFILE!r} (A8-prime B; --allow-other-profile only "
                         "with the owner's say-so)")
    return prof


@app.local_entrypoint()
def fix2_upload_init(allow_other_profile: bool = False):
    """Put C1's adapter (the local backup, sha256-checked against the gate manifest) into models/q35_4b_main500k_init
    on this account's volume, then re-read it through the client. Idempotent: a matching copy is left alone."""
    profile_check(allow_other_profile)
    want = c1_sha()
    for f in INIT_FILES:
        if sha256_file(BACKUP / f) != want[f]:
            raise SystemExit(f"local backup {BACKUP / f} does not match C1's sha256")
    try:
        print(json.dumps({"already_on_volume": volume_init_check()}))
        return
    except SystemExit as e:
        print(f"uploading C1 to models/{INIT_NAME} ({e})")
    with vol.batch_upload(force=True) as batch:
        for f in INIT_FILES:
            batch.put_file(str(BACKUP / f), f"models/{INIT_NAME}/{f}")
    print(json.dumps({"uploaded_and_verified": volume_init_check()}))


@app.local_entrypoint()
def fix2_spawn(expect_resume: bool = False, stop_after_min: float = 0.0, stop_at_step: int = 0, log_every: int = 0,
               allow_other_profile: bool = False):
    prof = profile_check(allow_other_profile)
    name, cfg = build_cfg(CONFIG, expect_resume, stop_after_min, stop_at_step, log_every)
    loc = local_checks(cfg)
    init = volume_init_check()
    dry = HERE / "extra/fix2_dryrun.json"
    step_s = json.loads(dry.read_text())["speed"]["step_s_estimate"] if dry.exists() else STEP_S_MAIN
    est = cost(loc["steps"], step_s)
    if not (stop_after_min > 0 or stop_at_step > 0):
        print("note: no stop point set; this segment runs to the end (one pass)")
    fc = train_relay35.spawn(name, cfg)
    print(json.dumps({"spawned_call": fc.object_id, "name": name, "profile": prof, "expect_resume": expect_resume,
                      "stop_at_unix": cfg["stop_at_unix"], **loc, "init_sha256": init, "cost_estimate": est}), flush=True)
