"""families/T24/plugin.py: T24 "revision materiality: does the edit change this case's outcome?" (C2_DATA_SPEC 2.1,
3.12; PREREG_FINAL A37). Code only before A38: nothing here writes a file.

A row shows two versions of one invented everyday policy (an original and a revised version that differ by ONE typed
edit plus 0-2 cosmetic rewordings or a reordering), one case record with every day count printed, and a short
narrative. Every policy clause is an admitted lexicon form (G-LEX) whose values are typed slots, so a cosmetic
rewording is another admitted form of the same clause meaning: its rule AST is identical (rules.ast_equal; the spec's
"admitted only by AST equality"). The card states how a version decides a case: NEG when the category is excluded,
the request is late or an amount rule fails; otherwise ALT when a condition clause gives ALT; otherwise POS. The
question asks whether the outcome differs between the versions, or for the outcome under the revised version.
Semantics: G0_SPEC.md (sha below).

  solver A   rule AST: each version becomes a rules.RuleSet (first_match over Rule / In / Cmp / Fn days_between, Lit
             values from the version's slots, Ref to the case slots) run by rules.resolve; materiality is
             outcome(V1) != outcome(V2)                                                     paradigm ast_interpreter
  solver B   solver_b.py: its own parser of the RENDERED row (block headers; bullet, table, update and edit-list
             containers read through the lexicon registry; record regex; skin template), then one SQL query per
             version over an in-memory sqlite database (julianday day counts, COALESCE for the time limit, CASE for
             the outcome)                                                                   paradigm sql_sqlite
  samplers   S1 forward; S2 boundary-first (every proposal on a boundary); S3 table-first (side-by-side table);
             S4 record-first update notice; S5 held out (held-out domains, edit-list container, held-out skins and
             wordings)
  edits      anchor; base time limit; amount rule (value, inclusivity, added, removed); condition clause (value, added,
             removed); exclusion = scope (value, added, removed); special time limit by category or by date window
             (value, added, removed); cosmetic only (rewordings, reordering)
  questions  yn_changes and yn_dneg (double negation) ask "the outcome changes"; complements yn_same (antonym),
             yn_not_change (syntactic) and yn_fail_change (implicit); ch_v2 asks the outcome under the revised version
  relations  complement; minimal-edit twin (request date, amount, category, condition, or the revised value of the
             edited clause); equiv (another skin and versions container); G4 metamorphic: rename the customer, shift
             every date, shift every amount, reorder the revised version, swap an unmentioned category
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import random
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from c2_kit import paths  # noqa: F401  (puts c_src/common on sys.path)
from c2_kit import cards as CD
from c2_kit import polarity as POL
from c2_kit import rules as RL
from c2_kit import slots as S
from c2_kit.choiceplan import plan_choice
from c2_kit.distractors import build_closed, error_model, register_name, uhash
from c2_kit.plugin import C2Plugin, ContractError, QuestionForm, RelationProposal, Spec, choose_forms
from c2_kit.rows import TextBuilder, assemble_row
from c2_kit import skin as K
import negcount  # noqa: E402  (c_src/common, read-only)

HERE = Path(__file__).resolve().parent
FAMILY = "T24"


# ------------------------------------------------------------------------------------------------ domain packs
@dataclass(frozen=True)
class Domain:
    """One everyday setting (a pack; G0_SPEC.md R2). After A38 the packs come from T24's Haiku pack tasks
    (haiku/author/, pack-a / pack-b) in this format and pass check_domain(). Every surface is lower case, one line,
    without digits, commas, " and ", pipes, braces or negation cues (negcount k_all > 0); the first date field is
    never later than the second."""
    key: str
    title: str                 # policy name, lower case ("returns policy")
    prefix: str                # case id prefix
    dates: tuple               # (earlier date field, later date field)
    amount: str                # the money field ("price")
    cats: tuple                # 4-5 item categories
    conds: tuple               # 3 conditions
    outcomes: tuple            # (POS, ALT, NEG) outcome names
    held_out: bool = False     # S5 only


STANDIN_DOMAINS = {d.key: d for d in (
    Domain("retail", "returns policy", "RET", ("order date", "delivery date"), "price",
           ("electronics", "clothing", "furniture", "toys", "kitchenware"), ("unopened", "opened", "final sale"),
           ("full refund", "store credit", "refund refused")),
    Domain("warranty", "repair cover policy", "WAR", ("purchase date", "registration date"), "repair cost",
           ("laptops", "phones", "tablets", "headphones"), ("intact", "water damaged", "dropped"),
           ("free repair", "discounted repair", "paid repair")),
    Domain("travel", "delay compensation policy", "TRV", ("booking date", "travel date"), "fare",
           ("rail", "coach", "ferry", "tram"), ("delayed", "cancelled", "rerouted"),
           ("cash compensation", "travel voucher", "claim refused")),
    Domain("expenses", "expense policy", "EXP", ("purchase date", "receipt date"), "amount",
           ("travel", "meals", "software", "training", "equipment"), ("itemised receipt", "card slip", "photo copy"),
           ("full reimbursement", "partial reimbursement", "claim rejected")),
    Domain("courses", "course fee policy", "CRS", ("enrolment date", "start date"), "course fee",
           ("language", "coding", "music", "art"), ("unattended", "partly attended", "fully attended"),
           ("fee returned", "course credit", "fee kept")),
    Domain("tickets", "ticket refund policy", "TKT", ("booking date", "event date"), "ticket price",
           ("concerts", "theatre", "sports", "festivals"), ("cancelled", "rescheduled", "relocated"),
           ("cash refund", "ticket credit", "refund refused")),
    Domain("shipping", "shipping claims policy", "SHP", ("ship date", "delivery date"), "declared value",
           ("parcels", "pallets", "envelopes", "crates"), ("crushed", "wet", "torn"),
           ("full payout", "partial payout", "claim closed")),
    Domain("rentals", "rental deposit policy", "RNT", ("pick-up date", "return date"), "deposit",
           ("cars", "vans", "bikes", "trailers"), ("clean", "scratched", "dented"),
           ("deposit returned", "deposit halved", "deposit kept")),
    Domain("subscriptions", "cancellation policy", "SUB", ("sign-up date", "renewal date"), "plan fee",
           ("monthly plan", "annual plan", "family plan", "student plan"), ("unused", "lightly used", "heavily used"),
           ("full refund", "prorated refund", "fee kept")),
    Domain("rebates", "rebate policy", "RBT", ("purchase date", "installation date"), "purchase price",
           ("heat pumps", "boilers", "water heaters", "solar panels"),
           ("certified install", "self install", "dealer install"),
           ("full rebate", "reduced rebate", "rebate refused")),
    Domain("hotels", "booking amendment policy", "HTL", ("booking date", "arrival date"), "room rate",
           ("standard rooms", "suites", "villas", "cabins"), ("member", "guest", "group"),
           ("full refund", "hotel credit", "charge kept"), held_out=True),
    Domain("gyms", "membership freeze policy", "GYM", ("join date", "injury date"), "monthly fee",
           ("basic", "premium", "family", "off-peak"), ("documented", "self-reported", "coach-reported"),
           ("fee waived", "fee halved", "fee charged"), held_out=True),
)}
SURFACE_RE = re.compile(r"[a-z][a-z' -]*[a-z]")
# label words (plugin LABEL_WORDS): the materiality words of the questions and generic outcome words; no pack string
# holds a materiality word, and no category, condition, date field or money field holds a generic outcome word
MATERIAL_WORDS = ("change", "changes", "changed", "unchanged", "same", "different", "difference", "differ", "differs",
                  "material", "immaterial", "affect", "affects", "affected", "unaffected", "matter", "matters")
OUTCOME_WORDS = ("refund", "credit", "compensation", "voucher", "reimbursement", "payout", "rebate")


# The label words the v1 Haiku authoring ran with (materiality words, generic outcome words and the stand-in packs
# outcome names): authoring.py and redo2.py rebuild the frozen task files from them. LABEL_WORDS (the plugin) adds the
# outcome names of every pool pack, which G-SL then keeps out of skins and wordings at generation time (F1).
AUTHORING_LABEL_WORDS = tuple(dict.fromkeys(MATERIAL_WORDS + OUTCOME_WORDS
                                            + tuple(o for d in STANDIN_DOMAINS.values() for o in d.outcomes)))
# The sha of the G0 (v2.1) the Haiku task files and the frozen pools were authored under: their manifests record it.
# The plugin's own G0_SHA256 moved with v2.2 (card text, balance, skins), which changes no pool and no task.
G0_SHA256_AUTHORED = "652dd74a8ec7b681e605130586bfc83274509f02f3d0eab75c9f6f584344b85f"
# The negative (antonym) predicates of "the outcome differs" (c2_kit.polarity P1-P3): "the same outcome" reads as one
# negation layer over "different", so a wording negates syntactically ("does not change") or uses one of these, never
# both; negcount's own implicit cues (fail to, lack, without, ...) count too.
NEGATIVE_PREDICATES = (
    r"same", r"unchanged", r"identical", r"alike", r"unaltered", r"unaffected", r"equal(?:ly)?",
    r"(?:stay|stays|stayed|staying|remain|remains|remained|remaining)\s+as\s+(?:it|they)\s+(?:was|were)",
    r"as\s+it\s+was", r"no\s+different",
)
# Lead ruling (strict-frame review of the Stage B pilot; never a relabel). c2_kit.polarity P4 ("aux + subject + not")
# flags 19 yn_not_change wordings and 1 yn_dneg wording. The 19 "Does the revision not change ...?" frames are kept: one
# syntactic negation, declared polarity -1, and both G5-H readers matched gold on every not_change row they read. The
# one held-out yn_dneg wording stacks a negative frame on "nothing ... changes" (frame + embedded negation), which reads
# either way: quarantined (it fed mixdev only; the training pool is unchanged).
QUARANTINED_WORDINGS = {
    "Would an auditor not agree that nothing about this case's outcome changes under the revision?":
        "lead ruling: negative question frame ('aux + subject + not') stacked on an embedded negation (P4)",
}


def check_domain(dom: Domain) -> list:
    """Program checks of one pack (G0_SPEC.md R2): the problems, empty when the pack is usable."""
    probs = []
    if not dom.title.endswith(" policy"):
        probs.append(f"title {dom.title!r}: '... policy'")
    for f in dom.dates:
        if not f.endswith(" date") or f == "request date":
            probs.append(f"date field {f!r}: ends in 'date' and is not the request date")
    sets = {"dates": dom.dates, "amount": (dom.amount,), "cats": dom.cats, "conds": dom.conds,
            "outcomes": dom.outcomes}
    if not re.fullmatch(r"[A-Z]{3}", dom.prefix):
        probs.append("case id prefix: three capital letters")
    if (len(dom.dates), len(dom.conds), len(dom.outcomes)) != (2, 3, 3) or not 4 <= len(dom.cats) <= 5:
        probs.append("sizes: 2 date fields, 4-5 categories, 3 conditions, 3 outcomes")
    seen: dict = {}
    for name, items in sets.items():
        if len(set(items)) != len(items):
            probs.append(f"{name}: a name repeats")
        for s in items:
            if s in seen and seen[s] != name:
                probs.append(f"{s!r} is in {seen[s]} and {name}")
            seen[s] = name
    for s in (dom.title,) + tuple(seen):
        if not SURFACE_RE.fullmatch(s) or re.search(r"\band\b|  ", s):
            probs.append(f"{s!r}: lower-case words, hyphens or apostrophes, no 'and'")
        elif negcount.k_all(s):
            probs.append(f"{s!r} holds a negation cue")
        if set(re.split(r"[ -]", s)) & set(MATERIAL_WORDS):
            probs.append(f"{s!r} holds a materiality label word")
    for s in dom.dates + (dom.amount,) + dom.cats + dom.conds:
        if set(s.split()) & set(OUTCOME_WORDS):
            probs.append(f"{s!r} holds a generic outcome word")
    return probs


STANDIN_TRAIN = tuple(k for k, d in STANDIN_DOMAINS.items() if not d.held_out)
STANDIN_HELD = tuple(k for k, d in STANDIN_DOMAINS.items() if d.held_out)


@dataclass(frozen=True)
class PackSet:
    """The packs a plugin deals to its cards: the key lists in dealing order (training / held out) and where they came
    from. `domains` is the global DOMAINS lookup (every pack of every set); `train` / `held` are this set's keys."""
    name: str
    train: tuple
    held: tuple


