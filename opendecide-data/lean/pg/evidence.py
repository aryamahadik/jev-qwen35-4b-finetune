# -*- coding: utf-8 -*-
"""pg.evidence -- procedural generator for the "evidence" family.

A case (claim, incident, shipment, alert ...) has a base-rate prior over 2-5
possible outcomes and 1-4 pieces of evidence, each with a stated likelihood
(conditional rates, detector sensitivity / false-alarm rate, likelihood ratio,
classifier reliability, or a threshold feature whose presence must be worked
out from dates / quantities).  The exact posterior is computed with Bayes'
rule (conditional independence stated in the text) using Fractions.

Traps built in on purpose: base-rate neglect, ignoring evidence, superseded
figures, wrong reference class, odds read as probability, per-1,000 read as
percent, unit mix-ups (lb/kg, km/mi, minutes/hours, MB/GB ...), inclusive vs
exclusive boundaries, absent signals, evidence-admissibility rules with
exceptions to exceptions (sometimes double negated), unverified junior notes
and vivid surface cues.

Pure standard library, deterministic in the seed.
    generate(n, seed) -> list[dict]
"""
import calendar
import datetime
import json
import math
import random
from decimal import Decimal, localcontext
from fractions import Fraction as F

FAMILY = "evidence"

# =========================================================================
# small text / number helpers
# =========================================================================
_MON = ["", "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"]
_DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _cap(s):
    return s[:1].upper() + s[1:] if s else s


def _low(s):
    if len(s) > 1 and s[1].isupper():
        return s
    return s[:1].lower() + s[1:] if s else s


def _join(items, conj="and"):
    items = list(items)
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return "%s %s %s" % (items[0], conj, items[1])
    return ", ".join(items[:-1]) + ", %s %s" % (conj, items[-1])


def _plain(x):
    """Exact decimal string of a Fraction with a finite decimal expansion."""
    x = F(x)
    for d in range(0, 14):
        y = x * 10 ** d
        if y.denominator == 1:
            n = y.numerator
            neg = n < 0
            s = str(abs(n))
            if d:
                s = s.rjust(d + 1, "0")
                s = s[:-d] + "." + s[-d:]
            return ("-" if neg else "") + s
    raise ValueError("not a finite decimal: %r" % (x,))


def _num(x):
    s = _plain(x)
    if "." in s:
        ip, fp = s.split(".")
    else:
        ip, fp = s, ""
    neg = ip.startswith("-")
    ip = ip.lstrip("-")
    if len(ip) > 3:
        ip = "{:,}".format(int(ip))
    return ("-" if neg else "") + ip + ("." + fp if fp else "")


def _pct(p):
    return _num(F(p) * 100) + "%"


_WQ = {F(1, 2): "half of {n}", F(1, 4): "a quarter of {n}", F(3, 4): "three quarters of {n}",
       F(1, 5): "one in five {n}", F(1, 10): "one in ten {n}", F(9, 10): "nine in ten {n}",
       F(2, 5): "two in five {n}", F(3, 5): "three in five {n}", F(4, 5): "four in five {n}",
       F(1, 20): "one in twenty {n}"}


def _Q(p, noun, style):
    """Quantity phrase: '<p> of <noun>' in the item's number style."""
    p = F(p)
    if style == "outof":
        return "%s out of every 100 %s" % (_num(p * 100), noun)
    if style == "in" and 0 < p < 1 and p.denominator <= 20:
        return "%d in %d %s" % (p.numerator, p.denominator, noun)
    if style == "per1000":
        return "%s of every 1,000 %s" % (_num(p * 1000), noun)
    if style == "pm":
        return "%s per 1,000 %s" % (_num(p * 1000), noun)
    if style == "words" and p in _WQ:
        return _WQ[p].format(n=noun)
    return "%s of %s" % (_pct(p), noun)


def _V(p, style):
    """Bare value string in the item's number style."""
    p = F(p)
    if style == "dec":
        return _num(p)
    if style == "in" and 0 < p < 1 and p.denominator <= 20:
        return "%d in %d" % (p.numerator, p.denominator)
    if style in ("per1000", "pm"):
        return "%s per 1,000" % _num(p * 1000)
    if style == "outof":
        return "%s out of 100" % _num(p * 100)
    return _pct(p)


def _fmt_date(d, style):
    if style == 0:
        return d.isoformat()
    if style == 1:
        return "%s %d, %d" % (_MON[d.month], d.day, d.year)
    if style == 2:
        return "%d %s %d" % (d.day, _MON[d.month], d.year)
    return "%s %d %s %d" % (_DOW[d.weekday()], d.day, _MON[d.month][:3], d.year)


def _rand_date(rng):
    return datetime.date(2023, 1, 2) + datetime.timedelta(days=rng.randrange(1100))


def _lr_round(raw, total):
    """Largest-remainder rounding of non-negative reals to integers summing to total."""
    fl = [int(math.floor(x)) for x in raw]
    rem = total - sum(fl)
    order = sorted(range(len(raw)), key=lambda i: (-(raw[i] - fl[i]), i))
    for i in order[:rem]:
        fl[i] += 1
    return fl


def _round_pct(post):
    raw = [F(p) * 100 for p in post]
    fl = [int(math.floor(x)) for x in raw]
    rem = 100 - sum(fl)
    order = sorted(range(len(raw)), key=lambda i: (-(raw[i] - fl[i]), i))
    for i in order[:rem]:
        fl[i] += 1
    return fl


def _argmax(v):
    best = 0
    for i in range(1, len(v)):
        if v[i] > v[best]:
            best = i
    return best


def _top_gap(v):
    s = sorted(v, reverse=True)
    return s[0] - s[1] if len(s) > 1 else s[0]


# =========================================================================
# units (two independent tables: Fraction for the engine, Decimal for check)
# =========================================================================
_UNITS = {
    "time": {"seconds": F(1, 3600), "minutes": F(1, 60), "hours": F(1), "days": F(24), "weeks": F(168)},
    "mass": {"g": F(1, 1000), "kg": F(1), "lb": F("0.45359237"), "oz": F("0.028349523125")},
    "length": {"mm": F(1, 1000), "cm": F(1, 100), "m": F(1), "km": F(1000), "mi": F("1609.344"),
               "ft": F("0.3048")},
    "data": {"KB": F(1, 1000), "MB": F(1), "GB": F(1000)},
}
_DEC_BASE = {  # everything in seconds / grams / millimetres / kilobytes
    "seconds": "1", "minutes": "60", "hours": "3600", "days": "86400", "weeks": "604800",
    "g": "1", "kg": "1000", "lb": "453.59237", "oz": "28.349523125",
    "mm": "1", "cm": "10", "m": "1000", "km": "1000000", "mi": "1609344", "ft": "304.8",
    "KB": "1", "MB": "1000", "GB": "1000000",
}
_UNIT_SING = {"seconds": "second", "minutes": "minute", "hours": "hour", "days": "day", "weeks": "week",
              "mi": "mile"}
_UNIT_PLUR = {"mi": "miles"}


def _qv(v, u):
    v = F(v)
    if v == 1 and u in _UNIT_SING:
        return "1 %s" % _UNIT_SING[u]
    return "%s %s" % (_num(v), _UNIT_PLUR.get(u, u))


_NICE = sorted(set([F(i) for i in range(1, 301)] + [F(i, 2) for i in range(1, 120)] +
                   [F(i, 10) for i in range(1, 60)] + [F(i, 100) for i in range(1, 30)] +
                   [F(i * 10) for i in range(31, 101)] + [F(i * 100) for i in range(11, 101)]))


def _nice(v):
    v = F(v)
    return v > 0 and (v * 100).denominator == 1 and v < 100000


_OPS = ["<=", "<", ">", ">="]
_FLIP = {"<=": "<", "<": "<=", ">=": ">", ">": ">="}


def _cmp(a, b, op):
    if op == "<=":
        return a <= b
    if op == "<":
        return a < b
    if op == ">=":
        return a >= b
    return a > b


_DAYS_REL = {
    "<=": ["within {T} days of {ref} (day {T} itself counts)", "no more than {T} days {dir} {ref}",
           "at most {T} days {dir} {ref}", "{T} days or fewer {dir} {ref}"],
    "<": ["less than {T} days {dir} {ref}", "within {T} days of {ref} (day {T} itself does not count)",
          "fewer than {T} days {dir} {ref}"],
    ">": ["more than {T} days {dir} {ref}", "over {T} days {dir} {ref}"],
    ">=": ["{T} or more days {dir} {ref}", "at least {T} days {dir} {ref}"],
}
_QTY_REL = {">": ["more than {T}", "over {T}", "above {T}"], ">=": ["{T} or more", "at least {T}"],
            "<": ["less than {T}", "under {T}"], "<=": ["{T} or less", "at most {T}", "no more than {T}"]}


# =========================================================================
# domain content
# =========================================================================
def _O(label, plural, desc, cue):
    return dict(label=label, plural=plural, desc=desc, cue=cue)


def _S(label, stat, yes, no):
    return dict(label=label, stat=stat, yes=yes, no=no)


def _GD(verb, short, ref, direction, Ts, obs):
    return dict(type="days", verb=verb, short=short, ref=ref, dir=direction, Ts=Ts, obs=obs)


def _GQ(dim, verb, short, suffix, Ts, units, obs):
    return dict(type="qty", dim=dim, verb=verb, short=short, suffix=suffix, Ts=Ts, units=units, obs=obs)


def _CH(name, names, A, A_yes, A_no, B, B_yes, B_no):
    return dict(name=name, names=names, A=A, A_yes=A_yes, A_no=A_no, B=B, B_yes=B_yes, B_no=B_no)


