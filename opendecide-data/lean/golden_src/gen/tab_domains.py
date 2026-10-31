"""Domains for gen_tables: realistic table builders (Claude-written vocabularies and value ranges) and the
rule-based ('special') claim operations that read notes under a table (discounts, exceptions, bands, fees, caps,
time zones, tie-breaks, weekday/weekend rates, series trends).

All names of shops, towns, clubs, people, products, carriers and medicines are invented or generic; numbers are
random within realistic ranges. Nothing here is a real record.
"""
import datetime as dt
from fractions import Fraction as Fr

from tab_core import (INF, MON3, MONTHS, NUMW, WEEKDAYS, Col, Ent, Table, VP, art, cap, fixed, fmt_date, fmt_time,
                      min_words, od, ordn, ordw, trim_dec)
from tab_ops import (F, N, T, NUMERIC, Op, ch, holds, is_int, k3, poss)

# ------------------------------------------------------------------------------------------------ vocabularies
FIRST = ["Amara", "Bilal", "Chen", "Daniela", "Emeka", "Farah", "Gustavo", "Hana", "Ibrahim", "Jolene", "Kenji",
         "Leilani", "Mateo", "Nadia", "Oluwaseun", "Priya", "Quentin", "Rosa", "Sipho", "Tamar", "Umar", "Valentina",
         "Wojtek", "Ximena", "Yusuf", "Zanele", "Aarav", "Brigid", "Carlos", "Dilnoza", "Eero", "Fatima", "Giorgos",
         "Halima", "Isaac", "Jia", "Kwame", "Lucia", "Marcus", "Noor", "Oskar", "Paloma", "Rahul", "Svetlana",
         "Tomasz", "Uzma", "Viktor", "Wren", "Yara", "Zeke", "Alex", "Sam", "Jordan", "Riley", "Aiyana", "Bongani",
         "Celine", "Dmitri", "Esperanza", "Finn", "Grace", "Hamza", "Ingrid", "Javier", "Keiko", "Liam", "Mei",
         "Nikolai", "Olga", "Pedro", "Rania", "Stefan", "Thandiwe", "Tariq", "Ulla", "Vikram", "Winifred", "Xavier",
         "Yetunde", "Zoltan", "Anika", "Benedikt", "Chiara", "Deshawn", "Elif", "Felipe", "Gulnara", "Hiroshi",
         "Imani", "Jakob", "Maya", "Omar", "Sofia", "Ethan", "Lena", "Arjun", "Nora", "Theo", "Ines", "Kofi", "Mira",
         "Luca", "Ada", "Bruno", "Clara", "Dev", "Eva", "Femi", "Gita", "Hugo", "Iris", "Jonas", "Kira", "Leon"]
LAST = ["Okafor", "Haddad", "Nakamura", "Silva", "Kowalski", "Mensah", "Novak", "Rossi", "Petrov", "Kim", "Garcia",
        "Nguyen", "O'Brien", "Schmidt", "Dubois", "Andersson", "Costa", "Yilmaz", "Ivanova", "Mbeki", "Chowdhury",
        "Tanaka", "Fernandes", "Larsen", "Moreau", "Zhang", "Kaur", "Adeyemi", "Horvath", "Lindqvist", "Mwangi",
        "Rahman", "Sato", "Vargas", "Walsh", "Abara", "Bauer", "Castillo", "Dimitriou", "Eriksen", "Fischer",
        "Gonzalez", "Hughes", "Ito", "Jensen", "Khan", "Lopez", "Murphy", "Nilsson", "Owusu", "Patel", "Quinn",
        "Reyes", "Santos", "Torres", "Usman", "Varga", "Weber", "Xu", "Young", "Zeller", "Achebe", "Brennan", "Cruz",
        "Dahl", "Esposito", "Farouk", "Gallagher", "Hassan", "Iqbal", "Jovanovic", "Kariuki", "Lund", "Mahlangu",
        "Nowak", "Ortiz", "Park", "Romero", "Sherpa", "Tran", "Ueda", "Volkov", "Whitaker", "Yamamoto", "Zulu",
        "Alvarez", "Banerjee", "Coleman", "Delgado", "Ekstrom", "Fitzgerald", "Grant", "Holm", "Ibarra", "Joshi"]
TOWNS = ["Ashbourne Vale", "Brookvale", "Carrowmore", "Dunmere", "Elmstead Cross", "Fenwick Bay", "Glenhaven",
         "Harrowby", "Ivybrook", "Kestrel Bay", "Larkfield", "Millbrook", "Northcote Hill", "Oakhurst", "Pinehurst",
         "Queensholm", "Ravenscar Point", "Stonebridge", "Thornbury Green", "Upfield", "Valemount", "Westmere",
         "Yarrowdale", "Amberley Heath", "Beckford Mill", "Cranmore", "Denholm", "Eastwick Down", "Fairhaven",
         "Greystone", "Hollingbrook", "Ingleby Cross", "Kingsbridge Moor", "Lowmoor", "Marlow Heath", "Newhaven Quay",
         "Oldbury Fields", "Penrose", "Redwater", "Silverdale", "Tidewell", "Underhill", "Wyndham Park", "Alderley",
         "Bramwell", "Castleton Rise", "Dovercourt", "Eldon", "Foxhollow", "Gorsey Bank", "Hartfield", "Kilnsey",
         "Linton Ferry", "Mossley Vale", "Netherby", "Otterburn", "Pellham", "Ridgeway", "Summerlea", "Tarnwick",
         "Wickham Down", "Yewbridge", "Arden Lea", "Blackwater", "Coldharbour", "Deepdale", "Everton Rise",
         "Fordham Cross", "Glenbrook", "Heathcote", "Kirkwall Bay", "Loxley", "Moorfield", "Norbury Mill"]
STREETS = ["Harbor Street", "Maple Avenue", "Riverside", "Old Town", "Westgate", "Northfield", "Eastbrook",
           "Kings Road", "Market Square", "Station Road", "Hillcrest", "Lakeside", "Parkview", "Mill Lane", "Elm Grove",
           "Bridgewater", "Canal Street", "Southpoint", "Highbury", "Cedar Park", "Queensway", "Victoria Road",
           "Orchard Lane", "Fairview", "Stonegate", "Clearwater", "Oakridge", "Pine Hill", "Seaview", "Meadowbank",
           "Ashby Road", "Chapel Street", "Greenway", "Brookside", "Castle Hill", "Longford", "Redhill", "Willow Bank",
           "Airport Retail Park", "Central Mall", "University Quarter", "Dockside", "Beacon Hill", "Cherry Tree",
           "Foxley", "Glenwood", "Hawthorn", "Ivy Lane", "Juniper Court", "Kingsmead", "Linden", "Marlowe",
           "Newbridge", "Oldfield", "Priory", "Quarry Bank", "Rosehill", "Sandgate", "Thornfield", "Upton Park",
           "Vale Road", "Wharf Street", "Yew Tree", "Abbey Road", "Bell Street", "Corn Exchange", "Drapers Lane"]
RETAIL_COS = ["Northwind Outfitters", "Brightleaf Grocers", "Copperline Hardware", "Bluebird Books",
              "Evergreen Pharmacy", "Summit Sports", "Tidewater Home", "Juniper Coffee", "Kestrel Electronics",
              "Larkspur Garden Centre", "Meridian Pet Supplies", "Oakhurst Furniture", "Harbourlight Bakery",
              "Pinecrest Toys", "Silverline Opticians", "Cobalt Cycles"]
PERIODS = ["Q1 2025", "Q2 2025", "Q3 2024", "Q4 2024", "March 2025", "October 2024", "the week of 6 October 2025",
           "the 2024 financial year", "January 2026", "the first half of 2025"]
REGIONS = ["North", "South", "East", "West", "Central"]
PRODUCTS = [  # (name, price lo, price hi in dollars, weight lo, weight hi in kg)
    ("Oak dining table", 299, 899, 25, 45), ("Pine bookcase", 89, 249, 18, 32), ("Office chair", 79, 349, 9, 18),
    ("Standing desk", 249, 699, 22, 38), ("Bedside lamp", 19, 79, 1, 3), ("Wool rug", 59, 299, 3, 12),
    ("Ceramic mug set", 12, 39, 1, 3), ("Cast-iron skillet", 24, 89, 2, 4), ("Chef's knife", 29, 149, 0.2, 0.5),
    ("French press", 19, 59, 0.5, 1.5), ("Electric kettle", 24, 99, 1, 2), ("Stand mixer", 179, 499, 6, 11),
    ("Garden hose (15 m)", 19, 59, 2, 5), ("Pair of pruning shears", 12, 49, 0.2, 0.6), ("Watering can", 9, 29, 0.5, 1.5),
    ("Cordless drill", 59, 229, 1.2, 2.8), ("Tape measure", 7, 29, 0.2, 0.5), ("Claw hammer", 11, 39, 0.5, 1),
    ("Screwdriver set", 14, 59, 0.5, 2), ("LED desk light", 21, 89, 0.6, 2), ("Wireless mouse", 12, 69, 0.1, 0.2),
    ("Mechanical keyboard", 49, 189, 0.8, 1.4), ("Laptop stand", 19, 79, 0.8, 2.5), ("Monitor arm", 39, 149, 2, 6),
    ("Yoga mat", 15, 69, 1, 2.5), ("Dumbbell pair (10 kg)", 29, 89, 20, 21), ("Camping tent", 79, 399, 2.5, 7),
    ("Sleeping bag", 39, 219, 1, 2.5), ("Hiking backpack", 49, 239, 1, 2.2), ("Bike helmet", 29, 149, 0.3, 0.6),
    ("Duvet (double)", 39, 189, 1.5, 3.5), ("Pillow pair", 19, 79, 1, 2), ("Bath towel set", 24, 89, 1.5, 3),
    ("Blender", 39, 199, 2, 5), ("Toaster", 19, 89, 1.5, 3), ("Rice cooker", 29, 139, 2, 4.5),
    ("Air purifier", 89, 399, 4, 9), ("Desk fan", 19, 69, 1.5, 4), ("Bookshelf speaker pair", 99, 449, 6, 14),
    ("Travel suitcase", 69, 299, 2.5, 5), ("Rain jacket", 39, 219, 0.3, 0.9), ("Pair of winter boots", 59, 219, 1.2, 2.4),
]
SUPPLIERS = ["Northline Supply", "Crestview Wholesale", "Harbor Trade Co.", "Pioneer Distribution", "Beacon Imports"]
DEPTS = ["Finance", "Marketing", "Operations", "Human Resources", "IT", "Legal", "Customer Service", "Research",
         "Facilities", "Sales", "Procurement", "Communications", "Logistics", "Quality Assurance", "Product",
         "Design", "Training", "Security", "Compliance", "Engineering"]
CLUB_SFX = ["Rovers", "United", "Athletic", "City", "Wanderers", "Rangers", "Town", "Albion", "FC", "Harriers"]
COUNTRIES = ["Kenya", "Ethiopia", "Japan", "Norway", "Brazil", "Canada", "Spain", "Morocco", "Germany", "Mexico",
             "Uganda", "Italy", "Australia", "Poland", "Chile", "Ireland", "Portugal", "India"]
BRANDS = ["Pyrelle Junior", "Febrinol Kids", "Calmadol Infant", "Thermocalm Junior", "Softfever Kids", "Nurelle Paediatric"]
INGRS = ["pyranol", "febrizone", "calmidine", "thermadol", "algorex"]
CARRIERS = ["Parcelwise", "Swiftpost", "Corvid Couriers", "Beacon Parcel", "Tern Express"]
ROOMS = [("Standard Single", 60, 120, 1), ("Standard Double", 80, 160, 2), ("Twin Room", 80, 160, 2), ("Deluxe Double", 120, 220, 2),
         ("Junior Suite", 180, 320, 3), ("Family Room", 140, 260, 4), ("Garden Suite", 200, 360, 3), ("Sea View Double", 140, 250, 2),
         ("Accessible Double", 90, 170, 2), ("Studio Apartment", 110, 200, 3), ("Penthouse Suite", 320, 450, 4),
         ("Economy Twin", 60, 110, 2), ("Superior King", 150, 260, 2), ("Loft Room", 130, 230, 3), ("Family Suite", 190, 330, 5),
         ("Bunk Room", 70, 130, 4)]
HOTELS = ["Harbourview Hotel", "The Linden Inn", "Castleton Lodge", "Seacliff House", "The Old Mill Hotel",
          "Brookside Guesthouse", "Meadowgate Hotel"]
PLANS = ["Starter", "Essential", "Plus", "Premium", "Family Share", "Student", "Traveller", "Everyday", "Pro",
         "Lite", "Value", "Ultra", "Flex", "Max", "Basic", "Connect"]
TELCOS = ["Lumen Mobile", "Brightwave", "Northstar Telecom", "Kite Mobile", "Parallax Wireless"]
CARS = [("Economy hatchback", 25, 45, 4, 1, 2), ("Compact hatchback", 30, 55, 5, 1, 2), ("Intermediate sedan", 40, 70, 5, 2, 3),
        ("Standard SUV", 55, 95, 5, 3, 4), ("Full-size sedan", 55, 90, 5, 3, 4), ("7-seat people carrier", 75, 130, 7, 3, 5),
        ("Premium SUV", 110, 190, 5, 4, 5), ("Electric compact", 45, 80, 5, 1, 2), ("Convertible", 80, 150, 4, 1, 2),
        ("Cargo van", 70, 120, 3, 6, 8), ("Pickup truck", 70, 120, 5, 3, 5), ("12-seat minibus", 120, 190, 12, 5, 8),
        ("Hybrid estate", 50, 85, 5, 3, 4), ("Compact SUV", 45, 80, 5, 2, 3)]
RENTALS = ["Roadway Rentals", "Kestrel Car Hire", "Arrow Drive", "Openroad Hire", "Metro Wheels"]
FOODS = [  # (name, serving g, kcal/100g, protein/100g, sugar/100g, fat/100g, fibre/100g)
    ("Oatmeal (dry)", 40, 379, 13.2, 1.0, 6.5, 10.1), ("Greek yogurt", 170, 97, 9.0, 3.6, 5.0, 0.0),
    ("Wholemeal bread", 36, 247, 10.7, 4.4, 3.4, 6.8), ("Brown rice (cooked)", 150, 123, 2.7, 0.4, 1.0, 1.6),
    ("Lentil dal", 150, 116, 9.0, 1.8, 0.4, 7.9), ("Chicken breast (grilled)", 120, 165, 31.0, 0.0, 3.6, 0.0),
    ("Salmon fillet", 130, 208, 20.4, 0.0, 13.4, 0.0), ("Cheddar cheese", 30, 403, 24.9, 0.5, 33.1, 0.0),
    ("Almond butter", 32, 614, 21.0, 4.4, 55.5, 10.3), ("Banana", 118, 89, 1.1, 12.2, 0.3, 2.6),
    ("Apple", 182, 52, 0.3, 10.4, 0.2, 2.4), ("Peanut butter", 32, 588, 25.1, 9.2, 50.4, 6.0),
    ("Hummus", 60, 166, 7.9, 0.3, 9.6, 6.0), ("Granola", 50, 471, 10.0, 24.0, 20.0, 5.3),
    ("Tofu (firm)", 100, 144, 15.8, 0.6, 8.7, 2.3), ("Boiled egg", 50, 155, 12.6, 1.1, 10.6, 0.0),
    ("Whole milk", 250, 61, 3.2, 5.1, 3.3, 0.0), ("Oat drink", 250, 45, 1.0, 4.0, 1.5, 0.8),
    ("Dark chocolate", 25, 546, 4.9, 48.0, 31.3, 7.0), ("Chickpea stew", 220, 139, 7.0, 0.3, 2.6, 6.4),
    ("Cottage cheese", 110, 98, 11.1, 2.7, 4.3, 0.0), ("Quinoa (cooked)", 185, 120, 4.4, 0.9, 1.9, 2.8),
    ("Muesli bar", 35, 420, 7.0, 25.0, 15.0, 5.0), ("Sweet potato (baked)", 150, 90, 2.0, 6.5, 0.2, 3.3),
]
MUSEUMS = ["Harbour Maritime Museum", "City Art Gallery", "Science Discovery Centre", "Railway Heritage Museum",
           "Natural History Hall", "Folk Life Museum", "Modern Design Gallery", "Castle Keep Museum"]
LINES = ["Kitchenware", "Garden", "Outdoor", "Home Office", "Toys", "Bedding", "Pet Care", "Lighting", "Bathroom",
         "Stationery", "Tools", "Sportswear"]
BUILDINGS = ["Block A", "Block B", "Block C", "Block D", "Library", "Sports Hall", "Main Hall", "Science Wing",
             "Arts Centre", "Staff Annex"]
DIVISIONS = ["Retail", "Wholesale", "Online", "Services", "Licensing", "International", "Healthcare", "Education"]
GRANTEES = ["Youth Theatre", "Food Bank", "Community Garden", "Historical Society", "Rowing Club", "Literacy Project",
            "Wildlife Trust", "Men's Shed", "Choir", "Repair Café", "Allotment Society", "Film Club"]
CLINICIANS = ["Dr Okafor", "Dr Haddad", "Dr Lindqvist", "Dr Mensah", "Dr Tanaka", "Dr Reyes", "Nurse Walsh",
              "Nurse Kariuki"]
