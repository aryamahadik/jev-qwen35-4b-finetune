"""Fine-tune a GLiClass uni-encoder as an OpenDecide decision model.

Recipes (step-matched, same seed):
  A0  base rows only (track L0: Choice + one affirmative Noul per state), task loss only
  A3  all rows (L0 + L2 consistency variants + L3 injection/distractor) + consistency loss
      complement: (p_a + p_b - 1)^2     equiv (paraphrase): (p_a - p_b)^2
Related rows sit in the same batch as SEPARATE sequences; no row ever sees another row.
"""
import argparse
import json
import math
import random
import time
from collections import defaultdict
from pathlib import Path

import torch
import torch.nn.functional as F

from gliclass_io import device, forward_logits, load, read_jsonl

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--base", default="knowledgator/gliclass-edge-v3.0")
ap.add_argument("--recipe", choices=["A0", "A3"], required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--epochs", type=float, default=2.0)
ap.add_argument("--lr", type=float, default=3e-5)
ap.add_argument("--batch", type=int, default=32)
ap.add_argument("--lam", type=float, default=0.5)
ap.add_argument("--seed", type=int, default=20260925)
ap.add_argument("--train_file", default="train.jsonl")
ap.add_argument("--rel_file", default="train_relations.jsonl")
ap.add_argument("--models_dir", default=str(HERE / "models"))
a = ap.parse_args()

random.seed(a.seed)
torch.manual_seed(a.seed)
dev = device()
rows_all = read_jsonl(HERE / "data" / a.train_file)
rels_all = read_jsonl(HERE / "data" / a.rel_file)
rows = [r for r in rows_all if a.recipe == "A3" or r["track"] == "L0"]
ids = {r["id"] for r in rows}
rels = [x for x in rels_all if a.recipe == "A3" and x["a"] in ids and x["b"] in ids]
# step-matched: both recipes take the number of steps A3 takes
n_steps = math.ceil(len(rows_all) / a.batch * a.epochs)

units = defaultdict(list)  # rows sharing a state go to the same batch
for r in rows:
    units[r["call_id"]].append(r)
units = list(units.values())
rel_by_row = defaultdict(list)
for x in rels:
    rel_by_row[x["a"]].append(x)


def batches():
    while True:
        random.shuffle(units)
        cur = []
        for u in units:
            cur.extend(u)
            if len(cur) >= a.batch:
                yield cur
                cur = []


EPS = {"mnli": 0.08}
model, tok = load(a.base, dev)
model.train()
opt = torch.optim.AdamW(model.parameters(), lr=a.lr, weight_decay=0.01)
warm = int(0.06 * n_steps)
sched = torch.optim.lr_scheduler.LambdaLR(
    opt, lambda s: (s + 1) / max(1, warm) if s < warm else max(0.0, (n_steps - s) / max(1, n_steps - warm)))

log, t0, gen = [], time.time(), batches()
for step in range(n_steps):
    batch = next(gen)
    logits, ks = forward_logits(model, tok, batch, dev)
    task, cons, pidx = [], [], {}
    for i, (r, k) in enumerate(zip(batch, ks)):
        if r["qtype"] == "noul":
            eps = EPS.get(r["source"], 0.05)
            y = torch.tensor(r["gold"] * (1 - 2 * eps) + eps, device=dev)
            task.append(F.binary_cross_entropy_with_logits(logits[i, 0], y))
            pidx[r["id"]] = torch.sigmoid(logits[i, 0])
        else:
            tgt = torch.tensor(r["options"].index(r["gold"]), device=dev)
            task.append(F.cross_entropy(logits[i, :k].unsqueeze(0), tgt.unsqueeze(0), label_smoothing=0.05))
    loss_task = torch.stack(task).mean()
    loss = loss_task
    if a.recipe == "A3":
        for r in batch:
            for x in rel_by_row.get(r["id"], []):
                if x["a"] in pidx and x["b"] in pidx:
                    pa, pb = pidx[x["a"]], pidx[x["b"]]
                    cons.append((pa + pb - 1) ** 2 if x["type"] == "complement" else (pa - pb) ** 2)
        if cons:
            ramp = min(1.0, step / max(1, 0.2 * n_steps))
            loss = loss + a.lam * ramp * torch.stack(cons).mean()
    opt.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    sched.step()
    if step % 50 == 0 or step == n_steps - 1:
        rec = {"step": step, "of": n_steps, "loss": round(loss.item(), 4), "task": round(loss_task.item(), 4),
               "cons": round(torch.stack(cons).mean().item(), 4) if cons else None,
               "lr": sched.get_last_lr()[0], "min": round((time.time() - t0) / 60, 2)}
        log.append(rec)
        print(json.dumps(rec), flush=True)

out = Path(a.models_dir) / a.out
out.mkdir(parents=True, exist_ok=True)
model.save_pretrained(out)
tok.save_pretrained(out)
(out / "train_meta.json").write_text(json.dumps({"args": vars(a), "rows": len(rows), "relations": len(rels),
                                                  "steps": n_steps, "minutes": round((time.time() - t0) / 60, 2), "log": log}, indent=2))
print("saved", out)
