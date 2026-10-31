"""transfer/T20/roles.py: the REPORTER role rule for Mode F notes (PILOT_VERDICT F6; G3-H).

Why. The G3-H extractor is asked for "the person who reported it, as written" (plugin.extract_fields). 13 of the 41
Mode F templates of the first pilot name the REPORTER only as the note's author, adder or forwarder ("written by", "added
by", "Runbook note by", "is forwarding this", "writes this review draft", "note from ... drafted for ..."). The extractor
(told to give null when the passage does not state the field) returns null for most of them: 10 templates failed G3-H
(34 rows dropped). The extraction schema is NOT changed to accept an author or a forwarder (that would make G3-H pass by
weakening what it measures); the notes must state the role the extractor is asked for.

The rule (one fixed definition, program-checked; label-blind: it reads the note text and its REPORTER value only):
  the sentence or line that holds the REPORTER value must hold a reporting cue
    raised | reported | spotted | flagged | noticed | sent      (any letter case, whole word)
    from                                                        (a field label "from:" or "message / alert / handoff
                                                                 from X"; never "note from X" or "note comes from X",
                                                                 which name the note's author)
  or the line must open with the name as a speaker label ("Dana Okafor: ...").
Author, adder, forwarder and relay roles (written, wrote, writes, drafted, added, filed, files, forwarding, relaying,
assigned by, "... by X" with no reporting cue) do not count.

Used by: haiku_author.check_freeform (a re-authored note that breaks the rule never enters a pool) and
plugin.T20Plugin.ctx_for (a frozen note that breaks the rule is quarantined, never rendered).
"""
from __future__ import annotations

import re

REPORTING_WORDS = ("raised", "reported", "spotted", "flagged", "noticed", "sent")
_CUE = re.compile(r"\b(?:" + "|".join(REPORTING_WORDS) + r")\b|(?<!note )(?<!comes )\bfrom\b", re.I)
_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")


def units(text: str) -> list:
    """The sentences and lines of a note."""
    return [u for u in _SPLIT.split(text or "") if u.strip()]


def reporter_problems(text: str, reporter: str) -> list:
    """[] when the sentence or line holding `reporter` states a reporting role, else the problem."""
    hits = [u for u in units(text) if reporter in u]
    if not hits:
        return [f"REPORTER {reporter!r} appears in no sentence or line"]
    for u in hits:
        if _CUE.search(u) or re.match(r"\s*" + re.escape(reporter) + r"\s*:", u):
            return []
    return [f"REPORTER role: the sentence or line holding {reporter!r} names no reporting cue "
            f"({', '.join(REPORTING_WORDS)}, from); an author, adder or forwarder is not the reporter"]
