"""Build raw rows for 'claimbuster' (ClaimBuster crowdsourced check-worthiness, 3-way).

Source: Zenodo record 3609356 (ClaimBuster: A Benchmark Dataset of Check-worthy Factual Claims),
file crowdsourced.csv ONLY (md5 af9649bc3cc93edbc804893720a50bde). groundtruth.csv is the test
set and is never downloaded or read. Licence: CC BY 4.0 (Zenodo record metadata 'license': cc-by-4.0).
Texts: sentences from US presidential debates 1960-2016 (human speech transcripts).
Labels: crowdsourced human annotations (Verdict: -1 NFS, 0 UFS, 1 CFS). No annotator counts -> soft=null.
Filters: 15-4000 chars, >=4 words, no interrupted fragments ending in '...'/'--', dedup (normalised).
Deterministic: seed 20261101; raw snapshot cached under breadth_src/cache/claimbuster/.
"""
import hashlib, json, os, random, re, urllib.request
import pandas as pd

SEED = 20261101
HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "cache", "claimbuster")
SRC = os.path.join(CACHE, "crowdsourced.csv")
URL = "https://zenodo.org/api/records/3609356/files/crowdsourced.csv/content"
MD5 = "af9649bc3cc93edbc804893720a50bde"
OUT = os.path.join(LEAN, "data", "v13_parts", "raw", "claimbuster.jsonl")
MAX_ROWS = 450

LABELS = {-1: "Non-factual statement", 0: "Unimportant factual statement", 1: "Check-worthy factual claim"}
OPTIONS = [LABELS[-1], LABELS[0], LABELS[1]]
INSTR = "Which kind of statement is this sentence from a political debate?"
META = {"dataset": "ClaimBuster (Zenodo 3609356) crowdsourced.csv", "config": "crowdsourced",
        "revision": "zenodo-3609356 crowdsourced.csv md5:" + MD5,
        "licence": "CC BY 4.0 (Zenodo record 3609356 metadata: license cc-by-4.0)", "split": "train"}


def fetch():
    os.makedirs(CACHE, exist_ok=True)
    if not os.path.exists(SRC):
        urllib.request.urlretrieve(URL, SRC)
    h = hashlib.md5(open(SRC, "rb").read()).hexdigest()
    assert h == MD5, f"md5 mismatch {h}"


def norm(t):
    return re.sub(r"\W+", " ", t.lower()).strip()


def main():
    fetch()
    df = pd.read_csv(SRC)
    assert df.Sentence_id.is_unique
    rng = random.Random(SEED)
    seen, pools = set(), {k: [] for k in LABELS}
    for r in df.sort_values("Sentence_id").itertuples(index=False):
        t = str(r.Text).strip()
        if not (15 <= len(t) <= 4000) or len(t.split()) < 4:
            continue
        # drop interrupted / trailing-off transcript fragments (end in '...' or '--'): low-signal, incomplete
        if re.search(r"(\.\.\.|\u2026|--|\u2014)\s*$", t):
            continue
        k = norm(t)
        if k in seen:
            continue
        seen.add(k)
        pools[int(r.Verdict)].append(r)
    for k in pools:
        rng.shuffle(pools[k])
    # round-robin over labels -> exactly balanced (150 each)
    rows, i = [], 0
    order = [1, 0, -1]
    while len(rows) < MAX_ROWS and any(i < len(pools[k]) for k in order):
        for k in order:
            if i < len(pools[k]) and len(rows) < MAX_ROWS:
                rows.append(pools[k][i])
        i += 1
    rng.shuffle(rows)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        for r in rows:
            f.write(json.dumps({
                "key": "claimbuster", "rid": str(r.Sentence_id), "state": str(r.Text).strip(),
                "instructions": INSTR, "options": OPTIONS, "gold": LABELS[int(r.Verdict)], "soft": None,
                "meta": {**META, "orig_label": int(r.Verdict)},
            }, ensure_ascii=False) + "\n")
    # stats
    from collections import Counter
    c = Counter(LABELS[int(r.Verdict)] for r in rows)
    L = sorted(len(str(r.Text).strip()) for r in rows)
    print("rows", len(rows), "pool sizes", {LABELS[k]: len(v) for k, v in pools.items()})
    print("labels", dict(c))
    print("soft coverage 0/%d" % len(rows))
    print("len min/median/mean/max", L[0], L[len(L) // 2], round(sum(L) / len(L)), L[-1])


if __name__ == "__main__":
    main()
