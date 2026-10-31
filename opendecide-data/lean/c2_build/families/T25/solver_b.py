"""families/T25/solver_b.py: T25 solver B, written from G0_SPEC.md (sections 1, 1.1, 1.2 and 7), not from plugin.py.

parse(row, ctx) reads the RENDERED row back into the canonical facts:
  - the card by full match against this module's own copy of the G0 v4 card text (1.1): the attribute and the three tier
    names in their stated order (rank = position in that list). The rules are read where the row prints them
    (c2_kit.cards.split_rules): row.card on a yes/no row, the head of the instructions on a choice row;
  - the source block (list, table, excerpt or keyed layout, G0 1.2) line by line with this module's own regular
    expressions: id, name, tier name -> rank, date (slots.parse), origin and the stated value (exactly one typed
    reading: integer cents, a date, or a count with a G0 section 7 unit; one kind per row);
  - the claim line (yes/no rows) and the question through its wording template (its admitted meaning is the form);
  - the narrative skin (Mode T) through skin.parse_skin; Mode F narrative facts are left to G3-H;
  - on choice rows, every option text back to its key (a value, a source id, or `undetermined`).
  It refuses a malformed bundle (G0 S3): repeated ids or names, an unknown tier name, a copy whose original is missing,
  is itself a copy, is dated after the copy or states another value, an attribute that differs between the card, the
  block, the claim and the question, or fewer than two independent sources or distinct independent values.
solve_b(view) sorts the independent sources by (tier rank, newest date first), groups equal (rank, date) keys with
itertools.groupby and reads the head group: one distinct value -> that value (or its id when the group is a single
source); several values -> `undetermined`. Imports no solver-A code (plugin.check_independence).
"""
from __future__ import annotations

import datetime as dt
import itertools
import re

from c2_kit import cards as CD
from c2_kit import skin as K
from c2_kit import slots as S

ABSTAIN = "undetermined"
ABSTAIN_TEXT = "Not determinable from reliable sources"
SOURCE_ABSTAIN_TEXT = "No source: not determinable from reliable sources"
CENTS = (("currency", "USD"), ("symbol", "$"))
UNITS = (("kilogram", "kilograms"), ("day", "days"), ("week", "weeks"), ("month", "months"), ("year", "years"),
         ("hour", "hours"), ("minute", "minutes"), ("night", "nights"), ("person", "people"), ("seat", "seats"),
         ("item", "items"), ("ticket", "tickets"))      # G0 section 7: the closed count-unit list
NARRATIVE = {"ASKER": ("name", ()), "ORG": ("name", ()), "ATTR": ("name", ())}
QUESTION = {"ATTR": ("name", ())}
# question form -> (what it asks, asks the positive side)   (G0 S7-S10)
FORMS = {"ch_value": ("value", True), "ch_source": ("source", True), "yn_claim": ("claim", True),
         "yn_claim_wrong": ("claim", False), "yn_claim_not": ("claim", False), "yn_claim_other": ("claim", False),
         "yn_claim_dneg": ("claim", True)}

# G0 v4 1.1: the card text, copied from the spec (exact)
_CW = "The listed sources are complete: no other source, tier or rule applies."
_CARD = (
    "How to settle the {ATTR} from the listed sources:\n"
    "- Tiers, most reliable first: {RANK_1}; then {RANK_2}; then {RANK_3}.\n"
    "- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are "
    "independent.\n"
    "- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it "
    "(never a date a source states). A less reliable source never wins.\n"
    "- Independent sources with that tier and date decide together: one value (or a lone source) stands; different "
    "values make the {ATTR} not determinable from reliable sources.\n"
    "- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\n"
    + _CW)


def _card_regex(card: str):
    parts, seen = [], set()
    for piece in re.split(r"(\{[A-Z0-9_]+\})", card):
        m = re.fullmatch(r"\{([A-Z0-9_]+)\}", piece)
        if not m:
            parts.append(re.escape(piece))
            continue
        g = m.group(1).lower()
        parts.append(f"(?P={g})" if g in seen else f"(?P<{g}>[^\\n;]+?)")
        seen.add(g)
    return re.compile("".join(parts))


CARD_RE = _card_regex(_CARD)
STATE = re.compile(
    r"(?P<narr>.*?)\n\n(?P<head>Sources on the|Source table for the|Excerpts on the|Source records for the) "
    r"(?P<attr>[^\n]+?):\n(?P<body>.*?)"
    r"(?:\n\nClaim to check: the (?P<cattr>[^\n]+?) is (?P<claim>[^\n]+)\.)?(?:\n\n(?P<tail>(?!Claim to check: ).+))?",
    re.S)
LAYOUT_OF = {"Sources on the": "list", "Source table for the": "table", "Excerpts on the": "excerpt",
             "Source records for the": "keyed"}
