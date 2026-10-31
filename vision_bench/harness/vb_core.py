"""Vision-bench core: items -> C1 rows -> multimodal prompts -> candidate-token readout (no generation).

Mirrors how C1 reads a decision (lean/jevbench_od.py to_row + hosting/fastcore/readout.py A5 readout), with the image placed
where the state text goes:
  * row = jevbench_od.to_row(question) with state = the image placeholder:  noul -> Yes/No (lettered A/B in style 'cygnet'),
    choice -> one option per criteria key (+ "- key: description" card), score -> one option per criteria level.
    HEADLINE score options are the criteria strings exactly as Jev receives them ("exactly two" ... "exactly ten"); C1's own
    text-bench form "<i>: <level>" (a zero-based index in front, which disagrees with the real count by 2 on img_count) is only
    run as the labelled diagnostic variant "count_prefixed".
  * prompt text = decoder_io.prompt_texts(Readout, [row], [perm])[0]  (style 'cygnet', layout 'schema_branch_mark', the layout
    the C1 adapter was trained in, read from its train_meta.json); thinking off; the image sits inside the UNTRUSTED markers.
  * readout = fp32 logsumexp over every vocabulary token that decodes to the option letter, at the last real prompt token,
    softmax at T = 1.0. choice: two views (given order + exact reversal), probabilities averaged (A5 '2view'); noul: one read.
The only change from the text readout is that the image features are spliced into the embeddings at the <|image_pad|> slots
(stock Qwen3.5 mechanics: same ViT, same M-RoPE positions) and that the ViT runs once per image, shared by the two views.
"""
from __future__ import annotations

import base64
import io
import json
import math
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))

import torch  # noqa: E402

import decoder_io as dio  # noqa: E402

BASE = "Qwen/Qwen3.5-4B"
REVISION = "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"
ADAPTER = os.path.expanduser("~/lean/models/q35_4b_main500k")
# C1 was trained and merged as the text-only class (Qwen3_5ForCausalLM): its adapter keys read "base_model.model.model.layers.N...".
# The multimodal class this bench loads (Qwen3_5ForConditionalGeneration) names the same modules
# "model.language_model.layers.N...", so peft silently leaves every LoRA_B at zero. The keys are renamed in a COPY of the adapter
# (values untouched); verify_adapter_loaded() then checks every tensor against the file and the Reader refuses to run otherwise.
ADAPTER_RENAMED = os.environ.get("VB_ADAPTER_RENAMED", os.path.expanduser("~/vision_bench/adapter_c1_renamed"))
KEY_OLD = "base_model.model.model.layers."
KEY_NEW = "base_model.model.model.language_model.layers."
ADAPTER_N_TENSORS, ADAPTER_N_LORA_B = 496, 248   # the real C1 adapter: 248 A + 248 B (language-model layers only)
VARIANTS = ("main", "count_prefixed", "yn_swapped")  # main = headline; the other two are labelled diagnostics# The VM's cached snapshot of the base has no preprocessor_config.json; the official one (same pinned revision) is shipped here.
PROC_DIR = os.environ.get("VB_PROC_DIR", os.path.expanduser("~/vision_bench/qwen35_processor"))
SUITES = ["img_sst2", "img_ar_sentiment", "img_pets", "img_vqa_yesno", "img_count"]
IMG_PLACEHOLDER = "<|vision_start|><|image_pad|><|vision_end|>"
PAD_MULTIPLE = int(os.environ.get("OD_PAD_MULTIPLE", "256"))  # decoder_io's bucketing of padded lengths (Triton autotune)
TEMPS = {"noul": 1.0, "choice": 1.0}  # C1 ships T = 1.0 (fastcore/readout.py)


# ---------------------------------------------------------------- data
def data_root():
    return os.environ.get("VB_DATA", os.path.join(os.path.dirname(HERE), "data"))


def load_cases(suites=None, root=None):
    root = root or data_root()
    out = []
    for s in suites or SUITES:
        for line in open(f"{root}/{s}/cases.jsonl", encoding="utf-8"):
            c = json.loads(line)
            c["_image_file"] = f"{root}/{s}/images/{os.path.basename(c['state'][0]['image'])}"
            out.append(c)
    return out


def gold_index(q, g):
    """Gold option index in the bench's own option order (score.py: options(), gold_idx())."""
    if q["type"] == "choice":
        return list(q["criteria"].keys()).index(g["label"])
    return int(g["label"])


def bench_options(q):
    if q["type"] == "noul":
        return ["false", "true"]
    if q["type"] == "score":
        return [str(i) for i in range(len(q["criteria"]))]
    return list(q["criteria"].keys())


