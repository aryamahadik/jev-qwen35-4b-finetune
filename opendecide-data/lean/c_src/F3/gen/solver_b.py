"""Solver B: backward version-graph resolver (G0 spec section 3). A different paradigm from solver A and a separate
module: it shares no code with solver_a (an import lint in the G3 report checks this).

It builds a pointer graph over the parsed structure (void edges, correction edges per value, rename edges, timed merge
edges, supersede edges, gap nodes) and resolves each queried value lazily, walking backwards in effect order from the
query point over the entity's whole-log rename closure. Transfer conditions (check, lock) recurse top-down with a
memo. It also returns the decisive path (hops) that sets `depth`, the decisive entry and the mechanisms on the path.
"""
from __future__ import annotations

UNKNOWN = "<UNKNOWN>"

_CMP = {"at least": (lambda a, b: a >= b), "no fewer than": (lambda a, b: a >= b),
        "at most": (lambda a, b: a <= b), "no more than": (lambda a, b: a <= b),
        "more than": (lambda a, b: a > b), "fewer than": (lambda a, b: a < b)}


class Trace:
    def __init__(self):
        self.hops = 0
        self.entries = []      # entry numbers on the decisive path
        self.mech = set()      # VOID, CORRECTION, SUPERSEDE, RENAME, MERGE, CHECK, SET, TRANSFER, ADJUST, CREATE
        self.crossed_gap = False

    def add(self, n, mech=None, hops=1):
        self.hops += hops
        if n is not None:
            self.entries.append(n)
        if mech:
            self.mech.add(mech)

    def merge_from(self, other):
        self.hops += other.hops
        self.entries += other.entries
        self.mech |= other.mech
        self.crossed_gap = self.crossed_gap or other.crossed_gap


