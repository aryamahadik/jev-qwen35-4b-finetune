"""GEN / ARITH sub-block: typed quantity DAG, exact decimal SOLVER A, error-model distractors, rendering.

Forms: AR-F1 (value of the final quantity), AR-F2 (threshold test), AR-F3 (first wrong line in a worked solution).
Gold = exact Decimal evaluation in topological order. No code is executed from rows. No model in the loop.
Solver B (separate session, exact Fractions + a unit-dimension checker) is NOT here.
"""
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, Decimal

from gen_common import (D2, Doc, dec, end_block, fmt_num, is_2dp, item_sep, join_names, pick_options_ranked, unit_text, dp_class)

DIM_UNITS = {"mass": ["gram", "kilogram"], "vol": ["litre"], "len": ["metre", "kilometre"],
             "time": ["second", "minute", "hour", "day", "week"], "count": ["count"]}
UNIT_DIM = {u: d for d, us in DIM_UNITS.items() for u in us}
UNIT_SCALE = {"gram": Decimal(1), "kilogram": Decimal(1000), "litre": Decimal(1), "metre": Decimal(1), "kilometre": Decimal(1000),
              "second": Decimal(1), "minute": Decimal(60), "hour": Decimal(3600), "day": Decimal(86400), "week": Decimal(604800),
              "count": Decimal(1)}
PCTS = [5, 10, 12, 15, 20, 25, 30, 40, 45, 50, 60, 75, 80]
RATIOS = [(1, 2), (2, 3), (1, 3), (3, 5), (2, 5), (1, 4), (3, 4), (1, 1), (3, 7)]
ROUND_RULES = ["nearest_int", "one_dp", "floor_int", "ceil_int"]
ROUND_TEXT = {"nearest_int": "to the nearest whole number (halves round up)", "one_dp": "to one decimal place (halves round up)",
              "floor_int": "down to a whole number", "ceil_int": "up to a whole number"}
MERGE_OPS = ("add", "sub", "min", "max")
MAXV = Decimal(10) ** 6
CMP_TEXT = {"ge": "at least", "le": "at most", "gt": "more than", "lt": "less than"}
UNIT_SLIP_FACTORS = [Decimal(10), Decimal("0.1"), Decimal(100), Decimal(1000), Decimal(60), Decimal(1) / Decimal(60)]


class Invalid(Exception):
    pass


def _round_value(v, rule):
    if rule == "nearest_int":
        return v.quantize(Decimal(1), rounding=ROUND_HALF_UP)
    if rule == "one_dp":
        return v.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    if rule == "floor_int":
        return v.quantize(Decimal(1), rounding=ROUND_FLOOR)
    if rule == "ceil_int":
        return v.quantize(Decimal(1), rounding=ROUND_CEILING)
    raise Invalid("bad rounding rule")


def apply_op(op, vals, units, param, strict=True):
    """Returns (value, unit). Raises Invalid. strict: >=0, <=1e6, <=2 decimals, unit rules."""
    a = vals[0]
    u = units[0]
    if op in ("add", "min", "max"):
        if strict and any(x != u for x in units):
            raise Invalid("unit mismatch")
        v = sum(vals, Decimal(0)) if op == "add" else (min(vals) if op == "min" else max(vals))
    elif op == "sub":
        v = vals[0] - vals[1]
    elif op == "mul":
        v = a * Decimal(param)
    elif op == "div":
        v = a / Decimal(param)
        if v * Decimal(param) != a:
            raise Invalid("inexact")
    elif op == "pct":
        v = a * Decimal(param) / Decimal(100)
    elif op == "split":
        r = param["r"]
        v = a * Decimal(r[param["which"]]) / Decimal(r[0] + r[1])
    elif op == "conv":
        if UNIT_DIM[param] != UNIT_DIM[u]:
            raise Invalid("conv across dimensions")
        v = a * UNIT_SCALE[u] / UNIT_SCALE[param]
        u = param
    elif op == "round":
        v = _round_value(a, param)
    else:
        raise Invalid("unknown op")
    if v < 0 or v > MAXV or not is_2dp(v):
        raise Invalid("out of range or not 2dp")
    return v, u


