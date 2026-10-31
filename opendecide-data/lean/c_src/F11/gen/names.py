"""Names for F11 cards: invented glossary terms, code names (near-synonyms), code IDs, designators, group names.

Every string passes the reserved-word check (F11-R3-13, F11-R5-01: negcount 0 and no reserved token) and the card-level
uniqueness rule (no name or term is a whole-token run of another).
"""
from __future__ import annotations

import common  # noqa: F401 (sys.path)

import re
from functools import lru_cache

import negcount
from common import rng, toks, contains_run
from pathlib import Path

from lex import RESERVED_WORDS, STOPWORDS

_CONS = "bdfgklmnprstvz"
_VOW = "aeiou"
_BAD_AFFIX = re.compile(r"^(un|non|dis|mal|anti|mis|in|im|ir|il|de|re|pre|sub|over|under)|(ia|itis|phobia|less|ness|"
                        r"ment|ing|ed|er|ly|s|es|ism|ist|ous|ful|able|ible|tion|sion|ity)$")


WORDS_GZ = Path(__file__).resolve().parent / "english_words.txt.gz"    # pinned copy of the Mac's /usr/share/dict/words
# (gzip -9 -n; same content, so local output is unchanged) so the build is identical on any platform (rrun)


@lru_cache(maxsize=1)
def english() -> frozenset:
    import gzip
    if WORDS_GZ.exists():
        with gzip.open(WORDS_GZ, "rt") as f:
            return frozenset(w.strip().lower() for w in f)
    raise SystemExit(f"pinned word list missing: {WORDS_GZ}")


def name_ok(s: str) -> bool:
    """Reserved-word and negcount check on one name, term, designator or unit form (F11-R5-01)."""
    if not s or ": " in s or "\n" in s:
        return False
    for t in negcount.tokenize(s):
        if t.low in RESERVED_WORDS:
            return False
    c = negcount.count(s)
    return c.k_syn == 0 and c.k_all == 0


def pseudo_words(n: int, *key, exclude=()) -> list[str]:
    """n invented words (2-3 syllables, not English, no morphology hint; spec 2.2 F10 rule reused)."""
    r = rng("pseudo", *key)
    eng, out, seen = english(), [], {x.lower() for x in exclude}
    tries = 0
    while len(out) < n and tries < 20000:
        tries += 1
        k = r.choice((2, 2, 3))
        w = "".join(r.choice(_CONS) + r.choice(_VOW) + (r.choice("lnrst") if r.random() < 0.35 else "")
                    for _ in range(k))
        if not 5 <= len(w) <= 9 or w in eng or w in seen or _BAD_AFFIX.search(w):
            continue
        if any(w[:4] == x[:4] for x in seen):
            continue
        if not name_ok(w):
            continue
        seen.add(w)
        out.append(w)
    if len(out) < n:
        raise ValueError("pseudo word pool exhausted")
    return out


# Claude-written closed banks for code names (neutral, non-ordinal, no value words, no level words; SEM-41)
NAME_HEADS = ("Variance", "Lapse", "Fault", "Drift", "Slip", "Breach", "Deviation", "Defect", "Irregularity",
              "Discrepancy", "Anomaly", "Departure", "Gap", "Shortfall", "Mismatch", "Exception", "Incident",
              "Occurrence", "Finding", "Concern", "Divergence", "Error", "Glitch", "Flaw", "Snag", "Hitch",
              "Disruption", "Interruption", "Overrun", "Misstep", "Oversight", "Hazard", "Strain", "Fracture",
              "Irregularity", "Lag", "Spillover", "Overlap", "Conflict", "Variation")
NAME_MODS = ("Amber", "Cobalt", "Copper", "Slate", "Linen", "Cedar", "Harbor", "Lantern", "Willow", "Granite",
             "Saffron", "Juniper", "Marble", "Indigo", "Hazel", "Russet", "Ivory", "Pewter", "Coral", "Thistle",
             "Bramble", "Meadow", "Quartz", "Sable", "Fennel", "Tamarind", "Laurel", "Basalt", "Cinder", "Heron",
             "Kestrel", "Osprey", "Plover", "Wren", "Falcon", "Badger", "Otter", "Lynx", "Marten", "Ermine",
             "Aspen", "Birch", "Alder", "Rowan", "Hawthorn", "Sorrel", "Clover", "Yarrow", "Tansy", "Bracken",
             "Garnet", "Topaz", "Jasper", "Agate", "Onyx", "Beryl", "Opal", "Cobble", "Flint", "Shale",
             "Lowland", "Upland", "Coastal", "Inland", "Northern", "Southern", "Eastern", "Western", "Central",
             "Outer", "Inner", "Lateral", "Forward", "Aft", "Crosswise", "Diagonal", "Oblique", "Radial",
             "Transverse", "Proximal", "Distal", "Dorsal", "Ventral")
