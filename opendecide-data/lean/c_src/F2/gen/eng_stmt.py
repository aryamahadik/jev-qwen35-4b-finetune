"""S5 line-item statements (held out; mix-tuning dev and depth sweep only, never a training row).

A statement (description | quantity | rate | amount): amounts printed, marked "computed" (M4: the line's pricing,
quantity x rate or the B4 overtime split), or blank with "none" quantity and rate cells (M3: nothing charged). Rules:
B4 multiplier above a stated unit count (scope: the line), a percentage deduction with a floor or a cap (X4, per
statement), positive deduction lines subtracted (U5), R1 / R2 rounding, a settlement date (D17: period end + N
calendar days, then D7's roll; D6a and the holiday line). Schemas: YN-T, CH-V, CH-D. Closed world only.
"""
from __future__ import annotations

import copy
import datetime as dt

from . import dcard, lex, money, options as O, qtext, render as R, rowkit
from .cards import common_card, style_set, DV_BY_STYLE
from .common import D, ONE, ZERO, HUNDRED, on_grid, quant, money_str, num_str, pct_str, date_str
from .money import Reject
from .mrows import gen_entity_id, thr_place_far, near_family, near_op

NAME = "stmt"
EARN = [("shift hours", "hour", "hours"), ("call-out visits", "visit", "visits"), ("standby days", "day", "days"),
        ("training sessions", "session", "sessions"), ("site inspections", "inspection", "inspections"),
        ("night shifts", "shift", "shifts")]
DEDS = ["uniform deduction", "canteen charges", "union dues", "advance repaid", "locker fee"]


def make_card(card, pack, rng, **kw):
    from .mcard import Labels
    common_card(card, pack, rng)
    L = Labels()
    s = {"dec2": rng.random() < 0.6, "cur": pack["currency"]}
    s["unit"] = D("0.01") if s["dec2"] else ONE
    earn = rng.sample(EARN, rng.randint(2, 3))
    s["earn"] = [e[0] for e in earn]
    s["b4"] = earn[0][0] if (rng.random() < 0.6 and not card.get("no_b4")) else None
    s["b4x"], s["b4m"] = rng.choice([8, 10, 20, 35, 40]), rng.choice([D("1.5"), D(2), D("1.25")])
    s["deds"] = rng.sample(DEDS, rng.randint(0, 2)) if not card.get("no_deds") else []
    s["gross"] = L(rng.choice(["gross pay", "gross earnings", "statement subtotal"]))
    s["net"] = L(rng.choice(["net pay", "amount payable", "net settlement"]))
    s["pd"] = L(rng.choice(["pension contribution", "levy deduction", "scheme deduction"]))
    s["pct"] = L(rng.choice(["contribution rate", "levy rate", "deduction rate"]))
    s["lim_kind"] = rng.choice(["floor", "cap"])
    s["lim"] = L("minimum deduction" if s["lim_kind"] == "floor" else "maximum deduction")
    s["per"] = "pay period end"
    s["N"] = rng.choice([3, 5, 7, 10, 14])
    sem = {"R1": rng.choice(["half_up", "half_even", "floor", "ceiling"]), "R1u": s["unit"], "R2": rng.choice(["final", "line"]),
           "X4": {"pctded": "total"}, "D7": rng.choice(["fwd", "back", "none"])}
    if card["schema"] == "YN-T":
        sem["R3"] = "rounded"
    s["sem"] = sem
    s["date_form"] = rng.choice(["gb_long", "us_long", "iso"])
    card["s"] = s
    card["shown"] = set(k for k in sem if k != "R1u") | {"R4"}
    card["omitted"] = []
    card["variants"] = []
    card["short"] = False
    card["defs_style"] = rng.choice(["one_line", "decision_list"])
    card["dv"] = rng.choice(DV_BY_STYLE[card["defs_style"]])
    card["task"] = rng.choice(["Work out the {net} for the {ent} in the text under these rules.",
                               "Apply these rules to the statement for the {ent} in the text."]).format(net=s["net"], ent=card["ent_sg"])
    card["none_ok"] = False
    card["styles"] = style_set(rng, card["card_id"], card.get("held_out", True), True)
    card["res_unit"] = s["unit"]
    return card


