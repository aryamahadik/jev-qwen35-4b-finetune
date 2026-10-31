"""F4 renderer: sampled structure -> Doc IR (state), card IR, question and options, then fmt1 render_row_text.

Sentence grammar (2.1): fact sentences with one named-entity subject and 'and'-joined conjuncts that each carry their
own copula, cue or verb; rules in the 2.1 forms (bulleted lists result-last with the exception on the closing line);
hedges, entity hedges, closure lines, the three attribution frames, the V2 topic line, background sentences.
"""
from __future__ import annotations

import datetime as dt
import random
from decimal import Decimal

import core as C
import f4lex as L

# ------------------------------------------------------------------------------------------------------- words


class Lex:
    def __init__(self, cp, date_fmt="dmy"):
        self.cp = cp
        self.types = cp.types
        self.date_fmt = date_fmt
        self.qty = {q["name"]: q for q in cp.qtys}

    def tsg(self, t):
        return self.types[t][0]

    def tpl(self, t):
        return self.types[t][1]

    def card_type(self):
        """<type> live value: the type noun on one-type cards, the umbrella noun otherwise."""
        return (self.types[0][0], self.types[0][1]) if len(self.types) == 1 else tuple(self.cp.umbrella)

    def num(self, q, v: Decimal):
        dec = self.qty[q]["dec"]
        return format(v.quantize(Decimal(1).scaleb(-dec)), "f")

    def unit(self, q):
        u = self.qty[q]["unit"]
        return "%" if u == "%" else " " + u

    def date(self, d: dt.date):
        if self.date_fmt == "iso":
            return d.isoformat()
        if self.date_fmt == "mdy":
            return f"{L.MONTHS[d.month - 1]} {d.day}, {d.year}"
        return f"{d.day} {L.MONTHS[d.month - 1]} {d.year}"

    def link(self, li):
        return self.cp.links[li]


def a_(noun):
    return L.article(noun)


# ------------------------------------------------------------------------------------------------------- conditions

def lit_phrase(pred, pos, cue=None, plural=False):
    """'is A' / 'is not A' / cue forms. cue: None | 'pos0' | 'neg0' | 'neg1'."""
    if cue and pos and cue.startswith("pos"):
        t = L.CUES["pos"][int(cue[3:])]
    elif cue and not pos and cue.startswith("neg"):
        t = L.CUES["neg"][int(cue[3:])]
    else:
        t = ("are " if plural else "is ") + ("" if pos else "not ") + "{P}"
        return t.format(P=pred)
    if plural:
        t = L.CUE_PLURAL[t]
    return t.format(P=pred)


def cmp_phrase(lx: Lex, cond, pid=0):
    k = cond[0]
    if k == "cmp":
        _, q, op, T = cond
        ph = L.CMP_PHRASES[op][pid % len(L.CMP_PHRASES[op])]
        return f"whose {q} " + ph.format(T=lx.num(q, T), U=lx.unit(q))
    if k == "rng":
        _, q, T1, T2 = cond[:4]
        ph = L.RANGE_PHRASES[pid % 2]
        return f"whose {q} " + ph.format(T1=lx.num(q, T1), T2=lx.num(q, T2), U=lx.unit(q))
    if k == "dcmp":
        _, a, op, D = cond
        ph = L.DATE_PHRASES[op][pid % 2]
        return f"whose {a} " + ph.format(D=lx.date(D))
    if k == "win":
        _, a, D1, D2 = cond[:4]
        ph = L.WINDOW_PHRASES[pid % 2]
        return f"whose {a} " + ph.format(D1=lx.date(D1), D2=lx.date(D2))
    raise ValueError(k)


def bullet_phrase(lx: Lex, cond, style, i):
    """A condition as a list item about the rule's single subject ('it is A', 'its lamp reading is ...')."""
    if cond[0] == "lit":
        return "it " + lit_phrase(cond[1], cond[2], style.get(f"cue{i}"))
    ph = cmp_phrase(lx, cond, style.get(f"ph{i}", 0))
    return "its " + ph[len("whose "):]


def body_phrase(lx: Lex, conds, style, plural=False):
    lits = [(i, c) for i, c in enumerate(conds) if c[0] == "lit"]
    cmps = [(i, c) for i, c in enumerate(conds) if c[0] != "lit"]
    parts = []
    if lits:
        parts.append("that " + " and ".join(lit_phrase(c[1], c[2], style.get(f"cue{i}"), plural) for i, c in lits))
    for i, c in cmps:
        parts.append(cmp_phrase(lx, c, style.get(f"ph{i}", 0)))
    return " and ".join(parts)


def head_phrase(head, plural=False):
    return lit_phrase(head[0], head[1], None, plural)


def exc_phrase(rule):
    if not rule.exc:
        return ""
    if rule.style.get("excw") == "except":
        return f", except one that is {rule.exc}"
    return f", unless it is {rule.exc}"


