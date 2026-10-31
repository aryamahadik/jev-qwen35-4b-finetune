"""families/T23/solver_b.py: T23 solver B, written from G0_SPEC.md (sections 1, 1.1, 1.2, 7), not from plugin.py.

parse(row, ctx) reads the RENDERED row back into the canonical facts:
  - the version block (list, table or log) and the case record line by line with this module's own regular
    expressions; every date by slots.parse; every term, quantity and claim by a typed amount reader (integer cents,
    day counts or device counts: exactly one reading, one kind per row);
  - the rules (row.card on a yes/no row, the head of the instructions on a choice row: cards.split_rules) by full
    match against this module's own copy of the G0 v4 card lines (skin.match_template over its name slots); which
    lines the card must hold follows from the parsed record and question (a clause line pair only when the record
    prints a clause, the within line on an outcome question, the claim line on a claim question). It fixes the
    anchor role and the window rule;
  - the narrative skin (Mode T) through skin.parse_skin; Mode F narrative facts are left to G3-H;
  - the question through its wording template (its admitted meaning is the question form);
  - on choice rows, every option text back to its key (a version id or a term value).
  It refuses a malformed record: the "replaces" chain must follow start-date order, printed ends must tile the
  windows (incl: end + 1 day = next start; excl: end = next start), the list / table head's end-date marker must
  agree with the card's window rule, the case dates must be ordered and on or after the first start, a printed day
  count must equal its date difference (the pair is read from the label "day count from A to B", A and B two case
  date labels without " date": G0 section 7), and a clause must name a real version, its own threshold (keep-old,
  retro) and the version that replaces it (sunset).
solve_b(view) loads the versions and case dates into an in-memory sqlite database. A SQL window filter on julianday
(printed end + 1 under incl; under the chain rule the start of the version whose "replaces" names it, by a self-join)
gives the default version; the clause is a separately coded rule over SQL date comparisons; every version gets a
governs flag ((default and not released) or pulled), and exactly one must hold. Imports no solver-A code
(plugin.check_independence).
"""
from __future__ import annotations

import datetime as dt
import re
import sqlite3

from c2_kit import cards as CARDS
from c2_kit import skin as K
from c2_kit import slots as S

CENTS = (("currency", "USD"), ("symbol", "$"))
AMOUNT_KINDS = (("cents", "cents", CENTS), ("days", "count", (("unit", ("day", "days")),)),
                ("devices", "count", (("unit", ("device", "devices")),)))
ROLES = ("purchase", "event", "filing", "decision")
NARRATIVE = {"CUSTOMER": ("name", ()), "ORG": ("name", ()), "ITEM": ("name", ()), "CASE_ID": ("id", ())}
QUESTION = {"CASE_ID": ("id", ()), "DOC": ("name", ()), "TERM_LABEL": ("name", ()), "CANDIDATE": ("id", ())}
CARD_SLOTS = {"DOC": ("name", ()), "ANCHOR": ("name", ()), "TERM_LABEL": ("name", ()), "QTY_LABEL": ("name", ())}
# G0 section 7: a printed day count is labelled "day count from A to B", A and B two case date labels without their
# trailing " date"; the count is B's date minus A's date in calendar days
DAY_COUNT_HEAD = "day count from "
# G0 1.2: the list / table head marks every printed end date as included (incl) or excluded (excl)
END_WORD = {"incl": "included", "excl": "excluded"}
# question form -> (predicate, asks the positive side)
FORMS = {"ch_version": (None, True), "ch_term": (None, True),
         "yn_version": ("version", True), "yn_version_other": ("version", False), "yn_version_not": ("version", False),
         "yn_claim": ("claim", True), "yn_claim_contra": ("claim", False), "yn_claim_not": ("claim", False),
         "yn_outcome": ("within", True), "yn_outcome_out": ("within", False), "yn_outcome_not": ("within", False)}

# G0 1.1: the card text, copied from the spec (exact)
_CW = ("Only the listed versions, clauses and case facts count, and they are complete: no other version, "
       "clause or fact exists.")
