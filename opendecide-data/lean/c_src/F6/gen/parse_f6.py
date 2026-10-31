"""G3 round-trip parser for F6 rows, written from G0 section 3 and the 3.1 lexicon (not from the renderer).

It reads each field where section 1.1 puts it: the card field on yes/no rows; on choice rows the card blocks inside
`instructions` and the option-definition lines of the card field; the record in `state`. Containers are read from
the style's published spec (fmt1 data files: skins / card styles / registers / instruction positions), never from
fmt1 code. The switch-sentence table, option-wording table and question frames are read as data (lex.SW,
lex.OPTION_TEXT, lex.FRAMES) through this module's own matching code; the scans come from scan.py (3.1 lists).

Output: a name-keyed structure in the same schema the solvers read. Any banned phrase, unlisted line, unrecognised
switch sentence, unparseable rule or structural breach raises ParseError (a G3 failure = generator bug).
"""
from __future__ import annotations

import html as _html
import json
import re
from functools import lru_cache

from . import common  # noqa: F401  (sys.path for fmt1)
from fmt1 import pool as fpool          # data access only (published style specs)

from . import scan
from .lex import SW, OPTION_TEXT, FRAMES

ID_RX = r"[A-Z]{2,4}-\d{4}"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


class ParseError(ValueError):
    pass


# the F6-local S5 unknown markers registered in the XF06 marker table (c_src/common/markers.json v1.1, F6 row)
S5_DIALOGUE = ("don't know", "declined to answer", "can't recall")


# ---------------------------------------------------------------- dates (row 48)

def parse_date(s: str):
    import datetime as dt
    s = s.strip()
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        d = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    else:
        m = re.fullmatch(r"(\d{1,2}) (" + "|".join(MONTHS) + r") (\d{4})", s)
        if not m:
            raise ParseError(f"date format: {s[:30]!r}")
        d = dt.date(int(m.group(3)), MONTHS.index(m.group(2)) + 1, int(m.group(1)))
    return (d - dt.date(1970, 1, 1)).days


def parse_date_phrase(s: str):
    """Exact date, 'from a to b' (one unknown day) or 'in <Month> <Year> (<n> days)'."""
    import datetime as dt
    s = s.strip()
    m = re.fullmatch(r"from (.+) to (.+)", s)
    if m:
        return {"k": "range", "a": parse_date(m.group(1)), "b": parse_date(m.group(2))}
    m = re.fullmatch(r"in (" + "|".join(MONTHS) + r") (\d{4}) \((\d+) days\)", s)
    if m:
        y, mo, n = int(m.group(2)), MONTHS.index(m.group(1)) + 1, int(m.group(3))
        a = (dt.date(y, mo, 1) - dt.date(1970, 1, 1)).days
        nxt = dt.date(y + (mo == 12), mo % 12 + 1, 1)
        if (nxt - dt.date(y, mo, 1)).days != n:
            raise ParseError("days in month misstated")
        return {"k": "month", "y": y, "m": mo, "a": a, "b": a + n - 1}
    return {"k": "exact", "d": parse_date(s)}


# ---------------------------------------------------------------- the frozen tables as patterns

def _tpl_rx(t: str) -> re.Pattern:
    parts = re.split(r"(\{[A-Za-z0-9_]+\})", t)
    out, seen = [], set()
    for p in parts:
        m = re.fullmatch(r"\{([A-Za-z0-9_]+)\}", p)
        if m:
            nm = m.group(1)
            if nm in seen:
                out.append(f"(?P={nm})")
            else:
                seen.add(nm)
                out.append(f"(?P<{nm}>.*?)" if nm in ("clause", "blank") else f"(?P<{nm}>.+?)")
        else:
            out.append(re.escape(p))
    return re.compile("^" + "".join(out) + "$")


@lru_cache(maxsize=1)
def switch_patterns():
    return [(k, _tpl_rx(v)) for k, v in SW.items()]


def match_switch(line: str):
    hits = []
    for k, rx in switch_patterns():
        m = rx.match(line)
        if m:
            hits.append((k, m.groupdict()))
    if not hits:
        return None
    # prefer the most specific (fewest placeholders, longest literal)
    hits.sort(key=lambda h: (sum(len(v or "") for v in h[1].values()), -len(SW[h[0]])))
    return hits[0]


@lru_cache(maxsize=1)
def frame_patterns():
    return [(k, _tpl_rx(v)) for k, v in FRAMES.items()]


# ---------------------------------------------------------------- published style specs (data)

@lru_cache(maxsize=1)
def heading_words() -> set:
    out = set()
    for r in fpool._load("registers.jsonl"):
        for v in r["headings"].values():
            out.add(v.lower())
        out.add(r.get("memo_title", "").lower())
    return {x for x in out if x}


def _strip_heading(line: str) -> str:
    s = line.strip()
    s = re.sub(r"^#+\s*", "", s)
    s = re.sub(r"^\*\*(.*)\*\*$", r"\1", s)
    s = re.sub(r"^\[(.*)\]$", r"\1", s)
    s = re.sub(r"^<(/?)[a-z0-9_]+>$", "", s)
    s = re.sub(r"^\d+\.\s+", "", s)
    s = s.rstrip(":")
    return s.strip()


def is_heading(line: str) -> bool:
    s = _strip_heading(line)
    return s == "" or s.lower() in heading_words() or bool(re.fullmatch(r"[=\-^~]+", line.strip()))


BULLET_RX = re.compile(r"^(?:[-*•+·]\s+)")


def card_lines(text: str, style: dict) -> list[str]:
    """Card text -> content lines (card-style chrome removed: quote prefixes, xml tags, indentation, bullets)."""
    cs = fpool.card_style(style["card_style"])
    out = []
    for raw in (text or "").split("\n"):
        ln = raw
        if cs["wrapper"] == "quote":
            ln = re.sub(r"^>\s?", "", ln)
        ln = ln.strip()
        if not ln or re.fullmatch(r"```\w*", ln):
            continue
        if re.fullmatch(r"</?[a-z0-9_]+>", ln):
            continue
        if re.fullmatch(r"[=\-^~]{3,}", ln):
            continue
        ln = BULLET_RX.sub("", ln)
        out.append(ln)
    return out


# ---------------------------------------------------------------- record readers (state)

TITLE_RX = re.compile(r"(?:Form: |Internal memorandum \| |Quick memo \| |MEMO \| |MEMORANDUM \| )?"
                      r"(?:(?:[A-Za-z][A-Za-z ]* file|[A-Z][A-Z ]* FILE) " + ID_RX +
                      r"|[A-Za-z][A-Za-z ]* (?:timeline|TIMELINE|register|REGISTER|under review|UNDER REVIEW))")


