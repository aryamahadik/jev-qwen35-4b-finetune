"""c2_kit/reference/r00_solver_b.py: R00 solver B, written from G0_LITE_R00.md (not from r00.py).

parse(row, ctx) reads the RENDERED row back into the canonical facts:
  - the program-rendered record block and rule sentence by this module's own regular expressions;
  - the comparator clause through the lexicon registry (admitted forms only: G-LEX vouches for each form's meaning);
  - the narrative skin (Mode T) through skin.parse_skin (the template-guided parser built on typed slot patterns);
    Mode F narrative facts are left to G3-H;
  - the question through its wording template (its admitted meaning is the question form);
  - on choice rows, every option text back to its key.
Every fact that appears twice (narrative and record, wording and record) must read the same.
solve_b(view) decides by enumeration: the filing window is the list of dates day 0 .. day N, built day by day, and the
filing date must be in it; the printed day count must equal the enumerated position; the amount test is a table on
the sign of the integer-cents difference. Imports no solver-A code (plugin.check_independence).
"""
from __future__ import annotations

import datetime as dt
import re

from .. import brute
from .. import skin as K
from .. import slots as S

CENTS = ("cents", (("currency", "USD"), ("symbol", "$")))
DAYS = ("count", (("unit", ("day", "days")),))
CATS = ("category", (("surfaces", (("catering", ("catering", "meals")), ("software", ("software",)),
                                   ("travel", ("travel",)))),))
SCHEMA = {"EMPLOYEE": ("name", ()), "EXPENSE_ID": ("id", ()), "CATEGORY": CATS, "AMOUNT": CENTS,
          "PURCHASE_DATE": ("date", ()), "RECEIPT_DATE": ("date", ()), "FILED_DATE": ("date", ())}
NARRATIVE_REQUIRED = ("EMPLOYEE", "CATEGORY", "RECEIPT_DATE")
RECORD_RE = re.compile(r"Expense record (?P<id>[^\s:]+):\n- amount: (?P<amount>[^\n]+)\n- purchase date: (?P<p>[^\n]+)"
                       r"\n- claim filed: (?P<f>[^\n]+)\n- days from purchase to filing: (?P<el>[^\n]+)")
RULE_RE = re.compile(r"Expense rule: an expense is auto-approved when both of these hold: its amount is (?P<cmp>.+?), "
                     r"and the claim is filed at most (?P<n>.+?) after the purchase date \(count the purchase date as "
                     r"day 0\)\. Any other expense goes to manual review\. The record is complete: no other rule or "
                     r"fact applies\.")
OPTION_VERDICT = {"Auto-approved": "approve", "Manual review": "review"}
AMOUNT_TEST = {"cmp.le": lambda diff: diff < 1, "cmp.lt": lambda diff: diff < 0}
ANSWER = {"yn_approved": lambda ok: 1 if ok else 0, "yn_review": lambda ok: 0 if ok else 1,
          "yn_not_approved": lambda ok: 0 if ok else 1, "ch_outcome": lambda ok: "approve" if ok else "review"}


class ParseError(ValueError):
    pass


def _one(rx, text, what):
    ms = list(rx.finditer(text))
    if len(ms) != 1:
        raise ParseError(f"{len(ms)} {what}(s) in the row")
    return ms[0]


def parse(row: dict, ctx) -> dict:
    state = row["state"]
    m = _one(RECORD_RE, state, "record block")
    rec = {"EXPENSE_ID": S.parse("id", m["id"]), "AMOUNT": S.parse("cents", m["amount"], CENTS[1]),
           "PURCHASE_DATE": S.parse("date", m["p"]).isoformat(), "FILED_DATE": S.parse("date", m["f"]).isoformat()}
    elapsed = S.parse("count", m["el"], DAYS[1])
    head = state[:m.start()]
    if not head.endswith("\n\n"):
        raise ParseError("narrative and record are not separated by one blank line")
    narrative = head[:-2]
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    told = {}
    if skin.author_mode == "T":
        told = K.parse_skin(skin, narrative, SCHEMA)
        missing = [k for k in NARRATIVE_REQUIRED if k not in told]
        if missing:
            raise ParseError(f"skin lacks required narrative slots {missing}")
    rule, sep, question = row["instructions"].partition("\n\n")
    if not sep:
        raise ParseError("rule and question are not separated")
    r = RULE_RE.fullmatch(rule)
    if not r:
        raise ParseError("rule sentence does not match the G0-lite wording")
    sem, _form, vals = ctx.lexicon.parse_exact(r["cmp"], {"X": CENTS}, admitted_only=True)
    limit = vals["X"]
    n_days = S.parse("count", r["n"], DAYS[1])
    wording = ctx.skin(row["meta"]["wording_id"])
    asked = K.match_template(wording.text, question, SCHEMA)
    for k, v in list(told.items()) + list(asked.items()):
        if k in rec and rec[k] != v:
            raise ParseError(f"{k} reads {v!r} in the text but {rec[k]!r} in the record")
    view = {"expense_id": rec["EXPENSE_ID"], "amount": rec["AMOUNT"], "limit": limit, "cmp": sem, "n_days": n_days,
            "purchase_date": rec["PURCHASE_DATE"], "filed_date": rec["FILED_DATE"], "elapsed": elapsed,
            "qform": wording.qform}
    if skin.author_mode == "T":
        view.update(employee=told["EMPLOYEE"], category=told["CATEGORY"], receipt_date=told["RECEIPT_DATE"])
    if row["qtype"] == "choice":
        view["options"] = [_option_key(wording.qform, t) for t in row["options"]]
    return view


def _option_key(qform: str, text: str):
    if qform == "ch_outcome":
        if text not in OPTION_VERDICT:
            raise ParseError(f"unknown verdict option {text!r}")
        return OPTION_VERDICT[text]
    if qform == "ch_deadline":
        return S.parse("date", text).isoformat()
    raise ParseError(f"question {qform} has no options")


def solve_b(view: dict):
    p = dt.date.fromisoformat(view["purchase_date"])
    f = dt.date.fromisoformat(view["filed_date"])
    window = brute.window_days(p, view["n_days"])
    if view["qform"] == "ch_deadline":
        return window[-1].isoformat()
    walked = brute.day_list(p, f)
    if not walked or len(walked) - 1 != view["elapsed"]:
        raise ParseError("the printed day count disagrees with the dates")
    in_window = f in set(window)
    amount_ok = AMOUNT_TEST[view["cmp"]](view["amount"] - view["limit"])
    return ANSWER[view["qform"]](amount_ok and in_window)
