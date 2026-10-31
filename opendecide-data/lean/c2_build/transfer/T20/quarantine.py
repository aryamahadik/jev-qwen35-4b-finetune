"""transfer/T20/quarantine.py: pool templates T20 does not render (fix iteration 1; C2_DATA_SPEC 6.3).

A quarantined template is never picked by plugin.T20Plugin.ctx_for; nothing is relabelled and no frozen pool file is
edited (pools/ keeps its sha256 manifest). Each entry names the evidence. The rules in c2_kit.polarity (wordings) and
roles.py (Mode F notes) quarantine more by program check; this file holds the decisions taken on gate evidence.

G3-H (pilot/PILOT_VERDICT.json, "g3h"): a Mode F template below 98% extraction is quarantined by rule. All 34
mismatches are one field, "reporter" returned null, on notes that name the REPORTER only as the author, adder or
forwarder (F6). The 3 borderline templates passed the pilot by luck of the extractor (5 rows) and are treated as
unadmitted too (verdict F6).

G5-H (verdict "g5h"): the kit rule (> 3% of a template's read rows disagree with gold) fires on 1 skin and 1 wording
because the one disputed row a0000 carries both (n = 2 each, 1 disagreement). Adjudication found a reader error (gold
right, the program answer reproduced by an independent regex solver); the gate is not loosened, so both stay quarantined
until a later read clears them.
"""
from __future__ import annotations

G3H_QUARANTINE = {
    "T20-fre-031fde13c2": "G3-H 4/6 (runbook_note; 'added by' only)",
    "T20-fre-09166146f8": "G3-H 3/8 (runbook_note; 'added by' only)",
    "T20-fre-10104b76c7": "G3-H 0/1 (runbook_note; 'Runbook note by' only)",
    "T20-fre-2b5767cb6d": "G3-H 0/1 (postmortem_draft; 'writes this review draft' only)",
    "T20-fre-35d26e280a": "G3-H 0/4 (postmortem_draft; 'written by' only)",
    "T20-fre-5b50a5a753": "G3-H 1/6 (handoff_log; 'is forwarding this' only)",
    "T20-fre-68bd98f1ad": "G3-H 2/7 (runbook_note; 'added by' only)",
    "T20-fre-b7d1ef2d89": "G3-H 1/6 (postmortem_draft; 'Written by' only)",
    "T20-fre-d3a3204464": "G3-H 3/8 (runbook_note; 'Added ... by' only)",
    "T20-fre-f3036726e6": "G3-H 0/1 (postmortem_draft; 'written by' only)",
    # borderline: passed G3-H in the pilot, author-style, so unadmitted (verdict F6)
    "T20-fre-5f319c87e4": "borderline pass (postmortem_draft; 'relaying the note of X, written for')",
    "T20-fre-766f0af572": "borderline pass (postmortem_draft; 'note from X, drafted for')",
    "T20-fre-4ed5874cef": "borderline pass (runbook_note; 'added by' only)",
}
G5H_QUARANTINE = {
    "T20-ski-3b2dda71f3": "G5-H template rule, n=2, 1 disagreement (incident_email skin); reader error, gate not loosened",
    "T20-wor-38f9393e8c": "G5-H template rule, n=2, 1 disagreement (yn_not_reaches wording); reader error, gate not loosened",
}
QUARANTINE = {**G3H_QUARANTINE, **G5H_QUARANTINE}
