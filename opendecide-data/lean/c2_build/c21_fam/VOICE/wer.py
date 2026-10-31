"""WER (whisper-normaliser STYLE, our own code; not the whisper-normalizer package) and the word aligner. Solver A side.

normalise(): lower case, contractions expanded, punctuation dropped, fillers dropped, symbol words / letter names / spelled
digits folded to a canonical symbol, runs of number words folded to digits. Reference and hypothesis go through the SAME function,
so digits-vs-words, symbols-vs-words and letters-vs-names are not errors (inverse text normalisation is not what WER measures).
NOT implemented (stated, UNVERIFIED effect): the package's British-to-American spelling map.
"""
import re

import numwords as NW
from vcommon import BAND_EDGES, FILLERS, NAME_TO_LETTER, WORD_TO_SYMBOL

_CONTRACT = [("won't", "will not"), ("can't", "can not"), ("cannot", "can not"), ("n't", " not"), ("'ll", " will"), ("'re", " are"),
             ("'ve", " have"), ("'m", " am"), ("'d", " would"), ("'s", " is")]
_TOK = re.compile(r"\d{4}-\d{2}-\d{2}|\d+(?:[.,]\d+)*%?(?:st|nd|rd|th)?|[a-z]+(?:'[a-z]+)?|[/\\._~#:=*@+&|<>$^%-]")
_NUMISH = set(NW.ONES) | {t for t in NW.TENS if t} | {"hundred", "thousand", "million", "billion", "point", "and", "oh"}


def _is_ordinal_word(t):
    return t in NW.ORD_REV or (t.endswith("th") and (t[:-2] in NW.ONES or t[:-2] in NW.TENS)) or (t.endswith("ieth") and t[:-4] + "y" in NW.TENS)


_MONTHS = {m: i + 1 for i, m in enumerate(NW.MONTHS)}
_MONTHS.update({m[:3]: i + 1 for i, m in enumerate(NW.MONTHS)})


def _fold_dates(toks):
    """month day year / day month year -> one ISO token, so a spoken date and a written date are the same on both sides."""
    out, i, n = [], 0, len(toks)

    def day(t):
        m = re.match(r"^(\d{1,2})(?:st|nd|rd|th)?$", t)
        return int(m.group(1)) if m and 1 <= int(m.group(1)) <= 31 else None
    while i < n:
        t = toks[i]
        if t in _MONTHS and i + 2 < n and day(toks[i + 1]) and re.match(r"^\d{4}$", toks[i + 2]):
            out.append("%s-%02d-%02d" % (toks[i + 2], _MONTHS[t], day(toks[i + 1])))
            i += 3
        elif day(t) and i + 2 < n and toks[i + 1] in _MONTHS and re.match(r"^\d{4}$", toks[i + 2]):
            out.append("%s-%02d-%02d" % (toks[i + 2], _MONTHS[toks[i + 1]], day(t)))
            i += 3
        else:
            out.append(t)
            i += 1
    return out


def _expand(text):
    t = text.lower()
    for a, b in _CONTRACT:
        t = t.replace(a, b)
    return t


_SOFT = {".", ",", ";", "!", "?", ":"}


def tokenize_text(text, regex=None):
    """Regex tokens, except that clause-level punctuation ('.', ',', ':' ...) attached to the end of a word is dropped
    ('delete it.' -> delete it). Inner punctuation (3.11, a.b) and isolated or leading symbols (' . ', '.log') are kept."""
    rx = regex or _TOK
    out = []
    for m in rx.finditer(text):
        t = m.group(0)
        if t in _SOFT:
            a, b = m.start() - 1, m.end()
            prev_alnum = a >= 0 and text[a].isalnum()
            next_alnum = b < len(text) and text[b].isalnum()
            if prev_alnum and not next_alnum:
                continue
        out.append(t)
    return out


def raw_tokens(text):
    return tokenize_text(_expand(text))


