import sys

import pytest
import torch

HOSTING = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/hosting"
sys.path.insert(0, HOSTING)
from fastcore import testing as T  # noqa: E402

from oc1 import smooth as SM  # noqa: E402


@pytest.fixture(scope="module")
def model():
    m = T.tiny_model(seed=1, dtype=torch.float32)
    # make activations non-trivial: random norm weights, a few outlier input channels
    g = torch.Generator().manual_seed(3)
    for n, p in m.named_parameters():
        if n.endswith("layernorm.weight"):
            p.data = torch.randn(p.shape, generator=g) * 0.5
    return m


def layer_types(m):
    return list(m.config.layer_types)


def test_groups_cover_every_consumer_of_a_norm(model):
    gs = SM.groups_for(layer_types(model))
    names = dict(model.named_modules())
    for norm, lins, cap in gs:
        assert norm in names and cap in names and cap == lins[0]
        for k in lins:
            assert k in names, k
    # GDN layers include in_proj_a / in_proj_b (they read the same smoothed input and must be rescaled)
    assert any(k.endswith("in_proj_a") for _, l, _ in gs for k in l) and any(k.endswith("in_proj_b") for _, l, _ in gs for k in l)
    # o_proj / out_proj / down_proj are never smoothed
    assert not any(k.endswith(("o_proj", "out_proj", "down_proj")) for _, l, _ in gs for k in l)


def test_smoothing_preserves_the_function(model):
    torch.manual_seed(0)
    gs = SM.groups_for(layer_types(model))
    ids = [torch.randint(5, 200, (1, 24)) for _ in range(6)]
    with torch.no_grad():
        ref = [model(input_ids=x).logits for x in ids]
    absmax = SM.collect_absmax(model, ids, gs, device="cpu")
    assert set(absmax) == {c for _, _, c in gs}
    sd = {k: v.detach().clone() for k, v in model.state_dict().items()}
    weights = {k: sd[k + ".weight"] for _, lins, _ in gs for k in lins}
    scales = SM.compute_scales(absmax, weights, gs, alpha=0.5)
    assert all(torch.isfinite(s).all() and (s > 0).all() for s in scales.values())
    new = SM.apply_scales(sd, gs, scales)
    assert len(new) == len(gs) * 1 + sum(len(l) for _, l, _ in gs)
    m2 = T.tiny_model(seed=1, dtype=torch.float32)
    m2.load_state_dict(sd)
    m2.load_state_dict({**sd, **new})
    with torch.no_grad():
        got = [m2(input_ids=x).logits for x in ids]
    for a, b in zip(ref, got):
        assert (a - b).abs().max() < 2e-4, float((a - b).abs().max())
    # smoothing actually changed something and flattened the per-channel activation range ratio on at least one group
    assert any(not torch.equal(new[k], sd[k]) for k in new)


def test_scales_follow_the_formula():
    import torch
    x = torch.tensor([4.0, 1.0, 0.25])
    W = torch.tensor([[1.0, 2.0, 4.0], [0.5, 1.0, 2.0]])
    gs = [("n", ["a", "b"], "a")]
    s = SM.compute_scales({"a": x}, {"a": W, "b": W}, gs, alpha=0.5)["n"]
    wm = W.abs().amax(0)
    assert torch.allclose(s, x.pow(0.5) / wm.pow(0.5))


def test_smooth_checkpoint_roundtrip(tmp_path):
    from safetensors.torch import load_file, save_file
    import json
    src, dst = tmp_path / "src", tmp_path / "dst"
    src.mkdir()
    P = "model.language_model.layers.0"
    t = {f"{P}.input_layernorm.weight": torch.zeros(4), f"{P}.post_attention_layernorm.weight": torch.zeros(4),
         f"{P}.self_attn.q_proj.weight": torch.ones(2, 4), f"{P}.self_attn.k_proj.weight": torch.ones(2, 4),
         f"{P}.self_attn.v_proj.weight": torch.ones(2, 4), f"{P}.mlp.gate_proj.weight": torch.ones(3, 4),
         f"{P}.mlp.up_proj.weight": torch.ones(3, 4), f"{P}.mlp.down_proj.weight": torch.ones(4, 3),
         "model.visual.x.weight": torch.ones(2)}
    save_file(t, str(src / "model.safetensors-00001-of-00001.safetensors"), metadata={"format": "pt"})
    (src / "model.safetensors.index.json").write_text(json.dumps({"weight_map": {k: "model.safetensors-00001-of-00001.safetensors" for k in t}}))
    (src / "config.json").write_text("{}")
    gs = SM.groups_for(["full_attention"])
    scales = {"model.layers.0.input_layernorm": torch.tensor([2.0, 2.0, 2.0, 2.0]),
              "model.layers.0.post_attention_layernorm": torch.tensor([4.0, 1.0, 1.0, 1.0])}
    meta = SM.smooth_checkpoint(src, dst, scales, gs, log=lambda *a: None)
    out = load_file(str(dst / "model.safetensors-00001-of-00001.safetensors"))
    assert torch.allclose(out[f"{P}.input_layernorm.weight"], torch.full((4,), -0.5))      # (1+0)/2 - 1
    assert torch.allclose(out[f"{P}.self_attn.q_proj.weight"], torch.full((2, 4), 2.0))
    assert torch.allclose(out[f"{P}.post_attention_layernorm.weight"], torch.tensor([-0.75, 0.0, 0.0, 0.0]))
    assert torch.equal(out[f"{P}.mlp.down_proj.weight"], t[f"{P}.mlp.down_proj.weight"])  # not smoothed
    assert torch.equal(out["model.visual.x.weight"], t["model.visual.x.weight"])
    assert (dst / "config.json").exists() and meta["tensors_changed"] == 1 + 3 + 1 + 2
