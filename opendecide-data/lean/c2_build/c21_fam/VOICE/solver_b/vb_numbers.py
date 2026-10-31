"""VOICE solver B: number-form normaliser (spoken words <-> canonical strings). Written by solver B from plain English and
VOICE/SCHEMA.md sections 2 and 3. Python 3 standard library only. Imports NOTHING from solver A."""
import re

from vb_tables import (DIGIT_WORD, TEENS, TENS, SCALES, UNITS_TO_19, ORDINAL_WORD, MONTH, MONTH_ABBR)

NUM_WORD_SET = set(UNITS_TO_19) | set(TENS) | set(SCALES) | set(ORDINAL_WORD)

_ORD_TO_CARD_WORD = {}   # "seventh" -> "seven" style stems are not needed: ORDINAL_WORD maps straight to values


# ---------------------------------------------------------------------------------------------------------------------
# cardinals

def cardinal_value(words, allow_and=False):
    """Strict English cardinal (0 <= n < 10**12) from a word list, or None. 'and' is accepted only when allow_and."""
    ws = list(words)
    if not ws:
        return None
    if allow_and:
        ws2 = []
        for i, w in enumerate(ws):
            if w == "and" and i > 0 and ws[i - 1] in ("hundred", "thousand", "million") and i + 1 < len(ws):
                continue
            ws2.append(w)
        ws = ws2
    if "zero" in ws:
        return 0 if ws == ["zero"] else None
    total = 0
    current = 0
    last_scale = 10 ** 12
    for w in ws:
        if w in UNITS_TO_19:
            v = UNITS_TO_19[w]
            r = current % 100
            if r == 0:
                current += v
            elif r >= 20 and r % 10 == 0 and 1 <= v <= 9:
                current += v
            else:
                return None
        elif w in TENS:
            if current % 100 != 0:
                return None
            current += TENS[w]
        elif w == "hundred":
            if not (1 <= current <= 9):
                return None
            current *= 100
        elif w in ("thousand", "million", "billion"):
            sc = SCALES[w]
            if sc >= last_scale or not (1 <= current <= 999):
                return None
            total += current * sc
            current = 0
            last_scale = sc
        else:
            return None
    return total + current


def digits_string(words, allow_oh=False):
    out = []
    for w in words:
        if w in DIGIT_WORD:
            out.append(str(DIGIT_WORD[w]))
        elif allow_oh and w == "oh":
            out.append("0")
        else:
            return None
    return "".join(out) if out else None


# ---------------------------------------------------------------------------------------------------------------------
# ordinals and years

def ordinal_suffix(n):
    if 11 <= n % 100 <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def ordinal_value(words):
    """['thirty', 'seventh'] -> 37; ['twelfth'] -> 12; ['one', 'hundredth'] -> 100; else None."""
    if not words:
        return None
    last = words[-1]
    if last not in ORDINAL_WORD:
        return None
    ov = ORDINAL_WORD[last]
    head = words[:-1]
    if not head:
        return ov
    # 'hundredth' / 'thousandth' take a multiplier: 'one hundred first' is [one, hundred, first]
    if ov in (100, 1000, 1000000):
        c = cardinal_value(head)
        return None if c is None else c * ov
    c = cardinal_value(head)
    if c is None:
        return None
    # the head must end a multiple of ten or a scale so that the ordinal fits ('thirty seventh', 'one hundred first')
    if ov < 10:
        if c % 10 != 0 or (c % 100) in range(10, 20):
            return None
        return c + ov
    if ov < 20:
        if c % 100 != 0:
            return None
        return c + ov
    return None if c % 100 != 0 else c + ov


def year_value(words):
    """Spoken years: [twenty twenty six]=2026, [two thousand five]=2005, [nineteen oh five]=1905, [eleven hundred]=1100,
    [nineteen ninety nine]=1999. Returns an int or None."""
    n = len(words)
    if n == 0:
        return None
    # thousands forms: <digit> thousand [rest]
    if n >= 2 and words[1] == "thousand" and words[0] in DIGIT_WORD:
        rest = words[2:]
        if not rest:
            return DIGIT_WORD[words[0]] * 1000
        c = cardinal_value(rest)
        if c is not None and c < 1000:
            return DIGIT_WORD[words[0]] * 1000 + c
        return None
    cand = set()
    for k in range(1, n):
        first = cardinal_value(words[:k])
        if first is None or not (10 <= first <= 99):
            continue
        rest = words[k:]
        if rest == ["hundred"]:
            cand.add(first * 100)
            continue
        if rest[0] in ("oh", "zero") and len(rest) == 2 and rest[1] in DIGIT_WORD and rest[1] != "zero":
            cand.add(first * 100 + DIGIT_WORD[rest[1]])
            continue
        second = cardinal_value(rest)
        if second is not None and 10 <= second <= 99:
            cand.add(first * 100 + second)
    if len(cand) == 1:
        return next(iter(cand))
    return None


def group_commas(int_digits):
    s = int_digits
    out = []
    while len(s) > 3:
        out.insert(0, s[-3:])
        s = s[:-3]
    out.insert(0, s)
    return ",".join(out)


