"""v3_polarity_ladder: the independent decide2 for F4 `gen3_polarity_ladder` (yn2b SPEC 5 F4, 8.1). Builder C.

Written from the SPEC (sections 4, 5/F4, 8), `yn2b/F4_POLARITY_LADDER_FORMAT.md`, the frame TEXTS (the wording of
`yn2b/f4_templates.json`; its `flips` field is never read) and the RENDERED rows. It never imports or reads the
generator's decision code: `gen3_polarity_ladder.py`, `pl_frames.py` (gold, CELL_FLIPS, CELL_ROLE, QUADS) and
`pl_sources.py`. No model is called.

Per raw row (options ['yes','no']):
  1. parse_frame(instructions)  -> which of the 30 frame sentences it is, the proposition P (the `{d}` slot), and the
                                   polarity of every switch, read from this module's own lexicon:
                                     * inner negation in front of P ("it does not hold that", "it cannot be said
                                       that", "it is false to say that", "it is untrue that", "nothing supports the
                                       idea that", "there is no truth in saying that") reads as not-P (the format
                                       note: every F4 proposition is either established or ruled out);
                                     * the act a record or a person took on P (approved / rejected, endorsed /
                                       dismissed, reads approved / refused, marks as met / unmet, confirm / reject,
                                       maintained / denied, admitted / turned away, passed / blocked, let this
                                       case proceed / stop this case);
                                     * what the question asks of that record (sound / unsound, hold up / fall short,
                                       borne out / contradicted, justified / unjustified, kept / changed, ...).
                                   The answer is yes iff truth(P) XOR (an odd number of negative switches).
  2. classify_p(P)              -> the proposition kind from P's own wording: (a) `"L" is the listed <noun> that fits
                                   <x> best`, or one of the (b) program decisions (F1 outcome / record, F1b claim /
                                   log, F2 may / verdict / output, F3 statement / record, F6 term / record).
  3. truth(P)                   (a) L equals the human gold of the base golden_train row (`meta.derived_from`), whose
                                    state must equal this row's state, and both L and that gold must be labels the
                                    card lists.
                                (b) P is rebuilt into the source family's own question wording and handed, with THIS
                                    row's state and THIS row's card lines (the source extra lines, plus 'the
                                    statement holds'/'fails' as the yes/no lines), to that family's independent
                                    decide2: v3_rule_chain (F1, F1b), v3_tool_guard (F2), v3_state_track (F3; P is
                                    read as its JB yes-statement, or as one of its judge questions), v3_def_literal
                                    (F6). A row whose truth needs the card (F1b rules, F6 definition, (a) labels) but
                                    whose card is not shown (card_style none) is UNDEFINED.
  4. decide2_row(row)           -> 'yes' / 'no', or mv_core.UNDEFINED when any step cannot be read unambiguously.

decide2 never reads gold, tier, polarity, role, view, tpl, renderer, shortcut fields or `yn2b/f4_sources.json`.
Besides state / instructions / options / card it reads only `meta.defs` (the card pointer), `meta.card_style`
(whether the card is shown) and, for (a), `meta.derived_from` (the base row whose human label is P's truth).

The REPORT (never the solver) also runs a second route for (b): it looks the source row up through
`yn2b/f4_sources.json` (src_key, src_rid), checks that the state and card lines were copied from it, runs the source
family's decide2 on that original row and compares it with route 1. It also cross-checks meta (polarity, renderer,
P) and the complement / equiv relations under decide2's answers.

CLI (from lean/):
  ../.venv/bin/python golden_src/gen3/v3_polarity_ladder.py           agreement + structure + cross-checks (prints)
  ../.venv/bin/python golden_src/gen3/v3_polarity_ladder.py --quick   agreement only
  ../.venv/bin/python golden_src/gen3/v3_polarity_ladder.py --write   also writes yn2b/v3_polarity_ladder_agreement.json
                                                                      and appends its sha256 to MANIFEST_yn2b.jsonl
Tests: yn2b/tests/test_v3_polarity_ladder.py.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
RAW = LEAN / "data" / "v14_parts" / "yn2b_raw"
DEFS = LEAN / "data" / "v14_parts" / "yn2b_defs"
GOLDEN_TRAIN = LEAN / "data" / "v14_parts" / "golden_train.jsonl"
SOURCES = LEAN / "yn2b" / "f4_sources.json"  # REPORT ONLY (route 2); the solver never opens it
REPORT_PATH = LEAN / "yn2b" / "v3_polarity_ladder_agreement.json"
KEY = "gen3_polarity_ladder"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import mv_core  # noqa: E402  (shared engine: UNDEFINED, load_defs; no F4 decision logic lives there)

UNDEFINED = mv_core.UNDEFINED
FORBIDDEN_IMPORTS = ("gen3_polarity_ladder", "pl_frames", "pl_sources")  # checked by the tests


class ParseError(Exception):
    pass


# ================================================================================================ 1. the frame
# Inner negation placed in front of P. Each reads as "P is false" (format note: P is established or ruled out).
NEG_INNER = (
    "it does not hold that",
    "it cannot be said that",
    "it is false to say that",
    "it is untrue that",
    "nothing supports the idea that",
    "there is no truth in saying that",
)

# R2 (1 Oct): two frame texts were re-synced with the reworded F4 frames (compliance_flag.scanner: 'attached a note
# ... is that note well founded / unfounded'; gatekeeping.rule: 'let this case proceed / stop this case'); the signs
# are read from the English wording like every other entry.
# The 30 frame sentences. {C} is the content clause: an optional inner negation, then P. A switch slot
# {name:word+|word-} lists its wordings; '+' keeps the sense of P, '-' reverses it. The signs are this module's own
# reading of each word (what makes the record / act / test come out yes), not a copy of any generator table.
FRAMES = [
    # a record states a verdict on C; the question asks whether the record is right (+) or wrong (-)
    ("verdict_record.logged",
     "An automated check logged the verdict that {C}. Going by the material given, is that logged verdict "
     "{ask:sound+|unsound-}?"),
    ("verdict_record.field",
     "A review field on file states that {C}. Measured against the material given, does that field "
     "{ask:hold up+|fall short-}?"),
    ("verdict_record.caselog",
     "The case log records the determination that {C}. Is that determination {ask:borne out+|contradicted-} by the "
     "material given?"),
    # someone took an act on C (accept + / refuse -); the question asks whether the act was right (+) or wrong (-)
    ("sign_off.supervisor",
     "Before closing the file, a supervisor {act:approved+|rejected-} the statement that {C}. Given the material "
     "provided, was that action {ask:justified+|unjustified-}?"),
    ("sign_off.mark",
     "The approval mark beside the line saying that {C} reads {act:approved+|refused-}. Should that mark be "
     "{ask:kept as it is+|changed-}?"),
    ("sign_off.lead",
     "At sign-off, a team lead {act:endorsed+|dismissed-} the claim that {C}. Would a careful check of the material "
     "given {ask:uphold+|overturn-} that call?"),
    ("compliance_flag.scanner",
     "A compliance scanner attached a note to this file stating that {C}. Given the material provided, is that note "
     "{ask:well founded+|unfounded-}?"),
    ("compliance_flag.tracker",
     "The compliance tracker marks the requirement that {C} as {act:met+|unmet-}. Does the material given "
     "{ask:support+|contradict-} that marking?"),
    ("compliance_flag.report",
     "An exception report states that {C}. Given the material provided, should the report be "
     "{ask:filed as it stands+|returned for revision-}?"),
    ("audit_finding.finding",
     "An internal audit recorded the finding that {C}. Is that finding {ask:in keeping with+|at variance with-} the "
     "information supplied?"),
    ("audit_finding.paper",
     "The auditors' working paper concludes that {C}. Would a reviewer of the information supplied need to "
     "{ask:keep+|strike out-} that conclusion?"),
    ("audit_finding.trail",
     "An audit trail entry asserts that {C}. In view of the information supplied, should the entry be "
     "{ask:retained+|removed-} in the final report?"),
    # the material is asked directly whether it shows C (+) or its denial (-)
    ("decision_direct.established",
     "Going by the material given, is it {ask:established+|excluded-} that {C}?"),
    ("decision_direct.conclusion",
     "Does the material given {ask:lead to+|rule against-} the conclusion that {C}?"),
    ("decision_direct.show",
     "Read strictly, does the material given {ask:show+|deny-} that {C}?"),
    ("exception_scope.statement",
     "With every condition and exception stated in the material applied, is the statement that {C} "
     "{ask:left standing+|overturned-}?"),
    ("exception_scope.claim",
     "Once the qualifications stated in the material are applied, does the claim that {C} {ask:hold+|break down-}?"),
    ("exception_scope.reading",
     "Do the limits and exceptions stated in the material {ask:leave intact+|defeat-} the reading that {C}?"),
    # a gate lets an item through exactly when C; it let it through (+) or stopped it (-); was that proper (+) or
    # improper (-)
    ("gatekeeping.gate",
     "A gate is meant to admit an item exactly when {C}. If the gate {act:admitted+|turned away-} this item, did it "
     "act {ask:properly+|improperly-}?"),
    ("gatekeeping.rule",
     "A rule lets a case proceed exactly when {C}. Given the material provided, would it be "
     "{ask:proper+|improper-} to {act:let this case proceed+|stop this case-}?"),
    ("gatekeeping.step",
     "An approval step should pass an item exactly when {C}. When the step {act:passed+|blocked-} this item, did it "
     "{ask:work as designed+|misfire-}?"),
    # the burden of showing C is met (+) or not (-)
    ("burden.meet",
     "Does the material given {ask:meet+|fall short of-} the burden of showing that {C}?"),
    ("burden.carried",
     "Is the conclusion that {C} {ask:carried+|defeated-} by the material given?"),
    ("burden.proof",
     "Would the material given {ask:satisfy+|leave unmet-} a demand for proof that {C}?"),
    # a checklist line says C; should it pass (+) or fail (-)
    ("checklist.tick",
     "One checklist item says that {C}. Going by the material given, should that item be ticked as "
     "{ask:done+|not done-}?"),
    ("checklist.mark",
     "On the review checklist, the line saying that {C} still needs a mark. Going by the material given, does that "
     "line deserve a {ask:pass+|fail-}?"),
    ("checklist.confirm",
     "A checklist asks reviewers to {act:confirm+|reject-} the item stating that {C}. Should a reviewer of the "
     "material given do so?"),
    # a starting view holds C (+) or denies it (-); the evidence keeps (+) or overturns (-) it
    ("counter_hypothesis.someone",
     "Would someone who {act:maintained+|denied-} that {C} have to {ask:keep+|give up-} that view after studying the "
     "information supplied?"),
    ("counter_hypothesis.analyst",
     "A hypothetical analyst starts from the view that {C}. Does the information supplied "
     "{ask:vindicate+|overturn-} that starting view?"),
    ("counter_hypothesis.hypothesis",
     "Take the working hypothesis that {C}. Once the information supplied has been weighed, should the hypothesis be "
     "{ask:kept+|dropped-}?"),
]

_SLOT = re.compile(r"\{C\}|\{(\w+):([^}]+)\}")


def _compile(tpl: str):
    parts, signs, pos = [], {}, 0
    for m in _SLOT.finditer(tpl):
        parts.append(re.escape(tpl[pos:m.start()]))
        if m.group(0) == "{C}":
            neg = "|".join(re.escape(n + " ") for n in sorted(NEG_INNER, key=len, reverse=True))
            parts.append(rf"(?P<inner>{neg})?(?P<d>.+?)")
        else:
            name, alts = m.group(1), m.group(2).split("|")
            words = {}
            for a in alts:
                if a[-1] not in "+-":
                    raise ValueError(f"switch alternative without a sign: {a!r}")
                words[a[:-1]] = a[-1] == "-"
            signs[name] = words
            parts.append(f"(?P<{name}>" + "|".join(re.escape(w) for w in sorted(words, key=len, reverse=True)) + ")")
        pos = m.end()
    parts.append(re.escape(tpl[pos:]))
    return re.compile("".join(parts)), signs


COMPILED = [(name, *_compile(tpl)) for name, tpl in FRAMES]
HELD_OUT_FAMILIES = ("audit_finding", "counter_hypothesis")  # SPEC 5 F4: dev_holdout only (report check)


@dataclass
class Frame:
    name: str
    d: str                       # the proposition P
    inner: str | None            # the inner negation wording, if any
    switches: dict               # switch name -> chosen wording
    negatives: list              # the switches that reverse the sense ('inner' included)

    @property
    def flips(self) -> int:
        return len(self.negatives)

    @property
    def family(self) -> str:
        return self.name.split(".")[0]


def _frame_hit(instr: str):
    hits = []
    for name, rx, signs in COMPILED:
        m = rx.fullmatch(instr)
        if m:
            hits.append((name, m, signs))
    if len(hits) != 1:
        raise ParseError(f"question matches {len(hits)} frames: {instr!r}")
    return hits[0]


def parse_frame(instr: str) -> Frame:
    name, m, signs = _frame_hit(instr)
    g = m.groupdict()
    d = g["d"]
    if any(d.startswith(n + " ") for n in NEG_INNER):
        raise ParseError(f"stacked inner negation: {d!r}")
    switches = {k: g[k] for k in signs}
    negatives = (["inner"] if g["inner"] else []) + [k for k in signs if signs[k][g[k]]]
    return Frame(name, d, g["inner"].strip() if g["inner"] else None, switches, negatives)


# ================================================================================================ 2. the proposition
_CL = r"(?P<clause>(?:[A-Z][a-z]+ )+\d+)"
_EN = r"(?P<ent>[a-z]+)"
_TM = r"(?P<term>(?:an? )?'[^']+')"
_RG = r"(?P<reg>[a-z][a-z ]*?)"

# (kind, P regex, source question template filled from the groups). The question templates are the source
# families' own yes/no wordings (each family's decide2 parses them); P is the same claim stated as a clause.
P_FORMS = [
    ("a", r'"(?P<L>[^"]+)" is the listed (?P<noun>[A-Za-z][A-Za-z -]*?) that fits (?P<obj>.+) best', None),
    ("f1.outcome", r'the outcome of this (?P<req>[a-z][\w -]*?) under the (?P<doc>[a-z][\w -]*?) is "(?P<x>[^"]+)"',
     'Under the {doc}, is the outcome of this {req} "{x}"?'),
    ("f1.record", r"the decision recorded in the case file for this (?P<req>[a-z][\w -]*?) is consistent with the "
                  r"(?P<doc>[a-z][\w -]*)",
     "Is the decision recorded for this {req} in line with the {doc}, rather than at odds with it?"),
    ("f1b.claim", r"under the rules in the card, the evidence establishes the claim",
     "Under the rules in the card, does the evidence establish the claim?"),
    ("f1b.log", r"under the card's rules, the fact-check log entry for this claim is consistent with the evidence",
     "The fact-check log has an entry for this claim. Is that entry consistent with the evidence under the card's "
     "rules, rather than at odds with it?"),
    ("f2.may", r"the proposed call may run under the policy",
     "Is the proposed call allowed to run under the policy?"),
    ("f2.verdict", r"the verdict the guardrail logged for the proposed call is consistent with the policy",
     "Is the verdict the guardrail logged for the proposed call consistent with the policy?"),
    ("f2.output", r"the assistant's output meets every requirement stated for it",
     "Is every stated requirement met by the assistant's output?"),
    ("f3.record", r"the agent's recorded state is consistent with the log under the numbered rules",
     "Is the agent's recorded state consistent with the log under the numbered rules?"),
    ("f3.record", r"every value in the agent record is supported by the log and the numbered rules",
     "Is every value in the agent record supported by the log and the numbered rules?"),
    ("f3.record", r"every entry of the agent record matches what the log gives under the numbered rules",
     "Does every entry of the agent record match what the log gives under the numbered rules?"),
    ("f6.term", rf"the {_EN} is {_TM} under {_CL} of the (?P<instr>.+)",
     "Under {clause} of the {instr}, is the {ent} {term}?"),
    ("f6.term", rf"the {_EN} is {_TM} by the definition in {_CL}, not by everyday usage",
     "Going by the definition in {clause} and not by everyday usage, is the {ent} {term}?"),
    ("f6.term", rf"the {_EN} counts as {_TM} as {_CL} defines that term",
     "Does the {ent} count as {term} as {clause} defines that term?"),
    ("f6.term", rf"the {_EN} qualifies as {_TM} under the definition in {_CL} alone",
     "Applying only the definition in {clause}, with no outside rules, does the {ent} qualify as {term}?"),
    ("f6.term", rf"the {_EN} should be classed as {_TM} with {_CL} as the binding definition",
     "Taking {clause} as the binding definition, should the {ent} be classed as {term}?"),
    ("f6.record", rf"the classification recorded in the {_RG} for this {_EN} is consistent with {_CL}",
     "Is the classification recorded in the {reg} for this {ent} consistent with {clause}?"),
    ("f6.record", rf"the {_EN}'s recorded classification is supported by the definition in {_CL}",
     "Is the {ent}'s recorded classification supported by the definition in {clause}?"),
    ("f6.record", rf"{_CL} supports the classification the {_RG} records for the {_EN}",
     "Does {clause} support the classification the {reg} records for the {ent}?"),
    ("f6.record", rf"the classification on file for the {_EN} is consistent with the definition in {_CL}",
     "Under {clause}, is the classification on file for the {ent} consistent with the definition?"),
    ("f6.record", rf"the entry in the {_RG} for this {_EN} is backed by {_CL} as written",
     "Is the entry in the {reg} for this {ent} backed by {clause} as written?"),
]
P_FORMS = [(k, re.compile(rx), q) for k, rx, q in P_FORMS]

# F3: P is the machine's JB yes-statement; v3_state_track reads statements that start with a capital and end '.'.
_F3_LOWER_LEADS = ("order ", "ticket ", "at least ", "fewer than ", "account ", "the ")


def f3_statement(p: str) -> str:
    return (p[0].upper() + p[1:] if p.startswith(_F3_LOWER_LEADS) else p) + "."


def _v3(name: str):
    import importlib
    return importlib.import_module(name)


@dataclass
class Prop:
    kind: str                    # 'a', 'f1.outcome', ..., 'f3.state', 'f6.record'
    text: str
    groups: dict = field(default_factory=dict)
    question: str | None = None  # the rebuilt source question (b), or the F3 statement


def classify_p(p: str) -> Prop:
    hits = []
    for kind, rx, q in P_FORMS:
        m = rx.fullmatch(p)
        if m:
            g = m.groupdict()
            hits.append(Prop(kind, p, g, q.format(**g) if q else None))
    st = _v3("v3_state_track")
    m, _ = st._match(st.STMT, f3_statement(p))
    if m:
        hits.append(Prop("f3.state", p, m.groupdict(), f3_statement(p)))
    if len(hits) != 1:
        raise ParseError(f"proposition matches {len(hits)} forms ({[h.kind for h in hits]}): {p!r}")
    return hits[0]


# ================================================================================================ 3. truth of P
HOLDS, FAILS = "the statement holds", "the statement fails"


def card_of(row: dict) -> dict:
    if row.get("_defs") is not None:
        return row["_defs"]
    qid = (row.get("meta") or {}).get("defs")
    if not qid:
        raise ParseError("row without a card")
    p = DEFS / f"{KEY}__{qid}.json"
    if not p.exists():
        raise ParseError(f"card file missing: {p.name}")
    return json.loads(p.read_text())


def card_parts(card: dict) -> dict:
    """Splits a card into its lines: task, labels / extra lines, holds, fails, yes, no (in this order)."""
    keys = list(card)
    if keys[-2:] != ["yes", "no"] or keys[-4:-2] != [HOLDS, FAILS]:
        raise ParseError(f"card does not end with holds / fails / yes / no: {keys}")
    body = keys[:-4]
    task = card[body[0]] if body and body[0] == "task" else None
    extra = {k: card[k] for k in (body[1:] if task is not None else body)}
    return {"task": task, "extra": extra, "holds": card[HOLDS], "fails": card[FAILS], "yes": card["yes"],
            "no": card["no"]}


def _shown(row: dict) -> bool:
    return (row.get("meta") or {}).get("card_style") != "none"


# ---- (a): the human gold of the base golden_train row
_GOLD: dict = {}


def prefetch_golden(ids) -> None:
    """One pass over golden_train.jsonl (1.2 GB) that caches the base rows named by `ids` (state, options, gold)."""
    want = {i for i in ids if i not in _GOLD}
    if not want:
        return
    pre = b'{"id": "'
    with open(GOLDEN_TRAIN, "rb") as f:
        for line in f:
            if not line.startswith(pre):
                continue
            j = line.find(b'"', len(pre))
            rid = line[len(pre):j].decode()
            if rid in want:
                r = json.loads(line)
                _GOLD[rid] = {"state": r["state"], "options": r.get("options"), "gold": r["gold"],
                              "source": r.get("source"), "group_id": r.get("group_id")}
                want.discard(rid)
                if not want:
                    break
    for rid in want:
        _GOLD[rid] = None


def golden_row(rid: str):
    if rid not in _GOLD:
        prefetch_golden(_all_derived_ids() | {rid})
    return _GOLD.get(rid)


def _all_derived_ids() -> set:
    out = set()
    for part in ("train", "dev"):
        p = _raw_path(part)
        if p.exists():
            for r in _read_jsonl(p):
                if (r.get("meta") or {}).get("derived_from"):
                    out.add(r["meta"]["derived_from"])
    return out


def truth_a(row: dict, prop: Prop, card: dict) -> dict:
    if not _shown(row):
        raise ParseError("(a) row whose card (the label definitions) is not shown")
    base_id = (row.get("meta") or {}).get("derived_from")
    if not base_id:
        raise ParseError("(a) row without meta.derived_from")
    base = golden_row(base_id)
    if base is None:
        raise ParseError(f"base row {base_id} not in golden_train")
    if base["state"] != row["state"]:
        raise ParseError(f"state differs from the base row {base_id}")
    parts = card_parts(card)
    labels = list(parts["extra"])
    L, gold = prop.groups["L"], base["gold"]
    if not isinstance(gold, str) or gold not in (base["options"] or []):
        raise ParseError(f"base row gold {gold!r} is not one of its options")
    if L not in base["options"]:
        raise ParseError(f"quoted label {L!r} is not an option of the base row")
    if L not in labels or gold not in labels:
        raise ParseError(f"the card lists {labels}, not both {L!r} and the human gold {gold!r}")
    return {"truth": L == gold, "route": "golden_train", "base_id": base_id, "human_gold": gold, "L": L,
            "labels": labels}


# ---- (b): the source family's decide2 on THIS row's state, the rebuilt question and THIS row's card lines
_PROBE_QID = "__v3_polarity_ladder_probe__"


def truth_b(row: dict, prop: Prop, card: dict) -> dict:
    parts = card_parts(card)
    fam = prop.kind.split(".")[0]
    probe = {"state": row["state"], "instructions": prop.question, "options": ["yes", "no"],
             "meta": {"defs": _PROBE_QID, "fmt": (row.get("meta") or {}).get("fmt")}}
    if fam == "f1" or fam == "f1b":
        rc = _v3("v3_rule_chain")
        if fam == "f1b":
            if not _shown(row):
                raise ParseError("F1b rules are printed only in the card, which is not shown")
            if parts["task"] is not None:
                raise ParseError("F1b card with a task line")
            pc = {**parts["extra"], "yes": parts["holds"], "no": parts["fails"]}
            old = rc.CARD_LOOKUP
            rc.set_card_lookup(lambda q: pc if q == _PROBE_QID else (old(q) if old else None))
            try:
                ans = rc.decide2_row_strict(probe)
            except (rc.ParseError, KeyError, ValueError, ZeroDivisionError, json.JSONDecodeError) as e:
                raise ParseError(f"v3_rule_chain: {type(e).__name__}: {e}") from None
            finally:
                rc.set_card_lookup(old)
        else:
            try:
                ans = rc.decide2_row_strict(probe)
            except (rc.ParseError, KeyError, ValueError, ZeroDivisionError, json.JSONDecodeError) as e:
                raise ParseError(f"v3_rule_chain: {type(e).__name__}: {e}") from None
        solver = "v3_rule_chain"
    elif fam == "f2":
        tg = _v3("v3_tool_guard")
        try:
            info = tg.solve(probe)
        except (tg.SolverError, KeyError, ValueError, json.JSONDecodeError) as e:
            raise ParseError(f"v3_tool_guard: {type(e).__name__}: {e}") from None
        expect = {"f2.may": "may", "f2.verdict": "judge", "f2.output": "output"}[prop.kind]
        if (info["family"], info["negated"]) != (expect, False):
            raise ParseError(f"v3_tool_guard read the rebuilt question as {info['family']}/{info['negated']}")
        ans = info["answer"]
        solver = "v3_tool_guard"
    elif fam == "f3":
        st = _v3("v3_state_track")
        try:
            s = st.Solver(probe)
            if prop.kind == "f3.state":
                ans = "yes" if s.statement(prop.question) else "no"
            else:
                if not any(re.fullmatch(p, prop.question) for p in st.JUDGE_Q):
                    raise ParseError(f"rebuilt judge question not read by v3_state_track: {prop.question!r}")
                ans = s.answer()
        except st.SolverError as e:
            raise ParseError(f"v3_state_track: {e}") from None
        solver = "v3_state_track"
    elif fam == "f6":
        dl = _v3("v3_def_literal")
        if not _shown(row):
            raise ParseError("the F6 definition is printed only in the card, which is not shown")
        if parts["task"] is not None or len(parts["extra"]) != 1:
            raise ParseError(f"F6 card needs exactly one definition line, has {list(parts['extra'])}")
        probe["_defs"] = {**parts["extra"], "yes": parts["holds"], "no": parts["fails"]}
        try:
            info = dl.solve(probe)
        except (dl.ParseError, KeyError, ValueError) as e:
            raise ParseError(f"v3_def_literal: {type(e).__name__}: {e}") from None
        want = "is" if prop.kind == "f6.term" else "judge"
        if (info["q"]["family"], info["q"]["neg"]) != (want, False):
            raise ParseError(f"v3_def_literal read the rebuilt question as {info['q']['family']}")
        ans = info["answer"]
        solver = "v3_def_literal"
    else:  # pragma: no cover
        raise ParseError(f"no solver for {prop.kind}")
    if ans not in ("yes", "no"):
        raise ParseError(f"{solver} answered {ans!r}")
    return {"truth": ans == "yes", "route": solver, "question": prop.question}


def truth(row: dict, prop: Prop, card: dict) -> dict:
    return truth_a(row, prop, card) if prop.kind == "a" else truth_b(row, prop, card)


# ================================================================================================ 4. the row
def solve(row: dict) -> dict:
    """Everything decide2 reads and concludes for one row (raises ParseError)."""
    if list(row.get("options") or []) != ["yes", "no"]:
        raise ParseError(f"F4 rows are yes/no; options {row.get('options')}")
    fr = parse_frame(row["instructions"])
    prop = classify_p(fr.d)
    card = card_of(row)
    t = truth(row, prop, card)
    yes = t["truth"] != (fr.flips % 2 == 1)
    return {"answer": "yes" if yes else "no", "frame": fr.name, "family": fr.family, "flips": fr.flips,
            "negatives": fr.negatives, "switches": fr.switches, "inner": fr.inner, "P": fr.d, "kind": prop.kind,
            **{k: v for k, v in t.items() if k != "labels"}}


def decide2_row(row: dict):
    """SPEC 8.1 entry point (mv_core.verify_labels): 'yes' / 'no', or UNDEFINED if the row cannot be read."""
    try:
        return solve(row)["answer"]
    except ParseError:
        return UNDEFINED


decide2_row_safe = decide2_row


# ================================================================================================ 5. reports
def _raw_path(part: str) -> Path:
    return RAW / (f"{KEY}.jsonl" if part == "train" else f"dev/{KEY}.jsonl")


def _rel_path(part: str) -> Path:
    return RAW / ("relations" if part == "train" else "dev/relations") / f"{KEY}.jsonl"


def _read_jsonl(p: Path) -> list:
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]


def load_rows(part: str = "train") -> list:
    return _read_jsonl(_raw_path(part))


def load_rels(part: str = "train") -> list:
    p = _rel_path(part)
    return _read_jsonl(p) if p.exists() else []


def _try(row: dict):
    try:
        return solve(row), None
    except ParseError as e:
        return None, str(e)


def agreement(rows: list) -> dict:
    prefetch_golden({r["meta"]["derived_from"] for r in rows if r["meta"].get("derived_from")})
    tab = defaultdict(Counter)
    dis, answers, infos = [], {}, {}
    for r in rows:
        info, err = _try(r)
        g2 = info["answer"] if info else None
        answers[r["rid"]] = g2
        infos[r["rid"]] = info
        m = r["meta"]
        key = f"{m.get('dev_kind') or 'train'}/{m['pack'].split('.')[0]}/{m['view']}/p{m['polarity']}"
        ok = g2 == r["gold"]
        tab[key]["agree" if ok else "disagree"] += 1
        if not ok:
            dis.append({"rid": r["rid"], "gold": r["gold"], "decide2": g2, "error": err,
                        "frame": info and info["frame"], "kind": info and info["kind"]})
    n = len(rows)
    agree = n - len(dis)
    return {"rows": n, "agree": agree, "rate": round(agree / max(1, n), 6), "disagreements": dis,
            "table": {k: dict(v) for k, v in sorted(tab.items())}, "answers": answers, "infos": infos}


def structure_under_decide2(rows: list, rels: list, answers: dict) -> dict:
    """SPEC 8.3: complement views invert decide2's answer, equiv views keep it (every relation is checked)."""
    by = {r["rid"]: r for r in rows}
    out = {"complement": 0, "equiv": 0, "complement_not_inverted": [], "equiv_changed": [], "unknown_rel": [],
           "same_state_broken": []}
    for rel in rels:
        a, b, t = rel["a"], rel["b"], rel["type"]
        if a not in by or b not in by or t not in ("complement", "equiv"):
            out["unknown_rel"].append(rel)
            continue
        if by[a]["state"] != by[b]["state"]:
            out["same_state_broken"].append([a, b])
        x, y = answers.get(a), answers.get(b)
        if t == "complement":
            out["complement"] += 1
            if x is None or y is None or x == y:
                out["complement_not_inverted"].append([a, b])
        else:
            out["equiv"] += 1
            if x is None or y is None or x != y:
                out["equiv_changed"].append([a, b])
    return out


