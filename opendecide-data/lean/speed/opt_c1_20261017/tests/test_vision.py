import json
import math
import random
import sys

import pytest

from oc1 import common as C
from oc1 import vision as V

VB = C.JEV_ROOT / "vision_bench"


def hf_smart_resize():
    """transformers' own smart_resize, cut out of its source file with ast (the module itself needs torchvision)."""
    import ast
    import importlib.util
    import math as _m
    spec = importlib.util.find_spec("transformers.models.qwen2_vl.image_processing_qwen2_vl")
    src = open(spec.origin).read()
    fn = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "smart_resize")
    ns = {"math": _m}
    exec(compile(ast.Module([fn], []), "smart_resize", "exec"), ns)
    return ns["smart_resize"]


def test_smart_resize_matches_transformers():
    hf = hf_smart_resize()
    rng = random.Random(0)
    for _ in range(400):
        h, w = rng.randint(20, 4000), rng.randint(20, 4000)
        assert V.smart_resize(h, w) == hf(h, w, factor=32, min_pixels=V.MIN_PIXELS, max_pixels=V.MAX_PIXELS), (h, w)
        mp = rng.choice([64, 128, 256, 512, 1024, 2048]) * 1024
        assert V.smart_resize(h, w, max_pixels=mp) == hf(h, w, factor=32, min_pixels=V.MIN_PIXELS, max_pixels=mp), (h, w, mp)


def test_native_token_counts_of_the_benchmark_images():
    assert V.visual_tokens(*V.smart_resize(500, 375)) == 192          # Pets 375x500 (w x h) example
    assert V.visual_tokens(*V.smart_resize(480, 640)) == 300          # VQA 640x480


def test_caps_bound_the_tokens_and_keep_the_aspect():
    for h, w in ((500, 375), (480, 640), (3000, 4000), (4000, 3000)):
        prev = None
        for cap in (1024, 512, 256, 128, 64):
            hh, ww = V.cap_dims(h, w, cap)
            n = V.visual_tokens(hh, ww)
            assert n <= cap and hh % 32 == 0 and ww % 32 == 0 and hh * ww >= V.MIN_PIXELS * 0.5
            assert abs(math.log((ww / hh) / (w / h))) < 0.45
            assert prev is None or n <= prev
            prev = n
        # a cap above the native size is a no-op
        assert V.cap_dims(h, w, 100000) == V.smart_resize(h, w)
    # the server's own resize of a capped image is the identity (so the predicted token count is what it will report)
    hh, ww = V.cap_dims(3000, 4000, 256)
    assert V.smart_resize(hh, ww) == (hh, ww)


def test_upscale_dims_hit_the_target():
    for tgt in (1024, 2048, 4096):
        n = V.visual_tokens(*V.upscale_dims(500, 375, tgt))
        assert 0.7 * tgt <= n <= 1.12 * tgt, (tgt, n)


def test_decide_matches_decoder_io_to_probs():
    from oc1 import items as I          # puts hosting/ and lean/ on sys.path
    from fastcore import testing as T
    dio = I.readout_mod().dio
    T.c1_tokenizer()                    # sets decoder_io's LAYOUT/STYLE from C1's train_meta
    import torch
    rng = random.Random(1)
    row = {"qtype": "choice", "options": ["a", "b", "c", "d"]}
    for perm in (None, [3, 2, 1, 0]):
        lg = [rng.uniform(-3, 3) for _ in range(4)]
        mine = V.view_probs(row, lg, perm)
        ref = dio.to_probs(row, torch.tensor(lg), perm, temp=1.0)
        assert all(abs(mine[k] - ref[k]) < 1e-6 for k in ref)
    rown = {"qtype": "noul", "options": None}
    for perm in (None, [1, 0]):
        lg = [0.3, -0.2]
        assert abs(V.view_probs(rown, lg, perm)["yes"] - dio.to_probs(rown, torch.tensor(lg), perm)["yes"]) < 1e-6
    # two-view average, and yes/no -> [p_false, p_true]
    p = V.decide(row, [[1, 0, 0, 0], [0, 0, 0, 1]], [None, [3, 2, 1, 0]])
    assert abs(sum(p) - 1) < 1e-9 and p[0] > p[1]
    assert V.decide(rown, [[2.0, 0.0]], [None]) == pytest.approx([1 - 0.8807970779778823, 0.8807970779778823])


def test_group_logits_parse():
    resp = {"meta_info": {"output_token_ids_logprobs": [[[-1.0, 7, None], [-2.0, 8, None], [-0.5, 9, None]]]}}
    out = V.group_logits(resp, [7, 8, 9], [2, 1])
    assert out[0] == pytest.approx(math.log(math.exp(-1) + math.exp(-2))) and out[1] == pytest.approx(-0.5)
    with pytest.raises(ValueError):
        V.group_logits(resp, [7, 99], [2])


@pytest.mark.skipif(not (VB / "data" / "img_pets" / "cases.jsonl").exists(), reason="vision bench data absent")
def test_pick_cases_and_to_row_on_real_cases():
    cases = V.pick_cases(5, seed=0)
    assert len(cases) == 10 and {c["suite"] for c in cases} == set(V.SUITES)
    for c in cases:
        qname, q = next(iter(c["questions"].items()))
        row, keys = V.to_row(q)
        assert row["state"] == V.IMG_PLACEHOLDER
        g = c["gold"][qname]
        gi = V.gold_index(q, g)
        assert 0 <= gi < len(V.bench_options(q))
        assert (row["qtype"] == "choice") == (q["type"] == "choice")
    # the copies of vb_core's logic agree with vb_core itself
    sys.path.insert(0, str(VB / "harness" / "vendor"))
    sys.path.insert(0, str(VB / "harness"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("vb_core_copy", VB / "harness" / "vb_core.py")
    try:
        vb = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(vb)
    except Exception as e:  # noqa: BLE001
        pytest.skip(f"vb_core not importable here: {type(e).__name__}")
    for c in cases:
        qname, q = next(iter(c["questions"].items()))
        assert vb.to_row(q) == V.to_row(q)
        assert vb.bench_options(q) == V.bench_options(q)
        assert vb.gold_index(q, c["gold"][qname]) == V.gold_index(q, c["gold"][qname])


def test_data_uri_never_starts_with_a_slash():
    """SGLang reads a bare base64 string starting with "/" as a file path; JPEG base64 starts with "/9j/" (17 Oct native-arm failure)."""
    import base64
    from oc1 import vision as V
    jpeg = b"\xff\xd8\xff\xe0" + b"\x00" * 20
    png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 20
    assert base64.b64encode(jpeg).decode().startswith("/9j/")
    assert V.data_uri(jpeg).startswith("data:image/jpeg;base64,/9j/")
    assert V.data_uri(png).startswith("data:image/png;base64,iVBOR")
