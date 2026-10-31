"""Cross-checks of solver A against deliberately different test oracles (not solver B; oracles live only in this file)."""
import itertools
import sqlite3
from decimal import Decimal
from fractions import Fraction

import pytest

import arith as A
import causal as C
import gen_common as g
import logic as L
import tables as TB
import temporal as T


def rng(*p):
    return g.make_rng("solver-test", *p)


# ------------------------------------------------------------------ ARITH: exactness
def frac_eval(spec):
    env = {b["id"]: (Fraction(b["value"]), b["unit"]) for b in spec["base"]}
    scale = A.UNIT_SCALE
    for st in spec["steps"]:
        vs = [env[a][0] for a in st["args"]]
        us = [env[a][1] for a in st["args"]]
        op, p = st["op"], st["param"]
        u = us[0]
        if op == "add":
            v = sum(vs)
        elif op == "sub":
            v = vs[0] - vs[1]
        elif op == "min":
            v = min(vs)
        elif op == "max":
            v = max(vs)
        elif op == "mul":
            v = vs[0] * p
        elif op == "div":
            v = vs[0] / p
        elif op == "pct":
            v = vs[0] * p / 100
        elif op == "split":
            v = vs[0] * p["r"][p["which"]] / (p["r"][0] + p["r"][1])
        elif op == "conv":
            v = vs[0] * Fraction(scale[u]) / Fraction(scale[p])
            u = p
        else:
            import math
            x = vs[0]
            if p == "nearest_int":
                v = Fraction(math.floor(x + Fraction(1, 2)))
            elif p == "one_dp":
                v = Fraction(math.floor(x * 10 + Fraction(1, 2)), 10)
            elif p == "floor_int":
                v = Fraction(math.floor(x))
            else:
                v = Fraction(math.ceil(x))
        env[st["id"]] = (v, u)
    return env[spec["final"]]


@pytest.mark.parametrize("bin_name", ["easy", "mid", "hard"])
def test_arith_decimal_matches_fractions_and_is_exact(bin_name):
    n = 0
    for i in range(60):
        r = rng("ar", bin_name, i)
        spec = A.make_spec("AR-F1", r, g.RowNamer("a%d" % i), bin_name)
        if spec is None:
            continue
        v, u = A.solve_value(spec)
        fv, fu = frac_eval(spec)
        assert Fraction(v) == fv and u == fu
        assert g.is_2dp(v) and v > 0
        env = A.evaluate(spec)
        assert all(g.is_2dp(x[0]) and x[0] >= 0 for x in env.values())
        n += 1
    assert n >= 40


def test_arith_error_models_never_equal_correct_and_are_nonnegative_2dp():
    bal = g.Balancer("t")
    for i in range(80):
        r = rng("arerr", i)
        spec = A.make_spec("AR-F1", r, g.RowNamer("e%d" % i), ["easy", "mid", "hard"][i % 3])
        correct = A.solve_value(spec)[0]
        ev = A.error_values(spec, r)
        for t, vals in ev.items():
            for v in vals:
                assert v != correct and v >= 0 and g.is_2dp(v)


def test_arith_f3_first_wrong_line_is_unique_and_matches_injection():
    bal = g.Balancer("t")
    seen = 0
    for i in range(80):
        r = rng("f3", i)
        spec = A.make_spec("AR-F3", r, g.RowNamer("f%d" % i), ["easy", "mid", "hard"][i % 3])
        f3 = A.make_f3(spec, r)
        if f3 is None:
            continue
        assert A.first_wrong_line(spec, f3["lines"]) == f3["j"] + 1
        # all lines before the fault are right; all lines after follow through from the faulty value
        truth = A.f3_correct_values(spec)
        assert all(f3["lines"][k]["value"] == truth[k] for k in range(f3["j"]))
        seen += 1
    assert seen >= 60