def mutations(row: dict) -> list:
    """Wording probes for one row: (description, mutated row, answer must invert?). Every switch is set to its
    opposite-sense wording (must invert), the inner negation is added or removed (must invert) or swapped for
    another inner negation (must not change)."""
    instr = row["instructions"]
    _, m, signs = _frame_hit(instr)
    out = []
    for sw, words in signs.items():
        cur = m.group(sw)
        s, e = m.span(sw)
        for w, neg in words.items():
            if neg != words[cur]:
                out.append((f"{sw}: {cur} -> {w}", instr[:s] + w + instr[e:], True))
    if m.group("inner"):
        s, e = m.span("inner")
        cur = m.group("inner").strip()
        out.append(("inner: remove", instr[:s] + instr[e:], True))
        for alt in NEG_INNER:
            if alt != cur:
                out.append((f"inner: {cur} -> {alt}", instr[:s] + alt + " " + instr[e:], False))
    else:
        s = m.start("d")
        out.append(("inner: add", instr[:s] + NEG_INNER[0] + " " + instr[s:], True))
    return [(desc, {**row, "instructions": q}, inv) for desc, q, inv in out]


def sensitivity(rows: list, answers: dict) -> dict:
    """decide2 really reads the wording: every probe of `mutations` moves the answer the way it says."""
    out = {"probes": 0, "ok": 0, "failed": []}
    for r in rows:
        a = answers.get(r["rid"])
        if a is None:
            continue
        for desc, mr, inv in mutations(r):
            out["probes"] += 1
            b = decide2_row(mr)
            want = ("no" if a == "yes" else "yes") if inv else a
            if b == want:
                out["ok"] += 1
            else:
                out["failed"].append([r["rid"], desc, None if b is UNDEFINED else b])
    return out


