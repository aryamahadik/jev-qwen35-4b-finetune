"""families/T30/solver_b.py: T30 solver B, written from G0_SPEC.md (not from plugin.py).

parse(row, ctx) reads the RENDERED row back into the canonical facts with this module's own readers:
  - the rule card (row.card on yes/no rows, the head of the instructions on choice rows: cards.split_rules) by one
    regular expression of the G0 card wording: the noun,
    the match and key labels, the letter-case rule, the two quoted action lists, the batch limit (a count);
  - the listing block (the state block whose header starts "Search results for") in its container: bullet lines,
    markdown table, JSON or CSV; the S4 preamble and an attached note line are recognised and skipped; a key written
    in backticks is read without them; dates are read by slots.parse in any date form;
  - the request block through skin.parse_skin, with a schema built from the card (USER and REF are names, ACTION is
    a category whose surfaces are the card's six action phrases);
  - the question through its wording template; on choice rows every option text back to its key.
solve_b(view) loads the entries and the action table into an in-memory sqlite database. The distinct matches are a
GROUP BY over the normalised key (lower() for the fold rule) of the rows whose name equals the request's name under
binary collation (exact names); the consequence class is a lookup in the action table read from the card; the step is
one SQL CASE expression. Imports no solver-A code (plugin.check_independence).
"""
from __future__ import annotations

import json
import re
import sqlite3

from c2_kit import cards
from c2_kit import skin as K
from c2_kit import slots as S

NORM_OF = {"with upper and lower case treated as the same": "fold",
           "with upper and lower case treated as different": "exact"}
STEP_OF_OPTION = {"Go ahead without asking the user": "proceed", "Ask the user which one is meant": "ask",
                  "Stop and tell the user nothing matched": "stop"}
NO_SINGLE = "No single entry: none or several distinct matches"
NOTE = "Note attached to the results: "
PREAMBLE = ("Agent step: searching the records for the name in the request.", "Tool output:")
CLOSED = "The search results are complete; only these rules decide what the agent does."
CHOICE_FORMS = ("ch_next", "ch_target")
ANSWER = {"yn_proceed": lambda step: int(step == "proceed"), "yn_no_hold": lambda step: int(step == "proceed"),
          "yn_hold": lambda step: int(step != "proceed"), "yn_not_proceed": lambda step: int(step != "proceed"),
          "yn_ask": lambda step: int(step == "ask"), "yn_settle": lambda step: int(step != "ask")}

_LBL = r"[a-z][a-z ]*[a-z]"
_Q3 = r'"[^"\n]+", "[^"\n]+" and "[^"\n]+"'
CARD_RE = re.compile(
    r"Rules for a request that names an? (?P<noun>" + _LBL + r"):\n"
    r"- Match: an entry matches only if its (?P<match>" + _LBL + r") is exactly the name in the request, letter for"
    r" letter; nicknames, short or long forms and spelling variants do not\.\n"
    r"- Identity: entries with identical (?P<key>" + _LBL + r") values, (?P<norm>with upper and lower case"
    r" treated as (?:the same|different)), are one (?P=noun); entries with different (?P=key) values"
    r" are different (?P<pl>" + _LBL + r"), whatever their other fields say\.\n"
    r"- Consequence: low-consequence: (?P<low>" + _Q3 + r")\. Consequential: (?P<cons>" + _Q3 + r")\.\n"
    r"- Decision: no distinct match: stop and tell the user nothing matched\. Exactly one distinct match: go ahead,"
    r" whatever the action\. Two or more distinct matches: consequential action: ask the user which one is meant;"
    r" low-consequence action: go ahead on all of them if there are at most (?P<limit>[^,\n]+?) distinct matches,"
    r" otherwise ask\.\n"
    r"- Dates never change the decision\.\n" + re.escape(CLOSED))
TRIPLE_RE = re.compile(r'"([^"\n]+)", "([^"\n]+)" and "([^"\n]+)"')
HEADER_RE = re.compile(r"Search results for (?P<pl>" + _LBL + r")(?P<tail>, in the order the tool returned them:"
                       r"| \(JSON\):| \(CSV\):|:)")
STYLE_OF_TAIL = {", in the order the tool returned them:": "lines", " (JSON):": "json", " (CSV):": "csv",
                 ":": "table"}


class ParseError(ValueError):
    pass


def _key_text(v: str) -> str:
    """A key as listed: the glob code form wraps it in backticks."""
    return v[1:-1] if len(v) > 2 and v[0] == "`" and v[-1] == "`" else v


