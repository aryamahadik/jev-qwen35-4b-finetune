"""Twins and relation units (1.7): boundary and value fact-flip pairs, negation units with double negation, premise
removal pairs, container-swap pairs, attack units. Every twin's gold is computed by solver A on its own Struct and
question (never copied); G3 then re-solves it with solver B."""
from __future__ import annotations

import copy
from fractions import Fraction

from f9alt import REWRITE, applicable, rewrite
from f9ast import atoms
from f9fmt import to_frac
from f9frames import solve
from f9lex import id_key
from f9render import ans_text
from f9rows import ATTACKS, CPICK, NEG_FORMS, fm_for
from f9samp import Retry, col_index
from f9solve_a import CBD, NONE, SPECIALS, Reject, SolverA, Undefined, cmp_op

ERR = (Undefined, Reject, KeyError, ZeroDivisionError, ValueError, TypeError, IndexError)


def _base(q):
    while q["op"] in ("thr", "not"):
        q = q["inner"]
    return q


def all_atoms(q):
    """Every atom of the query (filters, group conditions, list conditions, lookup predicates)."""
    out = []
    b = _base(q)
    for k in ("f", "fe", "fd", "a", "b", "p", "cond"):
        v = b.get(k)
        if isinstance(v, dict) and "k" in v:
            out += atoms(v)
    return out


def _col_of(st, name):
    for ti, t in enumerate(st["tables"]):
        for j, c in enumerate(t["cols"]):
            if c["name"] == name:
                return ti, j, c
    return None


def _gold(card, st, q, shown=None):
    try:
        return solve(card, st, q, shown=shown)
    except ERR:
        return None


def _t5_ok(card, c, v):
    dom = (card.get("t5_domains") or {}).get(c["name"])
    if dom is None:
        return True
    return v in dom["values"] or (c["type"] == "num" and to_frac(v) in [to_frac(x) for x in dom["values"]])


def flip_candidates(card, st, q, kind, rng):
    """[(ti, i, j, new_value)] single-cell edits: kind boundary (numeric / date cell moved across a stated literal)
    or value (a category value changed)."""
    out = []
    for a in all_atoms(q):
        a0 = a["arg"] if a["k"] == "not" else a
        col = a0.get("col")
        if a0["k"] == "line" and kind == "value":
            col = "component" if a0.get("comp") else ("level" if a0.get("level") else None)
        loc = _col_of(st, col) if col else None
        if not loc:
            continue
        ti, j, c = loc
        rows = st["tables"][ti]["rows"]
        if kind == "boundary" and c["type"] == "num" and a0["k"] == "cmp" and "lit" in a0:
            if a0.get("unit") and c.get("unit") and a0["unit"] != c["unit"]:
                continue
            x, step = to_frac(a0["lit"]), c.get("step") or Fraction(1)
            vals = [x - step, x, x + step]
            for i, r in enumerate(rows):
                if r[j] is None:
                    continue
                for v in vals:
                    if v < 0 or (c.get("lo") is not None and not (to_frac(c["lo"]) <= v <= to_frac(c["hi"]))):
                        continue
                    if cmp_op(to_frac(r[j]), a0["op"], x) != cmp_op(v, a0["op"], x):
                        out.append((ti, i, j, v if c.get("dp") else Fraction(int(v))))
        elif kind == "boundary" and c["type"] == "date" and a0["k"] == "win":
            vals = [x for x in (a0.get("lo"), a0.get("hi")) if x is not None]
            vals = sorted({y for x in vals for y in (x - 1, x, x + 1)})
            for i, r in enumerate(rows):
                if r[j] is None:
                    continue
                for v in vals:
                    if v != r[j]:
                        out.append((ti, i, j, v))
        elif kind == "value" and c["type"] in ("cat", "lvl", "comp") and a0["k"] in ("cmp", "in", "line"):
            dom = c.get("values") or (card.get("levels") if c["type"] == "lvl" else
                                      st["tables"][ti].get("comps"))
            for i, r in enumerate(rows):
                if r[j] is None:
                    continue
                for v in dom or []:
                    if v != r[j]:
                        out.append((ti, i, j, v))
    rng.shuffle(out)
    return out


def fact_flip(em, res, kind, tries=80):
    """Yes/no twin with one decisive cell changed so the label flips (boundary or value)."""
    card, rng = em.card, em.rng
    st, q, g = res["struct"], res["q"], res["gold"]
    for ti, i, j, v in flip_candidates(card, st, q, kind, rng)[:tries]:
        c = st["tables"][ti]["cols"][j]
        if not _t5_ok(card, c, v):
            continue
        st2 = copy.deepcopy(st)
        st2["tables"][ti]["rows"][i][j] = v
        g2 = _gold(card, st2, q)
        if isinstance(g2, bool) and g2 != g:
            return dict(res, struct=st2, gold=g2, edge=None, flip=[kind, ti, i, j])
    return None