LIST_LINE = re.compile(r"- Source (?P<id>\S+): (?P<name>[^;\n]+); tier (?P<tier>[^;\n]+); dated (?P<date>[^;\n]+); "
                       r"(?:independent|copied from Source (?P<of>\S+))\. It states the (?P<attr>.+?) is "
                       r"(?P<val>.+)\.")
TABLE_HEAD = "source | name | tier | dated | origin | stated value"
EXCERPT_LINE = re.compile(r"\[(?P<id>[^\]\s]+)\] (?P<name>.+?), tier (?P<tier>.+?), dated (?P<date>.+?), "
                          r"(?:independent|copied from (?P<of>\S+)): \"The (?P<attr>.+?) is (?P<val>.+)\.\"")
ORIGIN = re.compile(r"independent|copied from (?P<of>\S+)")
KEYED = ("source ", "  name: ", "  tier: ", "  dated: ", "  origin: ", "  states: ")


class ParseError(ValueError):
    pass


# ------------------------------------------------------------------------------------------------ values

def _date(text: str) -> str:
    try:
        return S.parse("date", text.strip()).isoformat()
    except S.SlotError as e:
        raise ParseError(f"date {text!r}: {e}") from None


def _value(text: str) -> tuple:
    """(kind, canonical value): the one typed reading of a stated value, an option or the claim (G0 S1)."""
    hits = []
    for kind, slot_kind, params in [("cents", "cents", CENTS), ("date", "date", ())] + [
            (f"count:{u[1]}", "count", (("unit", u),)) for u in UNITS]:
        try:
            v = S.parse(slot_kind, text.strip(), params)
        except S.SlotError:
            continue
        hits.append((kind, v.isoformat() if slot_kind == "date" else v))
    if len(hits) != 1:
        raise ParseError(f"{text!r} reads as {len(hits)} values")
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


def _ordinal(iso: str) -> int:
    return dt.date.fromisoformat(iso).toordinal()


# ------------------------------------------------------------------------------------------------ blocks

def _rows(body: str, layout: str) -> list:
    """[{id, name, tier, date, of, attr, val}] in listed order (raw texts; attr None where the layout omits it)."""
    lines = body.split("\n")
    out = []
    if layout == "list":
        for line in lines:
            m = LIST_LINE.fullmatch(line)
            if not m:
                raise ParseError(f"list line {line!r}")
            out.append(m.groupdict())
    elif layout == "excerpt":
        for line in lines:
            m = EXCERPT_LINE.fullmatch(line)
            if not m:
                raise ParseError(f"excerpt line {line!r}")
            out.append(m.groupdict())
    elif layout == "table":
        if lines[0] != TABLE_HEAD:
            raise ParseError("table header")
        for line in lines[1:]:
            cells = line.split(" | ")
            o = ORIGIN.fullmatch(cells[4]) if len(cells) == 6 else None
            if not o:
                raise ParseError(f"table row {line!r}")
            out.append({"id": cells[0], "name": cells[1], "tier": cells[2], "date": cells[3], "of": o["of"],
                        "attr": None, "val": cells[5]})
    else:
        if len(lines) % len(KEYED):
            raise ParseError("keyed records come in blocks of six lines")
        for k in range(0, len(lines), len(KEYED)):
            rec = lines[k:k + len(KEYED)]
            if any(not ln.startswith(p) for ln, p in zip(rec, KEYED)):
                raise ParseError(f"keyed record {rec!r}")
            got = [ln[len(p):] for ln, p in zip(rec, KEYED)]
            o = ORIGIN.fullmatch(got[4])
            if not o:
                raise ParseError(f"origin {got[4]!r}")
            out.append({"id": got[0], "name": got[1], "tier": got[2], "date": got[3], "of": o["of"], "attr": None,
                        "val": got[5]})
    if not out:
        raise ParseError("an empty source block")
    return out


def _sources(raw: list, tiers: list, attr: str) -> tuple:
    """Typed sources in listed order + the value kind; refuses a bundle that breaks G0 S3."""
    srcs, kinds = [], set()
    for r in raw:
        if r["attr"] is not None and _name(r["attr"]) != attr:
            raise ParseError("a source line names another attribute")
        if r["tier"] not in tiers:
            raise ParseError(f"tier {r['tier']!r} is not on the card's ranking")
        kind, val = _value(r["val"])
        kinds.add(kind)
        srcs.append({"id": _ident(r["id"]), "name": _name(r["name"]), "tier": tiers.index(r["tier"]) + 1,
                     "date": _date(r["date"]), "copy_of": _ident(r["of"]) if r["of"] else None, "value": val})
    if len(kinds) != 1:
        raise ParseError(f"stated values of several kinds {sorted(kinds)}")
    ids = [s["id"] for s in srcs]
    if len(set(ids)) != len(ids) or len({s["name"] for s in srcs}) != len(srcs):
        raise ParseError("two sources share an id or a name")
    by_id = {s["id"]: s for s in srcs}
    for s in srcs:
        if s["copy_of"] is None:
            continue
        orig = by_id.get(s["copy_of"])
        if orig is None or orig["copy_of"] is not None:
            raise ParseError(f"{s['id']} copies a missing source or another copy")
        if orig["value"] != s["value"] or _ordinal(s["date"]) < _ordinal(orig["date"]):
            raise ParseError(f"{s['id']} states another value than its original, or predates it")
    ind = [s for s in srcs if s["copy_of"] is None]
    if len(ind) < 2 or len({repr(s["value"]) for s in ind}) < 2:
        raise ParseError("fewer than two independent sources or distinct independent values")
    return srcs, kinds.pop()


