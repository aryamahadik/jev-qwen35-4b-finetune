"""families/T24/solver_b.py: T24 solver B, written from G0_SPEC.md (not from plugin.py).

parse(row, ctx) reads the RENDERED row back into the canonical facts with this module's own readers:
  - the card (cards.split_rules: row.card on a yes/no row, the instructions before the last blank line on a choice
    row) by the regular expression of the G0 v2.2 card wording, full or short: the policy title (full style; the
    short style names it only in the version headers), the three outcome names (by their role in the rule
    sentence), the amount field, the category and condition lists;
  - the state blocks (split on blank lines) by their header lines: bullet versions ("<Title>, original version:" /
    "..., revised version:"), the update notice ("Original version of the ... (before the update):"), the side-by-side
    table, the original version plus its edit list ("removed: ..." / "added: ..."; the revised version is the
    original minus the removed lines plus the added lines), and the case record (fixed field order, every day count
    printed). The one remaining block is the narrative;
  - every clause line through the lexicon registry (ctx.lexicon.parse_exact, admitted forms only), with a schema
    built from the card and the record (G-LEX vouches for each form's meaning; this module maps a meaning to its
    clause by its own table);
  - the narrative through skin.parse_skin (Mode T; facts it repeats must equal the record); Mode F is left to G3-H;
  - the question through its wording template; on choice rows every option text back to its outcome role.
solve_b(view) loads the case and both versions' clauses into an in-memory sqlite database and decides each version
with ONE SQL query: julianday differences for the day counts (checked against the printed counts first), COALESCE of
the category / date-window special limits over the base limit, EXISTS for the exclusion, amount and condition
clauses, a CASE for the outcome. Imports no solver-A code (plugin.check_independence).
"""
from __future__ import annotations

import re
import sqlite3

from c2_kit import skin as K
from c2_kit import slots as S
from c2_kit.cards import split_rules

DAY = ("count", (("unit", ("day", "days")),))
CENTS = ("cents", (("currency", "USD"), ("symbol", "$")))
DATE = ("date", ())
CLOSED = "The two versions and the case record are complete: no other rule or fact applies."
NONE_CELL = "(none)"
ROLE_OF = ("pos", "alt", "neg")
TABLE_KIND = {"Time limit": ("win",), "Amount rule": ("amt",), "Exclusion": ("exc",), "Condition rule": ("alt",),
              "Special time limit": ("ovc", "ovd")}
ANSWER = {"yn_changes": lambda a, b: 1 if a != b else 0, "yn_dneg": lambda a, b: 1 if a != b else 0,
          "yn_same": lambda a, b: 1 if a == b else 0, "yn_not_change": lambda a, b: 1 if a == b else 0,
          "yn_fail_change": lambda a, b: 1 if a == b else 0, "ch_v2": lambda a, b: b}

_W = r"[a-z][a-z' -]*[a-z]"
_OUT = (r"(?P<neg>" + _W + r") if the case's category is excluded, the request is late, or the case fails a rule on the"
        r" (?P<amount>" + _W + r"); otherwise (?P<alt>" + _W + r") if a clause gives (?P=alt) for the case's condition;"
        r" otherwise (?P<pos>" + _W + r")\.\n")
_LISTS = r"- Categories: (?P<cats>[^\n]+?)\. Conditions: (?P<conds>[^\n]+?)\.\n"
CARD_RE = re.compile(                                     # the full style (85% of rows)
    r"Apply each version of the (?P<title>" + _W + r") to the case on its own\.\n"
    r"- The outcome under each version is " + _OUT +
    r"- A special time-limit clause replaces only the limit, for cases in its category or whose date it names lies in"
    r" its window \(both end dates included\)\.\n"
    r"- Day counts are calendar days from the date named in the time-limit clause \(day zero\), printed in the"
    r" record\. Late means a day count above the limit\.\n" + _LISTS + re.escape(CLOSED))
CARD_SHORT_RE = re.compile(                               # the short style (15% of rows): no title line
    r"- Outcome under each version: " + _OUT +
    r"- A special time-limit clause replaces only the limit, for its category or for cases whose date it names lies in"
    r" its window \(both end dates included\)\.\n"
    r"- Late means the day count \(calendar days from the date named in the time-limit clause, day zero, printed in"
    r" the record\) is above the limit\.\n" + _LISTS + re.escape(CLOSED))
RECORD_RE = re.compile(
    r"Case record (?P<id>[^\s:]+):\n- category: (?P<cat>[^\n]+)\n- condition: (?P<cond>[^\n]+)\n"
    r"- (?P<alab>" + _W + r"): (?P<amount>[^\n]+)\n- (?P<f1>" + _W + r"): (?P<d1>[^\n]+)\n"
    r"- (?P<f2>" + _W + r"): (?P<d2>[^\n]+)\n- request date: (?P<req>[^\n]+)\n"
    r"- days from the (?P=f1) to the request date: (?P<k1>[^\n]+)\n"
    r"- days from the (?P=f2) to the request date: (?P<k2>[^\n]+)")