GROUP_HEADS = ("Cluster", "Family", "Branch", "Division", "Section", "Track", "Stream", "Ward", "Wing", "Sector")


def code_ids(n: int, *key) -> list[str]:
    """n code IDs in one per-card pattern of letters and digits, single tokens, no ordinal runs (SEM-41)."""
    r = rng("codeids", *key)
    pats = ("LLD", "LDL", "LLDD", "LDD", "LLDL")
    letters = "BCDFGHJKLMNPQRSTVWXZ"
    for _ in range(200):
        pat = r.choice(pats)
        out, seen = [], set()
        while len(out) < n:
            s = "".join(r.choice(letters) if c == "L" else r.choice("23456789") for c in pat)
            if s in seen or not name_ok(s):
                continue
            seen.add(s)
            out.append(s)
        if not ordinal_hit(out):
            return out
    raise ValueError("no code IDs")


def ordinal_hit(ids: list[str]) -> bool:
    """True when the IDs, read as numbers in list order, hold a run of 3 consecutive integers, or the list is sorted."""
    nums = []
    for s in ids:
        d = re.sub(r"\D", "", s)
        nums.append(int(d) if d else None)
    for i in range(len(nums) - 2):
        a, b, c = nums[i:i + 3]
        if None not in (a, b, c) and (b - a == 1 and c - b == 1 or a - b == 1 and b - c == 1):
            return True
    return len(ids) >= 3 and (ids == sorted(ids) or ids == sorted(ids, reverse=True))


def designators(prefix: str, n: int, *key, digits: int = 4, exclude=()) -> list[str]:
    r = rng("desig", prefix, *key)
    out, seen = [], set(exclude)
    lo, hi = 10 ** (digits - 1), 10 ** digits - 1
    while len(out) < n:
        s = f"{prefix}-{r.randint(lo, hi)}"
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def code_names(n: int, sibling_groups: list[list[int]], *key, avoid=()) -> list[str]:
    """Names for n codes: codes in one sibling group share a head word (near-synonyms with a neighbour); modifiers
    differ. avoid: value words and other card names (whole tokens). Raises when the banks run out."""
    r = rng("codenames", *key)
    avoid_t = {t for a in avoid for t in toks(a)}
    heads = [h for h in dict.fromkeys(NAME_HEADS) if h.lower() not in avoid_t]
    mods = [m for m in NAME_MODS if m.lower() not in avoid_t]
    r.shuffle(heads)
    r.shuffle(mods)
    names = [None] * n
    used = set()
    hi = 0
    for grp in sibling_groups:
        h = heads[hi % len(heads)]
        hi += 1
        for c in grp:
            for _ in range(500):
                m = r.choice(mods)
                nm = f"{m} {h}"
                if nm.lower() not in used:
                    break
            else:
                raise ValueError("code name bank exhausted")
            used.add(nm.lower())
            names[c] = nm
    for i in range(n):
        if names[i] is None:
            raise ValueError("code without a sibling group")
    return names


def group_names(n: int, *key, avoid=()) -> list[str]:
    r = rng("groupnames", *key)
    avoid_t = {t for a in avoid for t in toks(a)}
    mods = [m for m in NAME_MODS if m.lower() not in avoid_t]
    heads = [h for h in GROUP_HEADS if h.lower() not in avoid_t]
    h = r.choice(heads)
    ms = r.sample(mods, n)
    return [f"{m} {h}" for m in ms]


def overlap_free(strings: list[str]) -> bool:
    """No string is a whole-token run of another (case-folded); all distinct."""
    T = [toks(s) for s in strings]
    if len({tuple(t) for t in T}) != len(T):
        return False
    for i, a in enumerate(T):
        for j, b in enumerate(T):
            if i != j and len(a) < len(b) and contains_run(b, a):
                return False
    return True


def content_words(s: str, value_tokens: set) -> set:
    return {t for t in toks(s) if t not in STOPWORDS and t not in value_tokens}
