"""Log builder: draws hidden F3 structures (register, entries, documents) entry by entry and re-checks every section 1
generator rule after each addition (solver_a.check_rules). An entry that breaks a rule is dropped and another is drawn,
so every emitted structure is valid by construction. Samplers (samplers.py) drive it with their own shapes.
"""
from __future__ import annotations

import copy

import solver_a as A
from f3common import (ID_ALPHA, ID_DIGITS, d_add, edit_distance)


def code_ids(rng, prefix, n, taken, length=4, min_dist=3, digits_only=False):
    """n fresh IDs '<prefix>-<code>' with pairwise code distance >= min_dist (against `taken` too)."""
    out = []
    pool_taken = [t for t in taken if t.startswith(prefix + "-")]
    al = ID_DIGITS if digits_only else ID_ALPHA + ID_DIGITS
    tries = 0
    while len(out) < n:
        tries += 1
        if tries > 20000:
            raise RuntimeError("cannot draw ids")
        c = "".join(rng.choice(al) for _ in range(length))
        if not any(ch in ID_DIGITS for ch in c) or c[0] in ID_DIGITS and not digits_only and rng.random() < 0.5:
            continue
        cand = f"{prefix}-{c}"
        if cand in taken or cand in out:
            continue
        if any(edit_distance(cand, t) < min_dist for t in pool_taken + out):
            continue
        out.append(cand)
    return out


def lookalike_of(rng, ident, taken, all_same_prefix):
    """A distinct ID one character away from `ident` and >= 3 away from every other ID of its prefix."""
    pre, code = ident.split("-", 1)
    for _ in range(200):
        i = rng.randrange(len(code))
        al = ID_DIGITS if code[i] in ID_DIGITS else ID_ALPHA
        r = rng.choice(al)
        if r == code[i]:
            continue
        cand = f"{pre}-{code[:i]}{r}{code[i + 1:]}"
        if not any(ch in ID_DIGITS for ch in cand.split("-", 1)[1]):
            continue
        if cand in taken:
            continue
        if any(edit_distance(cand, t) < 2 for t in all_same_prefix if t != ident):
            continue
        return cand
    return None