# ---------------------------------------------------------------------------------------------------------------------
# dates

def iso_from(y, m, d):
    return "%04d-%02d-%02d" % (y, m, d)


def _day_from(tokens, i):
    """Day of month starting at tokens[i]: returns (day, next_index) or None. Accepts 14, 14th, fourteenth, twenty second."""
    if i >= len(tokens):
        return None
    t = tokens[i]
    m = re.match(r"^(\d{1,2})(?:st|nd|rd|th)?$", t)
    if m and 1 <= int(m.group(1)) <= 31:
        return int(m.group(1)), i + 1
    if t in ORDINAL_WORD:
        v = ORDINAL_WORD[t]
        if 1 <= v <= 31:
            return v, i + 1
    if t in TENS and i + 1 < len(tokens) and tokens[i + 1] in ORDINAL_WORD:
        v = ordinal_value([t, tokens[i + 1]])
        if v is not None and 1 <= v <= 31:
            return v, i + 2
    return None


def _year_from(tokens, i):
    """Year starting at tokens[i]: returns (year, next_index) or None. Prefers the longest year reading."""
    if i >= len(tokens):
        return None
    t = tokens[i]
    if re.match(r"^\d{4}$", t):
        return int(t), i + 1
    best = None
    for L in (5, 4, 3, 2, 1):
        if i + L <= len(tokens):
            v = year_value(tokens[i:i + L])
            if v is not None and 1000 <= v <= 2999:
                best = (v, i + L)
                break
    return best


def find_dates(tokens):
    """All date items in a token list: [(start, end, iso)] non-overlapping, left to right."""
    out = []
    i = 0
    n = len(tokens)
    while i < n:
        t = tokens[i]
        m = re.match(r"^(\d{4})-(\d\d)-(\d\d)$", t)
        if m:
            out.append((i, i + 1, t))
            i += 1
            continue
        month = MONTH.get(t) or MONTH_ABBR.get(t)
        if month:
            d = _day_from(tokens, i + 1)
            if d:
                y = _year_from(tokens, d[1])
                if y:
                    out.append((i, y[1], iso_from(y[0], month, d[0])))
                    i = y[1]
                    continue
        d = _day_from(tokens, i)
        if d:
            j = d[1]
            if j < n and tokens[j] == "of":
                j += 1
            if j < n:
                month = MONTH.get(tokens[j]) or MONTH_ABBR.get(tokens[j])
                if month:
                    y = _year_from(tokens, j + 1)
                    if y:
                        out.append((i, y[1], iso_from(y[0], month, d[0])))
                        i = y[1]
                        continue
        i += 1
    return out


def spoken_date_to_iso(words):
    """The segment form: month, ordinal day, year words -> ISO, or None."""
    ds = find_dates(list(words))
    if len(ds) == 1 and ds[0][0] == 0 and ds[0][1] == len(words):
        return ds[0][2]
    return None


# ---------------------------------------------------------------------------------------------------------------------
# number runs in a hypothesis

WRITTEN_NUM = re.compile(r"^-?\d[\d,]*(?:\.\d+)*(?:%|st|nd|rd|th)?$")


def is_written_number(t):
    return bool(WRITTEN_NUM.match(t))


def is_number_word(t):
    return t in NUM_WORD_SET


def _canon_written(t):
    """Candidate canonical strings for ONE written numeric token (commas folded away, kept as the engine wrote the digits)."""
    out = set()
    core = t
    pct = core.endswith("%")
    if pct:
        core = core[:-1]
    suf = ""
    m = re.match(r"^(.*?)(st|nd|rd|th)$", core)
    if m and m.group(1):
        core, suf = m.group(1), m.group(2)
    nocomma = core.replace(",", "")
    s = nocomma + suf + ("%" if pct else "")
    out.add(s)
    return out


