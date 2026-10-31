"""Frame builders: (card, frame, want) -> Struct + query, with gold from solver A (accept / reject toward the wanted
label or gold class). S2 places literals label-first at the boundary (at X / one unit step / farther) and plants
near-miss records; S1 / S3 / S4 / S6 draw forward and accept or reject."""
from __future__ import annotations

import copy
import random
from fractions import Fraction

from f9alt import REWRITE, rewrite
from f9ast import atoms
from f9lex import CMP_T10, CMP_T35, id_key
from f9samp import (BINS, Retry, add_unknowns, card_base_day, col_index, col_vals, draw_atom, draw_pred,
                    filter_cols, main_table, pick_bin, rand_num, s3_tables, s5_pivot, s6_order, s6_table,
                    unlisted_id)
from f9solve_a import CBD, NO_RECORD, NONE, SPECIALS, TIE, Reject, SolverA, Undefined, cmp_op


def solve(card, st, q, shown=None, alt=None):
    q2 = rewrite(q, alt) if alt and alt[0] in REWRITE else q
    return SolverA(st, card).answer(q2, alt=(alt if alt and alt[0] not in REWRITE else None), shown=shown)


def choose_lit(v, op, want, step, rng, lo=None, hi=None, placement=None):
    """A literal X (multiple of step) so that cmp(v, op, X) == want; placement: at / step / far (S2 3.2)."""
    pl = placement or rng.choice(["at", "step", "far"])
    cands = []
    for k in range(-25, 26):
        x = v + k * step
        if x <= 0:
            continue
        if lo is not None and x < lo:
            continue
        if hi is not None and x > hi:
            continue
        if cmp_op(v, op, x) != want:
            continue
        d = abs(k)
        b = "at" if d == 0 else ("step" if d == 1 else "far")
        cands.append((b, x))
    pref = [x for b, x in cands if b == pl]
    if pref:
        return rng.choice(pref), pl
    if cands:
        b, x = rng.choice(cands)
        return x, b
    raise Retry("no literal")


def lit_str(x, dp):
    from f9fmt import dec_str
    x = Fraction(x)
    return dec_str(x) if dp else str(int(x))