def _cells_lines(body: list) -> tuple:
    labels, rows = None, []
    for ln in body:
        if not ln.startswith("- "):
            raise ParseError(f"bullet line expected: {ln!r}")
        pairs = [p.split(": ", 1) for p in ln[2:].split("; ")]
        if len(pairs) != 4 or any(len(p) != 2 for p in pairs):
            raise ParseError(f"bullet line needs four 'label: value' fields: {ln!r}")
        lab = tuple(p[0] for p in pairs)
        if labels is not None and lab != labels:
            raise ParseError("bullet lines disagree on their labels")
        labels = lab
        rows.append([p[1] for p in pairs])
    return labels, rows


def _cells_table(body: list) -> tuple:
    def cells(ln):
        if not (ln.startswith("| ") and ln.endswith(" |")):
            raise ParseError(f"table row expected: {ln!r}")
        return ln[2:-2].split(" | ")
    if len(body) < 3 or cells(body[1]) != ["---"] * 4:
        raise ParseError("table needs a header, a rule and rows")
    labels = tuple(cells(body[0]))
    rows = [cells(ln) for ln in body[2:]]
    if len(labels) != 4 or any(len(r) != 4 for r in rows):
        raise ParseError("table rows need four cells")
    return labels, rows


def _cells_json(body: list) -> tuple:
    if len(body) != 1:
        raise ParseError("the JSON listing is one line")
    obj = json.loads(body[0])
    if set(obj) != {"results"} or not obj["results"]:
        raise ParseError("JSON listing: one non-empty 'results' array")
    keys = tuple(obj["results"][0])
    if len(keys) != 4 or any(tuple(o) != keys for o in obj["results"]):
        raise ParseError("JSON entries need the same four fields")
    if any(not isinstance(o[k], str) for o in obj["results"] for k in keys):
        raise ParseError("JSON listing values are strings")
    return tuple(k.replace("_", " ") for k in keys), [[o[k] for k in keys] for o in obj["results"]]


def _cells_csv(body: list) -> tuple:
    rows = [ln.split(",") for ln in body]
    if len(rows) < 2 or any(len(r) != 4 for r in rows):
        raise ParseError("CSV listing: a header and rows of four fields")
    return tuple(rows[0]), rows[1:]


READERS = {"lines": _cells_lines, "table": _cells_table, "json": _cells_json, "csv": _cells_csv}


def _listing_lines(block: str) -> list:
    """The block's lines from the listing header on (the S4 preamble skipped)."""
    lines = block.split("\n")
    return lines[2:] if tuple(lines[:2]) == PREAMBLE else lines


def _read_listing(block: str) -> tuple:
    lines = _listing_lines(block)
    h = HEADER_RE.fullmatch(lines[0]) if lines else None
    if not h:
        raise ParseError("listing header not found")
    body = lines[1:]
    if body and body[-1].startswith(NOTE):
        body = body[:-1]                         # an attached note never changes a fact
    labels, rows = READERS[STYLE_OF_TAIL[h["tail"]]](body)
    entries = []
    for name, detail, key, seen in rows:
        if not name or not detail or not key:
            raise ParseError("empty listing value")
        entries.append([name, detail, _key_text(key), S.parse("date", seen).isoformat()])
    return h["pl"], list(labels), entries


def _split_state(state: str) -> tuple:
    blocks = state.split("\n\n")
    if len(blocks) != 2:
        raise ParseError(f"the state holds {len(blocks)} blocks (request and listing expected)")
    is_list = [bool(HEADER_RE.fullmatch(_listing_lines(b)[0])) for b in blocks]
    if is_list.count(True) != 1:
        raise ParseError("exactly one listing block expected")
    i = is_list.index(True)
    return blocks[1 - i], blocks[i]


