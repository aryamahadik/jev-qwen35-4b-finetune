"""families/T07/plugin.py: T07 "headline promise vs footnote qualifier" (C2_DATA_SPEC 2.1, 3.16; PREREG_FINAL A37).

An advertisement makes one or two headline promises (free shipping, free returns, a price match ...), each marked with
a symbol (* or †). The fine print marked with the same symbol narrows its headline by one to three conditions joined
by AND, from six dimensions: delivery region (only / excluded), product category (only / excluded), price status
(excluded), order date (on or before / before / on or after a date), membership level (a level and above / and
below, on a ladder the card prints) and order subtotal (at least / over an amount). The row shows the advertisement
(program banner lines + a Haiku skin), the fine print (program lines built from admitted lexicon clauses; on Mode F
rows the clauses sit inside Haiku's free text), the customer's order record and the card. The question asks whether
the asked headline holds for this order, which fine-print condition of the asked headline the order misses, or which
headlines hold.
Semantics: G0_SPEC_v2.md = G0_SPEC.md (v1 + redo2 notes) + section 8 (sha pinned below).

  solver A   rule AST: And over one Cmp per condition (Fn t07_rank on the printed ladder), run by rules.evaluate
                                                                                            paradigm ast_interpreter
  solver B   solver_b.py: its own parser of the RENDERED row (banner, fine-print lines and Mode F text through the
             lexicon scan, four record containers, the card's ladder, the wording template); each condition becomes
             the SET of attribute values it admits (finite include / exclude sets; integer intervals on day ordinals,
             cents and printed ladder ranks); the sets of one footnote are intersected per dimension and the order's
             point is tested for membership                                                  paradigm set_algebra
  samplers   S1 forward; S2 label-first near miss (boundary values, one failing condition, overlapping footnotes);
             S3 order-table first; S4 support-chat transcript first; S5 held out (JSON record, held-out stores,
             skins, registers and wordings)
  questions  yes/no on predicate "gets_benefit": yn_gets, yn_dneg_gets (double negation, positive); complements
             yn_misses (antonym), yn_not_gets (syntactic), yn_fails_to (implicit); ch_failing (which condition of
             the asked headline's fine print the order misses, + "None"); ch_offers (both / only A / only B / neither)
  relations  complement; minimal-edit twin (one customer attribute or one bound moved across its condition); equiv
             (another register and record container); inv (an inert customer message); G4 metamorphic (rename the
             customer or the store; shift every date by 7 days; another admitted paraphrase of a condition; reverse
             the fine-print order)
Balance by construction: seeds 2k and 2k+1 share the question form, the visible structure (headlines, conditions,
layout, skin and wording) and mirrored cards c / N-1-c whose rates r and 1-r come from one uniform draw, so exactly one
row of each yes/no pair gets the headline benefit (G0 S24). Code only: nothing here writes a file (A37 f).
"""
from __future__ import annotations

import copy
import datetime as dt
import functools
import random
from pathlib import Path
from typing import NamedTuple

from c2_kit import polarity as POL
from c2_kit import rules as RL
from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.choiceplan import ChoicePlan
from c2_kit.distractors import Option, OptionSet, build_closed, error_model, register_name, uhash
from c2_kit.lexicon import LexiconError
from c2_kit.plugin import C2Plugin, ContractError, QuestionForm, RelationProposal, Spec, choose_forms
from c2_kit.relations import abstain_twin_kept
from c2_kit.rows import TextBuilder, assemble_row

HERE = Path(__file__).resolve().parent
FAMILY = "T07"
TD = dt.timedelta

# ------------------------------------------------------------------------------------------------ closed pools
# Program-side seed pools (G0_SPEC.md S2). After A38 they are extended from Haiku packs by program. Every surface is
# unique across all category sets, so a surface names one value of one dimension.
HEADLINES = {
    "free_shipping": ["Free shipping on every order"],
    "free_returns": ["Free returns on every purchase"],
    "price_match": ["We match any lower price"],
    "lifetime_warranty": ["A lifetime warranty on everything we sell"],
    "double_points": ["Double reward points on every purchase"],
    "free_assembly": ["Free assembly with every delivery"],
    "gift_wrap": ["Free gift wrapping at checkout"],
    "free_installation": ["Free installation for every appliance"],
}
BENEFITS = {
    "free_shipping": ["free shipping"], "free_returns": ["free returns"], "price_match": ["the price match"],
    "lifetime_warranty": ["the lifetime warranty"], "double_points": ["double reward points"],
    "free_assembly": ["free assembly"], "gift_wrap": ["free gift wrapping"],
    "free_installation": ["free installation"],
}
REGIONS = {k.lower(): [k] for k in ("Arvale", "Brenmoor", "Calderon", "Dunmere", "Eskarth", "Fallowmere",
                                    "Greyhaven", "Hollin")}
CATEGORIES = {"kitchenware": ["kitchenware"], "garden_tools": ["garden tools"], "furniture": ["furniture"],
              "electronics": ["electronics"], "toys": ["toys"], "bedding": ["bedding"],
              "sports_gear": ["sports gear"], "pet_supplies": ["pet supplies"]}
STATUSES = {"regular_price": ["regular price"], "clearance": ["clearance"], "final_sale": ["final sale"],
            "open_box": ["open box"], "refurbished": ["refurbished"], "pre_order": ["pre-order"]}
TIERS = {k.lower(): [k] for k in ("Bronze", "Silver", "Gold", "Platinum", "Basic", "Plus", "Premier", "Elite",
                                  "Green", "Blue", "Black")}
LADDERS = (("bronze", "silver", "gold", "platinum"), ("basic", "plus", "premier", "elite"),
           ("green", "blue", "black"))
# G0 S2 (H6): a store or customer name never holds a closed-set surface as a whole word (casefold)
STORES = ("Fernway Market", "Brightwell Home", "Kestrel Outfitters", "Copperleaf Kitchen", "Northvale Audio",
          "Bluecrest Sports", "Harborlight Goods", "Tidewell Supply", "Cedarline Living", "Pebblestone Garden",
          "Larkspur Playthings", "Marigold Pets", "Oakhurst Interiors", "Birchwood Linens", "Juniper Gadgets",
          "Wrenfield Outdoor")
STORES_HELD = ("Quaymoor Traders", "Elmstead Emporium", "Rowanbrook Store", "Thistledown Supply")
CUSTOMERS = ("Dana Okafor", "Lena Whitcombe", "Ravi Anand", "Mira Castell", "Tomas Ferreira", "Aiko Brandt",
             "Jonah Pryce", "Selin Yilmaz", "Priya Raman", "Hugo Lindqvist", "Nadia Haddad", "Owen Mensah",
             "Clara Voss", "Felix Moreau", "Ines Duarte", "Kofi Asante")
CUSTOMERS_HELD = ("Petra Halvorsen", "Matteo Rinaldi", "Yara Celik", "Bram Dekker")

# ------------------------------------------------------------------------------------------------ semantics
DIMS = ("region", "category", "status", "date", "tier", "spend")
ATTR = {"region": "REGION", "category": "CATEGORY", "status": "STATUS", "date": "ORDER_DATE", "tier": "TIER",
        "spend": "SUBTOTAL"}
CAT_SET = {"region": REGIONS, "category": CATEGORIES, "status": STATUSES, "tier": TIERS}
BOUND_KIND = {"region": "category", "category": "category", "status": "category", "date": "date",
              "tier": "category", "spend": "cents"}
SEMS = {   # sem id -> (dimension, operator, lexicon kind, meaning shown to the G-LEX extractors)
    "t07.region.in": ("region", "in", "other", "only orders delivered to the named region get the headline benefit"),
    "t07.region.out": ("region", "out", "other",
                       "orders delivered to the named region are excluded from the headline benefit"),
    "t07.category.in": ("category", "in", "other",
                        "only items in the named product category get the headline benefit"),
    "t07.category.out": ("category", "out", "other",
                         "items in the named product category are excluded from the headline benefit"),
    "t07.status.out": ("status", "out", "other",
                       "items with the named price status are excluded from the headline benefit"),
    "t07.date.le": ("date", "le", "temporal", "the order must be placed on the named date or earlier"),
    "t07.date.lt": ("date", "lt", "temporal", "the order must be placed strictly before the named date"),
    "t07.date.ge": ("date", "ge", "temporal", "the order must be placed on the named date or later"),
    "t07.spend.ge": ("spend", "ge", "comparator", "the order subtotal must be at least the named amount"),
    "t07.spend.gt": ("spend", "gt", "comparator", "the order subtotal must be strictly greater than the named amount"),
    "t07.tier.min": ("tier", "min", "comparator",
                     "the customer's membership level must be the named level or a higher one"),
    "t07.tier.max": ("tier", "max", "comparator",
                     "the customer's membership level must be the named level or a lower one"),
}
CLAUSE_KINDS = ("other", "temporal", "comparator")
A_OP = {"in": "==", "out": "!=", "le": "<=", "lt": "<", "ge": ">=", "gt": ">", "min": ">=", "max": "<="}
OP_WEIGHTS = {"region": (("t07.region.in", .5), ("t07.region.out", .5)),
              "category": (("t07.category.in", .5), ("t07.category.out", .5)),
              "status": (("t07.status.out", 1.0),),
              "date": (("t07.date.le", .45), ("t07.date.lt", .25), ("t07.date.ge", .30)),
              "tier": (("t07.tier.min", .6), ("t07.tier.max", .4)),
              "spend": (("t07.spend.ge", .6), ("t07.spend.gt", .4))}
