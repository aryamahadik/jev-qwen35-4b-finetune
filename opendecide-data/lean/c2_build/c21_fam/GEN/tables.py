"""GEN / TABLE sub-block: generated tables, query AST, pure-Python evaluator (SOLVER A), serialisation into the five table
carriers, near-miss distractors from flawed readings of the query.
Solver B (AST -> SQL on in-memory stdlib SQLite, plus a table-carrier parser) is NOT here.

Forms: TB-B1 filter and aggregate, TB-B2 which entry ranks first, TB-B3 two-table join aggregate, TB-B4 is the claim true.
"""
import datetime as dt
import json
from decimal import ROUND_HALF_UP, Decimal

from gen_common import D2, Doc, dec, end_block, fmt_num, is_2dp, pick_options_ranked, dp_class

OP_TEXT_NUM = {">=": "is at least", ">": "is more than", "<=": "is at most", "<": "is less than", "=": "is"}
OP_TEXT_DATE = {">=": "is on or after", ">": "is after", "<=": "is on or before", "<": "is before", "=": "is"}
AGG_WORD = {"sum": "total", "min": "minimum", "max": "maximum", "avg": "average", "count": "number of rows"}
NUMERIC = ("int", "dec")
FLIP_OP = {">=": ">", ">": ">=", "<=": "<", "<": "<="}


# ------------------------------------------------------------------------------------------------
# Tables
# ------------------------------------------------------------------------------------------------
def _cell_int(rng):
    return rng.randint(1, 500)


def _cell_dec(rng):
    return str((Decimal(rng.randint(100, 50000)) / Decimal(100)).quantize(D2))


def _cell_date(rng):
    return (dt.date(2026, 1, 1) + dt.timedelta(days=rng.randrange(0, 360))).isoformat()


def make_table(rng, namer, key, n_rows, n_cols, n_cats=None, with_dates=False, forced_types=None):
    """Columns: name (unique), >=1 cat, >=1 numeric, then extras. Returns a table dict."""
    types = ["name", "cat"]
    pool = ["int", "dec", "int", "dec", "cat", "date" if with_dates else "int"]
    while len(types) < n_cols:
        types.append(rng.choice(pool))
    if not any(t in NUMERIC for t in types):
        types[-1] = "int"
    if forced_types:
        types = list(forced_types)
    cols = [{"name": namer.lower("column", "%s.c%d" % (key, i)), "type": t} for i, t in enumerate(types)]
    cat_vals = {}
    for i, c in enumerate(cols):
        if c["type"] == "cat":
            k = n_cats or rng.randint(3, 5)
            cat_vals[i] = [namer.lower("category", "%s.k%d.%d" % (key, i, j)) for j in range(min(k, n_rows))]
    rows = []
    names = [namer.entity("%s.r%d" % (key, r)) for r in range(n_rows)]
    for r in range(n_rows):
        row = []
        for i, c in enumerate(cols):
            if c["type"] == "name":
                row.append(names[r])
            elif c["type"] == "cat":
                row.append(cat_vals[i][r] if r < len(cat_vals[i]) else rng.choice(cat_vals[i]))   # every value used at least once
            elif c["type"] == "int":
                row.append(_cell_int(rng))
            elif c["type"] == "dec":
                row.append(_cell_dec(rng))
            else:
                row.append(_cell_date(rng))
        rows.append(row)
    rng.shuffle(rows)
    return {"label": namer.lower("table", key), "columns": cols, "rows": rows}


def col_index(table, name):
    for i, c in enumerate(table["columns"]):
        if c["name"] == name:
            return i
    raise KeyError(name)


def cell_value(ty, v):
    if ty == "int":
        return Decimal(int(v))
    if ty == "dec":
        return Decimal(str(v))
    return v


# ------------------------------------------------------------------------------------------------
# Serialisation (five carriers). Ambiguity rule: no cell may contain a delimiter, a quote, a newline or edge whitespace.
# ------------------------------------------------------------------------------------------------
def cell_text(ty, v):
    if ty == "int":
        return str(int(v))
    if ty == "dec":
        return str(Decimal(str(v)).quantize(D2))
    return str(v)


BAD_CHARS = set('|,\t\n\r"\\{}[]:;=')


def carrier_safe(table):
    names = [c["name"] for c in table["columns"]]
    if len(set(names)) != len(names):
        return False
    for c in table["columns"]:
        if any(ch in BAD_CHARS or ch.isspace() for ch in c["name"]):
            return False
    for row in table["rows"]:
        for c, v in zip(table["columns"], row):
            s = cell_text(c["type"], v)
            if s != s.strip() or any(ch in BAD_CHARS for ch in s) or not s:
                return False
    return True


