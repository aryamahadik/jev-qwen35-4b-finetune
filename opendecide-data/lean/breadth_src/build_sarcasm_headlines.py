"""Build raw rows for 'sarcasm_headlines' (News Headlines Dataset for Sarcasm Detection v2, Misra).

Source   : HF raquiba/Sarcasm_News_Headline, revision 643ceefc17441e56cff66f57c03b13615545d42b,
           train.json ONLY (test.json is never downloaded or read).
           Raw snapshot: breadth_src/cache/sarcasm_headlines/train.json (+ README.md).
Licence  : CC BY 4.0, stated on the original Kaggle dataset page
           (kaggle.com/datasets/rmisra/news-headlines-dataset-for-sarcasm-detection, "License: Attribution 4.0
           International (CC BY 4.0)"); the HF mirror README carries no licence field.
Provenance: headlines written by professional editors (TheOnion = sarcastic, HuffPost = not sarcastic); the label
           is the publishing outlet (human editorial provenance), no model involvement.

Rules applied
- article_link is dropped (it names the outlet and would leak the label).
- Outlet redaction: rows whose headline names the outlets (onion / huffpost / huffington / huffpollster) are
  dropped rather than masked, so no placeholder artefacts enter the text.
- Shortcut removal: rows with parenthetical tags such as "(video)", "(update)", "(nsfw)" are dropped; in the
  train file every parenthesised headline is a HuffPost one, so this is a pure label cue. Square brackets are
  treated the same (HuffPost column tags such as "[in&out korea]", 4 HuffPost / 0 Onion).
- Media-post cue (verifier fix): headlines that open with "watch" / "listen" (HuffPost video/audio post form,
  "watch: ...", "watch live: ...", "watch X do Y"; 156 HuffPost / 1 Onion in train) are dropped.
- Censoring cue (verifier fix): headlines with asterisk-masked profanity ("f**k", "bullsh*t"; 35 HuffPost /
  2 Onion, while TheOnion prints profanity uncensored) are dropped.
- Text length 15-4,000 chars; exact-duplicate headlines (normalised) removed, and headlines that occur with
  both labels are dropped entirely.
- Dedup vs MN-DS (textminr/mn-ds @8b746353, titles + article bodies) and NewsMTSC (fhamborg/NewsMTSC @6b838e00,
  rw-hf and mt-hf train.jsonl sentences): drop exact normalised matches and headlines contained in any of
  their texts.
- Label-balanced round-robin over {yes, no}, at most 300 rows. Deterministic, seed 20261101.
"""
import json
import os
import random
import re
import shutil
from collections import Counter

import requests
from huggingface_hub import hf_hub_download

SEED = 20261101
KEY = "sarcasm_headlines"
REPO = "raquiba/Sarcasm_News_Headline"
REV = "643ceefc17441e56cff66f57c03b13615545d42b"
MNDS_REPO = "textminr/mn-ds"
MNDS_REV = "8b7463539dfa6093998523f7f9fb0b1ea0b867e6"
NEWSMTSC_URL = ("https://raw.githubusercontent.com/fhamborg/NewsMTSC/6b838e00f54423c253806327a0ae24dbffa24c9e/"
                "NewsSentiment/experiments/default/datasets/{cfg}/train.jsonl")
LICENCE = ("CC BY 4.0 (Kaggle dataset page rmisra/news-headlines-dataset-for-sarcasm-detection; "
           "HF mirror raquiba/Sarcasm_News_Headline has no licence field)")
MAX_ROWS = 300
QUESTION = "Is this news headline sarcastic?"
OPTIONS = ["yes", "no"]

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "cache", KEY)
OUT = os.path.join(LEAN, "data", "v13_parts", "raw", f"{KEY}.jsonl")

OUTLET = re.compile(r"onion|huff|huffington|huffpost|huffpollster", re.I)
PAREN = re.compile(r"[()\[\]]")
MEDIA = re.compile(r"^(watch|listen)\b")
STAR = re.compile(r"\*")


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s.lower())).strip()


