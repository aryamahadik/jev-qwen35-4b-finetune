"""PRISM write-blocked recurrent memory, prototype on Qwen3.5 (Gated DeltaNet layers).

In every Gated DeltaNet layer, the per-token write strength beta (how much a token writes into the recurrent state)
and log-decay g (how much the state is forgotten) are set to 0 for UNTRUSTED tokens on a subset of "policy" heads.
So untrusted text cannot write into, overwrite or erase those heads' memory; it can still be read through the other
("data") heads. Trusted = everything outside the TEXT/state span (system prompt, question, options, answer slot).

Known leaks (not closed in this prototype): the width-4 causal conv1d mixes a few evidence tokens into the next
trusted tokens, and the 25% full-attention layers mix everything into later layers' hidden states.
Usage: install(model_module, policy_frac); set_mask(bool tensor [B, T], True = untrusted) before each forward.
"""
from __future__ import annotations

import torch

STATE = {"mask": None, "policy_frac": 0.5, "enabled": False, "capture": None}


def install(modeling_module, policy_frac=0.5):
    """Wrap the module-level delta-rule functions the Gated DeltaNet layer calls (chunked prefill + recurrent)."""
    STATE["policy_frac"] = policy_frac
    for fname in ("torch_chunk_gated_delta_rule", "torch_recurrent_gated_delta_rule"):
        orig = getattr(modeling_module, fname)
        if getattr(orig, "_writeblock", False):
            continue

        def wrapped(query, key, value, g, beta, *args, _orig=orig, **kw):
            m = STATE["mask"]
            if STATE["enabled"] and m is not None and m.shape[1] == beta.shape[1]:
                H = beta.shape[-1]
                hp = max(1, int(H * STATE["policy_frac"]))
                block = m[:, :, None].to(beta.device) & (torch.arange(H, device=beta.device) < hp)[None, None, :]
                beta = beta.masked_fill(block, 0.0)  # no write
                g = g.masked_fill(block, 0.0)        # no decay/erase (log-decay 0 = keep state)
            out = _orig(query, key, value, g=g, beta=beta, *args, **kw)
            if STATE["capture"] is not None:
                STATE["capture"].append(out[0].detach())
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
