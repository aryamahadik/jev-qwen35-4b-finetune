"""gen_numeric_dates schemas, part 1: ages, deadlines, business days, calendar-day windows."""
import datetime as dt
import math

import numpy as np

from nd_common import (V, MONTHS, PLACES, WEEKDAYS, D, Schema, Sty, add_days, cap, dur_words, fd, fdm, ft, iso, isleap,
                       num_w, ordn, person, plural)


def bday_in_year(dob, year, conv):
    """Primary: birthday of `dob` in `year`; 29 Feb in a non-leap year -> 1 Mar ('mar1') or 28 Feb ('feb28')."""
    d = D(dob)
    try:
        return dt.date(year, d.month, d.day)
    except ValueError:
        return dt.date(year, 3, 1) if conv == "mar1" else dt.date(year, 2, 28)


def age_on(dob, ref, conv):
    d, r = D(dob), D(ref)
    years = r.year - d.year
    if r < bday_in_year(dob, r.year, conv):
        years -= 1
    return years


def attain2(dob, n, conv):
    """Independent: the date on which a person born on dob reaches age n."""
    y, m, day = (int(x) for x in dob.split("-"))
    ty = y + n
    leap = ty % 4 == 0 and (ty % 100 != 0 or ty % 400 == 0)
    if m == 2 and day == 29 and not leap:
        return iso(dt.date(ty, 3, 1)) if conv == "mar1" else iso(dt.date(ty, 2, 28))
    return iso(dt.date(ty, m, day))


def leap_note(f, st):
    if f["dob"] is None or f["dob"][5:] != "02-29":
        return ""
    alt = "1 March" if f["conv"] == "mar1" else "28 February"
    return st.c("leapn", [
        f" For anyone born on 29 February, the birthday in a non-leap year is treated as {alt}.",
        f" Applicants born on 29 February are considered to have their birthday on {alt} in non-leap years.",
    ])