def state_pairs(state: str, style: dict) -> tuple[list, list]:
    """(pairs [(key, value)], other text lines) from a fields-only record, per container."""
    sk = fpool.skin(style["skin"])
    cont = style["container"]
    p = sk.get("params", {})
    text = state
    pairs, other = [], []
    if cont == "html_snippet":
        t = re.sub(r"```\w*", "", text)
        for k, v in re.findall(r"<th[^>]*>(.*?)</th>\s*<td>(.*?)</td>", t, flags=re.S):
            pairs.append((_html.unescape(k).strip(), _html.unescape(v).strip()))
        for k, v in re.findall(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", t, flags=re.S):
            pairs.append((_html.unescape(k).strip(), _html.unescape(v).strip()))
        for x in re.findall(r"<p>(.*?)</p>", t, flags=re.S):
            other.append(_html.unescape(x).strip())
        for x in re.findall(r"<h\d>(.*?)</h\d>", t, flags=re.S):
            other.append(("TITLE", _html.unescape(x).strip()))
        return pairs, other
    if cont == "markdown_table":
        lines = text.split("\n")
        in_table = False
        head_seen = False
        for ln in lines:
            s = ln.strip()
            if s.startswith("|") and s.endswith("|"):
                cells = [c.strip() for c in s.strip("|").split("|")]
                if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    continue
                if not head_seen:
                    head_seen = True
                    continue
                if len(cells) != 2:
                    raise ParseError("fields table is not two columns")
                pairs.append((cells[0], cells[1]))
                in_table = True
            else:
                head_seen = False
                if not s:
                    continue
                if re.match(r"^(#+ |\*\*)", s):
                    other.append(("TITLE", re.sub(r"^#+ |\*\*", "", s).strip("*")))
                else:
                    other.append(s)
        return pairs, other
    lines = text.split("\n")
    if cont == "prose" and p.get("list_mode") == "inline":
        new = []
        for ln in lines:
            new += [x for x in re.split(r"(?<=\.)\s+(?=[A-Z])", ln) if x]
        lines = new
    for raw in lines:
        s = raw.strip()
        if not s or re.fullmatch(r"```\w*", s) or re.fullmatch(r"[=\-*]{3,}", s):
            continue
        s = BULLET_RX.sub("", s)
        s = re.sub(r"^\d+[.)]\s+", "", s)
        if TITLE_RX.fullmatch(s.strip("[]")):
            other.append(("TITLE", s))
            continue
        if cont == "prose" and s.endswith("."):
            body = s[:-1]
        else:
            body = s
        m = re.match(r"^(.+?) \.{3,} (.+)$", body)
        if m:
            pairs.append((m.group(1).strip(), m.group(2).strip()))
            continue
        m = re.match(r"^(.+?):\s+(.+)$", body)
        if m and not (cont == "prose" and not s.endswith(".")):
            v = m.group(2).strip()
            if cont == "form" and p.get("field", "").endswith("[ {value} ]"):
                mm = re.fullmatch(r"\[ (.+) \]", v)
                if not mm:
                    raise ParseError("form bracket value")
                v = mm.group(1)
            pairs.append((m.group(1).strip(), v))
            continue
        other.append(s)
    return pairs, other


# ---------------------------------------------------------------- instructions: wording + question

def split_instructions(instr: str, style: dict, wordings: set) -> tuple[str, str, str]:
    """(card text moved into instructions, wording, question) per the instruction position (published spec)."""
    ip = fpool.instr_position(style["instr_position"])
    reg = fpool.register(style["register"])
    text = instr.rstrip()
    q = None
    qrx = None
    for k, rx in frame_patterns():
        pass
    # the question is the last frame sentence in the text
    cands = []
    for k, v in FRAMES.items():
        pat = _tpl_rx(v).pattern[1:-1]
        for m in re.finditer(pat, text):
            cands.append((m.start(), m.end(), k, m.group(0)))
    inv = re.finditer(r"Is the outcome for " + ID_RX + r' "[^"]+"\?', text)
    for m in inv:
        cands.append((m.start(), m.end(), "qplain_inv", m.group(0)))
    for m in re.finditer(r"(?:Is|Was|Did|Does|Do|Has) [^?\n]*\?", text):
        cands.append((m.start(), m.end(), "inversion", m.group(0)))
    if not cands:
        raise ParseError("no question frame")
    cands.sort(key=lambda c: (c[0], -c[1]))
    # choose the frame match that ends last and is maximal at that end
    end = max(c[1] for c in cands)
    best = [c for c in cands if c[1] == end]
    best.sort(key=lambda c: c[0])
    s, e, kind, qtext = best[0]
    pre, post = text[:s], text[e:]
    pre_s = pre.rstrip()
    if ip["q_prefix"] and reg.get("q_prefix") and pre_s.endswith(reg["q_prefix"]):
        pre_s = pre_s[: -len(reg["q_prefix"])].rstrip()
    wording = None
    body = pre_s
    post_s = post.strip()
    if post_s:
        if post_s in wordings:
            wording = post_s
        else:
            raise ParseError("text after the question")
    else:
        for w in sorted(wordings, key=len, reverse=True):
            if body.endswith(w):
                wording = w
                body = body[: -len(w)].rstrip()
                break
    if wording is None:
        raise ParseError("instruction wording outside the approved pool")
    return body, wording, qtext


# ---------------------------------------------------------------- rules-kind card parsing

CMP_OPS = {"is at least": ">=", "is no fewer than": ">=", "is no less than": ">=", "is at most": "<=",
           "is no more than": "<=", "is more than": ">", "is above": ">", "exceeds": ">", "is fewer than": "<",
           "is less than": "<", "is below": "<"}
NUM_RX = re.compile(r"^the (?P<a>.+?) (?P<op>" + "|".join(sorted(map(re.escape, CMP_OPS), key=len, reverse=True))
                    + r") (?P<n>\d+) (?P<u>.+)$")
EV_RX = re.compile(r'^the (?P<s>.+?) (?P<v>had|did not have) an? "(?P<e>[^"]+)" event$')
CLS_RX = re.compile(r"^the (?P<s>.+?) is an? (?P<c>.+)$")
CAT_RX = re.compile(r"^the (?P<a>.+?) is (?P<v>.+)$")
RULE_RX = re.compile(r'^In (?P<nt>.+?), the outcome is "(?P<o>[^"]+)" if (?P<c>.+?)(?:, unless (?P<u>.+))?\.$')
NUM_PREFIX = re.compile(r"^(?:Rule (?P<a>\d+): |(?P<b>\d+)\. |\((?P<c>\d+)\) |R(?P<d>\d+)\. )")
EXC_RX = re.compile(r"^Exception to rule (?P<n>\d+)(?:, cell (?P<ca>.+?) / (?P<cb>.+?))?: (?P<r>.+)$")
OI_RX = re.compile(r'^The outcome is "(?P<o>[^"]+)" only if (?P<c>.+)\.$')
NOTICE_RX = re.compile(r"^(?P<n>.+?) takes effect on (?P<one>one day )?(?P<d>.+)\.$")
SUB_RX = re.compile(r"^Every (?P<b>.+?) is an? (?P<a>.+)\.$")
TLEAD_RX = re.compile(r"^Rule (?P<n>\d+): In (?P<nt>.+?), the outcome table below gives the outcome by the "
                      r"(?P<A>.+?) \(rows\) and the (?P<B>.+?) \(columns\)\.$")


def split_conds(c: str) -> list[str]:
    parts = c.split(" and ")
    # an event name in quotes may hold ' and '; re-join inside quotes
    out, buf = [], ""
    for p in parts:
        buf = p if not buf else buf + " and " + p
        if buf.count('"') % 2 == 0:
            out.append(buf)
            buf = ""
    if buf:
        raise ParseError("unbalanced quotes in a condition")
    return out


def parse_atom(t: str, ctx: dict) -> dict:
    m = NUM_RX.match(t)
    if m:
        a = m.group("a")
        if ctx["attrs"].get(a, {}).get("kind") not in (None, "num"):
            raise ParseError("attribute kind clash")
        u = m.group("u")
        if ctx["attrs"].get(a, {}).get("unit") not in (None, u):
            raise ParseError("unit clash")
        return {"t": "num", "a": a, "op": CMP_OPS[m.group("op")], "n": int(m.group("n"))}
    m = EV_RX.match(t)
    if m:
        ctx["nouns"].add(m.group("s"))
        return {"t": "ev", "e": m.group("e"), "neg": m.group("v") == "did not have"}
    m = CLS_RX.match(t)
    if m and m.group("c").endswith(" " + m.group("s")):
        ctx["nouns"].add(m.group("s"))
        return {"t": "cls", "c": m.group("c")}
    m = CAT_RX.match(t)
    if m:
        if " not " in f" {m.group('v')} ":
            raise ParseError("'not' on a category atom")
        return {"t": "cat", "a": m.group("a"), "v": m.group("v")}
    raise ParseError(f"unparseable condition: {t[:60]!r}")


def parse_rule_body(body: str, ctx: dict) -> dict:
    m = RULE_RX.match(body)
    if not m:
        raise ParseError(f"unparseable rule: {body[:60]!r}")
    conds = [parse_atom(x, ctx) for x in split_conds(m.group("c"))]
    if sum(1 for a in conds if a["t"] == "cls") > 1:
        raise ParseError("two class conditions")
    unless = parse_atom(m.group("u"), ctx) if m.group("u") else None
    if unless and unless["t"] == "cls" and False:
        raise ParseError("class atom in an unless clause")
    return {"notice": m.group("nt"), "out": m.group("o"), "conds": conds, "unless": unless}


def parse_text_table(lines: list[str], i: int, cs_table: str):
    """Read one card table (aligned / pipe / md / grid) starting at lines[i]; returns (rows, next index)."""
    rows = []
    j = i
    while j < len(lines):
        ln = lines[j]
        if cs_table in ("md", "grid"):
            if not ln.startswith(("|", "+")):
                break
            if ln.startswith("+") or re.fullmatch(r"\|(\s*:?-{3,}:?\s*\|)+", ln):
                j += 1
                continue
            rows.append([c.strip() for c in ln.strip("|").split("|")])
        elif cs_table == "pipe":
            if " | " not in ln:
                break
            rows.append([c.strip() for c in ln.split(" | ")])
        else:  # aligned
            if re.fullmatch(r"=+(\s+=+)*", ln):
                j += 1
                continue
            cells = re.split(r"\s{2,}", ln.strip())
            if len(rows) and len(cells) != len(rows[0]):
                break
            rows.append(cells)
        j += 1
    return rows, j


# ---------------------------------------------------------------- scans (3.1 scope)

def scan_record_text(t: str, markers: set, tag: str | None):
    s = t
    for m in sorted(markers | ({f"({tag})"} if tag else set()), key=len, reverse=True):
        s = s.replace(m, " ")
    hits = scan.banned_hits(s) + scan.completeness_hits(s)
    if hits:
        raise ParseError(f"banned or completeness phrase in record text: {sorted(set(hits))[:3]}")


def scan_rule_text(t: str):
    hits = scan.banned_hits(t)
    if hits:
        raise ParseError(f"banned phrase in card text: {sorted(set(hits))[:3]}")


def scan_question(t: str, allow_quant: bool = False):
    hits = scan.banned_hits(t) + scan.question_hits(t)
    if not allow_quant:
        hits += scan.completeness_hits(t)
    if hits:
        raise ParseError(f"banned phrase in the question: {sorted(set(hits))[:3]}")


# ---------------------------------------------------------------- rules-kind row

def _norm_notice(n: str) -> str:
    return n[0].lower() + n[1:] if n.startswith("The ") else n


def parse_rules_card(lines: list[str], style: dict) -> dict:
    cs = fpool.card_style(style["card_style"])
    ctx = {"attrs": {}, "nouns": set()}
    sw: dict = {}
    rules, excs, ois, notices, subs, defs = {}, [], [], {}, [], []
    table = None
    i = 0
    while i < len(lines):
        ln = lines[i]
        if is_heading(ln):
            i += 1
            continue
        hit = match_switch(ln)
        if hit:
            sw.setdefault(hit[0], []).append(hit[1])
            i += 1
            continue
        m = TLEAD_RX.match(ln)
        if m:
            rows, j = parse_text_table(lines, i + 1, cs["table"])
            if len(rows) < 2:
                raise ParseError("outcome table without rows")
            head = rows[0]
            if head[0].lower() != m.group("A").lower():
                raise ParseError("outcome table row heading name")
            cells = {}
            for r in rows[1:]:
                if len(r) != len(head):
                    raise ParseError("outcome table row length")
                for b, o in zip(head[1:], r[1:]):
                    cells[f"{r[0]}|{b}"] = o
            table = {"rid": "T", "num": int(m.group("n")), "notice": _norm_notice(m.group("nt")),
                     "A": m.group("A"), "B": m.group("B"), "rows": [r[0] for r in rows[1:]],
                     "cols": head[1:], "cells": cells}
            scan_rule_text(ln)
            i = j
            continue
        m = EXC_RX.match(ln)
        if m:
            scan_rule_text(ln)
            body = parse_rule_body(m.group("r"), ctx)
            body["notice"] = _norm_notice(body["notice"])
            excs.append((int(m.group("n")), m.group("ca"), m.group("cb"), body))
            i += 1
            continue
        m = NUM_PREFIX.match(ln)
        if m:
            n = int(next(g for g in m.groups() if g))
            body = ln[m.end():]
            scan_rule_text(body)
            r = parse_rule_body(body, ctx)
            r["notice"] = _norm_notice(r["notice"])
            if n in rules:
                raise ParseError("two rules with one number")
            rules[n] = r
            i += 1
            continue
        m = OI_RX.match(ln)
        if m:
            scan_rule_text(ln)
            ois.append({"out": m.group("o"), "cond": parse_atom(m.group("c"), ctx)})
            i += 1
            continue
        m = NOTICE_RX.match(ln)
        if m and not ln.startswith("Every "):
            scan_rule_text(ln)
            d = parse_date_phrase(m.group("d"))
            if (d["k"] == "exact") == bool(m.group("one")):
                raise ParseError("notice date phrase")
            notices[_norm_notice(m.group("n"))] = {"name": _norm_notice(m.group("n")), "date": d}
            i += 1
            continue
        m = SUB_RX.match(ln)
        if m:
            scan_rule_text(ln)
            subs.append([m.group("b"), m.group("a")])
            i += 1
            continue
        m = re.match(r"^(?P<n>[^:]+): (?P<t>.+)$", ln)
        if m:
            defs.append((m.group("n"), m.group("t")))
            i += 1
            continue
        raise ParseError(f"unrecognised card line: {ln[:70]!r}")
    return {"sw": sw, "rules": rules, "excs": excs, "onlyif": ois, "notices": notices, "subclass": subs,
            "table": table, "defs": defs, "ctx": ctx}


def _one(sw, k):
    v = sw.get(k) or []
    if len(v) > 1:
        raise ParseError(f"switch {k} stated twice")
    return v[0] if v else None


def parse_value_num(v: str, unit: str):
    m = re.fullmatch(r"(\d+) (.+)", v)
    if not m or m.group(2) != unit:
        raise ParseError(f"number value {v[:30]!r}")
    return int(m.group(1))


def parse_row(row: dict, wordings: set) -> dict:
    """Parse a rules-kind F6 row into a name-keyed structure + question + options."""
    style = fpool.style(row["meta"]["format_style"])
    qtype = row["qtype"]
    body, wording, qtext = split_instructions(row["instructions"], style, wordings)
    if qtype == "noul":
        if body.strip():
            raise ParseError("text before the wording on a yes/no row")
        card_text = row.get("card") or ""
        if any(ln.startswith(("- Yes: ", "- No: ")) for ln in card_text.split("\n")):
            raise ParseError("yes/no card line glued to an option")
        optdefs = {}
    else:
        card_text = body
        optdefs = {}
        for ln in (row.get("card") or "").split("\n"):
            if not ln.strip():
                continue
            m = re.fullmatch(r"- (.+?): (.+)", ln)
            if not m or m.group(1) not in row["options"]:
                raise ParseError("choice card field holds a line other than an option definition")
            optdefs[m.group(1)] = m.group(2)
    C = parse_rules_card(card_lines(card_text, style), style)
    sw = C["sw"]
    # ---- world, markers, evidence, D
    world, local = None, None
    if _one(sw, "r1") is not None:
        world = "open"
    if _one(sw, "r2") is not None or _one(sw, "r2_noev") is not None:
        if world:
            raise ParseError("two world rules")
        world = "closed"
    r3 = _one(sw, "r3")
    if r3:
        if world:
            raise ParseError("two world rules")
        world = "local"
    if not world:
        raise ParseError("no world rule (rows 1-3)")
    r18 = _one(sw, "r18")
    if not r18:
        raise ParseError("row 18 missing")
    D = parse_date(r18["D"])
    for k in ("r2", "r2_noev", "r3"):
        g = _one(sw, k)
        if g and parse_date(g["D"]) != D:
            raise ParseError("as-of date differs between sentences")
    r4 = _one(sw, "r4_1") if "r4_1" in sw else _one(sw, "r4_blank")
    marker = r4["m1"] if r4 else None
    markers = {marker} if marker else set()
    if "s5_markers" in sw:
        markers |= set(S5_DIALOGUE)
    if r4 and world != "open" and _one(sw, "r4_1") and r4["clause"] != ", even where this record is complete":
        raise ParseError("row 4 world clause")
    tag = None
    t1, t2 = _one(sw, "r26_not"), _one(sw, "r26_count")
    if t1 is not None:
        tag = {"tag": t1["tag"], "counts": False}
    elif t2 is not None:
        tag = {"tag": t2["tag"][0].lower() + t2["tag"][1:], "counts": True}
    # ---- attributes from rows 20 and 43
    attrs = {}
    for g in sw.get("r20_qdom", []):
        attrs[g["q"]] = {"name": g["q"], "kind": "num", "unit": g["unit"], "lo": int(g["lo"]), "hi": int(g["hi"])}
    for g in sw.get("r43", []):
        vals = re.split(r", or |, | or ", g["vals"])
        attrs[g["attr"]] = {"name": g["attr"], "kind": "cat", "vals": vals}
    rules_by_num = C["rules"]
    for r in list(rules_by_num.values()) + [x[3] for x in C["excs"]] + [{"conds": [o["cond"]]} for o in C["onlyif"]]:
        for at in r["conds"] + ([r["unless"]] if r.get("unless") else []):
            if at["t"] in ("num", "cat") and at["a"] not in attrs:
                raise ParseError(f"attribute without a stated domain: {at['a']}")
    nouns = C["ctx"]["nouns"]
    if len(nouns) > 1:
        raise ParseError("one case noun per card")
    events, classes = {}, {}
    for r in list(rules_by_num.values()) + [x[3] for x in C["excs"]]:
        for at in r["conds"] + ([r["unless"]] if r.get("unless") else []):
            if at["t"] == "ev":
                events[at["e"]] = {"name": at["e"]}
            if at["t"] == "cls":
                classes[at["c"]] = {"name": at["c"]}
    for b, a in C["subclass"]:
        classes.setdefault(b, {"name": b})
        classes.setdefault(a, {"name": a})
    if r3:
        classes.setdefault(r3["thing"], {"name": r3["thing"]})
        local = r3["thing"]
    # ---- rules, exceptions, table
    rules = []
    rid_of = {}
    for n in sorted(rules_by_num):
        r = rules_by_num[n]
        rid_of[n] = f"R{n}"
        rules.append({"rid": f"R{n}", "notice": r["notice"], "conds": r["conds"], "unless": r["unless"],
                      "out": r["out"], "exc": None})
    T = C["table"]
    if T:
        rid_of[T["num"]] = "T"
        for key in T["cells"]:
            pass
        if T["A"] not in attrs or T["B"] not in attrs:
            raise ParseError("outcome table attribute without a domain")
    for i, (n, ca, cb, body) in enumerate(C["excs"]):
        if n not in rid_of:
            raise ParseError("exception names no rule")
        if rid_of[n] == "T":
            if ca is None:
                raise ParseError("exception to a table names no cell")
            tgt = f"T:{ca}|{cb}"
            need = [{"t": "cat", "a": T["A"], "v": ca}, {"t": "cat", "a": T["B"], "v": cb}]
        else:
            tgt = rid_of[n]
            base = rules_by_num[n]
            need = base["conds"]
            if base.get("unless") != body.get("unless"):
                raise ParseError("exception omits the unless clause of its rule")
        for at in need:
            if at not in body["conds"]:
                raise ParseError("exception omits a condition of the rule it names")
        rules.append({"rid": f"X{i + 1}", "notice": body["notice"], "conds": body["conds"],
                      "unless": body["unless"], "out": body["out"], "exc": tgt})
    notices = C["notices"]
    for r in rules + ([{"notice": T["notice"]}] if T else []):
        if r["notice"] not in notices:
            raise ParseError(f"rule under an unstated notice: {r['notice']}")
        for x in notices.values():
            if x["date"].get("d", x["date"].get("b", 0)) > D:
                raise ParseError("notice dated after D")
    r7 = _one(sw, "r7")
    if not r7:
        raise ParseError("row 7 missing on a rule card")
    default = r7["Od"].strip('"')
    for r in rules:
        if r["out"] == default:
            raise ParseError("a rule gives the default outcome")
    if T and default in T["cells"].values():
        raise ParseError("a table cell gives the default outcome")
    # ---- card completeness (section 3)
    def need(key, cond, msg):
        if cond and not sw.get(key):
            raise ParseError(f"card completeness: {msg}")
    allr = rules + ([] if not T else [{"conds": [], "unless": None}])
    ops = {at["op"] for r in rules for at in r["conds"] + ([r["unless"]] if r.get("unless") else [])
           if at["t"] == "num"} | {o["cond"]["op"] for o in C["onlyif"] if o["cond"]["t"] == "num"}
    need("r11", ops & {">=", "<="}, "row 11")
    need("r12", ops & {">", "<"}, "row 12")
    need("r8", any(r.get("unless") for r in rules), "row 8")
    need("r9", bool(C["onlyif"]), "row 9")
    need("r10", bool(rules) or not T or bool(C["onlyif"]), "row 10")      # repair r1 v3c: a table-only policy has no "if" rule
    has_exc = any(r["exc"] for r in rules)
    has_sub = bool(C["subclass"])
    ok24 = {"r24"} | ({"r24_exc"} if not has_sub else set()) | ({"r24_sub"} if not has_exc else set()) | \
        ({"r24_date"} if not has_exc and not has_sub else set())
    if not any(k in sw for k in ok24):
        raise ParseError("card completeness: row 24 (variant)")
    if sum(1 for k in ("r24", "r24_exc", "r24_sub", "r24_date") if k in sw) != 1:
        raise ParseError("two row 24 sentences")
    need("r44", has_exc or has_sub, "row 44")
    need("r45", True, "row 45")
    need("r49", True, "row 49")
    need("r30", True, "row 30")
    need("r32", True, "row 32")
    need("r18_rules", True, "row 18 rules sentence")
    need("r53_short", bool(T), "row 53")
    nonexact = [n for n in notices.values() if n["date"]["k"] != "exact"]
    need("r15_date", any(n["date"]["k"] == "range" for n in nonexact), "row 15")
    need("r17", any(n["date"]["k"] == "month" for n in nonexact), "row 17")
    return {"style": style, "qtype": qtype, "wording": wording, "question": qtext, "card": C, "sw": sw,
            "world": world, "local": local, "D": D, "marker": marker, "ev_tag": tag, "attrs": attrs,
            "events": events, "classes": classes, "rules": rules, "table": T, "onlyif": C["onlyif"],
            "notices": notices, "subclass": C["subclass"], "default": default, "optdefs": optdefs,
            "markers": markers,
            "noun": next(iter(nouns)) if nouns else None}


# ---------------------------------------------------------------- record facts, question and options (rules kind)

CLAIM_RX = re.compile(r'^the outcome for (?P<c>' + ID_RX + r'|.+?) is (?P<neg>not )?"(?P<o>[^"]+)"$')


def _class_for_heading(key: str, classes: dict):
    kw = key.lower().split()
    for c in classes:
        cw = c.lower().split()
        if len(cw) == len(kw) and cw[0] == kw[0] and kw[-1].startswith(cw[-1][:max(3, len(cw[-1]) - 2)]):
            return c
    return None


def parse_facts(S: dict, row: dict, cases: list) -> dict:
    style = S["style"]
    if len(cases) > 1:
        per, top = state_sections(row["state"], style, cases)
        pairs = [(k, v, None) for k, v in top] + [(k, v, lab) for lab in cases for k, v in per[lab]]
        other = []
    elif style["container"] == "chat_log" or (style["container"] == "email_thread" and
                                              fpool.skin(style["skin"])["params"].get("order") != "single"):
        pp, other = transcript_pairs(row["state"], style, cases[0]), []
        pairs = [(k, v, cases[0]) for k, v in pp]
    else:
        pp, other = state_pairs(row["state"], style)
        pairs = [(k, v, cases[0]) for k, v in pp]
    lab_rx = "(" + "|".join(re.escape(c) for c in cases) + ")"
    markers = set(S.get("markers") or ({S["marker"]} if S["marker"] else set()))
    tag = (S["ev_tag"] or {}).get("tag")
    facts = {c: {"num": {}, "cat": {}, "ev": {}, "cls": {}, "inert": []} for c in cases}
    lists = {}
    D_state = None
    seen_keys = set()
    for k, v, sec in pairs:
        if (k, sec) in seen_keys:
            raise ParseError(f"key stated twice: {k[:40]}")
        seen_keys.add((k, sec))
        scan_record_text(k, markers, tag)
        scan_record_text(v, markers, tag)
        if k == "As-of date":
            D_state = parse_date(v)
            continue
        tagged = bool(tag) and v.endswith(f" ({tag})")
        core = v[: -len(f" ({tag})")] if tagged else v
        is_m = core in markers and not tagged
        m = re.fullmatch(r"(.+) for " + lab_rx, k)
        evname = None
        if m:
            evname = next((e for e in S["events"] if e.lower() == m.group(1).lower()), None)
        if evname and m.group(2) in facts:
            who = m.group(2)
            if is_m:
                facts[who]["ev"][evname] = {"m": True}
            elif re.fullmatch(r"(scheduled|planned|expected|requested) for .+", core):
                if tagged:
                    raise ParseError("a tagged plan")
                facts[who]["ev"][evname] = {"plan": parse_date(core.split(" for ", 1)[1])}
            else:
                d = parse_date_phrase(core)
                if d["k"] != "exact":
                    raise ParseError("ranged event date on a rules card")
                if d["d"] > S["D"]:
                    raise ParseError("event dated after D")
                facts[who]["ev"][evname] = {"v": True, "date": d["d"], **({"tag": True} if tagged else {})}
            continue
        cl = _class_for_heading(k, S["classes"])
        if cl:
            ents = []
            for e in v.split(", "):
                mm = re.fullmatch(r"(" + ID_RX + r"|.+?)(?: \((?P<x>.+)\))?", e)
                who, x = mm.group(1), mm.group("x")
                if x is None:
                    st = "v"
                elif x.startswith("membership ") and x[len("membership "):] in markers:
                    st = "m"
                elif tag and x == tag:
                    st = "tag"
                else:
                    raise ParseError("list entry form")
                ents.append((who, st))
                if who in facts:
                    if st == "m":
                        facts[who]["cls"][cl] = {"m": True}
                    elif st == "tag":
                        facts[who]["cls"][cl] = {"v": True, "tag": True}
                    else:
                        facts[who]["cls"][cl] = {"v": True}
            if not ents:
                raise ParseError("empty named list")
            lists[cl] = ents
            continue
        an = next((a for a in S["attrs"] if a.lower() == k.lower()), None)
        if an and sec is not None:
            a = S["attrs"][an]
            slot = facts[sec]["num" if a["kind"] == "num" else "cat"]
            if is_m:
                slot[an] = {"m": True}
            elif a["kind"] == "num":
                slot[an] = {"v": parse_value_num(core, a["unit"]), **({"tag": True} if tagged else {})}
            else:
                if core not in a["vals"]:
                    raise ParseError("category value outside its list")
                slot[an] = {"v": core, **({"tag": True} if tagged else {})}
            continue
        facts[sec if sec is not None else cases[0]]["inert"].append([k, v])
    if D_state is not None and D_state != S["D"]:
        raise ParseError("record as-of date differs from the card")
    others = []
    for o in other:
        if isinstance(o, tuple):
            continue
        scan_record_text(o, markers, tag)
        others.append(o)
    for c in S["classes"]:
        if c not in lists:
            raise ParseError(f"a named list is not shown: {c}")
    # closed-card structural checks (rows 2, 44)
    for b, a in S["subclass"]:
        for who in cases:
            fb, fa = facts[who]["cls"].get(b), facts[who]["cls"].get(a)
            closes_a = S["world"] == "closed" or (S["world"] == "local" and S["local"] == a)
            if fb and "v" in fb and not fb.get("tag") and fa is None and closes_a:
                raise ParseError("a listed <class B> case not listed as <class A> where A closes")
            b_known = fb is not None and "v" in fb and (not fb.get("tag") or (S["ev_tag"] or {}).get("counts"))
            if b_known and (fa is not None and (fa.get("m") or fa.get("tag"))):
                raise ParseError("a class fact fixed by a relation is marked or tagged")
    S["facts"] = facts
    S["lists"] = lists
    S["other_text"] = others
    return S


def parse_question(S: dict, row: dict) -> dict:
    q = S["question"]
    reg = fpool.register(S["style"]["register"])
    scan_question(q)
    out = {"text": q}
    m = re.fullmatch(r"Which outcome applies to (" + ID_RX + r")\?", q)
    if m:
        out.update(form="c_out", case=m.group(1))
        return out
    m = re.fullmatch(r"Which one additional fact would settle which outcome applies to (" + ID_RX + r")\?", q)
    if m:
        out.update(form="c_gap", case=m.group(1))
        return out
    m = re.fullmatch(r"Which of these cases (can|cannot) be decided from its record\?", q)
    if m:
        if "r52" not in S["sw"]:
            raise ParseError("card completeness: row 52")
        out.update(form="c_case", frame="c_case_" + m.group(1), cases=list(row["options"]))
        return out
    m = re.fullmatch(r'Is the outcome for (' + ID_RX + r') "([^"]+)"\?', q)
    if m:
        out.update(form="qplain", frame="qplain_inv", case=m.group(1),
                   claim={"t": "out_is", "o": m.group(2), "neg": False})
        return out
    for k in ("qdet_dneg", "qdet_leave", "qdet_imp", "qdet", "qest_est", "qest_show", "qest_det", "qplain_true"):
        rx = _tpl_rx(FRAMES[k])
        mm = rx.match(q)
        if mm:
            cm = CLAIM_RX.match(mm.group("S"))
            if not cm:
                raise ParseError("claim S not parseable")
            if k == "qplain_true" and False:
                pass
            form = "qdet" if k.startswith("qdet") else "qest" if k.startswith("qest") else "qplain"
            out.update(form=form, frame=k, case=cm.group("c"),
                       claim={"t": "out_is", "o": cm.group("o"), "neg": bool(cm.group("neg"))})
            from .lex import FRAME_SWITCH
            if not S["sw"].get(FRAME_SWITCH[k]):
                raise ParseError(f"card completeness: the frame's sentence ({FRAME_SWITCH[k]})")
            if k == "qdet_dneg" and not out["claim"]["neg"] and False:
                pass
            return out
    raise ParseError("question frame outside 3.1")


def parse_options(S: dict, row: dict, Q: dict) -> dict:
    if row["qtype"] == "noul":
        return {"kind": "yn"}
    opts = row["options"]
    if Q["form"] == "c_out":
        nei = next((g["NEI"] for g in S["sw"].get("r33", [])), None)
        none = next((g["NONE"] for g in S["sw"].get("r34", [])), None)
        conc, ab = [], {}
        for o in opts:
            if o == nei and o in OPTION_TEXT["nei"]:
                ab["nei"] = o
            elif o == none and o in OPTION_TEXT["none"]:
                ab["none"] = o
            elif o in OPTION_TEXT["nei"] + OPTION_TEXT["none"]:
                raise ParseError("abstain option without its card sentence (rows 33-34)")
            else:
                scan_record_text(o, set(), None)
                conc.append(o)
        if ab and not S["sw"].get("r50"):
            raise ParseError("card completeness: row 50")
        if "nei" in ab and "none" in ab and not S["sw"].get("r35"):
            raise ParseError("card completeness: row 35")
        return {"kind": "c_out", "concrete": conc, "abstain": ab}
    if Q["form"] == "c_gap":
        nothing = next((g["NOTHING"] for g in S["sw"].get("r51", [])), None)
        gaps = []
        for o in opts:
            if o == nothing and o in OPTION_TEXT["nothing"]:
                continue
            gaps.append(parse_gap_text(o, S))
        if nothing not in opts:
            raise ParseError("C-GAP row without the nothing-needed option")
        return {"kind": "c_gap", "gaps": gaps, "nothing": nothing, "texts": opts}
    raise ParseError("options for an unknown form")


def parse_gap_text(t: str, S: dict):
    m = re.fullmatch(r"the value of the (.+) of (" + ID_RX + r")", t)
    if m and m.group(1) in S["attrs"]:
        a = S["attrs"][m.group(1)]
        return [a["kind"], m.group(1)]
    m = re.fullmatch(r"the (.+) of (" + ID_RX + r")", t)
    if m and m.group(1) in S["attrs"]:
        a = S["attrs"][m.group(1)]
        return [a["kind"], m.group(1)]
    m = re.fullmatch(r'whether (' + ID_RX + r') had an? "([^"]+)" event', t)
    if m:
        return ["ev", m.group(2)]
    m = re.fullmatch(r'whether an? "([^"]+)" event happened for (' + ID_RX + r')', t)
    if m:
        return ["ev", m.group(1)]
    m = re.fullmatch(r"whether (" + ID_RX + r") (?:is|counts as) an? (.+)", t)
    if m:
        return ["cls", m.group(2)]
    m = re.fullmatch(r"the effective date of (.+)", t)
    if m:
        return ["nd", m.group(1)]
    raise ParseError(f"gap option text: {t[:50]!r}")


# ================================================================ S3 tables

S3_CMP = {"at least": ">=", "no fewer than": ">=", "no less than": ">=", "at most": "<=", "no more than": "<=",
          "more than": ">", "fewer than": "<", "less than": "<"}
_S3C = "|".join(sorted(map(re.escape, S3_CMP), key=len, reverse=True))


def _norm_key(s: str) -> str:
    return "_".join(re.findall(r"[a-z0-9]+", s.lower()))


def read_tables(state: str, style: dict) -> list:
    """Every table in the record as [header, rows...] (cells as strings; None for JSON null)."""
    cont = style["container"]
    sk = fpool.skin(style["skin"])
    p = sk.get("params", {})
    text = re.sub(r"^\s*```\w*\s*$", "", state, flags=re.M)
    if cont == "json":
        data = json.loads(text)
        if not isinstance(data, list) or not data:
            raise ParseError("JSON array expected")
        keys = list(data[0].keys())
        for d in data:
            if list(d.keys()) != keys:
                raise ParseError("a JSON entry without every key (row 42)")
        return [[keys] + [[d[k] for k in keys] for d in data]]
    if cont == "csv":
        if p.get("fixed"):
            lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
            rows = [re.split(r"\s{2,}", ln) for ln in lines]
        else:
            import csv as _csv
            lines = [ln.lstrip(" ").rstrip("\r") for ln in text.split("\n") if ln.strip(" \r")]
            rows = list(_csv.reader(lines, delimiter=p["delim"]))
        return [rows]
    if cont == "markdown_table":
        out, cur = [], None
        for ln in text.split("\n"):
            s = ln.strip()
            if s.startswith("|") and s.endswith("|"):
                cells = [c.strip() for c in s.strip("|").split("|")]
                if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    continue
                if cur is None:
                    cur = []
                    out.append(cur)
                cur.append(cells)
            else:
                cur = None
        return out
    if cont == "html_snippet":
        out = []
        for tb in re.findall(r"<table>(.*?)</table>", text, flags=re.S):
            rows = []
            for tr in re.findall(r"<tr>(.*?)</tr>", tb, flags=re.S):
                cells = [_html.unescape(c).strip() for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, flags=re.S)]
                rows.append(cells)
            out.append(rows)
        return out
    raise ParseError(f"no table reader for {cont}")


