"""Row plans (draw-order step 1-2, G0 spec 8): everything about a row that is fixed before its numbers are drawn.

A plan holds: version, world, form, gold or gold slot, placement class, side, direction, comparator class and word,
negation parity, <T> representation, option-count bucket, high / low, subset class, data form, style, wording.
Quota plans per card (exact per-cell quotas, 10.1) are drawn as shuffled cycles so each card is balanced.
"""
from __future__ import annotations

import itertools

import draws as D
import lexicon as L
import samplers as SP
from samplers import OPS


class Cycle:
    """A shuffled cycle over a list of values (exact per-cell quotas inside a card)."""

    def __init__(self, rng, values):
        self.rng = rng
        self.values = list(values)
        self.buf = []

    def next(self):
        if not self.buf:
            self.buf = list(self.values)
            self.rng.shuffle(self.buf)
        return self.buf.pop()


def option_bucket_n(rng, form: str, bucket: str, world: str) -> int:
    lo, hi = {"2-4": (2, 4), "5-9": (5, 9), "10-19": (10, 19), "20-60": (20, 26)}[bucket]
    if form == "inv":
        lo = max(lo, 3)
        hi = min(hi, 60)
    return rng.randint(lo, hi)


class CardPlanner:
    def __init__(self, card: dict, rng):
        self.card = card
        self.rng = rng
        sch = card["schema"]
        self.place = Cycle(rng, ["exact", "near", "far", "far"])
        self.dir = Cycle(rng, ["up", "down"])
        self.cmpcls = Cycle(rng, ["inclusive", "strict"])
        self.hl = Cycle(rng, ["high", "low"])
        self.version = Cycle(rng, self._versions())
        # repair r1: exact per-cell quotas inside a card (10.1) are kept by cycles, never by random draws
        self.gold = {}
        self.cmp_exact = {True: Cycle(rng, ["inclusive", "strict"]), False: Cycle(rng, ["inclusive", "strict"])}
        if sch == "bin":
            K = len(card["rules"]["bins"]) + 1
            self.slot = Cycle(rng, list(range(K)))
            self.edge = Cycle(rng, [True] * card.get("edge_k", 3) + [False] * (20 - card.get("edge_k", 3)))
        elif sch == "tier":
            K = len(card["rules"]["tiers"])
            self.slot = Cycle(rng, list(range(K)))
            self.tdec = Cycle(rng, [True])
        elif sch == "mat":
            self.slot = Cycle(rng, list(range(card["rules"]["mat"]["K"])))
            self.edge = Cycle(rng, [True] * 3 + [False] * 17)
        elif sch == "pred":
            self.slot = Cycle(rng, list(range(len(card["hyp_display"]))))
            self.changes = Cycle(rng, [True, False])
        elif sch in ("rank_top",):
            self.bucket = Cycle(rng, ["2-4", "5-9"])
        elif sch == "dec":
            self.bucket = Cycle(rng, ["2-4", "5-9"])
        elif sch == "inv":
            compact = card["rules"]["inv"]["kind"] == "q" and card["rules"]["inv"]["q"]["k"] != "score"
            # repair r1 (option-count plan, 1: INV 67 / 68 / 56 / 34): S3 table cards carry the 10-19 and 20-60 rows
            if compact and card["sampler"] == "S3":
                self.bucket = Cycle(rng, ["2-4"] * 2 + ["5-9"] * 2 + ["10-19"] * 5 + ["20-60"] * 3)
            elif card["sampler"] == "S3":
                self.bucket = Cycle(rng, ["2-4"] * 4 + ["5-9"] * 4 + ["10-19"] * 4)
            else:
                # cases written as sentences: at most 9 cases keep the row under the 2,000-token cap
                self.bucket = Cycle(rng, ["2-4"] * 1 + ["5-9"] * 1)
        elif sch == "rank_order":
            self.items = Cycle(rng, [4, 5])
            # P2 (48 orderings + NOTA) cannot stay under F8's 2,000-token cap (options print twice): P1 only
            self.subset = Cycle(rng, ["P1"])
        self.bform = Cycle(rng, card.get("data_forms") or ["rates"])

    def _versions(self):
        c = self.card
        if len(c["versions"]) == 1:
            return ["full"]
        k = int(round(c["short_rate"] * 20))
        return [c["versions"][1]] * k + ["full"] * (20 - k)

    def world_for(self, version: str) -> str:
        c = self.card
        if version != "full" or c.get("open_pct", 0) <= 0:
            return "closed"
        return "open" if self.rng.randrange(100) < c["open_pct"] else "closed"

    def base(self, form: str, world=None, version=None) -> dict:
        """Version and world are fixed first (a forced world or version never consumes another class's draw)."""
        v = version if version is not None else self.version.next()
        if world is None:
            w = self.world_for(v)
        else:
            w = world if v == "full" else "closed"
        return {"form": form, "version": v, "world": w}

    def gold_next(self, form: str, version: str, world: str) -> bool:
        """Card yes rate as an exact cycle (k yes of 20) per (form, version, world) cell, so every sub-population of a
        card (action-rule rows, open rows, short / no-card rows) carries the card's drawn rate (10.1)."""
        key = (form, version, world)
        if key not in self.gold:
            k = int(round(self.card["yes_rate"] * 20))
            self.gold[key] = Cycle(self.rng, [True] * k + [False] * (20 - k))
        return self.gold[key].next()

    def yn(self, form: str, neg: int = 0, gold=None, world=None, version=None, neg_words: bool = False,
           single: bool = False) -> dict:
        rng = self.rng
        p = self.base(form, world=world, version=version)
        p["gold"] = gold if gold is not None else self.gold_next(form, p["version"], p["world"])
        if form == "yn_thr":
            p["place"] = self.place.next() if p["world"] == "closed" else None
            p["dir"] = self.dir.next()
            if p["place"] == "exact" and single:
                # exact rows (F8-R3-C2): comparator class and polarity parity planned jointly. Given the gold, the
                # comparator class is a balanced cycle and the parity follows (yes exactly when (inclusive, even) or
                # (strict, odd)), so each of the four (comparator x parity) pairs is 1/4 of exact rows and the
                # comparator class carries no label information at d = 0.
                p["cmpcls"] = self.cmp_exact[p["gold"]].next()
                neg = 0 if (p["cmpcls"] == "inclusive") == p["gold"] else 1
            aff = p["gold"] if neg % 2 == 0 else (not p["gold"])
            if p["place"] == "exact" and not single:
                # neg-unit anchors keep parity 0; their negated twin gives the odd row with the same comparator
                p["cmpcls"] = "inclusive" if aff else "strict"
            elif p["place"] != "exact":
                p["cmpcls"] = self.cmpcls.next()
            up = p["dir"] == "up"
            p["side"] = ("below" if aff == up else "above") if p["place"] else None
            op = OPS[(p["dir"], p["cmpcls"])]
            # exact rows use plain comparator words only (no "no fewer / no more than"), so their k_all equals the
            # polarity count and every k_all cell holds (incl, even) + (strict, odd) = 1/2 of its exact rows
            plain = p["place"] == "exact" or neg > 0 or neg_words
            ws = [w["w"] for w in L.COMPARATORS[op] if (w["neg_ok"] or not plain)]
            p["cmp_word"] = rng.choice(ws)
            p["bform"] = self.bform.next()
            # repair r1 (10.1 <T> representation): the representation is drawn with the plan and kept through every
            # redraw of the numbers, so exact rows (T = v must sit on the grid) cannot tilt it toward easy grids
            p["trep"] = D.draw_trep(rng, SP.qtype_of(self.card, self.card["q"]), self.card)
        p["neg"] = neg
        return p

    def choice(self, form: str, world=None) -> dict:
        rng = self.rng
        p = self.base(form, world=world)
        c = self.card
        if form == "bin":
            K = len(c["rules"]["bins"]) + 1
            if K >= 19:
                p["world"] = "closed"                       # K = 19 cards host no open rows (F8-R2-14)
            n = K + (1 if p["world"] == "open" else 0)
            p["n"] = n
            if p["world"] == "open":
                p["slot"] = "CBD" if rng.randrange(n) == n - 1 else self.slot.next()
            else:
                p["slot"] = self.slot.next()
                # edge rows need the full card (SEM-11 edge reading); the cycle is drawn on closed full rows only and
                # its rate (card edge_k of 20) is set so edge rows are 15% of all BIN rows (10.1)
                p["edge_row"] = p["version"] == "full" and self.edge.next()
            p["bform"] = self.bform.next()
        elif form == "tier":
            # repair r1: steps come from the card's feasibility map (cardbuild._tier_feas, drawn at card creation),
            # so a planned (tier, step) is always constructible and the gold tier stays uniform (10.1)
            t = self.slot.next()
            F = c["_tier_F"][t]
            dec = [s for s in F if s is not None]
            if dec and (None not in F or self.tdec.next()):
                want = rng.choice(dec)
            else:
                want = None
            p["slot"], p["step"] = t, want
            p["world"] = "closed"
        elif form == "mat":
            p["slot"] = self.slot.next()
            p["edge_row"] = self.edge.next() and p["version"] == "full"
            p["world"] = "closed"
        elif form == "pred":
            p["slot"] = self.slot.next()
            p["changes"] = self.changes.next()
            p["world"] = "closed"
        elif form in ("rank_top", "dec"):
            b = self.bucket.next()
            n = option_bucket_n(rng, form, b, p["world"])
            if form == "dec":
                n = min(n, 5 + (1 if p["world"] == "open" else 0), len(c.get("actions") or []) +
                        (1 if p["world"] == "open" else 0))
                if b == "5-9" and n < 5:
                    n = 5 if len(c.get("actions") or []) >= 5 or p["world"] == "open" else n
            if p["world"] == "open":
                n = max(n, 3)
            p["n"] = max(2, n)
            p["hl"] = self.hl.next()
            if p["world"] == "open":
                p["slot"] = "CBD" if rng.randrange(p["n"]) == p["n"] - 1 else "det"
            p["tie"] = (p["world"] == "closed" and rng.random() < 0.04 and form == "rank_top")
        elif form == "rank_order":
            p["items"] = self.items.next()
            p["subset"] = self.subset.next()
            p["world"] = "closed"
            if p["items"] == 5:
                n = 25 if p["subset"] == "P1" else 49
                p["slot"] = "NOTA" if rng.randrange(n) == n - 1 else "det"
            else:
                p["slot"] = "det"
        elif form == "inv":
            b = self.bucket.next()
            n = option_bucket_n(rng, form, b, p["world"])
            p["n"] = n
            slot = rng.randrange(n)
            p["slot"] = "ABST" if slot == n - 1 else slot
        return p


