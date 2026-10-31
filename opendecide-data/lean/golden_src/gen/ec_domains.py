"""Domain vocabulary for gen_evidence_conflict (Claude-written; no third-party text).

Each domain is one real-world attribute that dated documents report on (a flight's gate, a pool's opening time, a
product lot's recall status, ...). A domain gives
  * gran     'day' (documents dated by day) or 'min' (documents timestamped to the minute, same day)
  * vtype    'cat' (several named values), 'num' (ordered numeric values; comparisons allowed) or 'bin' (two states)
  * event    True when the attribute belongs to one fixed future event (a sailing, a match, an appointment): the
             question date is then only a knowledge cut-off, and no scheduled/temporary changes are generated
  * allow    which report kinds are realistic for it (stmt, neg, sched, temp, corr, retr)
  * sources  ordered from most to least authoritative in real life, each with an 'official' flag and a text style
             ('formal' notice/email/letter, 'casual' text/post, 'record' system record/screen, 'call' call note)
  * clause templates: pres (present tense), base (with {AUX} modal), q (yes/no interrogative), negc (negated
    clause), noun (attribute noun phrase), vn (value noun), rv (record value), field (record field name), cmp/q_cmp
    (numeric comparison clauses with {C}); bin and some cat domains give per-value clause dicts instead.
All entity names, brands and places are invented.
"""
import datetime as dt

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

PERSONS = ["Amara Obi", "Bilal Haddad", "Chen Wei", "Daniela Ruiz", "Emeka Nwosu", "Farah Siddiqui", "Gustavo Lima",
           "Hana Kobayashi", "Ibrahim Keita", "Jolene Baptiste", "Kenji Mori", "Leilani Kahale", "Mateo Rossi",
           "Nadia Petrova", "Priya Nair", "Rosa Delgado", "Sipho Dlamini", "Tamar Levi", "Umar Farouk",
           "Valentina Greco", "Wojtek Nowak", "Ximena Torres", "Yusuf Demir", "Zanele Mokoena", "Brigid Walsh",
           "Carlos Mendes", "Dilnoza Karimova", "Eero Virtanen", "Giorgos Papas", "Halima Yusuf", "Isaac Mensah",
           "Kwame Asante", "Lucia Ferrari", "Marcus Webb", "Noor Rahman", "Oskar Lind", "Paloma Vega", "Rahul Mehta",
           "Svetlana Orlova", "Tomasz Wilk", "Uzma Qureshi", "Viktor Hale", "Wren Castillo", "Yara Haddad",
           "Aiyana Redcloud", "Bongani Zulu", "Celine Marchand", "Dmitri Volkov", "Esperanza Cruz", "Finn Gallagher"]
PLACE_PAIRS = [("Harbourview", "Harbourside"), ("Northgate", "Northfield"), ("Millbrook", "Millbank"),
               ("Ashby", "Ashford"), ("Kelso", "Kelton"), ("Fenwick", "Fenmore"), ("Rowan Hill", "Rowan Vale"),
               ("Carrow", "Carlow"), ("Linden", "Lindell"), ("Eastbrook", "Westbrook"), ("Alder Park", "Alder Green"),
               ("Stonebridge", "Stoneleigh"), ("Pinecrest", "Pineview"), ("Oakmont", "Oakridge"),
               ("Brookhaven", "Brookfield"), ("Glenwood", "Glenmore"), ("Thornbury", "Thornton"),
               ("Redwood", "Redcliff"), ("Bayside", "Baymount"), ("Clearwater", "Clearfield")]


def _alt_digits(rng, s):
    """A confusable variant of a digit string: swap two adjacent different digits (or change the last digit)."""
    ds = list(s)
    idx = [i for i in range(len(ds) - 1) if ds[i] != ds[i + 1] and ds[i].isdigit() and ds[i + 1].isdigit()]
    if idx:
        i = rng.choice(idx)
        ds[i], ds[i + 1] = ds[i + 1], ds[i]
    else:
        ds[-1] = str((int(ds[-1]) + rng.randint(1, 8)) % 10)
    return "".join(ds)


def _num(rng, lo, hi):
    while True:
        s = str(rng.randint(lo, hi))
        if len(set(s)) >= 2:
            return s


def S(sg, pl, off, style, docname, ref=None):
    """A source: singular/plural name (used both in document headers and in the question's rule),
    official flag, text style, and the noun a retraction or correction uses to refer to its earlier document."""
    return {"sg": sg, "pl": pl, "off": off, "style": style, "docname": docname, "ref": ref or sg}


# -------------------------------------------------------------------------------------------------- entity makers
AIRLINES = ["OD", "KX", "ZL", "NW", "TQ", "VB", "RH", "SJ", "EY", "PM"]
CITIES = ["Lisbon", "Porto", "Oslo", "Tallinn", "Valencia", "Kraków", "Split", "Bergen", "Seville", "Cork",
          "Gdańsk", "Malaga", "Riga", "Naples", "Bilbao", "Tromsø"]


def ent_flight(rng, ctx):
    n = _num(rng, 102, 989)
    code = rng.choice(AIRLINES)
    return {"E": f"{code} {n}", "C": f"{code} {_alt_digits(rng, n)}", "dest": rng.choice(CITIES)}


def ent_pool(rng, ctx):
    a, b = rng.choice(PLACE_PAIRS)
    kind = rng.choice(["Leisure Centre", "Sports Centre", "Aquatic Centre", "Community Pool"])
    return {"E": f"{a} {kind}", "C": f"{b} {kind}"}


BRIDGES = [("Kelso Bridge", "Kelso Footbridge"), ("Marlow Street bridge", "Marlow Road bridge"),
           ("Ashby Viaduct", "Ashby Bridge"), ("Carrow Swing Bridge", "Carrow Lift Bridge"),
           ("Linden Bridge", "Linden Weir crossing"), ("Fenwick Road bridge", "Fenwick Lane bridge"),
           ("Old Mill Bridge", "New Mill Bridge"), ("Harbour Street bridge", "Harbour Road bridge"),
           ("Queen's Bridge", "King's Bridge"), ("Stonebridge underpass", "Stonebridge flyover")]


def ent_bridge(rng, ctx):
    a, b = rng.choice(BRIDGES)
    if rng.random() < 0.5:
        a, b = b, a
    return {"E": a, "C": b}


BRANDS = ["Sunmeadow", "Brightfield", "Hollowbrook", "Greenacre", "Tidewell", "Larkspur", "Kindle Farm", "Oakhaven",
          "Riverstone", "Morning Rise"]
FOODS = ["oat drink (1 litre)", "infant cereal (400 g)", "smooth peanut butter (340 g)", "frozen spinach (750 g)",
         "chicken stock cubes (10 pack)", "granola bars (6 pack)", "tahini (300 g)", "hummus (200 g)",
         "chocolate chip cookies (250 g)", "baby rice (100 g)", "ready-to-eat lentil soup (400 g)"]


def ent_lot(rng, ctx):
    n = _num(rng, 1100, 9899)
    prod = f"{rng.choice(BRANDS)} {rng.choice(FOODS)}"
    return {"E": f"lot {n} of {prod}", "C": f"lot {_alt_digits(rng, n)} of {prod}"}


def ent_code(prefix_choices, lo, hi, sep="-"):
    def f(rng, ctx):
        n = _num(rng, lo, hi)
        p = rng.choice(prefix_choices)
        return {"E": f"{p}{sep}{n}", "C": f"{p}{sep}{_alt_digits(rng, n)}"}
    return f


