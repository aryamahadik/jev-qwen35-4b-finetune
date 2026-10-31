"""Money cards (S1 forward formula graphs, S2 target-first, S5 reuse): plans, skeleton, card clauses, value draws,
labeled problem LP, readings (E-alt and named errors) and hook values.

A plan fixes the formula type (lines, steps, exceptions), so the card's relevant SEM dimensions follow from it
(2.1, R1-17). Every sentence comes from lex templates; every document value is referred to by its label.
"""
from __future__ import annotations

import itertools
import math
from decimal import Decimal

from . import lex, money
from .common import D, ONE, HUNDRED, on_grid, money_str, num_str, pct_str, quant
from .money import Reject

FLAGS = ["rush order", "member account", "weekend work", "repeat customer", "after-hours call", "group booking",
         "early payment", "loyalty card", "own equipment supplied", "second visit", "shared load", "contract client",
         "remote site", "hazard work", "night shift", "fragile goods", "bulk order", "trade account", "prepaid",
         "escorted delivery", "online booking", "priority lane", "site induction done", "returning client"]
COUNTS = [("prior bookings", 0, 30), ("years as client", 0, 25), ("staff on site", 1, 12), ("days of notice", 0, 40),
          ("items in the order", 1, 60), ("open tickets", 0, 15)]
RESULT_NAMES = {"total": ["total charge", "amount payable", "invoice total", "amount due", "billable amount",
                          "job charge", "total fee"],
                "reimb": ["reimbursement", "amount refunded", "payout", "allowance paid"],
                "fee": ["service fee", "handling fee", "admin fee", "processing fee", "booking fee", "levy"],
                "net": ["balance", "net amount", "amount owed", "net balance"]}
OUTCOME_KINDS = ["approval route", "billing route", "handling level", "review path", "invoice track", "sign-off route"]
OUTCOME_SETS = [["desk approval", "team lead approval", "manager approval", "director approval", "board approval",
                 "panel approval"],
                ["invoice now", "invoice at month end", "invoice at quarter end", "split invoicing",
                 "deferred invoicing", "staged invoicing"],
                ["standard handling", "tracked handling", "supervised handling", "escalated handling",
                 "audited handling", "external handling"],
                ["fast lane", "regular lane", "checked lane", "held lane", "referred lane", "special lane"]]
MID_NAMES = {"disc": "discounted amount", "disc2": "discounted amount", "fee": "amount with the fee",
             "pctof": "fee before the minimum", "cap": "capped amount", "min": "amount after the minimum",
             "add": "amount with charges", "ded": "amount after deductions"}

PLANS = {
    "unit":     dict(lines="mul", steps=["add?"], exc="rate", rnd=False, mech=["partial", "exc", "plain"]),
    "unit_fee": dict(lines="mul", steps=["fee"], exc="rate", rnd=True, mech=["round", "partial", "exc", "plain"]),
    "cap":      dict(lines="mul", steps=["cap"], exc="rate", rnd=False, mech=["capfloor", "exc", "plain"]),
    "pct":      dict(lines="stated", steps=["fee"], exc="pct", rnd=True, mech=["round", "exc", "plain"]),
    "min":      dict(lines="stated", steps=["pctof", "min"], exc="pct", rnd=True, mech=["round", "capfloor", "exc", "plain"]),
    "disc":     dict(lines="stated", steps=["disc", "add?"], exc="pct", rnd=True, mech=["round", "exc", "plain"]),
    "disc_min": dict(lines="stated", steps=["disc", "min"], exc="pct", rnd=True, mech=["round", "capfloor", "exc", "plain"]),
    "net":      dict(lines="stated", steps=["ded", "floor0"], exc="add", rnd=False, mech=["exc", "plain"]),
    "disc2":    dict(lines="stated", steps=["disc2"], exc=None, rnd=True, mech=["round", "plain"]),
    "perk":     dict(lines="perk", steps=["add?"], exc="add", rnd=True, mech=["round", "partial", "exc", "plain"]),
    "listed":   dict(lines="stated", steps=["incfee"], exc=None, rnd=True, mech=["round", "plain"]),
}
STATED_NAMES = ["order amount", "contract value", "booking value", "claim amount", "invoice amount", "job value"]


class Labels:
    def __init__(self):
        self.used = set()

    def __call__(self, s):
        s = " ".join(s.split())
        base, i = s, 2
        while s.lower() in self.used:
            s = f"{base} {i}"
            i += 1
        self.used.add(s.lower())
        return s


