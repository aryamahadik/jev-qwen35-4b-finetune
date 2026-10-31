"""gen_constraints domains, part A: shipping, meeting rooms, meeting slots, health plans, flights, suppliers,
candidates, apartments, hotels, car rentals.  All names of companies, products, plans and people are invented."""
import datetime as dt
from fractions import Fraction as Fr

from cst_core import GE, GT, LE, LT, MISSING, NA, Attr, CmpCon, FnCon, cap, fmt_date, fmt_dur, fmt_money, fmt_time, \
    lex_word, modal, unk
from cst_dom_base import (FIRST, LAST, PEOPLE, Domain, grid, mk_bool, mk_cat, mk_cmp, mk_cond, mk_date, mk_derived,
                          mk_exc, mk_implicit, mk_range, mk_set, mk_tie, mk_window, mk_xunit, money_fmt)

D0 = dt.date(2026, 1, 5).toordinal()


def base_day(rng, weekday=True, span=900):
    d = D0 + rng.randint(0, span)
    while weekday and dt.date.fromordinal(d).weekday() >= 5:
        d += 1
    return d


def fd(o, st):
    return fmt_date(o, st["date"])


def ft(m, st):
    return fmt_time(m, st["time"])


def art(s):
    return ("an " if s[0].lower() in "aeio" else "a ") + s


def pick_name(rng, avoid=()):
    while True:
        n = rng.choice(FIRST)
        if n not in avoid:
            return n


CITIES = ["Leeds", "Denver", "Toronto", "Porto", "Adelaide", "Tucson", "Galway", "Utrecht", "Halifax", "Dunedin",
          "Spokane", "Aberdeen", "Tampere", "Cork", "Savannah", "Boise", "Kraków", "Lyon", "Brisbane", "Omaha"]

# ================================================================================================ shipping
SHIP_LABELS = ["Swiftpost Priority", "Swiftpost Economy", "Northline Ground", "Northline Express", "Parcelwing Standard",
               "Parcelwing Next Day", "Cargoline Saver", "Cargoline Plus", "BlueRoute Direct", "BlueRoute Value",
               "Keystone Courier", "Keystone Freight", "Harborlink Air", "Harborlink Ground", "Meridian Mail Standard",
               "Meridian Mail Express", "Falconer Rapid", "Falconer Basic", "Redkite Parcels", "Redkite Priority",
               "Tidewater Tracked", "Tidewater Saver", "Copperline Courier", "Copperline Economy", "Lanternpost First",
               "Lanternpost Second", "Waypoint Express", "Waypoint Ground", "Pinecrest Delivery", "Pinecrest Premium",
               "Orbit Parcel Standard", "Orbit Parcel Plus", "Stonebridge Freight", "Stonebridge Courier",
               "Hollyway Home", "Hollyway Business", "Quayside Express", "Quayside Economy", "Brightdrop Standard",
               "Brightdrop Priority"]
SHIP_ITEMS = ["framed print", "pair of hiking boots", "vintage camera", "box of handmade candles", "ceramic vase",
              "laptop", "set of textbooks", "wool blanket", "bicycle helmet", "record player", "espresso grinder",
              "board game collection", "quilt", "guitar pedal", "set of kitchen knives"]
SHIP_ATTRS = [
    Attr("price", "money", "Price", lo=599, hi=6999, step=50, cents=True, vp=["cost {c} {v}", "be priced at {c} {v}"],
         field=("Max price", None), pr="costs {v}"),
    Attr("transit", "num", "Transit time", lo=1, hi=10, unit=("business day", "business days"), cls="count",
         vp=["take {c} {v} in transit", "be in transit for {c} {v}"], field=("Max transit", None), pr="takes {v}"),
    Attr("cover", "money", "Insurance cover", lo=0, hi=100000, step=2500,
         vp=["include insurance cover of {c} {v}"], field=(None, "Min insurance cover"), pr="insures up to {v}"),
    Attr("maxw", "num", "Weight limit", lo=2, hi=30, unit=" kg", vp=["have a weight limit of {c} {v}"],
         pr="accepts parcels up to {v}"),
    Attr("tracking", "bool", "Tracking", p=0.7, vp=["include tracking", "come with tracking"], noun="tracking",
         pr=("includes tracking", "has no tracking")),
    Attr("signature", "bool", "Signature needed", p=0.4, vp=["require a signature on delivery"],
         anti=["be deliverable without a signature"], pr=("requires a signature on delivery", "needs no signature")),
    Attr("pickup", "bool", "Home pickup", p=0.5, vp=["offer home pickup", "include pickup from the sender's address"],
         noun="home pickup", pr=("offers home pickup", "has no home pickup")),
    Attr("pobox", "bool", "Delivers to PO boxes", p=0.55, vp=["deliver to PO boxes"],
         pr=("delivers to PO boxes", "does not deliver to PO boxes")),
]


def _ship_ctx(rng):
    today = base_day(rng)
    ship = today + rng.randint(0, 3)
    while dt.date.fromordinal(ship).weekday() >= 5:
        ship += 1
    hol = None
    if rng.random() < 0.35:
        hol = ship + rng.randint(1, 6)
        while dt.date.fromordinal(hol).weekday() >= 5:
            hol += 1
    return {"today": today, "ship": ship, "hol": hol, "name": pick_name(rng), "item": rng.choice(SHIP_ITEMS),
            "dest": rng.choice(CITIES), "value": 100 * 25 * rng.randint(4, 36)}


def _ship_arrive_ctx(ctx, st, ci):
    h = ""
    if ctx["hol"]:
        h = f" {fd(ctx['hol'], st)} is a public holiday with no deliveries."
    return (f"The parcel will be handed over on {fd(ctx['ship'], st)}; transit times count business days "
            f"(Monday to Friday) after that day.{h}")


SHIPPING = Domain(
    "shipping", "shipping option", "shipping options", "Service", SHIP_LABELS, SHIP_ATTRS,
    makers=[
        (3, "price", mk_cmp("price", LE, 0.25, 0.75)),
        (2, "transit", mk_cmp("transit", LE, 0.2, 0.6, strict_p=0.15)),
        (3, "arrive", mk_derived("arrive", ["transit"], lambda ctx: ("bizd", ("x", "ship"), ("a", "transit"),
                                                                      (ctx["hol"],) if ctx["hol"] else ()),
                                 LE, lambda rng, ctx, D: ctx["ship"] + rng.randint(2, 11),
                                 ["arrive {c} {v}", "be delivered {c} {v}"], fd, ctx_fn=_ship_arrive_ctx, step=1,
                                 tags=("temporal", "multi_hop"), cls="date", vd=(1, 2, 3, -1, -2, -3), group="transit")),
        (2, "cover", mk_implicit("cover", GE, lambda rng, ctx, D: ctx["value"],
                                 lambda rng, ctx, t: (f"The {ctx['item']} is worth {{v}}.", None),
                                 "insure the parcel for at least the item's value", vfmt=money_fmt())),
        (2, "maxw", mk_xunit("maxw", GE, "lb", Fr(10, 22), Fr(100000, 220462), [x * 10 + 5 for x in range(5, 55, 3)],
                             ["have a weight limit of {c} {v}", "accept parcels weighing {c} {v}"], "(1 kg = 2.2 lb)",
                             dec=1)),
        (2, "tracking", mk_bool("tracking")),
        (1, "signature", mk_bool("signature", want=False)),
        (1, "pickup", mk_bool("pickup")),
        (1, "pobox", mk_bool("pobox")),
    ],
    ties=[mk_tie("cheapest", [(("a", "price"), "min")], "the lowest price", ["price"]),
          mk_tie("fastest", [(("a", "transit"), "min"), (("a", "price"), "min")],
                 "the shortest transit time (if still tied, the lower price)", ["transit", "price"]),
          mk_tie("cover", [(("a", "cover"), "max")], "the highest insurance cover", ["cover"])],
    ctx_fn=_ship_ctx,
    contexts=[("I need to send a {item} to a customer in {dest}.", "{name} needs to send a {item} to a customer in {dest}."),
              ("I'm mailing a {item} to a friend in {dest}.", "{name} is mailing a {item} to a friend in {dest}."),
              ("Our office has to courier a {item} to a client in {dest}.", "{name}'s office has to courier a {item} to a client in {dest}.")],
    questions=["Which shipping option should {name} book{ifany}?", "Which shipping option meets all of the requirements{ifany}?",
               "Which service satisfies every stated requirement for this parcel{ifany}?"],
    intros=["Quotes for this parcel:", "Shipping options available:", "Services and quotes:"],
    subjects=["Shipping the {item}", "Courier for {dest}"],
    def_extra="business days skip weekends and stated holidays",
    nice=["pickup", "pobox"],
)

