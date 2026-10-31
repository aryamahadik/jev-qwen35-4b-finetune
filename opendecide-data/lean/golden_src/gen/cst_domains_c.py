"""gen_constraints domains, part C: personal loans, cloud servers, trains, gyms, volunteers for a shift, parking,
grant programs, used cars, software vendors.  All names are invented."""
import datetime as dt
from fractions import Fraction as Fr

from cst_core import GE, GT, LE, LT, MISSING, NA, Attr, CmpCon, FnCon, cap, fmt_dur, fmt_money, fmt_time, modal, unk
from cst_dom_base import (FIRST, PEOPLE, Domain, mk_bool, mk_cat, mk_cmp, mk_cond, mk_date, mk_derived, mk_exc,
                          mk_implicit, mk_range, mk_set, mk_tie, mk_window, mk_xunit, money_fmt)
from cst_domains_a import CITIES, base_day, fd, ft, pick_name

# ================================================================================================ loans
LOAN_LABELS = ["Harbor CU Personal", "Keystone Bank Flex", "Summit Lending Fixed", "Northwind Credit Plus",
               "Clearwater Bank Standard", "Evergreen CU Saver", "Beacon Finance Direct", "Riverbend Loans Basic",
               "Pinnacle Bank Select", "Oakmont Credit Union", "Lakeside Lending", "Granite Bank Personal",
               "Meridian CU Flex", "Cobalt Finance", "Fairway Bank Fixed", "Halyard Credit", "Ironwood Lending",
               "Juniper Bank Easy", "Kingfisher CU", "Lodestar Finance", "Maplewood Bank", "Nimbus Credit",
               "Orchard CU Personal", "Prairie Bank Fixed"]
LOAN_ATTRS = [
    Attr("apr", "num", "APR", lo=450, hi=2499, step=5, scale=100, unit="%", vp=["have an APR of {c} {v}"],
         field=("Max APR", None), pr="charges an APR of {v}", missing_ok=False),
    Attr("term", "num", "Term", lo=12, hi=84, step=12, unit=("month", "months"), cls="count", vp=["run for {c} {v}"],
         pr="runs for {v}", missing_ok=False),
    Attr("fee", "num", "Origination fee", lo=0, hi=60, step=5, scale=10, unit="%", vp=["charge an origination fee of {c} {v}"],
         field=("Max origination fee", None), pr="charges a {v} origination fee"),
    Attr("minscore", "num", "Minimum credit score", lo=580, hi=760, step=10, pr="requires a credit score of {v}",
         missing_ok=False),
    Attr("maxamt", "money", "Maximum loan", lo=500000, hi=5000000, step=100000, pr="lends up to {v}", missing_ok=False),
    Attr("penalty", "bool", "Prepayment penalty", p=0.35, vp=["charge a prepayment penalty"],
         anti=["let us repay early without a penalty"], pr=("charges a prepayment penalty", "has no prepayment penalty")),
    Attr("fund", "num", "Funding time", lo=1, hi=10, unit=("business day", "business days"), cls="count",
         vp=["fund the loan in {c} {v}"], pr="funds in {v}"),
    Attr("autopay", "bool", "Autopay discount", p=0.5, vp=["offer an autopay discount"],
         pr=("offers an autopay discount", "has no autopay discount")),
]


def _loan_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng),
            "use": rng.choice(["consolidate two credit cards", "pay for a car repair", "cover a home renovation",
                               "pay a tuition bill", "replace a boiler"])}


LOAN = Domain(
    "loan", "loan offer", "loan offers", "Lender", LOAN_LABELS, LOAN_ATTRS,
    makers=[
        (3, "apr", mk_cmp("apr", LE, 0.15, 0.6)),
        (2, "apr", mk_exc("apr", "autopay", LE, "it offers an autopay discount", gap=(10, 40), f0=0.1, f1=0.5)),
        (3, "score", mk_implicit("minscore", LE, lambda rng, ctx, D: rng.randrange(600, 751, 5),
                                 lambda rng, ctx, t: ("The applicant's credit score is {v}.", None),
                                 "accept the applicant's credit score (its minimum cannot be higher)",
                                 vfmt=lambda t, st: str(t))),
        (3, "amt", mk_implicit("maxamt", GE, lambda rng, ctx, D: 100000 * rng.randint(8, 45),
                               lambda rng, ctx, t: ("The amount needed is {v}.", None), "lend the full amount needed",
                               vfmt=money_fmt())),
        (2, "penalty", mk_bool("penalty", want=False)),
        (2, "fee", mk_cmp("fee", LE, 0.1, 0.5, neg_p=0.3)),
        (2, "term", mk_cmp("term", LE, strict_p=0.0, tlo=36, thi=60, tstep=12)),
        (1, "fund", mk_cmp("fund", LE, 0.1, 0.5, strict_p=0.0)),
    ],
    ties=[mk_tie("apr", [(("a", "apr"), "min")], "the lowest APR", ["apr"]),
          mk_tie("fee", [(("a", "fee"), "min"), (("a", "apr"), "min")], "the lowest origination fee (then the lower APR)",
                 ["fee", "apr"])],
    ctx_fn=_loan_ctx, cur="$",
    contexts=[("I'm taking out a personal loan to {use}.", "{name} is taking out a personal loan to {use}."),
              ("I've been pre-qualified by several lenders and need a loan to {use}.",
               "{name} has been pre-qualified by several lenders and needs a loan to {use}.")],
    questions=["Which loan offer should {name} accept{ifany}?", "Which offer meets all of the borrowing requirements{ifany}?",
               "Which of the listed loans satisfies every requirement{ifany}?"],
    intros=["Pre-qualified offers:", "Loan offers:", "Lenders that replied:"],
    subjects=["Loan offers", "Personal loan"],
    nice=["autopay"],
)

