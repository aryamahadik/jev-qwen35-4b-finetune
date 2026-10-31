"""gen_numeric_dates schemas, part 3: money, percentages, rounding, taxes, discounts, insurance, voting ratios."""
import datetime as dt
from decimal import Decimal, localcontext
from fractions import Fraction as Fr

import numpy as np

from nd_common import (V, MONTHS, PLACES, WEEKDAYS, D, Schema, Sty, add_days, cap, dec, drnd, fd, fdec, fdm, ft, ftrim,
                       iso, money, num_w, ordn, person, plural, rnd)

LAB = ["Situation: ", "Case: ", "", "Facts: "]
CURS = ["$", "$", "$", "€", "£", "CA$", "A$"]


def cents_round(x, mode="half_up"):
    """Fraction of cents -> int cents."""
    return int(rnd(Fr(x), 0, mode))


def dcents(x, mode="half_up"):
    """Decimal cents -> int cents (independent path)."""
    return int(drnd(x, 0, mode))


def mk_money(f):
    cur = f.get("cur", "$")
    return lambda c, whole=False: money(c, cur, whole)


# =============================================================================================================
class Discounts(Schema):
    """Coupon (maybe excluding sale items) then member discount, rounding to the cent, free-shipping threshold
    measured after discounts."""
    name = "discounts"
    quota = 650
    letter = True
    multi_hop = True
    ITEMS = ["running shoes", "rain jacket", "backpack", "water bottle", "desk lamp", "yoga mat", "headphones",
             "wool sweater", "coffee grinder", "board game", "phone case", "garden hose", "cookbook", "bath towels",
             "frying pan", "notebook set", "hiking socks", "bike light", "picture frame", "toolkit"]

    def sample(self, rng):
        k = rng.choice([2, 3, 3, 4])
        names = rng.sample(self.ITEMS, k)
        items = [[n, rng.randrange(599, 8999, 1) if rng.random() < 0.6 else rng.randrange(500, 9000, 100) - 1, rng.random() < 0.3]
                 for n in names]
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "cur": rng.choice(CURS),
             "items": items, "cp": rng.choice([10, 15, 20, 25, 30]), "excl": rng.random() < 0.6,
             "mp": rng.choice([0, 5, 10, 10]), "thr": rng.choice([5000, 7500, 10000, 12500, 15000]),
             "ship": rng.choice([499, 599, 795, 999, 1250])}
        # tune the last item's price so the merchandise total lands near the threshold
        target = f["thr"] + rng.choice([0, 0, -1, 1, -5, 5, -50, 60, -300, 400])
        lo, hi = 1, 60000
        while lo < hi:
            mid = (lo + hi) // 2
            items[-1][1] = mid
            if self.merch(f) >= target:
                hi = mid
            else:
                lo = mid + 1
        items[-1][1] = lo
        if not (100 <= lo <= 40000):
            return self.sample(rng)
        return f

    def merch(self, f):
        sub = sum(p for _, p, _ in f["items"])
        elig = sum(p for _, p, s in f["items"] if not (s and f["excl"]))
        after = sub - cents_round(Fr(elig * f["cp"], 100))
        return after - cents_round(Fr(after * f["mp"], 100))

    def merch2(self, f):
        sub = sum(Decimal(p) for _, p, _ in f["items"])
        elig = sum((Decimal(p) for _, p, s in f["items"] if not (s and f["excl"])), Decimal(0))
        after = sub - dcents(elig * Decimal(f["cp"]) / Decimal(100))
        return int(after - dcents(after * Decimal(f["mp"]) / Decimal(100)))

    def valid(self, f):
        return all(p > 0 for _, p, _ in f["items"]) and 0 <= f["cp"] < 100

    def preds(self, f):
        return {"free": self.merch(f) >= f["thr"]}

    def preds2(self, f):
        return {"free": not (self.merch2(f) < f["thr"])}

    preds_list = ("free",)

    def val(self, f):
        m = self.merch(f)
        return m + (0 if m >= f["thr"] else f["ship"])

    def val2(self, f):
        m = self.merch2(f)
        return m + (0 if m >= f["thr"] else f["ship"])

    def fmtv(self, f, v):
        return mk_money(f)(v)

    def wrongs(self, f):
        sub = sum(p for _, p, _ in f["items"])
        add = sub - cents_round(Fr(sub * (f["cp"] + f["mp"]), 100))            # added the percentages
        allc = sub - cents_round(Fr(sub * f["cp"], 100))
        allc -= cents_round(Fr(allc * f["mp"], 100))                              # coupon on sale items too
        m = self.merch(f)
        out = [add + (0 if add >= f["thr"] else f["ship"]), allc + (0 if allc >= f["thr"] else f["ship"]),
               m + f["ship"] if m >= f["thr"] else m, (m if sub >= f["thr"] else m + f["ship"]), add, allc]
        return out

    def alts(self, f):
        a = {"cp": [c for c in (10, 15, 20, 25, 30) if c != f["cp"]], "mp": [m for m in (0, 5, 10, 15) if m != f["mp"]],
             "excl": [not f["excl"]], "thr": [f["thr"] + d for d in (-2500, 2500, -500, 500)]}
        its = []
        for i, (n, p, s) in enumerate(f["items"]):
            for d in (-1, 1, -100, 100, -500, 500):
                if p + d > 0:
                    x = [list(t) for t in f["items"]]
                    x[i][1] = p + d
                    its.append(x)
            x = [list(t) for t in f["items"]]
            x[i][2] = not s
            its.append(x)
        a["items"] = its
        return a

    def edges(self, f, p):
        t = ["numeric"]
        if f["excl"] and any(s for _, _, s in f["items"]):
            t.append("exception")
        return t

    def render(self, f):
        st = Sty(f)
        M = mk_money(f)
        code = st.c("code", ["SAVE", "SPRING", "WELCOME", "EXTRA", "HELLO"]) + str(f["cp"])
        excl = (" Items already on sale are excluded from the coupon." if f["excl"] else " The coupon applies to all items, including sale items.")
        mem = (f"\n- Loyalty members then receive an additional {f['mp']}% off the order total after the coupon."
               if f["mp"] else "\n- There is currently no loyalty-member discount.")
        pol = (f"{f['org']} Outfitters - checkout rules\n- Coupon {code}: {f['cp']}% off eligible items.{excl}{mem}\n"
               f"- Each discount is calculated on the running total and rounded to the nearest cent (half a cent rounds up).\n"
               f"- Shipping costs {M(f['ship'])}, but is free when the merchandise total after all discounts is {M(f['thr'], True)} or more. Tax is added later and does not count toward the threshold.")
        lines = "\n".join(f"- {n}: {M(p)}{' (on sale)' if s else ''}" for n, p, s in f["items"])
        memb = " is a loyalty member and" if f["mp"] else ""
        scen = f"{f['who'][0]}{memb} has these items in the cart:\n{lines}\n{cap(f['who'][1])} {V(f['who'], 'enters')} coupon {code} at checkout."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Does {who}'s order qualify for free shipping?", f"Will {who} get free shipping on this order?"],
                    neg=[f"Will {who} have to pay for shipping?", f"Does {who}'s order fall short of the free-shipping threshold?"],
                    cpos="the order qualifies for free shipping", cneg="the order does not qualify for free shipping",
                    speakers=[("A friend who shops there told " + f["who"][2] + " that", "the friend"), ("The site's chat assistant said", "the chat assistant")])

    def letter_q(self, f):
        return [f"What will {f['who'][0]} pay before tax, including any shipping charge?"]