_WINDOWS = {
    "incl": "A version is in force from its start date through its end date, both dates included; an open-ended "
            "version stays in force.",
    "excl": "A version is in force from its start date through the day before its end date; an open-ended version "
            "stays in force.",
    "chain": "A version is in force from its start date until the version that replaces it takes effect, and on that "
             "start date the new version is in force.",
}
_TITLE = "Finding the version of the {DOC} that governs a case:"
_DEFAULT = "- The governing version is the version in force on the case's {ANCHOR}."
_DEFAULT_CLAUSE = ("- Default: the version in force on the case's {ANCHOR}; \"would govern\" in a clause means this "
                   "default.")
_CLAUSE_LINES = (
    "- At most one clause is printed: when its own condition holds, the version it points to governs, even if "
    "another version is in force on a later date; it is applied once, after the default.",
    "- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or "
    "before\" and \"on or after\" include it.")
_WITHIN = ("- The case is within the {TERM_LABEL} when its {QTY_LABEL} is at most the governing version's value, and "
           "outside it otherwise.")
_CLAIM = ("- A claim about the {TERM_LABEL} is supported when it states the governing version's value, and "
          "contradicted otherwise.")


def _card_template(window_text: str, has_clause: bool, outcome: bool, claim: bool) -> str:
    """G0 v4 1.1: the card this module expects for a record (full-matched, line by line, in this order)."""
    lines = [_TITLE, _DEFAULT_CLAUSE if has_clause else _DEFAULT, "- " + window_text]
    if has_clause:
        lines += list(_CLAUSE_LINES)
    if outcome:
        lines.append(_WITHIN)
    if claim:
        lines.append(_CLAIM)
    lines.append(_CW)
    return "\n".join(lines)


STATE = re.compile(
    r"(?P<narr>.*?)\n\n(?:Versions of the (?P<d1>[^\n]+) \(end dates (?P<m1>included|excluded)\):|"
    r"Version table of the (?P<d2>[^\n]+) \(end dates (?P<m2>included|excluded)\):|"
    r"Change log of the (?P<d3>[^\n]+), newest entry first:)\n(?P<vbody>.*?)\n\nCase (?P<cid>[^\s:]+):\n"
    r"(?P<cbody>.*?)\nEnd of case record\.(?:\n\n(?P<tail>.+))?", re.S)
LIST_LINE = re.compile(r"- (?P<id>\S+): (?:first version|replaces (?P<rep>\S+)); in force from (?P<s>.+?)"
                       r"(?: to (?P<e>.+?)|, open-ended); (?P<tl>.+?): (?P<t>.+)\.")
TABLE_HEAD = re.compile(r"version \| replaces \| in force from \| in force to \| (?P<tl>.+)")
TABLE_ROW = re.compile(r"(?P<id>[^\s|]+) \| (?:first version|(?P<rep>[^\s|]+)) \| (?P<s>[^|]+) \| "
                       r"(?:open-ended|(?P<e>[^|]+)) \| (?P<t>[^|]+)")
LOG_LINE = re.compile(r"(?P<s>[^|]+) \| (?P<id>\S+) takes effect(?:, replacing (?P<rep>\S+)| as the first version) \| "
                      r"(?P<tl>.+?): (?P<t>.+)")
KEEP = re.compile(r"Transition clause of (?P<on>\S+): if (?P=on) would govern a case whose (?P<lab>.+?) is before "
                  r"(?P<d>.+?), the version in force on that (?P=lab) governs it instead\.")
RETRO = re.compile(r"Transition clause of (?P<on>\S+): if a version older than (?P=on) would govern a case whose "
                   r"(?P<lab>.+?) is on or after (?P<d>.+?), (?P=on) governs it instead\.")
SUNSET = re.compile(r"Sunset clause of (?P<on>\S+): if (?P=on) would govern a case whose (?P<lab>.+?) is after "
                    r"(?P<d>.+?), (?P<to>\S+) governs it instead\.")
CASE_LINE = re.compile(r"- (?P<lab>[^:\n]+): (?P<val>.+)")
CLAIM_LINE = re.compile(r"- claim to check: the (?P<tl>.+?) for this case is (?P<val>.+)")


class ParseError(ValueError):
    pass


# ------------------------------------------------------------------------------------------------ values

def _date(text: str) -> str:
    try:
        return S.parse("date", text.strip()).isoformat()
    except S.SlotError as e:
        raise ParseError(f"date {text!r}: {e}") from None


