"""c2_build/families/T12/solver_b.py: T12 solver B, written from G0_SPEC.md (not from plugin.py).

parse(row, ctx) reads the RENDERED row back into the canonical facts (G0 v2.2 R12-R14):
  - the policy card (cards.split_rules: row.card on a yes/no row, the instructions before the last blank line on a
    choice row) line by line with this module's own regular expressions, in its full or its short style; the
    comparator and precedence clauses through the lexicon registry (admitted forms only: G-LEX vouches for each form's
    meaning);
  - the state blocks (split on blank lines): the purchase order, goods receipt, invoice and paid-invoice register in
    any of their four containers (key-value list, markdown table, CSV export, JSON), each read by its own parser; the
    Mode T narrative through skin.parse_skin (Mode F narrative facts are left to G3-H); a trailing pressure line
    carries no fact;
  - the question through its wording template; on choice rows every option text back to its key.
Every fact printed twice must read the same (line items, units, PO number, vendor, invoice number), and every printed
document total is re-derived here by integer arithmetic (the sum of quantity times unit price) and checked against the
text; no line total is printed (G0 v2.2 R2).
solve_b(view) loads the documents into an in-memory sqlite database (one table per document, joined on the line
number), evaluates every check as an integer-cents SQL query (the percent tolerance as 100 x difference against
percent x PO unit price: no division, no rounding), ranks the failing checks by the stated check order in SQL, and
maps the result to each question form with its own answer table (G0 R15-R19). Imports no solver-A code
(plugin.check_independence); nothing is written to disk (":memory:" only).
"""
from __future__ import annotations

import json
import re
import sqlite3

from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.cards import split_rules

# ------------------------------------------------------------------------------------------------ G0 closed sets
CURRENCY = {"USD": ("usd", "$"), "EUR": ("eur", "€"), "GBP": ("gbp", "£")}
UNIT_PLURAL = {"bag": "bags", "bottle": "bottles", "box": "boxes", "carton": "cartons", "case": "cases",
               "crate": "crates", "drum": "drums", "kit": "kits", "pack": "packs", "pallet": "pallets",
               "ream": "reams", "roll": "rolls", "set": "sets", "spool": "spools", "tube": "tubes", "unit": "units"}
UNIT_OF_WORD = {**{sg: sg for sg in UNIT_PLURAL}, **{pl: sg for sg, pl in UNIT_PLURAL.items()}}
DEPT_SCHEMA = ("category", (("surfaces", (("facilities", ("facilities",)), ("field", ("field service",)),
                                          ("it", ("IT support",)), ("lab", ("laboratory",)),
                                          ("marketing", ("marketing",)), ("warehouse", ("warehouse",)))),))
PERCENT = ("count", (("unit", ("percent", "percent")),))
NARRATIVE_SCHEMA = {"CLERK": ("name", ()), "DEPT": DEPT_SCHEMA, "VENDOR": ("name", ()), "INVOICE_ID": ("id", ()),
                    "PO_ID": ("id", ())}
WORDING_SCHEMA = {"INVOICE_ID": ("id", ())}
PREC_SEM = "prec.t12.first_failing"
CMP_ALLOWED = ("cmp.le", "cmp.lt")

# ------------------------------------------------------------------------------------------------ G0 R12: the card
# two styles (G0 v2.2): "full" on 85% of rows, "short" on 15%; every line of a card is in its style
STYLES = ("full", "short")
HEADER_RE = {
    "full": re.compile(r"AP policy of (?P<org>.+): each invoice gets exactly one action\."),
    "short": re.compile(r"(?P<org>.+) AP policy: each invoice gets exactly one action\."),
}
TITLE_KEY = {
    "full": {"Quantity check": "qty", "Price check": "price", "Duplicate check": "dup", "Approval-limit check": "limit"},
    "short": {"Quantity": "qty", "Price": "price", "Duplicate": "dup", "Approval limit": "limit"},
}
FAIL_PHRASE = {"qty": "hold for receipt", "price": "price-variance review", "dup": "reject as a duplicate",
               "limit": "route to a senior approver"}
