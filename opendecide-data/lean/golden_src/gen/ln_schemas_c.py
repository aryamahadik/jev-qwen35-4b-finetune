"""gen_logic_negation schemas, part C: short policies with an exception and an exception to the exception.

Every policy has (1) a Python decision function on the raw facts (numbers, categories) and (2) an independent logical
form over boolean atoms derived from the facts.  Fact combinations whose answer would depend on how an ambiguous
policy sentence is read are excluded (`valid`).  A twin pair changes exactly one fact so that the decision flips.
"""
from ln_engine import AND, IFF, NOT, OR, PEOPLE, art, cap, lit
from ln_schemas_a import mk, schema


class Policy:
    name = ""
    texts = []
    vars = {}

    def valid(self, f):
        return True


class Returns(Policy):
    name = "returns"
    texts = ["Items can be returned within 30 days of delivery. Sale items cannot be returned, unless they arrived damaged.",
             "You may return any item within 30 days of delivery. Items bought in the sale are final, except items "
             "that arrived damaged."]
    vars = {"days": [3, 7, 12, 18, 25, 29, 31, 35, 45, 60], "sale": [True, False], "damaged": [True, False]}
    ITEMS = ["lamp", "jacket", "blender", "rug", "desk chair", "kettle", "backpack", "coffee table", "toaster"]

    def valid(self, f):
        return not (f["days"] > 30 and f["damaged"])  # does 'damaged' also lift the 30-day limit? left unsaid

    def decide(self, f):
        return f["days"] <= 30 and (not f["sale"] or f["damaged"])

    def atoms(self, f):
        return {"W": f["days"] <= 30, "S": f["sale"], "D": f["damaged"]}

    def goal(self):
        return AND("W", OR(NOT("S"), "D"))

    def render(self, f, c):
        x, s = c["p"][0], c["p"][1]
        return (f"{x} bought {art(c['item'])} {'in the sale' if f['sale'] else 'at full price'}. It arrived "
                f"{'damaged' if f['damaged'] else 'in perfect condition'} {f['days']} days ago, and {s} wants to "
                f"return it.")

    def question(self, c):
        return f"Under this policy, can {c['p'][0]} return the {c['item']}?"

    def ctx(self, rng):
        return {"item": rng.choice(self.ITEMS)}


class GymFreeze(Policy):
    name = "gym_freeze"
    texts = ["Members can freeze their membership for up to three months a year. Members on the student plan cannot "
             "freeze their membership, except for a documented medical reason."]
    vars = {"months": [1, 2, 3, 4, 5], "student": [True, False], "reason": ["doc_med", "undoc_med", "travel"]}
    RT = {"doc_med": "while recovering from surgery, and {s} has a doctor's letter to show it",
          "undoc_med": "while recovering from a back injury, but {s} has no medical documentation",
          "travel": "while travelling abroad"}

    def valid(self, f):
        return not (f["months"] > 3 and f["reason"] == "doc_med")

    def decide(self, f):
        return f["months"] <= 3 and (not f["student"] or f["reason"] == "doc_med")

    def atoms(self, f):
        return {"M3": f["months"] <= 3, "St": f["student"], "Doc": f["reason"] == "doc_med"}

    def goal(self):
        return AND("M3", OR(NOT("St"), "Doc"))

    def render(self, f, c):
        x, s, o, p = c["p"]
        m = f["months"]
        return (f"{x} is on the {'student' if f['student'] else 'standard'} plan and wants to freeze {p} membership "
                f"for {m} {'month' if m == 1 else 'months'} {self.RT[f['reason']].format(s=s)}.")

    def question(self, c):
        return f"Under this policy, can {c['p'][0]} freeze the membership as requested?"

    def ctx(self, rng):
        return {}


class Bags(Policy):
    name = "checked_bag"
    texts = ["Each passenger may check one bag free of charge. Passengers on the Basic fare pay for every checked bag, "
             "unless they are frequent-flyer members. Bags over 23 kg always cost extra."]
    vars = {"fare": ["Basic", "Standard", "Flex"], "ff": [True, False], "w": [16, 19, 22, 23, 24, 26, 30]}

    def decide(self, f):
        return f["w"] <= 23 and (f["fare"] != "Basic" or f["ff"])

    def atoms(self, f):
        return {"Wt": f["w"] <= 23, "B": f["fare"] == "Basic", "FF": f["ff"]}

    def goal(self):
        return AND("Wt", OR(NOT("B"), "FF"))

    def render(self, f, c):
        x, s, o, p = c["p"]
        return (f"{x} is flying on the {f['fare']} fare and {'is' if f['ff'] else 'is not'} a frequent-flyer member. "
                f"{cap(p)} only checked bag weighs {f['w']} kg.")

    def question(self, c):
        return f"Under this policy, can {c['p'][0]} check the bag free of charge?"

    def ctx(self, rng):
        return {}


