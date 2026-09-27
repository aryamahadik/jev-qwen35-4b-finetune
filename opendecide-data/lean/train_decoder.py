"""LoRA fine-tuning of a decoder LM as an OpenDecide decision model (runs on Modal, see modal_od.py).

Same recipes and losses as train.py, on the decoder readout (decoder_io.py):
  task:  CE over the candidate tokens (Yes/No, or option letters) with the same label smoothing as train.py
  cons:  complement (pA + pB - 1)^2 and equiv (pA - pB)^2 on P(yes), related rows in the same batch as
         SEPARATE sequences (no row ever sees another row)
Choice options are re-shuffled every time a row is drawn, so the model cannot learn a letter prior.
anchor (v0.6): rows with meta.anchor get + beta * KL(p_base || p_student) over the candidate tokens, where p_base is the
         frozen base model (adapter disabled, no grad). Breadth rows stay close to the base model's general behaviour
         (learning-without-forgetting / self-distillation); robustness rows are free to specialise.

v0.11 terms (all off by default; with the keys unset the loss is exactly the v0.10 loss). They work on the CANONICAL
distribution of a row (canon_logp: choice -> row["options"] order, yes/no -> [yes, no]), i.e. with the displayed option
permutation undone, so two views of the same question are comparable outcome by outcome.
  lam_inv   relation 'inv' (a = clean row, b = attacked twin, same call_id): + lam_inv * KL(stopgrad(p_a) || p_b) over the
            full distribution, yes/no and choice rows. With lam_inv = 0, 'inv' relations keep the old behaviour
            (treated like 'equiv', the pre-v0.11 fallback for any non-complement type).
  sym_cons  True: 'equiv' = Jensen-Shannon(p_a, p_b) over the full distribution (choice rows too, when both rows have the
            same option set); 'complement' = symmetric KL between p_a and p_b with yes/no swapped. Weight lam, as before.
  perm_twin that fraction of choice rows is scored a second time under another permutation in the SAME cand_logits call;
            + lam_p * JS(canonical view 1, canonical view 2). Twins are picked with their own RNG, so batches and first
            permutations are identical to a run without twins.
All consistency terms (cons, inv, perm) share the 20% warm-up ramp. Every term is logged; a non-finite term aborts the run.
kd: only a dict meta.teacher is a distillation target (a string teacher is provenance, e.g. on LAH rows, and is ignored).
Rows the loss cannot score (gold not an option, gold_probs with no mass, >255 options, ...) fail before the model loads.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import shutil
import time
from collections import Counter, defaultdict
from pathlib import Path

import torch
import torch.nn.functional as F

import decoder_io
from decoder_io import Readout, cand_logits, load

EPS = {"mnli": 0.08}
# v0.11 loss knobs; these defaults reproduce the v0.10 loss exactly.
LOSS_DEFAULTS = {"lam_inv": 0.0, "sym_cons": False, "perm_twin": 0.0, "lam_p": 0.5}
TERMS = ("loss", "task", "cons", "cons_comp", "cons_equiv", "inv", "perm", "kl")


def read_jsonl(p):
    return [json.loads(l) for l in open(p)]


# ---------------------------------------------------------------- canonical order and divergences

def inverse_perm(perm):
    """perm[j] = canonical option shown at displayed position j  ->  inv[i] = displayed position of canonical option i."""
    inv = [0] * len(perm)
    for j, o in enumerate(perm):
        inv[o] = j
    return inv


def canon_logp(row, logits, perm, cyg=None):
    """Log-probs of one row in CANONICAL order: choice -> row["options"] order, yes/no -> [yes, no].
    `logits` are in displayed order (as cand_logits returns them for `perm`); this undoes the permutation.
    od-style yes/no rows are always read as [Yes, No] (perm None); cygnet-style ones carry a perm over [Yes, No]."""
    if cyg is None:
        cyg = decoder_io.STYLE == "cygnet"
    logp = F.log_softmax(logits.float(), -1)
    if perm is None or (row["qtype"] == "noul" and not cyg):
        return logp
    assert len(perm) == logp.shape[-1], (row.get("id"), len(perm), logp.shape)
    return logp[torch.tensor(inverse_perm(perm), device=logp.device)]


def kl_div(lp, lq):
    """KL(p || q) from log-probs over the same outcomes."""
    return F.kl_div(lq, lp, log_target=True, reduction="sum")


def js_div(lp, lq):
    """Jensen-Shannon divergence (natural log, in [0, ln 2]) from log-probs."""
    lm = torch.logsumexp(torch.stack([lp, lq]), 0) - math.log(2.0)
    return 0.5 * (kl_div(lp, lm) + kl_div(lq, lm))


def sym_kl(lp, lq):
    """Symmetric KL: (KL(p || q) + KL(q || p)) / 2."""
    return 0.5 * (kl_div(lp, lq) + kl_div(lq, lp))


def align(ra, la, rb, lb):
    """Canonical log-probs of two related rows over the SAME outcomes, or None when they are not comparable
    (yes/no vs choice, or different option sets). Same options in another order -> b is re-ordered to a's order."""
    if (ra["qtype"] == "noul") != (rb["qtype"] == "noul"):
        return None
    if ra["qtype"] == "noul":
        return la, lb
    oa, ob = ra["options"], rb["options"]
    if oa == ob:
        return la, lb
    if len(oa) != len(ob) or len(set(oa)) != len(oa) or set(oa) != set(ob):
        return None
    pos = {o: i for i, o in enumerate(ob)}
    return la, lb[torch.tensor([pos[o] for o in oa], device=lb.device)]


