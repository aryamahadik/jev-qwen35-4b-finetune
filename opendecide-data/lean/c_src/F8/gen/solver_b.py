"""Solver B (G2): re-solves the PARSED structure with different paradigms (G0 spec 4). Never imports solver A,
the samplers or the renderer.

  bayes, PRED     integer population counting: N = lcm of all denominators, integer cell counts, posterior as a
                  count ratio, comparisons by integer cross-multiplication; PRED gold_probs rebuilt from the counts
  expected, DEC   integer ledger: chances and amounts scaled to one common integer unit
  points, MAT     relational: stdlib sqlite3 in memory, one query per SEM-15 stage
  rank            pairwise tournament with integer cross-multiplication; ties by the parsed ID number
  open world      two steps as the spec's z3 procedure: (1) a witness answer a1 at one allowed point; (2) a search for
                  an allowed point with another answer: analytic extremes for numeric unknowns (each unknown sits in
                  one monotone / linear term, section 2 coupling rules), backtracking over Boolean unknowns.
                  z3 is not installed in this environment (no package installs allowed); see MANIFEST problems.
"""
from __future__ import annotations

import itertools
import math
import sqlite3
from fractions import Fraction as Fr


class BUndetermined(Exception):
    pass


def _lcm(*xs):
    out = 1
    for x in xs:
        out = out * x // math.gcd(out, x)
    return out


def _q(x) -> tuple:
    x = Fr(x)
    return x.numerator, x.denominator


def lt(a: tuple, b: tuple) -> bool:            # a < b by cross-multiplication (positive denominators)
    return a[0] * b[1] < b[0] * a[1]


def eq(a: tuple, b: tuple) -> bool:
    return a[0] * b[1] == b[0] * a[1]


def cmpop(a: tuple, op: str, b: tuple) -> bool:
    if op == ">":
        return lt(b, a)
    if op == ">=":
        return not lt(a, b)
    if op == "<":
        return lt(a, b)
    if op == "<=":
        return not lt(b, a)
    raise ValueError(op)


