# -*- coding: utf-8 -*-
"""pg.temporal -- procedural generator of hard "System-One" decision problems whose
answer hinges on dates, times and durations (family "temporal").

Every gold answer is computed by a small rule engine from the generated facts and
re-checked by an independent code path (Julian-day-number / minute arithmetic instead
of datetime arithmetic).  Pure standard library, deterministic from the seed.

API:  generate(n, seed) -> list[dict]
Run:  python3 -m pg.temporal      (prints 3 examples and runs the self-test)
"""
import calendar
import datetime as dt
import json
import math
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

FAMILY = "temporal"
ONE = dt.timedelta(days=1)


class Retry(Exception):
    """Scenario was degenerate (e.g. no mistake changes the answer); draw again."""


# ----------------------------------------------------------------------------- basics
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
MON3 = [m[:3] for m in MONTHS]
WDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
NUMW = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
        9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 14: "fourteen", 15: "fifteen",
        20: "twenty", 21: "twenty-one", 28: "twenty-eight", 30: "thirty", 45: "forty-five",
        60: "sixty", 90: "ninety"}


def pick(rng, xs):
    return xs[rng.randrange(len(xs))]


def cap(s):
    return s[:1].upper() + s[1:]


def an(w):
    return ("an " if w[:1].lower() in "aeiou" else "a ") + w


def ordinal(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)


def fdate(d, style):
    if style == 0:
        return d.isoformat()
    if style == 1:
        return "%d %s %d" % (d.day, MONTHS[d.month - 1], d.year)
    if style == 2:
        return "%s %d, %d" % (MONTHS[d.month - 1], d.day, d.year)
    if style == 3:
        return "%s %d %s %d" % (WDAYS[d.weekday()][:3], d.day, MON3[d.month - 1], d.year)
    if style == 4:
        return "%02d-%s-%d" % (d.day, MON3[d.month - 1], d.year)
    if style == 5:
        return "%s, %d %s %d" % (WDAYS[d.weekday()], d.day, MONTHS[d.month - 1], d.year)
    return "%s, %s %d, %d" % (WDAYS[d.weekday()], MONTHS[d.month - 1], d.day, d.year)


def ftime(h, m, style):
    if style == 1:
        hh = h % 12 or 12
        return "%d:%02d %s" % (hh, m, "am" if h < 12 else "pm")
    if style == 2:
        return "%02d%02d hrs" % (h, m)
    return "%02d:%02d" % (h, m)


