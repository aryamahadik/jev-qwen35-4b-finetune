"""Queries (question types Q1-Q8), labels, options and negated stem forms for one structure.

Each builder takes a target (yes/no label, or "choice") and returns a row spec or None:
  {"Q": query dict, "gold": 0/1 or option text, "options": [...] (choice), "polarity": "bad"|"not bad"|None,
   "status_option_row": bool, "abstain": None|"NEI"|"None"}
Labels come from solver A only. Solver B re-derives them later on the parse (G2/G3).
"""
from __future__ import annotations

import itertools
import random

import solver_a as A

CMPS_ALL = ("at least", "at most", "more than", "fewer than", "no fewer than", "no more than")
CMPS_NEG_OK = ("at least", "at most", "more than", "fewer than")
BUCKETS = ((2, 4), (5, 9), (10, 19), (20, 60))
BUCKET_TARGET = (0.35, 0.35, 0.15, 0.15)


class Ctx:
    """Replay of one closed structure, shared by the query builders."""

    def __init__(self, card, S):
        self.card, self.S = card, S
        self.states, self.eff, self.E, self.flags = A.replay(S)
        self.end = self.states[-1]
        self.dates = sorted({A.entry_date(S, e) for e in self.eff})
        ids = set()
        for it in S["register"]["items"]:
            ids.add(it[0])
        for e in S["entries"]:
            if e["t"] in ("CREATE",):
                ids.add(e["item"])
            if e["t"] == "RENAME" and e["kind"] == "item":
                ids.add(e["new"])
        self.item_latest = sorted({A.latest_id(S, None, i) for i in ids})
        hold = set()
        for it in S["register"]["items"]:
            hold.add(it[1])
        for e in S["entries"]:
            for k in ("holder", "sender", "receiver"):
                if e.get(k):
                    hold.add(e[k])
            if e["t"] == "MERGE":
                hold.add(e["absorbed"]); hold.add(e["survivor"])
            if e["t"] == "RENAME" and e["kind"] == "holder":
                hold.add(e["new"])
            if e["t"] == "CORR" and e["slot"] == "receiver":
                hold.add(e["value"])
        self.holder_latest = sorted({A.latest_id(S, None, h) for h in hold})
        self.records = sorted({r for _, r in S["register"].get("docs", [])} |
                              {e["new"] for e in S["entries"] if e["t"] == "SUPERSEDE"} |
                              {e["record"] for e in S["entries"] if e["t"] == "OPEN"})

    def exists_at(self, item, idx):
        return self.E.find(item) in self.states[idx].exists

    def latest(self, ident):
        return A.latest_id(self.S, None, ident)


P_FOCUS = 0.88


def _pick(ctx, rng, items):
    """Repair r2: a query names a focus-window item (sampler windows; deep, decisive chains at a uniform decile)
    with probability P_FOCUS when one is available; otherwise any item, as before."""
    foc = {ctx.E.find(y) for y in (ctx.S.get("_focus") or [])}
    if ctx.S.get("_target"):
        foc.add(ctx.E.find(ctx.S["_target"]))
    f = [y for y in items if ctx.E.find(y) in foc]
    if f and rng.random() < P_FOCUS:
        return rng.choice(f)
    return rng.choice(items)


def _pick_doc(ctx, rng, docs):
    f = [d for d in docs if d in (ctx.S.get("_fdocs") or [])]
    if f and rng.random() < P_FOCUS:
        return rng.choice(f)
    return rng.choice(docs)


def pick_k(rng, n_cands, extra=0, want_bucket=None, abstain=False):
    """Option count k (abstain slot included) inside the wanted bucket when feasible."""
    maxk = n_cands + extra
    if maxk < 2:
        return None
    if want_bucket is not None:
        lo, hi = BUCKETS[want_bucket]
        hi = min(hi, maxk)
        if lo > hi:
            return None
        if want_bucket == 3:
            hi = min(hi, 23)
        return rng.randint(lo, hi)
    return rng.randint(2, min(maxk, 9))


# ------------------------------------------------------------------------------------------------ polarity

def pol_status(card, value):
    return card["status_tag"].get(value)


