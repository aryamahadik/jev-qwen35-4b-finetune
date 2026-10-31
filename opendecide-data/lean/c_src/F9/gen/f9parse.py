"""G3 parser (1.6): reads a rendered F9 row back, written from the spec's grammar (closed comparator list, closed time
grammar, container grammars, T21 value formats), with field separation:
  - the clause parser reads only the card text (row `card` on yes/no rows; on choice rows the part of `instructions`
    outside the core located by the row's wording and its fmt1 instruction position);
  - container and value parsers read only `state` plus the handed parameters (T3 / T21 / T28 / T34, legend);
  - the question parser reads only the question sentence; the option parser reads only `options`.
Output: the stated SEM, the tables (typed values), the query AST, the option payloads and the solver-B context.
"""
from __future__ import annotations

import csv
import datetime as dt
import html as htmlmod
import io
import json
import re
from fractions import Fraction
from html.parser import HTMLParser

import yaml

from f9fmt import (DATE_FORMATS, DATE_RE, NUM_FORMATS, TIME_FORMATS, TIME_RE, num_regex, parse_date, parse_dt,
                   parse_num, parse_zone, to_frac, month_bounds, epoch_of_local)
from f9lex import (CBD, CMP_T10, CMP_T35, MONTHS, NONE_OPT, is_banned, is_marker_value)


class ParseError(Exception):
    pass


def fail(why):
    raise ParseError(why)


# ------------------------------------------------------------------------------------------------ instructions
def split_instructions(row, wording, style, reg_q_prefix):
    """(card_text or None, question). The core = wording + question in the style's instruction-position order."""
    ins = row["instructions"]
    ip = style["ip"]
    w = wording
    i = ins.rfind(w)
    if i < 0:
        fail("wording not found")
    if ip in ("IP1", "IP2", "IP4", "IP5"):
        joiner = {"IP1": "\n\n", "IP2": " ", "IP4": "\n", "IP5": "\n\n"}[ip]
        rest = ins[i + len(w):]
        if not rest.startswith(joiner):
            fail("joiner")
        rest = rest[len(joiner):]
        if ip == "IP1" and reg_q_prefix:
            if not rest.startswith(reg_q_prefix + " "):
                fail("q prefix")
            rest = rest[len(reg_q_prefix) + 1:]
        task = None
        if ip == "IP5" and row["qtype"] == "choice":
            j = rest.rfind("\n\n")
            if j >= 0:
                task = rest[j + 2:]
                rest = rest[:j]
        q = rest
        head = ins[:i]
    else:  # IP3: question then wording
        head_all = ins[:i]
        if not head_all.endswith("\n\n"):
            fail("joiner")
        head_all = head_all[:-2]
        j = head_all.rfind("\n\n")
        qpart = head_all[j + 2:] if j >= 0 else head_all
        head = head_all[:j + 2] if j >= 0 else ""
        if reg_q_prefix:
            if not qpart.startswith(reg_q_prefix + " "):
                fail("q prefix")
            qpart = qpart[len(reg_q_prefix) + 1:]
        q = qpart
        task = None
    card_text = None
    if row["qtype"] == "choice":
        head = head.rstrip("\n")
        if ip == "IP4" and head:
            card_text = head
        else:
            card_text = head or None
        if task:
            card_text = (card_text + "\n\n" + task) if card_text else task
    else:
        card_text = row.get("card")
    if "\n" in q:
        fail("question spans lines")
    return card_text, q


# ------------------------------------------------------------------------------------------------ card clauses
def _clean_card(text):
    """Strip card-style chrome: quote prefixes, item / step markers, xml tags, bold marks, table pipes."""
    out = []
    for ln in (text or "").split("\n"):
        s = ln.strip()
        if s.startswith(">"):
            s = s[1:].strip()
        s = re.sub(r"^</?[a-z0-9_]+>$", "", s)
        s = s.replace("**", "")
        s = re.sub(r"^(?:[-*•]\s+|\d+[.)]\s+|\(\d+\)\s+|R\d+\.\s+|Rule \d+:\s+)", "", s)
        out.append(s)
    return "\n".join(out)


TERM_T7 = re.compile(r"A (?P<rec>[a-z][a-z ]*?) counts as (?P<t>[a-z][a-z ]*?) if its (?P<A>.+?), unless its "
                     r"(?P<B>.+?)\. No other (?P=rec) counts as (?P=t)\.")
