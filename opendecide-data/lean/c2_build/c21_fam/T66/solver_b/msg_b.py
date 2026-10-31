"""MSG head of solver B (no execution at all).

YES iff the commit message describes the ONE behavioural hunk of the diff. Method: `msg_diff` reads the diff (token-level, AST-free) and names the change kind of
the behavioural hunk; `msg_lex` names the change kind the message talks about; equal kinds = YES; a message about another behavioural kind, or about formatting /
comment / docstring only (the trivial kinds), = NO (G0-lite 2.3 and Opus B3). When either side is not decisive, or a diff reading has an alternative that the message
matches, B abstains."""
import re

from . import msg_diff, msg_lex
from . import textparse as tp

# a message in the vocabulary of kind X that may also describe a change of kind Y: a default VALUE is a constant, so a "value changed" message does not exclude a
# change-default hunk (the G0-lite registers the kinds as separate rows; where their vocabularies overlap, B abstains instead of calling the message wrong)
AFFINITY = {"CH-5": ("CH-10",), "CH-6": ("CH-5",)}

HEADS = {"diff": r"^Diff:$", "msg": r"^Commit message: (.*)$"}


def solve(context):
    _pre, secs = tp.split_sections(context, HEADS)
    kinds = [k for k, _m, _b in secs]
    if kinds != ["diff", "msg"]:
        return None, "sections:" + ",".join(kinds)
    diff = secs[0][2]
    msg = (secs[1][1].group(1) + ("\n" + secs[1][2] if secs[1][2] else "")).strip()
    d = msg_diff.analyse(diff)
    if not d["ok"]:
        return None, "diff:" + d["why"]
    k, sc = msg_lex.classify(msg, d["idents"])
    if k is None:
        return None, "message kind not decisive"
    if k in msg_lex.TRIV:
        return "NO", "message describes a trivial edit"
    if k == d["kind"]:
        return "YES", "same kind"
    if k in d["alt"] or k in AFFINITY.get(d["kind"], ()):
        return None, "diff has an alternative reading that the message matches"
    return "NO", "message describes another kind"