def meta_crosscheck(rows: list, infos: dict) -> dict:
    """Report only: decide2's own reading against the row's meta and the build's source file (never used above)."""
    src = json.loads(SOURCES.read_text())["latents"] if SOURCES.exists() else {}
    out = {"polarity": [], "role": [], "view": [], "renderer": [], "P_vs_sources": [], "derived_from": [],
           "held_out_frame_outside_holdout": [], "holdout_with_training_frame": [], "frames": Counter(),
           "frame_family_by_split": defaultdict(Counter), "inner_negations": Counter(), "flips": Counter()}
    for r in rows:
        info = infos.get(r["rid"])
        if not info:
            continue
        m = r["meta"]
        rid = r["rid"]
        out["frames"][info["frame"]] += 1
        split = m.get("dev_kind") or "train"
        out["frame_family_by_split"][split][info["family"]] += 1
        out["flips"][info["flips"]] += 1
        if info["inner"]:
            out["inner_negations"][info["inner"]] += 1
        if info["flips"] != m.get("polarity"):
            out["polarity"].append([rid, info["flips"], m.get("polarity")])
        if {0: "para", 1: "neg", 2: "dneg"}.get(info["flips"]) != m.get("role"):
            out["role"].append([rid, info["flips"], m.get("role")])
        if (info["flips"] == 0) != (m.get("view") == "base"):
            out["view"].append([rid, info["flips"], m.get("view")])
        ren = m.get("renderer") or ""
        if (info["kind"] == "a") != ren.startswith("a.") or (info["kind"] != "a" and info["kind"] != ren):
            out["renderer"].append([rid, info["kind"], ren])
        s = src.get(m.get("latent_id"))
        if s is not None and s.get("P") != info["P"]:
            out["P_vs_sources"].append([rid, info["P"], s.get("P")])
        if info["kind"] == "a" and s is not None and s.get("base_id") != m.get("derived_from"):
            out["derived_from"].append([rid, s.get("base_id"), m.get("derived_from")])
        held = info["family"] in HELD_OUT_FAMILIES
        if held and split != "holdout":
            out["held_out_frame_outside_holdout"].append(rid)
        if split == "holdout" and not held:
            out["holdout_with_training_frame"].append(rid)
    out["frames"] = dict(sorted(out["frames"].items()))
    out["frame_family_by_split"] = {k: dict(sorted(v.items())) for k, v in out["frame_family_by_split"].items()}
    out["inner_negations"] = dict(out["inner_negations"])
    out["flips"] = dict(sorted(out["flips"].items()))
    return out