DOMAINS = [
    dict(key="insurance", what="explanation", case="claim", cases="claims", idp="CLM-",
         orgs=["Harbor Mutual", "Northgate Insurance", "Crescent Assurance", "Pinecrest Home & Auto"],
         intros=["{org} is reviewing claim {id}: a policyholder reports {detail}.",
                 "Claim {id} was lodged with {org} for {detail}.",
                 "A homeowner insured with {org} has filed claim {id} for {detail}."],
         details=["water damage in a finished basement ($8,400 requested)",
                  "the theft of two bicycles from a locked garage ($3,150 requested)",
                  "hail damage to a roof ($12,900 requested)", "a small kitchen fire ($6,200 requested)",
                  "a burst pipe in an upstairs bathroom ($9,750 requested)"],
         outcomes=[
             _O("Legitimate loss", "legitimate losses", "the loss happened as reported and the amount is fair",
                "The policyholder has been with {org} for 14 years and attached a neat, itemised list."),
             _O("Inflated claim", "inflated claims", "a real loss, but the amount has been padded",
                "The policyholder's email says the payout \"would finally cover the renovation we wanted\"."),
             _O("Staged loss", "staged losses", "the incident was deliberately arranged",
                "A neighbour posted online that the damage \"looked a bit too convenient\"."),
             _O("Filing error", "filing errors", "the claim was attached to the wrong policy or date by mistake",
                "The loss date on the claim form has been crossed out and rewritten."),
             _O("Duplicate claim", "duplicate claims", "the same loss has already been claimed elsewhere",
                "The subject line of the policyholder's email reads \"RE: RE: claim - trying again\"."),
         ],
         signals=[
             _S("another claim in the prior 24 months", "had another claim in the prior 24 months",
                "The policyholder had another claim in the prior 24 months.",
                "The policyholder had no other claim in the prior 24 months."),
             _S("receipts that are all round-dollar amounts", "came with receipts that were all round-dollar amounts",
                "Every receipt submitted is a round-dollar amount.", "Several receipts show non-round amounts."),
             _S("no police or fire report", "had no police or fire report on file",
                "There is no police or fire report on file.", "A police or fire report is on file."),
             _S("photos with stripped metadata", "included photos with their metadata stripped",
                "The attached photos have their metadata stripped.", "The attached photos have intact metadata."),
             _S("a payout-timing call before adjuster contact",
                "involved a call about payout timing before any adjuster contact",
                "The policyholder called about payout timing before any adjuster had been in touch.",
                "The policyholder made no payout-timing call before adjuster contact."),
         ],
         gates=[
             _GD("were filed", "filed", "the policy start date", "after", [30, 60, 90],
                 ["Policy start date: {d1}. Claim filed: {d2}.",
                  "The policy started on {d1}, and the claim was filed on {d2}."]),
             _GQ("time", "were first reported", "first reported", " after the loss",
                 [(72, "hours"), (3, "days"), (48, "hours")], ["hours", "days"],
                 ["The loss was first reported {V} after it happened.", "Time from loss to first report: {V}."]),
         ],
         tool=dict(name="the automated staged-loss screen", verb="flagged", inf="flag", target=2),
         clf="the intake triage model",
         channel=_CH("an anonymous tip-line report", "anonymous tip-line reports",
                     "it has been corroborated by a named witness",
                     "A named witness has since corroborated the tip.", "No named witness has corroborated the tip.",
                     "the witness is related to, or in business with, the policyholder",
                     "The corroborating witness is the policyholder's brother-in-law.",
                     "The corroborating witness has no connection to the policyholder."),
         ref=dict(broad="all {org} property claims", sub="property claims from the Coastal region",
                  member="The insured property is in Bayside County, which {org} files under its Coastal region."),
         segs=["commercial property policies", "auto policies", "renters' policies"],
         filler=[("Deductibles", "The standard deductible of $1,000 applies per occurrence; wind and hail losses in "
                                 "coastal counties carry a separate 2% deductible."),
                 ("Subrogation", "Where a third party caused the loss, {org} may seek recovery from that party after "
                                 "paying the insured, who must cooperate with any such action."),
                 ("Payment timing", "Undisputed amounts are paid within 15 business days of receiving a signed "
                                    "proof of loss."),
                 ("Appraisal clause", "If the insured and {org} disagree on the amount of loss, either side may demand "
                                      "an appraisal; each side pays its own appraiser and they split the umpire fee.")]),
    dict(key="saas_incident", what="root cause", case="incident", cases="incidents", idp="INC-",
         orgs=["Lumen Cloud", "Stackwell", "Parcelbase", "Nimbus CRM"],
         intros=["{org} declared incident {id} after {detail}.", "Incident {id} at {org}: {detail}.",
                 "The on-call engineer at {org} opened {id} because {detail}."],
         details=["checkout requests started failing for EU customers",
                  "the login API returned elevated 5xx errors",
                  "the dashboard became unusable for about 30% of tenants",
                  "webhook deliveries backed up for over an hour"],
         outcomes=[
             _O("Bad deploy", "incidents caused by a bad deploy", "a code change shipped shortly before the incident",
                "The incident channel is full of messages asking who merged last."),
             _O("Database saturation", "database-saturation incidents",
                "the primary database ran out of connections or I/O",
                "The first alert that fired was titled \"DB CPU high\"."),
             _O("Network/DNS fault", "network or DNS incidents", "traffic failed to route or resolve",
                "Several customers posted that the site \"can't be found\"."),
             _O("Third-party outage", "third-party outages", "an upstream provider was down",
                "The payment provider's status page shows a yellow banner."),
             _O("Config change", "config-change incidents", "a feature-flag or configuration change misbehaved",
                "Someone posted \"did anyone touch the flags?\" in the incident chat."),
         ],
         signals=[
             _S("errors confined to one region", "had errors confined to a single region",
                "Errors were confined to a single region.", "Errors appeared in every region."),
             _S("a deploy in the preceding hour", "were preceded by a deploy in the prior hour",
                "A deploy went out in the hour before the incident.",
                "No deploy went out in the hour before the incident."),
             _S("connection-pool exhaustion warnings", "logged connection-pool exhaustion warnings",
                "The logs contain connection-pool exhaustion warnings.",
                "There are no connection-pool exhaustion warnings in the logs."),
             _S("timeouts to an external API", "showed timeouts to an external API",
                "Traces show timeouts to an external API.", "Traces show no timeouts to external APIs."),
             _S("recovery without any rollback", "recovered without any rollback",
                "Service recovered without any rollback.", "Service recovered only after a rollback."),
         ],
         gates=[
             _GQ("time", "lasted", "lasting", "", [(90, "minutes"), (2, "hours"), (45, "minutes")],
                 ["minutes", "hours"], ["The incident lasted {V}.", "Time from first alert to resolution: {V}."]),
             _GD("occurred", "occurring", "the last dependency upgrade", "after", [7, 14, 30],
                 ["Last dependency upgrade: {d1}. Incident date: {d2}.",
                  "The last dependency upgrade shipped on {d1}; the incident happened on {d2}."]),
         ],
         tool=dict(name="the change-correlation bot", verb="flagged", inf="flag", target=0),
         clf="the auto-triage classifier",
         channel=_CH("a customer-submitted report", "customer-submitted reports",
                     "it was reproduced by an on-call engineer", "An on-call engineer reproduced it.",
                     "No engineer has reproduced it.",
                     "the reproduction was done on a staging environment rather than in production",
                     "The reproduction was done on staging, not production.",
                     "The reproduction was done in production."),
         ref=dict(broad="all incidents across {org}", sub="incidents in the payments service",
                  member="The affected service is payments-api, owned by the payments team."),
         segs=["the mobile apps", "internal tooling", "the data warehouse"],
         filler=[("Severity definitions", "SEV1: full outage for many customers; SEV2: a major feature degraded; "
                                          "SEV3: minor impact. Severity can be raised but not lowered mid-incident."),
                 ("Postmortems", "Postmortems are due within five business days and must be blameless."),
                 ("Status page", "Status page updates are posted at least every 30 minutes during a SEV1 or SEV2."),
                 ("On-call", "On-call rotations change every Monday at 10:00 local time.")]),
    dict(key="lending", what="outcome", case="delinquent account", cases="delinquent accounts", idp="ACC-",
         orgs=["Riverbend Credit Union", "Keystone Lending", "Brightpath Bank", "Oakline Finance"],
         intros=["{org} is forecasting how account {id} will resolve after {detail}.",
                 "Account {id} at {org} went delinquent: {detail}.",
                 "Collections at {org} flagged account {id} ({detail})."],
         details=["two missed card payments", "a missed instalment on a personal loan",
                  "a returned direct debit", "three weeks of arrears on a small-business card"],
         outcomes=[
             _O("Self-cure", "accounts that self-cured", "the borrower catches up without intervention",
                "The borrower's last message said \"sorry, payday was late this month\"."),
             _O("Hardship plan", "accounts that moved to a hardship plan", "the borrower needs a modified plan",
                "The borrower recently asked about \"payment holidays\" in the app."),
             _O("Charge-off", "accounts that were charged off", "the debt is written off as uncollectable",
                "The call notes say the borrower \"sounded very stressed\"."),
             _O("First-party fraud", "first-party fraud accounts", "the borrower never intended to repay",
                "The application was submitted at 3 a.m. from a mobile device."),
         ],
         signals=[
             _S("a prior payment dispute", "had a prior payment dispute",
                "The borrower has a prior payment dispute on file.", "The borrower has no prior payment dispute."),
             _S("credit utilisation above 90%", "had credit utilisation above 90%",
                "Credit utilisation is above 90%.", "Credit utilisation is below 90%."),
             _S("a partial payment this cycle", "made a partial payment in the current cycle",
                "A partial payment was made this cycle.", "No partial payment was made this cycle."),
             _S("an unreachable phone number", "had an unreachable phone number",
                "The phone number on file is unreachable.", "The phone number on file is reachable."),
             _S("an address change in the last 60 days", "had changed address in the last 60 days",
                "The address was changed within the last 60 days.", "The address has not changed in 60 days."),
         ],
         gates=[
             _GD("received the first collection call", "first collection call", "the missed due date", "after",
                 [7, 10, 14], ["Missed due date: {d1}. First collection call: {d2}.",
                               "The payment was due on {d1}; the first collection call was made on {d2}."]),
             _GQ("time", "had an account age at first missed payment of", "account age at first missed payment of",
                 "", [(8, "weeks"), (60, "days"), (12, "weeks")], ["weeks", "days"],
                 ["The account was {V} old at the first missed payment.", "Account age at first missed payment: {V}."]),
         ],
         tool=dict(name="the early-warning model", verb="flagged", inf="flag", target=2),
         clf="the collections segmentation model",
         channel=_CH("a note from a third-party collection agency", "notes from third-party collection agencies",
                     "it was confirmed on a recorded call", "It was confirmed on a recorded call.",
                     "It was not confirmed on any recorded call.", "the recording is more than 90 days old",
                     "The recording is 140 days old.", "The recording is from last week."),
         ref=dict(broad="all delinquent accounts", sub="delinquent accounts on the small-business card",
                  member="The account is a small-business card held by a sole trader."),
         segs=["mortgages", "auto loans", "student loans"],
         filler=[("Hardship policy", "Borrowers may request one payment holiday per 12 months; interest continues "
                                     "to accrue during the holiday."),
                 ("Contact rules", "Collection calls may only be placed between 08:00 and 21:00 local time and "
                                   "no more than three times in any seven-day period."),
                 ("Credit reporting", "Accounts are reported as delinquent to bureaus only once they are 30 days "
                                      "past due.")]),
    dict(key="clinic", what="outcome", case="booked appointment", cases="booked appointments", idp="APT-",
         orgs=["Lakeside Family Practice", "Eastgate Physio", "Northwood Health Centre", "Cedar Dental Group"],
         intros=["{org} wants to forecast what will happen with appointment {id}: {detail}.",
                 "Appointment {id} at {org} ({detail}) is on the overbooking review list.",
                 "The scheduling team at {org} is reviewing booking {id} - {detail}."],
         details=["a 30-minute follow-up visit", "an initial assessment",
                  "a routine check-up", "a 15-minute review slot"],
         outcomes=[
             _O("Attends on time", "appointments attended on time", "the patient arrives on time",
                "The patient has been with the practice for 20 years and always brings a thank-you card."),
             _O("Arrives late", "late arrivals", "the patient arrives more than 10 minutes late",
                "The booking note says \"coming straight from work\"."),
             _O("No-show", "no-shows", "the patient does not turn up and does not cancel",
                "The patient did not pick up when reception called about parking."),
             _O("Same-day cancellation", "same-day cancellations", "the patient cancels on the day",
                "The patient's child was reported sick at school last week."),
             _O("Reschedules in advance", "appointments rescheduled in advance", "the patient moves the booking early",
                "The patient asked last week whether Saturday slots exist."),
         ],
         signals=[
             _S("an unconfirmed SMS reminder", "had an unconfirmed SMS reminder",
                "The patient did not confirm the SMS reminder.", "The patient confirmed the SMS reminder."),
             _S("a previous no-show on record", "involved patients with a previous no-show on record",
                "The patient has a previous no-show on record.", "The patient has no previous no-show on record."),
             _S("an early-morning slot", "were early-morning slots", "The appointment is an early-morning slot.",
                "The appointment is not an early-morning slot."),
             _S("an unpaid balance", "involved patients with an unpaid balance",
                "The patient has an unpaid balance.", "The patient has no unpaid balance."),
             _S("a booking made by a relative", "had been booked by a relative rather than the patient",
                "The appointment was booked by a relative.", "The patient booked the appointment personally."),
         ],
         gates=[
             _GD("were booked", "booked", "the appointment", "before", [14, 21, 28],
                 ["Booked on {d1}; appointment date {d2}.",
                  "The booking was made on {d1} for an appointment on {d2}."]),
             _GQ("length", "involved a home-to-clinic distance of", "home-to-clinic distance of", "",
                 [(20, "km"), (15, "mi"), (30, "km")], ["km", "mi"],
                 ["The patient lives {V} from the clinic.", "Home-to-clinic distance on file: {V}."]),
         ],
         tool=dict(name="the no-show risk score", verb="flagged", inf="flag", target=2),
         clf="the scheduling assistant's outcome predictor",
         channel=_CH("information passed on by another patient", "reports passed on by other patients",
                     "it was confirmed directly with the patient", "Reception confirmed it directly with the patient.",
                     "Nobody has confirmed it with the patient.",
                     "the confirmation was a voicemail rather than a live conversation",
                     "The confirmation was a voicemail left by the patient.",
                     "The confirmation was a live phone conversation."),
         ref=dict(broad="all bookings across the group", sub="bookings at the Eastside site",
                  member="This booking is at the Eastside site."),
         segs=["telehealth calls", "vaccination clinics", "walk-in sessions"],
         filler=[("Late policy", "Patients arriving more than 15 minutes late may be asked to rebook."),
                 ("Cancellation fee", "A fee applies to cancellations with less than 24 hours' notice, waived for "
                                      "illness with a note."),
                 ("Parking", "Visitor parking is free for the first two hours with a validated ticket.")]),
    dict(key="logistics", what="cause of the delay", case="late shipment", cases="late shipments", idp="SHP-",
         orgs=["Meridian Freight", "BlueHarbor Logistics", "Quickline Parcels", "Northstar Courier"],
         intros=["{org} is investigating late shipment {id}: {detail}.",
                 "Shipment {id} handled by {org} arrived late ({detail}).",
                 "A customer escalated shipment {id} to {org} - {detail}."],
         details=["a parcel of kitchen equipment four days overdue", "a replacement laptop two days late",
                  "a box of spare parts delivered a week late", "a pallet of books that missed its slot"],
         outcomes=[
             _O("Carrier delay", "carrier delays", "the carrier's line-haul network ran behind",
                "The customer's complaint blames \"the useless courier\"."),
             _O("Customs hold", "customs holds", "the parcel was held for customs checks",
                "The parcel contains a perfume bottle, which the customer mentioned twice."),
             _O("Warehouse mis-pick", "warehouse mis-picks", "the wrong item or parcel left the warehouse",
                "The packing slip has a handwritten correction."),
             _O("Weather disruption", "weather disruptions", "storms or snow closed routes",
                "There was a named storm on the news that week."),
             _O("Address error", "address errors", "the address was incomplete or wrong",
                "The customer's street name is unusually long."),
         ],
         signals=[
             _S("a missing export scan", "had a missing export scan", "The tracking history has no export scan.",
                "The tracking history includes an export scan."),
             _S("a 'held at facility' status", "showed a 'held at facility' status",
                "Tracking shows 'held at facility'.", "Tracking never showed 'held at facility'."),
             _S("a delivery re-attempt", "included a delivery re-attempt", "A delivery re-attempt was logged.",
                "No delivery re-attempt was logged."),
             _S("other late parcels on the same route", "coincided with other late parcels on the same route",
                "Other parcels on the same route were also late.", "No other parcels on the same route were late."),
             _S("a label reprint", "involved a label reprint", "The label was reprinted at dispatch.",
                "The label was never reprinted."),
         ],
         gates=[
             _GD("were shipped", "shipped", "the order date", "after", [2, 3, 5],
                 ["Ordered: {d1}. Shipped: {d2}.", "The order was placed on {d1} and left the warehouse on {d2}."]),
             _GQ("mass", "involved parcels weighing", "parcel weighing", "", [(10, "kg"), (20, "lb"), (5, "kg")],
                 ["kg", "lb", "g"], ["The parcel weighs {V}.", "Declared parcel weight: {V}."]),
             _GQ("length", "were bound for addresses", "address", " from the depot",
                 [(50, "km"), (30, "mi"), (100, "km")], ["km", "mi"],
                 ["The delivery address is {V} from the depot."]),
         ],
         tool=dict(name="the customs-risk screener", verb="flagged", inf="flag", target=1),
         clf="the exceptions triage model",
         channel=_CH("a driver's handheld comment", "drivers' handheld comments",
                     "it is backed by a timestamped photo", "The comment is backed by a timestamped photo.",
                     "There is no photo attached to the comment.",
                     "the photo's GPS tag is more than 1 km from the delivery address",
                     "The photo's GPS tag is 3.4 km from the delivery address.",
                     "The photo's GPS tag matches the delivery address."),
         ref=dict(broad="all late shipments network-wide", sub="late shipments leaving the Rotterdam hub",
                  member="The parcel left from the Rotterdam hub."),
         segs=["domestic same-day parcels", "freight pallets", "returns traffic"],
         filler=[("Liability", "Carrier liability is limited to the declared value or $100, whichever is lower, "
                               "unless extra cover was bought."),
                 ("Claims window", "Loss or damage claims must be lodged within 21 days of the expected delivery date."),
                 ("Dangerous goods", "Lithium batteries shipped separately from equipment require a UN3480 label.")]),
    dict(key="manufacturing", what="source of the defect", case="defective unit", cases="defective units", idp="QA-",
         orgs=["Vantage Plastics", "Corwin Components", "Halden Moulding", "Apex Housings"],
         intros=["{org} quality engineering opened {id} for {detail}.",
                 "Defect report {id} at {org}: {detail}.",
                 "Customer return {id} reached {org} QA - {detail}."],
         details=["a cracked 40 mm housing", "a warped battery cover", "a connector shell that would not latch",
                  "a lid with a visible sink mark"],
         outcomes=[
             _O("Line A press", "defects from the Line A press", "the Line A injection press was out of setting",
                "The defect was logged by the Line A shift lead, who is known for sloppy paperwork."),
             _O("Supplier resin batch", "defects traced to a supplier resin batch", "the raw resin was out of spec",
                "A supplier representative visited the plant the day before."),
             _O("Mold wear", "defects caused by mold wear", "the mold cavity is worn",
                "The mold involved is the oldest one on the floor."),
             _O("Operator setup error", "operator setup errors", "the machine was set up wrongly at changeover",
                "The night shift had two new operators that week."),
             _O("Transit damage", "transit-damage cases", "the part was damaged after leaving the plant",
                "The customer's photo shows a crushed outer carton."),
         ],
         signals=[
             _S("surface bubbles", "showed surface bubbles", "The unit shows surface bubbles.",
                "The unit shows no surface bubbles."),
             _S("a changeover within the prior two hours", "followed a changeover within the prior two hours",
                "The unit was made within two hours of a changeover.",
                "The unit was not made within two hours of a changeover."),
             _S("defects in consecutive serial numbers", "appeared in consecutive serial numbers",
                "Neighbouring serial numbers have the same defect.",
                "Neighbouring serial numbers are defect-free."),
             _S("a clean final-inspection record", "had a clean final-inspection record",
                "The unit passed final inspection cleanly.", "The unit's final-inspection record has a note on it."),
             _S("flash along the parting line", "had flash along the parting line",
                "There is flash along the parting line.", "There is no flash along the parting line."),
         ],
         gates=[
             _GQ("length", "had a dimensional deviation of", "dimensional deviation of", "",
                 [(F(1, 2), "mm"), (F(3, 10), "mm"), (1, "mm")], ["mm", "cm"],
                 ["Measured deviation: {V}.", "The unit is out of tolerance by {V}."]),
             _GQ("time", "were made", "made", " after the last mold cleaning",
                 [(48, "hours"), (3, "days"), (36, "hours")], ["hours", "days"],
                 ["The unit was made {V} after the last mold cleaning."]),
         ],
         tool=dict(name="the vision inspection system", verb="flagged", inf="flag", target=2),
         clf="the defect-classification network",
         channel=_CH("a customer's description", "customers' descriptions",
                     "it is confirmed by a returned sample", "A returned sample confirms the description.",
                     "No sample has been returned.", "the returned sample arrived without its original packaging",
                     "The sample arrived loose, without its original packaging.",
                     "The sample arrived in its original packaging."),
         ref=dict(broad="all defects plant-wide", sub="defects on the 40 mm housing family",
                  member="The unit belongs to the 40 mm housing family."),
         segs=["metal stamping", "assembly line 3", "packaging"],
         filler=[("Tolerances", "Unless the drawing says otherwise, general tolerances follow ISO 2768-m."),
                 ("Containment", "Suspect stock is quarantined in the red cage until QA signs a release."),
                 ("Calibration", "Gauges are calibrated every six months; overdue gauges must not be used.")]),
    dict(key="retail_returns", what="reason for the return", case="return", cases="returns", idp="RMA-",
         orgs=["Marlowe & Finch", "Tidewater Outfitters", "Loomhouse", "Ardent Apparel"],
         intros=["{org} is auditing return {id}: {detail}.", "Return {id} came back to {org} - {detail}.",
                 "The returns desk at {org} escalated {id} ({detail})."],
         details=["a formal evening dress bought online", "a silk blouse", "a wool coat",
                  "a designer handbag"],
         outcomes=[
             _O("Genuine defect", "returns for a genuine defect", "the item was faulty",
                "The customer wrote a furious one-star review the same day."),
             _O("Wrong size or fit", "returns for wrong size or fit", "the item did not fit",
                "The customer mentioned she is \"between sizes\"."),
             _O("Changed mind", "changed-mind returns", "the customer simply no longer wanted it",
                "The customer bought three similar items in one order."),
             _O("Wardrobing", "wardrobing returns", "the item was worn once and then returned",
                "The order was placed two days before a big wedding weekend."),
             _O("Damaged in transit", "transit-damage returns", "the item was damaged on the way",
                "The courier for that area had complaints last month."),
         ],
         signals=[
             _S("tags removed", "came back with the tags removed", "The item came back with the tags removed.",
                "The item came back with the tags attached."),
             _S("a return reason of 'defective'", "were logged by the customer as 'defective'",
                "The customer selected 'defective' as the reason.", "The customer did not select 'defective'."),
             _S("the original packaging", "came back in the original packaging",
                "The item came back in the original packaging.", "The original packaging is missing."),
             _S("a first-time customer", "came from first-time customers", "This is the customer's first order.",
                "The customer has ordered before."),
             _S("perfume or makeup traces", "had perfume or makeup traces", "There are perfume or makeup traces.",
                "There are no perfume or makeup traces."),
         ],
         gates=[
             _GD("were returned", "returned", "delivery", "after", [14, 30, 45],
                 ["Delivered: {d1}. Return received: {d2}.",
                  "The order was delivered on {d1}; the return arrived on {d2}."]),
         ],
         tool=dict(name="the returns-abuse model", verb="flagged", inf="flag", target=3),
         clf="the returns-reason classifier",
         channel=_CH("a store associate's comment", "store associates' comments",
                     "it is supported by an inspection photo", "An inspection photo supports the comment.",
                     "No inspection photo was taken.", "the associate is the one who originally sold the item",
                     "The associate is the one who sold the item.", "The associate did not sell the item."),
         ref=dict(broad="all returns", sub="returns of formalwear", member="The item is from the formalwear range."),
         segs=["electronics", "home goods", "kitchenware"],
         filler=[("Refund method", "Refunds go back to the original payment method within 5-7 business days."),
                 ("Final sale", "Items marked final sale cannot be returned unless faulty."),
                 ("Exchanges", "Exchanges for a different size are free for loyalty members.")]),
    dict(key="hr_attrition", what="main reason for leaving", case="departure", cases="departures", idp="HR-",
         orgs=["Solace Software", "Brindle Analytics", "Kestrel Engineering", "Juniper Retail Group"],
         intros=["People Analytics at {org} is classifying departure {id}: {detail}.",
                 "Departure {id} at {org} ({detail}) needs a primary reason code.",
                 "HR at {org} is reviewing exit file {id} - {detail}."],
         details=["a senior engineer who resigned after four years", "a product manager who left after 18 months",
                  "a data analyst who resigned during probation", "a team lead who left after six years"],
         outcomes=[
             _O("Compensation", "departures driven by compensation", "pay was the main driver",
                "The employee recently asked a colleague what she earns."),
             _O("Manager relationship", "departures driven by the manager relationship",
                "friction with the line manager", "The employee skipped the last two one-to-ones."),
             _O("Career growth", "departures driven by career growth", "no route to the next role",
                "The employee just finished an evening MBA."),
             _O("Relocation", "departures due to relocation", "the employee moved away",
                "The employee's partner got a job offer in another city."),
             _O("Workload/burnout", "burnout-driven departures", "sustained overwork",
                "The employee sent emails after midnight three nights running."),
         ],
         signals=[
             _S("pay below the band midpoint", "involved employees paid below their band midpoint",
                "The employee was paid below the band midpoint.", "The employee was paid above the band midpoint."),
             _S("a manager change in the last six months", "followed a manager change in the last six months",
                "The employee's manager changed in the last six months.",
                "The employee's manager did not change in the last six months."),
             _S("no promotion in three years", "involved employees with no promotion in three years",
                "The employee had not been promoted in three years.",
                "The employee was promoted within the last three years."),
             _S("a declined remote-work request", "followed a declined remote-work request",
                "A remote-work request from the employee was declined.",
                "The employee never had a remote-work request declined."),
             _S("above-average overtime", "involved above-average overtime",
                "The employee's overtime was above average.", "The employee's overtime was below average."),
         ],
         gates=[
             _GD("handed in notice", "notice handed in", "their last performance review", "after", [14, 30, 60],
                 ["Last performance review: {d1}. Notice handed in: {d2}.",
                  "The last review took place on {d1}; notice was handed in on {d2}."]),
             _GQ("time", "had logged overtime of", "overtime of", " in their final month",
                 [(20, "hours"), (15, "hours"), (2, "days")], ["hours", "minutes"],
                 ["Overtime logged in the final month: {V}."]),
         ],
         tool=dict(name="the engagement-survey attrition score", verb="flagged", inf="flag", target=4),
         clf="the exit-interview text classifier",
         channel=_CH("an anonymous peer comment", "anonymous peer comments",
                     "it was confirmed in the exit interview", "The exit interview confirmed it.",
                     "The exit interview did not touch on it.",
                     "the exit interview was conducted by the employee's own manager",
                     "The exit interview was run by the employee's own manager.",
                     "The exit interview was run by an HR partner from another division."),
         ref=dict(broad="all voluntary departures", sub="departures from the engineering organisation",
                  member="The employee worked in platform engineering."),
         segs=["sales", "customer support", "finance"],
         filler=[("Notice periods", "Notice is one month for most roles and three months for directors."),
                 ("Garden leave", "Garden leave may be applied at the company's discretion."),
                 ("Rehire", "Former employees in good standing may reapply after six months.")]),
    dict(key="privacy_dlp", what="explanation for the alert", case="DLP alert", cases="DLP alerts", idp="DLP-",
         orgs=["Fenwick Health Systems", "Castell Insurance Group", "Orbital Payments", "Greystone Legal"],
         intros=["The security team at {org} is triaging alert {id}: {detail}.",
                 "Data-loss-prevention alert {id} fired at {org} - {detail}.",
                 "{org}'s privacy office asked for a view on alert {id} ({detail})."],
         details=["a large upload from a finance laptop", "a spreadsheet sent to an external address",
                  "a bulk export from the CRM", "an archive synced to a cloud drive"],
         outcomes=[
             _O("Data exfiltration", "genuine exfiltration events", "someone deliberately took data out",
                "The user recently complained loudly about a missed bonus."),
             _O("Misconfigured sync", "misconfigured sync jobs", "a backup or sync tool was set up wrongly",
                "The IT channel mentions a new backup tool rollout."),
             _O("Authorized transfer", "authorized transfers", "an approved business transfer",
                "The file name includes the word \"APPROVED\"."),
             _O("Test data", "test-data alerts", "synthetic or test records tripped the rule",
                "The file name starts with \"test_\"."),
         ],
         signals=[
             _S("an off-hours transfer", "happened outside working hours", "The transfer happened at 02:14.",
                "The transfer happened during working hours."),
             _S("a personal cloud destination", "went to a personal cloud-storage account",
                "The destination is a personal cloud-storage account.",
                "The destination is not a personal cloud-storage account."),
             _S("a matching change ticket", "had a matching change ticket", "There is a matching change ticket.",
                "There is no matching change ticket."),
             _S("customer records in the payload", "contained customer records",
                "The payload contains customer records.", "The payload contains no customer records."),
             _S("a first-time destination", "used a destination never seen before",
                "The destination has never been seen before.", "The destination has been used before."),
         ],
         gates=[
             _GQ("data", "involved transfers of", "transfer of", "", [(500, "MB"), (2, "GB"), (750, "MB")],
                 ["MB", "GB"], ["Transfer size: {V}.", "The flagged upload was {V}."]),
             _GD("occurred", "occurring", "the user's resignation notice", "after", [7, 14, 30],
                 ["Resignation notice given: {d1}. Transfer date: {d2}.",
                  "The user gave notice on {d1}; the transfer happened on {d2}."]),
         ],
         tool=dict(name="the UEBA anomaly model", verb="flagged", inf="flag", target=0),
         clf="the SOC triage assistant",
         channel=_CH("a tip from a co-worker", "tips from co-workers", "it was verified against access logs",
                     "The tip was verified against access logs.", "The tip has not been checked against any logs.",
                     "the verification used logs from a system with known clock skew",
                     "The logs used for verification come from a server with known clock skew.",
                     "The logs used for verification come from a correctly synced server."),
         ref=dict(broad="all DLP alerts", sub="DLP alerts from the finance department",
                  member="The user sits in the finance department (accounts payable)."),
         segs=["email DLP", "USB device control", "print monitoring"],
         filler=[("Breach notification", "Where personal data is confirmed lost, the regulator must be told within "
                                         "72 hours of the organisation becoming aware."),
                 ("Legal hold", "Mailboxes under legal hold must not be purged, even by retention policies."),
                 ("Encryption", "Removable media must be encrypted to the company standard.")]),
    dict(key="admissions", what="decision", case="admitted applicant", cases="admitted applicants", idp="ADM-",
         orgs=["Westbrook University", "Halvorsen College", "St. Aldric Institute", "Coastal State University"],
         intros=["The enrolment office at {org} is forecasting the decision of applicant {id}: {detail}.",
                 "Applicant {id} was admitted to {org} ({detail}).",
                 "{org} is predicting yield for admit {id} - {detail}."],
         details=["an engineering admit with a partial scholarship", "a biology admit from out of state",
                  "a music admit on the early round", "a business admit from the waitlist"],
         outcomes=[
             _O("Enrolls", "admits who enrolled", "the applicant accepts and enrols",
                "The applicant posted \"dream school!!\" on social media two years ago."),
             _O("Declines for another school", "admits who declined for another school",
                "the applicant goes elsewhere", "The applicant's essay praised a rival university's lab."),
             _O("Defers a year", "admits who deferred a year", "the applicant takes a gap year",
                "The applicant mentioned wanting to travel."),
             _O("Declines for cost", "admits who declined because of cost", "money is the deciding factor",
                "The applicant asked about part-time jobs on campus."),
         ],
         signals=[
             _S("a campus visit after admission", "visited campus after admission",
                "The applicant visited campus after being admitted.",
                "The applicant has not visited campus since being admitted."),
             _S("a financial-aid appeal", "filed a financial-aid appeal", "The applicant filed a financial-aid appeal.",
                "The applicant has not filed a financial-aid appeal."),
             _S("an opened housing application", "opened a housing application",
                "The applicant opened a housing application.", "The applicant has not opened a housing application."),
             _S("an offer from a higher-ranked school", "also held an offer from a higher-ranked school",
                "The applicant also holds an offer from a higher-ranked school.",
                "The applicant holds no offer from a higher-ranked school."),
             _S("attendance at the admitted-students webinar", "attended the admitted-students webinar",
                "The applicant attended the admitted-students webinar.",
                "The applicant skipped the admitted-students webinar."),
         ],
         gates=[
             _GD("first replied", "first reply", "the offer", "after", [7, 10, 14],
                 ["Offer sent: {d1}. First reply from the applicant: {d2}.",
                  "The offer went out on {d1}; the applicant first replied on {d2}."]),
             _GQ("length", "lived", "living", " from campus", [(300, "km"), (200, "mi"), (500, "km")],
                 ["km", "mi"], ["The applicant lives {V} from campus."]),
         ],
         tool=dict(name="the yield model's 'likely enroller' tag", verb="flagged", inf="flag", target=0),
         clf="the counsellor-notes classifier",
         channel=_CH("a comment from the applicant's school counsellor", "comments from school counsellors",
                     "the applicant confirmed it in writing", "The applicant confirmed it in writing.",
                     "The applicant has not confirmed it.",
                     "the written confirmation came before the financial-aid offer was issued",
                     "The written confirmation predates the financial-aid offer.",
                     "The written confirmation came after the financial-aid offer."),
         ref=dict(broad="all admitted applicants", sub="admitted international applicants",
                  member="The applicant lives in Singapore and applied as an international student."),
         segs=["graduate programmes", "transfer students", "the summer school"],
         filler=[("Deposit deadline", "The enrolment deposit is due by 1 May and is non-refundable after 15 June."),
                 ("Deferral rules", "Deferrals are granted for one year only and require a written plan."),
                 ("Housing", "First-year students are guaranteed housing if they apply by 1 June.")]),
    dict(key="travel_expenses", what="explanation", case="flagged expense", cases="flagged expenses", idp="EXP-",
         orgs=["Barrow & Kline", "Tessellate Consulting", "Northfield Pharma", "Quarry Media"],
         intros=["Finance at {org} is reviewing expense line {id}: {detail}.",
                 "Expense {id} was flagged by {org}'s audit rules - {detail}.",
                 "An auditor at {org} picked expense {id} for review ({detail})."],
         details=["a $412 client dinner in Chicago", "a $96 taxi ride in Berlin", "a $1,180 hotel folio in Singapore",
                  "a $238 mileage claim"],
         outcomes=[
             _O("Compliant expense", "compliant expenses", "a legitimate business cost within policy",
                "The employee is a senior director who travels constantly."),
             _O("Personal expense misfiled", "personal expenses filed by mistake",
                "a private cost submitted as business", "The receipt is from a restaurant near the employee's home."),
             _O("Duplicate submission", "duplicate submissions", "the same cost claimed twice",
                "IT says the expense app crashed several times that week."),
             _O("Inflated receipt", "inflated receipts", "the receipt amount was padded",
                "The receipt is handwritten."),
         ],
         signals=[
             _S("a weekend date", "were dated on a weekend", "The expense is dated on a Saturday.",
                "The expense is dated on a weekday."),
             _S("a round-number total", "had a round-number total", "The total is a round number.",
                "The total is not a round number."),
             _S("no matching card transaction", "had no matching corporate-card transaction",
                "There is no matching corporate-card transaction.", "There is a matching corporate-card transaction."),
             _S("the same amount claimed twice in the month", "matched another claim of the same amount that month",
                "Another claim for the same amount was filed that month.",
                "No other claim for the same amount was filed that month."),
             _S("a vendor outside the trip city", "came from a vendor outside the trip city",
                "The vendor is outside the trip city.", "The vendor is in the trip city."),
         ],
         gates=[
             _GD("were submitted", "submitted", "the end of the trip", "after", [30, 60, 90],
                 ["Trip ended: {d1}. Expense submitted: {d2}.",
                  "The trip ended on {d1}, and the expense was submitted on {d2}."]),
             _GQ("length", "claimed a driving distance of", "claimed distance of", "",
                 [(200, "km"), (100, "mi"), (150, "km")], ["km", "mi"], ["Claimed driving distance: {V}."]),
         ],
         tool=dict(name="the duplicate detector", verb="flagged", inf="flag", target=2),
         clf="the expense-audit classifier",
         channel=_CH("a remark from the employee's travel companion", "remarks from travel companions",
                     "the remark matches the hotel folio", "The remark matches the hotel folio.",
                     "The remark has not been checked against the hotel folio.",
                     "the hotel folio was supplied by the employee rather than by the hotel",
                     "The folio was supplied by the employee.", "The folio came directly from the hotel."),
         ref=dict(broad="all flagged expenses", sub="flagged meal expenses",
                  member="The expense is filed under 'Meals'."),
         segs=["airfare", "car rental", "conference fees"],
         filler=[("Per diem", "Meal per diems follow the published city rates; alcohol is never reimbursable."),
                 ("Receipts", "Receipts are required for every item above $25."),
                 ("Approvals", "Expenses above $2,500 need a second approver.")]),
    dict(key="public_benefits", what="processing outcome", case="benefit application",
         cases="benefit applications", idp="BEN-",
         orgs=["the State Department of Human Services", "the County Benefits Office", "the Regional Assistance Agency"],
         intros=["{org} is triaging application {id}: {detail}.", "Application {id} reached {org} - {detail}.",
                 "A caseworker at {org} is forecasting the outcome of application {id} ({detail})."],
         details=["a food-assistance application from a household of four", "an emergency rental-assistance request",
                  "a child-care subsidy application", "an energy-assistance application"],
         outcomes=[
             _O("Approve", "applications that were approved", "the household qualifies",
                "The applicant has three young children."),
             _O("Deny - income over limit", "applications denied for income over the limit",
                "household income is above the limit", "The applicant drives a fairly new car."),
             _O("Request missing documents", "applications returned for missing documents",
                "the file is incomplete", "The upload portal was slow on the day of submission."),
             _O("Refer for fraud review", "applications referred for fraud review",
                "possible misrepresentation", "The applicant's email address has lots of numbers in it."),
         ],
         signals=[
             _S("a gap in employment history", "showed a gap in employment history",
                "There is a gap in the employment history.", "There is no gap in the employment history."),
             _S("self-reported income only", "relied on self-reported income only",
                "Income is self-reported only.", "Income is backed by pay stubs."),
             _S("a household-size change", "reported a household-size change",
                "The household size changed this year.", "The household size is unchanged."),
             _S("a mismatch with the wage database", "had a mismatch with the state wage database",
                "The wage database shows a mismatch.", "The wage database matches the application."),
             _S("a previous application in the prior 12 months", "had a previous application in the prior 12 months",
                "There was a previous application in the prior 12 months.",
                "There was no previous application in the prior 12 months."),
         ],
         gates=[
             _GD("were submitted", "submitted", "the qualifying event", "after", [30, 60, 90],
                 ["Qualifying event (job loss): {d1}. Application submitted: {d2}.",
                  "The job loss happened on {d1}; the application was submitted on {d2}."]),
             _GQ("time", "reported weekly work hours of", "weekly work hours of", "",
                 [(20, "hours"), (30, "hours")], ["hours", "minutes"], ["Reported work per week: {V}."]),
         ],
         tool=dict(name="the income-verification check", verb="flagged", inf="flag", target=1),
         clf="the caseworker assist model",
         channel=_CH("a landlord's letter", "landlords' letters", "it is notarized", "The letter is notarized.",
                     "The letter is not notarized.", "the landlord is related to the applicant",
                     "The landlord is the applicant's uncle.", "The landlord is not related to the applicant."),
         ref=dict(broad="all applications statewide", sub="applications from rural counties",
                  member="The applicant lives in Harlan County, which is classed as rural."),
         segs=["disability benefits", "unemployment insurance", "housing vouchers"],
         filler=[("Appeals", "Applicants may appeal a denial within 90 days of the notice date."),
                 ("Interpreters", "Free interpreters are available for interviews in any language."),
                 ("Recertification", "Approved households recertify every 12 months.")]),
    dict(key="telecom", what="cause", case="dropped-call complaint", cases="dropped-call complaints", idp="TKT-",
         orgs=["Vireo Mobile", "Crestline Telecom", "Polar Wireless", "Summit Networks"],
         intros=["{org} customer care escalated ticket {id}: {detail}.", "Ticket {id} at {org} - {detail}.",
                 "A network engineer at {org} is diagnosing complaint {id} ({detail})."],
         details=["a customer reports calls dropping several times a day",
                  "a small business says calls cut out mid-sentence",
                  "a customer cannot complete calls longer than a minute or two",
                  "a family reports dropped calls on two phones"],
         outcomes=[
             _O("Tower congestion", "complaints caused by tower congestion", "the cell site is overloaded",
                "The customer lives next to a football stadium."),
             _O("Handset fault", "complaints caused by a handset fault", "the phone itself is faulty",
                "The customer's phone is a five-year-old model."),
             _O("Coverage gap", "complaints caused by a coverage gap", "the signal is too weak where they are",
                "The customer's house is at the end of a long valley road."),
             _O("SIM provisioning error", "SIM provisioning errors", "the SIM or line is set up wrongly",
                "The customer switched plans last week."),
             _O("Wi-Fi calling misconfiguration", "Wi-Fi calling misconfigurations",
                "calls are handed to a badly set up Wi-Fi calling path",
                "The customer recently bought a new router."),
         ],
         signals=[
             _S("drops only at peak hours", "dropped calls only at peak hours", "Calls drop only at peak hours.",
                "Calls drop at all times of day."),
             _S("drops on a second handset too", "also dropped calls on a second handset",
                "A second handset on the same line drops calls too.",
                "A second handset on the same line works fine."),
             _S("a recent SIM swap", "had a recent SIM swap", "The SIM was swapped recently.",
                "The SIM has not been swapped recently."),
             _S("neighbours reporting the same problem", "coincided with neighbours reporting the same problem",
                "Neighbours report the same problem.", "No neighbours report the problem."),
             _S("drops only indoors", "dropped calls only indoors", "Calls drop only indoors.",
                "Calls drop outdoors as well."),
         ],
         gates=[
             _GQ("length", "came from addresses", "address", " from the nearest tower",
                 [(5, "km"), (3, "mi"), (2, "km")], ["km", "mi", "m"],
                 ["The customer is {V} from the nearest tower."]),
             _GQ("time", "had calls dropping after", "calls dropping after", "",
                 [(90, "seconds"), (2, "minutes"), (45, "seconds")], ["seconds", "minutes"],
                 ["Calls typically drop after {V}."]),
         ],
         tool=dict(name="the network-analytics congestion alarm", verb="flagged", inf="flag", target=0),
         clf="the care-ticket classifier",
         channel=_CH("the customer's own diagnosis", "customers' own diagnoses",
                     "it was confirmed by a field technician", "A field technician confirmed it.",
                     "No technician has looked at it.", "the technician tested only on the customer's Wi-Fi",
                     "The technician tested only on the customer's Wi-Fi.",
                     "The technician tested on the mobile network."),
         ref=dict(broad="all dropped-call complaints", sub="complaints on 5G-only plans",
                  member="The customer is on a 5G-only plan."),
         segs=["fixed broadband", "business lines", "prepaid"],
         filler=[("Credits", "Customers with a confirmed network fault get a one-month service credit."),
                 ("Porting", "Number porting completes within one business day."),
                 ("Fair use", "Unlimited plans are subject to the fair-use policy above 300 GB a month.")]),
    dict(key="login_security", what="explanation", case="suspicious-login alert", cases="suspicious-login alerts",
         idp="SEC-",
         orgs=["Halcyon Bank", "Tern Logistics", "Mosaic Health", "Ironwood Energy"],
         intros=["The SOC at {org} is triaging alert {id}: {detail}.", "Alert {id} fired at {org} - {detail}.",
                 "Identity protection at {org} raised {id} ({detail})."],
         details=["a sign-in to a finance user's mailbox from a new country",
                  "a VPN login followed by a password reset", "two logins 40 minutes apart on different continents",
                  "a sign-in from an unmanaged device"],
         outcomes=[
             _O("Account takeover", "account takeovers", "an attacker controls the account",
                "An old helpdesk ticket shows the user once used the password \"Summer2024!\"."),
             _O("User travelling", "travelling users", "the real user is abroad",
                "The user's calendar shows a conference that week."),
             _O("VPN or proxy", "logins through a VPN or proxy", "the real user routed through a VPN",
                "The user works in the privacy team."),
             _O("Shared or new device", "logins from a shared or new device", "the real user on unfamiliar hardware",
                "The user's laptop was sent for repair last month."),
         ],
         signals=[
             _S("an impossible-travel pattern", "showed an impossible-travel pattern",
                "The logins form an impossible-travel pattern.", "The logins do not form an impossible-travel pattern."),
             _S("repeated MFA prompts", "involved repeated MFA prompts", "The user received repeated MFA prompts.",
                "There were no repeated MFA prompts."),
             _S("a new device fingerprint", "came from a new device fingerprint", "The device fingerprint is new.",
                "The device fingerprint has been seen before."),
             _S("a known VPN exit IP", "came from a known VPN exit IP", "The IP is a known VPN exit node.",
                "The IP is not a known VPN exit node."),
             _S("a mailbox-rule change after login", "were followed by a mailbox-rule change",
                "A mailbox rule was changed after the login.", "No mailbox rule was changed after the login."),
         ],
         gates=[
             _GQ("length", "originated", "originating", " from the user's usual location",
                 [(500, "km"), (300, "mi"), (1000, "km")], ["km", "mi"],
                 ["The login came from {V} away from the user's usual location."]),
             _GQ("time", "had a gap between consecutive logins of", "gap between consecutive logins of", "",
                 [(2, "hours"), (90, "minutes"), (1, "hours")], ["hours", "minutes"],
                 ["Time between the two logins: {V}."]),
         ],
         tool=dict(name="the identity-protection risk engine", verb="flagged", inf="flag", target=0),
         clf="the SOC triage assistant",
         channel=_CH("the user's own explanation", "users' own explanations",
                     "it was verified through a call-back to the user's registered phone number",
                     "It was verified through a call-back to the registered number.",
                     "Nobody has called the user back.", "the registered phone number was changed in the last 7 days",
                     "The registered number was changed four days ago.",
                     "The registered number has not changed in over a year."),
         ref=dict(broad="all suspicious-login alerts", sub="alerts on executive accounts",
                  member="The account belongs to the CFO."),
         segs=["service accounts", "contractor accounts", "API keys"],
         filler=[("Containment", "Disabling an account requires a ticket number and a second analyst's approval."),
                 ("Evidence handling", "Export sign-in logs before resetting anything; resets overwrite session data."),
                 ("User comms", "Never ask users for their password or MFA codes.")]),
]