TABLE_HEAD = ("| check | passes when | if it fails |", "|---|---|---|")
COND_QTY = {"full": "invoiced quantity is at most received quantity on every line",
            "short": "invoiced quantity at most received quantity on every line"}
COND_PCT_RE = re.compile(r"invoiced unit price minus PO unit price is (?P<c>.+) of the PO unit price on every line")
COND_ABS_RE = re.compile(r"invoiced unit price minus PO unit price is (?P<c>.+) on every line")
COND_DUP = {"full": "the invoice number is not in the paid-invoice register (exact match only)",
            "short": "invoice number not in the paid-invoice register (exact match only)"}
COND_LIMIT_RE = {
    "full": re.compile(r"the invoice total is (?P<c>.+) \(limit of approver (?P<a>[^()]+)\)"),
    "short": re.compile(r"invoice total is (?P<c>.+) \(limit of approver (?P<a>[^()]+)\)"),
}
ORDER_RE = re.compile(r"Check order: (?P<names>.+)\.")
NAME_KEY = {"quantity": "qty", "price": "price", "duplicate": "dup", "approval limit": "limit"}
RELEASE = {"full": "If every check passes: release for payment, the only action that pays. Lower invoiced prices "
                   "always pass.",
           "short": "If every check passes: release for payment, the only paying action. Lower invoiced prices "
                    "always pass."}
AMOUNTS_RE = re.compile(r"Amounts: (?P<cur>[A-Z]{3}), whole cents\.")
CODES_RE = re.compile(r"Answer codes: (?P<c>.+)\.")
CODE_PART_RE = re.compile(r"(?P<code>[A-Z][a-z]+) = (?P<p>[a-z -]+)")
PHRASE_KEY = {"release for payment": "release", "hold for receipt": "hold", "price-variance review": "review",
              "reject as a duplicate": "reject", "route to a senior approver": "escalate"}
CLOSED = "Nothing else applies: the policy and the documents shown are complete."
OPTION_KEY = {"Release for payment": "release", "Hold for receipt": "hold", "Send to price-variance review": "review",
              "Reject as a duplicate": "reject", "Route to a senior approver": "escalate"}
NONE_OPTION = "None of the lines"

# ------------------------------------------------------------------------------------------------ G0 R14: documents
KV = {
    "po": (re.compile(r"Purchase order (?P<id>\S+) from (?P<vendor>.+)"), None,
           re.compile(r"- line (?P<i>\d+): (?P<item>[^;\n]+); (?P<q>[^;\n]+?) at (?P<p>[^;\n]+)"), "- order total: "),
    "gr": (re.compile(r"Goods receipt (?P<id>\S+)"), None,
           re.compile(r"- line (?P<i>\d+): received (?P<q>[^;\n]+)"), None),
    "inv": (re.compile(r"Invoice (?P<id>\S+) for purchase order (?P<po>\S+)"), None,
            re.compile(r"- line (?P<i>\d+): (?P<item>[^;\n]+); (?P<q>[^;\n]+?) at (?P<p>[^;\n]+)"),
            "- invoice total: "),
}
KV_REG_RE = re.compile(r"Paid-invoice register for (?P<vendor>.+): (?P<ids>\S+(?:, \S+)*)")
TB = {
    "po": (re.compile(r"Purchase order (?P<id>\S+) \| vendor (?P<vendor>[^|]+)"),
           ("| line | item | quantity | unit price |", "|---|---|---|---|"),
           re.compile(r"\| (?P<i>\d+) \| (?P<item>[^|]+) \| (?P<q>[^|]+) \| (?P<p>[^|]+) \|"),
           re.compile(r"\| total \| \| \| (?P<t>[^|]+) \|")),
    "gr": (re.compile(r"Goods receipt (?P<id>\S+)"),
           ("| line | received |", "|---|---|"),
           re.compile(r"\| (?P<i>\d+) \| (?P<q>[^|]+) \|"), None),
    "inv": (re.compile(r"Invoice (?P<id>\S+) \| purchase order (?P<po>\S+)"),
            ("| line | item | quantity | unit price |", "|---|---|---|---|"),
            re.compile(r"\| (?P<i>\d+) \| (?P<item>[^|]+) \| (?P<q>[^|]+) \| (?P<p>[^|]+) \|"),
            re.compile(r"\| total \| \| \| (?P<t>[^|]+) \|")),
}
TB_REG_RE = re.compile(r"Paid-invoice register \| vendor (?P<vendor>[^|]+)")
CSV = {
    "po": (re.compile(r"Purchase order export, po_number (?P<id>\S+), vendor (?P<vendor>[^,]+)"),
           "line,item,quantity,unit_price"),
    "gr": (re.compile(r"Goods receipt export, gr_number (?P<id>\S+)"),
           "line,received"),
    "inv": (re.compile(r"Invoice export, invoice_number (?P<id>\S+), po_number (?P<po>\S+)"),
            "line,item,quantity,unit_price"),
}
CSV_REG_RE = re.compile(r"Paid-invoice register export, vendor (?P<vendor>[^,]+)")
JSON_HEAD = {"Purchase order (JSON):": "po", "Goods receipt (JSON):": "gr", "Invoice (JSON):": "inv",
             "Paid-invoice register (JSON):": "reg"}
