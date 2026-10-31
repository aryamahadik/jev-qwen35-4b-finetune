"""Definition illustrations (6.3 one-line + 1-2 examples; 6.4 rule 5) and few-shot worked cases (1.1; Q3 cards).

Illustrations: a marked hypothetical ("For example,") with hypothetical rules H1 / H2 over fields from the card's
reserved illustration sub-pool (no row of the card draws them) and neutral outcome letters, never a card outcome name,
rule id or notice number. Each is a mini structure labelled by solver A, parsed back (parse_illustration) and re-solved
by solver B; drawn once per card (fixed on every row of the card).
Worked cases: a small sibling structure of the card (3 rules, 4 fields, no notices), labelled by solver A, parsed back
and checked by solver B; shown in the Q3 card's few-shot block.
"""
from __future__ import annotations

import re
from decimal import Decimal

import lexicon as L
import solver_a as A
import solver_b as SB
from common import fmt_date, fmt_num, rng_for
from model import Attr, Case, Item, Lit, Policy, Rule, Struct

LETTERS = ["P", "Q", "R", "S"]
DEFAULT_LETTER = "Z"
ILLUS_ROWS = (5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 26, 28, 29, 30, 31, 35)


class IllusFail(Exception):
    pass


def _attr_from_pack(a, key, window):
    if a["type"] == "num":
        return Attr(key=key, name=a["name"], type="num", unit=a["unit"], places=a["places"], step=Decimal(a["step"]),
                    lo=Decimal(a["lo"]), hi=Decimal(a["hi"]), money=a.get("money", False))
    if a["type"] == "date":
        return Attr(key=key, name=a["name"], type="date", lo=window[0], hi=window[1])
    if a["type"] == "cat":
        return Attr(key=key, name=a["name"], type="cat", values=tuple(a["values"]))
    return Attr(key=key, name=a["name"], type="bool", true=a["true"], false=a.get("false"))


class Mini:
    """Text forms for illustrations (the card's operator forms, neutral letters, hypothetical rules H1 / H2)."""

    def __init__(self, card, attrs):
        self.card = card
        self.f = card["forms"]
        self.A = attrs

    def val(self, a, v):
        if a.type == "num":
            s = fmt_num(v, a.places)
            return s + ("" if a.unit == "%" else " ") + a.unit if a.unit else s
        if a.type == "date":
            return fmt_date(v, self.f["date_form"])
        if a.type == "bool":
            return "yes" if v else "no"
        return v

    def lit(self, m):
        a = self.A[m.attr]
        f = self.f
        if a.type == "bool":
            t = a.true if m.args[0] else a.false
            return t.replace("{S}", "the case")
        if a.type == "num":
            if m.op == "between":
                return f"{a.name} {f['num_between']} {self.val(a, m.args[0])} and {self.val(a, m.args[1])}"
            return f"{a.name} {f['num_' + m.op]} {self.val(a, m.args[0])}"
        if a.type == "date":
            return f"{a.name} {f['date_' + m.op]} {self.val(a, m.args[0])}"
        lb, rb = f["cat_br"]
        if len(m.args) == 1:
            return f"{a.name} {'is' if m.op == 'in' else 'is not'} {m.args[0]}"
        return f"{a.name} {'is one of' if m.op == 'in' else 'is not one of'} {lb}{', '.join(m.args)}{rb}"

    def item(self, it):
        if it.kind == "lit":
            return self.lit(it.mem[0])
        if it.kind == "or":
            return f"{self.lit(it.mem[0])} or {self.lit(it.mem[1])}"
        lb, rb = self.f["list_br"]
        lead = L.LIST_LEAD[it.kind].format(k=it.k)
        return f"{lead} {lb}{'; '.join(self.lit(m) for m in it.mem)}{rb}"

    def rule(self, r, tiers):
        tags = []
        if r.tier is not None:
            tags.append(f"{tiers[r.tier]} tier")
        if r.date is not None:
            tags.append(f"in force from {fmt_date(r.date, self.f['date_form'])}")
        head = f"H{r.rid}" + (f" ({'; '.join(tags)})" if tags else "")
        C = " and ".join(self.item(it) for it in r.items)
        if r.kind == "gen":
            body = f"if {C}, the outcome is {r.out}"
        else:
            body = f"if {C}, H{r.target} is switched off"
        if r.unless is not None:
            body += f", unless {self.lit(r.unless)}"
        return f"{head}: {body}"

    def text(self, rules, case_vals, claim, tiers):
        rs = " and ".join(f"'{self.rule(r, tiers)}'" for r in rules)
        facts = []
        for k, v in case_vals.items():
            a = self.A[k]
            facts.append(f"whose {a.name} is {self.val(a, v)}")
        fl = ", ".join(facts[:-1]) + (" and " if len(facts) > 1 else "") + facts[-1]
        return (f"{L.ILLUS_MARK} under the hypothetical rule{'s' if len(rules) > 1 else ''} {rs}, with "
                f"{DEFAULT_LETTER} when no rule applies, a case {fl} gets {claim}.")


