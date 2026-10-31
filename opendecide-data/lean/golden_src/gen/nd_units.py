"""gen_numeric_dates schemas, part 4: dosing, units, sports, HR, finance, fines, refunds."""
import calendar
import datetime as dt
from decimal import Decimal, localcontext
from fractions import Fraction as Fr

import numpy as np

from nd_common import (V, MONTHS, PLACES, WEEKDAYS, D, Schema, Sty, add_days, add_months, cap, dec, drnd, dur_words, fd,
                       fdec, fdm, ft, ftrim, iso, isleap, money, month_end, ordn, person, plural, rnd)
from nd_money import cents_round, dcents
from nd_time import age_on, attain2

LAB = ["Situation: ", "Case: ", "", "Facts: "]


# =============================================================================================================
class DosePerKg(Schema):
    """Weight-based dose with a per-dose cap; weight possibly in pounds (stated factor, stated rounding)."""
    name = "dose_per_kg"
    quota = 600
    letter = True
    multi_hop = True
    units = True
    hide_keys = {"ok": ["w10"]}
    DRUGS = [("paracetamol", 15, 1000, [120, 250]), ("acetaminophen", 15, 1000, [160]), ("ibuprofen", 10, 400, [100, 200]),
             ("amoxicillin", 25, 1000, [125, 250]), ("cefalexin", 12, 500, [125, 250])]

    def sample(self, rng):
        dname, rate, capmg, concs = rng.choice(self.DRUGS)
        conc = rng.choice(concs)
        unit = rng.choice(["kg", "lb", "lb"])
        kg10 = rng.randint(80, 700)  # tenths of kg
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "drug": dname, "rate": rate,
             "cap": capmg, "conc": conc, "unit": unit}
        if unit == "kg":
            f["w10"] = kg10
        else:
            f["w10"] = int(Fr(kg10, 10) * Fr(22, 10) * 10)  # tenths of lb
        mx = self.maxmg(f)
        ml = mx * 5 / conc
        ml10 = int(ml * 10) + rng.choice([0, 0, 1, -1, 2, -2, 5, -5, 10])
        f["ml10"] = max(1, ml10)
        return f

    def kg(self, f):
        if f["unit"] == "kg":
            return Fr(f["w10"], 10)
        return rnd(Fr(f["w10"], 10) / Fr(22, 10), 1, "down")

    def maxmg(self, f):
        return min(f["rate"] * self.kg(f), Fr(f["cap"]))

    def kg2(self, f):
        if f["unit"] == "kg":
            return Decimal(f["w10"]) / 10
        with localcontext() as c:
            c.prec = 40
            return drnd(Decimal(f["w10"]) / 10 / Decimal("2.2"), 1, "down")

    def maxmg2(self, f):
        a = Decimal(f["rate"]) * self.kg2(f)
        return a if a < Decimal(f["cap"]) else Decimal(f["cap"])

    def valid(self, f):
        return (f["w10"] is None or f["w10"] > 0) and f["ml10"] > 0

    def preds(self, f):
        mg = Fr(f["ml10"], 10) * f["conc"] / 5
        if f["w10"] is None:  # weight unknown: only an order above the absolute cap is decidable
            return {"ok": False if mg > f["cap"] else None}
        return {"ok": mg <= self.maxmg(f)}

    def preds2(self, f):
        mg = Decimal(f["ml10"]) / 10 * Decimal(f["conc"]) / 5
        if f["w10"] is None:
            return {"ok": None if not (mg > f["cap"]) else False}
        return {"ok": not (mg > self.maxmg2(f))}

    def val(self, f):
        if f["w10"] is None:
            return None
        return rnd(self.maxmg(f) * 5 / f["conc"], 1, "down")

    def val2(self, f):
        if f["w10"] is None:
            return None
        return Fr(drnd(self.maxmg2(f) * 5 / Decimal(f["conc"]), 1, "down"))

    def fmtv(self, f, v):
        return f"{fdec(v, 1)} mL"

    def wrongs(self, f):
        w = Fr(f["w10"], 10)
        out = [rnd(min(f["rate"] * w, Fr(f["cap"])) * 5 / f["conc"], 1, "down"),          # used pounds as kilograms
               rnd(f["rate"] * self.kg(f) * 5 / f["conc"], 1, "down"),                     # ignored the per-dose cap
               rnd(self.maxmg(f) * 5 / f["conc"], 1, "ceil"),
               rnd(self.maxmg(f) / f["conc"], 1, "down"),                                   # forgot the 5 mL
               rnd(min(f["rate"] * w * Fr(22, 10), Fr(f["cap"])) * 5 / f["conc"], 1, "down")]
        return out

    def alts(self, f):
        if f["w10"] is None:
            return {}
        return {"ml10": [f["ml10"] + d for d in (-1, 1, -2, 2, -5, 5, -10, 10)], "w10": [f["w10"] + d for d in (-1, 1, -5, 5, -10, 10)],
                "conc": [c for c in (100, 120, 125, 160, 200, 250) if c != f["conc"]][:3], "unit": ["kg" if f["unit"] == "lb" else "lb"]}

    def edges(self, f, p):
        t = ["numeric", "units"]
        if f["w10"] is None:
            return t + ["missing_info"]
        if self.maxmg(f) == f["cap"]:
            t.append("exception")
        return t

    def render(self, f):
        st = Sty(f)
        wt = None if f["w10"] is None else (f"{ftrim(Fr(f['w10'], 10), 1)} kg" if f["unit"] == "kg" else f"{ftrim(Fr(f['w10'], 10), 1)} lb")
        conv = ("\n- If weight is recorded in pounds, convert with 1 kg = 2.2 lb and round the result DOWN to one decimal place of a kilogram before calculating."
                if f["unit"] == "lb" or st.p("cv", 0.4) else "")
        pol = (f"{f['org']} Children's Hospital - ward dosing protocol: oral {f['drug']}\n- Single dose: {f['rate']} mg per kg of body weight, but never more than {f['cap']:,} mg in one dose.{conv}\n"
               f"- Oral suspension strength on this ward: {f['conc']} mg per 5 mL.\n- An ordered dose may be given only if it does not exceed the protocol maximum for a single dose.")
        wtxt = (f"weighs {wt}" if wt else "has not been weighed on this admission, and no current weight is recorded")
        scen = f"{f['who'][0]}, a child on the ward, {wtxt}. The order is for {ftrim(Fr(f['ml10'], 10), 1)} mL of the {f['conc']} mg/5 mL suspension as a single dose."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=["Is the ordered dose within the protocol maximum for a single dose?", "May the nurse give the ordered dose under this protocol?"],
                    neg=["Does the ordered dose exceed the protocol maximum for a single dose?", "Must the nurse query the order because the dose is too high?"],
                    cpos="the ordered dose is within the protocol maximum", cneg="the ordered dose is above the protocol maximum",
                    speakers=[("A student nurse told the charge nurse that", "the student nurse"), (f"{who}'s parent was told by a pharmacist that", "the pharmacist")])

    def letter_q(self, f):
        return ["Under the protocol, what is the largest volume of suspension (rounded down to 0.1 mL) that may be given as one dose?"]


# =============================================================================================================
class DoseTiming(Schema):
    """Minimum interval since the last dose and a rolling 24-hour dose limit."""
    name = "dose_timing"
    quota = 450
    multi_hop = True

    def sample(self, rng):
        H = rng.choice([4, 4, 6, 8])
        K = rng.choice([3, 4, 4])
        n = rng.randint(2, K + 1)
        start = rng.randrange(0, 1440, 15)
        times = []
        t = start
        for _ in range(n):
            times.append(t)
            t += H * 60 + rng.choice([0, 0, 15, 30, 60, 120])
        nxt = times[-1] + H * 60 + rng.choice([0, 0, -1, -15, 15, -30, 60])
        return {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "H": H, "K": K,
                "hist": times, "nxt": nxt, "drug": rng.choice(["paracetamol", "ibuprofen", "the pain reliever"])}

    def preds(self, f):
        last = max(f["hist"])
        ok1 = f["nxt"] - last >= f["H"] * 60
        cnt = sum(1 for t in f["hist"] if f["nxt"] - 1440 < t <= f["nxt"]) + 1
        return {"ok": ok1 and cnt <= f["K"]}

    def preds2(self, f):
        base = dt.datetime(2026, 1, 1)
        nxt = base + dt.timedelta(minutes=f["nxt"])
        ds = [base + dt.timedelta(minutes=t) for t in f["hist"]]
        if any((nxt - d) < dt.timedelta(hours=f["H"]) for d in ds):
            return {"ok": False}
        window = [d for d in ds if dt.timedelta(0) <= nxt - d < dt.timedelta(hours=24)]
        return {"ok": len(window) + 1 <= f["K"]}

    def valid(self, f):
        return f["nxt"] > max(f["hist"]) and sorted(f["hist"]) == f["hist"] and len(set(f["hist"])) == len(f["hist"])

    def alts(self, f):
        h = f["hist"]
        hs = []
        for i in range(len(h)):
            for d in (-60, 60, -30, 30, -120, 120):
                z = list(h)
                z[i] += d
                hs.append(z)
        if len(h) > 1:
            hs.append(h[1:])
        return {"nxt": [f["nxt"] + d for d in (-1, 1, -15, 15, -30, 30, -60, 60, 120)], "hist": hs, "K": [f["K"] - 1, f["K"] + 1],
                "H": [x for x in (4, 6, 8) if x != f["H"]]}

    def edges(self, f, p):
        return ["numeric", "temporal", "quantifier"]

    def _when(self, m, st, ref_day):
        day, mm = divmod(m, 1440)
        rel = day - ref_day
        lab = {0: "today", -1: "yesterday", -2: "two days ago"}.get(rel, f"{-rel} days ago")
        return f"{lab} at {ft(mm, st.i('ts', 3))}"

    def render(self, f):
        st = Sty(f)
        ref = f["nxt"] // 1440
        pol = (f"{f['org']} Clinic - home-care medication sheet for {f['drug']}\n- Leave at least {f['H']} hours between doses.\n"
               f"- Never give more than {f['K']} doses in any 24-hour period: counting the new dose, no more than {f['K']} doses may fall within the 24 hours ending at the time of the new dose.\n- Record every dose on this sheet.")
        hist = "; ".join(self._when(t, st, ref) for t in f["hist"])
        scen = (f"The sheet for {f['who'][0]} records doses {hist}. The next dose is planned for {self._when(f['nxt'], st, ref)}.").replace(".m..", ".m.")
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Can the planned dose be given to {who} at that time under the sheet's rules?", "Is the planned dose allowed at the planned time?"],
                    neg=["Would giving the planned dose at that time break the sheet's rules?", "Is the planned dose too early or one too many?"],
                    cpos="the planned dose is allowed at that time", cneg="the planned dose is not allowed at that time",
                    speakers=[(f"{who}'s older sibling said", "the sibling"), ("A home-care nurse said", "the nurse")])