class Absence(Policy):
    name = "school_absence"
    texts = ["Outside exam week, an absence is excused if and only if a parent sends a note. During exam week, an "
             "absence is excused if and only if the student has a doctor's note."]
    vars = {"exam": [True, False], "parent": [True, False], "doctor": [True, False]}

    def decide(self, f):
        return f["doctor"] if f["exam"] else f["parent"]

    def atoms(self, f):
        return {"E": f["exam"], "Pn": f["parent"], "Dn": f["doctor"]}

    def goal(self):
        return OR(AND("E", "Dn"), AND(NOT("E"), "Pn"))

    def render(self, f, c):
        x, s, o, p = c["p"]
        wk = "during exam week" if f["exam"] else "in an ordinary week, not exam week"
        return (f"{x} missed school on a {c['day']} {wk}. {cap(p)} parent {'sent' if f['parent'] else 'did not send'} "
                f"a note, and {s} {'had' if f['doctor'] else 'did not have'} a doctor's note.")

    def question(self, c):
        return f"Under these rules, is {c['p'][0]}'s absence excused?"

    def ctx(self, rng):
        return {"day": rng.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])}


class Flood(Policy):
    name = "home_insurance"
    texts = ["The policy covers water damage in the home. It does not cover flood damage unless the flood add-on was "
             "bought."]
    vars = {"cause": ["a burst pipe", "a leaking dishwasher", "an overflowing bath", "a river flood", "a flash flood",
                      "coastal flooding"], "addon": [True, False]}
    FLOOD = {"a river flood", "a flash flood", "coastal flooding"}

    def decide(self, f):
        return f["cause"] not in self.FLOOD or f["addon"]

    def atoms(self, f):
        return {"Fl": f["cause"] in self.FLOOD, "Ad": f["addon"]}

    def goal(self):
        return OR(NOT("Fl"), "Ad")

    def render(self, f, c):
        x = c["p"][0]
        return (f"{x}'s kitchen was damaged by water from {f['cause']}. {x} "
                f"{'bought' if f['addon'] else 'did not buy'} the flood add-on.")

    def question(self, c):
        return f"Under this policy, is the damage to {c['p'][0]}'s kitchen covered?"

    def ctx(self, rng):
        return {}


class Grant(Policy):
    name = "travel_grant"
    texts = ["The travel grant is open to full-time students. Part-time students in their final year may also apply; "
             "other part-time students may not."]
    vars = {"ft": [True, False], "year": ["first", "second", "final"]}

    def decide(self, f):
        return f["ft"] or f["year"] == "final"

    def atoms(self, f):
        return {"FT": f["ft"], "Fin": f["year"] == "final"}

    def goal(self):
        return OR("FT", "Fin")

    def render(self, f, c):
        x, s, o, p = c["p"]
        return f"{x} is a {'full-time' if f['ft'] else 'part-time'} student in {p} {f['year']} year."

    def question(self, c):
        return f"Under these rules, can {c['p'][0]} apply for the travel grant?"

    def ctx(self, rng):
        return {}


class Pharmacy(Policy):
    name = "pharmacy_collection"
    texts = ["Any adult may collect a prescription on a patient's behalf. Controlled medicines, however, must be "
             "collected by the patient in person, unless the patient has registered a named representative, who may "
             "then collect them."]
    vars = {"controlled": [True, False], "registered": [True, False]}

    def decide(self, f):
        return not f["controlled"] or f["registered"]

    def atoms(self, f):
        return {"Ctl": f["controlled"], "Reg": f["registered"]}

    def goal(self):
        return OR(NOT("Ctl"), "Reg")

    def render(self, f, c):
        x, y = c["p"][0], c["y"][0]
        med = "a controlled painkiller" if f["controlled"] else "an antibiotic cream"
        return (f"{x}'s prescription is for {med}. {y}, an adult {c['rel']} of {x}'s, "
                f"{'is' if f['registered'] else 'is not'} registered as {x}'s named representative and goes to the "
                f"pharmacy to collect it.")

    def question(self, c):
        return f"Under this policy, can {c['y'][0]} collect {c['p'][0]}'s prescription?"

    def ctx(self, rng):
        return {"rel": rng.choice(["neighbour", "friend", "cousin", "colleague"])}


