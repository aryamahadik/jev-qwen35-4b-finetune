"""Build raw rows for NewsMTSC (target-dependent sentiment in political news).

Source: GitHub fhamborg/NewsMTSC @ 6b838e00f54423c253806327a0ae24dbffa24c9e,
        NewsSentiment/experiments/default/datasets/newsmtsc-rw-hf/train.jsonl (TRAIN split only).
Licence: MIT (repo LICENSE file, "Copyright 2020 Felix Hamborg"; also the HF card fhamborg/news_sentiment_newsmtsc).
Texts: human-written news sentences (AllSides / POLUSA); labels: crowdworker (MTurk) majority, human.
Snapshot saved under breadth_src/cache/newsmtsc/ (train.jsonl, LICENSE, dataset_readme.md).

Design:
- One row per source record (= one target mention in one sentence); question names the mention.
- Sentences with two or more targets of DIFFERENT polarity are kept together as contrast groups
  (all targets of the sentence are selected, so the model sees the same text with different answers).
- Label balance by round-robin over labels (cap 40% per label); contrast groups are taken first up to
  ~45% of the budget, singles fill the rest.
- Filters: 15-4000 chars, no multi-line scraped boilerplate, no lowercase/space start, long texts must end in
  final punctuation (truncation guard), mention must sit at [from:to] and occur exactly once in the sentence
  (so the question is unambiguous), conflicting duplicate (sentence, mention) records dropped.
- Dedup vs MN-DS / Sarcasm headlines raw files if they already exist (normalised exact match, or containment when the
  shorter text has >= 40 chars).
- Date/time mentions (Monday, last week, ...) and clause-length mentions (>10 words) dropped (extraction errors);
  sentences ending in a title abbreviation ("... by Sen.", split error = truncated) dropped;
  sentences starting with an all-caps genre tag ("ANALYSIS/OPINION:") dropped.
- Pronoun mentions (he/she/him/myself/...) get the question 'toward the person or group referred to as "he"'.
"""
import json, os, random, re, sys, hashlib, collections

SEED = 20261101
N_MAX = 550
CAP_FRAC = 0.40
CONTRAST_FRAC = 0.45
REV = "6b838e00f54423c253806327a0ae24dbffa24c9e"
URL = ("https://raw.githubusercontent.com/fhamborg/NewsMTSC/" + REV +
       "/NewsSentiment/experiments/default/datasets/newsmtsc-rw-hf/train.jsonl")

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "cache", "newsmtsc")
RAW = os.path.join(CACHE, "train.jsonl")
OUT = os.path.join(LEAN, "data", "v13_parts", "raw", "newsmtsc.jsonl")
DEDUP_FILES = [os.path.join(LEAN, "data", "v13_parts", "raw", f)
               for f in ("mnds.jsonl", "sarcasm_headlines.jsonl")]

LABELS = {-1: "negative", 0: "neutral", 1: "positive"}
OPTIONS = ["negative", "neutral", "positive"]
META_BASE = {"dataset": "fhamborg/NewsMTSC (newsmtsc-rw-hf)", "config": "newsmtsc-rw-hf",
             "revision": REV,
             "licence": "MIT (github.com/fhamborg/NewsMTSC LICENSE; HF card fhamborg/news_sentiment_newsmtsc)",
             "split": "train"}


def norm(s):
    return re.sub(r"\s+", " ", s.lower()).strip()


def dnorm(s):
    """Dedup normaliser: lowercase alphanumerics only (sarcasm headlines are lowercased, unpunctuated)."""
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


DEDUP_MIN = 40  # containment only counts when the shorter text has >= 40 chars (avoids e.g. "moving forward.")


def dup_of(a, b):
    if a == b:
        return True
    short, long_ = (a, b) if len(a) <= len(b) else (b, a)
    return len(short) >= DEDUP_MIN and short in long_


