"""Parsing of the RENDERED row text (the only thing solver B reads): section splitter, lettered options, unified diff.

Nothing here looks at a label, a spec or a witness. Every function is pure text -> data."""
import re

OPTION_LINE = r"^([A-Z])\) (\S.*)$"


class ParseError(Exception):
    pass


def split_sections(context, heading_patterns):
    """Split `context` into (preamble, [(kind, match, body_text)]) at lines that match one of `heading_patterns` ({kind: compiled regex}).
    A heading is a whole line. The body of a section runs to the next heading (trailing blank lines dropped)."""
    lines = context.split("\n")
    marks = []
    for i, ln in enumerate(lines):
        for kind, rx in heading_patterns.items():
            m = re.match(rx, ln)
            if m:
                marks.append((i, kind, m))
                break
    pre = "\n".join(lines[:marks[0][0]]).strip("\n") if marks else context
    out = []
    for k, (i, kind, m) in enumerate(marks):
        end = marks[k + 1][0] if k + 1 < len(marks) else len(lines)
        body = "\n".join(lines[i + 1:end]).strip("\n")
        out.append((kind, m, body))
    return pre, out


def parse_options(rendered, options):
    """Letters and texts of the answer options, read from the rendered options block (fallback: the tail of the rendered text).
    Cross-checked against the structured option list when it is given. -> [(letter, text)]"""
    block = rendered.get("options_text")
    if not block:
        txt = rendered.get("text", "")
        tail = []
        for ln in reversed(txt.split("\n")):
            if re.match(OPTION_LINE, ln):
                tail.append(ln)
            else:
                break
        block = "\n".join(reversed(tail))
    got = []
    for ln in block.split("\n"):
        m = re.match(OPTION_LINE, ln)
        if not m:
            raise ParseError("option line")
        got.append((m.group(1), m.group(2).strip()))
    if len(got) < 2:
        raise ParseError("options")
    if [g[0] for g in got] != [chr(65 + i) for i in range(len(got))]:
        raise ParseError("option letters")
    if options:
        listed = [(o["letter"], str(o["text"]).strip()) for o in options]
        if listed != got:
            raise ParseError("options differ between rendered block and option list")
    return got


def letter_of(opts, label):
    hits = [lt for lt, tx in opts if tx == label]
    if len(hits) != 1:
        raise ParseError("label not among options")
    return hits[0]


# ---- unified diff ------------------------------------------------------------------------------------------------------------------
HUNK_HEAD = r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@"


class Hunk(object):
    def __init__(self, old_start, new_start):
        self.old_start, self.new_start = old_start, new_start
        self.lines = []                  # [(tag, text)] tag in " ", "-", "+"


def parse_diff(diff_text):
    """-> list of Hunk (all files). Raises ParseError when the text is not a unified diff of the expected shape."""
    hunks, cur = [], None
    for ln in diff_text.split("\n"):
        m = re.match(HUNK_HEAD, ln)
        if m:
            cur = Hunk(int(m.group(1)), int(m.group(3)))
            hunks.append(cur)
            continue
        if cur is None:
            if ln.startswith(("--- ", "+++ ", "diff ", "index ")) or not ln.strip():
                continue
            raise ParseError("diff header")
        if ln.startswith("\\"):
            continue
        if ln == "":
            cur.lines.append((" ", ""))              # an empty context line (some renderers drop the single space)
            continue
        tag = ln[0]
        if tag not in " -+":
            raise ParseError("diff line")
        cur.lines.append((tag, ln[1:]))
    if not hunks:
        raise ParseError("no hunks")
    return hunks
