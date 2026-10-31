"""S4 multi-table report (G0 4.4) and the small periodic tables of S2 / S6 Q-T rows: solver A semantics (SEM-22,
SEM-38, SEM-43, SEM-44, SEM-34 for exclusions, S4 criteria) and table-first samplers. Same contract as f13_samplers.

Model (f13_model schema additions):
  table section: sec["period"] = [D1, D2] (stated once in the body of an unsplit table or of part 1; continued parts
                 state none), sec["scope"] = unit (section mark); one fact
  table {ft, name, part: None | k, cols: ["id", "cat"?, <measure names>..., "date"?], rows: [[cell, ...]],
         total: None | int (part total of the table's summed measure `tmeas`), tmeas: measure | None}
        cells: id "PRE-1234", category value, int or TRACE, ISO date
  crit  {ft, rid, conds: [atom], join, outcome, eff}       S4 criterion: one version, no end date (F13R3-11)
  excl  {ft, xid, noun, eid, scope, status, eff, end}       exclusion (window item; counted, never applied)
Query: {qk: tq_count | tq_argmax | tq_cmp | tq_set | ag3_sum | ag3_count | tp_outcome | ag1_excl, table, unit,
        period [D1, D2], measure, op, thr, ent, ent2, date (ag1_excl), form, shown, claim, ...}
A table is selected by (name, unit, period): its unsplit section, or part 1 with that period plus every continued
part of the same name and unit.
"""
from __future__ import annotations

import itertools

import f13_base as B
import f13_model as M
from f13_samplers import Ctx, _why

TRACE = M.TRACE
UNDET = M.UNDET
TAB_QK = ("tq_count", "tq_argmax", "tq_cmp", "tq_crit", "tq_set", "ag3_sum", "ag3_count", "tp_outcome", "ag1_excl")
OPS = {"ge": lambda a, b: a >= b, "le": lambda a, b: a <= b, "gt": lambda a, b: a > b, "lt": lambda a, b: a < b}
NAMES = "ABCDEFGH"


# ================================================================================================ solver A
def _parts(doc, name, unit, period):
    """Sections of table (name, unit, period), part order; None when the selection is not one table."""
    first, cont = [], []
    for s in doc["sections"]:
        for f in s["facts"]:
            if f["ft"] != "table" or f["name"] != name or s.get("scope") != unit:
                continue
            if f["part"] in (None, 1):
                if s.get("period") == list(period):
                    first.append((s, f))
            else:
                cont.append((s, f))
    if len(first) != 1:
        return None
    s0, f0 = first[0]
    if f0["part"] is None:
        return [f0]
    # continued parts belong to the one split table of this name and unit
    splits = [f for s in doc["sections"] for f in s["facts"] if f["ft"] == "table" and f["name"] == name and
              s.get("scope") == unit and f["part"] == 1]
    if len(splits) != 1:
        return None
    return [f0] + sorted((f for _, f in cont), key=lambda f: f["part"])


def _rows(parts, measure):
    out = []
    for f in parts:
        if measure not in f["cols"]:
            return None
        ci = f["cols"].index(measure)
        di = f["cols"].index("date") if "date" in f["cols"] else None
        for row in f["rows"]:
            out.append((row[0], row[ci], row[di] if di is not None else None))
    return out


def _argmax(rows, tie):
    best = max(v for _, v, _ in rows)
    top = [r for r in rows if r[1] == best]
    if len(top) == 1:
        return top[0][0]
    if tie is None:
        return UNDET
    key = (lambda r: r[2]) if tie == "date" else (lambda r: r[0])
    top.sort(key=key)
    if key(top[0]) == key(top[1]):
        return UNDET
    return top[0][0]


def tab_core(doc):
    q, card = doc["query"], doc["card"]
    qk = q["qk"]
    if qk == "ag1_excl":
        on = M.d_(q["date"])
        return sum(1 for s in doc["sections"] for f in s["facts"] if f["ft"] == "excl" and f["scope"] == q["unit"]
                   and M.window_in_force(f["eff"], f["end"], f["status"], on))
    if qk == "tp_outcome":
        return tp_outcome(doc, q["ent"], q["period"])
    parts = _parts(doc, q["table"], q["unit"], q["period"])
    if parts is None:
        return UNDET
    if qk == "ag3_sum":
        if any(f["total"] is None for f in parts):
            return UNDET
        return sum(f["total"] for f in parts)
    rows = _rows(parts, q["measure"])
    if rows is None or not rows:
        return UNDET
    if qk in ("tq_count", "ag3_count"):
        return sum(1 for _, v, _ in rows if OPS[q["op"]](v, q["thr"]))
    if qk == "tq_set":
        return frozenset(e for e, v, _ in rows if OPS[q["op"]](v, q["thr"]))
    if qk == "tq_argmax":
        return _argmax(rows, card.get("tie"))
    if qk == "tq_cmp":
        d = {e: v for e, v, _ in rows}
        if q["ent"] not in d or q["ent2"] not in d:
            return UNDET
        return q["ent"] if d[q["ent"]] > d[q["ent2"]] else "__NOT__"
    if qk == "tq_crit":  # repair r6: criterion claim on one entity (slot-polar Q-T yes/no)
        d = {e: v for e, v, _ in rows}
        if q["ent"] not in d:
            return UNDET
        return q["ent"] if OPS[q["op"]](d[q["ent"]], q["thr"]) else "__NOT__"
    raise ValueError(qk)