# =============================================================================================================
class Baggage(Schema):
    """Checked-bag weight and linear size limits with pound/inch measurements (stated conversion factors)."""
    name = "baggage"
    quota = 500
    cat = ["within limits", "overweight only", "oversize only", "overweight and oversize"]
    cat_defs = {"within limits": "After converting with the stated factors, the bag's weight and its length + width + height are both at or below the limits.",
                "overweight only": "After converting, the weight is above the weight limit while the summed dimensions are at or below the size limit.",
                "oversize only": "After converting, the summed dimensions are above the size limit while the weight is at or below the weight limit.",
                "overweight and oversize": "After converting, both the weight and the summed dimensions are above their limits."}
    choice_share = 0.35
    units = True
    multi_hop = True

    def sample(self, rng):
        W = rng.choice([23, 23, 32, 20])
        L = rng.choice([158, 158, 203])
        wunit = rng.choice(["lb", "lb", "kg"])
        dunit = rng.choice(["in", "in", "cm"])
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "W": W, "L": L,
             "wunit": wunit, "dunit": dunit}
        # weight near the limit, in tenths of the display unit
        if wunit == "lb":
            b = Fr(W) / Fr(4536, 10000)
            f["w10"] = int(b * 10) + rng.choice([0, 1, -1, 2, -3, 10, -20])
        else:
            f["w10"] = W * 10 + rng.choice([0, 1, -1, 5, -5])
        if dunit == "in":
            tot2 = int(Fr(L) / Fr(254, 100) * 2) + rng.choice([0, 1, -1, 2, -2])  # half inches
        else:
            tot2 = (L + rng.choice([0, 1, -1, 3, -3])) * 2
        a = rng.randint(tot2 // 3, tot2 // 2)
        b_ = rng.randint(tot2 // 6, max(tot2 // 6 + 1, (tot2 - a) // 2))
        c = tot2 - a - b_
        f["dims2"] = sorted([a, b_, c], reverse=True)
        return f

    def kgv(self, f):
        w = Fr(f["w10"], 10)
        return w * Fr(4536, 10000) if f["wunit"] == "lb" else w

    def cmv(self, f):
        s = Fr(sum(f["dims2"]), 2)
        return s * Fr(254, 100) if f["dunit"] == "in" else s

    def catv(self, f):
        ow, os_ = self.kgv(f) > f["W"], self.cmv(f) > f["L"]
        return {(False, False): "within limits", (True, False): "overweight only", (False, True): "oversize only", (True, True): "overweight and oversize"}[(ow, os_)]

    def catv2(self, f):
        w = Decimal(f["w10"]) / 10
        kg = w * Decimal("0.4536") if f["wunit"] == "lb" else w
        s = Decimal(sum(f["dims2"])) / 2
        cm = s * Decimal("2.54") if f["dunit"] == "in" else s
        ow, os_ = kg > f["W"], cm > f["L"]
        return ["within limits", "oversize only", "overweight only", "overweight and oversize"][2 * ow + os_]

    def preds(self, f):
        return {"ok": self.catv(f) == "within limits"}

    def preds2(self, f):
        return {"ok": self.catv2(f) == "within limits"}

    def valid(self, f):
        return f["w10"] > 0 and min(f["dims2"]) > 0

    def alts(self, f):
        ds = []
        for i in range(3):
            for d in (-1, 1, -2, 2, -4, 4):
                z = list(f["dims2"])
                z[i] += d
                ds.append(z)
        return {"w10": [f["w10"] + d for d in (-1, 1, -2, 2, -5, 5, -20, 20)], "dims2": ds, "W": [x for x in (20, 23, 32) if x != f["W"]],
                "L": [x for x in (158, 203) if x != f["L"]]}

    def edges(self, f, p):
        return ["numeric", "units"]

    def render(self, f):
        st = Sty(f)
        pol = (f"{f['org']} Airways - checked baggage (economy)\n- Each checked bag may weigh at most {f['W']} kg.\n"
               f"- The sum of length + width + height may be at most {f['L']} cm, including wheels and handles.\n"
               f"- Conversions used at the airport: 1 lb = 0.4536 kg; 1 inch = 2.54 cm. A bag exactly at a limit is accepted.\n- Excess charges apply separately to weight and to size.")
        w = f"{ftrim(Fr(f['w10'], 10), 1)} {'lb' if f['wunit'] == 'lb' else 'kg'}"
        dims = " x ".join(ftrim(Fr(x, 2), 1) for x in f["dims2"]) + (" inches" if f["dunit"] == "in" else " cm")
        scen = f"{f['who'][0]}'s suitcase weighs {w} on the home scale and measures {dims} (length x width x height, wheels included)."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Is {who}'s suitcase within both the weight and the size limits?", f"Can {who} check the suitcase without any excess charge?"],
                    neg=[f"Will {who} have to pay an excess charge for the suitcase?", f"Does {who}'s suitcase break at least one of the limits?"],
                    cpos="the suitcase is within both limits", cneg="the suitcase breaks at least one limit",
                    speakers=[(f"{who}'s travel companion said", "the companion"), ("An airline agent on the phone said", "the agent")])

    def cat_q(self, f):
        return [f"How should {f['who'][0]}'s suitcase be classified under the baggage rules?"]


# =============================================================================================================
class ColdChain(Schema):
    """Fridge log in Fahrenheit vs a 2-8 degrees Celsius storage range (all readings must be within, inclusive)."""
    name = "cold_chain"
    quota = 450
    units = True
    table = True

    def can_hide(self, p):
        return True

    def hide(self, f, p, rng):
        g = dict(f)
        r = list(f["r10"])
        r[rng.randrange(len(r))] = None
        g["r10"] = r
        return g

    def sample(self, rng):
        n = rng.randint(4, 7)
        lo, hi = rng.choice([(2, 8), (2, 8), (15, 25), (-25, -15)])
        flo, fhi = Fr(lo) * 9 / 5 + 32, Fr(hi) * 9 / 5 + 32
        reads = [int(rng.uniform(float(flo) + 1, float(fhi) - 1) * 10) for _ in range(n)]
        i = rng.randrange(n)
        edge = rng.choice([flo, fhi])
        reads[i] = int(edge * 10) + rng.choice([0, 0, 1, -1, 2, -2])
        start = rng.choice([0, 360, 480])
        step = rng.choice([120, 180, 240])
        prod, unit = {(2, 8): (rng.choice(["vaccines", "insulin stock", "biologic medicines"]), "fridge"),
                      (15, 25): (rng.choice(["tablet stock", "room-temperature medicines"]), "storeroom"),
                      (-25, -15): (rng.choice(["frozen vaccine stock", "frozen plasma"]), "freezer")}[(lo, hi)]
        return {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "lo": lo, "hi": hi,
                "r10": reads, "start": start, "step": step, "prod": prod, "unit": unit}

    def cvals(self, f):
        return [None if r is None else (Fr(r, 10) - 32) * 5 / 9 for r in f["r10"]]

    def preds(self, f):
        cs = self.cvals(f)
        if any(c is not None and not (f["lo"] <= c <= f["hi"]) for c in cs):
            return {"ok": False}
        return {"ok": None if None in cs else True}

    def preds2(self, f):
        # compare in Fahrenheit tenths directly: lo*9/5+32 <= F <= hi*9/5+32  <=>  (lo*18+320) <= F10 ... scaled by 10
        ok, unk = True, False
        for r in f["r10"]:
            if r is None:
                unk = True
            elif not (f["lo"] * 18 + 320 <= r <= f["hi"] * 18 + 320):
                ok = False
        return {"ok": False if not ok else (None if unk else True)}

    def valid(self, f):
        return len(f["r10"]) >= 3

    def alts(self, f):
        rs = []
        for i in range(len(f["r10"])):
            if f["r10"][i] is None:
                continue
            for d in (-1, 1, -2, 2, -10, 10):
                z = list(f["r10"])
                z[i] += d
                rs.append(z)
        return {"r10": rs}

    def edges(self, f, p):
        return ["numeric", "units", "quantifier", "table"] + (["missing_info"] if None in f["r10"] else [])

    def render(self, f):
        st = Sty(f)
        ts = st.i("ts", 3)
        pol = (f"{f['org']} Health Centre - cold storage SOP\n- {cap(f['prod'])} must be stored between {f['lo']} °C and {f['hi']} °C inclusive at all times.\n"
               f"- The {f['unit']} logger records in degrees Fahrenheit; convert with °C = (°F - 32) x 5/9.\n"
               f"- If ANY logged reading is outside the range, the stock must be quarantined and the manufacturer contacted.")
        rows = "\n".join(f"{ft(f['start'] + i * f['step'], ts)} | " + ("no reading (logger error)" if r is None else f"{ftrim(Fr(r, 10), 1)} °F")
                         for i, r in enumerate(f["r10"]))
        scen = f"{f['who'][0]} downloads today's log for the {f['prod']} {f['unit']} (time | reading):\n{rows}"
        return f"{pol}\n\n{st.c('lab', ['', 'Log check: ', 'Situation: '])}{scen}"

    def pq(self, f, p):
        return dict(pos=["Were all of today's readings within the required range?", f"Can the {f['prod']} stay in use without quarantine based on today's log?"],
                    neg=[f"Must the {f['prod']} be quarantined because of today's log?", "Was at least one reading outside the required range?"],
                    cpos="every reading was within the range", cneg="at least one reading was outside the range",
                    speakers=[("The pharmacy technician reported that", "the technician"), ("A colleague glancing at the log said", "the colleague")])


# =============================================================================================================
class SpeedTicket(Schema):
    """Enforcement threshold 'limit + 10% + 2' with the measured speed in the other unit (1 mile = 1.609344 km)."""
    name = "speed_ticket"
    quota = 400
    units = True

    def sample(self, rng):
        lu = rng.choice(["mph", "mph", "kmh"])
        L = rng.choice([20, 25, 30, 40, 50, 60, 70]) if lu == "mph" else rng.choice([30, 50, 60, 80, 100, 110, 120])
        thr = Fr(L) * Fr(11, 10) + 2
        # measured speed in the other unit, integer
        other = thr * Fr(1609344, 10 ** 6) if lu == "mph" else thr / Fr(1609344, 10 ** 6)
        v = int(other) + rng.choice([0, 1, -1, 2, -2, 5, -5])
        return {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "lu": lu, "L": L, "v": v,
                "pct": 10, "add": 2}

    def speed_in_limit_units(self, f):
        k = Fr(1609344, 10 ** 6)
        return Fr(f["v"]) / k if f["lu"] == "mph" else Fr(f["v"]) * k

    def preds(self, f):
        thr = Fr(f["L"]) * (100 + f["pct"]) / 100 + f["add"]
        return {"ticket": self.speed_in_limit_units(f) > thr}

    def preds2(self, f):
        k = Decimal("1.609344")
        thr = Decimal(f["L"]) * Decimal(100 + f["pct"]) / Decimal(100) + Decimal(f["add"])
        # compare in the measured unit to avoid division
        return {"ticket": (Decimal(f["v"]) > thr * k) if f["lu"] == "mph" else (Decimal(f["v"]) * k > thr)}

    preds_list = ("ticket",)

    def valid(self, f):
        return f["v"] > 0

    def alts(self, f):
        return {"v": [f["v"] + d for d in (-1, 1, -2, 2, -3, 3)], "add": [0, 1, 3], "pct": [5, 15]}

    def edges(self, f, p):
        return ["numeric", "units"]

    def render(self, f):
        st = Sty(f)
        u = "mph" if f["lu"] == "mph" else "km/h"
        ou = "km/h" if f["lu"] == "mph" else "mph"
        add = f" plus {f['add']} {u}" if f["add"] else ""
        pol = (f"{f['org']} Police - speed enforcement guidance\n- On the road in question the limit is {f['L']} {u}.\n"
               f"- A ticket is issued only when the measured speed is MORE than the limit plus {f['pct']}% of the limit{add}.\n"
               f"- Speeds recorded in other units are converted with 1 mile = 1.609344 km before the comparison.")
        dev = st.c("dev", ["The officer's radar, set to", "The rental car's speedometer, which reads in", "The camera, which records in"])
        scen = f"{dev} {ou}, showed {f['who'][0]}'s car at {f['v']} {ou} on that road."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Should {who} receive a ticket under the guidance?", f"Is {who}'s measured speed above the ticketing threshold?"],
                    neg=[f"Should {who} be let off without a ticket under the guidance?", f"Is {who}'s speed at or below the ticketing threshold?"],
                    cpos=f"{who} should be ticketed", cneg=f"{who} should not be ticketed",
                    speakers=[(f"{who}'s passenger said", "the passenger"), ("A traffic lawyer told " + f["who"][2] + " that", "the lawyer")])