def mstr(v, card):
    return money_str(D(v), card["s"]["dec2"]) + " " + card["s"]["cur"]


def lbl(desc, what):
    return f"{desc} {what}"


def clauses(card, sem, shown, world):
    s = card["s"]
    out = [("Scope", "W0", lex.W0), ("Record", "W1", lex.W1), ("Statement", "STMT", lex.STMT_INTRO),
           ("Blank amounts", "M3", lex.M3)]
    rules = lex.fill(lex.M4_RULES["b4"], type=s["b4"]) if s["b4"] else lex.M4_RULES["plain"]
    out.append(("Computed amounts", "M4", lex.fill(lex.M4, rules=rules)))
    if s["b4"]:
        out.append(("Overtime", "B4", lex.fill(lex.B4, type=s["b4"], X=s["b4x"], m=num_str(s["b4m"]))))
    types = ", ".join(s["earn"][:-1]) + " and " + s["earn"][-1]
    out.append(("Gross", "CORE", lex.fill(lex.GROSS, gross=s["gross"], types=types)))
    out.append(("Deduction", "X4", lex.fill(lex.PCTDED[s["lim_kind"]], pd=s["pd"], pct=s["pct"], gross=s["gross"], lim=s["lim"])
                + " " + lex.fill(lex.X4_STMT[s["lim_kind"]], lim=s["lim"])))
    if s["deds"]:
        dl = ", ".join(s["deds"][:-1]) + " and " + s["deds"][-1] if len(s["deds"]) > 1 else s["deds"][0]
        out.append(("Net", "U5", lex.U5 + " " + lex.fill(lex.NET_DED, net=s["net"], gross=s["gross"], pd=s["pd"], deds=dl)))
    else:
        out.append(("Net", "CORE", lex.fill(lex.NET_NODED, net=s["net"], gross=s["gross"], pd=s["pd"])))
    u = (money_str(D(sem["R1u"]), True) if D(sem["R1u"]) < 1 else num_str(D(sem["R1u"]))) + " " + s["cur"]
    out.append(("Rounding", "R1", lex.fill(lex.R1[sem["R1"]], res="amounts", u=u)))
    out.append(("Rounding stage", "R2", lex.fill(lex.R2["final"], res=s["net"]) if sem["R2"] == "final"
                else lex.fill(lex.R2_STMT_LINE, pd=s["pd"])))
    if "R3" in sem:
        out.append(("Comparisons", "R3", lex.fill(lex.R3[sem["R3"]], res="amounts")))
    out.append(("Other rounding", "R4", lex.R4))
    out.append(("Dates", "D1", lex.D1))
    out.append(("Settlement", "D17", lex.fill(lex.D17, N=s["N"], per=s["per"])))
    out.append(("Business days", "D6A", lex.D6A))
    out.append(("Roll rule", "D7", lex.fill(lex.D7[sem["D7"]], dl="settlement date")))
    return out


SWEEP_KINDS = {2: ["printed", "blank", "blank"], 3: ["printed", "printed", "blank"], 4: ["computed", "printed", "blank"],
               5: ["computed", "computed", "blank"]}