# =============================================================================================================
class AgeCutoff(Schema):
    """Eligibility by age on a reference date (turns N exactly on the date, day before/after, 29 Feb births)."""
    name = "age_cutoff"
    quota = 900
    DOMS = ["youth_league", "scholarship", "senior_fare", "alcohol", "kindergarten", "car_rental", "youth_card",
            "voting", "lifeguard", "junior_golf"]

    def sample(self, rng):
        dom = rng.choice(self.DOMS)
        f = {"dom": dom, "who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9),
             "conv": rng.choice(["mar1", "feb28"])}
        yr = rng.choice([2025, 2026, 2026, 2027, 2027, 2028, 2029])
        if dom == "youth_league":
            f.update(kind="under", N=rng.choice([8, 10, 12, 14, 16, 19]))
            ref = rng.choice([dt.date(yr, 1, 1), dt.date(yr, 8, 1), dt.date(yr, 9, 1), dt.date(yr, 12, 31), dt.date(yr, 7, 31), dt.date(yr, 1, 1)])
        elif dom == "scholarship":
            k = rng.choice(["under", "le"])
            f.update(kind=k, N=rng.choice([25, 26, 30, 35]) if k == "under" else rng.choice([24, 25, 29, 30]))
            ref = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        elif dom == "senior_fare":
            f.update(kind="ge", N=rng.choice([60, 62, 65, 66]))
            ref = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        elif dom == "alcohol":
            f.update(kind="ge", N=rng.choice([21, 21, 18]))
            ref = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        elif dom == "kindergarten":
            f.update(kind="ge", N=5)
            ref = rng.choice([dt.date(yr, 9, 1), dt.date(yr, 9, 1), dt.date(yr, 8, 31), dt.date(yr, 9, 30), dt.date(yr, 12, 31)])
        elif dom == "car_rental":
            f.update(kind="ge", N=rng.choice([21, 25, 18]))
            ref = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        elif dom == "youth_card":
            f.update(kind="range", lo=16, N=rng.choice([25, 30]))
            ref = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        elif dom == "voting":
            f.update(kind="ge", N=18)
            ref = dt.date(yr, 11, rng.randint(2, 8)) if rng.random() < 0.6 else dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        elif dom == "lifeguard":
            f.update(kind="ge", N=rng.choice([15, 16]))
            ref = dt.date(yr, rng.randint(4, 7), rng.randint(1, 28))
        else:  # junior_golf
            f.update(kind="le", N=rng.choice([12, 14, 17, 18]))
            ref = dt.date(yr, rng.choice([1, 6, 7]), rng.choice([1, 15, 30]))
        if f["kind"] == "range" and "lo" not in f:
            f["lo"] = 16
        # which boundary to probe
        if f["kind"] == "ge":
            bnd = f["N"]
        elif f["kind"] == "under":
            bnd = f["N"]
        elif f["kind"] == "le":
            bnd = f["N"] + 1
        else:
            bnd = rng.choice([f["lo"], f["N"] + 1])
        r = rng.random()
        if r < 0.1 and dom not in ("youth_league", "kindergarten", "junior_golf"):  # 29 February birth
            for _ in range(50):
                by = rng.choice([y for y in range(ref.year - bnd - 3, ref.year - bnd + 4) if isleap(y)] or [2000])
                ty = by + bnd
                if not isleap(ty):
                    break
            else:
                return self.sample(rng)
            ref = rng.choice([dt.date(ty, 2, 28), dt.date(ty, 3, 1), dt.date(ty, 2, 27), dt.date(ty, 3, 2)])
            f["dob"] = f"{by}-02-29"
        else:
            if r < 0.4:
                delta = 0
            elif r < 0.65:
                delta = rng.choice([-1, 1])
            elif r < 0.8:
                delta = rng.choice([-1, 1]) * rng.randint(2, 10)
            else:
                delta = rng.choice([-1, 1]) * rng.randint(11, 700)
            b = ref + dt.timedelta(days=delta)
            if b.month == 2 and b.day == 29:
                b = b + dt.timedelta(days=1)
            f["dob"] = iso(dt.date(b.year - bnd, b.month, b.day))
        f["ref"] = iso(ref)
        f["hy"] = int(f["dob"][:4])
        f["dobform"] = "dob" if (f["dob"][5:] == "02-29" or rng.random() < 0.7) else "turns"
        f["turnsk"] = bnd if f["kind"] != "range" else rng.choice([f["lo"], f["N"] + 1])
        return f

    derived_keys = ("hy",)
    hide_keys = {"ok": ["dob"]}

    def valid(self, f):
        if f["dob"] is None:
            return True
        try:
            D(f["dob"])
            D(f["ref"])
        except ValueError:
            return False
        if f["dobform"] == "turns" and f["dob"][5:] == "02-29":
            return False
        return D(f["dob"]) < D(f["ref"]) and f["N"] > 0

    @staticmethod
    def _year_days(y):
        d = dt.date(y, 1, 1)
        while d.year == y:
            yield iso(d)
            d += dt.timedelta(days=1)

    def preds(self, f):
        if f["dob"] is None:
            outs = {self.preds(dict(f, dob=x))["ok"] for x in self._year_days(f["hy"]) if x < f["ref"]}
            return {"ok": outs.pop() if len(outs) == 1 else None}
        a = age_on(f["dob"], f["ref"], f["conv"])
        k, N = f["kind"], f["N"]
        ok = {"ge": a >= N, "under": a < N, "le": a <= N, "range": f.get("lo", 0) <= a <= N}[k]
        return {"ok": ok}

    def preds2(self, f):
        if f["dob"] is None:
            ends = [f"{f['hy']}-01-01", f"{f['hy']}-12-31"]
            outs = {self.preds2(dict(f, dob=x))["ok"] for x in ends if x < f["ref"]}
            return {"ok": outs.pop() if len(outs) == 1 else None}
        k, N, r = f["kind"], f["N"], f["ref"]
        if k == "ge":
            ok = r >= attain2(f["dob"], N, f["conv"])
        elif k == "under":
            ok = r < attain2(f["dob"], N, f["conv"])
        elif k == "le":
            ok = r < attain2(f["dob"], N + 1, f["conv"])
        else:
            ok = attain2(f["dob"], f["lo"], f["conv"]) <= r < attain2(f["dob"], N + 1, f["conv"])
        return {"ok": ok}

    def alts(self, f):
        if f["dob"] is None:
            return {"ref": [add_days(f["ref"], d) for d in (-1, 1)]}
        a = {"dob": [add_days(f["dob"], d) for d in (-2, -1, 1, 2)] if f["dob"][5:] != "02-29" else [],
             "ref": [add_days(f["ref"], d) for d in (-1, 1, -2, 2)]}
        if f["dob"][5:] == "02-29":
            a["conv"] = ["mar1", "feb28"]
        return a

    def edges(self, f, p):
        t = ["temporal", "numeric"]
        if f["dob"] is None:
            return t + ["missing_info"]
        if f["dob"][5:] == "02-29":
            t.append("exception")
        if f["dobform"] == "turns":
            t.append("implicit")
        return t

    def neg_rule(self, f):
        """True when the relevant rule is phrased negatively (so a negated question makes a double negation)."""
        st = Sty(f)
        dom = f["dom"]
        if dom == "youth_league":
            return st.i("pol", 3) in (1, 2)
        if dom in ("alcohol", "car_rental", "lifeguard"):
            return st.i("rule", 2) == 1
        if dom == "scholarship" and f["kind"] == "under":
            return st.i("rule", 2) == 1
        return False

    # ---- text
    def _dobtxt(self, f, st):
        n = f["who"][0]
        ds = st.i("ds", 2)
        if f["dob"] is None:
            if f["dom"] == "alcohol":
                return f"{n}'s driving licence is worn: only the year of birth, {f['hy']}, can be read."
            return st.c("dn", [f"{n} was born in {f['hy']}; the exact date of birth is not given on the form.",
                               f"The form shows only {n}'s year of birth, {f['hy']}, not the full date."])
        if f["dobform"] == "turns":
            k = f["turnsk"]
            y, m, d = (int(x) for x in f["dob"].split("-"))
            bd = dt.date(y + k, m, d)
            return st.c("tf", [f"{n}'s {ordn(k)} birthday falls on {fd(bd, ds)}.",
                               f"{n} turns {k} on {fd(bd, ds)}.",
                               f"According to {f['who'][3]} records, {n} reaches the age of {k} on {fd(bd, ds)}."])
        if f["dom"] == "alcohol":
            return st.c("dfa", [f"The date of birth on {n}'s driving licence is {fd(f['dob'], ds)}.",
                                f"{n}'s photo ID shows a date of birth of {fd(f['dob'], ds)}."])
        return st.c("df", [f"{n} was born on {fd(f['dob'], ds)}.",
                           f"{n}'s date of birth is {fd(f['dob'], ds)}.",
                           f"{n}'s passport gives {f['who'][3]} date of birth as {fd(f['dob'], ds)}."])

    def render(self, f):
        st = Sty(f)
        dom, N, n = f["dom"], f["N"], f["who"][0]
        ds = st.i("ds", 2)
        ref = fd(f["ref"], ds)
        org = f["org"]
        ln = leap_note(f, st)
        dob = self._dobtxt(f, st)
        if dom == "youth_league":
            sport = st.c("sp", ["Soccer", "Hockey", "Basketball", "Baseball", "Netball", "Rugby"])
            pol = st.c("pol", [
                f"{org} Youth {sport} League - registration rules\n- The U{N} division is for players who are under {N} years old on {ref}.{ln}\n- Each player must provide a copy of a birth certificate or passport.\n- Registration fees are non-refundable after the first practice.",
                f"{org} Junior {sport} - age eligibility\nA player may register for a U{N} team only if the player has not yet turned {N} on {ref}.{ln} Players may always play up an age group with the coach's approval, but never down.",
                f"{org} {sport} Association, age rules for U{N} teams: players who are {N} or older on {ref} are not eligible for U{N} teams.{ln} Proof of age is checked at the first game.",
            ])
            scen = f"{dob} {cap(f['who'][3])} family wants to sign {f['who'][2]} up for a U{N} team."
        elif dom == "scholarship":
            if f["kind"] == "under":
                rule = st.c("rule", [f"Applicants must be under {N} years of age on the closing date, {ref}.",
                                     f"Applicants must not have reached their {ordn(N)} birthday on or before the closing date ({ref})."])
            else:
                rule = st.c("rule", [f"The award is open to applicants aged {N} or younger on the closing date, {ref}.",
                                     f"To apply you must be no older than {N} on {ref}, the closing date."])
            fund = st.c("fund", ["Early Career Research Scholarship", "Young Artists Bursary", "Emerging Leaders Fellowship",
                                 "Graduate Travel Grant", "Young Engineers Award"])
            pol = f"{org} Foundation - {fund}, eligibility\n1. {rule}{ln}\n2. Applicants must be enrolled in, or have completed, a degree programme.\n3. Previous award holders may not apply again."
            scen = f"{dob} {n} submitted a complete application for the {fund} before the closing date."
        elif dom == "senior_fare":
            op = st.c("op", ["Rail", "Coach", "Ferry", "Transit"])
            rule = st.c("rule", [f"Senior fares are available to passengers aged {N} or over on the date of travel.",
                                 f"The senior discount applies only to travellers who have reached the age of {N} by the day of travel."])
            pol = f"{org} {op} - fare conditions\n- {rule}{ln}\n- Child fares apply to passengers aged 5 to 15.\n- Discounted fares must be booked at least 24 hours before departure."
            scen = f"{dob} {cap(f['who'][1])} {V(f['who'], 'is')} booking a one-way trip for {ref}."
        elif dom == "alcohol":
            rule = st.c("rule", [f"Alcohol may be sold only to customers who are at least {N} years old on the day of the sale.",
                                 f"Do not sell alcohol to anyone under {N} years of age on the day of the sale."])
            pol = f"{org} Market - checkout policy\n- {rule}{ln} Check the date of birth on a valid photo ID.\n- Tobacco products are kept behind the counter.\n- Refunds on alcohol require a receipt."
            scen = f"On {ref}, a customer, {n}, brings a bottle of wine to the checkout. {dob}"
        elif dom == "kindergarten":
            yr = D(f["ref"]).year
            rule = st.c("rule", [f"A child may enrol in kindergarten for the {yr}-{yr + 1} school year if the child turns five on or before {ref}.",
                                 f"Children must be five years old on {ref} to start kindergarten in the {yr}-{yr + 1} school year."])
            pol = f"{org} School District - kindergarten admission\n1. {rule}{ln}\n2. Proof of residence is required.\n3. Early entry is not offered."
            scen = f"{dob} {cap(f['who'][3])} parents want {f['who'][2]} to start kindergarten in the {yr}-{yr + 1} school year."
        elif dom == "car_rental":
            rule = st.c("rule", [f"The main driver must be at least {N} years old on the day the car is picked up.",
                                 f"Renters under {N} on the pick-up date cannot rent from this location."])
            pol = f"{org} Car Rental - rental terms\n- {rule}{ln}\n- A valid driving licence held for at least one year is required.\n- A security deposit is taken on a credit card."
            scen = f"{dob} {cap(f['who'][1])} {V(f['who'], 'has')} reserved a car to be picked up on {ref} and {V(f['who'], 'has')} held a licence for several years."
        elif dom == "youth_card":
            lo = f["lo"]
            rule = st.c("rule", [f"The Youth Card can be bought by anyone aged {lo} to {N} inclusive on the date of purchase.",
                                 f"You must be at least {lo} and no older than {N} on the day you buy the Youth Card."])
            pol = f"{org} Travel - Youth Card terms\n- {rule}{ln}\n- The card is valid for 12 months from the date of purchase.\n- Proof of age must be shown on request."
            scen = f"{dob} {cap(f['who'][1])} {V(f['who'], 'wants')} to buy a Youth Card on {ref}."
        elif dom == "voting":
            rule = st.c("rule", [f"You may vote in the election on {ref} if you will be 18 or older on election day.",
                                 f"Only people who are at least 18 years old on the day of the election ({ref}) may vote."])
            pol = f"{org} County Elections Office - who can vote\n- {rule}{ln}\n- You must be registered at your current address.\n- Voters must bring an accepted form of identification."
            scen = f"{dob} {cap(f['who'][1])} {V(f['who'], 'is')} registered at {f['who'][3]} current address and {V(f['who'], 'wants')} to vote in the election on {ref}."
        elif dom == "lifeguard":
            rule = st.c("rule", [f"Candidates must be at least {N} years old on the first day of the course ({ref}).",
                                 f"No candidate under {N} on {ref}, the first day of the course, may enrol."])
            pol = f"{org} Aquatic Centre - lifeguard certification course\n1. {rule}{ln}\n2. Candidates must swim 300 metres continuously.\n3. The course fee includes the exam."
            scen = f"{dob} {n} can swim 300 metres without stopping and wants to enrol in the course starting on {ref}."
        else:  # junior_golf
            rule = st.c("rule", [f"The junior tournament is open to golfers aged {N} or younger on {ref}.",
                                 f"Golfers who are older than {N} on {ref} must enter the adult tournament."])
            pol = f"{org} Golf Club - junior tournament entry\n- {rule}{ln}\n- A handicap certificate is required.\n- Entries close one week before the event."
            scen = f"{dob} {n} has a valid handicap certificate and entered on time."
        lab = st.c("lab", ["Situation: ", "Case: ", "", "Facts: "])
        return f"{pol}\n\n{lab}{scen}"

    def pq(self, f, p):
        dom, N, n = f["dom"], f["N"], f["who"][0]
        pr = f["who"][1]
        if dom == "youth_league":
            return dict(pos=[f"Is {n} eligible to play in the U{N} division?", f"Can {n} register for a U{N} team?"],
                        neg=[f"Is {n} too old for the U{N} division?", f"Is {n} ineligible for U{N} teams because of age?"],
                        cpos=f"{n} is young enough to play in the U{N} division", cneg=f"{n} is too old to play in the U{N} division",
                        speakers=[("The club registrar told the family", "the registrar"), ("A coach said", "the coach")])
        if dom == "scholarship":
            return dict(pos=[f"Does {n} meet the age requirement for the award?", f"Is {n} within the age limit for this award?"],
                        neg=[f"Is {n} over the age limit for the award?", f"Does {n} fail the age requirement for the award?"],
                        cpos=f"{n} meets the age requirement", cneg=f"{n} is over the age limit",
                        speakers=[("A foundation officer wrote to the applicant that", "the officer"), ("A friend told the applicant that", "the friend")])
        if dom == "senior_fare":
            return dict(pos=[f"Can {n} travel on a senior fare on that date?", f"Is {n} entitled to the senior fare for this trip?"],
                        neg=[f"Is {n} too young for the senior fare on the travel date?", f"Is {n} ineligible for the senior fare for this trip?"],
                        cpos=f"{n} qualifies for the senior fare on the travel date", cneg=f"{n} does not qualify for the senior fare on the travel date",
                        speakers=[("The booking agent told the passenger that", "the booking agent")])
        if dom == "alcohol":
            return dict(pos=["May the cashier sell the wine to the customer that day?", "Is the sale of the wine allowed under the policy?"],
                        neg=["Must the cashier refuse to sell the wine to the customer?", "Is the customer too young to buy the wine that day?"],
                        cpos="the customer is old enough to buy the wine", cneg="the customer is too young to buy the wine",
                        speakers=[("The shift supervisor told the cashier that", "the supervisor"), ("Another cashier said", "the other cashier")])
        if dom == "kindergarten":
            yr = D(f["ref"]).year
            return dict(pos=[f"Can {n} start kindergarten in the {yr}-{yr + 1} school year?", f"Is {n} old enough for kindergarten in {yr}-{yr + 1}?"],
                        neg=[f"Is {n} too young to start kindergarten in the {yr}-{yr + 1} school year?"],
                        cpos=f"{n} is old enough to start kindergarten that year", cneg=f"{n} is too young to start kindergarten that year",
                        speakers=[("The school secretary told the parents that", "the secretary"), ("A neighbour told the parents that", "the neighbour")])
        if dom == "car_rental":
            return dict(pos=[f"Can {n} rent the car as the main driver on the pick-up date?", f"Does {n} meet the minimum age to rent the car?"],
                        neg=[f"Is {n} too young to rent the car on the pick-up date?", f"Will {n} be turned away because of age at pick-up?"],
                        cpos=f"{n} meets the minimum age on the pick-up date", cneg=f"{n} is below the minimum age on the pick-up date",
                        speakers=[("The rental agent told the customer on the phone that", "the agent")])
        if dom == "youth_card":
            return dict(pos=[f"Can {n} buy the Youth Card on that date?", f"Is {n} within the age range for the Youth Card on that date?"],
                        neg=[f"Is {n} outside the age range for the Youth Card on that date?"],
                        cpos=f"{n} is within the Youth Card age range on that date", cneg=f"{n} is outside the Youth Card age range on that date",
                        speakers=[("The ticket office clerk said", "the clerk")])
        if dom == "voting":
            return dict(pos=[f"Can {n} vote in this election?", f"Is {n} old enough to vote on election day?"],
                        neg=[f"Is {n} too young to vote in this election?"],
                        cpos=f"{n} is old enough to vote in this election", cneg=f"{n} is too young to vote in this election",
                        speakers=[("A poll worker told " + f["who"][2] + " that", "the poll worker")])
        if dom == "lifeguard":
            return dict(pos=[f"Is {n} old enough to enrol in the course?", f"Does {n} meet the age requirement for the course?"],
                        neg=[f"Is {n} too young to enrol in the course?"],
                        cpos=f"{n} meets the course's age requirement", cneg=f"{n} is too young for the course",
                        speakers=[("The centre's receptionist told " + f["who"][2] + " that", "the receptionist")])
        return dict(pos=[f"Can {n} play in the junior tournament?", f"Is {n} eligible for the junior tournament?"],
                    neg=[f"Must {n} enter the adult tournament instead of the junior one?", f"Is {n} too old for the junior tournament?"],
                    cpos=f"{n} is eligible for the junior tournament", cneg=f"{n} is too old for the junior tournament",
                    speakers=[("The tournament secretary said", "the secretary")])