# =============================================================================================================
class RideHeight(Schema):
    """Height requirement given in inches with a rounded centimetre figure; which unit is official decides."""
    name = "ride_height"
    quota = 350
    units = True

    def sample(self, rng):
        N = rng.choice([36, 40, 42, 44, 46, 48, 52, 54])
        exact_cm = Fr(N) * Fr(254, 100)
        rcm = int(rnd(exact_cm, 0, "half_up"))
        lo, hi = sorted([exact_cm, Fr(rcm)])
        mm = rng.choice([int(lo * 10), int(hi * 10), int(lo * 10) + 1, int(hi * 10) - 1, int(lo * 10) - 1, int(hi * 10) + 1,
                         int((lo + hi) * 5)])
        return {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "N": N, "rcm": rcm,
                "off": rng.choice(["in", "cm"]), "h10": mm, "ride": rng.choice(["Thunder Run coaster", "Rapids log flume", "Sky Swing", "Junior Drop tower"])}

    def preds(self, f):
        h = Fr(f["h10"], 10)
        req = Fr(f["N"]) * Fr(254, 100) if f["off"] == "in" else Fr(f["rcm"])
        return {"ok": h >= req}

    def preds2(self, f):
        if f["off"] == "in":
            return {"ok": Decimal(f["h10"]) / 10 / Decimal("2.54") >= f["N"]}
        return {"ok": f["h10"] >= f["rcm"] * 10}

    def valid(self, f):
        return f["h10"] > 0

    def alts(self, f):
        return {"h10": [f["h10"] + d for d in (-1, 1, -2, 2, -3, 3)], "off": ["cm" if f["off"] == "in" else "in"]}

    def edges(self, f, p):
        t = ["numeric", "units"]
        h = Fr(f["h10"], 10)
        if (h >= Fr(f["N"]) * Fr(254, 100)) != (h >= f["rcm"]):
            t.append("conflicting_evidence")
        return t

    def render(self, f):
        st = Sty(f)
        off = ("The requirement is set in inches; the centimetre figure on the sign is rounded and for guidance only." if f["off"] == "in" else
               "The requirement is set in centimetres; the inch figure on the sign is given for guidance only.")
        pol = (f"{f['org']} Adventure Park - {f['ride']}\n- Riders must be at least {f['N']} inches ({f['rcm']} cm) tall.\n- {off}\n"
               f"- Height is measured without shoes at the ride entrance (1 inch = 2.54 cm).")
        scen = f"{f['who'][0]} is measured without shoes at {ftrim(Fr(f['h10'], 10), 1)} cm."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Is {who} tall enough to ride?", f"Does {who} meet the ride's height requirement?"],
                    neg=[f"Is {who} too short to ride?", f"Must {who} be turned away at the height check?"],
                    cpos=f"{who} is tall enough", cneg=f"{who} is too short",
                    speakers=[("The ride attendant told the family that", "the attendant"), (f"{who}'s parent said", "the parent")])


# =============================================================================================================
AGE_GROUPS = [(18, 34, 10800), (35, 39, 11100), (40, 44, 11400), (45, 49, 12000), (50, 54, 12300), (55, 59, 12900),
              (60, 64, 13800), (65, 69, 14700), (70, 200, 15600)]


class MarathonQualify(Schema):
    """Qualifying standard by age group (age on race day) and a chip time in h:mm:ss."""
    name = "marathon_qualify"
    quota = 450
    table = True
    multi_hop = True

    def sample(self, rng):
        race = dt.date(rng.choice([2026, 2027, 2028]), rng.choice([4, 10, 11]), rng.randint(1, 28))
        gi = rng.randrange(len(AGE_GROUPS))
        lo = AGE_GROUPS[gi][0]
        # birthday near the group boundary on race day half of the time
        if rng.random() < 0.5 and gi > 0:
            b = race + dt.timedelta(days=rng.choice([0, 1, -1, 2, -2]))
            if b.month == 2 and b.day == 29:
                b += dt.timedelta(days=1)
            dob = dt.date(b.year - lo, b.month, b.day)
        else:
            age = rng.randint(lo, min(AGE_GROUPS[gi][1], 80))
            dob = race - dt.timedelta(days=int(age * 365.25) + rng.randint(1, 300))
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "race": iso(race), "dob": iso(dob),
             "conv": "mar1", "offset": rng.choice([0, 300])}
        std = self.std(f)
        f["t"] = std + rng.choice([0, 0, 1, -1, 30, -30, 59, -60, 300, -300])
        return f

    def std(self, f):
        a = age_on(f["dob"], f["race"], f["conv"])
        for lo, hi, s in AGE_GROUPS:
            if lo <= a <= hi:
                return s - f["offset"]
        return None

    def std2(self, f):
        prev = None
        for lo, hi, s in AGE_GROUPS:
            if f["race"] >= attain2(f["dob"], lo, f["conv"]):
                prev = s
        return None if prev is None else prev - f["offset"]

    def valid(self, f):
        return self.std(f) is not None and f["t"] > 3600

    def preds(self, f):
        return {"ok": f["t"] <= self.std(f)}

    def preds2(self, f):
        return {"ok": not (f["t"] > self.std2(f))}

    def alts(self, f):
        return {"t": [f["t"] + d for d in (-1, 1, -2, 2, -60, 60, -300, 300)], "dob": [add_days(f["dob"], d) for d in (-1, 1, -2, 2)],
                "offset": [0 if f["offset"] else 300]}

    def edges(self, f, p):
        return ["numeric", "temporal", "table"]

    def render(self, f):
        st = Sty(f)
        ds = st.i("ds", 3)
        hm = lambda s: f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"
        rows = "\n".join(f"{lo}-{hi} | {hm(s)}" if hi < 200 else f"{lo}+ | {hm(s)}" for lo, hi, s in AGE_GROUPS)
        cut = ("\n- This year every standard is tightened by 5 minutes: subtract 5:00 from the table time." if f["offset"] else "")
        pol = (f"{f['org']} Marathon - qualifying standards\n- Your age group is based on your age on race day ({fd(f['race'], ds)}).\n"
               f"- Your chip time from a certified qualifier must be at or under your group's standard (h:mm:ss).{cut}\n\nAge group | Standard\n{rows}")
        t = f["t"]
        scen = f"{f['who'][0]} was born on {fd(f['dob'], ds)} and ran a certified qualifier with a chip time of {hm(t)}."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Has {who} achieved the qualifying standard?", f"Does {who}'s chip time qualify for the marathon?"],
                    neg=[f"Did {who} miss the qualifying standard?", f"Is {who}'s chip time too slow to qualify?"],
                    cpos=f"{who} qualified", cneg=f"{who} did not qualify",
                    speakers=[("A running-club friend told " + f["who"][2] + " that", "the friend")])


