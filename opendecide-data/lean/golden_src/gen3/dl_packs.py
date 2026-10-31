"""dl_packs: the domain packs of yn2b family F6 `gen3_def_literal` (yn2b/SPEC.md section 5 F6). DATA ONLY.

Ten packs, each a fictional rule book that defines terms "for its own purposes": customs tariff classification
(replaces the tribunal evidence pack, red-team R4), sports eligibility, club membership, insurance terms, school
policy, platform content rules, procurement, tenancy, grant rules and workplace safety. No hearsay, no Federal Rules of
Evidence wording and no out-of-court-statement structure appears anywhere (tested).

Per pack:
  attrs   typed attributes of the classified entity, each with the surface templates every renderer and every parser
          uses: `vp` (a verb phrase whose subject is the entity: "has a net weight of {op} {x}"), `fact` (one sentence
          stating the value), `label` (the field name in json / kv / markdown), `what` (for "the file does not record
          ..."). Kinds: num (integer with a unit format), date (a 2026 calendar date), cat (closed list of values),
          flag (yes / no).
  terms   the defined terms: invented terms / terms of art, and single real words given a deliberately different
          definition (`real`; SPEC F6: 30% of items), with
          their items (goods packs) and the everyday-usage / outside-knowledge statements (each with the verdict it
          implies for the term; the definition ignores them). Every real-world statement here is a true, commonly
          known fact (botany, food storage); statements about people and fictional institutions are fiction.
  regimes other (fictional) rule books whose rules appear as background ("outside rules") that the definition ignores.

Held out for dev_holdout / devx (SPEC F6: 2 packs and 3 invented terms): the packs `tenancy` and `safety`, and the
invented terms customs:class4_fibre, insurance:s4_escape and procurement:framework_b.

This module holds no labels and no decision logic (that is dl_core.decide); decide2 authors may import it for the
surface templates.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, timedelta

HELD_OUT_PACKS = ("tenancy", "safety")
HELD_OUT_TERMS = ("customs:class4_fibre", "insurance:s4_escape", "procurement:framework_b")

# operator words; {op} slot of num / date verb phrases. Each attribute picks one wording per operator (by index).
NUM_OPS = {">=": ("at least",), ">": ("more than",), "<=": ("at most", "no more than"), "<": ("less than",)}
COUNT_LESS = "fewer than"
DATE_OPS = {"<=": "on or before", "<": "before", ">=": "on or after", ">": "after"}
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December")


def fmt_date(d: date) -> str:
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def parse_date(s: str) -> date:
    m = re.fullmatch(r"(\d{1,2}) (" + "|".join(MONTHS) + r") (\d{4})", s.strip())
    if not m:
        raise ValueError(f"not a date: {s!r}")
    return date(int(m.group(3)), MONTHS.index(m.group(2)) + 1, int(m.group(1)))


# ------------------------------------------------------------------------------------------------ unit formats
def _n(v: int) -> str:
    return f"{v:,}"


UNITS = {  # unit id -> (format, regex that parses it back to an int)
    "kg": (lambda v: f"{_n(v)} kg", r"([\d,]+) kg"),
    "eur": (lambda v: f"€{_n(v)}", r"€([\d,]+)"),
    "pct": (lambda v: f"{v}%", r"(\d+)%"),
    "days": (lambda v: f"{v} day" if v == 1 else f"{v} days", r"(\d+) days?"),
    "years": (lambda v: f"{v} year" if v == 1 else f"{v} years", r"(\d+) years?"),
    "hours": (lambda v: f"{v} hour" if v == 1 else f"{v} hours", r"(\d+) hours?"),
    "cm": (lambda v: f"{v} cm", r"(\d+) cm"),
    "m": (lambda v: f"{v} m", r"(\d+) m"),
    "n": (lambda v: _n(v), r"([\d,]+)"),
}


def _unit(unit: str):
    """(format, regex) of a unit id: a UNITS key, or "noun:<singular>|<plural>" for counted things."""
    if unit.startswith("noun:"):
        sg, pl = unit[5:].split("|")
        return (lambda v: f"{_n(v)} {sg if v == 1 else pl}"), r"([\d,]+) (?:" + re.escape(sg) + "|" + re.escape(pl) + ")"
    return UNITS[unit]


def fmt_unit(unit: str, v: int) -> str:
    return _unit(unit)[0](v)


def unit_regex(unit: str) -> str:
    return _unit(unit)[1]


def parse_unit(unit: str, s: str) -> int:
    m = re.fullmatch(unit_regex(unit), s.strip())
    if not m:
        raise ValueError(f"{s!r} is not a {unit} value")
    return int(m.group(1).replace(",", ""))


@dataclass(frozen=True)
class Attr:
    """One typed attribute. vp/fact templates: num {op} {x} / {v}; date {op} {x} / {v}; cat {list} / {v};
    flag: vp_true / vp_false and fact_true / fact_false."""
    id: str
    kind: str                      # num | date | cat | flag
    label: str                     # field name (json / kv / markdown); no ':' or '.'
    what: str                      # "the consignment's net weight" (missing-fact sentence)
    vp: str = ""                   # num/date/cat verb phrase
    fact: str = ""                 # num/date/cat fact sentence
    unit: str = "n"                # num only
    lo: int = 0                    # num: value range; date: day-of-2026 range (1 = 1 January 2026)
    hi: int = 0
    limits: tuple = ()             # num: limits; date: day-of-2026 limits
    less: str = "less than"        # num: wording of "<"
    values: tuple = ()             # cat only
    vp_true: str = ""              # flag only
    vp_false: str = ""
    fact_true: str = ""
    fact_false: str = ""
    op_style: int = 0              # which NUM_OPS wording this attribute uses for "<="


def num(id, label, unit, vp, fact, what, lo, hi, limits, less="less than", op_style=0):
    return Attr(id, "num", label, what, vp=vp, fact=fact, unit=unit, lo=lo, hi=hi, limits=tuple(limits), less=less,
                op_style=op_style)


def dt(id, label, vp, fact, what, lo, hi, limits):
    return Attr(id, "date", label, what, vp=vp, fact=fact, lo=lo, hi=hi, limits=tuple(limits))


def cat(id, label, values, vp, fact, what):
    return Attr(id, "cat", label, what, vp=vp, fact=fact, values=tuple(values))


def flag(id, label, vp_true, vp_false, fact_true, fact_false, what):
    return Attr(id, "flag", label, what, vp_true=vp_true, vp_false=vp_false, fact_true=fact_true,
                fact_false=fact_false)


def day(d: int) -> date:
    """Day-of-2026 index (1 = 1 January 2026) -> date."""
    return date(2026, 1, 1) + timedelta(days=d - 1)


def day_index(d: date) -> int:
    return (d - date(2026, 1, 1)).days + 1


@dataclass(frozen=True)
class Term:
    id: str                        # pack-unique id; the global id is "<pack>:<id>"
    name: str                      # the defined term as printed in quotes
    real: bool                     # a real word given a deliberately different definition (SPEC F6: 30% of items)
    article: str                   # "a" / "an" before the term
    items: tuple = ()              # goods packs: (item text, ((usage statement, verdict), ...)), ...
    prefer: tuple = ()             # attribute ids preferred for elements (the rest of the pack is still allowed)


@dataclass(frozen=True)
class Pack:
    id: str
    title: str                     # human name of the pack
    instrument: str                # the rule book, e.g. "Harbour Tariff Schedule"
    clause: str                    # numbered unit word, e.g. "Tariff Note"
    entity: str                    # what is classified, e.g. "consignment"
    officer: str                   # who keeps the file, e.g. "classification officer"
    register: str                  # where a classification is recorded (judge rows)
    ref: str                       # file reference prefix
    attrs: tuple
    terms: tuple
    regimes: tuple                 # other rule books (outside rules)
    usage: tuple                   # (usage statement template with {t} {item}, verdict) for terms without own items
    item_kind: str                 # goods | person | event (how an item is named)
    items: tuple = ()              # generic item texts for goods packs (terms without own items)
    filler: tuple = ()             # neutral file details: (label, value template with {n} {d} {id} {name})
    neutral: tuple = ()            # neutral background sentences (no verdict), may use {item} / {name}

    def attr(self, aid: str) -> Attr:
        for a in self.attrs:
            if a.id == aid:
                return a
        raise KeyError(aid)

    def term(self, tid: str) -> Term:
        for t in self.terms:
            if t.id == tid:
                return t
        raise KeyError(tid)


def _u(t_true, t_false):
    """A usage pair: (statement implying the term applies, statement implying it does not)."""
    return ((t_true, True), (t_false, False))


# ================================================================================================ 1. customs
CUSTOMS = Pack(
    id="customs", title="customs tariff classification", instrument="Harbour Tariff Schedule", clause="Tariff Note",
    entity="consignment", officer="classification officer", register="tariff classification register", ref="CL",
    attrs=(
        num("net_weight", "net weight", "kg", "has a net weight of {op} {x}", "The consignment's net weight is {v}.",
            "the consignment's net weight", 40, 4000, (100, 250, 500, 1000, 2000)),
        num("value", "declared value", "eur", "has a declared value of {op} {x}",
            "The declared value of the consignment is {v}.", "the declared value of the consignment", 300, 60000,
            (1000, 2500, 5000, 10000, 20000), op_style=1),
        num("moisture", "moisture content", "pct", "has a moisture content of {op} {x}",
            "Laboratory testing put the moisture content at {v}.", "the moisture content", 2, 40, (8, 10, 12, 15, 20)),
        num("storage", "days in bonded storage", "days", "spent {op} {x} in bonded storage",
            "The goods spent {v} in bonded storage before release.", "how long the goods spent in bonded storage",
            0, 120, (14, 30, 45, 60, 90), less="fewer than"),
        cat("form", "form", ("raw", "washed", "dried", "sliced", "roasted", "frozen", "ground"),
            "was presented in {list} form", "The goods were presented in {v} form.", "the form of the goods"),
        cat("packing", "packing", ("bales", "sacks", "crates", "cartons", "drums", "bulk bags"),
            "is packed in {list}", "The goods arrived packed in {v}.", "how the goods were packed"),
        cat("origin", "shipped from", ("an inland port", "a coastal port", "a free-trade zone", "a river terminal"),
            "was shipped from {list}", "The consignment was shipped from {v}.", "where the consignment was shipped from"),
        flag("sealed", "sealed container", "travelled in a sealed container", "did not travel in a sealed container",
             "The consignment travelled in a sealed container.", "The consignment travelled in an unsealed container.",
             "whether the container was sealed"),
        flag("chilled", "chilled in transit", "was kept chilled in transit", "was not kept chilled in transit",
             "The consignment was kept chilled during transit.", "The consignment was not chilled during transit.",
             "whether the consignment was chilled in transit"),
        flag("predeclared", "declared before arrival", "was declared to the office before arrival",
             "was not declared to the office before arrival",
             "The importer declared the consignment to the office before it arrived.",
             "The importer declared the consignment only after it arrived.",
             "whether the consignment was declared before arrival"),
        flag("certificate", "plant health certificate", "carries a plant health certificate",
             "carries no plant health certificate", "A plant health certificate accompanies the consignment.",
             "No plant health certificate accompanies the consignment.",
             "whether a plant health certificate accompanies the consignment"),
        dt("arrival", "arrival date", "arrived {op} {x}", "The consignment arrived on {v}.",
           "the date the consignment arrived", 20, 330, (60, 91, 121, 182, 244)),
    ),
    terms=(
        Term("fruit", "fruit", True, "a", prefer=("form", "chilled", "moisture", "net_weight"), items=(
            ("tomatoes", _u("Botanically, the tomato is the fruit of the tomato plant.",
                            "In cooking, tomatoes are usually treated as a vegetable.")),
            ("cucumbers", _u("Botanically, a cucumber is a fruit, since it develops from the flower and holds the seeds.",
                             "Most shoppers think of cucumbers as a salad vegetable.")),
            ("rhubarb", _u("Rhubarb is usually cooked with sugar and served as a fruit dessert.",
                           "Botanically, the edible part of rhubarb is a leaf stalk, not a fruit.")),
            ("strawberries", _u("In everyday usage, strawberries are called fruit.",
                                "Botanically, the fleshy part of a strawberry grows from the base of the flower, so "
                                "it is not a true fruit.")),
            ("pumpkins", _u("Botanically, a pumpkin is a fruit.", "Pumpkins are usually sold and cooked as vegetables.")),
            ("bell peppers", _u("Botanically, a bell pepper is a fruit that contains seeds.",
                                "Bell peppers are usually treated as vegetables in cooking.")),
            ("aubergines", _u("Botanically, an aubergine is a berry, which is a kind of fruit.",
                              "In cooking, aubergines are treated as a vegetable.")),
            ("avocados", _u("Botanically, an avocado is a fruit with a single large seed.",
                            "Avocados are mostly eaten in savoury dishes, the way vegetables are.")),
        )),
        Term("nut", "nut", True, "a", prefer=("form", "moisture", "packing", "value"), items=(
            ("peanuts", _u("In everyday usage, peanuts are called nuts.",
                           "Botanically, a peanut is a legume, not a true nut.")),
            ("almonds", _u("Almonds are sold and eaten as nuts.",
                           "Botanically, an almond is the seed of a stone fruit, not a true nut.")),
            ("cashews", _u("Cashews are sold as nuts.",
                           "Botanically, a cashew is a seed that grows below the cashew apple, not a true nut.")),
            ("walnuts", _u("In everyday usage, walnuts are nuts.",
                           "Botanically, a walnut is the seed of a stone fruit rather than a true nut.")),
            ("hazelnuts", ((("Botanically, a hazelnut is a true nut."), True),)),
            ("chestnuts", ((("Botanically, a chestnut is a true nut."), True),)),
            ("pine nuts", _u("Pine nuts are sold alongside other nuts.",
                             "Botanically, pine nuts are the seeds of pine cones, not nuts.")),
            ("coconuts", _u("The coconut is commonly called a nut.",
                            "Botanically, a coconut is a stone fruit, not a true nut.")),
        )),
        Term("perishable", "perishable good", False, "a", prefer=("chilled", "storage", "moisture", "sealed"), items=(
            ("fresh figs", ((("Fresh figs spoil within a few days at room temperature."), True),)),
            ("live oysters", ((("Live oysters must be kept cold and eaten within days."), True),)),
            ("cut flowers", ((("Cut flowers wilt within days."), True),)),
            ("fresh milk", ((("Fresh milk sours within days unless it is kept cold."), True),)),
            ("bananas", ((("Bananas ripen and spoil within days."), True),)),
            ("honey", ((("Sealed honey can keep for years."), False),)),
            ("dried lentils", ((("Dried lentils keep for many months in dry storage."), False),)),
            ("salted cod", ((("Salted cod was traditionally prepared to keep for months without refrigeration."),
                             False),)),
            ("white rice", ((("Polished white rice keeps for a long time when it is stored dry."), False),)),
            ("frozen peas", _u("Frozen peas spoil quickly once they thaw.", "Frozen peas keep for months in a freezer.")),
        )),
        Term("bulk_raw", "bulk raw commodity", False, "a", prefer=("packing", "form", "net_weight", "value")),
        Term("class4_fibre", "Class 4 textile fibre", False, "a", prefer=("form", "packing", "moisture", "net_weight")),
    ),
    regimes=("the Inland Freight Code", "the exporting port's customs rules", "the Regional Trade Convention",
             "the Market Inspectors' Handbook"),
    usage=_u("On the quay, a shipment of {item} is informally called {at}.",
             "On the quay, nobody informally calls a shipment of {item} {at}."),
    item_kind="goods",
    items=("green coffee beans", "cocoa beans", "raw cotton", "sesame seed", "jute fibre", "sisal fibre", "flax straw",
           "dried apricots", "coir fibre", "hemp fibre", "wool tops", "malting barley"),
    filler=(("berth", "quay {n}"), ("vessel", "MV {stem}"), ("seal number", "{id}"), ("broker reference", "{id}"),
            ("inspection time", "{n} minutes"), ("pallet count", "{n} pallets")),
    neutral=("The inspection took place in the morning shift.", "The broker supplied the packing list on time.",
             "The consignment was weighed on the port's calibrated scale.",
             "Samples were taken from three different bales or cases."),
)

# ================================================================================================ 2. sports
SPORTS = Pack(
    id="sports", title="sports eligibility", instrument="Competition Rules of the Valley Football League",
    clause="Rule", entity="player", officer="league registration secretary", register="league eligibility register",
    ref="EL",
    attrs=(
        num("age", "age", "years", "is aged {op} {x}", "The player is {v} old.", "the player's age", 14, 41,
            (16, 18, 21, 23, 35)),
        num("matches", "league matches this season", "noun:league match|league matches",
            "has played {op} {x} this season", "The player has played {v} this season.",
            "how many league matches the player has played this season", 0, 40, (3, 5, 8, 10, 15),
            less="fewer than"),
        num("minutes", "minutes played this season", "noun:minute|minutes", "has played {op} {x} this season",
            "The player has been on the pitch for {v} this season.",
            "how many minutes the player has played this season", 0, 3000, (270, 450, 900, 1350), less="fewer than"),
        num("residence", "years living in the region", "years", "has lived in the region for {op} {x}",
            "The player has lived in the region for {v}.", "how long the player has lived in the region", 0, 15,
            (2, 3, 5), less="less than"),
        num("academy", "years in the club academy", "years", "spent {op} {x} in the club's academy",
            "The player spent {v} in the club's academy.", "how long the player spent in the club's academy", 0, 10,
            (2, 3, 4)),
        cat("contract", "registration type", ("an amateur registration", "a part-time contract", "a full-time contract",
                                              "a loan agreement", "a trial agreement"),
            "is registered under {list}", "The player is registered under {v}.", "the player's registration type"),
        flag("suspended", "serving a suspension", "is serving a suspension", "is not serving a suspension",
             "The player is currently serving a suspension.", "The player is not serving any suspension.",
             "whether the player is serving a suspension"),
        flag("medical", "pre-season medical passed", "passed the pre-season medical",
             "did not pass the pre-season medical", "The player passed the pre-season medical.",
             "The player did not pass the pre-season medical.", "whether the player passed the pre-season medical"),
        flag("capped", "national team appearances", "has played for a national team",
             "has never played for a national team", "The player has played for a national team.",
             "The player has never played for a national team.",
             "whether the player has played for a national team"),
        flag("fee", "season fee paid", "paid the season registration fee", "did not pay the season registration fee",
             "The player paid the season registration fee.", "The player has not paid the season registration fee.",
             "whether the player paid the season registration fee"),
        dt("registered", "registration date", "was registered {op} {x}", "The player was registered on {v}.",
           "the player's registration date", 10, 300, (31, 60, 91, 152, 213)),
    ),
    terms=(
        Term("veteran", "veteran", True, "a", prefer=("age", "matches", "residence")),
        Term("homegrown", "home-grown player", False, "a", prefer=("academy", "residence", "age")),
        Term("cat_b", "Category B entrant", False, "a", prefer=("contract", "registered", "matches")),
        Term("sub", "eligible substitute", False, "an", prefer=("registered", "medical", "suspended", "minutes")),
        Term("rookie", "rookie", True, "a", prefer=("matches", "minutes", "registered", "age")),
    ),
    regimes=("the national federation's rules", "the youth league's handbook", "the regional cup regulations"),
    usage=_u("Around the league, {item} is generally spoken of as {at}.",
             "Around the league, nobody speaks of {item} as {at}."),
    item_kind="person",
    filler=(("club", "{org}"), ("squad number", "{n}"), ("registration form number", "{id}"),
            ("training group", "group {L}"), ("position", "midfield")),
    neutral=("The player's club submitted the forms through the online portal.",
             "The player trains with the first team twice a week.",
             "The club's kit manager confirmed the shirt number."),
)

# ================================================================================================ 3. club
CLUB = Pack(
    id="club", title="club membership", instrument="Bylaws of the Northmere Rowing Club", clause="Bylaw",
    entity="applicant", officer="membership secretary", register="membership register", ref="MB",
    attrs=(
        num("age", "age", "years", "is aged {op} {x}", "The applicant is {v} old.", "the applicant's age", 16, 86,
            (18, 25, 60, 65, 70)),
        num("membership", "years of membership", "years", "has been a member for {op} {x}",
            "The applicant has been a club member for {v}.", "how long the applicant has been a member", 0, 40,
            (2, 5, 10, 15, 25)),
        num("sponsors", "sponsoring members", "noun:current member|current members", "is sponsored by {op} {x}",
            "The applicant's sponsorship form is signed by {v}.",
            "how many members sponsor the applicant", 0, 5, (2, 3), less="fewer than"),
        num("meetings", "general meetings attended last year", "noun:general meeting|general meetings",
            "attended {op} {x} last year", "The applicant attended {v} last year.",
            "how many general meetings the applicant attended last year", 0, 12, (2, 3, 4, 6), less="fewer than"),
        num("volunteer", "volunteer hours this year", "hours", "gave {op} {x} of volunteer work this year",
            "The applicant logged {v} of volunteer work this year.", "the applicant's volunteer hours this year",
            0, 80, (10, 20, 30, 40), less="fewer than"),
        num("household", "people in the household", "noun:person|people", "lives in a household of {op} {x}",
            "The applicant's household is made up of {v}.", "the size of the applicant's household", 1, 7, (2, 3, 4),
            less="fewer than"),
        cat("district", "home district", ("the Old Town", "the harbour district", "the river valley",
                                          "the hill villages", "a village outside the county"),
            "lives in {list}", "The applicant lives in {v}.", "where the applicant lives"),
        flag("dues", "dues paid", "has paid this year's dues in full", "has not paid this year's dues in full",
             "The applicant has paid this year's dues in full.", "The applicant still owes part of this year's dues.",
             "whether the applicant has paid this year's dues"),
        flag("boat", "owns a registered boat", "owns a registered boat", "does not own a registered boat",
             "The applicant owns a registered boat.", "The applicant does not own a registered boat.",
             "whether the applicant owns a registered boat"),
        flag("committee", "committee service", "has served on a club committee", "has never served on a club committee",
             "The applicant has served on a club committee.", "The applicant has never served on a club committee.",
             "whether the applicant has served on a club committee"),
        dt("applied", "application date", "applied {op} {x}", "The applicant applied on {v}.",
           "the date of the application", 5, 330, (32, 91, 152, 244, 305)),
    ),
    terms=(
        Term("senior", "senior member", False, "a", prefer=("age", "membership", "dues")),
        Term("family", "family member", False, "a", prefer=("household", "dues", "district")),
        Term("resident", "resident", True, "a", prefer=("district", "membership", "household")),
        Term("life", "life member", False, "a", prefer=("membership", "committee", "age")),
        Term("assoc2", "Associate (Class II)", False, "an", prefer=("sponsors", "meetings", "volunteer")),
    ),
    regimes=("the national rowing association's guidance", "the county sports council's rules",
             "the boathouse lease"),
    usage=_u("At the boathouse, {item} is commonly referred to as {at}.",
             "At the boathouse, nobody refers to {item} as {at}."),
    item_kind="person",
    filler=(("form number", "{id}"), ("locker number", "{n}"), ("preferred crew", "the {L} crew"),
            ("contact", "{name}")),
    neutral=("The applicant rows mostly on weekend mornings.", "The applicant's form was handed in at the boathouse.",
             "The applicant asked about the winter training schedule."),
)

# ================================================================================================ 4. insurance
INSURANCE = Pack(
    id="insurance", title="insurance terms", instrument="Home Policy Wording of Harrowgate Mutual", clause="Clause",
    entity="loss", officer="claims handler", register="claims register", ref="CLM",
    attrs=(
        cat("cause", "cause", ("a storm", "a burst pipe", "a river overflowing", "a blocked drain", "heavy rain",
                               "a tidal surge"),
            "was caused by {list}", "The loss was caused by {v}.", "the cause of the loss"),
        num("depth", "water depth", "cm", "involved water {op} {x} deep", "The water reached a depth of {v}.",
            "how deep the water reached", 0, 120, (5, 10, 25, 50)),
        num("unoccupied", "days unoccupied before the loss", "days", "happened after the home had stood empty for {op} {x}",
            "The home had stood empty for {v} before the loss.", "how long the home had stood empty", 0, 120,
            (30, 45, 60, 90), less="fewer than"),
        num("reported", "days taken to report", "days", "was reported {op} {x} after it happened",
            "The policyholder reported the loss {v} after it happened.", "how long the policyholder took to report",
            0, 60, (7, 14, 28, 30), less="fewer than"),
        num("amount", "amount claimed", "eur", "is a claim for {op} {x}", "The amount claimed is {v}.",
            "the amount claimed", 150, 80000, (500, 1000, 5000, 20000, 50000), op_style=1),
        num("rain", "hours of continuous rain", "hours", "followed {op} {x} of continuous rain",
            "The loss followed {v} of continuous rain.", "how many hours of continuous rain preceded the loss", 0, 72,
            (6, 12, 24, 48), less="fewer than"),
        num("prior", "claims in the last five years", "noun:claim|claims",
            "comes from a policyholder with {op} {x} in the last five years",
            "The policyholder has made {v} in the last five years.",
            "how many claims the policyholder made in the last five years", 0, 5, (1, 2, 3), less="fewer than"),
        flag("sudden", "sudden event", "happened suddenly", "built up gradually",
             "The damage happened suddenly.", "The damage built up gradually over weeks.",
             "whether the damage happened suddenly"),
        flag("maintained", "maintenance records up to date", "affected a property with up-to-date maintenance records",
             "affected a property without up-to-date maintenance records",
             "The property's maintenance records are up to date.", "The property's maintenance records are not up to date.",
             "whether the property's maintenance records are up to date"),
        flag("ground", "water entered at ground level", "involved water entering at ground level",
             "did not involve water entering at ground level", "The water entered the home at ground level.",
             "The water did not enter the home at ground level.", "whether the water entered at ground level"),
        flag("business", "business use", "affected a property used for business",
             "affected a property not used for business", "Part of the property is used for business.",
             "No part of the property is used for business.", "whether the property is used for business"),
        dt("date", "date of loss", "happened {op} {x}", "The loss happened on {v}.", "the date of the loss", 10, 330,
           (60, 121, 182, 244)),
    ),
    terms=(
        Term("flood", "flood", True, "a", prefer=("cause", "ground", "depth", "sudden")),
        Term("storm", "storm", True, "a", prefer=("rain", "cause", "sudden")),
        Term("accident", "accident", True, "an", prefer=("sudden", "maintained", "amount")),
        Term("insured", "insured event", False, "an", prefer=("reported", "amount", "maintained", "business")),
        Term("s4_escape", "Section 4 escape of water", False, "a", prefer=("cause", "unoccupied", "maintained")),
    ),
    regimes=("the national weather service's storm scale", "the building code", "general usage among loss adjusters"),
    usage=_u("In everyday speech, the policyholder's neighbours would call what happened {at}.",
             "In everyday speech, nobody would call what happened {at}."),
    item_kind="event",
    filler=(("policy number", "{id}"), ("adjuster", "{name}"), ("site visit date", "{d}"),
            ("number of photos received", "{n}")),
    neutral=("The adjuster visited the property within the week.", "The policyholder supplied photographs of the damage.",
             "The policy has been renewed every year since it started."),
)

# ================================================================================================ 5. school
SCHOOL = Pack(
    id="school", title="school policy", instrument="Student Handbook of Ashgrove Academy", clause="Section",
    entity="absence", officer="attendance officer", register="attendance register", ref="AB",
    attrs=(
        num("days", "school days missed", "days", "covers {op} {x} of school",
            "The absence covers {v} of school.", "how many school days the absence covers", 1, 20, (2, 3, 5, 10),
            less="fewer than"),
        num("notice", "hours of notice", "hours", "was requested with {op} {x} of notice",
            "The request was made {v} before the absence.", "how much notice was given", 0, 240, (24, 48, 72),
            less="less than"),
        num("year", "year group", "n", "is for a student whose year group is {op} {x}", "The student is in year {v}.",
            "the student's year group", 7, 13, (9, 10, 11, 12)),
        num("attendance", "attendance this year", "pct", "is for a student whose attendance this year is {op} {x}",
            "The student's attendance this year stands at {v}.", "the student's attendance this year", 70, 100,
            (90, 92, 95)),
        num("prior", "absences earlier this term", "noun:other absence|other absences", "follows {op} {x} this term",
            "The student has had {v} this term.", "how many other absences the student had this term",
            0, 10, (2, 3, 4, 5), less="fewer than"),
        cat("reason", "reason", ("a family holiday", "a medical appointment", "illness", "a sports competition",
                                 "religious observance", "a music exam"),
            "was for {list}", "The absence was for {v}.", "the reason for the absence"),
        cat("approver", "approved by", ("the head teacher", "the form tutor", "the school office", "the deputy head"),
            "was approved by {list}", "The absence was approved by {v}.", "who approved the absence"),
        flag("signed", "parent signature", "was requested on a form signed by a parent",
             "was not requested on a form signed by a parent", "A parent signed the request form.",
             "No parent signed the request form.", "whether a parent signed the request"),
        flag("doctor", "doctor's note", "is supported by a doctor's note", "is not supported by a doctor's note",
             "A doctor's note supports the absence.", "No doctor's note supports the absence.",
             "whether a doctor's note supports the absence"),
        flag("exams", "exam week", "fell in an exam week", "did not fall in an exam week",
             "The absence fell in an exam week.", "The absence did not fall in an exam week.",
             "whether the absence fell in an exam week"),
        dt("start", "first day of absence", "began {op} {x}", "The absence began on {v}.",
           "the first day of the absence", 10, 330, (32, 91, 152, 244)),
    ),
    terms=(
        Term("authorised", "authorised absence", False, "an", prefer=("approver", "notice", "signed")),
        Term("holiday", "holiday", True, "a", prefer=("reason", "days", "notice")),
        Term("band2", "Band 2 absence", False, "a", prefer=("days", "prior", "attendance")),
        Term("excused", "excused absence", False, "an", prefer=("doctor", "reason", "signed")),
    ),
    regimes=("the regional education office's attendance guidance", "the sports association's school rules",
             "the parents' association newsletter"),
    usage=_u("Most parents at the school would call an absence like this {at}.",
             "Most parents at the school would not call an absence like this {at}."),
    item_kind="person",
    filler=(("form number", "{id}"), ("tutor group", "{n}{L}"), ("contact", "{name}"),
            ("logging office", "the school office")),
    neutral=("The student's tutor was told about the absence.", "The request arrived through the parent portal.",
             "The student's homework was sent home."),
)

# ================================================================================================ 6. platform
PLATFORM = Pack(
    id="platform", title="platform content rules", instrument="Community Standards of Chirrup", clause="Standard",
    entity="post", officer="trust and safety reviewer", register="content review log", ref="PST",
    attrs=(
        num("followers", "account followers", "noun:follower|followers", "comes from an account with {op} {x}",
            "The account that published the post has {v}.", "how many followers the account has", 0,
            400000, (1000, 10000, 50000, 100000), less="fewer than"),
        num("reports", "user reports", "noun:user report|user reports", "drew {op} {x}", "The post drew {v}.",
            "how many user reports the post drew", 0, 50, (3, 5, 10, 20), less="fewer than"),
        num("account_age", "account age", "days", "comes from an account that is {op} {x} old",
            "The account is {v} old.", "how old the account is", 0, 2000, (30, 90, 180, 365), less="less than"),
        num("shares", "shares", "noun:time|times", "was shared {op} {x}", "The post was shared {v}.",
            "how many times the post was shared", 0, 20000, (100, 500, 1000, 5000), less="fewer than"),
        num("hourly", "posts by the account in the same hour", "noun:post|posts",
            "was one of {op} {x} the account published in the same hour",
            "The account published {v} in the same hour.",
            "how many posts the account published in the same hour", 1, 30, (5, 10, 20), less="fewer than"),
        cat("topic", "topic", ("cooking", "personal finance", "gaming", "fitness", "music", "travel"),
            "is about {list}", "The post is about {v}.", "the topic of the post"),
        flag("link", "external link", "contains an external link", "contains no external link",
             "The post contains an external link.", "The post contains no external link.",
             "whether the post contains an external link"),
        flag("paid", "paid to publish", "was published by a creator who was paid to publish it",
             "was not published for payment", "The creator was paid to publish the post.",
             "The creator was not paid to publish the post.", "whether the creator was paid to publish the post"),
        flag("label", "paid partnership label", "carries a paid partnership label", "carries no paid partnership label",
             "The post carries a paid partnership label.", "The post carries no paid partnership label.",
             "whether the post carries a paid partnership label"),
        flag("edited", "edited after publication", "was edited after publication", "was not edited after publication",
             "The post was edited after it was published.", "The post was not edited after it was published.",
             "whether the post was edited after publication"),
        dt("published", "publication date", "was published {op} {x}", "The post was published on {v}.",
           "the date the post was published", 10, 330, (60, 121, 182, 244)),
    ),
    terms=(
        Term("advert", "advertisement", True, "an", prefer=("paid", "label", "link")),
        Term("spam", "spam", True, "", prefer=("hourly", "link", "account_age")),
        Term("creator", "creator post", False, "a", prefer=("followers", "account_age", "topic")),
        Term("tier3", "Tier 3 content", False, "a", prefer=("reports", "shares", "followers")),
    ),
    regimes=("the advertising regulator's code", "another platform's community rules", "the trade press"),
    usage=_u("Most users who saw it would call the post {at}.",
             "Most users who saw it would not call the post {at}."),
    item_kind="person",
    filler=(("post id", "{id}"), ("reviewer queue", "queue {n}"), ("account handle", "@{stem}"),
            ("review start date", "{d}")),
    neutral=("The post was reviewed in the standard queue.", "The post was written in plain text with one image.",
             "The account has not changed its handle this year."),
)

# ================================================================================================ 7. procurement
PROCUREMENT = Pack(
    id="procurement", title="procurement", instrument="Procurement Rules of Eastholm Council", clause="Rule",
    entity="bid", officer="procurement officer", register="tender register", ref="TN",
    attrs=(
        num("value", "bid value", "eur", "is worth {op} {x}", "The bid is worth {v}.", "the value of the bid",
            5000, 900000, (25000, 50000, 100000, 250000), op_style=1),
        num("staff", "bidder's employees", "noun:employee|employees", "comes from a bidder with {op} {x}",
            "The bidder has {v}.", "how many people the bidder employs", 1, 400, (10, 50, 250),
            less="fewer than"),
        num("years", "years trading", "years", "comes from a bidder that has traded for {op} {x}",
            "The bidder has been trading for {v}.", "how long the bidder has been trading", 0, 40, (1, 2, 3, 5)),
        num("early", "days before the deadline", "days", "was submitted {op} {x} before the deadline",
            "The bid was submitted {v} before the deadline.", "how long before the deadline the bid was submitted",
            0, 30, (1, 2, 5, 10), less="fewer than"),
        num("lots", "lots bid for", "noun:lot|lots", "covers {op} {x}", "The bid covers {v}.",
            "how many lots the bid covers", 1, 8, (2, 3, 4), less="fewer than"),
        num("insurance", "insurance cover", "eur", "is backed by insurance cover of {op} {x}",
            "The bidder holds insurance cover of {v}.", "the bidder's insurance cover", 0, 10000000,
            (1000000, 2000000, 5000000)),
        cat("sector", "sector", ("construction", "catering", "cleaning", "IT services", "transport", "printing"),
            "is for {list} work", "The bid is for {v} work.", "the kind of work in the bid"),
        flag("local", "premises in the council area", "comes from a bidder with premises in the council area",
             "comes from a bidder without premises in the council area",
             "The bidder has premises in the council area.", "The bidder has no premises in the council area.",
             "whether the bidder has premises in the council area"),
        flag("certified", "quality certificate", "comes from a bidder holding the quality certificate",
             "comes from a bidder without the quality certificate", "The bidder holds the quality certificate.",
             "The bidder does not hold the quality certificate.", "whether the bidder holds the quality certificate"),
        flag("signed", "signed declaration", "includes a signed declaration", "does not include a signed declaration",
             "The bid includes a signed declaration.", "The bid does not include a signed declaration.",
             "whether the bid includes a signed declaration"),
        dt("submitted", "submission date", "was submitted {op} {x}", "The bid was submitted on {v}.",
           "the date the bid was submitted", 10, 330, (60, 121, 182, 244)),
    ),
    terms=(
        Term("small", "small business", False, "a", prefer=("staff", "years", "value")),
        Term("local", "local supplier", False, "a", prefer=("local", "sector", "staff")),
        Term("compliant", "compliant tender", False, "a", prefer=("signed", "early", "certified", "insurance")),
        Term("framework_b", "Framework B bid", False, "a", prefer=("lots", "value", "certified")),
        Term("startup", "start-up", True, "a", prefer=("years", "staff", "value")),
    ),
    regimes=("the national procurement guidance", "the chamber of commerce's membership rules",
             "the tax office's size bands"),
    usage=_u("In everyday business talk, people would put this bid down as {at}.",
             "In everyday business talk, nobody would put this bid down as {at}."),
    item_kind="person",
    filler=(("tender reference", "{id}"), ("contact", "{name}"), ("evaluator", "{name}"), ("envelope", "envelope {n}")),
    neutral=("The bid was received through the council's tender portal.", "The bidder attended the briefing session.",
             "The bid documents run to several pages."),
)

# ================================================================================================ 8. tenancy (held out)
TENANCY = Pack(
    id="tenancy", title="tenancy", instrument="Tenancy Agreement for 14 Larch Row", clause="Clause",
    entity="occupant", officer="letting agent", register="occupancy register", ref="TEN",
    attrs=(
        num("nights", "nights a week at the property", "noun:night|nights", "stays {op} {x} a week at the property",
            "The occupant stays {v} a week at the property.", "how many nights a week the occupant stays",
            0, 7, (2, 3, 4, 5), less="fewer than"),
        num("months", "months at the property", "noun:month|months", "has stayed at the property for {op} {x}",
            "The occupant has stayed at the property for {v}.", "how long the occupant has stayed", 0, 36,
            (1, 3, 6, 12), less="fewer than"),
        num("age", "age", "years", "is aged {op} {x}", "The occupant is {v} old.", "the occupant's age", 1, 90,
            (16, 18, 21, 65)),
        num("rent_share", "share of the rent paid", "pct", "pays {op} {x} of the rent",
            "The occupant pays {v} of the rent.", "what share of the rent the occupant pays", 0, 100,
            (10, 25, 50)),
        cat("relation", "relation to the tenant", ("spouse", "child", "sibling", "friend", "lodger", "carer"),
            "is the tenant's {list}", "The occupant is the tenant's {v}.", "the occupant's relation to the tenant"),
        flag("on_lease", "named on the lease", "is named on the lease", "is not named on the lease",
             "The occupant is named on the lease.", "The occupant is not named on the lease.",
             "whether the occupant is named on the lease"),
        flag("own_room", "own bedroom", "has their own bedroom", "does not have their own bedroom",
             "The occupant has their own bedroom.", "The occupant does not have their own bedroom.",
             "whether the occupant has their own bedroom"),
        flag("mail", "post received at the address", "receives post at the address",
             "does not receive post at the address", "The occupant receives post at the address.",
             "The occupant does not receive post at the address.", "whether the occupant receives post there"),
        flag("vehicle", "parks a vehicle at the property", "parks a vehicle at the property",
             "does not park a vehicle at the property", "The occupant parks a vehicle at the property.",
             "The occupant does not park a vehicle at the property.", "whether the occupant parks a vehicle there"),
        dt("moved_in", "move-in date", "moved in {op} {x}", "The occupant moved in on {v}.", "the move-in date",
           5, 330, (32, 91, 152, 244)),
    ),
    terms=(
        Term("guest", "guest", True, "a", prefer=("nights", "months", "on_lease")),
        Term("household", "household member", False, "a", prefer=("relation", "months", "mail")),
        Term("lodger", "lodger", True, "a", prefer=("rent_share", "own_room", "on_lease")),
        Term("sched2", "Schedule 2 occupant", False, "a", prefer=("age", "nights", "vehicle")),
    ),
    regimes=("the city's housing licence rules", "the council tax rules", "the landlords' association handbook"),
    usage=_u("Neighbours would ordinarily call {item} {at}.", "Neighbours would not ordinarily call {item} {at}."),
    item_kind="person",
    filler=(("inspection reference", "{id}"), ("inspector", "{name}"), ("flat number", "{n}"), ("visit date", "{d}")),
    neutral=("The letting agent visited during the quarterly inspection.", "The tenant answered the agent's questions.",
             "The property has three bedrooms."),
)

# ================================================================================================ 9. grant
GRANT = Pack(
    id="grant", title="grant rules", instrument="Grant Guidelines of the Fernhill Foundation", clause="Guideline",
    entity="applicant", officer="grants officer", register="grants register", ref="GR",
    attrs=(
        num("org_age", "years since founding", "years", "was founded {op} {x} ago",
            "The applicant was founded {v} ago.", "how long ago the applicant was founded", 0, 30, (1, 2, 3, 5)),
        num("income", "annual income", "eur", "has an annual income of {op} {x}",
            "The applicant's annual income is {v}.", "the applicant's annual income", 0, 5000000,
            (50000, 100000, 250000, 1000000), op_style=1),
        num("staff", "paid staff", "noun:paid staff member|paid staff members", "employs {op} {x}",
            "The applicant employs {v}.",
            "how many paid staff the applicant employs", 0, 200, (5, 10, 25, 50), less="fewer than"),
        num("volunteers", "volunteers", "noun:volunteer|volunteers", "has {op} {x}", "The applicant has {v}.",
            "how many volunteers the applicant has", 0, 500, (10, 20, 50), less="fewer than"),
        num("months", "project length", "noun:month|months", "proposes a project lasting {op} {x}",
            "The proposed project would last {v}.", "how long the proposed project would last", 1, 48,
            (6, 12, 18, 24, 36), less="fewer than"),
        num("match", "match funding", "pct", "brings match funding of {op} {x} of the cost",
            "The applicant brings match funding of {v} of the cost.", "the applicant's match funding", 0, 60,
            (10, 20, 25, 30)),
        cat("region", "region", ("the northern district", "the southern district", "the coastal district",
                                 "the capital"),
            "is based in {list}", "The applicant is based in {v}.", "where the applicant is based"),
        cat("sector", "sector", ("arts", "sport", "environment", "youth work", "heritage", "health"),
            "works in {list}", "The applicant works in {v}.", "the applicant's sector"),
        flag("charity", "registered charity", "is a registered charity", "is not a registered charity",
             "The applicant is a registered charity.", "The applicant is not a registered charity.",
             "whether the applicant is a registered charity"),
        flag("prior", "grant in the last two years", "received a grant from the foundation in the last two years",
             "has not received a grant from the foundation in the last two years",
             "The applicant received a grant from the foundation in the last two years.",
             "The applicant has not received a grant from the foundation in the last two years.",
             "whether the applicant received a grant in the last two years"),
        dt("submitted", "application date", "applied {op} {x}", "The application arrived on {v}.",
           "the date the application arrived", 10, 330, (60, 121, 182, 244)),
    ),
    terms=(
        Term("community", "community group", False, "a", prefer=("volunteers", "staff", "region")),
        Term("small_org", "small organisation", False, "a", prefer=("income", "staff", "org_age")),
        Term("heritage", "heritage project", False, "a", prefer=("sector", "months", "match")),
        Term("stream_c", "Stream C applicant", False, "a", prefer=("match", "prior", "charity")),
        Term("volunteer_led", "volunteer-led body", False, "a", prefer=("volunteers", "staff", "charity")),
    ),
    regimes=("the charity regulator's guidance", "the arts council's funding rules", "the tax office's definitions"),
    usage=_u("People in the local voluntary sector would call {item} {at}.",
             "People in the local voluntary sector would not call {item} {at}."),
    item_kind="person",
    filler=(("application number", "{id}"), ("contact", "{name}"), ("assessor", "{name}"), ("round", "round {n}")),
    neutral=("The application was complete when it arrived.", "The applicant attended an online information session.",
             "The budget sheet was attached as a spreadsheet."),
)

# ================================================================================================ 10. safety (held out)
SAFETY = Pack(
    id="safety", title="workplace safety", instrument="Site Safety Code of Brackwater Construction", clause="Section",
    entity="incident", officer="site safety officer", register="incident register", ref="INC",
    attrs=(
        num("height", "height involved", "m", "involved a drop of {op} {x}", "The drop involved was {v}.",
            "the height of the drop", 0, 30, (2, 3, 4, 6)),
        num("hours_lost", "working hours lost", "hours", "cost {op} {x} of work",
            "The incident cost {v} of work.", "how many working hours the incident cost", 0, 200, (8, 24, 72),
            less="fewer than"),
        num("days_off", "days off work", "days", "led to {op} {x} off work", "The worker took {v} off work.",
            "how many days the worker took off", 0, 60, (1, 3, 7), less="fewer than"),
        num("reported", "hours to report", "hours", "was reported {op} {x} after it happened",
            "The incident was reported {v} after it happened.", "how long it took to report the incident", 0, 96,
            (1, 4, 24, 48), less="less than"),
        num("witnesses", "witnesses", "noun:witness|witnesses", "had {op} {x}", "The incident had {v}.",
            "how many witnesses the incident had", 0, 6, (1, 2, 3), less="fewer than"),
        cat("location", "location", ("a scaffold", "a roof", "a trench", "a ladder", "the loading bay",
                                     "the site office"),
            "happened at {list}", "The incident happened at {v}.", "where the incident happened"),
        flag("first_aid", "first aid given", "needed first aid at the scene", "needed no first aid at the scene",
             "First aid was given at the scene.", "No first aid was needed at the scene.",
             "whether first aid was given at the scene"),
        flag("ppe", "protective equipment worn", "involved a worker wearing the required protective equipment",
             "involved a worker not wearing the required protective equipment",
             "The worker was wearing the required protective equipment.",
             "The worker was not wearing the required protective equipment.",
             "whether the worker wore the required protective equipment"),
        flag("contractor", "contractor involved", "involved a contractor", "involved no contractor",
             "A contractor was involved.", "No contractor was involved.", "whether a contractor was involved"),
        flag("powered", "powered equipment", "involved powered equipment", "involved no powered equipment",
             "Powered equipment was involved.", "No powered equipment was involved.",
             "whether powered equipment was involved"),
        dt("date", "incident date", "happened {op} {x}", "The incident happened on {v}.", "the date of the incident",
           10, 330, (60, 121, 182, 244)),
    ),
    terms=(
        Term("fall", "fall from height", False, "a", prefer=("height", "location", "ppe")),
        Term("near_miss", "near miss", False, "a", prefer=("first_aid", "hours_lost", "days_off")),
        Term("lti", "lost-time injury", False, "a", prefer=("days_off", "hours_lost", "first_aid")),
        Term("cat2", "Category 2 incident", False, "a", prefer=("reported", "witnesses", "powered")),
    ),
    regimes=("the national health and safety regulator's guidance", "the insurer's incident categories",
             "the trade union's site handbook"),
    usage=_u("Most people on site would call what happened {at}.",
             "Most people on site would not call what happened {at}."),
    item_kind="event",
    filler=(("report number", "{id}"), ("supervisor", "{name}"), ("shift", "shift {n}"), ("site", "{org} site")),
    neutral=("The site supervisor filled in the report form.", "The area was cleared and checked afterwards.",
             "The weather on the day was dry."),
)

PERSON_PACKS = ("sports", "club", "tenancy")  # the classified entity is a person: "a player who ...", not "that"

# Attributes that state the same fact from two sides (R2 coherence fix, 1 Oct): one item never shows both, so the
# two can never contradict each other (e.g. "33 months at the property" next to a move-in date last month).
EXCLUSIVE_ATTRS = {"tenancy": (("months", "moved_in"),)}


def rel(pack_id: str) -> str:
    return "who" if pack_id in PERSON_PACKS else "that"


# how the classified item is named: (description field template, description sentence template, name source)
DESC = {
    "customs": ("{item} shipped by {org}", "The consignment is {desc}.", "goods"),
    "sports": ("{name}", "The player is {desc}.", "person"),
    "club": ("{name}", "The applicant is {desc}.", "person"),
    "insurance": ("loss reported by {name}", "The loss was reported by {name}.", "person"),
    "school": ("absence of {name}", "The absence is for the student {name}.", "person"),
    "platform": ("post by {name}", "The post was published by {name}.", "person"),
    "procurement": ("bid from {org}", "The bid comes from {org}.", "org"),
    "tenancy": ("{name}", "The occupant is {desc}.", "person"),
    "grant": ("{org}", "The applicant is {desc}.", "org"),
    "safety": ("incident reported by {name}", "The incident was reported by {name}.", "person"),
}

PACKS = {p.id: p for p in (CUSTOMS, SPORTS, CLUB, INSURANCE, SCHOOL, PLATFORM, PROCUREMENT, TENANCY, GRANT, SAFETY)}
PACK_IDS = tuple(PACKS)
TERM_IDS = tuple(f"{p.id}:{t.id}" for p in PACKS.values() for t in p.terms)

# words that must never appear in any F6 text (SPEC F6 / red-team R4: no hearsay or evidence-rule structures)
BANNED_TOPIC_RE = re.compile(r"hearsay|out-of-court|out of court|federal rules? of evidence|\bFRE\b|declarant|"
                             r"rules? of evidence|tribunal|admissib", re.I)


def a_term(t: Term) -> str:
    """The term with its article, quoted: "a 'fruit'", "an 'advertisement'", "'spam'"."""
    return f"{t.article} '{t.name}'" if t.article else f"'{t.name}'"


def term_of(gid: str) -> tuple[Pack, Term]:
    p, t = gid.split(":", 1)
    return PACKS[p], PACKS[p].term(t)


def held_out_term(gid: str) -> bool:
    return gid.split(":", 1)[0] in HELD_OUT_PACKS or gid in HELD_OUT_TERMS


def terms_for(split: str) -> tuple:
    """train / dev_iid: kept packs and kept terms; dev_holdout / devx: the held-out packs plus the held-out terms."""
    hold = split in ("dev_holdout", "devx")
    return tuple(g for g in TERM_IDS if held_out_term(g) == hold)


def all_texts() -> list[str]:
    """Every literal text of the packs (for the banned-topic test and the 6-gram template checks)."""
    out = []
    for p in PACKS.values():
        out += [p.title, p.instrument, p.clause, p.entity, p.officer, p.register]
        for a in p.attrs:
            out += [a.label, a.what, a.vp, a.fact, a.vp_true, a.vp_false, a.fact_true, a.fact_false, *a.values]
        for t in p.terms:
            out.append(t.name)
            for it, us in t.items:
                out.append(it)
                out += [u for u, _ in us]
        out += list(p.regimes) + [u for u, _ in p.usage] + list(p.items) + list(p.neutral)
        out += [v for _, v in p.filler]
    return [x for x in out if x]