def to_row(q, state=IMG_PLACEHOLDER, score_prefix=False):
    """lean/jevbench_od.py to_row, unchanged except that the state is the image placeholder and (headline) score options carry
    no index prefix: the model sees the criteria strings exactly as Jev does. score_prefix=True restores C1's "<i>: <level>"."""
    qt, crit, instr = q["type"], q.get("criteria"), q["instructions"]
    row = {"state": state, "instructions": instr, "qtype": "choice", "options": None}
    if qt == "noul":
        row["qtype"] = "noul"
        if isinstance(crit, dict) and (crit.get("true") or crit.get("false")):
            row["card"] = f"- Yes: {crit.get('true') or 'the statement holds'}\n- No: {crit.get('false') or 'it does not hold'}"
        return row, None
    if qt == "choice":
        keys = list(crit.keys())
        row["options"] = keys
        notes = [f"- {k}: {v}" for k, v in crit.items() if v and str(v).strip() and str(v).strip() != k]
        if notes:
            row["card"] = "\n".join(notes)
        return row, keys
    keys = [str(i) for i in range(len(crit))]
    row["options"] = [f"{i}: {lvl}" for i, lvl in enumerate(crit)] if score_prefix else [str(lvl) for lvl in crit]
    assert len(set(row["options"])) == len(row["options"]), "score options must be distinct"
    return row, keys


def views_for(row, variant="main"):
    """fastcore/readout.py views_for (A5 2view): choice -> given order + exact reversal; noul -> the single read.
    Diagnostic yn_swapped: the single Yes/No read with the letters swapped (No = A, Yes = B)."""
    if variant == "yn_swapped":
        assert row["qtype"] == "noul", "yn_swapped applies to yes/no items only"
        return [[1, 0]]
    if row["qtype"] == "choice":
        return [None, list(range(len(row["options"])))[::-1]]
    return [None]


# ---------------------------------------------------------------- adapter (the C1 LoRA must really be applied)
def build_renamed_adapter(src, dst):
    """Write a copy of the adapter under dst whose keys land in the multimodal class. Values are untouched.
    Returns (original state dict, renamed state dict). Refuses an adapter with any key outside the text-only layout."""
    from safetensors.torch import load_file, save_file
    sd = load_file(os.path.join(src, "adapter_model.safetensors"))
    bad = [k for k in sd if not k.startswith(KEY_OLD)]
    assert not bad, f"adapter keys not in the expected text-only layout: {bad[:3]}"
    sd2 = {KEY_NEW + k[len(KEY_OLD):]: v.contiguous() for k, v in sd.items()}
    assert len(sd2) == len(sd)
    os.makedirs(dst, exist_ok=True)
    save_file(sd2, os.path.join(dst, "adapter_model.safetensors"), metadata={"format": "pt"})
    shutil.copy(os.path.join(src, "adapter_config.json"), os.path.join(dst, "adapter_config.json"))
    return sd, sd2


def verify_adapter_loaded(pm, sd_new, expect_tensors=None, expect_b=None):
    """Every tensor of the (renamed) adapter file must sit, bit for bit, in the injected LoRA parameter it belongs to; no injected
    LoRA parameter may be left without a file tensor; every lora_B must be non-zero. Raises AssertionError otherwise."""
    params = dict(pm.named_parameters())
    lora = [n for n in params if "lora_" in n]
    n_b = n_b_nonzero = n_nohome = n_unequal = 0
    seen = set()
    for k, t in sd_new.items():
        pk = k.replace(".lora_A.weight", ".lora_A.default.weight").replace(".lora_B.weight", ".lora_B.default.weight")
        p = params.get(pk)
        is_b = ".lora_B." in k
        n_b += is_b
        if p is None:
            n_nohome += 1
            continue
        seen.add(pk)
        if not torch.equal(p.detach().cpu().float(), t.to(p.dtype).float()):
            n_unequal += 1
        if is_b and float(p.detach().abs().sum()) > 0:
            n_b_nonzero += 1
    chk = {"n_tensors": len(sd_new), "n_lora_B": n_b, "n_lora_B_nonzero": n_b_nonzero, "n_no_home": n_nohome,
           "n_unequal_to_file": n_unequal, "n_model_lora_params": len(lora), "n_model_lora_params_not_in_file": len(set(lora) - seen)}
    assert chk["n_no_home"] == 0 and chk["n_unequal_to_file"] == 0 and chk["n_model_lora_params_not_in_file"] == 0, chk
    assert chk["n_lora_B"] > 0 and chk["n_lora_B_nonzero"] == chk["n_lora_B"], chk
    if expect_tensors is not None:
        assert chk["n_tensors"] == expect_tensors, chk
    if expect_b is not None:
        assert chk["n_lora_B"] == expect_b and chk["n_lora_B_nonzero"] == expect_b, chk
    return chk


