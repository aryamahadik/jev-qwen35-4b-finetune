"""Build raw rows for breadth set "newsgroups20" (20 Newsgroups, by-date TRAIN split, 20-way topic choice).

Source: SetFit/20_newsgroups on the HF Hub, pinned revision f1b91292 (raw snapshot saved in
breadth_src/cache/newsgroups20/): train.jsonl only (sklearn fetch_20newsgroups(subset="train",
remove=("headers", "footers", "quotes")), see create_dataset.py). The by-date test split (test.jsonl) is never
downloaded or read.
Licence: CC BY 4.0, stated on the UCI Machine Learning Repository record for dataset 113 "Twenty Newsgroups"
(https://archive.ics.uci.edu/dataset/113/twenty+newsgroups, saved as cache/newsgroups20/uci_113.html).
Provenance: human-written Usenet posts (1993); the label is the newsgroup the author posted to (human choice).

Rows: one per source post, 20-way choice over all groups (so the close comp.* hardware/OS groups, the three
religion groups, the three politics groups and the rec.* sports/vehicle pairs always act as distractors),
round-robin over labels (~27-28 per group).
Filters: >= 40 words, 200-4000 chars, mostly prose (drops uuencoded binaries, PGP keys, tables of numbers),
posts naming a newsgroup (full or short form, e.g. "comp.windows.x", "t.r.m") dropped as label leakage,
exact-duplicate texts dropped (cross-posts with conflicting groups dropped entirely), no two selected posts sharing
a 13-word run, 13-gram decontamination + exact-state match against our train/dev/eval files and JevBench public
(never the ohs* files). Deterministic, seed 20261101.

  python breadth_src/build_newsgroups20.py
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
KEY = "newsgroups20"
REV = "f1b91292074e7cfb69be58b642d583ec262f30ed"
HF = f"https://huggingface.co/datasets/SetFit/20_newsgroups/resolve/{REV}/"
FILES = {"train.jsonl": HF + "train.jsonl", "README.md": HF + "README.md",
         "create_dataset.py": HF + "create_dataset.py",
         "uci_113.html": "https://archive.ics.uci.edu/dataset/113/twenty+newsgroups"}
SHA = {"train.jsonl": "b696a1d6a43a306b2ea21cdf20be62c1e56a04908053f24e606707454e84a728",
       "README.md": "3311a2a4199146b583258f2b3cc9436d6a2ce60e99db13218639df11cafd400a",
       "create_dataset.py": "90b2d8dabd9fff7b4f7bd3e0fae29fdd24553d698ea733a75cdbe7484d25263d"}
LICENCE = ("CC BY 4.0 (UCI ML Repository dataset 113 'Twenty Newsgroups', DOI 10.24432/C5C323: 'This dataset is "
           "licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license.' "
           "https://archive.ics.uci.edu/dataset/113/twenty+newsgroups)")

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
CACHE = HERE / "cache" / KEY
OUT = LEAN / "data/v13_parts/raw" / f"{KEY}.jsonl"
DEFS = LEAN / "data/v13_parts/defs" / f"{KEY}.json"
JB = LEAN.parents[1] / "bench/jevbench/datasets/public"

MAX_ROWS = 550
MIN_WORDS = 40
QUESTION = "Which newsgroup was this Usenet post written for?"

NAME = {
    "alt.atheism": "atheism",
    "comp.graphics": "computer graphics",
    "comp.os.ms-windows.misc": "MS Windows",
    "comp.sys.ibm.pc.hardware": "IBM PC hardware",
    "comp.sys.mac.hardware": "Mac hardware",
    "comp.windows.x": "X Window System",
    "misc.forsale": "for sale",
    "rec.autos": "cars",
    "rec.motorcycles": "motorcycles",
    "rec.sport.baseball": "baseball",
    "rec.sport.hockey": "hockey",
    "sci.crypt": "cryptography",
    "sci.electronics": "electronics",
    "sci.med": "medicine",
    "sci.space": "space",
    "soc.religion.christian": "Christianity",
    "talk.politics.guns": "gun politics",
    "talk.politics.mideast": "Middle East politics",
    "talk.politics.misc": "general politics",
    "talk.religion.misc": "religion (general)",
}
OPTIONS = list(NAME.values())

DEF = {
    "atheism": "alt.atheism: atheists debating believers: existence of God, arguments against religious claims, Bible contradictions, morality without God and atheist topics, written mainly from a non-believer's side.",
    "computer graphics": "comp.graphics: computer graphics software, algorithms, image file formats, rendering, 3D modelling, ray tracing, image processing and graphics programming, not display hardware or window systems.",
    "MS Windows": "comp.os.ms-windows.misc: using and configuring Microsoft Windows 3.x (and DOS under it): drivers, settings, Windows applications, fonts, memory setup and crashes.",
    "IBM PC hardware": "comp.sys.ibm.pc.hardware: IBM-compatible PC hardware: motherboards, CPUs, hard drives and controllers (IDE/SCSI), memory, BIOS, buses, cards, monitors and ports on PCs.",
    "Mac hardware": "comp.sys.mac.hardware: Apple Macintosh hardware: Mac models, upgrades, memory, drives, monitors, peripherals, accelerators and hardware problems on Macs.",
    "X Window System": "comp.windows.x: the X Window System on Unix workstations: X servers, clients, Xlib and Motif programming, widgets, window managers, X resources and display setup.",
    "for sale": "misc.forsale: classified ads offering or seeking items for sale or trade, with prices, condition and contact details; general wanted/for-sale posts.",
    "cars": "rec.autos: automobiles: car models, buying and selling cars, driving, repairs and maintenance, car performance, safety, insurance and automotive industry news.",
    "motorcycles": "rec.motorcycles: motorcycles and riding: bikes, riding technique, gear and helmets, maintenance, touring, rider safety and motorcyclist culture.",
    "baseball": "rec.sport.baseball: baseball, mostly Major League: teams, players, games, statistics, trades, managers, standings and predictions.",
    "hockey": "rec.sport.hockey: ice hockey, mostly NHL and international: teams, players, games, playoffs, statistics, trades and broadcasts.",
    "cryptography": "sci.crypt: cryptography and privacy: encryption algorithms, keys, PGP, the Clipper chip and key escrow, wiretapping, and government policy on encryption.",
    "electronics": "sci.electronics: electronics: circuits, components, schematics, power supplies, test equipment, radio and building or repairing electronic devices.",
    "medicine": "sci.med: medicine and health: diseases, symptoms, treatments, drugs, diet, medical research and questions about doctors and health care.",
    "space": "sci.space: space science and exploration: NASA and space agencies, launches, spacecraft, missions, astronomy, orbital mechanics and space policy or funding.",
    "Christianity": "soc.religion.christian: moderated, mostly civil discussion of Christian faith among believers and inquirers: Bible interpretation, theology, doctrine, denominations, prayer, church practice and Christian living.",
    "gun politics": "talk.politics.guns: firearms politics: gun control laws, the Second Amendment, gun rights, self-defence, gun crime and incidents such as Waco involving weapons.",
    "Middle East politics": "talk.politics.mideast: Middle East politics and conflicts: Israel and the Palestinians, Arab states, Turkey, Armenia and Azerbaijan, history, massacres and related disputes.",
    "general politics": "talk.politics.misc: US political debate not about guns or the Middle East: government, taxes, the economy, the Clinton administration, law, civil liberties, gay rights and social policy.",
    "religion (general)": "talk.religion.misc: unmoderated catch-all religion debate: cults and David Koresh, fringe or non-mainstream beliefs, and heated Bible or morality disputes between believers and skeptics.",
}

words = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).split()
norm = lambda t: " ".join(words(t))


def fetch():
    CACHE.mkdir(parents=True, exist_ok=True)
    for name, url in FILES.items():
        p = CACHE / name
        if not p.exists():
            urllib.request.urlretrieve(url, p)
        if name in SHA:
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            assert h == SHA[name], f"{name} sha256 mismatch {h}"
    assert "CC BY 4.0" in (CACHE / "uci_113.html").read_text(encoding="utf-8", errors="ignore")


def prose(t):
    """True for mostly-prose posts (drops uuencoded/binary dumps, PGP keys, number tables, ASCII art)."""
    toks = t.split()
    if not toks or max(len(w) for w in toks) > 60:
        return False
    letters = sum(c.isalpha() for c in t)
    alnum_ws = sum(c.isalpha() or c.isspace() for c in t)
    if alnum_ws / len(t) < 0.80 or letters / len(t) < 0.60:
        return False
    alpha_words = sum(1 for w in toks if re.fullmatch(r"[A-Za-z][A-Za-z'\-]*[.,;:!?)\"]*", w))
    return alpha_words / len(toks) >= 0.6


def load():
    """Return ({norm_text: rec}, n_conflict). rec = {rid, text, label, orig_label}."""
    recs, bad = {}, set()
    for i, line in enumerate(open(CACHE / "train.jsonl", encoding="utf-8")):
        r = json.loads(line)
        text = r["text"].strip()
        k = norm(text)
        if not k or k in bad:
            continue
        rec = {"rid": f"train.jsonl:{i + 1}", "text": text, "label": NAME[r["label_text"]],
               "orig_label": r["label_text"], "orig_id": r["label"]}
        if k in recs:
            if recs[k]["label"] != rec["label"]:
                bad.add(k)
                del recs[k]
            continue
        recs[k] = rec
    return recs, len(bad)


# Label leakage: a post that names a newsgroup (e.g. "Followups directed to comp.windows.x", "post to sci.space")
# gives the gold away, so any post naming one of the 20 groups or their hierarchies is dropped.
GROUP_RE = re.compile(r"\b(alt\.atheism|comp\.(graphics|os|sys|windows)|misc\.forsale|rec\.(autos|motorcycles|sport)"
                      r"|sci\.(crypt|electronics|med|space)|soc\.religion|talk\.(politics|religion)|rec\.moto)", re.I)
# Usenet short forms of the group names (t.r.m = talk.religion.misc, c.o.msw = comp.os.ms-windows.misc, ...),
# each checked in the train file to occur almost only in its own group.
ABBR_RE = re.compile(r"(?<![\w.])(a\.a\.|c\.o\.m\w*|c\.s\.[im]\w*|c\.w\.x|c\.g\.|t\.r\.m?|t\.p\.[gm]\w*|s\.r\.c"
                     r"|r\.s\.[bh])(?!\w)", re.I)


def eligible(r):
    t = r["text"]
    return (200 <= len(t) <= 4000 and len(words(t)) >= MIN_WORDS and prose(t)
            and not GROUP_RE.search(t) and not ABBR_RE.search(t))


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
            w = words(line.replace("\\n", " "))
            for i in range(len(w) - n + 1):
                g = " ".join(w[i:i + n])
                if g in grams:
                    hit |= grams[g]
    return hit, len(files)


def ngrams(k, n=13):
    w = k.split()
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def row(rec):
    return {"key": KEY, "rid": rec["rid"], "state": rec["text"], "instructions": QUESTION,
            "options": OPTIONS, "gold": rec["label"], "soft": None,
            "meta": {"dataset": "SetFit/20_newsgroups (20 Newsgroups by-date, sklearn headers/footers/quotes removed)",
                     "config": "default", "revision": REV, "licence": LICENCE, "split": "train",
                     "orig_label": rec["orig_label"], "orig_label_id": rec["orig_id"], "qtype": "choice"}}


def main():
    fetch()
    rng = random.Random(SEED)
    recs, n_conflict = load()
    n_all = len(recs)
    recs = {k: r for k, r in recs.items() if eligible(r)}
    hit, n_files = contam(recs)
    for k in hit:
        recs.pop(k, None)
    print(f"unique texts: {n_all}; conflicting cross-posts dropped: {n_conflict}; eligible: {len(recs) + len(hit)}; "
          f"decontam hits: {len(hit)} (checked {n_files} files); pool: {len(recs)}")
    print("pool per label:", dict(collections.Counter(r["label"] for r in recs.values())))

    keys = sorted(recs)
    rng.shuffle(keys)
    queues = collections.defaultdict(list)
    for k in keys:
        queues[recs[k]["label"]].append(k)

    rows, seen_grams = [], set()
    while len(rows) < MAX_ROWS and any(queues.values()):
        for lab in OPTIONS:
            while queues[lab] and len(rows) < MAX_ROWS:
                k = queues[lab].pop(0)
                g = ngrams(k)
                if g & seen_grams:      # near-duplicate / re-post of an already selected post
                    continue
                seen_grams |= g
                rows.append(row(recs[k]))
                break

    OUT.parent.mkdir(parents=True, exist_ok=True)
    DEFS.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    DEFS.write_text(json.dumps(DEF, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    assert set(DEF) == set(OPTIONS)
    for w, d in DEF.items():
        assert 8 <= len(d.split()) <= 35, (w, len(d.split()))
    assert len({r["rid"] for r in rows}) == len(rows) and len({norm(r["state"]) for r in rows}) == len(rows)
    gold = collections.Counter(r["gold"] for r in rows)
    print(f"wrote {len(rows)} rows -> {OUT}")
    print("gold:", dict(gold), f"max share {max(gold.values()) / len(rows):.1%}")
    print("soft coverage: 0 (the label is the posting newsgroup; no annotator counts exist)")
    L = [len(r["state"]) for r in rows]
    print(f"chars min {min(L)} median {statistics.median(L)} mean {statistics.mean(L):.1f} max {max(L)}")


if __name__ == "__main__":
    main()