class Overtime(Policy):
    name = "overtime"
    texts = ["Employees are paid time-and-a-half for hours over 40 in a week. Managers are not paid overtime, except for "
             "hours worked on public holidays."]
    vars = {"mgr": [True, False], "hours": [36, 38, 40, 41, 42, 45, 48], "hol": [True, False]}

    def valid(self, f):
        return not (f["mgr"] and f["hol"])  # how the holiday exception meets the 40-hour rule is left unsaid

    def decide(self, f):
        return f["hours"] > 40 and (not f["mgr"] or f["hol"])

    def atoms(self, f):
        return {"O40": f["hours"] > 40, "Mg": f["mgr"], "Hol": f["hol"]}

    def goal(self):
        return AND("O40", OR(NOT("Mg"), "Hol"))

    def render(self, f, c):
        x = c["p"][0]
        role = "a warehouse manager" if f["mgr"] else "a warehouse assistant (not a manager)"
        hol = "including a shift on a public holiday" if f["hol"] else "none of them on a public holiday"
        return f"{x}, {role}, worked {f['hours']} hours last week, {hol}."

    def question(self, c):
        return f"Under this policy, is {c['p'][0]} paid any overtime for last week?"

    def ctx(self, rng):
        return {}


class Pets(Policy):
    name = "pets"
    texts = ["Tenants may keep one cat or one dog. Dogs over 15 kg are not allowed, except registered assistance dogs."]
    vars = {"dog": [True, False], "w": [4, 6, 9, 12, 15, 16, 22, 30], "assist": [True, False]}

    def valid(self, f):
        return f["dog"] or (not f["assist"] and f["w"] <= 6)

    def decide(self, f):
        return (not f["dog"]) or f["w"] <= 15 or f["assist"]

    def atoms(self, f):
        return {"Dg": f["dog"], "Hv": f["w"] > 15, "As": f["assist"]}

    def goal(self):
        return OR(NOT("Dg"), NOT("Hv"), "As")

    def render(self, f, c):
        x, s, o, p = c["p"]
        if not f["dog"]:
            return f"{x} wants to keep {p} cat in the flat. The cat weighs {f['w']} kg."
        a = "is a registered assistance dog" if f["assist"] else "is not an assistance dog"
        return f"{x} wants to keep {p} dog in the flat. The dog weighs {f['w']} kg and {a}."

    def question(self, c):
        return f"Under these rules, may {c['p'][0]} keep the pet in the flat?"

    def ctx(self, rng):
        return {}


class Pool(Policy):
    name = "pool"
    texts = ["The pool is open to all residents. Children under 12 may use the pool when an adult is with them, and "
             "not otherwise. During swimming lessons, the pool is closed to everyone except the lesson participants."]
    vars = {"age": [7, 9, 11, 12, 13, 15], "adult": [True, False], "lesson": [True, False], "part": [True, False]}

    def valid(self, f):
        if not f["lesson"] and f["part"]:
            return False
        return not (f["lesson"] and f["part"] and f["age"] < 12 and not f["adult"])

    def decide(self, f):
        if f["lesson"]:
            return f["part"]
        return f["age"] >= 12 or f["adult"]

    def atoms(self, f):
        return {"L": f["lesson"], "Pt": f["part"], "Ch": f["age"] < 12, "Ad": f["adult"]}

    def goal(self):
        return OR(AND("L", "Pt"), AND(NOT("L"), OR(NOT("Ch"), "Ad")))

    def render(self, f, c):
        x, s, o, p = c["p"]
        if f["lesson"]:
            when = ("during a swimming lesson, as one of its participants" if f["part"]
                    else "during a swimming lesson that " + s + " is not taking part in")
        else:
            when = "at a time when no lesson is running"
        comp = f"with {p} {c['adult']}" if f["adult"] else f"on {p} own"
        return f"{x}, a resident aged {f['age']}, wants to swim {when}, {comp}."

    def question(self, c):
        return f"Under these rules, may {c['p'][0]} use the pool at that time?"

    def ctx(self, rng):
        return {"adult": rng.choice(["father", "mother", "aunt", "uncle", "grandmother"])}