def serialize(table, carrier):
    names = [c["name"] for c in table["columns"]]
    rows = [[cell_text(c["type"], v) for c, v in zip(table["columns"], row)] for row in table["rows"]]
    if carrier == "TBL-PIPE":
        return "\n".join([" | ".join(names)] + [" | ".join(r) for r in rows])
    if carrier == "TBL-CSV":
        return "\n".join([",".join(names)] + [",".join(r) for r in rows])
    if carrier == "TBL-TSV":
        return "\n".join(["\t".join(names)] + ["\t".join(r) for r in rows])
    if carrier == "TBL-KV":
        return "\n".join("row %d: %s" % (i + 1, "; ".join("%s=%s" % (n, v) for n, v in zip(names, r))) for i, r in enumerate(rows))
    if carrier == "TBL-JSON":
        out = []
        for r in rows:
            obj = {}
            for c, v in zip(table["columns"], r):
                obj[c["name"]] = int(v) if c["type"] == "int" else v
            out.append(obj)
        return json.dumps(out, separators=(",", ":"))
    raise ValueError(carrier)


# ------------------------------------------------------------------------------------------------
# Query AST and evaluator   (SOLVER A)
# q = {"table": 0, "join": None | {"left_key": name, "right_key": name} (tables[0] = dim, tables[1] = fact),
#      "where": [{"t": 0|1, "col": name, "op": ">=", "val": ...}], "conj": "and"|"or",
#      "agg": {"fn": "sum", "t": 0|1, "col": name} | {"fn": "count"},  "group": {"t":0,"col":name} | None}
# ------------------------------------------------------------------------------------------------
def joined_rows(tables, q):
    """Rows as dicts {(t, col): value}."""
    t0 = tables[0]
    base = [{(0, c["name"]): cell_value(c["type"], v) for c, v in zip(t0["columns"], row)} for row in t0["rows"]]
    if not q.get("join"):
        return base
    t1 = tables[1]
    fact = [{(1, c["name"]): cell_value(c["type"], v) for c, v in zip(t1["columns"], row)} for row in t1["rows"]]
    lk, rk = q["join"]["left_key"], q["join"]["right_key"]
    out = []
    for f in fact:
        for d in base:
            if d[(0, lk)] == f[(1, rk)]:
                m = dict(d)
                m.update(f)
                out.append(m)
    return out


def cmp_val(a, op, b):
    return {">=": a >= b, ">": a > b, "<=": a <= b, "<": a < b, "=": a == b}[op]


def _where_val(tables, cond):
    ty = tables[cond["t"]]["columns"][col_index(tables[cond["t"]], cond["col"])]["type"]
    return cell_value(ty, cond["val"])


def filter_rows(tables, q, rows, skip=None, conj=None, ops=None):
    conds = q["where"]
    conj = conj or q.get("conj", "and")
    out = []
    for r in rows:
        res = []
        for i, c in enumerate(conds):
            if skip is not None and i == skip:
                continue
            op = c["op"] if ops is None or i not in ops else ops[i]
            res.append(cmp_val(r[(c["t"], c["col"])], op, _where_val(tables, c)))
        if not res:
            out.append(r)
        elif (all(res) if conj == "and" else any(res)):
            out.append(r)
    return out


def agg_values(fn, vals):
    if fn == "count":
        return Decimal(len(vals))
    if not vals:
        return None
    if fn == "sum":
        return sum(vals, Decimal(0))
    if fn == "min":
        return min(vals)
    if fn == "max":
        return max(vals)
    if fn == "avg":
        return (sum(vals, Decimal(0)) / Decimal(len(vals))).quantize(D2, rounding=ROUND_HALF_UP)
    raise ValueError(fn)


def run_scalar(tables, q, rows=None, skip=None, conj=None, ops=None, agg=None):
    rows = rows if rows is not None else joined_rows(tables, q)
    f = filter_rows(tables, q, rows, skip, conj, ops)
    a = agg or q["agg"]
    if a["fn"] == "count":
        return Decimal(len(f))
    return agg_values(a["fn"], [r[(a["t"], a["col"])] for r in f])


def run_groups(tables, q, rows=None, skip=None, agg=None):
    """{group value: aggregate}"""
    rows = rows if rows is not None else joined_rows(tables, q)
    f = filter_rows(tables, q, rows, skip)
    g = q["group"]
    buckets = {}
    for r in f:
        buckets.setdefault(r[(g["t"], g["col"])], []).append(r)
    a = agg or q["agg"]
    res = {}
    for k, rs in buckets.items():
        if a["fn"] == "count":
            res[k] = Decimal(len(rs))
        else:
            res[k] = agg_values(a["fn"], [r[(a["t"], a["col"])] for r in rs])
    return res


