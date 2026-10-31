"""region_latency.py (M6): the region / hosting-near-users latency table, measured by OUR client, same conditions for every endpoint.

Method (what makes the table comparable and honest):
  * one table per VANTAGE (a client location we control: this laptop; a free-credit CPU VM in another zone). The label and a
    free-text note are recorded, no IP lookup. "Near the users" is then read off the vantage that stands for the users; which
    vantage that is, is the owner's input (assumed), not ours.
  * endpoints are of two kinds: `echo` (echo_server.py on a CPU VM: the network floor, model-free) and `decide` (the real
    server: network + server). Both are measured with the same code path: one keep-alive connection per endpoint, TCP_NODELAY,
    concurrency 1, and the calls of all endpoints INTERLEAVED in a seeded random order so that drift (time of day, Wi-Fi) hits
    every endpoint alike. Warm-up calls are discarded. Percentiles are nearest rank. A failed call is counted, never dropped.
  * connection setup is measured separately on --n-conn fresh connections per endpoint (DNS, TCP connect, TLS handshake): a
    client that does not keep connections alive pays this on every call (about 194 ms on the 17 Oct Modal path).
  * network_ms = client_ms - server_ms, with server_ms read from the response (echo: ~0; decide: the server's own timing).
  * e2e estimate for an echo endpoint = its network p50 + the model server's batch-1 p50 (--server-p50-ms, author-run from the
    batch-1 measurement); tagged MODELLED. It is replaced by the measured `decide` number as soon as a real endpoint exists
    there. The Jev comparison is NOT done here: client_bench.py interleaves ours and Jev from the same client (a paid API call,
    run by the orchestrator, not by this script).
  * nothing here calls a model; `decide` mode sends dev requests (speed/workloads/N.jsonl), never OHS data; Modal hosts are refused.

  region_latency.py run   --endpoints inputs/endpoints.json --vantage laptop --note "home Wi-Fi" --n 200 --warm 20 --out out/region_laptop.json
  region_latency.py table --results out/region_*.json --out out/region_table.md [--server-p50-ms 30 --server-n 640]
Endpoints file: {"endpoints": [{"name","region","provider","kind":"echo|decide","url","path":"/decide","token_env":"VAR"}]}
"""
from __future__ import annotations

import argparse
import http.client
import json
import os
import platform
import random
import socket
import ssl
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

WORKLOAD = C.LEAN / "speed" / "workloads" / "N.jsonl"


class Ep:
    def __init__(self, spec):
        self.spec = spec
        self.name, self.region, self.kind = spec["name"], spec.get("region"), spec.get("kind", "echo")
        u = urlparse(spec["url"])
        self.scheme, self.host = u.scheme, u.hostname
        self.port = u.port or (443 if u.scheme == "https" else 80)
        self.path = spec.get("path") or ("/decide" if self.kind != "health" else "/health")
        tok = os.environ.get(spec["token_env"]) if spec.get("token_env") else None
        self.headers = {"Content-Type": "application/json", **({"Authorization": f"Bearer {tok}"} if tok else {})}
        self.conn = None
        C.refuse_modal(spec["url"])

    def open(self):
        cls = http.client.HTTPSConnection if self.scheme == "https" else http.client.HTTPConnection
        self.conn = cls(self.host, self.port, timeout=30)
        self.conn.connect()
        self.conn.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    def call(self, body: bytes):
        """-> (ok, client_ms, server_ms|None, reconnected)"""
        re = False
        for attempt in (0, 1):
            try:
                if self.conn is None:
                    self.open()
                t0 = time.perf_counter()
                self.conn.request("POST", self.path, body=body, headers=self.headers)
                r = self.conn.getresponse()
                data = r.read()
                ms = (time.perf_counter() - t0) * 1000.0
                srv = None
                try:
                    srv = float(json.loads(data).get("server_ms"))
                except (ValueError, TypeError, AttributeError):
                    pass
                return r.status == 200, ms, srv, re
            except (http.client.RemoteDisconnected, ConnectionResetError, BrokenPipeError, http.client.CannotSendRequest, OSError):
                self.conn = None
                if attempt:
                    return False, None, None, True
                re = True
        return False, None, None, re


def conn_setup(ep: Ep, n: int) -> dict:
    dns, tcp, tls = [], [], []
    for _ in range(n):
        try:
            t0 = time.perf_counter()
            ai = socket.getaddrinfo(ep.host, ep.port, type=socket.SOCK_STREAM)[0]
            t1 = time.perf_counter()
            s = socket.create_connection(ai[4][:2], timeout=10)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            t2 = time.perf_counter()
            if ep.scheme == "https":
                ss = ssl.create_default_context().wrap_socket(s, server_hostname=ep.host)
                tls.append((time.perf_counter() - t2) * 1000.0)
                ss.close()
            else:
                s.close()
            dns.append((t1 - t0) * 1000.0)
            tcp.append((t2 - t1) * 1000.0)
        except OSError:
            pass
    return {"dns_ms": C.summarize(dns), "tcp_connect_ms": C.summarize(tcp), "tls_ms": C.summarize(tls)}


def requests_for(kind: str, count: int, seed: int) -> list:
    if kind == "echo":
        return [json.dumps({"state": "x" * 2000, "questions": {"q0": {"type": "noul", "instructions": "x" * 100}}}).encode()]
    items = C.read_jsonl(WORKLOAD)
    rng = random.Random(seed)
    rng.shuffle(items)
    return [json.dumps(it["request"]).encode() for it in items[:count]]


