"""G3 round-trip parser for F1 rows (G0 F1 v7 section 4 "Round-trip parse").

Works from the rendered row only (card, state, instructions, options), the F1 operator lexicon (lexicon.py, a step-4
artifact) and the pack's declared vocabulary (subject noun, Boolean phrasings, presuppositions, affix words). It never
imports the renderer, the samplers or solver A, and never sees templates ids, seeds or the drawn structure.
It rebuilds the canonical structure (fields, rules, notices, inert classes, policy, case facts, unknown / not-recorded
sets, question, option map) and fails loudly on banned constructs (6.1), construct-set violations (R9), R8, R10,
XF06 markers and 6.4 placement errors.
"""
from __future__ import annotations

import re
from decimal import Decimal

import datetime as dt
import lexicon as L
from decode import decode, norm
from model import Attr, Case, Inert, Item, Lit, Notice, Policy, Rule, Struct

MONTHS = {m: i + 1 for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                          "September", "October", "November", "December"])}
DATE_RE = r"(?:\d{4}-\d{2}-\d{2}|\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4})"
NUM_RE = r"-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|-?\d+(?:\.\d+)?"


class ParseError(Exception):
    pass


def pdate(s: str) -> int:
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return dt.date.fromisoformat(s).toordinal()
    m = re.fullmatch(r"(\d{1,2}) (\w+) (\d{4})", s)
    if m:
        return dt.date(int(m.group(3)), MONTHS[m.group(2)], int(m.group(1))).toordinal()
    raise ParseError(f"bad date {s!r}")


def pnum(s: str) -> Decimal:
    return Decimal(s.replace(",", ""))


def ws(s: str) -> str:
    return " ".join(s.split())


# ---------------------------------------------------------------- statements

def _stmt_regex(t: str):
    parts = re.split(r"(\{[a-z_A-Z]+\})", t)
    out = []
    seen = set()
    for p in parts:
        m = re.fullmatch(r"\{([a-z_A-Z]+)\}", p)
        if m:
            name = m.group(1)
            if name in seen:
                out.append(f"(?P={name})")
            else:
                seen.add(name)
                out.append(f"(?P<{name}>[^.;:]+?)" if name not in ("strict_list", "listed", "tier_chain",
                                                                  "sec_sentence", "other_scope")
                           else f"(?P<{name}>[^.;:]+?)")
        else:
            out.append(re.escape(p))
    return re.compile("".join(out))


STMT_RX = {}
for k, vs in L.STATEMENTS.items():
    STMT_RX[k] = [_stmt_regex(v) for v in vs]
SHORT_RX = {k: _stmt_regex(v) for k, v in L.SHORT.items()}
HEADER_RX = re.compile(r"Issued by (?P<body>[^.]+?)\. Base policy effective (?P<B>" + DATE_RE +
                       r")\. This policy covers cases whose (?P<scope_name>[^.]+?) is (?P<scope_value>[^.;]+?); a "
                       r"case's governing date is its (?P<gov>[^.]+?)\.")

BANNED = [r"\bprovided that\b", r"\bas long as\b", r"\bsubject to (?:Rule|Section|Clause|Provision|Row)\b",
          r"\bnotwithstanding\b", r"\bexcept as provided in\b", r"\bexcept where\b", r"\bif and only if\b",
          r"\bneither\b", r"\bnone of the following\b", r"\bother than\b",
          r"\b(?:up to|until|through|prior to|since|as of|by) " + DATE_RE, r"\bexpires on\b",
          r"\bwithin \d+ days (?:after|before|of)\b", r"\bdays ending on\b", r"\bno later than \d+ days after\b",
          r"\bcases dated\b", r"\b(?:refused|withheld|declined to (?:give|show|provide))\b[^.]*\b(?:evidence|proof)\b"]
BANNED_RX = [re.compile(b, re.I) for b in BANNED]
IMPERATIVE_STARTS = ("Use ", "Check ", "Compare ", "Choose ", "Answer ", "Ignore ", "Apply ", "Pick ", "Select ")
XF06_BANNED = [r"(?<![\w-])n/a(?![\w-])", r"\bTBD\b", r"\bunknown\b", r"\bnull\b"]
EXTRA_GOOD = ["good news for the {subj}", "the {subj} is cleared", "the {subj} gets what it seeks"]
EXTRA_BAD = ["bad news for the {subj}", "the {subj} is stopped for now", "the {subj} is sent back"]
MEANINGS = sorted(L.GOOD_MEANINGS + L.BAD_MEANINGS + EXTRA_GOOD + EXTRA_BAD, key=len, reverse=True)
GOODM = set(L.GOOD_MEANINGS) | set(EXTRA_GOOD)


