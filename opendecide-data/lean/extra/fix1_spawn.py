"""Launch the 4B top-up q35_4b_main500k_fix1 (runs/q35_4b_fix1.json; yn2b/SPEC.md 14; draft amendment A8) as ONE
spawned segment on ONE Modal account. Same pattern as extra/relay_spawn.py: the local entrypoint .spawn()s
modal_od.train_relay35 and exits, so the run keeps going if the laptop goes offline.

modal_od.py is NOT edited. Its image uploads data/v14_parts/ files only when they are in modal_od.V14_KEEP, which
_data_ignore() reads when `modal run` collects the data mount (after this module is imported). This module sets that
set, in memory only, to the two fix1 files: the run reads nothing else from v14_parts, so the golden_train,
golden_dev and train_2b_golden_kd copies (about 2.7 GB) are not uploaded to the account. Only an image built by THIS
launcher is affected; every other launch from this checkout is unchanged. The training code is the frozen code of the main run (train_decoder / decoder_io / prism_x /
writeblock sha256 = the main run's train_meta "code"; train() records and checks it).

The init adapter is C1 (q35_4b_main500k), uploaded once per account to models/q35_4b_main500k_init (its own folder,
so a relay folder of the main run on that account can never be picked up by mistake). The launcher refuses to spawn
unless the volume's copy has the sha256 of the gate's C1 (gate/manifest_adapters.sha256).

Run from lean/ (one account; jaypatil-duke first, mahadikarya2 as fallback):
  B=/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k; P=jaypatil-duke
  MODAL_PROFILE=$P ../.venv/bin/modal volume put opendecide $B/adapter_config.json models/q35_4b_main500k_init/adapter_config.json
  MODAL_PROFILE=$P ../.venv/bin/modal volume put opendecide $B/adapter_model.safetensors models/q35_4b_main500k_init/adapter_model.safetensors
  MODAL_PROFILE=$P ../.venv/bin/modal run --detach extra/fix1_spawn.py::fix1_spawn --stop-after-min 240
  (after a planned stop or a lost input:) ... ::fix1_spawn --expect-resume --stop-after-min 240
Logs: MODAL_PROFILE=$P ../.venv/bin/modal app logs <app id>. Result: /vol/models/q35_4b_main500k_fix1 on that account.
"""
import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import modal_od  # noqa: E402
from modal_od import app, train_relay35, vol, HERE, RELAY_REQUIRED, QWEN35_TARGETS  # noqa: E402

CONFIG = "runs/q35_4b_fix1.json"
NAME = "q35_4b_main500k_fix1"
FIX1_FILES = ("fix1_train.jsonl", "fix1_relations.jsonl")
COUNTS = HERE / "data/v14_parts/fix1_counts.json"
INIT_NAME = "q35_4b_main500k_init"
INIT_DIR = f"/vol/models/{INIT_NAME}"
GATE_MANIFEST = HERE / "gate/manifest_adapters.sha256"
INIT_FILES = ("adapter_config.json", "adapter_model.safetensors")

modal_od.V14_KEEP.clear()  # in memory only (see the docstring): train() reads only cfg train_file / rel_file
modal_od.V14_KEEP.update(FIX1_FILES)


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
    return {f: man[f"models/q35_4b_main500k/{f}"] for f in INIT_FILES}


def build_cfg(config=CONFIG, expect_resume=False, stop_after_min=0.0, stop_at_step=0, log_every=0, now=None):
    """(name, cfg) exactly as modal_od.relay / extra/relay_spawn build it, plus the fix1 identity checks."""
    cfg = json.loads((HERE / config).read_text())
    missing = [k for k in RELAY_REQUIRED + ("init_adapter",) if k not in cfg]
    if missing:
        raise SystemExit(f"{config}: missing keys {missing} (every key must be written out)")
    name = cfg.pop("name")
    if name != NAME:
        raise SystemExit(f"{config}: name {name!r} is not {NAME!r}")
    if cfg["init_adapter"] != INIT_DIR:
        raise SystemExit(f"{config}: init_adapter {cfg['init_adapter']!r} is not {INIT_DIR!r}")
    if [Path(cfg["train_file"]).name, Path(cfg["rel_file"]).name] != list(FIX1_FILES):
        raise SystemExit(f"{config}: train_file / rel_file are not the fix1 files")
    if cfg["targets"] == "QWEN35":
        cfg["targets"] = QWEN35_TARGETS
    t = time.time() if now is None else now
    # an absolute end time: a Modal restart after a preemption keeps it (a relative stop_after_min would start over)
    cfg.update({"no_overwrite": True, "expect_resume": expect_resume, "stop_at_step": stop_at_step,
                "stop_at_unix": t + 60 * stop_after_min if stop_after_min > 0 else 0})
    if log_every > 0:
        cfg["log_every"] = log_every
    return name, cfg


def local_checks(cfg) -> dict:
    """The data files are the built ones (sha256 = fix1_counts.json) and the image's data mount will carry them."""
    counts = json.loads(COUNTS.read_text())
    out = {}
    for f in (cfg["train_file"], cfg["rel_file"]):
        p = HERE / "data" / f
        got, want = sha256_file(p), counts["files"].get(f)
        if got != want:
            raise SystemExit(f"data/{f}: sha256 {got[:12]}... is not the built {str(want)[:12]}... (fix1_counts.json)")
        if modal_od._data_ignore(Path(f)):
            raise SystemExit(f"data/{f} would not be uploaded (V14_KEEP patch missing?)")
        out[f] = got
    for k, n in (("expect_kd_targets", counts["kd_targets"]), ("expect_kd_full", counts["kd_full"])):
        if cfg.get(k) != n:
            raise SystemExit(f"{CONFIG}: {k} {cfg.get(k)} is not the built file's {n}")
    return out


def volume_init_check() -> dict:
    """The init adapter on this account's volume is byte-identical to C1 (read through the client, no container)."""
    want, got = c1_sha(), {}
    for f in INIT_FILES:
        h = hashlib.sha256()
        try:
            for chunk in vol.read_file(f"models/{INIT_NAME}/{f}"):
                h.update(chunk)
        except Exception as e:  # noqa: BLE001
            raise SystemExit(f"models/{INIT_NAME}/{f} is not on this account's volume ({e!r}); upload it first "
                             "(see the docstring)")
        got[f] = h.hexdigest()
        if got[f] != want[f]:
            raise SystemExit(f"models/{INIT_NAME}/{f}: sha256 {got[f][:12]}... is not C1's {want[f][:12]}...")
    return got


@app.local_entrypoint()
def fix1_spawn(expect_resume: bool = False, stop_after_min: float = 0.0, stop_at_step: int = 0, log_every: int = 0):
    name, cfg = build_cfg(CONFIG, expect_resume, stop_after_min, stop_at_step, log_every)
    data = local_checks(cfg)
    init = volume_init_check()
    if not (stop_after_min > 0 or stop_at_step > 0):
        print("note: no stop point set; this segment runs to the end (or until the account's credit runs out)")
    fc = train_relay35.spawn(name, cfg)
    print(json.dumps({"spawned_call": fc.object_id, "name": name, "expect_resume": expect_resume,
                      "stop_at_unix": cfg["stop_at_unix"], "data_sha256": data, "init_sha256": init}), flush=True)