def _amount(text: str) -> tuple:
    """(kind, int): the one typed reading of a term, quantity or claim text."""
    hits = []
    for kind, slot_kind, params in AMOUNT_KINDS:
        try:
            hits.append((kind, S.parse(slot_kind, text.strip(), params)))
        except S.SlotError:
            continue
    if len(hits) != 1:
        raise ParseError(f"{text!r} reads as {len(hits)} amounts")
    return hits[0]


def _name(text: str) -> str:
    try:
        return S.parse("name", text)
    except S.SlotError as e:
        raise ParseError(f"name {text!r}: {e}") from None


def _ident(text: str) -> str:
    try:
        return S.parse("id", text)
    except S.SlotError as e:
        raise ParseError(f"id {text!r}: {e}") from None


def _julian(iso: str) -> int:
    return dt.date.fromisoformat(iso).toordinal()


def _day_pair(qty_label: str, labels: list):
    """(from index, to index) of the case dates a "day count from A to B" label names (A, B = two date labels without
    their trailing " date", A the earlier role), or None when the quantity is an input. Exactly one split must fit."""
    if not qty_label.startswith(DAY_COUNT_HEAD):
        return None
    names = [lab[:-len(" date")] if lab.endswith(" date") else None for lab in labels]
    rest, fits = qty_label[len(DAY_COUNT_HEAD):], []
    for m in re.finditer(" to ", rest):
        a, b = rest[:m.start()], rest[m.end():]
        if a in names and b in names:
            fits.append((names.index(a), names.index(b)))
    if len(fits) != 1 or fits[0][0] >= fits[0][1]:
        raise ParseError(f"day count label {qty_label!r} does not name two case dates, earlier first")
    return fits[0]


# ------------------------------------------------------------------------------------------------ blocks

def _clause(line: str):
    for kind, rx in (("keep_old", KEEP), ("retro", RETRO), ("sunset", SUNSET)):
        m = rx.fullmatch(line)
        if m:
            return {"kind": kind, "on": _ident(m["on"]), "label": _name(m["lab"]), "date": _date(m["d"]),
                    "to": _ident(m["to"]) if kind == "sunset" else (_ident(m["on"]) if kind == "retro" else None)}
    raise ParseError(f"unknown clause line {line!r}")


def _versions(body: str, style: str) -> tuple:
    """([version dicts in listed order], clause or None, term label, the clause's listed version or None)."""
    lines = body.split("\n")
    vers, clause, after, labels = [], None, None, set()
    if style == "table":
        m = TABLE_HEAD.fullmatch(lines[0])
        if not m:
            raise ParseError("table header")
        labels.add(_name(m["tl"]))
        lines = lines[1:]
    for i, line in enumerate(lines):
        if line.startswith(("Transition clause of ", "Sunset clause of ", "  ")):
            if clause is not None or not vers:
                raise ParseError("a second clause line, or a clause before any version")
            indented = line.startswith("  ")
            if indented == (style == "table") or (style == "table" and i != len(lines) - 1):
                raise ParseError("a clause is indented under its version (list, log) or after the table (table)")
            clause = _clause(line[2:] if indented else line)
            after = vers[-1]["id"] if style != "table" else None
            continue
        rx = {"list": LIST_LINE, "table": TABLE_ROW, "log": LOG_LINE}[style]
        m = rx.fullmatch(line)
        if not m:
            raise ParseError(f"version line {line!r}")
        if style != "table":
            labels.add(_name(m["tl"]))
        e = m["e"] if style != "log" else None
        vers.append({"id": _ident(m["id"]), "start": _date(m["s"]), "end": _date(e) if e else None,
                     "replaces": _ident(m["rep"]) if m["rep"] else None, "term": _amount(m["t"])})
    if len(labels) != 1:
        raise ParseError("the version lines name more than one term label")
    return vers, clause, labels.pop(), after


