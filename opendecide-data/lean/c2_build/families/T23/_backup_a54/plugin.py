"""families/T23/plugin.py: T23 "governing version under transition clauses" (C2_DATA_SPEC 2.1 T23, 3.11; G0_SPEC.md
frozen, sha below).

One rule document in 2-4 versions (start dates, tiled windows, "replaces" pointers, one term value each) and one case
(purchase <= event <= filing <= decision dates, one printed quantity). The card's anchor date picks the default
version; at most one clause (grandfather / prospective keep-old, retroactive, sunset) may move the case to another
version (G0 R1-R9; R = semantic items, S1-S5 = samplers).

  solver A   rule engine: one kit rule AST per version window and per clause condition (rules.Cmp / And / Fn over
             the date slots), run by rules.evaluate, then the default + clause step            paradigm rule_engine
  solver B   solver_b.py: its own parser of the rendered row, an in-memory sqlite table, a SQL window filter on
             julianday (chain windows by a self-join on "replaces"), a separately coded clause rule and a governs
             flag for every version                                                             paradigm sql_sqlite
  status     a third, construction-only table (_status / _decide: start dates, case dates, the clause and SUNSET, the
             terms and Q; windows from the start dates only, never the printed ends or a rule AST): it steers the
             samplers and predicts minimal-edit twins, never the gold
  samplers   S1 forward (list); S2 near-miss edges (list); S3 version table first (table); S4 narrative over a pasted
             change log (log); S5 held out (table / log, held-out skins and registers; mixdev only)
  questions  ch_version, ch_term (open sets from error models); yn_version (+ other / not), yn_claim (+ contra / not),
             yn_outcome (+ out / not)
  relations  complement, minimal-edit twin, equiv, inv, G4 metamorphic (renames, a common date shift)
Pools below (domain packs, customers, organisations, items) are Claude-written stand-ins until the Haiku packs exist
(after A38); they live in code and nothing here writes a file.

G0 v4 (Stage B pilot fix iteration 1, 14 Oct 2026; PILOT_VERDICT FIX-1 to FIX-4 + the kit-level fixes):
  FIX-1  ctx_for(): a double-negation wording is never picked for a row whose complement is non-syntactic (antonym /
         implicit) - the partner would differ by two negation cues; the polarity screen (c2_kit.polarity) also keeps
         every wording that does not read with its form's polarity out of the pool, and the 13 double-negation
         wordings of the shape "aux + subject + not + a ... that does not ..." (negated question frame, G0 10)
  FIX-2  yn_version has the syntactic complement only (no admitted yn_version_other wording carries the one implicit
         cue G-TW needs); the form stays declared and checked by the G2 / G3 tests, it is just never proposed
  FIX-3  _pick_skin(): the author mode is drawn from the row key first (Mode F 20%), then the register (weights keep
         every register under the 15% cap), then a skin of that mode
  FIX-4  length: the card is cut to the rules the row needs (CardItem.when: the clause lines only when a clause is
         printed, the within / claim line only on outcome / claim questions) and yes/no rows carry it in row.card
         (printed once; cards.place_rules), choice rows keep it in the instructions
"""
from __future__ import annotations

import dataclasses
import datetime as dt
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import cards as CK  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import rules as RL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.distractors import build_options, error_model, register_name, uhash  # noqa: E402
from c2_kit.plugin import (C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec,  # noqa: E402
                           choose_forms)
from c2_kit.rows import TextBuilder, assemble_row  # noqa: E402

HERE = Path(__file__).resolve().parent
FAMILY = "T23"
DAY = dt.timedelta(days=1)
MAX_TRIES = 400
FIRST_DAY = dt.date(2023, 1, 2)

# ------------------------------------------------------------------------------------------------ roles and packs
ROLES = ("PURCHASE_DATE", "EVENT_DATE", "FILING_DATE", "DECISION_DATE")       # P <= EV <= F <= DEC (G0 R4)
ROLE_NAME = {"PURCHASE_DATE": "purchase", "EVENT_DATE": "event", "FILING_DATE": "filing",
             "DECISION_DATE": "decision"}
LABEL_SLOT = {"PURCHASE_DATE": "PURCHASE_LABEL", "EVENT_DATE": "EVENT_LABEL", "FILING_DATE": "FILING_LABEL",
              "DECISION_DATE": "DECISION_LABEL"}
ANCHORS = ("PURCHASE_DATE", "EVENT_DATE", "FILING_DATE")
UNITS = {"days": ("day", "days"), "devices": ("device", "devices")}


@dataclass(frozen=True)
class Pack:
    doc: str
    term: str
    tkind: str                  # days | cents | devices
    pool: tuple
    qty: str
    pair: tuple | None          # (from role, to role): Q is a printed day count; None: Q is an input amount / count
    labels: tuple               # purchase / event / filing / decision date labels
    items: tuple
    prefix: str                 # version code prefix


DOMAINS = {   # G0 section 7 (stand-ins for the Haiku packs)
    "refunds": Pack("refund policy", "refund window", "days", (7, 10, 14, 21, 28, 30, 45, 60, 90),
                    "day count from purchase to refund request", ("PURCHASE_DATE", "FILING_DATE"),
                    ("purchase date", "delivery date", "refund request date", "decision date"),
                    ("annual plan", "standing desk", "camera bag", "language course"), "RP"),
    "warranties": Pack("warranty terms", "warranty period", "days", (30, 60, 90, 180, 365, 730),
                       "day count from purchase to fault", ("PURCHASE_DATE", "EVENT_DATE"),
                       ("purchase date", "fault date", "claim date", "decision date"),
                       ("washing machine", "laptop", "e-bike", "coffee grinder"), "WT"),
    "fees": Pack("fee schedule", "fee cap", "cents", (1500, 2000, 2500, 3500, 4000, 5000, 7500), "fee charged", None,
                 ("account opening date", "billing date", "dispute date", "decision date"),
                 ("current account", "card account", "savings account", "merchant account"), "FS"),
    "leave": Pack("leave policy", "paid leave allowance", "days", (10, 12, 15, 20, 25, 30),
                  "number of leave days claimed", None, ("hire date", "leave start date", "claim date", "decision date"),
                  ("summer trip", "family visit", "study block", "house move"), "LP"),
    "subscriptions": Pack("subscription terms", "free cancellation period", "days", (3, 5, 7, 14, 21, 30),
                          "day count from sign-up to cancellation", ("PURCHASE_DATE", "FILING_DATE"),
                          ("sign-up date", "renewal date", "cancellation date", "decision date"),
                          ("streaming plan", "meal kit plan", "gym membership", "news subscription"), "ST"),
    "shipping": Pack("shipping policy", "delivery promise", "days", (2, 3, 4, 5, 7, 10, 14),
                     "day count from order to delivery", ("PURCHASE_DATE", "EVENT_DATE"),
                     ("order date", "delivery date", "complaint date", "decision date"),
                     ("sofa order", "printer order", "grocery order", "tyre order"), "SP"),
    "retention": Pack("records retention schedule", "retention period", "days", (30, 60, 90, 180, 365, 730),
                      "day count from record closure to deletion request", ("EVENT_DATE", "FILING_DATE"),
                      ("record creation date", "record closure date", "deletion request date", "decision date"),
                      ("customer file", "payroll record", "support transcript", "camera recording"), "RS"),
    "pricing": Pack("price list", "price cap per unit", "cents", (1250, 1499, 1999, 2400, 2999, 3500),
                    "unit price charged", None, ("contract date", "delivery date", "invoice date", "decision date"),
                    ("printer toner", "office chair", "safety boot", "cable reel"), "PL"),
    "travel": Pack("travel policy", "nightly hotel cap", "cents", (12000, 15000, 17500, 20000, 25000),
                   "nightly rate claimed", None, ("booking date", "travel date", "expense claim date", "decision date"),
                   ("conference trip", "client visit", "site audit", "team offsite"), "TP"),
    "licences": Pack("licence terms", "device limit", "devices", (1, 2, 3, 5, 10), "number of devices registered", None,
                     ("licence purchase date", "activation date", "support request date", "decision date"),
                     ("design suite", "antivirus licence", "notes app", "photo editor"), "LT"),
}
DOMAIN_KEYS = tuple(DOMAINS)
CUSTOMERS = ("Priya Raman", "Tomas Lindqvist", "Ana Ruiz", "Dana Okafor", "Lena Whitcombe", "Ravi Anand",
             "Mira Castell", "Aiko Brandt", "Jonas Feld", "Nadia Kowal", "Owen Pryce", "Sara Ilves", "Malik Osei",
             "Ines Duarte", "Kofi Mensah", "Hana Sato", "Lucas Brenner", "Eva Marsh", "Theo Kalnins", "Yara Haddad")
