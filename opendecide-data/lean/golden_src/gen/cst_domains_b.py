"""gen_constraints domains, part B: event venues, caterers, contractors, laptops, phone plans, course sections,
clinic appointments, childcare, translators, moving companies.  All names are invented."""
import datetime as dt
from fractions import Fraction as Fr

from cst_core import GE, GT, LE, LT, MISSING, NA, MON, Attr, CmpCon, FnCon, cap, fmt_date, fmt_money, fmt_time, \
    modal, unk
from cst_dom_base import (FIRST, PEOPLE, Domain, mk_bool, mk_cat, mk_cmp, mk_date, mk_derived, mk_exc, mk_implicit,
                          mk_range, mk_set, mk_tie, mk_xunit, money_fmt)
from cst_domains_a import CITIES, art, base_day, fd, ft, pick_name


def day_month(o):
    d = dt.date.fromordinal(o)
    return f"{d.day} {MON[d.month - 1]}"


# ================================================================================================ venues
VENUE_LABELS = ["The Glasshouse", "Riverside Hall", "Old Library Rooms", "Foundry Loft", "Harbour Pavilion",
                "The Assembly Rooms", "Brewhouse Yard", "Chapel Arts Space", "The Coach House", "Eastfield Barn",
                "The Exchange Rooms", "Garden Court", "Guildhall Suite", "Hillside Lodge", "Kingfisher Hall",
                "The Lantern Rooms", "Longmeadow Barn", "Mill Race Venue", "Northlight Studio", "The Observatory Rooms",
                "Orangery at Park Lane", "Printmakers Hall", "Queen's Wharf Hall", "Rooftop at Ninth", "The Round Room",
                "Seaview Terrace", "Signal Box Loft", "Stable Yard", "Tannery Hall", "The Waterworks Room"]
EVENTS = ["wedding reception", "company party", "charity gala", "product launch", "fiftieth birthday party",
          "alumni reunion", "awards dinner", "retirement party"]
VENUE_ATTRS = [
    Attr("cap", "num", "Capacity", lo=20, hi=400, step=10, unit=("guest", "guests"), cls="count", vp=["hold {c} {v}"],
         pr="holds {v}", missing_ok=False),
    Attr("fee", "money", "Hire fee", lo=50000, hi=1200000, step=5000, vp=["cost {c} {v} to hire", "have a hire fee of {c} {v}"],
         field=("Max hire fee", None), pr="costs {v} to hire", missing_ok=False),
    Attr("cater", "bool", "Outside caterers allowed", p=0.5, vp=["allow outside caterers"],
         pr=("allows outside caterers", "does not allow outside caterers")),
    Attr("step", "bool", "Step-free access", p=0.65, vp=["have step-free access"], noun="step-free access",
         pr=("has step-free access", "has no step-free access")),
    Attr("av", "bool", "AV included", p=0.5, vp=["include AV equipment"], noun="AV equipment",
         pr=("includes AV equipment", "does not include AV equipment")),
    Attr("curfew", "time", "Music curfew", lo=21 * 60, hi=23 * 60 + 45, step=15, cls="time",
         vp=["have a music curfew {c} {v}", "let music play until a curfew {c} {v}"], field=(None, "Earliest acceptable curfew"),
         pr="has a music curfew of {v}"),
    Attr("free", "bool", "Free on {date}", p=0.6, vp=["be free on the event date"], pr=("is free on {date}", "is booked on {date}")),
    Attr("park", "num", "Parking spaces", lo=0, hi=200, step=10, unit=("parking space", "parking spaces"), cls="count",
         vp=["have {c} {v}"], pr="has {v}"),
    Attr("dep", "num", "Deposit", lo=10, hi=50, step=5, unit="%", vp=["ask for a deposit of {c} {v}"],
         field=("Max deposit", None), pr="asks for a {v} deposit"),
]


def _venue_ctx(rng):
    today = base_day(rng)
    return {"today": today, "name": pick_name(rng), "event": rng.choice(EVENTS), "date": today + rng.randint(40, 200)}


VENUE = Domain(
    "venue", "venue", "venues", "Venue", VENUE_LABELS, VENUE_ATTRS,
    makers=[
        (4, "cap", mk_implicit("cap", GE, lambda rng, ctx, D: 10 * rng.randint(4, 30),
                               lambda rng, ctx, t: (rng.choice(["We expect {v} guests.", "The guest list stands at {v} people."]), None),
                               "hold all of the guests", vfmt=lambda t, st: str(t))),
        (2, "fee", mk_cmp("fee", LE, 0.2, 0.7)),
        (2, "fee", mk_exc("fee", "av", LE, "AV equipment is included", gap=(4, 20), f0=0.15, f1=0.6)),
        (2, "cater", mk_bool("cater")),
        (2, "step", mk_bool("step")),
        (1, "av", mk_bool("av")),
        (2, "curfew", mk_cmp("curfew", GE, 0.3, 0.8, strict_p=0.1)),
        (3, "free", mk_bool("free")),
        (1, "park", mk_cmp("park", GE, 0.1, 0.5, strict_p=0.0)),
        (1, "dep", mk_cmp("dep", LE, 0.2, 0.6, neg_p=0.3)),
    ],
    ties=[mk_tie("fee", [(("a", "fee"), "min")], "the lowest hire fee", ["fee"]),
          mk_tie("dep", [(("a", "dep"), "min"), (("a", "fee"), "min")], "the lowest deposit percentage (then the lower hire fee)",
                 ["dep", "fee"]),
          mk_tie("park", [(("a", "park"), "max")], "the most parking spaces", ["park"])],
    ctx_fn=_venue_ctx, hv=lambda ctx: {"date": day_month(ctx["date"])},
    cs=lambda ctx, st: {"dates": fd(ctx["date"], st), "a_event": art(ctx["event"])}, no_distract=["free"],
    contexts=[("I'm looking for a venue for our {event} on {dates}.", "{name} is looking for a venue for {a_event} on {dates}."),
              ("We're hosting {a_event} on {dates} and still need a venue.", "{name} is hosting {a_event} on {dates} and still needs a venue.")],
    questions=["Which venue should {name} book{ifany}?", "Which venue meets every requirement for the {event}{ifany}?",
               "Which of the listed venues satisfies all of the stated requirements{ifany}?"],
    intros=["Venues contacted:", "Venue shortlist:", "Replies from venues:"],
    subjects=["Venue for the {event}", "{event} venue"],
    nice=["av", "step"],
)

# ================================================================================================ caterers
CATER_LABELS = ["Saffron & Sage", "Blue Plate Catering", "The Copper Pot", "Harvest Table", "Olive & Thyme",
                "Salt Kitchen", "Greenleaf Catering", "Brass Spoon", "Fig Tree Kitchen", "Hearth & Home Catering",
                "Juniper Table", "Kettle Black Catering", "Larder Co.", "Mint Street Kitchen", "Nomad Kitchen",
                "Oak & Ember", "Peppercorn Catering", "Quince Kitchen", "Red Lentil Co.", "Silver Ladle",
                "Tamarind Tables", "Urban Picnic", "Vine & Barley", "Wild Garlic Kitchen", "Yellow Door Catering",
                "Zest Catering", "Basil & Bay", "Cardamom Kitchen", "Driftwood Catering", "Elderflower Events"]
