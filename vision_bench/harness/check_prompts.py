"""CPU-only prompt checks (no GPU): C1's text prompt + image slot vs the official Qwen3.5 processor route.
Run on the VM:  CUDA_VISIBLE_DEVICES= PYTHONPATH=~/vision_bench/pylib python -I? no (needs env) -> python check_prompts.py
"""
import hashlib
import json
import os
import sys

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vb_core as vb  # noqa: E402
from vb_core import dio  # noqa: E402

out = {}
cases = vb.load_cases()
by_suite = {}
for c in cases:
    by_suite.setdefault(c["suite"], c)
for which in ("c1", "base"):
    r = vb.Reader(which, load_model=False)
    out[which] = {"layout": dio.LAYOUT, "style": dio.STYLE, "chat_template_sha": hashlib.sha256((r.tok.chat_template or "").encode()).hexdigest()[:16],
                  "image_token_id": r.image_token_id, "merge": r.merge, "imgproc": type(r.imgproc).__name__}
    proc = None
    try:
        from transformers import Qwen3VLProcessor, Qwen3VLVideoProcessor
        vp = Qwen3VLVideoProcessor.from_pretrained(vb.PROC_DIR)
        proc = Qwen3VLProcessor(image_processor=r.imgproc, tokenizer=r.tok, video_processor=vp, chat_template=r.tok.chat_template)
    except Exception as e:  # noqa: BLE001
        out[which]["processor_error"] = f"{type(e).__name__}: {str(e)[:300]}"
    res = []
    for suite, c in by_suite.items():
        qid, q = next(iter(c["questions"].items()))
        prep = r.prepare(open(c["_image_file"], "rb").read(), q)
        row = prep["row"]
        item = {"suite": suite, "qtype": row["qtype"], "n_options": len(row["options"] or []), "views": len(prep["views"]),
                "n_tokens": [len(s) for s in prep["seqs"]], "n_image_tokens": prep["n_img"], "grid": prep["grid"].tolist(),
                "image_size": prep["size"], "pixel_values": list(prep["pv"].shape),
                "n_candidate_groups": len(prep["groups"]), "group_sizes": [len(g) for g in prep["groups"]][:6]}
        if proc is not None:
            # official route: the same C1 text split at the image slot, passed as multimodal chat content
            user = dio.user_msg(prep["row"], prep["views"][0])
            before, after = user.split(vb.IMG_PLACEHOLDER)
            msgs = [{"role": "system", "content": dio.CYGNET_SYSTEM},
                    {"role": "user", "content": [{"type": "text", "text": before}, {"type": "image"}, {"type": "text", "text": after}]}]
            from PIL import Image
            im = Image.open(c["_image_file"]).convert("RGB")
            tmpl = proc.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False)
            enc = proc(text=[tmpl], images=[im], return_tensors="pt")
            same_ids = enc["input_ids"][0].tolist() == prep["seqs"][0]
            same_pix = bool((enc["pixel_values"] == prep["pv"]).all()) and enc["image_grid_thw"].tolist() == prep["grid"].tolist()
            item["official_ids_equal"] = same_ids
            item["official_pixels_equal"] = same_pix
            item["official_template_equals_mine"] = tmpl.replace(vb.IMG_PLACEHOLDER, "<IMG>") == \
                dio.prompt_texts(r.ro, [prep["row"]], [prep["views"][0]])[0].replace(vb.IMG_PLACEHOLDER, "<IMG>")
        res.append(item)
        if suite in ("img_vqa_yesno", "img_count") and which == "c1":
            t = dio.prompt_texts(r.ro, [prep["row"]], [prep["views"][-1]])[0]
            out["example_" + suite] = t if len(t) < 3000 else t[:1500] + "\n...\n" + t[-1200:]
    out[which]["items"] = res
# adapter tokenizer vs base tokenizer on the same prompt
c = by_suite["img_pets"]
qid, q = next(iter(c["questions"].items()))
rc, rb = vb.Reader("c1", load_model=False), vb.Reader("base", load_model=False)
pc = rc.prepare(open(c["_image_file"], "rb").read(), q)
pb = rb.prepare(open(c["_image_file"], "rb").read(), q)
out["c1_vs_base_tokens_equal"] = pc["seqs"] == pb["seqs"]
print(json.dumps(out, indent=1, default=str))