H_ORIG = re.compile(r"(?P<t>" + _W + r"), original version:", re.I)
H_REV = re.compile(r"(?P<t>" + _W + r"), revised version:", re.I)
H_UPD_ORIG = re.compile(r"Original version of the (?P<t>" + _W + r") \(before the update\):")
H_UPD_REV = re.compile(r"Revised version of the (?P<t>" + _W + r") \(after the update\):")
H_TABLE = re.compile(r"(?P<t>" + _W + r"), original and revised versions side by side:", re.I)
H_EDITS = "Edits made in the revised version:"
CELLS_RE = re.compile(r"\| (?P<label>[A-Z][a-z ]+) \| (?P<a>[^|\n]+) \| (?P<b>[^|\n]+) \|")

OUTCOME_SQL = """
SELECT CASE
  WHEN EXISTS (SELECT 1 FROM clause c WHERE c.ver = :v AND c.kind = 'exc' AND c.cat = f.cat) THEN 'neg'
  WHEN julianday(f.req) - julianday(CASE w.field WHEN f.f1 THEN f.d1 WHEN f.f2 THEN f.d2 END) >
       COALESCE((SELECT c.n FROM clause c WHERE c.ver = :v AND c.kind = 'ovc' AND c.cat = f.cat),
                (SELECT c.n FROM clause c WHERE c.ver = :v AND c.kind = 'ovd'
                   AND julianday(CASE c.field WHEN f.f1 THEN f.d1 WHEN f.f2 THEN f.d2 END)
                       BETWEEN julianday(c.s) AND julianday(c.e)),
                w.n) THEN 'neg'
  WHEN EXISTS (SELECT 1 FROM clause c WHERE c.ver = :v AND c.kind = 'amt' AND NOT (CASE c.op
         WHEN 'ge' THEN f.amount >= c.x WHEN 'gt' THEN f.amount > c.x
         WHEN 'le' THEN f.amount <= c.x WHEN 'lt' THEN f.amount < c.x END)) THEN 'neg'
  WHEN EXISTS (SELECT 1 FROM clause c WHERE c.ver = :v AND c.kind = 'alt' AND c.cond = f.cond) THEN 'alt'
  ELSE 'pos' END
FROM fact f JOIN clause w ON w.ver = :v AND w.kind = 'win'
"""
DAYS_SQL = "SELECT julianday(req) - julianday(d1), julianday(req) - julianday(d2) FROM fact"


class ParseError(ValueError):
    pass


def _split_list(text: str) -> list:
    head, sep, last = text.rpartition(" and ")
    if not sep:
        return [text]
    return head.split(", ") + [last]


def _cat_schema(surfaces) -> tuple:
    return ("category", (("surfaces", tuple(sorted((s, (s,)) for s in surfaces))),))


def _clause(text: str, ctx, schema: dict, voc: dict) -> tuple:
    """(kind, params) of one clause line, read through the lexicon (admitted forms only) and checked against the
    card's closed sets."""
    sem, _form, vals = ctx.lexicon.parse_exact(text, schema, admitted_only=True)

    def need(ok, what):
        if not ok:
            raise ParseError(f"{what} in clause {text!r}")

    if sem == "t24.win":
        need(vals["A"] in voc["fields"], "time-limit date")
        return "win", {"n": vals["N"], "anchor": vals["A"]}
    if sem.startswith("t24.amt."):
        op = sem.rsplit(".", 1)[1]
        need(op in ("ge", "gt", "le", "lt") and vals["M"] == voc["amount"], "amount rule")
        return "amt", {"op": op, "x": vals["X"], "label": vals["M"]}
    if sem == "t24.exc":
        need(vals["C"] in voc["cats"], "excluded category")
        return "exc", {"cat": vals["C"]}
    if sem == "t24.alt":
        need(vals["K"] in voc["conds"] and vals["O"] == voc["outcomes"][1], "condition clause")
        return "alt", {"cond": vals["K"], "outcome": vals["O"]}
    if sem == "t24.ovc":
        need(vals["C"] in voc["cats"], "special category")
        return "ovc", {"cat": vals["C"], "n": vals["N"]}
    if sem == "t24.ovd":
        need(vals["A"] in voc["fields"] and vals["S"] <= vals["E"], "special date window")
        return "ovd", {"field": vals["A"], "start": vals["S"].isoformat(), "end": vals["E"].isoformat(),
                       "n": vals["N"]}
    raise ParseError(f"clause meaning {sem} is not a T24 clause")