# ================================================================================================ meeting rooms
ROOM_LABELS = [f"{x} Room" for x in ["Birch", "Cedar", "Maple", "Harbor", "Summit", "Atlas", "Juniper", "Quarry", "Linden",
                                      "Orchard", "Beacon", "Aspen", "Willow", "Granite", "Meadow", "Falcon", "Heron",
                                      "Cobalt", "Indigo", "Saffron", "Tidewater", "Lantern", "Compass", "Foundry",
                                      "Pioneer", "Riverside", "Skyline", "Hawthorn", "Magnolia", "Sequoia"]]
PURPOSES = ["quarterly planning session", "client pitch", "interview panel", "training workshop", "budget review",
            "product demo", "team retrospective", "board briefing", "onboarding session", "design review"]


def _ato(rng, ctx, o):
    f = o.get("afrom")
    f = 9 * 60 if (f is None or unk(f)) else f
    return min(21 * 60, f + rng.randrange(60, 541, 15))


ROOM_ATTRS = [
    Attr("cap", "num", "Seats", lo=2, hi=30, unit=("seat", "seats"), cls="count", vp=["seat {c} {v}", "hold {c} {v}"],
         field=(None, "Min seats"), pr="seats {v}", missing_ok=False),
    Attr("afrom", "time", "Free from", lo=7 * 60, hi=14 * 60, step=15, cls="time", pr="is free from {v}",
         missing_ok=False),
    Attr("ato", "time", "Free until", lo=8 * 60, hi=21 * 60, step=15, cls="time", gen=_ato, pr="is free until {v}",
         missing_ok=False),
    Attr("screen", "bool", "Video screen", p=0.6, vp=["have a video screen", "have a screen for video calls"],
         noun="a video screen", pr=("has a video screen", "has no video screen")),
    Attr("board", "bool", "Whiteboard", p=0.6, vp=["have a whiteboard"], noun="a whiteboard",
         pr=("has a whiteboard", "has no whiteboard")),
    Attr("access", "bool", "Step-free access", p=0.7, vp=["have step-free access", "be step-free"],
         noun="step-free access", pr=("has step-free access", "has no step-free access")),
    Attr("floor", "num", "Floor", lo=1, hi=12, pr="is on floor {v}", missing_ok=False),
    Attr("rate", "money", "Cost per hour", lo=0, hi=12000, step=500, vp=["cost {c} {v} an hour"],
         field=("Max hourly rate", None), pr="costs {v} an hour"),
    Attr("bldg", "cat", "Building", cats=["Building A", "Building B", "Building C", "Building D"],
         vp=["be in {v}"], pr="is in {v}"),
    Attr("food", "bool", "Catering allowed", p=0.5, vp=["allow catering", "allow food to be brought in"],
         pr=("allows catering", "does not allow catering")),
]


def _room_ctx(rng):
    name = pick_name(rng)
    start = rng.randrange(8 * 60, 16 * 60 + 1, 15)
    dur = rng.choice([30, 45, 60, 60, 90, 90, 120, 150, 180])
    return {"today": base_day(rng), "name": name, "purpose": rng.choice(PURPOSES), "start": start, "end": start + dur,
            "dur": dur, "day": rng.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])}


def _room_people(rng, ctx, t):
    if t <= 7 and rng.random() < 0.6:
        names = []
        while len(names) < t:
            n = pick_name(rng, avoid=names)
            names.append(n)
        return ("In-person attendees: " + ", ".join(names[:-1]) + f" and {names[-1]}.", names)
    return ("{v} people will attend in person.", None)


def _room_valid(o, ctx):
    f, t = o.get("afrom"), o.get("ato")
    if f is not None and t is not None and not unk(f) and not unk(t):
        return t >= f + 60
    return True


MEETING_ROOM = Domain(
    "meeting_room", "room", "rooms", "Room", ROOM_LABELS, ROOM_ATTRS,
    makers=[
        (4, "cap", mk_implicit("cap", GE, lambda rng, ctx, D: rng.randint(3, 22), _room_people,
                               "seat everyone attending in person", vfmt=lambda t, st: str(t))),
        (4, "window", mk_window("afrom", "ato", "start", "end",
                                ["The meeting runs from {s} to {e}.", "We need the room from {s} until {e}."],
                                ["be free for the whole meeting", "be available for the entire booking"])),
        (2, "screen", mk_bool("screen")),
        (1, "board", mk_bool("board")),
        (2, "access", mk_bool("access")),
        (2, "rate", mk_cmp("rate", LE, 0.25, 0.7)),
        (2, "total", mk_derived("total", ["rate"], lambda ctx: ("*", ("a", "rate"), ("k", Fr(ctx["dur"], 60))), LE,
                                lambda rng, ctx, D: 500 * rng.randint(4, 30),
                                ["cost {c} {v} in total for the booking", "come to {c} {v} for the whole booking"],
                                money_fmt(), ctx_fn=lambda ctx, st, ci: f"The booking is for {fmt_dur(ctx['dur'], st['dur'])}.",
                                step=500, group="rate")),
        (2, "bldg", mk_cat("bldg", (1, 2))),
        (1, "food", mk_bool("food")),
    ],
    ties=[mk_tie("smallest", [(("a", "cap"), "min")], "the fewest seats", ["cap"]),
          mk_tie("lowfloor", [(("a", "floor"), "min")], "the lowest floor", ["floor"]),
          mk_tie("cheap", [(("a", "rate"), "min"), (("a", "cap"), "min")],
                 "the lowest hourly cost (then the fewest seats)", ["rate", "cap"])],
    ctx_fn=_room_ctx, valid=_room_valid, always=["afrom", "ato"],
    cs=lambda ctx, st: {"startt": ft(ctx["start"], st), "a_purpose": art(ctx["purpose"])},
    contexts=[("I'm booking a room for our {purpose} on {day}.", "{name} is booking a room for {a_purpose} on {day}."),
              ("I need a meeting room for the {purpose} this {day}.", "{name} needs a meeting room for the {purpose} this {day}.")],
    questions=["Which room should {name} book{ifany}?", "Which room meets all of the booking requirements{ifany}?",
               "Which of the listed rooms satisfies every requirement{ifany}?"],
    intros=["Rooms on the booking system:", "Available rooms:", "Room list for {day}:"],
    subjects=["Room for the {purpose}", "Booking a room on {day}"],
    def_extra="availability must cover the whole meeting",
    nice=["board", "food"],
)

