"""families/T06/plugin.py: T06 "consumer return rights: non-waivable floor vs posted policy" (C2_DATA_SPEC 2.1, 3.13;
PREREG_FINAL A37).

A customer asks to return goods bought online. The row shows the customer's message (a Haiku skin), the order record
(item, type of goods, seal state for hygiene goods, handover, order / delivery / possession / request dates, the
reason, and the printed day counts) and the store's posted notice; the card is an excerpt of an invented consumer
statute in one of four styles. The statute grants two non-waivable rights: rejecting FAULTY goods within N_REJ days of
DELIVERY, and withdrawing for any reason within N_WD days of the day the buyer took POSSESSION, the second with three
exclusions (goods made to the buyer's specification; perishable goods; sealed hygiene goods whose seal was broken after
delivery) that never limit the first. A store notice cannot remove or shorten either right, and a full refund the
notice itself promises is owed as well. Every period counts the event's day as day zero and includes its last day.
Semantics: G0_SPEC_v4.md (frozen sha below; v2 = G0_SPEC.md authored the pools).

  solver A   decision tables on day ordinals: exclusion table, rejection table, withdrawal table, notice table keyed by
             (notice meaning, reason), outcome table over the three grant bits, question table   paradigm decision_table
  solver B   solver_b.py: its own parser of the RENDERED row (card templates per statute style, three record
             containers, the notice through the lexicon, the skin template); each period becomes the list of its
             calendar days walked one by one (brute.window_days) and the request date is looked up in it; a separate
             exclusion evaluator; its own notice-meaning and question tables                    paradigm day_bitmap
  samplers   S1 forward; S2 label-first near misses (boundary days and anchor traps boosted); S3 record-table-first;
             S4 notice-first chat thread; S5 held out (Regulations style, held-out jurisdictions and periods, JSON
             record, held-out skins and wordings)
  questions  yes/no on predicate "refund": yn_refund, yn_owed, yn_double (double negation, positive); complements
             yn_not_refund and yn_no_right (syntactic), yn_may_refuse (antonym); ch_rule "which rule gives the full
             refund" (closed set: rejection right / withdrawal right / the store's notice / none); ch_end_reject and
             ch_end_withdraw "on which date does the period end" (open sets of dates from error models)
  relations  complement; minimal-edit twin (one slot: request, delivery or possession date, reason, seal, a period
             length, the notice's days or the notice's meaning); equiv (another skin, register and record container);
             inv (an inert message line); G4 metamorphic (rename customer, item, store or jurisdiction; shift every
             date by seven days; swap one no-promise notice for another)
Code only: nothing here writes a file (A37 f).
"""
from __future__ import annotations

import datetime as dt
import random
from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path

from c2_kit import cards as CD
from c2_kit import polarity as POL
from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.choiceplan import ChoicePlan, plan_choice
from c2_kit.distractors import build_closed, build_options, error_model, register_name, uhash
from c2_kit.plugin import C2Plugin, ContractError, KitCtx, QuestionForm, RelationProposal, Spec, choose_forms
from c2_kit.relations import abstain_twin_kept
from c2_kit.rows import TextBuilder, assemble_row

HERE = Path(__file__).resolve().parent
FAMILY = "T06"
DAYS = ("day", "days")
TD = dt.timedelta

# ------------------------------------------------------------------------------------------------ closed pools
# Program-side seed pools (G0_SPEC.md section 3). After A38 they are expanded from Haiku packs by program.
JURIS = ("Valdoria", "Norvane", "Corvania", "Lunmark", "Tirasso", "Quillon", "Brevania", "Eskaria", "Sundrel",
         "Ostmere")
JURIS_HELD = ("Pellara", "Vessany")
STORES = ("Brightwell Home", "Kestrel Outfitters", "Fernway Market", "Lumenor Electronics", "Cedarline Living",
          "Bluecrest Sports", "Copperleaf Kitchen", "Northvale Audio", "Orchard Lane Florists", "Pebblestone Beauty",
          "Harborlight Goods", "Tidewell Supply")
CUSTOMERS = ("Dana Okafor", "Lena Whitcombe", "Ravi Anand", "Mira Castell", "Tomas Ferreira", "Aiko Brandt",
             "Jonah Pryce", "Selin Yilmaz", "Priya Raman", "Hugo Lindqvist", "Nadia Haddad", "Owen Mensah")
ITEMS = {
    "standard": ("desk lamp", "rain jacket", "bluetooth speaker", "coffee grinder", "pair of hiking boots",
                 "wall clock", "backpack", "table fan", "kettle", "yoga mat", "board game", "phone case"),
    "custom": ("engraved watch", "monogrammed towel set", "pair of made-to-measure curtains",
               "pair of custom-fit insoles", "name-printed mug", "engraved cutting board", "custom portrait canvas",
               "tailored blazer"),
    "perishable": ("fresh flower bouquet", "box of pastries", "cheese hamper", "fresh fruit box", "meal kit",
                   "birthday cake"),
    "hygiene": ("wireless earbud set", "electric toothbrush", "lipstick set", "face serum", "razor cartridge pack",
                "swimsuit", "hair clipper"),
}
GOODS_SET = {"standard": ["standard goods"], "custom": ["made to the buyer's specification"],
             "perishable": ["perishable goods"], "hygiene": ["sealed hygiene goods"]}
SEAL_SET = {"intact": ["intact"], "opened": ["broken after delivery"]}
REASON_SET = {"faulty": ["faulty"], "mind": ["change of mind"]}
HANDOVER_SET = {"direct": ["handed to the buyer at delivery"],      # G0 H11: delivery = the day the goods reach
                "locker": ["delivered to a parcel locker and collected by the buyer later"],   # the buyer, a locker
                "neighbour": ["delivered to a neighbour and collected by the buyer later"]}    # or a neighbour

# ------------------------------------------------------------------------------------------------ card (statute)
TRAIN_STYLES = ("act", "code", "charter")
HELD_STYLE = "regulation"
CLOSED_WORLD = ("The rules, the posted notice and the order record are complete; no other fact or message changes "
                "the case.")
# One item per line of a statute card: (full, compact, short). Item 0 is the head line, the same in every variant.
# The full text is the frozen G0 v2 card (G0 section 2, unchanged); compact and short (G0 v3) keep every rule: the same
# slots, numbers, operator words and negation count per item (c2_kit.cards.variant_problems, checked by the tests), and
# only drop filler ("from the delivery date" -> "of delivery", "the next day is day one", "from a purchase", "of the
# goods"). The held-out style (regulation, S5) has a full card only.
_H = lambda s: (s, s, s)  # noqa: E731
CARD_ITEMS = {
    "act": (
        _H("Consumer Sales Act of {JURIS} (excerpt)"),
        ("Section I (counting days). A right is used on the day the buyer asks for it. A period in this Act or in a "
         "store notice runs in calendar days from an event: the event's day is day zero, the next day is day one, and "
         "the period includes its last day.",
         "Section I (counting days). A right is used on the day the buyer asks for it. Periods in this Act or in a "
         "store notice run in calendar days from an event: the event's day is day zero, and the last day counts.",
         "Section I. A right is used on the day the buyer asks for it. Periods in this Act or in a store notice are "
         "calendar days from an event: the event's day is day zero, the last day counts."),
        ("Section II (faulty goods). A buyer may reject faulty goods and get a full refund within {N_REJ} from the "
         "delivery date.",
         "Section II (faulty goods). A buyer may reject faulty goods and get a full refund within {N_REJ} of "
         "delivery.",
         "Section II. A buyer may reject faulty goods for a full refund within {N_REJ} of delivery."),
        ("Section III (withdrawal). A buyer may withdraw from a purchase for any reason and get a full refund within "
         "{N_WD} from the day the buyer took possession of the goods. Section III does not cover goods made to the "
         "buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these "
         "exclusions do not limit Section II.",
         "Section III (withdrawal). A buyer may withdraw for any reason and get a full refund within {N_WD} from the "
         "day the buyer took possession. Section III does not cover goods made to the buyer's specification, "
         "perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions do not "
         "limit Section II.",
         "Section III. A buyer may withdraw for any reason for a full refund within {N_WD} of taking possession. It "
         "does not cover goods made to the buyer's specification, perishable goods, or sealed hygiene goods whose "
         "seal was broken after delivery; these exclusions do not limit Section II."),
        ("Section IV (store notices). A store notice cannot remove or shorten these rights. A store may promise more, "
         "and a full refund its posted notice promises is owed.",
         "Section IV (store notices). A store notice cannot remove or shorten these rights. A store may promise more, "
         "and a full refund its posted notice promises is owed.",
         "Section IV. A store notice cannot remove or shorten these rights. A store may promise more; a full refund "
         "its posted notice promises is owed."),
    ),
    "code": (
        _H("Civil Code of {JURIS}, consumer sales, Article K (extract)"),
        ("(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts "
         "calendar days from an event: the event's day is day zero, the next day is day one, and the final day of the "
         "limit still counts.",
         "(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts "
         "calendar days from an event: the event's day is day zero, and the final day still counts.",
         "(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts "
         "calendar days from an event: the event's day is day zero, the final day still counts."),
        ("(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts {N_REJ}, counted from "
         "the date of delivery.",
         "(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts {N_REJ} from the date "
         "of delivery.",
         "(b) A buyer may reject faulty goods and be refunded in full; the right lasts {N_REJ} from delivery."),
        ("(c) A buyer may withdraw from a purchase for any reason and be refunded in full; this right lasts {N_WD}, "
         "counted from the date the buyer took possession of the goods.",
         "(c) A buyer may withdraw for any reason and be refunded in full; this right lasts {N_WD} from the date the "
         "buyer took possession.",
         "(c) A buyer may withdraw for any reason and be refunded in full; the right lasts {N_WD} from taking "
         "possession."),
        ("(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene "
         "goods whose seal was broken after delivery. Paragraph (b) has no exclusions.",) * 3,
        ("(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund "
         "its posted notice promises is owed.",
         "(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund "
         "its posted notice promises is owed.",
         "(e) A seller's notice cannot remove or shorten these rights. A seller may promise more; a full refund its "
         "posted notice promises is owed."),
    ),
    "charter": (
        _H("Buyer's Rights Charter of {JURIS} (summary every store must display)"),
        ("- Counting days: you use a right on the day you ask for it. Periods count calendar days: a period's event "
         "day is day zero, the next day is day one, and the last day of the period still counts. Store notices count "
         "days the same way.",
         "- Counting days: you use a right on the day you ask for it. Periods count calendar days: a period's event "
         "day is day zero, and the last day still counts. Store notices count days the same way.",
         "- Counting days: you use a right on the day you ask for it. Periods are calendar days: the event day is day "
         "zero, the last day still counts. Store notices count the same way."),
        ("- Faulty-goods rule: you can reject faulty goods and get a full refund within {N_REJ} from the day they "
         "were delivered.",
         "- Faulty-goods rule: you can reject faulty goods and get a full refund within {N_REJ} from the day they "
         "were delivered.",
         "- Faulty-goods rule: you can reject faulty goods for a full refund within {N_REJ} of delivery."),
        ("- Cooling-off rule: for any reason, you can withdraw from a purchase and get a full refund within {N_WD} "
         "from the day you took possession of the goods. It does not cover goods made to your specification, "
         "perishable goods, or sealed hygiene goods whose seal was broken after delivery. These exclusions never "
         "limit the faulty-goods rule.",
         "- Cooling-off rule: for any reason, you can withdraw and get a full refund within {N_WD} from the day you "
         "took possession. It does not cover goods made to your specification, perishable goods, or sealed hygiene "
         "goods whose seal was broken after delivery. These exclusions never limit the faulty-goods rule.",
         "- Cooling-off rule: for any reason, you can withdraw for a full refund within {N_WD} of taking possession. "
         "It does not cover goods made to your specification, perishable goods, or sealed hygiene goods whose seal "
         "was broken after delivery; these exclusions never limit the faulty-goods rule."),
        ("- Store notices: a store notice cannot take away or shorten these rights. A store may promise more, and a "
         "full refund its posted notice promises is owed.",
         "- Store notices: a store notice cannot take away or shorten these rights. A store may promise more, and a "
         "full refund its posted notice promises is owed.",
         "- Store notices: a store notice cannot take away or shorten these rights. A store may promise more; a full "
         "refund its posted notice promises is owed."),
    ),
    "regulation": (
        _H("Distance Sales Regulations of {JURIS}, Part R (extract)"),
        _H("Reg. A (periods). A right is exercised on the day the consumer requests it. A period counts whole "
           "calendar days from its event: the event day is day zero, the next day is day one, and the final day is "
           "included. A trader's notice counts days the same way."),
        _H("Reg. B (rejection). A consumer may reject faulty goods and is due a full refund if the rejection is made "
           "within {N_REJ} of delivery."),
        _H("Reg. C (cancellation). A consumer may cancel a purchase for any reason and is due a full refund if the "
           "cancellation is made within {N_WD} of taking possession of the goods. Reg. C does not apply to goods made "
           "to the buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after "
           "delivery. Reg. B is not limited by these exclusions."),
        _H("Reg. D (notices). A trader's notice cannot exclude or shorten these rights. A trader may promise more, "
           "and a full refund its posted notice promises is due."),
    ),
}
CARD_VARIANTS = ("full", "compact", "short")
# The statute card of a style in one variant: the lines joined by newlines (G0 v3 section 2; solver B keeps its own copy).
CARD_TEXT = {(st, v): "\n".join(it[i] for it in items)
             for st, items in CARD_ITEMS.items() for i, v in enumerate(CARD_VARIANTS)
             if st in TRAIN_STYLES or v == "full"}
