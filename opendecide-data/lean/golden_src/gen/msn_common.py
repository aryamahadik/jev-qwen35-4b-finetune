"""Shared helpers for the moral_social_norms program generators (gen_msn_*). CPU-only, deterministic.

Labels follow by construction: every item is built from explicit facts and an explicit rule / agreement /
permission, and a small decision function computes the answer. No model is called.
"""
import collections
import datetime as dt
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent.parent
sys.path.insert(0, str(HERE.parent / "moral_social_norms"))
from common import (EDGE_TAGS, append_manifest, check_rows, edge_join, edge_tags, norm, summary,  # noqa: E402
                    write_defs, yesno_share)

RAW = LEAN / "data" / "v14_parts" / "raw"
FAMILY = "moral_social_norms"

# name, subject pronoun, object pronoun, possessive
PEOPLE = [
    ("Amara", "she", "her", "her"), ("Bilal", "he", "him", "his"), ("Chen Wei", "he", "him", "his"),
    ("Daniela", "she", "her", "her"), ("Emeka", "he", "him", "his"), ("Farah", "she", "her", "her"),
    ("Gustavo", "he", "him", "his"), ("Hana", "she", "her", "her"), ("Ibrahim", "he", "him", "his"),
    ("Jolene", "she", "her", "her"), ("Kenji", "he", "him", "his"), ("Leilani", "she", "her", "her"),
    ("Mateo", "he", "him", "his"), ("Nadia", "she", "her", "her"), ("Oluwaseun", "he", "him", "his"),
    ("Priya", "she", "her", "her"), ("Quentin", "he", "him", "his"), ("Rosa", "she", "her", "her"),
    ("Sipho", "he", "him", "his"), ("Tamar", "she", "her", "her"), ("Umar", "he", "him", "his"),
    ("Valentina", "she", "her", "her"), ("Wojtek", "he", "him", "his"), ("Ximena", "she", "her", "her"),
    ("Yusuf", "he", "him", "his"), ("Zanele", "she", "her", "her"), ("Aarav", "he", "him", "his"),
    ("Brigid", "she", "her", "her"), ("Carlos", "he", "him", "his"), ("Dilnoza", "she", "her", "her"),
    ("Eero", "he", "him", "his"), ("Fatima", "she", "her", "her"), ("Giorgos", "he", "him", "his"),
    ("Halima", "she", "her", "her"), ("Isaac", "he", "him", "his"), ("Jia Hui", "she", "her", "her"),
    ("Kwame", "he", "him", "his"), ("Lucia", "she", "her", "her"), ("Marcus", "he", "him", "his"),
    ("Noor", "she", "her", "her"), ("Oskar", "he", "him", "his"), ("Paloma", "she", "her", "her"),
    ("Rahul", "he", "him", "his"), ("Svetlana", "she", "her", "her"), ("Tomasz", "he", "him", "his"),
    ("Uzma", "she", "her", "her"), ("Viktor", "he", "him", "his"), ("Wren", "they", "them", "their"),
    ("Yara", "she", "her", "her"), ("Zeke", "he", "him", "his"), ("Alex", "they", "them", "their"),
    ("Sam", "they", "them", "their"), ("Jordan", "they", "them", "their"), ("Riley", "they", "them", "their"),
    ("Aiyana", "she", "her", "her"), ("Bongani", "he", "him", "his"), ("Céline", "she", "her", "her"),
    ("Dmitri", "he", "him", "his"), ("Esperanza", "she", "her", "her"), ("Finn", "he", "him", "his"),
    ("Grace", "she", "her", "her"), ("Hamza", "he", "him", "his"), ("Ingrid", "she", "her", "her"),
    ("Javier", "he", "him", "his"), ("Keiko", "she", "her", "her"), ("Liam", "he", "him", "his"),
    ("Mei", "she", "her", "her"), ("Nikolai", "he", "him", "his"), ("Olga", "she", "her", "her"),
    ("Pedro", "he", "him", "his"), ("Rania", "she", "her", "her"), ("Stefan", "he", "him", "his"),
    ("Thandiwe", "she", "her", "her"), ("Tariq", "he", "him", "his"), ("Ulla", "she", "her", "her"),
    ("Vikram", "he", "him", "his"), ("Winifred", "she", "her", "her"), ("Xavier", "he", "him", "his"),
    ("Yetunde", "she", "her", "her"), ("Zoltan", "he", "him", "his"), ("Anika", "she", "her", "her"),
    ("Benedikt", "he", "him", "his"), ("Chiara", "she", "her", "her"), ("Deshawn", "he", "him", "his"),
    ("Elif", "she", "her", "her"), ("Felipe", "he", "him", "his"), ("Gulnara", "she", "her", "her"),
    ("Hiroshi", "he", "him", "his"), ("Imani", "she", "her", "her"), ("Jakob", "he", "him", "his"),
]