class Builder:
    def __init__(self, card, rng: random.Random):
        self.card = card
        self.rng = rng
        self.s = card["sampler"]

    # -------------------------------------------------------------------------------------------- structs
    def struct(self, want=None):
        """Size hint (1.8): after a row overflows its token cap, the next draw keeps its bin with fewer rows (then
        fewer columns), set by the row builder in self.size_hint = {bin, max_rows, max_cols}."""
        card, rng = self.card, self.rng
        hint = getattr(self, "size_hint", None) or {}
        force = (want or {}).get("bin")
        b = pick_bin(self.s if self.s != "S5" else "S1", rng, force=force, weights=hint.get("w"))
        bins = BINS.get(self.s, BINS["S1"])
        bi = bins.index(b)
        while (hint.get(bi) or {}).get("redirect") is not None:
            bi = hint[bi]["redirect"]
            b = bins[bi]
        hb = hint.get(bi) or {}
        if hb.get("dead"):
            raise Retry("bin closed (1.8 cap)")
        self.last_bin = bi
        hi_cap = hb.get("max_rows") or 10 ** 6
        hint = hb

        def size(lo, hi):
            hi2 = max(lo, min(hi, hi_cap))
            return rng.randint(lo, hi2)
        need0 = (want or {}).get("min_rows") or 0
        if need0 > b[1]:  # a pick needs at least that many eligible ids: the smallest bin that holds them
            fits = [x for x in bins if x[1] >= need0]
            b = fits[0] if fits else bins[-1]
            bi = bins.index(b)
            hb = hint.get(bi) or {}
            if hb.get("dead"):
                raise Retry("bin closed (1.8 cap)")
            hi_cap = max(need0, hb.get("max_rows") or 10 ** 6)
            hint = hb
            self.last_bin = bi
        if self.s in ("S1", "S2", "S4"):
            lo, hi = b[0], b[1]
            need = (want or {}).get("min_rows") or 0
            lo = max(lo, min(need, hi))
            n = size(lo, hi)
            compact = self.s == "S4" and b[0] >= 81
            t = main_table(card, rng, n, compact=compact, max_cols=hint.get("max_cols"), lean=bool(hint.get("lean")),
                           keep_note=bool(getattr(self, "force_note", False)))
            return {"sampler": self.s, "tables": [t], "bin": BINS[self.s].index(b), "compact": compact}
        if self.s == "S3":
            dim, fact, orph = s3_tables(card, rng, size(b[0], b[1]))
            return {"sampler": "S3", "tables": [dim, fact], "orphans": orph, "bin": BINS["S3"].index(b)}
        if self.s == "S6":
            t = s6_table(card, rng, size(b[0], b[1]))
            s6_order(card, t, rng)
            return {"sampler": "S6", "tables": [t], "bin": BINS["S6"].index(b)}
        if self.s == "S5":
            return {"sampler": "S5", "tables": [], "pivot": s5_pivot(card, rng), "bin": 0}
        raise KeyError(self.s)

    # -------------------------------------------------------------------------------------------- dispatcher
    def build(self, frame, want, tries=80):
        last = None
        for _ in range(tries):
            try:
                st = self.struct(want)
                out = getattr(self, "f_" + frame)(st, want)
                if out is not None:
                    out.setdefault("struct", st)
                    return out
            except (Retry, Reject, Undefined) as e:
                last = e
                continue
        raise Retry(f"{frame}: no draw ({last})")

    # -------------------------------------------------------------------------------------------- helpers
    def T(self, st, role="main"):
        for t in st["tables"]:
            if t["role"] == role:
                return t
        raise KeyError(role)

    def ans(self, st, q, shown=None, alt=None):
        return solve(self.card, st, q, shown, alt)

    def check_yn(self, st, q, want):
        q["_qt"] = "yn"
        a = self.ans(st, q)
        if not isinstance(a, bool):
            raise Retry("yn special")
        if want.get("label") is not None and a != want["label"]:
            return None
        return {"q": q, "gold": a}

    def known_ids(self, st, cols, role="main"):
        t = self.T(st, role)
        js = [col_index(t, c) for c in cols if c in [x["name"] for x in t["cols"]]]
        return [r[0] for r in t["rows"] if all(r[j] is not None for j in js)]

    def phrase(self, kind, op_want=None):
        lst = self.card["cmp_count"] if kind == "count" else self.card["cmp_amount"]
        if op_want:
            lst = [p for p in lst if CMP_T10[p] in op_want] or lst
        return self.rng.choice(lst)

    def s2_pred(self, st, want_meet=True, n_atoms=None):
        """S2: build the filter around a decisive record (label-first; literals at the boundary)."""
        card, rng = self.card, self.rng
        t = self.T(st)
        cols = filter_cols(card, t)
        n = n_atoms or (1 if rng.random() < 0.5 else 2)
        chosen = rng.sample(cols, min(n, len(cols)))
        rec = rng.choice(t["rows"])
        aa = []
        for i, cn in enumerate(chosen):
            j = col_index(t, cn)
            c = t["cols"][j]
            v = rec[j]
            if v is None:
                raise Retry("decisive unknown")
            if c["type"] == "num":
                ph = rng.choice(card["cmp_amount"])
                op = CMP_T10[ph]
                meet = want_meet or i < len(chosen) - 1
                x, pl = choose_lit(Fraction(v), op, meet, c["step"], rng, c["lo"] + c["step"], c["hi"])
                aa.append({"k": "cmp", "col": cn, "op": op, "lit": lit_str(x, c["dp"]), "unit": c["unit"],
                           "_ph": ph, "_pl": pl})
            elif c["type"] == "cat":
                if want_meet or i < len(chosen) - 1:
                    aa.append({"k": "cmp", "col": cn, "op": "=", "lit": v})
                else:
                    aa.append({"k": "cmp", "col": cn, "op": "=", "lit": rng.choice([x for x in c["values"] if x != v])})
            else:
                aa.append(draw_atom(card, t, rng, cn, ["eq"]))
        return aa[0] if len(aa) == 1 else {"k": "and", "args": aa}

    def pred(self, st, **kw):
        if self.s == "S2" and self.rng.random() < 0.7:
            return self.s2_pred(st, want_meet=self.rng.random() < 0.5, n_atoms=kw.get("n_atoms"))
        return draw_pred(self.card, self.T(st), self.rng, **kw)

    def scope(self, q):
        if self.card["sem"]["world"] == "T2":
            q["_scope"] = True
        return q

    # ============================================================================== S1 / S2 / S4 yes/no
    def f_Y_EXISTS(self, st, want):
        q = self.scope({"op": "exists", "f": self.pred(st)})
        return self.check_yn(st, q, want)

    def f_Y_TERMX(self, st, want):
        tn = next(iter(self.card["terms"]))
        q = self.scope({"op": "exists", "f": {"k": "term", "name": tn}})
        return self.check_yn(st, q, want)

    def f_Y_COUNT(self, st, want):
        f = self.pred(st)
        q0 = {"op": "count", "f": f}
        c = self.ans(st, q0)
        if c in SPECIALS:
            raise Retry("count undetermined")
        ph = self.phrase("count")
        op = CMP_T10[ph]
        n, pl = choose_lit(Fraction(c), op, want["label"], Fraction(1), self.rng, lo=1)
        q = self.scope({"op": "thr", "inner": q0, "cmp": op, "lit": str(int(n)), "_ph": ph, "_pl": pl})
        return self.check_yn(st, q, want)

    def f_Y_MEAN(self, st, want):
        t = self.T(st)
        nums = [c for c in t["cols"] if c["type"] == "num" and "." not in c["name"]]
        c = self.rng.choice(nums)
        f = self.pred(st, exclude=(c["name"],))
        q0 = {"op": "mean", "col": c["name"], "f": f}
        m = self.ans(st, q0)
        if m in SPECIALS:
            raise Retry("empty mean")
        if self._addends(st, q0) > 5:
            raise Retry("addends")
        ph = self.phrase("amount")
        op = CMP_T10[ph]
        base = c["lo"] + c["step"] * int((m - c["lo"]) / c["step"])
        x, pl = choose_lit(base, op, want["label"], c["step"], self.rng, c["step"], c["hi"] * 2)
        q = self.scope({"op": "thr", "inner": q0, "cmp": op, "lit": lit_str(x, c["dp"]), "unit": c["unit"],
                        "_ph": ph, "_pl": pl})
        return self.check_yn(st, q, want)

    def _addends(self, st, q0):
        qq = {"op": "count", "f": q0.get("f")}
        n = self.ans(st, qq)
        if not isinstance(n, int):
            raise Retry("addends undetermined")
        return n

    def f_Y_LOOKN(self, st, want):
        t = self.T(st)
        nums = [c for c in t["cols"] if c["type"] == "num"]
        c = self.rng.choice(nums)
        rid = self.rng.choice(self.known_ids(st, [c["name"]]))
        v = t["rows"][[r[0] for r in t["rows"]].index(rid)][col_index(t, c["name"])]
        ph = self.phrase("amount")
        op = CMP_T10[ph]
        x, pl = choose_lit(Fraction(v), op, want["label"], c["step"], self.rng, c["step"], c["hi"] * 2)
        a = {"k": "cmp", "col": c["name"], "op": op, "lit": lit_str(x, c["dp"]), "unit": c["unit"], "_ph": ph,
             "_pl": pl}
        q = {"op": "lookup_p", "id": rid, "p": a}
        return self.check_yn(st, q, want)

    def f_Y_LOOKC(self, st, want, neg=False):
        t = self.T(st)
        cats = [c for c in t["cols"] if c["type"] == "cat"]
        c = self.rng.choice(cats)
        rid = self.rng.choice(self.known_ids(st, [c["name"]]))
        v = t["rows"][[r[0] for r in t["rows"]].index(rid)][col_index(t, c["name"])]
        others = [x for x in c["values"] if x != v]
        kind = self.rng.choice(["eq", "in2"] if self.card.get("use_in2") else ["eq"])
        if neg:
            kind = "not" if kind == "eq" else "neither"
        hit = want["label"] if not neg else not want["label"]
        if kind in ("eq", "not"):
            lit = v if hit else self.rng.choice(others)
            a = {"k": "cmp", "col": c["name"], "op": "=", "lit": lit}
            if kind == "not":
                a = {"k": "not", "arg": a}
        else:
            if hit:
                vals = [v, self.rng.choice(others)]
            else:
                vals = self.rng.sample(others, 2)
            self.rng.shuffle(vals)
            a = {"k": "in", "col": c["name"], "vals": vals}
            if kind == "neither":
                a = {"k": "not", "arg": a}
        q = {"op": "lookup_p", "id": rid, "p": a}
        return self.check_yn(st, q, want)

    def f_Y_TERM(self, st, want):
        tn = next(iter(self.card["terms"]))
        from f9ast import term_cols
        rid = self.rng.choice(self.known_ids(st, term_cols(self.card["terms"][tn])))
        q = {"op": "lookup_p", "id": rid, "p": {"k": "term", "name": tn}}
        return self.check_yn(st, q, want)

    def f_Y_FORALL(self, st, want):
        t = self.T(st)
        cats = [c for c in t["cols"] if c["type"] == "cat" and "." not in c["name"]]
        nums = [c for c in t["cols"] if c["type"] == "num" and "." not in c["name"]]
        ca, cb = self.rng.choice(cats), self.rng.choice(nums)
        va = self.rng.choice(col_vals(t, ca["name"]))
        A = {"k": "cmp", "col": ca["name"], "op": "=", "lit": va}
        q0 = {"op": "min", "col": cb["name"], "f": A}
        ph = self.rng.choice([p for p in self.card["cmp_amount"] if CMP_T10[p] in (">=", ">")] or ["at least {X}"])
        op = CMP_T10[ph]
        mn = self.ans(st, q0)
        if mn in SPECIALS:
            raise Retry("empty")
        x, pl = choose_lit(Fraction(mn), op, want["label"], cb["step"], self.rng, cb["step"], cb["hi"] * 2)
        B = {"k": "cmp", "col": cb["name"], "op": op, "lit": lit_str(x, cb["dp"]), "unit": cb["unit"], "_ph": ph}
        q = self.scope({"op": "forall", "a": A, "b": B})
        return self.check_yn(st, q, want)

    def f_Y_COMPARE(self, st, want):
        t = self.T(st)
        cats = [c for c in t["cols"] if c["type"] == "cat" and "." not in c["name"]]
        nums = [c for c in t["cols"] if c["type"] == "num" and "." not in c["name"]]
        ca = self.rng.choice(cats)
        va, vb = self.rng.sample(ca["values"], 2)
        agg = self.rng.choice(["sum", "count", "mean"])
        cb = self.rng.choice(nums)
        ph = self.rng.choice(self.card["cmp35"])
        if agg == "count" and "high" in ph:
            ph = ph.replace("higher than", "more than").replace("at least as high as", "at least as many as")
        q = {"op": "compare", "agg": agg, "col": None if agg == "count" else cb["name"],
             "a": {"k": "cmp", "col": ca["name"], "op": "=", "lit": va},
             "b": {"k": "cmp", "col": ca["name"], "op": "=", "lit": vb}, "cmp": CMP_T35[ph], "_ph": ph}
        if agg != "count":
            for g in ("a", "b"):
                if self._addends(st, {"f": q[g]}) > 5:
                    raise Retry("addends")
        return self.check_yn(st, self.scope(q), want)

    def f_Y_PRES(self, st, want):
        t = self.T(st)
        listed = [r[0] for r in t["rows"]]
        rid = self.rng.choice(listed) if want["label"] else unlisted_id(self.card["schema"]["prefix"], listed, self.rng)
        return self.check_yn(st, {"op": "presence", "id": rid}, want)

    def f_Y_ANY(self, st, want, q_kind="any"):
        if st.get("compact"):
            raise Retry("compact bin")
        t = self.T(st)
        sc = self.card["schema"]["list"]
        j = col_index(t, sc["name"])
        rows = [r for r in t["rows"] if r[j] is not None]
        if self.card["sem"]["missing"] == "T4":
            rows = [r for r in rows if all(v is not None for v in r)]
        r = self.rng.choice(rows)
        sub = sc["sub"]
        if self.rng.random() < 0.5:
            vals = [s[0] for s in r[j]] or sub[0]["values"]
            cond = {"k": "cmp", "col": "kind", "op": "=", "lit": self.rng.choice(vals if self.rng.random() < 0.7
                                                                                  else sub[0]["values"])}
        else:
            amts = [s[1] for s in r[j]] or [Fraction(10)]
            ph = self.phrase("amount")
            x, _ = choose_lit(Fraction(self.rng.choice(amts)), CMP_T10[ph], self.rng.random() < 0.5, Fraction(1),
                              self.rng, 1, 200)
            cond = {"k": "cmp", "col": "amount", "op": CMP_T10[ph], "lit": str(int(x)), "unit": sub[1]["unit"],
                    "_ph": ph}
        q = {"op": "quant_lookup", "id": r[0], "q": q_kind, "list": sc["name"], "cond": cond}
        return self.check_yn(st, q, want)

    def f_Y_EVERY(self, st, want):
        return self.f_Y_ANY(st, want, q_kind="every")

    # ============================================================================== value picks
    def value_gold(self, st, q, want):
        q["_qt"] = "value"
        a = self.ans(st, q)
        g = want.get("gold", "normal")
        if g == "normal" and a in SPECIALS:
            return None
        if g in ("NO_RECORD", "CBD") and a != {"NO_RECORD": NO_RECORD, "CBD": CBD}[g]:
            return None
        return {"q": q, "gold": a}

    def f_V_COUNT(self, st, want):
        q = self.scope({"op": "count", "f": self.pred(st, n_atoms=2)})
        out = self.value_gold(st, q, want)
        if out and isinstance(out["gold"], int) and out["gold"] > 12:
            return None
        return out

    def f_V_TCOUNT(self, st, want):
        tn = next(iter(self.card["terms"]))
        q = self.scope({"op": "count", "f": {"k": "term", "name": tn}})
        out = self.value_gold(st, q, want)
        if out and isinstance(out["gold"], int) and out["gold"] > 12:
            return None
        return out

    def _numcol(self, st):
        t = self.T(st)
        return self.rng.choice([c for c in t["cols"] if c["type"] == "num" and "." not in c["name"]])

    def f_V_SUM(self, st, want):
        c = self._numcol(st)
        q = self.scope({"op": "sum", "col": c["name"], "f": self.pred(st, exclude=(c["name"],), n_atoms=2)})
        if self._addends(st, q) > 5 or self._addends(st, q) < 1:
            return None
        return self.value_gold(st, q, want)

    def f_V_MEAN(self, st, want):
        c = self._numcol(st)
        f = self.pred(st, exclude=(c["name"],), n_atoms=2)
        q = self.scope({"op": "mean", "col": c["name"], "f": f})
        if want.get("gold") != "NO_RECORD" and self._addends(st, q) > 5:
            return None
        out = self.value_gold(st, q, want)
        if out and isinstance(out["gold"], Fraction):
            from f9fmt import round_half_up
            if round_half_up(out["gold"], self.card["sem"]["round_dp"]) == out["gold"] and self.rng.random() < 0.5:
                return None  # prefer means that need rounding (T22 live)
        return out

    def f_V_EXT(self, st, want):
        t = self.T(st)
        cols = [c for c in t["cols"] if c["type"] in ("num", "date") and "." not in c["name"]]
        c = self.rng.choice(cols)
        op = self.rng.choice(["min", "max"])
        q = self.scope({"op": op, "col": c["name"], "f": self.pred(st, exclude=(c["name"],), n_atoms=2)})
        return self.value_gold(st, q, want)

    def f_V_LOOK(self, st, want):
        t = self.T(st)
        cols = [c for c in t["cols"] if c["type"] in ("num", "cat", "date")]
        if want.get("col_type"):
            cols = [c for c in cols if c["type"] == want["col_type"]] or cols
        c = self.rng.choice(cols)
        listed = [r[0] for r in t["rows"]]
        g = want.get("gold", "normal")
        if g in ("NO_RECORD", "CBD") and not (g == "CBD" and self.card["sem"].get("missing") == "T5"):
            rid = unlisted_id(self.card["schema"]["prefix"], listed, self.rng)
        elif g == "CBD":
            el = [r[0] for r in t["rows"] if r[col_index(t, c["name"])] is None]
            if not el:
                j = col_index(t, c["name"])
                if c["name"] not in (self.card.get("t5_cols") or []):
                    raise Retry("col not T5")
                r = self.rng.choice(t["rows"])
                r[j] = None
                el = [r[0]]
            rid = self.rng.choice(el)
        else:
            rid = self.rng.choice(self.known_ids(st, [c["name"]]))
        q = {"op": "lookup", "id": rid, "col": c["name"]}
        return self.value_gold(st, q, want)

    def f_V_CDIST(self, st, want):
        t = self.T(st)
        c = self.rng.choice([c for c in t["cols"] if c["type"] == "cat" and "." not in c["name"]])
        q = self.scope({"op": "cdist", "col": c["name"], "f": self.pred(st, exclude=(c["name"],), n_atoms=2)})
        out = self.value_gold(st, q, want)
        if out and isinstance(out["gold"], int) and (out["gold"] < 1 or out["gold"] > 12):
            return None
        return out

    # ============================================================================== record picks
    def f_R_EXT(self, st, want):
        t = self.T(st)
        cols = [c for c in t["cols"] if c["type"] in ("num", "date") and "." not in c["name"]]
        if not cols:
            raise Retry("no top-level number or date column")
        c = self.rng.choice(cols)
        op = self.rng.choice(["argmax", "argmin"])
        # two filter atoms: a record pick needs >= 2 named distractors (1.3: E1 per atom, E11)
        f = self.pred(st, exclude=(c["name"],), n_atoms=2)
        q = self.scope({"op": op, "col": c["name"], "f": f})
        g = want.get("gold", "normal")
        if g == "TIE" or (g == "normal" and self.rng.random() < 0.2):
            self._plant_tie(st, q, c)
        q["_qt"] = "record"
        a = self.ans(st, q)
        if g == "normal" and a in SPECIALS:
            return None
        if g in ("NO_RECORD", "TIE") and a != {"NO_RECORD": NO_RECORD, "TIE": TIE}[g]:
            return None
        return {"q": q, "gold": a}

    def _plant_tie(self, st, q, c):
        t = self.T(st)
        sel = self.ans(st, {"op": "select", "f": q["f"]})
        if len(sel) < 2:
            raise Retry("no tie room")
        j = col_index(t, c["name"])
        rows = [r for r in t["rows"] if r[0] in sel and r[j] is not None]
        if len(rows) < 2:
            raise Retry("no tie room")
        vals = [r[j] for r in rows]
        best = max(vals) if q["op"] == "argmax" else min(vals)
        other = self.rng.choice([r for r in rows if r[j] != best] or rows[1:])
        other[j] = best

    def cond_pick(self, st, q, want, role, idcol_index=0, universe=None):
        """Condition pick: feasibility only (some id meets / some id does not); f9rows composes the shown options."""
        meet = self.ans(st, {**q, "op": "select"})
        if not isinstance(meet, frozenset):
            if self.card["sem"].get("missing") == "T5":
                return {"q": q, "gold": None}
            return None
        if want.get("gold", "normal") == "normal" and not meet:
            return None
        need = want.get("k_ids")
        if need and len(st["tables"][0]["rows"]) - len(meet) < need:
            return None  # too few non-meeting ids to fill the shown options
        q["_qt"] = "record"
        return {"q": q, "gold": None}

    def f_R_COND(self, st, want):
        q = self.scope({"op": "cpick", "f": self.pred(st)})
        return self.cond_pick(st, q, want, "main")

    def f_R_INV(self, st, want):
        tn = next(iter(self.card["terms"]))
        q = self.scope({"op": "cpick", "f": {"k": "term", "name": tn}})
        return self.cond_pick(st, q, want, "main")

    # ============================================================================== sets
    def set_gold(self, st, q, want):
        q["_qt"] = "set"
        a = self.ans(st, q)
        if a in SPECIALS:
            return None
        n = want.get("set_size")
        if n is not None and len(a) != n:
            return None
        return {"q": q, "gold": a}

    def f_SET_SEL(self, st, want):
        n = want.get("set_size", 2)
        f = self.pred(st, n_atoms=2 if len(self.T(st)["rows"]) > 25 else None)
        return self.set_gold(st, self.scope({"op": "select", "f": f}), want)

    def f_SET_TERM(self, st, want):
        tn = next(iter(self.card["terms"]))
        return self.set_gold(st, self.scope({"op": "select", "f": {"k": "term", "name": tn}}), want)

    # ============================================================================== S3
    def _ev_pred(self, st, n=None):
        t = self.T(st, "fact")
        card = self.card
        # a date column is a filter only on cards that state a time-window form (T15-T17; card["time_forms"])
        cols = [c["name"] for c in t["cols"] if c["type"] in ("cat", "num") or
                (c["type"] == "date" and card.get("time_forms"))]
        n = n or (1 if self.rng.random() < 0.6 else 2)
        ch = self.rng.sample(cols, min(n, len(cols)))
        aa = [draw_atom(card, t, self.rng, cn, ["eq", "in2"] + (["not"] if i == len(ch) - 1 else []))
              for i, cn in enumerate(ch)]
        aa.sort(key=lambda a: a["k"] == "not")
        return aa[0] if len(aa) == 1 else {"k": "and", "args": aa}

    def _dim_pred(self, st):
        t = self.T(st, "dim")
        cols = [c["name"] for c in t["cols"] if c["type"] in ("cat", "num")]
        cn = self.rng.choice(cols)
        return draw_atom(self.card, t, self.rng, cn, ["eq", "in2", "not"])

    def _live_keys(self, st):
        dim = self.T(st, "dim")
        return [r[0] for r in dim["rows"] if all(v is not None for v in r)]

    def f_Y_EANY(self, st, want):
        key = self.rng.choice(self._live_keys(st))
        q = {"op": "ent_any", "key": key, "fe": self._ev_pred(st)}
        return self.check_yn(st, q, want)

    def f_Y_ESUM(self, st, want):
        fact = self.T(st, "fact")
        nums = [c for c in fact["cols"] if c["type"] == "num"]
        c = self.rng.choice(nums)
        key = self.rng.choice(self._live_keys(st))
        fe = self._ev_pred(st, 1) if self.rng.random() < 0.4 else None
        q0 = {"op": "ent_sum", "key": key, "col": c["name"], "fe": fe}
        s = self.ans(st, q0)
        if s in SPECIALS or s <= 0:
            raise Retry("zero sum")
        if self.ans(st, {"op": "g_count", "fd": {"k": "cmp", "col": self.card["idcol"], "op": "=", "lit": key},
                         "fe": fe}) > 5:
            raise Retry("addends")
        ph = self.phrase("amount")
        x, pl = choose_lit(Fraction(s), CMP_T10[ph], want["label"], c["step"], self.rng, c["step"], None)
        q = {"op": "thr", "inner": q0, "cmp": CMP_T10[ph], "lit": lit_str(x, c["dp"]), "unit": c["unit"], "_ph": ph,
             "_pl": pl}
        q["inner"]["_role"] = "fact"
        return self.check_yn(st, q, want)

    def f_Y_GCOUNT(self, st, want):
        q0 = {"op": "g_count", "fd": self._dim_pred(st), "fe": None}
        c = self.ans(st, q0)
        ph = self.phrase("count")
        n, pl = choose_lit(Fraction(c), CMP_T10[ph], want["label"], Fraction(1), self.rng, lo=1)
        q = {"op": "thr", "inner": q0, "cmp": CMP_T10[ph], "lit": str(int(n)), "_ph": ph, "_pl": pl}
        return self.check_yn(st, q, want)

    def f_V_ESUM(self, st, want):
        fact = self.T(st, "fact")
        c = self.rng.choice([c for c in fact["cols"] if c["type"] == "num"])
        key = self.rng.choice(self._live_keys(st))
        # two event conditions: E1 (each), E11 and E2 give the 3+ named distractors a value pick needs (1.3)
        fe = self._ev_pred(st, 2)
        q = {"op": "ent_sum", "key": key, "col": c["name"], "fe": fe}
        if self.ans(st, {"op": "g_count", "fd": {"k": "cmp", "col": self.card["idcol"], "op": "=", "lit": key},
                         "fe": fe}) > 5:
            return None
        return self.value_gold(st, q, want)

    def f_V_GCOUNT(self, st, want):
        q = {"op": "g_count", "fd": self._dim_pred(st), "fe": None}
        out = self.value_gold(st, q, want)
        if out and isinstance(out["gold"], int) and out["gold"] > 12:
            return None
        return out

    def f_V_EATTR(self, st, want):
        dim = self.T(st, "dim")
        c = self.rng.choice([c for c in dim["cols"] if c["type"] in ("cat", "num")])
        g = want.get("gold", "normal")
        keys = [r[0] for r in dim["rows"]]
        if g == "NO_RECORD":
            fk = {r[0] for r in self.T(st, "fact")["rows"]}
            for _ in range(50):
                key = unlisted_id(self.card["schema"]["ent_prefix"], keys, self.rng)
                if key not in fk:
                    break
            else:
                raise Retry("no clean unlisted key")
        else:
            key = self.rng.choice(self.known_ids(st, [c["name"]], "dim"))
        q = {"op": "ent_attr", "key": key, "col": c["name"]}
        return self.value_gold(st, q, want)

    def f_E_GMAX(self, st, want):
        fact = self.T(st, "fact")
        agg = self.rng.choice(["count", "sum"])
        c = self.rng.choice([c for c in fact["cols"] if c["type"] == "num"])
        fe = self._ev_pred(st, 1) if self.rng.random() < 0.7 else None
        q = {"op": "g_argmax", "agg": agg, "col": c["name"] if agg == "sum" else None, "fe": fe, "fd": None,
             "dir": "max"}
        q["_qt"] = "record"
        a = self.ans(st, q)
        g = want.get("gold", "normal")
        if g == "normal" and a in SPECIALS:
            return None
        if g == "TIE" and a != TIE:
            return None
        return {"q": q, "gold": a}

    def f_E_COND(self, st, want):
        q = {"op": "cpick", "f": {"k": "has", "fe": self._ev_pred(st)}}
        return self.cond_pick(st, q, want, "dim")

    def f_SET_ENT(self, st, want):
        q = {"op": "select", "f": {"k": "has", "fe": self._ev_pred(st)}}
        return self.set_gold(st, q, want)

    # ============================================================================== S6
    def _line_atom(self, st, with_comp=None, levels_only=False):
        lv = self.card["levels"]
        t = self.T(st, "log")
        a = {"k": "line"}
        r = self.rng.random()
        if r < 0.45 or levels_only:
            a["level"] = self.rng.choice(lv[1:])
            a["lvl_op"] = "="
        elif r < 0.75:
            a["level"] = self.rng.choice(lv[1:3])
            a["lvl_op"] = ">="
        if with_comp is True or (with_comp is None and self.rng.random() < 0.5) or "level" not in a:
            if not levels_only:
                a["comp"] = self.rng.choice(t["comps"])
        if "level" not in a and "comp" not in a:
            a["level"] = self.rng.choice(lv[1:])
            a["lvl_op"] = "="
        return a

    def _window(self, st, form=None):
        t = self.T(st, "log")
        if form is None:
            if not self.card["time_forms"] or self.rng.random() < 0.4:
                return None
            form = self.rng.choice(self.card["time_forms"])
        off = self.card["sem"]["zone"]
        from f9fmt import local_day
        times = sorted(r[0] for r in t["rows"])
        a = {"k": "win", "col": "time", "_form": form}
        if form == "on":
            d = local_day(self.rng.choice(times), off)
            a.update(lo=d, hi=d, li=True, hi_i=True, unit="day", step=1)
        elif form == "from_to":
            d = local_day(self.rng.choice(times), off)
            a.update(lo=d, hi=d + self.rng.randint(1, 3), li=True, hi_i=True, unit="day", step=1)
        else:
            unit = 60 if (self.card["sem"].get("tf") or "hm") == "hm" else 1
            t1 = self.rng.choice(times)
            t1 = t1 - t1 % 60
            t2 = t1 + 60 * self.rng.randint(10, 240)
            a.update(lo=t1, hi=t2, li=True, hi_i=False, unit="sec", step=unit)
        return a

    def _lfilter(self, st, **kw):
        a = self._line_atom(st, **kw)
        w = self._window(st)
        return {"k": "and", "args": [a, w]} if w else a

    def _lex_shape(self):
        """Y_LEX filter shape: level operator and level (or none), component or not, time-window form (or none);
        same draw shares as _line_atom / _window."""
        lv = self.card["levels"]
        r = self.rng.random()
        if r < 0.45:
            lm, lev = "=", self.rng.choice(lv[1:])
        elif r < 0.75:
            lm, lev = ">=", self.rng.choice(lv[1:3])
        else:
            lm, lev = None, None
        comp = lm is None or self.rng.random() < 0.5
        tf = self.card["time_forms"]
        form = self.rng.choice(tf) if (tf and self.rng.random() >= 0.4) else None
        return lm, lev, comp, form

    def _lex_filter(self, st, shape):
        lm, lev, comp, form = shape
        t = self.T(st, "log")
        a = {"k": "line"}
        if lm:
            a["level"], a["lvl_op"] = lev, lm
        if comp:
            a["comp"] = self.rng.choice(t["comps"])
        w = self._window(st, form=form) if form else None
        return {"k": "and", "args": [a, w]} if w else a

    def f_Y_LEX(self, st, want):
        """Repair r1b (G6 question view: Y_LEX labels were 69% predictable from the question words; G7 questions
        without a number 70% yes): the filter shape is drawn first and kept only when this log holds both a matching
        and a non-matching filter of that shape, so the shape and its words carry no label; the component and the
        window position then realize the wanted label."""
        lab = want.get("label")
        if lab is None:
            return self.check_yn(st, {"op": "exists_lines", "f": self._lfilter(st)}, want)
        shape = self._lex_shape()
        found = {}
        for _ in range(16):
            f = self._lex_filter(st, shape)
            try:
                a = self.ans(st, {"op": "exists_lines", "f": f, "_qt": "yn"})
            except Exception:
                continue
            if isinstance(a, bool) and a not in found:
                found[a] = f
                if len(found) == 2:
                    break
        if len(found) < 2:
            return None
        return self.check_yn(st, {"op": "exists_lines", "f": found[lab]}, want)

    def f_Y_LCOUNT(self, st, want):
        q0 = {"op": "count_lines", "f": self._lfilter(st)}
        c = self.ans(st, q0)
        ph = self.phrase("count")
        n, pl = choose_lit(Fraction(c), CMP_T10[ph], want["label"], Fraction(1), self.rng, lo=1)
        q = {"op": "thr", "inner": q0, "cmp": CMP_T10[ph], "lit": str(int(n)), "_ph": ph, "_pl": pl}
        return self.check_yn(st, q, want)

    def f_Y_REQ(self, st, want):
        t = self.T(st, "log")
        reqs = sorted({r[3] for r in t["rows"] if r[3]}, key=id_key)
        if not reqs:
            raise Retry("no requests")
        a = self._line_atom(st, levels_only=self.rng.random() < 0.6)
        if "level" in a and "comp" in a:
            # 1.2 / F9-R2-03: a compound condition on one line ("an <ERROR> line from <C5>") is never asked in a
            # request condition; keep the component phrase (G2 repair r03)
            a.pop("level"), a.pop("lvl_op", None)
        a.pop("lvl_op", None) if a.get("lvl_op") == "=" else None
        if "level" in a:
            a["lvl_op"] = "="
        lab = want.get("label")
        if lab is not None:
            # repair r1b (as Y_LEX): the line condition is kept only when some request meets it and some does not,
            # and the request then realizes the wanted label (the condition's words carry no label)
            by = {True: [], False: []}
            for rq in self.rng.sample(reqs, min(40, len(reqs))):
                try:
                    v = self.ans(st, {"op": "req_any", "req": rq, "a": dict(a), "_qt": "yn"})
                except Exception:
                    continue
                if isinstance(v, bool):
                    by[v].append(rq)
            if not by[True] or not by[False]:
                return None
            return self.check_yn(st, {"op": "req_any", "req": self.rng.choice(by[lab]), "a": a}, want)
        q = {"op": "req_any", "req": self.rng.choice(reqs), "a": a}
        return self.check_yn(st, q, want)

    def f_V_LCOUNT(self, st, want):
        # a level and a component on one line condition give two E1 distractors (1.3: 3-8 named distractors)
        q = {"op": "count_lines", "f": self._lfilter(st, with_comp=True if self.rng.random() < 0.7 else None)}
        out = self.value_gold(st, q, want)
        if out and isinstance(out["gold"], int) and out["gold"] > 12:
            return None
        return out

    def f_V_FIRST(self, st, want):
        q = {"op": self.rng.choice(["first", "last"]),
             "f": self._lfilter(st, with_comp=True if self.rng.random() < 0.7 else None)}
        out = self.value_gold(st, q, want)
        if out and out["gold"] not in SPECIALS:
            # no first / last answer may depend on two lines with the same time (T32)
            t = self.T(st, "log")
            sel = [r for r in t["rows"]]
            times = [r[0] for r in sel]
            if times.count(out["gold"]) > 1:
                return None
        return out

    def f_C_COMP(self, st, want):
        a = self._line_atom(st, with_comp=False)
        a.pop("comp", None)
        if "level" not in a:
            a["level"], a["lvl_op"] = self.card["levels"][2], ">="
        w = self._window(st)
        q = {"op": "comp_argmax", "f": {"k": "and", "args": [a, w]} if w else a}
        q["_qt"] = "record"
        a2 = self.ans(st, q)
        g = want.get("gold", "normal")
        if g == "normal" and a2 in SPECIALS:
            return None
        if g == "TIE" and a2 != TIE:
            return None
        return {"q": q, "gold": a2}

    def _lift_pred(self, st):
        a1 = self._line_atom(st, levels_only=True)
        a2 = self._line_atom(st, with_comp=True)
        a2.pop("level", None), a2.pop("lvl_op", None)
        if self.rng.random() < 0.35:
            neg = self._line_atom(st, levels_only=True)
            neg["lvl_op"] = "="
            if neg["level"] == a1.get("level"):
                raise Retry("same level")
            return {"k": "and", "args": [{"k": "lift", "a": a2}, {"k": "not", "arg": {"k": "lift", "a": neg}}]}
        a1["lvl_op"] = "="
        return {"k": "and", "args": [{"k": "lift", "a": a1}, {"k": "lift", "a": a2}]}

    def f_C_REQ(self, st, want):
        q = {"op": "cpick", "f": self._lift_pred(st)}
        meet = self.ans(st, {"op": "select", "f": q["f"]})
        if want.get("gold", "normal") == "normal" and not meet:
            return None
        need = want.get("k_ids")
        reqs = {r[3] for r in self.T(st, "log")["rows"] if r[3]}
        if need and len(reqs) - len(meet) < need:
            return None  # too few non-meeting requests to fill the shown options
        q["_qt"] = "record"
        return {"q": q, "gold": None}

    def f_SET_REQ(self, st, want):
        q = {"op": "select", "f": self._lift_pred(st)}
        return self.set_gold(st, q, want)

    # ============================================================================== S5 (dev)
    def f_Y_CELL(self, st, want):
        pv = st["pivot"]
        marks = {tuple(m) for m in pv["marks"]}
        e = self.rng.choice(pv["entities"])
        j = self.rng.randrange(len(pv["periods"]))
        if (e, j) in marks:
            raise Retry("marked")
        v = pv["cells"][e][j]
        ph = self.phrase("amount")
        x, pl = choose_lit(Fraction(v), CMP_T10[ph], want["label"], Fraction(1), self.rng, 1, None)
        q = {"op": "thr", "inner": {"op": "cell", "ent": e, "period": pv["periods"][j]}, "cmp": CMP_T10[ph],
             "lit": str(int(x)), "unit": self.card["schema"]["measure"]["unit"], "_ph": ph, "_pl": pl}
        return self.check_yn(st, q, want)

    def f_V_ROWT(self, st, want):
        e = self.rng.choice(st["pivot"]["entities"])
        return self.value_gold(st, {"op": "row_total", "ent": e}, want)

    def f_R_TOP(self, st, want):
        q = {"op": "row_top", "dir": self.rng.choice(["max", "min"]), "_qt": "record"}
        a = self.ans(st, q)
        if a in SPECIALS:
            return None
        return {"q": q, "gold": a}

    def f_V_COLC(self, st, want):
        pv = st["pivot"]
        marks = {tuple(m) for m in pv["marks"]}
        mper = sorted({j for _, j in marks})
        # a marked period and a literal at an unmarked value, so the T31 / T30 / T10 readings (E13, E26, E2) differ
        pj = self.rng.choice(mper) if mper and self.rng.random() < 0.85 else self.rng.randrange(len(pv["periods"]))
        per = pv["periods"][pj]
        ph = self.rng.choice([p for p in self.card["cmp_amount"] if CMP_T10[p] in (">=", ">", "<=", "<")])
        vals = [pv["cells"][e][pj] for e in pv["entities"] if (e, pj) not in marks and 1 <= pv["cells"][e][pj] <= 199]
        if not vals or self.rng.random() >= 0.85:
            q = {"op": "col_count", "period": per, "cmp": CMP_T10[ph], "lit": str(self.rng.randint(20, 180)), "_ph": ph}
            return self.value_gold(st, q, want)
        # literal drawn among the period's unmarked values, preferring one where the named readings (E2 pcmp,
        # E13 with_marked, E26 footnote_row) give counts distinct from gold and from each other (1.3: >= 3 named)
        self.rng.shuffle(vals)
        q = None
        for x in vals[:12]:
            q = {"op": "col_count", "period": per, "cmp": CMP_T10[ph], "lit": str(x), "_ph": ph}
            try:
                got = {self.ans(st, q)}
                for alt in (("E13", "with_marked"), ("E26", "footnote_row"), ("E2", "pcmp")):
                    got.add(self.ans(st, rewrite(q, alt) if alt[0] in REWRITE else q,
                                     alt=None if alt[0] in REWRITE else alt))
            except (Reject, Undefined):
                continue
            if len(got) == 4:
                break
        return self.value_gold(st, q, want)