def _fold_numbers(toks):
    out, i, n = [], 0, len(toks)
    while i < n:
        t = toks[i]
        if (t in _NUMISH or _is_ordinal_word(t)) and not (t in ("and", "point", "oh") and (not out or i + 1 >= n)):
            j = i
            while j < n and (toks[j] in _NUMISH or toks[j].isdigit() or _is_ordinal_word(toks[j])):
                j += 1
            best = None
            if not any(x not in ("oh", "and", "point") for x in toks[i:j]):         # 'oh' alone is a letter name, not a zero
                out.append(t)
                i += 1
                continue
            for k in range(j, i, -1):                      # longest parsable prefix of the run
                run = toks[i:k]
                if run[0] in ("and", "point") or run[-1] in ("and", "point"):
                    continue
                cands = NW.parse_number_tokens(run)
                if cands:
                    best = (k, sorted(cands, key=lambda c: (len(c), c))[0])
                    break
            if best:
                out.append(best[1])
                i = best[0]
                continue
        out.append(t)
        i += 1
    return out


def normalise(text):
    toks = [t for t in raw_tokens(text) if t not in FILLERS]
    toks = _fold_dates(_fold_numbers(toks))
    out = []
    for t in toks:
        t = t.replace(",", "") if re.match(r"^\d{1,3}(,\d{3})+", t) else t
        if t in WORD_TO_SYMBOL and t not in ("and",):
            t = WORD_TO_SYMBOL[t]
        elif t in NAME_TO_LETTER:                # symmetric fold: 'you are' and 'u r' are the same on both sides
            t = NAME_TO_LETTER[t]
        out.append(t)
    return _glue(out)


def _glue(toks):
    """Runs of single-character tokens (spelled letters, digits, symbols) become one token, so 'kay ay eff', 'k a f' and 'kaf' are
    the same word. Reference and hypothesis alike. (The per-document WER used for band assignment is the unit-level
    span_check.doc_wer, which does not depend on this heuristic.)"""
    out, run = [], []
    for t in toks:
        if len(t) == 1:
            run.append(t)
        else:
            if run:
                out.append("".join(run))
                run = []
            out.append(t)
    if run:
        out.append("".join(run))
    return out


def align(ref, hyp, eq=None, sub_cost=1.0):
    """Levenshtein alignment. Returns [(i|None, j|None)] in order. sub_cost > 1 prefers insert+delete around a true match over a
    substitution (used by the span checker). Ties prefer match/sub, then deletion, then insertion."""
    eq = eq or (lambda a, b: a == b)
    n, m = len(ref), len(hyp)
    D = [[0.0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        D[i][0] = float(i)
    for j in range(1, m + 1):
        D[0][j] = float(j)
    for i in range(1, n + 1):
        ri = ref[i - 1]
        row, prev = D[i], D[i - 1]
        for j in range(1, m + 1):
            c = prev[j - 1] + (0.0 if eq(ri, hyp[j - 1]) else sub_cost)
            d = prev[j] + 1.0
            ins = row[j - 1] + 1.0
            row[j] = c if c <= d and c <= ins else (d if d <= ins else ins)
    pairs = []
    i, j = n, m
    eps = 1e-9
    while i > 0 or j > 0:
        if i > 0 and j > 0 and abs(D[i][j] - (D[i - 1][j - 1] + (0.0 if eq(ref[i - 1], hyp[j - 1]) else sub_cost))) < eps:
            pairs.append((i - 1, j - 1))
            i, j = i - 1, j - 1
        elif i > 0 and abs(D[i][j] - (D[i - 1][j] + 1.0)) < eps:
            pairs.append((i - 1, None))
            i -= 1
        else:
            pairs.append((None, j - 1))
            j -= 1
    pairs.reverse()
    return pairs


def wer(ref_text, hyp_text):
    """(wer, S, D, I, n_ref) on normalised tokens. An empty reference gives wer = 0 if the hypothesis is empty, else 1."""
    r, h = normalise(ref_text), normalise(hyp_text)
    if not r:
        return (0.0 if not h else 1.0), 0, 0, len(h), 0
    pairs = align(r, h)
    S = sum(1 for a, b in pairs if a is not None and b is not None and r[a] != h[b])
    D = sum(1 for a, b in pairs if b is None)
    I = sum(1 for a, b in pairs if a is None)
    return (S + D + I) / len(r), S, D, I, len(r)


def band_of(w):
    """0..3 for the four kept WER bands, None when over 25 percent (excluded)."""
    for k, edge in enumerate(BAND_EDGES):
        if w < edge:
            return k
    return None
