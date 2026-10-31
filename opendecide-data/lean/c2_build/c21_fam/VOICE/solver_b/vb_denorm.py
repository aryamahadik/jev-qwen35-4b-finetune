"""VOICE solver B, component 1: the independent DENORMALISER (gate V-C1). Written from VOICE/SCHEMA.md section 2 only.

    denormalise(view) -> list[str]     view = {tokens, segments: [{kind, tok:[a,b), src, style}], stratum}
Returns the written source tokens (lower case), in order, recovered from the spoken tokens and the segment map alone. Python 3
standard library only; imports nothing from solver A.
"""
from vb_tables import LETTER_NAME, SYMBOL_PHRASE, DIGIT_WORD, DOUBLE_YOU
import vb_numbers as N


class DenormError(Exception):
    pass


def _spelled(words):
    out = []
    i = 0
    while i < len(words):
        w = words[i]
        if w == "capital":
            i += 1
            continue
        if w == DOUBLE_YOU[0] and i + 1 < len(words) and words[i + 1] == DOUBLE_YOU[1]:
            out.append("w")
            i += 2
            continue
        if w in LETTER_NAME:
            out.append(LETTER_NAME[w])
            i += 1
            continue
        if len(w) == 1 and w.isalpha():   # a plain single letter is its own reading
            out.append(w)
            i += 1
            continue
        raise DenormError("spelled token not a letter name: %r" % w)
    return "".join(out)


def _digits(words):
    d = N.digits_string(words, allow_oh=False)
    if d is None:
        raise DenormError("digit words expected: %r" % (words,))
    return d


def _sym(words):
    key = tuple(words)
    if key in SYMBOL_PHRASE:
        return SYMBOL_PHRASE[key]
    out = []
    i = 0
    while i < len(words):   # a symbol segment can hold several symbols (defensive)
        if i + 1 < len(words) and (words[i], words[i + 1]) in SYMBOL_PHRASE:
            out.append(SYMBOL_PHRASE[(words[i], words[i + 1])])
            i += 2
        elif (words[i],) in SYMBOL_PHRASE:
            out.append(SYMBOL_PHRASE[(words[i],)])
            i += 1
        else:
            raise DenormError("symbol words expected: %r" % (words,))
    return "".join(out)


def _need(v, what, words):
    if v is None:
        raise DenormError("%s not readable: %r" % (what, words))
    return v


def _number_base(style, words):
    """Base styles: cardinal digits year decimal cardinal_frac version ordinal date. Returns a string."""
    if style == "cardinal":
        return str(_need(N.cardinal_value(words), "cardinal", words))
    if style == "digits":
        return _digits(words)
    if style == "year":
        return str(_need(N.year_value(words), "year", words))
    if style in ("decimal", "cardinal_frac"):
        if "point" not in words:
            raise DenormError("decimal without point: %r" % (words,))
        k = words.index("point")
        ip = words[:k]
        fp = words[k + 1:]
        i_val = N.cardinal_value(ip)
        if i_val is None:
            i_str = N.digits_string(ip, allow_oh=False)
            if i_str is None:
                raise DenormError("decimal integer part: %r" % (words,))
        else:
            i_str = str(i_val)
        if style == "decimal":
            f_str = _digits(fp)
        else:
            lead = 0
            rest = list(fp)
            while len(rest) > 1 and rest[0] in ("zero", "oh"):
                lead += 1
                rest = rest[1:]
            cf = N.cardinal_value(rest)
            if cf is None:
                raise DenormError("fraction not a cardinal: %r" % (words,))
            f_str = "0" * lead + str(cf)
        return i_str + "." + f_str
    if style == "version":
        parts, cur = [], []
        for w in words:
            if w == "point":
                parts.append(cur)
                cur = []
            else:
                cur.append(w)
        parts.append(cur)
        out = []
        for p in parts:
            v = N.cardinal_value(p)
            if v is None:
                d = N.digits_string(p, allow_oh=False)
                if d is None:
                    raise DenormError("version part not readable: %r" % (p,))
                out.append(d)
            else:
                out.append(str(v))
        return ".".join(out)
    if style == "ordinal":
        v = _need(N.ordinal_value(words), "ordinal", words)
        return str(v) + N.ordinal_suffix(v)
    if style == "date":
        return _need(N.spoken_date_to_iso(words), "date", words)
    raise DenormError("unknown number style %r" % style)


def _number(style, words):
    """Peel prefixes comma_ / pct_ / neg_ (any order), read the base style, put the wrappers back."""
    flags = []
    st = style
    ws = list(words)
    while True:
        for p in ("comma_", "pct_", "neg_"):
            if st.startswith(p):
                flags.append(p)
                st = st[len(p):]
                break
        else:
            break
    neg = pct = comma = False
    if "neg_" in flags:
        neg = True
        if not ws or ws[0] not in ("minus", "negative"):
            raise DenormError("neg without minus: %r" % (words,))
        ws = ws[1:]
    if "pct_" in flags:
        pct = True
        if not ws or ws[-1] != "percent":
            raise DenormError("pct without percent: %r" % (words,))
        ws = ws[:-1]
    if "comma_" in flags:
        comma = True
    body = _number_base(st, ws)
    if comma:
        ip, dot, fp = body.partition(".")
        body = N.group_commas(ip) + dot + fp
    return ("-" if neg else "") + body + ("%" if pct else "")


def invert_segment(kind, style, words):
    words = [w.lower() for w in words]
    if kind == "word" or kind == "word_hyphen":
        if style in ("hyphen", "word_hyphen") or kind == "word_hyphen":
            return "-".join(words)
        return " ".join(words)
    if kind == "spelled":
        return _spelled(words)
    if kind == "digits":
        return _digits(words)
    if kind == "sym":
        return _sym(words)
    if kind == "number":
        return _number(style, words)
    if kind == "disfl":
        return ""
    raise DenormError("unknown segment kind %r" % kind)


def denormalise(view):
    toks = view["tokens"]
    by_src = {}
    order = []
    for seg in view["segments"]:
        a, b = seg["tok"]
        text = invert_segment(seg["kind"], seg.get("style", ""), toks[a:b])
        src = seg.get("src")
        if src is None:
            continue
        if src not in by_src:
            by_src[src] = ""
            order.append(src)
        by_src[src] += text
    return [by_src[k].lower() for k in sorted(order)]


def written_reference_words(view):
    """Written reference words for the WER: denormalised source tokens in spoken order, plus the spoken disfluency words (fillers
    excluded). Used by vb_wer."""
    from vb_tables import FILLERS
    toks = view["tokens"]
    out = []
    cur = {}
    for seg in sorted(view["segments"], key=lambda g: g["tok"][0]):   # disfluency segments are listed last: order by token position
        a, b = seg["tok"]
        src = seg.get("src")
        if src is None:
            for w in toks[a:b]:
                if w.lower() not in FILLERS:
                    out.append(("disfl", w.lower()))
            continue
        text = invert_segment(seg["kind"], seg.get("style", ""), toks[a:b]).lower()
        if src not in cur:
            cur[src] = len(out)
            out.append(("src", text))
        else:
            k = cur[src]
            out[k] = ("src", out[k][1] + text)
    return [w for _k, w in out]