# ------------------------------------------------------------------------------------------------ parse

def parse(row: dict, ctx) -> dict:
    m = STATE.fullmatch(row["state"])
    if not m:
        raise ParseError("the state does not have the narrative / source block / claim layout")
    rules, question = CD.split_rules(row)       # row.card + the question, or the instructions split at the last blank line
    if not rules or not question or "\n\n" in question:
        raise ParseError("card and question are not separated")
    c = CARD_RE.fullmatch(rules)
    if not c:
        raise ParseError("the card does not match the G0 card text")
    attr = _name(c["attr"])
    tiers = [c["rank_1"], c["rank_2"], c["rank_3"]]
    if len(set(tiers)) != 3:
        raise ParseError("the card ranks a tier twice")
    if _name(m["attr"]) != attr:
        raise ParseError("the source block names another attribute")
    srcs, kind = _sources(_rows(m["body"], LAYOUT_OF[m["head"]]), tiers, attr)
    # question
    wording = ctx.skin(row["meta"]["wording_id"])
    qform = wording.qform
    if qform not in FORMS:
        raise ParseError(f"unknown question form {qform}")
    asked = K.match_template(wording.text, question, QUESTION)
    if "ATTR" in asked and asked["ATTR"] != attr:
        raise ParseError("the question names another attribute")
    claim = None
    if m["claim"] is not None:
        if _name(m["cattr"]) != attr:
            raise ParseError("the claim names another attribute")
        ckind, claim = _value(m["claim"])
        if ckind != kind:
            raise ParseError("the claim is of another kind than the stated values")
    if (claim is not None) != (FORMS[qform][0] == "claim"):
        raise ParseError("a claim line appears exactly on claim questions")
    # narrative
    skin = ctx.skin(row["meta"]["c2"]["skin_id"])
    told = {}
    if skin.author_mode == "T":
        if not set(skin.decl) <= set(NARRATIVE):
            raise ParseError(f"skin declares slots outside {sorted(NARRATIVE)}")
        told = K.parse_skin(skin, m["narr"], NARRATIVE)
        if not {"ASKER", "ORG"} <= set(told):
            raise ParseError("narrative lacks the asker or the organisation")
        if "ATTR" in told and told["ATTR"] != attr:
            raise ParseError("the narrative names another attribute")
    view = {"qform": qform, "attr": attr, "tiers": tiers, "sources": srcs, "claim": claim}
    if skin.author_mode == "T":
        view.update(asker=told["ASKER"], org=told["ORG"])
    if row["qtype"] == "choice":
        keys = []
        for text in row["options"]:
            if qform == "ch_value":
                if text == ABSTAIN_TEXT:
                    keys.append(ABSTAIN)
                    continue
                okind, val = _value(text)
                if okind != kind:
                    raise ParseError(f"option {text!r} is of another kind")
                keys.append(val)
            elif qform == "ch_source":
                if text == SOURCE_ABSTAIN_TEXT:
                    keys.append(ABSTAIN)
                    continue
                if not text.startswith("Source ") or text[7:] not in {s["id"] for s in srcs}:
                    raise ParseError(f"option {text!r} is not a listed source")
                keys.append(text[7:])
            else:
                raise ParseError(f"question {qform} has no options")
        view["options"] = keys
    return view


# ------------------------------------------------------------------------------------------------ solve (sort + group)

def _head_group(view: dict) -> list:
    """The independent sources sorted by (rank, newest date first), grouped by (rank, date): the head group."""
    pool = [s for s in view["sources"] if s["copy_of"] is None]
    pool = sorted(pool, key=lambda s: (s["tier"], -_ordinal(s["date"])))
    groups = [list(grp) for _, grp in itertools.groupby(pool, key=lambda s: (s["tier"], s["date"]))]
    return groups[0]


def solve_b(view: dict):
    head = _head_group(view)
    values = []
    for s in head:
        if s["value"] not in values:
            values.append(s["value"])
    what, positive = FORMS[view["qform"]]
    if what == "value":
        return values[0] if len(values) == 1 else ABSTAIN
    if what == "source":
        if len(head) == 1:
            return head[0]["id"]
        if len(values) > 1:
            return ABSTAIN
        raise ParseError("an agreeing tie has no single deciding source (never asked)")
    if len(values) != 1:
        raise ParseError("a claim question on a bundle that is not determinable (never asked)")
    same = values[0] == view["claim"]
    return int(same if positive else not same)
