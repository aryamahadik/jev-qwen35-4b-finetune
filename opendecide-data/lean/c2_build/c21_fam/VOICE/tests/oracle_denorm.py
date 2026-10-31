"""TEST ORACLE ONLY (not solver B). Inverts a verbalized public view back to written tokens so the round-trip harness and the
verbalizer can be unit-tested. Solver B writes the real, independent denormaliser in its own session."""
import re

import numwords as NW
from vcommon import NAME_TO_LETTER, WORD_TO_SYMBOL, MULTI_SYMBOL_WORDS


def _letters(words):
    out, i = [], 0
    while i < len(words):
        if words[i] == "capital":
            i += 1
            continue
        if words[i] == "double" and i + 1 < len(words) and words[i + 1] == "you":
            out.append("w")
            i += 2
            continue
        out.append(NAME_TO_LETTER[words[i]])
        i += 1
    return "".join(out)


def _syms(words):
    for k in (2, 3):
        if tuple(words[:k]) in MULTI_SYMBOL_WORDS:
            return MULTI_SYMBOL_WORDS[tuple(words[:k])]
    return {"slash": "/", "backslash": "\\", "dot": ".", "dash": "-", "underscore": "_", "tilde": "~", "hash": "#", "colon": ":", "equals": "=", "star": "*",
            "at": "@", "plus": "+", "percent": "%", "ampersand": "&", "pipe": "|", "dollar": "$", "caret": "^", "comma": ",", "semicolon": ";", "bang": "!",
            "apostrophe": "'", "quote": '"', "backtick": "`"}[words[0]]


def _number(words, style):
    if style.startswith("comma_"):
        v = _number(words, style[6:])
        ip, _, fp = v.partition(".")
        g = "{:,}".format(int(ip))
        return g + ("." + fp if fp else "")
    if style.startswith("pct_"):
        return _number(words[:-1], style[4:]) + "%"
    if style.startswith("neg_"):
        return "-" + _number(words[1:], style[4:])
    if style == "digits":
        return "".join(NW.WORD_DIGIT[w] for w in words)
    if style == "ordinal":
        n = sorted(NW.parse_number_tokens(words), key=len)[0]
        suf = "th" if 10 <= int(n) % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(int(n) % 10, "th")
        return n + suf
    if style == "date":
        mo = NW.MONTHS.index(words[0]) + 1
        rest = words[1:]
        for cut in range(1, len(rest)):
            d = NW.parse_number_tokens(rest[:cut])
            y = NW.parse_number_tokens(rest[cut:])
            if d and y:
                dd, yy = sorted(d, key=len)[0], sorted(y, key=len)[-1]
                if len(yy) == 4 and 1 <= int(dd) <= 31:
                    return "%s-%02d-%02d" % (yy, mo, int(dd))
        raise ValueError("date")
    c = NW.parse_number_tokens(words)
    if style in ("year",):
        c = {x for x in c if len(x) == 4} or c
    return sorted(c, key=lambda x: (len(x), x))[-1] if style == "year" else sorted(c, key=len)[0]


def denormalise(view):
    toks, segs = view["tokens"], view["segments"]
    by_src = {}
    for s in segs:
        if s["src"] is None:
            continue
        by_src.setdefault(s["src"], []).append(s)
    out = []
    for si in sorted(by_src):
        piece = ""
        parts = sorted(by_src[si], key=lambda s: s["tok"][0])
        if len(parts) == 1 and parts[0]["kind"] == "number":
            out.append(_number(toks[parts[0]["tok"][0]:parts[0]["tok"][1]], parts[0]["style"]))
            continue
        for s in parts:
            w = toks[s["tok"][0]:s["tok"][1]]
            k = s["kind"]
            if k == "word":
                piece += "-".join(w) if s["style"] == "word_hyphen" else "".join(w)
            elif k == "spelled":
                piece += _letters(w)
            elif k == "digits":
                piece += "".join(NW.WORD_DIGIT[x] for x in w)
            elif k == "sym":
                piece += _syms(w)
            elif k == "number":
                piece += _number(w, s["style"])
        out.append(piece)
    return out
