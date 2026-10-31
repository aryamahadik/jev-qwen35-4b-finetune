"""families/T15/plugin.py: T15 "eligibility gates and ordered claimant cascades" (C2_DATA_SPEC 2.1, 3.14;
PREREG_FINAL A37). Wave 2, everyday tier, 900 selected rows (about 1,350 generated).

Two tracks share one row shape: a short case note (Haiku skin), a program-rendered facts block, a rule card that states
every rule (closed world) and one question. Semantics: G0_SPEC.md (frozen sha below).
  gates      an applicant to an invented programme (household benefit or workplace scheme) meets 2-4 ordered gates.
             Each gate compares one printed fact with a limit through a lexicon comparator clause (at most / below
             for amounts; at least / more than for counts). An optional categorical route skips 1-3 named gates for an
             applicant enrolled in the route programme (skipped gates count as passed). Outcome: eligible, or "Not
             eligible: Gate X is the reason" for the FIRST applicable gate that fails.
  claimants  2-4 people ask to claim one child for an invented credit. Step one keeps the people who filed a claim;
             step two those with whom the child lived at least / more than N months; then three tie-breakers (parent;
             more months; higher income) in the order the card states, each keeping the people who come out best,
             until one is left. Nobody left after step two: nobody may claim the child.

  solver A   ordered decision lists (paradigm rule_engine): the gates are a rules.RuleSet under first_match whose
             rules are "fails Gate X" (route-guarded), default "eligible", run by rules.resolve; the claimant
             cascade is a sequence of rule steps (rules.evaluate filters, then tie-breakers that each keep the best)
  solver B   solver_b.py: its own parser of the RENDERED row; decision-table enumeration (paradigm decision_table):
             a truth table over every pass / fail combination of the gates, with integer-difference sign tests,
             and a pairwise duel table over the claimants still in the running
  samplers   S1 forward; S2 label-first (boundary and trap probabilities +0.20); S3 table-first (facts before the
             note, table or JSON); S4 interview transcript; S5 held out (held-out programmes, CSV facts, held-out
             skins and wordings)
  questions  gates: ch_outcome (closed set); yes/no on predicate "eligible": yn_eligible, yn_dneg_eligible (double
             negation), complements yn_ineligible (antonym), yn_gate_stops (option framing), yn_fails (implicit),
             yn_not_eligible (syntactic). claimants: ch_claimant (open set from error models + "nobody"); yes/no on
             predicate "claims": yn_may_claim, yn_dneg_claim, complements yn_barred (antonym), yn_elsewhere
             (option framing), yn_fails_claim (implicit), yn_may_not (syntactic)
  relations  complement; minimal-edit twin (one gated fact, limit, comparator or enrolment; one claimant's months,
             filing, income or relationship); equiv (another skin and container); inv (an inert note); G4 metamorphic
The construction side (GateFacts / ClaimFacts, _first_failure, _cascade) drives sampling, twin predictions, error
models and trap tags; solver A never calls it. Code only: nothing here writes a file (A37 f).

v1.3 (pilot fix iteration 1; G0_SPEC.md section 7): the ch_claimant display plan (k, the "Nobody may claim the child"
option, its gold share) is drawn from the row key before the structure (claim_plan, c2_kit.choiceplan); every
ch_outcome option is gold on 1 / (gates + 1) of the rows, twins included (OUTCOME_ELIGIBLE, OUTCOME_W); yes/no rows
carry the card in row.card (c2_kit.cards.place_rules); two fixed card sentences and the interview questions are
shorter; the plugin opts in to c2_kit.polarity.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path

from c2_kit import cards as CARDS
from c2_kit import rules as RL
from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.choiceplan import ChoicePlan, plan_choice
from c2_kit.distractors import build_closed, build_options, error_model, register_name, uhash
from c2_kit.plugin import C2Plugin, ContractError, QuestionForm, RelationProposal, Spec, choose_forms
from c2_kit.rows import TextBuilder, assemble_row

HERE = Path(__file__).resolve().parent
FAMILY = "T15"

# ------------------------------------------------------------------------------------------------ fixed text
LETTERS = "ABCD"
CLOSED_WORLD = "These rules and facts are complete, and only they decide the outcome."
NOTE_PREFIX = "Note added to the case: "
ELIGIBLE = "eligible"
NONE_KEY = "none"
NONE_TEXT = "Nobody may claim the child"
ELIGIBLE_TEXT = "Eligible"
PARENTS = ("mother", "father")
NONPARENTS = ("grandmother", "grandfather", "aunt", "uncle")
REL_SET = {r: [r] for r in PARENTS + NONPARENTS}
FILED_SET = {"yes": ["yes"], "no": ["no"]}
TIEBREAKS = ("parent", "months", "income")
DEFAULT_ORDER = ("parent", "months", "income")
TB_TEXT = {"parent": "a parent comes first, before a grandparent, aunt or uncle",
           "months": "the person with whom {SUBJECT} lived for more months comes first",
           "income": "the person with the higher annual income comes first"}
ORDINALS = ("First", "Second", "Third")
OP = {"cmp.le": "<=", "cmp.lt": "<", "cmp.ge": ">=", "cmp.gt": ">"}
INCLUSIVE = {"cmp.le": "cmp.lt", "cmp.ge": "cmp.gt"}          # inclusive sem -> its exclusive partner
EXCLUSIVE = {v: k for k, v in INCLUSIVE.items()}
FLIP_DIRECTION = {"cmp.le": "cmp.ge", "cmp.lt": "cmp.gt", "cmp.ge": "cmp.le", "cmp.gt": "cmp.lt"}
UNIT_MONTH = ("month", "months")


@dataclass(frozen=True)
class Field:
    """One applicant fact a gate can test (G0_SPEC.md S2-S3)."""
    fid: str
    slot: str               # the fact's slot name
    label: str              # facts-block label and option reason
    kind: str               # cents | count
    unit: tuple | None      # count unit (singular, plural)
    sense: str              # max: the fact must stay under the limit (le / lt); min: reach it (ge / gt)
    phrase: str             # the card's gate phrase; the comparator clause follows it
    question: str           # S4 interview question
    lim: tuple              # (lo, hi, step) for the limit
    decoy: tuple            # (lo, hi) for an ungated value
    domain: str

    @property
    def lex_slot(self) -> str:
        return "X" if self.kind == "cents" else "N"


FIELDS = {f.fid: f for f in (
    Field("gross", "F_GROSS", "gross monthly income", "cents", None, "max", "gross monthly income is ",
          "Gross monthly income?", (180000, 420000, 500), (90000, 520000), "household"),
    Field("net", "F_NET", "net monthly income", "cents", None, "max", "net monthly income is ",
          "Net monthly income?", (140000, 340000, 500), (60000, 420000), "household"),
    Field("assets", "F_ASSETS", "countable assets", "cents", None, "max", "countable assets are ",
          "Countable assets?", (200000, 1200000, 5000), (0, 1800000), "household"),
    Field("residence", "F_RES", "time in the service area", "count", UNIT_MONTH, "min",
          "the applicant has lived in the service area for ", "Time in the service area?",
          (3, 12, 1), (0, 60), "household"),
    Field("age", "F_AGE", "age", "count", ("year", "years"), "min", "the applicant's age is ", "Age?",
          (55, 67, 1), (18, 90), "household"),
    Field("tenure", "F_TENURE", "time employed", "count", UNIT_MONTH, "min", "the applicant has been employed for ",
          "Time employed?", (6, 24, 1), (0, 120), "work"),
    Field("hours", "F_HOURS", "hours worked in the past year", "count", ("hour", "hours"), "min",
          "hours worked in the past year are ", "Hours worked in the past year?", (700, 1500, 10),
          (0, 2400), "work"),
    Field("head", "F_HEAD", "employees at the worksite", "count", ("employee", "employees"), "min",
          "the worksite has ", "Employees at your worksite?", (15, 75, 1), (1, 400), "work"),
    Field("gpay", "F_GPAY", "gross annual pay", "cents", None, "max", "gross annual pay is ",
          "Gross annual pay?", (3000000, 9000000, 50000), (1500000, 12000000), "work"),
    Field("npay", "F_NPAY", "take-home annual pay", "cents", None, "max", "take-home annual pay is ",
          "Take-home annual pay?", (2200000, 7000000, 50000), (1000000, 9000000), "work"),
)}
DOMAIN_FIELDS = {"household": ("gross", "net", "assets", "residence", "age"),
                 "work": ("tenure", "hours", "head", "gpay", "npay")}
INCOME_PAIR = {"household": ("gross", "net"), "work": ("gpay", "npay")}
# Enrolment values (category keys = surfaces). Each route programme has at most one near-miss decoy.
ENROLL_SETS = {
    "household": ("Kestrel Housing Aid", "Kestrel Housing Loan", "Orchard Food Basket", "Orchard Food Box",
                  "Lakeside Disability Support", "none"),
    "work": ("Veteran Return Scheme", "Veteran Return Pilot", "Apprentice Pathway Program",
             "Apprentice Pathway Pilot", "Guild Caregiver Plan", "none"),
}
ROUTES = {"household": (("Kestrel Housing Aid", "Kestrel Housing Loan"), ("Orchard Food Basket", "Orchard Food Box"),
                        ("Lakeside Disability Support", None)),
          "work": (("Veteran Return Scheme", "Veteran Return Pilot"),
                   ("Apprentice Pathway Program", "Apprentice Pathway Pilot"), ("Guild Caregiver Plan", None))}

# ------------------------------------------------------------------------------------------------ packs and pools
# Program-side seed pools (G0_SPEC.md 3). After A38 they grow from Haiku pack pools (spec 3.0 packs).
GATE_PROGS = (("Harbor County Energy Credit", "household"), ("Lumen Valley Childcare Grant", "household"),
              ("Cedarline Transit Pass Discount", "household"), ("Northpeak Protected Family Leave", "work"),
              ("Granite Works Tuition Support", "work"), ("Bluepeak Caregiver Leave", "work"))
GATE_PROGS_HELD = (("Riverbend Heating Assistance", "household"), ("Cobalt Labs Parental Leave", "work"))
CREDITS = ("Lakeshore Family Credit", "Alder Grove Child Allowance", "Pinecrest Dependent Credit",
           "Marlow Bay Family Supplement")
CREDITS_HELD = ("Silverline Child Credit", "Brookfield Family Payment")
FEMALE_NAMES = ("Lena", "Mira", "Aiko", "Priya", "Grace", "Ines", "Keiko", "Maya", "Nadia", "Paula", "Rosa", "Tara",
                "Zara", "Amara", "Chloe", "Farah", "Hana", "Lucia", "Petra", "Selin")
MALE_NAMES = ("Ravi", "Tomas", "Omar", "Hugo", "Leon", "Oscar", "Sanjay", "Victor", "Yusuf", "Bruno", "Diego",
              "Gideon", "Ivan", "Kofi", "Anton", "Marco", "Tariq", "Pavel", "Jonas", "Kenji")
FIRST_NAMES = FEMALE_NAMES + MALE_NAMES + ("Dana", "Wren")      # applicants and renames (no relationship to agree)
FEMALE_RELS = ("mother", "grandmother", "aunt")
LAST_NAMES = ("Okafor", "Whitcombe", "Anand", "Castell", "Ferreira", "Brandt", "Shah", "Lindqvist", "Moreau",
              "Novak", "Haddad", "Kowalski", "Mensah", "Tanaka", "Rossi", "Byrne", "Duarte", "Iqbal", "Jansen",
              "Laine", "Murphy", "Osei", "Petrov", "Reyes", "Sato", "Vance", "Walsh", "Yilmaz", "Zhou", "Abbott")
CHILDREN = ("Mia", "Leo", "Ava", "Noah", "Zoe", "Eli", "Iris", "Owen", "Ruby", "Theo", "Nina", "Jonah", "Elsie",
            "Milo", "Luna", "Arlo")
WORKERS = ("Morgan Ellis", "Jordan Pike", "Casey Lund", "Riley Shaw", "Avery Stone", "Harper Quill", "Rowan Frost",
           "Skyler Mercer", "Emerson Hale", "Logan Brooks")
YEARS = (2025, 2026, 2027)
REAL_LIMITS = {("hours", 1250), ("head", 50)}   # real-world thresholds (US FMLA) are never drawn as limits
CASE_PATTERNS = {"household": "CASE-#####", "work": "HR-#####", "claimants": "CR-#####"}
TRAIN_SAMPLERS = ("S1", "S2", "S3", "S4")
PACK_KINDS = ("household", "work", "credit")
NAME_POOLS = ("female", "male", "neutral", "last", "children", "workers")


def make_pack(pid: str, kind: str, programme: str, routes=(), others=(), held_out: bool = False) -> dict:
    """A programme pack in plugin form (G0_SPEC.md S1, S5, section 3 item 5). Gate packs (household / work) carry
    their route programmes ((route, near-miss decoy or None), ...) and other programmes; enrol = every enrolment value
    a row of the pack may print (routes, decoys, others, then "none")."""
    if kind not in PACK_KINDS:
        raise ContractError(f"pack {pid}: kind {kind!r}")
    routes = tuple((r, n) for r, n in routes)
    enrol = tuple(x for r, n in routes for x in (r, n) if x) + tuple(others) + ("none",)
    if kind != "credit" and not routes:
        raise ContractError(f"pack {pid}: a gate pack lists its route programmes")
    if len(set(enrol)) != len(enrol):
        raise ContractError(f"pack {pid}: enrolment values repeat")
    return {"id": pid, "kind": kind, "programme": programme, "routes": routes, "others": tuple(others),
            "enrol": enrol if kind != "credit" else (), "held_out": bool(held_out)}


# Built-in packs: the Claude-written seed pools above, one pack per programme. With these the card -> pack map below
# reproduces v1 exactly (cards 0-2 household, 3-5 work, 6-9 credits). The Haiku pack pool replaces them through
# T15Plugin(packs=...), one pack per training card (12 household, 12 work, 16 credits) when the pool is large enough.
BUILTIN_PACKS = tuple(
    [make_pack(f"t15b.{d}.{i}", d, n, ROUTES[d], tuple(e for e in ENROLL_SETS[d] if e != "none" and e not in
                                                     {x for rn in ROUTES[d] for x in rn}))
     for i, (n, d) in enumerate(GATE_PROGS)]
    + [make_pack(f"t15b.held.{d}.{i}", d, n, ROUTES[d], (), held_out=True) for i, (n, d) in enumerate(GATE_PROGS_HELD)]
    + [make_pack(f"t15b.credit.{i}", "credit", n) for i, n in enumerate(CREDITS)]
    + [make_pack(f"t15b.held.credit.{i}", "credit", n, held_out=True) for i, n in enumerate(CREDITS_HELD)])

# ------------------------------------------------------------------------------------------------ sampling knobs
N_CARDS, N_CARDS_HELD = 10, 4           # cards per training sampler / for S5 (one programme pack each)
N_GATE_CARDS, N_GATE_CARDS_HELD = 6, 2  # cards 0..5 (S5: 0..1) are gate programmes, the rest credits
QFORM_SHARES = {
    "gates": (("ch_outcome", 0.58), ("yn_eligible", 0.17), ("yn_dneg_eligible", 0.04), ("yn_ineligible", 0.06),
              ("yn_gate_stops", 0.05), ("yn_fails", 0.05), ("yn_not_eligible", 0.05)),
    "claimants": (("ch_claimant", 0.58), ("yn_may_claim", 0.17), ("yn_dneg_claim", 0.04), ("yn_barred", 0.05),
                  ("yn_elsewhere", 0.05), ("yn_fails_claim", 0.05), ("yn_may_not", 0.06)),
}
# deep (G0 v1.4 S23, A43 b) is a property of the card the seed draws BEFORE the target: a 4-gate card / a 4-person cascade.
# It is stored in structure["deep"] and never recomputed from the answer, so depth carries no gold signal; every label
# is drawn as in the other depth classes (OUTCOME_*, claim_plan). The deep share is at most 10% of the specs.
GATE_COUNTS = ((2, 0.37), (3, 0.55), (4, 0.08))
PEOPLE_COUNTS = ((2, 0.30), (3, 0.62), (4, 0.08))
DEEP_COUNT = 4
#   ch_outcome: every option is gold on 1 / (gate count + 1) of the ROWS, twins included (G0 v1.3 S20, pilot FIX-2);
#   OUTCOME_ELIGIBLE / OUTCOME_W below set the base-row target that makes it so
#   ch_claimant: the display plan (k, shown, gold nobody) is drawn from the row key BEFORE the structure (G0 v1.3 S20,
#   pilot FIX-1; c2_kit.choiceplan): nobody is shown only on k = 3 rows, SHOW_ABSTAIN of them, and is gold on
#   NOBODY_SHARE of the shown base rows
P_NOBODY_NO = 0.20       # claimant yes/no rows whose answer is "the asked person does not claim": nobody claims
P_INCOME_GATE = 0.85     # a gate list holds at least one income gate
P_ROUTE, P_HOLDER = 0.50, 0.50
P_ROUTE_DECIDES = 0.50   # route listed, applicant not enrolled: the deciding gate is a skippable one
# ch_outcome base target by gate count (G0 v1.3 S20): P(eligible) and the weights of the decisive gate A, B, ... among
# the gates that apply. Calibrated so that every option is gold on 1/k of the rows once twins and copies are added.
OUTCOME_ELIGIBLE = {2: 0.270, 3: 0.205, 4: 0.166}
OUTCOME_W = {2: (0.476, 0.524), 3: (0.299, 0.329, 0.372), 4: (0.209, 0.235, 0.264, 0.292)}
P_NEAR = 0.45            # route listed, applicant not enrolled: enrolled in the route's near-miss programme
P_SKIP_FAIL = 0.60       # enrolled applicant: a skipped gate fails
P_MULTI = 0.30           # a gate after the deciding one also fails
P_EDGE = 0.35            # a gated value sits on a boundary (the limit or one unit / cent from it)
P_NET_TRAP = 0.60        # only gross gated and failing: net would pass the gross limit
P_PARENT = 0.50
P_FILED = 0.80
P_EDGE_MONTHS = 0.30
P_ORDER_TRAP = 0.45
P_FILED_TRAP = 0.25
P_INCOME_TIE = 0.25
P_THIRD = 0.12           # the third tie-breaker decides (two people tie on the first two)
P_ASK_TRAP = 0.75        # yes/no "no" rows: the asked person is a named error model's winner
S2_BOOST = 0.20
COMP_RATE, TWIN_RATE, EQUIV_RATE, INV_RATE = 0.45, 0.44, 0.10, 0.03
CLAIM_K = (2, 3)         # ch_claimant option counts, a label-blind draw (G0 S20)
ABSTAIN_MIN_K = 3        # "Nobody may claim the child" is shown only on k >= 3 rows (a k = 2 cell would sit on the
                         # spec 3.0 bar: gold on 1/2 of the rows that show it against a bar of wrong on >= 1/2)
SHOW_ABSTAIN = 0.85      # k = 3 rows: the label-blind probability that the option is shown (row key only)
NOBODY_SHARE = 0.46      # P(gold = nobody | shown) on a base row. Twin rows are never nobody (they dilute the shown
                         # cell), so the realised share over all rows is about 1/3 (G0 v1.3 section 7)
PARTNERS = {
    "yn_eligible": (("yn_ineligible", 0.30), ("yn_gate_stops", 0.25), ("yn_fails", 0.20), ("yn_not_eligible", 0.25)),
    "yn_dneg_eligible": (("yn_not_eligible", 1.0),),
    "yn_ineligible": (("yn_eligible", 1.0),), "yn_gate_stops": (("yn_eligible", 1.0),),
    "yn_fails": (("yn_eligible", 1.0),), "yn_not_eligible": (("yn_eligible", 0.6), ("yn_dneg_eligible", 0.4)),
    "yn_may_claim": (("yn_barred", 0.30), ("yn_elsewhere", 0.25), ("yn_fails_claim", 0.20), ("yn_may_not", 0.25)),
    "yn_dneg_claim": (("yn_may_not", 1.0),),
    "yn_barred": (("yn_may_claim", 1.0),), "yn_elsewhere": (("yn_may_claim", 1.0),),
    "yn_fails_claim": (("yn_may_claim", 1.0),), "yn_may_not": (("yn_may_claim", 0.6), ("yn_dneg_claim", 0.4)),
}
TRACK_OF = {q: t for t, tab in QFORM_SHARES.items() for q, _ in tab}

# Error models (every wrong option names one; G0_SPEC.md S22).
# T15-only names carry the t15_ prefix (the distractor catalog is shared by every family).
GATE_MODELS = ("stop_at_first_gate", "net_vs_gross", "drop_inclusive_endpoint", "add_exclusive_endpoint",
               "t15_ignore_route", "t15_route_skips_all", "t15_route_not_enrolled", "t15_last_failure",
               "t15_flip_direction", "t15_flip_gate_a", "t15_flip_gate_b", "t15_flip_gate_c", "t15_flip_gate_d",
               "t15_any_pass")
CLAIM_MODELS = ("wrong_tiebreak", "drop_inclusive_endpoint", "add_exclusive_endpoint", "t15_default_order",
                "t15_swap_first_two", "t15_skip_filed_check", "t15_skip_months_check", "t15_income_only",
                "t15_most_months", "t15_first_listed", "t15_income_all", "t15_first_filed")
for _name, _text in (
        ("t15_ignore_route", "ignores the categorical route and tests every gate"),
        ("t15_route_skips_all", "treats the categorical route as skipping every gate"),
        ("t15_route_not_enrolled", "applies the categorical route to an applicant who is not enrolled in the route "
                                   "programme"),
        ("t15_last_failure", "reports the last failing gate instead of the first in the listed order"),
        ("t15_flip_direction", "reads every upper limit as a lower limit and every lower limit as an upper limit"),
        ("t15_flip_gate_a", "reads the limit of Gate A in the wrong direction (at most as at least, or the reverse)"),
        ("t15_flip_gate_b", "reads the limit of Gate B in the wrong direction (at most as at least, or the reverse)"),
        ("t15_flip_gate_c", "reads the limit of Gate C in the wrong direction (at most as at least, or the reverse)"),
        ("t15_flip_gate_d", "reads the limit of Gate D in the wrong direction (at most as at least, or the reverse)"),
        ("t15_any_pass", "treats the applicant as eligible when any gate that applies passes"),
        ("t15_default_order", "applies the tie-breakers in the order parent, months, income instead of the stated "
                              "order"),
        ("t15_swap_first_two", "swaps the first two tie-breakers"),
        ("t15_skip_filed_check", "ignores the step that keeps only the people who filed a claim"),
        ("t15_skip_months_check", "ignores the step that keeps only the people who lived with the child long "
                                  "enough"),
        ("t15_income_only", "picks the highest income among the people in the running, ignoring the tie-breaker "
                            "order"),
        ("t15_most_months", "picks the person with whom the child lived longest, ignoring every other step"),
        ("t15_first_listed", "picks the first listed person still in the running"),
        ("t15_income_all", "picks the highest income among all the listed people, skipping steps one and two"),
        ("t15_first_filed", "picks the first listed person who filed a claim, skipping step two and the "
                            "tie-breakers")):
    register_name(_name, _text)


class Tie(ValueError):
    """Two claimants tie on every tie-breaker (never generated; such draws are rejected)."""


class NoPlan(ValueError):
    """A gate plan whose income facts cannot be made consistent (the sampler redraws the plan)."""


# ------------------------------------------------------------------------------------------------ program templates
def _gate_list(positions) -> str:
    names = [f"Gate {LETTERS[i]}" for i in positions]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


@lru_cache(maxsize=None)
def gate_card_template(gates: tuple, route: tuple | None) -> str:
    """The gate card (program text, G0_SPEC.md S15). Slots: PROG, YEAR, G<i>_CMP (clause on G<i>_LIM), ROUTE."""
    lines = ["{PROG} eligibility rules for {YEAR:plain}:",
             "- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason "
             "the applicant is not eligible."]
    for i, fid in enumerate(gates):
        lines.append(f"- Gate {LETTERS[i]}: passed when {FIELDS[fid].phrase}{{G{i + 1}_CMP}}.")
    if route:
        lines.append("- Route: an applicant enrolled in {ROUTE} skips " + _gate_list(route) + "; for that applicant, "
                     "skipped gates count as passed, and every other gate still applies.")
    lines.append("- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.")
    lines.append("- " + CLOSED_WORLD)
    return "\n".join(lines)


@lru_cache(maxsize=None)
def claim_card_template(order: tuple) -> str:
    """The claimant card (program text, G0_SPEC.md S16). Slots: PROG, YEAR, SUBJECT, MIN_CMP (clause on MIN_M)."""
    lines = ["{PROG} rules for {YEAR:plain}: who may claim {SUBJECT}.",
             "- Only one person may claim {SUBJECT}. Work through these steps in order.",
             "- Step one: only people who filed a claim for {SUBJECT} are considered.",
             "- Step two: of those, only people with whom {SUBJECT} lived for {MIN_CMP} in {YEAR:plain} stay in the "
             "running.",
             "- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who "
             "are best on it. The tie-breakers stop once one person is left."]
    for ordinal, tb in zip(ORDINALS, order):
        lines.append(f"- {ordinal} tie-breaker: {TB_TEXT[tb]}.")
    lines += ["- If nobody is left after step two, nobody may claim {SUBJECT}.",
              "- A parent means the child's mother or father. Different people's months can overlap.",
              "- " + CLOSED_WORLD]
    return "\n".join(lines)


def _json_key(label: str) -> str:
    return label.replace(" ", "_")


@lru_cache(maxsize=None)
def gate_facts_template(domain: str, style: str) -> tuple:
    """(header, body, escape) of the applicant facts block in one container (G0_SPEC.md S17)."""
    fs = [FIELDS[f] for f in DOMAIN_FIELDS[domain]]
    if style == "lines":
        body = "\n".join(f"- {f.label}: {{{f.slot}}}" for f in fs) + "\n- enrolled in: {ENROLL}"
        return "Facts for {SUBJECT} ({YEAR:plain}):", body, "text"
    if style == "table":
        rows = ["| fact | value |", "| --- | --- |"] + [f"| {f.label} | {{{f.slot}}} |" for f in fs]
        return "Facts for {SUBJECT} ({YEAR:plain}):", "\n".join(rows + ["| enrolled in | {ENROLL} |"]), "text"
    if style == "json":
        pairs = [f'"{_json_key(f.label)}": {{{f.slot}}}' for f in fs] + ['"enrolled_in": {ENROLL}']
        return "Facts for {SUBJECT} ({YEAR:plain}), as JSON:", "{" + ", ".join(pairs) + "}", "json"
    if style == "csv":
        rows = ["fact,value"] + [f"{f.label},{{{f.slot}:{'nocomma' if f.kind == 'cents' else 'plain'}}}" for f in fs]
        return ("Facts for {SUBJECT} ({YEAR:plain}), as CSV with amounts in USD:",
                "\n".join(rows + ["enrolled in,{ENROLL}"]), "text")
    if style == "transcript":
        rows = []
        for f in fs:
            rows += [f"Caseworker: {f.question}", f"{{SUBJECT}}: {{{f.slot}}}."]
        rows += ["Caseworker: Other programme enrolled in?", "{SUBJECT}: {ENROLL}."]
        return "Intake interview with {SUBJECT} ({YEAR:plain}):", "\n".join(rows), "text"
    raise ContractError(f"facts style {style!r}")


@lru_cache(maxsize=None)
def claim_facts_template(people: int, style: str) -> tuple:
    """(header, body, escape) of the claimant block in one container (G0_SPEC.md S17)."""
    idx = range(1, people + 1)
    if style == "lines":
        body = "\n".join(f"- {{C{i}_NAME}}: relationship to {{SUBJECT}}: {{C{i}_REL}}; months lived with {{SUBJECT}}: "
                         f"{{C{i}_MONTHS}}; annual income: {{C{i}_INC}}; filed a claim: {{C{i}_FILED}}" for i in idx)
        return "People who asked to claim {SUBJECT} ({YEAR:plain}):", body, "text"
    if style == "table":
        rows = ["| person | relationship to {SUBJECT} | months lived with {SUBJECT} | annual income | filed a claim |",
                "| --- | --- | --- | --- | --- |"]
        rows += [f"| {{C{i}_NAME}} | {{C{i}_REL}} | {{C{i}_MONTHS}} | {{C{i}_INC}} | {{C{i}_FILED}} |" for i in idx]
        return "People who asked to claim {SUBJECT} ({YEAR:plain}):", "\n".join(rows), "text"
    if style == "json":
        objs = ", ".join(f'{{"name": {{C{i}_NAME}}, "relationship": {{C{i}_REL}}, "months_lived_with_child": '
                         f'{{C{i}_MONTHS}}, "annual_income": {{C{i}_INC}}, "filed_a_claim": {{C{i}_FILED}}}}'
                         for i in idx)
        return "People who asked to claim {SUBJECT} ({YEAR:plain}), as JSON:", '{"people": [' + objs + "]}", "json"
    if style == "csv":
        rows = ["name,relationship,months lived with child,annual income,filed a claim"]
        rows += [f"{{C{i}_NAME}},{{C{i}_REL}},{{C{i}_MONTHS:plain}},{{C{i}_INC:nocomma}},{{C{i}_FILED}}" for i in idx]
        return ("People who asked to claim {SUBJECT} ({YEAR:plain}), as CSV with amounts in USD:", "\n".join(rows),
                "text")
    if style == "transcript":
        rows = []
        for i in idx:
            n = f"{{C{i}_NAME}}"
            rows += [f"Caseworker: {n}, your relation to {{SUBJECT}}?",
                     f"{n}: I am {{poss|SUBJECT}} {{C{i}_REL}}.",
                     "Caseworker: Months {SUBJECT} lived with you?", f"{n}: {{C{i}_MONTHS}}.",
                     "Caseworker: Annual income?", f"{n}: {{C{i}_INC}}.",
                     "Caseworker: Filed a claim for {SUBJECT}?", f"{n}: {{C{i}_FILED}}."]
        return "Interview notes for {SUBJECT} ({YEAR:plain}):", "\n".join(rows), "text"
    raise ContractError(f"facts style {style!r}")


STYLE_BY_REGISTER = {"json": "json", "ticket": "table", "form": "table", "log": "table"}


def facts_style(sampler: str, register: str) -> str:
    """Label-blind container choice (G0_SPEC.md S17): S5 CSV; S4 interview; a JSON skin gets JSON; S3 a table."""
    if sampler == "S5":
        return "csv"
    if sampler == "S4":
        return "transcript"
    if register == "json":
        return "json"
    if sampler == "S3":
        return "table"
    return STYLE_BY_REGISTER.get(register, "lines")


def outcome_text(key: str, gates: tuple) -> str:
    if key == ELIGIBLE:
        return ELIGIBLE_TEXT
    i = LETTERS.index(key[-1])
    return f"Not eligible: Gate {key[-1]} is the reason ({FIELDS[gates[i]].label})"


# ------------------------------------------------------------------------------------------------ construction side
@dataclass(frozen=True)
class Gate:
    letter: str
    fid: str
    sem: str
    limit: int
    value: int


@dataclass(frozen=True)
class GateFacts:
    domain: str
    gates: tuple            # Gate, in card order
    skips: frozenset | None  # letters the route skips (None: no route listed)
    route: str | None
    enroll: str
    facts: dict             # fid -> value (every domain field)

    @property
    def holder(self) -> bool:
        return self.route is not None and self.enroll == self.route

    @property
    def skipped(self) -> frozenset:
        return self.skips if self.holder else frozenset()


@dataclass(frozen=True)
class Person:
    name: str
    rel: str
    months: int
    income: int
    filed: str


@dataclass(frozen=True)
class ClaimFacts:
    people: tuple
    min_sem: str
    min_m: int
    order: tuple
    asked: str | None


def _passes(sem: str, v: int, limit: int) -> bool:
    if sem == "cmp.le":
        return v <= limit
    if sem == "cmp.lt":
        return v < limit
    if sem == "cmp.ge":
        return v >= limit
    if sem == "cmp.gt":
        return v > limit
    raise ContractError(f"sem {sem}")


def gate_facts(spec: Spec) -> GateFacts:
    v = spec.env()
    st = spec.structure
    gates = tuple(Gate(LETTERS[i], fid, v[f"G{i + 1}_CMP"], v[f"G{i + 1}_LIM"], v[FIELDS[fid].slot])
                  for i, fid in enumerate(st["gates"]))
    skips = frozenset(LETTERS[i] for i in st["route"]) if st["route"] else None
    return GateFacts(st["domain"], gates, skips, v.get("ROUTE") if st["route"] else None, v["ENROLL"],
                     {f: v[FIELDS[f].slot] for f in DOMAIN_FIELDS[st["domain"]]})


def claim_facts(spec: Spec) -> ClaimFacts:
    v = spec.env()
    st = spec.structure
    people = tuple(Person(v[f"C{i}_NAME"], v[f"C{i}_REL"], v[f"C{i}_MONTHS"], v[f"C{i}_INC"], v[f"C{i}_FILED"])
                   for i in range(1, st["people"] + 1))
    return ClaimFacts(people, v["MIN_CMP"], v["MIN_M"], tuple(st["order"]), v.get("ASKED"))


def _first_failure(gates, skipped, sems=None, values=None) -> str:
    """Construction-side outcome: the first listed applicable gate that fails, else eligible."""
    for g in gates:
        if g.letter in skipped:
            continue
        sem = (sems or {}).get(g.letter, g.sem)
        val = (values or {}).get(g.letter, g.value)
        if not _passes(sem, val, g.limit):
            return "fail_" + g.letter
    return ELIGIBLE


def _gate_outcome(f: GateFacts) -> str:
    return _first_failure(f.gates, f.skipped)


def _score(p: Person, tb: str) -> int:
    return {"parent": int(p.rel in PARENTS), "months": p.months, "income": p.income}[tb]


def _cascade(people, min_sem: str, min_m: int, order, *, filed: bool = True, months: bool = True):
    """Construction-side cascade: the strictly best person by the key tuple in `order`, among those who pass the
    steps; None when nobody passes. A full tie raises Tie."""
    pool = [p for p in people if (not filed or p.filed == "yes") and (not months or _passes(min_sem, p.months, min_m))]
    if not pool:
        return None
    keyed = sorted(((tuple(_score(p, t) for t in order), p.name) for p in pool), reverse=True)
    if len(keyed) > 1 and keyed[0][0] == keyed[1][0]:
        raise Tie(keyed[0][1])
    return keyed[0][1]


def _steps(c: ClaimFacts) -> int:
    """How many tie-breakers the cascade uses before one person (or nobody) is left."""
    left = [p for p in c.people if p.filed == "yes" and _passes(c.min_sem, p.months, c.min_m)]
    steps = 0
    for tb in c.order:
        if len(left) < 2:
            break
        steps += 1
        top = max(_score(p, tb) for p in left)
        left = [p for p in left if _score(p, tb) == top]
    return steps


def _claim_winner(c: ClaimFacts):
    return _cascade(c.people, c.min_sem, c.min_m, c.order)


def _answer(qform: str, outcome):
    """The answer a construction outcome implies (twin predictions, tags). outcome: a gate outcome key, or the
    claimant winner's name / None (with the asked name for yes/no)."""
    if qform == "ch_outcome":
        return outcome
    if qform == "ch_claimant":
        return NONE_KEY if outcome is None else outcome
    q = T15Plugin.QFORMS[qform]
    if q.predicate == ELIGIBLE:
        holds = outcome == ELIGIBLE
    else:
        winner, asked = outcome
        holds = winner is not None and winner == asked
    return int(holds if q.polarity == 1 else not holds)