# ---- route 2 (report only): the original source row, through yn2b/f4_sources.json
SRC_DECIDE2 = {"gen3_rule_chain": "v3_rule_chain", "gen3_tool_guard": "v3_tool_guard",
               "gen3_state_track": "v3_state_track", "gen3_def_literal": "v3_def_literal"}
_SRC_ROWS: dict = {}


def _source_row(key: str, rid: str):
    if key not in _SRC_ROWS:
        idx = {}
        for p in (RAW / f"{key}.jsonl", RAW / "dev" / f"{key}.jsonl"):
            if p.exists():
                for r in _read_jsonl(p):
                    idx[r["rid"]] = r
        _SRC_ROWS[key] = idx
    return _SRC_ROWS[key].get(rid)


def _src_card(key: str, row: dict):
    qid = (row.get("meta") or {}).get("defs")
    return mv_core.load_defs(key, qid) if qid else None


def source_crosscheck(rows: list, infos: dict) -> dict:
    """For every (b) row: the state and card lines were copied from the source row, the source family's decide2 on
    the ORIGINAL source row gives the same truth as route 1, and the source row's own gold agrees."""
    src = json.loads(SOURCES.read_text())["latents"] if SOURCES.exists() else {}
    out = {"b_rows": 0, "route2_agree": 0, "route2_disagree": [], "route2_undefined": [], "state_not_copied": [],
           "extra_lines_not_copied": [], "holds_fails_not_source_yes_no": [], "source_gold_vs_route1": [],
           "missing_source": [], "by_kind": Counter()}
    for r in rows:
        info = infos.get(r["rid"])
        if not info or info["kind"] == "a":
            continue
        out["b_rows"] += 1
        out["by_kind"][info["kind"]] += 1
        s = src.get(r["meta"]["latent_id"])
        sr = _source_row(s["src_key"], s["src_rid"]) if s else None
        if sr is None:
            out["missing_source"].append(r["rid"])
            continue
        if sr["state"] != r["state"]:
            out["state_not_copied"].append(r["rid"])
        sc = _src_card(s["src_key"], sr) or {}
        parts = card_parts(card_of(r))
        if {k: v for k, v in sc.items() if k not in ("yes", "no")} != parts["extra"]:
            out["extra_lines_not_copied"].append(r["rid"])
        if (sc.get("yes"), sc.get("no")) != (parts["holds"], parts["fails"]):
            out["holds_fails_not_source_yes_no"].append(r["rid"])
        mod = _v3(SRC_DECIDE2[s["src_key"]])
        a2 = mod.decide2_row(sr)
        t1 = info["truth"]  # route 1's truth of P
        if a2 not in ("yes", "no"):
            out["route2_undefined"].append(r["rid"])
        elif (a2 == "yes") == t1:
            out["route2_agree"] += 1
        else:
            out["route2_disagree"].append([r["rid"], s["src_rid"], a2])
        if (sr["gold"] == "yes") != t1:
            out["source_gold_vs_route1"].append([r["rid"], s["src_rid"], sr["gold"]])
    out["by_kind"] = dict(sorted(out["by_kind"].items()))
    return out