def _chronology(vers: list, window: str) -> list:
    """Versions in start order; the replaces chain and the printed ends must agree with it (G0 R2, R3)."""
    out = sorted(vers, key=lambda v: _julian(v["start"]))
    if len({v["start"] for v in out}) != len(out) or len({v["id"] for v in out}) != len(out):
        raise ParseError("two versions share a start date or an id")
    for i, v in enumerate(out):
        if v["replaces"] != (out[i - 1]["id"] if i else None):
            raise ParseError(f"{v['id']} does not replace the version before it")
        last = i == len(out) - 1
        if window == "chain":
            if v["end"] is not None:
                raise ParseError("a change-log version prints an end date")
            continue
        if last != (v["end"] is None):
            raise ParseError("only the newest version is open-ended")
        if not last:
            gap = _julian(out[i + 1]["start"]) - _julian(v["end"])
            if gap != (1 if window == "incl" else 0):
                raise ParseError(f"{v['id']}: printed end does not meet the next start under {window}")
    return out


def _rules_question(row: dict) -> tuple:
    """(rules, question): the rules sit in row.card on a yes/no row and at the head of the instructions on a choice row
    (cards.split_rules); the question is one paragraph."""
    if (row["qtype"] == "noul") != bool(row.get("card")):
        raise ParseError("the rules sit in row.card on yes/no rows and in the instructions on choice rows")
    rules, question = CARDS.split_rules(row)
    if not rules or not question or "\n\n" in question:
        raise ParseError("card and question are not separated")
    return rules, question


def _card(rules: str, has_clause: bool, outcome: bool, claim: bool) -> tuple:
    hits = []
    for window, text in _WINDOWS.items():
        try:
            got = K.match_template(_card_template(text, has_clause, outcome, claim), rules, CARD_SLOTS)
        except K.TemplateMismatch:
            continue
        hits.append((window, got))
    if len(hits) != 1:
        raise ParseError("the card does not match the G0 card text for this record and question")
    return hits[0]


# ------------------------------------------------------------------------------------------------ parse