def run(a) -> dict:
    spec = json.loads(Path(a.endpoints).read_text())["endpoints"]
    eps = [Ep(s) for s in spec if a.only in (None, s["name"])]
    rng = random.Random(a.seed)
    bodies = {e.name: requests_for(e.kind, a.n + a.warm, a.seed) for e in eps}
    setup = {e.name: conn_setup(e, a.n_conn) for e in eps}
    recs = {e.name: [] for e in eps}
    order = [e for _ in range(a.n + a.warm) for e in rng.sample(eps, len(eps))]       # interleaved, seeded, per round a shuffle
    seen = {e.name: 0 for e in eps}
    for e in order:
        k = seen[e.name]
        seen[e.name] += 1
        b = bodies[e.name][k % len(bodies[e.name])]
        ok, ms, srv, re = e.call(b)
        if k >= a.warm:
            recs[e.name].append({"ok": ok, "client_ms": ms, "server_ms": srv, "reconnected": re})
    out = {}
    for e in eps:
        r = recs[e.name]
        good = [x for x in r if x["ok"] and x["client_ms"] is not None]
        net = [x["client_ms"] - (x["server_ms"] or 0.0) for x in good]
        out[e.name] = {"region": e.region, "provider": e.spec.get("provider"), "kind": e.kind, "host": e.host,
                       "calls": len(r), "ok": len(good), "failed": len(r) - len(good), "reconnects": sum(x["reconnected"] for x in r),
                       "client_ms": C.summarize([x["client_ms"] for x in good]),
                       "server_ms": C.summarize([x["server_ms"] for x in good if x["server_ms"] is not None]),
                       "network_ms": C.summarize(net), "setup": setup[e.name],
                       "tag": C.tag("author-run", n=len(good), source=f"region_latency.py vantage {a.vantage}") if good else C.tag("not-measured")}
    return out


def table(results: list, server_p50: float | None, server_n: int | None) -> str:
    vantages = [r["vantage"] for r in results]
    names = []
    for r in results:
        for n in r["endpoints"]:
            if n not in names:
                names.append(n)
    L = ["# Region latency table (region_latency.py)", "",
         "Network p50 / p95 in ms (client - server, concurrency 1, keep-alive, interleaved), n calls per cell. "
         "echo = network floor only; decide = real server."]
    if server_p50 is not None:
        L.append(f"Estimated e2e p50 = network p50 + model server batch-1 p50 {server_p50} ms (author-run n={server_n}); tag MODELLED for echo rows.")
    L.append("")
    hdr = ["endpoint", "region", "kind"] + [f"{v}: net p50 / p95 (n)" for v in vantages]
    if server_p50 is not None:
        hdr += [f"{v}: est. e2e p50 (modelled)" for v in vantages]
    rows = []
    for n in names:
        first = next(r["endpoints"][n] for r in results if n in r["endpoints"])
        row = [n, first["region"], first["kind"]]
        est = []
        for r in results:
            e = r["endpoints"].get(n)
            if not e or not e["network_ms"].get("n"):
                row.append("-")
                est.append("-")
                continue
            row.append(f"{e['network_ms']['p50']} / {e['network_ms']['p95']} ({e['ok']})")
            est.append(round(e["network_ms"]["p50"] + (server_p50 or 0), 1) if (server_p50 is not None and e["kind"] == "echo") else
                       (e["client_ms"]["p50"] if e["kind"] == "decide" else "-"))
        rows.append(row + (est if server_p50 is not None else []))
    L += [C.md_table(hdr, rows), "", "Connection setup (fresh connection, p50 ms): dns / tcp connect / tls", ""]
    srows = []
    for n in names:
        row = [n]
        for r in results:
            e = r["endpoints"].get(n)
            row.append("-" if not e else " / ".join(str(e["setup"][k].get("p50", "-")) for k in ("dns_ms", "tcp_connect_ms", "tls_ms")))
        srows.append(row)
    L += [C.md_table(["endpoint"] + vantages, srows), ""]
    best = []
    for r in results:
        cand = [(e["network_ms"]["p50"], n) for n, e in r["endpoints"].items() if e["network_ms"].get("n")]
        best.append(f"{r['vantage']}: {min(cand)[1]} ({min(cand)[0]} ms)" if cand else f"{r['vantage']}: -")
    L += ["Lowest network p50 per vantage: " + "; ".join(best)]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--endpoints", default=str(C.ROOT / "inputs" / "endpoints.json"))
    r.add_argument("--vantage", required=True)
    r.add_argument("--note", default="")
    r.add_argument("--n", type=int, default=200)
    r.add_argument("--warm", type=int, default=20)
    r.add_argument("--n-conn", type=int, default=10)
    r.add_argument("--seed", type=int, default=0)
    r.add_argument("--only")
    r.add_argument("--out", required=True)
    t = sub.add_parser("table")
    t.add_argument("--results", nargs="+", required=True)
    t.add_argument("--server-p50-ms", type=float)
    t.add_argument("--server-n", type=int)
    t.add_argument("--out")
    a = ap.parse_args(argv)
    if a.cmd == "run":
        res = {"vantage": a.vantage, "note": a.note, "utc": C.utc(), "client": {"python": platform.python_version(), "platform": platform.platform()},
               "n": a.n, "warm": a.warm, "seed": a.seed, "endpoints": run(a)}
        C.write_json(a.out, res)
        for n, e in res["endpoints"].items():
            print(f"{n}: ok {e['ok']}/{e['calls']} net p50 {e['network_ms'].get('p50')} p95 {e['network_ms'].get('p95')} client p50 {e['client_ms'].get('p50')}")
        return 0
    results = [json.loads(Path(p).read_text()) for p in a.results]
    if a.server_p50_ms is not None and not a.server_n:
        raise SystemExit("--server-p50-ms needs --server-n (the n of the author-run batch-1 measurement it comes from)")
    md = table(results, a.server_p50_ms, a.server_n)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(md)
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
