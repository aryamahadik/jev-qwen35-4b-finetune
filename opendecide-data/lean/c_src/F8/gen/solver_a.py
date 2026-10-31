"""Solver A: the generator's forward evaluator on the structure object, in exact arithmetic (G0 spec 3).

Structure S (JSON-able; Fractions for numbers; built by the samplers, re-built by the G3 parser):
  form   yn_thr | yn_act | bin | tier | mat | rank_top | rank_order | dec | pred | inv
  sub    points | bayes | expected | rank
  world  closed | open
  mode   loss | net | None           (sign mode, SEM-20)
  q      the quantity: {"k": "score"} | {"k": "post", "h": i} | {"k": "el"} | {"k": "tec"} | {"k": "ev"} |
         {"k": "en"} | {"k": "chance"} | {"k": "risk", "def": "el" | "score" | "chance"}
  case   index of the asked entity (YN, BIN, TIER, MAT, PRED) or None
  ents   entities: [{"id", "pts", "bay", "outs", "cost", "en", "ch", "mat"}] (only the keys the sub-skill uses)
  rules  card rules the row uses: "scorecard" {"lines", "F", "M"}, "cuts", "tiers", "only_if" {tier: cond},
         "overrides" [{"cond", "tier"}], "bins", "bin_conv" lo|hi, "mat", "arules" {action: cond}, "inv"
  thr    yn_thr {"op", "T", "neg"};  act  yn_act {"action", "neg"};  hl  rank_top "high" | "low"
Answers: yn -> bool; bin / tier / mat / pred -> index; rank_top / dec / inv -> entity index or "CBD" / "NOTA";
rank_order -> tuple of entity indices (highest first). solve() returns {"ans", "det", "set"} (+ "post" on PRED).
Conventions `cv` switch one alternative reading at a time (CI lint, 3.1) or one named error (E1-E16, distractors).
"""
from __future__ import annotations

import copy
import itertools
from fractions import Fraction as Fr

DEFAULT_CV = {
    "unless": "std", "or": "std", "xor1": "std", "or_count": "once", "clamp": "final", "only_if": "std",
    "override": "std", "cut_edge": "std", "bin_edge": "std", "lvl_edge": "std", "cmp": "std", "cmp_class": None,
    "unstated": "absent", "remainder": "std", "own_cost": "std", "post": "std", "rank_by": "std", "grid": "std",
    "tie": "std", "impact": "std", "range_open": False, "groups_sum": False, "nr_zero": False, "abstain_any": False,
    "inv_open": "std", "en": "std", "risk": "std", "tier_by_name": False, "sem01_named": False, "net": "std",
    "el_max": False,
}


class Undetermined(Exception):
    pass


def CV(**kw) -> dict:
    d = dict(DEFAULT_CV)
    for k in kw:
        if k not in DEFAULT_CV:
            raise KeyError(k)
    d.update(kw)
    return d


# ---------------------------------------------------------------------------------------------------- comparisons
SWAP = {">": ">=", ">=": ">", "<": "<=", "<=": "<"}


def cmp(a: Fr, op: str, b: Fr, cv: dict | None = None, cls: str | None = None) -> bool:
    if cv and cv.get("cmp") == "swap" and cv.get("cmp_class") in (None, cls):
        op = SWAP[op]
    if op == ">":
        return a > b
    if op == ">=":
        return a >= b
    if op == "<":
        return a < b
    if op == "<=":
        return a <= b
    raise ValueError(op)


# ---------------------------------------------------------------------------------------------------- conditions
def part_holds(part: dict, ent: dict, S: dict, cv: dict) -> bool:
    t = part["t"]
    if t == "bool":
        v = ent["pts"]["b"].get(part["f"], False)
        if v is None:
            raise Undetermined("bool unknown")
        return bool(v)
    if t == "cat":
        return ent["pts"]["c"][part["name"]] == part["v"]
    if t == "amt":
        a = ent["pts"]["a"][part["name"]]
        if a is None:
            raise Undetermined("amount unknown")
        return cmp(a, part["op"], part["v"], cv, "amt")
    if t == "q":
        val = quantity(S, ent, part["q"], cv)
        return cmp(val, part["op"], part["v"], cv, "q")
    raise ValueError(t)