def _version(clauses: list) -> dict:
    out: dict = {}
    for kind, params in clauses:
        if kind in out:
            raise ParseError(f"two {kind} clauses in one version")
        out[kind] = params
    if "win" not in out or ("ovc" in out and "ovd" in out):
        raise ParseError("a version needs one time-limit clause and at most one special time limit")
    return out


def _bullets(lines: list, ctx, schema, voc) -> list:
    out = []
    for ln in lines:
        m = re.fullmatch(r"- (?P<c>.+)\.", ln)
        if not m:
            raise ParseError(f"bullet clause line expected: {ln!r}")
        out.append(_clause(m["c"], ctx, schema, voc))
    return out


def _record(block: str, cats: list, conds: list) -> dict:
    m = RECORD_RE.fullmatch(block)
    if not m:
        raise ParseError("case record does not match the G0 layout")
    if m["cat"] not in cats or m["cond"] not in conds:
        raise ParseError("record category or condition is outside the card's lists")
    return {"case_id": S.parse("id", m["id"]), "category": m["cat"], "condition": m["cond"],
            "amount_label": m["alab"], "amount": S.parse("cents", m["amount"], CENTS[1]),
            "date_fields": [m["f1"], m["f2"]], "d1": S.parse("date", m["d1"]).isoformat(),
            "d2": S.parse("date", m["d2"]).isoformat(), "req": S.parse("date", m["req"]).isoformat(),
            "days1": S.parse("count", m["k1"], DAY[1]), "days2": S.parse("count", m["k2"], DAY[1])}


def parse(row: dict, ctx) -> dict:
    card, question = split_rules(row)
    cm = CARD_RE.fullmatch(card) or CARD_SHORT_RE.fullmatch(card)
    if not cm:
        raise ParseError("card does not match the G0 wording")
    title = cm.groupdict().get("title")             # None on the short style: the version headers name the policy
    cats, conds = _split_list(cm["cats"]), _split_list(cm["conds"])
    outcomes = [cm["pos"], cm["alt"], cm["neg"]]
    if len(set(outcomes)) != 3 or len(set(cats)) != len(cats) or len(set(conds)) != len(conds):
        raise ParseError("card lists repeat a name")
    blocks = row["state"].split("\n\n")
    rec_blocks = [b for b in blocks if b.startswith("Case record ")]
    if len(rec_blocks) != 1:
        raise ParseError(f"{len(rec_blocks)} case records")
    rec = _record(rec_blocks[0], cats, conds)
    if rec["amount_label"] != cm["amount"]:
        raise ParseError("record amount field differs from the card's")
    voc = {"cats": cats, "conds": conds, "outcomes": outcomes, "fields": rec["date_fields"], "amount": cm["amount"]}
    schema = {"cat": _cat_schema(cats), "cond": _cat_schema(conds), "field": _cat_schema(rec["date_fields"]),
              "label": _cat_schema([cm["amount"]]), "out": _cat_schema(outcomes), "n": DAY, "x": CENTS, "d": DATE}
    v1 = v2 = None
    narrative = []
    titles = set()
    i = 0
    while i < len(blocks):
        b = blocks[i]
        head, _, body = b.partition("\n")
        lines = body.split("\n") if body else []
        if b is rec_blocks[0]:
            i += 1
            continue
        if (m := H_ORIG.fullmatch(head) or H_UPD_ORIG.fullmatch(head)) and v1 is None:
            titles.add(m["t"].lower())
            v1_lines = lines
            v1 = _version(_bullets(lines, ctx, schema, voc))
            if i + 1 < len(blocks) and blocks[i + 1].startswith(H_EDITS + "\n"):
                v2 = _apply_edits(v1_lines, blocks[i + 1].split("\n")[1:], ctx, schema, voc)
                i += 1
        elif (m := H_REV.fullmatch(head) or H_UPD_REV.fullmatch(head)) and v2 is None:
            titles.add(m["t"].lower())
            v2 = _version(_bullets(lines, ctx, schema, voc))
        elif (m := H_TABLE.fullmatch(head)) and v1 is None and v2 is None:
            titles.add(m["t"].lower())
            v1, v2 = _table(lines, ctx, schema, voc)
        else:
            narrative.append(b)
        i += 1
    if v1 is None or v2 is None or len(narrative) != 1 or len(titles) != 1 or (title and titles != {title}):
        raise ParseError("state blocks: need both versions under one title (the card's), one record and one "
                         "narrative")
    title = title or next(iter(titles))
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    told = {}
    if skin.author_mode == "T":
        sch = {"CUSTOMER": ("name", ()), "CASE_ID": ("id", ()), "CAT": _cat_schema(cats), "COND": _cat_schema(conds),
               "AMOUNT": CENTS, "D1": DATE, "D2": DATE, "REQ": DATE}
        told = K.parse_skin(skin, narrative[0], sch)
        if "CUSTOMER" not in told:
            raise ParseError("narrative skin lacks the customer")
        record_view = {"CASE_ID": rec["case_id"], "CAT": rec["category"], "COND": rec["condition"],
                       "AMOUNT": rec["amount"], "D1": rec["d1"], "D2": rec["d2"], "REQ": rec["req"]}
        for k, v in told.items():
            if k in record_view and record_view[k] != v:
                raise ParseError(f"{k} reads {v!r} in the narrative but {record_view[k]!r} in the record")
    wording = ctx.skin(row["meta"]["wording_id"])
    K.match_template(wording.text, question, {})
    view = {"title": title, "vocab": {"cats": cats, "conds": conds, "outcomes": outcomes}, "v1": v1, "v2": v2,
            "case": rec, "qform": wording.qform}
    if skin.author_mode == "T":
        view["customer"] = told["CUSTOMER"]
    if row["qtype"] == "choice":
        if wording.qform != "ch_v2":
            raise ParseError(f"choice row with question {wording.qform}")
        role = dict(zip(outcomes, ROLE_OF))
        if any(t not in role for t in row["options"]):
            raise ParseError("an option is not one of the card's outcomes")
        view["options"] = [role[t] for t in row["options"]]
    return view