def parse(row: dict, ctx) -> dict:
    request, listing = _split_state(row["state"])
    rule, question = cards.split_rules(row)         # yes/no rows: row.card + the question; choice rows: both in the
    if not rule or not question:                    # instructions, split at the blank line before the question
        raise ParseError("rule card and question are not separated")
    c = CARD_RE.fullmatch(rule)
    if not c:
        raise ParseError("rule card does not match the G0 wording")
    low, cons = TRIPLE_RE.fullmatch(c["low"]), TRIPLE_RE.fullmatch(c["cons"])
    if not low or not cons:
        raise ParseError("action lists are not three quoted phrases")
    low, cons = list(low.groups()), list(cons.groups())
    if len(set(low + cons)) != 6:
        raise ParseError("an action phrase is listed twice")
    pl, labels, entries = _read_listing(listing)
    if pl != c["pl"] or labels[0] != c["match"] or labels[2] != c["key"]:
        raise ParseError("the listing and the card name different fields")
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    if skin.author_mode != "T":
        raise ParseError("T30 rows carry Mode T skins only")
    schema = {"USER": ("name", ()), "REF": ("name", ()),
              "ACTION": ("category", (("surfaces", tuple(sorted((p, (p,)) for p in low + cons))),))}
    told = K.parse_skin(skin, request, schema)
    if set(told) != {"USER", "REF", "ACTION"}:
        raise ParseError(f"the request skin carries {sorted(told)}")
    wording = ctx.skin(row["meta"]["wording_id"])
    K.match_template(wording.text, question, {})
    qform = wording.qform
    if (row["qtype"] == "choice") != (qform in CHOICE_FORMS):
        raise ParseError("question form and row type disagree")
    view = {"noun": c["noun"], "noun_pl": pl, "labels": labels, "low_actions": low, "cons_actions": cons,
            "norm": NORM_OF[c["norm"]], "batch_max": S.parse("count", c["limit"]), "user": told["USER"],
            "ref": told["REF"], "action": told["ACTION"], "entries": entries, "qform": qform}
    if row["qtype"] == "choice":
        view["options"] = [_option_key(qform, t, view) for t in row["options"]]
    return view


def _option_key(qform: str, text: str, view: dict):
    if qform == "ch_next":
        if text not in STEP_OF_OPTION:
            raise ParseError(f"unknown step option {text!r}")
        return STEP_OF_OPTION[text]
    if text == NO_SINGLE:
        return "none"
    if text not in {e[2] for e in view["entries"]}:
        raise ParseError(f"option {text!r} is no listed key")
    return text.lower() if view["norm"] == "fold" else text


STEP_SQL = """
WITH matched AS (SELECT CASE WHEN :fold = 1 THEN lower(key) ELSE key END AS ident FROM entry WHERE name = :ref),
     distinct_ids AS (SELECT ident FROM matched GROUP BY ident),
     cls AS (SELECT class FROM action WHERE phrase = :action)
SELECT (SELECT COUNT(*) FROM distinct_ids),
       (SELECT MIN(ident) FROM distinct_ids),
       (SELECT COUNT(*) FROM cls),
       CASE WHEN (SELECT COUNT(*) FROM distinct_ids) = 0 THEN 'stop'
            WHEN (SELECT COUNT(*) FROM distinct_ids) = 1 THEN 'proceed'
            WHEN (SELECT class FROM cls) = 'consequential' THEN 'ask'
            WHEN (SELECT COUNT(*) FROM distinct_ids) <= :limit THEN 'proceed'
            ELSE 'ask' END
"""


def solve_b(view: dict):
    keys = [e[2] for e in view["entries"]]
    if not all(k.isascii() for k in keys) or not view["ref"].isascii():
        raise ParseError("sqlite lower() folds ASCII only")
    con = sqlite3.connect(":memory:")
    try:
        con.execute("CREATE TABLE entry (pos INTEGER PRIMARY KEY, name TEXT NOT NULL, key TEXT NOT NULL)")
        con.executemany("INSERT INTO entry VALUES (?, ?, ?)", [(i, e[0], e[2]) for i, e in enumerate(view["entries"])])
        con.execute("CREATE TABLE action (phrase TEXT PRIMARY KEY, class TEXT NOT NULL)")
        con.executemany("INSERT INTO action VALUES (?, 'low')", [(p,) for p in view["low_actions"]])
        con.executemany("INSERT INTO action VALUES (?, 'consequential')", [(p,) for p in view["cons_actions"]])
        n, only, n_cls, step = con.execute(STEP_SQL, {"fold": 1 if view["norm"] == "fold" else 0,
                                                      "ref": view["ref"], "action": view["action"],
                                                      "limit": view["batch_max"]}).fetchone()
    finally:
        con.close()
    if n_cls != 1:
        raise ParseError("the requested action is not in the card's table")
    if view["qform"] == "ch_target":
        return only if n == 1 else "none"
    if view["qform"] == "ch_next":
        return step
    return ANSWER[view["qform"]](step)