_GENERIC_FILLER = [
    ("Confidentiality", "This file contains internal information. Do not forward it outside the review team, and do "
                        "not paste case details into personal messaging apps."),
    ("Records retention", "Working notes are kept for seven years after closure and then destroyed under the records "
                          "schedule. Drafts that were never circulated may be deleted earlier."),
    ("Escalation contacts", "Weekday questions go to the duty lead. After 18:00 and at weekends, use the on-call rota; "
                            "the rota is published every Friday afternoon."),
    ("Glossary", "'Base rate' means the share of comparable past cases in each category before looking at anything "
                 "specific to this case. A 'signal' is an observable fact that is more common in some categories "
                 "than in others."),
    ("Unrelated meeting note", "The quarterly staffing review has moved to Thursday at 14:00. Please update the shared "
                               "calendar and send apologies to the chair if you cannot attend."),
    ("Change log", "v3.2 fixed a typo in the appendix; v3.1 re-ordered two sections. Neither revision changed any "
                   "figure used in this review."),
    ("Accessibility", "This material is available in large print or as plain text on request. Contact the methods "
                      "team with at least two working days' notice."),
    ("Training reminder", "All reviewers must complete the annual data-handling module before the end of the quarter. "
                          "Completion is tracked automatically."),
    ("Quality sampling", "Five percent of closed files are re-reviewed by a second analyst. Disagreements are logged "
                         "for calibration but do not reopen the file."),
    ("Dashboard note", "The dashboard refreshes every 15 minutes, so figures quoted in chat can lag by one refresh. "
                       "The figures in this file were exported directly and are not affected."),
    ("Holiday cover", "During the end-of-year closure, turnaround targets are paused and resume on the first working "
                      "day of January."),
    ("Template feedback", "Suggestions for improving this template can be sent to the methods team; they are "
                          "reviewed once a month."),
    ("System maintenance", "The case-management system will be offline for maintenance on Sunday between 01:00 and "
                           "04:00. Save drafts before then."),
    ("Office logistics", "The third-floor meeting rooms are being refurbished; bookings have moved to the second floor "
                         "until further notice."),
    ("Privacy reminder", "Only use the minimum personal data needed for a decision. Do not copy identifiers into "
                         "free-text fields that are shared with vendors."),
    ("Audit trail", "Every change to a case record is time-stamped and attributed. Edits made while logged in as "
                    "another user are a disciplinary matter."),
    ("Service levels", "Standard reviews should be completed within five working days and complex reviews within ten. "
                       "The clock pauses while waiting for third-party documents."),
    ("Naming conventions", "Attachments should be named with the case number first, then the document type, then the "
                           "date in YYYY-MM-DD format."),
]

