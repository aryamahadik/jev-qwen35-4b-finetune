"""transfer/T20/plugin.py: T20 "incident severity with override precedence and timed escalation" (C2_DATA_SPEC 2.2,
3.20; transfer dev only). G0_SPEC.md v3 (fix iteration 1 of the pilot verdict, F1-F6).

An incident record (service, users affected, reported urgency, customer-data exposure, opening, acknowledgement and
check times with fixed UTC offsets), a list of critical services and a maintenance window; a card that states the
impact bands, the severity matrix and four steps applied in order (maintenance lowering, critical-service floor, timed
escalation, data-exposure override). Yes/no forms ask whether the incident reaches a level at the check time; the
choice form asks for its severity. Semantics: G0_SPEC.md (frozen sha below).

  solver A   matrix + arithmetic counter: band by threshold comparisons, a dict lookup in the matrix, the steps in
             order, escalation steps = floor(min(check, ack - 1) / T) on minute differences of aware datetimes
                                                                                         paradigm matrix_counter
  solver B   solver_b.py: its own parser of the RENDERED row (the matrix and bands are read from the printed card);
             escalation by a minute-by-minute simulation of the clock from opening to the check time, on epoch minutes
             from brute.epoch_minutes                                                     paradigm simulator
  construct  _sev_c(): a third reading (a step loop over the planned values) that predicts twins; a guard refuses any
             spec where it and solver A disagree, and any spec outside the R2 domain
  packs      one pack per card (G0 R21): team and reporter names; training samplers draw from the training packs, S5
             from the held-out packs. After A38 the packs come from haiku_author.py (pool "packs"); STANDIN_PACKS serve
             the tests only
  samplers   S1 forward; S2 label-first boundaries (users at a threshold, acknowledgement exactly at a step); S3 record
             as a table; S4 on-call narrative with times in two offsets; S5 held out (JSON-like export, held-out skins)
  questions  yn_reaches and yn_double_neg (positive); complements yn_below (option framing), yn_not_reaches
             (syntactic), yn_fails (implicit); ch_sev (SEV1-SEV4)

Fix iteration 1 (pilot verdict; every change is a generator or template change, no gate is loosened, no label moves):
  F1 / F2  the base plan is stratified (slot_of / strat: choice vs yes/no, outcome, level, question form, twin request),
           and a twin is planned from its own key: the sampler draws structure until solver A's gold agrees with the
           plan AND, when this base is asked for a twin, a single-slot edit with the planned outcome exists (label-first;
           nothing is relabelled). The edit list is wider (USERS, URGENCY, EXPOSED, CHECK, ACK) so a base that reaches the
           level can be flipped too; choice twins go to a level drawn uniformly over the three others.
  F3       choice bases 55% of seed slots; the yes/no share of ROWS is measured by the pilot (G10).
  F4       the card is a cards.CardSpec (G0 v3 section 1.1): terse text, two styles (full, short on 15%), Step 1 only
           when a window is declared, the times sentence only on two-offset rows, the "reaches" sentence only on yes/no
           rows; yes/no rows carry it in row.card (printed once), choice rows in the instructions.
  F5       yn_double_neg (two syntactic negations, polarity +1): Haiku wordings when the pool has clean ones, else four
           program-written wordings (polarity-checked) used as program text; its complement partner is yn_not_reaches.
  F6       Mode F notes that name the REPORTER only as author / adder / forwarder are quarantined (roles.py,
           quarantine.py); POLARITY_CHECK screens every yes/no wording (c2_kit.polarity).
Every row is dev-only (transfer dev, never trained). Code only: nothing here writes a file (A37 f).
"""
from __future__ import annotations

import datetime as dt
import random
import re
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import cards as CARDS  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.distractors import build_closed, error_model, register_name, uhash  # noqa: E402
from c2_kit.plugin import C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec, choose_forms  # noqa: E402
from c2_kit.rows import TextBuilder, assemble_row  # noqa: E402
from transfer.T20 import quarantine as QR  # noqa: E402
from transfer.T20 import roles as ROLES  # noqa: E402

HERE = Path(__file__).resolve().parent
FAMILY = "T20"
MAX_TRIES = 600
POS_FORM, DOUBLE_NEG_FORM, CHOICE_FORM = "yn_reaches", "yn_double_neg", "ch_sev"
NEG_FORMS = ("yn_below", "yn_not_reaches", "yn_fails")
POS_FORMS = (POS_FORM, DOUBLE_NEG_FORM)
P_COMPLEMENT, P_EQUIV, P_INV = 0.50, 0.12, 0.08
W_SLOTS, N_CHOICE_SLOTS = 20, 11   # F3: 11 of every 20 seeds are choice bases (yes/no about 52% of the ROWS)
YN_Q = ((POS_FORM,) * 10 + (DOUBLE_NEG_FORM,) + ("yn_below",) * 3 + ("yn_not_reaches",) * 3 + ("yn_fails",) * 3)
TWIN_PER, TWIN_OF = 2, 5           # twins: 2 of every 5 bases of a class (twin share about 22% of rows)
CARD_SHARES = {"full": 0.85, "short": 0.15}   # G0 v3 1.1: a short card on 15% of rows (spec 3.0)
UNIT_MIN = ("minute", "minutes")
UNIT_USER = ("user", "users")
SEV = {"sev1": ["SEV1"], "sev2": ["SEV2"], "sev3": ["SEV3"], "sev4": ["SEV4"]}
SEV_KEYS = ("sev1", "sev2", "sev3", "sev4")
URGENCY = {"outage": ["outage"], "degraded": ["degraded"], "cosmetic": ["cosmetic"]}
URG_KEYS = ("outage", "degraded", "cosmetic")
YESNO = {"yes": ["yes"], "no": ["no"]}
SERVICES = {"payments": ["payments"], "login": ["login"], "search": ["search"], "checkout": ["checkout"],
            "reports": ["reports"], "email": ["email"], "storage": ["storage"], "chat": ["chat"]}
SERVICE_KEYS = tuple(sorted(SERVICES))
BANDS = ("wide", "partial", "minimal")
MATRICES = (   # rows wide / partial / minimal, columns outage / degraded / cosmetic (1 = SEV1); each monotone (G0 R4)
    ((1, 2, 3), (2, 3, 4), (3, 4, 4)),
    ((1, 1, 3), (2, 3, 4), (3, 4, 4)),
    ((1, 2, 4), (2, 2, 4), (3, 3, 4)),
    ((1, 2, 3), (1, 3, 4), (2, 3, 4)),
)
THRESHOLDS = ((50, 500), (100, 1000), (200, 2000), (25, 250))
STEP_MINUTES = (15, 20, 30, 45, 60)
OFFSETS = (0, 60, 120, -300, 330, 540, -180)
TEAMS = ("Platform on-call", "Atlas crew", "Identity team", "Ledger guild", "Messaging group", "Harbor squad")
REPORTERS = ("Dana Okafor", "Lena Whitcombe", "Ravi Anand", "Mira Castell", "Tomas Ferreira", "Aiko Brandt",
             "Jonas Feld", "Nadia Kowal")