DIETS = ["vegan", "vegetarian", "halal", "kosher", "gluten-free", "nut-free"]


def _cater_valid(o, ctx):
    a, b = o.get("ming"), o.get("maxg")
    if a is not None and b is not None and not unk(a) and not unk(b):
        return b >= a + 30
    return True


CATER_ATTRS = [
    Attr("pph", "money", "Price per guest", lo=1200, hi=9500, step=50, cents=True, vp=["charge {c} {v} per guest"],
         field=("Max price per guest", None), pr="charges {v} per guest", missing_ok=False),
    Attr("ming", "num", "Minimum guests", lo=10, hi=150, step=10, unit=("guest", "guests"), pr="needs at least {v}",
         missing_ok=False),
    Attr("maxg", "num", "Maximum guests", lo=40, hi=400, step=10, unit=("guest", "guests"), pr="serves up to {v}",
         missing_ok=False),
    Attr("diets", "set", "Dietary menus", items=DIETS, kset=(1, 4), vp=["offer {v} menus", "cater for {v} diets"],
         pr="offers {v} menus"),
    Attr("deliv", "money", "Delivery fee", lo=0, hi=30000, step=1000, pr="charges {v} for delivery", missing_ok=False),
    Attr("staff", "bool", "Serving staff included", p=0.5, vp=["include serving staff"], noun="serving staff",
         pr=("includes serving staff", "does not include serving staff")),
    Attr("free", "bool", "Free on {date}", p=0.65, vp=["be free on the event date"], pr=("is free on {date}", "is booked on {date}")),
    Attr("rating", "num", "Rating", lo=30, hi=50, scale=10, unit="/5", vp=["have a rating of {c} {v}"],
         field=(None, "Min rating"), pr="is rated {v}"),
]


def _cater_ctx(rng):
    today = base_day(rng)
    return {"today": today, "name": pick_name(rng), "event": rng.choice(EVENTS), "date": today + rng.randint(30, 150),
            "guests": 10 * rng.randint(5, 25)}


def _guest_sent(x, st):
    return f"We expect {x} guests."


CATERER = Domain(
    "caterer", "caterer", "caterers", "Caterer", CATER_LABELS, CATER_ATTRS,
    makers=[
        (4, "range", mk_range("ming", "maxg", lambda rng, ctx, D: ctx["guests"], _guest_sent,
                              ["be able to cater for that number of guests (within its minimum and maximum)",
                               "accept a party of that size"], step=10, vary_d=())),
        (3, "total", mk_derived("total", ["pph", "deliv"],
                                lambda ctx: ("+", ("*", ("a", "pph"), ("x", "guests")), ("a", "deliv")), LE,
                                lambda rng, ctx, D: 10000 * rng.randint(ctx["guests"] * 20 // 100, ctx["guests"] * 80 // 100 + 2),
                                ["cost {c} {v} in total, delivery included", "come to {c} {v} for everyone, delivery included"],
                                money_fmt(), ctx_fn=lambda ctx, st, ci: f"The quote is for {ctx['guests']} guests.",
                                step=10000, group="pph")),
        (2, "pph", mk_cmp("pph", LE, 0.25, 0.7)),
        (3, "diets", mk_set("diets", modes=("has", "all", "k"), w=(3, 4, 2))),
        (2, "staff", mk_bool("staff")),
        (3, "free", mk_bool("free")),
        (1, "rating", mk_cmp("rating", GE, 0.3, 0.8)),
    ],
    ties=[mk_tie("total", [(("+", ("*", ("a", "pph"), ("x", "guests")), ("a", "deliv")), "min")],
                 "the lowest total cost (price per guest times guests, plus delivery)", ["pph", "deliv"],
                 tags=("multi_hop",)),
          mk_tie("rating", [(("a", "rating"), "max"), (("a", "pph"), "min")],
                 "the highest rating (then the lower price per guest)", ["rating", "pph"])],
    ctx_fn=_cater_ctx, valid=_cater_valid, hv=lambda ctx: {"date": day_month(ctx["date"])},
    cs=lambda ctx, st: {"dates": fd(ctx["date"], st), "a_event": art(ctx["event"])}, no_distract=["free", "ming", "maxg"],
    contexts=[("I'm hiring a caterer for our {event} on {dates}.", "{name} is hiring a caterer for {a_event} on {dates}."),
              ("We still need food for the {event} on {dates}.", "{name} still needs food for the {event} on {dates}.")],
    questions=["Which caterer should {name} hire{ifany}?", "Which caterer meets all of the requirements{ifany}?",
               "Which of the quoted caterers satisfies every stated requirement{ifany}?"],
    intros=["Catering quotes:", "Caterers who replied:", "Options so far:"],
    subjects=["Catering for the {event}", "Caterer quotes"],
    nice=["staff"],
)

# ================================================================================================ contractors
CONTR_LABELS = ["Brightwork Renovations", "Stonefield Builders", "Cornerstone Remodeling", "Oakline Carpentry",
                "Truebuild Contractors", "Harbor Home Repair", "Level Line Construction", "Keystone Renovations",
                "Northwall Builders", "Plumbline Projects", "Redbrick Remodel", "Sturdy Oak Homes", "Timberframe Works",
                "Upright Builders", "Westside Renovation Co.", "Anchor Home Improvements", "Beacon Builders",
                "Craftline Interiors", "Dovetail Joinery", "Evenkeel Construction", "Firstcoat Decorators",
                "Groundwork Builders", "Hearthstone Renovations", "Ironwood Remodeling", "Joist & Beam",
                "Kingpost Builders", "Lintel Home Services", "Mortar & Mason", "Newel Post Carpentry", "Ridgeline Roofing"]
PROJECTS = ["kitchen remodel", "bathroom renovation", "roof replacement", "basement conversion", "deck build",
            "loft insulation", "garage conversion", "window replacement"]
CONTR_ATTRS = [
    Attr("bid", "money", "Bid", lo=400000, hi=6000000, step=10000, vp=["bid {c} {v}", "come in at {c} {v}"],
         field=("Max bid", None), pr="bids {v}", missing_ok=False),
    Attr("lic", "bool", "Licensed", p=0.75, vp=["be licensed"], anti=["be an unlicensed firm"],
         pr=("is licensed", "is not licensed")),
    Attr("ins", "bool", "Insured", p=0.7, vp=["carry liability insurance"], noun="liability insurance",
         pr=("carries liability insurance", "has no liability insurance")),
    Attr("start", "date", "Can start", date_lo=3, date_hi=60, cls="date", vp=["be able to start {c} {v}"],
         field=("Latest start", None), pr="can start on {v}", missing_ok=False),
    Attr("weeks", "num", "Duration", lo=2, hi=20, unit=("week", "weeks"), cls="count", vp=["take {c} {v}"],
         field=("Max duration", None), pr="needs {v}", missing_ok=False),
    Attr("warr", "num", "Warranty", lo=0, hi=10, unit=("year", "years"), cls="count", vp=["give a warranty of {c} {v}"],
         field=(None, "Min warranty"), pr="gives a {v} warranty"),
    Attr("rating", "num", "Review score", lo=30, hi=50, scale=10, unit="/5", vp=["have a review score of {c} {v}"],
         pr="has a review score of {v}"),
    Attr("refs", "num", "References", lo=0, hi=6, unit=("reference", "references"), cls="count", vp=["provide {c} {v}"],
         pr="provides {v}"),
    Attr("depo", "num", "Upfront deposit", lo=0, hi=50, step=5, unit="%", vp=["ask for {c} {v} upfront"],
         field=("Max deposit", None), pr="asks for {v} upfront"),
]


def _contr_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng), "project": rng.choice(PROJECTS)}


