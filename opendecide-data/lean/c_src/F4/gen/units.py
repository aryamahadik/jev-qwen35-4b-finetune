"""Selection units (G0 spec 6) and their rows: consistency triples, negation pairs, claim-negation pairs, contrast
twin sets, inert pairs, attack pairs and singles; choice forms CH-3, CH-2, CH-claim, CH-entity; layouts for S3
tables and S4 attributions; inert sentences (I1-I4) and verbatim carriers (V1-V4) (5.7); bait features that make
non-core rivals pivot (7.3 quotas)."""
from __future__ import annotations

import copy
import random
from decimal import Decimal

import core as C
import f4lex as L
import sampler as S
import solve_a as A

# ------------------------------------------------------------------------------------------------------- cloning


def clone(b: S.RB) -> S.RB:
    r, cp = b.r, b.cp
    b.r, b.cp = None, None
    try:
        b2 = copy.deepcopy(b)
    finally:
        b.r, b.cp = r, cp
    b2.r, b2.cp = r, cp
    return b2


def stmt_of(b: S.RB, e, p):
    for s in b.stmts:
        if s.kind == "lit" and s.e == e and s.pred == p:
            return s
    return None


def up_known(b: S.RB, card: C.Card):
    """Atoms determined in UP(T) under the card's flags (OW), for marker placement."""
    rec = S.to_record(b)
    v = C.base_view(rec, card, world=card.world or "OW")
    if (card.world or "OW") == "CW":
        return set()
    g = C.ground(v)
    assign, conf, _ = C.unit_propagate(g.units, g.clauses)
    return {a for a in assign if a[0] == "u"}


# ------------------------------------------------------------------------------------------------------- S3 tables

def layout_table(b: S.RB, card: C.Card, claim_atoms: set, rng, *, typ=None, closure_col=False, all_rows=False):
    """Move statements about entities of one type into a register table (5.3). Returns the table spec or None."""
    W = card.world or "OW"
    ents_by_t = {}
    for e, t in b.ents.items():
        ents_by_t.setdefault(t, []).append(e)
    if typ is None:
        typ = max(ents_by_t, key=lambda t: len(ents_by_t[t]))
    rows = sorted(ents_by_t.get(typ, []))
    if len(rows) < 2:
        return None
    known = up_known(b, card)
    derived = {r.head[0] for r in b.rules if r.head} | {r.ante for r in b.rules if r.ante}
    closed = {p for p, t, f, tid in b.closures}
    cols = []
    # predicate columns
    preds = sorted({s.pred for s in b.stmts if s.kind == "lit" and s.e in rows and s.via == "sent" and s.src is None
                    and s.pos is not None})
    for p in preds:
        if p in closed:
            continue
        cells = {}
        ok = True
        for e in rows:
            s = stmt_of(b, e, p)
            a = C.u(p, e)
            if s is not None and s.src is None and s.pos is not None:
                cells[e] = ("stated", s)
            elif s is not None:
                ok = False
                break
            else:
                if W == "CW":
                    if p in derived:
                        ok = False
                        break
                    cells[e] = ("addno", None)
                else:
                    if p in derived or p in b.exc_preds and card.unless == "listc" or a in known or \
                            a in claim_atoms or a in b.no_fact:
                        ok = False
                        break
                    cells[e] = ("marker", None)
        if not ok:
            continue
        cols.append(("pred", p, cells))
    # quantity / date columns
    for kind in ("val", "date"):
        keys = sorted({s.pred for s in b.stmts if s.kind == kind and s.e in rows and s.src is None})
        for q in keys:
            cells = {}
            ok = True
            for e in rows:
                s = next((x for x in b.stmts if x.kind == kind and x.e == e and x.pred == q), None)
                if s is not None and s.src is None:
                    cells[e] = ("stated", s)
                elif s is not None:
                    ok = False
                    break
                elif W == "CW":
                    ok = False
                    break
                else:
                    cells[e] = ("marker", None)
            if ok:
                cols.append(("qty" if kind == "val" else "date", q, cells))
    # link columns: only when every row names at least one partner
    for li in sorted({s.pred for s in b.stmts if s.kind == "link" and s.e in rows}):
        if all(any(s.kind == "link" and s.e == e and s.pred == li for s in b.stmts) for e in rows) and \
                rng.random() < 0.7:
            cols.append(("link", li, None))
    if closure_col and W == "OW":
        cands = [p for p in preds if p not in derived and p not in b.exc_preds and
                 all(C.u(p, e) not in claim_atoms for e in rows)]
        rng.shuffle(cands)
        for p in cands:
            if any(s.kind == "lit" and s.pred == p and s.src is not None for s in b.stmts):
                continue
            if any(h[2][0] == p or h[3][0] == p for h in b.hedges) or any(x[2] == p for x in b.ehedges):
                continue
            cols = [c for c in cols if not (c[0] == "pred" and c[1] == p)]
            cols.append(("closed", p, None))
            b.closures.append((p, typ, "column", "t1"))
            break
    if not cols:
        return None
    rng.shuffle(cols)
    tid = "t1"
    spec = {"tid": tid, "typ": typ, "rows": rows, "cols": []}
    for kind, key, cells in cols:
        spec["cols"].append((kind, key))
        if kind == "pred":
            for e, (how, s) in cells.items():
                if how == "stated":
                    s.via, s.tid = "cell", tid
                elif how == "addno":
                    st = C.Stmt(sid=b.sid(), kind="lit", e=e, pred=key, pos=False, via="cell", tid=tid)
                    b.stmts.append(st)
                else:
                    st = C.Stmt(sid=b.sid(), kind="lit", e=e, pred=key, pos=None, via="cell", tid=tid)
                    b.stmts.append(st)
        elif kind in ("qty", "date"):
            for e, (how, s) in cells.items():
                if how == "stated":
                    s.via, s.tid = "cell", tid
                else:
                    st = C.Stmt(sid=b.sid(), kind="val" if kind == "qty" else "date", e=e, pred=key, value=None,
                                via="cell", tid=tid)
                    b.stmts.append(st)
        elif kind == "link":
            for s in b.stmts:
                if s.kind == "link" and s.pred == key and s.e in rows:
                    s.via, s.tid = "cell", tid
        elif kind == "closed":
            for e in rows:
                s = stmt_of(b, e, key)
                if s is not None:
                    s.via, s.tid = "cell", tid
                else:
                    b.blank_cells.append((key, e, tid))
    return spec