def test_arith_f2_threshold_flips_under_the_chosen_error_model():
    bal = g.Balancer("t")
    ok = 0
    for i in range(80):
        r = rng("f2", i)
        spec = A.make_spec("AR-F2", r, g.RowNamer("g%d" % i), ["easy", "mid", "hard"][i % 3])
        want = bool(i % 2)
        res = A.make_threshold(spec, want, r, bal, "x")
        if res is None:
            continue
        cmp, thr, t = res
        spec["f2"] = {"cmp": cmp, "thr": g.fmt_num(thr), "trap_type": t}
        assert A.f2_answer(spec) == want
        ok += 1
    assert ok >= 60


# ------------------------------------------------------------------ LOGIC: BCP versus exhaustive enumeration
def enumerate_class(spec, lit):
    atoms = L.all_atoms(spec)
    idx = {a: i for i, a in enumerate(atoms)}
    clauses = L.ground_clauses(spec)
    facts = L.fact_lits(spec)
    a0, s0 = lit
    ent = con = True
    n_models = 0
    for bits in itertools.product([False, True], repeat=len(atoms)):
        if any(bits[idx[a]] != s for a, s in facts):
            continue
        if any(all(bits[idx[b]] for b in body) and bits[idx[h[0]]] != h[1] for body, h in clauses):
            continue
        n_models += 1
        val = bits[idx[a0]] == s0
        ent &= val
        con &= (not val)
    return n_models, ("Entailed" if ent else "Contradicted" if con else "Undetermined")


def test_logic_bcp_equals_exhaustive_enumeration():
    checked = 0
    for i in range(40):
        r = rng("lg", i)
        spec = L.make_kb(r, g.RowNamer("l%d" % i), "LG-L1", ["easy", "mid", "hard"][i % 3])
        if spec is None:
            continue
        atoms = L.all_atoms(spec)
        if len(atoms) > 13:
            continue
        for lit in [(a, s) for a in atoms if a[0] == "P" for s in (True, False)][:10]:
            n, cls = enumerate_class(spec, lit)
            assert n > 0
            assert L.classify(spec, lit) == cls, (spec, lit)
            checked += 1
    assert checked >= 100


def test_logic_every_ground_clause_is_horn():
    for i in range(60):
        spec = L.make_kb(rng("horn", i), g.RowNamer("h%d" % i), "LG-L2", ["easy", "mid", "hard"][i % 3])
        if spec is None:
            continue
        for body, head in L.ground_clauses(spec):
            positive = (1 if head[1] else 0)       # bodies are positive atoms, so they add only negative literals
            assert positive <= 1


def test_logic_atom_limit_and_consistency():
    for i in range(60):
        spec = L.make_kb(rng("lim", i), g.RowNamer("m%d" % i), "LG-L1")
        if spec:
            assert len(L.all_atoms(spec)) <= L.MAX_ATOMS and L.consistent(spec)


def test_l3_backtracking_equals_permutation_brute_force():
    for i in range(30):
        r = rng("l3", i)
        n = r.choice([4, 5])
        target = list(range(n))
        r.shuffle(target)
        cons = []
        for _ in range(60):
            c = L._rand_constraint(r, n, target)
            if c and c not in cons and L.holds(c, tuple(target)):
                cons.append(c)
            if len(cons) >= 5:
                break
        brute = {p for p in itertools.permutations(range(n)) if all(L.holds(c, p) for c in cons)}
        assert set(L.solve_arrangements(n, cons)) == brute


def test_l2_exactly_one_entailed_option_and_l4_binary():
    bal = g.Balancer("t")
    for i in range(30):
        it = L.make_l2(rng("l2", i), g.RowNamer("p%d" % i), ["easy", "mid", "hard"][i % 3], bal, "s")
        assert it and len(L.l2_entailed_options(it["spec"])) == 1
        it4 = L.make_l4(rng("l4", i), g.RowNamer("q%d" % i), "mid", i % 2 == 0, bal, "s")
        assert it4 and (L.solve_l4(it4["spec"]) == "yes") == (i % 2 == 0)


