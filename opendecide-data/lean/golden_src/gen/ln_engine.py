"""Logic engine + shared lexicon for gen_logic_negation (CPU only, deterministic, no model calls).

Every generated row carries a small logical form of what its text says (premises) and of what its question asks
(goal).  `decide` enumerates every world (bool atoms x small integer variables) consistent with the premises and
returns
    "T"  the goal is true in every such world      (the text guarantees it)
    "F"  the goal is false in every such world     (the text rules it out)
    "U"  the text leaves it open
    "X"  the premises are inconsistent (always a bug)
The generator's gold label for a row is "yes" iff decide(...) == "T"; for question types whose definition has no
"not enough information" reading the generator additionally asserts the answer is determined (T or F).  The
template code computes its own intended label by a separate path, and the two must agree for every row.

Formula syntax (tuples or JSON lists):
    "atom"                             boolean atom
    True / False
    ("not", f) ("and", f, ...) ("or", f, ...) ("imp", a, b) ("iff", a, b) ("xor", a, b)
    ("count", rel, k, [f, ...])        number of true fs  rel  k        (rel in >=, <=, ==, !=, >, <)
    ("cmp", t1, rel, t2)               integer terms: int | "var" | ("mul", c, t) | ("add", t, t)
Integer variables are declared per row as {"name": [lo, hi]} (inclusive).
"""
import itertools

REL = {">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b, "==": lambda a, b: a == b,
       "!=": lambda a, b: a != b, ">": lambda a, b: a > b, "<": lambda a, b: a < b}


def _is_node(f):
    return isinstance(f, (list, tuple))


def _atoms(f, acc, ints):
    if isinstance(f, bool):
        return
    if isinstance(f, str):
        if f in ints:
            raise ValueError(f"int var used as atom: {f}")
        acc.add(f)
        return
    op = f[0]
    if op == "count":
        for g in f[3]:
            _atoms(g, acc, ints)
    elif op == "cmp":
        for t in (f[1], f[3]):
            _term_vars(t, ints)
    else:
        for g in f[1:]:
            _atoms(g, acc, ints)


def _term_vars(t, ints):
    if isinstance(t, bool):
        raise ValueError("bool in int term")
    if isinstance(t, int):
        return
    if isinstance(t, str):
        if t not in ints:
            raise ValueError(f"undeclared int var {t}")
        return
    if t[0] == "mul":
        _term_vars(t[2], ints)
    elif t[0] == "add":
        _term_vars(t[1], ints)
        _term_vars(t[2], ints)
    else:
        raise ValueError(t)


def _val(t, w):
    if isinstance(t, int):
        return t
    if isinstance(t, str):
        return w[t]
    if t[0] == "mul":
        return t[1] * _val(t[2], w)
    return _val(t[1], w) + _val(t[2], w)


def ev(f, w):
    if isinstance(f, bool):
        return f
    if isinstance(f, str):
        return w[f]
    op = f[0]
    if op == "not":
        return not ev(f[1], w)
    if op == "and":
        return all(ev(g, w) for g in f[1:])
    if op == "or":
        return any(ev(g, w) for g in f[1:])
    if op == "imp":
        return (not ev(f[1], w)) or ev(f[2], w)
    if op == "iff":
        return ev(f[1], w) == ev(f[2], w)
    if op == "xor":
        return ev(f[1], w) != ev(f[2], w)
    if op == "count":
        n = sum(1 for g in f[3] if ev(g, w))
        return REL[f[1]](n, f[2])
    if op == "cmp":
        return REL[f[2]](_val(f[1], w), _val(f[3], w))
    raise ValueError(op)


def decide(prem, goal, ints=None, max_free=12):
    ints = ints or {}
    acc = set()
    for p in prem:
        _atoms(p, acc, ints)
    _atoms(goal, acc, ints)
    fixed, rest = {}, []
    for p in prem:
        if isinstance(p, str):
            if fixed.get(p) is False:
                return "X"
            fixed[p] = True
        elif _is_node(p) and p[0] == "not" and isinstance(p[1], str):
            if fixed.get(p[1]) is True:
                return "X"
            fixed[p[1]] = False
        else:
            rest.append(p)
    free = sorted(acc - set(fixed))
    assert len(free) <= max_free, ("too many free atoms", free)
    inames = sorted(ints)
    doms = [range(ints[n][0], ints[n][1] + 1) for n in inames]
    seen_t = seen_f = False
    for bits in itertools.product((False, True), repeat=len(free)):
        w = dict(fixed)
        w.update(zip(free, bits))
        for iv in itertools.product(*doms):
            w.update(zip(inames, iv))
            if all(ev(p, w) for p in rest):
                if ev(goal, w):
                    seen_t = True
                else:
                    seen_f = True
                if seen_t and seen_f:
                    return "U"
    if not (seen_t or seen_f):
        return "X"
    return "T" if seen_t else "F"


def to_json(f):
    if isinstance(f, (list, tuple)):
        return [to_json(g) for g in f]
    if isinstance(f, dict):
        return {k: to_json(v) for k, v in f.items()}
    return f