class Library(Policy):
    name = "library_loans"
    texts = ["Members may have up to 8 books on loan at a time. Reference books may not be borrowed, except overnight "
             "by members with a staff card."]
    vars = {"have": [3, 5, 6, 7, 8], "ref": [True, False], "staff": [True, False], "night": [True, False]}

    def decide(self, f):
        return f["have"] + 1 <= 8 and (not f["ref"] or (f["staff"] and f["night"]))

    def atoms(self, f):
        return {"Cap": f["have"] + 1 <= 8, "R": f["ref"], "Sc": f["staff"], "N": f["night"]}

    def goal(self):
        return AND("Cap", OR(NOT("R"), AND("Sc", "N")))

    def render(self, f, c):
        x = c["p"][0]
        book = "a reference book on tax law" if f["ref"] else "a novel"
        per = "overnight" if f["night"] else "for two weeks"
        return (f"{x} already has {f['have']} books on loan and wants to borrow {book} {per}. {x} "
                f"{'has' if f['staff'] else 'does not have'} a staff card.")

    def question(self, c):
        return f"Under these rules, may {c['p'][0]} borrow the book?"

    def ctx(self, rng):
        return {}


class LateWork(Policy):
    name = "late_work"
    texts = ["Assignments submitted after the deadline lose 10% of the marks for each day late. A student with an "
             "approved extension loses nothing, unless the work arrives after the extended deadline."]
    vars = {"late": [0, 1, 2, 4], "ext": [0, 1, 3, 5]}

    def decide(self, f):
        return f["late"] > f["ext"]

    def atoms(self, f):
        return {"Lt": f["late"] > 0, "Ex": f["ext"] > 0, "Af": f["late"] > f["ext"]}

    def goal(self):
        return AND("Lt", OR(NOT("Ex"), "Af"))

    def render(self, f, c):
        x = c["p"][0]
        sub = ("on the deadline day" if f["late"] == 0 else
               f"{f['late']} {'day' if f['late'] == 1 else 'days'} after the original deadline")
        ext = ("had no extension" if f["ext"] == 0 else
               f"had an approved extension of {f['ext']} {'day' if f['ext'] == 1 else 'days'}")
        return f"{x} submitted the essay {sub}. {x} {ext}."

    def question(self, c):
        return f"Under this policy, does {c['p'][0]} lose any marks?"

    def ctx(self, rng):
        return {}


class Parking(Policy):
    name = "parking_bay"
    texts = ["The loading bay may be used for up to 30 minutes by delivery vehicles only. Blue-badge holders may also "
             "use it, but not between 7 a.m. and 9 a.m."]
    vars = {"kind": ["delivery", "badge", "other"], "mins": [10, 20, 30, 35, 50], "rush": [True, False]}

    def valid(self, f):
        # the 30-minute limit is only stated for delivery vehicles; blue-badge stays are kept within it
        return not (f["kind"] == "badge" and f["mins"] > 30)

    def decide(self, f):
        if f["kind"] == "delivery":
            return f["mins"] <= 30
        if f["kind"] == "badge":
            return not f["rush"]
        return False

    def atoms(self, f):
        return {"Dv": f["kind"] == "delivery", "Bb": f["kind"] == "badge", "T30": f["mins"] <= 30, "Rh": f["rush"]}

    def goal(self):
        return OR(AND("Dv", "T30"), AND("Bb", NOT("Rh")))

    def render(self, f, c):
        x = c["p"][0]
        who = {"delivery": f"{x}, a delivery driver in a delivery van,",
               "badge": f"{x}, a blue-badge holder,", "other": f"{x}, who is neither a delivery driver nor a "
                                                               f"blue-badge holder,"}[f["kind"]]
        when = c["rush_t"] if f["rush"] else c["calm_t"]
        return f"{who} parked in the loading bay for {f['mins']} minutes starting at {when}."

    def question(self, c):
        return f"Under these rules, was {c['p'][0]} allowed to park there?"

    def ctx(self, rng):
        return {"rush_t": rng.choice(["7:15 a.m.", "7:40 a.m.", "8:10 a.m.", "8:20 a.m."]),
                "calm_t": rng.choice(["10:05 a.m.", "11:30 a.m.", "2:15 p.m.", "4:40 p.m."])}


class HotelCancel(Policy):
    name = "hotel_cancellation"
    texts = ["Bookings can be cancelled free of charge up to 48 hours before arrival. Non-refundable rates cannot be "
             "cancelled free of charge, unless the hotel itself has changed the booking."]
    vars = {"h": [96, 72, 49, 48, 47, 30, 12], "nonref": [True, False], "changed": [True, False]}

    def valid(self, f):
        return not (f["h"] < 48 and f["changed"])  # whether a hotel change also lifts the 48-hour limit is unsaid

    def decide(self, f):
        return f["h"] >= 48 and (not f["nonref"] or f["changed"])

    def atoms(self, f):
        return {"T48": f["h"] >= 48, "NR": f["nonref"], "Ch": f["changed"]}

    def goal(self):
        return AND("T48", OR(NOT("NR"), "Ch"))

    def render(self, f, c):
        x = c["p"][0]
        rate = "a non-refundable rate" if f["nonref"] else "a flexible rate"
        ch = "The hotel has changed the booking." if f["changed"] else "The hotel has not changed the booking."
        return f"{x} booked {rate} at {c['hotel']} and wants to cancel {f['h']} hours before arrival. {ch}"

    def question(self, c):
        return f"Under this policy, can {c['p'][0]} cancel free of charge?"

    def ctx(self, rng):
        return {"hotel": rng.choice(["the Alder Inn", "the Harbour Lodge", "the Linden Hotel", "the Seaview Hotel",
                                     "the Station Hotel"])}