def tab_argmax_top(doc):
    """tq_argmax: the records left at the top after the card's tie rule (one when the answer is decided; the records
    the rule cannot split otherwise); None when the selection has no answer (not one table, measure missing).
    G2 fix r1 (claim truth on settle / establish rows, SEM-04 / SEM-22)."""
    q, card = doc["query"], doc["card"]
    parts = _parts(doc, q["table"], q["unit"], q["period"])
    rows = None if parts is None else _rows(parts, q["measure"])
    if not rows:
        return None
    best = max(v for _, v, _ in rows)
    top = [r for r in rows if r[1] == best]
    tie = card.get("tie")
    if len(top) > 1 and tie is not None:
        key = (lambda r: r[2]) if tie == "date" else (lambda r: r[0])
        k0 = min(key(r) for r in top)
        top = [r for r in top if key(r) == k0]
    return frozenset(r[0] for r in top)


def tp_outcome(doc, ent, period):
    """S4 Q-P (F13R3-11): the report's criteria applied to the entity's one row in the tables of the named period."""
    card = doc["card"]
    hits = []
    for s in doc["sections"]:
        if s.get("period") != list(period):
            continue
        for f in s["facts"]:
            if f["ft"] == "table" and f["part"] is None:
                for row in f["rows"]:
                    if row[0] == ent:
                        hits.append(dict(zip(f["cols"], row)))
    if len(hits) != 1:
        return UNDET
    attrs = hits[0]
    fired = []
    for s in doc["sections"]:
        for f in s["facts"]:
            if f["ft"] == "crit" and M.d_(f["eff"]) <= M.d_(period[0]):
                if any(a["attr"] not in attrs for a in f["conds"]):
                    continue
                if M.eval_conds(f["conds"], f["join"], attrs):
                    fired.append(f)
    if not fired:
        return card["default"]
    best = max(f["eff"] for f in fired) if card["precedence"] == "later" else None
    tier = [f for f in fired if best is None or f["eff"] == best]
    outs = {f["outcome"] for f in tier}
    return outs.pop() if len(outs) == 1 else M.CONFLICT


def tab_completions(doc):
    """Traced cells of tables: per cell, the critical points of the predicates that read its column (2.4 exact
    finite check): the queried measure (threshold, every other stated value of the column) or a criterion attribute
    (its constants); a column no predicate reads takes one point."""
    import copy
    q = doc["query"]
    crit = {}
    for s in doc["sections"]:
        for f in s["facts"]:
            if f["ft"] == "crit":
                for a in f["conds"]:
                    crit.setdefault(a["attr"], []).append(a["val"])
    slots = []
    for si, s in enumerate(doc["sections"]):
        for fi, f in enumerate(s["facts"]):
            if f["ft"] != "table":
                continue
            for ri, row in enumerate(f["rows"]):
                for ci, v in enumerate(row):
                    if v == TRACE:
                        col = f["cols"][ci]
                        if col == q.get("measure"):
                            vals = [x[ci] for x in f["rows"] if isinstance(x[ci], int)]
                            vals += [x[g.index(col)] for s2 in doc["sections"] for g0 in s2["facts"]
                                     if g0["ft"] == "table" and g0 is not f and col in g0["cols"]
                                     for g in [g0["cols"]] for x in g0["rows"] if isinstance(x[g.index(col)], int)]
                            vals += [q["thr"]] if q.get("thr") is not None else []
                        elif col in crit:
                            vals = crit[col]
                        else:
                            slots.append((si, fi, ri, ci, [0]))
                            continue
                        pts = {0, max(vals + [0]) + 100}
                        for x in vals:
                            pts.update(y for y in (x - 1, x, x + 1) if y >= 0)
                        slots.append((si, fi, ri, ci, sorted(pts)))
    if not slots:
        return [doc]
    out = []
    for combo in itertools.product(*[sl[4] for sl in slots]):
        d2 = dict(doc)
        d2["sections"] = list(doc["sections"])
        for (si, fi, ri, ci, _), v in zip(slots, combo):
            sec = dict(d2["sections"][si])
            sec["facts"] = list(sec["facts"])
            f = dict(sec["facts"][fi])
            f["rows"] = [list(x) for x in f["rows"]]
            f["rows"][ri][ci] = v
            sec["facts"][fi] = f
            d2["sections"][si] = sec
        out.append(d2)
    return out


def tab_activate(d2, sec, nm):
    q = d2["query"]
    if nm["kind"] == "V" and nm.get("sub") == "period":
        q["period"] = list(nm["period"])
    elif nm["kind"] == "V":
        f = next(x for x in sec["facts"] if x.get("xid") == nm["xid"])
        f["status"] = "in force"
        if nm.get("new_eff"):
            f["eff"] = nm["new_eff"]
    elif nm["kind"] == "R":
        q["unit"] = nm["unit"]
    elif nm["kind"] == "I":
        q["ent"] = nm["id"]


def tab_witness(doc, sec):
    """T-D part completions besides {empty, original}: the part's own label type (rows of its table) as one row per
    entity of the original part with the measure at 0 and at a high value."""
    return []