STANDIN_PACKS = PackSet("standin", STANDIN_TRAIN, STANDIN_HELD)      # the 10 + 2 in-code packs: tests only
POOL_DIR = HERE / "pools"
MIN_TRAIN_PACKS, N_HELD_PACKS = 32, 4                                # G0 section 2 (one pack per card); spec 3.0 >= 25


def load_pool_packs(root: Path | None = None) -> tuple:
    """(domains, PackSet) of the FROZEN pack pool (pools/packs.json; sha256 = pools/MANIFEST.json pool_files), in file
    order: the training list is dealt to the cards in that order (domain_for). Every pack passes check_domain. Raises
    ContractError on a sha mismatch, a bad pack or a pool too small for one pack per card."""
    root = Path(root) if root else POOL_DIR
    man = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    raw = (root / "packs.json").read_bytes()
    want = man["pool_files"]["packs.json"]["sha256"]
    if hashlib.sha256(raw).hexdigest() != want:
        raise ContractError(f"pools/packs.json sha256 differs from pools/MANIFEST.json ({want[:12]})")
    doms: dict = {}
    train, held = [], []
    for rec in json.loads(raw.decode("utf-8")):
        p = rec["pack"]
        d = Domain(rec["pool_id"], p["title"], p["prefix"], tuple(p["date_fields"]), p["money_field"],
                   tuple(p["categories"]), tuple(p["conditions"]), tuple(p["outcomes"]), bool(rec["held_out"]))
        probs = check_domain(d)
        if probs or d.key in doms:
            raise ContractError(f"pool pack {d.key}: {probs or 'duplicate pool id'}")
        doms[d.key] = d
        (held if d.held_out else train).append(d.key)
    if len(train) < MIN_TRAIN_PACKS or len(held) != N_HELD_PACKS:
        raise ContractError(f"pack pool: {len(train)} training / {len(held)} held-out packs "
                            f"(need >= {MIN_TRAIN_PACKS} / {N_HELD_PACKS})")
    return doms, PackSet("pool", tuple(train), tuple(held))


try:                                              # the frozen pool is part of the family; absent only in odd checkouts
    _POOL_DOMAINS, POOL_PACKS = load_pool_packs()
    POOL_ERROR = None
except FileNotFoundError:
    _POOL_DOMAINS, POOL_PACKS, POOL_ERROR = {}, None, "pools/ not found"
except ContractError as _e:
    _POOL_DOMAINS, POOL_PACKS, POOL_ERROR = {}, None, str(_e)
# every pack a row can name (solvers and renderers look the pack up by key): stand-ins (tests) and the pool
DOMAINS = {**STANDIN_DOMAINS, **_POOL_DOMAINS}
# stand-in key lists under their old names (tests); the pool lists are POOL_PACKS.train / .held
TRAIN_DOMAINS, HELD_DOMAINS = STANDIN_TRAIN, STANDIN_HELD
CUSTOMERS = ("Dana Okafor", "Lena Whitcombe", "Ravi Anand", "Mira Castell", "Tomas Ferreira", "Aiko Brandt",
             "Priya Shah", "Omar Haddad", "Grace Mensah", "Hugo Laine", "Ines Duarte", "Keiko Sato", "Leon Novak",
             "Maya Reyes", "Nadia Petrov", "Oscar Byrne", "Rosa Kim", "Sanjay Iqbal", "Tara Walsh", "Victor Osei")

# ------------------------------------------------------------------------------------------------ rule constants
UNIT_DAY = ("day", "days")
ROLES = ("pos", "alt", "neg")                          # outcome keys (ch_v2 answers); Domain.outcomes in this order
PARAMS = {"win": ("N", "A"), "amt": ("M", "X"), "exc": ("C",), "alt": ("K", "O"), "ovc": ("C", "N"),
          "ovd": ("A", "S", "E", "N")}
OPS = ("ge", "gt", "le", "lt")
OP_SYM = {"ge": ">=", "gt": ">", "le": "<=", "lt": "<"}
OP_PY = {"ge": lambda a, x: a >= x, "gt": lambda a, x: a > x, "le": lambda a, x: a <= x, "lt": lambda a, x: a < x}
OP_FLIP = {"ge": "gt", "gt": "ge", "le": "lt", "lt": "le"}       # an inclusivity edit
OP_MISREAD = {"ge": "lt", "gt": "le", "le": "gt", "lt": "ge"}    # a "... do not qualify" form read as the requirement
OP_REVERSE = {"ge": "le", "gt": "lt", "le": "ge", "lt": "gt"}    # at least <-> at most (direction confused)
LIMITS = (7, 10, 14, 20, 21, 28, 30, 45, 60, 90)
SPECIAL_LIMITS = (3, 5, 7, 10, 14, 21, 30, 45, 60, 90)
AMOUNTS = (1500, 2000, 2500, 4000, 5000, 7500, 10000, 15000, 20000, 25000, 50000)
AMOUNT_STEPS = (500, 1000, 2500, 5000)
DAY_OFFSETS = (0, 0, 0, 1, 1, 1, -1, 2, -2, 4, -4, 7, -7, 11, -11)      # around a time limit: 0 / +1 = boundary
DAY_OFFSETS_BOOST = (0, 1)
AMOUNT_OFFSETS = (0, 0, -1, 1, -1, 1, 100, -100, 250, -250, 1000, -1000)
AMOUNT_OFFSETS_BOOST = (0, -1, 1)
GAPS = (0, 1, 2, 3, 3, 4, 5, 6, 7, 9, 12, 15, 20)                         # days between the two date fields
RANGE_IN = (0, 0, 1, 2, 4, 7, 10, 14)                                     # covering window: days before / after
RANGE_IN_BOOST = (0, 1)
RANGE_OUT = (1, 1, 2, 3, 6, 10, 20)                                       # window that misses the date: distance
RANGE_OUT_BOOST = (1,)
FIRST_DAY, SPAN_DAYS = dt.date(2025, 2, 1), 1030
P_CLAUSE = {"amt": 0.40, "exc": 0.35, "alt": 0.42, "ovr": 0.22}
VARIANTS = {"amount": (("value", 0.4), ("op", 0.2), ("add", 0.2), ("remove", 0.2)),
            "alt": (("value", 0.5), ("add", 0.25), ("remove", 0.25)),
            "excl": (("value", 0.5), ("add", 0.25), ("remove", 0.25)),
            "override": (("value", 0.5), ("add", 0.25), ("remove", 0.25))}
OWN_CLAUSE = {"amount": "amt", "alt": "alt", "excl": "exc", "override": "ovr"}
MASKS = {"anchor": ("exc", "amt"), "limit": ("exc", "amt"), "override": ("exc", "amt"), "amount": ("exc", "late"),
         "excl": ("amt", "late"), "alt": ("exc", "amt", "late")}
EDIT_GATE = {"anchor": "late", "limit": "late", "override": "late", "amount": "pf", "excl": "ex", "alt": "al"}
MAX_DOCS, MAX_CASES = 40, 60

# Target draw (G0_SPEC.md section 2): gold first (per-card rate), then (edit kind, case mode) from its label's table.
YES_PLAN = ((("anchor", "flip"), 0.40), (("limit", "flip"), 0.12), (("amount", "flip"), 0.12),
            (("alt", "flip"), 0.12), (("excl", "flip"), 0.10), (("override", "flip"), 0.14))
NO_PLAN = ((("cosmetic", "cosmetic"), 0.16),
           (("alt", "untouched"), 0.10), (("excl", "untouched"), 0.10), (("override", "untouched"), 0.16),
           (("limit", "untouched"), 0.08),
           (("anchor", "same"), 0.12), (("anchor", "masked"), 0.08),
           (("limit", "same"), 0.04), (("limit", "masked"), 0.02),
           (("amount", "same"), 0.06), (("amount", "masked"), 0.02),
           (("alt", "masked"), 0.02), (("excl", "masked"), 0.02), (("override", "same"), 0.01),
           (("override", "masked"), 0.01))
QFORM_SHARES = (("ch_v2", 0.54), ("yn_changes", 0.20), ("yn_same", 0.08), ("yn_not_change", 0.07),
                ("yn_fail_change", 0.05), ("yn_dneg", 0.06))
N_CARDS, N_CARDS_HELD = 8, 4                     # cards per training sampler (one pack each) / for S5
TRAIN_SAMPLERS = ("S1", "S2", "S3", "S4")
CONTAINER = {"S1": "lines", "S2": "lines", "S3": "table", "S4": "update", "S5": "diff"}
BLOCKS = {"S1": ("narr", "versions", "record"), "S2": ("record", "versions", "narr"),
          "S3": ("versions", "record", "narr"), "S4": ("narr", "record", "versions"),
          "S5": ("narr", "versions", "record")}