# ================================================================================================ cloud servers
PROVIDERS = ["Nimbus", "Stratus", "Cirrus"]
FAMS = ["std", "cpu", "mem", "gen", "burst"]
SIZES = ["small", "medium", "large", "xlarge", "2xlarge", "4xlarge"]
CLOUD_LABELS = [f"{p} {f}.{s}" for p in PROVIDERS for f in FAMS for s in SIZES]
REGIONS = ["us-east", "us-west", "eu-central", "eu-west", "ap-south", "ap-east"]
CLOUD_ATTRS = [
    Attr("vcpu", "num", "vCPUs", lo=2, hi=64, unit=None, gen=lambda rng, ctx, o: rng.choice([2, 4, 8, 16, 32, 64]),
         cls="count", pr="has {v} vCPUs", missing_ok=False),
    Attr("ram", "num", "Memory", lo=4, hi=512, unit=" GB", gen=lambda rng, ctx, o: rng.choice([4, 8, 16, 32, 64, 128, 256, 512]),
         vp=["have {c} {v} of memory"], field=(None, "Min memory"), pr="has {v} of memory", missing_ok=False),
    Attr("region", "cat", "Region", cats=REGIONS, vp=["run in {v}"], pr="runs in {v}", missing_ok=False),
    Attr("hourly", "money", "Price per hour", lo=5, hi=900, step=1, cents=True, vp=["cost {c} {v} an hour"],
         field=("Max hourly price", None), pr="costs {v} an hour", missing_ok=False),
    Attr("sla", "num", "Uptime SLA", lo=9900, hi=9999, step=1, scale=100, unit="%",
         gen=lambda rng, ctx, o: rng.choice([9900, 9950, 9990, 9995, 9999]), vp=["guarantee uptime of {c} {v}"],
         field=(None, "Min uptime SLA"), pr="guarantees {v} uptime"),
    Attr("gpu", "bool", "GPU", p=0.3, vp=["include a GPU"], noun="a GPU", pr=("includes a GPU", "has no GPU")),
    Attr("ssd", "num", "Local SSD", lo=0, hi=2000, unit=" GB", gen=lambda rng, ctx, o: rng.choice([0, 50, 100, 200, 400, 800, 1600]),
         vp=["have {c} {v} of local SSD"], pr="has {v} of local SSD"),
]


def _mk_vcpu(rng, ctx, D):
    t = rng.choice([4, 8, 16])
    a = D.A["vcpu"]
    return CmpCon("vcpu", a, GE, t, "neg" if rng.random() < 0.15 else "pos", wi=rng.randrange(12), vpi=0,
                  vp=["have {c} {v} vCPUs"], vfmt=lambda t, st: str(t), lo=2, hi=32, step=1, vstep=4)


def _cloud_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng),
            "job": rng.choice(["a customer database", "a nightly batch job", "an internal wiki", "a web API",
                               "a data pipeline", "a build server"])}


CLOUD = Domain(
    "cloud_instance", "server type", "server types", "Instance", CLOUD_LABELS, CLOUD_ATTRS,
    makers=[
        (3, "vcpu", _mk_vcpu),
        (3, "ram", mk_cmp("ram", GE, strict_p=0.0, tlo=16, thi=128, tstep=16)),
        (3, "region", mk_cat("region", (1, 2), neg_p=0.3)),
        (2, "hourly", mk_cmp("hourly", LE, 0.1, 0.6)),
        (3, "month", mk_derived("month", ["hourly"], lambda ctx: ("*", ("a", "hourly"), ("k", 730)), LE,
                                lambda rng, ctx, D: 1000 * rng.randint(10, 400),
                                ["cost {c} {v} a month", "come to {c} {v} per month"], money_fmt(),
                                ctx_fn=lambda ctx, st, ci: "Count a month as 730 hours of running time.", step=1000,
                                tags=("numeric", "multi_hop", "units"), group="hourly")),
        (2, "sla", mk_cmp("sla", GE, strict_p=0.0, tlo=9950, thi=9995, tstep=45)),
        (1, "gpu", mk_bool("gpu")),
        (1, "ssd", mk_cmp("ssd", GE, strict_p=0.0, tlo=100, thi=400, tstep=100)),
    ],
    ties=[mk_tie("hourly", [(("a", "hourly"), "min")], "the lowest hourly price", ["hourly"]),
          mk_tie("ram", [(("a", "ram"), "max"), (("a", "hourly"), "min")], "the most memory (then the lower price)",
                 ["ram", "hourly"])],
    ctx_fn=_cloud_ctx,
    contexts=[("I'm choosing a server type to host {job}.", "{name} is choosing a server type to host {job}."),
              ("We're moving {job} to the cloud and need one instance type.", "{name}'s team is moving {job} to the cloud and needs one instance type.")],
    questions=["Which server type should {name} pick{ifany}?", "Which instance type meets every requirement{ifany}?",
               "Which of the listed server types satisfies all of the requirements{ifany}?"],
    intros=["Instance types in the price list:", "Candidate instance types:", "Server options:"],
    subjects=["Server for {job}", "Instance type"],
)

# ================================================================================================ trains
TRAIN_LABELS = [f"Train {n}" for n in [1024, 1031, 1047, 1052, 1068, 1075, 1083, 1096, 1102, 1119, 1127, 1134, 1146,
                                      1153, 1161, 1178, 1185, 1192, 1204, 1217, 1223, 1238, 1246, 1259, 1263, 1271,
                                      1284, 1297, 1305, 1316]]
OPERATORS = ["Northern Rail Link", "Coastway Trains", "Midland Express", "Lakeshore Rail"]