ORGS = ("Lindenfeld Outfitters", "Brightwell Supply", "Corran Telecom", "Halvard Insurance", "Mistral Home",
        "Pembroke Travel", "Quayside Software", "Redfern Bank", "Selkirk Logistics", "Tamsin Fitness",
        "Upland Utilities", "Veridia Health")
RESERVE_CUSTOMERS = ("Quinn Arbeloa", "Rosa Templeton")       # G4 renames only
RESERVE_ORGS = ("Wexford Mutual", "Yarrow Retail")
RESERVE_IDS = ("rev-X", "rev-Y", "ZZ-901")

# ------------------------------------------------------------------------------------------------ card text (G0 1.1)
CLOSED_WORLD = ("Only the listed versions, clauses and case facts count, and they are complete: no other version, "
                "clause or fact exists.")
WINDOW_RULE = {     # G0 1.1 (v2: the excl rule says "the day before", never "up to": ambiguity pass H7)
    "incl": "A version is in force from its start date through its end date, both dates included; an open-ended "
            "version stays in force.",
    "excl": "A version is in force from its start date through the day before its end date; an open-ended version "
            "stays in force.",
    "chain": "A version is in force from its start date until the version that replaces it takes effect, and on that "
             "start date the new version is in force.",
}
# Card items (G0 1.1, v4): the v3 sentences, each shown only on the rows whose rules it can change. A clause line is
# printed with a clause in the record, the within line on outcome questions and the claim line on claim questions (all
# VISIBLE inputs, never the gold; cards.CardItem.when). Placement: yes/no rows carry the card in row.card (the served
# prompt prints it once), choice rows in the instructions (cards.place_rules). The v3 card (one fixed text, 232
# tokens, printed twice) is kept in test_plugin.py as the reference of the marker check (cards.variant_problems).
def _has_clause(spec: Spec) -> bool:
    return spec.structure["clause"] is not None


CARD_TITLE = "Finding the version of the {DOC} that governs a case:"
CARD_SPEC = CK.CardSpec(
    FAMILY,
    items=(
        CK.CardItem("default", "The governing version is the version in force on the case's {ANCHOR}.",
                       when=lambda s: not _has_clause(s)),
        CK.CardItem("default_clause", "Default: the version in force on the case's {ANCHOR}; \"would govern\" in "
                                         "a clause means this default.", when=_has_clause),
        CK.CardItem("window", "{WINDOW}"),
        CK.CardItem("clause", "At most one clause is printed: when its own condition holds, the version it points "
                                 "to governs, even if another version is in force on a later date; it is applied "
                                 "once, after the default.", when=_has_clause),
        CK.CardItem("dates", "An older version has an earlier start date. \"Before\" and \"after\" exclude the "
                                "date itself; \"on or before\" and \"on or after\" include it.", when=_has_clause),
        CK.CardItem("within", "The case is within the {TERM_LABEL} when its {QTY_LABEL} is at most the governing "
                                 "version's value, and outside it otherwise.",
                       when=lambda s: s.qform in OUTCOME_FORMS),
        CK.CardItem("claim", "A claim about the {TERM_LABEL} is supported when it states the governing version's "
                                "value, and contradicted otherwise.", when=lambda s: s.qform in CLAIM_FORMS),
    ),
    heads={"full": CARD_TITLE}, tail=CLOSED_WORLD, numbered=False)
END_MARK = {"incl": "end dates included", "excl": "end dates excluded"}      # G0 1.2 block marker (v2: H6)
CLAUSE_TPL = {
    "keep_old": "Transition clause of {{V{c}_ID}}: if {{V{c}_ID}} would govern a case whose {{{lab}}} is before "
                "{{V{c}_START}}, the version in force on that {{{lab}}} governs it instead.",
    "retro": "Transition clause of {{V{c}_ID}}: if a version older than {{V{c}_ID}} would govern a case whose "
             "{{DECISION_LABEL}} is on or after {{V{c}_START}}, {{V{c}_ID}} governs it instead.",
    "sunset": "Sunset clause of {{V{c}_ID}}: if {{V{c}_ID}} would govern a case whose {{DECISION_LABEL}} is after "
              "{{SUNSET}}, {{V{t}_ID}} governs it instead.",
}

# ------------------------------------------------------------------------------------------------ shares (G0 2-4, 6)
BASE_SHARES = (("ch_version", 0.32), ("ch_term", 0.24), ("yn_version", 0.15), ("yn_claim", 0.15),
               ("yn_outcome", 0.14))
SCENARIOS = (("none", 0.25), ("decisive", 0.32), ("tested", 0.13), ("foreign", 0.30))
CLAUSE_TYPES = (("grandfather", 0.30), ("prospective", 0.25), ("retroactive", 0.25), ("sunset", 0.20))
CLAUSE_KIND = {"grandfather": "keep_old", "prospective": "keep_old", "retroactive": "retro", "sunset": "sunset"}
KEEP_ROLE = {"grandfather": "PURCHASE_DATE", "prospective": "EVENT_DATE"}
# G0 v4 (FIX-2): yn_version proposes the syntactic complement only. yn_version_other (implicit: exactly one cue that
# negcount counts, no syntactic one) stays a declared form and is tested, but none of its 10 admitted training wordings
# carries a counted cue ("a different version from", "some version besides"), so G-TW failed on every such pair.
COMPLEMENTS = {"yn_version": (("yn_version_not", 1.0),),
               "yn_claim": (("yn_claim_contra", 0.6), ("yn_claim_not", 0.4)),
               "yn_outcome": (("yn_outcome_out", 0.6), ("yn_outcome_not", 0.4))}
P_COMPLEMENT, P_EQUIV, P_INV, P_TWIN = 0.6, 0.13, 0.05, 0.6
P_NEWEST = 0.6
# ch_version / ch_term options (G0 R14, R15; rank-cue fix): K = 2 on every row. The error models leave a single
# distinct wrong answer on about half of the rows, and a k lowered after a failed build leaks the gold (kit
# distractors.py: a family whose models are too thin for its k draws a smaller k for every row).
CHOICE_K = 2
CODE_LETTERS = "BCDFGHJKMPRTVWXZ"
SAMPLER_INDEX = {"S1": 0, "S2": 1, "S3": 2, "S4": 3, "S5": 4}
SAMPLER_STYLE = {"S1": "list", "S2": "list", "S3": "table", "S4": "log", "S5": None}   # S5: table / log by card
N_VERSIONS = {"S1": (2, 3, 3, 4), "S2": (2, 3), "S3": (3, 4), "S4": (2, 3), "S5": (2, 3, 4)}
P_EDGE = {"S1": 0.25, "S2": 0.9, "S3": 0.25, "S4": 0.25, "S5": 0.25}
P_TERM_EDGE = {"S1": 0.25, "S2": 0.7, "S3": 0.25, "S4": 0.25, "S5": 0.25}
S4_REGISTERS = ("email", "chat", "transcript")
# G0 v4 (FIX-3): the author mode is drawn from the row key first (Mode F = free-form notes, G0 7: target 20%, bar 25%),
# then the register, then a skin of that mode. S4 draws only email / chat / transcript (8.3% of rows each), so S1-S3
# give those three little and the five other registers (faq, json, memo, ticket, yaml) the rest: every register stays
# under the 15% cap of spec 3.0 (about 12-13% each; the equiv partner's skin is a pool-proportional pick). Mode F notes exist for six registers only (no json / yaml).
P_MODE_F = 0.20

# G0 section 10 ruling B2 (v3), verbatim: the G3-H ITEM field asks for the name alone, no leading article or possessive.
ITEM_FIELD_DESCRIBE = ("the item's name alone, with no leading article or possessive "
                       "(a, an, the, my, our, your, his, her, their, its)")

# a / an by the item's first sound (fix iteration 2). The table is read first, longest prefix first; anything else
# falls to the kit's c2_kit.skin.article. "an": letter-named starts (e-bike, x-ray, mp3), silent h. "a": a sounded
# "you" / "wuh" start.
ITEM_AN_PREFIXES = ("e-", "x-", "x ", "hour", "honest", "honour", "honor", "heir", "mp3", "sla ", "faq", "html", "mri")
ITEM_A_PREFIXES = ("u-", "unit", "union", "unique", "univers", "unif", "use", "usu", "usa", "eu", "one", "once",
                   "ubiq", "util")


def item_article(item: str) -> str:
    """"a" or "an" for an item name, by how its first word is said aloud."""
    low = item.strip().lower()
    for pre in sorted(ITEM_AN_PREFIXES + ITEM_A_PREFIXES, key=len, reverse=True):
        if low.startswith(pre):
            return "an" if pre in ITEM_AN_PREFIXES else "a"
    return K.article(item)