def draw(card, rng, depth=None):
    """One statement: earning lines (printed / computed / blank), deduction lines, rates, limits, dates."""
    s = card["s"]
    dec2 = s["dec2"]
    lines = []
    vals = {}
    plan = SWEEP_KINDS.get(depth) if depth else None
    for i, desc in enumerate(s["earn"]):
        kind = rng.choice(["printed", "computed", "computed", "blank"]) if i > 0 else rng.choice(["printed", "computed", "computed"])
        if plan is not None:
            kind = plan[i] if i < len(plan) else "blank"
        q = D(rng.randint(1, 60))
        r = (D(rng.randint(800, 6000)) / 100) if dec2 else D(rng.randint(8, 60))
        ql, rl, al = lbl(desc, "quantity"), lbl(desc, "rate"), lbl(desc, "amount")
        if kind == "blank":
            lines.append({"p": "blank", "mark": "blank", "desc": desc})
        elif kind == "printed":
            vals[ql], vals[rl], vals[al] = q, r, q * r
            lines.append({"p": "stated", "a": al, "q": ql, "r": rl, "mark": "printed", "desc": desc})
        else:
            vals[ql], vals[rl] = q, r
            if s["b4"] == desc:
                vals["B4 threshold"], vals["B4 multiplier"] = D(s["b4x"]), s["b4m"]
                lines.append({"p": "b4", "q": ql, "r": rl, "b4x": "B4 threshold", "b4m": "B4 multiplier", "mark": "computed", "desc": desc})
            else:
                lines.append({"p": "mul", "q": ql, "r": rl, "mark": "computed", "desc": desc})
    vals[s["pct"]] = D(rng.choice(["2", "2.5", "3", "4", "5", "5.5", "6", "7.5"]))
    vals[s["lim"]] = (D(rng.randint(2000, 9000)) / 100) if dec2 else D(rng.randint(20, 90))
    for dd in s["deds"]:
        vals[lbl(dd, "amount")] = (D(rng.randint(500, 9000)) / 100) if dec2 else D(rng.randint(5, 90))
    per = dcard.rand_date(rng)
    hol = []
    for _ in range(rng.choice([0, 1, 1, 2])):
        h = per + dt.timedelta(days=rng.randint(1, s["N"] + 6))
        if h.weekday() < 5 and h not in hol:
            hol.append(h)
    return {"lines": lines, "vals": vals, "per": per, "hol": sorted(hol)}


def make_lp(card, d, q):
    s = card["s"]
    lines = []
    for ln in d["lines"]:
        lines.append({k: ln[k] for k in ("p", "q", "r", "a", "b4x", "b4m", "mark") if ln.get(k) is not None})
    steps = [{"op": "pctded", "id": "pctded", "v": [s["pct"], s["lim"]], "lim": s["lim_kind"], "scope": "total"}]
    if s["deds"]:
        steps.append({"op": "ded", "id": "ded", "v": [lbl(x, "amount") for x in s["deds"]]})
    sem = dict(s["sem"])
    if len([l for l in lines if l["p"] != "blank"]) < 1:
        raise Reject("no earning line")
    LP = {"eng": "stmt", "world": "closed", "unit": s["unit"], "vals": dict(d["vals"]), "facts": {}, "lines": lines,
          "steps": steps, "excs": [], "sem": {k: v for k, v in sem.items() if k not in ("D7",)}, "target": "final", "q": q,
          "settle": {"N": s["N"], "D7": sem["D7"], "per_date": d["per"], "holidays": list(d["hol"])},
          "marks": [l["mark"] for l in d["lines"]]}
    return LP


def settle_date(LP):
    from .dateeval import roll
    st = LP["settle"]
    x = st["per_date"] + dt.timedelta(days=st["N"])
    return roll(x, st["D7"], set(st["holidays"]))


def value(LP, rd=None):
    return money.evaluate({**LP, "eng": "money"}, rd or {})


def readings(LP):
    from .mcard import alt_readings
    out = alt_readings({**LP, "eng": "money"}, set(LP["sem"]) | {"R1", "R4"})
    lim = LP["steps"][0]["lim"]
    out.append(("E-floor" if lim == "floor" else "E-cap", {"err": "E-floor" if lim == "floor" else "E-cap"}))
    return out


def gen_row(card, rng, var=0, want=None):
    want = want or {}
    sch = card["schema"]
    for attempt in range(300):
        try:
            d = draw(card, rng, depth=want.get("sweep_depth"))
            if sch == "CH-D":
                r = _settle_row(card, rng, d, want)
            else:
                r = _money_row(card, rng, d, want)
            if r is not None:
                return r
        except (Reject, ArithmeticError):
            continue
    raise Reject("no statement row")


def _ops(LP):
    v, tr = value(LP)
    return v, tr