CLOSED_WORLD = ("The incident record, the critical list, the maintenance window and these rules are complete: "
                "nothing else changes the answer.")
# F5: program-written double-negation wordings, used as PROGRAM text (not lexicon forms) while the pool holds no clean
# Haiku one. Each: outer frame "Is it not the case / true that", exactly two "not" (the second negates "reach"), no
# contraction, no other negative word, "at / as of the check time". T20Plugin.__init__ refuses any that breaks
# c2_kit.polarity (P1-P4, strict frames) or negcount's profile (k_all = k_syn = 2).
PROGRAM_DN_WORDINGS = (
    "Is it not the case that incident {INC_ID} does not reach {LEVEL} at the check time?",
    "At the check time, is it not true that incident {INC_ID} does not reach {LEVEL}?",
    "Under these rules, is it not the case that incident {INC_ID} does not reach {LEVEL} as of the check time?",
    "Is it not true that, as of the check time, incident {INC_ID} does not reach {LEVEL}?",
)
# F6 / polarity: the family's negative predicates (a wording that says "falls short of", "stays below" ... is a
# negation the lexicon of negcount does not list; c2_kit.polarity P1 / P2)
NEGATIVE_PREDICATES = (
    r"fall(?:s|ing)? short(?: of)?", r"(?:stay|stays|staying|remain|remains|remaining)(?: \w+)? below",
    r"miss(?:es|ed)?", r"(?:is|are) below", r"stop(?:s)? short", r"come(?:s)? up short",
    r"(?:is|are) less severe than",
)
MATRIX_SLOTS = tuple(f"MX_{r}_{c}" for r in "WPM" for c in "ODC")
SCENARIOS = ("plain", "escalation", "maintenance", "floor", "both", "exposure", "deep")
SCENARIO_WEIGHTS = (0.22, 0.28, 0.14, 0.12, 0.08, 0.09, 0.07)
FORCED_REACH = ("floor", "both", "exposure")   # scenarios whose answer reaches SEV2 and SEV3 whatever the numbers are
FEASIBLE = {"plain": SEV_KEYS, "escalation": SEV_KEYS[:3], "maintenance": SEV_KEYS[1:], "floor": SEV_KEYS[:2],
            "both": SEV_KEYS[1:2], "exposure": SEV_KEYS[:1], "deep": SEV_KEYS[:3]}
N_CARDS = 12                       # cards per sampler (one pack each)
TRAIN_SAMPLERS = ("S1", "S2", "S3", "S4")


# ------------------------------------------------------------------------------------------------ the card (G0 v3 1.1)

def _has_window(spec) -> bool:
    return "MW_START" in spec.slots


_STEPS_W = ("Then, in order:\n"
            "1. If opened inside the maintenance window (start included, end excluded): one level less severe, never "
            "less severe than SEV4. The window has no other effect.\n"
            "2. If the service is on the critical list and less severe than SEV2: SEV2.\n"
            "3. A step falls due at each full {STEP} after opening. Each step due at or before the check time: one "
            "level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\n"
            "4. If customer data was exposed: SEV1.")
_STEPS_N = ("Then, in order:\n"
            "1. If the service is on the critical list and less severe than SEV2: SEV2.\n"
            "2. A step falls due at each full {STEP} after opening. Each step due at or before the check time: one "
            "level more severe, never more severe than SEV1, unless acknowledged at or before that step's time.\n"
            "3. If customer data was exposed: SEV1.")
_STEPS_W_SHORT = ("In order:\n"
                  "1. If opened inside the maintenance window (start included, end excluded): one level less "
                  "severe, never less severe than SEV4; no other effect.\n"
                  "2. If the service is on the critical list and less severe than SEV2: SEV2.\n"
                  "3. A step falls due at each full {STEP} after opening; each step due at or before the check "
                  "time: one level more severe, never more severe than SEV1, unless acknowledged at or before that "
                  "step's time.\n"
                  "4. If customer data was exposed: SEV1.")
_STEPS_N_SHORT = ("In order:\n"
                  "1. If the service is on the critical list and less severe than SEV2: SEV2.\n"
                  "2. A step falls due at each full {STEP} after opening; each step due at or before the check "
                  "time: one level more severe, never more severe than SEV1, unless acknowledged at or before that "
                  "step's time.\n"
                  "3. If customer data was exposed: SEV1.")
CARD = CARDS.CardSpec(
    FAMILY,
    (CARDS.CardItem("impact",
                    "Impact: wide if {U2} or more users, partial if {U1} or more but fewer than {U2}, otherwise "
                    "minimal."),
     CARDS.CardItem("base",
                    "Base severity (outage, degraded, cosmetic): wide {MX_W_O}, {MX_W_D}, {MX_W_C}; partial "
                    "{MX_P_O}, {MX_P_D}, {MX_P_C}; minimal {MX_M_O}, {MX_M_D}, {MX_M_C}."),
     CARDS.CardItem("steps_window", _STEPS_W, short=_STEPS_W_SHORT, when=_has_window),
     CARDS.CardItem("steps_no_window", _STEPS_N, short=_STEPS_N_SHORT, when=lambda s: not _has_window(s)),
     CARDS.CardItem("times", "Times are whole minutes at fixed UTC offsets, compared as points in time.",
                    short="Times are whole minutes at fixed UTC offsets, compared as points in time.",
                    when=lambda s: not s.structure["printed"]),
     CARDS.CardItem("reaches", "An incident reaches a level when its severity is that level or more severe.",
                    short="An incident reaches a level when its severity is that level or more severe.",
                    when=lambda s: s.qform != CHOICE_FORM)),
    heads={"full": "SEV1 is the most severe, SEV4 the least.", "short": "SEV1 most severe, SEV4 least."},
    tail=CLOSED_WORLD, numbered=False)
RECORD = ("Incident {INC_ID} on {SERVICE}:\n- opened: {OPEN}\n- users affected: {USERS}\n- urgency reported: {URGENCY}"
          "\n- customer data exposed: {EXPOSED}\n- acknowledged: @ACK@\n- check time: {CHECK}@MINUTES@\n"
          "Critical services: @CRIT@\nMaintenance window: @MW@")


