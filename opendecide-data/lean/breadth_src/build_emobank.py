"""Build raw rows for EmoBank (valence / arousal / dominance), TRAIN split only.

Source: GitHub JULIELab/EmoBank, pinned commit 248ce2a43e165a66d31aeaed83cff9641d6654e0.
Raw snapshot saved in breadth_src/cache/emobank/ (emobank.csv, meta.tsv, individual_*_ratings.csv,
README.md). Licence: CC BY-SA 4.0, stated in the repo README.md ("## License").

Rules:
- drop boilerplate/metadata lines (emails, URLs, timestamps, postal addresses, date-only lines,
  signatures, editor notes) and near-duplicates (a text contained in an already-selected text);
- rows with split == 'train' in corpus/emobank.csv only (dev/test never read into output);
- drop SemEval items (id contains 'SemEval' or meta category == 'SemEval');
- pilot/ folder (incl. movie-review) never used;
- one row per source record; each record is assigned to at most one dimension;
- gold = side of the combined (reader+writer) mean in emobank.csv, kept only for clear extremes
  (V <= 2.5 / >= 3.5; A and D <= 2.6 / >= 3.4) AND rater agreement (soft prob of gold >= 0.7);
- soft = pooled individual reader+writer ratings (after the official (1,1,1) spam filter):
  P(high) = (#ratings > 3 + 0.5 * #ratings == 3) / N.
"""
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

SEED = 20261101
REV = "248ce2a43e165a66d31aeaed83cff9641d6654e0"
LICENCE = "CC BY-SA 4.0 (stated in README.md 'License' section of JULIELab/EmoBank)"
HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache" / "emobank"
OUT = HERE.parent / "data" / "v13_parts" / "raw" / "emobank.jsonl"
MAX_ROWS = 600

DIMS = {
    # dim: (column, low option, high option, low thr, high thr, question)
    "valence": ("V", "negative", "positive", 2.5, 3.5,
                "Is the feeling conveyed by this text negative or positive?"),
    "arousal": ("A", "calm", "excited", 2.6, 3.4,
                "How emotionally aroused is this text: calm or excited?"),
    "dominance": ("D", "controlled", "in control", 2.6, 3.4,
                  "Does this text convey a sense of being controlled or of being in control?"),
}
MIN_AGREE = 0.7


def norm(t):
    return re.sub(r"\W+", " ", t.lower()).strip()


# boilerplate / metadata lines (addresses, dates, blog timestamps, bylines, emails, signatures,
# editor notes): rated mostly as "calm" by raters, carry no affect content and some carry PII.
_JUNK = [
    re.compile(r"\S+@\S+|https?://|www\.", re.I),                  # email / URL
    re.compile(r"\b\d{1,2}:\d{2}\s*(AM|PM)\b", re.I),               # blog/comment timestamps
    re.compile(r"\b\d{5}-\d{4}\b|\b[A-Z]{2},?\s+\d{5}\b"),         # US postal addresses
    re.compile(r"ATTENTION EDITORS", re.I),                        # newswire editor notes
    re.compile(r"^\W*(Posted by|Comments \(\d+\))", re.I),           # blog metadata
    re.compile(r"^\W*(January|February|March|April|May|June|July|August|September|October|"
               r"November|December)\s+\d{1,2},\s+\d{4}\W*$"),        # date-only line
]


def is_junk(t):
    if any(p.search(t) for p in _JUNK):
        return True
    words = re.findall(r"[A-Za-z][A-Za-z'’-]*", t)
    # title-cased signature/letterhead line with no sentence punctuation (not ALL-CAPS headlines)
    if (words and all(w[0].isupper() for w in words) and not t.isupper()
            and not re.search(r"[.!?,;:\"”]\s*$", t.strip()) and len(words) <= 12):
        return True
    return False


