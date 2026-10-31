"""vm_cold_cycle.py (M4b): the scale-from-zero cost of the GCP path = VM stop -> VM start -> ssh up -> server healthy -> first decision.

A stopped GCE VM costs only its disk (gcp_run.sh), so "stop when idle, start on demand" is the cheapest warm-pool setting; this
script measures what the first request then waits. It runs from the Mac with gcloud (the transport gcp_run.sh uses: IAP ssh).
DRY RUN BY DEFAULT: without --go it only prints the commands. It STOPS THE VM, which kills the production server on it, so it is
an owner/orchestrator window action and has three guards: env LD_WINDOW (an authorised L-D window), env LD_VM_CYCLE_OK=yes
(this specific action), and a pre-check over ssh that no C2 read job is running (prod_stop.sh's pattern). After the cycles the VM
is left RUNNING with the production server restarted exactly as prod_start.sh does (--restore-cmd), and the downtime is logged.

Per cycle (perf_counter on the Mac, so each ssh poll adds up to --poll-s of resolution and ~2-4 s of IAP overhead on the ssh steps;
the numbers say so):
  stop_s      gcloud compute instances stop returns
  start_s     gcloud compute instances start returns (instance RUNNING)
  ssh_s       from start returned until `ssh true` works
  server_s    from ssh up until localhost:PORT/health answers 200 on the VM (the server is started by the VM's own startup, or by
              --server-start-cmd run over ssh if it does not come up by itself within --autostart-wait-s)
  total_s     stop not included: start command issued -> healthy  (what a request waits after a scale-from-zero)
  first_decision_ms (optional --probe-cmd run on the VM: it must print one JSON line {"ms": <float>})
Quota: GPUS_ALL_REGIONS = 1 and CPUS_ALL_REGIONS = 16; a start can fail with a stockout or quota error (gcp_run.sh exit 3): a failed
start is recorded as a result, not retried silently.

  LD_WINDOW=W1 LD_VM_CYCLE_OK=yes vm_cold_cycle.py --vm od-l4b --cycles 3 --go \\
      --restore-cmd '~/reads/start_server.sh --max-running 32 --max-mamba 128 --mem-fraction 0.8 --extra-args "--attention-backend triton"' \\
      --out out/vm_cold_cycle_od-l4b.json
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

PROJECT = "system-one-509903"
ZONES = {"od-l4": "us-central1-a", "od-l4b": "us-east4-c"}       # GPU VMs (gcp_run.sh); od-cpu1 has no GPU


def gcloud(vm, zone, *args):
    return ["gcloud", "compute", *args, vm, "--zone", zone, "--project", PROJECT]


def ssh(vm, zone, cmd):
    return ["gcloud", "compute", "ssh", vm, "--zone", zone, "--project", PROJECT, "--tunnel-through-iap", "--quiet", "--command", cmd]


def commands(vm, zone, port, probe_cmd=None, server_start=None) -> dict:
    return {"c2_check": ssh(vm, zone, f"pgrep -af '{C.C2_JOB_PATTERN}' || true"),
            "stop": gcloud(vm, zone, "instances", "stop"), "start": gcloud(vm, zone, "instances", "start"),
            "ssh_up": ssh(vm, zone, "true"),
            "health": ssh(vm, zone, f"curl -s -m 5 -o /dev/null -w '%{{http_code}}' localhost:{port}/health"),
            "server_start": ssh(vm, zone, server_start) if server_start else None,
            "probe": ssh(vm, zone, probe_cmd) if probe_cmd else None}


def run(cmd, timeout=900):
    t = time.perf_counter()
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr, time.perf_counter() - t


def one_cycle(a, cmds) -> dict:
    rec = {}
    rc, _, err, dt = run(cmds["stop"])
    rec["stop_s"], rec["stop_rc"] = round(dt, 1), rc
    if rc:
        rec["error"] = "stop failed: " + err[-200:]
        return rec
    t_start = time.perf_counter()
    rc, _, err, dt = run(cmds["start"])
    rec["start_s"], rec["start_rc"] = round(dt, 1), rc
    if rc:
        rec["error"] = "start failed (stockout or quota?): " + err[-200:]
        return rec
    t0 = time.perf_counter()
    while time.perf_counter() - t0 < a.timeout_s:
        if run(cmds["ssh_up"], 120)[0] == 0:
            break
        time.sleep(a.poll_s)
    else:
        rec["error"] = "ssh never came up"
        return rec
    rec["ssh_s"] = round(time.perf_counter() - t0, 1)
    t1 = time.perf_counter()
    started_by_us = False
    while time.perf_counter() - t1 < a.timeout_s:
        rc, out, _, _ = run(cmds["health"], 60)
        if rc == 0 and out.strip().endswith("200"):
            break
        if cmds["server_start"] and not started_by_us and time.perf_counter() - t1 > a.autostart_wait_s:
            run(cmds["server_start"], 1800)
            started_by_us = True
        time.sleep(a.poll_s)
    else:
        rec["error"] = "server never healthy"
        return rec
    rec["server_s"] = round(time.perf_counter() - t1, 1)
    rec["server_started_by_script"] = started_by_us
    rec["total_s"] = round(time.perf_counter() - t_start, 1)
    if cmds["probe"]:
        rc, out, _, _ = run(cmds["probe"], 300)
        try:
            rec["first_decision_ms"] = float(json.loads(out.strip().splitlines()[-1])["ms"])
        except (ValueError, KeyError, IndexError):
            rec["first_decision_ms"] = None
    return rec


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vm", required=True, choices=sorted(ZONES))
    ap.add_argument("--cycles", type=int, default=3)
    ap.add_argument("--port", type=int, default=30000, help="the port of the server ON THE VM that is polled (its production port)")
    ap.add_argument("--server-start-cmd")
    ap.add_argument("--autostart-wait-s", type=float, default=120.0)
    ap.add_argument("--restore-cmd", help="run once at the end if the server is not healthy (production restart)")
    ap.add_argument("--probe-cmd")
    ap.add_argument("--poll-s", type=float, default=5.0)
    ap.add_argument("--timeout-s", type=float, default=1800.0)
    ap.add_argument("--go", action="store_true", help="really stop/start the VM (default: print the commands only)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    zone = ZONES[a.vm]
    cmds = commands(a.vm, zone, a.port, a.probe_cmd, a.server_start_cmd)
    if not a.go:
        print(json.dumps({k: v for k, v in cmds.items() if v}, indent=1))
        print("DRY RUN: nothing executed (add --go inside an authorised window).")
        return 0
    window = C.require_window()
    if os.environ.get("LD_VM_CYCLE_OK") != "yes":
        raise SystemExit("LD_VM_CYCLE_OK=yes is required: this action stops the VM and the production server on it")
    rc, out, _, _ = run(cmds["c2_check"], 120)
    if rc != 0 or out.strip():
        print("C2 read job running on the VM (or the check failed): not stopping it\n" + out[:300], file=sys.stderr)
        return 9
    cyc = []
    for i in range(a.cycles):
        r = one_cycle(a, cmds)
        r["cycle"] = i + 1
        cyc.append(r)
        print(f"cycle {i + 1}: {r}", flush=True)
        if "error" in r:
            break
    restored = None
    rc, out, _, _ = run(cmds["health"], 120)
    if not (rc == 0 and out.strip().endswith("200")) and a.restore_cmd:
        restored = run(ssh(a.vm, zone, a.restore_cmd), 1800)[0]
    ok = [c for c in cyc if "error" not in c]
    res = {"window": window, "utc": C.utc(), "vm": a.vm, "zone": zone, "cycles": cyc, "restore_rc": restored,
           "summary": {"n_ok": len(ok), "total_s": C.summarize([c["total_s"] for c in ok]), "server_s": C.summarize([c["server_s"] for c in ok]),
                       "ssh_s": C.summarize([c["ssh_s"] for c in ok]), "start_s": C.summarize([c["start_s"] for c in ok])},
           "tag": C.tag("author-run", n=len(ok), source=f"vm_cold_cycle.py {a.vm} window {window}") if ok else C.tag("not-measured"),
           "note": "perf_counter on the Mac; ssh steps include IAP overhead; a stopped VM bills its disk only (gcp_run.sh)"}
    C.write_json(a.out, res)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
