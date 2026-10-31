"""F1 renderer: canonical structure + card -> Doc IR / card IR -> fmt1 row text (6.4 placement, A16.1 g).

Q3 rows: the whole card (construct statements in the card's definition style, outcome meanings, few-shot cases) is the
card field. Choice rows (Q1, Q2, Q4): answer-group statements (+ the outcome list on Q2 / Q4) go to the instructions
through fmt1 render_row_text(qtype='choice'); policy-group statements form the Interpretation section of the policy
document (state); Q1 outcome meanings are '- option: meaning' card lines. Short / no-card rows state everything inside
the policy document (6.2). Every row is rendered by fmt1 card.render_row_text and checked by card.loader_check.
"""
from __future__ import annotations

import random

import lexicon as L
from cards import card_statements
from common import fmt_date, fmt_num, rng_for, unit
from model import Attr, Item, Lit, Rule, Notice, Struct

from fmt1 import card as fcard
from fmt1 import pool as fpool
from fmt1.render import FormatError


class RenderFail(Exception):
    pass


def cap(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s


class Fmt:
    def __init__(self, card, S: Struct):
        self.card = card
        self.S = S
        self.f = card["forms"]
        self.disp = card["display"]

    # values
    def num(self, a: Attr, v):
        s = fmt_num(v, a.places)
        u = a.unit
        if not u:
            return s
        return s + ("" if u == "%" else " ") + u

    def date(self, o):
        return fmt_date(o, self.f["date_form"])

    def val(self, a: Attr, v):
        if a.type == "num":
            return self.num(a, v)
        if a.type == "date":
            return self.date(v)
        if a.type == "cat":
            return v
        if a.type == "bool":
            return L.YES if v else L.NO
        raise ValueError

    def out(self, o):
        return self.disp.get(o, o)

    # literals
    def lit(self, lit: Lit, subj_ref=None):
        a = self.S.attrs[lit.attr]
        subj = subj_ref or f"the {self.card['subj']}"
        if a.type == "bool":
            t = a.true if lit.args[0] else a.false
            if t is None:
                raise RenderFail("no false phrasing")
            return t.replace("{S}", subj)
        f = self.f
        if a.type == "num":
            if lit.op == "between":
                return f"{a.name} {f['num_between']} {self.num(a, lit.args[0])} and {self.num(a, lit.args[1])}"
            if lit.op == "within":
                return f"{a.name} {f['num_within']} {self.num(a, lit.args[0])}"
            return f"{a.name} {f['num_' + lit.op]} {self.num(a, lit.args[0])}"
        if a.type == "date":
            if lit.op == "fromto":
                return f"{a.name} is from {self.date(lit.args[0])} to {self.date(lit.args[1])}"
            return f"{a.name} {f['date_' + lit.op]} {self.date(lit.args[0])}"
        if a.type == "cat":
            lb, rb = f["cat_br"]
            vs = list(lit.args)
            if len(vs) == 1:
                return f"{a.name} {'is' if lit.op == 'in' else 'is not'} {vs[0]}"
            return f"{a.name} {'is one of' if lit.op == 'in' else 'is not one of'} {lb}{', '.join(vs)}{rb}"
        raise ValueError

    def item(self, it: Item, short=False):
        if it.kind == "lit":
            return self.lit(it.mem[0])
        if it.kind == "or":
            a, b = (self.lit(m) for m in it.mem)
            return L.ORBOTH_FRAME.format(a=a, b=b) if short else f"{a} or {b}"
        if it.kind == "xor":
            a, b = (self.lit(m) for m in it.mem)
            return L.XOR_FRAME.format(a=a, b=b)
        if it.kind in ("all", "any", "kofn"):
            lb, rb = self.f["list_br"]
            lead = L.LIST_LEAD[it.kind].format(k=it.k)
            return f"{lead} {lb}{'; '.join(self.lit(m) for m in it.mem)}{rb}"
        raise ValueError(it.kind)

    def cond(self, items, short=False):
        return " and ".join(self.item(it, short) for it in items)

    def rule_ref(self, rid):
        return f"{self.f['rule_noun']} {rid}"

    def rule(self, r: Rule, s3=False, with_id=True):
        card = self.card
        short = card["short"]
        tags = []
        if r.kind in ("pexc", "oexc") and not short:
            tags.append(f"exception to {self.rule_ref(r.target)}")
        if r.tier is not None and card["tiers"]:
            tags.append(L.TIER_TAG.format(tier=card["tiers"][r.tier]))
        if r.date is not None:
            tags.append(L.DATE_TAG.format(D=self.date(r.date)))
        C = self.cond(r.items, short)
        if r.kind == "gen":
            body = L.RULE_FRAMES["gen"].format(C=C, O=self.out(r.out))
        elif r.kind == "oexc":
            body = L.RULE_FRAMES["oexc"].split(": ", 1)[1].format(C=C, T=self.rule_ref(r.target), O=self.out(r.out))
        elif r.kind == "pexc":
            if short:
                body = L.RULE_FRAMES["pexc_short"].format(T=self.rule_ref(r.target), C=C)
            else:
                body = L.RULE_FRAMES["pexc"].split(": ", 1)[1].format(C=C, T=self.rule_ref(r.target))
        elif r.kind == "onlyif":
            body = L.RULE_FRAMES["onlyif"].format(O=self.out(r.out), C=C)
        else:
            raise ValueError
        if r.unless is not None:
            body += L.UNLESS_TAIL.format(B=self.lit(r.unless))
        body = cap(body) + "."
        if r.last is not None:
            body += L.LAST_TAIL.format(noun=self.f["rule_noun"].lower(), gov=self.S.attrs[self.S.policy.gov].name,
                                       D=self.date(r.last))
        head = self.rule_ref(r.rid) if with_id else ""
        if tags:
            head += f" ({'; '.join(tags)})"
        return f"{head}: {body}" if head else body

    def notice(self, n: Notice, body=None, inert_kind=None):
        f = self.f
        nn = f["notice_noun"]
        b = body or self.card["body"]
        if inert_kind == "draft":
            head = L.DRAFT_HEAD.format(body=b, ed=self.date(n.edate))
        else:
            head = L.NOTICE_HEAD.format(N=nn, n=n.num, body=b, nd=self.date(n.ndate), ed=self.date(n.edate))
        if n.ntype == "replace":
            txt = L.NOTICE_BODIES["replace"].format(T=self.rule_ref(n.target), TEXT=self.rule(n.rule))
        elif n.ntype == "repeal":
            txt = L.NOTICE_BODIES["repeal"].format(T=self.rule_ref(n.target))
        else:
            if n.pos is not None:
                p = n.pos
                pos = L.S3_POS[p[0]].format(noun=L.ROW_NOUN, k=p[1] if len(p) > 1 else "")
                txt = L.NOTICE_BODIES["insert_pos"].format(noun=f["rule_noun"].lower(), rid=n.rule.rid, POS=pos,
                                                           TEXT=self.rule(n.rule))
            else:
                txt = L.NOTICE_BODIES["insert"].format(noun=f["rule_noun"].lower(), rid=n.rule.rid,
                                                       TEXT=self.rule(n.rule))
        return f"{head} {txt}"

    def inert(self, e):
        if e.cls == "comment":
            return f"{L.COMMENT_HEAD} {e.text}."
        if e.cls == "other_scope":
            head = L.OTHER_SCOPE_HEAD.format(scope_name=self.card["scope"][0], scope_value=e.scope_value)
            return f"{head} {self.rule(e.rule, with_id=False)}"
        if e.cls == "draft":
            return self.notice(e.notice, body=e.body, inert_kind="draft")
        if e.cls == "other_body":
            return self.notice(e.notice, body=e.body)
        raise ValueError

    # fields block (row 44 lines)
    def field_line(self, a: Attr, open_world=False):
        if a.type == "num":
            lo, hi = self.num(a, a.lo), self.num(a, a.hi)
            u = a.unit or "units"
            if a.places == 0 and a.step == 1:
                return L.FIELD_LINES["num_int"].format(field=a.name, unit=u, lo=lo, hi=hi)
            if a.money and a.places == 2 and str(a.step) in ("0.01",):
                return L.FIELD_LINES["num_cent"].format(field=a.name, unit=u, lo=lo, hi=hi)
            return L.FIELD_LINES["num_step"].format(field=a.name, unit=u, step=fmt_num(a.step, a.places), lo=lo,
                                                    hi=hi)
        if a.type == "date":
            if open_world:
                return L.FIELD_LINES["date_dom"].format(field=a.name, lo=self.date(a.lo), hi=self.date(a.hi))
            return L.FIELD_LINES["date"].format(field=a.name)
        if a.type == "cat":
            lb, rb = self.f["cat_br"]
            return L.FIELD_LINES["cat"].format(field=a.name, vals=f"{lb}{', '.join(a.values)}{rb}")
        return L.FIELD_LINES["bool"].format(field=a.name)

    def fields_items(self):
        ow = self.S.policy.world == "open"
        keys = sorted(self.S.attrs, key=lambda k: (0 if k.startswith("f") else 1, int(k[1:])))
        return [cap(self.field_line(self.S.attrs[k], ow)) for k in keys]

    # case file
    def case_pairs(self, case, include_false=True):
        S = self.S
        out = [(f"{self.card['subj']} reference", case.ref)]
        keys = sorted(S.attrs, key=lambda k: (0 if k.startswith("f") else 1, int(k[1:])))
        for k in keys:
            a = S.attrs[k]
            if k in case.notrec:
                out.append((a.name, L.NOT_RECORDED))
                continue
            if k in case.unknown:
                raise RenderFail("unknown field in a record")
            v = case.vals[k]
            if a.type == "bool" and v is False and not include_false:
                continue  # closed world: a false Boolean key may be left out (row 1)
            out.append((a.name, self.val(a, v)))
        return out

    def case_sentences(self, case, rng, include_false=True, frames=None):
        S = self.S
        ref = case.ref
        subj_ref = f"{cap(self.card['subj'])} {ref}"
        out = [L.CASE_REF_FRAME.format(ref=ref)]
        keys = sorted(S.attrs, key=lambda k: (0 if k.startswith("f") else 1, int(k[1:])))
        for k in keys:
            a = S.attrs[k]
            if k in case.unknown:
                continue
            if k in case.notrec:
                out.append(L.CASE_FRAMES["notrec"].format(field=a.name))
                continue
            v = case.vals[k]
            if a.type == "bool":
                if v:
                    out.append(cap(a.true.replace("{S}", subj_ref)) + ".")
                else:
                    if a.false is None:
                        if S.policy.world != "open":
                            continue  # closed world: an unlisted yes/no fact is false (row 1)
                        raise RenderFail("known-false Boolean needs a row-4 cue")
                    if not include_false:
                        continue
                    out.append(cap(a.false.replace("{S}", subj_ref)) + ".")
                continue
            out.append(L.CASE_FRAMES[a.type].format(field=a.name, value=self.val(a, v)))
        return out


# ---------------------------------------------------------------- card IR

DEF_LABELS = {1: "Closed world", "2a": "Open world", "2cbd": "Undetermined", "2yn": "Yes/no under unknowns",
              3: "Missing fields", 4: "Explicit negatives", 5: "If", 6: "Unless", 7: "Only if", 8: "Inclusive bound",
              9: "Inclusive bound", 10: "Strict bound", 11: "Strict bound", 12: "Between", 13: "Or", "13x": "Either-or",
              14: "Lists", 15: "Categories", 16: "Dates", 18: "Day counts", 19: "Governing date",
              20: "Effective dates", 21: "Same-day notices", 22: "Replacement", "22p": "Replacement tiers",
              23: "Insertion", 24: "Repeal and expiry", 25: "No-effect text", 26: "Exceptions", 27: "Rule order",
              28: "Agreement", 29: "Specificity", 30: "Latest date", 31: "Tiers", 32: "Row order", 33: "Tie-breaker",
              "34e": "Ties", "34s": "Ties", 35: "Default", 36: "Rounding", 37: "Units", 38: "Undetermined vs escalate",
              39: "Question target", 40: "Text in the case", "41h": "Basis", "41D": "Basis D", "41T": "Basis T",
              "41F": "Basis F", "41M": "Basis M", 42: "Notices", 43: "Listed cases", "43n": "If no case qualifies",
              45: "Status words"}


def _dv_for(card, kind):
    """A fmt1 defs variant id for the card's definition style (fixed per card)."""
    if kind == "one_line":
        opts = ["DV01", "DV02", "DV03", "DV05", "DV06"]
    elif kind == "one_line_examples":
        opts = ["DV11", "DV12", "DV13", "DV14", "DV15", "DV16"]
    else:
        opts = ["DV35"]
    return opts[int(unit("dv", card["card_id"], kind) * len(opts))]


def outcome_entries(card):
    ents = []
    for o in card["outcomes"]:
        ents.append({"name": card["display"][o], "text": card["meanings"][o]})
    return ents


def card_ir_q3(card, stmts, illus, fewshot):
    """Q3: the card field holds everything (construct statements in the definition style, meanings, few-shot)."""
    ds = card["defs"]
    blocks = []
    if ds == "decision_list":
        blocks.append({"type": "steps", "items": [t for _, _, t in stmts]})
    else:
        dv = _dv_for(card, ds)
        ents = []
        for r, g, t in stmts:
            e = {"name": DEF_LABELS[r], "text": t}
            if ds == "one_line_examples" and illus.get(str(r)):
                e["examples"] = illus[str(r)]
            ents.append(e)
        # names must be unique in a defs block: suffix duplicates
        seen = {}
        for e in ents:
            n = e["name"]
            seen[n] = seen.get(n, 0) + 1
            if seen[n] > 1:
                e["name"] = f"{n} ({seen[n]})"
        blocks.append({"type": "defs", "variant": dv, "heading": None, "entries": ents})
    blocks.append({"type": "defs", "variant": "DV01", "heading": L.OUTCOME_LIST_HEAD.format(subj=card["subj"]),
                   "entries": outcome_entries(card)})
    if fewshot:
        blocks.append({"type": "fewshot", "template": card["fewshot_template"], "heading": None,
                       "examples": fewshot})
    return {"title": None, "blocks": blocks}


def card_ir_choice(card, stmts):
    """Choice rows: answer-group statements (moved to instructions by fmt1) + outcome meanings (Q1: option lines;
    Q2 / Q4: outcome list moved to instructions)."""
    ans = [(r, t) for r, g, t in stmts if g == "answer"]
    blocks = []
    if ans:
        blocks.append({"type": "items", "items": [t for r, t in ans]})
    if card["qtype"] == "Q1":
        blocks.append({"type": "defs", "variant": "DV01", "heading": None, "entries": outcome_entries(card)})
    elif not card["short"]:
        blocks.append({"type": "defs", "variant": "DV01",
                       "heading": L.OUTCOME_LIST_HEAD.format(subj=card["subj"]), "entries": outcome_entries(card)})
    return {"title": None, "blocks": blocks}


def interp_items(card, stmts, illus):
    """Interpretation section (policy-group statements) for choice cards, in the state."""
    pol = [(r, t) for r, g, t in stmts if g == "policy"]
    if not pol:
        return None
    if card["defs"] == "decision_list":
        return {"type": "steps", "items": [t for _, t in pol]}
    items = []
    for r, t in pol:
        items.append(t)
        if card["defs"] == "one_line_examples":
            for ex in illus.get(str(r), []):
                items.append(ex)
    return {"type": "items", "items": items}


# ---------------------------------------------------------------- short-card statements (6.2)

def short_statements(card, S: Struct):
    gov = S.attrs[S.policy.gov].name
    out = [L.SHORT["closed"], L.SHORT["default"].format(default=card["display"][card["default"]])]
    tiers = card["tiers"]
    tc = (f"{tiers[0]} tier rules override {tiers[1]} tier rules" + "".join(f", which override {x} tier rules"
                                                                            for x in tiers[2:])) if tiers else ""
    out.append(L.SHORT[card["prim"]].format(gov=gov, tier_chain=tc))
    incl, excl = [], []
    f = card["forms"]
    for c in sorted(card["constructs"]):
        if c in ("num_ge", "num_le", "date_onbefore", "date_onafter"):
            incl.append(f"'{f[c][3:]}'")
        elif c in ("num_gt", "num_lt", "date_before", "date_after"):
            excl.append(f"'{f[c][3:]}'")
    if incl or excl:
        if not incl:
            out.append(f"Under this policy, {', '.join(excl)} do not include the value named.")
        elif not excl:
            out.append(f"Under this policy, {', '.join(incl)} include the value named.")
        else:
            out.append(L.SHORT["cmp"].format(incl=", ".join(incl), excl=", ".join(excl)))
    if S.notices:
        out.append(L.SHORT["gov"].format(gov=gov))
        out.append(L.SHORT["eff"].format(gov=gov))
        if any(n.ntype == "insert" for n in S.notices):
            out.append(L.SHORT["insert"])
        if any(n.ntype == "repeal" for n in S.notices):
            out.append(L.SHORT["repeal"].format(gov=gov))
    return out


# ---------------------------------------------------------------- documents

def policy_header(card, S):
    sc = card["scope"]
    return f"Issued by {card['body']}. Base policy effective {fmt_date(S.policy.B, card['forms']['date_form'])}. " \
           f"This policy covers cases whose {sc[0]} is {sc[1]}; a case's governing date is its " \
           f"{S.attrs[S.policy.gov].name}."


def build_doc(card, S: Struct, cases, fm: Fmt, rng, stmts, illus, attack=None, case_mode=None, sampler=None,
              q4_refs=None):
    """Doc IR for the state."""
    sampler = sampler or card["sampler"]
    T = card["titles"]
    title = f"{card['body']}: {card['subj']} policy"
    blocks = []
    head = {"type": "para", "text": policy_header(card, S)}
    pol_blocks = [head]
    if card["short"]:
        pol_blocks.append({"type": "items", "items": short_statements(card, S)})
    elif card["qtype"] != "Q3":
        ii = interp_items(card, stmts, illus)
        if ii:
            pol_blocks.append({"type": "section", "heading": T["interp"], "blocks": [ii]})
    pol_blocks.append({"type": "section", "heading": T["fields"], "blocks": [{"type": "items",
                                                                           "items": fm.fields_items()}]})
    # rules
    inert_r = [e for e in S.inert if e.cls in ("other_scope", "comment")]
    inert_n = [e for e in S.inert if e.cls in ("draft", "other_body")]
    if sampler == "S3":
        tb = s3_table(card, S, fm)
        pol_blocks.append({"type": "section", "heading": "Decision table", "blocks": [tb]})
        extra = [fm.inert(e) for e in inert_r]
        if extra:
            pol_blocks.append({"type": "section", "heading": "Policy notes", "blocks": [{"type": "items",
                                                                                         "items": extra}]})
    elif sampler == "S6":
        pass
    else:
        rule_txt = [fm.rule(r) for r in S.rules]
        # inert policy sentences placed among the rules (never counted or ranked)
        for e in inert_r:
            pos = rng.randint(0, len(rule_txt))
            rule_txt.insert(pos, fm.inert(e))
        if sampler == "S4":
            pol_blocks.append({"type": "section", "heading": T["rules"],
                               "blocks": [{"type": "para", "text": t} for t in rule_txt]})
        else:
            pol_blocks.append({"type": "section", "heading": T["rules"], "blocks": [{"type": "items",
                                                                                  "items": rule_txt}]})
    notes_txt = [fm.notice(n) for n in sorted(S.notices, key=lambda n: n.num)]
    for e in inert_n:
        notes_txt.insert(rng.randint(0, len(notes_txt)), fm.inert(e))
    if sampler != "S6" and notes_txt:
        pol_blocks.append({"type": "section", "heading": T["notices"] if sampler != "S3" else "Revision notices",
                           "blocks": [{"type": "items", "items": notes_txt}]})
    if sampler == "S6":
        # base policy and notices as separate titled documents, shuffled (doc order fixed in the structure)
        docs = []
        base_rules = [fm.rule(r) for r in S.rules]
        for e in inert_r:
            base_rules.insert(rng.randint(0, len(base_rules)), fm.inert(e))
        nmap = {n.num: n for n in S.notices}
        for d in (S.doc_order or ["base"] + [n.num for n in S.notices]):
            if d == "base":
                docs.append({"type": "section", "heading": f"Base policy, effective {fm.date(S.policy.B)}",
                             "blocks": [{"type": "items", "items": base_rules}]})
            else:
                n = nmap[d]
                docs.append({"type": "section", "heading": f"{card['forms']['notice_noun']} {n.num}",
                             "blocks": [{"type": "para", "text": fm.notice(n)}]})
        for e in inert_n:
            docs.append({"type": "section", "heading": "Other correspondence",
                         "blocks": [{"type": "para", "text": fm.inert(e)}]})
        pol_blocks += docs
    # case file(s)
    case_blocks = []
    if card["qtype"] == "Q4":
        at_i = rng.randrange(len(cases)) if attack else -1
        for i, (c, ref) in enumerate(zip(cases, q4_refs)):
            if case_mode == "record":
                cb = [{"type": "fields", "label": None, "pairs": [list(p) for p in fm.case_pairs(c)]}]
                if i == at_i:
                    cb.append({"type": "para", "text": attack})
            else:
                sents = fm.case_sentences(c, rng, include_false=False)
                if i == at_i:
                    sents.insert(rng.randint(1, len(sents)), attack)
                cb = [{"type": "items", "items": sents}]
            case_blocks.append({"type": "section", "heading": ref, "blocks": cb})
        case_sec = [{"type": "section", "heading": T["cases"], "blocks": [{"type": "para", "text":
                     L.STATEMENTS[43][0].format(gov=S.attrs[S.policy.gov].name) if card["short"] else
                     "Each listed case below is headed by its reference."}]}] + case_blocks
    else:
        c = cases[0]
        if case_mode == "record":
            pairs = fm.case_pairs(c, include_false=rng.random() < 0.6)
            cb = [{"type": "fields", "label": None, "pairs": [list(p) for p in pairs]}]
            if attack:
                cb.append({"type": "para", "text": attack})
        else:
            sents = fm.case_sentences(c, rng, include_false=(S.policy.world == "open" or rng.random() < 0.5))
            if attack:
                sents.insert(rng.randint(1, len(sents)), attack)
            cb = [{"type": "items", "items": sents}] if sampler != "S4" else [{"type": "para", "text": " ".join(sents)}]
        case_sec = [{"type": "section", "heading": T["case"], "blocks": cb}]
    if sampler == "S2":
        blocks = case_sec + pol_blocks
    else:
        blocks = pol_blocks + case_sec
    return {"title": title, "blocks": blocks}


def s3_table(card, S: Struct, fm: Fmt):
    """Decision table: one row per base rule (display order), cells per column, 'otherwise' line last."""
    cols = sorted({m.attr for r in S.rules for it in r.items for m in it.mem},
                  key=lambda k: int(k[1:]) if k[1:].isdigit() else 99)
    pri = card["tiers"] if "PRIORITY" in (card["prim"], card["sec"]) else None
    later = "LATER" in (card["prim"], card["sec"])
    head = [L.ROW_NOUN] + [S.attrs[c].name for c in cols]
    if pri:
        head.append("Tier")
    if later:
        head.append("In force from")
    head.append("Outcome")
    rows = []
    for r in S.rules:
        cells = {m.attr: it for it in r.items for m in it.mem}
        row = [f"{L.ROW_NOUN} {r.rid}"]
        for c in cols:
            it = cells.get(c)
            if it is None:
                row.append("any")
            elif S.attrs[c].type == "bool":
                row.append(L.YES if it.mem[0].args[0] else L.NO)
            else:
                t = fm.lit(it.mem[0])
                row.append(t[len(S.attrs[c].name) + 1:])  # cell = the literal without the field name
        if pri:
            row.append(card["tiers"][r.tier])
        if later:
            row.append(fm.date(r.date))
        row.append(fm.out(r.out))
        rows.append(row)
    oth = ["Otherwise"] + ["any"] * len(cols) + (["-"] if False else [])
    if pri:
        oth.append("any tier")
    if later:
        oth.append("any date")
    oth.append(fm.out(card["default"]))
    rows.append(oth)
    return {"type": "table", "caption": None, "columns": head, "rows": rows}


# ---------------------------------------------------------------- question and options

def question(card, q, rng):
    f = card["forms"]
    if q["qtype"] == "Q3":
        frames = L.Q3_FRAMES[q["pol"]]
        fr = frames[q.get("frame", 0) % len(frames)]
        return fr.format(ref=q["ref_text"], X=card["display"][q["X"]])
    if q["qtype"] == "Q1":
        return L.Q1_FRAMES[f["q1_frame"]].format(ref=q["ref_text"])
    if q["qtype"] == "Q2":
        return L.Q2_FRAMES[f["q2_frame"]].format(ref=q["ref_text"])
    if q["qtype"] == "Q4":
        return L.Q4_FRAMES[f["q4_frame"]].format(X=card["display"][q["X"]])
    raise ValueError


def q2_option_text(card, pair):
    o, b = pair
    if o == "__CBD__":
        return card["cbd_label"]
    if isinstance(b, int):
        bt = L.BASIS_RULE.format(noun=card["forms"]["rule_noun"], rid=b)
    else:
        bt = card["codes"][b]
    return f"{card['display'][o]}{card['forms']['q2_sep']}{bt}"