def card_template(spec: Spec, style: str | None = None) -> str:
    """The card of a row (a {SLOT} template): its style (structure["card"]), the items that apply to the record (each
    item's `when` reads the record and the question type, never the gold), one item per line, the closed-world sentence
    last. No bullets and no indent (every token counts: C2_DATA_SPEC 3.0 length)."""
    style = style or spec.structure["card"]
    items = [it.text(style) for it in CARD.items if it.when is None or it.when(spec)]
    return "\n".join([CARD.heads[style]] + items + [CARD.tail])


# ------------------------------------------------------------------------------------------------ packs (G0 R21)

@dataclass(frozen=True)
class Pack:
    """One invented on-call organisation (G0_SPEC.md R21): the team and reporter names its cards use. After A38 the
    packs come from T20's Haiku pack task (haiku_author.py, pool "packs") and must pass check_pack(); until the frozen
    pool exists, STANDIN_PACKS serve the tests only."""
    key: str
    teams: tuple                 # 3 distinct team names
    reporters: tuple             # 4 distinct reporter names (first and last name)
    held_out: bool = False       # sampler S5 only


STANDIN_PACKS = tuple(
    Pack(f"t20-standin-{i:02d}", (TEAMS[i % 6], TEAMS[(i + 2) % 6], TEAMS[(i + 4) % 6]),
         tuple(REPORTERS[(i + k) % 8] for k in (0, 2, 4, 6)), held_out=i >= 6) for i in range(8))
TEAM_RE = re.compile(r"[A-Z][a-z]+(?:[ -][A-Za-z][a-z]+){1,2}")
PERSON_RE = re.compile(r"[A-Z][a-z]+ [A-Z][a-z]+")
PACK_BANNED = frozenset(SERVICE_KEYS) | {"incident", "incidents", "maintenance", "window", "alert", "alerts",
                                         "outage", "degraded", "cosmetic", "level", "priority", "data", "users"}


def check_pack(pack: Pack, label_words: tuple = ()) -> list:
    """Problems with one pack (G0 R21): name formats, distinct values, banned words, kit value lint."""
    from c2_kit import gsl
    probs = []
    if len(pack.teams) != 3 or len(set(pack.teams)) != 3:
        probs.append("three distinct team names")
    if len(pack.reporters) != 4 or len(set(pack.reporters)) != 4:
        probs.append("four distinct reporter names")
    for x in pack.teams:
        if not (isinstance(x, str) and TEAM_RE.fullmatch(x) and len(x) <= 32):
            probs.append(f"team {x!r}: 2-3 ASCII words, the first capitalised (hyphen or space between)")
    for x in pack.reporters:
        if not (isinstance(x, str) and PERSON_RE.fullmatch(x)):
            probs.append(f"reporter {x!r}: first and last name, two capitalised ASCII words")
    if probs:
        return probs
    vals = [*pack.teams, *pack.reporters]
    if any(a != b and a in b for a in vals for b in vals):
        probs.append("one name occurs inside another")
    words = {w for v in vals for w in re.split(r"[^a-z]+", v.lower()) if w}
    labels = gsl._label_forms(tuple(label_words))
    core = set().union(*gsl.CORE.values())
    hit = sorted(w for w in words if w in labels or w in PACK_BANNED or w in core)
    if hit:
        probs.append(f"banned words {hit}")
    if not probs:
        slots = {f"N{i}": S.name_slot(v) for i, v in enumerate(vals)}
        probs += [f"G-SL value lint: {v.rule} {v.detail}" for v in gsl.lint_values(slots)]
    return probs


def pack_for(packs: tuple, sampler: str, card: int) -> Pack:
    """One pack per card (G0 R21): S1-S4 draw from the training packs, S5 from the held-out packs; card ordinal =
    sampler index x N_CARDS + card, taken modulo the pool size."""
    pool = [p for p in packs if p.held_out == (sampler == "S5")]
    if not pool:
        raise ContractError(f"no {'held-out' if sampler == 'S5' else 'training'} pack")
    i = (0 if sampler == "S5" else TRAIN_SAMPLERS.index(sampler) * N_CARDS) + card
    return pool[i % len(pool)]


def in_domain(env: dict, critical: tuple) -> bool:
    """G0 R2: opened < check; opened < ack <= check; start < end; users >= 0; two distinct critical services."""
    ok = env["OPEN"] < env["CHECK"] and env["USERS"] >= 0 and len({env[n] for n in critical}) == 2
    if "ACK" in env:
        ok = ok and env["OPEN"] < env["ACK"] <= env["CHECK"]
    if "MW_START" in env:
        ok = ok and env["MW_START"] < env["MW_END"]
    return ok


def weighted(x: float, names) -> str:
    """The scenario at quantile x of SCENARIO_WEIGHTS restricted to `names` (label-blind)."""
    ws = [SCENARIO_WEIGHTS[SCENARIOS.index(n)] for n in names]
    acc, tot = 0.0, sum(ws)
    for n, w in zip(names, ws):
        acc += w / tot
        if x < acc:
            return n
    return names[-1]

for _n, _t in (("t20_band_exclusive", "reads 'X or more' as 'more than X' for the impact bands"),
               ("t20_skip_maintenance", "skips the maintenance-window lowering"),
               ("t20_skip_floor", "skips the critical-service floor"),
               ("t20_skip_escalation", "skips the timed escalation"),
               ("t20_skip_exposure", "skips the data-exposure override"),
               ("t20_ignore_ack", "keeps escalating after the acknowledgement"),
               ("t20_ack_boundary", "lets a step happen when the acknowledgement is exactly at its time"),
               ("t20_floor_first", "applies the critical floor before the maintenance lowering"),
               ("t20_window_end_inclusive", "counts an incident opened exactly at the window's end as inside it")):
    register_name(_n, _t)


# ------------------------------------------------------------------------------------------------ the plan (F1-F3)

def strat(sampler: str, name: str, idx: int, n: int) -> int:
    """A value of range(n) for the idx-th item of a stream, each value exactly once in every block of n consecutive
    indices (a seeded permutation per block). Label-blind: it reads the sampler, the stream name and the index only.
    Stratifying keeps the realised shares of a ~1,000-row pilot on their plan (an independent draw of each outcome
    moves the yes rate by qform, the choice golds and G6's metadata view by their sampling noise)."""
    blk, pos = divmod(idx, n)
    order = sorted(range(n), key=lambda v: uhash(FAMILY, "strat", name, sampler, blk, v))
    return order[pos]


