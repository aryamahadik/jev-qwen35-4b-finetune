"""grid_h100.hostops: the container-side operations that touch the outside world (Volume, network, GPU), kept apart so that the session
logic can be tested with fakes. Nothing here imports Modal."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from . import common as C
from . import merge_direct as MD

SNAP_REL = Path("hub") / ("models--" + C.BASE.replace("/", "--")) / "snapshots" / C.REVISION


class HostRefused(SystemExit):
    pass


def check_gpu(name: str | None) -> None:
    if not name or "H100" not in name:
        raise HostRefused(f"hostops: the GPU is {name!r}, not an H100")


def sglang_version(python: str = sys.executable) -> str:
    r = subprocess.run([python, "-c", "import sglang; print(sglang.__version__)"], capture_output=True, text=True, timeout=600)
    return r.stdout.strip()


def fetch_missing(names, dest, run=subprocess.run) -> dict:
    """Pinned non-weight files the Volume's HF snapshot lacks (preprocessor configs, LICENSE) come from the Hub at the pinned revision,
    in a subprocess so that this process stays offline; they are checked against BASE_PINS afterwards."""
    names = sorted(names)
    if not names:
        return {}
    env = {**os.environ, "HF_HOME": "/tmp/hf_meta", "HF_HUB_OFFLINE": "0"}
    code = ("import json; from huggingface_hub import hf_hub_download; "
            f"print(json.dumps({{n: hf_hub_download({C.BASE!r}, n, revision={C.REVISION!r}) for n in {names!r}}}))")
    r = run([sys.executable, "-c", code], env=env, capture_output=True, text=True, timeout=900)
    if r.returncode != 0:
        raise HostRefused(f"hostops: could not fetch {names} from the Hub: {(r.stderr or '')[-300:]}")
    got = json.loads(r.stdout.strip().splitlines()[-1])
    for n, p in got.items():
        shutil.copyfile(p, Path(dest) / n)
    return got


def download_base(dest, run=subprocess.run) -> Path:
    env = {**os.environ, "HF_HOME": "/tmp/hf", "HF_HUB_OFFLINE": "0"}
    code = (f"from huggingface_hub import snapshot_download; "
            f"print(snapshot_download({C.BASE!r}, revision={C.REVISION!r}, local_dir={str(dest)!r}))")
    r = run([sys.executable, "-c", code], env=env, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        raise HostRefused(f"hostops: base download failed: {(r.stderr or '')[-300:]}")
    return Path(dest)


def prepare_base(hf_root="/vol/hf", dest="/tmp/base", log=print, fetch=fetch_missing, download=download_base) -> dict:
    """The pinned Qwen3.5-4B snapshot on LOCAL disk (read by 19 merges): copied from the Volume's HF cache when it is there, else
    downloaded; the 12 pinned files are checked (weights by LFS sha256) before anything is merged."""
    src, dest = Path(hf_root) / SNAP_REL, Path(dest)
    if dest.exists():
        shutil.rmtree(dest)
    where = "volume"
    if src.exists() and any(src.glob("*.safetensors")):
        shutil.copytree(src, dest, symlinks=False)
    else:
        where = "hub download"
        download(dest)
    missing = [n for n in MD.BASE_PINS if not (dest / n).exists()]
    if missing:
        fetch(missing, dest)
    probs = MD.check_base_pins(dest)
    if probs:
        raise HostRefused("hostops: the base snapshot is not the pinned Qwen3.5-4B @ 851bf6e8: " + "; ".join(probs[:5]))
    log(f"base snapshot ready ({where}), {len(MD.BASE_PINS)} pins verified, missing fetched: {missing}")
    return {"base_dir": str(dest), "source": where, "fetched": missing, "pins_ok": True}


def prepare_c1_tok(src, pins: dict) -> Path:
    """C1's tokenizer + prompt-layout files (shipped with the job) checked against the S1 pin's tokenizer_pins."""
    src = Path(src)
    bad = []
    for n, want in sorted(pins.items()):
        p = src / n
        if not p.exists():
            bad.append(f"{n}: missing")
        elif C.sha256_file(p) != want:
            bad.append(f"{n}: sha256 differs from the pin")
    if bad:
        raise HostRefused("hostops: C1 tokenizer files differ from the S1 pin: " + "; ".join(bad))
    return src