def build(card, pack, rng):
    """Money skeleton card['m'] (labels, lines, steps with in/out names, exceptions, SEM vector)."""
    plan = PLANS[card["plan"]]
    L = Labels()
    qname, qsg, qpl = pack["qtys"][rng.randrange(min(5, len(pack["qtys"])))]
    rk = {"cap": "reimb", "net": "net", "pct": "fee", "min": "fee", "listed": "fee"}.get(card["plan"], "total")
    res = L(rng.choice(RESULT_NAMES[rk]))
    dec2 = card["dec2"]
    m = {"cur": pack["currency"], "dec2": dec2, "unit": D("0.01") if dec2 else ONE, "res": res, "lines": [],
         "steps": [], "excs": [], "qsg": qsg, "qpl": qpl, "partial": bool(card.get("partial")) and plan["lines"] == "mul", "k": None,
         "order_mode": False}
    nlines = card.get("nlines", 1)
    if plan["lines"] == "mul":
        kinds = ["standard", "extra", "weekend", "peak", "off-peak", "priority"]
        rng.shuffle(kinds)
        for i in range(nlines):
            if nlines == 1:
                ql, rl, lc = L(qname), L(f"rate per {qsg}"), L(f"{qsg} charge")
            else:
                ql, rl, lc = L(f"{kinds[i]} {qpl}"), L(f"{kinds[i]} rate per {qsg}"), L(f"{kinds[i]} charge")
            m["lines"].append({"p": "mul", "q": ql, "r": rl, "lc": lc})
    elif plan["lines"] == "perk":
        k = rng.choice([D(5), D(10), D(15), D(25), D(50), D(100)])
        m["k"] = k
        m["lines"].append({"p": "perk", "q": L(qname), "r": L(f"price per {num_str(k)} {qpl}"), "k": k,
                           "lc": L(f"{qsg} charge")})
    else:
        if card["plan"] == "net":
            nm = ["fees billed", "materials billed", "labour billed", "travel billed"]
            rng.shuffle(nm)
            for i in range(nlines):
                m["lines"].append({"p": "stated", "a": L(nm[i])})
        elif card["plan"] == "listed":
            m["lines"].append({"p": "stated", "a": L(rng.choice(["listed price", "list price", "shelf price"]))})
        else:
            m["lines"].append({"p": "stated", "a": L(rng.choice(STATED_NAMES))})
    priced = [l for l in m["lines"] if l["p"] in ("mul", "perk")]
    if len(m["lines"]) > 1:
        m["sub"] = L(rng.choice(["subtotal", "gross amount", "charges subtotal"]))
        base = m["sub"]
    else:
        base = priced[0]["lc"] if priced else m["lines"][0]["a"]
    m["base"] = base
    # steps
    raw = []
    for s in plan["steps"]:
        if s.endswith("?"):
            if not card.get("with_add"):
                continue
            s = s[:-1]
        raw.append(s)
    for s in raw:
        st = {"op": s, "id": s}
        if s == "add":
            st["v"] = L(rng.choice(["call-out fee", "booking charge", "delivery charge", "setup charge", "site fee"]))
        elif s == "fee":
            st["v"] = L(rng.choice(["service fee rate", "handling fee rate", "admin fee rate", "levy rate"]))
            st["fee"] = res if card["plan"] == "pct" else L(rng.choice(["service fee", "handling fee", "admin fee"]))
        elif s == "pctof":
            st["v"] = L(rng.choice(["fee rate", "commission rate", "charge rate"]))
        elif s == "disc":
            st["v"] = L(rng.choice(["member discount", "volume discount", "early booking discount", "trade discount"]))
        elif s == "disc2":
            a, b = rng.sample(["volume discount", "loyalty discount", "seasonal discount", "trade discount"], 2)
            st["v"] = [L(a), L(b)]
        elif s == "cap":
            st["v"] = L(rng.choice(["claim cap", "maximum payout", "reimbursement cap", "payout cap"]))
            st["scope"] = card.get("scope", "total")
        elif s == "min":
            st["v"] = L(rng.choice(["minimum charge", "minimum fee", "floor charge"]))
            st["scope"] = "total"
        elif s == "ded":
            nm = ["payments received", "credits applied", "deposit paid", "vouchers redeemed"]
            rng.shuffle(nm)
            st["v"] = [L(nm[i]) for i in range(card.get("nded", 1))]
        elif s == "incfee":
            st["v"] = L(rng.choice(["sales levy rate", "service charge rate", "duty rate"]))
            st["fee"] = res
        m["steps"].append(st)
    # in / out names (chain), or X1 order phrasing
    if card["plan"] == "disc" and card.get("with_add"):
        m["order_mode"] = True
    named = [s for s in m["steps"] if s["op"] != "floor0"]
    cur = base
    for i, st in enumerate(named):
        st["in"] = cur
        if st["op"] in ("fee",) and m_target(card) == "fee":
            st["out"] = st["fee"]
        elif st["op"] == "incfee":
            st["out"] = st["fee"]
        else:
            st["out"] = res if i == len(named) - 1 else L(MID_NAMES[st["op"]])
        cur = st["out"]
    if not named:
        # repair r1.1 (G5 flag, confirmed against Q1 "every question names its target node"): with no named step the
        # final value is the line charge (or subtotal) itself, so questions and rules name that node; v1.0 named an
        # undefined result ("total fee", "amount due")
        res = base
        m["res"] = base
    # exceptions
    nexc = card.get("nexc", 0) if plan["exc"] else 0
    flags = list(FLAGS)
    rng.shuffle(flags)
    cname, cvals = pack["cat"]
    cvals = [v for v in cvals if " and " not in v and " or " not in v][:5]
    fact_lbl = {}
    for no in range(1, nexc + 1):
        kind = plan["exc"]
        e = {"no": no, "kind": kind}
        if kind == "rate":
            ln = m["lines"][(no - 1) % len(m["lines"])]
            e["on"] = ln["r"]
            e["v"] = L(rng.choice(["express", "special", "member", "after-hours", "reduced", "priority"]) +
                       f" rate per {qsg}")
        elif kind == "pct":
            tgt = [s for s in m["steps"] if s["op"] in ("fee", "pctof", "disc")][0]
            e["on"] = tgt["v"]
            e["v"] = L(rng.choice(["reduced", "special", "partner", "promotional"]) + " " + tgt["v"])
        else:
            gen = [s for s in m["steps"] if s["op"] == "add"]
            if gen:
                e["on"] = gen[0]["v"]
            else:
                ded = [s for s in m["steps"] if s["op"] == "ded"]
                if not ded:
                    continue
                e["on"] = ded[0]["v"][0]
            e["v"] = L(rng.choice(["surcharge", "extra charge", "supplement", "loading"]))
        conn = card.get("conns", {}).get(no) or rng.choice(["O2", "O2", "UN1", "O1", "O3"])
        joins = {"O2": ["single", "and", "or1", "or2"], "UN1": ["single", "and", "or1"], "O1": ["and"],
                 "O3": ["or1"]}[conn]
        join = card.get("joins", {}).get(no) or rng.choice(joins)
        conds = []
        for ci in range(1 if join == "single" else 2):
            kc = rng.choice(["flag", "flag", "cat", "count"]) if cvals else rng.choice(["flag", "count"])
            if card.get("world") == "open" and ci == 0 and card.get("unk_type"):
                kc = card["unk_type"]
            if kc == "cat" and "cat" in fact_lbl:
                kc = "flag"
            if kc == "flag":
                conds.append({"f": L(flags.pop()), "op": "is", "v": "yes", "ftype": "flag"})
            elif kc == "cat":
                fact_lbl["cat"] = L(cname)
                conds.append({"f": fact_lbl["cat"], "op": "is", "v": rng.choice(cvals), "ftype": "cat",
                              "dom": list(cvals)})
            else:
                cn = rng.choice([c for c in COUNTS if c[0] not in fact_lbl])
                fact_lbl[cn[0]] = L(cn[0])
                op = rng.choice(["ge", "gt", "le", "lt"])
                x = rng.randint(cn[1] + 2, max(cn[1] + 3, cn[2] - 2))
                conds.append({"f": fact_lbl[cn[0]], "op": op, "v": str(x), "ftype": "count", "rng": (cn[1], cn[2]),
                              "ph": rng.randrange(2)})
        e.update({"conn": conn, "join": join, "conds": conds})
        m["excs"].append(e)
    # SEM vector (base variant)
    sem = {}
    if plan["rnd"]:
        sem["R1"] = card.get("r1") or rng.choice(["half_up", "half_even", "floor", "ceiling"])
        sem["R1u"] = m["unit"]
        if len(priced) >= 2:
            sem["R2"] = card.get("r2", "final")
        if card["schema"] in ("YN-T", "CH-O", "CL"):
            sem["R3"] = "rounded"
    if m["partial"]:
        sem["R5"] = card.get("r5") or rng.choice(["ceil", "floor"])
    if plan["lines"] == "perk":
        sem["U3"] = card.get("u3") or rng.choice(["pro_rata", "full_k"])
    lims = [s for s in m["steps"] if s["op"] in ("cap", "min")]
    if lims:
        sem["X4"] = {s["id"]: s["scope"] for s in lims}
    if any(s["op"] == "disc2" for s in m["steps"]):
        sem["X5"] = card.get("x5") or rng.choice(["succ", "added"])
    if any(s["op"] == "incfee" for s in m["steps"]):
        sem["X7"] = card.get("x7") or rng.choice(["include", "before"])
    if any(s["op"] == "floor0" for s in m["steps"]):
        sem["X8"] = "floor"
    if m["excs"]:
        sem["X2"] = {str(e["no"]): ("replace" if e["kind"] in ("rate", "pct") else "add") for e in m["excs"]}
        if len(m["excs"]) >= 2:
            sem["X3"] = card.get("x3") or rng.choice(["alone_lower", "alone_higher", "fold"])
    if m["order_mode"]:
        sem["X1"] = [0, 1]
    m["sem"] = sem
    m["target"] = m_target(card)
    m["round_what"] = res if "R2" not in sem else "charges"
    card["m"] = m
    return card