def parse_table_row(row: dict, wordings: set) -> dict:
    style = fpool.style(row["meta"]["format_style"])
    qtype = row["qtype"]
    body, wording, qtext = split_instructions(row["instructions"], style, wordings)
    card_text = row.get("card") if qtype == "noul" else body
    if qtype == "noul" and body.strip():
        raise ParseError("text before the wording on a yes/no row")
    if qtype == "choice" and (row.get("card") or "").strip():
        raise ParseError("a C-REC card field holds a line")
    sw = {}
    for ln in card_lines(card_text or "", style):
        if is_heading(ln):
            continue
        hit = match_switch(ln)
        if not hit:
            if ln.startswith(("Example: ", "Worked example: ")):      # repair r1: card examples, scanned
                if scan.banned_hits(ln) or scan.completeness_hits(ln):
                    raise ParseError("banned phrase in a card example")
                continue
            raise ParseError(f"unrecognised card line: {ln[:70]!r}")
        sw.setdefault(hit[0], []).append(hit[1])
    world = "open" if "r1" in sw else "closed" if ("r2" in sw or "r2_noev" in sw) else "local" if "r3" in sw \
        else None
    if world is None:
        raise ParseError("no world rule")
    D = parse_date(sw["r18"][0]["D"]) if "r18" in sw else None
    if D is None:
        raise ParseError("row 18 missing")
    cols = []
    for g in sw.get("r20_qdom", []):
        cols.append({"name": g["q"], "kind": "num", "unit": g["unit"], "lo": int(g["lo"]), "hi": int(g["hi"])})
    for g in sw.get("r43", []):
        cols.append({"name": g["attr"], "kind": "cat", "vals": re.split(r", or |, | or ", g["vals"])})
    json_card = "r42_json" in sw
    marker = (sw.get("r4_1") or sw.get("r4_blank") or [{}])[0].get("m1")
    blank = "r4_blank" in sw
    if not json_card and "r42" not in sw:
        raise ParseError("row 42 missing on a table card")
    if not json_card and blank != (sw["r42"][0]["blank"] == " or left blank"):
        raise ParseError("rows 4 and 42 disagree on blanks")
    # ---- the table
    tables = read_tables(row["state"], style)
    if not tables:
        raise ParseError("no table")
    head, *rows_ = tables[0]
    byname = {}
    for c in cols:
        hdr = f"{c['name']} ({c['unit']})" if c["kind"] == "num" else c["name"]
        byname[_norm_key(hdr)] = c
    idx = []
    for h in head[1:]:
        c = byname.get(_norm_key(h))
        if not c:
            raise ParseError(f"table column without a stated domain: {h}")
        idx.append(c)
    if len({c["name"] for c in idx}) != len(cols):
        raise ParseError("a stated column is not in the table")
    recs = []
    for r in rows_:
        if len(r) != len(head):
            raise ParseError("a record without every column (row 42)")
        rid = r[0]
        if not re.fullmatch(ID_RX, rid or ""):
            raise ParseError("record ID form")
        cells = {}
        for c, v in zip(idx, r[1:]):
            if v is None:
                if not json_card:
                    raise ParseError("null outside JSON")
                cells[c["name"]] = None
            elif v == "":
                if not blank:
                    raise ParseError("blank cell on a card whose rows 4 / 42 do not name blanks")
                cells[c["name"]] = None
            elif v == marker:
                cells[c["name"]] = None
            elif c["kind"] == "num":
                if not re.fullmatch(r"\d+", str(v)):
                    raise ParseError("table number form (row 42: exact values only)")
                x = int(v)
                if not c["lo"] <= x <= c["hi"]:
                    raise ParseError("a figure outside its stated domain")
                cells[c["name"]] = x
            else:
                if v not in c["vals"]:
                    raise ParseError("category value outside its list")
                cells[c["name"]] = v
        recs.append({"id": rid, "cells": cells})
    if len({r["id"] for r in recs}) != len(recs):
        raise ParseError("one ID twice")
    lst = None
    for t in tables[1:]:
        for r in t:
            if len(r) == 2 and r[0].lower() not in ("field", "attribute", "key", "name"):
                members = r[1].split(", ")
                lst = {"name": r[0][0].lower() + r[0][1:], "members": members}
    pairs, other = ([], [])
    if style["container"] in ("markdown_table", "html_snippet"):
        for o in other:
            pass
    T = {"kind": "table", "D": D, "world": world, "cols": [{**c, "id": c["name"]} for c in cols],
         "records": [{"id": r["id"], "cells": r["cells"]} for r in recs], "list": None, "marker": marker}
    if lst:
        closed = world == "closed" or (world == "local" and sw["r3"][0]["section"].lower() == lst["name"].lower())
        T["list"] = {"name": lst["name"], "members": lst["members"], "closed": closed}
    # ---- question
    scan_question(qtext, allow_quant=True)
    out = {"T": T, "style": style, "sw": sw}
    m = re.fullmatch(r"Which record(?: whose (?P<fc>.+?) is (?P<fv>.+?))? has the (?P<hl>highest|lowest) "
                     r"(?P<k>.+)\?", qtext)
    if m:
        if "r23" not in sw:
            raise ParseError("card completeness: row 23")
        key = next((c for c in cols if c["name"] == m.group("k")), None)
        if not key:
            raise ParseError("argmax key")
        Q = {"t": "argmax" if m.group("hl") == "highest" else "argmin", "key": key["name"]}
        if m.group("fc"):
            if "r42_filter" not in sw:
                raise ParseError("card completeness: filtered argmax sentence")
            Q["filter"] = {"col": m.group("fc"), "v": m.group("fv")}
        out.update(form="c_rec", Q=Q, frame="c_rec")
        nei = next((g["NEI"] for g in sw.get("r33", [])), None)
        none = next((g["NONE"] for g in sw.get("r34", [])), None)
        conc, ab = [], {}
        for o in row["options"]:
            if o == nei:
                ab["nei"] = o
            elif o == none:
                ab["none"] = o
            elif re.fullmatch(ID_RX, o) and o in [r["id"] for r in recs]:
                conc.append(o)
            else:
                raise ParseError("C-REC option is not a record ID or a fixed wording")
        out.update(concrete=conc, abstain=ab)
        return out
    frame, S = None, None
    for k in ("qdet_dneg", "qdet_leave", "qdet_imp", "qdet", "qest_est", "qest_show", "qest_det", "qplain_true"):
        mm = _tpl_rx(FRAMES[k]).match(qtext)
        if mm:
            frame, S = k, mm.group("S")
            break
    if frame is None:
        inv = _s3_inversion(qtext)
        if inv is None:
            raise ParseError("question frame outside 3.1")
        frame, S = "qplain_inv", inv
    else:
        from .lex import FRAME_SWITCH
        if FRAME_SWITCH[frame] not in sw:
            raise ParseError(f"card completeness: frame sentence {FRAME_SWITCH[frame]}")
    Q = _s3_claim(S, cols)
    if Q["t"] in ("forall", "exists", "none") or Q.get("filter"):
        need = {"forall": "r28_every", "exists": "r28_one", "none": "r28_no"}.get(Q["t"])
        if need and need not in sw:
            raise ParseError(f"card completeness: {need}")
        if Q.get("filter") and "r28_filter" not in sw:
            raise ParseError("card completeness: r28_filter")
    form = "qdet" if frame.startswith("qdet") else "qest" if frame.startswith("qest") else "qplain"
    out.update(form=form, frame=frame, Q=Q)
    return out


