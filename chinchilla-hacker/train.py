"""Step 2: train ONE model on a fixed compute budget and measure its loss.

Chinchilla details we copy:
  * compute is counted with the paper's Appendix F formula (flops.py);
    training tokens for a run = budget / (FLOPs per token)
  * one pass over fresh data: no character is ever seen twice
  * AdamW, with a cosine learning-rate schedule that decays 10x and ends exactly when the
    run ends. Kaplan et al. (2020) judged models part-way through one long schedule; the
    paper (Appendix B, Figure A1) shows that makes shorter runs look worse than they are.

Example:  python train.py --n_layer 3 --d_model 96 --flops 1e13
"""
import argparse
import json
import math
import os
import time

import numpy as np
import torch

from flops import train_flops_per_token
from model import GPT

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = json.load(open(os.path.join(HERE, "data", "vocab.json")))
BATCH, CTX = 64, 64  # default: 64 sequences x 64 characters = 4,096 characters per step
VAL_TOKENS = 2**19  # every model is scored on the same 524k held-out characters
RUNS = os.path.join(HERE, "runs")


def heads(d_model):
    """Attention heads: head size 16 where possible (14 or 20 for the two odd widths)."""
    return next(h for h in (d_model // 16, d_model // 14, d_model // 20, 2) if h >= 2 and d_model % h == 0)


def lr_for(d_model):
    """Peak learning rate from the lr pilot (sweep.py lr, figures/fig_lr.png): 8e-3 was best or within
    ~0.01 of best for widths up to 128; wider models went unstable there, so they get proportionally less."""
    return 8e-3 * min(1.0, 128 / d_model)


def device():
    return "mps" if torch.backends.mps.is_available() else "cpu"


class Stream:
    """Reads the training text in order, like one book with 64 bookmarks.
    Every run sees the same characters in the same order and never sees one twice."""

    def __init__(self, dev=None, batch=BATCH):
        data = np.fromfile(os.path.join(HERE, "data", "train.bin"), dtype=np.uint8)
        lane = len(data) // batch
        self.batch_size = batch
        self.lanes = torch.from_numpy(data[: batch * lane].reshape(batch, lane)).to(dev or device())
        self.max_steps = (lane - 1) // CTX

    def batch(self, step):
        chunk = self.lanes[:, step * CTX: step * CTX + CTX + 1].long()
        return chunk[:, :-1], chunk[:, 1:]


def lr_at(step, steps, max_lr, cycle=1.0):
    """Linear warmup, then cosine decay to max_lr / 10 at step `cycle * steps`.
    cycle = 1 is the paper's recipe; cycle > 1 overshoots the run (Kaplan-style)."""
    warmup = max(1, min(200, steps // 20))
    if step < warmup:
        return max_lr * (step + 1) / warmup
    progress = min(1.0, (step - warmup) / max(1, cycle * steps - warmup))
    return max_lr * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * progress)))


@torch.no_grad()
def evaluate(model, dev):
    val = np.fromfile(os.path.join(HERE, "data", "val.bin"), dtype=np.uint8, count=VAL_TOKENS + 1)
    x = torch.from_numpy(val.astype(np.int64))
    inputs, targets = x[:-1].view(-1, CTX), x[1:].view(-1, CTX)
    model.eval()
    total = 0.0
    for i in range(0, len(inputs), 512):
        total += model(inputs[i:i + 512].to(dev), targets[i:i + 512].to(dev)).item() * len(inputs[i:i + 512])
    model.train()
    return total / len(inputs)


def run(name, n_layer, d_model, n_head=None, flops=None, tokens=None, lr=2e-3, cycle=1.0, seed=0,
        batch=BATCH, stream=None, save=False, **tags):
    """Train one model for `flops` of compute (or exactly `tokens` characters). Returns a dict."""
    path = os.path.join(RUNS, name + ".json")
    if os.path.exists(path):  # finished earlier: the sweep can be stopped and resumed
        return json.load(open(path))
    n_head = n_head or heads(d_model)
    dev = device()
    torch.manual_seed(seed)
    model = GPT(len(VOCAB), CTX, n_layer, d_model, n_head).to(dev)
    fpt = train_flops_per_token(n_layer, d_model, n_head, CTX, len(VOCAB))
    steps = max(1, round((tokens or flops / fpt) / (batch * CTX)))
    if stream is None or stream.batch_size != batch:
        stream = Stream(batch=batch)
    assert steps <= stream.max_steps, f"{name} needs {steps} steps; the data only has {stream.max_steps}"

    decay = [p for p in model.parameters() if p.dim() >= 2]
    no_decay = [p for p in model.parameters() if p.dim() < 2]
    opt = torch.optim.AdamW([{"params": decay, "weight_decay": 0.1},
                             {"params": no_decay, "weight_decay": 0.0}], lr=lr, betas=(0.9, 0.95),
                            fused=dev in ("mps", "cuda"))
    log_every = max(1, steps // 200)
    curve, window, t0 = [], [], time.time()
    for step in range(steps):
        for group in opt.param_groups:
            group["lr"] = lr_at(step, steps, lr, cycle)
        x, y = stream.batch(step)
        loss = model(x, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        window.append(loss.detach())
        if (step + 1) % log_every == 0 or step == steps - 1:
            seen = (step + 1) * batch * CTX  # [tokens seen, FLOPs used, mean train loss, lr]
            curve.append([seen, seen * fpt, torch.stack(window).mean().item(), lr_at(step, steps, lr, cycle)])
            window = []

    result = dict(name=name, n_layer=n_layer, d_model=d_model, n_head=n_head, params=model.n_params(),
                  flops_per_token=fpt, tokens=steps * batch * CTX, flops=steps * batch * CTX * fpt,
                  budget=flops, steps=steps, batch=batch, lr=lr, cycle=cycle, seed=seed, val_loss=evaluate(model, dev),
                  curve=curve, seconds=round(time.time() - t0, 1), device=dev, **tags)
    os.makedirs(RUNS, exist_ok=True)
    json.dump(result, open(path, "w"))
    if save:
        torch.save(model.state_dict(), os.path.join(RUNS, name + ".pt"))
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--n_layer", type=int, required=True)
    p.add_argument("--d_model", type=int, required=True)
    p.add_argument("--flops", type=float)
    p.add_argument("--tokens", type=float)
    p.add_argument("--lr", type=float, default=2e-3)
    p.add_argument("--cycle", type=float, default=1.0)
    p.add_argument("--batch", type=int, default=BATCH, help="sequences of 64 characters per step")
    p.add_argument("--name", default=None)
    a = p.parse_args()
    name = a.name or f"test_L{a.n_layer}_d{a.d_model}_C{a.flops or a.tokens:.0e}"
    r = run(name, a.n_layer, a.d_model, flops=a.flops, tokens=a.tokens, lr=a.lr, cycle=a.cycle, batch=a.batch)
    print(f"{name}: {r['params']:,} params, {r['tokens']:,} tokens, {r['flops']:.2e} FLOPs, "
          f"val loss {r['val_loss']:.4f} ({r['seconds']} s)")