def evaluate(spec, mut=None):
    """Exact evaluation in topological order (steps are stored in topological order).
    mut: {step_id: ("skip",) | ("op", new_op) | ("param", p) | ("args", [ids]) | ("postround", rule)}  (error models only)
    Returns {id: (value, unit)}."""
    env = {b["id"]: (dec(b["value"]), b["unit"]) for b in spec["base"]}
    for bid, mm in (mut or {}).items():
        if bid in env and mm[0] == "scale":
            env[bid] = (env[bid][0] * mm[1], env[bid][1])
    for st in spec["steps"]:
        op, args, param = st["op"], st["args"], st["param"]
        post = None
        m = (mut or {}).get(st["id"])
        if m and m[0] == "scale":
            vals = [env[x][0] for x in args]
            units = [env[x][1] for x in args]
            v, u = apply_op(op, vals, units, param, strict=True)
            env[st["id"]] = (v * m[1], u)
            continue
        if m:
            if m[0] == "skip":
                env[st["id"]] = env[args[0]]
                continue
            if m[0] == "op":
                op = m[1]
            elif m[0] == "param":
                param = m[1]
            elif m[0] == "args":
                args = m[1]
            elif m[0] == "postround":
                post = m[1]
        vals = [env[a][0] for a in args]
        units = [env[a][1] for a in args]
        v, u = apply_op(op, vals, units, param, strict=(mut is None or m is None or m[0] != "op"))
        if post:
            v = _round_value(v, post)
        env[st["id"]] = (v, u)
    return env


def solve_value(spec):
    env = evaluate(spec)
    return env[spec["final"]]


# ------------------------------------------------------------------------------------------------
# Generation
# ------------------------------------------------------------------------------------------------
BIN_STEPS = {"easy": (3, 4), "mid": (5, 6), "hard": (7, 8)}


def bin_of_steps(n):
    return "easy" if n <= 4 else ("mid" if n <= 6 else "hard")


def _rand_base(rng, unit):
    if rng.random() < 0.3:
        v = Decimal(rng.randint(10, 900)) / Decimal(10) * (Decimal(1) if rng.random() < 0.5 else Decimal("0.5"))
        v = v.quantize(D2)
        if v == v.to_integral_value():
            v = v + Decimal("0.5")
        return v
    return Decimal(rng.randint(2, 240))


def _try_build(rng, n_steps, form):
    dim = rng.choices(list(DIM_UNITS), weights=[3, 2, 3, 4, 3])[0]
    units = DIM_UNITS[dim]
    B = rng.randint(2, min(4, max(2, n_steps - 1)))
    same_unit = len(units) == 1 or rng.random() < 0.6
    u0 = rng.choice(units)
    base, env = [], {}
    for i in range(B):
        u = u0 if same_unit else rng.choice(units)
        val = _rand_base(rng, u)
        bid = "b%d" % (i + 1)
        base.append({"id": bid, "value": fmt_num(val), "unit": u})
        env[bid] = (val, u)
    frontier = [b["id"] for b in base]
    steps = []
    for i in range(n_steps):
        remaining = n_steps - i
        need = len(frontier) - 1
        if need > 2 * remaining:
            return None
        by_unit = {}
        for f in frontier:
            by_unit.setdefault(env[f][1], []).append(f)
        merge_units = [u for u, fs in by_unit.items() if len(fs) >= 2]
        must_merge = need >= remaining
        do_merge = bool(merge_units) and need > 0 and (must_merge or rng.random() < 0.45)
        if must_merge and not merge_units:
            return None
        step = None
        for _try in range(14):
            if do_merge:
                u = rng.choice(merge_units)
                pool_ids = by_unit[u]
                fan = 3 if (len(pool_ids) >= 3 and need >= 2 and rng.random() < 0.3) else 2
                op = rng.choice(["add", "add", "sub", "min", "max"] if fan == 2 else ["add", "min", "max"])
                args = rng.sample(pool_ids, fan)
                if op == "sub":
                    args.sort(key=lambda a: -env[a][0])
                param = None
            else:
                tgt = rng.choice(frontier)
                u = env[tgt][1]
                ops = ["mul", "div", "pct", "pct", "split"]
                if len(DIM_UNITS[UNIT_DIM[u]]) > 1:
                    ops += ["conv", "conv"]
                if env[tgt][0] != env[tgt][0].to_integral_value():
                    ops += ["round"]
                op = rng.choice(ops)
                args = [tgt]
                if op == "mul":
                    param = rng.randint(2, 9)
                elif op == "div":
                    param = rng.randint(2, 10)
                elif op == "pct":
                    param = rng.choice(PCTS)
                elif op == "split":
                    param = {"r": list(rng.choice(RATIOS)), "which": rng.randint(0, 1)}
                elif op == "conv":
                    param = rng.choice([x for x in DIM_UNITS[UNIT_DIM[u]] if x != u])
                else:
                    param = rng.choice(ROUND_RULES)
            try:
                v, ou = apply_op(op, [env[a][0] for a in args], [env[a][1] for a in args], param)
            except Invalid:
                continue
            if v == env[args[0]][0] and op not in ("min", "max") and ou == env[args[0]][1]:
                continue                       # identity step
            if v == 0 and op != "sub":
                continue
            step = (op, args, param, v, ou)
            break
        if step is None:
            return None
        op, args, param, v, ou = step
        sid = "s%d" % (i + 1)
        env[sid] = (v, ou)
        steps.append({"id": sid, "op": op, "args": args, "param": param})
        frontier = [f for f in frontier if f not in args] + [sid]
    if len(frontier) != 1:
        return None
    final = frontier[0]
    if final != steps[-1]["id"] or env[final][0] <= 0:
        return None
    if any(env[final][0] == env[b["id"]][0] for b in base):
        return None
    return {"base": base, "steps": steps, "final": final, "dim": dim}


