"""How much latency is Modal networking (not the model)? CPU-only echo servers, no GPU cost.

  A) the standard Modal web endpoint (fastapi_endpoint), as used by serve_od.py
  B) a direct tunnel into the container (modal.forward), which bypasses the web-endpoint layer
Both answer a JSON POST with a tiny JSON body. Run: modal run latency_probe.py
"""
import json
import statistics
import time

import modal

app = modal.App("opendecide-latency-probe")
image = modal.Image.debian_slim(python_version="3.12").pip_install("fastapi[standard]", "httpx")


@app.function(image=image, scaledown_window=120, min_containers=0)
@modal.fastapi_endpoint(method="POST")
def echo(req: dict):
    return {"ok": True, "n": len(json.dumps(req))}


@app.function(image=image, timeout=600)
def tunnel_server(q: modal.Queue, seconds: int = 120):
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_POST(self):
            n = int(self.headers.get("content-length", 0))
            self.rfile.read(n)
            body = b'{"ok": true}'
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *a):
            pass

    srv = ThreadingHTTPServer(("0.0.0.0", 8000), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    with modal.forward(8000) as tunnel:
        q.put(tunnel.url)
        time.sleep(seconds)


def bench(url, n=40):
    import httpx
    payload = {"state": "x" * 2000, "questions": {"q": {"type": "noul", "instructions": "Is this a test?"}}}
    with httpx.Client(timeout=60) as c:
        for _ in range(3):
            c.post(url, json=payload)
        ts = []
        for _ in range(n):
            t = time.perf_counter()
            c.post(url, json=payload)
            ts.append((time.perf_counter() - t) * 1000)
    ts.sort()
    return {"median_ms": round(statistics.median(ts), 1), "p95_ms": round(ts[int(0.95 * len(ts))], 1), "min_ms": round(ts[0], 1)}


@app.local_entrypoint()
def main():
    out = {"web_endpoint": bench(echo.get_web_url())}
    with modal.Queue.ephemeral() as q:
        call = tunnel_server.spawn(q, 120)
        url = q.get(timeout=120)
        out["direct_tunnel"] = bench(url)
        call.cancel()
    print(json.dumps(out, indent=1))