# =============================================================================================================
class VatExpense(Schema):
    """Expense limit stated net of VAT while receipts show VAT-inclusive totals."""
    name = "vat_expense"
    quota = 450
    letter = True

    def sample(self, rng):
        rate = rng.choice([20, 19, 21, 10, 15, 25])
        ppl = rng.choice([1, 1, 2, 3, 4])
        capc = rng.choice([2500, 3000, 3500, 4000, 5000, 6000])
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "cur": rng.choice(["€", "£", "€", "CHF", "kr"]),
             "rate": rate, "ppl": ppl, "cap": capc, "kind": rng.choice(["meal", "hotel", "taxi"])}
        lim = capc * ppl
        net_target = lim + rng.choice([0, 0, 1, -1, 2, -2, 50, -50, lim * rate // 100 // 2])
        f["gross"] = cents_round(Fr(net_target * (100 + rate), 100))
        return f

    def net(self, f):
        return cents_round(Fr(f["gross"] * 100, 100 + f["rate"]))

    def net2(self, f):
        with localcontext() as c:
            c.prec = 40
            return dcents(Decimal(f["gross"]) / (Decimal(100 + f["rate"]) / Decimal(100)))

    def valid(self, f):
        return f["gross"] > 0

    def preds(self, f):
        return {"ok": self.net(f) <= f["cap"] * f["ppl"]}

    def preds2(self, f):
        return {"ok": not (self.net2(f) > f["cap"] * f["ppl"])}

    def val(self, f):
        return self.net(f)

    def val2(self, f):
        return self.net2(f)

    def fmtv(self, f, v):
        return money(v, f["cur"])

    def wrongs(self, f):
        g = f["gross"]
        return [cents_round(Fr(g * (100 - f["rate"]), 100)), g, cents_round(Fr(g * f["rate"], 100 + f["rate"])),
                self.net(f) + 1, self.net(f) - 1]

    def alts(self, f):
        return {"gross": [f["gross"] + d for d in (-1, 1, -2, 2, -3, 3, -100, 100)], "ppl": [f["ppl"] + 1, f["ppl"] - 1] if f["ppl"] > 1 else [2],
                "cap": [f["cap"] - 500, f["cap"] + 500], "rate": [r for r in (10, 19, 20, 21, 25) if r != f["rate"]]}

    def edges(self, f, p):
        return ["numeric", "units"] if f["ppl"] == 1 else ["numeric", "units", "multi_hop"]

    def render(self, f):
        st = Sty(f)
        M = lambda c: money(c, f["cur"])
        what = {"meal": ("Business meals", "per person", "a business dinner"), "hotel": ("Hotel nights", "per room per night", "a hotel stay"),
                "taxi": ("Taxi journeys", "per passenger", "a shared taxi")}[f["kind"]]
        pol = (f"{f['org']} Group - expense policy (Europe)\n- {what[0]} are reimbursed up to {M(f['cap'])} {what[1]}, measured EXCLUDING VAT.\n"
               f"- Receipt totals include VAT at {f['rate']}%. To find the amount excluding VAT, divide the total by 1.{f['rate']:02d} and round to the nearest cent (half a cent rounds up).")
        pol += "\n- Anything above the limit is paid by the employee."
        units = {"meal": plural(f["ppl"], "person", "people"), "hotel": plural(f["ppl"], "room-night"), "taxi": plural(f["ppl"], "passenger")}[f["kind"]]
        scen = f"{f['who'][0]} submits a receipt for {what[2]} covering {f['ppl']} {units}. The receipt total, including VAT, is {M(f['gross'])}."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Is the whole receipt within the reimbursement limit?", f"Will {who} be reimbursed in full for this receipt?"],
                    neg=[f"Is this receipt over the reimbursement limit?", f"Will {who} have to pay part of this expense personally?"],
                    cpos="the receipt is within the limit", cneg="the receipt is over the limit",
                    speakers=[("The finance assistant told " + f["who"][2] + " that", "the finance assistant")])

    def letter_q(self, f):
        return ["What is the receipt amount excluding VAT?"]


# =============================================================================================================
class IncomeTax(Schema):
    """Marginal tax bands; is the amount set aside enough?"""
    name = "income_tax"
    quota = 450
    letter = True

    def sample(self, rng):
        a = rng.choice([10000, 12000, 12570, 15000])
        b = rng.choice([40000, 50000, 50270, 60000])
        r1, r2 = rng.choice([(10, 20), (20, 40), (15, 30), (12, 25), (18, 33)])
        inc = rng.randrange(a + 1000, b + 60000, 10) * 100
        f = {"who": person(rng), "sty": rng.randrange(10 ** 9), "cur": rng.choice(["$", "£", "$"]), "a": a * 100, "b": b * 100,
             "r1": r1, "r2": r2, "inc": inc, "ded": rng.choice([0, 0, 200000, 350000])}
        tax = self.tax(f)
        f["saved"] = max(0, tax + rng.choice([0, 0, -1, 1, -100, 100, -5000, 5000]))
        return f

    def tax(self, f):
        t = max(0, f["inc"] - f["ded"])
        x = Fr(0)
        if t > f["a"]:
            x += Fr(min(t, f["b"]) - f["a"]) * f["r1"] / 100
        if t > f["b"]:
            x += Fr(t - f["b"]) * f["r2"] / 100
        return cents_round(x)

    def tax2(self, f):
        t = max(0, f["inc"] - f["ded"])
        bands = [(f["a"], 0), (f["b"], f["r1"]), (10 ** 15, f["r2"])]
        prev, tot = 0, Decimal(0)
        for top, r in bands:
            part = max(0, min(t, top) - prev)
            tot += Decimal(part) * Decimal(r) / Decimal(100)
            prev = top
        return dcents(tot)

    def valid(self, f):
        return f["a"] < f["b"] and f["inc"] > 0

    def preds(self, f):
        return {"ok": f["saved"] >= self.tax(f)}

    def preds2(self, f):
        return {"ok": not (f["saved"] < self.tax2(f))}

    def val(self, f):
        return self.tax(f)

    def val2(self, f):
        return self.tax2(f)

    def fmtv(self, f, v):
        return money(v, f["cur"])

    def wrongs(self, f):
        t = max(0, f["inc"] - f["ded"])
        return [cents_round(Fr(t * f["r2"], 100)), cents_round(Fr((t - f["a"]) * f["r2"], 100)),
                self.tax(dict(f, ded=0)), cents_round(Fr((t - f["a"]) * f["r1"], 100)), self.tax(f) + 100]

    def alts(self, f):
        return {"saved": [f["saved"] + d for d in (-1, 1, -100, 100, -1000, 1000)], "inc": [f["inc"] + d for d in (-10000, 10000, -100000, 100000)],
                "ded": [d for d in (0, 200000, 350000) if d != f["ded"]], "r2": [f["r2"] + 1, f["r2"] - 1]}

    def edges(self, f, p):
        return ["numeric", "multi_hop"] + (["exception"] if f["ded"] else [])

    def render(self, f):
        st = Sty(f)
        M = lambda c, w=False: money(c, f["cur"], w)
        ded = (f"\n- A standard deduction of {M(f['ded'], True)} is subtracted from income before the bands are applied." if f["ded"] else "")
        pol = (f"{st.c('j', ['Province of Westmark', 'Territory of Norland', 'Republic of Ostreva', 'State of Kellan'])} - income tax bands (simplified)\n"
               f"- Taxable income up to {M(f['a'], True)}: 0%\n- The part above {M(f['a'], True)} up to {M(f['b'], True)}: {f['r1']}%\n- The part above {M(f['b'], True)}: {f['r2']}%{ded}\n"
               f"- Each rate applies only to the income inside its band. Round the total tax to the nearest cent (half a cent rounds up).")
        scen = f"{f['who'][0]}'s income for the year is {M(f['inc'])}, with no other deductions or credits. {cap(f['who'][1])} {V(f['who'], 'has')} set aside {M(f['saved'])} to pay the tax."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Is the amount {who} set aside enough to pay the tax?", f"Does {who}'s savings pot cover the whole tax bill?"],
                    neg=[f"Will {who} be short of money for the tax bill?", f"Is the amount {who} set aside less than the tax owed?"],
                    cpos=f"the amount set aside covers the tax", cneg=f"the amount set aside is not enough",
                    speakers=[("A coworker told " + f["who"][2] + " that", "the coworker"), ("An online calculator suggested that", "the calculator")])

    def letter_q(self, f):
        return [f"How much income tax does {f['who'][0]} owe?"]


