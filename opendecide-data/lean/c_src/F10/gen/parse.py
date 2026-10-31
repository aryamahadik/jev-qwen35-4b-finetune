"""F10 G3 round-trip parser (G0 section 5). Reads only the rendered row (card, instructions, state, options) plus
the registered phrase pools (lexicon.py), the pack's attribute lexicon (templated prose) and the fmt1 skin data
(format style -> container). Never imports the renderer, the samplers, the card generator or solver A. Rebuilds
legend, definitions (card order, card type, world, helpers), case and omitted set, and the query."""
from __future__ import annotations

import datetime as dt
import json
import re
from decimal import Decimal

import lexicon as L

MONTHS = {m: i + 1 for i, m in enumerate(L.MONTHS)}


class ParseError(Exception):
    pass


def ws(s):
    return " ".join(s.split())


BULLET = re.compile(r"^\s*(?:[-*•+·]\s+|\d+[.)]\s+|Step \d+:\s+|\(\d+\)\s+|>\s?)+")


def clean_lines(text):
    """Card text -> content lines: quote prefixes, xml tags, bullets and markdown chrome stripped."""
    out = []
    for raw in (text or "").split("\n"):
        ln = raw.rstrip()
        while ln.startswith(">"):
            ln = ln[1:].lstrip()
        s = ln.strip()
        mx = re.fullmatch(r"<(/?)(section|part)_([a-z])>", s)
        if mx:
            out.append("\x00ENDSEC" if mx.group(1) else f"Section {mx.group(3).upper()}")
            continue
        if not s or re.fullmatch(r"</?[a-z0-9_]+>", s) or re.fullmatch(r"[=\-_~*#+|:\s]+", s):
            continue
        s = re.sub(r"^#{1,6}\s+", "", s)
        s = re.sub(r"^\*\*(.+)\*\*:?$", r"\1", s)
        out.append(s)
    return out


def strip_bullet(s):
    return BULLET.sub("", s, count=1).strip()


# ------------------------------------------------------------------------------------------------ values
def p_date(s, fmt=None):
    s = s.strip()
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return dt.date(int(m[1]), int(m[2]), int(m[3])).toordinal(), "iso"
    m = re.fullmatch(r"(\d{1,2}) ([A-Z][a-z]+) (\d{4})", s)
    if m and m[2] in MONTHS:
        return dt.date(int(m[3]), MONTHS[m[2]], int(m[1])).toordinal(), "dmy"
    m = re.fullmatch(r"([A-Z][a-z]+) (\d{1,2}), (\d{4})", s)
    if m and m[1] in MONTHS:
        return dt.date(int(m[3]), MONTHS[m[1]], int(m[2])).toordinal(), "mdy"
    raise ParseError(f"date {s!r}")


def p_num(s, a):
    """'35.5 hours' -> grid units of attribute a (U1 values converted by the card's factor)."""
    s = s.strip()
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(?: (.+))?", s)
    if not m:
        raise ParseError(f"number {s!r}")
    q = Decimal(m[1])
    unit = m[2]
    want = a.get("currency") if a["type"] == "amount" else a.get("unit")
    if unit and want and unit != want:
        conv = a.get("conv")
        if conv and unit == conv["u1"]:
            q = q * conv["k"]
        else:
            raise ParseError(f"unit {unit!r} for {a['name']!r}")
    g = q * (Decimal(10) ** a["d"])
    if g != g.to_integral_value():
        raise ParseError("off-grid value")
    return int(g)


def p_list(s, values):
    """'a, b, c' over known values (values never contain ', ')."""
    parts = [x.strip() for x in s.split(", ")]
    if any(p not in values for p in parts):
        raise ParseError(f"list {s!r}")
    return parts


def p_value(s, a, card):
    t = a["type"]
    s = s.strip()
    if t in ("count", "qty", "amount"):
        return p_num(s, a)
    if t == "date":
        v, f = p_date(s)
        if card.get("date_fmt") and f != card["date_fmt"]:
            raise ParseError("date format differs from the card's")
        return v
    if t == "cat":
        if s not in a["values"]:
            raise ParseError(f"category {s!r}")
        return s
    if t == "flag":
        if s in ("yes", "true", True):
            return True
        if s in ("no", "false", False):
            return False
        raise ParseError(f"flag {s!r}")
    if t == "tag":
        if s == "none":
            return ()
        return tuple(sorted(p_list(s, a["values"])))
    raise ParseError(t)


# ------------------------------------------------------------------------------------------------ operator lexicon
def _tpl_rx(tpl):
    body = re.escape(tpl.replace("{a}", "\x00"))
    for ph, grp in (("{v}", r"(?P<v>.+?)"), ("{w}", r"(?P<w>.+?)"), ("{D}", r"(?P<D>.+?)"), ("{D2}", r"(?P<D2>.+?)"),
                    ("{N}", r"(?P<N>\d+)"), ("{E}", r"(?P<E>.+?)"), ("{S}", r"(?P<S>.+?)"), ("{k}", r"(?P<k>\d+)")):
        body = body.replace(re.escape(ph), grp)
    body = body.replace(re.escape("\x00"), "")
    return re.compile("^" + body + "$")


