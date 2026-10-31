"""F11 card renders (G0 section 2 'Card (rendered)', section 7 grammar, section 10 canonical statements).

A Card holds the hidden taxonomy plus every surface choice fixed per card (IDs, names, report noun, card form,
statements used, examples, worked items). card_ir() builds the fmt1 card IR for one render ('base', 'masked',
'swapped') and one row route (yes/no: whole card; choice rows on one-line cards: offered codes as option lines).
"""
from __future__ import annotations

import datetime as dt
from fractions import Fraction

import lex
from tax import PRES

CMP_SETS = {"ge": lex.CMP_GE, "lt": lex.CMP_LT}


def fmt_num(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    s = f"{float(x):.6f}".rstrip("0").rstrip(".")
    return s


def fmt_date(d: dt.date) -> str:
    return d.isoformat()


def unit_form(a, x) -> str:
    return a.unit[0] if x == 1 else a.unit[1]


class Card:
    def __init__(self, **kw):
        self.__dict__.update(kw)

    # -------------------------------------------------------------- wording helpers
    @property
    def fill(self) -> dict:
        return {"report": self.report, "reports": self.reports, "entity": self.entity, "entities": self.entities,
                "event": self.event}

    def code_label(self, k, form) -> str:
        """Option / reference text of code k in a label form: code | masked -> ID; name -> name; swapped -> word."""
        if form in ("code", "masked"):
            return self.ids[k]
        if form == "swapped":
            return self.swapped[k]
        return self.names[k]

    # -------------------------------------------------------------- condition text (section 7 COND)
    def cond_text(self, aid, allowed, *, cmp_pick=0) -> list[str]:
        """One COND set as PART strings (a numeric or date range may need two parts)."""
        a = self.attrs[self.ai[aid]]
        s = sorted(allowed)
        if a.kind == "nom":
            vs = [a.values[i] for i in s]
            return [f"{a.name} is {vs[0]}"] if len(vs) == 1 else [f"{a.name} is one of {', '.join(vs)}"]
        if a.kind == "pres":
            return [f"{a.name} {'present' if s == [PRES] else 'absent'}"]
        lo, hi = s[0], s[-1]
        out = []
        if a.kind == "num":
            if lo > 0:
                c = a.cuts[lo - 1]
                out.append(f"{a.name} {self.cmp_word('ge', aid, cmp_pick)} {fmt_num(c)} {unit_form(a, c)}")
            if hi < a.n - 1:
                c = a.cuts[hi]
                out.append(f"{a.name} {self.cmp_word('lt', aid, cmp_pick)} {fmt_num(c)} {unit_form(a, c)}")
        else:
            if lo > 0:
                out.append(f"{a.name} {lex.DCMP_GE} {fmt_date(a.cuts[lo - 1])}")
            if hi < a.n - 1:
                out.append(f"{a.name} {lex.DCMP_LT} {fmt_date(a.cuts[hi])}")
        return out

    def cmp_word(self, kind, aid, pick=0):
        return self.cmp_forms.get((kind, aid), CMP_SETS[kind][0])

    def cell_text(self, aid, allowed) -> str:
        """Table cell (SEM-48)."""
        a = self.attrs[self.ai[aid]]
        if allowed is None or len(allowed) == a.n:
            return "any"
        s = sorted(allowed)
        if a.kind == "nom":
            return ", ".join(a.values[i] for i in s)
        if a.kind == "pres":
            return "present" if s == [PRES] else "absent"
        if a.kind == "num":
            return ", ".join(self.band_text(a, b) for b in s)
        lo, hi = s[0], s[-1]
        parts = []
        if lo > 0:
            parts.append(f"{lex.DCMP_GE} {fmt_date(a.cuts[lo - 1])}")
        if hi < a.n - 1:
            parts.append(f"{lex.DCMP_LT} {fmt_date(a.cuts[hi])}")
        return "; ".join(parts)

    def band_text(self, a, b) -> str:
        lo, hi = a.band_range(b)
        if lo is None:
            return f"under {fmt_num(hi)} {unit_form(a, hi)}"
        if hi is None:
            return f"{fmt_num(lo)} {unit_form(a, lo)} or more"
        return f"{fmt_num(lo)} to under {fmt_num(hi)} {unit_form(a, hi)}"

    def parts_text(self, k) -> list[str]:
        c = self.tax.codes[k]
        out = []
        for aid, s in c.parts(self.attrs):
            out += self.cond_text(aid, s)
        return out

    def mark_text(self, k) -> str:
        return f" {lex.MARK_FMT.format(mark=self.mark)}" if self.tax.codes[k].mark else ""

    def body(self, k, ref, mark=True) -> str:
        """The code's one-line entry after its 'ID NAME:' head (CODE / UNLESS / ONLY_IF; SEM-14, SEM-15)."""
        c = self.tax.codes[k]
        parts = "; ".join(self.parts_text(k))
        mt = self.mark_text(k) if mark else ""
        if c.rule is None:
            return parts + mt
        cond = " and ".join(self.cond_text(*c.rule["cond"]))
        t = ref(c.rule["target"])
        if c.rule["kind"] == "unless":
            s = f"{parts}, unless {cond}. If both {parts} and {cond} hold, use {t}."
        else:
            s = f"{parts}. Use {ref(k)} only if {cond} also holds. If {parts} holds but {cond} does not, use {t}."
        return s + mt

    def rule_sentence(self, k, ref) -> str:
        """Table cards: the unless / only-if written under the table (RULE_SENT)."""
        return f"{ref(k)}: {self.body(k, ref, mark=False)}"

    # -------------------------------------------------------------- glossary (SEM-43)
    def glossary_lines(self) -> list[str]:
        out = []
        for a in self.attrs:
            if a.kind == "nom":
                vs = []
                for i, v in enumerate(a.values):
                    ts = a.terms.get(i, [])
                    q = " or ".join(f"'{t}'" for t in ts)
                    vs.append(f"{v} (shown by {q})")
                out.append(f"{lex.GLOSSARY_LEAD} {a.name}: " + "; ".join(vs) + ".")
            elif a.kind == "pres":
                q = " or ".join(f"'{t}'" for t in a.terms["attr"])
                out.append(f"{a.name} (shown by {q}): present or absent.")
            elif a.kind == "num":
                q = " or ".join(f"'{t}'" for t in a.terms["attr"])
                out.append(f"{a.name} (shown by {q}) in {a.unit[0]}/{a.unit[1]}.")
            else:
                q = " or ".join(f"'{t}'" for t in a.terms["attr"])
                out.append(f"{a.name} (shown by {q}) is the date of the {a.event}.")
        return out

    # -------------------------------------------------------------- reading rules
    def reading_rules(self, render) -> list[str]:
        f = self.fill
        R = []
        if self.form == "short":
            R.append(lex.SEM["SEM-01"].format(**f))
            if not self.is_s7:
                R.append(lex.SEM["SEM-02"].format(**f))
                R.append(lex.SEM["SEM-06-SHORT"].format(kinds=self.kinds_text(), **f))
                R.append(lex.SEM["SEM-07"].format(**f))
                R.append(lex.SEM["SEM-43-SHORT"])
            R.append(lex.SEM["SEM-10"])
            R.append(lex.SEM["SEM-38"].format(**f))
            return R
        R.append(lex.SEM["SEM-01"].format(**f))
        R.append(lex.SEM["SEM-02"].format(**f))
        R.append(lex.SEM["SEM-10-S6" if self.shape == "list" else "SEM-10"])
        if self.shape == "list":
            R.append(lex.SEM["SEM-11"].format(**f))
        R.append(lex.SEM["SEM-16"])
        R.append(lex.SEM["SEM-38"].format(**f))
        R.append(lex.SEM["SEM-43"])
        R.append(lex.SEM["SEM-06"].format(kinds=self.kinds_text(), **f))
        R.append(lex.SEM["SEM-07"].format(**f))
        if self.shape == "box" and (self.tax.notes or any(c.rule for c in self.tax.codes)):
            s = lex.SEM["SEM-12"].format(**f)
            if self.tax.notes:
                s += " " + lex.SEM["SEM-12-NOTES"]
            R.append(s)
            if any(c.rule and c.rule["kind"] == "onlyif" for c in self.tax.codes):
                R.append(lex.SEM["SEM-15"])
        if any(a.kind == "nom" for a in self.attrs):
            R.append(lex.SEM["SEM-19"])
        if any(a.kind == "num" for a in self.attrs):
            R.append(lex.SEM["SEM-20"])
            R.append(lex.SEM["SEM-24"])
        if any(a.kind == "date" for a in self.attrs):
            R.append(lex.SEM["SEM-27"])
        pres = [a for a in self.attrs if a.kind == "pres"]
        if pres:
            cues = ", ".join(f"'{c.format(X='<term>')}'" for c in self.cues_used)
            R.append(lex.SEM["SEM-05"].format(cues=cues) + " " +
                     " ".join(lex.SEM["SEM-05-X"].format(X=a.name, **f) for a in pres))
        if self.shape == "group":
            R.append(lex.SEM["SEM-31"].format(**f))
            R.append(lex.SEM["SEM-33-S3"].format(**f))
        if self.shape == "key":
            R.append(lex.SEM["SEM-33-S5"].format(**f))
        if self.form == "table":
            R.append(lex.SEM["SEM-48"])
            if any(a.kind == "num" for a in self.attrs):
                R.append(lex.SEM["SEM-22"])
        if self.form == "rubric":
            R.append(lex.SEM["SEM-48-S6"].format(**f))
        if self.records:
            s = lex.SEM["SEM-50"]
            if self.log_lines:
                s += " " + lex.SEM["SEM-50-LOG"]
            R.append(s)
            for i, a in enumerate(self.attrs):
                R.append(lex.FIELD_LINE.format(attr=a.name, field=self.fields[i]))
        if render == "masked":
            R.append(lex.SEM["SEM-36"])
        elif self.name_rows or render == "swapped":
            R.append(lex.SEM["SEM-35"])
        if self.examples or self.worked:
            R.append(lex.SEM["SEM-37"])
        if any(c.mark for c in self.tax.codes):
            R.append(lex.SEM["SEM-52"].format(marks=lex.MARK_FMT.format(mark=self.mark),
                                              actions=lex.MARK_ACTIONS[self.mark]))
        return R

    def kinds_text(self) -> str:
        f = self.fill
        parts = []
        k = self.frame_kinds
        if "HEDGED" in k:
            parts.append("hedged (" + ", ".join(f"'{h}'" for h in self.hedges_used) + ")")
        if "HYPO" in k:
            parts.append("hypothetical ('hypothetically')")
        if "LATER" in k:
            parts.append(f"about a later or future {f['event']}")
        if "GENERIC" in k:
            parts.append(f"a general statement about all {f['entities']}")
        if "OTHER" in k:
            parts.append(f"about another {f['entity']}")
        if "PRIOR" in k:
            parts.append(f"about an earlier {f['event']}")
        if len(parts) == 1:
            return parts[0]
        return ", ".join(parts[:-1]) + ", or " + parts[-1]

    # -------------------------------------------------------------- code-list blocks
    def head(self, k, render) -> str:
        if render == "masked":
            return self.ids[k]
        nm = self.swapped[k] if render == "swapped" else self.names[k]
        return f"{self.ids[k]} {nm}"

    def code_blocks(self, render, route=None) -> list[dict]:
        """route (choice rows on one-line cards): {'offered': {k: option text}, 'other': {k: bracket label|None}}."""
        ref = lambda k: self.ids[k]  # noqa: E731  inside a full card a code is always referred to by its ID
        if self.form == "oneline":
            entries = []
            for k in self.order:
                if route and k in route["offered"]:
                    other = route["other"].get(k)
                    pre = f"({other}) " if other else ""
                    entries.append({"name": route["offered"][k], "text": pre + self.body(k, ref)})
                else:
                    entries.append({"name": self.head(k, render), "text": self.body(k, ref)})
            return [{"type": "section", "heading": lex.CODE_LIST_HEADING,
                     "blocks": [{"type": "defs", "variant": self.dv, "entries": entries}]}]
        if self.form == "table":
            cols = ["Code"] + ([] if render == "masked" else ["Name"]) + [a.name for a in self.attrs]
            rows = []
            for k in self.order:
                c = self.tax.codes[k]
                row = [self.ids[k]] + ([] if render == "masked" else
                                       [self.swapped[k] if render == "swapped" else self.names[k]])
                row += [self.cell_text(a.aid, c.box.get(a.aid)) for a in self.attrs]
                rows.append(row)
            bl = [{"type": "table", "columns": cols, "rows": rows, "caption": None}]
            marks = [self.ids[k] for k in self.order if self.tax.codes[k].mark]
            items = []
            if marks:
                items.append(f"Marked {lex.MARK_FMT.format(mark=self.mark)}: " + ", ".join(marks) + ".")
            items += [self.rule_sentence(k, ref) for k in self.order if self.tax.codes[k].rule]
            if items:
                bl.append({"type": "items", "items": items})
            return [{"type": "section", "heading": lex.CODE_LIST_HEADING, "blocks": bl}]
        if self.form == "group":
            return self.group_blocks(render, ref)
        if self.form == "list":
            return self.list_blocks(render)
        if self.form == "key":
            return self.key_blocks(render)
        if self.form == "short":
            return self.short_blocks()
        raise ValueError(self.form)

    def group_blocks(self, render, ref) -> list[dict]:
        t = self.tax
        g_attr = t.attrs[t.ai[t.gattr]]
        bl = []
        for gi in self.group_order:
            g = t.groups[gi]
            vals = ", ".join(g_attr.values[i] for i in sorted(g["vals"]))
            mk = ""
            if all(t.codes[k].mark for k in g["leaves"]):
                mk = " " + lex.MARK_FMT.format(mark=self.mark)
            items = [f"Group {self.gnames[gi]} ({g_attr.name}: {vals}){mk}"]
            for sn in t.scope_notes:
                if sn["src"] == gi:
                    cond = " and ".join(self.cond_text(*sn["cond"]))
                    items.append(f"Reports that would be in {self.gnames[sn['src']]} but meet {cond} belong to "
                                 f"{self.gnames[sn['dst']]} instead.")
            for k in self.leaf_order[gi]:
                items.append(f"{self.head(k, render)}: {'; '.join(self.parts_text(k))}")
            if g["residual"] is not None:
                k = g["residual"]
                items.append(f"{self.head(k, render)}: use only when the {self.report} belongs to "
                             f"{self.gnames[gi]} and no other {self.gnames[gi]} code fits.")
            bl.append({"type": "items", "items": items})
        return [{"type": "section", "heading": lex.CODE_LIST_HEADING, "blocks": bl}]

    def list_blocks(self, render) -> list[dict]:
        t = self.tax
        steps = []
        for conds, k in t.entries:
            ps = []
            for aid, s in conds:
                ps += self.cond_text(aid, s)
            steps.append(f"If {'; '.join(ps)} -> {self.ids[k]}")
        steps.append(f"Otherwise -> {self.ids[t.catch]}")
        bl = [{"type": "defs", "variant": self.dv_list, "entries": [{"text": s} for s in steps]}]
        if render != "masked":
            leg = [f"{self.ids[k]}: {self.swapped[k] if render == 'swapped' else self.names[k]}" +
                   (" " + lex.MARK_FMT.format(mark=self.mark) if t.codes[k].mark else "") for k in self.order]
        else:
            leg = [f"{self.ids[k]}" + (" " + lex.MARK_FMT.format(mark=self.mark) if t.codes[k].mark else "")
                   for k in self.order if t.codes[k].mark]
            leg = ([f"Marked {lex.MARK_FMT.format(mark=self.mark)}: " +
                    ", ".join(self.ids[k] for k in self.order if t.codes[k].mark) + "."] if leg else [])
        if leg:
            bl.append({"type": "items", "items": leg})
        return [{"type": "section", "heading": lex.CODE_LIST_HEADING, "blocks": bl}]

    def key_blocks(self, render) -> list[dict]:
        t = self.tax
        lines = []
        for n in sorted(t.couplets):
            cp = t.couplets[n]
            ref = lambda x: (str(x[1]) if x[0] == "n" else self.ids[x[1]])  # noqa: E731
            cond = " and ".join(self.cond_text(*cp["cond"]))
            if cp.get("group") is not None:
                lines.append(f"{n}. {self.gnames[cp['group']]}")
            lines.append(f"{n}a {cond} -> {ref(cp['a'])}")
            lines.append(f"{n}b otherwise -> {ref(cp['b'])}")
        bl = [{"type": "items", "items": lines}]
        if render != "masked":
            leg = [f"{self.ids[k]}: {self.swapped[k] if render == 'swapped' else self.names[k]}" +
                   (" " + lex.MARK_FMT.format(mark=self.mark) if t.codes[k].mark else "") for k in self.order]
            bl.append({"type": "items", "items": leg})
        return [{"type": "section", "heading": lex.CODE_LIST_HEADING, "blocks": bl}]

    def short_blocks(self) -> list[dict]:
        names = ", ".join(a.name for a in self.attrs)
        items = [f"Names give {names} in that order."]
        items += [self.names[k] + (" " + lex.MARK_FMT.format(mark=self.mark) if self.tax.codes[k].mark else "")
                  for k in self.order]
        return [{"type": "section", "heading": lex.CODE_LIST_HEADING, "blocks": [{"type": "items", "items": items}]}]

    # -------------------------------------------------------------- whole card IR
    def card_ir(self, render="base", route=None) -> dict:
        blocks = [{"type": "section", "heading": "Reading rules",
                   "blocks": [{"type": "items", "items": self.reading_rules(render)}]}]
        if self.form != "short":
            blocks.append({"type": "section", "heading": "Glossary",
                           "blocks": [{"type": "items", "items": self.glossary_lines()}]})
        blocks += self.code_blocks(render, route)
        notes = []
        ref = lambda k: self.ids[k]  # noqa: E731
        for w, l in self.tax.notes:
            a, b = (w, l) if self.note_order.get((w, l), 0) == 0 else (l, w)
            notes.append(f"If both {ref(a)} and {ref(b)} fit, use {ref(w)}.")
        if self.tax.default is not None:
            a = self.attrs[self.ai[self.tax.default[0]]]
            v0 = a.values[self.tax.default[1]] if a.kind in ("nom", "pres") else None
            s = lex.SEM["SEM-03"].format(A=a.name, V0=v0, **self.fill)
            if self.cue_sentences:
                s += " " + lex.SEM["SEM-03-CUE"].format(A=a.name)
            notes.append(s)
        if notes:
            blocks.append({"type": "section", "heading": "Notes", "blocks": [{"type": "items", "items": notes}]})
        if self.examples:
            blocks.append({"type": "section", "heading": "Examples",
                           "blocks": [{"type": "items", "items": [f"Example of {self.ids[k]}: {txt}"
                                                                  for k, txt in self.examples]}]})
        if self.worked:
            blocks.append({"type": "fewshot", "template": self.ft, "heading": None,
                           "examples": [{"case": txt, "answer": self.ids[k], "note": None} for k, txt in self.worked]})
        return {"blocks": blocks}
