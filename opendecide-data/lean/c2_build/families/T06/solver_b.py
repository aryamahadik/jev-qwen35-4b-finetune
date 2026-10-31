"""families/T06/solver_b.py: T06 solver B, written from G0_SPEC_v3.md (not from plugin.py).

parse(row, ctx) reads the RENDERED row back into the canonical facts with this module's own readers:
  - the rules (cards.split_rules: row.card on yes/no rows, the instructions before their last blank line on choice
    rows): this module's own copy of the statute cards of G0_SPEC_v3.md section 2 (act, code and charter in full /
    compact / short, regulation in full), read with skin.match_template (jurisdiction as a name, both periods as day
    counts); exactly one card must match;
  - the state blocks (separated by blank lines) by their fixed openings: the order record ("Order record ..."), the
    store notice ('... posted this notice at its checkout and on its website: "..."'), an optional message line
    ("Message added to the case: ", never a fact) and the customer's message (the one block left);
  - the order record in its container (bullet lines, markdown table, or JSON after "Order record (JSON):"), through
    this module's own label and key tables; dates by slots.parse in any date form, day counts as counts of days;
  - the notice text through the lexicon registry (admitted forms only: G-LEX vouches for each form's meaning);
  - the customer's message through skin.parse_skin (Mode T); a Mode F message is left to G3-H;
  - the question through its wording template; on choice rows every option text back to its key.
Every fact that appears twice (store in the record, the notice and the message; item in the record and the message)
must read the same.
solve_b(view) decides by day bitmaps: each period is the list of its calendar days, built day by day from its anchor
(brute.window_days), and a right holds when the request date is one of those days; every printed day count must equal
the number of steps of a day-by-day walk from its anchor to the request date. A separate exclusion evaluator decides
whether the withdrawal right is excluded; its own notice-meaning table says which reasons a notice covers and from
which date its period runs; its own question table maps the granting rules to the answer. Imports no solver-A code
(plugin.check_independence).
"""
from __future__ import annotations

import datetime as dt
import json
import re

from c2_kit import brute
from c2_kit import cards as CD
from c2_kit import skin as K
from c2_kit import slots as S

DAY_PARAMS = (("unit", ("day", "days")),)
DAYS = ("count", DAY_PARAMS)
CARD_SCHEMA = {"JURIS": ("name", ()), "N_REJ": DAYS, "N_WD": DAYS}
NARR_SCHEMA = {"CUSTOMER": ("name", ()), "ITEM": ("name", ()), "STORE": ("name", ())}
CLOSED = ("The rules, the posted notice and the order record are complete; no other fact or message changes the "
          "case.")
