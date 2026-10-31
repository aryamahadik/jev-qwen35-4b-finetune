"""Edit carriers (G0 addendum v3.2 section 4): `file_edit` (replace a span), `apply_patch` (unified diff) and `file_write`
(whole file, already a carrier in v3.1). An EditAction is the STRUCTURED action; render_edit() turns it into the tool-call
text of its carrier and parse_edit() reads that text back (the K1 round trip for edits: the call must parse back to the
same canonical hunk). Nothing here is executed.

The model of an edit: the file has OLD content lines (recorded in the simulated state) and the call produces NEW content
lines. The CANONICAL HUNK is the minimal differing region (common leading and trailing lines stripped): (removed, added).
Every carrier of the same change has the same canonical hunk, which is what makes "the same diff on a non-state file"
well defined: members of a pair share the hunk bytes and differ only in path / consumer record / zone.

Tool-call text (design choice, flagged: C2's layout of tool calls is L-0's): one JSON object per call,
  file_edit  : {"tool":"file_edit","path":P,"old_string":S,"new_string":T}      (S/T carry 1 context line each side)
  file_write : {"tool":"file_write","path":P,"content":C}                       (whole new file)
  apply_patch: {"tool":"apply_patch","patch":"--- a/P\\n+++ b/P\\n@@ -a,b +c,d @@\\n ctx\\n-old\\n+new\\n ctx\\n"}
"""
import json
import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

CARRIERS = ("file_edit", "apply_patch", "file_write")
EDIT_TOOLS = ("file_edit", "apply_patch")          # new carriers of v3.2 (file_write exists since v3.1)


@dataclass
class TextPayload:
    """Plain text content a history call wrote (kept in Spec.payloads next to Script payloads)."""
    text: str

    def to_dict(self):
        return {"text": self.text}

    def canon(self):
        return [{"text": self.text}]


def hunk(old_lines, new_lines):
    """-> (prefix_len, removed, added, suffix_len): the minimal differing region of two line lists."""
    o, n = list(old_lines), list(new_lines)
    p = 0
    while p < len(o) and p < len(n) and o[p] == n[p]:
        p += 1
    s = 0
    while s < len(o) - p and s < len(n) - p and o[len(o) - 1 - s] == n[len(n) - 1 - s]:
        s += 1
    return p, o[p:len(o) - s], n[p:len(n) - s], s


@dataclass
class EditAction:
    carrier: str                           # file_edit | apply_patch | file_write
    path: str
    old_lines: List[str] = field(default_factory=list)     # content before the call (recorded in the state)
    new_lines: List[str] = field(default_factory=list)     # content after the call

    def __post_init__(self):
        if self.carrier not in CARRIERS:
            raise ValueError("bad edit carrier %r" % self.carrier)

    # ---- canonical hunk ---------------------------------------------------------------------------------
    def hunk(self):
        _, removed, added, _ = hunk(self.old_lines, self.new_lines)
        return removed, added

    @property
    def removed(self):
        return self.hunk()[0]

    @property
    def added(self):
        return self.hunk()[1]

    def canon(self):
        removed, added = self.hunk()
        return [{"edit": 1, "path": self.path, "removed": removed, "added": added}]

    def cmds(self):                          # Script-like protocol: an edit has no shell commands of its own
        return []

    def to_dict(self):
        return {"edit": self.carrier, "path": self.path, "old_lines": list(self.old_lines), "new_lines": list(self.new_lines)}

    @staticmethod
    def from_dict(d):
        return EditAction(d["edit"], d["path"], list(d["old_lines"]), list(d["new_lines"]))

    def same_hunk_as(self, other):
        return self.hunk() == other.hunk()


# ---------------------------------------------------------------------------------------------------- rendering
def _join(lines):
    return "\n".join(lines)


def _occurrences(lines, span):
    n = len(span)
    if n == 0:
        return 0
    return sum(1 for i in range(len(lines) - n + 1) if list(lines[i:i + n]) == list(span))


def _context_window(edit):
    """Smallest symmetric context (1..8 lines each side where present) that makes the OLD span occur EXACTLY ONCE in the old content,
    as a real edit tool requires; the whole file when no window is unique."""
    p, removed, added, s = hunk(edit.old_lines, edit.new_lines)
    old = edit.old_lines
    tail = len(old) - s
    for k in range(1, 9):
        before = old[max(0, p - k):p]
        after = old[tail:tail + k]
        if _occurrences(old, before + removed + after) == 1:
            return p, before, removed, added, after
    return p, old[:p], removed, added, old[tail:]