def make_spec(form, rng, namer, bin_name, tries=400):
    lo, hi = BIN_STEPS[bin_name]
    if form == "AR-F3":
        lo = max(lo, 4)
        if lo > hi:
            lo = hi = 4
    for _ in range(tries):
        n = rng.randint(lo, hi)
        prog = _try_build(rng, n, form)
        if prog is None:
            continue
        spec = {"version": 1, "form": form, "dim": prog["dim"], "base": prog["base"], "steps": prog["steps"], "final": prog["final"],
                "count_noun": None, "names": {}}
        for i, x in enumerate(spec["base"] + spec["steps"]):
            spec["names"][x["id"]] = namer.lower("variable", x["id"])
        if any(b["unit"] == "count" for b in spec["base"]) or prog["dim"] == "count":
            spec["count_noun"] = namer.lower("count_noun", "cn")
        spec["n_steps"] = len(spec["steps"])
        return spec
    return None


# ------------------------------------------------------------------------------------------------
# Error models -> distractor values   (trap_type -> list of (value Decimal, detail))
# ------------------------------------------------------------------------------------------------
def _try_eval(spec, mut):
    try:
        env = evaluate(spec, mut)
    except Invalid:
        return None
    return env[spec["final"]][0]


def _uses(spec):
    use = {}
    for st in spec["steps"]:
        for a in st["args"]:
            use.setdefault(a, []).append(st["id"])
    return use


