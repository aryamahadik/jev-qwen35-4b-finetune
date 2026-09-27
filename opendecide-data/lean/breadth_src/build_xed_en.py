"""Build raw rows for breadth set "xed_en" (XED English, emotion-annotated movie subtitles).

Source: Helsinki-NLP/XED, pinned commit 76666d25 (raw snapshot saved in breadth_src/cache/xed_en/):
  AnnotatedData/en-annotated.tsv  (human multi-label Plutchik annotations, "text\\t1, 4")
  AnnotatedData/neu_en.txt        (human neutral annotations, "9\\ttext")
Licence: CC BY 4.0, stated at the end of the XED README.md (cache/xed_en/README.md).
XED has no official split; the whole English annotated release counts as train. Never the fi/projected files.

Rows:
  - single-label lines -> 8-way choice (Plutchik 8), round-robin over labels. Neutral is NOT offered: neu_en.txt
    has different preprocessing (no NER [PERSON] masking, untokenised punctuation, commas stripped), so every
    neutral line was identifiable from surface form alone (verifier fix). neu_en.txt is still loaded, only so
    that texts labelled both neutral and emotional are dropped as conflicting.
  - annotated texts are lightly detokenised (" ." -> ".", " ?" -> "?", etc.) so they read like normal text
  - multi-label lines -> yes/no label verification only ("Does this line express X?"): yes = an annotated
    emotion, no = an emotion none of the annotators chose
Filters: >= 4 words, 15-4000 chars, dedup (normalised text; texts with conflicting files dropped),
13-gram decontamination + exact-state match against our train/dev/eval files and JevBench public
(never the ohs* files). Deterministic, seed 20261101.

  python breadth_src/build_xed_en.py
"""
import collections
import glob
import hashlib
import json
import random
import re
import statistics
import urllib.request
from pathlib import Path

SEED = 20261101
KEY = "xed_en"
REV = "76666d251f147cf518071bef4f8415dab6b96115"
RAW = f"https://raw.githubusercontent.com/Helsinki-NLP/XED/{REV}/"
FILES = {"en-annotated.tsv": "AnnotatedData/en-annotated.tsv", "neu_en.txt": "AnnotatedData/neu_en.txt",
         "README.md": "README.md"}
SHA = {"en-annotated.tsv": "26ac0254fbdb8b09cf2b00d44041d9084ece31bd200ae7c0e0662fbd8b037d98",
       "neu_en.txt": "6e8b38af83b80fb64ec1139007973b1f09ec16d48549e82de22423cdba259f08",
       "README.md": "a0c88eff2fd93f76242793ff161ffdb9108ae5bdd1fd58fab9e8233fcc684228"}
LICENCE = "CC BY 4.0 (XED README.md, last line: 'License: Creative Commons Attribution 4.0 International License (CC-BY)')"

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
CACHE = HERE / "cache" / KEY
OUT = LEAN / "data/v13_parts/raw" / f"{KEY}.jsonl"
DEFS = LEAN / "data/v13_parts/defs" / f"{KEY}.json"
JB = LEAN.parents[1] / "bench/jevbench/datasets/public"

MAX_ROWS = 500
N_YESNO = 100          # multi-label verification rows (50 yes / 50 no)
N_CHOICE = MAX_ROWS - N_YESNO
CODE = {"1": "anger", "2": "anticipation", "3": "disgust", "4": "fear", "5": "joy", "6": "sadness",
        "7": "surprise", "8": "trust", "9": "neutral", "0": "neutral"}
EMOS = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
OPTIONS = list(EMOS)
Q_CHOICE = "Which emotion does this movie subtitle line express?"
Q_YESNO = "Does this movie subtitle line express {}?"