def m_target(card):
    return "fee" if card["plan"] in ("pct", "listed") else "final"


# ----------------------------------------------------------------------------------------------------------------- text

def mstr(v, card):
    return money_str(D(v), card["m"]["dec2"]) + " " + card["m"]["cur"]


def unit_phrase(card, u=None):
    u = D(u if u is not None else card["m"]["unit"])
    return (money_str(u, True) if u < 1 else num_str(u)) + " " + card["m"]["cur"]


def cond_text(c):
    if c["op"] == "is":
        return lex.fill(lex.C_IS, f=c["f"], v=c["v"])
    if c["op"] in lex.CMP_CARD_POST and c.get("ph", 0) == 1:
        return lex.fill(lex.C_NUM_POST, f=c["f"], x=c["v"], cmpph=lex.CMP_CARD_POST[c["op"]])
    phs = lex.CMP_CARD[c["op"]]
    return lex.fill(lex.C_NUM, f=c["f"], cmpph=phs[c.get("ph", 0) % len(phs)], x=c["v"])


def gate_text(e, join):
    conds = [cond_text(c) for c in e["conds"]]
    n = e["no"]
    if e["conn"] == "O1":
        return lex.fill(lex.G_O1, n=n, c1=conds[0], c2=conds[1])
    if e["conn"] == "O3":
        return lex.fill(lex.G_O3, n=n, c1=conds[0], c2=conds[1])
    c = conds[0] if join == "single" else lex.fill({"and": lex.J_AND, "or1": lex.J_OR1, "or2": lex.J_OR2}[join],
                                                   c1=conds[0], c2=conds[1])
    return lex.fill(lex.G_UN1 if e["conn"] == "UN1" else lex.G_O2, n=n, c=c)