def error_values(spec, rng):
    """{trap_type: [value, ...]} (values != correct, >= 0, 2dp). Each model is a plain mis-reading of the problem."""
    correct = solve_value(spec)[0]
    out = {}

    def add(t, v):
        if v is None or v == correct or v < 0 or not is_2dp(v) or v > MAXV:
            return
        lst = out.setdefault(t, [])
        if v not in lst:
            lst.append(v)

    steps = spec["steps"]
    for st in steps:
        add("omit_step", _try_eval(spec, {st["id"]: ("skip",)}))
        # swap operator
        op = st["op"]
        alt = {"add": "sub", "sub": "add", "min": "max", "max": "min", "mul": "div", "div": "mul"}.get(op)
        if alt and not (op == "add" and len(st["args"]) == 3):
            add("swap_op", _try_eval(spec, {st["id"]: ("op", alt)}))
        if op == "pct":
            add("swap_op", _try_eval(spec, {st["id"]: ("param", 100 - st["param"])}))
        if op == "split":
            add("swap_op", _try_eval(spec, {st["id"]: ("param", {"r": st["param"]["r"], "which": 1 - st["param"]["which"]})}))
        if op == "sub":
            add("swap_op", _try_eval(spec, {st["id"]: ("args", list(reversed(st["args"])))}))
        if op in ("mul", "div"):
            for d in (-1, 1):
                p = st["param"] + d
                if p >= (1 if op == "mul" else 2):
                    add("count_off_by_one", _try_eval(spec, {st["id"]: ("param", p)}))
        if op == "conv":
            add("unit_slip", _try_eval(spec, {st["id"]: ("skip",)}))
        if op == "pct":
            # percent of the wrong base: an earlier quantity of the same unit that is not the stated one
            env = evaluate(spec)
            u = env[st["args"][0]][1]
            ids_before = [b["id"] for b in spec["base"]] + [s["id"] for s in steps[: steps.index(st)]]
            for q in ids_before:
                if q != st["args"][0] and env[q][1] == u:
                    add("pct_wrong_base", _try_eval(spec, {st["id"]: ("args", [q])}))
        if op == "round":
            # early rounding: round the producer of the rounded value before continuing
            src = st["args"][0]
            prod = next((s for s in steps if s["id"] == src), None)
            if prod is not None:
                add("early_rounding", _try_eval(spec, {prod["id"]: ("postround", st["param"])}))
    # precedence: a multiplicative step fed by an additive step used only there is applied to one addend only
    use = _uses(spec)
    byid = {s["id"]: s for s in steps}
    env = evaluate(spec)
    for st in steps:
        if st["op"] in ("mul", "div", "pct") and st["args"][0] in byid:
            m = byid[st["args"][0]]
            if m["op"] in ("add", "sub") and len(m["args"]) == 2 and use.get(m["id"]) == [st["id"]]:
                try:
                    x = env[m["args"][0]]
                    y = env[m["args"][1]]
                    v1, _ = apply_op(st["op"], [x[0]], [x[1]], st["param"], strict=False)
                    v = v1 + y[0] if m["op"] == "add" else v1 - y[0]
                except Invalid:
                    continue
                try:
                    env2 = dict(env)
                    env2[st["id"]] = (v, env[st["id"]][1])
                    started = False
                    for s2 in steps:
                        if s2["id"] == st["id"]:
                            started = True
                            continue
                        if started:
                            vv, uu = apply_op(s2["op"], [env2[a][0] for a in s2["args"]], [env2[a][1] for a in s2["args"]], s2["param"])
                            env2[s2["id"]] = (vv, uu)
                    add("precedence", env2[spec["final"]][0])
                except Invalid:
                    pass
    # unit slip at an intermediate node (a power of ten, or 60 for time): the slip enters the computation, so the wrong final value is
    # not a digit-shifted copy of the correct one
    has_time = spec["dim"] == "time" or any(s["op"] == "conv" for s in steps)
    nodes = [b["id"] for b in spec["base"]] + [s["id"] for s in steps[:-1]]
    for nid in nodes:
        for f in UNIT_SLIP_FACTORS:
            if f in (Decimal(60), Decimal(1) / Decimal(60)) and not has_time:
                continue
            add("unit_slip", _try_eval(spec, {nid: ("scale", f)}))
    return out


def choose_options(spec, k, rng, balancer, scope):
    """Pick k-1 wrong values of pairwise distinct trap types, correct-answer rank balanced. Returns [(value, trap_type)] or None."""
    ev = error_values(spec, rng)
    return pick_options_ranked(solve_value(spec)[0], ev, k, rng, balancer, scope, sim=dp_class)


# ------------------------------------------------------------------------------------------------
# AR-F2: threshold chosen so that the picked error model lands on the other side
# ------------------------------------------------------------------------------------------------
def _truth(cmp, x, thr):
    return {"ge": x >= thr, "le": x <= thr, "gt": x > thr, "lt": x < thr}[cmp]


