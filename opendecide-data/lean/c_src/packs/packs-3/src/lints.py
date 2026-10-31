"""Pack lints for packs-3 (C_DATA_SPEC v4 2.1; family G0 pack rules referenced, not copied).

Word slots (values, names, kinds, roles, statuses, outcomes, label words, jargon) get the strict union of the pack-word
rules the G0 specs state: F9-R2-13 (connectives, comparator words, time-lead words, number tokens, marker words),
F3 rule 5 / R3-07 / R1-16 (mechanism stems, holder-change words, XF06 markers, negcount entries and implicit-cue verbs,
the eleven stem words), F1 outcome-name rule (no negation, no affixal negation), F7 factor-name rule (no negation cue,
no risk / plan / request / expectation factor). Phrase slots (events, consequences, fillers, inert facts, register
prose) get the negation lints only. Every family still runs its own pack lint before a card uses a pack.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LEAN = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(LEAN))
from c_src.common.negcount import count as negcount  # noqa: E402

CONNECTIVES = {"and", "or", "nor", "neither", "either", "unless", "only", "not", "but", "if", "except"}
COMPARATOR_WORDS = {"least", "more", "most", "fewer", "fewest", "less", "over", "under", "up", "between", "above",
                    "below", "exceed", "exceeds", "exceeded", "exceeding", "same", "than", "equal", "equals", "max",
                    "min", "maximum", "minimum", "beyond", "within"}
TIME_LEAD = {"before", "after", "from", "ending", "within", "per", "since", "until", "through", "till", "during"}
MARKER_WORDS = {"unknown", "none", "no", "null", "false", "true", "yes", "nil", "na", "n/a", "tbd", "tba", "void"}
MARKER_PHRASES = {"not recorded", "not stated", "not checked", "not known", "not available"}
ELEVEN = {"answer", "answers", "answered", "option", "options", "choice", "choices", "correct", "correctly",
          "incorrect", "incorrectly"}
MECH_STEMS = ["void", "cancel", "withdr", "amend", "correct", "fix", "supersed", "replac", "renam", "renumber", "mov",
              "retir", "merg", "consolidat", "absorb", "transfer", "revert", "revers", "creat", "adjust", "missing",
              "releas", "return", "dispos", "lost", "lose", "handed"]
IMPLICIT_VERBS = ["lack", "fail", "deny", "denie", "denial", "refus", "declin", "omit", "omission", "neglect",
                  "prevent", "absent", "absence", "without", "missing"]
FACTOR_BANNED = {"risk", "risks", "possible", "possibly", "request", "requests", "requested", "schedule", "scheduled",
                 "plan", "planned", "plans", "expected", "expect", "expects", "likely", "potential"}
AFFIX_NEG = re.compile(r"^(non-?[a-z]{3,}|un(?!der|it|ion|iform|ique|iversal|ison|ifi|ify|til)[a-z]{3,})$")
AFFIX_OK = {"under", "union", "unit", "units", "unity", "uniform", "uniforms", "unique", "universal", "university",
            "unison", "unload", "unloading", "unloaded", "unpack", "unpacking", "unearth", "nonce", "undertaker",
            "underpass", "underground", "undercroft", "understudy", "uniformed", "unitary", "uncle"}
NEG_PREFIX_WORDS = {"ineligible", "inactive", "incomplete", "invalid", "inadequate", "insufficient", "inaccurate",
                    "indirect", "illegal", "illegible", "irregular", "improper", "impractical", "impassable",
                    "disqualified", "disallowed", "discontinued", "dishonoured", "dishonored", "disapproved",
                    "inoperable", "inoperative", "insecure", "unsafe", "unpaid", "unlicensed", "unsigned",
                    "inaccessible", "incompatible", "inconsistent", "illegitimate", "immature", "impermissible",
                    "dissatisfied", "disorderly", "unfit", "unsound", "untidy", "unstable"}
NUMBER_TOKEN = re.compile(r"\d")


def tokens(s: str) -> list[str]:
    return re.findall(r"[a-z]+(?:[-'][a-z]+)*", s.lower().replace("_", " "))


def _stem_hit(tok: str, stems) -> str | None:
    for st in stems:
        if tok.startswith(st):
            return st
    return None


def neg_issues(s: str, allow_affix: bool = False) -> list[str]:
    out = []
    nc = negcount(s)
    if nc.k_all:
        out.append(f"negcount k_all={nc.k_all}")
    for t in tokens(s):
        base = t
        for part in base.split("-"):
            h = _stem_hit(part, IMPLICIT_VERBS)
            if h:
                out.append(f"implicit-cue:{h}")
        if not allow_affix:
            if (AFFIX_NEG.match(t) and t not in AFFIX_OK) or t in NEG_PREFIX_WORDS:
                out.append(f"affixal-negation:{t}")
    return out


def word_issues(s: str, *, mech: bool = True, allow_affix: bool = False, factor: bool = False) -> list[str]:
    """Strict lint for a word slot. Returns a list of issue codes (empty = pass)."""
    out = []
    low = s.lower().strip()
    if not low:
        return ["empty"]
    if NUMBER_TOKEN.search(low):
        out.append("number-token")
    if low in MARKER_WORDS or low in {"-", "?", "--", "??", "0", "1"}:
        out.append("marker-word")
    for mp in MARKER_PHRASES:
        if mp in low:
            out.append("marker-phrase")
    toks = tokens(low)
    split = [p for t in toks for p in t.split("-")]
    for t in split:
        if t in CONNECTIVES:
            out.append(f"connective:{t}")
        if t in COMPARATOR_WORDS:
            out.append(f"comparator:{t}")
        if t in TIME_LEAD:
            out.append(f"time-lead:{t}")
        if t in MARKER_WORDS:
            out.append(f"marker-token:{t}")
        if t in ELEVEN:
            out.append(f"stem-word:{t}")
    for t in toks:
        if mech:
            for part in t.split("-"):
                h = _stem_hit(part, MECH_STEMS)
                if h and part not in {"movie", "movies", "creative", "creativity", "creature", "returner"}:
                    out.append(f"mechanism:{h}")
        if factor and t in FACTOR_BANNED:
            out.append(f"factor-kind:{t}")
    out += neg_issues(low, allow_affix=allow_affix)
    return sorted(set(out))


def phrase_issues(s: str) -> list[str]:
    out = []
    if NUMBER_TOKEN.search(s):
        out.append("number-token")
    out += neg_issues(s.lower())
    toks = set(tokens(s))
    if toks & {"not", "no", "never", "none", "nobody", "nothing", "neither", "nor", "nowhere"}:
        out.append("core-negation")
    return sorted(set(out))


def lcs(a: list[str], b: list[str]) -> int:
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


def rouge_l(a: str, b: str) -> float:
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    l = lcs(ta, tb)
    if l == 0:
        return 0.0
    p, r = l / len(tb), l / len(ta)
    return 2 * p * r / (p + r)


def damerau(a: str, b: str) -> int:
    la, lb = len(a), len(b)
    d = [[0] * (lb + 1) for _ in range(la + 1)]
    for i in range(la + 1):
        d[i][0] = i
    for j in range(lb + 1):
        d[0][j] = j
    for i in range(1, la + 1):
        for j in range(1, lb + 1):
            c = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + c)
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
    return d[la][lb]


def levenshtein(a: str, b: str) -> int:
    la, lb = len(a), len(b)
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i] + [0] * lb
        for j in range(1, lb + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
        prev = cur
    return prev[lb]