DEF = {
    "anger": "The speaker shows annoyance, rage, hostility or irritation toward someone or something, for example through insults, threats, shouting or aggressive demands.",
    "anticipation": "The speaker looks ahead to something expected: interest, eagerness, planning, curiosity, vigilance or expectation about what will or should happen next, without fear about it.",
    "disgust": "The speaker shows revulsion, contempt, loathing, disdain or weary boredom toward something seen as gross, offensive, distasteful, worthless or morally repugnant.",
    "fear": "The speaker shows fright, worry, anxiety, alarm or a sense of threat or danger to themselves or others.",
    "joy": "The speaker shows happiness, delight, serenity, amusement, pleasure, pride or excitement about something good that is happening or has happened.",
    "sadness": "The speaker shows sorrow, grief, disappointment, regret, loneliness, hurt or pensiveness about a loss or something bad.",
    "surprise": "The speaker reacts to something unexpected or just discovered with amazement, astonishment, shock, disbelief or sudden realisation, often as an exclamation or incredulous question.",
    "trust": "The speaker shows acceptance, agreement, confidence, reliance, reassurance, admiration or faith in someone or something, for example making a deal, a promise or a vouching remark.",
    "yes": "The line conveys the emotion named in the question, in the sense of Plutchik's emotion model used by XED annotators.",
    "no": "The line does not convey the emotion named in the question; it expresses other emotions or none of that kind.",
}

words = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).split()
norm = lambda t: " ".join(words(t))


def fetch():
    CACHE.mkdir(parents=True, exist_ok=True)
    for name, path in FILES.items():
        p = CACHE / name
        if not p.exists():
            urllib.request.urlretrieve(RAW + path, p)
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        assert h == SHA[name], f"{name} sha256 mismatch {h}"


def load():
    """Return {norm_text: rec}; rec = {rid, text, labels(set of names), src, orig_label}. Conflicting duplicates dropped."""
    recs, bad = {}, set()

    def add(k, rec):
        if k in bad:
            return
        if k in recs:
            if recs[k]["labels"] != rec["labels"]:
                bad.add(k)
                del recs[k]
            return
        recs[k] = rec

    for i, line in enumerate(open(CACHE / "en-annotated.tsv", encoding="utf-8", newline="")):
        line = line.rstrip("\r\n")
        text, lab = line.rsplit("\t", 1)
        codes = [c.strip() for c in lab.split(",") if c.strip()]
        if not codes or any(c not in CODE or c in ("0", "9") for c in codes):
            continue
        add(norm(text), {"rid": f"en-annotated.tsv:{i + 1}", "text": detok(text),
                         "labels": frozenset(CODE[c] for c in codes), "orig_label": lab.strip()})
    for i, line in enumerate(open(CACHE / "neu_en.txt", encoding="utf-8")):
        p = line.rstrip("\r\n").split("\t")
        if len(p) != 2 or p[0] != "9":
            continue
        add(norm(p[1]), {"rid": f"neu_en.txt:{i + 1}", "text": p[1].strip(),
                         "labels": frozenset(["neutral"]), "orig_label": "9"})
    return recs, len(bad)


