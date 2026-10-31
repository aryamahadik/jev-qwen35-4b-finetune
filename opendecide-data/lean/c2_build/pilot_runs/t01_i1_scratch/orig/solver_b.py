"""families/T01/solver_b.py: T01 solver B, written from G0_SPEC.md (sections 1, 1.1, 1.2), not from plugin.py.

parse(row, ctx) reads the RENDERED row back into the canonical facts:
  - the record block (the paragraph whose first line is one of the G0 1.2 headers) line by line with this module's
    own regular expressions, for every kind and both styles (list, table);
  - the rule paragraph against this module's own copy of the G0 1.1 card text; window rules and comparators through
    the lexicon registry (admitted forms only), and only the sem ids G0 allows for that kind;
  - the narrative skin (Mode T) through skin.parse_skin; Mode F narrative facts are left to G3-H;
  - the question through its wording template (its admitted meaning is the question form);
  - on choice rows, every option text back to its key (a count, integer cents, an ISO date or a cash label).
Every fact printed twice (header and narrative, record and question, window end and reference date) must read the
same, and every printed intermediate (stay lengths, window spans, day counts, the plain N-day date, the office-time
restatement) is re-derived and must agree.
solve_b(view) decides by enumeration (paradigm day_bitmap): the set of present days built day by day and counted
inside the listed window; filing and waiting periods as explicit day lists (day zero first); per-day ledgers of
purchases and of deposits / withdrawals; a calendar walk past the listed closures; cutoffs in epoch minutes
(brute.epoch_minutes). Comparators are a sign table on integer cents. Imports no solver-A code
(plugin.check_independence).
"""
from __future__ import annotations

import datetime as dt
import re

from c2_kit import brute
from c2_kit import skin as K
from c2_kit import slots as S

ONE_DAY = dt.timedelta(days=1)
CENTS = (("currency", "USD"), ("symbol", "$"))
DAYS = (("unit", ("day", "days")),)
DIR_SET = (("surfaces", (("in", ("deposit",)), ("out", ("withdrawal",)))),)
METHOD_SET = (("surfaces", (("email", ("email",)), ("hand", ("hand delivery",)), ("post", ("post",)))),)
NARRATIVE = {"PERSON": ("name", ()), "REF": ("id", ()), "TOPIC": ("name", ())}
QUESTION = {"PERSON": ("name", ()), "REF": ("id", ()), "REF_DATE": ("date", ()), "ACTION": ("name", ()),
            "PERIL": ("name", ()), "DAY": ("date", ())}
SIGN_OK = {"cmp.gt": (1,), "cmp.ge": (0, 1)}
KIND_SEMS = {"rolling": ("win.rolling_cap",), "anchor": ("win.later_anchor",), "waiting": ("win.wait_after",)}
CASH_KEYS = {"Only the deposit total": "in", "Only the withdrawal total": "out", "Both totals": "both",
             "Neither total": "neither"}
CASH_LABEL = {(True, True): "both", (True, False): "in", (False, True): "out", (False, False): "neither"}
# question table (G0 S3): kind, and for yes/no forms whether "yes" means the kind's predicate holds
QUESTIONS = {"yn_over": ("rolling", True), "yn_within": ("rolling", False), "yn_not_over": ("rolling", False),
             "ch_days": ("rolling", None), "yn_timely": ("anchor", True), "yn_late": ("anchor", False),
             "yn_fail_time": ("anchor", False), "yn_not_timely": ("anchor", False), "ch_deadline": ("anchor", None),
             "yn_covered": ("waiting", True), "yn_in_waiting": ("waiting", False),
             "yn_not_covered": ("waiting", False), "ch_first_day": ("waiting", None),
             "yn_quotes": ("purchase", True), "yn_quotes_without": ("purchase", False),
             "yn_no_quotes": ("purchase", False), "ch_total": ("purchase", None),
             "yn_cash_report": ("cash", True), "yn_cash_without": ("cash", False),
             "yn_cash_no_report": ("cash", False), "ch_cash_which": ("cash", None), "ch_due": ("addon", None),
             "yn_on_time": ("cutoff", True), "yn_late_cut": ("cutoff", False), "yn_not_on_time": ("cutoff", False),
             "ch_receipt_day": ("cutoff", None)}

