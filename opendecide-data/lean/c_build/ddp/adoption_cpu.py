"""PREREG_FINAL A20 (c) adoption test 1 (CPU, local): DDP must give the single-GPU gradients and losses.

A tiny random Qwen3-like model (2 layers, hidden 64, fp32, no dropout) with the real Qwen3 tokenizer, the real prompt
path (decoder_io.cand_logits, cygnet style, schema_branch_mark layout) and the round-1 loss settings (aux_norm batch,
kd, kd_full_src, sym_cons, perm_twin, lam_inv, lam_ord, beta anchor, relation units, micro_tokens packing), 3 steps:
  A  the pinned trainer as committed (git HEAD copy of train_decoder.py), one fresh process
  B  train_decoder.train after importing train_ddp, one fresh process (default path)  -> must equal A bit for bit
  C  train_ddp.launch_ddp, 2 gloo processes        -> loss and gradients within 1e-5 relative of B
  D  as C, stopped after step 2 and resumed (2 launches)    -> bit-identical to C
  E  train_ddp.launch_ddp, 1 process               -> bit-identical to B
train_ddp builds its loop from the pinned train_decoder.train source plus the DDP hunks (train_decoder.py unchanged).
"LoRA" here = the attention and MLP projection weights of the tiny model are the trained tensors (full matrices,
fp32); the embedding and norms are frozen, as the base model is under LoRA.
Usage: git show HEAD:opendecide-data/lean/train_decoder.py > <orig>
       nice -n 10 python c_build/ddp/adoption_cpu.py --orig <orig> --work <scratch dir>
Writes c_build/ddp/ADOPTION_CPU.json."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import json
import os
import pickle
import random
import shutil
import sys
import time
import types
from pathlib import Path

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN))
sys.path.insert(0, str(LEAN / "c_build/ddp"))
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
import torch  # noqa: E402

import decoder_io  # noqa: E402
import train_ddp  # noqa: E402
import train_decoder as td  # noqa: E402

TOK_ID = "Qwen/Qwen3-4B-Instruct-2507"  # cached locally; only its tokenizer is used
TARGETS = ("q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj")
OUT = LEAN / "c_build/ddp/ADOPTION_CPU.json"


class _Tok:  # what train() saves next to the adapter; the real tokenizer lives in the cached Readout
    def save_pretrained(self, out_dir):
        pass


def _tiny_model(vocab: int):
    from transformers import Qwen3Config, Qwen3ForCausalLM
    cfg = Qwen3Config(vocab_size=vocab, hidden_size=64, intermediate_size=128, num_hidden_layers=2,
                      num_attention_heads=4, num_key_value_heads=2, head_dim=16, max_position_embeddings=4096,
                      tie_word_embeddings=True, attention_dropout=0.0)
    with torch.random.fork_rng():  # fixed weights; the trainer's own RNG streams are untouched
        torch.manual_seed(1234)
        m = Qwen3ForCausalLM(cfg).float()
    return m


def _fake_peft(model, _cfg):
    for n, p in model.named_parameters():
        p.requires_grad_(any(f".{t}." in n for t in TARGETS))
    model.print_trainable_parameters = lambda: None
    model.disable_adapter = contextlib.nullcontext

    def save(d):
        Path(d).mkdir(parents=True, exist_ok=True)
        torch.save({n: p.detach().clone() for n, p in model.named_parameters() if p.requires_grad}, Path(d) / "adapter.pt")
    model.save_pretrained = save
    return model


_REAL_CLIP = torch.nn.utils.clip_grad_norm_


def install(rank: int, work: str, modname: str, tag: str):
    """Fakes and probes in this process for module `modname` (train_decoder, or the frozen copy). Probes, written to
    work/probe_<tag>_r<rank>.pt after every step: the summed gradient each step clips (before clipping), every
    micro-batch loss (already divided by the whole-batch counts) and the row ids of every gradient forward."""
    mod = sys.modules[modname]
    with open(Path(work) / "readout.pkl", "rb") as f:
        ro = pickle.load(f)
    fake = types.ModuleType("peft")
    fake.LoraConfig = lambda **kw: kw
    fake.get_peft_model = _fake_peft
    sys.modules["peft"] = fake
    mod.load = lambda base, dev, **kw: (_tiny_model(len(ro.tok)).to(dev), _Tok())
    mod.Readout = lambda tok: ro
    probe = {"grads": [], "gn": [], "micro": [], "calls": []}
    real_loss, real_cand = mod.compute_loss, decoder_io.cand_logits

    def cand(model, ro_, rows, dev, perms=None):
        if torch.is_grad_enabled():
            probe["calls"].append([r["id"] for r in rows])
        return real_cand(model, ro_, rows, dev, perms=perms)

    def loss(c, batch, perms, lg, rel_by_row, step, *a, **k):
        out = real_loss(c, batch, perms, lg, rel_by_row, step, *a, **k)
        probe["micro"].append((int(step), float(out[0].detach()), [r["id"] for r in batch]))
        return out

    def clip(params, max_norm, *a, **k):
        params = list(params)
        probe["grads"].append(torch.cat([p.grad.detach().reshape(-1).clone() for p in params if p.grad is not None]))
        gn = _REAL_CLIP(params, max_norm, *a, **k)
        probe["gn"].append(float(gn))
        torch.save(probe, Path(work) / f"probe_{tag}_r{rank}.pt")
        return gn
    mod.cand_logits, mod.compute_loss = cand, loss
    torch.nn.utils.clip_grad_norm_ = clip


def _rows():
    """96-odd rows in whole units, the round-1 row kinds: yes/no with complement and inv twins (kd and kd_full targets,
    anchor rows), choice with inv + equiv twins (kd targets), ordinal choice rows (option_level), gold_probs rows."""
    rng = random.Random(20261006)
    words = "the policy says a refund is due within thirty days unless the item was opened or damaged by the buyer".split()
    text = lambda n: " ".join(rng.choice(words) for _ in range(n))  # noqa: E731
    rows, rels = [], []

    def base(rid, call, qtype, **kw):
        return {"id": rid, "group_id": "g_" + call, "call_id": call, "split": "train", "track": "L1", "source": "syn",
                "state": text(rng.choice([20, 60, 150, 400])), "qtype": qtype, "instructions": "Is the refund due?",
                "options": None, "gold": 1, "role": "aff", "meta": {}, **kw}
    for i in range(12):
        c = f"yn{i}"
        rows += [base(f"{c}_a", c, "noul", gold=1, meta={"teacher": {"yes": 0.8}, "anchor": i % 3 == 0}),
                 base(f"{c}_n", c, "noul", gold=0, role="neg"),
                 base(f"{c}_i", c, "noul", gold=1, role="inj", meta={"anchor": i % 4 == 1})]
        rels += [{"a": f"{c}_a", "b": f"{c}_n", "type": "complement"}, {"a": f"{c}_a", "b": f"{c}_i", "type": "inv"}]
    for i in range(10):
        c, o = f"ch{i}", [f"option {j} {text(2)}" for j in range(3 + i % 3)]
        t = {x: round(1.0 / len(o), 6) for x in o}
        t[o[0]] += round(1 - sum(t.values()), 6)
        rows += [base(f"{c}_a", c, "choice", options=o, gold=o[i % len(o)], instructions="Which option applies?",
                      meta={"teacher": t} if i % 2 else {}),
                 base(f"{c}_i", c, "choice", options=o, gold=o[i % len(o)], instructions="Which option applies?")]
        rels += [{"a": f"{c}_a", "b": f"{c}_i", "type": "inv"}, {"a": f"{c}_a", "b": f"{c}_i", "type": "equiv"}]
    for i in range(10):
        c, k = f"or{i}", 4 + i % 2
        lv = [f"level {j}" for j in range(k)]
        o = rng.sample(lv, k)
        rows.append(base(f"{c}_a", c, "choice", options=o, gold=lv[i % k], instructions="How severe is it?",
                         meta={"option_level": {x: j for j, x in enumerate(lv)}}))
    for i in range(6):
        c, o = f"gp{i}", ["low", "medium", "high"]
        rows.append(base(f"{c}_a", c, "choice", options=o, gold="medium", instructions="What is the risk?",
                         meta={"gold_probs": {"low": 0.2, "medium": 0.5, "high": 0.3}}))
    for i in range(6):
        c = f"kf{i}"
        rows.append(base(f"{c}_a", c, "noul", gold=1, source="gd_full", meta={"teacher": {"yes": 0.37 + 0.05 * i}}))
    return rows, rels


def _cfg(n_rows: int) -> dict:
    return {"base": "tiny-qwen3", "recipe": "A3", "batch": 16, "epochs": 2.5 * 16 / n_rows, "lr": 5e-4, "lam": 1.0,
            "beta": 0.1, "kd": 0.5, "kd_full_src": ["gd_full"], "lam_inv": 1.0, "sym_cons": True, "perm_twin": 0.3,
            "lam_p": 0.5, "lam_ord": 1.0, "aux_norm": "batch", "seed": 20261006, "grad_ckpt": False, "style": "cygnet",
            "layout": "schema_branch_mark", "micro_tokens": 1024, "log_every": 1, "ckpt_every_min": 0,
            "snap_every": 2, "train_file": "train.jsonl", "rel_file": "rels.jsonl"}


def _load_orig(path: str):
    spec = importlib.util.spec_from_file_location("train_decoder_orig", path)
    m = importlib.util.module_from_spec(spec)
    sys.modules["train_decoder_orig"] = m
    spec.loader.exec_module(m)
    return m


def _one_process(mod, cfg, work: Path, tag: str) -> dict:
    install(0, str(work), mod.__name__, tag)
    try:
        res = mod.train(dict(cfg), work, work / tag, dev="cpu")
    finally:
        torch.nn.utils.clip_grad_norm_ = _REAL_CLIP
    return res["meta"]


def _fresh_worker(kind: str, orig_path: str, cfg: dict, work: str, tag: str, q):
    decoder_io.STYLE = "cygnet"
    if kind == "orig":
        mod = _load_orig(orig_path)
    else:  # the DDP loop is built from train_decoder.train's source first: the default path must not notice
        train_ddp._built()
        mod = td
    q.put(_one_process(mod, cfg, Path(work), tag))


def _fresh(kind: str, orig_path: str, cfg: dict, work: Path, tag: str) -> dict:
    """One single-process run in a fresh process, like each DDP rank: the first import of the transformers model
    module (inside train(), after the seed) draws from Python's global random, so an in-process run that imported it
    earlier would draw different batches."""
    import multiprocessing as mp
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    pr = ctx.Process(target=_fresh_worker, args=(kind, orig_path, cfg, str(work), tag, q))
    pr.start()
    meta = q.get()
    pr.join()
    if pr.exitcode != 0:
        raise RuntimeError(f"fresh run {tag} exit code {pr.exitcode}")
    return meta


def _ddp(cfg, work: Path, tag: str, nproc: int, **kw) -> dict:
    return train_ddp.launch_ddp(dict(cfg, **kw), work, work / tag, nproc, dev="cpu", style="cygnet", logdir=work / f"logs_{tag}",
                         setup=(install, (str(work), "train_decoder", tag)))


def _probe(work: Path, tag: str, rank: int = 0) -> dict:
    return torch.load(work / f"probe_{tag}_r{rank}.pt", weights_only=False)


def _adapter(work: Path, tag: str) -> dict:
    return torch.load(work / tag / "adapter.pt", weights_only=False)


def _step_losses(probes: list) -> dict:
    out = {}
    for p in probes:
        for s, v, _ in p["micro"]:
            out[s] = out.get(s, 0.0) + v
    return out


def _rel(a: torch.Tensor, b: torch.Tensor) -> float:
    return float((a.double() - b.double()).norm() / b.double().norm().clamp_min(1e-30))


def _max_rel_elem(a: torch.Tensor, b: torch.Tensor) -> float:
    return float((a.double() - b.double()).abs().max() / b.double().abs().max().clamp_min(1e-30))


def _log(meta: dict) -> list:
    return [{k: v for k, v in r.items() if k != "min"} for r in meta["log"]]


def _split_ok(probes: list, ref_probe: dict, rows: list) -> dict:
    """Per step: the ranks' rows are disjoint, together exactly the one-process batch, and no unit is split."""
    call = {r["id"]: r["call_id"] for r in rows}
    ref = {}
    for s, _, ids in ref_probe["micro"]:
        ref.setdefault(s, set()).update(ids)
    out = {"steps": [], "ok": True}
    for s in sorted(ref):
        per = [set(i for st, _, ids in p["micro"] if st == s for i in ids) for p in probes]
        units = [set(call[i] for i in x) for x in per]
        ok = (set().union(*per) == ref[s] and sum(len(x) for x in per) == len(ref[s])
              and all(not (units[a] & units[b]) for a in range(len(units)) for b in range(a + 1, len(units))))
        out["steps"].append({"step": s, "rows_per_rank": [len(x) for x in per], "units_per_rank": [len(u) for u in units],
                             "ok": ok})
        out["ok"] &= ok
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--orig", required=True, help="git HEAD copy of train_decoder.py (the pinned trainer)")
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    t0 = time.time()
    work = Path(a.work)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    rows, rels = _rows()
    (work / "train.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (work / "rels.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    decoder_io.STYLE = "cygnet"
    tok = decoder_io.load_tokenizer(TOK_ID)
    with open(work / "readout.pkl", "wb") as f:
        pickle.dump(decoder_io.Readout(tok), f)
    print(json.dumps({"prepared": len(rows), "s": round(time.time() - t0, 1)}), flush=True)
    cfg = _cfg(len(rows))
    mA = _fresh("orig", a.orig, cfg, work, "A")
    mB = _fresh("new", a.orig, cfg, work, "B")
    print(json.dumps({"done": "A,B", "s": round(time.time() - t0, 1)}), flush=True)
    rC = _ddp(cfg, work, "C", 2)
    rE = _ddp(cfg, work, "E", 1)
    print(json.dumps({"done": "C,E", "s": round(time.time() - t0, 1)}), flush=True)
    rD1 = _ddp(cfg, work, "D", 2, stop_at_step=2)
    for r in (0, 1):
        shutil.copy(work / f"probe_D_r{r}.pt", work / f"probe_D1_r{r}.pt")
    rD2 = _ddp(cfg, work, "D", 2, expect_resume=True)
    print(json.dumps({"done": "D", "s": round(time.time() - t0, 1)}), flush=True)
    report(work, rows, mA, mB, rC, rE, rD1, rD2, t0, a.orig)


def report(work, rows, mA, mB, rC, rE, rD1, rD2, t0, orig):
    TOL = 1e-5
    pA, pB, pE = _probe(work, "A"), _probe(work, "B"), _probe(work, "E")
    pC = [_probe(work, "C", r) for r in (0, 1)]
    pD1 = [_probe(work, "D1", r) for r in (0, 1)]
    pD2 = [_probe(work, "D", r) for r in (0, 1)]
    wA, wB, wC, wD, wE = (_adapter(work, t) for t in ("A", "B", "C", "D", "E"))
    n = len(pB["grads"])
    lB, lC = _step_losses([pB]), _step_losses(pC)
    default_same = {
        "logs_equal": _log(mA) == _log(mB),
        "losses_equal": [v for _, v, _ in pA["micro"]] == [v for _, v, _ in pB["micro"]],
        "grads_bit_equal": len(pA["grads"]) == n and all(torch.equal(x, y) for x, y in zip(pA["grads"], pB["grads"])),
        "weights_bit_equal": wA.keys() == wB.keys() and all(torch.equal(wA[k], wB[k]) for k in wA)}
    default_same["pass"] = all(default_same.values())
    steps = []
    for s in range(n):
        steps.append({"step": s, "loss_1proc": lB[s], "loss_2proc": lC[s],
                      "loss_rel_diff": abs(lC[s] - lB[s]) / max(abs(lB[s]), 1e-30),
                      "grad_rel_l2_diff": _rel(pC[0]["grads"][s], pB["grads"][s]),
                      "grad_max_elem_rel_diff": _max_rel_elem(pC[0]["grads"][s], pB["grads"][s]),
                      "grad_norm_1proc": pB["gn"][s], "grad_norm_2proc": pC[0]["gn"][s],
                      "ranks_hold_same_grad": torch.equal(pC[0]["grads"][s], pC[1]["grads"][s])})
    wrel = max(_rel(wC[k], wB[k]) for k in wB)
    ddp2 = {"steps": steps, "weights_after_3_steps_max_rel_diff": wrel,
            "logged_terms_equal_at_4dp": _log(mB) == [{k: v for k, v in r.items() if k != "min"}
                                                       for r in rC["meta"]["log"]],
            "split": _split_ok(pC, pB, rows)}
    ddp2["pass"] = (n == 3 and all(x["loss_rel_diff"] <= TOL and x["grad_rel_l2_diff"] <= TOL
                                   and x["grad_max_elem_rel_diff"] <= TOL and x["ranks_hold_same_grad"] for x in steps)
                    and wrel <= TOL and ddp2["split"]["ok"])
    resume = {"stopped_at": rD1.get("next_step"), "weights_bit_equal_to_straight_2proc": all(torch.equal(wD[k], wC[k]) for k in wC),
              "grads_bit_equal": all(torch.equal(x, y) for x, y in zip(pD1[0]["grads"] + pD2[0]["grads"], pC[0]["grads"])),
              "logs_equal": _log(rD2["meta"]) == [{k: v for k, v in r.items() if k != "min"} for r in rC["meta"]["log"]]}
    resume["pass"] = resume["stopped_at"] == 2 and all(v for k, v in resume.items() if k != "stopped_at")
    one = {"grads_bit_equal": all(torch.equal(x, y) for x, y in zip(pE["grads"], pB["grads"])) and len(pE["grads"]) == n,
           "weights_bit_equal": all(torch.equal(wE[k], wB[k]) for k in wB),
           "logs_equal": _log(mB) == [{k: v for k, v in r.items() if k != "min"} for r in rE["meta"]["log"]]}
    one["pass"] = all(one.values())
    import transformers
    out = {"test": "PREREG_FINAL A20 (c) adoption test 1: CPU gloo, 1 vs 2 ranks, tiny Qwen3-like model, 3 steps",
           "pass": default_same["pass"] and ddp2["pass"] and resume["pass"] and one["pass"], "tolerance_rel": TOL,
           "A_vs_B_default_path_unchanged": default_same, "B_vs_C_1proc_vs_2_gloo_ranks": ddp2,
           "C_vs_D_ddp_stop_and_resume": resume, "B_vs_E_ddp_world_1": one,
           "setup": {"model": "Qwen3ForCausalLM 2 layers, hidden 64, 4 heads (2 kv), fp32, tokenizer " + TOK_ID,
                     "trained_tensors": sum(v.numel() for v in wB.values()), "rows": len(rows), "cfg": _cfg(len(rows)),
                     "steps": n, "micro_batches_per_step_1proc": [sum(1 for s, _, _ in pB["micro"] if s == k) for k in range(n)],
                     "micro_batches_per_step_per_rank_2proc": [[sum(1 for s, _, _ in p["micro"] if s == k) for p in pC]
                                                              for k in range(n)]},
           "env": {"torch": torch.__version__, "transformers": transformers.__version__, "python": sys.version.split()[0]},
           "code_sha256": {"train_decoder.py": hashlib.sha256((LEAN / "train_decoder.py").read_bytes()).hexdigest(),
                           "A_orig_copy": hashlib.sha256(Path(orig).read_bytes()).hexdigest(),
                           "c_build/ddp/train_ddp.py": train_ddp.CODE_SHA},
           "ddp_hunks": len(train_ddp.HUNKS),
           "seconds": round(time.time() - t0, 1)}
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps({"pass": out["pass"], "default": default_same["pass"], "ddp2": ddp2["pass"],
                      "resume": resume["pass"], "world1": one["pass"], "wrote": str(OUT)}), flush=True)


if __name__ == "__main__":
    main()
