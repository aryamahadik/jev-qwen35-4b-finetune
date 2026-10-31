"""F8 samplers: structure draws for every form (G0 spec 2, 8.1-8.5). One function per form builds S from a row plan.

Draw order (8): the plan fixes card version, form, world, placement class, side, comparator, polarity, <T>
representation and the gold slot before any number; numbers are then drawn (forward samplers S1, S3, S4) or solved
from the target (S2, and every sampler for bin, tier, rating and slot quotas, which are exact per-cell quotas, 10.1).
A draw that cannot realise its plan raises Retry; the caller redraws the numbers, never the plan.
"""
from __future__ import annotations

import copy
import itertools
import math
from fractions import Fraction as Fr

import draws as D
import lexicon as L
from numfmt import has_text
from solver_a import CV, Undetermined, assign, closed_answer, post_vec, quantity, solve, tier

OPS = {("up", "inclusive"): ">=", ("up", "strict"): ">", ("down", "inclusive"): "<=", ("down", "strict"): "<"}


class Retry(Exception):
    pass


def _pfloor(x: Fr) -> Fr:
    """Round a range end down to a whole percent (range ends are always shown as whole percents)."""
    return Fr(math.floor(x * 100), 100)


def new_id(card: dict, rng, used: set, prefix: str | None = None) -> str:
    """Fixed-width IDs, one prefix and one width per card (SEM-12, XF05); RANK-order cards use short IDs so that
    the 24 orderings fit the 2,000-token cap."""
    p = prefix or card["case"]["prefix"]
    w = card.get("id_width", 4)
    if w == 2:
        p = p[:2]
    lo, hi = 10 ** (w - 1), 10 ** w - 1
    for _ in range(1000):
        x = f"{p}-{rng.randint(lo, hi)}"
        if x not in used:
            used.add(x)
            return x
    raise Retry("ids")


# ------------------------------------------------------------------------------------------------ referenced facts
def _refs(card: dict) -> dict:
    R = card["rules"]
    conds = []
    for ln in (R.get("scorecard") or {}).get("lines", []):
        conds.append(ln["cond"])
        if ln.get("unless"):
            conds.append(ln["unless"])
    conds += list((R.get("only_if") or {}).values()) + [o["cond"] for o in R.get("overrides") or []]
    conds += list((R.get("arules") or {}).values())
    b, c, a = [], [], []
    for cond in conds:
        for p in cond["parts"]:
            if p["t"] == "bool" and p["f"] not in b:
                b.append(p["f"])
            if p["t"] == "cat" and p["name"] not in c:
                c.append(p["name"])
            if p["t"] == "amt" and p["name"] not in a:
                a.append(p["name"])
    return {"b": b, "c": c, "a": a}


def points_ent(rng, card: dict, pack: dict, eid: str, *, version: str, p_true=None, world="closed") -> dict:
    refs = _refs(card)
    pt = p_true if p_true is not None else rng.choice([30, 40, 50, 60])
    if not isinstance(pt, int):
        pt = int(round(pt * 100))
    b = {f: rng.randrange(100) < pt for f in refs["b"]}
    stated = {f: True for f in refs["b"]}
    if world == "closed" and version == "full" and card["sampler"] != "S3":
        for f in refs["b"]:
            if not b[f] and rng.random() < 0.5:
                stated[f] = False
    cats = {c["name"]: c["values"] for c in pack["cats"]}
    c = {n: rng.choice(cats[n]) for n in refs["c"]}
    a = {n: D.draw_money(rng, 100, 20000, 50) for n in refs["a"]}
    return {"id": eid, "pts": {"b": b, "c": c, "a": a, "stated": stated, "arng": {}}}


def make_open_bools(rng, ent: dict, n: int) -> list:
    keys = [f for f in ent["pts"]["b"]]
    rng.shuffle(keys)
    chosen = keys[:n]
    for f in chosen:
        ent["pts"]["b"][f] = None
        ent["pts"]["stated"][f] = True
    return chosen


# ------------------------------------------------------------------------------------------------ bayes data
def bayes_rates(rng, card, k: int, sign: str, shown: bool, rep_b: str, rep_l: str) -> dict:
    base, bden = D.draw_base_rates(rng, k, rep_b, card)
    lik, lden = [], []
    for _ in range(k):
        v, d = D.draw_chance(rng, rep_l, Fr(2, 100), Fr(95, 100), card=card)
        lik.append(v)
        lden.append(d)
    return {"form": "rates", "hyps": list(card["hyp_display"][:k]), "base": base, "lik": {sign: lik},
            "signs": [sign], "sig": {sign: shown}, "rng": {},
            "rep": {"base": rep_b, "base_den": bden, "lik": rep_l, "lik_den": lden}}


def bayes_counts(rng, card, k: int, sign: str, shown: bool) -> dict:
    cnt = []
    for _ in range(k):
        tot = rng.randint(20, 400)
        w = rng.randint(1, tot - 1)
        cnt.append([w, tot - w])
    return {"form": "counts", "hyps": list(card["hyp_display"][:k]), "cnt": {sign: cnt}, "signs": [sign],
            "sig": {sign: shown}, "base": None, "lik": {}, "rng": {}, "rep": {}}


def bayes_ne(rng, card, k: int, sign: str, shown: bool) -> dict:
    n = rng.randint(max(k, 20), 400)
    cuts = sorted(rng.sample(range(1, n), k - 1)) if k > 1 else []
    a = [y - x for x, y in zip([0] + cuts, cuts + [n])]
    return {"form": "nE", "hyps": list(card["hyp_display"][:k]), "ne": {sign: a}, "signs": [sign],
            "sig": {sign: shown}, "base": None, "lik": {}, "rng": {}, "rep": {}}


