"""families/T42/gen_pad.py: label-blind SHAPE of the equivalence functions (A45 pre-freeze fix).

Both functions of a pair get a docstring whose size is set by TARGETS drawn from the row key before the label exists:
the total character length, the number of lines, the maximum indentation and the longest line of each function are
hit EXACTLY, so no formatting feature (length, line count, indentation, longest line, differences between f and g) can
carry the label, whatever skeleton variant was used. The pair still goes through one ast.parse -> ast.unparse round trip
(a docstring is a statement, not a comment; the text is plain lowercase words, no digits, no quotes or backslashes).

  window(bounds, u)            map unit-interval draws to concrete targets inside the skeleton's window
  add_doc(src, R, tgt)         the function source with the docstring, or None when the targets are infeasible for it
  stats(src)                   (chars, lines, max indent, longest line)
"""
from __future__ import annotations

import ast
import math
import re

POOL = ("a go it of to in on at we us up so no by or an as be do he me my if is ox "
        "red map bag cap dot fix gap hat ink jar key lid mat net oak pad rod sun tag urn van web yak zip "
        "able area back bell bold calm clay cold dawn deep dust easy farm fast gold hill iron jump kind lake "
        "lamp mild nest open pale quiet rain safe tall unit vast warm yard zone "
        "brisk craft dream ember frost glide haven ivory jolly knack lemon merry noble olive plain quilt ridge "
        "stone tidal upper vivid weave young "
        "anchor bridge candle dagger engine forest garden hollow island jungle kettle ladder meadow narrow "
        "orchard pillow rabbit saddle timber valley window "
        "blanket compass drizzle evening fishing granite harvest lantern monsoon nursery outpost pelican "
        "quarter reliable seaside thicket").split()
BY_LEN: dict = {}
for _w in POOL:
    BY_LEN.setdefault(len(_w), []).append(_w)
MIN_W, MAX_W = min(BY_LEN), max(BY_LEN)


def filler(R, n: int) -> str:
    """Lowercase words joined by single spaces, exactly n characters (n >= 1)."""
    if n <= MAX_W:
        return R.choice(BY_LEN[n])
    while True:
        w = R.choice([x for x in BY_LEN if 2 <= x <= 7])
        if n - w - 1 >= 1:
            return R.choice(BY_LEN[w]) + " " + filler(R, n - w - 1)


NUM_RE = re.compile(r"\d+(?:[.,]\d+)?")


def n_numbers(src: str) -> int:
    return len(NUM_RE.findall(src))


def mag_sum(src: str) -> float:
    """Sum of the pilot's number magnitudes (log10 |x|, 0 for zero) over the numbers of a source."""
    t = 0.0
    for m in NUM_RE.findall(src):
        x = float(m.replace(",", ""))
        t += math.log10(abs(x)) if x else 0.0
    return t


def goal_cap(lens) -> float:
    return sum(0.95 if n == 1 else n - 0.0001 for n in lens)


def stats(src: str) -> tuple:
    lines = src.split("\n")
    ind = [len(x) - len(x.lstrip(" ")) for x in lines if x.strip()]
    return len(src), len(lines), max(ind) if ind else 0, max(len(x) for x in lines)


def window(b: dict, u: dict) -> dict:
    """Targets inside the skeleton window b = {L, N, I, M} (bounds of the unshaped functions) from draws u in [0, 1)."""
    N = b["N"] + 3 + int(u["n"] * 4)                                  # lines: docstring has >= 3 lines
    I = b["I"] + 4 * int(u["i"] * 2)                                   # max indentation: bound or bound + 4
    M = b["M"] + 10 + int(u["m"] * 31)                                 # longest line
    L = b["L"] + 16 * (N - 1) + int(u["l"] * 90)                       # total characters (room for >= N-1 doc lines)
    return {"L": L, "N": N, "I": I, "M": M, "Q": b["Q"] + 3 + int(u["q"] * 5), "S": b["S"] + 1.6 * (3 + int(u["q"] * 5)) + 0.8 * u["s"]}


def _split_rest(R, total: float, caps: list) -> list:
    """Split `total` into len(caps) shares in [0, cap_i] by random weights; the leftover of clipped shares goes to the others."""
    n = len(caps)
    share = [0.0] * n
    free = list(range(n))
    left = total
    for _ in range(n + 2):
        if not free or left <= 1e-12:
            break
        w = [R.random() + 0.15 for _ in free]
        tw = sum(w)
        nxt = []
        spent = 0.0
        for i, wi in zip(free, w):
            give = min(caps[i] - share[i], left * wi / tw)
            share[i] += give
            spent += give
            if caps[i] - share[i] > 1e-9:
                nxt.append(i)
        left -= spent
        free = nxt
    return share if left < 1e-6 else None


def add_doc(src: str, R, tg: dict, words=()):
    """Insert a docstring after the `def` line so that stats(result) == (L, N, I, M), n_numbers(result) == Q and the sum of the
    number magnitudes is S (+- 0.02). `words` (the skeleton vocabulary missing from the code) are placed whole in the text.
    None when infeasible for this draw (the caller retries another attempt)."""
    lines = src.split("\n")
    if not lines[0].startswith("def ") or not lines[0].endswith(":"):
        return None
    c_len, c_n, c_ind, c_max = stats(src)
    m = tg["N"] - c_n
    if m < 3 or c_ind > tg["I"] or c_max > tg["M"]:
        return None
    M, I = tg["M"], tg["I"]
    for _try in range(40):
        res = _try_doc(src, lines, R, tg, list(words), m, M, I, c_len, c_ind)
        if res is not None:
            return res
    return None