def rule_text(lx: Lex, rule):
    """('line', sentence) or ('list', lead-in, [items], closing or None)."""
    st = rule.style
    q = st.get("quant", "every")
    t = rule.typ
    sg, pl = lx.tsg(t), lx.tpl(t)
    if rule.form in ("univ", "neguniv") and len(rule.conds) == 3:
        items = [bullet_phrase(lx, c, st, i) for i, c in enumerate(rule.conds)]
        lead = L.LIST_LEADIN.format(type=sg)
        if rule.form == "neguniv":
            close = f"No such {sg} is {rule.head[0]}{exc_phrase(rule)}."
        else:
            close = L.LIST_CLOSE.format(type=sg, head=head_phrase(rule.head), exc=exc_phrase(rule))
        return ("list", lead, items, close)
    if rule.form == "kofn":
        lead = L.KOFN_LEADIN.format(type=sg, H=rule.head[0], k=rule.k)
        items = [bullet_phrase(lx, c, st, i) for i, c in enumerate(rule.conds)]
        return ("list", lead, items, None)
    if rule.form == "univ":
        if q == "all" and not rule.exc and rule.head[1] and all(c[0] == "lit" for c in rule.conds):
            return ("line", f"All {pl} {body_phrase(lx, rule.conds, st, plural=True)} "
                            f"{head_phrase(rule.head, plural=True)}.")
        Q = {"every": "Every", "each": "Each", "any": "Any", "all": "Every"}[q]
        return ("line", f"{Q} {sg} {body_phrase(lx, rule.conds, st)} {head_phrase(rule.head)}{exc_phrase(rule)}.")
    if rule.form == "neguniv":
        return ("line", f"No {sg} {body_phrase(lx, rule.conds, st)} is {rule.head[0]}{exc_phrase(rule)}.")
    if rule.form == "link":
        lk = lx.link(rule.link)
        t2 = lx.tsg(rule.ptyp)
        Q = {"every": "Every", "each": "Each", "any": "Any", "all": "Every"}[q]
        pc = lit_phrase(rule.pcond[0], rule.pcond[1], st.get("pcue"))
        return ("line", f"{Q} {sg} that {lk['active']} {a_(t2)} {t2} that {pc} {head_phrase(rule.head)}.")
    if rule.form == "onlyif":
        art = a_(sg).capitalize()
        return ("line", f"{art} {sg} is {rule.ante} only if it is {rule.head[0]}.")
    if rule.form == "or":
        Q = {"every": "Every", "each": "Each", "any": "Any", "all": "Every"}[q]
        a, b = rule.conds
        return ("line", f"{Q} {sg} that is {a[1]} or {b[1]} {head_phrase(rule.head)}.")
    if rule.form == "xor":
        Q = {"every": "Every", "each": "Each", "any": "Any", "all": "Every"}[q]
        a, b = rule.conds
        return ("line", f"{Q} {sg} that is either {a[1]} or {b[1]}, but not both, {head_phrase(rule.head)}.")
    raise ValueError(rule.form)


# ------------------------------------------------------------------------------------------------------- statements

def conjunct(lx: Lex, s: C.Stmt, cue=None):
    if s.kind == "lit":
        return lit_phrase(s.pred, s.pos, cue)
    if s.kind == "val":
        return f"has {a_(s.pred)} {s.pred} of {lx.num(s.pred, s.value)}{lx.unit(s.pred)}"
    if s.kind == "date":
        return f"has {a_(s.pred)} {s.pred} of {lx.date(s.value)}"
    if s.kind == "link":
        return f"{lx.link(s.pred)['active']} {s.value}"
    if s.kind == "type":
        t = lx.tsg(s.pred)
        return f"is {a_(t)} {t}"
    raise ValueError(s.kind)


def fact_sentence(lx: Lex, subject, parts):
    """parts: list of (Stmt, cue). One subject, 'and'-joined conjuncts, each with its own copula / cue / verb."""
    return f"{subject} " + " and ".join(conjunct(lx, s, cue) for s, cue in parts) + "."


def statement_text(lx: Lex, s: C.Stmt, cue=None):
    """One attributed statement body: exactly one literal, value or date (no terminal period)."""
    return f"{s.e} {conjunct(lx, s, cue)}"


def attribution(src: str, frame: str, body: str):
    S = src[:1].upper() + src[1:]
    if frame == "quote":
        return f'{S}: "{body}."'
    if frame == "reported":
        return f"{S} reported that {body}."
    return f"{S}: {body}."


