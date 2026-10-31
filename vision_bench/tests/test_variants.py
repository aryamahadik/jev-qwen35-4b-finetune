"""Prompt-level checks of the three variants with the REAL tokenizer (adapter's own) and a stub image processor (CPU, no weights):
  main            img_count options are the criteria strings Jev gets ('exactly two' ... 'exactly ten'), no index prefix
  count_prefixed  C1's text-bench form 'i: exactly N' (diagnostic only)
  yn_swapped      Yes/No letters swapped (A = No, B = Yes); P(yes) is read from the letter that now means Yes."""
import json, os, re, sys, types
HERE = os.path.dirname(os.path.abspath(__file__)); VB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(VB, "harness"))
os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", VB_PROC_DIR=f"{VB}/src/qwen35-4b-processor")
import torch, transformers
SIZES = json.load(open(f"{VB}/review/tmp/sizes.json"))
CUR = {"size": None}
class FakeIm:
    def __init__(self): self.size = CUR["size"]
    def load(self): pass
    def convert(self, m): return self
class StubProc:
    merge_size = 2
    def __call__(self, images, return_tensors):
        return {"pixel_values": torch.zeros(24, 1536), "image_grid_thw": torch.tensor([[1, 4, 6]])}
class StubAIP:
    @staticmethod
    def from_pretrained(path): return StubProc()
transformers.AutoImageProcessor = StubAIP
fake_pil = types.ModuleType("PIL"); fake_img = types.ModuleType("PIL.Image"); fake_img.open = lambda b: FakeIm(); fake_pil.Image = fake_img
sys.modules["PIL"] = fake_pil; sys.modules["PIL.Image"] = fake_img
import vb_core as vb
vb.ADAPTER = "/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k"   # tokenizer + train_meta only
rd = vb.Reader("c1", load_model=False)
cases = vb.load_cases()
first = {}
for c in cases: first.setdefault(c["suite"], c)
def prep(suite, variant):
    c = first[suite]; qid, q = next(iter(c["questions"].items()))
    CUR["size"] = tuple(SIZES[c["_image_file"]]); return rd.prepare(b"x", q, variant), q
def opts_block(text):
    m = re.search(r"Options:\n((?:[A-Z]{1,2}\. .*\n?)+)", text); return m.group(1).strip().splitlines()

# ---- img_count
p, q = prep("img_count", "main")
levels = list(q["criteria"]); print("criteria:", levels)
v0, v1 = opts_block(p["texts"][0]), opts_block(p["texts"][1])
print("main view 1:", v0); print("main view 2 (reversed):", v1)
assert v0 == [f"{vb.dio.label(i)}. {l}" for i, l in enumerate(levels)]
assert v1 == [f"{vb.dio.label(i)}. {l}" for i, l in enumerate(levels[::-1])]
assert not any(re.search(r"\d: ", t) for t in p["texts"]), "no index prefix in the headline"
assert len(p["groups"]) == 9 and p["keys"] == [str(i) for i in range(9)]
pp, _ = prep("img_count", "count_prefixed")
print("prefixed view 1:", opts_block(pp["texts"][0])[:3])
assert opts_block(pp["texts"][0])[0] == "A. 0: exactly two" and opts_block(pp["texts"][1])[0] == "A. 8: exactly ten"
# reversed view -> probabilities back in the bench's order, averaged: a peaked logit on the letter of 'exactly five' in each view
tgt = 3   # 'exactly five' is level index 3 (gold index = number - 2)
lg0 = torch.full((9,), -5.0); lg0[tgt] = 5.0            # view 1: option index == letter index
lg1 = torch.full((9,), -5.0); lg1[8 - tgt] = 5.0        # view 2 (reversed): letter 8-tgt shows level tgt
pr = rd.decide(p, [lg0, lg1]); assert max(range(9), key=pr.__getitem__) == tgt and abs(sum(pr) - 1) < 1e-6, pr
print("count combine OK, p(five) =", round(pr[tgt], 4))

# ---- yes/no
pm_, qy = prep("img_sst2", "main"); ps_, _ = prep("img_sst2", "yn_swapped")
bm, bs = opts_block(pm_["texts"][0]), opts_block(ps_["texts"][0])
print("yes/no main:", bm, "| swapped:", bs)
assert bm == ["A. Yes", "B. No"] or bm[0].startswith("A. Yes"), bm
assert bs[0].startswith("A. No") and bs[1].startswith("B. Yes"), bs
assert len(pm_["seqs"]) == 1 and len(ps_["seqs"]) == 1 and ps_["views"] == [[1, 0]]
assert pm_["groups"] == ps_["groups"]    # letters A/B in both
lgA = torch.tensor([5.0, 0.0])             # the model prefers letter A
yes_main = rd.decide(pm_, [lgA])[1]; yes_swap = rd.decide(ps_, [lgA])[1]
print(f"letter A preferred: P(yes) main {yes_main:.4f} | swapped {yes_swap:.4f}")
assert yes_main > 0.99 and yes_swap < 0.01
# image placeholder appears once and the token counts of the two orders match
assert all(t.count("<|image_pad|>") == pm_["n_img"] for t in pm_["texts"] + ps_["texts"])
assert len(pm_["seqs"][0]) == len(ps_["seqs"][0])
# the variants cannot be used on the wrong item type
try:
    prep("img_pets", "yn_swapped"); print("FAIL: yn_swapped accepted on a choice item"); sys.exit(1)
except AssertionError:
    print("yn_swapped refused on a choice item: OK")
print("VARIANT TESTS PASSED")