def ent_claim(rng, ctx):
    d = ent_code(["HC", "MV", "TR", "PH", "HX"], 10200, 98700)(rng, ctx)
    return {"E": f"claim {d['E']}", "C": f"claim {d['C']}"}


def ent_parcel(rng, ctx):
    a = rng.choice(["JX", "QP", "RL", "TK", "WM"])
    b = _num(rng, 1000, 9999)
    c = _num(rng, 1000, 9999)
    return {"E": f"parcel {a} {b} {c}", "C": f"parcel {a} {b} {_alt_digits(rng, c)}"}


SCHOOLS = [("Northfield Primary School", "Northfield Secondary School"), ("St Anne's Primary", "St Agnes' Primary"),
           ("Riverside Academy", "Riverdale Academy"), ("Maple Grove Elementary", "Maple Ridge Elementary"),
           ("Hillcrest Middle School", "Hillside Middle School"), ("Oakmont High School", "Oakridge High School"),
           ("Glenwood Infant School", "Glenmore Infant School"), ("Bayside Junior School", "Bayview Junior School")]


def fmt_day_name(d):
    return f"{WEEKDAYS[d.weekday()]} {d.day} {MONTHS[d.month - 1]}"


def ent_school(rng, ctx):
    a, b = rng.choice(SCHOOLS)
    if rng.random() < 0.5:
        a, b = b, a
    ev = fmt_day_name(ctx["event"])
    return {"E": a, "C": b, "EV": ev}


WORKSHOPS = [("Data Ethics Workshop", "Data Engineering Workshop"), ("Coastal Ecology Symposium", "Coastal Economics Symposium"),
             ("Urban Planning Forum", "Urban Policy Forum"), ("Soil Science Summer School", "Space Science Summer School"),
             ("Public Health Workshop", "Public Housing Workshop"), ("Robotics Bootcamp", "Rocketry Bootcamp"),
             ("Choral Conducting Course", "Choral Composition Course"), ("Marine Biology Colloquium", "Marine Geology Colloquium")]


def ent_workshop(rng, ctx):
    a, b = rng.choice(WORKSHOPS)
    if rng.random() < 0.5:
        a, b = b, a
    return {"E": f"the {a}", "C": f"the {b}"}


APPTS = [("physiotherapy", "dental"), ("dental", "eye-test"), ("eye-test", "physiotherapy"), ("vaccination", "dental"),
         ("hearing-test", "physiotherapy"), ("blood-test", "eye-test")]


def ent_appt(rng, ctx):
    name = rng.choice(PERSONS)
    a, b = rng.choice(APPTS)
    ev = fmt_day_name(ctx["event"])
    return {"E": f"{name}'s {a} appointment on {ev}", "C": f"{name}'s {b} appointment on {ev}"}


STREETS = ["Alder Road", "Kestrel Way", "Juniper Close", "Marlow Street", "Copper Lane", "Beacon Hill Road",
           "Foxhall Avenue", "Quarry Street", "Willow Crescent", "Tidewater Place"]


def ent_flat(rng, ctx):
    n = rng.randint(2, 88)
    fl = rng.randint(1, 6)
    a, b = rng.sample(["A", "B", "C", "D", "E", "F"], 2)
    st = rng.choice(STREETS)
    return {"E": f"Flat {fl}{a} at {n} {st}", "C": f"Flat {fl}{b} at {n} {st}"}


SOFTWARE = ["Tessera Analytics", "Northwind Ledger", "Quill Studio", "Harbor CRM", "Lumen Backup", "Atlas Scheduler",
            "Pinecone Mail Server", "Orbit POS"]


def ent_software(rng, ctx):
    p = rng.choice(SOFTWARE)
    maj = rng.randint(2, 9)
    mi = rng.randint(0, 7)
    return {"E": f"{p} {maj}.{mi}", "C": f"{p} {maj}.{mi + 1}" if rng.random() < 0.5 else f"{p} {maj + 1}.{mi}"}


FUNDS = ["Rowan Trust", "Kestrel Foundation", "Alder Fund", "Linden Charitable Trust", "Beacon Fund",
         "Harbourview Foundation", "Millbrook Trust"]
ROUNDS = [("community grants", "arts grants"), ("small research grants", "travel grants"),
          ("youth projects", "heritage projects"), ("environment grants", "education grants")]


def ent_grant(rng, ctx):
    f = rng.choice(FUNDS)
    a, b = rng.choice(ROUNDS)
    if rng.random() < 0.5:
        a, b = b, a
    return {"E": f"the {f} {a} round", "C": f"the {f} {b} round"}


def ent_district(rng, ctx):
    pairs = [("Eastbrook", "Westbrook"), ("North Linden", "South Linden"), ("Upper Carrow", "Lower Carrow"),
             ("Ashby East", "Ashby West"), ("Old Millbrook", "New Millbrook"), ("Kelso Heights", "Kelso Flats")]
    a, b = rng.choice(pairs)
    if rng.random() < 0.5:
        a, b = b, a
    return {"E": f"the {a} district", "C": f"the {b} district"}


TEAMS = ["Ashby Rovers", "Carrow United", "Millbrook Town", "Kelso Athletic", "Fenwick City", "Rowan Hill FC",
         "Linden Wanderers", "Harbourview Albion", "Stonebridge Rangers", "Bayside Harriers"]


def ent_match(rng, ctx):
    a, b = rng.sample(TEAMS, 2)
    ev = fmt_day_name(ctx["event"])
    ev2 = fmt_day_name(ctx["event"] + dt.timedelta(days=7))
    return {"E": f"the {a} v {b} match on {ev}", "C": f"the {b} v {a} match on {ev2}"}


def ent_train(rng, ctx):
    h = rng.randint(6, 21)
    m = rng.choice([12, 13, 14, 21, 23, 24, 31, 34, 41, 42, 43, 52])
    town = rng.choice(["Carrow", "Ashby", "Kelso", "Millbrook", "Fenwick", "Linden", "Thornbury", "Redcliff"])
    alt = int(str(m)[::-1])
    if alt >= 60 or alt == m:
        alt = (m + 10) % 60
    return {"E": f"the {h:02d}:{m:02d} service to {town}", "C": f"the {h:02d}:{alt:02d} service to {town}",
            "etime": h * 60 + m}


BOOKS = ["The Salt Road", "A Map of Small Rivers", "Winter in Kestrel Bay", "The Glass Orchard", "Notes on Quiet Streets",
         "The Lantern Keeper", "Paper Boats", "The Long Harbour"]


def ent_loan(rng, ctx):
    b = rng.choice(BOOKS)
    n = _num(rng, 20100, 98900)
    return {"E": f"the loan of '{b}' (item {n})", "C": f"the loan of '{b}' (item {_alt_digits(rng, n)})"}


EXHIBITS = [("'Northern Lights'", "'Northern Lines'"), ("'Paper and Ink'", "'Paper and Iron'"),
            ("'Voyages of the Ember'", "'Voyages of the Amber'"), ("'Clay Stories'", "'Clay Studies'"),
            ("'City of Glass'", "'City of Brass'"), ("'Early Maps'", "'Early Masks'")]
MUSEUMS = ["Millbank Museum", "Kelso Gallery", "Harbourview Museum of Art", "Linden Heritage Centre", "Ashby Museum"]


def ent_exhibit(rng, ctx):
    a, b = rng.choice(EXHIBITS)
    m = rng.choice(MUSEUMS)
    return {"E": f"the {a} exhibition at the {m}", "C": f"the {b} exhibition at the {m}"}


def ent_scholar(rng, ctx):
    name = rng.choice(PERSONS)
    f = rng.choice(FUNDS)
    a, b = rng.choice([("scholarship", "travel bursary"), ("bursary", "hardship grant"), ("scholarship", "book grant")])
    return {"E": f"{name}'s {f} {a}", "C": f"{name}'s {f} {b}"}


