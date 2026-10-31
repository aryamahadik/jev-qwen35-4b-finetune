"""oc1.vision: C1 + the Qwen3.5 vision tower, image-token caps, on 200 vision-bench items (100 Pets + 100 VQA yes/no).

The merged checkpoint keeps the base's vision tower byte for byte (export base layout: vision/MTP tensors == base bitwise),
so SGLang serves C1 with images as it serves the text decisions. Prompts are C1's own (vision_bench/harness/vb_core.py
to_row / views_for, copied unchanged below): the image sits where the state text goes, inside the untrusted markers; yes/no
= one read (Yes = A), choice = two views (given order + exact reversal) averaged.

  build_pack(...)        LAPTOP: items + prompt texts + candidate ids + the image files -> data/vision_pack/ (CPU)
  run_vision(...)        CONTAINER (image python: PIL + httpx, no torch): for each token-cap arm, every item through
                         POST /generate (text + image_data, prefill only, candidate-token logprobs), accuracy and latency
  smart_resize / cap_dims   the Qwen3-VL image-processor arithmetic (patch 16, merge 2 -> 32 px per token side): a cap is
                         applied CLIENT-SIDE by resizing to exactly the size the processor would pick for max_pixels = cap x 32 x 32,
                         so one server boot serves every cap; the server's prompt_tokens must then equal the predicted count.
Caps (visual tokens): native (uncapped), 256, 128, 64 ... plus latency-only UPSCALE arms (1024 / 2048 / 4096 tokens) that
show how latency grows with image tokens. The native size of these benchmark images is ~190-300 tokens, so caps >= 512 are
no-ops on them; the report says so.
"""
from __future__ import annotations

import base64
import io
import json
import math
import random
import time
from pathlib import Path

from . import common as C

FACTOR = 32                    # patch_size 16 x merge_size 2 (preprocessor_config.json of Qwen3.5-4B)
MIN_PIXELS, MAX_PIXELS = 65536, 16777216
IMG_PLACEHOLDER = "<|vision_start|><|image_pad|><|vision_end|>"
SUITES = ("img_pets", "img_vqa_yesno")
VB_DATA = C.JEV_ROOT / "vision_bench" / "data"
PACK_DIR = C.ROOT / "data" / "vision_pack"
SAMPLING = {"max_new_tokens": 0, "temperature": 1.0, "top_p": 1.0, "top_k": -1, "min_p": 0.0, "repetition_penalty": 1.0,
            "frequency_penalty": 0.0, "presence_penalty": 0.0}


# ---------------------------------------------------------------- vb_core copies (unchanged logic)
def bench_options(q):
    if q["type"] == "noul":
        return ["false", "true"]
    if q["type"] == "score":
        return [str(i) for i in range(len(q["criteria"]))]
    return list(q["criteria"].keys())


def gold_index(q, g):
    if q["type"] == "choice":
        return list(q["criteria"].keys()).index(g["label"])
    return int(g["label"])


def to_row(q, state=IMG_PLACEHOLDER):
    """vb_core.to_row (headline variant: no index prefix on score options; pets/vqa use choice and noul only)."""
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
    raise ValueError(f"vision pack: question type {qt!r} not used by Pets / VQA y/n")


def views_for(row):
    if row["qtype"] == "choice":
        return [None, list(range(len(row["options"])))[::-1]]
    return [None]


# ---------------------------------------------------------------- the image processor's arithmetic
def smart_resize(height: int, width: int, factor: int = FACTOR, min_pixels: int = MIN_PIXELS, max_pixels: int = MAX_PIXELS):
    """Qwen2-VL/Qwen3-VL smart_resize: round to multiples of `factor`, then scale into [min_pixels, max_pixels]."""
    if min(height, width) < 1:
        raise ValueError("empty image")
    h = max(factor, round(height / factor) * factor)
    w = max(factor, round(width / factor) * factor)
    if h * w > max_pixels:
        beta = math.sqrt(height * width / max_pixels)
        h = max(factor, math.floor(height / beta / factor) * factor)
        w = max(factor, math.floor(width / beta / factor) * factor)
    elif h * w < min_pixels:
        beta = math.sqrt(min_pixels / (height * width))
        h = math.ceil(height * beta / factor) * factor
        w = math.ceil(width * beta / factor) * factor
    return h, w


