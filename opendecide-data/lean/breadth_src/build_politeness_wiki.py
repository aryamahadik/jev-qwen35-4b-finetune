"""Build raw rows for politeness_wiki (Stanford Politeness Corpus, Wikipedia half, ConvoKit release).

Source : ConvoKit wikipedia-politeness-corpus.zip (NOT the Stack Exchange corpus; SE is an OHS-3 platform).
Licence: CC BY 4.0, stated in the ConvoKit docs "Data License" section
         (https://convokit.cornell.edu/documentation/wiki_politeness.html).
Labels : ConvoKit "Binary" (-1 impolite = bottom quartile, 0 neutral = middle half, +1 polite = top quartile of
         the Normalized Score). Normalized Score = mean of the 5 MTurk raters' per-worker z-scores (verified exactly).
Soft   : each rater's z-score is binned with the same quartile cut points as Binary -> 5 votes -> probabilities.
Split  : the corpus has no official split; the whole release is treated as train, and every text that appears in
         Cleanlab's stanford-politeness test.csv (a public test set built from this corpus) is dropped.
Overlap: texts are Wikipedia talk-page requests, and Kaggle Jigsaw (Wikipedia talk comments) sits inside the
         forbidden tasksource/zero-shot-label-nli via mbib-base/hate-speech, so any request sharing a 10-word run with
         a Jigsaw train/test comment is dropped (thesofakillers mirror, pinned revision + sha256). A one-off 10-gram
         scan of all label-NLI premises (train/validation/test, 27 Sep 2026) found no real overlap (1 generic phrase).
         Also standard 13-gram + exact-state decontamination against our data/*.jsonl (never ohs*) and JevBench public.
Deterministic (seed 20261101); raw snapshots are pinned by sha256 under cache/politeness_wiki/.
"""
import collections
import glob
import hashlib
import json
import pickle
import random
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np

SEED = 20261101
MAX_ROWS = 450
KEY = "politeness_wiki"
HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
CACHE = HERE / "cache" / KEY
OUT = LEAN / "data" / "v13_parts" / "raw" / f"{KEY}.jsonl"
DEFS = LEAN / "data" / "v13_parts" / "defs" / f"{KEY}.json"
JB = LEAN.parents[1] / "bench/jevbench/datasets/public"
JIG_REPO = "thesofakillers/jigsaw-toxic-comment-classification-challenge"
JIG_REV = "50f3c926ec8c07b440cb17b55d8cd80e8484497e"
JIG_SHA = {"train.csv": "bd4084611bd27c939ba98e5e63bc3e5a2c1a4e99477dcba46c829e4c986c429d",
           "test.csv": "c2513ce4abb98c4d1d216e3ca0d4377d57589a0989aa8c06a840509a16c786e8"}

ZIP_URL = "https://zissou.infosci.cornell.edu/convokit/datasets/wikipedia-politeness-corpus/wikipedia-politeness-corpus.zip"
ZIP_SHA = "90ec6c2c6e05d064a805d2e4be4a8d442f370b31f0025798e8eaf62d0014ba48"
CL_URL = "https://s.cleanlab.ai/stanford-politeness/fine-tuning/test.csv"
CL_SHA = "78b7f79887351aa4f5f089f1990b86c94343f1c170f0ed5652b825c5cc3b3306"

LICENCE = ("CC BY 4.0 (ConvoKit docs, 'Data License': https://convokit.cornell.edu/documentation/wiki_politeness.html; "
           "Copyright (C) 2017-2020 The ConvoKit Developers)")