# ------------------------------------------------------------------------------------------------ points: sqlite
class Rel:
    def __init__(self, ents: list):
        self.db = sqlite3.connect(":memory:")
        c = self.db
        c.execute("create table fb (e text, f text, v integer)")
        c.execute("create table fc (e text, n text, v text)")
        c.execute("create table fa (e text, n text, num integer, den integer)")
        for e in ents:
            p = e.get("pts") or {}
            for f, v in (p.get("b") or {}).items():
                if v is None:
                    continue
                c.execute("insert into fb values (?,?,?)", (e["id"], f, 1 if v else 0))
            for n, v in (p.get("c") or {}).items():
                c.execute("insert into fc values (?,?,?)", (e["id"], n, v))
            for n, v in (p.get("a") or {}).items():
                if v is None:
                    continue
                q = _q(v)
                c.execute("insert into fa values (?,?,?,?)", (e["id"], n, q[0], q[1]))

    def part(self, eid: str, p: dict, qv) -> bool:
        c = self.db
        if p["t"] == "bool":
            r = c.execute("select count(*) from fb where e=? and f=? and v=1", (eid, p["f"])).fetchone()[0]
            return r > 0
        if p["t"] == "cat":
            r = c.execute("select count(*) from fc where e=? and n=? and v=?", (eid, p["name"], p["v"])).fetchone()[0]
            return r > 0
        if p["t"] == "amt":
            num, den = _q(p["v"])
            sqlop = {">": ">", ">=": ">=", "<": "<", "<=": "<="}[p["op"]]
            r = c.execute(f"select count(*) from fa where e=? and n=? and num*? {sqlop} ?*den",
                          (eid, p["name"], den, num)).fetchone()[0]
            row = c.execute("select count(*) from fa where e=? and n=?", (eid, p["name"])).fetchone()[0]
            if row == 0:
                raise BUndetermined("amount unknown")
            return r > 0
        if p["t"] == "q":
            return cmpop(qv(p["q"]), p["op"], _q(p["v"]))
        raise ValueError(p["t"])

    def cond(self, eid, cond, qv) -> bool:
        vals = [self.part(eid, p, qv) for p in cond["parts"]]
        n = sum(vals)
        if cond["conn"] == "and":
            return n == len(vals)
        if cond["conn"] == "or":
            return n >= 1
        if cond["conn"] == "xor1":
            return n == 1
        raise ValueError(cond["conn"])

    def score(self, eid, sc, qv) -> int:
        c = self.db
        c.execute("drop table if exists ln")
        c.execute("create table ln (i integer, pts integer, applies integer)")
        for i, l in enumerate(sc["lines"]):
            a = self.cond(eid, l["cond"], qv)
            if a and l.get("unless") and self.cond(eid, l["unless"], qv):
                a = False
            c.execute("insert into ln values (?,?,?)", (i, l["pts"], 1 if a else 0))
        tot = c.execute("select coalesce(sum(pts),0) from ln where applies=1").fetchone()[0]
        return c.execute("select min(?, max(?, ?))", (sc["M"], sc["F"], tot)).fetchone()[0]

    def tier(self, eid, R, qv) -> int:
        c = self.db
        s = self.score(eid, R["scorecard"], qv)
        c.execute("drop table if exists cut")
        c.execute("create table cut (k integer, c integer)")
        for k, cc in enumerate(R["cuts"]):
            c.execute("insert into cut values (?,?)", (k + 1, cc))
        t = c.execute("select count(*) from cut where ? >= c", (s,)).fetchone()[0]
        limits = {int(k): v for k, v in R.get("only_if", {}).items()}
        c.execute("drop table if exists lim")
        c.execute("create table lim (t integer, ok integer)")
        for k in range(len(R["tiers"])):
            ok = 1 if (k not in limits or self.cond(eid, limits[k], qv)) else 0
            c.execute("insert into lim values (?,?)", (k, ok))
        ok_here = c.execute("select ok from lim where t=?", (t,)).fetchone()[0]
        if not ok_here:
            t = c.execute("select coalesce(max(t), 0) from lim where t < ? and ok = 1", (t,)).fetchone()[0]
        c.execute("drop table if exists ov")
        c.execute("create table ov (t integer)")
        for o in R.get("overrides", []):
            if self.cond(eid, o["cond"], qv):
                c.execute("insert into ov values (?)", (o["tier"],))
        r = c.execute("select max(t) from ov").fetchone()[0]
        return t if r is None else r


# ------------------------------------------------------------------------------------------------ bayes: counting
def counts_given_evidence(bay: dict) -> list:
    """Integer counts of each class among the cases that match the stated evidence (common population N)."""
    k = len(bay["hyps"])
    if bay["form"] == "counts":
        s = bay["signs"][0]
        col = 0 if bay["sig"][s] else 1
        return [bay["cnt"][s][j][col] for j in range(k)]
    if bay["form"] == "nE":
        s = bay["signs"][0]
        return [int(x) for x in bay["ne"][s]]
    if bay["form"] == "joint":
        s = bay["signs"][0]
        J = bay["joint"][s]
        if any(x is None for x in J):
            raise BUndetermined("joint unknown")
        N = _lcm(*[Fr(x).denominator for x in J])
        return [int(Fr(x) * N) for x in J]
    terms = []
    for j in range(k):
        t = Fr(bay["base"][j])
        for s in bay["signs"]:
            L = bay["lik"][s][j]
            if L is None:
                raise BUndetermined("lik unknown")
            t *= Fr(L) if bay["sig"][s] else 1 - Fr(L)
        terms.append(t)
    N = _lcm(*[t.denominator for t in terms])
    return [int(t * N) for t in terms]