def _gate_answer(qform: str, f: GateFacts):
    return _answer(qform, _gate_outcome(f))


def _claim_answer(qform: str, c: ClaimFacts):
    w = _claim_winner(c)
    return _answer(qform, w if qform == "ch_claimant" else (w, c.asked))


# Named wrong cascades (error models, trap tags and the "asked" choice share them).
def _claim_variants(c: ClaimFacts) -> dict:
    o = c.order

    def run(**kw):
        try:
            w = _cascade(c.people, kw.get("sem", c.min_sem), c.min_m, kw.get("order", o),
                         filed=kw.get("filed", True), months=kw.get("months", True))
        except Tie:
            return None
        return NONE_KEY if w is None else w

    def best_of(people, tb):
        if not people:
            return None
        top = max(_score(p, tb) for p in people)
        hits = [p.name for p in people if _score(p, tb) == top]
        return hits[0] if len(hits) == 1 else None

    pool = [p for p in c.people if p.filed == "yes" and _passes(c.min_sem, p.months, c.min_m)]
    return {"wrong_tiebreak": run(order=tuple(reversed(o))),
            "t15_default_order": run(order=DEFAULT_ORDER) if o != DEFAULT_ORDER else None,
            "t15_swap_first_two": run(order=(o[1], o[0], o[2])),
            "t15_skip_filed_check": run(filed=False),
            "t15_skip_months_check": run(months=False),
            "drop_inclusive_endpoint": run(sem=INCLUSIVE[c.min_sem]) if c.min_sem in INCLUSIVE else None,
            "add_exclusive_endpoint": run(sem=EXCLUSIVE[c.min_sem]) if c.min_sem in EXCLUSIVE else None,
            "t15_income_only": best_of(pool, "income"),
            "t15_most_months": best_of(list(c.people), "months"),
            "t15_first_listed": pool[0].name if pool else None}


