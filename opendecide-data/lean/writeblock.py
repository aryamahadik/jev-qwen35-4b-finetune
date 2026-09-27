"""PRISM write-blocked recurrent memory, prototype on Qwen3.5 (Gated DeltaNet layers).

In every Gated DeltaNet layer, the per-token write strength beta (how much a token writes into the recurrent state)
and log-decay g (how much the state is forgotten) are set to 0 for UNTRUSTED tokens on a subset of "policy" heads.
So untrusted text cannot write into, overwrite or erase those heads' memory; it can still be read through the other
("data") heads. Trusted = everything outside the TEXT/state span (system prompt, question, options, answer slot).
With beta = 0 the delta-rule write term is zero and with g = 0 the decay factor is exp(0) = 1, so a policy head's
state after an untrusted span equals its state before it (up to kernel arithmetic). What is READ from that state is
not protected: the query and output gate at later positions still depend on the evidence (PRISM_2B_MASTER_PLAN.md §4).

Known leaks (not closed in this prototype): the width-4 causal conv1d mixes a few evidence tokens into the next
trusted tokens, and the full-attention layers mix everything into later layers' hidden states.
Usage: install(model_module, policy_frac); set STATE["mask"] (bool [B, T], True = untrusted) before each forward.
Optional (P0 checks): STATE["heads"] = list with one bool [H] tensor per Gated DeltaNet layer (in call order) instead
of "the first policy_frac of heads"; STATE["mode"] = "both" | "beta" | "g"; call reset() before each forward so the
layer counter restarts; STATE["capture_state"] = [] records every layer's final recurrent state.
"""
from __future__ import annotations

import torch

STATE = {"mask": None, "policy_frac": 0.5, "enabled": False, "capture": None, "heads": None, "mode": "both",
         "calls": 0, "applied": 0, "n_layers": None, "capture_state": None, "capture_beta": None}


def reset():
    STATE["calls"] = 0
    STATE["applied"] = 0


def install(modeling_module, policy_frac=0.5):
    """Wrap the module-level delta-rule functions the Gated DeltaNet layer calls (chunked prefill + recurrent).
    The layer's forward looks these names up in its module at call time, and the fla / hub kernel is chosen inside
    them, so the wrapper runs on either kernel path (P0 check T0b counts the calls)."""
    STATE["policy_frac"] = policy_frac
    for fname in ("torch_chunk_gated_delta_rule", "torch_recurrent_gated_delta_rule"):
        orig = getattr(modeling_module, fname)
        if getattr(orig, "_writeblock", False):
            continue

        def wrapped(query, key, value, g, beta, *args, _orig=orig, **kw):
            k = STATE["calls"] if STATE["n_layers"] is None else STATE["calls"] % STATE["n_layers"]
            STATE["calls"] += 1
            m = STATE["mask"]
            if STATE["capture_beta"] is not None and m is not None and m.shape[1] == beta.shape[1]:
                mm = m.to(beta.device).float()[:, :, None]  # mean write strength per head over untrusted tokens
                STATE["capture_beta"].append(((beta.float() * mm).sum((0, 1)) / mm.sum((0, 1)).clamp_min(1)).cpu())
            if STATE["enabled"] and m is not None and m.shape[1] == beta.shape[1]:
                H = beta.shape[-1]
                if STATE["heads"] is not None:
                    hsel = STATE["heads"][k].to(beta.device)
                else:
                    hsel = torch.arange(H, device=beta.device) < max(1, int(H * STATE["policy_frac"]))
                block = m[:, :, None].to(beta.device) & hsel[None, None, :]
                STATE["applied"] += 1
                if STATE["mode"] in ("both", "beta"):
                    beta = beta.masked_fill(block, 0.0)  # no write
                if STATE["mode"] in ("both", "g"):
                    g = g.masked_fill(block, 0.0)        # no decay/erase (log-decay 0 = keep state)
            if STATE["capture_state"] is not None:
                kw["output_final_state"] = True
            out = _orig(query, key, value, g=g, beta=beta, *args, **kw)
            if STATE["capture"] is not None:
                STATE["capture"].append(out[0].detach())
            if STATE["capture_state"] is not None:
                STATE["capture_state"].append(out[1].detach().float())
            return out

        wrapped._writeblock = True
        setattr(modeling_module, fname, wrapped)


def untrusted_mask(tok, texts, spans, max_len=16384):
    """spans[i] = (char_start, char_end) of the untrusted state inside texts[i]; returns ([B, T] bool, encoding)."""
    enc = tok(texts, add_special_tokens=False, truncation=True, max_length=max_len, padding="longest",
              return_tensors="pt", return_offsets_mapping=True)
    off = enc.pop("offset_mapping")
    mask = torch.zeros(off.shape[:2], dtype=torch.bool)
    for i, (s, e) in enumerate(spans):
        mask[i] = (off[i, :, 0] >= s) & (off[i, :, 1] <= e) & (off[i, :, 1] > off[i, :, 0])
    return mask, enc
