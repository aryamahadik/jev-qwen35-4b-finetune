"""Reviewer round 2 (CPU only, Mac): inspect the real prompts / candidate tokens / option order handling of vb_core.
Run: opendecide-data/.venv/bin/python -I -B harness/rv2_prompts.py   (no weights, no GPU, no network)
Uses the adapter's own tokenizer (Mac backup copy of the C1 adapter) and the base tokenizer files fetched from the pinned revision."""
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
LAY_C1 = (rc.layout, rc.style)
# base reader with the pinned base tokenizer files (the VM loads it from the HF cache at the same revision)
from transformers import AutoTokenizer
orig = vb.dio.load_tokenizer
vb.dio.load_tokenizer = lambda p, adapter=None, revision=None: orig(SCR, adapter=None, revision=None)
rb = vb.Reader("base", load_model=False)
vb.dio.load_tokenizer = orig
print("c1 layout/style", LAY_C1, "| base layout/style", (rb.layout, rb.style))
print("C1 vs base tokenizer: vocab size", len(rc.tok), len(rb.tok), "| image_pad id", rc.image_token_id, rb.image_token_id)

# candidate token groups
def show(rd, name):
    g = rd.ro.letters
    print(f"[{name}] letter groups (first 3): ", [(c, [(i, rd.tok.decode([i])) for i in g[k]]) for k, c in enumerate("ABC")])
    w = rd.ro.wide[26:]
    print(f"[{name}] wide labels (first 12 beyond Z):", vb.dio.WIDE[26:38], "| group sizes", [len(x) for x in w[:12]])
show(rc, "c1"); show(rb, "base")
assert rc.ro.letters == rb.ro.letters and rc.ro.wide == rb.ro.wide, "candidate groups differ between the two tokenizers"
all_ids = [i for g in rc.ro.wide[:37] for i in g]
assert len(all_ids) == len(set(all_ids)), "a token id appears in two label groups (labels would overlap)"
print("label groups for 37 options are disjoint; n token ids:", len(all_ids))

cases = vb.load_cases()
first = {}
for c in cases: first.setdefault(c["suite"], c)
def prep_text(rd, c, variant="main"):
    CUR["size"] = tuple(SIZES[c["_image_file"]])
    qid, q = next(iter(c["questions"].items()))
    return rd.prepare(b"x", q, variant)
for s, c in first.items():
    p = prep_text(rc, c)
    t = p["texts"][0]
    short = re.sub(r"(<\|image_pad\|>)+", f"<|image_pad|>x{p['n_img']}", t)
    print("=" * 100); print(s, "| views", p["views"] if len(p["views"]) < 3 else "[None, reversed]", "| n tokens", [len(x) for x in p["seqs"]], "| image tokens", p["n_img"])
    print(short if s != "img_pets" else short[:1100] + "\n   ...\n" + short[-900:])
    tail = [rc.tok.decode([i]) for i in p["seqs"][0][-10:]]
    print("LAST 10 TOKENS:", tail)
    print("candidate groups:", [[rc.tok.decode([i]) for i in g] for g in p["groups"]][:4], "n groups", len(p["groups"]))

# 1) all 1000 items: prompt text identical across items except where the dataset question differs; c1 ids == base ids
dist = collections.defaultdict(set); mism = 0; maxlen = 0
for c in cases:
    p1 = prep_text(rc, c); p2 = prep_text(rb, c)
    if p1["seqs"] != p2["seqs"]: mism += 1
    maxlen = max(maxlen, max(len(x) for x in p1["seqs"]))
    for t in p1["texts"]:
        dist[c["suite"]].add(re.sub(r"(<\|image_pad\|>)+", "<IMG>", t))
print("items whose token ids differ between the C1 tokenizer and the base tokenizer:", mism, "of", len(cases), "| max prompt tokens", maxlen)
for s in vb.SUITES:
    print(s, "distinct prompt texts (all views, image run collapsed):", len(dist[s]))

# 2) gold leakage: is the gold label string present in the prompt text of an item? (only the question part may differ)
leak = collections.Counter()
for c in cases:
    qid, q = next(iter(c["questions"].items()))
    g = c["gold"][qid]["label"]
    t = prep_text(rc, c)["texts"][0]
    qt = q["type"]
    if qt == "choice":
        # every option is listed in every prompt, so test whether the gold option is marked differently from its siblings:
        # compare the option block with the one of the first item in the suite
        base_t = prep_text(rc, first[c["suite"]])["texts"][0]
        a = re.sub(r"(<\|image_pad\|>)+", "<IMG>", t); b = re.sub(r"(<\|image_pad\|>)+", "<IMG>", base_t)
        leak["choice_prompt_differs_from_suite_first_item"] += int(a != b)
    elif qt == "noul":
        leak["noul_instr_has_yes_no_answer_word"] += int(bool(re.search(r"\b(the answer is (yes|no))\b", q["instructions"], re.I)))
    else:
        leak["count_instr_has_digit_or_numword"] += int(bool(re.search(r"\b(\d+|two|three|four|five|six|seven|eight|nine|ten)\b", q["instructions"], re.I)))
print("leak probes (all should be 0):", dict(leak))
