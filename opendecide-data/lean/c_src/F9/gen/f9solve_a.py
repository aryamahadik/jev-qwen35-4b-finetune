"""Solver A (generator side): pandas over the canonical Struct, exact Fraction arithmetic, section-2 semantics stated
explicitly (no library NULL / rounding / string-compare defaults).

  SolverA(struct, card).answer(q, alt=None) -> answer
Answers: bool (yes/no), Fraction / int (values, dates as ordinals, times as epoch seconds), str (ids, categories),
frozenset (record sets), or one of the specials NO_RECORD, CBD, TIE, NONE.

alt = None (the card's semantics) or a tuple naming one section-2 alternative (an error tag of 1.3 with its
parameters). AST-rewrite alternatives (E1, E2, E3, E11, E12, E19) are applied by f9alt.rewrite before evaluation;
mode alternatives (E4, E6, E7, E8, E16, E17, E20, E23, E24, E26, E27, E29, E30, E32, E34) switch evaluation here.
"""
from __future__ import annotations

import itertools
from fractions import Fraction

import pandas as pd

from f9fmt import local_day, round_half_even, round_half_up, to_frac

NO_RECORD, CBD, TIE, NONE = "<NO_RECORD>", "<CBD>", "<TIE>", "<NONE>"
SPECIALS = (NO_RECORD, CBD, TIE, NONE)


class Undefined(Exception):
    """A never-generated case (T23 never-generated list, F9-R3-12): the row is rejected."""


class Reject(Exception):
    """The draw breaks a generation rule (two meeting options in a condition pick, etc.)."""


def lit_value(v, ctype):
    if ctype == "num":
        return to_frac(v)
    if ctype in ("date", "dt"):
        return int(v)
    return v


def cmp_op(a, op, b):
    if op == ">=":
        return a >= b
    if op == ">":
        return a > b
    if op == "<=":
        return a <= b
    if op == "<":
        return a < b
    if op == "=":
        return a == b
    if op == "!=":
        return a != b
    raise KeyError(op)


def _cf(s):
    return str(s).strip().casefold()


