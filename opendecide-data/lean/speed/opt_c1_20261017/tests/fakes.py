"""A fake SGLang for CPU tests: /generate (prefill-only logprobs at the requested ids), /v1/score (label_token_ids +
apply_softmax over the labels only), /flush_cache, /abort_request, /health, /server_info. Logits come from a tiny random
Qwen3.5 hybrid model, so answers are real functions of the token ids (not constants)."""
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import torch

from oc1 import configs as K
from oc1 import common as C


def good_info(path="/m"):
    return {"model_path": path, "dtype": "bfloat16", "quantization": None, "enable_fp32_lm_head": True,
            "context_length": K.CONTEXT_LEN, "disable_radix_cache": False, "mamba_radix_cache_strategy": "extra_buffer",
            "mamba_ssm_dtype": "float32", "linear_attn_backend": "triton", "linear_attn_prefill_backend": "triton",
            "speculative_algorithm": None, "sampling_defaults": "openai", "random_seed": 0, "max_running_requests": 64,
            "max_mamba_cache_size": 400, "version": C.SGLANG_VERSION, "enable_lora": False, "lora_paths": None}


class FakeSGLangServer:
    def __init__(self, model, delay_ms=0.0, page=64):
        self.model, self.delay, self.page = model, delay_ms / 1000.0, page
        self.calls = {"generate": 0, "score": 0, "flush": 0, "seqs": 0}
        self.seen = []                # prefix cache simulation: list of id tuples
        self.lock = threading.Lock()
        self.fail_next = 0
        me = self

        class H(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

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
                    self._send(200, good_info())
                else:
                    self._send(404, {"error": "nf"})

            def do_POST(self):
                raw = self.rfile.read(int(self.headers.get("Content-Length") or 0))
                body = json.loads(raw or b"{}")
                if me.delay:
                    time.sleep(me.delay)
                if self.path == "/generate":
                    if me.fail_next > 0:
                        me.fail_next -= 1
                        self._send(500, {"error": "boom"})
                        return
                    self._send(200, me.generate(body))
                elif self.path == "/v1/score":
                    self._send(200, me.score(body))
                elif self.path == "/flush_cache":
                    with me.lock:
                        me.calls["flush"] += 1
                        me.seen.clear()
                    self._send(200, "Cache flushed.", True)
                elif self.path == "/abort_request":
                    self._send(200, "", True)
                else:
                    self._send(404, {"error": "nf"})

            def log_message(self, *a):
                pass

        class S(ThreadingHTTPServer):
            daemon_threads = True
            request_queue_size = 256

        self.httpd = S(("127.0.0.1", 0), H)
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()

    def logprobs(self, ids):
        from oc1.items import readout_mod
        dio = readout_mod().dio
        body, head = dio._parts(self.model)
        with torch.no_grad():
            h = body(input_ids=torch.tensor([ids])).last_hidden_state[0, -1]
            return torch.log_softmax(h.float() @ head.weight.float().T, -1)

    def cached(self, ids):
        best = 0
        for s in self.seen:
            n = 0
            for a, b in zip(s, ids):
                if a != b:
                    break
                n += 1
            best = max(best, n)
        c = (best // self.page) * self.page
        self.seen.append(tuple(ids))
        return c

    def generate(self, body):
        with self.lock:
            self.calls["generate"] += 1
            self.calls["seqs"] += len(body["input_ids"])
        out = []
        for i, (ids, cand) in enumerate(zip(body["input_ids"], body["token_ids_logprob"])):
            lp = self.logprobs(ids)
            trips = [[float(lp[t]), int(t), None] for t in cand]
            with self.lock:
                cached = self.cached(ids)
            out.append({"text": "", "meta_info": {"id": body.get("rid", [None] * 99)[i], "prompt_tokens": len(ids),
                                                  "completion_tokens": 0, "cached_tokens": cached, "e2e_latency": 0.002,
                                                  "output_token_ids_logprobs": [trips]}})
        return out

    def score(self, body):
        with self.lock:
            self.calls["score"] += 1
        q, items, labels = body["query"], body["items"], body["label_token_ids"]
        rows, ptok = [], 0
        for it in items:
            ids = (it + q) if body.get("item_first") else (q + it)
            lp = self.logprobs(ids)
            v = torch.tensor([float(lp[t]) for t in labels], dtype=torch.float64)
            rows.append(torch.softmax(v, 0).tolist() if body.get("apply_softmax") else v.exp().tolist())
            ptok += len(ids)
        return {"scores": rows, "model": body.get("model"), "usage": {"prompt_tokens": ptok, "total_tokens": ptok},
                "object": "scoring"}
