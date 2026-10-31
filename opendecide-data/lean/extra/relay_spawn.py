"""Launch a relay segment with .spawn() so the run keeps going even if this laptop goes offline.

Why: on 1 Oct at 13:16 UTC the laptop lost its network. `modal run --detach modal_od.py::relay` uses .remote(), and
Modal cancelled the input, so segment 4 was killed; its signal save at step 25682 survived. Here the local entrypoint
spawns the function call and exits, so the call no longer depends on the client.

The config logic is copied exactly from modal_od.relay, so the run identity is identical (the resume checks enforce
this anyway). Run from lean/:
  MODAL_PROFILE=<acct> ../.venv/bin/modal run --detach extra/relay_spawn.py::relay_spawn --config runs/q35_4b_main.json \
      --expect-resume [--stop-after-min M]
Then stream the logs with `modal app logs <app id>`. The result is the checkpoint and adapter on the volume."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modal_od import app, train_relay35, HERE, RELAY_REQUIRED, QWEN35_TARGETS  # noqa: E402


@app.local_entrypoint()
def relay_spawn(config: str, expect_resume: bool = False, stop_after_min: float = 0.0, stop_at_step: int = 0,
                log_every: int = 0):
    cfg = json.loads((HERE / config).read_text())
    missing = [k for k in RELAY_REQUIRED if k not in cfg]
    if missing:
        raise SystemExit(f"{config}: missing keys {missing} (every key must be written out)")
    name = cfg.pop("name")
    if cfg["targets"] == "QWEN35":
        cfg["targets"] = QWEN35_TARGETS
    cfg.update({"no_overwrite": True, "expect_resume": expect_resume, "stop_at_step": stop_at_step,
                "stop_at_unix": time.time() + 60 * stop_after_min if stop_after_min > 0 else 0})
    if log_every > 0:
        cfg["log_every"] = log_every
    if not (stop_after_min > 0 or stop_at_step > 0):
        print("note: no stop point set; this segment runs to the end (or until the account's credit runs out)")
    fc = train_relay35.spawn(name, cfg)
    print(json.dumps({"spawned_call": fc.object_id, "name": name, "expect_resume": expect_resume,
                      "stop_at_unix": cfg["stop_at_unix"]}), flush=True)