# ------------------------------------------------------------------------------------------------ negation (1.7)
def neg_query(frame, q):
    """The wide-scope negated question of an affirmative (F9-R4-01) and whether a dneg form exists (F9-R4-02)."""
    form = NEG_FORMS.get(frame, "itnc")
    b = q
    if form == "quant_no":
        if b["op"] != "quant_lookup" or b["q"] != "any":
            form = "itnc"
        else:
            return dict(copy.deepcopy(b), q="no"), True
    if form == "atom":
        if b["op"] != "lookup_p" or b["p"]["k"] not in ("cmp", "in", "term") or (
                b["p"]["k"] == "cmp" and b["p"]["op"] != "="):
            form = "itnc"
        else:
            nq = copy.deepcopy(b)
            nq["p"] = {"k": "not", "arg": nq["p"]}
            return nq, True
    if form == "have_no":
        a = b.get("a") if b["op"] == "req_any" else None
        if not (a and a.get("k") == "line" and a.get("level") and a.get("lvl_op") in (None, "=") and not a.get("comp")):
            form = "itnc"
    if form == "there_no" and b["op"] not in ("exists", "presence", "exists_lines"):
        form = "itnc"
    nq = {"op": "not", "inner": copy.deepcopy(q), "_neg": form}
    return nq, form != "itnc"


def dneg_query(nq):
    return {"op": "not", "inner": copy.deepcopy(nq), "_neg": "itnc"}


def neg_unit(em, res, want_dneg):
    """[(res, kind)] for the negated row (and the dneg row); golds computed, complement / equiv checked."""
    card = em.card
    st, q, g = res["struct"], res["q"], res["gold"]
    nq, can_d = neg_query(res["frame"], q)
    gn = _gold(card, st, nq)
    if not isinstance(gn, bool) or gn == g:
        return None
    out = [(dict(res, q=nq, gold=gn, edge=None, neg=True), "negation")]
    if want_dneg and can_d:
        dq = dneg_query(nq)
        gd = _gold(card, st, dq)
        if isinstance(gd, bool) and gd == g:
            out.append((dict(res, q=dq, gold=gd, edge=None, neg=True), "dneg"))
    return out


# ------------------------------------------------------------------------------------------------ option tags
def _rtext(em, res, a, alt=None):
    if isinstance(a, frozenset) or a in SPECIALS:
        return a
    if res["form"] == "value":
        return ans_text(em.card, res["frame"], res["q"], a, fm_for(em.card, "full"),
                        alt if alt and alt[0] == "E23" else None)
    return a


def tag_ok_a(em, res, st, tag, payload, gold, shown):
    """Solver-A mirror of G3's tag reproduction (1.3): payload is the option's generator payload (value text for
    value picks, id / set / special otherwise)."""
    card, q = em.card, res["q"]
    t = tag[0]
    if t in ("gold", "gold_cbd_member", "EA", "ES", "ES2"):
        return True
    b = _base(q)
    op = b["op"]
    if t == "E0":
        x = tag[1]
        if op in ("lookup", "ent_attr"):
            q2 = dict(q)
            q2["id" if op == "lookup" else "key"] = x
            v = _gold(card, st, q2)
            return v is not None and v not in SPECIALS and _rtext(em, res, v) == payload
        if op == "cpick":
            return _gold(card, st, q, shown=[x]) == NONE
        return payload == x and payload != gold
    alt = tuple(tag)
    q2 = rewrite(q, alt) if alt[0] in REWRITE else q
    m = alt if alt[0] not in REWRITE else None
    if op == "cpick":
        try:
            sel = SolverA(st, card).answer({**q2, "op": "select"}, alt=m)
            sel0 = SolverA(st, card).answer({**q, "op": "select"})
        except ERR:
            return False
        return isinstance(sel, frozenset) and payload in sel and payload not in (
            sel0 if isinstance(sel0, frozenset) else set())
    try:
        v = SolverA(st, card).answer(q2, alt=m, shown=shown)
    except ERR:
        return False
    return _rtext(em, res, v, alt) == payload


