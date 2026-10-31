"""Build raw rows for vader_intensity: how positive or negative is this text, on a 5-level intensity scale, as
judged by 20-100 independent human raters?

Source : Hutto & Gilbert (ICWSM 2014) VADER ground-truth ratings, GitHub cjhutto/vaderSentiment,
         additional_resources/hutto_ICWSM_2014.tar.gz at commit 44fc044cd877310ee8278a0eadf34bcd50d41d06
         (sha256 pinned). Files used: tweets_*, nytEditorialSnippets_* (GroundTruth = texts, anonDataRatings = every
         rater's rating). The movie-review snippets are NOT used (they are Pang & Lee Rotten Tomatoes texts;
         rotten_tomatoes is a forbidden dev / label-NLI source), and the Amazon review snippets are NOT used (review
         fix: their reviews also appear in amazon_polarity, a forbidden label-NLI task).
Licence: MIT (repo LICENSE.txt at the pinned commit, 'Copyright (c) 2016 C.J. Hutto'; README: 'fully open-sourced
         under the MIT License'); the ratings archive is part of the licensed repository.
Texts  : tweet-like texts (4,000 public tweets with usernames/URLs anonymised + 200 author-written test sentences) and
         5,190 sentences from 500 NYT opinion articles.
Labels : every rater's -4..+4 sentiment rating (>= 20 pre-screened raters per text; ~95 for tweets), mapped per rater
         to 5 ordered levels: <= -3 very negative, -2..-1 somewhat negative, 0 neutral, +1..+2 somewhat positive,
         >= +3 very positive. soft = the raters' shares over the 5 levels; gold = the plurality level, kept only when
         it also contains the median rating and holds >= 50% of the raters.
Filters: >= 4 words; exact + near-exact dedupe (the 200 contrived minimal pairs collapse); decontamination.
Balance: up to 700 rows per level (all 'very negative').
Deterministic (seed 20261101); CPU only; no model calls.
"""
import collections
import random
import statistics
import sys
import tarfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ord_common as C  # noqa: E402

KEY = "vader_intensity"
SEED = C.SEED
CACHE = C.CACHE / KEY
COMMIT = "44fc044cd877310ee8278a0eadf34bcd50d41d06"
BASE = f"https://raw.githubusercontent.com/cjhutto/vaderSentiment/{COMMIT}/"
FILES = {
    "additional_resources/hutto_ICWSM_2014.tar.gz": "d5bb07d87474b3eb8d30b4deccbc23f19d742a6c5718fbacc65485b70b95c5fa",
    "LICENSE.txt": "b78925304c567623f14677bad66b8e305e7ddcaf7982c8d8411ce51c55a8bf51",
}
LICENCE = (f"MIT (https://github.com/cjhutto/vaderSentiment/blob/{COMMIT}/LICENSE.txt, 'Copyright (c) 2016 C.J. "
           f"Hutto'; README.rst: 'fully open-sourced under the MIT License')")
DATASET = "VADER ground-truth sentiment ratings (Hutto & Gilbert 2014), cjhutto/vaderSentiment hutto_ICWSM_2014"
SOURCES = {
    "tweets": "Tweet",
    "nytEditorialSnippets": "Sentence from a New York Times opinion article",
    # "amazonReviewSnippets" REMOVED in review (29 Sep 2026): Hu & Liu's 2004 Amazon reviews are also in
    # fancyzhx/amazon_polarity (forbidden label-NLI task amazon_polarity/amazon_polarity; used train source):
    # 83 of the 1,188 selected Amazon sentences shared a 12-word run with an amazon_polarity review (e.g. the
    # Apex DVD-player review 71_*), so the whole Amazon source is dropped (sharing-texts rule).
}
PER_LEVEL = 700
QUESTION = ("How positive or negative is the sentiment this text expresses, as a typical reader would rate its "
            "intensity?")
LEVELS = ["very negative", "somewhat negative", "neutral", "somewhat positive", "very positive"]
DEFS = {
    "very negative": "Strongly or extremely negative (rated -3 or -4 on a -4..+4 scale): intense anger, disgust, "
                     "despair, harsh criticism or insults, often intensified by boosters, capitals or exclamation "
                     "marks.",
    "somewhat negative": "Mildly to moderately negative (rated -1 or -2): a clear but restrained complaint, worry, "
                         "disappointment or criticism, or negativity softened by hedges or offset by minor "
                         "positives.",
    "neutral": "No net sentiment (rated 0): factual, descriptive or procedural text, questions without evaluative "
               "tone, or positives and negatives that cancel out.",
    "somewhat positive": "Mildly to moderately positive (rated +1 or +2): clear but restrained approval, "
                         "satisfaction, hope or praise, or positivity softened by hedges ('kind of good') or mixed "
                         "with minor negatives.",
    "very positive": "Strongly or extremely positive (rated +3 or +4): intense enthusiasm, delight, love or "
                     "superlative praise, often with boosters, capitals, exclamation marks or emoticons.",
}


def level(r):
    return 0 if r <= -3 else 1 if r <= -1 else 2 if r == 0 else 3 if r <= 2 else 4