def _reg():
    """(attribute-type family, op tag, regex, literal length) for every registered atom phrase."""
    out = []

    def add(fam, tag, tpls):
        for t in tpls:
            out.append((fam, tag, _tpl_rx(t), len(re.sub(r"\{[a-zA-Z0-9]+\}", "", t))))
    for op in ("ge", "le", "gt", "lt"):
        add("num", ("cmp", op), L.CMP[op])
    add("num_count", ("cmp", "ge"), L.CMP["ge_count"])
    add("num_count", ("cmp", "lt"), L.CMP["lt_count"])
    add("num", ("rng", False), L.RNG)
    add("num", ("rng", True), L.HALF)
    for op in ("ge", "gt", "le", "lt"):
        add("date", ("cmp", op), L.DATE_CMP[op])
    add("date", ("win",), L.WINDOW)
    for d in ("after", "before"):
        add("date", ("rel", d), L.REL[d])
    add("cat", ("cat", False, "is"), L.CAT_IN1)
    add("cat", ("cat", False, "oneof"), L.CAT_INN)
    add("cat", ("cat", True, "is"), L.CAT_NOT1)
    add("cat", ("cat", True, "oneof"), L.CAT_NOTN)
    add("cat", ("cat", True, "other"), L.CAT_OTHER)
    add("cat", ("cat", True, "except"), L.CAT_EXCEPT)
    add("flag", ("flag", True), L.FLAG[True])
    add("flag", ("flag", False), L.FLAG[False])
    for m, tp in L.TAG.items():
        add("tag", ("tag", m), tp)
    out.sort(key=lambda x: -x[3])
    return out


REG = _reg()
FAM = {"count": ("num", "num_count"), "qty": ("num",), "amount": ("num",), "date": ("date",), "cat": ("cat",),
       "flag": ("flag",), "tag": ("tag",)}


def parse_atom(text, P):
    """P: parse state with legend (slot -> attr), names, date_fmt. Longest attribute-name prefix, then the longest
    registered phrase whose values parse."""
    text = text.strip()
    leg = P["legend"]
    cands = sorted(leg.items(), key=lambda kv: -len(kv[1]["name"]))
    for s, a in cands:
        nm = a["name"]
        if not text.startswith(nm + " "):
            continue
        rest = text[len(nm):]
        for fam, tag, rx, _ in REG:
            if fam not in FAM[a["type"]]:
                continue
            m = rx.match(rest)
            if not m:
                continue
            try:
                return _build(tag, s, a, m, P)
            except ParseError:
                continue
    raise ParseError(f"atom {text[:60]!r}")


def _build(tag, s, a, m, P):
    g = m.groupdict()
    k = tag[0]
    if k == "cmp":
        c = p_value(g.get("v") or g.get("D"), a, P)
        return {"k": "atom", "t": "cmp", "a": s, "op": tag[1], "c": c}
    if k == "rng":
        return {"k": "atom", "t": "rng", "a": s, "lo": p_value(g["v"], a, P), "hi": p_value(g["w"], a, P),
                "half": tag[1]}
    if k == "win":
        return {"k": "atom", "t": "rng", "a": s, "lo": p_value(g["D"], a, P), "hi": p_value(g["D2"], a, P),
                "half": False}
    if k == "rel":
        e = [x for x, b in P["legend"].items() if b["name"] == g["E"] and b["type"] == "date"]
        if not e:
            raise ParseError("event")
        return {"k": "atom", "t": "rel", "a": s, "e": e[0], "n": int(g["N"]), "dir": tag[1]}
    if k == "cat":
        S = p_list(g["S"], a["values"])
        if tag[2] == "is" and len(S) != 1:
            raise ParseError("single")
        return {"k": "atom", "t": "cat", "a": s, "S": sorted(S), "neg": tag[1], "style": tag[2]}
    if k == "flag":
        return {"k": "atom", "t": "flag", "a": s, "v": tag[1]}
    if k == "tag":
        m_ = tag[1]
        S = p_list(g["S"], a["values"]) if g.get("S") is not None else []
        kk = int(g["k"]) if g.get("k") is not None else 0
        if m_ == "has" and len(S) != 1:
            raise ParseError("has")
        return {"k": "atom", "t": "tag", "a": s, "m": m_, "S": sorted(S), "kk": kk}
    raise ParseError(k)


# ------------------------------------------------------------------------------------------------ definitions
def parse_ref(text, P):
    t = text.strip()
    for neg, pre in ((True, "it is not a "), (False, "it is a ")):
        if t.startswith(pre) and t[len(pre):] in P["terms"]:
            return {"k": "ref", "to": P["terms"][t[len(pre):]], "neg": neg}
    for neg, pre in ((True, "it is not "), (False, "it is ")):
        if t.startswith(pre) and t[len(pre):] in P["helpers"]:
            return {"k": "ref", "to": P["helpers"][t[len(pre):]], "neg": neg}
    return None


def parse_cond(text, P):
    r = parse_ref(text, P)
    return r if r is not None else parse_atom(text, P)


def parse_item(text, P, allow_unless=True):
    r = parse_ref(text, P)
    if r is not None:
        return r
    if allow_unless and ", unless " in text:
        a, b = text.split(", unless ", 1)
        return {"k": "item", "atom": parse_atom(a, P), "unless": parse_cond(b, P)}
    return {"k": "item", "atom": parse_atom(text, P), "unless": None}


def _two(text, P, pre, mid, post):
    if not (text.startswith(pre) and text.endswith(post)):
        return None
    inner = text[len(pre):len(text) - len(post)]
    idx = [m.start() for m in re.finditer(re.escape(mid), inner)]
    for i in idx:
        try:
            a = parse_item(inner[:i], P, allow_unless=False)
            b = parse_item(inner[i + len(mid):], P, allow_unless=False)
            return [a, b]
        except ParseError:
            continue
    return None