# G0 1.1: the card text, copied from the spec (exact)
CW = "The listed rules and records are complete: no other rule, record or note changes the answer."
CARD = {   # G0 v2 (after the Haiku pass amb:T01)
    "rolling": "Stay rule: the person named in the record may be present on {WIN_CLAUSE}. Day counts are calendar "
               "days, and entry and exit days both count as days present. Only one {M_WIN} window is checked: the one "
               "that ends on the reference date, both ends included; its first day is printed with the record. The "
               "person is over the limit if the number of days present inside that window is more than {N_MAX}, and "
               "within the limit if it is {N_MAX} or fewer. " + CW,
    "anchor": "Filing rule: the {ACTION} must be filed {AN_CLAUSE}: the {EVA_LABEL} and the {EVB_LABEL}. Day zero is "
              "the later of those two dates, and the earlier date plays no part. Day counts are calendar days, and "
              "the final day of the period is {N_DAYS} after day zero. A filing made on any day up to and including "
              "that final day is in time; a filing after it is late. " + CW,
    "waiting": "Cover rule: a loss is covered only after {WAIT_CLAUSE}. That start date is the policy start date or, "
               "for a peril added by a rider, the rider's effective date; the same waiting period applies either way. "
               "Day counts are calendar days. The start date itself is day zero, the waiting period begins on the "
               "next day, and its final day is {W_DAYS} after the start date. A loss that happens after that final "
               "day is covered; a loss on or before it is not. " + CW,
    "purchase": "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request "
                "and every earlier purchase made inside the {M_WIN} window that ends on the request date; day counts "
                "are calendar days, and both ends of the window count. If that total is {CMP}, written quotes are "
                "required; otherwise the small-purchase path applies. " + CW,
    "cash": "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; "
            "never net one against the other, and never mix days. A cash report is required for a day if its deposit "
            "total or its withdrawal total is {CMP}, and not otherwise. " + CW,
    "addon": "Response rule: a response is due {N_DAYS} after the notice date, counted in calendar days with the "
             "notice date as day zero. If the notice was sent by post, add {K_DAYS} to that date. The date this gives "
             "is the day reached. If the day reached is a day the office is closed, the due date moves forward to the "
             "next day the office is open; otherwise the day reached is the due date. The office is open on every day "
             "except the listed closures. " + CW,
    "cutoff": "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with "
              "the office cutoff, and the due date is a date in office time; the record also gives the sending time "
              "in office time, in square brackets. Every response here is sent electronically and arrives at the "
              "instant it is sent. A response that arrives at or before the daily cutoff time counts as received that "
              "day; one that arrives after it counts as received on the next day. The cutoff is the same office clock "
              "time every day. A response is on time if it counts as received on or before the due date, and late "
              "otherwise. " + CW,
}


class ParseError(ValueError):
    pass


def _pattern(text: str) -> re.Pattern:
    """A full-match pattern for a card text: literal text escaped, each {NAME} a lazy named group (a repeated {NAME}
    must repeat the same text: a back-reference)."""
    parts, pos, seen = [], 0, set()
    for m in re.finditer(r"\{([A-Z][A-Z0-9_]*)\}", text):
        name = m.group(1).lower()
        parts.append(re.escape(text[pos:m.start()]))
        parts.append(f"(?P={name})" if name in seen else f"(?P<{name}>.+?)")
        seen.add(name)
        pos = m.end()
    parts.append(re.escape(text[pos:]))
    return re.compile("".join(parts), re.S)


