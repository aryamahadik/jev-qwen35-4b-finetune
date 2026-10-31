"""rk_math: which worked answer to an everyday calculation is correct and complete (both requested values exactly
right).  Wrong answers come from typical slips (tip or tax forgotten, tax on the wrong base, overtime rate wrong,
rounding down where the rule says round up, a misread number in the problem).  Values are exact by construction
(parameters are drawn so every requested value is exact at the stated precision).
"""
import copy
import math
import random
from fractions import Fraction as Fr

from rk_core import fix_articles

LABELS = [("Answer", "L"), ("Solution", "N"), ("Attempt", "N")]
LET = "ABCDEFGH"


def money(c):
    """c: Fraction/int cents -> '$12.34' (must be exact cents)."""
    assert Fr(c).denominator == 1, c
    c = int(c)
    return f"${c // 100:,}.{c % 100:02d}"


def pounds(p):
    assert Fr(p).denominator == 1
    p = int(p)
    return f"\u00a3{p // 100:,}.{p % 100:02d}"


def hm(minutes):
    h, m = divmod(int(minutes), 60)
    return f"{h} h {m:02d} min"


def clock(minutes):
    h, m = divmod(int(minutes) % 1440, 60)
    return f"{h:02d}:{m:02d}"


def dec1(x):
    x = Fr(x)
    assert (x * 10).denominator == 1, x
    t = int(x * 10)
    return f"{t // 10}.{t % 10}"


def exact(*vals, scale=1):
    return all((Fr(v) * scale).denominator == 1 for v in vals)


# ------------------------------------------------------------------------------------------------ templates
def g_bill(rng):
    return dict(S=rng.randrange(3000, 30000, 5), p=rng.choice([10, 12, 15, 18, 20, 25]), n=rng.randint(2, 8))


def c_bill(p):
    tot = Fr(p["S"]) * (100 + p["p"]) / 100
    return tot, tot / p["n"]


W_BILL = [lambda p: (Fr(p["S"]), Fr(p["S"]) / p["n"]),  # tip forgotten
          lambda p: (c_bill(p)[0], Fr(p["S"]) / p["n"]),  # split before tip
          lambda p: (c_bill(p)[0], c_bill(p)[0] / (p["n"] + 1)),  # divided by one too many
          lambda p: (Fr(p["S"]) + p["p"] * 100, (Fr(p["S"]) + p["p"] * 100) / p["n"])]  # tip read as dollars


def t_bill(p, v):
    return [f"{p['n']} colleagues have lunch together. The bill comes to {money(p['S'])} before tip. They add a "
            f"{p['p']}% tip on the bill and split the total equally.",
            f"A restaurant bill for {p['n']} people is {money(p['S'])}. The group adds a {p['p']}% tip to the bill "
            f"and then shares the total equally."][v]


def g_disc(rng):
    return dict(P=rng.randrange(1000, 60000, 50), d=rng.choice([10, 15, 20, 25, 30, 40, 50]),
                t=rng.choice([5, 6, 8, 10, 20]))


def c_disc(p):
    sale = Fr(p["P"]) * (100 - p["d"]) / 100
    return sale, sale * (100 + p["t"]) / 100


W_DISC = [lambda p: (c_disc(p)[0], c_disc(p)[0] + Fr(p["P"]) * p["t"] / 100),  # tax on the original price
          lambda p: (c_disc(p)[0], Fr(p["P"]) * (100 - p["d"] + p["t"]) / 100),  # rates added
          lambda p: (Fr(p["P"]) * p["d"] / 100, Fr(p["P"]) * p["d"] / 100 * (100 + p["t"]) / 100),  # discount amount
          lambda p: (c_disc(p)[0], c_disc(p)[0])]  # tax forgotten


def t_disc(p, v):
    item = ["jacket", "desk lamp", "pair of boots", "bike helmet", "rucksack", "coffee grinder"][p["P"] % 6]
    return [f"A {item} priced {money(p['P'])} is reduced by {p['d']}% in a sale. Sales tax of {p['t']}% is then "
            f"added to the sale price.",
            f"In a {p['d']}%-off sale, a {item} originally marked at {money(p['P'])} is discounted, and {p['t']}% tax "
            f"is charged on the discounted price."][v]


def g_ot(rng):
    return dict(r=rng.randrange(1200, 3600, 50), h=rng.randint(41, 56), base=rng.choice([37, 38, 40, 40, 40]))