def join_labels(labels):
    labels = [f"the {x}" for x in labels]
    return labels[0] if len(labels) == 1 else ", ".join(labels[:-1]) + " and " + labels[-1]


def clauses(card, sem, shown, world):
    """Ordered [(topic, sem_id, sentence)] for one card variant (sem = that variant's SEM vector)."""
    m = card["m"]
    res = m["res"]
    out = [("Scope", "W0", lex.W0)]
    if world == "closed":
        out.append(("Record", "W1", lex.W1))
    else:
        out.append(("Record", "W2", lex.fill(lex.W2, u=unit_phrase(card), nei=card["nei"])))
        seen = set()
        for e in m["excs"]:
            for c in e["conds"]:
                if c["ftype"] == "cat" and c["f"] not in seen:
                    seen.add(c["f"])
                    out.append(("Categories", "CATLIST", lex.fill(lex.CATLIST, f=c["f"], list=", ".join(c["dom"]))))
    pr = []
    for ln in m["lines"]:
        if ln["p"] == "mul":
            pr.append(lex.fill(lex.F_MUL, lc=ln["lc"], q=ln["q"], r=ln["r"]))
        elif ln["p"] == "perk":
            pr.append(lex.fill(lex.F_PERK, lc=ln["lc"], r=ln["r"], k=num_str(ln["k"]), units=m["qpl"], q=ln["q"]))
    if len(m["lines"]) > 1:
        names = [l["lc"] if l["p"] != "stated" else l["a"] for l in m["lines"]]
        pr.append(lex.fill(lex.F_SUM, tot=m["sub"], lines=join_labels(names)))
    if pr:
        out.append(("Pricing", "CORE", " ".join(pr)))
    if m["order_mode"]:
        names = []
        for st in m["steps"]:
            if st["op"] == "disc":
                out.append(("Discount", "R8", lex.fill(lex.F_DISC_X1, pct=st["v"]) + " " + lex.R8))
            elif st["op"] == "add":
                out.append(("Charges", "CORE", lex.fill(lex.F_ADD_X1, fixed=st["v"])))
        for i in sem["X1"]:
            names.append("the " + m["steps"][i]["v"])
        out.append(("Order", "X1", lex.fill(lex.X1, steps=lex.X1_SEP.join(names))))
        out.append(("Result", "CORE", lex.fill(lex.F_RESULT_X1, res=res, base=m["base"])))
    else:
        for st in m["steps"]:
            op = st["op"]
            if op == "disc":
                out.append(("Discount", "R8", lex.fill(lex.F_DISC, res=st["out"], base=st["in"], pct=st["v"]) + " " + lex.R8))
            elif op == "disc2":
                out.append(("Discounts", "X5", lex.fill(lex.F_DISC2, res=st["out"], base=st["in"], pct1=st["v"][0],
                                                        pct2=st["v"][1]) + " " + lex.X5[sem["X5"]]))
            elif op == "fee":
                t = lex.fill(lex.F_FEE, fee=st["fee"], pct=st["v"], base=st["in"])
                if m["target"] != "fee":
                    t += " " + lex.fill(lex.F_FEE_TOT, tot=st["out"], base=st["in"], fee=st["fee"])
                out.append(("Fee", "CORE", t))
            elif op == "pctof":
                out.append(("Fee", "CORE", lex.fill(lex.F_PCTOF, res=st["out"], pct=st["v"], base=st["in"])))
            elif op == "cap":
                per = "line" if sem["X4"][st["id"]] == "line" else "claim"
                out.append(("Cap", "X4", lex.fill(lex.F_CAP, res=st["out"], base=st["in"], cap=st["v"]) + " " +
                            lex.fill(lex.X4_CAP, cap=st["v"], per=per)))
            elif op == "min":
                per = "line" if sem["X4"][st["id"]] == "line" else "claim"
                out.append(("Minimum", "X4", lex.fill(lex.F_MIN, res=st["out"], base=st["in"], min=st["v"]) + " " +
                            lex.fill(lex.X4_MIN, min=st["v"], per=per)))
            elif op == "add":
                out.append(("Charges", "CORE", lex.fill(lex.F_ADD, tot=st["out"], fixed=st["v"], base=st["in"])))
            elif op == "ded":
                out.append(("Deductions", "U5", lex.U5 + " " + lex.fill(lex.F_DED, res=st["out"], gross=st["in"],
                                                                       lines=join_labels(st["v"]))))
            elif op == "floor0":
                if "X8" in shown:
                    # repair r2 (G5 wording flag): no "owed owed" when the result name already ends in "owed"
                    x8 = lex.X8.replace("{res} owed", "{res}") if str(res).strip().lower().endswith("owed") else lex.X8
                    out.append(("Floor", "X8", lex.fill(x8, res=res)))
            elif op == "incfee":
                out.append(("Listed prices", "X7", lex.fill(lex.X7[sem["X7"]], fee=st["fee"], listed=st["in"],
                                                            pct=st["v"])))
    for e in m["excs"]:
        form = sem["X2"][str(e["no"])]
        if e["kind"] in ("rate", "pct"):
            eff = lex.fill(lex.X2["rate"][form], n=e["no"], erate=e["v"], grate=e["on"])
        else:
            eff = lex.fill(lex.X2["add"][form], n=e["no"], echarge=e["v"], gcharge=e["on"])
        out.append((f"Exception {e['no']}", "GATE", gate_text(e, sem.get("ORJ", {}).get(str(e["no"]), e["join"]))
                    + " " + eff))
    if "X3" in sem:
        f = sem["X3"]
        if f == "fold":
            f = "fold_rate" if {e["kind"] for e in m["excs"]} <= {"rate", "pct"} else "fold_charge"
        out.append(("Several exceptions", "X3", lex.fill(lex.X3[f], res=res) if "{res}" in lex.X3[f] else lex.X3[f]))
    if "R5" in sem and "R5" in shown:
        ln = [l for l in m["lines"] if l["p"] == "mul"][0]
        t = lex.R5[sem["R5"]]
        kw = {k: v for k, v in (("unit", m["qsg"]), ("units", m["qpl"])) if "{" + k + "}" in t}
        out.append(("Partial units", "R5", lex.fill(t, **kw)))
    if "U3" in sem and "U3" in shown:
        out.append(("Partial blocks", "U3", lex.fill(lex.U3[sem["U3"]], k=num_str(m["k"]), units=m["qpl"])))
    if "R1" in sem and "R1" in shown:
        out.append(("Rounding", "R1", lex.fill(lex.R1[sem["R1"]], res=m["round_what"], u=unit_phrase(card, sem["R1u"]))))
        if "R2" in sem:
            out.append(("Rounding stage", "R2", lex.fill(lex.R2["final"], res=res) if sem["R2"] == "final" else lex.R2["line"]))
        if "R3" in sem:
            out.append(("Comparisons", "R3", lex.fill(lex.R3[sem["R3"]], res=m["round_what"])))
        out.append(("Other rounding", "R4", lex.R4))
    if card.get("op_item"):
        out.append(("Owed", "OP", lex.fill(lex.OP_MONEY, item=card["op_item"])))
    if card["schema"] == "CH-O":
        out.append(("Bands", "B1", lex.B1_SENT[sem.get("B1o", card["b1"])]))
    return out


