"""Question parser (1.6 question parse): the question sentence -> query AST, from the 1.2 keyword grammar (closed
comparator list, closed time grammar, line phrases, negation forms). Reads only the question and the handed
parameters (formats, units, legend, term names, column names from the parsed containers)."""
from __future__ import annotations

import re

from f9fmt import DATE_RE, TIME_RE, num_regex, parse_dt
from f9lex import CMP_T10, CMP_T35
from f9parse import QP, fail, ParseError

ID = r"[A-Z]{2,3}-\d{4}"
COMP = r"[A-Z]{2}-\d{2}"


def _cap(s):
    return s[:1].upper() + s[1:]


class QParser:
    def __init__(self, qp: QP, ctx):
        """ctx: {"sampler", "terms": set, "levels": [...], "item_cols": QP for list items, "dim": set(cols),
        "fact": set(cols)}"""
        self.qp = qp
        self.ctx = ctx

    # ------------------------------------------------------------------------------------------------ entry
    def parse(self, text):
        scope = False
        m = re.match(r"^Among the listed ([a-z][a-z ]*?), (.*)$", text)
        if m:
            scope = True
            text = _cap(m.group(2))
        if not text.endswith("?"):
            fail("question mark")
        body = text[:-1]
        q = self.question(body)
        if scope:
            self._set_scope(q)
        return q

    def _set_scope(self, q):
        b = q
        while b["op"] in ("not", "thr"):
            b = b["inner"]
        b["_scope"] = True

    def question(self, b):
        m = re.match(r"^Is it not the case that (.+)$", b)
        if m:
            return {"op": "not", "inner": self.claim(m.group(1)), "_neg": "itnc"}
        m = re.match(r"^Is there no (.+)$", b)
        if m:
            return {"op": "not", "inner": self.exists_like(m.group(1)), "_neg": "there_no"}
        m = re.match(r"^Is there (?:a|an) (.+)$", b)
        if m:
            return self.exists_like(m.group(1))
        m = re.match(rf"^Does request ({ID}) have no ([A-Z]+) line$", b)
        if m:
            return {"op": "not", "inner": {"op": "req_any", "req": m.group(1),
                                           "a": self.level_atom(m.group(2), "=")}, "_neg": "have_no"}
        m = re.match(rf"^Does request ({ID}) have (.+)$", b)
        if m:
            return {"op": "req_any", "req": m.group(1), "a": self.line_sg(m.group(2))}
        m = re.match(rf"^Does ({ID}) (not count|count) as (.+)$", b)
        if m:
            return self.term_lookup(m.group(1), m.group(3), m.group(2) == "not count")
        m = re.match(rf"^Does ({ID}) have (any|no) (.+)$", b)
        if m:
            return self.has_any(m.group(1), m.group(2), m.group(3))
        m = re.match(r"^Is every (.+?) also one (whose .+)$", b)
        if m:
            return self.forall(m.group(1), m.group(2))
        m = re.match(rf"^Is every (.+?) of ({ID}) one (whose .+)$", b)
        if m:
            return self.quant_every(m.group(1), m.group(2), m.group(3))
        m = re.match(r"^Is (.+)$", b)
        if m:
            return self.is_claim(m.group(1))
        return self.choice_q(b)

    # ------------------------------------------------------------------------------------------------ claims
    def claim(self, c):
        m = re.match(r"^there is no (.+)$", c)
        if m:
            return {"op": "not", "inner": self.exists_like(m.group(1)), "_neg": "there_no"}
        m = re.match(r"^there is (?:a|an) (.+)$", c)
        if m:
            return self.exists_like(m.group(1))
        m = re.match(rf"^request ({ID}) has no ([A-Z]+) line$", c)
        if m:
            return {"op": "not", "inner": {"op": "req_any", "req": m.group(1),
                                           "a": self.level_atom(m.group(2), "=")}, "_neg": "have_no"}
        m = re.match(rf"^request ({ID}) has (.+)$", c)
        if m:
            return {"op": "req_any", "req": m.group(1), "a": self.line_sg(m.group(2))}
        m = re.match(rf"^({ID}) (does not count|counts) as (.+)$", c)
        if m:
            return self.term_lookup(m.group(1), m.group(3), m.group(2) == "does not count")
        m = re.match(rf"^({ID}) has (any|no) (.+)$", c)
        if m:
            return self.has_any(m.group(1), m.group(2), m.group(3))
        m = re.match(r"^every (.+?) is also one (whose .+)$", c)
        if m:
            return self.forall(m.group(1), m.group(2))
        m = re.match(rf"^every (.+?) of ({ID}) is one (whose .+)$", c)
        if m:
            return self.quant_every(m.group(1), m.group(2), m.group(3))
        # '<head> is <tail>': try each ' is ' split, right to left
        idx = [mm.start() for mm in re.finditer(" is ", c)]
        errs = []
        for i in reversed(idx):
            try:
                return self.is_claim(c[:i] + " " + c[i + 4:], split=(i, c[:i], c[i + 4:]))
            except ParseError as e:
                errs.append(str(e))
        fail("claim: " + (errs[0] if errs else "no form"))

    def is_claim(self, body, split=None):
        """body = '<head> <tail>' (the question 'Is <head> <tail>?'); split = (i, head, tail) from a claim."""
        cands = []
        if split:
            cands = [(split[1], split[2])]
        else:
            words = body.split(" ")
            for i in range(len(words) - 1, 0, -1):
                cands.append((" ".join(words[:i]), " ".join(words[i:])))
        errs = []
        for head, tail in cands:
            try:
                return self.head_tail(head, tail)
            except ParseError as e:
                errs.append(str(e))
        fail("is-claim: " + (errs[-1] if errs else ""))

    def head_tail(self, head, tail):
        # compare (T35): '<group a> <cmp35> <group b>' with the group b inside tail
        for ph, op in sorted(CMP_T35.items(), key=lambda kv: -len(kv[0])):
            if tail.startswith(ph + " the "):
                ga = self.group(head)
                gb = self.group(tail[len(ph) + 1:])
                if ga[0] != gb[0] or ga[1] != gb[1]:
                    fail("compare groups differ in kind")
                return {"op": "compare", "agg": ga[0], "col": ga[1], "a": ga[2], "b": gb[2], "cmp": op}
        m = re.fullmatch(rf"the ([a-z_.]+) of ({ID}) in (Week \d+)", head)
        if m:
            op, v, u, ph = self.qp.cmp_phrase(tail, True, None)
            return {"op": "thr", "inner": {"op": "cell", "ent": m.group(2), "period": m.group(3)}, "cmp": op,
                    "lit": v, "unit": u}
        m = re.fullmatch(rf"the ([a-z_.]+) of ({ID})", head)
        if m:
            col, rid = m.group(1), m.group(2)
            a = self.qp.atom(f"{col} is {tail}")
            return {"op": "lookup_p", "id": rid, "p": a}
        m = re.fullmatch(r"the number of (.+)", head)
        if m:
            op, v, _, ph = self.qp.cmp_phrase(tail, False)
            return {"op": "thr", "inner": self.count_head(m.group(1)), "cmp": op, "lit": v}
        m = re.fullmatch(r"the average ([a-z_.]+) of the ([a-z][a-z ]*?) (whose .+)", head)
        if m:
            col = m.group(1)
            op, v, u, ph = self.qp.cmp_phrase(tail, True, col)
            return {"op": "thr", "inner": {"op": "mean", "col": col, "f": self.qp.pred(m.group(3))}, "cmp": op,
                    "lit": v, "unit": u}
        m = re.fullmatch(rf"the total ([a-z_.]+) of the ([a-z][a-z ]*?) of ({ID})(?: (whose .+))?", head)
        if m:
            col = m.group(1)
            op, v, u, ph = self.qp.cmp_phrase(tail, True, col)
            fe = self.qp.pred(m.group(4)) if m.group(4) else None
            return {"op": "thr", "inner": {"op": "ent_sum", "key": m.group(3), "col": col, "fe": fe}, "cmp": op,
                    "lit": v, "unit": u}
        fail("head")

    def count_head(self, s):
        """after 'the number of ': '<Rs> whose P' | '<evs> of the <ents> whose P' | '<line pl> logged[ W]'."""
        if self.ctx["sampler"] == "S6":
            m = re.fullmatch(r"(.+?) logged(?: (.+))?", s)
            if not m:
                fail("lines head")
            return {"op": "count_lines", "f": self.lfilter(self.line_pl(m.group(1)), m.group(2))}
        if self.ctx["sampler"] == "S3":
            m = re.fullmatch(r"([a-z][a-z ]*?) of the ([a-z][a-z ]*?) (whose .+)", s)
            if not m:
                fail("group count head")
            return {"op": "g_count", "fd": self.qp.pred(m.group(3)), "fe": None}
        m = re.fullmatch(r"([a-z][a-z ]*?) (whose .+)", s)
        if not m:
            fail("count head")
        return {"op": "count", "f": self.qp.pred(m.group(2))}

    def group(self, s):
        m = re.fullmatch(r"the number of ([a-z][a-z ]*?) (whose .+)", s)
        if m:
            return ("count", None, self.qp.pred(m.group(2)))
        m = re.fullmatch(r"the (total|average) ([a-z_.]+) of the ([a-z][a-z ]*?) (whose .+)", s)
        if m:
            return ("sum" if m.group(1) == "total" else "mean", m.group(2), self.qp.pred(m.group(4)))
        fail("group")

    def exists_like(self, s):
        if self.ctx["sampler"] == "S6":
            m = re.fullmatch(r"(.+?) logged(?: (.+))?", s)
            if not m:
                fail("exists lines")
            return {"op": "exists_lines", "f": self.lfilter(self.line_bare(m.group(1)), m.group(2))}
        m = re.fullmatch(r"([a-z][a-z ]*?) that counts as (.+)", s)
        if m:
            t = m.group(2)
            if t not in self.ctx["terms"]:
                fail("unknown term")
            return {"op": "exists", "f": {"k": "term", "name": t}}
        m = re.fullmatch(rf"([a-z][a-z ]*?) with ([a-z_]+) ({ID})", s)
        if m:
            return {"op": "presence", "id": m.group(3)}
        m = re.fullmatch(r"([a-z][a-z ]*?) (whose .+)", s)
        if m:
            return {"op": "exists", "f": self.qp.pred(m.group(2))}
        fail("exists")

    def term_lookup(self, rid, t, neg):
        if t not in self.ctx["terms"]:
            fail("unknown term")
        a = {"k": "term", "name": t}
        return {"op": "lookup_p", "id": rid, "p": {"k": "not", "arg": a} if neg else a}

    def has_any(self, rid, qk, rest):
        if self.ctx["sampler"] == "S3":
            if qk != "any":
                fail("S3 'no' form")
            m = re.fullmatch(r"([a-z][a-z ]*?) (whose .+)", rest)
            return {"op": "ent_any", "key": rid, "fe": self.qp.pred(m.group(2))}
        m = re.fullmatch(r"([a-z][a-z ]*?) (whose .+)", rest)
        if not m:
            fail("has any")
        lst = self.ctx["list"]
        return {"op": "quant_lookup", "id": rid, "q": qk, "list": lst, "cond": self.ctx["item_qp"].pred(m.group(2))}

    def quant_every(self, item, rid, rest):
        return {"op": "quant_lookup", "id": rid, "q": "every", "list": self.ctx["list"],
                "cond": self.ctx["item_qp"].pred(rest)}

    def forall(self, recs, rest):
        m = re.fullmatch(r"([a-z][a-z ]*?) (whose .+)", recs)
        if not m:
            fail("forall")
        return {"op": "forall", "a": self.qp.pred(m.group(2)), "b": self.qp.pred(rest)}

    # ------------------------------------------------------------------------------------------------ S6 phrases
    def level_atom(self, lv, op):
        if lv not in self.ctx["levels"]:
            fail("level not on the card")
        return {"k": "line", "level": lv, "lvl_op": op}

    def _line(self, s, plural):
        a = {"k": "line"}
        m = re.fullmatch(rf"(.*?)(?: from ({COMP}))?", s)
        core, comp = m.group(1), m.group(2)
        if plural:
            mm = re.fullmatch(r"lines at ([A-Z]+) or higher", core)
            if mm:
                a.update(self.level_atom(mm.group(1), ">="))
            elif core == "lines":
                pass
            else:
                mm = re.fullmatch(r"([A-Z]+) lines", core)
                if not mm:
                    fail("line phrase")
                a.update(self.level_atom(mm.group(1), "="))
        else:
            mm = re.fullmatch(r"line at ([A-Z]+) or higher", core)
            if mm:
                a.update(self.level_atom(mm.group(1), ">="))
            elif core == "line":
                pass
            else:
                mm = re.fullmatch(r"([A-Z]+) line", core)
                if not mm:
                    fail("line phrase")
                a.update(self.level_atom(mm.group(1), "="))
        if comp:
            a["comp"] = comp
        if len(a) == 1:
            fail("empty line phrase")
        return a

    def line_bare(self, s):
        return self._line(s, False)

    def line_sg(self, s):
        m = re.fullmatch(r"(?:a|an) (.+)", s)
        if not m:
            fail("article")
        return self._line(m.group(1), False)

    def line_pl(self, s):
        return self._line(s, True)

    def lfilter(self, line, w):
        if not w:
            return line
        typ = "dt"
        win = {"k": "win", "col": "time", **self.qp.time_phrase(w, typ)}
        return {"k": "and", "args": [line, win]}

    def lift(self, s):
        parts = s.split(" and ")
        aa = []
        for p in parts:
            m = re.fullmatch(r"no ([A-Z]+) line", p)
            if m:
                aa.append({"k": "not", "arg": {"k": "lift", "a": self.level_atom(m.group(1), "=")}})
                continue
            aa.append({"k": "lift", "a": self.line_sg(p)})
        if any(a["k"] == "not" for a in aa[:-1]):
            fail("negated lift before an unnegated operand")
        return aa[0] if len(aa) == 1 else {"k": "and", "args": aa}

    # ------------------------------------------------------------------------------------------------ choice
    def choice_q(self, b):
        qp = self.qp
        s = self.ctx["sampler"]
        m = re.fullmatch(r"How many ([a-z][a-z ]*?) are there (whose .+)", b)
        if m:
            return {"op": "count", "f": qp.pred(m.group(2))}
        m = re.fullmatch(r"How many ([a-z][a-z ]*?) count as (.+)", b)
        if m:
            return {"op": "count", "f": self._term(m.group(2))}
        m = re.fullmatch(r"How many different ([a-z_.]+) values do the ([a-z][a-z ]*?) (whose .+) have", b)
        if m:
            return {"op": "cdist", "col": m.group(1), "f": qp.pred(m.group(3))}
        m = re.fullmatch(r"How many ([a-z][a-z ]*?) belong to the ([a-z][a-z ]*?) (whose .+)", b)
        if m:
            return {"op": "g_count", "fd": qp.pred(m.group(3)), "fe": None}
        m = re.fullmatch(r"How many (.+?) were logged(?: (.+))?", b)
        if m and s == "S6":
            return {"op": "count_lines", "f": self.lfilter(self.line_pl(m.group(1)), m.group(2))}
        m = re.fullmatch(r"How many ([a-z][a-z ]*?) have a ([a-z_.]+) of (.+) in (Week \d+)", b)
        if m:
            op, v, u, ph = qp.cmp_phrase(m.group(3), True, None)
            return {"op": "col_count", "period": m.group(4), "cmp": op, "lit": v}
        m = re.fullmatch(r"In (\S+), what is the total ([a-z_.]+) of (" + ID + r") over all periods", b)
        if m:
            return {"op": "row_total", "ent": m.group(3)}
        m = re.fullmatch(rf"In (\S+), what is the total ([a-z_.]+) of the ([a-z][a-z ]*?) of ({ID})(?: (whose .+))?", b)
        if m:
            self._unit(m.group(1), m.group(2))
            return {"op": "ent_sum", "key": m.group(4), "col": m.group(2),
                    "fe": qp.pred(m.group(5)) if m.group(5) else None}
        m = re.fullmatch(r"In (\S+), what is the (total|average|highest|lowest) ([a-z_.]+) of the ([a-z][a-z ]*?) "
                         r"(whose .+)", b)
        if m:
            self._unit(m.group(1), m.group(3))
            op = {"total": "sum", "average": "mean", "highest": "max", "lowest": "min"}[m.group(2)]
            return {"op": op, "col": m.group(3), "f": qp.pred(m.group(5))}
        m = re.fullmatch(r"What is the (earliest|latest) ([a-z_.]+) of the ([a-z][a-z ]*?) (whose .+)", b)
        if m:
            return {"op": "min" if m.group(1) == "earliest" else "max", "col": m.group(2), "f": qp.pred(m.group(4))}
        m = re.fullmatch(rf"(?:In (\S+), w|W)hat is the ([a-z_.]+) of ({ID})", b)
        if m:
            col = m.group(2)
            if m.group(1):
                self._unit(m.group(1), col)
            elif qp.cols.get(col, {}).get("type") == "num":
                fail("value pick for an amount without its unit")
            if s == "S3":
                return {"op": "ent_attr", "key": m.group(3), "col": col}
            return {"op": "lookup", "id": m.group(3), "col": col}
        m = re.fullmatch(r"At what time was the (first|last) (.+?) logged(?: (.+))?", b)
        if m:
            return {"op": m.group(1), "f": self.lfilter(self.line_bare(m.group(2)), m.group(3))}
        m = re.fullmatch(r"Which of these ([a-z][a-z ]*?) is one (whose .+)", b)
        if m:
            return {"op": "cpick", "f": qp.pred(m.group(2))}
        m = re.fullmatch(r"Which of these ([a-z][a-z ]*?) counts as (.+)", b)
        if m:
            return {"op": "cpick", "f": self._term(m.group(2))}
        m = re.fullmatch(r"Which of these ([a-z][a-z ]*?) has any ([a-z][a-z ]*?) (whose .+)", b)
        if m:
            return {"op": "cpick", "f": {"k": "has", "fe": self.ctx["fact_qp"].pred(m.group(3))}}
        m = re.fullmatch(r"Which of these requests has (.+)", b)
        if m:
            return {"op": "cpick", "f": self.lift(m.group(1))}
        m = re.fullmatch(r"Which requests have (.+)", b)
        if m:
            return {"op": "select", "f": self.lift(m.group(1))}
        m = re.fullmatch(r"Which ([a-z][a-z ]*?) are the ones (whose .+)", b)
        if m:
            return {"op": "select", "f": qp.pred(m.group(2))}
        m = re.fullmatch(r"Which ([a-z][a-z ]*?) have any ([a-z][a-z ]*?) (whose .+)", b)
        if m:
            return {"op": "select", "f": {"k": "has", "fe": self.ctx["fact_qp"].pred(m.group(3))}}
        m = re.fullmatch(r"Which ([a-z][a-z ]*?) count as (.+)", b)
        if m:
            return {"op": "select", "f": self._term(m.group(2))}
        m = re.fullmatch(r"Which ([a-z][a-z ]*?) (whose .+) has the (highest|lowest|earliest|latest) ([a-z_.]+)", b)
        if m:
            return {"op": "argmax" if m.group(3) in ("highest", "latest") else "argmin", "col": m.group(4),
                    "f": qp.pred(m.group(2))}
        m = re.fullmatch(r"Which ([a-z][a-z ]*?) has the most ([a-z][a-z ]*?)(?: (whose .+))?", b)
        if m and s == "S3":
            fe = self.ctx["fact_qp"].pred(m.group(3)) if m.group(3) else None
            return {"op": "g_argmax", "agg": "count", "col": None, "fe": fe, "fd": None, "dir": "max"}
        m = re.fullmatch(r"Which ([a-z][a-z ]*?) has the highest total ([a-z_.]+) over its ([a-z][a-z ]*?)"
                         r"(?: (whose .+))?", b)
        if m:
            fe = self.ctx["fact_qp"].pred(m.group(4)) if m.group(4) else None
            return {"op": "g_argmax", "agg": "sum", "col": m.group(2), "fe": fe, "fd": None, "dir": "max"}
        m = re.fullmatch(r"Which ([a-z][a-z ]*?) logged the most (.+?)(?: ((?:on|from) .+))?", b)
        if m and s == "S6":
            return {"op": "comp_argmax", "f": self.lfilter(self.line_pl(m.group(2)), m.group(3))}
        m = re.fullmatch(r"Which ([a-z][a-z ]*?) has the (highest|lowest) total ([a-z_.]+)", b)
        if m and s == "S5":
            return {"op": "row_top", "dir": "max" if m.group(2) == "highest" else "min"}
        fail("no question form")

    def _term(self, t):
        if t not in self.ctx["terms"]:
            fail("unknown term")
        return {"k": "term", "name": t}

    def _unit(self, u, col):
        c = self.qp.cols.get(col)
        if c is None:
            fail("unknown column")
        cu = c.get("unit")
        if cu is None:
            return
        if u != cu and f"{u}->{cu}" not in self.qp.card.get("conv", {}) and f"{cu}->{u}" not in self.qp.card.get(
                "conv", {}):
            fail("answer unit not stated")
