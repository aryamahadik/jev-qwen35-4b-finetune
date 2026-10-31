"""Solver A: forward replay (G2 reference) for F3 structures (G0 spec section 3, solver A steps 1-6).

Structure (dict, JSON-able), shared by generator, parser and solvers:
  sampler       "S1".."S6"
  world         "closed" | "open";  gap_style None | "explicit" | "skipped" | "leading";  n0 (leading extracts)
  toggles       {"rename_mode": None|"alias"|"retire", "check": bool, "lock": bool, "lock_status": str|None,
                 "timed": bool}
  has_qty, statuses (card vocabulary), default_status
  register      {"items": [[item, holder, status, qty|None], ...], "docs": [[doc, record], ...]}
  entries       [{"n", "date", "time", "eff" (S6), "ref", "k" (S4), "t", ...slots}, ...] in numbering order
      t: CREATE(item, holder, status|None, qty|None)  OPEN(record, doc)  SET(item, field, value)
         ADJUST(item, sign, amount)  TRANSFER(item, sender, receiver)  VOID(target)  WITHDRAW(target_ref)
         CORR(target, slot, value)  SUPERSEDE(old, new)  RENAME(kind, old, new)  MERGE(absorbed, survivor)
  gaps          open cards: list of gap positions, each = the entry number after which entries are missing
  d0            S6: the opening snapshot date
Query (dict): qt, form ("choice"|"yn"), kind, item, holder, doc, record, value, cmp, n, point, still, nolonger,
  candidates (Q7), entry (Q8), neg ("A","N1".."N5","D").

Alt flags (2.1 check; section 2 Alt column) are program variants of this solver. They are only used by the 2.1 check.
"""
from __future__ import annotations

import copy

UNK = "<UNKNOWN>"
NO_SINGLE = "<NO_SINGLE_ANSWER>"

CMP_FUNCS = {
    "at least": lambda a, n: a >= n, "no fewer than": lambda a, n: a >= n,
    "at most": lambda a, n: a <= n, "no more than": lambda a, n: a <= n,
    "more than": lambda a, n: a > n, "fewer than": lambda a, n: a < n,
}
CMP_SWAP = {"at least": "more than", "no fewer than": "more than", "at most": "fewer than",
            "no more than": "fewer than", "more than": "at least", "fewer than": "at most"}
COMPLEMENT_FORMS = ("N1", "N2", "N3", "N4", "N5")


# ------------------------------------------------------------------------------------------------ orders

def effect_key(S, e):
    sp = S["sampler"]
    if sp == "S6":
        d = e.get("eff") or e["date"]
        return (d, e["n"])
    if sp == "S5":
        return (e["n"],)
    if sp == "S4":
        return (e["date"], e["ref"], e["k"])
    return (e["date"], e.get("time") or "", e["n"])


def entry_date(S, e):
    """The date T24/T25 read for an entry: the effective date on S6, else the entry's date."""
    return (e.get("eff") or e["date"]) if S["sampler"] == "S6" else e["date"]


def own_key(S, e):
    """Rule 10 order key of a VOID / CORRECTION entry itself (R2-06)."""
    sp = S["sampler"]
    if sp == "S6":
        return (e["date"], e["n"])
    if sp == "S5":
        return (e["n"],)
    if sp == "S4":
        return (e["date"], e["ref"], e["k"])
    return (e["date"], e.get("time") or "", e["n"])


# ------------------------------------------------------------------------------------------------ entities

class Ents:
    """Whole-log rename closure: every ID of an item or holder maps to one entity key (its first ID)."""

    def __init__(self, S, alts=frozenset()):
        self.parent = {}
        for e in S["entries"]:
            if e["t"] == "RENAME":
                a, b = self.find(e["old"]), self.find(e["new"])
                if a != b:
                    self.parent[b] = a
        if "T16" in alts:  # look-alike IDs (edit distance <= 2) count as one entity
            from f3common import edit_distance
            ids = set()
            for it in S["register"]["items"]:
                ids.add(it[0]); ids.add(it[1])
            for e in S["entries"]:
                for k in ("item", "holder", "sender", "receiver", "old", "new", "absorbed", "survivor"):
                    if isinstance(e.get(k), str):
                        ids.add(e[k])
            ids = sorted(ids)
            for i, a in enumerate(ids):
                for b in ids[i + 1:]:
                    if a.split("-")[0] == b.split("-")[0] and edit_distance(a, b) <= 2:
                        ra, rb = self.find(a), self.find(b)
                        if ra != rb:
                            self.parent[rb] = ra

    def find(self, x):
        while x in self.parent:
            x = self.parent[x]
        return x


