"""VOICE solver B, component 2: the independent SPAN-SURVIVAL CHECKER (gate V-C4, step (a2)). Written from VOICE/SCHEMA.md section 3.

    check(doc, hyp_text) -> bool                  kept?
    check_detail(doc, hyp_text) -> dict           {'kept', 'reasons': [..], 'spans': [(id, role, kind, ok)]}

Method (G0-lite section 2, solver B column): CHARACTER- AND KEY-LEVEL MATCHING with its own number-form normaliser and letter-run
joiner; no word alignment, no semi-Markov search.
    negation / polarity  global signature of stand-alone negation words, reference against hypothesis (contractions expanded);
    number / quantity / date  the canonical value must be one of the readings of a maximal number run (or a date item) of the hypothesis,
                              each hypothesis item consumed at most once (a longer run is a different number);
    entity / name / path / flag / rule / statement / authority  the span's folded character string (spoken symbols to characters, letter
                              names to letters, digit words to digits, case and fillers dropped, spaces dropped) must occur in the folded
                              hypothesis starting at a token boundary and ending at a token boundary (any token may contribute either its
                              own letters or its folded reading).
The context-recoverable exception is OFF (ctx_recoverable_enabled = False); a deleted or garbled span always drops the variant.
Python 3 standard library only; imports nothing from solver A.
"""
import re

from vb_tables import LETTER_NAME, SYMBOL_PHRASE, DIGIT_WORD, DOUBLE_YOU, NEGATION_WORDS, FILLERS
import vb_numbers as N
import vb_hyp as H
from vb_denorm import invert_segment, DenormError

CTX_RECOVERABLE_ENABLED = False


# ---------------------------------------------------------------------------------------------------------------------
# reference side: folded characters of a spoken token range

def fold_reference(doc, lo, hi):
    """Folded character string for spoken tokens [lo, hi), using the segment map for what each token IS."""
    toks = doc["tokens"]
    out = []
    for seg in sorted(doc["segments"], key=lambda g: g["tok"][0]):
        a, b = seg["tok"]
        a2, b2 = max(a, lo), min(b, hi)
        if a2 >= b2:
            continue
        words = [w.lower() for w in toks[a2:b2]]
        kind = seg["kind"]
        if kind == "disfl":
            continue
        if (a2, b2) == (a, b):
            try:
                if kind == "number":
                    out.append(invert_segment("number", seg.get("style", ""), words).replace(",", ""))
                else:
                    out.append(invert_segment(kind, seg.get("style", ""), words))
            except DenormError:
                out.append("".join(words))
        else:   # a span that cuts a segment: fold token by token
            out.append(_fold_loose(kind, words))
    return "".join(out).lower()


def _fold_loose(kind, words):
    parts = []
    i = 0
    while i < len(words):
        w = words[i]
        if kind == "spelled":
            if w == "capital":
                i += 1
                continue
            if w == DOUBLE_YOU[0] and i + 1 < len(words) and words[i + 1] == DOUBLE_YOU[1]:
                parts.append("w")
                i += 2
                continue
            parts.append(LETTER_NAME.get(w, w))
        elif kind == "digits" or kind == "number":
            parts.append(str(DIGIT_WORD[w]) if w in DIGIT_WORD else w)
        elif kind == "sym":
            if i + 1 < len(words) and (w, words[i + 1]) in SYMBOL_PHRASE:
                parts.append(SYMBOL_PHRASE[(w, words[i + 1])])
                i += 2
                continue
            parts.append(SYMBOL_PHRASE.get((w,), w))
        else:
            parts.append(w)
        i += 1
    return "".join(parts)


# ---------------------------------------------------------------------------------------------------------------------
# hypothesis side

def contains_folded(units, ref, relaxed=False):
    """Does `ref` occur as a concatenation of whole units (each contributing one of its alternatives), starting and ending on unit
    boundaries? relaxed: it may also start / end inside a unit (substring of the folded stream)."""
    if not ref:
        return True
    if relaxed:
        # build the stream with the first alternative that keeps characters, try the folded and the raw version
        raw = "".join(u[1][0] for u in units)
        fold = "".join(u[1][-1] for u in units)
        return ref in raw or ref in fold
    n = len(units)
    reach = [set() for _ in range(n + 1)]
    for i in range(n):
        reach[i].add(0)
        for off in reach[i]:
            for alt in units[i][1]:
                if alt and ref.startswith(alt, off):
                    reach[i + 1].add(off + len(alt))
    for i in range(1, n + 1):
        if len(ref) in reach[i]:
            return True
    return False


class HypView(object):
    def __init__(self, text):
        self.text = text
        self.tokens = H.coarse_tokens(text)
        self.units = H.alternatives(self.tokens)
        self.items = N.hyp_number_items(self.tokens)
        self.used = [False] * len(self.items)
        self.ref_tokens = []
        self.preconsumed = set()