def cond_holds(cond: dict, ent: dict, S: dict, cv: dict) -> bool:
    vals = [part_holds(p, ent, S, cv) for p in cond["parts"]]
    conn = cond["conn"]
    n = sum(vals)
    if conn == "and":
        return all(vals)
    if conn == "or":
        if cv["or"] == "xor":
            return n == 1
        if cv["or"] == "parity":
            return n % 2 == 1
        return n >= 1
    if conn == "xor1":
        m = cv["xor1"]
        if m == "inclusive":
            return n >= 1
        if m == "atmost1":
            return n <= 1
        if m == "parity":
            return n % 2 == 1
        return n == 1
    raise ValueError(conn)


# ---------------------------------------------------------------------------------------------------- points
def _names_unstated(cond: dict, ent: dict) -> bool:
    st = ent["pts"].get("stated", {})
    return any(p["t"] == "bool" and not st.get(p["f"], True) for p in cond["parts"])


def line_points(line: dict, ent: dict, S: dict, cv: dict) -> int:
    c = line["cond"]
    if cv["sem01_named"] and (_names_unstated(c, ent) or (line.get("unless") and _names_unstated(line["unless"], ent))):
        return 0
    holds = cond_holds(c, ent, S, cv)
    k = line["pts"]
    if cv["or_count"] == "per_part" and c["conn"] == "or" and holds:
        k = k * sum(part_holds(p, ent, S, cv) for p in c["parts"])
    u = line.get("unless")
    if not u:
        return k if holds else 0
    if cv["unless"] == "ignore":
        return k if holds else 0
    uh = cond_holds(u, ent, S, cv)
    if cv["unless"] == "iff":
        return k if not uh else 0
    return k if (holds and not uh) else 0


def score(ent: dict, S: dict, cv: dict) -> int:
    sc = S["rules"]["scorecard"]
    F, M = sc["F"], sc["M"]
    if cv["clamp"] == "running":
        tot = 0
        for ln in sc["lines"]:
            tot = min(M, max(F, tot + line_points(ln, ent, S, cv)))
        return tot
    tot = sum(line_points(ln, ent, S, cv) for ln in sc["lines"])
    if cv["clamp"] == "none":
        return tot
    return min(M, max(F, tot))


def tier_by_score(s: int, cuts: list, cv: dict) -> int:
    k = 0
    for i, c in enumerate(cuts):
        if (s > c) if cv["cut_edge"] == "lower" else (s >= c):
            k = i + 1
    return k


def tier(ent: dict, S: dict, cv: dict):
    """(tier index, tier_step) by SEM-15; tier_step in {None, 'only_if', 'override'} (XF08, F8-R3-C1)."""
    R = S["rules"]
    s = score(ent, S, cv)
    t0 = tier_by_score(s, R["cuts"], cv)
    only_if = {int(k): v for k, v in (R.get("only_if") or {}).items()}
    order = list(range(len(R["tiers"])))
    if cv["tier_by_name"] and R.get("name_rank"):
        order = sorted(order, key=lambda i: R["name_rank"][i])
    pos = {t: i for i, t in enumerate(order)}

    def meets(t):
        c = only_if.get(t)
        return True if c is None else cond_holds(c, ent, S, cv)
    t, step = t0, None
    mode = cv["only_if"]
    if mode != "ignore" and only_if:
        if mode == "sufficient":
            ok = [tt for tt in only_if if cond_holds(only_if[tt], ent, S, cv)]
            if ok:
                t = max(ok + [t], key=lambda x: pos[x])
        elif not meets(t):
            if mode == "one_down":
                t = order[max(0, pos[t] - 1)]
            elif mode == "skip_to_no_limit":
                lower = [tt for tt in order[:pos[t]] if tt not in only_if]
                t = lower[-1] if lower else order[0]
            elif mode == "bottom":
                t = order[0]
            else:
                lower = [tt for tt in order[:pos[t]] if meets(tt)]
                t = lower[-1] if lower else order[0]
    if t != t0:
        step = "only_if"
    ovs = R.get("overrides") or []
    if cv["override"] != "ignore" and ovs:
        fired = [o["tier"] for o in ovs if cond_holds(o["cond"], ent, S, cv)]
        if fired:
            if cv["override"] == "lowest":
                nt = min(fired, key=lambda x: pos[x])
            elif cv["override"] == "first":
                nt = fired[0]
            else:
                nt = max(fired, key=lambda x: pos[x])
            if mode == "limits_override" and not meets(nt):
                lower = [tt for tt in order[:pos[nt]] if meets(tt)]
                nt = lower[-1] if lower else order[0]
            if nt != t:
                step = "override"
            t = nt
    return t, step