def latest_id(S, ent_ids, ident):
    """The latest ID of the entity named by `ident` (options name entities by their latest ID; rule 12)."""
    cur = ident
    changed = True
    while changed:
        changed = False
        for e in S["entries"]:
            if e["t"] == "RENAME" and e["old"] == cur:
                cur = e["new"]
                changed = True
    return cur


# ------------------------------------------------------------------------------------------------ effective list

def expand(S, alts=frozenset()):
    """Entries with S4 withdrawals expanded to VOIDs (T41). Withdraw-Alt (T41b): only the first change."""
    out = []
    by_ref = {}
    for e in S["entries"]:
        if "ref" in e:
            by_ref.setdefault(e["ref"], []).append(e)
    for e in S["entries"]:
        if e["t"] == "WITHDRAW":
            targets = [x["n"] for x in by_ref.get(e["target_ref"], [])]
            if "T41b" in alts:
                targets = targets[:1]
            for tn in targets:
                out.append({**e, "t": "VOID", "target": tn, "_withdraw": True})
        else:
            out.append(e)
    return out


def effective(S, alts=frozenset(), view=None):
    """Solver A steps 1-3: drop voided entries, apply corrections per value, sort by effect key.
    view: None (the log as it stands now) or an own-key bound (T7 / T10 Alts: only voids / corrections whose own key
    is <= view count). Returns (eff list of corrected entry copies, info)."""
    ents = expand(S, alts)
    in_view = (lambda e: True) if view is None else (lambda e: own_key(S, e) <= view)
    voids = [e for e in ents if e["t"] == "VOID" and in_view(e)]
    if "T10" in alts and view is not None:
        pass  # T10 Alt (a void counts only from its own point) is the same view restriction, voids only
    voided = {e["target"] for e in voids}
    corrs_all = [e for e in ents if e["t"] == "CORR" and (in_view(e) or ("T10" in alts and "T7" not in alts))]
    if "T13b" in alts:  # a voided supersede still counts
        sup_n = {e["n"] for e in ents if e["t"] == "SUPERSEDE"}
        voided = {v for v in voided if v not in sup_n}
    live_corrs = []
    for c in corrs_all:
        if c["n"] in voided and "T12b" not in alts:
            continue
        live_corrs.append(c)
    # per value: highest-numbered live correction counts (T11); Alts c / e
    best = {}
    for c in sorted(live_corrs, key=lambda c: c["n"]):
        key = (c["target"], c["slot"]) if "T11e" not in alts else (c["target"],)
        best[key] = c
    if "T11c" in alts:  # the highest correction is voided -> the original value stands
        for c in sorted([c for c in corrs_all], key=lambda c: c["n"]):
            key = (c["target"], c["slot"])
            hi = max((x for x in corrs_all if (x["target"], x["slot"]) == key), key=lambda x: x["n"])
            if hi["n"] in voided:
                best.pop(key, None)
    by_target = {}
    for key, c in best.items():
        by_target.setdefault(c["target"], []).append(c)
    eff = []
    deferred = []
    for e in ents:
        if e["t"] in ("VOID", "CORR", "WITHDRAW"):
            continue
        if e["n"] in voided and not ("T12a" in alts and e["n"] in by_target):
            continue
        x = dict(e)
        for c in by_target.get(e["n"], []):
            if "T11a" in alts:
                deferred.append((c, x))
                continue
            _apply_corr(x, c)
        eff.append(x)
    if "T11a" in alts:  # a correction acts as a new latest entry, at its own point
        for c, x in deferred:
            eff.append({"t": "_CORR_AS_ENTRY", "n": c["n"], "date": c["date"], "time": c.get("time"),
                        "eff": c["date"], "ref": c.get("ref", 0), "k": c.get("k", 0), "src": x, "corr": c})
    if "T41a" in alts and S["sampler"] == "S4":
        eff.sort(key=lambda e: (e["date"], e["ref"], -e["k"]))
    else:
        eff.sort(key=lambda e: effect_key(S, e))
    return eff


def _apply_corr(x, c):
    s = c["slot"]
    if x["t"] == "SET" and s == "value":
        x["value"] = c["value"]
    elif x["t"] == "ADJUST" and s == "amount":
        x["amount"] = c["value"]
    elif x["t"] == "TRANSFER" and s == "receiver":
        x["receiver"] = c["value"]
    elif x["t"] == "CREATE" and s == "status":
        x["status"] = c["value"]
    elif x["t"] == "CREATE" and s == "qty":
        x["qty"] = c["value"]
    else:
        raise ValueError("correction slot does not fit its target")


# ------------------------------------------------------------------------------------------------ replay