# =============================================================================================================
class WinPct(Schema):
    """Winning percentage with ties counted as half a win; head-to-head tie-breaker."""
    name = "win_pct"
    quota = 400
    letter = True
    multi_hop = True

    def sample(self, rng):
        g = rng.choice([12, 14, 16, 18, 20, 24])
        ra = self._rec(rng, g)
        rb = self._rec(rng, g + rng.choice([0, 0, -1, 1, -2]))
        f = {"org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "a": ra, "b": rb, "h2h": rng.choice(["A", "B", "split"]),
             "ta": rng.choice(["Hawks", "Comets", "Rangers", "Otters", "Pilots"]), "tb": rng.choice(["Falcons", "Tigers", "Miners", "Storm", "Bears"]),
             "who": person(rng)}
        return f

    def _rec(self, rng, g):
        w = rng.randint(g // 3, g - 1)
        t = rng.randint(0, min(3, g - w))
        return [w, g - w - t, t]

    @staticmethod
    def pct(r):
        w, l, t = r
        return (Fr(w) + Fr(t, 2)) / (w + l + t)

    def preds(self, f):
        a, b = self.pct(f["a"]), self.pct(f["b"])
        return {"ok": a > b or (a == b and f["h2h"] == "A")}

    def preds2(self, f):
        (w1, l1, t1), (w2, l2, t2) = f["a"], f["b"]
        lhs = (2 * w1 + t1) * (w2 + l2 + t2)
        rhs = (2 * w2 + t2) * (w1 + l1 + t1)
        return {"ok": lhs > rhs or (lhs == rhs and f["h2h"] == "A")}

    def valid(self, f):
        return all(min(r) >= 0 and sum(r) > 0 for r in (f["a"], f["b"]))

    def val(self, f):
        return rnd(self.pct(f["a"]), 3, "half_up")

    def val2(self, f):
        w, l, t = f["a"]
        return Fr(drnd((Decimal(w) + Decimal(t) / 2) / Decimal(w + l + t), 3, "half_up"))

    def fmtv(self, f, v):
        s = fdec(v, 3)
        return s[1:] if s.startswith("0.") else s

    def wrongs(self, f):
        w, l, t = f["a"]
        out = [rnd(Fr(w, w + l), 3, "half_up") if w + l else None, rnd(Fr(w, w + l + t), 3, "half_up"), rnd(Fr(w + t, w + l + t), 3, "half_up"),
               rnd(Fr(w, w + l + t), 3, "half_up") + Fr(1, 1000)]
        return [x for x in out if x is not None]

    def alts(self, f):
        out = {"h2h": [x for x in ("A", "B", "split") if x != f["h2h"]]}
        for k in ("a", "b"):
            w, l, t = f[k]
            c = []
            for nw, nl, nt in ((w + 1, l - 1, t), (w - 1, l + 1, t), (w, l - 1, t + 1), (w - 1, l, t + 1), (w + 1, l, t - 1), (w, l + 1, t - 1)):
                if min(nw, nl, nt) >= 0:
                    c.append([nw, nl, nt])
            out[k] = c
        return out

    def edges(self, f, p):
        t = ["numeric"]
        if f["a"][2] or f["b"][2]:
            t.append("exception")
        return t

    def render(self, f):
        st = Sty(f)
        h2h = {"A": f"the {f['ta']} won the head-to-head series", "B": f"the {f['tb']} won the head-to-head series",
               "split": "the head-to-head series was split evenly"}[f["h2h"]]
        pol = (f"{f['org']} Youth Hockey League - standings rules\n- Teams are ranked by winning percentage = (wins + half of ties) / games played.\n"
               f"- If two teams have exactly the same percentage, the team that won the head-to-head series ranks higher; if that series was split, both share the place.\n"
               f"- Percentages are shown rounded to three decimals (a fourth decimal of 5 or more rounds up), but ranking uses the exact value.")
        (w1, l1, t1), (w2, l2, t2) = f["a"], f["b"]
        scen = (f"Final records (wins-losses-ties): {f['ta']} {w1}-{l1}-{t1}; {f['tb']} {w2}-{l2}-{t2}. This season {h2h}.")
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        return dict(pos=[f"Do the {f['ta']} rank strictly above the {f['tb']}?", f"Do the {f['ta']} finish ahead of the {f['tb']} in the standings?"],
                    neg=[f"Do the {f['ta']} fail to finish strictly ahead of the {f['tb']}?"],
                    cpos=f"the {f['ta']} rank above the {f['tb']}", cneg=f"the {f['ta']} do not rank above the {f['tb']}",
                    speakers=[("A local sports reporter wrote that", "the reporter"), (f"A {f['tb']} coach claimed that", "the coach")])

    def letter_q(self, f):
        return [f"What winning percentage is shown for the {f['ta']} (to three decimals)?"]


# =============================================================================================================
class FmlaEligibility(Schema):
    """Three cumulative leave-eligibility conditions (service length, hours, worksite size)."""
    name = "leave_eligibility"
    quota = 500
    multi_hop = True
    hide_keys = {"ok": ["hours", "emp"]}

    def sample(self, rng):
        leave = dt.date(rng.choice([2026, 2027, 2028]), rng.randint(1, 12), rng.randint(1, 28))
        m = rng.choice([12, 12, 11, 13, 24])
        hire = D(add_months(iso(leave), -m))
        hire = hire + dt.timedelta(days=rng.choice([0, 0, 1, -1, 3, -3, 20]))
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "hire": iso(hire), "leave": iso(leave),
             "hours": rng.choice([1250, 1249, 1251, 1300, 1100, 1800, 1240]), "emp": rng.choice([50, 49, 51, 120, 35]),
             "reason": rng.choice(["the birth of a child", "a serious health condition", "caring for a parent with a serious illness"])}
        return f

    def _ok(self, f, hours, emp):
        svc = D(f["leave"]) >= D(add_months(f["hire"], 12))
        return svc and hours >= 1250 and emp >= 50

    def preds(self, f):
        hs = [f["hours"]] if f["hours"] is not None else [0, 1249, 1250, 3000]
        es = [f["emp"]] if f["emp"] is not None else [0, 49, 50, 500]
        outs = {self._ok(f, h, e) for h in hs for e in es}
        return {"ok": outs.pop() if len(outs) == 1 else None}

    def preds2(self, f):
        # service: count whole months between hire and leave with a month-stepping loop
        h, l = D(f["hire"]), D(f["leave"])
        y, m, d = h.year, h.month, h.day
        y2, m2 = (y + 1, m)
        last = calendar.monthrange(y2, m2)[1]
        anniv = dt.date(y2, m2, min(d, last))
        svc = l >= anniv
        hs = [f["hours"]] if f["hours"] is not None else [1249, 1250]
        es = [f["emp"]] if f["emp"] is not None else [49, 50]
        outs = {svc and not (x < 1250) and not (e < 50) for x in hs for e in es}
        return {"ok": outs.pop() if len(outs) == 1 else None}

    def valid(self, f):
        return D(f["hire"]) < D(f["leave"]) and f["hire"][5:] != "02-29"

    def alts(self, f):
        return {"hire": [add_days(f["hire"], d) for d in (-1, 1, -3, 3, -30, 30)], "hours": [1249, 1250, 1251, 1200, 1300],
                "emp": [49, 50, 51, 30, 80]}

    def edges(self, f, p):
        t = ["numeric", "temporal", "quantifier"]
        if f["hours"] is None or f["emp"] is None:
            t.append("missing_info")
        return t

    def render(self, f):
        st = Sty(f)
        ds = st.i("ds", 3)
        pol = (f"{f['org']} Manufacturing - family and medical leave policy\nAn employee is eligible for protected leave only if ALL of the following are true on the first day of leave:\n"
               f"1. The employee has worked here for at least 12 months (the first anniversary of the hire date has been reached).\n"
               f"2. The employee worked at least 1,250 hours during the 12 months before the leave starts.\n"
               f"3. At least 50 employees work at or within 75 miles of the employee's worksite.")
        hrs = (f"{f['hours']:,} hours in the 12 months before the leave" if f["hours"] is not None else
               "an hours total for the past 12 months that has not been confirmed yet (the timekeeping export failed)")
        emp = (f"{f['emp']} employees work at or within 75 miles of {f['who'][3]} worksite" if f["emp"] is not None else
               f"the number of employees within 75 miles of {f['who'][3]} worksite has not been checked")
        scen = (f"{f['who'][0]} was hired on {fd(f['hire'], ds)} and asks for leave starting {fd(f['leave'], ds)} for {f['reason']}. "
                f"Payroll shows {hrs}, and {emp}.")
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Is {who} eligible for protected leave under this policy?", f"Does {who} meet all three eligibility conditions?"],
                    neg=[f"Is {who} ineligible for protected leave under this policy?", f"Does {who} fail at least one eligibility condition?"],
                    cpos=f"{who} is eligible for protected leave", cneg=f"{who} is not eligible for protected leave",
                    speakers=[("An HR generalist told " + f["who"][2] + " that", "the HR generalist"), ("A coworker said", "the coworker")])