class Resolver:
    def __init__(self, S):
        self.S = S
        self.sp = S["sampler"]
        tg = S.get("toggles") or {}
        self.mode = tg.get("rename_mode")
        self.check = bool(tg.get("check"))
        self.lock = bool(tg.get("lock"))
        self.lock_status = tg.get("lock_status")
        self.has_qty = bool(S.get("has_qty"))
        self.default_status = S.get("default_status")
        # --- expand notice withdrawals into void edges
        notice_changes = {}
        for e in S["entries"]:
            if e.get("ref") is not None and self.sp == "S4":
                notice_changes.setdefault(e["ref"], []).append(e["n"])
        self.void_of = {}            # target n -> void entry n
        for e in S["entries"]:
            if e["t"] == "VOID":
                self.void_of[e["target"]] = e["n"]
            elif e["t"] == "WITHDRAW":
                for tn in notice_changes.get(e["target_ref"], []):
                    self.void_of[tn] = e["n"]
        # --- correction edges, one per corrected value: the highest-numbered live correction counts
        self.corr = {}
        for e in sorted((x for x in S["entries"] if x["t"] == "CORR"), key=lambda x: x["n"]):
            if e["n"] in self.void_of:
                continue
            self.corr[(e["target"], e["slot"])] = e
        # --- rename closure (whole log)
        self._uf = {}
        for e in S["entries"]:
            if e["t"] == "RENAME":
                self._union(e["old"], e["new"])
        # --- candidate list in effect order (VOID / CORR / WITHDRAW act on targets, never listed here)
        cands = [e for e in S["entries"] if e["t"] not in ("VOID", "CORR", "WITHDRAW")]
        cands.sort(key=self._key)
        self.order = cands
        self.pos = {e["n"]: i for i, e in enumerate(cands)}
        # rename / merge timeline (renames and merges are never voided or corrected)
        self.retire_at = {}          # old ID -> position from which it is retired
        self.absorb_at = {}          # entity root -> position from which it is absorbed
        for i, e in enumerate(cands):
            if e["t"] == "RENAME" and self.mode == "retire":
                self.retire_at.setdefault(e["old"], i)
            if e["t"] == "MERGE":
                self.absorb_at.setdefault(self._root(e["absorbed"]), i)
        # gap nodes: positions in the candidate order after which entries are missing
        self.gaps = []
        if S.get("world") == "open":
            if S.get("gap_style") == "leading":
                self.gaps = [0]
            else:
                for g in S.get("gaps", []):
                    self.gaps.append(sum(1 for e in cands if e["n"] <= g))
        self._memo = {}
        # opening register
        self.reg_items = {}
        if S.get("gap_style") != "leading":
            for row in S["register"]["items"]:
                self.reg_items[self._root(row[0])] = row
        self.reg_docs = {d: r for d, r in S["register"].get("docs", [])}

    # ------------------------------------------------------------------ helpers
    def _key(self, e):
        if self.sp == "S6":
            return (e.get("eff") or e["date"], e["n"])
        if self.sp == "S5":
            return (e["n"],)
        if self.sp == "S4":
            return (e["date"], e["ref"], e["k"])
        return (e["date"], e.get("time") or "", e["n"])

    def _date(self, e):
        return (e.get("eff") or e["date"]) if self.sp == "S6" else e["date"]

    def _union(self, a, b):
        ra, rb = self._root(a), self._root(b)
        if ra != rb:
            self._uf[rb] = ra

    def _root(self, x):
        seen = 0
        while x in self._uf:
            x = self._uf[x]
            seen += 1
            if seen > 1000:
                raise RuntimeError("rename cycle")
        return x

    def _val(self, e, slot, default):
        c = self.corr.get((e["n"], slot))
        return (c["value"], c["n"]) if c else (default, None)

    def _ids_named(self, e, receiver=None):
        t = e["t"]
        if t == "CREATE":
            return [e["item"], e["holder"]]
        if t in ("SET", "ADJUST"):
            return [e["item"]]
        if t == "TRANSFER":
            return [e["item"], e["sender"], receiver if receiver is not None else e["receiver"]]
        if t == "MERGE":
            return [e["absorbed"], e["survivor"]]
        return []

    def _valid(self, e, i, receiver=None):
        """False if the (corrected) entry names an ID retired or absorbed at its own position i."""
        for idn in self._ids_named(e, receiver):
            r = self.retire_at.get(idn)
            if r is not None and r < i:
                return False
            a = self.absorb_at.get(self._root(idn))
            if a is not None and a < i:
                return False
        return True

    def _gap_between(self, lo, hi):
        """A gap lies at a position p with lo < p <= hi (p = number of candidates before the gap)."""
        return any(lo < g <= hi for g in self.gaps)

    def point_pos(self, point):
        k = point["kind"]
        if k == "end":
            return len(self.order)
        D = point["date"]
        if k in ("on", "as of", "at the end of"):
            return sum(1 for e in self.order if self._date(e) <= D)
        if k == "at the start of":
            return sum(1 for e in self.order if self._date(e) < D)
        raise ValueError(k)

    # ------------------------------------------------------------------ field resolution (backwards)
    def holder(self, item, upto, tr):
        """Holder entity root of `item` (entity root) just before candidate position `upto`."""
        key = ("h", item, upto)
        if key in self._memo:
            v, sub = self._memo[key]
            tr.merge_from(sub)
            return v
        sub = Trace()
        v = self._holder(item, upto, sub)
        self._memo[key] = (v, sub)
        tr.merge_from(sub)
        return v

    def _holder(self, item, upto, tr):
        i = upto - 1
        while i >= 0:
            if (i + 1) in self.gaps:
                tr.crossed_gap = True
                tr.add(None, "GAP")
                return UNKNOWN
            e = self.order[i]
            t = e["t"]
            if t == "TRANSFER" and self._root(e["item"]) == item:
                if e["n"] in self.void_of:
                    tr.add(self.void_of[e["n"]], "VOID")
                    i -= 1
                    continue
                recv, cn = self._val(e, "receiver", e["receiver"])
                if not self._valid(e, i, recv):
                    tr.add(None, "RENAME", hops=1)
                    i -= 1
                    continue
                if self.check or self.lock:
                    sub = Trace()
                    ok = True
                    if self.check:
                        if self.holder(item, i, sub) != self._root(e["sender"]):
                            ok = False
                    if ok and self.lock:
                        if self.status(item, i, sub) == self.lock_status:
                            ok = False
                    tr.add(None, "CHECK", hops=1)
                    tr.merge_from(sub)
                    if not ok:
                        tr.add(None, "CHECKBLOCK", hops=0)   # a stated condition blocks this transfer (R2-11)
                        i -= 1
                        continue
                tr.add(e["n"], "TRANSFER")
                if cn is not None:
                    tr.add(cn, "CORRECTION")
                return self._root(recv)
            if t == "MERGE" and self._valid(e, i):
                sub = Trace()
                before = self.holder(item, i, sub)
                if before == self._root(e["absorbed"]):
                    tr.add(e["n"], "MERGE")
                    tr.merge_from(sub)
                    return self._root(e["survivor"])
            if t == "CREATE" and self._root(e["item"]) == item:
                tr.add(e["n"], "CREATE")
                return self._root(e["holder"])
            i -= 1
        if 0 in self.gaps and upto >= 0:
            tr.crossed_gap = True
            tr.add(None, "GAP")
            return UNKNOWN
        row = self.reg_items.get(item)
        if row is None:
            return UNKNOWN
        tr.add(None, "REGISTER")
        return self._root(row[1])

    def status(self, item, upto, tr):
        key = ("s", item, upto)
        if key in self._memo:
            v, sub = self._memo[key]
            tr.merge_from(sub)
            return v
        sub = Trace()
        v = self._field(item, upto, sub, "status")
        self._memo[key] = (v, sub)
        tr.merge_from(sub)
        return v

    def qty(self, item, upto, tr):
        key = ("q", item, upto)
        if key in self._memo:
            v, sub = self._memo[key]
            tr.merge_from(sub)
            return v
        sub = Trace()
        v = self._field(item, upto, sub, "qty")
        self._memo[key] = (v, sub)
        tr.merge_from(sub)
        return v

    def _field(self, item, upto, tr, field):
        acc = 0
        i = upto - 1
        while i >= 0:
            if (i + 1) in self.gaps:
                tr.crossed_gap = True
                tr.add(None, "GAP")
                return UNKNOWN
            e = self.order[i]
            t = e["t"]
            if t in ("SET", "ADJUST", "CREATE") and self._root(e["item"]) == item:
                writes = (t == "SET" and e["field"] == field) or (t == "ADJUST" and field == "qty") or t == "CREATE"
                if not writes:
                    i -= 1
                    continue
                if t != "CREATE" and e["n"] in self.void_of:
                    tr.add(self.void_of[e["n"]], "VOID")
                    i -= 1
                    continue
                if not self._valid(e, i):
                    tr.add(None, "RENAME")
                    i -= 1
                    continue
                if t == "ADJUST":
                    amt, cn = self._val(e, "amount", e["amount"])
                    acc += e["sign"] * amt
                    tr.add(e["n"], "ADJUST", hops=0)
                    if cn is not None:
                        tr.add(cn, "CORRECTION")
                    i -= 1
                    continue
                if t == "SET":
                    v, cn = self._val(e, "value", e["value"])
                    tr.add(e["n"], "SET")
                else:
                    if field == "status":
                        v, cn = self._val(e, "status", e.get("status"))
                        if v is None:
                            v = self.default_status
                    else:
                        v, cn = self._val(e, "qty", e.get("qty"))
                        if v is None:
                            v = 0
                    tr.add(e["n"], "CREATE")
                if cn is not None:
                    tr.add(cn, "CORRECTION")
                return v + acc if field == "qty" else v
            i -= 1
        if 0 in self.gaps:
            tr.crossed_gap = True
            tr.add(None, "GAP")
            return UNKNOWN
        row = self.reg_items.get(item)
        if row is None:
            return UNKNOWN
        tr.add(None, "REGISTER")
        v = row[2] if field == "status" else row[3]
        if v is None:
            return UNKNOWN
        return v + acc if field == "qty" else v

    # ------------------------------------------------------------------ documents
    def current(self, doc, tr):
        root = self.reg_docs.get(doc)
        if root is None:
            for e in self.order:
                if e["t"] == "OPEN" and e["doc"] == doc:
                    root = e["record"]
                    tr.add(e["n"], "CREATE")
                    break
        else:
            tr.add(None, "REGISTER")
        if root is None:
            return UNKNOWN
        nxt = {}
        for e in self.order:
            if e["t"] != "SUPERSEDE":
                continue
            if e["n"] in self.void_of:
                tr.add(self.void_of[e["n"]], "VOID", hops=0)
                continue
            if e["old"] in nxt:
                raise AssertionError("supersede fork")
            nxt[e["old"]] = e
        cur, seen = root, {root}
        while cur in nxt:
            e = nxt[cur]
            tr.add(e["n"], "SUPERSEDE")
            cur = e["new"]
            if cur in seen:
                raise AssertionError("supersede cycle")
            seen.add(cur)
        return cur

    # ------------------------------------------------------------------ Q8
    def took_effect(self, n, tr):
        if n in self.void_of:
            tr.add(self.void_of[n], "VOID")
            return False
        i = self.pos.get(n)
        if i is None:
            return False
        e = self.order[i]
        recv, cn = self._val(e, "receiver", e["receiver"])
        if cn is not None:
            tr.add(cn, "CORRECTION")
        tr.add(e["n"], "TRANSFER")
        if not self._valid(e, i, recv):
            tr.add(None, "RENAME")
            return False
        item = self._root(e["item"])
        if self.check:
            tr.add(None, "CHECK")
            if self.holder(item, i, tr) != self._root(e["sender"]):
                tr.add(None, "CHECKBLOCK", hops=0)
                return False
        if self.lock:
            tr.add(None, "CHECK")
            if self.status(item, i, tr) == self.lock_status:
                tr.add(None, "CHECKBLOCK", hops=0)
                return False
        return True