class State:
    __slots__ = ("holder", "status", "qty", "exists", "current", "rec_doc", "retired", "absorbed")

    def __init__(self):
        self.holder, self.status, self.qty, self.exists = {}, {}, {}, set()
        self.current, self.rec_doc = {}, {}
        self.retired, self.absorbed = set(), set()

    def copy(self):
        s = State()
        s.holder, s.status, s.qty, s.exists = dict(self.holder), dict(self.status), dict(self.qty), set(self.exists)
        s.current, s.rec_doc = dict(self.current), dict(self.rec_doc)
        s.retired, s.absorbed = set(self.retired), set(self.absorbed)
        return s


def initial_state(S, E):
    st = State()
    for item, holder, status, qty in S["register"]["items"]:
        i = E.find(item)
        st.exists.add(i)
        st.holder[i] = E.find(holder) if holder is not None else UNK
        st.status[i] = status if status is not None else UNK
        st.qty[i] = qty if (S["has_qty"] and qty is not None) else (UNK if S["has_qty"] else None)
    for doc, rec in S["register"].get("docs", []):
        st.current[doc] = rec
        st.rec_doc[rec] = doc
    return st


def names(e):
    t = e["t"]
    if t == "CREATE":
        return [e["item"], e["holder"]]
    if t in ("SET", "ADJUST"):
        return [e["item"]]
    if t == "TRANSFER":
        return [e["item"], e["sender"], e["receiver"]]
    if t == "RENAME":
        return []
    if t == "MERGE":
        return [e["absorbed"], e["survivor"]]
    return []


def step(S, E, st, e, alts=frozenset(), log=None):
    """Apply one corrected effective entry to state st (in place). Returns True if it changed or could change
    something (False for an entry with no effect: a retired / absorbed ID or a blocked transfer)."""
    t = e["t"]
    tg = S["toggles"]
    if t == "_CORR_AS_ENTRY":
        x, c = e["src"], e["corr"]
        i = E.find(x.get("item", "")) if x.get("item") else None
        s = c["slot"]
        if x["t"] in ("SET", "CREATE") and s in ("value", "status") and (x["t"] == "CREATE" or x["field"] == "status"):
            st.status[i] = c["value"]
        elif x["t"] in ("SET", "CREATE") and s in ("value", "qty"):
            st.qty[i] = c["value"]
        elif x["t"] == "ADJUST":
            st.qty[i] = st.qty[i] + x["sign"] * (c["value"] - x["amount"])
        elif x["t"] == "TRANSFER":
            if st.holder.get(i) == E.find(x["receiver"]):
                st.holder[i] = E.find(c["value"])
        return True
    # rule 9/10: an entry that names a retired or absorbed ID has no effect (checked on the corrected entry)
    for idn in names(e):
        if idn in st.retired or E.find(idn) in st.absorbed:
            if "T15" in alts and E.find(idn) in st.absorbed and t == "TRANSFER":
                pass
            else:
                if log is not None:
                    log.append(("no_effect", e["n"]))
                return False
    if t == "CREATE":
        i = E.find(e["item"])
        st.exists.add(i)
        st.holder[i] = E.find(e["holder"])
        st.status[i] = e["status"] if e.get("status") is not None else S["default_status"]
        if S["has_qty"]:
            st.qty[i] = e["qty"] if e.get("qty") is not None else 0
        return True
    if t == "OPEN":
        st.current[e["doc"]] = e["record"]
        st.rec_doc[e["record"]] = e["doc"]
        return True
    if t == "SET":
        i = E.find(e["item"])
        if e["field"] == "status":
            st.status[i] = e["value"]
        else:
            st.qty[i] = e["value"]
        return True
    if t == "ADJUST":
        i = E.find(e["item"])
        q = st.qty.get(i)
        st.qty[i] = UNK if q == UNK or q is None else q + e["sign"] * e["amount"]
        return True
    if t == "TRANSFER":
        i = E.find(e["item"])
        ok = True
        if tg.get("check") and st.holder.get(i) != E.find(e["sender"]):
            ok = False
        if tg.get("lock") and st.status.get(i) == tg.get("lock_status"):
            ok = False
        if not ok:
            if log is not None:
                log.append(("blocked", e["n"]))
            return False
        st.holder[i] = E.find(e["receiver"])
        return True
    if t == "SUPERSEDE":
        doc = st.rec_doc.get(e["old"])
        if doc is not None and st.current.get(doc) == e["old"]:
            st.current[doc] = e["new"]
            st.rec_doc[e["new"]] = doc
            return True
        if "T13b" in alts and doc is not None:
            st.current[doc] = e["new"]
            st.rec_doc[e["new"]] = doc
            return True
        return False
    if t == "RENAME":
        if (tg.get("rename_mode") == "retire") != ("T14a" in alts):
            st.retired.add(e["old"])
        return True
    if t == "MERGE":
        a, b = E.find(e["absorbed"]), E.find(e["survivor"])
        for i, h in list(st.holder.items()):
            if h == a:
                st.holder[i] = b
        if "T15" not in alts:
            st.absorbed.add(a)
        return True
    raise ValueError(f"unknown entry type {t}")