CARD_RX = {k: _pattern(v) for k, v in CARD.items()}
_C = re.compile
HEADERS = (
    ("rolling", "list", _C(r"Stay record (?P<ref>\S+) for (?P<person>.+):")),
    ("rolling", "table", _C(r"Travel log (?P<ref>\S+), traveller (?P<person>.+):")),
    ("anchor", "list", _C(r"Case (?P<ref>\S+), party (?P<person>.+):")),
    ("anchor", "table", _C(r"Court notice, case (?P<ref>\S+), party (?P<person>.+):")),
    ("waiting", "list", _C(r"Policy (?P<ref>\S+), holder (?P<person>.+):")),
    ("purchase", "list", _C(r"Purchase log (?P<ref>\S+), kept by (?P<person>.+?), vendor (?P<vendor>.+):")),
    ("cash", "list", _C(r"Cash ledger (?P<ref>\S+), teller (?P<person>.+):")),
    ("notice", "list", _C(r"Notice (?P<ref>\S+) to (?P<person>.+):")),
)
STAY_L = _C(r"- entry day (?P<a>.+?), exit day (?P<b>.+?) \(whole stay: (?P<n>.+?)\)")
STAY_T = _C(r"\| (?P<a>.+?) \| (?P<b>.+?) \| (?P<n>.+?) \|")
REF_LINE = _C(r"Reference date: (?P<d>.+)")
WINDOW = _C(r"Window checked: (?P<a>.+?) to (?P<b>.+?), both included\.")
EVENT_L = _C(r"- (?P<label>[^:]+): (?P<d>.+)")
FILED_L = _C(r"- (?P<action>.+?) filed on: (?P<d>.+)")
ELAPSED_L = _C(r"- days from the (?P<label>.+?) to the filing: (?P<n>.+)")
EVENT_T = _C(r"\| (?P<d>.+?) \| (?P<label>.+?) \|")
FILED_T = _C(r"\| (?P<d>.+?) \| (?P<action>.+?) filed \|")
ELAPSED_T = _C(r"Days from the (?P<la>.+?) to the filing: (?P<na>.+?)\. Days from the (?P<lb>.+?) to the filing: "
               r"(?P<nb>.+?)\.")
START_L = _C(r"- policy start date: (?P<d>.+)")
RIDER_L = _C(r"- (?P<peril>.+?) cover: added by a rider effective (?P<d>.+)")
BASE_L = _C(r"- (?P<peril>.+?) cover: part of the base policy")
LOSS_L = _C(r"- (?P<peril>.+?) loss on: (?P<d>.+)")
EL_START_L = _C(r"- days from the policy start date to the loss: (?P<n>.+)")
EL_RIDER_L = _C(r"- days from the rider effective date to the loss: (?P<n>.+)")
PRIOR_L = _C(r"- earlier purchase on (?P<d>.+?): (?P<a>.+)")
REQUEST_L = _C(r"- new request on (?P<d>.+?): (?P<a>.+)")
TXN_L = _C(r"- (?P<d>.+?): (?P<t>deposit|withdrawal) of (?P<a>.+)")
DAY_L = _C(r"Day under review: (?P<d>.+)")
NOTICE_L = _C(r"- notice date: (?P<d>.+)")
METHOD_L = _C(r"- sent by: (?P<m>.+)")
BASE_DATE_L = _C(r"- (?P<n>.+?) after the notice date, before any postal add-on or closure: (?P<d>.+)")
CLOSURES_L = _C(r"Office closures: (?P<c>.+)\.")
DUE_L = _C(r"- response due date: (?P<d>.+)")
CUTOFF_L = _C(r"- office cutoff on the due date: (?P<t>.+)")
SENT_L = _C(r"- response sent: (?P<t>.+?) \[same instant in office time: (?P<o>.+)\]")


# ------------------------------------------------------------------------------------------------ reading values

