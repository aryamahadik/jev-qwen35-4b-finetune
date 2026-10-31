"""rk_multi: best-of-N selection among candidates described by attributes, under explicit rules (mandatory
requirements with exceptions, weighted criteria, cost formulas, points bands, best-value price ratios, lexicographic
priority, judging panels, points formulas, first-qualifying-in-order), with stated tie-breaks, distractor attributes
that no rule uses, missing values, printed corrections, mixed units and hypothetical questions.

sample(rng) -> spec (see rk_core); render(spec) -> (state, instructions, options, gold, edges); twin(spec, rng) ->
(spec2, description) where exactly one fact differs and the outcome differs.
"""
import copy
import random
import re
from fractions import Fraction as Fr

from rk_core import (NONE, TIE, UNDET, comp_attrs, cval, evaluate, fix_articles, fmt_date, fmt_dec, fmt_dt, fmt_dur, fmt_int,
                     fmt_money, fmt_time, ranking, used_attrs)
from rk_domains import CTX_HYPO, DOM, DOMAINS

LETTERS = "ABCDEFGH"
MECH_W = {"weighted": 0.30, "cost": 0.24, "banded": 0.12, "ratio": 0.08, "lexi": 0.12, "panel": 0.08,
          "linear": 0.07, "first": 0.05}
NAMECOL = {"laptops": "Supplier", "catering": "Caterer", "cleaning": "Contractor", "freight": "Carrier",
           "saas": "Product", "construction": "Contractor", "translation": "Agency", "venue": "Venue",
           "movers": "Company", "lease": "Address", "phone": "Provider", "energy": "Tariff name",
           "flights": "Airline and flight", "hotels": "Hotel", "grants": "Organisation", "seedfund": "Project",
           "hiring": "Name", "sports": "Name", "agents": "Name", "patches": "Author", "printing": "Print shop",
           "insurance": "Insurer", "coach": "Company", "rental": "Address"}
NO_RECV = {"flights", "hotels", "sports", "agents", "energy", "phone", "rental"}
TABLE_LAYOUTS = {"md", "pipe", "csv", "tsv", "fixed", "transposed"}
LAYOUTS = ["md", "pipe", "csv", "tsv", "fixed", "records", "bullets", "prose", "transposed", "kv", "numbered"]
RULE_STYLES = ["bullets", "numbered", "prose", "steps"]
WRAPS = ["plain", "email", "memo", "ticket"]


def art(w, cap=False):
    a = "an" if w[0].lower() in "aeiou" else "a"
    return a.capitalize() if cap else a


def lw_of(word):
    return word if word == "PR" else word.lower()


def plural(w):
    if w == "PR":
        return "PRs"
    if w.endswith(("ch", "sh", "s", "x")):
        return w + "es"
    if w.endswith("y") and w[-2] not in "aeiou":
        return w[:-1] + "ies"
    return w + "s"


def special_opts(word, kind):
    lw = lw_of(word)
    none = f"no {lw} qualifies"
    if kind == "best":
        return [none, "tie not settled by the rules", "cannot be determined"]
    return ["tie not settled by the rules", "cannot be determined"]


def gold_option(sc, out):
    sp = special_opts(sc["word"], sc["target"]["kind"])
    if out == NONE:
        assert sc["target"]["kind"] == "best", "NONE outcome needs a 'no <x> qualifies' option"
        return sp[0]
    if out == TIE:
        return "tie not settled by the rules"
    if out == UNDET:
        return "cannot be determined"
    return out


# ------------------------------------------------------------------------------------------------ value generation
def rand_val(A, rng, sc):
    k = A["kind"]
    if k in ("money", "num"):
        if A["hi"] <= A["lo"]:
            return A["lo"]
        return rng.randrange(A["lo"], A["hi"] + 1, A["step"])
    if k == "score":
        lo, hi = sc["scale"]
        return rng.randint(lo, hi)
    if k == "bool":
        return rng.random() < A["p"]
    if k == "cat":
        return rng.choice(A["vals"])
    raise ValueError(k)


def kind_of(A):
    return {"money": "num", "num": "num", "score": "num", "bool": "bool", "cat": "cat", "recv": "num"}[A["kind"]]


def gen_ctx(dom, rng):
    ctx = {}
    for k, spec in dom["ctx"].items():
        if isinstance(spec, tuple):
            ctx[k] = rng.randrange(spec[0], spec[1] + 1, spec[2])
        else:
            ctx[k] = rng.choice(spec)
    if dom["key"] == "saas":
        ctx["months"] = ctx["years"] * 12
    if dom["key"] == "coach":
        ctx["people"] = ctx["pupils"] + ctx["staff"]
    return ctx


def weights_100(rng, k):
    while True:
        cuts = sorted(rng.sample(range(2, 19), k - 1))
        parts = [b - a for a, b in zip([0] + cuts, cuts + [20])]
        if all(p >= 2 for p in parts) and len(set(parts)) > 1:
            return [5 * p for p in parts]


def choose_mech(dom, rng):
    ms = [m for m in dom["mechs"] if m != "weighted" or len(dom["scores"]) >= 2]
    ms = [m for m in ms if m != "ratio" or (dom["cost"] and dom["scores"])]
    return rng.choices(ms, weights=[MECH_W[m] for m in ms])[0]


def num_attrs(dom):
    return [a for a, A in dom["A"].items() if A["kind"] in ("money", "num")]