def replay(S, alts=frozenset(), view=None, E=None):
    """States: [opening, after eff[0], after eff[1], ...], plus the eff list and the entity map."""
    E = E or Ents(S, alts)
    eff = effective(S, alts, view)
    st = initial_state(S, E)
    if S.get("gap_style") == "leading":
        st = State()
    states = [st.copy()]
    flags = []
    for e in eff:
        changed = step(S, E, st, e, alts)
        flags.append(changed)
        states.append(st.copy())
    return states, eff, E, flags


# ------------------------------------------------------------------------------------------------ query points

def point_index(S, eff, point, alts=frozenset()):
    """Index into states for a single point."""
    k = point["kind"]
    if k == "end":
        return len(eff)
    D = point["date"]
    if k in ("on", "as of") and "T24a" in alts:
        k = "at the start of"
    if k in ("on", "as of", "at the end of"):
        return sum(1 for e in eff if _edate(S, e) <= D)
    if k == "at the start of":
        return sum(1 for e in eff if _edate(S, e) < D)
    raise ValueError(k)


def _edate(S, e):
    if e["t"] == "_CORR_AS_ENTRY":
        return e["date"]
    return entry_date(S, e)


def during_points(S, eff, D):
    """T24 Alt (b): start of D and right after each entry dated D."""
    i0 = sum(1 for e in eff if _edate(S, e) < D)
    pts = [i0]
    for j, e in enumerate(eff):
        if _edate(S, e) == D:
            pts.append(j + 1)
    return pts


def range_points(S, eff, d1, d2, alts=frozenset()):
    """T25: start of D1 and right after each effective entry dated D1..D2 (Alts: end-of-day only; exclusions)."""
    lo_incl, hi_incl = True, True
    if "T25b1" in alts:
        lo_incl = False
    if "T25b2" in alts:
        hi_incl = False
    if "T25b3" in alts:
        lo_incl = hi_incl = False
    if "T25a" in alts:
        pts = [sum(1 for e in eff if _edate(S, e) < d1)]
        dates = sorted({_edate(S, e) for e in eff if d1 <= _edate(S, e) <= d2})
        for d in dates:
            pts.append(sum(1 for e in eff if _edate(S, e) <= d))
        return pts
    if lo_incl:
        pts = [sum(1 for e in eff if _edate(S, e) < d1)]
    else:
        pts = [sum(1 for e in eff if _edate(S, e) <= d1)]
    for j, e in enumerate(eff):
        d = _edate(S, e)
        lo_ok = d >= d1 if lo_incl else d > d1
        hi_ok = d <= d2 if hi_incl else d < d2
        if lo_ok and hi_ok:
            pts.append(j + 1)
    return pts


def view_for(S, point, alts):
    """T7 / T10 Alts: the as-recorded view on the asked date (voids / corrections recorded after it do not count)."""
    if not ({"T7", "T10"} & set(alts)) or point["kind"] == "end":
        return None
    if point["kind"] == "range":
        D, strict = point["d2"], False
    else:
        D = point["date"]
        strict = point["kind"] == "at the start of"
    sp = S["sampler"]
    if sp in ("S1", "S2", "S3"):
        return (D, "", 0) if strict else (D, "99:99", 10 ** 9)
    if sp == "S4":
        return (D, 0, 0) if strict else (D, 10 ** 9, 10 ** 9)
    if sp == "S6":
        return (D, 0) if strict else (D, 10 ** 9)
    return None


# ------------------------------------------------------------------------------------------------ answering

def holder_ent(st, E, item):
    return st.holder.get(E.find(item))


def _held(S, st, E, item, alts):
    h = st.holder.get(E.find(item))
    if "T17" in alts and S["has_qty"] and st.qty.get(E.find(item)) == 0:
        return None
    return h