def run_candidates(words):
    """Canonical strings a maximal run of number-ish words can denote (see SCHEMA section 3). Empty set = no valid reading."""
    out = set()
    if not words:
        return out
    ws = list(words)
    if len(ws) == 1 and is_written_number(ws[0]):
        return _canon_written(ws[0])
    # sign and percent wrappers
    neg = ""
    if ws and ws[0] in ("minus", "negative"):
        neg = "-"
        ws = ws[1:]
    pct = ""
    if ws and ws[-1] == "percent":
        pct = "%"
        ws = ws[:-1]
    if not ws:
        return out
    if len(ws) == 1 and is_written_number(ws[0]) and not ws[0].startswith("-"):
        for c in _canon_written(ws[0]):
            out.add(neg + c + pct)
        return out
    if any(is_written_number(w) for w in ws):
        # a written number next to other number tokens is a longer, different number: no reading
        return out
    # split at "point"
    parts = [[]]
    for w in ws:
        if w == "point":
            parts.append([])
        else:
            parts[-1].append(w)
    if any(len(p) == 0 for p in parts):
        return out
    suffix = pct
    if len(parts) == 1:
        p = parts[0]
        c = cardinal_value(p, allow_and=True)
        if c is not None:
            out.add(neg + str(c) + suffix)
        d = digits_string(p, allow_oh=True)
        if d is not None:
            out.add(neg + d + suffix)
        y = year_value(p)
        if y is not None:
            out.add(neg + str(y) + suffix)
        o = ordinal_value(p)
        if o is not None and not neg and not pct:
            out.add(str(o) + ordinal_suffix(o))
        return out
    if len(parts) == 2:
        ipart = parts[0]
        ints = set()
        c = cardinal_value(ipart, allow_and=True)
        if c is not None:
            ints.add(str(c))
        d = digits_string(ipart, allow_oh=True)
        if d is not None:
            ints.add(d)
        fr = set()
        ds = digits_string(parts[1], allow_oh=True)
        if ds is not None:
            fr.add(ds)
        # cardinal fraction, with optional leading zero words
        lead = 0
        rest = parts[1]
        while rest and rest[0] in ("zero", "oh") and len(rest) > 1:
            lead += 1
            rest = rest[1:]
        cf = cardinal_value(rest)
        if cf is not None and not (rest == ["zero"] and lead):
            fr.add("0" * lead + str(cf))
        for a in ints:
            for b in fr:
                out.add(neg + a + "." + b + suffix)
        return out
    # version: every part is a cardinal or a digit string
    opts = []
    for p in parts:
        o = set()
        c = cardinal_value(p, allow_and=True)
        if c is not None:
            o.add(str(c))
        d = digits_string(p, allow_oh=True)
        if d is not None:
            o.add(d)
        if not o:
            return out
        opts.append(o)
    cur = [""]
    for k, o in enumerate(opts):
        cur = [(a + ("." if k else "") + b) for a in cur for b in o]
    for s in cur:
        out.add(neg + s + suffix)
    return out


def split_runs(tokens):
    """Indices of maximal runs of number WORDS: [(start, end)]. A written number token (digits) is always an item of its own and
    never joins a run. 'point' joins a run only between two number tokens; 'and' only between number words; 'oh' / 'o' only next to
    another number-word token; 'percent' closes a run (or a written number)."""
    n = len(tokens)
    isnum = [False] * n
    for i, t in enumerate(tokens):
        if is_number_word(t) or t in ("minus", "negative"):
            isnum[i] = True
    for i, t in enumerate(tokens):
        if t == "point" and 0 < i < n - 1 and isnum[i - 1] and (is_number_word(tokens[i + 1]) or tokens[i + 1] in ("oh", "zero")):
            isnum[i] = True
    for i, t in enumerate(tokens):
        if t == "oh":
            prev_num = i > 0 and (isnum[i - 1] and tokens[i - 1] != "minus")
            next_num = i < n - 1 and isnum[i + 1] and tokens[i + 1] not in ("point", "minus")
            if prev_num or next_num:
                isnum[i] = True
    for i, t in enumerate(tokens):
        if t == "percent" and i > 0 and isnum[i - 1]:
            isnum[i] = True
    runs = []
    i = 0
    while i < n:
        if isnum[i]:
            j = i
            while j < n and isnum[j]:
                j += 1
            runs.append((i, j))
            i = j
        else:
            i += 1
    return runs


def hyp_number_items(tokens):
    """Everything numeric in a hypothesis token list: dates first (consumed), then written numbers (one item each, with a following
    'percent' word read as a percent sign), then maximal runs of number words.
    Returns a list of items {kind: 'date'|'number', start, end, cands: set(str)} in order of position."""
    items = []
    consumed = [False] * len(tokens)
    for (a, b, iso) in find_dates(tokens):
        items.append({"kind": "date", "start": a, "end": b, "cands": {iso}})
        for k in range(a, b):
            consumed[k] = True
    i = 0
    n = len(tokens)
    while i < n:
        if consumed[i]:
            i += 1
            continue
        t = tokens[i]
        if is_written_number(t):
            cands = set(_canon_written(t))
            end = i + 1
            if end < n and tokens[end] == "percent" and not t.endswith("%"):
                cands |= set(c + "%" for c in _canon_written(t))
                end += 1
            items.append({"kind": "number", "start": i, "end": end, "cands": cands})
            i = end
            continue
        i += 1
    masked = [("\x00" if (consumed[k] or is_written_number(tokens[k])) else tokens[k]) for k in range(n)]
    runs = split_runs(masked)
    for (a, b) in runs:
        items.append({"kind": "number", "start": a, "end": b, "cands": run_candidates(tokens[a:b])})
    # "three thousand and fifty two": two number runs split by 'and' may also be ONE number (the British reading). The merged
    # reading is added as an alternative item that excludes its two parts (consuming one consumes the other).
    for r in range(len(runs) - 1):
        (a1, b1), (a2, b2) = runs[r], runs[r + 1]
        if b1 + 1 == a2 and tokens[b1] == "and" and tokens[b1 - 1] in ("hundred", "thousand", "million"):
            merged = set(run_candidates(tokens[a1:b1] + ["and"] + tokens[a2:b2]))
            if merged:
                items.append({"kind": "number", "start": a1, "end": b2, "cands": merged, "alt_of": [(a1, b1), (a2, b2)]})
    items.sort(key=lambda it: (it["start"], it["end"]))
    return items
