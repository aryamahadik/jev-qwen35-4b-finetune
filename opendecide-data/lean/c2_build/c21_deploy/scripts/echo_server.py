"""echo_server.py: a model-free stand-in for our /decide endpoint, to measure the NETWORK FLOOR to a region (stdlib only).

Run it on a small CPU VM in a candidate zone (free credit, no GPU quota) and point region_latency.py at it. It answers
  GET  /health            -> 200 "ok"
  POST /decide (any path) -> reads the whole body, waits --delay-ms, returns JSON of about --resp-bytes with "server_ms"
so a request has the size of a real decision (a few KB up, ~0.6 KB down) and the client's timing path is the one used for the
real server. It is NOT a model and its numbers are network + HTTP-stack only; add the measured batch-1 server time of the real
box to get an estimate (region_latency.py does that and tags it modelled), then validate on the real endpoint.

  echo_server.py --port 8080 [--token T] [--resp-bytes 600] [--delay-ms 0] [--bind 0.0.0.0]
SAFETY: bind to the VM's internal address and open the firewall to the client's IP only; --token makes it require
"Authorization: Bearer T". It logs nothing about request bodies.
"""
from __future__ import annotations

import argparse
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def make_server(port=0, bind="127.0.0.1", token=None, resp_bytes=600, delay_ms=0.0):
    pad = "x" * max(0, resp_bytes - 120)

    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        disable_nagle_algorithm = True

        def log_message(self, *a):
            pass

        def _send(self, code, payload: bytes, ctype="application/json"):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def _auth(self):
            if token and self.headers.get("Authorization") != f"Bearer {token}":
                self._send(401, b'{"error":"unauthorised"}')
                return False
            return True

        def do_GET(self):
            if self.path == "/health":
                self._send(200, b"ok", "text/plain")
            else:
                self._send(404, b"{}")

        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            self.rfile.read(n)
            if not self._auth():
                return
            t0 = time.perf_counter()
            if delay_ms:
                time.sleep(delay_ms / 1000.0)
            body = json.dumps({"answers": {"q0": {"type": "noul", "noul": 0.5}}, "pad": pad,
                               "server_ms": round((time.perf_counter() - t0) * 1000.0, 3), "engine": "echo"}).encode()
            self._send(200, body)

    srv = ThreadingHTTPServer((bind, port), H)
    srv.daemon_threads = True
    return srv


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--bind", default="127.0.0.1")
    ap.add_argument("--token")
    ap.add_argument("--resp-bytes", type=int, default=600)
    ap.add_argument("--delay-ms", type=float, default=0.0)
    a = ap.parse_args(argv)
    srv = make_server(a.port, a.bind, a.token, a.resp_bytes, a.delay_ms)
    print(f"echo server on {a.bind}:{srv.server_address[1]}", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