def answer(S, Q, alts=frozenset()):
    """The label: 0/1 for yes/no rows (negated stem form applied), the gold option text for choice rows,
    UNK when an open card leaves the value unknown (choice rows: NEI), NO_SINGLE when an Alt gives no single answer.

    Yes/no rows: truth(C) is the affirmative core claim (QT question); C' is the declarative of an N1 / N2 / N3 stem.
      A: C   N1: not C   N2: "X no longer holds Y" (its own truth)   N3: not C   N4: not C   N5: not C
      D over N1 / N3: C   D over N2: not "no longer"."""
    if S["world"] == "open":
        return answer_open(S, Q)
    view = view_for(S, Q.get("point", {"kind": "end"}), alts)
    states, eff, E, flags = replay(S, alts, view)
    if Q["form"] == "choice":
        return _affirm(S, Q, states, eff, E, flags, alts)
    form = Q.get("neg", "A")
    uses_nolonger = form == "N2" or (form == "D" and Q.get("dbase") == "N2")
    if uses_nolonger:
        nl = _nolonger(S, Q, states, eff, E, alts)
        if nl in (NO_SINGLE, None):
            return NO_SINGLE
        return int(nl) if form == "N2" else int(not nl)
    pt = Q.get("point", {"kind": "end"})
    if pt.get("kind") in ("on", "as of") and "T24b" in alts and Q["qt"] in ("Q1", "Q2", "Q4"):
        pts = during_points(S, eff, pt["date"])
        vals = [_claim_at(S, Q, states[p], E, alts) for p in pts]
        if form in COMPLEMENT_FORMS:
            return int(any(not v for v in vals)) if "T24b_inner" in alts else int(not any(vals))
        return int(any(vals))
    c = _affirm(S, Q, states, eff, E, flags, alts)
    if c in (NO_SINGLE, None, UNK):
        return NO_SINGLE if c != UNK else UNK
    c = bool(c)
    return int(not c) if form in COMPLEMENT_FORMS else int(c)


def _finish(Q, val):
    """Open-card labels (no Alts): the same form table as answer()."""
    if val in (UNK, NO_SINGLE) or val is None:
        return val
    if Q["form"] == "choice":
        return val
    form = Q.get("neg", "A")
    v = bool(val)
    return int(not v) if form in COMPLEMENT_FORMS else int(v)


def _claim_at(S, Q, st, E, alts):
    kind = Q["kind"]
    if kind == "status":
        s = st.status.get(E.find(Q["item"]))
        if Q["form"] == "choice":
            return s
        return s == Q["value"]
    if kind == "qty":
        q = st.qty.get(E.find(Q["item"]))
        cmpn = CMP_SWAP[Q["cmp"]] if "T22" in alts else Q["cmp"]
        return CMP_FUNCS[cmpn](q, Q["n"])
    if kind == "holder":
        h = _held(S, st, E, Q["item"], alts)
        if Q["form"] == "choice":
            return h
        return h == E.find(Q["holder"])
    raise ValueError(kind)


def _affirm(S, Q, states, eff, E, flags, alts):
    """Truth of the affirmative core claim C (yes/no) or the answer (choice)."""
    qt = Q["qt"]
    point = Q.get("point", {"kind": "end"})
    if qt == "Q3":
        cur = states[-1].current.get(Q["doc"])
        if "T13a" in alts:
            chain = _chain(S, states[-1], Q["doc"])
            if len(chain) >= 2:
                cur = chain[-2]
        if Q["form"] == "choice":
            return cur
        return cur == Q["record"]
    if qt == "Q8":
        return _transfer_took_effect(S, Q["entry"], eff, flags, alts)
    if qt == "Q6":
        st = states[-1]
        X = E.find(Q["holder"])
        if "T39a" in alts and S["has_qty"]:
            cnt = sum(st.qty.get(i) or 0 for i in st.exists if _held(S, st, E, i, alts) == X)
        else:
            cnt = sum(1 for i in st.exists if _held(S, st, E, i, alts) == X
                      and not ("T39b" in alts and S["has_qty"] and st.qty.get(i) == 0))
        cmpn = CMP_SWAP[Q["cmp"]] if "T22" in alts else Q["cmp"]
        return CMP_FUNCS[cmpn](cnt, Q["n"])
    if qt == "Q7":
        st = states[-1]
        X = E.find(Q["holder"])
        held = [c for c in Q["candidates"] if _held(S, st, E, c, alts) == X]
        if len(held) > 1:
            return NO_SINGLE
        return held[0] if held else Q["none_option"]
    if Q.get("still"):
        if "T31b" in alts and not held_at_some_point(S, Q, states, E, alts, eff):
            return NO_SINGLE
        return _held(S, states[-1], E, Q["item"], alts) == E.find(Q["holder"])
    if point["kind"] == "range":
        pts = range_points(S, eff, point["d1"], point["d2"], alts)
        return any(_claim_at(S, Q, states[p], E, alts) for p in pts)
    if point["kind"] in ("on", "as of") and "T24b" in alts:
        pts = during_points(S, eff, point["date"])
        vals = [_claim_at(S, Q, states[p], E, alts) for p in pts]
        if Q["form"] == "choice":
            return vals[0] if len(set(map(str, vals))) == 1 else NO_SINGLE
        return any(vals)
    idx = point_index(S, eff, point, alts)
    return _claim_at(S, Q, states[idx], E, alts)


def _nolonger(S, Q, states, eff, E, alts):
    """Truth of "X no longer holds Y" (T31): X held Y at some point and does not hold it at the end."""
    X = E.find(Q["holder"])
    at_end = _held(S, states[-1], E, Q["item"], alts) == X
    if "T31a" in alts:
        return not at_end
    some = held_at_some_point(S, Q, states, E, alts, eff)
    if "T31b" in alts and not some:
        return NO_SINGLE
    return some and not at_end


