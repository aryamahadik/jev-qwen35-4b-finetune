"""gen_msn_fault: who is in the wrong under an explicit agreement between people (yes/no, labels by construction,
single-fact twins).

Each item states a short agreement or shared norm between two or more people (meeting-room booking, carpool, lending
a car, group project, pet-sitting, family curfew, splitting a restaurant bill, group-chat privacy, trimming a
neighbour's tree, deli-counter tickets) and a timeline of what each person did. The question asks about ONE person;
the answer is computed from the agreement's terms only. Both parties can be at fault, so the model must attribute
fault to the right person; obligations can depend on what the other person did first (multi-hop), on deadlines and
grace periods (temporal / numeric), on quantifiers (every day, at least, twice) and on exceptions.

Questions (qid):
  wrong      "Under the agreement above, was X in the wrong?" / "Did X break the agreement above?"   yes <=> X breached
  kept       "Did X keep to the agreement above?"                                                    yes <=> no breach
  est_wrong  "Do the stated facts establish that X broke the agreement above?"            yes <=> breach (unknown -> no)
  pay        (lending only) "Under the agreement above, must X pay for the repair?"
  under      (bill only) "Did X pay less than the agreement above requires?"
Every base item has a twin (meta.twin_of) that changes exactly one fact so the answer flips. Deterministic (seed 20261103).
"""
import copy
import datetime as dt
import random
import re

from gen_msn_rules import Schema, sty
from msn_common import MONTHS, WEEKDAYS, cap, edge_join, fmt_time, num, person, plural, row, write_gen

KEY = "gen_msn_fault"
SEED = 20261103
N_PAIRS = 3000