# ================================================================================================ meeting slots
SLOT_LABELS = [f"Slot {c}" for c in "ABCDEFGHJKLM"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TZ_PAIRS = [("London", "New York", -5), ("London", "Chicago", -6), ("Berlin", "New York", -6), ("New York", "Los Angeles", -3),
            ("London", "Dubai", 4), ("Paris", "Toronto", -6), ("Chicago", "London", 6), ("New York", "London", 5),
            ("Sydney", "Singapore", -3), ("Madrid", "Mexico City", -7)]


def _slot_end(rng, ctx, o):
    s = o.get("start")
    s = 10 * 60 if (s is None or unk(s)) else s
    return min(19 * 60, s + rng.choice([30, 45, 60, 60, 75, 90, 120]))


def _slot_derive(o, ctx):
    d = o.get("day")
    o["dayn"] = MISSING if (d is None or unk(d)) else WEEKDAYS.index(d)
    s, e = o.get("start"), o.get("end")
    o["len"] = MISSING if (s is None or e is None or unk(s) or unk(e)) else e - s


def _slot_valid(o, ctx):
    s, e = o.get("start"), o.get("end")
    if s is not None and e is not None and not unk(s) and not unk(e):
        return e - s >= 30
    return True


SLOT_ATTRS = [
    Attr("day", "cat", "Day", cats=WEEKDAYS, vp=["be on {v}", "fall on {v}"], pr="is on {v}", missing_ok=False),
    Attr("start", "time", "Start", lo=8 * 60, hi=17 * 60, step=15, cls="time", vp=["start {c} {v}", "begin {c} {v}"],
         field=("Latest start", "Earliest start"), pr="starts at {v}", missing_ok=False),
    Attr("end", "time", "End", lo=8 * 60 + 30, hi=19 * 60, step=15, cls="time", gen=_slot_end,
         vp=["end {c} {v}", "finish {c} {v}"], field=("Latest end", None), pr="ends at {v}", missing_ok=False),
    Attr("who", "set", "Who can attend", items=[], gen=lambda rng, ctx, o: frozenset(
        rng.sample(ctx["people"], rng.randint(max(1, len(ctx["people"]) - 3), len(ctx["people"])))),
        vp=["work for {v}", "suit {v}"], pr="suits {v}"),
    Attr("room", "bool", "Room free", p=0.7, vp=["have a room free", "come with a free room"], noun="a free room",
         pr=("has a room free", "has no room free")),
    Attr("dayn", "num", "Day number", derived=True),
    Attr("len", "dur", "Length", derived=True, cls="amount", vp=["last {c} {v}", "be {c} {v} long"]),
]


def _slot_ctx(rng):
    name = pick_name(rng)
    people = []
    for _ in range(rng.randint(4, 6)):
        people.append(pick_name(rng, avoid=people + [name]))
    a, b, diff = rng.choice(TZ_PAIRS)
    wk = base_day(rng)
    while dt.date.fromordinal(wk).weekday() != 0:
        wk += 1
    return {"today": wk - rng.randint(1, 5), "name": name, "people": people, "purpose": rng.choice(PURPOSES),
            "tz_a": a, "tz_b": b, "tz_diff": diff, "remote": rng.choice(people), "week": wk}


def _mk_len(rng, ctx, D):
    a = D.A["len"]
    t = rng.choice([45, 60, 60, 75, 90])
    o = GE if rng.random() < 0.85 else GT
    c = CmpCon("len", a, o, t, "pos", wi=rng.randrange(12), vpi=rng.randrange(12), expr=("a", "len"),
               attrs=["start", "end"], lo=30, hi=150, step=15, field=False)
    c.tags.add("multi_hop")
    return c


def _mk_tz(rng, ctx, D):
    diff = ctx["tz_diff"] * 60
    lo_b, hi_b = rng.choice([(8 * 60, 17 * 60), (9 * 60, 17 * 60), (9 * 60, 18 * 60), (8 * 60 + 30, 16 * 60 + 30)])
    remote = ctx["remote"]
    ri = rng.randrange(12)

    def build(p):
        return ("and", ("cmp", ("+", ("a", "start"), ("k", diff)), GE, ("k", p["a"])),
                ("cmp", ("+", ("a", "end"), ("k", diff)), LE, ("k", p["b"]))), \
            [("start", p["a"] - diff + d * 15) for d in (-1, 0, 1)] + [("end", p["b"] - diff + d * 15) for d in (-1, 0, 1)]

    def text(p, st, mi):
        r = [f"fall within {remote}'s working hours, {ft(p['a'], st)} to {ft(p['b'], st)} {ctx['tz_b']} time",
             f"start no earlier than {ft(p['a'], st)} and end by {ft(p['b'], st)} in {ctx['tz_b']} time"][ri % 2]
        s = f"{modal('pos', mi)} {r}"
        return {"inline": s, "bullet": cap(s) + ".", "field": None}

    def ctxs(p, st):
        h = abs(ctx["tz_diff"])
        rel = "ahead of" if ctx["tz_diff"] > 0 else "behind"
        return (f"All slot times are in {ctx['tz_a']} time. {remote} works from {ctx['tz_b']}, which is {h} "
                f"hour{'s' if h != 1 else ''} {rel} {ctx['tz_a']}.")

    def vary(p, rng2):
        out = []
        for da in (-60, -30, 30, 60):
            out.append({"a": p["a"] + da, "b": p["b"]})
            out.append({"a": p["a"], "b": p["b"] + da})
        return [q for q in out if q["b"] - q["a"] >= 4 * 60]

    def chk(p, st):
        return [("tz", ctx["tz_diff"])]
    return FnCon("tz", ["start", "end"], {"a": lo_b, "b": hi_b}, build, text, vary, chk,
                 tags={"temporal", "multi_hop"}, group="tz", mscale=15, ctxs=ctxs)


MEETING_SLOT = Domain(
    "meeting_slot", "time slot", "time slots", "Slot", SLOT_LABELS, SLOT_ATTRS,
    makers=[
        (4, "who", mk_set("who", modes=("has", "all", "k"), w=(3, 4, 3), pool_fn=lambda ctx: ctx["people"])),
        (2, "day", mk_cat("day", (1, 2), neg_p=0.6)),
        (2, "start", mk_cmp("start", GE, 0.1, 0.45, strict_p=0.15)),
        (2, "end", mk_cmp("end", LE, 0.55, 0.9, strict_p=0.15)),
        (2, "len", _mk_len),
        (1, "room", mk_bool("room")),
        (3, "tz", _mk_tz),
    ],
    ties=[mk_tie("earliest", [(("a", "dayn"), "min"), (("a", "start"), "min")], "the earliest day and start time",
                 ["day", "start"]),
          mk_tie("longest", [(("a", "len"), "max"), (("a", "dayn"), "min")],
                 "the longest duration (if still tied, the earlier day)", ["start", "end", "day"])],
    ctx_fn=_slot_ctx, letters=True, derive=_slot_derive, valid=_slot_valid, always=["day", "start", "end"], no_distract=["who"],
    cs=lambda ctx, st: {"weekof": fd(ctx["week"], st), "people_list": ", ".join(ctx["people"][:-1]) + " and " + ctx["people"][-1],
                        "a_purpose": art(ctx["purpose"])},
    contexts=[("I need to find a time for {a_purpose} with {people_list} in the week of {weekof}.",
               "{name} needs to find a time for {a_purpose} with {people_list} in the week of {weekof}."),
              ("I'm scheduling our {purpose} for the week of {weekof}; the invite list is {people_list}.",
               "{name} is scheduling {a_purpose} for the week of {weekof}; the invite list is {people_list}.")],
    questions=["Which time slot should {name} pick{ifany}?", "Which slot meets every scheduling requirement{ifany}?",
               "Which of the candidate slots works under all of the constraints{ifany}?"],
    intros=["Candidate slots:", "Open slots from the shared calendar:", "Possible times:"],
    subjects=["Scheduling the {purpose}", "Finding a slot"],
    def_extra="convert time zones as stated",
)

# ================================================================================================ health plans
PLAN_LABELS = ["Bronze Saver", "Bronze Basic", "Silver Select", "Silver Plus", "Silver Flex", "Gold Choice", "Gold Premier",
               "Platinum Care", "Essential Care", "Value Care", "Family Shield", "Core HMO", "Core PPO", "Open Access",
               "Select Network", "Balance EPO", "Wellpath Standard", "Wellpath Plus", "Harborside Basic",
               "Harborside Plus", "Summit Care", "Summit Care Plus", "Keystone Health", "Keystone Health Lite",
               "Clearview Standard", "Clearview Premier", "Northwind Basic", "Northwind Complete", "Evergreen Core",
               "Evergreen Plus"]
HOSPITALS = ["Mercy General", "St. Anne's", "Lakeside Medical", "Valley Children's", "Northside Regional",
             "Eastgate Hospital"]
PLAN_ATTRS = [
    Attr("prem", "money", "Monthly premium", lo=15000, hi=90000, step=100, vp=["cost {c} {v} a month",
                                                                             "have a monthly premium of {c} {v}"],
         field=("Max monthly premium", None), pr="costs {v} a month"),
    Attr("ded", "money", "Deductible", lo=0, hi=700000, step=25000, vp=["have a deductible of {c} {v}"],
         field=("Max deductible", None), pr="has a {v} deductible"),
    Attr("oop", "money", "Out-of-pocket max", lo=200000, hi=950000, step=25000,
         vp=["have an out-of-pocket maximum of {c} {v}"], pr="caps out-of-pocket costs at {v}"),
    Attr("net", "set", "In-network hospitals", items=HOSPITALS, kset=(1, 4), vp=["include {v} in its network",
                                                                              "have {v} in network"],
         pr="has {v} in network"),
    Attr("dental", "bool", "Dental", p=0.45, vp=["include dental cover", "cover dental care"], noun="dental cover",
         pr=("includes dental", "has no dental cover")),
    Attr("vision", "bool", "Vision", p=0.45, vp=["include vision cover"], noun="vision cover",
         pr=("includes vision", "has no vision cover")),
    Attr("noref", "bool", "Specialists without referral", p=0.5, vp=["let members see specialists without a referral"],
         pr=("lets members see specialists without a referral", "requires a referral for specialists")),
    Attr("coins", "num", "Coinsurance", lo=0, hi=40, step=5, unit="%", vp=["have coinsurance of {c} {v}"],
         pr="has {v} coinsurance"),
    Attr("ptype", "cat", "Plan type", cats=["HMO", "PPO", "EPO"], vp=["be an {v} plan", "be a plan of type {v}"],
         pr="is an {v} plan", missing_ok=False),
    Attr("hsa", "bool", "HSA-eligible", p=0.4, vp=["be HSA-eligible"], pr=("is HSA-eligible", "is not HSA-eligible")),
]


def _plan_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng), "hosp": rng.choice(HOSPITALS),
            "who": rng.choice(["just myself", "my partner and me", "a family of four", "me and my daughter"])}