# Statute cards (G0_SPEC_v3.md section 2), this module's own copy: one text per (style, variant); each card is its
# lines joined by newlines. The closed-world sentence follows on the next line (CLOSED).
CARDS = {
    ("act", "full"): (
        "Consumer Sales Act of {JURIS} (excerpt)\n"
        "Section I (counting days). A right is used on the day the buyer asks for it. A period in this "
        "Act or in a store notice runs in calendar days from an event: the event's day is day zero, the "
        "next day is day one, and the period includes its last day.\n"
        "Section II (faulty goods). A buyer may reject faulty goods and get a full refund within {N_REJ} "
        "from the delivery date.\n"
        "Section III (withdrawal). A buyer may withdraw from a purchase for any reason and get a full "
        "refund within {N_WD} from the day the buyer took possession of the goods. Section III does not "
        "cover goods made to the buyer's specification, perishable goods, or sealed hygiene goods whose "
        "seal was broken after delivery; these exclusions do not limit Section II.\n"
        "Section IV (store notices). A store notice cannot remove or shorten these rights. A store may "
        "promise more, and a full refund its posted notice promises is owed."
    ),
    ("act", "compact"): (
        "Consumer Sales Act of {JURIS} (excerpt)\n"
        "Section I (counting days). A right is used on the day the buyer asks for it. Periods in this Act "
        "or in a store notice run in calendar days from an event: the event's day is day zero, and the "
        "last day counts.\n"
        "Section II (faulty goods). A buyer may reject faulty goods and get a full refund within {N_REJ} "
        "of delivery.\n"
        "Section III (withdrawal). A buyer may withdraw for any reason and get a full refund within "
        "{N_WD} from the day the buyer took possession. Section III does not cover goods made to the "
        "buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after "
        "delivery; these exclusions do not limit Section II.\n"
        "Section IV (store notices). A store notice cannot remove or shorten these rights. A store may "
        "promise more, and a full refund its posted notice promises is owed."
    ),
    ("act", "short"): (
        "Consumer Sales Act of {JURIS} (excerpt)\n"
        "Section I. A right is used on the day the buyer asks for it. Periods in this Act or in a store "
        "notice are calendar days from an event: the event's day is day zero, the last day counts.\n"
        "Section II. A buyer may reject faulty goods for a full refund within {N_REJ} of delivery.\n"
        "Section III. A buyer may withdraw for any reason for a full refund within {N_WD} of taking "
        "possession. It does not cover goods made to the buyer's specification, perishable goods, or "
        "sealed hygiene goods whose seal was broken after delivery; these exclusions do not limit Section "
        "II.\n"
        "Section IV. A store notice cannot remove or shorten these rights. A store may promise more; a "
        "full refund its posted notice promises is owed."
    ),
    ("code", "full"): (
        "Civil Code of {JURIS}, consumer sales, Article K (extract)\n"
        "(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's "
        "notice counts calendar days from an event: the event's day is day zero, the next day is day one, "
        "and the final day of the limit still counts.\n"
        "(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts {N_REJ}, "
        "counted from the date of delivery.\n"
        "(c) A buyer may withdraw from a purchase for any reason and be refunded in full; this right "
        "lasts {N_WD}, counted from the date the buyer took possession of the goods.\n"
        "(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed "
        "hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.\n"
        "(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a "
        "full refund its posted notice promises is owed."
    ),
    ("code", "compact"): (
        "Civil Code of {JURIS}, consumer sales, Article K (extract)\n"
        "(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's "
        "notice counts calendar days from an event: the event's day is day zero, and the final day still "
        "counts.\n"
        "(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts {N_REJ} "
        "from the date of delivery.\n"
        "(c) A buyer may withdraw for any reason and be refunded in full; this right lasts {N_WD} from "
        "the date the buyer took possession.\n"
        "(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed "
        "hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.\n"
        "(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a "
        "full refund its posted notice promises is owed."
    ),
    ("code", "short"): (
        "Civil Code of {JURIS}, consumer sales, Article K (extract)\n"
        "(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's "
        "notice counts calendar days from an event: the event's day is day zero, the final day still "
        "counts.\n"
        "(b) A buyer may reject faulty goods and be refunded in full; the right lasts {N_REJ} from "
        "delivery.\n"
        "(c) A buyer may withdraw for any reason and be refunded in full; the right lasts {N_WD} from "
        "taking possession.\n"
        "(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed "
        "hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.\n"
        "(e) A seller's notice cannot remove or shorten these rights. A seller may promise more; a full "
        "refund its posted notice promises is owed."
    ),
    ("charter", "full"): (
        "Buyer's Rights Charter of {JURIS} (summary every store must display)\n"
        "- Counting days: you use a right on the day you ask for it. Periods count calendar days: a "
        "period's event day is day zero, the next day is day one, and the last day of the period still "
        "counts. Store notices count days the same way.\n"
        "- Faulty-goods rule: you can reject faulty goods and get a full refund within {N_REJ} from the "
        "day they were delivered.\n"
        "- Cooling-off rule: for any reason, you can withdraw from a purchase and get a full refund "
        "within {N_WD} from the day you took possession of the goods. It does not cover goods made to "
        "your specification, perishable goods, or sealed hygiene goods whose seal was broken after "
        "delivery. These exclusions never limit the faulty-goods rule.\n"
        "- Store notices: a store notice cannot take away or shorten these rights. A store may promise "
        "more, and a full refund its posted notice promises is owed."
    ),
    ("charter", "compact"): (
        "Buyer's Rights Charter of {JURIS} (summary every store must display)\n"
        "- Counting days: you use a right on the day you ask for it. Periods count calendar days: a "
        "period's event day is day zero, and the last day still counts. Store notices count days the same "
        "way.\n"
        "- Faulty-goods rule: you can reject faulty goods and get a full refund within {N_REJ} from the "
        "day they were delivered.\n"
        "- Cooling-off rule: for any reason, you can withdraw and get a full refund within {N_WD} from "
        "the day you took possession. It does not cover goods made to your specification, perishable "
        "goods, or sealed hygiene goods whose seal was broken after delivery. These exclusions never "
        "limit the faulty-goods rule.\n"
        "- Store notices: a store notice cannot take away or shorten these rights. A store may promise "
        "more, and a full refund its posted notice promises is owed."
    ),
    ("charter", "short"): (
        "Buyer's Rights Charter of {JURIS} (summary every store must display)\n"
        "- Counting days: you use a right on the day you ask for it. Periods are calendar days: the event "
        "day is day zero, the last day still counts. Store notices count the same way.\n"
        "- Faulty-goods rule: you can reject faulty goods for a full refund within {N_REJ} of delivery.\n"
        "- Cooling-off rule: for any reason, you can withdraw for a full refund within {N_WD} of taking "
        "possession. It does not cover goods made to your specification, perishable goods, or sealed "
        "hygiene goods whose seal was broken after delivery; these exclusions never limit the "
        "faulty-goods rule.\n"
        "- Store notices: a store notice cannot take away or shorten these rights. A store may promise "
        "more; a full refund its posted notice promises is owed."
    ),
    ("regulation", "full"): (
        "Distance Sales Regulations of {JURIS}, Part R (extract)\n"
        "Reg. A (periods). A right is exercised on the day the consumer requests it. A period counts "
        "whole calendar days from its event: the event day is day zero, the next day is day one, and the "
        "final day is included. A trader's notice counts days the same way.\n"
        "Reg. B (rejection). A consumer may reject faulty goods and is due a full refund if the rejection "
        "is made within {N_REJ} of delivery.\n"
        "Reg. C (cancellation). A consumer may cancel a purchase for any reason and is due a full refund "
        "if the cancellation is made within {N_WD} of taking possession of the goods. Reg. C does not "
        "apply to goods made to the buyer's specification, perishable goods, or sealed hygiene goods "
        "whose seal was broken after delivery. Reg. B is not limited by these exclusions.\n"
        "Reg. D (notices). A trader's notice cannot exclude or shorten these rights. A trader may promise "
        "more, and a full refund its posted notice promises is due."
    ),
}
OPTION_KEY = {
    "act": {"Section II (faulty goods)": "reject", "Section III (withdrawal)": "withdraw",
            "The store's posted notice": "store", "None of them: no full refund is owed": "none"},
    "code": {"Article K(b) (faulty goods)": "reject", "Article K(c) (withdrawal)": "withdraw",
             "The seller's posted notice": "store", "None of them: no full refund is owed": "none"},
    "charter": {"The faulty-goods rule": "reject", "The cooling-off rule": "withdraw",
                "The store's posted notice": "store", "None of them: no full refund is owed": "none"},
    "regulation": {"Reg. B (rejection)": "reject", "Reg. C (cancellation)": "withdraw",
                   "The trader's posted notice": "store", "None of them: no full refund is due": "none"},
}
# The order record: line / table label -> view field, JSON key -> view field (G0_SPEC.md S13).
LABEL_FIELD = {"item": "item", "type of goods": "goods", "seal": "seal", "handover": "handover",
               "ordered on (the purchase date)": "ordered", "delivered on": "delivered",
               "buyer took possession on": "possession", "return requested on": "requested",
               "reason for the return": "reason", "days from the purchase date to the request": "days_order",
               "days from delivery to the request": "days_delivery",
               "days from possession to the request": "days_possession"}
