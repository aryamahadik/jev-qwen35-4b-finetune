"""pl_frames: the polarity-ladder frames of yn2b family F4 (gen3_polarity_ladder; yn2b/SPEC.md section 5 F4).

Claude-written for yn2b. A quad is frame x switch A x switch B (SPEC 5 F4): the frame is a yes/no question with the
slots {A}, {B} and {d}; {d} is a decision proposition (a lower-case clause, e.g. 'the proposed call may run under the
policy'); each switch has a keeping alternative (index 0) and an answer-flipping alternative (index 1). The four cells:

  cell "00"  para  (0 flips)   gold = truth(d)
  cell "10"  negA  (1 flip)    gold = not truth(d)
  cell "01"  negB  (1 flip)    gold = not truth(d)
  cell "11"  dneg  (2 flips)   gold = truth(d)

i.e. gold = truth(d) XOR flipA XOR flipB. Every frame is written so that this holds for a proposition that the material
either establishes or rules out (all F4 propositions are of that kind: program decisions and human gold labels).

Each quad also carries the two card lines of a yes/no row (SPEC 4.4: every card says what yes AND no mean): `y` restates
the question's own claim as a statement and `n` denies it, with the same switches filled in. The card therefore never
resolves the negations for the reader: a yes/no card says what the answers mean, the question still has to be read.

Families: 10 (SPEC 5 F4: the 7 of yn2b/robust/ladder_proto.py, rewritten, plus sign_off, compliance_flag and
audit_finding). Four of them evaluate a record (judge wording rule, SPEC 4.7: no right / wrong / correct / accurate ...,
the record is a log line or a form field, never a quoted speaker turn). Two families are held out for dev_holdout:
audit_finding (record) and counter_hypothesis. The held-out families use their own negation wrappers and wording, and
share no 6-word run with the training families (tested).

Never in any frame (SPEC 5 F4, 4.7, red-team S2): the dialogue_rebuttal cues (reply, replies, commenter, debate, "two
notes", a speaker label "Name:", agreed, disagree, back, undercut) and the judge-banned words. The 6-word-run bans
against the dialogue_rebuttal / v11 templates, the ship-split instructions, OHS-1/2 and the eval injected spans are
tested in yn2b/tests/test_gen3_polarity_ladder.py and re-checked on every rendered row by the builder.
"""
from __future__ import annotations

import re

# negated-clause wrappers: training families / held-out families (disjoint wording)
T_NOT = "it does not hold that {d}"
T_CANNOT = "it cannot be said that {d}"
T_FALSE = "it is false to say that {d}"
H_UNTRUE = "it is untrue that {d}"
H_NOTHING = "nothing supports the idea that {d}"
H_NOTRUTH = "there is no truth in saying that {d}"

FAMILIES = {  # family -> evaluates a record (judge tier)?
    "verdict_record": True, "sign_off": True, "compliance_flag": True, "audit_finding": True,
    "decision_direct": False, "exception_scope": False, "gatekeeping": False, "burden": False, "checklist": False,
    "counter_hypothesis": False,
}
HOLDOUT_FAMILIES = ("audit_finding", "counter_hypothesis")
TRAIN_FAMILIES = tuple(f for f in FAMILIES if f not in HOLDOUT_FAMILIES)


def Q(qid, family, q, y, n, A, B):
    return {"id": qid, "family": family, "q": q, "y": y, "n": n, "A": tuple(A), "B": tuple(B)}