def hedge_sentence(lx: Lex, h):
    kind, typ, cnd, hd = h
    sg, pl = lx.tsg(typ), lx.tpl(typ)
    cp_ = lit_phrase(cnd[0], cnd[1], None, plural=True)
    hp = lit_phrase(hd[0], hd[1], None, plural=True)
    if kind == "most":
        return f"Most {pl} that {cp_} {hp}."
    if kind == "many":
        return f"Many {pl} that {cp_} {hp}."
    if kind == "usually":
        return f"{pl[:1].upper() + pl[1:]} that {cp_} {hp.replace('are ', 'are usually ', 1)}."
    if kind == "often":
        return f"{pl[:1].upper() + pl[1:]} that {cp_} {hp.replace('are ', 'are often ', 1)}."
    if kind == "some":
        return f"Some {pl} that {cp_} {hp}."
    if kind == "notevery":
        return f"Not every {sg} that {lit_phrase(cnd[0], cnd[1])} {lit_phrase(hd[0], hd[1])}."
    if kind == "exist":
        return f"Some {sg} that {lit_phrase(cnd[0], cnd[1])} {lit_phrase(hd[0], hd[1])}."
    raise ValueError(kind)


def ehedge_sentence(kind, e, pred):
    return f"{e} {kind} {pred}."


def closure_line(lx: Lex, pred, typ, form):
    if form == "column":
        return f"The {pred} column is complete: a blank {pred} cell means No."
    return f"The record names every {lx.tsg(typ)} that is {pred}."


def topic_line(label, claim):
    p, e, pos = claim
    return f"{label}: whether {e} is {'' if pos else 'not '}{p}"


def claim_clause(claim):
    p, e, pos = claim
    return f"{e} is {'' if pos else 'not '}{p}"


# ======================================================================================================= state (Doc IR)

from decimal import Decimal as _D  # noqa: E402

PROSE_INLINE = ("prose.plain", "prose.titled_caps", "prose.section_signs")


def _cap(s):
    return s[:1].upper() + s[1:]


def group_facts(lx: Lex, rec, stmts, rng, *, max_conj=2, with_types=True, typed=None):
    """Fact sentences for unattributed sentence statements: per entity, 1-2 conjuncts per sentence, the entity's type
    conjunct joined to its first sentence. Returns [(sentence, [sids], subject)]. typed: set of entities whose type
    is already stated elsewhere (tables)."""
    typed = set(typed or ())
    by_e = {}
    for s in stmts:
        by_e.setdefault(s.e, []).append(s)
    out = []
    for e, ss in by_e.items():
        ss = list(ss)
        rng.shuffle(ss)
        parts = []
        if with_types and e not in typed:
            parts.append((C.Stmt(sid="type:" + e, kind="type", e=e, pred=rec.ents[e]), None))
            typed.add(e)
        for s in ss:
            parts.append((s, s.extra_cue if hasattr(s, "extra_cue") else None))
        i = 0
        while i < len(parts):
            n = 1 if rng.random() < 0.55 else max_conj
            chunk = parts[i:i + n]
            out.append((fact_sentence(lx, e, chunk), [p.sid for p, _ in chunk], e))
            i += n
    return out, typed


def type_sentences(lx: Lex, rec, ents):
    return [(f"{e} is {a_(lx.tsg(rec.ents[e]))} {lx.tsg(rec.ents[e])}.", ["type:" + e], e) for e in ents]


def cue_for(s: C.Stmt, rng):
    if s.kind != "lit" or s.pos is None:
        return None
    if s.pos and rng.random() < 0.12:
        return "pos0"
    if not s.pos and rng.random() < 0.3:
        return "neg0" if rng.random() < 0.6 else "neg1"
    return None


def table_block(lx: Lex, rec, tb, typed_vals: bool, caption):
    """A table: rows = entities; columns = ID, type, then the table's columns. Cells come from statements with
    via == 'cell' and this tid; marker statements give 'not recorded' (null when typed); closed columns give blank."""
    cols = [L.TABLE_ID_COL, L.TABLE_TYPE_COL]
    heads = []
    for kind, key in tb["cols"]:
        if kind in ("pred", "closed"):
            heads.append(key)
        elif kind == "qty":
            heads.append(key)
        elif kind == "date":
            heads.append(key)
        elif kind == "link":
            heads.append(lx.link(key)["active"])
    cols += heads
    cells = {}
    for s in rec.stmts:
        if s.via == "cell" and s.tid == tb["tid"]:
            if s.kind == "link":
                cells.setdefault((s.e, ("link", s.pred)), []).append(s.value)
            else:
                k = ("qty" if s.kind == "val" else ("date" if s.kind == "date" else None), s.pred)
                cells[(s.e, k if k[0] else ("pred", s.pred))] = s
    rows = []
    from fmt1.render import BLANK
    for e in tb["rows"]:
        r = [e, lx.tsg(rec.ents[e])]
        for kind, key in tb["cols"]:
            if kind == "link":
                ps = cells.get((e, ("link", key)))
                r.append(", ".join(sorted(ps)))
                continue
            ck = ("pred", key) if kind in ("pred", "closed") else (kind, key)
            s = cells.get((e, ck))
            if s is None:
                if kind == "closed":
                    r.append(BLANK)
                    continue
                raise ValueError("table cell without a statement")
            if s.kind == "lit":
                if s.pos is None:
                    r.append(None if typed_vals else "not recorded")
                else:
                    r.append(s.pos if typed_vals else ("Yes" if s.pos else "No"))
            elif s.kind == "val":
                if s.value is None:
                    r.append(None if typed_vals else "not recorded")
                else:
                    r.append(_D(lx.num(key, s.value)))
            elif s.kind == "date":
                r.append(None if (s.value is None and typed_vals) else ("not recorded" if s.value is None
                                                                       else lx.date(s.value)))
        rows.append(r)
    return {"type": "table", "caption": caption, "columns": cols, "rows": rows}