EQUIV_CONTAINER = {"lines": "table", "table": "lines", "update": "table", "diff": "lines"}
COMP_RATE, EQUIV_RATE, TWIN_RATE = 0.40, 0.10, 0.48
# Outcome under the revised version, by (outcome changes, the revised version has a condition clause). Masked cases
# are always NEG, so the other no-change cases lean away from NEG: the revised outcome then carries no gold signal.
# v2.2 (F3, G0 Balance): fitted so that the ch_v2 roles of all choice rows (bases, equiv partners, twins) are 1/k in
# each option bucket within +-3 pp (k = 3 also holds the rows whose V2 lost the condition clause, which cannot be ALT,
# so ALT is lifted where it can be); balance_check.choice_role_report measures it, P(change | role) stays in 0.45-0.55.
OUT2_WEIGHTS = {(True, True): (("pos", 0.315), ("alt", 0.305), ("neg", 0.38)),
                (True, False): (("pos", 0.53), ("neg", 0.47)),
                (False, True): (("pos", 0.41), ("alt", 0.46), ("neg", 0.13)),
                (False, False): (("pos", 0.595), ("neg", 0.405))}
DECOYS = ("amt", "exc", "alt", "ovr")            # cosmetic rows: one forced clause, like every other edit kind

# Fix iteration 2 (G6, c_card_without_question): the ch_v2 option count k and the gold role are dealt TOGETHER from
# the seed before any structure is drawn, so every role is gold at its fair share inside each k (k = 2: pos / neg
# 1/2 each; k = 3: pos / alt / neg 1/3 each), by construction and not by a fitted weight table. Half the choice rows
# take k = 3 (the revised-or-original version holds a condition clause), half k = 2 (neither does).
CELLS = (((2, "pos"), 1 / 4), ((2, "neg"), 1 / 4), ((3, "pos"), 1 / 6), ((3, "alt"), 1 / 6), ((3, "neg"), 1 / 6))

QUESTION_TABLE = {"yn_changes": lambda o1, o2: int(o1 != o2), "yn_dneg": lambda o1, o2: int(o1 != o2),
                  "yn_same": lambda o1, o2: int(o1 == o2), "yn_not_change": lambda o1, o2: int(o1 == o2),
                  "yn_fail_change": lambda o1, o2: int(o1 == o2), "ch_v2": lambda o1, o2: o2}

# ------------------------------------------------------------------------------------------------ program text
CLOSED_WORLD = "The two versions and the case record are complete: no other rule or fact applies."
TABLE_LABEL = {"win": "Time limit", "amt": "Amount rule", "exc": "Exclusion", "alt": "Condition rule",
               "ovr": "Special time limit"}
TABLE_ROWS = ("win", "amt", "exc", "alt", "ovr")
NONE_CELL = "(none)"


def _cap(t: str) -> str:
    return t[:1].upper() + t[1:]


def _list(items) -> str:
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


CARD_STYLES = (("full", 0.85), ("short", 0.15))     # G0 v2.2 R9: the short card on about 15% of rows (spec 3.0)
SHORT_CARD_SHARE = dict(CARD_STYLES)["short"]


@lru_cache(maxsize=None)
def card_spec(dom: Domain) -> CD.CardSpec:
    """The card of a pack as a c2_kit.cards.CardSpec (G0_SPEC.md R9 quotes both styles verbatim, pack constants as
    placeholders). Program text, no slot. Every rule of the v2.1 card is kept (variant_problems checks the short
    phrasing against the full one); v2.2 only shortens the wording and states that a special time-limit clause
    "replaces only the limit" (pilot G5-H: reader error t24_special_date_as_anchor)."""
    pos, alt, neg = dom.outcomes
    mid = (f"category is excluded, the request is late, or the case fails a rule on the {dom.amount}; otherwise {alt}"
           f" if a clause gives {alt} for the case")           # same words in both styles (variant_problems)
    items = (
        CD.CardItem(
            "outcome",
            f"The outcome under each version is {neg} if the case's {mid}'s condition; otherwise {pos}.",
            short=f"Outcome under each version: {neg} if the case's {mid}'s condition; otherwise {pos}."),
        CD.CardItem(
            "special",
            "A special time-limit clause replaces only the limit, for cases in its category or whose date it names"
            " lies in its window (both end dates included).",
            short="A special time-limit clause replaces only the limit, for its category or for cases whose date it"
                  " names lies in its window (both end dates included)."),
        CD.CardItem(
            "days",
            "Day counts are calendar days from the date named in the time-limit clause (day zero), printed in the"
            " record. Late means a day count above the limit.",
            short="Late means the day count (calendar days from the date named in the time-limit clause, day zero,"
                  " printed in the record) is above the limit."),
        CD.CardItem("lists", f"Categories: {_list(dom.cats)}. Conditions: {_list(dom.conds)}."),
    )
    return CD.CardSpec(FAMILY, items, heads={"full": f"Apply each version of the {dom.title} to the case on its own.",
                                             "short": ""}, tail=CLOSED_WORLD, numbered=False)


def rules_text(dom: Domain, style: str = "full") -> str:
    """The card text of a style (G0_SPEC.md R9): "full" (85% of rows) or "short" (15%)."""
    return card_spec(dom).template(style)


def record_template(dom: Domain) -> str:
    """The case record (program text with slots; G0_SPEC.md R10). Every day count is printed."""
    d1, d2 = dom.dates
    return ("Case record {CASE_ID}:\n- category: {CAT}\n- condition: {COND}\n"
            f"- {dom.amount}: {{AMOUNT}}\n- {d1}: {{D1}}\n- {d2}: {{D2}}\n- request date: {{REQ}}\n"
            f"- days from the {d1} to the request date: {{DAYS1}}\n"
            f"- days from the {d2} to the request date: {{DAYS2}}")


def sn(v: int, kind: str, param: str | None = None) -> str:
    """Slot name of a version clause (the clause slot itself, or one of its parameters)."""
    return f"V{v}_{kind.upper()}" + (f"_{param}" if param else "")


def sem_of(kind: str, p: dict) -> str:
    return f"t24.amt.{p['op']}" if kind == "amt" else f"t24.{kind}"


def _ovr_kind(kinds) -> str | None:
    return "ovc" if "ovc" in kinds else ("ovd" if "ovd" in kinds else None)


def _changed(spec: Spec, kind: str) -> bool:
    """A clause present in both versions whose sem, form or any value differs."""
    a, b = spec.slots[sn(1, kind)], spec.slots[sn(2, kind)]
    if a.value[:2] != b.value[:2]:
        return True
    return any(S.canonical(spec.slots[sn(1, kind, p)]) != S.canonical(spec.slots[sn(2, kind, p)])
               for p in PARAMS[kind])


def versions_template(spec: Spec, container: str | None = None) -> str:
    """The two versions in one container (G0_SPEC.md R11): bullet lines, an update notice, a side-by-side table or
    the original version plus an edit list."""
    dom = DOMAINS[spec.structure["domain"]]
    o1, o2 = spec.structure["v1"], spec.structure["v2"]
    container = container or spec.structure["container"]

    def bullets(v, order):
        return "\n".join(f"- {{{sn(v, k)}}}." for k in order)

    if container == "lines":
        return (f"{_cap(dom.title)}, original version:\n{bullets(1, o1)}\n\n"
                f"{_cap(dom.title)}, revised version:\n{bullets(2, o2)}")
    if container == "update":
        return (f"Original version of the {dom.title} (before the update):\n{bullets(1, o1)}\n\n"
                f"Revised version of the {dom.title} (after the update):\n{bullets(2, o2)}")
    if container == "table":
        rows = [f"{_cap(dom.title)}, original and revised versions side by side:",
                "| Clause | Original version | Revised version |", "| --- | --- | --- |"]
        for r in TABLE_ROWS:
            cells = []
            for v, order in ((1, o1), (2, o2)):
                k = _ovr_kind(order) if r == "ovr" else (r if r in order else None)
                cells.append(f"{{{sn(v, k)}}}" if k else NONE_CELL)
            if cells != [NONE_CELL, NONE_CELL]:
                rows.append(f"| {TABLE_LABEL[r]} | {cells[0]} | {cells[1]} |")
        return "\n".join(rows)
    if container == "diff":
        lines = []
        for k in o1:
            if k not in o2:
                lines.append(f"removed: {{{sn(1, k)}}}.")
            elif _changed(spec, k):
                lines += [f"removed: {{{sn(1, k)}}}.", f"added: {{{sn(2, k)}}}."]
        lines += [f"added: {{{sn(2, k)}}}." for k in o2 if k not in o1]
        return (f"{_cap(dom.title)}, original version:\n{bullets(1, o1)}\n\n"
                "Edits made in the revised version:\n" + "\n".join(lines))
    raise ContractError(f"container {container!r}")


# ------------------------------------------------------------------------------------------------ construction view
def facts(spec: Spec) -> tuple:
    """(domain, v1, v2, case) as plain python values, read from the spec's slots (the construction side: twins,
    tags and error models use it; solver A builds its own rule AST from the slots)."""
    env = spec.env()
    dom = DOMAINS[spec.structure["domain"]]
    vs = []
    for v in (1, 2):
        ver = {}
        for kind in spec.structure[f"v{v}"]:
            g = lambda p: env[sn(v, kind, p)]          # noqa: E731
            if kind == "win":
                ver[kind] = {"n": g("N"), "a": dom.dates.index(g("A"))}
            elif kind == "amt":
                ver[kind] = {"op": env[sn(v, kind)].rsplit(".", 1)[1], "x": g("X")}
            elif kind == "exc":
                ver[kind] = {"c": g("C")}
            elif kind == "alt":
                ver[kind] = {"k": g("K")}
            elif kind == "ovc":
                ver[kind] = {"c": g("C"), "n": g("N")}
            else:
                ver[kind] = {"a": dom.dates.index(g("A")), "s": g("S"), "e": g("E"), "n": g("N")}
        vs.append(ver)
    case = {"cat": env["CAT"], "cond": env["COND"], "amount": env["AMOUNT"], "d": (env["D1"], env["D2"]),
            "req": env["REQ"]}
    return dom, vs[0], vs[1], case


def _copy(ver: dict) -> dict:
    return {k: dict(p) for k, p in ver.items()}