INSURANCE_PLAN = Domain(
    "insurance_plan", "health plan", "health plans", "Plan", PLAN_LABELS, PLAN_ATTRS,
    makers=[
        (3, "prem", mk_cmp("prem", LE, 0.25, 0.75)),
        (2, "year", mk_derived("year", ["prem"], lambda ctx: ("*", ("a", "prem"), ("k", 12)), LE,
                               lambda rng, ctx, D: 100 * 100 * rng.randint(24, 96),
                               ["cost {c} {v} a year in premiums", "keep yearly premiums at {c} {v}"], money_fmt(),
                               step=10000, tags=("numeric", "multi_hop", "units"), group="prem")),
        (3, "ded", mk_cmp("ded", LE, 0.2, 0.7)),
        (1, "oop", mk_cmp("oop", LE, 0.3, 0.8)),
        (3, "net", mk_set("net", modes=("has", "all"), w=(6, 2))),
        (2, "dental", mk_bool("dental")),
        (1, "vision", mk_bool("vision")),
        (2, "noref", mk_bool("noref")),
        (1, "coins", mk_cmp("coins", LE, 0.2, 0.6, strict_p=0.1)),
        (2, "ptype", mk_cat("ptype", (1, 2), neg_p=0.4)),
        (1, "hsa", mk_bool("hsa")),
    ],
    ties=[mk_tie("prem", [(("a", "prem"), "min")], "the lowest monthly premium", ["prem"]),
          mk_tie("ded", [(("a", "ded"), "min"), (("a", "prem"), "min")],
                 "the lowest deductible (then the lowest premium)", ["ded", "prem"]),
          mk_tie("yearcost", [(("+", ("*", ("a", "prem"), ("k", 12)), ("a", "ded")), "min")],
                 "the lowest yearly premiums plus deductible", ["prem", "ded"], tags=("multi_hop",))],
    ctx_fn=_plan_ctx, cur="$",
    contexts=[("I'm choosing a health plan for {who} during open enrollment.",
               "{name} is choosing a health plan for {who} during open enrollment."),
              ("Our small business is picking one group health plan to offer staff.",
               "{name}'s small business is picking one group health plan to offer staff.")],
    questions=["Which health plan should {name} choose{ifany}?", "Which plan meets all of the stated requirements{ifany}?",
               "Which of the plans on offer satisfies every requirement{ifany}?"],
    intros=["Plans on offer this year:", "Plan comparison:", "Available plans:"],
    subjects=["Picking a health plan", "Open enrollment"],
    nice=["vision", "hsa"],
)

# ================================================================================================ flights
FLIGHT_LABELS = [f"Flight {n}" for n in [112, 147, 203, 218, 264, 305, 331, 360, 407, 422, 458, 511, 536, 574, 609, 633,
                                        688, 702, 745, 781, 815, 846, 872, 903, 927, 961, 1012, 1048, 1075, 1106, 1139,
                                        1164, 1201, 1233, 1270, 1302, 1345, 1388, 1420, 1457, 1493, 1526, 1568, 1604,
                                        1637, 1672, 1715, 1749, 1782, 1820]]
AIRLINES = ["Aurora Air", "Coastline Airways", "Northstar", "Bluejet", "Meridian Air", "Polar Air", "Sunway"]
US_TZ = {"New York": -5, "Boston": -5, "Atlanta": -5, "Miami": -5, "Washington": -5, "Chicago": -6, "Dallas": -6,
         "Houston": -6, "Minneapolis": -6, "Denver": -7, "Salt Lake City": -7, "Seattle": -8, "San Francisco": -8,
         "Los Angeles": -8, "Portland": -8}
TRIP_PURPOSES = ["a conference", "a job interview", "a family wedding", "a client meeting", "a training course",
                 "a friend's graduation"]


def _fl_derive(o, ctx):
    d, u = o.get("dep"), o.get("dur")
    o["arr"] = MISSING if (d is None or u is None or unk(d) or unk(u)) else d + u + 60 * ctx["diff"]


def _fl_valid(o, ctx):
    a = o.get("arr")
    if a is not None and not unk(a) and not (0 <= a <= 23 * 60 + 55):
        return False
    s, l = o.get("stops"), o.get("lay")
    if s is not None and l is not None and not unk(s):
        if s == 0 and l != NA:
            return False
        if s > 0 and l == NA:
            return False
    u = o.get("dur")
    if s is not None and u is not None and not unk(s) and not unk(u) and s > 0 and u < 150:
        return False
    if l is not None and u is not None and not unk(l) and not unk(u) and l + 60 > u:
        return False
    return True


def _stops_fmt(v, s):
    return "is nonstop" if v == 0 else f"makes {s}"


FL_ATTRS = [
    Attr("airline", "cat", "Airline", cats=AIRLINES, vp=["be operated by {v}", "fly with {v}"], pr="is operated by {v}",
         missing_ok=False),
    Attr("dep", "time", "Departs", lo=5 * 60 + 30, hi=21 * 60, step=5, cls="time", vp=["depart {c} {v}", "leave {c} {v}"],
         field=("Latest departure", "Earliest departure"), pr="departs at {v}", missing_ok=False),
    Attr("dur", "dur", "Travel time", lo=50, hi=540, step=5, vp=["take {c} {v} in total", "have a total travel time of {c} {v}"],
         field=("Max travel time", None), pr="takes {v} in total", missing_ok=False),
    Attr("arr", "time", "Arrives", derived=True, cls="time", vp=["arrive {c} {v}", "land {c} {v}"],
         field=("Latest arrival", None), pr="arrives at {v}"),
    Attr("stops", "num", "Stops", lo=0, hi=2, unit=("stop", "stops"), cls="count", pr=_stops_fmt, missing_ok=False,
         gen=lambda rng, ctx, o: rng.choice([0, 0, 1, 1, 1, 2])),
    Attr("lay", "dur", "Shortest layover", lo=25, hi=240, step=5, missing_ok=False,
         gen=lambda rng, ctx, o: NA if o.get("stops") == 0 else rng.randrange(25, 241, 5),
         vp=["have a layover of {c} {v}"], pr="has a shortest layover of {v}"),
    Attr("fare", "money", "Fare", lo=8900, hi=90000, step=100, vp=["cost {c} {v}", "have a fare of {c} {v}"],
         field=("Max fare", None), pr="costs {v}"),
    Attr("bag", "bool", "Checked bag included", p=0.5, vp=["include a checked bag"], noun="a checked bag",
         pr=("includes a checked bag", "does not include a checked bag")),
    Attr("refund", "bool", "Refundable", p=0.35, vp=["be refundable"], anti=["be a non-refundable fare"],
         pr=("is refundable", "is not refundable")),
    Attr("apt", "cat", "Arrival airport", cats=["Central", "North Field", "Bayshore"], vp=["land at {v}", "arrive at {v}"],
         pr="lands at {v}", missing_ok=False),
]
FL_ATTRS[4].special = {0: "nonstop"}