def argbest(d, highest=True):
    """Key with the highest/lowest value; None on a tie for first place."""
    if not d:
        return None
    items = sorted(d.items(), key=lambda kv: kv[1], reverse=highest)
    if len(items) > 1 and items[0][1] == items[1][1]:
        return None
    return items[0][0]


def second(d, highest=True):
    items = sorted(d.items(), key=lambda kv: kv[1], reverse=highest)
    if len(items) < 2 or (len(items) > 2 and items[1][1] == items[2][1]) or items[0][1] == items[1][1]:
        return None
    return items[1][0]


# ------------------------------------------------------------------------------------------------
# Condition / query text
# ------------------------------------------------------------------------------------------------
def cond_text(tables, c):
    t = tables[c["t"]]
    ty = t["columns"][col_index(t, c["col"])]["type"]
    if ty == "cat" or ty == "name":
        return "%s is %s" % (c["col"], c["val"])
    optext = (OP_TEXT_DATE if ty == "date" else OP_TEXT_NUM)[c["op"]]
    return "%s %s %s" % (c["col"], optext, c["val"])


def where_text(tables, q):
    parts = [cond_text(tables, c) for c in q["where"]]
    return (" %s " % q.get("conj", "and")).join(parts)


# ------------------------------------------------------------------------------------------------
# Generation
# ------------------------------------------------------------------------------------------------
BIN_DIMS = {"easy": ((4, 8), (3, 4)), "mid": ((9, 13), (4, 5)), "hard": ((14, 20), (5, 7))}


def _numeric_cols(table):
    return [c["name"] for c in table["columns"] if c["type"] in NUMERIC]


def _cat_cols(table):
    return [c["name"] for c in table["columns"] if c["type"] == "cat"]


def _rand_cond(rng, tables, t, rows_ref=None, allow_cat=True, allow_date=True):
    table = tables[t]
    cands = [c for c in table["columns"] if c["type"] in NUMERIC or (allow_cat and c["type"] == "cat") or (allow_date and c["type"] == "date")]
    c = rng.choice(cands)
    i = col_index(table, c["name"])
    vals = [r[i] for r in table["rows"]]
    if c["type"] == "cat":
        return {"t": t, "col": c["name"], "op": "=", "val": rng.choice(vals)}
    v = rng.choice(vals)
    return {"t": t, "col": c["name"], "op": rng.choice([">=", ">", "<=", "<"]), "val": cell_text(c["type"], v)}


def make_single_query(rng, tables, n_conds, agg_fns=("sum", "min", "max", "avg")):
    t = tables[0]
    conds = [_rand_cond(rng, tables, 0) for _ in range(n_conds)]
    # avoid two conditions on the same column
    if len({c["col"] for c in conds}) < len(conds):
        return None
    num = rng.choice(_numeric_cols(t))
    return {"table": 0, "join": None, "where": conds, "conj": rng.choice(["and", "and", "or"]) if n_conds == 2 else "and",
            "agg": {"fn": rng.choice(agg_fns), "t": 0, "col": num}, "group": None}


def num_text(x):
    return fmt_num(x)


def _agg_with(tables, q, fn):
    """Aggregate spec with function fn; a count query has no column, so use the first numeric one of the query's table."""
    a = q["agg"]
    if "col" in a:
        return dict(a, fn=fn)
    if q.get("join"):
        return {"fn": fn, "t": 1, "col": tables[1]["columns"][1]["name"]}
    return {"fn": fn, "t": 0, "col": _numeric_cols(tables[0])[0]}


def b1_flaws(tables, q):
    """{trap_type: [Decimal,...]} for a scalar query."""
    rows = joined_rows(tables, q)
    correct = run_scalar(tables, q, rows)
    out = {}

    def add(t, v):
        if v is None or v == correct or v < 0 or not is_2dp(v):
            return
        out.setdefault(t, [])
        if v not in out[t]:
            out[t].append(v)
    for i, c in enumerate(q["where"]):
        if c["op"] in FLIP_OP:
            add("boundary", run_scalar(tables, q, rows, ops={i: FLIP_OP[c["op"]]}))
        if len(q["where"]) > 1:
            add("filter_dropped", run_scalar(tables, q, rows, skip=i))
    if len(q["where"]) == 2:
        add("and_or", run_scalar(tables, q, rows, conj="or" if q.get("conj", "and") == "and" else "and"))
    for fn in ("sum", "min", "max", "avg", "count"):
        if fn != q["agg"]["fn"]:
            add("wrong_aggregate", run_scalar(tables, q, rows, agg=_agg_with(tables, q, fn)))
    if q["agg"].get("col") is not None:
        for other in _numeric_cols(tables[q["agg"]["t"]]):
            if other != q["agg"]["col"]:
                add("wrong_column", run_scalar(tables, q, rows, agg=dict(q["agg"], col=other)))
    return out