STYLE_TEXT = {st: CARD_TEXT[(st, "full")] for st in CARD_ITEMS}          # the frozen G0 v2 cards (full)
CARD_SHARES = {"full": 0.25, "compact": 0.60, "short": 0.15}             # training samplers; draw_style from the row key
CARD_SHARES_HELD = {"full": 1.0}                                         # S5 (regulation): the full card only
RULE_KEYS = ("reject", "withdraw", "store", "none")
OPTION_TEXT = {
    "act": {"reject": "Section II (faulty goods)", "withdraw": "Section III (withdrawal)",
            "store": "The store's posted notice", "none": "None of them: no full refund is owed"},
    "code": {"reject": "Article K(b) (faulty goods)", "withdraw": "Article K(c) (withdrawal)",
             "store": "The seller's posted notice", "none": "None of them: no full refund is owed"},
    "charter": {"reject": "The faulty-goods rule", "withdraw": "The cooling-off rule",
                "store": "The store's posted notice", "none": "None of them: no full refund is owed"},
    "regulation": {"reject": "Reg. B (rejection)", "withdraw": "Reg. C (cancellation)",
                   "store": "The trader's posted notice", "none": "None of them: no full refund is due"},
}


# G4 rule variants (G0 v4 S22; metamorphic partners only, never an emitted row): "swap" flips the notice rule (the posted
# notice replaces the statutory rights: only a refund the notice promises is owed), "nowd" deletes the withdrawal rule
# (and its exclusions): a right the rules do not state does not exist (the closed-world sentence).
RULE_MODES = ("std", "swap", "nowd")
NOTICE_ONLY = {
    "act": "Section IV (store notices). A store notice replaces these rights: the buyer gets a full refund only if the "
           "store's posted notice promises one.",
    "code": "(e) A seller's notice replaces these rights: the buyer gets a full refund only if the seller's posted "
            "notice promises one.",
    "charter": "- Store notices: a store notice replaces these rights: you get a full refund only if the store's posted "
               "notice promises one.",
    "regulation": "Reg. D (notices). A trader's notice replaces these rights: the consumer is due a full refund only if "
                  "the trader's posted notice promises one."}
DROP_LINES = {"act": (3,), "code": (3, 4), "charter": (3,), "regulation": (3,)}      # the withdrawal rule's line(s)


@lru_cache(maxsize=None)
def card_template(style: str, variant: str = "full", rule: str = "std") -> str:
    """The card (program text, G0_SPEC_v4.md S12): the statute excerpt in its style and variant (full / compact /
    short), then the closed-world sentence (one newline, no blank line: the rules stay one block). rule: a G4 partner's
    changed rule (RULE_MODES); "std" is the card of every emitted row."""
    lines = CARD_TEXT[(style, variant)].split("\n")
    if rule == "swap":
        lines[-1] = NOTICE_ONLY[style]
    elif rule == "nowd":
        lines = [ln for i, ln in enumerate(lines) if i not in DROP_LINES[style]]
    elif rule != "std":
        raise ContractError(f"rule mode {rule!r}")
    return "\n".join(lines) + "\n" + CLOSED_WORLD


# ------------------------------------------------------------------------------------------------ state blocks
NOTICE_TPL = '{STORE} posted this notice at its checkout and on its website: "{POLICY}"'
ATTACK_PREFIX = "Message added to the case: "
RECORD_FIELDS = (("ITEM", "item"), ("GOODS", "type of goods"), ("SEAL", "seal"), ("HANDOVER", "handover"),
                 ("ORDER_DATE", "ordered on (the purchase date)"), ("DELIVERY_DATE", "delivered on"),
                 ("POSSESSION_DATE", "buyer took possession on"), ("REQUEST_DATE", "return requested on"),
                 ("REASON", "reason for the return"), ("D_ORDER", "days from the purchase date to the request"),
                 ("D_DELIV", "days from delivery to the request"), ("D_POSS", "days from possession to the request"))
JSON_KEY = {"ORDER_ID": "order_id", "STORE": "store", "ITEM": "item", "GOODS": "goods_type", "SEAL": "seal",
            "HANDOVER": "handover", "ORDER_DATE": "purchase_date", "DELIVERY_DATE": "delivered_on",
            "POSSESSION_DATE": "possession_on", "REQUEST_DATE": "return_requested_on", "REASON": "reason",
            "D_ORDER": "days_purchase_to_request", "D_DELIV": "days_delivery_to_request",
            "D_POSS": "days_possession_to_request"}
ORDERS = {"S1": ("narrative", "record", "notice"), "S2": ("narrative", "record", "notice"),
          "S3": ("record", "notice", "narrative"), "S4": ("notice", "narrative", "record"),
          "S5": ("narrative", "record", "notice")}
SKIN_REGISTERS = {"S4": ("chat", "email")}


@lru_cache(maxsize=None)
def record_template(container: str, seal: bool, counts: bool) -> tuple:
    """(header, body, escape) of the order record in one container (G0_SPEC.md S13)."""
    fields = [(s, lab) for s, lab in RECORD_FIELDS if (s != "SEAL" or seal) and (not s.startswith("D_") or counts)]
    if container == "lines":
        return "Order record {ORDER_ID} from {STORE}:\n", "\n".join(f"- {lab}: {{{s}}}" for s, lab in fields), "text"
    if container == "table":
        rows = ["| field | value |", "| --- | --- |"] + [f"| {lab} | {{{s}}} |" for s, lab in fields]
        return "Order record {ORDER_ID} from {STORE}:\n", "\n".join(rows), "text"
    if container == "json":
        keys = ["ORDER_ID", "STORE"] + [s for s, _ in fields]
        return "Order record (JSON):\n", "{" + ", ".join(f'"{JSON_KEY[s]}": {{{s}}}' for s in keys) + "}", "json"
    raise ContractError(f"record container {container!r}")


def record_container(sampler: str, register: str) -> str:
    """Label-blind container choice: S5 and JSON / YAML skins get JSON; S3, ticket and form skins a table."""
    if sampler == "S5" or register in ("json", "yaml"):
        return "json"
    if sampler == "S3" or register in ("ticket", "form"):
        return "table"
    return "lines"


# ------------------------------------------------------------------------------------------------ store notices
# Lexicon sems of the posted notice (kind deontic: no promise; kind window: a promise with a period, 3/3 admission).
NO_PROMISE = ("pol.t06.final", "pol.t06.credit", "pol.t06.nocustom")
WINDOWED = ("pol.t06.faulty_order", "pol.t06.mind_order", "pol.t06.any_order", "pol.t06.any_delivery")
NOTICE_SCOPE = {"pol.t06.final": None, "pol.t06.credit": None, "pol.t06.nocustom": None,
                "pol.t06.faulty_order": ("faulty", "ordered"), "pol.t06.mind_order": ("mind", "ordered"),
                "pol.t06.any_order": ("any", "ordered"), "pol.t06.any_delivery": ("any", "delivered")}
P_SETS = {"pol.t06.faulty_order": (3, 5, 7, 10, 45, 60), "pol.t06.mind_order": (3, 5, 7, 30, 45, 60),
          "pol.t06.any_order": (7, 10, 30, 60), "pol.t06.any_delivery": (7, 10, 30, 45, 60, 90)}