def _chain(S, st, doc):
    rec = None
    for d, r in S["register"].get("docs", []):
        if d == doc:
            rec = r
    if rec is None:
        for e in S["entries"]:
            if e["t"] == "OPEN" and e["doc"] == doc:
                rec = e["record"]
    out = [rec]
    while out[-1] != st.current.get(doc):
        nxt = None
        for e in S["entries"]:
            if e["t"] == "SUPERSEDE" and e["old"] == out[-1] and st.rec_doc.get(e["new"]) == doc:
                nxt = e["new"]
        if nxt is None:
            break
        out.append(nxt)
    return out


def _transfer_took_effect(S, n, eff, flags, alts):
    for e, ch in zip(eff, flags):
        if e.get("n") == n and e["t"] == "TRANSFER":
            return bool(ch)
    if "T38" in alts:
        for e in S["entries"]:
            if e["n"] == n and e["t"] == "TRANSFER":
                return True
    return False


def held_at_some_point(S, Q, states, E, alts=frozenset(), eff=None):
    X = E.find(Q["holder"])
    if "T31c" in alts and eff is not None:
        pts = [0] + sorted({sum(1 for e in eff if _edate(S, e) <= d) for d in {_edate(S, e) for e in eff}})
        return any(_held(S, states[p], E, Q["item"], alts) == X for p in pts)
    return any(_held(S, st, E, Q["item"], alts) == X for st in states)


def guard_ok(S, states, eff, E, item, holder):
    """T31 generator guard: X held Y in the opening state or at the end of some date."""
    X = E.find(holder)
    if states[0].holder.get(E.find(item)) == X:
        return True
    for d in sorted({_edate(S, e) for e in eff}):
        p = sum(1 for e in eff if _edate(S, e) <= d)
        if states[p].holder.get(E.find(item)) == X:
            return True
    return False


# ------------------------------------------------------------------------------------------------ open world (T2)

def gap_positions(S, eff):
    """Positions in the effective list after which entries are missing (open cards; chronological listing)."""
    if S.get("gap_style") == "leading":
        return [0]
    out = []
    for g in S.get("gaps", []):
        out.append(sum(1 for e in eff if e["n"] <= g))
    return out


def open_values(S, E=None):
    """End-of-log values on an open card under T2: {item_entity: {"holder", "status", "qty"}} with UNK where the
    last exact setter (after voids and corrections) does not come after every missing entry; plus the states list
    of the shown replay (used only for the T31 guard at the opening point (c))."""
    E = E or Ents(S)
    eff = effective(S)
    gp = gap_positions(S, eff)
    last_gap = max(gp) if gp else -1
    items = {}
    lead = S.get("gap_style") == "leading"
    for item, holder, status, qty in S["register"]["items"]:
        i = E.find(item)
        items[i] = {"holder": (holder, -1), "status": (status, -1), "qty": (qty, -1), "adj": []}
    for pos, e in enumerate(eff):
        t = e["t"]
        if t == "CREATE":
            i = E.find(e["item"])
            items[i] = {"holder": (E.find(e["holder"]), pos),
                        "status": (e["status"] if e.get("status") is not None else S["default_status"], pos),
                        "qty": ((e["qty"] if e.get("qty") is not None else 0) if S["has_qty"] else None, pos),
                        "adj": []}
        elif t == "SET":
            i = E.find(e["item"])
            rec = items.setdefault(i, {"holder": (UNK, -2), "status": (UNK, -2), "qty": (UNK, -2), "adj": []})
            if e["field"] == "status":
                rec["status"] = (e["value"], pos)
            else:
                rec["qty"] = (e["value"], pos)
                rec["adj"] = []
        elif t == "ADJUST":
            i = E.find(e["item"])
            rec = items.setdefault(i, {"holder": (UNK, -2), "status": (UNK, -2), "qty": (UNK, -2), "adj": []})
            rec["adj"].append((pos, e["sign"] * e["amount"]))
        elif t == "TRANSFER":
            i = E.find(e["item"])
            rec = items.setdefault(i, {"holder": (UNK, -2), "status": (UNK, -2), "qty": (UNK, -2), "adj": []})
            rec["holder"] = (E.find(e["receiver"]), pos)
    out = {}
    for i, rec in items.items():
        v = {}
        for f in ("holder", "status", "qty"):
            val, pos = rec[f]
            if pos == -2 or (lead and pos < 0):
                v[f] = UNK
                continue
            known = pos >= last_gap if gp else True
            if pos < 0:
                known = not gp or (False if gp else True)
            if not known:
                v[f] = UNK
            elif f == "qty" and val is not None and val != UNK:
                v[f] = val + sum(d for p, d in rec["adj"] if p > pos)
            else:
                v[f] = val
        out[i] = v
    return out, eff, E