# ---------------------------------------------------------------------------------------------------- bayes
def post_vec(ent: dict, cv: dict) -> list:
    """Posterior over the hypotheses given every stated sign (SEM-30), or a named-error reading of it."""
    bay = ent["bay"]
    k = len(bay["hyps"])
    form = bay["form"]
    mode = cv["post"]
    if form == "counts":
        sign = bay["signs"][0]
        col = 0 if bay["sig"][sign] else 1
        cnt = [bay["cnt"][sign][j][col] for j in range(k)]
        tot_h = [bay["cnt"][sign][j][0] + bay["cnt"][sign][j][1] for j in range(k)]
        N = sum(tot_h)
        if mode == "prior":
            return [Fr(t, N) for t in tot_h]
        lik = [Fr(cnt[j], tot_h[j]) for j in range(k)]
        if mode == "inverse":
            return lik
        if mode == "neglect":
            s = sum(lik)
            if s == 0:
                raise Undetermined("zero")
            return [x / s for x in lik]
        if mode in ("joint", "joint_as_cond"):
            return [Fr(c, N) for c in cnt]
        s = sum(cnt)
        if s == 0:
            raise Undetermined("no cases with the evidence")
        return [Fr(c, s) for c in cnt]
    if form == "nE":
        sign = bay["signs"][0]
        a = list(bay["ne"][sign])
        n = sum(a)
        if mode == "prior":
            raise Undetermined("no base rates on an evidence-group row")
        if n == 0:
            raise Undetermined("empty evidence group")
        return [Fr(x, n) for x in a]
    if form == "joint":
        sign = bay["signs"][0]
        J = list(bay["joint"][sign])
        if any(x is None for x in J):
            raise Undetermined("joint unknown")
        if mode in ("joint_as_cond", "joint", "inverse"):
            return J
        if mode == "prior":
            raise Undetermined("no base rates on a joint-share row")
        s = sum(J)
        if s == 0:
            raise Undetermined("zero")
        return [x / s for x in J]
    base = list(bay["base"])
    if mode == "prior":
        return base
    lik = [Fr(1)] * k
    for sign in bay["signs"]:
        shown = bay["sig"][sign]
        for j in range(k):
            p = bay["lik"][sign][j]
            if p is None:
                raise Undetermined("lik unknown")
            lik[j] = lik[j] * (p if shown else 1 - p)
    if mode == "inverse":
        return lik
    if mode == "neglect":
        s = sum(lik)
        if s == 0:
            raise Undetermined("zero")
        return [x / s for x in lik]
    num = [b * l for b, l in zip(base, lik)]
    if mode == "joint":
        return num
    s = sum(num)
    if s == 0:
        raise Undetermined("P(E) = 0")
    return [x / s for x in num]


# ---------------------------------------------------------------------------------------------------- expected
def expected(ent: dict, kind: str, S: dict, cv: dict) -> Fr:
    if not ent.get("outs") and ent.get("ch") is not None and ent["ch"].get("amt") is not None:
        if ent["ch"]["p"] is None:
            raise Undetermined("chance unknown")
        return ent["ch"]["p"] * ent["ch"]["amt"]
    outs = ent["outs"]
    for o in outs:
        if o["p"] is None or o["a"] is None:
            raise Undetermined("outcome unknown")
    tot = sum(o["p"] for o in outs)
    if tot > 1:
        raise ValueError("listed chances above 1")
    scale = Fr(1)
    if cv["remainder"] == "rescale" and 0 < tot < 1:
        scale = 1 / tot
    if cv["el_max"]:
        el = max(o["a"] for o in outs)
    else:
        el = sum(o["p"] * scale * o["a"] for o in outs)
    if cv["net"] == "flip":
        el = -el
    if kind in ("el", "ev"):
        return el
    if kind == "tec":
        c = ent.get("cost")
        if c is None:
            raise Undetermined("own cost unknown")
        m = cv["own_cost"]
        if m == "exclude":
            return el
        if m == "twice":
            return el + 2 * c
        if m == "on_event":
            return el + c * tot
        return el + c
    raise ValueError(kind)


