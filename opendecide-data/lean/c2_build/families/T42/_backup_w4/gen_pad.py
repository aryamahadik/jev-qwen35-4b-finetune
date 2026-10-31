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
        x = float(m.replace(",", "."))
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


def add_doc(src: str, R, tg: dict):
    """Insert a docstring after the `def` line so that stats(result) == (L, N, I, M). None when infeasible."""
    lines = src.split("\n")
    if not lines[0].startswith("def ") or not lines[0].endswith(":"):
        return None
    c_len, c_n, c_ind, c_max = stats(src)
    m = tg["N"] - c_n
    if m < 3 or c_ind > tg["I"] or c_max > tg["M"]:
        return None
    B = tg["L"] - c_len                      # characters added: sum(len(line) + 1) over the docstring lines
    M, I = tg["M"], tg["I"]
    # indentation of continuation lines 2..m (multiples of 4, none beyond I; one equals I when I exceeds the core's)
    ind = [0] * m
    for j in range(1, m):
        ind[j] = 4 * R.randrange(0, I // 4 + 1)
    if I > c_ind:
        ind[R.randrange(1, m)] = I
    # per-line total length (indentation + quotes + text): first line 4 + 3 + text, last line ind + text + 3
    lo = [0] * m
    hi = [M] * m
    for j in range(m):
        base = (7 if j == 0 else ind[j]) + (3 if j == m - 1 else 0)
        lo[j] = base + 1
        if base + 1 > M:
            return None
    if B < sum(lo) + m or B > m * (M + 1):
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
        room = hi[j] - ln[j]
        if room <= 0:
            order.remove(j)
            continue
        d = min(room, need, R.randint(1, 12))
        ln[j] += d
        need -= d
    if need != 0:
        return None
    out = []
    for j in range(m):
        base = (7 if j == 0 else ind[j]) + (3 if j == m - 1 else 0)
        t = filler(R, ln[j] - base)
        pre = "    \"\"\"" if j == 0 else " " * ind[j]
        out.append(pre + t + ('"""' if j == m - 1 else ""))
    need_q = tg["Q"] - n_numbers(src)                  # numbers (digit tokens) the docstring must carry: total is exact
    if need_q < 0:
        return None
    if need_q:
        body = "\n".join(out)
        spans = [mm for mm in re.finditer(r"(?<![a-z])[a-z]{1,4}(?![a-z])", body)]
        if len(spans) < need_q:
            return None
        long_ = [mm for mm in spans if mm.end() - mm.start() >= 3]        # 3-4 digit numbers: the docstring numbers dominate
        short = [mm for mm in spans if mm.end() - mm.start() < 3]          # every magnitude feature, whatever the core holds
        pick = R.sample(long_, min(need_q, len(long_)))
        if len(pick) < need_q:
            pick += R.sample(short, need_q - len(pick))
        chosen = sorted(pick, key=lambda mm: -mm.start())
        val = []
        for mm in chosen:
            n = mm.end() - mm.start()
            val.append(R.randint(0, 9) if n == 1 else R.randint(10 ** (n - 1), 10 ** n - 1))
        for mm, v in zip(chosen, val):
            body = body[:mm.start()] + str(v) + body[mm.end():]
        out = body.split("\n")
    res = "\n".join([lines[0]] + out + lines[1:])
    try:
        back = ast.unparse(ast.parse(res))
    except SyntaxError:
        return None
    if back != res or stats(res) != (tg["L"], tg["N"], max(I, c_ind), M) or n_numbers(res) != tg["Q"]:
        return None
    return res