def posterior_q(bay: dict, h: int) -> tuple:
    cnt = counts_given_evidence(bay)
    tot = sum(cnt)
    if tot == 0:
        raise BUndetermined("no matching cases")
    return cnt[h], tot


# ------------------------------------------------------------------------------------------------ expected: ledger
def ledger(e: dict, kind: str) -> tuple:
    outs = e.get("outs") or []
    for o in outs:
        if o["p"] is None or o["a"] is None:
            raise BUndetermined("outcome unknown")
    dens = [Fr(o["p"]).denominator for o in outs] + [Fr(o["a"]).denominator for o in outs]
    if kind == "tec":
        if e.get("cost") is None:
            raise BUndetermined("cost")
        dens.append(Fr(e["cost"]).denominator)
    D = _lcm(*dens) if dens else 1
    D2 = D * D
    units = 0
    for o in outs:
        units += int(Fr(o["p"]) * D * Fr(o["a"]) * D)
    if kind == "tec":
        units += int(Fr(e["cost"]) * D2)
    return units, D2


# ------------------------------------------------------------------------------------------------ quantities
class SolverB:
    def __init__(self, S: dict):
        self.S = S
        self.R = S["rules"]
        self.rel = Rel(S["ents"]) if any("pts" in e for e in S["ents"]) else None

    def qval(self, e: dict, q: dict) -> tuple:
        k = q["k"]
        if k == "risk":
            k = q["def"]
        if k == "score":
            return self.rel.score(e["id"], self.R["scorecard"], lambda qq: self.qval(e, qq)), 1
        if k == "post":
            return posterior_q(e["bay"], q["h"])
        if k in ("el", "ev"):
            return ledger(e, "el")
        if k == "tec":
            return ledger(e, "tec")
        if k == "en":
            n = e["en"]
            if n["p"] is None:
                raise BUndetermined("en")
            p = Fr(n["p"])
            return n["n"] * p.numerator, p.denominator
        if k == "chance":
            if e.get("ch") is not None:
                if e["ch"]["p"] is None:
                    raise BUndetermined("chance")
                return _q(e["ch"]["p"])
            tot = Fr(0)
            for o in e["outs"]:
                if o["p"] is None:
                    raise BUndetermined("chance")
                tot += Fr(o["p"])
            return _q(tot)
        raise ValueError(k)

    def tournament(self, vals: list, high: bool) -> int:
        n = len(vals)
        ids = [int(e["id"].rsplit("-", 1)[-1]) for e in self.S["ents"]]
        for i in range(n):
            ok = True
            for j in range(n):
                if i == j:
                    continue
                better = lt(vals[j], vals[i]) if high else lt(vals[i], vals[j])
                tie = eq(vals[i], vals[j])
                if not (better or (tie and ids[i] < ids[j])):
                    ok = False
                    break
            if ok:
                return i
        raise BUndetermined("no tournament winner")

    def order(self, vals: list) -> tuple:
        n = len(vals)
        wins = [sum(1 for j in range(n) if j != i and lt(vals[j], vals[i])) for i in range(n)]
        if len(set(wins)) != n:
            raise BUndetermined("tie in an ordering")
        return tuple(sorted(range(n), key=lambda i: -wins[i]))

    def mat(self, e: dict) -> int:
        m = self.R["mat"]
        mm = e["mat"]
        db = sqlite3.connect(":memory:")
        db.execute("create table lv (axis text, k integer, num integer, den integer)")
        for k, x in enumerate(m["lik_edges"]):
            db.execute("insert into lv values ('L',?,?,?)", (k + 1, *_q(x)))
        for k, x in enumerate(m["imp_edges"]):
            db.execute("insert into lv values ('I',?,?,?)", (k + 1, *_q(x)))
        lik = _q(mm["lik"])
        imp = _q(Fr(mm["amt"]) if m["impact"] == "loss" else Fr(mm["lik"]) * Fr(mm["amt"]))
        if m["lik_conv"] == "lo":
            li = db.execute("select count(*) from lv where axis='L' and ?*den >= num*?", (lik[0], lik[1])).fetchone()[0]
        else:
            li = db.execute("select count(*) from lv where axis='L' and ?*den > num*?", (lik[0], lik[1])).fetchone()[0]
        ii = db.execute("select count(*) from lv where axis='I' and ?*den >= num*?", (imp[0], imp[1])).fetchone()[0]
        return m["grid"][li][ii]

    def inv_meets(self, e: dict) -> bool:
        r = self.R["inv"]
        if r["kind"] == "q":
            return cmpop(self.qval(e, r["q"]), r["op"], _q(r["v"]))
        return self.rel.cond(e["id"], self.R["arules"][r["action"]], lambda qq: self.qval(e, qq))

    # -------------------------------------------------------------------------------------------- closed answer
    def closed(self):
        S = self.S
        f = S["form"]
        ents = S["ents"]
        if f == "yn_thr":
            e = ents[S["case"]]
            a = cmpop(self.qval(e, S["q"]), S["thr"]["op"], _q(S["thr"]["T"]))
            return a if S["thr"]["neg"] % 2 == 0 else (not a)
        if f == "yn_act":
            e = ents[S["case"]]
            a = self.rel.cond(e["id"], self.R["arules"][S["act"]["action"]], lambda qq: self.qval(e, qq))
            return a if S["act"]["neg"] % 2 == 0 else (not a)
        if f == "bin":
            num, den = self.qval(ents[S["case"]], S["q"])
            c = 0
            for edge in self.R["bins"]:
                en, ed = _q(edge)
                above = num * ed >= en * den if self.R["bin_conv"] == "lo" else num * ed > en * den
                c += 1 if above else 0
            return c
        if f == "tier":
            e = ents[S["case"]]
            return self.rel.tier(e["id"], self.R, lambda qq: self.qval(e, qq))
        if f == "mat":
            return self.mat(ents[S["case"]])
        if f == "pred":
            cnt = counts_given_evidence(ents[S["case"]]["bay"])
            best = max(cnt)
            if cnt.count(best) > 1:
                raise BUndetermined("pred tie")
            return cnt.index(best)
        if f in ("rank_top", "dec"):
            vals = [self.qval(e, S["q"]) for e in ents]
            return self.tournament(vals, high=(f == "rank_top" and S["hl"] == "high"))
        if f == "rank_order":
            o = self.order([self.qval(e, S["q"]) for e in ents])
            sub = S.get("subset")
            if sub and o.index(sub["X"]) not in sub["pos"]:
                return "NOTA"
            return o
        if f == "inv":
            meet = [i for i, e in enumerate(ents) if self.inv_meets(e)]
            if len(meet) > 1:
                raise BUndetermined("two cases meet")
            return meet[0] if meet else "NOTA"
        raise ValueError(f)

    def gold_probs(self) -> list:
        cnt = counts_given_evidence(self.S["ents"][self.S["case"]]["bay"])
        tot = sum(cnt)
        return [Fr(c, tot) for c in cnt]


