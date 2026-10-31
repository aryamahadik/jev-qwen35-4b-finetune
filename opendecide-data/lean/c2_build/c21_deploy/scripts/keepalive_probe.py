"""keepalive_probe.py (M5): what does idleness cost? Latency of the first decision after an idle gap vs warm decisions.

Sequential client against ONE server we started (a trial server, never port 30000). For every gap g (seconds) in --gaps it
repeats --reps times: sleep g with the connection left open, send one decision on the SAME keep-alive connection (the "first"
call) and then --warm-k more; per rep it also samples nvidia-smi (pstate, sm clock, power) just before the first call so a GPU
down-clock after idle is visible. It records connection resets (the server or a proxy closed the idle connection: uvicorn's
default keep-alive timeout is 5 s; the client then has to reconnect, ~3 round trips with TLS) separately from model latency.

Outputs per gap (all author-run, n = reps): first_call_ms, warm_p50_ms (all warm calls pooled across gaps), penalty_ms =
first - warm p50, conn_reset_share, gpu sm_mhz / pstate at the first call. Dollar cost of keeping an instance alive is not
measured here: it is warm_pool_sim.py (rate x idle hours); this script measures what you buy with it (no cold penalty) and what
you lose without it (the penalty per gap length).

  LD_WINDOW=W1 keepalive_probe.py --url http://127.0.0.1:30010 --path /generate --body-file out/probe_body_N0.json \\
      --gaps 0:30,5:20,30:10,120:5,600:3 --warm-k 5 --out out/keepalive_L4.json
  (short profile ~47 min of wall time; the long one adds 1800:3, +90 min.)
--cpu-echo skips the window check for tests against a local stand-in server.
"""
from __future__ import annotations

import argparse
import http.client
import json
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402


def gpu_state() -> dict:
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=pstate,clocks.sm,power.draw,utilization.gpu", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=5).stdout.strip().splitlines()[0].split(",")
        return {"pstate": out[0].strip(), "sm_mhz": float(out[1]), "power_w": float(out[2]), "util": float(out[3])}
    except (OSError, subprocess.SubprocessError, ValueError, IndexError):
        return {}


class Conn:
    """One keep-alive connection; a call after the peer closed it reconnects once and says so."""

    def __init__(self, url):
        u = urlparse(url)
        self.cls = http.client.HTTPSConnection if u.scheme == "https" else http.client.HTTPConnection
        self.host, self.port = u.hostname, u.port or (443 if u.scheme == "https" else 80)
        self.c = None

    def _open(self):
        self.c = self.cls(self.host, self.port, timeout=120)
        self.c.connect()
        try:
            import socket
            self.c.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except OSError:
            pass

    def post(self, path, body: bytes):
        reset = False
        if self.c is None:
            self._open()
        for attempt in (0, 1):
            try:
                t0 = time.perf_counter()
                self.c.request("POST", path, body=body, headers={"Content-Type": "application/json"})
                r = self.c.getresponse()
                r.read()
                return r.status, (time.perf_counter() - t0) * 1000.0, reset
            except (http.client.RemoteDisconnected, ConnectionResetError, BrokenPipeError, http.client.CannotSendRequest, OSError):
                if attempt:
                    raise
                reset = True
                self._open()

    def close(self):
        if self.c:
            self.c.close()


def parse_gaps(s: str) -> list:
    out = []
    for part in s.split(","):
        g, n = part.split(":")
        out.append((float(g), int(n)))
    return out


def run(a) -> dict:
    body = Path(a.body_file).read_bytes()
    conn = Conn(a.url)
    for _ in range(a.warmup):
        conn.post(a.path, body)
    per_gap, warm_all = {}, []
    for g, reps in parse_gaps(a.gaps):
        rows = []
        for r in range(reps):
            time.sleep(g)
            gs = gpu_state()
            st, first, reset = conn.post(a.path, body)
            warm = []
            for _ in range(a.warm_k):
                _, ms, _ = conn.post(a.path, body)
                warm.append(ms)
            warm_all += warm
            rows.append({"first_ms": first, "status": st, "conn_reset": reset, "gpu": gs})
            print(f"gap {g:g}s rep {r + 1}/{reps}: first {first:.1f} ms reset={reset} warm_p50 {C.pct(warm, 0.5):.1f} gpu={gs}", flush=True)
        per_gap[str(g)] = rows
    conn.close()
    wp50 = C.pct(warm_all, 0.5)
    summ = {}
    for g, rows in per_gap.items():
        f = [x["first_ms"] for x in rows]
        sm = [x["gpu"]["sm_mhz"] for x in rows if x["gpu"]]
        summ[g] = {"n": len(rows), "first_ms": C.summarize(f), "penalty_ms_p50": round(C.pct(f, 0.5) - wp50, 2),
                   "conn_reset_share": round(sum(x["conn_reset"] for x in rows) / len(rows), 3),
                   "gpu_sm_mhz_mean": round(sum(sm) / len(sm), 0) if sm else None,
                   "gpu_pstates": sorted({x["gpu"].get("pstate") for x in rows if x["gpu"]})}
    return {"warm_ms": C.summarize(warm_all), "gaps": summ, "raw": per_gap}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--url", required=True)
    ap.add_argument("--path", default="/generate")
    ap.add_argument("--body-file", required=True)
    ap.add_argument("--gaps", default="0:30,5:20,30:10,120:5,600:3", help="gap_s:reps,... (seconds idle before the first call)")
    ap.add_argument("--warm-k", type=int, default=5)
    ap.add_argument("--warmup", type=int, default=20)
    ap.add_argument("--cpu-echo", action="store_true", help="tests against a local stand-in: skip the window check")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    C.refuse_modal(a.url)
    port = urlparse(a.url).port
    if port:
        C.refuse_prod_port(port, "the keep-alive probe")
    window = None if a.cpu_echo else C.require_window()
    res = run(a)
    n = sum(v["n"] for v in res["gaps"].values())
    res.update({"window": window, "utc": C.utc(), "url_host": urlparse(a.url).hostname,
                "tag": C.tag("author-run", n=n, source=f"keepalive_probe.py {a.gaps}")})
    C.write_json(a.out, res)
    return 0


if __name__ == "__main__":
    sys.exit(main())
