"""G3 round-trip parser for F4 rows (G0 spec section 4). Written from sections 2, 9 and the formats-1 skin specs
(container grammar data); it never imports the renderer. Inputs: the row's card, state, instructions, options, gold,
its format style id (to read the skin's grammar data) and the card lexicon (entity IDs, type nouns, umbrella noun,
predicates, quantities and units, date attributes, links, source names, document titles, closed pools).

Output: the canonical structure (dict) and a list of lint hits. Any sentence that fits no class is a parse error.
"""
from __future__ import annotations

import csv
import datetime as dt
import html.parser
import io
import json
import re
from decimal import Decimal

import f4lex as L

_FS_HEADERS = None


def _fewshot_headers():
    """Few-shot block headers from the formats-1 template data (grammar data, not renderer code), longest first."""
    global _FS_HEADERS
    if _FS_HEADERS is None:
        from pathlib import Path
        f = Path(__file__).resolve().parents[2] / "formats" / "formats-1" / "data" / "fewshot_templates.jsonl"
        hs = {json.loads(ln).get("header") for ln in open(f) if ln.strip()}
        _FS_HEADERS = sorted((h for h in hs if h), key=len, reverse=True)
    return _FS_HEADERS

MONTHS = {m.lower(): i + 1 for i, m in enumerate(L.MONTHS)}
BULLETS = ("- ", "+ ", "* ", "• ", "· ")


class ParseError(ValueError):
    pass


def norm(s):
    return " ".join(str(s).split())


# ------------------------------------------------------------------------------------------------------- lexicon

class Lexicon:
    """The card lexicon the parser may use (data only)."""

    def __init__(self, d: dict):
        self.d = d
        self.ids = set(d["ids"])
        self.types = {sg: pl for sg, pl in d["types"]}          # singular -> plural
        self.type_pl = {pl: sg for sg, pl in d["types"]}
        self.umbrella = tuple(d["umbrella"])
        self.preds = set(d["preds"])
        self.qty = {q["name"]: q for q in d["qtys"]}
        self.units = {q["name"]: q["unit"] for q in d["qtys"]}
        self.dattrs = set(d["dattrs"])
        self.links = {l["active"]: l for l in d["links"]}
        self.sources = list(d["sources"])
        self.titles = set(d.get("titles", []))
        self.example_ids = set(d.get("example_ids", []))
        self.example_preds = set(d.get("example_preds", []))
        self.background = set(d.get("background", []))
        self.memo_titles = set(d.get("memo_titles", []))
        self.ID = "(" + "|".join(sorted((re.escape(i) for i in self.ids | self.example_ids), key=len,
                                        reverse=True)) + ")"
        self.P = "(" + "|".join(sorted((re.escape(p) for p in self.preds | self.example_preds), key=len,
                                       reverse=True)) + ")"
        self.T = "(" + "|".join(sorted((re.escape(t) for t in self.types), key=len, reverse=True)) + ")"
        self.TPL = "(" + "|".join(sorted((re.escape(t) for t in self.type_pl), key=len, reverse=True)) + ")"
        self.Q = "(" + "|".join(sorted((re.escape(q) for q in self.qty), key=len, reverse=True)) + ")" \
            if self.qty else "(?!x)x"
        self.DA = "(" + "|".join(sorted((re.escape(a) for a in self.dattrs), key=len, reverse=True)) + ")" \
            if self.dattrs else "(?!x)x"
        self.LK = "(" + "|".join(sorted((re.escape(a) for a in self.links), key=len, reverse=True)) + ")" \
            if self.links else "(?!x)x"


NUM = r"(\d+(?:\.\d+)?)"
DATE = r"(\d{4}-\d{2}-\d{2}|\d{1,2} (?:" + "|".join(L.MONTHS) + r") \d{4}|(?:" + "|".join(L.MONTHS) + \
       r") \d{1,2}, \d{4})"


def parse_date(s):
    s = s.strip()
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.fullmatch(r"(\d{1,2}) ([A-Za-z]+) (\d{4})", s)
    if m:
        return dt.date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1)))
    m = re.fullmatch(r"([A-Za-z]+) (\d{1,2}), (\d{4})", s)
    if m:
        return dt.date(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2)))
    raise ParseError("date")


# ------------------------------------------------------------------------------------------------------- phrases

CMP_OPS = [  # (regex of the phrase after 'whose <q> ', op) ; {N} number, {U} unit
    (r"is at least {N}{U}", ">="), (r"is no fewer than {N}{U}", ">="), (r"is no less than {N}{U}", ">="),
    (r"is {N}{U} or more", ">="), (r"is more than {N}{U}", ">"), (r"is over {N}{U}", ">"),
    (r"is above {N}{U}", ">"), (r"exceeds {N}{U}", ">"), (r"is at most {N}{U}", "<="),
    (r"is no more than {N}{U}", "<="), (r"is up to {N}{U}", "<="), (r"is {N}{U} or fewer", "<="),
    (r"is {N}{U} or less", "<="), (r"is fewer than {N}{U}", "<"), (r"is less than {N}{U}", "<"),
    (r"is under {N}{U}", "<"), (r"is below {N}{U}", "<"),
]
DATE_OPS = [(r"is before {D}", "<"), (r"is prior to {D}", "<"), (r"is after {D}", ">"), (r"is later than {D}", ">"),
            (r"is on or before {D}", "<="), (r"is no later than {D}", "<="), (r"is on or after {D}", ">="),
            (r"is no earlier than {D}", ">=")]


def unit_re(lx: Lexicon, q):
    u = lx.units[q]
    return "%" if u == "%" else " " + re.escape(u)


def parse_lit(lx: Lexicon, s, plural=False):
    """'is A' / 'is not A' / cue forms -> (pred, pos)."""
    be = "are" if plural else "is"
    m = re.fullmatch(be + r" (not )?" + lx.P, s)
    if m:
        return (m.group(2), m.group(1) is None)
    m = re.fullmatch(("have" if plural else "has") + " " + lx.P + " standing", s)
    if m:
        return (m.group(1), True)
    m = re.fullmatch(("lack" if plural else "lacks") + " the " + lx.P + " designation", s)
    if m:
        return (m.group(1), False)
    m = re.fullmatch(("fail" if plural else "fails") + " to qualify as " + lx.P, s)
    if m:
        return (m.group(1), False)
    return None