# ------------------------------------------------------------------ CAUSAL
def moral_dsep(parents, n, x, y, Z):
    Z = set(Z)
    keep = {x, y} | Z
    for v in list(keep):
        keep |= C.ancestors(parents, v)
    adj = {v: set() for v in keep}
    for v in keep:
        ps = [p for p in parents[v] if p in keep]
        for p in ps:
            adj[v].add(p)
            adj[p].add(v)
        for a, b in itertools.combinations(ps, 2):
            adj[a].add(b)
            adj[b].add(a)
    seen, stack = {x}, [x]
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in Z and w not in seen:
                seen.add(w)
                stack.append(w)
    return y not in seen


def test_dsep_ball_passing_equals_moralised_ancestral_graph():
    for i in range(60):
        r = rng("ds", i)
        n = r.choice([4, 5, 6, 7])
        parents = C.random_dag(r, n, 0.4)
        x, y = r.sample(range(n), 2)
        others = [j for j in range(n) if j not in (x, y)]
        for k in range(0, min(3, len(others)) + 1):
            for Z in itertools.combinations(others, k):
                assert C.dsep_ballpass(parents, n, x, y, Z) == moral_dsep(parents, n, x, y, Z)


def test_backdoor_rule_equals_dsep_in_graph_without_outgoing_edges_of_t():
    for i in range(40):
        r = rng("bd", i)
        n = r.choice([5, 6])
        parents = C.random_dag(r, n, 0.4)
        t, o = r.sample(range(n), 2)
        spec = {"n": n, "parents": parents, "t": t, "o": o}
        cut = {j: [p for p in ps if p != t] for j, ps in parents.items()}
        others = [j for j in range(n) if j not in (t, o)]
        for k in range(len(others) + 1):
            for Z in itertools.combinations(others, k):
                desc_t = C.descendants(parents, n, t)
                oracle = (not (set(Z) & desc_t)) and moral_dsep(cut, n, t, o, Z)
                assert C.backdoor_valid(spec, Z) == oracle


def test_scm_abduction_reproduces_observation_and_counterfactual():
    for i in range(40):
        r = rng("scm", i)
        spec = C.make_scm(r, g.RowNamer("s%d" % i), "CA-C2", ["easy", "mid", "hard"][i % 3])
        if spec is None:
            continue
        s = C.norm(spec)
        u = C.abduct(s)
        tmp = dict(s)
        tmp["roots"] = {j: s["obs"][j] for j in range(s["n"]) if not s["parents"][j]}
        assert C.eval_scm(tmp, u=u) == s["obs"]
        # no-intervention counterfactual equals the record
        same = {s["do"]["var"]: s["obs"][s["do"]["var"]]}
        assert C.eval_scm(tmp, do=same, u=u) == s["obs"]
        assert C.solve(spec) != s["obs"][s["target"]]


def test_c3_roles_exclusive_and_flaw_outputs_differ():
    bal = g.Balancer("t")
    for i in range(40):
        it = C.make_c3(rng("c3", i), g.RowNamer("c%d" % i), ["easy", "mid", "hard"][i % 3], C.ROLES[i % 4], bal, "s")
        assert it and C.solve_c3(it["spec"]) == C.ROLES[i % 4]
        assert len({o["text"] for o in it["options"]}) == 4


# ------------------------------------------------------------------ TEMPORAL
def ordinal_add_months(y, m, d, n, rule):
    t = y * 12 + (m - 1) + n
    y2, m2 = divmod(t, 12)
    m2 += 1
    leap = (y2 % 4 == 0 and y2 % 100 != 0) or y2 % 400 == 0
    dim = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m2 - 1]
    if d <= dim:
        return y2, m2, d, 0
    if rule == "clamp":
        return y2, m2, dim, 0
    return y2, m2, dim, d - dim