def outcome_items(card, names, b1):
    outs = card["outs"]
    items = []
    for i, o in enumerate(outs):
        pos = "low" if i == 0 else "high" if i == len(outs) - 1 else "mid"
        kw = {k: mstr(o[k], card) for k in ("lo", "hi") if o.get(k) is not None}
        items.append(lex.fill(lex.OUT_ITEM, name=names[i], range=lex.fill(lex.OUT_RANGE[b1][pos], **kw)))
    return items


# ----------------------------------------------------------------------------------------------------------------- values

def kinds(card):
    """label -> value kind for every document value the card's rules read."""
    m = card["m"]
    k = {}
    for ln in m["lines"]:
        if ln["p"] in ("mul", "perk"):
            k[ln["q"]] = "qty"
            k[ln["r"]] = "money"
        else:
            k[ln["a"]] = "money"
    for st in m["steps"]:
        vs = st["v"] if isinstance(st.get("v"), list) else [st.get("v")]
        for v in vs:
            if v is not None:
                k[v] = "pct" if st["op"] in ("disc", "disc2", "fee", "pctof", "incfee") else "money"
    for e in m["excs"]:
        k[e["v"]] = k.get(e["on"], "money")
        for c in e["conds"]:
            k[c["f"]] = "count" if c["ftype"] == "count" else "fact"
    return k