def _date(text: str) -> str:
    try:
        return S.parse("date", text).isoformat()
    except S.SlotError as e:
        raise ParseError(f"date {text!r}: {e}") from None


def _days(text: str) -> int:
    try:
        return S.parse("count", text, DAYS)
    except S.SlotError as e:
        raise ParseError(f"day count {text!r}: {e}") from None


def _cents(text: str) -> int:
    try:
        return S.parse("cents", text, CENTS)
    except S.SlotError as e:
        raise ParseError(f"amount {text!r}: {e}") from None


def _moment(text: str) -> dt.datetime:
    try:
        return S.parse("datetime", text)
    except S.SlotError as e:
        raise ParseError(f"time {text!r}: {e}") from None


def _name(text: str) -> str:
    try:
        return S.parse("name", text)
    except S.SlotError as e:
        raise ParseError(f"name {text!r}: {e}") from None


def _full(rx: re.Pattern, line: str, what: str):
    m = rx.fullmatch(line)
    if not m:
        raise ParseError(f"{what}: line {line!r} does not match the G0 template")
    return m


def _d(iso: str) -> dt.date:
    return dt.date.fromisoformat(iso)


# ------------------------------------------------------------------------------------------------ blocks

def _find_block(state: str) -> tuple:
    paras = state.split("\n\n")
    hits = []
    for i, p in enumerate(paras):
        first = p.split("\n", 1)[0]
        for kind, style, rx in HEADERS:
            m = rx.fullmatch(first)
            if m:
                hits.append((i, kind, style, m))
    if len(hits) != 1 or hits[0][0] == 0:
        raise ParseError(f"{len(hits)} record block(s) after the narrative")
    i, kind, style, m = hits[0]
    lines = paras[i].split("\n")
    if kind == "notice":
        if len(lines) < 2:
            raise ParseError("notice block too short")
        kind = "addon" if lines[1].startswith("- notice date:") else "cutoff"
    return "\n\n".join(paras[:i]), kind, style, m, lines[1:]


def _rolling_block(lines: list, style: str) -> dict:
    if style == "table":
        if lines[:2] != ["| Entry day | Exit day | Whole stay |", "| --- | --- | --- |"]:
            raise ParseError("travel log table head")
        lines, rx = lines[2:], STAY_T
    else:
        rx = STAY_L
    if len(lines) < 3:
        raise ParseError("stay record too short")
    stays = []
    for line in lines[:-2]:
        m = _full(rx, line, "stay")
        stays.append([_date(m["a"]), _date(m["b"]), _days(m["n"])])
    ref = _date(_full(REF_LINE, lines[-2], "reference date")["d"])
    w = _full(WINDOW, lines[-1], "window")
    if _date(w["b"]) != ref:
        raise ParseError("the window does not end on the reference date")
    return {"stays": stays, "ref_date": ref, "win_start": _date(w["a"])}


def _anchor_block(lines: list, style: str) -> dict:
    if style == "table":
        if lines[:2] != ["| Date | Event |", "| --- | --- |"]:
            raise ParseError("court notice table head")
        rows = lines[2:]
        evs = [_full(EVENT_T, x, "event") for x in rows[:2]]
        out = {"labels": [_name(m["label"]) for m in evs], "events": [_date(m["d"]) for m in evs],
               "filed": None, "elapsed": None}
        if len(rows) == 2:
            return out
        if len(rows) != 4:
            raise ParseError("court notice rows")
        f = _full(FILED_T, rows[2], "filing")
        e = _full(ELAPSED_T, rows[3], "day counts")
        labels, counts, action = [e["la"], e["lb"]], [e["na"], e["nb"]], f["action"]
    else:
        evs = [_full(EVENT_L, x, "event") for x in lines[:2]]
        out = {"labels": [_name(m["label"]) for m in evs], "events": [_date(m["d"]) for m in evs],
               "filed": None, "elapsed": None}
        if len(lines) == 2:
            return out
        if len(lines) != 5:
            raise ParseError("case record lines")
        f = _full(FILED_L, lines[2], "filing")
        es = [_full(ELAPSED_L, x, "day count") for x in lines[3:5]]
        labels, counts, action = [m["label"] for m in es], [m["n"] for m in es], f["action"]
    if [_name(x) for x in labels] != out["labels"]:
        raise ParseError("day-count lines name other events")
    out.update(filed=_date(f["d"]), elapsed=[_days(x) for x in counts], _action=_name(action))
    return out


