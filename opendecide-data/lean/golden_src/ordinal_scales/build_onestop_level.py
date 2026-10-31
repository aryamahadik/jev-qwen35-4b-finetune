"""Build raw rows for onestop_level: at which of three ordered reading levels (elementary < intermediate < advanced)
was this news passage written?

Source : OneStopEnglish corpus (Vajjala & Lucic, BEA 2018), GitHub nishkalavallabhi/OneStopEnglishCorpus @
         37f8db3945cd2f3cc0caafe45674147b224349be (codeload zip, sha256 pinned), Texts-Together-OneCSVperFile/*.csv
         (189 articles; columns Elementary / Intermediate / Advanced, one paragraph per row). The CSV version is used
         because the Texts-SeparatedByReadingLevel/Int-Txt files have all non-ASCII typography stripped (no curly
         apostrophes/quotes, 'dont') and an 'Intermediate' header line - artefacts that would give the level away.
         Files are decoded as UTF-8, cp1252 or MacRoman (detected per file); PDF line wraps are re-joined and fi/fl
         ligatures expanded, identically for all levels; articles whose PDF extraction LOST the fi/fl ligatures
         ('Of ce', 'Paci c', ' rst') in any level are dropped entirely. No splits -> train.
Licence: CC BY-SA 4.0 (repo LICENSE.markdown and README.md 'This work is licensed under a Creative Commons
         Attribution-ShareAlike 4.0 International License').
Texts  : Guardian news articles (advanced = original level) rewritten by English teachers at onestopenglish.com
         (Macmillan) into intermediate and elementary versions for learners (human-written).
Labels : the level of the version the passage comes from (a human editorial decision, one per version) -> soft null.
Chunks : each version is split into passages of consecutive paragraphs (>= 70 words, at most ~220 words); a passage
         is DROPPED when its best word-5-gram Jaccard overlap with any passage of another level of the same article is
         >= 0.45 (the teacher left it almost unchanged, so its level cannot be told from the text); exact + near-exact
         dedupe inside the dataset; decontamination.
Balance: up to 500 passages per level; at most 4 passages per article-level so no article dominates.
Deterministic (seed 20261101); CPU only; no model calls.
"""
import collections
import csv
import io
import random
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ord_common as C  # noqa: E402

KEY = "onestop_level"
SEED = C.SEED
CACHE = C.CACHE / KEY
COMMIT = "37f8db3945cd2f3cc0caafe45674147b224349be"
URL = f"https://codeload.github.com/nishkalavallabhi/OneStopEnglishCorpus/zip/{COMMIT}"
ZIP_SHA = "4f57d7b4e91a0990623b175e5c7a0b44aa3c622fb131f3c3d2efa2e4aa389739"
LICENCE = (f"CC BY-SA 4.0 (https://github.com/nishkalavallabhi/OneStopEnglishCorpus/blob/{COMMIT}/LICENSE.markdown; "
           f"README.md 'This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International "
           f"License')")
DATASET = "OneStopEnglish corpus (nishkalavallabhi/OneStopEnglishCorpus), Texts-Together-OneCSVperFile"
LEVELS = [("Ele", "elementary"), ("Int", "intermediate"), ("Adv", "advanced")]
OPTIONS = ["elementary", "intermediate", "advanced"]
PER_LEVEL = 500
PER_ARTICLE_LEVEL = 4
QUESTION = ("This passage comes from a news article that English teachers rewrote for language learners at three "
            "reading levels. At which level is this passage written?")
DEFS = {
    "elementary": "The easiest rewrite (about CEFR A2-B1): short, mostly single-clause sentences, very common words, "
                  "simple tenses, difficult terms explained or dropped, few idioms or long noun phrases.",
    "intermediate": "The middle rewrite (about B1-B2): moderately long sentences with some subordinate clauses, "
                    "mostly everyday vocabulary with some less common words, lighter simplification of the original.",
    "advanced": "The original native-level newspaper text (about C1): long multi-clause sentences, rich or "
                "technical vocabulary, idioms, figurative language and dense reported speech, with no "
                "simplification.",
}


LEVEL_WORDS = {"elementary", "intermediate", "advanced"}
LIGATURE_LOSS = re.compile(r"(?<![’'])\b(?:Of ce|of ce|Paci c|speci c|signi cant|bene t|bene ts|con rm|de nitely|ef cient|"
                           r"scienti c|dif cult|traf c|in uence|rst|nal|nally|nancial|eld|elds|gure|gures|ight|"
                           r"ights|oor|oors|lm|lms|nd|nds|ve)\b(?![-'’])")


def decode(raw):
    """CSV files are UTF-8, cp1252 or MacRoman (the latter shows as 'McDonaldÕs' / 'ÒquoteÓ' if misread)."""
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        pass
    if any(b in raw for b in (b"\x92", b"\x93", b"\x94", b"\x96")):
        return raw.decode("cp1252")
    if any(b in raw for b in (b"\xd5", b"\xd2", b"\xd3", b"\xd0")):
        return raw.decode("mac_roman")
    return raw.decode("cp1252")