# ------------------------------------------------------------------------------------------------ open world
def _unknowns(S: dict) -> list:
    out = []
    for i, e in enumerate(S["ents"]):
        p = e.get("pts")
        if p:
            for f, v in p["b"].items():
                if v is None:
                    out.append(("b", i, f, None))
            for a, v in p["a"].items():
                if v is None:
                    out.append(("a", i, a, tuple(p["arng"][a])))
        b = e.get("bay")
        if b and b["form"] == "rates":
            for s, vec in b["lik"].items():
                for j, v in enumerate(vec):
                    if v is None:
                        out.append(("lik", i, (s, j), tuple(b["rng"][f"{s}|{j}"])))
        for k, o in enumerate(e.get("outs") or []):
            if o["p"] is None:
                out.append(("op", i, k, tuple(o["prng"])))
            if o["a"] is None:
                out.append(("oa", i, k, tuple(o["arng"])))
        if e.get("ch") is not None and e["ch"]["p"] is None:
            out.append(("ch", i, None, tuple(e["ch"]["rng"])))
    return out


def _set(S, u, val):
    import copy
    T = copy.deepcopy(S)
    kind, i, key, _ = u
    e = T["ents"][i]
    if kind == "b":
        e["pts"]["b"][key] = val
    elif kind == "a":
        e["pts"]["a"][key] = val
    elif kind == "lik":
        e["bay"]["lik"][key[0]][key[1]] = val
    elif kind == "op":
        e["outs"][key]["p"] = val
    elif kind == "oa":
        e["outs"][key]["a"] = val
    elif kind == "ch":
        e["ch"]["p"] = val
    return T