def answer_open(S, Q):
    """Open cards (T2): end-of-log questions only (Q1, Q4, Q5). UNK = the answer depends on a missing entry."""
    vals, eff, E = open_values(S)
    i = E.find(Q["item"])
    v = vals.get(i)
    if v is None:
        return UNK
    kind = Q["kind"]
    form = Q.get("neg", "A")
    if Q["qt"] == "Q4" and Q["form"] == "yn":
        h = v["holder"]
        if h == UNK:
            return UNK
        at_end = h == E.find(Q["holder"])
        if form == "N2" or (form == "D" and Q.get("dbase") == "N2"):
            if not open_guard(S, Q, eff, E):
                return UNK
            nl = not at_end
            return int(nl) if form == "N2" else int(not nl)
        return _finish(Q, at_end)
    if kind == "status":
        s = v["status"]
        if s == UNK:
            return UNK
        return _finish(Q, s if Q["form"] == "choice" else s == Q["value"])
    if kind == "qty":
        q = v["qty"]
        if q == UNK:
            return UNK
        return _finish(Q, CMP_FUNCS[Q["cmp"]](q, Q["n"]))
    if kind == "holder":
        h = v["holder"]
        if h == UNK:
            return UNK
        return _finish(Q, h if Q["form"] == "choice" else h == E.find(Q["holder"]))
    raise ValueError(kind)


def open_guard(S, Q, eff, E):
    """T31 guard on open cards, from known values only: X held Y in the opening register (explicit-marker and
    skipped-number cards, T2 (c)), or at the end of a date after the last missing entry (T2 (a))."""
    X = E.find(Q["holder"])
    if S.get("gap_style") in ("explicit", "skipped"):
        for item, holder, status, qty in S["register"]["items"]:
            if E.find(item) == E.find(Q["item"]) and E.find(holder) == X:
                return True
    gp = gap_positions(S, eff)
    last_gap = max(gp) if gp else 0
    # holder known at end of a date d: the last holder setter at or before the end of d comes after the last gap
    dates = sorted({_edate(S, e) for e in eff})
    for d in dates:
        p = sum(1 for e in eff if _edate(S, e) <= d)
        if p <= last_gap:
            continue
        hold, pos = UNK, -1
        for j, e in enumerate(eff[:p]):
            if e["t"] == "CREATE" and E.find(e["item"]) == E.find(Q["item"]):
                hold, pos = E.find(e["holder"]), j
            elif e["t"] == "TRANSFER" and E.find(e["item"]) == E.find(Q["item"]):
                hold, pos = E.find(e["receiver"]), j
        if pos >= last_gap and hold == X:
            return True
    return False


# ------------------------------------------------------------------------------------------------ generator rules