JSON_FIELD = {"order_id": "order_id", "store": "store", "item": "item", "goods_type": "goods", "seal": "seal",
              "handover": "handover", "purchase_date": "ordered", "delivered_on": "delivered",
              "possession_on": "possession", "return_requested_on": "requested", "reason": "reason",
              "days_purchase_to_request": "days_order", "days_delivery_to_request": "days_delivery",
              "days_possession_to_request": "days_possession"}
GOODS_OF = {"standard goods": "standard", "made to the buyer's specification": "custom",
            "perishable goods": "perishable", "sealed hygiene goods": "hygiene"}
SEAL_OF = {"intact": "intact", "broken after delivery": "opened"}
REASON_OF = {"faulty": "faulty", "change of mind": "mind"}
HANDOVER_OF = {"handed to the buyer at delivery": "direct",
               "delivered to a parcel locker and collected by the buyer later": "locker",
               "delivered to a neighbour and collected by the buyer later": "neighbour"}
DATE_FIELDS = ("ordered", "delivered", "possession", "requested")
COUNT_FIELDS = ("days_order", "days_delivery", "days_possession")
COUNT_ANCHOR = {"days_order": "ordered", "days_delivery": "delivered", "days_possession": "possession"}
REQUIRED = ("item", "goods", "handover", "ordered", "delivered", "possession", "requested", "reason")
RECORD_HEAD = re.compile(r"Order record (?:(?P<id>[A-Za-z0-9][A-Za-z0-9_.:/#-]*) from (?P<store>[^\n]+)|\(JSON\)):")
NOTICE_RE = re.compile(r'(?P<store>[^\n"]+) posted this notice at its checkout and on its website: '
                       r'"(?P<text>[^"\n]+)"')