def parse(row: dict, ctx) -> dict:
    m = STATE.fullmatch(row["state"])
    if not m:
        raise ParseError("the state does not have the narrative / versions / case layout")
    style = "list" if m["d1"] is not None else ("table" if m["d2"] is not None else "log")
    doc = _name(m["d1"] or m["d2"] or m["d3"])
    listed, clause, term_label, clause_after = _versions(m["vbody"], style)
    if style == "log" and [v["start"] for v in listed] != sorted((v["start"] for v in listed), reverse=True):
        raise ParseError("the change log is not newest first")
    if style != "log" and [v["start"] for v in listed] != sorted(v["start"] for v in listed):
        raise ParseError("the version list is not oldest first")
    rules, question = _rules_question(row)
    wording = ctx.skin(row["meta"]["wording_id"])
    qform = wording.qform
    if qform not in FORMS:
        raise ParseError(f"unknown question form {qform}")
    window, card = _card(rules, clause is not None, FORMS[qform][0] == "within", m["cbody"].count("\n") == 5)
    if (window == "chain") != (style == "log"):
        raise ParseError("the window rule does not fit the block style")
    if style != "log" and (m["m1"] or m["m2"]) != END_WORD[window]:
        raise ParseError("the block's end-date marker contradicts the card's window rule")
    vers = _chronology(listed, window)
    ids = [v["id"] for v in vers]
    # case record
    lines = m["cbody"].split("\n")
    if len(lines) not in (5, 6):
        raise ParseError("the case record has 5 or 6 lines")
    labels, dates = [], []
    for line in lines[:4]:
        c = CASE_LINE.fullmatch(line)
        if not c:
            raise ParseError(f"case line {line!r}")
        labels.append(_name(c["lab"]))
        dates.append(_date(c["val"]))
    q = CASE_LINE.fullmatch(lines[4])
    if not q:
        raise ParseError("quantity line")
    qty_label, qty = _name(q["lab"]), _amount(q["val"])
    claim = None
    if len(lines) == 6:
        c = CLAIM_LINE.fullmatch(lines[5])
        if not c or _name(c["tl"]) != term_label:
            raise ParseError("claim line")
        claim = _amount(c["val"])
    kinds = {v["term"][0] for v in vers} | {qty[0]} | ({claim[0]} if claim else set())
    if len(kinds) != 1:
        raise ParseError(f"terms, quantity and claim are of different kinds {sorted(kinds)}")
    if len(set(labels)) != 4:
        raise ParseError("case date labels repeat")
    if any(_julian(a) > _julian(b) for a, b in zip(dates, dates[1:])) or _julian(dates[0]) < _julian(vers[0]["start"]):
        raise ParseError("case dates out of order or before the first version")
    pair = _day_pair(qty_label, labels)
    if pair is not None:
        frm, to = pair
        if qty[0] != "days" or qty[1] != _julian(dates[to]) - _julian(dates[frm]):
            raise ParseError("the printed day count does not equal its date difference")
    # card against the records
    if (card["DOC"] != doc or card.get("TERM_LABEL", term_label) != term_label
            or card.get("QTY_LABEL", qty_label) != qty_label):
        raise ParseError("the card names another document, term or quantity")
    if card["ANCHOR"] not in labels[:3]:
        raise ParseError("the card's anchor is not a purchase, event or filing date label")
    anchor = ROLES[labels.index(card["ANCHOR"])]
    # clause
    out_clause = None
    if clause is not None:
        if clause["on"] not in ids or clause["label"] not in labels:
            raise ParseError("the clause names an unknown version or date")
        k = ids.index(clause["on"])
        role = ROLES[labels.index(clause["label"])]
        if style != "table" and clause_after != clause["on"]:
            raise ParseError("the clause is not printed under its own version")
        if clause["kind"] == "keep_old":
            if role not in ("purchase", "event") or k == 0 or clause["date"] != vers[k]["start"]:
                raise ParseError("keep-old clause: role, version or threshold")
        elif clause["kind"] == "retro":
            if role != "decision" or k == 0 or clause["date"] != vers[k]["start"]:
                raise ParseError("retroactive clause: role, version or threshold")
        else:
            if role != "decision" or k == len(vers) - 1 or clause["to"] != vers[k + 1]["id"]:
                raise ParseError("sunset clause: role or replacing version")
            nxt = vers[k + 2]["start"] if k + 2 < len(vers) else None
            if _julian(clause["date"]) < _julian(vers[k + 1]["start"]) or (nxt and clause["date"] >= nxt):
                raise ParseError("sunset date outside the replacing version's window")
        out_clause = {"kind": clause["kind"], "on": clause["on"], "role": role, "date": clause["date"],
                      "to": clause["to"]}
    # question
    asked = K.match_template(wording.text, question, QUESTION)
    if "CASE_ID" in asked and asked["CASE_ID"] != m["cid"]:
        raise ParseError("the question names another case")
    if "DOC" in asked and asked["DOC"] != doc or "TERM_LABEL" in asked and asked["TERM_LABEL"] != term_label:
        raise ParseError("the question names another document or term")
    pred = FORMS[qform][0]
    if (claim is not None) != (pred == "claim"):
        raise ParseError("a claim line appears exactly on claim questions")
    if pred == "version":
        if asked.get("CANDIDATE") not in ids:
            raise ParseError("the question names no listed version")
        quest = {"candidate": asked["CANDIDATE"]}
    elif pred == "claim":
        quest = {"claim": claim[1]}
    else:
        quest = {}
    # narrative
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    told = {}
    if skin.author_mode == "T":
        if not set(skin.decl) <= set(NARRATIVE):
            raise ParseError(f"skin declares slots outside {sorted(NARRATIVE)}")
        told = K.parse_skin(skin, m["narr"], NARRATIVE)
        if not {"CUSTOMER", "ORG", "ITEM"} <= set(told):
            raise ParseError("narrative lacks the customer, organisation or item")
        if "CASE_ID" in told and told["CASE_ID"] != m["cid"]:
            raise ParseError("the narrative names another case")
    view = {"qform": qform, "style": style, "window": window, "anchor": anchor, "doc": doc, "term_label": term_label,
            "qty_label": qty_label, "labels": labels,
            "versions": [{"id": v["id"], "start": v["start"], "end": v["end"], "replaces": v["replaces"],
                          "term": v["term"][1]} for v in vers],
            "clause": out_clause, "case": {"id": _ident(m["cid"]), "dates": dates, "qty": qty[1]},
            "question": quest}
    if skin.author_mode == "T":
        view.update(customer=told["CUSTOMER"], org=told["ORG"], item=told["ITEM"])
    if row["qtype"] == "choice":
        terms = {v["term"][1] for v in vers}
        kind = next(iter(kinds))
        keys = []
        for text in row["options"]:
            if qform == "ch_version":
                if text not in ids:
                    raise ParseError(f"option {text!r} is not a listed version")
                keys.append(text)
            elif qform == "ch_term":
                got = _amount(text)
                if got[0] != kind or got[1] not in terms:
                    raise ParseError(f"option {text!r} is not a listed term")
                keys.append(got[1])
            else:
                raise ParseError(f"question {qform} has no options")
        view["options"] = keys
    return view