def parse_whose(lx: Lexicon, s):
    """'whose <q> <phrase>' -> condition tuple (written operator and ends)."""
    m = re.fullmatch(r"whose " + lx.Q + r" (.+)", s)
    if m:
        q, rest = m.group(1), m.group(2)
        U = unit_re(lx, q)
        for pat, op in CMP_OPS:
            mm = re.fullmatch(pat.replace("{N}", NUM).replace("{U}", U), rest)
            if mm:
                return ("cmp", q, op, Decimal(mm.group(1)))
        for pat in (r"is between {N} and {N}{U}", r"is from {N} to {N}{U}"):
            mm = re.fullmatch(pat.replace("{N}", NUM).replace("{U}", U), rest)
            if mm:
                return ("rng", q, Decimal(mm.group(1)), Decimal(mm.group(2)))
    m = re.fullmatch(r"whose " + lx.DA + r" (.+)", s)
    if m:
        a, rest = m.group(1), m.group(2)
        for pat, op in DATE_OPS:
            mm = re.fullmatch(pat.replace("{D}", DATE), rest)
            if mm:
                return ("dcmp", a, op, parse_date(mm.group(1)))
        for pat in (r"is between {D} and {D}", r"is from {D} to {D}"):
            mm = re.fullmatch(pat.replace("{D}", DATE), rest)
            if mm:
                return ("win", a, parse_date(mm.group(1)), parse_date(mm.group(2)))
    return None


def split_and(s):
    """Split a conjunction 'X and Y and Z' at ' and ' (dates and ranges protected)."""
    prot = re.sub(r"between (\S+(?: \S+){0,3}?) and ", lambda m: "between " + m.group(1).replace(" ", "\x00") +
                  "\x00and\x00", s)
    parts = prot.split(" and ")
    return [p.replace("\x00", " ") for p in parts]


def parse_body(lx: Lexicon, body, plural=False):
    """'that is A and is not B and whose q ...' -> list of conditions."""
    conds = []
    rest = body
    if rest.startswith("that "):
        rest = rest[5:]
    parts = split_and(rest)
    i = 0
    while i < len(parts):
        p = parts[i]
        if p.startswith("whose "):
            c = parse_whose(lx, p)
            if c is None:
                raise ParseError("cond")
            conds.append(c)
        else:
            lit = parse_lit(lx, p, plural)
            if lit is None:
                raise ParseError("lit")
            conds.append(("lit",) + lit)
        i += 1
    return conds


def parse_item_cond(lx: Lexicon, s):
    """A bulleted list item: 'it is A' / 'it lacks ...' / 'its <q> ...'."""
    if s.startswith("it "):
        lit = parse_lit(lx, s[3:])
        if lit is None:
            raise ParseError("item")
        return ("lit",) + lit
    if s.startswith("its "):
        c = parse_whose(lx, "whose " + s[4:])
        if c is None:
            raise ParseError("item")
        return c
    raise ParseError("item")


# ------------------------------------------------------------------------------------------------------- sentences

def parse_conjunct(lx: Lexicon, e, s):
    """One conjunct of a fact sentence about entity e -> statement tuple."""
    m = re.fullmatch(r"is (a|an) " + lx.T, s)
    if m:
        if L.article(m.group(2)) != m.group(1):
            raise ParseError("article")
        return ("type", e, m.group(2))
    lit = parse_lit(lx, s)
    if lit:
        return ("lit", lit[0], e, lit[1])
    m = re.fullmatch(r"has (a|an) " + lx.Q + r" of " + NUM + r"(.*)", s)
    if m:
        q = m.group(2)
        if not re.fullmatch(unit_re(lx, q), m.group(4)):
            raise ParseError("unit")
        return ("val", e, q, Decimal(m.group(3)))
    m = re.fullmatch(r"has (a|an) " + lx.DA + r" of " + DATE, s)
    if m:
        return ("date", e, m.group(2), parse_date(m.group(3)))
    m = re.fullmatch(lx.LK + r" " + lx.ID, s)
    if m:
        if m.group(2) == e:
            raise ParseError("self_link")
        return ("link", m.group(1), e, m.group(2))
    raise ParseError("conjunct")


def parse_fact_sentence(lx: Lexicon, s):
    m = re.fullmatch(lx.ID + r" (.+)\.", s)
    if not m:
        return None
    e, rest = m.group(1), m.group(2)
    for bad in (" or ", " nor ", "neither ", "either ", " both "):
        if bad in " " + rest + " ":
            raise ParseError("fact_coord")
    parts = rest.split(" and ")
    out = []
    for p in parts:
        out.append(parse_conjunct(lx, e, p))
    return out


QUANT = {"Every": "every", "Each": "each", "Any": "any"}


def parse_rule_line(lx: Lexicon, s):
    """A single-sentence rule -> canonical rule dict, or None."""
    m = re.fullmatch(r"(Every|Each|Any) " + lx.T + r" that is either " + lx.P + r" or " + lx.P +
                     r", but not both, is (not )?" + lx.P + r"\.", s)
    if m:
        return {"form": "xor", "typ": m.group(2), "conds": [("lit", m.group(3), True), ("lit", m.group(4), True)],
                "head": (m.group(6), m.group(5) is None)}
    m = re.fullmatch(r"(Every|Each|Any) " + lx.T + r" that is " + lx.P + r" or " + lx.P + r" is (not )?" + lx.P +
                     r"\.", s)
    if m:
        return {"form": "or", "typ": m.group(2), "conds": [("lit", m.group(3), True), ("lit", m.group(4), True)],
                "head": (m.group(6), m.group(5) is None)}
    m = re.fullmatch(r"(Every|Each|Any) " + lx.T + r" that " + lx.LK + r" (a|an) " + lx.T + r" that (.+?) is (not )?"
                     + lx.P + r"\.", s)
    if m:
        pc = parse_lit(lx, m.group(6))
        if pc is None:
            raise ParseError("link_pcond")
        if L.article(m.group(5)) != m.group(4):
            raise ParseError("article")
        return {"form": "link", "typ": m.group(2), "link": m.group(3), "ptyp": m.group(5), "pcond": pc,
                "head": (m.group(8), m.group(7) is None)}
    m = re.fullmatch(r"(A|An) " + lx.T + r" is " + lx.P + r" only if it is " + lx.P + r"\.", s)
    if m:
        return {"form": "onlyif", "typ": m.group(2), "ante": m.group(3), "conds": [("lit", m.group(4), True)],
                "head": (m.group(4), True)}
    m = re.fullmatch(r"All " + lx.TPL + r" (.+?) are (not )?" + lx.P + r"\.", s)
    if m:
        conds = parse_body(lx, m.group(2), plural=True)
        if any(c[0] != "lit" for c in conds):
            raise ParseError("all_body")
        return {"form": "univ", "typ": lx.type_pl[m.group(1)], "conds": conds, "head": (m.group(4),
                                                                                       m.group(3) is None)}
    m = re.fullmatch(r"No " + lx.T + r" (.+?) is " + lx.P + r"(?:, unless it is " + lx.P + r"|, except one that is " +
                     lx.P + r")?\.", s)
    if m:
        conds = parse_body(lx, m.group(2))
        exc = m.group(4) or m.group(5)
        return {"form": "neguniv", "typ": m.group(1), "conds": conds, "head": (m.group(3), False), "exc": exc}
    m = re.fullmatch(r"(Every|Each|Any) " + lx.T + r" (.+?) is (not )?" + lx.P +
                     r"(?:, unless it is " + lx.P + r"|, except one that is " + lx.P + r")?\.", s)
    if m:
        conds = parse_body(lx, m.group(3))
        exc = m.group(6) or m.group(7)
        return {"form": "univ", "typ": m.group(2), "conds": conds, "head": (m.group(5), m.group(4) is None),
                "exc": exc}
    return None