class Parser:
    def __init__(self, row: dict, vocab: dict):
        self.row = row
        self.v = vocab
        self.subj = vocab["subject"]
        self.qtype = row["qtype"]
        self.kind, self.lines, self.tables = decode(row["state"])
        self.state_flat = ws("\n".join(self.lines))
        self.instr = ws(row.get("instructions") or "")
        self.card = row.get("card") or ""
        self.card_flat = ws(self.card)
        self.all_text = self.card_flat + " \n " + self.instr + " \n " + self.state_flat
        self.problems = []

    # ------------------------------------------------------------ helpers
    def fail(self, msg):
        raise ParseError(msg)

    def find_statements(self):
        shown = {}
        for k, rxs in STMT_RX.items():
            for rx in rxs:
                m = rx.search(self.all_text)
                if m:
                    shown[k] = m.groupdict()
                    where = "state" if (self.state_flat and rx.search(self.state_flat)) else \
                        ("card" if rx.search(self.card_flat) else "instructions")
                    shown[k]["_where"] = where
                    break
        short = {}
        for k, rx in SHORT_RX.items():
            m = rx.search(self.state_flat)
            if m:
                short[k] = m.groupdict()
        return shown, short

    # ------------------------------------------------------------ fields block
    FIELD_RX = re.compile(
        r"(?:(?<=^)|(?<=[\s>\"'|•*\-+]))(?P<f>[A-Z0-9][a-z0-9' \-]*?): (?:"
        r"a whole number of (?P<u1>[^,]+?), from (?P<lo1>" + NUM_RE + r")(?: ?(?P=u1))? to (?P<hi1>" + NUM_RE +
        r")(?: ?(?P=u1))?\."
        r"|an amount in (?P<u2>[^,]+?), to the cent, from (?P<lo2>" + NUM_RE + r")(?: ?(?P=u2))? to (?P<hi2>" +
        NUM_RE + r")(?: ?(?P=u2))?\."
        r"|a number of (?P<u3>.+?) in multiples of (?P<st3>" + NUM_RE + r"), from (?P<lo3>" + NUM_RE +
        r")(?: ?(?P=u3))? to (?P<hi3>" + NUM_RE + r")(?: ?(?P=u3))?\."
        r"|a date from (?P<dlo>" + DATE_RE + r") to (?P<dhi>" + DATE_RE + r")\."
        r"|a date\."
        r"|one of [\(\[](?P<vals>[^\)\]]+)[\)\]]\."
        r"|a yes/no fact\.)")

    def parse_fields(self):
        attrs = {}
        txt = "\n".join(self.lines)
        for m in self.FIELD_RX.finditer(txt):
            name = m.group("f")
            name = name[0].lower() + name[1:]
            g = m.groupdict()
            if g["lo1"] is not None:
                unit = g["u1"]
                unit, places, step = unit, 0, Decimal(1)
                lo, hi = pnum(self._strip_unit(g["lo1"], unit)), pnum(self._strip_unit(g["hi1"], unit))
                a = Attr(key=name, name=name, type="num", unit=unit, places=0, step=Decimal(1), lo=lo, hi=hi)
            elif g["lo2"] is not None:
                unit = g["u2"]
                a = Attr(key=name, name=name, type="num", unit=unit, places=2, step=Decimal("0.01"),
                         lo=pnum(g["lo2"]), hi=pnum(g["hi2"]), money=True)
            elif g["lo3"] is not None:
                unit = g["u3"]
                st = pnum(g["st3"])
                places = max(0, -st.as_tuple().exponent)
                a = Attr(key=name, name=name, type="num", unit=unit, places=places, step=st, lo=pnum(g["lo3"]),
                         hi=pnum(g["hi3"]))
            elif g["dlo"] is not None:
                a = Attr(key=name, name=name, type="date", lo=pdate(g["dlo"]), hi=pdate(g["dhi"]))
            elif g["vals"] is not None:
                a = Attr(key=name, name=name, type="cat", values=tuple(x.strip() for x in g["vals"].split(", ")))
            elif m.group(0).endswith("a yes/no fact."):
                bv = self.v["bools"].get(name)
                if bv is None:
                    self.fail(f"Boolean field without declared phrasing: {name}")
                a = Attr(key=name, name=name, type="bool", true=bv["true"], false=bv.get("false"),
                         presup=bv.get("presup"))
            else:
                a = Attr(key=name, name=name, type="date")
            if name in attrs:
                self.fail(f"field listed twice: {name}")
            attrs[name] = a
        if not attrs:
            self.fail("no Fields block")
        # a presupposed field that is not on the row: the phrasing presupposes nothing here (R8 holds trivially)
        for k, a in list(attrs.items()):
            if a.type == "bool" and a.presup and a.presup not in attrs:
                attrs[k] = Attr(**{**a.__dict__, "presup": None})
        # day-count fields are numeric fields whose unit is days (row 18)
        for k, a in list(attrs.items()):
            if a.type == "num" and a.unit in ("days", "day") and "day" in a.name:
                attrs[k] = Attr(**{**a.__dict__, "daycount": True})
        return attrs

    @staticmethod
    def _strip_unit(s, unit):
        return s

    # ------------------------------------------------------------ literals
    def setup_lexicon(self, attrs):
        self.attrs = attrs
        self.fnames = sorted([a.name for a in attrs.values() if a.type != "bool"], key=len, reverse=True)
        self.bool_phr = []
        for a in attrs.values():
            if a.type != "bool":
                continue
            subj = f"the {self.subj}"
            self.bool_phr.append((a.true.replace("{S}", subj), a.name, True))
            if a.false:
                self.bool_phr.append((a.false.replace("{S}", subj), a.name, False))
        self.bool_phr.sort(key=lambda x: len(x[0]), reverse=True)
        self.num_ops = sorted([(f, op) for op, fs in L.NUM_FORMS.items() for f in fs], key=lambda x: -len(x[0]))
        self.date_ops = sorted([(f, op) for op, fs in L.DATE_FORMS.items() for f in fs], key=lambda x: -len(x[0]))

    def _num_val(self, s, i, a):
        m = re.compile(r"(" + NUM_RE + r")").match(s, i)
        if not m:
            self.fail(f"number expected at {s[i:i + 30]!r}")
        v = pnum(m.group(1))
        j = m.end()
        if a.unit:
            sep = "" if a.unit == "%" else " "
            if not s.startswith(sep + a.unit, j):
                self.fail(f"unit {a.unit!r} expected after number")
            j += len(sep + a.unit)
        return v, j

    def _date_val(self, s, i):
        m = re.compile(DATE_RE).match(s, i)
        if not m:
            self.fail(f"date expected at {s[i:i + 30]!r}")
        return pdate(m.group(0)), m.end()

    def parse_lit(self, s, i, cat_br=None):
        for phr, name, val in self.bool_phr:
            if s.startswith(phr, i):
                end = i + len(phr)
                if end == len(s) or not s[end].isalnum():
                    return Lit(name, "is", (val,)), end
        for fn in self.fnames:
            if not s.startswith(fn + " ", i):
                continue
            a = self.attrs[fn]
            j = i + len(fn) + 1
            if a.type == "num":
                for form, op in self.num_ops:
                    if s.startswith(form + " ", j):
                        k = j + len(form) + 1
                        v1, k = self._num_val(s, k, a)
                        if op == "between":
                            if not s.startswith(" and ", k):
                                self.fail("between needs 'and'")
                            v2, k = self._num_val(s, k + 5, a)
                            return Lit(fn, "between", (v1, v2)), k
                        return Lit(fn, op, (v1,)), k
                self.fail(f"numeric operator expected after {fn!r}: {s[j:j + 30]!r}")
            if a.type == "date":
                if s.startswith("is from ", j):
                    d1, k = self._date_val(s, j + 8)
                    if not s.startswith(" to ", k):
                        self.fail("from-to needs 'to'")
                    d2, k = self._date_val(s, k + 4)
                    return Lit(fn, "fromto", (d1, d2)), k
                for form, op in self.date_ops:
                    if op == "fromto":
                        continue
                    if s.startswith(form + " ", j):
                        d, k = self._date_val(s, j + len(form) + 1)
                        return Lit(fn, op, (d,)), k
                self.fail(f"date operator expected after {fn!r}")
            if a.type == "cat":
                for form, op, multi in (("is not one of ", "notin", True), ("is one of ", "in", True),
                                        ("is not ", "notin", False), ("is ", "in", False)):
                    if s.startswith(form, j):
                        k = j + len(form)
                        if multi:
                            if s[k] not in "([":
                                self.fail("bracket expected for a category value set")
                            close = ")" if s[k] == "(" else "]"
                            e = s.index(close, k)
                            vals = [x.strip() for x in s[k + 1:e].split(", ")]
                            if any(x not in a.values for x in vals) or len(vals) < 2:
                                self.fail(f"bad category set {vals}")
                            if " or " in s[k:e] or " and " in s[k:e]:
                                self.fail("category values joined with or/and (row 15)")
                            return Lit(fn, op, tuple(sorted(vals))), e + 1
                        for val in sorted(a.values, key=len, reverse=True):
                            if s.startswith(val, k) and (k + len(val) == len(s) or not s[k + len(val)].isalnum()):
                                return Lit(fn, op, (val,)), k + len(val)
                        if not multi and form == "is not ":
                            continue
                self.fail(f"category literal expected after {fn!r}: {s[j:j + 40]!r}")
        self.fail(f"literal expected at {s[i:i + 50]!r}")

    def parse_item(self, s, i, list_br):
        for lk, lead in (("all", "all of the following hold "), ("any", "any of the following hold ")):
            if s.startswith(lead, i):
                return self._parse_list(s, i + len(lead), lk, 0, list_br)
        m = re.compile(r"at least (\d+) of the following hold ").match(s, i)
        if m:
            return self._parse_list(s, m.end(), "kofn", int(m.group(1)), list_br)
        if s.startswith("either ", i):
            a, j = self.parse_lit(s, i + 7)
            if not s.startswith(" or ", j):
                self.fail("either ... or expected")
            b, j = self.parse_lit(s, j + 4)
            if not s.startswith(", but not both", j):
                self.fail("'either A or B' without 'but not both' (6.1)")
            return Item("xor", (a, b)), j + len(", but not both"), True
        a, j = self.parse_lit(s, i)
        if s.startswith(" or ", j):
            b, j = self.parse_lit(s, j + 4)
            if s.startswith(", or both", j):
                j += len(", or both")
            return Item("or", (a, b)), j, True
        return Item("lit", (a,)), j, False

    def _parse_list(self, s, i, kind, k, list_br):
        if s[i] not in "([":
            self.fail("list members must be set off in brackets")
        close = ")" if s[i] == "(" else "]"
        j = i + 1
        mem = []
        while True:
            l, j = self.parse_lit(s, j)
            mem.append(l)
            if s.startswith("; ", j):
                j += 2
                continue
            if s.startswith(close, j):
                j += 1
                break
            self.fail(f"list member separator expected at {s[j:j + 20]!r}")
        if len(mem) < 2 or (kind == "kofn" and not (2 <= k <= len(mem) - 1)):
            self.fail("bad list")
        return Item(kind, tuple(mem), k), j, False

    def parse_cond(self, s, i, list_br=None):
        items = []
        bare_or = False
        while True:
            it, i, is_or = self.parse_item(s, i, list_br)
            items.append(it)
            bare_or = bare_or or is_or
            if s.startswith(" and ", i):
                i += 5
                continue
            break
        if bare_or and len(items) > 1:
            self.fail("bare 'or' next to other items (6.1)")
        return tuple(items), i

    # ------------------------------------------------------------ rules
    RULE_HEAD = re.compile(r"(?P<noun>Rule|Section|Clause|Provision|Row) (?P<id>\d+)(?: \((?P<tags>[^)]*)\))?: ")

    def parse_rule_text(self, s, i, rid=None, kind_hint=None, gov=None):
        """Parse one rule sentence starting at i (after the 'Noun n (tags): ' head). Returns (Rule, end)."""
        tags = {}
        r = None
        nounpat = r"(?:Rule|Section|Clause|Provision|Row) (\d+)"
        if s.startswith("If ", i):
            items, j = self.parse_cond(s, i + 3)
            m = re.compile(r", " + nounpat + r" is switched off").match(s, j)
            if m:
                tgt = int(m.group(1))
                j = m.end()
                if s.startswith(" and the outcome is ", j):
                    o, j = self._outcome(s, j + len(" and the outcome is "))
                    r = Rule(rid, "oexc", items, None, o, target=tgt)
                else:
                    r = Rule(rid, "pexc", items, None, None, target=tgt)
            elif s.startswith(", the outcome is ", j):
                o, j = self._outcome(s, j + len(", the outcome is "))
                r = Rule(rid, "gen", items, None, o)
            else:
                self.fail(f"rule body: outcome clause expected at {s[j:j + 30]!r}")
            if s.startswith(", unless ", j):
                b, j = self.parse_lit(s, j + len(", unless "))
                r.unless = b
                if any(it.kind in ("or", "xor") for it in items):
                    self.fail("unless next to a bare or (6.1)")
        elif s.startswith("The outcome is ", i):
            k = s.find(" only if ", i)
            if k < 0:
                self.fail("only-if expected")
            o = s[i + len("The outcome is "):k]
            items, j = self.parse_cond(s, k + len(" only if "))
            if s.startswith(", unless", j):
                self.fail("unless in an only-if rule (6.1)")
            r = Rule(rid, "onlyif", items, None, o)
        else:
            m = re.compile(nounpat + r" does not apply if ").match(s, i)
            if not m:
                self.fail(f"unknown rule form at {s[i:i + 40]!r}")
            items, j = self.parse_cond(s, m.end())
            r = Rule(rid, "pexc", items, None, None, target=int(m.group(1)))
        if not s.startswith(".", j):
            self.fail(f"rule must end with '.' at {s[j:j + 20]!r}")
        j += 1
        m = re.compile(r" This (?:rule|section|clause|provision|row) is in force for cases whose (?P<g>.+?) is on or "
                       r"before (?P<d>" + DATE_RE + r")\.").match(s, j)
        if m:
            if gov is not None and m.group("g") != gov:
                self.fail("last-applicable date not written with the governing-date field (6.1)")
            r.last = pdate(m.group("d"))
            j = m.end()
        return r, j

    def _outcome(self, s, j):
        k1 = s.find(", unless ", j)
        k2 = s.find(".", j)
        # an outcome name never holds ', unless ' or '.'
        ends = [x for x in (k1, k2) if x >= 0]
        k = min(ends)
        # a '.' inside a decimal / date cannot occur in an outcome name
        return s[j:k], k

    def apply_tags(self, r: Rule, tags: str | None, tiers):
        if not tags:
            return r
        for t in tags.split("; "):
            m = re.fullmatch(r"exception to (?:Rule|Section|Clause|Provision|Row) (\d+)", t)
            if m:
                if r.kind not in ("pexc", "oexc") or r.target != int(m.group(1)):
                    self.fail("exception tag disagrees with the rule text")
                continue
            m = re.fullmatch(r"(.+) tier", t)
            if m:
                if m.group(1) not in tiers:
                    self.fail(f"unknown tier {m.group(1)!r}")
                r.tier = tiers.index(m.group(1))
                continue
            m = re.fullmatch(r"in force from (" + DATE_RE + r")", t)
            if m:
                r.date = pdate(m.group(1))
                continue
            self.fail(f"unknown rule tag {t!r}")
        return r

    # ------------------------------------------------------------ notices and inert elements
    NOTICE_HEAD = re.compile(r"(?P<N>Notice|Amendment|Bulletin) (?P<n>\d+) from (?P<body>[^()]+?) \(issued (?P<nd>" +
                             DATE_RE + r"); effective (?P<ed>" + DATE_RE + r")\): ")
    DRAFT_HEAD = re.compile(r"Draft proposal from (?P<body>[^()]+?) \(not yet adopted; proposed effective date (?P<ed>" +
                            DATE_RE + r")\): ")
    SCOPE_HEAD = re.compile(r"For cases whose (?P<sn>[^:]+?) is (?P<sv>[^:]+?) only: ")
    COMMENT = re.compile(r"Comment: (?P<t>[^.]+)\.")

    def parse_notice_body(self, s, i, tiers, gov):
        nounpat = r"(?:Rule|Section|Clause|Provision|Row) (\d+)"
        m = re.compile(nounpat + r" is repealed\.").match(s, i)
        if m:
            return ("repeal", int(m.group(1)), None, None), m.end()
        m = re.compile(nounpat + r" is replaced by the following text\. ").match(s, i)
        if m:
            tgt = int(m.group(1))
            h = self.RULE_HEAD.match(s, m.end())
            if not h or int(h.group("id")) != tgt:
                self.fail("replacement text must restate the rule id")
            r, j = self.parse_rule_text(s, h.end(), rid=tgt, gov=gov)
            self.apply_tags(r, h.group("tags"), tiers)
            return ("replace", tgt, r, None), j
        m = re.compile(r"A new (?:rule|section|clause|provision|row) (\d+) is added(?: (at the top|at the bottom|"
                       r"directly below Row (\d+)))?\. ").match(s, i)
        if m:
            nid = int(m.group(1))
            pos = None
            if m.group(2):
                pos = ("top",) if m.group(2) == "at the top" else ("bottom",) if m.group(2) == "at the bottom" else \
                    ("after", int(m.group(3)))
            h = self.RULE_HEAD.match(s, m.end())
            if not h or int(h.group("id")) != nid:
                self.fail("inserted rule must carry its new id")
            r, j = self.parse_rule_text(s, h.end(), rid=nid, gov=gov)
            self.apply_tags(r, h.group("tags"), tiers)
            return ("insert", None, r, pos), j
        self.fail(f"notice body expected at {s[i:i + 40]!r}")

    # ------------------------------------------------------------ main
    def parse(self):
        shown, short = self.find_statements()
        self.shown, self.short = shown, short
        hdr = HEADER_RX.search(self.state_flat)
        if not hdr:
            self.fail("policy header missing")
        body, B, gov = hdr.group("body"), pdate(hdr.group("B")), hdr.group("gov")
        attrs = self.parse_fields()
        if gov not in attrs or attrs[gov].type != "date":
            self.fail("governing-date field not a date field")
        self.setup_lexicon(attrs)
        is_short = "closed" in short
        # policy
        tiers = []
        if 31 in shown:
            tiers = self._tiers(shown[31]["tier_chain"])
        elif "PRIORITY" in short:
            tiers = self._tiers(short["PRIORITY"]["tier_chain"])
        world = "closed"
        if "2a" in shown:
            world = "open"
        elif 3 in shown:
            world = "missing"
        prim = sec = None
        pols = []
        for k, p in ((29, "SPEC"), (30, "LATER"), (31, "PRIORITY"), (32, "ORDER")):
            if k in shown:
                pols.append(p)
        for p in ("SPEC", "LATER", "PRIORITY"):
            if p in short:
                pols.append(p)
        if 33 in shown:
            pn = shown[33]["prim_name"]
            prim = {v: k for k, v in L.POLICY_NAMES.items()}.get(pn)
            ss = shown[33]["sec_sentence"]
            sec = {v: k for k, v in L.SEC_SENTENCES.items()}.get(ss)
            if prim is None or sec is None or set(pols) != {prim, sec}:
                self.fail("tie-breaker statement disagrees with the precedence statements")
        else:
            if len(pols) != 1:
                self.fail(f"one precedence policy expected, found {pols}")
            prim = pols[0]
        tie, strict, esc = "esc", (), None
        if "34s" in shown:
            tie = "strict"
            strict = tuple(x.strip() for x in shown["34s"]["strict_list"].split(", "))
        if "34e" in shown:
            esc = shown["34e"]["escalate"]
        if 38 in shown:
            e2 = shown[38]["escalate"]
            if esc is not None and esc != e2:
                self.fail("two escalate outcomes")
            esc = e2
        default = shown.get(35, {}).get("default") or short.get("default", {}).get("default")
        if default is None:
            self.fail("no default statement")
        fallback = shown.get(7, {}).get("fallback")
        M = shown.get(3, {}).get("M")
        listed = tuple(x.strip() for x in shown[3]["listed"].split(", ")) if 3 in shown else ()
        cbd = shown.get("2cbd", {}).get("cbd") or shown.get(38, {}).get("cbd")
        codes = {c: shown[f"41{c}"][f"code_{c}"] for c in "DTFM" if f"41{c}" in shown}
        none_label = shown.get("43n", {}).get("none")
        # elements: notices, drafts, other-body notices, other-scope rules, comments, base rules, S3 table
        s = self.state_flat
        spans = []
        notices, inert = [], []
        for m in self.NOTICE_HEAD.finditer(s):
            (nt, tgt, r, pos), j = self.parse_notice_body(s, m.end(), tiers, gov)
            n = Notice(int(m.group("n")), nt, tgt, r, pdate(m.group("nd")), pdate(m.group("ed")), pos)
            if m.group("body") == body:
                notices.append(n)
            else:
                inert.append(Inert("other_body", num=n.num, notice=n, body=m.group("body")))
            spans.append((m.start(), j, ("n", n.num) if m.group("body") == body else None))
        for m in self.DRAFT_HEAD.finditer(s):
            (nt, tgt, r, pos), j = self.parse_notice_body(s, m.end(), tiers, gov)
            inert.append(Inert("draft", notice=Notice(None, nt, tgt, r, pdate(m.group("ed")), pdate(m.group("ed"))),
                               body=m.group("body")))
            spans.append((m.start(), j, None))
        for m in self.SCOPE_HEAD.finditer(s):
            r, j = self.parse_rule_text(s, m.end(), rid=0, gov=gov)
            inert.append(Inert("other_scope", rule=r, scope_value=m.group("sv")))
            spans.append((m.start(), j, None))
        for m in self.COMMENT.finditer(s):
            inert.append(Inert("comment", text=m.group("t")))
            spans.append((m.start(), m.end(), None))
        spans.sort()
        # base rules: heads outside the spans above
        rules = []
        order_pos = []
        for m in self.RULE_HEAD.finditer(s):
            if any(a <= m.start() < b for a, b, _ in spans):
                continue
            rid = int(m.group("id"))
            r, j = self.parse_rule_text(s, m.end(), rid=rid, gov=gov)
            self.apply_tags(r, m.group("tags"), tiers)
            rules.append(r)
            order_pos.append((m.start(), ("r", rid)))
        for a, b, tag in spans:
            if tag is not None:
                order_pos.append((a, tag))
        s3_rows = None
        tab = self._find_table()
        if tab is not None:
            rules, s3_rows, oth = self._parse_table(tab, tiers, gov)
            if oth != default:
                self.fail("table 'otherwise' line disagrees with the default statement")
            order_pos = [(i, ("r", rid)) for i, rid in enumerate(s3_rows)] + \
                        [(10 ** 6 + p, t) for p, t in order_pos if t[0] == "n"]
        order_pos.sort()
        order = [t for _, t in order_pos]
        # outcomes of the card
        outcomes = self._outcomes(rules, notices, default, esc, fallback, M, strict)
        if is_short:
            tie = "none"
        policy = Policy(world=world, prim=prim, sec=sec, tie=tie if prim != "ORDER" else "esc", strict=strict,
                        outcomes=tuple(outcomes), roles={}, valence=self.valence, default=default, escalate=esc,
                        fallback=fallback, M=M, gov=gov, body=body, B=B, listed=listed, tiers=tuple(tiers),
                        scope_name=hdr.group("scope_name"), scope_value=hdr.group("scope_value"))
        S = Struct(attrs=attrs, rules=rules, notices=notices, inert=inert, policy=policy, order=order,
                   s3_rows=s3_rows)
        q = self._question()
        self.q = q
        self.none_label = none_label
        cases = self._cases(S, world)
        opts = self._options(q, cbd, codes, none_label)
        self._checks(S, cases, shown, short, is_short)
        return {"S": S, "cases": cases, "q": q, "options": opts, "cbd": cbd, "codes": codes, "none": none_label,
                "shown": shown, "short": short, "is_short": is_short, "injected": list(self.injected)}

    def _tiers(self, chain):
        parts = re.split(r" rules override | rules, which override ", chain)
        parts = [p.strip() for p in parts if p.strip()]
        parts[-1] = re.sub(r" rules$", "", parts[-1])
        out = []
        for p in parts:
            m = re.fullmatch(r"(.+) tier", p)
            if not m:
                self.fail(f"bad tier chain {chain!r}")
            out.append(m.group(1))
        return out

    def _outcomes(self, rules, notices, default, esc, fallback, M, strict):
        names = []
        self.valence = {}
        txt = self.card + "\n" + (self.row.get("instructions") or "")
        for mt in MEANINGS:
            mm = mt.format(subj=self.subj)
            for m in re.finditer(r"(?:^|\n)[ \t]*(?:[-*•+]\s+|\d+\.\s+)?(?:\*\*)?(?P<n>[A-Za-z0-9][A-Za-z0-9' \-]*?)"
                                 r"(?:\*\*)?\s*(?::|=|\||::|→)?\s*\n?\s*" + re.escape(mm) + r"(?:$|\n| \()", txt):
                n = m.group("n").strip()
                if n not in names:
                    names.append(n)
                    self.valence[n] = "good" if mt in GOODM else "bad"
        if self.qtype == "choice" and not names:
            pass
        for o in [default, esc, fallback, M] + list(strict):
            if o and o not in names:
                names.append(o)
        for r in rules + [n.rule for n in notices if n.rule is not None]:
            if r.out and r.out not in names:
                names.append(r.out)
        return names

    # ------------------------------------------------------------ S3 table
    def _find_table(self):
        for t in self.tables:
            cols = [norm(c) for c in t["columns"]]
            if cols and cols[0] == "row" and "outcome" in cols:
                return t
        return None

    def _parse_table(self, t, tiers, gov):
        cols = t["columns"]
        ncol = [norm(c) for c in cols]
        fmap = {norm(n): n for n in self.attrs}
        rules, order, oth = [], [], None
        for row in t["rows"]:
            cells = dict(zip(ncol, row))
            head = row[0]
            out = cells["outcome"]
            if head == "Otherwise":
                oth = out
                continue
            m = re.fullmatch(r"Row (\d+)", head)
            if not m:
                self.fail(f"bad table row head {head!r}")
            rid = int(m.group(1))
            items = []
            for c, v in zip(ncol[1:], row[1:]):
                if c in ("outcome", "tier", "in force from"):
                    continue
                if c not in fmap:
                    self.fail(f"unknown table column {c!r}")
                fn = fmap[c]
                if v == "any":
                    continue
                a = self.attrs[fn]
                if a.type == "bool":
                    if v not in ("yes", "no"):
                        self.fail("bool cell must be yes / no")
                    items.append(Item("lit", (Lit(fn, "is", (v == "yes",)),)))
                    continue
                lit, j = self.parse_lit(f"{fn} {v}", 0)
                if j != len(fn) + 1 + len(v):
                    self.fail(f"table cell not fully read: {v!r}")
                items.append(Item("lit", (lit,)))
            r = Rule(rid, "gen", tuple(items), None, out)
            if "tier" in cells:
                if cells["tier"] not in tiers:
                    self.fail("unknown tier in table")
                r.tier = tiers.index(cells["tier"])
            if "in force from" in cells:
                r.date = pdate(cells["in force from"])
            rules.append(r)
            order.append(rid)
        if oth is None:
            self.fail("table without an 'otherwise' line")
        return rules, order, oth

    # ------------------------------------------------------------ cases
    def _case_regions(self):
        """[(ref, region text)] for the case file(s)."""
        lines = self.lines
        txt = "\n".join(lines)
        out = []
        if self.qtype == "choice" and self.row.get("_q4"):
            pass
        refs = self.row.get("_refs")
        m = re.search(r"Case reference: (?P<ref>[A-Za-z0-9\-]+)\.", txt)
        if m:
            start = m.start()
            out.append((m.group("ref"), self._region(txt, start)))
            return out
        pat = re.compile(r"(?i)" + r"[\s_\-]*".join(re.escape(w) for w in (self.subj + " reference").split()) +
                         r"[\s:|=.\-\"']*(?:is\s+)?(?P<ref>[A-Za-z0-9][A-Za-z0-9\-]*)")
        m = pat.search(txt)
        if m:
            out.append((m.group("ref"), self._region(txt, m.start())))
        return out

    SECTION_WORDS = {norm(x) for x in L.FIELDS_TITLES + L.POSSIBLE_TITLES + L.INTERP_TITLES + L.RULES_TITLES +
                     L.NOTICES_TITLES + ["Decision table", "Revision notices", "Policy notes", "Other correspondence", "Flowchart",
                                     "Revision notes"]}

    def _region(self, txt, start):
        rest = txt[start:]
        lines = rest.split("\n")
        out = []
        for i, l in enumerate(lines):
            if i > 0 and (norm(l) in self.SECTION_WORDS or l.strip().startswith("Issued by ")
                          or re.match(r"\s*(?:[#*=\-]+\s*)?Base policy, effective", l)):
                break
            out.append(l)
        return "\n".join(out)

    def _field_rx(self, name):
        words = re.findall(r"[A-Za-z0-9]+", name)
        return r"(?i)(?<![A-Za-z0-9])" + r"[\s_\-']*".join(re.escape(w) for w in words) + r"(?![A-Za-z0-9])"

    def _read_case(self, S, region, ref, world):
        vals, unknown, notrec = {}, set(), set()
        subj_ref = f"{self.subj[:1].upper() + self.subj[1:]} {ref}"
        flat = ws(region)
        for name, a in S.attrs.items():
            if a.type == "bool":
                t = a.true.replace("{S}", subj_ref)
                t = t[:1].upper() + t[1:]
                f = a.false.replace("{S}", subj_ref) if a.false else None
                f = (f[:1].upper() + f[1:]) if f else None
                got = None
                if re.search(re.escape(t) + r"\.", flat):
                    got = True
                if f and re.search(re.escape(f) + r"\.", flat):
                    if got is not None:
                        self.fail("Boolean stated both ways")
                    got = False
                m = re.search(self._field_rx(name) + r"[\s:|=.\"'\t]*(?:is\s+)?(?P<v>yes|no|not recorded)(?![A-Za-z])",
                              region)
                if m:
                    if got is not None:
                        self.fail("Boolean stated twice")
                    if m.group("v") == "not recorded":
                        self.fail("not recorded on a Boolean field")
                    got = m.group("v") == "yes"
                if got is None:
                    if world == "open":
                        unknown.add(name)
                    else:
                        vals[name] = False
                else:
                    vals[name] = got
                continue
            rx = self._field_rx(name) + r"(?:[\s:|=.\"'\t]*|[\s:|=.\"'\t]*(?:is\s+))(?P<v>"
            if a.type == "num":
                rx += r"not recorded|" + NUM_RE + r")"
            elif a.type == "date":
                rx += r"not recorded|" + DATE_RE + r")"
            else:
                rx += r"not recorded|" + "|".join(re.escape(v) for v in sorted(a.values, key=len, reverse=True)) + r")"
            ms = list(re.finditer(rx, region))
            if not ms:
                if world == "open":
                    unknown.add(name)
                    continue
                self.fail(f"no value for field {name!r}")
            if len({m.group("v") for m in ms}) > 1:
                self.fail(f"field {name!r} has two values")
            v = ms[0].group("v")
            if v == "not recorded":
                notrec.add(name)
                continue
            if a.type == "num":
                vals[name] = pnum(v)
            elif a.type == "date":
                vals[name] = pdate(v)
            else:
                vals[name] = v
        # injected instructions (inert, case file only)
        inj = [x for x in L.INJECTIONS if x in flat]
        return Case(vals, frozenset(unknown), frozenset(notrec), ref), inj

    def _cases(self, S, world):
        if self.q["qtype"] == "Q4":
            txt = "\n".join(self.lines)
            cases = []
            self.injected = []
            heads = [r for r in self.row["options"] if r != self.none_label]
            positions = []
            for r in heads:
                m = re.search(r"(?mi)^[ \t#*>\-•\[=\d.<]*" + re.escape(r) + r"[\]:* \t=>]*$", txt)
                if not m:
                    self.fail(f"case reference heading missing: {r}")
                positions.append((m.start(), r))
            positions.sort()
            for i, (p, r) in enumerate(positions):
                end = positions[i + 1][0] if i + 1 < len(positions) else len(txt)
                c, inj = self._read_case(S, self._region(txt[p:end], 0), r, world)
                cases.append(c)
                self.injected += inj
            return cases
        regs = self._case_regions()
        if len(regs) != 1:
            self.fail(f"one case file expected, found {len(regs)}")
        ref, region = regs[0]
        c, inj = self._read_case(S, region, ref, world)
        self.injected = inj
        return [c]

    # ------------------------------------------------------------ question and options
    def _question(self):
        txt = self.instr
        subj = re.escape(self.subj)
        if self.row["qtype"] == "noul":
            for pol in ("dneg", "neg", "aff"):
                for fr in L.Q3_FRAMES[pol]:
                    rx = re.escape(fr).replace(re.escape("{ref}"), subj + r" (?P<ref>[A-Za-z0-9\-]+)").replace(
                        re.escape("{X}"), r"(?P<X>[A-Za-z0-9' \-]+?)")
                    m = re.search(rx, txt)
                    if m:
                        return {"qtype": "Q3", "pol": pol, "X": m.group("X"), "ref": m.group("ref")}
            self.fail("no yes/no question frame")
        for fr in L.Q4_FRAMES:
            rx = re.escape(fr).replace(re.escape("{X}"), r"(?P<X>[A-Za-z0-9' \-]+?)")
            m = re.search(rx, txt)
            if m:
                return {"qtype": "Q4", "X": m.group("X")}
        for fr in L.Q2_FRAMES:
            rx = re.escape(fr).replace(re.escape("{ref}"), subj + r" (?P<ref>[A-Za-z0-9\-]+)")
            m = re.search(rx, txt)
            if m:
                return {"qtype": "Q2", "ref": m.group("ref")}
        for fr in L.Q1_FRAMES:
            rx = re.escape(fr).replace(re.escape("{ref}"), subj + r" (?P<ref>[A-Za-z0-9\-]+)")
            m = re.search(rx, txt)
            if m:
                return {"qtype": "Q1", "ref": m.group("ref")}
        self.fail("no question frame")

    def _options(self, q, cbd, codes, none_label):
        if q["qtype"] == "Q3":
            return None
        opts = self.row["options"]
        out = []
        if q["qtype"] == "Q1":
            for o in opts:
                out.append("__CBD__" if (cbd is not None and o == cbd) else o)
            return out
        if q["qtype"] == "Q4":
            for o in opts:
                out.append("__NONE__" if (none_label is not None and o == none_label) else o)
            return out
        inv_codes = {v: k for k, v in codes.items()}
        for o in opts:
            if cbd is not None and o == cbd:
                out.append(("__CBD__", None))
                continue
            got = None
            for sep in L.Q2_SEPS:
                m = re.fullmatch(r"(?P<o>.+?)" + re.escape(sep) + r"(?:(?:Rule|Section|Clause|Provision|Row) (?P<rid>\d+)|"
                                 r"(?P<code>code [A-Z]{3}))", o)
                if m:
                    b = int(m.group("rid")) if m.group("rid") else inv_codes.get(m.group("code"))
                    if b is None:
                        self.fail("undefined basis code")
                    got = (m.group("o"), b)
                    break
            if got is None:
                self.fail(f"Q2 option not readable: {o!r}")
            out.append(got)
        return out

    # ------------------------------------------------------------ G3 lints
    def _checks(self, S, cases, shown, short, is_short):
        allt = self.all_text
        for rx in BANNED_RX:
            m = rx.search(allt)
            if m:
                self.fail(f"banned construct (6.1): {m.group(0)!r}")
        # statements in the state are never imperatives to the reader (6.4 rule 4)
        for k, d in shown.items():
            if d.get("_where") == "state":
                for v in L.STATEMENTS[k]:
                    if v.startswith(IMPERATIVE_STARTS):
                        self.fail("imperative construct statement in the state")
        for rx in XF06_BANNED:
            m = re.search(rx, self.state_flat)
            if m and S.policy.world != "missing":
                self.fail(f"XF06 marker in the state: {m.group(0)!r}")
        if S.policy.world == "open":
            for t in self.tables:
                pass
        # R9: every construct used is on the card
        used = set()
        rlist = list(S.rules) + [n.rule for n in S.notices if n.rule is not None]
        for r in rlist:
            for it in r.all_items():
                if it.kind == "not":
                    used.add("unless")
                elif it.kind in ("or", "xor", "all", "any", "kofn"):
                    used.add(it.kind)
                for m in it.mem:
                    a = S.attrs[m.attr]
                    if a.type == "num":
                        used.add("num_" + m.op)
                    elif a.type == "date":
                        used.add("date_" + m.op)
                    elif a.type == "cat":
                        used.add("cat")
            if r.kind in ("pexc", "oexc"):
                used.add("exc")
            if r.kind == "onlyif":
                used.add("onlyif")
            if r.last is not None:
                used.add("last")
        if S.notices:
            used.add("notices")
            for n in S.notices:
                used.add(n.ntype)
        if S.inert:
            used.add("inert")
        need = {"num_ge": [8], "num_le": [9], "num_gt": [10], "num_lt": [11], "num_between": [12],
                "num_within": [18], "cat": [15], "or": [13], "xor": ["13x"], "all": [14], "any": [14],
                "kofn": [14], "unless": [6], "onlyif": [7], "exc": [26], "notices": [19, 20, 21, 42],
                "replace": [22], "insert": [23], "repeal": [24], "last": [19, 24], "inert": [25, 42]}
        for u in used:
            if u.startswith("date_"):
                rows = [16]
            else:
                rows = need.get(u, [])
            if is_short:
                continue
            for r in rows:
                if r not in shown and not (r == 25 and "25n" in shown):
                    self.fail(f"construct {u} used without its card statement (row {r}; R9)")
        if is_short:
            bad = used & {"unless", "onlyif", "xor", "all", "any", "kofn", "num_between", "num_within", "replace",
                          "last", "inert", "date_fromto", "oexc"}
            if bad:
                self.fail(f"construct outside the plain subset (6.2): {sorted(bad)}")
            if "insert" in used and "insert" not in short:
                self.fail("insert notice without its statement (6.2)")
            if "repeal" in used and "repeal" not in short:
                self.fail("repeal notice without its statement (6.2)")
        # R8: presupposition (case constraint and render rule)
        for c in cases:
            for k, a in S.attrs.items():
                if a.type == "bool" and a.presup and a.presup in S.attrs:
                    q = a.presup
                    q_true = c.vals.get(q) is True
                    if (c.vals.get(k) is True or k in c.unknown) and not q_true:
                        self.fail("R8 case constraint")
        # R10 (a): names and true phrasings carry no negation (checked by the caller with negcount)
        return True


def vocab_for(pack: dict, attrs_by_name: dict | None = None) -> dict:
    """The pack's declared vocabulary the parser may use: subject noun and Boolean phrasings (by field name)."""
    bools = {}
    names = {}
    for a in pack["attrs"]:
        names[a["key"]] = a["name"]
    for a in pack["attrs"]:
        if a["type"] == "bool":
            bools[a["name"]] = {"true": a["true"], "false": a.get("false"),
                                "presup": names.get(a.get("presup")) if a.get("presup") else None}
    return {"subject": pack["subject"]["noun"], "bools": bools, "affixed": pack.get("affixed", [])}