# ---------------------------------------------------------------------------------------------------- quantity
def _chance_of(ent: dict) -> Fr:
    if ent.get("ch") is not None:
        p = ent["ch"]["p"]
        if p is None:
            raise Undetermined("chance unknown")
        return p
    if ent.get("outs"):
        ps = [o["p"] for o in ent["outs"]]
        if any(p is None for p in ps):
            raise Undetermined("chance unknown")
        return sum(ps)
    raise Undetermined("no chance")


def _amount_of(S: dict, ent: dict) -> Fr:
    if S["form"] == "dec":
        return ent["cost"]
    if ent.get("outs"):
        if any(o["a"] is None for o in ent["outs"]):
            raise Undetermined("amount unknown")
        return max(o["a"] for o in ent["outs"])
    if ent.get("ch") is not None and ent["ch"].get("amt") is not None:
        return ent["ch"]["amt"]
    raise Undetermined("no amount")


def quantity(S: dict, ent: dict, q: dict, cv: dict, top: bool = False) -> Fr:
    if top and cv["rank_by"] != "std" and S["form"] in ("rank_top", "rank_order", "dec"):
        return _chance_of(ent) if cv["rank_by"] == "chance" else _amount_of(S, ent)
    k = q["k"]
    if k == "risk":
        d = q["def"] if cv["risk"] == "std" else cv["risk"]
        if d == "chance":
            return _chance_of(ent)
        if d == "amount":
            return _amount_of(S, ent)
        k = d
    if k == "score":
        return Fr(score(ent, S, cv))
    if k == "post":
        return post_vec(ent, cv)[q["h"]]
    if k in ("el", "tec", "ev"):
        return expected(ent, k, S, cv)
    if k == "en":
        e = ent["en"]
        if e["p"] is None:
            raise Undetermined("en unknown")
        if cv["en"] == "at_least_one":
            return 1 - (1 - e["p"]) ** e["n"]
        return e["n"] * e["p"]
    if k == "chance":
        return _chance_of(ent)
    raise ValueError(k)


# ---------------------------------------------------------------------------------------------------- bins, matrix
def level_of(v: Fr, edges: list, conv: str, flip: bool = False) -> int:
    """Index of the range holding v; edges are the interior edges e1 < ... < e(K-1). conv lo: [a, b); hi: (a, b]."""
    c = conv
    if flip:
        c = "hi" if conv == "lo" else "lo"
    k = 0
    for i, e in enumerate(edges):
        if (v >= e) if c == "lo" else (v > e):
            k = i + 1
    return k


def bin_of(p: Fr, edges: list, conv: str, cv: dict) -> int:
    return level_of(p, edges, conv, cv["bin_edge"] == "other")


def mat_levels(ent: dict, S: dict, cv: dict):
    m = S["rules"]["mat"]
    mm = ent["mat"]
    lik = mm["lik"]
    if m["impact"] == "loss":
        imp = lik * mm["amt"] if cv["impact"] == "expected" else mm["amt"]
    else:
        imp = mm["amt"] if cv["impact"] == "amount" else mm["p"] * mm["amt"]
    flip = cv["lvl_edge"] == "other"
    li = level_of(lik, m["lik_edges"], m["lik_conv"], flip)
    ii = level_of(imp, m["imp_edges"], "lo", flip)
    return li, ii


def mat_rating(ent: dict, S: dict, cv: dict) -> int:
    li, ii = mat_levels(ent, S, cv)
    g = S["rules"]["mat"]["grid"]
    if cv["grid"] == "transposed":
        if ii >= len(g) or li >= len(g[0]):
            raise Undetermined("transposed grid out of range")
        return g[ii][li]
    return g[li][ii]