# =============================================================================================================
class InsurancePayout(Schema):
    """Deductible, then coinsurance, capped by the out-of-pocket maximum."""
    name = "insurance_payout"
    quota = 500
    letter = True
    multi_hop = True
    hide_keys = {"ok": ["ded_left"]}

    def sample(self, rng):
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9),
             "ded": rng.choice([0, 25000, 50000, 100000, 150000]), "co": rng.choice([10, 20, 20, 30, 40]),
             "oop": rng.choice([150000, 300000, 450000, 600000]), "bill": rng.randrange(20000, 1200000, 100),
             "hsa": 0}
        f["ded_left"] = rng.choice([f["ded"], f["ded"] // 2, 0]) if f["ded"] else 0
        f["oop_left"] = rng.choice([f["oop"], f["oop"] // 2, rng.randrange(5000, f["oop"], 100)])
        sh = self.share(f)
        f["hsa"] = max(0, sh + rng.choice([0, 0, 1, -1, 100, -100, 5000, -5000]))
        return f

    def share(self, f):
        if f["ded_left"] is None:
            outs = {self.share(dict(f, ded_left=x)) for x in (0, f["ded"])}
            return outs.pop() if len(outs) == 1 else None
        b, dl = f["bill"], f["ded_left"]
        pay = min(b, dl) + Fr(max(0, b - dl) * f["co"], 100)
        return cents_round(min(pay, f["oop_left"]))

    def share2(self, f):
        if f["ded_left"] is None:
            outs = {self.share2(dict(f, ded_left=x)) for x in (0, f["ded"] // 2, f["ded"])}
            return outs.pop() if len(outs) == 1 else None
        b, dl = Decimal(f["bill"]), Decimal(f["ded_left"])
        d = b if b < dl else dl
        rest = b - d
        pay = d + rest * Decimal(f["co"]) / Decimal(100)
        if pay > Decimal(f["oop_left"]):
            pay = Decimal(f["oop_left"])
        return dcents(pay)

    def valid(self, f):
        return (f["ded_left"] is None or f["ded_left"] <= f["ded"]) and f["oop_left"] <= f["oop"] and f["bill"] > 0

    def preds(self, f):
        if f["ded_left"] is None:
            outs = {f["hsa"] >= self.share(dict(f, ded_left=x)) for x in range(0, f["ded"] + 1, 100)}
            return {"ok": outs.pop() if len(outs) == 1 else None}
        return {"ok": f["hsa"] >= self.share(f)}

    def preds2(self, f):
        if f["ded_left"] is None:  # the share is monotone in the unmet deductible: check both extremes
            outs = {not (f["hsa"] < self.share2(dict(f, ded_left=x))) for x in (0, f["ded"])}
            return {"ok": outs.pop() if len(outs) == 1 else None}
        return {"ok": not (f["hsa"] < self.share2(f))}

    def val(self, f):
        return self.share(f)

    def val2(self, f):
        return self.share2(f)

    def fmtv(self, f, v):
        return money(v)

    def wrongs(self, f):
        b = f["bill"]
        return [cents_round(Fr(b * f["co"], 100)), cents_round(f["ded_left"] + Fr(b * f["co"], 100)),
                cents_round(min(b, f["ded_left"]) + Fr(max(0, b - f["ded_left"]) * f["co"], 100)),
                cents_round(Fr(max(0, b - f["ded_left"]) * f["co"], 100)), cents_round(Fr(b * (100 - f["co"]), 100))]

    def alts(self, f):
        if f["ded_left"] is None:
            return {}
        return {"hsa": [f["hsa"] + d for d in (-1, 1, -100, 100, -5000, 5000)], "bill": [f["bill"] + d for d in (-100, 100, -5000, 5000, -50000, 50000)],
                "ded_left": [x for x in (0, f["ded"] // 2, f["ded"]) if x != f["ded_left"]], "co": [c for c in (10, 20, 30) if c != f["co"]],
                "oop_left": [f["oop_left"] - 5000, f["oop_left"] + 5000]}

    def edges(self, f, p):
        t = ["numeric"]
        if f["ded_left"] is None:
            return t + ["missing_info"]
        if self.share(f) == f["oop_left"]:
            t.append("exception")
        return t

    def render(self, f):
        st = Sty(f)
        M = lambda c, w=False: money(c, "$", w)
        pol = (f"{f['org']} Health Plan - cost sharing (in-network)\n- Annual deductible: {M(f['ded'], True)}. Until it is met, the member pays covered charges in full.\n"
               f"- After the deductible, the member pays {f['co']}% coinsurance and the plan pays {100 - f['co']}%.\n"
               f"- Out-of-pocket maximum: {M(f['oop'], True)} per year. Once the member's deductible and coinsurance payments reach it, the plan pays 100% for the rest of the year.\n"
               f"- Amounts are rounded to the nearest cent (half a cent rounds up).")
        dl = ("does not know how much of this year's deductible has already been met" if f["ded_left"] is None else
              "has already met this year's deductible" if f["ded_left"] == 0 else f"still has {M(f['ded_left'])} of the deductible to meet")
        scen = (f"{f['who'][0]} {dl}, and has {M(f['oop_left'])} left before reaching the out-of-pocket maximum. "
                f"{cap(f['who'][1])} {V(f['who'], 'receives')} an in-network bill of {M(f['bill'])} for a covered procedure and {V(f['who'], 'has')} {M(f['hsa'])} in a health savings account.")
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Is the balance in the health savings account enough to cover {who}'s share of this bill?", f"Can {who} pay {f['who'][3]} share of this bill entirely from the health savings account?"],
                    neg=[f"Is {who}'s share of this bill more than the savings account balance?", f"Will {who} need money beyond the savings account to pay {f['who'][3]} share?"],
                    cpos="the savings account covers the member's share", cneg="the savings account does not cover the member's share",
                    speakers=[("A billing representative told " + f["who"][2] + " that", "the representative")])

    def letter_q(self, f):
        return [f"How much of this bill does {f['who'][0]} have to pay?"]


# =============================================================================================================
class CurrencyExpense(Schema):
    """Foreign receipts converted at the rate for the receipt date from a rate table (direction varies)."""
    name = "currency_expense"
    quota = 500
    letter = True
    table = True
    multi_hop = True
    hide_keys = {"ok": ["rd"]}
    PAIRS = [("EUR", "€", "USD", "$", (10600, 11200)), ("GBP", "£", "USD", "$", (12400, 13200)), ("USD", "$", "CAD", "CA$", (13300, 14000)),
             ("JPY", "¥", "USD", "$", (6200, 7200)), ("EUR", "€", "GBP", "£", (8300, 8800)), ("USD", "$", "EUR", "€", (8900, 9500)),
             ("CHF", "CHF", "EUR", "€", (10300, 10900)), ("AUD", "A$", "USD", "$", (6300, 6900))]

    def sample(self, rng):
        fc, fs, hc, hs, (lo, hi) = rng.choice(self.PAIRS)
        yr = rng.choice([2025, 2026, 2027])
        d0 = dt.date(yr, rng.randint(1, 12), rng.randint(1, 24))
        days = [iso(d0 + dt.timedelta(days=k)) for k in range(4)]
        scale = 10 ** 6 if fc == "JPY" else 10 ** 4
        r0 = rng.randrange(lo, hi)
        rates = [r0 + rng.randint(-(r0 // 150), r0 // 150) for _ in days]  # home per 1 foreign, in 1/scale units (small daily moves)
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "fc": fc, "fs": fs, "hc": hc, "hs": hs,
             "days": days, "rates": rates, "scale": scale, "inv": rng.random() < 0.3, "rd": rng.choice(days[:3]) if True else None,
             "cap": rng.choice([5000, 6000, 7500, 10000, 15000]), "kind": rng.choice(["meal", "taxi", "conference"])}
        if f["inv"]:
            # table shows foreign per 1 home; store as integer foreign-per-home at scale 10**4 and derive the true rate
            j0 = rng.randrange(14000, 16000)
            f["rates"] = ([10 ** 8 // r for r in rates] if fc != "JPY" else [(j0 + rng.randint(-100, 100)) * 100 for _ in rates])
            f["scale"] = 10 ** 4
        target = f["cap"] + rng.choice([0, 0, 1, -1, -2, 2, 150, -150])
        # choose foreign amount (minor units; JPY has none) so the converted value lands near target
        lo_, hi_ = 1, 10 ** 9
        while lo_ < hi_:
            mid = (lo_ + hi_) // 2
            f["amt"] = mid
            if self.conv(f) >= target:
                hi_ = mid
            else:
                lo_ = mid + 1
        f["amt"] = lo_
        return f

    def rate(self, f):
        i = f["days"].index(f["rd"])
        return Fr(f["rates"][i], f["scale"])

    def minor(self, f):
        return 1 if f["fc"] == "JPY" else 100

    def conv(self, f):
        """converted amount in home cents."""
        amt = Fr(f["amt"], self.minor(f))
        home = amt / self.rate(f) if f["inv"] else amt * self.rate(f)
        return cents_round(home * 100)

    def conv2(self, f):
        i = f["days"].index(f["rd"])
        r = Decimal(f["rates"][i]) / Decimal(f["scale"])
        amt = Decimal(f["amt"]) / Decimal(self.minor(f))
        with localcontext() as c:
            c.prec = 50
            home = (amt / r) if f["inv"] else (amt * r)
            return dcents(home * 100)

    def valid(self, f):
        return f["amt"] > 0 and (f["rd"] is None or f["rd"] in f["days"])

    def preds(self, f):
        if f["rd"] is None:
            outs = {self.conv(dict(f, rd=d)) <= f["cap"] for d in f["days"]}
            return {"ok": outs.pop() if len(outs) == 1 else None}
        return {"ok": self.conv(f) <= f["cap"]}

    def preds2(self, f):
        if f["rd"] is None:
            outs = {not (self.conv2(dict(f, rd=d)) > f["cap"]) for d in f["days"]}
            return {"ok": outs.pop() if len(outs) == 1 else None}
        return {"ok": not (self.conv2(f) > f["cap"])}

    def val(self, f):
        return None if f["rd"] is None else self.conv(f)

    def val2(self, f):
        return None if f["rd"] is None else self.conv2(f)

    def fmtv(self, f, v):
        return money(v, f["hs"])

    def wrongs(self, f):
        out = []
        for d in f["days"]:
            if d != f["rd"]:
                out.append(self.conv(dict(f, rd=d)))
        out.append(self.conv(dict(f, inv=not f["inv"])))
        return out

    def alts(self, f):
        if f["rd"] is None:
            return {}
        return {"amt": [f["amt"] + d for d in (-1, 1, -2, 2, -100, 100, -1000, 1000)], "rd": [d for d in f["days"] if d != f["rd"]],
                "cap": [f["cap"] - 500, f["cap"] + 500]}

    def edges(self, f, p):
        return ["numeric", "units", "temporal"] + (["missing_info"] if f["rd"] is None else [])

    def fmt_amt(self, f):
        if f["fc"] == "JPY":
            return f"¥{f['amt']:,}"
        return money(f["amt"], f["fs"])

    def render(self, f):
        st = Sty(f)
        ds = st.i("ds", 3)
        hdr = (f"1 {f['hc']} in {f['fc']}" if f["inv"] else f"1 {f['fc']} in {f['hc']}")
        dp = len(str(f["scale"])) - 1
        rows = "\n".join(f"{fd(d, 2)} | {fdec(Fr(r, f['scale']), dp)}" for d, r in zip(f["days"], f["rates"]))
        what = {"meal": "Meals", "taxi": "Taxi fares", "conference": "Conference fees"}[f["kind"]]
        pol = (f"{f['org']} Foundation - travel reimbursement\n- {what} are reimbursed up to {money(f['cap'], f['hs'])} per receipt, in {f['hc']}.\n"
               f"- Convert foreign receipts using the rate for the date printed on the receipt, from the table below, and round to the nearest cent (half a cent rounds up).\n\n"
               f"Exchange rates (date | {hdr}):\n{rows}")
        if f["rd"] is None:
            scen = (f"{f['who'][0]} submits a receipt for {self.fmt_amt(f)} from a day in the week covered by the table; "
                    f"the date printed on the receipt is smudged and cannot be read.")
        else:
            scen = f"{f['who'][0]} submits a receipt dated {fd(f['rd'], ds)} for {self.fmt_amt(f)}."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Is {who}'s receipt within the reimbursement limit after conversion?", f"Will the whole receipt be reimbursed?"],
                    neg=[f"Does the converted receipt amount exceed the limit?", f"Will part of {who}'s receipt be left unreimbursed?"],
                    cpos="the converted receipt is within the limit", cneg="the converted receipt exceeds the limit",
                    speakers=[("The claims officer told " + f["who"][2] + " that", "the claims officer")])

    def letter_q(self, f):
        return [f"What is the receipt amount in {f['hc']} under this policy?"]


# =============================================================================================================
GP = {"A": Fr(4), "A-": Fr(37, 10), "B+": Fr(33, 10), "B": Fr(3), "B-": Fr(27, 10), "C+": Fr(23, 10), "C": Fr(2),
      "C-": Fr(17, 10), "D": Fr(1), "F": Fr(0)}
COURSES = ["Calculus II", "Organic Chemistry", "World History", "Microeconomics", "Data Structures", "Statistics",
           "Philosophy of Mind", "Spanish III", "Physics Lab", "Art History", "Linear Algebra", "Public Speaking",
           "Genetics", "Accounting I", "Creative Writing", "Music Theory", "Sociology", "Thermodynamics"]


class GpaHonors(Schema):
    """Credit-weighted GPA with a stated rounding rule, compared with honors thresholds."""
    name = "gpa_honors"
    quota = 500
    cat = ["summa cum laude", "magna cum laude", "cum laude", "no honors"]
    cat_defs = {"summa cum laude": "The GPA, computed and rounded exactly as the policy states, is at or above the summa threshold.",
                "magna cum laude": "The GPA, computed and rounded as stated, is at or above the magna threshold but below the summa threshold.",
                "cum laude": "The GPA, computed and rounded as stated, is at or above the cum laude threshold but below the magna threshold.",
                "no honors": "The GPA, computed and rounded as stated, is below the cum laude threshold."}
    choice_share = 0.3
    multi_hop = True
    table = True

    def sample(self, rng):
        th = rng.choice([(390, 370, 350), (385, 365, 345), (395, 375, 355), (380, 360, 340)])
        for _ in range(400):
            k = rng.randint(4, 7)
            cr = [rng.choice([1, 2, 3, 3, 3, 4, 4, 5]) for _ in range(k)]
            gr = [rng.choice(["A", "A", "A-", "A-", "B+", "B+", "B", "B-", "C+", "A"]) for _ in range(k)]
            g = sum(c * GP[x] for c, x in zip(cr, gr)) / sum(cr)
            if any(abs(g - Fr(t, 100)) <= Fr(1, 100) for t in th):
                break
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "cr": cr, "gr": gr,
             "names": rng.sample(COURSES, k), "th": list(th), "rule": rng.choice(["half_up", "down", "exact", "half_up"])}
        return f

    def gpa(self, f):
        g = sum(c * GP[x] for c, x in zip(f["cr"], f["gr"])) / sum(f["cr"])
        return g if f["rule"] == "exact" else rnd(g, 2, f["rule"])

    def gpa2(self, f):
        tab = {"A": "4.0", "A-": "3.7", "B+": "3.3", "B": "3.0", "B-": "2.7", "C+": "2.3", "C": "2.0", "C-": "1.7", "D": "1.0", "F": "0"}
        with localcontext() as c:
            c.prec = 60
            g = sum(Decimal(cc) * Decimal(tab[x]) for cc, x in zip(f["cr"], f["gr"])) / Decimal(sum(f["cr"]))
            if f["rule"] == "exact":
                return g
            return drnd(g, 2, f["rule"])

    def _cat(self, g, th):
        if g >= Fr(th[0], 100):
            return "summa cum laude"
        if g >= Fr(th[1], 100):
            return "magna cum laude"
        if g >= Fr(th[2], 100):
            return "cum laude"
        return "no honors"

    def catv(self, f):
        return self._cat(self.gpa(f), f["th"])

    def catv2(self, f):
        g = self.gpa2(f)
        th = [Decimal(t) / Decimal(100) for t in f["th"]]
        return ("summa cum laude" if g >= th[0] else "magna cum laude" if g >= th[1] else "cum laude" if g >= th[2] else "no honors")

    def preds(self, f):
        return {"honors": self.catv(f) != "no honors"}

    def preds2(self, f):
        return {"honors": self.catv2(f) != "no honors"}

    preds_list = ("honors",)

    def alts(self, f):
        a = {"rule": [r for r in ("half_up", "down", "exact") if r != f["rule"]]}
        g = []
        order = ["A", "A-", "B+", "B", "B-", "C+"]
        for i, x in enumerate(f["gr"]):
            j = order.index(x) if x in order else 3
            for y in (order[max(0, j - 1)], order[min(len(order) - 1, j + 1)]):
                if y != x:
                    z = list(f["gr"])
                    z[i] = y
                    g.append(z)
        a["gr"] = g
        c = []
        for i, x in enumerate(f["cr"]):
            for y in (x - 1, x + 1):
                if 1 <= y <= 5:
                    z = list(f["cr"])
                    z[i] = y
                    c.append(z)
        a["cr"] = c
        return a

    def edges(self, f, p):
        return ["numeric", "table"]

    def render(self, f):
        st = Sty(f)
        th = [fdec(Fr(t, 100), 2) for t in f["th"]]
        rule = {"half_up": "The GPA is rounded to two decimal places (a third decimal of 5 or more rounds up) before it is compared with the thresholds.",
                "down": "The GPA is truncated (not rounded) to two decimal places before it is compared with the thresholds.",
                "exact": "The exact GPA is compared with the thresholds; it is not rounded."}[f["rule"]]
        pol = (f"{f['org']} University - graduation honors\n- GPA = sum of (credits x grade points) / total credits. Grade points: A 4.0, A- 3.7, B+ 3.3, B 3.0, B- 2.7, C+ 2.3, C 2.0.\n"
               f"- {rule}\n- Summa cum laude: {th[0]} or higher; magna cum laude: {th[1]} or higher; cum laude: {th[2]} or higher.")
        GW = {"A": "A", "A-": "A minus", "B+": "B plus", "B": "B", "B-": "B minus", "C+": "C plus", "C": "C", "C-": "C minus"}
        rows = "\n".join(f"{n} | {c} | {g} ({GW[g]})" if g not in ("A", "B", "C") else f"{n} | {c} | {g}"
                         for n, c, g in zip(f["names"], f["cr"], f["gr"]))
        scen = f"{f['who'][0]}'s complete record (course | credits | grade):\n{rows}"
        return f"{pol}\n\n{st.c('lab', ['Record: ', '', 'Transcript: '])}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Does {who} graduate with honors of any level?", f"Does {who}'s GPA qualify for at least cum laude?"],
                    neg=[f"Does {who} graduate without any honors?", f"Does {who}'s GPA fall short of every honors threshold?"],
                    cpos=f"{who} qualifies for honors", cneg=f"{who} does not qualify for any honors",
                    speakers=[("A classmate told " + f["who"][2] + " that", "the classmate"), ("An advisor's email said", "the advisor's email")])

    def cat_q(self, f):
        return [f"Which honors designation does {f['who'][0]} receive?", f"What level of honors, if any, applies to {f['who'][0]}?"]


# =============================================================================================================
class PassMark(Schema):
    """Percentage from points with a stated rounding rule (half up / truncate / half even) against a pass mark."""
    name = "pass_mark"
    quota = 450
    letter = True

    def sample(self, rng):
        mx = rng.choice([40, 60, 80, 120, 150, 200, 250])
        pm = rng.choice([40, 50, 50, 60, 65, 70])
        rule = rng.choice(["half_up", "down", "half_even", "exact"])
        # points in half-point steps near the boundary
        tgt = Fr(pm, 100) * mx
        pts = tgt + Fr(rng.choice([0, 0, -1, 1, -2, 2, -3, 3, -5, 5]), 2)
        if rng.random() < 0.4:
            pts = Fr(pm * 2 - 1, 2) * mx / 100
            pts = rnd(pts * 2, 0, "floor") / 2 + Fr(rng.choice([0, 1]), 2)
        pts = max(Fr(0), min(Fr(mx), pts))
        return {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "mx": mx, "pm": pm,
                "rule": rule, "pts2": int(pts * 2), "subj": rng.choice(["chemistry", "driving theory", "first-aid", "accounting", "nursing pharmacology"])}

    def pct(self, f):
        p = Fr(f["pts2"], 2) / f["mx"] * 100
        return p if f["rule"] == "exact" else rnd(p, 0, f["rule"])

    def pct2(self, f):
        with localcontext() as c:
            c.prec = 50
            p = Decimal(f["pts2"]) / Decimal(2) / Decimal(f["mx"]) * Decimal(100)
            return p if f["rule"] == "exact" else drnd(p, 0, f["rule"])

    def valid(self, f):
        return 0 <= f["pts2"] <= 2 * f["mx"]

    def preds(self, f):
        return {"ok": self.pct(f) >= f["pm"]}

    def preds2(self, f):
        return {"ok": not (self.pct2(f) < f["pm"])}

    def val(self, f):
        return self.pct(f) if f["rule"] != "exact" else None

    def val2(self, f):
        return Fr(self.pct2(f)) if f["rule"] != "exact" else None

    def fmtv(self, f, v):
        return f"{ftrim(Fr(v), 2)}%"

    def wrongs(self, f):
        p = Fr(f["pts2"], 2) / f["mx"] * 100
        return [rnd(p, 0, m) for m in ("half_up", "down", "half_even", "ceil") if rnd(p, 0, m) != self.pct(f)] + [self.pct(f) + 1, self.pct(f) - 1]

    def alts(self, f):
        return {"pts2": [f["pts2"] + d for d in (-1, 1, -2, 2)], "rule": [r for r in ("half_up", "down", "half_even", "exact") if r != f["rule"]],
                "pm": [f["pm"] - 1, f["pm"] + 1]}

    def edges(self, f, p):
        return ["numeric"]

    def render(self, f):
        st = Sty(f)
        rule = {"half_up": "The percentage is rounded to the nearest whole number; exactly .5 rounds up.",
                "down": "The percentage is truncated to a whole number (any decimals are dropped, never rounded up).",
                "half_even": "The percentage is rounded to the nearest whole number; exactly .5 rounds to the nearest even number (so 64.5 becomes 64 and 65.5 becomes 66).",
                "exact": "The percentage is not rounded; the exact value is compared with the pass mark."}[f["rule"]]
        pol = (f"{f['org']} Academy - {f['subj']} exam regulations\n- The exam is marked out of {f['mx']} points; half points may be awarded.\n"
               f"- Final percentage = points scored / {f['mx']} x 100. {rule}\n- The pass mark is {f['pm']}%.")
        pts = ftrim(Fr(f["pts2"], 2), 1)
        scen = f"{f['who'][0]} scored {pts} points out of {f['mx']}."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Did {who} pass the exam?", f"Does {who}'s final percentage reach the pass mark?"],
                    neg=[f"Did {who} fail the exam?", f"Is {who}'s final percentage below the pass mark?"],
                    cpos=f"{who} passed", cneg=f"{who} failed",
                    speakers=[("A tutor told " + f["who"][2] + " that", "the tutor"), ("A classmate said", "the classmate")])

    def letter_q(self, f):
        return [f"What final percentage is recorded for {f['who'][0]}?"]


# =============================================================================================================
class TimeclockOvertime(Schema):
    """Quarter-hour punch rounding (7-minute rule), unpaid break, daily overtime threshold."""
    name = "timeclock"
    quota = 450
    letter = True
    multi_hop = True

    def sample(self, rng):
        t_in = rng.randrange(360, 600)
        brk = rng.choice([0, 30, 30, 45, 60])
        thr = rng.choice([8, 8, 10])
        target = thr * 60 + brk + rng.choice([0, 0, 15, -15, 30])
        t_out = t_in + target + rng.choice([-8, -7, 7, 8, 0, -1, 1, 22, 23, -22, -23])
        return {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "in": t_in, "out": t_out,
                "brk": brk, "thr": thr}

    @staticmethod
    def r15(m):
        r = m % 15
        return m - r if r <= 7 else m - r + 15

    @staticmethod
    def r15b(m):
        return ((m + 7) // 15) * 15

    def paid(self, f):
        return self.r15(f["out"]) - self.r15(f["in"]) - f["brk"]

    def paid2(self, f):
        return self.r15b(f["out"]) - self.r15b(f["in"]) - f["brk"]

    def valid(self, f):
        return 0 <= f["in"] < f["out"] < 1440 and self.paid(f) > 0

    def preds(self, f):
        return {"ok": self.paid(f) > f["thr"] * 60}

    def preds2(self, f):
        return {"ok": not (self.paid2(f) <= f["thr"] * 60)}

    def val(self, f):
        return self.paid(f)

    def val2(self, f):
        return self.paid2(f)

    def fmtv(self, f, v):
        return f"{ftrim(Fr(v, 60), 2)} hours"

    def wrongs(self, f):
        raw = f["out"] - f["in"] - f["brk"]
        p = self.paid(f)
        return [p + 15, p - 15, (f["out"] // 15) * 15 - (f["in"] // 15) * 15 - f["brk"], p + f["brk"],
                ((f["out"] + 14) // 15) * 15 - ((f["in"] + 14) // 15) * 15 - f["brk"], p + 30]

    def alts(self, f):
        return {"out": [f["out"] + d for d in (-1, 1, -2, 2, -15, 15)], "in": [f["in"] + d for d in (-1, 1, -8, 8)],
                "brk": [b for b in (0, 30, 45, 60) if b != f["brk"]], "thr": [t for t in (8, 9, 10) if t != f["thr"]]}

    def edges(self, f, p):
        return ["numeric", "temporal"]

    def render(self, f):
        st = Sty(f)
        ts = st.i("ts", 3)
        br = (f"An unpaid meal break of {f['brk']} minutes is deducted from each shift." if f["brk"] else "There is no unpaid break on this shift pattern.")
        pol = (f"{f['org']} Distribution Center - timekeeping\n- Clock-in and clock-out times are each rounded to the nearest quarter hour: 1 to 7 minutes past a quarter hour rounds down, 8 to 14 minutes rounds up.\n"
               f"- {br}\n- Paid time above {f['thr']} hours in a single day is paid as daily overtime.")
        scen = f"On {st.c('day', WEEKDAYS[:5])}, {f['who'][0]} clocked in at {ft(f['in'], ts)} and clocked out at {ft(f['out'], ts)}.".replace(".m..", ".m.")
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Is {who} owed any daily overtime for that day?", f"Does {who}'s paid time that day go above the daily overtime threshold?"],
                    neg=[f"Is all of {who}'s paid time that day at the regular rate, with no overtime?"],
                    cpos=f"{who} earned some daily overtime that day", cneg=f"{who} earned no overtime that day",
                    speakers=[("A shift lead told " + f["who"][2] + " that", "the shift lead")])

    def letter_q(self, f):
        return [f"How much paid time is {f['who'][0]} credited with for that day?"]


# =============================================================================================================
class CashRounding(Schema):
    """Sales tax to the cent, then cash rounding to 5 cents (card payments not rounded)."""
    name = "cash_rounding"
    quota = 400
    letter = True
    multi_hop = True

    def sample(self, rng):
        k = rng.choice([1, 2, 3])
        items = [rng.randrange(99, 4999) for _ in range(k)]
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "items": items,
             "tax": rng.choice([13, 5, 15, 12, 14]), "pay": rng.choice(["cash", "cash", "card"])}
        amt = self.due(f)
        f["asked"] = amt + rng.choice([0, 0, 0, -1, 1, -2, 2, 3, -3, 5, -5])
        return f

    def total(self, f):
        s = sum(f["items"])
        return s + cents_round(Fr(s * f["tax"], 100))

    def due(self, f):
        t = self.total(f)
        if f["pay"] == "card":
            return t
        r = t % 5
        return t - r if r in (0, 1, 2) else t + (5 - r)

    def due2(self, f):
        s = Decimal(sum(f["items"]))
        t = int(s + drnd(s * Decimal(f["tax"]) / Decimal(100), 0, "half_up"))
        if f["pay"] == "card":
            return t
        last = t % 10
        return {0: t, 1: t - 1, 2: t - 2, 3: t + 2, 4: t + 1, 5: t, 6: t - 1, 7: t - 2, 8: t + 2, 9: t + 1}[last]

    def valid(self, f):
        return all(x > 0 for x in f["items"]) and f["asked"] > 0

    def preds(self, f):
        return {"ok": f["asked"] == self.due(f)}

    def preds2(self, f):
        return {"ok": f["asked"] == self.due2(f)}

    def val(self, f):
        return self.due(f)

    def val2(self, f):
        return self.due2(f)

    def fmtv(self, f, v):
        return money(v, "$")

    def wrongs(self, f):
        t = self.total(f)
        return [t, (t // 5) * 5, -(-t // 5) * 5, (t // 10) * 10, self.due(f) + 5, self.due(f) - 5]

    def alts(self, f):
        its = []
        for i, x in enumerate(f["items"]):
            for d in (-1, 1, -2, 2, 3):
                z = list(f["items"])
                z[i] = x + d
                its.append(z)
        return {"asked": [f["asked"] + d for d in (-1, 1, -2, 2, -5, 5)], "pay": ["card" if f["pay"] == "cash" else "cash"], "items": its}

    def edges(self, f, p):
        return ["numeric"] + (["exception"] if f["pay"] == "card" else [])

    def render(self, f):
        st = Sty(f)
        tx = {13: "HST", 5: "GST", 15: "HST", 12: "combined sales tax", 14: "combined sales tax"}[f["tax"]]
        pol = (f"{f['org']} Grocers (Canada) - checkout guide\n- Add {tx} of {f['tax']}% to the subtotal of taxable items and round the tax to the nearest cent (half a cent rounds up).\n"
               f"- Cash payments: round the final total to the nearest 5 cents. Totals ending in 1 or 2 cents round down to 0; 3 or 4 round up to 5; 6 or 7 round down to 5; 8 or 9 round up to the next 10.\n"
               f"- Card and phone payments are charged the exact total, without rounding.")
        its = ", ".join(money(x) for x in f["items"])
        scen = (f"{f['who'][0]} buys {len(f['items'])} taxable {plural(len(f['items']), 'item')} priced {its} and pays by {'cash' if f['pay'] == 'cash' else 'debit card'}. "
                f"The cashier asks for {money(f['asked'])}.")
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        return dict(pos=["Is the cashier asking for the correct amount?", "Does the amount requested match the checkout rules?"],
                    neg=["Is the cashier asking for the wrong amount?"],
                    cpos="the cashier asked for the correct amount", cneg="the cashier asked for the wrong amount",
                    speakers=[(f"{f['who'][0]}'s friend, standing in line behind, said", "the friend")])

    def letter_q(self, f):
        return [f"How much should {f['who'][0]} be charged?"]


# =============================================================================================================
class Attendance(Schema):
    """Minimum attendance percentage with excused-absence rules (exact fractions, boundary cases)."""
    name = "attendance"
    quota = 500
    hide_keys = {"ok": ["exc_rule"]}

    def sample(self, rng):
        n = rng.choice([20, 24, 25, 30, 32, 36, 40, 45, 48, 60])
        p = rng.choice([75, 80, 80, 85, 90, 70])
        need = -(-p * n // 100)
        att = need + rng.choice([0, 0, -1, 1, -2, 2])
        ab = n - att
        e = rng.randint(0, min(ab, 4))
        return {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "n": n, "p": p,
                "u": ab - e, "e": e, "exc_rule": rng.choice(["attended", "absent", "attended"]),
                "phr": rng.choice(["attend", "miss"]), "dom": rng.choice(["course", "training", "apprentice"])}

    def _ok(self, f, rule):
        att = f["n"] - f["u"] - (0 if rule == "attended" else f["e"])
        return Fr(att, f["n"]) >= Fr(f["p"], 100)

    def preds(self, f):
        if f["exc_rule"] is None:
            a, b = self._ok(f, "attended"), self._ok(f, "absent")
            return {"ok": a if a == b else None}
        return {"ok": self._ok(f, f["exc_rule"])}

    def preds2(self, f):
        rules = ["attended", "absent"] if f["exc_rule"] is None else [f["exc_rule"]]
        outs = set()
        for r in rules:
            missed = f["u"] + (0 if r == "attended" else f["e"])
            outs.add(missed * 100 <= (100 - f["p"]) * f["n"])
        return {"ok": outs.pop() if len(outs) == 1 else None}

    def valid(self, f):
        return f["u"] >= 0 and f["e"] >= 0 and f["u"] + f["e"] <= f["n"]

    def alts(self, f):
        return {"u": [f["u"] + d for d in (-1, 1, -2, 2)], "e": [f["e"] + d for d in (-1, 1)],
                "exc_rule": [r for r in ("attended", "absent") if r != f["exc_rule"]], "p": [f["p"] - 5, f["p"] + 5]}

    def neg_rule(self, f):
        return f["phr"] == "miss"

    def edges(self, f, p):
        t = ["numeric"]
        if f["e"]:
            t.append("exception")
        if f["exc_rule"] is None:
            t.append("missing_info")
        if f["phr"] == "miss":
            t.append("negation")
        return t

    def render(self, f):
        st = Sty(f)
        n, p = f["n"], f["p"]
        what = {"course": "the course", "training": "the safety training", "apprentice": "the apprenticeship classes"}[f["dom"]]
        req = (f"Participants must attend at least {p}% of the {n} scheduled sessions of {what} to receive the certificate."
               if f["phr"] == "attend" else
               f"Participants who miss more than {100 - p}% of the {n} scheduled sessions of {what} do not receive the certificate.")
        if f["exc_rule"] == "attended":
            ex = "Absences excused with a medical certificate are treated as sessions attended."
        elif f["exc_rule"] == "absent":
            ex = "All absences count, including absences excused with a medical certificate."
        else:
            ex = "The committee has not yet decided whether absences excused with a medical certificate will count as attended this term."
        pol = f"{f['org']} Community College - certificate rules\n- {req}\n- {ex}\n- Late arrivals of more than 15 minutes are recorded as absences."
        scen = (f"{f['who'][0]} missed {f['u'] + f['e']} of the {n} sessions" +
                (f"; {f['e']} of those absences {'was' if f['e'] == 1 else 'were'} excused with a medical certificate." if f["e"] else ", none of them excused.") +
                " There were no late arrivals.")
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Does {who} meet the attendance requirement for the certificate?", f"Will {who} receive the certificate as far as attendance is concerned?"],
                    neg=[f"Does {who} fail the attendance requirement?", f"Will {who} be refused the certificate because of attendance?"],
                    cpos=f"{who} meets the attendance requirement", cneg=f"{who} fails the attendance requirement",
                    speakers=[("The course coordinator told " + f["who"][2] + " that", "the coordinator"), ("A classmate said", "the classmate")])


# =============================================================================================================
class PercentChange(Schema):
    """Relative percent change vs percentage-point change; 'more than' vs 'at least'."""
    name = "percent_change"
    quota = 500
    letter = True

    def sample(self, rng):
        dom = rng.choice(["rent", "rate_rel", "rate_pts", "salary", "price"])
        f = {"dom": dom, "who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9),
             "cmp": rng.choice(["gt", "ge"])}
        if dom in ("rate_rel", "rate_pts"):
            old = rng.choice([250, 300, 350, 400, 450, 500, 600, 800])  # basis points * 1 (percent * 100)
            thr = rng.choice([10, 15, 20, 25]) if dom == "rate_rel" else rng.choice([50, 75, 100, 150])
            if dom == "rate_rel":
                new = old + old * thr // 100 + rng.choice([0, 0, 1, -1, 5, -5, 25, -25])
            else:
                new = old + thr + rng.choice([0, 0, 1, -1, 5, -5, 25, -25])
            f.update(old=old, new=new, thr=thr)
        else:
            old = {"rent": rng.randrange(80000, 300000, 500), "salary": rng.randrange(4000000, 12000000, 50000),
                   "price": rng.randrange(900, 20000, 100)}[dom]
            thr = rng.choice([3, 5, 5, 7, 8, 10])
            new = old + old * thr // 100 + rng.choice([0, 0, 1, -1, 100, -100, 500, -500])
            f.update(old=old, new=new, thr=thr)
        return f

    def change(self, f):
        """relative change in percent, or point change in percentage points (both exact Fractions)."""
        if f["dom"] == "rate_pts":
            return Fr(f["new"] - f["old"], 100)
        return Fr(f["new"] - f["old"], f["old"]) * 100

    def thr(self, f):
        return Fr(f["thr"], 100) if f["dom"] == "rate_pts" else Fr(f["thr"])

    def preds(self, f):
        c, t = self.change(f), self.thr(f)
        return {"ok": c > t if f["cmp"] == "gt" else c >= t}

    def preds2(self, f):
        # cross-multiplied integers
        d = f["new"] - f["old"]
        if f["dom"] == "rate_pts":
            return {"ok": d > f["thr"] if f["cmp"] == "gt" else d >= f["thr"]}
        return {"ok": d * 100 > f["thr"] * f["old"] if f["cmp"] == "gt" else d * 100 >= f["thr"] * f["old"]}

    def valid(self, f):
        return f["old"] > 0 and f["new"] > 0

    def val(self, f):
        c = self.change(f)
        return c if (c * 100).denominator == 1 else None

    def val2(self, f):
        d = f["new"] - f["old"]
        c = Fr(d, 100) if f["dom"] == "rate_pts" else Fr(d * 100, f["old"])
        return c if (c * 100).denominator == 1 else None

    def fmtv(self, f, v):
        u = (" percentage point" if Fr(v) == 1 else " percentage points") if f["dom"] == "rate_pts" else "%"
        s = ftrim(Fr(v), 2)
        return f"{s}{u}" if u == "%" else f"{s}{u}"

    def wrongs(self, f):
        d = f["new"] - f["old"]
        out = []
        if f["dom"] in ("rate_rel", "rate_pts"):
            out += [Fr(d, 100), Fr(d * 100, f["old"])]
        out += [Fr(d * 100, f["new"]), self.change(f) + 1, self.change(f) - 1]
        return [x for x in out if (Fr(x) * 100).denominator == 1]

    def alts(self, f):
        return {"new": [f["new"] + d for d in (-1, 1, -5, 5, -100, 100)], "cmp": ["ge" if f["cmp"] == "gt" else "gt"],
                "thr": [f["thr"] + d for d in (-1, 1, -5, 5) if f["thr"] + d > 0]}

    def edges(self, f, p):
        t = ["numeric"]
        if f["dom"] in ("rate_rel", "rate_pts"):
            t.append("units")
        return t

    def render(self, f):
        st = Sty(f)
        cmpw = "more than" if f["cmp"] == "gt" else "at least"
        dom = f["dom"]
        if dom == "rent":
            pol = f"{f['org']} Tenancy Rules - rent increases\n- A rent increase of {cmpw} {f['thr']}% of the current rent requires 90 days' written notice; smaller increases require 30 days' notice.\n- Rent may be increased at most once in 12 months."
            scen = f"{f['who'][0]}'s landlord plans to raise the monthly rent from {money(f['old'])} to {money(f['new'])}."
        elif dom == "salary":
            pol = f"{f['org']} Corp - compensation policy\n- A pay rise of {cmpw} {f['thr']}% of the current base salary needs approval from a vice president.\n- Bonuses are handled separately."
            scen = f"A manager proposes raising {f['who'][0]}'s base salary from {money(f['old'], '$', True)} to {money(f['new'], '$', True)} a year."
        elif dom == "price":
            pol = f"{f['org']} Software - subscription terms\n- If the monthly price rises by {cmpw} {f['thr']}%, existing subscribers may cancel immediately with a pro-rated refund.\n- Taxes are not part of the price."
            scen = f"The monthly price of {f['who'][0]}'s plan is going up from {money(f['old'])} to {money(f['new'])}."
        elif dom == "rate_rel":
            pol = (f"{f['org']} Bank - variable-rate loan terms\n- If the interest rate increases by {cmpw} {f['thr']}% of the current rate (a relative increase, not percentage points), the borrower may switch to a fixed rate without a fee.\n"
                   f"- Rates are quoted per year.")
            scen = f"The rate on {f['who'][0]}'s loan is changing from {ftrim(Fr(f['old'], 100), 2)}% to {ftrim(Fr(f['new'], 100), 2)}% a year."
        else:
            pol = (f"{f['org']} Bank - variable-rate loan terms\n- If the interest rate increases by {cmpw} {ftrim(Fr(f['thr'], 100), 2)} {'percentage point' if f['thr'] == 100 else 'percentage points'}, the borrower may switch to a fixed rate without a fee.\n"
                   f"- Rates are quoted per year.")
            scen = f"The rate on {f['who'][0]}'s loan is changing from {ftrim(Fr(f['old'], 100), 2)}% to {ftrim(Fr(f['new'], 100), 2)}% a year."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        m = {"rent": (["Does this rent increase require 90 days' notice?"], ["Is 30 days' notice enough for this rent increase?"],
                      "the increase requires 90 days' notice", "30 days' notice is enough for this increase"),
             "salary": ([f"Does {who}'s proposed raise need a vice president's approval?"], [f"Can the manager approve {who}'s raise without a vice president?"],
                        "the raise needs a vice president's approval", "the raise does not need a vice president's approval"),
             "price": ([f"May {who} cancel immediately with a pro-rated refund because of this price rise?"], [f"Is this price rise too small to give {who} the right to cancel immediately?"],
                       f"{who} may cancel immediately", f"{who} may not cancel immediately"),
             "rate_rel": ([f"May {who} switch to a fixed rate without a fee?"], [f"Is the rate increase too small for a fee-free switch?"],
                          "the fee-free switch is available", "the fee-free switch is not available"),
             "rate_pts": ([f"May {who} switch to a fixed rate without a fee?"], [f"Is the rate increase too small for a fee-free switch?"],
                          "the fee-free switch is available", "the fee-free switch is not available")}[f["dom"]]
        sp = {"salary": [("An HR business partner told the manager that", "the HR business partner"), (f"A colleague of {who} said", "the colleague")],
              "rent": [("A tenants' association volunteer told " + f["who"][2] + " that", "the volunteer"), ("The letting agent said", "the letting agent")]}.get(
            f["dom"], [("A friend told " + f["who"][2] + " that", "the friend"), ("A customer adviser said", "the adviser")])
        return dict(pos=m[0], neg=m[1], cpos=m[2], cneg=m[3], speakers=sp)

    def letter_q(self, f):
        if f["dom"] == "rate_pts":
            return ["By how many percentage points is the rate increasing?"]
        if f["dom"] == "rate_rel":
            return ["By what percentage of the current rate is the rate increasing?"]
        return ["By what percentage is the amount increasing?"]


# =============================================================================================================
class Quorum(Schema):
    """Quorum and majority rules with abstentions."""
    name = "quorum_vote"
    quota = 500
    cat = ["passed", "failed", "no valid vote (no quorum)"]
    cat_defs = {"passed": "A quorum was present and the votes meet the stated majority rule, counted exactly as the rules define it (including how abstentions are treated).",
                "failed": "A quorum was present but the votes in favour do not meet the stated majority rule (a tie is not a majority).",
                "no valid vote (no quorum)": "Fewer members were present than the quorum requires, so the vote is invalid regardless of how people voted."}
    choice_share = 0.35
    multi_hop = True

    def sample(self, rng):
        M = rng.choice([9, 12, 15, 20, 21, 24, 30, 45, 60])
        q = rng.choice(["majority", "third", "fixed"])
        qn = rng.randint(M // 3, M // 2 + 2)
        rule = rng.choice(["cast", "present", "two_thirds", "members"])
        need_q = self.qneed(M, q, qn)
        P = max(1, need_q + rng.choice([0, 0, -1, 1, 2, 3, 5]))
        P = min(P, M)
        A = rng.randint(0, max(0, P // 4))
        vt = P - A
        Y = rng.randint(vt // 3, vt)
        N = vt - Y
        f = {"org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "M": M, "q": q, "qn": qn, "rule": rule,
             "votes": [Y, N, A], "body": rng.choice(["board", "council", "committee", "association"]), "who": person(rng)}
        return f

    @staticmethod
    def qneed(M, q, qn):
        if q == "majority":
            return M // 2 + 1
        if q == "third":
            return -(-M // 3)
        return qn

    def outcome(self, f):
        M = f["M"]
        Y, N, A = f["votes"]
        P = Y + N + A
        if P < self.qneed(M, f["q"], f["qn"]):
            return "no valid vote (no quorum)"
        r = f["rule"]
        if r == "cast":
            ok = Y > N
        elif r == "present":
            ok = Fr(Y, P) > Fr(1, 2)
        elif r == "two_thirds":
            ok = (Y + N) > 0 and Fr(Y, Y + N) >= Fr(2, 3)
        else:
            ok = Fr(Y, M) > Fr(1, 2)
        return "passed" if ok else "failed"

    def outcome2(self, f):
        M = f["M"]
        Y, N, A = f["votes"]
        P = sum(f["votes"])
        q = {"majority": 2 * P > M, "third": 3 * P >= M, "fixed": P >= f["qn"]}[f["q"]]
        if not q:
            return "no valid vote (no quorum)"
        ok = {"cast": Y - N >= 1, "present": 2 * Y > P, "two_thirds": 3 * Y >= 2 * (Y + N) and Y + N > 0, "members": 2 * Y > M}[f["rule"]]
        return "passed" if ok else "failed"

    def catv(self, f):
        return self.outcome(f)

    def catv2(self, f):
        return self.outcome2(f)

    def preds(self, f):
        return {"pass": self.outcome(f) == "passed"}

    def preds2(self, f):
        return {"pass": self.outcome2(f) == "passed"}

    preds_list = ("pass",)

    def valid(self, f):
        return min(f["votes"]) >= 0 and 0 < sum(f["votes"]) <= f["M"] and 1 <= f["qn"] <= f["M"]

    def alts(self, f):
        # one fact: move one vote between groups (P fixed), or change who attends, or the rule
        out = {"rule": [r for r in ("cast", "present", "two_thirds", "members") if r != f["rule"]],
               "q": [q for q in ("majority", "third", "fixed") if q != f["q"]]}
        return out

    def flip(self, f, rng, want, keys=None):
        g = super().flip(f, rng, want, keys)
        if g is not None:
            return g
        # vote moves change two counts at once; express them as a single 'votes' fact change
        moves = []
        for a, b in ((0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)):
            for k in (1, 2):
                v = list(f["votes"])
                v[a] -= k
                v[b] += k
                moves.append(dict(f, votes=v))
        for d in (1, 2, -1, -2):  # extra attendees who abstain / abstainers who stayed away
            v = list(f["votes"])
            v[2] += d
            moves.append(dict(f, votes=v))
        rng.shuffle(moves)
        for g in moves:
            if self.valid(g) and want(g):
                return g
        return None

    def edges(self, f, p):
        t = ["numeric", "quantifier"]
        if f["votes"][2]:
            t.append("exception")
        return t

    def render(self, f):
        st = Sty(f)
        M = f["M"]
        qtxt = {"majority": "A quorum is a majority of all members (more than half).", "third": "A quorum is at least one third of all members.",
                "fixed": f"A quorum is {f['qn']} members present."}[f["q"]]
        rtxt = {"cast": "A motion passes if more members vote in favour than against. Abstentions are not counted as votes cast.",
                "present": "A motion passes only if more than half of the members present vote in favour; an abstention therefore has the same effect as a vote against.",
                "two_thirds": "A motion passes if at least two thirds of the votes cast are in favour. Abstentions are not votes cast.",
                "members": "A motion passes only if more than half of ALL members (not just those present) vote in favour."}[f["rule"]]
        body = f["body"]
        pol = f"{f['org']} Residents' {cap(body)} - bylaws, section 7\n- The {body} has {M} members.\n- {qtxt}\n- {rtxt}\n- The chair votes like any other member."
        Y, N, A = f["votes"]
        scen = (f"At the meeting, {Y + N + A} members were present. On the motion to approve the budget, {Y} voted in favour, {N} voted against"
                + (f", and {A} abstained." if A else ", and nobody abstained."))
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        return dict(pos=["Did the motion to approve the budget pass?", "Was the budget validly approved under the bylaws?"],
                    neg=["Did the budget fail to be validly approved?", "Was the motion not carried under the bylaws?"],
                    cpos="the motion passed", cneg="the motion did not pass",
                    speakers=[("The secretary's minutes state that", "the secretary"), ("A member argued afterwards that", "that member")])

    def cat_q(self, f):
        return ["What is the result of the vote on the budget under the bylaws?"]


# =============================================================================================================
class TieredBill(Schema):
    """Tiered utility rates from meter readings (usage = current - previous), unit conversion for water."""
    name = "tiered_bill"
    quota = 450
    letter = True
    multi_hop = True

    def sample(self, rng):
        kind = rng.choice(["water", "power"])
        if kind == "water":
            tiers = [(rng.choice([5, 6, 8]), rng.choice([285, 310, 350])), (rng.choice([10, 12]), rng.choice([420, 465, 510])), (None, rng.choice([640, 700, 785]))]
            fixed = rng.choice([1250, 1800, 2200])
            use = rng.randint(3, 30)
        else:
            tiers = [(rng.choice([300, 400, 500]), rng.choice([12, 14, 15])), (rng.choice([400, 600]), rng.choice([18, 21, 23])), (None, rng.choice([27, 31, 34]))]
            fixed = rng.choice([900, 1000, 1500])
            use = rng.randint(200, 1500)
        prev = rng.randint(1000, 90000)
        f = {"kind": kind, "who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "tiers": [list(t) for t in tiers],
             "fixed": fixed, "prev": prev, "cur": prev + use}
        b = self.bill(f)
        f["budget"] = max(100, b + rng.choice([0, 0, 1, -1, 50, -50, 500, -500]))
        return f

    def bill(self, f):
        use = f["cur"] - f["prev"]
        tot = Fr(f["fixed"])
        left = use
        for size, rate in f["tiers"]:
            take = left if size is None else min(left, size)
            tot += take * rate if f["kind"] == "water" else Fr(take * rate, 1)
            left -= take
            if left <= 0:
                break
        return cents_round(tot)

    def bill2(self, f):
        use = f["cur"] - f["prev"]
        (s1, r1), (s2, r2), (_, r3) = f["tiers"]
        a = min(use, s1)
        b = min(max(use - s1, 0), s2)
        c = max(use - s1 - s2, 0)
        return int(Decimal(f["fixed"]) + Decimal(a * r1 + b * r2 + c * r3))

    def valid(self, f):
        return f["cur"] > f["prev"]

    def preds(self, f):
        return {"ok": self.bill(f) <= f["budget"]}

    def preds2(self, f):
        return {"ok": not (self.bill2(f) > f["budget"])}

    def val(self, f):
        return self.bill(f)

    def val2(self, f):
        return self.bill2(f)

    def fmtv(self, f, v):
        return money(v)

    def wrongs(self, f):
        use = f["cur"] - f["prev"]
        (s1, r1), (s2, r2), (_, r3) = f["tiers"]
        top = r1 if use <= s1 else r2 if use <= s1 + s2 else r3
        return [f["fixed"] + use * top, self.bill(f) - f["fixed"], f["fixed"] + f["cur"] * r1 if f["cur"] * r1 < 10 ** 7 else self.bill(f) + 100,
                self.bill(dict(f, cur=f["cur"] + 1)), self.bill(dict(f, cur=f["cur"] - 1))]

    def alts(self, f):
        return {"cur": [f["cur"] + d for d in (-1, 1, -2, 2, -5, 5)], "budget": [f["budget"] + d for d in (-1, 1, -100, 100, -500, 500)],
                "fixed": [f["fixed"] - 100, f["fixed"] + 100]}

    def edges(self, f, p):
        return ["numeric", "units"]

    def render(self, f):
        st = Sty(f)
        (s1, r1), (s2, r2), (_, r3) = f["tiers"]
        if f["kind"] == "water":
            u = "units (1 unit = 100 cubic feet = 748 gallons)"
            pol = (f"{f['org']} Water Utility - residential rates\n- Monthly service charge: {money(f['fixed'])}\n- Tier 1: the first {s1} units at {money(r1)} per unit\n"
                   f"- Tier 2: the next {s2} units at {money(r2)} per unit\n- Tier 3: every unit above {s1 + s2} at {money(r3)} per unit\n- Usage is billed in whole {u}; usage = current reading minus previous reading.")
            scen = f"{f['who'][0]}'s meter read {f['prev']:,} units last month and {f['cur']:,} units this month. {cap(f['who'][1])} budgeted {money(f['budget'])} for this month's water bill."
        else:
            pol = (f"{f['org']} Electric Cooperative - residential tariff\n- Basic charge: {money(f['fixed'])} per month\n- First {s1} kWh: {r1} cents per kWh\n"
                   f"- Next {s2} kWh: {r2} cents per kWh\n- All kWh above {s1 + s2}: {r3} cents per kWh\n- Usage = current meter reading minus previous reading. Taxes are billed separately.")
            scen = f"{f['who'][0]}'s meter showed {f['prev']:,} kWh at the previous reading and {f['cur']:,} kWh at this reading. {cap(f['who'][1])} budgeted {money(f['budget'])} for this bill before taxes."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Will the bill fit within {who}'s budget?", f"Is this bill at or below the amount {who} budgeted?"],
                    neg=[f"Will the bill be higher than {who} budgeted?", f"Does the bill exceed {who}'s budget?"],
                    cpos="the bill fits within the budget", cneg="the bill exceeds the budget",
                    speakers=[(f"{who}'s housemate estimated that", "the housemate")])

    def letter_q(self, f):
        return ["What is the amount of this bill (before any taxes)?"]


# =============================================================================================================
class ParkingFee(Schema):
    """Free period, per started hour (whole stay or after the free period), daily maximum; receipt check."""
    name = "parking_fee"
    quota = 450
    letter = True

    def sample(self, rng):
        free = rng.choice([0, 15, 30, 60])
        unit = rng.choice([60, 60, 30])
        rate = rng.choice([150, 200, 250, 300, 350, 400]) if unit == 60 else rng.choice([100, 125, 150])
        cap_ = rng.choice([1200, 1500, 2000, 2500, None])
        basis = rng.choice(["whole", "after"])
        t_in = rng.randrange(420, 1200)
        dur = rng.choice([free, free + 1, unit, unit + 1, 2 * unit, 2 * unit + 1, 3 * unit - 1, free + unit, free + unit + 1,
                          rng.randint(20, 600)])
        dur = max(1, dur)
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "free": free, "unit": unit, "rate": rate,
             "cap": cap_, "basis": basis, "in": t_in, "out": t_in + dur}
        fee = self.fee(f)
        f["rcpt"] = max(0, fee + rng.choice([0, 0, 0, rate, -rate, 50, -50]))
        return f

    def fee(self, f):
        d = f["out"] - f["in"]
        if d <= f["free"]:
            return 0
        chg = d if f["basis"] == "whole" else d - f["free"]
        units = -(-chg // f["unit"])
        x = units * f["rate"]
        return min(x, f["cap"]) if f["cap"] else x

    def fee2(self, f):
        a = dt.datetime(2000, 1, 1) + dt.timedelta(minutes=f["in"])
        b = dt.datetime(2000, 1, 1) + dt.timedelta(minutes=f["out"])
        mins = (b - a).total_seconds() / 60
        if mins <= f["free"]:
            return 0
        chg = mins if f["basis"] == "whole" else mins - f["free"]
        units = 0
        while units * f["unit"] < chg:
            units += 1
        x = units * f["rate"]
        return x if not f["cap"] or x < f["cap"] else f["cap"]

    def valid(self, f):
        return 0 <= f["in"] < f["out"] < 1440 and f["rcpt"] >= 0

    def preds(self, f):
        return {"ok": f["rcpt"] == self.fee(f)}

    def preds2(self, f):
        return {"ok": f["rcpt"] == self.fee2(f)}

    def val(self, f):
        return self.fee(f)

    def val2(self, f):
        return self.fee2(f)

    def fmtv(self, f, v):
        return money(v)

    def wrongs(self, f):
        d = f["out"] - f["in"]
        other = dict(f, basis="after" if f["basis"] == "whole" else "whole")
        return [self.fee(other), (d // f["unit"]) * f["rate"], self.fee(f) + f["rate"], self.fee(dict(f, cap=None)), -(-d // f["unit"]) * f["rate"]]

    def alts(self, f):
        return {"out": [f["out"] + d for d in (-1, 1, -2, 2, -30, 30)], "rcpt": [f["rcpt"] + d for d in (-f["rate"], f["rate"], -50, 50)],
                "basis": ["after" if f["basis"] == "whole" else "whole"], "free": [x for x in (0, 15, 30, 60) if x != f["free"]]}

    def edges(self, f, p):
        return ["numeric", "temporal"]

    def render(self, f):
        st = Sty(f)
        ts = st.i("ts", 3)
        u = "hour" if f["unit"] == 60 else "30 minutes"
        free = (f"The first {f['free']} minutes are free." if f["free"] else "There is no free period.")
        basis = ("If you stay longer than the free period, every started " + u + " of the whole stay is charged, counted from entry."
                 if f["basis"] == "whole" else
                 "If you stay longer than the free period, only the time after the free period is charged, per started " + u + ".")
        cap_ = (f" Maximum charge per day: {money(f['cap'])}." if f["cap"] else " There is no daily maximum.")
        pol = f"{f['org']} Station Car Park - tariff\n- {free}\n- {basis}\n- Rate: {money(f['rate'])} per {'started hour' if f['unit'] == 60 else 'started 30 minutes'}.{cap_}\n- " + ("Lost tickets are charged the daily maximum." if f["cap"] else "Lost tickets are charged a flat fee of $30.00.")
        scen = f"{f['who'][0]} entered at {ft(f['in'], ts)} and left at {ft(f['out'], ts)} the same day. The machine charged {money(f['rcpt'])}."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Did the machine charge {who} the correct amount under the tariff?", "Is the amount charged consistent with the tariff?"],
                    neg=[f"Was {who} charged the wrong amount?"],
                    cpos="the machine charged the correct amount", cneg="the machine charged the wrong amount",
                    speakers=[(f"The car park attendant told {f['who'][2]} that", "the attendant")])

    def letter_q(self, f):
        return [f"How much should {f['who'][0]} have been charged under the tariff?"]


# =============================================================================================================
class LatePenalty(Schema):
    """Marks deducted per started 24 hours late (or per calendar day), cap after which the mark is zero; pass mark."""
    name = "late_penalty"
    quota = 450
    letter = True
    multi_hop = True

    def sample(self, rng):
        mx = rng.choice([40, 50, 60, 80, 100])
        pen = rng.choice([5, 10, 10, 20])
        yr = rng.choice([2025, 2026, 2027])
        due = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        due_t = rng.choice([1439, 1020, 720, 540])
        late = rng.choice([0, 1, 2, 3, 5, 7, 10, 25, 23, 47, 49, 71, 73, 24 * 60 + 1, 24 * 60, 48 * 60, 48 * 60 + 1, 72 * 60 + 1, rng.randint(1, 8000)])
        s = due.toordinal() * 1440 + due_t + late
        pm = rng.choice([40, 50])
        raw = rng.randrange(int(mx * 0.3) * 2, mx * 2 + 1) / 2
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "mx": mx, "pen": pen, "due": iso(due),
             "due_t": due_t, "sd": iso(dt.date.fromordinal(s // 1440)), "st": s % 1440, "pm": pm, "raw2": int(raw * 2),
             "maxd": rng.choice([3, 5, 7])}
        return f

    def days_late(self, f):
        m = (D(f["sd"]).toordinal() * 1440 + f["st"]) - (D(f["due"]).toordinal() * 1440 + f["due_t"])
        return 0 if m <= 0 else -(-m // 1440)

    def days_late2(self, f):
        a = dt.datetime.combine(D(f["due"]), dt.time(f["due_t"] // 60, f["due_t"] % 60))
        b = dt.datetime.combine(D(f["sd"]), dt.time(f["st"] // 60, f["st"] % 60))
        if b <= a:
            return 0
        k = 0
        while a + dt.timedelta(days=k) < b:
            k += 1
        return k

    def mark(self, f, dl):
        raw = Fr(f["raw2"], 2)
        if dl > f["maxd"]:
            return Fr(0)
        return max(Fr(0), raw - Fr(f["pen"] * f["mx"], 100) * dl)

    def valid(self, f):
        return 0 <= f["st"] < 1440 and 0 <= f["raw2"] <= 2 * f["mx"]

    def preds(self, f):
        return {"ok": self.mark(f, self.days_late(f)) >= Fr(f["pm"] * f["mx"], 100)}

    def preds2(self, f):
        m = self.mark(f, self.days_late2(f))
        return {"ok": not (m * 100 < f["pm"] * f["mx"])}

    def val(self, f):
        return self.mark(f, self.days_late(f))

    def val2(self, f):
        return self.mark(f, self.days_late2(f))

    def fmtv(self, f, v):
        return f"{ftrim(Fr(v), 2)} out of {f['mx']}"

    def wrongs(self, f):
        dl = self.days_late(f)
        raw = Fr(f["raw2"], 2)
        out = [self.mark(f, max(0, dl - 1)), self.mark(f, dl + 1), max(Fr(0), raw * (1 - Fr(f["pen"] * dl, 100))),
               max(Fr(0), raw - f["pen"] * dl), raw]
        return [x for x in out if (x * 100).denominator == 1]

    def alts(self, f):
        return {"st": [x for x in (f["st"] - 1, f["st"] + 1, f["st"] - 60, f["st"] + 60) if 0 <= x < 1440],
                "sd": [add_days(f["sd"], k) for k in (-1, 1)], "raw2": [f["raw2"] + d for d in (-1, 1, -2, 2, -10, 10)],
                "pen": [p for p in (5, 10, 20) if p != f["pen"]], "maxd": [f["maxd"] - 1, f["maxd"] + 1]}

    def edges(self, f, p):
        return ["numeric", "temporal"]

    def render(self, f):
        st = Sty(f)
        ds, ts = st.i("ds", 3), st.i("ts", 3)
        pol = (f"{f['org']} School of Business - late submission policy\n- Assignments are due at {ft(f['due_t'], ts)} on the due date. Work submitted after that time loses {f['pen']}% of the maximum mark for each 24-hour period, or part of one, that it is late.\n"
               f"- Work more than {f['maxd']} days (that is, {f['maxd'] * 24} hours) late receives a mark of zero.\n- The pass mark is {f['pm']}% of the maximum mark.")
        raw = ftrim(Fr(f["raw2"], 2), 1)
        scen = (f"{f['who'][0]}'s assignment, marked out of {f['mx']}, was due on {fd(f['due'], ds, wd=True)}. It was submitted at {ft(f['st'], ts)} on {fd(f['sd'], ds, wd=True)} "
                f"and earned {raw} marks before any late penalty.")
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Does {who} pass the assignment after any late penalty?", f"Is {who}'s final mark at or above the pass mark?"],
                    neg=[f"Does {who} fail the assignment once the late policy is applied?", f"Is {who}'s final mark below the pass mark?"],
                    cpos=f"{who} passes the assignment", cneg=f"{who} fails the assignment",
                    speakers=[("A teaching assistant told " + f["who"][2] + " that", "the teaching assistant")])

    def letter_q(self, f):
        return [f"What is {f['who'][0]}'s final mark after the late policy is applied?"]
