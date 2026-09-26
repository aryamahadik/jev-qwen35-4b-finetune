"""End-to-end latency, API against API: our single model behind a direct Modal tunnel (modal.forward), speaking a
TypeSafe-style decision API, answering the SAME 515 bundled eval requests Jev answered (data/eval_calls.jsonl),
sent sequentially from this laptop over one keep-alive connection. Also returns predictions (accuracy parity check).

  modal run serve_tunnel.py --name ADAPTER --mode plain|system [--gpu L40S] [--seconds 900]
Writes preds/<name>_tunnel_<mode>.jsonl and logs/tunnel_<name>_<mode>.json.
"""
import json
import random
import statistics
import time
from pathlib import Path

import modal

from modal_od import SECRETS, image35, vol

HERE = Path(__file__).resolve().parent
app = modal.App("opendecide-tunnel")
image = image35.add_local_python_source("modal_od")  # the container imports this file, which imports modal_od


@app.function(image=image, gpu="L40S", volumes={"/vol": vol}, secrets=SECRETS, timeout=3600)
def serve(q: modal.Queue, name: str, base: str, mode: str, seconds: int, temps: dict, style: str = "cygnet",
          robust: dict | None = None):
    import math
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    import torch
    import decoder_io
    decoder_io.STYLE = style
    model, tok = decoder_io.load(base, "cuda", adapter=f"/vol/models/{name}" if name else None)
    if name:
        model = model.merge_and_unload()
    model.eval()
    ro = decoder_io.Readout(tok)
    lock = threading.Lock()

    def temper(qt, pr):
        T = temps.get("noul" if qt == "noul" else "choice", 1.0)
        z = {k: math.exp(math.log(max(v, 1e-12)) / T) for k, v in pr.items()}
        s_ = sum(z.values())
        return {k: v / s_ for k, v in z.items()}

    def decide(req):
        rows = []
        for k, qq in req["questions"].items():
            rows.append((k, {"state": req["state"], "instructions": qq["instructions"], "qtype": qq["type"],
                             "options": qq.get("options")}))
        with lock, torch.no_grad():
            if mode == "system":  # two-stage: extra variants only when a segment looks like a planted claim
                res = {k: decoder_io.robust_probs(model, ro, r, "cuda", **(robust or {}))[0] for k, r in rows}
            else:
                lg = decoder_io.cand_logits(model, ro, [r for _, r in rows], "cuda")
                res = {k: decoder_io.to_probs(r, l) for (k, r), l in zip(rows, lg)}
            torch.cuda.synchronize()
        return {k: temper(r["qtype"], res[k]) for k, r in rows}

    t0 = time.time()  # start-up: compile/autotune every length bucket (filler text, no eval data)
    decoder_io.warmup(model, ro, max_tokens=4096, batch_sizes=(1, 2, 3, 4, 6, 8, 12, 16))
    decoder_io.GRAPHS = decoder_io.GraphRunner(model, tok, batches=(1, 2, 4, 8))  # CUDA graphs, captured at start-up
    decoder_io.GRAPHS.capture_all(max_tokens=1024)  # requests here are short; longer shapes use the eager path
    print(f"warm-up {time.time() - t0:.0f}s")
    for _ in range(3):
        decide({"state": "warm up", "questions": {"q": {"type": "noul", "instructions": "Is this a test?"}}})

    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_POST(self):
            n = int(self.headers.get("content-length", 0))
            t = time.perf_counter()
            ans = decide(json.loads(self.rfile.read(n)))
            body = json.dumps({"answers": ans, "server_ms": (time.perf_counter() - t) * 1000}).encode()
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


@app.local_entrypoint()
def main(name: str = "", base: str = "Qwen/Qwen3.5-4B", mode: str = "plain", seconds: int = 900, gpu: str = "L40S",
         temps: str = "1.0,1.0", robust: str = ""):
    import httpx
    tn, tc = (float(x) for x in temps.split(","))
    rows = {json.loads(l)["id"]: json.loads(l) for l in open(HERE / "data/eval.jsonl")}
    calls = [json.loads(l) for l in open(HERE / "data/eval_calls.jsonl")]
    with modal.Queue.ephemeral() as q:
        call = serve.with_options(gpu=gpu).spawn(q, name, base, mode, seconds, {"noul": tn, "choice": tc}, "cygnet",
                                                 json.loads(robust) if robust else None)
        url = q.get(timeout=1200)
        out, lat, srv = [], [], []
        with httpx.Client(timeout=120) as c:
            for _ in range(3):
                c.post(url, json={"state": "warm", "questions": {"q": {"type": "noul", "instructions": "ok?"}}})
            for cl in calls:
                rid = list(cl["row_ids"])
                random.Random(cl["call_id"]).shuffle(rid)  # same seeded question order as run_jev.py
                qmap = {f"q{i}": r for i, r in enumerate(rid)}
                qs = {k: {"type": rows[v]["qtype"], "instructions": rows[v]["instructions"], "options": rows[v]["options"]}
                      for k, v in qmap.items()}
                t = time.perf_counter()
                res = c.post(url, json={"state": cl["state"], "questions": qs}).json()
                ms = (time.perf_counter() - t) * 1000
                lat.append(ms)
                srv.append(res["server_ms"])
                for k, rid_ in qmap.items():
                    out.append({"id": rid_, "model": f"{name}_tunnel_{mode}", "probs": res["answers"][k], "latency_ms": ms})
        call.cancel()
    label = f"{name or base.split('/')[-1]}_tunnel_{mode}"
    (HERE / f"preds/{label}.jsonl").write_text("".join(json.dumps(o) + "\n" for o in out))
    s = sorted(lat)
    stats = {"calls": len(lat), "client_median_ms": round(statistics.median(lat), 1), "client_p95_ms": round(s[int(0.95 * len(s))], 1),
             "server_median_ms": round(statistics.median(srv), 1), "server_p95_ms": round(sorted(srv)[int(0.95 * len(srv))], 1),
             "gpu": gpu, "mode": mode, "note": "same laptop/network and same 515 bundled requests as the Jev run (Jev median 203 ms)"}
    (HERE / f"logs/tunnel_{label}.json").write_text(json.dumps(stats, indent=1))
    print(json.dumps(stats, indent=1))
