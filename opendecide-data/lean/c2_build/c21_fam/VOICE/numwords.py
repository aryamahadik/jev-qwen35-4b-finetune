"""Number words, both directions (solver A side). CPU only, no third-party package.

forward:  cardinal / ordinal / digit-by-digit / decimal / version / year  -> list of spoken word tokens
backward: parse_number_tokens(tokens) -> set of canonical candidate strings ("443", "3.11", "2026", "5" ...)
The backward direction is used by the span-survival checker (a hypothesis may write digits, a cardinal, or digits one by one).
"""
import re

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
        "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
DIGIT_WORD = {str(i): ONES[i] for i in range(10)}
WORD_DIGIT = {w: str(i) for i, w in enumerate(ONES[:10])}
DIGIT_STRICT = dict(WORD_DIGIT)            # zero..nine only: used by the skeleton and the aligner (the letter 'o' is not a digit)
WORD_DIGIT["oh"] = "0"
WORD_DIGIT["o"] = "0"
WORD_DIGIT["nought"] = "0"
ORD_IRREG = {"one": "first", "two": "second", "three": "third", "five": "fifth", "eight": "eighth", "nine": "ninth", "twelve": "twelfth"}
ORD_REV = {v: k for k, v in ORD_IRREG.items()}
SCALES = [(10 ** 9, "billion"), (10 ** 6, "million"), (1000, "thousand")]
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
NUM_WORDS = set(ONES) | {t for t in TENS if t} | {"hundred", "thousand", "million", "billion", "oh", "point", "and"} | set(ORD_REV) | {"o"}