CONTRACTOR = Domain(
    "contractor", "contractor", "contractors", "Contractor", CONTR_LABELS, CONTR_ATTRS,
    makers=[
        (3, "bid", mk_cmp("bid", LE, 0.2, 0.7)),
        (3, "lic", mk_bool("lic")),
        (2, "ins", mk_bool("ins")),
        (2, "start", mk_date("start", LE, 10, 45)),
        (2, "weeks", mk_cmp("weeks", LE, 0.2, 0.6)),
        (2, "finish", mk_derived("finish", ["start", "weeks"],
                                 lambda ctx: ("+", ("a", "start"), ("*", ("a", "weeks"), ("k", 7))), LE,
                                 lambda rng, ctx, D: ctx["today"] + rng.randint(40, 150),
                                 ["be finished {c} {v}", "complete the work {c} {v}"], fd,
                                 ctx_fn=lambda ctx, st, ci: "A job finishes on its start date plus its duration in weeks.",
                                 step=1, tags=("temporal", "multi_hop"), cls="date", group="weeks")),
        (2, "warr", mk_cmp("warr", GE, 0.1, 0.5, strict_p=0.1)),
        (1, "rating", mk_cmp("rating", GE, 0.3, 0.8)),
        (1, "refs", mk_cmp("refs", GE, 0.2, 0.6, strict_p=0.0)),
        (2, "depo", mk_cmp("depo", LE, 0.1, 0.5, neg_p=0.35)),
    ],
    ties=[mk_tie("bid", [(("a", "bid"), "min")], "the lowest bid", ["bid"]),
          mk_tie("finish", [(("+", ("a", "start"), ("*", ("a", "weeks"), ("k", 7))), "min"), (("a", "bid"), "min")],
                 "the earliest finish date, start date plus duration (then the lower bid)", ["start", "weeks", "bid"],
                 tags=("multi_hop",)),
          mk_tie("warr", [(("a", "warr"), "max"), (("a", "bid"), "min")], "the longest warranty (then the lower bid)",
                 ["warr", "bid"])],
    ctx_fn=_contr_ctx, no_distract=["lic", "ins"],
    cs=lambda ctx, st: {"todays": fd(ctx["today"], st)},
    contexts=[("We're choosing a contractor for our {project}.", "{name} is choosing a contractor for a {project}."),
              ("I got quotes for the {project} and need to hire one firm.", "{name} got quotes for a {project} and needs to hire one firm.")],
    questions=["Which contractor should {name} hire{ifany}?", "Which contractor meets every requirement for the {project}{ifany}?",
               "Which of the bids satisfies all of the stated requirements{ifany}?"],
    intros=["Bids received:", "Contractor quotes:", "Firms that quoted:"],
    subjects=["Quotes for the {project}", "Hiring a contractor"],
)

# ================================================================================================ laptops
LAPTOP_LABELS = ["Vireo Air", "Vireo Pro", "Kestrel Book", "Kestrel Studio", "Nimbus Lite", "Nimbus Plus", "Orion Book",
                 "Orion Flex", "Tarn Ultra", "Tarn Work", "Lumen Slim", "Lumen Max", "Quill Air", "Quill Edge",
                 "Sparrow Go", "Sparrow Pro", "Atlas Note", "Atlas Note Plus", "Cinder Book", "Cinder Pro", "Delta Slate",
                 "Delta Workstation", "Ember Air", "Ember Pro", "Fjord Book", "Fjord Plus", "Granite Pro", "Harbor Book",
                 "Iris Air", "Juno Flex"]
PORTS = ["USB-C", "USB-A", "HDMI", "Ethernet", "SD card reader"]
LAPTOP_ATTRS = [
    Attr("price", "money", "Price", lo=49900, hi=299900, step=10000, vp=["cost {c} {v}"], field=("Max price", None),
         pr="costs {v}", missing_ok=False),
    Attr("ram", "num", "RAM", lo=8, hi=64, step=8, unit=" GB", gen=lambda rng, ctx, o: rng.choice([8, 16, 16, 24, 32, 64]),
         vp=["have {c} {v} of RAM"], field=(None, "Min RAM"), pr="has {v} of RAM"),
    Attr("ssd", "num", "Storage", lo=256, hi=2000, step=1, unit=" GB", gen=lambda rng, ctx, o: rng.choice([256, 512, 512, 1000, 2000]),
         vp=["have {c} {v} of storage"], field=(None, "Min storage"), pr="has {v} of storage"),
    Attr("kg", "num", "Weight", lo=95, hi=260, step=5, scale=100, unit=" kg", vp=["weigh {c} {v}"],
         field=("Max weight", None), pr="weighs {v}", missing_ok=False),
    Attr("batt", "num", "Battery life", lo=50, hi=200, step=5, scale=10, unit=" h", vp=["last {c} {v} on battery"],
         field=(None, "Min battery life"), pr="lasts {v} on battery"),
    Attr("os", "cat", "OS", cats=["Windows", "macOS", "ChromeOS", "Linux"], vp=["run {v}"], pr="runs {v}", missing_ok=False),
    Attr("ports", "set", "Ports", items=PORTS, kset=(1, 4), vp=["have {v} ports"], pr="has {v} ports"),
    Attr("warr", "num", "Warranty", lo=1, hi=4, unit=("year", "years"), cls="count", vp=["come with a warranty of {c} {v}"],
         pr="comes with a {v} warranty"),
]


def _lap_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng),
            "who": rng.choice(["new starters in the design team", "field engineers", "the finance team",
                               "a university course", "the sales team", "our support staff"])}