LEAD_RE = r"This provision covers every {T} that meets all of the following conditions:"
KOFN_RE = r"(A|An) {T} is {P} if at least (\d) of the following hold:"


def parse_list_rule(lx: Lexicon, lead, items, close):
    m = re.fullmatch(LEAD_RE.replace("{T}", lx.T), lead)
    if m:
        t = m.group(1)
        conds = [parse_item_cond(lx, x) for x in items]
        if close is None:
            raise ParseError("list_close")
        for x in items:
            if re.search(r"\b(unless|except)\b", x):
                raise ParseError("exc_in_bullet")
        mc = re.fullmatch(r"Every such " + re.escape(t) + r" is (not )?" + lx.P + r"(?:, unless it is " + lx.P +
                          r"|, except one that is " + lx.P + r")?\.", close)
        if mc:
            return {"form": "univ", "typ": t, "conds": conds, "head": (mc.group(2), mc.group(1) is None),
                    "exc": mc.group(3) or mc.group(4)}
        mc = re.fullmatch(r"No such " + re.escape(t) + r" is " + lx.P + r"(?:, unless it is " + lx.P +
                          r"|, except one that is " + lx.P + r")?\.", close)
        if mc:
            return {"form": "neguniv", "typ": t, "conds": conds, "head": (mc.group(1), False),
                    "exc": mc.group(2) or mc.group(3)}
        raise ParseError("list_close")
    m = re.fullmatch(KOFN_RE.replace("{T}", lx.T).replace("{P}", lx.P), lead)
    if m:
        conds = [parse_item_cond(lx, x) for x in items]
        return {"form": "kofn", "typ": m.group(2), "conds": conds, "head": (m.group(3), True), "k": int(m.group(4))}
    return None


def is_lead(lx, s):
    return bool(re.fullmatch(LEAD_RE.replace("{T}", lx.T), s) or
                re.fullmatch(KOFN_RE.replace("{T}", lx.T).replace("{P}", lx.P), s))


HEDGE_PATTERNS = [
    (r"Most {TPL} that (.+?) (are (?:not )?{P})\.", "most"), (r"Many {TPL} that (.+?) (are (?:not )?{P})\.", "many"),
    (r"{TPLC} that (.+?) are usually ((?:not )?{P})\.", "usually"), (r"{TPLC} that (.+?) are often ((?:not )?{P})\.",
                                                                    "often"),
    (r"Some {TPL} that (.+?) (are (?:not )?{P})\.", "some"), (r"Not every {T} that (.+?) (is (?:not )?{P})\.",
                                                              "notevery"),
    (r"Some {T} that (.+?) (is (?:not )?{P})\.", "exist"),
]


def parse_hedge(lx: Lexicon, s):
    tplc = "(" + "|".join(sorted((re.escape(t[:1].upper() + t[1:]) for t in lx.type_pl), key=len, reverse=True)) + ")"
    for pat, kind in HEDGE_PATTERNS:
        rx = pat.replace("{TPLC}", tplc).replace("{TPL}", lx.TPL).replace("{T}", lx.T).replace("{P}", lx.P)
        m = re.fullmatch(rx, s)
        if not m:
            continue
        tname = m.group(1)
        if kind in ("usually", "often"):
            tname = tname[:1].lower() + tname[1:]
        plural = kind in ("most", "many", "some", "usually", "often")
        typ = lx.type_pl[tname] if plural else tname
        cnd = parse_lit(lx, m.group(2), plural=plural)
        if kind in ("usually", "often"):
            hd = ((m.group(3).split()[-1]), not m.group(3).startswith("not "))
        else:
            hd = parse_lit(lx, m.group(3), plural=plural)
        if cnd is None or hd is None:
            raise ParseError("hedge")
        return {"kind": kind, "typ": typ, "cond": cnd, "head": hd}
    return None


def parse_ehedge(lx: Lexicon, s):
    m = re.fullmatch(lx.ID + r" (may well be|may be|might be) " + lx.P + r"\.", s)
    if m:
        return {"kind": m.group(2), "e": m.group(1), "pred": m.group(3)}
    return None


def parse_closure(lx: Lexicon, s):
    m = re.fullmatch(r"The record names every " + lx.T + r" that is " + lx.P + r"\.", s)
    if m:
        return {"pred": m.group(2), "typ": m.group(1), "form": "prose"}
    m = re.fullmatch(r"The " + lx.P + r" column is complete: a blank " + lx.P + r" cell means No\.", s)
    if m:
        if m.group(1) != m.group(2):
            raise ParseError("closure_col")
        return {"pred": m.group(1), "typ": None, "form": "column"}
    return None


def parse_attribution(lx: Lexicon, s):
    """'<Source>: <stmt>.' / '<Source>: "<stmt>."' / '<Source> reported that <stmt>.' -> (source, frame, stmt)."""
    for src in sorted(lx.sources, key=len, reverse=True):
        S = src[:1].upper() + src[1:]
        for cand in (S, src):
            if s.startswith(cand + ': "') and s.endswith('."'):
                return src, "quote", s[len(cand) + 3:-2]
            if s.startswith(cand + ": "):
                return src, "colon", s[len(cand) + 2:].rstrip(".")
            if s.startswith(cand + " reported that "):
                return src, "reported", s[len(cand) + 15:].rstrip(".")
    return None


# ======================================================================================================= containers

def unfence(text):
    lines = text.split("\n")
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines), None
    for i, ln in enumerate(lines):
        if ln.startswith("```"):
            title = "\n".join(lines[:i]).strip()
            body = lines[i + 1:]
            if body and body[-1].strip() == "```":
                body = body[:-1]
            return "\n".join(body), title
    if all(ln.startswith("    ") or not ln for ln in lines) and any(lines):
        return "\n".join(ln[4:] for ln in lines), None
    # indent4 fence with a title above it
    if len(lines) > 2 and not lines[0].startswith("    ") and lines[1] == "" and \
            all(ln.startswith("    ") or not ln for ln in lines[2:]):
        return "\n".join(ln[4:] for ln in lines[2:]), lines[0]
    return text, None