def slot_of(sampler: str, seed: int) -> tuple:
    """(kind, index): whether this seed's base is a choice or a yes/no base, and its index among that kind in the
    sampler's seed order. Each block of W_SLOTS seeds holds exactly N_CHOICE_SLOTS choice bases, at seeded places."""
    blk, pos = divmod(seed, W_SLOTS)
    order = sorted(range(W_SLOTS), key=lambda i: uhash(FAMILY, "slot", sampler, blk, i))
    choice = frozenset(order[:N_CHOICE_SLOTS])
    mine = pos in choice
    before = sum(1 for i in range(pos) if (i in choice) == mine)
    per = N_CHOICE_SLOTS if mine else W_SLOTS - N_CHOICE_SLOTS
    return ("choice" if mine else "yesno"), blk * per + before


def yn_stream(sampler: str, y: int) -> tuple:
    """(question-form slot, occurrence index of that slot) of the y-th yes/no base: every block of 20 holds the shares
    of YN_Q exactly, so each form's outcomes can be stratified inside the form."""
    blk, pos = divmod(y, len(YN_Q))
    order = sorted(range(len(YN_Q)), key=lambda v: uhash(FAMILY, "strat", "yn_q", sampler, blk, v))
    cls = [YN_Q[v] for v in order]
    return cls[pos], blk * YN_Q.count(cls[pos]) + cls[:pos].count(cls[pos])


def _twin_slot(sampler: str, cls: str, occ: int) -> tuple:
    """(requested, k): the occ-th base of a class asks for a twin in exactly TWIN_PER of every TWIN_OF; k indexes the
    requested ones densely (for the choice twins' level draw)."""
    blk = occ // TWIN_OF
    v = strat(sampler, f"twin|{cls}", occ, TWIN_OF)
    return v < TWIN_PER, blk * TWIN_PER + v


@dataclass(frozen=True)
class Plan:
    """Everything drawn before any structure: the base's kind, outcome and relation requests (label-blind: the seed's
    place in its sampler's stream; the label-first outcome is the plan itself)."""
    kind: str                # choice | yesno
    qform: str
    scenario: str
    target: object           # choice: the gold level key; yes/no: reaches (bool)
    level: str | None        # yes/no: the asked level key (sev2 / sev3)
    card: str                # full | short (qform-independent: a complement partner prints the same card)
    twin: bool               # this base gets a minimal-edit twin
    twin_to: str | None      # choice twin: the level key the twin must reach (uniform over the three others)


