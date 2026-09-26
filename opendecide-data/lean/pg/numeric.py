"""pg.numeric -- procedural generator for the "numeric" System-One decision family.

Every item hinges on exact arithmetic applied to stated rules: bands with corrections
(measurement uncertainty, as-weighed vs corrected mass), unit conversions (g/kg, mg/mL,
% w/v, ppm, bps, km/miles, in/lb, MB/GB, time zones), rounding rules (half-up, truncate,
round-up steps), caps and floors, tiered fees, pro-rata refunds, day-count conventions,
deductibles / sublimits / aggregates, per-night limits and per-diem rules.

Gold answers come from a small rule engine per scenario.  Each scenario also recomputes
the gold via an independent code path (Fraction ledger vs Decimal formula, day-by-day
loops, interval logic ...) and the generator asserts that both agree.  Each wrong option
is produced by re-running the engine with exactly one named mistake (forgot the
exception, superseded rule, off-by-one, unit mix-up, followed the unreviewed note ...).

Pure standard library, deterministic from the seed.
"""
import calendar
import datetime
import json
import math
import random
from decimal import Decimal as D, ROUND_HALF_UP, ROUND_DOWN, ROUND_CEILING, getcontext
from fractions import Fraction as F

getcontext().prec = 60

FAMILY = "numeric"
DT = datetime.date
DTM = datetime.datetime
TD = datetime.timedelta
C2 = D("0.01")


# ----------------------------------------------------------------------------- utils
def pick(rng, seq):
    return seq[rng.randrange(len(seq))]


def q2(x):
    return D(x).quantize(C2, rounding=ROUND_HALF_UP)


def qn(x, places=0, mode=ROUND_HALF_UP):
    return D(x).quantize(D(1).scaleb(-places), rounding=mode)


def fr_round(x, places=2, mode="half_up"):
    """Round a non-negative Fraction (independent of Decimal)."""
    s = F(10) ** places
    v = F(x) * s
    if mode == "half_up":
        n = math.floor(v + F(1, 2))
    elif mode == "down":
        n = math.floor(v)
    elif mode == "up":
        n = math.ceil(v)
    else:
        raise ValueError(mode)
    return F(n) / s


def dstr(x):
    """Plain decimal string without exponent / trailing zeros."""
    s = format(D(x).normalize(), "f")
    return s


CURS = [("$", "p"), ("USD ", "p"), ("€", "p"), ("EUR ", "p"), ("£", "p"), ("GBP ", "p"),
        (" CHF", "s"), ("CAD $", "p"), ("AUD ", "p"), (" USD", "s")]


def money(x, cur):
    s = "{:,.2f}".format(q2(x))
    return cur[0] + s if cur[1] == "p" else s + cur[0]


def fdate(d, st):
    if st == 0:
        return d.isoformat()
    if st == 1:
        return "%d %s %d" % (d.day, calendar.month_name[d.month], d.year)
    if st == 2:
        return "%s %d, %d" % (calendar.month_name[d.month], d.day, d.year)
    return "%d %s %d" % (d.day, calendar.month_abbr[d.month], d.year)


def fdt(t, st):
    if st == 0:
        return t.strftime("%Y-%m-%d %H:%M")
    if st == 1:
        return "%d %s %d, %s" % (t.day, calendar.month_name[t.month], t.year, t.strftime("%H:%M"))
    if st == 2:
        h = t.hour % 12 or 12
        return "%s %d, %d at %d:%02d %s" % (calendar.month_name[t.month], t.day, t.year, h, t.minute,
                                            "AM" if t.hour < 12 else "PM")
    return "%d %s %d %s" % (t.day, calendar.month_abbr[t.month], t.year, t.strftime("%H:%M"))


def rand_date(rng, y0=2024, y1=2026):
    a, b = DT(y0, 1, 1), DT(y1, 12, 31)
    return a + TD(days=rng.randint(0, (b - a).days))


def add_year(d):
    return d.replace(year=d.year + 1)


PEOPLE = ["A. Moreno", "J. Okafor", "P. Lindqvist", "R. Haddad", "S. Nakamura", "T. Brennan", "M. Kowalski",
          "L. Fontaine", "D. Mensah", "K. Iyer", "E. Petrov", "H. Castillo", "N. Abara", "C. Whitfield",
          "Y. Tanaka", "B. Oyelaran", "G. Rossi", "F. Dubois", "I. Novak", "O. Silva"]


# ------------------------------------------------------------------- rule versions
def plan_version(rng, key_date):
    new = rng.random() < 0.6
    if new:
        eff = key_date - TD(days=pick(rng, [0, 0, 1, 3, 9, 30, 75, 160]))
    else:
        eff = key_date + TD(days=pick(rng, [1, 1, 2, 4, 12, 30, 70]))
    return {"new": new, "eff": eff, "eff_old": eff - TD(days=rng.randint(330, 1100)),
            "rev": rng.randint(2, 11), "style": rng.randrange(4), "flip": rng.random() < 0.5}


def version_blocks(v, old_txt, new_txt, key_label, ds):
    fd = lambda d: fdate(d, ds)
    a, b, e, eo, st = v["rev"], v["rev"] + 1, v["eff"], v["eff_old"], v["style"]
    if st == 0:
        bl = ["Revision %d (effective %s): %s." % (a, fd(eo), old_txt),
              "Revision %d (effective %s): %s. Revision %d replaces Revision %d where the %s is on or after %s."
              % (b, fd(e), new_txt, b, a, key_label, fd(e))]
    elif st == 1:
        bl = ["Where the %s is on or before %s: %s." % (key_label, fd(e - TD(days=1)), old_txt),
              "Where the %s is on or after %s: %s." % (key_label, fd(e), new_txt)]
    elif st == 2:
        bl = ["Update circulated %s: from %s, %s. Until then, %s. The %s decides which figure applies."
              % (fd(e - TD(days=21)), fd(e), new_txt, old_txt, key_label)]
    else:
        bl = ["Schedule in force since %s: %s." % (fd(eo), old_txt),
              "Amendment taking effect %s (not retroactive; applied by %s): %s." % (fd(e), key_label, new_txt)]
    if len(bl) > 1 and v["flip"]:
        bl.reverse()
    return bl


# ---------------------------------------------------------------------------- notes
NOTE_WHO = ["a trainee analyst", "a summer intern", "a new hire still in onboarding",
            "a colleague from the sales team", "a contractor without approval rights",
            "the customer's own worksheet", "an unverified AI summary pasted into the ticket",
            "a reply on the community forum", "last year's quick-reference card",
            "a temp covering the front desk", "a junior associate (not an approver)"]


def note_text(rng, thing, v, reason):
    w = pick(rng, NOTE_WHO)
    r = (" - %s" % reason) if reason and rng.random() < 0.7 else ""
    t = pick(rng, [
        '%s left a comment: "I make the %s %s%s."' % (w[0].upper() + w[1:], thing, v, r),
        'Unreviewed draft by %s: %s = %s%s.' % (w, thing, v, r),
        'Note from %s: "Should be %s%s."' % (w, v, r),
        '%s suggested %s as the %s%s; nobody has checked this yet.' % (w[0].upper() + w[1:], v, thing, r),
        'Sticky note from %s: "%s%s. Done."' % (w, v, r),
    ])
    return t


def mk(**kw):
    base = dict(versions=[], rule_table=None, fact_table=None, card=None, kind="amount", reasons={}, ntr=0,
                bands=None, q_band=None, q_prop=None, q_thr=None)
    base.update(kw)
    return base


# =========================================================================== SCENARIOS
# --------------------------------------------------------------------- 1 insurance
INS_CATS = [("jewelry and watches", "a diamond pendant and a wristwatch"),
            ("portable electronics", "a laptop and a mirrorless camera"),
            ("bicycles", "an electric cargo bike"),
            ("fine art", "two signed lithographs"),
            ("musical instruments", "a vintage electric guitar"),
            ("sports equipment", "a set of golf clubs and a road-bike frame")]
VEH_PLACES = ["the insured's car, parked on a side street while the insured was at dinner",
              "the boot of the insured's car in a supermarket car park while the insured was shopping",
              "the insured's locked car, left overnight in a hotel car park"]
HOME_PLACES = ["the insured's flat during a break-in (front door forced)",
               "the insured's house while the family was away for the weekend",
               "a locked storage room in the insured's building"]


def ins_pay(L, S, ded, pct, order, R, waived, dac=False):
    d = D(0) if waived else ded
    p = D(pct) / 100
    if order == "loss":
        c = min(L, S)
        pay = c * p - d if dac else max(D(0), c - d) * p
    else:
        raw = L * p - d if dac else max(D(0), L - d) * p
        pay = min(raw, S)
    pay = max(D(0), pay)
    if R is not None:
        pay = min(pay, R)
    return q2(pay)


def ins_check(L, S, ded, pct, order, R, waived):
    L, S = F(L), F(S)
    d = F(0) if waived else F(ded)
    share = F(100 - pct, 100)
    if order == "loss":
        covered = L if L < S else S
        pay = F(0) if covered <= d else covered - (d + (covered - d) * share)
    else:
        raw = (L - d) * (1 - share) if L > d else F(0)
        pay = S if raw > S else raw
    if R is not None and pay > F(R):
        pay = F(R)
    return fr_round(pay)