DIM_WEIGHTS = (("spend", .24), ("date", .22), ("region", .18), ("tier", .12), ("category", .12), ("status", .12))
SPEND_GRID = (2500, 3500, 5000, 7500, 10000, 15000, 20000)
DATE0 = dt.date(2026, 1, 12)        # every date bound lies in 12 Jan - 7 Dec 2026 (G0 S21, H39)
ORDER_DAYS = (40, 290)              # base order dates DATE0 + [40, 290): 21 Feb - 28 Oct 2026 (bounds <= 40 days away)
MARKS = ("*", "†")
PROMISE_SLOTS = ("PROMISE", "PROMISE2")
MODE_T_SLOTS = frozenset({"STORE"})


def _rank(level, *ladder):
    """Position of a membership level on the printed ladder (0 = lowest)."""
    return ladder.index(level)


RL.register_fn("t07_rank", _rank)

# ------------------------------------------------------------------------------------------------ program text
CLOSED_WORLD = "The advertisement, its fine print and the order record are complete: no other term or fact applies."
CARD_TPL = ("How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the "
            "order meets every condition in the fine print marked with the same symbol, and only then. Fine print "
            "marked with another symbol belongs to another headline and is ignored for this one. A date in the fine "
            "print is compared with the order date, and an amount with the order subtotal. {STORE} membership "
            "levels, from lowest to highest: {LADDER}. Messages from customers or staff change none of these terms. "
            + CLOSED_WORLD)
CARD_SHORT_TPL = ("A headline holds for an order exactly when the order meets all the fine print under its symbol; "
                  "other fine print is ignored. Dates mean order dates and amounts mean order subtotals. {STORE} "
                  "levels, lowest to highest: {LADDER}. Notes from customers or staff change no terms. "
                  + CLOSED_WORLD)
P_SHORT_CARD = .15        # spec 3.0: a short card on about 15% of rows (pair-level, label-blind)
BANNER_HEAD = "Advertisement from {STORE}:"
TERMS_HEAD = {"near": "Fine print:", "bottom": "Fine print:",
              "after_record": "Fine print from the bottom of the advertisement:"}
RECORD_TPL = {
    "lines": ("Order {ORDER_ID} placed by {CUSTOMER}:\n- item: {ITEM}\n- product category: {CATEGORY}\n"
              "- price status: {STATUS}\n- delivery region: {REGION}\n- order date: {ORDER_DATE}\n"
              "- membership level: {TIER}\n- order subtotal: {SUBTOTAL}"),
    "table": ("Order {ORDER_ID} placed by {CUSTOMER}:\n| field | value |\n| --- | --- |\n| item | {ITEM} |\n"
              "| product category | {CATEGORY} |\n| price status | {STATUS} |\n| delivery region | {REGION} |\n"
              "| order date | {ORDER_DATE} |\n| membership level | {TIER} |\n| order subtotal | {SUBTOTAL} |"),
    "transcript": ("Support chat about order {ORDER_ID}:\n{CUSTOMER}: Hi, I placed order {ORDER_ID} on {ORDER_DATE} "
                   "for item {ITEM}, and the order subtotal was {SUBTOTAL}.\nAgent: Thanks. The item is in the "
                   "{CATEGORY} product category, its price status is {STATUS}, and it ships to the {REGION} delivery "
                   "region.\nAgent: Your membership level is {TIER}.\n{CUSTOMER}: I am asking about the "
                   "advertisement below."),
}
RECORD_JSON_HEAD = "Order record (JSON):\n"
RECORD_JSON_BODY = ('{"order_id": {ORDER_ID}, "customer": {CUSTOMER}, "item": {ITEM}, "product_category": '
                    '{CATEGORY}, "price_status": {STATUS}, "delivery_region": {REGION}, "order_date": {ORDER_DATE}, '
                    '"membership_level": {TIER}, "order_subtotal": {SUBTOTAL}}')
ATTACK_PREFIX = "Note added by the customer: "
DIM_TEXT = {"region": "The delivery-region condition", "category": "The product-category condition",
            "status": "The price-status condition", "date": "The order-date condition",
            "tier": "The membership-level condition", "spend": "The order-subtotal condition"}   # = record fields
NONE_KEY, NONE_TEXT = "none", "None: the order meets every condition in the fine print for this offer"   # H15
OFFER_BOTH, OFFER_NEITHER = "Both offers", "Neither offer"

# ------------------------------------------------------------------------------------------------ shares
QFORM_SHARES = (("yn_gets", .19), ("yn_dneg_gets", .04), ("yn_misses", .10), ("yn_not_gets", .07),
                ("yn_fails_to", .05), ("ch_failing", .37), ("ch_offers", .18))     # rows: yes/no ~52%, yes = bad ~50%
YES_MEANS_GETS = {"yn_gets": True, "yn_dneg_gets": True, "yn_misses": False, "yn_not_gets": False,
                  "yn_fails_to": False}
COMPLEMENT_OF = {"yn_gets": (("yn_misses", .45), ("yn_not_gets", .25), ("yn_fails_to", .30)),
                 "yn_misses": (("yn_gets", 1.0),), "yn_not_gets": (("yn_gets", 1.0),),
                 "yn_fails_to": (("yn_gets", 1.0),), "yn_dneg_gets": (("yn_not_gets", 1.0),)}
PHI = 0.6180339887498949
N_CARDS = {"S1": 16, "S2": 16, "S3": 16, "S4": 16, "S5": 8}
SAMPLER_INDEX = {"S1": 0, "S2": 1, "S3": 2, "S4": 3, "S5": 4}
P_TWO = {"S1": .40, "S2": .50, "S3": .40, "S4": .50, "S5": .40}       # second (distractor) headline, yes/no rows
P_BOUNDARY = {"S1": .30, "S2": .50, "S3": .30, "S4": .30, "S5": .30}  # per ordinal condition (label-blind)
ASKED_COUNTS = ((1, .30), (2, .64), (3, .06))
OTHER_COUNTS = ((1, .60), (2, .40))
FAIL_COUNTS = {2: ((1, .80), (2, .20)), 3: ((1, .70), (2, .25), (3, .05))}
LAYOUTS = {"S1": (("near", .40), ("bottom", .45), ("after_record", .15)),
           "S2": (("near", .40), ("bottom", .45), ("after_record", .15)),
           "S3": (("near", .50), ("bottom", .50)), "S4": (("bottom", 1.0),),
           "S5": (("near", .50), ("bottom", .50))}
CONTAINER = {"S1": "lines", "S2": "lines", "S3": "table", "S4": "transcript", "S5": "json"}
# G0 v2 S17 / S18 (fix iteration 1; STAGE_B_PILOT_REPORT "patterns across families"): the ch_failing "None" option is gold
# on exactly 1/k of the rows that show it (k = the options shown, None included; was a flat 25%, which put it at 21% of
# k = 2 rows and made it predictive: G6 choice +4-6 pp, G10 gold-is-longest -5.1 pp). Its display slot and the ch_offers
# outcome are stratified by index too (T07Plugin.row_plan: the idea of c2_kit.choiceplan, drawn before any structure).
P_FREEFORM = .35          # share of rows that use a compatible Mode F skin when one exists (cap: 40%, spec 3.0)
P_COMPLEMENT, P_EQUIV, P_INV, P_TWIN = .55, .13, .07, .45
P_TWIN_CHOICE = .70      # choice bases: higher, since twin_none_keep thins the ch_failing twins (keeps the 4.1 shares)
WINDOW_PAIRS = 2048      # choice streams stratify inside windows of 2,048 seed pairs (4,096 seeds) of a sampler


def twin_none_keep(closed: int) -> float:
    """ch_failing twins that move the gold onto "None: the order meets every condition" (fixing the one failing
    condition) are kept at 1 / closed^2, closed = the dimension labels of the row (k - 1), so that "None" stays gold on
    1/k of ALL emitted ch_failing rows of a k-cell (kit relations.abstain_twin_kept). With a = 1/k: a twin of a "None"
    base always lands on a dimension (a twins per base), a twin of a dimension base lands on "None" at the keep rate
    kappa ((1 - a) kappa twins per base), so the twins' None share is (1 - a) kappa / ((1 - a) kappa + a), which is
    exactly a when kappa = a^2 / (1 - a)^2 = 1 / (k - 1)^2."""
    return 1.0 / (closed * closed)


def strat(sampler: str, name: str, idx: int, n: int) -> int:
    """A value of range(n) for the idx-th item of a stream, each value exactly once in every block of n consecutive
    indices (a seeded permutation per block). Label-blind: it reads the sampler, the stream name and the index only.
    Stratifying (rather than drawing each item alone) keeps the realised shares of a ~1,000-row pilot on their plan:
    an independent draw of the choice rows' abstain gold moves G10's gold-is-longest by about 2 pp (1 SD) against a
    +/- 2 pp bar (the T35 lesson)."""
    blk, pos = divmod(idx, n)
    order = sorted(range(n), key=lambda v: uhash(FAMILY, "strat", name, sampler, blk, v))
    return order[pos]