class _H(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.segs, self.stack, self.buf, self.table, self.row = [], [], [], None, None

    def handle_starttag(self, tag, attrs):
        self.stack.append(tag)
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "th", "td", "caption", "dt", "dd"):
            self.buf = []
        if tag == "table":
            self.table = []
        if tag == "tr":
            self.row = []

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        txt = "".join(self.buf)
        if tag == "p":
            self.segs.append(("text", txt))
        elif tag == "li":
            self.segs.append(("bullet", txt))
        elif tag in ("h1", "h2", "h3", "h4", "caption"):
            self.segs.append(("chrome", txt))
        elif tag in ("th", "td"):
            self.row.append(txt)
        elif tag == "tr":
            self.table.append(self.row)
            self.row = None
        elif tag == "table":
            self.segs.append(("table", self.table[0], self.table[1:]))
            self.table = None
        self.buf = []

    def handle_data(self, data):
        self.buf.append(data)


def seg_html(text):
    h = _H()
    h.feed(text)
    out = []
    for sg in h.segs:
        if sg[0] in ("text", "bullet", "chrome"):
            out.append((sg[0], norm(sg[1])))
        else:
            out.append(sg)
    return out


def seg_json_obj(obj, out, key=None):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                out.append(("kv", k, v))
            elif isinstance(v, list) and v and all(isinstance(x, dict) for x in v):
                cols = list(v[0].keys())
                for x in v:
                    if list(x.keys()) != cols:
                        raise ParseError("json_keys")   # every entry of one table carries the same keys
                out.append(("chrome", k))
                out.append(("table", cols, [[x[c] for c in cols] for x in v]))
            elif isinstance(v, list):
                out.append(("chrome", k))
                for x in v:
                    if not isinstance(x, str):
                        raise ParseError("json_list")
                    out.append(("bullet", x))
            elif isinstance(v, dict):
                out.append(("chrome", k))
                seg_json_obj(v, out, k)
            else:
                raise ParseError("json_value")
    elif isinstance(obj, list):
        if obj and all(isinstance(x, dict) for x in obj):
            cols = list(obj[0].keys())
            for x in obj:
                if list(x.keys()) != cols:
                    raise ParseError("json_keys")
            out.append(("table", cols, [[x[c] for c in cols] for x in obj]))
        else:
            raise ParseError("json_top")
    return out


def seg_text(text, skin):
    """Line segments for prose, memo, sop and markdown skins."""
    segs = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s:
            segs.append(("break",))
            i += 1
            continue
        # markdown / grid tables
        if s.startswith("+") and re.fullmatch(r"\+(?:[-=]+\+)+", s):
            rows = []
            while i < len(lines) and lines[i].strip().startswith(("+", "|")):
                t = lines[i].strip()
                if t.startswith("|"):
                    rows.append([c.strip() for c in t.strip("|").split("|")])
                i += 1
            segs.append(("table", rows[0], rows[1:]))
            continue
        if s.startswith("| ") and s.endswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                t = lines[i].strip()
                if not re.fullmatch(r"\|(?:\s*:?-{3,}:?\s*\|)+", t):
                    rows.append([c.strip() for c in t[1:-1].split("|")])
                i += 1
            segs.append(("table", rows[0], rows[1:]))
            continue
        # aligned table: header line followed by a rule of '=' groups
        if i + 1 < len(lines) and re.fullmatch(r"=+(?:  =+)+", lines[i + 1].strip()):
            head = re.split(r"\s{2,}", s)
            rows = []
            i += 2
            while i < len(lines) and lines[i].strip():
                rows.append(re.split(r"\s{2,}", lines[i].strip()))
                i += 1
            segs.append(("table", head, rows))
            continue
        # pipe table (memo.internal): header row starting 'ID | type'
        if re.match(r"ID \| type(?: \||$)", s):
            rows = []
            while i < len(lines) and lines[i].strip() and "|" in lines[i]:
                rows.append([c.strip() for c in re.split(r" \|(?: |$)", lines[i])])
                i += 1
            n = len(rows[0])
            rows = [r + [""] * (n - len(r)) for r in rows]
            segs.append(("table", rows[0], rows[1:]))
            continue
        ind = len(ln) - len(ln.lstrip(" "))
        bullet = next((b for b in BULLETS if s.startswith(b)), None)
        if bullet:
            segs.append(("bullet", s[len(bullet):], ind))
        else:
            segs.append(("text", s, ind))
        i += 1
    return segs


# ======================================================================================================= state

SENT_SPLIT = re.compile(r'(?<=[.?!])\s+(?=[A-Z0-9"])|(?<=\.")\s+(?=[A-Z0-9])')
HEADINGS = set(L.HEADINGS_FACTS + L.HEADINGS_RULES + L.HEADINGS_TABLE + L.HEADINGS_STMTS + L.HEADINGS_NOTES +
               L.HEADINGS_NARR)