QUADS = [
    # ------------------------------------------------------------------ verdict_record (record)
    Q("vr1", "verdict_record",
      "An automated check logged the verdict that {A}. Going by the material given, is that logged verdict {B}?",
      "Going by the material given, the logged verdict that {A} is {B}.",
      "Going by the material given, the logged verdict that {A} is not {B}.",
      ("{d}", T_NOT), ("sound", "unsound")),
    Q("vr2", "verdict_record",
      "A review field on file states that {A}. Measured against the material given, does that field {B}?",
      "Measured against the material given, the review field stating that {A} does {B}.",
      "Measured against the material given, the review field stating that {A} does not {B}.",
      ("{d}", T_CANNOT), ("hold up", "fall short")),
    Q("vr3", "verdict_record",
      "The case log records the determination that {A}. Is that determination {B} by the material given?",
      "The determination that {A} is {B} by the material given.",
      "The determination that {A} is not {B} by the material given.",
      ("{d}", T_FALSE), ("borne out", "contradicted")),
    # ------------------------------------------------------------------ sign_off (record)
    Q("so1", "sign_off",
      "Before closing the file, a supervisor {A} the statement that {d}. Given the material provided, was that action "
      "{B}?",
      "Given the material provided, the supervisor's action, which {A} the statement that {d}, was {B}.",
      "Given the material provided, the supervisor's action, which {A} the statement that {d}, was not {B}.",
      ("approved", "rejected"), ("justified", "unjustified")),
    Q("so2", "sign_off",
      "The approval mark beside the line saying that {d} reads {A}. Should that mark be {B}?",
      "The {A} mark beside the line saying that {d} should be {B}.",
      "The {A} mark beside the line saying that {d} should not be {B}.",
      ("approved", "refused"), ("kept as it is", "changed")),
    Q("so3", "sign_off",
      "At sign-off, a team lead {A} the claim that {d}. Would a careful check of the material given {B} that call?",
      "A careful check of the material given would {B} the team lead's call, which {A} the claim that {d}.",
      "A careful check of the material given would not {B} the team lead's call, which {A} the claim that {d}.",
      ("endorsed", "dismissed"), ("uphold", "overturn")),
    # ------------------------------------------------------------------ compliance_flag (record)
    # R2 fix (1 Oct): was 'flagged this file with the note that {A} ... is that flag warranted?', which also reads as
    # 'does the file have a compliance problem' (a flag signals one), so a true note that something is in order
    # could be answered 'no'. The question now asks about the note itself.
    Q("cf1", "compliance_flag",
      "A compliance scanner attached a note to this file stating that {A}. Given the material provided, is that "
      "note {B}?",
      "Given the material provided, the scanner's note stating that {A} is {B}.",
      "Given the material provided, the scanner's note stating that {A} is not {B}.",
      ("{d}", T_NOT), ("well founded", "unfounded")),
    Q("cf2", "compliance_flag",
      "The compliance tracker marks the requirement that {d} as {A}. Does the material given {B} that marking?",
      "The material given does {B} marking the requirement that {d} as {A}.",
      "The material given does not {B} marking the requirement that {d} as {A}.",
      ("met", "unmet"), ("support", "contradict")),
    Q("cf3", "compliance_flag",
      "An exception report states that {A}. Given the material provided, should the report be {B}?",
      "Given the material provided, the report stating that {A} should be {B}.",
      "Given the material provided, the report stating that {A} should not be {B}.",
      ("{d}", T_CANNOT), ("filed as it stands", "returned for revision")),
    # ------------------------------------------------------------------ audit_finding (record, HELD OUT)
    Q("af1", "audit_finding",
      "An internal audit recorded the finding that {A}. Is that finding {B} the information supplied?",
      "The finding that {A} is {B} the information supplied.",
      "The finding that {A} is not {B} the information supplied.",
      ("{d}", H_UNTRUE), ("in keeping with", "at variance with")),
    Q("af2", "audit_finding",
      "The auditors' working paper concludes that {A}. Would a reviewer of the information supplied need to {B} that "
      "conclusion?",
      "A reviewer of the information supplied would need to {B} the working paper's conclusion that {A}.",
      "A reviewer of the information supplied would not need to {B} the working paper's conclusion that {A}.",
      ("{d}", H_NOTHING), ("keep", "strike out")),
    Q("af3", "audit_finding",
      "An audit trail entry asserts that {A}. In view of the information supplied, should the entry be {B} in the "
      "final report?",
      "In view of the information supplied, the entry asserting that {A} should be {B} in the final report.",
      "In view of the information supplied, the entry asserting that {A} should not be {B} in the final report.",
      ("{d}", H_NOTRUTH), ("retained", "removed")),
    # ------------------------------------------------------------------ decision_direct
    Q("dd1", "decision_direct",
      "Going by the material given, is it {A} that {B}?",
      "Going by the material given, it is {A} that {B}.",
      "Going by the material given, it is not {A} that {B}.",
      ("established", "excluded"), ("{d}", T_NOT)),
    Q("dd2", "decision_direct",
      "Does the material given {A} the conclusion that {B}?",
      "The material given does {A} the conclusion that {B}.",
      "The material given does not {A} the conclusion that {B}.",
      ("lead to", "rule against"), ("{d}", T_FALSE)),
    Q("dd3", "decision_direct",
      "Read strictly, does the material given {A} that {B}?",
      "Read strictly, the material given does {A} that {B}.",
      "Read strictly, the material given does not {A} that {B}.",
      ("show", "deny"), ("{d}", T_CANNOT)),
    # ------------------------------------------------------------------ exception_scope
    Q("es1", "exception_scope",
      "With every condition and exception stated in the material applied, is the statement that {A} {B}?",
      "With every condition and exception stated in the material applied, the statement that {A} is {B}.",
      "With every condition and exception stated in the material applied, the statement that {A} is not {B}.",
      ("{d}", T_NOT), ("left standing", "overturned")),
    Q("es2", "exception_scope",
      "Once the qualifications stated in the material are applied, does the claim that {A} {B}?",
      "Once the qualifications stated in the material are applied, the claim that {A} does {B}.",
      "Once the qualifications stated in the material are applied, the claim that {A} does not {B}.",
      ("{d}", T_FALSE), ("hold", "break down")),
    Q("es3", "exception_scope",
      "Do the limits and exceptions stated in the material {A} the reading that {B}?",
      "The limits and exceptions stated in the material do {A} the reading that {B}.",
      "The limits and exceptions stated in the material do not {A} the reading that {B}.",
      ("leave intact", "defeat"), ("{d}", T_CANNOT)),
    # ------------------------------------------------------------------ gatekeeping
    Q("gk1", "gatekeeping",
      "A gate is meant to admit an item exactly when {d}. If the gate {A} this item, did it act {B}?",
      "The gate, meant to admit an item exactly when {d}, {A} this item and in doing so acted {B}.",
      "The gate, meant to admit an item exactly when {d}, {A} this item and in doing so did not act {B}.",
      ("admitted", "turned away"), ("properly", "improperly")),
    # R2 fix (1 Oct): was '... would it be {B} to {A} this case?' with A = clear / stop; 'clear a case' also reads
    # as 'close / dismiss it' (= stop it), which flips the answer. The keeping act now repeats the rule's own words.
    Q("gk2", "gatekeeping",
      "A rule lets a case proceed exactly when {d}. Given the material provided, would it be {B} to {A}?",
      "Under a rule that lets a case proceed exactly when {d}, and given the material provided, it would be {B} to "
      "{A}.",
      "Under a rule that lets a case proceed exactly when {d}, and given the material provided, it would not be {B} "
      "to {A}.",
      ("let this case proceed", "stop this case"), ("proper", "improper")),
    Q("gk3", "gatekeeping",
      "An approval step should pass an item exactly when {d}. When the step {A} this item, did it {B}?",
      "When the approval step, which should pass an item exactly when {d}, {A} this item, it did {B}.",
      "When the approval step, which should pass an item exactly when {d}, {A} this item, it did not {B}.",
      ("passed", "blocked"), ("work as designed", "misfire")),
    # ------------------------------------------------------------------ burden
    Q("bu1", "burden",
      "Does the material given {A} the burden of showing that {B}?",
      "The material given does {A} the burden of showing that {B}.",
      "The material given does not {A} the burden of showing that {B}.",
      ("meet", "fall short of"), ("{d}", T_NOT)),
    Q("bu2", "burden",
      "Is the conclusion that {A} {B} by the material given?",
      "The conclusion that {A} is {B} by the material given.",
      "The conclusion that {A} is not {B} by the material given.",
      ("{d}", T_FALSE), ("carried", "defeated")),
    Q("bu3", "burden",
      "Would the material given {A} a demand for proof that {B}?",
      "The material given would {A} a demand for proof that {B}.",
      "The material given would not {A} a demand for proof that {B}.",
      ("satisfy", "leave unmet"), ("{d}", T_CANNOT)),
    # ------------------------------------------------------------------ checklist
    Q("ck1", "checklist",
      "One checklist item says that {A}. Going by the material given, should that item be ticked as {B}?",
      "Going by the material given, the checklist item saying that {A} should be ticked as {B}.",
      "Going by the material given, the checklist item saying that {A} should not be ticked as {B}.",
      ("{d}", T_NOT), ("done", "not done")),
    Q("ck2", "checklist",
      "On the review checklist, the line saying that {A} still needs a mark. Going by the material given, does that "
      "line deserve a {B}?",
      "Going by the material given, the checklist line saying that {A} deserves a {B}.",
      "Going by the material given, the checklist line saying that {A} does not deserve a {B}.",
      ("{d}", T_FALSE), ("pass", "fail")),
    Q("ck3", "checklist",
      "A checklist asks reviewers to {A} the item stating that {B}. Should a reviewer of the material given do so?",
      "A reviewer of the material given should {A} the checklist item stating that {B}.",
      "A reviewer of the material given should not {A} the checklist item stating that {B}.",
      ("confirm", "reject"), ("{d}", T_CANNOT)),
    # ------------------------------------------------------------------ counter_hypothesis (HELD OUT)
    Q("ch1", "counter_hypothesis",
      "Would someone who {A} that {d} have to {B} that view after studying the information supplied?",
      "Someone who {A} that {d} would have to {B} that view after studying the information supplied.",
      "Someone who {A} that {d} would not have to {B} that view after studying the information supplied.",
      ("maintained", "denied"), ("keep", "give up")),
    Q("ch2", "counter_hypothesis",
      "A hypothetical analyst starts from the view that {A}. Does the information supplied {B} that starting view?",
      "The information supplied does {B} the starting view that {A}.",
      "The information supplied does not {B} the starting view that {A}.",
      ("{d}", H_UNTRUE), ("vindicate", "overturn")),
    Q("ch3", "counter_hypothesis",
      "Take the working hypothesis that {A}. Once the information supplied has been weighed, should the hypothesis be "
      "{B}?",
      "Once the information supplied has been weighed, the working hypothesis that {A} should be {B}.",
      "Once the information supplied has been weighed, the working hypothesis that {A} should not be {B}.",
      ("{d}", H_NOTHING), ("kept", "dropped")),
]
QUAD = {q["id"]: q for q in QUADS}
CELLS = ("00", "10", "01", "11")
CELL_ROLE = {"00": "para", "10": "neg", "01": "neg", "11": "dneg"}
CELL_FLIPS = {"00": 0, "10": 1, "01": 1, "11": 2}
CELL_NAME = {"00": "para", "10": "negA", "01": "negB", "11": "dneg"}
SLOT = "{d}"