def _tr_derive(o, ctx):
    d, u = o.get("dep"), o.get("dur")
    o["arr"] = MISSING if (d is None or u is None or unk(d) or unk(u)) else d + u


def _tr_valid(o, ctx):
    a = o.get("arr")
    if a is not None and not unk(a) and a > 23 * 60 + 55:
        return False
    c, u = o.get("chg"), o.get("dur")
    if c is not None and u is not None and not unk(c) and not unk(u) and c > 0 and u < 60 + 30 * c:
        return False
    return True


def _chg_pr(v, s):
    return "is direct" if v == 0 else f"needs {s}"


TRAIN_ATTRS = [
    Attr("dep", "time", "Departs", lo=5 * 60, hi=21 * 60, step=5, cls="time", vp=["leave {c} {v}", "depart {c} {v}"],
         field=("Latest departure", "Earliest departure"), pr="leaves at {v}", missing_ok=False),
    Attr("dur", "dur", "Journey time", lo=40, hi=360, step=5, vp=["take {c} {v}"], field=("Max journey time", None),
         pr="takes {v}", missing_ok=False),
    Attr("arr", "time", "Arrives", derived=True, cls="time", vp=["arrive {c} {v}", "get in {c} {v}"],
         field=("Latest arrival", None), pr="arrives at {v}"),
    Attr("chg", "num", "Changes", lo=0, hi=3, unit=("change", "changes"), cls="count", pr=_chg_pr, missing_ok=False,
         gen=lambda rng, ctx, o: rng.choice([0, 0, 1, 1, 2, 3])),
    Attr("fare", "money", "Fare", lo=900, hi=15000, step=50, cents=True, vp=["cost {c} {v}"], field=("Max fare", None),
         pr="costs {v}", missing_ok=False),
    Attr("bike", "bool", "Bike space", p=0.5, vp=["have space for a bike"], pr=("has bike space", "has no bike space")),
    Attr("seat", "bool", "Seat reservation", p=0.5, vp=["include a seat reservation"], noun="a seat reservation",
         pr=("includes a seat reservation", "has no seat reservation")),
    Attr("op", "cat", "Operator", cats=OPERATORS, vp=["be run by {v}"], pr="is run by {v}", missing_ok=False),
    Attr("quiet", "bool", "Quiet coach", p=0.5, vp=["have a quiet coach"], pr=("has a quiet coach", "has no quiet coach")),
]
TRAIN_ATTRS[3].special = {0: "direct"}


def _train_ctx(rng):
    a, b = rng.sample(["Leeds", "York", "Bristol", "Cardiff", "Glasgow", "Edinburgh", "Norwich", "Exeter", "Carlisle",
                       "Durham", "Preston", "Bath"], 2)
    return {"today": base_day(rng), "name": pick_name(rng), "orig": a, "dest": b}


TRAIN = Domain(
    "train", "train", "trains", "Service", TRAIN_LABELS, TRAIN_ATTRS,
    makers=[
        (4, "arr", mk_cmp("arr", LE, strict_p=0.2, tlo=9 * 60, thi=22 * 60, tstep=15, attrs=["dep", "dur"],
                          lo=6 * 60, hi=23 * 60, step=15, vstep=15)),
        (2, "dep", mk_cmp("dep", GE, 0.1, 0.5, strict_p=0.2)),
        (2, "chg", mk_cmp("chg", LE, strict_p=0.0, tlo=1, thi=1, tstep=1, lo=1, hi=2, vp=["involve {c} {v}"])),
        (3, "fare", mk_cmp("fare", LE, 0.2, 0.7)),
        (2, "bike", mk_bool("bike")),
        (1, "seat", mk_bool("seat")),
        (1, "op", mk_cat("op", (1, 1), only_neg=True)),
        (2, "dur", mk_cmp("dur", LE, 0.2, 0.7)),
        (1, "quiet", mk_bool("quiet")),
    ],
    ties=[mk_tie("arr", [(("a", "arr"), "min")], "the earliest arrival", ["dep", "dur"]),
          mk_tie("fare", [(("a", "fare"), "min")], "the lowest fare", ["fare"]),
          mk_tie("chg", [(("a", "chg"), "min"), (("a", "fare"), "min")], "the fewest changes (then the lower fare)",
                 ["chg", "fare"])],
    ctx_fn=_train_ctx, derive=_tr_derive, valid=_tr_valid, always=["dep", "arr", "dur"],
    cs=lambda ctx, st: {"tdate": fd(ctx["today"] + 3, st)},
    contexts=[("I'm travelling by train from {orig} to {dest} on {tdate}.", "{name} is travelling by train from {orig} to {dest} on {tdate}."),
              ("I need a train from {orig} to {dest} on {tdate}; all times are local.",
               "{name} needs a train from {orig} to {dest} on {tdate}; all times are local.")],
    questions=["Which train should {name} take{ifany}?", "Which service meets every travel requirement{ifany}?",
               "Which of the listed trains satisfies all of the requirements{ifany}?"],
    intros=["Journey planner results:", "Trains that day:", "Departures:"],
    subjects=["Train to {dest}", "{orig} to {dest}"],
    nice=["quiet", "seat"],
)

# ================================================================================================ gyms
GYM_LABELS = ["Ironworks Gym", "Pulse Fitness", "Harbor Athletic Club", "Summit Strength", "Core Collective",
              "Northside Leisure Centre", "Peak Performance Gym", "Riverside Fitness", "Kinetic Studio", "Forge Fitness",
              "Urban Motion Gym", "Anchor Fitness", "Blueline Health Club", "Cedar Wellness", "Dynamo Gym",
              "Elevate Fitness", "Foundry Gym", "Greenpark Leisure", "Hustle House", "Momentum Club"]