class SolverA:
    def __init__(self, struct, card):
        self.s = struct
        self.card = card
        self.terms = card.get("terms") or {}
        self.sem = card["sem"]
        self.coltypes = {}
        for t in struct["tables"]:
            for c in t["cols"]:
                self.coltypes[(t["role"], c["name"])] = c
                if c["type"] == "list":
                    for sc in c["sub"]:
                        self.coltypes[("item", sc["name"])] = sc
        self.alt = None
        self.levels = card.get("levels")
        self._cache = {}

    def recs(self, role):
        """Records of a table (pandas DataFrame -> records, built once; T5 completions substitute in place)."""
        if role not in self._cache:
            d = self.df(role)
            self._cache[role] = d.to_dict("records")
        return self._cache[role]

    # -------------------------------------------------------------------------------------------- frames
    def table(self, role):
        for t in self.s["tables"]:
            if t["role"] == role:
                return t
        raise KeyError(role)

    def df(self, role):
        t = self.table(role)
        names = [c["name"] for c in t["cols"]]
        d = pd.DataFrame([list(r) for r in t["rows"]], columns=names, dtype=object)
        d["_pos"] = range(len(d))
        return d

    def ctype(self, role, col):
        c = self.coltypes.get((role, col))
        return c["type"] if c else None

    # -------------------------------------------------------------------------------------------- units (T28)
    def lit_in_col_unit(self, p, role):
        c = self.coltypes[(role, p["col"])]
        v = to_frac(p["lit"]) if "lit" in p else None
        return self._conv(v, p.get("unit"), c.get("unit"))

    def _conv(self, v, u_from, u_to):
        if v is None or u_from is None or u_to is None or u_from == u_to:
            return v
        if self.alt and self.alt[0] == "E9":
            return v
        f = (self.sem.get("conv") or {}).get(f"{u_from}->{u_to}")
        if f is None:
            g = (self.sem.get("conv") or {}).get(f"{u_to}->{u_from}")
            if g is None:
                raise KeyError(f"no stated factor {u_from}->{u_to}")
            return v / to_frac(g)
        return v * to_frac(f)

    # -------------------------------------------------------------------------------------------- predicates
    def ev(self, p, r, role, ctx=None):
        """r: dict col -> value (no UNKNOWN unless alt E4). Returns bool."""
        if p is None:
            return True
        k = p["k"]
        if k == "and":
            return all(self.ev(x, r, role, ctx) for x in p["args"])
        if k == "or":
            return any(self.ev(x, r, role, ctx) for x in p["args"])
        if k == "not":
            return not self.ev(p["arg"], r, role, ctx)
        if k == "xor":
            a, b = (self.ev(x, r, role, ctx) for x in p["args"])
            return a != b
        if k == "term":
            return self.term(p["name"], r, role, ctx)
        if k == "quant":
            items = r[p["list"]]
            if items is None:
                return self._unk_atom()
            sub = [dict(zip([c["name"] for c in self.coltypes[(role, p["list"])]["sub"]], it)) for it in items]
            hits = [self.ev(p["cond"], it, "item", ctx) for it in sub]
            if p["q"] == "any":
                return any(hits)
            if p["q"] == "every":
                if not sub:
                    return bool(self.alt and self.alt[0] == "E20")
                return all(hits)
            if p["q"] == "no":
                if not sub and self.alt and self.alt[0] == "E20":
                    return False
                return not any(hits)
        if k == "has":  # S3 entity: has any event meeting fe (T29: events of this key)
            return any(self.ev(p["fe"], e, "fact", ctx) for e in ctx["events_of"].get(r[ctx["dim_id"]], []))
        if k == "lift":  # S6 request: T41 per-atom lift over the lines carrying its id
            lines = ctx["lines_of"].get(r["request"], [])
            mode = self.alt[1] if self.alt and self.alt[0] == "E32" else None
            if mode == "last_line":
                lines = [max(lines, key=lambda x: (x["time"], x["_pos"]))] if lines else []
            elif mode == "first_line":
                lines = [min(lines, key=lambda x: (x["time"], x["_pos"]))] if lines else []
            return any(self.ev(p["a"], ln, "log", ctx) for ln in lines)
        if k == "line":
            ok = True
            if p.get("level") is not None:
                lv = self.levels
                ok = cmp_op(lv.index(r["level"]), p.get("lvl_op", "="), lv.index(p["level"]))
            if ok and p.get("comp") is not None:
                ok = r["component"] == p["comp"]
            return ok
        col = p["col"]
        v = r.get(col)
        ct = self.coltypes.get((role, col))
        typ = ct["type"] if ct else None
        if v is None:
            return self._unk_atom()
        if k == "cmp":
            if typ == "num":
                lit = self._conv(to_frac(p["lit"]), p.get("unit"), ct.get("unit"))
                return cmp_op(to_frac(v), p["op"], lit)
            if typ in ("date", "dt"):
                return cmp_op(int(v), p["op"], int(p["lit"]))
            if p["op"] == "=":
                return _cf(v) == _cf(p["lit"])
            if p["op"] == "!=":
                return _cf(v) != _cf(p["lit"])
            raise KeyError(p["op"])
        if k == "between":
            lo = self._conv(to_frac(p["lo"]), p.get("unit"), ct.get("unit"))
            hi = self._conv(to_frac(p["hi"]), p.get("unit"), ct.get("unit"))
            x = to_frac(v)
            if p.get("open"):
                return lo < x < hi
            return lo <= x <= hi
        if k == "in":
            return _cf(v) in {_cf(x) for x in p["vals"]}
        if k == "win":
            x = int(v)
            if p.get("unit") == "day" and typ == "dt":
                x = local_day(x, self.sem["zone"])
            lo, hi = p.get("lo"), p.get("hi")
            if lo is not None and not (x >= lo if p.get("li", True) else x > lo):
                return False
            if hi is not None and not (x <= hi if p.get("hi_i", True) else x < hi):
                return False
            return True
        if k == "contains":
            if self.alt and self.alt[0] == "E25":
                return str(p["s"]) in str(v)
            return _cf(p["s"]) in _cf(v)
        raise KeyError(k)

    def _unk_atom(self):
        if self.alt and self.alt[0] == "E4" and self.alt[1] == "meet":
            return True
        raise Undefined("UNKNOWN reached an atom")

    def term(self, name, r, role, ctx):
        t = self.terms[name]
        alt = self.alt or ()
        tag = alt[0] if alt else None
        if tag == "E26" and alt[1] == "usual_meaning" and t.get("usual"):
            return self.ev(t["usual"], r, role, ctx)
        for o in t.get("overrides") or []:
            if tag == "E26" and alt[1] == "general_over_specific":
                break
            if _cf(r.get(o["col"])) == _cf(o["val"]):
                c = self.ev(o["cond"], r, role, ctx)
                if tag == "E26" and alt[1] == "unless_kept" and t["kind"] == "T7":
                    return c and not self.ev(t["B"], r, role, ctx)
                if tag == "E26" and alt[1] == "closure_kept":
                    return c and self._general(t, r, role, ctx, tag)
                return c
        return self._general(t, r, role, ctx, tag)

    def _general(self, t, r, role, ctx, tag):
        if t["kind"] == "T7":
            a = self.ev(t["A"], r, role, ctx)
            b = self.ev(t["B"], r, role, ctx)
            return (a or b) if tag == "E16" else (a and not b)
        if t["kind"] == "T8":
            a = self.ev(t["A"], r, role, ctx)
            if tag == "E17":
                return a
            return a and self.ev(t["C"], r, role, ctx)
        if t["kind"] == "T9":
            return all(self.ev(x, r, role, ctx) for x in t["list"])
        raise KeyError(t["kind"])

    # -------------------------------------------------------------------------------------------- read columns
    def read_cols(self, q):
        from f9ast import pred_cols
        b = q
        while b["op"] in ("thr", "not"):
            b = b["inner"]
        cols = []
        for key in ("f", "a", "b", "p", "fe", "fd", "cond"):
            if isinstance(b.get(key), dict):
                cols += pred_cols(b[key], self.terms)
        if b["op"] == "quant_lookup":
            cols.append(b["list"])
        if b.get("col"):
            cols.append(b["col"])
        if b["op"] in ("argmax", "argmin", "cpick_ext"):
            for tk in self.sem.get("tie_chain") or []:
                cols.append(tk[0])
        return list(dict.fromkeys(cols))

    # -------------------------------------------------------------------------------------------- top level
    def answer(self, q, alt=None, shown=None):
        """shown: the option payloads shown on a condition pick (ids)."""
        self.alt = alt
        try:
            miss = self.sem.get("missing")
            if miss == "T5" and not (alt and alt[0] in ("E29", "E4")) and self.s["sampler"] in ("S1", "S2", "S3", "S4"):
                return self._t5(q, shown)
            return self._op(q, shown, bool(miss == "T4" or (alt and alt[0] == "E29")))
        finally:
            self.alt = None

    def _t5(self, q, shown):
        cells = self._unk_cells(q)
        if not cells:
            return self._op(q, shown, False)
        doms = [self.card["t5_domains"][c[2]]["values"] for c in cells]
        prod = 1
        for d in doms:
            prod *= len(d)
        if prod > 20000:
            raise Reject("T5 product > 20000")
        answers = {}
        try:
            for combo in itertools.product(*doms):
                for (role, i, name, j), v in zip(cells, combo):
                    self.recs(role)[i][name] = v
                a = self._op(q, shown, False)
                answers.setdefault(self.card["render_key"](q, a), a)
                if len(answers) > 1 and q.get("_qt") == "yn":
                    raise Reject("T5 yes/no row depends on an unknown")
        finally:
            for (role, i, name, j) in cells:
                self.recs(role)[i][name] = None
        if len(answers) == 1:
            return next(iter(answers.values()))
        if q.get("op") == "cpick" and all(a == NONE for a in answers.values()):
            return NONE
        return CBD

    def _unk_cells(self, q):
        rc = set(self.read_cols(q))
        out = []
        for t in self.s["tables"]:
            for i, r in enumerate(self.recs(t["role"])):
                for j, c in enumerate(t["cols"]):
                    if r[c["name"]] is None and c["name"] in rc:
                        out.append((t["role"], i, c["name"], j))
        if len(out) > 3:
            raise Reject("more than 3 unknown read cells")
        return out

    # -------------------------------------------------------------------------------------------- evaluation
    def _eval(self, q, st, shown, drop_unknown):
        return self._op(q, shown, drop_unknown)

    def _rows(self, role, cols_read, drop_unknown):
        rs = self.recs(role)
        if drop_unknown and cols_read:
            names = {c["name"] for c in self.table(role)["cols"]}
            cr = [c for c in cols_read if c in names]
            if cr:
                rs = [r for r in rs if all(r[c] is not None for c in cr)]
        return rs

    def _recs(self, d):
        return d

    def _filter(self, recs, f, role, ctx=None):
        return [r for r in recs if self.ev(f, r, role, ctx)]

    def _op(self, q, shown, drop):
        op = q["op"]
        alt = self.alt or ()
        if op == "not":
            return not self._op(q["inner"], shown, drop)
        if op == "thr":
            v = self._op(q["inner"], shown, drop)
            if v in SPECIALS:
                raise Undefined("threshold over an undefined value")
            lit = to_frac(q["lit"])
            if q.get("unit") and q["inner"].get("col"):
                role = q["inner"].get("_role", "main")
                ct = self.coltypes.get((role, q["inner"]["col"]))
                if ct and ct.get("unit"):
                    lit = self._conv(lit, q["unit"], ct["unit"])
            if alt and alt[0] == "E8" and isinstance(v, Fraction):
                v = round_half_up(v, self.sem.get("round_dp", 1))
            o = q["cmp"]
            if alt and alt[0] == "E2" and alt[1] == "thr":
                o = {">=": ">", ">": ">=", "<=": "<", "<": "<="}.get(o, o)
            return cmp_op(v, o, lit)
        s = self.s["sampler"]
        if s in ("S1", "S2", "S4"):
            return self._op_main(q, shown, drop)
        if s == "S3":
            return self._op_join(q, shown, drop)
        if s == "S6":
            return self._op_log(q, shown, drop)
        if s == "S5":
            return self._op_pivot(q, shown, drop)
        raise KeyError(s)

    # ---------------------------------------------------------------------------- single table (S1 / S2 / S4)
    def _tie_pick(self, cand, col, direction, idcol, role="main"):
        """cand: list of records; returns the winning id (T24) or TIE."""
        if not cand:
            return NO_RECORD
        key = (lambda r: to_frac(r[col])) if self.ctype(role, col) == "num" else (lambda r: int(r[col]))
        best = max(key(r) for r in cand) if direction == "max" else min(key(r) for r in cand)
        tied = [r for r in cand if key(r) == best]
        if len(tied) == 1:
            return tied[0][idcol]
        alt = self.alt or ()
        if alt and alt[0] == "E7" and alt[1] in ("first", "last"):
            r = min(tied, key=lambda r: r["_pos"]) if alt[1] == "first" else max(tied, key=lambda r: r["_pos"])
            return r[idcol]
        if self.sem.get("tie_variant") == "option":
            return TIE
        chain = list(self.sem.get("tie_chain") or [])
        for i, (tk, tdir) in enumerate(chain):
            if alt and alt[0] == "E7" and alt[1] == "dir" and i == 0:
                tdir = {"earliest": "latest", "latest": "earliest", "lowest": "highest", "highest": "lowest"}[tdir]
            if tk == idcol:
                from f9lex import id_key
                tied.sort(key=lambda r: id_key(r[idcol]), reverse=(tdir == "highest"))
                return tied[0][idcol]
            vals = [int(r[tk]) for r in tied]
            b = min(vals) if tdir == "earliest" else max(vals)
            tied = [r for r in tied if int(r[tk]) == b]
            if len(tied) == 1:
                return tied[0][idcol]
        raise Reject("tie chain did not end")

    def _op_main(self, q, shown, drop):
        op = q["op"]
        alt = self.alt or ()
        idcol = self.card["idcol"]
        rc = self.read_cols(q)
        recs = self._rows("main", rc, drop)
        f = q.get("f")
        if op == "exists":
            return any(self.ev(f, r, "main") for r in recs)
        if op in ("count", "cdist"):
            sel = self._filter(recs, f, "main")
            if op == "cdist":
                return len({_cf(r[q["col"]]) for r in sel})
            return len(sel)
        if op == "sum":
            sel = self._filter(recs, f, "main")
            return sum((to_frac(r[q["col"]]) for r in sel), Fraction(0))
        if op == "mean":
            sel = self._filter(recs, f, "main")
            if not sel:
                if alt and alt[0] == "E24":
                    return Fraction(0)
                return NO_RECORD
            return sum((to_frac(r[q["col"]]) for r in sel), Fraction(0)) / len(sel)
        if op in ("min", "max"):
            sel = self._filter(recs, f, "main")
            if not sel:
                if alt and alt[0] == "E24":
                    return Fraction(0) if self.ctype("main", q["col"]) == "num" else NO_RECORD
                return NO_RECORD
            vals = [to_frac(r[q["col"]]) if self.ctype("main", q["col"]) == "num" else int(r[q["col"]])
                    for r in sel]
            return max(vals) if op == "max" else min(vals)
        if op in ("argmax", "argmin"):
            sel = self._filter(recs, f, "main")
            return self._tie_pick(sel, q["col"], "max" if op == "argmax" else "min", idcol)
        if op == "lookup":
            hit = [r for r in self.recs("main") if r[idcol] == q["id"]]
            if not hit:
                if self.sem["world"] == "T2" and not (alt and alt[0] == "E30"):
                    return CBD
                return NO_RECORD
            r = hit[0]
            if alt and alt[0] == "E0":
                r = [x for x in self.recs("main") if x[idcol] == alt[1]][0]
            v = r[q["col"]]
            if v is None:
                if drop:
                    raise Undefined("lookup of a left-out record")
                if alt and alt[0] == "E4" and alt[1] == "zero":
                    return Fraction(0)
                raise Undefined("lookup reached UNKNOWN")
            return to_frac(v) if self.ctype("main", q["col"]) == "num" else v
        if op == "lookup_p":
            hit = [r for r in recs if r[idcol] == q["id"]]
            if not hit:
                raise Undefined("yes/no subject not listed or left out")
            return self.ev(q["p"], hit[0], "main")
        if op == "presence":
            return any(r[idcol] == q["id"] for r in self.recs("main"))
        if op == "forall":
            sel = self._filter(recs, q["a"], "main")
            if not sel:
                raise Undefined("forall over an empty set")
            return all(self.ev(q["b"], r, "main") for r in sel)
        if op == "compare":
            vals = []
            for g in ("a", "b"):
                sel = self._filter(recs, q[g], "main")
                if q["agg"] == "count":
                    vals.append(Fraction(len(sel)))
                elif q["agg"] == "sum":
                    vals.append(sum((to_frac(r[q["col"]]) for r in sel), Fraction(0)))
                else:
                    if not sel:
                        raise Undefined("compare of an empty average")
                    vals.append(sum((to_frac(r[q["col"]]) for r in sel), Fraction(0)) / len(sel))
            if alt and alt[0] == "E8":
                vals = [round_half_up(v, self.sem.get("round_dp", 1)) for v in vals]
            o = q["cmp"]
            if alt and alt[0] == "E2" and alt[1] == "cmp":
                o = {">": ">=", ">=": ">", "<": "<=", "<=": "<"}.get(o, o)
            return cmp_op(vals[0], o, vals[1])
        if op == "select":
            return frozenset(r[idcol] for r in self._filter(recs, f, "main"))
        if op == "cpick":
            return self._cpick(recs, f, "main", idcol, shown)
        if op == "quant_lookup":
            hit = [r for r in recs if r[idcol] == q["id"]]
            if not hit:
                raise Undefined("subject not listed")
            return self.ev({"k": "quant", "q": q["q"], "list": q["list"], "cond": q["cond"]}, hit[0], "main")
        raise KeyError(op)

    def _cpick(self, recs, f, role, idcol, shown, ctx=None):
        meet = [r[idcol] for r in recs if r[idcol] in (shown or []) and self.ev(f, r, role, ctx)]
        if len(meet) > 1:
            raise Reject("two shown options meet a condition pick")
        return meet[0] if meet else NONE

    # ---------------------------------------------------------------------------- two tables (S3)
    def _op_join(self, q, shown, drop):
        op = q["op"]
        alt = self.alt or ()
        key = self.card["idcol"]
        fk = self.card["fkcol"]
        dimcols = [c["name"] for c in self.table("dim")["cols"]]
        rc = self.read_cols(q)
        dim = self._rows("dim", [c for c in rc if c in dimcols], drop)
        factcols = [c["name"] for c in self.table("fact")["cols"]]
        facts = self._rows("fact", [c for c in rc if c in factcols], drop)
        keys = {r[key] for r in dim}
        all_keys = {r[key] for r in self.recs("dim")}
        if not (alt and alt[0] == "E6" and alt[1] == "orphans"):
            facts = [e for e in facts if e[fk] in keys]
        ev_of = {}
        for e in facts:
            ev_of.setdefault(e[fk], []).append(e)
        ctx = {"events_of": ev_of, "dim_id": key}
        fe = q.get("fe")
        fd = q.get("fd")
        if op == "ent_any":
            if q["key"] not in keys:
                raise Undefined("subject left out or unlisted")
            return any(self.ev(fe, e, "fact") for e in ev_of.get(q["key"], []))
        if op == "ent_sum":
            if q["key"] not in keys:
                raise Undefined("subject left out")
            return sum((to_frac(e[q["col"]]) for e in ev_of.get(q["key"], []) if self.ev(fe, e, "fact")),
                       Fraction(0))
        if op == "ent_attr":
            hit = [r for r in self.recs("dim") if r[key] == q["key"]]
            if not hit:
                return NO_RECORD
            v = hit[0][q["col"]]
            if v is None:
                raise Undefined("lookup reached UNKNOWN")
            return to_frac(v) if self.ctype("dim", q["col"]) == "num" else v
        if op == "g_count":
            ents = [r for r in dim if self.ev(fd, r, "dim", ctx)]
            if alt and alt[0] == "E6" and alt[1] == "orphans":
                ks = {r[key] for r in ents}
                return sum(1 for e in facts if (e[fk] in ks or e[fk] not in all_keys) and self.ev(fe, e, "fact"))
            ks = {r[key] for r in ents}
            return sum(1 for e in facts if e[fk] in ks and self.ev(fe, e, "fact"))
        if op == "g_argmax":
            ents = [r for r in dim if self.ev(fd, r, "dim", ctx)]
            score = {}
            for r in ents:
                evs = [e for e in ev_of.get(r[key], []) if self.ev(fe, e, "fact")]
                if q["agg"] == "count":
                    score[r[key]] = Fraction(len(evs))
                else:
                    score[r[key]] = sum((to_frac(e[q["col"]]) for e in evs), Fraction(0))
            if alt and alt[0] == "E6" and alt[1] == "zero_drop":
                score = {k: v for k, v in score.items() if any(self.ev(fe, e, "fact") for e in ev_of.get(k, []))}
            if not score or all(v == 0 for v in score.values()):  # counts AND totals (T23, F9-R5-03; G2 fix r03)
                raise Undefined("every group at 0")
            best = max(score.values()) if q["dir"] == "max" else min(score.values())
            tied = sorted([k for k, v in score.items() if v == best], key=lambda s: __import__("f9lex").id_key(s))
            if len(tied) == 1:
                return tied[0]
            if alt and alt[0] == "E7" and alt[1] in ("first", "last"):
                pos = {r[key]: r["_pos"] for r in self.recs("dim")}
                tied.sort(key=lambda k: pos[k])
                return tied[0] if alt[1] == "first" else tied[-1]
            if self.sem.get("tie_variant") == "option":
                return TIE
            tdir = self.sem["tie_chain"][0][1]
            if alt and alt[0] == "E7" and alt[1] == "dir":
                tdir = "highest" if tdir == "lowest" else "lowest"
            return tied[0] if tdir == "lowest" else tied[-1]
        if op == "select":
            return frozenset(r[key] for r in dim if self.ev(q["f"], r, "dim", ctx))
        if op == "cpick":
            return self._cpick(dim, q["f"], "dim", key, shown, ctx)
        if op == "exists":
            return any(self.ev(q["f"], r, "dim", ctx) for r in dim)
        raise KeyError(op)

    # ---------------------------------------------------------------------------- logs (S6)
    def _lines(self):
        recs = self.recs("log")
        if self.alt and self.alt[0] == "E34":
            seen, out = set(), []
            for r in recs:
                k = tuple((c, str(r[c])) for c in r if c != "_pos")
                if k in seen:
                    continue
                seen.add(k)
                out.append(r)
            recs = out
        return recs

    def _op_log(self, q, shown, drop):
        op = q["op"]
        alt = self.alt or ()
        lines = self._lines()
        f = q.get("f")
        if op == "count_lines":
            return sum(1 for r in lines if self.ev(f, r, "log"))
        if op == "exists_lines":
            return any(self.ev(f, r, "log") for r in lines)
        if op in ("first", "last"):
            sel = [r for r in lines if self.ev(f, r, "log")]
            if not sel:
                return NO_RECORD
            if alt and alt[0] == "E27":
                r = min(sel, key=lambda r: r["_pos"]) if op == "first" else max(sel, key=lambda r: r["_pos"])
                return int(r["time"])
            ts = [int(r["time"]) for r in sel]
            return min(ts) if op == "first" else max(ts)
        if op == "comp_argmax":
            comps = sorted({r["component"] for r in self.recs("log")},
                           key=lambda s: __import__("f9lex").id_key(s))
            cnt = {c: sum(1 for r in lines if r["component"] == c and self.ev(f, r, "log")) for c in comps}
            if all(v == 0 for v in cnt.values()):
                raise Undefined("every component at 0")
            best = max(cnt.values())
            tied = [c for c in comps if cnt[c] == best]
            if len(tied) == 1:
                return tied[0]
            if alt and alt[0] == "E7" and alt[1] in ("first", "last"):
                firstpos = {}
                for r in self.recs("log"):
                    firstpos.setdefault(r["component"], r["_pos"])
                tied.sort(key=lambda c: firstpos[c])
                return tied[0] if alt[1] == "first" else tied[-1]
            if self.sem.get("tie_variant") == "option":
                return TIE
            tdir = self.sem["tie_chain"][0][1]
            if alt and alt[0] == "E7" and alt[1] == "dir":
                tdir = "highest" if tdir == "lowest" else "lowest"
            return tied[0] if tdir == "lowest" else tied[-1]
        lines_of = {}
        for r in lines:
            if r["request"]:
                lines_of.setdefault(r["request"], []).append(r)
        reqs = sorted(lines_of, key=lambda s: __import__("f9lex").id_key(s))
        ctx = {"lines_of": lines_of}
        if op == "req_any":
            if q["req"] not in lines_of:
                raise Undefined("request not in the log")
            return self.ev({"k": "lift", "a": q["a"]}, {"request": q["req"]}, "req", ctx)
        if alt and alt[0] == "E32" and alt[1] == "same_line":
            def evr(p, req):
                return any(self._ev_same_line(p, ln, ctx) for ln in lines_of[req])
        else:
            def evr(p, req):
                return self.ev(p, {"request": req}, "req", ctx)
        if op == "select":
            return frozenset(rq for rq in reqs if evr(q["f"], rq))
        if op == "cpick":
            meet = [rq for rq in reqs if rq in (shown or []) and evr(q["f"], rq)]
            if len(meet) > 1:
                raise Reject("two shown options meet a condition pick")
            return meet[0] if meet else NONE
        raise KeyError(op)

    def _ev_same_line(self, p, ln, ctx):
        k = p["k"]
        if k == "and":
            return all(self._ev_same_line(x, ln, ctx) for x in p["args"])
        if k == "or":
            return any(self._ev_same_line(x, ln, ctx) for x in p["args"])
        if k == "not":
            return not self._ev_same_line(p["arg"], ln, ctx)
        if k == "lift":
            return self.ev(p["a"], ln, "log", ctx)
        return self.ev(p, ln, "log", ctx)

    # ---------------------------------------------------------------------------- pivot (S5, dev only)
    def _melt(self):
        pv = self.s["pivot"]
        rows = []
        for e in pv["entities"]:
            for j, per in enumerate(pv["periods"]):
                v = pv["cells"][e][j]
                marked = [e, j] in pv["marks"] or (e, j) in {tuple(m) for m in pv["marks"]}
                rows.append({"entity": e, "period": per, "value": to_frac(v), "marked": marked})
        return pd.DataFrame(rows)

    def _op_pivot(self, q, shown, drop):
        d = self._melt()
        alt = self.alt or ()
        if not (alt and alt[0] == "E13" and alt[1] == "with_marked"):
            if alt and alt[0] == "E26" and alt[1] == "footnote_row":
                bad = set(d[d["marked"]]["entity"])
                d = d[~d["entity"].isin(bad)]
            else:
                d = d[~d["marked"]]
        op = q["op"]
        if op == "cell":
            x = d[(d["entity"] == q["ent"]) & (d["period"] == q["period"])]
            if x.empty:
                raise Undefined("marked cell named alone")
            return x["value"].iloc[0]
        if op == "row_total":
            return sum(d[d["entity"] == q["ent"]]["value"], Fraction(0))
        if op == "row_top":
            tot = {e: sum(d[d["entity"] == e]["value"], Fraction(0)) for e in self.s["pivot"]["entities"]}
            dr = q["dir"] if not (alt and alt[0] == "E7" and alt[1] == "dir") else {"max": "min", "min": "max"}[q["dir"]]
            best = max(tot.values()) if dr == "max" else min(tot.values())
            tied = sorted([e for e, v in tot.items() if v == best], key=lambda s: __import__("f9lex").id_key(s))
            if len(tied) > 1:
                if self.sem.get("tie_variant") == "option":
                    return TIE
                return tied[0] if self.sem["tie_chain"][0][1] == "lowest" else tied[-1]
            return tied[0]
        if op == "col_count":
            x = d[d["period"] == q["period"]]
            lit = to_frac(q["lit"])
            return int(sum(1 for v in x["value"] if cmp_op(v, q["cmp"], lit)))
        raise KeyError(op)


def display_round(v: Fraction, dp: int, alt=None) -> Fraction:
    if alt and alt[0] == "E23":
        return round_half_even(v, dp)
    return round_half_up(v, dp)
