"""T66 render round trip (generator-side render fidelity; NOT solver B). Parse-only checks: the conflict view re-parses to the segments the resolution was built
from and carries no markers in the resolution; the shown files are valid Python (RK8 only is not); side tests are <= 14 lines; the strength witnesses (K2)
and the label witnesses (K1) are complete; the diff's hunk headers match their bodies. -> list of problems."""
import ast
import re

from . import merge3 as M3, merge_spec as MS, msg_spec as MSG, semver as SV


def _parses(text):
    try:
        ast.parse(text)
        return True
    except SyntaxError:
        return False


def _diff_ok(diff):
    lines = diff.rstrip("\n").split("\n")
    i = 2
    while i < len(lines):
        m = re.match(r"^@@ -(\d+),(\d+) \+(\d+),(\d+) @@$", lines[i])
        if not m:
            return False
        old_n, new_n = int(m.group(2)), int(m.group(4))
        i += 1
        o = n = 0
        while i < len(lines) and not lines[i].startswith("@@"):
            c = lines[i][:1]
            o += c in " -"
            n += c in " +"
            i += 1
        if (o, n) != (old_n, new_n):
            return False
    return True


def check(rec):
    s, bad = rec["spec"], []
    head = s["head"]
    if head == "MERGE":
        segs = M3.parse_view(s["view"])
        if len(M3.conflicts(segs)) != 1 or M3.render_view(segs) != s["view"]:
            bad.append("view")
        if any(m in s["resolution"] for m in (M3.MARK_OURS, M3.MARK_THEIRS, M3.MARK_SEP)):
            bad.append("markers_in_resolution")
        if _parses(s["resolution"]) == (s["rk"] == "RK8"):
            bad.append("parse_state")
        for t in (s["test_a"], s["test_b"]):
            if t["text"].count("\n") > MS.LINES_MAX or not _parses(t["text"]):
                bad.append("test_file")
        if not MS.strength_ok({m: dict(v, A_det=True, B_det=True) for m, v in s["strength"].items()}):
            bad.append("strength")
        for w in (s["witness"]["A"], s["witness"]["B"]):
            if not w["ok"] or w["runs"] is None or w["runs"] < 3:
                bad.append("witness_incomplete")
    elif head == "SEMVER":
        for t in (s["old"], s["new"], s["callers"]):
            if not _parses(t):
                bad.append("python_syntax")
        for tag in ("old", "new"):
            w = s["witness"][tag]
            if not w["ok"] or w["runs"] is None or w["runs"] < 3:
                bad.append("witness_incomplete")
        if not s["witness"]["old"]["passed"]:
            bad.append("gold_sanity")
    else:
        if not _diff_ok(s["diff"]):
            bad.append("diff_hunks")
        if "--- a/%s.py" % s["stem"] not in s["diff"]:
            bad.append("diff_header")
    return bad