CITIES = {  # name: (UTC offset in minutes, lat, lon) -- standard-time offsets, stated explicitly in each table's note
    "London": (0, 51.5, -0.1), "Lisbon": (0, 38.7, -9.1), "Reykjavik": (0, 64.1, -21.9), "Paris": (60, 48.9, 2.4),
    "Berlin": (60, 52.5, 13.4), "Madrid": (60, 40.4, -3.7), "Lagos": (60, 6.5, 3.4), "Athens": (120, 38.0, 23.7),
    "Cairo": (120, 30.0, 31.2), "Johannesburg": (120, -26.2, 28.0), "Istanbul": (180, 41.0, 29.0),
    "Nairobi": (180, -1.3, 36.8), "Dubai": (240, 25.2, 55.3), "Karachi": (300, 24.9, 67.0),
    "Delhi": (330, 28.6, 77.2), "Kathmandu": (345, 27.7, 85.3), "Dhaka": (360, 23.8, 90.4),
    "Bangkok": (420, 13.8, 100.5), "Singapore": (480, 1.35, 103.8), "Tokyo": (540, 35.7, 139.7),
    "Sydney": (600, -33.9, 151.2), "New York": (-300, 40.7, -74.0), "Chicago": (-360, 41.9, -87.6),
    "Denver": (-420, 39.7, -105.0), "Los Angeles": (-480, 34.1, -118.2), "Toronto": (-300, 43.7, -79.4),
    "Mexico City": (-360, 19.4, -99.1), "Sao Paulo": (-180, -23.5, -46.6),
}
DATE_STYLES = ["iso", "dmy", "mdy", "dmyn", "mdyn", "iso", "dmy"]
MISS = [("—", "— = not reported."), ("n/a", "n/a = figure not available."), ("", "A blank cell means the figure was not reported."),
        ("not reported", None), ("?", "? = not yet known."), ("–", "– = no figure reported.")]


def people(rng, n):
    out = set()
    while len(out) < n:
        out.add(f"{rng.choice(FIRST)} {rng.choice(LAST)}")
    out = sorted(out)
    rng.shuffle(out)
    return out


def pick(rng, pool, n, extra=6):
    names = rng.sample(pool, min(len(pool), n + extra))
    return names[:n], names[n:]


def rstep(rng, lo, hi, step=1):
    return rng.randrange(lo, hi + 1, step) if hi > lo else lo


def vf(deps, fn):
    def f(t, e):
        xs = [t.get(e, d) for d in deps]
        if any(x is None for x in xs):
            return None
        return fn(*xs)
    return f


def base_style(rng, t, allow_transposed=True):
    fmts = ["md", "md", "md", "md", "pipe", "pipe", "csv", "fixed", "fixed", "records", "tsv"]
    if allow_transposed and len(t.rows) <= 7 and len(t.cols) <= 6:
        fmts.append("transposed")
    fmt = rng.choice(fmts)
    miss = rng.choice([m for m in MISS if not (m[0] == "" and fmt in ("fixed", "records", "transposed"))])
    t.style.update(fmt=fmt, cellunit=rng.random() < 0.6, time=rng.choice(["24", "24", "12"]),
                   date=rng.choice(DATE_STYLES), miss=miss[0], miss_note=miss[1],
                   corr_tpl=rng.choice(["Correction: the {noun} for {e} should read {new}, not {old} as printed.",
                                        "Erratum: the {noun} for {e} was misprinted as {old}; the correct figure is {new}."]))


def set_partial(t, rng, rest, p_count=0.18, p_sel=0.14):
    r = rng.random()
    t.pool = list(rest)
    if r < p_count:
        t.partial = "count"
        t.total = len(t.rows) + rng.randint(2, 10)
        t.subtitle = rng.choice([f"Showing {{n}} of {t.total} {t.ent.pl}.",
                                 f"Excerpt: {{n}} of the {t.total} {t.ent.pl}.",
                                 f"({{n}} of {t.total} {t.ent.pl} shown)"])
    elif r < p_count + p_sel:
        t.partial = "selected"
        t.subtitle = rng.choice([f"Selected {t.ent.pl} only; the full list is longer.",
                                 f"Excerpt - not all {t.ent.pl} are shown.",
                                 f"Only some {t.ent.pl} are listed here."])


def random_blanks(t, rng, p=0.12):
    if rng.random() < p:
        cand = [(e, c.key) for e in t.rows for c in t.cols
                if not c.nomiss and c.key not in t.derived and c.kind not in ("cat", "bool") and c.ops != []
                and t.v[e].get(c.key) is not None]
        if cand:
            e, k = rng.choice(cand)
            t.v[e][k] = None


def mk(t, rng, n_rows, names, gen_row, rest=(), partial=True, blanks=True, transposed=True):
    t.rows = list(names[:n_rows])
    for e in t.rows:
        t.v[e] = gen_row(rng, e)
    t.mkrow = gen_row
    t.apply_derive()
    if partial:
        set_partial(t, rng, rest)
    else:
        t.pool = list(rest)
    base_style(rng, t, transposed)
    if blanks:
        random_blanks(t, rng)
    return t


def nrows(rng, lo=5, hi=10, long_p=0.12, long_hi=22):
    return rng.randint(15, long_hi) if rng.random() < long_p else rng.randint(lo, hi)


def subset_cols(rng, must, opt, k_lo, k_hi):
    k = rng.randint(k_lo, min(k_hi, len(opt)))
    chosen = set(must) | set(rng.sample(opt, k))
    return chosen


# ------------------------------------------------------------------------------------------------ retail
def build_retail(rng):
    co, per = rng.choice(RETAIL_COS), rng.choice(PERIODS)
    cur = rng.choice(["$", "$", "$", "€", "£"])
    scale = rng.random() < 0.3
    ent = Ent("Store", "store", "stores", rng.choice(["the {x} store", "the {x} branch", "the {x} store"]))
    allc = {
        "units": Col("units", "Units sold", "num", "number of units sold", lo=60, hi=980,
                     vp=VP("sold", "sell", "unit", "units", pp="sold"), cmpnoun="unit sales"),
        "rev": (Col("rev", "Revenue", "money", "revenue", pre=cur, unit_hdr=f"{cur}000s", force_hdr=True, lo=150,
                    hi=9800, scale=1000, avg=False, mass=True) if scale else
                Col("rev", "Revenue", "money", "revenue", pre=cur, unit_hdr=cur, lo=4000, hi=180000, step=10, mass=True)),
        "ret": Col("ret", "Returns", "num", "number of returns", lo=0, hi=45, vp=VP("had", "have", "return", "returns", pp="had"),
                   gen_lo=0),
        "staff": Col("staff", "Staff", "num", "number of staff", lo=4, hi=28,
                     vp=VP("employed", "employ", "staff member", "staff members", cobj="staff", pp="employed")),
        "region": Col("region", "Region", "cat", "region", cats=REGIONS, sayf="is in the {X} region",
                      sayfn="is not in the {X} region", sayp="are in the {X} region", filt="in the {X} region"),
        "opened": Col("opened", "Opened", "date", "opening date", tvp=("opened", "open", "on", "past"),
                      words=("later", "earlier", "latest", "earliest", "late", "early"),
                      above=("later than", "earlier than"), step=1, ops=["val", "thr", "cmp", "sup", "argthen", "count"]),
    }
    keys = subset_cols(rng, ["units"] if rng.random() < 0.6 else ["rev"], ["units", "rev", "ret", "staff", "region", "opened"], 2, 4)
    order = [k for k in ["region", "opened", "units", "rev", "ret", "staff"] if k in keys]
    cols = [allc[k] for k in order]
    vcols = []
    if "units" in keys and "ret" in keys:
        vcols.append(Col("net", "", "num", "number of units sold after returns", fn=vf(["units", "ret"], lambda u, r: u - r),
                         deps=["units", "ret"], vp=VP("sold", "sell", "unit", "units", suffix=" after returns"),
                         ops=["val", "thr", "cmp", "sup", "count"]))
    t = Table("retail", f"{co}: {rng.choice(['sales by store', 'store performance', 'branch results'])}, {per}", ent, cols, vcols)
    lo_date, hi_date = od(2006, 1, 1), od(2024, 12, 31)

    def gen(rng, e):
        units = rstep(rng, 60, 980)
        r = {"units": units, "ret": min(units // 8, rng.randint(0, 45)), "staff": rng.randint(4, 28),
             "region": rng.choice(REGIONS), "opened": rng.randint(lo_date, hi_date)}
        r["rev"] = rstep(rng, 150, 9800) if scale else rstep(rng, 4000, 180000, 10)
        return r
    t.valid = lambda t: all(t.v[e].get("ret") is None or t.v[e].get("units") is None or t.v[e]["ret"] <= t.v[e]["units"] for e in t.rows)
    names, rest = pick(rng, STREETS, nrows(rng), 8)
    return mk(t, rng, len(names), names, gen, rest)


# ------------------------------------------------------------------------------------------------ inventory
def build_inventory(rng):
    wh = rng.choice(["Central warehouse", "Store room B", "Unit 4 depot", "Main stockroom", "North distribution centre"])
    ent = Ent("Item", "item", "items", "the {xl}")
    has_status = rng.random() < 0.6
    allc = {
        "qty": Col("qty", "In stock", "num", "stock level", lo=0, hi=480, gen_lo=0,
                   vp=VP("has", "have", "unit in stock", "units in stock", cobj="units in stock", tense="pres", unit=("unit", "units"))),
        "reord": Col("reord", "Reorder level", "num", "reorder level", lo=10, hi=150, step=5, sum=False),
        "cost": Col("cost", "Unit cost", "money", "unit cost", pre="$", unit_hdr="$", dec=2, lo=50, hi=25000, step=5, sum=False),
        "aisle": Col("aisle", "Location", "cat", "location", cats=[f"Aisle {i}" for i in range(1, 9)],
                     sayf="is stored in {X}", sayfn="is not stored in {X}", sayp="are stored in {X}", filt="stored in {X}"),
        "sup": Col("sup", "Supplier", "cat", "supplier", cats=SUPPLIERS, sayf="is supplied by {X}",
                   sayfn="is not supplied by {X}", sayp="are supplied by {X}", filt="supplied by {X}"),
        "status": Col("status", "Status", "cat", "status", cats=["Active", "Discontinued"],
                      say={"Active": ("is listed as Active", "is not listed as Active", "are listed as Active", "are not listed as Active"),
                           "Discontinued": ("is listed as Discontinued", "is not listed as Discontinued",
                                            "are listed as Discontinued", "are not listed as Discontinued")},
                      filt="listed as {X}", nomiss=True),
    }
    keys = ["qty", "reord", "cost"] + rng.sample(["aisle", "sup"], rng.randint(0, 2)) + (["status"] if has_status else [])
    cols = [allc[k] for k in keys]
    deps = ["qty", "reord"] + (["status"] if has_status else [])

    def need(q, r, *st):
        return "yes" if (q <= r and not (st and st[0] == "Discontinued")) else "no"
    say_need = {"yes": ("needs to be reordered", "does not need to be reordered", "need to be reordered", "do not need to be reordered"),
                "no": ("does not need to be reordered", "needs to be reordered", "do not need to be reordered", "need to be reordered")}
    vcols = [Col("value", "", "money", "stock value", pre="$", dec=2, fn=vf(["qty", "cost"], lambda q, c: q * c),
                 deps=["qty", "cost"], ops=["val", "thr", "cmp", "sup", "sum", "count"], cmpnoun="stock value"),
             Col("need", "", "bool", "reorder status", cats=["yes", "no"], fn=vf(deps, need), deps=deps, say=say_need,
                 ops=["catval", "catcount", "argthen"], w=4.0, exc=has_status)]
    t = Table("inventory", f"{wh}: stock report{rng.choice(['', ' (end of day)', ' - weekly count'])}", ent, cols, vcols)

    def notes(t):
        rule = "Reorder rule: an item must be reordered when its units in stock are at or below its reorder level"
        return [rule + (", unless its status is Discontinued." if has_status else "."),
                "Stock value means units in stock multiplied by unit cost."]
    t.notes_fn = notes

    def gen(rng, e):
        reord = rstep(rng, 10, 150, 5)
        spec = next(x for x in PRODUCTS if x[0] == e)
        r = {"reord": reord, "cost": rstep(rng, spec[1] * 40, spec[2] * 60, 5), "aisle": rng.choice(allc["aisle"].cats),
             "sup": rng.choice(SUPPLIERS), "status": "Discontinued" if rng.random() < 0.25 else "Active"}
        x = rng.random()
        r["qty"] = reord if x < 0.15 else (rstep(rng, 0, max(0, reord - 1)) if x < 0.45 else rstep(rng, reord + 1, reord + 330))
        return r
    pool = [p[0] for p in PRODUCTS]
    names, rest = pick(rng, pool, nrows(rng), 8)
    return mk(t, rng, len(names), names, gen, rest)


# ------------------------------------------------------------------------------------------------ price list
def build_price(rng):
    shop = rng.choice(["Oakhurst Furniture", "Tidewater Home", "Copperline Hardware", "Summit Sports", "Larkspur Home & Garden"])
    p = rng.choice([10, 15, 20, 25])
    step = {10: 50, 15: 200, 20: 50, 25: 100}[p]
    ent = Ent("Product", "product", "products", "the {xl}")
    allc = {
        "price": Col("price", "Price", "money", "listed price", pre="$", unit_hdr="$", dec=2, lo=500, hi=90000, step=step,
                     cmpnoun="listed price", sum_all=False),
        "wt": Col("wt", "Weight", "num", "weight", dec=1, suf=" kg", unit_hdr="kg", lo=1, hi=450, conv=["g"], trim=False,
                  sum_all=False),
        "stock": Col("stock", "Stock", "cat", "stock status", cats=["In stock", "Low stock", "Out of stock"],
                     say={"In stock": ("is listed as in stock", "is not listed as in stock", "are listed as in stock", "are not listed as in stock"),
                          "Low stock": ("is listed as low stock", "is not listed as low stock", "are listed as low stock", "are not listed as low stock"),
                          "Out of stock": ("is listed as out of stock", "is not listed as out of stock", "are listed as out of stock",
                                           "are not listed as out of stock")},
                     filt="listed as {X}"),
        "rating": Col("rating", "Rating", "num", "average customer rating", dec=1, suf=" / 5", unit_hdr="out of 5", lo=21,
                      hi=50, hi_cap=50, sum=False),
        "warr": Col("warr", "Warranty", "num", "warranty period", suf=" months", unit_hdr="months", lo=6, hi=60, step=6, sum=False),
    }
    keys = ["price"] + rng.sample(["wt", "stock", "rating", "warr"], rng.randint(1, 3))
    cols = [allc[k] for k in keys]

    def member(pr, star):
        if star:
            return pr
        x = Fr(pr * (100 - p), 100)
        return int(x) if x.denominator == 1 else x
    vcols = [Col("mprice", "", "money", "member price", pre="$", dec=2, fn=vf(["price", "_star"], member),
                 deps=["price", "_star"], ops=["val", "thr", "cmp", "sup", "argthen", "count", "diff"], w=3.0, exc=True)]
    t = Table("price", f"{shop} - price list{rng.choice(['', ' (autumn catalogue)', ' - online store'])}", ent, cols, vcols)
    t.p["disc"] = p
    t.notes_fn = lambda t: [f"Members get {p}% off the listed price, except on products marked *."]

    def gen(rng, e):
        spec = next(x for x in PRODUCTS if x[0] == e)
        price = rstep(rng, spec[1] * 100, spec[2] * 100, step)
        return {"price": price, "wt": rng.randint(int(spec[3] * 10), int(spec[4] * 10)),
                "stock": rng.choice(allc["stock"].cats), "rating": rng.randint(21, 50), "warr": rng.choice([6, 12, 24, 36, 60]),
                "_star": rng.random() < 0.3}
    names, rest = pick(rng, [x[0] for x in PRODUCTS], nrows(rng, 5, 10, 0.05, 16), 8)
    t = mk(t, rng, len(names), names, gen, rest)
    if not any(t.v[e]["_star"] for e in t.rows):
        t.v[rng.choice(t.rows)]["_star"] = True
    return t


# ------------------------------------------------------------------------------------------------ league standings
def build_standings(rng):
    n = rng.randint(6, 12) if rng.random() > 0.06 else rng.randint(14, 18)
    P = rng.randint(10, 22)
    ent = Ent("Team", "team", "teams", "{x}")
    abbr = rng.random() < 0.5
    hide_pts = rng.random() < 0.3
    H = (lambda a, b: a if abbr else b)
    cols = [Col("P", H("P", "Played"), "num", "number of matches played", ops=[], nomiss=True),
            Col("W", H("W", "Won"), "num", "number of wins", vp=VP("won", "win", "match", "matches", pp="won"), nomiss=True),
            Col("D", H("D", "Drawn"), "num", "number of draws", vp=VP("drew", "draw", "match", "matches", pp="drawn"), nomiss=True),
            Col("L", H("L", "Lost"), "num", "number of defeats", vp=VP("lost", "lose", "match", "matches", pp="lost"), nomiss=True),
            Col("GF", H("GF", "Goals for"), "num", "number of goals scored", vp=VP("scored", "score", "goal", "goals", pp="scored"), nomiss=True),
            Col("GA", H("GA", "Goals against"), "num", "number of goals conceded", vp=VP("conceded", "concede", "goal", "goals", pp="conceded"), nomiss=True),
            Col("GD", H("GD", "Goal difference"), "num", "goal difference", signed=True, nonneg=False, domain_lo=-10 ** 9,
                ops=["val", "thr", "cmp", "sup", "count", "quant", "argthen"], nomiss=True, sum=False)]
    vcols = []
    if hide_pts:
        vcols.append(Col("Pts", "", "num", "points total", fn=vf(["W", "D"], lambda w, d: 3 * w + d), deps=["W", "D"],
                         vp=VP("has", "have", "point", "points", tense="pres", cobj="points"),
                         ops=["val", "thr", "cmp", "sup", "count", "argthen", "diff"]))
    else:
        cols.append(Col("Pts", H("Pts", "Points"), "num", "points total",
                        vp=VP("has", "have", "point", "points", tense="pres", cobj="points"), nomiss=True))
    t = Table("standings", f"{rng.choice(['County', 'Regional', 'Coastal', 'Valley'])} League {rng.choice(['Division One', 'Division Two', 'Premier Division'])} - table after {P} matches", ent, cols, vcols)
    t.derived = {"L", "GD"} | ({"Pts"} if not hide_pts else set())
    t.p["P"] = P

    def derive(t):
        for e in t.rows:
            r = t.v[e]
            r["P"] = P
            r["L"] = P - r["W"] - r["D"]
            r["GD"] = r["GF"] - r["GA"]
            if not hide_pts:
                r["Pts"] = 3 * r["W"] + r["D"]
    t.derive = derive

    def sort(t):
        if hide_pts:
            t.rows.sort()
        else:
            t.rows.sort(key=lambda e: (-t.v[e]["Pts"], -t.v[e]["GD"], -t.v[e]["GF"], e))
    t.sort = sort
    t.valid = lambda t: all(0 <= t.v[e]["W"] and 0 <= t.v[e]["D"] and t.v[e]["W"] + t.v[e]["D"] <= P
                            and t.v[e]["GF"] >= 0 and t.v[e]["GA"] >= 0 for e in t.rows)

    def notes(t):
        out = []
        if abbr:
            out.append("Key: P = played, W = won, D = drawn, L = lost, GF = goals for, GA = goals against, GD = goal difference"
                       + ("" if hide_pts else ", Pts = points") + ".")
        if hide_pts:
            out.append("Teams get 3 points for a win, 1 for a draw and 0 for a defeat.")
        out.append("Teams level on points are ranked by goal difference, then by goals scored.")
        return out
    t.notes_fn = notes

    def gen(rng, e):
        st = rng.uniform(0.1, 0.7)
        w = d = gf = ga = 0
        for _ in range(P):
            r = rng.random()
            if r < st:
                w += 1
                a = rng.choice([1, 1, 2, 2, 3, 4])
                gf, ga = gf + a, ga + rng.randint(0, a - 1)
            elif r < st + 0.27:
                d += 1
                a = rng.choice([0, 1, 1, 2])
                gf, ga = gf + a, ga + a
            else:
                a = rng.choice([1, 1, 2, 2, 3])
                ga, gf = ga + a, gf + rng.randint(0, a - 1)
        return {"W": w, "D": d, "GF": gf, "GA": ga}
    towns = rng.sample(TOWNS, n + 6)
    names = [f"{x} {rng.choice(CLUB_SFX)}" for x in towns]
    t.special = ["position"]
    return mk(t, rng, n, names, gen, names[n:], partial=False, blanks=False, transposed=False)


# ------------------------------------------------------------------------------------------------ player stats
def build_players(rng):
    teams = [f"{rng.choice(TOWNS).split()[0]} {x}" for x in rng.sample(["Hawks", "Comets", "Tide", "Foxes", "Stags", "Owls", "Rockets", "Pilots"], 3)]
    ent = Ent("Player", "player", "players", "{x}")
    allc = {
        "team": Col("team", "Team", "cat", "team", cats=teams, sayf="plays for the {X}", sayfn="does not play for the {X}",
                    sayp="play for the {X}", filt="on the {X}"),
        "gp": Col("gp", "GP", "num", "number of games played", lo=8, hi=82, vp=VP("played", "play", "game", "games", pp="played"),
                  sum=False),
        "ppg": Col("ppg", "PPG", "num", "points per game", dec=1, lo=30, hi=315,
                   vp=VP("averaged", "average", "point per game", "points per game", pp="averaged"), sum=False),
        "rpg": Col("rpg", "RPG", "num", "rebounds per game", dec=1, lo=10, hi=135,
                   vp=VP("averaged", "average", "rebound per game", "rebounds per game", pp="averaged"), sum=False),
        "apg": Col("apg", "APG", "num", "assists per game", dec=1, lo=5, hi=105,
                   vp=VP("averaged", "average", "assist per game", "assists per game", pp="averaged"), sum=False),
        "fg": Col("fg", "FG%", "pct", "field-goal percentage", dec=1, suf="%", lo=350, hi=650, hi_cap=1000, sum=False),
    }
    keys = ["team", "gp"] + rng.sample(["ppg", "rpg", "apg", "fg"], rng.randint(2, 4))
    cols = [allc[k] for k in keys]
    t = Table("players", f"{rng.choice(['Metro', 'Coastal', 'National', 'Valley'])} Basketball League - {rng.choice(['2024-25', '2025-26'])} season averages", ent, cols)
    legend = {"gp": "GP = games played", "ppg": "PPG = points per game", "rpg": "RPG = rebounds per game",
              "apg": "APG = assists per game", "fg": "FG% = field-goal percentage"}
    t.notes_fn = lambda t: ["Key: " + "; ".join(legend[k] for k in keys if k in legend) + "."]

    def gen(rng, e):
        return {"team": rng.choice(teams), "gp": rng.randint(8, 82), "ppg": rng.randint(30, 315), "rpg": rng.randint(10, 135),
                "apg": rng.randint(5, 105), "fg": rng.randint(350, 650)}
    names = people(rng, 20)
    n = nrows(rng, 5, 10)
    return mk(t, rng, n, names, gen, names[n:])


# ------------------------------------------------------------------------------------------------ grades
SCHEMES = [((90, "A"), (80, "B"), (70, "C"), (60, "D")), ((85, "A"), (70, "B"), (55, "C"), (40, "D"))]
SUBJ = ["Math", "English", "Science", "History", "Geography", "Art", "French", "Biology", "Chemistry", "Physics", "Computing", "Music"]


def build_grades(rng):
    scheme = rng.choice(SCHEMES)
    subs = rng.sample(SUBJ, rng.randint(3, 4))
    exc = rng.random() < 0.55
    att_thr = rng.choice([75, 80, 85])
    ent = Ent("Student", "student", "students", "{x}")
    cols = [Col(s.lower(), s, "num", f"{s} score", lo=35, hi=100, hi_cap=100, sum=False) for s in subs]  # scores are out of 100 (the grading key tops out at 100)
    cols.append(Col("att", "Attendance", "pct", "attendance", suf="%", unit_hdr="%", lo=55, hi=100, hi_cap=100, sum=False, mass=True))

    def band(x):
        for lo, L in scheme:
            if x >= lo:
                return L
        return "F"
    vcols = []
    for s in subs:
        k = s.lower()
        if exc:
            fn = vf([k, "att"], lambda x, a: "I" if a < att_thr else band(x))
            deps = [k, "att"]
        else:
            fn = vf([k], band)
            deps = [k]
        say = {}
        for L in ["A", "B", "C", "D", "F"]:
            say[L] = (f"earned {art(L)} {L} in {s}", f"did not earn {art(L)} {L} in {s}", f"earned {art(L)} {L} in {s}",
                      f"did not earn {art(L)} {L} in {s}")
        say["I"] = (f"received an I (Incomplete) in {s}", f"did not receive an I (Incomplete) in {s}",
                    f"received an I (Incomplete) in {s}", f"did not receive an I (Incomplete) in {s}")
        vcols.append(Col("g_" + k, "", "cat", f"{s} grade", cats=["A", "B", "C", "D", "F"] + (["I"] if exc else []), fn=fn,
                         deps=deps, say=say, ops=["catval", "catcount", "argthen"], w=2.0, exc=exc))
    ks = [s.lower() for s in subs]
    vcols.append(Col("avg", "", "num", f"average score across the {len(subs)} subjects", dec=1,
                     fn=vf(ks, lambda *xs: Fr(sum(xs) * 10, len(xs))), deps=ks, ops=["val", "thr", "cmp", "sup", "rank", "count"],
                     cmpnoun="average score"))
    t = Table("grades", f"{rng.choice(['Year 10', 'Year 11', 'Grade 9', 'Grade 11', 'Form 5'])} {rng.choice(['end-of-term', 'semester', 'mid-year'])} results - class {rng.choice('ABCDEFGH')}", ent, cols, vcols)

    def notes(t):
        parts = [f"{L} = {lo}-{hi}" for (lo, L), hi in zip(scheme, [100] + [x[0] - 1 for x in scheme[:-1]])]
        out = ["Grading key: " + ", ".join(parts) + f", F = below {scheme[-1][0]}."]
        if exc:
            out.append(f"Students whose attendance is below {att_thr}% receive an I (Incomplete) in every subject instead of a letter grade.")
        return out
    t.notes_fn = notes
    t.p.update(scheme=scheme, exc=exc, att_thr=att_thr)
    edges = [lo for lo, _ in scheme]

    def gen(rng, e):
        r = {}
        for k in ks:
            x = rng.random()
            if x < 0.3:
                b = rng.choice(edges)
                r[k] = min(100, b + rng.choice([-1, 0, 0, 1]))
            else:
                r[k] = rng.randint(38, 100)
        a = rng.random()
        r["att"] = (att_thr + rng.choice([-1, 0, 0, 1])) if a < 0.25 else rng.randint(62, 100)
        return r
    names = people(rng, 22)
    n = nrows(rng, 5, 10)
    return mk(t, rng, n, names, gen, names[n:])


# ------------------------------------------------------------------------------------------------ dosing chart (special)
BANDSETS = [[50, 80, 110, 160, 220, 270, 320, 440], [60, 90, 120, 150, 200, 250, 300, 400], [40, 60, 80, 100, 120, 160, 200, 260]]
DOSES = [25, 30, 40, 50, 60, 75, 90, 100, 120, 150, 200]  # tenths of a mL


def build_dosing(rng):
    edges = rng.choice(BANDSETS)
    k = rng.randint(4, len(edges) - 1)
    st = rng.randint(0, len(edges) - 1 - k)
    edges = edges[st:st + k + 1]
    brand, ingr = rng.choice(BRANDS), rng.choice(INGRS)
    conc = rng.choice([100, 120, 160, 200, 250])
    ent = Ent("Weight", "weight band", "weight bands", "the {x} band")
    const_gap = rng.random() < 0.5
    cols = [Col("dose", "Single dose", "num", "single dose", dec=1, suf=" mL", unit_hdr="mL", trim=True, ops=[], lo=25, hi=200, step=5),
            Col("maxd", "Max doses in 24 h", "num", "maximum number of doses in 24 hours", ops=[], lo=3, hi=4),
            Col("gap", "Min. hours between doses", "num", "minimum gap between doses", ops=[], lo=4, hi=8)]
    t = Table("dosing", f"{brand} oral suspension ({conc} mg {ingr} per 5 mL) - dosing by body weight", ent, cols)
    t.p.update(edges=edges, conc=conc, ingr=ingr, brand=brand)
    bands = []
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i + 1] - 1
        bands.append((lo, hi, f"{trim_dec(fixed(lo, 1))}-{trim_dec(fixed(hi, 1))} kg"))
    t.p["bands"] = bands
    ds = sorted(rng.sample(DOSES[:min(len(DOSES), len(bands) + 5)], len(bands)))
    g = rng.choice([4, 6, 8])
    t.rows = [b[2] for b in bands]
    for (lo, hi, lab), d in zip(bands, ds):
        t.v[lab] = {"dose": d, "maxd": rng.choice([3, 4]) if not const_gap else 4, "gap": g if const_gap else rng.choice([4, 6, 8])}
    t.notes_fn = lambda t: [f"Each 5 mL contains {conc} mg of {ingr}.",
                            f"Do not use for children weighing less than {trim_dec(fixed(edges[0], 1))} kg; "
                            f"above {trim_dec(fixed(edges[-1] - 1, 1))} kg, use the adult product."]
    t.valid = lambda t: all(t.v[a]["dose"] < t.v[b]["dose"] for a, b in zip(t.rows, t.rows[1:])) and \
        all(t.v[e]["maxd"] in (3, 4, 5) and t.v[e]["gap"] in (3, 4, 6, 8) for e in t.rows)
    t.special = ["dose"]
    t.mkrow = None
    base_style(rng, t)
    t.style["cellunit"] = rng.random() < 0.5
    return t


