"""Solver B's own unified-diff reader / applier (stdlib only). Used by T57 (shown patch -> candidate tree) and T56g (diff -> patched
tree, protected-path check from the diff headers)."""
import re

from .common import Unsupported

_HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def parse_diff(text):
    """-> list of {'old': path|None, 'new': path|None, 'hunks': [{'old_start','old_len','new_start','new_len','lines':[(tag, text)]}]}"""
    files = []
    cur = None
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("--- ") and i + 1 < len(lines) and lines[i + 1].startswith("+++ "):
            old = ln[4:].strip()
            new = lines[i + 1][4:].strip()
            cur = {"old": None if old == "/dev/null" else re.sub(r"^a/", "", old),
                   "new": None if new == "/dev/null" else re.sub(r"^b/", "", new), "hunks": []}
            files.append(cur)
            i += 2
            continue
        m = _HUNK.match(ln)
        if m and cur is not None:
            h = {"old_start": int(m.group(1)), "old_len": int(m.group(2) if m.group(2) is not None else 1),
                 "new_start": int(m.group(3)), "new_len": int(m.group(4) if m.group(4) is not None else 1), "lines": []}
            i += 1
            need_old, need_new = h["old_len"], h["new_len"]
            while i < len(lines) and (need_old > 0 or need_new > 0):
                l = lines[i]
                if l.startswith("\\"):
                    i += 1
                    continue
                tag, body = (l[0], l[1:]) if l else (" ", "")
                if tag == " ":
                    need_old -= 1
                    need_new -= 1
                elif tag == "-":
                    need_old -= 1
                elif tag == "+":
                    need_new -= 1
                else:
                    raise Unsupported("diff line tag %r" % tag)
                h["lines"].append((tag, body))
                i += 1
            cur["hunks"].append(h)
            continue
        i += 1
    return files


def apply_diff(tree, text):
    """Apply a unified diff to a {path: text} tree. Returns (new_tree, touched) where touched = list of
    {'path','kind': 'add'|'edit'|'delete'}. Raises ValueError when a context line does not match."""
    out = dict(tree)
    touched = []
    for f in parse_diff(text):
        path = f["new"] or f["old"]
        if f["old"] is not None and f["old"] in out and f["hunks"] and f["hunks"][0]["old_start"] == 0 and f["hunks"][0]["old_len"] == 0:
            kind = "add"                              # '-0,0' on an existing path: treated as a rewrite from empty
        existed = f["old"] is not None and f["old"] in out
        src = out.get(f["old"], "") if f["old"] is not None else ""
        lines = src.split("\n")
        if lines and lines[-1] == "":
            lines = lines[:-1]
        res = []
        pos = 0
        # hunks refer to the ORIGINAL file, so a diff whose hunks are listed out of order (the swapped-hunk copies) is applied in
        # file order, as `patch` would
        for h in sorted(f["hunks"], key=lambda x: x["old_start"]):
            start = h["old_start"] - 1 if h["old_len"] > 0 else h["old_start"]
            if start < pos or start > len(lines):
                raise ValueError("hunk out of order")
            res.extend(lines[pos:start])
            pos = start
            for tag, body in h["lines"]:
                if tag == " ":
                    if pos >= len(lines) or lines[pos] != body:
                        raise ValueError("context mismatch")
                    res.append(body)
                    pos += 1
                elif tag == "-":
                    if pos >= len(lines) or lines[pos] != body:
                        raise ValueError("removed line mismatch")
                    pos += 1
                else:
                    res.append(body)
        res.extend(lines[pos:])
        if f["new"] is None:
            out.pop(f["old"], None)
            touched.append({"path": f["old"], "kind": "delete"})
            continue
        out[f["new"]] = "\n".join(res) + ("\n" if res else "")
        if f["old"] is not None and f["old"] != f["new"]:
            out.pop(f["old"], None)
        touched.append({"path": f["new"], "kind": "edit" if existed else "add"})
    return out, touched