# ================================================================================================ cards
def tab_card(card, pack):
    r = B.rng("f13-tabcard", card["card_id"])
    ent = pack["ents"][0]
    card["tab"] = True
    card["ent_prefix"] = ent["prefix"]
    card["plural"] = ent["plural"]
    nums = [a for a in card["attrs"]]
    card["measures"] = nums[:4]
    card["cat"] = pack["cats"][0] if pack["cats"] else None
    if card["sampler"] == "S4":
        card["tie"] = ("date", "number", None)[card_no(card) % 3]
        card["fact_kinds"] = ["table", "table row", "criterion", "exclusion"]
        card["scoped_kinds"] = ["table", "exclusion"]
        card["has_case"] = False
        card["inverted"] = False
    else:
        card["tie"] = None
    card["tie_date"] = "record date"
    return card


def card_no(card):
    return int(card["card_id"].split("-c")[-1])


# ================================================================================================ helpers
def _sec(c, heading, role, facts, scope=None, period=None, **kw):
    c.sec_no += 1
    s = {"sid": f"s{c.sec_no:02d}", "heading": heading.format(n=c.sec_no + 1), "kind": "tab", "scope": scope,
         "role": role, "facts": facts, "trace": None}
    if period:
        s["period"] = list(period)
    s.update(kw)
    return s


HEADS = ("Statistical return {n}", "Report section {n}", "Data annex {n}", "Return {n}", "Tabulation {n}")


def _periods(c):
    """Current period and the prior period (consecutive, about one quarter each)."""
    d1 = B.add_days(c.base, c.r.randint(400, 600))
    ln = c.r.choice([30, 59, 90, 91])
    d2 = B.add_days(d1, ln)
    p0 = [B.add_days(d1, -(ln + 1)).isoformat(), B.add_days(d1, -1).isoformat()]
    return [d1.isoformat(), d2.isoformat()], p0


def _cols(card, measures, with_date):
    cols = ["id"]
    if card.get("cat"):
        cols.append("cat")
    cols += [m["name"] for m in measures]
    if with_date:
        cols.append("date")
    return cols


def _row(c, card, eid, cols, period, fixed=None):
    fixed = fixed or {}
    mm = {m["name"]: m for m in card["measures"]}
    row = []
    for k in cols:
        if k in fixed:
            row.append(fixed[k])
        elif k == "id":
            row.append(eid)
        elif k == "cat":
            row.append(c.r.choice(card["cat"]["values"]))
        elif k == "date":
            row.append(B.add_days(M.d_(period[0]), c.r.randint(0, (M.d_(period[1]) - M.d_(period[0])).days))
                       .isoformat())
        else:
            m = mm[k]
            row.append(c.r.randint(m["lo"], m["hi"]))
    return row


def _fill_count(c, rows, ci, op, thr, g, m):
    """Set column ci so that exactly g rows satisfy (op, thr); values stay inside the measure's range or near it."""
    idx = list(range(len(rows)))
    c.r.shuffle(idx)
    yes = set(idx[:g])
    lo, hi = m["lo"], m["hi"]
    for i in range(len(rows)):
        while True:
            v = c.r.randint(lo, hi)
            if OPS[op](v, thr) == (i in yes) and v != thr:
                break
        rows[i][ci] = v