# ---------------------------------------------------------------------------------------------------- answers
def id_num(e: dict) -> int:
    return int(e["id"].rsplit("-", 1)[-1])


def argbest(vals: list, ents: list, high: bool, cv: dict):
    best = max(vals) if high else min(vals)
    idx = [i for i, v in enumerate(vals) if v == best]
    if len(idx) == 1:
        return idx[0]
    t = cv["tie"]
    if t == "first":
        return idx[0]
    if t == "last":
        return idx[-1]
    if t == "higher_id":
        return max(idx, key=lambda i: id_num(ents[i]))
    if t == "none":
        raise Undetermined("tie")
    return min(idx, key=lambda i: id_num(ents[i]))


def inv_meets(S: dict, ent: dict, cv: dict) -> bool:
    r = S["rules"]["inv"]
    if r["kind"] == "q":
        v = quantity(S, ent, r["q"], cv)
        return cmp(v, r["op"], r["v"], cv, "inv")
    return cond_holds(S["rules"]["arules"][r["action"]], ent, S, cv)


def closed_answer(S: dict, cv: dict):
    f = S["form"]
    ents = S["ents"]
    if f == "yn_thr":
        v = quantity(S, ents[S["case"]], S["q"], cv, top=True)
        th = S["thr"]
        a = cmp(v, th["op"], th["T"], cv, "thr")
        return a if th["neg"] % 2 == 0 else (not a)
    if f == "yn_act":
        a = cond_holds(S["rules"]["arules"][S["act"]["action"]], ents[S["case"]], S, cv)
        return a if S["act"]["neg"] % 2 == 0 else (not a)
    if f == "bin":
        p = quantity(S, ents[S["case"]], S["q"], cv, top=True)
        return bin_of(p, S["rules"]["bins"], S["rules"]["bin_conv"], cv)
    if f == "tier":
        return tier(ents[S["case"]], S, cv)[0]
    if f == "mat":
        return mat_rating(ents[S["case"]], S, cv)
    if f == "pred":
        pv = post_vec(ents[S["case"]], cv)
        best = max(pv)
        idx = [i for i, v in enumerate(pv) if v == best]
        if len(idx) > 1:
            raise Undetermined("pred tie")
        return idx[0]
    if f in ("rank_top", "dec"):
        vals = [quantity(S, e, S["q"], cv, top=True) for e in ents]
        high = (S.get("hl") == "high") if f == "rank_top" else False
        return argbest(vals, ents, high, cv)
    if f == "rank_order":
        vals = [quantity(S, e, S["q"], cv, top=True) for e in ents]
        if len(set(vals)) != len(vals) and cv["tie"] == "std":
            raise Undetermined("rank_order tie")
        return tuple(sorted(range(len(ents)), key=lambda i: (-vals[i], id_num(ents[i]))))
    if f == "inv":
        meet = [i for i, e in enumerate(ents) if inv_meets(S, e, cv)]
        if len(meet) == 1:
            return meet[0]
        if not meet:
            return "NOTA"
        return ("MULTI",) + tuple(meet)
    raise ValueError(f)


# ---------------------------------------------------------------------------------------------------- open world
def unknown_slots(S: dict, cv: dict | None = None) -> list:
    """[(path, domain)] for every unknown: Booleans [True, False]; numbers [lo, hi] (closed ranges, both ends)."""
    out = []
    unstated = cv is not None and cv.get("unstated") == "unknown"
    for i, e in enumerate(S["ents"]):
        pts = e.get("pts")
        if pts:
            for f, v in pts["b"].items():
                if v is None or (unstated and not pts.get("stated", {}).get(f, True)):
                    out.append((("pts", i, "b", f), [True, False]))
            for a, v in (pts.get("a") or {}).items():
                if v is None:
                    out.append((("pts", i, "a", a), list(pts["arng"][a])))
        bay = e.get("bay")
        if bay and bay.get("lik"):
            for s, vec in bay["lik"].items():
                for j, v in enumerate(vec):
                    if v is None:
                        lo, hi = bay["rng"][f"{s}|{j}"]
                        if cv is not None and cv.get("groups_sum"):
                            others = sum(x for x in vec if x is not None)
                            hi = min(hi, 1 - others)
                        out.append((("lik", i, s, j), [lo, hi]))
        for k, o in enumerate(e.get("outs") or []):
            if o["p"] is None:
                out.append((("outp", i, k), list(o["prng"])))
            if o["a"] is None:
                out.append((("outa", i, k), list(o["arng"])))
        if e.get("ch") is not None and e["ch"]["p"] is None:
            out.append((("ch", i), list(e["ch"]["rng"])))
    return out


