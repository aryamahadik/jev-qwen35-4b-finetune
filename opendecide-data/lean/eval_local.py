"""Run a local GLiClass model (zero-shot id or fine-tuned dir) on lean/data/eval.jsonl."""
import argparse
import json
from pathlib import Path

import torch

from gliclass_io import latency, load, predict, read_jsonl, write_preds

HERE = Path(__file__).resolve().parent

ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True)
ap.add_argument("--name", required=True)
ap.add_argument("--latency", action="store_true")
ap.add_argument("--split", default="eval")
a = ap.parse_args()

rows = read_jsonl(HERE / f"data/{a.split}.jsonl")
PD = "preds" if a.split == "eval" else f"preds_{a.split}"
model, tok = load(a.model)
dev = next(model.parameters()).device
preds = predict(model, tok, rows, dev=dev)
write_preds(HERE / f"{PD}/{a.name}.jsonl", rows, preds, a.name)
meta = {"model": a.model, "name": a.name, "rows": len(rows)}
if a.latency:
    sample = [r for r in rows if r["track"] in ("ID", "ZS")]
    meta["latency_mps"] = latency(model, tok, sample, dev)
    cpu = torch.device("cpu")
    model.to(cpu)
    meta["latency_cpu"] = latency(model, tok, sample, cpu, n=100)
(HERE / f"{PD}/{a.name}.meta.json").write_text(json.dumps(meta, indent=2))
print(json.dumps(meta, indent=2))
