"""CPU check of vb_core.Reader.read (shared-ViT embedding splice, padded batch) against Reader.read_stock (stock multimodal forward)
on a tiny random Qwen3.5 composite (same transformers 5.17). Also: batch invariance and the effect of the 256 padding bucket."""
import os, sys, random
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/vision_bench/review")
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/vision_bench/harness")
os.environ["HF_HUB_OFFLINE"] = "1"
import torch
from tiny_common import tiny_config
from transformers import AutoModelForImageTextToText
import vb_core as vb

torch.manual_seed(1); random.seed(1)
model = AutoModelForImageTextToText.from_config(tiny_config()).eval()
rd = vb.Reader.__new__(vb.Reader)
rd.dev = "cpu"; rd.which = "tiny"; rd.top = model; rd.inner = model.model; rd.head = model.lm_head; rd.cfg = model.config
rd.image_token_id = 5; rd.pad_id = 0

def make_prep(h, w, n_views, n_cand, text_len):
    n_img = h * w // 4
    pv = torch.randn(h * w, 3 * 2 * 16 * 16)
    grid = torch.tensor([[1, h, w]])
    seqs = []
    for v in range(n_views):
        pre = [random.randint(10, 390) for _ in range(text_len)]
        post = [random.randint(10, 390) for _ in range(text_len // 2 + 3 * v)]
        seqs.append(pre + [3] + [5] * n_img + [4] + post)
    groups = [[10 + i] for i in range(n_cand)]
    return {"seqs": seqs, "pv": pv, "grid": grid, "groups": groups, "n_img": n_img}

preps = [make_prep(4, 6, 2, 3, 20), make_prep(8, 8, 1, 2, 31), make_prep(6, 4, 2, 9, 12)]
with torch.no_grad():
    batch = rd.read(preps)
    worst = 0.0
    for i, p in enumerate(preps):
        single = rd.read([p])[0]
        stock = rd.read_stock(p)
        for a, b, c in zip(batch[i], single, stock):
            worst = max(worst, float((a - c).abs().max()), float((b - c).abs().max()))
            print(f"item {i}: |batch-stock| {float((a - c).abs().max()):.2e}  |single-stock| {float((b - c).abs().max()):.2e}")
print("worst abs logit diff (fp32 CPU):", worst)
vb.PAD_MULTIPLE = 8
with torch.no_grad():
    b8 = rd.read(preps)
print("256-bucket vs 8-bucket worst diff:", max(float((x - y).abs().max()) for i in range(3) for x, y in zip(batch[i], b8[i])))
# sensitivity: are the logits large enough, and do they respond to the image? (so the 1e-7 agreement is not vacuous)
with torch.no_grad():
    p = preps[0]
    base = rd.read([p])[0][0]
    p2 = dict(p); p2["pv"] = torch.randn_like(p["pv"]) * 3
    alt = rd.read([p2])[0][0]
    print("logit scale:", float(base.abs().max()), "| change when pixels replaced:", float((base - alt).abs().max()))
    st2 = rd.read_stock(p2)[0]
    print("stock path sees the same change:", float((alt - st2).abs().max()))