JSON_KEYS = {"po": {"po_number", "vendor", "lines", "total_cents"},
             "gr": {"gr_number", "lines"},
             "inv": {"invoice_number", "po_number", "lines", "total_cents"},
             "reg": {"vendor", "paid_invoice_numbers"}}
JSON_LINE_KEYS = {"po": {"line", "item", "quantity", "unit_price_cents"},
                  "gr": {"line", "received"},
                  "inv": {"line", "item", "quantity", "unit_price_cents"}}

# ------------------------------------------------------------------------------------------------ G0 R15-R19: answers
ACTION_OF_CHECK = {"qty": "hold", "price": "review", "dup": "reject", "limit": "escalate"}
RELEASE_YES = {"yn_release": True, "yn_dneg_release": True, "yn_not_release": False, "yn_payment_stopped": False,
               "yn_exception_route": False}
PRICE_FAIL_YES = {"yn_within_tol": False, "yn_over_tol": True}


class ParseError(ValueError):
    pass


def _one(rx, text: str, what: str):
    m = rx.fullmatch(text)
    if not m:
        raise ParseError(f"{what}: {text[:80]!r}")
    return m


# ------------------------------------------------------------------------------------------------ value readers
def _qty(text: str) -> tuple:
    """(count, unit singular) from '40 cases' / 'one case' (the unit from the G0 closed list; agreement checked)."""
    m = re.fullmatch(r"(?P<n>\S+) (?P<u>[a-z]+)", str(text))
    if not m or m["u"] not in UNIT_OF_WORD:
        raise ParseError(f"quantity {text!r}")
    sg = UNIT_OF_WORD[m["u"]]
    return S.parse("count", str(text), (("unit", (sg, UNIT_PLURAL[sg])),)), sg


def _cents(text, money: tuple) -> int:
    if isinstance(text, bool):
        raise ParseError("an amount is never a boolean")
    if isinstance(text, int):
        return text
    return S.parse("cents", str(text), money)


def _name(text: str) -> str:
    return S.parse("name", str(text))


def _id(text: str) -> str:
    return S.parse("id", str(text))