def _covers(ver: dict, case: dict) -> bool:
    if "ovc" in ver:
        return case["cat"] == ver["ovc"]["c"]
    if "ovd" in ver:
        o = ver["ovd"]
        return o["s"] <= case["d"][o["a"]] <= o["e"]
    return False


def _gates(ver: dict, case: dict, m: dict | None = None) -> dict:
    """The four gates of one version for one case: excluded, late, amount fails, condition clause applies. `m` names
    one reading mistake (the error models): swap_anchor, day0, late1, no_late, no_alt, alt_any, no_special,
    special_all, special_anchor, no_exc, no_amt, op (an operator replacing the stated one)."""
    m = m or {}
    a = ver["win"]["a"]
    if m.get("swap_anchor"):
        a = 1 - a
    lim = ver["win"]["n"]
    ov = _ovr_kind(ver)
    if ov and not m.get("no_special") and (m.get("special_all") or _covers(ver, case)):
        lim = ver[ov]["n"]
        if m.get("special_anchor") and ov == "ovd":
            a = ver["ovd"]["a"]
    days = (case["req"] - case["d"][a]).days
    if m.get("day0"):
        days += 1
    if m.get("late1"):
        days -= 1
    ex = "exc" in ver and not m.get("no_exc") and case["cat"] == ver["exc"]["c"]
    pf = "amt" in ver and not m.get("no_amt") and not OP_PY[m.get("op") or ver["amt"]["op"]](case["amount"],
                                                                                              ver["amt"]["x"])
    al = "alt" in ver and not m.get("no_alt") and (m.get("alt_any") or case["cond"] == ver["alt"]["k"])
    return {"ex": ex, "late": days > lim and not m.get("no_late"), "pf": pf, "al": al}


def direct_outcome(ver: dict, case: dict, m: dict | None = None) -> str:
    """Construction-side outcome (plain arithmetic, not the rule AST): used for twin predictions, tags and the
    error models. G-TW checks solver A against it on every twin."""
    m = m or {}
    if m.get("pos_always"):
        return "pos"
    g = _gates(ver, case, m)
    if m.get("alt_first") and g["al"]:
        return "alt"
    if g["ex"] or g["late"] or g["pf"]:
        return "alt" if m.get("alt_fallback") else "neg"
    if m.get("alt_as_neg") and g["al"]:
        return "neg"
    return "alt" if g["al"] else "pos"


def _applies(kind: str, ver: dict, case: dict) -> bool:
    """Does the edited clause take part in deciding this case under this version?"""
    if kind == "limit":
        return not _covers(ver, case)
    if kind == "override":
        return _covers(ver, case)
    if kind == "excl":
        return "exc" in ver and case["cat"] == ver["exc"]["c"]
    if kind == "alt":
        return "alt" in ver and case["cond"] == ver["alt"]["k"]
    if kind == "amount":
        return "amt" in ver
    return True


def mode_of(kind: str, v1: dict, v2: dict, case: dict) -> str:
    """cosmetic | flip (the outcome changes) | untouched (the edited clause decides nothing for this case in either
    version) | masked (the edited clause flips but a shared clause decides) | same (it applies and agrees)."""
    o1, o2 = direct_outcome(v1, case), direct_outcome(v2, case)
    if kind == "cosmetic":
        return "cosmetic" if o1 == o2 else "cosmetic_changed"
    if o1 != o2:
        return "flip"
    if not (_applies(kind, v1, case) or _applies(kind, v2, case)):
        return "untouched"
    g = EDIT_GATE[kind]
    return "masked" if _gates(v1, case)[g] != _gates(v2, case)[g] else "same"


# ------------------------------------------------------------------------------------------------ solver A
def version_rules(spec: Spec, v: int) -> RL.RuleSet:
    """Solver A's AST of one version: first_match over [excluded, late (special / base), amount, condition], default
    POS. Clause values enter as Lit (so two versions' ASTs compare by value); case facts are Ref to the case slots."""
    env = spec.env()
    dom = DOMAINS[spec.structure["domain"]]
    kinds = set(spec.structure[f"v{v}"])

    def val(kind, p):
        return env[sn(v, kind, p)]

    def date_ref(field):
        return RL.Ref(("D1", "D2")[dom.dates.index(field)])

    rules = []
    if "exc" in kinds:
        rules.append(RL.Rule("excluded", "neg", RL.In(RL.Ref("CAT"), (RL.Lit(val("exc", "C")),))))
    age = RL.Fn("days_between", (date_ref(val("win", "A")), RL.Ref("REQ")))
    base_late = RL.Cmp(">", age, RL.Lit(val("win", "N")))
    cover = None
    if "ovc" in kinds:
        cover, special = RL.In(RL.Ref("CAT"), (RL.Lit(val("ovc", "C")),)), val("ovc", "N")
    elif "ovd" in kinds:
        f = date_ref(val("ovd", "A"))
        cover = RL.And((RL.Cmp("<=", RL.Lit(val("ovd", "S")), f), RL.Cmp("<=", f, RL.Lit(val("ovd", "E")))))
        special = val("ovd", "N")
    if cover is None:
        rules.append(RL.Rule("late", "neg", base_late))
    else:
        rules.append(RL.Rule("late_special", "neg", RL.And((cover, RL.Cmp(">", age, RL.Lit(special))))))
        rules.append(RL.Rule("late", "neg", RL.And((RL.Not(cover), base_late))))
    if "amt" in kinds:
        op = env[sn(v, "amt")].rsplit(".", 1)[1]
        rules.append(RL.Rule("amount", "neg", RL.Not(RL.Cmp(OP_SYM[op], RL.Ref("AMOUNT"), RL.Lit(val("amt", "X"))))))
    if "alt" in kinds:
        rules.append(RL.Rule("condition", "alt", RL.In(RL.Ref("COND"), (RL.Lit(val("alt", "K")),))))
    return RL.RuleSet(tuple(rules), "first_match", "pos")


def outcome_a(spec: Spec, v: int) -> str:
    return RL.resolve(version_rules(spec, v), spec.env()).effect


# ------------------------------------------------------------------------------------------------ draws
def _weyl(seed: int, sampler: str, which: int) -> float:
    """Low-discrepancy draw per seed (0 gold, 1 edit plan, 2 question form; a 3-d Kronecker sequence): the gold
    shares hold tightly within every question form on any run of seeds. 3 is the card style (its own 1-d draw)."""
    alpha = (0.6180339887498949, 0.41421356237309515, 0.7320508075688772, 0.14159265358979312,
             0.2360679774997897)[which]       # 4: the ch_v2 (k, role) cell (fix iteration 2)
    return (seed * alpha + uhash(FAMILY, "weyl", sampler, which)) % 1.0


def card_style(spec: Spec) -> str:
    """The card style of a unit (G0 v2.2 R9): "short" on SHORT_CARD_SHARE of the seeds, else "full". Label-blind and
    form-blind (seed and sampler only), so a complement, twin or equiv partner carries the same card as its base."""
    return "short" if _weyl(spec.seed, spec.sampler, 3) < SHORT_CARD_SHARE else "full"


def _edit_joint(material: bool, k: int) -> tuple:
    """(entries, roles, J): the joint of (edit kind, case mode) and the V2 role inside one (materiality, k) cell.
    Marginal over roles: 1/k each (the deal). Marginal over entries: the G0 plan table, with the alt edits living on
    k = 3 only (twice their share there, so the alt share over all choice rows is the table's). What a construction
    cannot give is excluded: a masked case is NEG; a flipping alt edit moves POS <-> ALT; an untouched alt edit
    never reaches ALT. Iterative proportional fitting of the support (deterministic floats)."""
    key = (material, k)
    if key in _JOINTS:
        return _JOINTS[key]
    roles = ("pos", "neg") if k == 2 else ROLES
    table = YES_PLAN if material else NO_PLAN
    a = sum(p for (kind, _m), p in table if kind == "alt")
    entries, t = [], []
    for (kind, mode), p in table:
        if kind == "alt":
            p = 0.0 if k == 2 else 2 * p
        else:
            p *= (1 - 2 * a) / (1 - a) if k == 3 else 1 / (1 - a)
        if p > 0:
            entries.append((kind, mode))
            t.append(p)

    def allowed(kind, mode, r):
        if mode == "masked":
            return r == "neg"
        if kind == "alt":
            return r in (("pos", "alt") if mode == "flip" else ("pos", "neg"))
        return True

    sup = [[1.0 if allowed(kind, mode, r) else 0.0 for r in roles] for kind, mode in entries]
    J = [[t[i] * sup[i][j] for j in range(len(roles))] for i in range(len(entries))]
    for _ in range(500):
        for j in range(len(roles)):
            s = sum(J[i][j] for i in range(len(entries)))
            for i in range(len(entries)):
                J[i][j] *= (1.0 / k) / s
        for i in range(len(entries)):
            s = sum(J[i])
            J[i] = [x * t[i] / s for x in J[i]]
    _JOINTS[key] = (entries, roles, J)
    return _JOINTS[key]


_JOINTS: dict = {}


def _pick_edit(u: float, material: bool, k: int, role: str) -> tuple:
    """(edit kind, case mode) given the dealt (k, role) and the materiality: the conditional of _edit_joint."""
    entries, roles, J = _edit_joint(material, k)
    j = roles.index(role)
    tot, acc = sum(J[i][j] for i in range(len(entries))), 0.0
    for i, e in enumerate(entries):
        acc += J[i][j] / tot
        if u < acc:
            return e
    return entries[-1]


def _share(table: tuple, u: float):
    acc = 0.0
    for k, w in table:
        acc += w
        if u < acc:
            return k
    return table[-1][0]


def _weighted(rng: random.Random, items) -> str:
    total = sum(w for _, w in items)
    x, acc = rng.random() * total, 0.0
    for k, w in items:
        acc += w
        if x < acc:
            return k
    return items[-1][0]


