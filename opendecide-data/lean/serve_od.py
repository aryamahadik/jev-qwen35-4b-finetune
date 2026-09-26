"""OpenDecide as an HTTP decision API on one Modal L4 GPU (Jev-style request: one state + named typed questions).

  modal deploy serve_od.py            -> prints the endpoint URL
  POST {"state": "...", "questions": {"q0": {"type": "noul", "instructions": "..."},
                                      "q1": {"type": "choice", "instructions": "...", "options": ["a", "b"]}}}
  -> {"answers": {"q0": {"type": "noul", "noul": 0.93}, "q1": {"type": "choice", "probabilities": {...}}}, "server_ms": ...}

Every question is its own sequence (questions never see each other); all questions of a request run as one GPU batch.
More than 24 options go through the shortlist + knockout path (hc.py). Scales to zero when idle.
"""
import time
from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent
ADAPTER = "/vol/models/q4b_v05_A3"
BASE = "Qwen/Qwen3-4B-Instruct-2507"
image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("torch==2.8.0", "transformers==4.57.6", "peft==0.17.1", "accelerate", "sentencepiece", "protobuf",
                 "sentence-transformers==5.1.1", "fastapi[standard]")
    .env({"HF_HOME": "/vol/hf", "TOKENIZERS_PARALLELISM": "false"})
    .add_local_python_source("decoder_io", "hc")
)
app = modal.App("opendecide-serve")
vol = modal.Volume.from_name("opendecide")


@app.cls(image=image, gpu="L4", volumes={"/vol": vol}, secrets=[modal.Secret.from_name("opendecide-keys")],
         scaledown_window=300, timeout=600, max_containers=1)
class Decider:
    @modal.enter()
    def load(self):
        import json

        import decoder_io
        import hc
        self.dio, self.hc = decoder_io, hc
        model, self.tok = decoder_io.load(BASE, "cuda", adapter=ADAPTER)
        self.model = model.merge_and_unload().eval()
        self.ro = decoder_io.Readout(self.tok)
        self.sl = hc.Shortlister("Alibaba-NLP/gte-modernbert-base")
        T = json.loads(Path("/vol/models/q4b_v05_A3/calibration.json").read_text()) if Path(
            "/vol/models/q4b_v05_A3/calibration.json").exists() else {"noul": 1.0, "choice": 1.0}
        self.T = T

    @modal.fastapi_endpoint(method="POST")
    def decide(self, req: dict):
        import torch
        t0 = time.perf_counter()
        state, qs = req["state"], req["questions"]
        small, big = [], []
        for k, q in qs.items():
            row = {"state": state, "instructions": q["instructions"], "qtype": q["type"], "options": q.get("options")}
            (big if q["type"] == "choice" and len(q["options"]) > 24 else small).append((k, row))
        answers = {}
        with torch.no_grad():
            if small:
                lg = self.dio.cand_logits(self.model, self.ro, [r for _, r in small], "cuda")
                for (k, r), l in zip(small, lg):
                    p = self.dio.to_probs(r, l, temp=self.T[r["qtype"]])
                    answers[k] = {"type": "noul", "noul": p["yes"]} if r["qtype"] == "noul" else {"type": "choice", "probabilities": p}
            for k, r in big:
                p, _ = self.hc.choose_many(self.model, self.tok, r, "cuda", chunk=24, keep=4, shortlist=self.sl, k=64)
                answers[k] = {"type": "choice", "probabilities": p}
        torch.cuda.synchronize()
        return {"answers": answers, "server_ms": (time.perf_counter() - t0) * 1000}