def _fl_ctx(rng):
    a, b = rng.sample(sorted(US_TZ), 2)
    while US_TZ[a] == US_TZ[b] and rng.random() < 0.6:
        a, b = rng.sample(sorted(US_TZ), 2)
    return {"today": base_day(rng), "name": pick_name(rng), "orig": a, "dest": b, "diff": US_TZ[b] - US_TZ[a],
            "purpose": rng.choice(TRIP_PURPOSES)}


def _fl_tznote(ctx):
    d = ctx["diff"]
    if d == 0:
        return f"{ctx['dest']} and {ctx['orig']} are in the same time zone; all times are local."
    rel = "ahead of" if d > 0 else "behind"
    return f"All times are local; {ctx['dest']} is {abs(d)} hour{'s' if abs(d) != 1 else ''} {rel} {ctx['orig']}."


def _mk_stops(rng, ctx, D):
    a = D.A["stops"]
    if rng.random() < 0.7:
        return CmpCon("stops", a, LE, 1, "neg" if rng.random() < 0.2 else "pos", wi=rng.randrange(12),
                      vpi=0, vp=["have {c} {v}", "make {c} {v}"], field=True)
    return CmpCon("stops", a, LT, 2, "pos", wi=0, vpi=0, vp=["have {c} {v}"])


def _mk_arr_origin(rng, ctx, D):
    if ctx["diff"] == 0:
        return None
    t = rng.randrange(11 * 60, 23 * 60, 15)
    diff = 60 * ctx["diff"]
    wi, vpi = rng.randrange(12), rng.randrange(12)

    def build(p):
        return ("cmp", ("-", ("a", "arr"), ("k", diff)), LE, ("k", p["t"])), []

    def text(p, st, mi):
        w = lex_word("time", LE, "pos", wi)
        s = f"{modal('pos', mi)} {['land', 'arrive'][vpi % 2]} {w} {ft(p['t'], st)} {ctx['orig']} time"
        return {"inline": s, "bullet": cap(s) + ".", "field": None}

    def vary(p, rng2):
        return [{"t": p["t"] + d} for d in (-60, -30, -15, 15, 30, 60) if 0 < p["t"] + d < 24 * 60]

    def chk(p, st):
        return [("cmp", "time", LE, "pos", ft(p["t"], st)), ("tz", ctx["diff"])]
    return FnCon("arr_o", ["dep", "dur"], {"t": t}, build, text, vary, chk, tags={"temporal", "multi_hop"},
                 group="arr", mscale=15)


FLIGHT = Domain(
    "flight", "flight", "flights", "Flight", FLIGHT_LABELS, FL_ATTRS,
    makers=[
        (4, "arr", mk_cmp("arr", LE, strict_p=0.2, tlo=10 * 60, thi=22 * 60, tstep=15, attrs=["dep", "dur"],
                          lo=6 * 60, hi=23 * 60, step=15, vstep=15)),
        (1, "arr_o", _mk_arr_origin),
        (2, "dep", mk_cmp("dep", GE, 0.1, 0.5, strict_p=0.2)),
        (2, "stops", _mk_stops),
        (2, "lay", mk_cond("stops", ("cmp", ("a", "stops"), GE, ("k", 1)), "a flight has a connection", "lay", GE,
                           0.1, 0.4, group="stops_lay")),
        (3, "fare", mk_cmp("fare", LE, 0.2, 0.7)),
        (2, "bag", mk_bool("bag")),
        (1, "refund", mk_bool("refund")),
        (2, "airline", mk_cat("airline", (1, 2), only_neg=True)),
        (1, "apt", mk_cat("apt", (1, 2), neg_p=0.3)),
        (2, "dur", mk_cmp("dur", LE, 0.3, 0.8)),
    ],
    ties=[mk_tie("cheapest", [(("a", "fare"), "min")], "the lowest fare", ["fare"]),
          mk_tie("early", [(("a", "arr"), "min")], "the earliest arrival", ["dep", "dur"]),
          mk_tie("short", [(("a", "dur"), "min"), (("a", "fare"), "min")],
                 "the shortest travel time (then the lower fare)", ["dur", "fare"])],
    ctx_fn=_fl_ctx, cur="$", derive=_fl_derive, valid=_fl_valid, always=["dep", "arr", "dur", "stops", "lay"],
    cs=lambda ctx, st: {"tznote": _fl_tznote(ctx), "tdate": fd(ctx["today"] + 14, st)},
    contexts=[("I need to fly from {orig} to {dest} on {tdate} for {purpose}. {tznote}",
               "{name} needs to fly from {orig} to {dest} on {tdate} for {purpose}. {tznote}"),
              ("I'm booking a one-way flight, {orig} to {dest}, on {tdate}. {tznote}",
               "{name} is booking a one-way flight, {orig} to {dest}, on {tdate}. {tznote}")],
    questions=["Which flight should {name} book{ifany}?", "Which flight meets every travel requirement{ifany}?",
               "Which of the listed flights satisfies all of the requirements{ifany}?"],
    intros=["Search results:", "Flights found for that day:", "Options from the booking site:"],
    subjects=["Flight to {dest}", "Booking {orig} to {dest}"],
    def_extra="times are local unless stated",
)

# ================================================================================================ suppliers
SUP_LABELS = ["Kestrel Components", "Ardent Metalworks", "Brightline Plastics", "Corvid Fasteners", "Delmar Industrial",
              "Everton Castings", "Fairhaven Supply", "Granite Ridge Parts", "Halcyon Polymers", "Ironbridge Tooling",
              "Juniper Electronics", "Kingsley Fabrication", "Larchmont Circuits", "Marlow Precision",
              "Northgate Moulding", "Oakridge Alloys", "Pemberton Wire", "Quillon Sensors", "Redfern Packaging",
              "Sableworks", "Tamarind Textiles", "Upland Coatings", "Vantage Springs", "Westbrook Bearings",
              "Yarrow Composites", "Zephyr Seals", "Ashcombe Glass", "Birchfield Rubber", "Calder Optics", "Dunmore Cable"]
PARTS = ["M6 hex bolts", "injection-moulded housings", "printed circuit boards", "corrugated shipping boxes",
         "stainless hinges", "rubber gaskets", "aluminium brackets", "cotton tote bags", "glass jars", "LED driver modules"]
SUP_ATTRS = [
    Attr("price", "money", "Unit price", lo=5, hi=4000, step=5, cents=True, vp=["charge {c} {v} per unit"],
         field=("Max unit price", None), pr="charges {v} per unit", missing_ok=False),
    Attr("moq", "num", "Minimum order", lo=50, hi=3000, step=50, unit=("unit", "units"), cls="count",
         pr="has a minimum order of {v}"),
    Attr("lead", "num", "Lead time", lo=3, hi=90, unit=("day", "days"), cls="count", vp=["have a lead time of {c} {v}"],
         field=("Max lead time", None), pr="has a lead time of {v}"),
    Attr("iso", "bool", "ISO 9001", p=0.6, vp=["be ISO 9001 certified"], noun="ISO 9001 certification",
         pr=("is ISO 9001 certified", "is not ISO 9001 certified")),
    Attr("region", "cat", "Ships from", cats=["domestic", "Canada", "Mexico", "EU", "East Asia", "South Asia"],
         vp=["ship from {v}"], pr="ships from {v}", missing_ok=False),
    Attr("ontime", "num", "On-time rate", lo=800, hi=995, step=5, scale=10, unit="%",
         vp=["have an on-time delivery rate of {c} {v}"], field=(None, "Min on-time rate"), pr="delivers on time {v} of the time"),
    Attr("defect", "num", "Defect rate", lo=5, hi=300, step=5, scale=100, unit="%", vp=["have a defect rate of {c} {v}"],
         field=("Max defect rate", None), pr="has a defect rate of {v}"),
    Attr("terms", "num", "Payment terms", lo=0, hi=90, step=15, unit=("day", "days"), cls="count",
         vp=["offer payment terms of {c} {v}"], field=(None, "Min payment terms"), pr="offers {v} to pay"),
    Attr("setup", "money", "Setup fee", lo=0, hi=150000, step=5000, pr="charges a {v} setup fee", missing_ok=False),
]


