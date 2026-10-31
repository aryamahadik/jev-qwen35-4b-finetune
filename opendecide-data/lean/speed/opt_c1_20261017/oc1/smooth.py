"""oc1.smooth: SmoothQuant for C1 as a pure BF16 -> BF16 checkpoint transform (the INT8 arm's first half).

SmoothQuant (Xiao et al. 2023) moves activation outliers into the weights: for the input channel j of a group of linears
that share one input X (the output of one RMSNorm),
        s_j = max|X_j|^alpha / max_over_the_group |W_:,j|^(1-alpha)        X' = X / s,   W' = W diag(s)
so  W'X' = WX  exactly. Qwen3.5 has zero-centred RMSNorms (y = x_hat * (1 + w)), so 1/s is folded into the norm:
        (1 + w') = (1 + w) / s        ->   w' = (1 + w) / s - 1
Groups per decoder layer (everything that reads the same normalised hidden state, nothing else is touched):
    input_layernorm       -> self_attn.{q,k,v}_proj                          (full-attention layers)
                          -> linear_attn.{in_proj_qkv, in_proj_z, in_proj_a, in_proj_b}   (GDN layers)
    post_attention_layernorm -> mlp.{gate_proj, up_proj}
in_proj_a / in_proj_b stay BF16 in the INT8 arm but MUST be rescaled too (they read the same smoothed input). o_proj,
out_proj and down_proj have no norm in front: they are not smoothed (plain per-channel / per-token quantization).
The transform keeps the function (tests: logits equal to ~1e-5 in fp32). The quantization itself is done online by
oc1/pypatch (OC1_ONLINE_MODE=int8) when the server loads the smoothed folder.

  groups_for(layer_types, prefix)       [(norm_key, [linear_key...], capture_key)]
  collect_absmax(model, batches, ...)   per-input-channel max |X| at each group's capture linear (forward pre-hooks)
  compute_scales(absmax, weights, ...)  {norm_key: s}
  apply_scales(tensors, groups, scales) {name: new tensor} for the norms and every linear in the groups
  smooth_checkpoint(src, dst, scales)   rewrite the safetensors shards (names as the base layout: model.language_model.layers.N...)
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path


def groups_for(layer_types: list, prefix: str = "model.layers") -> list:
    out = []
    for i, lt in enumerate(layer_types):
        L = f"{prefix}.{i}"
        if lt == "full_attention":
            lins = [f"{L}.self_attn.q_proj", f"{L}.self_attn.k_proj", f"{L}.self_attn.v_proj"]
        else:
            lins = [f"{L}.linear_attn.in_proj_qkv", f"{L}.linear_attn.in_proj_z", f"{L}.linear_attn.in_proj_a",
                    f"{L}.linear_attn.in_proj_b"]
        out.append((f"{L}.input_layernorm", lins, lins[0]))
        out.append((f"{L}.post_attention_layernorm", [f"{L}.mlp.gate_proj", f"{L}.mlp.up_proj"], f"{L}.mlp.gate_proj"))
    return out


def collect_absmax(model, batches, groups: list, device: str = "cuda") -> dict:
    """Run `batches` (iterable of input_ids tensors [1, T]) through the text model; return {capture_key: absmax[in_features]}."""
    import torch
    mods = dict(model.named_modules())
    acc, hooks = {}, []

    def make(key):
        def pre(module, args):
            x = args[0].detach()
            m = x.abs().reshape(-1, x.shape[-1]).amax(0).float().cpu()
            acc[key] = m if key not in acc else torch.maximum(acc[key], m)
        return pre

    for _, _, cap in groups:
        hooks.append(mods[cap].register_forward_pre_hook(make(cap)))
    try:
        with torch.no_grad():
            for ids in batches:
                model(input_ids=ids.to(device))
    finally:
        for h in hooks:
            h.remove()
    return acc


def compute_scales(absmax: dict, weights: dict, groups: list, alpha: float = 0.5, smin: float = 1e-5, smax: float = 1e5) -> dict:
    """weights {linear_key: tensor[out, in]}; -> {norm_key: s[in]} (float32)."""
    import torch
    scales = {}
    for norm, lins, cap in groups:
        xm = absmax[cap].float().clamp(min=1e-5)
        wm = torch.stack([weights[k].float().abs().amax(0) for k in lins]).amax(0).clamp(min=1e-5)
        s = (xm.pow(alpha) / wm.pow(1.0 - alpha)).clamp(smin, smax)
        scales[norm] = s
    return scales


def apply_scales(tensors: dict, groups: list, scales: dict, suffix: str = ".weight") -> dict:
    """tensors {name: tensor} must hold every norm / linear of the groups. Returns {name: new tensor} (same dtype)."""
    import torch
    new = {}
    for norm, lins, _ in groups:
        s = scales[norm].float()
        w = tensors[norm + suffix]
        new[norm + suffix] = (((1.0 + w.float()) / s) - 1.0).to(w.dtype)
        for k in lins:
            W = tensors[k + suffix]
            new[k + suffix] = (W.float() * s.unsqueeze(0)).to(W.dtype)
    return new


def smooth_checkpoint(src_dir, dst_dir, scales: dict, groups: list, key_prefix: str = "model.language_model.layers",
                      log=print) -> dict:
    """Rewrite src_dir's safetensors shards with the scaled tensors (all other tensors and files copied unchanged)."""
    from safetensors import safe_open
    from safetensors.torch import save_file
    src, dst = Path(src_dir), Path(dst_dir)
    dst.mkdir(parents=True, exist_ok=True)
    idx = json.loads((src / "model.safetensors.index.json").read_text())
    shard_of = idx["weight_map"]
    # groups are in model.layers.N... names; map to the checkpoint's prefix
    def ck(name):
        return name.replace("model.layers.", key_prefix + ".", 1)
    need = {}
    for norm, lins, _ in groups:
        for k in [norm] + lins:
            need[ck(k) + ".weight"] = shard_of[ck(k) + ".weight"]
    tensors = {}
    for sh in sorted(set(need.values())):
        with safe_open(str(src / sh), "pt") as f:
            for name, s in need.items():
                if s == sh:
                    tensors[name] = f.get_tensor(name)
    ck_groups = [(ck(n), [ck(x) for x in l], ck(c)) for n, l, c in groups]
    ck_scales = {ck(n): v for n, v in scales.items()}
    new = apply_scales(tensors, ck_groups, ck_scales)
    changed = 0
    for sh in sorted(set(shard_of.values())):
        out = {}
        with safe_open(str(src / sh), "pt") as f:
            meta = f.metadata()
            for name in f.keys():
                if name in new:
                    out[name] = new[name].contiguous()
                    changed += 1
                else:
                    out[name] = f.get_tensor(name)
        save_file(out, str(dst / sh), metadata=meta)
        log(f"smoothed shard {sh}")
    for p in sorted(src.iterdir()):
        if p.is_file() and not p.name.endswith(".safetensors") and p.name != "merge_manifest.json":
            shutil.copyfile(p, dst / p.name)
        elif p.is_dir():
            shutil.copytree(p, dst / p.name, dirs_exist_ok=True)
    meta = {"source": str(src), "alpha": None, "tensors_changed": changed, "groups": len(groups),
            "scale_stats": {k: [float(v.min()), float(v.median()), float(v.max())] for k, v in list(scales.items())[:6]}}
    (dst / "smooth_manifest.json").write_text(json.dumps(meta, indent=1))
    return meta