def second_perm(perm, rng):
    """A random permutation different from `perm` (len(perm) >= 2)."""
    n = len(perm)
    if n < 2:
        raise ValueError(f"second_perm needs >= 2 options, got {n}")
    while True:
        q = rng.sample(range(n), n)
        if q != list(perm):
            return q


def pick_twins(batch, perms, frac, rng):
    """[(i, perm2)] for the choice rows that get a second view (cfg perm_twin). frac 0 draws nothing from rng."""
    if not frac or frac <= 0:
        return []
    out = []
    for i, (r, p) in enumerate(zip(batch, perms)):
        if r["qtype"] == "choice" and len(r["options"]) > 1 and rng.random() < frac:
            out.append((i, second_perm(p, rng)))
    return out


# ---------------------------------------------------------------- batching

def make_units(rows, rels=()):
    """Rows grouped by call_id (one unit is never split across batches). 'inv' twins share call_id by construction;
    any 'inv' pair that does not is merged into one unit, so the invariance term always sees both rows.
    Returns (units, n_merged). Without such pairs the units are exactly the old call_id groups, in the same order."""
    units = defaultdict(list)
    for r in rows:
        units[r["call_id"]].append(r)
    cid = {r["id"]: r["call_id"] for r in rows}
    parent = {}

    def find(k):
        while parent.get(k, k) != k:
            k = parent[k]
        return k

    merged = 0
    for x in rels:
        if x.get("type") != "inv" or x["a"] not in cid or x["b"] not in cid:
            continue
        ka, kb = find(cid[x["a"]]), find(cid[x["b"]])
        if ka != kb:
            parent[kb] = ka
            merged += 1
    if merged:
        out = {}
        for k, u in units.items():
            out.setdefault(find(k), []).extend(u)
        units = out
    return list(units.values()), merged


def batches(units, batch_size):
    """Endless stream of batches of whole units (the global `random` stream, as before)."""
    while True:
        random.shuffle(units)
        cur = []
        for u in units:
            cur.extend(u)
            if len(cur) >= batch_size:
                yield cur
                cur = []


# ---------------------------------------------------------------- loss

def kd_target(r):
    """meta.teacher as a distillation target, or None. Only a dict of probabilities is a target ({"yes": p} for yes/no,
    {option: p} for choice). LAH rows (train_v07..v10s4, lah_train) carry meta.teacher = "<model id>" as provenance;
    that string is not a target, and used as one it crashed kd > 0 runs ('str' object has no attribute 'get')."""
    t = (r.get("meta") or {}).get("teacher")
    return t if isinstance(t, dict) and t else None