def c_ot(p):
    ot = Fr(p["h"] - p["base"]) * p["r"] * 3 / 2
    return ot, Fr(p["base"]) * p["r"] + ot


W_OT = [lambda p: (Fr(p["h"] - p["base"]) * p["r"] * 2, Fr(p["base"]) * p["r"] + Fr(p["h"] - p["base"]) * p["r"] * 2),
        lambda p: (Fr(p["h"] - p["base"]) * p["r"], Fr(p["h"]) * p["r"]),  # no premium
        lambda p: (c_ot(p)[0], Fr(p["h"]) * p["r"] + c_ot(p)[0]),  # overtime hours paid twice
        lambda p: (Fr(p["h"] - 40) * p["r"] * 3 / 2, Fr(40) * p["r"] + Fr(p["h"] - 40) * p["r"] * 3 / 2)]


def t_ot(p, v):
    nm = ["Sam", "Rita", "Kofi", "Lena", "Mateo", "Hana"][p["h"] % 6]
    return [f"{nm} earns {money(p['r'])} an hour. Hours above {p['base']} in a week are paid at 1.5 times the normal "
            f"rate. Last week {nm} worked {p['h']} hours.",
            f"The standard week is {p['base']} hours at {money(p['r'])} per hour; every hour beyond that is paid at time "
            f"and a half. {nm} worked {p['h']} hours this week."][v]


def g_recipe(rng):
    s = rng.choice([2, 4, 6, 8])
    return dict(s=s, t=rng.choice([x for x in (3, 5, 6, 9, 10, 12, 15, 20) if x != s]),
                a=rng.randrange(100, 600, 25), b=rng.randrange(100, 800, 50))


def c_recipe(p):
    return Fr(p["a"]) * p["t"] / p["s"], Fr(p["b"]) * p["t"] / p["s"]


W_RECIPE = [lambda p: (Fr(p["a"]) * p["s"] / p["t"], Fr(p["b"]) * p["s"] / p["t"]),  # inverted scale
            lambda p: (Fr(p["a"]) + (p["t"] - p["s"]) * 25, Fr(p["b"]) + (p["t"] - p["s"]) * 50),
            lambda p: (c_recipe(p)[0], Fr(p["b"])),  # milk not scaled
            lambda p: (Fr(p["a"]) * p["t"], Fr(p["b"]) * p["t"])]  # multiplied by people, not by the ratio


def t_recipe(p, v):
    dish = ["pancake", "flatbread", "sponge cake", "batter pudding"][p["a"] % 4]
    return [f"A {dish} recipe for {p['s']} people uses {p['a']} g of flour and {p['b']} ml of milk. You are cooking "
            f"for {p['t']} people and scale both amounts in proportion.",
            f"Scaling a {dish} recipe: the original serves {p['s']} and needs {p['a']} g flour and {p['b']} ml milk. "
            f"It must now serve {p['t']}."][v]


def g_trip(rng):
    v = rng.choice([40, 45, 48, 50, 60, 64, 72, 75, 80, 90, 96, 100, 120])
    return dict(d=rng.randrange(40, 520, 2), v=v, dep=rng.randrange(6 * 60, 13 * 60, 5))


def c_trip(p):
    mins = Fr(p["d"]) * 60 / p["v"]
    return mins, p["dep"] + mins


W_TRIP = [lambda p: (Fr(int(Fr(p["d"]) / p["v"]) * 60 + int((Fr(p["d"]) / p["v"] - int(Fr(p["d"]) / p["v"])) * 100)),
                     p["dep"] + int(Fr(p["d"]) / p["v"]) * 60 + int((Fr(p["d"]) / p["v"] - int(Fr(p["d"]) / p["v"])) * 100)),
          lambda p: (c_trip(p)[0], p["dep"] + c_trip(p)[0] + 60),  # clock slip
          lambda p: (c_trip(p)[0] + 30, p["dep"] + c_trip(p)[0] + 30),
          lambda p: (c_trip(p)[0], p["dep"] - c_trip(p)[0] + 2 * c_trip(p)[0] - 15)]


def t_trip(p, v):
    return [f"A coach leaves at {clock(p['dep'])} and drives {p['d']} km at a steady {p['v']} km/h with no stops.",
            f"Departure is at {clock(p['dep'])}. The route is {p['d']} km long and the train averages {p['v']} km/h "
            f"without stopping."][v]