MESSAGE_PREFIX = "Message added to the case: "
# Notice meaning (G0_SPEC.md S9): which reasons the store's promise covers and the record date its period runs from.
NOTICE_MEANING = {"pol.t06.final": None, "pol.t06.credit": None, "pol.t06.nocustom": None,
                  "pol.t06.faulty_order": (frozenset({"faulty"}), "ordered"),
                  "pol.t06.mind_order": (frozenset({"mind"}), "ordered"),
                  "pol.t06.any_order": (frozenset({"faulty", "mind"}), "ordered"),
                  "pol.t06.any_delivery": (frozenset({"faulty", "mind"}), "delivered")}
# Exclusions from the withdrawal right (G0_SPEC.md S7): always, or only when the seal was broken after delivery.
EXCLUDED_ALWAYS = frozenset({"custom", "perishable"})
EXCLUDED_IF_OPENED = frozenset({"hygiene"})
CHOICE_FORMS = ("ch_rule", "ch_end_reject", "ch_end_withdraw")


class ParseError(ValueError):
    pass


def _several(granting: list):
    raise ParseError(f"two rules give the refund ({granting}): no single deciding rule")


ANSWER = {
    "yn_refund": lambda granting: 1 if granting else 0,
    "yn_owed": lambda granting: 1 if granting else 0,
    "yn_double": lambda granting: 1 if granting else 0,
    "yn_not_refund": lambda granting: 0 if granting else 1,
    "yn_may_refuse": lambda granting: 0 if granting else 1,
    "yn_no_right": lambda granting: 0 if granting else 1,
    "ch_rule": lambda granting: "none" if not granting else (granting[0] if len(granting) == 1
                                                             else _several(granting)),
}


# ------------------------------------------------------------------------------------------------ readers
# G4 partner cards (G0 v4 S22, never an emitted row): the notice rule flipped (the posted notice replaces the statute) or the
# withdrawal rule deleted. This module's own copy of the changed line / the dropped line numbers (header = line 0).
NOTICE_ONLY = {
    "act": "Section IV (store notices). A store notice replaces these rights: the buyer gets a full refund only if the "
           "store's posted notice promises one.",
    "code": "(e) A seller's notice replaces these rights: the buyer gets a full refund only if the seller's posted "
            "notice promises one.",
    "charter": "- Store notices: a store notice replaces these rights: you get a full refund only if the store's posted "
               "notice promises one.",
    "regulation": "Reg. D (notices). A trader's notice replaces these rights: the consumer is due a full refund only if "
                  "the trader's posted notice promises one."}
DROPPED = {"act": (3,), "code": (3, 4), "charter": (3,), "regulation": (3,)}


def _read_card(text: str) -> tuple:
    """(statute style, slot values, rule mode) of the rules block: exactly one (style, variant, mode) template must match;
    mode is std on every emitted row, swap / nowd on a G4 partner."""
    hits = []
    for (style, _variant), tpl in CARDS.items():
        lines = tpl.split("\n")
        for mode, body, schema in (
                ("std", lines, CARD_SCHEMA),
                ("swap", lines[:-1] + [NOTICE_ONLY[style]], CARD_SCHEMA),
                ("nowd", [ln for i, ln in enumerate(lines) if i not in DROPPED[style]],
                 {k: v for k, v in CARD_SCHEMA.items() if k != "N_WD"})):
            try:
                hits.append((style, K.match_template("\n".join(body) + "\n" + CLOSED, text, schema), mode))
            except K.TemplateMismatch:
                continue
    if len(hits) != 1:
        raise ParseError(f"the card matches {len(hits)} statute cards")
    return hits[0]