def failing_dims(stc: dict) -> list:
    """The dimension labels a ch_failing row lists, in printed-structure order: every dimension of the asked footnote,
    then each further dimension of the other footnote once (G0 S17)."""
    a = stc["asked"]
    dims = [c[0] for c in stc["promises"][a]["conds"]]
    for p, prom in enumerate(stc["promises"]):
        dims += [c[0] for c in prom["conds"] if p != a and c[0] not in dims]
    return dims


class RowPlan(NamedTuple):
    """What a choice row's sampler fixes before drawing structure (T07Plugin.row_plan)."""
    k: int                # options shown
    gold_abstain: bool    # ch_failing: the gold is "None"
    abstain_slot: int     # ch_failing: the display position of "None" (-1: no abstain option)
    outcome: int          # ch_offers: stratified outcome index (-1: not a ch_offers row)


def offers_holds(outcome: int, keys: tuple) -> tuple:
    """(holds of headline 0, holds of headline 1) for a ch_offers outcome index 0-3: both, neither, only the headline
    whose option text ("Only <benefit>") is the LONGER one, only the other. Indexing by text length (never by label) and
    stratifying the index makes the gold the longest option on exactly 1/4 of the rows per block, whatever the benefit
    names are (a tie gives each "Only" option half credit in G10, which is symmetric)."""
    n = [len(BENEFITS[k][0]) for k in keys]
    longer = 0 if n[0] >= n[1] else 1
    if outcome == 0:
        return (True, True)
    if outcome == 1:
        return (False, False)
    return tuple((i == longer) == (outcome == 2) for i in (0, 1))


EQUIV_REGISTERS = ("web_banner", "app_banner", "flyer", "catalogue", "checkout_note")      # Mode T only (G0 S14)
EQUIV_REGISTERS_HELD = ("loyalty_newsletter", "shelf_tag")

register_name("t07_wrong_footnote", "applies the fine print marked for the other headline")
register_name("t07_all_footnotes", "applies every footnote on the page to the asked headline")
register_name("t07_exclusion_as_restriction", "reads an exclusion ('excludes X') as a restriction ('X only')")
register_name("t07_restriction_as_exclusion", "reads a restriction ('X only') as an exclusion ('excludes X')")
register_name("t07_tier_exact", "reads 'X members and above' as 'X members only'")
register_name("t07_reversed_bound", "reads a date, amount or level bound the wrong way round ('on or before' as "
              "'on or after', 'or more' as 'or less', 'and above' as 'and below')")
register_name("t07_first_condition_only", "checks only the first condition of the fine print")
EM_VARIANTS = {"ignore_qualifier": frozenset({"ignore"}), "t07_wrong_footnote": frozenset({"wrong_foot"}),
               "t07_all_footnotes": frozenset({"all_foot"}), "drop_inclusive_endpoint": frozenset({"drop_incl"}),
               "add_exclusive_endpoint": frozenset({"add_excl"}),
               "t07_exclusion_as_restriction": frozenset({"excl_as_in"}),
               "t07_restriction_as_exclusion": frozenset({"in_as_excl"}),
               "t07_tier_exact": frozenset({"tier_exact"}), "t07_reversed_bound": frozenset({"reverse"}),
               "t07_first_condition_only": frozenset({"first_only"})}


# The negative / antonym predicates of "gets the benefit" (c2_kit.polarity rules P1-P3; G0 v2 S19). A question wording
# negates the predicate syntactically ("does not get") OR uses one of these ("lose out on", "forfeit", "fail to"), never
# both, and never opens with a contracted negative frame ("Isn't it the case that ... doesn't get ...?"), which reads
# either way. negcount's own implicit cues (fail to, deny, lack, prevent ... from, refuse to, without, false ...) count
# too; these are the ones it does not list.
NEGATIVE_PREDICATES = (
    r"los(?:e|es|ing)\s+out|lost\s+out", r"forfeit(?:s|ed|ing)?", r"miss(?:es|ed|ing)?\s+out", r"shut\s+out",
    r"(?:go|goes|going|went)\s+without", r"fall(?:s|ing)?\s+short|fell\s+short", r"withh(?:o|e)ld(?:s|ing)?",
    r"exclud(?:e|es|ed|ing)", r"reject(?:s|ed|ing)?", r"refus(?:e|es|ed|ing)", r"den(?:y|ies|ied|ying)",
    r"bar(?:s|red|ring)?\s+from", r"block(?:s|ed|ing)?\s+from",
)


def _weighted(rng: random.Random, table):
    u, acc = rng.random(), 0.0
    for v, w in table:
        acc += w
        if u < acc:
            return v
    return table[-1][0]


def _cat(key: str, table: dict) -> S.Slot:
    return S.category_slot(key, table)


def card_rate(card: int, n_cards: int) -> float:
    """Per-card rate of the yes/no pivot, evenly spread over 20-80% (spec 3.0); r(N-1-c) = 1 - r(c)."""
    return 0.2 + 0.6 * (card + 0.5) / n_cards


def _draw_qform(sampler: str, pair: int) -> str:
    """Stratified, label-blind: a golden-ratio sequence over pair indices meets the shares within about 1/n."""
    u, acc = (pair * PHI + uhash(FAMILY, "qform", sampler)) % 1.0, 0.0
    for q, share in QFORM_SHARES:
        acc += share
        if u < acc:
            return q
    return QFORM_SHARES[-1][0]


@functools.lru_cache(maxsize=None)
def pack_of(sampler: str, fam: int) -> tuple:
    """The pack of mirrored cards fam and N-1-fam (store and membership ladder; label-blind)."""
    i = SAMPLER_INDEX[sampler] * 8 + fam
    stores = STORES_HELD if sampler == "S5" else STORES
    return (("ladder", LADDERS[i % len(LADDERS)]), ("pack", f"t07-placeholder-{i:02d}"),
            ("store", stores[i % len(stores)]))


def offer_key(holds: tuple, keys: tuple) -> str:
    if all(holds):
        return "both"
    if not any(holds):
        return "neither"
    return "only:" + keys[holds.index(True)]


def bound_params(dim: str) -> tuple:
    """Slot params of a bound of `dim` (category sets, USD cents)."""
    if dim in CAT_SET:
        return _cat(sorted(CAT_SET[dim])[0], CAT_SET[dim]).params
    if dim == "spend":
        return S.cents_slot(0).params
    return ()