def _s3_cond(t: str, cols: list) -> dict:
    m = re.fullmatch(r"an? (?P<c>.+?) of (?P<w>" + _S3C + r") (?P<n>\d+) (?P<u>.+)", t)
    if m:
        c = next((x for x in cols if x["name"] == m.group("c") and x["kind"] == "num"), None)
        if c and c["unit"] == m.group("u"):
            return {"col": c["name"], "op": S3_CMP[m.group("w")], "n": int(m.group("n"))}
    m = re.fullmatch(r"an? (?P<c>.+?) of (?P<v>.+)", t)
    if m:
        c = next((x for x in cols if x["name"] == m.group("c") and x["kind"] == "cat"), None)
        if c and m.group("v") in c["vals"]:
            return {"col": c["name"], "v": m.group("v")}
    raise ParseError(f"condition: {t[:50]!r}")


def _s3_claim(S: str, cols: list) -> dict:
    m = re.fullmatch(r"(?P<who>" + ID_RX + r") is (?P<neg>not )?on the (?P<l>.+)", S)
    if m:
        return {"t": "member", "who": m.group("who"), "neg": bool(m.group("neg"))}
    whose = r"(?: whose (?P<fc>.+?) is (?P<fv>.+?))?"
    pats = [("exists", r"at least one (?P<n>.+?) in the register" + whose + r" has (?P<c>an? .+)"),
            ("forall", r"every (?P<n>.+?) in the register" + whose + r" has (?P<c>an? .+)"),
            ("none", r"no (?P<n>.+?) in the register" + whose + r" has (?P<c>an? .+)"),
            ("count", r"(?P<w>" + _S3C + r") (?P<N>\d+) (?P<n>.+?) in the register" + whose + r" have (?P<c>an? .+)")]
    for t, p in pats:
        m = re.fullmatch(p, S)
        if m:
            Q = {"t": t, "cond": _s3_cond(m.group("c"), cols)}
            if m.group("fc"):
                fc = next((x for x in cols if x["name"] == m.group("fc") and x["kind"] == "cat"), None)
                if not fc or m.group("fv") not in fc["vals"]:
                    raise ParseError("filter")
                Q["filter"] = {"col": fc["name"], "v": m.group("fv")}
            if t == "count":
                Q["cmp"] = S3_CMP[m.group("w")]
                Q["N"] = int(m.group("N"))
            return Q
    raise ParseError(f"claim: {S[:60]!r}")


