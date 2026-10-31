"""VOICE solver B: hypothesis text helpers shared by the span checker and the WER (tokenising, filler removal, contractions).
Python 3 standard library only; imports nothing from solver A."""
import re

from vb_tables import FILLERS, LETTER_NAME, SYMBOL_WORD1, SYMBOL_PAIRS, DIGIT_WORD, NEGATION_WORDS, POLARITY_WORDS
import vb_numbers as N

_IRREGULAR = {"can't": ["can", "not"], "won't": ["will", "not"], "shan't": ["shall", "not"], "cannot": ["can", "not"], "ain't": ["is", "not"]}
_CLAUSE_END = re.compile(r"[.,;:!?]+$")


def expand_contraction(tok):
    """'don't' -> ['do', 'not']; 'cannot' -> ['can', 'not']; other tokens unchanged (as a one-element list)."""
    if tok in _IRREGULAR:
        return list(_IRREGULAR[tok])
    if tok.endswith("n't") and len(tok) > 3 and tok[:-3].isalpha():
        return [tok[:-3], "not"]
    return [tok]


def coarse_tokens(text, expand=True, split_number_hyphens=True):
    """Lower-case, split on white space, drop trailing clause punctuation, drop fillers, optionally expand negation contractions and
    split hyphenated number words ('twenty-six') and hyphenated spelled letters ('b-u-i-l-d')."""
    out = []
    for raw in text.lower().split():
        if re.fullmatch(r"[.,;:!?]+", raw):
            t = raw   # a stand-alone punctuation token is a symbol token (a dot read as a character), not clause punctuation
        else:
            t = _CLAUSE_END.sub("", raw)
        t = t.strip('"') if len(t) > 1 else t
        if not t:
            continue
        if t in FILLERS:
            continue
        if split_number_hyphens and "-" in t:
            parts = t.split("-")
            if all(p in N.NUM_WORD_SET for p in parts) and len(parts) > 1:
                out.extend(parts)
                continue
            if all(len(p) == 1 and p.isalnum() for p in parts) and len(parts) > 2:
                out.extend(parts)
                continue
        if expand:
            out.extend(expand_contraction(t))
        else:
            out.append(t)
    return out


FINE = re.compile(r"[a-z]+(?:'[a-z]+)?|\d+|[^\sa-z\d]")


def fine_count(tok):
    n = len(FINE.findall(tok))
    return n if n > 0 else 1


def is_symbolish(tok):
    """A token that is a symbol word or contains a punctuation character used in identifiers."""
    if tok in SYMBOL_WORD1:
        return True
    return any(c in tok for c in "/\\._-~#:=*@+%&|<>$^;!?'\"`()[]{},")


_EDGE_CHARS = "/\\._-~#:=*@+%&|<>$^;!?'`([{)]}"


def _joins_identifier(tok):
    """A symbol word, or a token that starts or ends with a symbol character (so a neighbouring 'no' belongs to a flag or path)."""
    if not tok:
        return False
    return tok in SYMBOL_WORD1 or tok[0] in _EDGE_CHARS or tok[-1] in _EDGE_CHARS


def negation_signature(tokens):
    """Negation words that stand alone: not part of an identifier (no symbol token or symbol character next to them) and not inside a
    spelled run. Contractions are expanded by the caller."""
    sig = []
    n = len(tokens)
    for i, t in enumerate(tokens):
        if t not in NEGATION_WORDS:
            continue
        prev_t = tokens[i - 1] if i > 0 else ""
        next_t = tokens[i + 1] if i + 1 < n else ""
        if _joins_identifier(prev_t) or _joins_identifier(next_t):
            continue
        sig.append(t)
    return sig


def polarity_signature(tokens):
    """Polarity words that stand alone (same identifier exclusion as the negation signature)."""
    sig = []
    n = len(tokens)
    for i, t in enumerate(tokens):
        if t not in POLARITY_WORDS:
            continue
        prev_t = tokens[i - 1] if i > 0 else ""
        next_t = tokens[i + 1] if i + 1 < n else ""
        if _joins_identifier(prev_t) or _joins_identifier(next_t):
            continue
        sig.append(t)
    return sorted(sig)


def alternatives(tokens):
    """Per hypothesis token (or token pair) the strings it may contribute to a folded character stream.
    Returns a list of units: (n_tokens, [alt strings])."""
    units = []
    i = 0
    n = len(tokens)
    while i < n:
        t = tokens[i]
        if i + 1 < n and (t, tokens[i + 1]) in SYMBOL_PAIRS:
            units.append((2, [t + tokens[i + 1], SYMBOL_PAIRS[(t, tokens[i + 1])]]))
            i += 2
            continue
        if t == "double" and i + 1 < n and tokens[i + 1] == "you":
            units.append((2, ["doubleyou", "w"]))
            i += 2
            continue
        alts = [t]
        if t in SYMBOL_WORD1:
            alts.append(SYMBOL_WORD1[t])
        if t in DIGIT_WORD:
            alts.append(str(DIGIT_WORD[t]))
        if t in LETTER_NAME:
            alts.append(LETTER_NAME[t])
        units.append((1, alts))
        i += 1
    return units
