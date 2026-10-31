"""formats-2 lints for Claude-written wordings: negation count (negcount), banned operator words, ROUGE-L between
seeds (G11: every Claude seed ROUGE-L < 0.7 to every other seed), OPI/attack strings (7.2 #8), length."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from common_f2 import LEAN

sys.path.insert(0, str(LEAN))
from c_src.common.negcount import count as negcount  # noqa: E402

TOKEN = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")

# Global operator ban: quantifiers, comparators, conditionals, modals, temporal order words, label and judgement
# words, and the family-defined status words (meets, assigned, fits, applies, holds, follows, determined, ...).
BANNED = [
    r"unless", r"except", r"excepting", r"only", r"if", r"either", r"or", r"all", r"every\w*", r"each", r"any\w*", r"some\w*",
    r"always", r"least", r"most", r"few", r"fewer", r"fewest", r"many", r"both", r"more", r"less", r"greater",
    r"above", r"below", r"over", r"under", r"between", r"within", r"beyond", r"exceed\w*", r"outside", r"equal\w*",
    r"before", r"after", r"until", r"till", r"since", r"while", r"when", r"whenever", r"first", r"last", r"next",
    r"previous\w*", r"earlier", r"earliest", r"later", r"latest", r"prior", r"former", r"latter",
    r"may", r"might", r"must", r"should", r"would", r"could", r"can", r"shall",
    r"right", r"wrong", r"true", r"false", r"correct", r"correctly", r"incorrect\w*", r"valid\w*", r"invalid\w*",
    r"accept\w*", r"reject\w*", r"approv\w*", r"den(?:y|ies|ied|ying)", r"yes", r"maybe", r"probabl\w*",
    r"likel\w*", r"unlikely", r"possibl\w*", r"impossible", r"certain\w*",
    r"appl(?:y|ies|ied|ying)", r"meet\w*", r"met", r"fit|fits|fitting|fitted", r"assign\w*", r"hold|holds|held",
    r"follow\w*", r"determin\w*", r"undetermined", r"enough", r"sufficient", r"insufficient", r"missing",
    r"known", r"unknown", r"unclear", r"necessar\w*", r"default\w*",
    r"ignore\w*", r"disregard\w*", r"override\w*", r"instead", r"pretend\w*", r"bypass\w*", r"forget\w*",
]
PHRASES = [r"in force", r"switched off", r"answer\s*:", r"task complete", r"previous instructions",
           r"a number of", r"not recorded"]
FAMILY_BANNED = {
    # F8 G0 section 5 (F8-AMB-22 / SEM wording lints as they bear on instruction wordings)
    "F8": [r"record\w*", r"log", r"logs", r"logged", r"on file", r"documented", r"registered", r"reported",
           r"likelihood", r"expected cost", r"expected loss", r"loss"],
    # F4 G0 section 7.5 (lines 1035-1052; F4-R4-04): the closed ban list for instruction wordings and persona lines,
    # every inflection. An F4 wording only tells the reader to read the record (or the card and the record) and to
    # answer the question or choose one of the options. Stricter than the literal list on two items: every form of
    # "decide" and "check" (the list names "decide whether" and "check whether").
    "F4": [
        # section 1 outcome words and other verbs of deciding or judging applied to the claim
        r"follow\w*", r"establish\w*", r"show\w*", r"rul(?:e|es|ed|ing)\s+out", r"leaves?\s+open", r"left\s+open",
        r"cannot\s+be\s+determined", r"decid\w*", r"judg\w*", r"check\w*", r"verif\w*", r"confirm\w*",
        r"assess\w*",
        # truth and correctness words
        r"true", r"truth\w*", r"false\w*", r"correct\w*", r"right\w*", r"wrong\w*", r"accept\w*", r"reject\w*",
        r"valid\w*",
        # words naming the claim or a statement
        r"claim\w*", r"statement\w*",
        # world, completeness, missing values, unknowns, trust, sources, facts, rules, derivation, outside knowledge
        r"treat\w*", r"assum\w*", r"consider\w*", r"counts?\s+as", r"counted\s+as", r"counting\s+as", r"only",
        r"stated", r"not\s+mentioned", r"missing", r"unknown", r"complet\w*", r"trust\w*", r"source\w*", r"fact\w*",
        r"rule\w*", r"work\w*\s+out", r"infer\w*", r"outside",
    ],
}
_BAN_RX = re.compile(r"(?<![a-z0-9'])(?:" + "|".join(BANNED) + r")(?![a-z0-9'])", re.I)
_PH_RX = re.compile("|".join(PHRASES), re.I)


def tokens(s):
    return TOKEN.findall(s.lower().replace("’", "'"))


def lint_text(text, family=None):
    probs = []
    n = negcount(text)
    if n.k_all or n.k_syn:
        probs.append(f"negation k_syn={n.k_syn} k_all={n.k_all}")
    for m in _BAN_RX.finditer(text):
        probs.append(f"banned word '{m.group(0)}'")
    for m in _PH_RX.finditer(text):
        probs.append(f"banned phrase '{m.group(0)}'")
    for rx in FAMILY_BANNED.get(family, []):
        if re.search(r"(?<![a-z0-9])(?:" + rx + r")(?![a-z0-9])", text, re.I):
            probs.append(f"family-banned '{rx}'")
    nt = len(tokens(text))
    if nt < 2 or nt > 70:
        probs.append(f"length {nt} words")
    if "\n" in text or "  " in text:
        probs.append("whitespace")
    return probs


def lcs(a, b):
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if x == y else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1]


def rouge_l(a, b):
    l = lcs(a, b)
    if l == 0:
        return 0.0
    p, r = l / len(b), l / len(a)
    return 2 * p * r / (p + r)


WTOKEN = re.compile(r"\w+")


def tokens_w(s):
    """Plain \\w+ tokenizer (splits "card's" into "card", "s"); G11 is checked under both tokenizers."""
    return WTOKEN.findall(s.lower().replace("’", "'"))


def _pairs_one(items, tok, thr):
    from collections import Counter
    toks = [(i, tok(t), Counter(tok(t))) for i, t in items]
    out = {}
    for x in range(len(toks)):
        ia, ta, ca = toks[x]
        for y in range(x + 1, len(toks)):
            ib, tb, cb = toks[y]
            if ia == ib:
                continue
            # exact bound: LCS <= multiset overlap, and ROUGE-L F <= 2*ov/(|a|+|b|)
            ov = sum((ca & cb).values())
            if ov == 0 or 2 * ov / (len(ta) + len(tb)) < thr:
                continue
            s = rouge_l(ta, tb)
            if s >= thr:
                k = tuple(sorted((ia, ib)))
                out[k] = max(out.get(k, 0.0), round(s, 3))
    return out


def rouge_pairs(items, thr=0.7):
    """items: list of (id, text); an id may appear more than once (US and GB spellings of one wording); pairs with
    the same id are skipped. ROUGE-L F is computed under BOTH tokenizers (`tokens`, which keeps "card's" whole, and
    the plain \\w+ `tokens_w`); a pair is returned when either score is >= thr. Returns (id1, id2, max score)."""
    a = _pairs_one(items, tokens, thr)
    b = _pairs_one(items, tokens_w, thr)
    for k, v in b.items():
        a[k] = max(a.get(k, 0.0), v)
    return [(k[0], k[1], v) for k, v in sorted(a.items())]