PRONOUNS = {"he", "she", "him", "her", "his", "hers", "they", "them", "their", "theirs", "it", "its", "we", "us", "our",
            "i", "me", "my", "you", "your", "himself", "herself", "themselves", "itself", "myself", "ourselves",
            "yourself"}
# automatic target extraction sometimes picked dates/times, which are not sentiment targets
TIME_MENTION = re.compile(r"(?i)^(?:(?:last|this|next|on)\s+)?(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
                          r"today|yesterday|tomorrow|tonight|week|weekend|month|year|night|morning|evening|afternoon)$")
MAX_MENTION_WORDS = 10  # longer "mentions" are extraction errors (whole clauses)
# sentence splitter cut after a title abbreviation ("... legislation championed by Sen.") -> truncated
ABBR_END = re.compile(r"\b(?:Sens?|Reps?|Gov|Mr|Mrs|Ms|Dr|St|Lt|Gen|Col|Sgt|Capt|Rev|Prof|Pres|Sec|Atty|No)\.\s*$")
TAG_PREFIX = re.compile(r"^[A-Z][A-Z/ ]{3,}:\s")  # e.g. "ANALYSIS/OPINION: " genre tags glued to the sentence


def load():
    if not os.path.exists(RAW):
        import urllib.request
        os.makedirs(CACHE, exist_ok=True)
        urllib.request.urlretrieve(URL, RAW)
    with open(RAW, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def load_dedup_texts():
    texts, used = [], []
    for p in DEDUP_FILES:
        if os.path.exists(p):
            used.append(os.path.basename(p))
            with open(p, encoding="utf-8") as f:
                for l in f:
                    if l.strip():
                        texts.append(dnorm(json.loads(l).get("state", "")))
    return texts, used


def main():
    rng = random.Random(SEED)
    recs = load()
    ext_texts, ext_used = load_dedup_texts()
    drop = collections.Counter()

    # clean + group by sentence
    by_sent = collections.OrderedDict()
    seen_pair = {}
    for r in recs:
        s, m = r["sentence"], r["mention"]
        if not (15 <= len(s) <= 4000):
            drop["length"] += 1; continue
        if "\n" in s or "\r" in s:
            drop["multiline_boilerplate"] += 1; continue  # scraped captions/teasers glued to the sentence
        if s[:1].isspace() or s.lstrip()[:1].islower():
            drop["starts_mid_sentence"] += 1; continue
        if len(s) > 100 and s.rstrip()[-1] not in '.?!"\u201d\u2019\')':
            drop["no_final_punct_long"] += 1; continue  # likely truncated (short headlines are kept)
        if ABBR_END.search(s):
            drop["cut_at_abbreviation"] += 1; continue
        if s[r["from"]:r["to"]] != m or s.count(m) != 1 or not m.strip():
            drop["mention_ambiguous"] += 1; continue
        if TIME_MENTION.match(m.strip()) or len(m.split()) > MAX_MENTION_WORDS:
            drop["mention_not_target"] += 1; continue
        if TAG_PREFIX.match(s):
            drop["genre_tag_prefix"] += 1; continue
        key = (norm(s), m)
        if key in seen_pair:
            if seen_pair[key] != r["polarity"]:
                seen_pair[key] = None  # conflict marker
            drop["dup_pair"] += 1; continue
        seen_pair[key] = r["polarity"]
        by_sent.setdefault(norm(s), []).append(r)
    # remove conflicting pairs
    for k in list(by_sent):
        by_sent[k] = [r for r in by_sent[k] if seen_pair[(k, r["mention"])] is not None]
        if not by_sent[k]:
            del by_sent[k]
    # dedup vs other v13 news sources
    if ext_texts:
        for k in list(by_sent):
            dk = dnorm(k)
            if any(dup_of(dk, t) for t in ext_texts if t):
                drop["dedup_ext"] += len(by_sent[k]); del by_sent[k]

    keys = sorted(by_sent)
    rng.shuffle(keys)
    contrast = [k for k in keys if len(by_sent[k]) >= 2 and len({r["polarity"] for r in by_sent[k]}) >= 2]
    contrast_set = set(contrast)
    singles_pool = collections.defaultdict(list)
    for k in keys:
        if k in contrast_set:
            continue
        for r in by_sent[k]:
            singles_pool[r["polarity"]].append(r)

    cap = int(N_MAX * CAP_FRAC)
    counts = collections.Counter()
    chosen, chosen_sent = [], set()

    # 1) contrast groups (whole sentence, all targets), keep labels under the balanced share
    share = N_MAX / len(LABELS)
    budget_c = int(N_MAX * CONTRAST_FRAC)
    for k in contrast:
        grp = sorted(by_sent[k], key=lambda r: r["from"])
        if len(grp) > 3:
            continue
        if len(chosen) + len(grp) > budget_c:
            continue
        add = collections.Counter(r["polarity"] for r in grp)
        if any(counts[p] + c > share for p, c in add.items()):
            continue
        chosen.extend((r, "contrast", k) for r in grp)
        counts.update(add)
        chosen_sent.add(k)

    # 2) singles: round-robin over labels, always topping up the least-filled label (one target per sentence)
    idx = {p: 0 for p in LABELS}
    exhausted = set()
    while len(chosen) < N_MAX and len(exhausted) < len(LABELS):
        p = min((q for q in LABELS if q not in exhausted), key=lambda q: (counts[q], q))
        pool = singles_pool[p]
        while idx[p] < len(pool) and norm(pool[idx[p]]["sentence"]) in chosen_sent:
            idx[p] += 1
        if idx[p] >= len(pool) or counts[p] >= cap:
            exhausted.add(p); continue
        r = pool[idx[p]]; idx[p] += 1
        k = norm(r["sentence"])
        chosen.append((r, "single", k)); chosen_sent.add(k); counts[p] += 1

    # emit: shuffle groups but keep contrast pairs adjacent
    groups = collections.OrderedDict()
    for r, kind, k in chosen:
        groups.setdefault(k, []).append((r, kind))
    order = list(groups); rng.shuffle(order)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    rows = []
    for k in order:
        for r, kind in groups[k]:
            meta = dict(META_BASE)
            meta.update({"orig_label": r["polarity"], "mention": r["mention"],
                         "char_span": [r["from"], r["to"]], "contrast_group": kind == "contrast",
                         "sentence_group": hashlib.sha1(k.encode()).hexdigest()[:12],
                         "dedup_checked_against": ext_used})
            rows.append({
                "key": "newsmtsc",
                "rid": r["id"],
                "state": r["sentence"],
                "instructions": (f'What sentiment does this news sentence express toward the person or group referred to as "{r["mention"]}"?'
                                 if r["mention"].strip().lower() in PRONOUNS else
                                 f'What sentiment does this news sentence express toward "{r["mention"]}"?'),
                "options": OPTIONS,
                "gold": LABELS[r["polarity"]],
                "soft": None,
                "meta": meta,
            })
    with open(OUT, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # report
    lab = collections.Counter(r["gold"] for r in rows)
    L = sorted(len(r["state"]) for r in rows)
    print("source records:", len(recs), "dropped:", dict(drop), "dedup files:", ext_used or "none present")
    print("rows:", len(rows), "labels:", dict(lab), "max share: %.3f" % (max(lab.values()) / len(rows)))
    print("contrast rows:", sum(r["meta"]["contrast_group"] for r in rows),
          "contrast sentences:", len({r["meta"]["sentence_group"] for r in rows if r["meta"]["contrast_group"]}))
    print("soft coverage: 0/%d (train file has only majority polarity)" % len(rows))
    print("len chars min/median/mean/max: %d/%d/%.0f/%d" % (L[0], L[len(L) // 2], sum(L) / len(L), L[-1]))
    print("unique rids:", len({r["rid"] for r in rows}))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