def g_fuel(rng):
    return dict(d=rng.randrange(50, 900, 10), c=rng.choice([45, 50, 55, 60, 64, 65, 70, 72, 75, 80, 85, 90]),
                q=rng.randrange(140, 210, 1))


def c_fuel(p):
    litres = Fr(p["d"]) * p["c"] / 1000
    return litres, litres * p["q"]


W_FUEL = [lambda p: (Fr(p["d"]) * p["c"] / 100, Fr(p["d"]) * p["c"] / 100 * p["q"]),  # consumption read x10
          lambda p: (c_fuel(p)[0], c_fuel(p)[0] * p["q"] / 10),
          lambda p: (Fr(p["d"]) * p["c"] / 1000 + 1, (Fr(p["d"]) * p["c"] / 1000 + 1) * p["q"]),
          lambda p: (c_fuel(p)[0], Fr(p["d"]) * p["q"])]


def t_fuel(p, v):
    return [f"A car uses {dec1(Fr(p['c'], 10))} litres of fuel per 100 km. The trip is {p['d']} km and fuel costs "
            f"{money(p['q'])} per litre.",
            f"Fuel costs {money(p['q'])} a litre. You will drive {p['d']} km in a car that uses "
            f"{dec1(Fr(p['c'], 10))} L/100 km."][v]


def g_paint(rng):
    return dict(l=rng.randrange(6, 30), h=rng.choice([2, 3]), win=rng.randrange(0, 8), coats=rng.choice([1, 2, 2, 3]),
                cov=rng.choice([8, 10, 12]), tin=rng.choice([Fr(5, 2), Fr(5), Fr(1)]))


def c_paint(p):
    area = Fr(p["l"] * p["h"] - p["win"])
    litres = area * p["coats"] / p["cov"]
    return litres, math.ceil(litres / p["tin"])


W_PAINT = [lambda p: (Fr(p["l"] * p["h"]) * p["coats"] / p["cov"], math.ceil(Fr(p["l"] * p["h"]) * p["coats"] / p["cov"] / p["tin"])),
           lambda p: (c_paint(p)[0], math.floor(c_paint(p)[0] / p["tin"])),
           lambda p: (Fr(p["l"] * p["h"] - p["win"]) / p["cov"], math.ceil(Fr(p["l"] * p["h"] - p["win"]) / p["cov"] / p["tin"])),
           lambda p: (c_paint(p)[0], math.ceil(c_paint(p)[0]))]


def tin_txt(t):
    return f"{dec1(t)} L" if Fr(t).denominator != 1 else f"{int(t)} L"


def t_paint(p, v):
    return [f"A wall is {p['l']} m long and {p['h']} m high, with {p['win']} m\u00b2 of windows that are not painted. "
            f"It needs {p['coats']} coat{'s' if p['coats'] != 1 else ''}. One litre of paint covers {p['cov']} m\u00b2 "
            f"per coat, and paint is sold in {tin_txt(p['tin'])} tins (you must buy whole tins).",
            f"Paint job: wall {p['l']} m by {p['h']} m, minus {p['win']} m\u00b2 of glazing; {p['coats']} "
            f"coat{'s' if p['coats'] != 1 else ''}; coverage {p['cov']} m\u00b2 per litre per coat; paint comes only "
            f"in whole {tin_txt(p['tin'])} tins."][v]


def g_int(rng):
    return dict(P=rng.randrange(100000, 2000000, 10000), r=rng.choice([2, 3, 4, 5, 6, 8]), y=rng.randint(2, 7))


def c_int(p):
    i = Fr(p["P"]) * p["r"] * p["y"] / 100
    return i, p["P"] + i


W_INT = [lambda p: (Fr(p["P"]) * p["r"] / 100, p["P"] + Fr(p["P"]) * p["r"] / 100),  # one year only
         lambda p: (Fr(p["P"]) * p["r"] * p["y"] / 100, Fr(p["P"]) * p["r"] * p["y"] / 100),  # total = interest
         lambda p: (Fr(p["P"]) * p["r"] * (p["y"] + 1) / 100, p["P"] + Fr(p["P"]) * p["r"] * (p["y"] + 1) / 100),
         lambda p: (Fr(p["P"]) * p["r"] * p["y"] / 1000, p["P"] + Fr(p["P"]) * p["r"] * p["y"] / 1000)]


