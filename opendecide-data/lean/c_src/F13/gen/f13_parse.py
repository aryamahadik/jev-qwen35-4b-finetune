"""F13 parser (G0 section 7): rendered row text -> sections -> facts (f13_model DATA schema), card features, query.
Reads only the row (state, card, instructions, question, options), and the pack view (entity nouns, attribute names
and units, scope kind and values, org name). Never imports the renderer (f13_text) or the samplers.

Containers (fmt1 skins): json, yaml (structured load), html_snippet (HTMLParser), markdown_table, memo, bullet_sop
(line grammar). Every fact sentence ends with '.', headings never do; field blocks follow a record label
"<item> record <ID>"; tables follow a caption "Table <T>" / "Part <k> of table <T>".
"""
from __future__ import annotations

import datetime as dt
import html as htmlmod
import json
import re
from html.parser import HTMLParser

import yaml

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
_MON = "(?:" + "|".join(MONTHS) + ")"
DATE_PAT = r"(?:\d{4}-\d{2}-\d{2}|\d{1,2} " + _MON + r" \d{4}|" + _MON + r" \d{1,2}, \d{4})"
DATE_RE = re.compile(DATE_PAT)
ID_PAT = r"[A-Z]{1,4}-[0-9A-Z]{2,6}"
VID_PAT = r"[A-Z]{1,4}-\d+\.\d+"
RID_PAT = r"[A-Z]{1,4}-\d+"
MARKERS = ("[not provided]", "[not provided in this copy]", "[illegible in this copy]")
TRACE = "__TRACE__"
OPP = {"at least": "ge", "at most": "le", "more than": "gt", "less than": "lt"}
BULLET = re.compile(r"^\s*(?:[-*•+▪◦·]|\d+[.)])\s+")


class ParseError(Exception):
    pass


def pdate(s: str) -> str:
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return s
    m = re.fullmatch(r"(\d{1,2}) (" + _MON[3:-1] + r") (\d{4})", s)
    if m:
        return dt.date(int(m.group(3)), MONTHS.index(m.group(2)) + 1, int(m.group(1))).isoformat()
    m = re.fullmatch(r"(" + _MON[3:-1] + r") (\d{1,2}), (\d{4})", s)
    if m:
        return dt.date(int(m.group(3)), MONTHS.index(m.group(1)) + 1, int(m.group(2))).isoformat()
    raise ParseError(f"date {s!r}")


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (s or "").lower()).strip("_")