def card_report(rows: list, infos: dict) -> dict:
    """The card says what the question asks: its yes/no lines restate the question around the same P, (a) cards
    describe L in 'the statement holds' and list L and the human gold among the labels."""
    out = {"rows": 0, "P_missing_from_yes_no": [], "a_holds_without_L": [], "a_fails_without_L": [],
           "no_line_not_negated": [], "cards_needed_but_hidden": []}
    for r in rows:
        info = infos.get(r["rid"])
        if not info:
            continue
        out["rows"] += 1
        parts = card_parts(card_of(r))
        if info["P"] not in parts["yes"] or info["P"] not in parts["no"]:
            out["P_missing_from_yes_no"].append(r["rid"])
        if not re.search(r"\bnot\b", parts["no"].replace(info["P"], "")):
            out["no_line_not_negated"].append(r["rid"])
        if info["kind"] == "a":
            q = f'"{info["L"]}"'
            if not parts["holds"].startswith(q):
                out["a_holds_without_L"].append(r["rid"])
            if q not in parts["fails"]:
                out["a_fails_without_L"].append(r["rid"])
        if not _shown(r) and (info["kind"] == "a" or info["kind"].startswith(("f1b", "f6"))):
            out["cards_needed_but_hidden"].append(r["rid"])
    return out


