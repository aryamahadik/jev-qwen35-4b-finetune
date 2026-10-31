"""Rebuild the five Vision Index suites of the System One vision track (img_refcoco is skipped: C1 has no box readout).

Re-implements build_suites.py / build_arabic.py / build_images.py for the needed suites, same pinned revisions, same seeds,
same selection rules, same fit() / save() rules. Output per suite, in its own folder under data/:
    data/<suite>/cases.jsonl      one case per line, in the bench's own format (state holds "images/<suite>/<n>.<ext>")
    data/<suite>/images/<n>.<ext> the image files (the bench path "images/<suite>/<n>.<ext>" maps to this folder)
verify_lock.py then compares the suite hashes with data.lock.json of the bench.
Run:  HF_HOME=<vision_bench>/hf_cache .venv/bin/python -I harness/build_data.py [suite ...]
"""
import io
import json
import math
import os
import random
import shutil
import sys

from datasets import load_dataset
from PIL import Image, ImageOps

ROOT = "/Users/aryamahadik/Documents/jev/vision_bench"
SRC_IMG = f"{ROOT}/src/system-one-bench/images"
DATA = f"{ROOT}/data"
CACHE = f"{ROOT}/hf_cache"
N, SEED = 200, 0
LONG = 1024
MIN_SIDE, MAX_SIDE, MIN_PIXELS = 280, 1568, 78_400
MAX_BYTES = 300_000

REV = {
    "stanfordnlp/sst2": "8d51e7e4887a4caaa95b3fbebbf53c0490b58bbb",
    "mteb/tweet_sentiment_multilingual": "bceb37eb62681b42e4147d879384917969bb1674",
    "timm/oxford-iiit-pet": "089695c834a7deb60505b7cc506672db1c31a6aa",
    "lmms-lab-encoder/VQAv2": "32665d35052eb4a6d4414851c3c829a72754915a",
    "vikhyatk/CountBenchQA": "76d600309e9d6147bd3713b4cd431518ac1206c8",
}


def load(name, *a, **kw):
    return load_dataset(name, *a, revision=REV[name], cache_dir=CACHE, **kw)


def perm(n, seed=SEED):
    idx = list(range(n))
    random.Random(seed).shuffle(idx)
    return idx


def fit(im):
    im = ImageOps.exif_transpose(im).convert("RGB")
    w, h = im.size
    s = min(1.0, LONG / max(w, h))
    s = max(s, MIN_SIDE / min(w, h), math.sqrt(MIN_PIXELS / (w * h)))
    if max(w, h) * s > MAX_SIDE:
        return None
    if abs(s - 1) > 1e-3:
        im = im.resize((math.ceil(w * s), math.ceil(h * s)), Image.LANCZOS)
    return im


class Suite:
    def __init__(self, name):
        self.name = name
        self.dir = f"{DATA}/{name}"
        if os.path.exists(self.dir):
            shutil.rmtree(self.dir)
        os.makedirs(f"{self.dir}/images")
        self.cases = []

    def save(self, im, i):
        for q in (88, 82, 75, 68, 60):
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=q, optimize=True)
            if buf.tell() <= MAX_BYTES:
                break
        with open(f"{self.dir}/images/{i}.jpg", "wb") as f:
            f.write(buf.getvalue())
        return {"image": f"images/{self.name}/{i}.jpg"}

    def png(self, i):  # committed rendered-text picture
        shutil.copyfile(f"{SRC_IMG}/{self.name}/{i}.png", f"{self.dir}/images/{i}.png")
        return {"image": f"images/{self.name}/{i}.png"}

    def add(self, i, image, qid, q, gold):
        self.cases.append({"suite": self.name, "id": f"{self.name}-{i}", "state": [image], "questions": {qid: q},
                           "gold": {qid: {"type": q["type"], **gold}}})

    def done(self):
        assert len(self.cases) == N, (self.name, len(self.cases))
        with open(f"{self.dir}/cases.jsonl", "w") as f:
            for c in self.cases:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
        print(self.name, len(self.cases), "cases", flush=True)


def img_sst2():
    s = Suite("img_sst2")
    ds = load("stanfordnlp/sst2", split="validation")
    for i, k in enumerate(perm(len(ds))[:N]):
        r = ds[k]
        s.add(i, s.png(i), "positive",
              {"type": "noul", "instructions": "Does the movie review shown in the image express a positive opinion of the movie?"},
              {"label": int(r["label"])})
    s.done()


def img_ar_sentiment():
    s = Suite("img_ar_sentiment")
    ds = load("mteb/tweet_sentiment_multilingual", "arabic", split="test")
    names = ["negative", "neutral", "positive"]
    SE = {"negative": "the writer expresses a negative opinion or feeling",
          "neutral": "no clear positive or negative opinion",
          "positive": "the writer expresses a positive opinion or feeling"}
    for i, k in enumerate(perm(len(ds))[:N]):
        r = ds[k]
        s.add(i, s.png(i), "sentiment",
              {"type": "choice", "instructions": "What is the sentiment of the Arabic tweet shown in the image?", "criteria": SE},
              {"label": names[int(r["label"])]})
    s.done()


def img_pets():
    s = Suite("img_pets")
    pets = load("timm/oxford-iiit-pet", split="test")
    names = pets.features["label"].names
    CATS = {"abyssinian", "bengal", "birman", "bombay", "british_shorthair", "egyptian_mau", "maine_coon", "persian",
            "ragdoll", "russian_blue", "siamese", "sphynx"}
    PETS = {n: f"{n.replace('_', ' ').title()} ({'cat' if n in CATS else 'dog'} breed)" for n in names}
    i = 0
    for k in perm(len(pets)):
        r = pets[k]
        im = fit(r["image"])
        if im is None:
            continue
        s.add(i, s.save(im, i), "breed",
              {"type": "choice", "instructions": "Which breed is the pet in the image?", "criteria": PETS},
              {"label": names[r["label"]]})
        i += 1
        if i == N:
            break
    s.done()


def img_vqa_yesno():
    s = Suite("img_vqa_yesno")
    vqa = load("lmms-lab-encoder/VQAv2", data_files={"validation": "data/validation-00000-of-00068.parquet"}, split="validation")
    vqa = vqa.filter(lambda r: r["answer_type"] == "yes/no" and r["multiple_choice_answer"] in ("yes", "no"))
    seen, i = set(), 0
    for k in perm(len(vqa)):
        r = vqa[k]
        if r["image_id"] in seen:
            continue
        im = fit(r["image"])
        if im is None:
            continue
        seen.add(r["image_id"])
        s.add(i, s.save(im, i), "answer_yes",
              {"type": "noul", "instructions": f"Looking at the image, is the answer to this question yes? {r['question']}"},
              {"label": int(r["multiple_choice_answer"] == "yes")})
        i += 1
        if i == N:
            break
    s.done()


def img_count():
    s = Suite("img_count")
    cb = load("vikhyatk/CountBenchQA", split="test")
    WORDS = ["two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    i = 0
    for k in perm(len(cb)):
        r = cb[k]
        im = fit(r["image"])
        if im is None or not 2 <= r["number"] <= 10:
            continue
        s.add(i, s.save(im, i), "count",
              {"type": "score", "instructions": r["question"], "criteria": [f"exactly {w}" for w in WORDS]},
              {"label": r["number"] - 2})
        i += 1
        if i == N:
            break
    s.done()


if __name__ == "__main__":
    todo = sys.argv[1:] or ["img_sst2", "img_ar_sentiment", "img_pets", "img_vqa_yesno", "img_count"]
    for name in todo:
        globals()[name]()