def _try_doc(src, lines, R, tg, words, m, M, I, c_len, c_ind):
    B = tg["L"] - c_len                      # characters added: sum(len(line) + 1) over the docstring lines
    ind = [0] * m
    for j in range(1, m):
        ind[j] = 4 * R.randrange(0, I // 4 + 1)
    if I > c_ind:
        ind[R.randrange(1, m)] = I
    base = [(7 if j == 0 else ind[j]) + (3 if j == m - 1 else 0) for j in range(m)]
    lo = [b + 1 for b in base]
    if any(x > M for x in lo) or B < sum(lo) + m or B > m * (M + 1):
        return None
    ln = list(lo)
    need = B - m - sum(lo)
    star = R.randrange(m)                    # the longest line hits M exactly
    need -= M - ln[star]
    ln[star] = M
    if need < 0:
        return None
    order = [j for j in range(m) if j != star]
    guard = 0
    while need > 0 and order and guard < 10000:
        guard += 1
        j = R.choice(order)
        room = M - ln[j]
        if room <= 0:
            order.remove(j)
            continue
        d = min(room, need, R.randint(1, 12))
        ln[j] += d
        need -= d
    if need != 0:
        return None
    cap = [ln[j] - base[j] for j in range(m)]          # text characters of each docstring line
    # vocabulary words go whole into random lines (one space between items)
    put = [[] for _ in range(m)]
    used = [0] * m
    ws = list(words)
    R.shuffle(ws)
    for w in sorted(ws, key=lambda x: -len(x)):
        ok = [j for j in range(m) if cap[j] - used[j] - (1 if put[j] else 0) >= len(w) + (1 if put[j] else 0)]
        if not ok:
            return None
        j = R.choice(ok)
        used[j] += len(w) + (1 if put[j] else 0)
        put[j].append(w)
    segs = []                                          # per line: [(text, is_filler)]
    for j in range(m):
        rem = cap[j] - used[j]
        items = [(w, False) for w in put[j]]
        R.shuffle(items)
        if rem:
            if put[j]:
                if rem < 2:
                    return None
                items.insert(R.randrange(len(items) + 1), (filler(R, rem - 1), True))
            else:
                items.append((filler(R, rem), True))
        segs.append(items)
    # numbers: the vocabulary digits are already in; the rest are filler words replaced by digit strings of the same width
    vtxt = " ".join(w for j in range(m) for w in put[j])
    q_v, s_v = n_numbers(vtxt), mag_sum(vtxt)
    q_need = tg["Q"] - n_numbers(src) - q_v
    T = tg["S"] - mag_sum(src) - s_v
    if q_need < 1 or T < 3.0:
        return None
    spans = []                                         # (line, item, start, width)
    for j in range(m):
        for it, (t, isf) in enumerate(segs[j]):
            if isf:
                for mm in re.finditer(r"(?<![a-z])[a-z]{1,4}(?![a-z])", t):
                    spans.append((j, it, mm.start(), mm.end() - mm.start()))
    four = [x for x in spans if x[3] == 4]
    if not four or len(spans) < q_need:
        return None
    first = R.choice(four)                             # a 4-digit number (>= 1000) dominates every magnitude feature
    rest = [x for x in spans if x is not first]
    R.shuffle(rest)
    pick = rest[:q_need - 1]
    spare = rest[q_need - 1:]
    caps = lambda ps: [x[3] - 1e-4 for x in ps]        # noqa: E731
    guard = 0
    while sum(caps(pick)) < T - 4.0 and spare and guard < 200:
        guard += 1
        wi = min(range(len(pick)), key=lambda i: pick[i][3]) if pick else None
        wj = max(range(len(spare)), key=lambda i: spare[i][3])
        if wi is None or spare[wj][3] <= pick[wi][3]:
            break
        pick[wi], spare[wj] = spare[wj], pick[wi]
    cs = caps(pick)
    lo1 = max(3.0, T - sum(cs))
    hi1 = min(3.97, T)
    if lo1 > hi1:
        return None
    m1 = R.uniform(lo1, hi1)
    sh = _split_rest(R, T - m1, cs) if pick else ([] if T - m1 < 1e-6 else None)
    if sh is None:
        return None
    vals, tot = [], 0.0
    for x, mg in zip(pick, sh):
        v = max(0, min(10 ** x[3] - 1, int(round(10 ** mg))))
        v = v if v >= 2 else R.randint(0, 1) if mg < 0.15 else v
        vals.append(v)
        tot += math.log10(v) if v else 0.0
    v1 = int(round(10 ** (T - tot)))
    if not 1000 <= v1 <= 9999:
        return None
    rep = {}
    for x, v in [(first, v1)] + list(zip(pick, vals)):
        rep.setdefault((x[0], x[1]), []).append((x[2], x[3], str(v).zfill(x[3])))
    out = []
    for j in range(m):
        parts = []
        for it, (t, isf) in enumerate(segs[j]):
            for st, wd, dg in sorted(rep.get((j, it), []), reverse=True):
                t = t[:st] + dg + t[st + wd:]
            parts.append(t)
        text = " ".join(parts)
        out.append(("    \"\"\"" if j == 0 else " " * ind[j]) + text + ('"""' if j == m - 1 else ""))
    res = "\n".join([lines[0]] + out + lines[1:])
    try:
        back = ast.unparse(ast.parse(res))
    except SyntaxError:
        return None
    if back != res or stats(res) != (tg["L"], tg["N"], max(I, c_ind), M) or n_numbers(res) != tg["Q"] \
            or abs(mag_sum(res) - tg["S"]) > 0.02:
        return None
    return res