def ent_permit(rng, ctx):
    n = _num(rng, 1100, 9899)
    p = rng.choice(["BP", "PL", "BLD"])
    return {"E": f"building permit {p}-{n}", "C": f"building permit {p}-{_alt_digits(rng, n)}"}


def ent_precinct(rng, ctx):
    n = _num(rng, 12, 98)
    return {"E": f"precinct {n}", "C": f"precinct {n[::-1]}"}


def ent_account(rng, ctx):
    bank = rng.choice(["Harbour", "Kestrel", "Linden", "Beacon", "Alder"])
    a, b = rng.choice([("Easy Saver", "Fixed Saver"), ("Instant Access Saver", "Notice Saver"),
                       ("Everyday Saver", "Junior Saver"), ("Online Saver", "Branch Saver")])
    if rng.random() < 0.5:
        a, b = b, a
    return {"E": f"the {bank} {a} account", "C": f"the {bank} {b} account"}


def ent_office(rng, ctx):
    pairs = [("Leeds", "Leith"), ("Ashby", "Ashford"), ("Kelso", "Kelton"), ("Millbrook", "Millbank"),
             ("Rowan Hill", "Rowan Vale"), ("Carrow", "Carlow"), ("Linden", "Lindell")]
    a, b = rng.choice(pairs)
    return {"E": f"the {a} office", "C": f"the {b} office"}


PORTS = [("Port Ellin", "Carra"), ("Kelso Pier", "Inchmore"), ("Ashby Harbour", "Tarran Isle"),
         ("Linden Quay", "Scarp"), ("Bayside Ferry Terminal", "Holm Island")]


def ent_sailing(rng, ctx):
    a, b = rng.choice(PORTS)
    h = rng.randint(7, 20)
    m = rng.choice([0, 15, 30, 45])
    t = f"{h:02d}:{m:02d}"
    return {"E": f"the {t} sailing from {a} to {b}", "C": f"the {t} sailing from {b} to {a}", "etime": h * 60 + m}


def ent_sample(rng, ctx):
    test = rng.choice(["potassium", "sodium", "haemoglobin", "vitamin D", "ferritin", "TSH", "creatinine"])
    n = _num(rng, 1100, 9899)
    p = rng.choice(["88", "41", "63", "27"])
    return {"E": f"the {test} result for sample {p}-{n}", "C": f"the {test} result for sample {p}-{_alt_digits(rng, n)}"}


PLAYERS = [("Tomasz Wilk", "Tomas Wilkes"), ("Kofi Mensah", "Kofi Mensa"), ("Luis Ortega", "Luis Ortiz"),
           ("Jonas Berg", "Jonas Borg"), ("Aaron Hale", "Adam Hale"), ("Mikel Arana", "Mikel Aranda"),
           ("Declan Rourke", "Declan Rourk"), ("Samir Haddad", "Samir Hadad")]


def ent_player(rng, ctx):
    a, b = rng.choice(PLAYERS)
    team = rng.choice(TEAMS)
    return {"E": f"{a} of {team}", "C": f"{b} of {team}"}


GOODS = ["the 2 kg bag of Hillcrest basmati rice", "the 1 litre bottle of Oakhaven olive oil",
         "the 500 g jar of Larkspur honey", "the 12-roll pack of Softwell toilet paper", "the 1 kg tub of Greenacre yoghurt",
         "the 750 ml bottle of Tidewell dish soap", "the 400 g box of Morning Rise oats"]


def ent_goods(rng, ctx):
    g = rng.choice(GOODS)
    a, b = rng.choice(PLACE_PAIRS)
    return {"E": f"{g} at the {a} store", "C": f"{g} at the {b} store"}


ROADS = [("Fenwick Road", "Fenwick Lane"), ("Marlow Street", "Marlow Avenue"), ("Kestrel Way", "Kestrel Drive"),
         ("Copper Lane", "Copper Road"), ("Beacon Hill Road", "Beacon Hill Drive"), ("Quarry Street", "Quarry Lane")]


def ent_road(rng, ctx):
    a, b = rng.choice(ROADS)
    if rng.random() < 0.5:
        a, b = b, a
    return {"E": a, "C": b}


def ent_rx(rng, ctx):
    n = _num(rng, 1100, 9899)
    p = rng.choice(["R", "RX", "P"])
    return {"E": f"prescription {p}-{n}", "C": f"prescription {p}-{_alt_digits(rng, n)}"}


SHOPS = ["Brightfield Home", "Kestrel Outdoor", "Linden Books", "Harbour Electronics", "Oakhaven Kitchenware",
         "Alder Toys", "Beacon Sports"]


def ent_shop(rng, ctx):
    s = rng.choice(SHOPS)
    a, b = rng.choice([("online orders", "in-store purchases"), ("in-store purchases", "online orders"),
                       ("full-price items", "sale items")])
    return {"E": f"{a} from {s}", "C": f"{b} from {s}"}


# -------------------------------------------------------------------------------------------------- value makers
def times(lo, hi, step, k_lo=3, k_hi=4):
    def f(rng):
        pool = list(range(lo, hi + 1, step))
        return sorted(rng.sample(pool, rng.randint(k_lo, min(k_hi, len(pool)))))
    return f


def pick(pool, k_lo=3, k_hi=4):
    def f(rng):
        return rng.sample(pool, rng.randint(k_lo, min(k_hi, len(pool))))
    return f


def money(lo, hi, step, k_lo=3, k_hi=4):
    return times(lo, hi, step, k_lo, k_hi)


def offs_dates(k_lo=3, k_hi=4):
    """Numeric date values are day offsets from the case's end; resolved to ordinals by the generator."""
    def f(rng):
        return sorted(rng.sample(list(range(3, 40)), rng.randint(k_lo, k_hi)))
    return f


# -------------------------------------------------------------------------------------------------- domains
ALLOW_ALL = ("stmt", "neg", "sched", "temp", "corr", "retr")
TIMECMP = [("le", "no later than"), ("lt", "before"), ("gt", "later than"), ("ge", "at or after")]
DATECMP = [("le", "on or before"), ("lt", "before"), ("gt", "after"), ("ge", "on or after")]
AMTCMP = [("ge", "at least"), ("gt", "more than"), ("lt", "less than"), ("le", "at most")]