def _money_row(card, rng, d, want):
    s = card["s"]
    LP = make_lp(card, d, {"kind": "value"})
    v, tr = _ops(LP)
    if v < 0 or not on_grid(v, D(LP["unit"])):
        return None
    ops = tr.ops
    printed = {}
    if want.get("sweep_depth") is not None:
        if ops != want["sweep_depth"]:
            return None
        grp = "d" if ops >= 3 else "a" if ops == 1 else "b"
    elif ops <= 2:
        grp = "a" if ops == 1 else "b"
    else:
        grp = "d" if ops <= 6 else None       # S5 is dev only: statements are deeper by shape; depth is logged
        if grp is None:
            return None
    if card["schema"] == "YN-T":
        neg = want.get("neg", 0)
        aff = want["aff"] if "aff" in want else rng.random() < 0.5
        Rv = money.compared_value({**LP, "eng": "money"}, {})
        unit = s["unit"]
        if rng.random() < 0.5:
            r = rng.random()
            delta = 0 if r < 0.3 else (-1 if r < 0.65 else 1)
            fam = near_family(rng, delta, aff)
            op = near_op(rng, delta, aff, fam)
            T = Rv - delta * unit
            place = {"near": True}
        else:
            op, T = thr_place_far(rng, Rv, unit, aff)
            place = {"near": False}
        if T <= 0:
            return None
        LP["q"] = {"kind": "thr", "cmp": op, "T": T, "neg": neg}
        a = money.yn_label({**LP, "eng": "money"}, {})[0]
        if a != aff:
            return None
        return {"LP": LP, "_lines": d["lines"], "qkind": "thr", "aff": aff, "neg": neg, "gold": aff ^ (neg % 2 == 1), "tags": ["cmp:" + ("incl" if op in ("ge", "le") else "excl")],
                "group": grp, "depth": ops, "ops": ops, "sel": tr.sel, "deep": grp == "d", "printed": set(), "placement": place}
    hk = {}
    for eid, rd in readings(LP):
        try:
            x, _ = value(LP, rd)
        except (Reject, ArithmeticError, ValueError):
            continue
        if x != v and x >= 0 and on_grid(x, D(LP["unit"])):
            hk.setdefault(x, []).append(eid)
    for ln in LP["lines"]:
        if ln.get("mark") == "computed":
            LP2 = copy.deepcopy(LP)
            LP2["lines"] = [l if l is not ln else {"p": "blank", "mark": "blank"} for l in LP["lines"]]
            try:
                x, _ = value(LP2)
                if x != v and x >= 0 and on_grid(x, D(LP["unit"])):
                    hk.setdefault(x, []).append("E-blank")
            except (Reject, ArithmeticError):
                pass
    single = O.single_hook_values(hk)
    k = min(rng.choice([2, 3, 4, 5]), 1 + len(single))
    if k < 2:
        return None
    rr = O.held_rank(want, k, rng)
    pr = O.pick_ranked(rng, v, single, k, rr)
    if pr is None:
        return None
    vals, errs = pr
    opts = [mstr(x, card) for x in vals]
    oerr = {mstr(x, card): e for x, e in errs.items()}
    oerr[mstr(v, card)] = "gold"
    LP["q"] = {"kind": "value"}
    return {"LP": LP, "_lines": d["lines"], "qkind": "value", "gold": mstr(v, card), "options": opts, "opt_err": oerr,
            "tags": [f"err:{e}" for e in errs.values()], "k": len(opts), "rank": rr, "group": grp, "depth": ops,
            "ops": ops, "sel": tr.sel, "deep": grp == "d", "printed": set()}


def _settle_row(card, rng, d, want):
    from .dateeval import roll
    s = card["s"]
    LP = make_lp(card, d, {"kind": "settle"})
    L = settle_date(LP)
    st = LP["settle"]
    hooks = {}
    base = st["per_date"] + dt.timedelta(days=st["N"])
    for f in ("fwd", "back", "none"):
        if f != st["D7"]:
            x = roll(base, f, set(st["holidays"]))
            hooks.setdefault(x, []).append(f"E-alt:D7:{f}")
    x = roll(base - dt.timedelta(days=1), st["D7"], set(st["holidays"]))
    hooks.setdefault(x, []).append("E-day")
    x = roll(base, st["D7"], set())
    hooks.setdefault(x, []).append("E-hol")
    hooks.pop(L, None)
    single = O.single_hook_values(hooks)
    k = min(rng.choice([2, 3, 4]), 1 + len(single))
    if k < 2:
        return None
    rr = O.held_rank(want, k, rng)
    pr = O.pick_ranked(rng, L, single, k, rr)
    if pr is None:
        return None
    vals, errs = pr
    f = s["date_form"]
    opts = [date_str(x, f) for x in vals]
    oerr = {date_str(x, f): e for x, e in errs.items()}
    oerr[date_str(L, f)] = "gold"
    return {"LP": LP, "_lines": d["lines"], "qkind": "settle", "gold": date_str(L, f), "options": opts, "opt_err": oerr,
            "tags": [f"err:{e}" for e in errs.values()], "k": len(opts), "rank": rr, "group": "a", "depth": 1, "ops": 1,
            "sel": 1, "deep": False, "printed": set(), "opt_dates": vals}