def _s3_inversion(q: str):
    m = re.fullmatch(r"Is (" + ID_RX + r") on the (.+)\?", q)
    if m:
        return f"{m.group(1)} is on the {m.group(2)}"
    m = re.fullmatch(r"Does (at least one|every) (.+?) have (an? .+)\?", q)
    if m:
        return f"{m.group(1)} {m.group(2)} has {m.group(3)}"
    m = re.fullmatch(r"Do (.+?) have (an? .+)\?", q)
    if m:
        return f"{m.group(1)} have {m.group(2)}"
    return None


# ================================================================ S4 timelines

def _quoted_list(s: str) -> list:
    return re.findall(r'"([^"]+)"', s)


def parse_timeline_row(row: dict, wordings: set) -> dict:
    style = fpool.style(row["meta"]["format_style"])
    body, wording, qtext = split_instructions(row["instructions"], style, wordings)
    if body.strip():
        raise ParseError("text before the wording on a yes/no row")
    sw = {}
    for ln in card_lines(row.get("card") or "", style):
        if is_heading(ln):
            continue
        hit = match_switch(ln)
        if not hit:
            if ln.startswith(("Example: ", "Worked example: ")):      # repair r1: card examples, scanned
                if scan.banned_hits(ln) or scan.completeness_hits(ln):
                    raise ParseError("banned phrase in a card example")
                continue
            raise ParseError(f"unrecognised card line: {ln[:70]!r}")
        sw.setdefault(hit[0], []).append(hit[1])
    if "r18" not in sw:
        raise ParseError("row 18 missing")
    D = parse_date(sw["r18"][0]["D"])
    world, local = None, None
    if "r1" in sw:
        world = "open"
    if "r2" in sw:
        world = "closed"
        if parse_date(sw["r2"][0]["D"]) != D:
            raise ParseError("closure date")
    if "r3_ev" in sw:
        world, local = "local", sw["r3_ev"][0]["event"]
    if world is None:
        raise ParseError("no world rule")
    types = _quoted_list(sw["r54"][0]["events"]) if "r54" in sw else []
    marker = (sw.get("r4_1") or [{}])[0].get("m1")
    day_dom = {}
    for g in sw.get("r20_day", []):
        day_dom[f"{g['event']}|{g['ent']}"] = (parse_date(g["lo"]), parse_date(g["hi"]))
    quants = {}
    for g in sw.get("r20_qdom", []):
        quants[g["q"]] = {"name": g["q"], "unit": g["unit"], "lo": int(g["lo"]), "hi": int(g["hi"])}
    for g in sw.get("r19", []):
        q = quants.get(g["q"])
        if not q:
            raise ParseError("rounding sentence for an unknown quantity")
        q["R"], q["mark"] = int(g["R"]), g["mark"]
        if int(g["h"]) * 2 != q["R"]:
            raise ParseError("rounding half")
    amb = False
    for g in sw.get("r21", []) + sw.get("r22", []):
        q = quants.get(g["q"])
        if not q:
            raise ParseError("unit sentence for an unknown quantity")
        if "V" in g:
            q["V"] = g["V"]
            amb = True
    for g in sw.get("r21_conv", []):
        for q in quants.values():
            if q["unit"] == g["U"]:
                q["V"], q["conv"] = g["V"], int(g["c"])
    noshare = _quoted_list(sw["r46_noshare"][0]["events"]) if "r46_noshare" in sw else []
    pairs, other = state_pairs(row["state"], style)
    events, figures = {}, {}
    D2 = None
    for k, v in pairs:
        scan_record_text(k, {marker} if marker else set(), None)
        if k == "As-of date":
            D2 = parse_date(v)
            continue
        m = re.fullmatch(r"(.+) for (" + ID_RX + r")", k)
        if not m:
            raise ParseError(f"record key: {k[:40]!r}")
        name, who = m.group(1)[0].lower() + m.group(1)[1:], m.group(2)
        if name in types:
            key = f"{name}|{who}"
            if v == marker:
                events[key] = {"k": "marker"}
                continue
            mm = re.fullmatch(r"(scheduled|planned|expected|requested) for (.+)", v)
            if mm:
                events[key] = {"k": "plan", "d": parse_date(mm.group(2))}
                continue
            d = parse_date_phrase(v)
            if d.get("b", d.get("d")) > D:
                raise ParseError("event date after D")
            events[key] = d
            continue
        q = quants.get(name)
        if not q:
            raise ParseError(f"record key names no event type or quantity: {name[:30]!r}")
        key = f"{name}|{who}"
        if v == marker:
            figures[key] = {"q": name, "k": "marker"}
            continue
        u = None
        mm = re.fullmatch(r"from (\d+) to (\d+) (.+)", v)
        if mm:
            u = "V" if mm.group(3) == q.get("V") else ("U" if mm.group(3) == q["unit"] else None)
            if u is None:
                raise ParseError("figure unit")
            figures[key] = {"q": name, "k": "range", "a": int(mm.group(1)), "b": int(mm.group(2)), "unit": u}
            continue
        mm = re.fullmatch(r"(\d+)(" + re.escape(q.get("mark", "\x00")) + r")? (.+)", v)
        if mm:
            u = "V" if mm.group(3) == q.get("V") else ("U" if mm.group(3) == q["unit"] else None)
            if u is None:
                raise ParseError("figure unit")
            if mm.group(2):
                figures[key] = {"q": name, "k": "round", "x": int(mm.group(1)), "unit": u}
            else:
                figures[key] = {"q": name, "k": "exact", "x": int(mm.group(1)), "unit": u}
            continue
        mm = re.fullmatch(r"(\d+)", v)
        if mm:
            if not amb:
                raise ParseError("a unitless figure on a default-unit card")
            figures[key] = {"q": name, "k": "unitless", "x": int(mm.group(1))}
            continue
        raise ParseError(f"figure value {v[:30]!r}")
    for o in other:
        if not isinstance(o, tuple):
            scan_record_text(o, {marker} if marker else set(), None)
    if D2 is not None and D2 != D:
        raise ParseError("record as-of date differs from the card")
    if sum(1 for f in figures.values() if f["k"] == "unitless") > 1:
        raise ParseError("two unitless figures (row 22)")
    qid = {name: name for name in quants}
    S = {"kind": "timeline", "D": D, "world": world, "local": local, "marker": marker, "events": events,
         "day_dom": day_dom, "figures": figures, "quantities": {n: {**q, "R": q.get("R", 0)} for n, q in quants.items()},
         "noshare_types": noshare}
    # ---- question
    scan_question(qtext)
    frame, Sx = None, None
    for k in ("qdet_dneg", "qdet_leave", "qdet_imp", "qdet", "qest_est", "qest_show", "qest_det", "qplain_true"):
        mm = _tpl_rx(FRAMES[k]).match(qtext)
        if mm:
            frame, Sx = k, mm.group("S")
            break
    if frame is None:
        frame, Sx = "qplain_inv", _s4_inversion(qtext)
        if Sx is None:
            raise ParseError("question frame outside 3.1")
    else:
        from .lex import FRAME_SWITCH
        if FRAME_SWITCH[frame] not in sw:
            raise ParseError(f"card completeness: {FRAME_SWITCH[frame]}")
    Q = _s4_claim(Sx, S, sw)
    form = "qdet" if frame.startswith("qdet") else "qest" if frame.startswith("qest") else "qplain"
    return {"S": S, "Q": Q, "form": form, "frame": frame}