# ------------------------------------------------------------------------------------------------ parse: card
def _card(card: str) -> tuple:
    """(facts, raw clause texts) from the policy card; clauses are read once the currency is known."""
    lines = card.split("\n")
    style = next((sty for sty in STYLES if HEADER_RE[sty].fullmatch(lines[0])), None)
    if style is None:
        raise ParseError(f"policy header {lines[0][:80]!r}")
    m = HEADER_RE[style].fullmatch(lines[0])
    out = {"org": _name(m["org"]), "card_style": style}
    titles = "|".join(re.escape(t) for t in TITLE_KEY[style])
    list_re = re.compile(rf"(?P<lead>\d+\.|-) (?P<title>{titles}): (?P<cond>.+)\. If it fails: (?P<act>[a-z -]+)\.")
    table_re = re.compile(rf"\| (?P<title>{titles}) \| (?P<cond>[^|]+) \| (?P<act>[a-z -]+) \|")
    k = 1
    table = lines[k] == TABLE_HEAD[0]
    if table:
        if lines[k + 1] != TABLE_HEAD[1]:
            raise ParseError("check table separator")
        k += 2
    rows = []
    while not lines[k].startswith("Check order: "):
        rm = (table_re if table else list_re).fullmatch(lines[k])
        if not rm:
            raise ParseError(f"check line {lines[k]!r}")
        key = TITLE_KEY[style][rm["title"]]
        if rm["act"] != FAIL_PHRASE[key]:
            raise ParseError(f"{key} check names the action {rm['act']!r}")
        rows.append((None if table else rm["lead"], key, rm["cond"]))
        k += 1
    display = [r[1] for r in rows]
    if len(set(display)) != len(display) or not {"qty", "price"} <= set(display) or not 2 <= len(display) <= 4:
        raise ParseError(f"checks {display}")
    if table:
        listing = "table"
    elif all(lead == "-" for lead, _, _ in rows):
        listing = "bulleted"
    elif [lead for lead, _, _ in rows] == [f"{i}." for i in range(1, len(rows) + 1)]:
        listing = "numbered"
    else:
        raise ParseError("check leads are neither 1., 2., ... nor bullets")
    om = _one(ORDER_RE, lines[k], "check order")
    names = om["names"].split(", then ")
    if any(x not in NAME_KEY for x in names):
        raise ParseError(f"check order {names}")
    order = [NAME_KEY[x] for x in names]
    if sorted(order) != sorted(display):
        raise ParseError("the check order names other checks than the list")
    if listing == "numbered" and order != display:
        raise ParseError("numbered checks are listed in another order than the check order")
    out.update(display=display, checks=order, style=listing)
    out["precedence"] = lines[k + 1]                    # read through the lexicon below
    if lines[k + 2] != RELEASE[style]:
        raise ParseError("release line")
    am = _one(AMOUNTS_RE, lines[k + 3], "amounts line")
    if am["cur"] not in CURRENCY:
        raise ParseError(f"currency {am['cur']}")
    out["currency_code"] = am["cur"]
    k += 4
    codes = None
    cm = CODES_RE.fullmatch(lines[k])
    if cm:
        codes = {}
        for part in cm["c"].split(", "):
            pm = CODE_PART_RE.fullmatch(part)
            if not pm or pm["code"] in codes or pm["p"] not in PHRASE_KEY:
                raise ParseError("answer codes")
            codes[pm["code"]] = PHRASE_KEY[pm["p"]]
        want = {"release"} | {ACTION_OF_CHECK[c] for c in order}
        if sorted(codes.values()) != sorted(want):
            raise ParseError("answer codes do not cover the card's actions once each")
        k += 1
    if lines[k:] != [CLOSED]:
        raise ParseError("closed-world sentence")
    out["codes"] = codes
    return out, {key: cond for _, key, cond in rows}