def pick_numeric_options(correct, flaws, k, rng, balancer, scope):
    return pick_options_ranked(correct, flaws, k, rng, balancer, scope, sim=dp_class)


def _mk_tables(rng, namer, form, bin_name, carrier):
    (rlo, rhi), (clo, chi) = BIN_DIMS[bin_name]
    for _ in range(50):
        t0 = make_table(rng, namer, "a", rng.randint(rlo, rhi), rng.randint(clo, chi), with_dates=rng.random() < 0.4)
        if carrier_safe(t0):
            return [t0]
    return None


def make_b1(rng, namer, bin_name, balancer, scope, carrier):
    for _ in range(200):
        tables = _mk_tables(rng, namer, "TB-B1", bin_name, carrier)
        if not tables:
            continue
        n_conds = 1 if bin_name == "easy" else rng.choice([1, 2])
        q = make_single_query(rng, tables, n_conds)
        if q is None:
            continue
        rows = joined_rows(tables, q)
        sel = filter_rows(tables, q, rows)
        if len(sel) < 2 or len(sel) == len(rows):
            continue
        ans = run_scalar(tables, q, rows)
        if ans is None:
            continue
        ch = pick_numeric_options(ans, b1_flaws(tables, q), 4, rng, balancer, scope)
        if ch is None:
            continue
        return _b1_item(tables, q, ans, ch, bin_name)
    return None