CLASSES = ["yoga", "spin", "HIIT", "pilates", "boxing", "swimming lessons"]
GYM_ATTRS = [
    Attr("monthly", "money", "Monthly fee", lo=1500, hi=12000, step=100, vp=["cost {c} {v} a month"],
         field=("Max monthly fee", None), pr="costs {v} a month", missing_ok=False),
    Attr("join", "money", "Joining fee", lo=0, hi=15000, step=500, pr="charges a {v} joining fee", missing_ok=False),
    Attr("opens", "time", "Opens", lo=5 * 60, hi=9 * 60, step=30, cls="time", vp=["open {c} {v}"],
         field=("Latest opening time", None), pr="opens at {v}", missing_ok=False),
    Attr("closes", "time", "Closes", lo=19 * 60, hi=23 * 60 + 30, step=30, cls="time", vp=["close {c} {v}"],
         field=(None, "Earliest closing time"), pr="closes at {v}", missing_ok=False),
    Attr("pool", "bool", "Pool", p=0.4, vp=["have a pool"], noun="a pool", pr=("has a pool", "has no pool")),
    Attr("classes", "set", "Classes", items=CLASSES, kset=(1, 4), vp=["run {v} classes", "offer {v} classes"],
         pr="runs {v} classes"),
    Attr("contract", "num", "Minimum contract", lo=0, hi=24, step=6, unit=("month", "months"), cls="count",
         vp=["have a minimum contract of {c} {v}"], pr="has a minimum contract of {v}", missing_ok=False),
    Attr("dist", "num", "Distance", lo=2, hi=120, scale=10, unit=" km", vp=["be {c} {v} away"], field=("Max distance", None),
         pr="is {v} away"),
]
GYM_ATTRS[6].special = {0: "none"}


def _gym_contract_pr(v, s):
    return "has minimum contract: none" if v == 0 else f"has a minimum contract of {s}"


GYM_ATTRS[6].pr = _gym_contract_pr


def _gym_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng), "city": rng.choice(CITIES)}


GYM = Domain(
    "gym", "gym", "gyms", "Gym", GYM_LABELS, GYM_ATTRS,
    makers=[
        (3, "year", mk_derived("year", ["monthly", "join"], lambda ctx: ("+", ("*", ("a", "monthly"), ("k", 12)), ("a", "join")),
                               LE, lambda rng, ctx, D: 5000 * rng.randint(6, 30),
                               ["cost {c} {v} for the first year, joining fee included"], money_fmt(), step=5000,
                               tags=("numeric", "multi_hop"), group="monthly")),
        (2, "monthly", mk_cmp("monthly", LE, 0.2, 0.7)),
        (3, "opens", mk_cmp("opens", LE, strict_p=0.15, tlo=6 * 60, thi=7 * 60, tstep=30, vp=["open {c} {v}"])),
        (2, "closes", mk_cmp("closes", GE, strict_p=0.15, tlo=21 * 60, thi=22 * 60 + 30, tstep=30)),
        (2, "pool", mk_bool("pool")),
        (3, "classes", mk_set("classes", modes=("has", "all", "k"), w=(4, 3, 2))),
        (2, "contract", mk_cmp("contract", LE, strict_p=0.0, neg_p=0.4, tlo=6, thi=12, tstep=6, lo=6, hi=24)),
        (1, "dist", mk_cmp("dist", LE, 0.1, 0.5)),
    ],
    ties=[mk_tie("year", [(("+", ("*", ("a", "monthly"), ("k", 12)), ("a", "join")), "min")],
                 "the lowest first-year cost (12 monthly fees plus the joining fee)", ["monthly", "join"],
                 tags=("multi_hop",)),
          mk_tie("dist", [(("a", "dist"), "min")], "the shortest distance", ["dist"])],
    ctx_fn=_gym_ctx,
    contexts=[("I'm joining a gym in {city}.", "{name} is joining a gym in {city}."),
              ("I want a gym membership that fits my schedule in {city}.", "{name} wants a gym membership that fits a busy schedule in {city}.")],
    questions=["Which gym should {name} join{ifany}?", "Which gym meets all of the requirements{ifany}?",
               "Which of the listed gyms satisfies every stated requirement{ifany}?"],
    intros=["Gyms nearby:", "Membership offers:", "Gyms I looked at:"],
    subjects=["Gym membership", "Which gym"],
    nice=["pool"],
)

# ================================================================================================ volunteers for a shift
VOL_ATTRS = [
    Attr("days", "set", "Available days", items=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], kset=(2, 5),
         vp=["be available on {v}", "be able to volunteer on {v}"], pr="is available on {v}", missing_ok=False),
    Attr("vfrom", "time", "Available from", lo=6 * 60, hi=14 * 60, step=30, cls="time", pr="is free from {v}",
         missing_ok=False),
    Attr("vto", "time", "Available until", lo=10 * 60, hi=22 * 60, step=30, cls="time",
         gen=lambda rng, ctx, o: min(22 * 60, (o.get("vfrom") if isinstance(o.get("vfrom"), int) else 9 * 60) + rng.randrange(120, 601, 30)),
         pr="is free until {v}", missing_ok=False),
    Attr("hours", "num", "Hours left this month", lo=0, hi=20, unit=("hour", "hours"), cls="count", pr="has {v} left this month"),
    Attr("aid", "bool", "First aid trained", p=0.5, vp=["be first-aid trained"], pr=("is first-aid trained", "is not first-aid trained")),
    Attr("check", "bool", "Background check", p=0.7, vp=["have a completed background check"],
         noun="a completed background check", pr=("has a completed background check", "has no completed background check")),
    Attr("langs", "set", "Languages", items=["English", "Spanish", "Arabic", "Polish", "Somali", "Urdu"], kset=(1, 3),
         vp=["speak {v}"], pr="speaks {v}"),
    Attr("drive", "bool", "Can drive the van", p=0.4, vp=["be able to drive the van"],
         pr=("can drive the van", "cannot drive the van")),
    Attr("shifts", "num", "Shifts done", lo=0, hi=40, unit=("shift", "shifts"), cls="count", vp=["have done {c} {v}"],
         pr="has done {v}"),
]