NUMW = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def person(rng, exclude=()):
    while True:
        p = rng.choice(PEOPLE)
        if p[0] not in exclude:
            return p


def num(n, rng=None, words=0.5):
    """Number as a word (<= 12) with probability `words`, else digits."""
    if rng is not None and 0 <= n <= 12 and rng.random() < words:
        return NUMW[n]
    return str(n)


def plural(n, one, many=None):
    return one if n == 1 else (many or one + "s")


def fmt_time(h, m=0, style=0):
    """style 0: '10:30 p.m.', 1: '22:30', 2: '10:30 PM'; midnight/noon handled."""
    if style == 1:
        return f"{h:02d}:{m:02d}"
    hh = h % 12 or 12
    suf = ("a.m." if h < 12 else "p.m.") if style == 0 else ("AM" if h < 12 else "PM")
    return f"{hh}:{m:02d} {suf}" if m else f"{hh} {suf}"


def fmt_date(d, style=0, weekday=True):
    wd = WEEKDAYS[d.weekday()] + ", " if weekday else ""
    if style == 0:
        return f"{wd}{MONTHS[d.month - 1]} {d.day}"
    return f"{wd}{d.day} {MONTHS[d.month - 1]}"


def cap(s):
    return s[:1].upper() + s[1:]


_THEY_VERBS = ("holds", "runs", "helps", "keeps", "lives", "owns", "works", "needs", "takes", "makes", "gets", "wants",
               "says", "thinks", "knows", "likes", "uses", "brings", "pays", "goes")


def fix_they(t):
    """Reviewer fix: singular 'they' takes plural verb agreement ('they was' -> 'they were', 'they runs' -> 'they run').
    Deterministic surface normalisation only; never changes a fact, a number or a label."""
    import re
    t = re.sub(r"\b([Tt]hey) was\b", r"\1 were", t)
    t = re.sub(r"\b([Tt]hey) is\b", r"\1 are", t)
    t = re.sub(r"\b([Tt]hey) has\b", r"\1 have", t)
    t = re.sub(r"\b([Tt]hey) does\b", r"\1 do", t)
    t = re.sub(r"\b([Tt]hey) (" + "|".join(_THEY_VERBS) + r")\b", lambda m: m.group(1) + " " + m.group(2)[:-1]
               if not m.group(2).endswith("es") or m.group(2) in ("takes", "makes", "likes", "uses", "lives") else
               m.group(1) + " " + m.group(2)[:-2], t)
    t = re.sub(r"\b([Tt]hey took a new ticket, number \d+, and) was\b", r"\1 were", t)
    return t


def row(key, rid, state, question, gold, qid, edge, orig, config, twin_of=None, gen_version="1"):
    state, question = fix_they(state), fix_they(question)
    meta = {"dataset": f"program generator golden_src/gen/{key}.py", "config": config, "revision": f"gen-v{gen_version}",
            "licence": "Generated by Claude-written program in this repo (no third-party text)", "split": "train",
            "orig_label": orig, "family": FAMILY, "edge": edge, "defs": qid}
    if twin_of:
        meta["twin_of"] = twin_of
    return {"key": key, "rid": rid, "state": state, "instructions": question, "options": ["yes", "no"],
            "gold": gold, "soft": None, "meta": meta}


def write_gen(key, rows, defs, notes, dataset_desc):
    import hashlib
    src = Path(sys.modules["__main__"].__file__).resolve()
    # pins the exact generator source AND every shared module it imports (reviewer fix: deps were not pinned)
    deps = [src, HERE / "msn_common.py", HERE / "gen_msn_rules.py", HERE.parent / "moral_social_norms" / "common.py"]
    h = hashlib.sha256()
    for d in dict.fromkeys(deps):
        h.update(d.read_bytes())
    rev = "gen-v1+sha256:" + h.hexdigest()[:16]
    for r in rows:
        r["meta"]["revision"] = rev
    check_rows(rows)
    RAW.mkdir(parents=True, exist_ok=True)
    out = RAW / f"{key}.jsonl"
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    for qid, d in defs.items():
        write_defs(f"{key}__{qid}", d)
    summary(rows)
    append_manifest({"key": key, "family": FAMILY, "dataset": dataset_desc,
                     "licence": "n/a (program-generated; Claude-written templates and rules, labels by construction)",
                     "rows": len(rows), "qtype": "yesno", "yesno_share": yesno_share(rows),
                     "edge_tags": edge_tags(rows), "notes": notes})
    return out