def _clauses(view: dict, conds: dict, ctx, money: tuple) -> None:
    style = view["card_style"]
    if conds["qty"] != COND_QTY[style]:
        raise ParseError("quantity condition")
    pm = COND_PCT_RE.fullmatch(conds["price"])
    if pm:
        sem, _fid, vals = ctx.lexicon.parse_exact(pm["c"], {"X": PERCENT}, admitted_only=True)
        view["tol_kind"] = "pct"
    else:
        am = _one(COND_ABS_RE, conds["price"], "price condition")
        sem, _fid, vals = ctx.lexicon.parse_exact(am["c"], {"X": ("cents", money)}, admitted_only=True)
        view["tol_kind"] = "abs"
    if sem not in CMP_ALLOWED:
        raise ParseError(f"price comparator {sem}")
    view.update(tol=vals["X"], tol_cmp=sem)
    if "dup" in conds and conds["dup"] != COND_DUP[style]:
        raise ParseError("duplicate condition")
    view.update(limit=None, limit_cmp=None, approver=None)
    if "limit" in conds:
        lm = _one(COND_LIMIT_RE[style], conds["limit"], "approval-limit condition")
        sem, _fid, vals = ctx.lexicon.parse_exact(lm["c"], {"X": ("cents", money)}, admitted_only=True)
        if sem not in CMP_ALLOWED:
            raise ParseError(f"limit comparator {sem}")
        view.update(limit=vals["X"], limit_cmp=sem, approver=_name(lm["a"]))
    psem, _fid, _ = ctx.lexicon.parse_exact(view["precedence"], {}, admitted_only=True)
    if psem != PREC_SEM:
        raise ParseError(f"precedence clause reads {psem}")
    view["precedence"] = psem


# ------------------------------------------------------------------------------------------------ parse: documents
def _line_tuple(kind: str, i, q, item=None, p=None, money=None) -> dict:
    """A receipt line is (line, received quantity); a purchase order or invoice line (line, item, quantity, unit price)."""
    qty, unit = _qty(q)
    out = {"i": int(i), "qty": qty, "unit": unit}
    if kind != "gr":
        out.update(item=_name(item), price=_cents(p, money))
    return out


def _read_kv(kind: str, block: str, money: tuple) -> dict:
    lines = block.split("\n")
    if kind == "reg":
        m = _one(KV_REG_RE, block, "register")
        return {"vendor": _name(m["vendor"]), "ids": [_id(x) for x in m["ids"].split(", ")]}
    head_re, _unused, line_re, total_prefix = KV[kind]
    out = dict(_one(head_re, lines[0], f"{kind} header").groupdict())
    body = lines[1:-1] if total_prefix else lines[1:]
    out["lines"] = [_line_tuple(kind, **_one(line_re, ln, f"{kind} line").groupdict(), money=money) for ln in body]
    if total_prefix:
        if not lines[-1].startswith(total_prefix):
            raise ParseError(f"{kind} total line")
        out["total"] = _cents(lines[-1][len(total_prefix):], money)
    return out


def _read_table(kind: str, block: str, money: tuple) -> dict:
    lines = block.split("\n")
    if kind == "reg":
        m = _one(TB_REG_RE, lines[0], "register header")
        if lines[1:3] != ["| invoice number |", "|---|"]:
            raise ParseError("register table head")
        ids = [_one(re.compile(r"\| (?P<x>\S+) \|"), ln, "register row")["x"] for ln in lines[3:]]
        return {"vendor": _name(m["vendor"]), "ids": [_id(x) for x in ids]}
    head_re, cols, line_re, total_re = TB[kind]
    out = dict(_one(head_re, lines[0], f"{kind} header").groupdict())
    if tuple(lines[1:3]) != cols:
        raise ParseError(f"{kind} table head")
    body = lines[3:-1] if total_re else lines[3:]
    out["lines"] = [_line_tuple(kind, **_one(line_re, ln, f"{kind} row").groupdict(), money=money) for ln in body]
    if total_re:
        out["total"] = _cents(_one(total_re, lines[-1], f"{kind} total row")["t"], money)
    return out


def _read_csv(kind: str, block: str, money: tuple) -> dict:
    lines = block.split("\n")
    if kind == "reg":
        m = _one(CSV_REG_RE, lines[0], "register header")
        if lines[1] != "invoice_number":
            raise ParseError("register column")
        return {"vendor": _name(m["vendor"]), "ids": [_id(x) for x in lines[2:]]}
    head_re, cols = CSV[kind]
    out = dict(_one(head_re, lines[0], f"{kind} header").groupdict())
    if lines[1] != cols:
        raise ParseError(f"{kind} columns")
    width = len(cols.split(","))
    body = lines[2:]
    if kind != "gr":
        last = body[-1].split(",")
        if last[:width - 1] != ["total"] + [""] * (width - 2):
            raise ParseError(f"{kind} total row")
        out["total"] = _cents(last[-1], money)
        body = body[:-1]
    rows = []
    for ln in body:
        cells = ln.split(",")
        if len(cells) != width:
            raise ParseError(f"{kind} csv row {ln!r}")
        if kind == "gr":
            rows.append(_line_tuple(kind, cells[0], cells[1], money=money))
        else:
            rows.append(_line_tuple(kind, cells[0], cells[2], item=cells[1], p=cells[3], money=money))
    out["lines"] = rows
    return out


