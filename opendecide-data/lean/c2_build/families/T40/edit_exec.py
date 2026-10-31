"""families/T40/edit_exec.py: the hermetic str_replace executor (run as a subprocess by edit.apply_edit).

Reads {"file", "old", "new"} as JSON on stdin; writes one JSON line {"label", "count"} on stdout. The real run:
the file is written to the working directory (a temp dir), read back, old_str is counted by str.count on the file
text, the replacement is str.replace(old, new, 1) on the file text when old_str occurs exactly once, the edited text is
written back and ast.parse reads it. Nothing is executed (ast.parse only reads). No imports beyond the standard
library; no network.
Labels: NO_MATCH (count 0), MULTIPLE (count >= 2), BREAKS_SYNTAX (once, edited file does not parse), APPLIES_ONCE.
"""
import ast
import json
import sys


def main() -> None:
    req = json.loads(sys.stdin.read())
    with open("before.py", "w", encoding="utf-8", newline="") as f:
        f.write(req["file"])
    with open("before.py", "r", encoding="utf-8", newline="") as f:
        text = f.read()
    old, new = req["old"], req["new"]
    n = text.count(old) if old else 0
    if n == 0:
        out = {"label": "NO_MATCH", "count": 0}
    elif n > 1:
        out = {"label": "MULTIPLE", "count": n}
    else:
        edited = text.replace(old, new, 1)
        with open("after.py", "w", encoding="utf-8", newline="") as f:
            f.write(edited)
        with open("after.py", "r", encoding="utf-8", newline="") as f:
            edited = f.read()
        try:
            ast.parse(edited)
            out = {"label": "APPLIES_ONCE", "count": 1}
        except (SyntaxError, ValueError):
            out = {"label": "BREAKS_SYNTAX", "count": 1}
    sys.stdout.write(json.dumps(out) + "\n")


main()