def _card_rate(sampler: str, card: int) -> float:
    """Per-card gold-change rate in [0.2, 0.8] (spec 3.0); cards come in antithetic pairs, so the mean is 0.5."""
    h = uhash(FAMILY, "card_rate", sampler, card // 2)
    return 0.2 + 0.6 * (h if card % 2 == 0 else 1.0 - h)


def domain_for(sampler: str, card: int, packs: PackSet) -> Domain:
    """One pack per card (G0_SPEC.md section 2, Cards; Haiku pass H34, H35): card c of the i-th training sampler
    takes training pack (8 i + c) mod P of the pack set, S5 card c takes held-out pack c mod P. The frozen pool
    (75 training + 4 held-out packs) gives every one of the 32 training cards its own pack; the 10 + 2 stand-ins
    (tests only) put every pack on >= 3 (training) or 2 (S5) cards."""
    if sampler == "S5":
        return DOMAINS[packs.held[card % len(packs.held)]]
    i = TRAIN_SAMPLERS.index(sampler)
    return DOMAINS[packs.train[(N_CARDS * i + card) % len(packs.train)]]


def _answer(qform: str, o1: str, o2: str):
    return QUESTION_TABLE[qform](o1, o2)


def predict(qform: str, v1: dict, v2: dict, case: dict):
    """The answer the construction predicts (direct_outcome on both versions; twins and G-TW use it)."""
    return _answer(qform, direct_outcome(v1, case), direct_outcome(v2, case))


for _name, _what in (
        ("t24_original_version", "gives the outcome under the original version instead of the revised one"),
        ("t24_ignore_special_limit", "uses the base time limit although a special time-limit clause covers the case"),
        ("t24_special_date_as_anchor", "counts the days from the date named in the special clause instead of the "
                                       "date named in the time-limit clause"),
        ("t24_ignore_exclusion", "ignores the exclusion clause"),
        ("t24_ignore_amount_rule", "ignores the amount rule"),
        ("t24_negative_rule_misread", "reads an amount rule worded as 'cases whose ... do not qualify' as the "
                                      "requirement itself"),
        ("t24_ignore_time_limit", "forgets the time limit and never treats the request as late"),
        ("t24_condition_before_gates", "applies the condition clause before the exclusion, time-limit and amount "
                                       "checks"),
        ("t24_condition_scope_ignored", "applies the condition clause's outcome whatever the case's condition is"),
        ("t24_special_limit_for_all", "applies the special time limit to every case, ignoring its category or date "
                                      "window"),
        ("t24_removed_clause_kept", "keeps applying a clause that the revised version removed"),
        ("t24_default_outcome", "assumes the case qualifies: skips the exclusion, time-limit and amount checks"),
        ("t24_amount_rule_reversed", "reads the amount rule in the opposite direction (at least as at most)"),
        ("t24_qualifies_in_full", "assumes the case qualifies in full and gives the main outcome without reading "
                                  "the clauses"),
        ("t24_alternative_as_fallback", "gives the alternative outcome, not the refusal, to a case that fails a "
                                        "check"),
        ("t24_condition_as_exclusion", "reads the condition clause as excluding the case")):
    register_name(_name, _what)


# ------------------------------------------------------------------------------------------------ the plugin
class T24Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "everyday"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "04f3cfbe29d55f24cf8dadd59cbb8277db5e9387398784e39f4e02f8a6fc83af"   # frozen v2.2 (G0 section 5)
    # the one Haiku ambiguity pass (G0 sections 4-5): workflow task id, the G0 sha it read, points raised / resolved
    G0_AMBIGUITY_PASS = {"task_id": "c2-data-stage-a/amb:T24", "model": "haiku",
                         "read_g0_sha256": "4f41cc724d72a1dc6e00fae25d7dd94b7c7ef4635654f685b55a25e6f7324d82",
                         "record": "haiku/ambiguity/amb_T24.json", "points": 45, "resolved": 45}
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "ast_interpreter"
    PARADIGM_B = "sql_sqlite"
    SOLVER_B_MODULE = "families.T24.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm("yn_changes", "noul", "material", 1),
        QuestionForm("yn_dneg", "noul", "material", 1),
        QuestionForm("yn_same", "noul", "material", -1, "antonym"),
        QuestionForm("yn_not_change", "noul", "material", -1, "syntactic"),
        QuestionForm("yn_fail_change", "noul", "material", -1, "implicit"),
        QuestionForm("ch_v2", "choice", answer_set="closed"),
    )}
    LABEL_WORDS = tuple(dict.fromkeys(AUTHORING_LABEL_WORDS + tuple(o for d in DOMAINS.values() for o in d.outcomes)))
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("memo", "email", "chat", "ticket", "json", "yaml", "letter", "log", "form", "transcript", "voicemail")
    HELD_OUT_REGISTERS = ("transcript", "voicemail")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW: tuple = ()
    # wording polarity (c2_kit.polarity P1-P3; kit item 3): a yes/no wording reads with its form's declared polarity.
    # "material" (the outcome differs) is positive; the same / unchanged / identical words are its antonym layer.
    POLARITY_CHECK = True
    POLARITY_NEGATIVES = NEGATIVE_PREDICATES
    POLARITY_BASE: dict = {}
    POLARITY_STRICT_FRAMES = False              # lead ruling below: only the one yn_dneg frame is quarantined

    def __init__(self, lexicon=None, packs=None):
        """packs: None = the frozen pack pool (pools/packs.json, sha-checked; the real generation); STANDIN_PACKS =
        the 10 + 2 in-code stand-in packs (unit tests only); or any PackSet over DOMAINS keys."""
        super().__init__(lexicon)
        self._form_cache: dict = {}
        self._screened: list = []                  # [(ctx, screened ctx, {wording id: problems})]
        if packs is None:
            if POOL_PACKS is None:
                raise ContractError(f"T24 needs its frozen pack pool: {POOL_ERROR}")
            packs = POOL_PACKS
        self.packs = packs

    # ------------------------------------------------------------------------------------------- lexicon forms
    def admitted_forms(self, sem: str) -> list:
        """Admitted, non-held-out lexicon forms of one clause meaning (sorted ids; G-LEX vouches for each)."""
        if self.lexicon is None:
            raise ContractError("T24 needs its lexicon registry (T24Plugin(lexicon=...))")
        if sem not in self._form_cache:
            self._form_cache[sem] = sorted(fid for fid, f in self.lexicon.forms.items() if f.sem_id == sem
                                           and not f.held_out and self.lexicon.status(fid) == "admitted")
            if not self._form_cache[sem]:
                raise ContractError(f"no admitted lexicon form for {sem}")
        return self._form_cache[sem]

    # ------------------------------------------------------------------------------------------- sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        held = sampler in self.HELD_OUT_SAMPLERS
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        card = seed % (N_CARDS_HELD if held else N_CARDS)
        dom = domain_for(sampler, card, self.packs)
        qform = _share(QFORM_SHARES, _weyl(seed, sampler, 2))
        hit = _weyl(seed, sampler, 0) < _card_rate(sampler, card)      # the row's gold yes (ch_v2: a change)
        q = self.QFORMS[qform]
        material = hit if q.qtype == "choice" or q.polarity == 1 else not hit
        cell = _share(CELLS, _weyl(seed, sampler, 4)) if q.qtype == "choice" else None     # (k, role)
        if cell is not None:
            kind, mode = _pick_edit(_weyl(seed, sampler, 1), material, *cell)
        else:
            kind, mode = _share(YES_PLAN if material else NO_PLAN, _weyl(seed, sampler, 1))
        v1, v2, edit, case = self._construct(rng, dom, kind, mode, sampler == "S2", cell)
        f1, f2 = self._forms_plan(rng, v1, v2, edit)
        order1, order2 = self._orders(rng, v1, v2, edit)
        slots = self._slots(rng, dom, v1, v2, f1, f2, case)
        structure = {"domain": dom.key, "v1": order1, "v2": order2, "edit": edit, "container": CONTAINER[sampler],
                     "blocks": list(BLOCKS[sampler])}
        spec = Spec(FAMILY, sampler, seed, f"{FAMILY}:{sampler}:c{card:02d}", qform, slots, structure=structure,
                    depth=2, pack=dom.key)
        return self.derive(spec)

    def _construct(self, rng, dom, kind, mode, boost, cell=None) -> tuple:
        """Docs, then case values by boundary-biased proposals, kept only when the case realises the drawn mode and
        the drawn outcome under the revised version (a masked case is NEG; the outcome target is dropped for the
        last quarter of the attempts, so a rare docs draw never blocks the mode)."""
        for attempt in range(MAX_DOCS):
            docs = self._docs(rng, dom, kind, mode, cell[0] if cell else None)
            if docs is None:
                continue
            v1, v2, edit = docs
            if cell is not None:                 # the dealt role is never dropped; structure is redrawn instead
                if ("alt" in v1 or "alt" in v2) != (cell[0] == 3) or (cell[1] == "alt" and "alt" not in v2):
                    continue
                want = cell[1]
            else:
                want = "neg" if mode == "masked" else _weighted(rng, OUT2_WEIGHTS[(mode == "flip", "alt" in v2)])
                if attempt >= 3 * MAX_DOCS // 4:
                    want = None
            for _ in range(MAX_CASES):
                got = self._case(rng, dom, v1, v2, edit, boost and attempt < MAX_DOCS // 2)
                if got is not None and mode_of(kind, *got) == mode and (
                        want is None or direct_outcome(got[1], got[2]) == want):
                    w1, w2, case = got
                    return w1, w2, edit, case
        raise ContractError(f"T24: no construction for {kind}/{mode} in {dom.key}")

    def _new_amt(self, rng) -> dict:
        return {"op": rng.choice(OPS), "x": rng.choice(AMOUNTS)}

    def _new_ovr(self, rng, dom, otype, ver) -> dict | None:
        ns = [n for n in SPECIAL_LIMITS if n != ver["win"]["n"]]
        if otype == "ovc":
            cats = [c for c in dom.cats if not ("exc" in ver and ver["exc"]["c"] == c)]
            return {"c": rng.choice(cats), "n": rng.choice(ns)}
        return {"a": rng.randrange(2), "s": None, "e": None, "n": rng.choice(ns)}

    def _docs(self, rng, dom, kind, mode, k=None):
        """V1 and V2 (one typed edit) for an edit kind. The clause set does not depend on the mode (so clause counts
        carry no gold signal): every kind forces its own clause, a limit edit an unchanged special clause, and one
        more clause drawn from the kind's mask sources (cosmetic: any clause). Date windows of special clauses are
        set with the case (_case)."""
        variant = _weighted(rng, VARIANTS[kind]) if kind in VARIANTS else {"anchor": "anchor", "limit": "value",
                                                                             "cosmetic": "none"}[kind]
        has = {c: rng.random() < p for c, p in P_CLAUSE.items()}
        if k is not None:                       # a dealt option count: the condition clause is present iff k = 3
            has["alt"] = k == 3
        own = OWN_CLAUSE.get(kind)
        if own:
            has[own] = variant != "add"
        if kind == "limit":
            has["ovr"] = True
        src = rng.choice([s for s in MASKS.get(kind, DECOYS) if s != own and not (k == 2 and s == "alt")])
        if src != "late":
            has[src] = True
        otype = rng.choice(("ovc", "ovd")) if has["ovr"] or kind == "override" else None
        v1 = {"win": {"n": rng.choice(LIMITS), "a": rng.randrange(2)}}
        if has["amt"]:
            v1["amt"] = self._new_amt(rng)
        if has["exc"]:
            v1["exc"] = {"c": rng.choice(dom.cats)}
        if has["alt"]:
            v1["alt"] = {"k": rng.choice(dom.conds)}
        if has["ovr"]:
            v1[otype] = self._new_ovr(rng, dom, otype, v1)
        v2 = _copy(v1)
        clause, sub = None, None
        if kind == "anchor":
            clause = "win"
            v2["win"]["a"] = 1 - v1["win"]["a"]
        elif kind == "limit":
            clause = "win"
            ov = _ovr_kind(v1)
            v2["win"]["n"] = rng.choice([n for n in LIMITS if n != v1["win"]["n"] and not (ov and n == v1[ov]["n"])])
        elif kind == "amount":
            clause = "amt"
            if variant == "value":
                x = v1["amt"]["x"]
                v2["amt"]["x"] = rng.choice([x + s for s in AMOUNT_STEPS] + [x - s for s in AMOUNT_STEPS if x - s > 0])
            elif variant == "op":
                v2["amt"]["op"] = OP_FLIP[v1["amt"]["op"]]
            elif variant == "add":
                v2["amt"] = self._new_amt(rng)
            else:
                del v2["amt"]
        elif kind == "alt":
            clause = "alt"
            if variant == "value":
                v2["alt"]["k"] = rng.choice([k for k in dom.conds if k != v1["alt"]["k"]])
            elif variant == "add":
                v2["alt"] = {"k": rng.choice(dom.conds)}
            else:
                del v2["alt"]
        elif kind == "excl":
            clause = "exc"
            blocked = {v2["ovc"]["c"]} if "ovc" in v2 else set()
            if variant == "value":
                c = [x for x in dom.cats if x != v1["exc"]["c"] and x not in blocked]
                if not c:
                    return None
                v2["exc"]["c"] = rng.choice(c)
            elif variant == "add":
                v2["exc"] = {"c": rng.choice([x for x in dom.cats if x not in blocked])}
            else:
                del v2["exc"]
        elif kind == "override":
            clause = otype
            if variant == "value":
                o = v2[otype]
                if otype == "ovc":
                    sub = rng.choice(("cat", "n"))
                    if sub == "cat":
                        c = [x for x in dom.cats if x != o["c"] and not ("exc" in v2 and v2["exc"]["c"] == x)]
                        o["c"] = rng.choice(c)
                else:
                    sub = rng.choice(("range", "n"))
                if sub == "n":
                    o["n"] = rng.choice([n for n in SPECIAL_LIMITS if n not in (o["n"], v2["win"]["n"])])
            elif variant == "add":
                v2[otype] = self._new_ovr(rng, dom, otype, v2)
            else:
                del v2[otype]
        return v1, v2, {"kind": kind, "clause": clause, "variant": variant, "sub": sub}

    def _range(self, rng, day: dt.date, boost: bool) -> tuple:
        """A date window of a special clause: covering `day` (half the draws) or missing it, edges near the day."""
        if rng.random() < 0.5:
            pool = RANGE_IN_BOOST if boost else RANGE_IN
            return day - dt.timedelta(days=rng.choice(pool)), day + dt.timedelta(days=rng.choice(pool))
        dist = dt.timedelta(days=rng.choice(RANGE_OUT_BOOST if boost else RANGE_OUT))
        width = dt.timedelta(days=rng.randrange(3, 31))
        if rng.random() < 0.5:
            return day - dist - width, day - dist
        return day + dist, day + dist + width

    def _case(self, rng, dom, v1, v2, edit, boost):
        """One proposal of case values (boundary-biased), with the special clauses' date windows."""
        w1, w2 = _copy(v1), _copy(v2)
        vs = (w1, w2)
        named_c = sorted({ver[k]["c"] for ver in vs for k in ("exc", "ovc") if k in ver})
        named_k = sorted({ver["alt"]["k"] for ver in vs if "alt" in ver})
        cat = rng.choice(named_c) if named_c and rng.random() < 0.55 else rng.choice(dom.cats)
        cond = rng.choice(named_k) if named_k and rng.random() < 0.5 else rng.choice(dom.conds)
        xs = sorted({ver["amt"]["x"] for ver in vs if "amt" in ver})
        if xs:
            amount = rng.choice(xs) + rng.choice(AMOUNT_OFFSETS_BOOST if boost else AMOUNT_OFFSETS)
        else:
            amount = rng.choice(AMOUNTS) + rng.randrange(-400, 400)
        amount = max(1, amount)
        limits = sorted({ver["win"]["n"] for ver in vs} | {ver[o]["n"] for ver in vs for o in ("ovc", "ovd")
                                                           if o in ver})
        ka = max(0, rng.choice(limits) + rng.choice(DAY_OFFSETS_BOOST if boost else DAY_OFFSETS))
        a = rng.choice(sorted({ver["win"]["a"] for ver in vs}))
        gap = rng.choice(GAPS)
        k1, k2 = (ka, max(0, ka - gap)) if a == 0 else (ka + gap, ka)
        req = FIRST_DAY + dt.timedelta(days=rng.randrange(SPAN_DAYS))
        case = {"cat": cat, "cond": cond, "amount": amount,
                "d": (req - dt.timedelta(days=k1), req - dt.timedelta(days=k2)), "req": req}
        o1, o2 = w1.get("ovd"), w2.get("ovd")
        if o1 or o2:
            o = o1 or o2
            r = self._range(rng, case["d"][o["a"]], boost)
            for ow in (o1, o2):
                if ow:
                    ow["s"], ow["e"] = r
            if o1 and o2 and edit["sub"] == "range":
                r2 = self._range(rng, case["d"][o["a"]], boost)
                if r2 == r:
                    return None
                o2["s"], o2["e"] = r2
        return w1, w2, case

    def _forms_plan(self, rng, v1, v2, edit) -> tuple:
        """Lexicon form of every clause. V2 keeps V1's form unless a clause is reworded (cosmetic: 1-2 clauses;
        otherwise one other clause on 45% of rows and the edited clause itself on 25%); label-blind draws."""
        f1 = {k: rng.choice(self.admitted_forms(sem_of(k, p))) for k, p in sorted(v1.items())}
        f2 = {}
        for k, p in sorted(v2.items()):
            same_sem = k in v1 and sem_of(k, v1[k]) == sem_of(k, p)
            f2[k] = f1[k] if same_sem else rng.choice(self.admitted_forms(sem_of(k, p)))
        shared = sorted(k for k in v2 if k in v1 and f2[k] == f1[k])
        if edit["kind"] == "cosmetic":
            pick = rng.sample(shared, min(1 if rng.random() < 0.6 else 2, len(shared)))
        else:
            others = [k for k in shared if k != edit["clause"]]
            pick = [rng.choice(others)] if others and rng.random() < 0.45 else []
            if edit["clause"] in shared and rng.random() < 0.25:
                pick.append(edit["clause"])
        for k in pick:
            alts = [f for f in self.admitted_forms(sem_of(k, v2[k])) if f != f1[k]]
            if alts:
                f2[k] = rng.choice(alts)
        return f1, f2

    def _orders(self, rng, v1, v2, edit) -> tuple:
        order1 = sorted(v1)
        rng.shuffle(order1)
        order2 = [k for k in order1 if k in v2]
        for k in sorted(set(v2) - set(v1)):
            order2.insert(rng.randrange(len(order2) + 1), k)
        if len(order2) >= 2 and rng.random() < (0.35 if edit["kind"] == "cosmetic" else 0.15):
            i = rng.randrange(len(order2) - 1)
            order2[i], order2[i + 1] = order2[i + 1], order2[i]
        return order1, order2

    def _slots(self, rng, dom, v1, v2, f1, f2, case) -> dict:
        cats, conds = {c: [c] for c in dom.cats}, {k: [k] for k in dom.conds}
        fields, outs, label = {d: [d] for d in dom.dates}, {o: [o] for o in dom.outcomes}, {dom.amount: [dom.amount]}
        s = {"CUSTOMER": S.name_slot(rng.choice(CUSTOMERS)),
             "CASE_ID": S.id_slot(f"{dom.prefix}-{rng.randrange(10000, 100000)}"),
             "CAT": S.category_slot(case["cat"], cats), "COND": S.category_slot(case["cond"], conds),
             "AMOUNT": S.cents_slot(case["amount"]), "D1": S.date_slot(case["d"][0]),
             "D2": S.date_slot(case["d"][1]), "REQ": S.date_slot(case["req"])}
        for v, ver, fm in ((1, v1, f1), (2, v2, f2)):
            for kind, p in ver.items():
                if kind == "win":
                    ps = {"N": S.count_slot(p["n"], UNIT_DAY), "A": S.category_slot(dom.dates[p["a"]], fields)}
                elif kind == "amt":
                    ps = {"M": S.category_slot(dom.amount, label), "X": S.cents_slot(p["x"])}
                elif kind == "exc":
                    ps = {"C": S.category_slot(p["c"], cats)}
                elif kind == "alt":
                    ps = {"K": S.category_slot(p["k"], conds), "O": S.category_slot(dom.outcomes[1], outs)}
                elif kind == "ovc":
                    ps = {"C": S.category_slot(p["c"], cats), "N": S.count_slot(p["n"], UNIT_DAY)}
                else:
                    ps = {"A": S.category_slot(dom.dates[p["a"]], fields), "S": S.date_slot(p["s"]),
                          "E": S.date_slot(p["e"]), "N": S.count_slot(p["n"], UNIT_DAY)}
                for name, slot in ps.items():
                    s[sn(v, kind, name)] = slot
                s[sn(v, kind)] = self.lexicon.clause(fm[kind], bind={name: sn(v, kind, name) for name in ps})
        return s

    def derive(self, spec: Spec) -> Spec:
        e = spec.slots
        k1 = (e["REQ"].value - e["D1"].value).days
        k2 = (e["REQ"].value - e["D2"].value).days
        spec = spec.replace(derived={"DAYS1": S.count_slot(k1, UNIT_DAY), "DAYS2": S.count_slot(k2, UNIT_DAY)},
                            derived_deps={"DAYS1": ("D1", "REQ"), "DAYS2": ("D2", "REQ")})
        kinds = set(spec.structure["v1"]) | set(spec.structure["v2"])
        deep = {"amt", "exc", "alt"} <= kinds and bool(kinds & {"ovc", "ovd"})
        return spec.replace(tags=self.trap_tags(spec), deep=deep)

    def trap_tags(self, spec: Spec) -> tuple:
        """Trap tags (spec 3.12 trap table; G0_SPEC.md section 2), recomputed for every spec, twins included."""
        dom, v1, v2, case = facts(spec)
        edit = spec.structure["edit"]
        kind = edit["kind"]
        mode = mode_of(kind, v1, v2, case)
        tags = {f"edit_{kind}", f"variant_{edit['variant']}", f"mode_{mode}"}
        if mode in ("cosmetic", "untouched"):
            tags.add("cosmetic_or_irrelevant")
        if kind == "anchor" and mode == "flip":
            tags.add("anchor_flip")
        if kind == "override" and mode == "untouched" and "ovd" in set(v1) | set(v2):
            tags.add("date_scope_excludes_case")
        for ver in (v1, v2):
            lim = ver[_ovr_kind(ver)]["n"] if _ovr_kind(ver) and _covers(ver, case) else ver["win"]["n"]
            if (case["req"] - case["d"][ver["win"]["a"]]).days - lim in (0, 1):
                tags.add("boundary_day")
            if "amt" in ver and abs(case["amount"] - ver["amt"]["x"]) <= 1:
                tags.add("boundary_amount")
            if "ovd" in ver and case["d"][ver["ovd"]["a"]] in (ver["ovd"]["s"], ver["ovd"]["e"],
                                                               ver["ovd"]["s"] - dt.timedelta(days=1),
                                                               ver["ovd"]["e"] + dt.timedelta(days=1)):
                tags.add("boundary_window")
        return tuple(sorted(tags))

    # ------------------------------------------------------------------------------------------- solver A
    def solve_a(self, spec: Spec):
        return _answer(spec.qform, outcome_a(spec, 1), outcome_a(spec, 2))

    def canonical(self, spec: Spec) -> dict:
        env = spec.env()
        dom = DOMAINS[spec.structure["domain"]]
        iso = lambda name: env[name].isoformat()      # noqa: E731
        vs = {}
        for v in (1, 2):
            ver = {}
            for kind in spec.structure[f"v{v}"]:
                g = lambda p: env[sn(v, kind, p)]      # noqa: E731
                if kind == "win":
                    ver[kind] = {"n": g("N"), "anchor": g("A")}
                elif kind == "amt":
                    ver[kind] = {"op": env[sn(v, kind)].rsplit(".", 1)[1], "x": g("X"), "label": g("M")}
                elif kind == "exc":
                    ver[kind] = {"cat": g("C")}
                elif kind == "alt":
                    ver[kind] = {"cond": g("K"), "outcome": g("O")}
                elif kind == "ovc":
                    ver[kind] = {"cat": g("C"), "n": g("N")}
                else:
                    ver[kind] = {"field": g("A"), "start": iso(sn(v, kind, "S")), "end": iso(sn(v, kind, "E")),
                                 "n": g("N")}
            vs[v] = ver
        return {"title": dom.title,
                "vocab": {"cats": list(dom.cats), "conds": list(dom.conds), "outcomes": list(dom.outcomes)},
                "v1": vs[1], "v2": vs[2],
                "case": {"case_id": env["CASE_ID"], "category": env["CAT"], "condition": env["COND"],
                         "amount_label": dom.amount, "amount": env["AMOUNT"], "date_fields": list(dom.dates),
                         "d1": iso("D1"), "d2": iso("D2"), "req": iso("REQ"), "days1": env["DAYS1"],
                         "days2": env["DAYS2"]},
                "customer": env["CUSTOMER"], "qform": spec.qform}

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        c = self.canonical(spec)
        return c if author_mode == "T" else {k: v for k, v in c.items() if k != "customer"}

    def extract_view(self, spec: Spec) -> dict:
        return {"customer": spec.env()["CUSTOMER"]}

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        return [Field("customer", "name", "the person who raised the case, as written")]

    def version_asts(self, spec: Spec) -> tuple:
        """Solver A's two rule ASTs (cosmetic admission: rules.ast_equal on the pair)."""
        return version_rules(spec, 1), version_rules(spec, 2)

    # ------------------------------------------------------------------------------------------- skins, wordings
    def pick_skin(self, spec: Spec, ctx, held: bool):
        """The narrative skin of a unit (G0 v2.2 section 2, Skins): a stratified, label-blind deal instead of a hash
        draw, so that on a run of consecutive seeds no skin feeds more than a few rows (spec 3.0: <= 6) and no
        register exceeds 15% (pilot report_only: skin_max_rows 10, register 15.7%). The unit index g (seed, sampler)
        picks the register round robin over a seeded register order and, inside it, the (g // R)-th skin of a seeded
        skin order, Mode T skins and Mode F documents alike. Seed and sampler only: never the question form, the
        gold or the generation order, so a unit renders the same alone or in a run."""
        samplers = TRAIN_SAMPLERS if spec.sampler in TRAIN_SAMPLERS else (spec.sampler,)
        g = spec.seed * len(samplers) + samplers.index(spec.sampler)
        cache = self.__dict__.setdefault("_skin_deal", {})
        hit = cache.get(held)
        if hit is None or hit[0] is not ctx:
            pool = [x for x in ctx.skins.values() if x.family == FAMILY and x.kind == "skin" and x.held_out == held]
            if not pool:
                raise LookupError(f"no skin for {FAMILY} (held_out={held})")
            regs = sorted({x.register for x in pool}, key=lambda r: uhash(FAMILY, "register_order", held, r))
            by_reg = {r: sorted((x for x in pool if x.register == r),
                                key=lambda x: uhash(FAMILY, "skin_order", held, x.skin_id)) for r in regs}
            hit = cache[held] = (ctx, regs, by_reg)
        _ctx, regs, by_reg = hit
        lst = by_reg[regs[g % len(regs)]]
        return lst[(g // len(regs)) % len(lst)]

    def _screened_ctx(self, ctx):
        """The kit context without the wordings that fail the polarity rule or carry a lead ruling (ctx_for)."""
        for c, screened, _bad in self._screened:
            if c is ctx or screened is ctx:
                return screened
        screened, bad = POL.screen(ctx, self)
        drop = {sid for sid, sk in screened.skins.items() if sk.kind == "wording" and sk.text in QUARANTINED_WORDINGS}
        if drop:
            screened = type(screened)(skins={k: v for k, v in screened.skins.items() if k not in drop},
                                      lexicon=screened.lexicon)
            bad = {**bad, **{sid: [QUARANTINED_WORDINGS[ctx.skins[sid].text]] for sid in drop}}
        self._screened.append((ctx, screened, bad))
        return screened

    def ctx_for(self, spec: Spec, ctx):
        """Pipeline hook: the context a unit renders with (so a complement partner never picks a screened wording)."""
        return self._screened_ctx(ctx)

    def quarantined_wordings(self, ctx) -> dict:
        """{wording skin id: problems} the screen kept out of `ctx` (polarity rule P1-P3 and the lead's rulings)."""
        self._screened_ctx(ctx)
        return next(bad for c, _s, bad in self._screened if c is ctx)

    # ------------------------------------------------------------------------------------------- render
    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        if attack is not None:
            raise ContractError("T24 v1 has no attack twins (everyday tier)")
        key = f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        ctx = self._screened_ctx(ctx)
        skin = skin or self.pick_skin(spec, ctx, held)
        if wording is None:                     # S5 prefers held-out wordings (mixdev); training rows never use them
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
        dom = DOMAINS[spec.structure["domain"]]
        tb = TextBuilder()
        for i, block in enumerate(spec.structure["blocks"]):
            if i:
                tb.add("state", "\n\n")
            if block == "narr":
                tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id)
            elif block == "versions":
                tb.add("state", K.fill(versions_template(spec), slots, forms))
            else:
                tb.add("state", K.fill(record_template(dom), slots, forms))
        style = card_style(spec)
        placed = CD.place_rules(tb, rules_text(dom, style), self.QFORMS[spec.qform].qtype)   # yes/no: row.card (once)
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if spec.qform == "ch_v2":
            kinds = set(spec.structure["v1"]) | set(spec.structure["v2"])
            keys = list(ROLES) if "alt" in kinds else ["pos", "neg"]
            os_ = build_closed(spec, ans, self._option_order(spec, key, keys), self.error_models(), row_key=key,
                               order="fixed", render_key=lambda r: dom.outcomes[ROLES.index(r)])
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            format_style=f"{skin.register}/{spec.structure['container']}",
                            defs_style=CD.defs_style(placed, style))

    def _option_order(self, spec: Spec, key: str, keys: list) -> list:
        """Option order of a ch_v2 row (kit choiceplan position). A twin must show the base row's option list in the
        same order (G-TW), so the order cannot follow the gold: it puts the DEALT role (a function of the seed, which
        a base row's gold always equals) at plan_choice's planned position and the other roles in their seeded
        order. A base row's gold is therefore at the planned position (uniform in each k); a twin's gold sits where
        its role falls in the same order. A spec the sampler did not deal (hand-built) keeps the seeded shuffle."""
        k, role = _share(CELLS, _weyl(spec.seed, spec.sampler, 4))
        if k != len(keys) or role not in keys:
            return sorted(keys, key=lambda r: uhash(key, "closed", repr(r)))
        pos = plan_choice(key, closed=len(keys)).pos
        others = sorted((r for r in keys if r != role), key=lambda r: uhash(key, "closed", repr(r)))
        return others[:pos] + [role] + others[pos:]

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        out = []
        if self.QFORMS[spec.qform].qtype == "noul" and uhash(FAMILY, "complement", spec.sampler, spec.seed) < COMP_RATE:
            out.append(RelationProposal("complement", qform=self.partner(spec)))
        if uhash(FAMILY, "equiv", spec.sampler, spec.seed) < EQUIV_RATE:
            st = dict(spec.structure, container=EQUIV_CONTAINER[spec.structure["container"]])
            out.append(RelationProposal("equiv", spec=spec.replace(structure=st), note="another skin and container"))
        if uhash(FAMILY, "twin", spec.sampler, spec.seed) < TWIN_RATE:
            t = self.twin(spec)
            if t is not None:
                out.append(t)
        return out + self.metamorphic(spec)

    def partner(self, spec: Spec) -> str:
        """The complement form: same predicate, opposite polarity, a negcount-legal pair (G0_SPEC.md R16)."""
        u = uhash(FAMILY, "complement_kind", spec.sampler, spec.seed)
        return {"yn_changes": "yn_same" if u < 0.5 else ("yn_not_change" if u < 0.75 else "yn_fail_change"),
                "yn_dneg": "yn_not_change", "yn_same": "yn_changes", "yn_fail_change": "yn_changes",
                "yn_not_change": "yn_changes" if u < 0.6 else "yn_dneg"}[spec.qform]

    def twin(self, spec: Spec):
        """Minimal-edit twin: exactly one input slot moves (request date, amount, category, condition, or the revised
        value of the edited clause); the predicted answer comes from the edited construction (direct_outcome), never
        from solve_a. The first candidate (seeded order) whose answer differs is used (ch_v2: the first that reaches
        the drawn target role, twin_role; the first differing one only when none does)."""
        dom, v1, v2, case = facts(spec)
        base = predict(spec.qform, v1, v2, case)
        edit = spec.structure["edit"]
        cands = []
        days = [(case["req"] - d).days for d in case["d"]]
        limits = sorted({ver["win"]["n"] for ver in (v1, v2)} | {ver[o]["n"] for ver in (v1, v2)
                                                                 for o in ("ovc", "ovd") if o in ver})
        for lim in limits:
            for a in (0, 1):
                for target in (lim, lim + 1):
                    shift = target - days[a]
                    if shift and days[1] + shift >= 0:
                        cands.append(("request", "REQ", case["req"] + dt.timedelta(days=shift)))
        for ver in (v1, v2):
            if "amt" in ver:
                for amt in (ver["amt"]["x"] - 1, ver["amt"]["x"], ver["amt"]["x"] + 1):
                    if amt >= 1 and amt != case["amount"]:
                        cands.append(("amount", "AMOUNT", amt))
        cands += [("category", "CAT", c) for c in dom.cats if c != case["cat"]]
        cands += [("condition", "COND", k) for k in dom.conds if k != case["cond"]]
        if edit["variant"] == "value" and edit["kind"] in ("limit", "amount", "override"):
            if edit["kind"] == "limit":
                ov = _ovr_kind(v2)
                cands += [("revised", "V2_WIN_N", n) for n in LIMITS
                          if n not in (v1["win"]["n"], v2["win"]["n"]) and not (ov and n == v2[ov]["n"])]
            elif edit["kind"] == "amount":
                cands += [("revised", "V2_AMT_X", x) for x in (case["amount"] - 1, case["amount"], case["amount"] + 1)
                          if x >= 1 and x not in (v1["amt"]["x"], v2["amt"]["x"])]
            elif edit["sub"] == "n":
                o = edit["clause"]
                cands += [("revised", sn(2, o, "N"), n) for n in SPECIAL_LIMITS
                          if n not in (v1[o]["n"], v2[o]["n"], v2["win"]["n"])]
        kinds = sorted({c[0] for c in cands}, key=lambda k: uhash(FAMILY, "twin_kind", spec.sampler, spec.seed, k))
        rank = {k: i for i, k in enumerate(kinds)}
        cands.sort(key=lambda c: (rank[c[0]], uhash(FAMILY, "twin_cand", spec.sampler, spec.seed, c[1], repr(c[2]))))
        target = self.twin_role(spec, v2, base) if spec.qform == "ch_v2" else None
        fallback = None
        for what, name, val in cands:
            t1, t2, tc = _copy(v1), _copy(v2), dict(case)
            if name == "REQ":
                tc["req"] = val
                slot = S.date_slot(val)
            elif name == "AMOUNT":
                tc["amount"] = val
                slot = S.cents_slot(val)
            elif name == "CAT":
                tc["cat"] = val
                slot = S.category_slot(val, {c: [c] for c in dom.cats})
            elif name == "COND":
                tc["cond"] = val
                slot = S.category_slot(val, {k: [k] for k in dom.conds})
            elif name == "V2_AMT_X":
                t2["amt"]["x"] = val
                slot = S.cents_slot(val)
            else:
                t2["win" if name == "V2_WIN_N" else edit["clause"]]["n"] = val
                slot = S.count_slot(val, UNIT_DAY)
            pred = predict(spec.qform, t1, t2, tc)
            if pred != base:
                prop = RelationProposal("twin", spec=spec.with_slot(name, slot), changed_slot=name, expect=pred,
                                        note=f"twin {what}")
                if target is None or pred == target:
                    return prop
                fallback = fallback or prop            # ch_v2: no candidate reaches the target role
        return fallback

    def twin_role(self, spec: Spec, v2: dict, base: str) -> str:
        """ch_v2 twin target (F3): the role the twin's gold should take, drawn label-blind from the spec's own key,
        uniform over the roles the revised version can give other than the base row's (alt only when the revised
        version holds a condition clause). plugin.twin takes the first candidate in the seeded order that reaches it,
        so the twin rows are as balanced over the roles as the base rows (G6 role prior)."""
        roles = [r for r in ROLES if r != base and (r != "alt" or "alt" in v2)]
        return roles[int(uhash(FAMILY, "twin_role", spec.sampler, spec.seed) * len(roles))]

    def metamorphic(self, spec: Spec) -> list:
        """G4 (checked, never emitted): each transformation keeps the answer by construction."""
        env = spec.env()
        out = [RelationProposal("metamorphic", spec=spec.with_slot(
            "CUSTOMER", S.name_slot(next(n for n in CUSTOMERS if n != env["CUSTOMER"]))), expect="same",
            note="rename the customer")]
        shift = dt.timedelta(days=35)
        out.append(RelationProposal("metamorphic", spec=spec.replace(slots={
            k: (S.date_slot(s.value + shift) if s.kind == "date" else s) for k, s in spec.slots.items()}),
            expect="same", note="shift every date"))
        out.append(RelationProposal("metamorphic", spec=spec.replace(slots={
            k: (S.cents_slot(s.value + 100) if s.kind == "cents" else s) for k, s in spec.slots.items()}),
            expect="same", note="shift every amount"))
        o2 = list(spec.structure["v2"])
        if len(o2) >= 2:
            out.append(RelationProposal("metamorphic", spec=spec.replace(structure=dict(spec.structure,
                                                                                          v2=o2[1:] + o2[:1])),
                                        expect="same", note="reorder the revised version"))
        dom, v1, v2, case = facts(spec)
        named = {ver[k]["c"] for ver in (v1, v2) for k in ("exc", "ovc") if k in ver}
        if case["cat"] not in named:
            free = [c for c in dom.cats if c not in named and c != case["cat"]]
            if free:
                out.append(RelationProposal("metamorphic", spec=spec.with_slot(
                    "CAT", S.category_slot(free[0], {c: [c] for c in dom.cats})), expect="same",
                    note="swap an unmentioned category"))
        return out

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def on_v2(fn):
            def run(spec):
                if spec.qform != "ch_v2":
                    return None
                dom, v1, v2, case = facts(spec)
                return fn(spec, v1, v2, case)
            return run

        def mistake(m, needs=None):
            return on_v2(lambda spec, v1, v2, case: direct_outcome(v2, case, m)
                         if needs is None or needs(spec, v2) else None)

        def neg_form(spec, v2):
            return "amt" in v2 and "do not qualify" in spec.slots[sn(2, "amt")].value[2]

        def kept(spec, v1, v2, case):
            merged = _copy(v2)
            for k, p in v1.items():
                if k not in merged and not (k in ("ovc", "ovd") and _ovr_kind(merged)):
                    merged[k] = dict(p)
            return direct_outcome(merged, case) if merged != v2 else None

        def misread(spec, v1, v2, case):
            if not neg_form(spec, v2):
                return None
            return direct_outcome(v2, case, {"op": OP_MISREAD[v2["amt"]["op"]]})

        models = {
            "t24_original_version": on_v2(lambda spec, v1, v2, case: direct_outcome(v1, case)),
            "wrong_anchor": mistake({"swap_anchor": True}),
            "count_day0": mistake({"day0": True}),
            "off_by_one_late": mistake({"late1": True}),
            "ignore_exception": mistake({"no_alt": True}, lambda spec, v2: "alt" in v2),
            "t24_ignore_special_limit": mistake({"no_special": True}, lambda spec, v2: _ovr_kind(v2) is not None),
            "t24_special_date_as_anchor": mistake({"special_anchor": True}, lambda spec, v2: "ovd" in v2),
            "t24_ignore_exclusion": mistake({"no_exc": True}, lambda spec, v2: "exc" in v2),
            "t24_ignore_amount_rule": mistake({"no_amt": True}, lambda spec, v2: "amt" in v2),
            "drop_inclusive_endpoint": on_v2(lambda spec, v1, v2, case: direct_outcome(
                v2, case, {"op": OP_FLIP[v2["amt"]["op"]]}) if "amt" in v2 and v2["amt"]["op"] in ("ge", "le")
                else None),
            "add_exclusive_endpoint": on_v2(lambda spec, v1, v2, case: direct_outcome(
                v2, case, {"op": OP_FLIP[v2["amt"]["op"]]}) if "amt" in v2 and v2["amt"]["op"] in ("gt", "lt")
                else None),
            "t24_negative_rule_misread": on_v2(misread),
            "t24_ignore_time_limit": mistake({"no_late": True}),
            "t24_condition_before_gates": mistake({"alt_first": True}, lambda spec, v2: "alt" in v2),
            "t24_condition_scope_ignored": mistake({"alt_any": True}, lambda spec, v2: "alt" in v2),
            "t24_special_limit_for_all": mistake({"special_all": True}, lambda spec, v2: _ovr_kind(v2) is not None),
            "t24_removed_clause_kept": on_v2(kept),
            "t24_default_outcome": mistake({"no_exc": True, "no_late": True, "no_amt": True}),
            "t24_amount_rule_reversed": on_v2(lambda spec, v1, v2, case: direct_outcome(
                v2, case, {"op": OP_REVERSE[v2["amt"]["op"]]}) if "amt" in v2 else None),
            "t24_qualifies_in_full": mistake({"pos_always": True}),
            "t24_alternative_as_fallback": mistake({"alt_fallback": True}, lambda spec, v2: "alt" in v2),
            "t24_condition_as_exclusion": mistake({"alt_as_neg": True}, lambda spec, v2: "alt" in v2),
        }
        return {k: error_model(k, fn) for k, fn in models.items()}
