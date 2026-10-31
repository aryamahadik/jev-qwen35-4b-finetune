"""Solver B (G2 / G3): sqlite over the structure PARSED from the rendered text. A different paradigm from solver A:
relational tables, SQL compiled from the parsed query AST, numbers as scaled integers (10^6), dates as day ordinals,
date-times as epoch seconds, explicit IS NOT NULL for T4, a completion loop for T5, phantom rows for T2 unlisted-ID
lookups, EXISTS for lifts and list quantifiers, integer cross-multiplication for exact comparison of averages.
Never relies on SQL three-valued logic: every compiled predicate runs on rows whose read columns are not NULL,
except under the E4 alternative, which is compiled explicitly."""
from __future__ import annotations

import itertools
import sqlite3
from fractions import Fraction

from f9ast import atoms, pred_cols

SCALE = 10 ** 6
NO_RECORD, CBD, TIE, NONE = "<NO_RECORD>", "<CBD>", "<TIE>", "<NONE>"
SPECIALS = (NO_RECORD, CBD, TIE, NONE)


class BUndefined(Exception):
    pass


class BReject(Exception):
    pass


def sc(v):
    v = Fraction(v)
    x = v * SCALE
    if x.denominator != 1:
        raise BReject("literal beyond 6 decimals")
    return int(x)


def _q(name):
    return '"' + name.replace('"', '""') + '"'