def rule_blocks(lx: Lex, rules):
    """[(kind, payload)] items: ('line', text) or ('list', lead, items, close)."""
    return [rule_text(lx, r) for r in rules]


def record_items(lx: Lex, rec, rng):
    """All record items (before layout): dict of lists. Each item: (text, sids, kind)."""
    tables = rec.extras.get("tables", [])
    in_table = set()
    for tb in tables:
        in_table |= set(tb["rows"])
    sent = [s for s in rec.stmts if s.via == "sent" and s.src is None]
    attrib = [s for s in rec.stmts if s.src is not None]
    for s in sent:
        s.extra_cue = cue_for(s, rng) if not getattr(s, "no_cue", False) else None
    facts, typed = group_facts(lx, rec, sent, rng, typed=in_table)
    need_type = [e for e in sorted(rec.ents) if e not in typed]
    types = type_sentences(lx, rec, need_type)
    items = {"facts": [(t, sids, "fact") for t, sids, _ in facts] + [(t, sids, "type") for t, sids, _ in types]}
    att = []
    for s in attrib:
        body = statement_text(lx, s, cue_for(s, rng))
        att.append((attribution(s.src, s.frame or "colon", body), [s.sid], "attr"))
    items["attrib"] = att
    rr = []
    for r in rec.rules:
        if r.where != "record":
            continue
        rr.append((rule_text(lx, r), [r.rid], "rule"))
    items["rules"] = rr
    notes = []
    for i, h in enumerate(rec.hedges):
        notes.append((hedge_sentence(lx, h), [f"h{i}"], "hedge"))
    for i, (k, e, p) in enumerate(rec.ehedges):
        notes.append((ehedge_sentence(k, e, p), [f"eh{i}"], "ehedge"))
    for i, (p, t, form, tid) in enumerate(rec.closures):
        if form == "prose":
            notes.append((closure_line(lx, p, t, form), [f"cl{i}"], "closure"))
    items["notes"] = notes
    items["colclosures"] = {tid: (closure_line(lx, p, t, "column"), [f"cl{i}"], "closure")
                            for i, (p, t, form, tid) in enumerate(rec.closures) if form == "column"}
    ex = rec.extras
    items["background"] = [(t, [f"bg{i}"], "bg") for i, t in enumerate(ex.get("background", []))]
    items["topic"] = [(ex["topic"], ["topic"], "topic")] if ex.get("topic") else []
    items["inject"] = [(ex["inject"], ["inject"], "inject")] if ex.get("inject") else []
    items["tables"] = tables
    return items


def _rule_to_blocks(item, container):
    """A rule item -> Doc blocks (list rules: lead-in para, items, closing para)."""
    (rt, sids, kind) = item
    if rt[0] == "line":
        return None
    _, lead, its, close = rt
    bl = [{"type": "para", "text": lead}, {"type": "items", "items": list(its)}]
    if close:
        bl.append({"type": "para", "text": close})
    return bl