def make_threshold(spec, want_yes, rng, balancer, scope):
    """Returns (cmp, thr, trap_type) or None. The wrong option's trap_type = the error model that flips the decision."""
    correct = solve_value(spec)[0]
    ev = error_values(spec, rng)
    types = [t for t, v in ev.items() if v]
    if not types:
        return None
    for _ in range(6):
        t = balancer.pick(scope, types)
        tv = rng.choice(ev[t])
        cmp = rng.choice(list(CMP_TEXT))
        cands = {correct, tv}
        lo, hi = min(correct, tv), max(correct, tv)
        for _i in range(6):
            cands.add(((lo + hi) / 2).quantize(D2))
        for z in (lo, hi):
            cands.add(z.quantize(Decimal(1)))
        cands |= {x + Decimal(d) for x in list(cands) for d in ("0.01", "-0.01")}
        good = [x for x in cands if x > 0 and is_2dp(x) and _truth(cmp, correct, x) == want_yes and _truth(cmp, tv, x) != want_yes]
        if not good:
            balancer.key_counts(scope)[t] -= 1
            continue
        ints = [x for x in good if x == x.to_integral_value()]
        thr = rng.choice(ints or good)
        return cmp, thr, t
    return None


def f2_answer(spec):
    correct = solve_value(spec)[0]
    return _truth(spec["f2"]["cmp"], correct, dec(spec["f2"]["thr"]))


# ------------------------------------------------------------------------------------------------
# AR-F3: worked solution with exactly one injected error
# ------------------------------------------------------------------------------------------------
def _line(spec, st, env, op, args, param, value, unit):
    return {"id": st["id"], "op": op, "args": list(args), "param": param, "value": value, "unit": unit}


def _fault_candidates(spec, j, rng):
    """Candidate faulty definitions for step index j: list of (kind, op, args, param, slip_delta)."""
    st = spec["steps"][j]
    out = []
    alt = {"add": "sub", "sub": "add", "min": "max", "max": "min", "mul": "div", "div": "mul"}
    if st["op"] in alt and not (st["op"] == "add" and len(st["args"]) == 3):
        out.append(("swap_op", alt[st["op"]], st["args"], st["param"], None))
    if st["op"] == "pct":
        out.append(("swap_op", "pct", st["args"], 100 - st["param"], None))
    if st["op"] in ("mul", "div"):
        for d in (-1, 1):
            p = st["param"] + d
            if p >= (1 if st["op"] == "mul" else 2):
                out.append(("count_off_by_one", st["op"], st["args"], p, None))
    if st["op"] == "split":
        out.append(("swap_op", "split", st["args"], {"r": st["param"]["r"], "which": 1 - st["param"]["which"]}, None))
    out.append(("omit_step", "skip", st["args"], None, None))
    for d in ("1", "-1", "10", "-10", "0.5", "-0.5"):
        out.append(("slip", st["op"], st["args"], st["param"], Decimal(d)))
    rng.shuffle(out)
    return out


def build_lines(spec, j, fault):
    """Worked-solution lines with the fault at step index j; later lines follow through from the wrong value.
    Returns list of line dicts or None when anything becomes invalid."""
    kind, fop, fargs, fparam, delta = fault
    env = {b["id"]: (dec(b["value"]), b["unit"]) for b in spec["base"]}
    lines = []
    for i, st in enumerate(spec["steps"]):
        op, args, param = st["op"], st["args"], st["param"]
        try:
            if i == j:
                if fop == "skip":
                    v, u = env[fargs[0]]
                    op, args, param = "skip", list(fargs), None
                else:
                    v, u = apply_op(fop, [env[a][0] for a in fargs], [env[a][1] for a in fargs], fparam, strict=(kind == "slip"))
                    if kind == "slip":
                        v = v + delta
                        if v < 0 or not is_2dp(v):
                            return None
                    op, args, param = fop, list(fargs), fparam
            else:
                v, u = apply_op(op, [env[a][0] for a in args], [env[a][1] for a in args], param)
        except Invalid:
            return None
        env[st["id"]] = (v, u)
        lines.append({"id": st["id"], "op": op, "args": args, "param": param, "value": v, "unit": u})
    return lines


def f3_correct_values(spec):
    env = evaluate(spec)
    return [env[s["id"]][0] for s in spec["steps"]]