# ------------------------------------------------------------------------------------------------ solve (sqlite)

_WINDOW_SQL = """
WITH win AS (
  SELECT v.vid AS vid, julianday(v.start) AS lo,
         CASE WHEN :chain = 1 THEN (SELECT julianday(r.start) FROM version r WHERE r.replaces = v.vid)
              WHEN v.finish IS NULL THEN NULL
              ELSE julianday(v.finish) + :pad END AS hi
  FROM version v)
SELECT w.vid FROM win w JOIN fact f ON f.role = :role
WHERE w.lo <= julianday(f.day) AND (w.hi IS NULL OR julianday(f.day) < w.hi)
"""


def _in_force(db, role: str, window: str) -> str:
    rows = db.execute(_WINDOW_SQL, {"chain": int(window == "chain"), "pad": int(window == "incl"),
                                    "role": role}).fetchall()
    if len(rows) != 1:
        raise ParseError(f"{len(rows)} versions are in force on the {role} date")
    return rows[0][0]


def _true(db, sql: str, args: tuple) -> bool:
    return bool(db.execute(sql, args).fetchone()[0])


def _governing(db, view: dict) -> str:
    default = _in_force(db, view["anchor"], view["window"])
    flags = {v["id"]: {"default": v["id"] == default, "released": False, "pulled": False} for v in view["versions"]}
    cl = view["clause"]
    if cl is not None:
        if cl["kind"] == "keep_old":
            if default == cl["on"] and _true(db, "SELECT julianday(day) < julianday(?) FROM fact WHERE role = ?",
                                              (cl["date"], cl["role"])):
                flags[default]["released"] = True
                flags[_in_force(db, cl["role"], view["window"])]["pulled"] = True
        elif cl["kind"] == "retro":
            older = _true(db, "SELECT julianday(a.start) < julianday(b.start) FROM version a, version b "
                              "WHERE a.vid = ? AND b.vid = ?", (default, cl["on"]))
            if older and _true(db, "SELECT julianday(day) >= julianday(?) FROM fact WHERE role = 'decision'",
                               (cl["date"],)):
                flags[default]["released"] = True
                flags[cl["to"]]["pulled"] = True
        elif default == cl["on"] and _true(db, "SELECT julianday(day) > julianday(?) FROM fact WHERE role = 'decision'",
                                           (cl["date"],)):
            flags[default]["released"] = True
            flags[cl["to"]]["pulled"] = True
    who = [vid for vid, f in flags.items() if (f["default"] and not f["released"]) or f["pulled"]]
    if len(who) != 1:
        raise ParseError(f"{len(who)} versions govern the case")
    return who[0]


def solve_b(view: dict):
    db = sqlite3.connect(":memory:")
    try:
        db.execute("CREATE TABLE version (vid TEXT PRIMARY KEY, start TEXT NOT NULL, finish TEXT, replaces TEXT, "
                   "term INTEGER NOT NULL)")
        db.executemany("INSERT INTO version VALUES (?, ?, ?, ?, ?)",
                       [(v["id"], v["start"], v["end"], v["replaces"], v["term"]) for v in view["versions"]])
        db.execute("CREATE TABLE fact (role TEXT PRIMARY KEY, day TEXT NOT NULL)")
        db.executemany("INSERT INTO fact VALUES (?, ?)", list(zip(ROLES, view["case"]["dates"])))
        gov = _governing(db, view)
        term = db.execute("SELECT term FROM version WHERE vid = ?", (gov,)).fetchone()[0]
        qform = view["qform"]
        pred, positive = FORMS[qform]
        if qform == "ch_version":
            return gov
        if qform == "ch_term":
            return term
        if pred == "version":
            ok = gov == view["question"]["candidate"]
        elif pred == "claim":
            ok = _true(db, "SELECT ? = ?", (term, view["question"]["claim"]))
        else:
            ok = _true(db, "SELECT ? <= ?", (view["case"]["qty"], term))
        return int(ok if positive else not ok)
    finally:
        db.close()