def _assign_all(S, us, vals):
    T = S
    for u, v in zip(us, vals):
        T = _set(T, u, v)
    return T


def _answer(S):
    try:
        return SolverB(S).closed()
    except BUndetermined:
        return "UNDEF"


def _points(us):
    """Candidate allowed points for the counter-example search: Booleans both ways (backtracking order) and the two
    analytic extremes of each numeric unknown (every numeric unknown enters one monotone or linear term)."""
    doms = []
    for u in us:
        if u[0] == "b":
            doms.append([False, True])
        else:
            doms.append([Fr(u[3][0]), Fr(u[3][1])])
    return doms


def solve(S: dict) -> dict:
    us = _unknowns(S)
    if not us:
        sb = SolverB(S)
        a = sb.closed()
        out = {"ans": a, "det": True}
        if S["form"] == "pred":
            out["gold_probs"] = sb.gold_probs()
        return out
    doms = _points(us)
    f = S["form"]
    # step 1: a witness answer at one allowed point (lower ends, Booleans false)
    witness = tuple(d[0] for d in doms)
    if f == "inv":
        return _inv_open(S, us, doms)
    if f == "bin":
        return _bin_open(S, us, doms)
    a1 = _answer(_assign_all(S, us, witness))
    # step 2: is there an allowed point with another answer? (backtracking over the candidate points)
    def search(k, vals):
        if k == len(us):
            a = _answer(_assign_all(S, us, vals))
            return a != a1
        for v in doms[k]:
            if search(k + 1, vals + (v,)):
                return True
        return False
    if a1 != "UNDEF" and not search(0, ()):
        return {"ans": a1, "det": True}
    return {"ans": "CBD", "det": False}


def _bin_open(S, us, doms):
    sb_vals = []
    for vals in itertools.product(*doms):
        T = _assign_all(S, us, vals)
        sb_vals.append(SolverB(T).closed())
    if len(set(sb_vals)) == 1:
        return {"ans": sb_vals[0], "det": True}
    return {"ans": "CBD", "det": False}


def _inv_open(S, us, doms):
    n = len(S["ents"])
    status = []
    for i in range(n):
        own = [k for k, u in enumerate(us) if u[1] == i]
        seen = set()
        for vals in itertools.product(*[doms[k] for k in own]):
            T = S
            for k, v in zip(own, vals):
                T = _set(T, us[k], v)
            try:
                seen.add(SolverB(T).inv_meets(T["ents"][i]))
            except BUndetermined:
                seen.add("U")
        status.append("meets" if seen == {True} else ("fails" if seen == {False} else "und"))
    sure = [i for i, s in enumerate(status) if s == "meets"]
    und = [i for i, s in enumerate(status) if s == "und"]
    if len(sure) == 1 and not und:
        return {"ans": sure[0], "det": True, "status": status}
    if not sure and und:
        return {"ans": "CBD", "det": False, "status": status}
    if not sure and not und:
        return {"ans": "NOTA", "det": True, "status": status}
    return {"ans": ("BADSHAPE",), "det": False, "status": status}