def _b1_item(tables, q, ans, ch, bin_name):
    spec = {"version": 1, "form": "TB-B1", "tables": tables, "query": q}
    opts = [{"text": num_text(ans), "trap": None, "correct": True}] + [{"text": num_text(v), "trap": t, "correct": False} for v, t in ch]
    t = tables[0]
    return {"spec": spec, "answer": num_text(ans), "options": opts, "score": len(t["rows"]) // 4 + len(t["columns"]) + 2 * len(q["where"])}


def solve_b1(spec):
    return num_text(run_scalar(spec["tables"], spec["query"]))


def make_b2(rng, namer, bin_name, balancer, scope, carrier):
    for _ in range(300):
        tables = _mk_tables(rng, namer, "TB-B2", bin_name, carrier)
        if not tables:
            continue
        t = tables[0]
        cats = _cat_cols(t)
        grouped = rng.random() < 0.7 and cats
        num = rng.choice(_numeric_cols(t))
        if grouped:
            gcol = rng.choice(cats)
            fn = rng.choice(["sum", "avg", "max", "min"])
            q = {"table": 0, "join": None, "where": [], "conj": "and", "agg": {"fn": fn, "t": 0, "col": num}, "group": {"t": 0, "col": gcol}}
            if rng.random() < 0.4 and bin_name != "easy":
                c = _rand_cond(rng, tables, 0, allow_cat=False)
                if c["col"] == num or c["col"] == gcol:
                    continue
                q["where"] = [c]
        else:
            nm = t["columns"][0]["name"]
            q = {"table": 0, "join": None, "where": [], "conj": "and", "agg": {"fn": "max", "t": 0, "col": num}, "group": {"t": 0, "col": nm}}
        highest = rng.random() < 0.75
        q["highest"] = highest
        rows = joined_rows(tables, q)
        g = run_groups(tables, q, rows)
        if len(g) < 4:
            continue
        best = argbest(g, highest)
        if best is None:
            continue
        flaws = b2_flaws(tables, q, rows, best)
        chosen, used, avail = [], {best}, [f for f, v in flaws.items() if v]
        while len(chosen) < 3 and avail:
            tt = balancer.pick(scope, avail)
            avail.remove(tt)
            vals = [v for v in flaws[tt] if v not in used]
            if not vals:
                balancer.key_counts(scope)[tt] -= 1
                continue
            v = rng.choice(vals)
            used.add(v)
            chosen.append((v, tt))
        rest = [k for k in g if k not in used]
        rng.shuffle(rest)
        while len(chosen) < 3 and rest:
            v = rest.pop()
            used.add(v)
            chosen.append((v, "other_group"))
        if len(chosen) < 3:
            continue
        # keep other_group rare: at most one per row, already true; reject rows with two
        if sum(1 for _, tt in chosen if tt == "other_group") > 1:
            continue
        spec = {"version": 1, "form": "TB-B2", "tables": tables, "query": q}
        return {"spec": spec, "answer": best, "options": [{"text": best, "trap": None, "correct": True}] +
                [{"text": v, "trap": tt, "correct": False} for v, tt in chosen], "score": len(t["rows"]) // 4 + len(t["columns"]) + len(q["where"]) * 2}
    return None


def b2_flaws(tables, q, rows, best):
    highest = q.get("highest", True)
    out = {}

    def add(tp, v):
        if v is not None and v != best:
            out.setdefault(tp, [])
            if v not in out[tp]:
                out[tp].append(v)
    for fn in ("sum", "avg", "max", "min", "count"):
        if fn != q["agg"]["fn"]:
            add("wrong_aggregate", argbest(run_groups(tables, q, rows, agg=_agg_with(tables, q, fn)), highest))
    for other in _numeric_cols(tables[0]):
        if other != q["agg"]["col"]:
            add("wrong_column", argbest(run_groups(tables, q, rows, agg=dict(q["agg"], col=other)), highest))
    if q["where"]:
        add("filter_ignored", argbest(run_groups(tables, q, rows, skip=0), highest))
    g = run_groups(tables, q, rows)
    add("lowest_instead" if highest else "highest_instead", argbest(g, not highest))
    add("second_place", second(g, highest))
    return out


def solve_b2(spec):
    q = spec["query"]
    return argbest(run_groups(spec["tables"], q), q.get("highest", True))


def make_b3(rng, namer, bin_name, balancer, scope, carrier):
    (rlo, rhi), _ = BIN_DIMS[bin_name]
    for _ in range(300):
        n_dim = rng.randint(4, 8)
        dim = make_table(rng, namer, "d", n_dim, rng.randint(3, 4), forced_types=None)
        if not carrier_safe(dim):
            continue
        # ensure the dim table has a numeric column
        dnum = _numeric_cols(dim)
        dcat = _cat_cols(dim)
        if not dnum or not dcat:
            continue
        keys = [r[0] for r in dim["rows"]]
        n_f = rng.randint(max(6, rlo), min(rhi + 2, 20))
        fcols = [{"name": namer.lower("column", "f.key"), "type": "name"}, {"name": namer.lower("column", "f.amount"), "type": rng.choice(["int", "dec"])}]
        if rng.random() < 0.5:
            fcols.append({"name": namer.lower("column", "f.extra"), "type": "int"})
        used_keys = rng.sample(keys, rng.randint(max(2, n_dim // 2), n_dim - 1))
        frows = []
        for i in range(n_f):
            row = []
            for c in fcols:
                row.append(rng.choice(used_keys) if c["type"] == "name" else (_cell_int(rng) if c["type"] == "int" else _cell_dec(rng)))
            frows.append(row)
        fact = {"label": namer.lower("table", "f"), "columns": fcols, "rows": frows}
        if not carrier_safe(fact):
            continue
        tables = [dim, fact]
        cc = rng.choice(dcat)
        ci = col_index(dim, cc)
        cval = rng.choice([r[ci] for r in dim["rows"] if r[0] in used_keys])
        where = [{"t": 0, "col": cc, "op": "=", "val": cval}]
        if bin_name != "easy" and rng.random() < 0.5:
            where.append({"t": 1, "col": fcols[1]["name"], "op": rng.choice([">=", "<="]), "val": cell_text(fcols[1]["type"], rng.choice([r[1] for r in frows]))})
        fn = rng.choice(["count", "sum", "sum", "avg", "max"])
        if fn == "count":
            agg = {"fn": "count"}
        elif rng.random() < 0.45:
            agg = {"fn": fn if fn != "count" else "sum", "t": 0, "col": rng.choice(dnum)}      # dimension value repeated per joined row
        else:
            agg = {"fn": fn, "t": 1, "col": fcols[1]["name"]}
        q = {"table": 0, "join": {"left_key": dim["columns"][0]["name"], "right_key": fcols[0]["name"]}, "where": where, "conj": "and", "agg": agg, "group": None}
        rows = joined_rows(tables, q)
        sel = filter_rows(tables, q, rows)
        if len(sel) < 2:
            continue
        ans = run_scalar(tables, q, rows)
        flaws = b3_flaws(tables, q, rows, ans)
        ch = pick_numeric_options(ans, flaws, 4, rng, balancer, scope)
        if ch is None:
            continue
        spec = {"version": 1, "form": "TB-B3", "tables": tables, "query": q}
        return {"spec": spec, "answer": num_text(ans), "options": [{"text": num_text(ans), "trap": None, "correct": True}] +
                [{"text": num_text(v), "trap": t, "correct": False} for v, t in ch], "score": len(frows) // 4 + 3 + 2 * len(where)}
    return None


def b3_flaws(tables, q, rows, correct):
    out = {}

    def add(t, v):
        if v is not None and v != correct and v >= 0 and is_2dp(v):
            out.setdefault(t, [])
            if v not in out[t]:
                out[t].append(v)
    dim, fact = tables
    a = q["agg"]
    # no fan-out: aggregate the dimension value over dimension rows instead of joined rows
    if a["fn"] != "count" and a["t"] == 0:
        drows = [{(0, c["name"]): cell_value(c["type"], v) for c, v in zip(dim["columns"], row)} for row in dim["rows"]]
        dq = dict(q, join=None, where=[c for c in q["where"] if c["t"] == 0])
        add("no_fanout", run_scalar(tables, dq, drows))
    if a["fn"] == "count":
        add("left_join_count", Decimal(len(filter_rows([dim, fact], dict(q, where=[c for c in q["where"] if c["t"] == 0]),
                                                     [{(0, c["name"]): cell_value(c["type"], v) for c, v in zip(dim["columns"], row)} for row in dim["rows"]]))))
        keys = {r[(0, q["join"]["left_key"])] for r in filter_rows(tables, q, rows)}
        add("distinct_keys", Decimal(len(keys)))
    for i, c in enumerate(q["where"]):
        if c["op"] in FLIP_OP:
            add("boundary", run_scalar(tables, q, rows, ops={i: FLIP_OP[c["op"]]}))
        if len(q["where"]) > 1:
            add("filter_dropped", run_scalar(tables, q, rows, skip=i))
    for fn in ("sum", "max", "avg", "count"):
        if fn != a["fn"]:
            add("wrong_aggregate", run_scalar(tables, q, rows, agg=_agg_with(tables, q, fn)))
    return out


def solve_b3(spec):
    return num_text(run_scalar(spec["tables"], spec["query"]))


# ---- B4 claims -----------------------------------------------------------------------------------
def make_b4(rng, namer, bin_name, want_true, balancer, scope, carrier):
    for _ in range(300):
        tables = _mk_tables(rng, namer, "TB-B4", bin_name, carrier)
        if not tables:
            continue
        kind = rng.choice(["value", "value", "count", "extreme"])
        t = tables[0]
        if kind == "extreme":
            num = rng.choice(_numeric_cols(t))
            highest = rng.random() < 0.6
            q = {"table": 0, "join": None, "where": [], "conj": "and", "agg": {"fn": "max" if highest else "min", "t": 0, "col": num}, "group": None, "highest": highest}
            if rng.random() < 0.5 and bin_name != "easy":
                c = _rand_cond(rng, tables, 0, allow_cat=True)
                if c["col"] == num:
                    continue
                q["where"] = [c]
            rows = joined_rows(tables, q)
            sel = filter_rows(tables, q, rows)
            if len(sel) < 3:
                continue
            ni = 0
            order = sorted(sel, key=lambda r: r[(0, num)], reverse=highest)
            if order[0][(0, num)] == order[1][(0, num)]:
                continue
            true_name = order[0][(0, t["columns"][0]["name"])]
            alts = {"second_place": order[1][(0, t["columns"][0]["name"])], "opposite_extreme": order[-1][(0, t["columns"][0]["name"])]}
            if q["where"]:
                full = sorted(rows, key=lambda r: r[(0, num)], reverse=highest)
                alts["filter_ignored"] = full[0][(0, t["columns"][0]["name"])]
            alts = {k: v for k, v in alts.items() if v != true_name}
            if not alts:
                continue
            ftype = balancer.pick(scope, list(alts))
            claimed = true_name if want_true else alts[ftype]
            spec = {"version": 1, "form": "TB-B4", "tables": tables, "query": q, "claim": {"kind": "extreme", "value": claimed}}
            truth = claimed == true_name
            wrong_flaw = ftype
        else:
            n_conds = 1 if bin_name == "easy" else rng.choice([1, 2])
            q = make_single_query(rng, tables, n_conds, agg_fns=("sum", "min", "max", "avg") if kind == "value" else ("sum",))
            if q is None:
                continue
            if kind == "count":
                q["agg"] = {"fn": "count"}
            rows = joined_rows(tables, q)
            sel = filter_rows(tables, q, rows)
            if len(sel) < 2 or len(sel) == len(rows):
                continue
            ans = run_scalar(tables, q, rows)
            flaws = b1_flaws(tables, q)
            types = [tp for tp, v in flaws.items() if v]
            if not types:
                continue
            ftype = balancer.pick(scope, types)
            fval = rng.choice(flaws[ftype])
            claimed = ans if want_true else fval
            spec = {"version": 1, "form": "TB-B4", "tables": tables, "query": q, "claim": {"kind": kind, "value": num_text(claimed)}}
            truth = claimed == ans
            wrong_flaw = ftype
        if truth != want_true:
            continue
        T = {True: "True", False: "False"}
        return {"spec": spec, "answer": T[truth].lower(), "options": [{"text": T[truth], "trap": None, "correct": True}, {"text": T[not truth], "trap": wrong_flaw, "correct": False}],
                "score": len(t["rows"]) // 4 + len(t["columns"]) + 2 * len(q["where"])}
    return None


def solve_b4(spec):
    q, claim, tables = spec["query"], spec["claim"], spec["tables"]
    t = tables[0]
    if claim["kind"] == "extreme":
        rows = joined_rows(tables, q)
        sel = filter_rows(tables, q, rows)
        num = q["agg"]["col"]
        order = sorted(sel, key=lambda r: r[(0, num)], reverse=q.get("highest", True))
        return "true" if order[0][(0, t["columns"][0]["name"])] == claim["value"] else "false"
    ans = run_scalar(tables, q)
    return "true" if num_text(ans) == claim["value"] else "false"


def perturb(item, rng, balancer, scope):
    """One slot edited so the answer changes. B1/B3: one numeric cell; B2: one numeric cell; B4: the claimed value."""
    spec = item["spec"]
    form = spec["form"]
    if form == "TB-B4":
        old = solve_b4(spec)
        q, claim, tables = spec["query"], spec["claim"], spec["tables"]
        if claim["kind"] == "extreme":
            t = tables[0]
            rows = joined_rows(tables, q)
            sel = filter_rows(tables, q, rows)
            num = q["agg"]["col"]
            order = sorted(sel, key=lambda r: r[(0, num)], reverse=q.get("highest", True))
            nmcol = t["columns"][0]["name"]
            names = [r[(0, nmcol)] for r in order]
            want_names = [n for n in names if n != claim["value"]] if old == "true" else [names[0]]
            if not want_names:
                return None
            newv = rng.choice(want_names)
            s2 = dict(spec, claim={"kind": "extreme", "value": newv})
        else:
            ans = run_scalar(tables, q)
            if old == "true":
                fl = b1_flaws(tables, q)
                vals = [v for vs in fl.values() for v in vs]
                if not vals:
                    return None
                newv = num_text(rng.choice(vals))
            else:
                newv = num_text(ans)
            s2 = dict(spec, claim={"kind": claim["kind"], "value": newv})
        new = solve_b4(s2)
        if new == old:
            return None
        T = {"true": "True", "false": "False"}
        other = "false" if new == "true" else "true"
        return {"spec": s2, "answer": new, "options": [{"text": T[new], "trap": None, "correct": True}, {"text": T[other], "trap": item["options"][1]["trap"] or "pair_claim", "correct": False}], "score": item["score"]}
    tables = spec["tables"]
    solve = {"TB-B1": solve_b1, "TB-B2": solve_b2, "TB-B3": solve_b3}[form]
    old = solve(spec)
    cells = [(ti, ri, ci) for ti, t in enumerate(tables) for ri in range(len(t["rows"])) for ci, c in enumerate(t["columns"]) if c["type"] in NUMERIC]
    rng.shuffle(cells)
    for ti, ri, ci in cells[:80]:
        ty = tables[ti]["columns"][ci]["type"]
        t2 = [dict(t, rows=[list(r) for r in t["rows"]]) for t in tables]
        v = _cell_int(rng) if ty == "int" else _cell_dec(rng)
        t2[ti]["rows"][ri][ci] = v
        s2 = dict(spec, tables=t2)
        try:
            new = solve(s2)
        except Exception:
            continue
        if new is None or new == old:
            continue
        if form == "TB-B2":
            q = spec["query"]
            rows = joined_rows(t2, q)
            g = run_groups(t2, q, rows)
            best = argbest(g, q.get("highest", True))
            if best is None or len(g) < 4:
                continue
            flaws = b2_flaws(t2, q, rows, best)
            chosen, used, avail = [], {best}, [f for f, vv in flaws.items() if vv]
            while len(chosen) < 3 and avail:
                tt = balancer.pick(scope, avail)
                avail.remove(tt)
                vals = [vv for vv in flaws[tt] if vv not in used]
                if not vals:
                    balancer.key_counts(scope)[tt] -= 1
                    continue
                vv = rng.choice(vals)
                used.add(vv)
                chosen.append((vv, tt))
            rest = [k for k in g if k not in used]
            rng.shuffle(rest)
            while len(chosen) < 3 and rest:
                vv = rest.pop()
                used.add(vv)
                chosen.append((vv, "other_group"))
            if len(chosen) < 3:
                continue
            return {"spec": s2, "answer": best, "options": [{"text": best, "trap": None, "correct": True}] +
                    [{"text": vv, "trap": tt, "correct": False} for vv, tt in chosen], "score": item["score"]}
        q = spec["query"]
        rows = joined_rows(t2, q)
        flaws = b1_flaws(t2, q) if form == "TB-B1" else b3_flaws(t2, q, rows, run_scalar(t2, q, rows))
        ans = run_scalar(t2, q, rows)
        ch = pick_numeric_options(ans, flaws, 4, rng, balancer, scope)
        if ch is None:
            continue
        return {"spec": s2, "answer": num_text(ans), "options": [{"text": num_text(ans), "trap": None, "correct": True}] +
                [{"text": num_text(vv), "trap": tt, "correct": False} for vv, tt in ch], "score": item["score"]}
    return None


# ------------------------------------------------------------------------------------------------
# Rendering
# ------------------------------------------------------------------------------------------------
def rank_phrase(spec):
    q = spec["query"]
    g = q["group"]
    a = q["agg"]
    word = {"sum": "total", "avg": "average", "max": "maximum", "min": "minimum"}[a["fn"]]
    hi = "highest" if q.get("highest", True) else "lowest"
    t = spec["tables"]
    if g["col"] == t[0]["columns"][0]["name"]:
        s = "%s %s" % (hi, a["col"])
    else:
        s = "%s %s %s per %s" % (hi, word, a["col"], g["col"])
    if q["where"]:
        s += ", counting only rows where %s" % where_text(t, q)
    return s


def _agg_phrase(q):
    return AGG_WORD[q["agg"]["fn"]]


def render(item, pool, widx, rng, domain, carrier="TBL-PIPE"):
    spec = item["spec"]
    form = spec["form"]
    tables = spec["tables"]
    doc = Doc()
    doc.sentence(pool.get("scene." + domain, rng.randrange(1 << 20)), {})
    blocks = []
    for t in tables:
        lab = pool.get("tb.table_label", rng.randrange(1 << 20)).replace("{label}", t["label"])
        blocks.append(lab + "\n" + serialize(t, carrier))
    text = "\n".join(blocks)
    doc.sep("\n")
    start = doc.pos
    intro = pool.get("tb.intro", rng.randrange(1 << 20))
    s = doc.sentence(intro, {"tables": (text, None, None)})
    q = spec["query"]
    if form == "TB-B3":
        doc.sep("\n")        # skeptic fix 18 Oct: the join key was never stated; the gold depends on it
        doc.sentence(pool.get("tb.join", rng.randrange(1 << 20)), {"lk": (q["join"]["left_key"], "entity", "name"), "rk": (q["join"]["right_key"], "entity", "name")})
    uses_avg = (q.get("agg", {}).get("fn") == "avg") or (form == "TB-B4" and q.get("agg", {}).get("fn") == "avg" and spec["claim"]["kind"] == "value")
    if uses_avg and form != "TB-B2":
        doc.sep("\n")
        doc.sentence(pool.get("tb.rounding", rng.randrange(1 << 20)), {}, whole=("entity", "rule"))
    end_block(doc, "TXT-NUMBERED")
    if form in ("TB-B1", "TB-B3"):
        a = q["agg"]
        col = a.get("col") or "rows"
        agg = _agg_phrase(q)
        if a["fn"] == "count":
            agg, col = "number", "rows"
        doc.sentence(pool.get("q." + form, widx), {"agg": (agg, "entity", "rule"), "col": (col, "entity", "name"), "cond": (where_text(tables, q), "entity", "rule")})
    elif form == "TB-B2":
        doc.sentence(pool.get("q.TB-B2", widx), {"rank_phrase": (rank_phrase(spec), "entity", "rule")})
    else:
        c = spec["claim"]
        if c["kind"] == "extreme":
            hi = "highest" if q.get("highest", True) else "lowest"
            claim = "the row with the %s %s%s is %s" % (hi, q["agg"]["col"], (" among rows where " + where_text(tables, q)) if q["where"] else "", c["value"])
        elif c["kind"] == "count":
            claim = "exactly %s rows satisfy: %s" % (c["value"], where_text(tables, q))
        else:
            claim = "the %s of %s over rows where %s is %s" % (_agg_phrase(q), q["agg"]["col"], where_text(tables, q), c["value"])
        doc.sentence(pool.get("q.TB-B4", widx), {"claim": ("\"%s\"" % claim, "entity", "statement")})       # quoted: the claim is a clause with its own "is"
    return doc.text(), doc.spans


def item_bin(item):
    spec = item["spec"]
    rows = max(len(t["rows"]) for t in spec["tables"])
    nconds = len(spec["query"]["where"])
    if len(spec["tables"]) > 1:
        # join items: 'hard' needs BOTH a big fact table and two filters. (Skeptic fix 18 Oct: with 'or', 92 percent of generated joins were hard
        # because a one-filter join almost never yields three distinct wrong answers, so TABLE broke the hard <= 30 percent bar.)
        return "hard" if (len(spec["tables"][1]["rows"]) >= 14 and nconds >= 2) else "mid"
    if rows >= 14:
        return "hard"
    if rows >= 9 or nconds >= 2:
        return "mid"
    return "easy"