# ================================================================================================ containers
class _H(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ev = []
        self.buf = None
        self.tag = None
        self.row = None

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3", "h4", "h5", "li", "th", "td", "dt", "dd", "p", "caption", "strong", "b"):
            if self.buf is None:
                self.buf, self.tag = [], tag
        if tag == "section":
            self.ev.append(("section",))
        if tag == "tr":
            self.row = []
        if tag in ("table", "dl"):
            self.ev.append(("tstart", tag))

    def handle_endtag(self, tag):
        if self.buf is not None and tag == self.tag:
            txt = re.sub(r"\s+", " ", "".join(self.buf)).strip()
            self.buf = None
            if tag in ("th", "td") and self.row is not None:
                self.row.append((tag, txt))
            elif tag in ("dt", "dd"):
                self.ev.append((tag, txt))
            else:
                self.ev.append(("h" if tag in ("h1", "h2", "h3", "h4", "h5", "strong", "b", "caption", "p") else tag,
                                txt))
        if tag == "tr" and self.row is not None:
            self.ev.append(("tr", self.row))
            self.row = None
        if tag in ("table", "dl"):
            self.ev.append(("tend", tag))
        if tag == "section":
            self.ev.append(("/section",))

    def handle_data(self, d):
        if self.buf is not None:
            self.buf.append(d)


class Seg:
    """Neutral segmentation: title + sections [{heading, blocks}], block = ("items", [str]) | ("fields", label,
    [(k, v)]) | ("table", caption, cols, rows)."""

    def __init__(self, ctx):
        self.ctx = ctx  # {"label_re": compiled, "caption_re": compiled, "title": str}
        self.title = None
        self.sections = []

    def new(self, heading):
        self.sections.append({"heading": heading.strip(), "blocks": []})

    def add_items(self, lines):
        if not self.sections:
            raise ParseError("items before the first heading")
        bl = self.sections[-1]["blocks"]
        if bl and bl[-1][0] == "items":
            bl[-1][1].extend(lines)
        else:
            bl.append(("items", list(lines)))


def _strip_fence(state: str) -> str:
    lines = state.split("\n")
    lines = [ln for ln in lines if not re.match(r"^\s*```", ln)]
    return "\n".join(lines)


def _dedent(text: str) -> str:
    lines = text.split("\n")
    ind = min((len(ln) - len(ln.lstrip(" ")) for ln in lines if ln.strip()), default=0)
    return "\n".join(ln[ind:] for ln in lines)


def _unwrap(obj):
    """A root holding scalar meta plus ONE mapping of sections (e.g. 'sections:' or a title key) -> flat root."""
    if isinstance(obj, dict):
        dv = [v for v in obj.values() if isinstance(v, dict)]
        lv = [v for v in obj.values() if isinstance(v, list)]
        if len(dv) == 1 and not lv and sum(isinstance(x, (list, dict)) for x in dv[0].values()) >= 2:
            return {**{k: v for k, v in obj.items() if not isinstance(v, dict)}, **dv[0]}
    return obj


def seg_struct(obj, ctx) -> Seg:
    S = Seg(ctx)
    obj = _unwrap(obj)
    if not isinstance(obj, dict):
        raise ParseError("structured root is not a mapping")
    for k, v in obj.items():
        if k in ("title", "name", "document", "heading") and isinstance(v, str) and S.title is None and not S.sections:
            S.title = v
            continue
        if isinstance(v, str) and not S.sections:
            continue  # doc meta pairs
        S.new(k)
        _struct_body(S, v, ctx)
    return S


def _struct_body(S, v, ctx):
    if isinstance(v, list):
        if all(isinstance(x, str) for x in v):
            S.add_items(v)
            return
        raise ParseError("section list of non-strings")
    if isinstance(v, str):
        S.add_items([v])
        return
    if not isinstance(v, dict):
        raise ParseError("section body type")
    for k2, v2 in v.items():
        if k2 in ("items", "notes", "lines", "entries", "points") and isinstance(v2, list):
            S.add_items([str(x) for x in v2])
        elif isinstance(v2, dict):
            S.sections[-1]["blocks"].append(("fields", k2, [(a, b) for a, b in v2.items()]))
        elif isinstance(v2, list) and v2 and all(isinstance(x, dict) for x in v2):
            cols = list(v2[0].keys())
            S.sections[-1]["blocks"].append(("table", k2, cols, [[x.get(c) for c in cols] for x in v2]))
        elif isinstance(v2, list):
            S.add_items([str(x) for x in v2])
        elif isinstance(v2, str):
            S.add_items([v2])
        else:
            raise ParseError(f"section value {k2}")


def seg_html(state, ctx) -> Seg:
    h = _H()
    h.feed(state)
    S = Seg(ctx)
    ev = h.ev
    pending_label = None
    i = 0
    in_sec = False
    while i < len(ev):
        e = ev[i]
        if e[0] == "section":
            in_sec = True
            pending_label = "__HEAD__"
        elif e[0] == "/section":
            in_sec = False
        elif e[0] == "h":
            t = e[1]
            if ctx["label_re"].match(t) or ctx["caption_re"].match(t):
                pending_label = t
            elif S.title is None and not S.sections:
                S.title = t
            elif (pending_label == "__HEAD__" or not in_sec) and t:
                S.new(t)
                pending_label = None
            else:
                S.new(t)
                pending_label = None
        elif e[0] == "li":
            S.add_items([e[1]])
        elif e[0] == "tstart":
            j = i + 1
            rows, pairs = [], []
            while j < len(ev) and ev[j][0] != "tend":
                if ev[j][0] == "tr":
                    rows.append(ev[j][1])
                elif ev[j][0] == "dt":
                    pairs.append([ev[j][1], None])
                elif ev[j][0] == "dd" and pairs:
                    pairs[-1][1] = ev[j][1]
                j += 1
            i = j
            if not S.sections:
                pending_label = None
                i += 1
                continue  # doc meta
            lab = pending_label if pending_label not in (None, "__HEAD__") else ""
            if pairs:
                S.sections[-1]["blocks"].append(("fields", lab, [tuple(p) for p in pairs]))
            elif rows and all(len(r) == 2 and r[0][0] == "th" and r[1][0] == "td" for r in rows):
                S.sections[-1]["blocks"].append(("fields", lab, [(r[0][1], r[1][1]) for r in rows]))
            elif rows:
                cols = [c[1] for c in rows[0]]
                S.sections[-1]["blocks"].append(("table", lab, cols, [[c[1] for c in r] for r in rows[1:]]))
            pending_label = None
        i += 1
    return S


def _md_strip(ln: str) -> str:
    s = ln.strip()
    s = re.sub(r"^#{1,6}\s+", "", s)
    m = re.fullmatch(r"\*\*(.+)\*\*", s)
    if m:
        s = m.group(1)
    return s


def seg_lines(state, ctx, container) -> Seg:
    S = Seg(ctx)
    lines = _strip_fence(state).split("\n")
    title_seen = False
    i = 0
    n = len(lines)

    def is_sep(s):
        return bool(re.fullmatch(r"[=\-_*~#]{3,}", s.strip()))

    while i < n:
        raw = lines[i]
        s = raw.strip()
        if not s or is_sep(s):
            i += 1
            continue
        if not title_seen:
            if ctx["title"].lower() in s.lower():
                title_seen = True
            i += 1
            continue
        if not S.sections and (": " in s and not BULLET.match(raw) and not s.endswith(".") and
                               not ctx["head_hint"](s)) or (not S.sections and BULLET.match(raw) and ": " in s and
                                                            not s.endswith(".")):
            i += 1  # doc meta pair
            continue
        body = _md_strip(s)
        # table (markdown) or fields
        if s.startswith("|"):
            block = []
            while i < n and lines[i].strip().startswith("|"):
                block.append(lines[i].strip())
                i += 1
            cells = [[c.strip() for c in ln.strip("|").split("|")] for ln in block
                     if not re.fullmatch(r"\|[\s:\-|]+\|", ln)]
            lab = S.sections[-1].pop("_label", "") if S.sections else ""
            if lab and ctx["label_re"].match(lab):
                S.sections[-1]["blocks"].append(("fields", lab, [(c[0], c[1]) for c in cells[1:]]))
            else:
                S.sections[-1]["blocks"].append(("table", lab, cells[0], cells[1:]))
            continue
        bm = BULLET.match(raw)
        content = raw[bm.end():].strip() if bm else body
        if ctx["label_re"].match(content) or ctx["caption_re"].match(content):
            if not S.sections:
                raise ParseError("label before heading")
            # field lines follow until a blank line (memo / bullet_sop) or a table (markdown)
            j = i + 1
            if j < n and lines[j].strip().startswith("|"):
                S.sections[-1]["_label"] = content
                i = j
                continue
            lt = _line_table(lines, j) if ctx["caption_re"].match(content) else None
            if lt is None and ctx["label_re"].match(content):
                ft_ = _line_table(lines, j)
                if ft_ and len(ft_[0]) == 2 and all(len(x) == 2 for x in ft_[1]):
                    S.sections[-1]["blocks"].append(("fields", content, [(x[0], x[1]) for x in ft_[1]]))
                    i = ft_[2]
                    continue
            if lt:
                S.sections[-1]["blocks"].append(("table", content, lt[0], lt[1]))
                i = lt[2]
                continue
            pairs = []
            while j < n and lines[j].strip():
                fl = lines[j]
                fm = BULLET.match(fl)
                fc = fl[fm.end():].strip() if fm else fl.strip()
                if ": " not in fc:
                    break
                k, v = fc.split(": ", 1)
                pairs.append((k, v))
                j += 1
            S.sections[-1]["blocks"].append(("fields", content, pairs))
            i = j
            continue
        if content.endswith(".") and (bm or S.sections):
            S.add_items([content])
            i += 1
            continue
        # heading
        h = re.sub(r"^\d+\.\s+", "", body)
        h = re.sub(r"^[-*•+]\s+", "", h)
        h = re.sub(r"^=+\s*(.*?)\s*=+$", r"\1", h)
        h = re.sub(r"^\[(.*)\]$", r"\1", h)
        h = h.rstrip(":").strip()
        S.new(h)
        i += 1
    for sc in S.sections:
        sc.pop("_label", None)
    return S


def _line_table(lines, j):
    """Plain-text tables after a caption: aligned columns over a '===' rule, bar-less ' | ' rows, or a grid."""
    n = len(lines)
    if j >= n or not lines[j].strip():
        return None
    if j + 1 < n and re.fullmatch(r"\s*=+(?:\s+=+)*\s*", lines[j + 1]):
        cols = re.split(r"\s{2,}", lines[j].strip())
        rows, k = [], j + 2
        while k < n and lines[k].strip():
            rows.append(re.split(r"\s{2,}", lines[k].strip()))
            k += 1
        return cols, rows, k
    if lines[j].strip().startswith("+"):
        body, k = [], j
        while k < n and lines[k].strip() and lines[k].strip()[0] in "+|":
            if lines[k].strip().startswith("|"):
                body.append([c.strip() for c in lines[k].strip().strip("|").split("|")])
            k += 1
        return (body[0], body[1:], k) if body else None
    if " | " in lines[j]:
        cols = [c.strip() for c in lines[j].strip().split(" | ")]
        rows, k = [], j + 1
        while k < n and lines[k].strip() and " | " in lines[k]:
            rows.append([c.strip() for c in lines[k].strip().split(" | ")])
            k += 1
        return cols, rows, k
    return None


def segment(state: str, ctx) -> Seg:
    td = _dedent(_strip_fence(state).strip("\n")).strip()
    if td.startswith("{"):
        return seg_struct(json.loads(td), ctx)
    if td.startswith("<"):
        return seg_html(state, ctx)
    try:
        obj = yaml.safe_load(td)
    except yaml.YAMLError:
        obj = None
    obj = _unwrap(obj)
    if isinstance(obj, dict) and sum(isinstance(v, (list, dict)) for v in obj.values()) >= 2:
        return seg_struct(obj, ctx)
    return seg_lines(state, ctx, None)


# ================================================================================================ pack-driven lexicon
class Lex:
    def __init__(self, pack: dict, card_feats: dict):
        self.pack = pack
        self.cf = card_feats
        self.attrs = {a["name"]: a for a in pack["nums"]}
        self.attr_slugs = {slug(a): a for a in self.attrs}
        self.nouns = [e["noun"] for e in pack["ents"]]
        self.kind = card_feats.get("scope_kind") or pack["scope_kind"]
        self.units = list(pack["units"]) if self.kind == pack["scope_kind"] else []
        nn = "|".join(re.escape(x) for x in sorted(self.nouns, key=len, reverse=True))
        self.label_re = re.compile(r"^(?:" + nn + r") record (" + ID_PAT + r")$", re.I)
        self.label_slug_re = re.compile(r"^(?:" + "|".join(slug(x) for x in self.nouns) + r")_record_([a-z0-9_]+)$")
        self.caption_re = re.compile(r"^(?:Part \d+ of table|Table) [A-Z0-9-]+(?: \(continued\))?$", re.I)
        an = "|".join(re.escape(x) for x in sorted(self.attrs, key=len, reverse=True))
        self.atom_re = re.compile(r"(?:the )?(" + an + r") is (at least|at most|more than|less than) (\d+)")
        self.unit_re = "|".join(re.escape(u) for u in sorted(self.units, key=len, reverse=True))

    def ctx(self):
        title = self.pack["org"]
        heads = ("chapter", "annex", "register", "bulletin", "notes", "file", "contacts", "staff", "glossary")
        return {"label_re": self.label_re, "caption_re": self.caption_re, "title": title,
                "head_hint": lambda s: s.lower().split(" ")[0].rstrip(":") in heads}

    def cid_from_label(self, lab: str) -> str | None:
        m = self.label_re.match(lab.strip())
        if m:
            return m.group(1)
        m = self.label_slug_re.match(slug(lab))
        if m:
            p = m.group(1).upper().split("_")
            return p[0] + "-" + "".join(p[1:])
        m = self.label_slug_re.match(slug(re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", lab.strip())))
        if m:
            x = re.fullmatch(r"([a-z]{1,4})_?(\d[0-9a-z]*)", m.group(1))
            if x:
                return x.group(1).upper() + "-" + x.group(2).upper()
        return None

    def conds(self, text: str):
        text = text.strip()
        atoms, joins, pos = [], [], 0
        for m in self.atom_re.finditer(text):
            gap = text[pos:m.start()].strip()
            if atoms:
                if gap not in ("and", "or"):
                    raise ParseError(f"cond gap {gap!r}")
                joins.append(gap)
            elif gap not in ("",):
                raise ParseError(f"cond lead {gap!r}")
            atoms.append({"attr": m.group(1), "op": OPP[m.group(2)], "val": int(m.group(3))})
            end = m.end()
            u = self.attrs[m.group(1)]["unit"]
            rest = text[end:]
            if u and rest.startswith(u):
                end += len(u)
            elif u and rest.startswith(" " + u):
                end += len(u) + 1
            pos = end
        if text[pos:].strip() or not atoms:
            raise ParseError(f"cond tail {text[pos:]!r}")
        if len(set(joins)) > 1:
            raise ParseError("mixed joins")
        return atoms, ("any" if joins and joins[0] == "or" else "all")

    def value(self, attr: str, v: str):
        v = v.strip()
        if v in MARKERS:
            return TRACE
        m = re.match(r"^(\d+)", v)
        if not m:
            raise ParseError(f"value {v!r}")
        return int(m.group(1))


# ================================================================================================ fact grammar
END_RE = r"(no end date|valid through (" + DATE_PAT + r")|repealed with effect from (" + DATE_PAT + r"))"


def _end(m, g0):
    if m.group(g0 + 1):
        return ["through", pdate(m.group(g0 + 1))]
    if m.group(g0 + 2):
        return ["repealed", pdate(m.group(g0 + 2))]
    return ["none"]


def parse_items(lines, L: Lex, item_noun_re, sec_scope_holder, st=None):
    """Item lines of one section -> facts. Mark lines attach to the item they name."""
    st = {} if st is None else st
    facts = []
    by_vid, by_eid = {}, {}
    outs = "|".join(re.escape(o) for o in sorted(L.cf["outcomes"], key=len, reverse=True))
    for ln in lines:
        ln = ln.strip()
        m = re.fullmatch(r"Rule (" + RID_PAT + r"), version (" + VID_PAT + r"): if (.+), the outcome for the "
                         + item_noun_re + r" is (" + outs + r")\.", ln)
        if m:
            cs, j = L.conds(m.group(3))
            f = {"ft": "rule", "rid": m.group(1), "vid": m.group(2), "rev": int(m.group(2).split(".")[-1]),
                 "scope": None, "status": None, "eff": None, "end": None, "conds": cs, "join": j,
                 "outcome": m.group(4), "form": "clause", "amends": None}
            facts.append(f)
            by_vid[f["vid"]] = f
            continue
        m = re.fullmatch(r"Amendment to rule (" + RID_PAT + r"): version (" + VID_PAT + r") amends version ("
                         + VID_PAT + r"); under version \2, if (.+), the outcome for the " + item_noun_re + r" is ("
                         + outs + r")\.", ln)
        if m:
            cs, j = L.conds(m.group(4))
            f = {"ft": "rule", "rid": m.group(1), "vid": m.group(2), "rev": int(m.group(2).split(".")[-1]),
                 "scope": None, "status": None, "eff": None, "end": None, "conds": cs, "join": j,
                 "outcome": m.group(5), "form": "amend", "amends": m.group(3)}
            facts.append(f)
            by_vid[f["vid"]] = f
            continue
        m = re.fullmatch(r"Version (" + VID_PAT + r") is marked for (.+)\.", ln)
        if m and m.group(1) in by_vid:
            by_vid[m.group(1)]["scope"] = m.group(2)
            continue
        m = re.fullmatch(r"Version (" + VID_PAT + r") status: (in force|draft|proposed|void)\.", ln)
        if m and m.group(1) in by_vid:
            by_vid[m.group(1)]["status"] = m.group(2)
            continue
        m = re.fullmatch(r"Version (" + VID_PAT + r"): effective (" + DATE_PAT + r"); " + END_RE + r"\.", ln)
        if m and m.group(1) in by_vid:
            by_vid[m.group(1)]["eff"] = pdate(m.group(2))
            by_vid[m.group(1)]["end"] = _end(m, 3)
            continue
        m = re.fullmatch(r"Version (" + VID_PAT + r"): " + END_RE + r"\.", ln)
        if m and m.group(1) in by_vid:
            by_vid[m.group(1)]["end"] = _end(m, 2)
            continue
        m = re.fullmatch(r"Version (" + VID_PAT + r") of rule (" + RID_PAT + r"): effective (" + DATE_PAT + r")\.", ln)
        if m:
            facts.append({"ft": "effreg", "vid": m.group(1), "rid": m.group(2), "eff": pdate(m.group(3))})
            continue
        m = re.fullmatch(r"Correction: (" + VID_PAT + r"|[A-Z]{1,4}-\d+) is void\.", ln)
        if m:
            facts.append({"ft": "void", "target": m.group(1)})
            continue
        m = re.fullmatch(r"Exception ([A-Z]{1,4}-\d+) to rule (" + RID_PAT + r") covers every " + item_noun_re
                         + r" whose (.+)\.", ln)
        if m:
            cs, j = L.conds(m.group(3))
            f = {"ft": "exc", "eid": m.group(1), "rid": m.group(2), "conds": cs, "join": j, "scope": None,
                 "status": None, "eff": None, "end": None}
            facts.append(f)
            by_eid[f["eid"]] = f
            continue
        m = re.fullmatch(r"Exception ([A-Z]{1,4}-\d+) is marked for (.+)\.", ln)
        if m and m.group(1) in by_eid:
            by_eid[m.group(1)]["scope"] = m.group(2)
            continue
        m = re.fullmatch(r"Exception ([A-Z]{1,4}-\d+) status: (in force|draft|proposed|void)\.", ln)
        if m and m.group(1) in by_eid:
            by_eid[m.group(1)]["status"] = m.group(2)
            continue
        m = re.fullmatch(r"Exception ([A-Z]{1,4}-\d+): effective (" + DATE_PAT + r"); " + END_RE + r"\.", ln)
        if m and m.group(1) in by_eid:
            by_eid[m.group(1)]["eff"] = pdate(m.group(2))
            by_eid[m.group(1)]["end"] = _end(m, 3)
            continue
        if _log_line(ln, L, facts, outs, item_noun_re):
            continue
        if _lc_line(ln, L, facts, st, outs, item_noun_re):
            continue
        m = re.fullmatch(re.escape(L.kind.capitalize()) + r": (.+)\.", ln)
        if m and not facts and (m.group(1) in L.units or (L.kind == "committee" and re.fullmatch(
                r"[A-Z][A-Za-z' ]+", m.group(1)))):
            sec_scope_holder.append(m.group(1))
            continue
        if re.search(r"\b(?:Rule|Version|Exception|Amendment|Correction|Motion|Proposal|Hold|Condition|Action|"
                     r"Decision|Revision|Meeting|Status)\b", ln) and (re.search(ID_PAT, ln) or re.search(DATE_PAT, ln)
                                                                    or ln.startswith("Status")):
            raise ParseError(f"unparsed query-type line {ln[:80]!r}")
        facts.append({"ft": "inert", "kind": "inert", "text": ln, "traced": False})
    for f in facts:
        if f["ft"] in ("rule", "exc") and (f["status"] is None or f["end"] is None):
            raise ParseError(f"incomplete item {f.get('vid') or f.get('eid')}")
        if f["ft"] in ("crit", "excl") and (f.get("eff") is None or f.get("status", 0) is None):
            raise ParseError(f"incomplete {f['ft']}")
        if f["ft"] in ("dec", "hold", "lcond") and (f.get("status") == "__P" or f.get("scope", 0) is None and
                                                    f["ft"] != "dec" or f.get("date", 0) is None):
            raise ParseError(f"incomplete {f['ft']} item")
    return facts


# ================================================================================================ S4 tables
def _table_fact(b, L, cf):
    """('table', caption, columns, rows) -> table fact; captions and headers may be slugged (JSON / YAML keys)."""
    _, cap, cols, rows = b
    m = re.fullmatch(r"table_([a-z])|part_(\d+)_of_table_([a-z])(_continued)?", slug(cap or ""))
    if not m:
        raise ParseError(f"table caption {cap!r}")
    name = (m.group(1) or m.group(3)).upper()
    part = int(m.group(2)) if m.group(2) else None
    if part is not None and (part > 1) != bool(m.group(4)):
        raise ParseError("continued mark")
    cmap = {}
    for nn in L.nouns:
        cmap[slug(nn + " ID")] = "id"
    for c in L.pack["cats"]:
        cmap[slug(c["name"])] = "cat"
    for a in L.pack["nums"]:
        cmap[slug(f"{a['name']} ({a['unit']})" if a["unit"] else a["name"])] = a["name"]
    if cf.get("tie_field"):
        cmap[slug(cf["tie_field"])] = "date"
    keys = []
    for c in cols:
        k = cmap.get(slug(str(c)))
        if k is None:
            raise ParseError(f"table column {c!r}")
        keys.append(k)
    out = []
    for row in rows:
        if len(row) != len(keys):
            raise ParseError("ragged table row")
        cells = []
        for k, v in zip(keys, row):
            v = str(v).strip()
            if k == "id":
                if not re.fullmatch(ID_PAT, v):
                    raise ParseError(f"table id {v!r}")
                cells.append(v)
            elif k == "cat":
                cells.append(v)
            elif k == "date":
                cells.append(pdate(v))
            else:
                cells.append(L.value(k, v))
        out.append(cells)
    return {"ft": "table", "name": name, "part": part, "cols": keys, "rows": out, "total": None, "tmeas": None}


# ================================================================================================ S2 / S6 grammar
def _lc_line(ln, L, facts, st, outs, item_noun_re) -> bool:
    """Decision notices (S2), motions / proposals / minutes corrections (S6), holds and conditions (S2), action items
    (S6), 'Meeting date' and 'Status: proposed.' lines. Appends facts; returns True when the line is consumed."""
    MT = "(" + item_noun_re + " " + ID_PAT + ")"
    O = "(" + outs + ")"
    m = re.fullmatch(r"Reporting period: (" + DATE_PAT + r") through (" + DATE_PAT + r")\.", ln)
    if m and st.get("period") is None:
        st["period"] = [pdate(m.group(1)), pdate(m.group(2))]
        return True
    m = re.fullmatch(r"Part total for part (\d+) of table ([A-Z]) \((.+?)\): (\d+)(?: .+)?\.", ln)
    if m:
        if m.group(3) not in L.attrs:
            raise ParseError("part total measure")
        st.setdefault("ptot", {})[(int(m.group(1)), m.group(2))] = (int(m.group(4)), m.group(3))
        return True
    m = re.fullmatch(r"Criterion (" + RID_PAT + r"): an? " + item_noun_re + r" is (" + outs + r") if (.+)\.", ln)
    if m:
        cs, j = L.conds(m.group(3))
        facts.append({"ft": "crit", "rid": m.group(1), "conds": cs, "join": j, "outcome": m.group(2), "eff": None})
        return True
    m = re.fullmatch(r"Criterion (" + RID_PAT + r"): effective (" + DATE_PAT + r"); no end date\.", ln)
    if m:
        for f in facts:
            if f["ft"] == "crit" and f["rid"] == m.group(1) and f["eff"] is None:
                f["eff"] = pdate(m.group(2))
                return True
        raise ParseError("criterion date without its criterion")
    m = re.fullmatch(r"Exclusion (" + ID_PAT + r") for (" + item_noun_re + r") (" + ID_PAT + r") is marked for (.+?); "
                     r"effective (" + DATE_PAT + r"); " + END_RE + r"\.", ln)
    if m:
        facts.append({"ft": "excl", "xid": m.group(1), "noun": m.group(2), "eid": m.group(3), "scope": m.group(4),
                      "status": None, "eff": pdate(m.group(5)), "end": _end(m, 6)})
        return True
    m = re.fullmatch(r"Exclusion (" + ID_PAT + r") status: (in force|draft|proposed|void)\.", ln)
    if m:
        for f in facts:
            if f["ft"] == "excl" and f["xid"] == m.group(1) and f["status"] is None:
                f["status"] = m.group(2)
                return True
        raise ParseError("exclusion status without its exclusion")
    m = re.fullmatch(r"Meeting date: (" + DATE_PAT + r")\.", ln)
    if m and not any(f["ft"] != "inert" for f in facts) and st.get("mdate") is None:
        st["mdate"] = pdate(m.group(1))
        return True
    m = re.fullmatch(r"Decision notice on " + MT + r", dated (" + DATE_PAT + r"): the outcome is " + O + r"\.", ln)
    if m:
        facts.append({"ft": "dec", "matter": m.group(1), "kind": "decision", "date": pdate(m.group(2)),
                      "outcome": m.group(3), "status": "in force", "votes": None})
        return True
    m = re.fullmatch(r"Revision notice on " + MT + r", dated (" + DATE_PAT + r"): the decision is revised; the outcome "
                     r"is " + O + r"\.", ln)
    if m:
        facts.append({"ft": "dec", "matter": m.group(1), "kind": "revision", "date": pdate(m.group(2)),
                      "outcome": m.group(3), "status": "in force", "votes": None})
        return True
    m = re.fullmatch(r"Motion to (make|revise) the decision on " + MT + r" so that \2 is " + O + r": in favour (\d+), "
                     r"against (\d+), abstain (\d+)\.", ln)
    if m:
        facts.append({"ft": "dec", "matter": m.group(2), "kind": "decision" if m.group(1) == "make" else "revision",
                      "date": st.get("mdate"), "outcome": m.group(3), "status": "in force",
                      "votes": [int(m.group(4)), int(m.group(5)), int(m.group(6))]})
        return True
    m = re.fullmatch(r"Proposal to revise the decision on " + MT + r" so that \1 is " + O + r"\.", ln)
    if m:
        facts.append({"ft": "dec", "matter": m.group(1), "kind": "revision", "date": st.get("mdate"),
                      "outcome": m.group(2), "status": "__P", "votes": None})
        return True
    if ln == "Status: proposed.":
        if not facts or facts[-1]["ft"] != "dec" or facts[-1]["votes"] is not None:
            raise ParseError("status line without a notice or proposal")
        facts[-1]["status"] = "proposed"
        return True
    m = re.fullmatch(r"Correction to the minutes of (" + DATE_PAT + r"): the (decision|revision) on " + MT +
                     r" made at the meeting of (" + DATE_PAT + r") is void\.", ln)
    if m:
        if pdate(m.group(1)) != pdate(m.group(4)):
            raise ParseError("void names two meetings")
        facts.append({"ft": "dvoid", "matter": m.group(3), "kind": m.group(2), "date": pdate(m.group(4))})
        return True
    m = re.fullmatch(r"Correction to the (decision|revision) notice on " + MT + r" dated (" + DATE_PAT +
                     r"): the notice is void\.", ln)
    if m:
        facts.append({"ft": "dvoid", "matter": m.group(2), "kind": m.group(1), "date": pdate(m.group(3))})
        return True
    m = re.fullmatch(r"Correction to the minutes of (" + DATE_PAT + r"): in the motion to (make|revise) the decision "
                     r"on " + MT + r", the outcome is " + O + r", not " + O + r"\.", ln)
    if m:
        facts.append({"ft": "dcorr", "matter": m.group(3), "kind": "decision" if m.group(2) == "make" else "revision",
                      "date": pdate(m.group(1)), "new": m.group(4), "old": m.group(5)})
        return True
    m = re.fullmatch(r"Correction to the (decision|revision) notice on " + MT + r" dated (" + DATE_PAT +
                     r"): the outcome is " + O + r", not " + O + r"\.", ln)
    if m:
        facts.append({"ft": "dcorr", "matter": m.group(2), "kind": m.group(1), "date": pdate(m.group(3)),
                      "new": m.group(4), "old": m.group(5)})
        return True
    m = re.fullmatch(r"Hold (" + ID_PAT + r") on (" + item_noun_re + r") (" + ID_PAT + r"): placed on (" + DATE_PAT +
                     r")(?:; released on (" + DATE_PAT + r"))?\.", ln)
    if m:
        facts.append({"ft": "hold", "hid": m.group(1), "noun": m.group(2), "eid": m.group(3),
                      "placed": pdate(m.group(4)), "released": pdate(m.group(5)) if m.group(5) else None,
                      "scope": None})
        return True
    m = re.fullmatch(r"Condition (" + ID_PAT + r") on (" + item_noun_re + r") (" + ID_PAT + r"): imposed on (" +
                     DATE_PAT + r")(?:; (met|waived) on (" + DATE_PAT + r"))?\.", ln)
    if m:
        facts.append({"ft": "lcond", "cnd": m.group(1), "noun": m.group(2), "eid": m.group(3),
                      "imposed": pdate(m.group(4)), "end": [m.group(5), pdate(m.group(6))] if m.group(5) else None,
                      "scope": None})
        return True
    m = re.fullmatch(r"(Hold|Condition) (" + ID_PAT + r") is marked for (.+)\.", ln)
    if m:
        key = "hid" if m.group(1) == "Hold" else "cnd"
        for f in facts:
            if f.get(key) == m.group(2):
                if f["scope"] is not None:
                    raise ParseError("two marks")
                f["scope"] = m.group(3)
                return True
        raise ParseError("mark for an unknown item")
    m = re.fullmatch(r"Action item (" + ID_PAT + r"): (.+)\.", ln)
    if m:
        ev = []
        for part in m.group(2).split("; "):
            x = re.fullmatch(r"(assigned|transferred) to (.+) on (" + DATE_PAT + r")", part)
            if x:
                ev.append([x.group(1), x.group(2), pdate(x.group(3))])
                continue
            x = re.fullmatch(r"(closed|reopened) on (" + DATE_PAT + r")", part)
            if not x:
                raise ParseError(f"action item event {part[:40]!r}")
            ev.append([x.group(1), None, pdate(x.group(2))])
        facts.append({"ft": "aitem", "aid": m.group(1), "events": ev})
        return True
    return False


TRACE_RE = re.compile(r"^(.+) \((.+)\): not included in this copy\.$")


def parse_doc(row: dict, pack: dict, card_feats: dict) -> dict:
    L = Lex(pack, card_feats)
    S = segment(row["state"], L.ctx())
    item_re = "(?:" + "|".join(re.escape(x) for x in L.nouns) + ")"
    secs = []
    for i, sc in enumerate(S.sections):
        out = {"sid": f"p{i:02d}", "heading": sc["heading"], "scope": None, "facts": [], "trace": None,
               "kind": None, "role": None}
        items = [ln for b in sc["blocks"] if b[0] == "items" for ln in b[1]]
        if len(items) == 1 and TRACE_RE.match(items[0]) and not any(b[0] != "items" for b in sc["blocks"]):
            m = TRACE_RE.match(items[0])
            out["trace"] = {"label": m.group(1), "scope_label": m.group(2)}
            out["kind"] = "trace"
            secs.append(out)
            continue
        holder = []
        st = {}
        for b in sc["blocks"]:
            if b[0] == "fields":
                cid = L.cid_from_label(b[1])
                if not cid:
                    raise ParseError(f"fields label {b[1]!r}")
                attrs, scope, gdate = {}, None, None
                for k, v in b[2]:
                    ks = slug(k)
                    v = str(v)
                    if ks == slug(L.kind):
                        scope = v
                    elif ks == slug(card_feats["gname"]):
                        gdate = pdate(v)
                    elif ks in L.attr_slugs:
                        attrs[L.attr_slugs[ks]] = L.value(L.attr_slugs[ks], v)
                    else:
                        raise ParseError(f"field {k!r}")
                out["facts"].append({"ft": "case", "cid": cid, "attrs": attrs, "scope": scope, "gdate": gdate})
                out["kind"] = "case_record"
            elif b[0] == "items":
                out["facts"].extend(parse_items(b[1], L, item_re, holder, st))
            else:
                out["facts"].append(_table_fact(b, L, card_feats))
        if holder:
            out["scope"] = holder[0]
        if st.get("mdate"):
            out["mdate"] = st["mdate"]
        if st.get("period"):
            out["period"] = st["period"]
        for f in out["facts"]:
            if f["ft"] == "table":
                key = (f["part"], f["name"])
                if key in st.get("ptot", {}):
                    f["total"], f["tmeas"] = st["ptot"].pop(key)
        if st.get("ptot"):
            raise ParseError("part total without its table")
        secs.append(out)
    return {"title": S.title, "sections": secs}


# ================================================================================================ card + question
def parse_card(text: str, pack: dict) -> dict:
    t = re.sub(r"\s+", " ", text)
    cf = {}
    m = re.search(r"shown as '(\[[^\]]+\])'", t)
    cf["marker"] = m.group(1) if m else None
    cf["world"] = "closed" if "Treat the document as complete" in t else (
        "open" if "is not given in this copy" in t else None)
    m = re.search(r"If no rule gives an outcome for the case, the outcome is '([^']+)'\.", t)
    cf["default"] = m.group(1) if m else None
    m = re.search(r"If two records tie on the measure a question asks about, choose the one with the (earlier|lower) "
                  r"(.+?)\. ", t + " ")
    cf["tie"] = None if not m else ("date" if m.group(1) == "earlier" else "number")
    cf["tie_field"] = m.group(2) if m and m.group(1) == "earlier" else None
    m = re.search(r"A motion carries if at least (\d+) members vote in favour", t)
    cf["vote_k"] = int(m.group(1)) if m else None
    m = re.search(r"marked for an? ([a-z][a-z ]*?) applies only to cases, matters and questions of that", t)
    cf["scope_kind"] = m.group(1) if m else None
    k = cf["scope_kind"] or pack["scope_kind"]
    if re.search(r"A rule for a specific " + re.escape(k) + r" overrides a rule with no " + re.escape(k), t):
        cf["precedence"] = "specific"
    elif "A rule with a later effective date overrides an earlier rule" in t:
        cf["precedence"] = "later"
    else:
        cf["precedence"] = None
    m = re.search(r"use the rules and versions in force on its (.+?), and read", t)
    cf["gname"] = m.group(1) if m else None
    m = re.search(r"The possible outcomes are (.+?)\.(?: |$)", t)
    cf["outcomes"] = []
    if m:
        body = m.group(1)
        for os_ in pack["outsets"]:
            alts = sorted(os_, key=len, reverse=True)
            rest = body
            for o in alts:
                rest = rest.replace(o, "\x00")
            if re.fullmatch(r"\x00(?:, \x00)*(?: and \x00)?", rest) and rest.count("\x00") == len(os_):
                cf["outcomes"] = list(os_)
                break
        if not cf["outcomes"]:
            cf["outcomes"] = [x.strip() for x in re.split(r", | and ", body)]
    return cf


def parse_case_desc(s: str, L: Lex, cf: dict) -> dict:
    s = s.strip()
    m = re.match(r"^an? (.+?) with (.+)$", s)
    if not m:
        raise ParseError(f"case desc {s[:60]!r}")
    keys = list(L.attrs) + [L.kind, cf["gname"]]
    kre = "|".join(re.escape(k) for k in sorted(keys, key=len, reverse=True))
    body = m.group(2)
    parts = list(re.finditer(r"(?:^|, | and )(" + kre + r") ", body))
    attrs, scope, gdate = {}, None, None
    for i, p in enumerate(parts):
        v = body[p.end(): parts[i + 1].start() if i + 1 < len(parts) else len(body)]
        k = p.group(1)
        if k == L.kind:
            scope = v
        elif k == cf["gname"]:
            gdate = pdate(v)
        else:
            attrs[k] = L.value(k, v)
    if scope is None or gdate is None:
        raise ParseError("case desc lacks scope / date")
    return {"cid": None, "attrs": attrs, "scope": scope, "gdate": gdate}


def parse_question(q: str, options, pack: dict, cf: dict) -> dict:
    L = Lex(pack, cf)
    item_re = "(?:" + "|".join(re.escape(x) for x in L.nouns) + ")"
    outs = "|".join(re.escape(o) for o in sorted(cf["outcomes"], key=len, reverse=True))
    out = {"neg": 0, "inner_neg": False}

    def cref(x):
        m = re.fullmatch(item_re + r" record (" + ID_PAT + r")", x)
        if m:
            return {"case_ref": m.group(1)}
        return {"case": parse_case_desc(x, L, cf)}
    m = re.fullmatch(r"What is the outcome for (.+)\?", q)
    if m:
        return {**out, "qk": "qp_outcome", "form": "choice", **cref(m.group(1))}
    m = re.fullmatch(r"Is it (not the case|true) that the outcome for (.+) is not (" + outs + r")\?", q)
    if m:
        return {**out, "qk": "qp_outcome", "form": "yn", "neg": 2 if m.group(1) == "not the case" else 1,
                **cref(m.group(2)), "claim": {"value": m.group(3)}}
    m = re.fullmatch(r"Is the outcome for (.+) (" + outs + r")\?", q)
    if m:
        return {**out, "qk": "qp_outcome", "form": "yn", **cref(m.group(1)), "claim": {"value": m.group(2)}}
    m = re.fullmatch(r"Does the document (fail to )?(establish|settle whether) that the outcome for (.+) is (not )?("
                     + outs + r")\?", q) or re.fullmatch(
        r"Does the document (fail to )?(settle whether) the outcome for (.+) is (not )?(" + outs + r")\?", q)
    if m:
        return {**out, "qk": "qp_outcome", "form": "establish" if m.group(2) == "establish" else "settle",
                "neg": 1 if m.group(1) else 0, "inner_neg": bool(m.group(4)), **cref(m.group(3)),
                "claim": {"value": m.group(5)}}
    m = re.fullmatch(r"Which version of rule (" + RID_PAT + r") is in force for (.+) as of (" + DATE_PAT + r")\?", q)
    if m:
        return {**out, "qk": "qr_version", "form": "choice", "rid": m.group(1), "unit": m.group(2),
                "date": pdate(m.group(3))}
    m = re.fullmatch(r"How many exceptions for (.+) are active as of (" + DATE_PAT + r")\?", q)
    if m:
        return {**out, "qk": "ag1_exc", "form": "choice", "unit": m.group(1), "date": pdate(m.group(2))}
    m = re.fullmatch(r"Which of these cases meets rule (" + RID_PAT + r")\?", q)
    if m:
        # repair r5 B7: the listed cases are the options (SEM-56); the abstain option is not a case description
        cs = []
        for o in options or []:
            try:
                cs.append(parse_case_desc(o, L, cf))
            except ParseError:
                continue
        return {**out, "qk": "qp_inverted", "form": "inverted", "rid": m.group(1), "cases": cs,
                "shown": list(range(len(cs)))}
    r_ = _lc_question(q, out, item_re, outs)
    if r_ is not None:
        return r_
    r_ = _tab_question(q, out, item_re, outs, L)
    if r_ is not None:
        return r_
    r_ = _log_question(q, out, item_re, outs)
    if r_ is not None:
        return r_
    raise ParseError(f"question {q[:80]!r}")


def _lc_question(q, out, item_re, outs):
    MT = "(" + item_re + " " + ID_PAT + ")"
    DT = "(" + DATE_PAT + ")"
    m = re.fullmatch(r"What is the decision on " + MT + r" for (.+?) as of " + DT + r"\?", q)
    if m:
        return {**out, "qk": "qr_decision", "form": "choice", "matter": m.group(1), "unit": m.group(2),
                "date": pdate(m.group(3))}
    m = re.fullmatch(r"Is it (not the case|true) that the decision on " + MT + r" for (.+?) is not (" + outs +
                     r") as of " + DT + r"\?", q)
    if m:
        return {**out, "qk": "qr_decision", "form": "yn", "neg": 2 if m.group(1) == "not the case" else 1,
                "matter": m.group(2), "unit": m.group(3), "claim": {"value": m.group(4)}, "date": pdate(m.group(5))}
    m = re.fullmatch(r"Is the decision on " + MT + r" for (.+?) (" + outs + r") as of " + DT + r"\?", q)
    if m:
        return {**out, "qk": "qr_decision", "form": "yn", "matter": m.group(1), "unit": m.group(2),
                "claim": {"value": m.group(3)}, "date": pdate(m.group(4))}
    m = re.fullmatch(r"Does the document (fail to )?(establish that|settle whether) the decision on " + MT +
                     r" for (.+?) is (not )?(" + outs + r") as of " + DT + r"\?", q)
    if m:
        return {**out, "qk": "qr_decision", "form": "establish" if m.group(2) == "establish that" else "settle",
                "neg": 1 if m.group(1) else 0, "inner_neg": bool(m.group(5)), "matter": m.group(3),
                "unit": m.group(4), "claim": {"value": m.group(6)}, "date": pdate(m.group(7))}
    m = re.fullmatch(r"How many (holds|conditions) on (" + item_re + r") (" + ID_PAT + r") for (.+?) are active as of "
                     + DT + r"\?", q)
    if m:
        return {**out, "qk": "ag1_hold" if m.group(1) == "holds" else "ag1_cond", "form": "choice",
                "noun": m.group(2), "eid": m.group(3), "unit": m.group(4), "date": pdate(m.group(5))}
    m = re.fullmatch(r"How many open action items for (.+?) have (.+?) as their holder as of " + DT + r"\?", q)
    if m:
        return {**out, "qk": "ag1_items", "form": "choice", "unit": m.group(1), "holder": m.group(2),
                "date": pdate(m.group(3))}
    AI = r"action item (" + ID_PAT + r") for (.+?) as of " + DT + r"\?"
    m = re.fullmatch(r"Who is the holder of " + AI, q)
    if m:
        return {**out, "qk": "qr_holder", "form": "choice", "aid": m.group(1), "unit": m.group(2),
                "date": pdate(m.group(3))}
    m = re.fullmatch(r"Is it (not the case|true) that (.+?) is not the holder of " + AI, q)
    if m:
        return {**out, "qk": "qr_holder", "form": "yn", "neg": 2 if m.group(1) == "not the case" else 1,
                "claim": {"value": m.group(2)}, "aid": m.group(3), "unit": m.group(4), "date": pdate(m.group(5))}
    m = re.fullmatch(r"Does the document (fail to )?(establish that|settle whether) (.+?) is (not )?the holder of " +
                     AI, q)
    if m:
        return {**out, "qk": "qr_holder", "form": "establish" if m.group(2) == "establish that" else "settle",
                "neg": 1 if m.group(1) else 0, "inner_neg": bool(m.group(4)), "claim": {"value": m.group(3)},
                "aid": m.group(5), "unit": m.group(6), "date": pdate(m.group(7))}
    m = re.fullmatch(r"Is (.+?) the holder of " + AI, q)
    if m:
        return {**out, "qk": "qr_holder", "form": "yn", "claim": {"value": m.group(1)}, "aid": m.group(2),
                "unit": m.group(3), "date": pdate(m.group(4))}
    return None



def _tab_question(q, out, item_re, outs, L):
    """S4 question forms (4.4, 3.2): periodic-table selections 'table <T> for <unit> from <D1> through <D2>', the
    report's criteria for an entity and a period, active exclusions as of a date."""
    DT = "(" + DATE_PAT + ")"
    PER = DT + " through " + DT
    SEL = r"table ([A-Z]) for (.+?) from " + PER
    an = "|".join(re.escape(x) for x in sorted(L.attrs, key=len, reverse=True))
    MEAS = "(" + an + ")"
    plur = "|".join(re.escape(e["plural"]) for e in L.pack["ents"])

    def sel(m, i):
        return {"table": m.group(i), "unit": m.group(i + 1), "period": [pdate(m.group(i + 2)), pdate(m.group(i + 3))]}

    def thr(meas, txt):
        v = L.value(meas, txt)
        if v == TRACE:
            raise ParseError("trace in a question")
        u = L.attrs[meas]["unit"]
        if u and txt.strip() not in (f"{v} {u}", f"{v}{u}"):
            raise ParseError("threshold unit")
        return v
    m = re.fullmatch(r"How many exclusions for (.+?) are active as of " + DT + r"\?", q)
    if m:
        return {**out, "qk": "ag1_excl", "form": "choice", "unit": m.group(1), "date": pdate(m.group(2))}
    m = re.fullmatch(r"How many (?:" + plur + r") in " + SEL + r" have " + MEAS + r" of (at least|at most|more than|"
                     r"less than) (.+)\?", q)
    if m:
        return {**out, "qk": "tq_count", "form": "choice", **sel(m, 1), "measure": m.group(5), "op": OPP[m.group(6)],
                "thr": thr(m.group(5), m.group(7))}
    m = re.fullmatch(r"Which (?:" + plur + r") in " + SEL + r" have " + MEAS + r" of (at least|at most|more than|"
                     r"less than) (.+)\?", q)
    if m:
        return {**out, "qk": "tq_set", "form": "choice", **sel(m, 1), "measure": m.group(5), "op": OPP[m.group(6)],
                "thr": thr(m.group(5), m.group(7))}
    m = re.fullmatch(r"What is the total " + MEAS + r" in " + SEL + r"\?", q)
    if m:
        return {**out, "qk": "ag3_sum", "form": "choice", **sel(m, 2), "measure": m.group(1)}
    m = re.fullmatch(r"Which " + item_re + r" in " + SEL + r" has the highest " + MEAS + r"\?", q)
    if m:
        return {**out, "qk": "tq_argmax", "form": "choice", **sel(m, 1), "measure": m.group(5)}
    E = item_re + " (" + ID_PAT + ")"
    m = re.fullmatch(r"Does " + E + r" have the highest " + MEAS + r" in " + SEL + r"\?", q)
    if m:
        return {**out, "qk": "tq_argmax", "form": "yn", "claim": {"value": m.group(1)}, "measure": m.group(2),
                **sel(m, 3)}
    m = re.fullmatch(r"Does " + E + r" have " + MEAS + r" of (at least|at most|more than|less than) (.+?) in " + SEL +
                     r"\?", q)
    if m:  # repair r6: tq_crit
        return {**out, "qk": "tq_crit", "form": "yn", "ent": m.group(1), "claim": {"value": m.group(1)},
                "measure": m.group(2), "op": OPP[m.group(3)], "thr": thr(m.group(2), m.group(4)), **sel(m, 5)}
    m = re.fullmatch(r"Is the " + MEAS + r" of " + E + r" higher than that of " + E + r" in " + SEL + r"\?", q)
    if m:
        return {**out, "qk": "tq_cmp", "form": "yn", "measure": m.group(1), "ent": m.group(2), "ent2": m.group(3),
                "claim": {"value": m.group(2)}, **sel(m, 4)}
    for pre, form in ((r"Is it (not the case|true) that ", "yn"),
                      (r"Does the document (fail to )?(establish that|settle whether) ", "est")):
        g0 = 1 if form == "yn" else 2
        m = re.fullmatch(pre + E + r" (has|does not have) the highest " + MEAS + r" in " + SEL + r"\?", q)
        if m:
            r_ = {**out, "qk": "tq_argmax", "claim": {"value": m.group(g0 + 1)}, "measure": m.group(g0 + 3),
                  **sel(m, g0 + 4)}
            return _pol(r_, form, m, m.group(g0 + 2) == "does not have")
        m = re.fullmatch(pre + E + r" (has|does not have) " + MEAS + r" of (at least|at most|more than|less than) (.+?) "
                         r"in " + SEL + r"\?", q)
        if m:  # repair r6: tq_crit
            r_ = {**out, "qk": "tq_crit", "ent": m.group(g0 + 1), "claim": {"value": m.group(g0 + 1)},
                  "measure": m.group(g0 + 3), "op": OPP[m.group(g0 + 4)], "thr": thr(m.group(g0 + 3), m.group(g0 + 5)),
                  **sel(m, g0 + 6)}
            return _pol(r_, form, m, m.group(g0 + 2) == "does not have")
        m = re.fullmatch(pre + r"the " + MEAS + r" of " + E + r" is (not )?higher than that of " + E + r" in " + SEL +
                         r"\?", q)
        if m:
            r_ = {**out, "qk": "tq_cmp", "measure": m.group(g0 + 1), "ent": m.group(g0 + 2), "ent2": m.group(g0 + 4),
                  "claim": {"value": m.group(g0 + 2)}, **sel(m, g0 + 5)}
            return _pol(r_, form, m, bool(m.group(g0 + 3)))
    LEAD = r"Under the report's criteria, "
    m = re.fullmatch(LEAD + r"what is the outcome for " + E + r" for " + PER + r"\?", q)
    if m:
        return {**out, "qk": "tp_outcome", "form": "choice", "ent": m.group(1),
                "period": [pdate(m.group(2)), pdate(m.group(3))]}
    m = re.fullmatch(LEAD + r"is " + E + r" (" + outs + r") for " + PER + r"\?", q)
    if m:
        return {**out, "qk": "tp_outcome", "form": "yn", "ent": m.group(1), "claim": {"value": m.group(2)},
                "period": [pdate(m.group(3)), pdate(m.group(4))]}
    for pre, form in ((r"is it (not the case|true) that ", "yn"),
                      (r"does the document (fail to )?(establish that|settle whether) ", "est")):
        g0 = 1 if form == "yn" else 2
        m = re.fullmatch(LEAD + pre + E + r" is (not )?(" + outs + r") for " + PER + r"\?", q)
        if m:
            r_ = {**out, "qk": "tp_outcome", "ent": m.group(g0 + 1), "claim": {"value": m.group(g0 + 3)},
                  "period": [pdate(m.group(g0 + 4)), pdate(m.group(g0 + 5))]}
            return _pol(r_, form, m, bool(m.group(g0 + 2)))
    return None


def _pol(r_, form, m, neg_in):
    """Polarity of a parsed yes/no family question: plain negation (neg 1 / 2) or establish / settle frames."""
    if form == "yn":
        if not neg_in:
            raise ParseError("'is it true that' without negation")
        r_["form"] = "yn"
        r_["neg"] = 2 if m.group(1) == "not the case" else 1
        return r_
    r_["form"] = "establish" if m.group(2) == "establish that" else "settle"
    r_["neg"] = 1 if m.group(1) else 0
    r_["inner_neg"] = neg_in
    return r_


# ================================================================================================ S3 log grammar
LOG_RE = re.compile(r"(" + DATE_PAT + r") (\d{2}:\d{2}) \| (\d+) \| ([^|]+?) \| (.+)\.")


def _log_line(ln, L, facts, outs, item_noun_re) -> bool:
    """'<date> <HH:MM> | <entry no> | <actor> | <text>.' log entries (S3). Appends one fact; True when consumed."""
    m = LOG_RE.fullmatch(ln)
    if not m:
        return False
    base = {"date": pdate(m.group(1)), "time": m.group(2), "no": int(m.group(3)), "actor": m.group(4)}
    t = m.group(5)
    x = re.fullmatch(r"Version (" + VID_PAT + r") of the (.+?) recorded; status (in force|proposed|draft); value (.+)",
                     t)
    if x:
        cfg = x.group(2)
        if not cfg.endswith(" setting") or cfg[:-8] not in L.attrs:
            raise ParseError(f"configuration {cfg!r}")
        facts.append({"ft": "le_ver", **base, "cfg": cfg, "vid": x.group(1), "status": x.group(3),
                      "value": L.value(cfg[:-8], x.group(4))})
        return True
    x = re.fullmatch(r"(" + VID_PAT + r") applied", t)
    if x:
        facts.append({"ft": "le_app", **base, "vid": x.group(1)})
        return True
    x = re.fullmatch(r"(.+?) rolled back to (" + VID_PAT + r")", t)
    if x:
        facts.append({"ft": "le_rb", **base, "cfg": x.group(1), "vid": x.group(2)})
        return True
    x = re.fullmatch(r"VOID entry (\d+)", t)
    if x:
        facts.append({"ft": "le_void", **base, "target": int(x.group(1))})
        return True
    x = re.fullmatch(r"Status of (" + item_noun_re + r") (" + ID_PAT + r") set to (" + outs + r")", t)
    if x:
        facts.append({"ft": "le_stat", **base, "noun": x.group(1), "eid": x.group(2), "status": x.group(3)})
        return True
    x = re.fullmatch(r"Record of version (" + VID_PAT + r") of the (.+?) viewed by (.+)", t)  # repair r9-2
    if x:
        facts.append({"ft": "le_noop", **base, "noun": "version", "eid": x.group(1), "cfg": x.group(2),
                      "verb": "viewed", "user": x.group(3)})
        return True
    x = re.fullmatch(r"Comment added to the record of version (" + VID_PAT + r") of the (.+?) by (.+)", t)
    if x:
        facts.append({"ft": "le_noop", **base, "noun": "version", "eid": x.group(1), "cfg": x.group(2),
                      "verb": "comment", "user": x.group(3)})
        return True
    x = re.fullmatch(r"Record of (" + item_noun_re + r") (" + ID_PAT + r") viewed by (.+)", t)
    if x:
        facts.append({"ft": "le_noop", **base, "noun": x.group(1), "eid": x.group(2), "verb": "viewed",
                      "user": x.group(3)})
        return True
    x = re.fullmatch(r"Comment added to the record of (" + item_noun_re + r") (" + ID_PAT + r") by (.+)", t)
    if x:
        facts.append({"ft": "le_noop", **base, "noun": x.group(1), "eid": x.group(2), "verb": "comment",
                      "user": x.group(3)})
        return True
    raise ParseError(f"log entry text {t[:60]!r}")


def _log_question(q, out, item_re, outs):
    DT = "(" + DATE_PAT + ")"
    m = re.fullmatch(r"How many log entries for (.+?) set the status of an? (" + item_re + r") to (" + outs +
                     r") as of " + DT + r"\?", q)
    if m:
        return {**out, "qk": "lg_count", "form": "choice", "unit": m.group(1), "noun": m.group(2),
                "filt": m.group(3), "date": pdate(m.group(4))}
    m = re.fullmatch(r"What is the value of the (.+?) in force for (.+?) as of " + DT + r"\?", q)
    if m:
        return {**out, "qk": "ag2_config", "form": "choice", "cfg": m.group(1), "unit": m.group(2),
                "date": pdate(m.group(3))}
    m = re.fullmatch(r"Which version of the (.+?) is in force for (.+?) as of " + DT + r"\?", q)
    if m:
        return {**out, "qk": "lg_version", "form": "choice", "cfg": m.group(1), "unit": m.group(2),
                "date": pdate(m.group(3))}
    V = r"version (" + VID_PAT + r") of the (.+?)"
    m = re.fullmatch(r"Is it (not the case|true) that " + V + r" is not in force for (.+?) as of " + DT + r"\?", q)
    if m:
        return {**out, "qk": "lg_version", "form": "yn", "neg": 2 if m.group(1) == "not the case" else 1,
                "claim": {"value": m.group(2)}, "cfg": m.group(3), "unit": m.group(4), "date": pdate(m.group(5))}
    m = re.fullmatch(r"Does the document (fail to )?(establish that|settle whether) " + V + r" is (not )?in force for "
                     r"(.+?) as of " + DT + r"\?", q)
    if m:
        return {**out, "qk": "lg_version", "form": "establish" if m.group(2) == "establish that" else "settle",
                "neg": 1 if m.group(1) else 0, "inner_neg": bool(m.group(5)), "claim": {"value": m.group(3)},
                "cfg": m.group(4), "unit": m.group(6), "date": pdate(m.group(7))}
    m = re.fullmatch(r"Is " + V + r" in force for (.+?) as of " + DT + r"\?", q)
    if m:
        return {**out, "qk": "lg_version", "form": "yn", "claim": {"value": m.group(1)}, "cfg": m.group(2),
                "unit": m.group(3), "date": pdate(m.group(4))}
    R = r"(" + item_re + r") (" + ID_PAT + r") for (.+?)"
    m = re.fullmatch(r"What is the status of " + R + r" as of " + DT + r"\?", q)
    if m:
        return {**out, "qk": "lg_status", "form": "choice", "noun": m.group(1), "eid": m.group(2),
                "unit": m.group(3), "date": pdate(m.group(4))}
    m = re.fullmatch(r"Is it (not the case|true) that the status of " + R + r" is not (" + outs + r") as of " + DT +
                     r"\?", q)
    if m:
        return {**out, "qk": "lg_status", "form": "yn", "neg": 2 if m.group(1) == "not the case" else 1,
                "noun": m.group(2), "eid": m.group(3), "unit": m.group(4), "claim": {"value": m.group(5)},
                "date": pdate(m.group(6))}
    m = re.fullmatch(r"Does the document (fail to )?(establish that|settle whether) the status of " + R + r" is (not )?("
                     + outs + r") as of " + DT + r"\?", q)
    if m:
        return {**out, "qk": "lg_status", "form": "establish" if m.group(2) == "establish that" else "settle",
                "neg": 1 if m.group(1) else 0, "inner_neg": bool(m.group(6)), "noun": m.group(3),
                "eid": m.group(4), "unit": m.group(5), "claim": {"value": m.group(7)}, "date": pdate(m.group(8))}
    m = re.fullmatch(r"Is the status of " + R + r" (" + outs + r") as of " + DT + r"\?", q)
    if m:
        return {**out, "qk": "lg_status", "form": "yn", "noun": m.group(1), "eid": m.group(2), "unit": m.group(3),
                "claim": {"value": m.group(4)}, "date": pdate(m.group(5))}
    return None