def t_int(p, v):
    return [f"{money(p['P'])} is placed in an account paying {p['r']}% simple interest per year (interest is not "
            f"added to the balance until the end). It stays there for {p['y']} years.",
            f"A loan of {money(p['P'])} is charged simple interest at {p['r']}% a year for {p['y']} years."][v]


def g_elec(rng):
    s = rng.randrange(10000, 90000)
    return dict(s=s, e=s + rng.randrange(150, 1500), rate=rng.randrange(18, 40), sc=rng.randrange(30, 65),
                days=rng.choice([28, 30, 31, 90, 91, 92]))


def c_elec(p):
    units = p["e"] - p["s"]
    return Fr(units), Fr(units) * p["rate"] + p["sc"] * p["days"]


W_ELEC = [lambda p: (Fr(p["e"] - p["s"]), Fr(p["e"] - p["s"]) * p["rate"]),  # standing charge forgotten
          lambda p: (Fr(p["e"] - p["s"]), Fr(p["e"] - p["s"]) * p["rate"] + p["sc"] * 30),
          lambda p: (Fr(p["e"] - p["s"] + 100), Fr(p["e"] - p["s"] + 100) * p["rate"] + p["sc"] * p["days"]),
          lambda p: (Fr(p["e"] - p["s"]), Fr(p["e"] - p["s"]) * p["rate"] + p["sc"])]


def t_elec(p, v):
    return [f"The electricity meter read {p['s']:,} kWh at the start of the billing period and {p['e']:,} kWh at the "
            f"end. The unit rate is {p['rate']}p per kWh and the standing charge is {p['sc']}p per day for the "
            f"{p['days']}-day period.",
            f"Meter readings: {p['s']:,} (opening) and {p['e']:,} (closing), both in kWh. Tariff: {p['rate']}p/kWh plus "
            f"{p['sc']}p per day standing charge; the bill covers {p['days']} days."][v]


def g_tiles(rng):
    return dict(l=rng.randrange(4, 20) * 5, w=rng.randrange(4, 16) * 5, waste=rng.choice([0, 5, 10, 10, 15]),
                box=rng.choice([8, 10, 12, 16, 20]))


def c_tiles(p):
    tiles = Fr(p["l"] * p["w"], 25) * (100 + p["waste"]) / 100
    t = math.ceil(tiles)
    return t, math.ceil(Fr(t, p["box"]))


