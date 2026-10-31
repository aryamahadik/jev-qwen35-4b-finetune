"""cold_start_probe.py (M4a): decompose the cold start of the S1 server on the box it runs on, n boots (VM-side, in a window).

Run ONLY inside an authorised L-D window (env LD_WINDOW=<label>; exit 9 when a C2 read job runs), with the GPU free (the
production server on port 30000 stopped by the window runner -- this script never stops a process it did not start, never
touches port 30000, and aborts when the GPU still holds more than --gpu-free-mib).

Per boot (repeat n times) it records, with perf_counter timestamps:
  t_spawn          the start command was launched (own process group; the pid is the only thing it may stop)
  markers          log markers by regex, first/last sight (defaults match SGLang 0.5.20 quiet logs: shards loaded, graph capture
                   begin/end); a marker never seen is null, never guessed
  t_health         /health first answered 200              -> boot_s = t_health - t_spawn
  first_decision   the first real decision (POST --body-file to --path) after health: lazy init / autotune shows here
  warm_p50         the median of the next --warm-n decisions
  cold_total_s     boot_s + first_decision_s (what a request that triggers a cold start waits, before any queueing)
  page_cache       "warm" (weights in the OS page cache from the previous boot) or "dropped" (--drop-caches: sudo -n sync; echo 3 >
                   /proc/sys/vm/drop_caches before the spawn: the disk-cold case that a VM start gives)
then stops the server it started (--stop-cmd, else SIGTERM to its process group) and waits for the GPU memory to fall.
Output: out/cold_start_<name>.json, every number tagged author-run with n = the number of boots (and calls for warm_p50).

  LD_WINDOW=W1 cold_start_probe.py --name ldcold --port 30010 \\
      --start-cmd 'bash ~/opt_r2/trial_server.sh ldcold 30010' --log-file ~/opt_r2/logs/ldcold.server.log \\
      --body-file ~/opt_r2/ld_body.json --repeat 3 --drop-caches-every 3 --out out/cold_start_L4.json
  cold_start_probe.py --dry-run ...           prints the plan and checks nothing else
The decision body is one real /generate body (input_ids + sampling params) written once with make_probe_body.py.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

DEFAULT_MARKERS = {
    "weights_loaded": {"re": r"loading shards:\s+100%", "which": "first"},
    "graph_capture_begin": {"re": r"Capturing (num tokens|batches).*\b0/\d+", "which": "first"},
    "graph_capture_end": {"re": r"Capturing (num tokens|batches).*\b100%\|", "which": "last"},
}


class LogTail:
    """Reads new bytes of a log file on every poll and stamps each marker with the poll time it was first/last seen."""

    def __init__(self, path, markers):
        self.path, self.pos = Path(path) if path else None, 0
        self.markers = {k: {"rx": re.compile(v["re"]), "which": v["which"], "t": None} for k, v in markers.items()}
        if self.path and self.path.exists():
            self.pos = self.path.stat().st_size            # only what this boot writes

    def poll(self, now: float) -> None:
        if not self.path or not self.path.exists():
            return
        with open(self.path, "rb") as f:
            f.seek(self.pos)
            chunk = f.read()
            self.pos = f.tell()
        text = chunk.decode("utf-8", "replace").replace("\r", "\n")
        for line in text.splitlines():
            for m in self.markers.values():
                if m["rx"].search(line) and (m["which"] == "last" or m["t"] is None):
                    m["t"] = now

    def result(self, t0: float) -> dict:
        return {k: (None if m["t"] is None else round(m["t"] - t0, 3)) for k, m in self.markers.items()}


def http(url, body=None, timeout=60.0):
    req = urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"} if body is not None else {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def one_boot(a, body, boot_idx: int, drop: bool) -> dict:
    rec = {"boot": boot_idx, "page_cache": "dropped" if drop else "warm"}
    if drop:
        r = subprocess.run(["sudo", "-n", "sh", "-c", "sync; echo 3 > /proc/sys/vm/drop_caches"], capture_output=True, text=True)
        rec["drop_caches_rc"] = r.returncode
        if r.returncode != 0:
            rec["page_cache"] = "warm (drop_caches failed: " + (r.stderr or "")[:80].strip() + ")"
    mem = C.gpu_mem_used_mib()
    if mem is not None and mem > a.gpu_free_mib:
        raise SystemExit(f"GPU holds {mem} MiB (> {a.gpu_free_mib}): another job owns it; this script will not stop it")
    tail = LogTail(a.log_file, DEFAULT_MARKERS)
    t0 = time.perf_counter()
    proc = subprocess.Popen(a.start_cmd, shell=True, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    rec["pid"] = proc.pid
    base = f"http://127.0.0.1:{a.port}"
    t_health = None
    try:
        while time.perf_counter() - t0 < a.boot_timeout:
            now = time.perf_counter()
            tail.poll(now)
            if proc.poll() is not None and t_health is None and proc.returncode not in (0, None):
                rec["error"] = f"start command exited rc={proc.returncode}"
                break
            try:
                st, _ = http(base + "/health", timeout=2.0)
                if st == 200:
                    t_health = time.perf_counter()
                    tail.poll(t_health)
                    break
            except (urllib.error.URLError, OSError, ValueError):
                pass
            time.sleep(a.poll_s)
        rec["markers_s"] = tail.result(t0)
        if t_health is None:
            rec.setdefault("error", "boot timeout")
            return rec
        rec["boot_s"] = round(t_health - t0, 2)
        lat = []
        for i in range(1 + a.warm_n):
            t1 = time.perf_counter()
            st, _ = http(base + a.path, body, timeout=120.0)
            lat.append((time.perf_counter() - t1) * 1000.0)
            if st != 200:
                rec["error"] = f"decision status {st}"
                break
        rec["first_decision_ms"] = round(lat[0], 1)
        rec["cold_total_s"] = round(rec["boot_s"] + lat[0] / 1000.0, 2)
        rec["warm_ms"] = C.summarize(lat[1:])
    finally:
        rec["stopped"] = stop_own(proc, a)
    return rec


def stop_own(proc, a) -> dict:
    """Stop only what this script started: --stop-cmd (it names the trial it launched), else SIGTERM to the process group."""
    out = {}
    if a.stop_cmd:
        out["stop_cmd_rc"] = subprocess.run(a.stop_cmd, shell=True, capture_output=True, timeout=120).returncode
    elif proc.poll() is None:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            out["sigterm_group"] = proc.pid
        except (ProcessLookupError, PermissionError) as e:
            out["error"] = str(e)
    t = time.time()
    while time.time() - t < 90:
        mem = C.gpu_mem_used_mib()
        if mem is None or mem < a.gpu_free_mib:
            break
        time.sleep(2)
    out["gpu_mem_after_mib"] = C.gpu_mem_used_mib()
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--name", required=True)
    ap.add_argument("--port", type=int, required=True, help="the trial server port (never 30000)")
    ap.add_argument("--start-cmd", required=True)
    ap.add_argument("--stop-cmd")
    ap.add_argument("--log-file", help="the server log to tail for phase markers")
    ap.add_argument("--body-file", required=True, help="one real decision body (JSON) for the first-decision timing")
    ap.add_argument("--path", default="/generate")
    ap.add_argument("--repeat", type=int, default=3)
    ap.add_argument("--drop-caches-every", type=int, default=0, help="drop the page cache before every k-th boot (0 = never)")
    ap.add_argument("--warm-n", type=int, default=20)
    ap.add_argument("--boot-timeout", type=float, default=1500.0)
    ap.add_argument("--poll-s", type=float, default=0.25)
    ap.add_argument("--gpu-free-mib", type=int, default=1500)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    C.refuse_prod_port(a.port, "a cold-start probe")
    C.refuse_modal(a.start_cmd)
    plan = {"name": a.name, "port": a.port, "repeat": a.repeat, "start_cmd": a.start_cmd, "stop_cmd": a.stop_cmd,
            "drop_caches_every": a.drop_caches_every, "markers": DEFAULT_MARKERS}
    if a.dry_run:
        print(json.dumps(plan, indent=1))
        return 0
    window = C.require_window()
    body = json.loads(Path(a.body_file).read_text())
    boots = []
    for i in range(1, a.repeat + 1):
        drop = bool(a.drop_caches_every) and i % a.drop_caches_every == 0
        r = one_boot(a, body, i, drop)
        boots.append(r)
        print(f"boot {i}: {r.get('page_cache')} boot_s={r.get('boot_s')} first_decision_ms={r.get('first_decision_ms')} "
              f"markers={r.get('markers_s')} {r.get('error', '')}", flush=True)
    ok = [b for b in boots if "boot_s" in b and "error" not in b]
    res = {"window": window, "utc": C.utc(), "plan": plan, "boots": boots,
           "summary": {"n_boots_ok": len(ok),
                       "boot_s": C.summarize([b["boot_s"] for b in ok]),
                       "boot_s_page_cache_warm": C.summarize([b["boot_s"] for b in ok if b["page_cache"] == "warm"]),
                       "boot_s_page_cache_dropped": C.summarize([b["boot_s"] for b in ok if b["page_cache"] == "dropped"]),
                       "cold_total_s": C.summarize([b["cold_total_s"] for b in ok])},
           "tag": C.tag("author-run", n=len(ok), source=f"cold_start_probe.py {a.name} window {window}") if ok else C.tag("not-measured")}
    C.write_json(a.out, res)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