def _s4_claim(Sx: str, S: dict, sw: dict) -> dict:
    m = re.fullmatch(r"the (?P<e>.+?) for (?P<w>" + ID_RX + r") (?P<v>happened|did not happen) "
                     r"(?P<b>by|on or before|no later than) (?P<d>.+)", Sx)
    if m:
        if "r16_dl" not in sw:
            raise ParseError("card completeness: deadline sentence")
        return {"t": "deadline", "ev": f"{m.group('e')}|{m.group('w')}", "by": parse_date(m.group("d")),
                "neg": m.group("v") == "did not happen"}
    m = re.fullmatch(r"the (?P<e1>.+?) for (?P<w1>" + ID_RX + r") (?P<v>happened|did not happen) before the "
                     r"(?P<e2>.+?) for (?P<w2>" + ID_RX + r")", Sx)
    if m:
        if "r46_noshare" not in sw or "r46_byday" not in sw:
            raise ParseError("card completeness: row 46")
        return {"t": "before", "e1": f"{m.group('e1')}|{m.group('w1')}", "e2": f"{m.group('e2')}|{m.group('w2')}",
                "neg": m.group("v") == "did not happen"}
    m = re.fullmatch(r"the (?P<e2>.+?) for (?P<w2>" + ID_RX + r") happened at least (?P<n>\d+) days after the "
                     r"(?P<e1>.+?) for (?P<w1>" + ID_RX + r")", Sx)
    if m:
        if "r47" not in sw:
            raise ParseError("card completeness: row 47")
        return {"t": "daycount", "e1": f"{m.group('e1')}|{m.group('w1')}", "e2": f"{m.group('e2')}|{m.group('w2')}",
                "N": int(m.group("n"))}
    m = re.fullmatch(r"the total of (?P<l>.+) is (?P<c>at least|no less than|at most|no more than|more than|less than) "
                     r"(?P<t>\d+) (?P<u>.+)", Sx)
    if m:
        parts = re.split(r", | and ", m.group("l"))
        figs, qn = [], None
        for p in parts:
            mm = re.fullmatch(r"the (.+) for (" + ID_RX + r")", p)
            if not mm:
                raise ParseError("total names a figure that is not 'the <quantity> for <ID>'")
            qn = mm.group(1)
            figs.append(f"{qn}|{mm.group(2)}")
        q = S["quantities"].get(qn)
        if not q or q["unit"] != m.group("u"):
            raise ParseError("total unit")
        op = {"at least": ">=", "no less than": ">=", "at most": "<=", "no more than": "<=", "more than": ">",
              "less than": "<"}[m.group("c")]
        need = "r11" if op in (">=", "<=") else "r12"
        if need not in sw:
            raise ParseError(f"card completeness: {need}")
        return {"t": "total", "figs": figs, "op": op, "T": int(m.group("t")), "q": qn}
    raise ParseError(f"claim: {Sx[:60]!r}")


