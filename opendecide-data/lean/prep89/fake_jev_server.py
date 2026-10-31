"""A LOCAL fake of TypeSafe's System One endpoint (POST /v1/systemone) for the CPU dry run. No network beyond
127.0.0.1. It answers only the SYNTHETIC stand-in (it reads its gold labels to plant a known accuracy) and refuses the
real OHS-3 file.

  ../.venv/bin/python prep89/fake_jev_server.py --root prep89/dryrun/root --port 0   (prints its URL)

Behaviour: the response model id is the pinned "typesafe/jev-1.13-20260917"; usage.input_tokens = request bytes / 4;
a seeded share of requests fails with HTTP 503 (the SDK and run_jev.py retry them); --hard-fail-calls N calls fail
their first 14 requests (more than run_jev.py's 4 attempts x 3 SDK tries), so a first run_jev.py pass leaves them
unanswered and the collector's resume pass must pick them up. Each repeat of the same question gets a fresh noise
draw (run 1, run 2 and the timing pass differ a little, like Jev's run-to-run noise).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import threading
import time
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ohs3_lib as L  # noqa: E402


class FakeJev:
    def __init__(self, root, acc_noul=0.93, acc_choice=0.78, fail_rate=0.01, hard_fail_calls=3, latency_ms=(15, 45),
                 seed=7):
        L.require_synthetic(root)
        self.rows = {r["id"]: r for r in L.read_jsonl(Path(root) / "data" / "ohs3.jsonl")}
        self.by_state = {}
        for r in self.rows.values():
            self.by_state.setdefault(r["state"], []).append(r)
        calls = sorted(L.read_jsonl(Path(root) / "data" / "ohs3_calls.jsonl"), key=lambda c: c["call_id"])
        rnd = random.Random(seed)
        self.hard = {c["state"] for c in rnd.sample(calls, hard_fail_calls)} if hard_fail_calls else set()
        self.acc = {"noul": acc_noul, "choice": acc_choice}
        self.fail_rate, self.lat, self.seed = fail_rate, latency_ms, seed
        self.seen = Counter()
        self.lock = threading.Lock()
        self.stats = Counter()
        self.fail_left = {}  # state -> the next N requests for it fail (dry run: forces the timing harness's refill)

    def fail_next(self, states, n):
        with self.lock:
            for st in states:
                self.fail_left[st] = n

    def _row(self, state, q):
        cands = self.by_state.get(state, [])
        if q["type"] == "choice":
            opts = list(q["criteria"])
            m = [r for r in cands if r["qtype"] == "choice" and r["options"] == opts]
        else:
            ins = q["instructions"] if isinstance(q["instructions"], str) else ""
            m = [r for r in cands if r["qtype"] == "noul" and r["instructions"] in ins]
            m.sort(key=lambda r: -len(r["instructions"]))  # the twin's instructions contain the base's
        return m[0] if m else None  # None: a warm-up (dev) question, answered without gold

    def answer(self, body):
        state = body["state"]
        key = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
        with self.lock:
            self.seen[key] += 1
            n = self.seen[key]
            self.stats["requests"] += 1
        with self.lock:
            left = self.fail_left.get(state, 0)
            if left > 0:
                self.fail_left[state] = left - 1
        if left > 0:
            self.stats["injected_fail"] += 1
            return 503, {"error": "fake injected failure"}
        if state in self.hard and n <= 14:
            self.stats["hard_fail"] += 1
            return 503, {"error": "fake hard failure"}
        rnd = random.Random(f"{self.seed}:{key}:{n}")
        if rnd.random() < self.fail_rate:
            self.stats["random_fail"] += 1
            return 503, {"error": "fake transient failure"}
        time.sleep(rnd.uniform(*self.lat) / 1000)
        answers = {}
        for name, q in body["questions"].items():
            r = self._row(state, q)
            if r is None:
                self.stats["unknown_question"] += 1
                if q["type"] == "noul":
                    answers[name] = {"type": "noul", "noul": 0.7}
                else:
                    o = list(q["criteria"])
                    answers[name] = {"type": "choice", "choice": o[0], "confidence": 1 / len(o),
                                     "probabilities": {x: 1 / len(o) for x in o}}
                continue
            rr = random.Random(f"{self.seed}:{r['id']}:{n}")
            right = rr.random() < self.acc[r["qtype"]]
            if r["qtype"] == "noul":
                truth = r["gold"] if right else 1 - r["gold"]
                conf = rr.uniform(0.6, 0.99)
                answers[name] = {"type": "noul", "noul": conf if truth == 1 else 1 - conf}
            else:
                opts = list(q["criteria"])
                pick = r["gold"] if right else rr.choice([o for o in opts if o != r["gold"]])
                rest = (1 - 0.6) / (len(opts) - 1)
                probs = {o: (0.6 if o == pick else rest) for o in opts}
                answers[name] = {"type": "choice", "choice": pick, "confidence": 0.6, "probabilities": probs}
        nbytes = len(json.dumps(body))
        return 200, {"model": L.PINNED_JEV, "answers": answers, "usage": {"input_tokens": nbytes // 4, "output_tokens": 0}}


def make_server(fake, port=0):
    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)))
            if self.path.rstrip("/") != "/v1/systemone":
                code, out = 404, {"error": "not found"}
            else:
                try:
                    code, out = fake.answer(body)
                except KeyError as e:
                    code, out = 422, {"detail": [{"loc": ["body"], "msg": str(e), "type": "value_error"}]}
            b = json.dumps(out).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b)))
            self.send_header("x-typesafe-request-id", hashlib.sha1(b).hexdigest()[:16])
            self.end_headers()
            self.wfile.write(b)

        def log_message(self, *a):
            pass

    class S(ThreadingHTTPServer):
        daemon_threads = True
        allow_reuse_address = True

    srv = S(("127.0.0.1", port), H)
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"


def start_in_thread(root, **kw):
    fake = FakeJev(root, **kw)
    srv, url = make_server(fake)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, url, fake


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--port", type=int, default=0)
    ap.add_argument("--hard-fail-calls", type=int, default=3)
    a = ap.parse_args()
    fake = FakeJev(a.root, hard_fail_calls=a.hard_fail_calls)
    srv, url = make_server(fake, a.port)
    print(json.dumps({"url": url}), flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    print(json.dumps(dict(fake.stats)), flush=True)


if __name__ == "__main__":
    main()