@lru_cache(maxsize=None)
def plan_of(sampler: str, seed: int) -> Plan:
    u = lambda *k: uhash(FAMILY, sampler, seed, *k)                    # noqa: E731
    kind, idx = slot_of(sampler, seed)
    card = CARDS.draw_style(f"{FAMILY}|{sampler}|{seed}", CARD_SHARES)
    if kind == "choice":                                  # the gold level first (stratified), then a scenario that
        target = SEV_KEYS[strat(sampler, "ch_sev", idx, 4)]           # can produce it
        fits = [s for s in SCENARIOS if target in FEASIBLE[s]]
        req, k = _twin_slot(sampler, f"ch|{target}", idx // 4)
        others = [lv for lv in SEV_KEYS if lv != target]
        twin_to = others[strat(sampler, f"twin_to|{target}", k, 3)] if req else None
        return Plan("choice", CHOICE_FORM, weighted(u("scenario"), fits), target, None, card, req, twin_to)
    q0, j = yn_stream(sampler, idx)
    reaches = strat(sampler, f"yn_reach|{q0}", j, 2) == 0
    level = ("sev2", "sev3")[strat(sampler, f"yn_lvl|{q0}|{int(reaches)}", j // 2, 2)]
    # exposure, floor and both always reach SEV2 and SEV3, so a draw that must NOT reach picks among the other four at
    # their weights (renormalized). The pilot rule moved these draws to "maintenance": 43% of the non-reaching rows had
    # a window and the window predicted the label (P(reach | window inside) 0.28 against 0.55), which G6's metadata
    # views read through the record length and the card length.
    scenario = weighted(u("scenario"), SCENARIOS if reaches else [x for x in SCENARIOS if x not in FORCED_REACH])
    req, _k = _twin_slot(sampler, f"yn|{q0}|{int(reaches)}", j // 2)
    return Plan("yesno", q0, scenario, reaches, level, card, req, None)


# ------------------------------------------------------------------------------------------------ solver A

def minutes(a: dt.datetime, b: dt.datetime) -> int:
    return int((b - a).total_seconds() // 60)


def band(spec: Spec, mistakes=frozenset()) -> str:
    env = spec.env()
    u = env["USERS"]
    if "t20_band_exclusive" in mistakes:
        return "wide" if u > env["U2"] else ("partial" if u > env["U1"] else "minimal")
    return "wide" if u >= env["U2"] else ("partial" if u >= env["U1"] else "minimal")


def base_level(spec: Spec, mistakes=frozenset()) -> int:
    env = spec.env()
    cell = {"wide": "W", "partial": "P", "minimal": "M"}[band(spec, mistakes)] + "_" + \
        {"outage": "O", "degraded": "D", "cosmetic": "C"}[env["URGENCY"]]
    return int(env[f"MX_{cell}"][-1])


def escalation_steps(spec: Spec, mistakes=frozenset()) -> int:
    env = spec.env()
    step = env["STEP"]
    check = minutes(env["OPEN"], env["CHECK"])
    if "ACK" not in env or "t20_ignore_ack" in mistakes:
        return max(0, check // step)
    ack = minutes(env["OPEN"], env["ACK"])
    limit = ack if "t20_ack_boundary" in mistakes else ack - 1
    return max(0, min(check, limit) // step)


def in_window(spec: Spec, mistakes=frozenset()) -> bool:
    env = spec.env()
    if "MW_START" not in env:
        return False
    if "t20_window_end_inclusive" in mistakes:
        return env["MW_START"] <= env["OPEN"] <= env["MW_END"]
    return env["MW_START"] <= env["OPEN"] < env["MW_END"]


def severity(spec: Spec, mistakes=frozenset()) -> int:
    """Solver A: 1 (SEV1) .. 4 (SEV4)."""
    env = spec.env()
    lvl = base_level(spec, mistakes)
    critical = env["SERVICE"] in {env[n] for n in spec.structure["critical"]}

    def lower(x):
        return min(4, x + 1) if in_window(spec, mistakes) and "t20_skip_maintenance" not in mistakes else x

    def floor(x):
        return min(x, 2) if critical and "t20_skip_floor" not in mistakes else x

    lvl = lower(floor(lvl)) if "t20_floor_first" in mistakes else floor(lower(lvl))
    if "t20_skip_escalation" not in mistakes:
        lvl = max(1, lvl - escalation_steps(spec, mistakes))
    if env["EXPOSED"] == "yes" and "t20_skip_exposure" not in mistakes:
        lvl = 1
    return lvl


def answer_for(qform: str, reaches: bool):
    if qform in POS_FORMS:
        return int(reaches)
    if qform in NEG_FORMS:
        return int(not reaches)
    raise ContractError(f"{qform} is not a yes/no form")


def _sev_c(spec: Spec) -> int:
    """Construction reading: the planned values through a plain step loop (no floor division)."""
    env, p = spec.env(), spec.structure["plan"]
    users = env["USERS"]
    row = "W" if users >= env["U2"] else ("P" if users >= env["U1"] else "M")
    col = {"outage": "O", "degraded": "D", "cosmetic": "C"}[env["URGENCY"]]
    lvl = SEV_KEYS.index(env[f"MX_{row}_{col}"]) + 1
    if p["window"]:
        lvl = min(4, lvl + 1)
    if p["critical"] and lvl > 2:
        lvl = 2
    open_, check, ack = env["OPEN"], env["CHECK"], env.get("ACK")
    j = 1
    while open_ + dt.timedelta(minutes=j * env["STEP"]) <= check:
        due = open_ + dt.timedelta(minutes=j * env["STEP"])
        if ack is None or ack > due:
            lvl = max(1, lvl - 1)
        j += 1
    return 1 if env["EXPOSED"] == "yes" else lvl


# ------------------------------------------------------------------------------------------------ twin edits (F1, F2)

def twin_edits(spec: Spec) -> list:
    """Every single-slot edit a minimal-edit twin may make, as (slot name, new Slot), in a fixed order:
    USERS across a band threshold (U1 - 1, U1, U2 - 1, U2), URGENCY to each other value, EXPOSED flipped, CHECK moved
    onto a step's due time or one minute before it, ACK moved onto a step's due time or one minute after it. A premise
    is never added or removed (the record's lines would change), the window and the critical list never move, and the
    plan flags stay as drawn, so _sev_c() stays the construction reading."""
    env = spec.env()
    out = []
    for u in sorted({env["U1"] - 1, env["U1"], env["U2"] - 1, env["U2"]}):
        if u >= 0 and u != env["USERS"]:
            out.append(("USERS", S.count_slot(u, UNIT_USER)))
    for v in URG_KEYS:
        if v != env["URGENCY"]:
            out.append(("URGENCY", S.category_slot(v, URGENCY)))
    out.append(("EXPOSED", S.category_slot("no" if env["EXPOSED"] == "yes" else "yes", YESNO)))
    open_, step, tz = env["OPEN"], env["STEP"], env["CHECK"].tzinfo
    chk = minutes(open_, env["CHECK"])
    ack = minutes(open_, env["ACK"]) if "ACK" in env else None
    at = lambda m: (open_ + dt.timedelta(minutes=m)).astimezone(tz)      # noqa: E731
    for j in range(1, chk // step + 3):
        for m in (j * step, j * step - 1):
            if m >= 1 and m != chk and (ack is None or m >= ack):
                out.append(("CHECK", S.datetime_slot(at(m))))
    if ack is not None:
        atz = env["ACK"].tzinfo
        for j in range(1, chk // step + 2):
            for m in (j * step, j * step + 1):
                if 1 <= m <= chk and m != ack:
                    out.append(("ACK", S.datetime_slot((open_ + dt.timedelta(minutes=m)).astimezone(atz))))
    return out


def twin_choice(spec: Spec, want: int | None = None):
    """The twin edit of a base (slot, new Slot, the twin's level) or None. Yes/no (spec.qform asks a level): the edits
    that flip the answer; choice: the edits whose twin is at level `want` (None: any edit that changes the level). One
    edit KIND is drawn uniformly among the kinds that qualify, then one edit of it (a seeded hash of the seed alone)."""
    env = spec.env()
    base = _sev_c(spec)
    yes_no = spec.qform != CHOICE_FORM
    lvl = int(env["LEVEL"][-1]) if yes_no else None
    crit = tuple(spec.structure["critical"])
    cands = []
    for slot, new in twin_edits(spec):
        twin = spec.with_slot(slot, new)
        if not in_domain(twin.env(), crit):
            continue
        sev2 = _sev_c(twin)
        if yes_no:
            ok = (sev2 <= lvl) != (base <= lvl)
        else:
            ok = sev2 == want if want is not None else sev2 != base
        if ok:
            cands.append((slot, new, sev2))
    if not cands:
        return None
    kinds = sorted({c[0] for c in cands})
    kind = kinds[min(len(kinds) - 1, int(uhash(FAMILY, "twin_kind", spec.sampler, spec.seed) * len(kinds)))]
    mine = [c for c in cands if c[0] == kind]
    return min(mine, key=lambda c: uhash(FAMILY, "twin_pick", spec.sampler, spec.seed, c[0], str(c[1].value)))


# ------------------------------------------------------------------------------------------------ the plugin

class T20Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "transfer_dev"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "4a05dc337b0941c328738018ff91a678b7633f5eeee9de385309d6b664022066"   # frozen G0_SPEC.md v3 (fix iteration 1)
    G0_HAIKU_TASK = "c2-data-stage-a/amb:T20"     # the one Haiku ambiguity pass (31 points; G0 section 8)
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "matrix_counter"
    PARADIGM_B = "simulator"
    SOLVER_B_MODULE = "transfer.T20.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm(POS_FORM, "noul", "reaches_level", 1, yes_is_bad=True),
        QuestionForm(DOUBLE_NEG_FORM, "noul", "reaches_level", 1, yes_is_bad=True),
        QuestionForm("yn_below", "noul", "reaches_level", -1, "option_framing", yes_is_bad=False),
        QuestionForm("yn_not_reaches", "noul", "reaches_level", -1, "syntactic", yes_is_bad=False),
        QuestionForm("yn_fails", "noul", "reaches_level", -1, "implicit", yes_is_bad=False),
        QuestionForm(CHOICE_FORM, "choice", answer_set="closed"),
    )}
    LABEL_WORDS = ("severe", "severity", "escalated", "escalate", "critical", "urgent", "minor", "major", "page",
                   "paged", "reaches", "sev")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("pager_alert", "oncall_chat", "status_page", "incident_ticket", "postmortem_draft",
                 "incident_email", "runbook_note", "handoff_log", "customer_report", "exec_summary")
    HELD_OUT_REGISTERS = ("customer_report", "exec_summary")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW = ()
    POLARITY_CHECK = True                 # c2_kit.polarity: yes/no wordings must read with their form's polarity
    POLARITY_NEGATIVES = NEGATIVE_PREDICATES
    POLARITY_STRICT_FRAMES = True         # also refuse "Does incident X not reach ...?" (aux + subject + not)

    def __init__(self, lexicon=None, packs=None):
        super().__init__(lexicon)
        self.packs = tuple(packs) if packs else STANDIN_PACKS
        bad = [(t, p) for t in PROGRAM_DN_WORDINGS for p in self._program_dn_problems(t)]
        if bad:
            raise ContractError(f"program double-negation wording refused: {bad[:2]}")
        self._screened: list = []                  # [(ctx, screened ctx, {skin id: why})]

    @staticmethod
    def _program_dn_problems(text: str) -> list:
        import negcount
        c = negcount.count(K.PH_RE.sub("X", text))
        probs = []
        if (c.k_all, c.k_syn) != (2, 2):
            probs.append(f"negation counts {(c.k_all, c.k_syn)} != (2, 2)")
        if sorted(x.name for x in K.placeholders(text)) != ["INC_ID", "LEVEL"]:
            probs.append("placeholders are INC_ID and LEVEL once each")
        if not re.search(r"\b(?:at|as of) the check time\b", text, re.I):
            probs.append("the check time is not named")
        probs += POL.problems(text, 1, negatives=NEGATIVE_PREDICATES, strict_frames=True)
        return probs

    # ------------------------------------------------------------------------------------------- the pool context
    def ctx_for(self, spec, ctx):
        """The kit context without the wordings that break the polarity rule (c2_kit.polarity), the pool templates
        quarantined on gate evidence (quarantine.py) and the Mode F notes that do not name the REPORTER as the reporter
        (roles.py), so neither render() nor the pipeline's partners can pick one. Cached per context object."""
        for c, screened, _bad in self._screened:
            if c is ctx:
                return screened
        screened, bad = POL.screen(ctx, self)
        bad = dict(bad)
        keep = {}
        for sid, sk in screened.skins.items():
            why = QR.QUARANTINE.get(sid)
            if why is not None:
                bad[sid] = [why]
                continue
            if sk.kind == "skin" and sk.author_mode == "F":
                probs = ROLES.reporter_problems(sk.text, dict(sk.brief).get("REPORTER", ""))
                if probs:
                    bad[sid] = probs
                    continue
            keep[sid] = sk
        screened = KitCtx(skins=keep, lexicon=ctx.lexicon)
        self._screened.append((ctx, screened, bad))
        return screened

    def quarantined(self, ctx) -> dict:
        """{skin id: problems} for the templates ctx_for() leaves out of `ctx`."""
        self.ctx_for(None, ctx)
        return next(bad for c, _s, bad in self._screened if c is ctx)

    # ------------------------------------------------------------------------------------------- sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        plan = plan_of(sampler, seed)
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        for i in range(MAX_TRIES):
            scen = plan.scenario if i < MAX_TRIES // 2 else "plain"     # plain reaches every target
            spec = self._draw(rng, seed, sampler, plan, scen)
            if spec is None:
                continue
            if plan.twin and twin_choice(spec, self._twin_want(spec, plan)) is None:
                continue                                  # label-first twin: this structure cannot make the planned twin
            return spec
        raise ContractError(f"T20 {sampler} seed {seed}: no spec reached its plan")

    @staticmethod
    def _twin_want(spec: Spec, plan: Plan):
        return int(plan.twin_to[-1]) if (plan.twin_to is not None and spec.qform == CHOICE_FORM) else None

    def _draw(self, rng, seed, sampler, plan: Plan, scenario):
        qform, target, level = plan.qform, plan.target, plan.level
        card = int(uhash(FAMILY, "card", seed) * N_CARDS)
        pack = pack_for(self.packs, sampler, card)
        mx = rng.choice(MATRICES)
        u1, u2 = rng.choice(THRESHOLDS)
        step = rng.choice(STEP_MINUTES)
        urg = rng.choice(URG_KEYS)
        b = rng.choice(BANDS)
        if sampler == "S2" and rng.random() < 0.6:
            users = rng.choice({"wide": (u2, u2 + 1), "partial": (u1, u2 - 1), "minimal": (u1 - 1, 0)}[b])
        else:
            users = {"wide": rng.randint(u2, u2 * 3), "partial": rng.randint(u1, u2 - 1),
                     "minimal": rng.randint(0, u1 - 1)}[b]
        service = rng.choice(SERVICE_KEYS)
        crit = rng.sample([s for s in SERVICE_KEYS if s != service], 2)
        critical = scenario in ("floor", "both") or (scenario == "deep" and rng.random() < 0.5)
        if critical:
            crit[rng.randrange(2)] = service
        window = scenario in ("maintenance", "both") or (scenario == "deep" and not critical)
        exposed = scenario == "exposure"
        off = dt.timezone(dt.timedelta(minutes=rng.choice(OFFSETS)))
        open_ = dt.datetime(2026, 1, 5, tzinfo=off) + dt.timedelta(minutes=rng.randrange(0, 300 * 24 * 60) // 5 * 5)
        escalate = scenario in ("escalation", "deep")
        n_steps = rng.choice((1, 1, 2, 3)) if escalate else 0
        if escalate:
            check_m = n_steps * step + rng.randint(0, step - 1)
            spare = max(1, check_m - n_steps * step + 1)
            ack_m = None if rng.random() < 0.5 else n_steps * step + rng.randint(1, spare)
            if ack_m is not None and ack_m > check_m:
                ack_m = None
            if sampler == "S2" and rng.random() < 0.5:
                ack_m = n_steps * step                     # acknowledged exactly at the last step's time
        else:
            check_m = rng.randint(5, step * 3)
            ack_m = rng.randint(1, min(step, check_m)) if check_m >= step or rng.random() < 0.5 else None
            if ack_m is None and check_m >= step:
                ack_m = rng.randint(1, step)
        check = open_ + dt.timedelta(minutes=check_m)
        ack = open_ + dt.timedelta(minutes=ack_m) if ack_m is not None else None
        two_offsets = sampler == "S4" or scenario == "deep"
        if two_offsets:
            off2 = dt.timezone(dt.timedelta(minutes=rng.choice([o for o in OFFSETS if o * 60 != off.utcoffset(None)
                                                                .total_seconds()])))
            check = check.astimezone(off2)
            ack = ack.astimezone(off2) if ack else None
        mw = None
        if window or rng.random() < 0.35:
            if window:
                start = open_ - dt.timedelta(minutes=rng.randint(0, 120) // 5 * 5)
                end = open_ + dt.timedelta(minutes=rng.randint(1, 180))
                if sampler == "S2" and rng.random() < 0.3:
                    start = open_
            else:
                if rng.random() < 0.5:
                    end = open_ - dt.timedelta(minutes=rng.choice((0, 0, 30, 90)))
                    start = end - dt.timedelta(minutes=rng.randint(30, 240))
                else:
                    start = open_ + dt.timedelta(minutes=rng.randint(1, 180))
                    end = start + dt.timedelta(minutes=rng.randint(30, 240))
            mw = (start, end)
        slots = {"INC_ID": S.id_slot(f"INC-{rng.randint(1000, 9999)}"), "SERVICE": S.category_slot(service, SERVICES),
                 "USERS": S.count_slot(users, UNIT_USER), "URGENCY": S.category_slot(urg, URGENCY),
                 "EXPOSED": S.category_slot("yes" if exposed else "no", YESNO), "OPEN": S.datetime_slot(open_),
                 "CHECK": S.datetime_slot(check), "STEP": S.count_slot(step, UNIT_MIN),
                 "U1": S.count_slot(u1), "U2": S.count_slot(u2),
                 "TEAM": S.name_slot(rng.choice(pack.teams)), "REPORTER": S.name_slot(rng.choice(pack.reporters))}
        if ack is not None:
            slots["ACK"] = S.datetime_slot(ack)
        for r, row in zip("WPM", mx):
            for c, v in zip("ODC", row):
                slots[f"MX_{r}_{c}"] = S.category_slot(f"sev{v}", SEV)
        for i, cs in enumerate(crit):
            slots[f"CRIT{i}"] = S.category_slot(cs, SERVICES)
        if mw:
            slots["MW_START"], slots["MW_END"] = S.datetime_slot(mw[0]), S.datetime_slot(mw[1])
        if qform != CHOICE_FORM:
            slots["LEVEL"] = S.category_slot(level, SEV)
            slots["LEVEL_NEXT"] = S.category_slot(SEV_KEYS[SEV_KEYS.index(level) + 1], SEV)
        layout = {"S3": "table", "S5": "export"}.get(sampler, "list")
        structure = {"critical": ["CRIT0", "CRIT1"], "layout": layout, "printed": not two_offsets,
                     "plan": {"window": bool(window and mw), "critical": critical}, "card": plan.card}
        card_id = f"{FAMILY}:{sampler}:c{card:02d}"
        spec = self.derive(Spec(FAMILY, sampler, seed, card_id, qform, slots, structure=structure, pack=pack.key))
        if not in_domain(spec.env(), tuple(structure["critical"])):
            return None
        sev = severity(spec)
        if sev != _sev_c(spec) or in_window(spec) != structure["plan"]["window"]:
            return None
        if qform == CHOICE_FORM:
            return spec if f"sev{sev}" == target else None
        return spec if (sev <= int(level[-1])) == target else None

    def derive(self, spec: Spec) -> Spec:
        """Printed intermediates (one-offset rows): minutes from opening to the check and to the acknowledgement."""
        env = {k: v.value for k, v in spec.slots.items()}
        derived, deps = {}, {}
        if spec.structure["printed"]:
            derived["M_CHECK"] = S.count_slot(minutes(env["OPEN"], env["CHECK"]))
            deps["M_CHECK"] = ("OPEN", "CHECK")
            if "ACK" in env:
                derived["M_ACK"] = S.count_slot(minutes(env["OPEN"], env["ACK"]))
                deps["M_ACK"] = ("OPEN", "ACK")
        s = spec.replace(derived=derived, derived_deps=deps)
        tags = []
        e = s.env()
        if e["USERS"] in (e["U1"], e["U2"]) or e["USERS"] + 1 in (e["U1"], e["U2"]):
            tags.append("band_boundary")
        if "ACK" in e and minutes(e["OPEN"], e["ACK"]) % e["STEP"] == 0:
            tags.append("ack_at_step")
        if "MW_START" in e and not in_window(s):
            tags.append("window_misses")
        if "MW_START" in e and e["OPEN"] == e["MW_START"]:
            tags.append("window_start")
        if severity(s, frozenset({"t20_floor_first"})) != severity(s):
            tags.append("order_matters")
        if not s.structure["printed"]:
            tags.append("two_offsets")
        steps = escalation_steps(s)
        active = int(in_window(s)) + int(e["SERVICE"] in {e[n] for n in s.structure["critical"]}) + \
            int(e["EXPOSED"] == "yes")
        ops = 1 + active + int(steps > 0) + int(not s.structure["printed"])
        return s.replace(tags=tuple(tags), depth=ops, deep=ops >= 4)

    # ------------------------------------------------------------------------------------------- solver A
    def solve_a(self, spec: Spec):
        sev = severity(spec)
        if spec.qform == CHOICE_FORM:
            return f"sev{sev}"
        return answer_for(spec.qform, sev <= int(spec.env()["LEVEL"][-1]))

    def canonical(self, spec: Spec) -> dict:
        e = spec.env()
        iso = lambda t: t.isoformat() if t is not None else None      # noqa: E731
        return {"incident": e["INC_ID"], "service": e["SERVICE"], "users": e["USERS"], "urgency": e["URGENCY"],
                "exposed": e["EXPOSED"], "open": iso(e["OPEN"]), "ack": iso(e.get("ACK")), "check": iso(e["CHECK"]),
                "m_check": e.get("M_CHECK"), "m_ack": e.get("M_ACK"), "step": e["STEP"], "u1": e["U1"], "u2": e["U2"],
                "matrix": [e[n] for n in MATRIX_SLOTS], "critical": [e[n] for n in spec.structure["critical"]],
                "window": [iso(e["MW_START"]), iso(e["MW_END"])] if "MW_START" in e else None,
                "asked": e.get("LEVEL_NEXT") if spec.qform == "yn_below" else e.get("LEVEL"), "team": e["TEAM"],
                "reporter": e["REPORTER"], "qform": spec.qform}

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        c = self.canonical(spec)
        return c if author_mode == "T" else {k: v for k, v in c.items() if k not in ("team", "reporter")}

    def extract_view(self, spec: Spec) -> dict:
        e = spec.env()
        return {"team": e["TEAM"], "reporter": e["REPORTER"]}

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        return [Field("team", "name", "the team handling the incident, as written"),
                Field("reporter", "name", "the person who reported it, as written")]

    # ------------------------------------------------------------------------------------------- render
    @staticmethod
    def row_key(spec: Spec) -> str:
        return f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"

    def record_template(self, spec: Spec) -> str:
        st = spec.structure
        ack = "{ACK}" if "ACK" in spec.slots else "not acknowledged"
        mins = ""
        if st["printed"]:
            mins = "\n- minutes from opening to the check: {M_CHECK}"
            if "ACK" in spec.slots:
                mins += "\n- minutes from opening to the acknowledgement: {M_ACK}"
        crit = "{CRIT0}, {CRIT1}"
        mw = "{MW_START} to {MW_END}" if "MW_START" in spec.slots else "none declared"
        tpl = RECORD.replace("@ACK@", ack).replace("@MINUTES@", mins).replace("@CRIT@", crit).replace("@MW@", mw)
        if st["layout"] == "table":
            lines = tpl.split("\n")
            head, rest = lines[0], [x for x in lines[1:] if x.startswith("- ")]
            tail = [x for x in lines[1:] if not x.startswith("- ")]
            tpl = "\n".join([head, "| field | value |", "|---|---|"] +
                            [f"| {x[2:].split(': ', 1)[0]} | {x[2:].split(': ', 1)[1]} |" for x in rest] + tail)
        elif st["layout"] == "export":
            tpl = "export incident:\n" + "\n".join("  " + x.lstrip("- ") for x in tpl.split("\n"))
        return tpl

    def _wording(self, spec: Spec, ctx, key: str):
        """(wording Skin or None, (program wording id, text) or None). A yes/no form picks an admitted Haiku wording; the
        double-negation form falls back to a program-written wording when the (screened) pool has none; the row then
        carries meta.program_wording (its wording_id stays None: it is program text, not a lexicon form)."""
        if spec.qform == DOUBLE_NEG_FORM:
            try:
                return ctx.pick(FAMILY, "wording", key, qform=spec.qform), None
            except LookupError:
                i = min(len(PROGRAM_DN_WORDINGS) - 1, int(uhash(FAMILY, "dn_wording", key) * len(PROGRAM_DN_WORDINGS)))
                return None, (f"T20-prog-dn-{i}", PROGRAM_DN_WORDINGS[i])
        return ctx.pick(FAMILY, "wording", key, qform=spec.qform), None

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        key = self.row_key(spec)
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        ctx = self.ctx_for(spec, ctx)                      # never pick a template the pool quarantines
        skin = skin or ctx.pick(FAMILY, "skin", key, held_out=held)
        program_q = None
        if wording is None:
            wording, program_q = self._wording(spec, ctx, key)
        if wording is not None and wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = dict(forms or choose_forms(spec, key))
        for k in ("U1", "U2", "STEP"):
            forms[k] = "digits"
        slots = spec.all_slots()
        tb = TextBuilder()
        tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id).add("state", "\n\n")
        tb.add("state", K.fill(self.record_template(spec), slots, forms))
        if attack is not None:
            tb.add("state", "\n\n").add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        # G0 v3 1.1: the served prompt prints row.card once, on yes/no rows only (their definitions block); a choice
        # row keeps the card at the head of its instructions (printed twice, but its only place). place_rules does both.
        placed = CARDS.place_rules(tb, K.fill(card_template(spec), slots, forms), self.QFORMS[spec.qform].qtype)
        if wording is not None:
            tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        else:
            tb.add("instructions", K.fill(program_q[1], slots, forms))
        ans = self.solve_a(spec)
        os_ = None
        if spec.qform == CHOICE_FORM:
            os_ = build_closed(spec, ans, list(SEV_KEYS), self.error_models(), row_key=key,
                               render_key=lambda k: SEV[k][0], order="fixed")
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, defs_style=CARDS.defs_style(placed, spec.structure["card"]),
                            extra_meta={"dev_only": True, **({"program_wording": program_q[0]} if program_q else {})})

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        out = []
        q = self.QFORMS[spec.qform]
        u = lambda *k: uhash(FAMILY, "rel", spec.sampler, spec.seed, *k)   # noqa: E731
        if q.qtype == "noul" and u("complement") < P_COMPLEMENT:
            if spec.qform == DOUBLE_NEG_FORM:
                partner = "yn_not_reaches"             # one negation cue fewer: an exact syntactic complement
            elif q.polarity == -1:
                partner = POS_FORM
            else:
                partner = NEG_FORMS[int(u("partner") * 3)]
            out.append(RelationProposal("complement", qform=partner))
        plan = plan_of(spec.sampler, spec.seed)
        if plan.twin:
            t = self._twin(spec, plan)
            if t is not None:
                out.append(t)
        x = u("extra")
        if x < P_EQUIV:
            new = {"list": "table", "table": "list", "export": "list"}[spec.structure["layout"]]
            out.append(RelationProposal("equiv", spec=spec.replace(structure={**spec.structure, "layout": new}),
                                        note=f"record as {new}"))
        elif x < P_EQUIV + P_INV:
            out.append(RelationProposal("inv"))
        return out + self._metamorphic(spec)

    def _twin(self, spec: Spec, plan: Plan):
        """The planned minimal-edit twin: one slot of twin_edits() changes, the prediction comes from _sev_c."""
        pick = twin_choice(spec, self._twin_want(spec, plan))
        if pick is None:
            return None
        slot, new, sev2 = pick
        twin = self.derive(spec.with_slot(slot, new))
        expect = (f"sev{sev2}" if spec.qform == CHOICE_FORM
                  else answer_for(spec.qform, sev2 <= int(spec.env()["LEVEL"][-1])))
        return RelationProposal("twin", spec=twin, changed_slot=slot, expect=expect)

    def _metamorphic(self, spec: Spec) -> list:
        env = spec.env()
        same = lambda s, note: RelationProposal("metamorphic", spec=s, expect="same", note=note)   # noqa: E731
        out = [same(spec.with_slot("TEAM", S.name_slot(next(t for t in TEAMS if t != env["TEAM"]))), "rename the team")]
        shift = dt.timedelta(days=7)
        moved = {k: S.datetime_slot(env[k] + shift) for k in ("OPEN", "CHECK", "ACK", "MW_START", "MW_END") if k in env}
        out.append(same(self.derive(spec.replace(slots={**spec.slots, **moved})), "shift every time by 7 days"))
        conv = {k: S.datetime_slot(env[k].astimezone(dt.timezone(dt.timedelta(hours=3)))) for k in ("CHECK", "ACK")
                if k in env}
        out.append(same(self.derive(spec.replace(slots={**spec.slots, **conv},
                                                 structure={**spec.structure, "printed": False})),
                        "write the check and acknowledgement times at another offset"))
        return out

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def mk(m):
            return lambda s: f"sev{severity(s, frozenset({m}))}" if s.qform == CHOICE_FORM else None
        return {name: error_model(name, mk(name)) for name in (
            "t20_band_exclusive", "t20_skip_maintenance", "t20_skip_floor", "t20_skip_escalation",
            "t20_skip_exposure", "t20_ignore_ack", "t20_ack_boundary", "t20_floor_first", "t20_window_end_inclusive")}