def read_tsv(tf, name):
    m = tf.extractfile(f"hutto_ICWSM_2014/{name}")
    out = []
    for line in m.read().decode("utf-8-sig", errors="strict").splitlines():
        p = line.rstrip("\r\n").split("\t")
        if len(p) >= 3:
            out.append(p)
    return out


def main():
    paths = {rel: C.fetch(BASE + rel, CACHE / Path(rel).name, sha) for rel, sha in FILES.items()}
    stats = collections.Counter()
    recs = []
    with tarfile.open(paths["additional_resources/hutto_ICWSM_2014.tar.gz"]) as tf:
        for src, label in SOURCES.items():
            texts = {p[0].strip(): p[2] for p in read_tsv(tf, f"{src}_GroundTruth.txt")}
            for p in read_tsv(tf, f"{src}_anonDataRatings.txt"):
                rid = p[0].strip()
                ratings = [int(x) for x in p[3].strip("[] ").split(",") if x.strip()]
                stats[f"{src}_records"] += 1
                if rid not in texts or len(ratings) < 20:
                    stats["drop_missing"] += 1
                    continue
                text = C.clean(texts[rid])
                if len(C.words(text)) < 4:
                    stats["drop_short"] += 1
                    continue
                cnt = collections.Counter(level(r) for r in ratings)
                top, tc = cnt.most_common(1)[0]
                if sum(1 for v in cnt.values() if v == tc) > 1:
                    stats["drop_tied_plurality"] += 1
                    continue
                med = level(int(statistics.median_low(ratings)))
                if med != top or tc / len(ratings) < 0.5:
                    stats["drop_unclear_plurality"] += 1
                    continue
                soft = C.fix_soft({LEVELS[i]: cnt.get(i, 0) / len(ratings) for i in range(5)})
                recs.append({"rid": f"vader-{src}-{rid}", "src": src, "text": text,
                             "state": f"{label}: {text}", "gold": LEVELS[top], "soft": soft, "n": len(ratings),
                             "mean": round(statistics.mean(ratings), 3), "ratings": ratings})
    stats["candidates"] = len(recs)
    rng = random.Random(SEED)
    recs.sort(key=lambda x: x["rid"])
    rng.shuffle(recs)
    nd = C.NearDup(thr=0.6)
    uniq = []
    for x in recs:
        if nd.seen(x["text"]):
            stats["drop_near_dup"] += 1
            continue
        uniq.append(x)
    hits = C.decon({x["rid"]: [x["text"]] for x in uniq}, KEY)
    hits.update(C.cross_v14({x["rid"]: [x["text"]] for x in uniq}, {KEY}))
    stats["drop_decon"] = len(hits)
    per = collections.defaultdict(list)
    for x in uniq:
        if x["rid"] not in hits:
            per[x["gold"]].append(x)
    chosen = []
    for lev in LEVELS:  # within a level, interleave the three sources so no genre dominates
        by_src = collections.defaultdict(list)
        for x in per[lev]:
            by_src[x["src"]].append(x)
        order = sorted(by_src)
        i = 0
        picked = []
        while len(picked) < PER_LEVEL and any(by_src[s] for s in order):
            s = order[i % len(order)]
            if by_src[s]:
                picked.append(by_src[s].pop())
            i += 1
        chosen += picked
    rows = []
    for x in chosen:
        edge = []
        if C.neg_count(x["text"]) >= 1:
            edge.append("negation")
        if C.HYPO.search(x["text"]):
            edge.append("hypothetical")
        if x["soft"][x["gold"]] < 0.6:
            edge.append("ambiguous")
        rows.append({
            "key": KEY, "rid": x["rid"], "state": x["state"], "instructions": QUESTION, "options": LEVELS,
            "gold": x["gold"], "soft": x["soft"],
            "meta": {"dataset": DATASET, "config": f"{x['src']}; 9-point ratings grouped into 5 levels per rater",
                     "revision": f"git:{COMMIT}; sha256:{FILES['additional_resources/hutto_ICWSM_2014.tar.gz']}",
                     "licence": LICENCE, "split": "train",
                     "orig_label": {"mean_rating": x["mean"], "n_raters": x["n"],
                                    "ratings": x["ratings"] if x["n"] <= 30 else None},
                     "family": C.FAMILY, "edge": C.edge_join(edge), "seed": SEED},
        })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {None: DEFS})
    print(dict(stats))
    print("by source:", dict(collections.Counter(r["meta"]["config"].split(";")[0] for r in rows)))
    st = C.summary(KEY, rows)
    C.show_samples(rows, n=5, seed=9)
    rec = C.manifest_record(
        KEY, DATASET, LICENCE, rows, "choice (5-level ordinal sentiment intensity, soft labels)",
        "Tweets and NYT opinion sentences with >= 20 raters each (-4..+4); per-rater ratings "
        "grouped into 5 levels, soft = rater shares, gold = plurality level that also holds the median and >= 50% "
        "of raters; movie (Rotten Tomatoes) and Amazon review snippets excluded (shared texts with forbidden "
        "rotten_tomatoes / amazon_polarity); up to 700 per level, sources interleaved.", st)
    return rows, rec


if __name__ == "__main__":
    rows, rec = main()
    if "--manifest" in sys.argv:
        C.append_manifest(rec)
        print("manifest record appended")