def make_f3(spec, rng, j=None):
    """Inject exactly one error. Returns {'j': index, 'fault': (...), 'lines': [...]} or None."""
    n = len(spec["steps"])
    truth = f3_correct_values(spec)
    js = [j] if j is not None else rng.sample(range(n), n)
    for jj in js:
        for fault in _fault_candidates(spec, jj, rng):
            lines = build_lines(spec, jj, fault)
            if lines is None or lines[jj]["value"] == truth[jj]:
                continue
            return {"j": jj, "kind": fault[0], "lines": lines}
    return None


def expr_text(spec, line):
    nm = spec["names"]
    a = [nm[x] for x in line["args"]]
    op, p = line["op"], line["param"]
    if op == "add":
        return " + ".join(a)
    if op == "sub":
        return "%s - %s" % (a[0], a[1])
    if op == "mul":
        return "%s * %d" % (a[0], p)
    if op == "div":
        return "%s / %d" % (a[0], p)
    if op == "pct":
        return "%d%% of %s" % (p, a[0])
    if op == "split":
        return "share %d of %s split %d:%d" % (p["which"] + 1, a[0], p["r"][0], p["r"][1])
    if op in ("min", "max"):
        return "%s(%s)" % (op, ", ".join(a))
    if op == "conv":
        return "%s in %s" % (a[0], p)
    if op == "round":
        return "%s rounded %s" % (a[0], ROUND_TEXT[p])
    if op == "skip":
        return a[0]
    raise Invalid(op)


def first_wrong_line(spec, lines):
    """SOLVER A for AR-F3: recompute each line from its STATED inputs and the step DEFINITION; first mismatch (1-based)."""
    stated = {b["id"]: (dec(b["value"]), b["unit"]) for b in spec["base"]}
    for i, (st, ln) in enumerate(zip(spec["steps"], lines)):
        if ln["op"] != st["op"] or ln["args"] != st["args"] or ln["param"] != st["param"]:
            return i + 1
        try:
            v, u = apply_op(st["op"], [stated[a][0] for a in st["args"]], [stated[a][1] for a in st["args"]], st["param"])
        except Invalid:
            return i + 1
        if v != dec(ln["value"]):
            return i + 1
        stated[st["id"]] = (dec(ln["value"]), u)
    return None


def line_option_types(n, j):
    """candidate wrong lines with their relation to the true line (1-based j1)."""
    j1 = j + 1
    c = {}
    if j1 + 1 <= n:
        c["next_line"] = j1 + 1
    if j1 - 1 >= 1:
        c["prev_line"] = j1 - 1
    if j1 != 1:
        c["first_line"] = 1
    if j1 != n:
        c["last_line"] = n
    others = [x for x in range(1, n + 1) if x != j1 and x not in c.values()]
    if others:
        c["other_line"] = None   # drawn later
    return c, others


# ------------------------------------------------------------------------------------------------
# Rendering
# ------------------------------------------------------------------------------------------------
def qty_text(spec, value, unit):
    return unit_text(value, unit, spec.get("count_noun"))


def _step_values(spec, pool, rng, doc, st):
    nm = spec["names"]
    op = st["op"]
    out = (nm[st["id"]], "entity", "name")
    if op in ("add", "min", "max"):
        vals = {"out": out, "args": (join_names([nm[a] for a in st["args"]]), "entity", "name")}
    elif op == "sub":
        vals = {"out": out, "a": (nm[st["args"][0]], "entity", "name"), "b": (nm[st["args"][1]], "entity", "name")}
    elif op in ("mul", "div", "pct"):
        vals = {"out": out, "a": (nm[st["args"][0]], "entity", "name"), "p": (str(st["param"]), "number", "number")}
    elif op == "split":
        r = st["param"]["r"]
        vals = {"out": out, "a": (nm[st["args"][0]], "entity", "name"), "r1": (str(r[0]), "number", "number"),
                "r2": (str(r[1]), "number", "number"), "which": (["first", "second"][st["param"]["which"]], "entity", "rule")}
    elif op == "conv":
        vals = {"out": out, "a": (nm[st["args"][0]], "entity", "name"), "unit": (st["param"] + "s", "number", "unit")}
    elif op == "round":
        vals = {"out": out, "a": (nm[st["args"][0]], "entity", "name"), "rule": (ROUND_TEXT[st["param"]], "entity", "rule")}
    else:
        raise Invalid(op)
    return "ar.step." + op, vals


