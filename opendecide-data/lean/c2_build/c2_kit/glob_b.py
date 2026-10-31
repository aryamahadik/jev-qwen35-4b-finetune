"""c2_kit/glob_b.py: glob matching by compiling the pattern to a regular expression (solver-B side; see globsem.py).

Independent of glob_a.py (which never uses `re`): each pattern character is translated to a regex fragment, and the
subject is tested with re.fullmatch (anchored) or re.match (prefix). tests/test_glob.py checks both matchers agree on
every pattern x subject pair of a brute-force table.
"""
from __future__ import annotations

import re

from .globsem import GlobSem


def compile_glob(pattern: str, sem: GlobSem) -> re.Pattern:
    one = "." if sem.star_crosses_slash else "[^/]"
    parts, i, n = [], 0, len(pattern)
    while i < n:
        c = pattern[i]
        if c == "*":
            j = i
            while j < n and pattern[j] == "*":
                j += 1
            wide = sem.star_crosses_slash or (sem.double_star and j - i >= 2)
            parts.append(".*" if wide else "[^/]*")
            i = j
            continue
        if c == "?" and sem.question_mark:
            parts.append(one)
        elif c == "$" and sem.dollar_end and i == n - 1:
            parts.append(r"\Z")
        else:
            parts.append(re.escape(c))
        i += 1
    flags = re.S | (0 if sem.case_sensitive else re.I)
    return re.compile("".join(parts), flags)


def match(pattern: str, subject: str, sem: GlobSem) -> bool:
    rx = compile_glob(pattern, sem)
    return bool(rx.fullmatch(subject) if sem.anchored else rx.match(subject))