INSTRUCTIONS = "How polite is this request?"
NAMES = {-1: "impolite", 0: "neutral", 1: "polite"}
OPTIONS = ["impolite", "neutral", "polite"]
# Labels are relative bands of the averaged 25-point MTurk politeness rating (bottom quarter / middle half / top
# quarter), so definitions describe how the request compares with a typical Wikipedia editor request.
DEF = {
    "impolite": "Among the least polite requests (bottom quarter as rated by annotators): noticeably blunter than a typical request, e.g. challenging direct questions ('Why did you...?', 'What is this?'), commands (including a bare sentence-initial 'Please ...' used as an order), accusations, sarcasm or impatience ('???'), openings like 'So' or 'You', and no greeting, thanks, apology or softening. It need not contain insults.",
    "neutral": "A typical, middle-of-the-road request (the middle half of ratings): plain matter-of-fact wording, or only one mild courtesy such as a single 'can/could you' or 'please' without warmth, or polite and blunt cues that roughly cancel out.",
    "polite": "Among the most polite requests (top quarter as rated by annotators): clearly more courteous than a typical request, usually combining several cues such as greeting, thanks, apology, praise or deference ('great work on...'), hedging ('I think', 'perhaps') and indirect phrasing ('would you mind', 'could you please'). A single 'could you' alone is not enough.",
}


def fetch(url, path, sha):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, path)
    got = hashlib.sha256(path.read_bytes()).hexdigest()
    if got != sha:
        sys.exit(f"sha256 mismatch for {path}: {got}")


def norm(t):
    return re.sub(r"\s+", " ", t).strip().lower()


def words(t):
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).split()


def gram_index(recs, n):
    """map n-word run -> set of rids (ConvoKit placeholders <url>/<person> removed first)."""
    g = collections.defaultdict(set)
    for rid, text in recs.items():
        w = [x for x in words(text) if x not in ("url", "person")]
        for i in range(len(w) - n + 1):
            g[" ".join(w[i:i + n])].add(rid)
    return g


def scan(texts, g, n):
    hit = set()
    for t in texts:
        w = words(t)
        for i in range(len(w) - n + 1):
            k = " ".join(w[i:i + n])
            if k in g:
                hit |= g[k]
    return hit


def jigsaw_hits(recs):
    """rids sharing a 10-word run with any Kaggle Jigsaw (Wikipedia talk) comment, train or test."""
    import pandas as pd
    from huggingface_hub import hf_hub_download
    g = gram_index(recs, 10)
    hit = set()
    for fn, sha in JIG_SHA.items():
        path = Path(hf_hub_download(JIG_REPO, fn, repo_type="dataset", revision=JIG_REV))
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        if got != sha:
            sys.exit(f"sha256 mismatch for jigsaw {fn}: {got}")
        hit |= scan(pd.read_csv(path)["comment_text"].astype(str), g, 10)
    return hit


def contam(recs, n=13):
    """rids sharing a 13-gram with, or exactly equal to a state in, our train/dev/eval files or JevBench public."""
    g = gram_index(recs, n)
    exact = collections.defaultdict(set)
    for rid, text in recs.items():
        exact[" ".join(words(text))].add(rid)
    files = sorted(f for f in glob.glob(str(LEAN / "data" / "*.jsonl")) if not Path(f).name.startswith("ohs"))
    files += sorted(glob.glob(str(JB / "*.jsonl")))
    hit = set()
    for f in files:
        for line in open(f, encoding="utf-8"):
            try:
                r = json.loads(line)
            except Exception:
                continue
            st = r.get("state") if isinstance(r, dict) else None
            if isinstance(st, str):
                hit |= exact.get(" ".join(words(st)), set())
            hit |= scan([line.replace("\\n", " ")], g, n)
    return hit, len(files)