def assign(S: dict, slots: list, values: tuple) -> dict:
    """A copy of S with the unknowns filled (only the touched entities are copied; rules are shared, read-only)."""
    T = dict(S)
    T["ents"] = list(S["ents"])
    for i in {path[1] for path, _ in slots}:
        T["ents"][i] = copy.deepcopy(S["ents"][i])
    for (path, _), v in zip(slots, values):
        kind = path[0]
        e = T["ents"][path[1]]
        if kind == "pts":
            e["pts"][path[2]][path[3]] = v
        elif kind == "lik":
            e["bay"]["lik"][path[2]][path[3]] = v
        elif kind == "outp":
            e["outs"][path[2]]["p"] = v
        elif kind == "outa":
            e["outs"][path[2]]["a"] = v
        elif kind == "ch":
            e["ch"]["p"] = v
    T["world"] = "assigned"
    return T


def _domains(slots: list, cv: dict) -> list:
    doms = []
    for path, dom in slots:
        if path[0] == "pts" and path[2] == "b":
            doms.append(dom)
            continue
        lo, hi = dom
        if cv["range_open"]:
            eps = (hi - lo) / 1000 if hi > lo else Fr(0)
            doms.append([lo + eps, hi - eps])
        else:
            doms.append([lo, hi])
    return doms


def _answer_safe(T: dict, cv: dict):
    try:
        return closed_answer(T, cv)
    except Undetermined:
        return "UNDEF"


def solve(S: dict, cv: dict | None = None) -> dict:
    cv = cv or CV()
    slots = unknown_slots(S, cv)
    if not slots:
        a = closed_answer(S, cv)
        out = {"ans": a, "det": True, "set": [a]}
        if S["form"] == "pred":
            out["post"] = post_vec(S["ents"][S["case"]], cv)
        return out
    if cv["nr_zero"]:
        vals = tuple((False if (p[0] == "pts" and p[2] == "b") else Fr(0)) for p, dom in slots)
        T = assign(S, slots, vals)
        a = _answer_safe(T, cv)
        return {"ans": a, "det": a != "UNDEF", "set": [a]}
    if cv["abstain_any"] and S["world"] == "open":
        return {"ans": "CBD", "det": False, "set": []}
    doms = _domains(slots, cv)
    if S["form"] == "inv":
        return _inv_open(S, slots, doms, cv)
    if S["form"] in ("rank_top", "dec") and len({p[1] for p, _ in slots}) > 1 or len(slots) > 10:
        if S["form"] in ("rank_top", "dec"):
            return _best_open(S, slots, doms, cv)
    if S["form"] == "bin":
        vals = []
        for combo in itertools.product(*doms):
            T = assign(S, slots, combo)
            vals.append(quantity(T, T["ents"][T["case"]], T["q"], cv, top=True))
        b1 = bin_of(min(vals), S["rules"]["bins"], S["rules"]["bin_conv"], cv)
        b2 = bin_of(max(vals), S["rules"]["bins"], S["rules"]["bin_conv"], cv)
        if b1 == b2:
            return {"ans": b1, "det": True, "set": [b1]}
        return {"ans": "CBD", "det": False, "set": sorted({b1, b2})}
    answers = []
    for combo in itertools.product(*doms):
        a = _answer_safe(assign(S, slots, combo), cv)
        if a not in answers:
            answers.append(a)
    if len(answers) == 1 and answers[0] != "UNDEF":
        return {"ans": answers[0], "det": True, "set": answers}
    return {"ans": "CBD", "det": False, "set": answers}