# =============================================================================================================
class BenefitsStart(Schema):
    """Coverage starts on the first day of the month after the month in which day N of employment falls."""
    name = "benefits_start"
    quota = 400
    letter = True

    def sample(self, rng):
        N = rng.choice([30, 60, 60, 90])
        hire = dt.date(rng.choice([2025, 2026, 2027, 2028]), rng.randint(1, 12), rng.randint(1, 28))
        if rng.random() < 0.4:  # make day N fall on a month's first or last day
            dn = hire + dt.timedelta(days=N - 1)
            tgt = rng.choice([dt.date(dn.year, dn.month, 1), D(month_end(dn.year, dn.month))])
            hire = tgt - dt.timedelta(days=N - 1)
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "N": N, "hire": iso(hire)}
        s = D(self._start(f))
        f["appt"] = iso(s + dt.timedelta(days=rng.choice([0, 0, -1, 1, -2, 5, -20])))
        return f

    def _start(self, f):
        dn = D(f["hire"]) + dt.timedelta(days=f["N"] - 1)
        return iso(dt.date(dn.year + (dn.month == 12), dn.month % 12 + 1, 1))

    def _start2(self, f):
        o = D(f["hire"]).toordinal() + f["N"] - 1
        dn = dt.date.fromordinal(o)
        nxt = D(month_end(dn.year, dn.month)) + dt.timedelta(days=1)
        return iso(nxt)

    def valid(self, f):
        return True

    def preds(self, f):
        return {"ok": f["appt"] >= self._start(f)}

    def preds2(self, f):
        return {"ok": not (D(f["appt"]) < D(self._start2(f)))}

    def val(self, f):
        return self._start(f)

    def val2(self, f):
        return self._start2(f)

    def fmtv(self, f, v):
        return fd(v, Sty(f).i("ds", 3))

    def wrongs(self, f):
        h = D(f["hire"])
        dn = h + dt.timedelta(days=f["N"])
        dn1 = h + dt.timedelta(days=f["N"] - 1)
        out = [iso(dn), iso(dt.date(dn.year + (dn.month == 12), dn.month % 12 + 1, 1)), iso(dt.date(dn1.year, dn1.month, 1)),
               add_months(iso(dt.date(dn1.year, dn1.month, 1)), 2), iso(D(add_months(f["hire"], f["N"] // 30)))]
        return out

    def alts(self, f):
        return {"appt": [add_days(f["appt"], d) for d in (-1, 1, -2, 2)], "hire": [add_days(f["hire"], d) for d in (-1, 1, -2, 2)],
                "N": [n for n in (30, 60, 90) if n != f["N"]]}

    def edges(self, f, p):
        return ["numeric", "temporal"]

    def render(self, f):
        st = Sty(f)
        ds = st.i("ds", 3)
        pol = (f"{f['org']} Logistics - benefits eligibility\n- Health coverage starts on the first day of the month after the month in which the employee completes {f['N']} days of employment.\n"
               f"- The hire date counts as day 1 of employment.\n- Coverage is not retroactive: care received before coverage starts is not covered.")
        scen = f"{f['who'][0]} was hired on {fd(f['hire'], ds)} and has a routine medical appointment on {fd(f['appt'], ds)}."
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Will {who}'s health coverage be in effect on the day of the appointment?", f"Is {who}'s appointment covered by the plan timing?"],
                    neg=[f"Will {who}'s appointment fall before coverage starts?", f"Is {who} still uncovered on the appointment date?"],
                    cpos=f"coverage will be in effect on the appointment date", cneg=f"coverage will not yet be in effect on the appointment date",
                    speakers=[("The onboarding coordinator told " + f["who"][2] + " that", "the coordinator")])

    def letter_q(self, f):
        return [f"On what date does {f['who'][0]}'s health coverage start?"]


# =============================================================================================================
class OvertimeWeekly(Schema):
    """Weekly hours table; overtime above 40 at 1.5x; holiday hours at 2x and excluded from the 40."""
    name = "overtime_weekly"
    quota = 450
    letter = True
    table = True
    multi_hop = True

    def sample(self, rng):
        days = WEEKDAYS[:5] + (["Saturday"] if rng.random() < 0.5 else [])
        target = rng.choice([2400, 2400, 2385, 2415, 2460, 2340, 2520])
        hrs = []
        left = target
        for i, d in enumerate(days):
            if i == len(days) - 1:
                q = left
            else:
                q = rng.choice([420, 450, 480, 495, 510, 540, 360])
            hrs.append(max(0, q))
            left -= q
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "days": days, "mins": hrs,
             "rate": rng.choice([1800, 2050, 2275, 2500, 1640]), "hol": rng.choice([None, None, 0, 3])}
        return f

    def split(self, f):
        hol = f["mins"][f["hol"]] if f["hol"] is not None else 0
        reg = sum(f["mins"]) - hol
        ot = max(0, reg - 2400)
        return reg - ot, ot, hol

    def pay(self, f):
        r, o, h = self.split(f)
        return cents_round(Fr(f["rate"]) * (Fr(r, 60) + Fr(o, 60) * Fr(3, 2) + Fr(h, 60) * 2))

    def pay2(self, f):
        tot = 0
        hol = 0
        for i, m in enumerate(f["mins"]):
            if f["hol"] == i:
                hol += m
            else:
                tot += m
        ot = tot - 2400 if tot > 2400 else 0
        amt = Decimal(f["rate"]) * (Decimal(tot - ot) / 60 + Decimal(ot) / 60 * Decimal("1.5") + Decimal(hol) / 60 * 2)
        return dcents(amt)

    def valid(self, f):
        return all(0 <= m <= 900 for m in f["mins"]) and (f["hol"] is None or f["hol"] < len(f["mins"]))

    def preds(self, f):
        return {"ok": self.split(f)[1] > 0}

    def preds2(self, f):
        tot = sum(m for i, m in enumerate(f["mins"]) if i != f["hol"])
        return {"ok": tot > 2400}

    def val(self, f):
        return self.pay(f)

    def val2(self, f):
        return self.pay2(f)

    def fmtv(self, f, v):
        return money(v)

    def wrongs(self, f):
        tot = sum(f["mins"])
        r = Fr(f["rate"])
        naive = cents_round(r * Fr(tot, 60))
        ot_all = cents_round(r * (Fr(min(tot, 2400), 60) + Fr(max(0, tot - 2400), 60) * Fr(3, 2)))
        return [naive, ot_all, self.pay(f) + cents_round(r / 2), self.pay(dict(f, hol=None))]

    def alts(self, f):
        ms = []
        for i in range(len(f["mins"])):
            for d in (-15, 15, -30, 30, -60, 60):
                z = list(f["mins"])
                z[i] += d
                ms.append(z)
        return {"mins": ms, "hol": [h for h in (None, 0, 3) if h != f["hol"]]}

    def edges(self, f, p):
        t = ["numeric", "table"]
        if f["hol"] is not None:
            t.append("exception")
        return t

    def render(self, f):
        st = Sty(f)
        pol = (f"{f['org']} Retail - pay rules (hourly staff)\n- Hours worked in a workweek beyond 40 are paid at 1.5 times the hourly rate.\n"
               f"- Hours worked on a public holiday are paid at 2 times the hourly rate and do NOT count toward the 40 hours.\n- Hours are recorded in hours and minutes; weekly pay is rounded to the nearest cent (half a cent rounds up).")
        hol = (f" {f['days'][f['hol']]} was a public holiday." if f["hol"] is not None else " There was no public holiday that week.")
        rows = "\n".join(f"{d} | {m // 60}:{m % 60:02d}" for d, m in zip(f["days"], f["mins"]))
        scen = f"{f['who'][0]} earns {money(f['rate'])} per hour. Time worked this week (day | h:mm):\n{rows}\n{hol.strip()}"
        return f"{pol}\n\n{st.c('lab', ['', 'Timesheet: ', 'Situation: '])}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Is {who} owed any overtime at 1.5 times the rate this week?", f"Did {who} work more than 40 countable hours this week?"],
                    neg=[f"Is none of {who}'s time this week paid at the 1.5 overtime rate?"],
                    cpos=f"{who} is owed some 1.5x overtime this week", cneg=f"{who} is not owed any 1.5x overtime this week",
                    speakers=[("The store manager told " + f["who"][2] + " that", "the manager")])

    def letter_q(self, f):
        return [f"What are {f['who'][0]}'s gross earnings for this week?"]