# ---------------------------------------------------------------------------------------------- query answering

def solve(S, Q):
    """(label, info). label: 0/1 for yes/no (negated stem form applied), option text for choice, '<UNKNOWN>' when
    the answer depends on a missing entry. info: depth, decisive entry, mechanisms on the path."""
    R = Resolver(S)
    tr = Trace()
    qt, form = Q["qt"], Q["form"]
    pt = Q.get("point") or {"kind": "end"}
    neg = Q.get("neg", "A")

    def item_root():
        return R._root(Q["item"])

    def at(upto, sub):
        kind = Q["kind"]
        if kind == "status":
            v = R.status(item_root(), upto, sub)
            return v if form == "choice" or v == UNKNOWN else (v == Q["value"])
        if kind == "qty":
            v = R.qty(item_root(), upto, sub)
            return v if v == UNKNOWN else _CMP[Q["cmp"]](v, Q["n"])
        if kind == "holder":
            v = R.holder(item_root(), upto, sub)
            if form == "choice" or v == UNKNOWN:
                return v
            return v == R._root(Q["holder"])
        raise ValueError(kind)

    nolonger_val = None
    if qt == "Q3":
        cur = R.current(Q["doc"], tr)
        val = cur if form == "choice" else (cur == Q["record"])
    elif qt == "Q8":
        val = R.took_effect(Q["entry"], tr)
        tr.hops += 1
    elif qt == "Q6":
        X = R._root(Q["holder"])
        cnt, best = 0, Trace()
        items = _all_items(S, R)
        for it in items:
            sub = Trace()
            h = R.holder(it, len(R.order), sub)
            if h == X:
                cnt += 1
            if _held_some_time(R, it, X) and sub.hops > best.hops:
                best = sub
        tr.merge_from(best)
        val = _CMP[Q["cmp"]](cnt, Q["n"])
    elif qt == "Q7":
        X = R._root(Q["holder"])
        held, best = [], Trace()
        for c in Q["candidates"]:
            sub = Trace()
            if R.holder(R._root(c), len(R.order), sub) == X:
                held.append(c)
            if sub.hops > best.hops:
                best = sub
        tr.merge_from(best)
        if len(held) > 1:
            raise AssertionError("Q7 rule 11: more than one listed item held")
        val = held[0] if held else Q["none_option"]
    elif Q.get("still") or neg == "N2" or (neg == "D" and Q.get("dbase") == "N2"):
        X = R._root(Q["holder"])
        sub = Trace()
        h_end = R.holder(item_root(), len(R.order), sub)
        tr.merge_from(sub)
        if h_end == UNKNOWN:
            val = UNKNOWN
        else:
            at_end = h_end == X
            if Q.get("still"):
                val = at_end
            else:
                guard = _guard(R, S, item_root(), X)
                if guard is None:
                    val = UNKNOWN
                else:
                    nolonger_val = guard and not at_end
                    val = at_end
    elif pt["kind"] == "range":
        lo = sum(1 for e in R.order if R._date(e) < pt["d1"])
        pts = [lo] + [i + 1 for i, e in enumerate(R.order)
                      if pt["d1"] <= R._date(e) <= pt["d2"] and e["n"] not in R.void_of]
        vals, best = [], Trace()
        for p in pts:
            sub = Trace()
            vals.append(at(p, sub))
            if sub.hops > best.hops:
                best = sub
        tr.merge_from(best)
        val = UNKNOWN if UNKNOWN in vals else any(vals)
    else:
        val = at(R.point_pos(pt), tr)
    # +1 for each rename alias hop between the question's ID and the ID the decisive entries use (depth, B02)
    if Q.get("item"):
        chain = _rename_chain(S, Q["item"])
        if len(chain) > 1:
            qpos = chain.index(Q["item"]) if Q["item"] in chain else 0
            seen = set()
            for n in tr.entries:
                e = next((x for x in S["entries"] if x["n"] == n), None)
                if e is not None and e.get("item") in chain and e["item"] != Q["item"] and n not in seen:
                    seen.add(n)
                    tr.hops += abs(chain.index(e["item"]) - qpos)
                    tr.mech.add("RENAME")
    info = _info(S, R, tr)
    if val == UNKNOWN:
        return UNKNOWN, info
    if form == "choice":
        return val, info
    if nolonger_val is not None:
        lab = int(nolonger_val) if neg == "N2" else int(not nolonger_val)
        return lab, info
    v = bool(val)
    if neg in ("N1", "N2", "N3", "N4", "N5"):
        v = not v
    return int(v), info