_FIRST = ["Alex", "Priya", "Jordan", "Mei", "Tomas", "Aisha", "Ben", "Chloe", "Dmitri", "Elena", "Farid", "Grace",
          "Hiro", "Ines", "Jonas", "Kemi", "Liam", "Maya", "Nikhil", "Olivia", "Pedro", "Rosa", "Sam", "Tariq",
          "Uma", "Victor", "Wen", "Yara", "Zoe"]
_LAST = ["Diaz", "Okafor", "Chen", "Novak", "Patel", "Schmidt", "Haddad", "Kim", "Moreau", "Silva", "Ivanova",
         "Brennan", "Tanaka", "Osei", "Larsen", "Rossi", "Nguyen", "Kowalski", "Mensah", "Ortiz"]
_JUNIOR = ["a trainee analyst", "a summer intern", "a new hire still in onboarding",
           "a temp contractor without sign-off rights", "a first-week associate", "a student on placement"]
_QUAL = ["not authorized to sign off", "unreviewed", "not an approved reviewer", "informal comment, no sign-off authority",
         "pending supervisor review"]
_ODDS = [(4, 1), (3, 1), (9, 1), (3, 2), (7, 3), (19, 1), (3, 2), (4, 1), (7, 3)]

_FLAG_NAMES = [
    ("noexc2", "missed the exception to the exception"),
    ("noexc", "missed the exception"),
    ("norule", "used evidence the rules exclude"),
    ("old", "used superseded figure"),
    ("ref", "wrong reference class"),
    ("offbyone", "off-by-one boundary"),
    ("unit", "unit mix-up"),
    ("odds", "read odds as probability"),
    ("complement", "treated absent signal as present"),
    ("lik_only", "base-rate neglect"),
    ("prior_only", "ignored the evidence"),
]
_TRAP_FLAGS = ("norule", "noexc", "noexc2", "old", "ref", "offbyone", "unit", "odds", "complement")
_DIST_EXTRA = [("double", "double-counted evidence"), ("avg", "averaged prior and evidence")]

# bucket scales: (cuts, labels)
_SCALES = [
    ([F(1, 10), F(3, 10), F(7, 10), F(9, 10)], ["Very unlikely", "Unlikely", "Uncertain", "Likely", "Very likely"]),
    ([F(1, 20), F(1, 4), F(1, 2), F(3, 4), F(19, 20)], ["Remote", "Low", "Moderate", "Elevated", "High",
                                                        "Near-certain"]),
    ([F(1, 5), F(2, 5), F(3, 5), F(4, 5)], ["Low", "Moderately low", "Even", "Moderately high", "High"]),
    ([F(1, 4), F(1, 2), F(3, 4)], ["Unlikely", "Possible", "Probable", "Highly likely"]),
    ([F(1, 3), F(2, 3)], ["Low", "Medium", "High"]),
    ([F(1, 10), F(1, 4), F(1, 2)], ["Negligible", "Low", "Moderate", "High"]),
]
_THRESH = [F(x, 100) for x in (5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 65, 70, 75, 80, 90)]


def _boundary_table():
    tab = {}
    for p in range(5, 96, 5):
        for s in list(range(50, 100, 5)) + [98, 99]:
            for f in range(1, 50):
                if f >= s:
                    continue
                P, S, Fp = F(p, 100), F(s, 100), F(f, 100)
                post = P * S / (P * S + (1 - P) * Fp)
                tab.setdefault(post, []).append((p, s, f))
    return tab


_BOUNDARY = _boundary_table()


# =========================================================================
# engine: gates, rules, posterior (primary exact path)
# =========================================================================
def _gate_value(g, naive=False):
    if g["type"] == "days":
        return F((g["d2"] - g["d1"]).days)
    if naive:
        return g["v"]
    U = _UNITS[g["dim"]]
    return g["v"] * U[g["uv"]] / U[g["uT"]]


def _gate_true(g, flip=False, naive=False):
    op = _FLIP[g["op"]] if flip else g["op"]
    return _cmp(_gate_value(g, naive), g["T"], op)


def _rule_eval(depth, A, B):
    if depth == 1:
        return False
    if depth == 2:
        return A
    return A and not B


def _included(P, ev, flags):
    if not ev.get("channel"):
        return True
    if "norule" in flags:
        return True
    r = P["rule"]
    depth = r["depth"]
    if "noexc" in flags:
        depth = 1
    elif "noexc2" in flags:
        depth = min(depth, 2)
    return _rule_eval(depth, r["A"], r["B"])


def _ev_vector(ev, flags):
    lik = ev["lik"]
    if "old" in flags and ev.get("old_lik"):
        lik = ev["old_lik"]
    if "unit" in flags and ev.get("unit_idx") is not None:
        lik = list(lik)
        lik[ev["unit_idx"]] = lik[ev["unit_idx"]] * 10
    if ev["kind"] in ("lr", "rel"):
        return list(lik)
    if ev["kind"] == "gate":
        present = _gate_true(ev["gate"], flip="offbyone" in flags, naive="unit" in flags)
    else:
        present = ev["present"]
    if present or "complement" in flags:
        return list(lik)
    return [1 - x for x in lik]


def _posterior(P, flags=()):
    k = P["k"]
    if "avg" in flags:
        a = _posterior(P, ("prior_only",))
        b = _posterior(P, ("lik_only",))
        return [(x + y) / 2 for x, y in zip(a, b)]
    if "ref" in flags and P.get("ref_prior"):
        prior = P["ref_prior"]
    elif "old" in flags and P.get("old_prior"):
        prior = P["old_prior"]
    elif "odds" in flags and P.get("odds_alt"):
        prior = P["odds_alt"]
    else:
        prior = P["prior"]
    if "lik_only" in flags:
        prior = [F(1)] * k
    w = list(prior)
    if "prior_only" not in flags:
        for ev in P["evs"]:
            if not _included(P, ev, flags):
                continue
            L = _ev_vector(ev, flags)
            if "double" in flags:
                L = [x * x for x in L]
            w = [a * b for a, b in zip(w, L)]
    Z = sum(w)
    return [x / Z for x in w]


def _n_included(P):
    return sum(1 for ev in P["evs"] if _included(P, ev, ()))


# =========================================================================
# independent check path (floats / Decimal / calendar / truth tables)
# =========================================================================
def _days_between_alt(d1, d2):
    """Count days from d1 to d2 by walking months with calendar.monthrange."""
    if (d2.year, d2.month) == (d1.year, d1.month):
        return d2.day - d1.day
    total = calendar.monthrange(d1.year, d1.month)[1] - d1.day
    y, m = d1.year, d1.month
    while True:
        m += 1
        if m == 13:
            y, m = y + 1, 1
        if (y, m) == (d2.year, d2.month):
            return total + d2.day
        total += calendar.monthrange(y, m)[1]


def _gate_true_alt(g):
    op = g["op"]
    with localcontext() as ctx:
        ctx.prec = 60
        if g["type"] == "days":
            val = Decimal(_days_between_alt(g["d1"], g["d2"]))
            thr = Decimal(_plain(g["T"]))
        else:
            val = Decimal(_plain(g["v"])) * Decimal(_DEC_BASE[g["uv"]])
            thr = Decimal(_plain(g["T"])) * Decimal(_DEC_BASE[g["uT"]])
        if op == "<=":
            return not (val > thr)
        if op == "<":
            return val < thr and val != thr
        if op == ">=":
            return not (val < thr)
        return val > thr and val != thr


_RULE_TT = {(1, a, b): False for a in (False, True) for b in (False, True)}
_RULE_TT.update({(2, a, b): a for a in (False, True) for b in (False, True)})
_RULE_TT.update({(3, True, False): True, (3, True, True): False, (3, False, True): False, (3, False, False): False})


def _posterior_check(P):
    k = P["k"]
    logw = [math.log(float(p)) for p in P["prior"]]
    for ev in P["evs"]:
        if ev.get("channel"):
            r = P["rule"]
            if not _RULE_TT[(r["depth"], r["A"], r["B"])]:
                continue
        if ev["kind"] == "gate":
            present = _gate_true_alt(ev["gate"])
        elif ev["kind"] in ("lr", "rel"):
            present = True
        else:
            present = ev["present"]
        for i in range(k):
            q = float(ev["lik"][i])
            if not present:
                q = 1.0 - q
            logw[i] += math.log(q)
    m = max(logw)
    ex = [math.exp(x - m) for x in logw]
    s = sum(ex)
    return [x / s for x in ex]


def _bucket(cuts, sides, p):
    idx = 0
    for j, c in enumerate(cuts):
        if p > c or (p == c and sides[j] == "hi"):
            idx = j + 1
    return idx


def _bucket_alt(cuts, sides, p, tol=1e-9):
    n = len(cuts) + 1
    for i in range(n):
        ok = True
        if i > 0:
            c = float(cuts[i - 1])
            if abs(p - c) < tol:
                ok = ok and sides[i - 1] == "hi"
            else:
                ok = ok and p > c
        if i < n - 1:
            c = float(cuts[i])
            if abs(p - c) < tol:
                ok = ok and sides[i] == "lo"
            else:
                ok = ok and p < c
        if ok:
            return i
    return -1