def value_text(card, v, kind):
    if kind == "money":
        return mstr(v, card)
    if kind == "pct":
        return pct_str(D(v))
    if kind == "qty":
        x = D(v)
        return f"{num_str(x)} {card['m']['qsg'] if x == 1 else card['m']['qpl']}"
    return str(v)


def _grid(rng, lo, hi, step):
    lo, hi, step = D(str(lo)), D(str(hi)), D(str(step))
    return lo + step * rng.randint(0, int((hi - lo) / step))


def draw(card, rng):
    """One row's values (vals: Decimal by label) and facts (str by label)."""
    m = card["m"]
    dec2 = m["dec2"]
    vals, facts = {}, {}
    exact = "R1" in card.get("omitted", []) or ("R1" not in m["sem"] and rng.random() < 0.0)

    def money_(lo, hi):
        lo, hi = int(math.ceil(float(lo))), int(math.floor(float(hi)))
        if hi <= lo:
            hi = lo + 1
        if dec2:
            return _grid(rng, lo, hi, rng.choice(["0.05", "0.25", "0.01", "0.5", "1"]))
        return _grid(rng, lo, hi, 1)

    for ln in m["lines"]:
        if ln["p"] == "mul":
            if m["partial"] and rng.random() < 0.6:
                vals[ln["q"]] = _grid(rng, 1, 30, rng.choice(["0.25", "0.5"]))
            else:
                vals[ln["q"]] = D(rng.randint(1, 40))
            vals[ln["r"]] = money_(8, 140)
        elif ln["p"] == "perk":
            vals[ln["q"]] = D(rng.randint(1, int(ln["k"] * 10)))
            vals[ln["r"]] = money_(4, 90)
        else:
            if exact:
                vals[ln["a"]] = D(rng.randint(40, 3000)) if dec2 else D(rng.randint(1, 30) * 100)
            else:
                vals[ln["a"]] = money_(40, 3000)
    for st in m["steps"]:
        op = st["op"]
        if op in ("fee", "pctof", "incfee"):
            vals[st["v"]] = _grid(rng, 1, 22, "1" if exact else rng.choice(["0.5", "0.25", "1"]))
        elif op == "disc":
            vals[st["v"]] = _grid(rng, 2, 40, "1" if exact else rng.choice(["0.5", "1", "2.5"]))
        elif op == "disc2":
            for k in st["v"]:
                vals[k] = _grid(rng, 2, 25, "1" if exact else rng.choice(["0.5", "1"]))
        elif op == "add":
            vals[st["v"]] = money_(5, 160)
        elif op in ("cap", "min"):
            vals[st["v"]] = money_(20, 2500)
        elif op == "ded":
            for k in st["v"]:
                vals[k] = money_(10, 2000)
    for e in m["excs"]:
        if e["kind"] == "rate":
            b = float(vals[e["on"]])
            v = money_(max(5, b * 0.5), max(10, b * 1.8))
            if v == vals[e["on"]]:
                v = v + (D("0.5") if dec2 else ONE)
            vals[e["v"]] = v
        elif e["kind"] == "pct":
            v = _grid(rng, 1, 35, "1" if exact else rng.choice(["0.5", "1"]))
            if v == vals[e["on"]]:
                v += 1
            vals[e["v"]] = v
        else:
            vals[e["v"]] = money_(5, 260)
        for c in e["conds"]:
            if c["ftype"] == "flag":
                facts.setdefault(c["f"], rng.choice(["yes", "no"]))
            elif c["ftype"] == "cat":
                facts.setdefault(c["f"], rng.choice(c["dom"]))
            else:
                lo, hi = c["rng"]
                facts.setdefault(c["f"], str(rng.randint(lo, hi)))
    return vals, facts