def _own(slots: list, doms: list, i: int):
    idx = [k for k, (p, _) in enumerate(slots) if p[1] == i]
    return [slots[k] for k in idx], [doms[k] for k in idx]


def inv_status(S: dict, slots: list, doms: list, cv: dict) -> list:
    """Per case over its own unknowns only (unknowns never couple two cases, section 2 coupling rules)."""
    status = []
    for i in range(len(S["ents"])):
        sl, dm = _own(slots, doms, i)
        seen = set()
        for combo in itertools.product(*dm):
            T = assign(S, sl, combo) if sl else S
            try:
                seen.add(inv_meets(T, T["ents"][i], cv))
            except Undetermined:
                seen.add("UNDEF")
        status.append("meets" if seen == {True} else ("fails" if seen == {False} else "und"))
    return status


def _best_open(S: dict, slots: list, doms: list, cv: dict) -> dict:
    """Argmax / argmin with independent per-entity unknowns: entity i can win iff, at its best value and every other
    entity at its worst, it beats them all (ties: the tie rule). Exact because no unknown is shared by two entities."""
    n = len(S["ents"])
    high = (S.get("hl") == "high") if S["form"] == "rank_top" else False
    rngs = []
    for i in range(n):
        sl, dm = _own(slots, doms, i)
        vals = []
        for combo in itertools.product(*dm):
            T = assign(S, sl, combo) if sl else S
            try:
                vals.append(quantity(T, T["ents"][i], T["q"], cv, top=True))
            except Undetermined:
                return {"ans": "CBD", "det": False, "set": ["UNDEF"]}
        rngs.append((min(vals), max(vals)))
    ids = [id_num(e) for e in S["ents"]]
    tie_lower = cv["tie"] in ("std",)
    win = []
    for i in range(n):
        best_i = rngs[i][1] if high else rngs[i][0]
        ok = True
        for j in range(n):
            if j == i:
                continue
            worst_j = rngs[j][0] if high else rngs[j][1]
            if (best_i > worst_j) if high else (best_i < worst_j):
                continue
            if best_i == worst_j and tie_lower and ids[i] < ids[j]:
                continue
            ok = False
            break
        if ok:
            win.append(i)
    if len(win) == 1:
        # determined only if i also wins in every assignment
        i = win[0]
        worst_i = rngs[i][0] if high else rngs[i][1]
        sure = all(((worst_i > (rngs[j][1] if high else rngs[j][0])) if high else
                    (worst_i < (rngs[j][1] if high else rngs[j][0]))) or
                   (worst_i == (rngs[j][1] if high else rngs[j][0]) and tie_lower and ids[i] < ids[j])
                   for j in range(n) if j != i)
        if sure:
            return {"ans": i, "det": True, "set": [i]}
    return {"ans": "CBD", "det": False, "set": win}


def _inv_open(S: dict, slots: list, doms: list, cv: dict) -> dict:
    """Per case: meets / fails / undetermined over the box; then SEM-32 or one of its alternative readings."""
    status = inv_status(S, slots, doms, cv)
    sure = [i for i, s in enumerate(status) if s == "meets"]
    und = [i for i, s in enumerate(status) if s == "und"]
    mode = cv["inv_open"]
    if mode in ("closed_variant", "only_not_failing"):
        cand = sure + und
        if len(cand) == 1:
            return {"ans": cand[0], "det": True, "set": [cand[0]], "status": status}
        if not cand:
            return {"ans": "NOTA", "det": True, "set": ["NOTA"], "status": status}
    if mode == "sure_despite_und" and len(sure) == 1:
        return {"ans": sure[0], "det": True, "set": [sure[0]], "status": status}
    if len(sure) == 1 and not und:
        return {"ans": sure[0], "det": True, "set": [sure[0]], "status": status}
    if not sure and und:
        return {"ans": "CBD", "det": False, "set": [], "status": status}
    if not sure and not und:
        return {"ans": "NOTA", "det": True, "set": ["NOTA"], "status": status}
    return {"ans": ("BADSHAPE",), "det": False, "set": [], "status": status}