# =========================================================================
# problem construction
# =========================================================================
def _split_int(rng, total, m, minv):
    if m == 0:
        return []
    for _ in range(100):
        w = [rng.random() + 0.15 for _ in range(m)]
        vals = _lr_round([x / sum(w) * total for x in w], total)
        if min(vals) >= minv:
            return vals
    base = [total // m] * m
    base[0] += total - sum(base)
    return base


def _rand_prior(rng, k, shape):
    for _ in range(80):
        if shape == "dominant":
            w = [rng.uniform(0.05, 0.35) for _ in range(k)]
            w[rng.randrange(k)] += rng.uniform(0.9, 2.5)
        elif shape == "flat":
            w = [rng.uniform(0.6, 1.4) for _ in range(k)]
        else:
            w = [rng.random() ** 1.3 + 0.03 for _ in range(k)]
        step = rng.choice([1, 1, 5, 5, 5])
        units = 100 // step
        vals = [x * step for x in _lr_round([x / sum(w) * units for x in w], units)]
        if min(vals) >= 2:
            return vals
    base = [100 // k] * k
    base[0] += 100 - sum(base)
    return base


def _rand_lik(rng, k, mode, fav):
    if mode == "weak":
        base = rng.randint(15, 80)
        vals = [min(95, max(3, base + rng.randint(-5, 5))) for _ in range(k)]
    elif mode == "strong":
        vals = [rng.randint(3, 35) for _ in range(k)]
        vals[fav] = rng.randint(50, 95)
    else:
        vals = [rng.randint(8, 70) for _ in range(k)]
        vals[fav] = min(95, vals[fav] + rng.randint(5, 25))
    if rng.random() < 0.5 and mode != "weak":
        vals = [min(95, max(5, 5 * int(round(v / 5.0)))) for v in vals]
    return [F(v, 100) for v in vals]


def _make_gate(rng, spec, mode, want):
    if spec["type"] == "days":
        T = rng.choice(spec["Ts"])
        if mode in ("edge", "unit"):
            gap = T
            op = rng.choice([o for o in _OPS if _cmp(T, T, o) == want])
        else:
            op = rng.choice(_OPS)
            cands = [g for g in range(max(1, T - 20), T + 21) if g != T and _cmp(g, T, op) == want]
            near = [g for g in cands if abs(g - T) <= 2]
            gap = rng.choice(near) if (near and rng.random() < 0.5) else rng.choice(cands)
        d1 = _rand_date(rng)
        d2 = d1 + datetime.timedelta(days=gap)
        rels = list(_DAYS_REL[op])
        rel = rng.choice(rels).format(T=T, ref=spec["ref"], dir=spec["dir"])
        return dict(type="days", T=F(T), op=op, d1=d1, d2=d2, rel=rel, label="%s %s" % (spec["short"], rel),
                    stat="%s %s" % (spec["verb"], rel), obs=rng.choice(spec["obs"]), edge=(gap == T), unit=False)
    Tv, uT = rng.choice(spec["Ts"])
    Tv = F(Tv)
    U = _UNITS[spec["dim"]]
    op = rng.choice(_OPS)
    cands = []
    if mode == "edge":
        op = rng.choice([o for o in _OPS if _cmp(Tv, Tv, o) == want])
        for u in spec["units"]:
            v = Tv * U[uT] / U[u]
            if _nice(v):
                cands.append((u, v))
    elif mode == "unit":
        for u in spec["units"]:
            if u == uT:
                continue
            fac = U[u] / U[uT]
            for v in _NICE:
                vt = v * fac
                if not (Tv / 4 <= vt <= Tv * 4):
                    continue
                if _cmp(vt, Tv, op) == want and _cmp(v, Tv, op) != want and abs(vt - Tv) >= Tv / 20:
                    cands.append((u, v))
    else:
        for v in _NICE:
            if Tv / 4 <= v <= Tv * 4 and _cmp(v, Tv, op) == want and abs(v - Tv) >= Tv / 10:
                cands.append((uT, v))
    if not cands:
        return None
    uv, v = rng.choice(cands)
    rel = rng.choice(_QTY_REL[op]).format(T=_qv(Tv, uT))
    return dict(type="qty", dim=spec["dim"], T=Tv, uT=uT, v=v, uv=uv, op=op, rel=rel,
                label="%s %s%s" % (spec["short"], rel, spec["suffix"]),
                stat="%s %s%s" % (spec["verb"], rel, spec["suffix"]),
                obs=rng.choice(spec["obs"]).format(V=_qv(v, uv)),
                edge=(v * U[uv] / U[uT] == Tv), unit=(uv != uT))


def _build_problem(rng, dom, cfg):
    k = min(cfg["k"], len(dom["outcomes"]))
    traps = cfg["traps"]
    cat = cfg["cat"]
    bnd = cfg.get("boundary")
    tgt = dom["tool"]["target"]
    specs = []
    seen_test = seen_rel = False
    for s in cfg["specs"]:
        s = dict(s)
        if s["kind"] == "test":
            if seen_test:
                s["kind"] = "cond"
            seen_test = True
        if s["kind"] == "rel":
            if seen_rel or k < 3:
                s["kind"] = "cond"
            else:
                seen_rel = True
        specs.append(s)
    need_tool = any(s["kind"] == "test" for s in specs)
    idx = list(range(len(dom["outcomes"])))
    rng.shuffle(idx)
    chosen = idx[:k]
    if need_tool and tgt not in chosen:
        chosen[rng.randrange(k)] = tgt
    outs = [dom["outcomes"][i] for i in chosen]
    tpos = chosen.index(tgt) if tgt in chosen else None
    P = dict(dom=dom, k=k, outs=outs, labels=[o["label"] for o in outs], tpos=tpos, cat=cat,
             traps=list(traps), boundary=bnd)
    # ---- prior
    if bnd is not None:
        p = cfg["bvals"][0]
        rest = _split_int(rng, 100 - p, k - 1, 2)
        pr = rest[:tpos] + [p] + rest[tpos:]
        prior = [F(x, 100) for x in pr]
    elif "odds" in traps and k == 2:
        a, b = rng.choice(_ODDS)
        mi = rng.randrange(2)
        prior = [F(b, a + b) if i == mi else F(a, a + b) for i in range(2)]
        alt = F(b, a)
        P["odds"] = dict(idx=mi, a=a, b=b)
        P["odds_alt"] = [alt if i == mi else 1 - alt for i in range(2)]
    else:
        shape = "dominant" if cat == "baserate" else rng.choice(["random", "random", "flat", "dominant"])
        prior = [F(x, 100) for x in _rand_prior(rng, k, shape)]
    P["prior"] = prior
    pa = _argmax(prior)
    # ---- evidence
    sigs = list(dom["signals"])
    rng.shuffle(sigs)
    gd = [g for g in dom["gates"] if g["type"] == "days"]
    gq = [g for g in dom["gates"] if g["type"] == "qty"]
    evs = []
    for s in specs:
        kind = s["kind"]
        weak = (cat == "weak")
        if cat in ("overturn", "baserate") and k > 1 and rng.random() < 0.75:
            fav = rng.choice([i for i in range(k) if i != pa])
        elif cat == "agree":
            fav = pa
        else:
            fav = rng.randrange(k)
        ev = dict(kind=kind)
        if kind in ("cond", "gate"):
            if s.get("uninf"):
                q = F(rng.randint(10, 90), 100)
                lik = [q] * k
                ev["uninf"] = True
            else:
                lik = _rand_lik(rng, k, "weak" if weak else rng.choice(["strong", "mixed"]), fav)
            if s.get("unit"):
                j = rng.randrange(k)
                lik[j] = F(rng.randint(2, 9), 100)
                ev["unit_idx"] = j
            if s.get("absent"):
                want = False
            else:
                want = rng.random() < 0.6
            if kind == "cond":
                if not sigs:
                    return None
                sig = sigs.pop()
                ev.update(label=sig["label"], stat=sig["stat"], sig=sig, present=want)
            else:
                gmode = s.get("gmode", "plain")
                if gmode == "unit":
                    pool = [g for g in gq if len(g["units"]) > 1]
                    if not pool:
                        gmode, pool = "edge", gd
                elif gmode == "edge":
                    pool = gd + gq
                else:
                    pool = gd + gq
                spec = rng.choice(pool)
                g = _make_gate(rng, spec, gmode, want)
                if g is None:
                    return None
                assert _gate_true(g) == want
                ev.update(label=g["label"], stat=g["stat"], gate=g, present=want)
            if s.get("channel"):
                ev["channel"] = True
            if s.get("old") and k >= 2:
                i, j = rng.sample(range(k), 2)
                if lik[i] != lik[j]:
                    old = list(lik)
                    old[i], old[j] = old[j], old[i]
                    ev["old_lik"] = old
                    ev["old_idx"] = (i, j)
        elif kind == "test":
            if bnd is not None:
                sv, fv = cfg["bvals"][1], cfg["bvals"][2]
                present = True
            else:
                if weak:
                    fv = rng.randint(10, 60)
                    sv = fv + rng.randint(1, 6)
                else:
                    sv = rng.randint(55, 98)
                    fv = rng.randint(2, 35)
                    if rng.random() < 0.5:
                        sv = min(95, 5 * int(round(sv / 5.0)))
                        fv = max(5, 5 * int(round(fv / 5.0)))
                present = False if s.get("absent") else (rng.random() < 0.65)
            lik = [F(sv, 100) if i == tpos else F(fv, 100) for i in range(k)]
            ev.update(present=present, t=tpos, s=F(sv, 100), f=F(fv, 100))
            if s.get("old"):
                if rng.random() < 0.5:
                    so = min(99, max(30, sv + rng.choice([-1, 1]) * rng.randint(12, 30)))
                    if so != sv:
                        ev["old_lik"] = [F(so, 100) if i == tpos else F(fv, 100) for i in range(k)]
                        ev["old_what"] = ("s", F(so, 100))
                else:
                    fo = min(60, max(1, fv + rng.choice([-1, 1]) * rng.randint(8, 25)))
                    if fo != fv:
                        ev["old_lik"] = [F(sv, 100) if i == tpos else F(fo, 100) for i in range(k)]
                        ev["old_what"] = ("f", F(fo, 100))
        elif kind == "lr":
            if not sigs:
                return None
            sig = sigs.pop()
            if s.get("uninf"):
                r = F(1)
            elif weak:
                r = rng.choice([F(6, 5), F(5, 4), F(4, 5)])
            else:
                r = rng.choice([F(2), F(3), F(4), F(5), F(3, 2), F(1, 2), F(1, 3), F(1, 4)])
            t = fav
            lik = [r if i == t else F(1) for i in range(k)]
            ev.update(label=sig["label"], sig=sig, t=t, r=r, present=True)
        elif kind == "rel":
            if weak:
                acc = F(int(round(100.0 / k)) + rng.randint(2, 6), 100)
            else:
                acc = F(rng.choice([60, 65, 70, 75, 80, 85, 90, 95]), 100)
            L = rng.randrange(k)
            lik = [acc if i == L else (1 - acc) / (k - 1) for i in range(k)]
            ev.update(acc=acc, L=L, present=True)
        else:
            return None
        ev["lik"] = lik
        evs.append(ev)
    P["evs"] = evs
    # ---- admissibility rule
    if any(e.get("channel") for e in evs):
        depth = 3 if "rule3" in traps else 2
        if bnd is not None:
            if depth == 2:
                A, B = False, rng.random() < 0.5
            else:
                A, B = True, True
        else:
            A = rng.random() < (0.8 if depth == 3 else 0.5)
            B = rng.random() < 0.5
        P["rule"] = dict(depth=depth, A=A, B=B, variant=rng.randrange(4))
    # ---- superseded prior / reference class
    if "old_prior" in traps and k >= 2:
        op = list(prior)
        for _ in range(12):
            rng.shuffle(op)
            if op != prior and _argmax(op) != pa:
                break
        if op != prior:
            P["old_prior"] = list(op)
    if "ref" in traps:
        for _ in range(20):
            rp = [F(x, 100) for x in _rand_prior(rng, k, "random")]
            if _argmax(rp) != pa and max(abs(a - b) for a, b in zip(rp, prior)) >= F(1, 10):
                P["ref_prior"] = rp
                break
    return P


# =========================================================================
# configuration
# =========================================================================
_SHORT_TRAPS = ["absent", "gate_edge", "unit_lik", "old_prior", "odds", "note", "cue", "uninf"]
_ALL_TRAPS = ["absent", "gate_edge", "gate_unit", "unit_lik", "old_prior", "old_lik", "ref", "rule2", "rule3",
              "odds", "uninf", "note", "cue"]


def _pick_cfg(rng, plan, attempt):
    lc, qk, ng = plan
    if lc == "short":
        k = rng.choice([2, 2, 3])
        n_ev = rng.choice([1, 1, 2])
        ntr = rng.choice([0, 1, 1, 1])
        pool = list(_SHORT_TRAPS)
    elif lc == "medium":
        k = rng.choice([2, 3, 3, 4, 4, 5])
        n_ev = rng.choice([1, 2, 2, 3, 3])
        ntr = rng.choice([1, 1, 2, 2, 3])
        pool = list(_ALL_TRAPS)
    else:
        k = rng.choice([3, 3, 4, 4, 5])
        n_ev = rng.choice([2, 3, 3, 4])
        ntr = rng.choice([2, 3, 3, 4])
        pool = list(_ALL_TRAPS)
    if attempt > 250:
        ntr = min(ntr, 1)
        n_ev = min(n_ev, 2)
    if qk == "dist":
        pool = [t for t in pool if t not in ("note",)]
    traps = rng.sample(pool, min(ntr, len(pool)))
    if "rule2" in traps and "rule3" in traps:
        traps.remove("rule2")
    if "odds" in traps:
        k = 2
    sub = None
    if qk == "noul":
        sub = rng.choices(["thr", "mlt", "top", "cmp", "dir"], weights=[22, 13, 30, 20, 15])[0]
        if sub == "cmp" and k < 3:
            k = 3 if lc != "short" else k
        if sub == "cmp" and k < 3:
            sub = "top"
    if "odds" in traps and k != 2:
        traps.remove("odds")
    cat = rng.choices(["overturn", "baserate", "weak", "agree"], weights=[30, 28, 20, 22])[0]
    cfg = dict(k=k, traps=traps, cat=cat, sub=sub, boundary=None, scale=None)
    # boundary engineering (exact posterior on a stated cut-point)
    want_bnd = (qk == "bucket" or (qk == "noul" and sub in ("thr", "mlt"))) and rng.random() < 0.35 \
        and "odds" not in traps
    if want_bnd:
        if qk == "bucket":
            si = rng.randrange(len(_SCALES))
            cfg["scale"] = si
            b = rng.choice(_SCALES[si][0])
        elif sub == "mlt":
            b = F(1, 2)
        else:
            b = rng.choice(_THRESH + [F(1, 3), F(2, 3)])
        if b in _BOUNDARY:
            cfg["boundary"] = b
            cfg["bvals"] = rng.choice(_BOUNDARY[b])
            specs = [dict(kind="test")]
            keep = [t for t in traps if t in ("rule2", "rule3", "uninf", "note", "cue", "old_prior", "ref")]
            if rng.random() < 0.5 and "rule2" not in keep and "rule3" not in keep and lc != "short":
                keep.append(rng.choice(["rule2", "rule3"]))
            if "rule2" in keep or "rule3" in keep:
                specs.append(dict(kind="cond", channel=True))
            if "uninf" in keep:
                specs.append(dict(kind=rng.choice(["cond", "lr"]), uninf=True))
            rng.shuffle(specs)
            cfg["traps"] = keep
            cfg["specs"] = specs
            if k < 2:
                cfg["k"] = 2
            return cfg
    specs = []
    if "gate_edge" in traps:
        specs.append(dict(kind="gate", gmode="edge"))
    if "gate_unit" in traps:
        specs.append(dict(kind="gate", gmode="unit"))
    if "rule2" in traps or "rule3" in traps:
        specs.append(dict(kind="cond", channel=True))
    if "unit_lik" in traps:
        specs.append(dict(kind="cond", unit=True))
    if "old_lik" in traps:
        specs.append(dict(kind=rng.choice(["test", "cond"]), old=True))
    if "uninf" in traps:
        specs.append(dict(kind=rng.choice(["cond", "lr"]), uninf=True))
    if "absent" in traps:
        specs.append(dict(kind=rng.choice(["cond", "test"]), absent=True))
    fillk = ["cond", "cond", "gate", "test", "lr"] + (["rel"] if k >= 3 else [])
    while len(specs) < n_ev:
        specs.append(dict(kind=rng.choice(fillk)))
    specs = specs[:5]
    rng.shuffle(specs)
    cfg["specs"] = specs
    return cfg


def _cat_ok(P, post, cat):
    am = _argmax(post)
    ap = _argmax(P["prior"])
    if _n_included(P) == 0:
        return cat in ("weak", "agree")
    lo = _posterior(P, ("lik_only",))
    al = _argmax(lo)
    if cat == "overturn":
        return am != ap
    if cat == "baserate":
        return am == ap and al != am and _top_gap(lo) > F(1, 100)
    if cat == "agree":
        return am == ap == al
    tv = sum(abs(a - b) for a, b in zip(post, P["prior"])) / 2
    return tv <= F(1, 10)


# =========================================================================
# questions
# =========================================================================
_ARGMAX_Q = [
    "What is the most likely {what} for {ref}? Give probabilities that reflect the evidence.",
    "Given the base rates and the evidence, which {what} is most probable for {ref}?",
    "Which option is the most likely {what}? Assign each option a probability that reflects the evidence.",
    "What is the most likely {what}?",
    "Weighing everything above, which {what} should be treated as most likely for {ref}?",
    "Estimate a probability for each possible {what} of {ref}. Which one comes out on top?",
    "Give probabilities that reflect the evidence. Which {what} is most likely?",
    "Using only the approved figures and the admissible evidence, what is the most probable {what}?",
]
_DIST_Q = [
    "Which probability assignment best reflects the evidence for {ref}?",
    "Which of these sets of probabilities is closest to the correct posterior for {ref}?",
    "A reviewer must record calibrated probabilities for {ref}. Which set should they record?",
    "Give probabilities that reflect the evidence: which option matches them (to the nearest percent)?",
    "Which probability distribution is correct once the admissible evidence is combined with the applicable base "
    "rates?",
]
_BUCKET_Q = [
    "How likely is it that {prop}? Choose the band that contains the probability.",
    "Using the bands below, rate the probability that {prop}.",
    "Which likelihood band applies to the proposition that {prop}? Band boundaries are exactly as stated.",
    "After combining the base rate with the admissible evidence, which band contains the probability that {prop}?",
]
_THR_REL = {">=": ["at least", "no less than"], ">": ["greater than", "more than", "above"],
            "<": ["less than", "below"], "<=": ["at most", "no more than"]}
_THR_Q = ["Is the probability that {prop} {rel} {c}?",
          "After accounting for all admissible evidence, is the probability that {prop} {rel} {c}?",
          "Does the probability that {prop} come out {rel} {c}?"]
_MLT_Q = ["Is it more likely than not that {prop}?", "Is the probability that {prop} above 50%?",
          "Is \"{lab}\" more likely than all the other possibilities combined?"]
_TOP_Q = ["Is \"{lab}\" the single most likely {what} for {ref}?",
          "Should \"{lab}\" be ranked as the most probable {what}?",
          "Does \"{lab}\" have the highest probability of any {what} once the evidence is taken into account?"]
_CMP_Q = ["After weighing the evidence, is \"{A}\" more probable than \"{B}\"?",
          "Is \"{A}\" now a likelier {what} than \"{B}\"?",
          "Taking the base rates and the evidence together, does \"{A}\" beat \"{B}\"?"]
_DIR_Q = ["Compared with its base rate, has the evidence made \"{lab}\" more likely?",
          "Did the probability of \"{lab}\" go up once the case evidence was taken into account?",
          "Is \"{lab}\" more probable after the evidence than before it?"]


def _cut_txt(c):
    c = F(c)
    if (c * 100).denominator == 1:
        return _pct(c)
    return {F(1, 3): "one third", F(2, 3): "two thirds"}[c]


def _scale_options(si, sides, rng):
    cuts, labels = _SCALES[si]
    opts = []
    n = len(labels)
    for i in range(n):
        parts = []
        if i > 0:
            c = _cut_txt(cuts[i - 1])
            if sides[i - 1] == "hi":
                parts.append(rng.choice(["at least %s", "%s or more", "%s or higher"]) % c)
            else:
                parts.append(rng.choice(["above %s", "more than %s", "over %s"]) % c)
        if i < n - 1:
            c = _cut_txt(cuts[i])
            if sides[i] == "lo":
                parts.append(rng.choice(["up to and including %s", "at most %s", "no more than %s"]) % c)
            else:
                parts.append(rng.choice(["below %s", "less than %s", "under %s"]) % c)
        if len(parts) == 2:
            txt = parts[0] + rng.choice([" but ", " and ", ", "]) + parts[1]
        else:
            txt = parts[0]
        opts.append("%d: %s (%s)" % (i, labels[i], txt))
    return opts


def _alt_posts(P, extra=False):
    out = []
    ninc = _n_included(P)
    for flag, name in _FLAG_NAMES:
        if flag in ("lik_only", "prior_only") and ninc == 0:
            continue
        if flag == "lik_only" and _top_gap(_posterior(P, ("lik_only",))) < F(1, 1000):
            continue
        out.append((flag, name, _posterior(P, (flag,))))
    if extra and ninc > 0:
        for flag, name in _DIST_EXTRA:
            out.append((flag, name, _posterior(P, (flag,))))
    return out


def _prop(rng, P, T):
    lab = P["labels"][T]
    d = P["dom"]
    return rng.choice(['the %s is "%s"' % (d["what"], lab),
                       '%s falls under "%s"' % (P["case_ref"], lab),
                       'the correct category for %s is "%s"' % (P["case_ref"], lab)])


def _noul_eval(q, post, prior):
    sub = q["sub"]
    if sub == "thr":
        return _cmp(post[q["T"]], q["c"], q["op"])
    if sub == "mlt":
        return post[q["T"]] > F(1, 2)
    if sub == "top":
        return _argmax(post) == q["T"]
    if sub == "cmp":
        return post[q["A"]] > post[q["B"]]
    return post[q["T"]] > prior[q["T"]]


def _noul_eval_alt(q, post, prior, tol=1e-9):
    sub = q["sub"]
    if sub in ("thr", "mlt"):
        p = post[q["T"]]
        c = float(q["c"]) if sub == "thr" else 0.5
        op = q["op"] if sub == "thr" else ">"
        eq = abs(p - c) < tol
        if op == ">=":
            return eq or p > c
        if op == "<=":
            return eq or p < c
        if op == ">":
            return (not eq) and p > c
        return (not eq) and p < c
    if sub == "top":
        return max(range(len(post)), key=lambda i: post[i]) == q["T"]
    if sub == "cmp":
        return post[q["A"]] > post[q["B"]]
    return post[q["T"]] > float(prior[q["T"]])


def _make_question(rng, P, post, cfg, qk, ngold):
    d = P["dom"]
    k = P["k"]
    labels = P["labels"]
    fmtd = dict(what=d["what"], ref=P["case_ref"])
    Q = dict(kind=qk, sub=cfg.get("sub"), mistakes={}, gold_probs=None, card=None, flips=0, gflips=0)
    alts = _alt_posts(P, extra=(qk == "dist"))
    if qk == "argmax":
        if _top_gap(post) < F(4, 100):
            return None
        g = _argmax(post)
        Q["gold"] = labels[g]
        Q["gidx"] = g
        opts = list(labels)
        rng.shuffle(opts)
        Q["options"] = opts
        gp = {labels[i]: float(post[i]) for i in range(k)}
        Q["gold_probs"] = gp
        for flag, name, ap in alts:
            if _top_gap(ap) < F(1, 200):
                continue
            a = _argmax(ap)
            if a != g:
                if flag in _TRAP_FLAGS:
                    Q["flips"] += 1
                else:
                    Q["gflips"] += 1
                Q["mistakes"].setdefault(labels[a], name)
        Q["text"] = rng.choice(_ARGMAX_Q).format(**fmtd)
        if rng.random() < 0.35:
            desc = {o["label"]: o["desc"] for o in P["outs"]}
            Q["card"] = "\n".join("- %s: %s" % (o, desc[o]) for o in opts)
        return Q
    if qk == "dist":
        gr = _round_pct(post)
        sep = rng.choice(["; ", " | ", ", "])
        def ds(r):
            return sep.join("%s %d%%" % (labels[i], r[i]) for i in range(k))
        cands = []
        pri = [a for a in alts if a[0] in _TRAP_FLAGS] + [a for a in alts if a[0] not in _TRAP_FLAGS]
        seen = [gr]
        for flag, name, ap in pri:
            r = _round_pct(ap)
            if max(abs(a - b) for a, b in zip(r, gr)) < 4:
                continue
            if any(max(abs(a - b) for a, b in zip(r, s)) < 3 for s in seen):
                continue
            seen.append(r)
            cands.append((flag, name, r))
        if len(cands) < 2:
            return None
        nd = min(len(cands), rng.choice([2, 3, 3, 4]))
        trap_c = [c for c in cands if c[0] in _TRAP_FLAGS]
        other_c = [c for c in cands if c[0] not in _TRAP_FLAGS]
        chosen = trap_c[:nd]
        rest = other_c[:]
        rng.shuffle(rest)
        chosen += rest[:nd - len(chosen)]
        Q["gold"] = ds(gr)
        Q["gold_ints"] = gr
        opts = [Q["gold"]]
        for flag, name, r in chosen:
            opts.append(ds(r))
            Q["mistakes"][ds(r)] = name
            if flag in _TRAP_FLAGS:
                Q["flips"] += 1
            else:
                Q["gflips"] += 1
        rng.shuffle(opts)
        Q["options"] = opts
        Q["text"] = rng.choice(_DIST_Q).format(**fmtd)
        return Q
    if qk == "bucket":
        si = cfg["scale"] if cfg.get("scale") is not None else rng.randrange(len(_SCALES))
        cuts, labs = _SCALES[si]
        sides = [rng.choice(["lo", "hi"]) for _ in cuts]
        if cfg.get("boundary") is not None:
            T = P["tpos"]
        else:
            pref = [i for i in range(k) if post[i] >= F(1, 10)]
            T = rng.choice(pref) if pref and rng.random() < 0.75 else rng.randrange(k)
        p = post[T]
        if p not in cuts and min(abs(p - c) for c in cuts) < F(12, 1000):
            return None
        opts = _scale_options(si, sides, rng)
        gi = _bucket(cuts, sides, p)
        Q.update(T=T, scale=si, sides=sides, gold=opts[gi], gidx=gi)
        for flag, name, ap in alts:
            ai = _bucket(cuts, sides, ap[T])
            if ai != gi:
                Q["flips" if flag in _TRAP_FLAGS else "gflips"] += 1
                Q["mistakes"].setdefault(opts[ai], name)
        if p in cuts:
            j = cuts.index(p)
            other = j + 1 if sides[j] == "lo" else j
            Q["mistakes"].setdefault(opts[other], "off-by-one boundary")
            Q["flips"] += 1
        Q["all_opts"] = list(opts)
        sh = list(opts)
        rng.shuffle(sh)
        Q["options"] = sh
        Q["text"] = rng.choice(_BUCKET_Q).format(prop=_prop(rng, P, T), **fmtd)
        return Q
    # ---- noul
    sub = cfg.get("sub") or "top"
    Q["options"] = None
    Q["sub"] = sub
    Q["gold"] = ngold
    prior = P["prior"]
    bnd = cfg.get("boundary")
    if sub == "thr":
        if bnd is not None:
            T = P["tpos"]
            c = bnd
            ops = [o for o in _OPS if _cmp(post[T], c, o) == bool(ngold)]
            op = rng.choice(ops)
        else:
            T = rng.randrange(k)
            p = post[T]
            cands = [(c, o) for c in _THRESH for o in _OPS
                     if abs(p - c) >= F(2, 100) and _cmp(p, c, o) == bool(ngold)]
            if not cands:
                return None
            cands.sort(key=lambda x: (abs(p - x[0]), x[0], x[1]))
            c, op = rng.choice(cands[:6])
        Q.update(T=T, c=c, op=op)
        Q["text"] = rng.choice(_THR_Q).format(prop=_prop(rng, P, T), rel=rng.choice(_THR_REL[op]), c=_cut_txt(c))
    elif sub == "mlt":
        if bnd is not None:
            if ngold != 0:
                return None
            T = P["tpos"]
        else:
            cands = [i for i in range(k) if (post[i] > F(53, 100) if ngold else post[i] < F(47, 100))]
            if not cands:
                return None
            T = rng.choice(cands)
        Q.update(T=T)
        Q["text"] = rng.choice(_MLT_Q).format(prop=_prop(rng, P, T), lab=labels[T])
    elif sub == "top":
        g = _argmax(post)
        if _top_gap(post) < F(3, 100):
            return None
        if ngold:
            T = g
        else:
            cands = [i for i in range(k) if i != g and post[g] - post[i] >= F(3, 100)]
            pref = [i for i in cands if i in (_argmax(prior), _argmax(_posterior(P, ("lik_only",))))]
            if not cands:
                return None
            T = rng.choice(pref) if pref and rng.random() < 0.7 else rng.choice(cands)
        Q.update(T=T)
        Q["text"] = rng.choice(_TOP_Q).format(lab=labels[T], **fmtd)
    elif sub == "cmp":
        pairs = [(a, b) for a in range(k) for b in range(k)
                 if a != b and abs(post[a] - post[b]) >= F(3, 100) and (post[a] > post[b]) == bool(ngold)]
        if not pairs:
            return None
        pref = [(a, b) for a, b in pairs if (prior[a] > prior[b]) != (post[a] > post[b])]
        A, B = rng.choice(pref) if pref and rng.random() < 0.7 else rng.choice(pairs)
        Q.update(A=A, B=B)
        Q["text"] = rng.choice(_CMP_Q).format(A=labels[A], B=labels[B], **fmtd)
    else:  # dir
        cands = [i for i in range(k) if abs(post[i] - prior[i]) >= F(1, 100) and (post[i] > prior[i]) == bool(ngold)]
        if not cands:
            return None
        T = rng.choice(cands)
        Q.update(T=T)
        Q["text"] = rng.choice(_DIR_Q).format(lab=labels[T])
    for flag, name, ap in alts:
        if sub in ("top",) and _top_gap(ap) < F(1, 200):
            continue
        a = _noul_eval(Q, ap, prior)
        if a != bool(ngold):
            Q["flips" if flag in _TRAP_FLAGS else "gflips"] += 1
            Q["mistakes"].setdefault(str(1 - ngold), name)
    return Q


# =========================================================================
# notes and surface cues
# =========================================================================
def _add_note(rng, P, Q):
    labels = P["labels"]
    k = P["k"]
    who = rng.choice(_JUNIOR)
    qual = rng.choice(_QUAL)
    name = "%s %s" % (rng.choice(_FIRST), rng.choice(_LAST))
    kind = Q["kind"]
    target = None
    if kind in ("argmax", "dist") or (kind == "noul" and Q["sub"] == "top"):
        if kind == "noul":
            if Q["gold"] == 1:
                others = [i for i in range(k) if i != Q["T"]]
                X = rng.choice(others)
                txt = rng.choice(["It's definitely %s, not %s. Seen this a hundred times.",
                                  "Forget %s - my money's on %s."])
                txt = (txt % (labels[X], labels[Q["T"]])) if txt.startswith("It's") else (txt % (labels[Q["T"]], labels[X]))
            else:
                X = Q["T"]
                txt = rng.choice(["Honestly, this is %s. Just close it as %s.",
                                  "Don't overthink the numbers: it's %s, clearly the top candidate%s."])
                txt = txt % (labels[X], labels[X]) if "close it" in txt else txt % (labels[X], "")
            target = str(1 - Q["gold"])
        else:
            g = labels.index(Q["gold"]) if kind == "argmax" else _argmax(P["post"])
            lo = _argmax(_posterior(P, ("lik_only",))) if _n_included(P) else g
            wrong = [i for i in range(k) if i != g]
            X = lo if lo != g and rng.random() < 0.6 else rng.choice(wrong)
            txt = rng.choice(["Honestly, this is %s. I've seen a dozen like it - just close it as %s.",
                              "Don't overthink the numbers: it's %s. The statistics make it look harder than %s is.",
                              "My money's on %s. Every file like this I've handled was %s.",
                              "Pretty sure it's %s - that's what it always is with these. Put %s at 90%% and move on."])
            txt = txt % (labels[X], labels[X] if "%s" in txt[txt.index("%s") + 2:] else "")
            if kind == "argmax":
                target = labels[X]
    elif kind == "bucket":
        cuts, _ = _SCALES[Q["scale"]]
        gi = Q["gidx"]
        n = len(cuts) + 1
        wrong = [i for i in range(n) if i != gi]
        wi = rng.choice(wrong)
        lo_c = cuts[wi - 1] if wi > 0 else F(0)
        hi_c = cuts[wi] if wi < n - 1 else F(1)
        vals = [v for v in range(1, 100) if lo_c < F(v, 100) < hi_c]
        if not vals:
            return None
        v = rng.choice(vals)
        T = labels[Q["T"]]
        txt = rng.choice(["I'd put the chance that it's %s at about %d%%. No need to run the numbers.",
                          "Gut feel: %s is roughly %d%% here.", "Quick estimate from me: %s, %d%%."]) % (T, v)
        target = Q["all_opts"][wi]
    else:
        sub = Q["sub"]
        T = labels[Q.get("T", 0)] if "T" in Q else None
        g = Q["gold"]
        if sub == "thr":
            c = Q["c"]
            vals = [v for v in range(1, 100) if _cmp(F(v, 100), c, Q["op"]) != bool(g) and abs(F(v, 100) - c) >= F(5, 100)]
            if not vals:
                return None
            v = rng.choice(vals)
            txt = rng.choice(["I'd put %s at about %d%%, no need to run the numbers.",
                              "Gut feel: %s is roughly %d%% here."]) % (T, v)
        elif sub == "mlt":
            txt = ("%s is obviously the more likely story here - I'd say 80%%." % T) if g == 0 else \
                  ("%s? One in ten, tops." % T)
        elif sub == "cmp":
            A, B = labels[Q["A"]], labels[Q["B"]]
            txt = ("%s is clearly more likely than %s here." % (B, A)) if g == 1 else \
                  ("%s is clearly ahead of %s." % (A, B))
        else:
            txt = ("If anything, this evidence argues against %s." % T) if g == 1 else \
                  ("This evidence clearly points towards %s." % T)
        target = str(1 - g)
    if target is not None:
        Q["mistakes"].setdefault(target, "followed unverified note")
    return dict(who=who, qual=qual, name=name, text=txt)


def _add_cue(rng, P, Q):
    k = P["k"]
    labels = P["labels"]
    kind = Q["kind"]
    if kind == "argmax":
        g = Q["gidx"]
        wrong = [i for i in range(k) if i != g]
        X = rng.choice(wrong)
        Q["mistakes"].setdefault(labels[X], "surface cue")
    elif kind == "noul" and Q["sub"] == "top" and Q["gold"] == 0:
        X = Q["T"]
        Q["mistakes"].setdefault("1", "surface cue")
    else:
        g = _argmax(P["post"])
        wrong = [i for i in range(k) if i != g]
        X = rng.choice(wrong)
    return P["outs"][X]["cue"].format(org=P["org"])


# =========================================================================
# rendering
# =========================================================================
def _prior_block(rng, P, prior, style, variant):
    labels, outs = P["labels"], P["outs"]
    cases = P["dom"]["cases"]
    vs = "pct" if style in ("dec", "pm") else style
    k = P["k"]
    rows = [(labels[i], _V(prior[i], "dec" if style == "dec" else vs)) for i in range(k)]
    rec = {labels[i]: _V(prior[i], "dec" if style == "dec" else vs) for i in range(k)}
    if variant == "counts":
        Ns = [N for N in (200, 400, 500, 600, 800, 1000, 1200, 2000, 2500) if all((p * N).denominator == 1 for p in prior)]
        if not Ns:
            variant = "list"
        else:
            N = rng.choice(Ns)
            parts = ["%s were %s" % (_num(prior[i] * N), outs[i]["plural"]) for i in range(k)]
            return ["Of the last %s %s reviewed, %s." % (_num(N), cases, _join(parts))], rows, rec
    if variant == "prob" or style == "dec":
        parts = ["P(%s) = %s" % (labels[i], _V(prior[i], "dec")) for i in range(k)]
        return ["Prior probabilities: %s." % _join(parts, "and")], rows, rec
    if variant == "hist":
        parts = ["%s were %s" % (_Q(prior[0], cases, vs), outs[0]["plural"])]
        parts += ["%s were %s" % (_V(prior[i], vs), outs[i]["plural"]) for i in range(1, k)]
        return ["Historically, %s." % _join(parts)], rows, rec
    parts = ["%s %s" % (labels[i], _V(prior[i], vs)) for i in range(k)]
    lead = rng.choice(["Base rates: ", "Share of past %s by category: " % cases, "Historical mix: "])
    return [lead + _join(parts) + "."], rows, rec


def _odds_block(rng, P):
    o = P["odds"]
    mi = o["idx"]
    other = 1 - mi
    outs = P["outs"]
    d = P["dom"]
    if rng.random() < 0.5:
        s = "The odds that a %s turns out to be \"%s\" are %d to %d; the only other possibility is \"%s\"." % (
            d["case"], P["labels"][mi], o["b"], o["a"], P["labels"][other])
    else:
        s = "Among past %s, %s outnumber %s by %d to %d (these are the only two categories)." % (
            d["cases"], outs[other]["plural"], outs[mi]["plural"], o["a"], o["b"])
    rows = [("Odds %s : %s" % (P["labels"][mi], P["labels"][other]), "%d : %d" % (o["b"], o["a"]))]
    rec = {"odds_%s_vs_%s" % (P["labels"][mi], P["labels"][other]): "%d to %d" % (o["b"], o["a"])}
    return [s], rows, rec


def _ev_stat(rng, P, ev, style):
    """-> (sentences, table_row or None, record)"""
    d = P["dom"]
    outs, labels, k = P["outs"], P["labels"], P["k"]
    cases, what = d["cases"], d["what"]
    vs = "pct" if style == "dec" else style
    kind = ev["kind"]
    if kind in ("cond", "gate"):
        lik = ev["lik"]
        label, stat = ev["label"], ev["stat"]
        ui = ev.get("unit_idx")
        if ev.get("uninf") and rng.random() < 0.6:
            q = lik[0]
            s = rng.choice(["The signal \"%s\" turns up at the same rate - %s - in every category." % (label, _V(q, vs)),
                            "The signal \"%s\" shows up in %s, whatever the true %s is." % (label, _Q(q, cases, vs),
                                                                                           what)])
            sents = [s]
        else:
            variant = "cond" if style == "dec" else rng.choice(["per", "per", "one", "neg", "cond"])
            sents = []
            if variant == "one":
                parts = []
                for i in range(k):
                    st = "pm" if i == ui else vs
                    parts.append(_Q(lik[i], outs[i]["plural"], st))
                sents.append("%s: seen in %s." % (_cap(label), _join(parts)))
            elif variant == "cond":
                parts = []
                for i in range(k):
                    if i == ui:
                        val = _V(lik[i], "pm")
                    else:
                        val = _V(lik[i], style)
                    if style == "dec":
                        parts.append("P(%s | %s) = %s" % (label, labels[i], val))
                    else:
                        parts.append("if the %s is %s, the chance of %s is %s" % (what, labels[i], label, val))
                if style == "dec":
                    sents.append("; ".join(parts) + ".")
                else:
                    sents.append(_cap("; ".join(parts)) + ".")
            else:
                negi = set()
                if variant == "neg":
                    cand = [i for i in range(k) if i != ui]
                    rng.shuffle(cand)
                    negi = set(cand[:rng.choice([1, 2])])
                for i in range(k):
                    pl = outs[i]["plural"]
                    p = lik[i]
                    if i == ui:
                        sents.append("Among %s, the rate of %s is %s." % (pl, label, _V(p, "pm")))
                    elif i in negi and p >= F(1, 2):
                        sents.append("All but %s of %s %s." % (_pct(1 - p), pl, stat))
                    elif i in negi:
                        sents.append("It is not unusual for %s to lack the signal \"%s\": %s of them do not show it."
                                     % (pl, label, _pct(1 - p)))
                    elif rng.random() < 0.5:
                        sents.append("%s %s." % (_cap(_Q(p, pl, vs)), stat))
                    else:
                        sents.append("Among %s, %s %s." % (pl, _V(p, vs), stat))
        if ev.get("old_lik"):
            i, j = ev["old_idx"]
            yr = P["yr_new"] - rng.randint(1, 3)
            sents.append("(The %d edition of these statistics listed %s for %s and %s for %s; both figures were "
                         "corrected in the current edition, which is the one given here.)" % (
                             yr, _V(ev["old_lik"][i], vs), outs[i]["plural"], _V(ev["old_lik"][j], vs),
                             outs[j]["plural"]))
        row = (label, [(_V(lik[i], "pm") if i == ui else _V(lik[i], style)) for i in range(k)])
        rec = {"signal": label, "share_showing_signal": {labels[i]: row[1][i] for i in range(k)}}
        return sents, row, rec
    if kind == "test":
        tool = d["tool"]
        N = tool["name"]
        t = ev["t"]
        s, f = ev["s"], ev["f"]
        tp = outs[t]["plural"]
        rs = "dec" if style == "dec" else "pct"
        v = rng.randrange(5 if (1 - s) >= F(15, 100) else 4)
        if v == 0:
            sent = "%s %s %s and %s." % (_cap(N), tool["verb"], _Q(s, tp, vs), _Q(f, "other " + cases, vs))
        elif v == 1:
            sent = "%s catches %s; its false-alarm rate on other %s is %s." % (_cap(N), _Q(s, tp, vs), cases,
                                                                             _V(f, rs))
        elif v == 2:
            sent = "%s misses %s, and it wrongly %s %s." % (_cap(N), _Q(1 - s, tp, vs), tool["verb"],
                                                          _Q(f, "other " + cases, vs))
        elif v == 3:
            sent = "%s has a sensitivity of %s and a specificity of %s for %s." % (_cap(N), _V(s, rs),
                                                                                 _V(1 - f, rs), tp)
        else:
            sent = ("It is not true that %s never misses: it fails to %s %s. It stays quiet on all but %s of "
                    "other %s." % (N, tool["inf"], _Q(1 - s, tp, vs), _pct(f), cases))
        sents = [sent]
        if ev.get("old_lik"):
            w, ov = ev["old_what"]
            what_txt = "a detection rate" if w == "s" else "a false-alarm rate"
            sents.append(rng.choice([
                "(The vendor's original datasheet quoted %s of %s; that datasheet was withdrawn after the in-house "
                "validation, which produced the figures above.)" % (what_txt, _V(ov, style)),
                "Note: an older version of this summary gave %s of %s. It has been superseded by the current "
                "validation figures stated above." % (what_txt, _V(ov, style))]))
        row = ("%s by %s" % (tool["verb"], N), [_V(ev["lik"][i], style) for i in range(k)])
        rec = {"tool": N, "target": labels[t], "detection_rate": _V(s, style),
               "false_alarm_rate_on_other_%s" % cases.replace(" ", "_"): _V(f, style)}
        return sents, row, rec
    if kind == "lr":
        t, r = ev["t"], ev["r"]
        label = ev["label"]
        tp = outs[t]["plural"]
        if r == 1:
            sent = rng.choice(["The signal \"%s\" shows up at the same rate in every category, %s included." % (
                label, tp), "The signal \"%s\" is equally common whatever the %s is." % (label, what)])
        else:
            words = {F(2): "twice", F(3): "three times", F(4): "four times", F(5): "five times",
                     F(3, 2): "one and a half times", F(1, 2): "only half", F(1, 3): "only a third",
                     F(1, 4): "only a quarter", F(6, 5): "1.2 times", F(5, 4): "1.25 times", F(4, 5): "only 0.8 times"}
            if rng.random() < 0.7:
                sent = "%s is %s as common among %s as among other %s." % (_cap(label), words[r], tp, cases)
            else:
                sent = "The likelihood ratio for %s is %s:%s in favour of \"%s\" versus any other %s." % (
                    label, _num(r.numerator), _num(r.denominator), labels[t], what)
        rec = {"signal": label, "likelihood_ratio": "%s vs any other = %s" % (labels[t], _num(r) if (r * 100).denominator == 1 else "%d/%d" % (r.numerator, r.denominator))}
        return [sent], None, rec
    # rel
    N = d["clf"]
    acc = ev["acc"]
    if style == "dec":
        freq = "with probability %s" % _num(acc)
    else:
        freq = "%s of the time" % _pct(acc)
    sent = rng.choice([
        "Whatever the true category, %s outputs that category %s; otherwise it outputs one of the other "
        "categories, each equally often." % (N, freq),
        "%s names the true %s %s, and its errors are spread evenly over the remaining categories." % (
            _cap(N), what, freq)])
    rec = {"classifier": N, "accuracy_given_any_true_category": _V(acc, style),
           "errors": "spread evenly over the other categories"}
    return [sent], None, rec


def _ev_obs(rng, P, ev):
    d = P["dom"]
    kind = ev["kind"]
    if kind in ("cond", "lr"):
        s = ev["sig"]["yes"] if ev["present"] else ev["sig"]["no"]
    elif kind == "gate":
        g = ev["gate"]
        if g["type"] == "days":
            s = g["obs"].format(d1=_fmt_date(g["d1"], P["dstyle"]), d2=_fmt_date(g["d2"], P["dstyle"]))
        else:
            s = g["obs"]
    elif kind == "test":
        tool = d["tool"]
        if ev["present"]:
            s = rng.choice(["%s %s this %s." % (_cap(tool["name"]), tool["verb"], d["case"]),
                            "%s raised an alert on this %s." % (_cap(tool["name"]), d["case"])])
        else:
            s = rng.choice(["%s did not %s this %s." % (_cap(tool["name"]), tool["inf"], d["case"]),
                            "%s returned no alert for this %s." % (_cap(tool["name"]), d["case"])])
    else:
        s = "%s labelled this %s \"%s\"." % (_cap(d["clf"]), d["case"], P["labels"][ev["L"]])
    out = []
    if ev.get("channel"):
        ch = d["channel"]
        out.append("According to %s, %s" % (ch["name"], _low(s)))
        r = P["rule"]
        out.append(ch["A_yes"] if r["A"] else ch["A_no"])
        if r["A"] and (r["depth"] == 3 or rng.random() < 0.35):
            out.append(ch["B_yes"] if r["B"] else ch["B_no"])
    else:
        out.append(s)
    return out


def _rule_sents(rng, P):
    ch = P["dom"]["channel"]
    r = P["rule"]
    v = r["variant"]
    if r["depth"] == 2:
        s = [["Information that comes only from %s is disregarded unless %s." % (ch["names"], ch["A"])],
             ["Do not use %s, except where %s." % (ch["names"], ch["A"])],
             ["A fact taken from %s may be used only if %s." % (ch["name"], ch["A"])],
             ["It is not acceptable to ignore a fact from %s when %s; in every other case such facts are not used."
              % (ch["name"], ch["A"])]][v]
    else:
        s = [["Information that comes only from %s is disregarded unless %s." % (ch["names"], ch["A"]),
              "However, even then it must be set aside if %s." % ch["B"]],
             ["Do not use %s, except where %s." % (ch["names"], ch["A"]),
              "Exception to that exception: if %s, the fact is excluded after all." % ch["B"]],
             ["A fact taken from %s counts only if %s and it is not the case that %s." % (ch["name"], ch["A"], ch["B"])],
             ["It is not acceptable to ignore a fact from %s when %s - unless %s, in which case it is not used "
              "either. In every other case such facts are not used." % (ch["name"], ch["A"], ch["B"])]][v]
    s.append(rng.choice(["All other information counts normally.", "Everything else in this file is admissible.",
                         "No other evidence is restricted."]))
    return s


def _indep_sent(rng, P):
    w = P["dom"]["what"]
    return rng.choice([
        "Treat the signals as conditionally independent given the true %s." % w,
        "Assume the pieces of evidence are independent of each other once the %s is known." % w,
        "The methods team has confirmed the signals are independent given the underlying category.",
        "Signals may be combined as independent evidence (checked by the methods team)."])


def _filler_blocks(rng, P):
    d = P["dom"]
    pool = []
    for t, x in d["filler"]:
        pool.append(dict(role="filler", title=t, sents=[x.format(org=P["org"])]))
    for t, x in _GENERIC_FILLER:
        pool.append(dict(role="filler", title=t, sents=[x]))
    rng.shuffle(pool)
    gen = []
    segs = list(d["segs"])
    rng.shuffle(segs)
    for _ in range(8):
        if rng.random() < 0.55 or not segs:
            o = rng.choice(d["outcomes"])
            sig = rng.choice(d["signals"])
            dt = _fmt_date(_rand_date(rng), P["dstyle"])
            nm = "%s %s" % (rng.choice(_FIRST), rng.choice(_LAST))
            gen.append(dict(role="filler", title=rng.choice(["For reference: an unrelated closed file",
                                                              "Other items in the queue (not this case)",
                                                              "Separate file, same week"]),
                            sents=["File %s%d (%s) was closed as \"%s\" by %s. %s That file has no bearing on this "
                                   "one." % (d["idp"], rng.randint(10000, 99999), dt, o["label"], nm, sig["yes"])]))
        else:
            seg = segs.pop()
            kk = rng.randint(2, min(4, len(d["outcomes"])))
            os_ = rng.sample(d["outcomes"], kk)
            vals = _rand_prior(rng, kk, "random")
            parts = ["%s %d%%" % (os_[i]["label"], vals[i]) for i in range(kk)]
            gen.append(dict(role="filler", title="Other segments (not applicable here)",
                            sents=["For %s - a separate line of business from this %s - the historical mix is %s. "
                                   "These figures are not used for this review." % (seg, d["case"], _join(parts))]))
    out = []
    while pool or gen:
        if gen and (not pool or rng.random() < 0.35):
            out.append(gen.pop())
        else:
            out.append(pool.pop())
    return out


def _make_blocks(rng, P, Q, note, cue):
    d = P["dom"]
    style = P["style"]
    blocks = []
    bg = [_cap(rng.choice(d["intros"]).format(org=P["org"], id=P["id"], detail=P["detail"]))]
    if P.get("ref_prior"):
        bg.append(d["ref"]["member"].format(org=P["org"]))
    if cue:
        bg.append(cue)
    blocks.append(dict(role="bg", title=rng.choice(["Background", "Case summary", "The file", "Situation"]),
                       sents=bg, jkey="case"))
    # priors
    pv = rng.choice(["list", "hist", "counts", "prob"] if style == "dec" else ["list", "hist", "counts", "list"])
    pri_blocks = []
    if P.get("odds"):
        s, rows, rec = _odds_block(rng, P)
        cur = dict(role="prior", title="Base rates", sents=s, table=(["Quantity", "Value"], rows), record=rec,
                   jkey="base_rates")
    else:
        s, rows, rec = _prior_block(rng, P, P["prior"], style, pv)
        title = rng.choice(["Base rates", "Prior probabilities", "Historical mix", "Starting point (before case facts)"])
        cur = dict(role="prior", title=title, sents=s, table=(["Outcome", "Base rate"], rows), record=rec,
                   jkey="base_rates")
    if P.get("ref_prior"):
        sub = d["ref"]["sub"]
        broad = d["ref"]["broad"].format(org=P["org"])
        cur["title"] = "Base rates for %s" % sub
        cur["sents"] = [rng.choice(["For %s specifically, the figures are as follows." % sub,
                                    "Figures for %s:" % sub])] + cur["sents"]
        cur["jkey"] = "base_rates_" + sub.replace(" ", "_")
        s2, rows2, rec2 = _prior_block(rng, P, P["ref_prior"], style, rng.choice(["list", "hist"]))
        dec = dict(role="prior_ref", title=rng.choice(["Portfolio-wide base rates", "Company-wide figures"]),
                   sents=["Across %s, the mix is different." % broad] + s2,
                   table=(["Outcome", "Base rate"], rows2), record=rec2, jkey="base_rates_" + broad.replace(" ", "_"))
        pri_blocks = [dec, cur] if rng.random() < 0.5 else [cur, dec]
    else:
        pri_blocks = [cur]
    if P.get("old_prior"):
        yo = P["yr_new"] - rng.randint(2, 4)
        s3, rows3, rec3 = _prior_block(rng, P, P["old_prior"], style, rng.choice(["list", "hist", "counts"]))
        ot, op_ = rng.choice([
            ("Base rates (%d study - superseded, do not use)" % yo,
             "The following figures come from the %d study, which was withdrawn after the %d recalibration." % (
                 yo, P["yr_new"])),
            ("Earlier base rates (%d, now out of date)" % yo,
             "Earlier estimate from %d, kept for history only; it has been replaced." % yo),
            ("Base rates - DRAFT v1 (never approved)", "DRAFT v1 figures, never approved and replaced by v2:")])
        oldb = dict(role="prior_old", title=ot, sents=[op_] + s3, table=(["Outcome", "Base rate (old)"], rows3),
                    record=rec3, jkey="base_rates_superseded_%d" % yo)
        cur["title"] = rng.choice(["Base rates (current, approved %d)" % P["yr_new"],
                                   "Updated base rates (v2, replaces all earlier versions)"])
        cur["sents"] = [rng.choice(["Current approved figures (%d):" % P["yr_new"],
                                    "These are the current figures and replace any earlier version."])] + cur["sents"]
        if rng.random() < 0.5:
            pri_blocks = [oldb] + pri_blocks
        else:
            pri_blocks = pri_blocks + [oldb]
    # stats
    st_s, rows, recs, extra = [], [], [], []
    for ev in P["evs"]:
        s, row, rec = _ev_stat(rng, P, ev, style)
        st_s += s
        recs.append(rec)
        if row is not None and not ev.get("old_lik") and not (ev.get("uninf") and False):
            rows.append(row)
        else:
            extra += s
    stats = dict(role="stats", title=rng.choice(["Signal statistics", "What the signals tell us", "Evidence strength",
                                                  "Reference statistics"]),
                 sents=st_s, record=recs, jkey="signal_statistics")
    if rows:
        stats["table"] = (["Signal"] + P["labels"], [[r[0]] + r[1] for r in rows])
        stats["table_pre"] = "Share of past %s in each category that showed each signal:" % d["cases"]
        stats["table_extra"] = extra
    indep = None
    if len(P["evs"]) >= 2:
        indep = dict(role="indep", title="Assumption", sents=[_indep_sent(rng, P)], jkey="assumption")
    obs_s = []
    for ev in P["evs"]:
        obs_s += _ev_obs(rng, P, ev)
    obs = dict(role="obs", title=rng.choice(["Findings for this %s" % d["case"], "Facts of this %s" % d["case"],
                                              "What the review found", "Case facts"]),
               sents=obs_s, jkey="observations")
    rule = None
    if P.get("rule"):
        rule = dict(role="rule", title=rng.choice(["Evidence rules", "Admissibility of evidence", "Which evidence counts"]),
                    sents=_rule_sents(rng, P), jkey="evidence_rules")
    nb = None
    if note:
        framed = rng.choice(["Note from %s (%s): \"%s\"", "Comment added by %s - %s: \"%s\"",
                             "[%s, %s] %s"]) % (note["who"], note["qual"], note["text"])
        nb = dict(role="note", title=rng.choice(["Comments", "Side note", "Reviewer comments"]), sents=[framed],
                  raw=note["text"], who=note["who"], qual=note["qual"], name=note["name"], jkey="comments")
    # order
    core = []
    mid = pri_blocks + [stats] + ([indep] if indep else [])
    if rng.random() < 0.3:
        core = [obs] + mid
    else:
        core = mid + [obs]
    if rule:
        pos = rng.randrange(len(core) + 1)
        core.insert(pos, rule)
    if nb:
        pos = rng.randrange(1, len(core) + 1)
        core.insert(pos, nb)
    return blocks + core


def _ascii_table(header, rows):
    cols = len(header)
    w = [max(len(str(r[i])) for r in [header] + rows) for i in range(cols)]
    line = lambda r: " | ".join(str(r[i]).ljust(w[i]) for i in range(cols)).rstrip()
    out = [line(header), "-+-".join("-" * x for x in w)]
    out += [line(r) for r in rows]
    return "\n".join(out)


def _block_text(b, use_table):
    if use_table and b.get("table"):
        hdr, rows = b["table"]
        pre = b.get("table_pre")
        parts = []
        if b["role"] in ("prior", "prior_old", "prior_ref"):
            lead = [s for s in b["sents"][:-1]]
            if lead:
                parts.append(" ".join(lead))
        if pre:
            parts.append(pre)
        parts.append(_ascii_table(hdr, [list(r) for r in rows]))
        if b.get("table_extra"):
            parts.append(" ".join(b["table_extra"]))
        return "\n".join(parts)
    return " ".join(b["sents"])


def _render(seed, P, blocks, fmt):
    rng = random.Random(seed)
    d = P["dom"]
    if fmt == "prose":
        paras = []
        for b in blocks:
            t = _block_text(b, False)
            if b["role"] not in ("bg",) and rng.random() < 0.35:
                t = "%s. %s" % (b["title"].rstrip("."), t) if rng.random() < 0.5 else "%s: %s" % (b["title"].upper(), t)
            paras.append(t)
        return "\n\n".join(paras)
    if fmt == "table":
        paras = []
        for b in blocks:
            t = _block_text(b, True)
            if b.get("table") or rng.random() < 0.4:
                t = "%s\n%s" % (b["title"], t)
            paras.append(t)
        return "\n\n".join(paras)
    if fmt == "bullets":
        mark = rng.choice(["-", "*", "•"])
        paras = []
        for b in blocks:
            if b.get("table") and rng.random() < 0.4:
                paras.append("%s:\n%s" % (b["title"], _block_text(b, True)))
            else:
                paras.append("%s:\n" % b["title"] + "\n".join("%s %s" % (mark, s) for s in b["sents"]))
        return "\n\n".join(paras)
    if fmt == "numbered":
        style = rng.randrange(3)
        paras = []
        for i, b in enumerate(blocks, 1):
            head = ["%d. %s" % (i, b["title"].upper()), "Section %d - %s" % (i, b["title"]),
                    "§%d %s" % (i, b["title"])][style]
            if b.get("table") and rng.random() < 0.5:
                body = _block_text(b, True)
            elif len(b["sents"]) > 1 and rng.random() < 0.5:
                body = "\n".join("  %d.%d %s" % (i, j, s) for j, s in enumerate(b["sents"], 1))
            else:
                body = " ".join(b["sents"])
            paras.append(head + "\n" + body)
        return "\n\n".join(paras)
    if fmt == "json":
        obj = {}
        for b in blocks:
            key = b.get("jkey") or b["title"].lower().replace(" ", "_")
            if b["role"] == "filler":
                key = "appendix_" + "".join(ch for ch in b["title"].lower().replace(" ", "_") if ch.isalnum() or ch == "_")
            base, n = key, 2
            while key in obj:
                key = "%s_%d" % (base, n)
                n += 1
            if b["role"] == "note":
                obj[key] = {"author": b["who"], "status": b["qual"], "text": b["raw"]}
            elif b.get("record") is not None:
                if b["role"] in ("prior", "prior_old", "prior_ref") and len(b["sents"]) > 1:
                    obj[key] = {"note": " ".join(b["sents"][:-1]), "values": b["record"]}
                else:
                    obj[key] = b["record"]
            else:
                obj[key] = b["sents"] if len(b["sents"]) > 1 else b["sents"][0]
        return json.dumps(obj, indent=rng.choice([1, 2]), ensure_ascii=False)
    domain = "".join(ch for ch in P["org"].lower() if ch.isalnum())[:18] + ".example"
    base = datetime.datetime(P["date"].year, P["date"].month, P["date"].day, 8, 30) + \
        datetime.timedelta(minutes=rng.randrange(120))
    people = {}

    def person(role):
        if role not in people:
            people[role] = "%s %s" % (rng.choice(_FIRST), rng.choice(_LAST))
        return people[role]
    roles = {"bg": "case owner", "obs": "case owner", "prior": "analytics", "prior_ref": "analytics",
             "stats": "analytics", "indep": "analytics", "prior_old": "analytics, earlier thread", "rule": "methods lead",
             "filler": "admin"}
    if fmt == "email":
        msgs = []
        for b in blocks:
            role = b["role"]
            if role == "note":
                sender = "%s (%s, %s)" % (b["name"], b["who"], b["qual"])
                body = b["raw"]
            else:
                r = roles[role]
                sender = "%s (%s)" % (person(r), r)
                body = _block_text(b, rng.random() < 0.4)
            if msgs and msgs[-1][0] == sender and role != "filler":
                msgs[-1][1].append(body)
            else:
                msgs.append((sender, [body], role))
        out = []
        t = base
        subj = "%s %s review" % (_cap(d["case"]), P["id"])
        for i, (sender, bodies, role) in enumerate(msgs):
            t = t + datetime.timedelta(minutes=rng.randint(7, 190))
            handle = sender.split(" (")[0].lower().replace(" ", ".")
            s = "RE: " + subj if i else subj
            if role == "filler":
                s = rng.choice(["FYI (unrelated)", "Housekeeping", "Fwd: reminder"])
            head = "From: %s <%s@%s>\nTo: review-team@%s\nDate: %s %02d:%02d\nSubject: %s" % (
                sender, handle, domain, domain, _fmt_date(t.date(), 0), t.hour, t.minute, s)
            out.append(head + "\n\n" + "\n\n".join(bodies))
        return ("\n\n" + rng.choice(["-" * 40, "=" * 30, "-----Original thread-----"]) + "\n\n").join(out)
    # log
    lines = []
    t = base
    for b in blocks:
        t = t + datetime.timedelta(minutes=rng.randint(1, 45))
        if b["role"] == "note":
            who = "%s (%s, %s)" % (b["name"].split()[0].lower(), b["who"], b["qual"])
            lines.append("[%s %02d:%02d] %s: %s" % (t.date().isoformat(), t.hour, t.minute, who, b["raw"]))
            continue
        r = roles[b["role"]]
        who = "%s (%s)" % (person(r).split()[0].lower(), r)
        if b.get("table") and rng.random() < 0.5:
            lines.append("[%s %02d:%02d] %s: %s -\n%s" % (t.date().isoformat(), t.hour, t.minute, who, b["title"],
                                                          _block_text(b, True)))
        else:
            lines.append("[%s %02d:%02d] %s: %s" % (t.date().isoformat(), t.hour, t.minute, who, " ".join(b["sents"])))
    return "\n".join(lines)


_FORMATS = ["prose", "bullets", "numbered", "table", "json", "email", "log"]
_FMT_W = [22, 16, 14, 14, 10, 14, 10]
_SHORT_FMT = ["prose", "bullets", "table", "prose"]


# =========================================================================
# item assembly
# =========================================================================
def _plan(n, rng):
    def alloc(weights):
        raw = [w * n for w in weights]
        return _lr_round(raw, n)
    lc = alloc([0.3, 0.4, 0.3])
    lengths = ["short"] * lc[0] + ["medium"] * lc[1] + ["long"] * lc[2]
    qc = alloc([0.42, 0.14, 0.14, 0.30])
    qks = ["argmax"] * qc[0] + ["dist"] * qc[1] + ["bucket"] * qc[2] + ["noul"] * qc[3]
    rng.shuffle(lengths)
    rng.shuffle(qks)
    golds = []
    c = 0
    order = rng.random() < 0.5
    for q in qks:
        if q == "noul":
            golds.append(int((c % 2 == 0) == order))
            c += 1
        else:
            golds.append(None)
    return list(zip(lengths, qks, golds))


def _make_item(rng, plan, index):
    lc, qk, ng = plan
    for attempt in range(800):
        dom = DOMAINS[(index + attempt // 40) % len(DOMAINS)] if rng.random() < 0.5 else rng.choice(DOMAINS)
        cfg = _pick_cfg(rng, plan, attempt)
        P = _build_problem(rng, dom, cfg)
        if P is None:
            continue
        post = _posterior(P)
        P["post"] = post
        chk = _posterior_check(P)
        assert all(abs(float(a) - b) < 1e-9 for a, b in zip(post, chk)), "posterior check failed"
        if cfg.get("boundary") is not None:
            assert post[P["tpos"]] == cfg["boundary"], "boundary engineering failed"
        needs_cat = qk in ("argmax", "dist") or (qk == "noul" and cfg.get("sub") in ("top", "cmp", "dir"))
        if needs_cat and cfg.get("boundary") is None and not _cat_ok(P, post, cfg["cat"]):
            continue
        # case-level details
        P["org"] = rng.choice(dom["orgs"])
        P["id"] = "%s%d" % (dom["idp"], rng.randint(10000, 99999))
        P["detail"] = rng.choice(dom["details"])
        P["date"] = _rand_date(rng)
        P["yr_new"] = P["date"].year
        P["dstyle"] = rng.randrange(4)
        P["case_ref"] = rng.choice(["this %s" % dom["case"], "%s %s" % (dom["case"], P["id"])])
        P["style"] = rng.choice(["pct"] * 6 + ["in", "outof", "words", "dec", "per1000"])
        Q = _make_question(rng, P, post, cfg, qk, ng)
        if Q is None:
            continue
        comp_traps = [t for t in cfg["traps"] if t not in ("note", "cue")]
        need_flip = comp_traps and rng.random() < (0.5 if lc == "short" else 0.75)
        if need_flip and Q["flips"] == 0:
            continue
        note = _add_note(rng, P, Q) if "note" in cfg["traps"] else None
        if "note" in cfg["traps"] and note is None:
            continue
        cue = _add_cue(rng, P, Q) if "cue" in cfg["traps"] else None
        blocks = _make_blocks(rng, P, Q, note, cue)
        fmt = rng.choice(_SHORT_FMT) if lc == "short" else rng.choices(_FORMATS, weights=_FMT_W)[0]
        rseed = rng.randrange(2 ** 31)
        state = _render(rseed, P, blocks, fmt)
        if lc == "short":
            if len(state) >= 600:
                continue
        else:
            lo, hi = (600, 2500) if lc == "medium" else (2500, 6000)
            target = rng.randint(lo + 60, (hi - 150) if lc == "long" else lo + 900)
            if len(state) > hi:
                continue
            if len(state) < target:
                fill = _filler_blocks(rng, P)
                cur = list(blocks)
                fi = 0
                while len(state) < target and fi < len(fill):
                    trial = list(cur)
                    trial.insert(rng.randrange(1, len(trial) + 1), fill[fi])
                    fi += 1
                    st2 = _render(rseed, P, trial, fmt)
                    if len(st2) <= hi:
                        cur, state = trial, st2
                blocks = cur
            if not (lo <= len(state) <= hi):
                continue
        n_ev = len(P["evs"])
        hard = (Q["flips"] >= 2 or cfg.get("boundary") is not None or
                (Q["flips"] >= 1 and (Q["gflips"] >= 1 or n_ev >= 3 or (P.get("rule") or {}).get("depth") == 3)))
        meta = {"family": FAMILY, "difficulty": "hard" if hard else "medium"}
        if Q["gold_probs"] is not None:
            gp = dict((o, Q["gold_probs"][o]) for o in Q["options"])
            meta["gold_probs"] = gp
        if Q["mistakes"]:
            meta["mistakes"] = Q["mistakes"]
        row = {"state": state, "qtype": "noul" if qk == "noul" else "choice", "instructions": Q["text"],
               "options": Q["options"], "gold": Q["gold"], "card": Q["card"], "meta": meta}
        P["Q"] = Q
        P["fmt"] = fmt
        P["lc"] = lc
        return row, P
    raise RuntimeError("could not build item for plan %r" % (plan,))


def _check_item(row, P):
    """Independent re-derivation of the gold from the problem facts."""
    Q = P["Q"]
    post = _posterior_check(P)
    exact = P["post"]
    assert all(abs(float(a) - b) < 1e-9 for a, b in zip(exact, post))
    labels = P["labels"]
    if Q["kind"] == "argmax":
        g = max(range(len(post)), key=lambda i: post[i])
        assert row["gold"] == labels[g]
        gp = row["meta"]["gold_probs"]
        for i, lab in enumerate(labels):
            assert abs(gp[lab] - post[i]) < 1e-9
    elif Q["kind"] == "dist":
        ints = Q["gold_ints"]
        assert sum(ints) == 100
        assert all(abs(post[i] * 100 - ints[i]) < 1.0 + 1e-9 for i in range(len(ints)))
        parts = row["gold"]
        for i, lab in enumerate(labels):
            assert "%s %d%%" % (lab, ints[i]) in parts
    elif Q["kind"] == "bucket":
        cuts = _SCALES[Q["scale"]][0]
        gi = _bucket_alt(cuts, Q["sides"], post[Q["T"]])
        assert row["gold"].startswith("%d:" % gi), (row["gold"], gi)
    else:
        a = _noul_eval_alt(Q, post, P["prior"])
        assert int(a) == row["gold"], (Q["sub"], a, row["gold"])
    for ev in P["evs"]:
        if ev["kind"] == "gate":
            assert _gate_true_alt(ev["gate"]) == _gate_true(ev["gate"]) == ev["present"]
            assert _days_between_alt(ev["gate"]["d1"], ev["gate"]["d2"]) == (ev["gate"]["d2"] - ev["gate"]["d1"]).days \
                if ev["gate"]["type"] == "days" else True
    if P.get("rule"):
        r = P["rule"]
        assert _RULE_TT[(r["depth"], r["A"], r["B"])] == _rule_eval(r["depth"], r["A"], r["B"])


def _generate(n, seed):
    rng = random.Random(seed)
    plans = _plan(n, rng)
    rows, probs = [], []
    for i, plan in enumerate(plans):
        irng = random.Random(rng.randrange(2 ** 62))
        row, P = _make_item(irng, plan, i)
        _check_item(row, P)
        rows.append(row)
        probs.append(P)
    return rows, probs


def generate(n, seed):
    """Return n rows of the "evidence" family, deterministic in seed."""
    return _generate(n, seed)[0]


# =========================================================================
# self-test
# =========================================================================
_KEYS = {"state", "qtype", "instructions", "options", "gold", "card", "meta"}


def _validate(row):
    assert set(row.keys()) == _KEYS, row.keys()
    assert isinstance(row["state"], str) and row["state"]
    assert isinstance(row["instructions"], str) and row["instructions"]
    assert row["qtype"] in ("choice", "noul")
    m = row["meta"]
    assert set(m.keys()) <= {"family", "difficulty", "gold_probs", "mistakes"}
    assert m["family"] == FAMILY and m["difficulty"] in ("medium", "hard")
    if row["qtype"] == "choice":
        opts = row["options"]
        assert isinstance(opts, list) and 2 <= len(opts) <= 8 and len(set(opts)) == len(opts)
        assert all(isinstance(o, str) for o in opts)
        assert row["gold"] in opts
        if row["card"] is not None:
            assert isinstance(row["card"], str)
            assert all(line.startswith("- ") for line in row["card"].split("\n"))
    else:
        assert row["options"] is None and row["gold"] in (0, 1) and row["card"] is None
    if "gold_probs" in m:
        gp = m["gold_probs"]
        assert abs(sum(gp.values()) - 1.0) < 1e-9
        assert set(gp) == set(row["options"])
        assert max(gp, key=gp.get) == row["gold"]
        assert all(0 <= v <= 1 for v in gp.values())
    if "mistakes" in m:
        for kx, v in m["mistakes"].items():
            assert isinstance(v, str) and v
            if row["qtype"] == "choice":
                assert kx in row["options"] and kx != row["gold"], (kx, row["gold"])
            else:
                assert kx == str(1 - row["gold"])
    json.dumps(row)


def _selftest(n=300, seed=12345):
    rows, probs = _generate(n, seed)
    assert len(rows) == n
    for r in rows:
        _validate(r)
    rows2 = generate(n, seed)
    assert json.dumps(rows, sort_keys=True) == json.dumps(rows2, sort_keys=True), "not deterministic"
    rows3 = generate(20, seed + 1)
    assert json.dumps(rows[:20], sort_keys=True) != json.dumps(rows3, sort_keys=True)
    # stats
    L = [len(r["state"]) for r in rows]
    short = sum(1 for x in L if x < 600)
    med = sum(1 for x in L if 600 <= x <= 2500)
    lng = sum(1 for x in L if 2500 < x <= 6000)
    noul = [r for r in rows if r["qtype"] == "noul"]
    yes = sum(r["gold"] for r in noul)
    choice = [r for r in rows if r["qtype"] == "choice"]
    pos = {}
    for r in choice:
        i = r["options"].index(r["gold"])
        pos[i] = pos.get(i, 0) + 1
    doms = {}
    for P in probs:
        doms[P["dom"]["key"]] = doms.get(P["dom"]["key"], 0) + 1
    fmts = {}
    for P in probs:
        fmts[P["fmt"]] = fmts.get(P["fmt"], 0) + 1
    kinds = {}
    for P in probs:
        key = P["Q"]["kind"] + ("/" + P["Q"]["sub"] if P["Q"]["kind"] == "noul" else "")
        kinds[key] = kinds.get(key, 0) + 1
    hard = sum(1 for r in rows if r["meta"]["difficulty"] == "hard")
    with_gp = sum(1 for r in rows if "gold_probs" in r["meta"])
    bnd = sum(1 for P in probs if P.get("boundary") is not None)
    weak = sum(1 for P in probs if P["cat"] == "weak" and P["Q"]["kind"] == "argmax")
    mist = {}
    for r in rows:
        for v in r["meta"].get("mistakes", {}).values():
            mist[v] = mist.get(v, 0) + 1
    assert short + med + lng == n
    assert len(doms) >= 8
    print("SELF-TEST OK: %d rows" % n)
    print("  length: short(<600)=%d medium(600-2500)=%d long(2500-6000)=%d  min=%d max=%d" % (
        short, med, lng, min(L), max(L)))
    print("  qtype: choice=%d noul=%d  noul yes-rate=%.3f" % (len(choice), len(noul), yes / max(1, len(noul))))
    print("  question kinds:", dict(sorted(kinds.items())))
    print("  gold position (choice):", dict(sorted(pos.items())))
    print("  domains (%d):" % len(doms), dict(sorted(doms.items())))
    print("  formats:", dict(sorted(fmts.items())))
    print("  difficulty hard=%d medium=%d; with gold_probs=%d; exact-boundary items=%d; weak-evidence argmax=%d" % (
        hard, n - hard, with_gp, bnd, weak))
    print("  mistake tags:", dict(sorted(mist.items(), key=lambda x: -x[1])))
    return rows


if __name__ == "__main__":
    ex = generate(12, 7)
    shown = 0
    for want in ("short", "medium", "long"):
        for r in ex:
            L = len(r["state"])
            cls = "short" if L < 600 else ("medium" if L <= 2500 else "long")
            if cls == want:
                print("=" * 100)
                print(json.dumps(r, indent=2, ensure_ascii=False))
                shown += 1
                break
    print("=" * 100)
    _selftest()
