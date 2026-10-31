"""F7 solver B (spec 4.2, 4.3): declarative constraint checking on the PARSED rubric and case, a different paradigm from
solver A's forward evaluation. z3 is not installed in this environment and F7 builders may not download packages, so
solver B states each level's membership condition as a constraint over the parsed facts and checks every candidate
value of `lvl` (a finite domain of K values): exactly one candidate must satisfy the constraints (the enumeration
analogue of "block the found value, re-check: UNSAT"). Values are compared as integers on each attribute's grid
(value / r), never as Fractions. Card proofs (totality, single value, monotonicity, reachability, coverage) run over
the grid regions that the parsed thresholds cut (every value between two adjacent thresholds is equivalent), which is
exhaustive over the grid domains of 2.2.
"""
from __future__ import annotations

import itertools
from fractions import Fraction


class SolveFail(Exception):
    pass


# ------------------------------------------------------------------------------------------------ domains
def domains(PC: dict, pack: dict) -> dict:
    """term -> {'kind', 'r', 'lo', 'hi'} from the pack's declared attributes (grid resolution and range)."""
    out = {}
    for t, fk in PC.get("bool_terms", {}).items():
        out[t] = {"kind": "bool"}
    for t in PC.get("listed", []):
        out[t] = {"kind": "bool"}
    for t, unit in PC.get("units", {}).items():
        a = next((a for a in pack["nums"] if a["term"] == t), None)
        if a is None:
            raise SolveFail("numeric term not in pack")
        out[t] = {"kind": "num", "r": a["r"], "lo": a["lo"], "hi": a["hi"]}
    if PC.get("qty_term"):
        a = next((a for a in pack["nums"] if a["term"] == PC["qty_term"]), None)
        if a is None:
            raise SolveFail("quantity not in pack")
        out[PC["qty_term"]] = {"kind": "num", "r": a["r"], "lo": a["lo"], "hi": a["hi"]}
    for t in PC.get("date_terms", []):
        import datetime as _dt
        start = (_dt.date.fromisoformat(pack["date_start"]) - _dt.date(2000, 1, 1)).days
        out[t] = {"kind": "date", "r": 1, "lo": start, "hi": PC.get("R", start + pack["date_span"])}
    for t in PC.get("ord_terms", []):
        out[t] = {"kind": "ord", "r": 1, "lo": 0, "hi": len(PC.get("ranks") or []) - 1}
    return out


def _q(x, r) -> int:
    """grid index of value x (exact; refuses off-grid values)."""
    k = Fraction(x) / Fraction(r)
    if k.denominator != 1:
        raise SolveFail("value off its grid")
    return int(k)


# ------------------------------------------------------------------------------------------------ atoms
def atom_holds(a: dict, val, dom: dict, ranks) -> bool:
    k = a["kind"]
    if k == "bool":
        return bool(val) if a["op"] == "present" else not bool(val)
    if k == "ord":
        t = ranks.index(a["rank"])
        x = int(val)
    elif k == "date":
        if a["op"] == "within":
            return int(a["t"]) <= int(val) and int(val) - int(a["t"]) <= int(a["N"])
        t, x = int(a["t"]), int(val)
    else:
        t, x = _q(a["t"], dom["r"]), _q(val, dom["r"])
    d = x - t
    return {">=": d >= 0, ">": d > 0, "<=": d <= 0, "<": d < 0}[a["op"]]


def crit_holds(c: dict, env: dict, D: dict, ranks) -> bool:
    t = c["t"]
    if t == "atom":
        a = c["a"]
        return atom_holds(a, env[a["term"]], D[a["term"]], ranks)
    if t in ("and", "allof"):
        res = [crit_holds(p, env, D, ranks) for p in c["parts"]]
        return min(res)
    if t in ("or", "anyof"):
        res = [crit_holds(p, env, D, ranks) for p in c["parts"]]
        return max(res)
    if t == "unless":
        return crit_holds(c["a"], env, D, ranks) and not atom_holds(c["b"], env[c["b"]["term"]], D[c["b"]["term"]], ranks)
    if t == "onlyif":
        return crit_holds(c["main"], env, D, ranks) and atom_holds(c["c"], env[c["c"]["term"]], D[c["c"]["term"]], ranks)
    raise SolveFail(t)