# ------------------------------------------------------------------------------------------------------- S4 attributions

def layout_attrib(b: S.RB, card: C.Card, cp, rng, claim, *, want_v4=False, decisive=()):
    """Attribute statements to sources (5.4): decisive facts only through unattributed or trusted lines; untrusted
    lines carry bait (the claim or its negation, corroboration), never exception or closed predicates."""
    trusted, untrusted = cp.sources
    trust_list = card.trust and card.trust[0] == "list"
    closed = {p for p, t, f, tid in b.closures}
    tag = None
    for s in list(b.stmts):
        if s.kind not in ("lit", "val", "date") or s.via != "sent" or s.src is not None or s.pos is None and \
                s.kind == "lit":
            continue
        if rng.random() < 0.55:
            if trust_list:
                s.src = rng.choice(trusted)
            else:
                s.src = rng.choice(trusted + untrusted)
            s.frame = rng.choice(("colon", "colon", "quote", "reported"))
            s.no_cue = False
    if trust_list and untrusted:
        p, x, pos = claim
        if want_v4:
            v = pos if rng.random() < 0.5 else (not pos)
            st = C.Stmt(sid=b.sid(), kind="lit", e=x, pred=p, pos=v, src=rng.choice(untrusted),
                        frame=rng.choice(("colon", "quote", "reported")), tag="V4")
            b.stmts.append(st)
            tag = "V4"
        # corroboration / contradiction bait on other literals
        others = [s for s in b.stmts if s.kind == "lit" and s.pos is not None and s.pred not in b.exc_preds and
                  s.pred not in closed and s.src is None and s.via == "sent"]
        if others and rng.random() < 0.5:
            s0 = rng.choice(others)
            v = s0.pos if rng.random() < 0.5 else (not s0.pos)
            n = 2 if (rng.random() < 0.4 and len(untrusted) >= 2) else 1
            for src in rng.sample(list(untrusted), n):
                b.stmts.append(C.Stmt(sid=b.sid(), kind="lit", e=s0.e, pred=s0.pred, pos=v,
                                      src=src, frame=rng.choice(("colon", "reported"))))
        # an untrusted report about an atom no fact settles (R9 / R20 bait)
        free = [(p2, e) for p2, t in b.preds.items() for e, te in b.ents.items() if te == t and
                b.role.get(p2) != "exc" and p2 not in closed and stmt_of(b, e, p2) is None and
                C.u(p2, e) not in b.no_fact]
        if free and rng.random() < 0.6:
            p2, e = rng.choice(free)
            v = rng.random() < 0.6
            n = 2 if (rng.random() < 0.35 and len(untrusted) >= 2) else 1
            for src in rng.sample(list(untrusted), n):
                b.stmts.append(C.Stmt(sid=b.sid(), kind="lit", e=e, pred=p2, pos=v, src=src,
                                      frame=rng.choice(("colon", "quote", "reported"))))
    return tag


# ------------------------------------------------------------------------------------------------------- additions

def fresh_pred(b: S.RB, t):
    return b.pred(t, "base")


def add_inert(b: S.RB, cp, card, claim, kind, rng):
    """One inserted, relevant-looking inert sentence (5.7). Returns the kind."""
    p, x, pos = claim
    t = b.ents[x]
    if kind == "I1":
        q = fresh_pred(b, t)
        b.fact(x, q, rng.random() < 0.6, tag="I1")
    elif kind == "I2":
        a = fresh_pred(b, t)
        h = fresh_pred(b, t)
        r = b.rule(form="univ", typ=t, conds=(("lit", a, True),), head=(h, rng.random() < 0.7))
        r.style["inert"] = "I2"
    elif kind == "I3":
        tpl = rng.choice(L.BACKGROUND_TEMPLATES)
        doc = rng.choice(cp.pack["docs"]) if cp.pack["docs"] else "file"
        txt = tpl.format(X=x, doc=doc, types=cp.types[t][1])
        b.notes.setdefault("background", []).append(txt)
    elif kind == "I4":
        a = fresh_pred(b, t)
        hk = rng.choice(("most", "many", "usually", "often", "some"))
        b.hedges.append((hk, t, (a, True), (p, True)))
    return kind


def add_carrier(b: S.RB, cp, card, claim, kind, rng):
    p, x, pos = claim
    t = b.ents[x]
    if kind == "V1":
        b.ehedges.append((rng.choice(L.ENTITY_HEDGES), x, p))
    elif kind == "V2":
        b.notes["topic"] = (rng.choice(L.TOPIC_LABELS), claim)
    elif kind == "V3":
        partner = b.notes.get("look_partner")
        if partner is None:
            raise S.Fail("no_look_partner")
        b.ents[partner] = t
        b.fact(partner, p, pos, tag="V3")
    elif kind == "V4":
        trusted, untrusted = cp.sources
        b.stmts.append(C.Stmt(sid=b.sid(), kind="lit", e=x, pred=p, pos=pos if rng.random() < 0.5 else not pos,
                              src=rng.choice(untrusted), frame=rng.choice(("colon", "quote", "reported")), tag="V4"))
    return kind


