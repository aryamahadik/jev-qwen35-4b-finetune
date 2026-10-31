"""p7_common: shared helpers of the P7 serving-freeze tools (C2 odds analysis lane P7). CPU only; no Modal.

The S1 path = SGLang 0.5.20, merged BF16 checkpoint, fp32 LM head, hybrid prefix cache (A35 / SPEED-2 arm S1), served on
the free L4 VM od-l4b through reads/fast_read.py (A49 f). Nothing here stops, restarts or signals a process it did not
start: the VM command runner refuses anything that is not a read (assert_readonly).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent            # lean/c2_build/serving
BUILD = HERE.parent                               # lean/c2_build
FORBIDDEN_PATH = re.compile(r"ohs|sealed|quarantine|longbench|jevbench|decision_index|ejs|jev_out", re.I)

C1_NAME = "q35_4b_main500k"
C1_ADAPTER_SHA256 = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
BASE = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
LAYOUT, STYLE = "schema_branch_mark", "cygnet"
PROD_PORT = 30000                                 # od-l4b production C1 server: never stopped, restarted or flushed here


def find_lean() -> Path:
    for c in (os.environ.get("OD_LEAN"), HERE.parents[1], Path.home() / "lean"):
        if c and (Path(c) / "decoder_io.py").exists() and (Path(c) / "hosting").exists():
            return Path(c).resolve()
    raise SystemExit("p7: no lean root with decoder_io.py and hosting/ (set OD_LEAN)")


def add_paths() -> Path:
    lean = find_lean()
    for p in (lean, lean / "hosting"):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    return lean


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def canon_sha(obj) -> str:
    return hashlib.sha256(canon(obj).encode()).hexdigest()


def refuse_path(p) -> None:
    """The never-open rule: sealed / OHS / quarantine / Jev / benchmark paths are refused by name."""
    if FORBIDDEN_PATH.search(str(p)):
        raise SystemExit(f"p7: {p}: a path of a sealed / OHS / quarantined / benchmark set is never opened here")


# ---- VM access (read-only) -------------------------------------------------------------------------------------------
READONLY_BAD = re.compile(
    r"(^|[\s;&|`(])(kill|pkill|killall|rm|mv|rmdir|shutdown|reboot|halt|poweroff|systemctl|service|nohup|setsid|"
    r"truncate|dd|chmod|chown|tee|sed\s+-i|apt|apt-get|pip|uv|nvidia-smi\s+(-r|--gpu-reset)|"
    r"gcloud\s+compute\s+instances\s+(stop|start|delete|reset|suspend))(\s|$)|stop_server|start_server|"
    r"prod_stop|prod_start|fast_read\.py\s+(serve|stop)|flush_cache|/admin/flush|-X\s*POST|--data|--request\s+POST")


def assert_readonly(cmd: str) -> str:
    """Refuse a VM command that could change the production server or anything else. Reads only (curl GET, cat, ls, ps,
    sha256sum, /proc, python3 scripts that only read, writes under /tmp/p7_* are allowed)."""
    m = READONLY_BAD.search(cmd)
    if not m:
        m = re.search(r">>?\s*(?!/tmp/p7_|/dev/null|&\d)\S", cmd)    # any redirection except to /tmp/p7_*, /dev/null, 2>&1
    if m:
        raise SystemExit(f"p7: VM command refused (not a read): {m.group(0).strip()!r}")
    return cmd


class Vm:
    """od-l4b through reads/vm_scripts/vm.sh (gcloud IAP ssh). Every command passes assert_readonly."""

    def __init__(self, script: Path | None = None, run=subprocess.run):
        self.script = Path(script or BUILD / "reads/vm_scripts/vm.sh")
        self.run = run

    def ssh(self, cmd: str, timeout: int = 180) -> str:
        assert_readonly(cmd)
        r = self.run(["bash", str(self.script), "ssh", cmd], capture_output=True, text=True, timeout=timeout)
        if r.returncode != 0:
            raise RuntimeError(f"vm ssh rc={r.returncode}: {(r.stdout or '')[-300:]}{(r.stderr or '')[-300:]}")
        return r.stdout

    def put(self, local, remote: str, timeout: int = 180) -> None:
        if not str(remote).startswith("od-l4b:/tmp/p7_"):
            raise SystemExit("p7: Vm.put writes only od-l4b:/tmp/p7_*")
        r = self.run(["bash", str(self.script), "scp", str(local), remote], capture_output=True, text=True, timeout=timeout)
        if r.returncode != 0:
            raise RuntimeError(f"vm scp rc={r.returncode}: {(r.stdout or '')[-300:]}")

    def get(self, remote: str, local, timeout: int = 180) -> None:
        r = self.run(["bash", str(self.script), "scp", remote, str(local)], capture_output=True, text=True, timeout=timeout)
        if r.returncode != 0:
            raise RuntimeError(f"vm scp rc={r.returncode}: {(r.stdout or '')[-300:]}")