def quads_of(family: str) -> list[str]:
    return [q["id"] for q in QUADS if q["family"] == family]


def is_record(qid: str) -> bool:
    return FAMILIES[QUAD[qid]["family"]]


def _fill(t: str, q: dict, cell: str) -> str:
    a, b = int(cell[0]), int(cell[1])
    return t.replace("{A}", q["A"][a]).replace("{B}", q["B"][b])


def cell_templates(qid: str, cell: str) -> tuple[str, str, str]:
    """(question, yes line, no line) of one cell, still with the {d} slot."""
    q = QUAD[qid]
    return _fill(q["q"], q, cell), _fill(q["y"], q, cell), _fill(q["n"], q, cell)


def render(qid: str, cell: str, d: str) -> tuple[str, str, str]:
    """The cell's question and its yes / no card lines with the proposition d filled in."""
    if not d or d != d.strip() or "{" in d or "}" in d:
        raise ValueError(f"bad proposition {d!r}")
    qt, yt, nt = cell_templates(qid, cell)
    return qt.replace(SLOT, d), yt.replace(SLOT, d), nt.replace(SLOT, d)


def gold(truth: bool, cell: str) -> bool:
    """SPEC 5 F4: gold = truth(P) XOR flipA XOR flipB."""
    return bool(truth) ^ (CELL_FLIPS[cell] % 2 == 1)


def all_templates(families=None) -> list[dict]:
    """Every cell question template as {quad, family, cell, text, flips, record} (text keeps the {d} slot)."""
    out = []
    for q in QUADS:
        if families is not None and q["family"] not in families:
            continue
        for c in CELLS:
            qt, yt, nt = cell_templates(q["id"], c)
            out.append({"quad": q["id"], "family": q["family"], "cell": c, "text": qt, "yes": yt, "no": nt,
                        "flips": CELL_FLIPS[c] % 2 == 1, "record": FAMILIES[q["family"]]})
    return out


DIALOGUE_CUES = ("reply", "replies", "commenter", "debate", "two notes", "agreed", "disagree", "back", "undercut")
SPEAKER_LABEL = re.compile(r"(^|[.?!]\s+)[A-Z][a-z]+:")
