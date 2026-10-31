"""rk_verify: independent re-derivation of every gen_ranking label.

multi   re-evaluates the selection spec with a separate implementation (pairwise 'strictly better' counting instead of
        sorting, its own cost / band / panel / hypothetical / missing-value code) and checks that every value the
        rules read is printed in the rendered text (cells, thresholds, corrections, context numbers).
resp    re-reads the RENDERED text: splits the replies out of the state, detects which key-point wording (correct
        value, equivalent wording, wrong value, true / false wording) each reply contains, reads the essential marks
        and send times from the text, and re-grades.
math    recomputes both requested values with Decimal arithmetic from the problem parameters (and checks the
        parameters are printed), then extracts the values each answer states from the rendered answer lines.
vote    parses the options, the counting rule and the ballot lines from the rendered text and recounts.
Each function returns the gold option string it derives.
"""
import copy
import itertools
import math
import re
from decimal import ROUND_CEILING, Decimal as Dm
from fractions import Fraction as Fr

import rk_math
import rk_multi
import rk_resp
import rk_vote
from rk_core import fix_articles
from rk_domains import DOM
from rk_topics import TOPIC


# ------------------------------------------------------------------------------------------------ multi
def _value(sc, i, a):
    v = sc["cands"][i]["v"].get(a)
    for ci, ca, nv in sc.get("corr", []):
        if ci == i and ca == a:
            v = nv
    return v


def _attrs_read(sc, gates, mech, tb):
    out = set()
    for g in gates:
        out.add(g["a"])
        if g.get("exc"):
            out.add(g["exc"]["a"])
    t = mech["type"]
    comps = []
    if t == "weighted":
        out |= {a for a, _ in mech["crit"]}
    elif t == "cost":
        comps = mech["comp"]
    elif t == "ratio":
        comps = mech["comp"]
        out.add(mech["qual"])
    elif t == "banded":
        out |= {a for a, _ in mech["bands"]}
    elif t == "lexi":
        out |= {a for a, _ in mech["keys"]}
    elif t == "linear":
        out |= {a for a, _ in mech["terms"]}
    elif t == "first":
        out.add("received")
    for a, _ in tb:
        if a == "@cost":
            comps = comps + sc["cost_comp"]
        else:
            out.add(a)
    for c in comps:
        if c[0] in ("mul", "add"):
            out.add(c[1])
            if c[0] == "mul":
                out |= {k[1:] for k in c[2] if k.startswith("@")}
        elif c[0] == "cond":
            out |= {c[1], c[2]}
        elif c[0] == "tier":
            out |= {c[1], c[2], c[3]}
    return out


def _cost(comps, val, ctx):
    total = Fr(0)
    for c in comps:
        kind = c[0]
        if kind == "add":
            total += Fr(val(c[1]))
        elif kind == "mul":
            f = Fr(val(c[1]))
            for k in c[2]:
                f = f * (Fr(val(k[1:])) if k[0] == "@" else Fr(ctx[k]))
            total += f
        elif kind == "cond":
            if val(c[2]) == c[3]:
                f = Fr(val(c[1]))
                for k in c[4]:
                    f = f * Fr(ctx[k])
                total += f
        elif kind == "tier":
            q = Fr(ctx[c[4]])
            price = val(c[2]) if q >= val(c[3]) else val(c[1])
            total += q * price
    return total


def _passes(g, val):
    a, op, t = g["a"], g["op"], g["t"]
    ex = g.get("exc")
    if ex and val(ex["a"]) is True:
        if ex["mode"] == "waive":
            return True
        t = ex["t2"]
    v = val(a)
    return {"true": lambda: v is True, "false": lambda: v is False, "in": lambda: v in t,
            "ge": lambda: v >= t, "gt": lambda: v > t, "le": lambda: v <= t, "lt": lambda: v < t}[op]()


