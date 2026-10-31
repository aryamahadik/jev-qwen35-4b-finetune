"""F10 name modes (G0 section 2 Name modes): invented pseudo-words (syllable generator + pack jargon candidates,
filtered), neutral IDs, swapped familiar label words. Filter-only inputs (never emitted, never a seed): a multilingual
word list (English web2 + web2a + SCOWL / Hunspell en_* stems, French and Spanish Hunspell stems) and an English
common-word list (Hunspell en_US stems, SCOWL size-60 class) for the edit-distance >= 2 rule."""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from common import contains_tokens, sha256_file, tokens

DICT = Path("/usr/share/dict")
LO = Path("/Applications/LibreOffice.app/Contents/Resources/extensions")
WORDLISTS = [
    ("web2 (Webster's Second, public domain)", DICT / "web2", "plain"),
    ("web2a (Webster's Second phrases, public domain)", DICT / "web2a", "plain"),
    ("Hunspell en_GB (SCOWL, BSD-style SCOWL licence)", LO / "dict-en" / "en_GB.dic", "hun"),
    ("Hunspell en_US (SCOWL, BSD-style SCOWL licence)", LO / "dict-en" / "en_US.dic", "hun"),
    ("Hunspell en_AU (SCOWL)", LO / "dict-en" / "en_AU.dic", "hun"),
    ("Hunspell en_ZA", LO / "dict-en" / "en_ZA.dic", "hun"),
    ("Hunspell fr (Dicollecte, MPL-2.0)", LO / "dict-fr" / "fr.dic", "hun"),
    ("Hunspell es_ES (RLA-ES, GPL/LGPL/MPL tri-licence)", LO / "dict-es" / "es_ES.dic", "hun"),
    ("Hunspell es_MX (RLA-ES)", LO / "dict-es" / "es_MX.dic", "hun"),
]
COMMON_EN = ("Hunspell en_US stems (SCOWL size 60, common English)", LO / "dict-en" / "en_US.dic")
# fallback when the Hunspell list is absent: all of web2 (a superset of any top-50K list, so stricter)
COMMON_FALLBACK = ("web2 (all entries; stricter than a top-50K list)", DICT / "web2")

# morphology list (Claude seed, CC0): affixes and roots that give a meaning hint
MORPH_PREFIX = ["mal", "mis", "dis", "non", "anti", "pre", "post", "over", "under", "hyper", "hypo", "micro", "macro",
                "neo", "pseudo", "proto", "poly", "mono", "multi", "semi", "sub", "super", "trans", "ultra", "inter",
                "counter", "auto", "bio", "geo", "tele", "eco", "cyber", "mega", "omni", "pan", "re", "un", "de"]
MORPH_SUFFIX = ["phobia", "phile", "itis", "osis", "ism", "ist", "ology", "logy", "ness", "less", "ful", "able",
                "ible", "ment", "tion", "sion", "ize", "ise", "ify", "cide", "cracy", "crat", "graph", "scope", "meter",
                "gen", "oid", "ectomy", "emia", "algia", "phage", "ward", "wise", "ship", "hood", "dom", "ly", "ing",
                "er", "est", "ed", "ous", "ish", "ive", "al", "ic"]
PROFANITY = ["fuck", "shit", "cunt", "dick", "cock", "piss", "slut", "whore", "bitch", "bastard", "twat", "wank",
             "arse", "fag", "nigg", "spic", "kike", "chink", "tits", "porn", "rape", "anal", "crap", "damn", "hell",
             "nazi", "kill", "dead", "sex"]


def _read(path, kind):
    out = set()
    if not path.exists():
        return out
    with open(path, encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            if kind == "hun" and i == 0 and line.strip().isdigit():
                continue
            w = line.strip().split("/")[0].split("\t")[0].strip()
            if w:
                out.add(w.lower())
    return out


@lru_cache(maxsize=1)
def wordlist():
    words, rec = set(), []
    for name, p, kind in WORDLISTS:
        s = _read(p, kind)
        if s:
            rec.append({"name": name, "path": str(p), "sha256": sha256_file(p), "entries": len(s)})
        words |= s
    langs = sorted({"en"} | ({"fr"} if any("fr" in r["name"] for r in rec) else set())
                   | ({"es"} if any("es_" in r["name"] for r in rec) else set()))
    return frozenset(words), {"inputs": rec, "union_entries": len(words), "languages": langs}


@lru_cache(maxsize=1)
def common_en():
    s = _read(COMMON_EN[1], "hun")
    if s:
        return frozenset(s)
    return frozenset(w for w in _read(COMMON_FALLBACK[1], "plain") if len(w) >= 3)


def common_info():
    return {"name": COMMON_EN[0] if COMMON_EN[1].exists() else COMMON_FALLBACK[0],
            "path": str(COMMON_EN[1] if COMMON_EN[1].exists() else COMMON_FALLBACK[1]), "entries": len(common_en())}


def edits1(w):
    letters = "abcdefghijklmnopqrstuvwxyz"
    splits = [(w[:i], w[i:]) for i in range(len(w) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    trans = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    reps = [a + c + b[1:] for a, b in splits if b for c in letters]
    ins = [a + c + b for a, b in splits for c in letters]
    return set(deletes + trans + reps + ins)


def invented_ok(w: str) -> tuple[bool, str]:
    w = w.lower()
    if not re.fullmatch(r"[a-z]{5,10}", w):
        return False, "shape"
    wl, _ = wordlist()
    if w in wl:
        return False, "wordlist"
    if any(w.startswith(p) for p in MORPH_PREFIX) or any(w.endswith(s) for s in MORPH_SUFFIX):
        return False, "morphology"
    if any(p in w for p in PROFANITY):
        return False, "profanity"
    ce = common_en()
    if w in ce or any(e in ce for e in edits1(w)):
        return False, "editdist"
    return True, ""


ONSETS = ["b", "d", "f", "g", "k", "l", "m", "n", "p", "r", "s", "t", "v", "z", "br", "dr", "gl", "kr", "pl", "tr",
          "sk", "sn", "vr", "zh", "th", "fl", "gr", "bl", "st", "q"]
NUCLEI = ["a", "e", "i", "o", "u", "ai", "ou", "ea", "ie", "oa", "y"]
CODAS = ["", "", "", "n", "r", "l", "m", "k", "x", "s", "th", "nd", "rk", "lt", "mp"]


def syllable_word(r, length):
    for _ in range(200):
        w = ""
        while len(w) < length:
            w += r.choice(ONSETS) + r.choice(NUCLEI) + r.choice(CODAS)
        w = w[:length]
        if re.search(r"[aeiouy]", w[-3:]) and invented_ok(w)[0]:
            return w
    return None