def _vol_valid(o, ctx):
    f, t = o.get("vfrom"), o.get("vto")
    if f is not None and t is not None and not unk(f) and not unk(t):
        return t >= f + 120
    return True


def _vol_ctx(rng):
    day = rng.choice(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    s = rng.randrange(8 * 60, 17 * 60, 30)
    ln = rng.choice([120, 180, 240, 300])
    return {"today": base_day(rng), "name": pick_name(rng), "day": day, "start": s, "end": s + ln, "len": ln // 60,
            "org": rng.choice(["the food bank", "the community kitchen", "the animal shelter", "the refugee welcome centre",
                               "the library homework club", "the charity shop"])}


FULLDAY = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday",
           "Sun": "Sunday"}


def _mk_vol_day(rng, ctx, D):
    from cst_core import SetCon
    c = SetCon("days", D.A["days"], "has", [ctx["day"]], 1, vpi=0)
    c.pool = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    c.fixed = True  # the shift day is stated in the context
    return c


VOLUNTEER = Domain(
    "volunteer", "volunteer", "volunteers", "Volunteer", PEOPLE, VOL_ATTRS,
    makers=[
        (4, "day", _mk_vol_day),
        (4, "window", mk_window("vfrom", "vto", "start", "end",
                                ["The shift runs from {s} to {e}.", "The shift starts at {s} and ends at {e}."],
                                ["be available for the whole shift", "be free for the entire shift"], shift_step=30)),
        (3, "hours", mk_implicit("hours", GE, lambda rng, ctx, D: ctx["len"],
                                 lambda rng, ctx, t: ("Volunteers may not go over their monthly hours cap; the shift counts as {v} hours.", None),
                                 "have enough hours left this month to cover it", vfmt=lambda t, st: str(t))),
        (2, "aid", mk_bool("aid")),
        (3, "check", mk_bool("check")),
        (2, "langs", mk_set("langs", modes=("has",), w=(1,))),
        (1, "drive", mk_bool("drive")),
        (1, "shifts", mk_cmp("shifts", GE, 0.1, 0.4, strict_p=0.0)),
    ],
    ties=[mk_tie("shifts", [(("a", "shifts"), "max")], "the most shifts already done", ["shifts"]),
          mk_tie("hours", [(("a", "hours"), "max")], "the most hours left this month", ["hours"])],
    ctx_fn=_vol_ctx, required=["day"], no_distract=["days", "check", "hours"],
    cs=lambda ctx, st: {"dayname": FULLDAY[ctx["day"]]},
    contexts=[("I coordinate volunteers at {org} and need one person to cover a shift on {dayname}.",
               "{name} coordinates volunteers at {org} and needs one person to cover a shift on {dayname}."),
              ("A {dayname} shift at {org} just opened up and I have to fill it.",
               "A {dayname} shift at {org} just opened up and {name} has to fill it.")],
    questions=["Which volunteer should {name} ask to cover the shift{ifany}?", "Which volunteer meets every requirement for the shift{ifany}?",
               "Which of the listed volunteers can take the shift under all of the rules{ifany}?"],
    intros=["Volunteer roster:", "People on the list:", "Volunteers who might be free:"],
    subjects=["Cover for the {dayname} shift", "Shift cover"],
    nice=["drive"],
)

# ================================================================================================ parking
PARK_LABELS = ["Elm Street Garage", "Central Station Car Park", "Market Square Parking", "Riverside Deck",
               "Northgate Car Park", "Harbour Parking", "Old Town Garage", "Civic Centre Car Park", "Westgate Parking",
               "Library Lane Garage", "Bridge Street Car Park", "Park & Walk East", "Cathedral Garage", "Quayside Car Park",
               "Victoria Road Parking", "Arena Car Park", "Canal Wharf Garage", "St. Mary's Car Park", "Hospital Road Garage",
               "Union Street Deck"]
PARK_ATTRS = [
    Attr("rate", "money", "Per hour", lo=100, hi=900, step=10, cents=True, pr="charges {v} an hour", missing_ok=False),
    Attr("cap", "money", "Daily maximum", lo=800, hi=4500, step=50, cents=True, pr="caps the day at {v}", missing_ok=False),
    Attr("height", "num", "Height limit", lo=180, hi=240, step=5, scale=100, unit=" m", pr="has a height limit of {v}",
         missing_ok=False),
    Attr("ev", "bool", "EV charging", p=0.45, vp=["have EV charging"], noun="EV charging", pr=("has EV charging", "has no EV charging")),
    Attr("late", "bool", "Open after midnight", p=0.5, vp=["stay open after midnight"],
         pr=("stays open after midnight", "closes at midnight")),
    Attr("walk", "num", "Walk to venue", lo=2, hi=25, unit=("minute", "minutes"), cls="count", vp=["be {c} {v} walk from the venue"],
         field=("Max walk", None), pr="is a {v} walk from the venue"),
    Attr("covered", "bool", "Covered", p=0.5, vp=["be covered"], pr=("is covered", "is open-air")),
]


def _park_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng), "hours": rng.randint(2, 11),
            "event": rng.choice(["a concert", "a hospital appointment", "a conference", "a football match", "a theatre show"])}


def _park_cost(ctx):
    return ("min", ("*", ("a", "rate"), ("k", ctx["hours"])), ("a", "cap"))