def main():
    zpath = CACHE / "wikipedia-politeness-corpus.zip"
    cpath = CACHE / "cleanlab_test.csv"
    fetch(ZIP_URL, zpath, ZIP_SHA)
    fetch(CL_URL, cpath, CL_SHA)

    with zipfile.ZipFile(zpath) as z:
        utts = [json.loads(l) for l in z.read("wikipedia-politeness-corpus/utterances.jsonl").decode().splitlines() if l.strip()]
        ann = pickle.loads(z.read("wikipedia-politeness-corpus/Annotations-bin.p"))

    import pandas as pd
    cl_test = {norm(t) for t in pd.read_csv(cpath)["prompt"].astype(str)}

    # per-worker z-score stats (reproduces ConvoKit "Normalized Score" exactly)
    per_w = collections.defaultdict(list)
    for d in ann:
        for w, s in d.items():
            per_w[w].append(int(s))
    wstat = {w: (float(np.mean(v)), float(np.std(v)) or 1.0) for w, v in per_w.items()}

    def ann_of(u):
        return ann[int(re.search(r"bin\{(\d+)\}", u["meta"]["Annotations"]).group(1))]

    # quartile cut points implied by Binary
    by_b = collections.defaultdict(list)
    for u in utts:
        by_b[u["meta"]["Binary"]].append(u["meta"]["Normalized Score"])
    lo = (max(by_b[-1]) + min(by_b[0])) / 2
    hi = (max(by_b[0]) + min(by_b[1])) / 2

    def vote(z):
        return "impolite" if z < lo else ("polite" if z >= hi else "neutral")

    recs = {str(u["id"]): u["text"] for u in utts}
    jig = jigsaw_hits(recs)
    dirty, nfiles = contam(recs)

    stats = collections.Counter()
    seen = set()
    pools = collections.defaultdict(list)
    for u in utts:
        text = u["text"]
        n = norm(text)
        if str(u["id"]) in jig:
            stats["jigsaw_overlap_drop"] += 1
            continue
        if str(u["id"]) in dirty:
            stats["decontam_drop"] += 1
            continue
        if not (15 <= len(text.strip()) <= 4000):
            stats["len_drop"] += 1
            continue
        if n in cl_test:
            stats["cleanlab_test_drop"] += 1
            continue
        if n in seen:
            stats["dup_drop"] += 1
            continue
        seen.add(n)
        d = ann_of(u)
        zs = [(int(s) - wstat[w][0]) / wstat[w][1] for w, s in d.items()]
        assert abs(np.mean(zs) - u["meta"]["Normalized Score"]) < 1e-6
        votes = collections.Counter(vote(z) for z in zs)
        soft = {o: round(votes[o] / len(zs), 4) for o in OPTIONS}
        gold = NAMES[u["meta"]["Binary"]]
        pools[gold].append({
            "key": KEY,
            "rid": str(u["id"]),
            "state": text,
            "instructions": INSTRUCTIONS,
            "options": OPTIONS,
            "gold": gold,
            "soft": soft,
            "meta": {
                "dataset": "ConvoKit wikipedia-politeness-corpus (Stanford Politeness Corpus, Wikipedia half)",
                "config": "wikipedia-politeness-corpus.zip",
                "revision": f"sha256:{ZIP_SHA}",
                "licence": LICENCE,
                "split": "train",
                "orig_label": {"Binary": u["meta"]["Binary"],
                               "Normalized Score": round(u["meta"]["Normalized Score"], 4),
                               "ratings_1to25": sorted(int(s) for s in d.values())},
            },
        })

    rng = random.Random(SEED)
    for k in sorted(pools):
        pools[k].sort(key=lambda r: r["rid"])
        rng.shuffle(pools[k])
    out = []
    labels = sorted(pools)
    i = 0
    while len(out) < MAX_ROWS and any(pools[k] for k in labels):
        k = labels[i % len(labels)]
        if pools[k]:
            out.append(pools[k].pop())
        i += 1
    rng.shuffle(out)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    DEFS.parent.mkdir(parents=True, exist_ok=True)
    DEFS.write_text(json.dumps(DEF, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    lens = [len(r["state"]) for r in out]
    cnt = collections.Counter(r["gold"] for r in out)
    agree = sum(max(r["soft"], key=r["soft"].get) == r["gold"] for r in out)
    print(f"decontam files scanned={nfiles}")
    print(f"source utterances={len(utts)} cut points lo={lo:.4f} hi={hi:.4f} drops={dict(stats)}")
    print(f"wrote {len(out)} rows -> {OUT}")
    print("per label:", {k: f"{v} ({v / len(out):.1%})" for k, v in sorted(cnt.items())})
    print(f"soft coverage: {sum(r['soft'] is not None for r in out)}/{len(out)}; soft argmax == gold: {agree / len(out):.1%}")
    print(f"length chars: min={min(lens)} median={int(np.median(lens))} mean={np.mean(lens):.0f} max={max(lens)}")


if __name__ == "__main__":
    main()