def S_insurance(rng, mode, cur=None):
    big = mode != "short"
    cur = cur or pick(rng, CURS)
    M = lambda x: money(x, cur)
    ds = rng.randrange(4)
    cat, item = pick(rng, INS_CATS)
    S = D(pick(rng, [1000, 1500, 2000, 2500, 3000, 4000, 5000]))
    L = D(rng.randrange(int(S) * 7 // 10, int(S) * 12 // 5)) + D(pick(rng, [0, 0, 25, 40, 99])) / 100
    ded = D(pick(rng, [250, 500, 750, 1000]))
    pct = pick(rng, [70, 75, 80, 85, 90])
    order = pick(rng, ["loss", "pay"])
    loss = rand_date(rng)
    filed = loss + TD(days=rng.randint(1, 25))
    cid = "%s-%d" % (pick(rng, ["CL", "CLM", "HC", "PR"]), rng.randint(10000, 99999))
    ntr = 0
    rules, versions, alts, reasons = [], [], {}, {}
    use_ver = big and rng.random() < 0.5
    use_waiver = big and rng.random() < 0.45
    use_agg = rng.random() < (0.25 if big else 0.1)
    use_cue = big and rng.random() < 0.45
    Lcue = None
    if use_cue:
        Lcue = q2(L * D(rng.randint(115, 170)) / 100)
        rules.append(pick(rng, [
            "The loss amount is the documented replacement cost on the date of loss, not the price originally paid.",
            "Value each loss at its documented replacement cost; purchase receipts only prove ownership."]))
        ntr += 1
    ded_other = None
    if use_ver:
        v = plan_version(rng, loss)
        ded_other = D(pick(rng, [x for x in (250, 500, 750, 1000, 1500) if D(x) != ded]))
        old_d, new_d = (ded_other, ded) if v["new"] else (ded, ded_other)
        versions = version_blocks(v, "the per-claim deductible is %s" % M(old_d),
                                  "the per-claim deductible is %s" % M(new_d), "date of loss", ds)
        rules.append(pick(rng, [
            "A per-claim deductible (see the schedule revisions) is subtracted before coinsurance.",
            "Subtract the per-claim deductible from the schedule first, then apply coinsurance."]))
        ntr += 1
    else:
        rules.append(pick(rng, [
            "A %s deductible applies per claim and is subtracted before coinsurance." % M(ded),
            "Each claim carries a %s deductible; take it off first, then apply coinsurance." % M(ded),
            "Per-claim deductible: %s (applied before the coinsurance percentage)." % M(ded)]))
    rules.append(pick(rng, [
        "After the deductible, the insurer pays %d%% of the remaining covered loss." % pct,
        "Coinsurance: insurer %d%%, insured %d%% of the covered loss left after the deductible." % (pct, 100 - pct),
        "Reimbursement rate: %d%% of what remains once the deductible is subtracted." % pct]))
    if order == "loss":
        rules.append(pick(rng, [
            "Special limit for %s: the loss is capped at %s before the deductible and coinsurance are applied." % (cat, M(S)),
            "For %s, at most %s of loss is recognised; apply deductible and coinsurance to that capped figure." % (cat, M(S)),
            "Sublimit for %s: %s. It caps the loss, not the payment: cap first, then deductible, then coinsurance." % (cat, M(S))]))
    else:
        rules.append(pick(rng, [
            "Special limit for %s: the most payable on one claim is %s, applied after deductible and coinsurance." % (cat, M(S)),
            "For %s the payment, not the loss, is capped at %s: compute the payment first, then cap it." % (cat, M(S)),
            "Sublimit for %s: %s maximum payable per claim (applied to the final payment)." % (cat, M(S))]))
    waived = False
    wfacts = []
    vehicle = on_time = False
    if use_waiver:
        N = pick(rng, [24, 48, 72])
        off = pick(rng, [-rng.randint(45, 1300), 0, 0, rng.randint(1, 59), rng.randint(60, 2000)])
        delay = N * 60 + off
        vehicle = rng.random() < 0.35
        on_time = delay <= N * 60
        waived = on_time and not vehicle
        disc = DTM.combine(loss, datetime.time(rng.randint(6, 23), pick(rng, [0, 5, 10, 15, 20, 30, 40, 45, 50])))
        rep = disc + TD(minutes=delay)
        rules.append(pick(rng, [
            "The deductible is waived for theft claims if a police report is filed within %d hours of discovery "
            "(exactly %d hours still qualifies). The waiver does not apply to property stolen from an unattended vehicle." % (N, N),
            "No deductible waiver is available unless a police report was filed no later than %d hours after the theft "
            "was discovered, and it is never available for items taken from an unattended vehicle." % N,
            "Theft deductible waiver: police report filed at most %d hours after discovery. Exception: thefts from "
            "unattended vehicles do not qualify." % N]))
        tst = rng.randrange(4)
        wfacts = [("Theft discovered", fdt(disc, tst)), ("Police report filed", fdt(rep, tst)),
                  ("Items taken from", pick(rng, VEH_PLACES) if vehicle else pick(rng, HOME_PLACES))]
        ntr += 1 + (1 if 0 <= off < 60 else 0) + (1 if vehicle and on_time else 0)
    R = None
    pre = ins_pay(L, S, ded, pct, order, None, waived)
    if use_agg and pre > 200:
        R = D(int(pre * D(rng.randint(45, 90)) / 100))
        rules.append(pick(rng, [
            "Only %s remains under this policy year's aggregate limit; no payment may exceed it." % M(R),
            "Remaining annual aggregate on this policy: %s. Payments cannot exceed what remains." % M(R)]))
        ntr += 1
    P = dict(L=L, S=S, ded=ded, pct=pct, order=order, R=R, waived=waived)

    def pay(**kw):
        q = dict(P)
        q.update(kw)
        return ins_pay(**q)

    gold = pay()
    check = ins_check(L, S, ded, pct, order, R, waived)
    if use_ver:
        alts["wrong_rule_version"] = pay(ded=ded_other)
        reasons["wrong_rule_version"] = "used the deductible from the schedule I had bookmarked"
    if use_waiver:
        if waived:
            alts["missed_deductible_waiver"] = pay(waived=False)
            reasons["missed_deductible_waiver"] = "deductible always applies"
        elif vehicle and on_time:
            alts["ignored_vehicle_exception"] = pay(waived=True)
            reasons["ignored_vehicle_exception"] = "police report was on time, so no deductible"
        else:
            alts["late_report_treated_as_on_time"] = pay(waived=True)
            reasons["late_report_treated_as_on_time"] = "report was filed in time, deductible waived"
    alts["sublimit_order_swapped"] = pay(order="pay" if order == "loss" else "loss")
    alts["forgot_sublimit"] = pay(S=D(10) ** 9)
    reasons["forgot_sublimit"] = "the whole documented loss is covered"
    if R is not None:
        alts["ignored_aggregate_limit"] = pay(R=None)
    if use_cue:
        alts["used_purchase_price"] = pay(L=Lcue)
        reasons["used_purchase_price"] = "based on the receipts"
    alts["deductible_after_coinsurance"] = pay(dac=True)
    alts["forgot_coinsurance"] = pay(pct=100)
    alts["paid_insured_share"] = pay(pct=100 - pct)
    facts = [("Claim", cid), ("Date of loss", fdate(loss, ds)), ("Claim received", fdate(filed, ds)),
             ("Items claimed", "%s (%s)" % (item, cat)), ("Documented replacement cost", M(L))]
    if use_cue:
        facts.append(("Original purchase price (receipts)", M(Lcue)))
    facts += wfacts
    return mk(cur=cur, domain="insurance", scen="insurance", cid=cid, M=M, fmt=M,
              title=pick(rng, ["Home Contents Policy - Theft and Specified Items", "Personal Property Cover: Settlement Rules",
                               "Claims Handling Guide - Contents Section", "Household Policy Wording (extract)"]),
              rules=rules, versions=versions, facts=facts, gold=gold, check=check, alts=alts, reasons=reasons,
              ntr=ntr, thing="settlement amount",
              q_choice=pick(rng, ["How much should the insurer pay on claim %s?" % cid,
                                  "What is the correct settlement amount for claim %s?" % cid,
                                  "Under the policy terms above, what amount is payable on claim %s?" % cid,
                                  "Which figure is the correct payment for claim %s?" % cid]),
              q_prop=lambda v: pick(rng, ["The draft settlement for claim %s is %s. Is that the correct payable amount?" % (cid, v),
                                          "Is %s the correct amount payable on claim %s?" % (v, cid),
                                          "Should claim %s be settled at exactly %s?" % (cid, v)]),
              q_thr=lambda c, t: pick(rng, ["Is the amount payable on claim %s %s %s?" % (cid, c, t),
                                            "Under the policy, will the payment on claim %s be %s %s?" % (cid, c, t)]))


# ------------------------------------------------------------------------ 2 travel
TRAVEL_US = [("Chicago", 229), ("Denver", 199), ("Boston", 289), ("Austin", 184), ("Seattle", 254),
             ("San Diego", 215), ("Atlanta", 177), ("Minneapolis", 169)]
TRAVEL_FX = [("Munich", 240, "EUR", "€"), ("Lyon", 205, "EUR", "€"), ("Edinburgh", 236, "GBP", "£"),
             ("Zurich", 318, "CHF", "CHF "), ("Dublin", 262, "EUR", "€")]
FX_RANGE = {"EUR": (10500, 11200), "GBP": (12200, 13200), "CHF": (10800, 11600)}


def travel_total(rate, cap, lodg_n, days, pd, partial, lunches, lunch_amt, miles, mrate):
    lodging = (min(rate, cap) if cap is not None else rate) * lodg_n
    meals = pd * (days - 2) + 2 * q2(pd * partial) - lunches * lunch_amt
    mileage = q2(D(miles) * mrate) if miles else D(0)
    return q2(lodging + meals + mileage)


def travel_check(d0, d1, rate, cap, pd, lunch_days, lunch_amt, km, mrate):
    tot = F(0)
    d = d0
    while d <= d1:
        if d < d1:
            tot += min(F(rate), F(cap))
        tot += F(pd) if d not in (d0, d1) else fr_round(F(pd) * F(3, 4))
        if d in lunch_days:
            tot -= F(lunch_amt)
        d += TD(days=1)
    if km:
        miles = fr_round(F(km) / F("1.609344"), 0)
        tot += fr_round(miles * F(mrate))
    return fr_round(tot)


def S_travel(rng, mode, cur=None):
    big = mode != "short"
    home = cur or pick(rng, [("$", "p"), ("USD ", "p"), (" USD", "s")])
    cur = home
    M = lambda x: money(x, home)
    ds = rng.randrange(4)
    foreign = big and rng.random() < 0.4
    if foreign:
        city, cap, fcode, fsym = pick(rng, TRAVEL_FX)
    else:
        city, cap = pick(rng, TRAVEL_US)
    cap = D(cap)
    nights = rng.randint(1, 5 if big else 3)
    d0 = rand_date(rng)
    d1 = d0 + TD(days=nights)
    days = nights + 1
    pd = D(pick(rng, [56, 59, 64, 68, 69, 74, 79, 80]))
    tid = "TR-%d" % rng.randint(10000, 99999)
    ntr = 1
    rules, versions, alts, reasons, facts = [], [], {}, {}, []
    rf = fx = fee = None
    if foreign:
        lo, hi = FX_RANGE[fcode]
        fx = D(rng.randint(lo, hi)) / 10000
        fee = D(pick(rng, ["0", "1", "2.5", "3"]))
        target = cap * D(rng.randint(80, 125)) / 100
        rf = q2(target / fx / (1 + fee / 100))
        rate = q2(rf * fx * (1 + fee / 100))
        ntr += 1
    else:
        rate = D(rng.randint(int(cap) * 78 // 100, int(cap) * 130 // 100)) + D(pick(rng, [0, 0, 99, 49])) / 100
    use_mile = big and rng.random() < 0.5
    mrate = D(pick(rng, ["0.67", "0.70", "0.655", "0.625", "0.725"]))
    km = miles = 0
    if use_mile:
        km = rng.randint(14, 160)
        miles = int(qn(D(km) / D("1.609344"), 0))
        ntr += 1
    lunch_days, lunch_amt = [], D(0)
    if big and days >= 3 and rng.random() < 0.35:
        full_days = [d0 + TD(days=i) for i in range(1, days - 1)]
        lunch_days = sorted(rng.sample(full_days, rng.randint(1, len(full_days))))
        lunch_amt = D(pick(rng, [12, 15, 16, 18]))
        ntr += 1
    ver_kind = None
    if big and rng.random() < 0.45:
        ver_kind = "mile" if use_mile else "pd"
        v = plan_version(rng, d0)
        if ver_kind == "mile":
            other = D(pick(rng, [x for x in ["0.625", "0.655", "0.67", "0.70", "0.725"] if D(x) != mrate]))
            o, n = (other, mrate) if v["new"] else (mrate, other)
            versions = version_blocks(v, "the mileage rate is %s per mile" % ("$" + dstr(o)),
                                      "the mileage rate is %s per mile" % ("$" + dstr(n)), "trip start date", ds)
        else:
            other = pd + pick(rng, [D(-5), D(-4), D(4), D(5), D(6)])
            o, n = (other, pd) if v["new"] else (pd, other)
            versions = version_blocks(v, "the M&IE per diem for %s is %s" % (city, M(o)),
                                      "the M&IE per diem for %s is %s" % (city, M(n)), "trip start date", ds)
        ntr += 1
    # ---- rules
    rules.append(pick(rng, [
        "Lodging: actual nightly cost up to %s per night in %s." % (M(cap), city),
        "Hotel costs are reimbursed at the lesser of the nightly rate paid and the %s ceiling of %s per night." % (city, M(cap)),
        "Nightly lodging may not exceed %s in %s; the traveller pays any excess." % (M(cap), city)]))
    if foreign:
        if fee > 0:
            rules.append("Foreign-currency hotel bills are converted at the card-statement rate. The card's %s%% foreign "
                         "transaction fee is reimbursable and is added to each night's converted cost (rounded to the cent) "
                         "before the nightly ceiling is applied." % dstr(fee))
        else:
            rules.append("Foreign-currency hotel bills are converted at the card-statement rate (the corporate card charges "
                         "no foreign transaction fee); round each night's converted cost to the cent, then apply the ceiling.")
    pd_txt = "the per diem shown in the rule history" if ver_kind == "pd" else M(pd)
    rules.append(pick(rng, [
        "Meals and incidentals: %s per calendar day of travel; the departure day and the return day are paid at 75%%." % pd_txt,
        "M&IE per diem is %s. First and last travel days get three-quarters of the daily rate (rounded to the cent)." % pd_txt,
        "Travel days are not paid at the full rate: departure and return days receive 75%% of the per diem (%s); "
        "all other days receive 100%%." % pd_txt]))
    if lunch_days:
        rules.append("When a lunch is provided (e.g., by a conference), deduct %s for each provided lunch." % M(lunch_amt))
    if use_mile:
        mr_txt = "the mileage rate in effect on the trip start date (see revisions)" if ver_kind == "mile" else "%s per mile" % ("$" + dstr(mrate))
        rules.append("Personal car use is paid at %s. Convert logged kilometres to miles (1 mile = 1.609344 km) and round "
                     "to the nearest whole mile before applying the rate; round the mileage amount to the cent." % mr_txt)
    # ---- engine
    base = dict(rate=rate, cap=cap, lodg_n=nights, days=days, pd=pd, partial=D("0.75"), lunches=len(lunch_days),
                lunch_amt=lunch_amt, miles=miles, mrate=mrate)

    def tot(**kw):
        q = dict(base)
        q.update(kw)
        return travel_total(**q)

    gold = tot()
    check = travel_check(d0, d1, rate, cap, pd, set(lunch_days), lunch_amt, km, mrate)
    alts["counted_days_not_nights"] = tot(lodg_n=days)
    reasons["counted_days_not_nights"] = "one hotel night per day of the trip"
    if rate > cap:
        alts["ignored_lodging_cap"] = tot(cap=None)
        reasons["ignored_lodging_cap"] = "the hotel receipt is valid, so we pay it"
    alts["full_per_diem_on_travel_days"] = tot(partial=D(1))
    if lunch_days:
        alts["forgot_meal_deduction"] = tot(lunches=0)
    if use_mile:
        alts["km_as_miles"] = tot(miles=km)
        reasons["km_as_miles"] = "mileage straight from the log"
    if ver_kind == "mile":
        alts["wrong_rule_version"] = tot(mrate=other)
    elif ver_kind == "pd":
        alts["wrong_rule_version"] = tot(pd=other)
    if foreign:
        if fee > 0:
            alts["fx_fee_not_added"] = tot(rate=q2(rf * fx))
        alts["cap_applied_in_foreign_currency"] = tot(rate=q2(min(rf, cap) * fx * (1 + fee / 100)), cap=None)
    alts["no_per_diem_on_travel_days"] = tot(partial=D(0))
    # ---- facts
    facts.append(("Trip", tid))
    facts.append(("Traveller", pick(rng, PEOPLE)))
    if big and rng.random() < 0.5:
        facts.append(("Purpose", "%d-day %s" % (days, pick(rng, ["client workshop", "sales conference", "site audit", "training course"]))))
        ntr += 1
    facts.append(("Destination", city))
    facts.append(("Departed", "%s (%s)" % (fdate(d0, ds), pick(rng, ["07:10 flight", "early train", "morning flight"]))))
    facts.append(("Returned", "%s (%s)" % (fdate(d1, ds), pick(rng, ["evening flight", "late train", "afternoon flight"]))))
    if foreign:
        facts.append(("Hotel invoice", "%d night(s) at %s%s per night" % (nights, fsym, "{:,.2f}".format(rf))))
        facts.append(("Card statement rate", "1 %s = %s USD" % (fcode, dstr(fx))))
    else:
        facts.append(("Hotel invoice", "%d night(s) at %s per night" % (nights, M(rate))))
    if lunch_days:
        facts.append(("Meals provided", "conference lunch on " + ", ".join(fdate(x, ds) for x in lunch_days)))
    if use_mile:
        facts.append(("Mileage log", "%d km (home to airport and back)" % km))
    return mk(cur=cur, domain="travel/expenses", scen="travel", cid=tid, M=M, fmt=M,
              title=pick(rng, ["Business Travel Policy - Reimbursement Rules", "Travel & Expense Handbook (excerpt)",
                               "T&E Policy v7 - Lodging, Meals, Mileage", "Employee Travel Reimbursement Guide"]),
              rules=rules, versions=versions, facts=facts, gold=gold, check=check, alts=alts, reasons=reasons,
              ntr=ntr, thing="reimbursable total",
              q_choice=pick(rng, ["What is the total reimbursable amount for trip %s?" % tid,
                                  "How much should be reimbursed for trip %s under the policy?" % tid,
                                  "Which total is correct for the expense claim on trip %s?" % tid]),
              q_prop=lambda v: pick(rng, ["The expense system shows %s for trip %s. Is that the correct reimbursable total?" % (v, tid),
                                          "Is %s the correct reimbursement for trip %s?" % (v, tid)]),
              q_thr=lambda c, t: pick(rng, ["Is the reimbursable total for trip %s %s %s?" % (tid, c, t),
                                            "Will the traveller on trip %s be reimbursed %s %s in total?" % (tid, c, t)]))


# -------------------------------------------------------------------- 3 SaaS refund
def saas_calc(P, used, term, rmode, fee_kind, fee_val, fee_min, fee_max, cool,
              fee_on_full=False, no_fee=False, clamp=True):
    if cool:
        return q2(P)
    raw = P * (term - used) / term
    ref = raw.quantize(C2, rounding=ROUND_DOWN if rmode == "down" else ROUND_HALF_UP)
    if no_fee:
        fee = D(0)
    elif fee_kind == "pct":
        fee = q2((P if fee_on_full else ref) * fee_val / 100)
        if clamp:
            fee = min(max(fee, fee_min), fee_max)
    else:
        fee = fee_val
    return q2(max(D(0), ref - fee))


def saas_check(P, s, c, e_excl, rmode, fee_kind, fee_val, fee_min, fee_max, cool):
    if cool:
        return F(P)
    term = 0
    d = s
    while d < e_excl:
        term += 1
        d += TD(days=1)
    used = sum(1 for i in range(term) if s + TD(days=i) <= c)
    raw = F(P) - F(P) * used / term
    ref = fr_round(raw, 2, "down" if rmode == "down" else "half_up")
    if fee_kind == "pct":
        fee = fr_round(ref * F(fee_val) / 100)
        fee = F(fee_min) if fee < F(fee_min) else (F(fee_max) if fee > F(fee_max) else fee)
    else:
        fee = F(fee_val)
    return ref - fee if ref > fee else F(0)


def S_saas(rng, mode, cur=None):
    big = mode != "short"
    cur = cur or pick(rng, CURS)
    M = lambda x: money(x, cur)
    ds = rng.randrange(4)
    P = D(pick(rng, [588, 708, 948, 1188, 1428, 1908, 2388, 2990, 4788, 5999, 8400]))
    while True:
        s = DT(2023, 1, 10) + TD(days=rng.randint(0, 1175))
        if not (s.month == 2 and s.day == 29):
            break
    e = add_year(s)
    term = (e - s).days
    cid = "ACC-%d" % rng.randint(100000, 999999)
    ntr = 1 + (1 if term == 366 else 0)
    cool_feat = big and rng.random() < 0.4
    N = pick(rng, [14, 30])
    renewal = rng.random() < 0.5
    if cool_feat and rng.random() < 0.7:
        c = s + TD(days=rng.randint(N - 3, N + 1) - 1)
    else:
        c = s + TD(days=rng.randint(20, term - 10))
    used = (c - s).days + 1
    cool = cool_feat and used <= N and not renewal
    rmode = pick(rng, ["down", "half_up"])
    if rng.random() < 0.6:
        fee_kind, fee_val = "pct", D(pick(rng, [10, 15, 20, 25]))
        fee_min, fee_max = D(pick(rng, [25, 50, 75])), D(pick(rng, [150, 250, 400, 600]))
    else:
        fee_kind, fee_val, fee_min, fee_max = "flat", D(pick(rng, [49, 75, 99, 150])), None, None
    versions, fee_other = [], None
    if big and rng.random() < 0.4:
        v = plan_version(rng, c)
        if fee_kind == "pct":
            fee_other = D(pick(rng, [x for x in (10, 15, 20, 25) if D(x) != fee_val]))
            ftxt = lambda x: "the early-termination fee is %s%% of the prorated refund" % dstr(x)
        else:
            fee_other = D(pick(rng, [x for x in (49, 75, 99, 150) if D(x) != fee_val]))
            ftxt = lambda x: "the flat early-termination fee is %s" % M(x)
        o, n = (fee_other, fee_val) if v["new"] else (fee_val, fee_other)
        versions = version_blocks(v, ftxt(o), ftxt(n), "cancellation date", ds)
        ntr += 1
    base = dict(P=P, used=used, term=term, rmode=rmode, fee_kind=fee_kind, fee_val=fee_val, fee_min=fee_min,
                fee_max=fee_max, cool=cool)

    def calc(**kw):
        q = dict(base)
        q.update(kw)
        return saas_calc(**q)

    gold = calc()
    check = saas_check(P, s, c, e, rmode, fee_kind, fee_val, fee_min, fee_max, cool)
    alts, reasons = {}, {}
    if cool:
        alts["missed_cooling_off"] = calc(cool=False)
        alts["missed_cooling_off_and_fee"] = calc(cool=False, no_fee=True)
        if fee_kind == "pct":
            f_full = min(max(q2(P * fee_val / 100), fee_min), fee_max)
        else:
            f_full = fee_val
        alts["fee_charged_in_cooling_off"] = q2(P - f_full)
    elif cool_feat and used <= N and renewal:
        alts["cooling_off_applied_to_renewal"] = q2(P)
        reasons["cooling_off_applied_to_renewal"] = "cancelled inside the cooling-off window, full refund"
        ntr += 1
    elif cool_feat and used == N + 1:
        alts["cooling_off_off_by_one"] = q2(P)
        ntr += 1
    alts["cancellation_day_not_billed"] = calc(used=used - 1)
    if term == 366:
        alts["assumed_365_day_term"] = calc(term=365)
        reasons["assumed_365_day_term"] = "annual price / 365 per day"
    else:
        alts["used_360_day_year"] = calc(term=360)
    alts["forgot_termination_fee"] = calc(no_fee=True)
    if fee_other is not None:
        alts["wrong_rule_version"] = calc(fee_val=fee_other)
    if fee_kind == "pct":
        alts["fee_on_full_price"] = calc(fee_on_full=True)
        alts["fee_min_max_ignored"] = calc(clamp=False)
    alts["wrong_rounding_mode"] = calc(rmode="half_up" if rmode == "down" else "down")
    # whole-month variant
    months_used = 0
    while True:
        m_end = s.replace(year=s.year + (s.month - 1 + months_used + 1) // 12,
                          month=(s.month - 1 + months_used + 1) % 12 + 1, day=min(s.day, 28))
        months_used += 1
        if m_end > c or months_used >= 12:
            break
    if not cool:
        ref_m = q2(P / 12 * (12 - months_used))
        if fee_kind == "pct":
            fee_m = min(max(q2(ref_m * fee_val / 100), fee_min), fee_max)
        else:
            fee_m = fee_val
        alts["whole_months_only"] = max(D(0), ref_m - fee_m)
    rules = []
    rules.append(pick(rng, [
        "Annual plans are prepaid. On cancellation, the unused part of the term is refunded pro rata by day.",
        "If an annual subscription is cancelled mid-term, the customer is refunded for the unused days of the term.",
        "Mid-term cancellations of prepaid annual plans are refunded on a daily pro-rata basis."]))
    rules.append(pick(rng, [
        "The cancellation day itself is billable: days up to and including the cancellation date count as used.",
        "Service runs until the end of the cancellation day, so that day counts as a used day.",
        "A cancellation date is not an unused day; count it as used."]))
    rules.append(pick(rng, [
        "Daily rate = annual price / actual number of days in the 12-month term (365 or 366).",
        "Use the actual length of the term in days (from the start date up to the day before the anniversary).",
        "The term length is the real number of calendar days in the subscription year, not a 360-day convention."]))
    rules.append("Round the prorated refund %s." % ("down to the cent (truncate)" if rmode == "down"
                                                     else "to the nearest cent (half up)"))
    if fee_kind == "pct" and fee_other is not None:
        rules.append("An early-termination fee (percentage as per the rule history, based on the prorated refund) is "
                     "deducted, subject to a minimum of %s and a maximum of %s." % (M(fee_min), M(fee_max)))
    elif fee_other is not None:
        rules.append("A flat early-termination fee (amount as per the rule history) is deducted from the prorated refund "
                     "(the refund cannot go below zero).")
    elif fee_kind == "pct":
        rules.append(pick(rng, [
            "An early-termination fee of %s%% of the prorated refund is deducted, subject to a minimum of %s and a "
            "maximum of %s." % (dstr(fee_val), M(fee_min), M(fee_max)),
            "Early termination fee: %s%% of the prorated refund (never less than %s, never more than %s), deducted "
            "from the refund." % (dstr(fee_val), M(fee_min), M(fee_max))]))
    else:
        rules.append("A flat early-termination fee of %s is deducted from the prorated refund (the refund cannot go "
                     "below zero)." % M(fee_val))
    if cool_feat:
        rules.append(pick(rng, [
            "Cooling-off: if the cancellation date falls within the first %d days of the term (the start date is day 1), "
            "the full price is refunded and no fee applies. Renewal terms have no cooling-off period." % N,
            "A full refund without any fee is given when a first-term customer cancels no later than day %d of the term "
            "(start date = day 1). This does not apply to renewals." % N]))
    if not big:
        fee_t = ("Early-termination fee: %s%% of the prorated refund (min %s, max %s)." % (dstr(fee_val), M(fee_min), M(fee_max))
                 if fee_kind == "pct" else "Flat early-termination fee: %s (refund not below zero)." % M(fee_val))
        rules = [pick(rng, ["Unused days of a prepaid annual plan are refunded pro rata; daily rate = price / actual days in the term (365 or 366).",
                            "Mid-term cancellation: refund the unused days pro rata, using the real number of days in the term."]),
                 pick(rng, ["The cancellation day counts as used.", "Days up to and including the cancellation date are used."]),
                 "Round the refund %s." % ("down to the cent" if rmode == "down" else "half up to the cent"), fee_t]
    facts = [("Account", cid), ("Plan", "Annual, prepaid %s" % M(P)), ("Term start", fdate(s, ds)),
             ("Term end", fdate(e - TD(days=1), ds)), ("Cancellation date", fdate(c, ds))]
    if cool_feat:
        facts.append(("Term type", "renewal (year %d)" % rng.randint(2, 5) if renewal else "first term"))
    if big and rng.random() < 0.4:
        facts.append(("Customer comment", '"We barely used it after the first %s months."' % rng.randint(2, 5)))
    return mk(cur=cur, domain="SaaS subscriptions", scen="saas", cid=cid, M=M, fmt=M, versions=versions,
              title=pick(rng, ["Subscription Terms - Cancellation and Refunds", "Billing Policy: Annual Plans",
                               "Customer Agreement, Schedule B (Refunds)", "Refund Desk Playbook"]),
              rules=rules, facts=facts, gold=gold, check=check, alts=alts, reasons=reasons, ntr=ntr,
              thing="refund",
              q_choice=pick(rng, ["What refund is due on account %s?" % cid,
                                  "How much should be refunded to account %s?" % cid,
                                  "Which refund amount is correct for the cancellation on account %s?" % cid]),
              q_prop=lambda v: pick(rng, ["Billing proposes refunding %s to account %s. Is that correct?" % (v, cid),
                                          "Is %s the correct refund for account %s?" % (v, cid)]),
              q_thr=lambda c_, t: pick(rng, ["Is the refund owed to account %s %s %s?" % (cid, c_, t),
                                             "Will account %s receive a refund %s %s?" % (cid, c_, t)]))


# ------------------------------------------------------------------------ 4 SLA
SLA_TIERS = [[("99.9", 10), ("99.5", 25), ("99.0", 50)],
             [("99.95", 5), ("99.9", 10), ("99.5", 25)],
             [("99.9", 10), ("99.0", 25), ("95.0", 100)],
             [("99.5", 10), ("99.0", 20), ("98.0", 30)]]


def sla_eval(incs, total, thr, incl, rnd, req, cnt_maint=False, excl_late=False, cnt_cust=False,
             cnt_degr=False, unit_mis=False):
    dt = F(0)
    for x in incs:
        m = F(x["mis"]) if (unit_mis and "mis" in x) else F(x["min"])
        k = x["kind"]
        if k == "out":
            dt += m
        elif k == "maint":
            if x["notice"] >= req:
                if cnt_maint:
                    dt += m
            elif not excl_late:
                dt += m
        elif k == "cust" and cnt_cust:
            dt += m
        elif k == "degr" and cnt_degr:
            dt += m
    up = (F(total) - dt) / total * 100
    if rnd == "round2":
        up = fr_round(up, 2)
    elif rnd == "trunc2":
        up = fr_round(up, 2, "down")
    tier = 0
    for i, t in enumerate(thr):
        if (up <= t) if incl else (up < t):
            tier = i + 1
    return tier


def sla_check(incs, total, thr_strs, incl, rnd, req):
    counted = sum(x["min"] for x in incs if x["kind"] == "out" or (x["kind"] == "maint" and x["notice"] < req))
    up = (D(total) - D(counted)) * D(100) / D(total)
    if rnd == "round2":
        up = up.quantize(C2, rounding=ROUND_HALF_UP)
    elif rnd == "trunc2":
        up = up.quantize(C2, rounding=ROUND_DOWN)
    for i in range(len(thr_strs) - 1, -1, -1):
        t = D(thr_strs[i])
        if (up <= t) if incl else (up < t):
            return i + 1
    return 0


def split_int(rng, total, k):
    if total <= 0:
        return []
    k = max(1, min(k, total))
    cuts = sorted(rng.sample(range(1, total), k - 1)) if k > 1 else []
    pts = [0] + cuts + [total]
    return [pts[i + 1] - pts[i] for i in range(k)]


def S_sla(rng, mode, cur=None):
    big = mode != "short"
    cur = cur or pick(rng, CURS)
    M = lambda x: money(x, cur)
    y, mo = pick(rng, [2024, 2025, 2026]), rng.randint(1, 12)
    nd = calendar.monthrange(y, mo)[1]
    total = nd * 1440
    tiers = pick(rng, SLA_TIERS)
    thr_s = [a for a, _ in tiers]
    thr = [F(a) for a in thr_s]
    pcts = [b for _, b in tiers]
    incl = rng.random() < 0.4
    rnd = pick(rng, ["none", "none", "round2", "trunc2"])
    req = pick(rng, [48, 72, 120])
    svc = pick(rng, ["Managed Postgres", "Object Storage", "SIP Trunk", "SD-WAN Link", "Hosted Contact Center",
                     "API Gateway", "Managed Kubernetes", "Business Fibre 1G"])
    cid = "SVC-%d" % rng.randint(1000, 9999)
    fee = D(rng.randrange(400, 12000, 10))
    as_amount = rng.random() < 0.3
    allowed = [F(total) * (100 - t) / 100 for t in thr]
    target = rng.randrange(4)
    lo = F(0) if target == 0 else allowed[target - 1]
    hi = allowed[target] if target < 3 else allowed[2] + max(F(60), allowed[2] / 2)
    if rng.random() < 0.35:
        edge = pick(rng, [lo, hi]) if target > 0 else hi
        dt = int(math.floor(edge)) + pick(rng, [-1, 0, 0, 1])
    else:
        a = int(math.ceil(lo))
        dt = rng.randint(a, max(a, int(math.floor(hi))))
    dt = max(dt, 0)
    ntr = 1
    incs = []
    rem = dt
    if big and dt >= 25 and rng.random() < 0.45:
        lm = rng.randint(10, min(dt - 5, 180))
        incs.append({"kind": "maint", "min": lm, "notice": req - rng.randint(1, req - 6)})
        rem = dt - lm
        ntr += 1
    for p in split_int(rng, rem, max(rng.randint(1, 3 if big else 2), -(-rem // 1380))):
        incs.append({"kind": "out", "min": p})
    for _ in range(rng.randint(0, 2 if big else 1)):
        incs.append({"kind": "maint", "min": rng.randint(20, 240), "notice": req + pick(rng, [0, rng.randint(1, 96)])})
        ntr += 1
    if rng.random() < (0.35 if big else 0.2):
        incs.append({"kind": "cust", "min": rng.randint(15, 200)})
        ntr += 1
    if big and rng.random() < 0.3:
        incs.append({"kind": "degr", "min": rng.randint(30, 300)})
        ntr += 1
    layout = pick(rng, ["startend", "duration"]) if big else "duration"
    mis_done = False
    days_avail = sorted(rng.sample(range(1, nd - 1, 2), len(incs)))
    rng.shuffle(incs)
    rows = []
    for i, x in enumerate(incs):
        x["day"] = days_avail[i]
        x["start"] = DTM(y, mo, x["day"], rng.randint(0, 23), pick(rng, [0, 5, 10, 12, 20, 25, 30, 41, 45, 50, 55]))
    incs.sort(key=lambda z: z["start"])
    for i, x in enumerate(incs):
        m = x["min"]
        st = x["start"]
        cat = {"out": pick(rng, ["Unplanned outage - database failover", "Unplanned outage - network partition",
                                 "Full service outage", "Outage - expired TLS certificate",
                                 "Unplanned outage - storage controller fault"]),
               "maint": "Scheduled maintenance",
               "cust": pick(rng, ["Customer-caused: firewall rule pushed by customer", "Customer-side power failure",
                                  "Customer DNS misconfiguration"]),
               "degr": "Degraded performance (elevated latency; service available)"}[x["kind"]]
        notice = ("announced %d h in advance" % x["notice"]) if x["kind"] == "maint" else "-"
        if layout == "startend":
            en = st + TD(minutes=m)
            nxt = " (+1 day)" if en.date() != st.date() else ""
            rows.append(["I-%d" % (i + 1), st.strftime("%Y-%m-%d %H:%M"), en.strftime("%H:%M") + nxt, cat, notice])
        else:
            fmt_k = rng.randrange(4)
            if not mis_done and big and x["kind"] in ("out", "maint") and m >= 12 and rng.random() < 0.4:
                if m % 6 == 0 and rng.random() < 0.5:
                    dur = "%s h" % dstr(D(m) / 60)
                    x["mis"] = F(m, 60)
                else:
                    dur = "{:,} s".format(m * 60)
                    x["mis"] = m * 60
                mis_done = True
                ntr += 1
            elif fmt_k == 0 or m < 60:
                dur = "%d min" % m
            elif fmt_k == 1:
                dur = "%d h %02d min" % (m // 60, m % 60)
            elif fmt_k == 2:
                dur = "%d:%02d (h:mm)" % (m // 60, m % 60)
            else:
                dur = "%d min" % m
            rows.append(["I-%d" % (i + 1), st.strftime("%Y-%m-%d %H:%M"), dur, cat, notice])
    headers = ["Ref", "Start (UTC)", "End (UTC)" if layout == "startend" else "Duration", "Category", "Notice"]
    tier = sla_eval(incs, total, thr, incl, rnd, req)
    check = sla_check(incs, total, thr_s, incl, rnd, req)
    ev = lambda **kw: sla_eval(incs, kw.pop("total", total), thr, kw.pop("incl", incl), kw.pop("rnd", rnd), req, **kw)
    talts = {}
    if any(x["kind"] == "maint" and x["notice"] >= req for x in incs):
        talts["counted_announced_maintenance"] = ev(cnt_maint=True)
    if any(x["kind"] == "maint" and x["notice"] < req for x in incs):
        talts["excluded_late_notice_maintenance"] = ev(excl_late=True)
    if any(x["kind"] == "cust" for x in incs):
        talts["counted_customer_caused"] = ev(cnt_cust=True)
    if any(x["kind"] == "degr" for x in incs):
        talts["counted_degraded_performance"] = ev(cnt_degr=True)
    if mis_done:
        talts["unit_mixup_duration"] = ev(unit_mis=True)
    talts["boundary_inclusivity"] = ev(incl=not incl)
    if rnd == "none":
        talts["rounded_uptime"] = ev(rnd="round2")
    else:
        talts["ignored_rounding_rule"] = ev(rnd="none")
    talts["wrong_month_length"] = ev(total=(30 if nd != 30 else 31) * 1440)
    mname = "%s %d" % (calendar.month_name[mo], y)
    bands = ["0: No service credit"] + ["%d: %d%% service credit" % (i + 1, p) for i, p in enumerate(pcts)]
    rules = [pick(rng, [
        "Monthly Uptime Percentage = (total minutes in the calendar month - Downtime minutes) / total minutes in the month x 100.",
        "Uptime % for a month is computed as (minutes in the month minus Downtime minutes) divided by minutes in the month, times 100.",
    ])]
    rules.append(pick(rng, [
        "Downtime excludes: (a) scheduled maintenance announced at least %d hours in advance; (b) outages caused by the "
        "customer's own equipment, configuration or actions; (c) periods of degraded performance while the service remains "
        "available. Maintenance announced with less notice counts as Downtime." % req,
        "Scheduled maintenance is not excluded from Downtime unless it was announced at least %d hours in advance. "
        "Customer-caused outages and degraded-but-available periods are not Downtime." % req]))
    rules.append({"none": "The Monthly Uptime Percentage is used as calculated, without rounding.",
                  "round2": "Round the Monthly Uptime Percentage to two decimal places (half up) before applying the tiers.",
                  "trunc2": "Truncate (do not round) the Monthly Uptime Percentage to two decimal places before applying the tiers."}[rnd])
    tier_rows = []
    word = "at or below" if incl else "below"
    for i in range(3):
        if i < 2:
            cond = "%s %s%% but %s %s%%" % (word, thr_s[i], "above" if incl else "at least", thr_s[i + 1])
        else:
            cond = "%s %s%%" % (word, thr_s[i])
        tier_rows.append([cond, "%d%% of the monthly fee" % pcts[i]])
    rule_table = None
    if rng.random() < 0.5:
        rules.append("Service credits by Monthly Uptime Percentage: " + "; ".join("%s -> %s" % (a, b) for a, b in tier_rows)
                     + "; otherwise no credit.")
    else:
        rule_table = ("Service credit tiers", ["Monthly Uptime Percentage", "Credit"],
                      tier_rows + [["%s %s%%" % ("above" if incl else "at or above", thr_s[0]), "no credit"]])
    rules.append("Only the single highest applicable tier is paid; tiers do not stack.")
    facts = [("Service", "%s (%s)" % (svc, cid)), ("Measurement month", mname), ("Monthly fee", M(fee))]
    ft = ("Incident log", headers, rows) if rows else None
    if not rows:
        facts.append(("Incident log", "no incidents recorded"))
    if not big:
        rtxt = {"none": "", "round2": ", rounded half up to 2 decimals", "trunc2": ", truncated to 2 decimals"}[rnd]
        rules = ["Uptime %% = (minutes in the month - downtime minutes) / minutes in the month x 100%s." % rtxt,
                 pick(rng, ["Not downtime: maintenance announced at least %d h ahead; customer-caused outages." % req,
                            "Maintenance counts as downtime unless announced %d h or more in advance; customer-caused "
                            "outages never count." % req]),
                 "Credit (highest tier only): " + "; ".join("%s %s%% -> %d%%" % (word, thr_s[i], pcts[i]) for i in range(3)) + "."]
        rule_table = None
        kind_txt = {"out": "outage", "maint": "maintenance", "cust": "customer-caused outage", "degr": "degraded"}
        items = []
        for x, r_ in zip(incs, rows):
            t = "%s %s, %s" % (r_[0], x["start"].strftime("%d %b %H:%M"), r_[2])
            t += " " + kind_txt[x["kind"]]
            if x["kind"] == "maint":
                t += " (announced %d h ahead)" % x["notice"]
            items.append(t)
        facts = [("Service", "%s (%s)" % (svc, cid)), ("Month", mname)]
        if as_amount:
            facts.append(("Monthly fee", M(fee)))
        facts.append(("Incidents", "; ".join(items) if items else "none"))
        ft = None
    reasons = {"counted_announced_maintenance": "every minute the service was down counts",
               "counted_customer_caused": "the service was down either way"}
    base = dict(cur=cur, domain="telecom/SaaS incidents", scen="sla", cid=cid, M=M,
                title=pick(rng, ["Service Level Agreement - Availability Commitment", "SLA Schedule 2: Uptime and Credits",
                                 "Master Services Agreement - Availability Credits"]),
                rules=rules, rule_table=rule_table, facts=facts, fact_table=ft, reasons=reasons, ntr=ntr)
    if as_amount:
        amt = lambda t: q2(fee * pcts[t - 1] / 100) if t > 0 else D("0.00")
        alts = {k: amt(v) for k, v in talts.items()}
        return mk(fmt=M, gold=amt(tier), check=F(amt(check)), alts=alts, thing="service credit",
                  q_choice=pick(rng, ["What service credit is owed for %s for %s?" % (cid, mname),
                                      "How much credit should be applied for %s (%s)?" % (cid, mname)]),
                  q_prop=lambda v: "The account team plans to credit %s for %s (%s). Is that the correct credit?" % (v, cid, mname),
                  q_thr=lambda c, t: "Is the service credit for %s for %s %s %s?" % (cid, mname, c, t), **base)
    alts = {k: bands[v] for k, v in talts.items()}

    def qb(b):
        i = bands.index(b)
        if i == 0:
            return pick(rng, ["Is it correct that no service credit is due for %s for %s?" % (cid, mname),
                              "Should %s receive no service credit for %s?" % (cid, mname)])
        return pick(rng, ["Does %s qualify for exactly the %d%% credit tier for %s?" % (cid, pcts[i - 1], mname),
                          "Is the applicable credit for %s in %s the %d%% tier?" % (cid, mname, pcts[i - 1])])
    return mk(kind="band", bands=bands, gold=bands[tier], check=bands[check], alts=alts, thing="credit tier",
              q_choice=pick(rng, ["Which service-credit tier applies to %s for %s?" % (cid, mname),
                                  "What credit level is %s entitled to for %s?" % (cid, mname)]),
              q_band=qb, **base)


# ------------------------------------------------------------------------ 5 loan
def loan_days(s, e, conv):
    if conv == "30/360":
        return 360 * (e.year - s.year) + 30 * (e.month - s.month) + (min(e.day, 30) - min(s.day, 30))
    return (e - s).days


def loan_int(P, rate, days, basis):
    return q2(P * rate / 100 * days / basis)


def loan_check(P, rate, s, e, conv):
    if conv == "30/360":
        a = s.year * 360 + (s.month - 1) * 30 + (30 if s.day >= 30 else s.day)
        b = e.year * 360 + (e.month - 1) * 30 + (30 if e.day >= 30 else e.day)
        days, basis = b - a, 360
    else:
        days = 0
        d = s
        while d < e:
            days += 1
            d += TD(days=1)
        basis = 360 if conv == "ACT/360" else 365
    return fr_round(F(P) * F(rate) * days / (100 * basis))


def S_loan(rng, mode, cur=None):
    big = mode != "short"
    cur = cur or pick(rng, CURS)
    M = lambda x: money(x, cur)
    ds = rng.randrange(4)
    P = D(rng.randrange(20, 1500) * 500)
    conv = pick(rng, ["ACT/360", "ACT/365", "30/360"])
    basis = 365 if conv == "ACT/365" else 360
    s = rand_date(rng)
    if conv == "30/360" and rng.random() < 0.4:
        s = s.replace(day=pick(rng, [28, 30, 31]) if s.month in (1, 3, 5, 7, 8, 10, 12) else 28)
    e = s + TD(days=rng.randint(28, 184))
    cid = "FAC-%d" % rng.randint(1000, 9999)
    floating = rng.random() < 0.6
    rules, versions, alts, reasons, facts = [], [], {}, {}, []
    ntr = 1
    spread_other = None
    if floating:
        base = D(rng.randint(150, 560)) / 100
        spread = pick(rng, [125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 410])
        floor = None
        if rng.random() < 0.45:
            floor = qn((base + D(rng.randint(5, 90)) / 100) * 4, 0) / 4 if rng.random() < 0.6 else \
                qn((base - D(rng.randint(10, 90)) / 100) * 4, 0) / 4
            ntr += 1
        eff_base = max(base, floor) if floor is not None else base
        use_ver = big and rng.random() < 0.45
        if use_ver:
            v = plan_version(rng, s)
            spread_other = spread + pick(rng, [-50, -25, 25, 40, 50])
            o, n = (spread_other, spread) if v["new"] else (spread, spread_other)
            versions = version_blocks(v, "the margin is %d bps" % o, "the margin is %d bps" % n,
                                      "interest period start date", ds)
            ntr += 1
        rate = eff_base + D(spread) / 100
        mtxt = "the margin shown in the rate history" if use_ver else "a margin of %d basis points (bps)" % spread
        rules.append(pick(rng, [
            "The interest rate for each period is the Base Rate plus %s." % mtxt,
            "Interest rate = Base Rate + %s; 100 bps = 1 percentage point." % mtxt]))
        if floor is not None:
            rules.append(pick(rng, [
                "If the Base Rate is below %s%%, the Base Rate is deemed to be %s%% (floor)." % (dstr(floor), dstr(floor)),
                "Base Rate floor: %s%%. A published Base Rate lower than the floor is not used; the floor applies instead." % dstr(floor)]))
        facts.append(("Base Rate fixed for the period", "%s%%" % dstr(base)))
    else:
        rate = D(rng.randint(450, 1150)) / 100
        rules.append("Interest accrues at a fixed rate of %s%% per annum." % dstr(rate))
        eff_base = spread = floor = base = None
    dcw = {"ACT/360": "actual number of days elapsed divided by 360",
           "ACT/365": "actual number of days elapsed divided by 365 (also in leap years)",
           "30/360": "30/360: every month counts as 30 days (a day 31 is treated as day 30) and the year as 360 days"}[conv]
    rules.append(pick(rng, [
        "Day count: %s." % dcw,
        "Interest is computed on the principal x annual rate x day-count fraction, where the day-count fraction is the %s." % dcw]))
    rules.append(pick(rng, [
        "Interest accrues from and including the first day of the period to but excluding the last day.",
        "Count days from the period start date (included) to the period end date (excluded)."]))
    rules.append("Round the interest amount to the nearest cent (half up).")
    days = loan_days(s, e, conv)
    gold = loan_int(P, rate, days, basis)
    check = loan_check(P, rate, s, e, conv)
    if conv == "30/360":
        alts["used_actual_days"] = loan_int(P, rate, (e - s).days, 360)
    else:
        alts["wrong_day_count_basis"] = loan_int(P, rate, days, 365 if basis == 360 else 360)
    alts["counted_both_end_dates"] = loan_int(P, rate, days + 1, basis)
    if floating:
        if floor is not None and floor > base:
            alts["ignored_rate_floor"] = loan_int(P, base + D(spread) / 100, days, basis)
        if spread_other is not None:
            alts["wrong_rule_version"] = loan_int(P, eff_base + D(spread_other) / 100, days, basis)
        alts["bps_misconverted"] = loan_int(P, eff_base + D(spread) / 1000, days, basis)
        alts["used_base_rate_only"] = loan_int(P, eff_base, days, basis)
    else:
        alts["used_whole_months"] = q2(P * rate / 100 / 12 * max(1, round(days / 30)))
    alts["simple_365_convention"] = loan_int(P, rate, (e - s).days, 365)
    facts = [("Facility", cid), ("Outstanding principal", M(P)),
             ("Interest period", "%s to %s" % (fdate(s, ds), fdate(e, ds)))] + facts
    if floating:
        facts.append(("Margin (per term sheet)", "%d bps" % spread) if spread_other is None else
                     ("Borrower", pick(rng, ["Northfield Logistics Ltd", "Aster Dental Group", "Kilnworth Farms LLC"])))
    if not big:
        dc = {"ACT/360": "actual days / 360", "ACT/365": "actual days / 365",
              "30/360": "30/360 (every month 30 days, a day 31 counts as 30; year of 360 days)"}[conv]
        rules = []
        if floating:
            rules.append(pick(rng, ["Rate = Base Rate + %d bps (100 bps = 1 percentage point)." % spread,
                                    "Interest rate: Base Rate plus a margin of %d basis points." % spread]))
            if floor is not None:
                rules.append("Base Rate floor: %s%%." % dstr(floor))
        else:
            rules.append("Fixed rate: %s%% per annum." % dstr(rate))
        rules.append("Day count %s; count from the start date (included) to the end date (excluded)." % dc)
        rules.append("Round the interest half up to the cent.")
    return mk(cur=cur, domain="banking/loans", scen="loan", cid=cid, M=M, fmt=M,
              title=pick(rng, ["Term Loan Agreement - Interest Clause", "Facility Agreement: Schedule 3 (Interest)",
                               "Credit Operations - Interest Calculation Standard"]),
              rules=rules, versions=versions, facts=facts, gold=gold, check=check, alts=alts, reasons=reasons,
              ntr=ntr, thing="interest amount",
              q_choice=pick(rng, ["How much interest is payable on facility %s for the period ending %s?" % (cid, fdate(e, ds)),
                                  "What is the interest due on %s for this interest period?" % cid]),
              q_prop=lambda v: "The loan system computed %s of interest for %s for this period. Is that correct?" % (v, cid),
              q_thr=lambda c, t: "Is the interest due on %s for this period %s %s?" % (cid, c, t))


# ------------------------------------------------------------------------ 6 shipping
def ship_calc(dims, wt, div, first, addl, fuel_pct, resid_fee, use="max", rnd="up", fuel_total=False):
    dim = dims[0] * dims[1] * dims[2] / div
    bw = max(wt, dim) if use == "max" else (wt if use == "actual" else dim)
    x = bw * 2
    units = int(x.to_integral_value(rounding=ROUND_CEILING if rnd == "up" else ROUND_HALF_UP))
    units = max(units, 1)
    base = first + (units - 1) * addl
    fuel = q2((base + resid_fee if fuel_total else base) * fuel_pct / 100)
    return q2(base + fuel + resid_fee)


def ship_check(dims, wt, div, first, addl, fuel_pct, resid_fee):
    vol = F(dims[0]) * F(dims[1]) * F(dims[2])
    halfs_dim = math.ceil(vol * 2 / F(div))
    halfs_act = math.ceil(F(wt) * 2)
    units = max(halfs_dim, halfs_act, 1)
    base = F(first) + (units - 1) * F(addl)
    return fr_round(base + fr_round(base * F(fuel_pct) / 100) + F(resid_fee))


def S_ship(rng, mode, cur=None):
    big = mode != "short"
    cur = cur or pick(rng, CURS)
    M = lambda x: money(x, cur)
    ds = rng.randrange(4)
    cid = "SHP-%d" % rng.randint(100000, 999999)
    imperial = rng.random() < 0.35
    div = pick(rng, [5000, 6000, 4000])
    if imperial:
        dims_in = [rng.randint(8, 32), rng.randint(6, 24), rng.randint(4, 20)]
        lb = D(rng.randint(20, 400)) / 10
        dims = [D(x) * D("2.54") for x in dims_in]
        wt = lb * D("0.45359237")
    else:
        dims = [D(rng.randint(15, 90)), D(rng.randint(12, 60)), D(rng.randint(8, 50))]
        wt = D(rng.randint(4, 300)) / 10
    first = D(rng.randint(690, 1490)) / 100
    addl = D(rng.randint(95, 295)) / 100
    fuel = D(pick(rng, ["8.5", "9.75", "11", "12.25", "14", "16.5", "18"]))
    resid_feat = rng.random() < (0.6 if big else 0.3)
    addr = pick(rng, ["residential (house)", "residential (apartment door)", "parcel locker inside an apartment building",
                      "business address (office reception)"]) if resid_feat else "business address (warehouse dock)"
    resid_amt = D(pick(rng, ["3.95", "4.95", "5.60", "6.25"]))
    resid = resid_amt if addr.startswith("residential") else D(0)
    ntr = 1 + (1 if imperial else 0) + (1 if resid_feat else 0)
    ship_date = rand_date(rng)
    rules, versions, alts, reasons = [], [], {}, {}
    div_other = None
    if big and rng.random() < 0.45:
        v = plan_version(rng, ship_date)
        div_other = pick(rng, [x for x in (4000, 5000, 6000) if x != div])
        o, n = (div_other, div) if v["new"] else (div, div_other)
        versions = version_blocks(v, "the dimensional divisor is %d" % o, "the dimensional divisor is %d" % n, "ship date", ds)
        ntr += 1
        dtxt = "the divisor in the rate-card history"
    else:
        dtxt = str(div)
    rules.append(pick(rng, [
        "Billable weight is the greater of the actual weight and the dimensional weight.",
        "We charge on whichever is higher: actual (scale) weight or dimensional weight."]))
    rules.append("Dimensional weight (kg) = length x width x height in cm / %s." % dtxt)
    rules.append(pick(rng, ["Round the billable weight up to the next 0.5 kg.",
                            "Billable weight is charged in 0.5 kg steps; any part of a step counts as a full step."]))
    rules.append("Weight charge: %s for the first 0.5 kg plus %s for each additional 0.5 kg." % (M(first), M(addl)))
    rules.append(pick(rng, ["Fuel surcharge: %s%% of the weight charge only (not of other surcharges); round to the cent." % dstr(fuel),
                            "A %s%% fuel surcharge applies to the weight charge; it is not applied to accessorial fees. Round to the cent." % dstr(fuel)]))
    if resid_feat:
        rules.append(pick(rng, [
            "Residential delivery surcharge: %s per parcel. Parcel lockers are not residential addresses, even inside apartment buildings." % M(resid_amt),
            "Deliveries to homes carry a %s residential surcharge; lockers and business addresses do not." % M(resid_amt)]))
    if imperial:
        rules.append("Measurements taken in inches or pounds must be converted first (1 in = 2.54 cm; 1 lb = 0.45359237 kg).")
    base = dict(dims=dims, wt=wt, div=div, first=first, addl=addl, fuel_pct=fuel, resid_fee=resid)

    def sc(**kw):
        q = dict(base)
        q.update(kw)
        return ship_calc(**q)

    gold = sc()
    check = ship_check(dims, wt, div, first, addl, fuel, resid)
    dimw = dims[0] * dims[1] * dims[2] / div
    alts["used_actual_weight" if dimw > wt else "used_dimensional_weight"] = sc(use="actual" if dimw > wt else "dim")
    alts["rounded_to_nearest_step"] = sc(rnd="nearest")
    if div_other:
        alts["wrong_rule_version"] = sc(div=div_other)
    else:
        alts["wrong_divisor"] = sc(div=6000 if div != 6000 else 5000)
    if resid > 0:
        alts["fuel_on_total"] = sc(fuel_total=True)
        alts["missed_residential_surcharge"] = sc(resid_fee=D(0))
    elif resid_feat and "locker" in addr:
        alts["locker_treated_as_residential"] = sc(resid_fee=resid_amt)
        reasons["locker_treated_as_residential"] = "it's an apartment building, so residential"
    if imperial:
        alts["lb_as_kg"] = sc(wt=lb)
        alts["inches_not_converted"] = sc(dims=[D(x) for x in dims_in])
    alts["forgot_fuel_surcharge"] = sc(fuel_pct=D(0))
    if imperial:
        dtxt_f = "%d x %d x %d in" % tuple(dims_in)
        wtxt = "%s lb" % dstr(lb)
    else:
        dtxt_f = "%s x %s x %s cm" % tuple(dstr(x) for x in dims)
        wtxt = "%s kg" % dstr(wt)
    facts = [("Shipment", cid), ("Ship date", fdate(ship_date, ds)), ("Parcel dimensions", dtxt_f),
             ("Scale weight", wtxt), ("Delivery address type", addr)]
    if big and rng.random() < 0.4:
        facts.append(("Declared value", M(D(rng.randint(40, 900)))))
    if not big:
        rules = [pick(rng, ["Billable weight = the greater of actual weight and L x W x H (cm) / %d, rounded up to the next 0.5 kg." % div,
                            "Charge on max(actual kg, cm3 / %d), rounded up to a whole 0.5 kg step." % div]),
                 "Price: %s for the first 0.5 kg + %s per additional 0.5 kg; fuel surcharge %s%% of that weight charge only (to the cent)."
                 % (M(first), M(addl), dstr(fuel))]
        if resid_feat:
            rules.append("Residential delivery: +%s (parcel lockers are not residential)." % M(resid_amt))
        if imperial:
            rules.append("Convert first: 1 in = 2.54 cm; 1 lb = 0.45359237 kg.")
    return mk(cur=cur, domain="logistics/shipping", scen="ship", cid=cid, M=M, fmt=M,
              title=pick(rng, ["Parcel Rate Card - Domestic Express", "Carrier Pricing Guide (2025 edition)",
                               "Shipping Charges: How We Bill"]),
              rules=rules, versions=versions, facts=facts, gold=gold, check=check, alts=alts, reasons=reasons,
              ntr=ntr, thing="shipping charge",
              q_choice=pick(rng, ["What is the total charge for shipment %s?" % cid,
                                  "How much will the carrier bill for shipment %s?" % cid]),
              q_prop=lambda v: "The invoice shows %s for shipment %s. Is that the correct charge?" % (v, cid),
              q_thr=lambda c, t: "Is the total charge for shipment %s %s %s?" % (cid, c, t))


# ------------------------------------------------------------------------ 7 QA
QA_NAMES = [("RELEASE", "RETEST", "REJECT"), ("Accept", "Hold for retest", "Reject"),
            ("PASS", "INCONCLUSIVE - RETEST", "FAIL")]
QA_CARD = ["lot conforms; release it to the warehouse", "result is inconclusive; hold the lot and retest",
           "lot does not conform; quarantine it for scrap or rework"]


def qa_decide(lo, hi, m, U, strict):
    a, b = m - U, m + U
    if strict:
        inside = (lo is None or a > lo) and (hi is None or b < hi)
    else:
        inside = (lo is None or a >= lo) and (hi is None or b <= hi)
    if inside:
        return 0
    outside = (lo is not None and b < lo) or (hi is not None and a > hi)
    return 2 if outside else 1


def qa_check(lo, hi, m, U, strict):
    m, U = F(m), F(U)
    res = 0
    for lim, side in ((lo, -1), (hi, 1)):
        if lim is None:
            continue
        lim = F(lim)
        near, far = m + side * U, m - side * U
        if side * (far - lim) > 0:
            res = max(res, 2)
        elif side * (near - lim) > 0 or (strict and near == lim):
            res = max(res, 1)
    return res


def qa_pick_m(rng, lo, hi, U, step, target):
    """Choose a measured value on the grid `step` near the band `target` (0 accept, 1 retest, 2 reject)."""
    g = lambda x: int((D(x) / step).to_integral_value(rounding=ROUND_HALF_UP))
    if target == 0:
        a = g(lo + U) if lo is not None else g(hi - U) - 40
        b = g(hi - U) if hi is not None else g(lo + U) + 40
        if a > b:
            a, b = b, a
        k = pick(rng, [a, b]) if rng.random() < 0.3 else rng.randint(a, b)
    elif target == 1:
        sides = [s for s in ("lo", "hi") if (lo if s == "lo" else hi) is not None]
        sd = pick(rng, sides)
        L = lo if sd == "lo" else hi
        a, b = g(L - U) + 1, g(L + U) - 1
        k = pick(rng, [a, b, g(L)]) if rng.random() < 0.35 else rng.randint(a, max(a, b))
    else:
        sides = [s for s in ("lo", "hi") if (lo if s == "lo" else hi) is not None]
        sd = pick(rng, sides)
        if sd == "lo":
            k = g(lo - U) - pick(rng, [1, 1, rng.randint(2, 30)])
        else:
            k = g(hi + U) + pick(rng, [1, 1, rng.randint(2, 30)])
    return D(k) * step


def S_qa(rng, mode, cur=None):
    big = mode != "short"
    ds = rng.randrange(4)
    names = pick(rng, QA_NAMES)
    variant = pick(rng, ["mass", "conc", "impurity"])
    cid = "LOT-%s%d" % (pick(rng, ["A", "B", "K", "M", "T"]), rng.randint(10000, 99999))
    strict = rng.random() < 0.3
    target = rng.randrange(3)
    rules, facts, talts, reasons = [], [("Lot", cid)], {}, {}
    ntr = 1
    dec_rule = pick(rng, [
        "Decision rule (guard-banded): accept only if the whole interval result +/- U lies within the specification%s. "
        "Reject only if the whole interval lies outside the specification. Otherwise the result is inconclusive and the lot "
        "must be retested." % (" and does not touch a limit (an interval edge exactly on a limit is NOT acceptable)" if strict
                               else " (an interval edge exactly on a limit is acceptable)"),
        "Conformity is decided with the measurement uncertainty U: conforming if result - U %s lower limit and result + U %s "
        "upper limit; non-conforming if result + U is below the lower limit or result - U is above the upper limit; "
        "anything else is inconclusive (retest)." % ((">", "<") if strict else (">=", "<="))])
    if variant == "mass":
        nom = pick(rng, [250, 500, 750, 1000])
        tol = D(pick(rng, ["1", "1.5", "2"]))
        lo = D(nom) * (1 - tol / 100)
        hi = D(nom) * (1 + tol / 100)
        U = D(pick(rng, ["0.4", "0.6", "0.8", "1.2"]))
        m = qa_pick_m(rng, lo, hi, U, D("0.1"), target)
        product = pick(rng, ["ground coffee", "infant formula", "dry pet food", "rice", "protein powder"])
        rules.append("Specification for %s %d g packs: net mass %s g to %s g." % (product, nom, dstr(lo), dstr(hi)))
        srules = ["Spec (%s, %d g packs): net mass %s-%s g; U = %s g (k = 2, already expanded)." % (product, nom, dstr(lo), dstr(hi), dstr(U)),
                  "Judge the as-weighed net mass (gross - tare), not the corrected value."]
        rules.append("Expanded measurement uncertainty of the weighing method: U = %s g (k = 2; already expanded - do "
                     "not multiply it again)." % dstr(U))
        rules.append(dec_rule)
        rules.append(pick(rng, ["Assess the as-weighed net mass (gross minus tare). Temperature-corrected values on the "
                                "printout are for trend charts only.",
                                "Use the original as-weighed net mass; do not use the corrected mass shown on the printout."]))
        corr = m + pick(rng, [D(1), D(-1)]) * D(rng.randint(5, 30)) / 10
        if rng.random() < 0.5:
            tare = D(rng.randint(150, 450)) / 10
            gross = m + tare
            facts += [("Gross mass", "%s kg" % dstr(qn(gross / 1000, 4))), ("Tare (container)", "%s g" % dstr(tare))]
            talts["used_gross_mass"] = qa_decide(lo, hi, gross, U, strict)
            ntr += 1
        else:
            facts.append(("Net mass as weighed", "%s g" % dstr(m) if rng.random() < 0.6 else "%s kg" % dstr(qn(m / 1000, 4))))
        facts.append(("Temperature-corrected net mass (informational)", "%s g" % dstr(corr)))
        talts["used_corrected_mass"] = qa_decide(lo, hi, corr, U, strict)
        lo_, hi_ = lo, hi
    elif variant == "conc":
        nom = D(pick(rng, [2, 5, 10, 20, 25]))
        tol = D(pick(rng, [5, 10]))
        lo = nom * (1 - tol / 100)
        hi = nom * (1 + tol / 100)
        U = qn(nom * D(pick(rng, ["1", "1.5", "2"])) / 100, 2)
        step = D("0.01")
        m = qa_pick_m(rng, lo, hi, U, step, target)
        api = pick(rng, ["lidocaine HCl", "caffeine citrate", "ondansetron", "sodium benzoate", "potassium sorbate"])
        rules.append("Specification: %s concentration %s mg/mL to %s mg/mL." % (api, dstr(lo), dstr(hi)))
        srules = ["Spec: %s %s-%s mg/mL; U = %s mg/mL (k = 2, already expanded)." % (api, dstr(lo), dstr(hi), dstr(U))]
        rules.append("Expanded uncertainty of the assay: U = %s mg/mL (k = 2, already expanded)." % dstr(U))
        rules.append(dec_rule)
        if rng.random() < 0.5:
            rules.append("Unit note: 1% w/v = 1 g per 100 mL = 10 mg/mL.")
            srules.append("1% w/v = 10 mg/mL.")
            facts.append(("Assay result", "%s %% w/v" % dstr(m / 10)))
            talts["percent_unit_mixup"] = qa_decide(lo, hi, m / 10, U, strict)
            ntr += 1
        else:
            dil = pick(rng, [2, 4, 5, 10])
            rules.append("Samples are diluted before analysis; multiply the instrument reading by the dilution factor.")
            srules.append("Multiply the reading by the dilution factor.")
            facts.append(("Instrument reading (diluted sample)", "%s mg/mL" % dstr(m / dil)))
            facts.append(("Dilution", "1:%d" % dil))
            talts["forgot_dilution_factor"] = qa_decide(lo, hi, m / dil, U, strict)
            ntr += 1
        lo_, hi_ = lo, hi
    else:
        limp = D(pick(rng, ["0.10", "0.15", "0.20", "0.50"]))
        hi = limp * 10000
        lo = None
        U = D(rng.randint(3, 15) * 10)
        m = qa_pick_m(rng, None, hi, U, D(1), target)
        imp = pick(rng, ["Impurity B", "residual solvent (ethanol)", "total related substances", "heavy metals (as Pb)"])
        rules.append("Specification: %s not more than %s%% w/w." % (imp, dstr(limp)))
        srules = ["Spec: %s NMT %s%% w/w (1%% w/w = 10,000 ppm); U = %s ppm (k = 2)." % (imp, dstr(limp), dstr(U))]
        rules.append("Unit note: 1% w/w = 10,000 ppm (mg/kg).")
        rules.append("Expanded uncertainty of the method: U = %s ppm (k = 2)." % dstr(U))
        rules.append(dec_rule.replace("within the specification", "at or below the limit" if not strict else "below the limit"))
        facts.append(("Result", "{:,} ppm".format(int(m))))
        talts["ppm_conversion_error"] = qa_decide(None, limp * 1000, m, U, strict)
        ntr += 1
        lo_, hi_ = lo, hi
    facts.append(("Tested", fdate(rand_date(rng), ds)))
    if not big:
        within = "at or below the limit" if variant == "impurity" else "within the spec"
        if strict:
            dr = "Release only if result +/- U is strictly %s (touching a limit is not enough)" % within.replace("at or below", "below")
        else:
            dr = "Release if result +/- U is entirely %s (touching a limit is OK)" % within
        rules = srules + [dr + "; reject if it is entirely outside; otherwise retest."]
        facts = [(a, b) for a, b in facts if a != "Tested"]
    gold = qa_decide(lo_, hi_, m, U, strict)
    check = qa_check(lo_, hi_, m, U, strict)
    talts["ignored_uncertainty"] = qa_decide(lo_, hi_, m, D(0), strict)
    talts["doubled_uncertainty"] = qa_decide(lo_, hi_, m, U * 2, strict)
    talts["boundary_inclusivity"] = qa_decide(lo_, hi_, m, U, not strict)
    reasons.update({"ignored_uncertainty": "the reading itself is inside the spec",
                    "used_corrected_mass": "corrected figure is the accurate one"})
    bands = list(names)
    alts = {k: bands[v] for k, v in talts.items()}
    card = [(names[i], QA_CARD[i]) for i in range(3)]

    def qb(b):
        i = bands.index(b)
        return [pick(rng, ["Can lot %s be released under the decision rule?" % cid, "Does lot %s pass and get released?" % cid]),
                pick(rng, ["Should lot %s be held for retest?" % cid, "Is the result for lot %s inconclusive (retest)?" % cid]),
                pick(rng, ["Must lot %s be rejected?" % cid, "Is lot %s non-conforming (reject)?" % cid])][i]
    return mk(domain="manufacturing QA", scen="qa", cid=cid, M=lambda x: money(x, ("$", "p")), kind="band",
              bands=bands, card=card,
              title=pick(rng, ["QC Release Procedure SOP-QA-114", "Quality Control - Lot Disposition Rules",
                               "Batch Release Standard (Measurement Uncertainty)"]),
              rules=rules, facts=facts, gold=bands[gold], check=bands[check], alts=alts, reasons=reasons, ntr=ntr,
              thing="disposition",
              q_choice=pick(rng, ["What disposition applies to lot %s?" % cid,
                                  "Under the decision rule, how should lot %s be dispositioned?" % cid]),
              q_band=qb)


# ------------------------------------------------------------------------ 8 HR leave
def hr_calc(B0, C, n, acc, taken_h, Pc, salary, ann_h):
    hourly = q2(salary / ann_h)
    bal = (min(B0, C) if C is not None else B0) + n * acc - taken_h
    hrs = min(bal, Pc) if Pc is not None else bal
    return q2(max(hrs, D(0)) * hourly)


def hr_check(B0, C, p1, td, acc, taken_days, hw, Pc, salary):
    hourly = fr_round(F(salary) / (F(hw) * 52))
    bal = F(B0) if F(B0) < F(C) else F(C)
    p = p1
    while p <= td:
        bal += F(acc)
        p += TD(days=14)
    bal -= F(taken_days) * F(hw) / 5
    if Pc is not None and bal > F(Pc):
        bal = F(Pc)
    return fr_round(max(bal, F(0)) * hourly)


def S_hr(rng, mode, cur=None):
    big = mode != "short"
    cur = cur or pick(rng, CURS)
    M = lambda x: money(x, cur)
    ds = rng.randrange(4)
    hw = pick(rng, [D(40), D("37.5"), D(35)])
    hpd = hw / 5
    ann_h = hw * 52
    salary = D(rng.randrange(42000, 150000, 500))
    y = pick(rng, [2024, 2025, 2026])
    p1 = DT(y, 1, rng.randint(3, 16))
    if rng.random() < 0.35:
        td = p1 + TD(days=14 * rng.randint(3, 20))
    else:
        td = p1 + TD(days=rng.randint(30, 300))
    n = 0
    p = p1
    while p <= td:
        n += 1
        p += TD(days=14)
    on_end = (td - p1).days % 14 == 0
    acc_mode = pick(rng, ["hours", "days"])
    if acc_mode == "hours":
        acc = D(pick(rng, ["3.08", "4.62", "6.15", "5.54", "3.69"]))
        dpy = None
    else:
        dpy = pick(rng, [15, 18, 20, 25])
        acc = q2(D(dpy) * hpd / 26)
    C = D(pick(rng, [40, 80, 100, 120]))
    B0 = D(rng.randint(30, 180)) + D(pick(rng, ["0", "0", "0.5", "0.25"]))
    taken_days = D(rng.randint(1, 14)) + pick(rng, [D(0), D(0), D("0.5")])
    taken_h = taken_days * hpd
    while min(B0, C) + n * acc - taken_h <= 8:
        taken_days = max(D(0), taken_days - 2)
        taken_h = taken_days * hpd
        if taken_days == 0:
            break
    bal = min(B0, C) + n * acc - taken_h
    Pc = pick(rng, [None, None, D(120), D(160), D(200)])
    if Pc is not None and rng.random() < 0.5 and bal > 56:
        Pc = D(max(40, (int(bal) - rng.randint(1, 24)) // 8 * 8))
    cid = "EMP-%d" % rng.randint(10000, 99999)
    ntr = 1 + (1 if B0 > C else 0) + (1 if on_end else 0) + (1 if hw != 40 else 0)
    versions, alts, reasons = [], {}, {}
    acc_other = None
    if big and acc_mode == "hours" and rng.random() < 0.45:
        acc_other = D(pick(rng, [x for x in ["3.08", "4.62", "6.15", "5.54", "3.69"] if D(x) != acc]))
        new = rng.random() < 0.6
        eff = DT(y, 1, 1) if new else td + TD(days=rng.randint(1, 90))
        v = {"new": new, "eff": eff, "eff_old": eff - TD(days=rng.randint(400, 1100)), "rev": rng.randint(2, 9),
             "style": rng.randrange(4), "flip": rng.random() < 0.5}
        o, nn = (acc_other, acc) if new else (acc, acc_other)
        versions = version_blocks(v, "leave accrues at %s hours per completed pay period" % dstr(o),
                                  "leave accrues at %s hours per completed pay period" % dstr(nn), "pay period end date", ds)
        ntr += 1
    rules = []
    if acc_mode == "hours":
        atxt = "the rate in the accrual history" if acc_other else "%s hours" % dstr(acc)
        rules.append(pick(rng, [
            "Annual leave accrues at %s per completed biweekly pay period. A period counts only if it ends on or before "
            "the last day of employment." % atxt,
            "Leave is credited at the end of each completed two-week pay period (%s per period); a pay period that has not "
            "ended by the last day worked earns nothing." % atxt]))
    else:
        rules.append("Employees accrue %d working days of leave per year, credited in 26 equal instalments at the end of "
                     "each completed biweekly pay period (a period ending on the last day of employment counts). Convert "
                     "days to hours with the employee's standard day (weekly hours / 5) and round each instalment to two "
                     "decimals." % dpy)
    rules.append(pick(rng, [
        "On 1 January, leave carried over from the previous year is capped at %s hours; any excess is forfeited." % dstr(C),
        "Carry-over into a new year may not exceed %s hours. Hours above the cap are lost on 1 January." % dstr(C)]))
    rules.append("Leave taken is recorded in days and converted at the employee's standard daily hours (weekly hours / 5).")
    rules.append(pick(rng, [
        "Hourly rate = annual salary / (standard weekly hours x 52), rounded to the cent.",
        "For payouts, the hourly rate is the annual salary divided by 52 times the contracted weekly hours (round to the cent)."]))
    if Pc is not None:
        rules.append(pick(rng, ["Unused leave is paid out on termination up to a maximum of %s hours." % dstr(Pc),
                                "Termination payout is capped at %s hours of leave; hours above the cap are not paid." % dstr(Pc)]))
    else:
        rules.append("All accrued, unused leave is paid out on termination (no cap).")
    base = dict(B0=B0, C=C, n=n, acc=acc, taken_h=taken_h, Pc=Pc, salary=salary, ann_h=ann_h)

    def hc(**kw):
        q = dict(base)
        q.update(kw)
        return hr_calc(**q)

    gold = hc()
    check = hr_check(B0, C, p1, td, acc, taken_days, hw, Pc, salary)
    if B0 > C:
        alts["forgot_carryover_cap"] = hc(C=None)
        reasons["forgot_carryover_cap"] = "full balance carries over"
    alts["periods_off_by_one"] = hc(n=n - 1 if on_end else n + 1)
    if hw != 40:
        wrong_hpd = D(8)
        acc_w = acc if acc_mode == "hours" else q2(D(dpy) * wrong_hpd / 26)
        alts["used_8_hour_day"] = hc(taken_h=taken_days * wrong_hpd, acc=acc_w)
        alts["used_2080_hours"] = hc(ann_h=D(2080))
    else:
        alts["used_7_5_hour_day"] = hc(taken_h=taken_days * D("7.5"))
    if Pc is not None and bal > Pc:
        alts["ignored_payout_cap"] = hc(Pc=None)
    if acc_other is not None:
        alts["wrong_rule_version"] = hc(acc=acc_other)
    alts["forgot_leave_taken"] = hc(taken_h=D(0))
    facts = [("Employee", "%s (%s)" % (pick(rng, PEOPLE), cid)), ("Annual salary", M(salary)),
             ("Standard hours", "%s hours per week" % dstr(hw)),
             ("Balance brought forward from last year (before any cap)", "%s hours" % dstr(B0)),
             ("Leave taken this year", "%s days" % dstr(taken_days)),
             ("First pay period of %d ended" % y, "%s (periods are biweekly, every 14 days)" % fdate(p1, ds)),
             ("Last day of employment", fdate(td, ds))]
    if big and rng.random() < 0.4:
        facts.append(("Sick leave balance", "%d hours" % rng.randint(10, 90)))
    if not big:
        acc_t = ("Accrual: %s h per completed biweekly pay period (it counts if it ends on or before the last day)." % dstr(acc)
                 if acc_mode == "hours" else
                 "Accrual: %d days/yr in 26 instalments, one per completed biweekly period (ending on or before the last day), "
                 "converted at weekly hours / 5 and rounded to 2 decimals." % dpy)
        rules = [acc_t, "Carry-over is capped at %s h on 1 January." % dstr(C),
                 "Leave taken (days) converts at weekly hours / 5.",
                 "Hourly rate = salary / (weekly hours x 52), to the cent.",
                 ("Payout cap: %s h." % dstr(Pc)) if Pc is not None else "No payout cap."]
        facts = [("Employee", cid), ("Salary", M(salary)), ("Weekly hours", dstr(hw)),
                 ("Brought forward (before cap)", "%s h" % dstr(B0)), ("Taken this year", "%s days" % dstr(taken_days)),
                 ("First %d pay period ended" % y, fdate(p1, ds)), ("Last day worked", fdate(td, ds))]
    return mk(cur=cur, domain="HR/leave", scen="hr", cid=cid, M=M, fmt=M,
              title=pick(rng, ["Annual Leave Policy - Accrual, Carry-over and Payout", "People Handbook: Leave",
                               "Payroll Guide - Final Pay Calculations"]),
              rules=rules, versions=versions, facts=facts, gold=gold, check=check, alts=alts, reasons=reasons,
              ntr=ntr, thing="leave payout",
              q_choice=pick(rng, ["What leave payout is owed to %s on termination?" % cid,
                                  "How much unused-leave pay should %s receive in the final paycheck?" % cid]),
              q_prop=lambda v: "Payroll has keyed a leave payout of %s for %s. Is that correct?" % (v, cid),
              q_thr=lambda c, t: "Is the leave payout for %s %s %s?" % (cid, c, t))


# ------------------------------------------------------------------------ 9 retail
RET_ITEMS = ["noise-cancelling headphones", "stand mixer", "down jacket", "robot vacuum", "espresso machine",
             "gaming monitor", "carbon trekking poles", "air purifier", "smartwatch", "cast-iron cookware set"]


def retail_calc(Lp, disc, tax, Sh, fee_pct, fee_min, fee_max, fee_applies, ship_back, eligible,
                base_list=False, clamp=True, fee_on_taxed=False, no_tax=False):
    if not eligible:
        return D("0.00")
    paid = Lp if base_list else q2(Lp * (100 - disc) / 100)
    taxamt = D(0) if no_tax else q2(paid * tax / 100)
    fee = D(0)
    if fee_applies:
        fee = q2((paid + taxamt if fee_on_taxed else paid) * fee_pct / 100)
        if clamp:
            fee = min(max(fee, fee_min), fee_max)
    return q2(paid + taxamt - fee + (Sh if ship_back else 0))


def retail_check(Lp, disc, tax, Sh, fee_pct, fee_min, fee_max, cond, k, W):
    if k > W:
        return F(0)
    ledger = []
    paid = fr_round(F(Lp) - F(Lp) * F(disc) / 100)
    ledger.append(paid)
    ledger.append(fr_round(paid * F(tax) / 100))
    if cond in ("opened", "damaged"):
        f = fr_round(paid * F(fee_pct) / 100)
        f = min(max(f, F(fee_min)), F(fee_max))
        ledger.append(-f)
    if cond == "defective":
        ledger.append(F(Sh))
    return sum(ledger, F(0))


def S_retail(rng, mode, cur=None):
    big = mode != "short"
    cur = cur or pick(rng, CURS)
    M = lambda x: money(x, cur)
    ds = rng.randrange(4)
    item = pick(rng, RET_ITEMS)
    Lp = D(rng.randint(40, 900)) + D(pick(rng, [0, 99, 95, 49])) / 100
    disc = D(pick(rng, [0, 10, 15, 20, 25])) if big or rng.random() < 0.5 else D(0)
    tax = D(pick(rng, ["6.25", "7", "8.875", "9.5", "5.5"]))
    Sh = D(pick(rng, ["5.99", "7.95", "12.50", "9.00"]))
    fee_pct = D(pick(rng, [10, 15, 20]))
    fee_min = D(pick(rng, [5, 10, 15]))
    fee_max = D(pick(rng, [40, 50, 75, 100]))
    ver_r, fee_pct_other = None, None
    W = pick(rng, [14, 30, 45])
    delivered = rand_date(rng)
    purchased = delivered - TD(days=rng.randint(2, 7))
    if rng.random() < 0.4:
        k = pick(rng, [W, W + 1, W - 1])
    else:
        k = rng.randint(1, W - 2)
    ret = delivered + TD(days=k)
    eligible = k <= W
    cond = pick(rng, ["unopened", "opened", "opened", "defective", "damaged"]) if big else pick(rng, ["unopened", "opened", "defective"])
    fee_applies = cond in ("opened", "damaged")
    ship_back = cond == "defective"
    cid = "ORD-%d" % rng.randint(1000000, 9999999)
    ntr = 1 + (1 if cond == "damaged" else 0) + (1 if k in (W, W + 1) else 0) + (1 if disc > 0 else 0)
    versions = []
    if big and fee_applies and rng.random() < 0.45:
        ver_r = plan_version(rng, purchased)
        fee_pct_other = D(pick(rng, [x for x in (10, 15, 20, 25) if D(x) != fee_pct]))
        o, n = (fee_pct_other, fee_pct) if ver_r["new"] else (fee_pct, fee_pct_other)
        versions = version_blocks(ver_r, "the restocking fee is %s%% of the pre-tax price paid" % dstr(o),
                                  "the restocking fee is %s%% of the pre-tax price paid" % dstr(n), "order (purchase) date", ds)
        ntr += 1
    base = dict(Lp=Lp, disc=disc, tax=tax, Sh=Sh, fee_pct=fee_pct, fee_min=fee_min, fee_max=fee_max,
                fee_applies=fee_applies, ship_back=ship_back, eligible=eligible)

    def rc(**kw):
        q = dict(base)
        q.update(kw)
        return retail_calc(**q)

    gold = rc()
    check = retail_check(Lp, disc, tax, Sh, fee_pct, fee_min, fee_max, cond, k, W)
    alts, reasons = {}, {}
    if k == W:
        alts["window_off_by_one"] = rc(eligible=False)
    elif k == W + 1:
        alts["window_off_by_one"] = rc(eligible=True)
        reasons["window_off_by_one"] = "still within the return window"
    if (ret - purchased).days > W and eligible:
        alts["window_counted_from_purchase"] = rc(eligible=False)
    if disc > 0:
        alts["used_list_price"] = rc(base_list=True, eligible=True)
    if fee_applies:
        alts["fee_min_max_ignored"] = rc(clamp=False, eligible=True)
        alts["fee_on_tax_inclusive_amount"] = rc(fee_on_taxed=True, eligible=True)
    if cond == "damaged":
        alts["waived_fee_despite_customer_damage"] = rc(fee_applies=False, ship_back=True, eligible=True)
        reasons["waived_fee_despite_customer_damage"] = "it's defective, so no restocking fee"
    if cond == "defective":
        alts["charged_fee_on_defective"] = rc(fee_applies=True, ship_back=False, eligible=True)
    elif cond == "opened":
        alts["refunded_shipping"] = rc(ship_back=True, eligible=True)
    alts["forgot_tax"] = rc(no_tax=True, eligible=True)
    if fee_pct_other is not None:
        alts["wrong_rule_version"] = rc(fee_pct=fee_pct_other)
    rules = [pick(rng, [
        "Returns are accepted if started no later than %d days after the delivery date (the delivery date is day 0)." % W,
        "The return window closes %d days after delivery; a return started on day %d is still accepted, day %d is not." % (W, W, W + 1),
        "A return is not refused unless it is started more than %d days after delivery." % W])]
    rules.append("Outside the window, no refund is made to the original payment method.")
    rules.append(pick(rng, [
        "Refunds are based on the price actually paid (after any discount), plus the sales tax charged on it.",
        "We refund what you paid for the item - net of coupons - together with the sales tax on that amount."]))
    if fee_pct_other is not None:
        rules.append("Opened items carry a restocking fee (percentage per the rule history) of the pre-tax price paid, "
                     "minimum %s, maximum %s. Unopened items have no fee." % (M(fee_min), M(fee_max)))
    else:
        rules.append(pick(rng, [
            "Opened items carry a restocking fee of %s%% of the price paid (before tax), minimum %s, maximum %s. "
            "Unopened items have no fee." % (dstr(fee_pct), M(fee_min), M(fee_max)),
            "Restocking fee for opened items: %s%% of the pre-tax price paid, but never below %s or above %s. No fee on "
            "unopened returns." % (dstr(fee_pct), M(fee_min), M(fee_max))]))
    rules.append(pick(rng, [
        "The restocking fee is waived for defective items, except where the defect was caused by the customer (e.g., a drop "
        "or liquid damage). Original shipping is refunded only for defective items whose fee is waived.",
        "Defective items: no restocking fee and the original shipping charge is refunded - unless the damage was caused by the "
        "customer, in which case the item is treated like any opened return."]))
    cond_txt = {"unopened": "unopened, original seal intact", "opened": "opened; works fine (customer changed mind)",
                "defective": "stops charging after two days (fault confirmed by technician)",
                "damaged": "cracked housing after the customer dropped it; no longer powers on"}[cond]
    facts = [("Order", cid), ("Item", item), ("List price", M(Lp))]
    if disc > 0:
        facts.append(("Coupon applied at checkout", "%s%% off" % dstr(disc)))
    facts += [("Sales tax rate", "%s%%" % dstr(tax)), ("Shipping paid", M(Sh)),
              ("Purchased", fdate(purchased, ds)), ("Delivered", fdate(delivered, ds)),
              ("Return started", fdate(ret, ds)), ("Condition", cond_txt)]
    if big and rng.random() < 0.4:
        facts.append(("Loyalty tier", "%s (free return label)" % pick(rng, ["Gold", "Platinum"])))
        ntr += 1
    if not big:
        rules = ["Return window: %d days after delivery (delivery = day 0; day %d OK); outside it, no refund." % (W, W),
                 "Refund = price paid after coupon + its sales tax.",
                 "Opened: restocking fee %s%% of pre-tax price paid (min %s, max %s). Unopened: no fee."
                 % (dstr(fee_pct), M(fee_min), M(fee_max)),
                 "Defective: no fee, shipping refunded - unless customer-caused."]
        facts = [(a, b) for a, b in facts if a != "Purchased"]
        alts.pop("window_counted_from_purchase", None)
    return mk(cur=cur, domain="retail returns", scen="retail", cid=cid, M=M, fmt=M, versions=versions,
              title=pick(rng, ["Returns & Refunds Policy", "Store Returns Policy (online orders)",
                               "Customer Care Guide - Refund Calculation"]),
              rules=rules, facts=facts, gold=gold, check=check, alts=alts, reasons=reasons, ntr=ntr,
              thing="refund",
              q_choice=pick(rng, ["How much should be refunded to the original payment method for order %s?" % cid,
                                  "What is the correct refund for order %s?" % cid]),
              q_prop=lambda v: "The returns desk wants to refund %s on order %s. Is that the correct amount?" % (v, cid),
              q_thr=lambda c, t: "Is the refund for order %s %s %s?" % (cid, c, t))


# ------------------------------------------------------------------------ 10 public benefits
BEN_BASE = {1: (1632, 292), 2: (2215, 536), 3: (2798, 768), 4: (3380, 975), 5: (3963, 1158), 6: (4546, 1390)}
CONV = {"weekly": D("4.3"), "biweekly": D("2.15"), "semimonthly": D(2)}


def ben_calc(h, pay, freq, u, lim, allot, std, minb, conv=None, skip_gross=False, ded_rate=D(20),
             ded_all=False, contrib_round=ROUND_CEILING, min_rule=True):
    c = (conv or CONV)[freq]
    E = q2(pay * c)
    gross = E + u
    if not skip_gross and gross > lim:
        return D("0.00")
    ded = q2((E + u if ded_all else E) * ded_rate / 100)
    net = max(D(0), gross - ded - std)
    contrib = (net * D("0.3")).to_integral_value(rounding=contrib_round)
    b = allot - contrib
    if min_rule and h <= 2 and b < minb:
        b = minb
    return q2(max(b, D(0)))


def ben_check(h, pay, freq, u, lim, allot, std, minb):
    E = fr_round(F(pay) * F(CONV[freq]))
    gross = E + F(u)
    if gross > F(lim):
        return F(0)
    net = gross - fr_round(E / 5) - F(std)
    net = net if net > 0 else F(0)
    contrib = math.ceil(net * 3 / 10)
    b = F(allot) - contrib
    if h <= 2 and b < F(minb):
        b = F(minb)
    return b if b > 0 else F(0)


def S_benefit(rng, mode, cur=None):
    big = mode != "short"
    cur = ("$", "p")
    M = lambda x: money(x, cur)
    ds = rng.randrange(4)
    fac = D(pick(rng, ["0.96", "1", "1.03", "1.07"]))
    table = {k: (qn(D(a) * fac, 0), qn(D(b) * fac, 0)) for k, (a, b) in BEN_BASE.items()}
    h = rng.randint(1, 6)
    lim, allot = table[h]
    std = D(pick(rng, [198, 204, 209, 215]))
    minb = D(pick(rng, [23, 24]))
    freq = pick(rng, ["weekly", "biweekly", "semimonthly"])
    u = D(pick(rng, [0, 0, rng.randint(50, 600)]))
    tgt = lim * D(rng.randint(55, 112)) / 100 - u
    pay = q2(max(D(50), tgt / CONV[freq]))
    app = rand_date(rng)
    cid = "HNS-%d" % rng.randint(100000, 999999)
    ntr = 1 + (1 if u > 0 else 0)
    versions, alts, reasons = [], {}, {}
    std_other = None
    if big and rng.random() < 0.5:
        v = plan_version(rng, app)
        std_other = std + pick(rng, [D(-11), D(-6), D(6), D(9)])
        o, n = (std_other, std) if v["new"] else (std, std_other)
        versions = version_blocks(v, "the standard deduction is %s" % M(o), "the standard deduction is %s" % M(n),
                                  "application date", ds)
        ntr += 1
    base = dict(h=h, pay=pay, freq=freq, u=u, lim=lim, allot=allot, std=std, minb=minb)

    def bc(**kw):
        q = dict(base)
        q.update(kw)
        return ben_calc(**q)

    gold = bc()
    check = ben_check(h, pay, freq, u, lim, allot, std, minb)
    alts["used_4_weeks_per_month"] = bc(conv={"weekly": D(4), "biweekly": D(2), "semimonthly": D(2)}) if freq != "semimonthly" \
        else bc(conv={"semimonthly": D("2.15")})
    if freq != "semimonthly":
        alts["used_exact_52_over_12"] = bc(conv={"weekly": D(52) / 12, "biweekly": D(26) / 12})
    alts["forgot_earned_income_deduction"] = bc(ded_rate=D(0))
    if u > 0:
        alts["deduction_on_all_income"] = bc(ded_all=True)
    E = q2(pay * CONV[freq])
    if E + u > lim:
        alts["skipped_gross_income_test"] = bc(skip_gross=True)
        reasons["skipped_gross_income_test"] = "net income is low enough"
        ntr += 1
    if std_other is not None:
        alts["wrong_rule_version"] = bc(std=std_other)
    alts["contribution_rounded_down"] = bc(contrib_round=ROUND_DOWN)
    if h <= 2:
        alts["missed_minimum_benefit"] = bc(min_rule=False)
    alts["max_benefit_without_contribution"] = q2(allot) if E + u <= lim else None
    rows = [[str(k), M(table[k][0]), M(table[k][1])] for k in range(1, 7)]
    rt = ("Monthly limits by household size", ["Household size", "Gross monthly income limit", "Maximum monthly benefit"], rows)
    std_txt = "the standard deduction in the schedule history" if std_other is not None else "a standard deduction of %s" % M(std)
    rules = [pick(rng, [
        "Convert pay to a monthly amount: weekly pay x 4.3; biweekly pay x 2.15; semimonthly pay x 2. Round to the cent.",
        "Monthly earned income = weekly pay x 4.3, or biweekly pay x 2.15, or semimonthly pay x 2 (round to the cent)."])]
    rules.append(pick(rng, [
        "Gross test: gross monthly income (earned + unearned, before any deduction) must be at or below the limit for the "
        "household size. A household that fails the gross test receives no benefit.",
        "No benefit is payable unless gross income - before deductions - does not exceed the gross limit in the table."]))
    rules.append("Net income = gross income - 20%% of earned income only (round to the cent) - %s; not below zero." % std_txt)
    rules.append("Benefit = maximum benefit for the household size - 30% of net income, where the 30% figure is rounded "
                 "UP to the next whole dollar.")
    rules.append("Eligible households of 1 or 2 people receive at least %s per month; larger households whose "
                 "calculated benefit is zero or less receive nothing." % M(minb))
    facts = [("Case", cid), ("Application date", fdate(app, ds)), ("Household size", "%d" % h),
             ("Earned income", "%s paid %s" % (M(pay), freq))]
    facts.append(("Unearned income", "%s per month (%s)" % (M(u), pick(rng, ["child support", "pension", "unemployment benefit"])))
                 if u > 0 else ("Unearned income", "none"))
    if big and rng.random() < 0.4:
        facts.append(("Savings", M(D(rng.randint(100, 2500)))))
    if not big:
        cv = {"weekly": "weekly pay x 4.3", "biweekly": "biweekly pay x 2.15", "semimonthly": "semimonthly pay x 2"}[freq]
        rules = ["Household of %d: gross income limit %s; maximum benefit %s." % (h, M(lim), M(allot)),
                 "Monthly earned income = %s (to the cent)." % cv,
                 "If gross income (before deductions) exceeds the limit, no benefit.",
                 "Net = gross - 20%% of earned income - %s standard deduction (not below 0)." % M(std),
                 "Benefit = maximum - 30%% of net, rounded up to a whole dollar%s." % (
                     "; eligible 1-2 person households get at least %s" % M(minb) if h <= 2 else "")]
        rt = None
    return mk(domain="public benefits", scen="benefit", cid=cid, M=M, fmt=M,
              title=pick(rng, ["Household Nutrition Support (HNS) - Benefit Calculation Manual",
                               "County Assistance Program: Eligibility and Allotments", "HNS Caseworker Handbook, Ch. 4"]),
              rules=rules, rule_table=rt, versions=versions, facts=facts, gold=gold, check=check, alts=alts,
              reasons=reasons, ntr=ntr, thing="monthly benefit",
              q_choice=pick(rng, ["What monthly benefit should case %s receive?" % cid,
                                  "Which monthly benefit amount is correct for case %s?" % cid]),
              q_prop=lambda v: "The eligibility worker entered a monthly benefit of %s for case %s. Is that correct?" % (v, cid),
              q_thr=lambda c, t: "Is the monthly benefit for case %s %s %s?" % (cid, c, t))


# ------------------------------------------------------------------------ 11 admissions
def adm_comp(gpa, test, tmax, essay, emax, w, bonus, rmode, cap=True):
    g = min(F(gpa), F(4)) if cap else F(gpa)
    comp = (w[0] * g / 4 * 100 + w[1] * F(test) / tmax * 100 + w[2] * F(essay) / emax * 100) / 100 + F(bonus)
    return fr_round(comp, 1, "down" if rmode == "trunc" else "half_up")


def adm_tier(comp, cuts):
    t = 0
    for i, c in enumerate(cuts):
        if comp >= c:
            t = i + 1
    return t


def adm_check(gpa, test, tmax, essay, emax, w, bonus, rmode, cuts):
    g = min(D(gpa), D(4))
    num = D(w[0]) * g * 25 * tmax * emax + D(w[1]) * D(test) * 100 * emax + D(w[2]) * D(essay) * 100 * tmax
    comp = num / (D(100) * tmax * emax) + D(bonus)
    comp = comp.quantize(D("0.1"), rounding=ROUND_DOWN if rmode == "trunc" else ROUND_HALF_UP)
    for i in (2, 1, 0):
        if comp >= D(cuts[i]):
            return i + 1
    return 0


def S_adm(rng, mode, cur=None):
    big = mode != "short"
    ds = rng.randrange(4)
    names = pick(rng, [("No merit award", "Bronze award ($2,000/yr)", "Silver award ($5,000/yr)", "Gold award ($9,000/yr)"),
                       ("Not eligible", "Tier C scholarship", "Tier B scholarship", "Tier A scholarship"),
                       ("No award", "Dean's award", "Provost's award", "President's award")])
    bands = ["%d: %s" % (i, nm) for i, nm in enumerate(names)]
    target = rng.randrange(4)
    cid = "APP-%d" % rng.randint(100000, 999999)
    best = None
    for attempt in range(80):
        w = pick(rng, [(50, 30, 20), (40, 40, 20), (60, 25, 15), (45, 35, 20)])
        test_kind = pick(rng, ["SAT", "ACT"])
        tmax = 1600 if test_kind == "SAT" else 36
        test = rng.randrange(900, 1601, 10) if test_kind == "SAT" else rng.randint(18, 36)
        emax = pick(rng, [6, 10])
        essay = D(rng.randint(2, emax * 2)) / 2
        gpa = D(rng.randint(260, 460)) / 100
        rmode = pick(rng, ["trunc", "round"])
        cuts = sorted(pick(rng, [(72, 80, 88), (70, 78, 86), (75, 82, 90), (68, 76, 85)]))
        first_gen = big and rng.random() < 0.45
        bridge = first_gen and rng.random() < 0.4
        bpts = D(pick(rng, ["1.0", "1.5", "2.0"]))
        bonus_ok = first_gen and (min(gpa, D(4)) >= D(3) or bridge)
        bonus = bpts if bonus_ok else D(0)
        comp = adm_comp(gpa, test, tmax, essay, emax, w, bonus, rmode)
        tier = adm_tier(comp, cuts)
        if tier != target and attempt < 60:
            continue
        cand = dict(w=w, test_kind=test_kind, tmax=tmax, test=test, emax=emax, essay=essay, gpa=gpa, rmode=rmode,
                    cuts=cuts, first_gen=first_gen, bridge=bridge, bpts=bpts, bonus=bonus, comp=comp, tier=tier)
        flips = adm_comp(gpa, test, tmax, essay, emax, w, bonus, "round" if rmode == "trunc" else "trunc")
        if adm_tier(flips, cuts) != tier or gpa > 4 or attempt > 40:
            best = cand
            break
        if best is None:
            best = cand
    c = best
    use_ver = big and rng.random() < 0.45
    appd = rand_date(rng)
    versions = []
    cuts_other = None
    if use_ver:
        v = plan_version(rng, appd)
        cuts_other = tuple(x + pick(rng, [-2, 2, 3]) for x in c["cuts"])
        o, n = (cuts_other, c["cuts"]) if v["new"] else (c["cuts"], cuts_other)
        ct = lambda cs: "the cut-offs are %s / %s / %s for %s / %s / %s" % (
            dstr(cs[2]), dstr(cs[1]), dstr(cs[0]), names[3], names[2], names[1])
        versions = version_blocks(v, ct(o), ct(n), "application submission date", ds)
    ev = lambda **kw: adm_tier(adm_comp(c["gpa"], c["test"], c["tmax"], c["essay"], c["emax"], kw.get("w", c["w"]),
                                        kw.get("bonus", c["bonus"]), kw.get("rmode", c["rmode"]), kw.get("cap", True)),
                               kw.get("cuts", c["cuts"]))
    gold = ev()
    check = adm_check(c["gpa"], c["test"], c["tmax"], c["essay"], c["emax"], c["w"], c["bonus"], c["rmode"], c["cuts"])
    talts = {"wrong_rounding_mode": ev(rmode="round" if c["rmode"] == "trunc" else "trunc")}
    if c["gpa"] > 4:
        talts["did_not_cap_gpa"] = ev(cap=False)
    if cuts_other:
        talts["wrong_rule_version"] = ev(cuts=cuts_other)
    if c["first_gen"]:
        talts["bonus_misapplied"] = ev(bonus=D(0) if c["bonus"] > 0 else c["bpts"])
    talts["equal_weights"] = ev(w=(F(100, 3), F(100, 3), F(100, 3)))
    ntr = 1 + len(talts) // 2 + (1 if use_ver else 0)
    w = c["w"]
    rules = [pick(rng, [
        "Merit composite = %d%% GPA points + %d%% test points + %d%% essay points." % w,
        "Composite score (0-100) weights: GPA %d%%, test %d%%, essay %d%%." % w])]
    rules.append("GPA points = GPA / 4.00 x 100; a weighted GPA above 4.00 counts as 4.00.")
    rules.append("Test points = %s score / %d x 100. Essay points = essay score / %d x 100." % (c["test_kind"], c["tmax"], c["emax"]))
    if c["first_gen"]:
        rules.append("First-generation applicants receive +%s composite points, but not if their (capped) GPA is below 3.00 "
                     "- unless they completed the Summer Bridge program, in which case the bonus applies regardless of GPA."
                     % dstr(c["bpts"]))
    rules.append("The composite (including any bonus) is %s to one decimal place before it is compared with the cut-offs."
                 % ("truncated (not rounded)" if c["rmode"] == "trunc" else "rounded half up"))
    if not use_ver:
        rules.append("Awards: %s at %s or higher; %s at %s or higher; %s at %s or higher; otherwise %s."
                     % (names[3], dstr(c["cuts"][2]), names[2], dstr(c["cuts"][1]), names[1], dstr(c["cuts"][0]), names[0]))
    else:
        rules.append("Awards are decided with the cut-offs in the rule history (a composite equal to a cut-off qualifies).")
    facts = [("Applicant", cid), ("Application submitted", fdate(appd, ds)), ("Weighted GPA", "%.2f" % c["gpa"]),
             (c["test_kind"] + " score", str(c["test"])), ("Essay score", "%s / %d" % (dstr(c["essay"]), c["emax"]))]
    if c["first_gen"]:
        facts.append(("First-generation student", "yes"))
        facts.append(("Summer Bridge program", "completed" if c["bridge"] else "not completed"))
    if big and rng.random() < 0.4:
        facts.append(("Interview rating", "%d / 5 (optional; not scored)" % rng.randint(2, 5)))
    alts = {k: bands[v] for k, v in talts.items()}

    def qb(b):
        i = bands.index(b)
        return "Does applicant %s qualify for exactly the %s level?" % (cid, names[i]) if i else \
            "Is it correct that applicant %s receives no merit award?" % cid
    if not big:
        rules = ["Composite = %d%% GPA points + %d%% test points + %d%% essay points." % w,
                 "GPA points = min(GPA, 4.00) / 4 x 100; %s points = score / %d x 100; essay points = score / %d x 100."
                 % (c["test_kind"], c["tmax"], c["emax"]),
                 "%s the composite to one decimal." % ("Truncate (do not round)" if c["rmode"] == "trunc" else "Round half up"),
                 "%s: %s+; %s: %s+; %s: %s+; otherwise %s." % (names[3], dstr(c["cuts"][2]), names[2], dstr(c["cuts"][1]),
                                                            names[1], dstr(c["cuts"][0]), names[0])]
    return mk(domain="education/admissions", scen="adm", cid=cid, M=lambda x: money(x, ("$", "p")), kind="band",
              bands=bands, title=pick(rng, ["Merit Scholarship Rules - First-Year Admissions",
                                           "Admissions Office: Merit Award Composite", "Scholarship Committee Guidelines"]),
              rules=rules, versions=versions, facts=facts, gold=bands[gold], check=bands[check], alts=alts, ntr=ntr,
              thing="award level",
              q_choice=pick(rng, ["Which merit award level should applicant %s receive?" % cid,
                                  "What award does applicant %s qualify for?" % cid]),
              q_band=qb)


# ------------------------------------------------------------------------ 12 telecom overage
def tel_calc(used, zero, allow, conv, step, t1, r1, r2, cap, round_up=True, flat=False):
    over = D(used) - D(zero) - D(allow) * conv
    if over <= 0:
        return D("0.00")
    gb = over / conv
    units = (gb / step).to_integral_value(rounding=ROUND_CEILING) * step if round_up else gb
    if flat and units > t1:
        ch = units * r2
    else:
        ch = min(units, t1) * r1 + max(units - t1, D(0)) * r2
    if cap is not None:
        ch = min(ch, cap)
    return q2(ch)


def tel_check(used, zero, allow, conv, step, t1, r1, r2, cap):
    over = F(used) - F(zero) - F(allow) * F(conv)
    if over <= 0:
        return F(0)
    nsteps = math.ceil(over / (F(conv) * F(step)))
    ch = F(0)
    for i in range(nsteps):
        start = F(step) * i
        ch += F(step) * (F(r1) if start < F(t1) else F(r2))
    if cap is not None and ch > F(cap):
        ch = F(cap)
    return fr_round(ch)


def S_tel(rng, mode, cur=None):
    big = mode != "short"
    cur = cur or pick(rng, CURS)
    M = lambda x: money(x, cur)
    allow = pick(rng, [10, 15, 20, 30, 50])
    conv = D(pick(rng, [1024, 1000]))
    step = D(pick(rng, ["1", "1", "0.5"]))
    t1 = D(pick(rng, [5, 10]))
    r1 = D(pick(rng, ["2.00", "2.50", "3.00", "4.00"]))
    r2 = r1 + D(pick(rng, ["1.00", "1.50", "2.00"]))
    over_mb = rng.randint(300, int(22 * conv))
    zero = rng.randint(200, 4000) if (big or rng.random() < 0.4) else 0
    used = int(allow * conv) + over_mb + zero
    cap = None
    if rng.random() < 0.4:
        raw = tel_calc(used, zero, allow, conv, step, t1, r1, r2, None)
        cap = D(pick(rng, [30, 40, 50, 60])) if rng.random() < 0.5 else max(D(10), qn(raw * D("0.8"), 0))
    cid = "MSISDN-...%04d" % rng.randint(0, 9999)
    svc0 = pick(rng, ["video pass", "music pass", "Unlimited Weekend add-on"])
    ntr = 1 + (1 if zero else 0) + (1 if cap is not None else 0)
    base = dict(used=used, zero=zero, allow=allow, conv=conv, step=step, t1=t1, r1=r1, r2=r2, cap=cap)

    def tc(**kw):
        q = dict(base)
        q.update(kw)
        return tel_calc(**q)

    gold = tc()
    check = tel_check(used, zero, allow, conv, step, t1, r1, r2, cap)
    alts = {"wrong_mb_per_gb": tc(conv=D(1000) if conv == 1024 else D(1024)),
            "charged_fractional_gb": tc(round_up=False),
            "top_rate_on_all_overage": tc(flat=True)}
    if cap is not None:
        alts["ignored_monthly_cap"] = tc(cap=None)
    if zero:
        alts["counted_zero_rated_usage"] = tc(zero=0)
    alts["ignored_allowance"] = tc(allow=0)
    rules = ["The plan includes %d GB of data per billing cycle. For billing, 1 GB = %s MB." % (allow, "{:,}".format(int(conv)))]
    if zero:
        rules.append(pick(rng, ["Usage on zero-rated services (%s) does not count toward the allowance or toward overage." % svc0,
                                "Zero-rated traffic (%s) is excluded before the allowance is applied." % svc0]))
    stxt = "per started GB" if step == 1 else "in started 0.5 GB blocks"
    rules.append(pick(rng, [
        "Overage is billed %s: the first %s GB of overage at %s per GB, any further overage at %s per GB." % (stxt, dstr(t1), M(r1), M(r2)),
        "Data beyond the allowance is charged %s. Tier 1 (first %s GB over): %s/GB. Tier 2 (everything above that): %s/GB."
        % (stxt, dstr(t1), M(r1), M(r2))]))
    if cap is not None:
        rules.append("Bill-shock protection: overage charges in one cycle never exceed %s." % M(cap))
    facts = [("Line", cid), ("Billing cycle", "%s" % pick(rng, ["3 Mar - 2 Apr", "15 Jun - 14 Jul", "1-30 Sep", "20 Oct - 19 Nov"])),
             ("Total data used (network record)", "{:,} MB".format(used))]
    if zero:
        facts.append(("Of which zero-rated (%s)" % svc0, "{:,} MB".format(zero)))
    return mk(cur=cur, domain="telecom billing", scen="tel", cid=cid, M=M, fmt=M,
              title=pick(rng, ["Mobile Plan Terms - Data Allowance and Overage", "Tariff Sheet: Data Overage Charges",
                               "Billing FAQ - How Data Overage Is Charged"]),
              rules=rules, facts=facts, gold=gold, check=check, alts=alts, ntr=ntr, thing="overage charge",
              reasons={"top_rate_on_all_overage": "they went into tier 2, so tier-2 price"},
              q_choice=pick(rng, ["What data overage charge applies to line %s this cycle?" % cid,
                                  "How much overage should line %s be billed?" % cid]),
              q_prop=lambda v: "The draft bill shows an overage charge of %s for line %s. Is that correct?" % (v, cid),
              q_thr=lambda c, t: "Is the overage charge for line %s %s %s?" % (cid, c, t))


# ------------------------------------------------------------------------ 13 breach notification
def tzl(off):
    if off == 0:
        return "UTC"
    return "UTC%s%02d:00" % ("+" if off > 0 else "-", abs(off))


def breach_band(aware, sub, H, incl):
    diff = int((sub - (aware + TD(hours=H))).total_seconds() // 60)
    if diff < 0 or (diff == 0 and incl):
        return 0
    return 1 if diff < 1440 else 2


def breach_check(aware, sub, H, incl):
    ep = DTM(1970, 1, 1)
    a = (aware - ep).days * 1440 + (aware - ep).seconds // 60
    s = (sub - ep).days * 1440 + (sub - ep).seconds // 60
    late = s - a - H * 60
    if late > 0 or (late == 0 and not incl):
        return 2 if late >= 24 * 60 else 1
    return 0


def S_breach(rng, mode, cur=None):
    big = mode != "short"
    ds = rng.randrange(4)
    H = pick(rng, [72, 72, 72, 48, 24])
    incl = rng.random() < 0.65
    tza = pick(rng, [-7, -5, -4, 0, 1, 2, 3, 8, 9])
    tzn = pick(rng, [z for z in (-5, -4, 0, 1, 2, 9) if z != tza])
    aware = DTM.combine(rand_date(rng), datetime.time(rng.randint(0, 23), pick(rng, [0, 5, 10, 15, 20, 30, 40, 45, 50, 55])))
    alert = aware - TD(hours=rng.randint(3, 40), minutes=rng.randint(0, 59))
    deadline = aware + TD(hours=H)
    target = rng.randrange(3)
    if target == 0:
        delta = -pick(rng, [0, 0, rng.randint(1, 90), rng.randint(91, 1800)])
    elif target == 1:
        delta = pick(rng, [1, rng.randint(2, 180), rng.randint(181, 1439)])
    else:
        delta = pick(rng, [1440, rng.randint(1441, 4000)])
    eff = deadline + TD(minutes=delta)
    initial, complete = None, None
    final = eff
    if big and rng.random() < 0.4:
        complete = rng.random() < 0.5
        if complete:
            initial = eff
            final = eff + TD(hours=rng.randint(20, 150))
        else:
            initial = min(eff, deadline) - TD(hours=rng.randint(2, 30))
    cid = "INC-%d-%03d" % (aware.year, rng.randint(1, 999))
    org = pick(rng, ["Brightwater Health Clinics", "Norland Credit Union", "Vela Retail Group", "Orchid Telecom"])
    sub = initial if complete else final
    gold = breach_band(aware, sub, H, incl)
    check = breach_check(aware, sub, H, incl)
    talts = {}
    talts["ignored_time_zones"] = breach_band(aware + TD(hours=tza), sub + TD(hours=tzn), H, incl)
    if tza != 0:
        talts["time_zone_sign_error"] = breach_band(aware + TD(hours=2 * tza), sub, H, incl)
    talts["clock_from_first_alert"] = breach_band(alert, sub, H, incl)
    if initial is not None:
        if complete:
            talts["ignored_valid_initial_notice"] = breach_band(aware, final, H, incl)
        else:
            talts["used_incomplete_initial_notice"] = breach_band(aware, initial, H, incl)
    talts["boundary_inclusivity"] = breach_band(aware, sub, H, not incl)
    ntr = 2 + (1 if initial is not None else 0) + (1 if delta in (0, 1, 1440) else 0)
    names = pick(rng, [("On time", "Late by less than 24 hours", "Late by 24 hours or more"),
                       ("Timely", "Late (under 24 h)", "Late (24 h or more)")])
    bands = list(names)
    st = rng.randrange(4)
    show = lambda t, off: "%s (%s)" % (fdt(t + TD(hours=off), st), tzl(off))
    rules = [pick(rng, [
        "The controller must notify the supervisory authority no later than %d hours after becoming aware of the breach%s."
        % (H, " (a notification at exactly %d:00 hours is still on time)" % H if incl else ""),
        "A notification is not late unless it is submitted more than %d hours after the controller became aware." % H
        if incl else "Notification must reach the authority before %d hours have elapsed since awareness; a submission at "
                     "exactly %d hours is late." % (H, H)])]
    rules.append(pick(rng, [
        "The controller 'becomes aware' when the security lead confirms that personal data was affected - not when the first "
        "automated alert fires.",
        "The clock starts at confirmation by the security lead that personal data is involved; earlier alerts do not start it."]))
    if initial is not None:
        rules.append("Notification may be made in phases. An initial notification counts toward the deadline only if it "
                     "states the categories of data and the approximate number of people affected; otherwise the deadline is "
                     "judged by the first notification that does.")
    rules.append("For the compliance report, classify each notification as: %s; %s; %s." % names)
    if rng.random() < 0.5:
        rules.append("Timestamps from different systems are recorded in local time with their UTC offset; compare them on a "
                     "single time base.")
    facts = [("Incident", "%s (%s)" % (cid, org)), ("First automated alert", show(alert, tza)),
             ("Confirmed by security lead", show(aware, tza))]
    if initial is not None:
        facts.append(("Initial notification submitted", show(initial, tzn) + (
            " - listed data categories and ~%s affected people" % "{:,}".format(rng.randint(200, 90000)) if complete
            else " - stated only that an incident was under investigation")))
        facts.append(("Full notification submitted", show(final, tzn)))
    else:
        facts.append(("Notification submitted to authority", show(final, tzn)))
    alts = {k: bands[v] for k, v in talts.items()}

    def qb(b):
        i = bands.index(b)
        return [pick(rng, ["Was the notification for %s made on time?" % cid, "Did %s meet the notification deadline?" % cid]),
                "Was the notification for %s late, but by less than 24 hours?" % cid,
                "Was the notification for %s late by 24 hours or more?" % cid][i]
    if not big:
        rules = [("Notify the authority no later than %d h after awareness (exactly %d:00 h is on time)." % (H, H)) if incl else
                 ("Notify the authority before %d h have passed since awareness (exactly %d:00 h is late)." % (H, H)),
                 "Awareness = confirmation by the security lead, not the first alert.",
                 "Classify as: %s / %s / %s." % names]
    return mk(domain="compliance/privacy", scen="breach", cid=cid, M=lambda x: money(x, ("€", "p")), kind="band",
              bands=bands, title=pick(rng, ["Personal Data Breach Procedure", "Privacy Incident Response Standard",
                                           "DPO Handbook - Notification Deadlines"]),
              rules=rules, facts=facts, gold=bands[gold], check=bands[check], alts=alts, ntr=ntr,
              reasons={"clock_from_first_alert": "clock started with the first alert"},
              thing="timeliness classification",
              q_choice=pick(rng, ["How should the notification for %s be classified?" % cid,
                                  "Which timeliness category applies to the authority notification for %s?" % cid]),
              q_band=qb)


# ------------------------------------------------------------------------ 14 FX wire
FX_PAIRS = [("USD", "EUR", (9000, 9500)), ("USD", "GBP", (7600, 8200)), ("GBP", "EUR", (11400, 12000)),
            ("EUR", "USD", (10500, 11200)), ("CAD", "USD", (7200, 7500)), ("AUD", "USD", (6400, 6800)),
            ("USD", "CHF", (8600, 9100))]


def fx_calc(S, fee, fee_mode, r, quote, margin, rmode, inter, charges, dir_err=False, margin_sign=1,
            no_margin=False, fee_err=False, inter_err=False, unrounded=False):
    amt = S - fee if (fee_mode == "deducted") != fee_err else S
    mul = (quote == "mult") != dir_err
    m = D(0) if no_margin else margin * margin_sign / 100
    if quote == "mult":
        cust = r * (1 - m)
    else:
        cust = r * (1 + m)
    if not unrounded:
        cust = qn(cust, 4)
    conv = amt * cust if mul else amt / cust
    conv = conv.quantize(C2, rounding=ROUND_DOWN if rmode == "down" else ROUND_HALF_UP)
    ded = inter if ((charges == "SHA") != inter_err) else D(0)
    return q2(max(D(0), conv - ded))


def fx_check(S, fee, fee_mode, r, quote, margin, rmode, inter, charges):
    amt = F(S) - (F(fee) if fee_mode == "deducted" else 0)
    if quote == "mult":
        cust = fr_round(F(r) * (1 - F(margin) / 100), 4)
        conv = amt * cust
    else:
        cust = fr_round(F(r) * (1 + F(margin) / 100), 4)
        conv = amt / cust
    conv = fr_round(conv, 2, "down" if rmode == "down" else "half_up")
    return conv - (F(inter) if charges == "SHA" else 0)


def S_fx(rng, mode, cur=None):
    big = mode != "short"
    src, dst, (lo, hi) = pick(rng, FX_PAIRS)
    sym = {"USD": ("$", "p"), "EUR": ("€", "p"), "GBP": ("£", "p"), "CHF": (" CHF", "s"),
           "CAD": ("CAD ", "p"), "AUD": ("AUD ", "p")}
    Ms = lambda x: money(x, sym[src])
    Md = lambda x: money(x, sym[dst])
    mid = D(rng.randint(lo, hi)) / 10000
    quote = pick(rng, ["mult", "div"])
    r = mid if quote == "mult" else qn(1 / mid, 4)
    S = D(rng.randint(500, 50000)) + D(pick(rng, [0, 0, 50, 75])) / 100
    fee = D(pick(rng, [15, 25, 30, 35, 45]))
    fee_mode = pick(rng, ["deducted", "separate"])
    margin = D(pick(rng, ["0.5", "0.75", "1", "1.5", "2", "2.5"]))
    rmode = pick(rng, ["down", "half_up"])
    charges = pick(rng, ["SHA", "OUR"]) if big or rng.random() < 0.5 else "OUR"
    inter = D(pick(rng, [10, 12, 15, 20, 25]))
    cid = "PMT-%d" % rng.randint(10000000, 99999999)
    exec_d = rand_date(rng)
    ds = rng.randrange(4)
    versions, margin_other = [], None
    if big and rng.random() < 0.4:
        vf = plan_version(rng, exec_d)
        margin_other = D(pick(rng, [x for x in ("0.5", "0.75", "1", "1.5", "2", "2.5") if D(x) != margin]))
        o, n = (margin_other, margin) if vf["new"] else (margin, margin_other)
        versions = version_blocks(vf, "the FX margin is %s%%" % dstr(o), "the FX margin is %s%%" % dstr(n), "execution date", ds)
    base = dict(S=S, fee=fee, fee_mode=fee_mode, r=r, quote=quote, margin=margin, rmode=rmode, inter=inter, charges=charges)

    def fc(**kw):
        q = dict(base)
        q.update(kw)
        return fx_calc(**q)

    gold = fc()
    check = fx_check(S, fee, fee_mode, r, quote, margin, rmode, inter, charges)
    alts = {"wrong_rate_direction": fc(dir_err=True), "margin_wrong_direction": fc(margin_sign=-1),
            "ignored_margin": fc(no_margin=True), "sender_fee_mishandled": fc(fee_err=True),
            "unrounded_customer_rate": fc(unrounded=True)}
    if big or charges == "SHA":
        alts["intermediary_fee_misapplied"] = fc(inter_err=True)
    if margin_other is not None:
        alts["wrong_rule_version"] = fc(margin=margin_other)
    ntr = 2 + (1 if charges == "SHA" else 0) + (1 if margin_other is not None else 0)
    qtxt = "1 %s = %s %s" % (src, dstr(r), dst) if quote == "mult" else "1 %s = %s %s" % (dst, dstr(r), src)
    mg = "the margin in the rule history" if margin_other is not None else "%s%%" % dstr(margin)
    rules = [pick(rng, [
        "Conversions use the day's mid-market quote adjusted by %s in the bank's favour (so the customer always "
        "receives less than at mid-market). Round the customer rate to 4 decimal places." % (
            "the margin shown in the rule history" if margin_other is not None else "a %s%% margin" % dstr(margin)),
        "The customer rate is the mid rate worsened by %s for the customer, rounded to four decimals." % mg])]
    rules.append("The sending fee of %s is %s." % (Ms(fee), "deducted from the amount before conversion" if fee_mode == "deducted"
                                                    else "charged separately to the sender's account and does not reduce the amount converted"))
    rules.append("Converted amounts are %s." % ("rounded down to the cent" if rmode == "down" else "rounded to the nearest cent (half up)"))
    rules.append(pick(rng, [
        "Charge option SHA: the correspondent bank deducts its fee (%s) from the amount received. Charge option OUR: the "
        "sender pays all fees and the beneficiary receives the full converted amount." % Md(inter),
        "Under OUR, no fee is deducted on the beneficiary side; under SHA, the intermediary fee of %s is taken from the "
        "converted amount." % Md(inter)]))
    facts = [("Payment", cid), ("Executed", fdate(exec_d, ds)), ("Amount instructed", Ms(S)), ("Beneficiary currency", dst),
             ("Mid-market quote at execution", qtxt), ("Charge option", charges)]
    if big and rng.random() < 0.4:
        facts.append(("Purpose", pick(rng, ["supplier invoice INV-%d" % rng.randint(1000, 9999), "tuition fees", "property deposit"])))
    if not big:
        rules = ["Customer rate = mid rate made %s%% worse for the customer, rounded to 4 decimals." % dstr(margin),
                 "Sending fee %s: %s." % (Ms(fee), "deducted before conversion" if fee_mode == "deducted" else "charged separately, not deducted"),
                 "Round the converted amount %s." % ("down to the cent" if rmode == "down" else "half up to the cent"),
                 ("SHA: the correspondent bank deducts %s from the amount received." % Md(inter)) if charges == "SHA" else
                 "OUR: the sender pays all fees; nothing is deducted on arrival."]
    return mk(domain="banking/payments", scen="fx", cid=cid, M=Md, fmt=Md, versions=versions,
              title=pick(rng, ["International Payments - Tariff and FX Rules", "Wire Transfer Terms (Cross-Border)",
                               "Treasury Ops: Outbound FX Payments"]),
              rules=rules, facts=facts, gold=gold, check=check, alts=alts, ntr=ntr, thing="amount received",
              reasons={"wrong_rate_direction": "just multiplied by the quote"},
              q_choice=pick(rng, ["How much will the beneficiary receive for payment %s (in %s)?" % (cid, dst),
                                  "What amount in %s arrives in the beneficiary account for %s?" % (dst, cid)]),
              q_prop=lambda v: "The payment confirmation says the beneficiary will receive %s for %s. Is that correct?" % (v, cid),
              q_thr=lambda c, t: "Will the beneficiary of %s receive %s %s?" % (cid, c, t))


# ------------------------------------------------------------------------ 15 healthcare billing
def health_calc(Ap, Dr, c, O, copay_part, coins_full=False):
    d = min(Ap, Dr)
    pt = d + (Ap if coins_full else (Ap - d)) * c / 100 + copay_part
    if O is not None:
        pt = min(pt, O)
    return q2(pt)


def health_check(Ap, Dr, c, O, copay, Av):
    ledger = F(0)
    remaining_ded = F(Dr)
    ded_part = F(Ap) if F(Ap) < remaining_ded else remaining_ded
    ledger += ded_part + (F(Ap) - ded_part) * F(c) / 100
    if Av is not None:
        ledger += F(copay) if F(copay) < F(Av) else F(Av)
    if ledger > F(O):
        ledger = F(O)
    return fr_round(ledger)


def S_health(rng, mode, cur=None):
    big = mode != "short"
    cur = cur or pick(rng, [("$", "p"), ("USD ", "p")])
    M = lambda x: money(x, cur)
    ds = rng.randrange(4)
    svc = pick(rng, ["Outpatient MRI, lumbar spine", "Colonoscopy with biopsy", "Knee arthroscopy (outpatient)",
                     "CT scan, abdomen", "Sleep study (in-lab)", "Physical therapy evaluation"])
    Ap = D(rng.randint(180, 4800)) + D(pick(rng, [0, 50, 37, 12])) / 100
    Bp = q2(Ap * D(rng.randint(140, 320)) / 100)
    Dann = D(pick(rng, [1000, 1500, 2000, 3000]))
    Dr = D(pick(rng, [0, rng.randint(1, int(Dann) - 1), Dann]))
    c = D(pick(rng, [10, 20, 25, 30]))
    OOPmax = D(pick(rng, [4000, 5500, 6500, 8000]))
    O = D(rng.randint(100, int(OOPmax)))
    visit = big and rng.random() < 0.4
    copay = D(pick(rng, [25, 35, 45, 60]))
    Av = D(rng.randint(90, 260)) if visit else None
    copay_part = min(copay, Av) if visit else D(0)
    dos = rand_date(rng)
    processed = dos + TD(days=rng.randint(5, 45))
    cid = "CLM-%d" % rng.randint(1000000, 9999999)
    versions, alts = [], {}
    c_other = None
    ntr = 1 + (1 if Dr < Dann else 0)
    if big and rng.random() < 0.45:
        v = plan_version(rng, dos)
        c_other = pick(rng, [x for x in (D(10), D(20), D(25), D(30)) if x != c])
        o, n = (c_other, c) if v["new"] else (c, c_other)
        versions = version_blocks(v, "coinsurance is %s%%" % dstr(o), "coinsurance is %s%%" % dstr(n), "date of service", ds)
        ntr += 1
    gold = health_calc(Ap, Dr, c, O, copay_part)
    check = health_check(Ap, Dr, c, O, copay, Av)
    alts["used_billed_charge"] = health_calc(Bp, Dr, c, O, copay_part)
    alts["used_annual_deductible"] = health_calc(Ap, Dann, c, O, copay_part)
    alts["ignored_oop_max"] = health_calc(Ap, Dr, c, None, copay_part)
    alts["coinsurance_on_full_allowed"] = health_calc(Ap, Dr, c, O, copay_part, coins_full=True)
    alts["reported_plan_share"] = q2(Ap + (Av or 0) - gold)
    if visit:
        alts["deductible_applied_to_visit"] = health_calc(Ap + Av, Dr, c, O, D(0))
    if c_other is not None:
        alts["wrong_rule_version"] = health_calc(Ap, Dr, c_other, O, copay_part)
    if (Dr + (Ap - min(Ap, Dr)) * c / 100 + copay_part) > O:
        ntr += 1
    ctxt = "the coinsurance percentage in the plan-year schedule" if c_other is not None else "%s%% coinsurance" % dstr(c)
    rules = [pick(rng, ["Cost sharing is always based on the plan's allowed amount, never on the provider's billed charge.",
                        "Patients pay a share of the allowed (contracted) amount; amounts billed above it are written off."])]
    rules.append("For procedures, the patient first pays any deductible still remaining this year, then %s on the rest of "
                 "the allowed amount." % ctxt)
    if visit:
        rules.append("Office visits have a %s copay; the deductible and coinsurance do not apply to the visit line itself "
                     "(the copay cannot exceed the visit's allowed amount)." % M(copay))
    rules.append(pick(rng, [
        "Once out-of-pocket spending reaches the annual maximum, the patient pays nothing more; the patient's share of a claim "
        "cannot exceed the out-of-pocket amount still remaining.",
        "The patient's share is capped at whatever is left of the annual out-of-pocket maximum."]))
    facts = [("Claim", cid), ("Date of service", fdate(dos, ds)), ("Processed", fdate(processed, ds)),
             ("Provider", "in-network"), ("Service", svc), ("Billed charge", M(Bp)), ("Allowed amount", M(Ap)),
             ("Annual deductible", M(Dann)), ("Deductible met so far this year", M(Dann - Dr)),
             ("Annual out-of-pocket maximum", M(OOPmax)), ("Out-of-pocket spent so far this year", M(OOPmax - O))]
    if visit:
        facts.insert(7, ("Office visit line (same day)", "allowed %s" % M(Av)))
    if not big:
        rules = ["Cost sharing uses the allowed amount, never the billed charge.",
                 "The patient pays any remaining deductible first, then %s%% coinsurance on the rest of the allowed amount." % dstr(c),
                 "The patient's share cannot exceed what is left of the out-of-pocket maximum."]
        facts = [("Claim", cid), ("Service", svc + " (in-network)"), ("Billed", M(Bp)), ("Allowed", M(Ap)),
                 ("Deductible", "%s per year, %s met so far" % (M(Dann), M(Dann - Dr))),
                 ("Out-of-pocket max", "%s per year, %s spent so far" % (M(OOPmax), M(OOPmax - O)))]
    return mk(cur=cur, domain="healthcare billing", scen="health", cid=cid, M=M, fmt=M,
              title=pick(rng, ["Summary of Benefits - Cost Sharing", "Explanation of Benefits: How Your Share Is Calculated",
                               "Plan Document - Member Cost Sharing"]),
              rules=rules, versions=versions, facts=facts, gold=gold, check=check, alts=alts, ntr=ntr,
              reasons={"used_billed_charge": "worked off the bill"},
              thing="patient responsibility",
              q_choice=pick(rng, ["What is the patient's responsibility for claim %s?" % cid,
                                  "How much does the member owe for claim %s?" % cid]),
              q_prop=lambda v: "The billing office plans to charge the patient %s for claim %s. Is that correct?" % (v, cid),
              q_thr=lambda c_, t: "Is the patient's share of claim %s %s %s?" % (cid, c_, t))


# ------------------------------------------------------------------------ 16 utility bill
def util_calc(kwh, days, b1, b2, r1, r2, r3, fixed_kind, fixed_val, prorate=True, flat=False):
    if prorate:
        t1, t2 = qn(D(b1) * days / 30, 0), qn(D(b2) * days / 30, 0)
    else:
        t1, t2 = D(b1), D(b2)
    if flat:
        rate = r1 if kwh <= t1 else (r2 if kwh <= t1 + t2 else r3)
        cents = kwh * rate
    else:
        e1 = min(kwh, t1)
        e2 = min(max(kwh - t1, D(0)), t2)
        e3 = max(kwh - t1 - t2, D(0))
        cents = e1 * r1 + e2 * r2 + e3 * r3
    energy = q2(cents / 100)
    fixed = q2(fixed_val * days) if fixed_kind == "daily" else fixed_val
    return q2(energy + fixed)


def util_check(prev, curr, mult, d0, d1, b1, b2, r1, r2, r3, fixed_kind, fixed_val):
    kwh = (curr - prev) * mult
    days = 0
    d = d0
    while d < d1:
        days += 1
        d += TD(days=1)
    t1 = fr_round(F(b1) * days / 30, 0)
    t2 = fr_round(F(b2) * days / 30, 0)
    cents = F(0)
    for lo, hi, r in ((0, t1, r1), (t1, t1 + t2, r2), (t1 + t2, None, r3)):
        seg = (min(F(kwh), hi) if hi is not None else F(kwh)) - lo
        if seg > 0:
            cents += seg * F(r)
    fixed = fr_round(F(fixed_val) * days) if fixed_kind == "daily" else F(fixed_val)
    return fr_round(fr_round(cents / 100) + fixed)


def S_util(rng, mode, cur=None):
    big = mode != "short"
    cur = cur or pick(rng, [("$", "p"), ("CAD $", "p"), ("AUD ", "p")])
    M = lambda x: money(x, cur)
    ds = rng.randrange(4)
    d0 = rand_date(rng)
    days = rng.randint(27, 34)
    d1 = d0 + TD(days=days)
    mult = pick(rng, [1, 1, 10, 20]) if big else pick(rng, [1, 10])
    b1, b2 = pick(rng, [(350, 400), (500, 500), (600, 400), (400, 600)])
    r1 = D(rng.randint(900, 1400)) / 100
    r2 = r1 + D(rng.randint(150, 400)) / 100
    r3 = r2 + D(rng.randint(150, 500)) / 100
    kwh_target = rng.randint(int(b1 * 0.6), int((b1 + b2) * 1.5)) if rng.random() < 0.15 else \
        rng.randint(int(b1 * 1.08), int((b1 + b2) * 1.6))
    diff = max(1, kwh_target // mult)
    prev = rng.randint(1000, 90000)
    curr = prev + diff
    kwh = D(diff * mult)
    fixed_kind = pick(rng, ["daily", "daily", "monthly"])
    fixed_val = D(pick(rng, ["0.39", "0.45", "0.52", "0.61"])) if fixed_kind == "daily" else D(pick(rng, ["11.50", "14.00", "18.75"]))
    cid = "ACCT-%d" % rng.randint(1000000, 9999999)
    ntr = 1 + (1 if mult > 1 else 0)
    versions, fixed_other = [], None
    if big and rng.random() < 0.4:
        vu = plan_version(rng, d1)
        fixed_other = fixed_val + (D(pick(rng, ["-0.06", "-0.04", "0.03", "0.05"])) if fixed_kind == "daily"
                                   else D(pick(rng, ["-2.00", "-1.25", "1.50", "2.25"])))
        o, n = (fixed_other, fixed_val) if vu["new"] else (fixed_val, fixed_other)
        ft_ = (lambda x: "the fixed charge is %s per billing day" % M(x)) if fixed_kind == "daily" else \
            (lambda x: "the fixed charge is %s per bill" % M(x))
        versions = version_blocks(vu, ft_(o), ft_(n), "current meter-reading date", ds)
        ntr += 1
    base = dict(kwh=kwh, days=days, b1=b1, b2=b2, r1=r1, r2=r2, r3=r3, fixed_kind=fixed_kind, fixed_val=fixed_val)

    def uc(**kw):
        q = dict(base)
        q.update(kw)
        return util_calc(**q)

    gold = uc()
    check = util_check(prev, curr, mult, d0, d1, b1, b2, r1, r2, r3, fixed_kind, fixed_val)
    alts = {"no_tier_proration": uc(prorate=False), "top_rate_on_all_kwh": uc(flat=True),
            "inclusive_day_count": uc(days=days + 1)}
    if mult > 1:
        alts["forgot_meter_multiplier"] = uc(kwh=D(diff))
    alts["forgot_fixed_charge"] = q2(gold - (q2(fixed_val * days) if fixed_kind == "daily" else fixed_val))
    if fixed_other is not None:
        alts["wrong_rule_version"] = uc(fixed_val=fixed_other)
    alts["all_kwh_at_first_rate"] = uc(r2=r1, r3=r1)
    rules = [pick(rng, ["Consumption (kWh) = (current reading - previous reading) x meter multiplier.",
                        "Multiply the register difference by the meter multiplier to get kWh."])]
    rules.append(pick(rng, ["Billing days = days from the previous reading date to the current reading date (do not count both ends).",
                            "The number of billing days is the difference between the two reading dates."]))
    rules.append("Tier sizes are stated for a 30-day period and are prorated to the billing days, rounded to the nearest "
                 "whole kWh.")
    rules.append("Energy rates (per 30 days): first %d kWh at %s cents/kWh; next %d kWh at %s cents/kWh; all further kWh at "
                 "%s cents/kWh. Round the energy charge to the cent." % (b1, dstr(r1), b2, dstr(r2), dstr(r3)))
    if fixed_other is not None:
        rules.append("Fixed charge: as per the tariff history (the reading date of the current reading decides).")
    else:
        rules.append("Fixed charge: %s." % ("%s per billing day" % M(fixed_val) if fixed_kind == "daily" else "%s per bill" % M(fixed_val)))
    facts = [("Account", cid), ("Previous reading", "{:,} on {}".format(prev, fdate(d0, ds))),
             ("Current reading", "{:,} on {}".format(curr, fdate(d1, ds))), ("Meter multiplier", "x%d" % mult)]
    if big and rng.random() < 0.4:
        facts.append(("Same period last year", "%d kWh" % rng.randint(300, 1500)))
    if not big:
        rules = ["kWh = (current - previous reading) x meter multiplier; billing days = days between the two reading dates.",
                 "Tier sizes are per 30 days, prorated to the billing days (whole kWh): first %d kWh at %s c/kWh, next %d at %s c/kWh, rest at %s c/kWh."
                 % (b1, dstr(r1), b2, dstr(r2), dstr(r3)),
                 "Round the energy charge to the cent. Fixed charge: %s." % (
                     "%s per billing day" % M(fixed_val) if fixed_kind == "daily" else "%s per bill" % M(fixed_val))]
    return mk(cur=cur, domain="utilities", scen="util", cid=cid, M=M, fmt=M, versions=versions,
              title=pick(rng, ["Residential Electricity Tariff R-1", "Understanding Your Electricity Bill",
                               "Tariff Schedule - Tiered Residential Rates"]),
              rules=rules, facts=facts, gold=gold, check=check, alts=alts, ntr=ntr, thing="bill total",
              q_choice=pick(rng, ["What is the total electricity bill for account %s for this period?" % cid,
                                  "How much should account %s be billed for this period?" % cid]),
              q_prop=lambda v: "The bill for account %s shows %s. Is that the correct total?" % (cid, v),
              q_thr=lambda c, t: "Is the bill for account %s %s %s?" % (cid, c, t))


SCENARIOS = [("insurance", S_insurance), ("travel", S_travel), ("saas", S_saas), ("sla", S_sla), ("loan", S_loan),
             ("ship", S_ship), ("qa", S_qa), ("hr", S_hr), ("retail", S_retail), ("benefit", S_benefit),
             ("adm", S_adm), ("tel", S_tel), ("breach", S_breach), ("fx", S_fx), ("health", S_health),
             ("util", S_util)]
SCEN_FN = dict(SCENARIOS)


# =========================================================================== NOISE
GENERIC_NOISE = [
    ("Confidentiality", "This document and any attachments are intended solely for the named recipients and may contain "
                        "confidential information. If you received it in error, notify the sender and delete all copies. "
                        "Unauthorised use, disclosure or copying is prohibited."),
    ("Record retention", "Case records are retained for {n1} years after closure and then securely destroyed, unless a legal "
                         "hold applies. Scanned paper originals may be discarded after {n2} days."),
    ("Accessibility", "Large-print, Braille and audio versions of this document are available on request at no charge. "
                      "Ask your case handler or call the service line."),
    ("Complaints", "If you are unhappy with how your matter was handled you may complain within {n1} weeks. We acknowledge "
                   "complaints within {n2} business days and aim to send a final response within eight weeks."),
    ("Data protection", "Personal data in this file is processed under our privacy notice. You may request access to, "
                        "correction of, or deletion of your data; requests are normally answered within one month."),
    ("Service hours", "The service desk is staffed Monday to Friday, 08:00-18:00 local time, excluding public holidays. "
                      "Messages received outside these hours are handled the next business day."),
    ("Document control", "Owner: Operations Policy. Review cycle: every {n1} months. Printed copies are uncontrolled; check "
                         "the intranet for the latest issue before relying on a printout."),
    ("Glossary (extract)", "'Business day' means a day other than a Saturday, Sunday or public holiday. 'Writing' includes "
                           "email. Headings are for convenience only and do not affect interpretation."),
    ("Language", "Where this document is translated, the English version prevails in the event of any inconsistency."),
    ("Training reminder", "All staff must complete the annual {topic} refresher by {d1}. Completion is tracked in the "
                          "learning portal; managers receive a weekly exception report."),
    ("Escalation matrix", "Level 1: case handler. Level 2: team lead (response within {n1} hours). Level 3: department "
                          "manager. Out-of-hours issues go to the duty manager via the on-call number."),
    ("System notice", "The case-management system will be unavailable for upgrades on {d1} between 22:00 and 02:00. Save "
                      "drafts locally and avoid submitting approvals during this window."),
    ("Office move", "From {d1} the team moves to the 4th floor, east wing. Desk numbers change; phone extensions stay the "
                    "same. Please clear personal items from the old desks by the Friday before."),
    ("Audit sampling", "Internal audit samples {n2} closed cases per quarter. Sampled files must include every calculation "
                       "worksheet and approval stamp; missing worksheets are logged as findings."),
]

DOMAIN_NOISE = {
    "insurance": [
        ("Section 9 - Flood", "Flood damage is excluded unless the optional flood endorsement has been purchased. Where it "
                              "applies, a separate flood deductible of {m1} applies per occurrence and flood payments are limited to {m2}."),
        ("Section 4 - Additional living expenses", "If the home is uninhabitable after an insured event, reasonable extra "
                                                   "living costs are paid for up to {n1} months, subject to an overall limit of {m2}."),
        ("Section 13 - Cancellation", "The policyholder may cancel at any time. Cancellation within the first {n2} days gives "
                                      "a full premium refund; afterwards the unearned premium is refunded pro rata less {m3}."),
        ("Premium instalments", "Monthly instalment plans carry a finance charge of {p1}% of the annual premium. After a "
                                "missed instalment there is a {n2}-day grace period before cover is suspended."),
        ("Section 15 - Liability", "Personal liability cover pays up to {m2} per occurrence for injury to others or damage to "
                                   "their property. It does not cover business activities."),
    ],
    "travel": [
        ("Airfare", "Economy class is required for flights under {n1} hours. Premium economy may be booked for longer flights "
                    "with director approval. Rail travel is standard class."),
        ("Receipts", "Itemised receipts are required for any single expense above {m3}. Card slips alone are not sufficient. "
                     "Missing receipts may be replaced by a signed declaration no more than {n1} times per year."),
        ("Ground transport", "Taxis and ride-hailing are reimbursed at cost for business journeys. Airport parking is "
                             "reimbursed up to {m3} per day. Rental cars must be mid-size or smaller."),
        ("Submission deadline", "Expense reports are due within {n2} days of the trip's end. Later reports need finance-"
                                "director sign-off and may be paid in the following cycle."),
        ("Client entertainment", "Client entertainment is capped at {m3} per attendee and must list attendees and the "
                                 "business purpose. Alcohol is not reimbursable at internal team events."),
    ],
    "saas": [
        ("Seat changes", "Seats added mid-term are charged pro rata from the day they are added. Seats removed mid-term reduce "
                         "the price only from the next renewal."),
        ("Support tiers", "Standard support responds within {n1} business hours. Premium support ({m3} per month) responds "
                          "within {n1} hours around the clock."),
        ("Price protection", "Renewal prices for customers on multi-year agreements may rise by no more than {p1}% per year."),
        ("Data export", "After cancellation, customer data stays available for export for {n2} days and is then permanently "
                        "deleted."),
        ("Payment terms", "Invoices are payable within {n2} days. Wire transfers below {m2} carry a bank handling fee of {m3}."),
    ],
    "sla": [
        ("Support response targets", "Priority 1 tickets: response within {n2} minutes. Priority 2: within {n1} hours. "
                                     "Response targets are not availability commitments and create no service credits."),
        ("Credit claims procedure", "Credits must be requested through the support portal within {n2} days after the end of "
                                    "the month and are applied to a future invoice; they are never paid in cash."),
        ("Preview features", "Services labelled beta or preview have no availability commitment and are outside this SLA."),
        ("Chronic failure", "If the service misses its commitment in three consecutive months, the customer may terminate the "
                            "affected service without penalty on {n2} days' notice."),
    ],
    "loan": [
        ("Prepayment", "The borrower may prepay on any interest payment date on {n1} business days' notice. Prepayments in "
                       "the first {n2} months carry a fee of {p1}% of the amount prepaid."),
        ("Default interest", "On any overdue amount, default interest accrues at {p1} percentage points above the contractual "
                             "rate from the due date until paid."),
        ("Commitment fee", "A commitment fee of {p1}% per annum accrues on the undrawn part of the facility and is payable "
                           "quarterly in arrears."),
        ("Financial covenants", "Net leverage must not exceed {n1}.0x at each quarter end. A breach is an event of default "
                                "unless cured within {n2} days."),
    ],
    "ship": [
        ("Restricted items", "Loose lithium batteries, aerosols over {n1}00 ml and perishables need the special-handling "
                             "service and cannot be sent on standard rates."),
        ("Delivery attempts", "Two delivery attempts are included. A third attempt costs {m3}. Parcels not collected within "
                              "{n2} days are returned to sender at the sender's cost."),
        ("Liability", "Liability for loss or damage is limited to {m2} per parcel unless extended cover was purchased. Claims "
                      "must be filed within {n2} days of the ship date."),
        ("Saturday delivery", "Saturday delivery is available in selected postcodes for {m3} per parcel."),
        ("Freight", "Pallet shipments over {n1}00 kg are quoted separately and are not priced from this rate card."),
    ],
    "qa": [
        ("Sampling plan", "Lots of up to {n1}00 units are sampled at {n2} units per lot. Larger lots follow the tightened "
                          "sampling plan."),
        ("Calibration", "Balances and analyzers are calibrated every {n2} days. An instrument past its calibration date must "
                        "be tagged out and may not be used for release testing."),
        ("Deviations", "Deviations must be logged within {n1} hours. Minor deviations are closed by the shift lead; major "
                       "deviations need QA manager approval."),
        ("Retained samples", "Keep {n1} reference samples per lot for {n1} years after expiry, stored at 15-25 C."),
        ("Labelling", "Batch labels must show the lot number, manufacturing date and an expiry date {n1} months after "
                      "manufacture."),
    ],
    "hr": [
        ("Parental leave", "Eligible employees receive {n1} weeks of paid parental leave, which may be taken in up to three "
                           "blocks within twelve months of the birth or placement."),
        ("Sick leave", "Sick leave accrues separately and is never paid out on termination."),
        ("Public holidays", "The company observes {n1} public holidays per year; a holiday on a weekend is observed on the "
                            "nearest working day."),
        ("Notice periods", "Employees must give {n1} weeks' notice of resignation. Pay in lieu of notice may be offered at the "
                           "company's discretion."),
        ("Jury duty", "Employees summoned for jury duty receive full pay for up to {n2} days per calendar year."),
    ],
    "retail": [
        ("Price matching", "We match a competitor's advertised price within {n1} days of purchase for identical in-stock "
                           "items. Marketplace sellers and clearance prices are excluded."),
        ("Gift receipts", "Returns with a gift receipt are refunded as store credit only."),
        ("Warranty", "After the return window closes, faults are handled under the manufacturer's warranty. Extended "
                     "protection plans bought separately are refundable within {n2} days."),
        ("Loyalty points", "Points earned on a purchase are removed when the item is returned. Points never convert into cash."),
        ("Exchanges", "Exchanges for a different size or colour are free within the return window and are not subject to a "
                      "restocking fee."),
    ],
    "benefit": [
        ("Reporting changes", "Households must report income changes of more than {m3} per month within {n1} days. Failure "
                              "to report may lead to an overpayment claim."),
        ("Certification period", "Benefits are certified for {n1} months. A recertification interview is scheduled at least "
                                 "{n2} days before the period ends."),
        ("Fair hearings", "Applicants may request a fair hearing within {n2} days of a decision notice. Benefits may continue "
                          "unchanged pending the hearing if it is requested within ten days."),
        ("Card replacement", "A lost benefit card is replaced free the first time in each certification period; later "
                             "replacements cost {m3}, deducted from the next issuance."),
    ],
    "adm": [
        ("Application fee", "The application fee is {m3}. Fee waivers are granted automatically to applicants who qualify "
                            "for need-based aid."),
        ("Housing", "First-year students are guaranteed campus housing if the housing deposit of {m3} is paid by {d1}."),
        ("Deferral", "Admitted students may defer for up to one year. Merit awards are held; need-based aid is recalculated."),
        ("Renewal", "Merit awards renew each year if the student keeps a cumulative GPA of at least 3.00 and completes "
                    "{n2} credits per year."),
    ],
    "tel": [
        ("Roaming", "Data used abroad in zone 2 countries is billed per MB at roaming rates and never counts against the "
                    "domestic allowance."),
        ("Device instalments", "Device plans run for {n1} months. Paying off the balance early carries no fee."),
        ("Late payment", "A late-payment fee of {m3} applies if the bill is unpaid {n2} days after the due date."),
        ("Hotspot", "Tethering is included on all plans at no extra charge, within the plan's allowance."),
    ],
    "breach": [
        ("Informing individuals", "Where a breach is likely to result in a high risk to individuals, they must be informed "
                                  "without undue delay. This is separate from the authority deadline."),
        ("Processor duties", "Processors must tell the controller about a breach without undue delay; our contracts require "
                             "this within {n1} hours. This does not change the controller's own deadline."),
        ("Breach register", "All breaches, including those not notified to the authority, are recorded in the internal "
                            "breach register with facts, effects and remedial action."),
        ("Encryption", "A breach of properly encrypted data where the key was not compromised is unlikely to require "
                       "notification to individuals."),
    ],
    "fx": [
        ("Cut-off times", "Instructions received after {n1}:00 local time are processed on the next business day."),
        ("Recalls", "A recall can be requested after sending, but the return of funds is not guaranteed. Each recall "
                    "request costs {m3}."),
        ("Limits", "Online transfers are limited to {m2} per day unless a higher limit has been agreed."),
        ("Screening", "Payments may be delayed for compliance screening. The bank is not liable for such delays."),
    ],
    "health": [
        ("Prior authorization", "Advanced imaging, inpatient admissions and specialty drugs require prior authorization; "
                                "without it the claim may be denied."),
        ("Appeals", "You may appeal a claim decision within {n2} days. Urgent appeals are decided within 72 hours."),
        ("Telehealth", "Telehealth visits with in-network providers have a {m3} copay."),
        ("Out-of-network care", "Out-of-network services have a separate deductible of {m1} and are paid at {p1}% below "
                                "the in-network level."),
    ],
    "util": [
        ("Budget billing", "Budget billing spreads charges evenly over {n1} months; the account is trued up annually."),
        ("Disconnection protection", "Service is not disconnected for non-payment on Fridays, weekends or holidays."),
        ("Net metering", "Solar export credits are applied at the retail rate and carried forward for up to {n1} months."),
        ("Late fees", "A late fee of {p1}% applies to balances unpaid after the due date."),
    ],
}


def fill_noise(rng, tpl, M, ds):
    vals = dict(n1=rng.randint(2, 12), n2=rng.randint(5, 90), p1=pick(rng, ["1.5", "2", "2.5", "3", "5", "10"]),
                m1=M(D(rng.randrange(250, 5000, 50))), m2=M(D(rng.randrange(1000, 50000, 500))),
                m3=M(D(rng.randrange(5, 150))), d1=fdate(rand_date(rng), ds),
                topic=pick(rng, ["anti-fraud", "data-protection", "information-security", "conduct"]))
    return tpl.format(**vals)


def noise_pool(rng, case, scen, n_other=3):
    ds = rng.randrange(4)
    M = case["M"]
    pool = [(t, fill_noise(rng, x, M, ds)) for t, x in DOMAIN_NOISE.get(scen, [])]
    pool += [(t, fill_noise(rng, x, M, ds)) for t, x in rng.sample(GENERIC_NOISE, 7)]
    for _ in range(n_other):
        r2 = random.Random(rng.getrandbits(48))
        other = SCEN_FN[scen](r2, "short", cur=case.get("cur"))
        if other["cid"] == case["cid"]:
            continue
        body = "; ".join("%s: %s" % (a, b) for a, b in other["facts"] if a not in ("Claim", "Account", "Lot", "Case", "Trip",
                                                                               "Order", "Shipment", "Facility", "Payment"))
        if other.get("fact_table"):
            body += " (incident log: %d entries)" % len(other["fact_table"][2])
        ttl = pick(rng, ["Other file %s (unrelated - different customer)", "Previous case %s - closed, for reference only",
                         "Separate request %s (not this case)"]) % other["cid"]
        pool.append((ttl, body + "."))
    rng.shuffle(pool)
    return pool


# =========================================================================== RENDERING
def table_text(t, ts):
    cap, headers, rows = t
    rows = [[str(c) for c in r] for r in rows]
    headers = [str(h) for h in headers]
    w = [max([len(h)] + [len(r[i]) for r in rows]) for i, h in enumerate(headers)]
    if ts == "ascii":
        sep = "+" + "+".join("-" * (x + 2) for x in w) + "+"
        ln = lambda cs: "| " + " | ".join(c.ljust(x) for c, x in zip(cs, w)) + " |"
        body = "\n".join([sep, ln(headers), sep] + [ln(r) for r in rows] + [sep])
    elif ts == "pipe":
        ln = lambda cs: "| " + " | ".join(cs) + " |"
        body = "\n".join([ln(headers), "|" + "|".join("---" for _ in headers) + "|"] + [ln(r) for r in rows])
    elif ts == "space":
        ln = lambda cs: "  ".join(c.ljust(x) for c, x in zip(cs, w)).rstrip()
        body = "\n".join([ln(headers), "  ".join("-" * x for x in w)] + [ln(r) for r in rows])
    else:
        q = lambda c: '"%s"' % c if "," in c else c
        body = "\n".join([",".join(q(h) for h in headers)] + [",".join(q(c) for c in r) for r in rows])
    return cap + ":\n" + body


def build_seq(case, rs, notes, noise):
    cid = case["cid"]
    rb = {"k": "rules", "t": pick(rs, ["Rules", "Policy terms", "Applicable rules", "Calculation rules", "Current provisions",
                                       "Terms that apply"]), "items": list(case["rules"]), "table": case["rule_table"]}
    vb = {"k": "versions", "t": pick(rs, ["Rule history", "Amendments", "Schedule revisions", "Change log"]),
          "items": case["versions"]} if case["versions"] else None
    fb = {"k": "facts", "t": pick(rs, ["Case %s" % cid, "Record %s" % cid, "Details for %s" % cid, "File %s" % cid]),
          "pairs": [(l, v) for l, v in case["facts"] if v != cid], "table": case["fact_table"]}
    nb = {"k": "notes", "t": pick(rs, ["Notes on file", "Comments", "Internal notes", "Thread comments"]),
          "items": notes} if notes else None
    seq = [rb] + ([vb] if vb else [])
    if vb and rs.random() < 0.35:
        seq = [vb, rb]
    seq = ([fb] + seq) if rs.random() < 0.3 else (seq + [fb])
    if nb:
        if rs.random() < 0.7:
            seq.append(nb)
        else:
            seq.insert(rs.randint(0, len(seq)), nb)
    for t, x in noise:
        seq.insert(rs.randint(0, len(seq)), {"k": "noise", "t": t, "text": x})
    return seq


def r_prose(title, seq, rs, ts, short):
    out = [] if (short and rs.random() < 0.5) else [title, ""]
    for b in seq:
        k = b["k"]
        if k == "facts":
            if rs.random() < 0.5:
                txt = "%s: %s." % (b["t"], "; ".join("%s: %s" % (l, v) for l, v in b["pairs"]))
            else:
                txt = "%s. %s" % (b["t"], " ".join("%s - %s." % (l, v.rstrip(".")) for l, v in b["pairs"]))
        elif k == "noise":
            txt = "%s. %s" % (b["t"], b["text"])
        elif k == "notes":
            txt = "\n".join(b["items"])
        else:
            txt = ("%s: " % b["t"] if rs.random() < 0.6 else "") + " ".join(b["items"])
        if b.get("table"):
            txt += "\n" + table_text(b["table"], ts)
        out += [txt, ""]
    return "\n".join(out).strip()


def r_bullets(title, seq, rs, ts, short):
    out = [] if (short and rs.random() < 0.5) else [title.upper() if rs.random() < 0.3 else title, ""]
    mark = pick(rs, ["-", "*", "•"])
    for b in seq:
        out.append("%s:" % b["t"])
        if b["k"] == "facts":
            out += ["%s %s: %s" % (mark, l, v) for l, v in b["pairs"]]
        elif b["k"] == "noise":
            out.append(b["text"])
        else:
            out += ["%s %s" % (mark, x) for x in b["items"]]
        if b.get("table"):
            out.append(table_text(b["table"], ts))
        out.append("")
    return "\n".join(out).strip()


def r_numbered(title, seq, rs, ts, short):
    out = [title, ""]
    for i, b in enumerate(seq, 1):
        out.append("%d. %s" % (i, b["t"]))
        if b["k"] == "facts":
            out += ["   (%s) %s: %s" % ("abcdefghijklmnopqrstuvwxyz"[j], l, v) for j, (l, v) in enumerate(b["pairs"])]
        elif b["k"] == "noise":
            out.append("   " + b["text"])
        else:
            out += ["   %d.%d %s" % (i, j, x) for j, x in enumerate(b["items"], 1)]
        if b.get("table"):
            out.append(table_text(b["table"], ts))
        out.append("")
    return "\n".join(out).strip()


def r_markdown(title, seq, rs, ts, short):
    out = ["# " + title, ""]
    for b in seq:
        out.append("## " + b["t"])
        if b["k"] == "facts":
            out += ["| Field | Value |", "|---|---|"] + ["| %s | %s |" % (l, v) for l, v in b["pairs"]]
        elif b["k"] == "noise":
            out.append(b["text"])
        elif b["k"] == "notes":
            out += ["> " + x for x in b["items"]]
        else:
            out += ["- " + x for x in b["items"]]
        if b.get("table"):
            out += ["", table_text(b["table"], "pipe")]
        out.append("")
    return "\n".join(out).strip()


def r_json(title, seq, rs, ts, short):
    obj = {"document": title}
    for b in seq:
        k = b["k"]
        if k == "rules":
            obj["rules"] = b["items"]
            if b.get("table"):
                cap, h, rows = b["table"]
                obj["rules_table"] = {"caption": cap, "rows": [dict(zip(h, r)) for r in rows]}
        elif k == "versions":
            obj["rule_history"] = b["items"]
        elif k == "facts":
            d = {"id": b["t"].split()[-1]}
            d.update({l: v for l, v in b["pairs"]})
            if b.get("table"):
                cap, h, rows = b["table"]
                d[cap] = [dict(zip(h, r)) for r in rows]
            obj["case_record"] = d
        elif k == "notes":
            obj["comments"] = b["items"]
        else:
            obj.setdefault("other_sections", []).append({"heading": b["t"], "text": b["text"]})
    return json.dumps(obj, indent=None if short else 2, ensure_ascii=False)


def r_email(title, seq, rs, ts, short):
    ops = pick(rs, ["Policy Desk <policy@corp.example>", "Operations Lead <ops-lead@corp.example>",
                    "Team Lead <teamlead@corp.example>"])
    req = pick(rs, PEOPLE)
    out = ["Subject: %s" % title, ""]
    for b in seq:
        k = b["k"]
        if k in ("rules", "versions"):
            out += ["From: %s" % ops, "", pick(rs, ["Rules we apply:", "Reminder of the current terms:", "Relevant wording:"])]
            out += ["- " + x for x in b["items"]]
            if b.get("table"):
                out.append(table_text(b["table"], ts))
            out.append("")
        elif k == "facts":
            out += ["-----Original Message-----", "From: %s" % req, "", "%s -" % b["t"]]
            out += ["%s: %s" % (l, v) for l, v in b["pairs"]]
            if b.get("table"):
                out.append(table_text(b["table"], ts))
            out.append("")
        elif k == "notes":
            out += ["-----Original Message-----", "From: %s" % pick(rs, PEOPLE), ""] + b["items"] + [""]
        else:
            out += ["---------- Forwarded message ----------", "Subject: %s" % b["t"], "", b["text"], ""]
    return "\n".join(out).strip()


def r_table(title, seq, rs, ts, short):
    out = [title, ""]
    for b in seq:
        k = b["k"]
        if k == "facts":
            out.append(table_text((b["t"], ["Field", "Value"], [[l, v] for l, v in b["pairs"]]), ts))
            if b.get("table"):
                out.append(table_text(b["table"], ts))
        elif k == "noise":
            out.append("[%s] %s" % (b["t"], b["text"]))
        elif k == "notes":
            out += ["> " + x for x in b["items"]]
        else:
            out.append(b["t"] + ":")
            pre = "R" if k == "rules" else "H"
            out += ["%s%d. %s" % (pre, i, x) for i, x in enumerate(b["items"], 1)]
            if b.get("table"):
                out.append(table_text(b["table"], ts))
        out.append("")
    return "\n".join(out).strip()


RENDER = {"prose": r_prose, "bullets": r_bullets, "numbered": r_numbered, "markdown": r_markdown, "json": r_json,
          "email": r_email, "table": r_table}
SHORT_FORMATS = ["prose", "bullets", "prose", "table", "json"]


def render(case, rseed, fmt, notes, noise, short):
    rs = random.Random(rseed)
    ts = pick(rs, ["ascii", "pipe", "space", "csv"])
    seq = build_seq(case, rs, notes, noise)
    return RENDER[fmt](case["title"], seq, rs, ts, short)


# =========================================================================== ASSEMBLY
CMPS = [("more than", lambda a, b: a > b), ("at least", lambda a, b: a >= b), ("less than", lambda a, b: a < b),
        ("no more than", lambda a, b: a <= b), ("over", lambda a, b: a > b), ("at most", lambda a, b: a <= b),
        ("under", lambda a, b: a < b)]


def nice_between(a, b):
    lo, hi = min(a, b), max(a, b)
    gap = hi - lo
    if gap <= C2:
        return None
    for step in (D(1000), D(500), D(100), D(50), D(10), D(5), D(1), D("0.5"), D("0.1"), C2):
        if gap > step * 2:
            c = ((lo + gap / 3) / step).to_integral_value(rounding=ROUND_CEILING) * step
            if lo < c < hi:
                return q2(c)
    c = q2((lo + hi) / 2)
    return c if lo < c < hi else None


def _build(rng, qtype, target, scen=None, mode=None):
    if scen is None:
        scen = pick(rng, SCENARIOS)[0]
    fn = SCEN_FN[scen]
    r = rng.random()
    if mode is None:
        mode = "short" if r < 0.30 else ("medium" if r < 0.70 else "long")
    for attempt in range(8):
        case = fn(rng, mode)
        kind = case["kind"]
        if kind == "amount":
            assert F(case["gold"]) == F(case["check"]), (scen, case["gold"], case["check"])
            fmt = case["fmt"]
        else:
            assert case["gold"] == case["check"], (scen, case["gold"], case["check"])
            fmt = lambda b: b
        gold_v = case["gold"]
        gold_s = fmt(gold_v)
        wrong, seen = [], {gold_s}
        for mname, val in case["alts"].items():
            if val is None or (kind == "amount" and val < 0):
                continue
            s = fmt(val)
            if s in seen:
                continue
            seen.add(s)
            wrong.append((mname, s, val))
        if len(wrong) >= (1 if kind == "band" else 2):
            break
    if kind == "amount" and len(wrong) < 2:
        for mname, val in (("arithmetic_slip_x10", q2(gold_v * 10)), ("dropped_last_step", q2(gold_v * D("0.9"))),
                           ("arithmetic_slip", q2(gold_v + D(100)))):
            s = fmt(val)
            if s not in seen and val >= 0:
                seen.add(s)
                wrong.append((mname, s, val))
    head, rest = wrong[:2], wrong[2:]
    rng.shuffle(rest)
    wrong = head + rest
    # misleading note
    notes, note_alt = [], None
    if wrong and rng.random() < {"short": 0.3, "medium": 0.45, "long": 0.55}[mode]:
        note_alt = wrong[0] if rng.random() < 0.6 else pick(rng, wrong[:3])
        notes.append(note_text(rng, case["thing"], note_alt[1], case["reasons"].get(note_alt[0])))
    mistakes, options, card = {}, None, None
    extra_hard = 0
    if qtype == "choice":
        if kind == "band":
            options = list(case["bands"])
            for mname, s, _ in wrong:
                mistakes.setdefault(s, mname)
            if case["card"]:
                card = "\n".join("- %s: %s" % (a, b) for a, b in case["card"])
        else:
            k = min(len(wrong), pick(rng, [2, 3, 3, 4, 4, 4, 5, 5, 6, 7]))
            chosen = [note_alt] if note_alt else []
            for w in wrong:
                if len(chosen) >= k:
                    break
                if w not in chosen:
                    chosen.append(w)
            options = [gold_s] + [w[1] for w in chosen]
            mistakes = {w[1]: w[0] for w in chosen}
        rng.shuffle(options)
        gold = gold_s
        instructions = case["q_choice"]
        chk = case["check"] if kind == "band" else case["fmt"](D(case["check"].numerator) / D(case["check"].denominator))
        gold_check = chk
    else:
        if kind == "band":
            if target == 1:
                b = gold_s
                if wrong:
                    mistakes = {"0": wrong[0][0]}
            else:
                if wrong:
                    w = note_alt if (note_alt and rng.random() < 0.5) else pick(rng, wrong[:3])
                    b = w[1]
                    mistakes = {"1": w[0]}
                else:
                    b = pick(rng, [x for x in case["bands"] if x != gold_s])
            instructions = case["q_band"](b)
            gold = target
            gold_check = 1 if case["check"] == b else 0
        else:
            done = False
            if rng.random() < 0.45:
                cands = [(gold_v, None)] + [(nice_between(gold_v, w[2]), w) for w in wrong]
                combos = [(T, cm) for T, _ in cands if T is not None for cm in CMPS]
                rng.shuffle(combos)
                fallback = None
                for T, (cw, cf) in combos:
                    if int(cf(gold_v, T)) != target:
                        continue
                    flips = [w for w in wrong if int(cf(w[2], T)) != target]
                    if flips:
                        fallback = (T, cw, cf, flips[0])
                        break
                    if fallback is None:
                        fallback = (T, cw, cf, None)
                if fallback:
                    T, cw, cf, fw = fallback
                    instructions = case["q_thr"](cw, fmt(T))
                    if fw:
                        mistakes = {str(1 - target): fw[0]}
                    if T == gold_v:
                        extra_hard = 1
                    gold = target
                    gold_check = int(cf(F(case["check"]), F(T)))
                    done = True
            if not done:
                if target == 1:
                    v = gold_s
                    if wrong:
                        mistakes = {"0": wrong[0][0]}
                else:
                    w = note_alt if (note_alt and rng.random() < 0.5) else pick(rng, wrong[:3])
                    v = w[1]
                    mistakes = {"1": w[0]}
                instructions = case["q_prop"](v)
                gold = target
                chkv = case["fmt"](D(case["check"].numerator) / D(case["check"].denominator))
                gold_check = 1 if chkv == v else 0
    # ---- render with length control
    rseed = rng.getrandbits(48)
    if mode == "short":
        fmts = [pick(rng, SHORT_FORMATS)] + SHORT_FORMATS
        state = None
        for f in fmts:
            for nt in (notes, []):
                s = render(case, rseed, f, nt, [], True)
                if state is None or len(s) < len(state):
                    state = s
                if len(s) < 600:
                    break
            if len(state) < 600:
                break
    else:
        f = pick(rng, list(RENDER))
        state = render(case, rseed, f, notes, [], False)
        if mode == "medium":
            target_len, max_len = rng.randint(650, 2300), 2450
        else:
            target_len, max_len = rng.randint(2700, 5700), 5950
        pool = noise_pool(random.Random(rng.getrandbits(48)), case, scen, n_other=2 if mode == "medium" else 4)
        noise = []
        for cand in pool:
            if len(state) >= target_len:
                break
            trial = render(case, rseed, f, notes, noise + [cand], False)
            if len(trial) > max_len:
                continue
            noise.append(cand)
            state = trial
    score = case["ntr"] + (1 if notes else 0) + (1 if mode == "long" else 0) + extra_hard
    diff = "hard" if score >= 3 else "medium"
    row = {"state": state, "qtype": qtype, "instructions": instructions,
           "options": options if qtype == "choice" else None, "gold": gold}
    if card and qtype == "choice":
        row["card"] = card
    meta = {"family": FAMILY, "difficulty": diff}
    if mistakes:
        meta["mistakes"] = mistakes
    row["meta"] = meta
    info = {"scen": scen, "domain": case["domain"], "gold_check": gold_check, "mode": mode}
    return row, info


def _generate(n, seed):
    rng = random.Random(seed)
    out = []
    yes = no = 0
    deck, mdeck = [], []
    for _ in range(n):
        if not deck:
            deck = [nm for nm, _ in SCENARIOS]
            rng.shuffle(deck)
        if not mdeck:
            mdeck = ["short"] * 3 + ["medium"] * 4 + ["long"] * 3
            rng.shuffle(mdeck)
        scen = deck.pop()
        mode = mdeck.pop()
        qtype = "choice" if rng.random() < 0.7 else "noul"
        target = None
        if qtype == "noul":
            if yes < no:
                target = 1
            elif no < yes:
                target = 0
            else:
                target = rng.randrange(2)
            if target:
                yes += 1
            else:
                no += 1
        item_rng = random.Random(rng.getrandbits(64))
        row, info = _build(item_rng, qtype, target, scen, mode)
        assert row["gold"] == info["gold_check"], ("independent check disagrees", info, row["gold"])
        out.append((row, info))
    return out


def generate(n: int, seed: int) -> list:
    """Return n rows of the "numeric" family, deterministic in `seed`."""
    return [r for r, _ in _generate(n, seed)]


# =========================================================================== SELF-TEST
def _validate(row):
    keys = set(row)
    assert keys <= {"state", "qtype", "instructions", "options", "gold", "card", "meta"}, keys
    assert {"state", "qtype", "instructions", "options", "gold", "meta"} <= keys, keys
    assert isinstance(row["state"], str) and row["state"].strip()
    assert isinstance(row["instructions"], str) and row["instructions"].strip()
    assert row["qtype"] in ("choice", "noul")
    m = row["meta"]
    assert m["family"] == FAMILY and m["difficulty"] in ("medium", "hard")
    assert set(m) <= {"family", "difficulty", "gold_probs", "mistakes"}
    if row["qtype"] == "choice":
        opts = row["options"]
        assert isinstance(opts, list) and 2 <= len(opts) <= 8, opts
        assert len(set(opts)) == len(opts), opts
        assert all(isinstance(o, str) for o in opts)
        assert row["gold"] in opts
        if "mistakes" in m:
            assert all(k in opts and k != row["gold"] for k in m["mistakes"]), (m["mistakes"], opts)
        if row.get("card") is not None:
            for line in row["card"].split("\n"):
                assert line.startswith("- ") and ": " in line
    else:
        assert row["options"] is None
        assert row["gold"] in (0, 1) and not isinstance(row["gold"], bool)
        assert "card" not in row or row["card"] is None
    if "gold_probs" in m:
        assert abs(sum(m["gold_probs"].values()) - 1) < 1e-9
    json.dumps(row)


if __name__ == "__main__":
    import collections
    demo = generate(3, 7)
    for r in demo:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        print("-" * 80)
    N = 300
    pairs = _generate(N, 12345)
    rows = [r for r, _ in pairs]
    for r in rows:
        _validate(r)
    assert rows == generate(N, 12345), "determinism failed"
    assert rows != generate(N, 999), "different seeds gave identical output"
    for r, info in pairs:
        assert r["gold"] == info["gold_check"]
    # extra independent checks over many seeds (asserts inside _build)
    for sd in range(5):
        _generate(200, 1000 + sd)
    lens = [len(r["state"]) for r in rows]
    short = sum(1 for x in lens if x < 600)
    med = sum(1 for x in lens if 600 <= x <= 2500)
    lng = sum(1 for x in lens if x > 2500)
    nouls = [r for r in rows if r["qtype"] == "noul"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    pos = collections.Counter(r["options"].index(r["gold"]) / max(1, len(r["options"]) - 1) for r in ch)
    print("items:", N, "choice:", len(ch), "noul:", len(nouls),
          "noul yes-rate: %.3f" % (sum(r["gold"] for r in nouls) / max(1, len(nouls))))
    print("length short/medium/long: %d/%d/%d  (min %d, max %d)" % (short, med, lng, min(lens), max(lens)))
    print("difficulty:", collections.Counter(r["meta"]["difficulty"] for r in rows))
    print("scenarios:", collections.Counter(i["scen"] for _, i in pairs))
    print("domains:", len(set(i["domain"] for _, i in pairs)))
    print("options per choice:", collections.Counter(len(r["options"]) for r in ch))
    print("gold first/last position share: %.2f / %.2f" % (
        sum(1 for r in ch if r["options"].index(r["gold"]) == 0) / len(ch),
        sum(1 for r in ch if r["options"].index(r["gold"]) == len(r["options"]) - 1) / len(ch)))
    print("SELF-TEST PASSED")
