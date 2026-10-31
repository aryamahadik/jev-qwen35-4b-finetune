"""Style and wording pools for F10 rows: training format styles (fmt1, never the 50 held-out ones) restricted to
record containers; S5 uses only the held-out styles. Instruction wordings: the formats-2 F10 pool filtered by the
wording-kind lint (R5-02) and the negation-frame lint (XF10)."""
from __future__ import annotations

import json
import re
from functools import lru_cache

from common import FMT2_DIR
from fmt1 import pool

RECORD_CT = ("prose", "memo", "bullet_sop", "key_value", "form", "json", "yaml", "csv", "markdown_table", "html_snippet")
KIND_VERBS = {
    "meets": ["meet", "meets", "met", "meeting", "apply", "applies", "applied", "applying", "match", "matches",
              "matched", "matching", "fit", "fits", "fitted", "fitting", "satisfy", "satisfies", "satisfied",
              "satisfying", "qualify", "qualifies", "qualified", "qualifying"],
    "assigned": ["assign", "assigns", "assigned", "assigning", "get", "gets", "got", "getting", "given", "receive",
                 "receives", "received", "receiving"],
    "defines": ["define", "defines", "defining"],
}
RULE_WORDS = [r"\banswer (?:yes|no)\b", r"\byes if\b", r"\bno if\b", r"\bfirst\b", r"\border\b", r"\btie\b",
              r"\bcannot be determined\b", r"\bnone of\b", r"\bunknown\b", r"\bmissing\b", r"\bwrong\b", r"\bright\b",
              r"\breject\b", r"\baccept\b", r"\bshould\b", r"\bwould\b"]


def kind_of(text):
    w = set(re.findall(r"[a-z]+", text.lower()))
    return {k for k, vs in KIND_VERBS.items() if w & set(vs)}


def wording_ok(text):
    if kind_of(text):
        return False
    t = text.lower()
    return not any(re.search(p, t) for p in RULE_WORDS)


@lru_cache(maxsize=1)
def wordings():
    rows = [json.loads(l) for l in open(FMT2_DIR / "wordings" / "family_pools.jsonl") if l.strip()]
    f10 = [r for r in rows if r.get("family") == "F10"]
    ok = [r for r in f10 if wording_ok(r["text"])]
    return ok, [r["id"] for r in f10 if r not in ok]


@lru_cache(maxsize=2)
def styles(held_out=False):
    out = {}
    for st in pool.styles(held_out=held_out):
        if st["container"] not in RECORD_CT or st["flags"].get("single_collection"):
            continue
        cs = pool.card_style(st["card_style"])
        if cs.get("def_layout") == "next_line":
            continue
        out.setdefault(st["omission_marker"], []).append(st)
    return out