def _rename_chain(S, ident):
    """IDs of one item in rename order (whole log)."""
    back = {e["new"]: e["old"] for e in S["entries"] if e["t"] == "RENAME"}
    fwd = {e["old"]: e["new"] for e in S["entries"] if e["t"] == "RENAME"}
    first = ident
    while first in back:
        first = back[first]
    out = [first]
    while out[-1] in fwd:
        out.append(fwd[out[-1]])
    return out


def _all_items(S, R):
    out = []
    for row in S["register"]["items"]:
        r = R._root(row[0])
        if r not in out:
            out.append(r)
    for e in S["entries"]:
        if e["t"] == "CREATE":
            r = R._root(e["item"])
            if r not in out:
                out.append(r)
    return out


def _held_some_time(R, item, X):
    for p in range(0, len(R.order) + 1):
        if R.holder(item, p, Trace()) == X:
            return True
    return False


def _guard(R, S, item, X):
    """T31 guard: X held Y in the opening state or at the end of some date. On open cards only known values count
    (the register at the opening point, or an end-of-date snapshot that crosses no gap). None = guard fails."""
    if S.get("world") == "open":
        if S.get("gap_style") in ("explicit", "skipped"):
            row = R.reg_items.get(item)
            if row is not None and R._root(row[1]) == X:
                return True
    else:
        if R.holder(item, 0, Trace()) == X:
            return True
    dates = sorted({R._date(e) for e in R.order})
    last_gap = max(R.gaps) if R.gaps else -1
    for d in dates:
        p = sum(1 for e in R.order if R._date(e) <= d)
        if S.get("world") == "open" and p <= last_gap:
            continue
        h = R.holder(item, p, Trace())
        if h == X:
            return True
    return None