def _sup_ctx(rng):
    today = base_day(rng)
    return {"today": today, "name": pick_name(rng), "part": rng.choice(PARTS), "qty": 50 * rng.randint(4, 80)}


def _sup_total_thr(rng, ctx, D):
    q = ctx["qty"]
    mid = q * rng.randrange(20, 1500, 5) + rng.randrange(0, 100000, 5000)
    return max(10000, (mid // 10000) * 10000)


SUPPLIER = Domain(
    "supplier", "supplier", "suppliers", "Supplier", SUP_LABELS, SUP_ATTRS,
    makers=[
        (3, "moq", mk_implicit("moq", LE, lambda rng, ctx, D: ctx["qty"],
                               lambda rng, ctx, t: ("This order is for {v}.", None),
                               "accept an order of that size (its minimum order cannot be above it)")),
        (2, "lead", mk_cmp("lead", LE, 0.1, 0.5)),
        (2, "by", mk_derived("by", ["lead"], lambda ctx: ("+", ("x", "today"), ("a", "lead")), LE,
                             lambda rng, ctx, D: ctx["today"] + rng.randint(8, 60),
                             ["be able to deliver {c} {v}", "get the parts to us {c} {v}"], fd,
                             ctx_fn=lambda ctx, st, ci: f"Today is {fd(ctx['today'], st)}; lead times are calendar days from today.",
                             step=1, tags=("temporal", "multi_hop"), cls="date", group="lead")),
        (3, "iso", mk_bool("iso")),
        (2, "region", mk_cat("region", (1, 3), neg_p=0.45)),
        (2, "ontime", mk_cmp("ontime", GE, 0.4, 0.85)),
        (1, "defect", mk_cmp("defect", LE, 0.2, 0.6)),
        (1, "terms", mk_cmp("terms", GE, 0.2, 0.5, strict_p=0.0)),
        (3, "total", mk_derived("total", ["price", "setup"],
                                lambda ctx: ("+", ("*", ("a", "price"), ("x", "qty")), ("a", "setup")), LE,
                                _sup_total_thr, ["cost {c} {v} for the whole order, setup fee included",
                                                 "keep the order total (units times unit price, plus setup) at {c} {v}"],
                                money_fmt(), ctx_fn=lambda ctx, st, ci: f"The order is for {ctx['qty']:,} units.",
                                step=10000, group="price")),
    ],
    ties=[mk_tie("total", [(("+", ("*", ("a", "price"), ("x", "qty")), ("a", "setup")), "min")],
                 "the lowest order total (unit price times quantity plus setup fee)", ["price", "setup"],
                 tags=("multi_hop",)),
          mk_tie("lead", [(("a", "lead"), "min"), (("a", "price"), "min")],
                 "the shortest lead time (then the lower unit price)", ["lead", "price"]),
          mk_tie("ontime", [(("a", "ontime"), "max")], "the highest on-time rate", ["ontime"])],
    ctx_fn=_sup_ctx, no_distract=["moq"],
    contexts=[("We're sourcing {part} and need to pick one supplier.", "{name}'s team is sourcing {part} and needs to pick one supplier."),
              ("I'm placing a purchase order for {part}.", "{name} is placing a purchase order for {part}.")],
    questions=["Which supplier should get the order{ifany}?", "Which supplier meets all of the purchasing requirements{ifany}?",
               "Which of the quoted suppliers satisfies every requirement{ifany}?"],
    intros=["Supplier quotes:", "Bids received:", "Shortlisted suppliers:"],
    subjects=["Supplier for {part}", "PO for {part}"],
    nice=[],
)

# ================================================================================================ candidates
ROLES = [("project coordinator", "a PMP certificate"), ("staff accountant", "a CPA licence"),
         ("network technician", "a CCNA certification"), ("data analyst", "a SQL certification"),
         ("site safety officer", "a NEBOSH certificate"), ("payroll specialist", "a payroll certification"),
         ("clinical coder", "a coding certification"), ("warehouse supervisor", "a forklift licence")]
LANGS = ["English", "Spanish", "French", "German", "Mandarin", "Portuguese", "Arabic", "Hindi", "Japanese", "Korean"]
CAND_ATTRS = [
    Attr("exp", "num", "Experience", lo=0, hi=15, unit=("year", "years"), cls="count",
         vp=["have {c} {v} of relevant experience"], field=(None, "Minimum experience"), pr="has {v} of experience",
         missing_ok=False),
    Attr("cert", "bool", "Holds {cert}", p=0.45, vp=["be certified"], pr=("holds {cert}", "does not hold {cert}")),
    Attr("langs", "set", "Languages", items=LANGS, kset=(1, 3), vp=["speak {v}"], pr="speaks {v}"),
    Attr("start", "date", "Can start", date_lo=3, date_hi=75, cls="date",
         vp=["be able to start {c} {v}", "be available to start {c} {v}"], field=("Latest start date", None),
         pr="can start on {v}"),
    Attr("salary", "money", "Salary expectation", lo=4000000, hi=16000000, step=100000,
         vp=["expect a salary of {c} {v}", "ask for {c} {v} a year"], field=("Maximum salary", None),
         pr="expects {v} a year"),
    Attr("mode", "cat", "Work preference", cats=["on-site", "hybrid", "remote"], vp=["want {v} work", "prefer {v} work"],
         pr="prefers {v} work", missing_ok=False),
    Attr("rtw", "bool", "Right to work", p=0.8, vp=["already have the right to work here"], noun="the right to work here",
         pr=("has the right to work here", "needs a work visa")),
    Attr("licence", "bool", "Driving licence", p=0.6, vp=["hold a driving licence"], noun="a driving licence",
         pr=("holds a driving licence", "has no driving licence")),
]


def _cand_ctx(rng):
    role, cert = rng.choice(ROLES)
    return {"today": base_day(rng), "name": pick_name(rng), "role": role, "cert": cert}


CANDIDATE = Domain(
    "candidate", "candidate", "candidates", "Candidate", PEOPLE, CAND_ATTRS,
    makers=[
        (2, "exp", mk_cmp("exp", GE, 0.15, 0.5, strict_p=0.1)),
        (3, "exp", mk_exc("exp", "cert", GE, lambda ctx: f"the candidate holds {ctx['cert']}", gap=(1, 3),
                          f0=0.25, f1=0.55)),
        (3, "langs", mk_set("langs", modes=("has", "all", "k"), w=(5, 2, 2))),
        (2, "start", mk_date("start", LE, 15, 55)),
        (2, "salary", mk_cmp("salary", LE, 0.3, 0.75)),
        (2, "mode", mk_cat("mode", (1, 2), neg_p=0.4)),
        (1, "rtw", mk_bool("rtw")),
        (1, "licence", mk_bool("licence")),
        (1, "cert", mk_bool("cert", vpf=lambda ctx: [f"hold {ctx['cert']}"])),
    ],
    ties=[mk_tie("exp", [(("a", "exp"), "max"), (("a", "start"), "min")],
                 "the most experience (if still tied, the earlier start date)", ["exp", "start"]),
          mk_tie("start", [(("a", "start"), "min")], "the earliest start date", ["start"]),
          mk_tie("salary", [(("a", "salary"), "min")], "the lowest salary expectation", ["salary"])],
    ctx_fn=_cand_ctx, hv=lambda ctx: {"cert": ctx["cert"]}, no_distract=["rtw"],
    cs=lambda ctx, st: {"todays": fd(ctx["today"], st)},
    contexts=[("I'm shortlisting for our open {role} position and can move one person to the final interview.",
               "{name} is shortlisting for an open {role} position and can move one person to the final interview."),
              ("We're filling a {role} vacancy; the hiring rules below are fixed.",
               "{name}'s team is filling a {role} vacancy; the hiring rules below are fixed.")],
    questions=["Which candidate should move to the final interview{ifany}?",
               "Which candidate meets every hiring requirement{ifany}?",
               "Which applicant satisfies all of the stated criteria for the {role} role{ifany}?"],
    intros=["Applicants:", "Candidate summary:", "Screening notes:"],
    subjects=["{role} shortlist", "Final interview pick"],
    nice=["licence"],
)

# ================================================================================================ apartments
STREETS = ["Alder Street", "Birch Lane", "Canal Road", "Dover Street", "Elm Terrace", "Foxglove Way", "Grove Avenue",
           "Hazel Road", "Ivy Court", "Juniper Place", "Kestrel Road", "Laurel Street", "Mill Lane", "Nettle Row",
           "Oak Crescent", "Poplar Street", "Quarry Road", "Rowan Avenue", "Sorrel Street", "Thistle Lane"]
APT_LABELS = [f"Apt {u}, {n} {s}" for u, n, s in
              [(f"{1 + i % 5}{'ABCD'[i % 4]}", 10 + (i * 7) % 80, STREETS[i % len(STREETS)]) for i in range(50)]]
APT_ATTRS = [
    Attr("rent", "money", "Rent", lo=90000, hi=400000, step=2500, vp=["rent for {c} {v} a month", "cost {c} {v} a month"],
         field=("Max rent", None), pr="rents for {v} a month", missing_ok=False),
    Attr("beds", "num", "Bedrooms", lo=1, hi=4, unit=("bedroom", "bedrooms"), cls="count", vp=["have {c} {v}"],
         field=(None, "Min bedrooms"), pr="has {v}", missing_ok=False),
    Attr("area", "num", "Floor area", lo=380, hi=1800, step=10, unit=" sq ft", vp=["have {c} {v} of floor space"],
         field=(None, "Min floor area"), pr="has {v} of floor space", missing_ok=False),
    Attr("pets", "set", "Pets allowed", items=["cats", "dogs"], kset=(0, 2), vp=["allow {v}"],
         pr=("allows {v}", "allows no pets")),
    Attr("parking", "bool", "Parking", p=0.45, vp=["include parking", "come with a parking space"], noun="parking",
         pr=("includes parking", "has no parking")),
    Attr("laundry", "cat", "Laundry", cats=["in-unit", "shared", "none"], vp=["have laundry that is {v}"],
         pr="has laundry: {v}"),
    Attr("floor", "num", "Floor", lo=1, hi=9, pr="is on floor {v}", missing_ok=False),
    Attr("lift", "bool", "Elevator", p=0.5, vp=["be in a building with an elevator"],
         pr=("has an elevator", "has no elevator")),
    Attr("avail", "date", "Available from", date_lo=0, date_hi=60, cls="date", vp=["be available {c} {v}"],
         pr="is available from {v}"),
    Attr("commute", "num", "Commute", lo=5, hi=70, step=5, unit=("minute", "minutes"), cls="count",
         vp=["have a commute of {c} {v}"], field=("Max commute", None), pr="has a {v} commute"),
    Attr("lease", "num", "Minimum lease", lo=6, hi=24, step=6, unit=("month", "months"), cls="count",
         vp=["require a lease of {c} {v}"], pr="requires a lease of {v}"),
]


def _apt_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng), "city": rng.choice(CITIES)}