DOMAINS = [
    dict(key="flight_gate", gran="min", vtype="cat", event=False, allow=("stmt", "neg", "sched", "corr", "retr"),
         ent=ent_flight, vals=pick(["A2", "A5", "A9", "B3", "B7", "B12", "B14", "C1", "C4", "C9", "D2", "D6", "D11", "E5"]),
         noun="the departure gate for flight {E}", vn="gate {V}", rv="{V}", field="Gate",
         topic="the departure gate of flight {E}",
         pres="flight {E} departs from gate {V}", base="flight {E} {AUX} depart from gate {V}",
         q="does flight {E} depart from gate {V}", negc="flight {E} does not depart from gate {V}",
         sources=[S("airline app alert", "airline app alerts", True, "formal", "alert", "app alert"),
                  S("airport departures screen", "airport departures screens", True, "record", "screen update"),
                  S("travel agent email", "travel agent emails", False, "formal", "email"),
                  S("text from a friend at the airport", "texts from friends at the airport", False, "casual", "text"),
                  S("traveller forum post", "traveller forum posts", False, "casual", "post")],
         other=["Boarding for flight {E} is expected to start 40 minutes before departure.",
                "Flight {E} to {dest} will be operated by a larger aircraft today.",
                "Passengers on flight {E} may bring one cabin bag of up to 8 kg.",
                "A hot meal will be served on flight {E}."],
         filler=["Please allow time for security.", "Thank you for flying with us.", "Check the app for live updates."]),
    dict(key="flight_time", gran="min", vtype="num", numkind="time", event=False, allow=("stmt", "neg", "corr", "retr"),
         ent=ent_flight, vals=times(13 * 60, 20 * 60, 5),
         noun="the scheduled departure time of flight {E}", vn="{V}", rv="{V}", field="Scheduled departure",
         topic="the scheduled departure time of flight {E}",
         pres="flight {E} is scheduled to depart at {V}", base="flight {E} {AUX} depart at {V}",
         q="is flight {E} scheduled to depart at {V}", negc="flight {E} is not scheduled to depart at {V}",
         cmp="flight {E} is scheduled to depart {C} {V}", q_cmp="is flight {E} scheduled to depart {C} {V}",
         ops=TIMECMP,
         sources=[S("airline app alert", "airline app alerts", True, "formal", "alert", "app alert"),
                  S("airport departures screen", "airport departures screens", True, "record", "screen update"),
                  S("travel agent email", "travel agent emails", False, "formal", "email"),
                  S("text from a friend", "texts from friends", False, "casual", "text")],
         other=["Flight {E} will board at gate B7.", "Check-in for flight {E} closes 45 minutes before departure.",
                "Flight {E} to {dest} is operated by a partner airline."],
         filler=["We apologise for any inconvenience.", "Please keep your boarding pass ready."]),
    dict(key="pool_hours", gran="day", vtype="num", numkind="time", event=False, allow=ALLOW_ALL,
         ent=ent_pool, vals=times(6 * 60, 9 * 60, 30),
         noun="the weekday opening time of the pool at {E}", vn="{V}", rv="{V}", field="Pool opens (weekdays)",
         topic="the weekday opening time of the pool at {E}",
         pres="the pool at {E} opens at {V} on weekdays", base="the pool at {E} {AUX} open at {V} on weekdays",
         q="does the pool at {E} open at {V} on weekdays", negc="the pool at {E} does not open at {V} on weekdays",
         cmp="the pool at {E} opens {C} {V} on weekdays", q_cmp="does the pool at {E} open {C} {V} on weekdays",
         ops=TIMECMP,
         sources=[S("centre website notice", "centre website notices", True, "formal", "website notice", "notice"),
                  S("reception noticeboard", "reception noticeboard notices", True, "formal", "noticeboard notice", "notice"),
                  S("front-desk phone call", "front-desk phone calls", False, "call", "call"),
                  S("community group post", "community group posts", False, "casual", "post"),
                  S("local newsletter", "local newsletters", False, "formal", "newsletter item")],
         other=["The sauna at {E} will close at 8 p.m. on Sundays.", "The gym at {E} is adding two spin classes.",
                "Swimming lessons at {E} restart after the school holidays.", "The café at {E} now takes card payments only."],
         filler=["Thank you for your patience.", "Lockers now take coins and tokens.", "Members, remember to bring your card."]),
    dict(key="bridge", gran="day", vtype="bin", event=False, allow=("stmt", "sched", "temp", "corr", "retr"), temp_vals=["closed"],
         ent=ent_bridge, vals=lambda rng: ["open", "closed"],
         pervalue={
             "open": {"pres": "the {E} is open to traffic", "base": "the {E} {AUX} be open to traffic",
                      "q": "is the {E} open to traffic", "negc": "the {E} is not open to traffic",
                      "negpres": "the {E} is no longer closed to traffic", "vn": "open to traffic", "rv": "OPEN"},
             "closed": {"pres": "the {E} is closed to traffic", "base": "the {E} {AUX} be closed to traffic",
                        "q": "is the {E} closed to traffic", "negc": "the {E} is not closed to traffic",
                        "negpres": "the {E} is not open to traffic", "vn": "closed to traffic", "rv": "CLOSED"}},
         field="Traffic status", topic="whether the {E} is open to traffic",
         sources=[S("council roadworks notice", "council roadworks notices", True, "formal", "notice"),
                  S("highways agency website", "highways agency website updates", True, "formal", "website update", "update"),
                  S("local radio traffic report", "local radio traffic reports", False, "spoken", "report"),
                  S("residents' group post", "residents' group posts", False, "casual", "post")],
         other=["Parking on the approach to the {E} is suspended for resurfacing.",
                "A new cycle lane is planned next to the {E}.", "Street lighting on the {E} will be upgraded next year."],
         filler=["Diversions are signposted.", "We apologise for the disruption.", "Allow extra time for journeys."]),
    dict(key="recall", gran="day", vtype="bin", event=False, allow=("stmt", "corr", "retr"),
         ent=ent_lot, vals=lambda rng: ["recalled", "cleared"],
         pervalue={
             "recalled": {"pres": "{E} is included in the recall", "base": "{E} {AUX} be included in the recall",
                          "q": "is {E} included in the recall", "negc": "{E} is not included in the recall",
                          "negpres": "{E} is no longer cleared for sale", "vn": "included in the recall", "rv": "RECALLED"},
             "cleared": {"pres": "{E} is not included in the recall", "base": "{E} {AUX} be left out of the recall",
                         "q": "is {E} left out of the recall", "negc": "{E} is included in the recall",
                         "negpres": "{E} is not part of the recall", "vn": "not included in the recall", "rv": "NOT RECALLED"}},
         field="Recall status", topic="whether {E} is included in the recall",
         sources=[S("food safety agency recall notice", "food safety agency recall notices", True, "formal", "notice"),
                  S("manufacturer statement", "manufacturer statements", True, "formal", "statement"),
                  S("supermarket customer email", "supermarket customer emails", False, "formal", "email"),
                  S("social media post", "social media posts", False, "casual", "post")],
         other=["The recall concerns possible undeclared sesame in some batches.",
                "Customers can return affected products for a full refund without a receipt.",
                "The best-before dates of the recalled batches run to next spring."],
         filler=["We apologise to our customers.", "No illnesses have been reported.", "Check the lot code on the base of the pack."]),
    dict(key="claim_status", gran="day", vtype="cat", event=False, allow=("stmt", "neg", "corr", "retr"),
         ent=ent_claim, vals=pick(["approved", "denied", "on hold pending documents", "under review"]),
         noun="the status of {E}", vn="{V}", rv="{V}", field="Claim status", topic="the status of {E}",
         pres="{E} is {V}", base="{E} {AUX} be {V}", q="is {E} {V}", negc="{E} is not {V}",
         sources=[S("insurer decision letter", "insurer decision letters", True, "formal", "letter"),
                  S("online claims portal", "online claims portal entries", True, "record", "portal entry", "portal entry"),
                  S("broker email", "broker emails", False, "formal", "email"),
                  S("call-centre phone call", "call-centre phone calls", False, "call", "call")],
         other=["The excess on the policy behind {E} is 250.", "Your policy renews in the autumn.",
                "Payments for approved claims are usually made within ten working days."],
         filler=["Please quote your claim number in any reply.", "Thank you for your patience.", "Kind regards."]),
    dict(key="parcel", gran="min", vtype="cat", event=False, allow=("stmt", "neg", "corr", "retr"),
         ent=ent_parcel, vals=pick(["transit", "ofd", "depot", "neighbour", "customs"]),
         pervalue={
             "transit": {"pres": "{E} is in transit", "base": "{E} {AUX} be in transit", "q": "is {E} in transit",
                         "negc": "{E} is not in transit", "vn": "in transit", "rv": "IN TRANSIT"},
             "ofd": {"pres": "{E} is out for delivery", "base": "{E} {AUX} be out for delivery",
                     "q": "is {E} out for delivery", "negc": "{E} is not out for delivery", "vn": "out for delivery",
                     "rv": "OUT FOR DELIVERY"},
             "depot": {"pres": "{E} is being held at the local depot", "base": "{E} {AUX} be held at the local depot",
                       "q": "is {E} being held at the local depot", "negc": "{E} is not being held at the local depot",
                       "vn": "held at the local depot", "rv": "HELD AT DEPOT"},
             "neighbour": {"pres": "{E} has been delivered to a neighbour", "base": "{E} {AUX} have been delivered to a neighbour",
                           "q": "has {E} been delivered to a neighbour", "negc": "{E} has not been delivered to a neighbour",
                           "vn": "delivered to a neighbour", "rv": "DELIVERED TO NEIGHBOUR"},
             "customs": {"pres": "{E} is awaiting customs clearance", "base": "{E} {AUX} be awaiting customs clearance",
                         "q": "is {E} awaiting customs clearance", "negc": "{E} is not awaiting customs clearance",
                         "vn": "awaiting customs clearance", "rv": "AWAITING CUSTOMS"}},
         noun="the tracking status of {E}", field="Tracking status", topic="the tracking status of {E}",
         sources=[S("carrier tracking page", "carrier tracking page entries", True, "record", "tracking entry"),
                  S("carrier customer-service call", "carrier customer-service calls", True, "call", "call"),
                  S("seller email", "seller emails", False, "formal", "email"),
                  S("message from a housemate", "messages from housemates", False, "casual", "message")],
         other=["The seller has offered a 10% discount code for the delay.", "{E} weighs 2.4 kg according to the label.",
                "A signature is not required for {E}."],
         filler=["Thanks for shopping with us.", "Tracking updates can take a few hours to appear."]),
    dict(key="school", gran="min", vtype="bin", event=True, allow=("stmt", "corr", "retr"),
         ent=ent_school, vals=lambda rng: ["open", "closed"],
         pervalue={
             "open": {"pres": "{E} is open on {EV}", "base": "{E} {AUX} be open on {EV}", "q": "is {E} open on {EV}",
                      "negc": "{E} is not open on {EV}", "negpres": "{E} is not closing on {EV}", "vn": "open", "rv": "OPEN"},
             "closed": {"pres": "{E} is closed on {EV}", "base": "{E} {AUX} be closed on {EV}", "q": "is {E} closed on {EV}",
                        "negc": "{E} is not closed on {EV}", "negpres": "{E} will not open on {EV}", "vn": "closed", "rv": "CLOSED"}},
         field="Status", topic="whether {E} is open on {EV}",
         sources=[S("school district closure notice", "school district closure notices", True, "formal", "notice"),
                  S("school text alert", "school text alerts", True, "casual", "text alert", "alert"),
                  S("local TV news website", "local TV news website reports", False, "formal", "report"),
                  S("parents' group chat message", "parents' group chat messages", False, "casual", "message")],
         other=["After-school clubs at {E} are cancelled for the rest of the week.", "Buses to {E} may run late because of ice.",
                "The {E} parents' evening has moved to next month."],
         filler=["Stay safe and keep warm.", "Please check back for updates.", "Thank you, families."]),
    dict(key="venue", gran="day", vtype="cat", event=False, allow=ALLOW_ALL,
         ent=ent_workshop, vals=pick(["Hall A", "Hall C", "Room 204", "Room 311", "the Linden Lecture Theatre", "the Atrium",
                                     "the Harbour Room"]),
         noun="the venue for {E} sessions", vn="{V}", rv="{V}", field="Venue", topic="the venue for {E} sessions",
         pres="{E} sessions take place in {V}", base="{E} sessions {AUX} take place in {V}",
         q="do {E} sessions take place in {V}", negc="{E} sessions do not take place in {V}",
         sources=[S("organiser email", "organiser emails", True, "formal", "email"),
                  S("event website", "event website updates", True, "formal", "website update", "update"),
                  S("printed programme", "printed programmes", False, "record", "programme"),
                  S("attendee chat message", "attendee chat messages", False, "casual", "message")],
         other=["Lunch for {E} is served in the foyer.", "Name badges for {E} can be collected from reception.",
                "The dinner for {E} starts at 7 p.m."],
         filler=["We look forward to seeing you.", "Wi-Fi details are on your badge.", "Best wishes, the organising team."]),
    dict(key="appointment", gran="day", vtype="num", numkind="time", event=True, allow=("stmt", "neg", "corr", "retr"),
         ent=ent_appt, vals=times(8 * 60, 17 * 60, 15),
         noun="the time of {E}", vn="{V}", rv="{V}", field="Appointment time", topic="the time of {E}",
         pres="{E} is at {V}", base="{E} {AUX} be at {V}", q="is {E} at {V}", negc="{E} is not at {V}",
         cmp="{E} is {C} {V}", q_cmp="is {E} {C} {V}", ops=TIMECMP,
         sources=[S("clinic booking system", "clinic booking system entries", True, "record", "booking entry", "booking"),
                  S("clinic reminder text", "clinic reminder texts", True, "casual", "reminder text", "reminder"),
                  S("receptionist phone call", "receptionist phone calls", True, "call", "call"),
                  S("family member's message", "family members' messages", False, "casual", "message")],
         other=["Please arrive ten minutes early for {E}.", "Parking at the clinic is free for patients.",
                "Bring a list of current medicines to {E}."],
         filler=["Reply STOP to opt out of reminders.", "To cancel, call the clinic at least 24 hours ahead."]),
    dict(key="rent", gran="day", vtype="num", numkind="money", event=False, allow=ALLOW_ALL,
         ent=ent_flat, vals=money(120000, 165000, 2500),
         noun="the monthly rent for {E}", vn="{V}", rv="{V}", field="Monthly rent", topic="the monthly rent for {E}",
         pres="the monthly rent for {E} is {V}", base="the monthly rent for {E} {AUX} be {V}",
         q="is the monthly rent for {E} {V}", negc="the monthly rent for {E} is not {V}",
         cmp="the monthly rent for {E} is {C} {V}", q_cmp="is the monthly rent for {E} {C} {V}", ops=AMTCMP,
         sources=[S("signed lease addendum", "signed lease addenda", True, "formal", "addendum"),
                  S("landlord email", "landlord emails", True, "formal", "email"),
                  S("letting agent listing", "letting agent listings", False, "record", "listing"),
                  S("flatmate message", "flatmate messages", False, "casual", "message")],
         other=["The deposit for {E} is held in a protection scheme.", "Bins for {E} are collected on Tuesdays.",
                "The boiler at {E} will be serviced next month."],
         filler=["Let me know if you have any questions.", "Best regards.", "Thanks!"]),
    dict(key="software", gran="day", vtype="bin", event=False, allow=("stmt", "sched", "corr", "retr"),
         ent=ent_software, vals=lambda rng: ["supported", "unsupported"],
         pervalue={
             "supported": {"pres": "{E} is supported", "base": "{E} {AUX} be supported", "q": "is {E} supported",
                           "negc": "{E} is not supported", "negpres": "{E} has not reached end of support",
                           "vn": "supported", "rv": "SUPPORTED"},
             "unsupported": {"pres": "{E} is out of support", "base": "{E} {AUX} be out of support",
                             "q": "is {E} out of support", "negc": "{E} is not out of support",
                             "negpres": "{E} is no longer supported", "vn": "out of support", "rv": "END OF SUPPORT"}},
         field="Support status", topic="whether {E} is supported",
         sources=[S("vendor lifecycle page", "vendor lifecycle page updates", True, "record", "lifecycle update", "lifecycle page update"),
                  S("vendor release notes", "vendor release notes", True, "formal", "release notes"),
                  S("reseller newsletter", "reseller newsletters", False, "formal", "newsletter"),
                  S("user forum post", "user forum posts", False, "casual", "post")],
         other=["A security patch for {E} was published last week.", "{E} now supports single sign-on.",
                "The installer for {E} is 1.2 GB."],
         filler=["Plan your upgrades early.", "See the documentation for details.", "Thank you for being a customer."]),
    dict(key="grant", gran="day", vtype="num", numkind="date", event=False, allow=("stmt", "neg", "corr", "retr"),
         ent=ent_grant, vals=offs_dates(),
         noun="the application deadline for {E}", vn="{V}", rv="{V}", field="Deadline",
         topic="the application deadline for {E}",
         pres="the application deadline for {E} is {V}", base="the application deadline for {E} {AUX} be {V}",
         q="is the application deadline for {E} {V}", negc="the application deadline for {E} is not {V}",
         cmp="the application deadline for {E} is {C} {V}", q_cmp="is the application deadline for {E} {C} {V}",
         ops=DATECMP,
         sources=[S("funder's call page", "funder's call page updates", True, "formal", "call page update", "update"),
                  S("funder email to applicants", "funder emails to applicants", True, "formal", "email"),
                  S("research office newsletter", "research office newsletters", False, "formal", "newsletter"),
                  S("colleague's message", "colleagues' messages", False, "casual", "message")],
         other=["Applicants to {E} may request up to 5,000.", "A webinar about {E} will be held next week.",
                "Budgets for {E} must include a short justification."],
         filler=["Good luck with your application.", "Contact the programme officer with questions."]),
    dict(key="boil_water", gran="day", vtype="bin", event=False, allow=("stmt", "sched", "temp", "corr", "retr"),
         temp_vals=["advisory"],
         ent=ent_district, vals=lambda rng: ["advisory", "none"],
         pervalue={
             "advisory": {"pres": "a boil-water advisory is in effect for {E}", "base": "a boil-water advisory {AUX} be in effect for {E}",
                          "q": "is a boil-water advisory in effect for {E}", "negc": "no boil-water advisory is in effect for {E}",
                          "negpres": "tap water in {E} is not safe to drink without boiling", "vn": "in effect", "rv": "BOIL WATER ADVISORY"},
             "none": {"pres": "no boil-water advisory is in effect for {E}", "base": "tap water in {E} {AUX} be safe to drink without boiling",
                      "q": "is tap water in {E} safe to drink without boiling", "negc": "a boil-water advisory is in effect for {E}",
                      "negpres": "residents of {E} do not need to boil their tap water", "vn": "not in effect", "rv": "NO ADVISORY"}},
         field="Boil-water advisory", topic="whether a boil-water advisory is in effect for {E}",
         sources=[S("water utility notice", "water utility notices", True, "formal", "notice"),
                  S("city health department update", "city health department updates", True, "formal", "update"),
                  S("local news site report", "local news site reports", False, "formal", "report"),
                  S("neighbourhood forum post", "neighbourhood forum posts", False, "casual", "post")],
         other=["Water pressure in {E} may be low overnight.", "Hydrant flushing in {E} is planned for the spring.",
                "Water bills for {E} are now issued quarterly."],
         filler=["Thank you for your patience.", "Bottled water is available at the library.", "Updates will follow."]),
    dict(key="kickoff", gran="day", vtype="num", numkind="time", event=True, allow=("stmt", "neg", "corr", "retr"),
         ent=ent_match, vals=times(12 * 60, 20 * 60, 15),
         noun="the kick-off time of {E}", vn="{V}", rv="{V}", field="Kick-off", topic="the kick-off time of {E}",
         pres="{E} kicks off at {V}", base="{E} {AUX} kick off at {V}", q="does {E} kick off at {V}",
         negc="{E} does not kick off at {V}", cmp="{E} kicks off {C} {V}", q_cmp="does {E} kick off {C} {V}", ops=TIMECMP,
         sources=[S("league fixtures page", "league fixtures page updates", True, "record", "fixtures update", "fixtures update"),
                  S("home club website", "home club website posts", True, "formal", "website post", "post"),
                  S("ticketing email", "ticketing emails", True, "formal", "email"),
                  S("fan forum post", "fan forum posts", False, "casual", "post")],
         other=["Tickets for {E} are almost sold out.", "{E} will be shown live on local television.",
                "Away fans for {E} should use the north entrance."],
         filler=["Enjoy the game.", "Gates open 90 minutes before kick-off."]),
    dict(key="train_platform", gran="min", vtype="cat", event=True, allow=("stmt", "neg", "corr", "retr"),
         ent=ent_train, vals=pick([str(i) for i in range(1, 13)]),
         noun="the departure platform for {E}", vn="platform {V}", rv="{V}", field="Platform",
         topic="the departure platform for {E}",
         pres="{E} departs from platform {V}", base="{E} {AUX} depart from platform {V}",
         q="does {E} depart from platform {V}", negc="{E} does not depart from platform {V}",
         sources=[S("station departure board", "station departure board updates", True, "record", "board update"),
                  S("rail operator app", "rail operator app updates", True, "record", "app update"),
                  S("station announcement", "station announcements", True, "spoken", "announcement"),
                  S("fellow passenger", "fellow passengers", False, "casual", "remark")],
         other=["{E} is formed of eight coaches today.", "The first-class section of {E} is at the front.",
                "Refreshments are not available on {E}."],
         filler=["Please mind the gap.", "Thank you for travelling with us."]),
    dict(key="library", gran="day", vtype="num", numkind="date", event=False, allow=("stmt", "neg", "corr", "retr"),
         ent=ent_loan, vals=offs_dates(),
         noun="the due date for {E}", vn="{V}", rv="{V}", field="Due date", topic="the due date for {E}",
         pres="{E} is due back on {V}", base="{E} {AUX} be due back on {V}", q="is {E} due back on {V}",
         negc="{E} is not due back on {V}", cmp="{E} is due back {C} {V}", q_cmp="is {E} due back {C} {V}", ops=DATECMP,
         sources=[S("library account page", "library account page entries", True, "record", "account entry"),
                  S("library reminder email", "library reminder emails", True, "formal", "email"),
                  S("date-due receipt", "date-due receipts", False, "record", "receipt"),
                  S("friend's message", "friends' messages", False, "casual", "message")],
         other=["You have two reservations waiting for collection.", "The library will be closed on the public holiday.",
                "Overdue fines for adult books are 25 cents a day."],
         filler=["Happy reading!", "Renew online at any time."]),
    dict(key="exhibit", gran="day", vtype="bin", event=False, allow=("stmt", "sched", "temp", "corr", "retr"),
         temp_vals=["closed"],
         ent=ent_exhibit, vals=lambda rng: ["open", "closed"],
         pervalue={
             "open": {"pres": "{E} is open to visitors", "base": "{E} {AUX} be open to visitors",
                      "q": "is {E} open to visitors", "negc": "{E} is not open to visitors",
                      "negpres": "{E} is not closed to visitors", "vn": "open to visitors", "rv": "OPEN"},
             "closed": {"pres": "{E} is closed to visitors", "base": "{E} {AUX} be closed to visitors",
                        "q": "is {E} closed to visitors", "negc": "{E} is not closed to visitors",
                        "negpres": "{E} is not open to visitors", "vn": "closed to visitors", "rv": "CLOSED"}},
         field="Status", topic="whether {E} is open to visitors",
         sources=[S("museum website", "museum website updates", True, "formal", "website update", "update"),
                  S("museum newsletter", "museum newsletters", True, "formal", "newsletter"),
                  S("travel guidebook", "travel guidebooks", False, "record", "guidebook entry", "entry"),
                  S("visitor review", "visitor reviews", False, "casual", "review")],
         other=["The museum café has new opening hours.", "Guided tours of {E} run on Saturdays.",
                "Photography without flash is allowed in {E}."],
         filler=["We look forward to welcoming you.", "Entry to the permanent collection is free."]),
    dict(key="scholarship", gran="day", vtype="num", numkind="money", event=False, allow=("stmt", "neg", "sched", "corr", "retr"),
         ent=ent_scholar, vals=money(250000, 600000, 50000),
         noun="the yearly value of {E}", vn="{V}", rv="{V}", field="Award per year", topic="the yearly value of {E}",
         pres="{E} is worth {V} a year", base="{E} {AUX} be worth {V} a year", q="is {E} worth {V} a year",
         negc="{E} is not worth {V} a year", cmp="{E} is worth {C} {V} a year", q_cmp="is {E} worth {C} {V} a year",
         ops=AMTCMP,
         sources=[S("award letter", "award letters", True, "formal", "letter"),
                  S("financial aid portal", "financial aid portal entries", True, "record", "portal entry"),
                  S("department administrator email", "department administrator emails", False, "formal", "email"),
                  S("student forum post", "student forum posts", False, "casual", "post")],
         other=["Recipients of awards like {E} must submit a short report each year.",
                "The award ceremony is in the spring.", "Payments are made at the start of each term."],
         filler=["Congratulations again.", "Please keep this message for your records."]),
    dict(key="permit", gran="day", vtype="cat", event=False, allow=("stmt", "neg", "corr", "retr"),
         ent=ent_permit, vals=pick(["approved", "under review", "refused", "on hold"]),
         noun="the status of {E}", vn="{V}", rv="{V}", field="Permit status", topic="the status of {E}",
         pres="{E} is {V}", base="{E} {AUX} be {V}", q="is {E} {V}", negc="{E} is not {V}",
         sources=[S("city permit database", "city permit database entries", True, "record", "database entry", "entry"),
                  S("planning officer letter", "planning officer letters", True, "formal", "letter"),
                  S("contractor email", "contractor emails", False, "formal", "email"),
                  S("neighbour's message", "neighbours' messages", False, "casual", "message")],
         other=["The site notice for {E} must stay up for 21 days.", "Inspections under {E} are booked online.",
                "Fees for {E} were paid in full."],
         filler=["Regards.", "Please contact the planning desk with questions."]),
    dict(key="polling", gran="day", vtype="cat", event=False, allow=("stmt", "neg", "sched", "corr", "retr"),
         ent=ent_precinct, vals=pick(["Linden Community Centre", "Ashby Library", "St Anne's Church Hall", "Carrow Fire Station",
                                     "the Millbrook Elementary gym", "Kestrel Road Scout Hut"]),
         noun="the polling place for {E}", vn="{V}", rv="{V}", field="Polling place", topic="the polling place for {E}",
         pres="voters in {E} vote at {V}", base="voters in {E} {AUX} vote at {V}", q="do voters in {E} vote at {V}",
         negc="voters in {E} do not vote at {V}",
         sources=[S("county election office notice", "county election office notices", True, "formal", "notice"),
                  S("sample ballot mailer", "sample ballot mailers", True, "record", "mailer"),
                  S("campaign flyer", "campaign flyers", False, "formal", "flyer"),
                  S("neighbour's post", "neighbours' posts", False, "casual", "post")],
         other=["Early voting opens two weeks before election day.", "Voters in {E} can request a mail ballot online.",
                "Bring photo ID if you are voting for the first time."],
         filler=["Every vote counts.", "Polls are open 7 a.m. to 8 p.m."]),
    dict(key="savings", gran="day", vtype="num", numkind="pct", event=False, allow=("stmt", "neg", "sched", "corr", "retr"),
         ent=ent_account, vals=money(185, 340, 15),
         noun="the interest rate on {E}", vn="{V}", rv="{V}", field="Interest rate (AER)", topic="the interest rate on {E}",
         pres="the interest rate on {E} is {V}", base="the interest rate on {E} {AUX} be {V}",
         q="is the interest rate on {E} {V}", negc="the interest rate on {E} is not {V}",
         cmp="the interest rate on {E} is {C} {V}", q_cmp="is the interest rate on {E} {C} {V}", ops=AMTCMP,
         sources=[S("bank rate-change notice", "bank rate-change notices", True, "formal", "notice"),
                  S("account statement", "account statements", True, "record", "statement"),
                  S("comparison website", "comparison website listings", False, "record", "listing"),
                  S("newspaper article", "newspaper articles", False, "formal", "article")],
         other=["{E} allows up to four withdrawals a year.", "Interest on {E} is paid monthly.",
                "The minimum deposit for {E} is 1."],
         filler=["Thank you for banking with us.", "Rates are variable."]),
    dict(key="carryover", gran="day", vtype="num", numkind="days", event=False, allow=("stmt", "neg", "sched", "corr", "retr"),
         ent=ent_office, vals=times(2, 12, 1),
         noun="the carry-over limit for unused annual leave at {E}", vn="{V}", rv="{V}", field="Leave carry-over limit",
         topic="the carry-over limit for unused annual leave at {E}",
         pres="the carry-over limit for unused annual leave at {E} is {V}",
         base="the carry-over limit for unused annual leave at {E} {AUX} be {V}",
         q="is the carry-over limit for unused annual leave at {E} {V}",
         negc="the carry-over limit for unused annual leave at {E} is not {V}",
         cmp="the carry-over limit for unused annual leave at {E} is {C} {V}",
         q_cmp="is the carry-over limit for unused annual leave at {E} {C} {V}", ops=AMTCMP,
         sources=[S("HR policy portal", "HR policy portal updates", True, "record", "portal update", "policy update"),
                  S("HR director email", "HR director emails", True, "formal", "email"),
                  S("line manager message", "line manager messages", False, "casual", "message"),
                  S("colleague chat message", "colleague chat messages", False, "casual", "message")],
         other=["Staff at {E} get two volunteering days a year.", "Payslips at {E} are now issued online.",
                "The summer social for {E} is on the last Friday of June."],
         filler=["Thanks, everyone.", "Any questions, just ask."]),
    dict(key="ferry", gran="min", vtype="bin", event=True, allow=("stmt", "corr", "retr"),
         ent=ent_sailing, vals=lambda rng: ["running", "cancelled"],
         pervalue={
             "running": {"pres": "{E} is running today", "base": "{E} {AUX} run today", "q": "is {E} running today",
                         "negc": "{E} is not running today", "negpres": "{E} is not cancelled today", "vn": "running",
                         "rv": "RUNNING"},
             "cancelled": {"pres": "{E} is cancelled today", "base": "{E} {AUX} be cancelled today",
                           "q": "is {E} cancelled today", "negc": "{E} is not cancelled today",
                           "negpres": "{E} will not run today", "vn": "cancelled", "rv": "CANCELLED"}},
         field="Status", topic="whether {E} is running today",
         sources=[S("ferry operator service update", "ferry operator service updates", True, "formal", "service update", "update"),
                  S("port information screen", "port information screens", True, "record", "screen update"),
                  S("local radio bulletin", "local radio bulletins", False, "spoken", "bulletin"),
                  S("passenger forum post", "passenger forum posts", False, "casual", "post")],
         other=["Vehicle bookings for {E} are full.", "The café on {E} is card-only.", "Dogs on {E} must stay on the car deck."],
         filler=["Safe travels.", "Check back before you leave home."]),
    dict(key="lab", gran="day", vtype="cat", event=False, allow=("stmt", "neg", "corr", "retr"), noun_ok=False,
         ent=ent_sample, vals=pick(["within the reference range", "above the reference range", "below the reference range"], 3, 3),
         noun="the flag on {E}", vn="{V}", rv="{V}", field="Flag", topic="the flag on {E}",
         pres="{E} is {V}", base="{E} {AUX} be {V}", q="is {E} {V}", negc="{E} is not {V}",
         sources=[S("laboratory report", "laboratory reports", True, "formal", "report"),
                  S("patient portal summary", "patient portal summaries", True, "record", "summary"),
                  S("clinic nurse's phone message", "clinic nurses' phone messages", True, "call", "message"),
                  S("family member's text", "family members' texts", False, "casual", "text")],
         other=["The sample for {E} was taken in the morning.", "A repeat test may be offered at the next visit.",
                "The laboratory's opening hours have changed."],
         filler=["Please discuss results with your clinician.", "This report was checked by laboratory staff."]),
    dict(key="player", gran="day", vtype="cat", event=False, allow=("stmt", "neg", "temp", "corr", "retr"), noun_ok=False,
         temp_vals=["suspended"],
         ent=ent_player, vals=pick(["available for selection", "injured", "suspended"], 3, 3),
         noun="the availability of {E}", vn="{V}", rv="{V}", field="Squad status", topic="the availability of {E}",
         pres="{E} is {V}", base="{E} {AUX} be {V}", q="is {E} {V}", negc="{E} is not {V}",
         sources=[S("club injury update", "club injury updates", True, "formal", "update"),
                  S("manager's press conference", "manager's press conferences", True, "spoken", "press conference"),
                  S("sports news report", "sports news reports", False, "formal", "report"),
                  S("fan account post", "fan account posts", False, "casual", "post")],
         other=["{E} signed a new two-year contract.", "{E} scored twice in the last friendly.",
                "{E} will wear the number 8 shirt this season."],
         filler=["Up the club!", "More news to follow."]),
    dict(key="price", gran="day", vtype="num", numkind="money", event=False, allow=ALLOW_ALL,
         ent=ent_goods, vals=money(249, 899, 25),
         noun="the shelf price of {E}", vn="{V}", rv="{V}", field="Price", topic="the shelf price of {E}",
         pres="{E} costs {V}", base="{E} {AUX} cost {V}", q="does {E} cost {V}", negc="{E} does not cost {V}",
         cmp="{E} costs {C} {V}", q_cmp="does {E} cost {C} {V}", ops=AMTCMP,
         sources=[S("store's online price list", "store's online price list entries", True, "record", "price list entry", "price list entry"),
                  S("in-store shelf label", "in-store shelf labels", True, "record", "shelf label"),
                  S("weekly flyer", "weekly flyers", False, "formal", "flyer"),
                  S("customer review", "customer reviews", False, "casual", "review")],
         other=["Loyalty members earn double points at the store this month.", "The store now opens at 7 a.m. on Sundays.",
                "Self-checkout tills have been added at the store."],
         filler=["Prices include tax.", "While stocks last."]),
    dict(key="speed", gran="day", vtype="num", numkind="speed", event=False, allow=ALLOW_ALL,
         ent=ent_road, vals=lambda rng: sorted(rng.sample([20, 30, 40, 50], rng.randint(3, 4))),
         noun="the speed limit on {E}", vn="{V}", rv="{V}", field="Speed limit", topic="the speed limit on {E}",
         pres="the speed limit on {E} is {V}", base="the speed limit on {E} {AUX} be {V}",
         q="is the speed limit on {E} {V}", negc="the speed limit on {E} is not {V}",
         cmp="the speed limit on {E} is {C} {V}", q_cmp="is the speed limit on {E} {C} {V}", ops=AMTCMP,
         sources=[S("council traffic order", "council traffic orders", True, "formal", "traffic order", "order"),
                  S("road sign photo", "road sign photos", True, "record", "photo"),
                  S("local news report", "local news reports", False, "formal", "report"),
                  S("drivers' forum post", "drivers' forum posts", False, "casual", "post")],
         other=["Parking bays on {E} are being repainted.", "A new pedestrian crossing is planned on {E}.",
                "Bin lorries use {E} on Monday mornings."],
         filler=["Drive safely.", "Enforcement cameras are in use."]),
    dict(key="pharmacy", gran="min", vtype="cat", event=False, allow=("stmt", "neg", "corr", "retr"),
         ent=ent_rx, vals=pick(["ready for collection", "being prepared", "waiting for stock"], 3, 3),
         noun="the status of {E}", vn="{V}", rv="{V}", field="Status", topic="the status of {E}",
         pres="{E} is {V}", base="{E} {AUX} be {V}", q="is {E} {V}", negc="{E} is not {V}",
         sources=[S("pharmacy system record", "pharmacy system records", True, "record", "record entry", "entry"),
                  S("pharmacy text alert", "pharmacy text alerts", True, "casual", "text alert", "alert"),
                  S("pharmacy assistant phone call", "pharmacy assistant phone calls", True, "call", "call"),
                  S("family member's message", "family members' messages", False, "casual", "message")],
         other=["The pharmacy closes at 6 p.m. on Saturdays.", "Bring photo ID when collecting {E}.",
                "{E} has two repeats left."],
         filler=["Thank you.", "Reply HELP for assistance."]),
    dict(key="returns", gran="day", vtype="num", numkind="days", event=False, allow=("stmt", "neg", "sched", "corr", "retr"),
         ent=ent_shop, vals=lambda rng: sorted(rng.sample([14, 21, 28, 30, 45, 60], rng.randint(3, 4))),
         noun="the return window for {E}", vn="{V}", rv="{V}", field="Return window", topic="the return window for {E}",
         pres="the return window for {E} is {V}", base="the return window for {E} {AUX} be {V}",
         q="is the return window for {E} {V}", negc="the return window for {E} is not {V}",
         cmp="the return window for {E} is {C} {V}", q_cmp="is the return window for {E} {C} {V}", ops=AMTCMP,
         sources=[S("returns policy page", "returns policy page updates", True, "formal", "policy update", "update"),
                  S("order confirmation email", "order confirmation emails", True, "formal", "email"),
                  S("customer service call", "customer service calls", False, "call", "call"),
                  S("customer review", "customer reviews", False, "casual", "review")],
         other=["Returned items must be unused and in their original packaging.", "Refunds go back to the original payment method.",
                "Gift cards cannot be returned."],
         filler=["Thanks for shopping with us.", "We are here to help."]),
]

DOM = {d["key"]: d for d in DOMAINS}
for _d in DOMAINS:
    assert all(k in _d for k in ("key", "gran", "vtype", "event", "allow", "ent", "vals", "field", "topic", "sources")), _d["key"]
    if _d["vtype"] in ("cat", "num") and "pervalue" not in _d:
        assert all(k in _d for k in ("pres", "base", "q", "negc", "noun", "vn")), _d["key"]
    if _d["vtype"] == "num":
        assert "cmp" in _d and "ops" in _d and "numkind" in _d, _d["key"]
    if _d["vtype"] == "bin":
        assert "neg" not in _d["allow"], _d["key"]
    if _d["event"]:
        assert "sched" not in _d["allow"] and "temp" not in _d["allow"], _d["key"]
    if _d["gran"] == "min":
        assert "temp" not in _d["allow"], _d["key"]
