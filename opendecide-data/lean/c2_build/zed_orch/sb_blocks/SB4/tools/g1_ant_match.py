#!/usr/bin/env python3
"""G1 helper for SB4 (A58 b, c.1): do the ANS headlines come from the ANT corpus, and can ANT-origin rows be told apart?

Counts only: no row text is printed or stored. Reads (as untrusted data; run with `python -I`):
  SB4/src/data/stance/{train,dev}.csv      ANS stance pairs (columns s1, s2, stance)
  SB4/ant_probe/v21/**/*.txt               ANT v2.1 multi-source files (a <TITLE> per document)
Writes SB4/checks/g1_ant_match.json (counts and the repeat statistics that identify the reference column).
"""
import csv
import glob
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

SB4 = Path(__file__).resolve().parent.parent
DIAC = re.compile("[ً-ٰٟـ]")
PUNCT = re.compile(r"[^\w\s]", re.U)


def norm(t: str) -> str:
    t = unicodedata.normalize("NFKC", t)
    t = DIAC.sub("", t)
    t = (t.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
          .replace("ى", "ي").replace("ة", "ه"))
    t = PUNCT.sub(" ", t.lower())
    return " ".join(t.split())


def read_csv(p):
    with open(p, encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        h = next(r)
        return h, list(r)


def jacc(a: set, b: set) -> float:
    return len(a & b) / max(1, len(a | b))


def main():
    # ANT titles
    titles = []
    nfiles = 0
    per_src = Counter()
    for p in sorted(glob.glob(str(SB4 / "ant_probe/v21/*/*/*.txt"))):
        nfiles += 1
        t = open(p, encoding="utf-8", errors="replace").read()
        m = re.search(r"<TITLE>(.*?)</TITLE>", t, re.S)
        if m:
            titles.append(norm(m.group(1)))
            per_src[Path(p).parts[-3]] += 1
    tset = set(titles)
    index = defaultdict(set)
    for i, t in enumerate(titles):
        for w in set(t.split()):
            index[w].add(i)
    tw = [set(t.split()) for t in titles]
    out = {"ant_files": nfiles, "ant_titles": len(titles), "ant_distinct_titles": len(tset), "ant_titles_per_source": dict(per_src)}

    def near(s: str):
        ws = set(s.split())
        if len(ws) < 3:
            return False
        # candidate docs by the rarest words
        cands = Counter()
        for w in sorted(ws, key=lambda w: len(index.get(w, ()))):
            if len(index.get(w, ())) > 400:
                continue
            for i in index.get(w, ()):
                cands[i] += 1
        for i, _ in cands.most_common(40):
            if jacc(ws, tw[i]) >= 0.8:
                return True
        return False

    for split in ("train", "dev"):
        h, rows = read_csv(SB4 / f"src/data/stance/{split}.csv")
        i1, i2, ic = h.index("s1"), h.index("s2"), h.index("stance")
        s1 = [norm(r[i1]) for r in rows]
        s2 = [norm(r[i2]) for r in rows]
        c1, c2 = Counter(s1), Counter(s2)
        rep = lambda c: {"distinct": len(c), "repeated_values": sum(1 for v in c.values() if v > 1), "rows_with_repeated_value": sum(v for v in c.values() if v > 1)}
        d = {"rows": len(rows), "s1_repeats": rep(c1), "s2_repeats": rep(c2),
             "s1_values_also_in_s2": len(set(c1) & set(c2)),
             "stance": dict(Counter(r[ic] for r in rows))}
        for name, col in (("s1", s1), ("s2", s2)):
            ex = [x in tset for x in col]
            nr = [(not e) and near(x) for e, x in zip(ex, col)]
            d[f"{name}_exact_in_ant"] = sum(ex)
            d[f"{name}_near_in_ant_not_exact"] = sum(nr)
            d[f"{name}_any_match"] = sum(1 for e, n in zip(ex, nr) if e or n)
        any_pair = sum(1 for a, b in zip(s1, s2) if (a in tset or near(a)) or (b in tset or near(b)))
        d["rows_with_any_side_matching_ant"] = any_pair
        out[split] = d
    out["note"] = "counts only; norm = NFKC, strip tashkeel/tatweel, alef/ya/ta-marbuta fold, drop punctuation; near = word-set Jaccard >= 0.8"
    (SB4 / "checks").mkdir(exist_ok=True)
    (SB4 / "checks/g1_ant_match.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
