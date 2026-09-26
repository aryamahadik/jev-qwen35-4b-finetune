"""LoRA fine-tuning of a decoder LM as an OpenDecide decision model (runs on Modal, see modal_od.py).

Same recipes and losses as train.py, on the decoder readout (decoder_io.py):
  task:  CE over the candidate tokens (Yes/No, or option letters) with the same label smoothing as train.py
  cons:  complement (pA + pB - 1)^2 and equiv (pA - pB)^2 on P(yes), related rows in the same batch as
         SEPARATE sequences (no row ever sees another row)
Choice options are re-shuffled every time a row is drawn, so the model cannot learn a letter prior.
anchor (v0.6): rows with meta.anchor get + beta * KL(p_base || p_student) over the candidate tokens, where p_base is the
         frozen base model (adapter disabled, no grad). Breadth rows stay close to the base model's general behaviour
         (learning-without-forgetting / self-distillation); robustness rows are free to specialise.
"""
from __future__ import annotations

import json
import math
import random
import time
from collections import defaultdict
from pathlib import Path

import torch
import torch.nn.functional as F

import decoder_io
from decoder_io import Readout, cand_logits, load

EPS = {"mnli": 0.08}


def read_jsonl(p):
    return [json.loads(l) for l in open(p)]


def train(cfg: dict, data_dir: Path, out_dir: Path, dev="cuda") -> dict:
    c = {"recipe": "A3", "epochs": 1.0, "lr": 1e-4, "batch": 16, "lam": 0.5, "r": 16, "alpha": 32, "dropout": 0.05, "beta": 0.0,
         "seed": 20260925, "train_file": "train.jsonl", "rel_file": "train_relations.jsonl", "grad_ckpt": True, **cfg}
    random.seed(c["seed"])
    torch.manual_seed(c["seed"])
    rows_all = read_jsonl(data_dir / c["train_file"])
    rels_all = read_jsonl(data_dir / c["rel_file"])
    rows = [r for r in rows_all if c["recipe"] != "A0" or r["track"] == "L0"]
    ids = {r["id"] for r in rows}
    rels = [x for x in rels_all if c["recipe"] != "A0" and x["a"] in ids and x["b"] in ids]
    n_steps = math.ceil(len(rows_all) / c["batch"] * c["epochs"])  # step-matched across recipes

    units = defaultdict(list)
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
                if len(cur) >= c["batch"]:
                    yield cur
                    cur = []

    from peft import LoraConfig, get_peft_model
    model, tok = load(c["base"], dev)
    if c["grad_ckpt"]:
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
        model.enable_input_require_grads()
    targets = c.get("targets") or ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    model = get_peft_model(model, LoraConfig(r=c["r"], lora_alpha=c["alpha"], lora_dropout=c["dropout"], task_type="CAUSAL_LM",
                                             target_modules=targets))
    model.print_trainable_parameters()
    model.train()
    ro = Readout(tok)
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=c["lr"], weight_decay=0.0)
    warm = int(0.05 * n_steps)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda s: (s + 1) / max(1, warm) if s < warm else 0.5 * (1 + math.cos(math.pi * (s - warm) / max(1, n_steps - warm))))

    log, t0, gen = [], time.time(), batches()
    for step in range(n_steps):
        batch = next(gen)
        cyg = decoder_io.STYLE == "cygnet"
        perms = [random.sample(range(len(r["options"])), len(r["options"])) if r["qtype"] == "choice"
                 else (random.sample([0, 1], 2) if cyg else None) for r in batch]
        with torch.autocast("cuda", dtype=torch.bfloat16):
            lg = cand_logits(model, ro, batch, dev, perms=perms)
        anc = [i for i, r in enumerate(batch) if c["beta"] > 0 and (r.get("meta") or {}).get("anchor")]
        kl = None
        if anc:
            with torch.no_grad(), model.disable_adapter(), torch.autocast("cuda", dtype=torch.bfloat16):
                blg = cand_logits(model, ro, [batch[i] for i in anc], dev, perms=[perms[i] for i in anc])
            kl = torch.stack([F.kl_div(F.log_softmax(lg[i], -1), F.log_softmax(b, -1), log_target=True, reduction="sum")
                              for i, b in zip(anc, blg)]).mean()
        task, cons, pidx = [], [], {}
        for r, perm, l in zip(batch, perms, lg):
            if r["qtype"] == "noul":
                eps = EPS.get(r["source"], 0.05)
                y = r["gold"] * (1 - 2 * eps) + eps
                logp = F.log_softmax(l, -1)
                iy, in_ = (perm.index(0), perm.index(1)) if cyg else (0, 1)  # displayed letter of Yes / No
                task.append(-(y * logp[iy] + (1 - y) * logp[in_]))
                pidx[r["id"]] = logp[iy].exp()
            else:
                gp = (r.get("meta") or {}).get("gold_probs")
                if gp:  # exact probabilistic target (e.g. Bayes posterior): soft cross-entropy on the displayed order
                    q = torch.tensor([float(gp.get(r["options"][i], 0.0)) for i in perm], device=dev)
                    q = 0.97 * q / q.sum() + 0.03 / len(perm)
                    task.append(-(q * F.log_softmax(l, -1)).sum())
                else:
                    gi = perm.index(r["options"].index(r["gold"]))
                    task.append(F.cross_entropy(l.unsqueeze(0), torch.tensor([gi], device=dev), label_smoothing=0.05))
        loss_task = torch.stack(task).mean()
        loss = loss_task
        if c["recipe"] != "A0":
            for r in batch:
                for x in rel_by_row.get(r["id"], []):
                    if x["a"] in pidx and x["b"] in pidx:
                        pa, pb = pidx[x["a"]], pidx[x["b"]]
                        cons.append((pa + pb - 1) ** 2 if x["type"] == "complement" else (pa - pb) ** 2)
            if cons:
                ramp = min(1.0, step / max(1, 0.2 * n_steps))
                loss = loss + c["lam"] * ramp * torch.stack(cons).mean()
        if kl is not None:
            loss = loss + c["beta"] * kl
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        sched.step()
        if step % c.get("log_every", 25) == 0 or step == n_steps - 1:
            rec = {"step": step, "of": n_steps, "loss": round(loss.item(), 4), "task": round(loss_task.item(), 4),
                   "cons": round(torch.stack(cons).mean().item(), 4) if cons else None,
                   "kl": round(kl.item(), 4) if kl is not None else None,
                   "lr": sched.get_last_lr()[0], "min": round((time.time() - t0) / 60, 2)}
            log.append(rec)
            print(json.dumps(rec), flush=True)

    out_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(out_dir)
    tok.save_pretrained(out_dir)
    meta = {"cfg": c, "rows": len(rows), "relations": len(rels), "steps": n_steps,
            "minutes": round((time.time() - t0) / 60, 2), "log": log}
    (out_dir / "train_meta.json").write_text(json.dumps(meta, indent=2))
    model.eval()
    return {"model": model, "tok": tok, "meta": meta}
