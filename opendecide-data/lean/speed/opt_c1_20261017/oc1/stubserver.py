"""oc1.stubserver: a model-free stand-in for SGLang's /generate and /v1/score (stdlib only), for CPU dry runs in the container.

Logprobs are a deterministic pseudo-random function of (token ids, candidate id), normalised over the candidate set so
that apply_softmax scores sum to 1. It is NOT a model: it exists to prove that the real runner / front / load client run
in the real image (imports, versions, paths, tokenizer, JSON shapes) and to measure the CPU ceiling of the Python side
(tokenize + render + JSON + HTTP) with a zero-cost "GPU": whatever QPS the front cannot reach here, no GPU can fix.
"""
from __future__ import annotations

import hashlib
import json
import math
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def _lp(ids, cand):
    h = hashlib.blake2b(repr((len(ids), ids[-8:], ids[:8])).encode(), digest_size=16).digest()
    seed = int.from_bytes(h[:8], "little")
    out = []
    for t in cand:
        x = (seed ^ (t * 0x9E3779B97F4A7C15)) & 0xFFFFFFFFFFFFFFFF
        x = (x ^ (x >> 29)) * 0xBF58476D1CE4E5B9 & 0xFFFFFFFFFFFFFFFF
        out.append(-8.0 + 6.0 * ((x >> 11) / float(1 << 53)))
    return out


class StubSGLang:
    def __init__(self, port=0, service_ms=0.0, host="127.0.0.1"):
        self.service = service_ms / 1000.0
        self.calls = {"generate": 0, "score": 0, "seqs": 0, "flush": 0}
        self.lock = threading.Lock()
        me = self

        class H(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"
            disable_nagle_algorithm = True

            def _send(self, code, obj, text=False):
                b = obj.encode() if text else json.dumps(obj).encode()
                self.send_response(code)
                self.send_header("Content-Type", "text/plain" if text else "application/json")
                self.send_header("Content-Length", str(len(b)))
                self.end_headers()
                self.wfile.write(b)

            def do_GET(self):
                if self.path == "/health":
                    self._send(200, "", True)
                elif self.path in ("/server_info", "/get_server_info"):
                    self._send(200, {"version": "0.5.20-stub"})
                else:
                    self._send(404, {})

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
                if me.service:
                    time.sleep(me.service)
                if self.path == "/generate":
                    out = []
                    for i, (ids, cand) in enumerate(zip(body["input_ids"], body["token_ids_logprob"])):
                        lp = _lp(ids, cand)
                        out.append({"text": "", "meta_info": {"id": (body.get("rid") or [None] * 999)[i], "prompt_tokens": len(ids),
                                                              "completion_tokens": 0, "cached_tokens": 0, "e2e_latency": me.service,
                                                              "output_token_ids_logprobs": [[[lp[k], int(t), None] for k, t in enumerate(cand)]]}})
                    with me.lock:
                        me.calls["generate"] += 1
                        me.calls["seqs"] += len(out)
                    self._send(200, out)
                elif self.path == "/v1/score":
                    rows = []
                    for it in body["items"]:
                        lp = _lp(body["query"] + it, body["label_token_ids"])
                        m = max(lp)
                        e = [math.exp(x - m) for x in lp]
                        z = sum(e)
                        rows.append([x / z for x in e])
                    with me.lock:
                        me.calls["score"] += 1
                    self._send(200, {"scores": rows, "usage": {"prompt_tokens": 0}})
                elif self.path == "/flush_cache":
                    with me.lock:
                        me.calls["flush"] += 1
                    self._send(200, "ok", True)
                else:
                    self._send(200, "", True)

            def log_message(self, *a):
                pass

        class S(ThreadingHTTPServer):
            daemon_threads = True
            request_queue_size = 512

        self.httpd = S((host, port), H)
        self.port = self.httpd.server_address[1]
        self.url = f"http://{host}:{self.port}"
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def start(self):
        self.thread.start()
        return self

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()