def decile_of(L, n):
    """G0 8 literal decile of slot L (0-based) among n statements."""
    return min(9, (10 * L) // n)


def decile_pick(m, n, t):
    """Repair r2: the decile the layout realises for target decile t in a block of n statements with m decisive ones:
    t itself when some feasible slot L in [m-1, n-1] lies in it, else the nearest feasible decile (ties: the lower).
    Shared with the build's target solver so both sides agree."""
    reach = sorted({decile_of(L, n) for L in range(m - 1, n)})
    return min(reach, key=lambda d: (abs(d - t), d))


def _placed(xs, rng, dec, info, key, pos_u=None):
    """Statement order inside one block (8; repair r2). The LAST decisive item sits at slot L, the other decisive items
    at random slots before it, the rest at random. pos_u is None (L uniform over the feasible slots [m-1, n-1]) or
    {"t": target decile}: L is drawn among the feasible slots whose literal decile floor(10 L / n) equals
    decile_pick(m, n, t). All placement randomness comes from a private generator seeded by ONE draw of rng, so the
    rest of the rendering is the same whatever L is. Without decisive items: a plain shuffle.
    info[key] = (L, n, m) for the position check."""
    xs = list(xs)
    if not dec:
        rng.shuffle(xs)
        return xs
    di = [x for x in xs if any(sd in dec for sd in x[1])]
    nd = [x for x in xs if not any(sd in dec for sd in x[1])]
    m, n = len(di), len(xs)
    if m == 0:
        rng.shuffle(xs)
        return xs
    prng = random.Random(rng.random())
    prng.shuffle(di)
    prng.shuffle(nd)
    if isinstance(pos_u, dict) and pos_u.get("t") is not None:
        d = decile_pick(m, n, int(pos_u["t"]))
        L = prng.choice([l for l in range(m - 1, n) if decile_of(l, n) == d])
    else:
        L = prng.randint(m - 1, n - 1)
    before = sorted(prng.sample(range(L), m - 1))
    out = [None] * n
    out[L] = di[-1]
    for slot, x in zip(before, di[:-1]):
        out[slot] = x
    it_nd = iter(nd)
    for i in range(n):
        if out[i] is None:
            out[i] = next(it_nd)
    info[key] = (L, n, m)
    return out


def _interleave_place(facts, line_rules, list_rules, fsz, rsz, dec, prng, info, pos_u):
    """S1 interleaved layout (5.1; repair r2): fact paragraphs (sizes fsz) alternate with rule groups (line-rule
    chunks of sizes rsz, then one group per list rule). The section is ONE block for the position check (G0 8: a
    non-block layout is measured among all its statements), so the last decisive statement of the merged sequence is
    put at a slot L whose literal decile is decile_pick-ed for the target, the other decisive facts / line rules at
    slots of their kind before it, the rest at random slots of their kind; list rules keep their place.
    Returns (facts, line_rules) reordered; info["mixed"] = (L, n, m); the separate facts / rules entries are dropped."""
    isdec = lambda x: any(sd in dec for sd in x[1])
    kinds = []
    gi = 0
    fq, rq = list(fsz), list(rsz) + [None] * len(list_rules)
    while fq or rq:
        if fq:
            kinds += ["F"] * fq.pop(0)
        if rq:
            r = rq.pop(0)
            if r is None:
                kinds.append(("S", gi))
                gi += 1
            else:
                kinds += ["R"] * r
    n = len(kinds)
    df = [x for x in facts if isdec(x)]
    dr = [x for x in line_rules if isdec(x)]
    ds = [i for i, k in enumerate(kinds) if isinstance(k, tuple) and isdec(list_rules[k[1]])]
    m = len(df) + len(dr) + len(ds)
    info.pop("facts", None)
    info.pop("rules", None)
    if m == 0:
        return facts, line_rules
    feas = []
    nf = nr = 0
    for i, k in enumerate(kinds):
        last_s = max(ds) if ds else -1
        if k == "F" and df and nf >= len(df) - 1 and nr >= len(dr) and last_s < i:
            feas.append(i)
        elif k == "R" and dr and nr >= len(dr) - 1 and nf >= len(df) and last_s < i:
            feas.append(i)
        elif isinstance(k, tuple) and i == last_s and nf >= len(df) and nr >= len(dr):
            feas.append(i)
        nf += k == "F"
        nr += k == "R"
    if not feas:
        raise ValueError("interleave_infeasible")
    info["_mixed_reach"] = sorted({decile_of(i, n) for i in feas})
    t = pos_u.get("t") if isinstance(pos_u, dict) else None
    if t is None:
        L = prng.choice(feas)
    else:
        reach = sorted({decile_of(i, n) for i in feas})
        d = min(reach, key=lambda d_: (abs(d_ - int(t)), d_))
        L = prng.choice([i for i in feas if decile_of(i, n) == d])
    fslots = [i for i, k in enumerate(kinds) if k == "F"]
    rslots = [i for i, k in enumerate(kinds) if k == "R"]

    def fill(items, dl, slots, last):
        nd_ = [x for x in items if not isdec(x)]
        prng.shuffle(dl)
        prng.shuffle(nd_)
        pre = [j for j, i in enumerate(slots) if i < L]
        out = [None] * len(slots)
        rest = list(dl)
        if last:
            out[slots.index(L)] = rest.pop()
            pre = [j for j in pre if slots[j] != L]
        for j, x in zip(sorted(prng.sample(pre, len(rest))), rest):
            out[j] = x
        it = iter(nd_)
        return [x if x is not None else next(it) for x in out]
    kL = kinds[L]
    facts = fill(facts, df, fslots, kL == "F")
    line_rules = fill(line_rules, dr, rslots, kL == "R")
    info["mixed"] = (L, n, m)
    return facts, line_rules


def build_doc(lx: Lex, rec, cp, style, rng, *, title=None, decisive=None, posinfo=None, pos_u=None):
    """Doc IR for the record in this style's container, laid out by the card's sampler shape. Returns (doc, order)
    where order lists the sids of record statements in display order (for the decisive-position check).
    decisive: sids (and rule ids) of the row's decisive statements; posinfo receives (L, n, m) per block."""
    dec = set(decisive or ())
    if posinfo is None:
        posinfo = {}
    cont = style["container"]
    skin = style["skin"]
    S = cp.sampler
    it = record_items(lx, rec, rng)
    order = []
    typed = cont in ("json", "yaml")
    single = skin in ("json.lines", "json.array") or cont == "csv"

    def lines(items):
        txt = []
        for t, sids, kind in items:
            if kind == "rule":
                assert t[0] == "line"
                txt.append(t[1])
            else:
                txt.append(t)
            order.extend(sids)
        return txt

    def shuffled(xs):
        xs = list(xs)
        rng.shuffle(xs)
        return xs
    if S == "S4":
        facts = list(it["facts"])            # placed below together with the attributed lines
        attrib = list(it["attrib"])
    elif S == "S5":
        facts = list(it["facts"])            # placed below together with the background lines
        attrib = _placed(it["attrib"], rng, dec, posinfo, "attrib", pos_u)
    else:
        facts = _placed(it["facts"], rng, dec, posinfo, "facts", pos_u)
        attrib = _placed(it["attrib"], rng, dec, posinfo, "attrib", pos_u)
    rules = _placed(it["rules"], rng, dec, posinfo, "rules", pos_u)
    notes = shuffled(it["notes"] + it["background"] + it["topic"] + it["inject"])
    # table rows (repair r1): rows stay in ID order unless the table holds a decisive cell; then the last decisive
    # row sits at a uniformly drawn feasible slot (8)
    tabs = []
    for tb in it["tables"]:
        drows = {f"row:{s_.e}" for s_ in rec.stmts if s_.via == "cell" and s_.tid == tb["tid"] and s_.sid in dec}
        if drows:
            ritems = _placed([(e, [f"row:{e}"], "row") for e in tb["rows"]], rng, drows, posinfo, "table", pos_u)
            tb = {**tb, "rows": [x[0] for x in ritems]}
        tabs.append(tb)
    it["tables"] = tabs
    line_rules = [x for x in rules if x[0][0] == "line"]
    list_rules = [x for x in rules if x[0][0] == "list"]
    blocks = []
    hd = {k: rng.choice(v) for k, v in (("facts", L.HEADINGS_FACTS), ("rules", L.HEADINGS_RULES),
                                         ("table", L.HEADINGS_TABLE), ("stmts", L.HEADINGS_STMTS),
                                         ("notes", L.HEADINGS_NOTES), ("narr", L.HEADINGS_NARR))}
    if single:
        if len(it["tables"]) != 1 or facts or rules or notes or attrib or it["colclosures"]:
            raise ValueError("single-table style needs a table-only record")
        tb = it["tables"][0]
        blk = table_block(lx, rec, tb, typed, None)
        order.extend(f"row:{e}" for e in tb["rows"])
        doc = {"blocks": [blk]}
        if not skin.startswith("json") and title:
            doc["title"] = title
        return doc, order
    # tables first (S3), with column-closure lines next to them
    for tb in it["tables"]:
        blk = table_block(lx, rec, tb, typed, None)
        order.extend(f"row:{e}" for e in tb["rows"])
        sub = [blk]
        cc = it["colclosures"].get(tb["tid"])
        if cc:
            sub.append({"type": "para", "text": cc[0]} if not typed else {"type": "items", "items": [cc[0]]})
            order.extend(cc[1])
        blocks.append({"type": "section", "heading": hd["table"] if len(it["tables"]) == 1 else
                       f"{hd['table']} {len(blocks) + 1}", "blocks": sub})
    if S == "S5":
        # narrative: facts and background mixed into paragraphs; reports on their own lines; procedure paragraph
        narr = _placed(facts + [x for x in notes if x[2] == "bg"], rng, dec, posinfo, "facts", pos_u)
        other_notes = [x for x in notes if x[2] != "bg"]
        paras = []
        i = 0
        while i < len(narr):
            n = rng.randint(2, 4)
            paras.append(narr[i:i + n])
            i += n
        att_slots = {rng.randint(0, max(0, len(paras))): [] for _ in attrib}
        nb = []
        for j, p in enumerate(paras):
            nb.append({"type": "para", "text": " ".join(lines(p))})
            if attrib and rng.random() < 0.5:
                a = attrib.pop()
                nb.append({"type": "para", "text": lines([a])[0]})
        for a in attrib:
            nb.append({"type": "para", "text": lines([a])[0]})
        blocks.append({"type": "section", "heading": hd["narr"], "blocks": nb})
        rb = []
        if line_rules:
            rb.append({"type": "para", "text": " ".join(lines(line_rules))})
        for x in list_rules:
            order.extend(x[1])
            rb.extend(_rule_to_blocks(x, cont))
        if rb:
            blocks.append({"type": "section", "heading": hd["rules"], "blocks": rb})
        if other_notes:
            blocks.append({"type": "section", "heading": hd["notes"],
                           "blocks": [{"type": "para", "text": t} for t in lines(other_notes)]})
        doc = {"blocks": blocks}
        if title:
            doc["title"] = title
        return doc, order
    use_items = typed or S in ("S2", "S3", "S4") or cont in ("bullet_sop",)
    fsz, rsz = [], []
    if S == "S4":
        stm = _placed(attrib + facts, rng, dec, posinfo, "facts", pos_u)
        blocks.append({"type": "section", "heading": hd["stmts"], "blocks": [{"type": "items",
                                                                             "items": lines(stm)}]})
        attrib = []
        facts = []
    if facts:
        if use_items:
            blocks.append({"type": "section", "heading": hd["facts"],
                           "blocks": [{"type": "items", "items": lines(facts)}]})
        else:
            fb = []
            i = 0
            while i < len(facts):
                n = rng.randint(2, 5)
                fsz.append(len(facts[i:i + n]))
                fb.append({"type": "para", "text": " ".join(lines(facts[i:i + n]))})
                i += n
            blocks.append({"type": "section", "heading": hd["facts"], "blocks": fb})
    if line_rules or list_rules:
        groups = []
        if use_items:
            if line_rules:
                groups.append([{"type": "items", "items": lines(line_rules)}])
        else:
            i = 0
            while i < len(line_rules):
                n = rng.randint(1, 3)
                rsz.append(len(line_rules[i:i + n]))
                groups.append([{"type": "para", "text": " ".join(lines(line_rules[i:i + n]))}])
                i += n
        for x in list_rules:
            if typed:
                raise ValueError("list rule in a typed container")
            order.extend(x[1])
            groups.append(_rule_to_blocks(x, cont))
        if S == "S1" and rng.random() < 0.5 and len(blocks) == 1 and not use_items:
            # interleave facts and rules (S1: half the rows); a list rule stays one group. Repair r2: the merged
            # section is one block for the position check, so facts and line rules are re-placed in it
            blocks.pop()
            prng_i = random.Random(rng.random())
            if dec:
                facts, line_rules = _interleave_place(facts, line_rules, list_rules, fsz, rsz, dec, prng_i,
                                                      posinfo, pos_u)
            txt = lambda its: [t[1] if k == "rule" else t for t, sids, k in its]
            fb, i = [], 0
            for sz in fsz:
                fb.append([{"type": "para", "text": " ".join(txt(facts[i:i + sz]))}])
                i += sz
            groups, i = [], 0
            for sz in rsz:
                groups.append([{"type": "para", "text": " ".join(txt(line_rules[i:i + sz]))}])
                i += sz
            for x in list_rules:
                groups.append(_rule_to_blocks(x, cont))
            posinfo["_layout"] = "interleaved"
            mixed = []
            while fb or groups:
                if fb:
                    mixed.extend(fb.pop(0))
                if groups:
                    mixed.extend(groups.pop(0))
            blocks.append({"type": "section", "heading": hd["facts"], "blocks": mixed})
        else:
            blocks.append({"type": "section", "heading": hd["rules"],
                           "blocks": [b_ for g_ in groups for b_ in g_]})
    if notes or attrib:
        nn = notes + attrib
        if use_items:
            blocks.append({"type": "section", "heading": hd["notes"],
                           "blocks": [{"type": "items", "items": lines(nn)}]})
        else:
            blocks.append({"type": "section", "heading": hd["notes"],
                           "blocks": [{"type": "para", "text": t} for t in lines(nn)]})
    doc = {"blocks": blocks}
    if title:
        doc["title"] = title
    return doc, order


# ======================================================================================================= card IR

def join_or(names):
    names = list(names)
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " or " + names[-1]


def clause_texts(lx: Lex, cp, clause_ids):
    """[(clause id, text)] in canonical order with live values filled (7.1, 9)."""
    tsg, tpl = lx.card_type()
    um_sg, um_pl = cp.umbrella
    out = []
    for cid in L.CLAUSE_ORDER:
        if cid not in clause_ids:
            continue
        if cid == "15":
            for q in cp.qtys:
                out.append(("15", L.CLAUSES["15"].format(quantity=q["name"], unit=q["unit"] if q["unit"] != "%"
                                                         else "percent")))
            continue
        t = L.CLAUSES[cid]
        t = t.replace("a {type}", a_(tsg) + " {type}").replace("A {type}", a_(tsg).capitalize() + " {type}")
        t = t.replace("{types}", tpl).replace("{type}", tsg).replace("{entities}", um_pl).replace("{entity}", um_sg)
        if cid == "22":
            t = t.replace("{sources}", join_or(cp.trust[1]))
        out.append((cid, t))
    return out


def persona_line(cp):
    return L.PERSONA_TEMPLATES[cp.persona_tpl % len(L.PERSONA_TEMPLATES)].format(role=cp.pack["role"])


def example_sentence(kind, tsg, A, H, Cx, X, world):
    if kind == "fwd":
        return f"If every {tsg} that is {A} is {H} and {X} is {A}, then the record establishes that {X} is {H}."
    if kind == "bwd":
        return f"If every {tsg} that is {A} is {H} and {X} is not {H}, then the record rules out that {X} is {A}."
    if kind == "exc":
        out = "the record leaves open whether" if world == "OW" else "the record rules out that"
        return (f"If every {tsg} that is {A} is {H}, unless it is {Cx}, and {X} is {A} and is {Cx}, then {out} "
                f"{X} is {H}.")
    raise ValueError(kind)


def card_ir(lx: Lex, cp, *, standing_rules=(), option_defs=None, fewshot=None):
    """The card IR for this card (same clauses on every row; option definitions per row form)."""
    blocks = [{"type": "para", "text": persona_line(cp)}]
    cl = clause_texts(lx, cp, cp.clause_set)
    ds = cp.defs_style
    tsg = lx.card_type()[0]
    if ds == "one_line_examples" and cp.example_kinds:
        ex_by = {}
        A, H, Cx = cp.example_preds
        X = L.EXAMPLE_IDS[0]
        for kind in cp.example_kinds:
            target = {"fwd": ("3", "3c", "3s"), "bwd": ("4",), "exc": ("6",)}[kind]
            for cid in target:
                if any(c == cid for c, _ in cl):
                    ex_by.setdefault(cid, []).append(example_sentence(kind, tsg, A, H, Cx, X, cp.world))
                    break
        entries = []
        seen_names = {}
        for cid, t in cl:
            nm = L.CLAUSE_TOPICS[cid]
            seen_names[nm] = seen_names.get(nm, 0) + 1
            if seen_names[nm] > 1:
                nm = f"{nm} ({seen_names[nm]})"
            e = {"name": nm, "text": t}
            if ex_by.get(cid):
                e["examples"] = ex_by.pop(cid)[:2]
            entries.append(e)
        blocks.append({"type": "defs", "variant": cp.defs_variant, "heading": None, "entries": entries})
    elif ds == "decision_list":
        blocks.append({"type": "steps", "items": [t for _, t in cl]})
    else:
        blocks.append({"type": "items", "items": [t for _, t in cl]})
    if standing_rules:
        items = []
        for r in standing_rules:
            rt = rule_text(lx, r)
            assert rt[0] == "line"
            items.append(rt[1])
        blocks.append({"type": "section", "heading": "Standing rules", "blocks": [{"type": "items", "items": items}]})
    if fewshot:
        blocks.append({"type": "fewshot", "template": fewshot["template"], "heading": None,
                       "examples": fewshot["examples"]})
    if option_defs:
        blocks.append({"type": "defs", "variant": "DV01", "heading": None,
                       "entries": [{"name": n, "text": t} for n, t in option_defs]})
    return {"blocks": blocks}


# ======================================================================================================= questions

def question_text(form, claim, frame_p, fill_i=0, *, types_pl=None, H=None):
    """The instantiated section 1 frame for a row."""
    cc = claim_clause(claim) if claim else None
    if form in ("YN-F", "YN-R", "YN-O"):
        key = {"YN-F": "F", "YN-R": "R", "YN-O": "O"}[form]
        fr = frame_p[0]
        fills = L.OUT_FILL[key]["A" if fr == "Q-A" else "B"]
        tpl = L.FRAMES[fr][frame_p[1]]
        return tpl.replace("{OUT}", fills[fill_i % len(fills)]).replace("<c>", cc)
    if form in ("YN-nF", "YN-nR"):
        key = {"YN-nF": "nF", "YN-nR": "nR"}[form]
        fills = L.OUT_FILL[key]["B"]
        tpl = L.FRAMES["Q-B"][frame_p[1]]
        return tpl.replace("{OUT}", fills[fill_i % len(fills)]).replace("<c>", cc)
    if form == "YN-dn":
        fills = L.OUT_FILL["dn"]["D"]
        tpl = L.FRAMES["Q-D"][frame_p[1]]
        return tpl.replace("{OUT}", fills[fill_i % len(fills)]).replace("<c>", cc)
    if form == "YN-T":
        return L.FRAMES["Q-T"][frame_p[1]].replace("<cq>", f'"{cc}"')
    if form in ("CH-3", "CH-2"):
        return L.FRAMES["Q-CH"][frame_p[1]].replace("<c>", cc)
    if form == "CH-claim":
        return L.FRAMES["Q-claim"][frame_p[1]].replace("{OUT}", L.QCLAIM_FILL)
    if form == "CH-entity":
        return (L.FRAMES["Q-entity"][frame_p[1]].replace("{OUT}", L.QENTITY_FILL[frame_p[1]])
                .replace("<types>", types_pl).replace("<H>", H))
    raise ValueError(form)


def frame_of(form, rng):
    if form == "YN-F":
        fr = "Q-A" if rng.random() < 0.8 else "Q-B"
    elif form == "YN-R":
        fr = "Q-A" if rng.random() < 0.7 else "Q-B"
    elif form == "YN-O":
        fr = "Q-A"
    elif form in ("YN-nF", "YN-nR"):
        fr = "Q-B"
    elif form == "YN-dn":
        fr = "Q-D"
    elif form == "YN-T":
        fr = "Q-T"
    elif form in ("CH-3", "CH-2"):
        fr = "Q-CH"
    elif form == "CH-claim":
        fr = "Q-claim"
    else:
        fr = "Q-entity"
    return (fr, rng.randrange(3))