def _s4_inversion(q: str):
    m = re.fullmatch(r"Did the (.+?) for (" + ID_RX + r") happen (.+)\?", q)
    if m:
        rest = m.group(3)
        mm = re.fullmatch(r"at least (\d+) days after (.+)", rest)
        if mm:
            return f"the {m.group(1)} for {m.group(2)} happened at least {mm.group(1)} days after {mm.group(2)}"
        return f"the {m.group(1)} for {m.group(2)} happened {rest}"
    m = re.fullmatch(r"Is the total of (.+?) (at least|no less than|at most|no more than|more than|less than) (\d+) (.+)\?",
                     q)
    if m:
        return f"the total of {m.group(1)} is {m.group(2)} {m.group(3)} {m.group(4)}"
    return None


# ================================================================ C-CASE (several case records under their labels)

def _label_of(line: str, labels: list):
    s = line.strip()
    s = re.sub(r"^```\w*$", "", s)
    s = BULLET_RX.sub("", s)
    s = re.sub(r"^#+\s*", "", s)
    s = re.sub(r"^\*\*(.*)\*\*$", r"\1", s)
    s = re.sub(r"^\[(.*)\]$", r"\1", s)
    s = re.sub(r"^==\s*(.*?)\s*==$", r"\1", s)
    s = re.sub(r"^\d+\.\s+", "", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = s.rstrip(":").strip()
    for lab in labels:
        if s.lower() == lab.lower():
            return lab
    return None


def state_sections(state: str, style: dict, labels: list) -> tuple[dict, list]:
    """{label: [(key, value)]} and the top-level pairs (as-of date, lists) of a multi-case record."""
    cont = style["container"]
    per = {lab: [] for lab in labels}
    top = []
    if cont == "html_snippet":
        t = re.sub(r"```\w*", "", state)
        rest = t
        for sec in re.findall(r"<section>(.*?)</section>", t, flags=re.S):
            h = re.search(r"<h\d>(.*?)</h\d>", sec, flags=re.S)
            lab = _label_of(_html.unescape(h.group(1)), labels) if h else None
            if lab is None:
                raise ParseError("section without a case label")
            for k, v in re.findall(r"<th[^>]*>(.*?)</th>\s*<td>(.*?)</td>", sec, flags=re.S):
                per[lab].append((_html.unescape(k).strip(), _html.unescape(v).strip()))
            for k, v in re.findall(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", sec, flags=re.S):
                per[lab].append((_html.unescape(k).strip(), _html.unescape(v).strip()))
            rest = rest.replace(sec, "")
        top_pairs, _ = state_pairs(rest, style)
        return per, top_pairs
    cur = None
    chunks = {None: []}
    for ln in state.split("\n"):
        lab = _label_of(ln, labels)
        if lab:
            cur = lab
            chunks.setdefault(cur, [])
            continue
        if re.fullmatch(r"\s*[=\-]{3,}\s*", ln) and cur is not None and not chunks[cur]:
            continue
        chunks.setdefault(cur, []).append(ln)
    for lab, lines in chunks.items():
        pairs, _ = state_pairs("\n".join(lines), style)
        if lab is None:
            top = pairs
        else:
            per[lab] = pairs
    # a top-level fields block after the last section lands in that section: move list / as-of pairs back
    return per, top


# ================================================================ S5 interview transcripts

def _messages(state: str, style: dict) -> list[str]:
    sk = fpool.skin(style["skin"])
    p = sk.get("params", {})
    reg = fpool.register(style["register"])
    if style["container"] == "chat_log":
        if not p.get("block"):
            return [ln.split(" | ", 2)[2] for ln in state.split("\n") if ln.strip()]
        out = []
        for blk in re.split(r"\n\s*\n", state.strip()):
            lines = blk.split("\n")
            out.append("\n".join(lines[1:]).strip())
        return out
    sep = p.get("separator")
    if p.get("counter"):
        blocks = re.split(r"(?m)^Message \d+ of \d+$", state)[1:]
    elif sep:
        blocks = state.split(sep)
    else:
        blocks = [state]
    greet = {g for g in (reg.get("email_greeting_generic"),) if g}
    close = reg.get("email_closing") or None
    out = []
    for b in blocks:
        body = []
        for ln in b.strip().split("\n"):
            s = ln.strip()
            if not s or re.match(r"^(From|To|Sent|Subject|Sender|Posted): ", s) or s in greet:
                continue
            if re.fullmatch(r"(Dear|Hi|Good morning) .+,", s):
                continue
            body.append(s)
        if close and close in body:
            body = body[: body.index(close)]
        txt = [x for x in body if x]
        if txt and not re.search(r"[?.]$", txt[0]):
            txt = txt[1:]          # the record title line of the first message
        out.append(" ".join(txt).strip())
    return out


def transcript_pairs(state: str, style: dict, case: str) -> list:
    msgs = [m for m in _messages(state, style) if m]
    if len(msgs) % 2:
        raise ParseError("an interview question without its answer")
    out = []
    for q, a in zip(msgs[0::2], msgs[1::2]):
        if not a.endswith("."):
            raise ParseError("answer form")
        a0 = a[:-1]
        al = a0[0].lower() + a0[1:]
        m = re.fullmatch(r"What is the (.+) of (" + ID_RX + r")\?", q)
        if m:
            if m.group(2) != case:
                raise ParseError("interview about another case")
            out.append((m.group(1), al if al in ("don't know", "declined to answer", "can't recall") else a0))
            continue
        m = re.fullmatch(r'Did (' + ID_RX + r') have an? "([^"]+)" event\?', q)
        if m:
            key = f"{m.group(2)} for {m.group(1)}"
            mm = re.fullmatch(r"Yes, on (.+)", a0)
            if mm:
                out.append((key, mm.group(1)))
                continue
            mm = re.fullmatch(r"It is (scheduled|planned|expected|requested) for (.+)", a0)
            if mm:
                out.append((key, f"{mm.group(1)} for {mm.group(2)}"))
                continue
            if al in ("don't know", "declined to answer", "can't recall"):
                out.append((key, al))
                continue
            raise ParseError("event answer form")
        raise ParseError(f"interview question form: {q[:50]!r}")
    return out