def _split_blocks(state: str) -> tuple:
    record, notice, message, other = [], [], [], []
    for b in state.split("\n\n"):
        first = b.split("\n", 1)[0]
        if RECORD_HEAD.fullmatch(first):
            record.append(b)
        elif NOTICE_RE.fullmatch(b):
            notice.append(b)
        elif b.startswith(MESSAGE_PREFIX):
            message.append(b)
        else:
            other.append(b)
    if len(record) != 1 or len(notice) != 1 or len(message) > 1 or len(other) != 1:
        raise ParseError(f"state blocks: {len(record)} record, {len(notice)} notice, {len(message)} message, "
                         f"{len(other)} other (want 1 / 1 / 0-1 / 1)")
    return record[0], notice[0], other[0]


def _pairs_lines(body: list) -> list:
    out = []
    for ln in body:
        if not ln.startswith("- ") or ": " not in ln:
            raise ParseError(f"record line expected: {ln!r}")
        out.append(tuple(ln[2:].split(": ", 1)))
    return out


def _pairs_table(body: list) -> list:
    if len(body) < 3 or body[0] != "| field | value |" or body[1] != "| --- | --- |":
        raise ParseError("record table needs its header and rule")
    out = []
    for ln in body[2:]:
        if not (ln.startswith("| ") and ln.endswith(" |")) or ln[2:-2].count(" | ") != 1:
            raise ParseError(f"record table row expected: {ln!r}")
        out.append(tuple(ln[2:-2].split(" | ")))
    return out


def _read_record(block: str) -> dict:
    lines = block.split("\n")
    head = RECORD_HEAD.fullmatch(lines[0])
    raw: dict = {}
    if head["id"] is None:                                       # JSON container
        obj = json.loads("\n".join(lines[1:]))
        if not isinstance(obj, dict) or any(k not in JSON_FIELD for k in obj):
            raise ParseError("JSON record: unknown keys")
        if any(not isinstance(v, str) for v in obj.values()):
            raise ParseError("JSON record values are strings")
        raw = {JSON_FIELD[k]: v for k, v in obj.items()}
    else:
        body = lines[1:]
        pairs = _pairs_table(body) if body and body[0].startswith("| ") else _pairs_lines(body)
        for label, value in pairs:
            if label not in LABEL_FIELD or LABEL_FIELD[label] in raw:
                raise ParseError(f"record label {label!r} unknown or repeated")
            raw[LABEL_FIELD[label]] = value
        raw["order_id"], raw["store"] = head["id"], head["store"]
    missing = [k for k in REQUIRED + ("order_id", "store") if k not in raw]
    if missing:
        raise ParseError(f"record lacks {missing}")
    rec = {"order_id": S.parse("id", raw["order_id"]), "store": S.parse("name", raw["store"]),
           "item": S.parse("name", raw["item"])}
    for fld, table in (("goods", GOODS_OF), ("handover", HANDOVER_OF), ("reason", REASON_OF)):
        if raw[fld] not in table:
            raise ParseError(f"{fld} {raw[fld]!r} is not a G0 value")
        rec[fld] = table[raw[fld]]
    if (rec["goods"] == "hygiene") != ("seal" in raw):
        raise ParseError("a seal line belongs to sealed hygiene goods and only to them")
    rec["seal"] = SEAL_OF[raw["seal"]] if "seal" in raw else None
    for fld in DATE_FIELDS:
        rec[fld] = S.parse("date", raw[fld]).isoformat()
    shown = [k for k in COUNT_FIELDS if k in raw]
    if shown and len(shown) != len(COUNT_FIELDS):
        raise ParseError("the day counts are printed all together or not at all")
    for fld in COUNT_FIELDS:
        rec[fld] = S.parse("count", raw[fld], DAY_PARAMS) if fld in raw else None
    return rec


def _read_notice(block: str, ctx) -> tuple:
    m = NOTICE_RE.fullmatch(block)
    sem, _form, vals = ctx.lexicon.parse_exact(m["text"], {"P": DAYS}, admitted_only=True)
    if sem not in NOTICE_MEANING:
        raise ParseError(f"notice meaning {sem} is not a G0 notice")
    p = vals.get("P")
    if (NOTICE_MEANING[sem] is None) != (p is None):
        raise ParseError("a notice with a promise states its days, and only such a notice does")
    return S.parse("name", m["store"]), sem, p