def T(m, style):
    """minutes after midnight -> clock text"""
    m %= 24 * 60
    return fmt_time(m // 60, m % 60, style)


class Fault(Schema):
    roles = ()
    extra_q = None  # (qid, template) for schema-specific question

    def verdict(self, p, f):
        return self.breach(p, f, f["_q"])


# ---------------------------------------------------------------------------------------------------------------
class RoomBooking(Fault):
    name = "room_booking"
    roles = ("booker", "taker")

    def params(self, rng):
        return {"g": rng.choice([10, 15, 20]), "S": rng.choice([9, 10, 11, 13, 14, 15]) * 60 + rng.choice([0, 30]),
                "ts": rng.randrange(3), "room": rng.choice(["Room Juniper", "the Oak meeting room", "Huddle Room 3", "the Blue Room"]),
                "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        g = p["g"]
        return "Office meeting-room policy", [
            f"A room booked in the shared calendar belongs to the person who booked it for that time slot.",
            f"If the booker has not arrived {g} minutes after the booked start time, the booking is released: from that "
            f"minute on, anyone may use the room and the booker has no claim to it.",
            "Rooms that are not booked are first come, first served."]

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["other"] = person(rng, exclude=(f["who"][0],))
        g = p["g"]
        f["b"] = rng.choice([2, g - 5, g - 1, g, g + 3, g + 8])  # taker enters at S+b
        f["a"] = f["b"] + rng.choice([2, 5, 12])  # booker arrives later than the taker
        if f["a"] == g:
            f["a"] += 1
        f["booked"] = rng.random() < 0.9
        return f

    def alts(self, p, f):
        g = p["g"]
        return {"b": [2, g - 3, g, g + 4], "a": [f["b"] + 2, g + 6, g + 12] + ([g - 1] if g - 1 > f["b"] else []), "booked": [True, False]}

    def valid(self, p, f):
        return f["a"] > f["b"] and f["a"] != p["g"] and f["b"] >= 0

    def breach(self, p, f, role):
        g = p["g"]
        if role == "taker":
            return f["booked"] and f["b"] < g
        # booker insisted the taker leave: wrong if there was no booking, or it had been released before the booker arrived
        return (not f["booked"]) or f["a"] > g

    def story(self, p, f, rng=None):
        A, B = f["who"][0], f["other"][0]
        S, ts = p["S"], p["ts"]
        bk = (f"{A} had booked {p['room']} from {T(S, ts)} to {T(S + 60, ts)} in the shared calendar." if f["booked"] else
              f"Nobody had booked {p['room']} that afternoon; {A} had meant to book it for {T(S, ts)} but forgot.")
        return (f"{bk} At {T(S + f['b'], ts)} the room was empty, so {B} went in and started a call. {A} arrived at "
                f"{T(S + f['a'], ts)} and insisted that {B} leave because the room was {A}'s.")

    def names(self, f):
        return {"booker": f["who"], "taker": f["other"]}

    def edges(self, p, f):
        t = ["temporal", "multi_hop"]
        if f["b"] == p["g"]:
            t.append("numeric")
        if not f["booked"]:
            t.append("exception")
        return t


# ---------------------------------------------------------------------------------------------------------------
class Carpool(Fault):
    name = "carpool"
    roles = ("driver", "rider")

    def params(self, rng):
        dep = rng.choice([7 * 60 + 30, 7 * 60 + 40, 8 * 60])
        return {"dep": dep, "txt": dep - rng.choice([30, 40, 60]), "w": rng.choice([5, 10]), "ts": rng.randrange(3),
                "spot": rng.choice(["the corner of Pine and 3rd", "the library car park", "the bus shelter on Mill Road"]), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        ts = p["ts"]
        return "Carpool agreement", [
            f"Pickup is at {p['spot']}. Riders must be at the pickup point by {T(p['dep'], ts)}, and the driver must not leave before {T(p['dep'], ts)}.",
            f"A rider who will not need the ride must text the driver by {T(p['txt'], ts)}.",
            # reviewer fix: the old wording ('has not texted') left the driver's duty undefined after a 'running behind' text
            f"Unless the rider has cancelled by text by {T(p['txt'], ts)}, a driver whose rider has not arrived by "
            f"{T(p['dep'], ts)} must wait {p['w']} more minutes and may then leave without them."]

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["other"] = person(rng, exclude=(f["who"][0],))
        dep, w = p["dep"], p["w"]
        f["show"] = rng.random() < 0.6
        f["arr"] = dep + rng.choice([-10, -2, 0, 3, 8])  # rider arrival (if show)
        f["texted"] = rng.choice([None, p["txt"] - 15, p["txt"] + 10])  # minutes; None = no text
        f["left"] = dep + rng.choice([-5, 0, 2, w, w + 3])
        return f

    def alts(self, p, f):
        dep, w = p["dep"], p["w"]
        return {"show": [True, False], "arr": [dep - 5, dep, dep + 4], "texted": [None, p["txt"] - 15, p["txt"] + 10],
                "left": [dep - 5, dep, dep + 2, dep + w, dep + w + 3]}

    def rider_rode(self, f):
        return f["show"] and f["arr"] <= f["left"]

    def breach(self, p, f, role):
        dep, w = p["dep"], p["w"]
        if role == "rider":
            if f["show"]:
                return f["arr"] > dep
            return not (f["texted"] is not None and f["texted"] <= p["txt"])
        # driver: in the wrong only if the rider did not ride and had not cancelled in time, and the driver left
        # before the departure time + the waiting period (leaving early with the rider aboard harms no one)
        cancelled = (not f["show"]) and f["texted"] is not None and f["texted"] <= p["txt"]
        if f["left"] < dep:
            return True  # reviewer fix: rule 1 ('must not leave before') is unconditional, read literally
        if self.rider_rode(f) or cancelled:
            return False
        return f["left"] < dep + w

    def story(self, p, f, rng=None):
        D, R = f["who"][0], f["other"][0]
        ts = p["ts"]
        parts = []
        if f["texted"] is not None:
            parts.append(f"{R} texted {D} at {T(f['texted'], ts)} to say {f['other'][1]} would not need the ride that day." if not f["show"] else
                         f"{R} texted {D} at {T(f['texted'], ts)} saying {f['other'][1]} was running a bit behind.")
        if f["show"]:
            if f["arr"] <= f["left"]:
                parts.append(f"{R} reached the pickup point at {T(f['arr'], ts)}.")
                parts.append(f"{D} drove off with {R} at {T(max(f['left'], f['arr']), ts)}." if f["left"] >= f["arr"] else "")
            else:
                parts.append(f"{D} drove off alone at {T(f['left'], ts)}.")
                parts.append(f"{R} reached the pickup point at {T(f['arr'], ts)}, after {D} had gone.")
        else:
            parts.append(f"{D} drove off alone at {T(f['left'], ts)}.")
            parts.append(f"{R} never came to the pickup point that morning.")
        return " ".join(x for x in parts if x)

    def names(self, f):
        return {"driver": f["who"], "rider": f["other"]}

    def edges(self, p, f):
        t = ["temporal", "multi_hop"]
        if f["left"] in (p["dep"], p["dep"] + p["w"]) or (f["show"] and f["arr"] == p["dep"]):
            t.append("numeric")
        if f["texted"] is not None:
            t.append("exception")
        return t


# ---------------------------------------------------------------------------------------------------------------
FUEL = ["a quarter full", "half full", "three-quarters full", "full"]


class Lending(Fault):
    name = "lending"
    roles = ("borrower",)
    extra_q = ("pay", ["Under the agreement above, must {X} pay for the repair?", "According to the agreement above, is {X} the one who has to pay for the repair?"])

    def params(self, rng):
        item = rng.choice([("car", "drive to"), ("van", "move furniture to"), ("pickup truck", "haul firewood to")])
        return {"item": item, "day": rng.randrange(7), "noon": rng.choice([12 * 60, 18 * 60, 10 * 60]), "ts": rng.randrange(3), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        it = p["item"][0]
        return "Lending agreement", [
            f"The owner lends the borrower the {it} until {WEEKDAYS[p['day']]} at {T(p['noon'], p['ts'])}; it must be back by then.",
            f"The {it} must be returned with the fuel tank at least as full as when it was borrowed.",
            f"Repairs needed because of normal use or wear are paid by the owner. Damage caused by misuse (driving it off-road, "
            f"overloading it, or letting someone who is not insured drive it) is paid by the borrower."]

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["other"] = person(rng, exclude=(f["who"][0],))
        f["late"] = rng.choice([-120, -15, 0, 20, 180])
        f["f0"] = rng.randrange(1, 4)
        f["f1"] = rng.choice([f["f0"] - 1, f["f0"], min(3, f["f0"] + 1)])
        f["dmg"] = rng.choice(["none", "wear", "misuse_offroad", "misuse_uninsured", "misuse_overload", "wear"])
        return f

    def alts(self, p, f):
        if f["_q"] == "pay":
            return {"dmg": ["wear", "misuse_offroad", "misuse_uninsured", "misuse_overload"]}
        return {"late": [-60, 0, 25], "f1": [f["f0"] - 1, f["f0"], min(3, f["f0"] + 1)]}

    def valid(self, p, f):
        # reviewer fix: in breach questions a 'misuse' story (uninsured driver, overloading, off-road) made the answer
        # ambiguous (the agreement calls it misuse but only allocates repair cost), so misuse appears only in 'pay' items
        if f["_q"] != "pay" and f["dmg"].startswith("misuse"):
            return False
        return 0 <= f["f1"] <= 3 and (f["_q"] != "pay" or f["dmg"] != "none")

    def breach(self, p, f, role):
        if f["_q"] == "pay":
            return f["dmg"].startswith("misuse")
        return f["late"] > 0 or f["f1"] < f["f0"]

    def story(self, p, f, rng=None):
        B, O = f["who"], f["other"][0]
        it, use = p["item"]
        ts = p["ts"]
        due = p["noon"]
        ret = due + f["late"]
        day = WEEKDAYS[p["day"]]
        rday = day if 0 <= ret < 24 * 60 else (WEEKDAYS[(p["day"] + (1 if ret >= 24 * 60 else -1)) % 7])
        s = (f"{B[0]} borrowed {O}'s {it} to {use} {['a friend\'s place', 'the countryside', 'the new flat'][sty(f, 'a', 3)]}; the tank was "
             f"{FUEL[f['f0']]} when {B[1]} picked it up. {cap(B[1])} returned it on {rday} at {T(ret, ts)} with the tank {FUEL[f['f1']]}.")
        s += {"none": "",
              "wear": f" A week later the {it}'s worn brake pads needed replacing, which the mechanic said was ordinary wear.",
              "misuse_offroad": f" {cap(B[1])} had taken it down a rocky forest track, and afterwards the {it} needed a new exhaust.",
              "misuse_uninsured": f" {cap(B[1])} let a cousin who is not insured on it drive for an hour, and the cousin scraped a door that now needs repair.",
              "misuse_overload": f" {cap(B[1])} loaded it well beyond its weight limit, and the rear suspension then needed repair."}[f["dmg"]]
        return s

    def names(self, f):
        return {"borrower": f["who"]}

    def edges(self, p, f):
        t = []
        if f["_q"] == "pay":
            t += ["exception", "implicit"] if f["dmg"] == "misuse_uninsured" else ["exception"]
        else:
            t += ["temporal", "quantifier"]
            if f["late"] == 0 or f["f1"] == f["f0"]:
                t.append("numeric")
        return t


# ---------------------------------------------------------------------------------------------------------------
class GroupProject(Fault):
    name = "group_project"
    roles = ("member", "editor")

    def params(self, rng):
        return {"dl": rng.choice([17, 18, 20]) * 60, "grace": rng.choice([60, 120]), "ts": rng.randrange(3),
                "course": rng.choice(["the marketing report", "the lab write-up", "the history presentation", "the design proposal"]), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        ts = p["ts"]
        return f"Team agreement for {p['course']}", [
            f"Each member uploads their own section to the shared folder by Thursday at {T(p['dl'], ts)}.",
            f"The editor compiles all sections into the final file by Friday at noon.",
            f"If any section is missing at the Thursday deadline, the editor must message the whole group within "
            f"{p['grace'] // 60} {plural(p['grace'] // 60, 'hour')} of the deadline, and compiles whatever sections exist by Friday at noon."]

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["other"] = person(rng, exclude=(f["who"][0],))
        dl = p["dl"]
        f["up"] = rng.choice([dl - 180, dl - 5, dl, dl + 30, dl + 24 * 60 - 60, None])  # member upload (Thu minutes; >1440 = Fri)
        f["msg"] = rng.choice([None, dl + 20, dl + p["grace"], dl + p["grace"] + 45])
        f["comp"] = rng.choice([24 * 60 + 11 * 60, 24 * 60 + 12 * 60, 24 * 60 + 14 * 60])
        return f

    def alts(self, p, f):
        dl, g = p["dl"], p["grace"]
        return {"up": [dl - 60, dl, dl + 30, None], "msg": [None, dl + 20, dl + g, dl + g + 45],
                "comp": [24 * 60 + 11 * 60, 24 * 60 + 12 * 60, 24 * 60 + 14 * 60]}

    def missing(self, p, f):
        return f["up"] is None or f["up"] > p["dl"]

    def breach(self, p, f, role):
        dl, g = p["dl"], p["grace"]
        if role == "member":
            return self.missing(p, f)
        late_comp = f["comp"] > 24 * 60 + 12 * 60
        if self.missing(p, f):
            return late_comp or f["msg"] is None or f["msg"] > dl + g
        return late_comp

    def when(self, m, ts):
        return ("Thursday" if m < 24 * 60 else "Friday") + " at " + T(m, ts)

    def story(self, p, f, rng=None):
        M, E = f["who"], f["other"][0]
        ts = p["ts"]
        s = [f"{E} was the editor."]
        s.append(f"{M[0]} uploaded {M[3]} section on {self.when(f['up'], ts)}." if f["up"] is not None else
                 f"{M[0]} never uploaded {M[3]} section.")
        if f["msg"] is not None:
            s.append(f"{E} messaged the group on {self.when(f['msg'], ts)} about {M[0]}'s section.")
        else:
            s.append(f"{E} did not send the group any message.")
        s.append(f"{E} finished compiling the final file on Friday at {T(f['comp'], ts)}.")
        return " ".join(s)

    def names(self, f):
        return {"member": f["who"], "editor": f["other"]}

    def edges(self, p, f):
        t = ["temporal", "multi_hop"]
        if f["up"] == p["dl"] or f["msg"] == p["dl"] + p["grace"] or f["comp"] == 36 * 60:
            t.append("numeric")
        if self.missing(p, f):
            t.append("exception")
        return t


# ---------------------------------------------------------------------------------------------------------------
class PetSitting(Fault):
    name = "pet_sitting"
    roles = ("sitter",)
    can_hide = True

    def params(self, rng):
        return {"w": rng.choice([20, 30, 45]), "days": rng.choice([2, 3]), "pet": rng.choice([("Biscuit", "dog"), ("Luna", "dog"), ("Pepper", "dog"), ("Mochi", "dog")]), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        n = p["pet"][0]
        return "Pet-sitting agreement", [
            f"Feed {n} twice every day, once in the morning and once in the evening.",
            f"Walk {n} for at least {p['w']} minutes in total every day.",
            f"If {n} vomits or refuses food, text the owner the same day."]

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["other"] = person(rng, exclude=(f["who"][0],))
        d = p["days"]
        f["feeds"] = tuple(rng.choice([2, 2, 2, 1]) for _ in range(d))
        f["walks"] = tuple(rng.choice([p["w"], p["w"] + 10, p["w"] - 5, p["w"] + 25]) for _ in range(d))
        f["vomit"] = rng.choice([None, 0, d - 1])
        f["texted"] = rng.choice([True, False])
        return f

    def alts(self, p, f):
        d = p["days"]
        out = {"texted": [True, False, "unknown"] if f["vomit"] is not None else [], "vomit": [None, 0]}
        # single-day changes are expressed as whole-tuple alternatives differing in one day
        fe, wa = list(f["feeds"]), list(f["walks"])
        alts_f, alts_w = [], []
        for i in range(d):
            for v in (1, 2):
                x = fe.copy(); x[i] = v; alts_f.append(tuple(x))
            for v in (p["w"] - 5, p["w"], p["w"] + 15):
                x = wa.copy(); x[i] = v; alts_w.append(tuple(x))
        out["feeds"] = alts_f
        out["walks"] = alts_w
        return out

    def breach(self, p, f, role):
        if any(x < 2 for x in f["feeds"]) or any(x < p["w"] for x in f["walks"]):
            return True
        if f["vomit"] is not None:
            if f["texted"] == "unknown":
                return None
            return not f["texted"]
        return False

    def story(self, p, f, rng=None):
        S, O = f["who"], f["other"][0]
        n = p["pet"][0]
        days = ["Friday", "Saturday", "Sunday"][: p["days"]]
        s = [f"{S[0]} looked after {O}'s dog {n} from {days[0]} to {days[-1]}."]
        for i, d in enumerate(days):
            fe = "fed " + n + (" in the morning and in the evening" if f["feeds"][i] == 2 else " only in the morning")
            s.append(f"On {d}, {S[1]} {fe} and walked {n} for {f['walks'][i]} minutes in total.")
            if f["vomit"] == i:
                s.append(f"That {d} {n} vomited after dinner." + ("" if f["texted"] == "unknown" else
                          (f" {S[0]} texted {O} about it that evening." if f["texted"] else f" {S[0]} did not tell {O}.")))
        return " ".join(s).replace("walked " + n + " for", "walked " + n + " for")

    def hide(self, p, f, rng):
        if f["vomit"] is not None and f["texted"] in (True, False) and all(x == 2 for x in f["feeds"]) and all(x >= p["w"] for x in f["walks"]):
            g = copy.deepcopy(f)
            g["texted"] = "unknown"
            return g
        return None

    def fill(self, p, f, want):
        g = copy.deepcopy(f)
        g["texted"] = not want  # want=True means we want breach? handled by caller mapping
        return g

    def names(self, f):
        return {"sitter": f["who"]}

    def edges(self, p, f):
        t = ["quantifier", "numeric"]
        if any(x == p["w"] for x in f["walks"]):
            t.append("temporal")
        if f["vomit"] is not None:
            t.append("exception")
        if f["texted"] == "unknown":
            t.append("missing_info")
        return t


# ---------------------------------------------------------------------------------------------------------------
class Curfew(Fault):
    name = "curfew"
    roles = ("teen",)

    def params(self, rng):
        return {"school": rng.choice([21 * 60 + 30, 22 * 60]), "wkend": rng.choice([23 * 60, 23 * 60 + 30, 24 * 60]),
                "x": rng.choice([15, 30]), "ts": rng.randrange(3), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        ts = p["ts"]
        return "Family agreement", [
            f"On school nights (Sunday to Thursday) you must be home by {T(p['school'], ts)}; on Friday and Saturday nights, by "
            f"{T(p['wkend'], ts)}" + (" (midnight)" if p["wkend"] == 24 * 60 else "") + ".",
            f"If you are going to be late, call before your curfew time, not after.",
            f"A call made before curfew excuses being late only if you are home within {p['x']} minutes after curfew."]

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["other"] = person(rng, exclude=(f["who"][0],))
        f["day"] = rng.randrange(7)
        cur = self.cur(p, f)
        f["home"] = cur + rng.choice([-20, 0, 10, p["x"], p["x"] + 10, 60])
        f["call"] = rng.choice([None, cur - 30, cur - 1, cur + 5])
        return f

    def cur(self, p, f):
        return p["wkend"] if f["day"] in (4, 5) else p["school"]

    def alts(self, p, f):
        cur = self.cur(p, f)
        return {"home": [cur - 10, cur, cur + 10, cur + p["x"], cur + p["x"] + 15], "call": [None, cur - 20, cur + 5],
                "day": [2, 4, 5, 6]}

    def breach(self, p, f, role):
        cur = self.cur(p, f)
        if f["home"] <= cur:
            return False
        excused = f["call"] is not None and f["call"] < cur and f["home"] <= cur + p["x"]
        return not excused

    def story(self, p, f, rng=None):
        K, P = f["who"], f["other"][0]
        ts = p["ts"]
        d = WEEKDAYS[f["day"]]
        s = f"On {d} night {K[0]} was out with friends and got home at {T(f['home'], ts)}."
        if f["call"] is not None:
            s += f" {cap(K[1])} had called home at {T(f['call'], ts)} and told {P}, {K[3]} {['parent', 'guardian', 'step-parent'][sty(f, 'a', 3)]}, that {K[1]} would be late."
        else:
            s += f" {cap(K[1])} did not call home."
        return s

    def names(self, f):
        return {"teen": f["who"]}

    def edges(self, p, f):
        cur = self.cur(p, f)
        t = ["temporal", "exception"]
        if f["home"] in (cur, cur + p["x"]):
            t.append("numeric")
        if f["day"] == 6:
            t.append("implicit")  # Sunday counts as a school night
        return t


# ---------------------------------------------------------------------------------------------------------------
class BillSplit(Fault):
    name = "bill_split"
    roles = ("diner",)
    extra_q = ("under", ["Did {X} pay less than the agreement above requires?"])

    def params(self, rng):
        return {"n": rng.choice([3, 4, 5]), "dseed": rng.randrange(10 ** 6), "rest": rng.choice(["Lotus Garden", "Trattoria Sole", "The Copper Pot", "Casa Verde"])}

    def rules(self, p):
        return "How the group agreed to split the bill", [
            "Everyone pays for the main dishes and drinks they ordered themselves.",
            "Shared starters and the tip are split equally among everyone at the table.",
            "Nobody has to pay for anything they did not order, apart from their equal part of the shared starters and tip."]

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        others = []
        ex = [f["who"][0]]
        for _ in range(p["n"] - 1):
            q = person(rng, exclude=tuple(ex))
            ex.append(q[0])
            others.append(q)
        f["others"] = tuple(others)
        f["own"] = rng.choice([14, 16, 18, 22, 25, 27]) + rng.choice([0, 0.5])
        f["drink"] = rng.choice([0, 3.5, 4, 6, 7.5])
        f["starters"] = rng.choice([12, 15, 18, 20, 24])
        f["tip"] = rng.choice([10, 12, 15, 20])
        while round((f["starters"] + f["tip"]) * 100) % p["n"]:
            f["tip"] += 1  # keep the equal share an exact number of cents
        share = round(f["own"] + f["drink"] + (f["starters"] + f["tip"]) / p["n"], 2)
        f["paid"] = round(share + rng.choice([-5, -1, -0.5, 0, 0, 1, 3]), 2)
        return f

    def owed(self, p, f):
        return round(f["own"] + f["drink"] + (f["starters"] + f["tip"]) / p["n"], 2)

    def alts(self, p, f):
        o = self.owed(p, f)
        return {"paid": [round(o - 2, 2), round(o - 0.5, 2), o, round(o + 1, 2)]}

    def breach(self, p, f, role):
        return round(f["paid"], 2) < round(self.owed(p, f), 2) - 1e-9

    def money(self, x):
        return f"${x:.2f}"

    def story(self, p, f, rng=None):
        X = f["who"]
        n = p["n"]
        names = [X[0]] + [o[0] for o in f["others"]]
        grp = ", ".join(names[:-1]) + " and " + names[-1]
        s = (f"{grp} had dinner at {p['rest']}. They shared starters costing {self.money(f['starters'])} and left a tip of "
             f"{self.money(f['tip'])}. {X[0]} ordered a main dish for {self.money(f['own'])}")
        s += (f" and a drink for {self.money(f['drink'])}." if f["drink"] else " and only drank tap water.")
        s += f" The others' orders came to different amounts. {X[0]} put in {self.money(f['paid'])}."
        return s

    def names(self, f):
        return {"diner": f["who"]}

    def edges(self, p, f):
        t = ["numeric", "quantifier"]
        if abs(f["paid"] - self.owed(p, f)) < 0.01:
            t.append("exception")
        return t


# ---------------------------------------------------------------------------------------------------------------
class ChatPrivacy(Fault):
    name = "chat_privacy"
    roles = ("sharer",)

    def params(self, rng):
        return {"grp": rng.choice(["the book club chat", "the flatmates' group chat", "the hiking group chat", "the cousins' chat"]), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        return f"Agreement for {p['grp']}", [
            "Nothing posted in the chat may be shared with anyone outside the group without the consent of the person who posted it.",
            "Sharing includes screenshots, forwarding, and retelling the content.",
            "Something the poster has already made public themselves may be shared freely."]

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["poster"] = person(rng, exclude=(f["who"][0],))
        f["out"] = person(rng, exclude=(f["who"][0], f["poster"][0]))
        f["whose"] = rng.choice(["other", "other", "own"])
        f["how"] = rng.choice(["screenshot", "forward", "retell"])
        f["recip"] = rng.choice(["outsider", "outsider", "member"])
        f["consent"] = rng.choice(["poster", "none", "third", "none"])
        f["public"] = rng.random() < 0.2
        return f

    def alts(self, p, f):
        return {"whose": ["own", "other"], "recip": ["outsider", "member"], "consent": ["poster", "none", "third"], "public": [True, False]}

    def breach(self, p, f, role):
        if f["whose"] == "own" or f["recip"] == "member" or f["public"]:
            return False
        return f["consent"] != "poster"

    def story(self, p, f, rng=None):
        A, Pp, O = f["who"], f["poster"][0], f["out"][0]
        news = ["that " + Pp + " is applying for a job abroad", "a photo of " + Pp + "'s new tattoo",
                "that " + Pp + " and " + f["poster"][3] + " partner had split up"][sty(f, "a", 3)]
        if f["whose"] == "own":
            posted = f"{A[0]} had posted in {p['grp']} " + ["that " + A[1] + " is applying for a job abroad", "a photo of " + A[2 + 1] + " new tattoo", "that " + A[1] + " had failed " + A[3] + " driving test"][sty(f, "a", 3)] + "."
        else:
            posted = f"{Pp} had posted in {p['grp']} {news}."
        how = {"screenshot": "sent a screenshot of the message", "forward": "forwarded the message", "retell": "told"}[f["how"]]
        who2 = f"{O}, who is not in the chat," if f["recip"] == "outsider" else f"{O}, who is also a member of the chat,"
        act = (f"{A[0]} {how} to {who2[:-1]}." if f["how"] != "retell" else f"{A[0]} told {who2} about it over coffee.")
        cons = {"poster": f" {Pp} had said beforehand that it was fine to pass it on.", "none": "",
                "third": f" Another group member said it would be fine; {Pp} was not asked."}[f["consent"]] if f["whose"] == "other" else ""
        pub = (f" {Pp} had already announced it on {['Instagram', 'Facebook', 'LinkedIn'][sty(f, 'b', 3)]} for everyone to see."
               if f["public"] and f["whose"] == "other" else "")
        return posted + " " + act + cons + pub

    def valid(self, p, f):
        return not (f["whose"] == "own" and (f["consent"] != "none" or f["public"]))

    def names(self, f):
        return {"sharer": f["who"]}

    def edges(self, p, f):
        t = ["exception", "negation"]
        if f["how"] == "retell":
            t.append("reported_speech")
        if f["consent"] == "third":
            t.append("implicit")
        return t


# ---------------------------------------------------------------------------------------------------------------
class TreeTrim(Fault):
    name = "tree_trim"
    roles = ("trimmer",)

    def params(self, rng):
        return {"tree": rng.choice(["apple tree", "oak", "cherry tree", "maple"]), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        return "Neighbour agreement", [
            "Each neighbour may cut back branches that hang over onto their own side of the fence, but only up to the fence line.",
            "No one may cut branches on the owner's side of the fence, or cut into the trunk, without the owner's agreement.",
            "Cut branches are offered back to the tree's owner."]

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["owner"] = person(rng, exclude=(f["who"][0],))
        f["cut"] = rng.choice(["overhang", "overhang", "beyond", "trunk"])
        f["agree"] = rng.random() < 0.3
        f["offered"] = rng.random() < 0.7
        return f

    def alts(self, p, f):
        return {"cut": ["overhang", "beyond", "trunk"], "agree": [True, False], "offered": [True, False]}

    def breach(self, p, f, role):
        if f["cut"] != "overhang" and not f["agree"]:
            return True
        return not f["offered"]

    def story(self, p, f, rng=None):
        A, O = f["who"], f["owner"][0]
        c = {"overhang": f"cut off the branches of {O}'s {p['tree']} that hung over {A[3]} side, stopping exactly at the fence line",
             "beyond": f"cut back {O}'s {p['tree']}, reaching over the fence to take off branches on {O}'s side as well",
             "trunk": f"cut the overhanging branches of {O}'s {p['tree']} and also sawed a notch into its trunk to stop it leaning"}[f["cut"]]
        s = f"{A[0]} {c}."
        if f["cut"] != "overhang":
            s += (f" {O} had agreed to this in advance." if f["agree"] else f" {O} had not been asked.")
        s += (f" {cap(A[1])} then offered the cut wood to {O}." if f["offered"] else f" {cap(A[1])} put the cut wood in {A[3]} own green bin without offering it to {O}.")
        return s

    def valid(self, p, f):
        return not (f["cut"] == "overhang" and f["agree"])

    def names(self, f):
        return {"trimmer": f["who"]}

    def edges(self, p, f):
        t = ["exception", "negation"]
        if f["cut"] != "overhang":
            t.append("quantifier")
        return t


# ---------------------------------------------------------------------------------------------------------------
class DeliQueue(Fault):
    name = "deli_queue"
    roles = ("customer",)

    def params(self, rng):
        return {"shop": rng.choice(["Rossi's Deli", "the Market Street butcher", "the bakery counter at FreshMart", "Kowalski's Deli"]), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        return f"Counter rules at {p['shop']}", [
            "Customers are served in ticket-number order.",
            "If your number is called and you are not at the counter, you must take a new ticket.",
            "Customers with a pre-order may collect it at the side window without a ticket."]

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["num"] = rng.randint(20, 90)
        f["missed"] = rng.random() < 0.5
        f["newticket"] = rng.random() < 0.4
        f["preorder"] = rng.random() < 0.2
        return f

    def alts(self, p, f):
        return {"missed": [True, False], "newticket": [True, False], "preorder": [True, False]}

    def breach(self, p, f, role):
        # the customer asked to be served at the counter ahead of the number now being called
        if f["preorder"]:
            return False
        return f["missed"] and not f["newticket"]

    def story(self, p, f, rng=None):
        C = f["who"]
        n = f["num"]
        if f["preorder"]:
            return (f"{C[0]} had placed a pre-order by phone. {cap(C[1])} went to the side window and collected it while "
                    f"number {n + 3} was being served at the counter, without taking a ticket.")
        s = f"{C[0]} took ticket number {n}."
        if f["missed"]:
            s += f" When number {n} was called, {C[1]} was outside taking a phone call."
        else:
            s += f" {cap(C[1])} waited at the counter the whole time."
        if f["missed"] and f["newticket"]:
            s += f" Coming back, {C[1]} took a new ticket, number {n + 7}, and was served when it was called."
        elif f["missed"]:
            s += f" Coming back while number {n + 3} was being served, {C[1]} asked to be served next using ticket {n}."
        else:
            s += f" {cap(C[1])} was served as soon as number {n} was called."
        return s

    def valid(self, p, f):
        return not (f["preorder"] and (f["missed"] or f["newticket"])) and not (not f["missed"] and f["newticket"])

    def names(self, f):
        return {"customer": f["who"]}

    def edges(self, p, f):
        t = ["exception"]
        if f["missed"]:
            t.append("multi_hop")
        return t


SCHEMAS = [RoomBooking(), Carpool(), Lending(), GroupProject(), PetSitting(), Curfew(), BillSplit(), ChatPrivacy(),
           TreeTrim(), DeliQueue()]

ROLE_Q = {
    "wrong": ["Under the agreement above, was {X} in the wrong?", "Did {X} break the agreement above?"],
    "kept": ["Did {X} keep to the agreement above?", "Did {X} act in line with the agreement above?"],
    "est_wrong": ["Do the stated facts establish that {X} broke the agreement above?"],
}
DEFS = {
    "wrong": {"yes": "Judged only by the agreement's terms, this person failed at least one of their own obligations (a deadline, "
                     "amount, condition or limit) and no stated exception excuses it; what others did wrong does not count.",
              "no": "Judged only by the agreement's terms, this person met all of their own obligations, or a stated exception "
                    "or the other person's earlier action released them; faults of other people do not count."},
    "kept": {"yes": "Judged only by the agreement's terms, this person met all of their own obligations, or a stated exception "
                    "or the other person's earlier action released them; faults of other people do not count.",
             "no": "Judged only by the agreement's terms, this person failed at least one of their own obligations (a deadline, "
                   "amount, condition or limit) and no stated exception excuses it."},
    "est_wrong": {"yes": "The stated facts are enough to show that this person broke one of their own obligations under the "
                         "agreement, with no stated exception applying.",
                  "no": "Either the facts show this person kept the agreement, or a fact needed to decide (for example whether "
                        "they sent a required message) is not stated, so a breach is not established."},
    "pay": {"yes": "Under the agreement, the repair was caused by misuse by the borrower (off-road driving, overloading, or an "
                   "uninsured driver they allowed), so the borrower pays.",
            "no": "Under the agreement, the repair comes from normal use or wear, so the owner pays, even if the borrower broke "
                  "other terms such as the return time or fuel level."},
    "under": {"yes": "The amount the person put in is less than their own dishes and drinks plus an equal share of the shared "
                     "starters and tip (computed to the cent).",
              "no": "The amount the person put in is at least their own dishes and drinks plus an equal share of the shared "
                    "starters and tip; paying extra is not paying less."},
}


def gold(qid, v):
    if qid in ("wrong", "est_wrong", "pay", "under"):
        return "yes" if v is True else "no"
    return "yes" if v is False else "no"  # kept


def render(s, p, f, qid, qvar):
    title, lines = s.rules(p)
    rl = "\n".join(f"{i + 1}. {ln}" for i, ln in enumerate(lines))
    state = f"{title}\n{rl}\n\nWhat happened: {s.story(p, f)}"
    state = re.sub(r"(a\.m\.|p\.m\.)\.", r"\1", state)
    X = s.names(f)[f["_q"]][0] if f["_q"] in s.names(f) else s.names(f)[s.roles[0]][0]
    if qid in ROLE_Q:
        tmpl = ROLE_Q[qid][qvar % len(ROLE_Q[qid])]
    else:
        tmpl = s.extra_q[1][qvar % len(s.extra_q[1])]
    return state, tmpl.format(X=X)


def main():
    rng = random.Random(SEED)
    rows, seen = [], set()
    per = N_PAIRS // len(SCHEMAS)
    stats = {}
    for s in SCHEMAS:
        made, tries = 0, 0
        while made < per and tries < 200000:
            tries += 1
            p = s.params(rng)
            f = s.facts(rng, p)
            # which question
            if s.extra_q and rng.random() < 0.5:
                qid = s.extra_q[0]
                f["_q"] = qid
            else:
                r = rng.random()
                qid = "wrong" if r < 0.45 else "kept" if r < 0.8 else "est_wrong"
                f["_q"] = rng.choice(s.roles)
            if not s.valid(p, f):
                continue
            base, twin = f, None
            if qid == "est_wrong" and s.can_hide and rng.random() < 0.7:
                h = s.hide(p, f, rng)
                if h is None:
                    continue
                base = h
                twin = copy.deepcopy(h)
                twin["texted"] = False  # supplying the missing fact: no text -> breach -> yes
            else:
                if s.verdict(p, f) is None:
                    continue
                twin = s.one_flip(p, f, rng)
                if twin is None:
                    continue
            diff = [k for k in set(base) | set(twin) if base.get(k) != twin.get(k)]
            assert len(diff) == 1, (s.name, diff)
            vb, vt = s.verdict(p, base), s.verdict(p, twin)
            if qid != "est_wrong" and (vb is None or vt is None):
                continue
            gb, gt = gold(qid, vb), gold(qid, vt)
            if gb == gt:
                continue
            qvar = rng.randrange(4)
            sb, qb = render(s, p, base, qid, qvar)
            st, qt = render(s, p, twin, qid, qvar)
            if sb == st or sb in seen or st in seen:
                continue
            seen.update({sb, st})  # every state text used once
            rid = f"{KEY}-{s.name}-{made:04d}"
            role = f["_q"]
            ob = {"schema": s.name, "about": role, "breach": vb}
            ot = {"schema": s.name, "about": role, "breach": vt}
            rows.append(row(KEY, rid, sb, qb, gb, qid, edge_join(sorted(set(s.edges(p, base)))), ob, f"{s.name}:{qid}"))
            rows.append(row(KEY, rid + "-twin", st, qt, gt, qid, edge_join(sorted(set(s.edges(p, twin)))), ot,
                            f"{s.name}:{qid}", twin_of=rid))
            made += 1
        stats[s.name] = made
    print("pairs per schema:", stats)
    pairs = [rows[i:i + 2] for i in range(0, len(rows), 2)]
    rng.shuffle(pairs)
    rows = [r for pr in pairs[:N_PAIRS] for r in pr]
    write_gen(KEY, rows, DEFS,
              notes=("program-generated multi-party agreements (10 schemas); the question asks about one named person; "
                     "both parties can be at fault; conditional obligations, grace periods, deadlines, per-day quantifiers, "
                     "bill arithmetic to the cent, consent from the wrong person; single-fact twins flip the answer "
                     "(meta.twin_of); negated framing ('keep to the agreement') and missing-info framing."),
              dataset_desc="gen_msn_fault (program generator, golden_src/gen/gen_msn_fault.py)")


if __name__ == "__main__":
    main()
