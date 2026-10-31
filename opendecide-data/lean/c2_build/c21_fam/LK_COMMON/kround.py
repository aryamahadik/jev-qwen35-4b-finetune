"""GV12 TWO-WAY slot round trip for the Haiku reword pass (K15 in T59, K14 in T60; binds every lane that lets Haiku reword text).
After rewording, (a) every decision-bearing span of the spec survives VERBATIM and (b) no decision-bearing span is ADDED: no value, count,
negation, qualifier, delegation line, order statement, consent naming, operation or target name, or word of the family's closed cue lexicon.
(b) is checked here by multiset comparison of numbers, negation words and the closed lexicon, plus the spec parse of solver B (the caller
passes `extra_new_spans` = what B's parser recovers from the reworded text that the spec does not contain). Failure is DROP-ONLY: the
reworded text is discarded, never repaired. Pure functions; no model is called.
"""
import collections
import re

_NUM = re.compile(r"\d+(?:\.\d+)?")
_NEG = re.compile(r"\b(?:not|no|never|none|without|neither|nor|cannot)\b|n't", re.I)

# closed cue lexicons (words that carry a decision in the family; a reworded text may not gain one the original lacks)
LEXICON = {
    "T59": ("either", "whichever", "any", "both", "default", "unless", "except", "only", "all", "every", "each", "undo", "undone", "permanent",
            "outside", "inside", "first", "then", "before", "after", "once", "instead", "ask", "confirm", "retry", "stop"),
    "T60": ("first", "then", "before", "after", "next", "finally", "once", "until", "order", "sequence", "afterwards", "followed", "begin",
            "start", "end", "last", "earlier", "later", "remember", "keep", "forget", "drop", "plan", "delegate"),
}


def _counts(pattern_or_words, text):
    if isinstance(pattern_or_words, re.Pattern):
        return sorted(m.group(0).lower() for m in pattern_or_words.finditer(text))
    out = []
    low = text.lower()
    for w in pattern_or_words:
        out += [w] * len(re.findall(r"\b" + re.escape(w) + r"\b", low))
    return sorted(out)


def two_way_ok(original, reworded, must_survive=(), family="T59", extra_new_spans=()):
    """-> (ok, reasons). `must_survive`: decision-bearing strings (values, ids, order statements, delegation lines ...) that must appear
    verbatim in `reworded`. `extra_new_spans`: spans solver B's parser recovers from `reworded` that are not in the spec (non-empty = fail)."""
    why = []
    for s in must_survive:
        if str(s) not in reworded:
            why.append("lost:%s" % str(s)[:30])
    if _counts(_NUM, original) != _counts(_NUM, reworded):
        why.append("numbers_differ")
    if len(_NEG.findall(original)) != len(_NEG.findall(reworded)):
        why.append("negation_count_differs")
    lo, lr = _counts(LEXICON[family], original), _counts(LEXICON[family], reworded)
    added = list((collections.Counter(lr) - collections.Counter(lo)).elements())
    if added:
        why.append("added_cue:%s" % ",".join(sorted(set(added))))
    if extra_new_spans:
        why.append("parser_found_new_span")
    return (not why), why
