"""Reviewer round 2 (CPU): independent mock-logit checks of the option readout / view combine with the real tokenizer."""

import json, os, re, sys, types, hashlib, collections
HERE = os.path.dirname(os.path.abspath(__file__)); VB = os.path.dirname(HERE)
sys.path.insert(0, HERE)
SCR = "/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/adbc4a3b-e366-431b-b0e2-96c55904b928/scratchpad/hf/base_tok"
os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", VB_PROC_DIR=f"{VB}/src/qwen35-4b-processor")
import torch, transformers
import math
def smart_resize(height, width, factor=32, min_pixels=65536, max_pixels=16777216):
    h_bar = round(height / factor) * factor; w_bar = round(width / factor) * factor
    if h_bar * w_bar > max_pixels:
        beta = math.sqrt((height * width) / max_pixels); h_bar = math.floor(height / beta / factor) * factor; w_bar = math.floor(width / beta / factor) * factor
    elif h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (height * width)); h_bar = math.ceil(height * beta / factor) * factor; w_bar = math.ceil(width * beta / factor) * factor
    return h_bar, w_bar
SIZES = json.load(open(f"{VB}/review/tmp/sizes.json"))
CUR = {"size": None}
class FakeIm:
    def __init__(self): self.size = CUR["size"]
    def load(self): pass
    def convert(self, m): return self
class StubProc:
    merge_size = 2
    def __call__(self, images, return_tensors):
        w, h = CUR["size"]
        rh, rw = smart_resize(h, w, factor=32, min_pixels=65536, max_pixels=16777216)
        gh, gw = rh // 16, rw // 16
        return {"pixel_values": torch.zeros(gh * gw, 1536), "image_grid_thw": torch.tensor([[1, gh, gw]])}
class StubAIP:
    @staticmethod
    def from_pretrained(path): return StubProc()
transformers.AutoImageProcessor = StubAIP
fake_pil = types.ModuleType("PIL"); fake_img = types.ModuleType("PIL.Image"); fake_img.open = lambda b: FakeIm(); fake_pil.Image = fake_img
sys.modules["PIL"] = fake_pil; sys.modules["PIL.Image"] = fake_img
import vb_core as vb
vb.ADAPTER = "/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k"


rc = vb.Reader("c1", load_model=False)
cases = vb.load_cases()
first = {}
for c in cases: first.setdefault(c["suite"], c)
def prep(c, variant="main"):
    CUR["size"] = tuple(SIZES[c["_image_file"]])
    qid, q = next(iter(c["questions"].items()))
    return rc.prepare(b"x", q, variant), q

# 1) every gold position of every choice/score suite: a position-invariant 'perfect' model must be read back as that option
for s in ("img_ar_sentiment", "img_pets", "img_count"):
    p, q = prep(first[s])
    n = len(p["groups"]); assert n == len(vb.bench_options(q)), (s, n)
    assert p["groups"] == rc.ro.cand(p["row"]) and p["groups"] == (rc.ro.letters[:n] if n <= 26 else rc.ro.wide[:n])
    bad = 0
    for t in range(n):
        lg0 = torch.full((n,), -6.0); lg0[t] = 6.0               # given order: option t sits at displayed position t
        lg1 = torch.full((n,), -6.0); lg1[n - 1 - t] = 6.0       # reversed order: option t sits at displayed position n-1-t
        pr = rc.decide(p, [lg0, lg1])
        ok = max(range(n), key=pr.__getitem__) == t and abs(sum(pr) - 1) < 1e-6 and pr[t] > 0.49
        bad += (not ok)
    # a model with pure first-letter bias (always 'A') must NOT look informative: report what the bench scorer would see
    la = torch.full((n,), -6.0); la[0] = 6.0
    pr = rc.decide(p, [la, la.clone()])
    top2 = sorted(range(n), key=pr.__getitem__, reverse=True)[:2]
    print(f"{s}: n_options {n} | all {n} gold positions read back correctly: {bad == 0} | pure 'A' bias -> top2 options {top2} with P {[round(pr[i],3) for i in top2]}")
    assert bad == 0
# a model that disagrees between orders: view1 says option 1, view2 says option 2 (as displayed in reversed order)
p, q = prep(first["img_ar_sentiment"])
l0 = torch.tensor([-5., 5., -5.]); l1 = torch.tensor([5., -5., -5.])   # view 2 letter A = option 2 (reversed): says option 2
pr = rc.decide(p, [l0, l1]); print("disagreeing views (opt1 vs opt2) ->", [round(x, 3) for x in pr])
assert abs(pr[1] - pr[2]) < 1e-6 and pr[0] < 0.01

# 2) yes/no: letters A/B (not the words Yes/No); main A=Yes, swapped A=No; probabilities in the bench order [false, true]
for s in ("img_sst2", "img_vqa_yesno"):
    pm, q = prep(first[s]); ps, _ = prep(first[s], "yn_swapped")
    assert pm["groups"] == rc.ro.letters[:2] == ps["groups"], "yes/no must be read from the letters A and B"
    assert [rc.tok.decode([i]).strip() for i in pm["groups"][0]] == ["A"] * 3
    lg = torch.tensor([4.0, -4.0])      # prefers letter A
    pmain, pswap = rc.decide(pm, [lg]), rc.decide(ps, [lg])
    lg2 = torch.tensor([-4.0, 4.0])
    print(f"{s}: prefers letter A -> bench probs [false,true] main {[round(x,3) for x in pmain]} swapped {[round(x,3) for x in pswap]}; "
          f"prefers letter B -> main {[round(x,3) for x in rc.decide(pm,[lg2])]} swapped {[round(x,3) for x in rc.decide(ps,[lg2])]}")
    assert pmain[1] > .99 and pswap[1] < .01
    # the displayed text of the swapped prompt: A. No / B. Yes
    t = ps["texts"][0]; assert "A. No\nB. Yes" in t and "Options: A. No; B. Yes" in t, t[:600]
    t = pm["texts"][0]; assert "A. Yes\nB. No" in t
print("DECIDE CHECKS PASSED")