LAPTOP = Domain(
    "laptop", "laptop", "laptops", "Model", LAPTOP_LABELS, LAPTOP_ATTRS,
    makers=[
        (3, "price", mk_cmp("price", LE, 0.2, 0.7)),
        (3, "ram", mk_cmp("ram", GE, strict_p=0.0, tlo=16, thi=32, tstep=8)),
        (1, "ssd", mk_cmp("ssd", GE, strict_p=0.0, tlo=512, thi=512, tstep=1, vstep=488)),
        (2, "ssd", mk_xunit("ssd", GE, "TB", Fr(1000), Fr(1024), [5, 10, 20], ["have {c} {v} of storage"],
                            "(1 TB = 1,000 GB)", dec=1)),
        (2, "kg", mk_cmp("kg", LE, 0.2, 0.6)),
        (2, "kg", mk_xunit("kg", LE, "lb", Fr(1000, 22), Fr(10000000, 220462), [x for x in range(28, 52, 2)],
                           ["weigh {c} {v}"], "(1 kg = 2.2 lb)", dec=1)),
        (2, "batt", mk_cmp("batt", GE, 0.3, 0.7)),
        (2, "os", mk_cat("os", (1, 2), neg_p=0.4)),
        (2, "ports", mk_set("ports", modes=("has", "all"), w=(5, 3))),
        (1, "warr", mk_cmp("warr", GE, strict_p=0.0, tlo=2, thi=3, tstep=1)),
    ],
    ties=[mk_tie("price", [(("a", "price"), "min")], "the lowest price", ["price"]),
          mk_tie("light", [(("a", "kg"), "min"), (("a", "price"), "min")], "the lowest weight (then the lower price)",
                 ["kg", "price"]),
          mk_tie("batt", [(("a", "batt"), "max")], "the longest battery life", ["batt"])],
    ctx_fn=_lap_ctx,
    contexts=[("I'm buying laptops for {who} and need to standardise on one model.",
               "{name} is buying laptops for {who} and needs to standardise on one model."),
              ("We need to pick a single laptop model for {who}.", "{name} needs to pick a single laptop model for {who}.")],
    questions=["Which laptop model should {name} order{ifany}?", "Which model meets all of the purchasing requirements{ifany}?",
               "Which of the listed laptops satisfies every requirement{ifany}?"],
    intros=["Models from the reseller:", "Laptop options:", "Spec sheet summary:"],
    subjects=["Laptop order", "Standard laptop"],
)

# ================================================================================================ phone plans
PHONE_LABELS = ["Talkmore Lite", "Talkmore Max", "Signal Basic", "Signal Unlimited", "Orbit Go", "Orbit Plus",
                "Nomad Travel", "Nomad Home", "Beacon Mobile Start", "Beacon Mobile Pro", "Pulse Essentials",
                "Pulse Premium", "Wavelink Flex", "Wavelink Max", "Echo Saver", "Echo Family", "Relay Basic", "Relay Max",
                "Kite Mobile Mini", "Kite Mobile Plus", "Lumen Connect", "Lumen Connect Pro", "Tandem Share", "Tandem Solo"]
ROAM = ["Canada", "Mexico", "EU", "UK", "Japan"]
PHONE_ATTRS = [
    Attr("monthly", "money", "Monthly price", lo=999, hi=8899, step=100, cents=True, vp=["cost {c} {v} a month"],
         field=("Max monthly price", None), pr="costs {v} a month", missing_ok=False),
    Attr("data", "num", "Data", lo=2, hi=1000, step=1, unit=" GB",
         gen=lambda rng, ctx, o: rng.choice([2, 5, 10, 15, 20, 30, 50, 75, 100, 1000]), vp=["include {c} {v} of data"],
         field=(None, "Min data"), pr="includes {v} of data"),
    Attr("contract", "num", "Contract", lo=0, hi=24, step=12, unit=("month", "months"), cls="count",
         vp=["have a contract of {c} {v}"], pr="has a {v} contract", missing_ok=False),
    Attr("hotspot", "bool", "Hotspot", p=0.6, vp=["allow hotspot use"], pr=("allows hotspot use", "does not allow hotspot use")),
    Attr("roam", "set", "Roaming included", items=ROAM, kset=(0, 3), vp=["include roaming in {v}"],
         pr=("includes roaming in {v}", "includes no roaming")),
    Attr("setup", "money", "Setup fee", lo=0, hi=5000, step=500, pr="has a {v} setup fee", missing_ok=False),
    Attr("g5", "bool", "5G", p=0.6, vp=["include 5G access"], noun="5G access", pr=("includes 5G", "has no 5G")),
]
PHONE_ATTRS[1].special = {1000: "unlimited"}
PHONE_ATTRS[2].special = {0: "no contract"}


def _contract_pr(v, s):
    return "has no contract" if v == 0 else f"has a contract of {s}"


PHONE_ATTRS[2].pr = _contract_pr


def _data_pr(v, s):
    return "includes unlimited data" if v == 1000 else f"includes {s} of data"


PHONE_ATTRS[1].pr = _data_pr


def _phone_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng)}


PHONE_PLAN = Domain(
    "phone_plan", "phone plan", "phone plans", "Plan", PHONE_LABELS, PHONE_ATTRS,
    makers=[
        (3, "monthly", mk_cmp("monthly", LE, 0.2, 0.7)),
        (2, "year", mk_derived("year", ["monthly", "setup"], lambda ctx: ("+", ("*", ("a", "monthly"), ("k", 12)), ("a", "setup")),
                               LE, lambda rng, ctx, D: 1000 * rng.randint(18, 90),
                               ["cost {c} {v} in the first year, setup fee included"], money_fmt(), step=1000,
                               tags=("numeric", "multi_hop", "units"), group="monthly")),
        (3, "data", mk_cmp("data", GE, strict_p=0.1, tlo=10, thi=50, tstep=5, vstep=5)),
        (2, "contract", mk_cmp("contract", LE, strict_p=0.0, neg_p=0.4, tlo=12, thi=12, tstep=12, lo=12, hi=24)),
        (2, "hotspot", mk_bool("hotspot")),
        (2, "roam", mk_set("roam", modes=("has", "all"), w=(5, 2))),
        (1, "g5", mk_bool("g5")),
    ],
    ties=[mk_tie("monthly", [(("a", "monthly"), "min")], "the lowest monthly price", ["monthly"]),
          mk_tie("data", [(("a", "data"), "max"), (("a", "monthly"), "min")], "the most data (then the lower monthly price)",
                 ["data", "monthly"])],
    ctx_fn=_phone_ctx,
    contexts=[("I'm switching phone plans and want one that fits the rules below.",
               "{name} is switching phone plans and wants one that fits the rules below."),
              ("I'm picking a new mobile plan before my contract ends.", "{name} is picking a new mobile plan before a contract ends.")],
    questions=["Which phone plan should {name} choose{ifany}?", "Which plan meets all of the requirements{ifany}?",
               "Which of the listed plans satisfies every stated requirement{ifany}?"],
    intros=["Plans on the comparison site:", "Current offers:", "Plans I found:"],
    subjects=["New phone plan", "Switching plans"],
    nice=["g5"],
)