def fofs(o):
    s = "+" if o >= 0 else "-"
    return "UTC%s%02d:%02d" % (s, abs(o) // 60, abs(o) % 60)


def money(x, cur="$"):
    if isinstance(x, Fraction):
        q = Decimal(x.numerator) / Decimal(x.denominator)
    else:
        q = Decimal(x)
    q = q.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return "%s%s" % (cur, "{:,.2f}".format(q))


def rand_date(rng, y0=2025, y1=2028):
    return dt.date(rng.randint(y0, y1), 1, 1) + ONE * rng.randrange(365)


def hrs(n):
    return "%d hour%s" % (n, "" if n == 1 else "s")


def note_value(rng, reason, val):
    lead = pick(rng, ["", "Quick check: ", "FYI - ", "My read: ", "Heads-up: "])
    tail = pick(rng, ["so the answer is %s." % val, "which gives %s." % val, "so I'd put %s." % val])
    r = reason if lead else cap(reason)
    return "%s%s, %s" % (lead, r, tail)


def dur_days(rng, n):
    r = rng.random()
    if n % 7 == 0 and r < 0.3:
        w = n // 7
        return "%s week%s" % (NUMW.get(w, str(w)), "" if w == 1 else "s")
    if n in NUMW and r < 0.55:
        return "%s (%d) days" % (NUMW[n], n)
    return "%d days" % n


class Fmt(object):
    """Per-item formatting choices."""

    def __init__(self, rng):
        self.ds = pick(rng, [0, 0, 1, 1, 2, 2, 3, 4, 5, 6])
        self.ts = pick(rng, [0, 0, 0, 1, 2])
        self.ods = pick(rng, [0, 1, 2, 5])

    def d(self, x):
        return fdate(x, self.ds)

    def od(self, x):
        return fdate(x, self.ods)

    def t(self, h, m):
        return ftime(h, m, self.ts)

    def dtm(self, x):
        return "%s %s" % (self.d(x.date()), self.t(x.hour, x.minute))


# ------------------------------------------------ independent calendar arithmetic (JDN)
def jdn(y, m, d):
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    return d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4 - y2 // 100 + y2 // 400 - 32045


def jdn_date(x):
    return jdn(x.year, x.month, x.day)


def jdn_to_ymd(j):
    a = j + 32044
    b = (4 * a + 3) // 146097
    c = a - 146097 * b // 4
    d = (4 * c + 3) // 1461
    e = c - 1461 * d // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = 100 * b + d - 4800 + m // 10
    return year, month, day


def jdn_to_date(j):
    return dt.date(*jdn_to_ymd(j))


def is_leap(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def dim(y, m):
    return [31, 29 if is_leap(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]


def j_isb(j, hj, wk):
    return (j % 7) not in wk and j not in hj


def j_count(ja, jb, hj, wk):
    """business days in (ja, jb] by whole-week arithmetic (independent of datetime)."""
    if jb <= ja:
        return 0
    n = jb - ja
    full, rem = divmod(n, 7)
    c = full * (7 - len(wk))
    base = ja + full * 7
    for k in range(1, rem + 1):
        if (base + k) % 7 not in wk:
            c += 1
    for h in hj:
        if ja < h <= jb and h % 7 not in wk:
            c -= 1
    return c


def j_add_b(jE, n, hj, wk):
    j = jE + n
    while j_count(jE, j, hj, wk) < n:
        j += 1
    return j


def j_next_b(j, hj, wk):
    j += 1
    while not j_isb(j, hj, wk):
        j += 1
    return j


def j_roll(j, hj, wk=(5, 6)):
    while not j_isb(j, hj, wk):
        j += 1
    return j


# ------------------------------------------------------ primary calendar arithmetic
def is_bday(d, hs, wk=(5, 6)):
    return d.weekday() not in wk and d not in hs


def next_bday_after(d, hs, wk=(5, 6)):
    x = d + ONE
    while not is_bday(x, hs, wk):
        x += ONE
    return x


def roll_fwd(d, hs, wk=(5, 6)):
    while not is_bday(d, hs, wk):
        d += ONE
    return d


def add_bdays(d, n, hs, wk=(5, 6)):
    x, k = d, 0
    while k < n:
        x += ONE
        if is_bday(x, hs, wk):
            k += 1
    return x


def sub_bdays(d, n, hs, wk=(5, 6)):
    x, k = d, 0
    while k < n:
        x -= ONE
        if is_bday(x, hs, wk):
            k += 1
    return x


def bdays_between(a, b, hs, wk=(5, 6)):
    c, x = 0, a
    while x < b:
        x += ONE
        if is_bday(x, hs, wk):
            c += 1
    return c


def add_months(d, k):
    y, m = divmod(d.month - 1 + k, 12)
    y += d.year
    m += 1
    return dt.date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def add_months_indep(d, k):
    idx = d.year * 12 + (d.month - 1) + k
    y, m0 = idx // 12, idx % 12
    last = dim(y, m0 + 1)
    return dt.date(y, m0 + 1, d.day if d.day <= last else last)


def add_months_overflow(d, k):
    y, m = divmod(d.month - 1 + k, 12)
    y += d.year
    m += 1
    last = calendar.monthrange(y, m)[1]
    if d.day <= last:
        return dt.date(y, m, d.day)
    return dt.date(y, m, last) + ONE * (d.day - last)


def add_months_drift(d, k):
    x = d
    for _ in range(k):
        x = add_months(x, 1)
    return x


def month_exists(d, k):
    y, m = divmod(d.month - 1 + k, 12)
    return d.day <= calendar.monthrange(y + d.year, m + 1)[1]


def last_of_month(y, m):
    return dt.date(y, m, calendar.monthrange(y, m)[1])


def utc_of(d, h, m, off):
    return dt.datetime(d.year, d.month, d.day, h, m,
                       tzinfo=dt.timezone(dt.timedelta(minutes=off))).astimezone(dt.timezone.utc)


def j_umin(d, h, m, off):
    return jdn_date(d) * 1440 + h * 60 + m - off


def local_of(u, off):
    x = u.astimezone(dt.timezone(dt.timedelta(minutes=off)))
    return x.date(), x.hour, x.minute


def naive_min(d, h, m):
    return jdn_date(d) * 1440 + h * 60 + m


# ----------------------------------------------------------------------- word pools
PEOPLE = ["Priya Nair", "Tomasz Kowalski", "Amara Okafor", "Lucas Moreau", "Mei Lin", "Diego Hernandez",
          "Sarah Goldberg", "Kwame Mensah", "Yuki Tanaka", "Fatima Al-Sayed", "Olivia Bennett",
          "Rahul Deshpande", "Ingrid Larsen", "Chen Wei", "Aisha Bello", "Mateo Rossi", "Hannah Schmidt",
          "Jamal Carter", "Elena Petrova", "Noah Fischer", "Grace Kim", "Oscar Lindqvist", "Zanele Dlamini",
          "Arjun Mehta", "Sofia Marquez", "Liam O'Connor", "Nadia Haddad", "Kenji Watanabe", "Beatriz Souza",
          "Emeka Obi"]
JUNIOR = ["trainee adjuster", "summer intern", "temp agency staff member", "junior analyst (still in onboarding)",
          "front-desk associate", "new starter (week 2)", "contractor without approval authority",
          "customer service rep (not authorised to make determinations)", "student placement",
          "shadowing trainee"]
SENIOR = ["Operations Lead", "Team Manager", "Senior Case Officer", "Compliance Manager", "Head of Service",
          "Duty Supervisor"]
HOLIDAY_NAMES = ["Founders' Day", "Civic Holiday", "Heritage Day", "Spring Bank Holiday", "Midsummer Holiday",
                 "Harvest Day", "Unity Day", "Remembrance Day", "Regional Public Holiday", "Company Wellness Day",
                 "National Day", "Late Summer Holiday", "Reconciliation Day", "Mountain Day", "Lantern Festival"]
PLACES = ["Port Aldren", "Kelmsford", "Varenna Bay", "New Halden", "Sorrento Ridge", "Maribel", "Oakhaven",
          "Tessaly", "Quillon", "Ardmere", "Brightwater", "Loch Carron", "Sundermere", "Castor Point"]
OFFSETS = [-480, -420, -360, -300, -240, -180, 0, 60, 120, 180, 240, 330, 345, 480, 540, 570, 600, 660, 780]


def make_holidays(rng, must, lo, hi, n_extra=2, wk=(5, 6), allow_weekend=False):
    hol = []
    for m in must:
        if m not in hol:
            hol.append(m)
    tries = 0
    target = len(hol) + n_extra
    span = max(1, (hi - lo).days)
    while len(hol) < target and tries < 80:
        tries += 1
        d = lo + ONE * rng.randint(0, span)
        if (allow_weekend or d.weekday() not in wk) and d not in hol:
            hol.append(d)
    hol.sort()
    return hol


def hol_text(rng, F, hols):
    names = rng.sample(HOLIDAY_NAMES, len(hols))
    return "; ".join("%s (%s)" % (F.d(h), n) for h, n in zip(hols, names))


# ------------------------------------------------------------- irrelevant material
DOMAIN_FILLER = {
    "insurance": ["Salvage recovered after settlement belongs to the insurer.",
                  "Loss adjusters are appointed for property claims above $15,000.",
                  "Policyholders must take reasonable steps to prevent further damage.",
                  "Fraudulent claims void the policy from the date of the fraudulent act.",
                  "Excess amounts are shown on the policy schedule."],
    "retail": ["Items must be returned with all original accessories.",
               "Personalised items cannot be returned unless faulty.",
               "Refunds are issued to the original payment method where possible.",
               "Gift receipts entitle the holder to an exchange or store credit only.",
               "We do not accept returns of opened hygiene products."],
    "hr": ["Employees may be accompanied at any hearing by a colleague or union representative.",
           "Minutes of grievance meetings are shared within five working days.",
           "Overtime must be approved in advance by the line manager.",
           "Travel to hearings is paid at the standard mileage rate.",
           "Flexible working requests are handled under a separate procedure."],
    "benefits": ["Claimants must report changes in household composition.",
                 "Overpayments may be recovered from future benefit.",
                 "Interpreters are provided free of charge at hearings.",
                 "Identity documents must be originals or certified copies.",
                 "Home visits may be arranged for claimants with limited mobility."],
    "banking": ["Card PINs must never be shared, including with bank staff.",
                "Foreign transaction fees are disclosed in the tariff of charges.",
                "Statements are available online for seven years.",
                "Joint account holders are jointly and severally liable.",
                "Contactless limits are set by the card scheme."],
    "travel": ["Economy class is the standard for flights under six hours.",
               "Alcohol is not reimbursable.",
               "Receipts are required for any single item above $25.",
               "Mileage is reimbursed at the published rate per mile.",
               "Hotel bookings must be made through the approved travel portal."],
    "education": ["Students must use their institutional email for all correspondence.",
                  "Academic misconduct cases are handled by the Conduct Panel.",
                  "Transcripts show all attempts at a module.",
                  "Reasonable adjustments are arranged through Disability Services.",
                  "Library fines do not affect academic standing."],
    "manufacturing": ["Nonconforming material must be tagged red and segregated.",
                      "First-article inspection reports are retained for ten years.",
                      "Supplier corrective action requests use form SQ-8D.",
                      "Packaging must meet the ISTA 2A drop test.",
                      "Changes to sub-tier suppliers require written approval."],
    "healthcare": ["Claims must include a valid NPI for the rendering provider.",
                   "Modifier 25 requires separate documentation.",
                   "Interpreter services are billed under code T1013.",
                   "Patients may request a copy of their records in writing.",
                   "Referrals are valid for the specialist named on the referral."],
    "logistics": ["Parcels over 30 kg are carried by the freight network.",
                  "Signature on delivery can be waived in the tracking app.",
                  "Dangerous goods must be declared at booking.",
                  "Redelivery can be requested up to three times.",
                  "Customs duties are the responsibility of the recipient."],
    "telecom": ["Planned maintenance is announced on the status page.",
                "Data allowances reset at the start of each billing cycle.",
                "Handsets remain the property of the provider until paid off.",
                "Roaming charges are listed in the international tariff.",
                "Fair-use limits apply to unlimited plans."],
    "compliance": ["Personal data must be minimised to what is necessary.",
                   "Processing records are reviewed annually by the DPO.",
                   "Staff complete data protection training every year.",
                   "Encryption at rest is mandatory for customer databases.",
                   "Vendor due diligence is refreshed every two years."],
    "housing": ["Tenants must not sublet without written consent.",
                "Smoke alarms are tested at the start of each tenancy.",
                "Pets require prior written approval.",
                "Bins are collected on the published schedule.",
                "Keys must be returned at the end of the tenancy."],
    "saas": ["Customer data is hosted in the region selected at sign-up.",
             "API rate limits are published in the developer documentation.",
             "Single sign-on is available on Enterprise plans.",
             "Feature requests are reviewed quarterly.",
             "Status updates are posted on the public status page."],
    "it": ["Password resets are self-service through the portal.",
           "Personal devices must be enrolled before accessing email.",
           "Software requests need line-manager approval.",
           "Shared drives are backed up nightly.",
           "Printers are managed by the facilities team."],
    "security": ["Customer must keep an up-to-date escalation contact list.",
                 "Threat intelligence reports are issued monthly.",
                 "Log retention is 13 months.",
                 "Penetration tests are scheduled annually.",
                 "Agents must be kept within two versions of the latest release."],
    "facilities": ["Contractors must sign in at reception.",
                   "Hot works require a permit.",
                   "Fire doors must not be wedged open.",
                   "Asbestos surveys are held by the facilities office.",
                   "Lift servicing is carried out monthly."],
}


_AVOID = []


def _ppl(rng):
    """a person name for filler text that never collides with a name in the case facts."""
    return pick(rng, [x for x in PEOPLE if x not in _AVOID] or PEOPLE)


def _f_contact(rng, org, dom, F):
    p = _ppl(rng)
    return ("Contacts", "Questions about this procedure go to %s (%s), extension %d, or the shared mailbox "
            "listed on the intranet. Out-of-hours queries are answered the next working day." %
            (p, pick(rng, SENIOR), rng.randint(2000, 7999)))


def _f_confid(rng, org, dom, F):
    return ("Confidentiality", "This document is for internal use by %s staff. Do not forward outside the "
            "organisation. Printed copies are uncontrolled; always check the intranet for the latest issue." % org)


def _f_revhist(rng, org, dom, F):
    y = rng.randint(2019, 2024)
    rows = []
    for i in range(rng.randint(2, 4)):
        d = dt.date(y + i, rng.randint(1, 12), rng.randint(1, 28))
        rows.append("  rev %d.%d  %s  %s" % (1 + i, rng.randint(0, 3), d.isoformat(),
                                             pick(rng, ["editorial corrections only", "updated contact details",
                                                        "reformatted tables", "fixed typographical errors",
                                                        "added accessibility statement"])))
    return ("Revision history (editorial; no change to any time limit)", "\n".join(rows))


def _f_other_cases(rng, org, dom, F):
    rows = ["  Ref        Name                 Opened       Status"]
    for _ in range(rng.randint(3, 5)):
        d = rand_date(rng)
        rows.append("  %-10s %-20s %-12s %s" % ("%s-%d" % (pick(rng, ["REF", "CS", "Q", "INC"]), rng.randint(10000, 99999)),
                                             _ppl(rng)[:20], d.isoformat(),
                                             pick(rng, ["Closed", "Awaiting docs", "Escalated", "Closed - paid",
                                                        "Withdrawn", "On hold"])))
    return ("Other items in the queue (for information only; not under review)", "\n".join(rows))


def _f_domain_clauses(rng, org, dom, F):
    pool = DOMAIN_FILLER.get(dom) or DOMAIN_FILLER["compliance"]
    k = min(len(pool), rng.randint(2, 4))
    return ("General provisions", " ".join(rng.sample(pool, k)))


def _f_retention(rng, org, dom, F):
    return ("Record keeping", "All determinations, together with the evidence relied on, are kept for %d years "
            "after the case is closed and then securely destroyed. Paper files are scanned within %d working days." %
            (rng.randint(5, 10), rng.randint(2, 6)))


def _f_complaints(rng, org, dom, F):
    return ("Complaints about our service", "If you are unhappy with how we handled your case you can complain "
            "within %d months. We aim to reply within %d working days. This does not affect any separate "
            "appeal or review rights described elsewhere." % (rng.randint(3, 12), rng.randint(10, 20)))


def _f_system(rng, org, dom, F):
    d = rand_date(rng)
    return ("System notice", "The case management system will be unavailable on %s from %s to %s for an "
            "upgrade. Work captured on paper during the outage must be keyed in afterwards." %
            (F.d(d), F.t(22, 0), F.t(23, rng.choice([15, 30, 45]))))


def _f_fees(rng, org, dom, F):
    return ("Schedule of administrative fees", "Duplicate documents: $%d. Certified copies: $%d. Courier "
            "re-dispatch: $%d. Fees are reviewed each financial year and are not refundable." %
            (rng.randint(5, 15), rng.randint(15, 40), rng.randint(8, 25)))


def _f_access(rng, org, dom, F):
    return ("Accessibility", "This document is available in large print, audio and easy-read formats. Contact "
            "the accessibility team to request an alternative format or a sign-language interpreter.")


def _f_training(rng, org, dom, F):
    return ("Training reminder", "All staff handling cases must complete module %s-%d on the learning platform. "
            "Completion is tracked by team leaders monthly." % (pick(rng, ["QA", "OPS", "CX", "REG"]),
                                                                  rng.randint(100, 499)))


def _f_privacy(rng, org, dom, F):
    return ("Data protection", "%s processes personal data only as needed to administer this procedure. "
            "Individuals may request access to, or correction of, their data by writing to the Data "
            "Protection Officer." % org)


def _f_faq(rng, org, dom, F):
    qs = [("Can I nominate someone to act for me?", "Yes, with a signed authority form."),
          ("Do you accept scanned signatures?", "Yes, for all forms except the statutory declaration."),
          ("Where do I send original documents?", "To the central processing address; do not send them to branches."),
          ("Can I get a paper copy of my file?", "Yes, one copy per year free of charge."),
          ("Is parking available at the office?", "Limited visitor parking is available on request.")]
    k = rng.randint(2, 3)
    return ("Frequently asked questions", "\n".join("Q: %s\nA: %s" % qa for qa in rng.sample(qs, k)))


def _f_hours(rng, org, dom, F):
    return ("Contact centre opening hours", "Phone lines: %s-%s Monday to %s. Web chat: %s-%s every day. "
            "Opening hours are for enquiries only; they are not relevant to how any period in this document is counted." %
            (F.t(8, 0), F.t(pick(rng, [18, 19, 20]), 0), pick(rng, ["Friday", "Saturday"]), F.t(7, 0), F.t(22, 0)))


def _f_escalation(rng, org, dom, F):
    rows = ["  Level 1  %-18s  first-line review" % _ppl(rng), "  Level 2  %-18s  %s" % (_ppl(rng), pick(rng, SENIOR)),
            "  Level 3  %-18s  director sign-off" % _ppl(rng)]
    return ("Escalation matrix", "\n".join(rows))


def _f_glossary(rng, org, dom, F):
    g = [("Determination", "the formal outcome recorded on the case"), ("Case owner", "the officer responsible for the file"),
         ("Evidence", "any document relied on in reaching a determination"), ("Portal", "the secure online account"),
         ("Representative", "a person authorised in writing to act for the customer"), ("Reference", "the unique case identifier")]
    k = rng.randint(3, 4)
    return ("Glossary", "\n".join("%s - %s." % x for x in rng.sample(g, k)))


def _f_disclaimer(rng, org, dom, F):
    return ("Disclaimer", "This summary is provided for convenience. If there is any conflict between this summary and the "
            "full terms, the full terms prevail. Nothing in this document affects statutory rights.")


def _f_minutes(rng, org, dom, F):
    d = rand_date(rng)
    return ("Extract from team meeting minutes (%s)" % F.d(d), "Attendees discussed the backlog, the new scanning vendor "
            "and holiday cover. Action: %s to update the shared rota. No changes to procedure were agreed." % _ppl(rng))


FILLERS = [_f_hours, _f_escalation, _f_glossary, _f_disclaimer, _f_minutes, _f_contact, _f_confid, _f_revhist, _f_other_cases, _f_domain_clauses, _f_retention, _f_complaints,
           _f_system, _f_fees, _f_access, _f_training, _f_privacy, _f_faq]


# ------------------------------------------------------------------ rendering
def r_rules(rng, head, rules, style, secno):
    if style == "prose":
        return "%s\n%s" % (head, " ".join(rules))
    if style == "bullets":
        b = pick(rng, ["- ", "* ", "• "])
        return "%s\n%s" % (head, "\n".join(b + r for r in rules))
    if style == "numbered":
        return "%d. %s\n%s" % (secno, head, "\n".join("%d.%d %s" % (secno, i + 1, r) for i, r in enumerate(rules)))
    return "%s\n%s" % (head, "\n".join("(%s) %s" % (chr(97 + i), r) for i, r in enumerate(rules)))


def r_facts(rng, facts, prose, style):
    if style == "prose" and prose:
        return prose
    if style == "table":
        w = max(len(k) for k, _ in facts)
        vw = max(len(v) for _, v in facts)
        lines = ["%s | %s" % ("Field".ljust(w), "Value"), "%s-+-%s" % ("-" * w, "-" * min(vw, 40))]
        lines += ["%s | %s" % (k.ljust(w), v) for k, v in facts]
        return "\n".join(lines)
    if style == "json":
        return json.dumps(dict((k, v) for k, v in facts), indent=2, ensure_ascii=False)
    if style == "kv":
        return "\n".join("%s: %s" % (k, v) for k, v in facts)
    if style == "inline":
        return "; ".join("%s: %s" % (k, v) for k, v in facts) + "."
    return "\n".join("- %s: %s" % (k, v) for k, v in facts)


def r_note(rng, note):
    kind, author, text = note
    if kind == "system":
        return "%s (automated pre-check, not a determination): %s" % (author, text)
    if kind == "customer":
        return "Message from %s: \"%s\"" % (author, text)
    return "Note from %s: %s" % (author, text)


def render_state(rng, sc, size, parts):
    """parts: dict(wrap, rfmt, ffmt, note, extras) -> state text."""
    F = sc["F"]
    rules_block = r_rules(rng, sc["head"], sc["rules"], parts["rfmt"], parts["secno"])
    old_block = None
    if sc.get("old"):
        oh, orules = sc["old"]
        old_block = r_rules(rng, oh, orules, "prose" if parts["rfmt"] == "prose" else "bullets", parts["secno"])
    facts_block = r_facts(rng, sc["facts"], sc.get("prose"), parts["ffmt"])
    note = parts["note"]
    extras = parts["extras"]
    title = sc["title"]
    wrap = parts["wrap"]
    fh = parts["facts_head"]
    ex_txt = ["%s\n%s" % (h, b) for h, b in extras]
    if wrap == "email":
        s = sc["sender"]
        lines = ["From: %s <%s@%s.example>" % (s, s.split()[0].lower(), sc["org"].split()[0].lower().strip(",.")),
                 "To: %s" % parts["team"], "Subject: %s" % sc["subject"], "",
                 "Hi all,", "", parts["intro"], "", fh, facts_block, "",
                 "Relevant text, copied from \"%s\":" % title, rules_block]
        if old_block:
            lines += ["", old_block]
        for e in ex_txt:
            lines += ["", e]
        lines += ["", "Thanks,", s]
        if note:
            lines += ["", "-----", "Reply:", r_note(rng, note)]
        return "\n".join(lines)
    if wrap == "ticket":
        lines = ["[%s] %s | %s" % (parts["system"], sc["cid"], sc["subject"]),
                 "Status: awaiting determination | Queue: %s" % parts["team"], "---", facts_block, "---",
                 "Linked guidance: %s" % title, rules_block]
        if old_block:
            lines += ["", old_block]
        for e in ex_txt:
            lines += ["---", e]
        if note:
            lines += ["---", "Comments:", r_note(rng, note)]
        return "\n".join(lines)
    if wrap == "memo":
        lines = ["MEMORANDUM", "To: %s" % parts["team"], "From: %s, %s" % (sc["sender"], pick(rng, SENIOR)),
                 "Re: %s" % sc["subject"], "", "Extract from %s:" % title, rules_block]
        if old_block:
            lines += ["", old_block]
        blocks = [fh + "\n" + facts_block] + ex_txt
        for b in blocks:
            lines += ["", b]
        if note:
            lines += ["", r_note(rng, note)]
        return "\n".join(lines)
    # plain document
    blocks = [rules_block]
    if old_block:
        blocks.append(old_block)
    tail = [fh + "\n" + facts_block]
    if note:
        tail.append(r_note(rng, note))
    mid = list(ex_txt)
    pre = []
    if mid and rng.random() < 0.5:
        pre.append(mid.pop(0))
    body = pre + blocks + mid[: len(mid) // 2] + tail + mid[len(mid) // 2:]
    return title + "\n\n" + "\n\n".join(body)


def choose_parts(rng, sc, size):
    ffs = ["bullets", "table", "json", "kv"] + (["prose", "prose"] if sc.get("prose") else [])
    parts = dict(
        wrap=pick(rng, ["doc", "doc", "doc", "email", "ticket", "memo"]) if size != "short" else pick(rng, ["doc", "doc", "ticket"]),
        rfmt=pick(rng, ["prose", "bullets", "numbered", "lettered"]),
        ffmt=pick(rng, ffs if size != "short" else [f for f in ffs if f in ("prose", "kv", "bullets")]),
        secno=rng.randint(2, 9),
        team=pick(rng, ["Case Review Team", "Operations", "Determinations Desk", "Service Assurance", "Back Office",
                        "Quality Team"]),
        system=pick(rng, ["CaseHub", "Servio", "TrackOne", "DeskFlow", "OpsBoard"]),
        intro=pick(rng, ["Can someone confirm the outcome on this one before I close it?",
                         "Please decide this case today; details below.",
                         "Flagging this for a determination. I have pasted the policy text underneath.",
                         "Customer is chasing. Need a decision on the case below."]),
        facts_head=pick(rng, ["Case details", "Record under review", "Facts", "Case file", "Details of the case",
                              "Record"]) + ":",
        note=None, extras=[])
    return parts


def build_state(rng, sc, size):
    ftxt = " ".join(v for _, v in sc["facts"])
    _AVOID[:] = [x for x in PEOPLE if x in ftxt or x.split()[0] in ftxt]
    if sc.get("sender") and sc["sender"] in ftxt:
        sc["sender"] = pick(rng, [p_ for p_ in PEOPLE if p_ not in ftxt])
    parts = choose_parts(rng, sc, size)
    notes = sc.get("notes") or []
    pnote = {"short": 0.3, "medium": 0.55, "long": 0.75}[size]
    if notes and rng.random() < pnote:
        m, text = pick(rng, notes)
        kind = pick(rng, ["person", "person", "person", "system"])
        if kind == "system":
            parts["note"] = ("system", pick(rng, ["AutoCheck", "RulesBot v1", "Triage macro"]), text)
        else:
            parts["note"] = ("person", "%s, %s" % (_ppl(rng), pick(rng, JUNIOR)), text)
        parts["note_mistake"] = m
    pool = [f for f in FILLERS]
    rng.shuffle(pool)
    dom = sc["domain"]

    def gen_extra():
        f = pool.pop() if pool else pick(rng, [_f_other_cases, _f_domain_clauses, _f_system])
        return f(rng, sc["org"], dom, sc["F"])

    if size == "short":
        st = render_state(rng, sc, size, parts)
        if len(st) >= 600 and parts["note"]:
            parts["note"] = None
            st = render_state(rng, sc, size, parts)
        if len(st) >= 600 and parts["ffmt"] != "kv":
            parts["ffmt"] = "kv"
            st = render_state(rng, sc, size, parts)
        if len(st) >= 600 and parts["rfmt"] != "prose":
            parts["rfmt"] = "prose"
            st = render_state(rng, sc, size, parts)
        if len(st) >= 600:
            parts["ffmt"] = "inline"
            parts["wrap"] = "doc"
            st = render_state(rng, sc, size, parts)
        return (st, parts) if len(st) < 600 else (None, parts)
    if size == "medium":
        for _ in range(pick(rng, [0, 1, 1, 2])):
            parts["extras"].append(gen_extra())
        st = render_state(rng, sc, size, parts)
        guard = 0
        while len(st) < 600 and guard < 6:
            guard += 1
            parts["extras"].append(gen_extra())
            st = render_state(rng, sc, size, parts)
        while len(st) > 2500 and parts["extras"]:
            parts["extras"].pop()
            st = render_state(rng, sc, size, parts)
        if len(st) > 2500 and parts["note"]:
            parts["note"] = None
            st = render_state(rng, sc, size, parts)
        return (st, parts) if 600 <= len(st) <= 2500 else (None, parts)
    target = rng.randint(2700, 5600)
    st = render_state(rng, sc, size, parts)
    guard = 0
    while len(st) < target and guard < 30:
        guard += 1
        parts["extras"].append(gen_extra())
        st2 = render_state(rng, sc, size, parts)
        if len(st2) > 6000:
            parts["extras"].pop()
            break
        st = st2
    st = render_state(rng, sc, size, parts)
    return (st, parts) if 2500 <= len(st) <= 6000 else (None, parts)


Q_CHOICE_TAIL = ["Choose one option.", "Select the single correct option.", "Answer with exactly one of the listed options.",
                 "Pick the best answer from the options.", "Select one."]
Q_NOUL_TAIL = ["Answer 1 for yes or 0 for no.", "Reply 1 (yes) or 0 (no).", "Output 1 if yes, 0 if no.",
               "Answer 1 = yes, 0 = no."]


def finalize(rng, sc, qtype, target, size):
    st, parts = build_state(rng, sc, size)
    if st is None:
        return None
    traps = list(sc.get("traps", []))
    if parts["note"]:
        traps.append("misleading_note")
    if parts["extras"] or size == "long":
        traps.append("irrelevant_sections")
    card = None
    meta = {"family": FAMILY}
    if qtype == "choice":
        k = pick(rng, sc["kinds"])
        opts = list(k["opts"])
        gold = k["gold"]
        mis = dict(k.get("mis", {}))
        if len(opts) > 8:
            keep = [gold] + [o for o in opts if o != gold and o in mis][:7]
            if len(keep) < 8:
                keep += [o for o in opts if o not in keep][: 8 - len(keep)]
            opts = keep
        if len(opts) < 2:
            return None
        rng.shuffle(opts)
        if k.get("kind") == "label" and rng.random() < 0.3:
            pre = pick(rng, ["OUT", "DET", "RES", "CODE", "R"])
            codes = ["%s-%d" % (pre, i + 1) for i in range(len(opts))]
            rng.shuffle(codes)
            cmap = dict(zip(opts, codes))
            card = "\n".join("- %s: %s" % (cmap[o], o) for o in sorted(opts, key=lambda o: cmap[o]))
            mis = dict((cmap[o], v) for o, v in mis.items() if o in cmap)
            gold = cmap[gold]
            opts = [cmap[o] for o in opts]
            q = k["q"] + " (Answer with the outcome code from the card.)"
        else:
            q = k["q"]
            mis = dict((o, v) for o, v in mis.items() if o in opts)
        instr = q + "\n" + pick(rng, Q_CHOICE_TAIL)
        options = opts
    else:
        cands = [(q, a) for q, a in sc.get("yn", []) if a == target]
        if cands and rng.random() < 0.6:
            q, _ = pick(rng, cands)
        else:
            k = pick(rng, sc["kinds"])
            if target == 1:
                opt = k["gold"]
            else:
                wrong = [o for o in k["opts"] if o != k["gold"]]
                named = [o for o in wrong if o in k.get("mis", {})]
                if not wrong:
                    return None
                opt = pick(rng, named if named and rng.random() < 0.8 else wrong)
            disp = opt.split(": ", 1)[1] if (opt[:1].isdigit() and ": " in opt[:4]) else opt
            q = k["prop"].format(opt=disp)
        instr = q + "\n" + pick(rng, Q_NOUL_TAIL)
        options, gold, mis = None, target, {}
    core = set(t for t in traps if t != "irrelevant_sections")
    score = len(core) + (1 if size == "long" else 0) + (1 if "misleading_note" in core and "boundary" in core else 0)
    meta["difficulty"] = "hard" if score >= 4 else "medium"
    if mis:
        meta["mistakes"] = mis
    row = {"state": st, "qtype": qtype, "instructions": instr, "options": options, "gold": gold}
    if card:
        row["card"] = card
    row["meta"] = meta
    row["_tpl"] = sc["tpl"]
    row["_domain"] = sc["domain"]
    row["_checked"] = bool(sc.get("checked"))
    return row


def mk_scn(**kw):
    kw.setdefault("traps", [])
    kw.setdefault("notes", [])
    kw.setdefault("yn", [])
    kw.setdefault("old", None)
    kw.setdefault("prose", None)
    return kw


def note_text(rng, reason, wrong):
    lead = pick(rng, ["", "Quick check: ", "FYI - ", "My read: ", "Heads-up: ", "Looked at this: "])
    tail = pick(rng, ["so the outcome should be \"%s\"." % wrong, "so I'd record \"%s\"." % wrong,
                      "which means \"%s\"." % wrong, "so this is \"%s\" - can we close it?" % wrong])
    r = reason if lead else cap(reason)
    return "%s%s, %s" % (lead, r, tail)


def label_kind(q, prop, labels, gold_idx, variants):
    """labels: list of option strings; variants: list of (mistake, idx)."""
    mis = {}
    for m, idx in variants:
        if idx != gold_idx and labels[idx] not in mis:
            mis[labels[idx]] = m
    return dict(kind="label", q=q, prop=prop, opts=list(labels), gold=labels[gold_idx], mis=mis)


def value_kind(kind, q, prop, gold_v, variants, fmt, fill=None):
    """variants: list of (mistake, value). fill: extra (mistake, value) used only if < 3 options."""
    g = fmt(gold_v)
    opts, mis = [g], {}
    for m, v in variants:
        s = fmt(v)
        if s not in opts:
            opts.append(s)
            mis[s] = m
    for m, v in (fill or []):
        if len(opts) >= 4:
            break
        s = fmt(v)
        if s not in opts:
            opts.append(s)
            mis[s] = m
    return dict(kind=kind, q=q, prop=prop, opts=opts[:8], gold=g, mis=dict((o, v) for o, v in mis.items() if o in opts[:8]))


def ordinal_labels(texts):
    return ["%d: %s" % (i, t) for i, t in enumerate(texts)]


# ============================================================ S1  filing deadlines
DL = [
    dict(key="insurance", orgs=["Harborview Mutual", "Kestrel Insurance Co.", "Bluestone Assurance"],
         doc="Claims Handling Manual", head="Notification of claims", sub="claim", subs="claims", recv="reported",
         trig="the date of loss", trig_s="the loss", trig_dn="date of loss", idp="CLM", actor="policyholder",
         T_key="Date of loss", S_key="Claim reported on",
         story="{name} suffered water damage from a burst pipe on {T}. The claim was reported {chan} on {S}.",
         chan=["by phone", "through the web portal", "via the broker"],
         labels=["Accept claim for processing", "Accept with 15% late-notice reduction", "Deny claim as untimely"],
         grace="A claim reported after the deadline but no more than {G} days after it is accepted subject to a 15% late-notice reduction of the settled amount.",
         W=[30, 45, 60], Wold=[30, 60, 90], G=[10, 14, 30],
         ext=dict(kind="add", E=[14, 30], text="If the insured was admitted to hospital at any time during the reporting period, that period is extended by {E} days.",
                  fact=("Hospital admission during reporting period", "Yes (discharge summary on file)", "None recorded")),
         excl=dict(kind="flag", text="The hospital extension does not apply to claims under the Travel Assistance rider.",
                   fact=("Cover section", "Travel Assistance rider", "Home Contents")),
         misc=[("Policy number", "HM-{n}"), ("Estimated loss", "${amt}")]),
    dict(key="retail", orgs=["Orchard & Pine Home Goods", "Brightcart", "Lumen Outfitters"],
         doc="Returns and Refunds Policy", head="Return window", sub="return", subs="returns", recv="received at our returns centre",
         trig="the delivery date", trig_s="delivery", trig_dn="delivery date", idp="RMA", actor="customer",
         T_key="Delivered", S_key="Return received at returns centre",
         story="{name}'s order was delivered on {T}. The parcel was sent back {chan} and received at the returns centre on {S}.",
         chan=["by courier", "through a drop-off point", "by post"],
         labels=["Full refund to original payment method", "Store credit only", "Return refused"],
         grace="Returns received after the return window has closed but no more than {G} days after it are accepted for store credit only.",
         W=[14, 28, 30], Wold=[14, 30, 60], G=[7, 14],
         ext=dict(kind="add", E=[15, 30], text="Members of the loyalty programme receive an additional {E} days.",
                  fact=("Loyalty member", "Yes (Plus tier)", "No")),
         excl=dict(kind="flag", text="The loyalty extension does not apply to electronics.",
                   fact=("Item category", "Electronics (wireless headphones)", "Home textiles (duvet cover)")),
         misc=[("Order value", "${amt}"), ("Order number", "OP-{n}")]),
    dict(key="hr", orgs=["Castellan Foods Ltd", "Norvale Engineering", "Pinecrest Hospital Trust"],
         doc="Employee Handbook - Grievance Procedure", head="Time limits for grievances", sub="grievance", subs="grievances", recv="filed",
         trig="the incident complained of", trig_s="the incident", trig_dn="incident date", idp="GRV", actor="employee",
         T_key="Incident date", S_key="Grievance filed",
         story="{name} objected to a shift-allocation decision made on {T}; the written grievance was filed {chan} on {S}.",
         chan=["by email to HR", "through the HR portal", "by hand to the line manager"],
         labels=["Accept grievance for a hearing", "Accept only with the HR Director's late-filing waiver", "Dismiss grievance as out of time"],
         grace="A grievance filed after the deadline but no more than {G} days after it may be heard only with a late-filing waiver from the HR Director.",
         W=[20, 21, 30], Wold=[14, 28, 42], G=[7, 10],
         ext=dict(kind="add", E=[10, 14], text="If the employee was on approved medical leave on the day the filing period would otherwise end, the period is extended by {E} days.",
                  fact=("On approved medical leave when the period ended", "Yes (fit note on file)", "No")),
         excl=dict(kind="flag", text="This extension is not available for grievances about rates of pay.",
                   fact=("Grievance subject", "Rate of pay (overtime rate)", "Shift allocation")),
         misc=[("Department", "Dispatch"), ("Employee number", "E{n}")]),
    dict(key="benefits", orgs=["Summit County Benefits Office", "Riverside Department of Social Services", "Eastmoor Housing Assistance Agency"],
         doc="Appeals Procedure", head="Time limit for appeals", sub="appeal", subs="appeals", recv="received",
         trig="the date printed on the decision notice", trig_s="the notice", trig_dn="notice date", idp="APL", actor="claimant",
         T_key="Decision notice date", S_key="Appeal received",
         story="A decision notice dated {T} was issued to {name}. The appeal form was received {chan} on {S}.",
         chan=["by post", "at the front counter", "through the online portal"],
         labels=["Appeal is timely - schedule a hearing", "Accept late appeal only on a finding of good cause", "Dismiss appeal as untimely"],
         grace="An appeal received after the deadline but no more than {G} days after it may be accepted only if good cause for the delay is shown.",
         W=[15, 30, 60], Wold=[10, 30, 90], G=[10, 30],
         ext=dict(kind="add", E=[5, 3], text="Where the decision notice was sent by post, {E} days are added to the appeal period.",
                  fact=("Notice delivery method", "Post (first class)", "Online account only")),
         excl=dict(kind="flag", text="The additional days for postal notices do not apply if the claimant had opted in to electronic notices, even where a paper copy was also posted.",
                   fact=("Opted in to electronic notices", "Yes", "No")),
         misc=[("Programme", "Housing support"), ("Case number", "SC-{n}")]),
    dict(key="banking", orgs=["Alder Street Bank", "Northfield Credit Union", "Crescent Savings"],
         doc="Card Dispute Procedures", head="Dispute window", sub="dispute", subs="disputes", recv="raised",
         trig="the statement date on which the transaction first appeared", trig_s="the statement", trig_dn="statement date", idp="DSP", actor="cardholder",
         T_key="Statement date (first appearance)", S_key="Dispute raised",
         story="The disputed charge first appeared on {name}'s statement dated {T}. {name} raised the dispute {chan} on {S}.",
         chan=["in the mobile app", "by phone", "in branch"],
         labels=["Open formal dispute with provisional credit", "Open goodwill review (no provisional credit)", "Decline - outside the dispute window"],
         grace="Disputes raised after the deadline but no more than {G} days after it may be handled as a goodwill review without provisional credit.",
         W=[45, 60, 90], Wold=[60, 120, 45], G=[15, 30],
         ext=dict(kind="add", E=[15, 30], text="If the cardholder was hospitalised or abroad without access to statements, the period is extended by {E} days on production of evidence.",
                  fact=("Evidence of hospitalisation or travel provided", "Yes (travel itinerary)", "No")),
         excl=dict(kind="flag", text="The extension is not available for disputes on business cards.",
                   fact=("Card type", "Business card", "Personal card")),
         misc=[("Disputed amount", "${amt}"), ("Card ending", "{n4}")]),
    dict(key="travel", orgs=["Meridian Consulting Group", "Talbot & Reyes LLP", "Quanta Analytics"],
         doc="Travel and Expense Policy", head="Submission deadline", sub="expense report", subs="expense reports", recv="submitted",
         trig="the last day of the trip", trig_s="the trip end", trig_dn="trip end date", idp="EXP", actor="employee",
         T_key="Trip end date", S_key="Expense report submitted",
         story="{name} returned from a client trip that ended on {T} and submitted the expense report {chan} on {S}.",
         chan=["in the expense tool", "by email to Finance", "through the mobile app"],
         labels=["Reimburse in full", "Reimburse only with VP approval", "Not reimbursable (late submission)"],
         grace="Reports submitted after the deadline but no more than {G} days after it may be reimbursed only with written VP approval.",
         W=[30, 45, 60], Wold=[60, 90, 30], G=[15, 30],
         ext=dict(kind="add", E=[15, 30], text="Employees on a field assignment longer than four weeks have {E} additional days.",
                  fact=("Field assignment longer than 4 weeks", "Yes", "No")),
         excl=dict(kind="flag", text="The field-assignment extension does not apply to corporate-card charges, which must always be reconciled within the standard period.",
                   fact=("Payment method", "Corporate card", "Personal card (out of pocket)")),
         misc=[("Report total", "${amt}"), ("Cost centre", "CC-{n}")]),
    dict(key="education", orgs=["Westbrook University", "Carroway College", "Lakeshore Institute of Technology"],
         doc="Academic Regulations - Grade Appeals", head="Time limit for grade appeals", sub="grade appeal", subs="grade appeals", recv="lodged",
         trig="the date the grade was posted", trig_s="grade posting", trig_dn="grade posting date", idp="GA", actor="student",
         T_key="Grade posted", S_key="Appeal lodged",
         story="{name}'s module grade was posted on {T}; the appeal was lodged {chan} on {S}.",
         chan=["through the registry portal", "by email to the registry", "in person at the registry desk"],
         labels=["Appeal accepted for review", "Accepted only with the Dean's waiver", "Appeal rejected as late"],
         grace="An appeal lodged after the deadline but no more than {G} days after it may be considered only with the Dean's written waiver.",
         W=[10, 14, 20], Wold=[7, 21, 28], G=[5, 7],
         ext=dict(kind="switch", req=True, T2_key="Marked work returned to student",
                  text="If the student requested the marked work, the appeal period instead runs from the date the marked work was returned to the student.",
                  fact=("Marked work requested", "Yes - requested on {R}", "No")),
         excl=dict(kind="after_base", text="That exception does not apply where the request for the marked work was made after the original appeal period had already expired."),
         misc=[("Module", "ECON{n3}"), ("Student ID", "S{n}")]),
    dict(key="manufacturing", orgs=["Kestrel Components", "Ironvale Fabrication", "Delta Precision Castings"],
         doc="Supplier Quality Agreement", head="Notification of nonconforming goods", sub="supplier claim", subs="supplier claims", recv="notified to the supplier",
         trig="the date the goods were received", trig_s="receipt", trig_dn="goods receipt date", idp="SQC", actor="buyer",
         T_key="Goods received", S_key="Claim notified to supplier",
         story="Lot L{n3} was received on {T}. A nonconformance claim was notified to the supplier {chan} on {S}.",
         chan=["via the supplier portal", "by formal letter", "by email to the supplier's quality manager"],
         labels=["Submit claim for full credit", "Submit as goodwill claim (50% credit)", "Claim time-barred - absorb the cost"],
         grace="Claims notified after the deadline but no more than {G} days after it may be submitted as goodwill claims at 50% credit.",
         W=[30, 45, 60], Wold=[30, 60, 90], G=[10, 15],
         ext=dict(kind="switch", T2_key="Defect discovered",
                  text="For latent defects that could not reasonably have been detected at receiving inspection, the period runs from the date the defect was discovered.",
                  fact=("Latent defect", "Yes (found during machining)", "No (visible at receiving)")),
         excl=dict(kind="flag", text="The latent-defect rule does not apply to lots accepted under a concession at receiving.",
                   fact=("Accepted under concession", "Yes (concession C-114)", "No")),
         misc=[("Part number", "PN-{n}"), ("Lot value", "${amt}")]),
    dict(key="healthcare", orgs=["Meridian Health Plan", "Crestview Health Partners", "Arbor Community Health"],
         doc="Provider Manual - Timely Filing", head="Timely filing limits", sub="claim", subs="claims", recv="received by the plan",
         trig="the date of service", trig_s="the service", trig_dn="date of service", idp="HCL", actor="provider",
         T_key="Date of service", S_key="Claim received",
         story="The patient ({name}) was seen on {T}. The provider's claim was received {chan} on {S}.",
         chan=["electronically (EDI 837)", "on a paper claim form", "through the clearinghouse"],
         labels=["Process claim", "Process with 20% timely-filing reduction", "Deny - timely filing limit exceeded"],
         grace="A claim received after the filing limit but no more than {G} days after it is processed with a 20% timely-filing reduction.",
         W=[90, 120, 180], Wold=[90, 180, 365], G=[15, 30],
         ext=dict(kind="switch", T2_key="Primary payer remittance date",
                  text="Where the plan is the secondary payer, the filing period runs from the date of the primary payer's remittance advice.",
                  fact=("Plan is secondary payer", "Yes", "No")),
         excl=dict(kind="flag", text="This does not apply where the primary payer denied the claim for its own timely-filing reasons.",
                   fact=("Primary payer outcome", "Denied - untimely filing", "Paid in part")),
         misc=[("Billed amount", "${amt}"), ("Member ID", "MH{n}")]),
]


def dl_compute(p, fl=()):
    use_old = False
    if p["ver"]:
        pivot = p["T"] if p["ver_mode"] == "trigger" else p["S"]
        use_old = pivot < p["EFF"]
        if "wrong_version" in fl:
            use_old = not use_old
    W = p["Wold"] if use_old else p["W"]
    conv = p["conv_old"] if use_old else p["conv"]
    if "off_by_one" in fl:
        conv = "excl" if conv == "incl" else "incl"
    span = W - (1 if conv == "excl" else 0)

    def last(trig, extra=0):
        L = trig + ONE * (span + extra)
        if p["roll"] and "ignored_rollover" not in fl:
            L = roll_fwd(L, p["holset"])
        return L

    L_base = last(p["T"])
    L = L_base
    if p["ext"] and p["ext_cond"]:
        if p["excl_kind"] == "flag":
            ex = p["excl_flag"]
        elif p["excl_kind"] == "after_base":
            ex = p["R"] > L_base
        else:
            ex = False
        on = not ex
        if "misapplied_extension" in fl:
            on = True
        if "forgot_extension" in fl:
            on = False
        if on:
            L = last(p["T2"]) if p["ext_kind"] == "switch" else last(p["T"], p["E"])
    S = p["S"]
    if S <= L:
        st = 0
    elif p["grace"] and "ignored_grace" not in fl and S <= L + ONE * p["G"]:
        st = 1
    else:
        st = 2
    return L, st


def dl_indep(p):
    hj = sorted(set(jdn_date(h) for h in p["hols"]))
    jT, jS = jdn_date(p["T"]), jdn_date(p["S"])
    old = False
    if p["ver"]:
        pv = jT if p["ver_mode"] == "trigger" else jS
        old = pv < jdn_date(p["EFF"])
    W, conv = (p["Wold"], p["conv_old"]) if old else (p["W"], p["conv"])
    span = W - (1 if conv == "excl" else 0)

    def rl(j):
        return j_roll(j, hj) if p["roll"] else j

    base = rl(jT + span)
    last = base
    if p["ext"] and p["ext_cond"]:
        if p["excl_kind"] == "flag":
            ex = p["excl_flag"]
        elif p["excl_kind"] == "after_base":
            ex = jdn_date(p["R"]) > base
        else:
            ex = False
        if not ex:
            last = rl(jdn_date(p["T2"]) + span) if p["ext_kind"] == "switch" else rl(jT + span + p["E"])
    late_days = jS - last
    if late_days <= 0:
        st = 0
    elif p["grace"] and late_days <= p["G"]:
        st = 1
    else:
        st = 2
    return jdn_to_date(last), st


def dl_window_sentence(rng, D, W, conv):
    fm = dict(sub=D["sub"], Subs=cap(D["subs"]), recv=D["recv"], trig=D["trig"], trig_s=D["trig_s"],
              Wt=dur_days(rng, W), Word=ordinal(W), Asub=cap(an(D["sub"])), asub=an(D["sub"]))
    if conv == "incl":
        opts = [("{Subs} must be {recv} within {Wt} after {trig}.", False, True),
                ("{Asub} must be {recv} no later than {Wt} after {trig}.", False, True),
                ("{Asub} is in time if it is {recv} on or before the {Word} day following {trig}.", False, False),
                ("No {sub} shall be treated as late unless it is {recv} more than {Wt} after {trig}.", True, True)]
    else:
        opts = [("{Subs} must be {recv} within {Wt} of {trig}, counting the day of {trig_s} as day 1.", False, False),
                ("{Asub} must be {recv} before the {Word} day after {trig}; one {recv} on that day or later is late.", False, False),
                ("{Asub} {recv} on or after the {Word} day following {trig} is out of time.", False, False),
                ("No {sub} may be treated as timely unless it is {recv} fewer than {Wt} after {trig}.", True, True)]
    t, dneg, clar = pick(rng, opts)
    return t.format(**fm), dneg, clar


def gen_deadline(rng, size, F):
    D = pick(rng, DL)
    org = pick(rng, D["orgs"])
    name = pick(rng, PEOPLE)
    cid = "%s-%d" % (D["idp"], rng.randint(10000, 99999))
    pv, pe, px, pg, pr = {"short": (.08, .35, .35, .4, .25), "medium": (.35, .55, .5, .5, .35),
                          "long": (.5, .65, .6, .55, .45)}[size]
    ver = rng.random() < pv
    ext = rng.random() < pe
    excl = ext and rng.random() < px
    grace = rng.random() < pg
    roll = rng.random() < pr
    W = pick(rng, D["W"])
    conv = pick(rng, ["incl", "excl"])
    T = rand_date(rng)
    e, x = D["ext"], D["excl"]
    p = dict(T=T, S=T, W=W, conv=conv, ver=False, ext=ext, grace=grace, roll=roll, hols=[], holset=frozenset(),
             ext_kind=e["kind"], ext_cond=False, excl_kind="none", excl_flag=False, E=0, T2=None, R=None,
             G=pick(rng, D["G"]) if grace else 0)
    if ext:
        p["ext_cond"] = rng.random() < 0.75
        if e["kind"] == "add":
            p["E"] = pick(rng, e["E"])
        if excl:
            p["excl_kind"] = x["kind"]
            if x["kind"] == "flag":
                p["excl_flag"] = rng.random() < 0.5
        if e["kind"] == "switch" and p["ext_cond"]:
            if e.get("req"):
                p["R"] = T + ONE * rng.randint(2, W + 5)
                p["T2"] = p["R"] + ONE * rng.randint(1, 8)
            else:
                p["T2"] = T + ONE * rng.randint(5, W + 20)
    if ver:
        p["ver"] = True
        p["ver_mode"] = pick(rng, ["trigger", "receipt"])
        p["Wold"] = pick(rng, [w for w in D["Wold"] if w != W])
        p["conv_old"] = pick(rng, ["incl", "excl"])
        if p["ver_mode"] == "trigger":
            p["EFF"] = T + ONE * pick(rng, [-40, -12, -3, -1, 0, 1, 2, 6, 20, 45])
        else:
            p["EFF"] = T - ONE * 900
    if roll:
        Lraw, _ = dl_compute(p, ("ignored_rollover",))
        must = [Lraw] if (Lraw.weekday() < 5 and rng.random() < 0.6) else []
        p["hols"] = make_holidays(rng, must, T - ONE * 20, T + ONE * (W + 70), n_extra=rng.randint(1, 3))
        p["holset"] = frozenset(p["hols"])
    L0, _ = dl_compute(p)
    bnd = L0 + ONE * p["G"] if (grace and rng.random() < 0.45) else L0
    S = bnd + ONE * pick(rng, [-2, -1, 0, 0, 1, 1, 2, 3])
    if S <= T:
        S = T + ONE * rng.randint(1, 3)
    if p["T2"] and S < p["T2"]:
        raise Retry()
    p["S"] = S
    if ver and p["ver_mode"] == "receipt":
        p["EFF"] = S + ONE * pick(rng, [-25, -6, -1, 0, 1, 4, 15])
    L, st = dl_compute(p)
    assert (L, st) == dl_indep(p), "deadline independent check failed"
    if roll and ext and p["ext_kind"] == "add" and L != dl_compute(p, ("forgot_extension",))[0]:
        # reject if "roll first, then extend" would read differently from "extend, then roll"
        use_old = p["ver"] and ((p["T"] if p["ver_mode"] == "trigger" else p["S"]) < p["EFF"])
        span = (p["Wold"] if use_old else W) - (1 if (p["conv_old"] if use_old else conv) == "excl" else 0)
        if roll_fwd(roll_fwd(T + ONE * span, p["holset"]) + ONE * p["E"], p["holset"]) != L:
            raise Retry()
    flags = ["off_by_one"]
    if ver:
        flags.append("wrong_version")
    if roll:
        flags.append("ignored_rollover")
    if ext and p["ext_cond"]:
        flags += ["forgot_extension", "misapplied_extension"]
    if grace:
        flags.append("ignored_grace")
    res = [(f, dl_compute(p, (f,))) for f in flags]
    if not any(r[1] != st for _, r in res):
        raise Retry()
    lab = D["labels"]
    labels = [lab[0], lab[1], lab[2]] if grace else [lab[0], lab[2]]
    idx = (lambda s: s) if grace else (lambda s: 0 if s == 0 else 1)
    # ---------------- text
    ws, dneg, clar = dl_window_sentence(rng, D, W, conv)
    rules = [ws]
    if clar:
        rules.append(pick(rng, ["In computing any period under this section, the day of %s is not counted and the period ends at the end of its last day." % D["trig_s"],
                                "Day 1 of any period is the day after %s; the last day of the period is included." % D["trig_s"]]))
    if ext:
        rules.append(e["text"].format(E=p["E"]))
    if excl:
        rules.append(x["text"])
    if roll:
        rules.append(pick(rng, ["If the last day of a period falls on a Saturday, a Sunday or a listed holiday, the period ends instead on the next day that is none of these.",
                                "Where a period would end on a weekend day or a listed holiday, it is extended to the next business day."]))
        rules.append("Listed holidays: %s." % hol_text(rng, F, p["hols"]))
    if grace:
        rules.append(D["grace"].format(G=p["G"]) + (" The grace period is counted from the deadline as determined under the preceding provisions." if (ext or roll) else ""))
    old = None
    title = "%s - %s" % (org, D["doc"])
    traps = []
    if ver:
        v = rng.randint(2, 6)
        EFF = p["EFF"]
        if p["ver_mode"] == "trigger":
            tr = "Version %d applies where the %s is on or after %s; where the %s is earlier, Version %d continues to apply." % (v, D["trig_dn"], F.d(EFF), D["trig_dn"], v - 1)
        else:
            tr = "Version %d applies to every %s %s on or after %s, whatever the %s." % (v, D["sub"], D["recv"], F.d(EFF), D["trig_dn"])
        rules.insert(0 if rng.random() < 0.5 else len(rules), tr)
        ows, _, _ = dl_window_sentence(rng, D, p["Wold"], p["conv_old"])
        old = ("Superseded text - Version %d (in force %s to %s)" % (v - 1, F.d(EFF - ONE * rng.randint(400, 1200)), F.d(EFF - ONE)),
               [ows, "All other provisions were the same as in the current version."])
        title += " (Version %d)" % v
        traps.append("superseded_rule")
    if size != "short" and rng.random() < 0.5:
        rules.insert(rng.randint(0, len(rules)), pick(rng, DOMAIN_FILLER.get(D["key"], DOMAIN_FILLER["compliance"])))
    chan = pick(rng, D["chan"])
    facts = [("Reference", cid), (cap(D["actor"]), name), (D["T_key"], F.d(T)), (D["S_key"], F.d(S))]
    extra = []
    if ext or rng.random() < 0.2:
        k_, yes, no = e["fact"]
        cond = p["ext_cond"] if ext else (rng.random() < 0.5 and e["kind"] == "add")
        extra.append((k_, (yes if cond else no).format(R=F.d(p["R"]) if p["R"] else "")))
        if ext and e["kind"] == "switch" and p["ext_cond"]:
            extra.append((e["T2_key"], F.d(p["T2"])))
    if excl and x["kind"] == "flag":
        k_, yes, no = x["fact"]
        extra.append((k_, yes if p["excl_flag"] else no))
    fillv = dict(n=rng.randint(100000, 999999), n3=rng.randint(100, 999), n4="%04d" % rng.randint(0, 9999),
                 amt="{:,}".format(rng.randint(150, 24000)))
    for k_, v_ in D["misc"]:
        extra.append((k_, v_.format(**fillv)))
    extra.append(("Channel", chan))
    facts += extra
    prose = D["story"].format(name=name, T=F.d(T), S=F.d(S), chan=chan, **fillv) + " Reference %s. " % cid + \
        " ".join("%s: %s." % (k_, v_) for k_, v_ in extra if k_ != "Channel")
    # ---------------- questions
    rv = D["recv"]
    q1 = pick(rng, ["Under the text above, what is the correct determination for %s %s?" % (D["sub"], cid),
                    "How should %s %s be handled?" % (D["sub"], cid),
                    "Which outcome should be recorded for %s?" % cid])
    k1 = label_kind(q1, "Is \"{opt}\" the correct determination for %s %s?" % (D["sub"], cid), labels, idx(st),
                    [(f, idx(r[1])) for f, r in res])
    gq = " (disregarding any grace provision)" if grace else ""
    q2 = "What was the last day on which %s %s could be %s and still count as on time%s?" % (D["sub"], cid, rv, gq)
    fillers = [("off_by_one", L - ONE), ("off_by_one", L + ONE), ("off_by_two", L + 2 * ONE)]
    k2 = value_kind("date", q2, "Was {opt} the last day on which %s %s could be %s and still count as on time%s?" % (D["sub"], cid, rv, gq),
                    L, [(f, r[0]) for f, r in res], F.od, fillers)
    kinds = [k1, k1, k2]
    yn = [("Was %s %s %s within the applicable deadline%s?" % (D["sub"], cid, rv, gq), int(st == 0))]
    if grace:
        yn.append(("Is %s %s barred outright (neither on time nor saved by the grace provision)?" % (D["sub"], cid), int(st == 2)))
    if ext and p["ext_cond"]:
        on = dl_compute(p, ())[0] != dl_compute(p, ("forgot_extension",))[0]
        yn.append(("Does the extension/exception provision change the deadline that applies to %s?" % cid, int(on)))
    notes = []
    for f, (Lf, sf) in res:
        if sf == st:
            continue
        if f == "off_by_one":
            reason = "counting %d days from the %s I get %s as the last day" % (W, D["trig_dn"], F.d(Lf))
        elif f == "wrong_version":
            gold_old = p["ver"] and ((p["T"] if p["ver_mode"] == "trigger" else p["S"]) < p["EFF"])
            reason = "the %d-day limit is the one that applies, giving %s as the last day" % (W if gold_old else p["Wold"], F.d(Lf))
        elif f == "ignored_rollover":
            reason = "the period simply expired on %s" % F.d(Lf)
        elif f == "forgot_extension":
            reason = "the standard period expired on %s" % F.d(Lf)
        elif f == "misapplied_extension":
            reason = "the extension/exception clause applies here, so the deadline moves to %s" % F.d(Lf)
        else:
            reason = "it came in after the deadline and late items are simply refused"
        notes.append((f, note_text(rng, reason, labels[idx(sf)])))
    if abs((S - L).days) <= 1 or (grace and abs((S - L - ONE * p["G"]).days) <= 1):
        traps.append("boundary")
    if dneg:
        traps.append("double_negation")
    if excl and p["ext_cond"]:
        traps.append("exception_to_exception")
    if roll:
        traps.append("holiday_rollover")
    return mk_scn(tpl="deadline." + D["key"], domain=D["key"], org=org, F=F, title=title, head=D["head"], rules=rules,
                  old=old, facts=facts, prose=prose, kinds=kinds, yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="%s %s - timeliness" % (cap(D["sub"]), cid), sender=pick(rng, PEOPLE), checked=True)


# ============================================================ S2  business-day clocks
BD = [
    dict(key="logistics", orgs=["Northgate Logistics", "Parcelwise", "Bluefin Freight"], doc="Express Delivery Promise",
         head="Delivery commitment", idp="ORD", who="Customer", subj="order", X_key="Order confirmed", A_key="Delivered on",
         std="Express orders are delivered no later than the {Nord} business day after the dispatch day.",
         cnt="Express orders are delivered within {N} business days, counting the dispatch day as business day 1.",
         cut="Orders confirmed {cp} {c} on a business day are dispatched the same day; any other order is dispatched on the next business day.",
         mode="simple", cutp=0.85, N=[2, 3, 4, 5],
         labels=["On time - no compensation", "Late - refund the shipping fee", "Late by 3+ business days - refund shipping and issue a 10% voucher"],
         band="A delivery late by one or two business days earns a refund of the shipping fee; a delivery late by three or more business days earns the shipping refund plus a 10% voucher.",
         dq="By what date did order {cid} have to be delivered to count as on time?", ynq="Was order {cid} delivered on time?"),
    dict(key="banking", orgs=["Alder Street Bank", "Northfield Credit Union", "Crescent Savings"], doc="Funds Availability Policy",
         head="When deposited funds become available", idp="DEP", who="Account holder", subj="deposit", X_key="Cheque deposited", A_key="Funds made available",
         std="Funds from a cheque deposit are made available no later than the {Nord} business day after the banking day on which the deposit is received.",
         cnt="Funds from a cheque deposit are made available within {N} business days, counting the banking day of receipt as day 1.",
         cut="Deposits received {cp} {c} on a business day are treated as received that banking day; later deposits, and deposits on non-business days, are treated as received on the next business day.",
         mode="simple", cutp=0.9, N=[2, 3, 5],
         labels=["Bank met its availability commitment", "Late availability - refund overdraft fees and pay $25 goodwill"],
         dq="What was the latest date on which the funds from deposit {cid} had to be made available?", ynq="Were the funds from deposit {cid} made available on time?"),
    dict(key="compliance", orgs=["Veritas Energy Retail", "Clearwater Utilities", "Sterling Home Finance"], doc="Complaint Handling Standard",
         head="Acknowledgement of complaints", idp="CMP", who="Complainant", subj="complaint", X_key="Complaint received", A_key="Acknowledgement sent",
         std="Written complaints must be acknowledged no later than the {Nord} business day after the day of receipt.",
         cnt="Written complaints must be acknowledged within {N} business days, counting the day of receipt as day 1.",
         cut="A complaint received {cp} {c} on a business day counts as received that day; otherwise it counts as received on the next business day.",
         mode="simple", cutp=0.6, N=[2, 3, 5],
         labels=["Acknowledged on time", "Late acknowledgement - record a service standard breach"],
         dq="What was the last day on which complaint {cid} could be acknowledged on time?", ynq="Was complaint {cid} acknowledged on time?"),
    dict(key="healthcare", orgs=["Meridian Health Plan", "Crestview Health Partners", "Bayside Care Network"], doc="Utilization Management Standards",
         head="Decision time frames - standard prior authorization", idp="PA", who="Member", subj="prior-authorization request", X_key="Request received", A_key="Decision issued",
         std="Standard prior-authorization requests are decided no later than the {Nord} business day after the day a complete request is received.",
         cnt="Standard prior-authorization requests are decided within {N} business days, counting the day a complete request is received as day 1.",
         mode="switch", cutp=0.0, N=[3, 5, 7],
         sw_text="A request missing required clinical information is not complete; for such a request the period starts on the day the missing information is received, not the day of the original request.",
         X2_key="Missing clinical notes received", inc_fact=("Complete on arrival", "No - clinical notes missing", "Yes"),
         labels=["Decision issued on time", "Decision late - the request is deemed approved"],
         dq="What was the decision deadline for request {cid}?", ynq="Was the decision on request {cid} issued on time?"),
    dict(key="benefits", orgs=["Summit County Benefits Office", "Riverside Department of Social Services", "Harlow District Council"], doc="Service Standards for Applications",
         head="Processing time", idp="APP", who="Applicant", subj="application", X_key="Application form received", A_key="Decision issued",
         std="A decision is issued no later than the {Nord} business day after the day the application becomes complete.",
         cnt="A decision is issued within {N} business days, counting the day the application becomes complete as day 1.",
         mode="max", cutp=0.0, N=[5, 8, 10],
         sw_text="An application becomes complete on the day the last required document is received (or on the day the form is received, if that is later).",
         X2_key="Last required document received",
         labels=["Decision issued on time", "Late - an interim payment must be issued"],
         dq="What was the decision deadline for application {cid}?", ynq="Was the decision on application {cid} issued on time?"),
    dict(key="telecom", orgs=["Brightline Telecom", "Skyreach Mobile", "Corvid Networks"], doc="Number Porting Code of Practice",
         head="Porting time frame", idp="PRT", who="Subscriber", subj="port request", X_key="Port request validated", A_key="Port completed",
         std="A number port is completed no later than the {Nord} business day after the day the port request is validated.",
         cnt="A number port is completed within {N} business days, counting the day of validation as day 1.",
         cut="Requests validated {cp} {c} on a business day count from that day; all others count from the next business day.",
         mode="simple", cutp=0.8, N=[1, 2, 3],
         labels=["Port completed on time", "Late port - credit one month's line rental"],
         dq="By what date did port request {cid} have to be completed?", ynq="Was port request {cid} completed on time?"),
    dict(key="education", orgs=["Westbrook University", "Carroway College", "Lakeshore Institute of Technology"], doc="Registry Service Standards",
         head="Official transcripts", idp="TR", who="Student", subj="transcript request", X_key="Transcript request received", A_key="Transcript issued",
         std="Official transcripts are issued no later than the {Nord} business day after the day on which both the request and the fee have been received.",
         cnt="Official transcripts are issued within {N} business days, counting the day on which both the request and the fee have been received as day 1.",
         mode="max", cutp=0.0, N=[3, 5, 7], X2_key="Fee payment received", sw_text=None,
         labels=["Issued on time", "Late - refund the transcript fee"],
         dq="What was the latest date for issuing transcript request {cid} on time?", ynq="Was transcript request {cid} issued on time?"),
    dict(key="manufacturing", orgs=["Kestrel Components", "Gulfstar Plastics", "Delta Precision Castings"], doc="Nonconformance Procedure QP-13",
         head="Reporting to suppliers", idp="NCR", who="Inspector", subj="nonconformance report", X_key="Defect detected", A_key="NCR issued to supplier",
         std="A nonconformance report must be issued to the supplier no later than the {Nord} business day after the day of detection.",
         cnt="A nonconformance report must be issued to the supplier within {N} business days, counting the day of detection as day 1.",
         mode="simple", cutp=0.0, N=[2, 3, 4, 5],
         labels=["NCR issued on time", "NCR late - log a procedural nonconformity"],
         dq="What was the deadline for issuing NCR {cid}?", ynq="Was NCR {cid} issued on time?"),
]


def bd_trigger(p, fl):
    X = p["X"]
    if p["mode"] == "switch" and p["incomplete"] and "used_wrong_trigger" not in fl:
        X = p["X2"]
    if p["mode"] == "max" and "used_wrong_trigger" not in fl:
        X = max(p["X"], p["X2"])
    return X


def bd_compute(p, fl=()):
    wk = (5, 6) if "wrong_weekend" in fl else p["wk"]
    if "ignored_holidays" in fl:
        hol = []
    elif "ignored_observed" in fl:
        hol = p["hol_listed"]
    else:
        hol = p["hol_eff"]
    hs = frozenset(hol)
    X = bd_trigger(p, fl)
    if p["cut"] and "ignored_cutoff" not in fl:
        late = p["tmin"] > p["cmin"] if p["cincl"] else p["tmin"] >= p["cmin"]
        if "cutoff_boundary" in fl and p["tmin"] == p["cmin"]:
            late = not late
        E = next_bday_after(X, hs, wk) if (late or not is_bday(X, hs, wk)) else X
    else:
        E = X
    n = p["N"] - (1 if p["cnt"] else 0)
    if "off_by_one" in fl:
        n = n + 1 if p["cnt"] else n - 1
    due = E + ONE * n if "calendar_days" in fl else add_bdays(E, n, hs, wk)
    A = p["A"]
    if A <= due:
        st = 0
    else:
        lb = (A - due).days if "calendar_days" in fl else bdays_between(due, A, hs, wk)
        st = 1 if (not p["three"] or lb <= 2) else 2
    return due, st


def bd_indep(p):
    wk = p["wk"]
    hj = sorted(set(jdn_date(h) for h in p["hol_eff"]))
    jX = jdn_date(bd_trigger(p, ()))
    if p["cut"]:
        late = p["tmin"] > p["cmin"] if p["cincl"] else p["tmin"] >= p["cmin"]
        jE = j_next_b(jX, hj, wk) if (late or not j_isb(jX, hj, wk)) else jX
    else:
        jE = jX
    n = p["N"] - (1 if p["cnt"] else 0)
    jd = j_add_b(jE, n, hj, wk)
    jA = jdn_date(p["A"])
    if jA <= jd:
        st = 0
    else:
        st = 1 if (not p["three"] or j_count(jd, jA, hj, wk) <= 2) else 2
    return jdn_to_date(jd), st


def gen_bdays(rng, size, F):
    D = pick(rng, BD)
    org = pick(rng, D["orgs"])
    name = pick(rng, PEOPLE)
    cid = "%s-%d" % (D["idp"], rng.randint(10000, 99999))
    wk = (4, 5) if (rng.random() < (0.3 if D["key"] == "manufacturing" else 0.12)) else (5, 6)
    N = pick(rng, D["N"])
    cut = rng.random() < D["cutp"]
    cnt = rng.random() < 0.3 and N >= 2
    X = rand_date(rng)
    p = dict(wk=wk, N=N, cut=cut, cnt=cnt, mode=D["mode"], X=X, X2=None, incomplete=False, three=len(D["labels"]) == 3,
             hol_listed=[], hol_eff=[], tmin=0, cmin=0, cincl=True, A=X)
    if not cut and cnt and not is_bday(X, frozenset(), wk):
        X = next_bday_after(X, frozenset(), wk)
        p["X"] = X
    if D["mode"] == "switch":
        p["incomplete"] = rng.random() < 0.6
        if p["incomplete"]:
            p["X2"] = X + ONE * rng.randint(1, 9)
    elif D["mode"] == "max":
        p["X2"] = X + ONE * rng.randint(-6, 9)
    ch, cm = pick(rng, [(12, 0), (14, 0), (15, 0), (16, 0), (17, 0), (14, 30), (16, 30)])
    p["cmin"] = ch * 60 + cm
    if cut:
        p["cincl"] = rng.random() < 0.6
        if rng.random() < 0.35:
            p["tmin"] = p["cmin"]
        else:
            p["tmin"] = max(7 * 60, min(22 * 60, p["cmin"] + 5 * rng.randint(-40, 40)))
    else:
        p["tmin"] = 5 * rng.randint(96, 216)
    # holidays (chosen around a provisional deadline)
    due0, _ = bd_compute(p, ())
    Xs = bd_trigger(p, ())
    inr = [Xs + ONE * i for i in range(1, (due0 - Xs).days + 1) if (Xs + ONE * i).weekday() not in wk]
    must = rng.sample(inr, min(len(inr), pick(rng, [0, 1, 1, 2]))) if inr else []
    listed = make_holidays(rng, must, Xs - ONE * 40, Xs + ONE * 60, n_extra=rng.randint(1, 2), wk=wk)
    observed = []
    obs_rule = False
    if wk == (5, 6) and size != "short" and rng.random() < 0.35:
        cands = [d for d in inr if d.weekday() in (0, 4) and d not in listed]
        if cands:
            o = pick(rng, cands)
            wkd = o + ONE if o.weekday() == 4 else o - ONE
            listed.append(wkd)
            listed.sort()
            obs_rule = True
    for h in listed:
        if h.weekday() == 5 and obs_rule:
            observed.append(h - ONE)
        elif h.weekday() == 6 and obs_rule:
            observed.append(h + ONE)
        elif h.weekday() not in wk:
            observed.append(h)
    p["hol_listed"] = listed
    p["hol_eff"] = sorted(set(observed))
    due, _ = bd_compute(p, ())
    hs = frozenset(p["hol_eff"])
    k = pick(rng, [-1, 0, 0, 1, 1, 2, 3] if p["three"] else [-1, 0, 0, 1, 1, 2])
    A = add_bdays(due, k, hs, wk) if k >= 0 else sub_bdays(due, -k, hs, wk)
    p["A"] = A
    due, st = bd_compute(p, ())
    assert (due, st) == bd_indep(p), "business-day independent check failed"
    flags = ["off_by_one", "calendar_days"]
    if p["hol_eff"]:
        flags.append("ignored_holidays")
    if obs_rule:
        flags.append("ignored_observed")
    if cut:
        flags += ["ignored_cutoff", "cutoff_boundary"]
    if wk != (5, 6):
        flags.append("wrong_weekend")
    if D["mode"] != "simple":
        flags.append("used_wrong_trigger")
    res = [(f, bd_compute(p, (f,))) for f in flags]
    if not any(r[1] != st for _, r in res) or not any(r[0] != due for _, r in res):
        raise Retry()
    # ---------------- text
    fm = dict(N=N, Nord=ordinal(N))
    rules = [(D["cnt"] if cnt else D["std"]).format(**fm)]
    if wk == (5, 6) and size == "short":
        rules.append("Business days: Monday to Friday, except listed holidays.")
    elif wk == (5, 6):
        rules.append(pick(rng, ["Business days are Monday to Friday, excluding the public holidays listed below.",
                                "A business day is any day other than a Saturday, a Sunday or a listed public holiday."]))
    else:
        rules.append("Our working week runs Sunday to Thursday; Friday and Saturday are weekly rest days. Listed public holidays are also not business days.")
    if obs_rule:
        rules.append("When a listed holiday falls on a Saturday it is observed on the preceding Friday; when it falls on a Sunday it is observed on the following Monday. Observed days are not business days.")
    if cut:
        cp = "at or before" if p["cincl"] else "before"
        if p["cincl"] and rng.random() < 0.4:
            cp = "no later than"
        rules.append(D["cut"].format(cp=cp, c=F.t(ch, cm)))
    if D["mode"] != "simple" and D.get("sw_text"):
        rules.append(D["sw_text"])
    if p["three"]:
        rules.append(D["band"])
    elif size != "short":
        rules.append(pick(rng, ["Anything later than that is recorded as: %s." % D["labels"][1],
                                "If the deadline is missed, the outcome is: %s." % D["labels"][1]]))
    rules.append(("Holidays: %s." if size == "short" else "Public holidays: %s.") % hol_text(rng, F, listed) if listed else "No public holidays fall in the relevant period.")
    if size != "short" and rng.random() < 0.4:
        rules.insert(rng.randint(0, len(rules)), pick(rng, DOMAIN_FILLER.get(D["key"], DOMAIN_FILLER["logistics"])))
    F2 = Fmt(rng)
    F2.ds = pick(rng, [F.ds, 3, 5, 6])  # sometimes weekday shown, sometimes not
    facts = [("Reference", cid), (D["who"], name)]
    if cut or rng.random() < 0.5:
        th, tm = divmod(p["tmin"], 60)
        facts.append((D["X_key"], "%s at %s" % (F2.d(p["X"]), F.t(th, tm))))
    else:
        facts.append((D["X_key"], F2.d(p["X"])))
    if D["mode"] == "switch":
        facts.append((D["inc_fact"][0], D["inc_fact"][1] if p["incomplete"] else D["inc_fact"][2]))
        if p["incomplete"]:
            facts.append((D["X2_key"], F2.d(p["X2"])))
    if D["mode"] == "max":
        facts.append((D["X2_key"], F2.d(p["X2"])))
    facts.append((D["A_key"], F2.d(A)))
    prose = "%s %s (%s). " % (cap(D["subj"]), cid, name) + " ".join("%s: %s." % (k_, v_) for k_, v_ in facts[2:])
    # ---------------- questions
    labels = D["labels"]
    k1 = label_kind("What is the correct outcome for %s %s?" % (D["subj"], cid),
                    "Is \"{opt}\" the correct outcome for %s %s?" % (D["subj"], cid), labels, st,
                    [(f, r[1]) for f, r in res])
    fill = [("off_by_one", due + ONE), ("off_by_one", due - ONE)]
    k2 = value_kind("date", D["dq"].format(cid=cid), "Is {opt} the correct answer to: " + D["dq"].format(cid=cid),
                    due, [(f, r[0]) for f, r in res], F.od, fill)
    yn = [(D["ynq"].format(cid=cid), int(st == 0))]
    if p["three"]:
        yn.append(("Is a 10%% voucher due for %s %s?" % (D["subj"], cid), int(st == 2)))
    notes = []
    X0 = bd_trigger(p, ())
    th_, tm_ = divmod(p["tmin"], 60)
    BR = {"off_by_one": ("not counting the first day, the deadline was %s" if cnt else "counting the first day as day 1, the deadline was %s"),
          "calendar_days": "%d days after %s is %%s" % (N, F.d(X0)),
          "ignored_holidays": "counting every weekday, the deadline was %s",
          "ignored_observed": "the holiday fell on a weekend so it changes nothing; the deadline was %s",
          "ignored_cutoff": "the clock starts on the day it came in, which puts the deadline at %s",
          "cutoff_boundary": "%s is right on the cut-off, which puts the deadline at %%s" % F.t(th_, tm_),
          "wrong_weekend": "only Saturdays and Sundays are non-working days, so the deadline was %s",
          "used_wrong_trigger": "the clock starts on %s, so the deadline was %%s" % F.d(p["X"])}
    for f, (df, sf) in res:
        if sf != st:
            notes.append((f, note_text(rng, BR[f] % F.d(df), labels[sf])))
    traps = ["business_days"]
    if p["hol_eff"]:
        traps.append("holiday")
    if cut and p["tmin"] == p["cmin"]:
        traps.append("boundary_cutoff")
    if abs((A - due).days) <= 1:
        traps.append("boundary")
    if wk != (5, 6):
        traps.append("nonstandard_weekend")
    if D["mode"] != "simple":
        traps.append("trigger_date")
    return mk_scn(tpl="business_days." + D["key"], domain=D["key"], org=org, F=F2, title="%s - %s" % (org, D["doc"]),
                  head=D["head"], rules=rules, facts=facts, prose=prose, kinds=[k1, k2], yn=yn, notes=notes,
                  traps=traps, cid=cid, subject="%s %s" % (cap(D["subj"]), cid), sender=pick(rng, PEOPLE), checked=True)



# ============================================================ S3  calendar months vs 30-day months
MO = [
    dict(key="banking", orgs=["Alder Street Bank", "Northfield Credit Union", "Crescent Savings"], doc="Personal Loan Terms",
         head="Repayment schedule", idp="LN", who="Borrower", anchor_key="Loan disbursed", K=list(range(1, 13)),
         convs=["anniv", "d30"], dirn="le",
         rules={"anniv": "Instalment n falls due on the same day of the month as the disbursement date, n months after disbursement. If that month has no such day, the instalment falls due on the last day of that month.",
                "d30": "For scheduling purposes a month is treated as 30 days: instalment n falls due 30 x n days after the disbursement date."},
         drift_hint="Each due date is calculated from the disbursement date, not from the previous due date.",
         q="On what date is instalment {k} of loan {cid} due?",
         yn="Instalment {k} of loan {cid} was paid on {X}. Was it paid on or before its due date?"),
    dict(key="saas", orgs=["Lumen Cloud", "Stratus Workspace", "Nimbus CRM"], doc="Subscription Terms",
         head="Monthly renewals", idp="SUB", who="Customer", anchor_key="Subscription start date", K=list(range(1, 13)),
         convs=["anniv", "d30"], dirn="ge",
         rules={"anniv": "A monthly subscription renews on the same day of the month as its start date; in a month without that day it renews on the last day of that month.",
                "d30": "Billing periods are exactly 30 days long; renewal n takes place 30 x n days after the start date."},
         drift_hint="Every renewal date is counted from the original start date, never from the previous renewal.",
         q="On what date does renewal number {k} of subscription {cid} take place?",
         yn="The customer of subscription {cid} cancelled on {X}. A cancellation made before a renewal date avoids that renewal's charge; one made on or after it does not. Is the customer charged for renewal number {k}?"),
    dict(key="hr", orgs=["Castellan Foods Ltd", "Norvale Engineering", "Pinecrest Hospital Trust"], doc="Employee Handbook - Probation",
         head="Length of probation", idp="EMP", who="Employee", anchor_key="Start date", K=[3, 6, 9, 12],
         convs=["anniv_m1", "d30_m1"], dirn="le",
         rules={"anniv_m1": "Probation lasts {k} months from the start date. It ends on the day before the date {k} months later that has the same day-of-month as the start date; if that month has no such date, it ends on the last day of that month.",
                "d30_m1": "Probation lasts {k} months; for this purpose a month is 30 days, so probation ends on day {k30} counting the start date as day 1."},
         q="What is the last day of probation for employee {cid}?",
         yn="Employee {cid} was dismissed with effect from {X}. Was that within the probation period?"),
    dict(key="telecom", orgs=["Brightline Telecom", "Skyreach Mobile", "Corvid Networks"], doc="Customer Contract Terms",
         head="Minimum term", idp="CTR", who="Subscriber", anchor_key="Activation date", K=[6, 12, 18, 24],
         convs=["anniv_m1", "d30_m1"], dirn="le",
         rules={"anniv_m1": "The minimum term is {k} months. It starts on the activation date and ends on the day before the date {k} months later with the same day-of-month (or on the last day of that month if there is no such date).",
                "d30_m1": "The minimum term is {k} months of 30 days each, i.e. it ends on day {k30} counting the activation date as day 1."},
         pre="A cancellation taking effect on or before the last day of the minimum term incurs the early termination fee.",
         q="What is the last day of the minimum term for contract {cid}?",
         yn="The cancellation of contract {cid} takes effect on {X}. Does the early termination fee apply?"),
    dict(key="insurance", orgs=["Harborview Mutual", "Kestrel Insurance Co.", "Bluestone Assurance"], doc="Short-Term Motor Policy Wording",
         head="Period of insurance", idp="POL", who="Policyholder", anchor_key="Cover start date", K=[1, 3, 6],
         convs=["anniv_m1", "d30_m1"], dirn="le",
         rules={"anniv_m1": "Cover runs for {k} {mo}: it starts on the start date and ends at the end of the day before the date {k} {mo} later with the same day-of-month (or at the end of the last day of that month if there is no such date).",
                "d30_m1": "Cover runs for {k} {mo}, each month being 30 days, so the last day of cover is day {k30} counting the start date as day 1."},
         q="What is the last day of cover under policy {cid}?",
         yn="Policy {cid}: is a loss occurring on {X} within the period of insurance?"),
    dict(key="healthcare", orgs=["Meridian Health Plan", "Bayside Care Network", "Arbor Community Health"], doc="Care Transition Quality Standard",
         head="Post-discharge follow-up", idp="PT", who="Patient", anchor_key="Discharge date", K=[1, 2, 3],
         convs=["anniv", "d30"], dirn="le",
         rules={"anniv": "After a cardiac admission, a follow-up appointment must take place no later than {k} calendar {mo} after discharge, i.e. on or before the same day of the month {k} {mo} later (the last day of that month where there is no such day).",
                "d30": "After a cardiac admission, a follow-up appointment must take place no later than {k30} days after the discharge date."},
         q="What is the latest compliant follow-up date for patient {cid}?",
         yn="Patient {cid} had the follow-up appointment on {X}. Was it compliant with the standard?"),
    dict(key="education", orgs=["Westbrook University", "Carroway College", "Lakeshore Institute of Technology"], doc="Admissions Policy - Deferral",
         head="Deferred offers", idp="APP", who="Applicant", anchor_key="Original programme start date", K=[6, 9, 12],
         convs=["anniv", "d30"], dirn="le",
         rules={"anniv": "A deferred place may be taken up on any date up to and including the same calendar day {k} months after the original programme start date (the last day of the month where that day does not exist).",
                "d30": "A deferred place may be taken up until {k30} days after the original programme start date; enrolment on that day is still allowed."},
         q="What is the last day on which applicant {cid} can take up the deferred place?",
         yn="Applicant {cid} asked to enrol on {X}. Is the deferred place still available on that date?"),
]
MO_PARTNER = {"anniv": "d30", "d30": "anniv", "anniv_m1": "d30_m1", "d30_m1": "anniv_m1"}


def mo_value(conv, D0, k):
    if conv == "anniv":
        return add_months(D0, k)
    if conv == "anniv_m1":
        return add_months(D0, k) - ONE if month_exists(D0, k) else add_months(D0, k)
    if conv == "d30":
        return D0 + ONE * (30 * k)
    if conv == "d30_m1":
        return D0 + ONE * (30 * k - 1)
    if conv == "overflow":
        return add_months_overflow(D0, k)
    if conv == "overflow_m1":
        return add_months_overflow(D0, k) - ONE
    if conv == "drift":
        return add_months_drift(D0, k)
    if conv == "drift_m1":
        return add_months_drift(D0, k) - ONE
    raise ValueError(conv)


def mo_value_indep(conv, D0, k):
    idx = D0.year * 12 + D0.month - 1 + k
    y, m = idx // 12, idx % 12 + 1
    exists = D0.day <= dim(y, m)
    if conv == "anniv":
        return add_months_indep(D0, k)
    if conv == "anniv_m1":
        a = add_months_indep(D0, k)
        return jdn_to_date(jdn_date(a) - 1) if exists else a
    if conv == "d30":
        return jdn_to_date(jdn_date(D0) + 30 * k)
    return jdn_to_date(jdn_date(D0) + 30 * k - 1)


def gen_months(rng, size, F):
    D = pick(rng, MO)
    org = pick(rng, D["orgs"])
    name = pick(rng, PEOPLE)
    cid = "%s-%d" % (D["idp"], rng.randint(10000, 99999))
    conv = pick(rng, D["convs"])
    y, m = rng.randint(2025, 2028), rng.randint(1, 12)
    if rng.random() < 0.65:
        day = pick(rng, [d for d in (29, 30, 31) if d <= dim(y, m)] or [28])
    else:
        day = rng.randint(1, 28)
    D0 = dt.date(y, m, day)
    Ks = list(D["K"])
    short_k = [k for k in Ks if not month_exists(D0, k)]
    k = pick(rng, short_k) if (short_k and rng.random() < 0.75) else pick(rng, Ks)
    ver = size != "short" and rng.random() < 0.3
    gconv = conv
    EFF = None
    if ver:
        EFF = D0 + ONE * pick(rng, [-200, -30, -1, 0, 1, 20, 150])
        oconv = MO_PARTNER[conv]
        if D0 < EFF:
            gconv = oconv
    gold = mo_value(gconv, D0, k)
    assert gold == mo_value_indep(gconv, D0, k), "month independent check failed"
    var = []
    if ver:
        var.append(("wrong_version", mo_value(MO_PARTNER[gconv], D0, k)))
    part = MO_PARTNER[gconv]
    var.append(("used_30_day_months" if gconv.startswith("anniv") else "used_calendar_months", mo_value(part, D0, k)))
    m1 = gconv.endswith("_m1")
    var.append(("off_by_one", mo_value(gconv[:-3] if m1 else gconv + "_m1", D0, k)))
    if gconv.startswith("anniv"):
        var.append(("month_overflow", mo_value("overflow_m1" if m1 else "overflow", D0, k)))
        if k >= 2:
            var.append(("anchor_drift", mo_value("drift_m1" if m1 else "drift", D0, k)))
    if all(v == gold for _, v in var):
        raise Retry()
    rules = []
    if D.get("pre"):
        rules.append(D["pre"])
    mo = "month" if k == 1 else "months"
    rules.append(D["rules"][conv].format(k=k, k30=30 * k, mo=mo))
    if conv == "anniv" and D.get("drift_hint") and rng.random() < 0.4:
        rules.append(D["drift_hint"])
    old = None
    traps = ["month_length"]
    if ver:
        v = rng.randint(2, 5)
        rules.append("Version %d of these terms applies where the %s is on or after %s; earlier ones remain under Version %d." % (
            v, D["anchor_key"].lower(), F.d(EFF), v - 1))
        old = ("Version %d (superseded)" % (v - 1), [D["rules"][MO_PARTNER[conv]].format(k=k, k30=30 * k, mo=mo)])
        traps.append("superseded_rule")
    if size != "short" and rng.random() < 0.4:
        rules.insert(rng.randint(0, len(rules)), pick(rng, DOMAIN_FILLER.get(D["key"], DOMAIN_FILLER["banking"])))
    facts = [("Reference", cid), (D["who"], name), (D["anchor_key"], F.d(D0))]
    if D["key"] == "banking":
        facts.append(("Principal", money(rng.randint(20, 400) * 100)))
        facts.append(("Term", "%d monthly instalments" % max(k, rng.randint(12, 36))))
    elif D["key"] == "saas":
        facts.append(("Plan", pick(rng, ["Team (monthly)", "Pro (monthly)", "Starter (monthly)"])))
    elif D["key"] == "telecom":
        facts.append(("Monthly charge", money(rng.randint(20, 90))))
    delta = pick(rng, [-2, -1, 0, 0, 1, 1, 2])
    X = gold + ONE * delta
    if D["dirn"] == "le":
        ans = int(X <= gold)
    else:
        ans = int(X >= gold)
    q = D["q"].format(k=k, cid=cid)
    fill = [("off_by_one", gold + ONE), ("off_by_one", gold - ONE)]
    k1 = value_kind("date", q, "Is {opt} the correct answer to the question: " + q, gold, var, F.od, fill)
    yn = [(D["yn"].format(k=k, cid=cid, X=F.d(X)), ans)]
    MR = {"used_30_day_months": "a month is just 30 days, so I added %d days to %s" % (30 * k, F.d(D0)),
          "used_calendar_months": "%d %s on from %s is the same day of the month" % (k, mo, F.d(D0)),
          "off_by_one": {"anniv": "it ends the day before the same date %d %s later" % (k, mo),
                         "anniv_m1": "it runs to the same date %d %s later" % (k, mo),
                         "d30": "counting the start date as day 1, it is day %d" % (30 * k),
                         "d30_m1": "the start date itself is not counted, so I added %d days" % (30 * k)}[gconv],
          "month_overflow": "the missing days just roll over into the next month",
          "anchor_drift": "I stepped forward one month at a time from %s" % F.d(D0),
          "wrong_version": "the other version of the terms is the one to use"}
    notes = []
    for mname, v in var:
        if v != gold:
            notes.append((mname, note_value(rng, MR[mname], F.d(v))))
    if abs(delta) <= 1:
        traps.append("boundary")
    prose = "%s %s: %s. %s" % (D["who"], name, cid, " ".join("%s: %s." % (a, b) for a, b in facts[2:]))
    return mk_scn(tpl="months." + D["key"], domain=D["key"], org=org, F=F, title="%s - %s" % (org, D["doc"]), head=D["head"],
                  rules=rules, old=old, facts=facts, prose=prose, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="%s %s - date check" % (D["who"], cid), sender=pick(rng, PEOPLE), checked=True)


# ============================================================ S4  time zones
def two_offsets(rng, mindiff=180):
    while True:
        a, b = pick(rng, OFFSETS), pick(rng, OFFSETS)
        if abs(a - b) >= mindiff:
            return a, b


def zlabel(rng, place, o):
    return pick(rng, ["%s (%s)" % (place, fofs(o)), "%s, %s" % (place, fofs(o))])


def gen_tz_dose(rng, size, F):
    org = pick(rng, ["Arbor Community Health", "Meridian Travel Clinic", "Crestview Pharmacy Services"])
    name = pick(rng, PEOPLE)
    cid = "RX-%d" % rng.randint(10000, 99999)
    H = pick(rng, [8, 12, 24])
    w = pick(rng, [1, 2]) if H == 24 else 1
    miss = {8: 4, 12: 6, 24: 12}[H]
    o1, o2 = two_offsets(rng, 240)
    p1, p2 = rng.sample(PLACES, 2)
    d1 = rand_date(rng)
    h1, m1 = rng.randint(6, 22), 5 * rng.randint(0, 11)
    u1 = utc_of(d1, h1, m1, o1)
    if rng.random() < 0.75:
        diff = pick(rng, [-w * 60, w * 60, miss * 60]) + pick(rng, [-30, -10, -5, 0, 0, 5, 10, 30])
    else:
        diff = 5 * rng.randint(-40, 200)
    u2 = u1 + dt.timedelta(minutes=H * 60 + diff)
    d2, h2, m2 = local_of(u2, o2)

    def band(x, strict=False):
        if (x <= -w * 60) if strict else (x < -w * 60):
            return 0
        if (x < w * 60) if strict else (x <= w * 60):
            return 1
        if (x < miss * 60) if strict else (x <= miss * 60):
            return 2
        return 3
    gd = int((u2 - u1).total_seconds() // 60) - H * 60
    assert gd == j_umin(d2, h2, m2, o2) - j_umin(d1, h1, m1, o1) - H * 60 == diff, "dose tz check failed"
    g = band(diff)
    dn = naive_min(d2, h2, m2) - naive_min(d1, h1, m1) - H * 60
    ds = (naive_min(d2, h2, m2) + o2) - (naive_min(d1, h1, m1) + o1) - H * 60
    var = [("tz_ignored", band(dn)), ("tz_sign_flip", band(ds)), ("boundary_exclusive", band(diff, True))]
    if band(dn) == g:
        raise Retry()
    labels = ordinal_labels(["Early dose (taken more than %d h before it was due)" % w, "On-schedule dose",
                             "Late dose (take it and continue)", "Missed dose (should have been skipped)"])
    rules = ["Take one dose every %d hours. Each dose is due exactly %d hours after the previous dose was actually taken." % (H, H),
             "A dose taken no more than %d hour%s before or after its due time counts as on schedule." % (w, "" if w == 1 else "s"),
             "A dose taken more than %d hour%s before its due time is an early dose." % (w, "" if w == 1 else "s"),
             "A dose taken more than %d hour%s but no more than %d hours after its due time is a late dose: take it and carry on." % (w, "" if w == 1 else "s", miss),
             "If more than %d hours have passed since the due time, the dose is missed: skip it and take the next dose at the usual time." % miss]
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, ["Store below 25 C.", "Swallow whole with water.", "Do not take with grapefruit juice.",
                                "Keep out of the reach of children."]))
    dep = u1 + dt.timedelta(minutes=max(30, min(150, int((u2 - u1).total_seconds() // 180))))
    onboard = rng.random() < 0.5
    arr = u2 + dt.timedelta(minutes=5 * rng.randint(6, 60)) if onboard else u2 - dt.timedelta(minutes=5 * rng.randint(6, 36))
    if arr <= dep:
        raise Retry()
    dd, dh, dm = local_of(dep, o1)
    ad, ah, am = local_of(arr, o2)
    facts = [("Patient", name), ("Prescription", cid),
             ("Previous dose", "%s at %s, local time in %s" % (F.d(d1), F.t(h1, m1), zlabel(rng, p1, o1))),
             ("Flight", "departed %s %s local (%s); landed %s %s local (%s)" % (F.d(dd), F.t(dh, dm), p1, F.d(ad), F.t(ah, am), p2))]
    if onboard:
        facts.append(("Next dose", "taken on board on %s at %s by the cabin clock, which was already set to destination time (%s)" % (F.d(d2), F.t(h2, m2), fofs(o2))))
    else:
        facts.append(("Next dose", "taken on %s at %s, local time in %s" % (F.d(d2), F.t(h2, m2), zlabel(rng, p2, o2))))
    q = "How should the dose recorded as \"Next dose\" for %s be classified?" % name
    k1 = label_kind(q, "Should the next dose taken by %s be classified as \"{opt}\"?" % name, labels, g, var)
    yn = [("Was the next dose taken by %s on schedule?" % name, int(g == 1)),
          ("Should the next dose taken by %s have been skipped as a missed dose?" % name, int(g == 3))]
    notes = [("tz_ignored", note_text(rng, "the clock said %s last time and %s this time, so that is the gap" % (F.t(h1, m1), F.t(h2, m2)), labels[band(dn)]))]
    traps = ["timezone"]
    if min(abs(diff + w * 60), abs(diff - w * 60), abs(diff - miss * 60)) <= 10:
        traps.append("boundary")
    return mk_scn(tpl="timezone.dose", domain="healthcare", org=org, F=F, title="%s - Medication instructions" % org,
                  head="Dosing schedule", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="Dose timing query - %s" % name, sender=pick(rng, PEOPLE), checked=True)


def gen_tz_exam(rng, size, F):
    org = pick(rng, ["Westbrook University", "Carroway College", "Lakeshore Institute of Technology", "Open Meridian University"])
    name = pick(rng, PEOPLE)
    cid = "S%d" % rng.randint(1000000, 9999999)
    oz = pick(rng, [0, 0, 60, -300, 600])
    osz = pick(rng, [o for o in OFFSETS if abs(o - oz) >= 180])
    pz, ps = rng.sample(PLACES, 2)
    Dd = rand_date(rng)
    dh, dm = pick(rng, [(23, 59), (17, 0), (12, 0), (9, 0)])
    du = utc_of(Dd, dh, dm, oz)
    if rng.random() < 0.8:
        late = pick(rng, [0, 1440, 4320]) + pick(rng, [-45, -5, -1, 0, 0, 1, 5, 30, 120])
    else:
        late = rng.randint(-600, 5000)
    su = du + dt.timedelta(minutes=late)
    sd, sh, sm = local_of(su, osz)
    assert j_umin(sd, sh, sm, osz) - j_umin(Dd, dh, dm, oz) == late, "exam tz check failed"

    def band(x, strict=False):
        if x <= 0:
            return 0
        if (x < 1440) if strict else (x <= 1440):
            return 1
        if (x < 4320) if strict else (x <= 4320):
            return 2
        return 3
    g = band(late)
    ln = naive_min(sd, sh, sm) - naive_min(Dd, dh, dm)
    ls = (naive_min(sd, sh, sm) + osz) - (naive_min(Dd, dh, dm) + oz)
    var = [("tz_ignored", band(ln)), ("tz_sign_flip", band(ls)), ("boundary_exclusive", band(late, True))]
    if all(v == g for _, v in var):
        raise Retry()
    labels = ordinal_labels(["On time - no penalty", "Up to 24 hours late - 10% penalty",
                             "More than 24 and up to 72 hours late - 25% penalty", "More than 72 hours late - not marked"])
    zone = "UTC" if oz == 0 else fofs(oz)
    rules = ["The deadline for the final project is %s at %s %s%s." % (F.d(Dd), F.t(dh, dm), zone, "" if oz == 0 else " (%s campus time)" % pz),
             "Lateness is measured from the deadline to the time the submission is received by the platform.",
             "Work received up to and including 24 hours late loses 10%; more than 24 and up to and including 72 hours late loses 25%; work received more than 72 hours late is not marked."]
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["education"]))
    facts = [("Student", "%s (%s)" % (name, cid)), ("Studying from", "%s, %s" % (ps, fofs(osz))),
             ("Platform receipt", "%s at %s (displayed in the student's local time, %s)" % (F.d(sd), F.t(sh, sm), fofs(osz))),
             ("File", pick(rng, ["final_project.zip", "report_v3.pdf", "submission.docx"]))]
    q = "Which lateness band applies to %s's final project submission?" % name
    k1 = label_kind(q, "Does band \"{opt}\" apply to %s's submission?" % name, labels, g, var)
    yn = [("Was %s's submission on time?" % name, int(g == 0)), ("Will %s's submission be marked at all?" % name, int(g != 3))]
    notes = [("tz_ignored", note_text(rng, "the receipt says %s %s and the deadline is %s %s" % (F.d(sd), F.t(sh, sm), F.d(Dd), F.t(dh, dm)), labels[band(ln)]))]
    traps = ["timezone"] + (["boundary"] if min(abs(late), abs(late - 1440), abs(late - 4320)) <= 5 else [])
    return mk_scn(tpl="timezone.exam", domain="education", org=org, F=F, title="%s - Module handbook" % org, head="Submission deadline",
                  rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="Late submission query - %s" % name, sender=pick(rng, PEOPLE), checked=True)


def gen_tz_wire(rng, size, F):
    org = pick(rng, ["Alder Street Bank", "Crescent Savings", "Harbourline Commercial Bank"])
    cid = "WIR-%d" % rng.randint(100000, 999999)
    name = pick(rng, PEOPLE)
    ob = pick(rng, [-300, -240, 0, 60, 480, 540])
    oc = pick(rng, [o for o in OFFSETS if abs(o - ob) >= 240])
    pb, pc = rng.sample(PLACES, 2)
    ch, cm = pick(rng, [(15, 0), (16, 0), (17, 30), (14, 0)])
    incl = rng.random() < 0.6
    db = rand_date(rng)
    tmin = ch * 60 + cm + pick(rng, [-20, -5, 0, 0, 5, 30, 90, -120])
    tmin = max(0, min(1435, tmin))
    hb, mb = divmod(tmin, 60)
    ub = utc_of(db, hb, mb, ob)
    dc, hc, mc = local_of(ub, oc)
    hols = make_holidays(rng, [d for d in [db, db + ONE] if d.weekday() < 5 and rng.random() < 0.25], db - ONE * 30, db + ONE * 30, n_extra=1)
    hs = frozenset(hols)

    def value(d, t, fl=()):
        hs_ = frozenset() if "ignored_holidays" in fl else hs
        ok_t = t <= ch * 60 + cm if incl else t < ch * 60 + cm
        if "cutoff_boundary" in fl and t == ch * 60 + cm:
            ok_t = not ok_t
        if is_bday(d, hs_) and ok_t:
            return d
        if "ignored_weekend" in fl:
            return d + ONE
        return next_bday_after(d, hs_)
    g = value(db, tmin)
    hj = [jdn_date(h) for h in hols]
    jb = (j_umin(dc, hc, mc, oc) + ob) // 1440
    tb = (j_umin(dc, hc, mc, oc) + ob) % 1440
    okt = tb <= ch * 60 + cm if incl else tb < ch * 60 + cm
    gi = jb if (j_isb(jb, hj, (5, 6)) and okt) else j_next_b(jb, hj, (5, 6))
    assert jdn_to_date(gi) == g, "wire tz check failed"
    nm = naive_min(dc, hc, mc)
    sflip = nm + oc + ob  # applying offsets with the wrong sign
    var = [("tz_ignored", value(dc, hc * 60 + mc)),
           ("tz_sign_flip", value(jdn_to_date(sflip // 1440), sflip % 1440)),
           ("ignored_holidays", value(db, tmin, ("ignored_holidays",))),
           ("cutoff_boundary", value(db, tmin, ("cutoff_boundary",))),
           ("ignored_weekend", value(db, tmin, ("ignored_weekend",)))]
    if all(v == g for _, v in var[:2]):
        raise Retry()
    rules = ["Outgoing international payments are processed in %s (%s)." % (pb, fofs(ob)),
             "Instructions received %s %s %s time on a business day are sent with that day's value date; any other instruction receives the value date of the next business day." % ("at or before" if incl else "before", F.t(ch, cm), pb),
             "Business days are Monday to Friday excluding the bank holidays listed: %s." % hol_text(rng, F, hols)]
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["banking"]))
    facts = [("Payment reference", cid), ("Customer", name), ("Customer location", "%s (%s)" % (pc, fofs(oc))),
             ("Instruction submitted", "%s at %s customer local time" % (F.d(dc), F.t(hc, mc))),
             ("Amount", money(rng.randint(500, 90000), pick(rng, ["$", "EUR ", "GBP "])))]
    q = "What value date will payment %s receive?" % cid
    k1 = value_kind("date", q, "Will payment %s receive value date {opt}?" % cid, g, var, F.od, [("off_by_one", g + ONE)])
    yn = [("Will payment %s receive a value date equal to the customer's local submission date (%s)?" % (cid, F.d(dc)), int(g == dc)),
          ("Was payment %s received within the cut-off on a business day (so it keeps the same bank-local day as value date)?" % cid, int(g == db))]
    notes = [("tz_ignored", note_value(rng, "the customer sent it at %s on %s and that is the time to test against the cut-off" % (F.t(hc, mc), F.d(dc)), F.d(var[0][1])))] if var[0][1] != g else []
    traps = ["timezone", "cutoff_time"] + (["boundary"] if abs(tmin - ch * 60 - cm) <= 5 else []) + (["holiday"] if hols else [])
    return mk_scn(tpl="timezone.wire", domain="banking", org=org, F=F, title="%s - Payment cut-off times" % org, head="Value dates",
                  rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="Value date query %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_tz_breach(rng, size, F):
    org = pick(rng, ["Sterling Home Finance", "Veritas Energy Retail", "Clearwater Utilities", "Lumen Cloud"])
    cid = "BR-%d" % rng.randint(1000, 9999)
    oa = pick(rng, OFFSETS)
    on = pick(rng, [o for o in OFFSETS if abs(o - oa) >= 180])
    pa, pn = rng.sample(PLACES, 2)
    ad = rand_date(rng)
    ah, am = rng.randint(0, 23), 5 * rng.randint(0, 11)
    au = utc_of(ad, ah, am, oa)
    det = au - dt.timedelta(minutes=5 * rng.randint(24, 400))
    if rng.random() < 0.8:
        el = 4320 + pick(rng, [-120, -30, -5, 0, 0, 5, 30, 240])
    else:
        el = 5 * rng.randint(600, 1100)
    nu = au + dt.timedelta(minutes=el)
    nd, nh, nm_ = local_of(nu, on)
    assert j_umin(nd, nh, nm_, on) - j_umin(ad, ah, am, oa) == el, "breach tz check failed"
    g = int(el <= 4320)
    dd_, dh_, dm_ = local_of(det, oa)
    naive_a = naive_min(ad, ah, am)
    naive_n = naive_min(nd, nh, nm_)
    e_ign = naive_n - naive_a
    e_flip = (naive_n + on) - (naive_a + oa)
    e_det = int((nu - det).total_seconds() // 60)
    datebased = int((nd - ad).days <= 3)
    labels = ["Notification made in time", "Late notification - reasons for the delay must be recorded and sent"]
    vi = [("tz_ignored", 0 if e_ign <= 4320 else 1), ("tz_sign_flip", 0 if e_flip <= 4320 else 1),
          ("from_detection", 0 if e_det <= 4320 else 1), ("counted_calendar_dates", 0 if datebased else 1)]
    gi = 0 if g else 1
    if all(v == gi for _, v in vi):
        raise Retry()

    def futc(x):
        return "%s %02d:%02d UTC" % (x.date().isoformat(), x.hour, x.minute)
    dl = au + dt.timedelta(hours=72)
    v_ign = dt.datetime(ad.year, ad.month, ad.day, ah, am, tzinfo=dt.timezone.utc) + dt.timedelta(hours=72)
    v_flip = v_ign + dt.timedelta(minutes=oa)
    v_det = det + dt.timedelta(hours=72)
    v_date = utc_of(ad + ONE * 3, 23, 59, oa)
    rules = ["A personal data breach must be notified to the supervisory authority without undue delay and in any event within 72 hours after the organisation becomes aware of it.",
             "The organisation becomes aware of a breach when the security lead confirms that personal data has been affected - not when suspicious activity is first logged.",
             "A notification made after 72 hours must be accompanied by the reasons for the delay."]
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["compliance"]))
    facts = [("Incident", cid), ("Suspicious activity first logged", "%s %s (%s, %s)" % (F.d(dd_), F.t(dh_, dm_), pa, fofs(oa))),
             ("Breach confirmed by security lead", "%s %s (%s, %s)" % (F.d(ad), F.t(ah, am), pa, fofs(oa))),
             ("Notification receipt from authority portal", "%s %s (%s, %s)" % (F.d(nd), F.t(nh, nm_), pn, fofs(on))),
             ("Records affected", "{:,}".format(rng.randint(40, 90000)))]
    k1 = label_kind("What is the correct classification of the notification for incident %s?" % cid,
                    "Is \"{opt}\" the correct classification for incident %s's notification?" % cid, labels, gi, vi)
    k2 = value_kind("datetime", "By what time (UTC) did the notification for incident %s have to be received?" % cid,
                    "Was {opt} the latest time the notification for incident %s could be received?" % cid, dl,
                    [("tz_ignored", v_ign), ("tz_sign_flip", v_flip), ("from_detection", v_det), ("counted_calendar_dates", v_date)], futc)
    yn = [("Was the notification for incident %s made within 72 hours?" % cid, g)]
    notes = [(m, note_text(rng, r, labels[v])) for (m, v), r in zip(vi, [
        "the confirmation was at %s on %s and the portal receipt at %s on %s, which is %.1f hours" % (F.t(ah, am), F.d(ad), F.t(nh, nm_), F.d(nd), e_ign / 60.0),
        "converting both times to UTC gives a gap of %.1f hours" % (e_flip / 60.0),
        "the clock starts when the activity was first logged on %s" % F.d(dd_),
        "it went in on %s, within three calendar days of %s" % (F.d(nd), F.d(ad))]) if v != gi]
    traps = ["timezone", "unit_hours_vs_days", "surface_cue"] + (["boundary"] if abs(el - 4320) <= 5 else [])
    return mk_scn(tpl="timezone.breach", domain="compliance", org=org, F=F, title="%s - Personal Data Breach Procedure" % org,
                  head="Notification to the authority", rules=rules, facts=facts, kinds=[k1, k2], yn=yn, notes=notes,
                  traps=traps, cid=cid, subject="Breach %s - was notification on time?" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_tz_maint(rng, size, F):
    org = pick(rng, ["Lumen Cloud", "Brightline Telecom", "Stratus Workspace", "Corvid Networks"])
    cid = "OUT-%d" % rng.randint(1000, 9999)
    op = pick(rng, [0, 0, 60, -300])
    oc = pick(rng, [o for o in OFFSETS if abs(o - op) >= 180])
    pp, pc = rng.sample(PLACES, 2)
    Dm = rand_date(rng)
    while Dm.weekday() != 6:
        Dm += ONE
    h1 = pick(rng, [0, 1, 2, 3])
    dur = pick(rng, [2, 3, 4])
    ws = utc_of(Dm, h1, 0, op)
    we = ws + dt.timedelta(hours=dur)
    target = pick(rng, [0, 0, 30, 31, 120, 121, 5 * rng.randint(1, 60)])
    if target == 0:
        a = 5 * rng.randint(0, 6)
        b = 5 * rng.randint(0, 6)
        st_, en_ = ws + dt.timedelta(minutes=a), we - dt.timedelta(minutes=b)
    else:
        pre = rng.randint(0, target)
        post = target - pre
        st_, en_ = ws - dt.timedelta(minutes=pre), we + dt.timedelta(minutes=post)
    if en_ <= st_:
        raise Retry()
    sd, sh, sm = local_of(st_, oc)
    ed, eh, em = local_of(en_, oc)

    def outside(s0, e0, w0, w1):
        tot = e0 - s0
        ov = max(0, min(e0, w1) - max(s0, w0))
        return tot - ov
    js, je = j_umin(sd, sh, sm, oc), j_umin(ed, eh, em, oc)
    jw0 = j_umin(Dm, h1, 0, op)
    out_i = outside(js, je, jw0, jw0 + dur * 60)
    out_p = int((en_ - st_).total_seconds() // 60) - max(0, int((min(en_, we) - max(st_, ws)).total_seconds() // 60))
    assert out_p == out_i == target, "maintenance tz check failed"

    def band(x):
        return 0 if x <= 0 else 1 if x <= 30 else 2 if x <= 120 else 3
    g = band(target)
    ns, ne = naive_min(sd, sh, sm), naive_min(ed, eh, em)
    nw0 = naive_min(Dm, h1, 0)
    o_ign = outside(ns, ne, nw0, nw0 + dur * 60)
    o_flip = outside(ns + oc, ne + oc, nw0 + op, nw0 + op + dur * 60)
    var = [("tz_ignored", band(o_ign)), ("tz_sign_flip", band(o_flip)), ("counted_whole_outage", band(ne - ns))]
    if all(v == g for _, v in var):
        raise Retry()
    labels = ordinal_labels(["No service credit", "5% service credit", "10% service credit", "25% service credit"])
    zone = "UTC" if op == 0 else "%s (%s)" % (pp, fofs(op))
    rules = ["Planned maintenance windows are announced at least 7 days in advance and are excluded from availability calculations.",
             "The maintenance window for this month was %s, %s to %s %s." % (F.d(Dm), F.t(h1, 0), F.t(h1 + dur, 0), zone),
             "Service credits are based on the minutes of outage falling outside any announced maintenance window: none - no credit; 1 to 30 minutes - 5%; 31 to 120 minutes - 10%; more than 120 minutes - 25%."]
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["telecom"]))
    facts = [("Outage reference", cid), ("Customer site", "%s (%s)" % (pc, fofs(oc))),
             ("Outage start (customer monitoring, local time)", "%s %s" % (F.d(sd), F.t(sh, sm))),
             ("Outage end (customer monitoring, local time)", "%s %s" % (F.d(ed), F.t(eh, em))),
             ("Services affected", pick(rng, ["VoIP trunks", "Primary API", "Mail relay", "SD-WAN edge"]))]
    q = "Which service credit is due for outage %s?" % cid
    k1 = label_kind(q, "Is \"{opt}\" the service credit due for outage %s?" % cid, labels, g, var)
    yn = [("Is any service credit due for outage %s?" % cid, int(g > 0)), ("Is a credit of 10%% or more due for outage %s?" % cid, int(g >= 2))]
    notes = [(m, note_text(rng, r, labels[v])) for (m, v), r in zip(var, [
        "comparing the monitoring times %s-%s directly with the window gives %d minutes outside it" % (F.t(sh, sm), F.t(eh, em), o_ign),
        "after converting the offsets I get %d minutes outside the window" % o_flip,
        "the whole outage lasted %d minutes" % (ne - ns)]) if v != g]
    traps = ["timezone"] + (["boundary"] if target in (0, 30, 31, 120, 121) else [])
    return mk_scn(tpl="timezone.maintenance", domain="telecom", org=org, F=F, title="%s - Service Level Agreement, Schedule 2" % org,
                  head="Maintenance and service credits", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps,
                  cid=cid, subject="Credit request for outage %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def dispatch(rng, size, F, fns):
    fn = pick(rng, fns)
    for _ in range(40):
        try:
            return fn(rng, size, F)
        except Retry:
            continue
    raise Retry()


def gen_timezone(rng, size, F):
    return dispatch(rng, size, F, [gen_tz_dose, gen_tz_exam, gen_tz_wire, gen_tz_breach, gen_tz_maint])


# ============================================================ S5  SLA clocks (business hours, pauses)
SLA_D = [
    dict(key="saas", orgs=["Lumen Cloud", "Stratus Workspace", "Nimbus CRM"], doc="Support Service Level Agreement", unit="ticket", done="resolved", idp="TKT"),
    dict(key="telecom", orgs=["Brightline Telecom", "Corvid Networks", "Skyreach Business"], doc="Business Connectivity SLA", unit="fault", done="restored", idp="FLT"),
    dict(key="it", orgs=["Castellan Foods IT", "Norvale Engineering IT Services"], doc="Internal IT Service Catalogue", unit="incident", done="resolved", idp="INC"),
    dict(key="facilities", orgs=["Harbor Point Facilities", "Crane & Lowe Property Services"], doc="Maintenance Response Standards", unit="work order", done="repaired", idp="WO"),
    dict(key="security", orgs=["Sentinel Watch", "Bastion MDR"], doc="Managed Detection Service Levels", unit="incident", done="contained", idp="SEC"),
]


def bmin(t0, t1, bh, wk, hs):
    total = 0
    day = t0.date()
    while day <= t1.date():
        if is_bday(day, hs, wk):
            s = dt.datetime(day.year, day.month, day.day) + dt.timedelta(minutes=bh[0])
            e = dt.datetime(day.year, day.month, day.day) + dt.timedelta(minutes=bh[1])
            lo, hi = max(s, t0), min(e, t1)
            if hi > lo:
                total += int((hi - lo).total_seconds() // 60)
        day += ONE
    return total


def bmin_indep(t0, t1, bh, wk, hj):
    a = naive_min(t0.date(), t0.hour, t0.minute)
    b = naive_min(t1.date(), t1.hour, t1.minute)
    tot = 0
    x = a
    while x < b:
        j, mod = divmod(x, 1440)
        if j_isb(j, hj, wk) and bh[0] <= mod < bh[1]:
            tot += 5
        x += 5
    return tot


def advance_b(t, mins, bh, wk, hs):
    cur = t
    while True:
        day = cur.date()
        base = dt.datetime(day.year, day.month, day.day)
        if is_bday(day, hs, wk):
            s, e = base + dt.timedelta(minutes=bh[0]), base + dt.timedelta(minutes=bh[1])
            if cur < s:
                cur = s
            if cur < e:
                av = int((e - cur).total_seconds() // 60)
                if mins <= av:
                    return cur + dt.timedelta(minutes=mins)
                mins -= av
        cur = base + ONE


def wall(a, b):
    return int((b - a).total_seconds() // 60)


def gen_sla(rng, size, F):
    D = pick(rng, SLA_D)
    org = pick(rng, D["orgs"])
    cid = "%s-%d" % (D["idp"], rng.randint(100000, 999999))
    bh = pick(rng, [(8 * 60, 18 * 60), (9 * 60, 17 * 60), (7 * 60, 19 * 60), (8 * 60 + 30, 17 * 60 + 30)])
    wk = (5, 6) if rng.random() < 0.8 else (6,)
    t_p1 = pick(rng, [2, 4, 6])
    t_p2 = pick(rng, [8, 12, 16])
    t_p3 = pick(rng, [24, 30, 40])
    targets = {"P1": (t_p1 * 60, "24x7"), "P2": (t_p2 * 60, "bh"), "P3": (t_p3 * 60, "bh")}
    B1, B2 = pick(rng, [(2, 8), (1, 4), (4, 16)])
    prio = pick(rng, ["P1", "P2", "P2", "P3", "P3"])
    recl = size != "short" and rng.random() < 0.5
    cust = pick(rng, [x for x in ("P1", "P2", "P3") if x != prio]) if recl else prio
    target, clock = targets[prio]
    over = pick(rng, [0, B1 * 60, B2 * 60]) + pick(rng, [-30, -5, 0, 0, 5, 45, -90])
    goal = max(60, target + over)
    d0 = rand_date(rng)
    t0 = dt.datetime(d0.year, d0.month, d0.day, rng.randint(0, 23), 5 * rng.randint(0, 11))
    lo = t0 - ONE * 5
    hols = make_holidays(rng, [], t0.date(), t0.date() + ONE * 12, n_extra=pick(rng, [0, 1, 1, 2]), wk=wk)
    hs = frozenset(hols)
    pause = rng.random() < 0.75
    a1 = 5 * rng.randint(3, max(4, goal * 7 // 50))
    a1 = min(a1, goal - 5)
    if clock == "24x7":
        p0 = t0 + dt.timedelta(minutes=a1)
        pw = 5 * rng.randint(6, 300)
        p1 = p0 + dt.timedelta(minutes=pw)
        t3 = p1 + dt.timedelta(minutes=goal - a1) if pause else t0 + dt.timedelta(minutes=goal)
    else:
        p0 = advance_b(t0, a1, bh, wk, hs)
        pw = 5 * rng.randint(6, 400)
        p1 = p0 + dt.timedelta(minutes=pw)
        t3 = advance_b(p1, goal - a1, bh, wk, hs) if pause else advance_b(t0, goal, bh, wk, hs)
    tr = t0 + dt.timedelta(minutes=5 * rng.randint(2, 20))
    p = dict(t0=t0, t3=t3, p0=p0, p1=p1, pause=pause, prio=prio, cust=cust, targets=targets, bh=bh, wk=wk, hs=hs)

    def compute(fl=()):
        pr = p["cust"] if "used_customer_priority" in fl else p["prio"]
        tg, ck = targets[pr]
        if ck == "24x7" or "wall_clock" in fl:
            el = wall(t0, t3) - (wall(p0, p1) if (pause and "ignored_pause" not in fl) else 0)
        else:
            h_ = frozenset() if "ignored_holidays" in fl else hs
            el = bmin(t0, t3, bh, wk, h_)
            if pause and "ignored_pause" not in fl:
                el -= wall(p0, p1) if "pause_as_wall" in fl else bmin(p0, p1, bh, wk, h_)
        ov = el - tg
        return (0 if ov <= 0 else 1 if ov <= B1 * 60 else 2 if ov <= B2 * 60 else 3), el
    g, el = compute()
    assert el == goal, "sla construction mismatch"
    hj = [jdn_date(h) for h in hols]
    if clock == "24x7":
        el_i = (naive_min(t3.date(), t3.hour, t3.minute) - naive_min(t0.date(), t0.hour, t0.minute)) - \
            ((naive_min(p1.date(), p1.hour, p1.minute) - naive_min(p0.date(), p0.hour, p0.minute)) if pause else 0)
    else:
        el_i = bmin_indep(t0, t3, bh, wk, hj) - (bmin_indep(p0, p1, bh, wk, hj) if pause else 0)
    assert el_i == el, "sla independent check failed"
    flags = ["wall_clock", "ignored_pause", "pause_as_wall", "ignored_holidays", "used_customer_priority"]
    res = [(f, compute((f,))[0]) for f in flags]
    if not any(v != g for _, v in res):
        raise Retry()
    labels = ordinal_labels(["Target met - no service credit", "5% service credit", "10% service credit", "20% service credit"])
    days = "Monday to Friday" if wk == (5, 6) else "Monday to Saturday"
    rules = ["Resolution targets by priority: P1 - %d hours, measured around the clock (24x7); P2 - %d business hours; P3 - %d business hours." % (t_p1, t_p2, t_p3),
             "Business hours are %s to %s, %s, excluding the public holidays listed below." % (F.t(*divmod(bh[0], 60)), F.t(*divmod(bh[1], 60)), days),
             "The clock runs from the time the %s is logged until it is %s." % (D["unit"], D["done"]),
             "The clock is paused while the %s is in 'Awaiting customer' status and restarts when the customer responds. Paused time is excluded in the same units as the target." % D["unit"],
             "Service credits depend on how far the target was exceeded, measured in the same units as the target: up to and including %s - 5%%; more than %s and up to and including %s - 10%%; more than %s - 20%%." % (hrs(B1), hrs(B1), hrs(B2), hrs(B2)),
             "Public holidays: %s." % (hol_text(rng, F, hols) if hols else "none in the relevant period")]
    if recl or rng.random() < 0.3:
        rules.append("Targets follow the priority assigned by %s at triage; the priority selected by the customer when logging is not binding." % org)
    if size != "short" and rng.random() < 0.4:
        rules.append(pick(rng, DOMAIN_FILLER.get(D["key"], DOMAIN_FILLER["telecom"])))
    facts = [("Reference", cid), ("Logged", F.dtm(t0)), ("Priority chosen by customer", cust),
             ("Priority assigned at triage", prio), ("First response", F.dtm(tr))]
    if pause:
        facts += [("Status set to Awaiting customer", F.dtm(p0)), ("Customer responded", F.dtm(p1))]
    facts.append(("%s" % cap(D["done"]), F.dtm(t3)))
    q = "What service credit is due for %s %s?" % (D["unit"], cid)
    k1 = label_kind(q, "Is \"{opt}\" the service credit due for %s %s?" % (D["unit"], cid), labels, g, res)
    yn = [("Was the resolution target for %s %s met?" % (D["unit"], cid), int(g == 0)),
          ("Is a service credit of 10%% or more due for %s?" % cid, int(g >= 2))]
    reasons = {"wall_clock": "from %s to %s is %.1f hours on the clock" % (F.dtm(t0), F.dtm(t3), wall(t0, t3) / 60.0),
               "ignored_pause": "the pause doesn't matter, the customer's delay is still our time",
               "pause_as_wall": "the pause was only %.1f hours so I took that off" % (wall(p0, p1) / 60.0),
               "ignored_holidays": "I counted every weekday in the period as a business day",
               "used_customer_priority": "the customer logged it as %s" % cust}
    notes = [(f, note_text(rng, reasons[f], labels[v])) for f, v in res if v != g]
    traps = ["business_hours"] + (["clock_pause"] if pause else []) + (["surface_cue"] if recl else []) + \
        (["boundary"] if min(abs(goal - target), abs(goal - target - B1 * 60), abs(goal - target - B2 * 60)) <= 5 else [])
    return mk_scn(tpl="sla." + D["key"], domain=D["key"], org=org, F=F, title="%s - %s" % (org, D["doc"]), head="Service levels",
                  rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="SLA check for %s" % cid, sender=pick(rng, PEOPLE), checked=True)



# ============================================================ S6  which rule version applies (effective dates)
def gen_ver_perdiem(rng, size, F):
    org = pick(rng, ["Meridian Consulting Group", "Talbot & Reyes LLP", "Quanta Analytics", "Kestrel Components"])
    name = pick(rng, PEOPLE)
    cid = "TRV-%d" % rng.randint(10000, 99999)
    EFF = rand_date(rng)
    Ro, Rn = rng.sample([59, 64, 68, 69, 74, 79, 86], 2)
    n = rng.randint(1, 6)
    start = EFF - ONE * rng.randint(0, max(0, n - 1)) if rng.random() < 0.8 else EFF + ONE * pick(rng, [-n - 1, 1, 3])
    end = start + ONE * (n - 1)
    conv = pick(rng, ["daily", "daily", "first"])

    def amount(fl=()):
        days = [start + ONE * i for i in range(n)]
        if "counted_nights" in fl and n > 1:
            days = days[:-1]
        cv = conv
        if "wrong_rate_convention" in fl:
            cv = "first" if conv == "daily" else "daily"
        tot = Fraction(0)
        for i, d in enumerate(days):
            ref = start if cv == "first" else d
            if "all_new_rate" in fl:
                r = Rn
            elif "all_old_rate" in fl:
                r = Ro
            else:
                new = ref > EFF if "eff_day_old" in fl else ref >= EFF
                r = Rn if new else Ro
            f = Fraction(3, 4) if (i == 0 or i == len(days) - 1) and "ignored_75pct" not in fl else Fraction(1)
            tot += r * f
        return tot
    g = amount()
    # independent: quarters, JDN comparisons
    je, js = jdn_date(EFF), jdn_date(start)
    q = 0
    for i in range(n):
        ref = js if conv == "first" else js + i
        r = Rn if ref >= je else Ro
        q += r * (3 if i in (0, n - 1) else 4)
    assert Fraction(q, 4) == g, "per diem independent check failed"
    flags = ["all_new_rate", "all_old_rate", "eff_day_old", "ignored_75pct", "counted_nights", "wrong_rate_convention"]
    var = [(f, amount((f,))) for f in flags]
    if sum(1 for _, v in var if v != g) < 2:
        raise Retry()
    fm = lambda x: money(x)
    rules = ["Meals and incidental expenses (M&IE) are paid at a daily rate for every calendar day of travel, including the day of departure and the day of return.",
             "On the first and on the last day of travel, 75% of the daily rate is paid (a one-day trip is paid at 75%).",
             "Daily M&IE rate for the destination: %s per day up to and including %s; %s per day from %s onwards." % (money(Ro), F.d(EFF - ONE), money(Rn), F.d(EFF)),
             "The rate for each day of travel is the rate in force on that day." if conv == "daily" else
             "The rate in force on the first day of travel applies to every day of the trip, even if the rate changes during the trip."]
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["travel"]))
    claimed = pick(rng, [v for _, v in var if v != g])
    facts = [("Trip", cid), ("Traveller", name), ("Departure", F.d(start)), ("Return", F.d(end)),
             ("Destination", pick(rng, PLACES)), ("Hotel nights", str(max(0, n - 1))),
             ("M&IE claimed by traveller", fm(claimed))]
    q = "What M&IE amount should be reimbursed for trip %s?" % cid
    k1 = value_kind("amount", q, "Is {opt} the correct M&IE reimbursement for trip %s?" % cid, g, var, fm)
    yn = [("Should the M&IE claimed by the traveller for trip %s (%s) be paid exactly as claimed?" % (cid, fm(claimed)), 0),
          ("Is the correct M&IE reimbursement for trip %s more than %s?" % (cid, fm(claimed)), int(g > claimed))]
    R = {"all_new_rate": "the new rate is in force now, so it applies to the whole trip",
         "all_old_rate": "the trip was booked under the old rate, so that rate applies throughout",
         "eff_day_old": "the new rate only starts the day after %s" % F.d(EFF),
         "ignored_75pct": "every travel day gets the full daily rate",
         "counted_nights": "I paid one day per hotel night",
         "wrong_rate_convention": "the rate is set per day of travel" if conv == "first" else "the first day's rate covers the whole trip"}
    notes = [(f, note_value(rng, R[f], fm(v))) for f, v in var if v != g]
    traps = ["superseded_rule", "effective_date"] + (["boundary"] if start <= EFF <= end else [])
    return mk_scn(tpl="version.per_diem", domain="travel", org=org, F=F, title="%s - Travel Policy, Annex B (M&IE)" % org,
                  head="Meals and incidental expenses", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps,
                  cid=cid, subject="M&IE check for %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_ver_deductible(rng, size, F):
    org = pick(rng, ["Harborview Mutual", "Kestrel Insurance Co.", "Bluestone Assurance"])
    name = pick(rng, PEOPLE)
    cid = "CLM-%d" % rng.randint(10000, 99999)
    EFF = rand_date(rng)
    do, dn = rng.sample([250, 500, 750, 1000, 1500, 2500], 2)
    lim = pick(rng, [5000, 10000, 15000, 25000])
    LD = EFF + ONE * pick(rng, [-20, -3, -1, 0, 0, 1, 2, 15])
    RD = LD + ONE * rng.randint(2, 40)
    if (LD < EFF) == (RD < EFF) and rng.random() < 0.7:
        RD = EFF + ONE * rng.randint(1, 20) if LD < EFF else RD
    loss = pick(rng, [lim + pick(rng, [do, dn]) - 250, lim + 300, rng.randint(8, 60) * 250, lim + max(do, dn) + 500])

    def pay(fl=()):
        ref = RD if "used_report_date" in fl else LD
        new = ref > EFF if "eff_day_old" in fl else ref >= EFF
        ded = dn if new else do
        if "forgot_deductible" in fl:
            ded = 0
        x = max(loss - ded, 0)
        if "forgot_limit" in fl:
            return x
        if "deducted_after_limit" in fl:
            return max(min(loss, lim) - ded, 0)
        return min(x, lim)
    g = pay()
    ded_i = dn if jdn_date(LD) >= jdn_date(EFF) else do
    gi = loss - ded_i if loss - ded_i < lim else lim
    assert max(gi, 0) == g, "deductible independent check failed"
    flags = ["used_report_date", "eff_day_old", "forgot_deductible", "forgot_limit", "deducted_after_limit"]
    var = [(f, pay((f,))) for f in flags]
    if sum(1 for _, v in var if v != g) < 2:
        raise Retry()
    rules = ["The policy year renews at 00:00 on %s. From that time the deductible for water-damage claims changes from %s to %s." % (F.d(EFF), money(do), money(dn)),
             "The deductible that applies to a claim is the one in force on the date the loss occurred, whatever the date on which the claim is reported or settled.",
             "The deductible is subtracted from the assessed loss first; the result is then subject to the per-claim limit of %s." % money(lim)]
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["insurance"]))
    facts = [("Claim", cid), ("Policyholder", name), ("Date of loss", F.d(LD)), ("Date reported", F.d(RD)),
             ("Assessed loss", money(loss)), ("Peril", "Escape of water")]
    q = "What amount should be paid on claim %s?" % cid
    k1 = value_kind("amount", q, "Is {opt} the correct payment on claim %s?" % cid, g, var, money)
    usednew = LD >= EFF
    yn = [("Does the renewed (%s) deductible apply to claim %s?" % (money(dn), cid), int(usednew)),
          ("Is the payment on claim %s capped by the per-claim limit?" % cid, int(loss - (dn if usednew else do) > lim))]
    R = {"used_report_date": "the claim was reported on %s, so that year's deductible applies" % F.d(RD),
         "eff_day_old": "the renewal only takes effect after %s" % F.d(EFF),
         "forgot_deductible": "the deductible was waived as it's a water claim",
         "forgot_limit": "the loss minus the deductible is what we owe",
         "deducted_after_limit": "cap the loss at the limit first and then take off the deductible"}
    notes = [(f, note_value(rng, R[f], money(v))) for f, v in var if v != g]
    traps = ["effective_date", "surface_cue"] + (["boundary"] if abs((LD - EFF).days) <= 1 else [])
    return mk_scn(tpl="version.deductible", domain="insurance", org=org, F=F, title="%s - Household Policy Schedule and Wording" % org,
                  head="Deductibles and limits", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps,
                  cid=cid, subject="Settlement figure for %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_ver_parental(rng, size, F):
    org = pick(rng, ["Castellan Foods Ltd", "Norvale Engineering", "Pinecrest Hospital Trust", "Quanta Analytics"])
    name = pick(rng, PEOPLE)
    cid = "EMP-%d" % rng.randint(10000, 99999)
    EFF = rand_date(rng)
    Wo, Wn = pick(rng, [(12, 16), (14, 18), (16, 20), (18, 26), (20, 16)])
    birth = EFF + ONE * pick(rng, [-9, -2, -1, 0, 1, 3, 12])
    due = birth + ONE * pick(rng, [-12, -6, 5, 10, 16]) if rng.random() < 0.8 else birth
    LS = birth + ONE * pick(rng, [0, 0, 3, 7])

    def end(fl=()):
        ref = due if "used_due_date" in fl else birth
        new = ref >= EFF
        if "wrong_version" in fl:
            new = not new
        w = Wn if new else Wo
        st = birth if "used_birth_as_start" in fl else LS
        return st + ONE * (7 * w - (0 if "off_by_one" in fl else 1))
    g = end()
    wi = Wn if jdn_date(birth) >= jdn_date(EFF) else Wo
    assert jdn_to_date(jdn_date(LS) + 7 * wi - 1) == g, "parental independent check failed"
    flags = ["used_due_date", "wrong_version", "off_by_one", "used_birth_as_start"]
    var = [(f, end((f,))) for f in flags]
    rules = ["Birth-parent leave is %d weeks for children born on or after %s (previously %d weeks)." % (Wn, F.d(EFF), Wo),
             "Entitlement is determined by the child's actual date of birth, not the expected week of childbirth.",
             "Leave is taken as one continuous block starting on the date chosen by the employee; the last day of leave is the day before the same weekday %d or %d weeks later, as applicable." % (Wo, Wn)]
    if rng.random() < 0.5:
        rules[2] = "Leave is one continuous block; a leave of N weeks that starts on a given day ends on the day before the same weekday N weeks later."
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["hr"]))
    facts = [("Employee", "%s (%s)" % (name, cid)), ("Expected date of childbirth", F.d(due)), ("Actual date of birth", F.d(birth)),
             ("Leave start date", F.d(LS)), ("Department", pick(rng, ["Finance", "Logistics", "Ward 7", "R&D"]))]
    q = "What is the last day of %s's birth-parent leave?" % name
    k1 = value_kind("date", q, "Is {opt} the last day of %s's birth-parent leave?" % name, g, var, F.od, [("off_by_one", g - ONE)])
    yn = [("Is %s entitled to the %d-week leave?" % (name, Wn), int(birth >= EFF))]
    R = {"used_due_date": "the baby was due on %s, so that decides which scheme applies" % F.d(due),
         "wrong_version": "the policy that applies is the other one",
         "off_by_one": "the leave runs to the same weekday at the end of the period",
         "used_birth_as_start": "leave is counted from the birth date"}
    notes = [(f, note_value(rng, R[f], F.d(v))) for f, v in var if v != g]
    traps = ["effective_date", "surface_cue"] + (["boundary"] if abs((birth - EFF).days) <= 1 else [])
    return mk_scn(tpl="version.parental_leave", domain="hr", org=org, F=F, title="%s - Family Leave Policy" % org,
                  head="Birth-parent leave", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps,
                  cid=cid, subject="Leave end date for %s" % name, sender=pick(rng, PEOPLE), checked=True)


def gen_ver_tuition(rng, size, F):
    org = pick(rng, ["Westbrook University", "Carroway College", "Lakeshore Institute of Technology"])
    name = pick(rng, PEOPLE)
    cid = "S%d" % rng.randint(1000000, 9999999)
    new_s = pick(rng, [[(7, 100), (14, 75), (28, 50)], [(10, 100), (20, 50)], [(5, 100), (12, 80), (19, 50), (26, 25)]])
    old_s = pick(rng, [[(14, 100), (21, 50)], [(7, 100), (21, 75), (35, 25)], [(10, 90), (30, 50)]])
    EFF = rand_date(rng)
    ver = size != "short" and rng.random() < 0.6
    TS = EFF + ONE * pick(rng, [-120, -5, 0, 0, 3, 90]) if ver else rand_date(rng)
    use_old = ver and TS < EFF
    sch = old_s if use_old else new_s
    th = pick(rng, [t for t, _ in sch])
    WD = TS + ONE * (th - 1 + pick(rng, [-1, 0, 0, 1, 2]))
    LA = WD - ONE * rng.randint(3, 15)

    def pct(fl=()):
        s_ = sch
        if "wrong_version" in fl and ver:
            s_ = new_s if use_old else old_s
        ref = LA if "used_last_attendance" in fl else WD
        dnum = (ref - TS).days + (0 if "off_by_one" in fl else 1)
        for t, pc in s_:
            if dnum <= t:
                return pc
        return 0
    g = pct()
    dn_i = jdn_date(WD) - jdn_date(TS) + 1
    gi = 0
    for t, pc in sch:
        if dn_i <= t:
            gi = pc
            break
    assert gi == g, "tuition independent check failed"
    levels = sorted(set([0] + [pc for _, pc in new_s] + ([pc for _, pc in old_s] if ver else [])))
    labels = ordinal_labels([("No refund" if x == 0 else "%d%% refund" % x) for x in levels])
    flags = ["off_by_one", "used_last_attendance"] + (["wrong_version"] if ver else [])
    var = [(f, levels.index(pct((f,)))) for f in flags]
    if all(v == levels.index(g) for _, v in var):
        raise Retry()

    def sched_text(sc):
        parts, prev = [], 0
        for t, pc in sc:
            parts.append("withdrawal effective on day %d to %d: %d%%" % (prev + 1, t, pc) if prev else "withdrawal effective on or before day %d: %d%%" % (t, pc))
            prev = t
        parts.append("after day %d: no refund" % prev)
        return "; ".join(parts) + "."
    rules = ["Day 1 of term is the first day of classes; days are calendar days.",
             "A withdrawal is effective on the date the withdrawal form is received by the Registry, not the last date of attendance.",
             "Tuition refund schedule: " + sched_text(new_s)]
    old = None
    if ver:
        rules.append("This schedule applies to terms starting on or after %s. Terms that started earlier keep the previous schedule." % F.d(EFF))
        old = ("Previous refund schedule (terms starting before %s)" % F.d(EFF), [sched_text(old_s)])
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["education"]))
    facts = [("Student", "%s (%s)" % (name, cid)), ("Term start (first day of classes)", F.d(TS)),
             ("Last date of attendance", F.d(LA)), ("Withdrawal form received by Registry", F.d(WD)),
             ("Tuition charged", money(rng.randint(20, 90) * 100))]
    q = "What tuition refund is %s entitled to?" % name
    k1 = label_kind(q, "Is %s entitled to \"{opt}\"?" % name, labels, levels.index(g), var)
    yn = [("Is %s entitled to any tuition refund?" % name, int(g > 0))]
    R = {"off_by_one": "the form arrived %d days after term started" % (WD - TS).days,
         "used_last_attendance": "the student stopped attending on %s" % F.d(LA),
         "wrong_version": "the refund schedule to use is the other one"}
    notes = [(f, note_text(rng, R[f], labels[v])) for f, v in var if v != levels.index(g)]
    traps = ["boundary", "surface_cue"] + (["superseded_rule"] if ver else [])
    return mk_scn(tpl="version.tuition_refund", domain="education", org=org, F=F, title="%s - Fees and Refunds Regulations" % org,
                  head="Refunds on withdrawal", rules=rules, old=old, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps,
                  cid=cid, subject="Refund for %s" % name, sender=pick(rng, PEOPLE), checked=True)


def gen_ver_price(rng, size, F):
    org = pick(rng, ["Brightline Telecom", "Skyreach Mobile", "Lumen Cloud", "Clearwater Utilities"])
    cid = "ACC-%d" % rng.randint(100000, 999999)
    c = rng.randint(1, 28)
    mode = pick(rng, ["ge30", "gt30", "month"])
    y, m = rng.randint(2025, 2028), rng.randint(1, 12)
    S0 = dt.date(y, m, c)
    if mode == "month":
        N = add_months(S0, -1) + ONE * pick(rng, [-1, 0, 0, 1, 2])
    else:
        N = S0 - ONE * (30 - pick(rng, [-1, 0, 0, 1, 2]))

    def cycle_on_or_after(d, strict=False):
        x = dt.date(d.year, d.month, c)
        k = 0
        while x < d or (strict and x == d):
            k += 1
            x = add_months(dt.date(d.year, d.month, c), k)
        return x

    def first(fl=()):
        md = mode
        if "used_30_days" in fl:
            md = "ge30"
        if "used_calendar_month" in fl:
            md = "month"
        if "off_by_one" in fl:
            md = {"ge30": "gt30", "gt30": "ge30", "month": "month_gt"}[md]
        if "next_cycle" in fl:
            return cycle_on_or_after(N, strict=True)
        if "no_cycle_alignment" in fl:
            return N + ONE * 30 if mode != "month" else add_months(N, 1)
        if md == "ge30":
            return cycle_on_or_after(N + ONE * 30)
        if md == "gt30":
            return cycle_on_or_after(N + ONE * 30, strict=True)
        if md == "month":
            return cycle_on_or_after(add_months(N, 1))
        return cycle_on_or_after(add_months(N, 1), strict=True)
    g = first()
    # independent: scan day by day with JDN for the first day whose day-of-month is c and satisfies the rule
    jN = jdn_date(N)
    lim = jdn_date(add_months_indep(N, 1)) if mode == "month" else jN + 30
    j = jN + 1
    while True:
        yy, mm, dd = jdn_to_ymd(j)
        okd = (j >= lim) if mode != "gt30" else (j > lim)
        if dd == c and okd:
            break
        j += 1
    assert jdn_to_date(j) == g, "price independent check failed"
    flags = ["off_by_one", "next_cycle", "no_cycle_alignment"] + (["used_calendar_month"] if mode != "month" else ["used_30_days"])
    var = [(f, first((f,))) for f in flags]
    if sum(1 for _, v in var if v != g) < 2:
        raise Retry()
    rtxt = {"ge30": "A price change takes effect from the first billing period that starts at least 30 days after the date of the notice.",
            "gt30": "A price change takes effect from the first billing period that starts more than 30 days after the date of the notice.",
            "month": "A price change takes effect from the first billing period that starts at least one calendar month after the date of the notice (same day of the following month, or the last day of that month if it has no such day)."}[mode]
    rules = [rtxt, "Billing periods start on the %s day of each month." % ordinal(c),
             "Customers may leave without an early termination fee before the price change takes effect."]
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["telecom"]))
    old_p = rng.randint(20, 60)
    facts = [("Account", cid), ("Price-change notice dated", F.d(N)), ("Current monthly price", money(old_p)),
             ("New monthly price", money(old_p + rng.randint(2, 9))), ("Notice channel", pick(rng, ["email", "letter", "SMS and email"]))]
    q = "From which billing period start date does the new price apply to account %s?" % cid
    k1 = value_kind("date", q, "Does the new price first apply to account %s from the billing period starting {opt}?" % cid, g, var, F.od)
    X = pick(rng, [g, add_months(g, -1)])
    yn = [("Will the billing period starting %s for account %s be charged at the new price?" % (F.d(X), cid), int(X >= g))]
    R = {"off_by_one": "30 days after the notice is the cut-off and that day itself counts differently",
         "next_cycle": "it applies from the very next bill after the notice",
         "no_cycle_alignment": "the change is effective 30 days (or a month) after the notice",
         "used_calendar_month": "a month's notice is what's required",
         "used_30_days": "30 days' notice is enough"}
    notes = [(f, note_value(rng, R[f], F.d(v))) for f, v in var if v != g]
    traps = ["boundary", "month_length" if mode == "month" else "day_count"]
    return mk_scn(tpl="version.price_change", domain="telecom", org=org, F=F, title="%s - General Terms, Clause 14 (Price changes)" % org,
                  head="Changes to prices", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="When does the new price start for %s?" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_ver_benefit(rng, size, F):
    org = pick(rng, ["Summit County Benefits Office", "Riverside Department of Social Services", "Harlow District Council"])
    name = pick(rng, PEOPLE)
    cid = "APP-%d" % rng.randint(10000, 99999)
    EFF = rand_date(rng)
    Lo = rng.randint(20, 40) * 1000
    Ln = Lo + pick(rng, [-2500, 1500, 2000, 3000])
    freq = pick(rng, [("weekly", 52, 48, "4 weeks a month"), ("every two weeks", 26, 24, "twice a month"),
                      ("twice a month", 24, 26, "every two weeks"), ("monthly", 12, 13, "13 periods")])
    fname, fac, wfac, wdesc = freq
    AR = EFF + ONE * pick(rng, [-15, -2, -1, 0, 1, 4])
    DD = AR + ONE * rng.randint(5, 30)
    lim = Ln if AR >= EFF else Lo
    other = Lo if AR >= EFF else Ln
    lo_, hi_ = min(lim, other), max(lim, other)
    annual_t = pick(rng, [lim, lim - 100, lim + 100, (lo_ + hi_) // 2, int(lim * 1.02), int(lim * 0.98)])
    amt = max(100, int(round(annual_t / fac)))

    def elig(fl=()):
        L_ = lim
        if "used_decision_date" in fl:
            L_ = Ln if DD >= EFF else Lo
        f_ = wfac if "wrong_pay_frequency" in fl else fac
        if "monthly_vs_annual" in fl:
            return int(amt <= L_)
        ann = amt * f_
        return int(ann <= L_) if "strict_limit" not in fl else int(ann < L_)
    g = elig()
    assert int(amt * fac <= (Ln if jdn_date(AR) >= jdn_date(EFF) else Lo)) == g, "benefit independent check failed"
    labels = ["Eligible", "Not eligible - income above the limit"]
    flags = ["used_decision_date", "wrong_pay_frequency", "strict_limit"]
    var = [(f, 1 - elig((f,))) for f in flags]
    if all(v == 1 - g for _, v in var):
        raise Retry()
    rules = ["A household is eligible if its annual gross income does not exceed the income limit.",
             "Income limit: %s a year for applications assessed under the rules in force before %s; %s a year from %s." % (money(Lo), F.d(EFF), money(Ln), F.d(EFF)),
             "An application is assessed under the rules in force on the date the complete application was received, not the date of the decision.",
             "Annual income is calculated from the regular pay amount multiplied by the number of pay periods in a year (weekly: 52; every two weeks: 26; twice a month: 24; monthly: 12)."]
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["benefits"]))
    facts = [("Application", cid), ("Applicant", name), ("Complete application received", F.d(AR)),
             ("Decision date", F.d(DD)), ("Gross pay", "%s, paid %s" % (money(amt), fname)), ("Household size", str(rng.randint(1, 6)))]
    q = "What is the correct eligibility decision for application %s?" % cid
    k1 = label_kind(q, "Is \"{opt}\" the correct decision for application %s?" % cid, labels, 1 - g, var)
    yn = [("Is application %s eligible?" % cid, g)]
    R = {"used_decision_date": "the decision was made on %s, so that date's limit applies" % F.d(DD),
         "wrong_pay_frequency": "paid %s is the same as %s" % (fname, wdesc),
         "strict_limit": "income has to be below the limit"}
    notes = [(f, note_text(rng, R[f], labels[v])) for f, v in var if v != 1 - g]
    traps = ["effective_date", "unit_pay_frequency"] + (["boundary"] if abs(amt * fac - lim) <= 200 else [])
    return mk_scn(tpl="version.benefit_limit", domain="benefits", org=org, F=F, title="%s - Eligibility Manual, Chapter 3" % org,
                  head="Income test", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="Eligibility decision %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_version(rng, size, F):
    return dispatch(rng, size, F, [gen_ver_perdiem, gen_ver_deductible, gen_ver_parental, gen_ver_tuition, gen_ver_price, gen_ver_benefit])


# ============================================================ S7  schedule adherence / intervals
def gen_adh_flight(rng, size, F):
    org = pick(rng, ["Aerolinea Costa", "Northwind Air", "Bluecrest Airways", "Coastal Rail Express"])
    rail = "Rail" in org
    cid = "%s%d" % (pick(rng, ["NW", "BC", "AC", "CR"]), rng.randint(100, 9999))
    name = pick(rng, PEOPLE)
    o1, o2 = two_offsets(rng, 60) if rng.random() < 0.6 else (0, 0)
    sd = rand_date(rng)
    sa = dt.datetime(sd.year, sd.month, sd.day, rng.randint(6, 23), 5 * rng.randint(0, 11))
    if rng.random() < 0.8:
        delay = pick(rng, [15, 180]) + pick(rng, [-10, -1, 0, 0, 1, 5, 25])
    else:
        delay = rng.randint(-20, 300)
    ga = sa + dt.timedelta(minutes=delay)
    taxi = 5 * rng.randint(1, 5)
    td = ga - dt.timedelta(minutes=taxi)
    dep_delay = delay + pick(rng, [-40, -25, 20, 35])
    block = 5 * rng.randint(18, 100)
    sdep_u = utc_of(sa.date(), sa.hour, sa.minute, o2) - dt.timedelta(minutes=block)
    sdd, sdh, sdm = local_of(sdep_u, o1)
    adep_u = sdep_u + dt.timedelta(minutes=dep_delay)
    add_, adh, adm = local_of(adep_u, o1)

    def band(x, fl=()):
        on = x <= 15 if "boundary_inclusive" in fl else x < 15
        comp = x > 180 if "boundary_exclusive" in fl else x >= 180
        return 0 if on else (2 if comp else 1)
    g = band(delay)
    gi = naive_min(ga.date(), ga.hour, ga.minute) - naive_min(sa.date(), sa.hour, sa.minute)
    assert gi == delay and band(gi) == g, "flight independent check failed"
    tdl = delay - taxi
    var = [("used_touchdown_time", band(tdl)), ("used_departure_delay", band(dep_delay)),
           ("boundary_inclusive", band(delay, ("boundary_inclusive",))), ("boundary_exclusive", band(delay, ("boundary_exclusive",)))]
    if all(v == g for _, v in var):
        raise Retry()
    veh = "train" if rail else "flight"
    arr_word = "reaches the platform" if rail else "reaches the arrival gate (on-block time)"
    labels = ordinal_labels(["On time", "Delayed - no compensation", "Delayed 3 hours or more - compensation due"])
    rules = ["Arrival time means the time the %s %s; %s is not used." % (veh, arr_word, "the time it passes the station signal" if rail else "touchdown time"),
             "A %s is on time if it arrives less than 15 minutes after its scheduled arrival time." % veh,
             "Passengers whose %s arrives 3 hours or more after its scheduled arrival time are entitled to compensation." % veh,
             "Times in the timetable and in operational logs are local times at the station or airport concerned."]
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["travel"]))
    tdn = "Passed station signal" if rail else "Touchdown"
    facts = [("Service", cid), ("Passenger claim by", name),
             ("Scheduled departure", "%s %s (local, %s)" % (F.d(sdd), F.t(sdh, sdm), fofs(o1))),
             ("Actual departure", "%s %s (local, %s)" % (F.d(add_), F.t(adh, adm), fofs(o1))),
             ("Scheduled arrival", "%s %s (local, %s)" % (F.d(sa.date()), F.t(sa.hour, sa.minute), fofs(o2))),
             (tdn, "%s %s (local)" % (F.d(td.date()), F.t(td.hour, td.minute))),
             ("Arrival at gate" if not rail else "Arrival at platform", "%s %s (local)" % (F.d(ga.date()), F.t(ga.hour, ga.minute)))]
    q = "How should the arrival of %s %s be classified?" % (veh, cid)
    k1 = label_kind(q, "Should the arrival of %s %s be classified as \"{opt}\"?" % (veh, cid), labels, g, var)
    yn = [("Is %s entitled to compensation for %s %s?" % (name, veh, cid), int(g == 2)), ("Did %s %s arrive on time?" % (veh, cid), int(g == 0))]
    R = {"used_touchdown_time": ("it passed the signal at %s" if rail else "it touched down at %s") % F.t(td.hour, td.minute),
         "used_departure_delay": "it left %d minutes late" % dep_delay,
         "boundary_inclusive": "exactly 15 minutes late still counts as on time",
         "boundary_exclusive": "you need more than 3 hours for compensation"}
    notes = [(f, note_text(rng, R[f], labels[v])) for f, v in var if v != g]
    traps = ["surface_cue"] + (["boundary"] if min(abs(delay - 15), abs(delay - 180)) <= 1 else [])
    return mk_scn(tpl="adherence.arrival", domain="travel", org=org, F=F, title="%s - Punctuality and Compensation Rules" % org,
                  head="Punctuality", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="Delay claim %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_adh_vaccine(rng, size, F):
    org = pick(rng, ["Arbor Community Health", "Bayside Care Network", "Crestview Pediatrics"])
    name = pick(rng, PEOPLE)
    cid = "IMM-%d" % rng.randint(10000, 99999)
    vac, I = pick(rng, [("hepatitis A", 180), ("HPV", 150), ("varicella", 28), ("MMR", 28), ("hepatitis B", 28), ("Tdap booster", 56), ("rotavirus", 28)])
    It = "%d weeks" % (I // 7) if I % 7 == 0 and rng.random() < 0.6 else "%d days" % I
    grace = not (vac == "rotavirus" and rng.random() < 0.0)
    exc = size != "short" and rng.random() < 0.35
    live = vac in ("varicella", "MMR")
    d1 = rand_date(rng)
    gap = I - 4 + pick(rng, [-2, -1, -1, 0, 0, 1, 4]) if rng.random() < 0.85 else I + rng.randint(60, 400)
    d2 = d1 + ONE * gap
    rule_live = exc and live

    def status(fl=()):
        gr = 4
        if "forgot_grace" in fl or (rule_live and "misapplied_grace" not in fl):
            gr = 0
        if "grace_off_by_one" in fl and gr:
            gr = 5
        need = I if "weeks_as_months" not in fl else (add_months(d1, max(1, I // 28)) - d1).days
        if "restart_series" in fl and gap > I + 30:
            return 2
        return 0 if gap >= need - gr else 1

    def earliest(fl=()):
        gr = 0 if ("forgot_grace" in fl or (rule_live and "misapplied_grace" not in fl)) else (5 if "grace_off_by_one" in fl else 4)
        need = I if "weeks_as_months" not in fl else (add_months(d1, max(1, I // 28)) - d1).days
        return d1 + ONE * (need - gr)
    g = status()
    ge = earliest()
    gi_need = I - (0 if rule_live else 4)
    assert (0 if jdn_date(d2) - jdn_date(d1) >= gi_need else 1) == g and jdn_to_date(jdn_date(d1) + gi_need) == ge, "vaccine independent check failed"
    flags = ["forgot_grace", "grace_off_by_one", "restart_series"] + (["misapplied_grace"] if rule_live else []) + (["weeks_as_months"] if "weeks" in It else [])
    var = [(f, status((f,))) for f in flags]
    evar = [(f, earliest((f,))) for f in flags if f != "restart_series"]
    labels = ["Valid dose - continue the series", "Invalid dose - repeat it after the minimum interval", "Restart the series from dose 1"]
    rules = ["The minimum interval between dose 1 and dose 2 of %s vaccine is %s." % (vac, It),
             "A dose given up to 4 days before the minimum interval has elapsed is counted as valid (the 4-day grace period).",
             "A dose given 5 or more days early is invalid and must be repeated; the repeat dose is due once the minimum interval has passed after the invalid dose.",
             "There is no maximum interval: never restart a series because of a long gap between doses."]
    if exc:
        rules.append("The grace period does not apply to live vaccines (MMR, varicella) when the minimum interval must be respected in full to avoid interference; for these, the full %s applies." % It if live else
                     "The grace period does not apply to live vaccines (MMR, varicella); it does apply to all other vaccines.")
    if size != "short" and rng.random() < 0.4:
        rules.append(pick(rng, DOMAIN_FILLER["healthcare"]))
    facts = [("Patient", "%s (%s)" % (name, cid)), ("Vaccine", vac), ("Dose 1 given", F.d(d1)), ("Dose 2 given", F.d(d2)),
             ("Clinic", pick(rng, PLACES))]
    k1 = label_kind("How should dose 2 of %s for patient %s be recorded?" % (vac, cid),
                    "Should dose 2 for patient %s be recorded as \"{opt}\"?" % cid, labels, g, var)
    k2 = value_kind("date", "What was the earliest date on which dose 2 of %s could have been given to patient %s and still count as valid?" % (vac, cid),
                    "Was {opt} the earliest date on which dose 2 for patient %s would count as valid?" % cid, ge, evar, F.od,
                    [("off_by_one", ge + ONE), ("off_by_one", ge - ONE)])
    yn = [("Does dose 2 for patient %s count as valid?" % cid, int(g == 0))]
    R = {"forgot_grace": "it was given before the full %s had passed" % It,
         "grace_off_by_one": "it's within the grace period if you count the days generously",
         "restart_series": "the gap was so long the series has to start again",
         "misapplied_grace": "the 4-day grace period covers it",
         "weeks_as_months": "%s is basically a calendar month" % It}
    notes = [(f, note_text(rng, R[f], labels[v])) for f, v in var if v != g]
    traps = ["grace_period"] + (["boundary"] if abs(gap - (I - 4)) <= 1 else []) + (["exception"] if exc else [])
    return mk_scn(tpl="adherence.vaccine_interval", domain="healthcare", org=org, F=F, title="%s - Immunization Schedule Guidance" % org,
                  head="Minimum intervals and grace period", rules=rules, facts=facts, kinds=[k1, k2], yn=yn, notes=notes,
                  traps=traps, cid=cid, subject="Dose 2 validity - %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_adh_calibration(rng, size, F):
    org = pick(rng, ["Kestrel Components", "Ironvale Fabrication", "Delta Precision Castings", "Gulfstar Plastics"])
    cid = "GAUGE-%d" % rng.randint(1000, 9999)
    lot = "LOT-%d" % rng.randint(10000, 99999)
    unit = pick(rng, ["days", "months"])
    n = pick(rng, [90, 180, 365]) if unit == "days" else pick(rng, [3, 6, 12])
    cls = pick(rng, ["A", "B", "B"])
    safety = rng.random() < 0.35
    exc = size != "short" and rng.random() < 0.6
    C = rand_date(rng)
    if unit == "months" and rng.random() < 0.6:
        C = dt.date(C.year, C.month, min(31, dim(C.year, C.month)))

    def due(fl=()):
        if unit == "days":
            return C + ONE * n if "wrong_unit" not in fl else add_months(C, max(1, round(n / 30)))
        return add_months(C, n) if "wrong_unit" not in fl else C + ONE * (30 * n)
    G = 7
    Dd = due()
    M = Dd + ONE * pick(rng, [-1, 0, 0, 1, 2, G, G + 1, 3])

    def status(fl=()):
        d_ = due(fl)
        in_cal = M <= d_ if "off_by_one" not in fl else M < d_
        if in_cal:
            return 0
        g_ok = cls == "B" and not (exc and safety)
        if "misapplied_grace" in fl:
            g_ok = cls == "B"
        if "forgot_grace" in fl:
            g_ok = False
        return 1 if (g_ok and M <= d_ + ONE * G) else 2
    g = status()
    if unit == "days":
        jd = jdn_date(C) + n
    else:
        jd = jdn_date(add_months_indep(C, n))
    jm = jdn_date(M)
    gok = cls == "B" and not (exc and safety)
    gi = 0 if jm <= jd else (1 if gok and jm <= jd + G else 2)
    assert gi == g, "calibration independent check failed"
    flags = ["wrong_unit", "off_by_one", "forgot_grace"] + (["misapplied_grace"] if (exc and safety and cls == "B") else [])
    var = [(f, status((f,))) for f in flags]
    if all(v == g for _, v in var):
        raise Retry()
    labels = ["Release lot - gauge was in calibration", "Release with deviation record (grace-period use)", "Quarantine lot - gauge overdue for calibration"]
    rules = ["Every gauge has a calibration interval of %d %s. The due date is the last calibration date plus the interval%s." % (
        n, unit, " (same day-of-month; last day of the month where that day does not exist)" if unit == "months" else ""),
        "A gauge may be used up to and including its due date.",
        "Class B gauges may be used for up to %d days after the due date, provided a deviation record is raised." % G,
        "Measurements taken with an overdue gauge that is not covered by the grace period make the lot nonconforming: quarantine it."]
    if exc:
        rules.append("The grace period is not available when the gauge is used to accept safety-critical lots.")
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["manufacturing"]))
    facts = [("Gauge", cid), ("Gauge class", cls), ("Last calibrated", F.d(C)), ("Used to measure", lot),
             ("Measurement date", F.d(M)), ("Lot classification", "Safety-critical" if safety else "Standard")]
    q = "What should happen to %s, measured with gauge %s?" % (lot, cid)
    k1 = label_kind(q, "Is \"{opt}\" the correct disposition of %s?" % lot, labels, g, var)
    k2 = value_kind("date", "What is the calibration due date of gauge %s?" % cid, "Is {opt} the calibration due date of gauge %s?" % cid,
                    Dd, [("wrong_unit", due(("wrong_unit",)))], F.od, [("off_by_one", Dd - ONE), ("off_by_one", Dd + ONE)])
    yn = [("Can %s be released (with or without a deviation record)?" % lot, int(g != 2)), ("Was gauge %s within its calibration interval on the measurement date?" % cid, int(g == 0))]
    R = {"wrong_unit": "the interval works out to %s" % F.d(due(("wrong_unit",))),
         "off_by_one": "a gauge is overdue on its due date", "forgot_grace": "anything after the due date is overdue",
         "misapplied_grace": "it's a Class B gauge so the 7-day grace applies"}
    notes = [(f, note_text(rng, R[f], labels[v])) for f, v in var if v != g]
    traps = ["grace_period"] + (["exception_to_exception"] if exc and safety and cls == "B" else []) + (["month_length"] if unit == "months" else []) + \
        (["boundary"] if (M - Dd).days in (-1, 0, 1, G, G + 1) else [])
    return mk_scn(tpl="adherence.calibration", domain="manufacturing", org=org, F=F, title="%s - Calibration Control Procedure QP-07" % org,
                  head="Calibration status and use of gauges", rules=rules, facts=facts, kinds=[k1, k2], yn=yn, notes=notes,
                  traps=traps, cid=cid, subject="Disposition of %s" % lot, sender=pick(rng, PEOPLE), checked=True)


def gen_adh_refill(rng, size, F):
    org = pick(rng, ["Crestview Pharmacy Services", "Arbor Community Pharmacy", "Meridian Health Plan"])
    name = pick(rng, PEOPLE)
    cid = "RX-%d" % rng.randint(100000, 999999)
    DS = pick(rng, [28, 30, 60, 90, 45])
    ctl = rng.random() < 0.4
    std_p, ctl_p = pick(rng, [(75, 90), (80, 90), (75, 85)])
    P = ctl_p if ctl else std_p
    FD = rand_date(rng)
    pick_up = FD + ONE * rng.randint(1, 5)

    def earliest(fl=()):
        pp = P
        if "wrong_percentage" in fl:
            pp = std_p if ctl else ctl_p
        x = Fraction(DS * pp, 100)
        dd = math.floor(x) if "rounded_down" in fl else math.ceil(x)
        base = pick_up if "used_pickup_date" in fl else FD
        return base + ONE * (dd - (1 if "fill_day_as_day1" in fl else 0))
    g = earliest()
    num = DS * P
    days_i = num // 100 + (1 if num % 100 else 0)
    assert jdn_to_date(jdn_date(FD) + days_i) == g, "refill independent check failed"
    flags = ["rounded_down", "fill_day_as_day1", "wrong_percentage", "used_pickup_date"]
    var = [(f, earliest((f,))) for f in flags]
    rules = ["A refill may be dispensed once at least %d%% of the days' supply of the previous fill has elapsed (%d%% for controlled substances)." % (std_p, ctl_p),
             "Days elapsed are counted from the date the previous prescription was filled (that date is day 0), not the date it was collected.",
             "Where the percentage gives a fraction of a day, round up to the next whole day."]
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["healthcare"]))
    drug = pick(rng, ["oxycodone 5 mg" if ctl else "lisinopril 10 mg", "zolpidem 10 mg" if ctl else "metformin 500 mg",
                      "methylphenidate 18 mg" if ctl else "atorvastatin 20 mg"])
    facts = [("Patient", name), ("Prescription", cid), ("Drug", "%s (%s)" % (drug, "controlled substance" if ctl else "not controlled")),
             ("Previous fill date", F.d(FD)), ("Collected by patient", F.d(pick_up)), ("Days' supply", str(DS))]
    q = "What is the earliest date on which prescription %s can be refilled?" % cid
    k1 = value_kind("date", q, "Is {opt} the earliest date on which prescription %s can be refilled?" % cid, g, var, F.od, [("off_by_one", g + ONE)])
    X = g + ONE * pick(rng, [-1, 0, 0, 1])
    yn = [("The patient asks for the refill of %s on %s. Can it be dispensed that day?" % (cid, F.d(X)), int(X >= g))]
    R = {"rounded_down": "%d%% of %d days is %s days" % (P, DS, str(Fraction(DS * P, 100))),
         "fill_day_as_day1": "the fill date counts as day 1",
         "wrong_percentage": "the threshold is %d%%" % (std_p if ctl else ctl_p),
         "used_pickup_date": "the patient only collected it on %s" % F.d(pick_up)}
    notes = [(f, note_value(rng, R[f], F.d(v))) for f, v in var if v != g]
    traps = ["rounding", "surface_cue"] + (["exception"] if ctl else [])
    return mk_scn(tpl="adherence.refill", domain="healthcare", org=org, F=F, title="%s - Early Refill Policy" % org,
                  head="Refill timing", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="Refill request %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_adh_slot(rng, size, F):
    org = pick(rng, ["Northgate Logistics", "Bluefin Freight", "Orchard & Pine Distribution Centre"])
    cid = "BKG-%d" % rng.randint(10000, 99999)
    carrier = pick(rng, ["Haulwise", "RapidRoute", "TransCo", "Linehaul 24"])
    d = rand_date(rng)
    sh = rng.randint(5, 18)
    L = pick(rng, [60, 120])
    E_, Lt = pick(rng, [(15, 30), (10, 45), (20, 60)])
    S = sh * 60
    En = S + L
    tgt = pick(rng, [S - E_, En, En + Lt]) + pick(rng, [-5, -1, 0, 0, 1, 5])
    if rng.random() < 0.2:
        tgt = S + 5 * rng.randint(-12, 36)
    A = tgt
    dock = A + 5 * rng.randint(3, 12)

    def band(a, fl=()):
        early = a < S - E_ if "boundary_flip" not in fl else a <= S - E_
        if early:
            return 0
        endref = S if "measured_from_slot_start" in fl else En
        if (a <= endref) if "boundary_flip" not in fl else (a < endref):
            return 1
        if (a <= endref + Lt) if "boundary_flip" not in fl else (a < endref + Lt):
            return 2
        return 3
    g = band(A)
    ai = A
    gi = 0 if ai < S - E_ else 1 if ai <= S + L else 2 if ai <= S + L + Lt else 3
    assert gi == g, "slot independent check failed"
    var = [("used_dock_time", band(dock)), ("measured_from_slot_start", band(A, ("measured_from_slot_start",))),
           ("boundary_flip", band(A, ("boundary_flip",)))]
    if all(v == g for _, v in var):
        raise Retry()
    labels = ordinal_labels(["Early - hold in the waiting area until the slot opens", "On time - unload",
                             "Late - unload and charge the late-arrival fee", "Missed slot - refuse and rebook"])
    rules = ["Arrival time is the time the vehicle checks in at the gatehouse; the time the dock door opens is not relevant.",
             "Vehicles arriving up to %d minutes before the start of the booked slot are treated as on time; earlier arrivals are early." % E_,
             "Vehicles arriving after the end of the booked slot but no more than %d minutes after it are unloaded with a late-arrival fee." % Lt,
             "Vehicles arriving more than %d minutes after the end of the booked slot have missed the slot and must rebook." % Lt]
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["logistics"]))

    def tm(x):
        return F.t(*divmod(x % 1440, 60))
    facts = [("Booking", cid), ("Carrier", carrier), ("Date", F.d(d)), ("Booked slot", "%s-%s" % (tm(S), tm(En))),
             ("Gatehouse check-in", tm(A)), ("Dock door opened", tm(dock)), ("Pallets", str(rng.randint(4, 33)))]
    q = "How should the arrival for booking %s be handled?" % cid
    k1 = label_kind(q, "Should booking %s be handled as \"{opt}\"?" % cid, labels, g, var)
    yn = [("Should a late-arrival fee be charged for booking %s?" % cid, int(g == 2)), ("Can booking %s be unloaded on this visit?" % cid, int(g in (1, 2)))]
    R = {"used_dock_time": "the dock door log shows %s" % tm(dock), "measured_from_slot_start": "lateness counts from the start of the slot",
         "boundary_flip": "the boundary minute goes the other way"}
    notes = [(f, note_text(rng, R[f], labels[v])) for f, v in var if v != g]
    traps = ["surface_cue"] + (["boundary"] if min(abs(A - (S - E_)), abs(A - En), abs(A - En - Lt)) <= 1 else [])
    return mk_scn(tpl="adherence.delivery_slot", domain="logistics", org=org, F=F, title="%s - Inbound Booking Rules" % org,
                  head="Slot adherence", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="Gatehouse query - %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_adherence(rng, size, F):
    return dispatch(rng, size, F, [gen_adh_flight, gen_adh_vaccine, gen_adh_calibration, gen_adh_refill, gen_adh_slot])



# ============================================================ S8  age / tenure thresholds
def bday_in_year(b, y, feb29="mar1"):
    if b.month == 2 and b.day == 29 and not calendar.isleap(y):
        return dt.date(y, 3, 1) if feb29 == "mar1" else dt.date(y, 2, 28)
    return dt.date(y, b.month, b.day)


def age_on(b, d, feb29="mar1"):
    a = d.year - b.year
    if d < bday_in_year(b, d.year, feb29):
        a -= 1
    return a


def age_on_indep(b, d, feb29="mar1"):
    k, jd = 0, jdn_date(d)
    while True:
        y = b.year + k + 1
        if b.month == 2 and b.day == 29 and not is_leap(y):
            mm, dd = (3, 1) if feb29 == "mar1" else (2, 28)
        else:
            mm, dd = b.month, b.day
        if jdn(y, mm, dd) <= jd:
            k += 1
        else:
            return k


FEB29_TXT = {"mar1": "A person born on 29 February is treated as having their birthday on 1 March in years that are not leap years.",
             "feb28": "A person born on 29 February is treated as having their birthday on 28 February in years that are not leap years."}


def rand_birth(rng, near, years, spread=(-2, -1, 0, 0, 1, 2)):
    y = near.year - years
    try:
        b = dt.date(y, near.month, near.day)
    except ValueError:
        b = dt.date(y, 2, 28)
    b = b + ONE * pick(rng, list(spread))
    if rng.random() < 0.08:
        ly = y - (y % 4)
        if not is_leap(ly):
            ly -= 4
        b = dt.date(ly, 2, 29)
    return b


def gen_age_school(rng, size, F):
    org = pick(rng, ["Cedar Valley School District", "Harlow District Council - School Admissions", "Eastmoor Unified Schools"])
    name = pick(rng, PEOPLE).split()[0] + " " + pick(rng, PEOPLE).split()[-1]
    cid = "ADM-%d" % rng.randint(10000, 99999)
    A = pick(rng, [4, 5, 6])
    cutoffs = [(9, 1), (8, 31), (12, 31), (10, 1), (9, 30)]
    cn = pick(rng, cutoffs)
    ver = size != "short" and rng.random() < 0.45
    co = pick(rng, [c for c in cutoffs if c != cn]) if ver else cn
    Y0 = rng.randint(2026, 2029)
    Yv = Y0 + pick(rng, [0, 1]) if ver else 0
    feb29 = pick(rng, ["mar1", "feb28"])

    def cutoff(Y, fl=()):
        c = cn
        if ver:
            use_new = Y >= Yv
            if "wrong_version" in fl:
                use_new = not use_new
            c = cn if use_new else co
        return dt.date(Y, c[0], c[1])
    B = rand_birth(rng, cutoff(Y0), A)

    def first_year(fl=()):
        if "used_birth_year" in fl:
            return B.year + A
        for Y in range(B.year + A - 1, B.year + A + 3):
            c = cutoff(Y, fl)
            att = bday_in_year(B, B.year + A, feb29)
            ok = att < c if "strict_cutoff" in fl else att <= c
            if "feb29_other" in fl:
                att = bday_in_year(B, B.year + A, "feb28" if feb29 == "mar1" else "mar1")
                ok = att <= c
            if ok:
                return Y
        return B.year + A + 3
    g = first_year()
    for Y in range(B.year + A - 1, B.year + A + 3):
        if age_on_indep(B, cutoff(Y), feb29) >= A:
            gi = Y
            break
    assert gi == g, "school independent check failed"
    flags = ["strict_cutoff", "used_birth_year"] + (["wrong_version"] if ver else []) + (["feb29_other"] if (B.month, B.day) == (2, 29) else [])
    var = [(f, first_year((f,))) for f in flags]
    if all(v == g for _, v in var):
        raise Retry()

    def sy(Y):
        return "%d-%02d" % (Y, (Y + 1) % 100)
    cm = lambda c: "%d %s" % (c[1], MONTHS[c[0] - 1])
    rules = ["A child may start in the first year of school in the school year beginning in September of year Y if the child has reached the age of %d on or before %s of year Y." % (A, cm(cn))]
    if ver:
        rules.append("This cut-off applies to school years beginning in %d or later. For school years beginning before %d the cut-off date was %s." % (Yv, Yv, cm(co)))
    if (B.month, B.day) == (2, 29) or rng.random() < 0.3:
        rules.append(FEB29_TXT[feb29])
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["education"]))
    facts = [("Application", cid), ("Child", name), ("Date of birth", F.d(B)),
             ("Year of application", str(B.year + A - 1)), ("Preferred school", pick(rng, PLACES) + " Primary")]
    q = "In which school year can %s first start school?" % name
    k1 = value_kind("label", q, "Is {opt} the first school year in which %s can start school?" % name, g, var, sy,
                    [("off_by_one", g + 1), ("off_by_one", g - 1)])
    yn = [("Can %s start school in %s?" % (name, sy(g - 1 if rng.random() < 0.5 else g)), None)]
    yq = yn[0][0]
    yn = [(yq, int(sy(g) in yq))]
    R = {"strict_cutoff": "the child has to be %d before the cut-off date" % A, "used_birth_year": "born in %d means starting in %d" % (B.year, B.year + A),
         "wrong_version": "the other cut-off date is the one that applies", "feb29_other": "a 29 February birthday counts on the other day in common years"}
    notes = [(f, note_value(rng, R[f], sy(v))) for f, v in var if v != g]
    traps = ["age_threshold", "boundary"] + (["superseded_rule"] if ver else []) + (["leap_day"] if (B.month, B.day) == (2, 29) else [])
    return mk_scn(tpl="age.school_entry", domain="education", org=org, F=F, title="%s - Admission Arrangements" % org,
                  head="Age of admission", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="School start year for %s" % name, sender=pick(rng, PEOPLE), checked=True)


def gen_age_fare(rng, size, F):
    org = pick(rng, ["Coastal Rail Express", "Metroline Transit", "Brightline Telecom", "Lumen Outfitters"])
    tele = "Telecom" in org
    shop = "Outfitters" in org
    name = pick(rng, PEOPLE)
    cid = "BK-%d" % rng.randint(100000, 999999)
    D_ = rand_date(rng)
    tgt = pick(rng, [16, 26, 65, 16, 26, 65])
    B = rand_birth(rng, D_, tgt, (-1, 0, 0, 1))
    P = D_ - ONE * rng.randint(3, 40)
    feb29 = "mar1"

    def cat(fl=()):
        ref = P if "used_booking_date" in fl else D_
        if "calendar_year_age" in fl:
            a = ref.year - B.year
        else:
            a = age_on(B, ref, feb29)
            if "birthday_not_counted" in fl and ref == bday_in_year(B, ref.year, feb29):
                a -= 1
        if a < 16:
            return 0
        if a <= 25:
            return 1
        if a < 65:
            return 2
        return 3
    g = cat()
    ai = age_on_indep(B, D_, feb29)
    assert (0 if ai < 16 else 1 if ai <= 25 else 2 if ai < 65 else 3) == g, "fare independent check failed"
    flags = ["used_booking_date", "calendar_year_age", "birthday_not_counted"]
    var = [(f, cat((f,))) for f in flags]
    if all(v == g for _, v in var):
        raise Retry()
    what, when = ("plan", "on the date the plan starts") if tele else (("discount", "on the date of purchase") if shop else ("fare", "on the date of travel"))
    labels = ["Child %s" % what, "Youth %s" % what, "Standard adult %s" % what, "Senior %s" % what]
    rules = ["Age is taken %s, not on the date of booking or ordering." % when,
             "Child %s: under 16. Youth %s: 16 to 25 inclusive (a person is 25 until the day before their 26th birthday). Senior %s: 65 or over. Everyone else: standard adult %s." % (what, what, what, what),
             "A person attains a given age at the start of their birthday."]
    if (B.month, B.day) == (2, 29) or rng.random() < 0.2:
        rules.append(FEB29_TXT[feb29])
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["telecom" if tele else "retail" if shop else "travel"]))
    dkey = "Plan start date" if tele else ("Date of purchase" if shop else "Date of travel")
    facts = [("Booking", cid), ("Customer", name), ("Date of birth", F.d(B)), ("Booked on", F.d(P)), (dkey, F.d(D_))]
    q = "Which %s category applies to booking %s?" % (what, cid)
    k1 = label_kind(q, "Does the \"{opt}\" category apply to booking %s?" % cid, labels, g, var)
    yn = [("Is %s eligible for the %s on booking %s?" % (name, labels[g if rng.random() < 0.5 else (g + 1) % 4].lower(), cid), None)]
    yq = yn[0][0]
    yn = [(yq, int(labels[g].lower() in yq))]
    R = {"used_booking_date": "on the booking date %s the customer was %d" % (F.d(P), age_on(B, P, feb29)),
         "calendar_year_age": "%d minus %d gives the age" % (D_.year, B.year), "birthday_not_counted": "the birthday itself doesn't count yet"}
    notes = [(f, note_text(rng, R[f], labels[v])) for f, v in var if v != g]
    traps = ["age_threshold", "surface_cue"] + (["boundary"] if abs((D_ - bday_in_year(B, D_.year, feb29)).days) <= 1 else [])
    dom = "telecom" if tele else ("retail" if shop else "travel")
    return mk_scn(tpl="age.fare_category", domain=dom, org=org, F=F, title="%s - Age-Based Pricing Conditions" % org,
                  head="Age categories", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="Category check %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_age_dependent(rng, size, F):
    org = pick(rng, ["Meridian Health Plan", "Crestview Health Partners", "Harborview Mutual"])
    name = pick(rng, PEOPLE)
    cid = "MBR-%d" % rng.randint(100000, 999999)
    A = pick(rng, [26, 26, 25, 23])
    feb29 = pick(rng, ["mar1", "feb28"])
    tb = rand_date(rng)
    B = rand_birth(rng, tb, A, (0,))
    turn = bday_in_year(B, B.year + A, feb29)
    end = last_of_month(turn.year, turn.month)

    def lastday(fl=()):
        if "ended_at_birthday" in fl:
            return turn - ONE
        if "ended_end_of_year" in fl:
            return dt.date(turn.year, 12, 31)
        if "ended_month_before" in fl:
            return turn.replace(day=1) - ONE
        return end
    g = lastday()
    iy, im = jdn_to_ymd(jdn(turn.year, turn.month, 1) + 40)[:2]
    assert jdn_to_date(jdn(iy, im, 1) - 1) == g and age_on_indep(B, turn, feb29) == A, "dependant independent check failed"
    X = pick(rng, [g, g + ONE, turn, turn - ONE, g - ONE * rng.randint(1, 10), g + ONE * rng.randint(2, 20)])
    flags = ["ended_at_birthday", "ended_end_of_year", "ended_month_before"]
    var = [(f, lastday((f,))) for f in flags]
    labels = ["Covered as a dependant", "Not covered - dependant eligibility has ended"]
    gl = 0 if X <= g else 1
    lvar = [(f, 0 if X <= v else 1) for f, v in var]
    rules = ["A child of the member is covered as a dependant until the end of the calendar month in which the child reaches age %d." % A,
             "Cover ends at midnight on the last day of that month; claims are assessed by the date of service."]
    if (B.month, B.day) == (2, 29) or rng.random() < 0.3:
        rules.append(FEB29_TXT[feb29])
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["healthcare"]))
    facts = [("Member", cid), ("Dependant", name), ("Dependant date of birth", F.d(B)), ("Date of service", F.d(X)),
             ("Claim amount", money(rng.randint(40, 3000)))]
    k1 = label_kind("Is the claim for %s's service on %s covered?" % (name, F.d(X)), "Is \"{opt}\" the correct outcome for %s's claim?" % name, labels, gl, lvar)
    k2 = value_kind("date", "What is the last day on which %s is covered as a dependant under member %s?" % (name, cid),
                    "Is {opt} the last day of %s's dependant cover?" % name, g, var, F.od, [("off_by_one", g + ONE)])
    yn = [("Is %s still covered as a dependant on %s?" % (name, F.d(X)), int(X <= g))]
    R = {"ended_at_birthday": "cover stops when the child turns %d" % A, "ended_end_of_year": "cover runs to the end of that year",
         "ended_month_before": "cover stops at the end of the month before the birthday"}
    notes = [(f, note_value(rng, R[f], F.d(v))) for f, v in var if v != g]
    traps = ["age_threshold", "end_of_month"] + (["leap_day"] if (B.month, B.day) == (2, 29) else []) + (["boundary"] if abs((X - g).days) <= 1 else [])
    return mk_scn(tpl="age.dependant_cover", domain="insurance", org=org, F=F, title="%s - Member Handbook, Eligibility" % org,
                  head="Dependant eligibility", rules=rules, facts=facts, kinds=[k1, k2], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="Dependant eligibility query %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def completed_years(a, b):
    """completed anniversaries of a on or before b (anniversary of 29 Feb falls on 1 Mar)."""
    return max(0, age_on(a, b, "mar1"))


def gen_age_vesting(rng, size, F):
    org = pick(rng, ["Castellan Foods Ltd", "Norvale Engineering", "Alder Street Bank", "Quanta Analytics"])
    name = pick(rng, PEOPLE)
    cid = "EMP-%d" % rng.randint(10000, 99999)
    sched = pick(rng, [[(2, 20), (3, 40), (4, 60), (5, 80), (6, 100)], [(1, 25), (2, 50), (3, 75), (4, 100)], [(3, 100)]])
    H = rand_date(rng, 2016, 2022)
    ny = pick(rng, [t for t, _ in sched] + [2, 3])
    T = bday_in_year(H, H.year + ny, "mar1") + ONE * pick(rng, [-1, 0, 0, 1, 40, -60])
    brk = size != "short" and rng.random() < 0.45
    H1 = T1 = None
    mil = False
    gap_long = False
    if brk:
        H1 = H - ONE * rng.randint(900, 2200)
        gap = pick(rng, [200, 330, 364, 365, 366, 420, 600])
        T1 = H - ONE * gap
        if T1 <= H1 + ONE * 200:
            H1 = T1 - ONE * rng.randint(400, 1500)
        gap_long = add_months(T1, 12) < H
        if add_months(T1, 12) == H:
            raise Retry()
        mil = gap_long and rng.random() < 0.5

    def years(fl=()):
        if "calendar_year_diff" in fl:
            y = T.year - H.year
        elif "rounded_up" in fl:
            y = completed_years(H, T) + (0 if bday_in_year(H, T.year, "mar1") == T else 1)
        else:
            y = completed_years(H, T)
        if brk:
            inc = (not gap_long) or mil
            if "misapplied_break_rule" in fl:
                inc = not inc
            if inc:
                if "combined_partial_years" in fl:
                    return ((T - H).days + (T1 - H1).days) // 365
                y += completed_years(H1, T1)
        return y

    def pct(y):
        v = 0
        for t, pc in sched:
            if y >= t:
                v = pc
        return v
    levels = [0] + [pc for _, pc in sched]
    g = levels.index(pct(years()))
    yi = age_on_indep(H, T)
    if brk and ((jdn_date(add_months_indep(T1, 12)) >= jdn_date(H)) or mil):
        yi += age_on_indep(H1, T1)
    assert levels.index(pct(yi)) == g, "vesting independent check failed"
    flags = ["calendar_year_diff", "rounded_up"] + (["misapplied_break_rule", "combined_partial_years"] if brk else [])
    var = [(f, levels.index(pct(years((f,))))) for f in flags]
    if all(v == g for _, v in var):
        raise Retry()
    labels = ordinal_labels(["%d%% vested" % x for x in levels])
    rules = ["Vesting schedule (completed years of service -> vested %): " + ", ".join("%d -> %d%%" % (t, pc) for t, pc in sched) + "; fewer than %d -> 0%%." % sched[0][0],
             "A year of service is completed on each anniversary of the hire date while the employee is still employed; the anniversary date itself counts.",
             "Partial years are ignored."]
    if brk:
        rules.append("Service from an earlier period of employment counts only if the employee was rehired within 12 months of leaving; completed years from each period are added together, and partial years from different periods are never combined.")
        rules.append("A break caused by military service is disregarded, whatever its length.")
    if size != "short" and rng.random() < 0.4:
        rules.append(pick(rng, DOMAIN_FILLER["hr"]))
    facts = [("Employee", "%s (%s)" % (name, cid)), ("Hire date (current employment)", F.d(H)), ("Termination date", F.d(T))]
    if brk:
        facts += [("Earlier employment", "%s to %s" % (F.d(H1), F.d(T1))),
                  ("Reason for break", "Military service (reservist deployment)" if mil else pick(rng, ["Resigned to travel", "Career break", "Joined another employer"]))]
    facts.append(("Account balance", money(rng.randint(3000, 90000))))
    q = "What is %s's vested percentage at termination?" % name
    k1 = label_kind(q, "Is %s \"{opt}\" at termination?" % name, labels, g, var)
    yn = [("Is %s fully vested at termination?" % name, int(levels[g] == 100)), ("Is %s vested in any part of the account?" % name, int(levels[g] > 0))]
    R = {"calendar_year_diff": "%d to %d is %d years" % (H.year, T.year, T.year - H.year), "rounded_up": "a part year counts as a year",
         "misapplied_break_rule": "the earlier service should be treated the other way", "combined_partial_years": "adding the days from both periods together gives more full years"}
    notes = [(f, note_text(rng, R[f], labels[v])) for f, v in var if v != g]
    traps = ["tenure_threshold"] + (["exception_to_exception"] if brk and mil else []) + (["boundary"] if abs((T - bday_in_year(H, T.year, "mar1")).days) <= 1 else [])
    return mk_scn(tpl="age.vesting", domain="hr", org=org, F=F, title="%s - Retirement Savings Plan, Vesting Rules" % org,
                  head="Vesting", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="Vesting at termination - %s" % name, sender=pick(rng, PEOPLE), checked=True)


def gen_age_pension(rng, size, F):
    org = pick(rng, ["Summit County Benefits Office", "National Pension Service of Ardmere", "Public Employees Retirement Board"])
    name = pick(rng, PEOPLE)
    cid = "PEN-%d" % rng.randint(100000, 999999)
    Ny, Nm = 66, pick(rng, [0, 2, 4, 6, 8, 10])
    by = rng.randint(1958, 1962)
    bm = rng.randint(1, 12)
    bd = pick(rng, [1, 1, 2, 2, 15, 28, 30, 31])
    bd = min(bd, dim(by, bm))
    B = dt.date(by, bm, bd)
    dbr = rng.random() < 0.7

    def start(fl=()):
        mm = Nm if "ignored_months" not in fl else 0
        anniv = add_months(B, 12 * Ny + mm)
        att = anniv - ONE if (dbr and "ignored_day_before_rule" not in fl) else anniv
        if "paid_same_month" in fl:
            return att.replace(day=1)
        nx = add_months(att.replace(day=1), 1)
        return nx
    g = start()
    an_i = add_months_indep(B, 12 * Ny + Nm)
    att_i = jdn_to_date(jdn_date(an_i) - 1) if dbr else an_i
    idx = att_i.year * 12 + att_i.month
    assert dt.date(idx // 12, idx % 12 + 1, 1) == g, "pension independent check failed"
    flags = ["ignored_months", "paid_same_month"] + (["ignored_day_before_rule"] if dbr else [])
    var = [(f, start((f,))) for f in flags]
    rules = ["Full retirement age for claimants born in %d is %d years%s." % (by, Ny, (" and %d months" % Nm) if Nm else ""),
             "Benefits are payable from the first day of the month following the month in which the claimant attains full retirement age."]
    if dbr:
        rules.insert(1, "For the purposes of this scheme a person attains an age on the day before the anniversary of their birth.")
    else:
        rules.insert(1, "A person attains an age on the anniversary of their birth.")
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["benefits"]))
    facts = [("Claim", cid), ("Claimant", name), ("Date of birth", F.d(B)), ("Claim filed", F.d(g - ONE * rng.randint(20, 200))),
             ("National insurance record", "%d qualifying years" % rng.randint(30, 45))]
    fm = lambda d: "%s %d" % (MONTHS[d.month - 1], d.year)
    q = "From which month is %s's retirement benefit first payable?" % name
    k1 = value_kind("month", q, "Is %s's retirement benefit first payable from {opt}?" % name, g, var, fm,
                    [("off_by_one", add_months(g, 1)), ("off_by_one", add_months(g, -1))])
    yn = [("Is %s's benefit payable for %s?" % (name, fm(add_months(g, pick(rng, [-1, 0])))), None)]
    yq = yn[0][0]
    yn = [(yq, int(fm(g) in yq))]
    R = {"ignored_months": "the pension age is %d" % Ny, "paid_same_month": "payment starts in the month the age is reached",
         "ignored_day_before_rule": "the birthday is when the age is reached"}
    notes = [(f, note_value(rng, R[f], fm(v))) for f, v in var if v != g]
    traps = ["age_threshold", "months_arithmetic"] + (["legal_fiction"] if dbr else []) + (["boundary"] if bd <= 2 else [])
    return mk_scn(tpl="age.pension_start", domain="benefits", org=org, F=F, title="%s - State Pension Guide" % org,
                  head="When benefits start", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="Pension start month for %s" % name, sender=pick(rng, PEOPLE), checked=True)


def gen_age(rng, size, F):
    return dispatch(rng, size, F, [gen_age_school, gen_age_fare, gen_age_dependent, gen_age_vesting, gen_age_pension])


# ============================================================ S9  grace periods and late fees
def gen_grace_rent(rng, size, F):
    org = pick(rng, ["Eastmoor Housing Association", "Crane & Lowe Property Services", "Riverside Lettings"])
    name = pick(rng, PEOPLE)
    cid = "TEN-%d" % rng.randint(1000, 9999)
    y, m = rng.randint(2025, 2028), rng.randint(1, 12)
    Gd = pick(rng, [3, 5, 5, 7])
    F0, F1, Cap = pick(rng, [(50, 10, 150), (35, 5, 100), (25, 15, 125), (40, 10, 100)])
    roll = rng.random() < 0.5
    hols = make_holidays(rng, [], dt.date(y, m, 1), dt.date(y, m, 1) + ONE * 30, n_extra=rng.randint(0, 2))
    if roll and rng.random() < 0.4 and dt.date(y, m, Gd).weekday() < 5:
        hols = sorted(set(hols + [dt.date(y, m, Gd)]))
    hs = frozenset(hols)
    GE = dt.date(y, m, Gd)
    GEr = roll_fwd(GE, hs) if roll else GE
    P = GEr + ONE * pick(rng, [-1, 0, 1, 1, 2, 5, 8, 12, 20])
    post = P - ONE * rng.randint(2, 6)

    def fee(fl=()):
        ge = GE if "ignored_rollover" in fl else GEr
        pd = post if "used_postmark" in fl else P
        if "fee_from_due_date" in fl:
            dl = (pd - dt.date(y, m, 1)).days
        else:
            dl = (pd - ge).days
        if "off_by_one" in fl:
            dl -= 1
        if dl <= 0:
            return 0
        f = F0 + F1 * dl
        return f if "forgot_cap" in fl else min(f, Cap)
    g = fee()
    hj = [jdn_date(h) for h in hols]
    jge = j_roll(jdn(y, m, Gd), hj) if roll else jdn(y, m, Gd)
    dli = jdn_date(P) - jge
    assert (0 if dli <= 0 else min(F0 + F1 * dli, Cap)) == g, "rent independent check failed"
    flags = ["used_postmark", "fee_from_due_date", "off_by_one", "forgot_cap"] + (["ignored_rollover"] if roll else [])
    var = [(f, fee((f,))) for f in flags]
    if sum(1 for _, v in var if v != g) < 2:
        raise Retry()
    rules = ["Rent is due on the 1st day of each month. Rent is paid when it is received by the landlord, not when it is posted.",
             "No late fee is charged if the rent is received on or before the %s of the month." % ordinal(Gd),
             "If rent is received later, a late fee of $%d is charged plus $%d for each day after the %s up to and including the day the rent is received, subject to a maximum total late fee of $%d." % (F0, F1, ordinal(Gd), Cap)]
    if roll:
        rules.append("If the %s falls on a Saturday, Sunday or public holiday, the fee-free period is extended to the next day that is not one of those; daily charges then run from that day. Public holidays: %s." % (
            ordinal(Gd), hol_text(rng, F, hols) if hols else "none this month"))
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["housing"]))
    facts = [("Tenancy", cid), ("Tenant", name), ("Rent due", F.d(dt.date(y, m, 1))), ("Cheque postmarked", F.d(post)),
             ("Payment received", F.d(P)), ("Monthly rent", money(rng.randint(8, 30) * 100))]
    q = "What late fee, if any, should be charged to tenancy %s for this month?" % cid
    fm = lambda v: money(v) if v else "No late fee ($0.00)"
    k1 = value_kind("amount", q, "Is {opt} the correct late fee for tenancy %s this month?" % cid, g, var, fm)
    yn = [("Should any late fee be charged to tenancy %s this month?" % cid, int(g > 0))]
    R = {"used_postmark": "the cheque was posted on %s" % F.d(post), "fee_from_due_date": "daily charges run from the due date on the 1st",
         "off_by_one": "the day the rent arrives isn't charged", "forgot_cap": "the fee just keeps adding up", "ignored_rollover": "the fee-free period ended on the %s" % ordinal(Gd)}
    notes = [(f, note_value(rng, R[f], fm(v))) for f, v in var if v != g]
    traps = ["grace_period", "surface_cue"] + (["holiday_rollover"] if roll and GEr != GE else [])
    return mk_scn(tpl="grace.rent_late_fee", domain="housing", org=org, F=F, title="%s - Tenancy Agreement, Clause 4" % org,
                  head="Payment of rent", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="Late fee for %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_grace_premium(rng, size, F):
    org = pick(rng, ["Harborview Mutual", "Bluestone Assurance", "Kestrel Life"])
    name = pick(rng, PEOPLE)
    cid = "POL-%d" % rng.randint(100000, 999999)
    Dd = rand_date(rng)
    G = pick(rng, [30, 31])
    Rn = pick(rng, [0, 60, 90]) if size != "short" else 0
    CL = Dd + ONE * pick(rng, [-3, 5, G - 1, G, G + 1, G + 10, G + 40])
    pk = pick(rng, ["none", "in_grace", "at_edge", "after_edge", "reinstated"])
    if pk == "none":
        P = None
    elif pk == "in_grace":
        P = Dd + ONE * rng.randint(1, G - 1)
    elif pk == "at_edge":
        P = Dd + ONE * G
    elif pk == "after_edge":
        P = Dd + ONE * (G + 1)
    else:
        P = Dd + ONE * (G + rng.randint(2, max(3, Rn or 30)))

    def outcome(fl=()):
        GG = G - 1 if "grace_off_by_one" in fl else G
        if CL < Dd:
            return 0
        paid = P is not None and P <= Dd + ONE * GG
        if paid:
            return 0
        if CL <= Dd + ONE * GG:
            return 0 if "forgot_deduction" in fl else 1
        if Rn and P is not None and Dd + ONE * GG < P <= Dd + ONE * (GG + Rn):
            if "ignored_reinstatement" in fl:
                return 2
            if CL >= P or "reinstatement_backdated" in fl:
                return 0
        return 2
    g = outcome()
    jD, jC = jdn_date(Dd), jdn_date(CL)
    jP = jdn_date(P) if P else None
    if jC < jD or (jP is not None and jP - jD <= G):
        gi = 0
    elif jC - jD <= G:
        gi = 1
    elif Rn and jP is not None and G < jP - jD <= G + Rn and jC >= jP:
        gi = 0
    else:
        gi = 2
    assert gi == g, "premium independent check failed"
    flags = ["grace_off_by_one", "forgot_deduction"] + (["ignored_reinstatement", "reinstatement_backdated"] if Rn else [])
    var = [(f, outcome((f,))) for f in flags]
    if all(v == g for _, v in var):
        raise Retry()
    labels = ["Pay the claim in full", "Pay the claim less the overdue premium", "Decline - the policy had lapsed"]
    rules = ["Each annual premium is due on the renewal date. A grace period runs until the end of the %s day after the due date." % ordinal(G),
             "If the premium is received within the grace period, cover continues without interruption.",
             "If a loss occurs during the grace period and the premium has not been received by the end of the grace period, the claim is paid less the overdue premium.",
             "If the premium is not received by the end of the grace period, the policy lapses with effect from the due date."]
    if Rn:
        rules.append("A lapsed policy is reinstated if the overdue premium is received within %d days after the end of the grace period. Reinstatement restores cover only from the date the premium is received; losses between the end of the grace period and that date are not covered." % Rn)
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["insurance"]))
    facts = [("Policy", cid), ("Policyholder", name), ("Premium due date", F.d(Dd)),
             ("Premium received", F.d(P) if P else "Not received"), ("Date of loss", F.d(CL)),
             ("Annual premium", money(rng.randint(3, 30) * 100))]
    q = "How should the claim under policy %s be settled?" % cid
    k1 = label_kind(q, "Should the claim under policy %s be settled as \"{opt}\"?" % cid, labels, g, var)
    yn = [("Is the loss under policy %s covered (in full or in part)?" % cid, int(g != 2))]
    R = {"grace_off_by_one": "a %d-day grace period ends on day %d after the due date minus one" % (G, G), "forgot_deduction": "cover continued through the grace period",
         "ignored_reinstatement": "once the policy lapses, that's it", "reinstatement_backdated": "reinstatement puts the policy back as if it never lapsed"}
    notes = [(f, note_text(rng, R[f], labels[v])) for f, v in var if v != g]
    traps = ["grace_period"] + (["exception_to_exception"] if Rn else []) + (["boundary"] if (CL - Dd).days in (G, G + 1) or (P and (P - Dd).days in (G, G + 1)) else [])
    return mk_scn(tpl="grace.premium", domain="insurance", org=org, F=F, title="%s - Policy Conditions" % org,
                  head="Premiums, grace period and lapse", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps,
                  cid=cid, subject="Claim settlement under %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_grace_card(rng, size, F):
    org = pick(rng, ["Alder Street Bank", "Northfield Credit Union", "Crescent Card Services"])
    name = pick(rng, PEOPLE)
    cid = "CARD-%04d" % rng.randint(0, 9999)
    ob = pick(rng, [-300, -240, 0, 60])
    oc = pick(rng, [o for o in OFFSETS if abs(o - ob) >= 180])
    Dd = rand_date(rng)
    hols = make_holidays(rng, [d for d in [Dd] if d.weekday() < 5 and rng.random() < 0.3], Dd - ONE * 20, Dd + ONE * 20, n_extra=1)
    hs = frozenset(hols)
    ED = roll_fwd(Dd, hs)
    tb = 17 * 60 + pick(rng, [-30, -1, 0, 0, 1, 20, 90])
    day = ED + ONE * pick(rng, [0, 0, 0, 1, -1])
    ub = utc_of(day, tb // 60, tb % 60, ob)
    cd, ch, cmn = local_of(ub, oc)
    k_prev = pick(rng, [None, 3, 5, 6, 7, 9])
    prev = add_months(Dd, -k_prev) if k_prev else None

    def late(dday, tmin, fl=()):
        ed = Dd if "ignored_rollover" in fl else ED
        if dday < ed:
            return False
        if dday > ed:
            return True
        return tmin > 17 * 60 if "boundary_exclusive" not in fl else tmin >= 17 * 60

    def outcome(fl=()):
        if "tz_ignored" in fl:
            L = late(cd, ch * 60 + cmn, fl)
        elif "tz_sign_flip" in fl:
            x = naive_min(cd, ch, cmn) + oc + ob
            L = late(jdn_to_date(x // 1440), x % 1440, fl)
        else:
            L = late(day, tb, fl)
        if not L:
            return 0
        w = 7 if "repeat_window_off_by_one" in fl else 6
        return 2 if (k_prev is not None and k_prev <= w) else 1
    g = outcome()
    xm = j_umin(cd, ch, cmn, oc) + ob
    jd, tm = divmod(xm, 1440)
    jed = j_roll(jdn_date(Dd), [jdn_date(h) for h in hols])
    Li = jd > jed or (jd == jed and tm > 17 * 60)
    gi = 0 if not Li else (2 if (k_prev is not None and k_prev <= 6) else 1)
    assert gi == g, "card independent check failed"
    flags = ["tz_ignored", "tz_sign_flip", "ignored_rollover", "boundary_exclusive", "repeat_window_off_by_one"]
    var = [(f, outcome((f,))) for f in flags]
    if all(v == g for _, v in var):
        raise Retry()
    labels = ["No late fee", "Late fee $29", "Late fee $40 (repeat late payment)"]
    zone = "%s (%s)" % (pick(rng, PLACES), fofs(ob))
    rules = ["A payment is on time if it is received by 5:00 pm on the due date, %s time. Payments received after 5:00 pm are late." % zone,
             "If the due date falls on a Saturday, Sunday or bank holiday, a payment received by 5:00 pm on the next business day is on time. Bank holidays: %s." % hol_text(rng, F, hols),
             "The late fee is $29, or $40 if another payment was late in any of the previous six billing cycles (billing cycles are monthly)."]
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["banking"]))
    facts = [("Account", cid), ("Cardholder", name), ("Payment due date", F.d(Dd)),
             ("Payment made", "%s at %s, cardholder's local time (%s)" % (F.d(cd), F.t(ch, cmn), fofs(oc))),
             ("Previous late payment", ("statement due %s (%d billing cycles before this one)" % (F.d(prev), k_prev)) if prev else "none on record")]
    q = "What late fee applies to account %s for this statement?" % cid
    k1 = label_kind(q, "Is \"{opt}\" correct for account %s this statement?" % cid, labels, g, var)
    yn = [("Was the payment on account %s on time?" % cid, int(g == 0))]
    R = {"tz_ignored": "the cardholder paid at %s on %s" % (F.t(ch, cmn), F.d(cd)), "tz_sign_flip": "converting the cardholder's time to bank time gives that",
         "ignored_rollover": "the due date was %s, no extension" % F.d(Dd), "boundary_exclusive": "5:00 pm exactly is already late",
         "repeat_window_off_by_one": "the earlier late payment is still within the look-back"}
    notes = [(f, note_text(rng, R[f], labels[v])) for f, v in var if v != g]
    traps = ["timezone", "cutoff_time"] + (["holiday_rollover"] if ED != Dd else []) + (["boundary"] if abs(tb - 17 * 60) <= 1 or k_prev in (6, 7) else [])
    return mk_scn(tpl="grace.card_payment", domain="banking", org=org, F=F, title="%s - Credit Card Agreement, Section 9" % org,
                  head="Payments and late fees", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="Late fee dispute %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_grace_library(rng, size, F):
    org = pick(rng, ["Westbrook University Library", "Carroway College Learning Centre", "Oakhaven Public Library"])
    name = pick(rng, PEOPLE)
    cid = "LIB-%d" % rng.randint(10000, 99999)
    DU = rand_date(rng)
    g_ = pick(rng, [2, 3, 5])
    rate = pick(rng, [Fraction(1, 4), Fraction(1, 2), Fraction(1)])
    cap_ = pick(rng, [5, 10, 15])
    closed_rule = rng.random() < 0.35
    hols = make_holidays(rng, [], DU, DU + ONE * 40, n_extra=rng.randint(0, 2), wk=(6,)) if closed_rule else []
    hs = frozenset(hols)
    RT = DU + ONE * pick(rng, [g_ - 1, g_, g_ + 1, g_ + 2, 10, 25, 50])

    def days_late(fl=()):
        if closed_rule and "counted_closure_days" not in fl:
            return bdays_between(DU, RT, hs, (6,))
        return (RT - DU).days

    def fine(fl=()):
        dl = days_late(fl)
        if "off_by_one" in fl:
            dl += 1
        if dl <= g_ and "ignored_grace" not in fl:
            return Fraction(0)
        ch = dl - g_ if "counted_from_grace_end" in fl else dl
        f = rate * ch
        return f if "forgot_cap" in fl else min(f, Fraction(cap_))
    g = fine()
    if closed_rule:
        dli = j_count(jdn_date(DU), jdn_date(RT), [jdn_date(h) for h in hols], (6,))
    else:
        dli = jdn_date(RT) - jdn_date(DU)
    assert (Fraction(0) if dli <= g_ else min(rate * dli, Fraction(cap_))) == g, "library independent check failed"
    flags = ["off_by_one", "ignored_grace", "counted_from_grace_end", "forgot_cap"] + (["counted_closure_days"] if closed_rule else [])
    var = [(f, fine((f,))) for f in flags]
    if sum(1 for _, v in var if v != g) < 2:
        raise Retry()
    rules = ["Items are due back on the due date shown on the loan receipt.",
             "No fine is charged if an item is returned within %d days after the due date." % g_,
             "If an item is returned later than that, the fine is %s for every day after the due date, including the first %d days, up to a maximum of %s per item." % (money(rate), g_, money(cap_))]
    if closed_rule:
        rules.append("Days on which the library is closed are not counted. The library is closed on Sundays and on these holidays: %s." % (hol_text(rng, F, hols) if hols else "none in this period"))
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["education"]))
    facts = [("Borrower", "%s (%s)" % (name, cid)), ("Item", pick(rng, ["Principles of Econometrics", "Organic Chemistry, 3rd ed.", "A History of the Baltic", "DSLR camera kit"])),
             ("Due date", F.d(DU)), ("Returned", F.d(RT))]
    fm = lambda v: money(v) if v else "No fine ($0.00)"
    q = "What fine should %s be charged for this item?" % name
    k1 = value_kind("amount", q, "Is {opt} the correct fine for %s's item?" % name, g, var, fm)
    yn = [("Should %s be charged any fine for this item?" % name, int(g > 0))]
    R = {"off_by_one": "the due date itself counts as a late day", "ignored_grace": "anything after the due date is fined",
         "counted_from_grace_end": "the fine only runs after the %d fine-free days" % g_, "forgot_cap": "the fine is just rate times days",
         "counted_closure_days": "every calendar day counts"}
    notes = [(f, note_value(rng, R[f], fm(v))) for f, v in var if v != g]
    traps = ["grace_period"] + (["closure_days"] if closed_rule else []) + (["boundary"] if abs(days_late() - g_) <= 1 else [])
    return mk_scn(tpl="grace.library_fine", domain="education", org=org, F=F, title="%s - Loans and Fines" % org,
                  head="Overdue items", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="Fine query %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_grace(rng, size, F):
    return dispatch(rng, size, F, [gen_grace_rent, gen_grace_premium, gen_grace_card, gen_grace_library])


# ============================================================ S10  notice periods
def gen_notice_renewal(rng, size, F):
    org = pick(rng, ["Lumen Cloud", "Stratus Workspace", "Brightline Telecom", "Veritas Energy Retail"])
    cust = pick(rng, ["Ardent Dental Group", "Harrow & Finch Architects", "Blue Heron Cafes", "Mistral Robotics"])
    cid = "AGR-%d" % rng.randint(10000, 99999)
    N = pick(rng, [30, 60, 90])
    TE = rand_date(rng)
    RD = TE + ONE
    v = pick(rng, ["v1", "v2", "v3", "v4"])
    LND = {"v1": TE - ONE * N, "v2": RD - ONE * N, "v3": TE - ONE * N, "v4": TE - ONE * N}[v]
    deem = size != "short" and rng.random() < 0.6
    orc = pick(rng, [-300, 0, 60, 330])
    osn = pick(rng, [o for o in OFFSETS if abs(o - orc) >= 180]) if deem else orc
    hs = frozenset()
    target = LND + ONE * pick(rng, [-1, 0, 0, 1])
    rt = pick(rng, [16 * 60 + 30, 17 * 60, 17 * 60 + 5, 18 * 60 + 30, 10 * 60])
    ur = utc_of(target, rt // 60, rt % 60, orc)
    sd, sh, sm = local_of(ur, osn)

    def deemed(fl=()):
        if not deem or "ignored_deemed_receipt" in fl:
            if "tz_ignored" in fl or not deem:
                return sd if deem else target
            return target
        if "tz_ignored" in fl:
            d_, t_ = sd, sh * 60 + sm
        else:
            d_, t_ = target, rt
        if not is_bday(d_, hs) or t_ > 17 * 60:
            return next_bday_after(d_, hs)
        return d_

    def lnd(fl=()):
        if "off_by_one" in fl:
            return LND + ONE if v in ("v1", "v3", "v4") else LND - ONE
        return LND

    def outcome(fl=()):
        return 0 if deemed(fl) <= lnd(fl) else 1
    g = outcome()
    jl = jdn_date(TE) - N + (1 if v == "v2" else 0)
    xm = j_umin(sd, sh, sm, osn) + orc
    jd, tmin = divmod(xm, 1440)
    if deem and (jd % 7 >= 5 or tmin > 17 * 60):
        jd = j_next_b(jd, [], (5, 6))
    assert (0 if jd <= jl else 1) == g and jdn_to_date(jl) == LND, "renewal independent check failed"
    flags = ["off_by_one"] + (["ignored_deemed_receipt", "tz_ignored"] if deem else [])
    var = [(f, outcome((f,))) for f in flags]
    if all(x == g for _, x in var):
        raise Retry()
    labels = ["Agreement ends at the end of the current term", "Agreement renews automatically for a further term"]
    ntext = {"v1": "at least %d days before the last day of the current term" % N,
             "v2": "at least %d days before the renewal date (the day after the last day of the term)" % N,
             "v3": "not less than %d clear days before the renewal date (clear days exclude both the day the notice is received and the renewal date)" % N,
             "v4": "more than %d days before the renewal date (the day after the last day of the term)" % N}[v]
    rules = ["This agreement renews automatically for successive 12-month terms unless either party gives written notice of non-renewal %s." % ntext]
    if deem:
        rules.append("A notice sent by email is received when it is sent, except that a notice sent after 5:00 pm or on a Saturday or Sunday (in each case at the recipient's registered office, %s) is treated as received at 9:00 am on the next business day." % fofs(orc))
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["saas"] if "saas" in DOMAIN_FILLER else DOMAIN_FILLER["telecom"]))
    facts = [("Agreement", cid), ("Customer", cust), ("Current term ends", F.d(TE))]
    if deem:
        facts.append(("Non-renewal notice emailed by customer", "%s at %s (customer's local time, %s)" % (F.d(sd), F.t(sh, sm), fofs(osn))))
    else:
        facts.append(("Non-renewal notice received", F.d(target)))
    facts.append(("Annual fee", money(rng.randint(20, 400) * 100)))
    q = "What is the effect of the customer's notice on agreement %s?" % cid
    k1 = label_kind(q, "Is \"{opt}\" the correct effect of the notice on agreement %s?" % cid, labels, g, var)
    k2 = value_kind("date", "What was the last day on which a notice of non-renewal for agreement %s could be received in time?" % cid,
                    "Was {opt} the last day on which non-renewal notice for agreement %s could be received in time?" % cid,
                    LND, [("off_by_one", lnd(("off_by_one",)))], F.od, [("off_by_one", LND - ONE), ("off_by_one", LND + ONE), ("off_by_two", LND - 2 * ONE)])
    yn = [("Did the customer's notice prevent agreement %s from renewing?" % cid, int(g == 0))]
    R = {"off_by_one": "%d days before %s is the deadline" % (N, F.d(RD if v in ("v1", "v3", "v4") else TE)),
         "ignored_deemed_receipt": "it was received the day it was sent", "tz_ignored": "the email went out at %s" % F.t(sh, sm)}
    notes = [(f, note_text(rng, R[f], labels[x])) for f, x in var if x != g]
    traps = ["notice_period", "boundary"] + (["timezone", "deemed_receipt"] if deem else []) + (["double_negation"] if v == "v3" else [])
    return mk_scn(tpl="notice.auto_renewal", domain="saas" if "Cloud" in org or "Stratus" in org else "telecom", org=org, F=F,
                  title="%s - Master Services Agreement" % org, head="Term and renewal", rules=rules, facts=facts, kinds=[k1, k2],
                  yn=yn, notes=notes, traps=traps, cid=cid, subject="Non-renewal notice for %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_notice_resign(rng, size, F):
    org = pick(rng, ["Castellan Foods Ltd", "Norvale Engineering", "Pinecrest Hospital Trust", "Kestrel Components"])
    name = pick(rng, PEOPLE)
    cid = "EMP-%d" % rng.randint(10000, 99999)
    k = pick(rng, [2, 4, 4, 8])
    kp = 1
    prob = rng.random() < 0.5
    safety = prob and size != "short" and rng.random() < 0.5
    exc2 = size != "short"
    hols = []
    NG = rand_date(rng)
    hs = frozenset(hols)
    DG = roll_fwd(NG, hs)
    wk_ = kp if (prob and not (exc2 and safety)) else k
    earliest = DG + ONE * (7 * wk_)
    LW = earliest + ONE * pick(rng, [-2, -1, 0, 0, 1, 3])

    def e_(fl=()):
        dg = NG if "ignored_weekend_rule" in fl else DG
        w = wk_
        if "forgot_exception" in fl:
            w = k
        if "misapplied_exception" in fl and prob:
            w = kp
        return dg + ONE * (7 * w - (1 if "counted_notice_day" in fl else 0))

    def outcome(fl=()):
        return 0 if LW >= e_(fl) else 1
    g = outcome()
    jdg = jdn_date(NG)
    while jdg % 7 >= 5:
        jdg += 1
    assert jdn_to_date(jdg + 7 * wk_) == earliest and (0 if jdn_date(LW) >= jdg + 7 * wk_ else 1) == g, "resignation independent check failed"
    flags = ["ignored_weekend_rule", "counted_notice_day"] + (["forgot_exception"] if prob and not safety else []) + (["misapplied_exception"] if safety else [])
    var = [(f, outcome((f,))) for f in flags]
    if all(x == g for _, x in var):
        raise Retry()
    labels = ["Notice sufficient - pay out accrued leave", "Notice short - accrued-leave payout is forfeited"]
    rules = ["Employees must give at least %s' written notice of resignation." % ("%d weeks" % k),
             "The notice period starts on the day after notice is given, and the last day of employment may not fall before the last day of the notice period.",
             "Notice given on a Saturday or Sunday is treated as given on the following Monday."]
    if prob:
        rules.append("Employees still in their probation period need give only one week's notice.")
        if exc2:
            rules.append("This does not apply to probationers in safety-critical roles, who must give the full notice period.")
    if size != "short" and rng.random() < 0.4:
        rules.append(pick(rng, DOMAIN_FILLER["hr"]))
    facts = [("Employee", "%s (%s)" % (name, cid)), ("Resignation letter handed in", F.d(NG)), ("Requested last working day", F.d(LW)),
             ("On probation", "Yes" if prob else "No"), ("Role", "Forklift operator (safety-critical)" if safety else pick(rng, ["Payroll clerk", "Buyer", "Receptionist"]))]
    q = "What is the correct outcome for %s's resignation?" % name
    k1 = label_kind(q, "Is \"{opt}\" the correct outcome for %s's resignation?" % name, labels, g, var)
    evar = [(f, e_((f,))) for f in flags]
    k2 = value_kind("date", "What is the earliest permissible last day of employment for %s?" % name,
                    "Is {opt} the earliest permissible last day of employment for %s?" % name, earliest, evar, F.od, [("off_by_one", earliest - ONE), ("off_by_one", earliest + ONE)])
    yn = [("Did %s give sufficient notice?" % name, int(g == 0))]
    R = {"ignored_weekend_rule": "the notice was handed in on %s" % F.d(NG), "counted_notice_day": "the day of handing in counts towards the notice",
         "forgot_exception": "everyone gives %d weeks" % k, "misapplied_exception": "probationers only need a week"}
    notes = [(f, note_text(rng, R[f], labels[x])) for f, x in var if x != g]
    traps = ["notice_period"] + (["exception_to_exception"] if safety else []) + (["boundary"] if abs((LW - earliest).days) <= 1 else []) + (["weekend_rule"] if DG != NG else [])
    return mk_scn(tpl="notice.resignation", domain="hr", org=org, F=F, title="%s - Employee Handbook, Leaving Us" % org,
                  head="Notice of resignation", rules=rules, facts=facts, kinds=[k1, k2], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="Resignation - %s" % name, sender=pick(rng, PEOPLE), checked=True)


def gen_notice_appt(rng, size, F):
    org = pick(rng, ["Arbor Community Health", "Bayside Care Network", "Lakeshore Physiotherapy", "Crestview Dental"])
    name = pick(rng, PEOPLE)
    cid = "APT-%d" % rng.randint(100000, 999999)
    oz = pick(rng, [-300, -240, 0, 60, 600])
    op = pick(rng, [o for o in OFFSETS if abs(o - oz) >= 120])
    mode = pick(rng, ["24h", "bday"])
    ad = rand_date(rng)
    ah, am = rng.randint(8, 17), pick(rng, [0, 15, 30, 45])
    au = utc_of(ad, ah, am, oz)
    hols = make_holidays(rng, [], ad - ONE * 10, ad, n_extra=pick(rng, [0, 1]))
    hs = frozenset(hols)
    pbd = ad - ONE
    while not is_bday(pbd, hs):
        pbd -= ONE
    dl24 = au - dt.timedelta(hours=24)
    dlb = utc_of(pbd, 17, 0, oz)
    dl = dl24 if mode == "24h" else dlb
    cu = dl + dt.timedelta(minutes=pick(rng, [-60, -5, 0, 0, 5, 45, 600]))
    if rng.random() < 0.12:
        cu = au + dt.timedelta(minutes=10)
    cd, ch, cm = local_of(cu, op)

    def outcome(fl=()):
        if "tz_ignored" in fl:
            c = utc_of(cd, ch, cm, oz)
        else:
            c = cu
        if c >= au:
            return 2
        if "used_24h_rule" in fl:
            d_ = dl24
        elif "ignored_weekend" in fl and mode == "bday":
            d_ = utc_of(ad - ONE, 17, 0, oz)
        else:
            d_ = dl
        ok = c <= d_ if "boundary_exclusive" not in fl else c < d_
        return 0 if ok else 1
    g = outcome()
    jc = j_umin(cd, ch, cm, op)
    ja = j_umin(ad, ah, am, oz)
    if mode == "24h":
        jdl = ja - 1440
    else:
        hj = [jdn_date(h) for h in hols]
        jp = jdn_date(ad) - 1
        while not j_isb(jp, hj, (5, 6)):
            jp -= 1
        jdl = jp * 1440 + 17 * 60 - oz
    gi = 2 if jc >= ja else (0 if jc <= jdl else 1)
    assert gi == g, "appointment independent check failed"
    flags = ["tz_ignored", "boundary_exclusive"] + (["used_24h_rule", "ignored_weekend"] if mode == "bday" else [])
    var = [(f, outcome((f,))) for f in flags]
    if all(x == g for _, x in var):
        raise Retry()
    labels = ["No fee", "Late-cancellation fee ($40)", "No-show fee ($75)"]
    zone = "%s (%s)" % (pick(rng, PLACES), fofs(oz))
    if mode == "24h":
        r1 = "Appointments cancelled at least 24 hours before the appointment time incur no fee; later cancellations incur the late-cancellation fee."
    else:
        r1 = "Appointments may be cancelled free of charge until 5:00 pm on the last business day before the appointment; later cancellations incur the late-cancellation fee. Business days are Monday to Friday except listed clinic holidays (%s)." % (hol_text(rng, F, hols) if hols else "none this month")
    rules = ["All appointment times are in clinic time, %s, including for video appointments." % zone, r1,
             "A cancellation made at or after the appointment start time, or no cancellation at all, is a no-show."]
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["healthcare"]))
    facts = [("Booking", cid), ("Patient", name), ("Appointment", "%s at %s (clinic time)" % (F.d(ad), F.t(ah, am))),
             ("Type", pick(rng, ["Video consultation", "Physiotherapy session", "Follow-up review"])),
             ("Cancelled via app", "%s at %s (patient's phone, %s)" % (F.d(cd), F.t(ch, cm), fofs(op)))]
    q = "Which fee applies to booking %s?" % cid
    k1 = label_kind(q, "Does \"{opt}\" apply to booking %s?" % cid, labels, g, var)
    yn = [("Can booking %s be cancelled without any fee?" % cid, int(g == 0))]
    R = {"tz_ignored": "the app shows %s on %s" % (F.t(ch, cm), F.d(cd)), "boundary_exclusive": "right on the deadline is already too late",
         "used_24h_rule": "anything more than 24 hours ahead is free", "ignored_weekend": "the day before the appointment is the deadline day"}
    notes = [(f, note_text(rng, R[f], labels[x])) for f, x in var if x != g]
    traps = ["timezone", "notice_period"] + (["boundary"] if abs(int((cu - dl).total_seconds() // 60)) <= 5 else [])
    return mk_scn(tpl="notice.appointment_cancellation", domain="healthcare", org=org, F=F, title="%s - Cancellation Policy" % org,
                  head="Cancellations and missed appointments", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps,
                  cid=cid, subject="Fee query %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_notice_lease(rng, size, F):
    org = pick(rng, ["Eastmoor Housing Association", "Riverside Lettings", "Crane & Lowe Property Services"])
    name = pick(rng, PEOPLE)
    cid = "TEN-%d" % rng.randint(1000, 9999)
    y, m = rng.randint(2025, 2028), rng.randint(1, 12)
    last = dim(y, m)
    post = dt.date(y, m, last) - ONE * pick(rng, [0, 1, 2, 3, 5, 10])
    posted = rng.random() < 0.7
    hs = frozenset()
    R_ = add_bdays(post, 2, hs) if posted else post

    def end(fl=()):
        r = post if "used_posting_date" in fl else R_
        if "thirty_days" in fl:
            return r + ONE * 30
        if "end_of_receipt_month" in fl:
            return last_of_month(r.year, r.month)
        if "corresponding_date" in fl:
            return add_months(r, 1)
        nx = add_months(dt.date(r.year, r.month, 1), 1)
        return last_of_month(nx.year, nx.month)
    g = end()
    jr = jdn_date(post)
    if posted:
        c = 0
        while c < 2:
            jr += 1
            if jr % 7 < 5:
                c += 1
    ry, rm, _ = jdn_to_ymd(jr)
    idx = ry * 12 + rm
    ny, nm = idx // 12, idx % 12 + 1
    assert dt.date(ny, nm, dim(ny, nm)) == g, "lease independent check failed"
    flags = ["thirty_days", "end_of_receipt_month", "corresponding_date"] + (["used_posting_date"] if posted else [])
    var = [(f, end((f,))) for f in flags]
    rules = ["The tenant may end the tenancy by giving at least one full calendar month's written notice, expiring on the last day of a calendar month.",
             "A full calendar month must run from the first to the last day of a month, entirely after the day the notice is received."]
    if posted:
        rules.append("A notice sent by first-class post is treated as received on the second business day after the day of posting (business days: Monday to Friday).")
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["housing"]))
    facts = [("Tenancy", cid), ("Tenant", name), ("Notice to end tenancy", ("posted first class on %s" % F.d(post)) if posted else ("handed to the office on %s" % F.d(post))),
             ("Tenant's proposed end date", F.d(post + ONE * 30)), ("Monthly rent", money(rng.randint(6, 25) * 100))]
    q = "What is the earliest date on which tenancy %s can end under this notice?" % cid
    k1 = value_kind("date", q, "Is {opt} the earliest date on which tenancy %s can end?" % cid, g, var, F.od)
    X = post + ONE * 30
    yn = [("Can tenancy %s end on the tenant's proposed date (%s)?" % (cid, F.d(X)), int(X >= g and X == last_of_month(X.year, X.month)))]
    R = {"thirty_days": "a month's notice is 30 days", "end_of_receipt_month": "notice can expire at the end of the month it arrives in",
         "corresponding_date": "one month after the notice date is enough", "used_posting_date": "the notice was sent on %s" % F.d(post)}
    notes = [(f, note_value(rng, R[f], F.d(v))) for f, v in var if v != g]
    traps = ["notice_period", "month_length", "surface_cue"] + (["deemed_receipt"] if posted else [])
    return mk_scn(tpl="notice.lease_end", domain="housing", org=org, F=F, title="%s - Assured Tenancy Agreement" % org,
                  head="Ending the tenancy", rules=rules, facts=facts, kinds=[k1], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="End date for %s" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_notice_ecn(rng, size, F):
    org = pick(rng, ["Kestrel Components", "Ironvale Fabrication", "Delta Precision Castings"])
    custo = pick(rng, ["Apex Motors", "Nordic Rail Systems", "Heliotrope Medical"])
    cid = "ECN-%d" % rng.randint(1000, 9999)
    N = pick(rng, [5, 10, 15])
    I = rand_date(rng)
    while I.weekday() >= 5:
        I += ONE
    v = pick(rng, ["nth", "full"])
    hols0 = [I - ONE * i for i in range(1, 3 * N) if (I - ONE * i).weekday() < 5]
    must = rng.sample(hols0, pick(rng, [0, 1, 2]))
    hols = [h for h in make_holidays(rng, must, I - ONE * 60, I + ONE * 30, n_extra=1) if h != I]
    hs = frozenset(hols)
    LD = sub_bdays(I, N + (1 if v == "full" else 0), hs)
    S = LD + ONE * pick(rng, [-1, 0, 0, 1, 2])

    def latest(fl=()):
        h_ = frozenset() if "ignored_holidays" in fl else hs
        n = N + (1 if v == "full" else 0)
        if "off_by_one" in fl:
            n = n - 1 if v == "full" else n + 1
        if "calendar_days" in fl:
            return I - ONE * n
        return sub_bdays(I, n, h_)

    def outcome(fl=()):
        return 0 if S <= latest(fl) else 1
    g = outcome()
    hj = [jdn_date(h) for h in hols]
    jl = jdn_date(LD)
    assert j_count(jl - 1, jdn_date(I) - 1, hj, (5, 6)) == N + (1 if v == "full" else 0) and j_isb(jl, hj, (5, 6)), "ecn independent check failed"
    flags = ["off_by_one", "calendar_days", "ignored_holidays"]
    var = [(f, outcome((f,))) for f in flags]
    dvar = [(f, latest((f,))) for f in flags]
    if all(x == g for _, x in var) and all(x == LD for _, x in dvar):
        raise Retry()
    labels = ["ECN compliant - implement on the planned date", "ECN late - implementation must be deferred"]
    rtxt = ("An engineering change notice (ECN) must reach the customer no later than the %s business day before the planned implementation date." % ordinal(N)) if v == "nth" else \
        ("At least %d full business days must separate the day the customer receives an ECN and the planned implementation date (neither of those two days counts)." % N)
    rules = [rtxt, "Business days exclude Saturdays, Sundays and the plant holidays listed: %s." % hol_text(rng, F, hols)]
    if size != "short" and rng.random() < 0.5:
        rules.append(pick(rng, DOMAIN_FILLER["manufacturing"]))
    facts = [("ECN", cid), ("Customer", custo), ("Change", pick(rng, ["Alternate resin supplier", "Revised torque spec", "New heat-treat furnace"])),
             ("Planned implementation date", F.d(I)), ("ECN received by customer", F.d(S))]
    k1 = label_kind("Is %s compliant with the notice requirement?" % cid, "Is \"{opt}\" the correct status of %s?" % cid, labels, g, var)
    k2 = value_kind("date", "What is the last day on which the customer could receive %s for the planned implementation date to stand?" % cid,
                    "Is {opt} the last day on which the customer could receive %s in time?" % cid, LD, dvar, F.od, [("off_by_one", LD - ONE)])
    yn = [("Can the change under %s be implemented on the planned date?" % cid, int(g == 0))]
    R = {"off_by_one": "counting back %d business days from %s gives the deadline" % (N, F.d(I)), "calendar_days": "%d days before the implementation date is fine" % N,
         "ignored_holidays": "every weekday counts"}
    notes = [(f, note_text(rng, R[f], labels[x])) for f, x in var if x != g]
    traps = ["business_days", "notice_period"] + (["holiday"] if must else []) + (["boundary"] if abs((S - LD).days) <= 1 else [])
    return mk_scn(tpl="notice.engineering_change", domain="manufacturing", org=org, F=F, title="%s - Customer Quality Requirements" % org,
                  head="Change notification", rules=rules, facts=facts, kinds=[k1, k2], yn=yn, notes=notes, traps=traps, cid=cid,
                  subject="%s notice check" % cid, sender=pick(rng, PEOPLE), checked=True)


def gen_notice(rng, size, F):
    return dispatch(rng, size, F, [gen_notice_renewal, gen_notice_resign, gen_notice_appt, gen_notice_lease, gen_notice_ecn])


# ======================================================================== registry
GENS = [gen_deadline, gen_bdays, gen_months, gen_timezone, gen_sla, gen_version, gen_adherence, gen_age, gen_grace, gen_notice]




SUBKINDS = [
    ("deadline", gen_deadline), ("business_days", gen_bdays), ("months", gen_months), ("sla", gen_sla),
    ("timezone", gen_tz_dose), ("timezone", gen_tz_exam), ("timezone", gen_tz_wire), ("timezone", gen_tz_breach),
    ("timezone", gen_tz_maint),
    ("version", gen_ver_perdiem), ("version", gen_ver_deductible), ("version", gen_ver_parental),
    ("version", gen_ver_tuition), ("version", gen_ver_price), ("version", gen_ver_benefit),
    ("adherence", gen_adh_flight), ("adherence", gen_adh_vaccine), ("adherence", gen_adh_calibration),
    ("adherence", gen_adh_refill), ("adherence", gen_adh_slot),
    ("age", gen_age_school), ("age", gen_age_fare), ("age", gen_age_dependent), ("age", gen_age_vesting),
    ("age", gen_age_pension),
    ("grace", gen_grace_rent), ("grace", gen_grace_premium), ("grace", gen_grace_card), ("grace", gen_grace_library),
    ("notice", gen_notice_renewal), ("notice", gen_notice_resign), ("notice", gen_notice_appt),
    ("notice", gen_notice_lease), ("notice", gen_notice_ecn),
]
# sub-kinds whose rendered text can fit under 600 characters
SHORT_OK = [gen_deadline, gen_bdays, gen_months, gen_tz_exam, gen_ver_parental, gen_ver_price, gen_adh_refill,
            gen_age_school, gen_age_fare, gen_age_dependent, gen_age_vesting, gen_age_pension, gen_grace_library,
            gen_notice_renewal, gen_notice_resign, gen_notice_lease, gen_notice_ecn]
# sub-kinds that carry several domains internally get extra weight in the plan
WEIGHT = {gen_deadline: 3, gen_bdays: 3, gen_months: 2, gen_sla: 2}


def _plan(master, n):
    fams = []
    for f, _ in SUBKINDS:
        if f not in fams:
            fams.append(f)
    by_f = dict((f, [fn for g, fn in SUBKINDS if g == f]) for f in fams)
    long_pool = []
    for f in fams:
        subs = []
        for fn in by_f[f]:
            subs += [fn] * WEIGHT.get(fn, 1)
        long_pool.append(subs)
    short_pool = []
    for fn in SHORT_OK:
        short_pool += [fn] * WEIGHT.get(fn, 1)
    return fams, long_pool, short_pool


def generate(n, seed, _keep=False):
    master = random.Random(seed)
    n_choice = int(round(n * 0.7))
    qtypes = ["choice"] * n_choice + ["noul"] * (n - n_choice)
    master.shuffle(qtypes)
    n_noul = n - n_choice
    tg = [1] * (n_noul // 2) + [0] * (n_noul - n_noul // 2)
    if n_noul % 2 and master.random() < 0.5:
        tg[-1] = 1
    master.shuffle(tg)
    n_s, n_m = int(round(n * 0.3)), int(round(n * 0.4))
    sizes = ["short"] * n_s + ["medium"] * n_m + ["long"] * (n - n_s - n_m)
    master.shuffle(sizes)
    fams, long_pool, short_pool = _plan(master, n)
    fam_order = [i % len(fams) for i in range(n)]
    master.shuffle(fam_order)
    sp = list(short_pool)
    master.shuffle(sp)
    ctr = [master.randrange(len(p)) for p in long_pool]
    si = 0
    plan = []
    for i in range(n):
        if sizes[i] == "short":
            plan.append(sp[si % len(sp)])
            si += 1
        else:
            fi = fam_order[i]
            pool = long_pool[fi]
            plan.append(pool[ctr[fi] % len(pool)])
            ctr[fi] += 1
    all_fns = [fn for _, fn in SUBKINDS]
    rows = []
    ti = 0
    for i in range(n):
        qt = qtypes[i]
        target = None
        if qt == "noul":
            target = tg[ti]
            ti += 1
        row = None
        for attempt in range(200):
            rng = random.Random(seed * 1000003 + i * 7919 + attempt * 104729)
            size = sizes[i] if attempt < 180 else "medium"
            if attempt < 60:
                gen = plan[i]
            elif sizes[i] == "short" and attempt < 180:
                gen = short_pool[(i + attempt) % len(short_pool)]
            else:
                gen = all_fns[(i + attempt) % len(all_fns)]
            try:
                F = Fmt(rng)
                sc = gen(rng, size, F)
                row = finalize(rng, sc, qt, target, size)
            except Retry:
                row = None
            if row is not None:
                break
        if row is None:
            raise RuntimeError("could not generate item %d" % i)
        if not _keep:
            for k in ("_tpl", "_domain", "_checked"):
                row.pop(k, None)
        rows.append(row)
    return rows


# ======================================================================== self-test
ROW_KEYS = {"state", "qtype", "instructions", "options", "gold", "meta"}


def _check_row(r):
    keys = set(r.keys())
    assert ROW_KEYS <= keys <= ROW_KEYS | {"card"}, keys
    assert isinstance(r["state"], str) and r["state"].strip()
    assert isinstance(r["instructions"], str) and r["instructions"].strip()
    assert r["qtype"] in ("choice", "noul")
    m = r["meta"]
    assert set(m.keys()) <= {"family", "difficulty", "gold_probs", "mistakes"}, m.keys()
    assert m["family"] == FAMILY and m["difficulty"] in ("medium", "hard")
    if r["qtype"] == "choice":
        o = r["options"]
        assert isinstance(o, list) and 2 <= len(o) <= 8 and all(isinstance(x, str) for x in o)
        assert len(set(o)) == len(o), o
        assert r["gold"] in o
        for k, v in m.get("mistakes", {}).items():
            assert k in o and k != r["gold"] and isinstance(v, str)
        if r.get("card") is not None:
            lines = r["card"].split("\n")
            assert len(lines) == len(o) and all(l.startswith("- ") for l in lines)
            assert sorted(l[2:].split(":")[0] for l in lines) == sorted(o)
    else:
        assert r["options"] is None and r["gold"] in (0, 1) and "card" not in r
    if "gold_probs" in m:
        assert abs(sum(m["gold_probs"].values()) - 1.0) < 1e-9


def _unit_checks():
    rng = random.Random(123)
    for _ in range(3000):
        d = dt.date(1900, 1, 1) + ONE * rng.randrange(80000)
        j = jdn_date(d)
        assert jdn_to_date(j) == d and j - d.toordinal() == 1721425 and j % 7 == d.weekday()
        k = rng.randint(-30, 30)
        assert add_months(d, k) == add_months_indep(d, k)
        b = d - ONE * rng.randrange(40000)
        for f29 in ("mar1", "feb28"):
            assert age_on(b, d, f29) == age_on_indep(b, d, f29) if d >= b else True
        e = d + ONE * rng.randrange(60)
        hol = sorted(set(d + ONE * rng.randrange(60) for _ in range(3)))
        wk = pick(rng, [(5, 6), (4, 5), (6,)])
        assert bdays_between(d, e, frozenset(hol), wk) == j_count(jdn_date(d), jdn_date(e), [jdn_date(h) for h in hol], wk)
        o1 = pick(rng, OFFSETS)
        h, mi = rng.randint(0, 23), rng.randint(0, 59)
        u = utc_of(d, h, mi, o1)
        assert naive_min(u.date(), u.hour, u.minute) == j_umin(d, h, mi, o1)


def _selftest(n=300, seed=20260926):
    import subprocess
    import sys
    _unit_checks()
    rows = generate(n, seed, _keep=True)
    for r in rows:
        assert r.pop("_checked") is True, "independent check missing"
        r.pop("_tpl")
        r.pop("_domain")
        _check_row(r)
    a = json.dumps(generate(n, seed), sort_keys=True)
    b = json.dumps(generate(n, seed), sort_keys=True)
    assert a == b, "not deterministic"
    assert json.dumps(rows, sort_keys=True) == a, "private fields changed output"
    code = "import json,hashlib;from pg.temporal import generate;print(hashlib.sha256(json.dumps(generate(60,%d),sort_keys=True).encode()).hexdigest())" % seed
    hs = set()
    for phs in ("1", "4242"):
        env = dict(__import__("os").environ, PYTHONHASHSEED=phs)
        out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env,
                             cwd=__import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
        assert out.returncode == 0, out.stderr
        hs.add(out.stdout.strip())
    assert len(hs) == 1, "output depends on PYTHONHASHSEED"
    ch = [r for r in rows if r["qtype"] == "choice"]
    nu = [r for r in rows if r["qtype"] == "noul"]
    assert abs(len(ch) / float(n) - 0.7) < 0.02
    yes = sum(r["gold"] for r in nu) / float(len(nu))
    assert abs(yes - 0.5) < 0.02, yes
    L = [len(r["state"]) for r in rows]
    sh, md, lg = sum(l < 600 for l in L), sum(600 <= l <= 2500 for l in L), sum(2500 < l <= 6000 for l in L)
    assert sh + md + lg == n
    assert abs(sh / float(n) - 0.3) < 0.03 and abs(md / float(n) - 0.4) < 0.03 and abs(lg / float(n) - 0.3) < 0.03
    pos = [0] * 8
    for r in ch:
        pos[r["options"].index(r["gold"])] += 1
    diff = sum(1 for r in rows if r["meta"]["difficulty"] == "hard")
    return dict(n=n, choice=len(ch), noul=len(nu), noul_yes_rate=round(yes, 3), short=sh, medium=md, long=lg,
                gold_positions=pos, hard=diff)


if __name__ == "__main__":
    ex = generate(3, 7)
    for r in ex:
        print("=" * 100)
        print(r["state"])
        print("-" * 100)
        print("INSTRUCTIONS:", r["instructions"])
        print("OPTIONS:", r["options"])
        if r.get("card"):
            print("CARD:\n" + r["card"])
        print("GOLD:", r["gold"])
        print("META:", json.dumps(r["meta"]))
    print("=" * 100)
    import collections
    rows = generate(300, 20260926, _keep=True)
    tpls = collections.Counter(r["_tpl"] for r in rows)
    doms = collections.Counter(r["_domain"] for r in rows)
    print("templates used: %d distinct; domains: %d distinct %s" % (len(tpls), len(doms), sorted(doms)))
    print("SELF-TEST PASSED:", json.dumps(_selftest()))