def render_edit(edit):
    """Tool-call text of the edit's carrier (deterministic; JSON, ensure_ascii False, compact separators)."""
    dumps = lambda o: json.dumps(o, ensure_ascii=False, separators=(", ", ": "))
    if edit.carrier == "file_write":
        return dumps({"tool": "file_write", "path": edit.path, "content": _join(edit.new_lines)})
    p, before, removed, added, after = _context_window(edit)
    if edit.carrier == "file_edit":
        return dumps({"tool": "file_edit", "path": edit.path, "old_string": _join(before + removed + after),
                      "new_string": _join(before + added + after)})
    # apply_patch: unified diff with one context line on each side where present
    start_old = p - len(before) + 1 if (before or removed or after) else 0
    body = [" " + l for l in before] + ["-" + l for l in removed] + ["+" + l for l in added] + [" " + l for l in after]
    n_old = len(before) + len(removed) + len(after)
    n_new = len(before) + len(added) + len(after)
    start_new = start_old
    patch = "--- a/%s\n+++ b/%s\n@@ -%d,%d +%d,%d @@\n%s" % (edit.path, edit.path, start_old, n_old, start_new, n_new, "\n".join(body))
    return dumps({"tool": "apply_patch", "patch": patch})


def parse_edit(text):
    """Read a rendered call back. -> dict {carrier, path, removed, added, new_content (file_write only) } or None."""
    try:
        o = json.loads(text)
    except Exception:
        return None
    if not isinstance(o, dict):
        return None
    tool = o.get("tool")
    if tool == "file_write" and isinstance(o.get("content"), str) and isinstance(o.get("path"), str):
        return {"carrier": "file_write", "path": o["path"], "new_content": o["content"].split("\n") if o["content"] != "" else []}
    if tool == "file_edit" and isinstance(o.get("old_string"), str) and isinstance(o.get("new_string"), str):
        old = o["old_string"].split("\n") if o["old_string"] != "" else []
        new = o["new_string"].split("\n") if o["new_string"] != "" else []
        _, removed, added, _ = hunk(old, new)
        return {"carrier": "file_edit", "path": o["path"], "removed": removed, "added": added, "old_span": old, "new_span": new}
    if tool == "apply_patch" and isinstance(o.get("patch"), str):
        lines = o["patch"].split("\n")
        if len(lines) < 3 or not lines[0].startswith("--- a/") or not lines[1].startswith("+++ b/"):
            return None
        path = lines[0][len("--- a/"):]
        if lines[1][len("+++ b/"):] != path:
            return None
        old, new = [], []
        for l in lines[3:]:
            if l.startswith("-"):
                old.append(l[1:])
            elif l.startswith("+"):
                new.append(l[1:])
            elif l.startswith(" "):
                old.append(l[1:])
                new.append(l[1:])
            elif l == "":
                continue
            else:
                return None
        _, removed, added, _ = hunk(old, new)
        return {"carrier": "apply_patch", "path": path, "removed": removed, "added": added, "old_span": old, "new_span": new}
    return None


def roundtrip_edit(edit, text):
    """K1 for edit carriers: does the call text parse back to the spec's path and canonical hunk? -> (ok, detail)."""
    r = parse_edit(text)
    if r is None:
        return False, "unparsable"
    if r["carrier"] != edit.carrier or r["path"] != edit.path:
        return False, "carrier/path differ"
    if edit.carrier == "file_write":
        if r["new_content"] != list(edit.new_lines):
            return False, "content differs"
        return True, "ok"
    removed, added = edit.hunk()
    if r["removed"] != removed or r["added"] != added:
        return False, "hunk differs"
    return True, "ok"


def edit_text_lines(edit):
    """The text lines a model sees in the call (for token estimates and the injection scan): hunk lines or content."""
    return list(edit.new_lines) if edit.carrier == "file_write" else list(edit.removed) + list(edit.added)


def apply_parsed(old_lines, parsed):
    """Reconstruct the NEW content from a parsed call and the recorded OLD content (the consumer round trip of K23: the
    induced effects are recomputed from the RENDERED edit, not from the spec). None when the span is not found exactly once."""
    if parsed["carrier"] == "file_write":
        return list(parsed["new_content"])
    old_span, new_span = parsed["old_span"], parsed["new_span"]
    n = len(old_span)
    hits = [i for i in range(len(old_lines) - n + 1) if list(old_lines[i:i + n]) == list(old_span)]
    if len(hits) != 1 or n == 0:
        return None
    i = hits[0]
    return list(old_lines[:i]) + list(new_span) + list(old_lines[i + n:])