# ================================================================================================ course sections
COURSES = ["STAT 210", "BIO 115", "ECON 201", "CHEM 142", "HIST 230", "PSYC 101", "MATH 221", "ENGL 205"]
SECTION_LABELS = [f"{c}-{k:02d}" for c in COURSES for k in range(1, 13)]
DAYPATS = [("Mon", "Wed", "Fri"), ("Tue", "Thu"), ("Mon", "Wed"), ("Wed", "Fri"), ("Mon",), ("Tue",), ("Thu",), ("Fri",),
           ("Tue", "Thu"), ("Mon", "Wed", "Fri")]
INSTR = ["Dr. Adeyemi", "Dr. Brennan", "Prof. Castillo", "Dr. Duarte", "Prof. Haddad", "Dr. Ibarra", "Prof. Kowalski",
         "Dr. Larsen"]


def _sec_end(rng, ctx, o):
    s = o.get("start")
    s = 10 * 60 if (s is None or unk(s)) else s
    return min(21 * 60 + 50, s + rng.choice([50, 75, 80, 110, 170]))


def _sec_valid(o, ctx):
    s, e = o.get("start"), o.get("end")
    if s is not None and e is not None and not unk(s) and not unk(e):
        return 50 <= e - s <= 180
    return True


SEC_ATTRS = [
    Attr("days", "set", "Days", items=["Mon", "Tue", "Wed", "Thu", "Fri"], gen=lambda rng, ctx, o: frozenset(rng.choice(DAYPATS)),
         vp=["meet on {v}"], pr="meets {v}", missing_ok=False),
    Attr("start", "time", "Starts", lo=8 * 60, hi=19 * 60, step=30, cls="time", vp=["start {c} {v}"],
         field=(None, "Earliest start"), pr="starts at {v}", missing_ok=False),
    Attr("end", "time", "Ends", lo=8 * 60 + 50, hi=21 * 60 + 50, step=5, cls="time", gen=_sec_end, vp=["end {c} {v}"],
         field=("Latest end", None), pr="ends at {v}", missing_ok=False),
    Attr("seats", "num", "Open seats", lo=0, hi=30, unit=("open seat", "open seats"), cls="count", vp=["have {c} {v}"],
         pr="has {v}", gen=lambda rng, ctx, o: rng.choice([0, 0, 1, 2, 3, 5, 8, 12, 20])),
    Attr("mode", "cat", "Format", cats=["in person", "online", "hybrid"], vp=["be taught {v}"], pr="is taught {v}",
         missing_ok=False),
    Attr("instr", "cat", "Instructor", cats=INSTR, vp=["be taught by {v}"], pr="is taught by {v}", missing_ok=False),
    Attr("campus", "cat", "Campus", cats=["Main campus", "North campus", "Downtown campus"], vp=["be held on the {v}"],
         pr="is held on the {v}", missing_ok=False),
]


def _sec_ctx(rng):
    cd = rng.choice([("Tue", "Thu"), ("Mon", "Wed"), ("Mon", "Wed", "Fri"), ("Fri",), ("Tue",)])
    cs = rng.randrange(9 * 60, 17 * 60, 30)
    return {"today": base_day(rng), "name": pick_name(rng), "course": rng.choice(COURSES), "cdays": cd, "cstart": cs,
            "cend": cs + rng.choice([120, 180, 240]),
            "job": rng.choice(["part-time job", "lab assistant shift", "volunteering shift", "sports practice"])}


def _sec_labels(rng, ctx, n):
    ks = sorted(rng.sample(range(1, 13), n))
    return [f"{ctx['course']}-{k:02d}" for k in ks]


def _mk_clash(rng, ctx, D):
    ti = rng.randrange(12)

    def build(p):
        pr = ("or", ("disj", ("a", "days"), tuple(p["d"])), ("cmp", ("a", "end"), LE, ("k", p["s"])),
              ("cmp", ("a", "start"), GE, ("k", p["e"])))
        return pr, [("end", p["s"] + d * 5) for d in (-1, 0, 1)] + [("start", p["e"] + d * 30) for d in (-1, 0, 1)]

    def text(p, st, mi):
        r = [f"clash with {ctx['name']}'s {ctx['job']}", f"overlap {ctx['name']}'s {ctx['job']}"][ti % 2]
        s = f"{modal('neg', mi)} {r}"
        return {"inline": s + " (back-to-back is fine)", "bullet": cap(s) + " (back-to-back is fine).", "field": None}

    def ctxs(p, st):
        dd = ", ".join(x for x in ["Mon", "Tue", "Wed", "Thu", "Fri"] if x in p["d"])
        return f"{ctx['name']} has a {ctx['job']} on {dd} from {ft(p['s'], st)} to {ft(p['e'], st)}."

    def vary(p, rng2):
        out = []
        for d in (-60, -30, 30, 60, 90, -90):
            out.append({"d": p["d"], "s": p["s"] + d, "e": p["e"] + d})
        for dd in [("Tue", "Thu"), ("Mon", "Wed"), ("Mon", "Wed", "Fri"), ("Fri",), ("Tue",), ("Wed",), ("Thu",)]:
            if tuple(dd) != tuple(p["d"]):
                out.append({"d": dd, "s": p["s"], "e": p["e"]})
        return [q for q in out if 7 * 60 <= q["s"] and q["e"] <= 22 * 60]

    def chk(p, st):
        return [("window_ctx", ft(p["s"], st), ft(p["e"], st))]
    return FnCon("clash", ["days", "start", "end"], {"d": tuple(ctx["cdays"]), "s": ctx["cstart"], "e": ctx["cend"]},
                 build, text, vary, chk, tags={"temporal", "negation", "implicit"}, group="clash", mscale=30, ctxs=ctxs)


def _mk_seats(rng, ctx, D):
    return CmpCon("seats", D.A["seats"], GE, 1, "pos", wi=rng.choice([0, 3]), vpi=0)