def _read_json(kind: str, obj, money: tuple) -> dict:
    if not isinstance(obj, dict) or set(obj) != JSON_KEYS[kind]:
        raise ParseError(f"{kind} JSON keys")
    if kind == "reg":
        ids = obj["paid_invoice_numbers"]
        if not isinstance(ids, list) or not all(isinstance(x, str) for x in ids):
            raise ParseError("register JSON list")
        return {"vendor": _name(obj["vendor"]), "ids": [_id(x) for x in ids]}
    key = {"po": "po_number", "gr": "gr_number", "inv": "invoice_number"}[kind]
    out = {"id": obj[key]}
    if kind == "inv":
        out["po"] = obj["po_number"]
    if kind == "po":
        out["vendor"] = obj["vendor"]
    if kind != "gr":
        if not isinstance(obj["total_cents"], int):
            raise ParseError("JSON totals are integer cents")
        out["total"] = obj["total_cents"]
    rows = []
    for x in obj["lines"]:
        if not isinstance(x, dict) or set(x) != JSON_LINE_KEYS[kind] or not isinstance(x["line"], int):
            raise ParseError(f"{kind} JSON line")
        if kind == "gr":
            rows.append(_line_tuple(kind, x["line"], x["received"]))
        else:
            if not isinstance(x["unit_price_cents"], int):
                raise ParseError("JSON prices are integer cents")
            rows.append(_line_tuple(kind, x["line"], x["quantity"], item=x["item"], p=x["unit_price_cents"],
                                    money=money))
    out["lines"] = rows
    return out


def _classify(block: str):
    """(kind, container) of a document block by its first line, or None for any other block."""
    first = block.split("\n", 1)[0]
    if first in JSON_HEAD:
        return JSON_HEAD[first], "json"
    for kind, prefix in (("po", "Purchase order "), ("gr", "Goods receipt "), ("inv", "Invoice "),
                         ("reg", "Paid-invoice register")):
        if first.startswith(prefix):
            if " export, " in first:
                return kind, "csv"
            if kind == "reg":
                return kind, "table" if first.startswith("Paid-invoice register | ") else "kv"
            second = block.split("\n")[1] if "\n" in block else ""
            return kind, "table" if second.startswith("| ") else "kv"
    return None


def _documents(state: str, money: tuple) -> tuple:
    docs, rest, fmts = {}, [], set()
    for block in state.split("\n\n"):
        c = _classify(block)
        if c is None:
            rest.append(block)
            continue
        kind, fmt = c
        if kind in docs:
            raise ParseError(f"two {kind} blocks")
        if fmt == "json":
            obj = json.loads(block.split("\n", 1)[1])
            docs[kind] = _read_json(kind, obj, money)
        else:
            docs[kind] = {"kv": _read_kv, "table": _read_table, "csv": _read_csv}[fmt](kind, block, money)
        fmts.add(fmt)
    if not {"po", "gr", "inv"} <= set(docs) or len(fmts) != 1:
        raise ParseError("state needs a purchase order, a goods receipt and an invoice in one container")
    return docs, rest


