"""Case drawing for program cards: points inside solver-B regions (label-first), near misses (one change away),
threshold moves, open-world omission sets with solver A completions (P sets, XF15 rejection rule)."""
from __future__ import annotations

import model as M
from cardgen import draw_ranges
from examples import _point_in
from solver_b import CardB

NUM = ("count", "qty", "amount")


class Cases:
    def __init__(self, card, r):
        self.card = card
        self.r = r
        self.leg = card["legend"]
        self.cb = CardB(self.leg, card["defs"], card["order"], card["ctype"])
        self.mc = M.Card(card["defs"], card["order"])
        self.ordered = card["ctype"] in ("first", "dlist")
        self.draw = draw_ranges(self.leg)
        self.drawbox = self.cb.draw_box(self.draw)

    def region_for(self, target):
        sp = self.cb.sp
        if target == "none":
            R = self.cb.none_region()
        else:
            R = self.cb.assigned_region(target)
        return sp.inter(R, [self.drawbox])

    def point(self, R, tries=30):
        sp = self.cb.sp
        for _ in range(tries):
            if not R:
                return None
            box = self.r.choice(R)
            c = _point_in(box, self.leg, self.r, self.draw)
            if sp.box_in(sp.point_box(c), R):
                return c
        return None

    def answer(self, case, omitted=()):
        if omitted:
            return M.possible_answers(self.mc, self.leg, {k: v for k, v in case.items() if k not in omitted},
                                      omitted, self.ordered)
        return {self.mc.assigned_term(case, self.ordered)}

    def meets(self, did, case, omitted=(), kind="meets"):
        cc = {k: v for k, v in case.items() if k not in omitted}
        return M.possible_meets(self.mc, self.leg, cc, omitted, did, self.ordered, kind)

    def thresholds(self, did):
        """(slot, grid constant) pairs of a definition's atoms (incl. relative d as ('d', x, e))."""
        out = []
        for at in M.walk_atoms(self.card["defs"][did]):
            for s, cs in M.atom_consts(at):
                for c in cs:
                    out.append((s, c))
        return out

    def move_to_threshold(self, case, did, keep):
        """Move one decisive attribute exactly onto a constant of did, keeping keep(case) true."""
        ths = self.thresholds(did)
        self.r.shuffle(ths)
        for s, c in ths:
            c2 = dict(case)
            if isinstance(s, tuple):
                _, x, e = s
                c2[x] = c2[e] + c
            else:
                if self.leg[s]["type"] in NUM and c < 0:
                    continue
                c2[s] = c
            if keep(c2):
                return c2, s
        return None, None

    def one_change(self, case, s):
        """Candidate values one change away on slot s (grid step / other category value / flag / tag)."""
        a = self.leg[s]
        v = case[s]
        t = a["type"]
        if t in NUM:
            return [x for x in (v - 1, v + 1) if x >= 0]
        if t == "date":
            return [v - 1, v + 1]
        if t == "cat":
            return [x for x in a["values"] if x != v]
        if t == "flag":
            return [not v]
        if t == "tag":
            out = []
            for tg in a["values"]:
                st = set(v)
                st.symmetric_difference_update({tg})
                out.append(tuple(sorted(st)))
            return out
        return []

    def near_miss_for(self, case, target):
        """A slot whose one-change move makes `target` the assigned answer (case near miss), or None."""
        slots = list(self.leg)
        self.r.shuffle(slots)
        for s in slots:
            for v in self.one_change(case, s):
                c2 = dict(case)
                c2[s] = v
                if self.mc.assigned_term(c2, self.ordered) == target:
                    return s
        return None

    def slot_reps(self, s, case):
        """Candidate replacement values for slot s covering every cell of the card's constants."""
        pairs = M.rel_pairs(self.card["defs"])
        for x, e in pairs:
            if s in (x, e):
                ds = M.reps_numeric(sorted({c for d in self.card["defs"].values() for at in M.walk_atoms(d)
                                            if at["t"] == "rel" and (at["a"], at["e"]) == (x, e)
                                            for c in (at["n"], -at["n"], 0)}), None)
                return [case[e] + d for d in ds] if s == x else [case[x] - d for d in ds]
        return M.attr_reps(self.leg, self.card["defs"], s)

    def near_miss_any(self, case, target):
        """Slot whose change to some value makes target the assigned answer (S2 / S3 case near miss)."""
        slots = list(self.leg)
        self.r.shuffle(slots)
        for s in slots:
            for v in self.slot_reps(s, case):
                if v == case[s]:
                    continue
                c2 = dict(case)
                c2[s] = v
                if self.mc.assigned_term(c2, self.ordered) == target:
                    return s
        return None