PARKING = Domain(
    "parking", "car park", "car parks", "Car park", PARK_LABELS, PARK_ATTRS,
    makers=[
        (4, "cost", mk_derived("cost", ["rate", "cap"], _park_cost, LE, lambda rng, ctx, D: 50 * rng.randint(10, 70),
                               ["cost {c} {v} for the whole stay", "come to {c} {v} for the stay"], money_fmt(cents=True),
                               ctx_fn=lambda ctx, st, ci: f"The stay is {ctx['hours']} hours; each car park charges its hourly rate but never more than its daily maximum.",
                               step=50, group="rate")),
        (3, "height", mk_implicit("height", GE, lambda rng, ctx, D: rng.randrange(190, 231, 5),
                                  lambda rng, ctx, t: ("The van is {v} tall.", None), "fit the van under its height limit",
                                  vfmt=lambda t, st: f"{t // 100}.{t % 100:02d} m")),
        (2, "ev", mk_bool("ev")),
        (2, "late", mk_bool("late")),
        (2, "walk", mk_cmp("walk", LE, 0.2, 0.6)),
        (1, "covered", mk_bool("covered")),
    ],
    ties=[mk_tie("cost", [(("min", ("*", ("a", "rate"), ("x", "hours")), ("a", "cap")), "min")],
                 "the lowest cost for the stay", ["rate", "cap"], tags=("multi_hop",)),
          mk_tie("walk", [(("a", "walk"), "min")], "the shortest walk", ["walk"])],
    ctx_fn=_park_ctx,
    contexts=[("I'm driving our van into town for {event} and need to park.", "{name} is driving a van into town for {event} and needs to park."),
              ("I need parking near {event} for the van.", "{name} needs parking near {event} for a van.")],
    questions=["Which car park should {name} use{ifany}?", "Which car park meets all of the requirements{ifany}?",
               "Which of the listed car parks satisfies every requirement{ifany}?"],
    intros=["Car parks nearby:", "Parking options:", "Garages within walking distance:"],
    subjects=["Parking for {event}", "Where to park"],
    nice=["covered"],
)

# ================================================================================================ grant programs
GRANT_LABELS = ["Community Spark Fund", "Riverside Arts Grant", "Northfield Heritage Fund", "Green Streets Grant",
                "Youth Futures Fund", "Neighbourhood Kitchen Fund", "Open Spaces Grant", "Digital Inclusion Fund",
                "Library Friends Grant", "Makers Micro-Grant", "Coastal Communities Fund", "Healthy Minds Grant",
                "Small Steps Fund", "Rural Links Grant", "Civic Pride Fund", "Bright Ideas Grant", "Warm Homes Fund",
                "Active Lives Grant", "Story Seeds Fund", "Common Ground Grant"]
ORGTYPES = ["registered charity", "community group", "social enterprise", "school", "individual artist"]
GRANT_ATTRS = [
    Attr("award", "money", "Maximum award", lo=100000, hi=10000000, step=50000, pr="awards up to {v}", missing_ok=False),
    Attr("deadline", "date", "Deadline", date_lo=2, date_hi=80, cls="date", pr="closes on {v}", missing_ok=False),
    Attr("who", "set", "Who can apply", items=ORGTYPES, kset=(1, 3), pr="is open to: {v}", missing_ok=False),
    Attr("match", "num", "Match funding required", lo=0, hi=50, step=5, unit="%", vp=["require match funding of {c} {v}"],
         field=("Max match funding", None), pr="requires {v} match funding"),
    Attr("decide", "num", "Decision time", lo=2, hi=20, unit=("week", "weeks"), cls="count", vp=["decide within {v}", "give a decision in {c} {v}"],
         pr="decides in {v}"),
    Attr("capital", "bool", "Funds equipment", p=0.5, vp=["fund equipment purchases"],
         pr=("funds equipment purchases", "does not fund equipment")),
    Attr("region", "cat", "Area covered", cats=["nationwide", "North region", "South region", "city only"],
         vp=["cover {v}"], pr="covers {v}", missing_ok=False),
]


def _grant_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng), "orgtype": rng.choice(ORGTYPES[:4]),
            "project": rng.choice(["a community garden", "an after-school coding club", "a repair café",
                                   "a mural project", "a lunch club for older residents", "a youth football league"])}


def _mk_orgtype(rng, ctx, D):
    from cst_core import SetCon
    c = SetCon("who", D.A["who"], "has", [ctx["orgtype"]], 1, vpi=0)
    c.pool = ORGTYPES
    c.fixed = True  # the applicant's organisation type is stated in the context
    return c


GRANT_ATTRS[2].vp = ["be open to a {v}", "accept applications from a {v}"]


def _mk_decide(rng, ctx, D):
    return CmpCon("decide", D.A["decide"], LE, rng.randint(4, 10), "pos", wi=rng.randrange(12), vpi=1)