def detok(t):
    t = re.sub(r" +([.,?!:;%)])", r"\1", t)
    t = re.sub(r"\( +", "(", t)
    t = re.sub(r" +(n't|'s|'re|'ll|'ve|'m|'d)\b", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()


def eligible(r):
    return len(r["text"].split()) >= 4 and 15 <= len(r["text"]) <= 4000 and len(words(r["text"])) >= 3


def contam(recs, n=13):
    """Return norm keys sharing a 13-gram with, or exactly equal to a state in, our train/dev/eval files or JevBench."""
    grams = collections.defaultdict(set)
    for k in recs:
        w = k.split()
        for i in range(len(w) - n + 1):
            grams[" ".join(w[i:i + n])].add(k)
    files = [f for f in glob.glob(str(LEAN / "data" / "*.jsonl")) if not Path(f).name.startswith("ohs")]
    files += glob.glob(str(JB / "*.jsonl"))
    hit = set()
    for f in files:
        for line in open(f, encoding="utf-8"):
            try:
                r = json.loads(line)
            except Exception:
                continue
            st = r.get("state") if isinstance(r, dict) else None
            if isinstance(st, str):
                ks = norm(st)
                if ks in recs:
                    hit.add(ks)
            if grams:
                w = words(line.replace("\\n", " "))
                for i in range(len(w) - n + 1):
                    g = " ".join(w[i:i + n])
                    if g in grams:
                        hit |= grams[g]
    return hit, len(files)


def row(rec, instr, options, gold, qtype, asked=None):
    return {"key": KEY, "rid": rec["rid"] + (f"#{asked}" if asked else ""), "state": rec["text"],
            "instructions": instr, "options": options, "gold": gold, "soft": None,
            "meta": {"dataset": "Helsinki-NLP/XED (English annotated + neutral)", "config": "en",
                     "revision": REV, "licence": LICENCE, "split": "train",
                     "orig_label": rec["orig_label"], "qtype": qtype,
                     "all_labels": sorted(rec["labels"]), **({"asked_label": asked} if asked else {})}}


def main():
    fetch()
    rng = random.Random(SEED)
    recs, n_conflict = load()
    recs = {k: r for k, r in recs.items() if eligible(r)}
    hit, n_files = contam(recs)
    for k in hit:
        recs.pop(k, None)
    print(f"eligible after dedup/filters: {len(recs) + len(hit)}; conflicting texts dropped: {n_conflict}; "
          f"decontam hits: {len(hit)} (checked {n_files} files)")

    keys = sorted(recs)
    rng.shuffle(keys)
    single = collections.defaultdict(list)
    multi = []
    for k in keys:
        r = recs[k]
        (single[next(iter(r["labels"]))] if len(r["labels"]) == 1 else multi).append(r)

    rows = []
    # choice: round-robin over the 9 labels
    qs = {lab: list(single[lab]) for lab in OPTIONS}
    while len(rows) < N_CHOICE and any(qs.values()):
        for lab in OPTIONS:
            if qs[lab] and len(rows) < N_CHOICE:
                rows.append(row(qs[lab].pop(0), Q_CHOICE, OPTIONS, lab, "choice"))
    # yes/no verification on multi-label lines: alternate yes/no, asked label round-robin over the 8 emotions
    i = 0
    mq = list(multi)
    while len([r for r in rows if r["meta"]["qtype"] == "yesno"]) < N_YESNO and mq:
        want_yes = i % 2 == 0
        emo = EMOS[(i // 2) % len(EMOS)]
        pick = next((j for j, r in enumerate(mq) if (emo in r["labels"]) == want_yes), None)
        i += 1
        if pick is None:
            continue
        r = mq.pop(pick)
        rows.append(row(r, Q_YESNO.format(emo), ["yes", "no"], "yes" if want_yes else "no", "yesno", emo))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    DEFS.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    DEFS.write_text(json.dumps(DEF, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    for w, d in DEF.items():
        assert 8 <= len(d.split()) <= 35, (w, len(d.split()))
    assert len({r["rid"] for r in rows}) == len(rows) and len({norm(r["state"]) for r in rows}) == len(rows)
    gold = collections.Counter(r["gold"] for r in rows)
    print(f"wrote {len(rows)} rows -> {OUT}")
    print("qtype:", dict(collections.Counter(r["meta"]["qtype"] for r in rows)))
    print("gold:", dict(gold), f"max share {max(gold.values()) / len(rows):.1%}")
    print("choice gold:", dict(collections.Counter(r["gold"] for r in rows if r["meta"]["qtype"] == "choice")))
    print("yesno asked:", dict(collections.Counter((r["meta"]["asked_label"], r["gold"]) for r in rows if r["meta"]["qtype"] == "yesno")))
    print("soft coverage: 0 (XED releases aggregated labels only, no annotator counts)")
    L = [len(r["state"]) for r in rows]
    print(f"chars min {min(L)} median {statistics.median(L)} mean {statistics.mean(L):.1f} max {max(L)}")


if __name__ == "__main__":
    main()
