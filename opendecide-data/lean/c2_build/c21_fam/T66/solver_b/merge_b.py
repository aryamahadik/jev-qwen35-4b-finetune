"""MERGE head of solver B.

Question: do BOTH shown test suites pass on the proposed resolution? Method: split the rendered context into its sections, read the conflict view as a three-way
hunk list (ours / base / theirs, used for the marker-residue rule), then evaluate each shown suite on the resolution with solver B's own evaluator (`pyi`); nothing
is compiled or executed natively. Rules written from the G0-lite (K2 strength: a candidate that leaves a marker, does not parse, or fails any shown test is NO)."""
import re

from . import pyi
from . import textparse as tp

HEADS = {
    "view": r"^Conflict view of (\S+)\.py:$",
    "test_a": r"^Tests of side A \((\S+)\):$",
    "test_b": r"^Tests of side B \((\S+)\):$",
    "resolution": r"^Proposed resolution of (\S+)\.py:$",
}
MARKER = r"^(<<<<<<<|=======|>>>>>>>|\|\|\|\|\|\|\|)( .*)?$"


class Hunk3(object):
    def __init__(self, ours, base, theirs):
        self.ours, self.base, self.theirs = ours, base, theirs


def parse_conflict_view(view):
    """-> (n_common_lines, [Hunk3]); ParseError when the markers are not well formed (git-style diff3: ours / base / theirs)."""
    hunks, state, cur, common = [], "common", None, 0
    for ln in view.split("\n"):
        if ln.startswith("<<<<<<<"):
            if state != "common":
                raise tp.ParseError("nested marker")
            state, cur = "ours", Hunk3([], [], [])
        elif ln.startswith("|||||||"):
            if state != "ours":
                raise tp.ParseError("marker order")
            state = "base"
        elif ln.startswith("=======") and state in ("ours", "base"):
            if state == "ours":
                state = "base"          # a two-way style hunk has no base part: both separators close the previous part
            state = "theirs"
        elif ln.startswith(">>>>>>>"):
            if state != "theirs":
                raise tp.ParseError("marker order")
            hunks.append(cur)
            state, cur = "common", None
        elif state == "common":
            common += 1
        else:
            {"ours": cur.ours, "base": cur.base, "theirs": cur.theirs}[state].append(ln)
    if state != "common":
        raise tp.ParseError("unterminated conflict")
    return common, hunks


def solve(context):
    """-> (label or None, reason). None = abstain (reason says why)."""
    _pre, secs = tp.split_sections(context, HEADS)
    kinds = [k for k, _m, _b in secs]
    if kinds != ["view", "test_a", "test_b", "resolution"]:
        return None, "sections:" + ",".join(kinds)
    (_, mv, view), (_, _ma, ta), (_, _mb, tb), (_, mr, res) = secs
    stem = mr.group(1)
    if mv.group(1) != stem:
        return None, "stem mismatch"
    try:
        n_common, hunks = parse_conflict_view(view)
    except tp.ParseError as e:
        return None, "view:%s" % e
    if not hunks:
        return None, "view without conflict"
    # rule 1: a marker left in the candidate is not a program
    if any(re.match(MARKER, ln) for ln in res.split("\n")):
        return "NO", "marker residue"
    # rule 2: the candidate must parse
    bad = pyi.check_syntax(res)
    if bad:
        return "NO", "candidate does not parse"
    # rule 3: evaluate the two shown suites on the candidate
    w = pyi.World({stem: res})
    ra = pyi.run_suite(w, ta, "test_a")
    rb = pyi.run_suite(pyi.World({stem: res}), tb, "test_b")
    if ra.status == "unsupported" or rb.status == "unsupported":
        return None, "unsupported:%s|%s" % (ra.detail, rb.detail)
    if ra.ok and rb.ok:
        return "YES", "both suites pass"
    return "NO", "suite A %s, suite B %s" % (ra.status, rb.status)