def add_bait(b: S.RB, cp, card, claim, rng, label):
    """Rival-sensitive content on c's predicate that leaves the gold answer unchanged (validated by solver A)."""
    p, x, pos = claim
    t = b.ents[x]
    W = card.world or "OW"
    kinds = []
    if "exc" in cp.feats:
        kinds.append("exc_true")
    if "or" in cp.feats:
        kinds.append("xor_both")
    if "hedge" in cp.feats and W == "OW":
        kinds.append("hedge")
    if "onlyif" in cp.feats and W == "OW":
        kinds.append("onlyif")
    if "lookalike" in cp.feats and b.notes.get("look_partner") is None:
        kinds.append("look")
    if not kinds:
        return None
    k = rng.choice(kinds)
    if k == "exc_true":
        a = b.pred(t, "base")
        c = b.pred(t, "exc")
        hp = pos if rng.random() < 0.5 else (not pos)
        b.rule(form="univ", typ=t, conds=(("lit", a, True),), head=(p, hp), exc=c)
        b.fact(x, a, True)
        b.fact(x, c, True)
    elif k == "xor_both":
        a = b.pred(t, "base")
        a2 = b.pred(t, "base")
        b.rule(form="xor", typ=t, conds=(("lit", a, True), ("lit", a2, True)), head=(p, True))
        b.fact(x, a, True)
        b.fact(x, a2, True)
    elif k == "hedge":
        a = b.pred(t, "base")
        b.hedges.append((rng.choice(("most", "many", "usually", "often")), t, (a, True), (p, True)))
        b.fact(x, a, True)
    elif k == "onlyif":
        a = b.pred(t, "base")
        b.rule(form="onlyif", typ=t, conds=(("lit", a, True),), head=(a, True), ante=p)
        b.fact(x, a, True)
    elif k == "look":
        try:
            a2, b2 = b.look_pair(t)
        except S.Fail:
            return None
        q = b.pred(t, "base")
        b.fact(a2, q, True)
        b.fact(b2, p, rng.random() < 0.5)
    return k


# ------------------------------------------------------------------------------------------------------- record finish

def fill_cw_values(b: S.RB, rng):
    """CW: every value a rule reads is given (2.1). Entities with no value get one that fails the rule's condition."""
    import datetime as dt
    for r in b.rules:
        for c in r.conds:
            if c[0] in ("cmp", "rng"):
                q = next((x for x in b.cp.qtys if x["name"] == c[1]), None)
                if q is None:
                    continue
                step = Decimal(1).scaleb(-q["dec"])
                for e, t in sorted(b.ents.items()):
                    if (r.typ != t and not getattr(b, "ground_all", False)) or (e, c[1]) in b.vals:
                        continue
                    lo, hi = Decimal(str(q["lo"])), Decimal(str(q["hi"]))
                    for _ in range(40):
                        v = (lo + (hi - lo) * Decimal(str(rng.random()))).quantize(step)
                        if not S._eval_cond(c, v):
                            b.value(e, c[1], v)
                            break
            elif c[0] in ("dcmp", "win"):
                lo, hi = b.cp.window
                for e, t in sorted(b.ents.items()):
                    if r.typ != t or (e, c[1]) in b.dates:
                        continue
                    for _ in range(40):
                        v = lo + dt.timedelta(days=rng.randint(0, (hi - lo).days))
                        if not S._eval_cond(c, v):
                            b.date(e, c[1], v)
                            break


def finish(b: S.RB, cp, card, rng, *, s5_background=0):
    if (card.world or "OW") == "CW":
        fill_cw_values(b, rng)
    if getattr(cp, "rules_where", "record") == "card":
        for r in b.rules:
            r.where = "card"
    elif "standing" in cp.feats and not b.notes.get("_standing_done"):
        b.notes["_standing_done"] = True
        for r in b.rules:
            if r.form in ("univ", "neguniv") and len(r.conds) == 3 or r.form == "kofn" or r.style.get("pad"):
                continue
            if rng.random() < 0.5:
                r.where = "card"
    rec = S.to_record(b)
    bg = list(b.notes.get("background", []))
    if s5_background:
        pool_ = list(cp.pack["background"])
        rng.shuffle(pool_)
        for t in pool_[:s5_background]:
            bg.append(t)
        ents = sorted(b.ents)
        for _ in range(max(0, s5_background - len(pool_[:s5_background]))):
            tpl = rng.choice(L.BACKGROUND_TEMPLATES)
            e = rng.choice(ents)
            doc = rng.choice(cp.pack["docs"]) if cp.pack["docs"] else "file"
            bg.append(tpl.format(X=e, doc=doc, types=cp.types[b.ents[e]][1]))
    rec.extras["background"] = bg
    if b.notes.get("topic"):
        lab, cl = b.notes["topic"]
        import render_f4 as R
        rec.extras["topic"] = R.topic_line(lab, cl)
    if b.notes.get("inject"):
        rec.extras["inject"] = b.notes["inject"]
    rec.extras["tables"] = b.notes.get("tables", [])
    rec.blank_cells = list(b.blank_cells)
    return rec


def reserve_look(b: S.RB, t):
    """Make the row's subject one of a marked look-alike pair; the partner is kept for a V3 carrier or R16 bait."""
    for a, p in b.cp.looks:
        if a in b._ids and p in b._ids:
            b._ids.remove(a)
            b._ids.remove(p)
            b.ents[a] = t
            b.notes["look_partner"] = p
            return a
    raise S.Fail("looks")


def use_look_partner(b: S.RB):
    p = b.notes.get("look_partner")
    x = b.notes["claim"][1]
    if p is None:
        raise S.Fail("no_look_partner")
    if p not in b.ents:
        b.ents[p] = b.ents[x]
        b.lookalikes.append((x, p))
    return p


# ======================================================================================================= unit builder

