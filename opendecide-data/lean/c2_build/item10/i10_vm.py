"""Item 10: the free C1 reads on the GCP L4 (od-l4b) through the already-running SGLang server (reads/fast_read.py,
zed_orch/GCP_RUNBOOK.md). Never stops or restarts the VM or the server unless the server is down (then the same
start_server.sh line that reads/vm_scripts/crowd_driver.sh uses). One bulk read at a time: refuses while any fast_read /
od_gcp job runs. No Modal, no paid compute.

  i10_vm.py status                          VM state, server health, running jobs
  i10_vm.py predict-start                   push data/i10_c1read.jsonl, check its sha256, start the 2-view read (detached)
  i10_vm.py predict-wait [--minutes N]      poll the job log until rc=...
  i10_vm.py predict-pull                    pull preds_i10_c1read/q35_4b_main500k.{jsonl,meta.json}
  i10_vm.py crowd-start                     push data/c2_crowd_shards/I10, start the one-view crowd read (crowd_driver.sh I10)
  i10_vm.py crowd-wait [--minutes N]
  i10_vm.py crowd-pull                      pull data/c2_crowd_shards/I10/labels_q35_4b_main500k
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import i10_lib as L  # noqa: E402

P, Z, V = "system-one-509903", "us-east4-c", "od-l4b"
TMP = os.environ.get("I10_TMP", "/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/adbc4a3b-e366-431b-b0e2-96c55904b928/scratchpad")
IAP = ["--tunnel-through-iap", "--zone", Z, "--project", P]
NOISE = ("numpy", "increasing_the_tcp", "warning", "tunnel, consider")


def _filter(txt: str) -> str:
    return "\n".join(l for l in txt.splitlines() if l.strip() and not any(n in l.lower() for n in NOISE))


def ssh(cmd: str, check: bool = True, timeout: int = 900) -> str:
    r = subprocess.run(["gcloud", "compute", "ssh", V, *IAP, "--command", cmd], capture_output=True, text=True, timeout=timeout)
    out = _filter(r.stdout + "\n" + r.stderr)
    if check and r.returncode != 0:
        raise SystemExit(f"ssh failed (rc={r.returncode}): {out[-600:]}")
    return out


def scp(*args: str, timeout: int = 1800) -> str:
    r = subprocess.run(["gcloud", "compute", "scp", *IAP, *args], capture_output=True, text=True, timeout=timeout)
    out = _filter(r.stdout + "\n" + r.stderr)
    if r.returncode != 0:
        raise SystemExit(f"scp failed (rc={r.returncode}): {out[-600:]}")
    return out


def status() -> str:
    return ssh('date -u; curl -s -m 5 -o /dev/null -w "health=%{http_code}\\n" localhost:30000/health; '
               'pgrep -af "fast_read|od_gcp|crowd_driver|label_driver" | grep -v pgrep | cut -c1-160; '
               'nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader', check=False)


def busy() -> bool:
    out = ssh('pgrep -af "fast_read.py (predict|label)|od_gcp.py|crowd_driver|label_driver" | grep -v pgrep | wc -l', check=False)
    try:
        return int(out.strip().splitlines()[-1]) > 0
    except (ValueError, IndexError):
        return True


def need_server_up() -> None:
    h = ssh('curl -s -m 5 -o /dev/null -w "%{http_code}" localhost:30000/health', check=False).strip().splitlines()
    if not h or h[-1] != "200":
        raise SystemExit("the SGLang server is down: start it with the runbook line (reads/README.md, section 1), then retry")


def predict_start() -> None:
    need_server_up()
    if busy():
        raise SystemExit("a bulk read is running on the VM: one bulk read at a time")
    f = L.DATA / f"{L.READ_SPLIT}.jsonl"
    scp(str(f), str(f) + ".sha256", f"{V}:~/lean/data/")
    print(ssh(f"cd ~/lean/data && sha256sum -c {L.READ_SPLIT}.jsonl.sha256"))
    ssh(f'cd ~/reads && rm -f ~/jobs/i10_read.log && (setsid nohup bash -c "export PATH=\\$HOME/bin:\\$PATH; '
        f'~/od/bin/python -B fast_read.py predict --name {L.C1} --splits {L.READ_SPLIT} --workers 12 --chunk 8; echo rc=\\$?" '
        f'> ~/jobs/i10_read.log 2>&1 < /dev/null &)')
    print("started", time.strftime("%H:%M:%S", time.gmtime()), "UTC")


def wait(log: str, minutes: int) -> str:
    end = time.time() + 60 * minutes
    while time.time() < end:
        out = ssh(f"tail -c 400 {log}", check=False)
        if "rc=" in out or "DRIVER_DONE" in out:
            return out
        time.sleep(60)
    return "timeout\n" + ssh(f"tail -c 400 {log}", check=False)


def predict_pull() -> None:
    d = L.LEAN / f"preds_{L.READ_SPLIT}"
    d.mkdir(parents=True, exist_ok=True)
    scp(f"{V}:~/lean/preds_{L.READ_SPLIT}/{L.C1}.jsonl", f"{V}:~/lean/preds_{L.READ_SPLIT}/{L.C1}.meta.json", str(d) + "/")
    print(sorted(p.name for p in d.iterdir()))


def crowd_start() -> None:
    need_server_up()
    if busy():
        raise SystemExit("a bulk read is running on the VM: one bulk read at a time")
    src = L.DATA / "c2_crowd_shards" / "I10"
    if not src.is_dir():
        raise SystemExit("no shards: run `c2_select.py tasks --fam I10 --write-shards` first")
    tgz = f"{TMP}/i10_crowd_shards.tgz"
    subprocess.run(["tar", "czf", tgz, "--exclude", "labels_*", "-C", str(L.DATA), "c2_crowd_shards/I10"], check=True)
    scp(tgz, f"{V}:~/jobs/i10_crowd_shards.tgz")
    ssh("cd ~/lean/data && rm -rf c2_crowd_shards/I10 && tar xzf ~/jobs/i10_crowd_shards.tgz && ls c2_crowd_shards/I10 | head -3")
    ssh('ls ~/reads/crowd_driver.sh >/dev/null 2>&1 || echo missing', check=False)
    scp(str(Path(__file__).resolve().parent.parent / "reads" / "vm_scripts" / "crowd_driver.sh"), f"{V}:~/reads/crowd_driver.sh")   # the VM may not hold it
    ssh('cd ~/reads && rm -f ~/jobs/i10_crowd.log && (setsid nohup bash ~/reads/crowd_driver.sh I10 > ~/jobs/i10_crowd.log 2>&1 < /dev/null &)')
    print("started", time.strftime("%H:%M:%S", time.gmtime()), "UTC")


def crowd_pull() -> None:
    dst = L.DATA / "c2_crowd_shards" / "I10"
    dst.mkdir(parents=True, exist_ok=True)
    scp("--recurse", f"{V}:~/lean/data/c2_crowd_shards/I10/labels_{L.C1}", str(dst) + "/")
    print(sorted(p.name for p in (dst / f"labels_{L.C1}").iterdir())[:6])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["status", "predict-start", "predict-wait", "predict-pull", "crowd-start", "crowd-wait",
                                    "crowd-pull"])
    ap.add_argument("--minutes", type=int, default=9)
    a = ap.parse_args(argv)
    if a.cmd == "status":
        print(status())
    elif a.cmd == "predict-start":
        predict_start()
    elif a.cmd == "predict-wait":
        print(wait("~/jobs/i10_read.log", a.minutes))
    elif a.cmd == "predict-pull":
        predict_pull()
    elif a.cmd == "crowd-start":
        crowd_start()
    elif a.cmd == "crowd-wait":
        print(wait("~/jobs/i10_crowd.log", a.minutes))
    elif a.cmd == "crowd-pull":
        crowd_pull()


if __name__ == "__main__":
    main()