def _info(S, R, tr):
    depth = max(1, tr.hops)
    # +1 when the effect order differs from the listing order on the decisive entries
    lst = S.get("list_order")
    path = [n for n in tr.entries if n is not None]
    if lst and len(set(path)) >= 2:
        lpos = {n: i for i, n in enumerate(lst)}
        def okey(n):
            e = next((x for x in S["entries"] if x["n"] == n), None)
            return R._key(e) if e is not None else (0,)
        by_eff = sorted(set(path), key=okey)
        by_list = sorted(set(path), key=lambda n: lpos.get(n, -1))
        if by_eff != by_list:
            depth += 1
    dec = None
    if path:
        def own(n):
            e = next(x for x in S["entries"] if x["n"] == n)
            if e["t"] in ("VOID", "CORR", "WITHDRAW"):
                if R.sp == "S6":
                    return (e["date"], e["n"])
                return R._key(e)
            return R._key(e)
        dec = max(set(path), key=own)
    allents = sorted(S["entries"], key=lambda e: _own_or_eff(S, R, e))
    decile = None
    if dec is not None:
        rank = [e["n"] for e in allents].index(dec)
        decile = min(9, int(10 * rank / max(1, len(allents))))
    return {"depth": depth, "decisive": dec, "decile": decile, "mech": sorted(tr.mech), "path": path,
            "crossed_gap": tr.crossed_gap}


def _own_or_eff(S, R, e):
    if e["t"] in ("VOID", "CORR", "WITHDRAW") and R.sp == "S6":
        return (e["date"], e["n"])
    return R._key(e)