YES_LABELS = {  # form -> (labels giving yes, labels giving no) in mapped terms (F/R/O)
    "YN-F": ("F", "RO"), "YN-dn": ("F", "RO"), "YN-R": ("R", "FO"), "YN-O": ("O", "FR"), "YN-T": ("F", "R"),
    "YN-nF": ("RO", "F"), "YN-nR": ("FO", "R"),
}


def pick_label(form, yes: bool, world, short, neg, rng):
    """Mapped label (F/R/O) for a yes/no form and target answer (7.5 label mixes; CW and short-card rules)."""
    ys, ns = YES_LABELS[form]
    pool_ = ys if yes else ns
    if world == "CW":
        pool_ = "".join(c for c in pool_ if c != "O")
    if short and (form in ("YN-R", "YN-nR") or neg):
        pool_ = "".join(c for c in pool_ if c != "O")
    if not pool_:
        raise S.Fail("label_pool")
    return rng.choice(pool_)


def cw_lab(m):
    return "T" if m == "F" else "F"


def base_record(cp, card, rng, spec, *, label, neg, depth, look=False, extra_pop=0, bait=True, matched=False):
    """Base sampled record for a unit (chain for c, distractors, bait, layout)."""
    W = card.world or "OW"
    tgt = {"world": W, "label": label if W == "OW" else cw_lab(label), "depth": depth, "neg": neg,
           "want": dict(spec.get("want", {})), "look": look}
    b, c, ch = S.make_base(cp, rng, tgt)
    b.notes["leaves"] = list(ch.leaves)
    x = c[1]
    if extra_pop:
        b.notes["pop"] = S.population(b, x, extra_pop, None, W, rng, matched=matched)
    if spec.get("shrink") or getattr(cp, "cls", "") in ("lean", "inv"):
        pass
    elif rng.random() < 0.6 and cp.sampler in ("S2",):
        S.irrelevant_rules(b, rng.randint(1, 2), rng)
    elif rng.random() < 0.3:
        S.irrelevant_rules(b, 1, rng)
    if bait and spec.get("bait"):
        b.notes["bait"] = add_bait(b, cp, card, c, rng, label)
    if look and spec.get("look_use") == "r16":
        p = use_look_partner(b)
        nm = b.near_miss[0] if b.near_miss else None
        leaves = b.notes["leaves"]
        try:
            if nm and nm[0][0] == "u" and nm[0][2] == x and label == "O":
                b.fact(p, nm[0][1], nm[1])
            elif leaves:
                a, v = rng.choice(leaves)
                if a[2] == x:
                    b.fact(p, a[1], not v)
        except S.Fail:
            pass
    return b, c


def apply_layout(b, cp, card, rng, claim_atoms, spec):
    if cp.sampler == "S3" or cp.inverted:
        tb = layout_table(b, card, claim_atoms, rng, typ=b.ents[b.notes["claim"][1]],
                          closure_col=("closure" in cp.feats and rng.random() < 0.5))
        if tb is None:
            raise S.Fail("no_table")
        b.notes["tables"] = [tb]
    if cp.sampler in ("S4", "S5") and "attrib" in cp.feats:
        # V4 names the addition target (the row's c, or on CH-claim rows the gold-independent target; repair r1)
        layout_attrib(b, card, cp, rng, b.notes.get("target") or b.notes["claim"],
                      want_v4=(spec.get("carrier") == "V4"))


def finish_rec(b, cp, card, rng):
    return finish(b, cp, card, rng, s5_background=(rng.randint(1, 3) if cp.sampler == "S5" else 0))


def analyze_row(rec, card, form, claim, c, b, *, options=None, H=None, none_shown=False, etyp=None):
    row = {"form": form, "claim": claim, "c": c}
    if form == "CH-claim":
        row.update({"options": options, "none_shown": none_shown})
    if form == "CH-entity":
        row.update({"options": options, "H": H, "etyp": etyp})
    res = A.analyze(rec, card, row, near_miss=b.near_miss)
    return row, res


def neg_claim(cl):
    return (cl[0], cl[1], not cl[2])


# ------------------------------------------------------------------------------------------------------- choice options