def parse_body(text, P):
    text = text.strip()
    for form, head in L.LIST_HEAD.items():
        if text.startswith(head + ": "):
            parts = text[len(head) + 2:].split(L.ITEM_SEP)
            items = [parse_item(p, P) for p in parts]
            if form in ("ANY", "NOTANY", "NOTALL") and items[-1].get("unless") is not None:
                raise ParseError("unless-position lint")
            return {"k": "body", "form": form, "items": items}
    if text.startswith("either "):
        two = _two(text, P, "either ", " or ", ", but not both")
        if two:
            return {"k": "body", "form": "XOR", "items": two}
    if text.startswith("neither "):
        two = _two(text, P, "neither ", " nor ", "")
        if two:
            return {"k": "body", "form": "NEITHER", "items": two}
    return {"k": "body", "form": "single", "items": [parse_item(text, P)]}


def split_def_text(text, name):
    """body sentence, ONLY-IF condition text, Exception text (registered sentence frames)."""
    oi_pre = f" A record is a {name} only if "
    exc_tail = f" is not a {name}."
    exc_pre = " Exception: a record "
    body, oi, exc = text, None, None
    j = body.find(exc_pre)
    if j >= 0 and body.endswith(exc_tail):
        exc = body[j + len(exc_pre):len(body) - len(exc_tail)]
        body = body[:j]
    i = body.find(oi_pre)
    if i >= 0:
        if not body.endswith("."):
            raise ParseError("only-if")
        oi = body[i + len(oi_pre):-1]
        body = body[:i]
    if not body.endswith("."):
        raise ParseError("definition must end with '.'")
    return body[:-1], oi, exc


FAQ_SPLIT = re.compile(r" Q: [^?]*\? A: ")


def strip_faq(text, name):
    """S5 FAQ glossary: keep the base line and every answer in a registered ONLY-IF / Exception frame for this term
    (narrowing); an answer in any other form must be a restated reading rule and adds nothing (it is dropped)."""
    parts = FAQ_SPLIT.split(text)
    if len(parts) == 1:
        return text
    keep = [parts[0]]
    for a in parts[1:]:
        if a.startswith(f"A record is a {name} only if ") or (a.startswith("Exception: a record ")
                                                               and a.endswith(f" is not a {name}.")):
            keep.append(a)
        elif a.startswith("A record is a ") or a.startswith("Exception: "):
            raise ParseError("FAQ answer frame")
    return " ".join(keep)


def parse_def(text, name, did, P, helper=False):
    body_t, oi_t, exc_t = split_def_text(strip_faq(text, name), name)
    d = {"id": did, "body": parse_body(body_t, P), "onlyif": None, "exc": None, "helper": helper, "section": None}
    if oi_t is not None:
        d["onlyif"] = parse_cond(oi_t, P)
    if exc_t is not None:
        if exc_t.startswith("where "):
            d["exc"] = parse_atom(exc_t[6:], P)
        elif exc_t.startswith("that "):
            r = parse_ref("it " + exc_t[5:], P)
            if r is None or r["neg"]:
                raise ParseError("exception reference")
            d["exc"] = r
        else:
            raise ParseError("exception frame")
    return d


def split_examples(text):
    """Strip an inline ' (e.g. ex1; ex2)' tail (fmt1 option lines and DV12)."""
    if text.endswith(")") and " (e.g. " in text:
        i = text.rfind(" (e.g. ")
        return text[:i], [x.strip() for x in text[i + 7:-1].split("; ")]
    return text, []


# ------------------------------------------------------------------------------------------------ card
def _frame_rx(tpl, groups):
    body = re.escape(tpl)
    for ph, grp in groups.items():
        body = body.replace(re.escape(ph), grp)
    return re.compile("^" + body + "$")


LEG_HEAD = [_frame_rx(t, {"{E}": r"(?P<E>.+?)"}) for t in L.LEGEND_HEAD]
LEG_RX = [(t, _frame_rx(fr[t], {"{a}": r"(?P<a>[^:=|]+?)", "{u}": r"(?P<u>.+?)", "{d}": r"(?P<d>\d)",
                                "{cur}": r"(?P<cur>.+?)", "{V}": r"(?P<V>.+?)"}), len(re.sub(r"\{[a-zA-Z]+\}", "", fr[t])))
          for fr in L.ST19 for t in ("count", "amount", "qty", "cat", "flag", "date", "tag")]
DATE_FMT_TEXT = {txt: k for k, txt in L.DATE_FORMATS}


def _rule_rx(text):
    g = {"{E}": r"(?P<E>.+?)", "{M}": r"(?P<M>.+?)", "{CBD}": r"(?P<CBD>.+?)", "{NONE}": r"(?P<NONE>.+?)",
         "{T}": r".+?", "{doc}": r".+?", "{W}": r".+?", "{F}": r"(?P<F>.+?)", "{S}": r".+?", "{A}": r".+?",
         "{B}": r".+?", "{u1}": r"(?P<u1>.+?)", "{u1s}": r"(?P<u1s>.+?)", "{u2}": r"(?P<u2>.+?)", "{k}": r"(?P<k>\d+)",
         "{CUR}": r"(?P<CUR>.*?)"}
    body = re.escape(text)
    for ph, grp in g.items():
        body = body.replace(re.escape(ph), grp, 1).replace(re.escape(ph), "(?:.+?)")
    return re.compile("^" + body + "$")


RULE_RX = {i: [_rule_rx(t) for t in ts] for i, ts in L.ST.items() if i != "ST25_CUR"}
TYPE_RULE = {"ST27": "amo", "ST27b": "partition", "ST28": "first", "ST28_S3": "dlist", "ST43": "desc"}
MARKERS = {"'not recorded'": "not recorded", "'unknown'": "unknown", "null": "null",
           "leaving the attribute out": "key_left_out"}