def render(spec, pool, widx, rng, domain, f3=None, carrier="TXT-PROSE"):
    """Returns (stem, spans). `widx` indexes the form's question wording; fact sentences use rng-chosen variants."""
    form = spec["form"]
    doc = Doc()
    doc.sentence(pool.get("scene." + domain, rng.randrange(1 << 20)), {})
    nm = spec["names"]
    idx = 0
    for b in spec["base"]:
        item_sep(doc, carrier, idx)
        idx += 1
        doc.sentence(pool.get("ar.base", rng.randrange(1 << 20)),
                     {"name": (nm[b["id"]], "entity", "name"), "qty": (qty_text(spec, dec(b["value"]), b["unit"]), "number", "quantity")})
    for st in spec["steps"]:
        item_sep(doc, carrier, idx)
        idx += 1
        key, vals = _step_values(spec, pool, rng, doc, st)
        doc.sentence(pool.get(key, rng.randrange(1 << 20)), vals)
    qkey = "q." + form
    if form == "AR-F1":
        qv = {"final": (nm[spec["final"]], "entity", "name")}
    elif form == "AR-F2":
        env = evaluate(spec)
        unit = env[spec["final"]][1]
        qv = {"final": (nm[spec["final"]], "entity", "name"), "cmp": (CMP_TEXT[spec["f2"]["cmp"]], "entity", "rule"),
              "thr": (qty_text(spec, dec(spec["f2"]["thr"]), unit), "number", "quantity")}
    elif form == "AR-F3":
        doc.sep("\n")
        doc.raw("Worked solution:")
        for i, ln in enumerate(f3["lines"]):
            doc.sep("\n")
            txt = "%s = %s = %s" % (nm[ln["id"]], expr_text(spec, ln), qty_text(spec, ln["value"], ln["unit"]))
            doc.sentence(pool.get("ar.f3.line", i + rng.randrange(1 << 8)), {"n": (str(i + 1), "number", "number"), "text": (txt, "number", "quantity")})
        doc.sep("\n")
        qv = {"n": (str(len(f3["lines"])), "number", "number")}
    else:
        raise Invalid(form)
    end_block(doc, carrier) if form != "AR-F3" else doc.sep("\n")
    doc.sentence(pool.get(qkey, widx), qv)
    return doc.text(), doc.spans


def answer_value(spec, f3=None):
    form = spec["form"]
    if form == "AR-F1":
        v, u = solve_value(spec)
        return {"value": fmt_num(v), "unit": u}
    if form == "AR-F2":
        return {"yes": f2_answer(spec)}
    return {"line": first_wrong_line(spec, f3["lines"])}


def option_text_value(spec, v):
    u = solve_value(spec)[1]
    return qty_text(spec, v, u)


# ------------------------------------------------------------------------------------------------
# Minimal pairs: edit one slot so that the answer changes
# ------------------------------------------------------------------------------------------------
def perturb_f1(spec, rng):
    """Edit one base value; returns a new spec whose final value differs, or None."""
    base = spec["base"][:]
    order = list(range(len(base)))
    rng.shuffle(order)
    old = solve_value(spec)[0]
    for i in order:
        for _ in range(8):
            cand = _rand_base(rng, base[i]["unit"]) if rng.random() < 0.3 else Decimal(max(2, int(dec(base[i]["value"])) + rng.choice([-7, -3, -2, -1, 1, 2, 3, 5, 9])))
            if cand == dec(base[i]["value"]) or cand <= 0:
                continue
            s2 = dict(spec)
            s2["base"] = [dict(b) for b in base]
            s2["base"][i]["value"] = fmt_num(cand)
            try:
                v, _ = solve_value(s2)
            except Invalid:
                continue
            if v != old and v > 0:
                s2.pop("f2", None)
                return s2
    return None


def perturb_f2(spec, rng, balancer, scope):
    """Same program, threshold moved across the final value so the answer flips."""
    want = not f2_answer(spec)
    r = make_threshold(spec, want, rng, balancer, scope)
    if r is None:
        return None
    cmp, thr, t = r
    s2 = dict(spec)
    s2["f2"] = {"cmp": cmp, "thr": fmt_num(thr), "trap_type": t}
    return s2