# =============================================================================================================
class GrantBudget(Schema):
    """Indirect-cost cap as a percentage of the right base (direct costs, modified direct costs, or total)."""
    name = "grant_budget"
    quota = 400
    letter = True
    table = True
    multi_hop = True

    def sample(self, rng):
        pers = rng.randrange(40000, 180000, 100) * 100
        fr_ = pers * rng.choice([20, 25, 30]) // 100
        trav = rng.randrange(2000, 15000, 50) * 100
        equip = rng.choice([0, 0, rng.randrange(6000, 60000, 100) * 100])
        sup = rng.randrange(1000, 20000, 50) * 100
        f = {"org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "who": person(rng), "pers": pers, "fr": fr_, "trav": trav,
             "equip": equip, "sup": sup, "p": rng.choice([10, 15, 20, 25]), "base": rng.choice(["tdc", "mtdc", "total"])}
        mx = self.maxind(f)
        f["ind"] = max(0, mx + rng.choice([0, 0, 1, -1, 100, -100, 50000, -50000, f["equip"] * f["p"] // 100]))
        return f

    def maxind(self, f):
        tdc = f["pers"] + f["fr"] + f["trav"] + f["equip"] + f["sup"]
        if f["base"] == "tdc":
            return cents_round(Fr(tdc * f["p"], 100), "down")
        if f["base"] == "mtdc":
            return cents_round(Fr((tdc - f["equip"]) * f["p"], 100), "down")
        # indirect <= p% of (direct + indirect)  <=>  indirect <= p/(100-p) * direct
        return cents_round(Fr(tdc * f["p"], 100 - f["p"]), "down")

    def ok2(self, f):
        tdc = f["pers"] + f["fr"] + f["trav"] + f["equip"] + f["sup"]
        ind = f["ind"]
        if f["base"] == "tdc":
            return ind * 100 <= tdc * f["p"]
        if f["base"] == "mtdc":
            return ind * 100 <= (tdc - f["equip"]) * f["p"]
        return ind * 100 <= (tdc + ind) * f["p"]

    def valid(self, f):
        return f["ind"] >= 0

    def preds(self, f):
        return {"ok": f["ind"] <= self.maxind(f)}

    def preds2(self, f):
        return {"ok": self.ok2(f)}

    def val(self, f):
        return self.maxind(f)

    def val2(self, f):
        tdc = Decimal(f["pers"] + f["fr"] + f["trav"] + f["equip"] + f["sup"])
        p = Decimal(f["p"])
        with localcontext() as c:
            c.prec = 50
            x = {"tdc": tdc * p / 100, "mtdc": (tdc - Decimal(f["equip"])) * p / 100, "total": tdc * p / (100 - p)}[f["base"]]
            return dcents(x, "floor")

    def fmtv(self, f, v):
        return money(v)

    def wrongs(self, f):
        g = lambda b: self.maxind(dict(f, base=b))
        tdc = f["pers"] + f["fr"] + f["trav"] + f["equip"] + f["sup"]
        return [g(b) for b in ("tdc", "mtdc", "total") if b != f["base"]] + [cents_round(Fr((tdc + f["ind"]) * f["p"], 100), "down"),
                                                                             cents_round(Fr(f["pers"] * f["p"], 100), "down")]

    def alts(self, f):
        return {"ind": [f["ind"] + d for d in (-1, 1, -100, 100, -50000, 50000)], "base": [b for b in ("tdc", "mtdc", "total") if b != f["base"]],
                "p": [x for x in (10, 15, 20, 25) if x != f["p"]], "equip": [0] if f["equip"] else [1500000]}

    def edges(self, f, p):
        t = ["numeric", "table"]
        if f["base"] == "mtdc" and f["equip"]:
            t.append("exception")
        return t

    def render(self, f):
        st = Sty(f)
        base = {"tdc": f"{f['p']}% of total direct costs (all direct cost lines, including equipment)",
                "mtdc": f"{f['p']}% of modified total direct costs, which means total direct costs EXCLUDING equipment",
                "total": f"{f['p']}% of the total project budget (direct costs plus the indirect costs themselves)"}[f["base"]]
        pol = (f"{f['org']} Community Foundation - budget rules for project grants\n- Indirect costs may not exceed {base}.\n"
               f"- Budgets that break this rule are returned without review.")
        rows = [("Personnel", f["pers"]), ("Fringe benefits", f["fr"]), ("Travel", f["trav"]), ("Equipment", f["equip"]), ("Supplies", f["sup"]),
                ("Indirect costs", f["ind"])]
        tab = "\n".join(f"{a} | {money(b)}" for a, b in rows)
        scen = f"{f['who'][0]} is submitting this budget (line | amount):\n{tab}"
        return f"{pol}\n\n{st.c('lab', ['', 'Budget: ', 'Situation: '])}{scen}"

    def pq(self, f, p):
        return dict(pos=["Do the indirect costs in this budget comply with the rule?", "Is this budget's indirect-cost line within the allowed maximum?"],
                    neg=["Do the indirect costs in this budget exceed the allowed maximum?", "Will this budget be returned because of the indirect-cost rule?"],
                    cpos="the indirect costs comply with the rule", cneg="the indirect costs exceed the allowed maximum",
                    speakers=[("A grants officer told " + f["who"][2] + " that", "the grants officer")])

    def letter_q(self, f):
        return ["What is the largest indirect-cost amount this budget could include under the rule (rounded down to the cent)?"]


# =============================================================================================================
class RefundCategory(Schema):
    """Return outcome by days since delivery, opened/unopened, defect exception, holiday extension."""
    name = "refund_policy"
    quota = 500
    cat = ["full refund", "refund minus restocking fee", "store credit only", "no refund"]
    cat_defs = {"full refund": "Counting days from delivery exactly as stated, the return qualifies for the whole price back (unopened within the first window, a defect within the defect window, or an extension that covers it).",
                "refund minus restocking fee": "The return is within the first window but the item was opened and is not defective, so the price minus the restocking fee is refunded.",
                "store credit only": "The return is after the first window but within the store-credit window (and no defect or extension gives a better outcome).",
                "no refund": "The return is after every window that applies, and no stated exception covers it."}
    choice_share = 0.35

    def sample(self, rng):
        yr = rng.choice([2025, 2026, 2027])
        w1, w2, dw = rng.choice([(14, 30, 90), (15, 45, 60), (30, 60, 90)])
        deliv = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        if rng.random() < 0.25:
            deliv = dt.date(yr, rng.choice([11, 12]), rng.randint(1, 28))
        k = rng.choice([w1, w1 + 1, w2, w2 + 1, dw, dw + 1, rng.randint(1, dw + 20), w1 - 1])
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "w1": w1, "w2": w2, "dw": dw,
             "deliv": iso(deliv), "ret": iso(deliv + dt.timedelta(days=k)), "opened": rng.random() < 0.5,
             "defect": rng.random() < 0.2, "order_gap": rng.randint(2, 9), "hol": rng.random() < 0.6}
        return f

    def _ext(self, f):
        d = D(f["deliv"])
        return f["hol"] and dt.date(d.year, 11, 1) <= d <= dt.date(d.year, 12, 24)

    def catv(self, f):
        d, r = D(f["deliv"]), D(f["ret"])
        k = (r - d).days
        in1 = k <= f["w1"] or (self._ext(f) and r <= dt.date(d.year + 1, 1, 31))
        if f["defect"] and k <= f["dw"]:
            return "full refund"
        if in1:
            return "refund minus restocking fee" if f["opened"] else "full refund"
        if k <= f["w2"]:
            return "store credit only"
        return "no refund"

    def catv2(self, f):
        d0 = D(f["deliv"]).toordinal()
        r0 = D(f["ret"]).toordinal()
        dd = D(f["deliv"])
        ext = f["hol"] and (dd.month == 11 or (dd.month == 12 and dd.day <= 24))
        first = (r0 - d0 <= f["w1"]) or (ext and r0 <= dt.date(dd.year + 1, 1, 31).toordinal())
        if f["defect"] and not (r0 - d0 > f["dw"]):
            return "full refund"
        if first:
            return ["full refund", "refund minus restocking fee"][int(bool(f["opened"]))]
        return "store credit only" if r0 - d0 <= f["w2"] else "no refund"

    def preds(self, f):
        return {"full": self.catv(f) == "full refund"}

    def preds2(self, f):
        return {"full": self.catv2(f) == "full refund"}

    preds_list = ("full",)

    def valid(self, f):
        return D(f["ret"]) >= D(f["deliv"])

    def alts(self, f):
        return {"ret": [add_days(f["ret"], d) for d in (-1, 1, -2, 2, -10, 10)], "opened": [not f["opened"]], "defect": [not f["defect"]],
                "hol": [not f["hol"]], "deliv": [add_days(f["deliv"], d) for d in (-1, 1)]}

    def edges(self, f, p):
        t = ["numeric", "temporal"]
        if f["defect"] or self._ext(f):
            t.append("exception")
        return t

    def render(self, f):
        st = Sty(f)
        ds = st.i("ds", 3)
        hol = ("\n- Holiday extension: items delivered between November 1 and December 24 may be returned under the first-window terms until January 31 of the following year." if f["hol"] else "")
        pol = (f"{f['org']} Home Electronics - returns policy\n- Days are counted from the delivery date (the delivery date is day 0).\n"
               f"- Within {f['w1']} days: full refund for unopened items; opened items are refunded minus a 15% restocking fee.\n"
               f"- Day {f['w1'] + 1} to day {f['w2']}: store credit only.\n- After day {f['w2']}: no refund.\n"
               f"- Defective items: full refund up to day {f['dw']}, whether opened or not.{hol}")
        od = D(f["deliv"]) - dt.timedelta(days=f["order_gap"])
        state = "opened and used" if f["opened"] else "still sealed in their original packaging"
        chg = "changed their mind" if f["who"][1] == "they" else f"changed {f['who'][3]} mind"
        defect = " They have a manufacturing defect: they will not power on." if f["defect"] else f" They work normally; {f['who'][1]} simply {chg}."
        scen = (f"{f['who'][0]} ordered a pair of wireless headphones on {fd(od, ds)}; they were delivered on {fd(f['deliv'], ds)}. "
                f"{cap(f['who'][1])} {V(f['who'], 'brings')} them back on {fd(f['ret'], ds)}. The headphones are {state}.{defect}")
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Will {who} get a full refund of the price?", f"Is {who} entitled to the whole price back?"],
                    neg=[f"Will {who} get less than a full refund of the price?"],
                    cpos=f"{who} will get a full refund", cneg=f"{who} will not get a full refund",
                    speakers=[("A store clerk told " + f["who"][2] + " that", "the clerk"), ("A friend told " + f["who"][2] + " that", "the friend")])

    def cat_q(self, f):
        return [f"What does {f['who'][0]} get for this return under the policy?"]


# =============================================================================================================
class LibraryFine(Schema):
    """Fine per OPEN day overdue (closed Sundays and listed holidays), capped per item; charge check."""
    name = "library_fine"
    quota = 400
    letter = True

    def sample(self, rng):
        due = dt.date(rng.choice([2025, 2026, 2027]), rng.randint(1, 12), rng.randint(1, 28))
        rate = rng.choice([10, 20, 25, 30, 50])
        capc = rng.choice([300, 500, 800, 1000, None])
        k = rng.choice([1, 2, 3, 6, 7, 8, 13, 15, 22, 30])
        ret = due + dt.timedelta(days=k)
        hol = []
        if rng.random() < 0.5:
            h = due + dt.timedelta(days=rng.randint(1, k))
            if h.weekday() != 6:
                hol = [iso(h)]
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "due": iso(due), "ret": iso(ret),
             "rate": rate, "cap": capc, "hol": hol, "item": rng.choice(["novel", "DVD", "cookbook", "audiobook", "travel guide"])}
        fee = self.fine(f)
        f["charged"] = max(0, fee + rng.choice([0, 0, 0, rate, -rate, 2 * rate]))
        return f

    def open_days(self, f):
        d, n = D(f["due"]) + dt.timedelta(days=1), 0
        while d <= D(f["ret"]):
            if d.weekday() != 6 and iso(d) not in f["hol"]:
                n += 1
            d += dt.timedelta(days=1)
        return n

    def fine(self, f):
        x = self.open_days(f) * f["rate"]
        return min(x, f["cap"]) if f["cap"] else x

    def fine2(self, f):
        H = np.array(f["hol"], dtype="datetime64[D]")
        n = int(np.busday_count(np.datetime64(f["due"]) + 1, np.datetime64(f["ret"]) + 1, weekmask="1111110", holidays=H))
        x = n * f["rate"]
        return x if not f["cap"] or x <= f["cap"] else f["cap"]

    def valid(self, f):
        return D(f["ret"]) > D(f["due"]) and f["charged"] >= 0

    def preds(self, f):
        return {"ok": f["charged"] == self.fine(f)}

    def preds2(self, f):
        return {"ok": f["charged"] == self.fine2(f)}

    def val(self, f):
        return self.fine(f)

    def val2(self, f):
        return self.fine2(f)

    def fmtv(self, f, v):
        return money(v)

    def wrongs(self, f):
        cal = (D(f["ret"]) - D(f["due"])).days
        out = [cal * f["rate"], self.open_days(dict(f, hol=[])) * f["rate"], (self.open_days(f) + 1) * f["rate"], self.open_days(f) * f["rate"]]
        if f["cap"]:
            out.append(min(cal * f["rate"], f["cap"]))
        return out

    def alts(self, f):
        return {"ret": [add_days(f["ret"], d) for d in (-1, 1, -2, 2)], "charged": [f["charged"] + d for d in (-f["rate"], f["rate"])],
                "hol": [[]] if f["hol"] else [], "cap": [c for c in (300, 500, None) if c != f["cap"]]}

    def edges(self, f, p):
        t = ["numeric", "temporal"]
        if f["hol"]:
            t.append("exception")
        return t

    def render(self, f):
        st = Sty(f)
        ds = st.i("ds", 3)
        hol = (f" The library was also closed on {fd(f['hol'][0], ds, wd=True)} for a public holiday." if f["hol"] else "")
        cap_ = (f" The fine for one item never exceeds {money(f['cap'])}." if f["cap"] else " There is no maximum fine.")
        pol = (f"{f['org']} Public Library - overdue fines\n- {money(f['rate'])} for each day the library is open after the due date, up to and including the day the item is returned.{cap_}\n"
               f"- The library is open Monday to Saturday and closed on Sundays.{hol}\n- Days the library is closed are not charged.")
        scen = (f"{f['who'][0]}'s {f['item']} was due on {fd(f['due'], ds, wd=True)} and was returned at the desk on {fd(f['ret'], ds, wd=True)}. "
                f"The system charged a fine of {money(f['charged'])}.")
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Is the fine charged to {who} correct under the rules?", "Does the charged fine match the library's rules?"],
                    neg=[f"Was {who} charged an incorrect fine?"],
                    cpos="the fine is correct", cneg="the fine is incorrect",
                    speakers=[("The librarian at the desk told " + f["who"][2] + " that", "the librarian")])

    def letter_q(self, f):
        return [f"What fine should {f['who'][0]} pay for the {f['item']}?"]


