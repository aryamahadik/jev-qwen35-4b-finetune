"""C round-1 G9 crowd read on a Modal H100 (PREREG A17: owner GO ~$15; 1 view per read; C1 + 4B-E + base 4B).

Written by the mixer builder; NOT run by any agent (paid step). The commands are in c_build/crowd_r1/CROWD_READ_r1.sh.
Its own app and image: the same pinned Qwen3.5 package set as modal_od.image35 (read from modal_od.py by ast, so the
pinned launcher modal_od.py is unchanged and nothing under bench/ is uploaded). Only the od_gcp label path is used
(L4-verified): every shard of crowd_r1_shards/<FAM> on the Volume is labelled once, given option order, no TTA
(no --tta flags, no --perm-seed), merged adapter, bf16; the Volume is committed after every shard (resumable).

  modal run --detach c_build/modal_crowd.py::crowd --name q35_4b_main500k --fams F1,F2,F3 --max-min <CAP_MIN>

SERVER-SIDE TIME CAP (required; endgame/crowd_cap.py computes it from the credit left): --max-min sets this call's
function timeout (crowd_read.with_options(timeout=...)) AND an absolute deadline (launch time + max_min) that the
container checks at start, after every shard commit, and with a watchdog thread. A Modal restart after a preemption
gets a fresh timeout but keeps the absolute deadline, so a container never runs past launch + max_min, whatever the Mac
does. Finished shards are committed, so a relaunch resumes.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

import modal

LEAN = Path(__file__).resolve().parent.parent


def _pinned35() -> list[str]:
    if not modal.is_local():  # inside the container the source tree is absent; the image is already built
        return []
    tree = ast.parse((LEAN / "modal_od.py").read_text())
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", None) == "PINNED35" for t in n.targets):
            v = n.value.func.value if isinstance(n.value, ast.Call) else n.value
            return ast.literal_eval(v).split()
    raise SystemExit("PINNED35 not found in modal_od.py")


app = modal.App("opendecide-crowd")
vol = modal.Volume.from_name("opendecide", create_if_missing=False)
image = (
    modal.Image.debian_slim(python_version="3.12.10")
    .pip_install(*_pinned35())
    .env({"HF_HOME": "/vol/hf", "HF_HUB_ENABLE_HF_TRANSFER": "1", "TOKENIZERS_PARALLELISM": "false",
          "TRITON_CACHE_DIR": "/vol/triton_cache"})
    .add_local_file(LEAN / "decoder_io.py", "/root/decoder_io.py")
    .add_local_file(LEAN / "prism_x.py", "/root/prism_x.py")
    .add_local_file(LEAN / "od_gcp.py", "/root/od_gcp.py")
    .add_local_file(LEAN / "shard_golden.py", "/root/shard_golden.py")
    .add_local_file(LEAN / "writeblock.py", "/root/writeblock.py")
)
BASE, REVISION, LAYOUT = "Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a", "schema_branch_mark"
CROWD_NAMES = ("q35_4b_main500k", "q35_4b_pxE", "q35_4b_base0")


class _Deadline(BaseException):   # BaseException: an `except Exception` inside od_gcp cannot swallow it
    pass


@app.function(image=image, gpu="H100!", volumes={"/vol": vol}, timeout=12 * 3600)
def crowd_read(name: str, fams: list, deadline_unix: float = 0.0) -> dict:
    import os
    import sys
    import threading
    import time
    sys.path.insert(0, "/root")
    if not deadline_unix:
        raise SystemExit("no deadline: launch with --max-min (endgame/crowd_cap.py)")
    if time.time() >= deadline_unix:            # a restart after the cap: do nothing
        return {"status": "deadline_passed_before_start"}
    # hard stop at the deadline even inside a shard (the shard in progress is lost; finished shards are committed)
    timer = threading.Timer(max(1.0, deadline_unix - time.time()), lambda: os._exit(3))
    timer.daemon = True
    timer.start()
    try:
        return _crowd_read(name, fams, deadline_unix)
    finally:
        timer.cancel()


def _crowd_read(name: str, fams: list, deadline_unix: float) -> dict:
    import time
    import od_gcp
    import shard_golden as sg
    if name not in CROWD_NAMES:
        raise SystemExit(f"{name}: not a crowd model {CROWD_NAMES}")
    od_gcp.MODELS = Path("/vol/models")
    write = sg.write_json_atomic

    def write_and_commit(path, obj):  # a shard's meta is written last: commit then (durable, resumable)
        write(path, obj)
        vol.commit()
        if time.time() >= deadline_unix - 60:   # between shards: stop cleanly before the cap
            raise _Deadline()
    sg.write_json_atomic = write_and_commit
    done = {}
    for fam in fams:
        if time.time() >= deadline_unix - 60:
            done["status"] = "deadline"
            break
        sd = Path("/vol/crowd_r1_shards") / fam
        if not (sd / sg.MANIFEST).exists():
            raise SystemExit(f"{sd}: no shard manifest (upload the shards first)")
        a = od_gcp.parser().parse_args(["label", "--name", name, "--base", BASE, "--layout", LAYOUT,
                                        "--shards-dir", str(sd), "--revision", REVISION])
        try:
            od_gcp.cmd_label(a)
        except _Deadline:
            vol.commit()
            done["status"] = "deadline"
            break
        vol.commit()
        done[fam] = str(sd / f"labels_{name}")
    return done


@app.local_entrypoint()
def crowd(name: str, fams: str, max_min: float = 0.0):
    import time
    if not 1 <= max_min <= 600:
        raise SystemExit("--max-min is required (1-600; endgame/crowd_cap.py prints it): no uncapped crowd read")
    deadline = time.time() + 60 * max_min
    fn = crowd_read.with_options(timeout=int(60 * max_min))
    print(json.dumps({"launch": name, "fams": fams, "max_min": max_min, "deadline_unix": round(deadline)}))
    print(json.dumps(fn.remote(name, [f for f in fams.split(",") if f], deadline)))