# ------------------------------------------------------------------------------------------------ level constraints
def mode_candidates(PC: dict, env: dict, D: dict) -> list[int]:
    """Every lvl in 0..K-1 whose membership constraint holds under the card's mode."""
    K = PC["K"]
    ranks = PC.get("ranks") or []
    mode = PC["mode"]
    out = []
    if mode == "ladder":
        h = {k: crit_holds(PC["crits"][k], env, D, ranks) for k in range(1, K)}
        for l in range(K):
            if all(h[j] for j in range(1, l + 1)) and (l == K - 1 or not h[l + 1]):
                out.append(l)
    elif mode == "highest":
        h = {k: crit_holds(PC["crits"][k], env, D, ranks) for k in range(1, K)}
        for l in range(K):
            if (l == 0 or h[l]) and not any(h[j] for j in range(l + 1, K)):
                out.append(l)
    elif mode in ("count", "points"):
        tot = 0
        for f in PC["listed"]:
            if env.get(f):
                tot += PC["weights"][f] if mode == "points" else 1
        for l in range(K):
            lo, hi = PC["bands"][l]
            if (lo is None or tot >= lo) and (hi is None or tot <= hi):
                out.append(l)
    elif mode == "cut":
        x = env[PC["qty_term"]]
        for l in range(K):
            rg = PC["ranges"][l]
            if _in_range(x, rg):
                out.append(l)
    elif mode == "grid":
        rows = PC["grid"]
        ok = {k: all(atom_holds(a, env[a["term"]], D[a["term"]], ranks) for a in rows[k]) for k in range(1, K)}
        for l in range(K):
            if (l == 0 or ok[l]) and not any(ok[j] for j in range(l + 1, K)):
                out.append(l)
    return out


def _in_range(x, rg) -> bool:
    x = Fraction(x)
    kind = rg[0]
    if kind == "int":
        return rg[1] <= x <= rg[2]
    if kind == "ge":
        return x >= rg[1]
    if kind == "le":
        return x <= rg[1]
    _, lo, lo_in, hi, hi_in = rg
    if lo is not None and not (x >= lo if lo_in else x > lo):
        return False
    if hi is not None and not (x <= hi if hi_in else x < hi):
        return False
    return True


def final_candidates(PC: dict, env: dict, D: dict) -> list[int]:
    K = PC["K"]
    ranks = PC.get("ranks") or []
    ms = mode_candidates(PC, env, D)
    ovs = PC.get("overrides", [])
    if not ovs:
        return ms
    fl = next((o for o in ovs if o["type"] == "floor"), None)
    cp = next((o for o in ovs if o["type"] == "cap"), None)
    ff = bool(fl) and crit_holds(fl["cond"], env, D, ranks)
    cf = bool(cp) and crit_holds(cp["cond"], env, D, ranks)
    out = []
    for l in range(K):
        for m in ms:
            if ff and cf:
                okv = l == (cp["m"] if PC["winner"] == "cap" else fl["m"])
            elif ff:
                okv = l >= fl["m"] and (l == m or (l == fl["m"] and m < fl["m"]))
            elif cf:
                okv = l <= cp["m"] and (l == m or (l == cp["m"] and m > cp["m"]))
            else:
                okv = l == m
            if okv:
                out.append(l)
                break
    return out


def env_from_case(PC: dict, case: dict, D: dict) -> dict:
    env = {}
    for t, d in D.items():
        if d["kind"] == "bool":
            env[t] = bool(case["presence"].get(t, False))  # unmentioned (C1), missing (C15), plan (C3), partial (C20)
        else:
            if t not in case["values"]:
                raise SolveFail(f"value not stated: {t}")
            env[t] = case["values"][t]
            if d["kind"] in ("num",):
                _q(env[t], d["r"])
                if not (d["lo"] <= env[t] <= d["hi"]):
                    raise SolveFail("value outside its domain")
    return env


def solve_b(PC: dict, case: dict, pack: dict) -> int:
    D = domains(PC, pack)
    env = env_from_case(PC, case, D)
    c = final_candidates(PC, env, D)
    if len(c) != 1:
        raise SolveFail(f"{len(c)} levels satisfy the constraints")
    return c[0]


# ------------------------------------------------------------------------------------------------ card proofs (4.3)
def _all_atoms(PC):
    out = []

    def walk(c):
        t = c["t"]
        if t == "atom":
            out.append(c["a"])
        elif t in ("and", "or", "allof", "anyof"):
            for p in c["parts"]:
                walk(p)
        elif t == "unless":
            walk(c["a"])
            out.append(c["b"])
        elif t == "onlyif":
            walk(c["main"])
            out.append(c["c"])
    for c in PC.get("crits", {}).values():
        walk(c)
    for o in PC.get("overrides", []):
        walk(o["cond"])
    for row in PC.get("grid", {}).values():
        out += row
    return out