# The family's negative / antonym predicates (c2_kit.polarity POLARITY_NEGATIVES): yn_may_refuse asks "may the store
# refuse / decline / turn down the refund" (G0 S11: negcount lists none of them as a cue, so the rule reads them as ONE
# lexical negative, polarity -1).
NEGATIVE_PREDICATES = (r"refus(?:e|es|ed|ing|al)", r"declin(?:e|es|ed|ing)", r"turn(?:s|ed|ing)?\s+down",
                       r"den(?:y|ies|ied|ying)", r"withh[eo]ld\w*")

# ------------------------------------------------------------------------------------------------ sampling knobs
N_CARDS, N_CARDS_HELD = 6, 4                 # cards per training sampler (24 training cards) / for S5
N_REJ, N_REJ_HELD = (14, 21, 28, 30), (20, 35)
N_WD, N_WD_HELD = (7, 10, 14), (12, 15)
QFORM_SHARES = (("ch_rule", 0.42), ("ch_end_reject", 0.07), ("ch_end_withdraw", 0.07),
                ("yn_refund", 0.11), ("yn_owed", 0.08), ("yn_double", 0.03),
                ("yn_not_refund", 0.07), ("yn_may_refuse", 0.10), ("yn_no_right", 0.05))
# ch_rule display, windows and gold (G0 v3 S10). The v2 closed set showed all four keys on every row, drew the three periods
# up front and then the target, and so the record's COARSE facts (reason, type of goods, notice scope) decided the answer by
# themselves: "change of mind" rules out the faulty-goods right, excluded goods rule out withdrawal, a no-promise notice rules
# out the notice, and because the statutory windows nested (N_WD <= 14 <= N_REJ, one request day, all anchors before it) the
# only rule that can ever be the sole grantor is the one whose window ends last. The G6 "card without question" view of a
# ch_rule row (one fixed question, so the facts are all there is) scored 0.45 against 0.25 on 986 rows; the reason alone
# predicts the key at 0.47 and reason + exclusion + notice scope at 0.59 (in-sample Bayes bound on the v2 rows). v3:
#   display  the rules the coarse facts leave open (_applicable: reason faulty -> reject; goods not excluded -> withdraw; a
#            notice that promises for this reason -> store; at least two) plus "none", the abstain option: k = 3 or 4, so no
#            shown option is ruled out by the reason, the goods or the notice alone;
#   target   drawn uniformly over the display BEFORE any period or date, so every shown option, "none" included, is gold on
#            1 / k of the rows (the abstain bands of c2_kit.choiceplan);
#   windows  the target's window ends on a day drawn from a wide range, every other window 1-3 days earlier (a refusal: all
#            within 3 days of one another), and each period is that end minus the rule's own anchor lag (so the numbers
#            are whatever the lags make them, and neither a period nor a printed day count says which rule wins: v3's first
#            draw took the periods from one pool and the gold was the largest period on 96% of the rows, and the printed
#            day counts alone gave the G6 card view +3 pp); the request is one of the last NEAR_DAYS days of the target's
#            window (the first days after the last window for "none").
# Nothing is relabelled: the target comes first and the dates realise it; solver A still derives the gold from the record.
NONE_KEY = "none"
RULE3 = ("reject", "withdraw", "store")
MIN_RULES_SHOWN = 2          # a ch_rule row shows at least two rules besides "none" (k >= 3: an abstain option needs it)
E_RANGE, E_RANGE_HELD = (9, 34), (35, 45)   # ch_rule: the last window's end, in days from possession (S5: longer ends)
GAP_MAX = 3                  # ch_rule: every other window ends 1..GAP_MAX days before the target's ("none": 0..GAP_MAX)
NEAR_DAYS = 4                # the request is one of the last NEAR_DAYS days of a window (the first after it, for a refusal)
END_FORMS = ("ch_end_reject", "ch_end_withdraw")
GOODS_W = (("standard", 0.40), ("custom", 0.18), ("perishable", 0.14), ("hygiene", 0.28))
HANDOVER_W = (("direct", 0.60), ("locker", 0.25), ("neighbour", 0.15))
POLICY_W = (("pol.t06.final", 0.16), ("pol.t06.credit", 0.11), ("pol.t06.nocustom", 0.08),
            ("pol.t06.faulty_order", 0.14), ("pol.t06.mind_order", 0.19), ("pol.t06.any_order", 0.15),
            ("pol.t06.any_delivery", 0.17))
SHIP_W = ((1, 0.08), (2, 0.18), (3, 0.22), (4, 0.18), (5, 0.14), (6, 0.10), (7, 0.06), (8, 0.04))   # order -> delivery
PICKUP_W = ((1, 0.30), (2, 0.25), (3, 0.18), (4, 0.12), (5, 0.09), (6, 0.06))     # delivery -> possession (not direct)
P_BOUNDARY, P_ORDER_TRAP, P_COND = 0.08, 0.08, 0.00   # label-blind preferences among the dates that realise a target
S2_BOOST = 0.30                                        # S2 label-first: every trap preference raised
P_FEB, P_MONTH_END = 0.22, 0.33                        # delivery dates before a February end / a month end
DEEP_RATE = 0.06                                       # day counts not printed (meta.deep), yes/no and ch_rule only
COMP_RATE, TWIN_RATE, EQUIV_RATE, INV_RATE = 0.42, 0.48, 0.11, 0.04   # twin 0.48: 22% of rows (spec 4.1: 20-25)
# ch_rule twins that move the gold onto "none" from a deciding rule are kept at this rate (kit
# relations.abstain_twin_kept; the twin search then looks for an edit that names another rule), by the row's option count
# k (the display plus "none"), so "none" is 1 / k of the emitted rows in each k cell, twins included: unthinned twins
# were 70% none (38% of rows); with one rate for both k the twins were 32% none at k = 3 (right, 33%) but 36% at k = 4
# (right: 25%), and "none" is the longest option text in every style, so the shortfall showed as gold-is-longest -2.5 pp
TWIN_NONE_KEEP = {3: 0.22, 4: 0.05}
MAX_TRIES = 200

# Error models (every wrong option names one; G0_SPEC.md S20).
for _name, _text in (
        ("t06_sign_wins", "follows the store's posted notice instead of the statute, as if a stricter notice could "
                          "remove the statutory rights"),
        ("t06_ignore_notice", "applies the statute alone and ignores what the store's posted notice promises"),
        ("t06_order_date_anchor", "counts the statutory periods from the order (purchase) date instead of the "
                                  "delivery date or the day the buyer took possession"),
        ("t06_delivery_for_possession", "counts the withdrawal period from the delivery date instead of the day the "
                                        "buyer took possession"),
        ("t06_possession_for_delivery", "counts the faulty-goods period from the day the buyer took possession "
                                        "instead of the delivery date"),
        ("t06_absolute_exception", "treats an exclusion as absolute: applies the hygiene exclusion with the seal "
                                   "intact, or applies the exclusions to the faulty-goods right as well"),
        ("t06_swap_periods", "uses the withdrawal period for faulty goods and the faulty-goods period for withdrawal"),
        ("t06_notice_from_delivery", "counts a notice period stated from the purchase date from the delivery date "
                                     "instead"),
        ("t06_notice_any_reason", "reads the store's notice as covering every reason for a return, ignoring the "
                                  "reason it names"),
        ("t06_reason_picks_rule", "names the statutory right that matches the stated reason, ignoring its period "
                                  "and its exclusions"),
        ("t06_other_right", "mixes up the two statutory rights: names the withdrawal right for a faulty return and "
                            "the faulty-goods right for a change of mind"),
        ("t06_sign_decides", "names the store's posted notice as the deciding rule because it is the rule on "
                             "display"),
        ("t06_both_ends_early", "counts the event's day as day 1 and also leaves out the last day (two days early)"),
        ("t06_both_ends_late", "starts counting the day after day zero and also counts one day past the last day "
                               "(two days late)"),
        ("t06_business_days", "counts the statutory period in weekdays (Monday to Friday) instead of calendar days"),
        ("t06_notice_period", "uses the store notice's number of days instead of the statute's period")):
    register_name(_name, _text)
END_K = (3, 4)               # ch_end_*: label-blind option count, from the row's display plan (choiceplan)


# ------------------------------------------------------------------------------------------------ facts
@dataclass(frozen=True)
class Facts:
    style: str
    juris: str
    n_rej: int
    n_wd: int
    store: str
    policy: str              # notice sem id
    p: int | None            # the notice's days (windowed notices only)
    goods: str
    seal: str | None         # hygiene goods only
    handover: str
    reason: str
    ordered: dt.date
    delivered: dt.date
    possession: dt.date
    requested: dt.date


def facts(spec: Spec) -> Facts:
    v = spec.env()
    return Facts(spec.structure["style"], v["JURIS"], v["N_REJ"], v["N_WD"], v["STORE"], v["POLICY"],
                 v.get("P_DAYS"), v["GOODS"], v.get("SEAL"), v["HANDOVER"], v["REASON"], v["ORDER_DATE"],
                 v["DELIVERY_DATE"], v["POSSESSION_DATE"], v["REQUEST_DATE"])


# Construction side (sampling targets, twin predictions, error models, trap tags). Solver A does not use these: it
# runs the decision tables below on day ordinals.
def _excluded(goods: str, seal, absolute: bool = False) -> bool:
    if goods in ("custom", "perishable"):
        return True
    if goods == "hygiene":
        return absolute or seal == "opened"
    return False


def _grants(f: Facts, *, statute=True, notice=True, rej_anchor="delivered", wd_anchor="possession", shift=0,
            absolute=False, ignore_exc=False, swap=False, notice_anchor=None, notice_any_reason=False,
            no_withdraw=False) -> frozenset:
    """The rules that give a full refund (keys reject / withdraw / store); the keyword arguments switch on one named
    mistake each (error models and trap tags)."""
    def within(anchor: dt.date, n: int) -> bool:
        return 0 <= (f.requested - anchor).days <= n + shift

    n_rej, n_wd = (f.n_wd, f.n_rej) if swap else (f.n_rej, f.n_wd)
    out = set()
    if statute:
        if (f.reason == "faulty" and within(getattr(f, rej_anchor), n_rej)
                and not (absolute and _excluded(f.goods, f.seal, True))):
            out.add("reject")
        if (not no_withdraw and (ignore_exc or not _excluded(f.goods, f.seal, absolute))
                and within(getattr(f, wd_anchor), n_wd)):
            out.add("withdraw")
    scope = NOTICE_SCOPE[f.policy]
    if notice and scope is not None:
        reason, anchor = scope
        if (reason in ("any", f.reason) or notice_any_reason) and within(getattr(f, notice_anchor or anchor), f.p):
            out.add("store")
    return frozenset(out)