# =============================================================================================================
class InterestDays(Schema):
    """Simple interest for the actual number of days on a 365- or 360-day basis (start included, end excluded)."""
    name = "interest_days"
    quota = 400
    letter = True

    def sample(self, rng):
        s = dt.date(rng.choice([2027, 2028, 2025, 2026]), rng.randint(1, 12), rng.randint(1, 28))
        if rng.random() < 0.4:
            s = dt.date(rng.choice([2027, 2028]), rng.choice([1, 2]), rng.randint(1, 28))
        days = rng.randint(20, 200)
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "P": rng.randrange(1000, 50000, 50) * 100,
             "r100": rng.choice([375, 450, 525, 600, 725, 800, 950]), "basis": rng.choice([365, 360]), "start": iso(s),
             "end": iso(s + dt.timedelta(days=days))}
        v = self.interest(f)
        f["billed"] = v + rng.choice([0, 0, 0, 1, -1, 50, -50, 200])
        return f

    def interest(self, f):
        days = (D(f["end"]) - D(f["start"])).days
        return cents_round(Fr(f["P"]) * Fr(f["r100"], 10000) * days / f["basis"])

    def interest2(self, f):
        days = D(f["end"]).toordinal() - D(f["start"]).toordinal()
        with localcontext() as c:
            c.prec = 50
            return dcents(Decimal(f["P"]) * Decimal(f["r100"]) / Decimal(10000) * Decimal(days) / Decimal(f["basis"]))

    def valid(self, f):
        return D(f["end"]) > D(f["start"]) and f["billed"] > 0

    def preds(self, f):
        return {"ok": f["billed"] == self.interest(f)}

    def preds2(self, f):
        return {"ok": f["billed"] == self.interest2(f)}

    def val(self, f):
        return self.interest(f)

    def val2(self, f):
        return self.interest2(f)

    def fmtv(self, f, v):
        return money(v)

    def wrongs(self, f):
        o = dict(f, basis=365 if f["basis"] == 360 else 360)
        days = (D(f["end"]) - D(f["start"])).days
        return [self.interest(o), cents_round(Fr(f["P"]) * Fr(f["r100"], 10000) * (days + 1) / f["basis"]),
                cents_round(Fr(f["P"]) * Fr(f["r100"], 10000) * (days - 1) / f["basis"]), cents_round(Fr(f["P"]) * Fr(f["r100"], 10000) * days / 366)]

    def alts(self, f):
        return {"end": [add_days(f["end"], d) for d in (-1, 1)], "basis": [365 if f["basis"] == 360 else 360],
                "billed": [f["billed"] + d for d in (-1, 1, -50, 50)], "r100": [f["r100"] + 25, f["r100"] - 25]}

    def edges(self, f, p):
        t = ["numeric", "temporal"]
        s, e = D(f["start"]), D(f["end"])
        if any(s <= dt.date(y, 2, 29) < e for y in range(s.year, e.year + 1) if isleap(y)):
            t.append("implicit")
        return t

    def render(self, f):
        st = Sty(f)
        ds = st.i("ds", 3)
        basis = ("Interest = principal x annual rate x days / 365 (a 365-day year is used even in leap years)." if f["basis"] == 365 else
                 "Interest = principal x annual rate x days / 360 (the lender's 360-day year convention).")
        pol = (f"{f['org']} Business Lending - short-term loan terms\n- Simple interest accrues for each day from the start date up to, but not including, the repayment date.\n"
               f"- {basis}\n- The interest is rounded to the nearest cent (half a cent rounds up).")
        scen = (f"{f['who'][0]} borrowed {money(f['P'])} at {ftrim(Fr(f['r100'], 100), 2)}% a year on {fd(f['start'], ds)} and repaid everything on {fd(f['end'], ds)}. "
                f"The payoff statement shows interest of {money(f['billed'])}.")
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        return dict(pos=["Is the interest on the payoff statement correct under the loan terms?", "Does the statement show the right amount of interest?"],
                    neg=["Is the interest on the payoff statement wrong?"],
                    cpos="the statement's interest is correct", cneg="the statement's interest is wrong",
                    speakers=[(f"{f['who'][0]}'s accountant said", "the accountant")])

    def letter_q(self, f):
        return ["How much interest is due under the loan terms?"]