def parse(row: dict, ctx) -> dict:
    card_text, question = CD.split_rules(row)         # yes/no rows: row.card + the question; choice rows: head + question
    if not card_text or not question:
        raise ParseError("the rules and the question are not separated")
    style, card, rule = _read_card(card_text)
    rec_block, notice_block, narrative = _split_blocks(row["state"])
    rec = _read_record(rec_block)
    store, sem, p = _read_notice(notice_block, ctx)
    if store != rec["store"]:
        raise ParseError("the notice and the record name different stores")
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    told = {}
    if skin.author_mode == "T":
        told = K.parse_skin(skin, narrative, NARR_SCHEMA)
        if set(told) != set(NARR_SCHEMA):
            raise ParseError(f"the customer's message carries {sorted(told)}")
        if told["ITEM"] != rec["item"] or told["STORE"] != rec["store"]:
            raise ParseError("the message and the record disagree on the item or the store")
    wording = ctx.skin(row["meta"]["wording_id"])
    K.match_template(wording.text, question, {})
    qform = wording.qform
    if (row["qtype"] == "choice") != (qform in CHOICE_FORMS):
        raise ParseError("question form and row type disagree")
    view = {"style": style, "juris": card["JURIS"], "n_reject": card["N_REJ"], "n_withdraw": card.get("N_WD"), "rule": rule,
            "store": rec["store"], "policy": sem, "p_days": p, "order_id": rec["order_id"], "item": rec["item"],
            "goods": rec["goods"], "seal": rec["seal"], "handover": rec["handover"], "reason": rec["reason"],
            "ordered": rec["ordered"], "delivered": rec["delivered"], "possession": rec["possession"],
            "requested": rec["requested"], "days_order": rec["days_order"], "days_delivery": rec["days_delivery"],
            "days_possession": rec["days_possession"], "qform": qform}
    if skin.author_mode == "T":
        view["customer"] = told["CUSTOMER"]
    if row["qtype"] == "choice":
        view["options"] = [_option_key(qform, style, t) for t in row["options"]]
    return view


def _option_key(qform: str, style: str, text: str):
    if qform == "ch_rule":
        if text not in OPTION_KEY[style]:
            raise ParseError(f"unknown rule option {text!r}")
        return OPTION_KEY[style][text]
    return S.parse("date", text).isoformat()


# ------------------------------------------------------------------------------------------------ solver B
def _withdrawal_excluded(goods: str, seal) -> bool:
    """The separate exclusion evaluator (G0_SPEC.md S7)."""
    if goods in EXCLUDED_ALWAYS:
        return True
    if goods in EXCLUDED_IF_OPENED:
        if seal not in ("intact", "opened"):
            raise ParseError("sealed hygiene goods need a seal state")
        return seal == "opened"
    return False


def solve_b(view: dict):
    day = {k: dt.date.fromisoformat(view[k]) for k in DATE_FIELDS}
    req = day["requested"]
    if not day["ordered"] < day["delivered"] <= day["possession"] <= req:
        raise ParseError("record dates out of order")
    for fld in COUNT_FIELDS:
        if view[fld] is not None and len(brute.day_list(day[COUNT_ANCHOR[fld]], req)) - 1 != view[fld]:
            raise ParseError(f"the printed {fld} disagrees with a day-by-day walk")
    if view["qform"] == "ch_end_reject":
        return brute.window_days(day["delivered"], view["n_reject"])[-1].isoformat()
    if view["qform"] == "ch_end_withdraw":
        return brute.window_days(day["possession"], view["n_withdraw"])[-1].isoformat()

    def holds(anchor: str, n: int) -> bool:
        return req in set(brute.window_days(day[anchor], n))

    granting = []
    if view["rule"] != "swap" and view["reason"] == "faulty" and holds("delivered", view["n_reject"]):
        granting.append("reject")
    if (view["rule"] == "std" and not _withdrawal_excluded(view["goods"], view["seal"])
            and holds("possession", view["n_withdraw"])):
        granting.append("withdraw")
    meaning = NOTICE_MEANING[view["policy"]]
    if meaning is not None and view["reason"] in meaning[0] and holds(meaning[1], view["p_days"]):
        granting.append("store")
    return ANSWER[view["qform"]](granting)