TERM_T8 = re.compile(r"A (?P<rec>[a-z][a-z ]*?) counts as (?P<t>[a-z][a-z ]*?) only if its (?P<A>.+?)\. Every "
                     r"(?P=rec) whose (?P<A2>.+?) and whose (?P<C>.+?) counts as (?P=t)\. No other (?P=rec) counts "
                     r"as (?P=t)\.")
TERM_T9 = re.compile(r"A (?P<rec>[a-z][a-z ]*?) counts as (?P<t>[a-z][a-z ]*?) exactly when all of the following "
                     r"hold: (?P<L>.+?)\.(?:\s|$|\|)")
OVERRIDE = re.compile(r"For (?P<v>[A-Za-z][A-Za-z ]*?) (?P<recs>[a-z][a-z ]*?), (?P<t>[a-z][a-z ]*?) means its "
                      r"(?P<c>.+?) instead\.")


def parse_card(text, sampler_hint=None):
    """The stated SEM and the parameters handed to the value / question parsers."""
    c = {"stated": set()}
    if not text:
        return c
    t = _clean_card(text)
    flat = re.sub(r"\s+", " ", t)
    if re.search(r"The (?:data|log|report) lists every ", flat):
        c["world"] = "T1"
        m = re.search(r"has the answer '(no such [a-z ]+?)'", flat)
        if m:
            c["no_record"] = m.group(1)
    if "The data may not list every" in flat:
        if c.get("world"):
            fail("two world clauses")
        c["world"] = "T2"
    m = re.search(r"'(unknown|not recorded)' means the value is not known\. A value of 0 is a real zero\.", flat)
    if m:
        c["null"] = m.group(1)
    elif "null means the value is not known. A value of 0 is a real zero." in flat:
        c["null"] = "null"
    if "is left out of that question: it is not counted, added, averaged, compared, listed or picked." in flat:
        c["missing"] = "T4"
    if "A value that is not known could be any allowed value. If the answer depends on it, the answer cannot be " \
       "determined. Allowed values: " in flat:
        if c.get("missing"):
            fail("T4 and T5")
        c["missing"] = "T5"
        seg = flat.split("Allowed values: ", 1)[1].split(" Known values follow the same limits.", 1)[0]
        c["t5"] = seg
    m = re.search(r"Dates are written (YYYY-MM-DD|YYYY/MM/DD|DD\.MM\.YYYY|D MMM YYYY|D MMMM YYYY)\.", flat)
    if m:
        c["df"] = {v: k for k, v in DATE_FORMATS.items()}[m.group(1)]
    m = re.search(r"(No mark|'[.,]') splits thousands, and '([.,])' marks decimals\.", flat)
    if m:
        th = "" if m.group(1) == "No mark" else m.group(1)[1]
        c["nf"] = {("", "."): "plain", (",", "."): "comma", (".", ","): "euro"}[(th, m.group(2))]
    m = re.search(r"Times are written (HH:MM|HH:MM:SS), 24-hour, in (UTC[+-]\d{2}:\d{2})\.", flat)
    if m:
        c["tf"] = {v: k for k, v in TIME_FORMATS.items()}[m.group(1)]
        c["zone"] = parse_zone(m.group(2))
    m = re.search(r"In CSV blocks, fields are separated by (commas|semicolons|tabs)\.", flat)
    if m:
        c["csv"] = {"commas": ",", "semicolons": ";", "tabs": "\t"}[m.group(1)]
    units = {}
    for m in re.finditer(r"(?:^|(?<=[.:|=] )|(?<=[Uu]nits )|(?<=UNITS ))([a-z][a-z_.]*[a-z]) is in (\S+?)\.(?=\s|$)",
                         flat):
        units[m.group(1)] = m.group(2)
    c["units"] = units
    conv = {}
    for m in re.finditer(r"1 (\S+) = (\d+) (\S+)\.", flat):
        conv[f"{m.group(1)}->{m.group(3)}"] = m.group(2)
    c["conv"] = conv
    bools = {}
    for m in re.finditer(r"In ([a-z_]+), (true|1) means yes and (false|0) means no\.", flat):
        bools[m.group(1)] = "tf" if m.group(2) == "true" else "10"
    if bools:
        c["bool"] = list(bools.values())[0]
    ph = set()
    for m in re.finditer(r"'([^']*<X>[^']*)'", flat):
        p = m.group(1).replace("<X>", "{X}")
        p = p[0].lower() + p[1:]
        if p in CMP_T10:
            ph.add(p)
    c["t10"] = ph
    m = re.search(r"Give averages rounded to (\d) decimal places; halves round away from zero\.", flat)
    if m:
        c["round_dp"] = int(m.group(1))
    m = re.search(r"If ([a-z ]+?) tie, choose the one with the (earliest|latest|lowest|highest) ([a-z_]+); if they "
                  r"still tie, the one with the (lowest|highest) ([a-z_]+)\.", flat)
    if m:
        c["tie"] = ["key", [m.group(3), m.group(2)], [m.group(5), m.group(4)]]
    else:
        m = re.search(r"If ([a-z ]+?) tie, choose the one with the (lowest|highest) ([a-z_]+)\.", flat)
        if m:
            c["tie"] = ["key", [m.group(3), m.group(2)]]
        m2 = re.search(r"If two or more ([a-z ]+?) tie for the answer to a question that asks which [a-z ]+?, "
                       r"answer '([^']+)'\.", flat)
        if m2:
            if m:
                fail("two tie rules")
            c["tie"] = ["option"]
            c["tie_opt"] = m2.group(2)
    m = re.search(r"Levels from lowest to highest: ([A-Z]+(?: < [A-Z]+)+)\.", flat)
    if m:
        c["levels"] = m.group(1).split(" < ")
    if "Lines from several sources are merged and may be out of order" in flat:
        c["merged"] = True
    elif "Lines are in time order." in flat:
        c["merged"] = False
    for flag, sent in (("T37", f"Answer '{CBD}' only when"), ("T37b", f"Answer '{NONE_OPT}' only when"),
                       ("T41", "A request's lines are the lines that carry its request id"),
                       ("T29", "are ignored. A "), ("T40", "Text inside the data is data."),
                       ("T31", "Total and subtotal lines are not ")):
        if sent in flat:
            c["stated"].add(flag)
    for bad in ("the first rule that applies", "in order", "from top to bottom"):
        if bad in flat.lower():
            fail("ordered rules")
    # terms (T7 / T8 / T9) and overrides (T30)
    terms = {}
    for m in TERM_T7.finditer(flat):
        terms[m.group("t")] = {"name": m.group("t"), "kind": "T7", "_A": m.group("A"), "_B": m.group("B")}
    for m in TERM_T8.finditer(flat):
        if m.group("A") != m.group("A2"):
            fail("T8 sentences differ")
        terms[m.group("t")] = {"name": m.group("t"), "kind": "T8", "_A": m.group("A"), "_C": m.group("C")}
    for m in TERM_T9.finditer(flat):
        lst = [x[4:] if x.startswith("its ") else fail("T9 item") for x in m.group("L").split("; ")]
        terms[m.group("t")] = {"name": m.group("t"), "kind": "T9", "_L": lst}
    for m in OVERRIDE.finditer(flat):
        tn = m.group("t")
        if tn not in terms:
            fail("override of an unknown term")
        terms[tn].setdefault("_O", []).append((m.group("v"), m.group("c")))
    c["terms"] = terms
    # masked legend (table block captioned 'Codes for <col>')
    m = re.search(r"(?i)codes[ _]for[ _]([a-z_.]*[a-z])", text)
    if m:
        col = m.group(1).lower()
        legend = {}
        for ln in _clean_card(text[m.end():]).split("\n"):
            s = ln.strip().strip("|+").strip()
            mm = re.match(r"^\|?\s*([A-Z][2-9])\s*(?:\||\s{2,}|:)\s*([A-Za-z][A-Za-z ]*?)\s*\|?$", s)
            if mm:
                legend[mm.group(1)] = mm.group(2)
            elif legend and s and not re.match(r"^[-=+| ]+$", s) and not s.lower().startswith("code"):
                break
        c["legend"] = {"col": col, "codes": legend}
    c["flat"] = flat
    return c