def make_lp(card, vals, facts, q, sem):
    m = card["m"]
    lines = [{k: ln[k] for k in ("p", "q", "r", "a", "k") if ln.get(k) is not None} for ln in m["lines"]]
    steps = [{k: s[k] for k in ("op", "id", "v", "scope", "lim") if s.get(k) is not None} for s in m["steps"]]
    for s_ in steps:
        if s_["op"] in ("cap", "min") and "X4" in sem and s_["id"] in sem["X4"]:
            s_["scope"] = sem["X4"][s_["id"]]
    excs = []
    for e in m["excs"]:
        d = {k: e[k] for k in ("no", "conn", "kind", "v", "on")}
        d["join"] = sem.get("ORJ", {}).get(str(e["no"]), e["join"])
        d["conds"] = [{"f": c["f"], "op": c["op"], "v": c["v"]} for c in e["conds"]]
        excs.append(d)
    s2 = {k: v for k, v in sem.items() if k not in ("ORJ", "B1o")}
    om = set(card.get("omitted", []))
    if "R1" in om:
        for k in ("R1", "R1u", "R2", "R3"):
            s2.pop(k, None)
    for d in ("R5", "U3", "X8"):
        if d in om:
            s2.pop(d, None)
    if "X8" in om:
        steps = [s for s in steps if s["op"] != "floor0"]
    LP = {"eng": "money", "world": card["world"], "unit": m["unit"], "vals": dict(vals), "facts": dict(facts),
          "lines": lines, "steps": steps, "excs": excs, "sem": s2, "target": m["target"], "q": q}
    if card["world"] == "open":
        LP["cats"] = {c["f"]: list(c["dom"]) for e in m["excs"] for c in e["conds"] if c["ftype"] == "cat"}
    return LP


# ----------------------------------------------------------------------------------------------------------------- readings