# =============================================================================================================
class DtiLtv(Schema):
    """Two ratio tests: debt-to-income (monthly debts incl. new payment / gross monthly income) and loan-to-value."""
    name = "dti_ltv"
    quota = 450
    multi_hop = True
    hide_keys = {"ok": ["card"]}

    def sample(self, rng):
        inc = rng.randrange(48000, 180000, 1000) * 100
        mon = Fr(inc, 12)
        cap_dti = rng.choice([36, 43, 45, 50])
        cap_ltv = rng.choice([80, 90, 95, 97])
        price = rng.randrange(200000, 900000, 1000) * 100
        car = rng.choice([0, rng.randrange(200, 700) * 100])
        stu = rng.choice([0, rng.randrange(150, 500) * 100])
        card = rng.randrange(25, 300) * 100
        target = mon * cap_dti / 100
        pay = int(target) - car - stu - card + rng.choice([0, 0, 100, -100, 1, -1, 5000, -5000])
        pay = max(50000, pay)
        down_pct = 100 - cap_ltv + rng.choice([0, 0, 1, -1, 5])
        loan = price * (100 - down_pct) // 100 + rng.choice([0, 0, 100, -100])
        return {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "inc": inc, "cap_dti": cap_dti,
                "cap_ltv": cap_ltv, "price": price, "loan": loan, "car": car, "stu": stu, "card": card, "pay": pay}

    def _ok(self, f, card):
        debts = f["car"] + f["stu"] + card + f["pay"]
        dti = Fr(debts) / Fr(f["inc"], 12)
        ltv = Fr(f["loan"], f["price"])
        return dti <= Fr(f["cap_dti"], 100) and ltv <= Fr(f["cap_ltv"], 100)

    def preds(self, f):
        if f["card"] is None:
            outs = {self._ok(f, c) for c in (0, 2500, 10 ** 7)}
            return {"ok": outs.pop() if len(outs) == 1 else None}
        return {"ok": self._ok(f, f["card"])}

    def preds2(self, f):
        cards = [f["card"]] if f["card"] is not None else [0, 10 ** 7]
        outs = set()
        for c in cards:
            debts = f["car"] + f["stu"] + c + f["pay"]
            outs.add(debts * 12 * 100 <= f["cap_dti"] * f["inc"] and f["loan"] * 100 <= f["cap_ltv"] * f["price"])
        return {"ok": outs.pop() if len(outs) == 1 else None}

    def valid(self, f):
        return f["loan"] < f["price"] and f["pay"] > 0

    def alts(self, f):
        a = {"pay": [f["pay"] + d for d in (-100, 100, -1, 1, -5000, 5000)], "loan": [f["loan"] + d for d in (-100, 100, -500000, 500000)],
             "inc": [f["inc"] + d for d in (-100000, 100000)]}
        if f["card"] is not None:
            a["card"] = [f["card"] + d for d in (-100, 100, -2000, 2000) if f["card"] + d >= 0]
        return a

    def edges(self, f, p):
        t = ["numeric", "quantifier"]
        if f["card"] is None:
            t.append("missing_info")
        return t

    def render(self, f):
        st = Sty(f)
        pol = (f"{f['org']} Mortgage - pre-approval rules\n- Debt-to-income (DTI) = all monthly debt payments, including the new mortgage payment, divided by gross MONTHLY income (annual salary / 12). DTI may not exceed {f['cap_dti']}%.\n"
               f"- Loan-to-value (LTV) = loan amount / purchase price. LTV may not exceed {f['cap_ltv']}%.\n- Both tests must be passed.")
        debts = []
        if f["car"]:
            debts.append(f"a car loan of {money(f['car'])} a month")
        if f["stu"]:
            debts.append(f"student loan payments of {money(f['stu'])} a month")
        debts.append(f"a credit card minimum payment of {money(f['card'])} a month" if f["card"] is not None else
                     "a credit card minimum payment whose amount the applicant has not provided yet")
        scen = (f"{f['who'][0]} earns {money(f['inc'], '$', True)} a year before tax and has {', '.join(debts[:-1]) + (' and ' if len(debts) > 1 else '') + debts[-1]}. "
                f"{cap(f['who'][1])} {V(f['who'], 'wants')} to borrow {money(f['loan'])} to buy a home priced at {money(f['price'])}; the new mortgage payment would be {money(f['pay'])} a month.")
        return f"{pol}\n\n{st.c('lab', LAB)}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Does {who} pass both pre-approval tests?", f"Can {who} be pre-approved under these rules?"],
                    neg=[f"Does {who} fail at least one of the pre-approval tests?", f"Must {who}'s pre-approval be declined under these rules?"],
                    cpos=f"{who} passes both tests", cneg=f"{who} fails at least one test",
                    speakers=[("A loan officer told " + f["who"][2] + " that", "the loan officer"), ("A relative told " + f["who"][2] + " that", "the relative")])


# =============================================================================================================
class AvgDailyBalance(Schema):
    """Average daily balance over a statement period from an opening balance and dated transactions."""
    name = "avg_daily_balance"
    quota = 400
    letter = True
    table = True
    multi_hop = True

    def sample(self, rng):
        y, m = rng.choice([2025, 2026, 2027, 2028]), rng.randint(1, 12)
        n = calendar.monthrange(y, m)[1]
        thr = rng.choice([100000, 150000, 250000, 500000])
        opening = thr + rng.randrange(-80000, 80000, 100)
        tx = []
        for _ in range(rng.randint(2, 5)):
            d = rng.randint(2, n)
            amt = rng.choice([1, -1]) * rng.randrange(5000, 120000, 100)
            tx.append([d, amt])
        tx.sort()
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "y": y, "m": m, "open": opening,
             "tx": tx, "thr": thr, "fee": rng.choice([800, 1200, 1500])}
        # nudge the last transaction so the average lands near the threshold
        tgt = thr * n + rng.choice([0, 0, 1, -1, 100, -100, n * 50, -n * 50])
        cur = sum(self._balances(f))
        last_d = tx[-1][0]
        span = n - last_d + 1
        delta = Fr(tgt - cur, span)
        tx[-1][1] += int(delta)
        return f

    def _balances(self, f):
        n = calendar.monthrange(f["y"], f["m"])[1]
        bal, out, i = f["open"], [], 0
        tx = sorted(f["tx"])
        for d in range(1, n + 1):
            while i < len(tx) and tx[i][0] == d:
                bal += tx[i][1]
                i += 1
            out.append(bal)
        return out

    def adb(self, f):
        b = self._balances(f)
        return Fr(sum(b), len(b))

    def adb2(self, f):
        n = calendar.monthrange(f["y"], f["m"])[1]
        tot = f["open"] * n
        for d, a in f["tx"]:
            tot += a * (n - d + 1)
        return Fr(tot, n)

    def valid(self, f):
        n = calendar.monthrange(f["y"], f["m"])[1]
        return all(1 <= d <= n for d, _ in f["tx"]) and min(self._balances(f)) >= 0 and all(a != 0 for _, a in f["tx"])

    def preds(self, f):
        return {"ok": self.adb(f) >= f["thr"]}

    def preds2(self, f):
        return {"ok": not (self.adb2(f) < f["thr"])}

    def val(self, f):
        return cents_round(self.adb(f))

    def val2(self, f):
        return dcents(Decimal(self.adb2(f).numerator) / Decimal(self.adb2(f).denominator))

    def fmtv(self, f, v):
        return money(v)

    def wrongs(self, f):
        b = self._balances(f)
        end = b[-1]
        simple = cents_round(Fr(f["open"] + end, 2))
        n = len(b)
        off = cents_round(Fr(sum(b) - b[0] + f["open"], n))
        return [simple, end, off, cents_round(self.adb(f)) + 100, cents_round(Fr(sum(b[:-1]), n - 1))]

    def alts(self, f):
        txs = []
        for i, (d, a) in enumerate(f["tx"]):
            for dd in (-1, 1, -3, 3):
                z = [list(t) for t in f["tx"]]
                z[i][0] = d + dd
                txs.append(sorted(z))
            for da in (-100, 100, -1000, 1000):
                z = [list(t) for t in f["tx"]]
                z[i][1] = a + da
                txs.append(z)
        return {"tx": txs, "thr": [f["thr"] - 1000, f["thr"] + 1000], "open": [f["open"] + d for d in (-100, 100, -1000, 1000)]}

    def edges(self, f, p):
        return ["numeric", "temporal", "table"]

    def render(self, f):
        st = Sty(f)
        mon = f"{MONTHS[f['m'] - 1]} {f['y']}"
        pol = (f"{f['org']} Savings Bank - checking account fees\n- The monthly fee of {money(f['fee'])} is waived if the account's average daily balance for the calendar month is at least {money(f['thr'], '$', True)}.\n"
               f"- Average daily balance = the sum of the end-of-day balances for every day of the month / the number of days in the month.\n- A transaction changes the balance at the end of the day it is posted.")
        rows = "\n".join(f"{MONTHS[f['m'] - 1][:3]} {d} | {'+' if a > 0 else '-'}{money(abs(a))}" for d, a in sorted(f["tx"]))
        scen = f"{f['who'][0]}'s account had a balance of {money(f['open'])} at the start of {mon} (end of the previous day). Transactions posted in {mon} (date | amount):\n{rows}"
        return f"{pol}\n\n{st.c('lab', ['', 'Statement: ', 'Situation: '])}{scen}"

    def pq(self, f, p):
        who = f["who"][0]
        return dict(pos=[f"Is the monthly fee waived for {who} this month?", f"Does {who}'s average daily balance meet the waiver threshold?"],
                    neg=[f"Will {who} be charged the monthly fee?", f"Is {who}'s average daily balance below the waiver threshold?"],
                    cpos="the fee is waived this month", cneg="the fee is charged this month",
                    speakers=[("A bank teller told " + f["who"][2] + " that", "the teller")])

    def letter_q(self, f):
        return [f"What is {f['who'][0]}'s average daily balance for the month, rounded to the nearest cent (half a cent rounds up)?"]
