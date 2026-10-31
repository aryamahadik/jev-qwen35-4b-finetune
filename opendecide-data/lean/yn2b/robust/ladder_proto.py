"""Prototype of the F4 polarity ladder for DECISION questions (tool call may run / state holds / clause applies).
Same quad mechanism as build_v11_fixes (frame + switch A + switch B -> para / neg / neg / dneg), new frames.
Checks (the v11 held-out rules): no 6-word run shared with the held-out dev_negwords family (dialogue_rebuttal)
or any v11 train template; no forbidden dialogue cue; no cue word more than 60% tied to answer-flipping questions.
Slots: {d} = decision proposition in lower case, e.g. "the proposed transfer_funds call may run under the policy".
Read-only: imports the v11 template list, writes nothing."""
import sys
from collections import Counter
sys.argv = ["x"]; sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)) + "/../..")
import build_v11_fixes as b

def Q(family, frame, A, B, a_flips=True, b_flips=True):
    return dict(family=family, frame=frame, A=A, B=B, form="prop", a_flips=a_flips, b_flips=b_flips)

QUADS = [
    Q("verdict_record", "An automated check logged the verdict that {A}. Given the record above, is that logged verdict {B}?",
      ("{d}", "it is not the case that {d}"), ("sound", "unsound")),
    Q("verdict_record", "The review field reads \"{A}\". Checking the facts, is the review field {B}?",
      ("PASS: {d}", "FAIL: it is not so that {d}"), ("accurate", "inaccurate")),
    Q("verdict_record", "A second-line auditor signed off on the finding that {A}. Should that sign-off {B}?",
      ("{d}", "it isn't so that {d}"), ("stand", "be reversed")),
    Q("decision_direct", "Under the rules given, {A} {B}?", ("is it established that", "is it ruled out that"), ("{d}", "it isn't the case that {d}")),
    Q("decision_direct", "Applying every clause as written, {A} the conclusion that {d} {B}?", ("is", "is it wrong to say"), ("supported", "unsupported")),
    Q("exception_scope", "Taking the exceptions and amendments into account, does the outcome {A} {B}?",
      ("leave standing the conclusion that {d}", "overturn the conclusion that {d}"), ("hold", "fail")),
    Q("gatekeeping", "If a gatekeeper {A} on the basis that {d}, would the gatekeeper have acted {B}?",
      ("waved it through", "stopped it"), ("correctly", "in error")),
    Q("burden", "Is the conclusion that {d} {A} by the material, or {B}?",
      ("borne out", "contradicted"), ("is it at least not refuted", "is it refuted")),
    Q("checklist", "Checklist item: \"{A}\". Should this item be marked {B}?",
      ("{d}", "it is not so that {d}"), ("done", "not done")),
    Q("counter_hypothesis", "Would someone who {A} that {d} have to {B} their view after reading everything above?",
      ("maintained", "denied"), ("keep", "abandon")),
]
T = b.expand_quads(QUADS)
dev = [t for t in b.TEMPLATES if t["family"] == b.DEV_FAMILY]
v11train = [t for t in b.TEMPLATES if t["family"] != b.DEV_FAMILY]
dev_runs = set().union(*[b.runs(t["text"]) for t in dev])
tr_runs = set().union(*[b.runs(t["text"]) for t in v11train])
clash_dev = {t["tid"]: sorted(b.runs(t["text"]) & dev_runs) for t in T if b.runs(t["text"]) & dev_runs}
clash_tr = {t["tid"]: sorted(b.runs(t["text"]) & tr_runs)[:2] for t in T if b.runs(t["text"]) & tr_runs}
BAN = ("reply", "replies", "commenter", "debate", "two notes", "sam", "jo:", "disagree", "agreed", "back", "undercut")
banned = [t["tid"] for t in T if any(w in b.toks(t["text"]) or w in t["text"].lower() for w in BAN if " " in w or w in b.toks(t["text"]))]
shares = b.cue_shares((t["text"], t["polarity"] == "neg") for t in T)
print("templates", len(T), Counter(t["role"] for t in T))
print("6-word runs shared with held-out dialogue_rebuttal:", clash_dev or "none")
print("6-word runs shared with v11 train templates:", clash_tr or "none")
print("dialogue cues present:", banned or "none")
mx = max(((w, s) for w, s in shares.items() if s[1] >= 4), key=lambda kv: kv[1][0]); print("max cue neg-share (count>=4):", mx, "(v11 rule: <= 0.60)")