# ------------------------------------------------------------------------------------------------ formula helpers
def NOT(f):
    return ("not", f)


def AND(*fs):
    return ("and",) + tuple(fs)


def OR(*fs):
    return ("or",) + tuple(fs)


def IMP(a, b):
    return ("imp", a, b)


def IFF(a, b):
    return ("iff", a, b)


def CNT(rel, k, fs):
    return ("count", rel, k, list(fs))


def CMP(a, rel, b):
    return ("cmp", a, rel, b)


def lit(atom, val):
    return atom if val else ("not", atom)


# ------------------------------------------------------------------------------------------------ text helpers
NUMW = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def cap(s):
    return s[:1].upper() + s[1:]


def low(s):
    return s[:1].lower() + s[1:] if not s[:2].isupper() else s


def nw(n):
    """Number as a word for 0..20, else digits."""
    return NUMW[n] if 0 <= n <= 20 else f"{n:,}"


def nmix(n, rng, p_word=0.5):
    return NUMW[n] if 0 <= n <= 12 and rng.random() < p_word else f"{n:,}"


def join(xs, conj="and"):
    xs = list(xs)
    if not xs:
        return ""
    if len(xs) == 1:
        return xs[0]
    if len(xs) == 2:
        return f"{xs[0]} {conj} {xs[1]}"
    return ", ".join(xs[:-1]) + f" {conj} " + xs[-1]


def art(w):
    return ("an " if w[:1].lower() in "aeiou" else "a ") + w


# name, subject pronoun, object pronoun, possessive (he/she only, so present-tense agreement never breaks)
PEOPLE = [
    ("Amara", "she", "her", "her"), ("Bilal", "he", "him", "his"), ("Chen Wei", "he", "him", "his"),
    ("Daniela", "she", "her", "her"), ("Emeka", "he", "him", "his"), ("Farah", "she", "her", "her"),
    ("Gustavo", "he", "him", "his"), ("Hana", "she", "her", "her"), ("Ibrahim", "he", "him", "his"),
    ("Jolene", "she", "her", "her"), ("Kenji", "he", "him", "his"), ("Leilani", "she", "her", "her"),
    ("Mateo", "he", "him", "his"), ("Nadia", "she", "her", "her"), ("Oluwaseun", "he", "him", "his"),
    ("Priya", "she", "her", "her"), ("Quentin", "he", "him", "his"), ("Rosa", "she", "her", "her"),
    ("Sipho", "he", "him", "his"), ("Tamar", "she", "her", "her"), ("Umar", "he", "him", "his"),
    ("Valentina", "she", "her", "her"), ("Wojtek", "he", "him", "his"), ("Ximena", "she", "her", "her"),
    ("Yusuf", "he", "him", "his"), ("Zanele", "she", "her", "her"), ("Aarav", "he", "him", "his"),
    ("Brigid", "she", "her", "her"), ("Carlos", "he", "him", "his"), ("Dilnoza", "she", "her", "her"),
    ("Eero", "he", "him", "his"), ("Fatima", "she", "her", "her"), ("Giorgos", "he", "him", "his"),
    ("Halima", "she", "her", "her"), ("Isaac", "he", "him", "his"), ("Jia Hui", "she", "her", "her"),
    ("Kwame", "he", "him", "his"), ("Lucia", "she", "her", "her"), ("Marcus", "he", "him", "his"),
    ("Noor", "she", "her", "her"), ("Oskar", "he", "him", "his"), ("Paloma", "she", "her", "her"),
    ("Rahul", "he", "him", "his"), ("Svetlana", "she", "her", "her"), ("Tomasz", "he", "him", "his"),
    ("Uzma", "she", "her", "her"), ("Viktor", "he", "him", "his"), ("Yara", "she", "her", "her"),
    ("Zeke", "he", "him", "his"), ("Aiyana", "she", "her", "her"), ("Bongani", "he", "him", "his"),
    ("Céline", "she", "her", "her"), ("Dmitri", "he", "him", "his"), ("Esperanza", "she", "her", "her"),
    ("Finn", "he", "him", "his"), ("Grace", "she", "her", "her"), ("Hamza", "he", "him", "his"),
    ("Ingrid", "she", "her", "her"), ("Javier", "he", "him", "his"), ("Keiko", "she", "her", "her"),
    ("Liam", "he", "him", "his"), ("Mei", "she", "her", "her"), ("Nikolai", "he", "him", "his"),
    ("Olga", "she", "her", "her"), ("Pedro", "he", "him", "his"), ("Rania", "she", "her", "her"),
    ("Stefan", "he", "him", "his"), ("Thandiwe", "she", "her", "her"), ("Tariq", "he", "him", "his"),
    ("Ulla", "she", "her", "her"), ("Vikram", "he", "him", "his"), ("Winifred", "she", "her", "her"),
    ("Xavier", "he", "him", "his"), ("Yetunde", "she", "her", "her"), ("Zoltan", "he", "him", "his"),
    ("Anika", "she", "her", "her"), ("Benedikt", "he", "him", "his"), ("Chiara", "she", "her", "her"),
    ("Deshawn", "he", "him", "his"), ("Elif", "she", "her", "her"), ("Felipe", "he", "him", "his"),
    ("Gulnara", "she", "her", "her"), ("Hiroshi", "he", "him", "his"), ("Imani", "she", "her", "her"),
    ("Jakob", "he", "him", "his"), ("Maya", "she", "her", "her"), ("Tobias", "he", "him", "his"),
    ("Ayesha", "she", "her", "her"), ("Diego", "he", "him", "his"), ("Nomvula", "she", "her", "her"),
    ("Arjun", "he", "him", "his"), ("Freya", "she", "her", "her"), ("Kofi", "he", "him", "his"),
    ("Linh", "she", "her", "her"), ("Mohammed", "he", "him", "his"), ("Sofia", "she", "her", "her"),
    ("Ravi", "he", "him", "his"), ("Beatriz", "she", "her", "her"), ("Callum", "he", "him", "his"),
    ("Dagny", "she", "her", "her"), ("Ezra", "he", "him", "his"), ("Gabriela", "she", "her", "her"),
    ("Henrik", "he", "him", "his"), ("Ines", "she", "her", "her"), ("Joaquin", "he", "him", "his"),
    ("Kamala", "she", "her", "her"), ("Lorenzo", "he", "him", "his"), ("Magdalena", "she", "her", "her"),
    ("Nnamdi", "he", "him", "his"), ("Orla", "she", "her", "her"), ("Pavel", "he", "him", "his"),
    ("Qiu Yan", "she", "her", "her"), ("Rashid", "he", "him", "his"), ("Saoirse", "she", "her", "her"),
    ("Teodor", "he", "him", "his"), ("Uchenna", "she", "her", "her"), ("Vusi", "he", "him", "his"),
]
FIRST = [p[0] for p in PEOPLE]