def check_rows(rows, kd=0.0, max_options=decoder_io.MAX_OPTIONS):
    """Fail fast (before loading a model) on rows the loss cannot score; otherwise they crash or NaN mid-run."""
    bad = []
    for r in rows:
        rid, meta = r.get("id"), (r.get("meta") or {})
        if r["qtype"] == "noul":
            g = r.get("gold")
            if not isinstance(g, (int, float)) or not 0 <= g <= 1:
                bad.append((rid, f"noul gold {g!r} not in [0, 1]"))
            t = kd_target(r) if kd > 0 else None
            if t is not None and "yes" not in t:
                bad.append((rid, "noul meta.teacher has no 'yes'"))
            continue
        o = r.get("options") or []
        if not 1 <= len(o) <= max_options:
            bad.append((rid, f"{len(o)} options (allowed 1..{max_options})"))
            continue
        gp = meta.get("gold_probs")
        if gp:
            if not sum(float(gp.get(x, 0.0)) for x in o) > 0:
                bad.append((rid, "meta.gold_probs has no mass on the row's options"))
        elif r.get("gold") not in o:
            bad.append((rid, f"gold {r.get('gold')!r} not among the options"))
    if bad:
        raise ValueError(f"train_decoder: {len(bad)} unusable training row(s), e.g. {bad[:5]}")


def check_finite(terms, step, batch):
    live = {k: v for k, v in terms.items() if v is not None}
    vals = torch.stack([v.detach().float().reshape(()) for v in live.values()])
    if bool(torch.isfinite(vals).all()):
        return
    got = dict(zip(live, vals.tolist()))
    bad = [k for k, v in got.items() if not math.isfinite(v)]
    raise FloatingPointError(
        f"train_decoder: non-finite loss term(s) {bad} at step {step}; terms={ {k: round(v, 6) for k, v in got.items()} }; "
        f"batch row ids (first 8): {[r.get('id') for r in batch[:8]]}. Aborting instead of training on NaN.")