def diagnose(row: dict) -> dict:
    """For a disagreement: decide2's reading next to the build's own record of P's truth (report only)."""
    info, err = _try(row)
    src = json.loads(SOURCES.read_text())["latents"] if SOURCES.exists() else {}
    s = src.get(row["meta"]["latent_id"], {})
    d = {"rid": row["rid"], "gold": row["gold"], "error": err, "meta_polarity": row["meta"].get("polarity"),
         "meta_tpl": row["meta"].get("tpl"), "build_truth": s.get("truth")}
    if info:
        t1 = (info["answer"] == "yes") != (info["flips"] % 2 == 1)
        d.update(decide2=info["answer"], frame=info["frame"], flips=info["flips"], truth_P=t1, kind=info["kind"])
        if info["flips"] != row["meta"].get("polarity"):
            d["why"] = "frame polarity: decide2 counts a different number of flips than the build"
        elif s.get("truth") is not None and s["truth"] != t1:
            d["why"] = "truth of P: decide2's source solver and the build's recorded truth differ"
        else:
            d["why"] = "same flips and same truth(P) but different gold: the build's gold formula"
    return d


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _rel(p) -> str:
    p = Path(p).resolve()
    return str(p.relative_to(LEAN)) if p.is_relative_to(LEAN) else str(p)