def _claim_extra(c: ClaimFacts) -> dict:
    """Two more claimant misreadings that skip both steps (options only: the samplers read _claim_variants). They give
    the "nobody" rows as many named wrong claimants as the others, so the option count k and the abstain display can
    be drawn once from the row key (a k lowered on failure carried the label: G0 S20)."""
    top = max((p.income for p in c.people), default=None)
    rich = [p.name for p in c.people if p.income == top]
    return {"t15_income_all": rich[0] if len(rich) == 1 else None,
            "t15_first_filed": next((p.name for p in c.people if p.filed == "yes"), None)}


def _gate_variants(f: GateFacts) -> dict:
    g0 = f.gates[0]
    income = INCOME_PAIR[f.domain]
    swap = {}
    for g in f.gates:
        if g.fid in income:
            other = income[1] if g.fid == income[0] else income[0]
            swap[g.letter] = f.facts[other]
    incl = {g.letter: INCLUSIVE[g.sem] for g in f.gates if g.sem in INCLUSIVE}
    excl = {g.letter: EXCLUSIVE[g.sem] for g in f.gates if g.sem in EXCLUSIVE}
    failing = [g.letter for g in f.gates if g.letter not in f.skipped and not _passes(g.sem, g.value, g.limit)]
    out = {
        "stop_at_first_gate": ELIGIBLE if _passes(g0.sem, g0.value, g0.limit) else "fail_" + g0.letter,
        "net_vs_gross": _first_failure(f.gates, f.skipped, values=swap) if swap else None,
        "drop_inclusive_endpoint": _first_failure(f.gates, f.skipped, sems=incl) if incl else None,
        "add_exclusive_endpoint": _first_failure(f.gates, f.skipped, sems=excl) if excl else None,
        "t15_ignore_route": _first_failure(f.gates, frozenset()) if f.holder else None,
        "t15_route_skips_all": ELIGIBLE if f.holder else None,
        "t15_route_not_enrolled": _first_failure(f.gates, f.skips) if f.route is not None and not f.holder else None,
        "t15_last_failure": ("fail_" + failing[-1]) if failing else ELIGIBLE,
        "t15_flip_direction": _first_failure(f.gates, f.skipped,
                                             sems={g.letter: FLIP_DIRECTION[g.sem] for g in f.gates}),
        "t15_any_pass": ELIGIBLE if any(g.letter in f.skipped or _passes(g.sem, g.value, g.limit)
                                        for g in f.gates) else None,
    }
    for g in f.gates:
        out["t15_flip_gate_" + g.letter.lower()] = _first_failure(f.gates, f.skipped,
                                                                  sems={g.letter: FLIP_DIRECTION[g.sem]})
    return out