def pol_holding(card, holder_id, roles):
    r = roles.get(holder_id)
    for name, tag in card["roles"]:
        if name == r:
            return tag
    return None


def pol_qty(card, cmp_):
    if card.get("qty_high_bad") is None:
        return None
    high = cmp_ in ("at least", "more than", "no fewer than")
    return "bad" if high == bool(card["qty_high_bad"]) else "not bad"


def pol_count(card, cmp_):
    high_bad = card.get("count_high_bad", True)
    high = cmp_ in ("at least", "more than", "no fewer than")
    return "bad" if high == high_bad else "not bad"


# ------------------------------------------------------------------------------------------------ builders

def _end_word(rng):
    return rng.choice(("at the end", "now", "currently"))


def q_status(ctx, rng, *, form, target, point=None, want_bucket=None):
    c, S = ctx.card, ctx.S
    pt = point or {"kind": "end"}
    idx = _pt_index(ctx, pt)
    items = [y for y in ctx.item_latest if (idx is None or ctx.exists_at(y, idx))]
    if not items:
        return None
    y = _pick(ctx, rng, items)
    Q = {"qt": "Q1" if pt["kind"] == "end" else "Q2", "form": form, "kind": "status", "item": y, "point": pt,
         "end_word": _end_word(rng), "kinds": c["kind_nouns"] and rng.random() < 0.5}
    if form == "choice":
        gold = A.answer(S, Q)
        if gold in (None, A.UNK, A.NO_SINGLE):
            return None
        k = pick_k(rng, len(S["statuses"]), want_bucket=want_bucket)
        if not k:
            return None
        others = [s for s in S["statuses"] if s != gold]
        opts = [gold] + rng.sample(others, k - 1)
        rng.shuffle(opts)
        return {"Q": Q, "gold": gold, "options": opts, "polarity": None, "status_option_row": True}
    # yes/no
    if pt["kind"] == "range":
        vals = list(S["statuses"])
    else:
        Q0 = dict(Q, form="choice")
        cur = A.answer(S, Q0)
        if cur in (None, A.UNK, A.NO_SINGLE):
            return None
        vals = [cur] if target == 1 else [s for s in S["statuses"] if s != cur]
    rng.shuffle(vals)
    for v in vals:
        Q2 = dict(Q, value=v, neg="A")
        lab = A.answer(S, Q2)
        if lab == target:
            return {"Q": Q2, "gold": lab, "polarity": pol_status(c, v)}
    return None


def q_qty(ctx, rng, *, target, point=None):
    c, S = ctx.card, ctx.S
    if not S["has_qty"]:
        return None
    pt = point or {"kind": "end"}
    idx = _pt_index(ctx, pt)
    items = [y for y in ctx.item_latest if (idx is None or ctx.exists_at(y, idx))]
    if not items:
        return None
    y = _pick(ctx, rng, items)
    st = ctx.states[idx if idx is not None else -1]
    q = st.qty.get(ctx.E.find(y))
    if q is None or q == A.UNK:
        return None
    cmp_ = rng.choices(CMPS_ALL, [3, 3, 2, 2, 1, 1])[0]
    for _ in range(12):
        N = max(1, q + rng.choice((-2, -1, 0, 0, 1, 2)))
        Q = {"qt": "Q1" if pt["kind"] == "end" else "Q2", "form": "yn", "kind": "qty", "item": y, "cmp": cmp_, "n": N,
             "point": pt, "end_word": _end_word(rng), "neg": "A", "kinds": c["kind_nouns"] and rng.random() < 0.5}
        lab = A.answer(S, Q)
        if lab == target:
            return {"Q": Q, "gold": lab, "polarity": pol_qty(c, cmp_)}
    return None


def _pt_index(ctx, pt):
    if pt["kind"] == "end":
        return len(ctx.eff)
    if pt["kind"] == "range":
        return sum(1 for e in ctx.eff if A.entry_date(ctx.S, e) < pt["d1"])
    return A.point_index(ctx.S, ctx.eff, pt)


