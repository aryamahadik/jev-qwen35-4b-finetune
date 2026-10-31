"""Build golden rows for opentdb (Open Trivia Database: user-contributed, moderator-verified multiple-choice trivia).

Source : opentdb.com API snapshot made by fetch_opentdb.py on 29 Sep 2026 (every verified type=multiple question the
         API serves, all 24 categories, session token so no repeats), cache/opentdb/opentdb_multiple.json, sha256
         pinned below. A question database has no splits -> train.
Licence: CC BY-SA 4.0, stated on the official API page https://opentdb.com/api_config.php: 'All data provided by the
         API is available under the Creative Commons Attribution-ShareAlike 4.0 International License.'
Texts  : questions, correct answers and three wrong answers written by human contributors and verified by the site's
         moderators (the API serves only verified questions).
Rows   : state = category + the question; options = the correct answer and the three wrong answers in a fixed
         pseudo-random order (seeded by the question text, so the gold position is balanced); per-row definitions
         (defs/opentdb__<qid>.json).
Drops  : time-sensitive questions (current / currently / as of / latest / most recent / this year / recently / today /
         newest / upcoming / still), questions that refer to a picture, rows with duplicate or overlong choices,
         near-duplicate questions (word 3-gram Jaccard >= 0.9); caps: Video Games 300 and Japanese Anime & Manga 150
         rows (so general knowledge, science, geography and history are not swamped); decontamination vs forbidden
         label-NLI, local train/dev/eval files, round-1 golden parts and JevBench public.
Edge   : negation, quantifier, temporal (year/date questions or choices), units, numeric.
Deterministic (seed 20261207).
"""
import collections
import hashlib
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAMILY, HERE, MAX_OPT_WORDS, UNITS, append_manifest, clean, decon, has_negation,  # noqa: E402
                     is_all, is_none, letter_refs, near_dup_filter, norm, option_defs, qid_of, sha256, show_samples,
                     summary, write_outputs)

KEY = "opentdb"
SEED = 20261207
SNAP = HERE / "cache" / "opentdb" / "opentdb_multiple.json"
PINNED_SHA = "74779327cbec4f4113bb80c0eac9a134f5db2125c203b92089994d37fa6bd2b7"  # snapshot of 29 Sep 2026 (4,510 questions)
LICENCE = ("CC BY-SA 4.0 (official API page https://opentdb.com/api_config.php: 'All data provided by the API is "
           "available under the Creative Commons Attribution-ShareAlike 4.0 International License.')")
INSTR = "Which answer choice correctly answers this trivia question?"
CAPS = {"Entertainment: Video Games": 300, "Entertainment: Japanese Anime & Manga": 150}
STALE = re.compile(r"(?i)\b(current|currently|as of|latest|most recent|this year|recently|today|nowadays|newest|"
                   r"upcoming|still|so far|to date|at the moment|right now|presently)\b")
PIC = re.compile(r"(?i)\b(picture|pictured|image|shown|photo)\b")


def edge_of(q, options):
    if has_negation(q):
        return "negation"
    if any(is_all(o) or is_none(o) for o in options):
        return "quantifier"
    text = q + " " + " ".join(options)
    if re.search(r"(?i)\b(what|which|in what) year\b|\bwhen\b|\bcentury\b|\bdecade\b", q) or all(
            re.fullmatch(r"\d{3,4}( (BC|AD|BCE|CE))?", o) for o in options):
        return "temporal"
    if UNITS.search(text):
        return "units"
    if re.search(r"\d", text):
        return "numeric"
    return None


def main():
    if sha256(SNAP) != PINNED_SHA:
        sys.exit(f"snapshot sha256 {sha256(SNAP)} != pinned {PINNED_SHA}")
    data = json.loads(SNAP.read_text())
    stats = collections.Counter()
    recs = []
    for i, r in enumerate(data):
        q = clean(r["question"])
        opts = [clean(r["correct_answer"])] + [clean(x) for x in r["incorrect_answers"]]
        if len(opts) != 4 or not all(opts) or len({norm(o) for o in opts}) < 4 or not norm(q):
            stats["bad_choices"] += 1
            continue
        if max(len(o.split()) for o in opts) > MAX_OPT_WORDS or any(letter_refs(o, 4) for o in opts):
            stats["long_or_letter_choice"] += 1
            continue
        if STALE.search(q) or PIC.search(q):
            stats["time_sensitive_or_picture"] += 1
            continue
        rid = "otdb_" + hashlib.sha1((r["category"] + "|" + q).encode()).hexdigest()[:12]
        rng = random.Random(f"{SEED}:{rid}")
        order = opts[:]
        rng.shuffle(order)
        recs.append({"rid": rid, "cat": r["category"], "diff": r["difficulty"], "q": q, "options": order,
                     "gold": opts[0]})
    print(f"snapshot={len(data)} usable={len(recs)} drops={dict(stats)}")
    recs = near_dup_filter(recs, lambda r: r["q"], thresh=0.9, strip_numbers=False)
    print(f"after near-dup: {len(recs)}")
    hits = decon({r["rid"]: [r["q"]] for r in recs})
    recs = [r for r in recs if r["rid"] not in hits]
    print(f"after decon: {len(recs)}")
    rng = random.Random(SEED)
    by = collections.defaultdict(list)
    for r in recs:
        by[r["cat"]].append(r)
    chosen = []
    for c in sorted(by):
        pool = by[c]
        rng.shuffle(pool)
        chosen += pool[:CAPS.get(c, len(pool))]
    print("categories:", dict(collections.Counter(r["cat"] for r in chosen)))

    rows, defs = [], {}
    for r in chosen:
        q = qid_of(r["rid"])
        defs[q] = option_defs(r["q"], r["options"], kind="exam")
        rows.append({
            "key": KEY, "rid": r["rid"], "state": f"Trivia question (category: {r['cat']}).\n\nQuestion: {r['q']}",
            "instructions": INSTR, "options": r["options"], "gold": r["gold"], "soft": None,
            "meta": {"dataset": "Open Trivia Database (opentdb.com), verified multiple-choice questions",
                     "config": f"category {r['cat']}; difficulty {r['diff']}; 4-way answer choice",
                     "revision": f"API snapshot 2026-09-29; sha256:{PINNED_SHA}", "licence": LICENCE,
                     "split": "train", "orig_label": {"correct_answer": r["gold"]}, "family": FAMILY,
                     "edge": edge_of(r["q"], r["options"]), "defs": q, "seed": SEED}})
    rng.shuffle(rows)
    write_outputs(KEY, rows, defs)
    s = summary(KEY, rows)
    show_samples(rows, defs, n=5, seed=4)
    append_manifest({
        "key": KEY, "family": FAMILY, "dataset": "Open Trivia Database (opentdb.com) verified multiple-choice questions",
        "licence": LICENCE, "rows": len(rows), "qtype": "choice (4 answer choices; per-row option definitions)",
        "yesno_share": 0.0, "edge_tags": sorted(k for k in s["edges"] if k),
        "notes": ("human-written, moderator-verified trivia over 24 categories (general knowledge, science, geography, "
                  "history, arts, sport, entertainment); wrong answers are human-written near misses; time-sensitive "
                  "and picture questions dropped; video-game and anime categories capped; choice order seeded per "
                  f"question; gold position {dict(sorted(s['pos'].items()))}.")})


if __name__ == "__main__":
    main()