APARTMENT = Domain(
    "apartment", "apartment", "apartments", "Listing", APT_LABELS, APT_ATTRS,
    makers=[
        (2, "rent", mk_cmp("rent", LE, 0.2, 0.7)),
        (2, "rent", mk_exc("rent", "parking", LE, "parking is included", alt_words=("is acceptable", "is fine"),
                           gap=(4, 10), f0=0.2, f1=0.6)),
        (2, "beds", mk_cmp("beds", GE, 0.3, 0.7, strict_p=0.0)),
        (1, "area", mk_cmp("area", GE, 0.2, 0.6)),
        (1, "area", mk_xunit("area", GE, "m²", Fr(1076, 100), Fr(107639, 10000), [x for x in range(45, 150, 5)],
                             ["have {c} {v} of floor space"], "(1 m² ≈ 10.76 sq ft)", dec=0)),
        (2, "pets", mk_set("pets", modes=("has",), w=(1,))),
        (2, "parking", mk_bool("parking")),
        (2, "lift", mk_cond("floor", ("cmp", ("a", "floor"), GE, ("k", 3)), "the apartment is on the third floor or higher",
                            "lift", GE, then_bool=True, group="floor_lift")),
        (2, "avail", mk_date("avail", LE, 10, 45)),
        (2, "commute", mk_cmp("commute", LE, 0.2, 0.6)),
        (1, "lease", mk_cmp("lease", LE, 0.2, 0.5, strict_p=0.0, neg_p=0.3)),
    ],
    ties=[mk_tie("rent", [(("a", "rent"), "min")], "the lowest rent", ["rent"]),
          mk_tie("commute", [(("a", "commute"), "min"), (("a", "rent"), "min")],
                 "the shortest commute (then the lower rent)", ["commute", "rent"]),
          mk_tie("area", [(("a", "area"), "max")], "the most floor space", ["area"])],
    ctx_fn=_apt_ctx,
    cs=lambda ctx, st: {"todays": fd(ctx["today"], st)},
    contexts=[("I'm apartment hunting in {city} and want to apply for exactly one place.",
               "{name} is apartment hunting in {city} and wants to apply for exactly one place."),
              ("My lease ends soon, so I'm choosing a new apartment in {city}.",
               "{name}'s lease ends soon, so {name} is choosing a new apartment in {city}.")],
    questions=["Which apartment should {name} apply for{ifany}?", "Which listing meets all of the requirements{ifany}?",
               "Which of these apartments satisfies every stated requirement{ifany}?"],
    intros=["Listings saved so far:", "Apartments viewed:", "Current listings:"],
    subjects=["Apartment shortlist", "Which place to apply for"],
    nice=["lift"],
)

# ================================================================================================ hotels
HOTEL_LABELS = ["The Alder House", "Harbourview Inn", "Kingsgate Hotel", "Linden Suites", "Maple Court Hotel",
                "Northbank Lodge", "Old Mill Hotel", "Parkside Inn", "Quayside Rooms", "Riverstone Hotel",
                "Saltmarsh Inn", "The Tannery Hotel", "Union Square Suites", "Victoria Lane Hotel", "Westgate Inn",
                "The Cobbled Yard", "Brookfield Hotel", "Cathedral View Inn", "Dockside Lodge", "Elmwood Suites",
                "The Foundry Hotel", "Greenway Inn", "Hilltop House", "The Ivy Rooms", "Jubilee Hotel", "Kiln House",
                "Lighthouse Inn", "Market Street Hotel", "The Nook", "Orchard Lodge", "Pier House", "The Rookery",
                "Station Hotel", "Tower Bridge Inn", "The Wharf", "Crescent Hotel", "Meadowbank Inn", "The Granary",
                "Canal House", "Beacon Hotel"]
HOTEL_ATTRS = [
    Attr("rate", "money", "Nightly rate", lo=7900, hi=45000, step=100, vp=["have a nightly rate of {c} {v}"],
         field=("Max nightly rate", None), pr="has a nightly rate of {v}", missing_ok=False),
    Attr("fee", "money", "Resort fee per night", lo=0, hi=4500, step=500, pr="adds a {v} nightly fee", missing_ok=False),
    Attr("dist", "num", "Distance to venue", lo=2, hi=150, scale=10, unit=" km", vp=["be {c} {v} from the venue"],
         field=("Max distance", None), pr="is {v} from the venue", missing_ok=False),
    Attr("bfast", "bool", "Breakfast included", p=0.45, vp=["include breakfast"], noun="breakfast",
         pr=("includes breakfast", "does not include breakfast")),
    Attr("cancel", "bool", "Free cancellation", p=0.55, vp=["offer free cancellation"], noun="free cancellation",
         pr=("offers free cancellation", "has no free cancellation")),
    Attr("rating", "num", "Guest rating", lo=60, hi=98, scale=10, unit="/10", vp=["have a guest rating of {c} {v}"],
         field=(None, "Min rating"), pr="is rated {v}"),
    Attr("parking", "bool", "Parking", p=0.5, vp=["have parking"], noun="parking", pr=("has parking", "has no parking")),
    Attr("access", "bool", "Accessible room", p=0.6, vp=["have an accessible room available"],
         pr=("has an accessible room", "has no accessible room")),
]