GRANT = Domain(
    "grant_program", "funding program", "funding programs", "Program", GRANT_LABELS, GRANT_ATTRS,
    makers=[
        (4, "who", _mk_orgtype),
        (3, "award", mk_implicit("award", GE, lambda rng, ctx, D: 50000 * rng.randint(4, 150),
                                 lambda rng, ctx, t: ("The project needs {v}.", None),
                                 "be able to award the full amount the project needs", vfmt=money_fmt())),
        (3, "deadline", mk_derived("deadline", ["deadline"], lambda ctx: ("-", ("a", "deadline"), ("x", "today")), GE,
                                   lambda rng, ctx, D: rng.choice([10, 14, 21, 28]),
                                   ["have a deadline {c} {v} days from today"], lambda t, st: str(t),
                                   ctx_fn=lambda ctx, st, ci: f"Today is {fd(ctx['today'], st)}; the application needs time to prepare.",
                                   step=1, tags=("temporal", "multi_hop"), cls="count", wset=[0, 2], neg_p=0.0,
                                   vd=(1, 2, 3, 5, 7, -1, -2, -3, -5, -7))),
        (2, "match", mk_cmp("match", LE, 0.0, 0.4, strict_p=0.0, neg_p=0.3)),
        (2, "decide", _mk_decide),
        (1, "capital", mk_bool("capital")),
        (2, "region", mk_cat("region", (1, 2), only_pos=True)),
    ],
    ties=[mk_tie("award", [(("a", "award"), "max")], "the largest maximum award", ["award"]),
          mk_tie("decide", [(("a", "decide"), "min"), (("a", "award"), "max")],
                 "the fastest decision (then the larger award)", ["decide", "award"])],
    ctx_fn=_grant_ctx, required=["who"],
    cs=lambda ctx, st: {"article": "an" if ctx["orgtype"][0] in "aeiou" else "a"},
    contexts=[("We're {article} {orgtype} applying for money for {project}; we can only prepare one application.",
               "{name}'s organisation is {article} {orgtype} applying for money for {project} and can only prepare one application."),
              ("I'm writing one grant application for {project} on behalf of our {orgtype}.",
               "{name} is writing one grant application for {project} on behalf of {article} {orgtype}.")],
    questions=["Which funding program should {name} apply to{ifany}?", "Which program meets all of the requirements{ifany}?",
               "Which of the listed grants satisfies every requirement{ifany}?"],
    intros=["Open funding calls:", "Grants found:", "Programs on the funder list:"],
    subjects=["Grant for {project}", "Which grant to apply for"],
    nice=["capital"],
)

# ================================================================================================ used cars
COLORS = ["silver", "blue", "white", "black", "red", "grey", "green", "bronze"]
MODELS = ["Tarlo hatchback", "Arden sedan", "Kestra estate", "Morrow SUV", "Pellan hatchback", "Vesta coupe",
          "Corvan sedan", "Luma crossover"]
CAR2_LABELS = [f"{c.capitalize()} {m}" for c in COLORS for m in MODELS]
USED_ATTRS = [
    Attr("price", "money", "Price", lo=300000, hi=3500000, step=10000, vp=["cost {c} {v}"], field=("Max price", None),
         pr="costs {v}", missing_ok=False),
    Attr("miles", "num", "Mileage", lo=5000, hi=150000, step=500, unit=" miles", vp=["have {c} {v} on the clock"],
         field=("Max mileage", None), pr="has {v} on the clock", missing_ok=False),
    Attr("year", "num", "Year", lo=2008, hi=2025, pr="is from {v}", missing_ok=False),
    Attr("owners", "num", "Previous owners", lo=1, hi=5, unit=("owner", "owners"), cls="count", vp=["have had {c} {v}"],
         pr="has had {v}"),
    Attr("accident", "bool", "Accident history", p=0.3, vp=["have an accident history"],
         anti=["have a clean, accident-free history"], pr=("has an accident history", "has no accident history")),
    Attr("trans", "cat", "Gearbox", cats=["automatic", "manual"], vp=["be {v}"], pr="is {v}", missing_ok=False),
    Attr("fuel", "cat", "Fuel", cats=["petrol", "diesel", "hybrid", "electric"], vp=["run on {v}", "be {v}"], pr="runs on {v}",
         missing_ok=False),
    Attr("service", "bool", "Full service history", p=0.55, vp=["come with a full service history"], noun="a full service history",
         pr=("has a full service history", "has a partial service history")),
]


USED_ATTRS[2].nocomma = True


def _used_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng), "city": rng.choice(CITIES)}


def _mk_year2(rng, ctx, D):
    t = rng.randint(2012, 2020)
    wi = rng.randrange(12)

    def build(p):
        return ("cmp", ("a", "year"), GE, ("k", p["t"])), [("year", p["t"] + d) for d in (-1, 0, 1)]

    def text(p, st, mi):
        s = f"{modal('pos', mi)} {['be from', 'date from'][wi % 2]} {p['t']} or later"
        return {"inline": s, "bullet": cap(s) + ".", "field": f"Oldest acceptable year: {p['t']}"}

    def vary(p, rng2):
        return [{"t": p["t"] + d} for d in (-3, -2, -1, 1, 2, 3)]

    def chk(p, st):
        return [("orlater", str(p["t"]))]
    return FnCon("year", ["year"], {"t": t}, build, text, vary, chk, tags={"numeric", "temporal"}, group="year", mscale=1)


USED_CAR = Domain(
    "used_car", "car", "cars", "Listing", CAR2_LABELS, USED_ATTRS,
    makers=[
        (3, "price", mk_cmp("price", LE, 0.2, 0.7)),
        (2, "miles", mk_cmp("miles", LE, 0.2, 0.7)),
        (2, "miles", mk_xunit("miles", LE, "km", Fr(10, 16), Fr(1000000, 1609344), [x * 10000 for x in range(6, 22, 2)],
                              ["have {c} {v} on the clock"], "(1 mile = 1.6 km)", dec=0)),
        (2, "year", _mk_year2),
        (1, "owners", mk_cmp("owners", LE, strict_p=0.0, tlo=1, thi=3, tstep=1)),
        (3, "accident", mk_bool("accident", want=False)),
        (2, "trans", mk_cat("trans", (1, 1), neg_p=0.4)),
        (1, "fuel", mk_cat("fuel", (1, 2), neg_p=0.5)),
        (2, "service", mk_bool("service")),
    ],
    ties=[mk_tie("miles", [(("a", "miles"), "min")], "the lowest mileage", ["miles"]),
          mk_tie("price", [(("a", "price"), "min")], "the lowest price", ["price"]),
          mk_tie("year", [(("a", "year"), "max"), (("a", "price"), "min")], "the newest year (then the lower price)",
                 ["year", "price"])],
    ctx_fn=_used_ctx, no_distract=["accident"],
    contexts=[("I'm buying a used car in {city} and will test-drive only one.", "{name} is buying a used car in {city} and will test-drive only one."),
              ("I've saved some used-car listings in {city} and want to pick one to buy.", "{name} has saved some used-car listings in {city} and wants to pick one to buy.")],
    questions=["Which car should {name} go and see{ifany}?", "Which listing meets all of the requirements{ifany}?",
               "Which of the saved cars satisfies every stated requirement{ifany}?"],
    intros=["Saved listings:", "Cars for sale:", "Listings:"],
    subjects=["Used car shortlist", "Car listings"],
)