def main():
    rng = random.Random(SEED)
    eb = pd.read_csv(CACHE / "emobank.csv", keep_default_na=False, dtype={"text": str})
    meta = pd.read_csv(CACHE / "meta.tsv", sep="\t", keep_default_na=False)
    eb = eb[eb.split == "train"].merge(meta[["id", "category"]], on="id", how="left")
    eb = eb[(eb.category != "SemEval") & (~eb.id.str.contains("SemEval"))]

    ind = pd.concat([pd.read_csv(CACHE / "individual_reader_ratings.csv"),
                     pd.read_csv(CACHE / "individual_writer_ratings.csv")])
    ind = ind.query("not (V == 1 and A == 1 and D == 1)")  # official spam filter (aggregation.ipynb)
    ind = ind[ind.id.isin(set(eb.id))]
    ratings = {k: g for k, g in ind.groupby("id")}

    # length filter + dedup (keep first by id order)
    seen, recs = set(), []
    for r in eb.sort_values("id").itertuples(index=False):
        t = r.text
        if not (15 <= len(t.strip()) <= 4000):
            continue
        k = norm(t)
        if len(k.split()) < 3 or k in seen or is_junk(t):
            continue
        seen.add(k)
        recs.append(r)

    # candidates per (dim, label)
    cands = defaultdict(list)
    for r in recs:
        g = ratings.get(r.id)
        if g is None or len(g) < 4:
            continue
        for dim, (col, lo, hi, tlo, thi, _) in DIMS.items():
            v = float(getattr(r, col))
            vals = g[col].tolist()
            p_hi = (sum(x > 3 for x in vals) + 0.5 * sum(x == 3 for x in vals)) / len(vals)
            if v <= tlo and 1 - p_hi >= MIN_AGREE:
                gold = lo
            elif v >= thi and p_hi >= MIN_AGREE:
                gold = hi
            else:
                continue
            soft = {lo: round(1 - p_hi, 4), hi: round(p_hi, 4)}
            cands[(dim, gold)].append((r, soft, v, len(vals)))

    # genre-interleaved queues per (dim,label), clearest items popped first (pop() takes the end)
    queues = {}
    for key in sorted(cands):
        byg = defaultdict(list)
        for c in cands[key]:
            byg[c[0].category].append(c)
        for gname in byg:
            # clearest first: rater agreement on gold, then distance of the mean from the midpoint 3
            byg[gname].sort(key=lambda c: c[0].id)
            rng.shuffle(byg[gname])
            byg[gname].sort(key=lambda c: (max(c[1].values()), abs(c[2] - 3.0)))
        order = sorted(byg)
        q, i = [], 0
        while any(byg.values()):
            gname = order[i % len(order)]
            if byg[gname]:
                q.append(byg[gname].pop())
            i += 1
        queues[key] = q

    # round-robin over the 6 labels, scarcest first; a record is used once
    keys = sorted(queues, key=lambda k: (len(queues[k]), k))
    used, used_norm, rows = set(), [], []
    counts = Counter()
    while len(rows) < MAX_ROWS and any(queues[k] for k in keys):
        for key in keys:
            if len(rows) >= MAX_ROWS:
                break
            q = queues[key]
            # skip used records and near-duplicates (one text contained in an already-used text)
            while q and (q[0][0].id in used or any(
                    (nk := f" {norm(q[0][0].text)} ") in u or u in nk for u in used_norm)):
                q.pop(0)
            if not q:
                continue
            r, soft, v, n = q.pop(0)
            used.add(r.id)
            used_norm.append(f" {norm(r.text)} ")
            dim, gold = key
            col, lo, hi, _, _, question = DIMS[dim]
            rows.append({
                "key": "emobank",
                "rid": r.id,
                "state": r.text,
                "instructions": question,
                "options": [lo, hi],
                "gold": gold,
                "soft": soft,
                "meta": {"dataset": "JULIELab/EmoBank", "config": f"corpus/emobank.csv:{dim}",
                         "revision": REV, "licence": LICENCE, "split": "train",
                         "orig_label": {col: v, "n_ratings": n, "genre": r.category}},
            })
            counts[key] += 1

    rng.shuffle(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print("wrote", len(rows), "->", OUT)
    print("candidates:", {f"{d}/{l}": len(v) for (d, l), v in sorted(cands.items())})
    print("counts:", {f"{d}/{l}": c for (d, l), c in sorted(counts.items())})
    gl = Counter(r["gold"] for r in rows)
    print("max label share: %.3f" % (max(gl.values()) / len(rows)))
    print("soft coverage:", sum(r["soft"] is not None for r in rows), "/", len(rows))
    print("genres:", dict(Counter(r["meta"]["orig_label"]["genre"] for r in rows)))
    L = sorted(len(r["state"]) for r in rows)
    print("len min/median/mean/max:", L[0], L[len(L) // 2], round(sum(L) / len(L)), L[-1])
    print("mean soft prob of gold: %.3f" % (sum(r["soft"][r["gold"]] for r in rows) / len(rows)))


if __name__ == "__main__":
    main()