def ch_claim_options(b, cp, card, rng, c, k, none_shown, none_gold, gold_u=None, ents_ok=None):
    """k displayed options for a CH-claim row. Returns (options list with None for the None option, gold index or
    'NONE', distractor tags). ents_ok (repair r1, G7): distractor claims only about these entities (c's entity and
    its matched near-miss twins), so no option entity is mentioned more or less often because of its role."""
    W = card.world or "OW"
    rec = finish_rec(clone(b), cp, card, random.Random(rng.random()))
    view = C.base_view(rec, card, world=W)
    if W == "OW":
        g = C.ground(view)
        assign, conf, _ = C.unit_propagate(g.units, g.clauses)
        if conf:
            raise S.Fail("inconsistent")

        def lab(cl):
            return C.label_ow_up(g, A.claim_lit(cl))
    else:
        M, ok, _ = C.cw_model(view)
        if not ok:
            raise S.Fail("cw_inconsistent")

        def lab(cl):
            return "F" if C.cw_val(view, M, C.u(cl[0], cl[1])) == cl[2] else "R"
    preds_used = set()
    for r in rec.rules:
        preds_used.add(r.head[0])
        for cc in r.conds:
            if cc[0] == "lit":
                preds_used.add(cc[1])
        if r.pcond:
            preds_used.add(r.pcond[0])
        if r.ante:
            preds_used.add(r.ante)
    preds_used -= rec.exc_preds
    cands = []
    for e, t in rec.ents.items():
        if ents_ok is not None and e not in ents_ok:
            continue
        for p in sorted(preds_used):
            if rec.preds.get(p) != t:
                continue
            for pos in (True, False):
                cl = (p, e, pos)
                if cl == c or (none_gold and cl == c):
                    continue
                L_ = lab(cl)
                if L_ == "F":
                    continue
                if cp.short and L_ == "O" and not pos:
                    continue        # 7.4: on short cards every OPEN option is a positive claim
                cands.append((cl, L_))
    if cp.short and cands:
        # 7.4: short-card options must keep their answer under every reading the short card leaves open
        cl_map = {i: A.claim_lit(cl) for i, (cl, _) in enumerate(cands)}
        bad = set()
        views = [C.view_for(rec, card, "R1"), C.view_for(rec, card, "R3")]
        cwc = C.base_view(rec, card, world="CW")
        cwc.missing_false = True
        cwc.cw_mode = "conj"
        views.append(cwc)
        for v in views:
            for i, L_ in C.labels_for_view(v, cl_map).items():
                if L_ in ("F", "X"):
                    bad.add(i)
        ow = C.base_view(rec, card, world="OW")
        for i, cl in cl_map.items():
            if i not in bad and C.forward_label(ow, cl) == "F":
                bad.add(i)
        cands = [x for i, x in enumerate(cands) if i not in bad]
    rng.shuffle(cands)
    n_dis = k - (1 if not none_gold else 0) - (1 if none_shown else 0)
    if none_gold:
        n_dis -= 1      # c itself is shown as the designated distractor
    negs = [x for x in cands if not x[0][2]]
    poss = [x for x in cands if x[0][2]]
    pick = []
    # G10 "longest option is gold": a negated claim is longer, so distractors are negated at the gold's own rate
    # (CH-claim golds are negated on about 37% of rows); the count is drawn per row, then filled
    n_neg = sum(1 for _ in range(n_dis) if rng.random() < 0.37)
    if len(negs) < n_neg:
        raise S.Fail("few_neg_distractors")
    pick = [negs.pop() for _ in range(n_neg)]
    while len(pick) < n_dis and poss:
        pick.append(poss.pop())
    if len(pick) < n_dis:
        raise S.Fail("few_distractors")
    claims = [cl for cl, _ in pick] + [c]
    rng.shuffle(claims)
    opts = list(claims)
    if none_shown:
        opts.append(None)
    # gold slot uniform over the displayed slots (display drawn first; structure built for the gold class)
    order = list(range(len(opts)))
    rng.shuffle(order)
    opts = [opts[i] for i in order]
    if gold_u is not None:
        # 8: gold slot uniform per bucket; the plan hands each unit a stratified draw u, slot = floor(u * k)
        gi = opts.index(None) if none_gold else opts.index(c)
        tgt = min(len(opts) - 1, int(gold_u * len(opts)))
        opts[gi], opts[tgt] = opts[tgt], opts[gi]
    if none_gold:
        gold = "NONE"
    else:
        gold = opts.index(c)
    return opts, gold


# ------------------------------------------------------------------------------------------------------- units

# repair r2 (G10, G0 8 literal decisive decile within the rules block): a rules block of n < 10 rules can never put its
# last decisive rule in decile 9 (floor(10 (n-1) / n) <= 8), and with m >= 2 decisive rules never in decile 0. On PAD_RATE
# of the eligible units, drawn independently of the label and structure, the record's rule list is filled with
# irrelevant rules (predicates fresh, so outside c's component, as I2's logical form) up to a drawn total of 10-12 rules
# (G0 2.1: 2-12 rules per record). Pad rules use a type other than c's when the card has one, stay in the record (never
# moved to the card as standing rules) and are sampler-built structure, not the counted inert sentence (5.7).
# No pad on inverted cards, on CH-claim rows of lean cards (their option lists fill the length budget), on cards
# that print every rule, or on a second shrink retry; a first shrink retry pads to 10 rules.
PAD_RATE = 0.85
S3_TABLE_POP = 5


def _pad_rules(b: S.RB, cp, spec, rng, x):
    pad = rng.random() < PAD_RATE
    tot = rng.randint(10, 12)
    cls = getattr(cp, "cls", "")
    if not pad or (spec.get("shrink") or 0) >= 2 or cls == "inv" or \
            (cls == "lean" and spec["forms"][0] == "CH-claim") or getattr(cp, "rules_where", "record") == "card":
        return 0
    if spec.get("shrink"):
        tot = 10
    if spec.get("kind") == "inert":
        tot = min(tot, 11)    # the inert twin may add one I2 rule; 2.1 caps a record at 12 rules
    tx = b.ents[x]
    others = [i for i in range(len(cp.types)) if i != tx]
    before = len(b.rules)
    for _ in range(max(0, tot - before)):
        t = rng.choice(others) if others else tx
        try:
            a = b.pred(t, "base")
            h = b.pred(t, "derived")
        except S.Fail:
            break
        b.rule(form="univ", typ=t, conds=(("lit", a, True),), head=(h, rng.random() < 0.7))
    for r in b.rules[before:]:
        r.style["pad"] = True
    return len(b.rules) - before