def _hotel_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng), "city": rng.choice(CITIES), "nights": rng.randint(2, 6),
            "event": rng.choice(["a trade fair", "a wedding", "a medical conference", "a marathon", "a job fair",
                                 "a music festival"])}


def _hotel_total_thr(rng, ctx, D):
    return 10000 * rng.randint(2 * ctx["nights"], 4 * ctx["nights"] + 4)


HOTEL = Domain(
    "hotel", "hotel", "hotels", "Hotel", HOTEL_LABELS, HOTEL_ATTRS,
    makers=[
        (2, "rate", mk_cmp("rate", LE, 0.2, 0.7)),
        (2, "rate", mk_exc("rate", "bfast", LE, "breakfast is included", gap=(10, 30), f0=0.15, f1=0.55)),
        (3, "total", mk_derived("total", ["rate", "fee"],
                                lambda ctx: ("*", ("+", ("a", "rate"), ("a", "fee")), ("k", ctx["nights"])), LE,
                                _hotel_total_thr, ["cost {c} {v} for the whole stay, nightly fees included",
                                                   "come to {c} {v} in total for all nights"],
                                money_fmt(), ctx_fn=lambda ctx, st, ci: f"The stay is {ctx['nights']} nights.",
                                step=5000, group="rate")),
        (2, "dist", mk_cmp("dist", LE, 0.1, 0.5)),
        (1, "dist", mk_xunit("dist", LE, "miles", Fr(16), Fr(1609344, 100000), [x for x in range(5, 60, 5)],
                             ["be {c} {v} from the venue"], "(1 mile = 1.6 km)", dec=1)),
        (2, "bfast", mk_bool("bfast")),
        (2, "cancel", mk_bool("cancel")),
        (2, "rating", mk_cmp("rating", GE, 0.3, 0.8)),
        (1, "parking", mk_bool("parking")),
        (1, "access", mk_bool("access")),
    ],
    ties=[mk_tie("total", [(("+", ("a", "rate"), ("a", "fee")), "min")], "the lowest nightly cost including fees",
                 ["rate", "fee"], tags=("multi_hop",)),
          mk_tie("close", [(("a", "dist"), "min")], "the shortest distance to the venue", ["dist"]),
          mk_tie("rating", [(("a", "rating"), "max"), (("a", "rate"), "min")],
                 "the highest guest rating (then the lower nightly rate)", ["rating", "rate"])],
    ctx_fn=_hotel_ctx,
    contexts=[("I'm booking a hotel in {city} for {event}.", "{name} is booking a hotel in {city} for {event}."),
              ("I need somewhere to stay in {city} while I attend {event}.", "{name} needs somewhere to stay in {city} while attending {event}.")],
    questions=["Which hotel should {name} book{ifany}?", "Which hotel meets all of the stay requirements{ifany}?",
               "Which of the listed hotels satisfies every requirement{ifany}?"],
    intros=["Hotels with rooms left:", "Search results:", "Options near the venue:"],
    subjects=["Hotel for {event}", "Where to stay in {city}"],
    nice=["parking", "access"],
)

# ================================================================================================ car rental
AGENCIES = ["Roadway", "Kerbside", "Metro Drive", "Openroad", "Cityhop", "Summit Auto"]
CLASSES = ["Economy", "Compact", "Midsize", "Full-size", "Minivan", "SUV", "Estate"]
CAR_LABELS = [f"{a} {c}" for a in AGENCIES for c in CLASSES]
CAR_ATTRS = [
    Attr("daily", "money", "Daily rate", lo=2500, hi=15000, step=100, vp=["cost {c} {v} a day"],
         field=("Max daily rate", None), pr="costs {v} a day", missing_ok=False),
    Attr("seats", "num", "Seats", lo=2, hi=8, unit=("seat", "seats"), cls="count", vp=["have {c} {v}"],
         pr="has {v}", missing_ok=False),
    Attr("bags", "num", "Luggage", lo=1, hi=6, unit=("large bag", "large bags"), cls="count", vp=["fit {c} {v}"],
         pr="fits {v}"),
    Attr("trans", "cat", "Transmission", cats=["automatic", "manual"], vp=["be {v}"], pr="is {v}", missing_ok=False),
    Attr("minage", "num", "Minimum driver age", lo=18, hi=25, pr="needs drivers aged {v}+"),
    Attr("fuel", "cat", "Fuel", cats=["petrol", "diesel", "hybrid", "electric"], vp=["run on {v}", "be {v}"],
         pr="runs on {v}", missing_ok=False),
    Attr("unl", "bool", "Unlimited mileage", p=0.55, vp=["include unlimited mileage"], noun="unlimited mileage",
         pr=("includes unlimited mileage", "has a mileage cap")),
    Attr("loc", "cat", "Pickup", cats=["airport", "downtown", "train station"], vp=["be picked up at the {v}"],
         pr="is picked up at the {v}", missing_ok=False),
]


def _car_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng), "city": rng.choice(CITIES), "days": rng.randint(2, 10)}


CAR_RENTAL = Domain(
    "car_rental", "rental car", "rental cars", "Car", CAR_LABELS, CAR_ATTRS,
    makers=[
        (3, "seats", mk_implicit("seats", GE, lambda rng, ctx, D: rng.randint(3, 7),
                                 lambda rng, ctx, t: (rng.choice(["There will be {v} of us in the car.",
                                                                  "We are a group of {v}, all travelling together."]), None),
                                 "seat the whole group", vfmt=lambda t, st: str(t))),
        (2, "bags", mk_implicit("bags", GE, lambda rng, ctx, D: rng.randint(2, 5),
                                lambda rng, ctx, t: ("We are bringing {v} large bags.", None),
                                "fit all of our large bags", vfmt=lambda t, st: str(t))),
        (2, "minage", mk_implicit("minage", LE, lambda rng, ctx, D: rng.randint(19, 26),
                                  lambda rng, ctx, t: ("The only driver is {v} years old.", None),
                                  "accept a driver of that age", vfmt=lambda t, st: str(t))),
        (2, "trans", mk_cat("trans", (1, 1), neg_p=0.4)),
        (1, "fuel", mk_cat("fuel", (1, 2), neg_p=0.6)),
        (2, "unl", mk_bool("unl")),
        (1, "loc", mk_cat("loc", (1, 2), neg_p=0.3)),
        (2, "daily", mk_cmp("daily", LE, 0.2, 0.7)),
        (2, "total", mk_derived("total", ["daily"], lambda ctx: ("*", ("a", "daily"), ("k", ctx["days"])), LE,
                                lambda rng, ctx, D: 1000 * rng.randint(4 * ctx["days"], 11 * ctx["days"]),
                                ["cost {c} {v} for the whole rental", "come to {c} {v} for all days combined"],
                                money_fmt(), ctx_fn=lambda ctx, st, ci: f"The rental is for {ctx['days']} days.",
                                step=1000, group="daily")),
    ],
    ties=[mk_tie("cheap", [(("a", "daily"), "min")], "the lowest daily rate", ["daily"]),
          mk_tie("bags", [(("a", "bags"), "max"), (("a", "daily"), "min")],
                 "the most luggage space (then the lower daily rate)", ["bags", "daily"])],
    ctx_fn=_car_ctx,
    contexts=[("I'm renting a car in {city} for a road trip.", "{name} is renting a car in {city} for a road trip."),
              ("We need a rental car in {city} for a family visit.", "{name}'s family needs a rental car in {city} for a visit.")],
    questions=["Which rental car should {name} reserve{ifany}?", "Which car meets all of the rental requirements{ifany}?",
               "Which of the listed rentals satisfies every requirement{ifany}?"],
    intros=["Cars available for those dates:", "Rental quotes:", "Search results:"],
    subjects=["Car hire in {city}", "Rental car"],
    nice=["unl"],
)

CANDIDATE.person = True
DOMAINS_A = [SHIPPING, MEETING_ROOM, MEETING_SLOT, INSURANCE_PLAN, FLIGHT, SUPPLIER, CANDIDATE, APARTMENT, HOTEL,
             CAR_RENTAL]