def visual_tokens(h: int, w: int) -> int:
    return (h // FACTOR) * (w // FACTOR)


def cap_dims(height: int, width: int, max_tokens: int | None):
    """Target (h, w) for a token cap (None = native). The cap is max_pixels = max_tokens x 32 x 32 in smart_resize."""
    if max_tokens is None:
        return smart_resize(height, width)
    return smart_resize(height, width, max_pixels=max(max_tokens * FACTOR * FACTOR, MIN_PIXELS))


def upscale_dims(height: int, width: int, target_tokens: int):
    """Dims whose smart_resize lands near `target_tokens` by scaling the native size up (latency-only arms)."""
    cur = visual_tokens(*smart_resize(height, width))
    s = math.sqrt(max(target_tokens, 1) / max(cur, 1))
    return smart_resize(int(height * s), int(width * s), min_pixels=MIN_PIXELS, max_pixels=max(target_tokens * 1.1 * FACTOR * FACTOR, MIN_PIXELS))


# ---------------------------------------------------------------- scoring (pure python, = decoder_io.to_probs + 2view average)
def group_logits(resp_item: dict, flat: list, sizes: list) -> list:
    """SGLang meta_info.output_token_ids_logprobs[0] ([[logprob, token_id, None], ...]) -> per-letter logsumexp."""
    got = {int(t[1]): float(t[0]) for t in resp_item["meta_info"]["output_token_ids_logprobs"][0]}
    miss = [t for t in flat if t not in got]
    if miss:
        raise ValueError(f"{len(miss)} candidate ids without a logprob")
    out, k = [], 0
    for s in sizes:
        vals = [got[t] for t in flat[k:k + s]]
        m = max(vals)
        out.append(m + math.log(sum(math.exp(v - m) for v in vals)) if m > -math.inf else -math.inf)
        k += s
    return out


def softmax(xs):
    m = max(xs)
    e = [math.exp(x - m) for x in xs]
    z = sum(e)
    return [v / z for v in e]


def view_probs(row: dict, logits: list, perm) -> dict:
    """decoder_io.to_probs at T = 1.0 for the cygnet style."""
    pr = softmax(logits)
    if row["qtype"] == "noul":
        order = perm if perm is not None else [0, 1]
        p_yes = pr[order.index(0)]
        return {"yes": p_yes, "no": 1 - p_yes}
    opts = row["options"] if perm is None else [row["options"][i] for i in perm]
    return dict(zip(opts, pr))


def decide(row: dict, per_view_logits: list, perms: list) -> list:
    """-> probability vector in the bench's option order (noul: [p_false, p_true])."""
    probs = [view_probs(row, lg, pm) for lg, pm in zip(per_view_logits, perms)]
    if row["qtype"] == "noul":
        p = probs[0]["yes"]
        return [1.0 - p, p]
    if len(probs) == 2:
        return [(probs[0][o] + probs[1][o]) / 2 for o in row["options"]]
    return [probs[0][o] for o in row["options"]]


# ---------------------------------------------------------------- the pack (laptop)
def pick_cases(n_per_suite: int = 100, seed: int = 0, root=VB_DATA) -> list:
    out = []
    for s in SUITES:
        cases = C.read_jsonl(Path(root) / s / "cases.jsonl")
        rng = random.Random(f"{seed}:{s}")
        for c in rng.sample(cases, min(n_per_suite, len(cases))):
            c["_image_file"] = str(Path(root) / s / "images" / Path(c["state"][0]["image"]).name)
            out.append(c)
    return out


def build_pack(out_dir=PACK_DIR, n_per_suite: int = 100, seed: int = 0, tok=None, ro=None, root=VB_DATA, log=print) -> dict:
    """items.jsonl + images/ under out_dir. `tok`/`ro` = I.load_c1(...) results (C1's tokenizer + Readout)."""
    from . import items as I
    dio = I.readout_mod().dio
    out_dir = Path(out_dir)
    (out_dir / "images").mkdir(parents=True, exist_ok=True)
    rows = []
    for c in pick_cases(n_per_suite, seed, root):
        qname, q = next(iter(c["questions"].items()))
        row, keys = to_row(q)
        views = views_for(row)
        groups = ro.cand(row)
        flat = [t for g in groups for t in g]
        texts, n_text = [], []
        for perm in views:
            text = dio.prompt_texts(ro, [row], [perm])[0]
            assert text.count("<|image_pad|>") == 1, "the image placeholder must appear once in the prompt"
            texts.append(text)
            n_text.append(len(tok(text, add_special_tokens=False)["input_ids"]))
        g = c["gold"][qname]
        src = Path(c["_image_file"])
        dst = out_dir / "images" / f"{c['id']}{src.suffix}"
        dst.write_bytes(src.read_bytes())
        rows.append({"id": c["id"], "suite": c["suite"], "qtype": row["qtype"], "row": row, "perms": views, "texts": texts,
                     "n_text_tokens": n_text, "flat": flat, "sizes": [len(x) for x in groups],
                     "options": bench_options(q), "gold": gold_index(q, g), "image": f"images/{dst.name}"})
    C.write_jsonl(out_dir / "items.jsonl", rows)
    meta = {"n": len(rows), "by_suite": {s: sum(1 for r in rows if r["suite"] == s) for s in SUITES}, "seed": seed,
            "image_bytes": sum((out_dir / r["image"]).stat().st_size for r in rows), "built_utc": C.utc()}
    C.write_json(out_dir / "pack.json", meta)
    log(f"vision pack: {meta}")
    return meta


# ---------------------------------------------------------------- the container side (image python: PIL + httpx)
def prepare_image(path: Path, max_tokens: int | None, upscale_to: int | None = None) -> tuple:
    """-> (png/jpeg bytes, (h, w) sent, predicted visual tokens). Native = the file as is (the server does its own resize)."""
    from PIL import Image
    im = Image.open(path)
    im.load()
    im = im.convert("RGB")
    w0, h0 = im.size
    if upscale_to is not None:
        h, w = upscale_dims(h0, w0, upscale_to)
    else:
        h, w = cap_dims(h0, w0, max_tokens)
    if upscale_to is None and max_tokens is None:
        return path.read_bytes(), (h0, w0), visual_tokens(h, w)
    if (h, w) != (h0, w0):
        im = im.resize((w, h), Image.BICUBIC)
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    return buf.getvalue(), (h, w), visual_tokens(h, w)


def data_uri(img_bytes: bytes) -> str:
    """image_data entry as a data: URI. A BARE base64 string is not safe: SGLang's loader treats a string starting with "/" as a
    file path, and every JPEG's base64 starts with "/9j/" (17 Oct run: the native arm, which sends the original JPEGs, got 200 HTTP 500s
    'File name too long'; the re-encoded PNG arms worked because "iVBOR" does not start with "/")."""
    mime = "image/jpeg" if img_bytes[:3] == b"\xff\xd8\xff" else "image/png"
    return f"data:{mime};base64,{base64.b64encode(img_bytes).decode()}"


def post_item(client, it: dict, img_bytes: bytes, pred_tokens: int, timeout: float = 120.0) -> dict:
    """Both views of one item; returns {probs, ms, prompt_tokens, token_mismatch}."""
    b64 = data_uri(img_bytes)
    logits, ptoks, t0 = [], [], time.perf_counter()
    for text in it["texts"]:
        body = {"text": text, "image_data": [b64], "sampling_params": dict(SAMPLING), "return_logprob": True,
                "logprob_start_len": -1, "token_ids_logprob": it["flat"], "stream": False}
        r = client.post("/generate", json=body, timeout=timeout)
        r.raise_for_status()
        d = r.json()
        d = d[0] if isinstance(d, list) else d
        logits.append(group_logits(d, it["flat"], it["sizes"]))
        ptoks.append(int(d["meta_info"]["prompt_tokens"]))
    ms = (time.perf_counter() - t0) * 1000.0
    probs = decide(it["row"], logits, it["perms"])
    exp = [nt - 1 + pred_tokens for nt in it["n_text_tokens"]]
    return {"probs": probs, "ms": ms, "prompt_tokens": ptoks, "expected_tokens": exp, "token_mismatch": ptoks != exp}


def run_vision(spec: dict, log=print) -> dict:
    """spec: sgl_url, pack_dir, caps ([None | int]), upscale ([int]), upscale_n, warm. Sequential, batch 1."""
    import httpx
    pack = Path(spec["pack_dir"])
    items = C.read_jsonl(pack / "items.jsonl")
    client = httpx.Client(base_url=spec["sgl_url"], timeout=120.0)
    out = {"n_items": len(items), "arms": {}}
    arms = [{"name": "native" if c is None else f"cap{c}", "max_tokens": c} for c in spec.get("caps", [None, 256, 128, 64])]
    arms += [{"name": f"upscale{u}", "upscale": u} for u in spec.get("upscale", [1024, 2048, 4096])]
    for arm in arms:
        sub = items[: int(spec.get("upscale_n", 24))] if "upscale" in arm else items
        warm = sub[: int(spec.get("warm", 6))]
        for it in warm:
            b, hw, pt = prepare_image(pack / it["image"], arm.get("max_tokens"), arm.get("upscale"))
            try:
                post_item(client, it, b, pt)
            except Exception:  # noqa: BLE001
                pass
        recs, errs = [], 0
        for it in sub:
            t_prep = time.perf_counter()
            b, hw, pt = prepare_image(pack / it["image"], arm.get("max_tokens"), arm.get("upscale"))
            prep_ms = (time.perf_counter() - t_prep) * 1000.0
            try:
                r = post_item(client, it, b, pt)
            except Exception as e:  # noqa: BLE001
                errs += 1
                recs.append({"id": it["id"], "suite": it["suite"], "error": f"{type(e).__name__}: {str(e)[:100]}"})
                continue
            p = r["probs"]
            pred = max(range(len(p)), key=p.__getitem__)
            recs.append({"id": it["id"], "suite": it["suite"], "ok": True, "correct": int(pred == it["gold"]), "pred": pred,
                         "probs": [round(x, 6) for x in p], "ms": r["ms"], "prep_ms": prep_ms, "size_hw": list(hw),
                         "pred_tokens": pt, "prompt_tokens": r["prompt_tokens"], "token_mismatch": r["token_mismatch"]})
        good = [r for r in recs if r.get("ok")]
        by = {}
        for s in SUITES:
            g = [r for r in good if r["suite"] == s]
            if g:
                by[s] = {"n": len(g), "acc": round(100 * sum(r["correct"] for r in g) / len(g), 2),
                         "ms": C.summarize([r["ms"] for r in g])}
        out["arms"][arm["name"]] = {"n": len(good), "errors": errs, "acc": round(100 * sum(r["correct"] for r in good) / len(good), 2) if good else None,
                                    "by_suite": by, "ms_per_decision": C.summarize([r["ms"] for r in good]),
                                    "prep_ms": C.summarize([r["prep_ms"] for r in good]),
                                    "visual_tokens_pred": C.summarize([r["pred_tokens"] for r in good], 1),
                                    "token_mismatches": sum(r["token_mismatch"] for r in good), "records": recs}
        log(f"vision arm {arm['name']}: {out['arms'][arm['name']]['acc']}% on {len(good)}; "
            f"p50 {out['arms'][arm['name']]['ms_per_decision'].get('p50')} ms; mismatches {out['arms'][arm['name']]['token_mismatches']}")
    base = out["arms"].get("native", {}).get("records", [])
    bmap = {r["id"]: r for r in base if r.get("ok")}
    for name, a in out["arms"].items():
        same = n = 0
        for r in a["records"]:
            b = bmap.get(r.get("id"))
            if r.get("ok") and b:
                n += 1
                same += r["pred"] == b["pred"]
        a["agree_with_native"] = round(same / n, 4) if n else None
    return out