def check_rules(S):
    """Generator rules checked by replay (section 1 rules 3, 6-10, 19 and transfer sanity). Returns a list of
    violation codes (empty = valid). Used on every structure, twin and metamorphic variant."""
    bad = []
    E = Ents(S)
    ents = expand(S)
    nums = [e["n"] for e in S["entries"]]
    by_n = {e["n"]: e for e in ents if e["t"] not in ("VOID",) or not e.get("_withdraw")}
    voided = set()
    for e in ents:
        if e["t"] == "VOID":
            tgt = next((x for x in S["entries"] if x["n"] == e["target"]), None)
            if tgt is None:
                bad.append("void_target_missing")
                continue
            if tgt["t"] not in ("SET", "ADJUST", "TRANSFER", "CORR", "SUPERSEDE"):
                bad.append("void_target_type")
            if not e.get("_withdraw") and own_key(S, tgt) >= own_key(S, e):
                bad.append("void_before_target")
            voided.add(e["target"])
    if any(e["t"] == "VOID" and e["n"] in voided for e in S["entries"]):
        bad.append("void_voided")
    for e in S["entries"]:
        if e["t"] == "CORR":
            tgt = next((x for x in S["entries"] if x["n"] == e["target"]), None)
            if tgt is None:
                bad.append("corr_target_missing")
                continue
            okslot = (tgt["t"], e["slot"]) in (("SET", "value"), ("ADJUST", "amount"), ("TRANSFER", "receiver"),
                                               ("CREATE", "status"), ("CREATE", "qty"))
            if not okslot:
                bad.append("corr_slot")
            if tgt["t"] == "CREATE" and e["slot"] == "qty" and not S["has_qty"]:
                bad.append("corr_slot")
            if own_key(S, tgt) >= own_key(S, e):
                bad.append("corr_before_target")
            if tgt["t"] == "ADJUST" and e["slot"] == "amount" and e["value"] < 1:
                bad.append("adjust_size")
    if bad:
        return bad
    try:
        states, eff, E, flags = replay(S)
    except (ValueError, KeyError, TypeError) as ex:
        return ["replay_error:" + type(ex).__name__]
    tg = S["toggles"]
    st = initial_state(S, E)
    if S.get("gap_style") == "leading":
        st = State()
    created = set(i for i in st.exists)
    for e in eff:
        t = e["t"]
        # rule 19: no entry names an item before its CREATE (open leading extracts: items before N0 exist)
        if t in ("SET", "ADJUST", "TRANSFER") and E.find(e["item"]) not in st.exists \
                and S.get("gap_style") != "leading":
            bad.append("item_before_create")
        if t == "CREATE":
            if E.find(e["item"]) in st.exists:
                bad.append("create_existing")
            if e["holder"] in st.retired or E.find(e["holder"]) in st.absorbed:
                bad.append("create_names_retired")
        if t == "TRANSFER":
            if E.find(e["sender"]) == E.find(e["receiver"]):
                bad.append("self_transfer")
            if E.find(e["receiver"]) in st.absorbed or e["receiver"] in st.retired:
                if not (e["receiver"] in st.retired and tg.get("rename_mode") == "retire"):
                    bad.append("receiver_absorbed")
                else:
                    bad.append("receiver_retired")
            named_ok = not any(x in st.retired or E.find(x) in st.absorbed for x in names(e))
            if not tg.get("check") and named_ok and S["world"] == "closed":
                if st.holder.get(E.find(e["item"])) != E.find(e["sender"]):
                    bad.append("rule6_sender")
        if t == "MERGE":
            a, b = E.find(e["absorbed"]), E.find(e["survivor"])
            if a == b or a in st.absorbed or b in st.absorbed:
                bad.append("merge_bad")
        if t == "RENAME":
            if E.find(e["old"]) in st.absorbed:
                bad.append("rename_absorbed")
        if t == "SUPERSEDE":
            doc = st.rec_doc.get(e["old"])
            if doc is None or st.current.get(doc) != e["old"]:
                bad.append("rule8_supersede")
            if e["new"] in st.rec_doc:
                bad.append("supersede_not_fresh")
        step(S, E, st, e)
        if S["has_qty"]:
            for i, q in st.qty.items():
                if q is not None and q != UNK and q < 0:
                    bad.append("rule7_negative")
                    break
    # rule 9: no entry before a rename uses the new ID it gives (effect order, corrected values)
    ren = [(effect_key(S, e), e["new"]) for e in S["entries"] if e["t"] == "RENAME"]
    for key, new in ren:
        for e in eff:
            if effect_key(S, e) < key and new in names(e):
                bad.append("rule9_new_id_early")
    # rule 10: a CORRECTION after a rename/merge never uses an ID retired/absorbed at its own point
    for c in S["entries"]:
        if c["t"] == "CORR" and c["slot"] == "receiver":
            tgt = next(x for x in S["entries"] if x["n"] == c["target"])
            if E.find(c["value"]) == E.find(tgt["sender"]):
                bad.append("corr_receiver_is_sender")
            for e in S["entries"]:
                if e["t"] == "RENAME" and e["old"] == c["value"] and tg.get("rename_mode") == "retire" \
                        and effect_key(S, e) < own_key(S, c):
                    bad.append("rule10_corr_retired")
                if e["t"] == "RENAME" and e["new"] == c["value"] and effect_key(S, e) > effect_key(S, tgt):
                    bad.append("rule10_corr_new_id_early")
                if e["t"] == "MERGE" and E.find(e["absorbed"]) == E.find(c["value"]) \
                        and effect_key(S, e) < own_key(S, c):
                    bad.append("rule10_corr_absorbed")
    # rule 8: a voided SUPERSEDE has no other SUPERSEDE of the same document between it and the void (own keys)
    fin = states[-1]
    full_doc = {}
    for d, r in S["register"].get("docs", []):
        full_doc[r] = d
    for e in S["entries"]:
        if e["t"] == "OPEN":
            full_doc[e["record"]] = e["doc"]
    for e in sorted([x for x in S["entries"] if x["t"] == "SUPERSEDE"], key=lambda x: effect_key(S, x)):
        if e["old"] in full_doc:
            full_doc[e["new"]] = full_doc[e["old"]]
    for v in ents:
        if v["t"] != "VOID":
            continue
        tgt = next((x for x in S["entries"] if x["n"] == v["target"]), None)
        if tgt and tgt["t"] == "SUPERSEDE":
            doc = full_doc.get(tgt["old"])
            for e in S["entries"]:
                if e["t"] == "SUPERSEDE" and e is not tgt and full_doc.get(e["old"]) == doc \
                        and own_key(S, tgt) < effect_key(S, e) < own_key(S, v):
                    bad.append("rule8_void_window")
    return sorted(set(bad))