# ------------------------------------------------------------------------------------------------ values
class Fmt:
    def __init__(self, c, sampler):
        self.nf = c.get("nf", "plain")
        self.df = c.get("df", "iso")
        self.tf = c.get("tf", "hm")
        self.zone = c.get("zone", 0)
        self.null = c.get("null")
        self.bool = c.get("bool", "tf")
        self.csv = c.get("csv", ",")
        self.units = c.get("units", {})
        self.legend = c.get("legend")


def typed_cell(s, fm: Fmt):
    """Untyped cell -> (kind, value): UNK, num-string, date, bool, str."""
    s0 = s.strip()
    if s0 == "":
        fail("blank cell")
    if is_banned(s0):
        fail("banned marker")
    if fm.null and s0 == fm.null:
        return ("UNK", None)
    return ("raw", s0)


def type_column(name, unit, raws, fm: Fmt):
    """Decide a column's type from its header and its cells (one stated format each)."""
    vals = [r for r in raws if r is not None]
    if not vals:
        fail(f"column {name} all unknown")
    if unit is not None:
        dp = None
        out = []
        for v in raws:
            if v is None:
                out.append(None)
                continue
            q = parse_num(v, fm.nf)
            d = len(v.split(NUM_FORMATS[fm.nf][1])[1]) if NUM_FORMATS[fm.nf][1] in v else 0
            if dp is None:
                dp = d
            elif d != dp:
                fail("mixed decimals")
            out.append(q)
        return {"name": name, "type": "num", "unit": unit, "dp": dp}, out
    if re.fullmatch(r"[A-Z]{2,3}-\d{4}", vals[0]) and all(re.fullmatch(r"[A-Z]{2,3}-\d{4}", v) for v in vals):
        return {"name": name, "type": "id"}, list(raws)
    if all(re.fullmatch(DATE_RE[fm.df], v) for v in vals):
        return {"name": name, "type": "date"}, [None if v is None else parse_date(v, fm.df) for v in raws]
    toks = ("true", "false") if fm.bool == "tf" else ("1", "0")
    if all(v in toks for v in vals):
        return {"name": name, "type": "bool"}, [None if v is None else v == toks[0] for v in raws]
    for v in vals:
        if is_marker_value(v):
            fail("marker-shaped value")
    out = list(raws)
    if fm.legend and fm.legend["col"] == name:
        codes = fm.legend["codes"]
        out = [None if v is None else (codes[v] if v in codes else fail("code not in legend")) for v in raws]
    return {"name": name, "type": "cat"}, out