def build_report(parts=("train", "dev")) -> dict:
    rep = {"tool": "golden_src/gen3/v3_polarity_ladder.py", "key": KEY,
           "author": "builder C (independent of decide; never read gen3_polarity_ladder.py, pl_frames.py logic or "
                     "pl_sources.py; frame polarity from its own lexicon, truth(P) from golden_train (a) or the "
                     "source families' decide2 on the rebuilt question (b))",
           "inputs": {}, "parts": {}}
    for part in parts:
        p = _raw_path(part)
        rows, rels = load_rows(part), load_rels(part)
        rep["inputs"][part] = {"path": _rel(p), "rows": len(rows), "sha256": _sha(p),
                               "relations": {"path": _rel(_rel_path(part)), "sha256": _sha(_rel_path(part))}}
        ag = agreement(rows)
        by = {r["rid"]: r for r in rows}
        dis = [{**d, "diagnosis": diagnose(by[d["rid"]])} for d in ag["disagreements"]]
        rep["parts"][part] = {
            "rows": ag["rows"], "agree": ag["agree"], "disagree": ag["rows"] - ag["agree"], "rate": ag["rate"],
            "by_split_pack_view_polarity": ag["table"], "disagreements": dis,
            "by_kind": dict(sorted(Counter(i["kind"] for i in ag["infos"].values() if i).items())),
            "truth_route": dict(sorted(Counter(i["route"] for i in ag["infos"].values() if i).items())),
            "structure": structure_under_decide2(rows, rels, ag["answers"]),
            "meta_crosscheck": meta_crosscheck(rows, ag["infos"]),
            "source_crosscheck": source_crosscheck(rows, ag["infos"]),
            "cards": card_report(rows, ag["infos"]),
            "wording_sensitivity": sensitivity(rows, ag["answers"])}
    return rep