def alt_readings(LP, shown):
    """[(E-alt id, rd)] for every listed alternative of every shown SEM dimension (R2-16)."""
    sem = LP["sem"]
    out = []
    if "R1" in sem and "R1" in shown:
        for mode in ("half_up", "half_even", "floor", "ceiling"):
            if mode != sem["R1"] and not (mode == "half_even" and D(sem["R1u"]) > ONE):
                out.append((f"E-alt:R1:{mode}", {"sem": {"R1": mode}}))
        if "R2" in sem:
            out.append(("E-alt:R2", {"sem": {"R2": "line" if sem["R2"] == "final" else "final"}}))
        out.append(("E-alt:R4:display", {"sem": {"R4alt": "display"}}))
        out.append(("E-alt:R4:r1", {"sem": {"R4alt": "r1"}}))
    if "R5" in sem and "R5" in shown:
        for mode in ("ceil", "floor", "exact"):
            if mode != sem["R5"]:
                out.append((f"E-alt:R5:{mode}", {"sem": {"R5": mode}}))
    if "U3" in sem and "U3" in shown:
        for mode in ("pro_rata", "full_k", "blocks"):
            if mode != sem["U3"]:
                out.append((f"E-alt:U3:{mode}", {"sem": {"U3": mode}}))
    if "X4" in sem and len(LP["lines"]) > 1:
        for sid, sc in sem["X4"].items():
            out.append((f"E-alt:X4:{sid}", {"sem": {"X4": {**sem["X4"], sid: "line" if sc == "total" else "total"}}}))
    for dim, a, b in (("X5", "succ", "added"), ("X6", "after", "before"), ("X7", "include", "before")):
        if dim in sem:
            out.append((f"E-alt:{dim}", {"sem": {dim: b if sem[dim] == a else a}}))
    if "X8" in sem and "X8" in shown:
        out.append(("E-alt:X8", {"sem": {"X8": "none"}}))
    if "X1" in sem:
        for perm in itertools.permutations(range(len(sem["X1"]))):
            if list(perm) != list(sem["X1"]):
                out.append((f"E-alt:X1:{''.join(map(str, perm))}", {"sem": {"X1": list(perm)}}))
    if "X2" in sem:
        for no, form in sem["X2"].items():
            out.append((f"E-alt:X2:{no}", {"sem": {"X2": {**sem["X2"], no: "add" if form == "replace" else "replace"}}}))
    if "X3" in sem:
        for f in ("alone_lower", "alone_higher", "fold"):
            if f != sem["X3"]:
                out.append((f"E-alt:X3:{f}", {"sem": {"X3": f}}))
    for e in LP.get("excs", []):
        if e["join"] in ("or1", "or2") and e["conn"] in ("O2", "UN1"):
            out.append((f"E-alt:OR:{e['no']}", {"oralt": {e["no"]: True}}))
        for ci, c in enumerate(e["conds"]):
            if c["op"] in ("ge", "gt", "le", "lt"):
                out.append((f"E-alt:CMP:{e['no']}.{ci}",
                            {"cmpalt": {(e["no"], ci): {"ge": "gt", "gt": "ge", "le": "lt", "lt": "le"}[c["op"]]}}))
    return out


def error_readings(LP):
    out = []
    ops = {s["op"] for s in LP["steps"]}
    if "cap" in ops:
        out.append(("E-cap", {"err": "E-cap"}))
    if "min" in ops:
        out.append(("E-floor", {"err": "E-floor"}))
    for e in LP.get("excs", []):
        out.append((f"E-exc:{e['no']}", {"err": f"E-exc:{e['no']}"}))
        if e["conn"] == "UN1":
            out.append((f"E-unless:{e['no']}", {"err": f"E-unless:{e['no']}"}))
    return out


def hooks(LP, shown, gold):
    """{value: [hook ids]} for every hook value on the display grid, gold excluded (3.4), E-capval and E-copy
    included."""
    unit = D(LP["unit"])
    got = {}

    def put(v, eid):
        if v is None or v < 0 or not on_grid(v, unit) or v == gold:
            return
        got.setdefault(v, []).append(eid)

    for eid, rd in alt_readings(LP, shown) + error_readings(LP):
        try:
            v, _ = money.evaluate(LP, rd)
        except (Reject, money.Unknown, ArithmeticError, ValueError):
            continue
        put(v, eid)
    vals = {k: D(v) for k, v in LP["vals"].items()}
    _, tr0 = money.evaluate(LP, {})
    for s in LP["steps"]:
        if s["op"] == "cap" and "bind:cap" not in tr0.flags:
            put(vals[s["v"]], "E-capval")
        if s["op"] == "min" and "bind:floor" not in tr0.flags:
            put(vals[s["v"]], "E-capval")
    for ln in LP["lines"]:
        if ln["p"] == "stated":
            put(vals[ln["a"]], "E-copy")
    return got


def flags_and_tags(LP, gold_val, shown):
    """has: / bind: / dec: adjustment tags (3.8) for a money row, computed with A."""
    v0, tr = money.evaluate(LP, {})
    tags = set()
    ops = {s["op"] for s in LP["steps"]}
    has = []
    if "cap" in ops:
        has.append(("cap", {"err": "E-cap"}))
    if "min" in ops:
        has.append(("floor", {"err": "E-floor"}))
    if LP.get("excs"):
        has.append(("exc", {"excl": {e["no"] for e in LP["excs"]}}))
    if "R1" in LP["sem"]:
        has.append(("round", {"norround": True}))
    if "R5" in LP["sem"] or "U3" in LP["sem"]:
        alt = {"sem": {"R5": "exact"}} if "R5" in LP["sem"] else {"sem": {"U3": "pro_rata"}}
        has.append(("partial", alt))
    return has