def test_t1_matches_ordinal_arithmetic_oracle():
    import datetime as dt
    bal = g.Balancer("t")
    n = 0
    for i in range(80):
        it = T.make_t1(rng("t1", i), g.RowNamer("t%d" % i), ["easy", "mid", "hard"][i % 3], bal, "s")
        if not it:
            continue
        spec = it["spec"]
        cur = dt.date.fromisoformat(spec["start"]).toordinal()
        for op in spec["ops"]:
            d0 = dt.date.fromordinal(cur)
            if op["unit"] == "day":
                cur += op["n"]
            elif op["unit"] == "week":
                cur += 7 * op["n"]
            elif op["unit"] == "month":
                y, m, d, extra = ordinal_add_months(d0.year, d0.month, d0.day, op["n"], spec["month_rule"])
                cur = dt.date(y, m, d).toordinal() + extra
            else:
                hol = {dt.date.fromisoformat(h).toordinal() for h in spec["holidays"]}
                k = 0
                while k < op["n"]:
                    cur += 1
                    wd = (cur + 6) % 7          # date.fromordinal(1) is a Monday
                    if wd not in spec["weekend"] and cur not in hol:
                        k += 1
        assert dt.date.fromordinal(cur).isoformat() == T.solve_t1(spec)
        n += 1
    assert n >= 60


def test_t2_matches_integer_minute_oracle():
    import datetime as dt
    bal = g.Balancer("t")
    for i in range(60):
        it = T.make_t2(rng("t2", i), g.RowNamer("u%d" % i), ["easy", "mid", "hard"][i % 3], bal, "s")
        if not it:
            continue
        s = it["spec"]
        def mins(ts):
            h, m = ts["hm"].split(":")
            return dt.date.fromisoformat(ts["date"]).toordinal() * 1440 + int(h) * 60 + int(m) - ts["off"]
        assert T.duration_minutes(s) == mins(s["t2"]) - mins(s["t1"]) > 0


def test_t3_relation_on_integer_endpoints():
    bal = g.Balancer("t")
    for i in range(60):
        want = T.REL[i % 4]
        it = T.make_t3(rng("t3", i), g.RowNamer("v%d" % i), "mid", want, bal, "s")
        assert it and T.solve_t3(it["spec"]) == want


def test_t4_plan_critical_path_equals_event_simulation():
    bal = g.Balancer("t")
    for i in range(40):
        it = T.make_t4(rng("t4", i), g.RowNamer("w%d" % i), "mid", i % 2 == 0, bal, "s", variant="plan")
        if not it:
            continue
        tasks = it["spec"]["tasks"]
        t = 0
        finish = {}
        pending = list(tasks)
        while pending:                       # step through time in 5 minute ticks
            t += 5
            for task in list(pending):
                if all(a in finish for a in task["after"]):
                    start = max([finish[a] for a in task["after"]] or [0])
                    if t >= start + task["dur"]:
                        finish[task["name"]] = start + task["dur"]
                        pending.remove(task)
        sim = max(finish.values())
        assert sim == T.critical_path(tasks) or abs(sim - T.critical_path(tasks)) < 5


# ------------------------------------------------------------------ TABLE: evaluator versus sqlite
def sql_for(tables, q):
    def cond(c):
        t = tables[c["t"]]
        ty = t["columns"][TB.col_index(t, c["col"])]["type"]
        val = c["val"] if ty in ("cat", "name", "date") else c["val"]
        lit = "'%s'" % val if ty in ("cat", "name", "date") else val
        return '%s."%s" %s %s' % ("t%d" % c["t"], c["col"], c["op"], lit)
    where = (" %s " % q.get("conj", "and").upper()).join(cond(c) for c in q["where"]) or "1=1"
    frm = "t0"
    if q.get("join"):
        frm = 't0 JOIN t1 ON t0."%s" = t1."%s"' % (q["join"]["left_key"], q["join"]["right_key"])
    a = q["agg"]
    sel = "COUNT(*)" if a["fn"] == "count" else "%s(t%d.\"%s\")" % ({"sum": "SUM", "min": "MIN", "max": "MAX", "avg": "AVG"}[a["fn"]], a["t"], a["col"])
    return "SELECT %s FROM %s WHERE %s" % (sel, frm, where)