COURSE_SECTION = Domain(
    "course_section", "section", "sections", "Section", SECTION_LABELS, SEC_ATTRS,
    makers=[
        (4, "clash", _mk_clash),
        (3, "seats", _mk_seats),
        (2, "mode", mk_cat("mode", (1, 2), neg_p=0.4)),
        (1, "instr", mk_cat("instr", (1, 2), only_neg=True)),
        (2, "end", mk_cmp("end", LE, 0.4, 0.85, strict_p=0.1, tlo=12 * 60, thi=19 * 60, tstep=30)),
        (2, "start", mk_cmp("start", GE, 0.05, 0.4, strict_p=0.1, tlo=9 * 60, thi=13 * 60, tstep=30)),
        (1, "campus", mk_cat("campus", (1, 2), neg_p=0.3)),
    ],
    ties=[mk_tie("early", [(("a", "start"), "min")], "the earliest start time", ["start"]),
          mk_tie("seats", [(("a", "seats"), "max")], "the most open seats", ["seats"])],
    ctx_fn=_sec_ctx, valid=_sec_valid, label_fn=_sec_labels, always=["days", "start", "end"], no_distract=["seats"],
    contexts=[("I need to register for one section of {course} next term.",
               "{name} needs to register for one section of {course} next term."),
              ("Registration opens tomorrow and I have to pick a {course} section.",
               "Registration opens tomorrow and {name} has to pick a {course} section.")],
    questions=["Which section should {name} register for{ifany}?", "Which {course} section meets every requirement{ifany}?",
               "Which of the listed sections satisfies all of the constraints{ifany}?"],
    intros=["Sections in the timetable:", "Open sections:", "Timetable entries:"],
    subjects=["{course} registration", "Picking a {course} section"],
)

# ================================================================================================ clinic appointments
APPT_LABELS = [f"Appointment {c}" for c in "ABCDEFGHJKLM"]
CLINICIANS = ["Dr. Osei", "Dr. Lindqvist", "Dr. Patel", "Dr. Moreau", "Dr. Tanaka", "Dr. Haddad", "NP Novak", "NP Castillo"]
INSURERS = ["Meridian Health", "Crestline", "Unity Mutual", "Harbor Care", "Evergreen Assurance"]


def _appt_derive(o, ctx):
    d = o.get("date")
    o["wd"] = MISSING if (d is None or unk(d)) else dt.date.fromordinal(d).weekday()


APPT_ATTRS = [
    Attr("clin", "cat", "Clinician", cats=CLINICIANS, vp=["be with {v}"], pr="is with {v}", missing_ok=False),
    Attr("date", "date", "Date", date_lo=1, date_hi=28, cls="date", vp=["be {c} {v}", "take place {c} {v}"],
         field=("Latest date", "Earliest date"), pr="is on {v}", missing_ok=False),
    Attr("time", "time", "Time", lo=8 * 60, hi=18 * 60 + 30, step=15, cls="time", vp=["start {c} {v}"],
         field=("Latest time", "Earliest time"), pr="starts at {v}", missing_ok=False),
    Attr("site", "cat", "Location", cats=["Riverside Clinic", "Northgate Health Centre", "Eastside Medical", "Hillview Practice"],
         vp=["be at {v}"], pr="is at {v}", missing_ok=False),
    Attr("kind", "cat", "Visit type", cats=["in person", "by video", "by phone"], vp=["take place {v}"],
         pr="takes place {v}", missing_ok=False),
    Attr("ins", "set", "Insurance accepted", items=INSURERS, kset=(1, 4), vp=["accept {v}"], pr="accepts {v}"),
    Attr("lang", "set", "Languages spoken", items=["English", "Spanish", "Mandarin", "Vietnamese", "Arabic", "Polish"],
         kset=(1, 3), vp=["be with a clinician who speaks {v}"], pr="is with a clinician who speaks {v}"),
    Attr("wd", "num", "Weekday", derived=True),
]


def _appt_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng),
            "reason": rng.choice(["a follow-up visit", "a skin check", "an annual physical", "a medication review",
                                  "a sports injury"])}


def _mk_weekday(rng, ctx, D):
    bad = rng.choice([(5, 6), (0,), (4,), (2,)])
    names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    vi = rng.randrange(12)

    def build(p):
        return ("not", ("in", ("a", "wd"), frozenset(p["b"]))), []

    def text(p, st, mi):
        dn = " or ".join(names[k] + "s" for k in p["b"]) if p["b"] != (5, 6) else "a weekend"
        s = f"{modal('neg', mi)} {['fall on', 'be on'][vi % 2]} {dn}"
        return {"inline": s, "bullet": cap(s) + ".", "field": None}

    def vary(p, rng2):
        return [{"b": b} for b in [(0,), (1,), (2,), (3,), (4,)] if b != p["b"]]

    def chk(p, st):
        return [("weekday",)]
    return FnCon("weekday", ["date"], {"b": bad}, build, text, vary, chk, tags={"temporal", "negation", "multi_hop"},
                 group="weekday", mscale=1)


CLINIC_APPT = Domain(
    "clinic_appointment", "appointment", "appointments", "Slot", APPT_LABELS, APPT_ATTRS,
    makers=[
        (3, "date", mk_date("date", LE, 5, 20)),
        (1, "date2", mk_date("date", GE, 3, 12, cid="date2")),
        (1, "weekday", _mk_weekday),
        (3, "time", mk_cmp("time", GE, 0.4, 0.8, strict_p=0.15)),
        (2, "kind", mk_cat("kind", (1, 2), neg_p=0.35)),
        (3, "ins", mk_set("ins", modes=("has",), w=(1,))),
        (2, "lang", mk_set("lang", modes=("has",), w=(1,))),
        (1, "site", mk_cat("site", (1, 2), neg_p=0.5)),
        (1, "clin", mk_cat("clin", (1, 2), only_neg=True)),
    ],
    ties=[mk_tie("early", [(("a", "date"), "min"), (("a", "time"), "min")], "the earliest date and time", ["date", "time"])],
    ctx_fn=_appt_ctx, letters=True, derive=_appt_derive, always=["date", "time"],
    cs=lambda ctx, st: {"todays": fd(ctx["today"], st)},
    contexts=[("I'm booking {reason} and the clinic sent me some open appointments.",
               "{name} is booking {reason} and the clinic sent some open appointments."),
              ("I need an appointment for {reason}; today is {todays}.", "{name} needs an appointment for {reason}; today is {todays}.")],
    questions=["Which appointment should {name} book{ifany}?", "Which appointment meets all of the requirements{ifany}?",
               "Which of the offered appointments satisfies every requirement{ifany}?"],
    intros=["Open appointments:", "Slots offered by the clinic:", "Available times:"],
    subjects=["Booking {reason}", "Clinic appointment"],
)

# ================================================================================================ childcare
CARE_LABELS = ["Little Acorns", "Sunbeam Nursery", "Bright Steps", "Tiny Oaks", "Rainbow Kite", "Maple Tree Nursery",
               "Puddle Jumpers", "Honeycomb Childcare", "Treetops Nursery", "Pebbles Early Learning", "Ladybird Lodge",
               "Starfish Nursery", "Willow Tots", "Buttercup House", "Kiteflyers", "Acorn & Oak", "Blue Wren Nursery",
               "Clover Kids", "Daisy Chain Nursery", "Fernhill Tots", "Goslings", "Hopscotch House", "Jellybean Nursery",
               "Little Harbour", "Moonbeam Childcare", "Nest Early Years", "Otter Den Nursery", "Poppy Fields Nursery",
               "Robin's Nest Nursery", "Seedlings"]


def _care_valid(o, ctx):
    a, b = o.get("mina"), o.get("maxa")
    if a is not None and b is not None and not unk(a) and not unk(b):
        return b >= a + 12
    return True