def split_header(h):
    m = re.fullmatch(r"([a-z][a-z_]*[a-z])\s?\(([^)]+)\)", h)
    if m:
        return m.group(1), m.group(2)
    if not re.fullmatch(r"[a-z][a-z_]*[a-z]", h):
        fail("bad header")
    return h, None


# ------------------------------------------------------------------------------------------------ containers
class _HT(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.cur, self.cell, self.inc = [], None, None, False

    def handle_starttag(self, tag, attrs):
        if attrs:
            fail("html attrs")
        if tag == "tr":
            self.cur = []
        elif tag in ("td", "th"):
            self.cell = ""
            self.inc = True

    def handle_endtag(self, tag):
        if tag in ("td", "th"):
            self.cur.append(self.cell)
            self.inc = False
        elif tag == "tr":
            self.rows.append(self.cur)

    def handle_data(self, d):
        if self.inc:
            self.cell += d


def parse_grid(kind, body, fm: Fmt):
    """-> (headers, rows of raw strings or None)."""
    if kind == "md":
        lines = [ln for ln in body.split("\n") if ln.strip()]
        rows = []
        for ln in lines:
            if not (ln.startswith("| ") and ln.endswith(" |")):
                fail("md row")
            cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", ln[1:-1])]
            rows.append(cells)
        if not all(c == "---" for c in rows[1]):
            fail("md separator")
        hdr, data = rows[0], rows[2:]
    elif kind == "csv":
        rd = csv.reader(io.StringIO(body), delimiter=fm.csv)
        rows = [r for r in rd]
        hdr, data = rows[0], rows[1:]
    elif kind == "html":
        p = _HT()
        p.feed(body)
        hdr, data = p.rows[0], p.rows[1:]
    elif kind == "fw":
        lines = body.split("\n")
        h = lines[0]
        starts = [m.start() for m in re.finditer(r"(?:^|(?<=  ))\S", h)]
        hdr = h.split()
        if len(hdr) != len(starts):
            fail("fw header")
        data = []
        for ln in lines[1:]:
            cells = []
            for j, s0 in enumerate(starts):
                e = starts[j + 1] if j + 1 < len(starts) else None
                seg = ln[s0:e] if e else ln[s0:]
                if j + 1 < len(starts) and not seg.endswith("  ") and len(ln) > e:
                    fail("fw separator")
                cells.append(seg.strip())
            data.append(cells)
    elif kind == "kv":
        blocks = [b for b in body.split("\n\n") if b.strip()]
        hdr, data = None, []
        for b in blocks:
            ks, vs = [], []
            for ln in b.split("\n"):
                if ": " not in ln:
                    fail("kv line")
                k, v = ln.split(": ", 1)
                ks.append(k)
                vs.append(v)
            if hdr is None:
                hdr = ks
            elif ks != hdr:
                fail("kv keys differ")
            data.append(vs)
    else:
        fail("grid kind")
    if any(len(r) != len(hdr) for r in data):
        fail("ragged")
    return hdr, data


def table_from_grid(hdr, data, fm, role):
    cols, colvals = [], []
    for j, h in enumerate(hdr):
        name, unit = split_header(h)
        raws = []
        for r in data:
            k, v = typed_cell(r[j], fm)
            raws.append(v)
        c, vals = type_column(name, unit, raws, fm)
        cols.append(c)
        colvals.append(vals)
    rows = [list(x) for x in zip(*colvals)] if data else []
    return {"role": role, "cols": cols, "rows": rows}


FENCE = re.compile(r"^```(csv|table|records|json|jsonl|yaml|log)\n(.*?)\n```$", re.S)


def find_blocks(state):
    """Container finder: code fences, HTML tables, markdown blocks and 4-space indented blocks."""
    out = []
    parts = re.split(r"\n\n(?=```|<table>|\| |    \S|[A-Z][a-z ]*:\n)", state)
    for p in parts:
        p2 = p.strip("\n")
        m = FENCE.match(p2)
        if m:
            out.append((m.group(1), m.group(2)))
        elif p2.startswith("<table>") and p2.endswith("</table>"):
            out.append(("html", p2))
        elif p2.startswith("| "):
            out.append(("md", p2))
        elif p2.startswith("    "):
            out.append(("indent", "\n".join(ln[4:] for ln in p2.split("\n"))))
        elif re.fullmatch(r"[A-Z][a-z ]*:", p2):
            out.append(("caption", p2[:-1]))
        elif re.match(r"^[a-z_]+ by [a-z ]+ and week, in \S+:$", p2):
            out.append(("pivot_caption", p2))
        else:
            fail("unfenced prose")
    return out


KIND = {"csv": "csv", "table": "fw", "records": "kv", "md": "md", "html": "html"}


class JNum(str):
    """A JSON / YAML number literal, kept as its exact text (native numbers only; F9-R1-05)."""


def _yaml_nodes(node):
    import yaml.nodes as N
    if isinstance(node, N.SequenceNode):
        return [_yaml_nodes(x) for x in node.value]
    if isinstance(node, N.MappingNode):
        out = {}
        for k, v in node.value:
            out[k.value] = _yaml_nodes(v)
        return out
    if node.style == '"':
        return node.value
    if node.style is None:
        v = node.value
        if v == "null":
            return None
        if v in ("true", "false"):
            return v == "true"
        if v == "[]":
            return []
        if re.fullmatch(r"-?\d+(?:\.\d+)?", v):
            return JNum(v)
        fail("plain YAML scalar that is not a number, bool or null")
    fail("YAML scalar style")


def parse_s4(kind, body, fm: Fmt):
    if kind == "json":
        try:
            data = json.loads(body, parse_float=JNum, parse_int=JNum)
        except json.JSONDecodeError:
            fail("json")
    elif kind == "jsonl":
        data = []
        for ln in body.split("\n"):
            try:
                data.append(json.loads(ln, parse_float=JNum, parse_int=JNum))
            except json.JSONDecodeError:
                fail("jsonl")
    else:
        try:
            node = yaml.compose(body)
        except yaml.YAMLError:
            fail("yaml")
        data = _yaml_nodes(node)
    if not isinstance(data, list) or not data or not all(isinstance(r, dict) for r in data):
        fail("s4 shape")
    keys = list(data[0].keys())
    for r in data:
        if list(r.keys()) != keys:
            fail("missing key on a non-T6 card")
    cols, rows = [], [[] for _ in data]
    for k in keys:
        v0 = [r[k] for r in data]
        if any(isinstance(v, dict) for v in v0):
            sub = list(next(v for v in v0 if isinstance(v, dict)).keys())
            for k2 in sub:
                raws = []
                for v in v0:
                    if not isinstance(v, dict) or list(v.keys()) != sub:
                        fail("nested object shape")
                    raws.append(v[k2])
                c, vals = _s4_col(f"{k}.{k2}", raws, fm)
                cols.append(c)
                for i, x in enumerate(vals):
                    rows[i].append(x)
        elif any(isinstance(v, list) for v in v0):
            subk = None
            lv = []
            for v in v0:
                if v is None:
                    lv.append(None)
                    continue
                if not isinstance(v, list):
                    fail("list type")
                items = []
                for it in v:
                    if not isinstance(it, dict):
                        fail("sub-item")
                    if subk is None:
                        subk = list(it.keys())
                    if list(it.keys()) != subk:
                        fail("sub-item keys")
                    items.append([it[x] for x in subk])
                lv.append(items)
            subcols = []
            if subk:
                for j, sk in enumerate(subk):
                    raws = [it[j] for v in lv if v for it in v]
                    c, _ = _s4_col(sk, raws, fm)
                    subcols.append(c)
                lv = [None if v is None else [[_s4_val(x, subcols[j]) for j, x in enumerate(it)] for it in v]
                      for v in lv]
            cols.append({"name": k, "type": "list", "sub": subcols})
            for i, x in enumerate(lv):
                rows[i].append(x)
        else:
            c, vals = _s4_col(k, v0, fm)
            cols.append(c)
            for i, x in enumerate(vals):
                rows[i].append(x)
    return {"role": "main", "cols": cols, "rows": rows}


def _s4_col(name, raws, fm):
    vals = [v for v in raws if v is not None]
    if not vals:
        fail("all null")
    if all(isinstance(v, bool) for v in vals):
        return {"name": name, "type": "bool"}, list(raws)
    if all(isinstance(v, JNum) for v in vals):
        dp = max((len(v.split(".")[1]) if "." in v else 0) for v in vals)
        if any((len(v.split(".")[1]) if "." in v else 0) != dp for v in vals):
            fail("mixed decimals")
        return {"name": name, "type": "num", "unit": None, "dp": dp}, [None if v is None else _s4_val(v, {"type": "num"})
                                                                       for v in raws]
    if all(isinstance(v, str) and not isinstance(v, JNum) for v in vals):
        if all(re.fullmatch(r"[A-Z]{2,3}-\d{4}", v) for v in vals) and len(vals) == len(raws):
            return {"name": name, "type": "id"}, list(raws)
        if all(re.fullmatch(DATE_RE[fm.df], v) for v in vals):
            return {"name": name, "type": "date"}, [None if v is None else parse_date(v, fm.df) for v in raws]
        for v in vals:
            if is_marker_value(v) or is_banned(v) or v == "":
                fail("marker-shaped value")
            if re.fullmatch(r"-?\d+(?:[.,]\d+)?", v):
                fail("numeric field written as a string")
        out = list(raws)
        if fm.legend and fm.legend["col"] == name:
            out = [None if v is None else (fm.legend["codes"][v] if v in fm.legend["codes"] else fail("code"))
                   for v in raws]
        return {"name": name, "type": "cat"}, out
    fail("mixed field types")


def _s4_val(x, c):
    if x is None:
        return None
    if c["type"] == "num":
        from decimal import Decimal
        return Fraction(Decimal(str(x)))
    return x


LOG_RES = {
    "bracket": r"^\[(?P<t>.+?)\] \[(?P<lv>[A-Z]+)\] (?P<c>[A-Z]{2}-\d{2}): (?P<rest>.*)$",
    "isocomp": r"^(?P<t>{DT}) (?P<c>[A-Z]{2}-\d{2}) (?P<lv>[A-Z]+) (?P<rest>.*)$",
    "kv": r'^time="(?P<t>.+?)" level=(?P<lv>[A-Z]+) component=(?P<c>[A-Z]{2}-\d{2}) msg="(?P<msg>[^"]*)"(?P<kv>(?: \w+=\S+)*)$',
    "syslog": r"^(?P<t>{DT}) (?P<c>[A-Z]{2}-\d{2})\[(?P<lv>[A-Z]+)\]: (?P<rest>.*)$",
}


def parse_log(body, fm: Fmt):
    dtre = DATE_RE[fm.df] + " " + TIME_RE[fm.tf]
    res = {k: re.compile(v.replace("{DT}", dtre)) for k, v in LOG_RES.items()}
    lines = body.split("\n")
    syn = None
    rows = []
    keys = {}
    for ln in lines:
        hits = [k for k, r in res.items() if r.match(ln)]
        if len(hits) != 1:
            fail("log line matches no syntax or two")
        if syn is None:
            syn = hits[0]
        elif hits[0] != syn:
            fail("two syntaxes")
        m = res[syn].match(ln)
        t = parse_dt(m.group("t"), fm.zone, fm.df, fm.tf)
        if syn == "kv":
            msg, kvs = m.group("msg"), m.group("kv")
        else:
            rest = m.group("rest")
            mm = re.match(r"^(?P<msg>[^=]*?)(?P<kv>(?: \w+=\S+)*)$", rest)
            if not mm:
                fail("log message")
            msg, kvs = mm.group("msg"), mm.group("kv")
        kv = {}
        for p in kvs.split():
            k, v = p.split("=", 1)
            kv[k] = v
            keys.setdefault(k, None)
        rows.append({"time": t, "level": m.group("lv"), "component": m.group("c"), "message": msg, "kv": kv})
    return syn, rows, list(keys)


def parse_pivot(body, fm):
    lines = [ln for ln in body.split("\n") if ln.strip()]
    rows = []
    for ln in lines:
        if not (ln.startswith("| ") and ln.endswith(" |")):
            fail("pivot row")
        rows.append([c.strip() for c in ln[1:-1].split("|")])
    hdr = rows[0]
    periods = hdr[1:]
    ents, cells, marks, groups, cur = [], {}, [], [], []
    printed = []
    for r in rows[2:]:
        lab = r[0]
        if lab in ("Subtotal", "Total"):
            printed.append((lab, [int(x) for x in r[1:]], list(cur)))
            if lab == "Subtotal":
                groups.append(cur)
                cur = []
            continue
        ents.append(lab)
        cur.append(lab)
        vals = []
        for j, x in enumerate(r[1:]):
            if x.endswith("*"):
                marks.append([lab, j])
                x = x[:-1]
            vals.append(int(x))
        cells[lab] = vals
    # T31 re-addition of printed totals (unmarked values; a subtotal back to the previous subtotal line)
    mk = {tuple(m) for m in marks}
    for lab, vals, grp in printed:
        for j in range(len(periods)):
            if lab == "Subtotal":
                s = sum(cells[e][j] for e in grp if (e, j) not in mk)
            else:
                s = sum(cells[e][j] for e in ents if (e, j) not in mk)
            if s != vals[j]:
                fail("printed total does not re-add")
    return {"entities": ents, "periods": periods, "cells": cells, "marks": marks, "groups": groups,
            "ent_label": hdr[0]}


# ------------------------------------------------------------------------------------------------ predicates
CMP_ITEMS = sorted(CMP_T10.items(), key=lambda kv: -len(kv[0]))


class QP:
    """Question / definition grammar (1.2) over the parsed columns."""

    def __init__(self, cols, fm: Fmt, card):
        self.cols = cols  # name -> {"type", "unit", "role", "dp"}
        self.fm = fm
        self.card = card

    def amount(self, s, col=None):
        m = re.fullmatch(f"({num_regex(self.fm.nf)}) (\\S+)", s)
        if not m:
            fail("amount without unit")
        unit = m.group(2)
        cu = self.cols[col]["unit"] if col and self.cols.get(col) else None
        ok_units = {cu} | {k.split("->")[0] for k in self.card.get("conv", {})} | {
            k.split("->")[1] for k in self.card.get("conv", {})} | set(self.fm.units.values())
        if unit not in ok_units and cu is not None:
            fail("literal unit not stated")
        return parse_num(m.group(1), self.fm.nf), unit

    def count_lit(self, s):
        if not re.fullmatch(num_regex(self.fm.nf), s):
            fail("count literal")
        return parse_num(s, self.fm.nf)

    def cmp_phrase(self, s, amount=True, col=None):
        """'<phrase with X>' -> (op, X, unit, phrase)."""
        for ph, op in CMP_ITEMS:
            pre, post = ph.split("{X}")
            if s.startswith(pre) and s.endswith(post):
                x = s[len(pre):len(s) - len(post)] if post else s[len(pre):]
                x = x.strip()
                if not x:
                    continue
                try:
                    if amount:
                        v, u = self.amount(x, col)
                    else:
                        v, u = self.count_lit(x), None
                except ParseError:
                    continue
                if self.card.get("t10") is not None and self.card.get("check_t10") and ph not in self.card["t10"]:
                    fail("comparator not stated on the card")
                return op, v, u, ph
        fail("comparator outside the closed list")

    def atom(self, s, role_cols=None):
        m = re.match(r"^([a-z][a-z_.]*[a-z]) (is|contains) (.+)$", s)
        if not m:
            fail("atom")
        col, verb, rest = m.group(1), m.group(2), m.group(3)
        if col not in self.cols:
            fail(f"unknown column {col}")
        c = self.cols[col]
        if verb == "contains":
            mm = re.fullmatch(r'"([^"]+)"', rest)
            if not mm:
                fail("contains literal")
            return {"k": "contains", "col": col, "s": mm.group(1)}
        t = c["type"]
        if t == "num":
            mm = re.fullmatch(r"between (.+?) and (.+)", rest)
            if mm:
                lo, u1 = self.amount(mm.group(1), col)
                hi, u2 = self.amount(mm.group(2), col)
                if u1 != u2:
                    fail("between units")
                return {"k": "between", "col": col, "lo": lo, "hi": hi, "unit": u1}
            op, v, u, ph = self.cmp_phrase(rest, True, col)
            return {"k": "cmp", "col": col, "op": op, "lit": v, "unit": u}
        if t == "cat":
            if rest.startswith("not equal to "):
                return {"k": "cmp", "col": col, "op": "!=", "lit": rest[13:]}
            mm = re.fullmatch(r"neither (.+?) nor (.+)", rest)
            if mm:
                return {"k": "not", "arg": {"k": "in", "col": col, "vals": [mm.group(1), mm.group(2)]}}
            if rest.startswith("not "):
                return {"k": "not", "arg": {"k": "cmp", "col": col, "op": "=", "lit": rest[4:]}}
            mm = re.fullmatch(r"(.+?) or (.+)", rest)
            if mm:
                return {"k": "in", "col": col, "vals": [mm.group(1), mm.group(2)]}
            return {"k": "cmp", "col": col, "op": "=", "lit": rest}
        if t == "date":
            return {"k": "win", "col": col, **self.time_phrase(rest, "date")}
        fail("atom type")

    def time_phrase(self, s, typ):
        D = DATE_RE[self.fm.df]
        pd = lambda x: parse_date(x, self.fm.df)  # noqa: E731
        m = re.fullmatch(f"from ({D}) to ({D})", s)
        if m:
            return {"lo": pd(m.group(1)), "hi": pd(m.group(2)), "li": True, "hi_i": True, "unit": "day", "step": 1}
        m = re.fullmatch(f"on or before ({D})", s)
        if m:
            return {"lo": None, "hi": pd(m.group(1)), "li": True, "hi_i": True, "unit": "day", "step": 1}
        m = re.fullmatch(f"on or after ({D})", s)
        if m:
            return {"lo": pd(m.group(1)), "hi": None, "li": True, "hi_i": True, "unit": "day", "step": 1}
        m = re.fullmatch(f"before ({D})", s)
        if m:
            return {"lo": None, "hi": pd(m.group(1)), "li": True, "hi_i": False, "unit": "day", "step": 1}
        m = re.fullmatch(f"after ({D})", s)
        if m:
            return {"lo": pd(m.group(1)), "hi": None, "li": False, "hi_i": True, "unit": "day", "step": 1}
        m = re.fullmatch(f"on ({D})", s)
        if m:
            d = pd(m.group(1))
            return {"lo": d, "hi": d, "li": True, "hi_i": True, "unit": "day", "step": 1}
        m = re.fullmatch(r"in (" + "|".join(MONTHS) + r") (\d{4})", s)
        if m:
            lo, hi = month_bounds(int(m.group(2)), MONTHS.index(m.group(1)) + 1)
            return {"lo": lo, "hi": hi, "li": True, "hi_i": True, "unit": "day", "step": 1}
        m = re.fullmatch(f"in the (\\d+) days ending on ({D})", s)
        if m:
            n, d = int(m.group(1)), pd(m.group(2))
            return {"lo": d - n + 1, "hi": d, "li": True, "hi_i": True, "unit": "day", "step": 1}
        if typ == "dt":
            T = DATE_RE[self.fm.df] + " " + TIME_RE[self.fm.tf]
            m = re.fullmatch(f"from ({T}) up to but not including ({T})", s)
            if m:
                return {"lo": parse_dt(m.group(1), self.fm.zone, self.fm.df, self.fm.tf),
                        "hi": parse_dt(m.group(2), self.fm.zone, self.fm.df, self.fm.tf), "li": True,
                        "hi_i": False, "unit": "sec", "step": 60 if self.fm.tf == "hm" else 1}
        fail("time phrase outside the closed grammar")

    def pred(self, s, lead="whose"):
        if not s.startswith(lead + " "):
            fail("pred lead")
        parts = s[len(lead) + 1:].split(f" and {lead} ")
        aa = [self.atom(p) for p in parts]
        neg = [i for i, a in enumerate(aa) if a["k"] == "not"]
        if neg and neg != [len(aa) - 1]:
            fail("negated part before an unnegated operand")
        if len(aa) == 2:
            c0 = aa[0].get("col") or aa[0]["arg"]["col"]
            c1 = aa[1].get("col") or aa[1]["arg"]["col"]
            if c0 == c1:
                fail("same-column AND")
        return aa[0] if len(aa) == 1 else {"k": "and", "args": aa}

    def def_cond(self, s):
        return self.atom(s)