def snapshot():
    os.makedirs(CACHE, exist_ok=True)
    for f in ("train.json", "README.md"):  # never test.json
        dst = os.path.join(CACHE, f)
        if not os.path.exists(dst):
            shutil.copy(hf_hub_download(REPO, f, repo_type="dataset", revision=REV), dst)
    return os.path.join(CACHE, "train.json")


def dedup_corpus():
    """Return (exact_set, big_text) of normalised MN-DS + NewsMTSC train texts."""
    texts = []
    p = hf_hub_download(MNDS_REPO, "train.jsonl", repo_type="dataset", revision=MNDS_REV)
    with open(p) as fh:
        for line in fh:
            r = json.loads(line)
            texts.append(r.get("title") or "")
            texts.append(r.get("content") or "")
    ddir = os.path.join(CACHE, "dedup")
    os.makedirs(ddir, exist_ok=True)
    for cfg in ("newsmtsc-rw-hf", "newsmtsc-mt-hf"):
        dst = os.path.join(ddir, f"{cfg}_train.jsonl")
        if not os.path.exists(dst):
            resp = requests.get(NEWSMTSC_URL.format(cfg=cfg), timeout=120)
            resp.raise_for_status()
            with open(dst, "wb") as out:
                out.write(resp.content)
        with open(dst) as fh:
            for line in fh:
                texts.append(json.loads(line)["sentence"])
    normed = [norm(t) for t in texts if t]
    return set(normed), " | ".join(normed)


def main():
    path = snapshot()
    recs = []
    with open(path) as fh:
        for i, line in enumerate(fh):
            r = json.loads(line)
            recs.append((i, r["headline"], int(r["is_sarcastic"])))

    stats = Counter()
    by_norm = {}
    for i, h, y in recs:
        by_norm.setdefault(norm(h), set()).add(y)

    exact, big = dedup_corpus()
    seen = set()
    pools = {"yes": [], "no": []}
    for i, h, y in recs:
        n = norm(h)
        if not (15 <= len(h) <= 4000):
            stats["drop_length"] += 1
            continue
        if OUTLET.search(h):
            stats["drop_outlet_mention"] += 1
            continue
        if PAREN.search(h):
            stats["drop_paren_cue"] += 1
            continue
        if MEDIA.search(h):
            stats["drop_media_post_cue"] += 1
            continue
        if STAR.search(h):
            stats["drop_asterisk_censor_cue"] += 1
            continue
        if len(by_norm[n]) > 1:
            stats["drop_conflicting_label"] += 1
            continue
        if n in seen:
            stats["drop_duplicate"] += 1
            continue
        seen.add(n)
        pools["yes" if y == 1 else "no"].append((i, h, y))

    rng = random.Random(SEED)
    for k in ("yes", "no"):
        rng.shuffle(pools[k])

    def ok(n):
        if n in exact or (len(n) >= 20 and n in big):
            stats["drop_overlap_mnds_newsmtsc"] += 1
            return False
        return True

    rows, iters = [], {k: iter(v) for k, v in pools.items()}
    order = ["yes", "no"]
    rng.shuffle(order)
    while len(rows) < MAX_ROWS:
        progressed = False
        for lab in order:
            if len(rows) >= MAX_ROWS:
                break
            for i, h, y in iters[lab]:
                if ok(norm(h)):
                    rows.append({
                        "key": KEY,
                        "rid": f"train.json:{i}",
                        "state": h,
                        "instructions": QUESTION,
                        "options": OPTIONS,
                        "gold": lab,
                        "soft": None,
                        "meta": {"dataset": REPO, "config": "default", "revision": REV, "licence": LICENCE,
                                 "split": "train", "orig_label": y},
                    })
                    progressed = True
                    break
        if not progressed:
            break

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    L = sorted(len(r["state"]) for r in rows)
    print("source rows:", len(recs), "filter stats:", dict(stats))
    print("pool sizes:", {k: len(v) for k, v in pools.items()})
    print("written:", len(rows), "->", OUT)
    print("labels:", dict(Counter(r["gold"] for r in rows)))
    print("soft coverage:", sum(r["soft"] is not None for r in rows), "/", len(rows))
    print("length chars min/median/mean/max:", L[0], L[len(L) // 2], round(sum(L) / len(L), 1), L[-1])


if __name__ == "__main__":
    main()