def solve_ne_to(rng, card, k, sign, shown, h, q: Fr, tries=200):
    for _ in range(tries):
        mult = rng.randint(1, max(1, 400 // max(1, q.denominator)))
        n = q.denominator * mult
        if n < max(k, 10) or n > 1200:
            continue
        a_h = q.numerator * mult
        rest = n - a_h
        if k > 1 and rest < k - 1:
            continue
        cuts = sorted(rng.sample(range(1, rest), k - 2)) if k > 2 else []
        parts = [y - x for x, y in zip([0] + cuts, cuts + [rest])] if k > 1 else []
        if parts and min(parts) < 1:
            continue
        it = iter(parts)
        a = [a_h if j == h else next(it) for j in range(k)]
        bay = {"form": "nE", "hyps": list(card["hyp_display"][:k]), "ne": {sign: a}, "signs": [sign],
               "sig": {sign: shown}, "base": None, "lik": {}, "rng": {}, "rep": {}}
        if post_vec({"bay": bay}, CV())[h] == q:
            return bay
    raise Retry("nE solve")


def bayes_any(rng, card, form, k, sign, shown):
    if form == "rates" and k >= 3:
        shown = True                            # depth 2k (+k per unstated complement) stays <= 6
    if form == "rates" and card.get("two_signs") and (k == 2 or card["schema"] == "pred") and rng.randrange(2):
        # S5 two-stage evidence: two signs, both shown, independent given the class (SEM-26)
        bay = bayes_rates(rng, card, k, sign, True, rng.choice(card["reps"]), rng.choice(card["reps"]))
        s2 = [x for x in card["signs"] if x != sign][0]
        lik2 = []
        for _ in range(k):
            v, d = D.draw_chance(rng, bay["rep"]["lik"], Fr(5, 100), Fr(95, 100), card=card)
            lik2.append(v)
        if bay["rep"]["lik"] in ("frac", "ain", "aoutof"):
            return bay
        bay["lik"][s2] = lik2
        bay["signs"].append(s2)
        bay["sig"][s2] = True
        return bay
    if form == "counts":
        return bayes_counts(rng, card, k, sign, shown)
    if form == "nE":
        return bayes_ne(rng, card, k, sign, shown)
    if form == "joint":
        return bayes_joint(rng, card, k, sign)
    return bayes_rates(rng, card, k, sign, shown, rng.choice(card["reps"]), rng.choice(card["reps"]))


def bayes_joint(rng, card, k: int, sign: str) -> dict:
    tot_units = rng.choice([20, 40, 60, 80])
    cuts = sorted(rng.sample(range(1, tot_units), k - 1)) if k > 1 else []
    parts = [b - a for a, b in zip([0] + cuts, cuts + [tot_units])]
    J = [Fr(p, 100) for p in parts]
    return {"form": "joint", "hyps": list(card["hyp_display"][:k]), "joint": {sign: J}, "signs": [sign],
            "sig": {sign: True}, "base": None, "lik": {}, "rng": {}, "rep": {"joint": "pct0"}}


def rates_in_range(rng, card, k, sign, shown, rep_b, rep_l, h, lo: Fr, hi: Fr, lo_incl: bool, hi_incl: bool,
                   tries=300):
    """Rates data whose posterior P(H_h | evidence) lies in a range (forward draws, rejection)."""
    for _ in range(tries):
        bay = bayes_rates(rng, card, k, sign, shown, rep_b, rep_l)
        try:
            v = post_vec({"bay": bay}, CV())[h]
        except Undetermined:
            continue
        if (v > lo or (lo_incl and v == lo)) and (v < hi or (hi_incl and v == hi)):
            return bay
    raise Retry("rates range")


def solve_rates_to(rng, card, k, sign, shown, rep_b, rep_l, h, q: Fr, tries=120):
    """Rates data whose posterior P(H_h | evidence) is exactly q (target-first, 8.2)."""
    for _ in range(tries):
        bay = bayes_rates(rng, card, k, sign, shown, rep_b, rep_l)
        base = bay["base"]
        lik = bay["lik"][sign]
        eff = [x if shown else 1 - x for x in lik]
        rest = sum(base[j] * eff[j] for j in range(k) if j != h)
        if q <= 0 or q >= 1 or base[h] == 0:
            continue
        need = q * rest / (base[h] * (1 - q))           # effective likelihood for H_h
        L_h = need if shown else 1 - need
        if not (0 < L_h < 1):
            continue
        den = bay["rep"]["lik_den"][h]
        if not has_text(L_h, rep_l, den):
            if rep_l in ("frac", "ain", "aoutof") and has_text(L_h, rep_l, None) and L_h.denominator in \
                    (list(card.get("frac_denoms") or []) + list(L.AIN_DENOMS)):
                den = L_h.denominator
            else:
                continue
        lik[h] = L_h
        bay["rep"]["lik_den"][h] = den
        if post_vec({"bay": bay}, CV())[h] == q:
            return bay
    raise Retry("rates solve")


def solve_counts_to(rng, card, k, sign, shown, h, q: Fr, tries=400):
    col = 0 if shown else 1
    for _ in range(tries):
        m_unit = q.denominator
        mult = rng.randint(1, max(1, 400 // max(1, m_unit)))
        m = m_unit * mult
        if m < 4 or m > 1200:
            continue
        a = q.numerator * mult
        rest = m - a
        if k > 1 and rest < (k - 1):
            continue
        if k == 1 and rest:
            continue
        parts = []
        if k > 1:
            cuts = sorted(rng.sample(range(1, rest), k - 2)) if k > 2 and rest > k - 2 else []
            if k > 2 and len(cuts) != k - 2:
                continue
            parts = [y - x for x, y in zip([0] + cuts, cuts + [rest])]
            if min(parts) < 1:
                continue
        withs = []
        it = iter(parts)
        for j in range(k):
            withs.append(a if j == h else next(it))
        cnt = []
        for j in range(k):
            other = rng.randint(1, 400)
            cnt.append([withs[j], other] if col == 0 else [other, withs[j]])
        bay = {"form": "counts", "hyps": list(card["hyp_display"][:k]), "cnt": {sign: cnt}, "signs": [sign],
               "sig": {sign: shown}, "base": None, "lik": {}, "rng": {}, "rep": {}}
        if post_vec({"bay": bay}, CV())[h] == q:
            return bay
    raise Retry("counts solve")


def solve_joint_to(rng, card, k, sign, h, q: Fr, tries=200):
    for _ in range(tries):
        tot = rng.choice([20, 25, 40, 50, 60, 75, 80])
        a = q * tot
        if a.denominator != 1 or a.numerator < 1 or a.numerator >= tot:
            continue
        a = a.numerator
        rest = tot - a
        if rest < k - 1:
            continue
        cuts = sorted(rng.sample(range(1, rest), k - 2)) if k > 2 else []
        parts = [y - x for x, y in zip([0] + cuts, cuts + [rest])] if k > 1 else []
        if parts and min(parts) < 1:
            continue
        it = iter(parts)
        J = [Fr(a, 100) if j == h else Fr(next(it), 100) for j in range(k)]
        bay = {"form": "joint", "hyps": list(card["hyp_display"][:k]), "joint": {sign: J}, "signs": [sign],
               "sig": {sign: True}, "base": None, "lik": {}, "rng": {}, "rep": {"joint": "pct0"}}
        if post_vec({"bay": bay}, CV())[h] == q:
            return bay
    raise Retry("joint solve")


# ------------------------------------------------------------------------------------------------ outcomes
def outcomes(rng, card, n: int, *, mode: str, reps: list, remainder: bool, amt_lo=200, amt_hi=20000,
             fixed_event: bool = False):
    evs = list(card.get("events") or ["loss event"])
    if not fixed_event:
        rng.shuffle(evs)
    for _ in range(200):
        outs = []
        for i in range(n):
            rep = rng.choice(reps)
            p, den = D.draw_chance(rng, rep, Fr(1, 100), Fr(60, 100), card=card)
            a = D.draw_money(rng, amt_lo, amt_hi, rng.choice([50, 100]))
            if mode == "net" and rng.random() < 0.5:
                a = -a
            outs.append({"ev": evs[i % len(evs)], "p": p, "a": a, "prep": rep, "pden": den, "prng": None,
                         "arng": None})
        tot = sum(o["p"] for o in outs)
        if tot > 1:
            continue
        if not remainder and tot != 1 and n == 1:
            # a single outcome with no remainder would be a sure loss; keep a remainder (SEM-19 is on the card)
            pass
        if len({o["ev"] for o in outs}) != len(outs):
            continue
        return outs
    raise Retry("outcomes")


# ------------------------------------------------------------------------------------------------ helpers
def qtype_of(card: dict, q: dict) -> str:
    k = q["k"]
    if k == "risk":
        k = q["def"]
    return {"score": "score", "post": "chance", "chance": "chance", "el": "money", "tec": "money", "ev": "money",
            "en": "num"}[k]


def answer(S, cv=None):
    return solve(S, cv or CV())


def base_S(card, form, world="closed"):
    return {"form": form, "sub": card["sub"], "world": world, "mode": card.get("mode"), "q": dict(card.get("q", {})),
            "case": 0, "ents": [], "rules": card["rules"], "card_id": card["card_id"]}


def _yes_is_bad(card, S):
    """10.2: from quantity polarity, direction and negation parity; null for neutral items."""
    f = S["form"]
    if f == "yn_act":
        pol = card["act_pol"].get(S["act"]["action"])
        v = True if pol == "protective" else (False if pol == "favourable" else None)
        neg = S["act"]["neg"]
    else:
        k = S["q"]["k"]
        if k in ("score", "el", "tec", "risk"):
            adv = True
        elif k == "ev":
            adv = False
        elif k == "en":
            adv = True
        elif k == "post":
            pol = card["hyp"]["pol"].get(card["hyp"]["labels"][S["q"]["h"]])
            adv = True if pol == "adverse" else (False if pol == "favourable" else None)
        else:
            adv = True
        if adv is None:
            return None
        up = S["thr"]["op"] in (">", ">=")
        v = adv == up
        neg = S["thr"]["neg"]
    if v is None:
        return None
    return v if neg % 2 == 0 else (not v)


# ================================================================================================ YN threshold
def gen_yn_thr(card, pack, plan, rng):
    S = base_S(card, "yn_thr", plan["world"])
    q = dict(card["q"])
    used = set()
    eid = new_id(card, rng, used)
    sub = card["sub"]
    if q["k"] == "post":
        hyps = card["hyp"]["labels"]
        polar = [i for i, x in enumerate(hyps) if card["hyp"]["pol"][x] in ("adverse", "favourable")]
        q["h"] = plan.get("h", rng.choice(polar or [0]))
    S["q"] = q
    qt = qtype_of(card, q)
    ent = {"id": eid}
    k_h = len(card.get("hyp_display") or [1, 2])
    form = None
    if sub == "points" or q.get("def") == "score":
        ent = points_ent(rng, card, pack, eid, version=plan["version"], world=plan["world"])
    elif q["k"] == "post":
        form = plan.get("bform") or rng.choice(card["data_forms"])
        sign = rng.choice(card["signs"])
        shown = rng.random() < 0.5 if form != "joint" else True
        if plan["world"] == "open":
            form = "rates"
        ent["bay"] = bayes_any(rng, card, form, k_h, sign, shown)
    elif q["k"] == "en":
        rep = rng.choice(card["reps"])
        p, den = D.draw_chance(rng, rep, Fr(1, 100), Fr(80, 100), card=card)
        ent["en"] = {"n": rng.randint(3, 60), "p": p, "rep": rep, "den": den, "ev": card["events"][0]}
    elif q["k"] in ("el", "tec", "ev") or q.get("def") in ("el",):
        n = rng.choices([1, 2, 3], [45, 40, 15])[0]
        ent["outs"] = outcomes(rng, card, n, mode=card["mode"], reps=card["reps"], remainder=True)
        if q["k"] == "tec":
            ent["cost"] = Fr(0) if rng.random() < 0.08 else D.draw_money(rng, 50, 5000, 50)
            ent["cost_word"] = rng.choice(["0", "None"]) if ent["cost"] == 0 else None
            ent["action"] = rng.choice(card["actions"])["label"]
    elif q.get("def") == "chance":
        rep = rng.choice(card["reps"])
        p, den = D.draw_chance(rng, rep, Fr(1, 100), Fr(95, 100), card=card)
        ent["ch"] = {"p": p, "rep": rep, "den": den, "ev": card["events"][0], "rng": None}
    S["ents"] = [ent]
    # open world: 1-3 unknowns, every allowed value giving the same answer (determined by construction)
    if plan["world"] == "open":
        _make_unknowns(rng, card, S, ent, plan)
    # value and threshold
    trep = plan.get("trep") or D.draw_trep(rng, qt, card)
    valid, cap = _valid_range(card, S, qt, ent)
    op = OPS[(plan["dir"], plan["cmpcls"])]
    if plan["world"] == "open":
        lo, hi = _value_interval(S, ent)
        T = _open_threshold(rng, lo, hi, qt, trep, plan, valid)
        S["thr"] = {"op": op, "T": T, "neg": plan["neg"], "trep": trep}
        d = None
    else:
        v = quantity(S, ent, q, CV())
        if not isinstance(v, Fr):
            v = Fr(v)
        res = D.place_threshold(v, qt, trep, plan["place"], plan["side"], rng, valid=valid, cap=cap)
        if res is None:
            raise Retry("placement")
        T, d = res
        S["thr"] = {"op": op, "T": T, "neg": plan["neg"], "trep": trep}
    S["cmp_word"] = plan["cmp_word"]
    return S, {"placement": plan["place"] if plan["world"] == "closed" else "open",
               "d_steps": d, "t_repr": trep, "qt": qt}


def _valid_range(card, S, qt, ent):
    if qt == "chance":
        return (Fr(0), Fr(1)), 500
    if qt == "score":
        sc = card["rules"]["scorecard"]
        return (Fr(sc["F"]), Fr(sc["M"])), sc["M"] - sc["F"]
    if qt == "money":
        if S["mode"] == "net":
            return (None, None), None
        return (Fr(0), None), None
    if qt == "num":
        return (Fr(0), Fr(ent["en"]["n"])), None
    raise ValueError(qt)


def _value_interval(S, ent):
    from solver_a import _domains, assign, unknown_slots
    slots = unknown_slots(S)
    doms = _domains(slots, CV())
    vals = []
    for combo in itertools.product(*doms):
        T = assign(S, slots, combo)
        vals.append(quantity(T, T["ents"][0], T["q"], CV()))
    return min(vals), max(vals)


def _open_threshold(rng, lo, hi, qt, trep, plan, valid):
    on, g = D.t_grid(qt, trep)
    aff = plan["gold"] if plan["neg"] % 2 == 0 else (not plan["gold"])
    up = plan["dir"] == "up"
    # aff with up: value above T everywhere -> T below lo; aff with down: value below T -> T above hi
    want_below = (aff and up) or ((not aff) and (not up))
    for _ in range(60):
        D_ = rng.randint(1, 40)
        if want_below:
            T = D._grid_floor(lo, g) - (D_ - 1) * g
            if T == lo and plan["cmpcls"] == "strict" and up:
                T -= g
        else:
            T = D._grid_floor(hi, g) + D_ * g
        while not on(T):
            T += (-g if want_below else g)
        if valid[0] is not None and not T > valid[0]:
            continue
        if valid[1] is not None and not T < valid[1]:
            continue
        return T
    raise Retry("open threshold")


def _make_unknowns(rng, card, S, ent, plan):
    n = rng.choices([1, 2, 3], [60, 30, 10])[0]
    sub = card["sub"]
    if "pts" in ent:
        make_open_bools(rng, ent, min(n, len(ent["pts"]["b"])))
    elif "bay" in ent and ent["bay"]["form"] == "rates":
        sign = ent["bay"]["signs"][0]
        j = rng.randrange(len(ent["bay"]["hyps"]))
        if rng.random() < 0.6:
            v = ent["bay"]["lik"][sign][j]
            w = Fr(rng.randint(2, 15), 100)
            lo, hi = max(Fr(0), v - w), min(Fr(1), v + w)
            lo, hi = Fr(math.floor(lo * 100), 100), Fr(math.ceil(hi * 100), 100)
            ent["bay"]["rng"][f"{sign}|{j}"] = (lo, hi)
            ent["bay"]["rngshow"] = ent["bay"].get("rngshow", {})
            ent["bay"]["rngshow"][f"{sign}|{j}"] = True
        else:
            ent["bay"]["rng"][f"{sign}|{j}"] = (Fr(0), Fr(1))
        ent["bay"]["lik"][sign][j] = None
    elif "outs" in ent:
        k = rng.randrange(len(ent["outs"]))
        o = ent["outs"][k]
        others = sum(x["p"] for i, x in enumerate(ent["outs"]) if i != k)
        if rng.random() < 0.5:
            w = Fr(rng.randint(2, 15), 100)
            lo = max(Fr(0), Fr(math.floor((o["p"] - w) * 100), 100))
            hi = min(_pfloor(1 - others), Fr(math.ceil((o["p"] + w) * 100), 100))
            o["prng"], o["p"] = (lo, hi), None
            o["prng_show"] = True
        else:
            w = rng.choice([200, 500, 1000])
            lo = max(Fr(0), o["a"] - w) if S["mode"] != "net" else o["a"] - w
            o["arng"], o["a"] = (lo, o["a"] + w), None
            o["arng_show"] = True
    elif "en" in ent or "ch" in ent:
        raise Retry("no open en/chance rows")
    else:
        raise Retry("open")


# ================================================================================================ YN action rule
def gen_yn_act(card, pack, plan, rng):
    S = base_S(card, "yn_act", plan["world"])
    S["q"] = {"k": "score"} if card["rules"].get("scorecard") else {"k": "none"}
    used = set()
    a = rng.choice(sorted(card["rules"]["arules"]))
    want_aff = plan["gold"] if plan["neg"] % 2 == 0 else (not plan["gold"])
    for _ in range(300):
        ent = points_ent(rng, card, pack, new_id(card, rng, used), version=plan["version"], world=plan["world"])
        S["ents"] = [ent]
        S["act"] = {"action": a, "neg": plan["neg"]}
        if plan["world"] == "open":
            make_open_bools(rng, ent, rng.choice([1, 1, 2]))
        r = solve(S, CV())
        if not r["det"]:
            continue
        aff = r["ans"] if plan["neg"] % 2 == 0 else (not r["ans"])
        if aff == want_aff:
            return S, {"placement": None, "d_steps": None, "t_repr": None, "qt": None}
    raise Retry("act")


# ================================================================================================ BIN
def gen_bin(card, pack, plan, rng):
    S = base_S(card, "bin", plan["world"])
    hyps = card["hyp_display"]
    k = len(hyps)
    h = rng.randrange(k)
    S["q"] = {"k": "post", "h": h}
    edges = card["rules"]["bins"]
    conv = card["rules"]["bin_conv"]
    K = len(edges) + 1
    sign = rng.choice(card["signs"])
    form = plan.get("bform") or rng.choice(card["data_forms"])
    shown = rng.random() < 0.5 if form != "joint" else True
    if form == "rates" and k >= 3:
        shown = True
    used = set()
    ent = {"id": new_id(card, rng, used)}
    if plan["world"] == "closed":
        tb = plan["slot"]
        if plan.get("edge_row") and form == "rates":
            form = rng.choice(["counts", "nE", "joint"])
        if form == "rates":
            lo = Fr(0) if tb == 0 else edges[tb - 1]
            hi = Fr(1) if tb == len(edges) else edges[tb]
            ent["bay"] = rates_in_range(rng, card, k, sign, shown, rng.choice(card["reps"]), rng.choice(card["reps"]),
                                        h, lo, hi, conv == "lo" or tb == 0, conv == "hi" or tb == len(edges))
            S["ents"] = [ent]
            return S, {"edge_row": False}
        q = _target_in_bin(rng, edges, conv, tb, plan.get("edge_row", False))
        if form == "counts":
            ent["bay"] = solve_counts_to(rng, card, k, sign, shown, h, q)
        elif form == "nE":
            ent["bay"] = solve_ne_to(rng, card, k, sign, shown, h, q)
        elif form == "joint":
            ent["bay"] = solve_joint_to(rng, card, k, sign, h, q)
        else:
            ent["bay"] = solve_rates_to(rng, card, k, sign, shown, rng.choice(card["reps"]),
                                        rng.choice(card["reps"]), h, q)
        S["ents"] = [ent]
        return S, {"edge_row": plan.get("edge_row", False)}
    # open world: one P(E | Hj) unknown with a stated range (rates form only)
    rep_b, rep_l = rng.choice(card["reps"]), rng.choice(card["reps"])
    if k >= 3:
        shown = True
    for _ in range(200):
        ent["bay"] = bayes_rates(rng, card, k, sign, shown, rep_b, rep_l)
        S["ents"] = [ent]
        j = rng.randrange(k)
        v = ent["bay"]["lik"][sign][j]
        w = Fr(rng.randint(1, 20), 100)
        lo = max(Fr(0), Fr(math.floor((v - w) * 100), 100))
        hi = min(Fr(1), Fr(math.ceil((v + w) * 100), 100))
        ent["bay"]["lik"][sign][j] = None
        ent["bay"]["rng"][f"{sign}|{j}"] = (lo, hi)
        ent["bay"]["rngshow"] = {f"{sign}|{j}": True}
        try:
            r = solve(S, CV())
        except (Undetermined, ZeroDivisionError):
            continue
        want = plan["slot"]
        if (want == "CBD" and not r["det"]) or (want != "CBD" and r["det"] and r["ans"] == want):
            return S, {"edge_row": False}
    raise Retry("bin open")


def _target_in_bin(rng, edges, conv, tb, edge_row):
    lo = Fr(0) if tb == 0 else edges[tb - 1]
    hi = Fr(1) if tb == len(edges) else edges[tb]
    if edge_row:
        # a value exactly on an edge that belongs to bin tb under the card's convention
        if conv == "lo" and tb > 0:
            return lo
        if conv == "hi" and tb < len(edges):
            return hi
        raise Retry("edge row impossible for this bin")
    for _ in range(100):
        k = rng.randint(math.ceil(lo * 1000) + 1, max(math.ceil(lo * 1000) + 1, math.floor(hi * 1000) - 1))
        q = Fr(k, 1000)
        if lo < q < hi and 0 < q < 1:
            return q
    raise Retry("bin target")


# ================================================================================================ TIER
def _tier_pool(card, pack, plan, rng, n=1500):
    pool = card.setdefault("_tier_pool", {})
    S = base_S(card, "tier", "closed")
    used = set()
    for a in range(n):
        pt = [20, 35, 50, 65, 80, 92][a % 6]
        ent = points_ent(rng, card, pack, new_id(card, rng, used), version="short", p_true=pt)
        S["ents"] = [ent]
        t, step = tier(ent, S, CV())
        pool.setdefault((t, step), []).append(ent["pts"])
    card["_tier_pool_n"] = card.get("_tier_pool_n", 0) + n
    return pool


def gen_tier(card, pack, plan, rng):
    """Target tier and decisive step (XF08: only-if limit or override on >= 50% of TIER rows) from a pool of drawn
    fact sets (rejection sampling with the draws kept, so infeasible plans fail fast)."""
    S = base_S(card, "tier", "closed")
    pool = card.get("_tier_pool") or _tier_pool(card, pack, plan, rng)
    want_t, want_step = plan["slot"], plan["step"]
    if len(pool.get((want_t, want_step), [])) < 2 and card.get("_tier_pool_n", 0) < 12000:
        pool = _tier_pool(card, pack, plan, rng)
    cand = pool.get((want_t, want_step)) or []
    if not cand:
        alts = [k for k in pool if k[0] == want_t and pool[k]]
        if not alts:
            raise Retry("tier infeasible")
        alts.sort(key=lambda k: (k[1] is None, rng.random()))
        want_step = alts[0][1]
        cand = pool[alts[0]]
    import errors as ER
    for _ in range(min(25, len(cand))):
        pts = cand.pop(rng.randrange(len(cand)))
        used = set()
        ent = {"id": new_id(card, rng, used), "pts": copy.deepcopy(pts)}
        if plan["version"] == "full":
            for f, v in ent["pts"]["b"].items():
                ent["pts"]["stated"][f] = v or (rng.randrange(2) == 0)
        S["ents"] = [ent]
        t, step = tier(ent, S, CV())
        if t != want_t or step != want_step:
            continue
        if not ER.has_distractor(S, t):
            continue
        return S, {"tier_step": step}
    raise Retry("tier pool")


# ================================================================================================ MAT
def gen_mat(card, pack, plan, rng):
    S = base_S(card, "mat", "closed")
    m = card["rules"]["mat"]
    want = plan["slot"]
    cells = [(i, j) for i in range(len(m["grid"])) for j in range(len(m["grid"][0])) if m["grid"][i][j] == want]
    if not cells:
        raise Retry("no cell")
    li, ii = rng.choice(cells)
    edge = plan.get("edge_row", False)
    used = set()
    le, ie = m["lik_edges"], m["imp_edges"]
    llo = Fr(0) if li == 0 else le[li - 1]
    lhi = Fr(1) if li == len(le) else le[li]
    for _ in range(300):
        rep = rng.choice(card["reps"])
        if edge and rng.random() < 0.5 and (li > 0 or li < len(le)):
            # likelihood exactly on an edge that belongs to level li
            if m["lik_conv"] == "lo" and li > 0:
                p = llo
            elif m["lik_conv"] == "hi" and li < len(le):
                p = lhi
            else:
                continue
            if not has_text(p, rep):
                rep = "pct0"
            den = None
            edge_kind = "lik"
        else:
            try:
                p, den = D.draw_chance(rng, rep, max(Fr(1, 100), llo), min(Fr(99, 100), lhi), card=card)
            except ValueError:
                continue
            edge_kind = None
        ilo = Fr(1) if ii == 0 else ie[ii - 1]
        ihi = ie[ii] if ii < len(ie) else ie[-1] * 3
        if m["impact"] == "loss":
            if edge and edge_kind is None and ii > 0:
                amt = ilo
                edge_kind = "imp"
            else:
                amt = D.draw_money(rng, int(ilo), int(ihi) - 1, 10)
            imp = amt
        else:
            # impact = chance x loss of the one listed outcome (F8-R3-04 (ii))
            if edge and edge_kind is None and ii > 0:
                amt = ilo / p
                edge_kind = "imp"
                if amt.denominator != 1:
                    continue
            else:
                lo_a, hi_a = math.ceil(ilo / p), math.floor((ihi - 1) / p)
                if lo_a > hi_a:
                    continue
                amt = Fr(rng.randint(lo_a, hi_a))
            imp = p * amt
        ent = {"id": new_id(card, rng, used), "mat": {"lik": p, "amt": amt, "p": p, "rep": rep, "den": den}}
        S["ents"] = [ent]
        try:
            if closed_answer(S, CV()) == want:
                if edge and edge_kind is None:
                    continue
                return S, {"edge_row": bool(edge_kind)}
        except Undetermined:
            continue
    raise Retry("mat")


# ================================================================================================ RANK / DEC / INV ents
def rank_ent(rng, card, pack, eid, d, plan, *, version="full"):
    ent = {"id": eid}
    if d == "chance":
        rep = rng.choice(card["reps"])
        p, den = D.draw_chance(rng, rep, Fr(1, 100), Fr(95, 100), card=card)
        ent["ch"] = {"p": p, "rep": rep, "den": den, "ev": card["events"][0], "rng": None,
                     "amt": D.draw_money(rng, 500, 30000, 100)}
    elif d == "el":
        n = 1 if card["sampler"] == "S3" else rng.choice([1, 1, 2])
        ent["outs"] = outcomes(rng, card, n, mode="loss", reps=card["reps"], remainder=True, fixed_event=True)
    elif d == "score":
        ent.update(points_ent(rng, card, pack, eid, version=version, p_true=plan.get("_pt")))
    elif d == "tec":
        ent["outs"] = outcomes(rng, card, 1, mode="loss", reps=card["reps"], remainder=True, fixed_event=True)
        ent["cost"] = Fr(0) if rng.random() < 0.08 else D.draw_money(rng, 50, 5000, 50)
        ent["cost_word"] = rng.choice(["0", "None"]) if ent["cost"] == 0 else None
    return ent


def _risk_def(card):
    q = card["q"]
    if q["k"] == "risk":
        return q["def"]
    return q["k"]


def gen_rank_top(card, pack, plan, rng):
    S = base_S(card, "rank_top", plan["world"])
    S["hl"] = plan["hl"]
    d = _risk_def(card)
    n = plan["n"]
    cbd_shown = plan["world"] == "open"
    k = n - 1 if cbd_shown else n
    for _ in range(400):
        used = set()
        ents = [rank_ent(rng, card, pack, new_id(card, rng, used), d, plan) for _ in range(k)]
        S["ents"] = ents
        if plan.get("tie"):
            _plant_tie(rng, S, d)
        if plan["world"] == "open":
            _rank_open_unknown(rng, card, S, d)
        try:
            r = solve(S, CV())
        except (Undetermined, ValueError):
            continue
        if plan["world"] == "open":
            if (plan["slot"] == "CBD") != (not r["det"]):
                continue
        elif not r["det"]:
            continue
        return S, {}
    raise Retry("rank_top")


def _plant_tie(rng, S, d):
    ents = S["ents"]
    if len(ents) < 2 or d != "chance":
        raise Retry("tie only on chance rows")
    vals = [e["ch"]["p"] for e in ents]
    best = max(vals) if S.get("hl", "high") == "high" else min(vals)
    i = vals.index(best)
    j = rng.choice([x for x in range(len(ents)) if x != i])
    ents[j]["ch"] = dict(ents[i]["ch"])
    rep = rng.choice(["pct0", "frac", "dec", "ain"])
    if has_text(ents[j]["ch"]["p"], rep, None):
        ents[j]["ch"]["rep"], ents[j]["ch"]["den"] = rep, None


def _rank_open_unknown(rng, card, S, d):
    e = rng.choice(S["ents"])
    if d == "chance":
        v = e["ch"]["p"]
        w = Fr(rng.randint(2, 25), 100)
        lo = max(Fr(0), Fr(math.floor((v - w) * 100), 100))
        hi = min(Fr(1), Fr(math.ceil((v + w) * 100), 100))
        e["ch"]["p"], e["ch"]["rng"] = None, (lo, hi)
    elif d in ("el", "tec"):
        o = e["outs"][0]
        others = sum(x["p"] for x in e["outs"][1:])
        w = Fr(rng.randint(2, 25), 100)
        lo = max(Fr(0), Fr(math.floor((o["p"] - w) * 100), 100))
        hi = min(_pfloor(1 - others), Fr(math.ceil((o["p"] + w) * 100), 100))
        o["p"], o["prng"], o["prng_show"] = None, (lo, hi), True
    else:
        raise Retry("open score rank")


def gen_rank_order(card, pack, plan, rng):
    S = base_S(card, "rank_order", "closed")
    d = _risk_def(card)
    n_items = plan["items"]
    for _ in range(400):
        used = set()
        pts = [15, 35, 55, 75, 92]
        rng.shuffle(pts)
        ents = [rank_ent(rng, card, pack, new_id(card, rng, used), d, {**plan, "_pt": pts[i]})
                for i in range(n_items)]
        S["ents"] = ents
        try:
            truth = closed_answer(S, CV())
        except (Undetermined, ValueError):
            continue
        errs = _rank_error_orders(S)
        if not errs:
            continue
        if n_items == 4:
            return S, {"subset_class": "full", "errs": errs}
        # 5 items: subset class P1 / P2 (F8-R1-08)
        cls = plan["subset"]
        want_nota = plan["slot"] == "NOTA"
        X = rng.randrange(n_items)
        positions = list(range(n_items))
        for _ in range(40):
            p = rng.choice(positions)
            qpos = rng.choice([x for x in positions if x != p]) if cls == "P2" else None
            allowed = {p} if cls == "P1" else {p, qpos}

            def in_cls(order):
                return order.index(X) in allowed
            if in_cls(truth) == want_nota:
                continue
            if not any(in_cls(o) for o in errs.values()):
                continue
            S["subset"] = {"cls": cls, "X": X, "pos": sorted(allowed)}
            return S, {"subset_class": cls, "errs": errs}
    raise Retry("rank_order")


def _rank_error_orders(S):
    import errors as ER
    out = {}
    truth = closed_answer(S, CV())
    for eid, answers in ER.named_errors(S).items():
        for o in answers:
            if o != truth and isinstance(o, tuple):
                out.setdefault(eid, o)
    return out


def gen_dec(card, pack, plan, rng):
    S = base_S(card, "dec", plan["world"])
    n = plan["n"]
    k = n - 1 if plan["world"] == "open" else n
    acts = list(card["actions"])
    if len(acts) < k:
        raise Retry("not enough actions")
    for _ in range(400):
        used = set()
        rng.shuffle(acts)
        ents = []
        ev = card["events"][0]
        S["dec_case"] = new_id(card, rng, used)
        aprefix = "ACT" if card["case"]["prefix"] != "ACT" else "ACN"
        for a in acts[:k]:
            e = {"id": new_id(card, rng, used, aprefix), "action": a["label"]}
            rep = rng.choice(card["reps"])
            p, den = D.draw_chance(rng, rep, Fr(1, 100), Fr(70, 100), card=card)
            amt = D.draw_money(rng, 500, 30000, 100)
            e["outs"] = [{"ev": ev, "p": p, "a": amt, "prep": rep, "pden": den, "prng": None, "arng": None}]
            e["cost"] = Fr(0) if rng.random() < 0.15 else D.draw_money(rng, 50, 8000, 50)
            e["cost_word"] = rng.choice(["0", "None"]) if e["cost"] == 0 else None
            ents.append(e)
        S["ents"] = ents
        if plan.get("tie"):
            vals = [quantity(S, e, S["q"], CV()) for e in ents]
            i = vals.index(min(vals))
            j = rng.choice([x for x in range(len(ents)) if x != i])
            diff = vals[j] - vals[i]
            nc = ents[j]["cost"] - diff
            if nc < 0 or nc.denominator != 1:
                continue
            ents[j]["cost"] = nc
            ents[j]["cost_word"] = None if nc != 0 else "0"
        if plan["world"] == "open":
            e = rng.choice(ents)
            o = e["outs"][0]
            w = Fr(rng.randint(2, 25), 100)
            lo = max(Fr(0), Fr(math.floor((o["p"] - w) * 100), 100))
            hi = min(Fr(1), Fr(math.ceil((o["p"] + w) * 100), 100))
            o["p"], o["prng"], o["prng_show"] = None, (lo, hi), True
        try:
            r = solve(S, CV())
        except (Undetermined, ValueError):
            continue
        if plan["world"] == "open" and (plan["slot"] == "CBD") != (not r["det"]):
            continue
        if plan["world"] == "closed" and not r["det"]:
            continue
        return S, {}
    raise Retry("dec")


# ================================================================================================ PRED
def gen_pred(card, pack, plan, rng):
    S = base_S(card, "pred", "closed")
    k = len(card["hyp_display"])
    S["q"] = {"k": "post", "h": 0}
    sign = rng.choice(card["signs"])
    used = set()
    form = rng.choice(card["data_forms"])
    if form == "joint":
        form = "rates"
    for _ in range(600):
        shown = rng.random() < 0.5
        ent = {"id": new_id(card, rng, used)}
        ent["bay"] = bayes_any(rng, card, form, k, sign, shown)
        S["ents"] = [ent]
        try:
            pv = post_vec(ent, CV())
        except Undetermined:
            continue
        srt = sorted(pv, reverse=True)
        if srt[0] - srt[1] < Fr(1, 20):
            continue
        g = pv.index(srt[0])
        try:
            prior = post_vec(ent, CV(post="prior"))
        except Undetermined:
            prior = None
        changes = None if prior is None else (prior.index(max(prior)) != g or prior.count(max(prior)) > 1)
        if plan.get("changes") is not None and changes is not None and changes != plan["changes"]:
            continue
        if g != plan["slot"]:
            continue
        return S, {"evidence_changes": changes}
    raise Retry("pred")


# ================================================================================================ INV
def inv_ent(rng, card, pack, eid, plan):
    sub = card["sub"]
    if card["rules"]["inv"]["kind"] == "act" or sub == "points":
        return points_ent(rng, card, pack, eid, version=plan["version"], p_true=plan.get("_pt"))
    d = card["rules"]["inv"]["q"]["k"] if card["rules"]["inv"]["kind"] == "q" else "chance"
    if d == "risk":
        d = card["rules"]["inv"]["q"]["def"]
    return rank_ent(rng, card, pack, eid, d, plan)


def gen_inv(card, pack, plan, rng):
    S = base_S(card, "inv", plan["world"])
    r = card["rules"]["inv"]
    S["q"] = dict(r["q"]) if r["kind"] == "q" else {"k": "none"}
    n_cases = plan["n"] - 1
    slot = plan["slot"]                       # case index or "ABST"
    for _ in range(10):
        used = set()
        ents = []
        for i in range(n_cases):
            ents.append(inv_ent(rng, card, pack, new_id(card, rng, used), plan))
        S["ents"] = ents
        # make exactly the planned case meet (closed), or none
        ok = _inv_fit(rng, card, pack, S, slot, plan)
        if not ok:
            continue
        return S, {}
    raise Retry("inv")


def _case_status(S, i):
    """meets / fails / und for case i over its own unknowns (no unknown couples two cases)."""
    from solver_a import _domains, inv_meets, unknown_slots
    one = {**S, "ents": [S["ents"][i]]}
    slots = unknown_slots(one)
    if not slots:
        try:
            return "meets" if inv_meets(S, S["ents"][i], CV()) else "fails"
        except Undetermined:
            return "und"
    slots = [((p[0], i) + tuple(p[2:]), d) for p, d in slots]
    doms = _domains(slots, CV())
    seen = set()
    for combo in itertools.product(*doms):
        T = assign(S, slots, combo) if slots else S
        try:
            seen.add(inv_meets(T, T["ents"][i], CV()))
        except Undetermined:
            seen.add("U")
    return "meets" if seen == {True} else ("fails" if seen == {False} else "und")


def _inv_fit(rng, card, pack, S, slot, plan) -> bool:
    ents = S["ents"]
    for i in range(len(ents)):
        want = "meets" if slot == i else "fails"
        for t in range(60):
            if _case_status(S, i) == want:
                break
            ents[i] = inv_ent(rng, card, pack, ents[i]["id"], {**plan, "_pt": [15, 30, 50, 70, 88][t % 5]})
        else:
            return False
    if plan["world"] == "open":
        if slot == "ABST":
            # shape (ii): no sure meet, >= 1 undetermined case
            idx = rng.randrange(len(ents))
            if not _make_unknown(rng, card, S, idx, want="und"):
                return False
        else:
            # shape (i): add 1-2 unknowns that leave every status as it is
            for _ in range(rng.choice([1, 1, 2])):
                idx = rng.randrange(len(ents))
                if not _make_unknown(rng, card, S, idx, want=_case_status(S, idx)):
                    return False
    try:
        r = solve(S, CV())
    except (Undetermined, ValueError):
        return False
    if plan["world"] == "closed":
        ok = (r["ans"] == slot) if slot != "ABST" else (r["ans"] == "NOTA")
    else:
        ok = (r["ans"] == slot) if slot != "ABST" else (r["ans"] == "CBD")
    if ok and plan["world"] == "closed":
        import errors as ER
        gold = r["ans"]
        if not ER.has_distractor(S, gold):
            _plant_boundary(rng, card, pack, S, slot, plan)
            try:
                r2 = solve(S, CV())
            except (Undetermined, ValueError):
                return False
            ok = r2["ans"] == gold
            if ok and not ER.has_distractor(S, gold):
                ok = _inv_force_distractor(rng, card, pack, S, slot, plan)
    return ok


def _inv_force_distractor(rng, card, pack, S, slot, plan) -> bool:
    """Make one named error (from the rule quantity's list) move the answer to another single option, by redrawing
    whole cases (each keeps its correct status). Cases are cached per error reading, so a redraw re-checks one case."""
    import errors as ER
    from solver_a import inv_meets
    qk = card["rules"]["inv"]["q"]["k"]
    cvs = [cv for eid in ER.INV_BY_Q.get(qk, []) for cv in ER.E[eid]]
    ents = S["ents"]
    n = len(ents)

    def row(i):
        out = []
        for cv in cvs:
            try:
                out.append(inv_meets(S, ents[i], cv))
            except (Undetermined, ValueError, ZeroDivisionError):
                out.append(None)
        return out
    M = [row(i) for i in range(n)]

    def found():
        for c in range(len(cvs)):
            col = [M[i][c] for i in range(n)]
            if None in col:
                continue
            meet = [i for i in range(n) if col[i]]
            if slot == "ABST":
                if len(meet) == 1:
                    return True
            elif len(meet) <= 1 and meet != [slot]:
                return True
        return False
    if found():
        return True
    pts = [15, 35, 55, 75, 90]
    for t in range(150):
        if slot != "ABST" and t % 3 == 0:
            i = slot
            want = "meets"
        else:
            i = rng.choice([x for x in range(n) if x != slot] or [slot])
            want = "fails"
        old = ents[i]
        ents[i] = inv_ent(rng, card, pack, old["id"], {**plan, "_pt": pts[t % len(pts)]})
        if _case_status(S, i) != want:
            ents[i] = old
            continue
        M[i] = row(i)
        if found():
            return ER.has_distractor(S, slot if slot != "ABST" else "NOTA")
    return False


def _plant_rescale(rng, S, v, k, op):
    """NOTA row on a '>= v' expected-loss rule: one failing case whose loss alone reaches v (so reading the chance as
    100%, E10, makes it qualify), every other failing case with a loss below v (so E10 moves no other case)."""
    if op != ">=":
        return
    ents = S["ents"]
    j = rng.randrange(len(ents))
    for i, e in enumerate(ents):
        if len(e.get("outs") or []) != 1:
            return
        o = e["outs"][0]
        c = e.get("cost") or 0 if k == "tec" else 0
        if i == j:
            hi = v - c
            if hi <= 0:
                return
            for _ in range(60):
                pk = rng.randint(2, 60)
                L_ = Fr(rng.randint(int(hi), int(hi * 100 / pk)))
                if Fr(pk, 100) * L_ + c < v <= L_ + c:
                    o["p"], o["prep"], o["pden"], o["a"] = Fr(pk, 100), "pct0", None, L_
                    break
        else:
            top = int(v - c) - 1
            if top < 100:
                return
            o["a"] = Fr(rng.randint(100, top) // 10 * 10 or 100)


def _plant_boundary(rng, card, pack, S, slot, plan):
    """Put one case exactly on the rule's comparison value, so that the comparator-inclusion error (E5) changes
    which case qualifies: a failing case on a strict comparison, or the qualifying case on an inclusive one."""
    r = card["rules"]["inv"]
    if r["kind"] != "q":
        return
    op, v, k = r["op"], r["v"], r["q"]["k"]
    strict = op in (">", "<")
    if strict:
        cands = [i for i in range(len(S["ents"])) if i != slot]
    elif slot != "ABST":
        cands = [slot]
    else:
        return
    if not cands:
        return
    i = rng.choice(cands)
    e = S["ents"][i]
    if k == "chance" and e.get("ch") is not None:
        e["ch"]["p"], e["ch"]["rep"], e["ch"]["den"] = v, "pct0", None
    elif k in ("el", "tec") and e.get("outs"):
        if slot == "ABST":
            _plant_rescale(rng, S, v, k, op)
            return
        o = e["outs"][0]
        base = v - (e.get("cost") or 0) if k == "tec" else v
        if len(e["outs"]) > 1 or base <= 0:
            return
        for _ in range(60):
            pk = rng.randint(2, 90)
            L_ = base * 100 / pk
            if L_.denominator == 1 and 100 <= L_ <= 60000:
                o["p"], o["prep"], o["pden"], o["a"] = Fr(pk, 100), "pct0", None, L_
                return
    elif k == "score":
        for t in range(400):
            ent = points_ent(rng, card, pack, e["id"], version=plan["version"], p_true=[15, 35, 55, 75][t % 4])
            S["ents"][i] = ent
            if quantity(S, ent, {"k": "score"}, CV()) == v:
                return
        S["ents"][i] = e


def _make_unknown(rng, card, S, i, want: str) -> bool:
    """Make one fact of case i unknown (with a stated range for numbers) so that its status becomes `want`."""
    rule = card["rules"]["inv"]
    tried = set()
    for _ in range(12):
        e = S["ents"][i]
        backup = copy.deepcopy(e)
        if "pts" in e:
            known = [f for f, v in e["pts"]["b"].items() if v is not None and f not in tried]
            if not known:
                return False
            f = rng.choice(known)
            tried.add(f)
            e["pts"]["b"][f] = None
            e["pts"]["stated"][f] = True
        elif e.get("ch") is not None and e["ch"]["p"] is not None:
            v = e["ch"]["p"]
            ref = rule["v"] if rule["kind"] == "q" and rule["q"]["k"] == "chance" else v
            w = Fr(rng.randint(2, 30), 100)
            if want == "und":
                lo, hi = min(v, ref) - w, max(v, ref) + w
            else:
                lo, hi = v - Fr(rng.randint(1, 4), 100), v + Fr(rng.randint(1, 4), 100)
            lo = max(Fr(0), Fr(math.floor(lo * 100), 100))
            hi = min(Fr(1), Fr(math.ceil(hi * 100), 100))
            e["ch"]["p"], e["ch"]["rng"] = None, (lo, hi)
        elif e.get("outs") and e["outs"][0]["p"] is not None:
            o = e["outs"][0]
            others = sum(x["p"] for x in e["outs"][1:])
            w = Fr(rng.randint(2, 30), 100) if want == "und" else Fr(rng.randint(1, 4), 100)
            lo = max(Fr(0), Fr(math.floor((o["p"] - w) * 100), 100))
            hi = min(_pfloor(1 - others), Fr(math.ceil((o["p"] + w) * 100), 100))
            o["p"], o["prng"], o["prng_show"] = None, (lo, hi), True
        else:
            return False
        if _case_status(S, i) == want:
            return True
        S["ents"][i] = backup
    return False


GEN = {"yn_thr": gen_yn_thr, "yn_act": gen_yn_act, "bin": gen_bin, "tier": gen_tier, "mat": gen_mat,
       "rank_top": gen_rank_top, "rank_order": gen_rank_order, "dec": gen_dec, "pred": gen_pred, "inv": gen_inv}