def unwrap(cell):
    """The CSV cells keep the PDF line wraps: re-join them (a wrapped hyphenated compound keeps its hyphen)."""
    lines = [ln.strip() for ln in cell.replace("\r", "").split("\n") if ln.strip()]
    out = ""
    for ln in lines:
        if not out:
            out = ln
        elif out.endswith("-") and ln[:1].islower():
            out += ln
        else:
            out += " " + ln
    out = out.replace("\ufb01", "fi").replace("\ufb02", "fl")
    return C.clean(out)


def chunks(paras):
    out, cur, n = [], [], 0
    for p in paras:
        w = len(p.split())
        if cur and n + w > 220:
            if n >= 70:
                out.append("\n".join(cur))
            cur, n = [], 0
        cur.append(p)
        n += w
        if n >= 70:
            out.append("\n".join(cur))
            cur, n = [], 0
    if cur and n >= 70:
        out.append("\n".join(cur))
    return out


def jacc(a, b):
    return len(a & b) / max(1, len(a | b))


def main():
    p = C.fetch(URL, CACHE / f"OneStopEnglishCorpus-{COMMIT}.zip", ZIP_SHA)
    stats = collections.Counter()
    docs = collections.defaultdict(dict)  # article -> level -> list of paragraphs
    with zipfile.ZipFile(p) as z:
        for name in z.namelist():
            m = re.match(rf"OneStopEnglishCorpus-{COMMIT}/Texts-Together-OneCSVperFile/([^/]+)\.csv$", name)
            if not m:
                continue
            text = decode(z.read(name))
            rows = list(csv.reader(io.StringIO(text)))
            hdr = [h.strip() for h in rows[0]]
            if hdr[:3] != ["Elementary", "Intermediate", "Advanced"]:
                stats["drop_bad_header"] += 1
                continue
            levs = {}
            for j, lev in enumerate(("Ele", "Int", "Adv")):
                paras = [unwrap(r[j]) for r in rows[1:] if len(r) > j and r[j].strip()]
                levs[lev] = [x for x in paras if x and x.lower() not in LEVEL_WORDS]
            if any(LIGATURE_LOSS.search(" ".join(v)) for v in levs.values()):
                stats["drop_article_pdf_ligature_loss"] += 1  # e.g. 'Of ce', 'Paci c': 'fi'/'fl' lost in extraction
                continue
            docs[m.group(1).strip()] = levs
    stats["articles"] = len(docs)
    recs = []
    for art in sorted(docs):
        lv = docs[art]
        if set(lv) != {"Ele", "Int", "Adv"}:
            stats["drop_incomplete_article"] += 1
            continue
        ch = {k: chunks(v) for k, v in lv.items()}
        sh = {k: [C.shingles(c) for c in cs] for k, cs in ch.items()}
        for k, opt in LEVELS:
            for i, c in enumerate(ch[k]):
                best = max((jacc(sh[k][i], o) for k2 in sh if k2 != k for o in sh[k2]), default=0.0)
                if best >= 0.45:
                    stats["drop_same_as_other_level"] += 1
                    continue
                recs.append({"rid": f"ose-{re.sub(r'[^a-z0-9]+', '_', art.lower()).strip('_')}-{k.lower()}-{i}",
                             "art": art, "lev": opt, "text": c, "best": round(best, 3), "pos": i})
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
    used = collections.Counter()
    for x in uniq:
        if x["rid"] in hits:
            continue
        if used[(x["art"], x["lev"])] >= PER_ARTICLE_LEVEL:
            continue
        used[(x["art"], x["lev"])] += 1
        per[x["lev"]].append(x)
    n = min(PER_LEVEL, min(len(v) for v in per.values()) + 150)
    chosen = [x for o in OPTIONS for x in per[o][:n]]
    rows = []
    for x in chosen:
        edge = []
        if x["best"] >= 0.3:
            edge.append("ambiguous")  # close to another level's wording
        if C.REPORTED.search(x["text"]):
            edge.append("reported_speech")
        rows.append({
            "key": KEY, "rid": x["rid"], "state": x["text"], "instructions": QUESTION, "options": OPTIONS,
            "gold": x["lev"], "soft": None,
            "meta": {"dataset": DATASET, "config": "passages of 70-220 words; levels Ele/Int/Adv",
                     "revision": f"git:{COMMIT}; sha256(codeload zip):{ZIP_SHA}", "licence": LICENCE,
                     "split": "train", "orig_label": {"level": x["lev"], "article": x["art"], "passage": x["pos"],
                                                      "max_overlap_other_levels": x["best"]},
                     "family": C.FAMILY, "edge": C.edge_join(edge), "seed": SEED},
        })
    rng.shuffle(rows)
    C.write_outputs(KEY, rows, {None: DEFS})
    print(dict(stats))
    st = C.summary(KEY, rows)
    C.show_samples(rows, n=5, seed=2)
    rec = C.manifest_record(
        KEY, DATASET, LICENCE, rows, "choice (3-level ordinal reading level)",
        "Passages (70-220 words) from teacher-rewritten Guardian articles at elementary / intermediate / advanced "
        "level; passages nearly unchanged across levels (5-gram Jaccard >= 0.45) dropped; <= 4 passages per "
        "article-level; balanced.", st)
    return rows, rec


if __name__ == "__main__":
    rows, rec = main()
    if "--manifest" in sys.argv:
        C.append_manifest(rec)
        print("manifest record appended")