# ------------------------------------------------------------------------------------------------ sampling
def sample(rng, dom=None, mech=None, kind=None):
    dom = dom or rng.choice(DOMAINS)
    A = dom["A"]
    mech = mech or choose_mech(dom, rng)
    n = rng.choices([3, 4, 5, 6, 7, 8], weights=[18, 30, 26, 15, 8, 3])[0]
    if mech == "panel":
        n = min(n, 6)
    word, scheme = rng.choice(dom["labels"])
    labels = [f"{word} {LETTERS[k] if scheme == 'L' else k + 1}" for k in range(n)]
    names = rng.sample(dom["names"], n)
    ctx = gen_ctx(dom, rng)
    sc = {"dom": dom["key"], "word": word, "cands": [{"label": labels[k], "name": names[k], "v": {}} for k in range(n)],
          "kinds": {}, "gates": [], "mech": None, "tb": [], "tb_final": "lots",
          "missing": {"score": None, "bool": None}, "enum": {}, "corr": [], "ctx": ctx,
          "target": {"kind": "best", "hypo": None}, "scores": list(dom["scores"]),
          "cost_comp": dom["cost"]["comp"] if dom["cost"] else None, "scale": None, "alt": [], "show": [],
          "gate_meta": [], "r": {}}
    sc["scale"] = rng.choice([(1, 5), (1, 10), (0, 10)])
    used = []
    # mechanism
    if mech == "weighted":
        k = min(len(dom["scores"]), rng.choice([2, 3, 3, 4]))
        crit = rng.sample(dom["scores"], k)
        style = rng.choice(["pct", "pct", "mult", "points"])
        if style == "mult":
            while True:
                ws = [rng.randint(1, 4) for _ in crit]
                if len(set(ws)) > 1:
                    break
            div = 1
        else:
            ws = weights_100(rng, k)
            div = 100 if style == "pct" else sc["scale"][1]
        sc["mech"] = {"type": "weighted", "crit": [[a, w] for a, w in zip(crit, ws)], "div": div, "style": style}
        used += crit
    elif mech == "cost":
        sc["mech"] = {"type": "cost", "comp": dom["cost"]["comp"]}
        used += comp_attrs(dom["cost"]["comp"])
    elif mech == "banded":
        k = min(len(dom["band"]), rng.choice([2, 2, 3]))
        ba = rng.sample(dom["band"], k)
        sc["mech"] = {"type": "banded", "bands": [[a, None] for a in ba]}
        used += ba
    elif mech == "ratio":
        q = rng.choice(dom["scores"])
        wp = rng.choice([30, 40, 50, 60])
        sc["mech"] = {"type": "ratio", "comp": dom["cost"]["comp"], "wp": wp, "qual": q, "wq": 100 - wp,
                      "qmax": sc["scale"][1]}
        used += comp_attrs(dom["cost"]["comp"]) + [q]
    elif mech == "lexi":
        keys = list(dom["lexi"])
        first = keys[0] if rng.random() < 0.5 else rng.choice(keys)
        rest = [x for x in keys if x != first]
        rng.shuffle(rest)
        keys = [first] + rest[:rng.choice([1, 2])]
        sc["mech"] = {"type": "lexi", "keys": [list(x) for x in keys]}
        used += [a for a, _ in keys]
    elif mech == "panel":
        J = rng.choice([3, 4, 4, 5])
        aggs = ["mean", "median", "sum"] + (["trim", "trim"] if J >= 4 else [])
        sc["mech"] = {"type": "panel", "agg": rng.choice(aggs), "judges": J,
                      "pscale": rng.choice([(1, 10), (0, 20), (1, 5)])}
        sc["kinds"]["panel"] = "panel"
    elif mech == "linear":
        terms = [[a, rng.choice(cs)] for a, cs, _ in dom["linear"]]
        if len(terms) > 3 and rng.random() < 0.4:
            terms.pop(rng.randrange(1, len(terms)))
        sc["mech"] = {"type": "linear", "terms": terms}
        used += [a for a, _ in terms]
    elif mech == "first":
        sc["mech"] = {"type": "first"}
        used.append("received")
    # gates
    ng = rng.choices([0, 1, 2, 3], weights=[18, 36, 31, 15])[0]
    if mech == "first":
        ng = max(ng, 2)
    pool = list(dom["gates"])
    rng.shuffle(pool)
    forced = [g for g in pool if g.get("ctxt") and (g["ctxt"] != "tests" or rng.random() < 0.6)]
    pool = forced + [g for g in pool if g not in forced]
    ng = max(ng, len(forced))
    seen = set()
    for g in pool:
        if len(sc["gates"]) >= ng:
            break
        if g["a"] in seen:
            continue
        seen.add(g["a"])
        Ag = A[g["a"]]
        gm = {"style": rng.choice(["pos", "pos", "neg", "dneg"])}
        if Ag["kind"] == "bool":
            if g.get("exc") and rng.random() < 0.7:
                gate = {"a": g["a"], "op": "true", "t": None, "exc": {"a": g["exc"]["a"], "mode": "waive", "t2": None}}
                used.append(g["exc"]["a"])
            elif g.get("exc"):
                continue
            else:
                gate = {"a": g["a"], "op": "false" if g.get("neg") else "true", "t": None, "exc": None}
        elif Ag["kind"] == "cat":
            gate = {"a": g["a"], "op": "in", "t": list(g["ok"]), "exc": None}
            gm["vb"], gm["vb3"] = g["vb"], g["vb3"]
        else:
            op = rng.choice(g["ops"])
            gate = {"a": g["a"], "op": op, "t": None, "exc": None}
            if g.get("zero"):
                gate["op"], gate["t"] = "le", 0
                gm["zero"] = True
            if g.get("ctxt"):
                gm["ctxt"] = g["ctxt"]
            if g.get("exc") and rng.random() < 0.6:
                gate["exc"] = {"a": g["exc"]["a"], "mode": g["exc"]["mode"], "t2": None, "d": g["exc"].get("d", 0)}
                used.append(g["exc"]["a"])
        sc["gates"].append(gate)
        sc["gate_meta"].append(gm)
        used.append(g["a"])
    # deadline gate (temporal)
    if dom["key"] not in NO_RECV and (rng.random() < 0.10 or (mech == "first" and rng.random() < 0.3)):
        sc["gates"].append({"a": "received", "op": "le", "t": None, "exc": None})
        sc["gate_meta"].append({"style": rng.choice(["pos", "neg"]), "deadline": True})
        used.append("received")
    # tie-breaks
    if mech in ("weighted", "cost", "banded", "ratio", "panel", "linear"):
        pool = [(a, d, p) for a, d, p in dom["tb"]]
        if mech == "weighted":
            pool += [(c, "high", f"the higher {A[c]['hdr'].lower()} score") for c, _ in sc["mech"]["crit"]] * 2
        if dom["cost"] and mech not in ("cost", "ratio"):
            pool.append(("@cost", "low", "the lower total cost"))
        if mech == "cost":
            pool = [x for x in pool if x[0] not in comp_attrs(dom["cost"]["comp"])] or pool
        rng.shuffle(pool)
        k = rng.choice([1, 1, 2])
        tbs = []
        for a, d, p in pool:
            if a in [x[0] for x in tbs]:
                continue
            tbs.append((a, d, p))
            if len(tbs) >= k:
                break
        sc["tb"] = [[a, d] for a, d, _ in tbs]
        sc["r"]["tb_phr"] = [p for _, _, p in tbs]
        for a, _, _ in tbs:
            if a == "@cost":
                used += comp_attrs(dom["cost"]["comp"])
            else:
                used.append(a)
        if rng.random() < 0.45 and dom["key"] not in NO_RECV:
            sc["tb"].append(["received", "low"])
            sc["r"]["tb_phr"].append("the earlier submission")
            sc["tb_final"] = "none"
            used.append("received")
    elif mech == "lexi":
        sc["r"]["tb_phr"] = []
        if rng.random() < 0.4 and dom["key"] not in NO_RECV:
            sc["tb"] = [["received", "low"]]
            sc["r"]["tb_phr"] = ["the earlier submission"]
            sc["tb_final"] = "none"
            used.append("received")
    else:
        sc["r"]["tb_phr"] = []
        sc["tb_final"] = "none"
    used = list(dict.fromkeys(used))
    # displayed attributes: used + distractors
    extra = rng.sample(dom["dist"], min(len(dom["dist"]), rng.choice([1, 2, 2, 3])))
    others = [a for a in A if a not in used and a not in extra and a not in dom["dist"]]
    rng.shuffle(others)
    extra += others[:rng.choice([0, 1, 1, 2])]
    if "received" not in used and rng.random() < 0.15 and dom["key"] not in NO_RECV:
        extra.append("received")
    gated = {g["a"] for g in sc["gates"]}
    extra = [a for a in extra if (a not in dom["must"] or a in gated) and a not in used]
    show = list(dict.fromkeys([a for a in used if a != "panel"] + extra))
    rng.shuffle(show)
    sc["show"] = show
    for a in show:
        sc["kinds"][a] = "num" if a == "received" else kind_of(A[a])
    # values
    for c in sc["cands"]:
        for a in show:
            if a == "received":
                continue
            c["v"][a] = rand_val(A[a], rng, sc)
    if dom["key"] == "patches":
        for c in sc["cands"]:
            c["v"]["passed"] = sc["ctx"]["tests"] if rng.random() < 0.72 else sc["ctx"]["tests"] - rng.randint(1, 6)
    if dom["key"] == "printing":
        for c in sc["cands"]:
            if "bulk" in c["v"] and "unit" in c["v"]:
                c["v"]["bulk"] = max(20, c["v"]["unit"] - rng.randrange(2, max(3, c["v"]["unit"] // 3)))
    if mech == "panel":
        lo, hi = sc["mech"]["pscale"]
        for c in sc["cands"]:
            base = rng.randint(lo + (hi - lo) // 4, hi - (hi - lo) // 5)
            c["v"]["panel"] = [max(lo, min(hi, base + rng.randint(-(hi - lo) // 4 - 1, (hi - lo) // 4 + 1)))
                               for _ in range(sc["mech"]["judges"])]
    sc["r"]["date"] = rng.randrange(20, 330)
    if "received" in show:
        d0 = sc["r"]["date"]
        dl = d0 * 1440 + rng.choice([12 * 60, 17 * 60, 16 * 60 + 30, 23 * 60 + 59, 9 * 60])
        sc["ctx"]["_deadline"] = dl
        stamps = set()
        for c in sc["cands"]:
            while True:
                st = dl - rng.randrange(0, 3 * 1440) + (rng.randrange(1, 600) if rng.random() < 0.2 else 0)
                if st not in stamps:
                    break
            stamps.add(st)
            c["v"]["received"] = st
        if rng.random() < 0.3:
            c = rng.choice(sc["cands"])
            if dl not in stamps:
                c["v"]["received"] = dl
    # gate thresholds
    for gi, g in enumerate(sc["gates"]):
        gm = sc["gate_meta"][gi]
        if g["a"] == "received":
            g["t"] = sc["ctx"]["_deadline"]
            continue
        if g["op"] in ("true", "false", "in") or gm.get("zero"):
            continue
        Ag = A[g["a"]]
        if gm.get("ctxt"):
            ck = gm["ctxt"]
            g["t"] = sc["ctx"][ck]
            # make a few candidates fail / sit on the boundary
            for c in sc["cands"]:
                if g["a"] == "passed":
                    continue
                r = rng.random()
                good = g["op"] in ("ge", "gt")
                if r < 0.25:
                    c["v"][g["a"]] = g["t"] - Ag["step"] * rng.randint(1, 5) if good else g["t"] + Ag["step"] * rng.randint(1, 5)
                elif r < 0.35:
                    c["v"][g["a"]] = g["t"]
                elif r < 1.0:
                    c["v"][g["a"]] = g["t"] + Ag["step"] * rng.randint(0, 40) if good else g["t"] - Ag["step"] * rng.randint(0, 40)
                c["v"][g["a"]] = max(Ag["lo"] if Ag["lo"] > 0 else 0, c["v"][g["a"]])
            continue
        vals = sorted(c["v"][g["a"]] for c in sc["cands"])
        if rng.random() < 0.55:
            g["t"] = rng.choice(vals)
        else:
            j = rng.randrange(len(vals))
            g["t"] = vals[j] + (Ag["step"] if g["op"] in ("le", "lt") else -Ag["step"]) * rng.randint(0, 2)
        if g["exc"] and g["exc"]["mode"] == "relax":
            g["exc"]["t2"] = g["t"] + g["exc"]["d"] if g["op"] in ("le", "lt") else g["t"] - g["exc"]["d"]
    # banded mechanism: bands around the observed values
    if mech == "banded":
        for pair in sc["mech"]["bands"]:
            a = pair[0]
            pair[1] = make_bands(A[a], [c["v"][a] for c in sc["cands"]], rng)
    # units: mixed display (per year vs per month, weeks vs days)
    alt_ok = [a for a in show if A.get(a, {}).get("alt") and a in used]
    if alt_ok and rng.random() < 0.4:
        a = rng.choice(alt_ok)
        alt = A[a]["alt"]
        for i, c in enumerate(sc["cands"]):
            if rng.random() < 0.45:
                if alt == "weeks":
                    w = max(1, round(c["v"][a] / 7))
                    c["v"][a] = 7 * w
                elif alt == "month12":
                    c["v"][a] -= c["v"][a] % 12
                sc["alt"].append([i, a])
    # target
    kind = kind or rng.choices(["best", "second", "last", "hypo"], weights=[58, 13, 11, 18])[0]
    if mech == "first" and kind in ("second", "last"):
        kind = "best"
    if kind == "hypo":
        h = pick_hypo(sc, dom, rng)
        if h is None:
            kind = "best"
        else:
            sc["target"] = {"kind": "best", "hypo": h}
    if kind != "hypo":
        sc["target"] = {"kind": kind, "hypo": None}
    # render choices
    r = sc["r"]
    r.update({"layout": rng.choice(LAYOUTS), "rules": rng.choice(RULE_STYLES), "wrap": rng.choices(WRAPS, [5, 2, 2, 1])[0],
              "rules_first": rng.random() < 0.65, "score_style": rng.choice(["slash", "plain"]),
              "tstyle": rng.randint(0, 1), "dstyle": rng.randint(0, 2), "durstyle": rng.randint(0, 2),
              "intro": rng.randrange(100), "title": rng.randrange(100), "q": rng.randrange(1000), "num": rng.randint(100, 9899),
              "miss_tok": rng.randrange(3), "hdr": rng.randrange(6),
              "name_style": rng.randrange(3), "person": rng.choice(["Dana Whitfield", "Sam Okoro", "Priti Shah",
                                                                     "Marco Bellini", "Ruth Adler", "Jin Park"]),
              "wprefix": rng.randrange(4), "tb_style": rng.randrange(3), "mstyle": rng.randrange(3)})
    r["gate_phr"] = [rng.randrange(3) for _ in sc["gates"]]
    return sc


def make_bands(Aa, vals, rng):
    """Three (or four) bands with cut points at or near observed values; lo/hi inclusive (None = open)."""
    step = Aa.get("step", 1)
    s = sorted(set(vals))
    lo_all, hi_all = Aa["lo"], Aa["hi"]
    for _ in range(20):
        if len(s) >= 3 and rng.random() < 0.7:
            c1, c2 = sorted(rng.sample(s, 2))
        else:
            c1 = rng.randrange(lo_all, hi_all + 1, step)
            c2 = rng.randrange(lo_all, hi_all + 1, step)
            c1, c2 = sorted((c1, c2))
        if c2 - c1 >= 2 * step:
            break
    else:
        c1, c2 = lo_all + (hi_all - lo_all) // 3, lo_all + 2 * (hi_all - lo_all) // 3
        c1 -= (c1 - lo_all) % step
        c2 -= (c2 - lo_all) % step
    pts = rng.choice([(10, 6, 2), (5, 3, 0), (8, 4, 1), (20, 10, 0), (3, 2, 1)])
    exact = Aa["kind"] == "num" and Aa.get("dp", 0) == 0 and step == 1
    better = Aa["better"] or "low"
    if exact:  # integer inclusive bands: <= c1, c1+1..c2, > c2
        bands = [[None, c1], [c1 + 1, c2], [c2 + 1, None]]
    else:  # half-open bands in minor units: < c1, c1 .. < c2, >= c2
        bands = [[None, c1 - 1], [c1, c2 - 1], [c2, None]]
    if better == "low":
        return [[b[0], b[1], p] for b, p in zip(bands, pts)]
    return [[b[0], b[1], p] for b, p in zip(bands, reversed(pts))]


def pick_hypo(sc, dom, rng):
    opts = ["withdraw"] * 3
    m = sc["mech"]
    if m["type"] == "weighted" and len(m["crit"]) >= 3:
        opts += ["drop"] * 2
    numg = [i for i, g in enumerate(sc["gates"]) if g["op"] in ("ge", "gt", "le", "lt") and not
            sc["gate_meta"][i].get("zero") and g["a"] not in ("received", "passed") and not g.get("exc")]
    boolg = [i for i, g in enumerate(sc["gates"]) if g["op"] in ("true", "false", "in") and not g.get("exc")]
    if numg:
        opts += ["gate"] * 2
    if boolg:
        opts += ["nogate"] * 2
    ck = [k for c in (m.get("comp") or []) if c[0] == "mul" for k in c[2] if k in CTX_HYPO and k in dom["ctx"]]
    ck += [k for c in (m.get("comp") or []) if c[0] == "tier" for k in [c[4]] if k in CTX_HYPO and k in dom["ctx"]]
    if m["type"] in ("cost", "ratio") and ck:
        opts += ["ctx"] * 3
    t = rng.choice(opts)
    if t == "withdraw":
        return {"type": "withdraw", "i": rng.randrange(len(sc["cands"]))}
    if t == "drop":
        return {"type": "drop", "a": rng.choice(m["crit"])[0]}
    if t == "gate":
        gi = rng.choice(numg)
        g = sc["gates"][gi]
        A = DOM[sc["dom"]]["A"][g["a"]]
        st = A.get("step", 1)
        delta = st * rng.choice([1, 2, 3, 5, 10])
        loosen = rng.random() < 0.6
        up = (g["op"] in ("le", "lt")) == loosen
        return {"type": "gate", "g": gi, "t": None, "delta": delta if up else -delta}
    if t == "nogate":
        return {"type": "nogate", "g": rng.choice(boolg)}
    k = rng.choice(sorted(set(ck)))
    spec = DOM[sc["dom"]]["ctx"][k]
    return {"type": "ctx", "k": k, "v": None, "spec": list(spec) if isinstance(spec, tuple) else list(spec)}


def finalize_hypo(sc, rng):
    h = sc["target"]["hypo"]
    if not h:
        return True
    if h["type"] == "gate":
        g = sc["gates"][h["g"]]
        if g["t"] is None:
            return False
        h["t"] = g["t"] + h.pop("delta") if "delta" in h else h["t"]
        if h["t"] == g["t"] or h["t"] < 0:
            return False
    if h["type"] == "ctx" and h["v"] is None:
        spec = h.pop("spec")
        cur = sc["ctx"][h["k"]]
        if len(spec) == 3 and all(isinstance(x, int) for x in spec) and spec[1] > spec[0] + spec[2] * 3:
            for _ in range(30):
                v = rng.randrange(spec[0], spec[1] + 1, spec[2])
                if v != cur:
                    break
        else:
            vals = [x for x in spec if x != cur]
            if not vals:
                return False
            v = rng.choice(vals)
        if v == cur:
            return False
        h["v"] = v
    return True


# ------------------------------------------------------------------------------------------------ tie forcing
def force_tie(sc, rng):
    """Edit one mechanism value of an adjacent competitor so that it ties the other on the primary metric."""
    m = sc["mech"]
    if m["type"] not in ("weighted", "cost", "banded", "linear", "panel"):
        return False
    try:
        order, keys = ranking(sc)
    except KeyError:
        return False
    if len(order) < 2:
        return False
    kind = sc["target"]["kind"]
    pos = {"best": 0, "second": rng.choice([0, 1]), "last": len(order) - 2}[kind]
    if pos + 1 >= len(order) or pos < 0:
        return False
    lab_x, lab_y = order[pos], order[pos + 1]
    ix = [c["label"] for c in sc["cands"]].index(lab_x)
    iy = [c["label"] for c in sc["cands"]].index(lab_y)
    target_p = keys[pos][0]
    A = DOM[sc["dom"]]["A"]
    tries = []
    if m["type"] == "weighted":
        for a, _ in m["crit"]:
            lo, hi = sc["scale"]
            tries += [(a, v) for v in range(lo, hi + 1)]
    elif m["type"] == "cost":
        for a in comp_attrs(m["comp"]):
            Aa = A.get(a)
            if Aa and Aa["kind"] == "money":
                cur = sc["cands"][iy]["v"][a]
                tries += [(a, cur + d * Aa["step"]) for d in range(-60, 61)]
    elif m["type"] == "banded":
        for a, bands in m["bands"]:
            for lo, hi, _ in bands:
                if lo is not None:
                    tries.append((a, lo))
                if hi is not None:
                    tries.append((a, hi))
    elif m["type"] == "linear":
        for a, _ in m["terms"]:
            cur = sc["cands"][iy]["v"][a]
            tries += [(a, cur + d) for d in range(-8, 9) if cur + d >= 0]
    elif m["type"] == "panel":
        xs = sc["cands"][iy]["v"]["panel"]
        lo, hi = m["pscale"]
        for j in range(len(xs)):
            tries += [(("panel", j), v) for v in range(lo, hi + 1)]
    rng.shuffle(tries)
    for a, v in tries:
        s2 = copy.deepcopy(sc)
        if isinstance(a, tuple):
            s2["cands"][iy]["v"]["panel"][a[1]] = v
        else:
            Aa = A[a]
            if Aa["kind"] in ("money", "num") and not (Aa["lo"] <= v <= Aa["hi"]):
                continue
            if cval(s2, iy, a) is None:
                continue
            if any(ci == iy and ca == a for ci, ca, _ in s2["corr"]):
                continue
            s2["cands"][iy]["v"][a] = v
        try:
            o2, k2 = ranking(s2)
        except KeyError:
            continue
        if lab_x in o2 and lab_y in o2 and len(o2) == len(order):
            kx = k2[o2.index(lab_x)][0]
            ky = k2[o2.index(lab_y)][0]
            if kx == ky == target_p or (kx == ky and m["type"] == "cost"):
                sc.clear()
                sc.update(s2)
                return True
    return False


# ------------------------------------------------------------------------------------------------ missing values / corrections
def add_missing(sc, rng):
    m = sc["mech"]
    cand_attrs = []
    if m["type"] == "weighted":
        cand_attrs += [a for a, _ in m["crit"]]
    if m["type"] == "ratio":
        cand_attrs.append(m["qual"])
    for g in sc["gates"]:
        if sc["kinds"].get(g["a"]) == "bool" and not g.get("exc"):
            cand_attrs.append(g["a"])
    if not cand_attrs:
        return False
    a = rng.choice(cand_attrs)
    try:
        order, _ = ranking(sc)
    except KeyError:
        return False
    labs = [c["label"] for c in sc["cands"]]
    if order and rng.random() < 0.7:
        i = labs.index(rng.choice(order[:2]))
    else:
        i = rng.randrange(len(labs))
    sc["cands"][i]["v"][a] = None
    is_score = a in sc["scores"]
    if rng.random() < 0.45:
        if is_score:
            sc["missing"]["score"] = "zero"
        else:
            sc["missing"]["bool"] = "fail"
    lo, hi = sc["scale"]
    sc["enum"][a] = list(range(lo, hi + 1)) if is_score else [True, False]
    return True


def add_correction(sc, rng):
    A = DOM[sc["dom"]]["A"]
    used = [a for a in used_attrs(sc) if a in A and A[a]["kind"] in ("money", "num", "score")
            and a not in ("received",) and all(a != x[1] for x in sc["alt"])]
    if not used:
        return False
    a = rng.choice(used)
    i = rng.randrange(len(sc["cands"]))
    cur = sc["cands"][i]["v"].get(a)
    if cur is None:
        return False
    Aa = A[a]
    for _ in range(20):
        if Aa["kind"] == "score":
            lo, hi = sc["scale"]
            nv = rng.randint(lo, hi)
        else:
            nv = cur + Aa["step"] * rng.choice([-10, -5, -3, -2, -1, 1, 2, 3, 5, 10])
            if not (Aa["lo"] <= nv <= Aa["hi"]):
                continue
        if nv != cur:
            sc["corr"].append([i, a, nv])
            sc["r"]["corr_date"] = rng.randrange(1, 4)
            return True
    return False


# ------------------------------------------------------------------------------------------------ twin search
def candidate_values(sc, a, cur, i):
    A = DOM[sc["dom"]]["A"]
    Aa = A.get(a)
    if a == "received":
        dl = sc["ctx"].get("_deadline", cur)
        vals = [dl, dl + 1, dl - 1, dl + 30, dl - 30, cur + 60, cur - 60, cur + 1440, cur - 1440]
        vals += [c["v"]["received"] + d for c in sc["cands"] for d in (-1, 1)]
        taken = {c["v"]["received"] for k, c in enumerate(sc["cands"]) if k != i}
        return [v for v in dict.fromkeys(vals) if v != cur and v not in taken]
    k = Aa["kind"]
    if k == "bool":
        return [not cur] if cur is not None else [True, False]
    if k == "cat":
        return [x for x in Aa["vals"] if x != cur]
    if k == "score":
        lo, hi = sc["scale"]
        return [v for v in range(lo, hi + 1) if v != cur]
    st = Aa["step"]
    vals = []
    if cur is not None:
        vals += [cur + d * st for d in (1, -1, 2, -2, 3, -3, 5, -5, 10, -10, 20, -20)]
    for g in sc["gates"]:
        if g["a"] == a and g["t"] is not None and not isinstance(g["t"], list):
            vals += [g["t"], g["t"] + st, g["t"] - st]
    vals += [c["v"].get(a) for c in sc["cands"] if c["v"].get(a) is not None]
    alt = [x for x in sc["alt"] if x[0] == i and x[1] == a]
    out = []
    for v in dict.fromkeys(vals):
        if v is None or v == cur:
            continue
        if a == "passed":
            if not (0 <= v <= sc["ctx"]["tests"]):
                continue
        elif not (Aa["lo"] <= v <= Aa["hi"]):
            continue
        if alt and Aa["alt"] == "weeks" and v % 7:
            continue
        if alt and Aa["alt"] == "month12" and v % 12:
            continue
        if (v - Aa["lo"]) % st and a != "passed":
            continue
        out.append(v)
    return out


def edits(sc, rng):
    """All single-fact edits (description, new spec)."""
    out = []
    ua = used_attrs(sc)
    A = DOM[sc["dom"]]["A"]
    for i, c in enumerate(sc["cands"]):
        for a in ua:
            if a == "panel":
                for j, x in enumerate(c["v"]["panel"]):
                    lo, hi = sc["mech"]["pscale"]
                    for v in range(max(lo, x - 3), min(hi, x + 3) + 1):
                        if v != x:
                            s2 = copy.deepcopy(sc)
                            s2["cands"][i]["v"]["panel"][j] = v
                            out.append(({"type": "judge", "i": i, "j": j, "old": x, "new": v}, s2, abs(v - x)))
                continue
            corr = [k for k, (ci, ca, _) in enumerate(sc["corr"]) if ci == i and ca == a]
            if corr:
                k = corr[0]
                cur = sc["corr"][k][2]
                for v in candidate_values(sc, a, cur, i)[:12]:
                    s2 = copy.deepcopy(sc)
                    s2["corr"][k][2] = v
                    out.append(({"type": "correction", "i": i, "a": a, "old": cur, "new": v}, s2, 1))
                continue
            cur = c["v"].get(a)
            if cur is None:
                for v in sc["enum"].get(a, []):
                    s2 = copy.deepcopy(sc)
                    s2["cands"][i]["v"][a] = v
                    out.append(({"type": "fill", "i": i, "a": a, "old": None, "new": v}, s2, 1))
                continue
            vals = candidate_values(sc, a, cur, i)
            for rank, v in enumerate(vals[:16]):
                s2 = copy.deepcopy(sc)
                s2["cands"][i]["v"][a] = v
                mag = rank + 1
                out.append(({"type": "cell", "i": i, "a": a, "old": cur, "new": v}, s2, mag))
            if a in sc["enum"] and rng.random() < 0.5:
                s2 = copy.deepcopy(sc)
                s2["cands"][i]["v"][a] = None
                out.append(({"type": "blank", "i": i, "a": a, "old": cur, "new": None}, s2, 3))
    for gi, g in enumerate(sc["gates"]):
        if g["op"] in ("ge", "gt", "le", "lt") and not sc["gate_meta"][gi].get("zero") and g["a"] != "received" \
                and not sc["gate_meta"][gi].get("ctxt"):
            st = A[g["a"]]["step"]
            for d in (1, -1, 2, -2, 3, -3, 5, -5):
                s2 = copy.deepcopy(sc)
                s2["gates"][gi]["t"] = g["t"] + d * st
                if s2["gates"][gi]["t"] < 0:
                    continue
                if g.get("exc") and g["exc"]["mode"] == "relax":
                    s2["gates"][gi]["exc"]["t2"] = g["exc"]["t2"] + d * st
                out.append(({"type": "gate", "g": gi, "old": g["t"], "new": g["t"] + d * st}, s2, abs(d) + 1))
    m = sc["mech"]
    ck = []
    for comp in (m.get("comp") or []) + ((sc["cost_comp"] or []) if any(a == "@cost" for a, _ in sc["tb"]) else []):
        if comp[0] == "mul":
            ck += [k for k in comp[2] if not k.startswith("@") and k in CTX_HYPO]
        if comp[0] == "tier":
            ck.append(comp[4])
    for gi, g in enumerate(sc["gates"]):
        if sc["gate_meta"][gi].get("ctxt") and sc["gate_meta"][gi]["ctxt"] in sc["ctx"] and \
                sc["gate_meta"][gi]["ctxt"] not in ("people", "tests"):
            ck.append(sc["gate_meta"][gi]["ctxt"])
    for k in dict.fromkeys(ck):
        if k not in DOM[sc["dom"]]["ctx"]:
            continue
        spec = DOM[sc["dom"]]["ctx"].get(k)
        cur = sc["ctx"][k]
        if isinstance(spec, tuple):
            cands = [cur + d * spec[2] for d in (1, -1, 2, -2, 5, -5, 10, -10, 20, -20, 40, -40)]
            cands = [v for v in cands if spec[0] <= v <= spec[1]]
        elif isinstance(spec, list):
            cands = [v for v in spec if v != cur]
        else:
            continue
        for v in cands:
            s2 = copy.deepcopy(sc)
            s2["ctx"][k] = v
            h = s2["target"].get("hypo")
            if h and h["type"] == "ctx" and h["k"] == k and h["v"] == v:
                continue
            out.append(({"type": "ctx", "k": k, "old": cur, "new": v}, s2, 2))
    if m["type"] == "weighted" and m.get("style") == "mult":
        for ci, (a, w) in enumerate(m["crit"]):
            for v in (w - 1, w + 1, w + 2):
                if 1 <= v <= 5:
                    s2 = copy.deepcopy(sc)
                    s2["mech"]["crit"][ci][1] = v
                    ws = [x[1] for x in s2["mech"]["crit"]]
                    if len(set(ws)) == 1:
                        continue
                    out.append(({"type": "weight", "a": a, "old": w, "new": v}, s2, 2))
    return out


def twin(sc, rng, base_out):
    cands = []
    for desc, s2, mag in edits(sc, rng):
        if s2["target"].get("hypo") and s2["target"]["hypo"]["type"] == "gate":
            g = s2["gates"][s2["target"]["hypo"]["g"]]
            if s2["target"]["hypo"]["t"] == g["t"]:
                continue
        o2 = evaluate(s2)
        if o2 == "REJECT" or o2 == base_out:
            continue
        cands.append((desc, s2, mag, o2))
    if not cands:
        return None
    special = [x for x in cands if x[3] in (NONE, TIE, UNDET)]
    normal = [x for x in cands if x[3] not in (NONE, TIE, UNDET)]
    pool = normal if (normal and (not special or rng.random() < 0.82)) else special
    wts = []
    for desc, s2, mag, o2 in pool:
        w = 1.0 / mag
        if desc["type"] in ("gate", "ctx", "weight"):
            w *= 0.6
        wts.append(w)
    desc, s2, mag, o2 = rng.choices(pool, weights=wts)[0]
    return s2, desc, o2


# ------------------------------------------------------------------------------------------------ rendering helpers
def gn(Aa):
    g = Aa.get("gnp") or Aa["hdr"].lower()
    for art in ("a ", "an "):
        if g.startswith(art):
            return g[len(art):]
    return g


def fmt_v(sc, a, v, i=None, bare=False):
    dom = DOM[sc["dom"]]
    r = sc["r"]
    if a == "received":
        return fmt_dt(v, r["dstyle"], r["tstyle"])
    Aa = dom["A"][a]
    k = Aa["kind"]
    if v is None:
        if k == "bool":
            return ["not confirmed", "awaiting confirmation", "unknown"][r["miss_tok"]]
        return ["not scored", "—", "pending"][r["miss_tok"]]
    alt = i is not None and [i, a] in sc["alt"]
    if k == "money":
        cur, minor = Aa.get("cur") or dom["cur"], Aa["minor"]
        if alt and Aa["alt"] == "year":
            return fmt_money(v * 12, cur, minor) + Aa["per"].replace("month", "year")
        if alt and Aa["alt"] == "month12":
            return fmt_money(v // 12, cur, minor, force_dec=True) + "/month"
        return fmt_money(v, cur, minor) + ("" if bare else Aa["per"])
    if k == "num":
        f = Aa.get("fmt")
        if f == "year":
            return str(v)
        if f == "dur":
            return fmt_dur(v, r["durstyle"])
        if f == "time":
            return fmt_time(v, r["tstyle"])
        if alt and Aa["alt"] == "weeks":
            w = v // 7
            return f"{w} week" + ("" if w == 1 else "s")
        s = fmt_dec(v, Aa["dp"])
        u = Aa["u"]
        if isinstance(u, tuple):
            return f"{s} {u[0] if v == 10 ** Aa['dp'] else u[1]}"
        return s + u
    if k == "score":
        return f"{v}/{sc['scale'][1]}" if r["score_style"] == "slash" else str(v)
    if k == "bool":
        return Aa["yes"] if v else Aa["no"]
    return str(v)


def hdr_of(sc, a):
    if a == "received":
        return "Received"
    Aa = DOM[sc["dom"]]["A"][a]
    if Aa["kind"] == "score" and sc["r"]["score_style"] == "plain":
        return f"{Aa['hdr']} ({sc['scale'][0]}-{sc['scale'][1]})"
    return Aa["hdr"]


def cur_word(dom):
    return {"$": "dollars", "£": "pounds", "€": "euros", "p": "pence"}[dom["cur"]]


def thr_txt(sc, a, t):
    Aa = DOM[sc["dom"]]["A"].get(a, {})
    if gn(Aa).startswith("number of") if Aa else False:
        return fmt_dec(t, Aa.get("dp", 0))
    return fmt_v(sc, a, t, bare=True)


def cmp_phrase(sc, a, op, t, variant):
    txt = thr_txt(sc, a, t)
    Aa = DOM[sc["dom"]]["A"].get(a, {})
    if Aa.get("fmt") == "time" or a == "received":
        return {"le": ["no later than {t}", "by {t} at the latest", "at or before {t}"],
                "lt": ["before {t}", "earlier than {t}", "before {t}"]}[op][variant].format(t=txt)
    if op == "le" and t == 0 and gn(Aa).startswith("number of"):
        return "0"
    return {"ge": ["at least {t}", "{t} or more", "no less than {t}"],
            "gt": ["more than {t}", "over {t}", "greater than {t}"],
            "le": ["at most {t}", "no more than {t}", "{t} or less"],
            "lt": ["less than {t}", "under {t}", "below {t}"]}[op][variant].format(t=txt)


def fail_phrase(sc, a, op, t, variant):
    txt = thr_txt(sc, a, t)
    Aa = DOM[sc["dom"]]["A"].get(a, {})
    if Aa.get("fmt") == "time":
        return {"le": ["later than {t}", "after {t}", "after {t}"], "lt": ["{t} or later", "at or after {t}",
                                                                        "{t} or later"]}[op][variant].format(t=txt)
    return {"ge": ["below {t}", "under {t}", "less than {t}"],
            "gt": ["{t} or less", "at or below {t}", "no more than {t}"],
            "le": ["above {t}", "over {t}", "more than {t}"],
            "lt": ["{t} or more", "at or above {t}", "no less than {t}"]}[op][variant].format(t=txt)


def gate_sentence(sc, gi):
    dom = DOM[sc["dom"]]
    g = sc["gates"][gi]
    gm = sc["gate_meta"][gi]
    ps, pp = dom["party"]
    Pp = pp[0].upper() + pp[1:]
    var = sc["r"]["gate_phr"][gi]
    style = gm["style"]
    tags = []
    a = g["a"]
    if gm.get("deadline"):
        t = sc["ctx"]["_deadline"]
        day, mod = divmod(t, 1440)
        when = f"{fmt_time(mod, sc['r']['tstyle'])} on {fmt_date(day, 0)}"
        tags.append("temporal")
        if style == "pos":
            return f"Only {pp} received by {when} are considered.", tags
        return f"{Pp} received after {when} are rejected.", tags + ["negation"]
    Aa = dom["A"][a]
    if gm.get("zero"):
        tags.append("quantifier")
        if a == "red":
            s = ["Players who received a red card during the season are not eligible.",
                 "Only players with no red cards are eligible.",
                 "No player with a red card can win."][var]
        else:
            s = ["A patch must not add any new lint warnings.", "Patches that add a new lint warning are rejected.",
                 "Only patches with zero new lint warnings can be merged."][var]
        return s, tags + ["negation"]
    if gm.get("ctxt") == "tests":
        tags.append("quantifier")
        s = [f"A patch must pass all {g['t']} tests.", f"Patches that fail any of the {g['t']} tests are rejected.",
             f"No patch is merged unless every one of the {g['t']} tests passes."][var]
        return s, tags + (["negation"] if var else [])
    if g["op"] in ("true", "false", "in"):
        vb = gm.get("vb") or Aa["vb"]
        vb3 = gm.get("vb3") or Aa["vb3"]
        if g["op"] == "false":
            s = {"pos": f"{Pp} must not {vb}.", "neg": f"{Pp} that {vb} are excluded.",
                 "dneg": f"{art(ps, True)} {ps} that does not {vb} is not excluded on this ground; one that does is excluded."}[style]
            tags.append("negation")
            if style == "dneg":
                tags.append("double_negation")
            return s, tags
        exc = g.get("exc")
        if exc:
            fl = dom["A"][exc["a"]]
            tags.append("exception")
            s = [f"{Pp} must {vb}, unless they {fl['vb']}.",
                 f"{Pp} must {vb}; this requirement is waived for {pp} that {fl['vb']}.",
                 f"Only {pp} that {vb} are eligible, except that {pp} that {fl['vb']} are also eligible."][var]
            return s, tags
        if style == "pos":
            return [f"{Pp} must {vb}.", f"Every {ps} must {vb}.", f"Mandatory: {pp} must {vb}."][var], tags
        if style == "neg":
            return [f"{Pp} that do not {vb} are excluded.", f"Any {ps} that does not {vb} is rejected.",
                    f"{art(ps, True)} {ps} that fails to {vb} cannot be chosen."][var], tags + ["negation"]
        return [f"No {ps} that fails to {vb} will be considered.",
                f"It is not acceptable for {art(ps)} {ps} not to {vb}.",
                (f"No {ps} is eligible unless they {vb}." if dom.get("person") else
                 f"No {ps} is eligible unless it {vb3}.")][var], tags + ["negation", "double_negation"]
    # numeric thresholds
    noun = gn(Aa)
    its = "their" if dom.get("person") else "its"
    op, t = g["op"], g["t"]
    ok = cmp_phrase(sc, a, op, t, var)
    bad = fail_phrase(sc, a, op, t, var)
    exc = g.get("exc")
    if gm.get("ctxt") == "refs_ok" or a == "refs_ok":
        tags.append("quantifier")
    if a == "refs_ok":
        k = t if op == "ge" else t + 1
        s = [f"At least {k} of a candidate's 3 references must be satisfactory.",
             f"Candidates with fewer than {k} satisfactory references (out of 3) are not considered.",
             f"No candidate is appointed unless at least {k} of their 3 references are satisfactory."][var]
        return s, tags + (["negation"] if var else [])
    if exc:
        fl = dom["A"][exc["a"]]
        tags.append("exception")
        if exc["mode"] == "relax":
            ok2 = cmp_phrase(sc, a, op, exc["t2"], 0)
            s = [f"Each {ps}'s {noun} must be {ok}, except that {ok2} is accepted from {pp} that {fl['vb']}.",
                 f"The {noun} must be {ok} ({ok2} for {pp} that {fl['vb']}).",
                 f"{Pp} whose {noun} is {bad} are excluded, unless they {fl['vb']}, in which case the limit is "
                 f"{ok2}."][var]
            return s, tags + (["negation"] if var == 2 else [])
        s = f"Each {ps}'s {noun} must be {ok}; this requirement is waived for {pp} that {fl['vb']}."
        return s, tags
    if style == "pos":
        return [f"Each {ps}'s {noun} must be {ok}.", f"The {noun} must be {ok}.",
                f"Requirement: {noun} {ok}."][var], tags
    if style == "neg":
        return [f"{Pp} whose {noun} is {bad} are excluded.", f"Any {ps} whose {noun} is {bad} is ruled out.",
                f"{art(ps, True)} {ps} cannot be chosen if {its} {noun} is {bad}."][var], tags + ["negation"]
    return [f"No {ps} is accepted unless {its} {noun} is {ok}.",
            f"No {ps} whose {noun} is {bad} will be considered.",
            f"{art(ps, True)} {ps} is not eligible unless {its} {noun} is {ok}."][var], tags + ["negation"]


def band_text(sc, a, bands):
    Aa = DOM[sc["dom"]]["A"][a]
    exact = Aa["kind"] == "num" and Aa.get("dp", 0) == 0 and Aa.get("step", 1) == 1
    parts = []
    for lo, hi, p in bands:
        pt = f"{p} point" + ("" if p == 1 else "s")
        if exact:
            f = lambda x: fmt_v(sc, a, x, bare=True)
            u = Aa.get("u")
            if isinstance(u, tuple):
                g = lambda x: fmt_int(x)
                if lo is None:
                    rng_t = f"{f(hi)} or fewer"
                elif hi is None:
                    rng_t = f"{f(lo)} or more"
                elif lo == hi:
                    rng_t = f"exactly {f(lo)}"
                else:
                    rng_t = f"{g(lo)} to {g(hi)} {u[1]}"
            elif lo is None:
                rng_t = f"{f(hi)} or less"
            elif hi is None:
                rng_t = f"{f(lo)} or more"
            elif lo == hi:
                rng_t = f"exactly {f(lo)}"
            else:
                rng_t = f"{f(lo)} to {f(hi)}"
        else:
            f = lambda x: fmt_v(sc, a, x, bare=True)
            if lo is None:
                rng_t = f"under {f(hi + 1)}"
            elif hi is None:
                rng_t = f"{f(lo)} or more"
            else:
                rng_t = f"{f(lo)} up to but not including {f(hi + 1)}"
        parts.append(f"{rng_t} = {pt}")
    return f"{Aa['hdr']}: " + "; ".join(parts)


def mech_sentences(sc):
    dom = DOM[sc["dom"]]
    A = dom["A"]
    ps, pp = dom["party"]
    m = sc["mech"]
    t = m["type"]
    ms = sc["r"]["mstyle"]
    tags = []
    lo, hi = sc["scale"]
    if t == "weighted":
        crit = [(A[a]["hdr"], w) for a, w in m["crit"]]
        tags.append("numeric")
        if m["style"] == "pct":
            lst = ", ".join(f"{h} {w}%" for h, w in crit[:-1]) + f" and {crit[-1][0]} {crit[-1][1]}%"
            s = [f"Each {ps} is scored from {lo} to {hi} on each criterion, and the weighted total decides: {lst}. "
                 f"The highest weighted total ranks first.",
                 f"Weighting: {lst}. Criterion scores run from {lo} to {hi}; the {ps} with the highest weighted score "
                 f"wins.",
                 f"Scores ({lo} = weakest, {hi} = strongest) are combined using these weights: {lst}. Highest weighted "
                 f"score wins."][ms]
        elif m["style"] == "mult":
            lst = ", ".join(f"{h} x{w}" for h, w in crit)
            s = [f"Each criterion score ({lo}-{hi}) is multiplied by its weight and the results are added: {lst}. "
                 f"The highest total ranks first.",
                 f"Total = sum of (score x weight), with weights {lst}; scores run from {lo} to {hi}. Highest total "
                 f"wins.",
                 f"Multiply each score ({lo} to {hi}) by the weight shown ({lst}) and add them up; the largest total "
                 f"wins."][ms]
        else:
            lst = ", ".join(f"{h} {w} points" for h, w in crit[:-1]) + f" and {crit[-1][0]} {crit[-1][1]} points"
            s = [f"The criteria are worth {lst}. Each {ps} earns a criterion's points in proportion to its score out of "
                 f"{hi} (score / {hi} x points available). The most points wins.",
                 f"Points available: {lst}; points earned = score out of {hi} / {hi} x points available. The highest "
                 f"points total wins.",
                 f"{art(ps, True)} {ps} scoring s out of {hi} on a criterion earns s/{hi} of that criterion's points ({lst}). "
                 f"Most points wins."][ms]
        return [s], tags
    if t == "cost":
        tags += ["numeric"]
        if len(m["comp"]) > 1:
            tags.append("multi_hop")
        if any(c[0] in ("cond", "tier") for c in m["comp"]):
            tags.append("exception")
        noun, defn = cost_text(sc)
        if noun:
            s = [f"The eligible {ps} with the lowest {noun} is chosen, where {noun} = {defn}.",
                 f"Among eligible {pp}, choose the one with the lowest {noun} ({noun} = {defn}).",
                 f"Lowest {noun} wins: {noun} = {defn}."][ms]
        else:
            s = [f"The eligible {ps} with the lowest cost is chosen, comparing {defn}.",
                 f"Among eligible {pp}, choose the cheapest, comparing {defn}.",
                 f"Lowest price wins, where price means {defn}."][ms]
        return [s], tags
    if t == "banded":
        tags.append("numeric")
        lines = [band_text(sc, a, b) for a, b in m["bands"]]
        head = [f"Points are awarded per criterion as follows, and the {ps} with the most points in total wins:",
                "Scoring bands (add up the points; highest total wins):",
                f"Each {ps} collects points from these bands; the highest total is chosen:"][ms]
        return [head + " " + " | ".join(lines) + "."] if sc["r"]["rules"] == "prose" else [head] + lines, tags
    if t == "ratio":
        tags += ["numeric", "multi_hop"]
        noun, defn = cost_text(sc)
        ct = f"{noun} ({defn})" if noun else defn
        qh = A[m["qual"]]["hdr"].lower()
        s = [f"Best value: price is worth {m['wp']} points and {qh} {m['wq']} points. Price is measured as {ct}. The "
             f"lowest eligible price earns all {m['wp']} price points; any other eligible {ps} earns {m['wp']} x "
             f"(lowest price / its price). {A[m['qual']]['hdr']} points = {m['wq']} x ({qh} score / {m['qmax']}). "
             f"Points are not rounded; the highest combined total wins.",
             f"Combined score = {m['wp']} x (lowest eligible price / this {ps}'s price) + {m['wq']} x ({qh} score / "
             f"{m['qmax']}), where price means {ct}. No rounding. Highest combined score wins.",
             f"Price counts for {m['wp']} points (the cheapest eligible {ps} gets all {m['wp']}; others get "
             f"{m['wp']} x cheapest price / their price, price being {ct}) and {qh} for {m['wq']} points ({m['wq']} "
             f"x score / {m['qmax']}). Unrounded totals are compared; the highest wins."][ms]
        return [s], tags
    if t == "lexi":
        parts = []
        for a, d in m["keys"]:
            Aa = A[a]
            if Aa.get("fmt") == "time":
                dd = "earliest first" if d == "low" else "latest first"
            else:
                dd = ["higher is better", "highest first", "more is better"][ms] if d == "high" else \
                    ["lower is better", "lowest first", "less is better"][ms]
            parts.append(f"{Aa['hdr'].lower()} ({dd})")
        s = f"Rank the {pp} by {parts[0]}"
        for k, p in enumerate(parts[1:]):
            s += f"; if tied, by {p}" if k == 0 else f"; if still tied, by {p}"
        s += ". The top-ranked eligible " + ps + " is chosen." if sc["target"]["kind"] == "best" else "."
        return [s], tags
    if t == "panel":
        tags.append("numeric")
        J = m["judges"]
        plo, phi = m["pscale"]
        agg = {"mean": "the average (mean) of the judges' scores",
               "sum": "the total of the judges' scores",
               "median": "the median of the judges' scores" + (
                   " (with an even number of judges, the average of the two middle scores)" if J % 2 == 0 else ""),
               "trim": "the average of the judges' scores after removing the single highest and the single lowest "
                       "score"}[m["agg"]]
        s = [f"{J} judges each scored every {ps} from {plo} to {phi}. {art(ps, True)} {ps}'s final score is {agg}; the highest final "
             f"score wins.",
             f"Final score = {agg}. Scores run from {plo} to {phi}. Highest final score ranks first.",
             f"The panel ({J} judges, scores {plo}-{phi}) ranks {pp} by {agg}, highest first."][ms]
        return [s], tags
    if t == "linear":
        tags.append("numeric")
        parts = []
        lin_u = {a: u for a, _, u in dom["linear"]}
        for k, (a, c) in enumerate(m["terms"]):
            u = lin_u[a]
            if c == 1 and k == 0:
                parts.append(f"1 point per {u}")
            elif c > 0:
                parts.append(("+ " if k else "") + f"{c} points per {u}")
            else:
                parts.append(f"- {-c} point{'s' if c != -1 else ''} per {u}")
        form = " ".join(parts)
        s = [f"Award points = {form}. The eligible {ps} with the most award points wins.",
             f"Each nominee earns {form}; the highest total wins.",
             f"Points formula: {form}. Highest points total wins."][ms]
        return [s], tags
    if t == "first":
        tags.append("temporal")
        s = [f"{pp[0].upper() + pp[1:]} are considered in the order they were received (see the timestamps), and "
             f"the first one that meets every requirement is chosen.",
             f"Work through the {pp} from earliest received to latest; choose the first that meets all the "
             f"requirements.",
             f"First come, first served: the earliest-received {ps} that meets every requirement is chosen."][ms]
        return [s], tags
    raise ValueError(t)


def cost_text(sc):
    """(noun, definition) when the domain text is a formula 'noun = definition', else (None, phrase)."""
    dom = DOM[sc["dom"]]
    t = dom["cost"]["text"][sc["r"]["mstyle"] % len(dom["cost"]["text"])]
    fmt = {k: (fmt_int(v) if isinstance(v, int) else v) for k, v in sc["ctx"].items()}
    t = t.format(**fmt)
    if " = " in t:
        noun, defn = t.split(" = ", 1)
        return noun, defn
    return None, t


def tb_sentence(sc):
    phr = list(sc["r"].get("tb_phr") or [])
    for k, (a, _) in enumerate(sc["tb"]):
        if a == "@cost" and k < len(phr):
            noun, defn = cost_text(sc)
            phr[k] = f"the lower {noun} ({noun} = {defn})" if noun else f"the lower total cost ({defn})"
    ps = DOM[sc["dom"]]["party"][1]
    lots = sc["tb_final"] == "lots"
    ts = sc["r"]["tb_style"]
    if not phr:
        if sc["mech"]["type"] in ("first",):
            return None
        return [f"If {ps} are still level, the decision is made by drawing lots.",
                "Any remaining tie is settled by drawing lots.",
                "Remaining ties go to a draw."][ts] if lots else None
    if len(phr) == 1:
        s = [f"Ties are broken by {phr[0]}.", f"If two {DOM[sc['dom']]['party'][1]} are level, {phr[0]} wins.",
             f"Tie-break: {phr[0]}."][ts]
    else:
        s = [f"Ties are broken by {phr[0]}, then by {', then by '.join(phr[1:])}.",
             f"If two are level, {phr[0]} wins; if still level, {' and then '.join(phr[1:])}.",
             f"Tie-breaks, in order: {'; '.join(phr)}."][ts]
    if lots:
        s += [" If still tied, the decision is made by drawing lots.", " Any remaining tie goes to a draw.",
              " A tie that survives these is settled by lot."][ts]
    return s


def missing_sentence(sc):
    out = []
    if sc["missing"].get("score") == "zero":
        out.append(["A criterion with no score counts as 0.", "Unscored criteria score zero.",
                    "Any criterion left unscored is treated as a score of 0."][sc["r"]["tb_style"]])
    if sc["missing"].get("bool") == "fail":
        out.append(["Anything not confirmed counts as not met.", "An unconfirmed requirement counts as failed.",
                    "If a requirement has not been confirmed, treat it as not met."][sc["r"]["tb_style"]])
    return out


# ------------------------------------------------------------------------------------------------ candidate block
def cand_head(sc, i, style):
    c = sc["cands"][i]
    return [f"{c['label']} ({c['name']})", f"{c['label']}: {c['name']}", f"{c['label']} — {c['name']}"][style]


def prose_frag(sc, i, a):
    dom = DOM[sc["dom"]]
    v = cval_display(sc, i, a)
    if a == "received":
        return f"was received on {fmt_v(sc, a, v)}"
    Aa = dom["A"][a]
    if v is None:
        if Aa["kind"] == "bool":
            return f"has not confirmed whether it {Aa['vb3']}"
        return f"has not yet been scored for {Aa['hdr'].lower()}"
    if Aa["kind"] == "bool":
        return Aa["pt"] if v else Aa["pf"]
    s = fmt_v(sc, a, v, i)
    if Aa["kind"] == "score":
        return f"scored {s} for {Aa['hdr'].lower()}"
    return Aa["prose"].format(v=s)


def cval_display(sc, i, a):
    return sc["cands"][i]["v"].get(a)


def cand_block(sc):
    r = sc["r"]
    lay = r["layout"]
    cols = list(sc["show"])
    panel = sc["mech"]["type"] == "panel"
    J = sc["mech"].get("judges", 0)
    hdrs = [hdr_of(sc, a) for a in cols] + [f"Judge {j + 1}" for j in range(J)] if panel else \
        [hdr_of(sc, a) for a in cols]
    namecol = NAMECOL[sc["dom"]]
    idcol = sc["word"] if sc["word"] != namecol else "Ref"
    rows = []
    for i, c in enumerate(sc["cands"]):
        cells = [fmt_v(sc, a, c["v"].get(a), i) for a in cols]
        if panel:
            cells += [str(x) for x in c["v"]["panel"]]
        rows.append(cells)
    labs = [c["label"] for c in sc["cands"]]
    names = [c["name"] for c in sc["cands"]]
    if lay == "md":
        H = [idcol, namecol] + hdrs
        out = ["| " + " | ".join(H) + " |", "|" + "|".join("---" for _ in H) + "|"]
        for L, nm, cells in zip(labs, names, rows):
            out.append("| " + " | ".join([L, nm] + cells) + " |")
        return "\n".join(out)
    if lay == "pipe":
        H = [idcol, namecol] + hdrs
        out = [" | ".join(H)]
        for L, nm, cells in zip(labs, names, rows):
            out.append(" | ".join([L, nm] + cells))
        return "\n".join(out)
    if lay in ("csv", "tsv"):
        sep = "," if lay == "csv" else "\t"
        q = (lambda x: f'"{x}"' if ("," in x and sep == ",") else x)
        H = [idcol, namecol] + hdrs
        out = [sep.join(q(h) for h in H)]
        for L, nm, cells in zip(labs, names, rows):
            out.append(sep.join(q(x) for x in [L, nm] + cells))
        return "\n".join(out)
    if lay == "fixed":
        H = [idcol, namecol] + hdrs
        data = [[L, nm] + cells for L, nm, cells in zip(labs, names, rows)]
        wid = [max(len(H[k]), *(len(d[k]) for d in data)) for k in range(len(H))]
        out = ["  ".join(h.ljust(w) for h, w in zip(H, wid)).rstrip()]
        out.append("  ".join("-" * w for w in wid))
        for d in data:
            out.append("  ".join(x.ljust(w) for x, w in zip(d, wid)).rstrip())
        return "\n".join(out)
    if lay == "transposed":
        H = [""] + labs
        out = ["| " + " | ".join(H) + " |", "|" + "|".join("---" for _ in H) + "|"]
        out.append("| " + " | ".join([namecol] + names) + " |")
        for k, h in enumerate(hdrs):
            out.append("| " + " | ".join([h] + [rows[i][k] for i in range(len(labs))]) + " |")
        return "\n".join(out)
    if lay == "records":
        out = []
        for i, (cells) in enumerate(rows):
            out.append(cand_head(sc, i, r["name_style"]))
            for h, x in zip(hdrs, cells):
                out.append(f"  {h}: {x}")
            out.append("")
        return "\n".join(out).rstrip()
    if lay in ("bullets", "numbered", "kv"):
        out = []
        for i, cells in enumerate(rows):
            if lay == "kv":
                out.append(" | ".join([labs[i], f"{namecol}={names[i]}"] +
                                      [f"{h}={x}" for h, x in zip(hdrs, cells)]))
            else:
                body = "; ".join(f"{h}: {x}" for h, x in zip(hdrs, cells))
                pre = "- " if lay == "bullets" else f"{i + 1}) "
                hd = cand_head(sc, i, r['name_style'])
                out.append(f"{pre}{hd}{'' if hd.endswith('.') else '.'} {body}")
        return "\n".join(out)
    if lay == "prose":
        out = []
        for i, c in enumerate(sc["cands"]):
            frs = [prose_frag(sc, i, a) for a in cols]
            if panel:
                frs.append("received judges' scores of " + ", ".join(str(x) for x in c["v"]["panel"]) +
                           " (judges 1 to " + str(J) + " in order)")
            if len(frs) == 1:
                body = frs[0]
            else:
                body = ", ".join(frs[:-1]) + " and " + frs[-1]
            out.append(f"{cand_head(sc, i, 0)} {body}.")
        return "\n".join(out)
    raise ValueError(lay)


def correction_lines(sc):
    out = []
    dom = DOM[sc["dom"]]
    for i, a, nv in sc["corr"]:
        c = sc["cands"][i]
        old = fmt_v(sc, a, c["v"][a], i)
        new = fmt_v(sc, a, nv, i)
        d = fmt_date(sc["r"]["date"] + sc["r"].get("corr_date", 1), 0)
        hdr = dom["A"][a]["hdr"] if a in dom["A"] else a
        out.append([f"Correction ({d}): {c['label']}'s {hdr.lower()} was entered wrongly above as {old}; the correct "
                    f"figure is {new}.",
                    f"Update {d}: {c['name']} has corrected its {hdr.lower()} to {new} (the {old} shown above is out "
                    f"of date).",
                    f"Erratum: for {c['label']}, read {hdr.lower()} {new}, not {old}."][sc["r"]["tb_style"]])
    return out


def rules_block(sc):
    sents, tags = [], []
    for gi in range(len(sc["gates"])):
        s, tg = gate_sentence(sc, gi)
        sents.append(s)
        tags += tg
    ms, tg = mech_sentences(sc)
    tags += tg
    tb = tb_sentence(sc)
    ex = missing_sentence(sc)
    style = sc["r"]["rules"]
    heads = ["Evaluation rules:", "Selection rules", "How the decision is made:", "Award criteria (as published):",
             "Rules agreed in advance:", "Decision rules:"]
    head = heads[sc["r"]["hdr"]]
    body = sents + ms + ([tb] if tb else []) + ex
    if style == "bullets":
        return "\n".join([head] + ["- " + x for x in body]), tags
    if style == "numbered":
        return "\n".join([head] + [f"{k + 1}. {x}" for k, x in enumerate(body)]), tags
    if style == "prose":
        return (head.rstrip(":") + ": " if not head.endswith(":") else head + " ") + " ".join(body), tags
    steps = []
    if sents:
        steps.append("Step 1 (eligibility): " + " ".join(sents))
    steps.append(f"Step {len(steps) + 1} (ranking): " + " ".join(ms + ex))
    if tb:
        steps.append(f"Step {len(steps) + 1} (ties): " + tb)
    return "\n".join([head] + steps), tags


def intro_text(sc):
    dom = DOM[sc["dom"]]
    r = sc["r"]
    fmt = {}
    for k, v in sc["ctx"].items():
        fmt[k] = fmt_int(v) if isinstance(v, int) else v
    if "cap" in sc["ctx"]:
        fmt["cap_txt"] = fmt_money(sc["ctx"]["cap"], dom["cur"])
    if "cover" in sc["ctx"]:
        fmt["cover_txt"] = fmt_money(sc["ctx"]["cover"], dom["cur"])
    fmt.update(org=dom["orgs"][r["intro"] % len(dom["orgs"])], n=len(sc["cands"]), date=fmt_date(r["date"], 0),
               num=r["num"], nounp=dom["party"][1])
    title = dom["titles"][r["title"] % len(dom["titles"])].format(**fmt)
    intro = dom["intro"][r["intro"] % len(dom["intro"])].format(**fmt)
    intro = intro[0].upper() + intro[1:]
    intro = re.sub(r"(\w)s's\b", r"\1s'", intro)
    return title, intro, fmt["org"]


def render(sc):
    dom = DOM[sc["dom"]]
    r = sc["r"]
    title, intro, org = intro_text(sc)
    rules, tags = rules_block(sc)
    cands = cand_block(sc)
    corr = correction_lines(sc)
    parts = [intro]
    if r["rules_first"]:
        parts += [rules, cands]
    else:
        parts += [cands, rules]
    if corr:
        parts.append("\n".join(corr))
    body = "\n\n".join(parts)
    if r["wrap"] == "email":
        state = f"From: {r['person']}\nSubject: {title}\n\nHi all,\n\n{body}\n\nThanks,\n{r['person'].split()[0]}"
    elif r["wrap"] == "memo":
        state = f"MEMO\nRe: {title}\nFrom: {r['person']}\n\n{body}"
    elif r["wrap"] == "ticket":
        state = f"Ticket #{r['num'] * 7 % 90000 + 10000}: {title}\n\n{body}"
    else:
        state = f"{title}\n\n{body}"
    state = fix_articles(state)
    ins = fix_articles(question(sc, org))
    opts = [c["label"] for c in sc["cands"]] + special_opts(sc["word"], sc["target"]["kind"])
    edges = list(tags)
    if r["layout"] in TABLE_LAYOUTS:
        edges.append("table")
    if any(cval(sc, i, a) is None for i in range(len(sc["cands"])) for a in used_attrs(sc) if a != "panel"):
        edges.append("missing_info")
    if sc["corr"]:
        edges.append("conflicting_evidence")
    if sc["alt"]:
        edges.append("units")
    if sc["target"].get("hypo"):
        edges.append("hypothetical")
    if any(a == "@cost" for a, _ in sc["tb"]) or any(a == "received" for a, _ in sc["tb"]):
        edges.append("multi_hop" if any(a == "@cost" for a, _ in sc["tb"]) else "temporal")
    if any(dom["A"].get(a, {}).get("fmt") in ("time", "dur") for a in used_attrs(sc)):
        edges.append("temporal")
    if len(sc["cands"]) >= 7 or len(state) > 2600:
        edges.append("long_context")
    if sc["mech"]["type"] in ("cost", "ratio") or any(g["op"] in ("ge", "gt", "le", "lt") for g in sc["gates"]):
        edges.append("numeric")
    return state, ins, opts, list(dict.fromkeys(edges))


QT = {
    "best": ["Under the evaluation rules in the text, which {lw} {goal}?",
             "Applying the mandatory requirements, the scoring method and the tie-break rules exactly as written, "
             "which {lw} {goal}?",
             "Which {lw} {goal} according to the stated selection rules?",
             "Going strictly by the rules and figures given, which {lw} should be chosen?",
             "Which {lw} is selected once the stated requirements, method and tie-breaks are applied?",
             "Based only on the information and rules given, which {lw} comes out on top?",
             "Which {lw} ranks first under the stated rules?",
             "Following the decision rules set out in the text, which {lw} {goal}?",
             "If the stated rules are followed exactly, which {lw} is picked?",
             "Which {lw} wins under the stated criteria, weights and requirements?",
             "According to the rules above, which {lw} {goal}?",
             "Which {lw} does the stated method select?"],
    "second": ["Which {lw} ranks second under the stated rules (the reserve choice if the winner drops out)?",
               "Under the stated method, which {lw} would be the runner-up?",
               "Which {lw} finishes in second place once the rules and tie-breaks are applied?",
               "Applying the requirements, method and tie-breaks as written, which {lw} is ranked second?",
               "Which {lw} would be the reserve (second-ranked) choice under these rules?",
               "Which {lw} comes second in the ranking produced by the stated rules?"],
    "last": ["Among the {lw_p} that meet every mandatory requirement, which one ranks last under the stated method?",
             "Which eligible {lw} comes bottom of the ranking under the stated rules?",
             "Under the stated rules and tie-breaks, which of the eligible {lw_p} ranks lowest?",
             "Ignoring any {lw} that fails a requirement, which one is ranked last by the stated method?",
             "Which qualifying {lw} would be ranked last if the stated rules were applied in full?"],
    "withdraw": ["If {L} withdrew before the decision, which {lw} {goal2} under the same rules?",
                 "Suppose {L} drops out. Applying the same rules, which {lw} {goal2}?",
                 "Which {lw} {goal2} if {L} were withdrawn and everything else stayed the same?"],
    "drop": ["If the {crit} criterion were removed and the other weights stayed the same, which {lw} {goal2}?",
             "Suppose {crit} is no longer scored (the remaining weights are unchanged). Which {lw} {goal2}?"],
    "gate": ["If the requirement on {noun} were changed to {cmp}, which {lw} {goal2} under otherwise unchanged rules?",
             "Suppose the {noun} requirement became {cmp}. Which {lw} {goal2}?"],
    "nogate": ["If the requirement that {pp} {vb} were dropped, which {lw} {goal2} under the remaining rules?",
               "Suppose {pp} no longer had to {vb}. Which {lw} {goal2}?"],
    "ctx": ["If {change}, which {lw} {goal2} under the same rules?",
            "Suppose {change} (everything else unchanged). Which {lw} {goal2}?"],
}


def question(sc, org):
    dom = DOM[sc["dom"]]
    lw = lw_of(sc["word"])
    goal, goal2 = dom["goal"]
    q = sc["r"]["q"]
    fmt = dict(lw=lw, lw_p=plural(lw), goal=goal, goal2=goal2, org=org, pp=dom["party"][1])
    h = sc["target"].get("hypo")
    if not h:
        tl = QT[sc["target"]["kind"]]
        return tl[q % len(tl)].format(**fmt)
    t = h["type"]
    if t == "withdraw":
        fmt["L"] = sc["cands"][h["i"]]["label"]
    elif t == "drop":
        fmt["crit"] = dom["A"][h["a"]]["hdr"].lower()
    elif t == "gate":
        g = sc["gates"][h["g"]]
        fmt["noun"] = gn(dom["A"][g["a"]])
        fmt["cmp"] = cmp_phrase(sc, g["a"], g["op"], h["t"], 0)
    elif t == "nogate":
        g = sc["gates"][h["g"]]
        gm = sc["gate_meta"][h["g"]]
        vb = gm.get("vb") or dom["A"][g["a"]]["vb"]
        if g["op"] == "false":
            vb = "not " + vb
        fmt["vb"] = vb
    elif t == "ctx":
        fmt["change"] = CTX_HYPO[h["k"]].format(v=fmt_int(h["v"]) if isinstance(h["v"], int) else h["v"])
    tl = QT[t]
    return tl[q % len(tl)].format(**fmt)


# ------------------------------------------------------------------------------------------------ naive answers (hardness)
def naive_outcomes(sc):
    outs = []
    s = copy.deepcopy(sc)
    h = sc["target"].get("hypo")
    if s["gates"] and not (h and h["type"] in ("gate", "nogate")):
        s["gates"] = []
        outs.append(evaluate(s))
    if sc["corr"]:
        s = copy.deepcopy(sc)
        s["corr"] = []
        outs.append(evaluate(s))
    if sc["mech"]["type"] == "weighted":
        s = copy.deepcopy(sc)
        for x in s["mech"]["crit"]:
            x[1] = 1
        outs.append(evaluate(s))
    if sc["tb"]:
        s = copy.deepcopy(sc)
        s["tb"] = []
        s["tb_final"] = "lots"
        outs.append(evaluate(s))
    if sc["mech"]["type"] == "cost" and len(sc["mech"]["comp"]) > 1:
        s = copy.deepcopy(sc)
        c0 = s["mech"]["comp"][0]
        s["mech"]["comp"] = [["add", c0[1]]] if c0[0] in ("mul", "add") else [["add", c0[1]]]
        outs.append(evaluate(s))
    if sc["target"].get("hypo"):
        s = copy.deepcopy(sc)
        s["target"]["hypo"] = None
        outs.append(evaluate(s))
    return [o for o in outs if o != "REJECT"]


def build(rng, want=None):
    """Sample a scenario with a valid outcome; returns (spec, outcome) or None."""
    kind = None
    sc = sample(rng, kind=kind)
    if not finalize_hypo(sc, rng):
        return None
    if rng.random() < 0.22:
        force_tie(sc, rng)
    if rng.random() < 0.18:
        add_missing(sc, rng)
    if rng.random() < 0.10:
        add_correction(sc, rng)
    out = evaluate(sc)
    if out == "REJECT":
        return None
    if out == NONE and rng.random() < 0.55:
        return None
    if out not in (NONE, TIE, UNDET):
        trap = [o for o in naive_outcomes(sc) if o != out]
        if not trap and rng.random() < 0.45:
            return None
    return sc, out
