"""Serialise OpenDecide rows for GLiClass uni-encoders and score them.

One row = one forward pass input (rows are never packed next to a related row).
  Noul:   <<LABEL>>{instructions}<<SEP>>{state}                 -> sigmoid(logit_0)
  Choice: <<LABEL>>{opt_1}...<<LABEL>>{opt_K}<<SEP>>{instructions}\n{state} -> softmax(logits[:K])
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import torch
from gliclass import GLiClassModel
from transformers import AutoTokenizer

MAX_LEN = 512


def device():
    return torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")


def serialize(row) -> tuple[str, int]:
    if row["qtype"] == "noul":
        labels, prompt = [row["instructions"]], ""
    else:
        labels, prompt = row["options"], row["instructions"] + "\n"
    return "".join(f"<<LABEL>>{l}" for l in labels) + "<<SEP>>" + prompt + row["state"], len(labels)


def load(path_or_id, dev=None):
    dev = dev or device()
    model = GLiClassModel.from_pretrained(path_or_id).to(dev)
    tok = AutoTokenizer.from_pretrained(path_or_id)
    return model, tok


def forward_logits(model, tok, rows, dev):
    texts, ks = zip(*[serialize(r) for r in rows])
    enc = tok(list(texts), truncation=True, max_length=MAX_LEN, padding="longest", return_tensors="pt").to(dev)
    out = model(input_ids=enc["input_ids"], attention_mask=enc["attention_mask"], max_num_classes=max(ks))
    return out.logits, list(ks)


def to_probs(row, logit_row, k):
    if row["qtype"] == "noul":
        p = torch.sigmoid(logit_row[0]).item()
        return {"yes": p, "no": 1 - p}
    pr = torch.softmax(logit_row[:k], dim=-1).tolist()
    return dict(zip(row["options"], pr))


@torch.no_grad()
def predict(model, tok, rows, batch_size=32, dev=None):
    dev = dev or device()
    model.eval()
    order = sorted(range(len(rows)), key=lambda i: len(rows[i]["state"]) + 20 * len(rows[i]["options"] or []))
    preds = [None] * len(rows)
    for s in range(0, len(order), batch_size):
        idx = order[s:s + batch_size]
        batch = [rows[i] for i in idx]
        logits, ks = forward_logits(model, tok, batch, dev)
        logits = logits.float().cpu()
        for j, i in enumerate(idx):
            preds[i] = to_probs(rows[i], logits[j], ks[j])
    return preds


@torch.no_grad()
def latency(model, tok, rows, dev, n=200):
    """Median / p95 ms per single-row forward pass (batch size 1)."""
    model.eval()
    ts = []
    for r in rows[: n + 10]:
        t = time.perf_counter()
        logits, _ = forward_logits(model, tok, [r], dev)
        if dev.type == "mps":
            torch.mps.synchronize()
        ts.append((time.perf_counter() - t) * 1000)
    ts = sorted(ts[10:])
    return {"device": dev.type, "median_ms": ts[len(ts) // 2], "p95_ms": ts[int(len(ts) * 0.95)], "n": len(ts)}


def read_jsonl(p):
    return [json.loads(l) for l in open(p)]


def write_preds(path, rows, preds, model_name):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for r, p in zip(rows, preds):
            f.write(json.dumps({"id": r["id"], "model": model_name, "probs": p}) + "\n")
