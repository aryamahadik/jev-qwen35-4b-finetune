"""F6 closed-lexicon scans (G0 3.1). Data only: the banned-phrase lists of 3.1, the completeness-word ban (F6-R5-05),
the marker / plan / evidence lexicons, the question-frame ban and the instruction-wording rule (F6-R5-06).

Used by the generator to filter pack strings and by the G3 parser (parse_f6.py) on record, question, option and
instruction-wording text. Switch sentences (matched whole against the switch-sentence table), the fixed option
wordings and S5 dialogue markers are exempt (3.1 "Scope of the scan").
"""
from __future__ import annotations

import re

BANNED = [  # 3.1 "banned" column (operators, quantifiers, dates, ranges, hedges, plans, markers, evidence, negation)
    "when", "whenever", "provided that", "as long as", "in case", "where",
    "only when", "if and only if", "iff",
    "except", "except when", "but not if", "otherwise", "save", "notwithstanding",
    "in all other cases", "by default",
    "despite", "regardless of",
    "the first rule that matches", "the first rule that applies", "first match", "in order", "in the order listed",
    "top to bottom", "earlier rules", "later rules", "higher in the list", "lower in the list", "takes priority",
    "takes precedence",
    "and/or", "either", "one or the other",
    "or more", "or fewer", "or less", "up to", "a minimum of", "a maximum of", "not below", "not above",
    "over", "under", "beyond",
    "until", "till", "through", "within", "since", "starting", "due", "the deadline is", "prior to", "following",
    "early", "mid", "late", "spring", "summer", "autumn", "fall", "winter", "quarter",
    "between", "days later", "business days", "working days",
    "any", "some", "none", "a few", "most",
    "about", "approximately", "roughly", "around", "nearly", "almost",
    "booked", "will", "intends", "pending", "upcoming", "arranged",
    "n/a", "tbd", "will check",
    "alleged", "reportedly", "claimed",
    "is it clear that", "is it false that", "best", "most likely", "should",
    "never", "neither", "nor", "without", "fail to", "fails to", "failed to", "lack", "lacks", "lacked", "refuse",
    "refused", "deny", "denied", "hardly", "other than", "rule out", "ruled out",
    "is not more than", "is not less than", "does not exceed", "not exceeding", "is not before", "is not after",
    "not equal to", "not at least",
]
QUESTION_BANNED = ["wrong", "right", "reject", "accept", "would be", "should be"]
COMPLETENESS = ["all", "every", "each", "whole", "entire", "full", "complete", "exhaustive", "only", "partial",
                "incomplete", "known", "so far"]
MARKERS = ["not recorded", "unknown"]
S5_MARKERS = ["don't know", "declined to answer", "can't recall"]
PLAN_WORDS = ["scheduled", "planned", "expected", "requested"]
EVIDENCE_TAGS = ["unverified", "self-reported"]
ABSTAIN_WORDS = ["determined", "determine", "settle", "settled", "enough information", "none of these",
                 "nothing more", "undetermined", "leaves this open"]
WORDING_BANNED = (["likely", "likelihood", "guess", "guessing", "best", "most likely", "should", "assume",
                   "assumption", "assumptions", "default", "defaults", "unsure", "not sure", "uncertain",
                   "establish", "establishes", "show that", "shows", "determine", "determined", "settle", "settled",
                   "leave open", "leaves open", "impossible to tell", "enough information", "none of these",
                   "not recorded", "unknown", "missing", "complete", "incomplete", "full", "extent"]
                  + COMPLETENESS)
QUANTIFIERS_S = ["every", "all", "each", "at least one"]


def _rx(words):
    alts = sorted({re.escape(w) for w in words}, key=len, reverse=True)
    return re.compile(r"(?<![A-Za-z0-9'])(" + "|".join(alts) + r")(?![A-Za-z0-9'])", re.I)


_BANNED = _rx(BANNED)
_COMPL = _rx(COMPLETENESS)
_MARK = _rx(MARKERS + S5_MARKERS + PLAN_WORDS + EVIDENCE_TAGS + ABSTAIN_WORDS)
_WORD_BAN = _rx(WORDING_BANNED + BANNED)
_DASH_RANGE = re.compile(r"(?<![\d\-])\d+\s*[-\u2010-\u2015\u2212]\s*\d+(?![\d\-])")
_DASH_ALONE = re.compile(r"(^|\s)[-‐-―−]+(\s|$)")


ALLOWED = ["at most", "at least one", "at least", "no fewer than", "no less than", "no more than", "no later than",
           "no earlier than", "on or before", "on or after", "only if", "exactly when"]
_ALLOWED = _rx(ALLOWED)


def banned_hits(text: str) -> list[str]:
    text = _ALLOWED.sub(" ", text)
    out = [m.group(1).lower() for m in _BANNED.finditer(text)]
    if _DASH_RANGE.search(text):
        out.append("dash range")
    return out


_QBAN = None


def question_hits(text: str) -> list[str]:
    global _QBAN
    if _QBAN is None:
        _QBAN = _rx(QUESTION_BANNED)
    return [m.group(1).lower() for m in _QBAN.finditer(text)]


def completeness_hits(text: str) -> list[str]:
    text = _ALLOWED.sub(" ", text)
    return [m.group(1).lower() for m in _COMPL.finditer(text)]


def record_hits(text: str) -> list[str]:
    """Pack strings used as names, headings, keys or values: 3.1 banned list, completeness ban, and no overlap with
    the marker / plan / evidence / abstain lexicons (row 41: pairwise disjoint)."""
    return banned_hits(text) + completeness_hits(text) + [m.group(1).lower() for m in _MARK.finditer(text)] + \
        (["dash"] if _DASH_ALONE.search(text) else [])


def wording_hits(text: str) -> list[str]:
    """F6-R5-06: an instruction wording names the answer format only (no answer semantics), and passes the 3.1 scan,
    the completeness ban and the frame ban."""
    return [m.group(1).lower() for m in _WORD_BAN.finditer(text)] + \
        (["dash range"] if _DASH_RANGE.search(text) else [])