def _waiting_block(lines: list, style: str) -> dict:
    if len(lines) < 2:
        raise ParseError("policy block too short")
    start = _date(_full(START_L, lines[0], "policy start")["d"])
    m = RIDER_L.fullmatch(lines[1])
    rider = _date(m["d"]) if m else None
    m = m or _full(BASE_L, lines[1], "cover line")
    out = {"peril": _name(m["peril"]), "start": start, "rider": rider, "loss": None, "elapsed": None}
    rest = lines[2:]
    if not rest:
        return out
    if len(rest) != (3 if rider else 2):
        raise ParseError("loss lines")
    lo = _full(LOSS_L, rest[0], "loss")
    if _name(lo["peril"]) != out["peril"]:
        raise ParseError("the loss names another peril")
    el = [_days(_full(EL_START_L, rest[1], "day count from the start")["n"]),
          _days(_full(EL_RIDER_L, rest[2], "day count from the rider")["n"]) if rider else None]
    out.update(loss=_date(lo["d"]), elapsed=el)
    return out


def _purchase_block(lines: list, style: str) -> dict:
    if len(lines) < 3:
        raise ParseError("purchase log too short")
    prior = []
    for line in lines[:-2]:
        m = _full(PRIOR_L, line, "earlier purchase")
        prior.append([_date(m["d"]), _cents(m["a"])])
    r = _full(REQUEST_L, lines[-2], "new request")
    w = _full(WINDOW, lines[-1], "window")
    req = _date(r["d"])
    if _date(w["b"]) != req:
        raise ParseError("the window does not end on the request date")
    return {"prior": prior, "req_date": req, "req_amt": _cents(r["a"]), "win_start": _date(w["a"])}


def _cash_block(lines: list, style: str) -> dict:
    if len(lines) < 2:
        raise ParseError("cash ledger too short")
    txns = []
    for line in lines[:-1]:
        m = _full(TXN_L, line, "transaction")
        txns.append([_date(m["d"]), S.parse("category", m["t"], DIR_SET), _cents(m["a"])])
    return {"txns": txns, "day": _date(_full(DAY_L, lines[-1], "day under review")["d"])}


def _addon_block(lines: list, style: str) -> dict:
    if len(lines) != 4:
        raise ParseError("notice block lines")
    b = _full(BASE_DATE_L, lines[2], "plain due line")
    c = _full(CLOSURES_L, lines[3], "closures")["c"]
    return {"notice": _date(_full(NOTICE_L, lines[0], "notice date")["d"]),
            "method": S.parse("category", _full(METHOD_L, lines[1], "method")["m"], METHOD_SET),
            "_n_line": _days(b["n"]), "base": _date(b["d"]),
            "closed": [] if c == "none" else [_date(x) for x in c.split("; ")]}


def _cutoff_block(lines: list, style: str) -> dict:
    if len(lines) != 3:
        raise ParseError("notice block lines")
    due = _date(_full(DUE_L, lines[0], "due date")["d"])
    cut = _moment(_full(CUTOFF_L, lines[1], "cutoff")["t"])
    m = _full(SENT_L, lines[2], "sending time")
    sent, office = _moment(m["t"]), _moment(m["o"])
    if brute.epoch_minutes(sent) != brute.epoch_minutes(office):
        raise ParseError("the bracketed office time is not the same instant")
    if office.utcoffset() != cut.utcoffset() or sent.utcoffset() == cut.utcoffset():
        raise ParseError("office time must be the cutoff's offset, the sending time another one")
    if cut.date().isoformat() != due:
        raise ParseError("the printed cutoff is not on the due date")
    return {"due": due, "cutoff": cut.isoformat(), "sent": sent.isoformat(), "sent_office": office.isoformat()}