W_TILES = [lambda p: (math.ceil(Fr(p["l"] * p["w"], 25)), math.ceil(Fr(math.ceil(Fr(p["l"] * p["w"], 25)), p["box"]))),
           lambda p: (c_tiles(p)[0], c_tiles(p)[0] // p["box"]),
           lambda p: (math.ceil(Fr(p["l"] * p["w"], 50) * (100 + p["waste"]) / 100),
                      math.ceil(Fr(math.ceil(Fr(p["l"] * p["w"], 50) * (100 + p["waste"]) / 100), p["box"]))),
           lambda p: (c_tiles(p)[0] + 1, math.ceil(Fr(c_tiles(p)[0] + 1, p["box"])))]


def t_tiles(p, v):
    L, W = Fr(p["l"], 10), Fr(p["w"], 10)
    extra = f" plus {p['waste']}% extra for cutting (round the tile count up)" if p["waste"] else \
        " (no allowance for cutting)"
    a = "an" if dec1(L).startswith(("8", "11.", "18.")) else "a"
    return [f"A floor measures {dec1(L)} m by {dec1(W)} m. It is covered with 50 cm x 50 cm tiles,{extra}. Tiles come "
            f"in boxes of {p['box']}, and only whole boxes are sold.",
            f"Tiling {a} {dec1(L)} m x {dec1(W)} m floor with square tiles 0.5 m on a side{extra}; boxes hold "
            f"{p['box']} tiles and cannot be split."][v]


def g_ship(rng):
    return dict(a=rng.randrange(600, 1500, 25), b=rng.randrange(150, 450, 25), w1=rng.randrange(5, 120),
                w2=rng.randrange(5, 120))


def cost_ship(a, b, w10):
    kg = math.ceil(Fr(w10, 10))
    return Fr(a + b * (kg - 1))


def c_ship(p):
    c1 = cost_ship(p["a"], p["b"], p["w1"])
    return c1, c1 + cost_ship(p["a"], p["b"], p["w2"])


W_SHIP = [lambda p: (Fr(p["a"]) + p["b"] * (Fr(p["w1"], 10) - 1), Fr(p["a"]) + p["b"] * (Fr(p["w1"], 10) - 1)
                     + Fr(p["a"]) + p["b"] * (Fr(p["w2"], 10) - 1)),  # no rounding up
          lambda p: (Fr(p["a"] + p["b"] * math.ceil(Fr(p["w1"], 10))),
                     Fr(p["a"] + p["b"] * math.ceil(Fr(p["w1"], 10))) + p["a"] + p["b"] * math.ceil(Fr(p["w2"], 10))),
          lambda p: (c_ship(p)[0], cost_ship(p["a"], p["b"], p["w1"] + p["w2"])),  # combined weight
          lambda p: (c_ship(p)[0], c_ship(p)[0] * 2)]


def t_ship(p, v):
    return [f"A courier charges {money(p['a'])} for the first kilogram and {money(p['b'])} for each additional "
            f"kilogram or part of a kilogram. Parcel 1 weighs {dec1(Fr(p['w1'], 10))} kg and parcel 2 weighs "
            f"{dec1(Fr(p['w2'], 10))} kg; each parcel is charged separately.",
            f"Courier rates: first kg {money(p['a'])}, then {money(p['b'])} per extra kg (any part of a kg counts as a "
            f"whole kg). Two parcels are sent separately: {dec1(Fr(p['w1'], 10))} kg and {dec1(Fr(p['w2'], 10))} kg."][v]


TEMPLATES = {
    "bill": dict(gen=g_bill, calc=c_bill, wrong=W_BILL, text=t_bill, f1=money, f2=money, prec=(1, 1),
                 alts=[("p", [10, 12, 15, 18, 20, 25]), ("n", "pm1")], area="restaurant bill",
                 ask="the total including the tip and the amount each person pays",
                 both=["Total with tip {a}; each person pays {b}.", "The bill comes to {a} in total, so everyone pays {b}.",
                       "{a} altogether, which is {b} each."],
                 one=["The total including the tip is {a}.", "Each person pays {b}."]),
    "disc": dict(gen=g_disc, calc=c_disc, wrong=W_DISC, text=t_disc, f1=money, f2=money, prec=(1, 1),
                 alts=[("d", [10, 15, 20, 25, 30, 40, 50]), ("t", [5, 6, 8, 10, 20])], area="sale price",
                 ask="the sale price before tax and the final price including tax",
                 both=["Sale price {a}; with tax {b}.", "After the discount it is {a}, and {b} once tax is added.",
                       "{a} before tax, {b} after tax."],
                 one=["The sale price before tax is {a}.", "The final price with tax is {b}."]),
    "ot": dict(gen=g_ot, calc=c_ot, wrong=W_OT, text=t_ot, f1=money, f2=money, prec=(1, 1),
               alts=[("h", "pm2"), ("base", [37, 38, 40])], area="overtime pay",
               ask="the overtime pay and the total pay for the week",
               both=["Overtime pay {a}; total pay {b}.", "The overtime comes to {a}, making {b} for the week.",
                     "{a} of overtime, {b} in total."],
               one=["The overtime pay is {a}.", "Total pay for the week is {b}."]),
    "recipe": dict(gen=g_recipe, calc=c_recipe, wrong=W_RECIPE, text=t_recipe, f1=lambda x: f"{int(x)} g",
                   f2=lambda x: f"{int(x)} ml", prec=(1, 1), alts=[("t", [3, 5, 6, 9, 10, 12, 15, 20])],
                   area="recipe scaling", ask="how much flour and how much milk are needed",
                   both=["Flour {a}, milk {b}.", "You need {a} of flour and {b} of milk.", "{a} flour and {b} milk."],
                   one=["You need {a} of flour.", "You need {b} of milk."]),
    "trip": dict(gen=g_trip, calc=c_trip, wrong=W_TRIP, text=t_trip, f1=hm, f2=clock, prec=(1, 1),
                 alts=[("v", [40, 45, 48, 50, 60, 64, 72, 75, 80, 90, 96, 100, 120])], area="journey time",
                 ask="the journey time and the arrival time",
                 both=["Journey time {a}; arrival at {b}.", "It takes {a}, arriving at {b}.", "{a} on the road, in at {b}."],
                 one=["The journey takes {a}.", "It arrives at {b}."]),
    "fuel": dict(gen=g_fuel, calc=c_fuel, wrong=W_FUEL, text=t_fuel, f1=lambda x: f"{dec1(x)} L", f2=money,
                 prec=(10, 1), alts=[("c", [45, 50, 55, 60, 64, 65, 70, 72, 75, 80, 85, 90])], area="fuel cost",
                 ask="how many litres of fuel the trip uses and what that fuel costs",
                 both=["Fuel used {a}; cost {b}.", "The trip needs {a}, costing {b}.", "{a} of fuel, {b}."],
                 one=["The trip uses {a} of fuel.", "The fuel costs {b}."]),
    "paint": dict(gen=g_paint, calc=c_paint, wrong=W_PAINT, text=t_paint, f1=lambda x: f"{dec1(x)} L",
                  f2=lambda x: f"{int(x)} tin" + ("" if int(x) == 1 else "s"), prec=(10, 1),
                  alts=[("coats", [1, 2, 3]), ("win", "pm1")], area="paint quantity",
                  ask="how many litres of paint are needed and how many tins must be bought",
                  both=["Paint needed {a}; buy {b}.", "You need {a} of paint, so {b}.", "{a}, which means {b}."],
                  one=["You need {a} of paint.", "Buy {b}."]),
    "int": dict(gen=g_int, calc=c_int, wrong=W_INT, text=t_int, f1=money, f2=money, prec=(1, 1),
                alts=[("y", "pm1"), ("r", [2, 3, 4, 5, 6, 8])], area="simple interest",
                ask="the total interest and the final amount (principal plus interest)",
                both=["Interest {a}; final amount {b}.", "It earns {a}, so the final amount is {b}.",
                      "{a} interest, {b} in total."],
                one=["The interest is {a}.", "The final amount is {b}."]),
    "elec": dict(gen=g_elec, calc=c_elec, wrong=W_ELEC, text=t_elec, f1=lambda x: f"{int(x):,} kWh", f2=pounds,
                 prec=(1, 1), alts=[("days", [28, 30, 31, 90, 91, 92]), ("rate", "pm1")], area="electricity bill",
                 ask="the electricity used and the total bill",
                 both=["Usage {a}; bill {b}.", "You used {a}, so the bill is {b}.", "{a}, costing {b}."],
                 one=["You used {a}.", "The bill is {b}."]),
    "tiles": dict(gen=g_tiles, calc=c_tiles, wrong=W_TILES, text=t_tiles, f1=lambda x: f"{int(x)} tiles",
                  f2=lambda x: f"{int(x)} box" + ("" if int(x) == 1 else "es"), prec=(1, 1),
                  alts=[("box", [8, 10, 12, 16, 20]), ("waste", [0, 5, 10, 15])], area="tiling",
                  ask="how many tiles are needed and how many boxes must be bought",
                  both=["{a} needed; buy {b}.", "You need {a}, which means {b}.", "{a} in {b}."],
                  one=["You need {a}.", "Buy {b}."]),
    "ship": dict(gen=g_ship, calc=c_ship, wrong=W_SHIP, text=t_ship, f1=money, f2=money, prec=(1, 1),
                 alts=[("w1", "pm5"), ("b", "pm25")], area="courier charges",
                 ask="the charge for parcel 1 and the total charge for both parcels",
                 both=["Parcel 1 costs {a}; both together {b}.", "{a} for parcel 1 and {b} in total.",
                       "Parcel 1: {a}. Total: {b}."],
                 one=["Parcel 1 costs {a}.", "The total for both parcels is {b}."]),
}


def ok_params(tk, p):
    T = TEMPLATES[tk]
    try:
        v1, v2 = T["calc"](p)
    except (ZeroDivisionError, ValueError):
        return False
    s1, s2 = T["prec"]
    if not exact(v1, scale=s1) or not exact(v2, scale=s2):
        return False
    if Fr(v1) <= 0 or Fr(v2) <= 0:
        return False
    if tk == "trip" and (p["dep"] + v1) >= 1440:
        return False
    if tk == "paint" and p["l"] * p["h"] - p["win"] <= 0:
        return False
    return True


def fmt_pair(tk, pair):
    T = TEMPLATES[tk]
    return T["f1"](pair[0]), T["f2"](pair[1])


def valid_pair(tk, pair):
    T = TEMPLATES[tk]
    s1, s2 = T["prec"]
    return exact(pair[0], scale=s1) and exact(pair[1], scale=s2) and Fr(pair[0]) > 0 and Fr(pair[1]) > 0


def alt_params(tk, p, rng):
    T = TEMPLATES[tk]
    out = []
    for name, spec in T["alts"]:
        if isinstance(spec, list):
            vals = [x for x in spec if x != p[name]]
        else:
            step = int(spec[2:])
            vals = [p[name] + step, p[name] - step, p[name] + 2 * step, p[name] - 2 * step]
        for v in vals:
            q = dict(p)
            q[name] = v
            if name == "n" and v < 2:
                continue
            if name in ("win",) and v < 0:
                continue
            if ok_params(tk, q) and fmt_pair(tk, T["calc"](q)) != fmt_pair(tk, T["calc"](p)):
                out.append((name, v, q))
    return out


def sample(rng):
    tk = rng.choice(sorted(TEMPLATES))
    T = TEMPLATES[tk]
    for _ in range(200):
        p = T["gen"](rng)
        if ok_params(tk, p):
            break
    else:
        return None
    correct = fmt_pair(tk, T["calc"](p))
    word, scheme = rng.choice(LABELS)
    n = rng.choice([3, 4, 4, 5, 5, 6])
    answers = []
    seen = {correct}
    # a misread-number answer (correct for a nearby version of the problem) makes a natural twin
    alts = alt_params(tk, p, rng)
    rng.shuffle(alts)
    misread = None
    for name, v, q in alts:
        pr = fmt_pair(tk, T["calc"](q))
        if pr not in seen:
            misread = (name, v, pr)
            seen.add(pr)
            answers.append({"vals": list(pr), "kind": "misread", "misread": [name, v]})
            break
    wrongs = list(T["wrong"])
    rng.shuffle(wrongs)
    for wf in wrongs:
        try:
            pr = wf(p)
        except (ZeroDivisionError, ValueError):
            continue
        if not valid_pair(tk, pr):
            continue
        f = fmt_pair(tk, pr)
        if f in seen:
            continue
        seen.add(f)
        answers.append({"vals": list(f), "kind": "slip"})
    has_correct = rng.random() < 0.85
    if has_correct:
        answers.append({"vals": list(correct), "kind": "correct"})
    # incomplete answers (one value right, the other missing) and one-value-wrong answers
    if rng.random() < 0.6:
        k = rng.randrange(2)
        vals = [correct[0], None] if k == 0 else [None, correct[1]]
        answers.append({"vals": vals, "kind": "incomplete"})
    if len(answers) < n:
        for a in list(answers):
            if a["kind"] == "slip" and a["vals"][0] != correct[0] and a["vals"][1] != correct[1] and rng.random() < 0.5:
                mix = [correct[0], a["vals"][1]] if rng.random() < 0.5 else [a["vals"][0], correct[1]]
                if tuple(mix) not in seen:
                    seen.add(tuple(mix))
                    answers.append({"vals": mix, "kind": "half"})
                    break
    rng.shuffle(answers)
    if not has_correct and not any(a["kind"] in ("misread",) for a in answers):
        pass
    answers = answers[:n] if len(answers) > n else answers
    if len(answers) < 3:
        return None
    if has_correct and not any(a["kind"] == "correct" for a in answers):
        return None
    labels = [f"{word} {LET[i] if scheme == 'L' else i + 1}" for i in range(len(answers))]
    for a, L in zip(answers, labels):
        a["label"] = L
        a["style"] = rng.randrange(3)
    item = {"tk": tk, "p": p, "answers": answers, "word": word,
            "r": {"text": rng.randrange(2), "q": rng.randrange(1000), "rule": rng.randrange(3), "lay": rng.randrange(3),
                  "names": rng.sample(["Ana", "Ben", "Chen", "Dev", "Eli", "Femi", "Gus", "Ines", "Jo"], len(answers))}}
    return item


def grade(item):
    tk = item["tk"]
    T = TEMPLATES[tk]
    c = fmt_pair(tk, T["calc"](item["p"]))
    ok = [a["label"] for a in item["answers"] if a["vals"][0] == c[0] and a["vals"][1] == c[1]]
    if not ok:
        return "NONE"
    if len(ok) > 1:
        return "MULTI"
    return ok[0]


def answer_text(item, a):
    T = TEMPLATES[item["tk"]]
    v1, v2 = a["vals"]
    if v1 is not None and v2 is not None:
        return T["both"][a["style"]].format(a=v1, b=v2)
    if v1 is not None:
        return T["one"][0].format(a=v1)
    return T["one"][1].format(b=v2)


def none_opt(word):
    return f"none of the {word.lower()}s"


def render(item):
    T = TEMPLATES[item["tk"]]
    r = item["r"]
    w = item["word"].lower()
    prob = T["text"](item["p"], r["text"])
    task = f"Task: find {T['ask']}."
    rule = [f"Marking rule: an {w} is correct and complete only if it gives both requested values and both are exactly "
            f"right for the figures given (to the precision shown). An {w} that gives only one value is incomplete.",
            f"Only an {w} that states both requested values, each exactly right, counts as correct and complete; a "
            f"missing value makes it incomplete.",
            f"To pass, an {w} must give both values asked for, and both must be exactly correct for the problem as "
            f"stated."][r["rule"]]
    rule = rule.replace("an solution", "a solution").replace("An solution", "A solution")
    lines = []
    for a, nm in zip(item["answers"], r["names"]):
        txt = answer_text(item, a)
        lines.append([f"{a['label']} ({nm}): {txt}", f"{a['label']}: \"{txt}\"", f"- {a['label']}, from {nm}: {txt}"][r["lay"]])
    head = ["Worked problem (" + T["area"] + ")", "Maths check: " + T["area"], "Homework question"][r["lay"]]
    state = fix_articles(f"{head}\n\n{prob}\n{task}\n\n{rule}\n\nSubmitted {w}s:\n" + "\n".join(lines))
    q = ["Which {w} is correct and complete?", "Under the marking rule, which {w} is right?",
         "Which {w} gives both requested values exactly right?", "Which submitted {w} passes the marking rule?"]
    ins = q[r["q"] % len(q)].format(w=w)
    opts = [a["label"] for a in item["answers"]] + [none_opt(item["word"])]
    return state, ins, opts


def gold_option(item, out):
    return none_opt(item["word"]) if out == "NONE" else out


def edges(item):
    e = ["numeric", "multi_hop"]
    if item["tk"] in ("trip",):
        e += ["temporal", "units"]
    if item["tk"] in ("fuel", "elec", "recipe", "tiles", "paint"):
        e.append("units")
    if any(None in a["vals"] for a in item["answers"]):
        e.append("missing_info")
    return list(dict.fromkeys(e))


def twin(item, rng, base_out):
    tk = item["tk"]
    T = TEMPLATES[tk]
    cands = []
    for name, v, q in alt_params(tk, item["p"], rng):
        it2 = copy.deepcopy(item)
        it2["p"] = q
        o2 = grade(it2)
        if o2 not in (base_out, "MULTI"):
            w = 3.0 if o2 != "NONE" else 0.15
            cands.append((it2, {"type": "problem", "param": name, "old": item["p"][name], "new": v}, o2, w))
    c = fmt_pair(tk, T["calc"](item["p"]))
    for i, a in enumerate(item["answers"]):
        for k in range(2):
            if a["vals"][k] is None:
                continue
            if a["vals"][k] == c[k]:
                # break a correct value (use a slip value from another answer, if any)
                pool = [b["vals"][k] for b in item["answers"] if b["vals"][k] not in (None, c[k])]
                if not pool:
                    continue
                nv = rng.choice(pool)
            else:
                nv = c[k]
            it2 = copy.deepcopy(item)
            it2["answers"][i]["vals"][k] = nv
            if any(b["vals"] == it2["answers"][i]["vals"] for j, b in enumerate(it2["answers"]) if j != i):
                continue
            o2 = grade(it2)
            if o2 not in (base_out, "MULTI"):
                cands.append((it2, {"type": "answer", "label": a["label"], "slot": k, "old": a["vals"][k], "new": nv},
                              o2, 0.3 if o2 == "NONE" else 1.0))
    if not cands:
        return None
    it2, desc, o2, _ = rng.choices(cands, weights=[x[3] for x in cands])[0]
    return it2, desc, o2


def build(rng):
    it = sample(rng)
    if it is None:
        return None
    out = grade(it)
    if out == "MULTI":
        return None
    return it, out
