"""c2_kit/glob_a.py: glob matching by token AST and memoised search (solver-A side; see globsem.py).

The pattern becomes a token list (LIT c, STAR, DSTAR, QMARK, END); match() runs a memoised search over (token index,
subject index). Written without regular expressions so glob_b.py (regex compile) is an independent implementation.
"""
from __future__ import annotations

from functools import lru_cache

from .globsem import GlobSem

LIT, STAR, DSTAR, QMARK, END = "lit", "star", "dstar", "qmark", "end"


def tokens(pattern: str, sem: GlobSem) -> tuple:
    out, i, n = [], 0, len(pattern)
    while i < n:
        c = pattern[i]
        if c == "*":
            j = i
            while j < n and pattern[j] == "*":
                j += 1
            run = j - i
            out.append((DSTAR, None) if (sem.double_star and run >= 2 and not sem.star_crosses_slash) else (STAR, None))
            i = j
            continue
        if c == "?" and sem.question_mark:
            out.append((QMARK, None))
        elif c == "$" and sem.dollar_end and i == n - 1:
            out.append((END, None))
        else:
            out.append((LIT, c))
        i += 1
    return tuple(out)


def match(pattern: str, subject: str, sem: GlobSem) -> bool:
    toks = tokens(pattern, sem)
    s = subject if sem.case_sensitive else subject.lower()
    if not sem.case_sensitive:
        toks = tuple((k, v.lower() if k == LIT else v) for k, v in toks)
    n = len(s)

    @lru_cache(maxsize=None)
    def m(i: int, j: int) -> bool:
        if i == len(toks):
            return j == n if sem.anchored else True
        kind, val = toks[i]
        if kind == END:
            return j == n
        if kind in (STAR, DSTAR):
            if m(i + 1, j):
                return True
            crosses = kind == DSTAR or sem.star_crosses_slash
            return j < n and (crosses or s[j] != "/") and m(i, j + 1)
        if kind == QMARK:
            return j < n and (sem.star_crosses_slash or s[j] != "/") and m(i + 1, j + 1)
        return j < n and s[j] == val and m(i + 1, j + 1)

    return m(0, 0)


def literal_chars(pattern: str, sem: GlobSem) -> int:
    """Count of literal characters (a common specificity component)."""
    return sum(1 for k, _ in tokens(pattern, sem) if k == LIT)