def find_rules(lines):
    hits = {}
    for ln in lines:
        s = strip_bullet(ln)
        for i, rxs in RULE_RX.items():
            for rx in rxs:
                m = rx.match(s)
                if m:
                    hits.setdefault(i, m.groupdict())
    return hits


def parse_legend(lines, P):
    idx = None
    for i, ln in enumerate(lines):
        for rx in LEG_HEAD:
            m = rx.match(strip_bullet(ln))
            if m:
                idx, P["entity"] = i, m["E"]
                break
        if idx is not None:
            break
    if idx is None:
        raise ParseError("no legend")
    leg = {}
    for ln in lines[idx + 1:]:
        s = strip_bullet(ln)
        if any(rx.match(s) for rx, _ in HELPER_RX):
            break           # a helper-word override sentence ends the legend (it is never an attribute line)
        hits = []
        for t, rx, lit in LEG_RX:
            m = rx.match(s)
            if m:
                hits.append((len(m["a"]), -lit, t, m.groupdict()))
        if not hits:
            break
        hits.sort(key=lambda h: (h[0], h[1]))
        _, _, t, g = hits[0]
        a = {"name": g["a"], "type": t, "d": 0, "unit": None, "currency": None, "values": None, "conv": None}
        if t == "count":
            a["unit"] = g["u"]
        elif t == "amount":
            a["currency"], a["d"] = g["cur"], 2
        elif t == "qty":
            a["unit"], a["d"] = g["u"], int(g["d"])
        elif t in ("cat", "tag"):
            a["values"] = g["V"].split(", ")
        leg[len(leg)] = a
    if not leg:
        raise ParseError("empty legend")
    P["legend"] = leg
    P["legend_span"] = (idx, idx + 1 + len(leg))
    return idx + 1 + len(leg)


SEPS = (": ", " = ", " | ")
NOT_HEADS = ("Example", "Sample", "Illustration", "Exception", "Note", "Outcome for", "Answer", "Output", "Input")
EX_PRE = ("Example: ", "Sample: ", "Illustration: ")
HELPER_RX = [(re.compile(r"^In this (?P<doc>.+?), (?P<W>.+?) means (?P<B>.+)\.$"), None),
             (re.compile(r"^In section (?P<S>[A-Z]) only, (?P<W>.+?) means (?P<B>.+)\.$"), "S"),
             (re.compile(r"^Elsewhere in this (?P<doc>.+?), (?P<W>.+?) means (?P<B>.+)\.$"), None)]
SEC_RX = re.compile(r"^(?:\d+[.)]\s*|\[\d+\]\s*)?(?:section|part) (?P<S>[a-z])\s*:?$", re.I)
SEC_XML = re.compile(r"^<(?:section|part)_(?P<S>[a-z])>$")


def head_split(s):
    for sep in SEPS:
        i = s.find(sep)
        if i > 0:
            name = s[:i].strip()
            if any(name.startswith(h) for h in NOT_HEADS) or len(name.split()) > 3:
                continue
            return name, s[i + len(sep):]
    return None, None


def parse_glossary(lines, P, start):
    """Definitions (card order), helper overrides with their sections, in-definition examples."""
    terms, helpers = {}, {}
    cand = []
    section = None
    for raw in lines[start:]:
        if raw == "\x00ENDSEC":
            section = None
            continue
        s = strip_bullet(raw)
        m = SEC_RX.match(re.sub(r"^[\[(<=\s]+|[\])>:=\s]+$", "", s))
        if m:
            section = m["S"].upper()
            continue
        hm = None
        for rx, kind in HELPER_RX:
            mm = rx.match(s)
            if mm:
                hm = (mm, kind)
                break
        if hm is not None:
            mm, kind = hm
            W = mm["W"]
            hid = "h:" + W + (":A" if kind == "S" else "")
            helpers[W if kind != "S" else W + "@A"] = hid
            cand.append(("helper", hid, W, mm["B"] + ".", mm.groupdict().get("S")))
            continue
        name, rest = head_split(s)
        if name is not None:
            cand.append(("term", name, name, rest, section))
    P["terms"] = {c[1]: "t:" + c[1] for c in cand if c[0] == "term"}
    P["helpers"] = {}
    for k, v in helpers.items():
        P["helpers"].setdefault(k.split("@")[0], v)
    defs, order, examples = {}, [], {}
    for kind, key, name, text, sec in cand:
        if kind == "helper":
            hid = key
            # section-scoped helper: references written inside its section resolve to the scoped definition
            try:
                d = parse_def(text, name, hid, P, helper=True)
            except ParseError:
                continue
            d["section"] = sec
            defs[hid] = d
            continue
        text, exs = split_examples(text)
        try:
            d = parse_def(text, name, "t:" + name, {**P, "helpers": _scoped(P, helpers, sec)})
        except ParseError:
            P["terms"].pop(name, None)
            continue
        d["section"] = sec
        did = "t:" + name
        if did in defs:
            raise ParseError(f"two definitions for {name!r}")
        defs[did] = d
        order.append(did)
        if exs:
            examples.setdefault(did, []).extend(exs)
    P["order_names"] = [d[2:] for d in order]
    return defs, order, examples


def _scoped(P, helpers, sec):
    out = {}
    for k, v in helpers.items():
        w = k.split("@")[0]
        if k.endswith("@A"):
            if sec == "A":
                out[w] = v
        else:
            out.setdefault(w, v)
            if sec != "A":
                out[w] = v
    if sec == "A":
        for k, v in helpers.items():
            if k.endswith("@A"):
                out[k.split("@")[0]] = v
    return out


def _cells(s):
    s = s.strip()
    if s.startswith("|") and s.endswith("|"):
        return [c.strip() for c in s[1:-1].split(" | ")]
    if " | " in s:
        return [c.strip() for c in s.split(" | ")]
    return [c.strip() for c in re.split(r"\s{2,}", s)]