def agree_item_article(skin, item: str):
    """Mode F only: the note's literal "a" / "an" before its brief ITEM is swapped for the one the row's item needs
    (the note was written for another item, so "an laptop" / "a office chair" would otherwise print). Other
    determiners (the, my, their) and Mode T skins ({a|ITEM} already agrees) are untouched. Reads the item only."""
    if skin.author_mode != "F":
        return skin
    brief = dict(skin.brief).get("ITEM")
    if not brief:
        return skin
    art = item_article(item)

    def swap(m):
        new = art.capitalize() if m.group(1)[0].isupper() else art
        return new + m.group(2)

    text = re.sub(r"\b(an?|An?)(\s+)(?=" + re.escape(brief) + r")", swap, skin.text)
    return skin if text == skin.text else dataclasses.replace(skin, text=text)
REGISTER_WEIGHTS = {
    "T": (("email", 0.04), ("chat", 0.04), ("transcript", 0.04), ("faq", 0.15), ("json", 0.22), ("memo", 0.15),
          ("ticket", 0.15), ("yaml", 0.21)),
    "F": (("email", 0.06), ("chat", 0.06), ("transcript", 0.06), ("faq", 0.26), ("memo", 0.28), ("ticket", 0.28)),
}
CARDS = 6
TAIL_DAYS = 420                          # case dates fall at most this long after the newest start
SUNSET_SPAN = 400                        # sunset upper bound when the replacing version is the newest (G0 R8)
Q_SCALE = 3                              # printed day counts stay within this many times the pool max

QUESTION_FORMS = (
    QuestionForm("ch_version", "choice", answer_set="open"),
    QuestionForm("ch_term", "choice", answer_set="open"),
    QuestionForm("yn_version", "noul", "governs", 1),
    QuestionForm("yn_version_other", "noul", "governs", -1, "implicit"),
    QuestionForm("yn_version_not", "noul", "governs", -1, "syntactic"),
    QuestionForm("yn_claim", "noul", "claim_supported", 1),
    QuestionForm("yn_claim_contra", "noul", "claim_supported", -1, "antonym"),
    QuestionForm("yn_claim_not", "noul", "claim_supported", -1, "syntactic"),
    QuestionForm("yn_outcome", "noul", "within_term", 1),
    QuestionForm("yn_outcome_out", "noul", "within_term", -1, "antonym"),
    QuestionForm("yn_outcome_not", "noul", "within_term", -1, "syntactic"),
)
QF = {q.qform: q for q in QUESTION_FORMS}
PREDICATE = {q.qform: q.predicate for q in QUESTION_FORMS}
POLARITY = {q.qform: q.polarity for q in QUESTION_FORMS}
CANDIDATE_FORMS = ("yn_version", "yn_version_other", "yn_version_not")
CLAIM_FORMS = ("yn_claim", "yn_claim_contra", "yn_claim_not")
OUTCOME_FORMS = ("yn_outcome", "yn_outcome_out", "yn_outcome_not")
# The negative / antonym / implicit-complement predicates of T23's three predicates (c2_kit.polarity rules P1-P3; G0 7
# and 10: the antonym of "within the term" is "outside / beyond / exceed", of "supports the claim" "contradicts /
# conflicts with / goes against it", of "governs" "a different version / some version besides / other than"). A wording
# negates the positive predicate syntactically OR uses one of these, never both; negcount's own implicit cues (fail,
# lack, without ...) count too.
NEGATIVE_PREDICATES = (
    r"outside", r"beyond", r"exceed(?:s|ed|ing)?", r"over", r"above", r"contradict(?:s|ed|ing|ion)?",
    r"conflict(?:s|ed|ing)?", r"against", r"disagree(?:s|d)?", r"differ(?:s|ed|ing)?", r"different",
    r"depart(?:s|ed|ing)?", r"other\s+than", r"besides",
)

# ------------------------------------------------------------------------------------------------ error models (G0 5)
register_name("t23_original_version", "applies the first (oldest) version of the rule")
register_name("t23_ignore_clause", "applies the version in force on the anchor date and skips the transition or "
                                   "sunset clause")
register_name("t23_foreign_clause", "applies a transition or sunset clause even when it belongs to a version that "
                                    "would not govern the case")
register_name("t23_purchase_date", "selects the version in force on the purchase date instead of the stated anchor")
register_name("t23_event_date", "selects the version in force on the event date instead of the stated anchor")
register_name("t23_filing_date", "selects the version in force on the filing date instead of the stated anchor")
register_name("t23_decision_date", "selects the version in force on the decision date instead of the stated anchor")
VER_EM = ("newest_version", "t23_original_version", "t23_ignore_clause", "t23_foreign_clause", "t23_purchase_date",
          "t23_event_date", "t23_filing_date", "t23_decision_date", "drop_inclusive_endpoint",
          "add_exclusive_endpoint")
ANCHOR_MODS = {"t23_purchase_date": "PURCHASE_DATE", "t23_event_date": "EVENT_DATE",
               "t23_filing_date": "FILING_DATE", "t23_decision_date": "DECISION_DATE"}


# ------------------------------------------------------------------------------------------------ helpers

def _draw(u: float, shares: tuple) -> str:
    acc = 0.0
    for key, share in shares:
        acc += share
        if u < acc:
            return key
    return shares[-1][0]