def make_unit(cp, card, spec, rng):
    """Build all rows of one selection unit (sampled side, validated by solver A). Returns a list of drafts."""
    kind = spec["kind"]
    W = card.world or "OW"
    short = card.short
    forms = spec["forms"]
    f0 = forms[0]
    neg = spec["neg"]
    depth = spec["depth"]
    label = spec["label"]
    look = spec.get("carrier") == "V3" or spec.get("look_use") == "r16"
    drafts = []
    if f0 in ("CH-claim",):
        none_gold = spec["none_gold"]
        lab0 = "O" if none_gold else "F"
        if W == "CW" and none_gold:
            lab0 = "R"
        pop = max(1, spec["k"] // 3 - spec.get("shrink", 0))
        b, c = base_record(cp, card, rng, spec, label=lab0, neg=neg, depth=depth, look=look, extra_pop=pop,
                           bait=False, matched=True)
        # repair r1 (G7): the options are drawn first, on the bare record (c's entity and its matched near-miss
        # twins only); every addition (bait, verbatim carrier, inert sentence) then targets one claim option drawn
        # uniformly, independently of gold, so no option is named by an addition because it is gold
        ents_ok = {c[1]} | set(b.notes.get("pop", []))
        opts, gold = ch_claim_options(b, cp, card, rng, c, spec["k"], spec["none_shown"], none_gold,
                                      gold_u=spec.get("gold_u"), ents_ok=ents_ok)
        tgt = rng.choice([o for o in opts if o is not None])
        if spec.get("carrier") == "V3" and tgt[1] != c[1]:
            tgt, opts = _look_target(b, tgt, opts)
        b.notes["target"] = tgt
        if spec.get("bait"):
            b.notes["bait"] = add_bait(b, cp, card, tgt, rng, lab0)
        _additions(b, cp, card, rng, spec, tgt)
        _pad_rules(b, cp, spec, rng, c[1])
        claim_atoms = {C.u(c[0], c[1])}
        b_pre = clone(b)
        lseed = rng.random()
        apply_layout(b, cp, card, random.Random(lseed), claim_atoms, spec)
        rec = finish_rec(b, cp, card, random.Random(lseed + 1))
        row, res = analyze_row(rec, card, "CH-claim", None, c, b, options=opts, none_shown=spec["none_shown"])
        if not res["ok"]:
            raise S.Fail("a:" + res["why"])
        if str(res["gold"]) != str(gold):
            raise S.Fail("ch_claim_gold")
        drafts.append({"rec": rec, "row": row, "res": res, "role": "base", "b": b, "b_pre": b_pre,
                       "lseed": lseed})
    elif f0 == "CH-entity":
        b, c, rec, row, res, b_pre, lseed = _ch_entity(cp, card, rng, spec)
        drafts.append({"rec": rec, "row": row, "res": res, "role": "base", "b": b, "b_pre": b_pre,
                       "lseed": lseed})
    else:
        pop_ = 0 if spec.get("shrink") else rng.choice((0, 1, 1, 2))
        if cp.sampler == "S3":
            # repair r2 (G10 literal decile within the table block): tables of 2-5 rows reach only a few deciles
            # (n = 2: {0, 5}), so S3 records carry >= S3_TABLE_POP near-miss entities of c's type (label-independent)
            # (not on cards that print every rule: their single-table styles need a table-only record)
            grow = not spec.get("shrink") and getattr(cp, "rules_where", "record") != "card"
            pop_ = max(S3_TABLE_POP, pop_) if grow else max(1, pop_)
        b, c = base_record(cp, card, rng, spec, label=label, neg=neg, depth=depth, look=look, extra_pop=pop_)
        _additions(b, cp, card, rng, spec, c)
        _pad_rules(b, cp, spec, rng, c[1])
        claim_atoms = {C.u(c[0], c[1])}
        b_pre = clone(b)
        lseed = rng.random()
        apply_layout(b, cp, card, random.Random(lseed), claim_atoms, spec)
        rec = finish_rec(b, cp, card, random.Random(lseed + 1))
        for i, f in enumerate(forms):
            cl = c
            if kind == "claimneg" and i == 1:
                cl = neg_claim(c)
            row, res = analyze_row(rec, card, f, cl, c, b)
            if not res["ok"]:
                raise S.Fail("a:" + res["why"])
            role = "base" if i == 0 else "variant"
            drafts.append({"rec": rec, "row": row, "res": res, "role": role, "b": b, "b_pre": b_pre,
                           "lseed": lseed})
        # check the base label target
        lab_c = drafts[0]["res"]["label_c"]
        if lab_c != label:
            raise S.Fail("label_mismatch")
        if f0 in ("CH-3", "CH-2"):
            drafts[0]["row"]["opt_labels"] = None
    # relation-unit specific checks and twins
    if kind == "contrast":
        twins = _contrast_twins(cp, card, rng, spec, drafts[0])
        drafts.extend(twins)
    elif kind == "inert":
        drafts.append(_inert_twin(cp, card, rng, spec, drafts[0]))
    elif kind == "attack":
        drafts.append(_attack_twin(cp, card, rng, spec, drafts[0]))
    for d in drafts:
        d["unit_kind"] = kind
    return drafts


def _look_target(b, tgt, opts):
    """V3 on a CH-claim row whose (gold-independent) target is a near-miss twin z of c's entity: z takes the ID of
    a free look-alike pair (a renaming, label-preserving by MR1), so the V3 fact is about z's own look-alike."""
    z = tgt[1]
    for a, pp in b.cp.looks:
        if a in b._ids and pp in b._ids and a not in b.ents and pp not in b.ents:
            b._ids.remove(a)
            b._ids.remove(pp)
            _rename_ent(b, z, a)
            b.notes["look_partner_t"] = pp
            opts = [None if o is None else ((o[0], a, o[2]) if o[1] == z else o) for o in opts]
            return (tgt[0], a, tgt[2]), opts
    raise S.Fail("looks_v3_target")


def _rename_ent(b, old, new):
    b.ents[new] = b.ents.pop(old)
    for st in b.stmts:
        if st.e == old:
            st.e = new
        if st.kind == "link" and st.value == old:
            st.value = new
    b.vals = {((new if e == old else e), q): v for (e, q), v in b.vals.items()}
    b.dates = {((new if e == old else e), q): v for (e, q), v in b.dates.items()}
    b.links = {(li, new if a == old else a, new if y == old else y) for li, a, y in b.links}
    if b.notes.get("pop"):
        b.notes["pop"] = [new if e == old else e for e in b.notes["pop"]]


def _additions(b, cp, card, rng, spec, c):
    """Carrier and inert sentence for the row. c is the addition target: the row's c on yes/no, CH-3 and CH-2 rows;
    on CH-claim rows a claim option drawn independently of gold (repair r1)."""
    if spec.get("carrier"):
        if spec["carrier"] == "V3":
            if b.notes.get("look_partner_t") and c[1] != b.notes["claim"][1]:
                p = b.notes["look_partner_t"]
                b.ents[p] = b.ents[c[1]]
                b.lookalikes.append((c[1], p))
            else:
                p = use_look_partner(b)
            b.fact(p, c[0], c[2], tag="V3")
        elif spec["carrier"] != "V4":
            add_carrier(b, cp, card, c, spec["carrier"], rng)
    if spec.get("inert") and spec["kind"] != "inert":
        add_inert(b, cp, card, c, spec["inert"], rng)


def _relayout(cp, card, b2, spec, lseed):
    claim = b2.notes["claim"]
    apply_layout(b2, cp, card, random.Random(lseed), {C.u(claim[0], claim[1])}, spec)
    return finish_rec(b2, cp, card, random.Random(lseed + 1))


def _decisive_leaves(d):
    """Leaf premises of the base derivation (facts / closure units) that a twin may change."""
    res = d["res"]
    out = []
    for lit in res.get("leaves", []):
        out.append(lit)
    return out


def _contrast_twins(cp, card, rng, spec, d0):
    """1-2 record-side twins whose gold answer differs from the base (6; XF03)."""
    W = card.world or "OW"
    b0 = d0["b_pre"]
    lseed = d0["lseed"]
    base_gold = str(d0["res"]["gold"])
    c = b0.notes["claim"]
    form = d0["row"]["form"]
    lab = d0["res"]["label_c"]
    cands = []
    leaves = [l for l in d0["res"].get("leaves", []) if l[0][0] == "u"]
    cmp_leaves = [l for l in d0["res"].get("leaves", []) if l[0][0] in ("c", "r", "d", "w")]
    if lab in ("F", "R") or (W == "CW" and lab == "F" and c[2]) or (W == "CW"):
        for (a, v) in leaves:
            cands.append(("premise_removed", a, v))
            cands.append(("fact_flip", a, v))
    for nm in b0.near_miss:
        cands.append(("fact_flip_nm", nm[0], nm[1]))
    decided = d0["res"].get("derivation")
    for s in b0.stmts:
        if decided and s.kind == "val" and s.value is not None:
            cands.append(("value_flip", s, None))
        if decided and s.kind == "date" and s.value is not None:
            cands.append(("date_shift", s, None))
        if s.kind == "lit" and s.pred in b0.exc_preds and s.pos is not None:
            cands.append(("exception_toggle", s, None))
    if not leaves:
        for (a, v) in b0.notes.get("leaves", []):
            if a[0] == "u":
                cands.append(("fact_flip", a, v))
                if W == "OW":
                    cands.append(("premise_removed", a, v))
    for i, cl in enumerate(b0.closures):
        cands.append(("closure_toggle", i, None))
    rng.shuffle(cands)
    cands.sort(key=lambda x: {"value_flip": 1, "date_shift": 1}.get(x[0], 0) if x[1] is not None and
               not (hasattr(x[1], "e") and x[1].e == c[1]) else 0)
    want = spec.get("twin_n", 1)
    out = []
    late = []
    used = set()
    for kind, a, v in cands:
        if len(out) >= want:
            break
        if kind in used and len(cands) > want:
            continue
        b2 = clone(b0)
        try:
            tk = _modify(b2, kind, a, v, W, card, rng)
        except S.Fail:
            continue
        if tk is None:
            continue
        try:
            rec2 = _relayout(cp, card, b2, spec, lseed)
        except S.Fail:
            continue
        row2, res2 = analyze_row(rec2, card, form, c, c, b2)
        if not res2["ok"] or str(res2["gold"]) == base_gold:
            continue
        if form in ("CH-3",) and res2["gold"] == base_gold:
            continue
        # 2.3: no d1 rows, and a twin never goes deeper than the plan's cap (4) or its base
        if not (2 <= res2["depth"] <= max(4, d0["res"]["depth"])):
            continue
        # G10 balance on CH-3 ("longest option is gold"): most twins of a decided base land on OPEN, so an OPEN twin
        # of a decided base is kept only part of the time while another candidate remains
        if form == "CH-3" and res2["label_c"] == "O" and lab != "O":
            late.append({"rec": rec2, "row": row2, "res": res2, "role": "twin", "b": b2, "twin_kind": tk})
            if rng.random() < 0.9:
                continue
        used.add(kind)
        out.append({"rec": rec2, "row": row2, "res": res2, "role": "twin", "b": b2, "twin_kind": tk})
    if len(out) < 1 and late:
        out.append(late[0])
    if len(out) < 1:
        raise S.Fail("no_contrast_twin")
    return out


def _modify(b2, kind, a, v, W, card, rng):
    if kind == "premise_removed":
        if W != "OW":
            return None
        s = stmt_of(b2, a[2], a[1])
        if s is None or s.src is not None and False:
            return None
        b2.stmts = [x for x in b2.stmts if x is not s]
        b2.no_fact.add(a)
        b2.near_miss.append((a, v))
        return "premise_removed"
    if kind == "fact_flip":
        s = stmt_of(b2, a[2], a[1])
        if s is None or s.pos is None:
            return None
        s.pos = not s.pos
        b2.near_miss.append((a, not s.pos))
        return "fact_flip"
    if kind == "fact_flip_nm":
        if a[0] != "u":
            return None
        s = stmt_of(b2, a[2], a[1])
        if s is not None:
            s.pos = v
        else:
            b2.no_fact.discard(a)
            b2.fact(a[2], a[1], v)
        return "fact_flip"
    if kind == "value_flip":
        s = next((x for x in b2.stmts if x.kind == "val" and x.e == a.e and x.pred == a.pred), None)
        if s is None:
            return None
        q = next(q for q in b2.cp.qtys if q["name"] == s.pred)
        step = Decimal(1).scaleb(-q["dec"])
        conds = [cc for r in b2.rules for cc in r.conds if cc[0] in ("cmp", "rng") and cc[1] == s.pred]
        if not conds:
            return None
        cc = conds[0]
        if cc[0] == "cmp":
            T = cc[3]
            cand = [T - step, T, T + step]
        else:
            cand = [cc[2] - step, cc[2], cc[3], cc[3] + step]
        cur = S._eval_cond(cc, s.value)
        alt = [x for x in cand if S._eval_cond(cc, x) != cur]
        if not alt:
            return None
        old_v = s.value
        s.value = rng.choice(alt)
        b2.vals[(s.e, s.pred)] = s.value
        b2.near_miss.append((("V", s.e, s.pred, old_v), True))
        return "value_flip"
    if kind == "date_shift":
        s = next((x for x in b2.stmts if x.kind == "date" and x.e == a.e and x.pred == a.pred), None)
        if s is None:
            return None
        conds = [cc for r in b2.rules for cc in r.conds if cc[0] in ("dcmp", "win") and cc[1] == s.pred]
        if not conds:
            return None
        cc = conds[0]
        import datetime as dt
        one = dt.timedelta(days=1)
        cand = [cc[3] - one, cc[3], cc[3] + one] if cc[0] == "dcmp" else [cc[2] - one, cc[2], cc[3], cc[3] + one]
        cur = S._eval_cond(cc, s.value)
        alt = [x for x in cand if S._eval_cond(cc, x) != cur]
        if not alt:
            return None
        old_v = s.value
        s.value = rng.choice(alt)
        b2.dates[(s.e, s.pred)] = s.value
        b2.near_miss.append((("D", s.e, s.pred, old_v), True))
        return "date_shift"
    if kind == "exception_toggle":
        s = next((x for x in b2.stmts if x.kind == "lit" and x.e == a.e and x.pred == a.pred and x.pos is not None),
                 None)
        if s is None:
            return None
        if W == "OW" and card.unless == "strict" and rng.random() < 0.4:
            b2.stmts = [x for x in b2.stmts if x is not s]
        else:
            s.pos = not s.pos
        return "exception_toggle"
    if kind == "closure_toggle":
        if W != "OW" or a >= len(b2.closures) or b2.closures[a][2] != "prose":
            return None
        del b2.closures[a]
        return "closure_toggle"
    return None


def _inert_twin(cp, card, rng, spec, d0):
    b2 = clone(d0["b_pre"])
    c = b2.notes["claim"]
    kinds = ["I1", "I2", "I3"] + (["I4"] if (card.world == "OW" and "hedge" in cp.feats) else [])
    k = spec.get("inert") or rng.choice(kinds)
    # repair r1 (G7): on choice rows with claim or entity options the inserted sentence targets an option drawn
    # independently of gold (CH-claim: the unit's addition target; CH-entity: a uniformly drawn listed entity)
    tgt = c
    form0 = d0["row"]["form"]
    if form0 == "CH-claim":
        tgt = b2.notes.get("target") or c
    elif form0 == "CH-entity":
        tgt = (c[0], rng.choice(list(d0["row"]["options"])), True)
    add_inert(b2, cp, card, tgt, k, rng)
    rec2 = _relayout(cp, card, b2, spec, d0["lseed"])
    row2, res2 = analyze_row(rec2, card, d0["row"]["form"], d0["row"]["claim"], c, b2,
                             options=d0["row"].get("options"), H=d0["row"].get("H"),
                             none_shown=d0["row"].get("none_shown", False), etyp=d0["row"].get("etyp"))
    if not res2["ok"] or str(res2["gold"]) != str(d0["res"]["gold"]) or res2["label_c"] != d0["res"]["label_c"]:
        raise S.Fail("inert_changed")
    return {"rec": rec2, "row": row2, "res": res2, "role": "variant", "b": b2, "inert_kind": k,
            "twin_kind": "inert"}


def _attack_twin(cp, card, rng, spec, d0):
    rec2 = copy.copy(d0["rec"])
    rec2.extras = dict(d0["rec"].extras)
    yn = d0["row"]["form"].startswith("YN")
    ans = rng.choice(L.ATTACK_ANS_YN if yn else L.ATTACK_ANS_CH)
    rec2.extras["inject"] = rng.choice(L.ATTACKS).format(ANS=ans)
    return {"rec": rec2, "row": dict(d0["row"]), "res": d0["res"], "role": "attacked", "b": d0["b"],
            "twin_kind": "attack"}


def _ch_entity(cp, card, rng, spec):
    W = card.world or "OW"
    k = spec["k"]
    b, c = base_record(cp, card, rng, spec, label="F", neg=False, depth=spec["depth"], extra_pop=0, bait=False)
    x = c[1]
    S.population(b, x, k - 1, None, W, rng, matched=True, detail=False)
    t = b.ents[x]
    claim_atoms = {C.u(c[0], e) for e, te in b.ents.items() if te == t}
    b_pre = clone(b)
    lseed = rng.random()
    apply_layout(b, cp, card, random.Random(lseed), claim_atoms, spec)
    tb = b.notes["tables"][0]
    if len(tb["rows"]) != k:
        raise S.Fail("ch_entity_k")
    rec = finish_rec(b, cp, card, random.Random(lseed + 1))
    opts = list(tb["rows"])
    rng.shuffle(opts)
    if spec.get("gold_u") is not None:
        gi, tgt = opts.index(x), min(len(opts) - 1, int(spec["gold_u"] * len(opts)))
        opts[gi], opts[tgt] = opts[tgt], opts[gi]
    row, res = analyze_row(rec, card, "CH-entity", None, c, b, options=opts, H=c[0], etyp=t)
    if not res["ok"]:
        raise S.Fail("a:" + res["why"])
    if res["gold"] != opts.index(x):
        raise S.Fail("ch_entity_gold")
    return b, c, rec, row, res, b_pre, lseed