def _keynorm(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def chrome_core(s):
    t = s.strip()
    t = re.sub(r"^#{1,6} ", "", t)
    t = re.sub(r"^\*\*(.+)\*\*$", r"\1", t)
    t = re.sub(r"^== (.+) ==$", r"\1", t)
    t = re.sub(r"^\[(.+)\]$", r"\1", t)
    t = re.sub(r"^§ \d+ ", "", t)
    t = re.sub(r"^\d+\. ", "", t)
    t = re.sub(r":$", "", t)
    return t


def is_chrome(lx: Lexicon, s):
    t = chrome_core(s)
    low = t.lower()
    known = {h.lower() for h in HEADINGS} | {x.lower() for x in lx.titles} | {x.lower() for x in lx.memo_titles}
    known |= {f"{h.lower()} {i}" for h in L.HEADINGS_TABLE for i in range(1, 5)}
    if low in known:
        return True
    if " | " in s:
        a, b = s.split(" | ", 1)
        return a.lower() in {x.lower() for x in lx.memo_titles} and b.lower() in {x.lower() for x in lx.titles}
    if re.fullmatch(r"[=*\-]{3,}", s.strip()):
        return True
    return False


def background_res(lx: Lexicon):
    out = []
    dl = list(lx.d.get("docs") or []) or ["file"]   # a pack with no document type uses the word "file" (5.7 I3)
    docs = "(" + "|".join(sorted((re.escape(d) for d in dl), key=len, reverse=True)) + ")"
    for t in L.BACKGROUND_TEMPLATES:
        rx = re.escape(t).replace(re.escape("{X}"), lx.ID).replace(re.escape("{doc}"), docs) \
            .replace(re.escape("{types}"), lx.TPL)
        out.append(re.compile(rx))
    return out


def attack_res():
    ans = "(" + "|".join(re.escape(a) for a in L.ATTACK_ANS_YN + L.ATTACK_ANS_CH) + ")"
    return [re.compile(re.escape(t).replace(re.escape("{ANS}"), ans)) for t in L.ATTACKS]


def classify_sentence(lx: Lexicon, s, bgres, atres):
    """-> (kind, payload). Raises ParseError on a sentence that fits no class."""
    a = parse_attribution(lx, s)
    if a:
        src, frame, body = a
        if frame != "quote" and ('"' in body):
            raise ParseError("quote_outside_frame")
        if re.search(r"\.\s|;| and | or | but | also ", body):
            raise ParseError("attr_multi")
        fs = parse_fact_sentence(lx, body + ".")
        if not fs or len(fs) != 1 or fs[0][0] == "type":
            raise ParseError("attr_stmt")
        return ("attr", (src, frame, fs[0]))
    c = parse_closure(lx, s)
    if c:
        return ("closure", c)
    for p in L.TOPIC_LABELS:
        m = re.fullmatch(re.escape(p) + r": whether " + lx.ID + r" is (not )?" + lx.P, s)
        if m:
            return ("topic", (m.group(1), m.group(3), m.group(2) is None))
    if ": " in s:
        for rx in atres:
            if rx.fullmatch(s):
                return ("inject", s)
        raise ParseError("label_statement")
    r = parse_rule_line(lx, s)
    if r:
        return ("rule", r)
    h = parse_hedge(lx, s)
    if h:
        return ("hedge", h)
    eh = parse_ehedge(lx, s)
    if eh:
        return ("ehedge", eh)
    for rx in bgres:
        if rx.fullmatch(s):
            return ("bg", s)
    if s in lx.background:
        return ("bg", s)
    for rx in atres:
        if rx.fullmatch(s):
            return ("inject", s)
    fs = parse_fact_sentence(lx, s)
    if fs:
        return ("fact", fs)
    raise ParseError("sentence")


def split_sentences(text):
    return [x.strip() for x in SENT_SPLIT.split(text) if x.strip()]


def parse_state(state: str, style: dict, skin: dict, lx: Lexicon):
    """-> dict(items=[(kind, payload)], tables=[(cols, rows)], lint=[...])."""
    cont = style["container"]
    body, ftitle = unfence(state)
    lint = []
    if cont == "json":
        if skin["params"].get("layout") == "lines":
            objs = [json.loads(x) for x in body.split("\n") if x.strip()]
            segs = seg_json_obj(objs, [])
        else:
            segs = seg_json_obj(json.loads(body), [])
    elif cont == "yaml":
        import yaml
        segs = seg_json_obj(yaml.safe_load(body), [])
    elif cont == "csv":
        lines = body.split("\n")
        if ftitle is None and lines and not any(d in lines[0] for d in (",", ";", "\t", "|", "  ")):
            ftitle, lines = lines[0], lines[2:] if len(lines) > 1 and not lines[1] else lines[1:]
        txt = "\n".join(lines)
        if skin["params"].get("fixed"):
            rows = [re.split(r"\s{2,}", ln.strip()) for ln in lines if ln.strip()]
        else:
            rows = list(csv.reader(io.StringIO(txt), delimiter=skin["params"]["delim"]))
        segs = [("table", rows[0], rows[1:])]
    elif cont == "html_snippet":
        segs = seg_html(body)
    else:
        segs = seg_text(body, skin)
    if ftitle:
        segs = [("chrome", ftitle)] + segs
    items, tables = [], []
    bgres, atres = background_res(lx), attack_res()
    i = 0
    numbered = skin["id"] == "prose.numbered_paras"
    while i < len(segs):
        sg = segs[i]
        k = sg[0]
        if k == "break":
            i += 1
            continue
        if k == "table":
            tables.append((sg[1], sg[2]))
            i += 1
            continue
        if k == "kv":
            tkey = (skin.get("vocab") or {}).get("title", "title")
            if _keynorm(sg[1]) in (_keynorm(tkey), "title") and (sg[2] in lx.titles):
                i += 1
                continue
            raise ParseError("kv_line")
        text = sg[1]
        if k == "chrome":
            if not (is_chrome(lx, text) or _keynorm(text) in {_keynorm(h) for h in HEADINGS} or
                    _keynorm(text) in {"rows", "entries", "items", "points", "notes", "summary"} or
                    any(_keynorm(text) == _keynorm(f"{h} {n}") for h in L.HEADINGS_TABLE for n in range(1, 5))):
                raise ParseError("chrome")
            i += 1
            continue
        if k == "bullet" and is_chrome(lx, text):
            i += 1
            continue
        if k == "text":
            if numbered:
                text = re.sub(r"^\d+\. ", "", text)
            if is_chrome(lx, text):
                i += 1
                continue
            if text.endswith(":") and not is_lead(lx, text) and is_chrome(lx, text[:-1]):
                i += 1
                continue
        # lead-in of a list rule: its items follow as bullets, then (universal) a closing line
        if is_lead(lx, text):
            its = []
            j = i + 1
            while j < len(segs) and segs[j][0] in ("bullet", "break"):
                if segs[j][0] == "bullet" and is_chrome(lx, segs[j][1]):
                    break   # a section heading rendered as a bullet ends the list
                if segs[j][0] == "bullet":
                    its.append(segs[j][1])
                j += 1
            close = None
            if text.startswith("This provision"):
                while j < len(segs) and segs[j][0] == "break":
                    j += 1
                if j < len(segs) and segs[j][0] == "text":
                    cl = segs[j][1]
                    if numbered:
                        cl = re.sub(r"^\d+\. ", "", cl)
                    sents = split_sentences(cl)
                    close = sents[0]
                    rest = " ".join(sents[1:])
                    j += 1
                    if rest:
                        segs.insert(j, ("text", rest, 0))
            r = parse_list_rule(lx, text, its, close)
            if r is None:
                raise ParseError("list_rule")
            r["_list"] = True
            items.append(("rule", r))
            i = j
            continue
        sents = [text] if k == "bullet" else split_sentences(text)
        for s in sents:
            items.append(classify_sentence(lx, s, bgres, atres))
        i += 1
    return {"items": items, "tables": tables, "lint": lint}


# ======================================================================================================= tables

def table_stmts(lx: Lexicon, cols, rows, typed: bool):
    """Table -> (entity types, statements). Columns: ID, type, predicates, quantities, dates, link phrases."""
    kn = {_keynorm(c): c for c in cols}
    keys = [_keynorm(c) for c in cols]
    if keys[:2] != ["id", "type"]:
        raise ParseError("table_head")
    kinds = []
    for c in cols[2:]:
        k = _keynorm(c)
        hit = None
        for p in lx.preds:
            if _keynorm(p) == k:
                hit = ("pred", p)
        for q in lx.qty:
            if _keynorm(q) == k:
                hit = ("qty", q)
        for a in lx.dattrs:
            if _keynorm(a) == k:
                hit = ("date", a)
        for a in lx.links:
            if _keynorm(a) == k:
                hit = ("link", a)
        if hit is None:
            raise ParseError("table_col")
        kinds.append(hit)
    ents, stmts = [], []
    for r in rows:
        e = str(r[0])
        if e not in lx.ids:
            raise ParseError("table_id")
        t = str(r[1])
        if t not in lx.types:
            raise ParseError("table_type")
        ents.append((e, t))
        for (kind, key), v in zip(kinds, r[2:]):
            if kind == "pred":
                if typed:
                    if v is None:
                        stmts.append(("lit", key, e, None, "cell"))
                    elif isinstance(v, bool):
                        stmts.append(("lit", key, e, v, "cell"))
                    else:
                        raise ParseError("cell_bool")
                else:
                    if v == "Yes":
                        stmts.append(("lit", key, e, True, "cell"))
                    elif v == "No":
                        stmts.append(("lit", key, e, False, "cell"))
                    elif v == "not recorded":
                        stmts.append(("lit", key, e, None, "cell"))
                    elif v == "":
                        stmts.append(("blank", key, e))
                    else:
                        raise ParseError("cell_value")
            elif kind == "qty":
                if v is None or v == "not recorded":
                    stmts.append(("val", key, e, None, "cell"))
                elif v == "":
                    raise ParseError("blank_qty")
                else:
                    stmts.append(("val", key, e, Decimal(str(v)), "cell"))
            elif kind == "date":
                if v is None or v == "not recorded":
                    stmts.append(("date", key, e, None, "cell"))
                else:
                    stmts.append(("date", key, e, parse_date(str(v)), "cell"))
            elif kind == "link":
                if v in (None, "", "not recorded", "No", "none", False):
                    raise ParseError("link_cell")
                for y in str(v).split(", "):
                    if y not in lx.ids or y == e:
                        raise ParseError("link_cell_id")
                    stmts.append(("link", key, e, y, "cell"))
    return ents, stmts, kinds


# ======================================================================================================= card / instructions

def clause_regexes(lx: Lexicon):
    """{clause id: compiled regex over whitespace-normalised text}."""
    tv = sorted(set(lx.types) | {lx.umbrella[0]}, key=len, reverse=True)
    tp = sorted(set(lx.type_pl) | {lx.umbrella[1]}, key=len, reverse=True)
    out = {}
    for cid, t in L.CLAUSES.items():
        t = t.replace("a {type}", "\x01 {type}").replace("A {type}", "\x02 {type}")
        rx = re.escape(norm(t)).replace("\x01", "(?:a|an)").replace("\x02", "(?:A|An)")
        rx = rx.replace(re.escape("{types}"), "(?P<tp>" + "|".join(map(re.escape, tp)) + ")")
        rx = rx.replace(re.escape("{type}"), "(?P<t>" + "|".join(map(re.escape, tv)) + ")", 1)
        rx = rx.replace(re.escape("{type}"), "(?P=t)")
        rx = rx.replace(re.escape("{entities}"), re.escape(lx.umbrella[1])).replace(re.escape("{entity}"),
                                                                                     re.escape(lx.umbrella[0]))
        if cid == "15":
            qs = "|".join(map(re.escape, lx.qty)) or "(?!x)x"
            us = "|".join(map(re.escape, sorted({(u if u != "%" else "percent") for u in lx.units.values()}))) or \
                "(?!x)x"
            rx = rx.replace(re.escape("{quantity}"), "(?P<q>" + qs + ")").replace(re.escape("{unit}"),
                                                                                  "(?P<u>" + us + ")")
        if cid == "22":
            rx = rx.replace(re.escape("{sources}"), "(?P<src>.+?)")
        out[cid] = re.compile(rx)
    return out


def parse_card_text(lx: Lexicon, text: str):
    """Clause ids found (with their live values), standing rules, examples. Returns dict."""
    nt = norm(text)
    res = {"clauses": set(), "live_type": set(), "trusted": None, "q15": {}, "spans": []}
    for cid, rx in clause_regexes(lx).items():
        for m in rx.finditer(nt):
            res["clauses"].add(cid)
            res["spans"].append(m.span())
            gd = m.groupdict()
            if gd.get("t"):
                res["live_type"].add(gd["t"])
            if cid == "15":
                res["q15"][gd["q"]] = gd["u"]
            if cid == "22":
                src = gd["src"]
                names = re.split(r", | or ", src)
                for n in names:
                    if n not in lx.sources:
                        raise ParseError("trust_name")
                res["trusted"] = tuple(sorted(names))
    return res


def residual(text: str, spans, extra_strings):
    """Text left after removing recognised clause spans and known strings; must be chrome only."""
    nt = norm(text)
    keep = []
    last = 0
    for a, b in sorted(spans):
        if a < last:
            continue
        keep.append(nt[last:a])
        last = b
    keep.append(nt[last:])
    rest = " ".join(keep)
    for s in sorted(extra_strings, key=len, reverse=True):
        if not norm(s):
            continue
        rest = re.sub(r"(?<![\w-])" + re.escape(norm(s)) + r"(?![\w-])", " ", rest, flags=re.I)
    return norm(rest)


# ======================================================================================================= questions

def question_regexes(lx: Lexicon):
    """[(regex, form, frame/paraphrase)] for every admitted frame paraphrase and slot fill."""
    C_ = lx.ID + r" is (not )?" + lx.P
    out = []
    ff = {"F": "YN-F", "R": "YN-R", "O": "YN-O", "nF": "YN-nF", "nR": "YN-nR", "dn": "YN-dn"}
    for key, by in L.OUT_FILL.items():
        for frk, fills in by.items():
            fr = {"A": "Q-A", "B": "Q-B", "D": "Q-D"}[frk]
            for pi, tpl in enumerate(L.FRAMES[fr]):
                for fill in fills:
                    rx = re.escape(tpl).replace(re.escape("{OUT}"), re.escape(fill)).replace(re.escape("<c>"), C_)
                    out.append((re.compile(rx), ff[key], f"{fr}/p{pi}"))
    for pi, tpl in enumerate(L.FRAMES["Q-T"]):
        rx = re.escape(tpl).replace(re.escape("<cq>"), '"' + C_ + '"')
        out.append((re.compile(rx), "YN-T", f"Q-T/p{pi}"))
    for pi, tpl in enumerate(L.FRAMES["Q-CH"]):
        out.append((re.compile(re.escape(tpl).replace(re.escape("<c>"), C_)), "CH-x", f"Q-CH/p{pi}"))
    for pi, tpl in enumerate(L.FRAMES["Q-claim"]):
        out.append((re.compile(re.escape(tpl).replace(re.escape("{OUT}"), re.escape(L.QCLAIM_FILL))), "CH-claim",
                    f"Q-claim/p{pi}"))
    for pi, tpl in enumerate(L.FRAMES["Q-entity"]):
        rx = re.escape(tpl).replace(re.escape("{OUT}"), re.escape(L.QENTITY_FILL[pi])) \
            .replace(re.escape("<types>"), lx.TPL).replace(re.escape("<H>"), lx.P)
        out.append((re.compile(rx), "CH-entity", f"Q-entity/p{pi}"))
    return out


def find_question(lx: Lexicon, instr: str):
    hits = []
    nt = norm(instr)
    for rx, form, fp in question_regexes(lx):
        for m in rx.finditer(nt):
            hits.append((m.span(), form, fp, m))
    # keep maximal, non-nested matches (a Q-B match inside a Q-D sentence is not a second question)
    best = [h for h in hits if not any(o is not h and o[0][0] <= h[0][0] and h[0][1] <= o[0][1] and
                                       (o[0][1] - o[0][0]) > (h[0][1] - h[0][0]) for o in hits)]
    spans = {h[0] for h in best}
    if len(spans) != 1:
        raise ParseError("question_count")
    h = best[0]
    return h


# ======================================================================================================= row

def parse_row(fields: dict, style: dict, skin: dict, lexd: dict):
    """fields: card, state, instructions, options, qtype, gold. Returns (canon, info)."""
    lx = Lexicon(lexd)
    qtype = fields["qtype"]
    card_text = fields.get("card") or ""
    instr = fields["instructions"]
    # --- card clauses live in card (yes/no) or instructions (choice)
    ctext = card_text if qtype == "noul" else instr
    cinfo = parse_card_text(lx, ctext)
    # standing rules, examples, persona, wording
    extra_known = []
    card_rules = []
    examples = []
    persona = None
    for tpl in L.PERSONA_TEMPLATES:
        rx = re.escape(tpl).replace(re.escape("{role}"), re.escape(lexd["role"]))
        if re.search(rx, norm(ctext)):
            persona = tpl
            extra_known.append(tpl.format(role=lexd["role"]))
    if persona is None:
        raise ParseError("persona")
    for ln in ctext.split("\n"):
        s = norm(re.sub(r"^\s*(?:(?:[-+*\u2022\u00b7>]|\d+(?:\.\d+)*[.)]|\(\d+\)|Rule \d+:|R\d+\.)\s+)*", "", ln))
        if not s:
            continue
        r = None
        try:
            r = parse_rule_line(lx, s)
        except ParseError:
            r = None
        if r:
            r["where"] = "card"
            card_rules.append(r)
            extra_known.append(s)
            continue
        for ex in re.findall(r"If [^.]*?, then the record [^.]*?\.", s):
            examples.append(ex)
            extra_known.append(ex)
    # few-shot cases
    fs_cases = re.findall(r"Record: (.*?) Question: (.*?\?)", norm(ctext))
    for rec_t, q in fs_cases:
        extra_known.append(f"Record: {rec_t} Question: {q}")
    q = find_question(lx, instr)
    (qa, qb), form, fp, qm = q
    extra_known.append(qm.group(0))
    wording = None
    for w in lexd["wordings"]:
        if norm(w) in norm(instr):
            wording = w
            extra_known.append(w)
            break
    if wording is None:
        raise ParseError("wording")
    # residual check over the card text (choice rows: instructions minus question and wording)
    chrome_words = set()
    for v in L.CLAUSE_TOPICS.values():
        chrome_words.add(v)
    rest = residual(ctext, cinfo["spans"], extra_known + ["Standing rules", "Definitions"] +
                    [p for p in lexd.get("q_prefixes", []) if p] + sorted(chrome_words, key=len, reverse=True))
    rest = re.sub(r"\(\d+\)|\*\*", " ", rest)
    # few-shot block chrome (formats-1 few-shot template data; repair r1): XML-like item tags first, then the
    # template headers in any card-style decoration (brackets, heading marks, trailing colon, upper case)
    rest = re.sub(r"</?[a-z_]+>", " ", rest)
    for hdr in _fewshot_headers():
        rest = re.sub(r"(?i)(?:^|(?<=\s))[\[#*=_]*\s*" + re.escape(hdr) + r"\s*[\]:*=_]*(?=\s|$)", " ", rest)
    rest = re.sub(r"(?:^|\s)(?:[-+*•·>=#|:()\[\]<>/^~]+|\d+(?:\.\d+)*[.)]?|Example(?: \d+)?:?|For example:|Sample:|"
                  r"Illustration:|\(e\.g\.|e\.g\.|Answer:|A:|Q:|Output:|Input:|Outcome:|Answer key:|Its answer:|"
                  r"Correct choice:|Decision:|Case \d+:|Past case \d+|Item \d+\.|Here is a case\.|=>|Yes|No|"
                  r"Worked examples|Solved cases|Examples|Sample input and output|Reference decisions|"
                  r"Past cases and their outcomes|Practice items with answers|Illustrations|Calibration examples|"
                  r"Rule \d+:|R\d+\.|\(\d+\)|Step \d+:|\u2192)(?=\s|$)", " ", " " + rest + " ")
    rest = re.sub(r"</?[a-z_]+>", " ", rest)
    if norm(rest):
        raise ParseError("card_residual:" + norm(rest)[:200])
    # --- state
    st = parse_state(fields["state"], style, skin, lx)
    typed = style["container"] in ("json", "yaml")
    ents, stmts, rules, hedges, ehedges, closures, blanks = {}, [], [], [], [], [], []
    attr_srcs = set()
    for kind, pl in st["items"]:
        if kind == "fact":
            for c in pl:
                if c[0] == "type":
                    if c[1] in ents and ents[c[1]] != c[2]:
                        raise ParseError("two_types")
                    ents[c[1]] = c[2]
                elif c[0] == "lit":
                    stmts.append(("lit", c[1], c[2], c[3], "sent"))
                elif c[0] == "val":
                    stmts.append(("val", c[2], c[1], c[3], "sent"))
                elif c[0] == "date":
                    stmts.append(("date", c[2], c[1], c[3], "sent"))
                elif c[0] == "link":
                    stmts.append(("link", c[1], c[2], c[3], "sent"))
        elif kind == "attr":
            src, frame, c = pl
            attr_srcs.add(src)
            prov = "attr:" + src
            if c[0] == "lit":
                stmts.append(("lit", c[1], c[2], c[3], prov))
            elif c[0] == "val":
                stmts.append(("val", c[2], c[1], c[3], prov))
            elif c[0] == "date":
                stmts.append(("date", c[2], c[1], c[3], prov))
            else:
                raise ParseError("attr_kind")
        elif kind == "rule":
            pl["where"] = "record"
            rules.append(pl)
        elif kind == "hedge":
            hedges.append(pl)
        elif kind == "ehedge":
            ehedges.append(pl)
        elif kind == "closure":
            closures.append(pl)
    tkinds = []
    for cols, rows in st["tables"]:
        te, ts, kinds = table_stmts(lx, cols, rows, typed)
        tkinds.append((kinds, te))
        for e, t in te:
            if e in ents and ents[e] != t:
                raise ParseError("two_types")
            ents[e] = t
        for s in ts:
            if s[0] == "blank":
                blanks.append((s[1], s[2]))
            else:
                stmts.append(s)
    # column closures: the closed column's table lists one type
    for c in closures:
        if c["form"] == "column":
            tys = None
            for kinds, te in tkinds:
                if any(k == ("pred", c["pred"]) for k in kinds):
                    tys = {t for _, t in te}
            if not tys or len(tys) != 1:
                raise ParseError("closure_table")
            c["typ"] = tys.pop()
    for p, e in blanks:
        if not any(c["form"] == "column" and c["pred"] == p for c in closures):
            raise ParseError("blank_open_column")
    # --- options / claim / gold
    opts = fields.get("options")
    defs = {}
    for ln in card_text.split("\n") if qtype == "choice" else []:
        if ln.startswith("- ") and ": " in ln:
            k, v = ln[2:].split(": ", 1)
            defs[k] = v
    claim = None
    out_opts = None
    none_shown = False
    gold = None
    C_ = lx.ID + r" is (not )?" + lx.P
    if form.startswith("YN"):
        if qtype != "noul":
            raise ParseError("qtype")
        claim = (qm.group(3), qm.group(1), qm.group(2) is None)
        gold = "yes" if fields["gold"] == 1 else "no"
    elif form == "CH-x":
        claim = (qm.group(3), qm.group(1), qm.group(2) is None)
        labs = []
        for o in opts:
            lab = None
            for st3 in L.CH3_OPTION_SETS:
                if o in st3:
                    lab = "FRO"[st3.index(o)]
            for st2 in L.CH2_OPTION_SETS:
                if o in st2:
                    lab = "FR"[st2.index(o)]
            if o in defs:
                d = defs[o]
                inv = {v: k for k, v in L.CH3_DEFS.items()}
                inv2 = {v: k for k, v in L.CH2_DEFS.items()}
                lab = inv.get(d) or inv2.get(d)
            if lab is None:
                raise ParseError("ch_option")
            labs.append(lab)
        form = "CH-3" if len(opts) == 3 else "CH-2"
        out_opts = labs
        gold = labs[opts.index(fields["gold"])]
    elif form == "CH-claim":
        out_opts = []
        for o in opts:
            if o == L.NONE_OPTION:
                none_shown = True
                out_opts.append(None)
                continue
            m = re.fullmatch(C_, o)
            if not m:
                raise ParseError("claim_option")
            out_opts.append((m.group(3), m.group(1), m.group(2) is None))
        gold = "NONE" if fields["gold"] == L.NONE_OPTION else opts.index(fields["gold"])
    elif form == "CH-entity":
        for o in opts:
            if o not in lx.ids:
                raise ParseError("entity_option")
        out_opts = list(opts)
        claim = None
        gold = opts.index(fields["gold"])
        H = qm.group(2)
        tname = lx.type_pl[qm.group(1)]
    # --- flags
    cl = cinfo["clauses"]
    if "3s" in cl:
        world = "unspecified"
    elif "1" in cl and "3" in cl:
        world = "OW"
    elif "2" in cl and "3c" in cl:
        world = "CW"
    else:
        raise ParseError("world")
    if world == "unspecified":
        unless = "unspecified"
    elif "7a" in cl:
        unless = "strict"
    elif "7b" in cl:
        unless = "listc"
    elif world == "CW" and "6" in cl:
        unless = "cw"
    else:
        unless = "none"
    if "22" in cl:
        trust = ["list"] + list(cinfo["trusted"])
    elif "22b" in cl:
        trust = ["all"]
    else:
        trust = ["unspecified"]
    canon = {
        "flags": {"world": world, "unless": unless, "trust": trust, "clauses": sorted(cl)},
        "ents": sorted([e, t] for e, t in ents.items()),
        "stmts": sorted(_c(s) for s in stmts),
        "blank": sorted([p, e] for p, e in blanks),
        "rules": sorted(_crule(r) for r in rules + card_rules),
        "hedges": sorted(_c((h["kind"], h["typ"], list(h["cond"]), list(h["head"]))) for h in hedges),
        "ehedges": sorted(_c((h["kind"], h["e"], h["pred"])) for h in ehedges),
        "closures": sorted([c["pred"], c["typ"], c["form"]] for c in closures),
        "form": form,
        "claim": list(claim) if claim else None,
        "options": [list(o) if isinstance(o, tuple) else o for o in out_opts] if out_opts is not None else None,
        "none_shown": none_shown,
        "gold": gold,
    }
    if form == "CH-entity":
        canon["H"] = H
        canon["etype"] = tname
    info = {"frame": fp, "wording": wording, "persona": persona, "examples": examples, "fewshot": fs_cases,
            "attr_sources": sorted(attr_srcs), "live_type": sorted(cinfo["live_type"]), "q15": cinfo["q15"]}
    return canon, info


def _c(x):
    out = []
    for v in x:
        if isinstance(v, Decimal):
            out.append(format(v, "f"))
        elif isinstance(v, dt.date):
            out.append(v.isoformat())
        elif isinstance(v, (list, tuple)):
            out.append(_c(v))
        else:
            out.append(v)
    return out


def _crule(r):
    conds = sorted(_c(c) for c in r.get("conds", []))
    return _c([r["form"], r["typ"], conds, list(r["head"]), r.get("ante"), r.get("exc"), r.get("link"),
               r.get("ptyp"), list(r["pcond"]) if r.get("pcond") else None, r.get("k", 0), r.get("where", "record")])