def write_agreement(out_path: Path | None = None, manifest: bool = True) -> dict:
    """Writes yn2b/v3_polarity_ladder_agreement.json (the SPEC 8.1 record for F4) and appends its sha256 to
    golden_src/gen3/MANIFEST_yn2b.jsonl. Reads the raw rows only; writes nothing under data/."""
    out_path = Path(out_path or REPORT_PATH)
    rep = build_report()
    text = json.dumps(rep, indent=1, ensure_ascii=False, default=str) + "\n"
    out_path.write_text(text)
    if manifest:
        if str(LEAN / "yn2b") not in sys.path:
            sys.path.insert(0, str(LEAN / "yn2b"))
        import yn2b_common as yc
        yc.manifest_append({"tool": "golden_src/gen3/v3_polarity_ladder.py", "key": KEY, "part": "decide2_agreement",
                            "path": _rel(out_path), "rows": sum(v["rows"] for v in rep["parts"].values()),
                            "sha256": hashlib.sha256(text.encode()).hexdigest(), "inputs": rep["inputs"],
                            "agree": {k: [v["agree"], v["rows"]] for k, v in rep["parts"].items()}})
    return rep


def _print(rep: dict) -> None:
    for part, v in rep["parts"].items():
        print(f"== {part}: {v['agree']}/{v['rows']} agree ({100 * v['rate']:.2f}%)")
        for d in v["disagreements"]:
            print("  DIS", json.dumps(d, default=str))
        if "structure" in v:
            st, mc, sc, cd = v["structure"], v["meta_crosscheck"], v["source_crosscheck"], v["cards"]
            print(f"  kinds {v['by_kind']}")
            print(f"  structure: complement {st['complement']} (not inverted {len(st['complement_not_inverted'])}), "
                  f"equiv {st['equiv']} (changed {len(st['equiv_changed'])}), unknown {len(st['unknown_rel'])}, "
                  f"state differs {len(st['same_state_broken'])}")
            print(f"  meta: polarity {len(mc['polarity'])}, role {len(mc['role'])}, view {len(mc['view'])}, renderer "
                  f"{len(mc['renderer'])}, P {len(mc['P_vs_sources'])}, derived_from {len(mc['derived_from'])}, "
                  f"held-out frame outside holdout {len(mc['held_out_frame_outside_holdout'])}, holdout with "
                  f"training frame {len(mc['holdout_with_training_frame'])}; flips {mc['flips']}")
            print(f"  frame families by split {mc['frame_family_by_split']}")
            print(f"  route 2 (source rows): {sc['route2_agree']}/{sc['b_rows']} agree, disagree "
                  f"{len(sc['route2_disagree'])}, undefined {len(sc['route2_undefined'])}, state not copied "
                  f"{len(sc['state_not_copied'])}, extra lines {len(sc['extra_lines_not_copied'])}, holds/fails "
                  f"{len(sc['holds_fails_not_source_yes_no'])}, source gold vs route 1 "
                  f"{len(sc['source_gold_vs_route1'])}, missing {len(sc['missing_source'])}")
            ws = v["wording_sensitivity"]
            print(f"  wording probes: {ws['ok']}/{ws['probes']} move the answer as expected; failed {len(ws['failed'])}")
            print(f"  cards: {cd['rows']} rows; P missing {len(cd['P_missing_from_yes_no'])}, no-line not negated "
                  f"{len(cd['no_line_not_negated'])}, (a) holds/fails without L {len(cd['a_holds_without_L'])}/"
                  f"{len(cd['a_fails_without_L'])}, needed but hidden {len(cd['cards_needed_but_hidden'])}")


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--quick", action="store_true", help="agreement only")
    ap.add_argument("--json", help="write the full report here (scratch path; never under data/)")
    ap.add_argument("--write", action="store_true",
                    help="write yn2b/v3_polarity_ladder_agreement.json and append its sha256 to MANIFEST_yn2b.jsonl")
    a = ap.parse_args(argv)
    if a.write:
        rep = write_agreement()
    elif a.quick:
        rep = {"parts": {}}
        for part in ("train", "dev"):
            ag = agreement(load_rows(part))
            rep["parts"][part] = {k: v for k, v in ag.items() if k not in ("answers", "infos")}
            rep["parts"][part]["disagree"] = ag["rows"] - ag["agree"]
    else:
        rep = build_report()
    _print(rep)
    if a.json:
        Path(a.json).write_text(json.dumps(rep, indent=1, ensure_ascii=False, default=str))
    return rep


if __name__ == "__main__":
    main()
