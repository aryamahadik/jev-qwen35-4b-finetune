"""families/T43/patching.py: unified diffs (solver A side): make_diff, strict apply_diff, diff statistics.

A patch is a unified diff of the whole file against the SHOWN file (context 1). It APPLIES iff, for every hunk, the
context and removed lines equal the file's lines at the stated start line (offset 0, fuzz 0). Otherwise it does not apply.
"""
from __future__ import annotations

import difflib
import re

HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@$")


def make_diff(old: str, new: str, path: str, n: int = 1) -> str:
    d = difflib.unified_diff(old.split("\n"), new.split("\n"), f"a/{path}", f"b/{path}", n=n, lineterm="")
    return "\n".join(d)


def parse_diff(diff: str):
    """[(old_start_1based, old_len, [lines with their marker])] or None when the text is not a unified diff."""
    lines = diff.split("\n")
    if len(lines) < 4 or not lines[0].startswith("--- ") or not lines[1].startswith("+++ "):
        return None
    hunks, cur = [], None
    for ln in lines[2:]:
        m = HUNK.match(ln)
        if m:
            cur = [int(m.group(1)), int(m.group(2)) if m.group(2) is not None else 1, []]
            hunks.append(cur)
        elif cur is not None and ln[:1] in (" ", "-", "+"):
            cur[2].append(ln)
        else:
            return None
    return hunks or None


def apply_diff(text: str, diff: str):
    """The patched text, or None when the patch does not apply (strict)."""
    hunks = parse_diff(diff)
    if hunks is None:
        return None
    src = text.split("\n")
    out, pos = [], 0
    for start, old_len, body in hunks:
        s0 = start - 1 if old_len else start          # a zero-length old range names the line AFTER which it inserts
        old = [ln[1:] for ln in body if ln[0] in " -"]
        if len(old) != old_len or s0 < pos or src[s0:s0 + old_len] != old:
            return None
        out += src[pos:s0]
        out += [ln[1:] for ln in body if ln[0] in " +"]
        pos = s0 + old_len
    return "\n".join(out + src[pos:])


def stats(diff: str) -> dict:
    hunks = parse_diff(diff) or []
    add = sum(ln[0] == "+" for h in hunks for ln in h[2])
    rem = sum(ln[0] == "-" for h in hunks for ln in h[2])
    return {"added": add, "removed": rem, "hunks": len(hunks), "changed": add + rem}


DIFF_EDGES = (2, 4, 6)


def diff_bin(changed: int) -> int:
    return sum(changed > e for e in DIFF_EDGES)


def shift_header(diff: str, by: int) -> str:
    """The same hunks with every old and new start moved by `by` lines (a patch made for another version of the file)."""
    def sh(m):
        a, b, c, d = m.group(1), m.group(2), m.group(3), m.group(4)
        return f"@@ -{int(a) + by}" + (f",{b}" if b is not None else "") + f" +{int(c) + by}" + \
               (f",{d}" if d is not None else "") + " @@"
    return "\n".join(HUNK.sub(sh, ln) if ln.startswith("@@") else ln for ln in diff.split("\n"))