class DoseOp(Op):
    name, qa_ok = "dose", True

    def applicable(self, t):
        return t.dom == "dosing"

    def band(self, t, w):
        for lo, hi, lab in t.p["bands"]:
            if lo <= w <= hi:
                return lab
        return None

    def value(self, t, s):
        b = self.band(t, s["w"])
        kind = s["kind"]
        if kind == "allowed":
            return "yes" if b else "no"
        if b is None:
            return None
        r = t.v[b]
        if kind == "dose":
            return r["dose"]
        if kind == "maxday":
            return r["dose"] * r["maxd"]
        if kind == "mg":
            m = Fr(r["dose"] * t.p["conc"], 50)
            return int(m) if m.denominator == 1 else None
        if kind == "interval":
            return r["gap"]
        return None

    def sample(self, t, rng, want):
        if want == N:
            return None
        kind = rng.choice(["dose", "dose", "maxday", "mg", "interval", "allowed"])
        bands = t.p["bands"]
        i = rng.randrange(len(bands))
        lo, hi, lab = bands[i]
        choice = rng.random()
        if kind == "allowed" and rng.random() < 0.5:
            w = rng.choice([t.p["edges"][0] - rng.choice([1, 2, 5, 10]), t.p["edges"][-1] + rng.choice([0, 5, 20])])
        elif choice < 0.3:
            w = lo
        elif choice < 0.55:
            w = hi
        elif choice < 0.7 and i + 1 < len(bands):
            w = hi + 1
        else:
            w = rng.randint(lo, hi)
        if w <= 0:
            return None
        s = {"op": "dose", "kind": kind, "w": w}
        x = self.value(t, s)
        if x is None and kind != "allowed":
            return None
        if kind == "allowed":
            s["v"] = "yes"
            return s if self.eval(t, s) == want else None
        if kind == "interval":
            opts = [x, x - 2, x - 1, x + 2, x + 4] if want == T else [x - 1, x - 2, x - 4]
            opts = [h for h in opts if h >= 2 and (h >= x) == (want == T)]
            if not opts:
                return None
            s["v"] = rng.choice(opts)
            return s
        if want == T:
            s["v"] = x
        else:
            j = [b for b in bands if b[2] != self.band(t, w)]
            other = self.value(t, dict(s, w=rng.choice(j)[0])) if j else None
            cands = [other] * 2 + ([x + 5, x - 5] if kind == "dose" else [x + 10 * (1 if kind != "mg" else 2), x - 10])
            if kind == "maxday":
                r = t.v[self.band(t, w)]
                cands.append(r["dose"] * (r["maxd"] + 1))
            cands = [c for c in cands if c is not None and c > 0 and c != x]
            if not cands:
                return None
            s["v"] = rng.choice(cands)
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        x = self.value(t, s)
        if s["kind"] == "allowed":
            return T if x == "yes" else F
        if x is None:
            return F
        if s["kind"] == "interval":
            return T if s["v"] >= x else F
        return T if x == s["v"] else F

    def _w(self, s):
        return trim_dec(fixed(s["w"], 1))

    def _vstr(self, t, s):
        k = s["kind"]
        if k in ("dose", "maxday"):
            return trim_dec(fixed(s["v"], 1)) + " mL"
        if k == "mg":
            return f"{s['v']} mg"
        if k == "interval":
            return f"{s['v']} hours"
        return ""

    def text(self, t, s):
        w, V, tv = self._w(s), self._vstr(t, s), s["tv"]
        child = ch([f"a child weighing {w} kg", f"a {w} kg child", f"a child who weighs {w} kg"], tv, 2)
        k = s["kind"]
        if k == "dose":
            forms = [f"For {child}, the chart's single dose is {V}", f"The chart gives {child} a single dose of {V}"]
        elif k == "maxday":
            forms = [f"According to the chart, the 24-hour maximum for {child} is {V}",  # states the limit itself, not a bound on it
                     f"The most {child} can be given in 24 hours under the chart is {V}"]
        elif k == "mg":
            forms = [f"Each chart dose for {child} contains {V} of {t.p['ingr']}",
                     f"A single dose for {child} delivers {V} of {t.p['ingr']}"]
        elif k == "interval":
            forms = [f"Under the chart, doses for {child} can be given {V} apart",
                     f"The chart allows {child} to have doses {V} apart"]
        else:
            forms = [f"The chart allows {child} to be given this medicine", f"The chart gives a dose for {child}"]
        return cap(ch(forms, tv))

    def qa(self, t, s):
        w = self._w(s)
        k = s["kind"]
        if k == "dose":
            return f"What single dose does the chart give for a child weighing {w} kg?", self._vstr(t, s)
        if k == "maxday":
            return f"What is the most a child weighing {w} kg may be given in 24 hours according to the chart?", self._vstr(t, s)
        if k == "mg":
            return f"How many mg of {t.p['ingr']} does one chart dose for a child weighing {w} kg contain?", self._vstr(t, s)
        return None

    def cells(self, t, s):
        b = self.band(t, s["w"])
        if b is None:
            return []
        return {"dose": [(b, "dose")], "maxday": [(b, "dose"), (b, "maxd")], "mg": [(b, "dose")],
                "interval": [(b, "gap")]}.get(s["kind"], [])

    def consts(self, t, s):
        b = self.band(t, s["w"])
        k = s["kind"]
        if b is None or k == "allowed":
            return []
        if k == "dose":
            return [("dose", s["v"])]
        if k == "interval":
            return [("gap", s["v"]), ("gap", s["v"] + 1)]
        if k == "maxday":
            r = t.v[b]
            out = []
            if s["v"] % r["maxd"] == 0:
                out.append(("dose", s["v"] // r["maxd"]))
            if s["v"] % r["dose"] == 0:
                out.append(("maxd", s["v"] // r["dose"]))
            return out
        if k == "mg" and (s["v"] * 50) % t.p["conc"] == 0:
            return [("dose", s["v"] * 50 // t.p["conc"])]
        return []

    def mutate(self, t, s, rng):
        bands = t.p["bands"]
        if s["kind"] == "allowed":
            return dict(s, w=rng.choice([t.p["edges"][0], t.p["edges"][0] - 1, t.p["edges"][-1] - 1, t.p["edges"][-1]]))
        lo, hi, lab = rng.choice(bands)
        return dict(s, w=rng.choice([lo, hi, (lo + hi) // 2]))

    def edges(self, t, s):
        out = {"numeric", "multi_hop"} | ({"units"} if s["kind"] == "mg" else set())
        if s["kind"] == "allowed":
            out.add("exception")
        if s["kind"] == "interval":
            out.add("quantifier")
        return out


# ------------------------------------------------------------------------------------------------ shipping (special)
SHIPBANDS = [(0, 5), (5, 10), (10, 20), (20, 50), (50, 100), (100, 200), (200, 300)]  # tenths of kg: (lo exclusive, hi inclusive)


def band_label(lo, hi):
    L, H = trim_dec(fixed(lo, 1)), trim_dec(fixed(hi, 1))
    return f"Up to {H} kg" if lo == 0 else f"Over {L} kg, up to {H} kg"


def build_shipping(rng):
    car = rng.choice(CARRIERS)
    nb = rng.randint(4, 7)
    bands = SHIPBANDS[:nb]
    nz = rng.randint(3, 5)
    cur = rng.choice(["$", "$", "£", "€"])
    ent = Ent("Weight", "weight band", "weight bands", "the {x} band")
    cols = [Col(f"z{i}", f"Zone {i}", "money", f"Zone {i} rate", pre=cur, unit_hdr=cur, dec=2, ops=[], lo=200, hi=15000, step=5)
            for i in range(1, nz + 1)]
    t = Table("shipping", f"{car} standard parcel rates{rng.choice(['', ' (2025)', ' - domestic'])}", ent, cols)
    free = rng.random() < 0.6
    thr = rng.choice([50, 60, 75, 100]) * 100
    zmax = rng.randint(1, nz - 1)
    t.p.update(bands=[(lo, hi, band_label(lo, hi)) for lo, hi in bands], free=free, thr=thr, zmax=zmax, cur=cur, nz=nz, car=car)
    t.rows = [b[2] for b in t.p["bands"]]
    base = rng.randint(250, 520)
    for i, lab in enumerate(t.rows):
        row = {}
        b = base + i * rng.randint(90, 260)
        for z in range(1, nz + 1):
            row[f"z{z}"] = int(round(b * (1 + 0.22 * (z - 1) + rng.random() * 0.05) / 5.0)) * 5
        t.v[lab] = row
    notes = [f"Parcels over {trim_dec(fixed(bands[-1][1], 1))} kg are not accepted."]
    if free:
        zs = "Zone 1" if zmax == 1 else f"Zones 1-{zmax}"
        notes.append(f"Standard shipping is free on orders of {cur}{thr // 100} or more sent to {zs}.")
    t.notes_fn = lambda t: list(notes)

    def valid(t):
        for z in range(1, nz + 1):
            col = [t.v[e][f"z{z}"] for e in t.rows]
            if any(a >= b for a, b in zip(col, col[1:])):
                return False
        return all(t.v[e]["z1"] > 0 for e in t.rows)
    t.valid = valid
    t.special = ["ship"]
    t.mkrow = None
    base_style(rng, t)
    return t


class ShipOp(Op):
    name, qa_ok = "ship", True

    def applicable(self, t):
        return t.dom == "shipping"

    def band(self, t, w):
        for lo, hi, lab in t.p["bands"]:
            if lo < w <= hi:
                return lab
        return None

    def rate(self, t, w, z):
        b = self.band(t, w)
        return None if b is None else t.v[b][f"z{z}"]

    def cost(self, t, s):
        k = s["kind"]
        if k == "rate":
            return self.rate(t, s["w"], s["z"])
        if k == "free":
            r = self.rate(t, s["w"], s["z"])
            if r is None:
                return None
            if t.p["free"] and s["ov"] >= t.p["thr"] and s["z"] <= t.p["zmax"]:
                return 0
            return r
        if k == "sum2":
            a, b = self.rate(t, s["w"], s["z"]), self.rate(t, s["w2"], s["z"])
            return None if a is None or b is None else a + b
        return None

    def wsample(self, t, rng):
        lo, hi, lab = rng.choice(t.p["bands"])
        x = rng.random()
        if x < 0.35:
            return hi
        if x < 0.5 and lo > 0:
            return lo + 1
        return rng.randint(lo + 1, hi)

    def sample(self, t, rng, want):
        if want == N:
            return None
        kind = rng.choice(["rate", "rate", "free", "sum2", "cmp2"] if t.p["free"] else ["rate", "rate", "sum2", "cmp2"])
        z = rng.randint(1, t.p["nz"])
        s = {"op": "ship", "kind": kind, "w": self.wsample(t, rng), "z": z}
        if kind == "free":
            thr = t.p["thr"]
            s["ov"] = rng.choice([thr, thr - 100, thr + rng.choice([0, 500, 1250]), thr - rng.choice([1, 50, 501])])
            s["z"] = rng.choice([t.p["zmax"], t.p["zmax"] + 1 if t.p["zmax"] < t.p["nz"] else 1, rng.randint(1, t.p["nz"])])
        if kind == "sum2":
            s["w2"] = self.wsample(t, rng)
        if kind == "cmp2":
            s["w2"] = self.wsample(t, rng)
            s["z2"] = rng.randint(1, t.p["nz"])
            if (s["w2"], s["z2"]) == (s["w"], s["z"]):
                return None
            return s if self.eval(t, s) == want else None
        x = self.cost(t, s)
        if x is None:
            return None
        if want == T:
            s["v"] = x
        else:
            w2 = self.wsample(t, rng)
            alt = [self.rate(t, w2, s["z"]), self.rate(t, s["w"], max(1, s["z"] - 1)), self.rate(t, s["w"], min(t.p["nz"], s["z"] + 1))]
            if kind == "free":
                alt += [self.rate(t, s["w"], s["z"]), 0]
            if kind == "sum2":
                alt += [2 * self.rate(t, s["w"], s["z"]), x + 100, x - 50]
            alt = [a for a in alt if a is not None and a != x and a >= 0]
            if not alt:
                return None
            s["v"] = rng.choice(alt)
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        if s["kind"] == "cmp2":
            a, b = self.rate(t, s["w"], s["z"]), self.rate(t, s["w2"], s["z2"])
            if a is None or b is None:
                return None
            return T if a > b else F
        x = self.cost(t, s)
        if x is None:
            return None
        return T if x == s["v"] else F

    def _m(self, t, v):
        if v == 0:
            return "nothing (free)"
        return f"{t.p['cur']}{fixed(v, 2)}"

    def _w(self, w):
        return trim_dec(fixed(w, 1)) + " kg"

    def text(self, t, s):
        k, tv = s["kind"], s["tv"]
        z = s["z"]
        if k == "rate":
            forms = [f"Sending a {self._w(s['w'])} parcel to Zone {z} costs {self._m(t, s['v'])}",
                     f"The standard rate for a {self._w(s['w'])} parcel to Zone {z} is {self._m(t, s['v'])}"]
        elif k == "free":
            ov = f"{t.p['cur']}{fixed(s['ov'], 2)}"
            forms = [f"Standard shipping for a {ov} order weighing {self._w(s['w'])} sent to Zone {z} costs {self._m(t, s['v'])}",
                     f"A customer whose {ov} order weighs {self._w(s['w'])} pays {self._m(t, s['v'])} for standard shipping to Zone {z}"]
        elif k == "sum2":
            forms = [f"Sending two parcels to Zone {z}, one weighing {self._w(s['w'])} and one weighing {self._w(s['w2'])}, costs {self._m(t, s['v'])} in total"]
        else:
            forms = [f"Sending a {self._w(s['w'])} parcel to Zone {z} costs more than sending a {self._w(s['w2'])} parcel to Zone {s['z2']}"]
        return cap(ch(forms, tv))

    def qa(self, t, s):
        k = s["kind"]
        if k == "rate":
            return f"How much does it cost to send a {self._w(s['w'])} parcel to Zone {s['z']} by standard post?", self._m(t, s["v"])
        if k == "sum2":
            return (f"What is the total cost of sending a {self._w(s['w'])} parcel and a {self._w(s['w2'])} parcel to Zone {s['z']}?",
                    self._m(t, s["v"]))
        if k == "free":
            ov = f"{t.p['cur']}{fixed(s['ov'], 2)}"
            return f"How much is standard shipping for a {ov} order weighing {self._w(s['w'])} sent to Zone {s['z']}?", self._m(t, s["v"])
        return None

    def cells(self, t, s):
        out = []
        for w, z in ((s["w"], s["z"]), (s.get("w2"), s.get("z2", s["z"]))):
            if w is None:
                continue
            b = self.band(t, w)
            if b:
                out.append((b, f"z{z}"))
        return out

    def consts(self, t, s):
        if "v" not in s:
            return []
        out = [(f"z{s['z']}", s["v"])]
        if s["kind"] == "sum2":
            a, b = self.rate(t, s["w"], s["z"]), self.rate(t, s["w2"], s["z"])
            if a is not None and b is not None:
                out += [(f"z{s['z']}", s["v"] - a), (f"z{s['z']}", s["v"] - b)]
        return out

    def mutate(self, t, s, rng):
        if s["kind"] == "free":
            return dict(s, ov=rng.choice([t.p["thr"], t.p["thr"] - 1, t.p["thr"] + 1000, t.p["thr"] - 1000]))
        return dict(s, w=self.wsample(t, rng))

    def edges(self, t, s):
        out = {"numeric", "multi_hop"}
        if s["kind"] == "free":
            out.add("exception")
        return out


# ------------------------------------------------------------------------------------------------ train departures
def build_trains(rng):
    stn = rng.choice(TOWNS)
    ent = Ent("Service", "service", "services", "service {x}")
    dests = rng.sample([x for x in TOWNS if x != stn], rng.randint(3, 5))
    stat = ["On time"] + [f"Delayed {m} min" for m in (2, 3, 4, 5, 6, 8, 10, 12, 15, 18, 20, 25, 30, 40)]
    arr_note = rng.random() < 0.5
    cols = [Col("dest", "To", "cat", "destination", cats=dests, sayf="runs to {X}", sayfn="does not run to {X}",
                sayp="run to {X}", filt="to {X}", nomiss=True),
            Col("dep", "Departs", "time", "scheduled departure time", tvp=("departs", "depart", "at", "pres"),
                words=("later", "earlier", "latest", "earliest", "late", "early"), above=("later than", "earlier than"),
                ops=["val", "thr", "cmp", "diff", "count", "quant", "argthen"], nomiss=True, lo=330, hi=1350, step=5),
            Col("arr", "Arrives", "time", "scheduled arrival time", tvp=("arrives", "arrive", "at", "pres"),
                words=("later", "earlier", "latest", "earliest", "late", "early"), above=("later than", "earlier than"),
                ops=["val", "thr", "cmp", "count"], nomiss=True, lo=350, hi=1435, step=1),
            Col("plat", "Platform", "cat", "platform", cats=[str(i) for i in range(1, 13)], sayf="leaves from platform {X}",
                sayfn="does not leave from platform {X}", sayp="leave from platform {X}", filt="leaving from platform {X}", nomiss=True),
            Col("status", "Status", "cat", "status", cats=stat, sayf='is shown as "{X}"', sayfn='is not shown as "{X}"',
                sayp='are shown as "{X}"', nomiss=True)]

    def delay(st):
        return 0 if st == "On time" else int(st.split()[1])
    vcols = [Col("edep", "", "time", "expected departure time", fn=vf(["dep", "status"], lambda d, st: d + delay(st)),
                 deps=["dep", "status"], words=("later", "earlier", "latest", "earliest", "late", "early"),
                 above=("later than", "earlier than"), ops=["val", "thr", "cmp", "sup", "count"]),
             Col("jt", "", "dur", "scheduled journey time", fn=vf(["dep", "arr"], lambda d, a: a - d), deps=["dep", "arr"],
                 words=("longer", "shorter", "longest", "shortest", "long", "short"), above=("longer than", "shorter than"),
                 conv=["hm"], ops=["val", "thr", "cmp", "sup", "count", "diff"], cmpnoun="scheduled journey time")]
    if arr_note:
        vcols.append(Col("earr", "", "time", "expected arrival time", fn=vf(["arr", "status"], lambda a, st: a + delay(st)),
                         deps=["arr", "status"], words=("later", "earlier", "latest", "earliest", "late", "early"),
                         above=("later than", "earlier than"), ops=["val", "thr", "cmp", "sup"]))
    t = Table("trains", f"Departures from {stn} - {fmt_date(od(2025, rng.randint(1, 12), rng.randint(1, 28)), 'wlong')}", ent, cols, vcols)

    def notes(t):
        out = ["Times are scheduled times; a delay shown in the Status column moves the expected departure later by that many minutes."]
        if arr_note:
            out.append("Delays are expected to apply to arrival times as well.")
        return out
    t.notes_fn = notes
    t.sort = lambda t: t.rows.sort(key=lambda e: (t.v[e]["dep"], e))
    t.valid = lambda t: all(330 <= t.v[e]["dep"] < t.v[e]["arr"] <= 1439 for e in t.rows)

    base_jt = {x: rng.randint(20, 150) for x in dests}

    def gen(rng, e):
        d = rstep(rng, 330, 1260, 5)
        dest = rng.choice(dests)
        return {"dest": dest, "dep": d, "arr": d + int(base_jt[dest] * rng.uniform(0.85, 1.2)), "plat": str(rng.randint(1, 12)),
                "status": "On time" if rng.random() < 0.55 else rng.choice(stat[1:])}
    codes = set()
    while len(codes) < 22:
        codes.add(f"{rng.randint(1, 9)}{rng.choice('ABCDGHKLMNPRSTW')}{rng.randint(10, 99)}")
    codes = sorted(codes)
    rng.shuffle(codes)
    n = nrows(rng, 5, 10)
    return mk(t, rng, n, codes, gen, codes[n:], partial=True, blanks=False)


# ------------------------------------------------------------------------------------------------ flights with time zones
def build_flights(rng):
    origin = rng.choice(list(CITIES))
    off0 = CITIES[origin][0]
    carrier = rng.choice(["Skylark Air", "Tern Airways", "Aurora Jet", "Meridian Air", "Coastline Airlines"])
    code = rng.choice(["VQ", "ZB", "JX", "RW", "LK", "TQ"])
    dests = rng.sample([c for c in CITIES if c != origin and CITIES[c][0] != off0], rng.randint(4, 6))
    ent = Ent("Flight", "flight", "flights", "flight {x}")
    cols = [Col("to", "To", "cat", "destination", cats=dests, sayf="flies to {X}", sayfn="does not fly to {X}", sayp="fly to {X}",
                filt="to {X}", nomiss=True),
            Col("dep", "Departs (local)", "time", "departure time", tvp=("departs", "depart", "at", "pres"),
                words=("later", "earlier", "latest", "earliest", "late", "early"), above=("later than", "earlier than"),
                ops=["val", "thr", "cmp", "sup", "count", "diff"], nomiss=True, lo=300, hi=1380, step=5),
            Col("arr", "Arrives (local)", "time", "arrival time", ops=[], nomiss=True, lo=0, hi=2879)]

    def ft(t, e):
        d, a, dest = t.get(e, "dep"), t.get(e, "arr"), t.get(e, "to")
        if None in (d, a, dest):
            return None
        return (a - CITIES[dest][0]) - (d - off0)
    ftc = Col("ft", "", "dur", "flight time", fn=ft, deps=["dep", "arr", "to"], dstyle="long", conv=["hm", "min"], w=4.0,
              words=("longer", "shorter", "longest", "shortest", "long", "short"), above=("longer than", "shorter than"),
              ops=["val", "thr", "cmp", "sup", "count", "argthen", "diff"],
              custom={"eq": ["{P} flight time is {V}", "{E} takes {V} from take-off to landing"],
                      "gt": ["{P} flight time is more than {V}", "{E} is in the air for more than {V}"],
                      "lt": ["{P} flight time is less than {V}", "{E} is in the air for less than {V}"],
                      "ge": ["{P} flight time is at least {V}"], "le": ["{P} flight time is at most {V}"],
                      "eq_neg": ["{P} flight time is not {V}"], "gt_neg": ["{E} is not in the air for more than {V}"],
                      "lt_neg": ["{E} is not in the air for less than {V}"],
                      "p_gt": ["have a flight time of more than {V}"], "p_lt": ["have a flight time of less than {V}"],
                      "p_ge": ["have a flight time of at least {V}"], "p_le": ["have a flight time of at most {V}"],
                      "p_eq": ["have a flight time of exactly {V}"],
                      "cmp_gt": ["{A} has a longer flight time than {B}", "{A} spends longer in the air than {B}"],
                      "cmp_lt": ["{A} has a shorter flight time than {B}", "{A} spends less time in the air than {B}"],
                      "cmp_ge": ["{A} spends at least as long in the air as {B}"], "cmp_le": ["{A} spends no longer in the air than {B}"],
                      "cmp_eq": ["{A} and {B} have exactly the same flight time"],
                      "cmp_gt_neg": ["{A} does not have a longer flight time than {B}"],
                      "cmp_lt_neg": ["{A} does not have a shorter flight time than {B}"],
                      "cmp_eq_neg": ["{A} and {B} do not have the same flight time"],
                      "sup_hi": ["{E} has the longest flight time{SC}"], "sup_lo": ["{E} has the shortest flight time{SC}"],
                      "sup_hi_neg": ["{E} does not have the longest flight time{SC}"],
                      "sup_lo_neg": ["{E} does not have the shortest flight time{SC}"],
                      "psup_hi": ["has the longest flight time"], "psup_lo": ["has the shortest flight time"],
                      "ptop_hi": ["have the longest flight times"], "ptop_lo": ["have the shortest flight times"],
                      "diff_dir": ["{PA} flight time is {D} longer than {PB}"], "diff_abs": ["{PA} and {PB} flight times differ by {D}"],
                      "diff_atl": ["{PA} flight time is at least {D} longer than {PB}"],
                      "q_val": ["How long is {P} flight time?"], "q_diff": ["How much longer is {PA} flight time than {PB}?"]})
    t = Table("flights", f"{carrier} departures from {origin} - {fmt_date(od(2025, rng.choice([1, 2, 3, 11, 12]), rng.randint(1, 28)), 'long_dmy')}",
              ent, cols, [ftc])
    t.p["origin"] = origin
    t.notes_fn = lambda t: ["All times are local. UTC offsets on the travel date: " + ", ".join(
        f"{c} {'+' if CITIES[c][0] >= 0 else '-'}{abs(CITIES[c][0]) // 60}:{abs(CITIES[c][0]) % 60:02d}"
        for c in [origin] + sorted({t.v[e]['to'] for e in t.rows})) + ". (+1) = next day."]

    def dist(a, b):
        import math
        la1, lo1, la2, lo2 = map(math.radians, (CITIES[a][1], CITIES[a][2], CITIES[b][1], CITIES[b][2]))
        h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
        return 2 * 6371 * math.asin(math.sqrt(h))

    def gen(rng, e):
        dest = rng.choice(dests)
        dur = int(round((dist(origin, dest) / 820 * 60 + 35 + rng.randint(-10, 20)) / 5.0)) * 5
        for _ in range(50):
            d = rstep(rng, 300, 1380, 5)
            a = d + dur + CITIES[dest][0] - off0
            if 0 <= a < 2880:
                break
        return {"to": dest, "dep": d, "arr": a}
    t.valid = lambda t: all(0 <= t.v[e]["arr"] < 2880 and 300 <= t.v[e]["dep"] < 1440 and ft(t, e) > 20 for e in t.rows)
    t.sort = lambda t: t.rows.sort(key=lambda e: (t.v[e]["dep"], e))
    codes = sorted({f"{code} {rng.randint(100, 989)}" for _ in range(30)})
    rng.shuffle(codes)
    n = rng.randint(4, 9)
    t = mk(t, rng, n, codes, gen, codes[n:], partial=False, blanks=False)
    return t if t.valid(t) else None


# ------------------------------------------------------------------------------------------------ HR
def build_hr(rng):
    org = rng.choice(["Harbourline Logistics", "Evergreen Health Trust", "Kestrel Software", "Oakhurst Council",
                      "Meridian Engineering", "Brightwater Utilities"])
    asof = od(2025, rng.randint(1, 12), rng.randint(1, 28))
    cutoff = asof - rng.randint(400, 1500)
    ent = Ent("Employee", "employee", "employees", "{x}")
    dsel = rng.sample(DEPTS, rng.randint(3, 5))
    ct = {"Permanent": ("is on a permanent contract", "is not on a permanent contract", "are on permanent contracts",
                        "are not on permanent contracts"),
          "Fixed-term": ("is on a fixed-term contract", "is not on a fixed-term contract", "are on fixed-term contracts",
                         "are not on fixed-term contracts"),
          "Contractor": ("is a contractor", "is not a contractor", "are contractors", "are not contractors")}
    allc = {
        "dept": Col("dept", "Department", "cat", "department", cats=dsel, sayf="works in {X}", sayfn="does not work in {X}",
                    sayp="work in {X}", filt="in {X}"),
        "start": Col("start", "Start date", "date", "start date", tvp=("started", "start", "on", "past"),
                     words=("later", "earlier", "latest", "earliest", "late", "early"), above=("later than", "earlier than"),
                     ops=["val", "thr", "cmp", "sup", "diff", "count", "argthen"], nomiss=True),
        "ctype": Col("ctype", "Contract", "cat", "contract type", cats=list(ct), say=ct, filt="on {X} contracts", nomiss=True),
        "leave": Col("leave", "Leave left (days)", "num", "remaining annual leave", lo=0, hi=30, gen_lo=0,
                     vp=VP("has", "have", "day of annual leave left", "days of annual leave left", cobj="annual leave left",
                           count=False, tense="pres", unit=("day", "days"))),
        "hours": Col("hours", "Hours/week", "num", "contracted weekly hours", lo=12, hi=40, sum=False, avg=True,
                     vp=VP("works", "work", "contracted hour a week", "contracted hours a week", cobj="contracted hours a week", tense="pres",
                           unit=("hour", "hours"))),
    }
    keys = ["start", "ctype"] + rng.sample(["dept", "leave", "hours"], rng.randint(1, 3))
    cols = [allc[k] for k in ["dept", "start", "ctype", "leave", "hours"] if k in keys]

    def bonus(st, c):
        return "yes" if (c == "Permanent" and st <= cutoff) else "no"

    def years(st):
        a, b = dt.date.fromordinal(st), dt.date.fromordinal(asof)
        return b.year - a.year - ((b.month, b.day) < (a.month, a.day))
    vcols = [Col("bonus", "", "bool", "bonus eligibility", cats=["yes", "no"], fn=vf(["start", "ctype"], bonus), deps=["start", "ctype"],
                 say={"yes": ("qualifies for the loyalty bonus", "does not qualify for the loyalty bonus", "qualify for the loyalty bonus",
                              "do not qualify for the loyalty bonus"),
                      "no": ("does not qualify for the loyalty bonus", "qualifies for the loyalty bonus",
                             "do not qualify for the loyalty bonus", "qualify for the loyalty bonus")},
                 ops=["catval", "catcount", "argthen"], w=5.0, exc=True),
             Col("years", "", "num", "completed years of service", fn=vf(["start"], years), deps=["start"],
                 vp=VP("has completed", "have completed", "full year of service", "full years of service",
                       cobj="full years of service", tense="pres"), ops=["val", "thr", "cmp", "count"])]
    vcols[1].vp.aux = lambda pl=False: "has" if not pl else "have"
    vcols[1].vp.base = "completed"
    t = Table("hr", f"{org} - staff list as of {fmt_date(asof, 'long_dmy')}", ent, cols, vcols)
    t.p.update(asof=asof, cutoff=cutoff)
    t.notes_fn = lambda t: [f"Loyalty bonus: permanent staff who started on or before {fmt_date(cutoff, 'long_dmy')} qualify; "
                            f"fixed-term staff and contractors do not qualify."]

    def gen(rng, e):
        x = rng.random()
        st = cutoff + rng.choice([0, 0, -1, 1]) if x < 0.25 else rng.randint(asof - 4400, asof - 30)
        if dt.date.fromordinal(st).month == 2 and dt.date.fromordinal(st).day == 29:
            st += 1
        return {"dept": rng.choice(dsel), "start": st, "ctype": rng.choice(["Permanent"] * 3 + ["Fixed-term", "Contractor"]),
                "leave": rng.randint(0, 30), "hours": rng.choice([16, 20, 24, 30, 35, 37, 40])}
    t.valid = lambda t: all(t.v[e]["start"] < asof and not (dt.date.fromordinal(t.v[e]["start"]).month == 2 and
                                                             dt.date.fromordinal(t.v[e]["start"]).day == 29) for e in t.rows)
    names = people(rng, 22)
    n = nrows(rng, 5, 10)
    return mk(t, rng, n, names, gen, names[n:])


# ------------------------------------------------------------------------------------------------ library loans
TITLE_A = ["Silent", "Glass", "Northern", "Hidden", "Last", "Winter", "Paper", "Iron", "Salt", "Hollow", "Distant", "Amber"]
TITLE_B = ["Orchard", "Harbour", "Lighthouse", "Garden", "Archive", "River", "Mountain", "Kingdom", "Letters", "Engine",
           "Meadow", "Compass"]


def build_library(rng):
    lib = rng.choice([f"{x} Public Library" for x in ("Millbrook", "Harrowby", "Glenhaven", "Denholm", "Fairhaven")])
    year = rng.choice([2024, 2025, 2026, 2024])
    start = od(year, rng.choice([1, 2, 2, 3, 11, 12]) if year != 2026 else rng.choice([1, 2]), 1)
    asof = start + rng.randint(55, 75)
    rate = rng.choice([20, 25, 50])
    cap_ = rng.choice([500, 800, 1000])
    NR = 1
    ent = Ent("Borrower", "borrower", "borrowers", "{x}")
    cols = [Col("item", "Item", "cat", "item", ops=[], nomiss=True),
            Col("out", "Borrowed", "date", "borrowing date", tvp=("borrowed the item", "borrow the item", "on", "past"),
                words=("later", "earlier", "latest", "earliest", "late", "early"), above=("later than", "earlier than"),
                ops=["val", "thr", "cmp", "sup"], nomiss=True),
            Col("due", "Due", "date", "due date", words=("later", "earlier", "latest", "earliest", "late", "early"),
                above=("later than", "earlier than"), ops=["val", "cmp"], nomiss=True),
            Col("ret", "Returned", "date", "return date", ops=[], nomiss=True, special={NR: "Not returned"})]

    def late(due, ret):
        end = asof if ret == NR else ret
        return max(0, end - due)
    vcols = [Col("late", "", "num", "number of overdue days", fn=vf(["due", "ret"], late), deps=["due", "ret"],
                 vp=VP("has", "have", "overdue day", "overdue days", cobj="overdue days", tense="pres"),
                 ops=["val", "thr", "cmp", "sup", "count", "quant", "argthen"]),
             Col("fine", "", "money", "overdue fine", pre="$", dec=2, fn=vf(["due", "ret"], lambda d, r: min(cap_, late(d, r) * rate)),
                 deps=["due", "ret"], ops=["val", "thr", "cmp", "sup", "sum", "count"], w=3.0, exc=True)]
    t = Table("library", f"{lib} - loans report as of {fmt_date(asof, 'long_dmy')}", ent, cols, vcols)
    t.p.update(asof=asof, rate=rate, cap=cap_)
    t.notes_fn = lambda t: [f"Fines: ${fixed(rate, 2)} for each day after the due date, up to a maximum of ${fixed(cap_, 2)} per loan. "
                            f"Loans not yet returned are counted up to {fmt_date(asof, 'long_dmy')}."]

    def gen(rng, e):
        o = start + rng.randint(0, 35)
        d = o + rng.choice([14, 21, 28])
        x = rng.random()
        if x < 0.2 and d < asof:
            r = NR
        else:
            r = d + rng.choice([-9, -5, -2, -1, 0, 0, 1, 2, 3, 5, 8, 12, 19, 25])
            r = max(o + 1, min(asof, r))
        return {"item": f"The {rng.choice(TITLE_A)} {rng.choice(TITLE_B)}", "out": o, "due": d, "ret": r}
    t.valid = lambda t: all(t.v[e]["out"] < t.v[e]["due"] and (t.v[e]["ret"] == NR or t.v[e]["out"] < t.v[e]["ret"] <= asof)
                            for e in t.rows)
    t.editable = ["ret", "due"]
    names = people(rng, 20)
    n = nrows(rng, 5, 9)
    return mk(t, rng, n, names, gen, names[n:], blanks=False)


# ------------------------------------------------------------------------------------------------ hotel (special: stay cost)
def build_hotel(rng):
    h = rng.choice(HOTELS)
    cur = rng.choice(["$", "€", "£"])
    ent = Ent("Room type", "room type", "room types", "the {x}")
    say_b = {"Yes": ("includes breakfast", "does not include breakfast", "include breakfast", "do not include breakfast"),
             "No": ("does not include breakfast", "includes breakfast", "do not include breakfast", "include breakfast")}
    cols = [Col("wk", "Sun-Thu night", "money", "weeknight rate", pre=cur, unit_hdr=cur, lo=60, hi=450, step=5, nomiss=True,
                ops=["val", "thr", "cmp", "sup", "diff", "count"], sum=False),
            Col("we", "Fri-Sat night", "money", "weekend rate", pre=cur, unit_hdr=cur, lo=70, hi=520, step=5, nomiss=True,
                ops=["val", "thr", "cmp", "sup", "diff", "count"], sum=False),
            Col("guests", "Max guests", "num", "maximum occupancy", lo=1, hi=6, nomiss=True, sum=False,
                vp=VP("sleeps", "sleep", "guest", "guests", tense="pres", cobj="guests")),
            Col("bfast", "Breakfast included", "bool", "breakfast", cats=["Yes", "No"], say=say_b, nomiss=True)]
    t = Table("hotel", f"{h} - room rates{rng.choice(['', ' (per room, per night)', ' - 2025 season'])}", ent, cols)
    disc = rng.random() < 0.5
    k, p = rng.choice([5, 6, 7]), rng.choice([10, 20])
    t.p.update(disc=disc, k=k, p=p, cur=cur)
    t.notes_fn = lambda t: ["Weekend rates apply to Friday and Saturday nights; every other night is charged at the Sun-Thu rate."] + \
        ([f"Stays of {k} nights or more get {p}% off the total room charge."] if disc else [])

    def gen(rng, e):
        spec = next(x for x in ROOMS if x[0] == e)
        wk = rstep(rng, spec[1], spec[2], 5)
        return {"wk": wk, "we": wk + rstep(rng, 0, 90, 5), "guests": spec[3], "bfast": rng.choice(["Yes", "No"])}
    t.valid = lambda t: all(t.v[e]["we"] >= t.v[e]["wk"] for e in t.rows)
    t.special = ["stay"]
    names, rest = pick(rng, [x[0] for x in ROOMS], rng.randint(4, 8), 3)
    return mk(t, rng, len(names), names, gen, rest, partial=False, blanks=False)


class StayOp(Op):
    name, qa_ok = "stay", True

    def applicable(self, t):
        return t.dom == "hotel"

    def cost(self, t, room, day, n):
        r = t.v[room]
        tot = 0
        for i in range(n):
            wd = (day + i) % 7
            tot += r["we"] if wd in (4, 5) else r["wk"]
        tot *= 100  # cents
        if t.p["disc"] and n >= t.p["k"]:
            tot = tot * (100 - t.p["p"]) // 100
        return tot

    def sample(self, t, rng, want):
        if want == N:
            return None
        room = rng.choice(t.rows)
        day = rng.randrange(7)
        n = rng.choice([1, 2, 2, 3, 3, 4, 5, t.p["k"], t.p["k"] - 1, t.p["k"] + 1])
        kind = rng.choice(["cost", "cost", "cost", "cmp"])
        s = {"op": "stay", "kind": kind, "e": room, "day": day, "n": n}
        if kind == "cmp":
            others = [x for x in t.rows if x != room]
            s["b"] = rng.choice(others)
            return s if self.eval(t, s) == want else None
        x = self.cost(t, room, day, n)
        if want == T:
            s["v"] = x
        else:
            r = t.v[room]
            alts = [r["wk"] * n * 100, r["we"] * n * 100, self.cost(t, room, (day + 1) % 7, n), self.cost(t, room, day, n + 1)]
            if t.p["disc"] and n >= t.p["k"]:
                alts.append(sum((r["we"] if (day + i) % 7 in (4, 5) else r["wk"]) for i in range(n)) * 100)
            alts = [a for a in alts if a != x and a > 0]
            if not alts:
                return None
            s["v"] = rng.choice(alts)
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        x = self.cost(t, s["e"], s["day"], s["n"])
        if s["kind"] == "cmp":
            y = self.cost(t, s["b"], s["day"], s["n"])
            return T if x < y else F
        return T if x == s["v"] else F

    def _m(self, t, v):
        return f"{t.p['cur']}{fixed(v // 100, 0) if v % 100 == 0 else fixed(v, 2)}"

    def text(self, t, s):
        n, tv = s["n"], s["tv"]
        E = t.ent.r(s["e"])
        nights = f"{n}-night stay" if n > 1 else "one-night stay"
        a_ = art(str(n)) if n > 1 else "a"
        d = WEEKDAYS[s["day"]]
        if s["kind"] == "cmp":
            B = t.ent.r(s["b"])
            return cap(ch([f"{a_} {nights} in {E} checking in on {d} costs less than the same stay in {B}",
                           f"Checking in on {d} for {n} night{'s' if n > 1 else ''}, {E} is cheaper than {B}"], tv))
        V = self._m(t, s["v"])
        return cap(ch([f"{a_} {nights} in {E} checking in on {d} costs {V} in total",
                       f"Checking in on {d} and staying {n} night{'s' if n > 1 else ''}, a guest in {E} pays {V} for the room"], tv))

    def qa(self, t, s):
        if s["kind"] != "cost":
            return None
        n = s["n"]
        return (f"What is the total room charge for {n} night{'s' if n > 1 else ''} in {t.ent.r(s['e'])}, checking in on {WEEKDAYS[s['day']]}?",
                self._m(t, s["v"]))

    def cells(self, t, s):
        out = [(s["e"], "wk"), (s["e"], "we")]
        if s["kind"] == "cmp":
            out += [(s["b"], "wk"), (s["b"], "we")]
        return out

    def consts(self, t, s):
        return []

    def mutate(self, t, s, rng):
        return dict(s, day=(s["day"] + rng.choice([1, 2, 3, 6])) % 7) if rng.random() < 0.5 else \
            dict(s, n=max(1, s["n"] + rng.choice([-1, 1])))

    def edges(self, t, s):
        out = {"numeric", "multi_hop", "temporal"}
        if t.p["disc"]:
            out.add("exception")
        return out


# ------------------------------------------------------------------------------------------------ phone plans
def build_plans(rng):
    tel = rng.choice(TELCOS)
    ent = Ent("Plan", "plan", "plans", "the {x} plan")
    fee_on = rng.random() < 0.5
    fee = rng.choice([1000, 1500, 2500, 3000])
    say5 = {"Yes": ("includes 5G access", "does not include 5G access", "include 5G access", "do not include 5G access"),
            "No": ("does not include 5G access", "includes 5G access", "do not include 5G access", "include 5G access")}
    cols = [Col("price", "Monthly price", "money", "monthly price", pre="$", unit_hdr="$", dec=2, lo=800, hi=9500, nomiss=True,
                sum_all=False),
            Col("data", "Data (GB)", "num", "monthly data allowance", lo=1, hi=150, unl=True, sum=False, avg=False,
                vp=VP("includes", "include", "GB of data", "GB of data", cobj="data", count=False, tense="pres", unit=("GB", "GB")),
                ops=["thr", "cmp", "sup", "count", "quant"], nomiss=True),
            Col("mins", "Minutes", "num", "monthly minutes", lo=100, hi=3000, step=50, unl=True, sum=False, avg=False,
                vp=VP("includes", "include", "minute", "minutes", cobj="minutes", tense="pres"),
                ops=["thr", "cmp", "sup", "count", "quant"], nomiss=True),
            Col("term", "Contract (months)", "num", "contract length", lo=1, hi=36, sum=False, nomiss=True,
                ops=["val", "thr", "cmp", "count", "quant"]),
            Col("g5", "5G", "bool", "5G access", cats=["Yes", "No"], say=say5, nomiss=True)]

    def total(pr, m):
        return pr * m + (fee if (fee_on and m == 1) else 0)
    vcols = [Col("tot", "", "money", "total cost over the full contract", pre="$", dec=2, fn=vf(["price", "term"], total),
                 deps=["price", "term"], ops=["val", "thr", "cmp", "sup", "count", "argthen"], cmpnoun="total contract cost",
                 w=3.0, exc=fee_on)]
    t = Table("plans", f"{tel} - mobile plans{rng.choice(['', ' (prices per month)', ' - current offers'])}", ent, cols, vcols)
    t.notes_fn = lambda t: ["Unlimited = no cap on usage."] + \
        ([f"A one-time setup fee of ${fixed(fee, 2)} applies to plans with a 1-month contract."] if fee_on else [])
    t.p.update(fee_on=fee_on, fee=fee)

    def gen(rng, e):
        return {"price": rng.randint(8, 95) * 100 - rng.choice([1, 1, 5, 0]),
                "data": INF if rng.random() < 0.25 else rng.choice([1, 2, 5, 8, 10, 15, 20, 30, 40, 50, 75, 100, 150]),
                "mins": INF if rng.random() < 0.4 else rng.choice([100, 250, 500, 750, 1000, 1500, 2000, 3000]),
                "term": rng.choice([1, 1, 12, 12, 18, 24, 24, 36]), "g5": rng.choice(["Yes", "No"])}
    t.special = []
    names, rest = pick(rng, PLANS, rng.randint(4, 8), 3)
    return mk(t, rng, len(names), names, gen, rest, partial=False, blanks=False)


# ------------------------------------------------------------------------------------------------ car rental (special: cost)
def build_rental(rng):
    co = rng.choice(RENTALS)
    ent = Ent("Car class", "car class", "car classes", "the {xl}")
    fuel_say = {"Petrol": ("runs on petrol", "does not run on petrol", "run on petrol", "do not run on petrol"),
                "Diesel": ("runs on diesel", "does not run on diesel", "run on diesel", "do not run on diesel"),
                "Hybrid": ("is a hybrid", "is not a hybrid", "are hybrids", "are not hybrids"),
                "Electric": ("is fully electric", "is not fully electric", "are fully electric", "are not fully electric")}
    cols = [Col("rate", "Daily rate", "money", "daily rate", pre="$", unit_hdr="$", dec=2, lo=2500, hi=19000, step=100, nomiss=True,
                sum_all=False),
            Col("seats", "Seats", "num", "number of seats", lo=2, hi=12, sum=False, nomiss=True,
                vp=VP("seats", "seat", "person", "people", tense="pres", cobj="people")),
            Col("bags", "Large bags", "num", "luggage capacity", lo=1, hi=8, sum=False, nomiss=True,
                vp=VP("fits", "fit", "large bag", "large bags", tense="pres", cobj="large bags")),
            Col("fuel", "Fuel", "cat", "fuel type", cats=list(fuel_say), say=fuel_say, filt="that {X}", nomiss=True)]
    cols[3].filt = None
    t = Table("rental", f"{co} - car classes and daily rates", ent, cols)
    k, p = rng.choice([5, 7, 7, 10]), rng.choice([10, 20, 25])
    t.p.update(k=k, p=p)
    t.notes_fn = lambda t: [f"Rentals of {k} days or more get {p}% off the daily rate."]

    def gen(rng, e):
        spec = next(x for x in CARS if x[0] == e)
        return {"rate": rstep(rng, spec[1] * 100, spec[2] * 100, 100), "seats": spec[3], "bags": rng.randint(spec[4], spec[5]),
                "fuel": "Electric" if "Electric" in e else ("Hybrid" if "Hybrid" in e else rng.choice(["Petrol", "Diesel", "Hybrid"]))}
    t.special = ["rent"]
    names, rest = pick(rng, [x[0] for x in CARS], rng.randint(4, 8), 3)
    return mk(t, rng, len(names), names, gen, rest, partial=False, blanks=False)


class RentOp(Op):
    name, qa_ok = "rent", True

    def applicable(self, t):
        return t.dom == "rental"

    def cost(self, t, e, d):
        r = t.v[e]["rate"] * d
        if d >= t.p["k"]:
            r = r * (100 - t.p["p"]) // 100
        return r

    def sample(self, t, rng, want):
        if want == N:
            return None
        e = rng.choice(t.rows)
        k = t.p["k"]
        d = rng.choice([1, 2, 3, 4, k - 1, k, k, k + 1, k + 3])
        kind = rng.choice(["cost", "cost", "cost", "cmp"])
        s = {"op": "rent", "kind": kind, "e": e, "d": d}
        if kind == "cmp":
            s["b"] = rng.choice([x for x in t.rows if x != e])
            s["d2"] = rng.choice([d, d + 1, d - 1, k]) or 1
            if s["d2"] < 1:
                return None
            return s if self.eval(t, s) == want else None
        x = self.cost(t, e, d)
        if want == T:
            s["v"] = x
        else:
            alts = [t.v[e]["rate"] * d, self.cost(t, e, d + 1), self.cost(t, e, max(1, d - 1)),
                    t.v[e]["rate"] * d * (100 - t.p["p"]) // 100]
            alts = [a for a in alts if a != x]
            if not alts:
                return None
            s["v"] = rng.choice(alts)
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        x = self.cost(t, s["e"], s["d"])
        if s["kind"] == "cmp":
            return T if x > self.cost(t, s["b"], s["d2"]) else F
        return T if x == s["v"] else F

    def text(self, t, s):
        E = t.ent.r(s["e"])
        d, tv = s["d"], s["tv"]
        days = f"{d} day{'s' if d > 1 else ''}"
        if s["kind"] == "cmp":
            B = t.ent.r(s["b"])
            d2 = f"{s['d2']} day{'s' if s['d2'] > 1 else ''}"
            return cap(ch([f"Renting {E} for {days} costs more than renting {B} for {d2}"], tv))
        V = f"${fixed(s['v'], 2)}"
        return cap(ch([f"Renting {E} for {days} costs {V}", f"{art(str(d))} {d}-day rental of {E} costs {V} in total"], tv))

    def qa(self, t, s):
        if s["kind"] != "cost":
            return None
        return f"How much does it cost to rent {t.ent.r(s['e'])} for {s['d']} day{'s' if s['d'] > 1 else ''}?", f"${fixed(s['v'], 2)}"

    def cells(self, t, s):
        return [(s["e"], "rate")] + ([(s["b"], "rate")] if s["kind"] == "cmp" else [])

    def consts(self, t, s):
        if s["kind"] != "cost":
            return []
        d = s["d"]
        fac = (100 - t.p["p"]) if d >= t.p["k"] else 100
        num = s["v"] * 100
        den = d * fac
        return [("rate", num // den)] if num % den == 0 else []

    def mutate(self, t, s, rng):
        return dict(s, d=max(1, s["d"] + rng.choice([-1, 1, 2])))

    def edges(self, t, s):
        return {"numeric", "exception", "multi_hop"}


# ------------------------------------------------------------------------------------------------ budget (special)
def build_budget(rng):
    org = rng.choice(["Harrowby City Council", "Northfield University", "Evergreen Health Trust", "Kestrel Software",
                      "Brightwater Utilities", "Glenhaven School District"])
    yr = rng.choice(["2024", "2025", "2024-25"])
    cur = rng.choice(["$", "£", "€"])
    ent = Ent("Department", "department", "departments", rng.choice(["the {x} department", "{x}"]))
    sc = rng.random() < 0.35
    if sc:  # figures in thousands; claims state full amounts
        cols = [Col("bud", "Budget", "money", "budget", pre=cur, unit_hdr=f"{cur}000s", force_hdr=True, scale=1000, lo=20, hi=900,
                    nomiss=True, avg=False),
                Col("act", "Actual spend", "money", "actual spending", pre=cur, unit_hdr=f"{cur}000s", force_hdr=True, scale=1000,
                    lo=15, hi=1000, nomiss=True, mass=True, avg=False)]
    else:
        cols = [Col("bud", "Budget", "money", "budget", pre=cur, unit_hdr=cur, lo=20000, hi=900000, step=1000, nomiss=True),
                Col("act", "Actual spend", "money", "actual spending", pre=cur, unit_hdr=cur, lo=15000, hi=1000000, step=100, nomiss=True, mass=True)]
    cols = cols + [
            Col("head", "Headcount", "num", "headcount", lo=3, hi=60, vp=VP("has", "have", "employee", "employees", tense="pres",
                                                                          cobj="employees"))]
    if rng.random() < 0.5:
        cols = cols[:2]
    t_scale = 1000 if sc else 1
    t = Table("budget", f"{org} - budget vs actual spending, {yr}", ent, cols)
    t.p["cur"] = cur
    t.p["scale"] = t_scale

    def gen(rng, e):
        if sc:
            b = rng.randint(20, 900)
            x = rng.random()
            a = b if x < 0.1 else max(5, int(b * rng.uniform(0.78, 1.18)))
            return {"bud": b, "act": a, "head": rng.randint(3, 60)}
        b = rstep(rng, 20000, 900000, 1000)
        x = rng.random()
        a = b if x < 0.1 else int(b * rng.uniform(0.78, 1.18)) // 100 * 100
        return {"bud": b, "act": max(100, a), "head": rng.randint(3, 60)}
    t.special = ["budget"]
    names, rest = pick(rng, DEPTS, nrows(rng, 5, 10), 4)
    return mk(t, rng, len(names), names, gen, rest, partial=False, blanks=False)


class BudgetOp(Op):
    name, qa_ok = "budget", True

    def applicable(self, t):
        return t.dom == "budget"

    def sample(self, t, rng, want):
        if want == N:
            return None
        kind = rng.choice(["over", "within", "by", "share", "share", "maxover"])
        e = rng.choice(t.rows)
        b, a = t.v[e]["bud"], t.v[e]["act"]
        s = {"op": "budget", "kind": kind, "e": e}
        if kind == "by":
            unit = 100 if t.p["scale"] == 1 else 1
            if a <= b:
                if want == T:
                    return None
                s["v"] = b - a if a < b else rng.choice([unit, 10 * unit])
            else:
                s["v"] = (a - b) if want == T else rng.choice([a - b + unit, a - b - unit, a - b + 10 * unit, a - b + 5 * unit])
            if s["v"] <= 0:
                return None
        if kind == "share":
            s["rel"] = rng.choice(["lt", "ge", "gt", "le"])
            ratio = Fr(a * 100, b)
            cands = [int(ratio), int(ratio) + 1, 90, 95, 100, 105, 110, 80, 85]
            if ratio.denominator == 1:
                cands += [int(ratio)] * 3
            rng.shuffle(cands)
            for pct in cands:
                if 50 <= pct <= 150 and self.eval(t, dict(s, pct=pct)) == want:
                    s["pct"] = pct
                    break
            else:
                return None
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        k = s["kind"]
        b, a = t.v[s["e"]]["bud"], t.v[s["e"]]["act"]
        if k == "over":
            return T if a > b else F
        if k == "within":
            return T if a <= b else F
        if k == "by":
            return T if a - b == s["v"] else F
        if k == "share":
            return T if holds(Fr(a * 100, b), s["rel"], s["pct"]) else F
        if k == "maxover":
            over = {e: t.v[e]["act"] - t.v[e]["bud"] for e in t.rows}
            m = max(over.values())
            if m <= 0:
                return None
            top = [e for e, x in over.items() if x == m]
            if len(top) > 1:
                return None
            return T if top[0] == s["e"] else F
        return None

    def text(self, t, s):
        E = t.ent.r(s["e"])
        k, tv = s["kind"], s["tv"]
        cur = t.p["cur"]
        if k == "over":
            return cap(ch([f"{E} spent more than its budget", f"{E} went over budget"], tv))
        if k == "within":
            return cap(ch([f"{E} stayed within its budget", f"{E} did not spend more than its budget"], tv))
        if k == "by":
            amt = f"{cur}{s['v'] * t.p['scale']:,}"
            return cap(ch([f"{E} went over budget by exactly {amt}", f"{E} overspent its budget by {amt}"], tv))
        if k == "share":
            w = {"lt": "less than", "ge": "at least", "gt": "more than", "le": "at most"}[s["rel"]]
            return cap(ch([f"{E} spent {w} {s['pct']}% of its budget"], tv))
        return cap(ch([f"{E} went over budget by the largest amount", f"Of all the {t.ent.pl}, {E} overspent by the most"], tv))

    def qa(self, t, s):
        if s["kind"] == "by":
            return f"By how much did {t.ent.r(s['e'])} go over its budget?", f"{t.p['cur']}{s['v'] * t.p['scale']:,}"
        if s["kind"] == "maxover":
            return f"Which {t.ent.sg} went over budget by the largest amount?", s["e"]
        return None

    def cells(self, t, s):
        if s["kind"] == "maxover":
            return [(e, k) for e in t.rows for k in ("bud", "act")]
        return [(s["e"], "bud"), (s["e"], "act")]

    def consts(self, t, s):
        b, a = t.v[s["e"]]["bud"], t.v[s["e"]]["act"]
        u = 100 if t.p["scale"] == 1 else 1
        if s["kind"] == "by":
            return [("act", b + s["v"]), ("bud", a - s["v"])]
        if s["kind"] in ("over", "within"):
            return [("act", b), ("act", b + u), ("bud", a), ("bud", a - 10 * u)]
        if s["kind"] == "share":
            x = Fr(b * s["pct"], 100)
            return [("act", int(x) // u * u), ("act", (int(x) // u + 1) * u)] + ([("act", int(x))] if x.denominator == 1 else [])
        return []

    def mutate(self, t, s, rng):
        if s["kind"] == "share":
            return dict(s, pct=s["pct"] + rng.choice([-5, 5, -1, 1]))
        if s["kind"] == "by":
            u = 100 if t.p["scale"] == 1 else 1
            return dict(s, v=max(u, s["v"] + rng.choice([-10 * u, 10 * u, u])))
        return dict(s, e=rng.choice([x for x in t.rows if x != s["e"]]))

    def edges(self, t, s):
        return {"numeric", "multi_hop"} | ({"negation"} if s["kind"] == "within" else set()) | \
            ({"units"} if t.p["scale"] != 1 and s["kind"] == "by" else set())


# ------------------------------------------------------------------------------------------------ weather
def build_weather(rng):
    reg = rng.choice(["Coastal district", "Upland region", "Northern valleys", "Lake country", "Southern plains"])
    month = rng.randint(1, 12)
    day = od(2025, month, rng.randint(1, 28))
    season_base = [-2, 0, 4, 9, 14, 18, 21, 20, 16, 10, 5, 1][month - 1] + rng.randint(-4, 4)
    ent = Ent("Town", "town", "towns", "{x}")
    allc = {
        "hi": Col("hi", "High", "num", "daytime high", suf="°C", unit_hdr="°C", nonneg=False, lo=-15, hi=42, sum=False,
                  avg=True, domain_lo=-10 ** 9),
        "lo": Col("lo", "Low", "num", "overnight low", suf="°C", unit_hdr="°C", nonneg=False, lo=-25, hi=32, sum=False,
                  domain_lo=-10 ** 9),
        "rain": Col("rain", "Rainfall", "num", "rainfall", dec=1, suf=" mm", unit_hdr="mm", lo=0, hi=480, conv=["cm"], mass=True, sum=False,
                    gen_lo=0, custom={"cmp_gt": ["{A} had more rain than {B}"], "cmp_lt": ["{A} had less rain than {B}"],
                                      "sup_hi": ["{E} had the most rain{SC}", "{E} was the wettest {SG}{SC}"],
                                      "sup_lo": ["{E} had the least rain{SC}"], "psup_hi": ["had the most rain"],
                                      "psup_lo": ["had the least rain"], "ptop_hi": ["had the most rain"],
                                      "ptop_lo": ["had the least rain"]}),
        "wind": Col("wind", "Max gust", "num", "strongest wind gust", suf=" km/h", unit_hdr="km/h", lo=5, hi=120, sum=False),
        "sun": Col("sun", "Sunshine", "num", "sunshine", dec=1, suf=" h", unit_hdr="hours", lo=0, hi=150, gen_lo=0, sum=False,
                   vp=VP("had", "have", "hour of sunshine", "hours of sunshine", cobj="sunshine", count=False, unit=("hour", "hours"))),
    }
    for c in allc.values():
        for k, v in list(c.custom.items()):
            c.custom[k] = [x.replace("{SG}", "town") for x in v]
    keys = ["hi", "lo"] + rng.sample(["rain", "wind", "sun"], rng.randint(1, 3))
    cols = [allc[k] for k in keys]
    frost = {"yes": ("dropped below freezing overnight", "did not drop below freezing overnight",
                     "dropped below freezing overnight", "did not drop below freezing overnight"),
             "no": ("did not drop below freezing overnight", "dropped below freezing overnight",
                    "did not drop below freezing overnight", "dropped below freezing overnight")}
    vcols = [Col("rng", "", "num", "temperature range (high minus low)", suf="°C", fn=vf(["hi", "lo"], lambda h, l: h - l),
                 deps=["hi", "lo"], ops=["val", "thr", "cmp", "sup", "count", "argthen"], cmpnoun="temperature range"),
             Col("frost", "", "bool", "frost", cats=["yes", "no"], fn=vf(["lo"], lambda l: "yes" if l < 0 else "no"), deps=["lo"],
                 say=frost, ops=["catval", "catcount"])]
    t = Table("weather", f"{reg}: weather observations for {fmt_date(day, 'wlong')}", ent, cols, vcols)
    t.notes_fn = lambda t: ["Below freezing means below 0°C."] if any(t.v[e].get("lo") is not None and t.v[e]["lo"] <= 1 for e in t.rows) else []

    def gen(rng, e):
        h = season_base + rng.randint(-6, 8)
        return {"hi": h, "lo": h - rng.randint(2, 14), "rain": 0 if rng.random() < 0.3 else rng.randint(1, 350),
                "wind": rng.randint(8, 95), "sun": rng.randint(0, 140)}
    t.valid = lambda t: all(t.v[e].get("hi") is None or t.v[e].get("lo") is None or t.v[e]["hi"] >= t.v[e]["lo"] for e in t.rows)
    names, rest = pick(rng, TOWNS, nrows(rng, 5, 10), 8)
    return mk(t, rng, len(names), names, gen, rest)


# ------------------------------------------------------------------------------------------------ nutrition
def build_nutrition(rng):
    src = rng.choice(["Canteen menu", "Snack shelf", "Breakfast options", "Meal-prep planner", "Pantry staples"])
    ent = Ent("Food", "food", "foods", "{x}")
    def vp(o, c):
        return VP("has", "have", f"g of {o} per serving", f"g of {o} per serving", cobj=f"{c} per serving", count=False, tense="pres",
                  unit=("g", "g"))
    allc = {
        "serv": Col("serv", "Serving", "num", "serving size", suf=" g", unit_hdr="g", lo=20, hi=260, sum=False, nomiss=True),
        "kcal": Col("kcal", "Energy", "num", "energy per serving", suf=" kcal", unit_hdr="kcal", lo=20, hi=500, sum_all=False,
                    vp=VP("has", "have", "calorie per serving", "calories per serving", cobj="calories per serving", tense="pres",
                          unit=("calorie", "calories"))),
        "prot": Col("prot", "Protein", "num", "protein per serving", dec=1, suf=" g", unit_hdr="g", lo=0, hi=500, vp=vp("protein", "protein"),
                    sum_all=False),
        "sug": Col("sug", "Sugar", "num", "sugar per serving", dec=1, suf=" g", unit_hdr="g", lo=0, hi=500, vp=vp("sugar", "sugar"),
                   sum_all=False),
        "fat": Col("fat", "Fat", "num", "fat per serving", dec=1, suf=" g", unit_hdr="g", lo=0, hi=500, vp=vp("fat", "fat"), sum_all=False),
        "fib": Col("fib", "Fibre", "num", "fibre per serving", dec=1, suf=" g", unit_hdr="g", lo=0, hi=300, vp=vp("fibre", "fibre"),
                   sum_all=False),
    }
    keys = ["serv"] + rng.sample(["kcal", "prot", "sug", "fat", "fib"], rng.randint(2, 4))
    cols = [allc[k] for k in keys]
    vcols = []
    for k in keys[1:]:
        if k == "kcal":
            continue
        nm = {"prot": "protein", "sug": "sugar", "fat": "fat", "fib": "fibre"}[k]
        vcols.append(Col(k + "100", "", "num", f"{nm} per 100 g", dec=1,
                         fn=vf([k, "serv"], lambda x, sv: Fr(x * 100, sv) if sv > 0 else None), deps=[k, "serv"],
                         vp=VP("has", "have", f"g of {nm} per 100 g", f"g of {nm} per 100 g", cobj=f"{nm} per 100 g",
                               count=False, tense="pres", unit=("g", "g")), ops=["thr", "cmp", "sup", "count"], units_edge=True))
    t = Table("nutrition", f"{src} - nutrition per serving", ent, cols, vcols)
    t.notes_fn = lambda t: ["All nutrient values are per serving of the size shown."]

    def gen(rng, e):
        spec = next(x for x in FOODS if x[0] == e)
        sv = max(10, int(spec[1] * rng.uniform(0.85, 1.15)))
        f = lambda per100: max(0, int(round(per100 * sv / 10 * rng.uniform(0.9, 1.1))))
        return {"serv": sv, "kcal": max(1, int(round(spec[2] * sv / 100 * rng.uniform(0.92, 1.08)))), "prot": f(spec[3]),
                "sug": f(spec[4]), "fat": f(spec[5]), "fib": f(spec[6])}
    t.valid = lambda t: all(t.v[e]["serv"] >= 10 for e in t.rows)
    names, rest = pick(rng, [x[0] for x in FOODS], nrows(rng, 5, 9), 6)
    return mk(t, rng, len(names), names, gen, rest)


# ------------------------------------------------------------------------------------------------ race results
def build_race(rng):
    ev = rng.choice(["marathon", "10K", "half marathon"])
    town = rng.choice(TOWNS)
    ent = Ent("Runner", "runner", "runners", "{x}")
    lo, hi = {"marathon": (7600, 17000), "10K": (1700, 4200), "half marathon": (3700, 8400)}[ev]
    groups = ["18-34", "35-44", "45-54", "55+"]
    tcust = {"eq": ["{E} finished in {V}", "{P} finishing time was {V}"], "lt": ["{E} finished in under {V}", "{E} ran faster than {V}"],
             "gt": ["{E} took longer than {V}", "{P} finishing time was over {V}"], "le": ["{E} finished in {V} or less"],
             "ge": ["{E} took {V} or longer"], "eq_neg": ["{E} did not finish in {V}"], "lt_neg": ["{E} did not finish in under {V}"],
             "gt_neg": ["{E} did not take longer than {V}"],
             "p_eq": ["finished in exactly {V}"], "p_lt": ["finished in under {V}"], "p_gt": ["took longer than {V}"],
             "p_le": ["finished in {V} or less"], "p_ge": ["took {V} or longer"],
             "cmp_lt": ["{A} finished ahead of {B}", "{A} ran a faster time than {B}"],
             "cmp_gt": ["{A} finished behind {B}", "{A} ran a slower time than {B}"],
             "cmp_le": ["{A} finished no later than {B}"], "cmp_ge": ["{A} finished no earlier than {B}"],
             "cmp_eq": ["{A} and {B} finished in exactly the same time"],
             "cmp_lt_neg": ["{A} did not finish ahead of {B}"], "cmp_gt_neg": ["{A} did not finish behind {B}"],
             "cmp_eq_neg": ["{A} and {B} did not finish in the same time"],
             "sup_lo": ["{E} ran the fastest time{SC}", "{E} was the fastest runner{SC}"], "sup_hi": ["{E} ran the slowest time{SC}"],
             "sup_lo_neg": ["{E} did not run the fastest time{SC}"], "sup_hi_neg": ["{E} did not run the slowest time{SC}"],
             "psup_lo": ["ran the fastest time"], "psup_hi": ["ran the slowest time"],
             "ptop_lo": ["ran the fastest times"], "ptop_hi": ["ran the slowest times"],
             "rank_lo": ["{E} finished {O}{SC}", "{E} took {O} place{SC}"], "rank_hi": ["{E} ran the {O}-slowest time{SC}"],
             "diff_dir": ["{A} finished {D} behind {B}"], "diff_atl": ["{A} finished at least {D} behind {B}"],
             "diff_abs": ["{A} and {B} finished {D} apart"],
             "q_val": ["What was {P} finishing time?"], "q_diff": ["How far behind {B} did {A} finish?"]}
    cols = [Col("time", "Time", "dur", "finishing time", durfmt="hms", lo=lo, hi=hi, conv=["words"], nomiss=True, sum=False,
                avg=False, words=("slower", "faster", "slowest", "fastest", "slow", "fast"), custom=tcust),
            Col("ctry", "Country", "cat", "country", cats=COUNTRIES, sayf="is from {X}", sayfn="is not from {X}", sayp="are from {X}",
                filt="from {X}", nomiss=True),
            Col("grp", "Age group", "cat", "age group", cats=groups, sayf="ran in the {X} age group", sayfn="did not run in the {X} age group",
                sayp="ran in the {X} age group", filt="in the {X} age group", nomiss=True)]
    t = Table("race", f"{town} {ev} {rng.choice([2024, 2025])} - results", ent, cols)
    cs = rng.sample(COUNTRIES, rng.randint(3, 6))

    def gen(rng, e):
        return {"time": rng.randint(lo, hi), "ctry": rng.choice(cs), "grp": rng.choice(groups)}
    t.sort = lambda t: t.rows.sort(key=lambda e: (t.v[e]["time"], e))
    names = people(rng, 24)
    n = nrows(rng, 6, 12)
    return mk(t, rng, n, names, gen, names[n:], blanks=False)


# ------------------------------------------------------------------------------------------------ grants (special + missing)
def build_grants(rng):
    fund = rng.choice(["Community Fund", "Small Grants Programme", "Neighbourhood Fund", "Arts & Heritage Fund"])
    town = rng.choice(TOWNS)
    cur = rng.choice(["$", "£", "€"])
    ent = Ent("Applicant", "applicant", "applicants", "{x}")
    cats = ["Arts", "Sport", "Environment", "Education", "Community"]
    cols = [Col("req", "Requested", "money", "amount requested", pre=cur, unit_hdr=cur, lo=5000, hi=80000, step=500, nomiss=True),
            Col("awd", "Awarded", "money", "amount awarded", pre=cur, unit_hdr=cur, lo=0, hi=80000, step=500, gen_lo=0),
            Col("cat", "Category", "cat", "category", cats=cats, sayf="applied under {X}", sayfn="did not apply under {X}",
                sayp="applied under {X}", filt="in the {X} category", nomiss=True)]
    t = Table("grants", f"{town} {fund} - {rng.choice(['spring', 'autumn', 'annual'])} round {rng.choice([2024, 2025])}", ent, cols)
    t.p["cur"] = cur

    def gen(rng, e):
        r = rstep(rng, 5000, 80000, 500)
        x = rng.random()
        a = r if x < 0.3 else (0 if x < 0.45 else (r // 2 // 500 * 500 if x < 0.55 else rstep(rng, 500, r, 500)))
        return {"req": r, "awd": a, "cat": rng.choice(cats)}
    t.valid = lambda t: all(t.v[e]["awd"] is None or t.v[e]["awd"] <= t.v[e]["req"] for e in t.rows)
    t.special = ["grant"]
    names = [f"{rng.choice(TOWNS).split()[0]} {g}" for g in rng.sample(GRANTEES, 12)]
    names = list(dict.fromkeys(names))
    n = min(len(names) - 2, nrows(rng, 5, 9))
    t = mk(t, rng, n, names, gen, names[n:], partial=True, blanks=False)
    t.style["miss"], t.style["miss_note"] = "Pending", "Pending = decision not yet made."
    for e in t.rows:
        if rng.random() < 0.12:
            t.v[e]["awd"] = None
    return t


class GrantOp(Op):
    name, qa_ok, n_ok = "grant", True, True

    def applicable(self, t):
        return t.dom == "grants"

    def sample(self, t, rng, want):
        kind = rng.choice(["half", "full", "none", "short", "short"])
        if want == N:
            ents = [e for e in t.rows if t.v[e]["awd"] is None] or [rng.choice(t.rows)]
            e = rng.choice(ents)
            t.v[e]["awd"] = None
        else:
            ents = [e for e in t.rows if t.v[e]["awd"] is not None]
            if not ents:
                return None
            e = rng.choice(ents)
        s = {"op": "grant", "kind": kind, "e": e}
        r, a = t.v[e]["req"], t.v[e]["awd"]
        if kind == "short":
            if a is None:
                s["v"] = rng.choice([r // 2 // 500 * 500, 5000, 2500]) or 500
            elif want == T:
                if a == r:
                    return None
                s["v"] = r - a
            else:
                s["v"] = rng.choice([r - a + 500, max(500, r - a - 500), r, a]) if a != r else rng.choice([500, 1000])
            if s["v"] <= 0:
                return None
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        r, a = t.v[s["e"]]["req"], t.v[s["e"]]["awd"]
        if a is None:
            return N
        k = s["kind"]
        if k == "half":
            return T if 2 * a >= r else F
        if k == "full":
            return T if a == r else F
        if k == "none":
            return T if a == 0 else F
        if k == "short":
            return T if (r - a == s["v"] and a > 0) else F
        return None

    def text(self, t, s):
        E = t.ent.r(s["e"])
        k, tv = s["kind"], s["tv"]
        if k == "half":
            return cap(ch([f"{E} was awarded at least half of the amount it requested", f"{E} received at least 50% of its request"], tv))
        if k == "full":
            return cap(ch([f"{E} received the full amount it asked for", f"{E} was awarded everything it requested"], tv))
        if k == "none":
            return cap(ch([f"{E} was awarded nothing", f"{E}'s application received no money"], tv))
        return cap(ch([f"{E} was awarded {t.p['cur']}{s['v']:,} less than it requested"], tv))

    def qa(self, t, s):
        return None

    def cells(self, t, s):
        return [(s["e"], "awd"), (s["e"], "req")]

    def consts(self, t, s):
        r = t.v[s["e"]]["req"]
        out = [("awd", r), ("awd", r // 2 // 500 * 500), ("awd", (r // 2 // 500 + 1) * 500), ("awd", 0)]
        if s["kind"] == "short":
            out.append(("awd", r - s["v"]))
        return out

    def mutate(self, t, s, rng):
        return None

    def edges(self, t, s):
        out = {"numeric"}
        if t.v[s["e"]]["awd"] is None:
            out.add("missing_info")
        if s["kind"] == "none":
            out.add("negation")
        return out


# ------------------------------------------------------------------------------------------------ appointments
def build_appts(rng):
    clinic = rng.choice(["Riverside Health Centre", "Oakhurst Family Practice", "Harbour Physiotherapy", "Northcote Dental Clinic"])
    day = od(2025, rng.randint(1, 12), rng.randint(1, 28))
    ent = Ent("Patient", "appointment", "appointments", "the appointment for {x}")
    clin = rng.sample(CLINICIANS, rng.randint(2, 3))
    typ = {"In person": ("is an in-person appointment", "is not an in-person appointment", "are in-person appointments", "are not in-person appointments"),
           "Video": ("is a video appointment", "is not a video appointment", "are video appointments", "are not video appointments"),
           "Phone": ("is a phone appointment", "is not a phone appointment", "are phone appointments", "are not phone appointments")}
    lcust = {"cmp_gt": ["{A} lasts longer than {B}"], "cmp_lt": ["{A} is shorter than {B}"], "cmp_eq": ["{A} and {B} are the same length"],
             "cmp_ge": ["{A} lasts at least as long as {B}"], "cmp_le": ["{A} lasts no longer than {B}"],
             "cmp_gt_neg": ["{A} does not last longer than {B}"], "cmp_lt_neg": ["{A} is not shorter than {B}"],
             "cmp_eq_neg": ["{A} and {B} are not the same length"],
             "sup_hi": ["{E} is the longest appointment{SC}"], "sup_lo": ["{E} is the shortest appointment{SC}"],
             "sup_hi_neg": ["{E} is not the longest appointment{SC}"], "sup_lo_neg": ["{E} is not the shortest appointment{SC}"],
             "psup_hi": ["is the longest"], "psup_lo": ["is the shortest"], "ptop_hi": ["are the longest"], "ptop_lo": ["are the shortest"],
             "diff_dir": ["{A} lasts {D} longer than {B}"], "diff_atl": ["{A} lasts at least {D} longer than {B}"],
             "diff_abs": ["{A} and {B} differ in length by {D}"], "q_diff": ["How much longer does {A} last than {B}?"]}
    cols = [Col("clin", "Clinician", "cat", "clinician", cats=clin, sayf="is with {X}", sayfn="is not with {X}", sayp="are with {X}",
                filt="with {X}", nomiss=True),
            Col("start", "Start", "time", "start time", tvp=("starts", "start", "at", "pres"),
                words=("later", "earlier", "latest", "earliest", "late", "early"), above=("later than", "earlier than"),
                ops=["val", "thr", "cmp", "sup", "count"], nomiss=True, lo=480, hi=1080, step=5),
            Col("len", "Length", "dur", "length", unit_hdr="min", lo=10, hi=60, step=5, nomiss=True, sum=True, avg=False, conv=["hm"],
                vp=VP("lasts", "last", "", "", tense="pres", cobj="time", count=False), custom=lcust,
                ops=["val", "thr", "cmp", "sup", "count"]),
            Col("type", "Type", "cat", "appointment type", cats=list(typ), say=typ, nomiss=True)]
    vcols = [Col("end", "", "time", "end time", fn=vf(["start", "len"], lambda s_, l_: s_ + l_), deps=["start", "len"],
                 tvp=("ends", "end", "at", "pres"), words=("later", "earlier", "latest", "earliest", "late", "early"),
                 above=("later than", "earlier than"), ops=["val", "thr", "cmp", "sup", "count"])]
    t = Table("appts", f"{clinic} - appointments for {fmt_date(day, 'wlong')}", ent, cols, vcols)
    t.sort = lambda t: t.rows.sort(key=lambda e: (t.v[e]["start"], e))

    nxt = {c: rstep(rng, 480, 600, 5) for c in clin}

    def gen(rng, e):
        c = rng.choice(clin)
        ln = rng.choice([10, 15, 15, 20, 30, 30, 45, 60])
        st = min(1080, nxt[c] + rng.choice([0, 0, 5, 10, 15, 30, 45]))
        nxt[c] = st + ln
        return {"clin": c, "start": st, "len": ln, "type": rng.choice(list(typ))}

    def valid(t):
        for c in clin:
            iv = sorted((t.v[e]["start"], t.v[e]["start"] + t.v[e]["len"]) for e in t.rows if t.v[e]["clin"] == c)
            if any(b[0] < a[1] for a, b in zip(iv, iv[1:])):
                return False
        return all(420 <= t.v[e]["start"] <= 1140 and 5 <= t.v[e]["len"] <= 90 for e in t.rows)
    t.valid = valid
    t.special = ["overlap"]
    names = people(rng, 18)
    n = nrows(rng, 5, 10)
    t = mk(t, rng, n, names, gen, names[n:], partial=False, blanks=False)
    return t if valid(t) else None


class OverlapOp(Op):
    name = "overlap"

    def applicable(self, t):
        return t.dom == "appts"

    def sample(self, t, rng, want):
        if want == N:
            return None
        srt = sorted(t.rows, key=lambda e: t.v[e]["start"])
        pairs = [(x, y) for i, x in enumerate(srt) for y in srt[i + 1:i + 4] if t.v[x]["clin"] != t.v[y]["clin"]]
        if not pairs:
            return None
        a, b = rng.choice(pairs)
        if rng.random() < 0.5:
            a, b = b, a
        s = {"op": "overlap", "a": a, "b": b}
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        sa, la = t.v[s["a"]]["start"], t.v[s["a"]]["len"]
        sb, lb = t.v[s["b"]]["start"], t.v[s["b"]]["len"]
        return T if (sa < sb + lb and sb < sa + la) else F

    def text(self, t, s):
        A, B = t.ent.r(s["a"]), t.ent.r(s["b"])
        return cap(ch([f"{A} overlaps with {B}", f"{A} and {B} overlap in time"], s["tv"]))

    def cells(self, t, s):
        return [(s["a"], "start"), (s["a"], "len"), (s["b"], "start"), (s["b"], "len")]

    def consts(self, t, s):
        sa, la = t.v[s["a"]]["start"], t.v[s["a"]]["len"]
        sb, lb = t.v[s["b"]]["start"], t.v[s["b"]]["len"]
        return [("start", sb - la), ("start", sa + la), ("start", sb + lb), ("start", sa - lb), ("len", sb - sa), ("len", sa - sb)]

    def mutate(self, t, s, rng):
        return None

    def edges(self, t, s):
        return {"temporal", "multi_hop", "numeric"}


# ------------------------------------------------------------------------------------------------ league position (special)
class PosOp(Op):
    name, qa_ok = "position", True

    def applicable(self, t):
        return t.dom == "standings"

    def order(self, t):
        key = lambda e: (3 * t.v[e]["W"] + t.v[e]["D"], t.v[e]["GF"] - t.v[e]["GA"], t.v[e]["GF"])
        srt = sorted(t.rows, key=key, reverse=True)
        keys = [key(e) for e in srt]
        return srt, keys

    def sample(self, t, rng, want):
        if want == N:
            return None
        srt, keys = self.order(t)
        kind = rng.choice(["pos", "pos", "above"])
        if kind == "pos":
            i = rng.randrange(len(srt))
            s = {"op": "position", "kind": "pos", "e": srt[i], "k": i + 1 if want == T else i + 1 + rng.choice([-1, 1])}
            if s["k"] < 1 or s["k"] > len(srt):
                return None
        else:
            i = rng.randrange(len(srt) - 1)
            a, b = srt[i], srt[i + 1]
            if want == F:
                a, b = b, a
            s = {"op": "position", "kind": "above", "e": a, "b": b}
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        srt, keys = self.order(t)
        i = srt.index(s["e"])
        if (i > 0 and keys[i - 1] == keys[i]) or (i + 1 < len(keys) and keys[i + 1] == keys[i]):
            return None
        if s["kind"] == "pos":
            return T if i + 1 == s["k"] else F
        j = srt.index(s["b"])
        if keys[j] == keys[i]:
            return None
        return T if i < j else F

    def text(self, t, s):
        E = s["e"]
        tv = s["tv"]
        if s["kind"] == "pos":
            o = ordw(s["k"])
            return cap(ch([f"{E} is {o} in the table", f"{E} occupies {o} place in the table",
                           f"{E} sits in {o} position once the ranking rules are applied"], tv))
        return cap(ch([f"{E} is placed above {s['b']} in the table", f"{E} ranks higher in the table than {s['b']}"], tv))

    def qa(self, t, s):
        if s["kind"] != "pos":
            return None
        return f"In which position is {s['e']} in the table?", ordn(s["k"])

    def cells(self, t, s):
        return [(e, k) for e in t.rows for k in ("W", "D", "GF", "GA")]

    def consts(self, t, s):
        return []

    def mutate(self, t, s, rng):
        if s["kind"] == "pos":
            ks = [k for k in (s["k"] - 1, s["k"] + 1) if 1 <= k <= len(t.rows)]
            return dict(s, k=rng.choice(ks)) if ks else None
        return dict(s, e=s["b"], b=s["e"])

    def edges(self, t, s):
        return {"multi_hop", "numeric"} | ({"implicit"} if "Pts" not in [c.key for c in t.cols] else set())


# ------------------------------------------------------------------------------------------------ time series (special)
def build_series(rng):
    kind = rng.choice(["orders", "visitors", "kwh", "revenue", "members"])
    per = rng.choice(["m1", "m2", "q", "y"])
    if per == "m1":
        P = MONTHS[:rng.randint(4, 6)]
        unit, yr = "month", rng.choice([2024, 2025])
    elif per == "m2":
        P = MONTHS[6:6 + rng.randint(4, 6)]
        unit, yr = "month", rng.choice([2024, 2025])
    elif per == "q":
        P, unit, yr = ["Q1", "Q2", "Q3", "Q4"], "quarter", rng.choice([2024, 2025])
    else:
        y0 = rng.choice([2018, 2019, 2020])
        P, unit, yr = [str(y0 + i) for i in range(rng.randint(4, 6))], "year", None
    abbr = per in ("m1", "m2") and rng.random() < 0.5
    hdr = [p[:3] if abbr else p for p in P]
    if kind == "orders":
        ent = Ent("Product line", "product line", "product lines", "the {x} line")
        names_pool, title = LINES, "Online orders by product line"
        mk_vp = lambda p: VP("received", "receive", "order", "orders", suffix=f" in {p}", pp="received")
        noun, dec, pre, suf, uh, lo, hi = "number of orders", 0, "", "", None, 200, 9000
    elif kind == "visitors":
        ent = Ent("Museum", "museum", "museums", "the {x}")
        names_pool, title = MUSEUMS, "Visitor numbers by museum"
        mk_vp = lambda p: VP("welcomed", "welcome", "visitor", "visitors", suffix=f" in {p}", pp="welcomed")
        noun, dec, pre, suf, uh, lo, hi = "number of visitors", 0, "", "", None, 1500, 60000
    elif kind == "kwh":
        ent = Ent("Building", "building", "buildings", "{x}")
        names_pool, title = BUILDINGS, "Electricity use by building (kWh)"
        mk_vp = lambda p: VP("used", "use", "kWh", "kWh", cobj="electricity", count=False, suffix=f" in {p}", pp="used",
                             unit=("kWh", "kWh"))
        noun, dec, pre, suf, uh, lo, hi = "electricity use", 0, "", "", None, 800, 26000
    elif kind == "revenue":
        ent = Ent("Division", "division", "divisions", "the {x} division")
        names_pool, title = DIVISIONS, "Revenue by division ($ millions)"
        mk_vp = lambda p: VP("earned", "earn", "", "", cobj="revenue", count=False, suffix=f" in {p}", pp="earned")
        noun, dec, pre, suf, uh, lo, hi = "revenue", 1, "$", " million", None, 15, 950
    else:
        ent = Ent("Branch", "branch", "branches", "the {x} branch")
        names_pool, title = STREETS, "Gym membership by branch"
        mk_vp = lambda p: VP("had", "have", "member", "members", suffix=f" in {p}", pp="had")
        noun, dec, pre, suf, uh, lo, hi = "number of members", 0, "", "", None, 150, 4200
    cols = []
    for p, h in zip(P, hdr):
        pl = f"{p} {yr}" if (yr and per != "q") else (f"{p} {yr}" if yr else p)
        c = Col("p_" + p, h, "money" if kind == "revenue" else "num", f"{noun} in {pl}", dec=dec, pre=pre, suf=suf,
                lo=lo, hi=hi, vp=mk_vp(pl), cmpnoun=f"{noun} in {pl}", force_hdr=(kind == "revenue"),
                ops=["val", "thr", "cmp", "sup", "count", "quant", "sum", "diff", "rank"])
        cols.append(c)
    freq = {"month": "monthly", "quarter": "quarterly", "year": "yearly"}[unit]
    t = Table("series", f"{title} - {freq} figures" + (f", {yr}" if yr else ""), ent, cols)
    if kind == "revenue":
        t.p["money_m"] = True
    t.p.update(P=P, unit=unit, yr=yr, kind=kind, noun=noun, dec=dec)

    def gen(rng, e):
        v = rng.randint(lo, hi)
        r = {}
        for p in P:
            r["p_" + p] = max(1, v)
            v = int(v * rng.uniform(0.82, 1.22)) if rng.random() > 0.1 else v
        return r
    t.special = ["series"]
    names, rest = pick(rng, names_pool, rng.randint(4, 7), 2)
    return mk(t, rng, len(names), names, gen, rest, partial=False)


class SeriesOp(Op):
    name, qa_ok = "series", True

    def applicable(self, t):
        return t.dom == "series"

    def _pl(self, t, p):
        yr = t.p["yr"]
        return f"{p} {yr}" if yr else p

    def _v(self, t, e, p):
        return t.get(e, "p_" + p)

    def sample(self, t, rng, want):
        if want == N:
            return None
        P = t.p["P"]
        e = rng.choice(t.rows)
        if any(self._v(t, e, p) is None for p in P):
            return None
        kind = rng.choice(["cmp", "trend", "trend", "pct", "pct", "peak", "total", "count"])
        s = {"op": "series", "kind": kind, "e": e}
        if kind == "cmp":
            i, j = sorted(rng.sample(range(len(P)), 2))
            s.update(p1=P[i], p2=P[j], rel=rng.choice(["gt", "lt"]))
        elif kind == "trend":
            i = rng.randrange(len(P) - 2)
            j = rng.randrange(i + 2, len(P))
            s.update(p1=P[i], p2=P[j], dirn=rng.choice(["up", "down", "never_down", "never_up"]))
        elif kind == "pct":
            i, j = sorted(rng.sample(range(len(P)), 2))
            a, b = self._v(t, e, P[i]), self._v(t, e, P[j])
            ch_ = Fr((b - a) * 100, a)
            base = abs(int(ch_))
            pct = rng.choice([base, base + 1, max(1, base - 1), 5, 10, 15, 20, 25])
            if pct <= 0:
                return None
            s.update(p1=P[i], p2=P[j], dirn="up" if b >= a else "down", rel=rng.choice(["gt", "ge", "lt"]), pct=pct)
            if rng.random() < 0.2:
                s["dirn"] = "down" if s["dirn"] == "up" else "up"
        elif kind == "peak":
            s.update(p=rng.choice(P), hi=rng.random() < 0.7)
        elif kind == "total":
            if t.p["kind"] == "members":
                return None
            i = rng.randrange(len(P) - 1)
            j = rng.randrange(i + 1, len(P))
            s.update(p1=P[i], p2=P[j])
            tot = sum(self._v(t, e, p) for p in P[i:j + 1])
            s["v"] = tot if want == T else rng.choice([tot + self._v(t, e, P[j]) if j + 1 < len(P) else tot + 10,
                                                        tot - self._v(t, e, P[i]), tot + 10, tot - 100, tot + 1])
            if s["v"] <= 0:
                return None
        else:
            vals = [self._v(t, e, p) for p in P]
            c = rng.choice(vals)
            k = sum(v > c for v in vals)
            s.update(c=c, n=k if want == T else k + rng.choice([-1, 1]))
            if s["n"] < 0:
                return None
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        P = t.p["P"]
        e, k = s["e"], s["kind"]
        vals = {p: self._v(t, e, p) for p in P}
        if any(v is None for v in vals.values()):
            return None
        if k == "cmp":
            return T if holds(vals[s["p2"]], s["rel"], vals[s["p1"]]) else F
        if k == "trend":
            i, j = P.index(s["p1"]), P.index(s["p2"])
            seq = [vals[p] for p in P[i:j + 1]]
            pairs = list(zip(seq, seq[1:]))
            d = s["dirn"]
            ok = {"up": all(b > a for a, b in pairs), "down": all(b < a for a, b in pairs),
                  "never_down": all(b >= a for a, b in pairs), "never_up": all(b <= a for a, b in pairs)}[d]
            return T if ok else F
        if k == "pct":
            a, b = vals[s["p1"]], vals[s["p2"]]
            chg = Fr((b - a) * 100, a)
            if s["dirn"] == "down":
                chg = -chg
            if chg <= 0 and s["rel"] == "lt":
                return None  # 'fell by less than p%' presupposes that it fell
            return T if holds(chg, s["rel"], s["pct"]) else F
        if k == "peak":
            m = max(vals.values()) if s["hi"] else min(vals.values())
            ps = [p for p in P if vals[p] == m]
            if len(ps) > 1:
                return None
            return T if ps[0] == s["p"] else F
        if k == "total":
            i, j = P.index(s["p1"]), P.index(s["p2"])
            return T if sum(vals[p] for p in P[i:j + 1]) == s["v"] else F
        if k == "count":
            return T if sum(v > s["c"] for v in vals.values()) == s["n"] else F
        return None

    def _fmt(self, t, v):
        c = t.cols[0]
        if t.p.get("money_m"):
            return f"${fixed(v, 1)} million"
        x = fixed(v, 0)
        if c.vp:
            return x + c.vp.obj(1 if v == 1 else 2)
        return x

    def _meas(self, t):
        return {"orders": "orders", "visitors": "visitor numbers", "kwh": "electricity use", "revenue": "revenue",
                "members": "membership"}[t.p["kind"]]

    def text(self, t, s):
        E = t.ent.r(s["e"])
        P = self._pl
        k, tv = s["kind"], s["tv"]
        m = self._meas(t)
        unit = t.p["unit"]
        if k == "cmp":
            w = "higher" if s["rel"] == "gt" else "lower"
            return cap(ch([f"{poss(E)} {m} {'were' if m.endswith('s') and m != 'visitor numbers' else 'was'} {w} in {P(t, s['p2'])} than in {P(t, s['p1'])}".replace("visitor numbers was", "visitor numbers were"),
                           f"{E} had {w} {m} in {P(t, s['p2'])} than in {P(t, s['p1'])}"], tv))
        if k == "trend":
            d = s["dirn"]
            ph = {"up": f"rose every {unit}", "down": f"fell every {unit}", "never_down": f"never fell from one {unit} to the next",
                  "never_up": f"never rose from one {unit} to the next"}[d]
            return cap(f"{poss(E)} {m} {ph} between {P(t, s['p1'])} and {P(t, s['p2'])}")
        if k == "pct":
            w = {"gt": "by more than", "ge": "by at least", "lt": "by less than"}[s["rel"]]
            v = "grew" if s["dirn"] == "up" else "fell"
            return cap(ch([f"{poss(E)} {m} {v} {w} {s['pct']}% from {P(t, s['p1'])} to {P(t, s['p2'])}",
                           f"From {P(t, s['p1'])} to {P(t, s['p2'])}, {poss(E)} {m} {v} {w} {s['pct']}%"], tv))
        if k == "peak":
            if s["hi"]:
                return cap(ch([f"{poss(E)} {m} peaked in {P(t, s['p'])}", f"{E} recorded its highest {m} in {P(t, s['p'])}"], tv))
            return cap(f"{poss(E)} {m} {'were' if m == 'visitor numbers' else 'was'} at {'their' if m == 'visitor numbers' else 'its'} lowest in {P(t, s['p'])}")
        if k == "total":
            tn = {"orders": "orders", "visitors": "visitors", "kwh": "electricity use", "revenue": "revenue"}[t.p["kind"]]
            return cap(ch([f"{poss(E)} total {tn} from {P(t, s['p1'])} to {P(t, s['p2'])} inclusive came to {self._fmt(t, s['v'])}"], tv))
        n = s["n"]
        return cap(f"{poss(E)} {m} {'were' if m == 'visitor numbers' else 'was'} above {self._fmt(t, s['c'])} in exactly "
                   f"{n} of the {len(t.p['P'])} {unit}s shown")

    def qa(self, t, s):
        if s["kind"] == "total":
            E = t.ent.r(s["e"])
            tn = {"orders": "number of orders", "visitors": "number of visitors", "kwh": "electricity use",
                  "revenue": "revenue"}[t.p["kind"]]
            return (f"What was {poss(E)} total {tn} from {self._pl(t, s['p1'])} to {self._pl(t, s['p2'])} inclusive?",
                    self._fmt(t, s["v"]))
        if s["kind"] == "peak" and s["hi"]:
            E = t.ent.r(s["e"])
            return f"In which {t.p['unit']} did {poss(E)} {self._meas(t)} peak?", self._pl(t, s["p"])
        return None

    def cells(self, t, s):
        return [(s["e"], "p_" + p) for p in t.p["P"]]

    def consts(self, t, s):
        out = []
        if s["kind"] == "count":
            out += [("p_" + p, s["c"]) for p in t.p["P"]] + [("p_" + p, s["c"] + 1) for p in t.p["P"]]
        if s["kind"] == "pct":
            a = self._v(t, s["e"], s["p1"])
            sign = 1 if s["dirn"] == "up" else -1
            x = Fr(a * (100 + sign * s["pct"]), 100)
            out += [("p_" + s["p2"], int(x)), ("p_" + s["p2"], int(x) + 1), ("p_" + s["p2"], int(x) - 1)]
        if s["kind"] == "total":
            P = t.p["P"]
            i, j = P.index(s["p1"]), P.index(s["p2"])
            tot = sum(self._v(t, s["e"], p) for p in P[i:j + 1])
            out += [("p_" + p, self._v(t, s["e"], p) + s["v"] - tot) for p in P[i:j + 1]]
        return out

    def mutate(self, t, s, rng):
        if s["kind"] == "pct":
            return dict(s, pct=s["pct"] + rng.choice([-2, -1, 1, 2, 5]))
        if s["kind"] == "total":
            return dict(s, v=s["v"] + rng.choice([-10, 10, 1, -1, 100]))
        if s["kind"] == "count":
            return dict(s, n=max(0, s["n"] + rng.choice([-1, 1])))
        if s["kind"] == "peak":
            return dict(s, p=rng.choice([p for p in t.p["P"] if p != s["p"]]))
        return None

    def edges(self, t, s):
        out = {"numeric", "temporal"}
        if s["kind"] in ("trend", "count"):
            out.add("quantifier")
        if s["kind"] in ("pct", "total", "trend"):
            out.add("multi_hop")
        if s["kind"] == "trend" and s["dirn"].startswith("never"):
            out.add("negation")
        return out


SPECIAL = {o.name: o for o in (DoseOp(), ShipOp(), StayOp(), RentOp(), BudgetOp(), GrantOp(), OverlapOp(), PosOp(), SeriesOp())}

BUILDERS = {"retail": (build_retail, 8), "inventory": (build_inventory, 6), "price": (build_price, 6),
            "standings": (build_standings, 6), "players": (build_players, 4), "grades": (build_grades, 6),
            "dosing": (build_dosing, 5), "shipping": (build_shipping, 5), "trains": (build_trains, 5),
            "flights": (build_flights, 4), "hr": (build_hr, 5), "library": (build_library, 5), "hotel": (build_hotel, 4),
            "plans": (build_plans, 4), "rental": (build_rental, 4), "budget": (build_budget, 4), "weather": (build_weather, 5),
            "nutrition": (build_nutrition, 4), "race": (build_race, 4), "grants": (build_grants, 3), "appts": (build_appts, 3),
            "series": (build_series, 7)}