def representatives(PC: dict, D: dict) -> dict:
    ranks = PC.get("ranks") or []
    reps = {}
    ths = {}
    for a in _all_atoms(PC):
        if a["kind"] in ("num",):
            ths.setdefault(a["term"], set()).add(Fraction(a["t"]))
        elif a["kind"] == "date":
            ths.setdefault(a["term"], set()).add(int(a["t"]))
            if a["op"] == "within":
                ths[a["term"]].add(int(a["t"]) + int(a["N"]))
    if PC["mode"] == "cut":
        q = PC["qty_term"]
        s = set()
        rs = list(PC["ranges"].values())
        integer = all(rg[0] in ("int", "ge", "le") for rg in rs)
        if integer:
            lows = sorted((rg[1] if rg[0] in ("int", "ge") else None) for rg in rs if rg[0] != "le")
            smallest = min((rg[1] for rg in rs if rg[0] in ("int", "ge")), default=None)
            has_le = any(rg[0] == "le" for rg in rs)
            for rg in rs:
                if rg[0] in ("int", "ge") and (has_le or rg[1] != smallest):
                    s.add(Fraction(rg[1]))
                if rg[0] == "le":
                    s.add(Fraction(rg[1]) + 1)
        else:
            for rg in rs:
                for x in rg[1:]:
                    if isinstance(x, Fraction):
                        s.add(x)
        ths[q] = s
    for t, d in D.items():
        if d["kind"] == "bool":
            reps[t] = [False, True]
        elif d["kind"] == "ord":
            reps[t] = list(range(len(ranks)))
        else:
            r = Fraction(d["r"])
            vals = {Fraction(d["lo"]), Fraction(d["hi"])}
            for x in ths.get(t, []):
                for dd in (-1, 0, 1):
                    vals.add(Fraction(x) + dd * r)
            reps[t] = sorted(v for v in vals if Fraction(d["lo"]) <= v <= Fraction(d["hi"]))
    return reps, ths


def prove_card(PC: dict, pack: dict, *, spacing: int = 2, cut_spacing: int = 4, max_regions: int = 400000) -> dict:
    """Totality, single value, monotonicity (some direction per attribute), reachability of every level (and of every
    (firing pattern, level) pair on override cards), threshold spacing and band contiguity. Raises SolveFail."""
    D = domains(PC, pack)
    reps, ths = representatives(PC, D)
    terms = sorted(D)
    sizes = [len(reps[t]) for t in terms]
    total = 1
    for s in sizes:
        total *= s
    if total > max_regions:
        raise SolveFail(f"too many regions ({total})")
    K = PC["K"]
    # spacing (2.2, T07)
    for t, s in ths.items():
        r = Fraction(D[t].get("r", 1))
        xs = sorted(s)
        need = cut_spacing if PC["mode"] == "cut" else spacing
        for a, b in zip(xs, xs[1:]):
            if (b - a) / r < need:
                raise SolveFail("thresholds closer than the spacing rule")
    if PC["mode"] in ("count", "points"):
        bs = sorted(((lo if lo is not None else -1, hi) for lo, hi in PC["bands"].values()), key=lambda x: x[0])
        for (lo1, hi1), (lo2, hi2) in zip(bs, bs[1:]):
            if hi1 is None or lo2 != hi1 + 1:
                raise SolveFail("bands not contiguous")
    level_of = {}
    reach = set()
    pat_reach = set()
    ranks = PC.get("ranks") or []
    fl = next((o for o in PC.get("overrides", []) if o["type"] == "floor"), None)
    cp = next((o for o in PC.get("overrides", []) if o["type"] == "cap"), None)
    for combo in itertools.product(*[reps[t] for t in terms]):
        env = dict(zip(terms, combo))
        c = final_candidates(PC, env, D)
        if len(c) != 1:
            raise SolveFail(f"not total / single valued ({len(c)} levels)")
        level_of[combo] = c[0]
        reach.add(c[0])
        if fl or cp:
            ff = bool(fl) and crit_holds(fl["cond"], env, D, ranks)
            cf = bool(cp) and crit_holds(cp["cond"], env, D, ranks)
            pat_reach.add(("both" if ff and cf else "floor" if ff else "cap" if cf else "none", c[0]))
    if reach != set(range(K)):
        raise SolveFail(f"unreachable levels {sorted(set(range(K)) - reach)}")
    # monotonicity: for each attribute there is a direction in which the level never decreases
    for i, t in enumerate(terms):
        ok_up = ok_down = True
        others = [reps[u] for j, u in enumerate(terms) if j != i]
        for rest in itertools.product(*others):
            seq = []
            for x in reps[t]:
                combo = list(rest)
                combo.insert(i, x)
                seq.append(level_of[tuple(combo)])
            if any(b < a for a, b in zip(seq, seq[1:])):
                ok_up = False
            if any(b > a for a, b in zip(seq, seq[1:])):
                ok_down = False
            if not ok_up and not ok_down:
                raise SolveFail(f"level not monotone in {t}")
    need_pairs = set()
    if fl or cp:
        for l in range(K):
            need_pairs.add(("none", l))
        if fl:
            for l in range(fl["m"], K):
                need_pairs.add(("floor", l))
        if cp:
            for l in range(0, cp["m"] + 1):
                need_pairs.add(("cap", l))
        if fl and cp:
            need_pairs.add(("both", cp["m"] if PC["winner"] == "cap" else fl["m"]))
        miss = need_pairs - pat_reach
        if miss:
            raise SolveFail(f"unreachable (pattern, level) pairs {sorted(miss)[:3]}")
    return {"regions": total, "levels": K}
