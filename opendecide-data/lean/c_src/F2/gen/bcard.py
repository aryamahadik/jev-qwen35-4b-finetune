"""S3 tiered rate tables: card skeleton, clauses, row values (band table, placement), LP, readings, hooks, document."""
from __future__ import annotations

import copy
import math
from decimal import Decimal

from . import bandeval as BE, lex, options as O, qtext
from .common import D, ONE, ZERO, HUNDRED, on_grid, quant, money_str, num_str, pct_str
from .money import Reject, Tr

CHARGE_NAMES = ["tariff charge", "usage charge", "band charge", "levy due", "service charge"]
AMT_MONEY = ["shipment value", "turnover reported", "order value", "insured value", "contract sum"]
AMT_COUNT = ["units used", "items processed", "loads hauled", "pages scanned", "parcels sent"]
BAND_NAMES = [["Starter", "Standard", "Plus", "Premium", "Elite", "Summit", "Apex", "Crown"],
              ["Tier one", "Tier two", "Tier three", "Tier four", "Tier five", "Tier six", "Tier seven", "Tier eight"],
              ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Titanium", "Iridium", "Osmium"]]


def build(card, pack, rng):
    from .mcard import Labels
    L = Labels()
    s = {}
    s["dec2"] = card.setdefault("dec2", rng.random() < 0.5)
    s["unit"] = D("0.01") if s["dec2"] else ONE
    s["cur"] = pack["currency"]
    rk = card.get("rate_kind") or rng.choice(["pct", "pct", "unit", "flat"])
    if card["world"] == "open":
        rk = rng.choice(["pct", "unit"])
    s["rate_kind"] = rk
    b2 = card.get("b2") or ("marginal" if (rk != "flat" and rng.random() < 0.3 and card["world"] == "closed"
                                          and card["schema"] != "CL") else "flat")
    s["count"] = rk == "unit" or (rk == "flat" and rng.random() < 0.4)
    if card.get("computed") is not None and card["schema"] != "CH-B" and rk != "flat":
        computed = bool(card["computed"])    # sweep cards only (v1.1): a stated banding amount for level 1
    else:
        computed = card["schema"] in ("CH-B",) or rk == "flat" or (b2 == "flat" and rng.random() < 0.6)
    s["computed"] = computed
    if s["count"]:
        nm = rng.choice(AMT_COUNT)
        s["amt"] = L(nm)
        s["usg"], s["upl"] = (nm.split()[0][:-1] if nm.split()[0].endswith("s") else nm.split()[0]), nm.split()[0]
    else:
        s["amt"] = L(rng.choice(AMT_MONEY))
    if computed:
        if s["count"]:
            s["q"], s["p"] = L(rng.choice(["batches", "pallets", "shifts", "trips"])), L(rng.choice(["units per batch", "items per pallet", "loads per shift", "parcels per trip"]))
        else:
            s["q"], s["p"] = L(rng.choice(["quantity ordered", "items supplied", "hours booked"])), L(rng.choice(["unit price", "price per item", "hourly price"]))
    s["charge"] = L(rng.choice(CHARGE_NAMES))
    s["names"] = rng.choice(BAND_NAMES)
    s["fee"] = L(rng.choice(["booking fee", "admin fee", "handling fee"])) if (card.get("fee") or (card.get("fee") is None and card["schema"] not in ("CH-B", "CL") and rk != "flat" and rng.random() < 0.4)) else None
    if s["fee"]:
        s["withfee"] = L(rng.choice(["charge with fee", "total before limits"]))
    s["minmax"] = card.get("minmax") or (rng.choice([None, None, "min", "cap"]) if card["schema"] != "CH-B" else None)
    if s["minmax"] or s["fee"]:
        s["final"] = L(rng.choice(["amount billed", "total levy", "charge billed"]))
    if s["minmax"]:
        s["lim"] = L({"min": rng.choice(["minimum charge", "floor charge"]), "cap": rng.choice(["maximum charge", "charge ceiling"])}[s["minmax"]])
    elif not s["fee"]:
        # repair r1.1 (G5 flag, confirmed): v1.0 overwrote the fee step's output name with the charge's own name on
        # cards with a fee and no limit ("The X adds the fee to the X")
        s["final"] = s["charge"]
    if b2 == "flat" and (card["world"] == "open" or rng.random() < 0.35) and card["schema"] != "CH-B":
        cname, cvals = pack["cat"]
        cvals = [v for v in cvals if " and " not in v and " or " not in v][:5]
        s["x10"] = {"f": L(cname), "v": rng.choice(cvals), "dom": cvals}
    else:
        s["x10"] = None
    sem = {"B1": card.get("b1") or rng.choice(["upper", "lower"]), "B2": b2}
    if s["count"] and b2 == "marginal":
        sem["B1"] = "upper"           # R3-05: marginal tables over whole-unit counts are upper-inclusive
    rnd = rk == "pct" or (rk == "unit" and s["dec2"])
    if rnd:
        sem["R1"] = card.get("r1") or rng.choice(["half_up", "half_even", "floor", "ceiling"])
        sem["R1u"] = s["unit"]
        if card["schema"] in ("YN-T", "CL"):
            sem["R3"] = "rounded"
    if s["minmax"]:
        sem["X4"] = {s["minmax"]: "total"}
    s["sem"] = sem
    s["nb"] = card.get("nb") or rng.randint(3, 8)
    card["b"] = s
    card["shown"] = set(k for k in sem if k != "R1u") | ({"R4"} if "R1" in sem else set())
    card["omitted"] = []
    return card


def clauses(card, sem, shown, world):
    s = card["b"]
    out = [("Scope", "W0", lex.W0)]
    if world == "closed":
        out.append(("Record", "W1", lex.W1))
    else:
        out.append(("Record", "W2", lex.fill(lex.W2, u=unit_phrase(card), nei=card["nei"])))
        if s["x10"]:
            out.append(("Categories", "CATLIST", lex.fill(lex.CATLIST, f=s["x10"]["f"], list=", ".join(s["x10"]["dom"]))))
    if s["computed"]:
        out.append(("Amount", "CORE", lex.fill(lex.F_MUL, lc=s["amt"], q=s["q"], r=s["p"])))
    out.append(("Band table", "BT", lex.BT_INTRO))
    out.append(("Bands", "B1", lex.B1_SENT[sem["B1"]]))
    out.append(("Band mode", "B2", lex.fill(lex.B2[sem["B2"]], amt=s["amt"])))
    rk = s["rate_kind"]
    kw = {"amt": s["amt"]}
    if rk == "unit":
        kw["unit"] = s["usg"]
    if rk == "flat":
        kw = {"charge": s["charge"]}
    out.append(("Rates", "RATE", lex.fill(lex.RATE_KIND[rk], **kw)))
    out.append(("Charge", "CORE", lex.fill(lex.BAND_CHARGE, charge=s["charge"], amt=s["amt"])))
    if s["x10"]:
        out.append(("Category rule", "X10", lex.fill(lex.X10, f=s["x10"]["f"], v=s["x10"]["v"], item=card["ent_sg"],
                                                     amt=s["amt"])))
    pre = s["charge"]
    if s["fee"]:
        nm = s["withfee"] if s["minmax"] else s["final"]
        out.append(("Fee", "CORE", lex.fill(lex.F_ADD, tot=nm, fixed=s["fee"], base=s["charge"])))
        pre = nm
    if s["minmax"] == "min":
        out.append(("Minimum", "X4", lex.fill(lex.F_MIN, res=s["final"], base=pre, min=s["lim"]) + " " +
                    lex.fill(lex.X4_MIN, min=s["lim"], per="claim")))
    elif s["minmax"] == "cap":
        out.append(("Cap", "X4", lex.fill(lex.F_CAP, res=s["final"], base=pre, cap=s["lim"]) + " " +
                    lex.fill(lex.X4_CAP, cap=s["lim"], per="claim")))
    if "R1" in sem and "R1" in shown:
        out.append(("Rounding", "R1", lex.fill(lex.R1[sem["R1"]], res=s["final"], u=unit_phrase(card, sem["R1u"]))))
        if "R3" in sem:
            out.append(("Comparisons", "R3", lex.fill(lex.R3[sem["R3"]], res=s["final"])))
        out.append(("Other rounding", "R4", lex.R4))
    return out


def unit_phrase(card, u=None):
    s = card["b"]
    u = D(u if u is not None else s["unit"])
    return (money_str(u, True) if u < 1 else num_str(u)) + " " + s["cur"]


def mstr(v, card):
    return money_str(D(v), card["b"]["dec2"]) + " " + card["b"]["cur"]


def amt_text(v, card):
    return mstr(v, card) if not card["b"]["count"] else num_str(D(v))


# ----------------------------------------------------------------------------------------------------------------- tables and values

def draw_table(card, rng, nb=None):
    s = card["b"]
    nb = nb or (rng.randint(10, 13) if rng.random() < 0.08 else s["nb"])
    if s["count"]:
        step = D(rng.choice([5, 10, 20, 25]))
        e0 = step * rng.randint(1, 4)
    else:
        step = D(rng.choice([50, 100, 250, 500]))
        e0 = step * rng.randint(1, 4)
    edges = [e0]
    for i in range(nb - 2):
        edges.append(edges[-1] + step * rng.randint(1, 4))
    rk = s["rate_kind"]
    rates = []
    falling = s["sem"]["B2"] == "flat" and rk != "flat" and rng.random() < 0.15
    for i in range(nb):
        if rk == "pct":
            r = D(rng.choice(["0.5", "1", "1.5", "2", "2.5", "3", "4", "5", "6", "7.5", "8", "10", "12"]))
        elif rk == "unit":
            r = D(rng.randint(1, 40)) * (D("0.05") if s["dec2"] else ONE) + (D(1) if not s["dec2"] else ZERO)
        else:
            r = D(rng.randint(2, 60)) * (D(5) if not s["dec2"] else D("2.5"))
        rates.append(r)
    rates = sorted(set(rates), reverse=falling)
    while len(rates) < nb:
        rates.append(rates[-1] + (D(1) if not falling else ZERO))
        rates = sorted(set(rates), reverse=falling)
        if len(rates) < nb and falling:
            rates.append(max(rates) + 1)
            rates = sorted(set(rates), reverse=True)
    rates = rates[:nb]
    names = list(card["band_disp"][:nb]) if len(card["band_disp"]) >= nb else [f"{s['names'][0]} {i + 1}" for i in range(nb)]
    bands = []
    for i in range(nb):
        bands.append({"name": names[i], "lo": edges[i - 1] if i > 0 else None, "hi": edges[i] if i < nb - 1 else None,
                      "rate": rates[i]})
    return bands, falling


def solve_qp(target, card, rng):
    """q x p == target exactly, q whole in 1..60, p on the price grid inside a sane range."""
    s = card["b"]
    unit = ONE if s["count"] else s["unit"]
    cands = list(range(1, 61))
    rng.shuffle(cands)
    for q in cands:
        p = target / q
        if on_grid(p, unit) and p > 0 and (p >= 1 or s["count"]):
            return D(q), p
    return None


def draw(card, rng, want_band=None, place=None):
    """Values for one row: band table, banding amount (placed in a target band / on an edge), facts, limit."""
    s = card["b"]
    bands, falling = draw_table(card, rng)
    nb = len(bands)
    tb = want_band if want_band is not None else rng.randrange(nb)
    tb = min(tb, nb - 1)
    b = bands[tb]
    unit = ONE if s["count"] else s["unit"]
    lo = D(b["lo"]) if b.get("lo") is not None else None
    hi = D(b["hi"]) if b.get("hi") is not None else None
    b1 = s["sem"]["B1"]
    if place == "edge":
        cand_e = [x for x in (lo, hi) if x is not None]
        e = rng.choice(cand_e)
        v = e
    elif place in ("below", "above"):
        cand_e = [x for x in (lo, hi) if x is not None]
        e = rng.choice(cand_e)
        v = e - unit if place == "below" else e + unit
    else:
        a = lo if lo is not None else (D(1) if s["count"] else unit * 100)
        z = hi if hi is not None else (a * 2 + (D(50) if s["count"] else D(1000)))
        if z <= a:
            z = a + 10
        span = int((z - a) / unit)
        v = a + unit * rng.randint(1, max(1, span - 1))
    if v <= 0:
        raise Reject("amount <= 0")
    vals, facts = {}, {}
    if s["computed"]:
        qp = solve_qp(v, card, rng)
        if qp is None:
            raise Reject("no q x p")
        vals[s["q"]], vals[s["p"]] = qp
    else:
        vals[s["amt"]] = v
    for i, bb in enumerate(bands):
        pass
    if s["x10"]:
        facts[s["x10"]["f"]] = rng.choice(s["x10"]["dom"])
    if s["minmax"]:
        vals[s["lim"]] = D(rng.randint(5, 400)) * (D(5) if not s["dec2"] else D("2.5"))
    if s["fee"]:
        vals[s["fee"]] = D(rng.randint(2, 60)) * (D(5) if not s["dec2"] else D("1.25"))
    return {"bands": bands, "vals": vals, "facts": facts, "falling": falling, "tb": tb, "amount": v}


def make_lp(card, d, q, sem):
    s = card["b"]
    LP = {"eng": "band", "world": card["world"], "unit": s["unit"],
          "amt": {"kind": "mul", "q": s["q"], "p": s["p"]} if s["computed"] else {"kind": "stated", "a": s["amt"]},
          "bands": [dict(b) for b in d["bands"]], "rate_kind": s["rate_kind"], "vals": dict(d["vals"]),
          "facts": dict(d["facts"]), "sem": {k: v for k, v in sem.items()},
          "steps": ([{"op": s["minmax"], "id": s["minmax"], "v": s["lim"], "scope": "total"}] if s["minmax"] else []),
          "x10": ({"f": s["x10"]["f"], "v": s["x10"]["v"]} if s["x10"] else None), "q": q, "fee": s["fee"],
          "count": s["count"], "_amt_label": s["amt"]}
    if card["world"] == "open" and s["x10"]:
        LP["cats"] = {s["x10"]["f"]: list(s["x10"]["dom"])}
    return LP


def alt_readings(LP, shown):
    sem = LP["sem"]
    out = [("E-tier-", {"err": "E-tier-"}), ("E-tier+", {"err": "E-tier+"})]
    out.append(("E-alt:B1", {"sem": {"B1": "lower" if sem.get("B1") == "upper" else "upper"}}))
    if LP["rate_kind"] != "flat" and not (LP.get("count") and sem.get("B2") == "flat"):
        out.append(("E-alt:B2", {"sem": {"B2": "marginal" if sem.get("B2") == "flat" else "flat"}}))
    if "R1" in sem:
        for mode in ("half_up", "half_even", "floor", "ceiling"):
            if mode != sem["R1"]:
                out.append((f"E-alt:R1:{mode}", {"sem": {"R1": mode}}))
    if LP.get("x10"):
        out.append(("E-exc", {"err": "E-exc"}))
    for st in LP.get("steps", []):
        out.append(("E-cap" if st["op"] == "cap" else "E-floor", {"err": "E-cap" if st["op"] == "cap" else "E-floor"}))
    return out


def hooks(LP, shown, gold):
    unit = D(LP["unit"])
    got = {}

    def put(v, eid):
        if v is None or v < 0 or not on_grid(v, unit) or v == gold:
            return
        got.setdefault(v, []).append(eid)
    for eid, rd in alt_readings(LP, shown):
        try:
            v, _ = BE.evaluate(LP, rd)
        except (Reject, ArithmeticError, ValueError):
            continue
        put(v, eid)
    _, tr0 = BE.evaluate(LP, {})
    for st in LP.get("steps", []):
        if (st["op"] == "cap" and "bind:cap" not in tr0.flags) or (st["op"] == "min" and "bind:floor" not in tr0.flags):
            put(D(LP["vals"][st["v"]]), "E-capval")
    if LP["amt"]["kind"] == "stated" and not LP.get("count"):
        put(D(LP["vals"][LP["amt"]["a"]]), "E-copy")
    return got


def band_hooks(LP, shown, gold_name):
    """Bands reached by hook readings of the banding amount's band (CH-B): E-tier neighbours, E-alt:B1 on edges."""
    names = [b["name"] for b in LP["bands"]]
    gi = names.index(gold_name)
    reach = {}
    sem = LP["sem"]
    try:
        n2 = BE.band_of(LP, {"sem": {"B1": "lower" if sem["B1"] == "upper" else "upper"}})
        if n2 != gold_name:
            reach.setdefault(n2, set()).add("E-alt:B1")
    except Reject:
        pass
    if LP["amt"]["kind"] == "mul":
        for k, eid in ((LP["amt"]["q"], "E-copy:q"), (LP["amt"]["p"], "E-copy:p")):
            v = D(LP["vals"][k])
            try:
                n2 = LP["bands"][BE.locate(v, LP["bands"], sem["B1"])]["name"]
                if n2 != gold_name:
                    reach.setdefault(n2, set()).add(eid)
            except Reject:
                pass
    for j, eid in ((gi - 1, "E-tier-"), (gi + 1, "E-tier+")):
        if 0 <= j < len(names) and names[j] not in reach:
            reach[names[j]] = {eid}
    return {n: sorted(ids)[0] for n, ids in reach.items() if len(ids) == 1}


def doc_ir(card, LP, eid, *, inert=None, attack=None, cases=None):
    s = card["b"]
    blocks = []
    rec = [(f"{card['ent_sg']} ID", eid)] if eid else []
    if s["x10"] and not cases:
        rec.append((s["x10"]["f"], str(LP["facts"][s["x10"]["f"]])))
    if s["computed"] and not cases:
        rec.append((s["q"], num_str(D(LP["vals"][s["q"]]))))
        rec.append((s["p"], amt_text(LP["vals"][s["p"]], card) if not s["count"] else num_str(D(LP["vals"][s["p"]]))))
    elif not cases:
        rec.append((s["amt"], amt_text(LP["vals"][s["amt"]], card)))
    for name, v in (LP.get("printed") or {}).items():
        if name == s["amt"] or name.endswith(" part"):
            rec.append((name, amt_text(v, card)))
        else:
            rec.append((name, mstr(v, card)))
    if inert:
        rec.append(inert)
    if s["minmax"]:
        rec.append((s["lim"], mstr(LP["vals"][s["lim"]], card)))
    if s["fee"]:
        rec.append((s["fee"], mstr(LP["vals"][s["fee"]], card)))
    from .render import BLANK
    rows = []
    for b in LP["bands"]:
        r = D(b["rate"])
        rt = pct_str(r) if s["rate_kind"] == "pct" else mstr(r, card)
        rows.append([b["name"], num_str(D(b["lo"])) if b.get("lo") is not None else BLANK,
                     num_str(D(b["hi"])) if b.get("hi") is not None else BLANK, rt])
    if cases:
        blocks.append(cases)
    if rec:
        blocks.append({"type": "fields", "label": card["rec_label"], "pairs": [list(p) for p in rec]})
    blocks.append({"type": "table", "caption": card["table_caption"], "columns": ["band", "lower edge", "upper edge", "rate"],
                   "rows": rows})
    if attack:
        blocks.append({"type": "para", "text": attack})
    doc = {"blocks": blocks}
    if card.get("doc_title"):
        doc["title"] = card["doc_title"]
    return doc