def load_db(tables):
    db = sqlite3.connect(":memory:")
    for i, t in enumerate(tables):
        cols = ", ".join('"%s" %s' % (c["name"], {"int": "INTEGER", "dec": "NUMERIC", "cat": "TEXT", "name": "TEXT", "date": "TEXT"}[c["type"]]) for c in t["columns"])
        db.execute("CREATE TABLE t%d (%s)" % (i, cols))
        db.executemany("INSERT INTO t%d VALUES (%s)" % (i, ",".join("?" * len(t["columns"]))), [[(int(v) if c["type"] == "int" else (float(v) if c["type"] == "dec" else v)) for c, v in zip(t["columns"], row)] for row in t["rows"]])
    return db


def test_table_evaluator_matches_sqlite_for_b1_and_b3():
    bal = g.Balancer("t")
    n = 0
    for i in range(40):
        for form, mk in (("b1", lambda r, nm, b: TB.make_b1(r, nm, b, bal, "s", "TBL-CSV")), ("b3", lambda r, nm, b: TB.make_b3(r, nm, b, bal, "s", "TBL-CSV"))):
            it = mk(rng(form, i), g.RowNamer("x%s%d" % (form, i)), ["easy", "mid", "hard"][i % 3] if form == "b1" else "mid")
            if not it:
                continue
            tables, q = it["spec"]["tables"], it["spec"]["query"]
            db = load_db(tables)
            row = db.execute(sql_for(tables, q)).fetchone()[0]
            mine = TB.run_scalar(tables, q)
            if q["agg"]["fn"] == "avg":
                assert abs(float(mine) - float(row)) < 0.006
            else:
                assert abs(float(mine) - float(row)) < 1e-6
            n += 1
    assert n >= 40


def test_table_carriers_are_unambiguous_for_stdlib_parsers():
    import csv
    import io
    import json
    for i in range(20):
        t = TB.make_table(rng("car", i), g.RowNamer("k%d" % i), "a", 8, 5)
        if not TB.carrier_safe(t):
            continue
        names = [c["name"] for c in t["columns"]]
        rows = [[TB.cell_text(c["type"], v) for c, v in zip(t["columns"], row)] for row in t["rows"]]
        assert list(csv.reader(io.StringIO(TB.serialize(t, "TBL-CSV")))) == [names] + rows
        assert list(csv.reader(io.StringIO(TB.serialize(t, "TBL-TSV")), delimiter="\t")) == [names] + rows
        assert [[x.strip() for x in l.split("|")] for l in TB.serialize(t, "TBL-PIPE").split("\n")] == [names] + rows
        js = json.loads(TB.serialize(t, "TBL-JSON"))
        assert [list(o) for o in js] == [names] * len(rows)
        assert [[str(o[k]) if t["columns"][j]["type"] != "dec" else o[k] for j, k in enumerate(o)] for o in js] == rows
        kv = TB.serialize(t, "TBL-KV").split("\n")
        assert [[p.split("=")[1] for p in l.split(": ", 1)[1].split("; ")] for l in kv] == rows


def test_carrier_safe_rejects_delimiters():
    t = {"label": "x", "columns": [{"name": "a", "type": "cat"}, {"name": "b", "type": "int"}], "rows": [["x|y", 1]]}
    assert not TB.carrier_safe(t)
    t["rows"] = [[" lead", 1]]
    assert not TB.carrier_safe(t)
    t["rows"] = [["ok", 1]]
    assert TB.carrier_safe(t)


def test_b2_has_no_tie_for_first_place():
    bal = g.Balancer("t")
    for i in range(40):
        it = TB.make_b2(rng("b2", i), g.RowNamer("y%d" % i), ["easy", "mid", "hard"][i % 3], bal, "s", "TBL-PIPE")
        if not it:
            continue
        q = it["spec"]["query"]
        gr = TB.run_groups(it["spec"]["tables"], q)
        vals = sorted(gr.values(), reverse=q.get("highest", True))
        assert vals[0] != vals[1]