# ================================================================================================ software vendors
SAAS_LABELS = ["Tallyboard", "Clearnote", "Fieldkit", "Brightdesk", "Loopwise", "Taskharbor", "Notewell", "Planfold",
               "Queueline", "Ridgepoint", "Shiftly", "Trackwell", "Uplane", "Vaultly", "Workgrid", "Yardstick HQ",
               "Zenpost", "Arbor Tasks", "Beamline", "Crewbase"]
SAAS_ATTRS = [
    Attr("seat", "money", "Price per user per month", lo=300, hi=4500, step=50, cents=True, vp=["cost {c} {v} per user per month"],
         field=("Max price per user", None), pr="costs {v} per user per month", missing_ok=False),
    Attr("sso", "bool", "SSO", p=0.55, vp=["support single sign-on"], noun="single sign-on",
         pr=("supports single sign-on", "has no single sign-on")),
    Attr("res", "cat", "Data stored in", cats=["US", "EU", "UK", "Canada", "Australia"], vp=["store data in {v}"],
         pr="stores data in {v}", missing_ok=False),
    Attr("soc2", "bool", "SOC 2 report", p=0.55, vp=["have a SOC 2 report"], noun="a SOC 2 report",
         pr=("has a SOC 2 report", "has no SOC 2 report")),
    Attr("uptime", "num", "Uptime SLA", lo=9900, hi=9999, step=1, scale=100, unit="%",
         gen=lambda rng, ctx, o: rng.choice([9900, 9950, 9990, 9995, 9999]), vp=["guarantee uptime of {c} {v}"],
         field=(None, "Min uptime"), pr="guarantees {v} uptime"),
    Attr("maxu", "num", "User limit", lo=10, hi=1000, step=10, unit=("user", "users"), cls="count", pr="allows up to {v}",
         missing_ok=False),
    Attr("api", "bool", "API access", p=0.6, vp=["include API access"], noun="API access", pr=("includes API access", "has no API access")),
]


def _saas_ctx(rng):
    return {"today": base_day(rng), "name": pick_name(rng), "users": 5 * rng.randint(4, 60),
            "tool": rng.choice(["project-tracking tool", "shared notes app", "help-desk tool", "scheduling tool",
                                "field-service app"])}


SAAS = Domain(
    "saas_vendor", "software vendor", "software vendors", "Product", SAAS_LABELS, SAAS_ATTRS,
    makers=[
        (3, "year", mk_derived("year", ["seat"], lambda ctx: ("*", ("a", "seat"), ("k", 12 * ctx["users"])), LE,
                               lambda rng, ctx, D: 100000 * max(1, ctx["users"] * 12 * rng.randint(4, 40) // 1000),
                               ["cost {c} {v} a year for everyone", "come to {c} {v} per year for all users"], money_fmt(),
                               ctx_fn=lambda ctx, st, ci: f"We need {ctx['users']} user accounts, billed for 12 months a year.",
                               step=100000, tags=("numeric", "multi_hop", "units"), group="seat")),
        (2, "seat", mk_cmp("seat", LE, 0.2, 0.7)),
        (3, "sso", mk_bool("sso")),
        (3, "res", mk_cat("res", (1, 2), neg_p=0.25)),
        (2, "soc2", mk_bool("soc2")),
        (2, "uptime", mk_cmp("uptime", GE, strict_p=0.0, tlo=9950, thi=9995, tstep=45)),
        (3, "maxu", mk_implicit("maxu", GE, lambda rng, ctx, D: ctx["users"],
                                lambda rng, ctx, t: ("The team has {v} people who all need accounts.", None),
                                "allow enough users for the whole team", vfmt=lambda t, st: str(t))),
        (1, "api", mk_bool("api")),
    ],
    ties=[mk_tie("seat", [(("a", "seat"), "min")], "the lowest price per user", ["seat"]),
          mk_tie("uptime", [(("a", "uptime"), "max"), (("a", "seat"), "min")], "the highest uptime SLA (then the lower price)",
                 ["uptime", "seat"])],
    ctx_fn=_saas_ctx, no_distract=["maxu"],
    contexts=[("We're buying a {tool} and procurement wants exactly one vendor.", "{name}'s company is buying a {tool} and procurement wants exactly one vendor."),
              ("I'm picking a {tool} for the team.", "{name} is picking a {tool} for the team.")],
    questions=["Which vendor should {name} choose{ifany}?", "Which product meets all of the procurement requirements{ifany}?",
               "Which of the listed vendors satisfies every requirement{ifany}?"],
    intros=["Vendors evaluated:", "Products on the shortlist:", "Vendor comparison:"],
    subjects=["{tool} selection", "Vendor shortlist"],
    nice=["api"],
)

VOLUNTEER.person = True
DOMAINS_C = [LOAN, CLOUD, TRAIN, GYM, VOLUNTEER, PARKING, GRANT, USED_CAR, SAAS]