def _yes_target(sampler: str, seed: int) -> bool:
    """Label-first target bit: seeds 2k and 2k + 1 share the question form and get opposite targets, so every yes/no
    form is exactly 50% yes over any run of whole seed pairs (G0 section 4)."""
    return (uhash(FAMILY, "yes", sampler, seed // 2) < 0.5) != bool(seed % 2)


def _card(sampler: str, card: int) -> tuple:
    """(domain, anchor, style, window) fixed by the card (G0 section 2)."""
    si = SAMPLER_INDEX[sampler]
    dom = DOMAIN_KEYS[(si * CARDS + card) % len(DOMAIN_KEYS)]
    anchor = ANCHORS[(card + si) % 3]
    style = SAMPLER_STYLE[sampler] or ("table" if card % 2 == 0 else "log")
    if style == "log":
        return dom, anchor, style, "chain"
    return dom, anchor, style, ("incl", "excl")[(card // 2 if sampler == "S5" else card) % 2]


def _term_slot(tkind: str, x: int) -> S.Slot:
    return S.cents_slot(x) if tkind == "cents" else S.count_slot(x, UNITS[tkind])


def _idx(starts: list, d: dt.date):
    """Construction table: the 1-based version in force on d (windows tile, so the last start on or before d)."""
    k = None
    for i, s in enumerate(starts):
        if s <= d:
            k = i + 1
    return k


def _decide(st: dict) -> int:
    cl = st["clause"]
    return cl["target"] if cl and cl["fires"] else st["d0"]


def _gap(rng: random.Random, span: int) -> int:
    r = rng.random()
    if r < 0.10:
        g = 0
    elif r < 0.16:
        g = 1
    elif r < 0.55:
        g = rng.randint(2, 30)
    else:
        g = rng.randint(31, 200)
    return min(g, span)


def _ident(x):
    return x


def _code_ids(rng: random.Random, prefix: str, n: int, u: float) -> list:
    """ch_version ids (G0 R14): random document codes, so the sorted order of the shown ids is random against the
    versions' order (v1 / v2 or rev-A / rev-B would sort the newer version higher, a content-free cue on the gold:
    the newest version governs most rows by design, spec 3.11)."""
    if u < 0.5:
        return [f"{prefix}-{x}" for x in rng.sample(range(100, 1000), n)]
    if u < 0.75:
        return [f"{prefix}{x}" for x in rng.sample(range(10, 100), n)]
    return [f"{prefix}-{x}{c}" for x, c in zip(rng.sample(range(10, 100), n), rng.sample(CODE_LETTERS, n))]


DN_FRAME_PROBLEM = ("P4 double negation under a negated question frame 'aux + subject + not' (G0 v4 section 10: "
                    "the frame and the inner negation can be read as a confirming question, which reverses the gold)")


@dataclass(frozen=True)
class _CtxEntry:
    screened: KitCtx          # the context without the wordings that break the polarity rule
    narrow: KitCtx            # ... and without any double-negation wording (rows with a non-syntactic complement)
    bad: dict                 # {wording skin id: problems}
    dn: frozenset             # the double-negation wordings that stay in `screened`


class T23(C2Plugin):
    FAMILY = FAMILY
    TIER = "everyday"
    G0_LITE = HERE / "G0_SPEC.md"
    G0_SHA256 = "d0596ab2514856c23b315ff312d4bf321ffe486a9ec7c9faf7a79d29fa2837c3"   # frozen v4 14 Oct (G0 section 11); v3 = G0_SPEC_v3.md
    G0_SHA256_V3 = "ab1d650e87488de1868ebbbd8b7051008bb3d462f748ca85b8f087fc15a1227c"   # the pools_v2 freeze
    G0_HAIKU_TASK = "c2-data-stage-a/amb:T23"     # the one Haiku ambiguity pass (48 points; G0 section 9)
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "rule_engine"
    PARADIGM_B = "sql_sqlite"
    SOLVER_B_MODULE = "families.T23.solver_b"
    QFORMS = QF
    LABEL_WORDS = ("supported", "unsupported", "contradicted", "contradicts", "governs", "governing", "grandfathered",
                   "within the", "outside the")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("memo", "email", "chat", "ticket", "json", "yaml", "faq", "transcript", "notice", "export")
    HELD_OUT_REGISTERS = ("notice", "export")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW = ("FAQ", "HR", "IT")
    POLARITY_CHECK = True                       # c2_kit.polarity: a yes/no wording must read with its form's polarity
    POLARITY_NEGATIVES = NEGATIVE_PREDICATES
    POLARITY_STRICT_FRAMES = False              # the strict frame rule (P4) is applied to double negations only (below)

    def __init__(self, lexicon=None):
        super().__init__(lexicon)
        self._ems = None
        self._ctx_cache: list = []              # [(ctx, _CtxEntry)]: the polarity screen of a context, once
        self._mode_ids: dict = {}               # id(ctx) -> {author mode: frozenset of the OTHER mode's skin ids}

    # ============================================================================================ wording screen (FIX-1)
    @classmethod
    def wording_problems(cls, qform: str, text: str) -> list:
        """The wording rule of G0 v4 section 11 for one question wording: c2_kit.polarity P1-P3 (the wording reads with
        its form's polarity), plus P4 on a double negation (no negated question frame). [] = fine. A (re)authoring
        round calls this before admitting a yes/no wording (the v3 authoring path stays as it was: its disk == rebuild
        check reproduces the pool freeze)."""
        probs = POL.form_problems(cls, qform, text)
        q = QF.get(qform)
        if q is not None and q.qtype == "noul":
            r = POL.read(text, NEGATIVE_PREDICATES)
            if r.k_syn >= 2 and r.frame == "subject_not":
                probs.append(DN_FRAME_PROBLEM)
        return probs

    def _entry(self, ctx):
        """The wording screen of one kit context (wording_problems on every yes/no wording), cached by the context
        object. Label-blind: it reads wording texts and forms, never a row."""
        for c, ent in self._ctx_cache:
            if c is ctx:
                return ent
        bad, dn = {}, set()
        for sid, sk in ctx.skins.items():
            if sk.kind != "wording" or not sk.qform or QF[sk.qform].qtype != "noul":
                continue
            probs = self.wording_problems(sk.qform, sk.text)
            if probs:
                bad[sid] = probs
            elif POL.read(sk.text, NEGATIVE_PREDICATES).k_syn >= 2:
                dn.add(sid)
        screened = (KitCtx(skins={k: v for k, v in ctx.skins.items() if k not in bad}, lexicon=ctx.lexicon)
                    if bad else ctx)
        narrow = KitCtx(skins={k: v for k, v in screened.skins.items() if k not in dn}, lexicon=ctx.lexicon)
        ent = _CtxEntry(screened, narrow, bad, frozenset(dn))
        self._ctx_cache.append((ctx, ent))
        return ent

    def ctx_for(self, spec, ctx):
        """The kit context a row's pipeline unit draws from (pipeline.build_unit calls this on the base spec):
        - wordings that break the polarity rule are left out (P1-P3 for every yes/no wording; P4 for double negations);
        - a row whose proposed complement is non-syntactic (antonym / implicit) gets no double-negation wording: the
          partner would carry two negation cues fewer than the base (PILOT_VERDICT FIX-1, G-TW). The choice depends on
          the row key only (the same draw relations() makes), never on the gold."""
        ent = self._entry(ctx)
        if spec is not None:
            comp = self._complement_form(spec)
            if comp is not None and QF[comp].complement_kind != "syntactic":
                return ent.narrow
        return ent.screened

    def quarantined_wordings(self, ctx) -> dict:
        """{wording skin id: polarity problems} for the wordings ctx_for() leaves out of `ctx`."""
        return dict(self._entry(ctx).bad)

    # ============================================================================================ sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        qform = _draw(uhash(FAMILY, "qform", sampler, seed // 2), BASE_SHARES)     # seed pairs share the form
        card = rng.randrange(CARDS)
        dom, anchor, style, window = _card(sampler, card)
        scen = _draw(uhash(FAMILY, "scen", sampler, seed), SCENARIOS)
        ctype = self._clause_type(scen, anchor, uhash(FAMILY, "ctype", sampler, seed))
        ctx = {"seed": seed, "sampler": sampler, "qform": qform, "card": card, "dom": dom, "anchor": anchor,
               "style": style, "window": window, "scen": scen, "ctype": ctype,
               "yes": _yes_target(sampler, seed) if QF[qform].qtype == "noul" else None}
        for _ in range(MAX_TRIES):
            spec = self._attempt(rng, ctx)
            if spec is not None:
                return spec
        raise ContractError(f"T23 {sampler} seed {seed}: no {scen}/{ctype} spec in {MAX_TRIES} draws")

    @staticmethod
    def _clause_type(scen: str, anchor: str, u: float):
        """A clause type that can realise the scenario (a keep-old clause fires only when its role date comes before
        the anchor in P <= E <= F order: G0 section 3)."""
        if scen == "none":
            return None
        ok = []
        for t, w in CLAUSE_TYPES:
            if scen == "decisive" and t in KEEP_ROLE and ROLES.index(KEEP_ROLE[t]) >= ROLES.index(anchor):
                continue
            ok.append((t, w))
        total = sum(w for _, w in ok)
        return _draw(u, tuple((t, w / total) for t, w in ok))

    @staticmethod
    def _pick_d0(rng: random.Random, choices: list, n: int) -> int:
        """Default-version draw: the newest version weighs P_NEWEST, the older ones share the rest (G0 section 3)."""
        if len(choices) == 1:
            return choices[0]
        if n in choices:
            if rng.random() < P_NEWEST:
                return n
            choices = [c for c in choices if c != n]
        return rng.choice(choices)

    def _attempt(self, rng: random.Random, ctx: dict):
        sampler, scen, ctype = ctx["sampler"], ctx["scen"], ctx["ctype"]
        pack = DOMAINS[ctx["dom"]]
        n = rng.choice(N_VERSIONS[sampler])
        starts = [FIRST_DAY + DAY * rng.randrange(0, 700)]
        for _ in range(1, n):
            starts.append(starts[-1] + DAY * rng.randint(45, 320))
        edge = rng.random() < P_EDGE[sampler]
        plan = self._plan(rng, ctx, starts, edge)
        if plan is None:
            return None
        dates = self._place(rng, starts, plan, ctx["anchor"])
        if dates is None:
            return None
        sunset = None
        if ctype == "sunset":
            sunset = self._sunset(rng, starts, plan["c"], dates[3], scen, edge)
            if sunset is None:
                return None
        clause = None
        if ctype:
            role = KEEP_ROLE.get(ctype, "DECISION_DATE")
            clause = {"type": ctype, "kind": CLAUSE_KIND[ctype], "on": plan["c"], "role": role}
        st = self._status_of(starts, dict(zip(ROLES, dates)), ctx["anchor"], clause, sunset, [], None)
        if not self._scenario_holds(st, scen):
            return None
        gov = _decide(st)
        forced = None
        if ctx["qform"] == "yn_outcome" and pack.pair and rng.random() < P_TERM_EDGE[sampler]:
            got = self._edge_q(rng, pack, starts, plan, dates, ctx["yes"])
            if got is not None:
                st2 = self._status_of(starts, dict(zip(ROLES, got[0])), ctx["anchor"], clause, sunset, [], None)
                if self._scenario_holds(st2, scen) and _decide(st2) == gov:
                    dates, forced = got
        got = self._terms(rng, ctx, pack, n, gov, dict(zip(ROLES, dates)), forced)
        if got is None:
            return None
        terms, qty = got
        spec = self._build(rng, ctx, pack, starts, dates, terms, qty, clause, sunset)
        if spec is None:
            return None
        return self._finish(spec, ctx, gov)

    def _plan(self, rng, ctx, starts, edge):
        """Which version is the default (d0), which version carries the clause (c) and the date intervals or pins the
        scenario needs (G0 sections 2-3)."""
        n, scen, ctype, anchor = len(starts), ctx["scen"], ctx["ctype"], ctx["anchor"]
        S_ = [None] + starts                                   # 1-based starts
        lo, hi, pin = {}, {}, {}
        c = None
        kind = CLAUSE_KIND.get(ctype)
        everyone = list(range(1, n + 1))
        if kind is None:
            d0 = self._pick_d0(rng, everyone, n)
        elif kind == "keep_old":
            role = KEEP_ROLE[ctype]
            c = rng.randint(2, n)
            if scen == "foreign":
                d0 = self._pick_d0(rng, [k for k in everyone if k != c], n)
            else:
                d0 = c
                if scen == "decisive":
                    hi[role] = S_[c] - DAY
                    if edge:
                        pin[role] = S_[c] - DAY
                else:
                    lo[role] = S_[c]
                    if edge:
                        pin[role] = S_[c]
        elif kind == "retro":
            c = rng.randint(2, n)
            if scen == "foreign":
                d0 = self._pick_d0(rng, list(range(c, n + 1)), n)
            else:
                d0 = self._pick_d0(rng, list(range(1, c)), n)
                if scen == "decisive":
                    lo["DECISION_DATE"] = S_[c]
                    if edge:
                        pin["DECISION_DATE"] = S_[c]
                else:
                    hi["DECISION_DATE"] = S_[c] - DAY
                    if edge:
                        pin["DECISION_DATE"] = S_[c] - DAY
        else:  # sunset
            c = rng.randint(1, n - 1)
            if scen == "foreign":
                d0 = self._pick_d0(rng, [k for k in everyone if k != c], n)
            else:
                d0 = c
                if scen == "decisive":
                    lo["DECISION_DATE"] = S_[c + 1] + DAY
                else:
                    hi["DECISION_DATE"] = self._sunset_hi(starts, c)
        # the anchor sits in d0's window
        lo[anchor] = max(lo.get(anchor, S_[d0]), S_[d0])
        top = S_[d0 + 1] - DAY if d0 < n else S_[n] + DAY * TAIL_DAYS
        hi[anchor] = min(hi.get(anchor, top), top)
        if edge and not pin and (kind is None or scen == "foreign"):
            ends = ([S_[d0]] if d0 >= 2 else []) + ([S_[d0 + 1] - DAY] if d0 < n else [])
            if ends:
                pin[anchor] = rng.choice(ends)
        return {"d0": d0, "c": c, "lo": lo, "hi": hi, "pin": pin}

    @staticmethod
    def _sunset_hi(starts: list, c: int) -> dt.date:
        n = len(starts)
        return starts[c + 1] - DAY if c + 2 <= n else starts[c] + DAY * SUNSET_SPAN

    @staticmethod
    def _intervals(starts, plan):
        """Per-role [lo, hi] from the plan (pins collapse an interval; None: a pin outside its interval)."""
        first, last = starts[0], starts[-1] + DAY * TAIL_DAYS
        lo = [max(first, plan["lo"].get(r, first)) for r in ROLES]
        hi = [min(last, plan["hi"].get(r, last)) for r in ROLES]
        for i, r in enumerate(ROLES):
            if r in plan["pin"]:
                p = plan["pin"][r]
                if not lo[i] <= p <= hi[i]:
                    return None
                lo[i] = hi[i] = p
        return lo, hi

    def _place(self, rng, starts, plan, anchor):
        """Four ordered case dates inside the plan's intervals: the anchor first (uniform in its window), then the
        earlier roles backwards and the later roles forwards with gaps (0 and 1 day included)."""
        got = self._intervals(starts, plan)
        if got is None:
            return None
        lo, hi = got
        for i in range(1, 4):
            lo[i] = max(lo[i], lo[i - 1])
        for i in range(2, -1, -1):
            hi[i] = min(hi[i], hi[i + 1])
        if any(a > b for a, b in zip(lo, hi)):
            return None
        a = ROLES.index(anchor)
        dates = [None] * 4
        dates[a] = lo[a] + DAY * rng.randint(0, (hi[a] - lo[a]).days)
        for i in range(a - 1, -1, -1):
            top = min(hi[i], dates[i + 1])
            dates[i] = top - DAY * _gap(rng, (top - lo[i]).days)
        for i in range(a + 1, 4):
            base = max(lo[i], dates[i - 1])
            dates[i] = base + DAY * _gap(rng, (hi[i] - base).days)
        return dates

    def _edge_q(self, rng, pack, starts, plan, dates, yes):
        """Day-count edge (G0 section 2): move the later date of the pack's pair so that Q = t (yes) or t + 1 (no) for
        a pool term t, inside its interval and between its neighbours. (dates, t) or None."""
        frm, to = (ROLES.index(r) for r in pack.pair)
        if ROLES[to] in plan["pin"]:
            return None
        lo, hi = self._intervals(starts, plan)
        for t in rng.sample(list(pack.pool), len(pack.pool)):
            new = dates[frm] + DAY * (t + (0 if yes else 1))
            if lo[to] <= new <= hi[to] and dates[to - 1] <= new and (to == 3 or new <= dates[to + 1]):
                out = list(dates)
                out[to] = new
                return out, t
        return None

    def _sunset(self, rng, starts, c, dec, scen, edge):
        lo, hi = starts[c], self._sunset_hi(starts, c)          # starts[c] = S_c+1 (0-based list)
        if scen == "decisive":
            hi = min(hi, dec - DAY)
            if edge and lo <= dec - DAY <= hi:
                return dec - DAY
        elif scen == "tested":
            lo = max(lo, dec)
            if edge and lo == dec <= hi:
                return dec
        if lo > hi:
            return None
        return lo + DAY * rng.randint(0, (hi - lo).days)

    @staticmethod
    def _scenario_holds(st: dict, scen: str) -> bool:
        cl = st["clause"]
        if scen == "none":
            return cl is None
        if cl is None:
            return False
        return {"decisive": cl["fires"], "tested": cl["applies"] and not cl["fires"],
                "foreign": not cl["applies"]}[scen]

    def _terms(self, rng, ctx, pack, n, gov, dates, forced=None):
        """Distinct pool term values (one per version) and Q. yn_outcome rows hit their yes / no target here: with a
        printed day count the governing term is a pool value on the target side of Q (`forced` when _edge_q already
        placed Q = t or t + 1), with an input Q the quantity is chosen around the governing term (Q = T_G and
        T_G + 1 are the edges)."""
        yes, sampler = ctx["yes"], ctx["sampler"]
        outcome = ctx["qform"] == "yn_outcome"
        edge = rng.random() < P_TERM_EDGE[sampler]
        pool = list(pack.pool)
        q = (dates[pack.pair[1]] - dates[pack.pair[0]]).days if pack.pair else None
        if q is not None and q > max(pool) * Q_SCALE:
            return None                                        # a day count far outside the pack's range
        if outcome and pack.pair:
            opts = [forced] if forced is not None else [t for t in pool if (t >= q if yes else t < q)]
            if not opts:
                return None
            g_t = rng.choice(opts)
            others = rng.sample([t for t in pool if t != g_t], n - 1)
            terms = others[:gov - 1] + [g_t] + others[gov - 1:]
        else:
            terms = rng.sample(pool, n)
        if q is None:
            q = self._input_qty(rng, pack.tkind, terms[gov - 1], yes if outcome else None, edge)
        return terms, q

    @staticmethod
    def _input_qty(rng, tkind: str, t: int, yes, edge: bool) -> int:
        if yes is None:
            t = t if rng.random() < 0.5 else rng.choice((t // 2 + 1, t * 2))
            if tkind == "cents":
                return max(100, int(t * rng.uniform(0.5, 1.5)) // 100 * 100)
            return max(1, int(t * rng.uniform(0.4, 1.6)))
        if edge:
            return t if yes else t + 1
        if tkind == "cents":
            step = rng.randint(1, max(1, t // 200)) * 100
            return max(100, t - step) if yes else t + step
        if yes:
            return rng.randint(max(1, t // 2), t)
        return t + rng.randint(1, 3 if tkind == "devices" else 10)

    def _ids(self, rng, pack: Pack, n: int, qform: str | None = None) -> list:
        u = rng.random()
        if qform == "ch_version":            # the ids are the options: codes whose sort order is random (R14)
            return _code_ids(rng, pack.prefix, n, u)
        if u < 0.4:
            return [f"v{k}" for k in range(1, n + 1)]
        if u < 0.7:
            return [f"rev-{'ABCD'[k]}" for k in range(n)]
        codes = rng.sample(range(100, 1000), n)
        return [f"{pack.prefix}-{x}" for x in codes]

    def _build(self, rng, ctx, pack, starts, dates, terms, qty, clause, sunset):
        n = len(starts)
        slots = {"DOC": S.name_slot(pack.doc), "TERM_LABEL": S.name_slot(pack.term),
                 "QTY_LABEL": S.name_slot(pack.qty), "CUSTOMER": S.name_slot(rng.choice(CUSTOMERS)),
                 "ORG": S.name_slot(rng.choice(ORGS)), "ITEM": S.name_slot(rng.choice(pack.items)),
                 "CASE_ID": S.id_slot(f"CASE-{rng.randrange(1000, 10000)}")}
        for r, label in zip(ROLES, pack.labels):
            slots[LABEL_SLOT[r]] = S.name_slot(label)
        for r, d in zip(ROLES, dates):
            slots[r] = S.date_slot(d)
        for k, (vid, s, t) in enumerate(zip(self._ids(rng, pack, n, ctx["qform"]), starts, terms), start=1):
            slots[f"V{k}_ID"] = S.id_slot(vid)
            slots[f"V{k}_START"] = S.date_slot(s)
            slots[f"V{k}_TERM"] = _term_slot(pack.tkind, t)
        if sunset is not None:
            slots["SUNSET"] = S.date_slot(sunset)
        if pack.pair is None:
            slots["QTY"] = _term_slot(pack.tkind, qty)
        structure = {"domain": ctx["dom"], "style": ctx["style"], "window": ctx["window"], "anchor": ctx["anchor"],
                     "n": n, "tkind": pack.tkind, "qty": list(pack.pair) if pack.pair else None, "clause": clause}
        return Spec(FAMILY, ctx["sampler"], ctx["seed"], f"{FAMILY}:{ctx['sampler']}:c{ctx['card']:02d}",
                    ctx["qform"], slots, structure=structure, pack=f"t23:{ctx['dom']}")

    def _finish(self, spec: Spec, ctx: dict, gov: int):
        """Question pointers (CANDIDATE / CLAIM), depth, tags, and the construction-vs-solver-A guard."""
        q = spec.qform
        spec = self.derive(spec)                                # printed ends first: solver A reads them
        if q in CANDIDATE_FORMS + CLAIM_FORMS:
            k = gov if ctx["yes"] else self._wrong_version(spec, gov)
            if k is None:
                return None
            pointer = {"candidate": f"V{k}_ID"} if q in CANDIDATE_FORMS else {"claim": f"V{k}_TERM"}
            spec = self.derive(spec.replace(structure={**spec.structure, **pointer}))
        st = self._status(spec)
        applies = bool(st["clause"] and st["clause"]["applies"])
        depth = 1 + applies + (q in OUTCOME_FORMS)
        spec = spec.replace(depth=depth, deep=depth >= 3)
        spec = spec.replace(tags=self._tags(spec, st))
        if self._resolve(spec) != _decide(st):
            raise ContractError(f"T23 seed {spec.seed}: construction table and solver A disagree")
        return spec

    def _wrong_version(self, spec: Spec, gov: int):
        """yn 'no' rows: the version named by the first error model (seeded order) that names another version."""
        for name in sorted(VER_EM, key=lambda m: uhash(FAMILY, "cand", spec.sampler, spec.seed, m)):
            k = self._resolve(spec, frozenset({name}))
            if k not in (None, gov):
                return k
        return None

    def _tags(self, spec: Spec, st: dict) -> tuple:
        v, s = spec.env(), spec.structure
        n = s["n"]
        starts = [v[f"V{k}_START"] for k in range(1, n + 1)]
        gov = _decide(st)
        tags = set()
        if gov != n:
            tags.add("newest_wrong")
        cl, scl = s["clause"], st["clause"]
        if cl is None:
            tags.add("plain")
        else:
            tags.add(cl["type"])
            tags.add("clause_decisive" if scl["fires"] else ("clause_tested" if scl["applies"] else "foreign_clause"))
        edges = {x for b in starts[1:] for x in (b - DAY, b)}
        if v[s["anchor"]] in edges:
            tags.add("boundary")
        if cl is not None and scl["applies"]:
            sc = starts[cl["on"] - 1]
            if cl["kind"] == "keep_old" and v[cl["role"]] in (sc - DAY, sc):
                tags.add("boundary")
            if cl["kind"] == "retro" and v["DECISION_DATE"] in (sc - DAY, sc):
                tags.add("boundary")
            if cl["kind"] == "sunset" and v["DECISION_DATE"] in (v["SUNSET"], v["SUNSET"] + DAY):
                tags.add("boundary")
        if spec.qform in OUTCOME_FORMS and st["q"] in (st["terms"][gov - 1], st["terms"][gov - 1] + 1):
            tags.add("term_edge")
        if starts[-1] > v["DECISION_DATE"]:
            tags.add("future_version")
        if spec.deep:
            tags.add("deep")
        return tuple(sorted(tags))

    # ============================================================================================ derive
    def derive(self, spec: Spec) -> Spec:
        st = spec.structure
        n = st["n"]
        derived, deps = {}, {}
        if st["style"] != "log":
            for k in range(1, n):
                nxt = spec.slots[f"V{k + 1}_START"].value
                derived[f"V{k}_END"] = S.date_slot(nxt - DAY if st["window"] == "incl" else nxt)
                deps[f"V{k}_END"] = (f"V{k + 1}_START",)
        if st["qty"]:
            frm, to = st["qty"]
            derived["QTY"] = S.count_slot((spec.slots[to].value - spec.slots[frm].value).days, UNITS["days"])
            deps["QTY"] = (frm, to)
        for key, name in (("candidate", "CANDIDATE"), ("claim", "CLAIM")):
            if st.get(key):
                derived[name] = spec.slots[st[key]]
                deps[name] = (st[key],)
        return spec.replace(derived=derived, derived_deps=deps)

    # ============================================================================================ solver A
    def _window(self, spec: Spec, k: int, d):
        """Rule AST: version k is in force on the date node d (G0 R3)."""
        st = spec.structure
        lo = RL.Cmp("<=", RL.Ref(f"V{k}_START"), d)
        if k == st["n"]:
            return lo
        if st["window"] == "chain":
            return RL.And((lo, RL.Cmp("<", d, RL.Ref(f"V{k + 1}_START"))))
        return RL.And((lo, RL.Cmp("<=" if st["window"] == "incl" else "<", d, RL.Ref(f"V{k}_END"))))

    def _in_force(self, spec: Spec, env: dict, slot: str, mods: frozenset):
        st = spec.structure
        shift = 0
        if "drop_inclusive_endpoint" in mods and st["window"] == "incl":
            shift = 1
        if "add_exclusive_endpoint" in mods and st["window"] in ("excl", "chain"):
            shift = -1
        d = RL.Ref(slot) if not shift else RL.Fn("add_days", (RL.Ref(slot), RL.Lit(shift)))
        hits = [k for k in range(1, st["n"] + 1) if RL.evaluate(self._window(spec, k, d), env)]
        return hits[0] if len(hits) == 1 else None

    def _resolve(self, spec: Spec, mods: frozenset = frozenset()):
        """Solver A (mods empty) and the error models (one rule swapped): the governing version, 1-based, or None."""
        st, env = spec.structure, spec.env()
        if "newest_version" in mods:
            return st["n"]
        if "t23_original_version" in mods:
            return 1
        anchor = st["anchor"]
        for m, slot in ANCHOR_MODS.items():
            if m in mods:
                if slot == anchor:
                    return None
                anchor = slot
        d0 = self._in_force(spec, env, anchor, mods)
        cl = st["clause"]
        if d0 is None or cl is None or "t23_ignore_clause" in mods:
            return d0
        c, foreign = cl["on"], "t23_foreign_clause" in mods
        start_c = RL.Ref(f"V{c}_START")
        if cl["kind"] == "keep_old":
            op = "<=" if "add_exclusive_endpoint" in mods else "<"
            if (foreign or d0 == c) and RL.evaluate(RL.Cmp(op, RL.Ref(cl["role"]), start_c), env):
                return self._in_force(spec, env, cl["role"], mods)
            return d0
        if cl["kind"] == "retro":
            late = RL.Cmp(">" if "drop_inclusive_endpoint" in mods else ">=", RL.Ref("DECISION_DATE"), start_c)
            node = late if foreign else RL.And((RL.Cmp("<", RL.Ref(f"V{d0}_START"), start_c), late))
            return c if RL.evaluate(node, env) else d0
        late = RL.Cmp(">=" if "add_exclusive_endpoint" in mods else ">", RL.Ref("DECISION_DATE"), RL.Ref("SUNSET"))
        return c + 1 if (foreign or d0 == c) and RL.evaluate(late, env) else d0

    def solve_a(self, spec: Spec):
        g = self._resolve(spec)
        if g is None:
            raise ContractError("T23: no version is in force on the anchor date (never generated)")
        env, q = spec.env(), spec.qform
        if q == "ch_version":
            return env[f"V{g}_ID"]
        if q == "ch_term":
            return env[f"V{g}_TERM"]
        node = {"governs": RL.Cmp("==", RL.Ref(f"V{g}_ID"), RL.Ref("CANDIDATE")),
                "claim_supported": RL.Cmp("==", RL.Ref(f"V{g}_TERM"), RL.Ref("CLAIM")),
                "within_term": RL.Cmp("<=", RL.Ref("QTY"), RL.Ref(f"V{g}_TERM"))}[PREDICATE[q]]
        ok = RL.evaluate(node, env)
        return int(ok if POLARITY[q] == 1 else not ok)

    # ============================================================================================ construction table
    @staticmethod
    def _status_of(starts: list, dates: dict, anchor: str, clause, sunset, terms: list, q) -> dict:
        d0 = _idx(starts, dates[anchor])
        out = None
        if clause:
            c = clause["on"]
            if clause["kind"] == "keep_old":
                applies, cond = d0 == c, dates[clause["role"]] < starts[c - 1]
                target = _idx(starts, dates[clause["role"]])
            elif clause["kind"] == "retro":
                applies = d0 is not None and starts[d0 - 1] < starts[c - 1]
                cond, target = dates["DECISION_DATE"] >= starts[c - 1], c
            else:
                applies, cond, target = d0 == c, dates["DECISION_DATE"] > sunset, c + 1
            fires = applies and cond
            out = {"applies": applies, "fires": fires, "target": target if fires else None}
        return {"d0": d0, "clause": out, "terms": list(terms), "q": q}

    def _status(self, spec: Spec) -> dict:
        v, st = spec.env(), spec.structure
        n = st["n"]
        return self._status_of([v[f"V{k}_START"] for k in range(1, n + 1)], {r: v[r] for r in ROLES}, st["anchor"],
                               st["clause"], v.get("SUNSET"), [v[f"V{k}_TERM"] for k in range(1, n + 1)], v["QTY"])

    def _answer_st(self, spec: Spec, st: dict):
        """The answer the construction table predicts (twins), by the G0 R11-R18 truth conditions."""
        g, env, q = _decide(st), spec.env(), spec.qform
        if q == "ch_version":
            return env[f"V{g}_ID"]
        if q == "ch_term":
            return st["terms"][g - 1]
        ok = {"governs": lambda: env[f"V{g}_ID"] == env["CANDIDATE"],
              "claim_supported": lambda: st["terms"][g - 1] == env["CLAIM"],
              "within_term": lambda: st["q"] <= st["terms"][g - 1]}[PREDICATE[q]]()
        return int(ok if POLARITY[q] == 1 else not ok)

    # ============================================================================================ facts (G3)
    def canonical(self, spec: Spec) -> dict:
        a, st = spec.all_slots(), spec.structure
        n = st["n"]

        def c(name):
            return S.canonical(a[name]) if name in a else None

        versions = [{"id": c(f"V{k}_ID"), "start": c(f"V{k}_START"), "end": c(f"V{k}_END"),
                     "replaces": c(f"V{k - 1}_ID") if k > 1 else None, "term": c(f"V{k}_TERM")}
                    for k in range(1, n + 1)]
        clause = None
        cl = st["clause"]
        if cl:
            k = cl["on"]
            clause = {"kind": cl["kind"], "on": c(f"V{k}_ID"), "role": ROLE_NAME[cl["role"]],
                      "date": c("SUNSET") if cl["kind"] == "sunset" else c(f"V{k}_START"),
                      "to": {"keep_old": None, "retro": c(f"V{k}_ID"), "sunset": c(f"V{k + 1}_ID")}[cl["kind"]]}
        question = ({"candidate": c("CANDIDATE")} if st.get("candidate") else
                    {"claim": c("CLAIM")} if st.get("claim") else {})
        return {"qform": spec.qform, "style": st["style"], "window": st["window"], "anchor": ROLE_NAME[st["anchor"]],
                "doc": c("DOC"), "term_label": c("TERM_LABEL"), "qty_label": c("QTY_LABEL"),
                "labels": [c(LABEL_SLOT[r]) for r in ROLES], "versions": versions, "clause": clause,
                "case": {"id": c("CASE_ID"), "dates": [c(r) for r in ROLES], "qty": c("QTY")},
                "question": question, "customer": c("CUSTOMER"), "org": c("ORG"), "item": c("ITEM")}

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        c = self.canonical(spec)
        return c if author_mode == "T" else {k: v for k, v in c.items() if k not in ("customer", "org", "item")}

    def extract_view(self, spec: Spec) -> dict:
        c = self.canonical(spec)
        return {"customer": c["customer"], "org": c["org"], "item": c["item"], "case_id": c["case"]["id"]}

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        return [Field("customer", "name", "the customer who raised the case, as written"),
                Field("org", "name", "the organisation the case is raised with, as written"),
                Field("item", "str", ITEM_FIELD_DESCRIBE),
                Field("case_id", "id", "the case reference, as written")]

    # ============================================================================================ render
    def _row_key(self, spec: Spec) -> str:
        return f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"

    def card_template(self, spec: Spec) -> str:
        """The card of this row as a slot template (G0 1.1, v4): the title, the rules the row needs, the closed-world
        sentence. {ANCHOR} is the anchor role's date label slot, {WINDOW} one of the three window rules."""
        st = spec.structure
        return (CARD_SPEC.template("full", spec).replace("{ANCHOR}", "{" + LABEL_SLOT[st["anchor"]] + "}")
                .replace("{WINDOW}", WINDOW_RULE[st["window"]]))

    def clause_template(self, spec: Spec):
        cl = spec.structure["clause"]
        if not cl:
            return None
        return CLAUSE_TPL[cl["kind"]].format(c=cl["on"], t=cl["on"] + 1, lab=LABEL_SLOT[cl["role"]])

    def versions_template(self, spec: Spec) -> str:
        """The program-written version block as a slot template (G0 1.2)."""
        st = spec.structure
        n, style = st["n"], st["style"]
        cl = st["clause"]
        clause = self.clause_template(spec)
        lines = []
        if style == "list":
            lines.append(f"Versions of the {{DOC}} ({END_MARK[st['window']]}):")
            for k in range(1, n + 1):
                rep = "first version" if k == 1 else f"replaces {{V{k - 1}_ID}}"
                win = f"in force from {{V{k}_START}}" + (f" to {{V{k}_END}}" if k < n else ", open-ended")
                lines.append(f"- {{V{k}_ID}}: {rep}; {win}; {{TERM_LABEL}}: {{V{k}_TERM}}.")
                if cl and cl["on"] == k:
                    lines.append("  " + clause)
        elif style == "table":
            lines += [f"Version table of the {{DOC}} ({END_MARK[st['window']]}):",
                      "version | replaces | in force from | in force to | {TERM_LABEL}"]
            for k in range(1, n + 1):
                rep = "first version" if k == 1 else f"{{V{k - 1}_ID}}"
                end = f"{{V{k}_END}}" if k < n else "open-ended"
                lines.append(f"{{V{k}_ID}} | {rep} | {{V{k}_START}} | {end} | {{V{k}_TERM}}")
            if clause:
                lines.append(clause)
        else:
            lines.append("Change log of the {DOC}, newest entry first:")
            for k in range(n, 0, -1):
                what = "as the first version" if k == 1 else f"replacing {{V{k - 1}_ID}}"
                sep = " " if k == 1 else ", "
                lines.append(f"{{V{k}_START}} | {{V{k}_ID}} takes effect{sep}{what} | {{TERM_LABEL}}: {{V{k}_TERM}}")
                if cl and cl["on"] == k:
                    lines.append("  " + clause)
        return "\n".join(lines)

    def case_template(self, spec: Spec) -> str:
        lines = ["Case {CASE_ID}:"]
        lines += [f"- {{{LABEL_SLOT[r]}}}: {{{r}}}" for r in ROLES]
        lines.append("- {QTY_LABEL}: {QTY}")
        if spec.structure.get("claim"):
            lines.append("- claim to check: the {TERM_LABEL} for this case is {CLAIM}")
        lines.append("End of case record.")
        return "\n".join(lines)

    def _term_text(self, spec: Spec):
        tkind = spec.structure["tkind"]

        def text(x):
            return S.render(_term_slot(tkind, x), "symbol" if tkind == "cents" else "digits")
        return text

    @staticmethod
    def _uniform_forms(spec: Spec, forms: dict) -> dict:
        """One number form per kind in a row (terms, Q and the claim read alike): every count / cents slot takes the
        form of the first such slot by name, with words -> digits and whole -> symbol (valid for every value). A
        function of the incoming forms only, so partners and twins that reuse a row's forms keep them."""
        out = dict(forms)
        for kind, swap in (("count", {"words": "digits"}), ("cents", {"whole": "symbol"})):
            names = sorted(k for k, s in spec.all_slots().items() if s.kind == kind and k in out)
            if names:
                f = swap.get(out[names[0]], out[names[0]])
                out.update({k: f for k in names})
        return out

    def _other_mode(self, ctx, mode: str) -> frozenset:
        """Ids of the narrative skins NOT written in `mode` (ctx.pick's exclude list), cached per context object."""
        ent = self._mode_ids.get(id(ctx))
        if ent is None or ent[0] is not ctx:
            ent = (ctx, {m: frozenset(k for k, v in ctx.skins.items() if v.kind == "skin" and v.author_mode != m)
                         for m in ("T", "F")})
            self._mode_ids[id(ctx)] = ent
        return ent[1][mode]

    def _pick_skin(self, ctx, spec: Spec, key: str, held: bool):
        """The narrative skin of a row (G0 v4, FIX-3): author mode from the row key first (Mode F with probability
        P_MODE_F; a held-out S5 row takes a Mode T held-out skin), then the register (S4: email / chat / transcript;
        S1-S3: REGISTER_WEIGHTS of the mode), then a skin of that mode. Label-blind: the row key only. A (mode,
        register) with no skin (the unit-test fixtures hold one Mode F note) falls back to the mode, then to Mode T."""
        if held:
            return ctx.pick(FAMILY, "skin", key, held_out=True)
        mode = "F" if uhash(key, "mode") < P_MODE_F else "T"
        if spec.sampler == "S4":
            reg = S4_REGISTERS[int(uhash(key, "register") * len(S4_REGISTERS))]
        else:
            reg = _draw(uhash(key, "register"), REGISTER_WEIGHTS[mode])
        for m, r in ((mode, reg), (mode, None), ("T", None)):
            try:
                return ctx.pick(FAMILY, "skin", key, register=r, exclude=self._other_mode(ctx, m), held_out=False)
            except LookupError:
                continue
        raise LookupError(f"T23: no training narrative skin for {key}")

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        key = self._row_key(spec)
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        ent = self._entry(ctx)
        ctx = ent.screened                      # never pick (or accept) a wording that breaks the polarity rule
        skin = skin or self._pick_skin(ctx, spec, key, held)
        if wording is not None and wording.skin_id in ent.bad:
            raise K.RenderError(f"wording {wording.skin_id} is quarantined: {ent.bad[wording.skin_id][0]}")
        wording = wording or ctx.pick(FAMILY, "wording", key, qform=spec.qform)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = self._uniform_forms(spec, forms or choose_forms(spec, key))
        slots = spec.all_slots()
        skin = agree_item_article(skin, slots["ITEM"].value)
        tb = TextBuilder()
        tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id)
        tb.add("state", "\n\n").add("state", K.fill(self.versions_template(spec), slots, forms))
        tb.add("state", "\n\n").add("state", K.fill(self.case_template(spec), slots, forms))
        if attack is not None:
            tb.add("state", "\n\n").add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        field = CK.place_rules(tb, K.fill(self.card_template(spec), slots, forms), QF[spec.qform].qtype)
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if spec.qform in ("ch_version", "ch_term"):
            show = _ident if spec.qform == "ch_version" else self._term_text(spec)
            # k = CHOICE_K on every row, never lowered after a failed build (kit distractors.py; G0 R14)
            os_ = build_options(spec, ans, self.error_models(), k=CHOICE_K, row_key=key, render_key=show)
            if os_ is None:
                raise K.RenderError("no distinct error-model answer for the options")
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, defs_style=CK.defs_style(field, "full"))

    # ============================================================================================ relations
    def relations(self, spec: Spec) -> list:
        out = []
        key = self._row_key(spec)
        comp = self._complement_form(spec)
        if comp is not None:
            out.append(RelationProposal("complement", qform=comp))
        u = uhash(FAMILY, "extra", key)
        if u < P_EQUIV:
            out.append(RelationProposal("equiv"))
        elif u < P_EQUIV + P_INV:
            out.append(RelationProposal("inv"))
        if uhash(FAMILY, "twin", key) < P_TWIN:
            t = self._twin(spec)
            if t is not None:
                out.append(t)
        return out + self._metamorphic(spec)

    def _complement_form(self, spec: Spec):
        """The complement question form relations() proposes for this row (a draw from the row key), or None. The
        wording screen (ctx_for) makes the same draw, so the base wording is picked knowing the partner's kind."""
        comp = COMPLEMENTS.get(spec.qform)
        key = self._row_key(spec)
        if comp and uhash(FAMILY, "comp", key) < P_COMPLEMENT:
            return _draw(uhash(FAMILY, "ckind", key), comp)
        return None

    def _valid(self, spec: Spec) -> bool:
        """Semantic invariants a twin must keep (G0 R2-R4, R8, section 6)."""
        v, st = spec.env(), spec.structure
        n = st["n"]
        starts = [v[f"V{k}_START"] for k in range(1, n + 1)]
        if any(b <= a for a, b in zip(starts, starts[1:])):
            return False
        ds = [v[r] for r in ROLES]
        if ds[0] < starts[0] or any(b < a for a, b in zip(ds, ds[1:])):
            return False
        terms = [v[f"V{k}_TERM"] for k in range(1, n + 1)]
        if len(set(terms)) != n or min(terms) < 1:
            return False
        cl = st["clause"]
        if cl and cl["kind"] == "sunset":
            c = cl["on"]
            if not starts[c] <= v["SUNSET"] <= self._sunset_hi(starts, c):
                return False
        return "QTY" not in spec.slots or v["QTY"] >= 0

    def _twin(self, spec: Spec):
        """One input slot moves across one boundary so that exactly one part of the construction table changes
        (the default version, the clause state, Q or the terms); the prediction is the table's answer (never solver
        A's) and the twin is kept only when the answer flips (G0 section 6)."""
        v, st = spec.env(), spec.structure
        n = st["n"]
        base = self._status(spec)
        base_ans = self._answer_st(spec, base)
        starts = [v[f"V{k}_START"] for k in range(1, n + 1)]
        cands = []
        for r in ROLES:
            for b in starts[1:]:
                cands += [(r, S.date_slot(x)) for x in (b - DAY, b)]
        if "SUNSET" in v:
            sun, dec = v["SUNSET"], v["DECISION_DATE"]
            cands += [("DECISION_DATE", S.date_slot(x)) for x in (sun, sun + DAY)]
            cands += [("SUNSET", S.date_slot(x)) for x in (dec - DAY, dec)]
        for k in range(2, n + 1):
            for r in ROLES:
                cands += [(f"V{k}_START", S.date_slot(x)) for x in (v[r], v[r] + DAY)]
        if spec.qform in OUTCOME_FORMS:
            g = _decide(base)
            t, q = base["terms"][g - 1], base["q"]
            if not st["qty"]:
                cands += [("QTY", _term_slot(st["tkind"], x)) for x in (t, t + 1)]
            cands += [(f"V{g}_TERM", _term_slot(st["tkind"], x)) for x in (q, q - 1) if x >= 1]
        seen = set()
        cands = [x for x in cands if (x[0], S.canonical(x[1])) not in seen and not seen.add((x[0], S.canonical(x[1])))
                 and S.canonical(x[1]) != S.canonical(spec.slots[x[0]])]
        cands.sort(key=lambda x: uhash(FAMILY, "twinop", spec.sampler, spec.seed, x[0], S.canonical(x[1])))
        for slot, new in cands:
            twin = spec.with_slot(slot, new)
            if not self._valid(twin):
                continue
            twin = self.derive(twin)
            st2 = self._status(twin)
            parts = [p for p in ("d0", "clause", "terms", "q") if st2[p] != base[p]]
            if len(parts) != 1:
                continue
            ans2 = self._answer_st(twin, st2)
            if ans2 == base_ans:
                continue
            return RelationProposal("twin", spec=twin, changed_slot=slot, expect=ans2, note=parts[0])
        return None

    def _metamorphic(self, spec: Spec) -> list:
        """G4 (checked, never emitted): renames and a common date shift leave the answer as predicted."""
        v, st = spec.env(), spec.structure
        out = []
        who = next(x for x in RESERVE_CUSTOMERS if x != v["CUSTOMER"])
        out.append(RelationProposal("metamorphic", spec=spec.with_slot("CUSTOMER", S.name_slot(who)), expect="same",
                                    note="rename the customer"))
        org = next(x for x in RESERVE_ORGS if x != v["ORG"])
        out.append(RelationProposal("metamorphic", spec=spec.with_slot("ORG", S.name_slot(org)), expect="same",
                                    note="rename the organisation"))
        shift = DAY * 35
        moved = {k: S.date_slot(s.value + shift) for k, s in spec.slots.items() if s.kind == "date"}
        out.append(RelationProposal("metamorphic", spec=spec.replace(slots={**spec.slots, **moved}), expect="same",
                                    note="shift every date by 35 days"))
        g = self._resolve(spec)
        ids = {v[f"V{k}_ID"] for k in range(1, st["n"] + 1)}
        new = next(x for x in RESERVE_IDS if x not in ids)
        out.append(RelationProposal("metamorphic", spec=spec.with_slot(f"V{g}_ID", S.id_slot(new)),
                                    expect=new if spec.qform == "ch_version" else "same",
                                    note="rename the gold version"))
        return out

    # ============================================================================================ error models
    def error_models(self) -> dict:
        if self._ems is None:
            ems = {}
            for name in VER_EM:
                def fn(spec, name=name):
                    if spec.qform not in ("ch_version", "ch_term"):
                        return None
                    k = self._resolve(spec, frozenset({name}))
                    if k is None:
                        return None
                    return spec.env()[f"V{k}_{'ID' if spec.qform == 'ch_version' else 'TERM'}"]
                ems[name] = error_model(name, fn)
            self._ems = ems
        return self._ems