class CarRental(Policy):
    name = "car_rental"
    texts = ["Drivers must be at least 21 to rent a car. Drivers under 25 pay a young-driver fee, unless they are "
             "renting on a company account."]
    vars = {"age": [19, 20, 21, 22, 24, 25, 26, 35], "company": [True, False]}

    def decide(self, f):
        return f["age"] >= 21 and (f["age"] >= 25 or f["company"])

    def atoms(self, f):
        return {"A21": f["age"] >= 21, "A25": f["age"] >= 25, "Co": f["company"]}

    def goal(self):
        return AND("A21", OR("A25", "Co"))

    def render(self, f, c):
        x = c["p"][0]
        acc = "on a company account" if f["company"] else "privately, not on a company account"
        return f"{x}, who is {f['age']}, wants to rent a car {acc}."

    def question(self, c):
        return f"Under these rules, can {c['p'][0]} rent a car without paying a young-driver fee?"

    def ctx(self, rng):
        return {}


class Museum(Policy):
    name = "museum_entry"
    texts = ["Entry is free for children under 16. Adults pay $12, except on the first Sunday of each month, when "
             "entry is free for everyone, unless a special exhibition is running."]
    vars = {"age": [8, 12, 15, 16, 17, 30, 45, 70], "first_sun": [True, False], "special": [True, False]}

    def valid(self, f):
        return not (f["age"] < 16 and f["special"])  # whether children pay during special exhibitions is unsaid

    def decide(self, f):
        return f["age"] < 16 or (f["first_sun"] and not f["special"])

    def atoms(self, f):
        return {"Ch": f["age"] < 16, "FS": f["first_sun"], "Sp": f["special"]}

    def goal(self):
        return OR("Ch", AND("FS", NOT("Sp")))

    def render(self, f, c):
        x = c["p"][0]
        day = "the first Sunday of the month" if f["first_sun"] else f"an ordinary {c['day']}"
        sp = "while a special exhibition is running" if f["special"] else "when no special exhibition is running"
        return f"{x}, aged {f['age']}, visits the museum on {day}, {sp}."

    def question(self, c):
        return f"Under these rules, is entry free for {c['p'][0]}?"

    def ctx(self, rng):
        return {"day": rng.choice(["Saturday", "Tuesday", "Wednesday", "Friday"])}


POLICIES = [Returns(), GymFreeze(), Bags(), Absence(), Flood(), Grant(), Pharmacy(), Overtime(), Pets(), Pool(),
            Library(), LateWork(), Parking(), HotelCancel(), CarRental(), Museum()]


@schema("policy_exceptions", 480)
def s_policy(rng):
    pol = rng.choice(POLICIES)
    for _ in range(50):
        f = {k: rng.choice(v) for k, v in pol.vars.items()}
        if pol.valid(f):
            break
    else:
        return None
    d = pol.decide(f)
    alts = []
    for k, vals in pol.vars.items():
        for v in vals:
            if v == f[k]:
                continue
            g = dict(f)
            g[k] = v
            if pol.valid(g) and pol.decide(g) != d:
                alts.append(g)
    if not alts:
        return None
    g = rng.choice(alts)
    p = rng.choice(PEOPLE)
    y = rng.choice([q for q in PEOPLE if q[0] != p[0]])
    c = {"p": p, "y": y}
    c.update(pol.ctx(rng))
    text = rng.choice(pol.texts)
    q = pol.question(c)
    out = []
    for facts in (f, g):
        at = pol.atoms(facts)
        prem = [lit(a, v) for a, v in sorted(at.items())]
        out.append(mk(f"{text} {pol.render(facts, c)}", q, "policy", "exception", prem, pol.goal(),
                      "yes" if pol.decide(facts) else "no", pol.name))
    rng.shuffle(out)
    return out


assert IFF  # re-exported helpers kept for symmetry with parts A/B