BLOCKS = {"rolling": _rolling_block, "anchor": _anchor_block, "waiting": _waiting_block,
          "purchase": _purchase_block, "cash": _cash_block, "addon": _addon_block, "cutoff": _cutoff_block}


# ------------------------------------------------------------------------------------------------ rules

def _clause(lexicon, text: str, schema: dict, kind: str):
    try:
        sem, _form, vals = lexicon.parse_exact(text, schema, admitted_only=True)
    except ValueError as e:
        raise ParseError(f"rule clause {text!r}: {e}") from None
    if sem not in KIND_SEMS.get(kind, SIGN_OK):
        raise ParseError(f"clause {text!r} means {sem}, not a {kind} rule")
    return sem, vals


def _rules(kind: str, text: str, lexicon) -> dict:
    m = CARD_RX[kind].fullmatch(text)
    if not m:
        raise ParseError(f"rule paragraph does not match the G0 {kind} card")
    count = ("count", DAYS)
    if kind == "rolling":
        sem, v = _clause(lexicon, m["win_clause"], {"N": count, "M": count}, kind)
        if (_days(m["m_win"]), _days(m["n_max"])) != (v["M"], v["N"]):
            raise ParseError("the card's checked period or limit differs from its rule clause")
        return {"rule": sem, "n_max": v["N"], "m_win": v["M"]}
    if kind == "anchor":
        sem, v = _clause(lexicon, m["an_clause"], {"N": count}, kind)
        if _days(m["n_days"]) != v["N"]:
            raise ParseError("the card's final day differs from its rule clause")
        return {"rule": sem, "n_days": v["N"], "action": _name(m["action"]),
                "_labels": [_name(m["eva_label"]), _name(m["evb_label"])]}
    if kind == "waiting":
        sem, v = _clause(lexicon, m["wait_clause"], {"W": count}, kind)
        if _days(m["w_days"]) != v["W"]:
            raise ParseError("the card's final waiting day differs from its rule clause")
        return {"rule": sem, "w_days": v["W"]}
    if kind in ("purchase", "cash"):
        sem, v = _clause(lexicon, m["cmp"], {"X": ("cents", CENTS)}, kind)
        out = {"cmp": sem, "threshold": v["X"]}
        if kind == "purchase":
            out["m_win"] = _days(m["m_win"])
        return out
    if kind == "addon":
        return {"n_days": _days(m["n_days"]), "k_days": _days(m["k_days"])}
    return {}


# ------------------------------------------------------------------------------------------------ parse