def new_eid(card, rng, used):
    return gen_entity_id(card, rng, used)


def doc_ir(card, spec, eid):
    s = card["s"]
    LP = spec["LP"]
    rows = []
    vals = LP["vals"]
    for ln, mark in zip(LP["lines"], LP["marks"]):
        pass
    for ln in card["_last_lines"]:
        desc = ln["desc"]
        if ln["mark"] == "blank":
            rows.append([desc, "none", "none", R.BLANK])
        elif ln["mark"] == "printed":
            rows.append([desc, num_str(vals[ln["q"]]), mstr(vals[ln["r"]], card), mstr(vals[ln["a"]], card)])
        else:
            rows.append([desc, num_str(vals[ln["q"]]), mstr(vals[ln["r"]], card), lex.COMPUTED_MARK])
    for dd in s["deds"]:
        rows.append([dd, "none", "none", mstr(vals[lbl(dd, "amount")], card)])
    f = s["date_form"]
    st = LP["settle"]
    rec = [(f"{card['ent_sg']} ID", eid), (s["per"], date_str(st["per_date"], f, weekday=True)),
           (s["pct"], pct_str(vals[s["pct"]])), (s["lim"], mstr(vals[s["lim"]], card)),
           (lex.HOL_NOTE, "; ".join(date_str(h, f, weekday=True) for h in st["holidays"]) if st["holidays"] else "none")]
    rel = [st["per_date"], st["per_date"] + dt.timedelta(days=st["N"])] + list(st["holidays"]) + spec.get("opt_dates", [])
    lo, hi = min(rel) - dt.timedelta(days=3), max(rel) + dt.timedelta(days=4)
    strip = [lo + dt.timedelta(days=i) for i in range((hi - lo).days + 1)]
    if len(strip) > 45:
        raise Reject("strip")
    rec.append((lex.STRIP_NOTE, "; ".join(date_str(x, f, weekday=True) for x in strip)))
    blocks = [{"type": "table", "caption": "Statement", "columns": ["description", "quantity", "rate", "amount"], "rows": rows},
              {"type": "fields", "label": card["rec_label"], "pairs": [list(p) for p in rec]}]
    doc = {"blocks": blocks}
    if card.get("doc_title"):
        doc["title"] = card["doc_title"]
    return doc


def question(card, spec, eid, rng):
    s = card["s"]
    if spec["qkind"] == "thr":
        T = mstr(spec["LP"]["q"]["T"], card)
        op = spec["LP"]["q"]["cmp"]
        q, info = qtext.thr_question(s["net"], eid, op, T, spec["LP"]["q"]["neg"], spec.get("tf", False), rng)
        info["pol"] = qtext.pol_tag("up" if op in ("ge", "gt") else "down", card["side_money"], spec["LP"]["q"]["neg"])
        return q, info
    if spec["qkind"] == "value":
        return lex.fill(rng.choice(lex.Q_VALUE), res=s["net"], id=eid), {"neg": 0, "tf": 0}
    return lex.fill(rng.choice(lex.Q_SETTLE), id=eid), {"neg": 0, "tf": 0}


def to_row(card, spec, rng, *, row_id, var=0, eid=None, inert=None, attack=None, role="clean", style_key=None):
    q, qinfo = question(card, spec, eid, rng)
    spec["decisive"] = []
    card["_last_lines"] = spec["_lines"]
    doc_fn = lambda single: doc_ir(card, spec, eid)  # noqa: E731
    cl = clauses(card, card["s"]["sem"], card["shown"], "closed")
    cir = R.card_ir(card, cl)
    row, res, P = rowkit.assemble(card, spec, row_id=row_id, var=var, doc_fn=doc_fn, question=q, qinfo=qinfo,
                                  card_ir_=cir, role=role, style_key=style_key)
    return row, res, P, q