def parse_table(lines, P):
    """S3 code table (ST51 grammar): header 'code' <columns> 'rule'; one atom per non-'any' cell."""
    hdr = None
    for i, ln in enumerate(lines):
        c = _cells(ln)
        if len(c) >= 3 and c[0] == "code" and c[-1] == "rule":
            hdr = (i, c)
            break
    if hdr is None:
        raise ParseError("no code table")
    i0, cols = hdr
    leg = P["legend"]
    colslots = []
    for nm in cols[1:-1]:
        sl = [s for s, a in leg.items() if a["name"] == nm]
        if not sl:
            raise ParseError(f"table column {nm!r}")
        colslots.append(sl[0])
    rows = []
    for ln in lines[i0 + 1:]:
        c = _cells(ln)
        if len(c) != len(cols):
            break
        rows.append(c)
    P["terms"] = {r[0]: "t:" + r[0] for r in rows}
    P["helpers"] = {}
    defs, order = {}, []
    for r in rows:
        name = r[0]
        items = []
        for s, cell in zip(colslots, r[1:-1]):
            if cell == L.TABLE_ANY:
                continue
            items.append({"k": "item", "atom": parse_atom(leg[s]["name"] + " " + cell, P), "unless": None})
        if not items:
            raise ParseError("row with no condition")
        d = {"id": "t:" + name, "body": {"k": "body", "form": "single" if len(items) == 1 else "ALL", "items": items},
             "onlyif": None, "exc": None, "helper": False, "section": None}
        rule = r[-1]
        if rule != L.RULE_NONE:
            for part in rule.split("; "):
                if part.startswith("only if "):
                    d["onlyif"] = parse_atom(part[8:], P)
                elif part.startswith("exception: "):
                    d["exc"] = parse_atom(part[11:], P)
                else:
                    raise ParseError(f"rule cell {rule!r}")
        defs[d["id"]] = d
        order.append(d["id"])
    return defs, order


def parse_record_line(text, P):
    """'a <entity> with <attr> <value>, <attr> <value>' -> (stated slots, case)."""
    pre = f"a {P['entity']} with "
    if not text.startswith(pre):
        raise ParseError("example record")
    rest = text[len(pre):]
    leg = P["legend"]
    names = sorted(((a["name"], s) for s, a in leg.items()), key=lambda x: -len(x[0]))
    pos, found = 0, []
    while pos < len(rest):
        hit = next(((nm, s) for nm, s in names if rest.startswith(nm + " ", pos)), None)
        if hit is None:
            raise ParseError("example attribute")
        nm, s = hit
        vstart = pos + len(nm) + 1
        nxt = len(rest)
        for nm2, _ in names:
            j = rest.find(", " + nm2 + " ", vstart)
            if j >= 0:
                nxt = min(nxt, j)
        found.append((s, rest[vstart:nxt]))
        pos = nxt + 2 if nxt < len(rest) else nxt
    case = {}
    for s, v in found:
        case[s] = p_value(v, leg[s], P)
    return sorted(case), case


def parse_examples(lines, P, inline):
    """Every in-definition example: (record, term name, s3?)"""
    out = []
    texts = list(inline)
    for ln in lines:
        s = strip_bullet(ln)
        for pre in EX_PRE:
            if s.startswith(pre):
                texts.append(s[len(pre):].rstrip("."))
    for t in texts:
        for frame, s3 in ((" meets the conditions of row ", True), (" meets the definition of ", False)):
            if frame in t:
                rec, name = t.rsplit(frame, 1)
                out.append((parse_record_line(rec, P), name, s3))
                break
        else:
            raise ParseError("example frame")
    return out