def compute_loss(c, batch, perms, lg, rel_by_row, step, n_steps, dev, kl=None, twins=(), cyg=None):
    """Loss of one step. lg[i] = candidate logits of batch[i] in its displayed order perms[i]; kl = anchor KL (or None);
    twins = [(i, perm2, logits2)]: second views of choice rows (perm_twin).
    Returns (loss, terms, counts): terms maps every name in TERMS to a 0-d tensor, or None when absent this step."""
    if cyg is None:
        cyg = decoder_io.STYLE == "cygnet"
    lam_inv, sym = float(c.get("lam_inv", 0.0) or 0.0), bool(c.get("sym_cons", False))
    task, cons, pidx = [], [], {}
    for r, perm, l in zip(batch, perms, lg):
        teach = kd_target(r) if c.get("kd", 0) > 0 else None  # distillation target
        if r["qtype"] == "noul":
            eps = EPS.get(r["source"], 0.05)
            y = r["gold"] * (1 - 2 * eps) + eps
            if teach:
                y = (1 - c["kd"]) * y + c["kd"] * float(teach["yes"])
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
            elif teach:  # soft target = (1 - kd) * smoothed gold + kd * teacher, in the displayed order
                gi = perm.index(r["options"].index(r["gold"]))
                q = torch.full((len(perm),), 0.05 / len(perm), device=dev)
                q[gi] += 0.95
                tq = torch.tensor([float(teach.get(r["options"][i], 0.0)) for i in perm], device=dev)
                q = (1 - c["kd"]) * q + c["kd"] * tq / tq.sum().clamp_min(1e-9)
                task.append(-(q * F.log_softmax(l, -1)).sum())
            else:
                gi = perm.index(r["options"].index(r["gold"]))
                task.append(F.cross_entropy(l.unsqueeze(0), torch.tensor([gi], device=dev), label_smoothing=0.05))
    loss_task = torch.stack(task).mean()
    loss = loss_task
    terms = dict.fromkeys(TERMS)
    terms["task"] = loss_task
    counts = {"cons": 0, "inv": 0, "twin": len(twins), "rel_skipped": 0}
    ramp = min(1.0, step / max(1, 0.2 * n_steps))

    pos = {r["id"]: i for i, r in enumerate(batch)}
    canon = {}

    def ci(i):  # canonical log-probs of batch[i], by position (twins never go through an id lookup)
        if i not in canon:
            canon[i] = canon_logp(batch[i], lg[i], perms[i], cyg)
        return canon[i]

    def cl(rid):
        return ci(pos[rid])

    inv, comp, equiv = [], [], []
    if c["recipe"] != "A0":
        for r in batch:
            for x in rel_by_row.get(r["id"], []):
                kind = x["type"]
                if kind == "inv" and lam_inv > 0:
                    if x["a"] in pos and x["b"] in pos:
                        ab = align(batch[pos[x["a"]]], cl(x["a"]), batch[pos[x["b"]]], cl(x["b"]))
                        if ab is None:
                            counts["rel_skipped"] += 1
                        else:
                            inv.append(kl_div(ab[0].detach(), ab[1]))  # teacher = clean view, no gradient through it
                    continue
                if sym:
                    if x["a"] not in pos or x["b"] not in pos:
                        continue
                    ra, rb = batch[pos[x["a"]]], batch[pos[x["b"]]]
                    if kind == "complement":
                        if ra["qtype"] != "noul" or rb["qtype"] != "noul":
                            counts["rel_skipped"] += 1
                            continue
                        t = sym_kl(cl(x["a"]), cl(x["b"]).flip(0))  # [yes, no] of b -> [no, yes]
                        comp.append(t)
                    else:
                        ab = align(ra, cl(x["a"]), rb, cl(x["b"]))
                        if ab is None:
                            counts["rel_skipped"] += 1
                            continue
                        t = js_div(*ab)
                        equiv.append(t)
                    cons.append(t)
                elif x["a"] in pidx and x["b"] in pidx:
                    pa, pb = pidx[x["a"]], pidx[x["b"]]
                    t = (pa + pb - 1) ** 2 if kind == "complement" else (pa - pb) ** 2
                    cons.append(t)
                    (comp if kind == "complement" else equiv).append(t)
        if cons:
            terms["cons"] = torch.stack(cons).mean()
            loss = loss + c["lam"] * ramp * terms["cons"]
    if comp:
        terms["cons_comp"] = torch.stack(comp).mean().detach()
    if equiv:
        terms["cons_equiv"] = torch.stack(equiv).mean().detach()
    counts["cons"], counts["inv"] = len(cons), len(inv)
    if kl is not None:
        terms["kl"] = kl
        loss = loss + c["beta"] * kl
    if inv:
        terms["inv"] = torch.stack(inv).mean()
        loss = loss + lam_inv * ramp * terms["inv"]
    if twins:
        pt = [js_div(ci(i), canon_logp(batch[i], l2, p2, cyg)) for i, p2, l2 in twins]
        terms["perm"] = torch.stack(pt).mean()
        loss = loss + float(c.get("lam_p", 0.5)) * ramp * terms["perm"]
    terms["loss"] = loss
    check_finite(terms, step, batch)
    return loss, terms, counts


# ---------------------------------------------------------------- training

def _est_tokens(r: dict) -> int:
    """Rough prompt length in tokens (system prompt + text + question + options + card), for micro-batch packing."""
    n = len(r.get("state") or "") + len(r.get("card") or "") + len(r.get("instructions") or "")
    n += sum(len(o) + 4 for o in (r.get("options") or []))
    return int((n + 600) / 3.2)