def _key(sc, mech, tb, ctx, i, val, cheapest):
    t = mech["type"]
    ks = []
    if t == "weighted":
        ks.append(Fr(sum(w * val(a) for a, w in mech["crit"]), mech["div"]))
    elif t == "cost":
        ks.append(-_cost(mech["comp"], val, ctx))
    elif t == "banded":
        tot = 0
        for a, bands in mech["bands"]:
            v = val(a)
            hit = [p for lo, hi, p in bands if (lo is None or lo <= v) and (hi is None or v <= hi)]
            assert len(hit) == 1, (a, v, bands)
            tot += hit[0]
        ks.append(Fr(tot))
    elif t == "ratio":
        price = _cost(mech["comp"], val, ctx)
        ks.append(mech["wp"] * cheapest / price + Fr(mech["wq"] * val(mech["qual"]), mech["qmax"]))
    elif t == "lexi":
        for a, d in mech["keys"]:
            ks.append(Fr(val(a)) * (1 if d == "high" else -1))
    elif t == "panel":
        xs = sorted(sc["cands"][i]["v"]["panel"])
        n = len(xs)
        if mech["agg"] == "sum":
            ks.append(Fr(sum(xs)))
        elif mech["agg"] == "mean":
            ks.append(Fr(sum(xs), n))
        elif mech["agg"] == "trim":
            ks.append(Fr(sum(xs) - xs[0] - xs[-1], n - 2))
        else:
            ks.append(Fr(xs[n // 2]) if n % 2 else Fr(xs[n // 2 - 1] + xs[n // 2], 2))
    elif t == "linear":
        ks.append(Fr(sum(c * val(a) for a, c in mech["terms"])))
    elif t == "first":
        ks.append(-Fr(val("received")))
    for a, d in tb:
        x = _cost(sc["cost_comp"], val, ctx) if a == "@cost" else Fr(val(a))
        ks.append(x if d == "high" else -x)
    return tuple(ks)


def verify_multi(sc):
    gates = copy.deepcopy(sc["gates"])
    mech = copy.deepcopy(sc["mech"])
    ctx = dict(sc["ctx"])
    tb = [list(x) for x in sc["tb"]]
    gone = None
    h = sc["target"].get("hypo")
    if h:
        if h["type"] == "withdraw":
            gone = h["i"]
        elif h["type"] == "drop":
            mech["crit"] = [x for x in mech["crit"] if x[0] != h["a"]]
            tb = [x for x in tb if x[0] != h["a"]]
        elif h["type"] == "gate":
            gates[h["g"]]["t"] = h["t"]
        elif h["type"] == "nogate":
            gates.pop(h["g"])
        elif h["type"] == "ctx":
            ctx[h["k"]] = h["v"]
    read = _attrs_read(sc, gates, mech, tb) - {"panel"}
    n = len(sc["cands"])
    live = [i for i in range(n) if i != gone]
    open_cells = []
    for i in live:
        for a in sorted(read):
            if _value(sc, i, a) is not None:
                continue
            kind = sc["kinds"][a]
            if kind == "bool" and sc["missing"].get("bool") == "fail":
                continue
            if kind == "num" and a in sc["scores"] and sc["missing"].get("score") == "zero":
                continue
            open_cells.append((i, a))
    choices = [sc["enum"][a] for _, a in open_cells]
    results = set()
    kind_t = sc["target"]["kind"]
    for combo in itertools.product(*choices) if open_cells else [()]:
        fill = dict(zip(open_cells, combo))

        def mk(i):
            def val(a):
                v = _value(sc, i, a)
                if v is None:
                    if (i, a) in fill:
                        return fill[(i, a)]
                    if sc["kinds"][a] == "bool":
                        return False
                    return 0
                return v
            return val

        vals = {i: mk(i) for i in live}
        elig = [i for i in live if all(_passes(g, vals[i]) for g in gates)]
        if not elig:
            results.add("NONE" if kind_t == "best" else "REJECT")
            continue
        cheapest = min(_cost(mech["comp"], vals[i], ctx) for i in elig) if mech["type"] == "ratio" else None
        K = {i: _key(sc, mech, tb, ctx, i, vals[i], cheapest) for i in elig}
        better = {i: sum(1 for j in elig if K[j] > K[i]) for i in elig}
        worse = {i: sum(1 for j in elig if K[j] < K[i]) for i in elig}
        equal = {i: sum(1 for j in elig if K[j] == K[i]) for i in elig}
        if kind_t == "best":
            top = [i for i in elig if better[i] == 0]
        elif kind_t == "last":
            if len(elig) < 2:
                results.add("REJECT")
                continue
            top = [i for i in elig if worse[i] == 0]
        else:
            if len(elig) < 2:
                results.add("REJECT")
                continue
            top = [i for i in elig if better[i] <= 1 < better[i] + equal[i]]
        results.add(sc["cands"][top[0]]["label"] if len(top) == 1 else "TIE")
    assert "REJECT" not in results
    out = next(iter(results)) if len(results) == 1 else "UNDET"
    return rk_multi.gold_option(sc, out)


def check_multi_text(sc, state, ins):
    """Every value the rules read is printed where the reader can see it."""
    probs = []
    for c in sc["cands"]:
        if c["label"] not in state or c["name"] not in state:
            probs.append(("label/name", c["label"]))
    for i, c in enumerate(sc["cands"]):
        for a in sc["show"]:
            if sc["r"]["layout"] == "prose":
                s = fix_articles(rk_multi.prose_frag(sc, i, a))
            else:
                s = rk_multi.fmt_v(sc, a, c["v"].get(a), i)
            if s not in state:
                probs.append(("cell", c["label"], a, s))
        if sc["mech"]["type"] == "panel":
            if sc["r"]["layout"] == "prose":
                if ", ".join(str(x) for x in c["v"]["panel"]) not in state:
                    probs.append(("panel", c["label"]))
    for gi, g in enumerate(sc["gates"]):
        if g["op"] in ("ge", "gt", "le", "lt") and g["a"] not in ("received", "refs_ok", "passed") and \
                not sc["gate_meta"][gi].get("zero"):
            s = rk_multi.thr_txt(sc, g["a"], g["t"])
            if s not in state:
                probs.append(("threshold", g["a"], s))
    for i, a, nv in sc["corr"]:
        s = rk_multi.fmt_v(sc, a, nv, i)
        if s not in state:
            probs.append(("correction", a, s))
    comps = (sc["mech"].get("comp") or []) + (sc["cost_comp"] or [] if any(x[0] == "@cost" for x in sc["tb"]) else [])
    for c in comps:
        keys = c[2] if c[0] == "mul" else (c[4] if c[0] == "cond" else ([c[4]] if c[0] == "tier" else []))
        for k in keys:
            if k.startswith("@") or k == "days" and sc["dom"] == "energy" or k == "bags" or k == "claims":
                continue
            v = sc["ctx"][k]
            if f"{v:,}" not in state:
                probs.append(("ctx", k, v))
    h = sc["target"].get("hypo")
    if h and h["type"] == "withdraw" and sc["cands"][h["i"]]["label"] not in ins:
        probs.append(("hypo", h))
    return probs


def diff_count(a, b):
    """Number of single facts that differ between two multi specs."""
    d = 0
    for ca, cb in zip(a["cands"], b["cands"]):
        for k in set(ca["v"]) | set(cb["v"]):
            x, y = ca["v"].get(k), cb["v"].get(k)
            if k == "panel" and x is not None:
                d += sum(1 for p, q in zip(x, y) if p != q)
            elif x != y:
                d += 1
    d += sum(1 for ga, gb in zip(a["gates"], b["gates"]) if ga != gb)
    d += sum(1 for k in set(a["ctx"]) | set(b["ctx"]) if a["ctx"].get(k) != b["ctx"].get(k))
    d += sum(1 for x, y in zip(a["corr"], b["corr"]) if x != y)
    if a["mech"] != b["mech"]:
        d += 1
    for k in ("target", "tb", "missing", "show", "alt"):
        if a[k] != b[k]:
            d += 100
    return d


# ------------------------------------------------------------------------------------------------ resp (text level)
def _norm(t):
    return re.sub(r"\s+", " ", t.lower()).strip()


def _time_min(s):
    m = re.search(r"\b(\d{1,2}):(\d{2})(?:\s*(am|pm))?", s)
    if m:
        h, mi, ap = int(m.group(1)), int(m.group(2)), m.group(3)
    else:
        m = re.search(r"\b(\d{1,2})\s*(am|pm)\b", s)
        h, mi, ap = int(m.group(1)), 0, m.group(2)
    if ap == "pm" and h != 12:
        h += 12
    if ap == "am" and h == 12:
        h = 0
    return h * 60 + mi


def verify_resp(item, state):
    topic = TOPIC[item["topic"]]
    labels = [r["label"] for r in item["resps"]]
    # split replies out of the rendered state
    pos = []
    for L in labels:
        m = re.search(r"(?m)^(?:\[)?" + re.escape(L) + r"(?= \(sent| - | \|)", state)
        assert m, L
        pos.append(m.start())
    assert pos == sorted(pos)
    blocks = [state[p:(pos[k + 1] if k + 1 < len(pos) else len(state))] for k, p in enumerate(pos)]
    heads, texts = [], []
    for b in blocks:
        if re.match(r"^\S+ \d+ \(sent ", b):
            h, _, t = b.partition("): ")
            heads.append(h)
            texts.append(t)
        else:
            h, _, t = b.partition("\n")
            heads.append(h)
            texts.append(t)
    sent = [_time_min(h) for h in heads]
    # key lines and essential marks, read from the text
    key_block = state.split("\n\n")[1]
    key_lines = [ln[2:] for ln in key_block.split("\n") if ln.startswith("- ")]
    facts = [next(f for f in topic["facts"] if f["id"] == x["id"]) for x in item["facts"]]
    keyval, essential = {}, set()
    for f in facts:
        hit = None
        for ln in key_lines:
            base = ln.replace(" (essential)", "")
            if f["kind"] == "val":
                for v in f["vals"]:
                    if base == f["key"].format(v=v):
                        hit = (v, ln)
            else:
                if base == f["key_t"]:
                    hit = (True, ln)
                elif base == f["key_f"]:
                    hit = (False, ln)
        assert hit is not None, f["id"]
        keyval[f["id"]] = hit[0]
        if hit[1].endswith("(essential)"):
            essential.add(f["id"])
    # statuses from reply text
    sts = []
    for t in texts:
        tn = _norm(t)
        st = {}
        for f in facts:
            right = wrong = False
            if f["kind"] == "val":
                for v in f["vals"]:
                    forms = [v] + f["eq"].get(v, [])
                    for form in forms:
                        for s in f["say"]:
                            if _norm(s.format(v=form)) in tn:
                                if v == keyval[f["id"]]:
                                    right = True
                                else:
                                    wrong = True
            else:
                for s in f["say_t"]:
                    if _norm(s) in tn:
                        right, wrong = (right or keyval[f["id"]] is True), (wrong or keyval[f["id"]] is False)
                for s in f["say_f"]:
                    if _norm(s) in tn:
                        right, wrong = (right or keyval[f["id"]] is False), (wrong or keyval[f["id"]] is True)
            st[f["id"]] = "cw" if right and wrong else ("c" if right else ("w" if wrong else "o"))
        sts.append(st)
    fids = [f["id"] for f in facts]
    rub = item["rubric"]
    if rub == "cc":
        good = [k for k, s in enumerate(sts) if all(s[f] == "c" for f in fids)]
        assert len(good) <= 1
        out = labels[good[0]] if good else "NONE"
    elif rub == "pts":
        m = re.search(r"\+(\d+) for each key point|earns (\d+) point\(s\)|correct key point = \+(\d+)", state)
        pc = int(next(g for g in m.groups() if g))
        m = re.search(r"-(\d+) for each key point|loses (\d+) point\(s\)|contradicted key point = -(\d+)", state)
        pw = int(next(g for g in m.groups() if g))
        tot = [sum(pc if s[f] == "c" else (-pw if s[f] in ("w", "cw") else 0) for f in fids) for s in sts]
        best = max(tot)
        out = min((k for k in range(len(sts)) if tot[k] == best), key=lambda k: sent[k])
        out = labels[out]
    else:
        passing = [k for k, s in enumerate(sts) if all(s[f] == "c" for f in essential) and
                   all(s[f] not in ("w", "cw") for f in fids)]
        if not passing:
            out = "NONE"
        else:
            cnt = {k: sum(1 for f in fids if f not in essential and sts[k][f] == "c") for k in passing}
            best = max(cnt.values())
            out = labels[min((k for k in passing if cnt[k] == best), key=lambda k: sent[k])]
    return rk_resp.gold_option(item, out)


# ------------------------------------------------------------------------------------------------ math
def _d(x):
    return Dm(x.numerator) / Dm(x.denominator) if isinstance(x, Fr) else Dm(x)


def _cents(x):
    x = Dm(x)
    assert x == x.to_integral_value(), x
    x = int(x)
    return f"{x // 100:,}.{x % 100:02d}"


def expected_math(tk, p):
    D = Dm
    if tk == "bill":
        tot = D(p["S"]) * D(100 + p["p"]) / D(100)
        return "$" + _cents(tot), "$" + _cents(tot / D(p["n"]))
    if tk == "disc":
        sale = D(p["P"]) * D(100 - p["d"]) / D(100)
        return "$" + _cents(sale), "$" + _cents(sale * D(100 + p["t"]) / D(100))
    if tk == "ot":
        extra = D(p["h"] - p["base"]) * D(p["r"]) * D("1.5")
        return "$" + _cents(extra), "$" + _cents(D(p["base"]) * D(p["r"]) + extra)
    if tk == "recipe":
        f = D(p["a"]) * D(p["t"]) / D(p["s"])
        m = D(p["b"]) * D(p["t"]) / D(p["s"])
        assert f == f.to_integral_value() and m == m.to_integral_value()
        return f"{int(f)} g", f"{int(m)} ml"
    if tk == "trip":
        mins = D(p["d"]) * D(60) / D(p["v"])
        assert mins == mins.to_integral_value()
        mins = int(mins)
        arr = p["dep"] + mins
        return f"{mins // 60} h {mins % 60:02d} min", f"{arr // 60:02d}:{arr % 60:02d}"
    if tk == "fuel":
        litres = D(p["d"]) * D(p["c"]) / D(10) / D(100)
        assert litres * 10 == (litres * 10).to_integral_value()
        return f"{litres:.1f} L", "$" + _cents(litres * D(p["q"]))
    if tk == "paint":
        area = D(p["l"]) * D(p["h"]) - D(p["win"])
        litres = area * D(p["coats"]) / D(p["cov"])
        assert litres * 10 == (litres * 10).to_integral_value()
        tin = _d(Fr(p["tin"]))
        tins = int((litres / tin).to_integral_value(rounding=ROUND_CEILING))
        return f"{litres:.1f} L", f"{tins} tin" + ("" if tins == 1 else "s")
    if tk == "int":
        i = D(p["P"]) * D(p["r"]) * D(p["y"]) / D(100)
        return "$" + _cents(i), "$" + _cents(D(p["P"]) + i)
    if tk == "elec":
        units = p["e"] - p["s"]
        pence = D(units) * D(p["rate"]) + D(p["sc"]) * D(p["days"])
        return f"{units:,} kWh", "£" + _cents(pence)
    if tk == "tiles":
        area = D(p["l"]) / D(10) * D(p["w"]) / D(10)
        raw = area / D("0.25") * D(100 + p["waste"]) / D(100)
        tiles = int(raw.to_integral_value(rounding=ROUND_CEILING))
        boxes = -(-tiles // p["box"])
        return f"{tiles} tiles", f"{boxes} box" + ("" if boxes == 1 else "es")
    if tk == "ship":
        def one(w10):
            kg = -(-w10 // 10)
            return D(p["a"]) + D(p["b"]) * D(kg - 1)
        c1 = one(p["w1"])
        return "$" + _cents(c1), "$" + _cents(c1 + one(p["w2"]))
    raise ValueError(tk)


TOKEN = re.compile(r"[$£][\d,]+\.\d{2}|\d+ h \d{2} min|\b\d{2}:\d{2}\b|\d+\.\d L\b|\b\d+ g\b|\b\d+ ml\b|"
                   r"[\d,]+ kWh|\b\d+ tiles?\b|\b\d+ box(?:es)?\b|\b\d+ tins?\b")


def verify_math(item, state):
    e1, e2 = expected_math(item["tk"], item["p"])
    prob = state.split("\nTask:")[0]
    p = item["p"]
    plain = {"bill": ["n", "p"], "disc": ["d", "t"], "ot": ["h", "base"], "recipe": ["s", "t", "a", "b"],
             "trip": ["d", "v"], "fuel": ["d"], "paint": ["l", "h", "win", "coats", "cov"], "int": ["r", "y"],
             "elec": ["rate", "sc", "days"], "tiles": ["box"], "ship": []}[item["tk"]]
    moneyp = {"bill": ["S"], "disc": ["P"], "ot": ["r"], "fuel": ["q"], "int": ["P"], "ship": ["a", "b"]}.get(item["tk"], [])
    for k in plain:
        if not re.search(r"(?<![\d.,])" + str(p[k]) + r"(?![\d])", prob):
            raise AssertionError(("param not printed", k, p[k]))
    for k in moneyp:
        if rk_math.money(p[k]) not in prob:
            raise AssertionError(("money param not printed", k, p[k]))
    if item["tk"] == "elec":
        assert f"{p['s']:,}" in prob and f"{p['e']:,}" in prob
    lines = state.split("\n")
    good = []
    for a in item["answers"]:
        ln = next(x for x in lines if re.match(r"^(?:- )?" + re.escape(a["label"]) + r"\b", x))
        txt = ln.split(":", 1)[1] if ":" in ln else ln
        toks = TOKEN.findall(txt)
        if toks == [e1, e2]:
            good.append(a["label"])
    assert len(good) <= 1
    return rk_math.gold_option(item, good[0] if good else "NONE")


# ------------------------------------------------------------------------------------------------ vote
def verify_vote(state):
    lines = state.split("\n")
    opts = [m.group(1) for m in (re.match(r"^- ([A-Z][a-z]+ [A-Z0-9]):", x) for x in lines) if m]
    rule = next(x for x in lines if "ounting rule" in x or x.startswith(("Borda", "Instant", "Two-round", "Approval",
                                                                         "Only first")))
    if "Borda" in rule:
        method = "borda"
    elif "nstant runoff" in rule:
        method = "irv"
    elif "top-two" in rule or "Two-round" in rule:
        method = "runoff"
    elif "pproval" in rule:
        method = "approval"
    else:
        method = "plurality"
    groups = []
    start = next(k for k, x in enumerate(lines) if x.startswith(("Ballots", "Ranked ballots", "Preference ballots")))
    for x in lines[start + 1:]:
        m = re.match(r"^(\d+) [^:]+: (.+)$", x)
        if m:
            sep = ", " if method == "approval" else " > "
            groups.append((int(m.group(1)), m.group(2).split(sep)))
    total = sum(n for n, _ in groups)
    k = len(opts)

    def first_counts(alive):
        c = {o: 0 for o in alive}
        for n, rk in groups:
            top = next((o for o in rk if o in alive), None)
            if top is not None:
                c[top] += n
        return c

    def second_counts():
        c = {o: 0 for o in opts}
        for n, rk in groups:
            if len(rk) >= 2:
                c[rk[1]] += n
        return c

    def winner(score, pool, tb=None):
        hi = max(score[o] for o in pool)
        w = [o for o in pool if score[o] == hi]
        if len(w) > 1 and tb:
            hi2 = max(tb[o] for o in w)
            w = [o for o in w if tb[o] == hi2]
        return w[0] if len(w) == 1 else None

    if method == "plurality":
        w = winner(first_counts(opts), opts, second_counts())
    elif method == "borda":
        pts = {o: 0 for o in opts}
        for n, rk in groups:
            for i, o in enumerate(rk):
                pts[o] += n * (k - 1 - i)
        w = winner(pts, opts, first_counts(opts))
    elif method == "approval":
        c = {o: sum(n for n, rk in groups if o in rk) for o in opts}
        w = winner(c, opts)
    elif method == "irv":
        orig = first_counts(opts)
        alive = list(opts)
        w = None
        while True:
            f = first_counts(alive)
            maj = [o for o in alive if f[o] * 2 > total]
            if maj:
                w = maj[0]
                break
            if len(alive) == 2:
                w = winner(f, alive)
                break
            lo = min(f[o] for o in alive)
            out = [o for o in alive if f[o] == lo]
            if len(out) > 1:
                lo2 = min(orig[o] for o in out)
                out = [o for o in out if orig[o] == lo2]
            alive.remove(sorted(out, key=lambda o: opts.index(o))[-1])
    else:
        f = first_counts(opts)
        maj = [o for o in opts if f[o] * 2 > total]
        if maj:
            w = maj[0]
        else:
            s = second_counts()
            order = sorted(opts, key=lambda o: (f[o], s[o]), reverse=True)
            if len(order) > 2 and (f[order[1]], s[order[1]]) == (f[order[2]], s[order[2]]):
                w = None
            else:
                a, b = order[0], order[1]
                va = sum(n for n, rk in groups if rk.index(a) < rk.index(b))
                vb = total - va
                w = a if va > vb else (b if vb > va else None)
    return w if w else rk_vote.tie_opt()