def _answer(qform: str, grants: frozenset, f: Facts):
    """The answer a construction implies (twin predictions, error models). ch_rule with two granting rules: None."""
    if qform == "ch_rule":
        return next(iter(grants)) if len(grants) == 1 else ("none" if not grants else None)
    if qform == "ch_end_reject":
        return (f.delivered + TD(days=f.n_rej)).isoformat()
    if qform == "ch_end_withdraw":
        return (f.possession + TD(days=f.n_wd)).isoformat()
    q = T06Plugin.QFORMS[qform]
    return int(bool(grants) if q.polarity == 1 else not grants)


def _decision(qform: str, grants: frozenset):
    """What the case's traps are measured on: the deciding rule (ch_rule) or the refund decision (other forms)."""
    if qform == "ch_rule":
        return next(iter(grants)) if len(grants) == 1 else ("none" if not grants else "several")
    return bool(grants)


def _notice_count(f: Facts):
    scope = NOTICE_SCOPE[f.policy]
    return None if scope is None else (f.requested - getattr(f, scope[1])).days


def _restrictive(f: Facts) -> bool:
    """The notice reads as refusing this case: no promise at all, a refusal of this item type, or a promise for
    this reason whose period has run out."""
    if f.policy in ("pol.t06.final", "pol.t06.credit"):
        return True
    if f.policy == "pol.t06.nocustom":
        return f.goods == "custom"
    scope = NOTICE_SCOPE[f.policy]
    return scope[0] in ("any", f.reason) and _notice_count(f) > f.p


TRAP_MISTAKES = {"order_date": (dict(rej_anchor="ordered", wd_anchor="ordered"),),
                 "possession_date": (dict(wd_anchor="delivered"), dict(rej_anchor="possession")),
                 "boundary_day": (dict(shift=-1), dict(shift=1)),
                 "conditional_exception": (dict(absolute=True),)}


def _flips(f: Facts, qform: str, mistakes: tuple) -> bool:
    base = _decision(qform, _grants(f))
    return any(_decision(qform, _grants(f, **kw)) != base for kw in mistakes)


def _consistent(f: Facts, qform: str) -> bool:
    """Facts a generator (or a twin edit) may produce."""
    if not f.ordered < f.delivered <= f.possession <= f.requested:
        return False
    if (f.handover == "direct") != (f.possession == f.delivered):
        return False
    if (f.goods == "hygiene") != (f.seal is not None) or (f.policy in WINDOWED) != (f.p is not None):
        return False
    if min(f.n_rej, f.n_wd, f.p or 1) < 1:
        return False
    if qform == "ch_end_reject" and f.reason != "faulty":
        return False
    if qform == "ch_end_withdraw" and _excluded(f.goods, f.seal):
        return False
    return True


def _generable(f: Facts, qform: str) -> bool:
    """Facts the generator and the twin edits may emit: consistent, and the request is never on the possession day
    (G0 H1: "day zero is in time" and "days 1..N are in time" then give the same answer on every row; both solvers
    still count day zero as in time, S2)."""
    return _consistent(f, qform) and f.possession < f.requested


def _applicable(f: Facts) -> tuple:
    """The rules the record's coarse facts leave open (G0 v3 S10; sorted): the faulty-goods right needs the reason "faulty",
    withdrawal needs goods that are not excluded, the notice needs a promise that covers the reason. A function of
    everything but the dates and the periods, so twins that edit dates show the same options (G-TW)."""
    out = []
    if f.reason == "faulty":
        out.append("reject")
    if not _excluded(f.goods, f.seal):
        out.append("withdraw")
    scope = NOTICE_SCOPE[f.policy]
    if scope is not None and scope[0] in ("any", f.reason):
        out.append("store")
    return tuple(sorted(out))


def _ends(f: Facts) -> dict:
    """The last in-time day (ordinal) of every applicable rule's window."""
    anchor = {"reject": (f.delivered, f.n_rej), "withdraw": (f.possession, f.n_wd)}
    scope = NOTICE_SCOPE[f.policy]
    if scope is not None:
        anchor["store"] = (getattr(f, scope[1]), f.p)
    return {k: a.toordinal() + n for k, (a, n) in anchor.items() if k in _applicable(f)}


# ------------------------------------------------------------------------------------------------ solver A tables
# Solver A's own tables (decision_table paradigm): every rule is a lookup, every period test an ordinal difference.
EXCLUSION_TABLE = {("standard", None): False, ("custom", None): True, ("perishable", None): True,
                   ("hygiene", "intact"): False, ("hygiene", "opened"): True}
REJECT_TABLE = {("faulty", True): True, ("faulty", False): False, ("mind", True): False, ("mind", False): False}
WITHDRAW_TABLE = {(False, True): True, (False, False): False, (True, True): False, (True, False): False}
NOTICE_TABLE = {   # (notice sem, reason) -> the record date its period runs from, or None (no promise for the case)
    ("pol.t06.final", "faulty"): None, ("pol.t06.final", "mind"): None,
    ("pol.t06.credit", "faulty"): None, ("pol.t06.credit", "mind"): None,
    ("pol.t06.nocustom", "faulty"): None, ("pol.t06.nocustom", "mind"): None,
    ("pol.t06.faulty_order", "faulty"): "ORDER_DATE", ("pol.t06.faulty_order", "mind"): None,
    ("pol.t06.mind_order", "faulty"): None, ("pol.t06.mind_order", "mind"): "ORDER_DATE",
    ("pol.t06.any_order", "faulty"): "ORDER_DATE", ("pol.t06.any_order", "mind"): "ORDER_DATE",
    ("pol.t06.any_delivery", "faulty"): "DELIVERY_DATE", ("pol.t06.any_delivery", "mind"): "DELIVERY_DATE",
}
OUTCOME_TABLE = {   # (rejection, withdrawal, notice) -> (full refund owed, deciding rule)
    (False, False, False): (False, "none"), (True, False, False): (True, "reject"),
    (False, True, False): (True, "withdraw"), (False, False, True): (True, "store"),
    (True, True, False): (True, "several"), (True, False, True): (True, "several"),
    (False, True, True): (True, "several"), (True, True, True): (True, "several"),
}


def _only_rule(decider: str) -> str:
    if decider == "several":
        raise ContractError("ch_rule asked on a case where two rules give the refund (never generated)")
    return decider


QUESTION_TABLE = {
    "yn_refund": lambda refund, decider: 1 if refund else 0,
    "yn_owed": lambda refund, decider: 1 if refund else 0,
    "yn_double": lambda refund, decider: 1 if refund else 0,
    "yn_not_refund": lambda refund, decider: 0 if refund else 1,
    "yn_may_refuse": lambda refund, decider: 0 if refund else 1,
    "yn_no_right": lambda refund, decider: 0 if refund else 1,
    "ch_rule": lambda refund, decider: _only_rule(decider),
}


# ------------------------------------------------------------------------------------------------ helpers
def _weyl(seed: int, sampler: str, which: int) -> float:
    """Low-discrepancy draw per seed (gold and question form): shares hold tightly on any run of seeds."""
    alpha = (0.6180339887498949, 0.41421356237309515)[which]
    return (seed * alpha + uhash(FAMILY, "weyl", sampler, which)) % 1.0


def _share(table: tuple, u: float) -> str:
    acc = 0.0
    for k, w in table:
        acc += w
        if u < acc:
            return k
    return table[-1][0]


def _weighted(rng: random.Random, items) -> object:
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


def _delivery_date(rng: random.Random) -> dt.date:
    """Delivery dates that make the periods cross a February end (leap and common years) or a month end."""
    r = rng.random()
    if r < P_FEB:
        return dt.date(rng.choice((2027, 2028)), 2, 1) + TD(days=rng.randrange(6, 28))
    if r < P_FEB + P_MONTH_END:
        y, m = rng.choice((2026, 2027, 2028)), rng.randrange(1, 13)
        last = dt.date(y + (m == 12), m % 12 + 1, 1) - TD(days=1)
        return last - TD(days=rng.randrange(0, 8))
    return dt.date(2026, 1, 15) + TD(days=rng.randrange(0, 1050))


@dataclass(frozen=True)
class Scenario:
    reason: str
    goods: str
    seal: str | None
    handover: str
    policy: str
    p: int | None
    item: str