class Builder:
    """Holds one structure under construction. `S` follows the solver_a schema."""

    def __init__(self, card, rng, *, sampler, n_items, n_holders, n_docs=0, recs_per_doc=(1, 1), in_register=0.6,
                 start_date="2041-03-02", timed=False, d0=None, lookalikes=0, holder_lookalikes=0,
                 qty_range=(1, 60)):
        self.card, self.rng = card, rng
        self.sampler = sampler
        tg = {"rename_mode": card.get("rename_mode"), "check": bool(card.get("check")),
              "lock": bool(card.get("lock")), "lock_status": card.get("lock_status"), "timed": bool(timed)}
        self.S = {"sampler": sampler, "world": "closed", "gap_style": None, "n0": None, "toggles": tg,
                  "has_qty": bool(card.get("has_qty")), "statuses": list(card["statuses"]),
                  "default_status": card["default_status"], "register": {"items": [], "docs": []},
                  "entries": [], "gaps": [], "d0": d0}
        self.taken = set()
        ip, hp = card["item_prefix"], card["holder_prefix"]
        strict = bool(card.get("rule21"))   # 2.1 rows: IDs pairwise >= 3 apart (T16 Alt merges IDs within 2)
        self.ilen, self.idist = (4, 3) if strict else (3, 2)
        self.items = code_ids(rng, ip, n_items, self.taken, length=self.ilen, min_dist=self.idist)
        self.taken |= set(self.items)
        hl = 4 if strict else (2 if n_holders <= 24 else 3)
        self.hlen, self.hdist = hl, (3 if strict else 1)
        self.holders = code_ids(rng, hp, n_holders, self.taken, length=hl, digits_only=True, min_dist=self.hdist)
        self.taken |= set(self.holders)
        # planned look-alike entities (distinct entities; E4)
        self.look_items = {}
        for y in rng.sample(self.items, min(lookalikes, len(self.items))):
            la = lookalike_of(rng, y, self.taken, [t for t in self.taken if t.startswith(ip + "-")])
            if la:
                self.look_items[la] = y
                self.taken.add(la)
                self.items.append(la)
        self.look_holders = {}
        for h in rng.sample(self.holders, min(holder_lookalikes, len(self.holders))):
            la = lookalike_of(rng, h, self.taken, [t for t in self.taken if t.startswith(hp + "-")])
            if la:
                self.look_holders[la] = h
                self.taken.add(la)
                self.holders.append(la)
        self.qty_range = qty_range
        # documents and their root records
        self.docs = []
        self.rec_prefix = {}
        for j in range(n_docs):
            dt_name = card["doc_types"][j % len(card["doc_types"])]
            dpre = card["doc_prefixes"][j % len(card["doc_prefixes"])]
            code = None
            for _ in range(100):
                c = f"{dpre}-{rng.randint(10, 98)}"
                if c not in self.taken:
                    code = c
                    break
            self.taken.add(code)
            self.docs.append(code)
            # repair r2 (G6 choice (a)): one record prefix per card, so a record ID never shares its document's
            # prefix (a Q3 option's prefix no longer points at the queried document)
            self.rec_prefix[code] = card["doc_prefixes"][0] + "R"
        self.doc_type = {d: card["doc_types"][j % len(card["doc_types"])] for j, d in enumerate(self.docs)}
        self.records = set()
        # register
        if card.get("_big_roster_now") and card.get("has_register"):
            in_register = 1.0
        reg_items = [y for y in self.items if rng.random() < in_register] if in_register < 1 else list(self.items)
        self.uncreated = [y for y in self.items if y not in reg_items]
        for y in reg_items:
            h = rng.choice(self.holders)
            s = rng.choice(self.S["statuses"])
            q = rng.randint(*qty_range) if self.S["has_qty"] else None
            self.S["register"]["items"].append([y, h, s, q])
        self.unopened = []
        for d in self.docs:
            r = self.fresh_record(d)
            if rng.random() < 0.75 or sampler in ("S6",):
                self.S["register"]["docs"].append([d, r])
            else:
                self.unopened.append((d, r))
        self.date = start_date
        self.time = "08:00" if timed else None
        self.timed = timed
        self.n = 0
        self.win = {}        # repair r2: focus windows, item id -> (lo, hi) entry positions
        self.dwin = {}       # document -> (lo, hi)
        self.rec_doc = {r: d for d, r in self.S["register"]["docs"]}
        self.rec_doc.update({r: d for d, r in self.unopened})

    # ------------------------------------------------------------------ ids
    def fresh_record(self, doc):
        pre = self.rec_prefix[doc]
        r = code_ids(self.rng, pre, 1, self.taken | self.records, length=4)[0]
        self.records.add(r)
        if hasattr(self, "rec_doc"):
            self.rec_doc[r] = doc
        self.taken.add(r)
        return r

    def fresh_item_id(self):
        r = code_ids(self.rng, self.card["item_prefix"], 1, self.taken, length=self.ilen, min_dist=self.idist)[0]
        self.taken.add(r)
        return r

    def fresh_holder_id(self):
        r = code_ids(self.rng, self.card["holder_prefix"], 1, self.taken, length=self.hlen, digits_only=True,
                     min_dist=self.hdist)[0]
        self.taken.add(r)
        return r

    # ------------------------------------------------------------------ time
    def next_stamp(self, same_day_p=0.3, max_step=4):
        rng = self.rng
        if self.n == 0:
            pass
        elif rng.random() < same_day_p and (not self.timed or self.time < "19:30"):
            pass
        else:
            self.date = d_add(self.date, rng.randint(1, max_step))
            if self.timed:
                self.time = "07:00"
        if self.timed:
            h, m = map(int, self.time.split(":"))
            mins = h * 60 + m + rng.randint(5, 90)
            mins = min(mins, 20 * 60 + 59)
            self.time = f"{mins // 60:02d}:{mins % 60:02d}"
        return self.date, self.time

    # ------------------------------------------------------------------ state
    def state(self):
        states, eff, E, flags = A.replay(self.S)
        return states[-1], E

    def valid(self):
        return not A.check_rules(self.S)

    def try_add(self, e, stamp=True):
        """Append entry e (dict without n/date) if every generator rule still holds. Returns the entry or None."""
        saved = (self.date, self.time, self.n)
        if stamp:
            d, t = self.next_stamp()
        else:
            d, t = self.date, self.time
        e = dict(e)
        e["n"] = self.n + 1
        e.setdefault("date", d)
        if self.timed:
            e.setdefault("time", t)
        else:
            e["time"] = None
        self.S["entries"].append(e)
        bad = A.check_rules(self.S)
        if bad:
            self.S["entries"].pop()
            self.date, self.time, self.n = saved
            return None
        self.n += 1
        return e

    # ------------------------------------------------------------------ random entries
    # ------------------------------------------------------------------ focus windows (repair r2)
    def set_windows(self, n_total, k=None, docs=True, min_hi=3, chains=None, exclude=()):
        """Planted chains (repair r2; G10 depth, decile and mechanism targets). Up to k existing items get a planted
        decisive chain: a writer (SET for status, TRANSFER for holder) plus the planned hops (correction of the
        writer, a later write that is voided, renames, a merge of the holder), placed at distinct positions inside a
        window [lo, hi) whose end hi is uniform over the log, so the decisive entry lands at a uniform decile. From
        lo on, the item is never drawn at random (only its planned steps touch it), so the chain stays decisive.
        One document may get a focus window (SUPERSEDE drawn on it more often, frozen after hi). Every planted entry
        still has to pass check_rules; a step that fails is skipped and the chain is simply shallower."""
        rng = self.rng
        pool = [y for y in self.items if y not in self.look_items and y not in exclude]
        if chains is None:
            if k is None:
                k = rng.choice([1, 2, 2, 3])
            chains = [("status" if rng.random() < 0.5 else "holder", rng.choice([2, 3, 3, 4, 4])) for _ in range(k)]
        rng.shuffle(pool)
        pool = pool[:max(1, len([y for y in self.items if y not in self.look_items]) - 1)]   # keep a free item
        self.chains = getattr(self, "chains", [])
        for (field, want), y in zip(chains, pool):
            steps = self._chain_steps(field, want)
            # the chain's last step lands at a planned decile. A chain of L steps cannot end before position L, so
            # its decile is drawn from the feasible ones (leaning early); shallow chains fill the early deciles,
            # deep chains the later ones (repair r2: no truncation, so planned depth is kept)
            L = len(steps)
            while L > n_total and steps:
                steps = steps[:-1]
                if steps and steps[-1] in ("VSET", "VTR"):
                    steps = steps[:-1]
                L = len(steps)
            if not steps:
                continue
            tmin = max(0, -(-10 * L // n_total) - 1)
            if self.card.get("world") == "open":
                tmin = max(tmin, 4)    # open cards: a yes/no answer needs the chain after the hidden entries
            ts = list(range(min(tmin, 9), 10))
            t = rng.choices(ts, weights=[1.0 + 1.2 * (9 - x) / 9 for x in ts])[0]
            hi = max(L, min(n_total, int((t + rng.random()) * n_total / 10) + 1))
            span = len(steps) + rng.randint(0, 3)
            lo = max(0, hi - span)
            pos = sorted(rng.sample(range(lo, hi), len(steps)))
            self.win[y] = (lo, lo)
            self.chains.append({"item": y, "field": field, "steps": steps, "pos": pos, "i": 0, "w_n": None,
                                "v_n": None, "want": want})
        if docs and self.docs:
            d = rng.choice(self.docs)
            hi = rng.randint(min(min_hi, n_total), n_total)
            self.dwin[d] = (max(0, hi - rng.randint(4, 9)), hi)
            if "SUPERSEDE" in self.card["mechs"] and self.sampler not in ("S6",):
                # repair r2 (G7: Q3 yes/no rows were 34% yes, since a "yes" needs a superseded document): the focus
                # document gets a planted chain of 1-3 supersedes inside its window
                k = rng.choice([1, 2, 2, 3])
                lo, hi2 = self.dwin[d]
                if hi2 - lo >= k:
                    self.chains = getattr(self, "chains", [])
                    self.chains.append({"item": None, "doc": d, "field": "doc", "steps": ["SUP"] * k,
                                        "pos": sorted(rng.sample(range(lo, hi2), k)), "i": 0, "w_n": None,
                                        "v_n": None, "want": k + 1})

    def plant_now(self, Y, field, want, first=None):
        """S2 (target-first): plant Y's whole chain at the current point, in one run of entries (repair r2)."""
        ch = {"item": Y, "field": field, "steps": self._chain_steps(field, want, first=first), "pos": [], "i": 0,
              "w_n": None, "v_n": None, "want": want}
        ch["pos"] = [0] * len(ch["steps"])
        self.chains = getattr(self, "chains", []) + [ch]
        ci = len(self.chains) - 1
        while ch["i"] < len(ch["steps"]):
            st, E = self.state()
            e = self._chain_entry(ch, ch["steps"][ch["i"]], st, E)
            if e is None:
                self._chain_skip(ch)
                continue
            self.chain_done(ci, self.try_add(e))
        return ch

    def _chain_steps(self, field, want, first=None):
        rng, m = self.rng, set(self.card["mechs"])
        sp = self.sampler
        opts = []
        if "CORR" in m:
            opts.append("CORR")
        if "VOID" in m:
            opts += ["VPAIR"] * 4          # S4: the void is a withdrawal of the write's notice (R1-21)
        if "RENAME" in m and self.S["toggles"]["rename_mode"] and sp != "S6":
            opts += ["RENY", "RENY"] if field == "status" else ["RENY", "RENH"]
        if field == "holder" and "MERGE" in m and sp != "S6":
            opts += ["MERGEH"] * 2
        rng.shuffle(opts)
        # the card's own rename or merge leads most chains, so it is decisive on about half of the rows where it
        # appears (R2-11) and on >= 8% of rows (G10)
        if first is None and rng.random() < 0.75:
            lead = [h for h in ("RENY", "RENH", "MERGEH") if h in opts]
            if "MERGEH" in lead and rng.random() < 0.6:
                first = "MERGE"
            elif lead:
                first = "RENAME"
        fh = {"VOID": "VPAIR", "CORR": "CORR", "RENAME": "RENY", "MERGE": "MERGEH"}.get(first)
        if fh in opts:
            opts.remove(fh)
            opts.insert(0, fh)
        hops = opts[:max(0 if fh is None else 1, want - 1)]
        steps = ["W"]
        tail = []
        for h in hops:
            if h == "VPAIR":
                tail.append(["VSET" if field == "status" else "VTR", "VOID"])
            else:
                tail.append([h])
        rng.shuffle(tail)
        for t in tail:
            steps += t
        return steps

    def chain_next(self, st, E):
        """The next planted entry due at this position: (entry, token) or (None, None)."""
        for ci, ch in enumerate(getattr(self, "chains", [])):
            while ch["i"] < len(ch["steps"]) and ch["pos"][ch["i"]] <= self.n:
                e = self._chain_entry(ch, ch["steps"][ch["i"]], st, E)
                if e is not None:
                    return e, ci
                self._chain_skip(ch)
        return None, None

    def chain_done(self, ci, got):
        ch = self.chains[ci]
        step = ch["steps"][ch["i"]]
        if got is None:
            self._chain_skip(ch)
            return
        if step == "W":
            ch["w_n"] = got["n"]
            if got["t"] == "CREATE" and got["item"] in self.uncreated:
                self.uncreated.remove(got["item"])
        elif step in ("VSET", "VTR"):
            ch["v_n"] = got["n"]
        ch["i"] += 1

    def _chain_skip(self, ch):
        step = ch["steps"][ch["i"]]
        ch["i"] += 1
        if step == "W":
            ch["i"] = len(ch["steps"])        # no writer: abandon the chain (the item stays frozen)
        elif step in ("VSET", "VTR") and ch["i"] < len(ch["steps"]) and ch["steps"][ch["i"]] == "VOID":
            ch["i"] += 1

    def _chain_entry(self, ch, step, st, E):
        if step == "SUP":
            d = ch["doc"]
            if d not in st.current:
                return None
            return {"t": "SUPERSEDE", "old": st.current[d], "new": self.fresh_record(d)}
        Y = ch["item"]
        r = E.find(Y)
        if r not in st.exists:
            if step == "W" and Y in self.uncreated:
                return self.cand_entry("CREATE", st, E, item=Y)   # the creation is the chain's writer
            return None
        if step == "W":
            return self.cand_entry("SET" if ch["field"] == "status" else "TRANSFER", st, E, item=Y)
        if step == "VSET":
            return self.cand_entry("SET", st, E, item=Y)
        if step == "VTR":
            return self.cand_entry("TRANSFER", st, E, item=Y)
        if step == "VOID":
            if not ch["v_n"]:
                return None
            if self.sampler == "S4":
                v = next((x for x in self.S["entries"] if x["n"] == ch["v_n"]), None)
                ref = v.get("ref") if v else None
                ents = [x for x in self.S["entries"] if x.get("ref") == ref]
                if ref is None or any(x["t"] not in ("SET", "ADJUST", "TRANSFER", "CORR", "SUPERSEDE") for x in ents) \
                        or any(x["t"] == "WITHDRAW" and x.get("target_ref") == ref for x in self.S["entries"]):
                    return None
                return {"t": "WITHDRAW", "target_ref": ref}
            return {"t": "VOID", "target": ch["v_n"]}
        if step == "CORR":
            w = next((x for x in self.S["entries"] if x["n"] == ch["w_n"]), None)
            if w is None or self.is_voided(w["n"]):
                return None
            if w["t"] == "SET":
                vals = [v for v in self.S["statuses"] if v != w["value"]]
                return {"t": "CORR", "target": w["n"], "slot": "value", "value": self.rng.choice(vals)}
            if w["t"] == "TRANSFER":
                live = [x for x in self.live_holders(st, E) if E.find(x) not in (E.find(w["receiver"]),
                                                                                 E.find(w["sender"]))]
                if not live:
                    return None
                return {"t": "CORR", "target": w["n"], "slot": "receiver", "value": self.rng.choice(live)}
            if w["t"] == "CREATE" and ch["field"] == "status":
                vals = [v for v in self.S["statuses"] if v != w.get("status")]
                return {"t": "CORR", "target": w["n"], "slot": "status", "value": self.rng.choice(vals)}
            return None
        if step == "RENY":
            if not self.S["toggles"]["rename_mode"]:
                return None
            return {"t": "RENAME", "kind": "item", "old": self.name_of(Y, E, st), "new": self.fresh_item_id()}
        h = st.holder.get(r)
        if h is None:
            return None
        if step == "RENH":
            if not self.S["toggles"]["rename_mode"]:
                return None
            return {"t": "RENAME", "kind": "holder", "old": self.holder_name(h, E, st), "new": self.fresh_holder_id()}
        if step == "MERGEH":
            live = self.live_holders(st, E)
            a = self.holder_name(h, E, st)
            others = [x for x in live if E.find(x) != E.find(a)]
            if a not in live or len(live) < 3 or not others:
                return None
            return {"t": "MERGE", "absorbed": a, "survivor": self.rng.choice(others)}
        return None

    def _wst(self, lo_hi):
        lo, hi = lo_hi
        return "frozen" if self.n >= hi else ("active" if self.n >= lo else "pending")

    def _roots(self, E, which):
        return {E.find(y) for y, w in self.win.items() if self._wst(w) == which}

    def _docs(self, which):
        return {d for d, w in self.dwin.items() if self._wst(w) == which}

    def _about(self, x, E, depth=0):
        """(item root, doc) an entry is about, following VOID and CORR targets."""
        if depth > 6 or x is None:
            return None, None
        if x["t"] in ("VOID", "CORR"):
            tgt = next((e for e in self.S["entries"] if e["n"] == x.get("target")), None)
            return self._about(tgt, E, depth + 1)
        if x["t"] == "SUPERSEDE":
            return None, self.rec_doc.get(x["old"])
        if x.get("item"):
            return E.find(x["item"]), None
        return None, None

    def _touches_frozen(self, x, E, fr_items, fr_docs):
        it, d = self._about(x, E)
        return (it is not None and it in fr_items) or (d is not None and d in fr_docs)

    def _frozen_holders(self, st, E, fr_items):
        return {E.find(st.holder.get(r)) for r in fr_items if st.holder.get(r) is not None}

    def touches_frozen(self, x):
        """Public check (S4 withdrawals): does entry x (or an entry it points at) concern a frozen item or doc?"""
        if not self.win and not self.dwin:
            return False
        st, E = self.state()
        return self._touches_frozen(x, E, self._roots(E, "frozen"), self._docs("frozen"))

    def cand_entry(self, kind, st, E, *, item=None, target_types=None):
        """One random entry of `kind` given the current end state. None if impossible."""
        rng, S = self.rng, self.S
        alive_items = [i for i in self.all_item_ids() if E.find(i) in st.exists]
        if kind == "CREATE":
            if not self.uncreated:
                return None
            if item is None and self.win:
                frz = {y for y, w in self.win.items() if self._wst(w) == "frozen"}
                cand = [y for y in self.uncreated if y not in frz]
                if not cand:
                    return None
                y = cand[0]
            else:
                y = self.uncreated[0] if item is None else item
            h = rng.choice(self.live_holders(st, E))
            blank_s = rng.random() < self.card.get("blank_rate", 0.0)
            blank_q = rng.random() < self.card.get("blank_rate", 0.0)
            e = {"t": "CREATE", "item": y, "holder": h,
                 "status": None if blank_s else rng.choice(S["statuses"]),
                 "qty": (None if blank_q else rng.randint(*self.qty_range)) if S["has_qty"] else None}
            return e
        if kind == "OPEN":
            if not self.unopened:
                return None
            d, r = self.unopened[0]
            return {"t": "OPEN", "record": r, "doc": d}
        if not alive_items and kind in ("SET", "SETQ", "ADJUST", "TRANSFER"):
            return None
        fr = ac = frd = acd = frh = set()
        if self.win or self.dwin:
            fr, ac = self._roots(E, "frozen"), self._roots(E, "active")
            frd, acd = self._docs("frozen"), self._docs("active")
            frh = self._frozen_holders(st, E, fr)
        if item is None and (fr or ac) and alive_items:
            pool = [i for i in alive_items if E.find(i) not in fr]
            if not pool:
                if kind in ("SET", "SETQ", "ADJUST", "TRANSFER"):
                    return None
                y = None
            else:
                y = rng.choices(pool, weights=[6.0 if E.find(i) in ac else 1.0 for i in pool])[0]
        else:
            y = item if item is not None else (rng.choice(alive_items) if alive_items else None)
        if kind == "SET":
            cur = st.status.get(E.find(y))
            vals = [v for v in S["statuses"] if v != cur]
            return {"t": "SET", "item": self.name_of(y, E, st), "field": "status", "value": rng.choice(vals)}
        if kind == "SETQ":
            if not S["has_qty"]:
                return None
            return {"t": "SET", "item": self.name_of(y, E, st), "field": "qty", "value": rng.randint(*self.qty_range)}
        if kind == "ADJUST":
            if not S["has_qty"]:
                return None
            q = st.qty.get(E.find(y))
            if q is None or q == A.UNK:
                return None
            sign = rng.choice((1, -1)) if q >= 2 else 1
            amt = rng.randint(1, max(1, min(25, q - 1))) if sign < 0 else rng.randint(1, 25)
            return {"t": "ADJUST", "item": self.name_of(y, E, st), "sign": sign, "amount": amt}
        if kind == "TRANSFER":
            h = st.holder.get(E.find(y))
            live = [x for x in self.live_holders(st, E) if E.find(x) != h]
            if not live or h is None:
                return None
            recv = rng.choice(live)
            sender = self.holder_name(h, E, st)
            if S["toggles"]["check"] and rng.random() < self.card.get("wrong_sender_p", 0.3):
                others = [x for x in self.live_holders(st, E) if E.find(x) not in (h, E.find(recv))]
                if others:
                    sender = rng.choice(others)
            return {"t": "TRANSFER", "item": self.name_of(y, E, st), "sender": sender, "receiver": recv}
        if kind == "VOID":
            cands = [x for x in S["entries"] if x["t"] in (target_types or ("SET", "ADJUST", "TRANSFER", "CORR",
                                                                          "SUPERSEDE"))
                     and not self.is_voided(x["n"])]
            if fr or frd:
                cands = [x for x in cands if not self._touches_frozen(x, E, fr, frd)]
            if not cands:
                return None
            if (ac or acd) and rng.random() < 0.7:
                foc = [x for x in cands if self._about(x, E)[0] in ac or self._about(x, E)[1] in acd]
                if foc:
                    return {"t": "VOID", "target": foc[-1 if len(foc) < 2 or rng.random() < 0.75 else -2]["n"]}
            w = [1.0 + 2.0 * (i >= len(cands) - 4) for i in range(len(cands))]
            tgt = rng.choices(cands, weights=w)[0]
            return {"t": "VOID", "target": tgt["n"]}
        if kind == "CORR":
            cands = [x for x in S["entries"] if x["t"] in ("SET", "ADJUST", "TRANSFER", "CREATE")
                     and not self.is_voided(x["n"])]
            if self.card.get("encoding") in ("rec", "table"):
                # repair r2: record and table rows never correct an increase or decrease (the 'correct increase' /
                # 'correct decrease' actions are outside the independent solver B's record grammar)
                cands = [x for x in cands if x["t"] != "ADJUST"]
            if fr:
                cands = [x for x in cands if not self._touches_frozen(x, E, fr, frd)]
            if not cands:
                return None
            tgt = rng.choice(cands)
            if ac and rng.random() < 0.7:
                foc = [x for x in cands if self._about(x, E)[0] in ac]
                if foc:
                    tgt = foc[-1]
            if tgt["t"] == "SET":
                if tgt["field"] == "status":
                    vals = [v for v in S["statuses"] if v != tgt["value"]]
                    return {"t": "CORR", "target": tgt["n"], "slot": "value", "value": rng.choice(vals)}
                return {"t": "CORR", "target": tgt["n"], "slot": "value",
                        "value": rng.randint(*self.qty_range)}
            if tgt["t"] == "ADJUST":
                return {"t": "CORR", "target": tgt["n"], "slot": "amount",
                        "value": max(1, tgt["amount"] + rng.choice((-3, -2, -1, 1, 2, 3)))}
            if tgt["t"] == "TRANSFER":
                live = [x for x in self.live_holders(st, E) if x not in (tgt["receiver"], tgt["sender"])]
                if not live:
                    return None
                return {"t": "CORR", "target": tgt["n"], "slot": "receiver", "value": rng.choice(live)}
            if tgt["t"] == "CREATE":
                if S["has_qty"] and rng.random() < 0.5:
                    return {"t": "CORR", "target": tgt["n"], "slot": "qty", "value": rng.randint(*self.qty_range)}
                vals = [v for v in S["statuses"] if v != tgt.get("status")]
                return {"t": "CORR", "target": tgt["n"], "slot": "status", "value": rng.choice(vals)}
        if kind == "SUPERSEDE":
            docs = [d for d in self.docs if d in st.current and d not in frd]
            if not docs:
                return None
            d = rng.choices(docs, weights=[6.0 if x in acd else 1.0 for x in docs])[0]
            return {"t": "SUPERSEDE", "old": st.current[d], "new": self.fresh_record(d)}
        if kind == "RENAME":
            if not S["toggles"]["rename_mode"]:
                return None
            if ac and rng.random() < 0.75:
                act = [i for i in alive_items if E.find(i) in ac]
                if act:
                    y = rng.choice(act)
                    return {"t": "RENAME", "kind": "item", "old": self.name_of(y, E, st), "new": self.fresh_item_id()}
            if rng.random() < 0.5 and alive_items and y is not None:
                y0 = self.name_of(y, E, st)
                return {"t": "RENAME", "kind": "item", "old": y0, "new": self.fresh_item_id()}
            live = [h for h in self.live_holders(st, E) if E.find(h) not in frh]
            if not live:
                return None
            h0 = rng.choice(live)
            return {"t": "RENAME", "kind": "holder", "old": h0, "new": self.fresh_holder_id()}
        if kind == "MERGE":
            live = self.live_holders(st, E)
            if len(live) < 3:
                return None
            if ac and rng.random() < 0.7:
                hs = [self.holder_name(st.holder[r], E, st) for r in ac if st.holder.get(r) is not None]
                hs = [h for h in hs if h in live and E.find(h) not in frh]
                if hs:
                    a = rng.choice(hs)
                    return {"t": "MERGE", "absorbed": a, "survivor": rng.choice([x for x in live if x != a])}
            okl = [h for h in live if E.find(h) not in frh]
            if len(okl) < 1:
                return None
            a = rng.choice(okl)
            b = rng.choice([x for x in live if x != a])
            return {"t": "MERGE", "absorbed": a, "survivor": b}
        return None

    # ------------------------------------------------------------------ names
    def all_item_ids(self):
        out = list(self.items)
        for e in self.S["entries"]:
            if e["t"] == "RENAME" and e["kind"] == "item":
                out.append(e["new"])
        return out

    def name_of(self, y, E, st):
        """The ID to use for entity of y now: the latest valid ID (renamed IDs under retire)."""
        root = E.find(y)
        cur = root
        changed = True
        while changed:
            changed = False
            for e in self.S["entries"]:
                if e["t"] == "RENAME" and e["old"] == cur:
                    cur, changed = e["new"], True
        return cur

    def holder_name(self, h_root, E, st):
        return self.name_of(h_root, E, st)

    def live_holders(self, st, E):
        """Valid holder IDs now (latest IDs; never absorbed)."""
        out = []
        roots = []
        for h in self.holders:
            r = E.find(h)
            if r in st.absorbed or r in roots:
                continue
            roots.append(r)
            out.append(self.name_of(h, E, st))
        return out

    def is_voided(self, n):
        for e in self.S["entries"]:
            if e["t"] == "VOID" and e["target"] == n:
                return True
        return False

    # ------------------------------------------------------------------ forward run
    def run(self, n_entries, weights, max_tries=12):
        """Forward Markov draw of n_entries valid entries with the given type weights."""
        kinds = list(weights)
        w = [weights[k] for k in kinds]
        fails = 0
        while self.n < n_entries and fails < n_entries * 30:
            st, E = self.state()
            ce, ci = self.chain_next(st, E)
            if ce is not None:
                self.chain_done(ci, self.try_add(ce))
                continue
            ok = False
            for _ in range(max_tries):
                k = self.rng.choices(kinds, weights=w)[0]
                if k == "CREATE" and not self.uncreated:
                    continue
                e = self.cand_entry(k, st, E)
                if e is None:
                    continue
                got = self.try_add(e)
                if got is not None:
                    if k == "CREATE":
                        self.uncreated.remove(e["item"])
                    if k == "OPEN":
                        self.unopened.pop(0)
                    ok = True
                    break
            if not ok:
                fails += 1
        return self.n >= n_entries