def _micro_groups(batch: list, uid: dict, tw: list, budget: int) -> list:
    """Split a batch into micro-batches of whole units (a unit holds a record's related rows, so relation terms stay
    inside one micro-batch). Cost of a micro-batch = sequences x padded max length (twins count as extra sequences).
    Units are packed longest first; a unit over the budget on its own becomes its own micro-batch."""
    pad = max(1, decoder_io.PAD_MULTIPLE)
    padded = lambda n: -(-n // pad) * pad
    twin_n = Counter(i for i, _ in tw)
    order, members = [], defaultdict(list)
    for i, r in enumerate(batch):
        u = uid.get(r["id"], ("row", i))
        if u not in members:
            order.append(u)
        members[u].append(i)
    info = []
    for u in order:
        idx = members[u]
        info.append((max(_est_tokens(batch[i]) for i in idx), sum(1 + twin_n[i] for i in idx), idx))
    info.sort(key=lambda x: -x[0])
    groups, cur, cur_len, cur_seq = [], [], 0, 0
    for ln, nseq, idx in info:
        if cur and (cur_seq + nseq) * padded(max(cur_len, ln)) > budget:
            groups.append(sorted(cur))
            cur, cur_len, cur_seq = [], 0, 0
        cur += idx
        cur_len, cur_seq = max(cur_len, ln), cur_seq + nseq
    if cur:
        groups.append(sorted(cur))
    return groups


def _fingerprint(c: dict, rows: list, n_steps: int) -> str:
    """Identifies a run for resume: the config (minus resume knobs), the step count and the training rows."""
    cfg = {k: v for k, v in c.items() if k not in ("resume", "ckpt_every_min")}
    h = hashlib.sha256(json.dumps(cfg, sort_keys=True, default=str).encode())
    h.update(str(n_steps).encode())
    for r in rows:
        h.update(r["id"].encode())
    return h.hexdigest()


def _save_ckpt(ckpt: Path, model, opt, sched, next_step: int, log: list, minutes: float, fp: str):
    """Atomic checkpoint: write to _ckpt.tmp, then swap it in, so a VM stopped mid-write leaves the old one intact."""
    tmp = ckpt.with_name(ckpt.name + ".tmp")
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    model.save_pretrained(tmp / "adapter")
    torch.save({"step": next_step, "opt": opt.state_dict(), "sched": sched.state_dict(), "log": log, "minutes": minutes,
                "fingerprint": fp, "torch_rng": torch.get_rng_state(),
                "cuda_rng": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None}, tmp / "state.pt")
    old = ckpt.with_name(ckpt.name + ".old")
    if ckpt.exists():
        ckpt.rename(old)
    tmp.rename(ckpt)
    if old.exists():
        shutil.rmtree(old)
    print(json.dumps({"checkpoint": str(ckpt), "next_step": next_step}), flush=True)


def train(cfg: dict, data_dir: Path, out_dir: Path, dev="cuda") -> dict:
    c = {"recipe": "A3", "epochs": 1.0, "lr": 1e-4, "batch": 16, "lam": 0.5, "r": 16, "alpha": 32, "dropout": 0.05, "beta": 0.0,
         "seed": 20260925, "train_file": "train.jsonl", "rel_file": "train_relations.jsonl", "grad_ckpt": True,
         **LOSS_DEFAULTS, **cfg}
    if not (c["lam_inv"] >= 0 and 0 <= c["perm_twin"] <= 1 and c["lam_p"] >= 0):
        raise ValueError(f"bad v0.11 loss cfg: lam_inv={c['lam_inv']} perm_twin={c['perm_twin']} lam_p={c['lam_p']}")
    decoder_io.LAYOUT = c.get("layout", "text_first")  # PRISM layout test (prompt order); predictions after training reuse it
    random.seed(c["seed"])
    torch.manual_seed(c["seed"])
    twin_rng = random.Random(c["seed"] + 1)  # own stream: perm_twin never changes batches or first permutations
    rows_all = read_jsonl(data_dir / c["train_file"])
    rels_all = read_jsonl(data_dir / c["rel_file"])
    rows = [r for r in rows_all if c["recipe"] != "A0" or r["track"] == "L0"]
    ids = {r["id"] for r in rows}
    rels = [x for x in rels_all if c["recipe"] != "A0" and x["a"] in ids and x["b"] in ids]
    n_steps = math.ceil(len(rows_all) / c["batch"] * c["epochs"])  # step-matched across recipes
    check_rows(rows, c.get("kd", 0) or 0)

    units, inv_merged = make_units(rows, rels)
    if inv_merged:
        print(f"make_units: merged {inv_merged} 'inv' pair(s) with different call_ids into one unit", flush=True)
    rel_by_row = defaultdict(list)
    for x in rels:
        rel_by_row[x["a"]].append(x)
    rel_types = dict(sorted(Counter(x["type"] for x in rels).items()))
    print(json.dumps({"rows": len(rows), "relations": rel_types, "units": len(units),
                      "kd_targets": sum(kd_target(r) is not None for r in rows) if c.get("kd", 0) else 0,
                      **{k: c[k] for k in LOSS_DEFAULTS}}), flush=True)

    from peft import LoraConfig, get_peft_model
    model, tok = load(c["base"], dev)
    if c["grad_ckpt"]:
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
        model.enable_input_require_grads()
    targets = c.get("targets") or ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    if c.get("init_adapter"):  # continue training an existing adapter (stage 2); the KL anchor still uses the frozen base
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, c["init_adapter"], is_trainable=True)
    else:
        model = get_peft_model(model, LoraConfig(r=c["r"], lora_alpha=c["alpha"], lora_dropout=c["dropout"],
                                                 task_type="CAUSAL_LM", target_modules=targets))
    model.print_trainable_parameters()
    model.train()
    ro = Readout(tok)
    n_max = max((len(r["options"]) for r in rows if r["qtype"] == "choice"), default=0)
    if n_max > 26 and getattr(ro, "wide", None) is not None and len(ro.wide) < n_max:
        raise ValueError(f"train_decoder: a row has {n_max} options but this tokenizer has only {len(ro.wide)} labels")
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=c["lr"], weight_decay=0.0)
    warm = int(0.05 * n_steps)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda s: (s + 1) / max(1, warm) if s < warm else 0.5 * (1 + math.cos(math.pi * (s - warm) / max(1, n_steps - warm))))

    log, t0, gen = [], time.time(), batches(units, c["batch"])
    # Save-and-resume (Spot VMs, auto-stop timers): every ckpt_every_min minutes the adapter, optimizer, scheduler,
    # step, log and RNG states go to out_dir/_ckpt. A rerun of the same config resumes exactly: the finished steps'
    # random-number use (batch order, option permutations, twin picks) is replayed without GPU work, then the torch
    # RNG states are restored.
    ckpt, start, every = out_dir / "_ckpt", 0, float(c.get("ckpt_every_min", 15))
    fp = _fingerprint(c, rows, n_steps)
    old = ckpt.with_name(ckpt.name + ".old")
    if not (ckpt / "state.pt").exists() and (old / "state.pt").exists():  # stopped between the two renames
        if ckpt.exists():
            shutil.rmtree(ckpt)
        old.rename(ckpt)
    if c.get("resume", True) and (ckpt / "state.pt").exists():
        st = torch.load(ckpt / "state.pt", map_location="cpu", weights_only=False)
        if st.get("fingerprint") == fp:
            from peft import set_peft_model_state_dict
            from safetensors.torch import load_file
            set_peft_model_state_dict(model, load_file(str(ckpt / "adapter" / "adapter_model.safetensors")))
            opt.load_state_dict(st["opt"])
            sched.load_state_dict(st["sched"])
            cyg0 = decoder_io.STYLE == "cygnet"
            for _ in range(st["step"]):
                b = next(gen)
                ps = [random.sample(range(len(r["options"])), len(r["options"])) if r["qtype"] == "choice"
                      else (random.sample([0, 1], 2) if cyg0 else None) for r in b]
                pick_twins(b, ps, c["perm_twin"], twin_rng)
            torch.set_rng_state(st["torch_rng"])
            if torch.cuda.is_available() and st.get("cuda_rng") is not None:
                torch.cuda.set_rng_state_all(st["cuda_rng"])
            start, log, t0 = st["step"], st["log"], time.time() - 60 * st["minutes"]
            print(json.dumps({"resumed_at_step": start, "of": n_steps}), flush=True)
        else:
            print("checkpoint in", ckpt, "is for a different run; starting fresh", flush=True)
    last_ckpt = time.time()
    uid = {r["id"]: k for k, u in enumerate(units) for r in u}
    micro_tok = int(c.get("micro_tokens", 0) or 0)
    for step in range(start, n_steps):
        batch = next(gen)
        cyg = decoder_io.STYLE == "cygnet"
        perms = [random.sample(range(len(r["options"])), len(r["options"])) if r["qtype"] == "choice"
                 else (random.sample([0, 1], 2) if cyg else None) for r in batch]
        tw = pick_twins(batch, perms, c["perm_twin"], twin_rng)  # second views ride in the same forward call
        # Gradient accumulation (cfg micro_tokens > 0, for small GPUs): the batch is split into micro-batches of whole
        # units under a padded-token budget; each micro-batch's loss is weighted by its share of the batch's rows. The
        # random draws above are made for the whole batch, so data order and resume are unchanged.
        groups = _micro_groups(batch, uid, tw, micro_tok) if micro_tok > 0 else [list(range(len(batch)))]
        opt.zero_grad(set_to_none=True)
        agg, wsum, counts = defaultdict(float), defaultdict(float), Counter()
        for idx in groups:
            mb, mp = [batch[i] for i in idx], [perms[i] for i in idx]
            local = {i: j for j, i in enumerate(idx)}
            mtw = [(local[i], p2) for i, p2 in tw if i in local]
            with torch.autocast("cuda", dtype=torch.bfloat16):
                lg_all = cand_logits(model, ro, mb + [mb[i] for i, _ in mtw], dev, perms=mp + [p for _, p in mtw])
            lg = lg_all[:len(mb)]
            twins = [(i, p2, l2) for (i, p2), l2 in zip(mtw, lg_all[len(mb):])]
            anc = [i for i, r in enumerate(mb) if c["beta"] > 0 and (r.get("meta") or {}).get("anchor")]
            kl = None
            if anc:
                with torch.no_grad(), model.disable_adapter(), torch.autocast("cuda", dtype=torch.bfloat16):
                    blg = cand_logits(model, ro, [mb[i] for i in anc], dev, perms=[mp[i] for i in anc])
                kl = torch.stack([F.kl_div(F.log_softmax(lg[i], -1), F.log_softmax(b, -1), log_target=True, reduction="sum")
                                  for i, b in zip(anc, blg)]).mean()
            loss, mterms, mcounts = compute_loss(c, mb, mp, lg, rel_by_row, step, n_steps, dev, kl=kl, twins=twins, cyg=cyg)
            w = len(mb) / len(batch)
            (loss * w if len(groups) > 1 else loss).backward()
            for k, v in mterms.items():
                if v is not None:
                    agg[k] += w * float(v.detach())
                    wsum[k] += w
            counts.update(mcounts)
        terms = {k: (torch.tensor(agg[k] / wsum[k]) if wsum[k] > 0 else None) for k in TERMS}
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        sched.step()
        if step % c.get("log_every", 25) == 0 or step == n_steps - 1:
            rec = {"step": step, "of": n_steps,
                   **{k: (round(v.item(), 4) if v is not None else None) for k, v in terms.items()},
                   "n_cons": counts["cons"], "n_inv": counts["inv"], "n_twin": counts["twin"],
                   "n_rel_skipped": counts["rel_skipped"],
                   "lr": sched.get_last_lr()[0], "min": round((time.time() - t0) / 60, 2)}
            log.append(rec)
            print(json.dumps(rec), flush=True)
        if every > 0 and step < n_steps - 1 and time.time() - last_ckpt >= 60 * every:
            _save_ckpt(ckpt, model, opt, sched, step + 1, log, (time.time() - t0) / 60, fp)
            last_ckpt = time.time()

    out_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(out_dir)
    tok.save_pretrained(out_dir)
    if ckpt.exists():  # the finished adapter supersedes the checkpoint
        shutil.rmtree(ckpt)
    meta = {"cfg": c, "rows": len(rows), "relations": len(rels), "relation_types": rel_types, "inv_merged": inv_merged,
            "steps": n_steps, "minutes": round((time.time() - t0) / 60, 2), "log": log}
    (out_dir / "train_meta.json").write_text(json.dumps(meta, indent=2))
    model.eval()
    return {"model": model, "tok": tok, "meta": meta}