def _join(docs: dict) -> dict:
    """One view of the three documents, line by line; every repeated fact and every printed document total checked
    (the total of a document is the sum of quantity times unit price over its lines; no line total is printed)."""
    po, gr, inv = docs["po"], docs["gr"], docs["inv"]
    n = len(po["lines"])
    if not 1 <= n <= 4 or len(gr["lines"]) != n or len(inv["lines"]) != n:
        raise ParseError("the documents list different numbers of lines")
    vendor, po_id = _name(po["vendor"]), _id(po["id"])
    if _id(inv["po"]) != po_id:
        raise ParseError("the invoice names another purchase order")
    lines = []
    for k, (a, b, c) in enumerate(zip(po["lines"], gr["lines"], inv["lines"]), 1):
        if not a["i"] == b["i"] == c["i"] == k or not a["item"] == c["item"]:
            raise ParseError(f"line {k}: numbering or item differs between documents")
        if not a["unit"] == b["unit"] == c["unit"]:
            raise ParseError(f"line {k}: unit differs between documents")
        lines.append({"item": a["item"], "unit": a["unit"], "po_qty": a["qty"], "po_price": a["price"],
                      "received": b["qty"], "inv_qty": c["qty"], "inv_price": c["price"]})
    if len({x["item"] for x in lines}) != n:
        raise ParseError("two lines name the same item")
    po_sum = sum(x["po_qty"] * x["po_price"] for x in lines)
    inv_sum = sum(x["inv_qty"] * x["inv_price"] for x in lines)
    if po["total"] != po_sum or inv["total"] != inv_sum:
        raise ParseError("a printed document total is not the sum of quantity times unit price")
    out = {"vendor": vendor, "po_id": po_id, "gr_id": _id(gr["id"]), "invoice_id": _id(inv["id"]),
           "lines": lines,
           "po_total": po["total"], "inv_total": inv["total"], "register": None}
    if "reg" in docs:
        if _name(docs["reg"]["vendor"]) != vendor:
            raise ParseError("the register is for another vendor")
        out["register"] = docs["reg"]["ids"]
    return out


# ------------------------------------------------------------------------------------------------ parse
def parse(row: dict, ctx) -> dict:
    card, question = split_rules(row)
    if not card or not question:
        raise ParseError("policy and question are not separated")
    view, conds = _card(card)
    code = view.pop("currency_code")
    cur, sym = CURRENCY[code]
    money = (("currency", code), ("symbol", sym))
    _clauses(view, conds, ctx, money)
    docs, rest = _documents(row["state"], money)
    view.update(_join(docs))
    view["currency"] = cur
    if ("dup" in view["checks"]) != (view["register"] is not None):
        raise ParseError("the register is shown iff the duplicate check is on the card")
    wording = ctx.skin(row["meta"]["wording_id"])
    asked = K.match_template(wording.text, question, WORDING_SCHEMA)
    view["qform"] = wording.qform
    if not 1 <= len(rest) <= 2:
        raise ParseError("state blocks: the documents, a narrative and at most one pressure line")
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    told = {}
    if skin.author_mode == "T":
        told = K.parse_skin(skin, rest[0], NARRATIVE_SCHEMA)
        if "CLERK" not in told or "DEPT" not in told:
            raise ParseError("the narrative skin lacks CLERK / DEPT")
        view.update(clerk=told["CLERK"], dept=told["DEPT"])
    printed = {"VENDOR": view["vendor"], "INVOICE_ID": view["invoice_id"], "PO_ID": view["po_id"]}
    for k, v in list(told.items()) + list(asked.items()):
        if k in printed and v != printed[k]:
            raise ParseError(f"{k} reads {v!r} in the text but {printed[k]!r} in the documents")
    if row["qtype"] == "choice":
        view["options"] = [_option_key(view, t) for t in row["options"]]
    return view


def _option_key(view: dict, text: str):
    if view["qform"] == "ch_action":
        table = view["codes"] if view["codes"] else OPTION_KEY
        if text not in table:
            raise ParseError(f"unknown action option {text!r}")
        return table[text]
    if view["qform"] == "ch_price_line":
        if text == NONE_OPTION:
            return "none"
        if text not in [x["item"] for x in view["lines"]]:
            raise ParseError(f"option {text!r} names no line")
        return text
    raise ParseError(f"question {view['qform']} has no options")


