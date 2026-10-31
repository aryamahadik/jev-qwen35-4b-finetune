"""Build the harness' real prompts on the Mac (no model weights): tokenizer of the pinned base + the adapter's own tokenizer,
candidate-token groups, option order/labels, gold-leak scan. Nothing is written outside review/."""
import os, sys, json, re, hashlib
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/vision_bench/harness")
os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", VB_PROC_DIR="/Users/aryamahadik/Documents/jev/vision_bench/src/qwen35-4b-processor")
import types, torch, transformers
SIZES = json.load(open("/Users/aryamahadik/Documents/jev/vision_bench/review/tmp/sizes.json"))
CUR = {"size": None}
def smart_resize(h, w, factor=32, mn=65536, mx=16777216):
    hb, wb = round(h / factor) * factor, round(w / factor) * factor
    if hb * wb > mx:
        b = (h * w / mx) ** 0.5; hb = max(factor, int(h / b // factor) * factor); wb = max(factor, int(w / b // factor) * factor)
    elif hb * wb < mn:
        b = (mn / (h * w)) ** 0.5; hb = int(-(-h * b // factor) * factor); wb = int(-(-w * b // factor) * factor)
    return hb, wb
class FakeIm:
    def __init__(self): self.size = CUR["size"]
    def load(self): pass
    def convert(self, m): return self
class StubProc:
    merge_size = 2
    def __call__(self, images, return_tensors):
        w, h = images[0].size; hb, wb = smart_resize(h, w); gh, gw = hb // 16, wb // 16
        return {"pixel_values": torch.zeros(gh * gw, 1536), "image_grid_thw": torch.tensor([[1, gh, gw]])}
class StubAIP:
    @staticmethod
    def from_pretrained(path): return StubProc()
transformers.AutoImageProcessor = StubAIP
fake_pil = types.ModuleType("PIL"); fake_img = types.ModuleType("PIL.Image"); fake_img.open = lambda b: FakeIm(); fake_pil.Image = fake_img
sys.modules["PIL"] = fake_pil; sys.modules["PIL.Image"] = fake_img
import vb_core as vb
vb.ADAPTER = "/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k"
from vb_core import dio
rd = vb.Reader("c1", load_model=False)
print("layout/style:", rd.layout, rd.style, "| image_token_id", rd.image_token_id, "| tokenizer len", len(rd.tok))
cases = vb.load_cases()
first = {}
for c in cases: first.setdefault(c["suite"], c)
tok = rd.tok
for s, c in first.items():
    qid, q = next(iter(c["questions"].items()))
    CUR["size"] = tuple(SIZES[c["_image_file"]]); prep = rd.prepare(open(c["_image_file"], "rb").read(), q)
    g = prep["groups"]
    print(f"\n=== {s} ({q['type']}) views={len(prep['views'])} n_groups={len(g)} img_tokens={prep['n_img']} seq_len={[len(x) for x in prep['seqs']]} size={prep['size']}")
    print("candidate groups (first 3):", [(grp, [tok.decode([t]) for t in grp]) for grp in g[:3]])
    if s in ("img_vqa_yesno", "img_pets", "img_count", "img_sst2"):
        t = prep["texts"][-1]
        t = re.sub(r"(<\|image_pad\|>)+", "<|image_pad|>x%d" % prep["n_img"], t)
        print(t if len(t) < 2600 else t[:1300] + "\n...[cut]...\n" + t[-900:])
# pets: labels past Z and their groups
c = first["img_pets"]; qid, q = next(iter(c["questions"].items()))
CUR["size"] = tuple(SIZES[c["_image_file"]]); prep = rd.prepare(open(c["_image_file"], "rb").read(), q)
print("\npets labels 24..36:", [dio.label(i) for i in range(24, 37)], "| group sizes:", [len(x) for x in prep["groups"][24:]])
print("pets groups disjoint:", len({t for gg in prep["groups"] for t in gg}) == sum(len(gg) for gg in prep["groups"]))
# yes/no: which letter is Yes; token of A and B
c = first["img_vqa_yesno"]; qid, q = next(iter(c["questions"].items()))
CUR["size"] = tuple(SIZES[c["_image_file"]]); prep = rd.prepare(open(c["_image_file"], "rb").read(), q)
print("\nyes/no cand groups decode to:", [[tok.decode([t]) for t in grp] for grp in prep["groups"]], "| p_yes from letter:", "A (first group)")
# leak scan: gold label strings / ids / file names in any prompt text? (cheap: scan prompts of all suites for the gold label text of THAT item when it is not an option)
leaks = 0
for c in cases:
    qid, q = next(iter(c["questions"].items()))
    g = c["gold"][qid]
    if q["type"] == "choice" or q["type"] == "score":
        continue
    # yes/no: the prompt must not contain the numeric gold; question text is shared with Jev anyway
    pass
txt = {c["id"]: json.dumps(c["questions"], ensure_ascii=False) for c in cases}
print("\nprompt inputs per item come only from questions (type/instructions/criteria) + image; keys of what to_row reads:", sorted(vb.to_row.__code__.co_names))
# does any question text for img_count / vqa contain a number word equal to the gold?
words = ["two","three","four","five","six","seven","eight","nine","ten"]
n = 0
for c in cases:
    if c["suite"] != "img_count": continue
    qid, q = next(iter(c["questions"].items())); gold = c["gold"][qid]["label"]
    if re.search(rf"\b{words[gold]}\b|\b{gold+2}\b", q["instructions"].lower()): n += 1
print("img_count items whose question text contains the gold number:", n, "of 200")