# ------------------------------------------------------------------------------------------------ draw helpers
def _weyl(seed: int, sampler: str, which: int) -> float:
    """Low-discrepancy draw per seed (target answer and question form): shares hold tightly on any run of seeds."""
    alpha = (0.6180339887498949, 0.41421356237309515)[which]
    return (seed * alpha + uhash(FAMILY, "weyl", sampler, which)) % 1.0


def _share(table: tuple, u: float):
    acc = 0.0
    for k, w in table:
        acc += w
        if u < acc:
            return k
    return table[-1][0]


def _weighted(rng: random.Random, items):
    total = sum(w for _, w in items)
    x, acc = rng.random() * total, 0.0
    for k, w in items:
        acc += w
        if x < acc:
            return k
    return items[-1][0]


def _card_rate(sampler: str, card: int) -> float:
    """Per-card gold-yes rate in [0.2, 0.8] (spec 3.0); cards come in antithetic pairs, so the mean is 0.5."""
    h = uhash(FAMILY, "card_rate", sampler, card // 2)
    return 0.2 + 0.6 * (h if card % 2 == 0 else 1.0 - h)


def p_eligible(n_gates: int) -> float:
    """ch_outcome: P(gold = eligible) of a BASE spec with this many gates (G0 v1.3 S20; pilot FIX-2). The target is
    1 / (gates + 1) of the rows, and the minimal-edit twins (28% of the rows) are skewed toward eligible and the early
    gates (an edit that mends the one failing gate gives eligible; one that breaks an earlier gate gives fail A), so the
    base target is lower: OUTCOME_ELIGIBLE and OUTCOME_W solve (1 + eps) q + tau T q = uniform on the measured twin
    transitions T (c2_build/pilot_runs/t15_i1_scratch is the calibration record, never a gate)."""
    return OUTCOME_ELIGIBLE[n_gates]


def claim_key(spec: Spec) -> str:
    return f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"


def claim_plan(row_key: str) -> ChoicePlan:
    """The ch_claimant display plan, from the row key alone (G0 v1.3 S20; c2_kit.choiceplan). k is a label-blind draw
    from CLAIM_K; "Nobody may claim the child" can be shown only when k >= ABSTAIN_MIN_K, on SHOW_ABSTAIN of those rows,
    and is gold on NOBODY_SHARE of the shown rows (always shown when gold: the plan never shows it less than gold).
    The sampler draws the target FIRST from this plan and the structure after it (label-first); nothing is relabelled."""
    k = CLAIM_K[min(len(CLAIM_K) - 1, int(uhash(row_key, "k") * len(CLAIM_K)))]
    if k >= ABSTAIN_MIN_K:
        return plan_choice(row_key, ks=(k,), abstain=True, show_rate=SHOW_ABSTAIN, abstain_share=NOBODY_SHARE)
    return plan_choice(row_key, ks=(k,), abstain=False)


def _pattern_id(rng: random.Random, pattern: str) -> str:
    return "".join(str(rng.randrange(10)) if ch == "#" else ch for ch in pattern)


def _value(rng: random.Random, f: Field, sem: str, limit: int, ok: bool, boost: float) -> int:
    """A value on the planned side of the limit; a boundary value (the limit, one unit or cent away) on P_EDGE."""
    if rng.random() < P_EDGE + boost:
        cands = {("cmp.le", True): (limit, limit - 1), ("cmp.le", False): (limit + 1,),
                 ("cmp.lt", True): (limit - 1,), ("cmp.lt", False): (limit, limit + 1),
                 ("cmp.ge", True): (limit, limit + 1), ("cmp.ge", False): (limit - 1,),
                 ("cmp.gt", True): (limit + 1,), ("cmp.gt", False): (limit, limit - 1)}[(sem, ok)]
        v = cands[0] if len(cands) == 1 or rng.random() < 0.65 else cands[1]
        if v >= 0:
            return v
    if f.sense == "max":
        lo, hi = (int(limit * 0.45), limit - 2) if ok else (limit + 2, int(limit * 1.6) + 2)
    else:
        lo, hi = (limit + 2, int(limit * 1.8) + 2) if ok else (int(limit * 0.3), limit - 2)
    lo, hi = max(lo, f.decoy[0]), min(hi, f.decoy[1])      # stay inside the field's plausible range
    if lo > hi:                                    # tiny limits: fall back to the boundary
        v = {("cmp.le", True): limit, ("cmp.le", False): limit + 1, ("cmp.lt", True): limit - 1,
             ("cmp.lt", False): limit, ("cmp.ge", True): limit, ("cmp.ge", False): limit - 1,
             ("cmp.gt", True): limit + 1, ("cmp.gt", False): limit}[(sem, ok)]
        if v < 0:
            raise ContractError("no value on the planned side")
        return v
    return rng.randint(max(0, lo), hi)


def _decoy(rng: random.Random, f: Field) -> int:
    return rng.randint(*f.decoy)


# ------------------------------------------------------------------------------------------------ the plugin
class T15Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "everyday"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "a18013761c40b4c417a5d92090180f63501daf5fc46fa7e13d4567c6390a5aff"   # frozen (v1.4)
    G0_HAIKU_TASK = "c2-data-stage-a/amb:T15"     # the one Haiku ambiguity pass (G0_SPEC.md section 6)
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "rule_engine"
    PARADIGM_B = "decision_table"
    SOLVER_B_MODULE = "families.T15.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm("ch_outcome", "choice", answer_set="closed"),
        QuestionForm("yn_eligible", "noul", ELIGIBLE, 1, yes_is_bad=False),
        QuestionForm("yn_dneg_eligible", "noul", ELIGIBLE, 1, yes_is_bad=False),
        QuestionForm("yn_ineligible", "noul", ELIGIBLE, -1, "antonym", yes_is_bad=True),
        QuestionForm("yn_gate_stops", "noul", ELIGIBLE, -1, "option_framing", yes_is_bad=True),
        QuestionForm("yn_fails", "noul", ELIGIBLE, -1, "implicit", yes_is_bad=True),
        QuestionForm("yn_not_eligible", "noul", ELIGIBLE, -1, "syntactic", yes_is_bad=True),
        QuestionForm("ch_claimant", "choice", answer_set="open", abstain=True),
        QuestionForm("yn_may_claim", "noul", "claims", 1, yes_is_bad=False),
        QuestionForm("yn_dneg_claim", "noul", "claims", 1, yes_is_bad=False),
        QuestionForm("yn_barred", "noul", "claims", -1, "antonym", yes_is_bad=True),
        QuestionForm("yn_elsewhere", "noul", "claims", -1, "option_framing", yes_is_bad=True),
        QuestionForm("yn_fails_claim", "noul", "claims", -1, "implicit", yes_is_bad=True),
        QuestionForm("yn_may_not", "noul", "claims", -1, "syntactic", yes_is_bad=True),
    )}
    LABEL_WORDS = ("eligible", "ineligible", "qualify", "not eligible", "nobody may claim", "may claim")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("memo", "chat", "email", "ticket", "json", "yaml", "log", "form", "transcript", "voicemail")
    HELD_OUT_REGISTERS = ("transcript", "voicemail")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW = ("Caseworker",)
    # wording polarity (c2_kit.polarity, G0 v1.3 section 7): a yes/no wording reads with its form's declared polarity.
    # The antonym / negative predicates of the family's pool; the option-framing forms (yn_gate_stops, yn_elsewhere)
    # are exempt by the kit; plain "is X not eligible" frames stay (no strict frames). The frozen pool has 0 failures.
    POLARITY_CHECK = True
    POLARITY_NEGATIVES = (r"ineligible", r"barred", r"shut out", r"disqualif\w*", r"excluded?", r"unqualified",
                          r"turned down", r"rejected", r"debarred", r"locked out", r"blocked")

    def __init__(self, lexicon=None, packs=None, names=None):
        """packs: programme packs (make_pack form); None = BUILTIN_PACKS. names: {pool: names} for any of NAME_POOLS
        (female, male, neutral first names; last names; children; workers = caseworker full names); a pool left out
        keeps its built-in value."""
        super().__init__(lexicon)
        self._builtin = packs is None
        self.packs = tuple(packs if packs is not None else BUILTIN_PACKS)
        self._pack_by_id = {pk["id"]: pk for pk in self.packs}
        if len(self._pack_by_id) != len(self.packs):
            raise ContractError("pack ids repeat")
        self._pools = {}
        for kind in PACK_KINDS:
            for held in (False, True):
                pool = tuple(pk for pk in self.packs if pk["kind"] == kind and pk["held_out"] == held)
                if not pool:
                    raise ContractError(f"no {'held-out ' if held else ''}{kind} pack")
                self._pools[(kind, held)] = pool
        nm = dict(names or {})
        if set(nm) - set(NAME_POOLS):
            raise ContractError(f"name pools {sorted(set(nm) - set(NAME_POOLS))}")
        self.female = tuple(nm.get("female", FEMALE_NAMES))
        self.male = tuple(nm.get("male", MALE_NAMES))
        self.first = self.female + self.male + tuple(nm.get("neutral", ("Dana", "Wren")))
        self.last = tuple(nm.get("last", LAST_NAMES))
        self.children = tuple(nm.get("children", CHILDREN))
        self.workers = tuple(nm.get("workers", WORKERS))
        if set(self.female) & set(self.male) or set(self.children) & set(self.first):
            raise ContractError("a first name is in two pools")

    def card_pack(self, sampler: str, card: int) -> dict:
        """The programme pack of a C2 card (G0_SPEC.md S1): gate cards 0-2 household, 3-5 work, 6-9 credits (S5:
        card 0 household, 1 work, 2-3 credits); training samplers take consecutive packs, so with >= 12 / 12 / 16
        training packs every training card has its own."""
        held = sampler in self.HELD_OUT_SAMPLERS
        if held:
            kind, j = (("household", 0) if card == 0 else ("work", 0) if card == 1 else ("credit", card - 2))
        else:
            si = TRAIN_SAMPLERS.index(sampler)
            kind, j = (("household", si * 3 + card) if card < 3 else ("work", si * 3 + card - 3) if card < 6
                       else ("credit", si * 4 + card - 6))
        pool = self._pools[(kind, held)]
        return pool[j % len(pool)]

    def _pack_of(self, structure: dict):
        """The gate pack a spec was drawn from (Haiku packs), or None (built-in v1 sets by domain)."""
        return self._pack_by_id.get(structure.get("pack")) if structure.get("pack") else None

    def _routes(self, structure: dict) -> tuple:
        pk = self._pack_of(structure)
        return pk["routes"] if pk else ROUTES[structure["domain"]]

    def _enrol_set(self, structure: dict) -> tuple:
        pk = self._pack_of(structure)
        return pk["enrol"] if pk else ENROLL_SETS[structure["domain"]]

    # ------------------------------------------------------------------------------------------- sampling
    def _comparator(self, sem: str, bind_to: str, kind: str, rng: random.Random) -> S.Slot:
        """A clause slot from an admitted comparator form of `sem` whose bound has the field's kind."""
        if self.lexicon is None:
            raise ContractError("T15 needs its lexicon registry (T15Plugin(lexicon=...))")
        name = "X" if kind == "cents" else "N"
        ids = _comparator_ids(self.lexicon, sem, name)
        if not ids:
            raise ContractError(f"no admitted comparator form for {sem} on a {kind} bound")
        return self.lexicon.clause(rng.choice(ids), bind={name: bind_to})

    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        held = sampler in self.HELD_OUT_SAMPLERS
        card = seed % (N_CARDS_HELD if held else N_CARDS)
        n_gate = N_GATE_CARDS_HELD if held else N_GATE_CARDS
        track = "gates" if card < n_gate else "claimants"
        qform = _share(QFORM_SHARES[track], _weyl(seed, sampler, 1))
        boost = S2_BOOST if sampler == "S2" else 0.0
        common = {"YEAR": S.count_slot(rng.choice(YEARS)), "WORKER": S.name_slot(rng.choice(self.workers))}
        pk = self.card_pack(sampler, card)
        if track == "gates":
            name, domain = pk["programme"], pk["kind"]
            common["PROG"] = S.name_slot(name)
            common["CASE_ID"] = S.id_slot(_pattern_id(rng, CASE_PATTERNS[domain]))
            for _ in range(20):            # a plan with no consistent income pair is redrawn from the same stream
                try:
                    slots, structure = self._sample_gates(rng, seed, sampler, card, domain, qform, boost, pk)
                    break
                except NoPlan:
                    continue
            else:
                raise ContractError(f"no gate plan for seed {seed} / {sampler}")
            pack = f"t15.gates.{domain}.{sampler}.c{card:02d}" if self._builtin else pk["id"]
        else:
            common["PROG"] = S.name_slot(pk["programme"])
            common["CASE_ID"] = S.id_slot(_pattern_id(rng, CASE_PATTERNS["claimants"]))
            pack = f"t15.claimants.{sampler}.c{card:02d}" if self._builtin else pk["id"]
            plan = claim_plan(f"{FAMILY}|{seed}|{sampler}|{qform}") if qform == "ch_claimant" else None
            for _ in range(50):           # a ch_claimant case the planned options cannot fill is redrawn (G0 S20); the
                slots, structure = self._sample_claimants(rng, seed, sampler, card, qform, boost, plan)   # target stays
                spec = self.derive(Spec(FAMILY, sampler, seed, f"{FAMILY}:{sampler}:c{card:02d}", qform,
                                        {**common, **slots}, structure=structure, depth=2, pack=pack))
                if self._options_ok(spec):
                    return spec
            raise ContractError(f"no ch_claimant case fills the drawn options (seed {seed} / {sampler})")
        spec = Spec(FAMILY, sampler, seed, f"{FAMILY}:{sampler}:c{card:02d}", qform, {**common, **slots},
                    structure=structure, depth=2, pack=pack)
        return self.derive(spec)

    # ---------------------------------------------------------------------------------- gates track
    def _sample_gates(self, rng, seed, sampler, card, domain, qform, boost, pk) -> tuple:
        # display and rule draws first (label-blind): gate list, comparators, limits, route, enrolment, applicant
        k = _weighted(rng, GATE_COUNTS)
        fids = self._gate_fields(rng, domain, k)
        sems = [rng.choice(("cmp.le", "cmp.lt")) if FIELDS[f].sense == "max" else rng.choice(("cmp.ge", "cmp.gt"))
                for f in fids]
        limits = self._limits(rng, domain, fids)
        route = None
        if rng.random() < P_ROUTE:
            n_skip = rng.randint(1, k - 1)
            weights = [(i, 2.0 if fids[i] in INCOME_PAIR[domain] else 1.0) for i in range(k)]
            chosen = []
            for _ in range(n_skip):
                i = _weighted(rng, [(j, w) for j, w in weights if j not in chosen])
                chosen.append(i)
            route = tuple(sorted(chosen))
            route_name, near = rng.choice(pk["routes"])
        holder = route is not None and rng.random() < P_HOLDER
        if holder:
            enroll = route_name
        elif route is not None:
            others = [e for e in pk["enrol"] if e not in (route_name, near)]
            enroll = near if near and rng.random() < P_NEAR + boost else rng.choice(others)
        else:
            enroll = rng.choice(pk["enrol"])
        subject = f"{rng.choice(self.first)} {rng.choice(self.last)}"
        # then the target, then statuses and values that realise it
        u = _weyl(seed, sampler, 0)
        q = self.QFORMS[qform]
        if qform == "ch_outcome":
            eligible = u < p_eligible(k)
        else:
            yes = u < _card_rate(sampler, card)
            eligible = yes if q.polarity == 1 else not yes
        skipped = set(route) if holder else set()
        avail = [i for i in range(k) if i not in skipped]
        d = None
        if not eligible:
            if route is not None and not holder and rng.random() < P_ROUTE_DECIDES + boost:
                d = rng.choice(list(route))
            elif qform == "ch_outcome":
                d = _weighted(rng, [(i, OUTCOME_W[k][i]) for i in avail])
            else:
                d = rng.choice(avail)
        status = []
        for i in range(k):
            if i in skipped:
                status.append(rng.random() >= P_SKIP_FAIL + boost)
            elif d is None or i < d:
                status.append(True)
            elif i == d:
                status.append(False)
            else:
                status.append(rng.random() >= P_MULTI + boost)
        gated = {fids[i]: (sems[i], limits[fids[i]], status[i]) for i in range(k)}
        values = self._facts(rng, domain, gated, boost)
        slots = {"SUBJECT": S.name_slot(subject),
                 "ENROLL": S.category_slot(enroll, {e: [e] for e in pk["enrol"]})}
        if route is not None:
            slots["ROUTE"] = S.category_slot(route_name, {e: [e] for e in pk["enrol"]})
        for i, fid in enumerate(fids):
            f = FIELDS[fid]
            slots[f"G{i + 1}_LIM"] = self._num_slot(f, limits[fid])
            slots[f"G{i + 1}_CMP"] = self._comparator(sems[i], f"G{i + 1}_LIM", f.kind, rng)
        for fid in DOMAIN_FIELDS[domain]:
            slots[FIELDS[fid].slot] = self._num_slot(FIELDS[fid], values[fid])
        structure = {"track": "gates", "domain": domain, "gates": list(fids),
                     "route": list(route) if route is not None else None, "deep": k >= DEEP_COUNT}
        if not self._builtin:
            structure["pack"] = pk["id"]
        return slots, structure

    @staticmethod
    def _num_slot(f: Field, v: int) -> S.Slot:
        return S.cents_slot(v) if f.kind == "cents" else S.count_slot(v, f.unit)

    @staticmethod
    def _gate_fields(rng: random.Random, domain: str, k: int) -> list:
        pool = list(DOMAIN_FIELDS[domain])
        income = INCOME_PAIR[domain]
        want_income = rng.random() < P_INCOME_GATE
        for _ in range(100):
            fids = rng.sample(pool, k)
            if want_income == any(f in income for f in fids):
                return fids
        return fids                                   # k = 4 of 5 fields always holds an income gate

    @staticmethod
    def _limits(rng: random.Random, domain: str, fids) -> dict:
        lim = {}
        for fid in fids:
            lo, hi, step = FIELDS[fid].lim
            lim[fid] = rng.randrange(lo, hi + 1, step)
            while (fid, lim[fid]) in REAL_LIMITS:
                lim[fid] = rng.randrange(lo, hi + 1, step)
        g, n = INCOME_PAIR[domain]
        if g in lim and n in lim:                         # both income gates: the net limit sits under the gross one
            step = FIELDS[n].lim[2]
            lim[n] = max(step, round(lim[g] * rng.uniform(0.70, 0.85) / step) * step)
        return lim

    @staticmethod
    def _facts(rng: random.Random, domain: str, gated: dict, boost: float) -> dict:
        """Every domain fact: gated ones on their planned side; net strictly below gross (G0_SPEC.md S2)."""
        g, n = INCOME_PAIR[domain]
        for _ in range(400):
            vals = {}
            for fid in DOMAIN_FIELDS[domain]:
                if fid in (g, n):
                    continue
                f = FIELDS[fid]
                vals[fid] = _value(rng, f, *gated[fid], boost) if fid in gated else _decoy(rng, f)
            gv = _value(rng, FIELDS[g], *gated[g], boost) if g in gated else None
            nv = _value(rng, FIELDS[n], *gated[n], boost) if n in gated else None
            if gv is None and nv is None:
                gv = _decoy(rng, FIELDS[g])
                nv = int(gv * rng.uniform(0.62, 0.90))
            elif nv is None:
                sem, lim, ok = gated[g]
                hi = lim if sem == "cmp.le" else lim - 1
                lo = int(gv * 0.62)
                if not ok and lo <= min(hi, gv - 1) and rng.random() < P_NET_TRAP + boost:
                    nv = rng.randint(lo, min(hi, gv - 1))          # net reads as passing the gross gate
                else:
                    nv = int(gv * rng.uniform(0.62, 0.90))
            elif gv is None:
                gv = int(nv / rng.uniform(0.62, 0.90)) + 1
            if 0 < nv < gv:
                vals[g], vals[n] = gv, nv
                return vals
        raise NoPlan("no consistent income pair for this gate plan")

    # ---------------------------------------------------------------------------------- claimants track
    def _sample_claimants(self, rng, seed, sampler, card, qform, boost, plan=None) -> tuple:
        m = _weighted(rng, PEOPLE_COUNTS)
        order = tuple(rng.sample(TIEBREAKS, 3))
        min_m = rng.choice((5, 6, 7))
        min_sem = rng.choice(("cmp.ge", "cmp.gt"))
        child = rng.choice(self.children)
        u = _weyl(seed, sampler, 0)
        q = self.QFORMS[qform]
        if qform == "ch_claimant":
            nobody, asked_wins = plan.gold_abstain, None           # label-first: the plan's target (G0 v1.3 S20)
        else:
            yes = u < _card_rate(sampler, card)
            asked_wins = yes if q.polarity == 1 else not yes
            nobody = (not asked_wins) and rng.random() < P_NOBODY_NO
        want = {"order": rng.random() < P_ORDER_TRAP + boost, "filed": rng.random() < P_FILED_TRAP + boost,
                "edge": rng.random() < P_EDGE_MONTHS + boost, "tie": rng.random() < P_INCOME_TIE + boost / 2,
                "third": (not nobody) and rng.random() < P_THIRD + boost / 2}
        drop_order = ("tie", "third", "edge", "order", "filed")
        for attempt in range(4000):
            relax = set(drop_order[:attempt // 500])
            people = self._draw_people(rng, m, min_sem, min_m, boost, want["edge"] and "edge" not in relax,
                                       want["tie"] and "tie" not in relax, want["third"] and "third" not in relax)
            c = ClaimFacts(people, min_sem, min_m, order, None)
            try:
                w = _claim_winner(c)
            except Tie:
                continue
            if (w is None) != nobody:
                continue
            if want["third"] and "third" not in relax and _steps(c) < 3:
                continue
            var = _claim_variants(c)
            if want["order"] and "order" not in relax and not any(
                    var[k] not in (None, NONE_KEY if w is None else w)
                    for k in ("wrong_tiebreak", "t15_default_order", "t15_swap_first_two")):
                continue
            if want["filed"] and "filed" not in relax and var["t15_skip_filed_check"] in (None, w or NONE_KEY):
                continue
            gold = NONE_KEY if w is None else w
            wrong = sorted({a for a in var.values() if a not in (None, gold)})
            if qform == "ch_claimant" and not wrong:
                continue                                    # every ch_claimant row shows >= 1 named distractor
            asked = None
            if qform != "ch_claimant":
                if asked_wins:
                    asked = w
                else:
                    traps = [a for a in wrong if a != NONE_KEY]
                    losers = [p.name for p in people if p.name != w]
                    asked = rng.choice(traps) if traps and rng.random() < P_ASK_TRAP + boost else rng.choice(losers)
            break
        else:
            raise ContractError("claimant draw found no people for this target")
        slots = {"SUBJECT": S.name_slot(child), "MIN_M": S.count_slot(min_m, UNIT_MONTH),
                 "MIN_CMP": self._comparator(min_sem, "MIN_M", "count", rng)}
        for i, p in enumerate(people, 1):
            slots[f"C{i}_NAME"] = S.name_slot(p.name)
            slots[f"C{i}_REL"] = S.category_slot(p.rel, REL_SET)
            slots[f"C{i}_MONTHS"] = S.count_slot(p.months, UNIT_MONTH)
            slots[f"C{i}_INC"] = S.cents_slot(p.income)
            slots[f"C{i}_FILED"] = S.category_slot(p.filed, FILED_SET)
        if asked is not None:
            slots["ASKED"] = S.name_slot(asked)
        return slots, {"track": "claimants", "people": m, "order": list(order), "deep": m >= DEEP_COUNT}

    def _draw_people(self, rng, m, min_sem, min_m, boost, edge: bool, tie: bool, third: bool = False) -> tuple:
        rels, used, names = [], set(), []
        for _ in range(m):
            free = [r for r in PARENTS if r not in used]
            if free and rng.random() < P_PARENT:
                r = rng.choice(free)
                used.add(r)
            else:
                r = rng.choice(NONPARENTS)
            rels.append(r)
            # a first name that agrees with the relationship and differs from every other person's first name
            firsts = {n.split()[0] for n in names}
            first = rng.choice([x for x in (self.female if r in FEMALE_RELS else self.male) if x not in firsts])
            names.append(f"{first} {rng.choice(self.last)}")
        months = [rng.randint(0, 12) for _ in range(m)]
        if edge:
            j = rng.randrange(m)
            months[j] = min_m if rng.random() < 0.7 else (min_m - 1 if min_sem == "cmp.ge" else min_m + 1)
        incomes = []
        for _ in range(m):
            v = rng.randrange(1500000, 9500001, 100)
            incomes.append(v + rng.randint(1, 99) if rng.random() < 0.3 else v)
        if tie and m >= 2:
            a, b = rng.sample(range(m), 2)
            incomes[b] = incomes[a]
        filed = ["yes" if rng.random() < P_FILED - boost / 2 else "no" for _ in range(m)]
        if third and m >= 2:                              # two people tie on parent status and months, both running
            a, b = rng.sample(range(m), 2)
            if (rels[a] in PARENTS) != (rels[b] in PARENTS):
                j = a if rels[a] in PARENTS else b
                rels[j] = {"mother": "aunt", "father": "uncle"}[rels[j]]
            months[a] = months[b] = max(months[a], min_m + 1)
            filed[a] = filed[b] = "yes"
        return tuple(Person(names[i], rels[i], months[i], incomes[i], filed[i]) for i in range(m))

    # ---------------------------------------------------------------------------------- derive / tags
    def derive(self, spec: Spec) -> Spec:
        """No printed intermediates (every compared value is printed as given); recompute trap tags and depth."""
        tags, deep = self._tags(spec)
        if "deep" in spec.structure:                  # drawn from the seed before the target (A43 b), never from the answer
            deep = bool(spec.structure["deep"])
        return spec.replace(tags=tags, deep=deep, depth=3 if deep else 2)

    def _tags(self, spec: Spec) -> tuple:
        t = set()
        if spec.structure["track"] == "gates":
            f = gate_facts(spec)
            out = _gate_outcome(f)
            var = _gate_variants(f)
            t.add("route_listed" if f.route else "no_route")
            if f.holder:
                t.add("route_holder")
            if out == ELIGIBLE:
                t.add("outcome_eligible")
            if var["stop_at_first_gate"] != out:
                t.add("first_gate_trap")
            if var["net_vs_gross"] not in (None, out):
                t.add("net_gross_trap")
            if var["t15_ignore_route"] not in (None, out):
                t.add("route_decides")
            if var["t15_route_not_enrolled"] not in (None, out):
                t.add("route_not_enrolled_trap")
            if f.route and not f.holder and f.enroll != "none":
                t.add("other_enrolment")
            if any(g.value == g.limit for g in f.gates):
                t.add("at_limit")
            if any(abs(g.value - g.limit) == 1 for g in f.gates):
                t.add("one_off_limit")
            if any(g.value == g.limit and g.sem in ("cmp.le", "cmp.ge") for g in f.gates):
                t.add("at_limit_passes")
            failing = [g for g in f.gates if g.letter not in f.skipped and not _passes(g.sem, g.value, g.limit)]
            if len(failing) >= 2:
                t.add("multi_fail")
            tested = len(f.gates) if out == ELIGIBLE else LETTERS.index(out[-1]) + 1
            deep = tested >= 4
        else:
            c = claim_facts(spec)
            w = _claim_winner(c)
            var = _claim_variants(c)
            gold = NONE_KEY if w is None else w
            if w is None:
                t.add("nobody")
            if any(var[k] not in (None, gold) for k in ("wrong_tiebreak", "t15_default_order",
                                                         "t15_swap_first_two")):
                t.add("order_trap")
            if var["t15_skip_filed_check"] not in (None, gold):
                t.add("filed_trap")
            if var["t15_skip_months_check"] not in (None, gold):
                t.add("months_trap")
            if any(p.months == c.min_m for p in c.people):
                t.add("months_at_minimum")
            pool = [p for p in c.people if p.filed == "yes" and _passes(c.min_sem, p.months, c.min_m)]
            if len({p.income for p in pool}) < len(pool):
                t.add("income_tie")
            if any(p.rel in PARENTS for p in pool) and w is not None and w not in {p.name for p in pool
                                                                                   if p.rel in PARENTS}:
                t.add("parent_loses")
            steps = _steps(c)
            if steps >= 2:
                t.add("second_tiebreak")
            if steps >= 3:
                t.add("third_tiebreak")
            deep = steps >= 3
        return tuple(sorted(t)), deep

    # ------------------------------------------------------------------------------------------- solver A
    def solve_a(self, spec: Spec):
        if spec.structure["track"] == "gates":
            outcome = RL.resolve(_gate_ruleset(spec), spec.env()).effect
            return QUESTION_TABLE[spec.qform](outcome, None)
        winner = _claim_steps(spec)
        return QUESTION_TABLE[spec.qform](winner, spec.env().get("ASKED"))

    def canonical(self, spec: Spec) -> dict:
        v = spec.env()
        st = spec.structure
        out = {"track": st["track"], "prog": v["PROG"], "year": v["YEAR"], "subject": v["SUBJECT"],
               "worker": v["WORKER"], "case_id": v["CASE_ID"], "qform": spec.qform}
        if st["track"] == "gates":
            out.update(domain=st["domain"],
                       gates=[[fid, v[f"G{i + 1}_CMP"], v[f"G{i + 1}_LIM"]] for i, fid in enumerate(st["gates"])],
                       route=None if not st["route"] else {"programme": v["ROUTE"],
                                                           "skips": [LETTERS[i] for i in st["route"]]},
                       facts={fid: v[FIELDS[fid].slot] for fid in DOMAIN_FIELDS[st["domain"]]},
                       enrolled=v["ENROLL"])
        else:
            out.update(min_sem=v["MIN_CMP"], min_months=v["MIN_M"], order=list(st["order"]),
                       people=[[v[f"C{i}_NAME"], v[f"C{i}_REL"], v[f"C{i}_MONTHS"], v[f"C{i}_INC"], v[f"C{i}_FILED"]]
                               for i in range(1, st["people"] + 1)],
                       asked=v.get("ASKED"))
        return out

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        if author_mode != "T":
            raise ContractError("T15 v1 is Mode T only (G0_SPEC.md S19)")
        return self.canonical(spec)

    # ------------------------------------------------------------------------------------------- render
    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        key = f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        skin = skin or ctx.pick(FAMILY, "skin", key, held_out=held)
        if skin.author_mode != "T":
            raise ContractError(f"skin {skin.skin_id}: T15 v1 renders Mode T skins only")
        if wording is None:                 # S5 prefers held-out wordings (mixdev); training rows never use them
            try:
                wording = ctx.pick(FAMILY, "wording", key, qform=spec.qform, held_out=held)
            except LookupError:
                if not held:
                    raise
                wording = ctx.pick(FAMILY, "wording", key, qform=spec.qform)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, key)
        slots = spec.all_slots()
        st = spec.structure
        style = facts_style(spec.sampler, skin.register)
        if st["track"] == "gates":
            head, body, escape = gate_facts_template(st["domain"], style)
            card = gate_card_template(tuple(st["gates"]), tuple(st["route"]) if st["route"] else None)
        else:
            head, body, escape = claim_facts_template(st["people"], style)
            card = claim_card_template(tuple(st["order"]))
        tb = TextBuilder()

        def note():
            tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id)

        def facts():
            tb.add("state", K.fill(head, slots, forms)).add("state", "\n")
            tb.add("state", K.fill(body, slots, forms, escape=escape))
            if attack is not None:
                tb.add("state", "\n" + NOTE_PREFIX).add("state", attack.fill(slots, forms), skin_id=attack.skin_id)

        if spec.sampler == "S3":
            facts()
            tb.add("state", "\n\n")
            note()
        else:
            note()
            tb.add("state", "\n\n")
            facts()
        # G0 v1.3 S18 (pilot FIX-3): the served prompt prints row.instructions twice and row.card once on yes/no rows, so
        # a yes/no row carries its rules in row.card (its definitions block) and a choice row, which prints no card,
        # keeps them at the head of its instructions. Same words, same order; only the field changes.
        placed = CARDS.place_rules(tb, K.fill(card, slots, forms), self.QFORMS[spec.qform].qtype)
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if spec.qform == "ch_outcome":
            gates = tuple(st["gates"])
            keys = [ELIGIBLE] + [f"fail_{LETTERS[i]}" for i in range(len(gates))]
            os_ = build_closed(spec, ans, keys, self.error_models(), row_key=key,
                               render_key=lambda k: outcome_text(k, gates))
        elif spec.qform == "ch_claimant":
            os_ = self._claimant_options(spec, ans)
            if os_ is None:
                raise K.RenderError("ch_claimant: too few named answers for the drawn option count")
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, format_style=f"{skin.register}/{style}",
                            defs_style=CARDS.defs_style(placed, "full"))

    def _claimant_options(self, spec: Spec, ans):
        """The ch_claimant options of the row's plan (claim_plan: k, the display of "Nobody may claim the child" and its
        position all come from the row key). None when the named answers cannot fill the planned set: the spec is
        resampled (sample) or the twin is not proposed (relations), never re-tried with a smaller k or with "nobody"
        forced on. A nobody gold needs a plan that targets it (base, equiv and inv rows): a twin never ends in nobody
        (_twin_claimants), so the displayed set stays a function of the row key, not of the gold. A twin of a nobody
        base keeps the base's k and display (strict_plan False: the plan adapts to the person gold)."""
        key = claim_key(spec)
        plan = claim_plan(key)
        if ans == NONE_KEY and not plan.gold_abstain:
            return None
        return build_options(spec, ans, self.error_models(), row_key=key,
                             render_key=lambda a: NONE_TEXT if a == NONE_KEY else a,
                             abstain=(NONE_KEY, NONE_TEXT), plan=plan, strict_plan=False)

    def _options_ok(self, spec: Spec) -> bool:
        return spec.qform != "ch_claimant" or self._claimant_options(spec, self.solve_a(spec)) is not None

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        out = []
        q = self.QFORMS[spec.qform]
        if q.qtype == "noul" and uhash(FAMILY, "complement", spec.sampler, spec.seed) < COMP_RATE:
            out.append(RelationProposal("complement", qform=self._partner(spec)))
        u = uhash(FAMILY, "extra", spec.sampler, spec.seed)
        if u < EQUIV_RATE:
            out.append(RelationProposal("equiv"))
        elif u < EQUIV_RATE + INV_RATE:
            out.append(RelationProposal("inv"))
        if uhash(FAMILY, "twin", spec.sampler, spec.seed) < TWIN_RATE:
            t = self._twin(spec)
            if t is not None and self._options_ok(self.derive(t.spec)):
                out.append(t)
        return out + [m for m in self._metamorphic(spec) if self._options_ok(self.derive(m.spec))]

    def _partner(self, spec: Spec) -> str:
        """The complement form: same predicate, opposite polarity; syntactic pairs differ by one negation cue."""
        u = uhash(FAMILY, "complement_kind", spec.sampler, spec.seed)
        return _share(PARTNERS[spec.qform], u)

    def _twin(self, spec: Spec):
        """Exactly one input slot changes; the prediction comes from the edited construction (_first_failure /
        _cascade), never from solve_a. The first edit (in a seeded order) that changes the answer is used."""
        rng = random.Random(f"{FAMILY}|twin|{spec.sampler}|{spec.seed}")
        if spec.structure["track"] == "gates":
            return self._twin_gates(spec, rng)
        return self._twin_claimants(spec, rng)

    def _twin_gates(self, spec: Spec, rng: random.Random):
        f = gate_facts(spec)
        base = _gate_answer(spec.qform, f)
        g_name, n_name = INCOME_PAIR[f.domain]
        kinds = sorted(("fact", "limit", "comparator", "route"),
                       key=lambda k: uhash(FAMILY, "twin_kind", spec.sampler, spec.seed, k))
        order = sorted(range(len(f.gates)), key=lambda i: uhash(FAMILY, "twin_gate", spec.sampler, spec.seed, i))
        for kind in kinds:
            if kind == "route":
                if f.route is None:
                    continue
                if f.holder:
                    near = next((nm for r, nm in self._routes(spec.structure) if r == f.route), None)
                    new = near or "none"
                else:
                    new = f.route
                f2 = replace(f, enroll=new)
                ans = _gate_answer(spec.qform, f2)
                if ans != base:
                    slot = S.category_slot(new, {e: [e] for e in self._enrol_set(spec.structure)})
                    return RelationProposal("twin", spec=spec.with_slot("ENROLL", slot), changed_slot="ENROLL",
                                            expect=ans, note="twin route")
                continue
            for i in order:
                g = f.gates[i]
                ok = _passes(g.sem, g.value, g.limit)
                fld = FIELDS[g.fid]
                if kind == "fact":
                    new_v = {("cmp.le", True): g.limit + 1, ("cmp.lt", True): g.limit, ("cmp.ge", True): g.limit - 1,
                             ("cmp.gt", True): g.limit, ("cmp.le", False): g.limit, ("cmp.lt", False): g.limit - 1,
                             ("cmp.ge", False): g.limit, ("cmp.gt", False): g.limit + 1}[(g.sem, ok)]
                    if new_v < 0:
                        continue
                    facts2 = {**f.facts, g.fid: new_v}
                    if not 0 < facts2[n_name] < facts2[g_name]:
                        continue
                    gates2 = tuple(replace(x, value=new_v) if x.fid == g.fid else x for x in f.gates)
                    f2 = replace(f, gates=gates2, facts=facts2)
                    name, slot = fld.slot, self._num_slot(fld, new_v)
                elif kind == "limit":
                    new_l = {("cmp.le", True): g.value - 1, ("cmp.lt", True): g.value, ("cmp.ge", True): g.value + 1,
                             ("cmp.gt", True): g.value, ("cmp.le", False): g.value, ("cmp.lt", False): g.value + 1,
                             ("cmp.ge", False): g.value, ("cmp.gt", False): g.value - 1}[(g.sem, ok)]
                    if new_l < 1 or (g.fid, new_l) in REAL_LIMITS:      # G0 H38: never a real threshold
                        continue
                    f2 = replace(f, gates=tuple(replace(x, limit=new_l) if x.letter == g.letter else x
                                                for x in f.gates))
                    name, slot = f"G{i + 1}_LIM", self._num_slot(fld, new_l)
                else:  # comparator: only an inclusive / exclusive swap at the limit moves the gate
                    if g.value != g.limit:
                        continue
                    new_sem = INCLUSIVE.get(g.sem) or EXCLUSIVE[g.sem]
                    f2 = replace(f, gates=tuple(replace(x, sem=new_sem) if x.letter == g.letter else x
                                                for x in f.gates))
                    name = f"G{i + 1}_CMP"
                    slot = self._comparator(new_sem, f"G{i + 1}_LIM", fld.kind, rng)
                ans = _gate_answer(spec.qform, f2)
                if ans != base:
                    return RelationProposal("twin", spec=spec.with_slot(name, slot), changed_slot=name, expect=ans,
                                            note=f"twin {kind}")
        return None

    def _twin_claimants(self, spec: Spec, rng: random.Random):
        c = claim_facts(spec)
        base = _claim_answer(spec.qform, c)
        kinds = sorted(("months", "filed", "income", "relation"),
                       key=lambda k: uhash(FAMILY, "twin_kind", spec.sampler, spec.seed, k))
        order = sorted(range(len(c.people)), key=lambda i: uhash(FAMILY, "twin_person", spec.sampler, spec.seed, i))
        for kind in kinds:
            for j in order:
                p = c.people[j]
                if kind == "months":
                    inside = _passes(c.min_sem, p.months, c.min_m)
                    new = {("cmp.ge", True): c.min_m - 1, ("cmp.gt", True): c.min_m,
                           ("cmp.ge", False): c.min_m, ("cmp.gt", False): c.min_m + 1}[(c.min_sem, inside)]
                    if not 0 <= new <= 12:
                        continue
                    p2 = replace(p, months=new)
                    name, slot = f"C{j + 1}_MONTHS", S.count_slot(new, UNIT_MONTH)
                elif kind == "filed":
                    new = "no" if p.filed == "yes" else "yes"
                    p2 = replace(p, filed=new)
                    name, slot = f"C{j + 1}_FILED", S.category_slot(new, FILED_SET)
                elif kind == "income":
                    others = [q.income for q in c.people if q is not p]
                    top = max(others)
                    new = top + 100 if p.income <= top else top - 100
                    if new <= 0:
                        continue
                    p2 = replace(p, income=new)
                    name, slot = f"C{j + 1}_INC", S.cents_slot(new)
                else:
                    taken = {q.rel for q in c.people if q is not p}
                    if p.rel in PARENTS:
                        new = {"mother": "grandmother", "father": "grandfather"}[p.rel]
                    else:
                        free = [r for r in PARENTS if r not in taken]
                        new = {"grandmother": "mother", "aunt": "mother", "grandfather": "father",
                               "uncle": "father"}[p.rel]
                        if new not in free:                   # the parent of that gender is already listed
                            continue
                    p2 = replace(p, rel=new)
                    name, slot = f"C{j + 1}_REL", S.category_slot(new, REL_SET)
                c2 = replace(c, people=c.people[:j] + (p2,) + c.people[j + 1:])
                try:
                    ans = _claim_answer(spec.qform, c2)
                except Tie:
                    continue
                if spec.qform == "ch_claimant" and ans == NONE_KEY:
                    continue                                # a twin never ends in nobody (claim_plan, G0 v1.3 S20)
                if spec.qform == "ch_claimant" and not any(a not in (None, ans) for a in _claim_variants(c2).values()):
                    continue                                # like the sampler: >= 1 named distractor on the twin
                if ans != base:
                    return RelationProposal("twin", spec=spec.with_slot(name, slot), changed_slot=name, expect=ans,
                                            note=f"twin {kind}")
        return None

    def _metamorphic(self, spec: Spec) -> list:
        """G4 (checked, never emitted): changes the card says never matter keep the answer."""
        rng = random.Random(f"{FAMILY}|g4|{spec.sampler}|{spec.seed}")
        v = spec.env()
        out = [RelationProposal("metamorphic", spec=spec.with_slot("YEAR", S.count_slot(
                   next(y for y in YEARS if y != v["YEAR"]))), expect="same", note="change the year"),
               RelationProposal("metamorphic", spec=spec.with_slot("WORKER", S.name_slot(
                   next(w for w in self.workers if w != v["WORKER"]))), expect="same", note="rename the caseworker")]
        if spec.structure["track"] == "gates":
            f = gate_facts(spec)
            subj = next(f"{a} {b}" for a in self.first for b in self.last if f"{a} {b}" != v["SUBJECT"])
            out.append(RelationProposal("metamorphic", spec=spec.with_slot("SUBJECT", S.name_slot(subj)),
                                        expect="same", note="rename the applicant"))
            gated = {g.fid for g in f.gates}
            g_name, n_name = INCOME_PAIR[f.domain]
            for fid in sorted(set(DOMAIN_FIELDS[f.domain]) - gated, key=lambda x: uhash(spec.seed, x)):
                fld = FIELDS[fid]
                new = _decoy(rng, fld)
                facts2 = {**f.facts, fid: new}
                if new != f.facts[fid] and 0 < facts2[n_name] < facts2[g_name]:
                    out.append(RelationProposal("metamorphic", spec=spec.with_slot(fld.slot, self._num_slot(fld, new)),
                                                expect="same", note="change an ungated fact"))
                    break
            for g in sorted(f.gates, key=lambda x: uhash(spec.seed, "deeper", x.letter)):
                fld = FIELDS[g.fid]
                if not _passes(g.sem, g.value, g.limit):
                    continue
                step = max(1, g.limit // 10)
                new = g.value - step if fld.sense == "max" else g.value + step
                facts2 = {**f.facts, g.fid: new}
                if new >= 0 and 0 < facts2[n_name] < facts2[g_name]:
                    out.append(RelationProposal("metamorphic", spec=spec.with_slot(fld.slot, self._num_slot(fld, new)),
                                                expect="same", note="move a passing fact further inside its limit"))
                    break
            if not f.holder:
                others = [e for e in self._enrol_set(spec.structure) if e not in (f.enroll, f.route)]
                new = others[int(uhash(spec.seed, "enroll") * len(others))]
                out.append(RelationProposal("metamorphic", spec=spec.with_slot("ENROLL", S.category_slot(
                    new, {e: [e] for e in self._enrol_set(spec.structure)})), expect="same",
                    note="change a non-route enrolment"))
        else:
            c = claim_facts(spec)
            w = _claim_winner(c)
            child = next(x for x in self.children if x != v["SUBJECT"])
            out.append(RelationProposal("metamorphic", spec=spec.with_slot("SUBJECT", S.name_slot(child)),
                                        expect="same", note="rename the child"))
            m = len(c.people)
            perm = list(range(m))[::-1]
            slots2 = dict(spec.slots)
            for i, j in enumerate(perm, 1):
                for part in ("NAME", "REL", "MONTHS", "INC", "FILED"):
                    slots2[f"C{i}_{part}"] = spec.slots[f"C{j + 1}_{part}"]
            out.append(RelationProposal("metamorphic", spec=spec.replace(slots=slots2), expect="same",
                                        note="reverse the order of the people"))
            names = {p.name for p in c.people}
            for j, p in enumerate(c.people):
                if p.name in (w, c.asked):
                    continue
                pool = self.female if p.rel in FEMALE_RELS else self.male
                firsts = {n.split()[0] for n in names}
                new = next(f"{a} {b}" for a in pool for b in self.last if a not in firsts)
                out.append(RelationProposal("metamorphic", spec=spec.with_slot(f"C{j + 1}_NAME", S.name_slot(new)),
                                            expect="same", note="rename a person who does not win"))
                break
            if w is not None:
                j = next(i for i, p in enumerate(c.people) if p.name == w)
                out.append(RelationProposal("metamorphic", spec=spec.with_slot(
                    f"C{j + 1}_INC", S.cents_slot(c.people[j].income + 100000)), expect="same",
                    note="raise the winner's income"))
        return out

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def run(name):
            def fn(spec):
                if spec.qform == "ch_outcome":
                    return _gate_variants(gate_facts(spec)).get(name)
                if spec.qform == "ch_claimant":
                    c = claim_facts(spec)
                    return {**_claim_variants(c), **_claim_extra(c)}.get(name)
                return None
            return fn

        return {n: error_model(n, run(n)) for n in dict.fromkeys(GATE_MODELS + CLAIM_MODELS)}


# ------------------------------------------------------------------------------------------------ solver A
def _comparator_ids(lexicon, sem: str, slot_name: str) -> list:
    return sorted(fid for fid, x in lexicon.forms.items()
                  if x.sem_id == sem and x.kind == "comparator" and dict(x.slots).get(slot_name)
                  and lexicon.status(fid) == "admitted")


def _gate_ruleset(spec: Spec) -> RL.RuleSet:
    """Solver A, gates: an ordered decision list. Rule "fail_X" fires when Gate X fails (and, for a skippable gate,
    the applicant is not enrolled in the route); first_match picks the first listed; default eligible."""
    st = spec.structure
    env = spec.env()
    skips = set(st["route"] or ())
    enrolled = RL.Cmp("==", RL.Ref("ENROLL"), RL.Ref("ROUTE"))
    rules = []
    for i, fid in enumerate(st["gates"]):
        test = RL.Cmp(OP[env[f"G{i + 1}_CMP"]], RL.Ref(FIELDS[fid].slot), RL.Ref(f"G{i + 1}_LIM"))
        when = RL.And((RL.Not(enrolled), RL.Not(test))) if i in skips else RL.Not(test)
        rules.append(RL.Rule(f"fail_{LETTERS[i]}", f"fail_{LETTERS[i]}", when))
    return RL.RuleSet(tuple(rules), "first_match", ELIGIBLE)


def _claim_steps(spec: Spec):
    """Solver A, claimants: the card's steps as rules, in order. Steps one and two are rule filters; each
    tie-breaker keeps the people with the best score; a full tie is never generated (refused here)."""
    env = spec.env()
    op = OP[env["MIN_CMP"]]
    left = []
    for i in range(1, spec.structure["people"] + 1):
        rule = RL.And((RL.Cmp("==", RL.Ref(f"C{i}_FILED"), RL.Lit("yes")),
                       RL.Cmp(op, RL.Ref(f"C{i}_MONTHS"), RL.Ref("MIN_M"))))
        if RL.evaluate(rule, env):
            left.append(i)
    parent = {i: RL.evaluate(RL.In(RL.Ref(f"C{i}_REL"), tuple(RL.Lit(r) for r in PARENTS)), env) for i in left}
    score = {"parent": lambda i: 1 if parent[i] else 0, "months": lambda i: env[f"C{i}_MONTHS"],
             "income": lambda i: env[f"C{i}_INC"]}
    for tb in spec.structure["order"]:
        if len(left) < 2:
            break
        best = max(score[tb](i) for i in left)
        left = [i for i in left if score[tb](i) == best]
    if not left:
        return None
    if len(left) > 1:
        raise ContractError("full tie among claimants (never generated)")
    return env[f"C{left[0]}_NAME"]


QUESTION_TABLE = {
    "ch_outcome": lambda o, a: o,
    "yn_eligible": lambda o, a: 1 if o == ELIGIBLE else 0,
    "yn_dneg_eligible": lambda o, a: 1 if o == ELIGIBLE else 0,
    "yn_ineligible": lambda o, a: 0 if o == ELIGIBLE else 1,
    "yn_gate_stops": lambda o, a: 0 if o == ELIGIBLE else 1,
    "yn_fails": lambda o, a: 0 if o == ELIGIBLE else 1,
    "yn_not_eligible": lambda o, a: 0 if o == ELIGIBLE else 1,
    "ch_claimant": lambda w, a: NONE_KEY if w is None else w,
    "yn_may_claim": lambda w, a: 1 if w is not None and w == a else 0,
    "yn_dneg_claim": lambda w, a: 1 if w is not None and w == a else 0,
    "yn_barred": lambda w, a: 0 if w is not None and w == a else 1,
    "yn_elsewhere": lambda w, a: 0 if w is not None and w == a else 1,
    "yn_fails_claim": lambda w, a: 0 if w is not None and w == a else 1,
    "yn_may_not": lambda w, a: 0 if w is not None and w == a else 1,
}