# =============================================================================================================
class AgeBand(Schema):
    """Age band on a reference date -> category (car rental surcharge bands, youth divisions)."""
    name = "age_band"
    quota = 350
    choice_share = 1.0
    preds_list = ()

    def __init__(self, kind):
        self.kind = kind
        self.name = f"age_band_{kind}"
        if kind == "rental":
            self.cat = ["standard rate", "young driver surcharge", "cannot rent"]
            self.cat_defs = {
                "standard rate": "The driver is at or above the age at which the stated standard rate starts, counted in completed years on the pick-up date.",
                "young driver surcharge": "The driver has reached the minimum rental age but not the standard-rate age on the pick-up date (completed years), so the surcharge band applies.",
                "cannot rent": "The driver is below the minimum rental age on the pick-up date (completed years; a birthday on the pick-up date already counts)."}
        else:
            self.cat = ["U10", "U12", "U14", "not eligible"]
            self.cat_defs = {
                "U10": "The player's age on the stated cutoff date, in completed years, is below 10.",
                "U12": "The player's age on the stated cutoff date, in completed years, is 10 or 11.",
                "U14": "The player's age on the stated cutoff date, in completed years, is 12 or 13.",
                "not eligible": "The player is 14 or older on the stated cutoff date (a birthday on the cutoff date already counts), so no youth division applies."}

    def sample(self, rng):
        f = {"who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "conv": rng.choice(["mar1", "feb28"])}
        yr = rng.choice([2025, 2026, 2027, 2028, 2029])
        if self.kind == "rental":
            lo, hi = rng.choice([(21, 25), (18, 25), (21, 26), (20, 25)])
            f.update(lo=lo, hi=hi)
            ref = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
            bnd = rng.choice([lo, hi])
        else:
            ref = dt.date(yr, rng.choice([1, 8, 9]), 1)
            bnd = rng.choice([10, 12, 14])
        r = rng.random()
        delta = 0 if r < 0.35 else (rng.choice([-1, 1]) if r < 0.6 else rng.choice([-1, 1]) * rng.randint(2, 300))
        b = ref + dt.timedelta(days=delta)
        if b.month == 2 and b.day == 29:
            b += dt.timedelta(days=1)
        f["dob"] = iso(dt.date(b.year - bnd, b.month, b.day))
        f["ref"] = iso(ref)
        return f

    def valid(self, f):
        return D(f["dob"]) < D(f["ref"])

    def catv(self, f):
        a = age_on(f["dob"], f["ref"], f["conv"])
        if self.kind == "rental":
            return "cannot rent" if a < f["lo"] else ("young driver surcharge" if a < f["hi"] else "standard rate")
        return "U10" if a < 10 else "U12" if a < 12 else "U14" if a < 14 else "not eligible"

    def catv2(self, f):
        r = f["ref"]
        if self.kind == "rental":
            if r < attain2(f["dob"], f["lo"], f["conv"]):
                return "cannot rent"
            return "young driver surcharge" if r < attain2(f["dob"], f["hi"], f["conv"]) else "standard rate"
        for age, lab in ((10, "U10"), (12, "U12"), (14, "U14")):
            if r < attain2(f["dob"], age, f["conv"]):
                return lab
        return "not eligible"

    def alts(self, f):
        return {"dob": [add_days(f["dob"], d) for d in (-2, -1, 1, 2, -40, 40, -400, 400, -1461, 1461, -2922, 2922, -1826, 1826)],
                "ref": [add_days(f["ref"], d) for d in (-1, 1, -2, 2)]}

    def edges(self, f, p):
        return ["temporal", "numeric"]

    def render(self, f):
        st = Sty(f)
        ds = st.i("ds", 3)
        n = f["who"][0]
        dob = st.c("dob", [f"{n} was born on {fd(f['dob'], ds)}.", f"{n}'s date of birth is {fd(f['dob'], ds)}."])
        if self.kind == "rental":
            lo, hi = f["lo"], f["hi"]
            sur = st.c("sur", ["$25", "$30", "€19", "£22"])
            pol = st.c("pol", [
                f"{f['org']} Car Hire - driver age\n- Minimum age: {lo} on the pick-up date.\n- Drivers aged {lo} to {hi - 1} on the pick-up date pay a young driver surcharge of {sur} per day.\n- Drivers aged {hi} or over pay the standard rate.",
                f"{f['org']} Rentals, age policy: renters must have turned {lo} by the day the car is collected. A daily young driver surcharge ({sur}) applies to renters who are under {hi} on that day; everyone else pays the standard rate.",
            ])
            scen = f"{dob} {cap(f['who'][1])} {V(f['who'], 'is')} collecting a car on {fd(f['ref'], ds)}."
        else:
            pol = st.c("pol", [
                f"{f['org']} Youth Soccer - divisions for the season\nDivisions are set by the player's age on {fd(f['ref'], ds)}:\n- under 10: U10\n- 10 or 11: U12\n- 12 or 13: U14\n- 14 or older: not eligible for youth divisions",
                f"{f['org']} Junior Football Club. A player's division depends on how old the player is on {fd(f['ref'], ds)}. Players under 10 play U10; players aged 10-11 play U12; players aged 12-13 play U14. Players aged 14 and over on that date cannot join a youth division.",
            ])
            scen = f"{dob} {cap(f['who'][3])} parents are registering {f['who'][2]} for the season."
        return f"{pol}\n\n{st.c('lab', ['Situation: ', 'Case: ', ''])}{scen}"

    def cat_q(self, f):
        n = f["who"][0]
        if self.kind == "rental":
            return [f"Which rate applies to {n}'s rental?", f"Under the age policy, how is {n}'s rental treated?"]
        return [f"Which division does {n} belong in?", f"In which division should {n} be registered?"]


# =============================================================================================================
class SubmissionDeadline(Schema):
    """Deadline with a clock time (inclusive 'by / no later than' vs exclusive 'before'), grace period, extension
    exception; categories on time / late with penalty / rejected."""
    name = "submission_deadline"
    quota = 900
    preds_list = ("accepted", "ontime", "penalty")
    cat = ["on time", "late but accepted with the penalty", "rejected as too late"]
    cat_defs = {"on time": "The submission is not after the applicable deadline; exactly at the original deadline counts as on time for 'by' or 'no later than' wording but not for 'before', and an approved extension runs up to and including its stated end.",
                "late but accepted with the penalty": "The submission is after the applicable deadline but within the stated grace period (grace never applies on top of an approved extension), so it is accepted with the penalty.",
                "rejected as too late": "The submission is after the deadline and also after the end of any grace period or approved extension that applies."}
    hide_keys = {"ontime": ["sub_t"]}
    DOMS = ["grant", "claim", "paper", "coursework", "permit", "tender", "tax", "essay"]

    def sample(self, rng):
        dom = rng.choice(self.DOMS)
        yr = rng.choice([2025, 2026, 2027, 2028])
        dd = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        dl_t = rng.choice([1439, 1439, 1020, 720, 1080, 960, 540, 1439, 1020])
        incl = rng.choice([True, True, False]) if dl_t != 1439 else True
        grace = rng.choice([0, 24, 48, 72, 2, 12])
        f = {"dom": dom, "who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9), "dl_d": iso(dd),
             "dl_t": dl_t, "incl": incl, "grace": grace, "ext": "none", "ext_h": rng.choice([24, 48, 72, 168])}
        if rng.random() < 0.2:
            f["ext"] = rng.choice(["approved", "requested"])
        dlm = dl_t
        r = rng.random()
        if r < 0.35:
            off = rng.choice([0, 0, 1, -1])
        elif r < 0.6:
            off = grace * 60 + rng.choice([0, 1, -1, 2])
        elif r < 0.75 and f["ext"] != "none":
            off = f["ext_h"] * 60 + rng.choice([0, 1, -1])
        else:
            off = rng.choice([-1, 1]) * rng.randint(2, 4000)
        t = dd.toordinal() * 1440 + dlm + off
        sd, sm = divmod(t, 1440)
        f["sub_d"], f["sub_t"] = iso(dt.date.fromordinal(sd)), sm
        return f

    def _abs(self, d, t):
        return D(d).toordinal() * 1440 + t

    def _status(self, f, sub_t=None):
        st_ = f["sub_t"] if sub_t is None else sub_t
        dl = self._abs(f["dl_d"], f["dl_t"])
        s = self._abs(f["sub_d"], st_)
        on = s <= dl if f["incl"] else s < dl
        if f["ext"] == "approved":
            # extension replaces the deadline: 'up to N days after the original deadline' includes its end; no penalty, no grace
            ed = dl + f["ext_h"] * 60
            on2 = s <= ed
            return "on time" if on2 else "rejected as too late"
        if on:
            return "on time"
        if f["grace"] and s <= dl + f["grace"] * 60:
            return "late but accepted with the penalty"
        return "rejected as too late"

    def catv(self, f):
        if f["sub_t"] is None:
            outs = {self._status(f, t) for t in range(0, 1440)}
            return outs.pop() if len(outs) == 1 else None
        return self._status(f)

    def catv2(self, f):
        if f["sub_t"] is None:
            outs = {self._status2(f, t) for t in (0, 1439, f["dl_t"], (f["dl_t"] - 1) % 1440, (f["dl_t"] + 1) % 1440)}
            return outs.pop() if len(outs) == 1 else None
        return self._status2(f, f["sub_t"])

    def _status2(self, f, sub_t):
        dl = dt.datetime.combine(D(f["dl_d"]), dt.time()) + dt.timedelta(minutes=f["dl_t"])
        s = dt.datetime.combine(D(f["sub_d"]), dt.time()) + dt.timedelta(minutes=sub_t)
        late = (s > dl) if f["incl"] else (s >= dl)
        if f["ext"] == "approved":
            e = dl + dt.timedelta(hours=f["ext_h"])
            return "rejected as too late" if s > e else "on time"
        if not late:
            return "on time"
        if f["grace"] > 0 and (s - dl) <= dt.timedelta(hours=f["grace"]):
            return "late but accepted with the penalty"
        return "rejected as too late"

    def preds(self, f):
        c = self.catv(f)
        if c is None:
            # accepted / penalty may still be decidable
            outs = {self._status(f, t) for t in range(1440)}
            acc = {o != "rejected as too late" for o in outs}
            pen = {o == "late but accepted with the penalty" for o in outs}
            return {"accepted": acc.pop() if len(acc) == 1 else None, "ontime": None,
                    "penalty": pen.pop() if len(pen) == 1 else None}
        return {"accepted": c != "rejected as too late", "ontime": c == "on time",
                "penalty": c == "late but accepted with the penalty"}

    def preds2(self, f):
        c = self.catv2(f)
        if c is None:
            return {"accepted": self.preds(f)["accepted"], "ontime": None, "penalty": self.preds(f)["penalty"]}
        return {"accepted": c in ("on time", "late but accepted with the penalty"), "ontime": c == "on time",
                "penalty": c == "late but accepted with the penalty"}

    def valid(self, f):
        if f["sub_t"] is not None and not (0 <= f["sub_t"] < 1440):
            return False
        if not f["incl"] and f["dl_t"] == 1439:
            return False
        return True

    def alts(self, f):
        t = f["sub_t"]
        a = {"incl": [not f["incl"]] if f["dl_t"] != 1439 else [],
             "grace": [g for g in (0, 2, 12, 24, 48, 72) if g != f["grace"]],
             "ext": [e for e in ("none", "approved", "requested") if e != f["ext"]],
             "sub_d": [add_days(f["sub_d"], d) for d in (-1, 1, -2, 2, 3)]}
        if t is not None:
            a["sub_t"] = [x for x in (t - 1, t + 1, t - 2, t + 2, t - 30, t + 30, t - 90, t + 90) if 0 <= x < 1440]
        return a

    def reveal_vals(self, f, key):
        return list(range(0, 1440, 7)) + [f["dl_t"], f["dl_t"] - 1, f["dl_t"] + 1]

    def edges(self, f, p):
        t = ["temporal", "numeric"]
        if f["ext"] != "none":
            t.append("exception")
        if f["sub_t"] is None:
            t.append("missing_info")
        return t

    def _dl_phrase(self, f, st):
        ts = st.i("ts", 3)
        ds = st.i("ds", 3)
        tm = ft(f["dl_t"], ts)
        date = fd(f["dl_d"], ds, wd=st.p("wd", 0.5))
        if f["incl"]:
            return st.c("inc", [f"no later than {tm} on {date}", f"by {tm} on {date}", f"at or before {tm} on {date}"])
        return st.c("exc", [f"before {tm} on {date}", f"strictly before {tm} on {date}"])

    def render(self, f):
        st = Sty(f)
        dom, n = f["dom"], f["who"][0]
        thing = {"grant": "grant application", "claim": "claim form", "paper": "paper", "coursework": "coursework",
                 "permit": "permit application", "tender": "tender", "tax": "tax return", "essay": "scholarship essay"}[dom]
        body = {"grant": f"{f['org']} Community Fund - submission rules",
                "claim": f"{f['org']} Mutual Insurance - claim filing",
                "paper": f"{f['org']} Workshop on Applied Statistics - call for papers",
                "coursework": f"{f['org']} College - coursework submission policy",
                "permit": f"{f['org']} City Planning - event permit applications",
                "tender": f"{f['org']} Water Authority - invitation to tender",
                "tax": f"{f['org']} Revenue Office - filing rules for the annual return",
                "essay": f"{f['org']} Scholarship Trust - essay round"}[dom]
        things = {"grant": "Grant applications", "claim": "Claim forms", "paper": "Papers", "coursework": "Coursework",
                  "permit": "Permit applications", "tender": "Tenders", "tax": "Tax returns", "essay": "Scholarship essays"}[dom]
        verb = "is" if dom == "coursework" else "are"
        lines = [f"{things} must be submitted {self._dl_phrase(f, st)}. The time of submission is the time stamp shown on the online portal (all times are local time)."]
        g = f["grace"]
        pen = st.c("pen", ["a 10% penalty", "a late fee of $50", "a penalty of 5 points", "a reduction of one grade step"])
        if g:
            gtxt = f"{g} hours" if g not in (24, 48, 72) or st.p("gh", 0.5) else f"{g // 24} {plural(g // 24, 'day')} ({g} hours)"
            lines.append(st.c("gr", [f"A grace period of {gtxt} follows the deadline: submissions received after the deadline but no more than {gtxt} after it are accepted with {pen}.",
                                     f"Late submissions are accepted with {pen} if they arrive within {gtxt} after the deadline (a submission exactly {gtxt} after the deadline is still accepted)."]))
            lines.append("Anything received after the grace period is rejected.")
        else:
            lines.append(st.c("ng", ["There is no grace period: late submissions are rejected.",
                                     "Late submissions are not accepted under any circumstances except an approved extension."]))
        if f["ext"] != "none" or st.p("extl", 0.5):
            eh = f["ext_h"]
            et = f"{eh} hours" if eh % 24 else f"{eh // 24} {plural(eh // 24, 'day')}"
            lines.append(f"An applicant whose extension request has been approved in writing may submit up to {et} after the original deadline with no penalty; no grace period applies on top of an extension. A request that has not been approved does not change the deadline.")
        pol = body + "\n" + "\n".join(f"- {x}" for x in lines)
        ts, ds = st.i("ts2", 3), st.i("ds2", 3)
        if f["sub_t"] is None:
            when = st.c("wh", [f"on {fd(f['sub_d'], ds, wd=True)}; the confirmation email shows the date but not the time",
                               f"on {fd(f['sub_d'], ds, wd=True)} (the portal receipt was lost, so the exact time is unknown)"])
        else:
            when = f"at {ft(f['sub_t'], ts)} on {fd(f['sub_d'], ds, wd=True)}"
        ext = {"none": "", "approved": f" Before the deadline, {n} had asked for an extension, and it was approved in writing.",
               "requested": f" Before the deadline, {n} emailed to ask for an extension but has not received any reply."}[f["ext"]]
        scen = st.c("sc", [f"{n} submitted {f['who'][3]} {thing} {when}.{ext}",
                           f"The portal records that {n}'s {thing} was received {when}.{ext}"])
        return f"{pol}\n\n{st.c('lab', ['Situation: ', 'Case: ', '', 'What happened: '])}{scen}"

    def pq(self, f, p):
        n = f["who"][0]
        thing = {"grant": "grant application", "claim": "claim", "paper": "paper", "coursework": "coursework",
                 "permit": "permit application", "tender": "tender", "tax": "tax return", "essay": "essay"}[f["dom"]]
        sp = [("A colleague told " + f["who"][2] + " that", "the colleague"), ("The help desk replied that", "the help desk")]
        if p == "accepted":
            return dict(pos=[f"Will {n}'s {thing} be accepted?", f"Is {n}'s {thing} accepted under the rules (with or without a penalty)?"],
                        neg=[f"Will {n}'s {thing} be rejected as too late?", f"Is {n}'s {thing} refused under the rules?"],
                        cpos=f"the {thing} will be accepted", cneg=f"the {thing} will be rejected as too late", speakers=sp)
        if p == "ontime":
            return dict(pos=[f"Was {n}'s {thing} submitted on time, so that no late penalty applies?", f"Was {n}'s {thing} submitted within the applicable deadline?"],
                        neg=[f"Was {n}'s {thing} late?", f"Did {n} miss the deadline?"],
                        cpos=f"the {thing} was on time", cneg=f"the {thing} was late", speakers=sp)
        return dict(pos=[f"Will {n}'s {thing} be accepted but with the late penalty?", f"Does the late penalty apply to {n}'s {thing}?"],
                    neg=[],
                    cpos=f"the {thing} is accepted with the late penalty", cneg=f"no late penalty applies to the {thing}", speakers=sp)

    def cat_q(self, f):
        return [f"How should {f['who'][0]}'s submission be treated under these rules?", "Which outcome applies to this submission?"]


# =============================================================================================================
HOL_POOL = [("public holiday",), ("bank holiday",), ("regional holiday",), ("office closed",), ("national holiday",),
            ("state holiday",)]


def bdays_after(start, n, hol):
    """Primary: the n-th business day after start (start excluded)."""
    d = D(start)
    k = 0
    while k < n:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and iso(d) not in hol:
            k += 1
    return iso(d)


class BusinessDays(Schema):
    """'Within N business days after X' / 'at least N business days before Y' with listed holidays (observed dates)."""
    name = "business_days"
    quota = 900
    letter = True
    derived_keys = ("holnames",)

    def can_hide(self, p):
        return True

    def hide(self, f, p, rng):
        """An unconfirmed possible closure day inside the window: the answer then depends on it."""
        lo, hi = (D(f["start"]), D(f["act"])) if f["mode"] == "within" else (D(f["act"]), D(f["leave"]))
        c = [lo + dt.timedelta(days=k) for k in range(1, (hi - lo).days + 1)]
        c = [d for d in c if d.weekday() < 5 and iso(d) not in f["hol"] and d != D(f.get("leave") or "1900-01-01")]
        if not c:
            return None
        g = dict(f)
        g["maybe"] = iso(rng.choice(c))
        return g
    DOMS = ["return", "transfer", "notice", "cooling", "records", "warranty_reg"]

    def sample(self, rng):
        dom = rng.choice(self.DOMS)
        mode = "before" if dom == "notice" else "within"
        yr = rng.choice([2025, 2026, 2027, 2028])
        start = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        n = rng.choice([2, 3, 5, 5, 7, 10, 10, 14, 15])
        f = {"dom": dom, "mode": mode, "who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9),
             "n": n, "start": iso(start)}
        # holidays near the window (listed explicitly, with observed dates)
        hol = []
        span = [start + dt.timedelta(days=i) for i in range(1, n * 2 + 6)]
        for _ in range(rng.choice([0, 1, 1, 2, 2, 3])):
            d = rng.choice(span)
            if d.weekday() < 5 and iso(d) not in hol:
                hol.append(iso(d))
        f["hol"] = sorted(hol)
        f["holnames"] = [rng.choice(HOL_POOL)[0] for _ in hol]
        dl = D(bdays_after(iso(start), n, set(hol)))
        if mode == "within":
            r = rng.random()
            if r < 0.4:
                act = dl
            elif r < 0.7:
                act = dl + dt.timedelta(days=1)
                while act.weekday() >= 5 and rng.random() < 0.5:
                    act += dt.timedelta(days=1)
            else:
                act = dl + dt.timedelta(days=rng.choice([-3, -2, -1, 2, 3, 4]))
            f["act"] = iso(act)
        else:
            # notice given on 'act'; leave starts on 'start' + lead; need >= n business days strictly between
            leave = start + dt.timedelta(days=rng.randint(n + 2, n * 2 + 6))
            while leave.weekday() >= 5:
                leave += dt.timedelta(days=1)
            f["leave"] = iso(leave)
            f["act"] = iso(start)
            # re-centre holidays inside the notice window
            span = [start + dt.timedelta(days=i) for i in range(1, (leave - start).days)]
            hol = sorted({iso(d) for d in rng.sample(span, min(len(span), rng.choice([0, 1, 2]))) if d.weekday() < 5})
            f["hol"] = hol
            f["holnames"] = [rng.choice(HOL_POOL)[0] for _ in hol]
            # move notice date so the count is near n
            cnt = self._between(f["act"], f["leave"], set(hol))
            shift = cnt - n + rng.choice([0, 0, -1, 1])
            a = D(f["act"])
            while shift > 0:
                a += dt.timedelta(days=1)
                if a.weekday() < 5 and iso(a) not in hol:
                    shift -= 1
            f["act"] = iso(a)
        return f

    @staticmethod
    def _between(a, b, hol):
        d = D(a) + dt.timedelta(days=1)
        k = 0
        while d < D(b):
            if d.weekday() < 5 and iso(d) not in hol:
                k += 1
            d += dt.timedelta(days=1)
        return k

    def valid(self, f):
        if f["mode"] == "before":
            return D(f["act"]) < D(f["leave"])
        return D(f["act"]) >= D(f["start"])

    def preds(self, f):
        if f.get("maybe"):
            outs = {self.preds(dict(f, maybe=None, hol=sorted(f["hol"] + x)))["ok"] for x in ([], [f["maybe"]])}
            return {"ok": outs.pop() if len(outs) == 1 else None}
        hol = set(f["hol"])
        if f["mode"] == "within":
            return {"ok": D(f["act"]) <= D(bdays_after(f["start"], f["n"], hol))}
        return {"ok": self._between(f["act"], f["leave"], hol) >= f["n"]}

    def preds2(self, f):
        if f.get("maybe"):
            outs = {self.preds2(dict(f, maybe=None, hol=h))["ok"] for h in (f["hol"], sorted(f["hol"] + [f["maybe"]]))}
            return {"ok": outs.pop() if len(outs) == 1 else None}
        H = np.array(f["hol"], dtype="datetime64[D]")
        if f["mode"] == "within":
            s = np.datetime64(f["start"]) + 1
            cnt = int(np.busday_count(s, np.datetime64(f["act"]), holidays=H))
            return {"ok": cnt < f["n"]}
        cnt = int(np.busday_count(np.datetime64(f["act"]) + 1, np.datetime64(f["leave"]), holidays=H))
        return {"ok": cnt >= f["n"]}

    def val(self, f):
        if f["mode"] == "within":
            return bdays_after(f["start"], f["n"], set(f["hol"]))
        # latest notice date that still gives n business days before leave
        d = D(f["leave"]) - dt.timedelta(days=1)
        while self._between(iso(d), f["leave"], set(f["hol"])) < f["n"]:
            d -= dt.timedelta(days=1)
        return iso(d)

    def val2(self, f):
        H = np.array(f["hol"], dtype="datetime64[D]")
        if f["mode"] == "within":
            return str(np.busday_offset(np.datetime64(f["start"]), f["n"], roll="forward", holidays=H)
                       if np.is_busday(np.datetime64(f["start"]), holidays=H)
                       else np.busday_offset(np.datetime64(f["start"]), f["n"] - 1, roll="forward", holidays=H))
        # n business days strictly between notice and leave -> notice is the n-th business day before leave,
        # or any later non-business day before the next business day; latest date = day before the n-th-last bday...
        lv = np.datetime64(f["leave"])
        nth = np.busday_offset(lv, -f["n"], roll="forward", holidays=H)
        # notice may be as late as the day before `nth` counts as between? notice day excluded -> latest notice = nth - 1
        # but if days between nth-1 and nth are non-business the latest is simply nth - 1.
        return str(nth - 1)

    def fmtv(self, f, v):
        return fd(v, Sty(f).i("ds", 3), wd=True)

    def wrongs(self, f):
        hol = set(f["hol"])
        s = D(f["start"])
        out = []
        if f["mode"] == "within":
            out.append(iso(s + dt.timedelta(days=f["n"])))          # calendar days
            out.append(bdays_after(f["start"], f["n"], set()))       # forgot holidays
            out.append(bdays_after(f["start"], f["n"] - 1, hol))     # counted the start day
            out.append(bdays_after(f["start"], f["n"] + 1, hol))
        else:
            v = D(self.val(f))
            out += [iso(v + dt.timedelta(days=1)), iso(v - dt.timedelta(days=1)),
                    iso(D(f["leave"]) - dt.timedelta(days=f["n"])), iso(v + dt.timedelta(days=2))]
        return out

    def alts(self, f):
        a = {"act": [add_days(f["act"], d) for d in (-2, -1, 1, 2, 3)], "n": [f["n"] - 1, f["n"] + 1]}
        if f["hol"]:
            a["hol"] = [f["hol"][:-1]]
            a["holnames"] = []
        return a

    def flip(self, f, rng, want, keys=None):
        g = super().flip(f, rng, want, keys)
        if g is not None and g["hol"] != f["hol"]:
            g["holnames"] = f["holnames"][:len(g["hol"])]
        return g

    def edges(self, f, p):
        t = ["temporal", "numeric"]
        if f["hol"]:
            t.append("exception")
        if f.get("maybe"):
            t.append("missing_info")
        return t

    def render(self, f):
        st = Sty(f)
        ds = st.i("ds", 3)
        n = f["n"]
        who = f["who"][0]
        hols = "; ".join(f"{fd(h, ds, wd=True)} ({nm})" for h, nm in zip(f["hol"], f["holnames"]))
        maybe = (f" The office might also close on {fd(f['maybe'], ds, wd=True)} for a regional holiday; this has not been confirmed either way."
                 if f.get("maybe") else "")
        hl = (f"Business days are Monday to Friday, excluding these public holidays: {hols}." if f["hol"] else
              st.c("nohol", ["Business days are Monday to Friday; there are no public holidays in the period concerned.",
                             "Business days are Monday to Friday (no public holidays fall in this period)."])) + maybe
        dom = f["dom"]
        start = fd(f["start"], ds, wd=True)
        act = fd(f["act"], ds, wd=True)
        cnt = st.c("cnt", ["The day of {ev} itself is not counted; day 1 is the first business day after it.",
                           "Counting starts on the first business day after {ev}."])
        if dom == "return":
            pol = f"{f['org']} Electronics - returns\n- A return must be requested within {n} {plural(n, 'business day')} after the delivery date. {cnt.format(ev='delivery')}\n- {hl}\n- Items must be returned in their original packaging."
            scen = f"{who}'s order was delivered on {start}. {cap(f['who'][1])} requested a return on {act}."
        elif dom == "transfer":
            pol = f"{f['org']} Bank - payment disputes\n- A customer may dispute a card payment within {n} {plural(n, 'business day')} after the transaction is posted. {cnt.format(ev='posting')}\n- {hl}\n- Disputes can be opened in the app or by phone."
            scen = f"A payment on {who}'s card was posted on {start}. {cap(f['who'][1])} opened a dispute on {act}."
        elif dom == "cooling":
            pol = f"{f['org']} Home Improvements - contract terms\n- The customer may cancel this contract without penalty within {n} {plural(n, 'business day')} after signing it. {cnt.format(ev='signing')}\n- {hl}\n- Cancellations must be sent in writing."
            scen = f"{who} signed the contract on {start} and sent a written cancellation on {act}."
        elif dom == "records":
            pol = f"{f['org']} Health Clinic - records requests\n- Patients may appeal a records decision within {n} {plural(n, 'business day')} after the decision letter is dated. {cnt.format(ev='the letter date')}\n- {hl}\n- Appeals are reviewed by the privacy officer."
            scen = f"The decision letter to {who} was dated {start}. {cap(f['who'][1])} filed an appeal on {act}."
        elif dom == "warranty_reg":
            pol = f"{f['org']} Appliances - extended warranty\n- The product must be registered within {n} {plural(n, 'business day')} after installation to qualify for the extended warranty. {cnt.format(ev='installation')}\n- {hl}\n- Registration is free."
            scen = f"{who}'s dishwasher was installed on {start}, and {f['who'][1]} registered it online on {act}."
        else:  # notice
            pol = (f"{f['org']} Logistics - leave requests\n- Employees must give at least {n} {"business day's" if n == 1 else "business days'"} notice before the first day of planned leave. "
                   f"Only business days strictly between the day notice is given and the first day of leave count.\n- {hl}\n- Leave of more than two weeks needs a manager's approval.")
            scen = f"{who} gave notice on {act} for leave starting on {fd(f['leave'], ds, wd=True)}."
        return f"{pol}\n\n{st.c('lab', ['Situation: ', 'Case: ', ''])}{scen}"

    def pq(self, f, p):
        who, dom = f["who"][0], f["dom"]
        if dom == "notice":
            return dict(pos=[f"Did {who} give enough notice for the leave?", f"Does {who}'s notice meet the {f['n']}-business-day requirement?"],
                        neg=[f"Was {who}'s notice too short under the policy?", f"Did {who} fail to give enough notice?"],
                        cpos=f"{who} gave enough notice", cneg=f"{who}'s notice was too short",
                        speakers=[("The HR assistant told " + f["who"][2] + " that", "the HR assistant")])
        act = {"return": "the return request", "transfer": "the dispute", "cooling": "the cancellation",
               "records": "the appeal", "warranty_reg": "the registration"}[dom]
        return dict(pos=[f"Was {act} made within the allowed period?", f"Was {act} on time under the policy?"],
                    neg=[f"Was {act} made too late?", f"Did {who} miss the deadline for {act}?"],
                    cpos=f"{act} was on time", cneg=f"{act} was too late",
                    speakers=[("A customer service agent told " + f["who"][2] + " that", "the agent"), ("A friend told " + f["who"][2] + " that", "the friend")])

    def letter_q(self, f):
        if f["dom"] == "notice":
            return ["What is the latest date on which notice could have been given for this leave?"]
        act = {"return": "a return can be requested", "transfer": "the dispute can be opened", "cooling": "the contract can be cancelled",
               "records": "the appeal can be filed", "warranty_reg": "the product can be registered"}[f["dom"]]
        return [f"What is the last day on which {act} under the policy?"]


# =============================================================================================================
class DayWindow(Schema):
    """Calendar-day windows (N days; day 0 vs day 1 counting; crossing 29 February) and 'one year' warranties."""
    name = "day_window"
    quota = 800
    letter = True
    DOMS = ["trial", "return", "warranty365", "warranty_year", "insulin", "cooling14", "probation"]

    def sample(self, rng):
        dom = rng.choice(self.DOMS)
        yr = rng.choice([2027, 2027, 2028, 2028, 2025, 2026, 2031, 2032])
        f = {"dom": dom, "who": person(rng), "org": rng.choice(PLACES), "sty": rng.randrange(10 ** 9),
             "count": rng.choice(["day1", "day0"]), "conv": rng.choice(["feb28", "mar1"])}
        f["n"] = {"trial": rng.choice([7, 14, 30, 30, 60]), "return": rng.choice([14, 28, 30, 45, 60, 90]),
                  "warranty365": 365, "warranty_year": 1, "insulin": 28, "cooling14": 14,
                  "probation": rng.choice([60, 90, 90, 180])}[dom]
        if dom in ("warranty365", "warranty_year") or rng.random() < 0.35:
            # straddle 29 February
            ly = rng.choice([2024, 2028, 2032])
            if dom in ("warranty365", "warranty_year"):
                s = dt.date(ly - 1, rng.randint(3, 12), rng.randint(1, 28)) if rng.random() < 0.5 else dt.date(ly, rng.choice([1, 2]), rng.randint(1, 28))
                if rng.random() < 0.15:
                    s = dt.date(ly, 2, 29)
            else:
                s = dt.date(ly, 2, 29) - dt.timedelta(days=rng.randint(1, f["n"]))
        else:
            s = dt.date(yr, rng.randint(1, 12), rng.randint(1, 28))
        f["start"] = iso(s)
        last = D(self._last(f))
        f["act"] = iso(last + dt.timedelta(days=rng.choice([0, 0, 1, 1, -1, 2, -2, 365 - 366])))
        return f

    def _last(self, f):
        s = D(f["start"])
        if f["dom"] == "warranty_year":
            # ends on the same calendar date one year later (inclusive); 29 Feb -> per conv
            try:
                return iso(dt.date(s.year + 1, s.month, s.day))
            except ValueError:
                return iso(dt.date(s.year + 1, 3, 1) if f["conv"] == "mar1" else dt.date(s.year + 1, 2, 28))
        n = f["n"]
        return iso(s + dt.timedelta(days=n - 1 if f["count"] == "day1" else n))

    def _last2(self, f):
        y, m, d = (int(x) for x in f["start"].split("-"))
        if f["dom"] == "warranty_year":
            ny = y + 1
            if m == 2 and d == 29 and not isleap(ny):
                return f"{ny}-03-01" if f["conv"] == "mar1" else f"{ny}-02-28"
            return f"{ny:04d}-{m:02d}-{d:02d}"
        o = dt.date(y, m, d).toordinal() + f["n"] - (1 if f["count"] == "day1" else 0)
        return dt.date.fromordinal(o).isoformat()

    def valid(self, f):
        return D(f["act"]) >= D(f["start"])

    def preds(self, f):
        return {"ok": D(f["act"]) <= D(self._last(f))}

    def preds2(self, f):
        return {"ok": f["act"] <= self._last2(f)}

    def val(self, f):
        return self._last(f)

    def val2(self, f):
        return self._last2(f)

    def fmtv(self, f, v):
        return fd(v, Sty(f).i("ds", 3), wd=Sty(f).p("wdv", 0.3))

    def wrongs(self, f):
        s = D(f["start"])
        L = D(self._last(f))
        out = [iso(L + dt.timedelta(days=1)), iso(L - dt.timedelta(days=1))]
        if f["dom"] == "warranty_year":
            out.append(iso(s + dt.timedelta(days=365)))
            out.append(iso(s + dt.timedelta(days=364)))
        else:
            try:
                out.append(iso(dt.date(s.year, s.month + 1, s.day)) if s.month < 12 else iso(dt.date(s.year + 1, 1, s.day)))
            except ValueError:
                pass
            out.append(iso(L + dt.timedelta(days=2)))
        return out

    def alts(self, f):
        a = {"act": [add_days(f["act"], d) for d in (-2, -1, 1, 2)], "start": [add_days(f["start"], d) for d in (-1, 1, -2, 2)]}
        if f["dom"] != "warranty_year":
            a["count"] = ["day0" if f["count"] == "day1" else "day1"]
        if f["dom"] == "warranty_year" and f["start"][5:] == "02-29":
            a["conv"] = ["mar1" if f["conv"] == "feb28" else "feb28"]
        return a

    def edges(self, f, p):
        t = ["temporal", "numeric"]
        s, L = D(f["start"]), D(self._last(f))
        if any(s <= dt.date(y, 2, 29) <= L for y in range(s.year, L.year + 1) if isleap(y)):
            t.append("implicit")
        if f["start"][5:] == "02-29":
            t.append("exception")
        return t

    def render(self, f):
        st = Sty(f)
        ds = st.i("ds", 3)
        n, who, dom = f["n"], f["who"][0], f["dom"]
        cnt = (st.c("c1", ["The day of {ev} counts as day 1.", "Day 1 is the day of {ev} itself."]) if f["count"] == "day1" else
               st.c("c0", ["The day of {ev} is day 0; counting starts the next day.", "The {n} days are counted from the day after {ev}."]))
        start, act = fd(f["start"], ds, wd=st.p("wd", 0.3)), fd(f["act"], ds, wd=st.p("wd", 0.3))
        if dom == "trial":
            pol = f"{f['org']} Streaming - free trial terms\n- The free trial lasts {n} days. {cnt.format(ev='sign-up', n=n)} The trial ends at the end of its last day.\n- If you cancel on or before the last day of the trial, you are not charged.\n- One trial per household."
            scen = f"{who} signed up for the free trial on {start} and cancelled on {act}."
        elif dom == "return":
            pol = f"{f['org']} Outdoor Gear - return window\n- Items may be returned within {n} days of purchase. {cnt.format(ev='purchase', n=n)} Returns are accepted up to and including the last day of the window.\n- Worn footwear cannot be returned."
            scen = f"{who} bought a tent on {start} and brought it back unused on {act}."
        elif dom == "warranty365":
            pol = f"{f['org']} Tools - limited warranty\n- The warranty covers defects reported within 365 days of purchase. {cnt.format(ev='purchase', n=365)} Note that a 365-day period is not always the same as one calendar year.\n- Proof of purchase is required."
            scen = f"{who} bought a cordless drill on {start}. It stopped working and {f['who'][1]} reported the defect on {act}."
        elif dom == "warranty_year":
            cv = "1 March" if f["conv"] == "mar1" else "28 February"
            leapn = f" For purchases made on 29 February, the anniversary in a non-leap year is taken to be {cv}." if f["start"][5:] == "02-29" else ""
            pol = f"{f['org']} Appliances - one-year warranty\n- The warranty runs for one year: it covers defects reported on or before the first anniversary of the purchase date (the same calendar date one year later).{leapn}\n- Cosmetic damage is not covered."
            scen = f"{who} bought a microwave on {start} and reported a fault on {act}."
        elif dom == "insulin":
            pol = f"{f['org']} Pharmacy - storage advice\n- Once opened, a vial may be used for {n} days. {cnt.format(ev='first use', n=n)} Discard any remaining medicine after the last day.\n- Keep unopened vials in the refrigerator."
            scen = f"{who} opened a new vial on {start} and wants to use it on {act}."
        elif dom == "cooling14":
            pol = f"{f['org']} Online Courses - cancellation\n- You may cancel within {n} days of enrolment for a full refund. {cnt.format(ev='enrolment', n=n)} Cancellations are accepted up to the end of the last day.\n- Course materials must not have been downloaded."
            scen = f"{who} enrolled on {start}, downloaded nothing, and cancelled on {act}."
        else:  # probation
            pol = f"{f['org']} Hospital - probation\n- New staff are on probation for {n} days. {cnt.format(ev='the first day of work', n=n)} Probation ends at the end of its last day.\n- Probationary staff may not approve overtime."
            scen = f"{who} started work on {start}. On {act} {f['who'][1]} asked whether {f['who'][1]} {'were' if f['who'][1] == 'they' else 'was'} still a probationary employee."
        return f"{pol}\n\n{st.c('lab', ['Situation: ', 'Case: ', ''])}{scen}"

    def pq(self, f, p):
        who, dom = f["who"][0], f["dom"]
        sp = [("A store employee told " + f["who"][2] + " that", "the employee"), ("A friend told " + f["who"][2] + " that", "the friend")]
        m = {"trial": (f"Did {who} cancel within the free trial, so that {f['who'][1]} will not be charged?", f"Will {who} be charged because {f['who'][1]} cancelled after the trial ended?",
                       f"{who} cancelled within the trial", f"{who} cancelled after the trial ended"),
             "return": (f"Was the tent returned within the return window?", f"Was the tent returned too late?",
                        "the return was within the window", "the return was too late"),
             "warranty365": (f"Was the defect reported within the warranty period?", f"Was the defect reported after the warranty expired?",
                             "the defect was reported within the warranty period", "the warranty had already expired"),
             "warranty_year": (f"Is the fault covered by the one-year warranty?", f"Had the warranty already expired when the fault was reported?",
                               "the fault is covered", "the warranty had expired"),
             "insulin": (f"May {who} still use the vial on that day?", f"Should the vial already have been discarded by that day?",
                         "the vial may still be used that day", "the vial should already have been discarded"),
             "cooling14": (f"Is {who} entitled to a full refund?", f"Did {who} cancel too late for a refund?",
                           f"{who} cancelled in time for a full refund", f"{who} cancelled too late for a refund"),
             "probation": (f"Was {who} still on probation on that date?", f"Had {who}'s probation already ended by that date?",
                           f"{who} was still on probation", f"{who}'s probation had already ended")}[dom]
        return dict(pos=[m[0]], neg=[m[1]], cpos=m[2], cneg=m[3], speakers=sp)

    def letter_q(self, f):
        return {"trial": ["What is the last day of the free trial?"], "return": ["What is the last day on which the tent could be returned?"],
                "warranty365": ["What is the last day on which a defect is covered?"], "warranty_year": ["What is the last day the warranty covers?"],
                "insulin": ["What is the last day on which the opened vial may be used?"], "cooling14": ["What is the last day to cancel for a full refund?"],
                "probation": ["What is the last day of the probation period?"]}[f["dom"]]