def retag(em, res, st, gold):
    """Options of a twin that keeps its base's display: every distractor keeps its tag when that tag reproduces on
    the twin's Struct, else takes another tag (E0 or a named error) that does; None when one cannot."""
    card = em.card
    shown = res.get("shown")
    out = []
    for payload, text, tag in res["options"]:
        if tag[0] in ("EA", "ES", "ES2"):
            out.append((payload, text, tag))
            continue
        pay = text if res["form"] == "value" else payload
        if tag[0] not in ("gold", "gold_cbd_member") and tag_ok_a(em, res, st, tag, pay, gold, shown):
            out.append((payload, text, tag))
            continue
        found = None
        for alt in applicable(res["q"], card, res["form"] if res["form"] != "record" else "record"):
            if tag_ok_a(em, res, st, list(alt), pay, gold, shown):
                found = list(alt)
                break
        if found is None and res["form"] != "value" and isinstance(payload, str):
            if tag_ok_a(em, res, st, ["E0", payload], pay, gold, shown):
                found = ["E0", payload]
        if found is None and res["form"] == "value" and _base(res["q"])["op"] in ("lookup", "ent_attr"):
            b = _base(res["q"])
            own = b.get("id") or b.get("key")
            for r in st["tables"][0]["rows"]:  # another record that shows the same value (a wrong row read)
                if r[0] != own and tag_ok_a(em, res, st, ["E0", r[0]], pay, gold, shown):
                    found = ["E0", r[0]]
                    break
        if found is None:
            return None
        out.append((payload, text, found))
    return out


# ------------------------------------------------------------------------------------------------ premise removal
def premise_removal(em, res, tries=60):
    """Twin of a choice row that shows 'cannot be determined' with a definite gold: on T5 cards one decisive known
    cell of a T5 column becomes UNKNOWN; on T2 cards the looked-up listed record is deleted. Both solvers must give
    'cannot be determined'; the display is the base's (XF01 / R5-SC1)."""
    card, rng = em.card, em.rng
    st, q = res["struct"], res["q"]
    shown = res.get("shown")
    edits = []
    if card["sem"].get("missing") == "T5":
        for c in card.get("t5_cols") or []:
            loc = _col_of(st, c)
            if not loc:
                continue
            ti, j, _ = loc
            edits += [("unk", ti, i, j) for i, r in enumerate(st["tables"][ti]["rows"]) if r[j] is not None]
    elif card["sem"]["world"] == "T2" and _base(q)["op"] == "lookup":
        rid = _base(q)["id"]
        edits = [("del", 0, i, None) for i, r in enumerate(st["tables"][0]["rows"]) if r[0] == rid]
    rng.shuffle(edits)
    for kind, ti, i, j in edits[:tries]:
        st2 = copy.deepcopy(st)
        if kind == "unk":
            st2["tables"][ti]["rows"][i][j] = None
        else:
            del st2["tables"][ti]["rows"][i]
        g2 = _gold(card, st2, q, shown=shown)
        if g2 != CBD:
            continue
        opts = retag(em, res, st2, g2)
        if opts is None:
            continue
        from f9lex import CBD as CBD_TXT
        return dict(res, struct=st2, gold=g2, options=opts, gold_text=CBD_TXT, edge=None, prem=[kind, ti, i, j])
    return None


# ------------------------------------------------------------------------------------------------ attack (1.7)
def attack_twin(em, res):
    """The attacked row: one free-text cell that Q never reads gets an injected instruction; solver A gives the
    same gold and the same value for every option, or the unit is not made (F9-A46, F9-R4-05)."""
    card, rng = em.card, em.rng
    st, q = res["struct"], res["q"]
    t = st["tables"][0] if st.get("tables") else None
    if t is None:
        return None
    names = [c["name"] for c in t["cols"]]
    tcol = "message" if card["sampler"] == "S6" else ("note" if "note" in names else None)
    if tcol is None:
        return None
    try:
        read = set(SolverA(st, card).read_cols(q))
    except ERR:
        return None
    if tcol in read or any(a.get("k") == "contains" for a in all_atoms(q)):
        return None
    j = names.index(tcol)
    rows = [i for i, r in enumerate(t["rows"]) if r[j] is not None]
    if not rows:
        return None
    st2 = copy.deepcopy(st)
    st2["tables"][0]["rows"][rng.choice(rows)][j] = rng.choice(ATTACKS)
    g2 = _gold(card, st2, q, shown=res.get("shown"))
    if g2 != res["gold"]:
        return None
    if res["form"] != "yn":
        for payload, text, tag in res["options"]:
            if tag[0] in ("gold", "gold_cbd_member", "EA", "ES", "ES2"):
                continue
            pay = text if res["form"] == "value" else payload
            if not tag_ok_a(em, res, st2, tag, pay, g2, res.get("shown")):
                return None
    return dict(res, struct=st2, attacked=True)