CARE_ATTRS = [
    Attr("fee", "money", "Monthly fee", lo=60000, hi=240000, step=1000, vp=["cost {c} {v} a month"],
         field=("Max monthly fee", None), pr="costs {v} a month", missing_ok=False),
    Attr("mina", "num", "Youngest age accepted", lo=0, hi=36, step=3, unit=("month", "months"), pr="takes children from {v}",
         missing_ok=False),
    Attr("maxa", "num", "Oldest age accepted", lo=24, hi=72, step=6, unit=("month", "months"), pr="takes children up to {v}",
         missing_ok=False),
    Attr("opens", "time", "Opens", lo=6 * 60 + 30, hi=9 * 60, step=15, cls="time", pr="opens at {v}", missing_ok=False),
    Attr("closes", "time", "Closes", lo=16 * 60, hi=19 * 60, step=15, cls="time", pr="closes at {v}", missing_ok=False),
    Attr("spots", "num", "Places free", lo=0, hi=5, unit=("place", "places"), cls="count", vp=["have {c} {v} free"],
         pr="has {v} free"),
    Attr("dist", "num", "Distance from home", lo=3, hi=150, scale=10, unit=" km", vp=["be {c} {v} from home"],
         field=("Max distance", None), pr="is {v} from home"),
    Attr("meals", "bool", "Meals included", p=0.5, vp=["include meals"], noun="meals", pr=("includes meals", "does not include meals")),
    Attr("lic", "bool", "Licensed", p=0.85, vp=["be licensed"], pr=("is licensed", "is not licensed")),
]


def _care_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng), "age": rng.randint(6, 60)}


def _age_sent(x, st):
    y, m = divmod(x, 12)
    if y == 0:
        return f"The child is {x} months old."
    if m == 0:
        return f"The child is {y} year{'s' if y > 1 else ''} old (exactly {x} months)." if y > 1 else f"The child turned 1 today ({x} months)."
    return f"The child is {y} year{'s' if y > 1 else ''} and {m} month{'s' if m > 1 else ''} old."


CHILDCARE = Domain(
    "childcare", "nursery", "nurseries", "Nursery", CARE_LABELS, CARE_ATTRS,
    makers=[
        (4, "age", mk_range("mina", "maxa", lambda rng, ctx, D: ctx["age"], _age_sent,
                            ["accept a child of that age", "take a child of that age (within its age range)"], step=1,
                            vary_d=(1, 2, 3, 6, -1, -2, -3, -6), tags=("numeric", "implicit", "units", "multi_hop"))),
        (3, "opens", mk_implicit("opens", LE, lambda rng, ctx, D: rng.randrange(7 * 60, 9 * 60 + 1, 15),
                                 lambda rng, ctx, t: ("Drop-off has to be at {v}.", None), "open at or before drop-off time",
                                 vfmt=lambda t, st: fmt_time(t, st["time"]))),
        (3, "closes", mk_implicit("closes", GE, lambda rng, ctx, D: rng.randrange(16 * 60 + 30, 18 * 60 + 31, 15),
                                  lambda rng, ctx, t: ("Pick-up is at {v} at the earliest.", None),
                                  "close at or after pick-up time", vfmt=lambda t, st: fmt_time(t, st["time"]))),
        (3, "spots", mk_cmp("spots", GE, strict_p=0.0, tlo=1, thi=1, tstep=1)),
        (2, "fee", mk_cmp("fee", LE, 0.2, 0.7)),
        (1, "dist", mk_cmp("dist", LE, 0.1, 0.5)),
        (1, "meals", mk_bool("meals")),
        (2, "lic", mk_bool("lic")),
    ],
    ties=[mk_tie("fee", [(("a", "fee"), "min")], "the lowest monthly fee", ["fee"]),
          mk_tie("dist", [(("a", "dist"), "min")], "the shortest distance from home", ["dist"])],
    ctx_fn=_care_ctx, no_distract=["lic", "spots"],
    contexts=[("I'm looking for a nursery place for my child.", "{name} is looking for a nursery place for a child."),
              ("We're choosing a nursery before I go back to work.", "{name}'s family is choosing a nursery before {name} goes back to work.")],
    questions=["Which nursery should {name} choose{ifany}?", "Which nursery meets all of the family's requirements{ifany}?",
               "Which of the listed nurseries satisfies every requirement{ifany}?"],
    intros=["Nurseries visited:", "Local nurseries:", "Nursery shortlist:"],
    subjects=["Nursery place", "Choosing a nursery"],
    nice=["meals"],
)

# ================================================================================================ translators
PAIRS = ["English to Spanish", "Spanish to English", "English to French", "French to English", "English to German",
         "German to English", "English to Portuguese", "English to Japanese"]
TR_ATTRS = [
    Attr("pairs", "set", "Language pairs", items=PAIRS, kset=(1, 3), vp=["translate {v}"], pr="translates {v}"),
    Attr("rate", "money", "Rate per word", lo=6, hi=30, step=1, cents=True, vp=["charge {c} {v} per word"],
         field=("Max rate per word", None), pr="charges {v} per word", missing_ok=False),
    Attr("turn", "num", "Turnaround", lo=1, hi=14, unit=("working day", "working days"), cls="count",
         vp=["deliver within {v}"], pr="delivers in {v}"),
    Attr("cert", "bool", "Certified translator", p=0.5, vp=["be a certified translator"],
         pr=("is a certified translator", "is not certified")),
    Attr("spec", "set", "Specialisms", items=["legal", "medical", "technical", "marketing", "financial"], kset=(1, 3),
         vp=["specialise in {v} texts"], pr="specialises in {v} texts"),
    Attr("rating", "num", "Client rating", lo=30, hi=50, scale=10, unit="/5", vp=["have a client rating of {c} {v}"],
         field=(None, "Min rating"), pr="is rated {v}"),
]


def _mk_turn(rng, ctx, D):
    a = D.A["turn"]
    return CmpCon("turn", a, LE, rng.randint(3, 8), "pos", wi=rng.randrange(12), vpi=0,
                  vp=["deliver in {c} {v}", "turn the job around in {c} {v}"])


def _tr_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng), "words": 500 * rng.randint(2, 30),
            "doc": rng.choice(["a supply contract", "a patient information leaflet", "a product manual",
                               "a marketing brochure", "an annual report", "a tenancy agreement"])}