# ------------------------------------------------------------------------------------------------ state (record)
def nk(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def _unfence(text):
    lines = [l for l in text.split("\n") if not re.match(r"^\s*(```|~~~)", l)]
    ind = [len(l) - len(l.lstrip(" ")) for l in lines if l.strip()]
    m = min(ind) if ind else 0
    return "\n".join(l[m:] for l in lines).strip("\n")


def _flatten(o, path, out):
    if isinstance(o, dict):
        for k, v in o.items():
            _flatten(v, path + [str(k)], out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            _flatten(v, path + [str(i)], out)
    else:
        out.append((path, o))


class _HT:
    def __init__(self, text):
        from html.parser import HTMLParser

        class H(HTMLParser):
            def __init__(s):
                super().__init__(convert_charrefs=True)
                s.cells, s.rows, s.cur, s.dl, s.pending_dt, s.text, s.heads = None, [], None, [], None, [], []
                s.tag = None

            def handle_starttag(s, tag, a):
                s.tag = tag
                if tag == "tr":
                    s.cells = []
                if tag in ("td", "th", "dt", "dd", "h1", "h2", "h3", "h4", "h5", "p", "li"):
                    s.cur = []

            def handle_endtag(s, tag):
                t = "".join(s.cur or []).strip()
                if tag in ("td", "th") and s.cells is not None:
                    s.cells.append(" ".join(t.split()))
                elif tag == "tr" and s.cells is not None:
                    s.rows.append(s.cells)
                    s.cells = None
                elif tag == "dt":
                    s.pending_dt = t
                elif tag == "dd":
                    s.dl.append((s.pending_dt, " ".join(t.split())))
                    s.rows.append(["\x00DL", s.pending_dt, " ".join(t.split())])
                elif tag in ("h1", "h2", "h3", "h4", "h5"):
                    s.heads.append(t)
                    s.rows.append(["\x00HEAD", t])
                elif tag in ("p", "li"):
                    s.text.append(" ".join(t.split()))
                s.cur = None if tag in ("td", "th", "dt", "dd", "h1", "h2", "h3", "h4", "h5", "p", "li") else s.cur

            def handle_data(s, d):
                if s.cur is not None:
                    s.cur.append(d)
        h = H()
        h.feed(text)
        self.rows, self.dl, self.text = h.rows, h.dl, h.text


KV_RX = [re.compile(r"^(?P<k>[^:=|\[\]]+?)\s*::\s+(?P<v>.+)$"),
         re.compile(r"^(?P<k>[^:=|\[\]]+?):\s+\[ (?P<v>.+) \]$"), re.compile(r"^(?P<k>[^:=|\[\]]+?):\s+(?P<v>.+?)\.?$"),
         re.compile(r"^(?P<k>[a-zA-Z0-9_ ]+?)\s?=\s?(?P<v>.+)$"), re.compile(r"^(?P<k>.+?) \.{3,} (?P<v>.+)$"),
         re.compile(r"^(?P<k>[^|]+?) \| (?P<v>.+)$"), re.compile(r"^\[(?P<k>[^\]]+)\] (?P<v>.+)$"),
         re.compile(r"^The (?P<k>.+?) is (?P<v>.+?)\.$")]


def kv_pairs(text):
    """Key-value pairs from line-oriented containers (key-value, form, memo, bullet SOP, prose fields)."""
    out = []
    for raw in _unfence(text).split("\n"):
        s = strip_bullet(raw.strip())
        if not s:
            continue
        multi = s.count(": ") >= 2 or (s.startswith("The ") and s.count(" is ") >= 2)
        parts = re.split(r"(?<=\.)\s+(?=[a-zA-Z])", s) if multi else [s]
        for p in parts:
            for rx in KV_RX:
                m = rx.match(p.strip())
                if m:
                    out.append((m["k"].strip(), m["v"].strip()))
                    break
    return out


def table_pairs(text, names):
    """(key, value) pairs from a one-row table in csv / markdown / html form (header row = attribute names)."""
    t = _unfence(text)
    if "<t" in t:
        h = _HT(t)
        rows = [r for r in h.rows if r and r[0] != "\x00HEAD"]
        if len(rows) >= 2:
            return list(zip(rows[0], rows[1]))
        return list(h.dl)
    lines = [l.strip() for l in t.split("\n") if l.strip()]   # an indented code block keeps CSV quoting intact
    for i, l in enumerate(lines):
        for splitter in (lambda x: [c.strip() for c in x.strip().strip("|").split("|")],
                         lambda x: next(iter(__import__("csv").reader([x], delimiter=","))),
                         lambda x: [c.strip() for c in x.split(";")], lambda x: [c.strip() for c in x.split("\t")],
                         lambda x: [c.strip() for c in re.split(r"\s{2,}", x.strip())]):
            hdr = splitter(l)
            if len(hdr) >= 2 and all(nk(h) in names for h in hdr):
                for nxt in lines[i + 1:]:
                    if re.fullmatch(r"[|\s:\-]+", nxt):
                        continue
                    vals = splitter(nxt)
                    if len(vals) == len(hdr):
                        return list(zip(hdr, vals))
    raise ParseError("table record")


MARKER_WORDS = {"not recorded": "not recorded", "unknown": "unknown"}


def _assign(pairs, P, marker):
    leg = P["legend"]
    byk = {nk(a["name"]): s for s, a in leg.items()}
    case, omitted, seen = {}, [], set()
    for k, v in pairs:
        s = byk.get(nk(k))
        if s is None:
            continue
        if s in seen:
            raise ParseError(f"attribute {k!r} twice")
        seen.add(s)
        if v is None:
            if marker != "null":
                raise ParseError("null on a non-null style")
            omitted.append(s)
            continue
        if isinstance(v, bool):
            if leg[s]["type"] != "flag":
                raise ParseError("typed bool on a non-flag")
            case[s] = v
            continue
        if isinstance(v, (int, float)):
            v = str(v)
        if len(v) >= 2 and v[0] == v[-1] == '"':
            v = v[1:-1]         # a style that quotes every scalar value
        if v in MARKER_WORDS:
            if marker != v:
                raise ParseError(f"marker {v!r} not the style's")
            omitted.append(s)
            continue
        if leg[s]["type"] == "flag" and v in ("true", "false") and not P.get("typed"):
            raise ParseError("untyped true/false")
        case[s] = p_value(v, leg[s], P)
    for s in leg:
        if s not in seen:
            if marker != "key_left_out":
                raise ParseError(f"attribute {leg[s]['name']!r} left out on a {marker!r} style")
            omitted.append(s)
    return case, sorted(omitted)


def statement_pairs(text, P, pack_attrs):
    """Templated prose: each sentence is one registered attribute statement (pack lexicon) or an omission
    statement; attack / inert sentences match neither and give no value."""
    leg = P["legend"]
    E = P["entity"]
    refs = [f.format(E=E) for f in L.ENTITY_REF]
    out = []
    body = [strip_bullet(l.strip()) for l in _unfence(text).split("\n")]
    body = [l for l in body if l.endswith(".") and not re.fullmatch(r"[=\-_*#\s]+", l)]
    sents = re.split(r"(?<=\.)\s+(?=[A-Z])", " ".join(body))
    for snt in sents:
        snt = snt.strip()
        hit = False
        best = []
        for s, a in leg.items():
            pa = pack_attrs.get(a["name"])
            if not pa:
                continue
            for kind, tpl in (pa.get("statements") or {}).items():
                if not tpl:
                    continue
                for ref in refs:
                    rx = "^" + re.escape(tpl.replace("{E}", "\x01")).replace("\x01", re.escape(ref)).replace(
                        re.escape("{v}"), "(?P<v>.+?)") + r"\.$"
                    m = re.match(rx, snt)
                    if not m:
                        continue
                    v = {"positive": "yes", "negative": "no", "none": "none"}.get(kind, m.groupdict().get("v"))
                    try:
                        p_value(v, a, P)
                    except ParseError:
                        continue
                    best.append((len(tpl), a["name"], v))
        if best:
            best.sort(key=lambda x: -x[0])
            if len(best) > 1 and best[0][0] == best[1][0] and best[0][1] != best[1][1]:
                raise ParseError("ambiguous statement")
            out.append((best[0][1], best[0][2]))
            hit = True
        if not hit:
            for f in L.OMIT_STMT:
                rx = "^" + re.escape(f).replace(re.escape("{a}"), "(?P<a>.+?)").replace(re.escape("{E}"), re.escape(E)).replace(
                    re.escape("{M}"), "(?P<M>not recorded|unknown)") + "$"
                m = re.match(rx, snt)
                if m:
                    out.append((m["a"], m["M"]))
                    break
    return out


def parse_state(state, P, container, marker, pack_attrs=None, prose_record=False):
    P["typed"] = container in ("json", "yaml")
    if container == "json":
        t = _unfence(state)
        try:
            obj = json.loads(t)
        except Exception:
            obj = [json.loads(l) for l in t.split("\n") if l.strip()]
        flat = []
        _flatten(obj, [], flat)
        pairs = [(p[-1], v) for p, v in flat]
    elif container == "yaml":
        import yaml
        t = "\n".join(l for l in _unfence(state).split("\n") if not l.lstrip().startswith("#"))
        flat = []
        _flatten(yaml.safe_load(t), [], flat)
        pairs = [(p[-1], v) for p, v in flat]
    elif container in ("csv", "markdown_table", "html_snippet"):
        pairs = table_pairs(state, {nk(a["name"]) for a in P["legend"].values()})
    elif prose_record:
        pairs = statement_pairs(state, P, pack_attrs or {})
    else:
        pairs = kv_pairs(state)
    return _assign(pairs, P, marker)


# ------------------------------------------------------------------------------------------------ question
def _q_rx(tpl, extra=None):
    # a slot never spans a question mark, so an earlier question-like sentence (an S5 FAQ line, an example text)
    # cannot swallow the row's question
    g = {"{E}": r"(?P<E>[^?]+?)", "{X}": r"(?P<X>[^?]+?)", "{C}": r"(?P<C>[^?]+?)"}
    body = re.escape(tpl)
    for ph, grp in g.items():
        body = body.replace(re.escape(ph), grp, 1)
        name = grp[4:grp.index(">")]
        body = body.replace(re.escape(ph), f"(?P={name})")
    return re.compile(body)


def _qs(rx, t, P):
    """First match whose target slot is a defined term: a reading-rule sentence that quotes a question-like phrase
    ("'Is a Y' means ...") is skipped and the search resumes one character later (matches may overlap)."""
    m = rx.search(t)
    while m is not None and m["X"] not in P["terms"]:
        m = rx.search(t, m.start() + 1)
    return m


def parse_question(instr, qtype, P):
    """(form, wording kind, target name or None, negation level)."""
    t = ws(instr)
    if qtype == "noul":
        clauses = []
        for kind, tpls in L.Q_YN.items():
            for q, pos, neg in tpls:
                clauses.append((kind, q, pos, neg))
        for kind, q, pos, neg in clauses:     # double negation first (longest frame)
            m = _qs(_q_rx(L.TRUTH_NEG[0].replace("{C}", neg)), t, P)
            if m:
                return "yn", kind, m["X"], 2
        for kind, q, pos, neg in clauses:
            m = _qs(_q_rx(L.TRUTH_POS[0].replace("{C}", neg)), t, P)
            if m:
                return "yn", kind, m["X"], 1
            m = _qs(_q_rx(L.TRUTH_NEG[0].replace("{C}", pos)), t, P)
            if m:
                return "yn", kind, m["X"], 1
        for kind, q, pos, neg in clauses:
            m = _qs(_q_rx(q), t, P)
            if m:
                return "yn", kind, m["X"], 0
        raise ParseError("yes/no question")
    for tpl in L.Q_INVERTED:
        m = _qs(_q_rx(tpl), t, P)
        if m:
            return "inv", "meets", m["X"], 0
    for key, tpls in L.Q_CHOICE.items():
        for tpl in tpls:
            if _q_rx(tpl).search(t):
                return "choice", ("defines" if key == "s6" else "assigned"), None, 0
    raise ParseError("choice question")


def abstain_key(o):
    if o in L.NONE_TEXT or o in L.NONE_TEXT_S3:
        return "none"
    if o in L.CBD_TEXT:
        return "cbd"
    return None


# ------------------------------------------------------------------------------------------------ row
def card_text(row):
    return ((row.get("card") or "") + "\n" + (row.get("instructions") or ""))


def parse_program_row(row, container, sampler, pack_attrs=None, prose_record=False):
    """Parse one program row (S1-S4, S6). Returns a dict: card_like, query, case, omitted, examples, opt_keys."""
    P = {}
    lines = clean_lines(card_text(row))
    end = parse_legend(lines, P)
    rules = find_rules(lines)
    types = [TYPE_RULE[i] for i in rules if i in TYPE_RULE]
    if len(set(types)) != 1:
        raise ParseError(f"card type sentences {types}")
    ctype = types[0]
    world = "open" if "ST5" in rules else ("closed" if "ST4" in rules else None)
    marker = MARKERS.get(rules["ST5"]["M"]) if "ST5" in rules else None
    if "ST23" in rules:
        f = rules["ST23"]["F"]
        P["date_fmt"] = DATE_FMT_TEXT.get(f)
        if P["date_fmt"] is None:
            raise ParseError("date format")
    if "ST26" in rules:
        g = rules["ST26"]
        for a in P["legend"].values():
            if a["type"] in ("count", "qty") and a.get("unit") == g["u2"]:
                a["conv"] = {"u1": g["u1"], "k": int(g["k"])}
    a0, a1 = P["legend_span"]
    rest_lines = lines[:a0] + lines[a1:]
    if sampler == "S3":
        defs, order = parse_table(rest_lines, P)
        inline = []
    else:
        defs, order, inl = parse_glossary(rest_lines, P, 0)
        inline = [x for v in inl.values() for x in v]
    if not order:
        raise ParseError("no definitions")
    exs = parse_examples(lines, P, inline)
    form, wkind, X, neg = parse_question(row.get("instructions") or "", row["qtype"], P)
    if wkind == "meets" and sampler == "S3":
        pass
    q = {"form": form, "wkind": wkind, "neg": neg}
    if X is not None:
        if X not in P["terms"]:
            raise ParseError(f"question target {X!r} is not a term")
        q["target"] = P["terms"][X]
    opt_keys = None
    if row["qtype"] == "choice" and form == "choice":
        opt_keys = []
        for o in row["options"]:
            a = abstain_key(o)
            if a:
                opt_keys.append(a)
            elif o in P["terms"]:
                opt_keys.append(P["terms"][o])
            else:
                raise ParseError(f"option {o!r} names no term")
        q["shown"] = opt_keys
    out = {"card_like": {"ctype": ctype, "legend": P["legend"], "defs": defs, "order": order, "world": world},
           "query": q, "examples": exs, "opt_keys": opt_keys, "P": P, "marker": marker}
    if form == "inv":
        out["records"] = parse_inverted_state(row, P, container, row["options"])
        q["records"] = [json.dumps(c, sort_keys=True, default=list) for c in sorted(
            [{str(k): v for k, v in rr.items()} for rr in out["records"].values()], key=lambda c: json.dumps(c, sort_keys=True, default=list))]
    elif sampler == "S6":
        out["description"] = parse_description(row["state"], P)
    else:
        mk = marker or ("key_left_out" if world == "open" else "none-closed")
        case, om = parse_state(row["state"], P, container, marker if world == "open" else "closed",
                               pack_attrs, prose_record)
        if world != "open" and om:
            raise ParseError("closed-world record leaves a fact out")
        out["case"], out["omitted"] = case, om
        q["case"] = {str(k): (list(v) if isinstance(v, tuple) else v) for k, v in sorted(case.items())}
        q["omitted"] = om
    return out


def parse_description(state, P):
    raw = _unfence(state)
    t = ws(raw)
    for f in L.DESC_FRAME:
        rx = "^" + re.escape(f).replace(re.escape("{E}"), re.escape(P["entity"])).replace(re.escape("{B}"), "(?P<B>.+)") + "$"
        for cand in [t] + [strip_bullet(x) for x in raw.split("\n")] + re.split(r"(?<=\.)\s+(?=[A-Z])", t):
            m = re.match(rx, cand.strip())
            if m:
                return {"id": "desc", "body": parse_body(m["B"], P), "onlyif": None, "exc": None, "helper": False,
                        "section": None}
    raise ParseError("description")


def parse_inverted_state(row, P, container, labels):
    """Inverted rows: the shown records, each under its record label (option text)."""
    lab_n = {nk(l): l for l in labels}
    state = row["state"]
    groups = {l: [] for l in labels}
    if container in ("json", "yaml"):
        if container == "json":
            obj = json.loads(_unfence(state))
        else:
            import yaml
            obj = yaml.safe_load("\n".join(l for l in _unfence(state).split("\n") if not l.lstrip().startswith("#")))
        flat = []
        _flatten(obj, [], flat)
        for path, v in flat:
            lab = next((lab_n[nk(p)] for p in path if nk(p) in lab_n), None)
            if lab is not None:
                groups[lab].append((path[-1], v))
    elif container == "html_snippet":
        h = _HT(_unfence(state))
        cur = None
        for ev in h.rows:
            if ev and ev[0] == "\x00HEAD":
                cur = lab_n.get(nk(ev[1]), cur if nk(ev[1]) not in lab_n else None)
                if nk(ev[1]) in lab_n:
                    cur = lab_n[nk(ev[1])]
                continue
            if cur is None:
                continue
            if ev and ev[0] == "\x00DL":
                groups[cur].append((ev[1], ev[2]))
            elif len(ev) == 2:
                groups[cur].append((ev[0], ev[1]))
    else:
        cur = None
        txt = _unfence(state)
        for raw in txt.split("\n"):
            s = strip_bullet(raw.strip())
            k = nk(re.sub(r"^\[|\]$|:$", "", s))
            if k in lab_n:
                cur = lab_n[k]
                continue
            if cur is None:
                continue
            if container in ("markdown_table", "csv") and s:
                # a record printed as a two-column table (attribute, value); header and rule rows name no attribute
                cells = [c.strip() for c in s.strip("|").split("|")] if s.startswith("|") else \
                    next(iter(__import__("csv").reader([s])))
                if len(cells) == 2:
                    groups[cur].append((cells[0], cells[1]))
                    continue
            for kk, vv in kv_pairs(s):
                groups[cur].append((kk, vv))
    out = {}
    for lab in labels:
        case, om = _assign(groups[lab], P, "closed")
        out[lab] = case
    return out