def parse(row: dict, ctx) -> dict:
    narrative, kind, style, head, lines = _find_block(row["state"])
    view = {"kind": kind, "style": style, "ref": S.parse("id", head["ref"]), "person": _name(head["person"])}
    if kind == "purchase":
        view["vendor"] = _name(head["vendor"])
    view.update(BLOCKS[kind](lines, style))
    rule, sep, question = row["instructions"].partition("\n\n")
    if not sep:
        raise ParseError("rule and question are not separated")
    view.update(_rules(kind, rule, ctx.lexicon))
    # printed intermediates and repeated facts
    if kind == "anchor":
        labels = view.pop("_labels")
        if labels != view["labels"]:
            raise ParseError("the rule and the record name different events")
        action = view.pop("_action", None)
        if action is not None and action != view["action"]:
            raise ParseError("the record files another document")
    if kind == "addon" and view.pop("_n_line") != view["n_days"]:
        raise ParseError("the plain due line counts another number of days")
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    if skin.author_mode == "T":
        told = K.parse_skin(skin, narrative, NARRATIVE)
        if told.get("PERSON") != view["person"] or told.get("REF") != view["ref"] or "TOPIC" not in told:
            raise ParseError("the narrative and the record name different people or files")
        view["topic"] = told["TOPIC"]
    wording = ctx.skin(row["meta"]["wording_id"])
    asked = K.match_template(wording.text, question, QUESTION)
    same = {"PERSON": "person", "REF": "ref", "REF_DATE": "ref_date", "ACTION": "action", "PERIL": "peril",
            "DAY": "day"}
    for k, v in asked.items():
        if same[k] not in view or view[same[k]] != v:
            raise ParseError(f"the question reads {k}={v!r}, the record does not")
    q = wording.qform
    if QUESTIONS.get(q, (None,))[0] != kind:
        raise ParseError(f"question {q} on a {kind} card")
    view["qform"] = q
    _check_intermediates(view)
    if row["qtype"] == "choice":
        view["options"] = [_option_key(q, t) for t in row["options"]]
    return view


def _check_intermediates(view: dict) -> None:
    """Printed intermediates re-derived, plus the generator invariants of G0 DF4-DF7 (H1, H13): a row that breaks one
    has no printed rule for that case, so solver B refuses it and the unit is dropped."""
    kind = view["kind"]
    if kind == "rolling":
        if len(brute.day_list(_d(view["win_start"]), _d(view["ref_date"]))) != view["m_win"]:
            raise ParseError("the printed window does not span the stated number of days")
        for a, b, n in view["stays"]:
            if len(brute.day_list(_d(a), _d(b))) != n:
                raise ParseError("a printed stay length disagrees with its dates")
            if _d(b) > _d(view["ref_date"]):
                raise ParseError("a stay ends after the reference date (G0 DF4)")
    elif kind == "anchor" and view["filed"]:
        f = _d(view["filed"])
        if f < max(_d(x) for x in view["events"]):
            raise ParseError("the filing is dated before the later event (G0 DF5)")
        for ev, n in zip(view["events"], view["elapsed"]):
            if len(brute.day_list(_d(ev), f)) - 1 != n:
                raise ParseError("a printed day count to the filing disagrees")
    elif kind == "waiting" and view["rider"] and _d(view["rider"]) <= _d(view["start"]):
        raise ParseError("the rider takes effect on or before the policy start (G0 DF6)")
    elif kind == "waiting" and view["loss"]:
        loss = _d(view["loss"])
        if loss <= _d(view["rider"] or view["start"]):
            raise ParseError("the loss is not after the start date of its cover (G0 DF6)")
        if len(brute.day_list(_d(view["start"]), loss)) - 1 != view["elapsed"][0]:
            raise ParseError("the day count from the policy start disagrees")
        if view["rider"] and len(brute.day_list(_d(view["rider"]), loss)) - 1 != view["elapsed"][1]:
            raise ParseError("the day count from the rider disagrees")
    elif kind == "purchase":
        if len(brute.day_list(_d(view["win_start"]), _d(view["req_date"]))) != view["m_win"]:
            raise ParseError("the printed window does not span the stated number of days")
        if any(_d(d) >= _d(view["req_date"]) for d, _ in view["prior"]):
            raise ParseError("an earlier purchase is dated on or after the request (G0 DF7)")
    elif kind == "addon":
        if brute.window_days(_d(view["notice"]), view["n_days"])[-1].isoformat() != view["base"]:
            raise ParseError("the plain due date is not the stated number of days after the notice")


def _option_key(qform: str, text: str):
    if qform == "ch_days":
        return _days(text)
    if qform == "ch_total":
        return _cents(text)
    if qform == "ch_cash_which":
        if text not in CASH_KEYS:
            raise ParseError(f"unknown cash option {text!r}")
        return CASH_KEYS[text]
    if qform in ("ch_deadline", "ch_first_day", "ch_due", "ch_receipt_day"):
        return _date(text)
    raise ParseError(f"question {qform} has no options")