# ------------------------------------------------------------------------------------------------ the plugin
class T06Plugin(C2Plugin):
    FAMILY = FAMILY
    TIER = "everyday"
    G0_LITE = HERE / "G0_SPEC_v4.md"
    G0_SHA256 = "84b81c33c293969c325d88aafb0fa5d4e172d3ccdd4607964884e35e038063d7"   # G0 v4, frozen 14 Oct (section 9); v3 was 2d97b12f
    G0_SHA256_AUTHORED = "4f6b322adab8a1810ac165686a2305d28607de558131118780c52da5f0e59563"   # v2 = G0_SPEC.md, the
    # version every pools_v2 task, answer and manifest was authored against (freeze_v2.py, haiku_author.py, pool_freeze.py)
    G0_HAIKU_TASK = "c2-data-stage-a/amb:T06"
    G0_AMBIGUITY_PASS = {"task": "c2-data-stage-a/amb:T06", "model": "haiku", "date": "2026-10-13", "n_points": 52,
                         "points_file": "haiku/ambiguity/amb_T06_points.json",
                         "points_sha256": "b4d675cc56271b5f7580daacbbb676779b49b07dca7fda4f66204ff52ad6fe87",
                         "input_g0_sha256": "7991d7d56cea25800afb62fdad93ab0d41eccc540012c59bf237d690150b0f46",
                         "resolved_in": "G0_SPEC.md (v2) section 7 (H1-H52)"}
    SAMPLERS = ("S1", "S2", "S3", "S4", "S5")
    HELD_OUT_SAMPLERS = ("S5",)
    PARADIGM_A = "decision_table"
    PARADIGM_B = "day_bitmap"
    SOLVER_B_MODULE = "families.T06.solver_b"
    QFORMS = {q.qform: q for q in (
        QuestionForm("yn_refund", "noul", "refund", 1, yes_is_bad=False),
        QuestionForm("yn_owed", "noul", "refund", 1, yes_is_bad=False),
        QuestionForm("yn_double", "noul", "refund", 1, yes_is_bad=False),
        QuestionForm("yn_not_refund", "noul", "refund", -1, "syntactic", yes_is_bad=True),
        QuestionForm("yn_may_refuse", "noul", "refund", -1, "antonym", yes_is_bad=True),
        QuestionForm("yn_no_right", "noul", "refund", -1, "syntactic", yes_is_bad=True),
        QuestionForm("ch_rule", "choice", answer_set="closed"),
        QuestionForm("ch_end_reject", "choice", answer_set="open"),
        QuestionForm("ch_end_withdraw", "choice", answer_set="open"),
    )}
    LABEL_WORDS = ("refund", "entitled", "owed", "owe", "reject", "rejection", "withdraw", "withdrawal", "faulty",
                   "defect", "defective", "broken", "final", "late", "full refund", "in time", "store credit",
                   "no refunds")
    CLOSED_WORLD_SENTENCE = CLOSED_WORLD
    REGISTERS = ("chat", "email", "ticket", "memo", "receipt", "json", "yaml", "form", "transcript", "letter")
    HELD_OUT_REGISTERS = ("transcript", "letter")
    GSL_EXCEPTIONS: dict = {}
    NAME_ALLOW: tuple = ()
    # wording polarity (c2_kit.polarity P1-P3; G0 v3 S11): the antonym form yn_may_refuse reads "refuse / decline / turn
    # down" as ONE negative predicate (polarity -1, no syntactic cue), so a wording may negate a positive predicate
    # ("has no right", "is not entitled") or use one of these, never both. yn_double carries two syntactic negations over
    # a positive predicate. P4 (strict "aux + subject + not" frames) is not applied: 12 yn_not_refund wordings use "Is the
    # customer not entitled ...?", the family's one-negation syntactic form (lead ruling, G0 v3 section 7).
    POLARITY_CHECK = True
    POLARITY_NEGATIVES = NEGATIVE_PREDICATES
    POLARITY_STRICT_FRAMES = False

    def __init__(self, lexicon=None):
        super().__init__(lexicon)
        self._screened: list = []                  # [(ctx, screened ctx, {wording id: problems})]

    def ctx_for(self, spec, ctx):
        """The kit context without the wordings that break the polarity rule (c2_kit.polarity), so neither render() nor
        the pipeline's complement partner can pick one. Label-blind (the wording text and its form only); cached per
        context object. The frozen pool holds none (G0 v3 section 7); this is the safety net for a re-authored pool."""
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

    # ------------------------------------------------------------------------------------------- display plans
    @staticmethod
    def row_key(spec: Spec) -> str:
        return f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"

    @staticmethod
    def end_plan(key: str) -> ChoicePlan:
        """The display plan of a ch_end_* row (no abstain option): k (3 or 4), the gold's position and its sorted rank
        among the dates, from the row key alone."""
        return plan_choice(key, ks=END_K, abstain=False)

    def _end_options(self, spec: Spec, ans=None, fmt=None):
        """The planned ch_end_* option set (dates in one form), or None when the error-model dates cannot fill the plan's
        k and rank around the gold, or when an option would equal a date the record prints: sample() then draws another
        structure (the plan never changes) and twins that cannot fill it are not proposed."""
        key = self.row_key(spec)
        ans = self.solve_a(spec) if ans is None else ans
        if fmt is None:
            def as_text(iso: str) -> str:
                return iso
        else:
            def as_text(iso: str) -> str:
                return S.render(S.date_slot(dt.date.fromisoformat(iso)), fmt)
        os_ = build_options(spec, ans, self.error_models(), row_key=key, render_key=as_text, order_key=str,
                            plan=self.end_plan(key), strict_plan=False)
        if os_ is None:
            return None
        f = facts(spec)
        printed = {d.isoformat() for d in (f.ordered, f.delivered, f.possession, f.requested)}
        if any(o.key in printed for o in os_.options):
            # an option that equals a date the record prints would appear verbatim in the text, and G6 / G7 read "the option
            # is printed in the record" as a cue (v2: an option equal to the request date was the gold on 58% of the rows
            # that had one, 154 options in 815 rows): another structure is drawn, never another option
            return None
        return os_

    # ------------------------------------------------------------------------------------------- sampling
    def sample(self, seed: int, sampler: str) -> Spec:
        if sampler not in self.SAMPLERS:
            raise ContractError(f"sampler {sampler}")
        if self.lexicon is None:
            raise ContractError("T06 needs its lexicon registry (T06Plugin(lexicon=...)) for the notice forms")
        rng = random.Random(f"{FAMILY}|{sampler}|{seed}")
        held = sampler in self.HELD_OUT_SAMPLERS
        card = seed % (N_CARDS_HELD if held else N_CARDS)
        style = HELD_STYLE if held else TRAIN_STYLES[card % len(TRAIN_STYLES)]
        jpool = JURIS_HELD if held else JURIS
        juris = jpool[(card + 3 * self.SAMPLERS.index(sampler)) % len(jpool)]
        qform = _share(QFORM_SHARES, _weyl(seed, sampler, 1))
        counts = qform in END_FORMS or uhash(FAMILY, "deep", sampler, seed) >= DEEP_RATE
        # display and rule draws first (label-blind): names, order id, period lengths, trap preferences, card variant
        customer, store = rng.choice(CUSTOMERS), rng.choice(STORES)
        order_id = f"ORD-{rng.randrange(10000, 100000)}"
        n_rej, n_wd = rng.choice(N_REJ_HELD if held else N_REJ), rng.choice(N_WD_HELD if held else N_WD)
        boost = S2_BOOST if sampler == "S2" else 0.0
        wants = (rng.random() < P_BOUNDARY + boost, rng.random() < P_ORDER_TRAP + boost, rng.random() < P_COND + boost)
        variant = CD.draw_style(f"{FAMILY}|{sampler}|{seed}|card", CARD_SHARES_HELD if held else CARD_SHARES)
        u0 = _weyl(seed, sampler, 0)
        # then the target answer (ch_rule: after the display, uniformly over it), then a scenario and the dates that realise it
        target = None if qform == "ch_rule" else self._target(qform, u0, _card_rate(sampler, card))
        for _ in range(MAX_TRIES):
            sc = self._scenario(rng)
            if qform == "ch_rule":
                got = self._realize_rule(rng, sc, style, juris, store, held, u0, wants, f"{FAMILY}|{seed}|{sampler}|{qform}")
                f, target = got if got is not None else (None, None)
            else:
                if not self._possible(sc, qform, target):
                    continue
                f = self._realize(rng, sc, style, juris, store, n_rej, n_wd, qform, target, wants)
            if f is None:
                continue
            slots = {"CUSTOMER": S.name_slot(customer), "STORE": S.name_slot(store), "ORDER_ID": S.id_slot(order_id),
                     "ITEM": S.name_slot(sc.item), "JURIS": S.name_slot(juris), "N_REJ": S.count_slot(f.n_rej, DAYS),
                     "N_WD": S.count_slot(f.n_wd, DAYS), "GOODS": S.category_slot(f.goods, GOODS_SET),
                     "HANDOVER": S.category_slot(f.handover, HANDOVER_SET),
                     "REASON": S.category_slot(f.reason, REASON_SET), "ORDER_DATE": S.date_slot(f.ordered),
                     "DELIVERY_DATE": S.date_slot(f.delivered), "POSSESSION_DATE": S.date_slot(f.possession),
                     "REQUEST_DATE": S.date_slot(f.requested), "POLICY": self._policy_clause(f.policy, rng)}
            if f.seal is not None:
                slots["SEAL"] = S.category_slot(f.seal, SEAL_SET)
            if f.p is not None:
                slots["P_DAYS"] = S.count_slot(f.p, DAYS)
            spec = Spec(FAMILY, sampler, seed, f"{FAMILY}:{sampler}:c{card:02d}", qform, slots,
                        structure={"style": style, "counts": counts, "card": variant}, depth=2 if counts else 3,
                        deep=not counts, pack=f"t06.{style}.{juris.lower()}.{sampler}.c{card:02d}")
            spec = self.derive(spec)
            if qform == "ch_rule" and _answer(qform, _grants(f), f) != target:
                raise ContractError(f"{sampler}/{seed}: the realised ch_rule gold disagrees with its target")
            if qform in END_FORMS and self._end_options(spec) is None:
                continue                       # the dates cannot fill the planned k and rank: another structure
            return spec
        raise ContractError(f"{sampler}/{seed}: no scenario realises target {target!r} for {qform}")

    def _target(self, qform: str, u: float, rate: float) -> str:
        """The target before any fact exists: the refund decision (yes/no) or any date (ch_end_*). A ch_rule target needs
        its display first (_realize_rule)."""
        if qform in END_FORMS:
            return "any"
        q = self.QFORMS[qform]
        yes = u < rate
        return "refund" if (yes if q.polarity == 1 else not yes) else "no_refund"

    def _scenario(self, rng: random.Random) -> Scenario:
        reason = "faulty" if rng.random() < 0.5 else "mind"
        goods = _weighted(rng, GOODS_W)
        seal = rng.choice(("intact", "opened")) if goods == "hygiene" else None
        handover = _weighted(rng, HANDOVER_W)
        policy = _weighted(rng, POLICY_W)
        p = rng.choice(P_SETS[policy]) if policy in P_SETS else None
        return Scenario(reason, goods, seal, handover, policy, p, rng.choice(ITEMS[goods]))

    @staticmethod
    def _possible(sc: Scenario, qform: str, target: str) -> bool:
        """Can some dates realise the target in this scenario? (Cheap pre-check; _realize decides.)"""
        can_rej = sc.reason == "faulty"
        can_wd = not _excluded(sc.goods, sc.seal)
        scope = NOTICE_SCOPE[sc.policy]
        can_store = scope is not None and scope[0] in ("any", sc.reason)
        if qform == "ch_end_reject":
            return can_rej
        if qform == "ch_end_withdraw":
            return can_wd
        return {"refund": can_rej or can_wd or can_store, "no_refund": True, "reject": can_rej, "withdraw": can_wd,
                "store": can_store, "none": True}[target]

    @staticmethod
    def _hits(qform: str, target: str, g: frozenset) -> bool:
        if target == "any":
            return True
        if target == "refund":
            return bool(g)
        if target in ("no_refund", "none"):
            return not g
        return g == {target}

    @staticmethod
    def _draw_base(rng, sc: Scenario, style, juris, store, n_rej, n_wd) -> Facts:
        """The record's facts before the request: shipping and pickup lags and a delivery date (the request is placed on
        the possession day; every caller replaces it)."""
        ship = _weighted(rng, SHIP_W)
        pickup = 0 if sc.handover == "direct" else _weighted(rng, PICKUP_W)
        delivered = _delivery_date(rng)
        return Facts(style, juris, n_rej, n_wd, store, sc.policy, sc.p, sc.goods, sc.seal, sc.handover,
                     sc.reason, delivered - TD(days=ship), delivered, delivered + TD(days=pickup),
                     delivered + TD(days=pickup))

    def _pick_request(self, rng, base: Facts, qform, target, wants, near: int | None = None, edge: bool = False):
        """The request day (days from possession) chosen among every day that hits the target, with the label-blind trap
        preferences; None when no day hits it. near: only the last `near` of those days (the first `near` for "none"):
        the request sits at the edge of the target's tail, so the printed day counts say nothing about the target."""
        want_boundary, want_order, want_cond = wants
        dmax = max(base.n_rej, base.n_wd, base.p or 0) + 10
        cands = [f for f in (replace(base, requested=base.possession + TD(days=d)) for d in range(1, dmax + 1))
                 if self._hits(qform, target, _grants(f)) and _generable(f, qform)]
        if not cands:
            return None
        for want, trap in ((want_boundary, "boundary_day"), (want_order, "order_date"),
                           (want_cond, "conditional_exception")):
            if want:
                sub = [f for f in cands if _flips(f, qform, TRAP_MISTAKES[trap])]
                cands = sub or cands
        if near is not None:
            cands = cands[:near] if target == NONE_KEY else cands[-near:]
        elif edge:
            cands = self._edge_days(rng, base, cands, target)
        return rng.choice(cands)

    @staticmethod
    def _edge_days(rng, base: Facts, cands: list, target: str) -> list:
        """Yes/no rows: the request sits within NEAR_DAYS of the end of one rule's window, whatever the target. A refund
        lies in the last days of one applicable window; a refusal with an applicable rule lies in the first days after the
        latest window ends; a refusal with no applicable rule lies in the last days of a window the case does not use
        (a period of the card or the notice). So the printed day counts have the same size in both classes: v2 drew the
        request uniformly over every day that hits the target and the counts' magnitude said how late it was (G6
        metadata view: refund rate 0.35 in the top decile of the mean numeral magnitude, 0.60 in the bottom ones)."""
        pos = base.possession.toordinal()
        day = lambda f: f.requested.toordinal() - pos            # noqa: E731
        app = sorted({end - pos for end in _ends(base).values()})
        if target == "refund":
            order = list(app)
            rng.shuffle(order)
            for e in order:
                sub = [f for f in cands if e - NEAR_DAYS < day(f) <= e]
                if sub:
                    return sub
            return cands[-NEAR_DAYS:]
        if app:
            return sorted(cands, key=day)[:NEAR_DAYS]
        scope = NOTICE_SCOPE[base.policy]
        hyp = [base.delivered.toordinal() + base.n_rej - pos, base.n_wd,
               (getattr(base, scope[1]).toordinal() + base.p - pos) if scope is not None else base.n_rej]
        e = rng.choice([x for x in hyp if x >= 1] or [NEAR_DAYS])
        sub = [f for f in cands if e - NEAR_DAYS < day(f) <= e]
        return sub or sorted(cands, key=day)[:NEAR_DAYS]

    def _realize(self, rng, sc: Scenario, style, juris, store, n_rej, n_wd, qform, target, wants):
        """Facts whose grant set hits the target: shipping and pickup lags, a delivery date, then the request day."""
        for _ in range(8):
            f = self._pick_request(rng, self._draw_base(rng, sc, style, juris, store, n_rej, n_wd), qform, target,
                                   wants, edge=qform not in END_FORMS)
            if f is not None:
                return f
        return None

    @staticmethod
    def rule_order(key: str, rules: tuple) -> tuple:
        """(display in its label-blind order of the row key, the planned gold position) of a ch_rule row (G0 v4 S10): the
        shown rules + "none" (k = len(rules) + 1, set by the record's coarse facts before any target exists) in the
        order build_closed gives them (a function of the key and the display alone, so a twin shows the same list), and the
        kit ChoicePlan's position (closed set, abstain shown: uniform over the k places by construction, from the row
        key alone). The target is the option AT that position, so the gold position is scheduled, never left to the draw."""
        order = tuple(sorted(rules + (NONE_KEY,), key=lambda a: uhash(key, "closed", repr(a))))
        return order, plan_choice(key, closed=len(rules), abstain=True).pos

    def _realize_rule(self, rng, sc: Scenario, style, juris, store, held: bool, u: float, wants, key: str):
        """(facts, target) of a ch_rule row, label-first: the display (the rules the coarse facts leave open, at least
        MIN_RULES_SHOWN, plus "none"), then the target from the row's plan ("none" when the plan says so, else uniform
        over the shown rules by the low-discrepancy u: every shown option is gold on 1 / k of the rows), then lags, delivery date and the three periods (one pool for the statute and the notice)
        until the target's window ends strictly last, then the request day near the end of the target's tail."""
        probe = Facts(style, juris, 1, 1, store, sc.policy, sc.p, sc.goods, sc.seal, sc.handover, sc.reason,
                      dt.date(2026, 1, 1), dt.date(2026, 1, 2), dt.date(2026, 1, 2), dt.date(2026, 1, 3))
        applicable = _applicable(probe)
        if len(applicable) < MIN_RULES_SHOWN:
            return None
        order, pos = self.rule_order(key, tuple(sorted(applicable)))
        target = order[pos]
        lo, hi = E_RANGE_HELD if held else E_RANGE
        scope = NOTICE_SCOPE[sc.policy]
        for _ in range(24):
            base = self._draw_base(rng, sc, style, juris, store, 1, 1)         # lags and delivery date; periods follow
            pos = base.possession
            last = rng.randint(lo, hi)

            def end(rule: str) -> int:
                """The window's last in-time day, in days from possession: the target's is `last`, the others end earlier."""
                if target == NONE_KEY:
                    return last - rng.randint(0, GAP_MAX)
                return last if rule == target else last - rng.randint(1, GAP_MAX)
            n_rej = end("reject") + (pos - base.delivered).days
            n_wd = end("withdraw")
            p = end("store") + (pos - getattr(base, scope[1])).days if scope is not None else None
            f = self._pick_request(rng, replace(base, n_rej=n_rej, n_wd=n_wd, p=p), "ch_rule", target, wants,
                                   near=NEAR_DAYS)
            if f is not None:
                return f, target
        return None

    def _policy_clause(self, sem: str, rng: random.Random | None) -> S.Slot:
        """A clause slot for one admitted notice form of `sem` (rng None: the first admitted form)."""
        ids = sorted(fid for fid, x in self.lexicon.forms.items()
                     if x.sem_id == sem and self.lexicon.status(fid) == "admitted")
        if not ids:
            raise ContractError(f"no admitted notice form for {sem}")
        fid = ids[0] if rng is None else rng.choice(ids)
        return self.lexicon.clause(fid, bind={"P": "P_DAYS"} if sem in WINDOWED else {})

    def derive(self, spec: Spec) -> Spec:
        """Printed intermediates: the three day counts to the request date (not on deep rows); then the trap tags."""
        v = spec.env()
        derived, deps = {}, {}
        if spec.structure["counts"]:
            for name, src in (("D_ORDER", "ORDER_DATE"), ("D_DELIV", "DELIVERY_DATE"), ("D_POSS", "POSSESSION_DATE")):
                derived[name] = S.count_slot((v["REQUEST_DATE"] - v[src]).days, DAYS)
                deps[name] = (src, "REQUEST_DATE")
        spec = spec.replace(derived=derived, derived_deps=deps)
        return spec.replace(tags=self._tags(spec))

    def _tags(self, spec: Spec) -> tuple:
        f = facts(spec)
        g = _grants(f)
        statute = bool(g & {"reject", "withdraw"})
        t = {trap for trap, mistakes in TRAP_MISTAKES.items() if _flips(f, spec.qform, mistakes)}
        if statute and "store" not in g and _restrictive(f):
            t.add("stricter_sign")
        if "store" in g and not statute:
            t.add("generous_notice")
        if not spec.structure["counts"]:
            t.add("deep")
        if f.ordered <= dt.date(2028, 2, 29) <= f.requested:
            t.add("leap_day")
        if (f.delivered.year, f.delivered.month) != (f.requested.year, f.requested.month):
            t.add("month_end")
        return tuple(sorted(t))

    # ------------------------------------------------------------------------------------------- solver A
    def solve_a(self, spec: Spec):
        v = spec.env()

        def day(name: str) -> int:
            return v[name].toordinal()

        if spec.qform == "ch_end_reject":
            return dt.date.fromordinal(day("DELIVERY_DATE") + v["N_REJ"]).isoformat()
        if spec.qform == "ch_end_withdraw":
            return dt.date.fromordinal(day("POSSESSION_DATE") + v["N_WD"]).isoformat()
        req = day("REQUEST_DATE")
        rule = spec.structure.get("rule", "std")         # a G4 partner: the notice replaces the statute / no withdrawal rule
        rej = REJECT_TABLE[(v["REASON"], rule != "swap" and req - day("DELIVERY_DATE") <= v["N_REJ"])]
        excluded = EXCLUSION_TABLE[(v["GOODS"], v.get("SEAL"))]
        wd = WITHDRAW_TABLE[(excluded, rule == "std" and req - day("POSSESSION_DATE") <= v["N_WD"])]
        anchor = NOTICE_TABLE[(v["POLICY"], v["REASON"])]
        st = anchor is not None and req - day(anchor) <= v["P_DAYS"]
        refund, decider = OUTCOME_TABLE[(rej, wd, st)]
        return QUESTION_TABLE[spec.qform](refund, decider)

    def canonical(self, spec: Spec) -> dict:
        v = spec.env()
        return {"style": spec.structure["style"], "juris": v["JURIS"], "n_reject": v["N_REJ"],
                "n_withdraw": None if spec.structure.get("rule") == "nowd" else v["N_WD"],
                "rule": spec.structure.get("rule", "std"), "store": v["STORE"], "policy": v["POLICY"], "p_days": v.get("P_DAYS"),
                "order_id": v["ORDER_ID"], "customer": v["CUSTOMER"], "item": v["ITEM"], "goods": v["GOODS"],
                "seal": v.get("SEAL"), "handover": v["HANDOVER"], "reason": v["REASON"],
                "ordered": v["ORDER_DATE"].isoformat(), "delivered": v["DELIVERY_DATE"].isoformat(),
                "possession": v["POSSESSION_DATE"].isoformat(), "requested": v["REQUEST_DATE"].isoformat(),
                "days_order": v.get("D_ORDER"), "days_delivery": v.get("D_DELIV"),
                "days_possession": v.get("D_POSS"), "qform": spec.qform}

    def canonical_for(self, spec: Spec, author_mode: str) -> dict:
        """Mode F: the customer's name lives only in the free-form message, so G3-H checks it, not the parser."""
        c = self.canonical(spec)
        return c if author_mode == "T" else {k: x for k, x in c.items() if k != "customer"}

    def extract_view(self, spec: Spec) -> dict:
        c = self.canonical(spec)
        return {"customer": c["customer"], "item": c["item"], "store": c["store"]}

    # G3-H item field (iteration 2): states whether a leading article is part of the value. G0 v2 section 4 item 2 has the mode F
    # author write "the" or "my" before ITEM, and the generator's item is the bare name, so the schema says to leave it out.
    ITEM_DESCRIBE_I2 = ("the name of the goods the person bought, as written, without any article or possessive before it "
                        "(leave out the, my, a, an)")
    ITEM_DESCRIBE = ITEM_DESCRIBE_I2                  # what extract_fields prints (pool-era rebuilds swap in the authored text)
    ITEM_DESCRIBE_AUTHORED = "the goods the person bought, as written"     # the text the pool-era G3-H task files carry

    def extract_fields(self, spec: Spec) -> list:
        from c2_kit.g3h import Field
        return [Field("customer", "name", "the person who wants to send the goods back, as written"),
                Field("item", "name", T06Plugin.ITEM_DESCRIBE),
                Field("store", "name", "the store the goods came from, as written")]

    # ------------------------------------------------------------------------------------------- render
    def _pick_skin(self, ctx, spec: Spec, key: str, held: bool):
        for reg in sorted(SKIN_REGISTERS.get(spec.sampler, ()), key=lambda r: uhash(key, "register", r)):
            try:
                return ctx.pick(FAMILY, "skin", key, register=reg, held_out=held)
            except LookupError:
                continue
        return ctx.pick(FAMILY, "skin", key, held_out=held)

    def _pick_wording(self, ctx, spec: Spec, key: str, held: bool):
        """S5 prefers held-out wordings (mixdev); training rows never use them."""
        if held:
            try:
                return ctx.pick(FAMILY, "wording", key, qform=spec.qform, held_out=True)
            except LookupError:
                pass
        return ctx.pick(FAMILY, "wording", key, qform=spec.qform)

    def render(self, spec: Spec, ctx, *, skin=None, wording=None, forms=None, attack=None):
        ctx = self.ctx_for(spec, ctx)                  # never pick a wording that breaks the polarity rule
        key = self.row_key(spec)
        held = spec.sampler in self.HELD_OUT_SAMPLERS
        skin = skin or self._pick_skin(ctx, spec, key, held)
        wording = wording or self._pick_wording(ctx, spec, key, held)
        if wording.qform != spec.qform:
            raise ContractError(f"wording {wording.skin_id} asks {wording.qform}, spec asks {spec.qform}")
        forms = dict(forms or choose_forms(spec, key))
        # The printed day counts (what the request day is: the answer's own arithmetic) are always digits. The words form
        # exists only for 0..20, so a row whose form order prefers words printed "nineteen days" for a count within 20 and
        # "27 days" beyond it: the number of numerals in a row then said how late the request was (G6 metadata view,
        # n_numbers x question form 0.54 on 3,241 yes/no rows; refund rate 0.64 at 10 numerals vs 0.36 at 13).
        for name in ("D_ORDER", "D_DELIV", "D_POSS"):
            if name in forms:
                forms[name] = "digits"
        slots = spec.all_slots()
        style, variant = spec.structure["style"], spec.structure.get("card", "full")
        container = record_container(spec.sampler, skin.register)
        narrative = skin.fill(slots, forms)
        if "\n\n" in narrative.text or narrative.text != narrative.text.strip():
            raise K.RenderError(f"skin {skin.skin_id}: a narrative is one block (no blank line, no outer space)")
        tb = TextBuilder()
        for i, block in enumerate(ORDERS[spec.sampler]):
            if i:
                tb.add("state", "\n\n")
            if block == "narrative":
                tb.add("state", narrative, skin_id=skin.skin_id)
            elif block == "record":
                head, body, escape = record_template(container, "SEAL" in spec.slots, spec.structure["counts"])
                tb.add("state", K.fill(head, slots, forms)).add("state", K.fill(body, slots, forms, escape=escape))
            else:
                tb.add("state", K.fill(NOTICE_TPL, slots, forms))
        if attack is not None:
            tb.add("state", "\n\n" + ATTACK_PREFIX).add("state", attack.fill(slots, forms), skin_id=attack.skin_id)
        # the rules (G0 v3 S12): yes/no rows print them once from row.card, choice rows from the head of the instructions
        placed = CD.place_rules(tb, K.fill(card_template(style, variant, spec.structure.get("rule", "std")), slots, forms),
                                self.QFORMS[spec.qform].qtype)
        tb.add("instructions", wording.fill(slots, forms), skin_id=wording.skin_id)
        ans = self.solve_a(spec)
        os_ = None
        if spec.qform == "ch_rule":
            # a closed set: the shown rules and "none" (abstain) in one label-blind order of the row key (a twin must show the
            # same option list: G-TW, so the display is a function of the record's coarse facts, _applicable); the
            # gold position is uniform because the gold is uniform over the display and the order never reads it.
            shown = _applicable(facts(spec))
            if ans != NONE_KEY and ans not in shown:
                raise ContractError(f"ch_rule gold {ans!r} is not among the shown options {shown}")
            os_ = build_closed(spec, ans, list(shown), self.error_models(), row_key=key,
                               render_key=OPTION_TEXT[style].__getitem__,
                               abstain=(NONE_KEY, OPTION_TEXT[style][NONE_KEY]), show_abstain=True)
        elif spec.qform in END_FORMS:
            fmt = forms["REQUEST_DATE"]
            os_ = self._end_options(spec, ans, fmt)         # k, position and sorted rank from the row's plan
            if os_ is None:
                raise K.RenderError(f"{spec.qform}: the error-model dates leave a side of the gold empty")
        return assemble_row(self, spec, tb, answer=ans, option_set=os_, skin=skin, wording=wording, forms=forms,
                            attack=attack, format_style=f"{skin.register}/{container}",
                            defs_style=CD.defs_style(placed, variant))

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
            if t is not None:
                out.append(t)
        return out + self._metamorphic(spec)

    def _partner(self, spec: Spec) -> str:
        """Same predicate, opposite polarity; syntactic pairs differ by exactly one negation cue (G0_SPEC.md S17)."""
        u = uhash(FAMILY, "complement_kind", spec.sampler, spec.seed)
        return {"yn_refund": "yn_may_refuse" if u < 0.6 else "yn_not_refund",
                "yn_owed": "yn_may_refuse" if u < 0.6 else "yn_no_right",
                "yn_double": "yn_no_right" if u < 0.5 else "yn_not_refund",
                "yn_not_refund": "yn_refund" if u < 0.7 else "yn_double",
                "yn_may_refuse": "yn_refund" if u < 0.5 else "yn_owed",
                "yn_no_right": "yn_owed" if u < 0.7 else "yn_double"}[spec.qform]

    TWIN_KINDS = ("request", "reason", "seal", "delivery", "possession", "n_rej", "n_wd", "p_days", "policy")

    def _twin(self, spec: Spec):
        """Exactly one input slot changes; the prediction comes from the edited facts (_grants / _answer), never
        from solve_a. Kinds are tried in a seeded order; within a kind, the smallest edit that changes the answer."""
        f = facts(spec)
        base = _answer(spec.qform, _grants(f), f)
        kinds = sorted(self.TWIN_KINDS, key=lambda k: uhash(FAMILY, "twin_kind", spec.sampler, spec.seed, k))
        for kind in kinds:
            for slot, new, f2 in self._edits(kind, spec, f):
                if not _generable(f2, spec.qform):
                    continue
                want = _answer(spec.qform, _grants(f2), f2)
                if want is None or want == base:
                    continue
                if spec.qform == "ch_rule" and not abstain_twin_kept(
                        f"{FAMILY}|{spec.sampler}|{spec.seed}", base, want, NONE_KEY,
                        TWIN_NONE_KEEP[len(_applicable(f)) + 1]):
                    continue
                twin = spec.with_slot(slot, new)
                if spec.qform in END_FORMS and self._end_options(self.derive(twin)) is None:
                    continue           # the twin's dates cannot fill the row's planned k and rank: the next edit
                if spec.qform == "ch_rule" and _applicable(f2) != _applicable(f):
                    continue           # a twin shows the same options as its base (G-TW): the next edit
                return RelationProposal("twin", spec=twin, changed_slot=slot, expect=want, note=f"twin {kind}")
        return None

    def _edits(self, kind: str, spec: Spec, f: Facts) -> list:
        """[(slot, new slot, edited facts)] for one edit kind, smallest edits first."""
        q = spec.qform
        end = q in END_FORMS

        def by_distance(cands, cur):
            return sorted({c for c in cands if c != cur}, key=lambda c: (abs((c - cur).days), c))

        if kind == "request":
            if end:
                return []
            cands = {f.requested - TD(days=1), f.requested + TD(days=1)}
            ends = [(f.delivered, f.n_rej), (f.possession, f.n_wd)]
            if f.p is not None:
                ends.append((getattr(f, NOTICE_SCOPE[f.policy][1]), f.p))
            for anchor, n in ends:
                cands |= {anchor + TD(days=n), anchor + TD(days=n + 1)}
            return [("REQUEST_DATE", S.date_slot(c), replace(f, requested=c))
                    for c in by_distance(cands, f.requested) if c >= f.possession]
        if kind == "reason":
            if end:
                return []
            new = "mind" if f.reason == "faulty" else "faulty"
            return [("REASON", S.category_slot(new, REASON_SET), replace(f, reason=new))]
        if kind == "seal":
            if end or f.goods != "hygiene":
                return []
            new = "opened" if f.seal == "intact" else "intact"
            return [("SEAL", S.category_slot(new, SEAL_SET), replace(f, seal=new))]
        if kind == "delivery":
            if f.handover == "direct" or q == "ch_end_withdraw":
                return []
            cands = {f.requested - TD(days=f.n_rej), f.requested - TD(days=f.n_rej + 1),
                     f.delivered - TD(days=1), f.delivered + TD(days=1)}
            if f.policy == "pol.t06.any_delivery":
                cands |= {f.requested - TD(days=f.p), f.requested - TD(days=f.p + 1)}
            return [("DELIVERY_DATE", S.date_slot(c), replace(f, delivered=c))
                    for c in by_distance(cands, f.delivered)]
        if kind == "possession":
            if f.handover == "direct" or q == "ch_end_reject":
                return []
            cands = {f.requested - TD(days=f.n_wd), f.requested - TD(days=f.n_wd + 1),
                     f.possession - TD(days=1), f.possession + TD(days=1)}
            return [("POSSESSION_DATE", S.date_slot(c), replace(f, possession=c))
                    for c in by_distance(cands, f.possession)]
        if kind in ("n_rej", "n_wd"):
            if (kind == "n_rej" and q == "ch_end_withdraw") or (kind == "n_wd" and q == "ch_end_reject"):
                return []
            cur = f.n_rej if kind == "n_rej" else f.n_wd
            d = (f.requested - (f.delivered if kind == "n_rej" else f.possession)).days
            pool = set(N_REJ + N_REJ_HELD if kind == "n_rej" else N_WD + N_WD_HELD) | {d, d - 1}
            vals = sorted((x for x in pool if 3 <= x <= 60 and x != cur), key=lambda x: (abs(x - cur), x))
            slot = "N_REJ" if kind == "n_rej" else "N_WD"
            return [(slot, S.count_slot(x, DAYS), replace(f, **{kind: x})) for x in vals]
        if kind == "p_days":
            if f.p is None or end:
                return []
            d = _notice_count(f)
            vals = sorted((x for x in set(P_SETS[f.policy]) | {d, d - 1} if 1 <= x <= 120 and x != f.p),
                          key=lambda x: (abs(x - f.p), x))
            return [("P_DAYS", S.count_slot(x, DAYS), replace(f, p=x)) for x in vals]
        if kind == "policy":
            if f.p is None or end:
                return []
            return [("POLICY", self._policy_clause(sem, None), replace(f, policy=sem))
                    for sem in WINDOWED if sem != f.policy]
        raise ContractError(f"twin kind {kind}")

    def _metamorphic(self, spec: Spec) -> list:
        """G4 (checked, never emitted): names, the jurisdiction, a common date shift and the wording of a
        no-promise notice never matter."""
        v = spec.env()
        f = facts(spec)
        key = (FAMILY, "g4", spec.sampler, spec.seed)

        def other(pool, cur):
            return min((x for x in pool if x != cur), key=lambda x: uhash(*key, x))

        out = [RelationProposal("metamorphic", spec=spec.with_slot("CUSTOMER", S.name_slot(other(CUSTOMERS,
                                v["CUSTOMER"]))), expect="same", note="rename the customer"),
               RelationProposal("metamorphic", spec=spec.with_slot("ITEM", S.name_slot(other(ITEMS[f.goods],
                                v["ITEM"]))), expect="same", note="another item of the same type of goods"),
               RelationProposal("metamorphic", spec=spec.with_slot("STORE", S.name_slot(other(STORES, v["STORE"]))),
                                expect="same", note="rename the store"),
               RelationProposal("metamorphic", spec=spec.with_slot("JURIS", S.name_slot(other(
                   JURIS_HELD if spec.sampler in self.HELD_OUT_SAMPLERS else JURIS, v["JURIS"]))), expect="same",
                   note="rename the jurisdiction")]
        week = TD(days=7)
        shifted = spec.replace(slots={**spec.slots, **{k: S.date_slot(v[k] + week) for k in (
            "ORDER_DATE", "DELIVERY_DATE", "POSSESSION_DATE", "REQUEST_DATE")}})
        exp = "same"
        if spec.qform in END_FORMS:
            exp = (dt.date.fromisoformat(_answer(spec.qform, frozenset(), f)) + week).isoformat()
        out.append(RelationProposal("metamorphic", spec=shifted, expect=exp, note="shift every date by seven days"))
        if f.policy in NO_PROMISE:
            sem = other(("pol.t06.final", "pol.t06.credit"), f.policy)
            out.append(RelationProposal("metamorphic", spec=spec.with_slot("POLICY", self._policy_clause(sem, None)),
                                        expect="same", note="another no-promise notice"))
        return out + self._rule_relations(spec)

    # G4 rate per base spec (label-blind hash); only units whose gold really flips are proposed, so the achieved share is
    # lower (measured in pilot_i2/FIX_I2_NOTES.md). Never emitted: checked by solver A, solver B and every row gate.
    SWAP_RATE, DELETE_RATE, NONCE_RATE = 0.55, 0.60, 0.10
    NONCE_SYL = ("vor", "qui", "zen", "dar", "mel", "tro", "bax", "lun", "fe", "ky", "ro", "sul")

    def _nonce(self, spec: Spec, what: str, lower: bool = False) -> str:
        syl = [min(self.NONCE_SYL, key=lambda s, i=i: uhash(FAMILY, "nonce", spec.sampler, spec.seed, what, i, s))
               for i in range(3)]
        w = "".join(syl)
        return w if lower else w.capitalize()

    def _rule_relations(self, spec: Spec) -> list:
        """G4 relations the family's set lacked (FINAL_PLAN S2 item 5; metamorphic: checked, never emitted):
        rule-swap (same facts, the notice rule flipped, the gold flips), rule-deleted (the withdrawal rule removed: a right
        the rules do not state does not exist; the gold becomes no refund / the option "none") and nonce vocabulary (the
        customer, store, item and jurisdiction names replaced by invented words; the rules and the gold stay)."""
        out = []
        if spec.structure.get("rule", "std") != "std":
            return out
        f = facts(spec)
        if spec.qform not in END_FORMS:
            base = _answer(spec.qform, _grants(f), f)
            for mode, rate, kw, note in (
                    ("swap", self.SWAP_RATE, dict(statute=False), "rule swap: the notice replaces the statute"),
                    ("nowd", self.DELETE_RATE, dict(no_withdraw=True), "rule deleted: no withdrawal rule")):
                want = _answer(spec.qform, _grants(f, **kw), f)
                if (want is not None and want != base
                        and uhash(FAMILY, "rule_" + mode, spec.sampler, spec.seed) < rate):
                    out.append(RelationProposal("metamorphic", spec=spec.replace(structure={**spec.structure, "rule": mode}),
                                                expect=want, note=note))
        if uhash(FAMILY, "nonce", spec.sampler, spec.seed) < self.NONCE_RATE:
            s2 = (spec.with_slot("CUSTOMER", S.name_slot(self._nonce(spec, "c")))
                  .with_slot("STORE", S.name_slot(self._nonce(spec, "s") + " Mart"))
                  .with_slot("ITEM", S.name_slot(self._nonce(spec, "i", True)))
                  .with_slot("JURIS", S.name_slot(self._nonce(spec, "j"))))
            out.append(RelationProposal("metamorphic", spec=s2, expect="same", note="nonce names for customer, store, item, jurisdiction"))
        return out

    # ------------------------------------------------------------------------------------------- error models
    def error_models(self) -> dict:
        def run(rule_kw=None, end_fn=None, rule_fn=None):
            def fn(spec):
                f = facts(spec)
                if spec.qform == "ch_rule":
                    if rule_fn is not None:
                        return rule_fn(f)
                    return None if rule_kw is None else _answer("ch_rule", _grants(f, **rule_kw), f)
                if spec.qform in END_FORMS and end_fn is not None:
                    ans = end_fn(spec.qform, f)
                    # a model whose date is one the record prints gives no output (an option equal to a printed date is a
                    # verbatim cue for G6 / G7; see _end_options)
                    return None if ans in {d.isoformat() for d in (f.ordered, f.delivered, f.possession, f.requested)} else ans
                return None
            return fn

        def end_date(anchor_of, n_of):
            def fn(qform, f):
                anchor, n = anchor_of(qform, f), n_of(qform, f)
                return None if anchor is None or n is None else (anchor + TD(days=n)).isoformat()
            return fn

        def own_anchor(qform, f):
            return f.delivered if qform == "ch_end_reject" else f.possession

        def own_n(qform, f):
            return f.n_rej if qform == "ch_end_reject" else f.n_wd

        def other_n(qform, f):
            n = f.n_wd if qform == "ch_end_reject" else f.n_rej
            return None if n == own_n(qform, f) else n

        def swapped_anchor(qform, f):
            if f.possession == f.delivered:
                return None
            return f.possession if qform == "ch_end_reject" else f.delivered

        def weekdays(qform, f):
            d, n = own_anchor(qform, f), own_n(qform, f)
            while n > 0:
                d += TD(days=1)
                n -= d.weekday() < 5
            return d.isoformat()

        def notice_n(qform, f):
            return None if f.p is None or f.p == own_n(qform, f) else f.p

        fns = {
            "t06_sign_wins": run(dict(statute=False)),
            "t06_ignore_notice": run(dict(notice=False)),
            "t06_order_date_anchor": run(dict(rej_anchor="ordered", wd_anchor="ordered"),
                                         end_date(lambda q, f: f.ordered, own_n)),
            "t06_delivery_for_possession": run(dict(wd_anchor="delivered"), end_date(
                lambda q, f: swapped_anchor(q, f) if q == "ch_end_withdraw" else None, own_n)),
            "t06_possession_for_delivery": run(dict(rej_anchor="possession"), end_date(
                lambda q, f: swapped_anchor(q, f) if q == "ch_end_reject" else None, own_n)),
            "count_day0": run(dict(shift=-1), end_date(own_anchor, lambda q, f: own_n(q, f) - 1)),
            "off_by_one_late": run(dict(shift=1), end_date(own_anchor, lambda q, f: own_n(q, f) + 1)),
            "t06_absolute_exception": run(dict(absolute=True)),
            "ignore_exception": run(dict(ignore_exc=True)),
            "t06_swap_periods": run(dict(swap=True), end_date(own_anchor, other_n)),
            "t06_notice_from_delivery": run(dict(notice_anchor="delivered")),
            "t06_notice_any_reason": run(dict(notice_any_reason=True)),
            "t06_reason_picks_rule": run(rule_fn=lambda f: "reject" if f.reason == "faulty" else "withdraw"),
            "t06_other_right": run(rule_fn=lambda f: "withdraw" if f.reason == "faulty" else "reject"),
            "t06_sign_decides": run(rule_fn=lambda f: "store"),
            "t06_both_ends_early": run(end_fn=end_date(own_anchor, lambda q, f: own_n(q, f) - 2)),
            "t06_both_ends_late": run(end_fn=end_date(own_anchor, lambda q, f: own_n(q, f) + 2)),
            "t06_business_days": run(end_fn=weekdays),
            "t06_notice_period": run(end_fn=end_date(own_anchor, notice_n)),
        }
        return {k: error_model(k, fn) for k, fn in fns.items()}
