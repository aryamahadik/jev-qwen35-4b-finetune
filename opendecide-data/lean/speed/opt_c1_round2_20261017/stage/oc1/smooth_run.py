"""oc1.smooth_run: calibration + SmoothQuant transform of the merged C1 checkpoint (runs under /opt/fastpath python).

    python -m oc1.smooth_run --src /out/models/q35_4b_main500k_merged --dst /out/models/q35_4b_main500k_merged__smooth
                             [--n 96] [--alpha 0.5] [--device cuda]

Calibration = the first view of N dev decisions of the parity set P (a stratified draw with seed 1; prompts <= 1,500 tokens
so the system header that carries the massive activations is intact), run through the BF16 model with forward pre-hooks on
the first consumer of every norm. Only dev prompts; no labels are read. Output folder = the merged folder with the smoothed
norms / linears (oc1.smooth) + smooth_manifest.json; the INT8 arm then serves it with OC1_ONLINE_MODE=int8.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    ap.add_argument("--work", default="/root/work")
    ap.add_argument("--n", type=int, default=96)
    ap.add_argument("--alpha", type=float, default=0.5)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--out", default="/tmp/smooth_result.json")
    a = ap.parse_args(argv)
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import torch
    from oc1 import common as C
    from oc1 import items as I
    from oc1 import parity as PAR
    from oc1 import smooth as SM
    t0 = time.time()
    src = Path(a.src)
    tok, ro, _ = I.load_c1(src / "c1_tokenizer")
    R = I.readout_mod()
    items = [it for it in I.load_items(a.work, "P")]
    pick = PAR.stratified_sample(items, a.n * 2, seed=1)
    ids = []
    for it in pick:
        p = I.prepare_one(it, R, ro, tok)
        if p.items[0].n_tokens <= 1500:
            ids.append(torch.tensor([p.items[0].ids]))
        if len(ids) >= a.n:
            break
    dio = R.dio
    from transformers import AutoModelForCausalLM
    try:
        model = AutoModelForCausalLM.from_pretrained(str(src), dtype=torch.bfloat16, attn_implementation="sdpa")
    except (ValueError, KeyError):
        from transformers import AutoModelForImageTextToText
        model = AutoModelForImageTextToText.from_pretrained(str(src), dtype=torch.bfloat16, attn_implementation="sdpa")
    model = model.to(a.device).eval()
    cfg = getattr(model.config, "text_config", model.config)
    types = list(cfg.layer_types)
    names = dict(model.named_modules())
    mod_prefix = "model.language_model.layers" if f"model.language_model.layers.0.input_layernorm" in names else "model.layers"
    g_mod = SM.groups_for(types, mod_prefix)
    g_std = SM.groups_for(types, "model.layers")
    absmax = SM.collect_absmax(model, ids, g_mod, device=a.device)
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    weights = {k: sd[k + ".weight"] for _, lins, _ in g_mod for k in lins}
    scales_mod = SM.compute_scales(absmax, weights, g_mod, alpha=a.alpha)
    scales_std = {gs[0]: scales_mod[gm[0]] for gm, gs in zip(g_mod, g_std)}
    del model
    torch.cuda.empty_cache()
    meta = SM.smooth_checkpoint(src, a.dst, scales_std, g_std, key_prefix="model.language_model.layers")
    meta.update({"alpha": a.alpha, "n_calibration_prompts": len(ids), "calibration_tokens": sum(int(x.shape[1]) for x in ids),
                 "wall_s": round(time.time() - t0, 1)})
    Path(a.dst, "smooth_manifest.json").write_text(json.dumps(meta, indent=1))
    Path(a.out).write_text(json.dumps(meta))
    print(json.dumps(meta))
    return 0


if __name__ == "__main__":
    sys.exit(main())