def _thr(c, m):
    return c.r.randint(m["lo"] + max(1, (m["hi"] - m["lo"]) // 4), m["hi"] - max(1, (m["hi"] - m["lo"]) // 4))


def _q(plan, card, **kw):
    q = {"skill": "QT", "form": plan["form"], "neg": plan.get("neg", 0), "inner_neg": plan.get("inner_neg", False),
         "shown": plan["shown"], "abstain": "NEI" if card["world"] == "open" else "NONE"}
    if plan["form"] in ("yn", "establish", "settle"):
        q["claim"] = {"value": plan["claim_value"]}
    q.update(kw)
    return q


def _finish(doc, dec, plan):
    from f13_lc import _finish_lc
    return _finish_lc(doc, dec, plan)


# ================================================================================================ Q-T samplers
def _slot_shown(r, gold, pool, k, gi, closed):
    """Display-then-gold: k - 1 shown values from pool, gold at display slot gi (gi == k - 1: abstain gold; on closed
    cards gold is then left out of the shown values)."""
    rest = [x for x in pool if x != gold]
    if gi == k - 1:
        if closed:
            if len(rest) < k - 1:
                return None
            return r.sample(rest, k - 1)
        if len(rest) < k - 2:
            return None
        sh = r.sample(rest, k - 2) + [gold]
        r.shuffle(sh)
        return sh
    if len(rest) < k - 2:
        return None
    sh = r.sample(rest, k - 2)
    sh.insert(gi, gold)
    return sh


def tab_qt(card, pack, plan, seed):
    """plan kind: tcount | ag3cnt | targmax | tcmp | tset | ag3sum. Counts: value + shown from the plan; entity, set and
    sum answers: k + gi (display slot) resolved here, or truth (yes/no forms). nm_kinds subset of {V (prior period),
    R (other unit)}; AG-3 rows use R only (a split look-alike table in one section)."""
    c = Ctx(card, pack, seed)
    r = c.r
    k = plan["kind"]
    closed = card["world"] == "closed"
    unit = r.choice(card["units"])
    others = [u for u in card["units"] if u != unit]
    name = r.choice(NAMES)
    P, P0 = _periods(c)
    meas = r.sample(card["measures"], min(len(card["measures"]), r.choice([2, 3])))
    m = meas[0]
    with_date = card.get("tie") == "date"
    cols = _cols(card, meas, with_date)
    ci = cols.index(m["name"])
    taken = set()
    n_rows = max(plan.get("n_rows") or 0, r.randint(5, 12))
    ids = sorted(B.new_id(card["ent_prefix"], 4, r, taken, digits_only=True) for _ in range(n_rows))
    op = r.choice(["ge", "le", "gt", "lt"])
    thr = _thr(c, m)
    split = k in ("ag3sum", "ag3cnt")
    nmk = ([x for x in plan["nm_kinds"] if x == "R"] or ["R"]) if split else list(plan["nm_kinds"])
    ent = ent2 = None
    form = plan["form"]
    # ---------------------------------------------------------------- gold + shown
    if k in ("tcount", "ag3cnt"):
        g, shown = plan["value"], list(plan["shown"])
    elif k == "targmax":
        g = r.choice(ids)
        if form == "choice":
            shown = _slot_shown(r, g, ids, plan["k"], plan["gi"], closed)
            if shown is None:
                return _why("tab shown")
        else:
            shown = list(ids)
            ent = g if plan["truth"] else r.choice([x for x in ids if x != g])
    elif k == "tcmp":
        ent, ent2 = r.sample(ids, 2)
        g = ent if plan["truth"] else "__NOT__"
        shown = [ent, "__NOT__"]
    elif k == "tcrit":  # repair r6
        ent = r.choice(ids)
        g = ent if plan["truth"] else "__NOT__"
        shown = [ent, "__NOT__"]
    elif k == "tset":
        # repair r7 (G7 tset x longest: gold was the centre of its own mutations, never the longest option): every
        # option is a mutation of one centre set and gold is drawn uniformly from that pool (exchangeable length rank)
        c0 = frozenset(r.sample(ids, r.choice([1, 2, 2, 3, 4])))
        pool = {c0}
        for _ in range(80):
            x = set(c0)
            if r.random() < 0.5 and len(x) > 1:
                x.discard(r.choice(sorted(x)))
            else:
                x.add(r.choice(ids))
            if r.random() < 0.3:
                x.add(r.choice(ids))
            if x:
                pool.add(frozenset(x))
        pool = sorted(pool, key=lambda z: sorted(z))
        gs = r.choice(pool)
        g = gs
        shown = _slot_shown(r, gs, pool, plan["k"], plan["gi"], closed)
        if shown is None:
            return _why("tab set shown")
    else:
        g, shown = None, None
    claim = None
    if form != "choice":
        claim = ent if k in ("targmax", "tcmp", "tcrit") else None

    def nm_want():
        pool = [x for x in shown if x != g] if shown else []
        if form == "choice":
            return r.choice(pool) if pool else None
        if k in ("tcmp", "tcrit"):
            return "__NOT__" if g == ent else ent
        return claim if claim != g else r.choice([x for x in ids if x != g])

    def build_rows(target, period, idset):
        rows = [_row(c, card, e, cols, period) for e in idset]
        if k in ("tcount", "ag3cnt"):
            if target > len(rows):
                return None
            _fill_count(c, rows, ci, op, thr, target, m)
        elif k == "tset":
            yes = {idset.index(e) for e in target if e in idset}
            for i in range(len(rows)):
                while True:
                    v = r.randint(m["lo"], m["hi"])
                    if OPS[op](v, thr) == (i in yes) and v != thr:
                        break
                rows[i][ci] = v
        elif k == "targmax":
            wi = idset.index(target)
            top = r.randint(m["lo"] + 2, m["hi"])
            for i in range(len(rows)):
                rows[i][ci] = r.randint(m["lo"], top - 1)
            rows[wi][ci] = top
            if card.get("tie") and r.random() < 0.15:
                if card["tie"] == "number":
                    later = [i for i in range(len(rows)) if idset[i] > target]
                else:
                    di = cols.index("date")
                    later = [i for i in range(len(rows)) if rows[i][di] > rows[wi][di]]
                if later:
                    rows[r.choice(later)][ci] = top
        elif k == "tcmp":
            i1, i2 = idset.index(ent), idset.index(ent2)
            a_, b_ = sorted(r.sample(range(m["lo"], m["hi"] + 1), 2))
            rows[i1][ci], rows[i2][ci] = (b_, a_) if target == ent else (a_, b_)
        elif k == "tcrit":
            i1 = idset.index(ent)
            while True:
                v = r.randint(m["lo"], m["hi"])
                if OPS[op](v, thr) == (target == ent) and v != thr:
                    break
            rows[i1][ci] = v
        return rows

    def chunks_of(rows, n):
        cuts = sorted(r.sample(range(1, len(rows)), n - 1))
        return [rows[a_:b_] for a_, b_ in zip([0] + cuts, cuts + [len(rows)])]
    sections, dec = [], []
    if split:
        rows = [_row(c, card, e, cols, P) for e in ids] if k == "ag3sum" else build_rows(g, P, ids)
        if rows is None:
            return None
        chunks = chunks_of(rows, plan["n_dec"])
        if k == "ag3cnt" and any(not any(OPS[op](x[ci], thr) for x in ch) for ch in chunks):
            return _why("tab part without a hit")
        for pi, ch in enumerate(chunks, start=1):
            f = {"ft": "table", "name": name, "part": pi, "cols": cols, "rows": ch,
                 "total": sum(x[ci] for x in ch), "tmeas": m["name"]}
            sections.append(_sec(c, r.choice(HEADS), "decisive", [f], scope=unit, period=P if pi == 1 else None))
            dec.append(sections[-1]["sid"])
        if k == "ag3sum":
            totals = [sum(x[ci] for x in ch) for ch in chunks]
            g = sum(totals)
    else:
        rows = build_rows(g, P, ids)
        if rows is None:
            return None
        f = {"ft": "table", "name": name, "part": None, "cols": cols, "rows": rows, "total": None, "tmeas": None}
        sections.append(_sec(c, r.choice(HEADS), "decisive", [f], scope=unit, period=P))
        dec.append(sections[-1]["sid"])
    # ---------------------------------------------------------------- near-misses (same name and columns)
    nm_vals = []
    for kind in nmk:
        u2 = r.choice(others)
        per = P0 if kind == "V" else P
        if k == "ag3sum":
            nrows = [_row(c, card, e, cols, per) for e in sorted(B.new_id(card["ent_prefix"], 4, r, taken, True)
                                                                 for _ in range(r.randint(5, 12)))]  # r15 A46: as gold (was 4-8)
        else:
            want = nm_want()
            if want is None:
                return _why("tab nm pool")
            ids2 = ids if k in ("targmax", "tcmp", "tcrit", "tset") else sorted(
                B.new_id(card["ent_prefix"], 4, r, taken, digits_only=True) for _ in range(r.randint(5, 10)))
            nrows = build_rows(want, per, ids2)
            if nrows is None:
                return None
        if split:
            fs = [{"ft": "table", "name": name, "part": pi, "cols": cols, "rows": ch, "total": sum(x[ci] for x in ch),
                   "tmeas": m["name"]} for pi, ch in enumerate(chunks_of(nrows, 2), start=1)]
            nm_vals.append(sum(f["total"] for f in fs))
        else:
            fs = [{"ft": "table", "name": name, "part": None, "cols": cols, "rows": nrows, "total": None,
                   "tmeas": None}]
        if kind == "V":
            sections.append(_sec(c, r.choice(HEADS), "near_miss", fs, scope=unit, period=P0,
                                 nm={"kind": "V", "sub": "period", "tab": True, "period": P0}))
        else:
            sections.append(_sec(c, r.choice(HEADS), "near_miss", fs, scope=u2, period=P,
                                 nm={"kind": "R", "tab": True, "unit": u2}))
    if k == "ag3sum":
        # options: gold, the near-misses' totals, and the 2.2 distractors (first part only, parts plus rows)
        pool = list(dict.fromkeys(nm_vals + [totals[0], g - totals[-1], g + totals[0], g + r.randint(3, 40),
                                             max(1, g - r.randint(3, 40))]))
        pool = [x for x in pool if x != g and x > 0]
        if any(v == g for v in nm_vals):
            return _why("ag3 nm equal")
        kk = plan["k"]
        rest = [x for x in pool if x not in nm_vals]
        r.shuffle(rest)
        base = nm_vals + rest
        if plan["gi"] == kk - 1 and closed:
            shown = base[: kk - 1]
        elif plan["gi"] == kk - 1:
            shown = base[: kk - 2] + [g]
        else:
            # repair r15 (A46, G10 numeric gold rank; r9 cand ag3sum terciles 11/64/14 vs 35/29/25): gold's rank among the
            # kk - 1 numeric options is drawn in the plan (nr, kept over retries); the smaller / larger slots take the
            # near-miss totals and named-error values on that side, then F-NUM fillers; a side that cannot hold the
            # near-miss totals or cannot be filled fails the attempt (retried on the same plan with fresh document seeds).
            nr = plan.get("nr", 0)
            nlo, nhi = nr, kk - 2 - nr
            lo_v = [x for x in nm_vals if x < g]
            hi_v = [x for x in nm_vals if x > g]
            if len(lo_v) > nlo or len(hi_v) > nhi:
                return _why("ag3 rank side")
            lo_v += [x for x in rest if x < g][: nlo - len(lo_v)]
            hi_v += [x for x in rest if x > g][: nhi - len(hi_v)]
            used = set(lo_v + hi_v + [g])
            for _ in range(80):
                if len(lo_v) >= nlo and len(hi_v) >= nhi:
                    break
                lo_side = len(lo_v) < nlo
                x = g - r.randint(3, 60) if lo_side else g + r.randint(3, 60)
                if x >= 1 and x not in used:
                    (lo_v if lo_side else hi_v).append(x)
                    used.add(x)
            if len(lo_v) != nlo or len(hi_v) != nhi:
                return _why("ag3 rank fill")
            shown = lo_v + hi_v
            r.shuffle(shown)
            shown.insert(plan["gi"], g)
        if len(shown) != kk - 1 or not set(nm_vals) <= set(shown):
            return _why("ag3 shown")
        r.shuffle(shown) if plan["gi"] == kk - 1 else None
    # role-less context: another table of the period (fresh entity IDs, another name)
    for _ in range(r.randint(1, 2)):
        n2 = r.choice([x for x in NAMES if x != name])
        ids3 = sorted(B.new_id(card["ent_prefix"], 4, r, taken, digits_only=True) for _ in range(r.randint(3, 6)))
        cols3 = _cols(card, r.sample(card["measures"], min(2, len(card["measures"]))), with_date)
        f = {"ft": "table", "name": n2, "part": None, "cols": cols3, "rows": [_row(c, card, e, cols3, P) for e in ids3],
             "total": None, "tmeas": None}
        sections.append(_sec(c, r.choice(HEADS), "other", [f], scope=r.choice(card["units"]), period=P))
    if not any(s["role"] == "near_miss" for s in sections):
        return _why("tab no nm")
    qk = {"tcount": "tq_count", "ag3cnt": "ag3_count", "targmax": "tq_argmax", "tcmp": "tq_cmp", "tcrit": "tq_crit", "tset": "tq_set",
          "ag3sum": "ag3_sum"}[k]
    pl = dict(plan, value=g, shown=shown, claim_value=claim if claim is not None else plan.get("claim_value"))
    q = _q(pl, card, qk=qk, table=name, unit=unit, period=P, measure=m["name"],
           op=op if k in ("tcount", "ag3cnt", "tset", "tcrit") else None,
           thr=thr if k in ("tcount", "ag3cnt", "tset", "tcrit") else None,
           ent=ent if k in ("tcmp", "tcrit") else None, ent2=ent2)
    doc = {"card": card, "sections": sections, "query": q, "case": None, "title": f"{card['org']} {card['doc_noun']}"}
    return _finish(doc, dec, pl)


def _nm_target(plan, g, pool, r):
    if plan["form"] == "choice":
        return r.choice(pool)
    cv = plan["claim_value"]
    return cv if cv != g else r.choice(pool)


# ================================================================================================ S4 Q-P and AG-1
def tab_qp(card, pack, plan, seed):
    """S4 Q-P (F13R3-11): criteria over table measures applied to one entity's row for the named period.
    plan: value (gold outcome), form, shown, nm_kinds subset of {V (prior period row), I (look-alike entity)}."""
    c = Ctx(card, pack, seed)
    r = c.r
    unit = r.choice(card["units"])
    P, P0 = _periods(c)
    meas = card["measures"][:3]
    cols = _cols(card, meas, card.get("tie") == "date")
    taken = set()
    ids = sorted(B.new_id(card["ent_prefix"], 4, r, taken, digits_only=True) for _ in range(r.randint(4, 9)))
    E = r.choice(ids)
    eff = B.add_days(M.d_(P0[0]), -r.randint(10, 300)).isoformat()
    g = plan["value"]
    outs = card["outcomes"]
    nondef = [o for o in outs if o != card["default"]]
    chosen = [g] if g != card["default"] else []
    rest = [o for o in nondef if o not in chosen]
    r.shuffle(rest)
    chosen += rest[: max(0, len(meas) - len(chosen))]
    ms = r.sample(meas, len(chosen))
    rid0 = r.randint(10, 60)
    crits = [{"ft": "crit", "rid": f"R-{rid0 + 3 * i}", "conds": [{"attr": ms[i]["name"], "op": r.choice(
        ["ge", "gt", "le", "lt"]), "val": _thr(c, ms[i])}], "join": "all", "outcome": o, "eff": eff}
             for i, o in enumerate(chosen)]

    def row_for(target, eid, period):
        """A row on which exactly the target's criterion fires (or none for the default)."""
        for _ in range(200):
            row = _row(c, card, eid, cols, period)
            d = dict(zip(cols, row))
            fired = [x["outcome"] for x in crits if M.eval_conds(x["conds"], "all", d)]
            if (target == card["default"] and not fired) or fired == [target]:
                return row
        return None
    rows = []
    for e in ids:
        rw = row_for(g if e == E else r.choice(outs), e, P)
        if rw is None:
            return _why("tp row")
        rows.append(rw)
    name = r.choice(NAMES)
    sections, dec = [], []
    sections.append(_sec(c, r.choice(HEADS), "decisive", [{"ft": "table", "name": name, "part": None, "cols": cols,
                                                          "rows": rows, "total": None, "tmeas": None}],
                         scope=unit, period=P))
    dec.append(sections[-1]["sid"])
    crit_secs = []
    split = r.random() < 0.5 and len(crits) >= 2
    groups = [crits[: len(crits) // 2], crits[len(crits) // 2:]] if split else [crits]
    for gr in groups:
        crit_secs.append(_sec(c, "Methodology {n}", "other", list(gr)))
    sections += crit_secs
    if g != card["default"]:
        for s in crit_secs:
            if any(x["outcome"] == g for x in s["facts"]):
                s["role"] = "decisive"
                dec.append(s["sid"])
    pool = [o for o in plan["shown"] if o != g]
    for kind in plan["nm_kinds"]:
        want = _nm_target(plan, g, pool, r) if pool else None
        if want is None:
            return _why("tp pool")
        if kind == "V":
            rw = row_for(want, E, P0)
            ids2 = [B.new_id(card["ent_prefix"], 4, r, taken, digits_only=True) for _ in range(r.randint(2, 5))]
            rws = [rw] + [row_for(r.choice(outs), e, P0) for e in ids2]
            if any(x is None for x in rws):
                return _why("tp row")
            rws.sort(key=lambda x: x[0])
            sections.append(_sec(c, r.choice(HEADS), "near_miss", [{"ft": "table", "name": name, "part": None,
                                                                    "cols": cols, "rows": rws, "total": None,
                                                                    "tmeas": None}], scope=unit, period=P0,
                                 nm={"kind": "V", "sub": "period", "tab": True, "period": P0}))
        else:
            e2 = B.lookalike(E, r, taken)
            if e2 is None:
                return None
            taken.add(e2)
            rw = row_for(want, e2, P)
            if rw is None:
                return _why("tp row")
            n2 = r.choice([x for x in NAMES if x != name])
            sections.append(_sec(c, r.choice(HEADS), "near_miss", [{"ft": "table", "name": n2, "part": None,
                                                                    "cols": cols, "rows": [rw], "total": None,
                                                                    "tmeas": None}], scope=unit, period=P,
                                 nm={"kind": "I", "tab": True, "id": e2}))
    q = _q(plan, card, skill="QP", qk="tp_outcome", ent=E, period=P)
    doc = {"card": card, "sections": sections, "query": q, "case": None, "title": f"{card['org']} {card['doc_noun']}"}
    return _finish(doc, dec, plan)


def tab_excl(card, pack, plan, seed):
    """AG-1 active exclusions for a unit (SEM-34; each names one entity and carries one scope mark)."""
    c = Ctx(card, pack, seed)
    r = c.r
    unit = r.choice(card["units"])
    others = [u for u in card["units"] if u != unit]
    Dq = B.add_days(c.base, r.randint(600, 800))
    taken = set()
    g, nd = plan["value"], plan["n_dec"]
    if g < nd:
        return None
    split = sorted(r.sample(range(1, g), nd - 1)) if nd > 1 else []
    sizes = [b - a for a, b in zip([0] + split, split + [g])]

    def ex(scope, status="in force", eff=None, end=("none",)):
        return {"ft": "excl", "xid": B.new_id("EX", 3, r, taken, digits_only=True), "noun": card["item"],
                "eid": B.new_id(card["ent_prefix"], 4, r, taken, digits_only=True), "scope": scope, "status": status,
                "eff": (eff or B.add_days(Dq, -r.randint(20, 400))).isoformat(), "end": list(end)}
    sections, dec = [], []
    for k in sizes:
        fs = [ex(unit, end=("none",) if r.random() < 0.6 else ("through", B.add_days(Dq, r.randint(0, 200))
                                                                .isoformat())) for _ in range(k)]
        sections.append(_sec(c, "Notes to the tables {n}", "decisive", fs))
        dec.append(sections[-1]["sid"])
    pool = [x for x in plan["shown"] if x != g and x >= 1]
    for kind in plan["nm_kinds"]:
        if kind == "V":
            sub = r.choice(["not_yet", "draft", "proposed"])
            if sub == "not_yet":
                e = ex(unit, eff=B.add_days(Dq, r.randint(1, 120)))
                nm = {"kind": "V", "tab": True, "xid": e["xid"], "new_eff": B.add_days(Dq, -r.randint(1, 60))
                      .isoformat()}
            else:
                e = ex(unit, status=sub)
                nm = {"kind": "V", "tab": True, "xid": e["xid"]}
            if g + 1 not in plan["shown"]:
                return _why("excl V unshown")
            sections.append(_sec(c, "Notes to the tables {n}", "near_miss", [e], nm=nm))
        else:
            if not pool:
                return None
            u2 = r.choice(others)
            sections.append(_sec(c, "Notes to the tables {n}", "near_miss", [ex(u2) for _ in range(r.choice(pool))],
                                 nm={"kind": "R", "tab": True, "unit": u2}))
    e = ex(unit, eff=B.add_days(Dq, -r.randint(300, 500)), end=("through", B.add_days(Dq, -r.randint(1, 200))
                                                                 .isoformat()))
    sections.append(_sec(c, "Notes to the tables {n}", "other", [e]))
    q = _q(plan, card, skill="QP", qk="ag1_excl", unit=unit, date=Dq.isoformat())
    doc = {"card": card, "sections": sections, "query": q, "case": None, "title": f"{card['org']} {card['doc_noun']}"}
    return _finish(doc, dec, plan)


# ================================================================================================ traces (2.4)
def _qtables(doc):
    """(section, fact) of the queried table(s) and, for tp rows, the entity's table."""
    q = doc["query"]
    out = []
    for s in doc["sections"]:
        if s["role"] != "decisive":
            continue
        for f in s["facts"]:
            if f["ft"] == "table":
                out.append((s, f))
    return out


def tab_apply_td(doc, c, trace_sec):
    """T-D on an S4 row: a value trace on a decisive cell of an unsplit table (never on a cell a part total pins,
    A07), or a decisive continued part replaced by a part trace."""
    import copy
    q = doc["query"]
    want = {"choice": ("abstain",), "establish": ("no",), "settle": ("claim", None)}.get(q["form"])
    opts = []
    for s, f in _qtables(doc):
        if f["part"] is None:
            col = q.get("measure")
            if q["qk"] == "tp_outcome":
                cols = [a["attr"] for x in doc["sections"] for g in x["facts"] if g["ft"] == "crit" for a in g["conds"]]
            else:
                cols = [col]
            for ri, row in enumerate(f["rows"]):
                if q.get("ent") and q["qk"] in ("tp_outcome", "tq_crit") and row[0] != q["ent"]:
                    continue
                for k in cols:
                    if k in f["cols"]:
                        opts.append(("val", s["sid"], (ri, f["cols"].index(k))))
        else:
            opts.append(("part", s["sid"], (f"Part {f['part']} of table {f['name']}",
                                            f"{doc['card']['scope_kind']} {s['scope']}")))
    c.r.shuffle(opts)
    for kind, sid, x in opts[:12]:
        d2 = copy.deepcopy(doc)
        si = next(i for i, y in enumerate(d2["sections"]) if y["sid"] == sid)
        # repair r2: keep what the T-D replaced (answerable base for role checks, SM.td_base)
        orig = copy.deepcopy(d2["sections"][si]["facts"][0]["rows"][x[0]][x[1]]) if kind == "val" else \
            copy.deepcopy(d2["sections"][si])
        if kind == "val":
            d2["sections"][si]["facts"][0]["rows"][x[0]][x[1]] = TRACE
        else:
            old = d2["sections"][si]
            ts = trace_sec(c, x[0], None, "TD", old["heading"], original=old["facts"])
            ts["trace"]["scope_label"] = x[1]
            ts["trace"]["orig_scope"] = old.get("scope")
            ts["trace"]["orig_period"] = old.get("period")
            ts["sid"] = sid
            d2["sections"][si] = ts
        if M.option_answer(d2) == want and len(M.answers(d2)) >= 2:
            d2["td"] = {"kind": kind, "sid": sid, "orig": orig}
            if kind == "val":
                d2["td"]["cell"] = list(x)  # sidecar bookkeeping only (repair r1)
            return d2
    return None


def tab_add_traces(doc, c, trace_sec, ti_labels):
    """1-3 traces, >= 1 T-B or T-D: T-B value traces on a cell of the queried table that the answer does not read
    (another measure column), T-B parts of the queried table name for another unit, T-I contact parts."""
    import copy
    r = c.r
    card, q = doc["card"], doc["query"]
    unit = q.get("unit") or r.choice(card["units"])
    nmr = {s["nm"]["unit"] for s in doc["sections"] if s.get("nm") and s["nm"]["kind"] == "R"}
    free = [u for u in card["units"] if u != unit and u not in nmr]
    n = r.choices([1, 2, 3], [0.4, 0.4, 0.2])[0]
    have_q = 1 if doc.get("td") else 0
    kinds = [] if have_q else ["TB"]
    while len(kinds) + have_q < n:
        kinds.append("TB" if (have_q + kinds.count("TB")) < 2 and r.random() < 0.4 else "TI")
    read = {q.get("measure")} | {a["attr"] for s in doc["sections"] for f in s["facts"] if f["ft"] == "crit"
                                 for a in f["conds"]}
    for k in kinds:
        if k == "TI":
            doc["sections"].append(trace_sec(c, r.choice(ti_labels), unit if r.random() < 0.6 else
                                             r.choice(card["units"]), "TI", "Contacts ({n})"))
            continue
        # an other-unit table part is benign only when the question selects its table by unit (SEM-30); a criteria
        # row (tp) or an exclusion count could be completed from any table, so those rows get value traces only
        modes = ["value", "part"] if free and q.get("table") else ["value"]
        for mode in r.sample(modes, len(modes)):
            d2 = copy.deepcopy(doc)
            if mode == "value":
                cands = [(si, ri, ci) for si, s in enumerate(d2["sections"]) if s["role"] == "decisive"
                         for f in s["facts"] if f["ft"] == "table"
                         for ri, row in enumerate(f["rows"]) for ci, col in enumerate(f["cols"])
                         if col not in read and col not in ("id", "cat", "date") and row[ci] != TRACE]
                if not cands:
                    continue
                si, ri, ci = r.choice(cands)
                d2["sections"][si]["facts"][0]["rows"][ri][ci] = TRACE
            else:
                name = q.get("table") or r.choice(NAMES)
                ts = trace_sec(c, f"Table {name}", r.choice(free), "TB", r.choice(HEADS))
                d2["sections"].append(ts)
            if M.option_answer(d2) == M.option_answer(doc) and M.answers(d2) == M.answers(doc):
                doc = d2
                break
    # repair r1 (G0 2.4 / G10 traces: every row 1-3 traces with >= 1 T-B or T-D): a T-B draw that found no benign
    # cell used to be dropped silently (S4 rows with no trace or T-I only); retry other unread cells of the queried
    # tables, then refuse the document (build_row redraws it) instead of emitting a row without a T-B / T-D
    def _n_tb(d):
        return sum(1 for s in d["sections"] if (s.get("trace") or {}).get("cls") in ("TB", "TD")) + sum(
            1 for s in d["sections"] for f in s["facts"] if f["ft"] == "table" for row in f["rows"] if TRACE in row)
    if have_q or _n_tb(doc) >= 1:
        return doc
    tis = [i for i, s in enumerate(doc["sections"]) if (s.get("trace") or {}).get("cls") == "TI"]
    if len(tis) >= 3:
        doc["sections"].pop(tis[-1])
    # T-B may sit on a field of a decisive or near-miss section (G0 2.4) when every completion keeps the answer:
    # unread columns first, then other cells (e.g. another entity's criterion cell on a tp row), answer-set checked
    cands = [(col in read, si, ri, ci) for si, s in enumerate(doc["sections"]) if s["role"] in ("decisive", "near_miss")
             for f in s["facts"][:1] if f["ft"] == "table"
             for ri, row in enumerate(f["rows"]) for ci, col in enumerate(f["cols"])
             if col not in ("id", "cat", "date") and row[ci] != TRACE]
    r.shuffle(cands)
    cands.sort(key=lambda x: x[0])
    for _, si, ri, ci in cands[:12]:
        d2 = copy.deepcopy(doc)
        d2["sections"][si]["facts"][0]["rows"][ri][ci] = TRACE
        if M.option_answer(d2) == M.option_answer(doc) and M.answers(d2) == M.answers(doc):
            return d2
    if free and q.get("table"):
        d2 = copy.deepcopy(doc)
        d2["sections"].append(trace_sec(c, f"Table {q['table']}", r.choice(free), "TB", r.choice(HEADS)))
        if M.option_answer(d2) == M.option_answer(doc) and M.answers(d2) == M.answers(doc):
            return d2
    return None