# ------------------------------------------------------------------------------------------------ solver B

def _sign(x: int) -> int:
    return (x > 0) - (x < 0)


def _rolling(view: dict) -> dict:
    present = set()
    for a, b, _n in view["stays"]:
        days = set(brute.day_list(_d(a), _d(b)))
        if present & days:
            raise ParseError("stays overlap")
        present |= days
    bitmap = [day in present for day in brute.day_list(_d(view["win_start"]), _d(view["ref_date"]))]
    count = sum(bitmap)
    return {"value": count, "holds": count > view["n_max"]}


def _anchor(view: dict) -> dict:
    later = sorted(_d(x) for x in view["events"])[-1]
    period = brute.window_days(later, view["n_days"])            # day zero (the later date) .. day N
    out = {"value": period[-1].isoformat()}
    if view["filed"]:
        f = _d(view["filed"])
        out["holds"] = f in set(brute.day_list(min(f, later), period[-1]))
    return out


def _waiting(view: dict) -> dict:
    start = _d(view["rider"] or view["start"])
    waiting = brute.window_days(start, view["w_days"])           # day zero .. the final waiting day
    out = {"value": (waiting[-1] + ONE_DAY).isoformat()}
    if view["loss"]:
        loss = _d(view["loss"])
        out["holds"] = loss not in set(brute.day_list(min(loss, start), waiting[-1]))
    return out


def _purchase(view: dict) -> dict:
    ledger = {day: 0 for day in brute.day_list(_d(view["win_start"]), _d(view["req_date"]))}
    for d, amt in view["prior"]:
        if _d(d) in ledger:
            ledger[_d(d)] += amt
    total = view["req_amt"] + sum(ledger.values())
    return {"value": total, "holds": _sign(total - view["threshold"]) in SIGN_OK[view["cmp"]]}


def _cash(view: dict) -> dict:
    ledger = {}
    for d, direction, amt in view["txns"]:
        ledger.setdefault(_d(d), {"in": 0, "out": 0})[direction] += amt
    today = ledger.get(_d(view["day"]), {"in": 0, "out": 0})
    ok = SIGN_OK[view["cmp"]]
    label = CASH_LABEL[(_sign(today["in"] - view["threshold"]) in ok, _sign(today["out"] - view["threshold"]) in ok)]
    return {"value": label, "holds": label != "neither"}


def _addon(view: dict) -> dict:
    day = _d(view["base"])
    if view["method"] == "post":
        day = brute.window_days(day, view["k_days"])[-1]
    closed = {_d(x) for x in view["closed"]}
    while day in closed:                                         # walk forward to the next open day
        day = day + ONE_DAY
    return {"value": day.isoformat()}


def _cutoff(view: dict) -> dict:
    cut = dt.datetime.fromisoformat(view["cutoff"])
    sent = dt.datetime.fromisoformat(view["sent"])
    office = dt.datetime.fromisoformat(view["sent_office"])
    on_time = brute.epoch_minutes(sent) <= brute.epoch_minutes(cut)
    after = office.hour * 60 + office.minute > cut.hour * 60 + cut.minute
    received = office.date() + (ONE_DAY if after else dt.timedelta(0))
    return {"value": received.isoformat(), "holds": on_time}


SOLVERS = {"rolling": _rolling, "anchor": _anchor, "waiting": _waiting, "purchase": _purchase, "cash": _cash,
           "addon": _addon, "cutoff": _cutoff}


def solve_b(view: dict):
    kind, positive = QUESTIONS[view["qform"]]
    if kind != view["kind"]:
        raise ParseError("question and card kind disagree")
    out = SOLVERS[kind](view)
    if positive is None:
        return out["value"]
    return 1 if out["holds"] == positive else 0