def cardinal(n):
    """0 <= n < 10**12 -> list of words ('one hundred twenty three'; no 'and')."""
    if n < 0:
        return ["minus"] + cardinal(-n)
    if n < 20:
        return [ONES[n]]
    if n < 100:
        return [TENS[n // 10]] + ([ONES[n % 10]] if n % 10 else [])
    if n < 1000:
        return [ONES[n // 100], "hundred"] + (cardinal(n % 100) if n % 100 else [])
    for val, name in SCALES:
        if n >= val:
            return cardinal(n // val) + [name] + (cardinal(n % val) if n % val else [])
    raise ValueError(n)


def ordinal(n):
    w = cardinal(n)
    last = w[-1]
    if last in ORD_IRREG:
        w[-1] = ORD_IRREG[last]
    elif last.endswith("y"):
        w[-1] = last[:-1] + "ieth"
    elif last == "hundred" or last in ("thousand", "million", "billion"):
        w[-1] = last + "th"
    else:
        w[-1] = last + "th"
    return w


def digit_words(s):
    return [DIGIT_WORD[c] for c in s if c.isdigit()]


def decimal_words(s, frac_style="digits"):
    """'3.25' -> three point two five. frac_style 'cardinal' reads the fraction as a number ('three point twenty five')."""
    ip, fp = s.split(".")
    out = cardinal(int(ip)) + ["point"]
    out += digit_words(fp) if frac_style == "digits" else cardinal(int(fp))
    return out


def version_words(s):
    """'3.11' -> three point eleven; '3.11.2' -> three point eleven point two (each part read as a cardinal)."""
    parts = s.split(".")
    out = []
    for i, p in enumerate(parts):
        if i:
            out.append("point")
        out += cardinal(int(p)) if (len(p) <= 2 and not (len(p) == 2 and p[0] == "0")) else digit_words(p)
    return out


def year_words(y):
    """1100..2099 as spoken years: 2026 -> twenty twenty six; 2005 -> two thousand five; 1900 -> nineteen hundred."""
    if 2000 <= y <= 2009:
        return ["two", "thousand"] + (cardinal(y - 2000) if y > 2000 else [])
    a, b = divmod(y, 100)
    if b == 0:
        return cardinal(a) + ["hundred"]
    return cardinal(a) + (["oh"] + cardinal(b) if b < 10 else cardinal(b))


# ------------------------------------------------------------------------------------------------
# backward: tokens -> candidate canonical strings
# ------------------------------------------------------------------------------------------------
_DIGITS = re.compile(r"^\d+(?:[.,]\d+)*$")
_ORD_DIGITS = re.compile(r"^(\d+)(?:st|nd|rd|th)$")


def _parse_group(tokens):
    """0..999 with a strict grammar: [ones hundred] [and] (teen | ones | tens [ones])."""
    toks = [t for t in tokens]
    if not toks:
        return None
    i, val = 0, 0
    if len(toks) >= 2 and toks[0] in ONES[1:10] and toks[1] == "hundred":
        val = ONES.index(toks[0]) * 100
        i = 2
        if i < len(toks) and toks[i] == "and":
            i += 1
    rest = toks[i:]
    if not rest:
        return val if i else None
    if len(rest) == 1:
        t = rest[0]
        if t in ONES:
            if t == "zero" and (val or len(toks) > 1):
                return None
            return val + ONES.index(t)
        if t in TENS and t:
            return val + TENS.index(t) * 10
        return None
    if len(rest) == 2 and rest[0] in TENS and rest[0] and rest[1] in ONES[1:10]:
        return val + TENS.index(rest[0]) * 10 + ONES.index(rest[1])
    return None


def _parse_cardinal(tokens):
    """tokens (lower) -> int or None. Strict grammar (groups of three digits, scales descending). Does not accept 'point'."""
    toks = [t for t in tokens if t != "and" or False]
    raw = list(tokens)
    if not raw:
        return None
    total, last_scale, buf = 0, 10 ** 12, []
    scale_val = {"thousand": 1000, "million": 10 ** 6, "billion": 10 ** 9}
    for t in raw:
        if t in scale_val:
            g = _parse_group(buf)
            if g is None or scale_val[t] >= last_scale:
                return None
            total += g * scale_val[t]
            last_scale = scale_val[t]
            buf = []
        else:
            buf.append(t)
    if buf:
        # an 'and' after a scale word ('one thousand and five') is allowed
        if buf and buf[0] == "and" and last_scale < 10 ** 12:
            buf = buf[1:]
        g = _parse_group(buf)
        if g is None:
            return None
        total += g
    elif last_scale == 10 ** 12:
        return None
    return total


def _ordinal_to_cardinal_tokens(tokens):
    if not tokens:
        return None
    last = tokens[-1]
    if last in ORD_REV:
        return tokens[:-1] + [ORD_REV[last]]
    if last.endswith("ieth") and last[:-4] + "y" in TENS:
        return tokens[:-1] + [last[:-4] + "y"]
    for suf in ("hundredth", "thousandth", "millionth", "billionth"):
        if last == suf:
            return tokens[:-1] + [suf[:-2]]
    if last.endswith("th") and last[:-2] in ONES + [t for t in TENS if t]:
        return tokens[:-1] + [last[:-2]]
    return None


def parse_number_tokens(tokens):
    """Set of canonical strings the token sequence can denote. Empty set = not a number."""
    toks = [t.lower().strip() for t in tokens if t.strip()]
    out = set()
    if not toks:
        return out
    if len(toks) == 1:
        t = toks[0]
        if _DIGITS.match(t):
            out.add(t.replace(",", "") if re.match(r"^\d{1,3}(,\d{3})+(\.\d+)?$", t) else t)
            out.add(t)
        m = _ORD_DIGITS.match(t)
        if m:
            out.add(m.group(1))
        if t.endswith("%") and _DIGITS.match(t[:-1]):
            out.add(t[:-1])
    # digit by digit (also digit words mixed with digit chars)
    if all(t in WORD_DIGIT or (t.isdigit() and len(t) == 1) for t in toks):
        out.add("".join(WORD_DIGIT.get(t, t) for t in toks))
    # decimals / versions: a 'point' splits integer and fraction parts
    if "point" in toks:
        parts, cur = [], []
        for t in toks:
            if t == "point":
                parts.append(cur)
                cur = []
            else:
                cur.append(t)
        parts.append(cur)
        ok, pieces = True, []
        for i, p in enumerate(parts):
            if not p:
                ok = False
                break
            if i == 0:
                v = _parse_cardinal(p)
                if v is None and all(t in WORD_DIGIT for t in p):
                    pieces.append("".join(WORD_DIGIT[t] for t in p))
                elif v is None:
                    ok = False
                else:
                    pieces.append(str(v))
            else:
                if all(t in WORD_DIGIT for t in p):
                    pieces.append("".join(WORD_DIGIT[t] for t in p))
                else:
                    v = _parse_cardinal(p)
                    if v is None:
                        ok = False
                        break
                    pieces.append(str(v))
        if ok:
            out.add(".".join(pieces))
        return out
    v = _parse_cardinal(toks)
    if v is not None:
        out.add(str(v))
    o = _ordinal_to_cardinal_tokens(toks)
    if o is not None:
        v = _parse_cardinal(o)
        if v is not None:
            out.add(str(v))
    if len(toks) >= 2 and toks[-1] == "hundred":
        a = _parse_cardinal(toks[:-1])
        if a is not None and 10 <= a <= 99:
            out.add(str(a * 100))
    # year style: 'twenty twenty six', 'nineteen ninety nine', 'nineteen oh five', 'two thousand five'
    for cut in range(1, len(toks)):
        a, b = toks[:cut], toks[cut:]
        va = _parse_cardinal(a)
        if b[0] in ("oh", "o") and len(b) > 1:
            vb = _parse_cardinal(b[1:])
            if va is not None and vb is not None and 10 <= va <= 99 and 1 <= vb <= 9:
                out.add("%d0%d" % (va, vb))
        else:
            vb = _parse_cardinal(b)
            if va is not None and vb is not None and 10 <= va <= 99 and 10 <= vb <= 99:
                out.add("%d%02d" % (va, vb))
    return out