# ------------------------------------------------------------------------------------------------ solve: sqlite
def solve_b(view: dict):
    con = sqlite3.connect(":memory:")
    try:
        con.execute("CREATE TABLE po (line INTEGER PRIMARY KEY, item TEXT, qty INTEGER, cents INTEGER)")
        con.execute("CREATE TABLE gr (line INTEGER PRIMARY KEY, item TEXT, qty INTEGER)")
        con.execute("CREATE TABLE inv (line INTEGER PRIMARY KEY, item TEXT, qty INTEGER, cents INTEGER)")
        con.execute("CREATE TABLE reg (number TEXT)")
        con.execute("CREATE TABLE policy (chk TEXT PRIMARY KEY, rank INTEGER)")
        con.execute("CREATE TABLE fails (chk TEXT PRIMARY KEY)")
        for k, x in enumerate(view["lines"], 1):
            con.execute("INSERT INTO po VALUES (?, ?, ?, ?)", (k, x["item"], x["po_qty"], x["po_price"]))
            con.execute("INSERT INTO gr VALUES (?, ?, ?)", (k, x["item"], x["received"]))
            con.execute("INSERT INTO inv VALUES (?, ?, ?, ?)", (k, x["item"], x["inv_qty"], x["inv_price"]))
        for x in view["register"] or ():
            con.execute("INSERT INTO reg VALUES (?)", (x,))
        for rank, chk in enumerate(view["checks"]):
            con.execute("INSERT INTO policy VALUES (?, ?)", (chk, rank))
        op_t = ">" if view["tol_cmp"] == "cmp.le" else ">="
        if view["tol_kind"] == "pct":
            price_sql = (f"SELECT inv.line FROM inv JOIN po ON po.line = inv.line "
                         f"WHERE 100 * (inv.cents - po.cents) {op_t} :tol * po.cents ORDER BY inv.line")
        else:
            price_sql = (f"SELECT inv.line FROM inv JOIN po ON po.line = inv.line "
                         f"WHERE inv.cents - po.cents {op_t} :tol ORDER BY inv.line")
        price_lines = [r[0] for r in con.execute(price_sql, {"tol": view["tol"]})]
        failing = {
            "qty": con.execute("SELECT COUNT(*) FROM inv JOIN gr ON gr.line = inv.line "
                               "WHERE inv.qty > gr.qty").fetchone()[0] > 0,
            "price": bool(price_lines),
        }
        if "dup" in view["checks"]:
            failing["dup"] = con.execute("SELECT COUNT(*) FROM reg WHERE number = :n",
                                         {"n": view["invoice_id"]}).fetchone()[0] > 0
        if "limit" in view["checks"]:
            op_l = ">" if view["limit_cmp"] == "cmp.le" else ">="
            failing["limit"] = bool(con.execute(f"SELECT (SELECT SUM(qty * cents) FROM inv) {op_l} :lim",
                                                {"lim": view["limit"]}).fetchone()[0])
        for chk in view["checks"]:
            if failing[chk]:
                con.execute("INSERT INTO fails VALUES (?)", (chk,))
        first = con.execute("SELECT f.chk FROM fails f JOIN policy p ON p.chk = f.chk ORDER BY p.rank "
                            "LIMIT 1").fetchone()
    finally:
        con.close()
    action = ACTION_OF_CHECK[first[0]] if first else "release"
    q = view["qform"]
    if q == "ch_action":
        return action
    if q == "ch_price_line":
        if len(price_lines) > 1:
            raise ParseError("more than one line fails the price check: no single line answers")
        return view["lines"][price_lines[0] - 1]["item"] if price_lines else "none"
    if q in PRICE_FAIL_YES:
        return 1 if bool(price_lines) == PRICE_FAIL_YES[q] else 0
    if q in RELEASE_YES:
        return 1 if (action == "release") == RELEASE_YES[q] else 0
    if q == "yn_price_review":
        return 1 if action == "review" else 0
    raise ParseError(f"unknown question form {q}")