TRANSLATOR = Domain(
    "translator", "translator", "translators", "Translator", PEOPLE, TR_ATTRS,
    makers=[
        (4, "pairs", mk_set("pairs", modes=("has", "all"), w=(6, 2))),
        (2, "spec", mk_set("spec", modes=("has",), w=(1,))),
        (3, "total", mk_derived("total", ["rate"], lambda ctx: ("*", ("a", "rate"), ("x", "words")), LE,
                                lambda rng, ctx, D: 5000 * max(1, ctx["words"] * rng.randint(8, 24) // 5000),
                                ["cost {c} {v} for the whole document", "come to {c} {v} in total"], money_fmt(),
                                ctx_fn=lambda ctx, st, ci: f"The document is {ctx['words']:,} words long.", step=1000,
                                group="rate")),
        (2, "rate", mk_cmp("rate", LE, 0.2, 0.7)),
        (2, "turn", _mk_turn),
        (2, "cert", mk_bool("cert")),
        (1, "rating", mk_cmp("rating", GE, 0.3, 0.8)),
    ],
    ties=[mk_tie("rate", [(("a", "rate"), "min")], "the lowest rate per word", ["rate"]),
          mk_tie("turn", [(("a", "turn"), "min"), (("a", "rate"), "min")], "the fastest turnaround (then the lower rate)",
                 ["turn", "rate"])],
    ctx_fn=_tr_ctx,
    contexts=[("I need {doc} translated and have quotes from freelancers.", "{name} needs {doc} translated and has quotes from freelancers."),
              ("Our team has to get {doc} translated this month.", "{name}'s team has to get {doc} translated this month.")],
    questions=["Which translator should {name} hire{ifany}?", "Which translator meets all of the requirements{ifany}?",
               "Which of the freelancers satisfies every stated requirement{ifany}?"],
    intros=["Freelancers who quoted:", "Translator profiles:", "Quotes:"],
    subjects=["Translation of {doc}", "Translator quotes"],
)

# ================================================================================================ movers
MOVER_LABELS = ["Two Rivers Moving", "Swift Crate Movers", "Blue Van Removals", "Careful Hands Moving", "Cornerstone Movers",
                "Easy Lift Removals", "Firstmile Movers", "Good Neighbour Moving", "Homeward Removals", "Keystone Moving Co.",
                "Longhaul Movers", "Milestone Removals", "New Leaf Moving", "Openroad Removals", "Pack & Go Movers",
                "Quickstep Removals", "Redwood Movers", "Safe Passage Moving", "Tall Oaks Removals", "Uptown Movers",
                "Vanguard Removals", "Waypoint Movers", "Anchor Removals", "Bluebird Moving", "Crossway Movers",
                "Dockside Removals", "Evergreen Movers", "Foxhill Removals", "Greystone Moving", "Harbour Lights Removals"]
MOVER_ATTRS = [
    Attr("quote", "money", "Quote", lo=60000, hi=600000, step=1000, vp=["quote {c} {v}"], field=("Max quote", None),
         pr="quotes {v}", missing_ok=False),
    Attr("vol", "num", "Truck capacity", lo=400, hi=1800, step=50, unit=" cu ft", vp=["have a truck of {c} {v}"],
         field=(None, "Min truck capacity"), pr="brings a truck of {v}", missing_ok=False),
    Attr("free", "bool", "Free on {date}", p=0.6, vp=["be free on moving day"], pr=("is free on {date}", "is booked on {date}")),
    Attr("cover", "bool", "Full-value cover", p=0.5, vp=["offer full-value cover"], noun="full-value cover",
         pr=("offers full-value cover", "offers only basic cover")),
    Attr("crew", "num", "Crew", lo=2, hi=6, unit=("mover", "movers"), cls="count", vp=["send {c} {v}"], pr="sends {v}"),
    Attr("stairs", "money", "Stairs fee", lo=0, hi=30000, step=2500, pr="adds a stairs fee of {v}", missing_ok=False),
    Attr("pack", "bool", "Packing service", p=0.45, vp=["offer a packing service"], pr=("offers packing", "does not offer packing")),
    Attr("rating", "num", "Rating", lo=30, hi=50, scale=10, unit="/5", vp=["have a rating of {c} {v}"], pr="is rated {v}"),
]


def _mover_ctx(rng):
    today = base_day(rng)
    return {"today": today, "name": pick_name(rng), "date": today + rng.randint(14, 60), "floor": rng.choice(["third", "fourth", "fifth"]),
            "from": rng.choice(CITIES)}


MOVER = Domain(
    "moving_company", "moving company", "moving companies", "Company", MOVER_LABELS, MOVER_ATTRS,
    makers=[
        (3, "total", mk_derived("total", ["quote", "stairs"], lambda ctx: ("+", ("a", "quote"), ("a", "stairs")), LE,
                                lambda rng, ctx, D: 5000 * rng.randint(20, 110),
                                ["cost {c} {v} in total, stairs fee included"], money_fmt(),
                                ctx_fn=lambda ctx, st, ci: f"The flat is on the {ctx['floor']} floor with no lift, so any stairs fee applies.",
                                step=5000, group="quote")),
        (2, "quote", mk_cmp("quote", LE, 0.2, 0.7)),
        (2, "vol", mk_cmp("vol", GE, 0.2, 0.7)),
        (2, "vol", mk_xunit("vol", GE, "m³", Fr(353, 10), Fr(353147, 10000), [x for x in range(15, 50, 3)],
                            ["have a truck of {c} {v}"], "(1 m³ ≈ 35.3 cu ft)", dec=0)),
        (3, "free", mk_bool("free")),
        (2, "cover", mk_bool("cover")),
        (1, "crew", mk_cmp("crew", GE, 0.2, 0.6, strict_p=0.0)),
        (1, "pack", mk_bool("pack")),
        (1, "rating", mk_cmp("rating", GE, 0.3, 0.8)),
    ],
    ties=[mk_tie("total", [(("+", ("a", "quote"), ("a", "stairs")), "min")], "the lowest total (quote plus stairs fee)",
                 ["quote", "stairs"], tags=("multi_hop",)),
          mk_tie("crew", [(("a", "crew"), "max"), (("a", "quote"), "min")], "the biggest crew (then the lower quote)",
                 ["crew", "quote"])],
    ctx_fn=_mover_ctx, hv=lambda ctx: {"date": day_month(ctx["date"])}, no_distract=["free"],
    cs=lambda ctx, st: {"dates": fd(ctx["date"], st)},
    contexts=[("I'm moving out of my flat in {from} on {dates} and need movers.", "{name} is moving out of a flat in {from} on {dates} and needs movers."),
              ("We're relocating on {dates} and got quotes from moving companies.", "{name} is relocating on {dates} and got quotes from moving companies.")],
    questions=["Which moving company should {name} book{ifany}?", "Which mover meets all of the requirements{ifany}?",
               "Which of the quoted companies satisfies every stated requirement{ifany}?"],
    intros=["Quotes received:", "Moving companies:", "Movers who replied:"],
    subjects=["Movers for {dates}", "Moving quotes"],
    nice=["pack"],
)

TRANSLATOR.person = True
DOMAINS_B = [VENUE, CATERER, CONTRACTOR, LAPTOP, PHONE_PLAN, COURSE_SECTION, CLINIC_APPT, CHILDCARE, TRANSLATOR, MOVER]