def _canon_number(c):
    """Canonical comparison form of a span's canonical number string (commas folded away)."""
    return c.replace(",", "")


def _match_number_group(view, spans, idx):
    """Fallback when a span has no reading of its own: two or three consecutive number spans whose spoken words ended up adjacent in the
    hypothesis (the words between them were dropped) are one run of number words. If that run is exactly the spoken words of the spans
    in a row, all of them survive. Returns the number of spans consumed (0 = no)."""
    toks = view.tokens
    for g in (3, 2):
        grp = spans[idx:idx + g]
        if len(grp) < g or not all(_span_is_numberish(s) and s["kind"] != "date" for s in grp):
            continue
        words = []
        for s in grp:
            words.extend(w.lower() for w in view.ref_tokens[s["tok"][0]:s["tok"][1]])
        for k, it in enumerate(view.items):
            if view.used[k] or it["kind"] != "number":
                continue
            if toks[it["start"]:it["end"]] == words:
                view.used[k] = True
                return g
    return 0


def _match_number(view, canonical, kind):
    want = _canon_number(canonical)
    for k, it in enumerate(view.items):
        if view.used[k]:
            continue
        if kind == "date" and it["kind"] != "date":
            continue
        if kind != "date" and it["kind"] == "date":
            continue
        if want in it["cands"]:
            view.used[k] = True
            parts = it.get("alt_of")
            for k2, it2 in enumerate(view.items):   # an alternative reading of the same tokens is consumed with it
                if parts and (it2["start"], it2["end"]) in [tuple(p) for p in parts]:
                    view.used[k2] = True
                if it2.get("alt_of") and (it["start"], it["end"]) in [tuple(p) for p in it2["alt_of"]]:
                    view.used[k2] = True
            return True
    return False


def _span_is_numberish(span):
    return span["role"] == "number" and span["kind"] in ("number", "quantity", "date", "version", "year", "ordinal", "percent")


def check_detail(doc, hyp_text):
    view = HypView(hyp_text)
    reasons = []
    results = []
    # 1. global negation signature (stand-alone negation words; contractions expanded; identifiers excluded)
    ref_tokens = []
    for w in doc["tokens"]:
        ref_tokens.extend(H.expand_contraction(w.lower()))
    ref_sig = H.negation_signature(ref_tokens)
    hyp_sig = H.negation_signature(view.tokens)
    neg_ok = (ref_sig == hyp_sig)
    if not neg_ok:
        reasons.append("negation_signature")
    # 1b. global polarity signature (a polarity word that appears or disappears anywhere changes what the instruction permits)
    if H.polarity_signature(ref_tokens) != H.polarity_signature(view.tokens):
        reasons.append("polarity_signature")
    # 2. spans in order
    view.ref_tokens = doc["tokens"]
    word_pool = {}
    for tok in view.tokens:
        word_pool[tok] = word_pool.get(tok, 0) + 1
    word_used = {}
    spans = doc["spans"]
    for si, span in enumerate(spans):
        role, kind, canon_s = span["role"], span["kind"], span["canonical"]
        lo, hi = span["tok"]
        ok = True
        if si in view.preconsumed:
            results.append((span.get("id"), role, kind, True))
            continue
        if role == "negation":
            if kind in ("negation",) and canon_s.lower() in NEGATION_WORDS or kind == "negation":
                ok = neg_ok   # covered by the signature
            else:   # polarity word: it must stand in the hypothesis as a word as often as the reference span needs it
                w = canon_s.lower()
                word_used[w] = word_used.get(w, 0) + 1
                ok = word_pool.get(w, 0) >= word_used[w]
        elif _span_is_numberish(span):
            parts = canon_s.split()
            ok = _match_number(view, parts[0], "date" if kind == "date" else "number")
            if not ok and kind != "date":
                g = _match_number_group(view, spans, si)
                if g:
                    ok = True
                    view.preconsumed.update(range(si + 1, si + g))
            for extra in parts[1:]:
                e = extra.lower()
                word_used[e] = word_used.get(e, 0) + 1
                ok = ok and word_pool.get(e, 0) >= word_used[e]
        else:   # entity / name / path / flag / rule / statement / authority / any other kind
            ref = fold_reference(doc, lo, hi)
            relaxed = bool(span.get("partial"))
            ok = contains_folded(view.units, ref, relaxed=relaxed)
        results.append((span.get("id"), role, kind, ok))
        if not ok:
            reasons.append("%s:%s" % (role, kind))
    kept = (not reasons)
    return {"kept": kept, "reasons": reasons, "spans": results}


def check(doc, hyp_text):
    return check_detail(doc, hyp_text)["kept"]