def _mini_struct(attrs, rules, prim, tiers, B):
    pol = Policy(world="closed", prim=prim, sec=None, tie="esc", strict=(), outcomes=tuple(LETTERS + [DEFAULT_LETTER]),
                 roles={}, valence={}, default=DEFAULT_LETTER, escalate="E", fallback=None, M=None, gov="g", body="",
                 B=B, tiers=tuple(tiers))
    at = dict(attrs)
    at["g"] = Attr(key="g", name="g", type="date", lo=B, hi=B + 1000, role="gov")
    return Struct(attrs=at, rules=rules, notices=[], inert=[], policy=pol, order=[("r", r.rid) for r in rules])


def make_illustrations(card, pack, rows_shown, n_per=1, max_rows=3):
    """{str(row): [text, ...]} for the card's illustratable policy rows. Raises IllusFail if a pick cannot be made."""
    rng = rng_for("illus", card["card_id"])
    pa = {a["key"]: a for a in pack["attrs"]}
    res = [pa[k] for k in card["illus_keys"] if k in pa]
    num = next((a for a in res if a["type"] == "num"), None)
    cat = next((a for a in res if a["type"] == "cat"), None)
    boo = next((a for a in res if a["type"] == "bool"), None)
    dat = next((a for a in res if a["type"] == "date"), None)
    out = {}
    checks = []
    if num is None:
        return out, checks
    attrs = {"n": _attr_from_pack(num, "n", card["window"])}
    if cat:
        attrs["c"] = _attr_from_pack(cat, "c", card["window"])
    if boo:
        attrs["b"] = _attr_from_pack(boo, "b", card["window"])
    if dat:
        attrs["d"] = _attr_from_pack(dat, "d", card["window"])
    mini = Mini(card, attrs)
    an = attrs["n"]
    span = int((an.hi - an.lo) / an.step)
    tiers = card["tiers"] or ["upper", "lower"]
    B = card["B"]
    picks = [r for r in rows_shown if r in ILLUS_ROWS]
    rng.shuffle(picks)
    picks = set(picks[:max_rows])
    for row in rows_shown:
        if row not in picks:
            continue
        exs = []
        for t in range(n_per):
            T = an.lo + an.step * rng.randint(max(1, span // 4), max(2, span * 3 // 4))
            prim = card["prim"] if card["prim"] in ("SPEC", "LATER", "PRIORITY") else "SPEC"
            rules, vals = None, None
            if row in (8, 9, 10, 11):
                op = {8: "ge", 9: "le", 10: "gt", 11: "lt"}[row]
                rules = [Rule(1, "gen", (Item("lit", (Lit("n", op, (T,)),)),), None, "P")]
                vals = {"n": T}
            elif row == 12:
                U = T + an.step * rng.randint(2, 6)
                if U > an.hi:
                    continue
                rules = [Rule(1, "gen", (Item("lit", (Lit("n", "between", (T, U)),)),), None, "P")]
                vals = {"n": rng.choice([T, U])}
            elif row in (5, 35):
                rules = [Rule(1, "gen", (Item("lit", (Lit("n", "ge", (T,)),)),), None, "P")]
                vals = {"n": T + an.step if row == 5 else T - an.step}
            elif row == 15 and cat:
                vs = list(attrs["c"].values)
                pick = tuple(sorted(rng.sample(vs, 2)))
                rules = [Rule(1, "gen", (Item("lit", (Lit("c", "in", pick),)),), None, "P")]
                vals = {"c": rng.choice(vs)}
            elif row == 16 and dat:
                d0 = B + rng.randint(20, 200)
                op = rng.choice([o for o in ("before", "onbefore", "after", "onafter") if "date_" + o in card["forms"]])
                rules = [Rule(1, "gen", (Item("lit", (Lit("d", op, (d0,)),)),), None, "P")]
                vals = {"d": d0}
            elif row == 6 and boo:
                rules = [Rule(1, "gen", (Item("lit", (Lit("n", "ge", (T,)),)),), Lit("b", "is", (True,)), "P")]
                vals = {"n": T, "b": rng.random() < 0.5}
            elif row == 13 and boo:
                rules = [Rule(1, "gen", (Item("or", (Lit("n", "ge", (T,)), Lit("b", "is", (True,)))),), None, "P")]
                vals = {"n": T + an.step, "b": True}
            elif row == 14 and boo and cat:
                vs = list(attrs["c"].values)
                mem = (Lit("n", "ge", (T,)), Lit("b", "is", (True,)), Lit("c", "in", (vs[0],)))
                rules = [Rule(1, "gen", (Item("kofn", mem, 2),), None, "P")]
                vals = {"n": T, "b": False, "c": rng.choice(vs)}
            elif row == 26 and boo:
                rules = [Rule(1, "gen", (Item("lit", (Lit("n", "ge", (T,)),)),), None, "P"),
                         Rule(2, "pexc", (Item("lit", (Lit("b", "is", (True,)),)),), None, None, target=1)]
                vals = {"n": T + an.step, "b": rng.random() < 0.6}
            elif row == 28:
                rules = [Rule(1, "gen", (Item("lit", (Lit("n", "ge", (T,)),)),), None, "P"),
                         Rule(2, "gen", (Item("lit", (Lit("n", "le", (T + an.step * 3,)),)),), None, "P")]
                vals = {"n": T + an.step}
                prim = "SPEC"
            elif row == 29 and boo:
                rules = [Rule(1, "gen", (Item("lit", (Lit("n", "ge", (T,)),)),), None, "P"),
                         Rule(2, "gen", (Item("lit", (Lit("n", "ge", (T,)),)), Item("lit", (Lit("b", "is", (True,)),))),
                              None, "Q")]
                vals = {"n": T, "b": True}
                prim = "SPEC"
            elif row == 30:
                rules = [Rule(1, "gen", (Item("lit", (Lit("n", "ge", (T,)),)),), None, "P", date=B - 90),
                         Rule(2, "gen", (Item("lit", (Lit("n", "le", (T + an.step * 4,)),)),), None, "Q",
                              date=B - rng.choice([10, 30, 60]))]
                vals = {"n": T + an.step}
                prim = "LATER"
            elif row == 31 and len(tiers) >= 2:
                rules = [Rule(1, "gen", (Item("lit", (Lit("n", "ge", (T,)),)),), None, "P", tier=1),
                         Rule(2, "gen", (Item("lit", (Lit("n", "le", (T + an.step * 4,)),)),), None, "Q", tier=0)]
                vals = {"n": T + an.step}
                prim = "PRIORITY"
            if rules is None:
                continue
            used = {m.attr for r in rules for it in r.all_items() for m in it.mem}
            attrs_used = {k: attrs[k] for k in sorted(used)}
            S = _mini_struct(attrs_used, rules, prim, tiers, B)
            v = dict(vals)
            v["g"] = B + 30
            try:
                r = A.solve_closed(S, v)
            except A.Reject:
                continue
            claim = r["final"]
            vals_shown = {k: vals[k] for k in vals}
            txt = mini.text(rules, vals_shown, claim, tiers)
            exs.append(txt)
            checks.append((txt, attrs_used, prim, tiers, claim, rules, vals_shown))
        if exs:
            out[str(row)] = exs
    return out, checks


# ---------------------------------------------------------------- illustration parse (G3 side)

ILL_RX = re.compile(r"For example, under the hypothetical rules? (?P<rules>.+?), with Z when no rule applies, a case "
                    r"(?P<facts>.+?) gets (?P<claim>[A-Z])\.")


def parse_illustration(text, attrs_decl, card_forms_parser, tiers):
    """Parse one illustration with the row parser's literal grammar. Returns (rules, vals, claim)."""
    m = ILL_RX.fullmatch(text)
    if not m:
        raise IllusFail("illustration form")
    P = card_forms_parser
    rules = []
    for rm in re.finditer(r"'H(?P<id>\d+)(?: \((?P<tags>[^)]*)\))?: if (?P<body>.+?)'(?= and 'H|$)", m.group("rules")):
        body = rm.group("body")
        items, j = P.parse_cond(body, 0)
        rest = body[j:]
        unless = None
        mm = re.match(r", the outcome is (?P<o>[A-Z])(?:, unless (?P<u>.+))?$", rest)
        r = None
        if mm:
            r = Rule(int(rm.group("id")), "gen", items, None, mm.group("o"))
            if mm.group("u"):
                u, k = P.parse_lit(mm.group("u"), 0)
                r.unless = u
        else:
            mm = re.match(r", H(?P<t>\d+) is switched off(?:, unless (?P<u>.+))?$", rest)
            if not mm:
                raise IllusFail("illustration rule body")
            r = Rule(int(rm.group("id")), "pexc", items, None, None, target=int(mm.group("t")))
            if mm.group("u"):
                u, k = P.parse_lit(mm.group("u"), 0)
                r.unless = u
        if rm.group("tags"):
            for t in rm.group("tags").split("; "):
                if t.endswith(" tier"):
                    r.tier = tiers.index(t[:-5])
                elif t.startswith("in force from "):
                    from parse_f1 import pdate
                    r.date = pdate(t[len("in force from "):])
        rules.append(r)
    facts = {}
    from parse_f1 import pdate, pnum
    s = m.group("facts")
    names = sorted(attrs_decl, key=len, reverse=True)
    i = 0
    while i < len(s):
        for sep in ("whose ", ", whose ", " and whose "):
            if s.startswith(sep, i):
                i += len(sep)
                break
        else:
            raise IllusFail("illustration facts")
        name = next((n for n in names if s.startswith(n + " is ", i)), None)
        if name is None:
            raise IllusFail("illustration fact field")
        i += len(name) + 4
        ends = [k for k in (s.find(", whose ", i), s.find(" and whose ", i)) if k >= 0]
        j = min(ends) if ends else len(s)
        vs = s[i:j]
        a = attrs_decl[name]
        if a.type == "num":
            facts[name] = pnum(vs.split(" ")[0].rstrip("%"))
        elif a.type == "date":
            facts[name] = pdate(vs)
        elif a.type == "bool":
            facts[name] = vs == "yes"
        else:
            facts[name] = vs
        i = j
    return rules, facts, m.group("claim")


def check_illustration(text, card, pack, parser_factory):
    """G3 for one illustration: parse it back and re-solve with solver B; the stated letter must match."""
    decl = {}
    for a in pack["attrs"]:
        if a["key"] in card["illus_keys"]:
            decl[a["name"]] = _attr_from_pack(a, a["name"], card["window"])
    P = parser_factory(decl)
    tiers = card["tiers"] or ["upper", "lower"]
    rules, facts, claim = parse_illustration(text, decl, P, tiers)
    m = ILL_RX.fullmatch(text)
    used = {mm.attr for r in rules for it in r.all_items() for mm in it.mem}
    attrs = {k: decl[k] for k in used}
    prim = "LATER" if any(r.date is not None for r in rules) else "PRIORITY" if any(r.tier is not None for r in rules) \
        else "SPEC"
    S = _mini_struct(attrs, rules, prim, tiers, card["B"])
    v = dict(facts)
    v["g"] = card["B"] + 30
    got = SB.closed(S, v)["final"]
    if got != claim:
        raise IllusFail(f"illustration claim {claim} != solver B {got}")
    return True


# ---------------------------------------------------------------- few-shot worked cases (Q3 cards)

FEWSHOT_TEMPLATES = ["FT01", "FT02", "FT03", "FT04", "FT05", "FT08", "FT09", "FT11", "FT12", "FT14", "FT15", "FT16"]
WC_RX = re.compile(r"Worked case\. Rules: (?P<rules>.+?) When no rule applies, the outcome is (?P<default>[^.]+?)\. "
                   r"Facts: (?P<facts>.+?)\. Question: is the final outcome (?P<X>[^?]+?)\?")


def make_worked_cases(card, pack, n=None):
    """1-3 sibling structures drawn once for the card: (case text, 'Yes' / 'No', structure) each."""
    import copy
    import samplers as SM
    from render_f1 import Fmt
    rng = rng_for("fewshot", card["card_id"])
    c2 = dict(card)
    c2["constructs"] = {x for x in card["constructs"] if x not in ("notices", "replace", "repeal", "insert", "inert",
                                                                   "last", "onlyif", "exc", "exc2", "pexc_short")}
    c2["world"] = "closed"
    c2["listed_keys"] = []
    n = n or rng.randint(1, 3)
    out = []
    tries = 0
    while len(out) < n and tries < 300:
        tries += 1
        try:
            S = SM.draw_struct(c2, pack, rng, sampler="S1", n_rules=3)
            S.attrs = {k: a for k, a in S.attrs.items() if a.role == "gov" or a.type != "date" or
                       any(m.attr == k for r in S.rules for it in r.all_items() for m in it.mem)}
            S.notices, S.inert = [], []
            S.policy.world = "closed"
            S.policy.listed = ()
            S.attrs = {k: a for k, a in S.attrs.items() if a.role != "distractor"}
            case = SM.draw_case(S, c2, rng, ref="")
            r = A.solve(S, case)
            X = rng.choice(card["outcomes"])
            ans = A.q3_answer(r, X, "aff")
            if ans is None:
                continue
            want_yes = len([1 for o in out if o[1] == "Yes"]) < (len(out) + 1) / 2
            if (ans == 1) != want_yes and tries < 200:
                continue
            fm = Fmt(card, S)
            rules_txt = " ".join(fm.rule(rr) for rr in S.rules)
            facts = []
            for k, a in sorted(S.attrs.items()):
                v = case.vals[k]
                facts.append(f"the {a.name} is {fm.val(a, v)}")
            txt = (f"Worked case. Rules: {rules_txt} When no rule applies, the outcome is "
                   f"{card['display'][card['default']]}. Facts: {'; '.join(facts)}. Question: is the final outcome "
                   f"{card['display'][X]}?")
            out.append((txt, "Yes" if ans == 1 else "No", (S, case, X)))
        except (A.Reject, SM.DrawFail, KeyError, ValueError, IndexError):
            continue
    return out


def check_worked_case(text, answer, card, pack):
    """G3 for a worked case: parse its rules and facts back and re-solve with solver B (the card's policy)."""
    import parse_f1 as PF
    from model import Attr as _A
    decl = {}
    for a in pack["attrs"]:
        decl[a["name"]] = _attr_from_pack(a, a["name"], card["window"])
    m = WC_RX.fullmatch(text)
    if not m:
        raise IllusFail("worked case form")
    P = PF.Parser.__new__(PF.Parser)
    P.subj = card["subj"]
    P.problems = []
    P.setup_lexicon({k: a for k, a in decl.items()})
    rs = m.group("rules")
    rules = []
    i = 0
    while i < len(rs):
        h = PF.Parser.RULE_HEAD.match(rs, i)
        if not h:
            raise IllusFail("worked case rule head")
        r, j = P.parse_rule_text(rs, h.end(), rid=int(h.group("id")))
        P.apply_tags(r, h.group("tags"), card["tiers"])
        rules.append(r)
        i = j + (1 if rs[j:j + 1] == " " else 0)
    facts = {}
    for part in m.group("facts").split("; "):
        mm = re.fullmatch(r"the (?P<f>.+?) is (?P<v>.+)", part)
        name = next((n for n in sorted(decl, key=len, reverse=True) if part.startswith(f"the {n} is ")), None)
        if name is None:
            raise IllusFail("worked case fact")
        vs = part[len(f"the {name} is "):]
        a = decl[name]
        if a.type == "num":
            facts[name] = PF.pnum(vs.split(" ")[0].rstrip("%"))
        elif a.type == "date":
            facts[name] = PF.pdate(vs)
        elif a.type == "bool":
            facts[name] = vs == "yes"
        else:
            facts[name] = vs
    used = {mm_.attr for r in rules for it in r.all_items() for mm_ in it.mem}
    gov = next((n for n, a in decl.items() if a.type == "date" and n in facts and n not in used), None)
    attrs = {k: decl[k] for k in facts}
    disp = card["display"]
    pol = Policy(world="closed", prim=card["prim"], sec=card["sec"], tie=card["tie"] if card["tie"] != "none" else "esc",
                 strict=tuple(disp[x] for x in card["strict"]), outcomes=tuple(disp[x] for x in card["outcomes"]),
                 roles={}, valence={}, default=m.group("default"), escalate=disp[card["escalate"]],
                 fallback=None, M=None, gov=gov or "g", body="", B=card["B"], tiers=tuple(card["tiers"]))
    if gov is None:
        attrs["g"] = _A(key="g", name="g", type="date", lo=card["B"], hi=card["B"] + 1000)
        facts["g"] = card["B"] + 30
    S = Struct(attrs=attrs, rules=rules, notices=[], inert=[], policy=pol, order=[("r", r.rid) for r in rules])
    fin = SB.closed(S, facts)["final"]
    got = "Yes" if fin == m.group("X") else "No"
    if got != answer:
        raise IllusFail(f"worked case answer {answer} != solver B {got}")
    return True