PLACES = ["Northfield", "Riverbend", "Lakeside", "Harborview", "Pinecrest", "Maple Grove", "Stonebridge",
          "Cedar Valley", "Westbrook", "Summit Ridge", "Oakmont", "Brookhaven", "Fairview", "Glenwood", "Ashford",
          "Kingsley", "Millbrook", "Redwood", "Silver Lake", "Thornbury", "Elmstead", "Bayside", "Clearwater",
          "Hollins", "Juniper Hill", "Larchmont", "Meadowvale", "Norwood", "Parkside", "Quarry Bay", "Rosedale",
          "Sherwood", "Tidewater", "Upland", "Valemont", "Willowdale", "Yarrow", "Beacon Hill", "Copperfield",
          "Dunmore", "Evergreen", "Foxhall", "Granger", "Highcliff", "Ivybridge", "Kestrel Point", "Lowell Heath"]

COMPANIES = ["Apex Supply Co.", "Brightwell Logistics", "Corvid Tools", "Dunmore Fasteners", "Elmstead Paper",
             "Fairhaven Metals", "Greystone Works", "Halden Packaging", "Ironvale Parts", "Juniper Office Goods",
             "Kestrel Electrical", "Larkspur Textiles", "Marlow Timber", "Northgate Plastics", "Orchard Print",
             "Pellham Glass", "Quillon Foods", "Redfern Cables", "Saltmarsh Paints", "Tarrow Hardware",
             "Umber Ceramics", "Vantree Furniture", "Wexley Chemicals", "Yarrowby Seeds"]

RESTAURANTS = ["Casa Verde", "Little Saigon", "The Copper Pot", "Bella Napoli", "Golden Wok", "The Olive Tree",
               "Blue Harbor Grill", "Spice Route", "Maple Diner", "Sakura House", "El Farolito", "The Green Fork",
               "Nonna's Kitchen", "Harbor Fish Bar", "Taj Palace", "Le Petit Four", "The Salt Cellar",
               "Mesa Blanca", "The Rusty Anchor", "Pho Real", "Kebab Corner", "The Tin Kettle"]

TEAMS = ["the Rovers", "the Harriers", "the Comets", "the Falcons", "the Otters", "the Wanderers", "the Kestrels",
         "the Pioneers", "the Mariners", "the Foxes", "the Badgers", "the Ravens", "the Titans", "the Hornets"]

STREETS = ["Mill Lane", "Station Road", "Park Avenue", "Church Street", "Queen's Road", "Bridge Street", "High Street",
           "Elm Road", "Victoria Street", "Market Lane", "Harbour Road", "Birch Road", "Hill Road", "Chapel Lane",
           "Kings Way", "Orchard Close", "Canal Street", "Rose Avenue", "Forge Lane", "Meadow Road"]

HOTELS = ["the Alder Inn", "the Harbour Lodge", "the Linden Hotel", "the Old Mill Hotel", "the Seaview Hotel",
          "the Granary Rooms", "the Birchwood Inn", "the Quayside Hotel", "the Station Hotel", "the Kingsway Inn"]


def people(rng, k, exclude=()):
    pool = [p for p in PEOPLE if p[0] not in exclude]
    return rng.sample(pool, k)


def names(rng, k, exclude=()):
    return [p[0] for p in people(rng, k, exclude)]