class SolverB:
    def __init__(self, P):
        """P: the parse result (f9g3.parse_row): tables, ctx (world, missing, t5, terms, tie, levels, round_dp,
        conv, zone, sampler)."""
        self.P = P
        self.ctx = P["ctx"]
        self.db = sqlite3.connect(":memory:")
        self.db.execute("PRAGMA case_sensitive_like = OFF")
        self.types = {}
        self.alt = None
        self._load()

    # -------------------------------------------------------------------------------------------- load
    def _load(self):
        for t in self.P["btables"]:
            role = t["role"]
            cols = [c for c in t["cols"] if c["type"] != "list"]
            defs = ["_pos INTEGER", "_listed INTEGER"] + [f"{_q(c['name'])} {'TEXT' if c['type'] in ('cat', 'id', 'fk', 'comp', 'req', 'lvl', 'text') else 'INTEGER'}" for c in cols]
            if role == "log":
                defs.append("_lvl INTEGER")
            self.db.execute(f"CREATE TABLE {role} ({', '.join(defs)})")
            for c in t["cols"]:
                self.types[(role, c["name"])] = c
                if c["type"] == "list":
                    self.db.execute(f"CREATE TABLE items (_rec INTEGER, _j INTEGER, "
                                    + ", ".join(f"{_q(s['name'])} {'TEXT' if s['type'] == 'cat' else 'INTEGER'}"
                                                for s in c["sub"]) + ")")
                    self.db.execute("CREATE TABLE lists (_rec INTEGER, state TEXT)")
                    for s in c["sub"]:
                        self.types[("item", s["name"])] = s
            for i, r in enumerate(t["rows"]):
                vals = [i, 1]
                for c, v in zip(t["cols"], r):
                    if c["type"] == "list":
                        st = "null" if v is None else ("empty" if not v else "value")
                        self.db.execute("INSERT INTO lists VALUES (?, ?)", (i, st))
                        for j, it in enumerate(v or []):
                            self.db.execute(f"INSERT INTO items VALUES ({', '.join(['?'] * (2 + len(it)))})",
                                            [i, j] + [self._enc(x, s) for x, s in zip(it, c["sub"])])
                        continue
                    vals.append(self._enc(v, c))
                if role == "log":
                    vals.append(self.ctx["levels"].index(r[[c["name"] for c in t["cols"]].index("level")]))
                self.db.execute(f"INSERT INTO {role} VALUES ({', '.join(['?'] * len(vals))})", vals)

    def _enc(self, v, c):
        if v is None:
            return None
        t = c["type"]
        if t == "num":
            return sc(v)
        if t == "bool":
            return 1 if v else 0
        if t in ("date", "dt"):
            return int(v)
        return str(v)

    # -------------------------------------------------------------------------------------------- predicates
    def conv_factor(self, col_unit, lit_unit):
        """(num, den): literal in lit_unit -> col_unit multiply by num/den (T28 stated factors only)."""
        if not lit_unit or not col_unit or lit_unit == col_unit:
            return 1, 1
        if self.alt and self.alt[0] == "E9":
            return 1, 1
        conv = self.ctx.get("conv") or {}
        if f"{lit_unit}->{col_unit}" in conv:
            return int(conv[f"{lit_unit}->{col_unit}"]), 1
        if f"{col_unit}->{lit_unit}" in conv:
            return 1, int(conv[f"{col_unit}->{lit_unit}"])
        raise BReject("no stated factor")

    def sql(self, p, role, tab):
        """-> (sql expression, params). tab: the SQL alias of the row's table."""
        if p is None:
            return "1", []
        k = p["k"]
        if k in ("and", "or"):
            parts = [self.sql(x, role, tab) for x in p["args"]]
            j = " AND " if k == "and" else " OR "
            return "(" + j.join(x[0] for x in parts) + ")", [v for x in parts for v in x[1]]
        if k == "not":
            s, a = self.sql(p["arg"], role, tab)
            return f"(NOT {s})", a
        if k == "xor":
            (s1, a1), (s2, a2) = (self.sql(x, role, tab) for x in p["args"])
            return f"(({s1}) <> ({s2}))", a1 + a2
        if k == "term":
            return self.term_sql(p["name"], role, tab)
        if k == "has":
            s, a = self.sql(p["fe"], "fact", "e")
            key = self.ctx["key"]
            return f"EXISTS (SELECT 1 FROM fact e WHERE e.{_q(key)} = {tab}.{_q(key)} AND {self.notnull(p['fe'], 'fact', 'e')} AND {s})", a
        if k == "lift":
            return self.lift_sql(p, tab)
        if k == "line":
            parts, a = [], []
            if p.get("level") is not None:
                op = p.get("lvl_op", "=")
                parts.append(f"{tab}._lvl {op} ?")
                a.append(self.ctx["levels"].index(p["level"]))
            if p.get("comp") is not None:
                parts.append(f"{tab}.component = ?")
                a.append(p["comp"])
            return "(" + " AND ".join(parts or ["1"]) + ")", a
        if k == "quant":
            s, a = self.sql(p["cond"], "item", "it")
            ex = f"EXISTS (SELECT 1 FROM items it WHERE it._rec = {tab}._pos AND {s})"
            nonempty = f"EXISTS (SELECT 1 FROM items it WHERE it._rec = {tab}._pos)"
            nfail = f"NOT EXISTS (SELECT 1 FROM items it WHERE it._rec = {tab}._pos AND NOT ({s}))"
            vac = self.alt and self.alt[0] == "E20"
            if p["q"] == "any":
                return ex, a
            if p["q"] == "every":
                return (f"({nfail})" if vac else f"({nfail} AND {nonempty})"), a
            if p["q"] == "no":
                return (f"(NOT {ex} AND {nonempty})" if vac else f"(NOT {ex})"), a
        col = p["col"]
        c = self.types[(role, col)]
        ref = f"{tab}.{_q(col)}"
        e4 = self.alt and self.alt[0] == "E4" and self.alt[1] == "meet"
        if k == "cmp":
            if c["type"] == "num":
                n, d = self.conv_factor(c.get("unit"), p.get("unit"))
                lit = Fraction(p["lit"])
                expr = f"({ref} * ?) {p['op'].replace('!=', '<>')} (? * ?)"
                args = [d, sc(lit), n]
                # ref * d  op  lit * n   (lit converted to the column unit = lit * n / d)
            elif c["type"] in ("date", "dt"):
                expr, args = f"{ref} {p['op'].replace('!=', '<>')} ?", [int(p["lit"])]
            elif p["op"] in ("=", "!="):
                expr = f"LOWER(TRIM({ref})) {'=' if p['op'] == '=' else '<>'} LOWER(TRIM(?))"
                args = [str(p["lit"])]
            else:
                raise BReject("op on text")
        elif k == "between":
            n, d = self.conv_factor(c.get("unit"), p.get("unit"))
            if p.get("open"):
                expr = f"(({ref} * ?) > (? * ?) AND ({ref} * ?) < (? * ?))"
            else:
                expr = f"(({ref} * ?) >= (? * ?) AND ({ref} * ?) <= (? * ?))"
            args = [d, sc(p["lo"]), n, d, sc(p["hi"]), n]
        elif k == "in":
            expr = "LOWER(TRIM(" + ref + ")) IN (" + ", ".join("LOWER(TRIM(?))" for _ in p["vals"]) + ")"
            args = [str(v) for v in p["vals"]]
        elif k == "win":
            x = ref
            if p.get("unit") == "day" and c["type"] == "dt":
                x = f"((({ref} + {self.ctx.get('zone', 0) * 60}) / 86400) + 719163)"
            parts, args = [], []
            if p.get("lo") is not None:
                parts.append(f"{x} {'>=' if p.get('li', True) else '>'} ?")
                args.append(int(p["lo"]))
            if p.get("hi") is not None:
                parts.append(f"{x} {'<=' if p.get('hi_i', True) else '<'} ?")
                args.append(int(p["hi"]))
            expr = "(" + " AND ".join(parts or ["1"]) + ")"
        elif k == "contains":
            if self.alt and self.alt[0] == "E25":
                expr, args = f"instr({ref}, ?) > 0", [p["s"]]
            else:
                expr, args = f"instr(LOWER({ref}), LOWER(?)) > 0", [p["s"]]
        else:
            raise BReject(f"atom {k}")
        if e4:
            return f"({ref} IS NULL OR ({expr}))", args
        return f"({expr})", args

    def term_sql(self, name, role, tab):
        t = self.ctx["terms"][name]
        alt = self.alt or ()
        tag = alt[0] if alt else None

        def S(p):
            return self.sql(p, role, tab)
        if tag == "E26" and alt[1] == "usual_meaning" and t.get("usual"):
            return S(t["usual"])
        if t["kind"] == "T7":
            a, b = S(t["A"]), S(t["B"])
            gen = (f"({a[0]} OR {b[0]})" if tag == "E16" else f"({a[0]} AND NOT {b[0]})"), a[1] + b[1]
        elif t["kind"] == "T8":
            a, c = S(t["A"]), S(t["C"])
            gen = (a if tag == "E17" else (f"({a[0]} AND {c[0]})", a[1] + c[1]))
        else:
            parts = [S(x) for x in t["list"]]
            gen = "(" + " AND ".join(x[0] for x in parts) + ")", [v for x in parts for v in x[1]]
        ovs = t.get("overrides") or []
        if not ovs or (tag == "E26" and alt[1] == "general_over_specific"):
            return gen
        sql, args = gen
        cases, cargs = [], []
        for o in ovs:
            cs, ca = S(o["cond"])
            if tag == "E26" and alt[1] == "unless_kept" and t["kind"] == "T7":
                b = S(t["B"])
                cs, ca = f"({cs} AND NOT {b[0]})", ca + b[1]
            elif tag == "E26" and alt[1] == "closure_kept":
                cs, ca = f"({cs} AND {gen[0]})", ca + gen[1]
            cases.append(f"WHEN LOWER(TRIM({tab}.{_q(o['col'])})) = LOWER(TRIM(?)) THEN {cs}")
            cargs += [str(o["val"])] + ca
        return f"(CASE {' '.join(cases)} ELSE {sql} END)", cargs + args

    def lift_sql(self, p, tab):
        mode = self.alt[1] if self.alt and self.alt[0] == "E32" else None
        s, a = self.sql(p["a"], "log", "l2")
        if mode in ("last_line", "first_line"):
            agg = "MAX" if mode == "last_line" else "MIN"
            pick = (f"(SELECT l3._pos FROM log l3 WHERE l3.request = {tab}.request ORDER BY l3.time "
                    f"{'DESC' if mode == 'last_line' else 'ASC'}, l3._pos {'DESC' if mode == 'last_line' else 'ASC'} "
                    f"LIMIT 1)")
            return f"EXISTS (SELECT 1 FROM log l2 WHERE l2._pos = {pick} AND {s})", a
        return f"EXISTS (SELECT 1 FROM log l2 WHERE l2.request = {tab}.request AND {s})", a

    def notnull(self, p, role, tab):
        cols = [c for c in pred_cols(p, self.ctx["terms"]) if (role, c) in self.types]
        if not cols:
            return "1"
        return "(" + " AND ".join(f"{tab}.{_q(c)} IS NOT NULL" for c in cols) + ")"

    # -------------------------------------------------------------------------------------------- top level
    def answer(self, q, alt=None, shown=None):
        self.alt = alt
        try:
            miss = self.ctx.get("missing")
            if miss == "T5" and not (alt and alt[0] in ("E29", "E4")):
                return self._t5(q, shown)
            return self._op(q, shown, drop=(miss == "T4" or bool(alt and alt[0] == "E29")))
        finally:
            self.alt = None

    def read_cols(self, q):
        b = q
        while b["op"] in ("thr", "not"):
            b = b["inner"]
        cols = []
        for key in ("f", "a", "b", "p", "fe", "fd", "cond"):
            if isinstance(b.get(key), dict):
                cols += pred_cols(b[key], self.ctx["terms"])
        if b.get("col"):
            cols.append(b["col"])
        if b["op"] == "quant_lookup":
            cols.append(b["list"])
        if b["op"] in ("argmax", "argmin"):
            for tk in (self.ctx.get("tie") or [])[1:]:
                cols.append(tk[0])
        return list(dict.fromkeys(cols))

    def _t5(self, q, shown):
        rc = set(self.read_cols(q))
        cells = []
        for t in self.P["btables"]:
            for c in t["cols"]:
                if c["name"] in rc and c["type"] != "list":
                    for (pos,) in self.db.execute(f"SELECT _pos FROM {t['role']} WHERE {_q(c['name'])} IS NULL"):
                        cells.append((t["role"], pos, c))
        if not cells:
            return self._op(q, shown, drop=False)
        if len(cells) > 3:
            raise BReject("more than 3 unknown read cells")
        doms = []
        for role, pos, c in cells:
            d = self.ctx["t5"].get(c["name"])
            if d is None:
                raise BReject("unknown cell outside the stated domains")
            doms.append(d)
        answers = {}
        try:
            for combo in itertools.product(*doms):
                for (role, pos, c), v in zip(cells, combo):
                    self.db.execute(f"UPDATE {role} SET {_q(c['name'])} = ? WHERE _pos = ?", (self._enc(v, c), pos))
                a = self._op(q, shown, drop=False)
                answers.setdefault(self.P["render_key"](q, a), a)
        finally:
            for role, pos, c in cells:
                self.db.execute(f"UPDATE {role} SET {_q(c['name'])} = NULL WHERE _pos = ?", (pos,))
        if len(answers) == 1:
            return next(iter(answers.values()))
        if q["op"] == "cpick" and all(a == NONE for a in answers.values()):
            return NONE
        return CBD

    def _op(self, q, shown, drop):
        op = q["op"]
        if op == "not":
            return not self._op(q["inner"], shown, drop)
        if op == "thr":
            v = self._op(q["inner"], shown, drop)
            if v in SPECIALS:
                raise BUndefined("threshold over undefined")
            lit = Fraction(q["lit"])
            ib = q["inner"]
            if q.get("unit") and ib.get("col"):
                role = {"ent_sum": "fact"}.get(ib["op"], "main")
                c = self.types.get((role, ib["col"]))
                if c and c.get("unit"):
                    n, d = self.conv_factor(c["unit"], q["unit"])
                    lit = lit * n / d
            if self.alt and self.alt[0] == "E8" and isinstance(v, Fraction):
                v = half_up(v, self.ctx.get("round_dp", 1))
            o = q["cmp"]
            if self.alt and self.alt[0] == "E2" and self.alt[1] == "thr":
                o = {">=": ">", ">": ">=", "<=": "<", "<": "<="}.get(o, o)
            return {">=": v >= lit, ">": v > lit, "<=": v <= lit, "<": v < lit, "=": v == lit, "!=": v != lit}[o]
        s = self.ctx["sampler"]
        if s in ("S1", "S2", "S4"):
            return self._main(q, shown, drop)
        if s == "S3":
            return self._join(q, shown, drop)
        if s == "S6":
            return self._log(q, shown, drop)
        if s == "S5":
            return self._pivot(q, shown, drop)
        raise BReject(s)

    # ------------------------------------------------------------------------------------------------ main
    def _where(self, f, role, tab, drop, extra_cols=(), listed=False):
        s, a = self.sql(f, role, tab)
        w = [s]
        if drop:
            cols = [c for c in list(pred_cols(f, self.ctx["terms"])) + list(extra_cols)
                    if (role, c) in self.types and self.types[(role, c)]["type"] != "list"]
            for c in dict.fromkeys(cols):
                w.append(f"{tab}.{_q(c)} IS NOT NULL")
        if listed:
            w.append(f"{tab}._listed = 1")
        return " AND ".join(w), a

    def _main(self, q, shown, drop):
        op = q["op"]
        idc = self.ctx["idcol"]
        db = self.db
        alt = self.alt or ()
        rc = self.read_cols(q)
        if op in ("exists", "count", "cdist", "sum", "mean", "min", "max", "argmax", "argmin", "select"):
            extra = [q["col"]] if q.get("col") else []
            if op in ("argmax", "argmin"):
                extra += [tk[0] for tk in (self.ctx.get("tie") or [])[1:]]
            w, a = self._where(q.get("f"), "main", "m", drop, extra, listed=True)
            if op == "exists":
                return db.execute(f"SELECT EXISTS (SELECT 1 FROM main m WHERE {w})", a).fetchone()[0] == 1
            if op == "count":
                return db.execute(f"SELECT COUNT(*) FROM main m WHERE {w}", a).fetchone()[0]
            if op == "cdist":
                return db.execute(f"SELECT COUNT(DISTINCT LOWER(TRIM(m.{_q(q['col'])}))) FROM main m WHERE {w}",
                                  a).fetchone()[0]
            if op == "select":
                return frozenset(r[0] for r in db.execute(f"SELECT m.{_q(idc)} FROM main m WHERE {w}", a))
            col = q["col"]
            c = self.types[("main", col)]
            if op in ("sum", "mean"):
                n, tot = db.execute(f"SELECT COUNT(*), TOTAL(m.{_q(col)}) FROM main m WHERE {w}", a).fetchone()
                tot = int(db.execute(f"SELECT COALESCE(SUM(m.{_q(col)}), 0) FROM main m WHERE {w}", a).fetchone()[0])
                if op == "sum":
                    return Fraction(tot, SCALE)
                if n == 0:
                    if alt and alt[0] == "E24":
                        return Fraction(0)
                    return NO_RECORD
                return Fraction(tot, SCALE * n)
            if op in ("min", "max"):
                r = db.execute(f"SELECT {op.upper()}(m.{_q(col)}), COUNT(*) FROM main m WHERE {w}", a).fetchone()
                if r[1] == 0:
                    if alt and alt[0] == "E24" and c["type"] == "num":
                        return Fraction(0)
                    return NO_RECORD
                return Fraction(r[0], SCALE) if c["type"] == "num" else int(r[0])
            # argmax / argmin with the T24 chain
            return self._pick(f"SELECT m.{_q(idc)}, m.{_q(col)}, m._pos" + "".join(
                f", m.{_q(tk[0])}" for tk in (self.ctx.get("tie") or [])[1:]) + f" FROM main m WHERE {w}", a,
                op == "argmax", idc)
        if op == "lookup":
            r = db.execute(f"SELECT {_q(q['col'])}, _listed FROM main WHERE {_q(idc)} = ?", (q["id"],)).fetchall()
            if not r:
                if self.ctx["world"] == "T2" and not (alt and alt[0] == "E30"):
                    return self._phantom_lookup(q)
                return NO_RECORD
            v = r[0][0]
            if v is None:
                if alt and alt[0] == "E4" and alt[1] == "zero":
                    return Fraction(0)
                raise BUndefined("lookup of unknown")
            c = self.types[("main", q["col"])]
            return Fraction(v, SCALE) if c["type"] == "num" else (int(v) if c["type"] == "date" else v)
        if op == "lookup_p":
            w, a = self._where(q["p"], "main", "m", drop)
            ok = db.execute(f"SELECT COUNT(*) FROM main m WHERE m.{_q(idc)} = ? AND {self._nn(q['p'], drop)}",
                            [q["id"]]).fetchone()[0]
            if not ok:
                raise BUndefined("subject left out or unlisted")
            return db.execute(f"SELECT EXISTS (SELECT 1 FROM main m WHERE m.{_q(idc)} = ? AND {w})",
                              [q["id"]] + a).fetchone()[0] == 1
        if op == "presence":
            return db.execute(f"SELECT EXISTS (SELECT 1 FROM main WHERE {_q(idc)} = ?)", (q["id"],)).fetchone()[0] == 1
        if op == "forall":
            wa, aa = self._where(q["a"], "main", "m", drop, pred_cols(q["b"], self.ctx["terms"]), listed=True)
            sb, ab = self.sql(q["b"], "main", "m")
            n = db.execute(f"SELECT COUNT(*) FROM main m WHERE {wa}", aa).fetchone()[0]
            if n == 0:
                raise BUndefined("forall over empty")
            bad = db.execute(f"SELECT COUNT(*) FROM main m WHERE {wa} AND NOT {sb}", aa + ab).fetchone()[0]
            return bad == 0
        if op == "compare":
            vals = []
            for g in ("a", "b"):
                w, a = self._where(q[g], "main", "m", drop, [q["col"]] if q.get("col") else [], listed=True)
                if q["agg"] == "count":
                    vals.append(Fraction(db.execute(f"SELECT COUNT(*) FROM main m WHERE {w}", a).fetchone()[0]))
                else:
                    n, tot = db.execute(f"SELECT COUNT(*), COALESCE(SUM(m.{_q(q['col'])}), 0) FROM main m WHERE {w}",
                                        a).fetchone()
                    if q["agg"] == "sum":
                        vals.append(Fraction(int(tot), SCALE))
                    else:
                        if n == 0:
                            raise BUndefined("empty average")
                        vals.append(Fraction(int(tot), SCALE * n))
            if alt and alt[0] == "E8":
                vals = [half_up(v, self.ctx.get("round_dp", 1)) for v in vals]
            o = q["cmp"]
            if alt and alt[0] == "E2" and alt[1] == "cmp":
                o = {">": ">=", ">=": ">", "<": "<=", "<=": "<"}.get(o, o)
            x, y = vals
            return {">": x > y, ">=": x >= y, "<": x < y, "<=": x <= y, "=": x == y}[o]
        if op == "cpick":
            return self._cpick("main", "m", idc, q["f"], shown, drop)
        if op == "quant_lookup":
            p = {"k": "quant", "q": q["q"], "list": q["list"], "cond": q["cond"]}
            s, a = self.sql(p, "main", "m")
            r = db.execute(f"SELECT m._pos, l.state FROM main m JOIN lists l ON l._rec = m._pos WHERE m.{_q(idc)} = ?",
                           [q["id"]]).fetchall()
            if not r:
                raise BUndefined("subject not listed")
            if r[0][1] == "null":
                raise BUndefined("null list")
            return db.execute(f"SELECT EXISTS (SELECT 1 FROM main m WHERE m.{_q(idc)} = ? AND {s})",
                              [q["id"]] + a).fetchone()[0] == 1
        raise BReject(f"op {op}")

    def _nn(self, p, drop):
        if not drop:
            return "1"
        return self.notnull(p, "main", "m")

    def _pick(self, sql, args, is_max, idc):
        rows = self.db.execute(sql, args).fetchall()
        if not rows:
            return NO_RECORD
        best = max(r[1] for r in rows) if is_max else min(r[1] for r in rows)
        tied = [r for r in rows if r[1] == best]
        if len(tied) == 1:
            return tied[0][0]
        alt = self.alt or ()
        if alt and alt[0] == "E7" and alt[1] in ("first", "last"):
            r = min(tied, key=lambda r: r[2]) if alt[1] == "first" else max(tied, key=lambda r: r[2])
            return r[0]
        tie = self.ctx.get("tie") or ["key"]
        if tie[0] == "option":
            return TIE
        chain = tie[1:]
        for i, (col, d) in enumerate(chain):
            if alt and alt[0] == "E7" and alt[1] == "dir" and i == 0:
                d = {"earliest": "latest", "latest": "earliest", "lowest": "highest", "highest": "lowest"}[d]
            if col == idc:
                tied.sort(key=lambda r: int(r[0].split("-")[1]), reverse=(d == "highest"))
                return tied[0][0]
            j = 3 + i
            vals = [r[j] for r in tied]
            b = min(vals) if d in ("earliest", "lowest") else max(vals)
            tied = [r for r in tied if r[j] == b]
            if len(tied) == 1:
                return tied[0][0]
        raise BReject("tie chain open")

    def _cpick(self, role, tab, idc, f, shown, drop, extra=""):
        w, a = self._where(f, role, tab, drop)
        meet = [r[0] for r in self.db.execute(f"SELECT {tab}.{_q(idc)} FROM {role} {tab} WHERE {w}", a)]
        hit = [x for x in shown or [] if x in meet]
        if len(hit) > 1:
            raise BReject("two shown options meet")
        return hit[0] if hit else NONE

    def _phantom_lookup(self, q):
        """T2 phantom extension for an unlisted ID: phantoms carrying that ID take the column's critical values
        (lowest and highest listed value one unit step outside, or two category values); different answers ->
        cannot be determined."""
        c = self.types[("main", q["col"])]
        col = q["col"]
        vals = [r[0] for r in self.db.execute(f"SELECT {_q(col)} FROM main WHERE {_q(col)} IS NOT NULL")]
        if c["type"] == "num":
            step = SCALE // (10 ** c.get("dp", 0))
            crit = [min(vals) - step if min(vals) - step >= 0 else max(vals) + 2 * step, max(vals) + step]
        elif c["type"] == "date":
            crit = [min(vals) - 1, max(vals) + 1]
        else:
            crit = sorted(set(vals))[:2] if len(set(vals)) >= 2 else [vals[0], vals[0] + " x"]
        answers = set()
        for v in crit:
            answers.add(v)
        return CBD if len(answers) > 1 else NO_RECORD

    # ------------------------------------------------------------------------------------------------ join
    def _join(self, q, shown, drop):
        op = q["op"]
        db = self.db
        key = self.ctx["key"]
        alt = self.alt or ()
        rc = self.read_cols(q)
        dim_nn = " AND ".join([f"d.{_q(c)} IS NOT NULL" for c in rc if ("dim", c) in self.types] or ["1"]) \
            if drop else "1"
        ev_nn = " AND ".join([f"e.{_q(c)} IS NOT NULL" for c in rc if ("fact", c) in self.types and c != key] or ["1"]) \
            if drop else "1"
        orph = alt and alt[0] == "E6" and alt[1] == "orphans"
        join = "1" if orph else f"e.{_q(key)} IN (SELECT d.{_q(key)} FROM dim d WHERE {dim_nn})"
        if op == "ent_any":
            ok = db.execute(f"SELECT COUNT(*) FROM dim d WHERE d.{_q(key)} = ? AND {dim_nn}", [q["key"]]).fetchone()[0]
            if not ok:
                raise BUndefined("subject")
            s, a = self.sql(q["fe"], "fact", "e")
            return db.execute(f"SELECT EXISTS (SELECT 1 FROM fact e WHERE e.{_q(key)} = ? AND {ev_nn} AND {s})",
                              [q["key"]] + a).fetchone()[0] == 1
        if op == "ent_sum":
            ok = db.execute(f"SELECT COUNT(*) FROM dim d WHERE d.{_q(key)} = ? AND {dim_nn}", [q["key"]]).fetchone()[0]
            if not ok:
                raise BUndefined("subject")
            s, a = self.sql(q.get("fe"), "fact", "e")
            v = db.execute(f"SELECT COALESCE(SUM(e.{_q(q['col'])}), 0) FROM fact e WHERE e.{_q(key)} = ? AND {ev_nn} "
                           f"AND {s}", [q["key"]] + a).fetchone()[0]
            return Fraction(int(v), SCALE)
        if op == "ent_attr":
            r = db.execute(f"SELECT {_q(q['col'])} FROM dim WHERE {_q(key)} = ?", [q["key"]]).fetchall()
            if not r:
                return NO_RECORD
            v = r[0][0]
            if v is None:
                raise BUndefined("unknown")
            c = self.types[("dim", q["col"])]
            return Fraction(v, SCALE) if c["type"] == "num" else v
        if op == "g_count":
            sd, ad = self.sql(q.get("fd"), "dim", "d")
            se, ae = self.sql(q.get("fe"), "fact", "e")
            ents = f"SELECT d.{_q(key)} FROM dim d WHERE {dim_nn} AND {sd}"
            if orph:
                cond = f"(e.{_q(key)} IN ({ents}) OR e.{_q(key)} NOT IN (SELECT {_q(key)} FROM dim))"
            else:
                cond = f"e.{_q(key)} IN ({ents})"
            return db.execute(f"SELECT COUNT(*) FROM fact e WHERE {cond} AND {ev_nn} AND {se}",
                              ad + ae).fetchone()[0]
        if op == "g_argmax":
            sd, ad = self.sql(q.get("fd"), "dim", "d")
            se, ae = self.sql(q.get("fe"), "fact", "e")
            # repair r1c (G3 on SQLite >= 3.36: no rowid on a subquery): the fact rowid is selected as _rid
            agg = "COUNT(e._rid)" if q["agg"] == "count" else f"COALESCE(SUM(e.{_q(q['col'])}), 0)"
            sqlq = (f"SELECT d.{_q(key)}, {agg}, d._pos, COUNT(e._rid) FROM dim d LEFT JOIN "
                    f"(SELECT e.rowid AS _rid, * FROM fact e WHERE {ev_nn} AND {se}) e ON e.{_q(key)} = d.{_q(key)} "
                    f"WHERE {dim_nn} AND {sd} GROUP BY d.{_q(key)}, d._pos")
            rows = db.execute(sqlq, ae + ad).fetchall()
            if alt and alt[0] == "E6" and alt[1] == "zero_drop":
                rows = [r for r in rows if r[3] > 0]
            if not rows or all(r[1] == 0 for r in rows):  # counts AND totals (T23, F9-R5-03; G2 fix r03)
                raise BUndefined("every group at 0")
            best = max(r[1] for r in rows)
            tied = [r for r in rows if r[1] == best]
            if len(tied) == 1:
                return tied[0][0]
            if alt and alt[0] == "E7" and alt[1] in ("first", "last"):
                r = min(tied, key=lambda r: r[2]) if alt[1] == "first" else max(tied, key=lambda r: r[2])
                return r[0]
            tie = self.ctx.get("tie") or ["key"]
            if tie[0] == "option":
                return TIE
            d = tie[1][1]
            if alt and alt[0] == "E7" and alt[1] == "dir":
                d = "highest" if d == "lowest" else "lowest"
            tied.sort(key=lambda r: int(r[0].split("-")[1]), reverse=(d == "highest"))
            return tied[0][0]
        if op in ("select", "cpick", "exists"):
            f = q["f"]
            s, a = self.sql(f, "dim", "d")
            # 'has' atoms must see only joined, non-left-out events: rebuild them with the T4 / T29 filters
            rows = [r[0] for r in db.execute(f"SELECT d.{_q(key)} FROM dim d WHERE {dim_nn} AND {s}", a)]
            if op == "select":
                return frozenset(rows)
            if op == "exists":
                return bool(rows)
            hit = [x for x in shown or [] if x in rows]
            if len(hit) > 1:
                raise BReject("two shown options meet")
            return hit[0] if hit else NONE
        raise BReject(op)

    # ------------------------------------------------------------------------------------------------ log
    def _lines_sql(self):
        if self.alt and self.alt[0] == "E34":
            cols = ", ".join(_q(c["name"]) for c in next(t for t in self.P["btables"] if t["role"] == "log")["cols"])
            return f"(SELECT MIN(_pos) AS _pos, 1 AS _listed, {cols}, MIN(_lvl) AS _lvl FROM log GROUP BY {cols})"
        return "log"

    def _log(self, q, shown, drop):
        op = q["op"]
        db = self.db
        L = self._lines_sql()
        alt = self.alt or ()
        if op in ("count_lines", "exists_lines", "first", "last"):
            s, a = self.sql(q["f"], "log", "l")
            if op == "count_lines":
                return db.execute(f"SELECT COUNT(*) FROM {L} l WHERE {s}", a).fetchone()[0]
            if op == "exists_lines":
                return db.execute(f"SELECT EXISTS (SELECT 1 FROM {L} l WHERE {s})", a).fetchone()[0] == 1
            rows = db.execute(f"SELECT l.time, l._pos FROM {L} l WHERE {s}", a).fetchall()
            if not rows:
                return NO_RECORD
            if alt and alt[0] == "E27":
                r = min(rows, key=lambda r: r[1]) if op == "first" else max(rows, key=lambda r: r[1])
                return r[0]
            return min(r[0] for r in rows) if op == "first" else max(r[0] for r in rows)
        if op == "comp_argmax":
            s, a = self.sql(q["f"], "log", "l")
            comps = [r[0] for r in db.execute("SELECT DISTINCT component FROM log")]
            cnt = {c: 0 for c in comps}
            for c, n in db.execute(f"SELECT l.component, COUNT(*) FROM {L} l WHERE {s} GROUP BY l.component", a):
                cnt[c] = n
            if all(v == 0 for v in cnt.values()):
                raise BUndefined("every component at 0")
            best = max(cnt.values())
            tied = sorted([c for c, v in cnt.items() if v == best], key=lambda c: int(c.split("-")[1]))
            if len(tied) == 1:
                return tied[0]
            if alt and alt[0] == "E7" and alt[1] in ("first", "last"):
                pos = {c: p for c, p in db.execute("SELECT component, MIN(_pos) FROM log GROUP BY component")}
                tied.sort(key=lambda c: pos[c])
                return tied[0] if alt[1] == "first" else tied[-1]
            tie = self.ctx.get("tie") or ["key"]
            if tie[0] == "option":
                return TIE
            d = tie[1][1]
            if alt and alt[0] == "E7" and alt[1] == "dir":
                d = "highest" if d == "lowest" else "lowest"
            return tied[0] if d == "lowest" else tied[-1]
        reqs = sorted({r[0] for r in db.execute("SELECT DISTINCT request FROM log WHERE request <> ''")},
                      key=lambda x: int(x.split("-")[1]))
        if op == "req_any":
            if q["req"] not in reqs:
                raise BUndefined("request")
            s, a = self.lift_sql({"k": "lift", "a": q["a"]}, "r")
            return db.execute(f"SELECT {s} FROM (SELECT ? AS request) r", a + [q["req"]]).fetchone()[0] == 1
        if alt and alt[0] == "E32" and alt[1] == "same_line":
            s, a = self._same_line(q["f"])
            meet = sorted({r[0] for r in db.execute(f"SELECT l.request FROM log l WHERE l.request <> '' AND {s}", a)})
        else:
            s, a = self.sql(q["f"], "req", "r")
            meet = [rq for rq in reqs if db.execute(f"SELECT {s} FROM (SELECT ? AS request) r",
                                                    a + [rq]).fetchone()[0] == 1]
        if op == "select":
            return frozenset(meet)
        if op == "cpick":
            hit = [x for x in shown or [] if x in meet]
            if len(hit) > 1:
                raise BReject("two shown options meet")
            return hit[0] if hit else NONE
        raise BReject(op)

    def _same_line(self, p):
        k = p["k"]
        if k in ("and", "or"):
            parts = [self._same_line(x) for x in p["args"]]
            return "(" + (" AND " if k == "and" else " OR ").join(x[0] for x in parts) + ")", [v for x in parts for v in x[1]]
        if k == "not":
            s, a = self._same_line(p["arg"])
            return f"(NOT {s})", a
        if k == "lift":
            return self.sql(p["a"], "log", "l")
        raise BReject("same_line")

    # ------------------------------------------------------------------------------------------------ pivot
    def _pivot(self, q, shown, drop):
        db = self.db
        alt = self.alt or ()
        if alt and alt[0] == "E13" and alt[1] == "with_marked":
            w = "1"
        elif alt and alt[0] == "E26" and alt[1] == "footnote_row":
            w = "entity NOT IN (SELECT entity FROM pivot WHERE marked = 1)"
        else:
            w = "marked = 0"
        op = q["op"]
        if op == "cell":
            r = db.execute(f"SELECT value FROM pivot WHERE entity = ? AND period = ? AND {w}",
                           (q["ent"], q["period"])).fetchall()
            if not r:
                raise BUndefined("marked cell")
            return Fraction(r[0][0], SCALE)
        if op == "row_total":
            v = db.execute(f"SELECT COALESCE(SUM(value), 0) FROM pivot WHERE entity = ? AND {w}", (q["ent"],)).fetchone()[0]
            return Fraction(int(v), SCALE)
        if op == "row_top":
            rows = db.execute(f"SELECT entity, value FROM pivot WHERE {w}").fetchall()
            ents = [r[0] for r in db.execute("SELECT DISTINCT entity FROM pivot")]
            tot = {e: 0 for e in ents}
            for e, v in rows:
                tot[e] += v
            dr = q["dir"] if not (alt and alt[0] == "E7" and alt[1] == "dir") else {"max": "min", "min": "max"}[q["dir"]]
            best = max(tot.values()) if dr == "max" else min(tot.values())
            tied = sorted([e for e, v in tot.items() if v == best], key=lambda x: int(x.split("-")[1]))
            if len(tied) > 1:
                tie = self.ctx.get("tie") or ["key"]
                if tie[0] == "option":
                    return TIE
            return tied[0]
        if op == "col_count":
            lit = sc(q["lit"])
            o = q["cmp"]
            return db.execute(f"SELECT COUNT(*) FROM pivot WHERE period = ? AND {w} AND value {o} ?",
                              (q["period"], lit)).fetchone()[0]
        raise BReject(op)


def half_up(v: Fraction, dp: int) -> Fraction:
    """sign x floor((2 |p| 10^n + q) / (2q)) / 10^n (integer arithmetic; T22)."""
    p, qd = v.numerator, v.denominator
    s = -1 if p < 0 else 1
    n = 10 ** dp
    return Fraction(s * ((2 * abs(p) * n + qd) // (2 * qd)), n)


def half_even(v: Fraction, dp: int) -> Fraction:
    n = 10 ** dp
    x = v * n
    fl = x.numerator // x.denominator
    rem = x - fl
    if rem > Fraction(1, 2) or (rem == Fraction(1, 2) and fl % 2 == 1):
        fl += 1
    return Fraction(fl, n)