def date_point(ctx, rng, *, kinds=("on", "as of", "at the end of", "at the start of"), boundary=False):
    S = ctx.S
    if not ctx.dates:
        return None
    k = rng.choice(kinds)
    d = rng.choice(ctx.dates)
    if S.get("_focus") and rng.random() < 0.5 and len(ctx.dates) >= 3:
        d = rng.choice(ctx.dates[len(ctx.dates) // 3:])   # repair r2: later dates put more of a chain on the path
    if not boundary and rng.random() < 0.3:
        d = A_dshift(d, rng.choice((-1, 1)))
    if S["sampler"] == "S6":
        if k == "at the start of" and d <= S["d0"]:
            return None
        if d < S["d0"]:
            return None
    return {"kind": k, "date": d}


def range_point(ctx, rng):
    S = ctx.S
    if len(ctx.dates) < 2:
        return None
    a, b = sorted(rng.sample(ctx.dates, 2))
    if S["sampler"] == "S6" and a <= S["d0"]:
        return None
    return {"kind": "range", "d1": a, "d2": b}


def A_dshift(d, k):
    from f3common import d_add
    return d_add(d, k)


def q_record(ctx, rng, *, form, target, want_bucket=None):
    c, S = ctx.card, ctx.S
    docs = [d for d in ctx.end.current]
    if not docs:
        return None
    doc = _pick_doc(ctx, rng, docs)
    if form == "yn":
        # repair r2 (G7: Q3 yes/no rows with a SUPERSEDE on the path were 26% yes): a "yes" record question asks
        # about a document whose current record came through a supersede chain when one exists, so the chain is
        # decisive on yes rows as often as on no rows
        chained = [d for d in docs if ctx.end.current[d] not in {r for x, r in S["register"].get("docs", [])
                                                                 if x == d}
                   and any(e["t"] == "SUPERSEDE" and e["new"] == ctx.end.current[d] for e in S["entries"])]
        if target == 1:
            if chained:
                doc = rng.choice(chained)
            elif any(e["t"] == "SUPERSEDE" for e in S["entries"]):
                return None
            # repair r2.2 (G7 'of deviation' / Q3 29% yes): a log with no supersede entry at all asks yes about
            # any document, so a card whose logs never supersede still has yes rows (no supersede cue either way)
    cur = ctx.end.current[doc]
    Q = {"qt": "Q3", "form": form, "kind": "record", "doc": doc, "end_word": _end_word(rng)}
    if form == "choice":
        same = [r for r in ctx.records if ctx.end.rec_doc.get(r) == doc or _chain_member(S, doc, r)]
        others = [r for r in ctx.records if r not in same]
        pool = [r for r in same if r != cur] + others
        k = pick_k(rng, len(pool) + 1, want_bucket=want_bucket)
        if not k:
            return None
        opts = [cur] + (pool[:k - 1] if len(pool) >= k - 1 else pool)
        if len(opts) < 2:
            return None
        rng.shuffle(opts)
        return {"Q": Q, "gold": cur, "options": opts, "polarity": None}
    if target == 1:
        R = cur
    else:
        cands = [r for r in ctx.records if r != cur]
        if not cands:
            return None
        same = [r for r in cands if _chain_member(S, doc, r)]
        R = rng.choice(same) if same and rng.random() < 0.7 else rng.choice(cands)
    Q.update(record=R, neg="A")
    lab = A.answer(S, Q)
    if lab != target:
        return None
    return {"Q": Q, "gold": lab, "polarity": c["doc_tag"].get(c["_doctype"].get(doc))}


def _chain_member(S, doc, r):
    rec = None
    for d, x in S["register"].get("docs", []):
        if d == doc:
            rec = x
    for e in S["entries"]:
        if e["t"] == "OPEN" and e["doc"] == doc:
            rec = e["record"]
    members = {rec}
    changed = True
    while changed:
        changed = False
        for e in S["entries"]:
            if e["t"] == "SUPERSEDE" and e["old"] in members and e["new"] not in members:
                members.add(e["new"])
                changed = True
    return r in members


def q_holds(ctx, rng, *, target, roles, mode="end", item=None):
    """Q4: 'Does X hold Y at the end?', 'Does X still hold Y?' or 'Did X hold Y on D?'."""
    c, S = ctx.card, ctx.S
    pt = {"kind": "end"}
    if mode == "date":
        pt = date_point(ctx, rng, kinds=("on",))
        if pt is None:
            return None
    idx = _pt_index(ctx, pt)
    items = [y for y in ctx.item_latest if ctx.exists_at(y, idx)]
    if item is not None:
        items = [y for y in items if ctx.E.find(y) == ctx.E.find(item)]
    if not items:
        return None
    y = _pick(ctx, rng, items)
    st = ctx.states[idx]
    h = st.holder.get(ctx.E.find(y))
    if h is None:
        return None
    if target == 1:
        X = ctx.latest(h)
    else:
        # distractors: a past holder (E10/E11) or any other live holder
        past = {ctx.latest(s.holder.get(ctx.E.find(y))) for s in ctx.states if s.holder.get(ctx.E.find(y))}
        cands = [x for x in ctx.holder_latest if ctx.E.find(x) != h]
        pref = [x for x in cands if x in past]
        if not cands:
            return None
        X = rng.choice(pref) if pref and rng.random() < 0.6 else rng.choice(cands)
    Q = {"qt": "Q4", "form": "yn", "kind": "holder", "item": y, "holder": X, "point": pt, "neg": "A",
         "end_word": _end_word(rng), "kinds": c["kind_nouns"] and rng.random() < 0.5}
    if mode == "still":
        Q["still"] = True
        if not A.guard_ok(S, ctx.states, ctx.eff, ctx.E, y, X):
            return None
    lab = A.answer(S, Q)
    if lab != target:
        return None
    return {"Q": Q, "gold": lab, "polarity": pol_holding(c, X, roles)}


def q_who(ctx, rng, *, want_bucket=None):
    c, S = ctx.card, ctx.S
    items = [y for y in ctx.item_latest if ctx.exists_at(y, len(ctx.eff))]
    if not items:
        return None
    y = _pick(ctx, rng, items)
    Q = {"qt": "Q5", "form": "choice", "kind": "holder", "item": y, "point": {"kind": "end"},
         "end_word": _end_word(rng), "qc_v": rng.randrange(2), "kinds": c["kind_nouns"] and rng.random() < 0.5}
    gold_ent = A.answer(S, Q)
    if gold_ent in (None, A.UNK, A.NO_SINGLE):
        return None
    gold = ctx.latest(gold_ent)
    pool = [h for h in ctx.holder_latest if ctx.E.find(h) != ctx.E.find(gold)]
    k = pick_k(rng, len(pool) + 1, want_bucket=want_bucket)
    if not k:
        return None
    opts = [gold] + rng.sample(pool, k - 1)
    rng.shuffle(opts)
    return {"Q": Q, "gold": gold, "options": opts, "polarity": None}


def q_count(ctx, rng, *, target, roles):
    c, S = ctx.card, ctx.S
    X = rng.choice(ctx.holder_latest)
    cnt = sum(1 for i in ctx.end.exists if ctx.end.holder.get(i) == ctx.E.find(X))
    cands = sum(1 for i in ctx.end.exists if any(s.holder.get(i) == ctx.E.find(X) for s in ctx.states))
    cmp_ = rng.choices(CMPS_ALL, [3, 3, 2, 2, 1, 1])[0]
    for _ in range(10):
        N = max(1, cnt + rng.choice((-1, 0, 0, 1, 2)))
        Q = {"qt": "Q6", "form": "yn", "kind": "count", "holder": X, "cmp": cmp_, "n": N, "neg": "A",
             "end_word": _end_word(rng), "kinds": c["kind_nouns"] and rng.random() < 0.5}
        lab = A.answer(S, Q)
        if lab == target:
            deep = cands > 8 or N > 6
            return {"Q": Q, "gold": lab, "polarity": pol_count(c, cmp_), "q6_deep": deep}
    return None


def q_inverse(ctx, rng, *, want_bucket=None, slot=None):
    """Q7 (inverted cards): 'Which of these <items> does X hold at the end?' with the None option (XF01)."""
    c, S = ctx.card, ctx.S
    X = rng.choice(ctx.holder_latest)
    Xe = ctx.E.find(X)
    held = [y for y in ctx.item_latest if ctx.exists_at(y, len(ctx.eff)) and ctx.end.holder.get(ctx.E.find(y)) == Xe]
    not_held = [y for y in ctx.item_latest if ctx.exists_at(y, len(ctx.eff)) and ctx.end.holder.get(ctx.E.find(y)) != Xe]
    if slot is not None:
        k, none_gold = slot["k"], slot["abstain_gold"]
    else:
        k = pick_k(rng, len(not_held) + 1, extra=1, want_bucket=want_bucket)
        if not k or k < 3:
            return None
        none_gold = rng.random() < 1.0 / k
    if none_gold:
        if len(not_held) < k - 1:
            return None
        cands = rng.sample(not_held, k - 1)
        gold = c["none"]
    else:
        if not held or len(not_held) < k - 2:
            return None
        g = rng.choice(held)
        cands = [g] + rng.sample(not_held, k - 2)
        gold = g
    rng.shuffle(cands)
    Q = {"qt": "Q7", "form": "choice", "kind": "inverse", "holder": X, "candidates": cands,
         "none_option": c["none"], "end_word": _end_word(rng), "kinds": c["kind_nouns"] and rng.random() < 0.5}
    lab = A.answer(S, Q)
    if lab != gold:
        return None
    opts = cands + [c["none"]]
    rng.shuffle(opts)
    return {"Q": Q, "gold": gold, "options": opts, "polarity": None, "abstain": "None"}


def q_transfer(ctx, rng, *, target, roles):
    c, S = ctx.card, ctx.S
    trs = [e for e in S["entries"] if e["t"] == "TRANSFER"]
    rng.shuffle(trs)
    for e in trs:
        Q = {"qt": "Q8", "form": "yn", "kind": "transfer", "entry": e["n"], "neg": "A"}
        # rule 15: the item exists at the transfer's point (always true by rule 19)
        lab = A.answer(S, Q)
        if lab == target:
            return {"Q": Q, "gold": lab, "polarity": pol_holding(c, e["receiver"], roles)}
    return None


# ------------------------------------------------------------------------------------------------ open cards

def open_query(card, S, rng, qt, form, target=None, want_bucket=None, roles=None, slot=None):
    """Open cards: Q1 (status choice / yes-no, quantity yes-no), Q4 end (incl. still / no longer), Q5. Choice rows
    with k >= 3 show NEI; its gold slot is drawn first (display-then-gold, XF01)."""
    vals, eff, E = A.open_values(S)
    items = sorted({A.latest_id(S, None, i) for i in vals})
    if not items:
        return None
    y = rng.choice(items)
    v = vals[E.find(y)]
    if qt == "Q1" and form == "choice":
        if slot is not None:
            k, nei_gold = slot["k"], slot["abstain_gold"]
            if k > len(S["statuses"]) + 1:
                return None
        else:
            k = pick_k(rng, len(S["statuses"]), extra=1, want_bucket=want_bucket)
            if not k:
                return None
            nei_gold = k >= 3 and rng.random() < 1.0 / k
        nei_shown = k >= 3
        Q = {"qt": "Q1", "form": "choice", "kind": "status", "item": y, "point": {"kind": "end"},
             "end_word": _end_word(rng), "kinds": card["kind_nouns"] and rng.random() < 0.5}
        lab = A.answer_open(S, Q)
        if nei_gold != (lab == A.UNK):
            return None
        if lab == A.UNK:
            opts = rng.sample(S["statuses"], min(len(S["statuses"]), k - 1)) + [card["nei"]]
            if len(opts) != k:
                return None
            gold = card["nei"]
        else:
            others = [s for s in S["statuses"] if s != lab]
            n_other = k - 1 - (1 if nei_shown else 0)
            if n_other > len(others):
                return None
            opts = [lab] + rng.sample(others, n_other) + ([card["nei"]] if nei_shown else [])
            gold = lab
        rng.shuffle(opts)
        return {"Q": Q, "gold": gold, "options": opts, "polarity": None, "status_option_row": True,
                "abstain": "NEI" if nei_shown else None}
    if qt == "Q5":
        hs = set()
        for it in S["register"]["items"]:
            hs.add(it[1])
        for e in S["entries"]:
            for kk in ("holder", "sender", "receiver"):
                if e.get(kk):
                    hs.add(e[kk])
            if e["t"] == "CORR" and e["slot"] == "receiver":
                hs.add(e["value"])
        hs = sorted(hs)
        if slot is not None:
            k, nei_gold = slot["k"], slot["abstain_gold"]
            if k > len(hs) + 1:
                return None
        else:
            k = pick_k(rng, len(hs), extra=1, want_bucket=want_bucket)
            if not k:
                return None
            nei_gold = k >= 3 and rng.random() < 1.0 / k
        nei_shown = k >= 3
        Q = {"qt": "Q5", "form": "choice", "kind": "holder", "item": y, "point": {"kind": "end"},
             "end_word": _end_word(rng), "qc_v": rng.randrange(2), "kinds": card["kind_nouns"] and rng.random() < 0.5}
        lab = A.answer_open(S, Q)
        if nei_gold != (lab == A.UNK):
            return None
        if lab == A.UNK:
            if len(hs) < k - 1:
                return None
            opts = rng.sample(hs, k - 1) + [card["nei"]]
            gold = card["nei"]
        else:
            others = [h for h in hs if E.find(h) != lab]
            n_other = k - 1 - (1 if nei_shown else 0)
            if n_other > len(others):
                return None
            gold = lab
            opts = [lab] + rng.sample(others, n_other) + ([card["nei"]] if nei_shown else [])
        rng.shuffle(opts)
        return {"Q": Q, "gold": gold, "options": opts, "polarity": None, "abstain": "NEI" if nei_shown else None}
    if qt == "Q1":
        if S["has_qty"] and rng.random() < 0.35:
            q = v["qty"]
            if q == A.UNK:
                return None
            cmp_ = rng.choices(CMPS_ALL, [3, 3, 2, 2, 1, 1])[0]
            N = max(1, q + rng.choice((-2, -1, 0, 1, 2)))
            Q = {"qt": "Q1", "form": "yn", "kind": "qty", "item": y, "cmp": cmp_, "n": N, "point": {"kind": "end"},
                 "end_word": _end_word(rng), "neg": "A", "kinds": card["kind_nouns"] and rng.random() < 0.5}
            lab = A.answer_open(S, Q)
            if lab != target:
                return None
            return {"Q": Q, "gold": lab, "polarity": pol_qty(card, cmp_)}
        s = v["status"]
        if s == A.UNK:
            return None
        val = s if target == 1 else rng.choice([x for x in S["statuses"] if x != s])
        Q = {"qt": "Q1", "form": "yn", "kind": "status", "item": y, "value": val, "point": {"kind": "end"},
             "end_word": _end_word(rng), "neg": "A", "kinds": card["kind_nouns"] and rng.random() < 0.5}
        lab = A.answer_open(S, Q)
        if lab != target:
            return None
        return {"Q": Q, "gold": lab, "polarity": pol_status(card, val)}
    if qt == "Q4":
        h = v["holder"]
        if h == A.UNK:
            return None
        hs = set(x[1] for x in S["register"]["items"]) | {e[k] for e in S["entries"]
                                                           for k in ("holder", "sender", "receiver") if e.get(k)}
        if target == 1:
            X = h
        else:
            cands = sorted(x for x in hs if E.find(x) != h)
            if not cands:
                return None
            X = rng.choice(cands)
        still = rng.random() < 0.3 and card.get("still_on")
        Q = {"qt": "Q4", "form": "yn", "kind": "holder", "item": y, "holder": X, "point": {"kind": "end"},
             "neg": "A", "end_word": _end_word(rng), "kinds": card["kind_nouns"] and rng.random() < 0.5}
        if still:
            Q["still"] = True
            if not A.open_guard(S, Q, eff, E):
                return None
        lab = A.answer_open(S, Q)
        if lab != target:
            return None
        return {"Q": Q, "gold": lab, "polarity": pol_holding(card, X, roles or {})}
    return None


# ------------------------------------------------------------------------------------------------ negation forms

def neg_forms_allowed(Q):
    """(complement forms, D allowed with base) for a yes/no row's stem kind (2.2 form table, R4-01..R4-04)."""
    qt, kind = Q["qt"], Q["kind"]
    pt = Q.get("point") or {"kind": "end"}
    if Q.get("cmp") in ("no fewer than", "no more than"):
        return [], None
    if pt.get("kind") == "range":
        return ["N5"], None
    if kind in ("qty", "count"):
        return ["N4", "N5"], None
    if Q.get("still"):
        return ["N2", "N5"], "N2"
    if qt == "Q3":
        return ["N1", "N3", "N4", "N5"], "N1N3"
    if qt == "Q8":
        return ["N1", "N3", "N4", "N5"], "N1N3"
    if qt == "Q4" and pt["kind"] == "end":
        return ["N1", "N2", "N4", "N5"], "N1N2"
    if qt in ("Q1", "Q2", "Q4") and kind in ("status", "holder"):
        return ["N1", "N4", "N5"], "N1"
    return ["N4", "N5"], None


def twin_neg(Q, form, dbase=None):
    q = dict(Q)
    q["neg"] = form
    q.pop("a_frame", None)
    if form == "D":
        q["dbase"] = dbase
    if form in ("N2",) or (form == "D" and dbase == "N2"):
        q.pop("still", None)
        q["point"] = {"kind": "end"}
    return q


# ------------------------------------------------------------------------------------------------ 2.1 Alt check

def triggered_alts(card, S, Q):
    """Program variants (section 2 Alt column) whose trigger the row's structure or question touches (2.1 rows:
    closed, S1/S4, no check, lock, gaps, renames, merges, masks, notes; ISO / month-name dates)."""
    ts = {e["t"] for e in S["entries"]}
    alts = []
    pt = Q.get("point") or {"kind": "end"}
    if pt.get("kind") not in ("end", None) and ({"VOID", "CORR", "WITHDRAW"} & ts):
        alts += ["T7", "T10"]
    if "CORR" in ts:
        alts += ["T11a", "T11c", "T11e"]
    if "CORR" in ts and ({"VOID", "WITHDRAW"} & ts):
        alts += ["T12a", "T12b"]
    if "SUPERSEDE" in ts and Q["qt"] == "Q3":
        alts += ["T13a", "T13b"]
    alts.append("T16")
    if S["has_qty"] and Q["qt"] in ("Q4", "Q5", "Q6"):
        alts.append("T17")
    if Q.get("cmp"):
        alts.append("T22")
    if pt.get("kind") in ("on", "as of"):
        alts += ["T24a", "T24b"]
        if Q.get("neg") in A.COMPLEMENT_FORMS:
            alts.append("T24b_inner")
    if pt.get("kind") == "range":
        alts += ["T25a", "T25b1", "T25b2", "T25b3"]
    if Q.get("still") or Q.get("neg") == "N2" or (Q.get("neg") == "D" and Q.get("dbase") == "N2"):
        alts += ["T31a", "T31b", "T31c"]
    if Q["qt"] == "Q8":
        alts.append("T38")
    if Q["qt"] == "Q6":
        alts += ["T39a", "T39b"]
    if S["sampler"] == "S4":
        alts += ["T41a"]
        if "WITHDRAW" in ts:
            alts.append("T41b")
    return alts


def alt_check(card, S, Q, gold):
    """True if every single Alt and every pair of Alts gives the gold label (2.1 check). Logs per-variant drops."""
    alts = triggered_alts(card, S, Q)
    singles = [frozenset([a]) for a in alts if a != "T24b_inner"]
    if "T24b_inner" in alts:
        singles.append(frozenset(["T24b", "T24b_inner"]))
    combos = list(singles)
    for a, b in itertools.combinations(singles, 2):
        combos.append(a | b)
    for al in combos:
        try:
            lab = A.answer(S, Q, alts=al)
        except (ValueError, KeyError, TypeError, IndexError, AttributeError):
            return False, sorted(al)
        if lab != gold:
            return False, sorted(al)
    return True, None