def attach_c1_adapter(model, src, dst, expect_tensors=None, expect_b=None):
    """Load the C1 LoRA into the multimodal model through the renamed copy and prove it landed. Returns (PeftModel, check dict)."""
    from peft import PeftModel
    _, sd_new = build_renamed_adapter(src, dst)
    pm = PeftModel.from_pretrained(model, dst)
    return pm, verify_adapter_loaded(pm, sd_new, expect_tensors, expect_b)


# ---------------------------------------------------------------- model
class Reader:
    def __init__(self, which, dev="cuda", load_model=True):
        """which: 'c1' (base + LoRA adapter via peft) or 'base' (plain Qwen3.5-4B). load_model=False: CPU-only prompt checks."""
        from transformers import AutoImageProcessor, AutoModelForImageTextToText, AutoTokenizer
        self.which, self.dev = which, dev
        adapter = ADAPTER if which == "c1" else None
        info = dio.resolve_prompt([adapter] if adapter else [], BASE, "schema_branch_mark", "cygnet", REVISION, force=False) \
            if adapter else {"layout": "schema_branch_mark", "style": "cygnet", "base": BASE, "revision": REVISION}
        dio.LAYOUT, dio.STYLE = info["layout"], info["style"]  # C1: from the adapter's saved training cfg; base: the same
        self.layout, self.style = dio.LAYOUT, dio.STYLE
        self.tok = dio.load_tokenizer(BASE, adapter=adapter, revision=REVISION)
        self.imgproc = AutoImageProcessor.from_pretrained(PROC_DIR)
        self.image_token_id = self.tok.convert_tokens_to_ids("<|image_pad|>")
        self.ro = dio.Readout(self.tok)
        self.pad_id = self.tok.pad_token_id
        self.merge = getattr(self.imgproc, "merge_size", 2)
        if not load_model:
            return
        t0 = time.time()
        model = AutoModelForImageTextToText.from_pretrained(BASE, dtype=torch.bfloat16, attn_implementation="sdpa",
                                                            revision=REVISION).to(dev)
        self.adapter_check = None
        if adapter:
            model, self.adapter_check = attach_c1_adapter(model, adapter, ADAPTER_RENAMED, ADAPTER_N_TENSORS, ADAPTER_N_LORA_B)
            model = model.to(dev)
        model.eval()
        self.model = model
        self.top = model.get_base_model() if hasattr(model, "get_base_model") else model
        self.inner, self.head = self.top.model, self.top.lm_head
        self.cfg = self.top.config
        assert self.image_token_id == self.cfg.image_token_id
        self.load_s = time.time() - t0

    # ---- CPU side
    def prepare(self, image_bytes, q, variant="main"):
        """Decode + preprocess the image, build the C1 prompt(s) for every view, tokenize. Returns a dict (CPU tensors).
        variant: 'main' (headline), 'count_prefixed' (score options with C1's "<i>: " prefix), 'yn_swapped' (Yes/No letters swapped)."""
        assert variant in VARIANTS, variant
        from PIL import Image
        im = Image.open(io.BytesIO(image_bytes))
        im.load()
        im = im.convert("RGB")
        px = self.imgproc(images=[im], return_tensors="pt")
        pv, grid = px["pixel_values"], px["image_grid_thw"]
        n_img = int(grid.prod(-1).item() // (self.merge ** 2))
        row, keys = to_row(q, score_prefix=(variant == "count_prefixed"))
        views = views_for(row, variant)
        groups = self.ro.cand(row)
        seqs, texts = [], []
        for perm in views:
            text = dio.prompt_texts(self.ro, [row], [perm])[0]
            assert text.count("<|image_pad|>") == 1, "the image placeholder must appear once in the prompt"
            text = text.replace("<|image_pad|>", "<|image_pad|>" * n_img)
            ids = self.tok(text, add_special_tokens=False)["input_ids"]
            seqs.append(ids)
            texts.append(text)
        return {"row": row, "keys": keys, "views": views, "groups": groups, "seqs": seqs, "pv": pv, "grid": grid,
                "n_img": n_img, "size": im.size, "texts": texts, "variant": variant}

    # ---- GPU side
    @torch.no_grad()
    def read(self, preps):
        """Candidate logits for every view of every prepared item. One padded forward over all their sequences.
        Returns [[tensor(len(groups)) per view] per item]."""
        dev = self.dev
        flat_seqs, owner = [], []
        for i, p in enumerate(preps):
            for ids in p["seqs"]:
                flat_seqs.append(ids)
                owner.append(i)
        B = len(flat_seqs)
        L = -(-max(len(s) for s in flat_seqs) // PAD_MULTIPLE) * PAD_MULTIPLE
        ids = torch.full((B, L), self.pad_id, dtype=torch.long)
        mask = torch.zeros((B, L), dtype=torch.long)
        for b, s in enumerate(flat_seqs):
            ids[b, :len(s)] = torch.tensor(s, dtype=torch.long)
            mask[b, :len(s)] = 1
        mm = (ids == self.image_token_id).int()
        grid_per_seq = torch.cat([preps[o]["grid"] for o in owner], 0)  # one image per sequence, in sequence order
        pos, _ = self.inner.get_rope_index(ids, mm_token_type_ids=mm, image_grid_thw=grid_per_seq, attention_mask=mask)
        ids_d, mask_d, pos_d = ids.to(dev), mask.to(dev), pos.to(dev)
        pv = torch.cat([p["pv"] for p in preps], 0).to(dev)
        grid = torch.cat([p["grid"] for p in preps], 0).to(dev)
        feats = self.inner.get_image_features(pv, grid).pooler_output  # one ViT pass per image, shared by its views
        emb = self.inner.get_input_embeddings()(ids_d)
        for b, o in enumerate(owner):
            emb[b, ids_d[b] == self.image_token_id] = feats[o].to(emb.dtype)
        hs = self.inner(inputs_embeds=emb, position_ids=pos_d, attention_mask=mask_d).last_hidden_state
        last = mask_d.sum(1) - 1
        h = hs[torch.arange(B, device=dev), last]
        out = [[] for _ in preps]
        for b, o in enumerate(owner):
            groups = preps[o]["groups"]
            flat = [t for g in groups for t in g]
            lg = h[b].float() @ self.head.weight[flat].float().T
            parts, k = [], 0
            for g in groups:
                parts.append(torch.logsumexp(lg[k:k + len(g)], 0))
                k += len(g)
            out[o].append(torch.stack(parts))
        return out

    @torch.no_grad()
    def adapter_effect(self, prep):
        """Max |candidate logit with the LoRA on - with the LoRA off| over the views of one prepared item. Must be > 0 for C1."""
        on = self.read([prep])[0]
        with self.model.disable_adapter():
            off = self.read([prep])[0]
        return max(float((a - b).abs().max()) for a, b in zip(on, off))

    @torch.no_grad()
    def read_stock(self, prep):
        """Reference path for tests only: the unmodified Qwen3.5 multimodal forward (ViT run again for each view)."""
        dev = self.dev
        outs = []
        for ids in prep["seqs"]:
            t = torch.tensor([ids], dtype=torch.long, device=dev)
            mm = (t == self.image_token_id).int()
            hs = self.inner(input_ids=t, attention_mask=torch.ones_like(t), pixel_values=prep["pv"].to(dev),
                            image_grid_thw=prep["grid"].to(dev), mm_token_type_ids=mm).last_hidden_state
            h = hs[0, -1]
            groups = prep["groups"]
            flat = [t for g in groups for t in g]
            lg = h.float() @ self.head.weight[flat].float().T
            parts, k = [], 0
            for g in groups:
                parts.append(torch.logsumexp(lg[k:k + len(g)], 0))
                k += len(g)
            outs.append(torch.stack(parts))
        return outs

    def decide(self, prep, view_logits):
        """Logits of each view -> (probability vector in the bench's option order, extra info). C1's combine()."""
        row, keys = prep["row"], prep["keys"]
        T = TEMPS["noul" if row["qtype"] == "noul" else "choice"]
        probs = [dio.to_probs(row, lg, perm, temp=T) for lg, perm in zip(view_logits, prep["views"])]
        if row["qtype"] == "noul":
            p_yes = probs[0]["yes"]
            return [1.0 - p_yes, p_yes]
        if len(probs) == 2:
            p = {o: (probs[0][o] + probs[1][o]) / 2 for o in row["options"]}
        else:
            p = {o: probs[0][o] for o in row["options"]}
        return [p[o] for o in row["options"]]


def sync(dev="cuda"):
    if dev == "cuda":
        torch.cuda.synchronize()


def decision_record(q, gold, probs):
    """The typed answer the HTTP server returns for one question (Decisions-API-like)."""
    if q["type"] == "noul":
        return {"type": "noul", "noul": probs[1], "probabilities": {"false": probs[0], "true": probs[1]}}
    opts = bench_options(q)
    top = max(range(len(probs)), key=probs.__getitem__)
    key = "choice" if q["type"] == "choice" else "score"
    ans = {"type": q["type"], key: opts[top] if q["type"] == "choice" else int(opts[top]),
           "confidence": probs[top], "probabilities": dict(zip(opts, probs))}
    return ans