def _apply_edits(v1_lines: list, edit_lines: list, ctx, schema, voc) -> dict:
    """The revised version = the original lines minus the removed ones plus the added ones."""
    kept = list(v1_lines)
    added = []
    if not edit_lines:
        raise ParseError("empty edit list")
    for ln in edit_lines:
        m = re.fullmatch(r"(?P<op>removed|added): (?P<c>.+)\.", ln)
        if not m:
            raise ParseError(f"edit line expected: {ln!r}")
        if m["op"] == "removed":
            if f"- {m['c']}." not in kept:
                raise ParseError("a removed line is not in the original version")
            kept.remove(f"- {m['c']}.")
        else:
            added.append(f"- {m['c']}.")
    return _version(_bullets(kept + added, ctx, schema, voc))


def _table(lines: list, ctx, schema, voc) -> tuple:
    if lines[:2] != ["| Clause | Original version | Revised version |", "| --- | --- | --- |"]:
        raise ParseError("table header")
    a, b = [], []
    for ln in lines[2:]:
        m = CELLS_RE.fullmatch(ln)
        if not m or m["label"] not in TABLE_KIND:
            raise ParseError(f"table row {ln!r}")
        for cell, out in ((m["a"], a), (m["b"], b)):
            if cell == NONE_CELL:
                continue
            kind, params = _clause(cell, ctx, schema, voc)
            if kind not in TABLE_KIND[m["label"]]:
                raise ParseError(f"a {kind} clause in the {m['label']!r} row")
            out.append((kind, params))
    return _version(a), _version(b)


def solve_b(view: dict):
    c = view["case"]
    db = sqlite3.connect(":memory:")
    try:
        db.execute("CREATE TABLE fact (cat TEXT, cond TEXT, amount INTEGER, f1 TEXT, f2 TEXT, d1 TEXT, d2 TEXT,"
                   " req TEXT)")
        db.execute("INSERT INTO fact VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (c["category"], c["condition"], c["amount"], c["date_fields"][0], c["date_fields"][1], c["d1"],
                    c["d2"], c["req"]))
        k1, k2 = db.execute(DAYS_SQL).fetchone()
        if (k1, k2) != (c["days1"], c["days2"]) or k2 < 0 or k1 < k2:
            raise ParseError("the printed day counts disagree with the dates")
        db.execute("CREATE TABLE clause (ver INTEGER, kind TEXT, op TEXT, cat TEXT, cond TEXT, n INTEGER,"
                   " field TEXT, x INTEGER, s TEXT, e TEXT)")
        for ver in (1, 2):
            for kind, p in view[f"v{ver}"].items():
                db.execute("INSERT INTO clause VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (ver, kind, p.get("op"), p.get("cat"), p.get("cond"), p.get("n"),
                            p.get("anchor", p.get("field")), p.get("x"), p.get("start"), p.get("end")))
        got = [db.execute(OUTCOME_SQL, {"v": ver}).fetchall() for ver in (1, 2)]
    finally:
        db.close()
    if any(len(g) != 1 or g[0][0] not in ROLE_OF for g in got):
        raise ParseError("a version does not decide exactly one outcome")
    return ANSWER[view["qform"]](got[0][0][0], got[1][0][0])