class T07Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "everyday"
    G0_LITE = HERE / "G0_SPEC_v2.md"
    G0_SHA256 = "23e31c2badd5643b5249781cbb84ae0381368f18af331ed615c62368f8c2bf5a"   # frozen v2 (14 Oct 2026, fix iteration 1)
    # v1 + redo2 notes R1-R5 (G0_SPEC.md): the spec the Haiku tasks, the pools and the extraction records were authored under
    G0_SHA256_AUTHORED = "c474992824be67c98e0e91c7bd96cf4663147d83b7b2d105b565b16b756f66a3"
    G0_AMBIGUITY_PASS = {"task_id": "c2-data-stage-a/amb:T07", "model": "haiku",
                         "read_g0_sha256": "8bfd3a57f932e145bdedaafaf252f3652205e63654fbce4c023d2fd2cb320e5a",
                         "points": 47, "resolved": 47,
                         "record": "haiku/ambiguity/amb_T07_points.json"}
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "ast_interpreter"
    PARADIGM_B = "set_algebra"
    SOLVER_B_MODULE = "families.T07.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm("yn_gets", "noul", "gets_benefit", 1, yes_is_bad=False),
        QuestionForm("yn_misses", "noul", "gets_benefit", -1, "antonym", yes_is_bad=True),
        QuestionForm("yn_not_gets", "noul", "gets_benefit", -1, "syntactic", yes_is_bad=True),
        QuestionForm("yn_fails_to", "noul", "gets_benefit", -1, "implicit", yes_is_bad=True),
        QuestionForm("yn_dneg_gets", "noul", "gets_benefit", 1, yes_is_bad=False),
        QuestionForm("ch_failing", "choice", answer_set="closed", abstain=True),
        QuestionForm("ch_offers", "choice", answer_set="closed"),
    )}
    LABEL_WORDS = ("qualify", "eligible", "ineligible", "entitled", "honour", "honor", "miss out", "missed out",
                   "left out")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("web_banner", "app_banner", "flyer", "catalogue", "checkout_note", "email_promo", "sms",
                 "social_post", "warranty_card", "loyalty_newsletter", "shelf_tag", "voice_promo")
    HELD_OUT_REGISTERS = ("loyalty_newsletter", "shelf_tag", "voice_promo")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW = ()
    POLARITY_CHECK = True                 # c2_kit.polarity: yes/no wordings must read with their form's polarity (G0 v2 S19)
    POLARITY_NEGATIVES = NEGATIVE_PREDICATES
    POLARITY_STRICT_FRAMES = True         # also refuse "aux + subject + not" (no frozen wording breaks it: free)

    def __init__(self, lexicon=None):
        super().__init__(lexicon)
        self._sig_cache: dict = {}
        self._cells: dict = {}             # (sampler, window) -> choice-stream index tables (choice_cell)
        self._fids: dict = {}              # (sem, sampler, lexicon size) -> admitted form ids (_form_ids)
        self._screened: list = []          # [(ctx, screened ctx, {wording id: problems})]

    # ------------------------------------------------------------------------------------------- polarity (G0 v2 S19)
    def ctx_for(self, spec, ctx):
        """The kit context without the wordings that break the polarity rule (c2_kit.polarity; 6 contracted
        yn_dneg_gets wordings in the frozen pool), so neither render() nor the pipeline's complement partner can pick one.
        Cached per context object."""
        for c, screened, _bad in self._screened:
            if c is ctx:
                return screened
        screened, bad = POL.screen(ctx, self)
        self._screened.append((ctx, screened, bad))
        return screened

    def quarantined_wordings(self, ctx) -> dict:
        """{wording skin id: polarity problems} for the wordings ctx_for() leaves out of `ctx`."""
        self.ctx_for(None, ctx)
        return next(bad for c, _s, bad in self._screened if c is ctx)

    # ------------------------------------------------------------------------------------------- sampling
    def _form_ids(self, sem: str, sampler: str) -> list:
        """Admitted condition forms of a sem for a sampler (training forms; held-out ones for S5 when it has any).
        Cached per plugin instance: the registry is not changed while an instance samples (the choice streams replay the
        structure draws of a whole window, so this is called ~10^5 times)."""
        if self.lexicon is None:
            raise ContractError("T07 needs its lexicon registry (T07Plugin(lexicon=...))")
        hit = self._fids.get((sem, sampler))
        if hit is None:
            ids = sorted(f for f, x in self.lexicon.forms.items()
                         if x.sem_id == sem and self.lexicon.status(f) == "admitted")
            held = [f for f in ids if self.lexicon.forms[f].held_out]
            if sampler in self.HELD_OUT_SAMPLERS and held:
                ids = held
            else:
                ids = [f for f in ids if f not in held] or ids
            hit = self._fids[(sem, sampler)] = ids
        if not hit:
            raise ContractError(f"no admitted condition form for {sem}")
        return list(hit)

    def _draw_dims(self, rng: random.Random, k: int, overlap=None) -> list:
        pool = list(DIM_WEIGHTS)
        out = []
        if overlap:
            first = rng.choice(sorted(overlap))
            out.append(first)
            pool = [(d, w) for d, w in pool if d != first]
        while len(out) < k:
            tot = sum(w for _, w in pool)
            d = _weighted(rng, [(d, w / tot) for d, w in pool])
            out.append(d)
            pool = [(x, w) for x, w in pool if x != d]
        rng.shuffle(out)
        return out

    def _draw_structure(self, prng: random.Random, sampler: str, qform: str, pack: dict) -> tuple:
        """Pair-level (label-blind) structure: headlines, conditions and their admitted wordings, layout."""
        if qform == "ch_offers":
            two, asked = True, None
            counts = [1, 1] if prng.random() < .85 else ([2, 1] if prng.random() < .5 else [1, 2])
        else:
            two = prng.random() < P_TWO[sampler]
            asked = prng.randrange(2) if two else 0
            counts = [0, 0] if two else [0]
            counts[asked] = _weighted(prng, ASKED_COUNTS)
            if two:
                counts[1 - asked] = _weighted(prng, OTHER_COUNTS)
        keys = tuple(prng.sample(sorted(HEADLINES), len(counts)))
        dims = [None] * len(counts)
        first = asked if asked is not None else 0
        dims[first] = self._draw_dims(prng, counts[first])
        for p in range(len(counts)):
            if p != first:
                overlap = set(dims[first]) if (sampler == "S2" and prng.random() < .6) else None
                dims[p] = self._draw_dims(prng, counts[p], overlap)
        promises, clauses = [], {}
        for p, ds in enumerate(dims):
            conds = []
            for d in ds:
                sem = _weighted(prng, OP_WEIGHTS[d])
                bslot, cslot = f"P{p + 1}_{d.upper()}", f"P{p + 1}_Q_{d.upper()}"
                clauses[cslot] = prng.choice(self._form_ids(sem, sampler))
                conds.append([d, bslot, cslot])
            promises.append({"slot": PROMISE_SLOTS[p], "mark": MARKS[p], "conds": conds})
        foot_order = ([0, 1] if prng.random() < .5 else [1, 0]) if len(counts) == 2 else [0]
        container = CONTAINER[sampler]
        stc = {"v": "T07.v1", "promises": promises, "asked": asked, "foot_order": foot_order,
               "layout": _weighted(prng, LAYOUTS[sampler]), "container": container,
               "record_first": sampler in ("S3", "S4", "S5"),
               "card": "short" if prng.random() < P_SHORT_CARD else "full",
               "ladder": [f"TL{i}" for i in range(len(pack["ladder"]))]}
        return stc, clauses, keys

    def _design(self, srng: random.Random, sampler: str, qform: str, stc: dict, positive: bool, plan=None,
                keys=None) -> list:
        """Pass / fail of every condition (the gold design; values are drawn to realise it). Choice rows are label-first
        from their plan (G0 v2 S17 / S18): ch_failing's gold is "None" iff plan.gold_abstain; ch_offers' outcome index
        (stratified) picks both / neither / only the longer or the shorter "Only <benefit>" option."""
        proms = stc["promises"]

        def fail_some(n):
            k = 1 if (sampler == "S2" or n == 1) else _weighted(srng, FAIL_COUNTS[n])
            bad = set(srng.sample(range(n), k))
            return [i not in bad for i in range(n)]

        out = [[True] * len(p["conds"]) for p in proms]
        if qform == "ch_offers":
            holds = offers_holds(plan.outcome, keys)
            for p, prom in enumerate(proms):
                n = len(prom["conds"])
                out[p] = [True] * n if holds[p] else fail_some(n)
            return out
        a = stc["asked"]
        n = len(proms[a]["conds"])
        if qform == "ch_failing":                          # gold "none" iff the plan says (1/k), else one condition
            g = n if plan.gold_abstain else srng.randrange(n)
            out[a] = [i != g for i in range(n)]
        else:
            out[a] = [True] * n if positive else fail_some(n)
        for p, prom in enumerate(proms):
            if p != a:
                out[p] = [srng.random() < .5 for _ in prom["conds"]]
        return out

    @staticmethod
    def _assign_cat(srng, cs: list, universe: list) -> tuple:
        a = srng.choice(universe)
        b = {}
        for bslot, op, ok, _bd in cs:
            same = (op == "in") == ok                       # in + pass or out + fail: the bound is the order's value
            b[bslot] = a if same else srng.choice([x for x in universe if x != a])
        return a, b

    @staticmethod
    def _assign_status(srng, cs: list) -> tuple:
        """No bound is ever "regular price", and a record that a status condition reads never shows it either, so
        neither the record value nor the bound alone hints at the outcome."""
        marked = [k for k in sorted(STATUSES) if k != "regular_price"]
        a = srng.choice(marked) if cs else ("regular_price" if srng.random() < .45 else srng.choice(marked))
        b = {}
        for bslot, _op, ok, _bd in cs:
            b[bslot] = a if not ok else srng.choice([x for x in marked if x != a])
        return a, b

    @staticmethod
    def _assign_date(srng, cs: list) -> tuple:
        a = DATE0 + TD(days=srng.randrange(*ORDER_DAYS))
        b = {}
        for bslot, op, ok, bd in cs:
            k = TD(days=1 if bd else srng.randint(2, 40))
            if op == "le":          # passes iff order date <= bound; boundary: equal (pass) or one day late (fail)
                b[bslot] = (a if bd else a + k) if ok else a - k
            elif op == "lt":        # passes iff order date < bound; boundary: one day early (pass) or equal (fail)
                b[bslot] = a + k if ok else (a if bd else a - k)
            else:                   # ge: passes iff order date >= bound; boundary: equal (pass) or one day early (fail)
                b[bslot] = (a if bd else a - k) if ok else a + k
        return a, b

    @staticmethod
    def _assign_spend(srng, cs: list) -> tuple:
        """Bounds first (uniform over the grid: a bound alone never hints at the outcome), then the subtotal inside the
        band the designed outcomes allow, near the bounds. A boundary condition puts it at its bound or 1 cent across
        (at most one per dimension); otherwise it stays more than 1 cent from every bound."""
        if not cs:
            return srng.randrange(1500, 25000), {}
        for _ in range(200):
            b = {bslot: srng.choice(SPEND_GRID) for bslot, *_ in cs}
            lo = max([b[s] + (op == "gt") for s, op, ok, _ in cs if ok], default=None)
            hi = min([b[s] - (op == "ge") for s, op, ok, _ in cs if not ok], default=None)
            if lo is None or hi is None or lo + 4 <= hi:
                break
        else:
            raise ContractError("no subtotal satisfies the designed spend outcomes")
        flagged = next(((s, op, ok) for s, op, ok, bd in cs if bd), None)
        if flagged is not None:
            s, op, ok = flagged
            a = b[s] + {("ge", True): 0, ("ge", False): -1, ("gt", True): 1, ("gt", False): 0}[(op, ok)]
            if (lo is None or a >= lo) and (hi is None or a <= hi):
                return a, b
        for _ in range(200):
            if lo is not None and hi is not None:
                a = srng.randint(lo + 2, hi - 2)
            elif lo is not None:
                a = srng.randint(lo + 2, lo + max(300, lo * 3 // 10))
            else:
                a = srng.randint(max(1000, hi - max(300, hi * 3 // 10)), hi - 2)
            if all(abs(a - x) > 1 for x in b.values()):
                return a, b
        raise ContractError("no subtotal away from every bound")

    @staticmethod
    def _assign_tier(srng, cs: list, ladder: tuple) -> tuple:
        """Bounds first (uniform over the levels a rule can name: never the lowest for "and above", never the highest
        for "and below"; a bound alone never hints at the outcome), then the record's level inside the range the
        designed outcomes allow. A boundary condition puts it at its bound (pass) or one level across (fail)."""
        m = len(ladder)
        if not cs:
            return ladder[srng.randrange(m)], {}
        for _ in range(200):
            rb = {bslot: (srng.randint(1, m - 1) if op == "min" else srng.randint(0, m - 2)) for bslot, op, *_ in cs}
            lo = max([rb[s] if op == "min" else rb[s] + 1 for s, op, ok, _ in cs if (op == "min") == ok], default=0)
            hi = min([rb[s] - 1 if op == "min" else rb[s] for s, op, ok, _ in cs if (op == "min") != ok],
                     default=m - 1)
            if lo <= hi:
                break
        else:
            raise ContractError("no membership level satisfies the designed outcomes")
        r = None
        flagged = next(((s, op, ok) for s, op, ok, bd in cs if bd), None)
        if flagged is not None:
            s, op, ok = flagged
            r0 = rb[s] if ok else (rb[s] - 1 if op == "min" else rb[s] + 1)
            r = r0 if lo <= r0 <= hi else None
        if r is None:
            r = srng.randint(lo, hi)
        return ladder[r], {s: ladder[x] for s, x in rb.items()}

    def _assign(self, srng, sampler: str, stc: dict, clauses: dict, out: list, ladder: tuple) -> dict:
        by_dim: dict = {}
        for p, prom in enumerate(stc["promises"]):
            for i, (dim, bslot, cslot) in enumerate(prom["conds"]):
                op = SEMS[self.lexicon.forms[clauses[cslot]].sem_id][1]
                bd = dim in ("date", "spend", "tier") and srng.random() < P_BOUNDARY[sampler]
                by_dim.setdefault(dim, []).append((bslot, op, out[p][i], bd))
        vals = {}
        for dim in DIMS:
            cs = by_dim.get(dim, [])
            if dim in ("region", "category"):
                a, b = self._assign_cat(srng, cs, sorted(CAT_SET[dim]))
            elif dim == "status":
                a, b = self._assign_status(srng, cs)
            elif dim == "date":
                a, b = self._assign_date(srng, cs)
            elif dim == "spend":
                a, b = self._assign_spend(srng, cs)
            else:
                a, b = self._assign_tier(srng, cs, ladder)
            vals[ATTR[dim]] = a
            vals.update(b)
        return vals

    def _bound_slot(self, dim: str, value) -> S.Slot:
        if dim in CAT_SET:
            return _cat(value, CAT_SET[dim])
        return S.date_slot(value) if dim == "date" else S.cents_slot(value)

    def _pair_draw(self, sampler: str, pair: int) -> tuple:
        """The pair-level, label-blind draws of sample() (qform, card index, pack, structure, clause forms, headline
        keys): a pure function of (sampler, pair, the lexicon). Fresh objects on every call."""
        prng = random.Random(f"{FAMILY}|{sampler}|pair|{pair}")
        qform = _draw_qform(sampler, pair)
        n = N_CARDS[sampler]
        c0 = prng.randrange(n)
        pack = dict(pack_of(sampler, min(c0, n - 1 - c0)))
        stc, clauses, keys = self._draw_structure(prng, sampler, qform, pack)
        return qform, c0, pack, stc, clauses, keys

    def choice_cell(self, sampler: str, pair: int) -> tuple:
        """(cell, n_before, window) of a choice pair: cell = the number of dimension labels (ch_failing) or 4
        (ch_offers); window = pair // WINDOW_PAIRS; n_before = the choice pairs of the same form and cell before it in
        its window of the sampler's pair order. A row's index in its stream is 2 * n_before + side, so the plan's strata
        run over the pairs a sampler actually draws (a replay of the label-blind structure draws of one window, cached;
        blocks of k rows stratify inside a window, so a window of 4,096 seeds holds every cell's blocks whole to +/- 1
        row). Label-blind: no gold is read."""
        win = pair // WINDOW_PAIRS
        tab = self._cells.get((sampler, win))
        if tab is None:
            tab, seen = {}, {}
            for p in range(win * WINDOW_PAIRS, (win + 1) * WINDOW_PAIRS):
                q = _draw_qform(sampler, p)
                if q in ("ch_failing", "ch_offers"):
                    cell = len(failing_dims(self._pair_draw(sampler, p)[3])) if q == "ch_failing" else 4
                    tab[p] = (cell, seen.get((q, cell), 0))
                    seen[(q, cell)] = tab[p][1] + 1
            self._cells[(sampler, win)] = tab
        cell, before = tab[pair]
        return cell, before, win

    def row_plan(self, sampler: str, seed: int, qform: str) -> RowPlan:
        """The plan of a ch_failing / ch_offers row (G0 v2 S17 / S18; the idea of c2_kit.choiceplan), fixed by the seed's
        place in its sampler's stream before any structure is realised:
          ch_failing  k = the dimension labels + the always shown "None"; gold_abstain: the gold IS "None" (exactly 1/k
                      in every block of k rows of that k); abstain_slot: where "None" is displayed (exactly uniform per
                      k). The dimension labels fill the other slots in a key-hash order, so a twin (same key, other gold)
                      prints the same option list (G-TW compares closed sets in order).
          ch_offers   outcome: 0 both, 1 neither, 2 only the longer "Only <benefit>" option, 3 only the other; each value
                      once in every block of 4 rows of the stream.
        The design then realises the plan label-first; solver A's gold always agrees (checked in sample()); nothing is
        ever relabelled. Label-blind: the seed's place and k only."""
        pair, side = divmod(seed, 2)
        cell, before, win = self.choice_cell(sampler, pair)
        j = 2 * before + side
        if qform == "ch_failing":
            k = cell + 1
            return RowPlan(k, strat(sampler, f"cf_ab{k}w{win}", j, k) == 0, strat(sampler, f"cf_slot{k}w{win}", j, k), -1)
        if qform == "ch_offers":
            return RowPlan(4, False, -1, strat(sampler, f"co_outw{win}", j, 4))
        raise ContractError(f"{qform} is not a choice form with a plan")

    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        pair, side = divmod(seed, 2)
        srng = random.Random(f"{FAMILY}|{sampler}|seed|{seed}")
        qform, c0, pack, stc, clauses, keys = self._pair_draw(sampler, pair)
        n = N_CARDS[sampler]
        card = c0 if side == 0 else n - 1 - c0
        v = uhash(FAMILY, "v", sampler, pair)
        r = card_rate(c0, n)
        positive = (v < r) if side == 0 else not (v < r)  # complementary thresholds: exactly one is positive (S24)
        plan = self.row_plan(sampler, seed, qform) if qform in ("ch_failing", "ch_offers") else None
        out = self._design(srng, sampler, qform, stc, positive, plan, keys)
        vals = self._assign(srng, sampler, stc, clauses, out, pack["ladder"])
        held = sampler in self.HELD_OUT_SAMPLERS
        slots = {"STORE": S.name_slot(pack["store"]),
                 "CUSTOMER": S.name_slot(srng.choice(CUSTOMERS_HELD if held else CUSTOMERS)),
                 "ORDER_ID": S.id_slot(f"ORD-{srng.randrange(100000, 999999)}"),
                 "ITEM": S.id_slot(f"SKU-{srng.randrange(10000, 99999)}"),
                 "REGION": _cat(vals["REGION"], REGIONS), "CATEGORY": _cat(vals["CATEGORY"], CATEGORIES),
                 "STATUS": _cat(vals["STATUS"], STATUSES), "ORDER_DATE": S.date_slot(vals["ORDER_DATE"]),
                 "TIER": _cat(vals["TIER"], TIERS), "SUBTOTAL": S.cents_slot(vals["SUBTOTAL"])}
        for i, t in enumerate(pack["ladder"]):
            slots[f"TL{i}"] = _cat(t, TIERS)
        for p, prom in enumerate(stc["promises"]):
            slots[prom["slot"]] = _cat(keys[p], HEADLINES)
            for dim, bslot, cslot in prom["conds"]:
                slots[bslot] = self._bound_slot(dim, vals[bslot])
                slots[cslot] = self.lexicon.clause(clauses[cslot], bind={"X": bslot})
        if stc["asked"] is not None:
            slots["ASKED"] = _cat(keys[stc["asked"]], BENEFITS)
        depth = (sum(len(p["conds"]) for p in stc["promises"]) if qform == "ch_offers"
                 else len(stc["promises"][stc["asked"]]["conds"]))
        spec = Spec(FAMILY, sampler, seed, f"{FAMILY}:{sampler}:c{card:02d}", qform, slots, structure=stc,
                    depth=depth, deep=depth >= 3, pack=pack["pack"])
        spec = self.derive(spec)
        if plan is not None:                                  # label-first: the construction reached its plan
            ok = {(c[0], c[1]): self.cond_pass(spec, c) for c in self._conds(spec)}
            gold = self.answer_from(spec, ok)                 # the construction's gold (G2 compares both solvers to it)
            want = ((gold == NONE_KEY) == plan.gold_abstain if qform == "ch_failing"
                    else gold == offer_key(offers_holds(plan.outcome, keys), tuple(keys)))
            if not want:
                raise ContractError(f"{qform} seed {seed}: solver A gold {gold!r} disagrees with its plan (generator bug)")
        return spec

    def derive(self, spec: Spec) -> Spec:
        """No printed intermediates (every compared value is printed as is); recompute the trap tags."""
        return spec.replace(tags=self._tags(spec))

    def _conds(self, spec: Spec) -> list:
        """[(promise index, position, dim, bound slot, clause slot, sem id)] in printed order per footnote."""
        out = []
        for p, prom in enumerate(spec.structure["promises"]):
            for i, (dim, bslot, cslot) in enumerate(prom["conds"]):
                out.append((p, i, dim, bslot, cslot, spec.slots[cslot].value[0]))
        return out

    def _tags(self, spec: Spec) -> tuple:
        stc, v = spec.structure, spec.env()
        tags = set()
        if len(stc["promises"]) == 2:
            tags.add("two_headlines")
            d0 = {c[0] for c in stc["promises"][0]["conds"]}
            if d0 & {c[0] for c in stc["promises"][1]["conds"]}:
                tags.add("shared_dim")
        if stc["layout"] != "near":
            tags.add("fine_print_later")
        for _p, _i, dim, bslot, _c, sem in self._conds(spec):
            if bslot not in v:
                continue
            a, b = v[ATTR[dim]], v[bslot]
            if SEMS[sem][1] == "out":
                tags.add("exclusion")
            if dim == "date":
                if a == b:
                    tags.add("date_edge")
                    if SEMS[sem][1] in ("le", "lt"):
                        tags.add("time_bound_ends_on_order_date")
                elif abs((a - b).days) == 1:
                    tags.add("date_near")
            elif dim == "spend":
                if abs(a - b) <= 1:
                    tags.add("spend_edge" if a == b else "spend_near")
            elif dim == "tier" and a == b:
                tags.add("tier_edge")
        if spec.deep:
            tags.add("deep")
        return tuple(sorted(tags))

    # ------------------------------------------------------------------------------------------- solver A
    def _cond_node(self, spec: Spec, cond: tuple):
        _p, _i, dim, bslot, _cslot, sem = cond
        op = SEMS[sem][1]
        attr, bound = RL.Ref(ATTR[dim]), RL.Ref(bslot)
        if op in ("min", "max"):
            ladder = tuple(RL.Ref(t) for t in spec.structure["ladder"])
            return RL.Cmp(A_OP[op], RL.Fn("t07_rank", (attr,) + ladder), RL.Fn("t07_rank", (bound,) + ladder))
        return RL.Cmp(A_OP[op], attr, bound)

    def footnote_ast(self, spec: Spec, p: int):
        return RL.And(tuple(self._cond_node(spec, c) for c in self._conds(spec) if c[0] == p))

    def solve_a(self, spec: Spec):
        env = spec.env()
        stc = spec.structure
        if spec.qform == "ch_offers":
            holds = tuple(RL.evaluate(self.footnote_ast(spec, p), env) for p in range(len(stc["promises"])))
            return offer_key(holds, tuple(env[pr["slot"]] for pr in stc["promises"]))
        a = stc["asked"]
        if spec.qform == "ch_failing":
            fails = [c[2] for c in self._conds(spec) if c[0] == a and not RL.evaluate(self._cond_node(spec, c), env)]
            if len(fails) > 1:
                raise ContractError("ch_failing spec with more than one failing condition (generator bug)")
            return fails[0] if fails else NONE_KEY
        gets = RL.evaluate(self.footnote_ast(spec, a), env)
        return int(gets == YES_MEANS_GETS[spec.qform])

    # ------------------------------------------------------------------------------------------- facts
    def canonical(self, spec: Spec) -> dict:
        v, stc = spec.env(), spec.structure
        proms = stc["promises"]
        return {"qform": spec.qform, "store": v["STORE"], "customer": v["CUSTOMER"], "order_id": v["ORDER_ID"],
                "item": v["ITEM"],
                "record": {"region": v["REGION"], "category": v["CATEGORY"], "status": v["STATUS"],
                           "order_date": v["ORDER_DATE"].isoformat(), "tier": v["TIER"], "subtotal": v["SUBTOTAL"]},
                "ladder": [v[t] for t in stc["ladder"]],
                "headlines": [[pr["mark"], v[pr["slot"]]] for pr in proms],
                "footnotes": [[proms[i]["mark"], [[spec.slots[c[2]].value[0], S.canonical(spec.slots[c[1]])]
                                                  for c in proms[i]["conds"]]] for i in stc["foot_order"]],
                "asked": v.get("ASKED")}

    def extract_view(self, spec: Spec) -> dict:
        """G3-H on a Mode F text: the (rule, bound) of each dimension of the (only) footnote, and the store."""
        view = {"store": spec.env()["STORE"]}
        conds = {c[0]: c for c in spec.structure["promises"][0]["conds"]}
        for d in DIMS:
            c = conds.get(d)
            view[f"{d}_rule"] = SEMS[spec.slots[c[2]].value[0]][1] if c else "absent"
            view[f"{d}_bound"] = S.canonical(spec.slots[c[1]]) if c else None
        return view

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        rules = {"region": ("in", "out", "absent"), "category": ("in", "out", "absent"), "status": ("out", "absent"),
                 "date": ("le", "lt", "ge", "absent"), "tier": ("min", "max", "absent"),
                 "spend": ("ge", "gt", "absent")}
        says = {"region": "the delivery-region rule of the fine print: in = only that region, out = that region "
                          "excluded, absent = no region rule",
                "category": "the product-category rule: in = only that category, out = that category excluded, "
                            "absent = none",
                "status": "the price-status rule: out = items with that status excluded, absent = none",
                "date": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, "
                        "absent = none",
                "tier": "the membership rule: min = that level and above, max = that level and below, absent = none",
                "spend": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none"}
        out = [Field("store", "name", "the store that runs the advertisement")]
        for d in DIMS:
            out.append(Field(f"{d}_rule", "enum", says[d], choices=rules[d]))
            out.append(Field(f"{d}_bound", BOUND_KIND[d], f"the value the {d} rule names, as written (null if "
                             "absent)", bound_params(d)))
        return out

    # ------------------------------------------------------------------------------------------- render
    def _bound_schema(self, decl: dict) -> dict:
        out = {}
        for name, kind in decl.items():
            dim = name.split("_", 1)[1].lower() if name.startswith("P") and "_" in name else None
            out[name] = (kind, bound_params(dim) if dim in BOUND_KIND else ())
        return out

    def _freeform_signature(self, skin) -> tuple:
        """The condition sems a Mode F text embeds, in text order (admitted lexicon forms only). G0 S14 (H21, H26):
        the text holds exactly one `*`, directly followed by its condition sentences (whitespace between them only);
        a text that breaks this fits no spec (empty signature)."""
        key = (skin.skin_id, skin.text)
        if key not in self._sig_cache:
            sig = ()
            try:
                ms = self.lexicon.scan(skin.text, self._bound_schema(skin.decl), kinds=CLAUSE_KINDS,
                                       admitted_only=True)
                star = skin.text.find("*")
                gaps = [skin.text[star + 1:ms[0].start]] + [skin.text[x.end:y.start] for x, y in zip(ms, ms[1:])] \
                    if ms else []
                if ms and skin.text.count("*") == 1 and star < ms[0].start and not "".join(gaps).strip():
                    sig = tuple(m.sem_id for m in ms)
            except LexiconError:
                pass
            self._sig_cache[key] = sig
        return self._sig_cache[key]

    def compatible(self, skin, spec: Spec) -> bool:
        """A Mode T skin declares only the store; a Mode F skin carries exactly the conditions of a one-headline
        spec, in printed order (G0 S14)."""
        slots = spec.all_slots()
        if any(name not in slots or slots[name].kind != kind for name, kind in skin.decl.items()):
            return False
        if skin.author_mode == "T":
            return set(skin.decl) <= MODE_T_SLOTS
        proms = spec.structure["promises"]
        if len(proms) != 1:
            return False
        conds = proms[0]["conds"]
        if set(skin.decl) - MODE_T_SLOTS != {c[1] for c in conds}:
            return False
        return self._freeform_signature(skin) == tuple(slots[c[2]].value[0] for c in conds)

    def _pick_skin(self, ctx, spec: Spec, pkey: str, held: bool):
        cands = [s for s in ctx.skins.values() if s.family == FAMILY and s.kind == "skin" and s.held_out == held
                 and self.compatible(s, spec)]
        free = [s for s in cands if s.author_mode == "F"]
        pool = free if (free and uhash(pkey, "mode") < P_FREEFORM) else [s for s in cands if s.author_mode == "T"]
        if not pool:
            raise LookupError(f"no compatible T07 skin (held_out={held})")
        return min(pool, key=lambda s: uhash(pkey, "skin", s.skin_id))

    def _pick_wording(self, ctx, pkey: str, qform: str, held: bool):
        if held:
            try:
                return ctx.pick(FAMILY, "wording", pkey, qform=qform, held_out=True)
            except LookupError:
                pass
        return ctx.pick(FAMILY, "wording", pkey, qform=qform)

    @staticmethod
    def _banner_tpl(stc: dict) -> str:
        return BANNER_HEAD + "".join(f"\n{{{p['slot']}}}{p['mark']}" for p in stc["promises"])

    @staticmethod
    def _terms_tpl(stc: dict) -> str:
        lines = [TERMS_HEAD[stc["layout"]]]
        for i in stc["foot_order"]:
            p = stc["promises"][i]
            lines.append(p["mark"] + " " + " ".join("{" + c[2] + "}" for c in p["conds"]))
        return "\n".join(lines)

    @staticmethod
    def _card_tpl(stc: dict) -> str:
        names = [f"{{{t}}}" for t in stc["ladder"]]
        tpl = CARD_SHORT_TPL if stc.get("card") == "short" else CARD_TPL
        return tpl.replace("{LADDER}", ", ".join(names[:-1]) + " and " + names[-1])

    @staticmethod
    def _blocks(stc: dict, freeform: bool) -> list:
        lay = stc["layout"]
        ad = ["banner", "terms", "skin"] if lay == "near" else ["banner", "skin", "terms"]
        if stc["record_first"]:
            out = ["record"] + ad
        elif lay == "after_record":
            out = ["banner", "skin", "record", "terms"]
        else:
            out = ad + ["record"]
        return [b for b in out if not (freeform and b == "terms")]

    def _offer_text(self, spec: Spec, forms: dict):
        slots = spec.all_slots()
        names = {}
        for pr in spec.structure["promises"]:
            k = slots[pr["slot"]].value
            names[k] = S.render(_cat(k, BENEFITS), forms.get("ASKED"))

        def text(key):
            if key == "both":
                return OFFER_BOTH
            if key == "neither":
                return OFFER_NEITHER
            return "Only " + names[key.split(":", 1)[1]]
        return text

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        key = f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"
        pkey = f"{spec.family}|pair{spec.seed // 2}|{spec.sampler}|{spec.qform}"   # pairs share skin and wording
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        ctx = self.ctx_for(spec, ctx)                  # never pick a wording that breaks the polarity rule
        skin = skin or self._pick_skin(ctx, spec, pkey, held)
        if not self.compatible(skin, spec):
            raise ContractError(f"skin {skin.skin_id} does not fit this spec (G0 S14)")
        wording = wording or self._pick_wording(ctx, pkey, spec.qform, held)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = forms or choose_forms(spec, key)
        slots, stc = spec.all_slots(), spec.structure
        freeform = skin.author_mode == "F"
        tb = TextBuilder()
        for j, block in enumerate(self._blocks(stc, freeform)):
            if j:
                tb.add("state", "\n\n")
            if block == "banner":
                tb.add("state", K.fill(self._banner_tpl(stc), slots, forms))
            elif block == "terms":
                tb.add("state", K.fill(self._terms_tpl(stc), slots, forms))
            elif block == "skin":
                tb.add("state", skin.fill(slots, forms), skin_id=skin.skin_id)
            elif stc["container"] == "json":
                tb.add("state", K.fill(RECORD_JSON_HEAD, slots, forms))
                tb.add("state", K.fill(RECORD_JSON_BODY, slots, forms, escape="json"))
            else:
                tb.add("state", K.fill(RECORD_TPL[stc["container"]], slots, forms))
        if attack is not None:
            tb.add("state", "\n\n" + ATTACK_PREFIX).add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        tb.add("instructions", K.fill(self._card_tpl(stc), slots, forms)).add("instructions", "\n\n")
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_, models = None, self.error_models()
        if spec.qform == "ch_failing":
            os_ = self._failing_options(spec, ans, key, models)
        elif spec.qform == "ch_offers":
            ks = [slots[pr["slot"]].value for pr in stc["promises"]]
            os_ = build_closed(spec, ans, ["both", "only:" + ks[0], "only:" + ks[1], "neither"], models,
                               row_key=key, render_key=self._offer_text(spec, forms))
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, defs_style=f"card_{stc.get('card', 'full')}",
                            format_style=f"{stc['container']}/{stc['layout']}/{skin.register}/{skin.escape}")

    def _failing_options(self, spec: Spec, ans, key: str, models: dict):
        """The ch_failing option list: one label per dimension in a key-hash order, "None" displayed at the plan's
        abstain slot (exactly uniform per k). The list depends on the row key and the structure only, never on the gold,
        so a twin or an equiv / inv partner of the row prints the very same list (G-TW). plan_report reads the planned
        abstain share from meta["plan"] (1/k)."""
        dims = failing_dims(spec.structure)
        os_ = build_closed(spec, ans, dims, models, row_key=key, render_key=DIM_TEXT.__getitem__,
                           abstain=(NONE_KEY, NONE_TEXT), show_abstain=True, order="fixed")
        none = next(o for o in os_.options if o.key == NONE_KEY)
        rest = sorted((o for o in os_.options if o.key != NONE_KEY), key=lambda o: uhash(key, "closed", repr(o.key)))
        slot = self.row_plan(spec.sampler, spec.seed, "ch_failing").abstain_slot
        opts = rest[:slot] + [none] + rest[slot:]
        gi = next(i for i, o in enumerate(opts) if o.role == "gold")
        k = len(opts)
        plan = ChoicePlan(key, k, True, ans == NONE_KEY, gi, None, 1.0 / k, "shuffle", k - 1)
        out = OptionSet(opts, gi, {**os_.meta, "plan": plan.to_json(), "abstain_slot": "shuffle"})
        self._name_abstain(out, spec, models)                       # a wrong "None" is named (G0 S23)
        return out

    @staticmethod
    def _name_abstain(os_, spec: Spec, models: dict) -> None:
        """build_closed leaves the abstain option unnamed; record the error models that produce "none"."""
        for j, o in enumerate(os_.options):
            if o.role == "abstain":
                err = tuple(n for n in sorted(models) if models[n].fn(spec) == NONE_KEY)
                os_.options[j] = Option(o.key, o.text, "abstain", err)

    # ------------------------------------------------------------------------------------------- construction view
    def cond_pass(self, spec: Spec, cond: tuple, variant=frozenset()) -> bool:
        """The construction's reading of one condition (direct comparisons; not the AST). `variant` swaps one rule
        for an error model."""
        if "ignore" in variant:
            return True
        v = spec.env()
        _p, _i, dim, bslot, _c, sem = cond
        a, b, op = v[ATTR[dim]], v[bslot], SEMS[sem][1]
        if dim in ("region", "category", "status"):
            if op == "out" and "excl_as_in" in variant:
                op = "in"
            elif op == "in" and "in_as_excl" in variant:
                op = "out"
            return (a == b) if op == "in" else (a != b)
        if dim == "tier":
            ladder = [v[t] for t in spec.structure["ladder"]]
            ra, rb = ladder.index(a), ladder.index(b)
            if "tier_exact" in variant:
                return ra == rb
            up = (op == "min") != ("reverse" in variant)            # "and above" (or "and below" read reversed)
            if "drop_incl" in variant:
                return ra > rb if up else ra < rb
            return ra >= rb if up else ra <= rb
        if "reverse" in variant:
            op = {"le": "ge", "lt": "gt", "ge": "le", "gt": "lt"}[op]
        if "drop_incl" in variant:
            op = {"le": "lt", "ge": "gt"}.get(op, op)
        if "add_excl" in variant:
            op = {"lt": "le", "gt": "ge"}.get(op, op)
        return {"le": a <= b, "lt": a < b, "ge": a >= b, "gt": a > b}[op]

    def answer_from(self, spec: Spec, ok: dict):
        """The answer when condition (promise, position) passes iff ok[(p, i)] (twin predictions)."""
        stc = spec.structure
        conds = self._conds(spec)
        if spec.qform == "ch_offers":
            holds = tuple(all(ok[(c[0], c[1])] for c in conds if c[0] == p) for p in range(len(stc["promises"])))
            return offer_key(holds, tuple(spec.env()[pr["slot"]] for pr in stc["promises"]))
        a = stc["asked"]
        fails = [c[2] for c in conds if c[0] == a and not ok[(c[0], c[1])]]
        if spec.qform == "ch_failing":
            return None if len(fails) > 1 else (fails[0] if fails else NONE_KEY)
        return int((not fails) == YES_MEANS_GETS[spec.qform])

    # ------------------------------------------------------------------------------------------- relations
    def relations(self, spec: Spec) -> list:
        out = []
        smp, seed, q = spec.sampler, spec.seed, spec.qform
        if q in COMPLEMENT_OF and uhash(FAMILY, "comp", smp, seed) < P_COMPLEMENT:
            u, acc, q2 = uhash(FAMILY, "ckind", smp, seed), 0.0, COMPLEMENT_OF[q][-1][0]
            for cand, w in COMPLEMENT_OF[q]:
                acc += w
                if u < acc:
                    q2 = cand
                    break
            out.append(RelationProposal("complement", qform=q2))
        u = uhash(FAMILY, "extra", smp, seed)
        if u < P_EQUIV:
            out.append(self._equiv(spec))
        elif u < P_EQUIV + P_INV:
            out.append(RelationProposal("inv"))
        if uhash(FAMILY, "twin", smp, seed) < (P_TWIN if self.QFORMS[q].qtype == "noul" else P_TWIN_CHOICE):
            t = self._twin(spec)
            if t is not None:
                out.append(t)
        return out + self._metamorphic(spec)

    def _equiv(self, spec: Spec) -> RelationProposal:
        regs = EQUIV_REGISTERS_HELD if spec.sampler in self.HELD_OUT_SAMPLERS else EQUIV_REGISTERS
        reg = min(regs, key=lambda r: uhash(FAMILY, "equiv_reg", spec.sampler, spec.seed, r))
        other = {"lines": "table", "table": "lines", "transcript": "table", "json": "table"}
        s2 = spec.replace(structure={**spec.structure, "container": other[spec.structure["container"]]})
        return RelationProposal("equiv", spec=s2, register=reg, note="another register and record container")

    def _shared(self, spec: Spec, dim: str) -> bool:
        return sum(1 for c in self._conds(spec) if c[2] == dim) > 1

    def _flip_edit(self, spec: Spec, cond: tuple, to_pass: bool, use_attr: bool):
        """(slot, new Slot) that moves exactly `cond` to the other side (None when one slot cannot)."""
        v = spec.env()
        _p, _i, dim, bslot, _c, sem = cond
        op = SEMS[sem][1]
        a, b = v[ATTR[dim]], v[bslot]
        aslot = ATTR[dim]
        rng = random.Random(f"{FAMILY}|twin|{spec.sampler}|{spec.seed}")
        if dim in ("region", "category"):
            universe = sorted(CAT_SET[dim])
            same = (op == "in") == to_pass
            if use_attr:
                return aslot, _cat(b if same else rng.choice([x for x in universe if x != b]), CAT_SET[dim])
            return bslot, _cat(a if same else rng.choice([x for x in universe if x != a]), CAT_SET[dim])
        if dim == "status":
            marked = [k for k in sorted(STATUSES) if k != "regular_price"]
            if use_attr:
                return aslot, _cat(rng.choice([x for x in sorted(STATUSES) if x != b]) if to_pass else b, STATUSES)
            if to_pass:
                return bslot, _cat(rng.choice([x for x in marked if x != a]), STATUSES)
            return (bslot, _cat(a, STATUSES)) if a in marked else None
        if dim == "date":
            one = TD(days=1)
            new_a = {("le", True): b, ("le", False): b + one, ("lt", True): b - one, ("lt", False): b,
                     ("ge", True): b, ("ge", False): b - one}[(op, to_pass)]
            new_b = {("le", True): a, ("le", False): a - one, ("lt", True): a + one, ("lt", False): a,
                     ("ge", True): a, ("ge", False): a + one}[(op, to_pass)]
            return (aslot, S.date_slot(new_a)) if use_attr else (bslot, S.date_slot(new_b))
        if dim == "spend":
            if use_attr:
                return aslot, S.cents_slot({("ge", True): b, ("ge", False): b - 1, ("gt", True): b + 1,
                                            ("gt", False): b}[(op, to_pass)])
            if to_pass:
                cand = [g for g in SPEND_GRID if (g <= a if op == "ge" else g < a)]
                return (bslot, S.cents_slot(cand[-1])) if cand else None
            cand = [g for g in SPEND_GRID if (g > a if op == "ge" else g >= a)]
            return (bslot, S.cents_slot(cand[0])) if cand else None
        ladder = [v[t] for t in spec.structure["ladder"]]
        ra, rb, m = ladder.index(a), ladder.index(b), len(ladder)
        step = -1 if op == "min" else 1                          # one level across the line, away from passing
        if use_attr:
            r = rb if to_pass else rb + step
            return (aslot, _cat(ladder[r], TIERS)) if 0 <= r < m else None
        r = ra if to_pass else ra - step
        ok_bound = 1 <= r <= m - 1 if op == "min" else 0 <= r <= m - 2
        return (bslot, _cat(ladder[r], TIERS)) if ok_bound else None

    def _twin(self, spec: Spec):
        """Exactly one input slot moves exactly one condition across its line; the prediction is the construction's
        outcome table with that one condition flipped (never solve_a)."""
        conds = self._conds(spec)
        ok = {(c[0], c[1]): self.cond_pass(spec, c) for c in conds}
        stc, q = spec.structure, spec.qform
        cands = []
        groups = range(len(stc["promises"])) if q == "ch_offers" else [stc["asked"]]
        for p in groups:
            mine = [c for c in conds if c[0] == p]
            fails = [c for c in mine if not ok[(c[0], c[1])]]
            if not fails:
                cands += mine
            elif len(fails) == 1:
                cands += fails
        if not cands:
            return None
        cond = min(cands, key=lambda c: uhash(FAMILY, "twin_cond", spec.sampler, spec.seed, c[3]))
        to_pass = not ok[(cond[0], cond[1])]
        use_attr = (not self._shared(spec, cond[2])) and uhash(FAMILY, "twin_attr", spec.sampler, spec.seed) < .6
        edit = self._flip_edit(spec, cond, to_pass, use_attr) or (
            self._flip_edit(spec, cond, to_pass, False) if use_attr else None)
        if edit is None:
            return None
        ok2 = dict(ok)
        ok2[(cond[0], cond[1])] = to_pass
        pred, base = self.answer_from(spec, ok2), self.answer_from(spec, ok)
        if pred is None or pred == base:
            return None
        if q == "ch_failing" and not abstain_twin_kept(f"{FAMILY}|{spec.sampler}|{spec.seed}", base, pred, NONE_KEY,
                                                       twin_none_keep(len(failing_dims(stc)))):
            return None
        return RelationProposal("twin", spec=spec.with_slot(*edit), changed_slot=edit[0], expect=pred,
                                note=f"{cond[2]}:{'attr' if edit[0] == ATTR[cond[2]] else 'bound'}")

    def _metamorphic(self, spec: Spec) -> list:
        v, stc, seed = spec.env(), spec.structure, spec.seed
        out = []
        pool = CUSTOMERS_HELD if spec.sampler in self.HELD_OUT_SAMPLERS else CUSTOMERS
        name = min((n for n in pool if n != v["CUSTOMER"]), key=lambda n: uhash(FAMILY, "mm_name", seed, n))
        out.append(RelationProposal("metamorphic", spec=spec.with_slot("CUSTOMER", S.name_slot(name)), expect="same",
                                    note="rename the customer"))
        stores = STORES_HELD if spec.sampler in self.HELD_OUT_SAMPLERS else STORES
        store = min((n for n in stores if n != v["STORE"]), key=lambda n: uhash(FAMILY, "mm_store", seed, n))
        out.append(RelationProposal("metamorphic", spec=spec.with_slot("STORE", S.name_slot(store)), expect="same",
                                    note="rename the store"))
        wk = TD(days=7)
        dates = {k: S.date_slot(x + wk) for k, x in v.items() if k in spec.slots and spec.slots[k].kind == "date"}
        out.append(RelationProposal("metamorphic", spec=spec.replace(slots={**spec.slots, **dates}), expect="same",
                                    note="shift every date by 7 days"))
        for _p, _i, _dim, bslot, cslot, sem in self._conds(spec):
            alts = [f for f in self._form_ids(sem, spec.sampler) if f != spec.slots[cslot].value[1]]
            if alts:
                fid = min(alts, key=lambda f: uhash(FAMILY, "mm_para", seed, f))
                out.append(RelationProposal("metamorphic", spec=spec.with_slot(
                    cslot, self.lexicon.clause(fid, bind={"X": bslot})), expect="same",
                    note="another admitted paraphrase of a condition"))
                break
        if len(stc["foot_order"]) == 2:
            out.append(RelationProposal("metamorphic", spec=spec.replace(
                structure={**stc, "foot_order": stc["foot_order"][::-1]}), expect="same",
                note="reverse the fine-print order"))
        return out

    # ------------------------------------------------------------------------------------------- error models
    def _model_answer(self, spec: Spec, variant: frozenset):
        q = spec.qform
        if q not in ("ch_failing", "ch_offers"):
            return None
        conds = self._conds(spec)
        n_prom = len(spec.structure["promises"])

        def conds_for(p):
            if "wrong_foot" in variant:
                return [c for c in conds if c[0] == 1 - p] if n_prom == 2 else None
            if "all_foot" in variant:
                return conds if n_prom == 2 else None
            mine = [c for c in conds if c[0] == p]
            return mine[:1] if "first_only" in variant else mine

        if q == "ch_failing":
            cs = conds_for(spec.structure["asked"])
            if cs is None:
                return None
            fails = sorted({c[2] for c in cs if not self.cond_pass(spec, c, variant)})
            return NONE_KEY if not fails else (fails[0] if len(fails) == 1 else None)
        holds = []
        for p in range(n_prom):
            cs = conds_for(p)
            if cs is None:
                return None
            holds.append(all(self.cond_pass(spec, c, variant) for c in cs))
        return offer_key(tuple(holds), tuple(spec.env()[pr["slot"]] for pr in spec.structure["promises"]))

    def error_models(self) -> dict:
        return {name: error_model(name, functools.partial(self._model_answer, variant=var))
                for name, var in EM_VARIANTS.items()}
