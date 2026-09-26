# -*- coding: utf-8 -*-
"""pg.policy -- procedural generator of hard "System-One" decision problems built on
long policy / contract / benefit documents (family "policy").

Each item has numbered sections with two look-alike defined terms, a threshold rule,
exceptions and exceptions-to-exceptions, class-specific overrides, dated endorsements
that supersede base clauses only for later cases, a precedence clause, a case file and
sometimes a note from a junior (unauthorised) colleague who pushes a surface answer.

The gold outcome is computed by a small rule engine (solve) from the sampled facts and
re-checked by an independent evaluator (solve2: ordinal dates, integer cross-multiplied
comparisons, boolean formula, Decimal money).  Every wrong option is the output of the
same engine run with one (or two) named reasoning mistakes switched on.

API:  generate(n, seed) -> list[dict]
Run:  python3 -m pg.policy      (prints 3 examples and runs the self-test)
"""
import datetime as dt
import json
import random
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

FAMILY = "policy"


class Retry(Exception):
    """Degenerate draw (e.g. no mistake changes the answer, or length out of range)."""


# ----------------------------------------------------------------------------- helpers
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII",
         "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"]
LETTERS = "ABCDEFGHIJKLMNOPQRST"


def pick(rng, xs):
    return xs[rng.randrange(len(xs))]


def cap(s):
    return s[:1].upper() + s[1:]


def fnum(x):
    """Format an int / Fraction exactly (decimals only when needed)."""
    x = Fraction(x)
    if x.denominator == 1:
        return "{:,}".format(x.numerator)
    d = Decimal(x.numerator) / Decimal(x.denominator)
    s = format(d.quantize(Decimal("0.0001")), "f").rstrip("0").rstrip(".")
    ip, _, fp = s.partition(".")
    ip = "{:,}".format(int(ip))
    return ip + ("." + fp if fp else "")


def money(x, cur="$"):
    q = Decimal(Fraction(x).numerator) / Decimal(Fraction(x).denominator)
    q = q.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return "%s%s" % (cur, "{:,.2f}".format(q))


def fdate(d, style):
    if style == 0:
        return d.isoformat()
    if style == 1:
        return "%d %s %d" % (d.day, MONTHS[d.month - 1], d.year)
    if style == 2:
        return "%s %d, %d" % (MONTHS[d.month - 1], d.day, d.year)
    if style == 3:
        return "%02d/%02d/%d" % (d.day, d.month, d.year) + " (DD/MM/YYYY)"
    return "%s %d %d" % (MONTHS[d.month - 1][:3], d.day, d.year)


# --------------------------------------------------------------- comparison wording
# dir "over": rule hits when q exceeds the limit; "under": when q is below it.
CMP_TXT = {
    ("over", False): ["more than {L} {u}", "in excess of {L} {u}", "longer than {L} {u}",
                      "over {L} {u}", "more than {L} {u}"],
    ("over", True): ["{L} or more {u}", "at least {L} {u}", "not less than {L} {u}",
                     "no fewer than {L} {u}", "{L} {u} or longer"],
    ("under", False): ["less than {L} {u}", "fewer than {L} {u}", "under {L} {u}",
                       "less than {L} {u}"],
    ("under", True): ["{L} {u} or less", "no more than {L} {u}", "not more than {L} {u}",
                      "at most {L} {u}", "{L} {u} or fewer"],
}


def cmp_text(rng, direction, incl, L, unit):
    t = pick(rng, CMP_TXT[(direction, incl)])
    return t.format(L=fnum(L), u=unit)


def hit(q, L, incl, direction):
    if direction == "over":
        return q >= L if incl else q > L
    return q <= L if incl else q < L


AMEND_WHEN = {True: ["on or after {D}", "on and after {D}", "from {D} (inclusive)",
                     "with effect from and including {D}"],
              False: ["after {D}", "strictly after {D}", "later than {D}",
                      "after (not on) {D}"]}


# --------------------------------------------------------------- numbering styles
class Num(object):
    """Section heading / cross-reference style, consistent within one document."""

    def __init__(self, rng, short=False):
        self.style = rng.randrange(6) if not short else pick(rng, [0, 1, 4])
        self.sub = rng.randrange(2)  # 0 -> 4(a), 1 -> 4.1

    def head(self, n, title):
        s = self.style
        if s == 0:
            return "Section %d. %s" % (n, title)
        if s == 1:
            return "§ %d  %s" % (n, title)
        if s == 2:
            return "%d. %s" % (n, title.upper())
        if s == 3:
            return "Article %s — %s" % (ROMAN[n - 1], title)
        if s == 4:
            return "Clause %d: %s" % (n, title)
        return "PART %s. %s" % (LETTERS[n - 1], title)

    def ref(self, n, k=None):
        s = self.style
        base = {0: "Section %d" % n, 1: "§ %d" % n, 2: "Section %d" % n,
                3: "Article %s" % ROMAN[n - 1], 4: "Clause %d" % n,
                5: "Part %s" % LETTERS[n - 1]}[s]
        if k is None:
            return base
        if self.sub == 0 or s in (3, 5):
            return "%s(%s)" % (base, "abcdefgh"[k])
        return "%s.%d" % (base, k + 1)

    def item(self, n, k):
        if self.sub == 0 or self.style in (3, 5):
            return "(%s)" % "abcdefgh"[k]
        return "%d.%d" % (n, k + 1) if self.style not in (3, 5) else "(%s)" % "abcdefgh"[k]


# --------------------------------------------------------------- mistake names
MISTAKE_NAMES = {
    "term": "surface term: confused the two defined terms",
    "unit": "unit mix-up: compared the raw number in the wrong unit",
    "boundary": "off-by-one: inclusive/exclusive threshold flipped",
    "amend_boundary": "effective-date boundary: on vs after the effective date",
    "date_basis": "wrong trigger date for the endorsement",
    "old_rule": "applied the superseded (pre-endorsement) rule",
    "retro": "applied the endorsement retroactively",
    "first_amend": "ignored the later endorsement (later one prevails)",
    "general": "used the general rule instead of the class-specific override",
    "no_exception": "forgot the exception",
    "no_exc_exc": "forgot the exception to the exception",
    "deductible": "forgot the deductible / deduction",
    "gate_boundary": "off-by-one on the eligibility threshold",
    "ignore_gate": "skipped the eligibility requirement",
    "order": "applied the percentage before subtracting the deduction",
}


# =========================================================================== domains
# Term A holds iff (X and Y); term B holds iff (X and not Y).  X is always true in the case.
# y = (label, text when Y true [A holds], text when Y false [B holds]).
# c1/c2 = (rule phrase, fact when true, fact when false, label).
# sub = (name, plural, fact when case is of the class, fact when not, label).
# gate = (condition with {CMP}, unit, limits, dir, label, fact with {G}).
# ev = (event label, other-date label, event basis phrase, other basis phrase, other_after_event).
F = Fraction
DOMAINS = []


def domain(**kw):
    kw.setdefault("gate", None)
    kw.setdefault("alts", [])
    kw.setdefault("else_txt", "")
    DOMAINS.append(kw)
    return kw


domain(
    key="insurance_property", polarity="restrict",
    orgs=["Harbourline Mutual", "Keystone Home Assurance", "Blue Fen Insurance Co.", "Tallis & Reed Underwriters"],
    docs=["Homeowners Policy HO-{n}", "Residential Property Wording RP-{n}", "Home Cover Master Policy (Form {n})"],
    case="claim", cid="CLM", approver="claims examiner", juniors=["claims trainee", "summer intern", "junior adjuster (no settlement authority)"],
    A=("Vacant", "means no person resides in the Dwelling and it lacks the personal property needed for customary occupancy."),
    B=("Unoccupied", "means no person resides in the Dwelling although it still holds the personal property needed for customary occupancy."),
    y=("Contents", "The tenants had removed all furniture and belongings; the rooms were bare.",
       "The owner's furniture, beds and kitchen equipment remained in the house."),
    surface=['The first notice of loss describes the house as "{w}".',
             'A neighbour told the field adjuster the house had been "{w}" for months.',
             'The broker\'s cover email calls the property "{w}".'],
    dir="over", unit="days", unit_rule="consecutive days", alts=[("weeks", F(7))], limits=[30, 45, 60, 90, 120],
    cond="the Dwelling had been {T} for {CMP} immediately before the loss",
    q=("Period without a resident", "No one had lived in the house for {Q} before the loss."),
    rule_title="Vacancy and occupancy", trig="no payment is due for the loss",
    neg="no claim is refused under this provision",
    sub=("Seasonal Dwelling", "Seasonal Dwellings", "The schedule lists the property as a Seasonal Dwelling.",
         "The property is the insured's primary residence, not a Seasonal Dwelling.", "Property class"),
    c1=("the Dwelling was being renovated under a valid building permit",
        "A building permit for renovation was valid and work was in progress at the time of loss.",
        "No renovation work or building permit was in place.", "Renovation"),
    c2=("the loss was caused by theft or vandalism", "The damage was caused by vandals who forced a rear door.",
        "The damage was caused by a pipe that burst during a cold snap.", "Cause of loss"),
    gate=("the Policy has been in force for {CMP} on the date of loss", "days", [14, 30, 60], "over",
          "Policy in force", "The policy had been in force for {G} days on the date of loss."),
    ev=("Date of loss", "Date reported", "losses occurring", "claims reported", True),
    scheme="pay", amt=dict(A=(4000, 90000, 50), d=[500, 1000, 1500, 2500], keep=[50, 60, 75]),
    fa=("Adjusted loss", "The adjusted amount of the loss is {A}."), fd=("Deductible", "The policy deductible is {d}."),
    out=dict(NOTRIG="Approve and pay {amt}", TRIG="Deny the claim under {sec}",
             TRIG_NEW="Approve at {keep}% and pay {amt}", INELIG="Decline: waiting period in {gsec} not met"),
    am_out="A loss that would otherwise be refused under {ref} is instead payable at {keep}% of the adjusted loss after the deductible.",
    fdefs=[("Dwelling", "means the building described in the Declarations, including attached structures."),
           ("Occurrence", "means an accident, including repeated exposure to substantially the same conditions."),
           ("Actual Cash Value", "means replacement cost less physical depreciation.")],
    fsecs=[("Water backup", "Loss caused by water backing up through sewers or drains is covered up to $5,000 per occurrence."),
           ("Mold", "Mold remediation is limited to $10,000 in the aggregate per policy period."),
           ("Loss settlement", "Covered losses to the Dwelling are settled at replacement cost once repairs are complete; until then, at Actual Cash Value."),
           ("Mortgage clause", "Payment for loss to the Dwelling is made jointly to the insured and any mortgagee named in the Declarations.")],
    noise=[("Policy form", "Special form, all-risk"), ("Roof", "The roof was replaced six years ago."),
           ("Prior claims", "One hail claim was paid three years ago."), ("Contact", "The insured prefers email.")],
)

domain(
    key="hr_bonus_clawback", polarity="charge",
    orgs=["Corvane Systems", "Mistral Foods plc", "Oakridge Analytics", "Pelham Logistics Group"],
    docs=["Employee Handbook, Chapter {n}", "Sign-On Bonus Agreement (Template {n})", "Compensation Policy CP-{n}"],
    case="exit file", cid="HR", approver="HR business partner", juniors=["HR intern", "payroll assistant", "new HR coordinator"],
    A=("Voluntary Resignation", "means an employee-initiated termination that is not preceded by a Material Adverse Change."),
    B=("Good Reason Resignation", "means an employee-initiated termination that is preceded by a Material Adverse Change."),
    y=("Before resigning", "No change was made to the employee's pay, title or duties before the resignation.",
       "Three weeks before resigning, the employee's base pay was cut by 15%, a Material Adverse Change."),
    surface=['HR\'s exit checklist records the departure as a "{w}".',
             'The manager wrote "{w}" in the offboarding ticket.'],
    dir="under", unit="months", unit_rule="months of service", alts=[("years", F(12))], limits=[6, 9, 12, 18, 24, 36],
    cond="the Employee's employment ends by {T} with {CMP}",
    q=("Length of service", "The employee's employment ended after {Q} of service."),
    rule_title="Sign-on bonus repayment", trig="the Employee must repay {p0}% of the Sign-On Bonus",
    neg="no part of the Sign-On Bonus is repayable",
    sub=("Relocated Hire", "Relocated Hires", "The employee was hired under the relocation programme (a Relocated Hire).",
         "The employee was a local hire, not a Relocated Hire.", "Hire type"),
    c1=("the Employee's position had been eliminated in a reorganisation announced before the resignation",
        "Before the resignation, the company announced a reorganisation that eliminated the employee's position.",
        "The employee's position was not affected by any reorganisation.", "Reorganisation"),
    c2=("the Employee joins a competitor listed in Schedule 2 within six months",
        "The employee joined a Schedule 2 competitor one month later.",
        "The employee has not joined any company listed in Schedule 2.", "Next employer"),
    ev=("Last day of employment", "Resignation notice given", "employments ending", "resignation notices given", False),
    scheme="charge", amt=dict(A=(4000, 30000, 500), p0=[100], p1=[50, 60, 75]),
    fa=("Sign-on bonus", "A sign-on bonus of {A} was paid on joining."), fd=None,
    out=dict(TRIG="Recover {amt} from the employee", TRIG_NEW="Recover {amt} from the employee",
             NOTRIG="No repayment is owed"),
    am_out="Where repayment is required under {ref}, the Employee repays {p1}% of the Sign-On Bonus instead of {p0}%.",
    fdefs=[("Start Date", "means the first day on which the Employee performs services."),
           ("Material Adverse Change", "means a base-pay cut of 10% or more, a demotion, or a required relocation over 50 miles."),
           ("Sign-On Bonus", "means the one-time payment described in the offer letter.")],
    fsecs=[("Holiday carry-over", "Up to five unused vacation days may be carried into the next calendar year."),
           ("Expense claims", "Expense claims must be submitted within 60 days with itemised receipts."),
           ("Notice period", "Employees below grade 7 give two weeks' notice; grade 7 and above give four weeks."),
           ("Equipment return", "Company equipment must be returned on or before the last day of employment.")],
    noise=[("Grade", "Grade 6"), ("Department", "Customer Success"), ("Accrued vacation", "4.5 days unused"),
           ("Exit interview", "Completed")],
)

domain(
    key="bank_late_fee", polarity="charge",
    orgs=["Fenwick Savings Bank", "Northgate Credit Union", "Alder & Pike Bank", "Summit Ridge Lending"],
    docs=["Personal Loan Terms and Conditions (v{n})", "Consumer Lending Fee Schedule FS-{n}", "Loan Account Agreement, Form {n}"],
    case="account review", cid="LN", approver="collections supervisor", juniors=["collections trainee", "branch intern", "new servicing analyst"],
    A=("Delinquent Account", "means an account with an installment unpaid after its due date and no Payment Arrangement in force."),
    B=("Arranged Account", "means an account with an installment unpaid after its due date while a Payment Arrangement is in force."),
    y=("Payment arrangement", "No Payment Arrangement had been agreed for the missed installment.",
       "A written Payment Arrangement was agreed and in force for the missed installment."),
    surface=['The collections dashboard flags the account as "{w}".',
             'The customer\'s last statement is stamped "{w}".'],
    dir="over", unit="days", unit_rule="days past due", alts=[("weeks", F(7))], limits=[10, 14, 15, 21, 30],
    cond="an installment on any {T} remains unpaid for {CMP}",
    q=("Days past due", "The missed installment had been unpaid for {Q} at the fee run."),
    rule_title="Late fees", trig="a Late Fee of {p0}% of the overdue installment is charged",
    neg="no Late Fee is charged",
    sub=("Student Loan Account", "Student Loan Accounts", "The loan is a Student Loan Account.",
         "The loan is a personal installment loan, not a Student Loan Account.", "Product"),
    c1=("the installment was missed because of an error in the Bank's own autopay system",
        "The installment was missed because the Bank's autopay system failed to collect it.",
        "The installment was missed because the customer's account had insufficient funds.", "Reason missed"),
    c2=("the customer already received a system-error waiver in the previous 12 months",
        "The customer already received a system-error waiver seven months ago.",
        "The customer has never received a fee waiver.", "Waiver history"),
    ev=("Installment due date", "Customer complaint received", "installments falling due", "complaints received", True),
    scheme="charge", amt=dict(A=(300, 4000, 5), p0=[5, 6, 8], p1=[3, 4, 10]),
    fa=("Overdue installment", "The overdue installment is {A}."), fd=None,
    out=dict(TRIG="Charge a late fee of {amt}", TRIG_NEW="Charge a late fee of {amt}", NOTRIG="Do not charge a late fee"),
    am_out="The Late Fee under {ref} is {p1}% of the overdue installment (replacing {p0}%).",
    fdefs=[("Payment Arrangement", "means a written agreement to pay overdue amounts on a revised schedule."),
           ("Business Day", "means a day other than Saturday, Sunday or a bank holiday."),
           ("Statement Date", "means the monthly date on which a statement is produced.")],
    fsecs=[("Returned payments", "A returned-payment fee of $25 applies to each dishonoured payment."),
           ("Early repayment", "The loan may be repaid early at any time without charge."),
           ("Interest", "Interest accrues daily on the outstanding principal at the contract rate."),
           ("Statements", "Statements are issued monthly on the Statement Date.")],
    noise=[("Loan term", "60 months"), ("Channel", "Online"), ("Credit score at origination", "712"),
           ("Paperless", "Yes")],
)

domain(
    key="logistics_liability", polarity="restrict",
    orgs=["Transvia Freight", "Northsea Cold Chain B.V.", "Rapid Reefer Lines", "Castellan Logistics"],
    docs=["General Conditions of Carriage GCC-{n}", "Temperature-Controlled Services Terms (Ed. {n})", "Carrier Tariff Rules, Part {n}"],
    case="claim", cid="CC", approver="claims manager", juniors=["claims clerk", "graduate trainee", "night-shift dispatcher"],
    A=("Perishable Cargo", "means goods carried under temperature control whose labelled shelf life is under 30 days."),
    B=("Temperature-Controlled Cargo", "means goods carried under temperature control whose labelled shelf life is 30 days or more."),
    y=("Shelf life", "The labels show a shelf life of 12 days.", "The labels show a shelf life of 18 months."),
    surface=['The shipper\'s booking form ticked the box "{w}".',
             'The driver\'s exception report describes the load as "{w}".'],
    dir="over", unit="hours", unit_rule="hours", alts=[("days", F(24)), ("minutes", F(1, 60))], limits=[24, 36, 48, 72],
    cond="{T} is held at the destination depot awaiting collection for {CMP}",
    q=("Time held at depot", "The consignment was held at the destination depot for {Q} before collection."),
    rule_title="Depot storage and spoilage", trig="the Carrier is not liable for spoilage",
    neg="the Carrier remains liable for spoilage",
    sub=("Pharmaceutical Consignment", "Pharmaceutical Consignments", "The consignment is registered as a Pharmaceutical Consignment.",
         "The consignment is food produce, not a Pharmaceutical Consignment.", "Cargo class"),
    c1=("the Carrier failed to send the arrival notice required by these Conditions",
        "The Carrier did not send the required arrival notice to the consignee.",
        "The Carrier sent the arrival notice on the day of arrival.", "Arrival notice"),
    c2=("the booking omitted a working consignee phone number",
        "The booking listed a consignee phone number that was disconnected.",
        "The booking listed a working consignee phone number.", "Consignee contact"),
    gate=("the shipper's account has been open for {CMP} at the time of shipment", "days", [30, 60, 90], "over",
          "Account age", "The shipper's account had been open for {G} days at the time of shipment."),
    ev=("Arrival at depot", "Claim submitted", "consignments arriving", "claims submitted", True),
    scheme="pay", amt=dict(A=(1500, 40000, 25), d=[150, 250, 400], keep=[40, 50, 70]),
    fa=("Claimed value", "The documented value of the spoiled goods is {A}."),
    fd=("Handling deduction", "The standard handling deduction is {d}."),
    out=dict(NOTRIG="Pay the claim: {amt}", TRIG="Reject the spoilage claim under {sec}",
             TRIG_NEW="Pay {keep}% of the claim: {amt}", INELIG="Reject: account-age condition in {gsec} not met"),
    am_out="Spoilage that would be excluded under {ref} is compensated at {keep}% of the claim after the handling deduction.",
    fdefs=[("Consignee", "means the party entitled to take delivery."),
           ("Transit Window", "means the delivery period quoted at booking."),
           ("Depot", "means a Carrier-operated cross-dock facility.")],
    fsecs=[("Dangerous goods", "Dangerous goods must be declared; undeclared dangerous goods travel at the shipper's risk."),
           ("Heavy pieces", "Single pieces over 1,000 kg require prior booking of lifting equipment."),
           ("Customs", "The Carrier acts as customs agent only when instructed in writing."),
           ("Transit loss", "Liability for loss in transit is limited to the declared value on the waybill.")],
    noise=[("Pallets", "6 pallets"), ("Route", "Rotterdam - Lyon"), ("Reefer setpoint", "+2 to +4 C"),
           ("Seal number", "intact on arrival")],
)

domain(
    key="health_preauth", polarity="restrict",
    orgs=["Meridian Health Plan", "Cobalt Care Benefits", "Lakeshore Employee Health Trust", "Verity Medical Scheme"],
    docs=["Summary Plan Description, Part {n}", "Group Medical Benefit Booklet (Rev. {n})", "Utilization Management Rules UM-{n}"],
    case="claim", cid="MC", approver="utilization reviewer", juniors=["benefits intern", "new customer-service rep", "billing trainee"],
    A=("Elective Admission", "means an admission booked 24+ hours ahead where the physician has not certified the condition as time-sensitive."),
    B=("Time-Sensitive Admission", "means an admission booked 24+ hours ahead where the physician has certified the condition as time-sensitive."),
    y=("Physician certification", "The referral letter contains no time-sensitivity certification.",
       "The referring physician signed a time-sensitivity certification on the referral."),
    surface=['The hospital\'s pre-admission form labels the stay "{w}".',
             'The member\'s portal message describes it as "{w}".'],
    dir="over", unit="days", unit_rule="days", alts=[("hours", F(1, 24)), ("weeks", F(7))], limits=[2, 3, 5, 7, 10, 14],
    cond="notice of the {T} reaches the Plan {CMP} after the admission date",
    q=("Notification timing", "The Plan received notice of the admission {Q} after the admission date."),
    rule_title="Prior notification", trig="benefits for that admission are denied",
    neg="benefits are not denied for late notification",
    sub=("Maternity Admission", "Maternity Admissions", "The admission was for a planned caesarean delivery (a Maternity Admission).",
         "The admission was for a knee replacement, not a Maternity Admission.", "Admission type"),
    c1=("the member was physically or mentally unable to give notice",
        "The member was sedated and unable to give notice for most of the stay.",
        "The member was alert and able to communicate throughout.", "Member capacity"),
    c2=("an authorised representative named on the membership record was available to give notice",
        "The member's spouse, named as authorised representative, was at the hospital throughout.",
        "No authorised representative is named on the membership record.", "Representative"),
    gate=("coverage has been continuous for {CMP} before the admission", "days", [30, 60, 90], "over",
          "Continuous coverage", "Coverage had been continuous for {G} days before the admission."),
    ev=("Admission date", "Claim received", "admissions", "claims received", True),
    scheme="pay", amt=dict(A=(3000, 60000, 25), d=[250, 500, 750], keep=[50, 70, 80]),
    fa=("Allowed amount", "The allowed amount for the stay is {A}."), fd=("Member copay", "The member's inpatient copay is {d}."),
    out=dict(NOTRIG="Pay the claim: {amt}", TRIG="Deny benefits for the admission under {sec}",
             TRIG_NEW="Pay at {keep}%: {amt}", INELIG="Deny: waiting period under {gsec} not satisfied"),
    am_out="Instead of denial under {ref}, benefits are paid at {keep}% of the allowed amount after the copay.",
    fdefs=[("Allowed Amount", "means the maximum amount the Plan pays for a covered service."),
           ("Network Provider", "means a provider under contract with the Plan."),
           ("Plan Year", "means the 12-month period beginning January 1.")],
    fsecs=[("Out-of-network care", "Services from non-network providers are paid at 60% of the Allowed Amount."),
           ("Pharmacy", "Specialty drugs are limited to a 30-day supply at retail pharmacies."),
           ("Appeals", "A member may appeal an adverse determination within 180 days of receiving it."),
           ("Coordination of benefits", "Where another plan is primary, this Plan pays the balance up to its normal benefit.")],
    noise=[("Hospital", "St. Brendan Regional"), ("Length of stay", "4 nights"), ("Diagnosis code", "M17.11"),
           ("Network status", "In-network")],
)

domain(
    key="saas_sla", polarity="charge",
    orgs=["Stratus Ledger Inc.", "Beaconfield Software", "Quillon Cloud", "Parapet Data Services"],
    docs=["Service Level Agreement SLA-{n}", "Master Subscription Agreement, Schedule {n}", "Uptime Commitment (v{n})"],
    case="credit request", cid="INC", approver="customer success lead", juniors=["support engineer (tier 1)", "new account coordinator", "billing intern"],
    A=("Full Outage", "means a period, other than Scheduled Maintenance, in which the Service is unavailable to all of Customer's users."),
    B=("Partial Outage", "means a period, other than Scheduled Maintenance, in which the Service is unavailable to some but not all users."),
    y=("Scope", "Every user in the customer's tenant was unable to log in.",
       "About 30% of the customer's users were affected; the rest worked normally."),
    surface=['The status page headline read "{w}".', 'The customer\'s ticket subject line says "{w} - urgent".'],
    dir="over", unit="minutes", unit_rule="minutes", alts=[("hours", F(60))], limits=[30, 45, 60, 90, 120, 240],
    cond="a {T} lasts {CMP}",
    q=("Incident duration", "The incident lasted {Q} from first alert to resolution."),
    rule_title="Service credits", trig="Customer receives a Service Credit of {p0}% of that month's fee",
    neg="no Service Credit is due",
    sub=("Enterprise Plus subscription", "Enterprise Plus subscriptions", "The customer is on the Enterprise Plus plan.",
         "The customer is on the Business plan.", "Plan"),
    c1=("the incident was caused by a configuration change made by Customer",
        "The incident started when the customer's admin pushed an SSO configuration change.",
        "The incident was caused by a failed database migration on the provider's side.", "Root cause"),
    c2=("Provider failed to post the incident on its status page within 30 minutes",
        "The provider did not post the incident on its status page until two hours in.",
        "The provider posted the incident on its status page within 10 minutes.", "Status page"),
    ev=("Incident date", "Credit request submitted", "incidents occurring", "credit requests submitted", True),
    scheme="charge", amt=dict(A=(2000, 60000, 100), p0=[10, 15, 25], p1=[20, 30, 50]),
    fa=("Monthly fee", "The customer's monthly subscription fee is {A}."), fd=None,
    out=dict(TRIG="Issue a service credit of {amt}", TRIG_NEW="Issue a service credit of {amt}",
             NOTRIG="No service credit is owed"),
    am_out="The Service Credit under {ref} is {p1}% of the monthly fee (previously {p0}%).",
    fdefs=[("Scheduled Maintenance", "means maintenance announced at least 72 hours in advance."),
           ("Tenant", "means Customer's logically separated instance of the Service."),
           ("Monthly Fee", "means the subscription fee invoiced for the affected month.")],
    fsecs=[("Support hours", "Priority 1 tickets are answered 24x7; other tickets during business hours."),
           ("Data export", "Customer may export its data at any time in CSV or JSON format."),
           ("Suspension", "Provider may suspend accounts more than 30 days overdue."),
           ("Beta features", "Beta features are excluded from all service levels.")],
    noise=[("Region", "eu-west"), ("Seats", "340"), ("Severity", "SEV-1"), ("Postmortem", "Published")],
)

domain(
    key="tuition_residency", polarity="charge",
    orgs=["Westmark State University", "Colbrook College", "University of the Eastern Plains", "Halden Institute of Technology"],
    docs=["Residency Classification Regulations (Ed. {n})", "Tuition and Fees Policy TF-{n}", "Registrar's Manual, Chapter {n}"],
    case="classification request", cid="RES", approver="residency officer", juniors=["admissions intern", "student worker at the front desk", "new admissions counsellor"],
    A=("Domiciled Resident", "means a person present in the State whose primary purpose is not to attend an educational institution."),
    B=("Student Sojourner", "means a person present in the State whose primary purpose is to attend an educational institution."),
    y=("Purpose of move", "She moved to the State for a full-time nursing job and enrolled later.",
       "She moved to the State to enrol and has worked only part-time on campus."),
    surface=['Her application form ticks "{w}".', 'The admissions counsellor\'s email calls her a "{w}".'],
    dir="over", unit="months", unit_rule="months before the census date", alts=[("years", F(12))], limits=[12, 18, 24],
    cond="a {T} has lived in the State for {CMP}",
    q=("Time in State", "She had lived in the State for {Q} before the census date."),
    rule_title="Tuition classification", trig="the student is billed at the in-state rate of {r0} per credit",
    neg="no student is billed at the in-state rate",
    else_txt="All other students are billed at the out-of-state rate of {ralt} per credit.",
    sub=("Graduate Student", "Graduate Students", "She is enrolling in a graduate (MSc) programme.",
         "She is enrolling as an undergraduate.", "Level"),
    c1=("the student holds a tuition scholarship funded by another state's government",
        "She holds a tuition scholarship funded by a neighbouring state's government.",
        "She receives no government-funded scholarship.", "Scholarship"),
    c2=("the student is a dependant of an active-duty service member stationed in the State",
        "Her father is an active-duty service member stationed in the State.",
        "No member of her family serves in the military.", "Military connection"),
    ev=("Census date of the term", "Application submitted", "terms with a census date", "applications submitted", False),
    scheme="rate", amt=dict(n=(9, 18), r0=[310, 350, 420], ralt=[890, 960, 1120], r1=[20, 35, 50]),
    fa=("Credits", "She is registered for {n} credits."), fd=None,
    out=dict(TRIG="Bill at the in-state rate: {amt}", TRIG_NEW="Bill at the in-state rate: {amt}",
             NOTRIG="Bill at the out-of-state rate: {amt}"),
    am_out="The in-state rate under {ref} is {r1} per credit (replacing {r0}).",
    fdefs=[("Census Date", "means the date on which enrolment is counted for the term."),
           ("Credit", "means one semester credit hour."), ("State", "means the State of Westmark.")],
    fsecs=[("Late registration", "Registration after the first week incurs a $75 late fee."),
           ("Refunds", "Tuition is refunded in full for courses dropped before the Census Date."),
           ("Payment plans", "Tuition may be paid in three instalments."),
           ("Transcripts", "Official transcripts cost $12 each.")],
    noise=[("Programme", "Health Sciences"), ("Housing", "Off-campus"), ("Age", "24"), ("FAFSA", "Filed")],
)

domain(
    key="travel_per_diem", polarity="charge",
    orgs=["Orrin & Blake Consulting", "Galvanic Engineering Ltd", "Pinecrest Health Systems", "Tessellate Media"],
    docs=["Travel and Expense Policy TE-{n}", "Business Travel Rules (v{n})", "Finance Manual, Section {n}: Travel"],
    case="expense report", cid="EXP", approver="expense approver", juniors=["finance intern", "travel desk assistant", "new AP clerk"],
    A=("Overnight Travel", "means business travel outside the Home Area that includes at least one overnight stay."),
    B=("Day Travel", "means business travel outside the Home Area that begins and ends on the same day."),
    y=("Overnight stay", "The traveller stayed at a hotel near the client site.", "The traveller drove home each evening."),
    surface=['The expense report\'s trip-type field says "{w}".', 'The travel booking was entered as "{w}".'],
    dir="over", unit="km", unit_rule="km", alts=[("miles", F(1609344, 1000000))], limits=[80, 100, 150, 200],
    cond="an employee on {T} works at a destination {CMP} from the Home Office",
    q=("Distance", "The client site is {Q} from the traveller's Home Office by road."),
    rule_title="Daily allowance", trig="the employee receives a daily allowance of {r0} per travel day",
    neg="no daily allowance is paid",
    else_txt="In all other cases a flat meal allowance of {ralt} per travel day applies.",
    sub=("Rail Trip", "Rail Trips", "The trip was made entirely by train.", "The trip was made by company car.", "Mode"),
    c1=("the client provided all meals free of charge", "The client's contract provided full board for every travel day.",
        "Meals were not provided by the client.", "Meals"),
    c2=("HR booked the trip as a Mandatory Training Trip", "HR booked the trip as a Mandatory Training Trip.",
        "The trip was a client visit booked by the team.", "Trip category"),
    gate=("the trip was pre-approved {CMP} before departure", "days", [3, 5, 7, 10], "over",
          "Pre-approval", "The trip was pre-approved {G} days before departure."),
    ev=("Trip start date", "Report submitted", "trips starting", "reports submitted", True),
    scheme="rate", amt=dict(n=(2, 6), r0=[55, 64, 72, 85], ralt=[18, 22, 25], r1=[4, 6, 8]),
    fa=("Travel days", "The trip lasted {n} travel days."), fd=None,
    out=dict(TRIG="Pay a daily allowance totalling {amt}", TRIG_NEW="Pay a daily allowance totalling {amt}",
             NOTRIG="Pay only the flat meal allowance totalling {amt}", INELIG="Reject the report: pre-approval rule in {gsec} not met"),
    am_out="The daily allowance under {ref} is {r1} per travel day (replacing {r0}).",
    fdefs=[("Home Area", "means the city in which the employee's Home Office is located."),
           ("Home Office", "means the office to which the employee is contractually assigned."),
           ("Travel Day", "means a calendar day on which the employee is travelling on business.")],
    fsecs=[("Class of travel", "Economy class is required for flights under six hours."),
           ("Mileage", "Private car use is reimbursed at the published mileage rate."),
           ("Alcohol", "Alcohol is not reimbursable."), ("Corporate card", "Cardholders must reconcile statements monthly.")],
    noise=[("Cost centre", "4410"), ("Client", "Brightwater Utilities"), ("Booking reference", "TRV-2231"),
           ("Approver on leave", "Delegated to deputy")],
)

domain(
    key="retail_returns", polarity="restrict",
    orgs=["Brightcart Stores", "Hollis Electronics", "Marlow & Finch Home", "UrbanNest Retail"],
    docs=["Returns and Refunds Policy (v{n})", "Customer Terms of Sale, Part {n}", "Store Operations Manual RR-{n}"],
    case="return", cid="RMA", approver="store manager", juniors=["weekend sales associate", "seasonal cashier", "new customer-service agent"],
    A=("Used Item", "means a returned product whose packaging has been opened and that shows signs of use."),
    B=("Opened Item", "means a returned product whose packaging has been opened but that shows no signs of use."),
    y=("Condition", "The returns inspection found clear signs of use (scratches and wear).",
       "The returns inspection found no signs of use; protective films were still in place."),
    surface=['The associate typed "{w}" in the return-reason field.', 'The customer\'s chat message calls it "{w}".'],
    dir="over", unit="days", unit_rule="days", alts=[("weeks", F(7))], limits=[14, 15, 30, 45],
    cond="any {T} is returned {CMP} after delivery",
    q=("Return timing", "The item came back {Q} after it was delivered."),
    rule_title="Returns and refunds", trig="no refund is given",
    neg="a refund is not refused under this clause",
    sub=("Large Appliance", "Large Appliances", "The item is a washing machine (a Large Appliance).",
         "The item is a pair of headphones.", "Category"),
    c1=("the customer is a Premier Member", "The customer is a Premier Member.",
        "The customer is not enrolled in the Premier programme.", "Membership"),
    c2=("the item was bought during a Clearance Event", "The item was bought during the January Clearance Event.",
        "The item was bought at the regular price.", "Purchase type"),
    ev=("Delivery date", "Order placed", "purchases delivered", "orders placed", False),
    scheme="pay", amt=dict(A=(40, 2500, 1), d=[10, 15, 25], keep=[50, 70, 80]),
    fa=("Price paid", "The customer paid {A}."), fd=("Restocking fee", "The restocking fee for opened packaging is {d}."),
    out=dict(NOTRIG="Refund {amt}", TRIG="Refuse the refund under {sec}", TRIG_NEW="Refund {keep}%: {amt}"),
    am_out="An item that would be refused under {ref} is refunded at {keep}% of the price less the restocking fee.",
    fdefs=[("Delivery", "means the date shown on the carrier's proof of delivery."),
           ("Proof of Purchase", "means an original receipt or order confirmation."),
           ("Premier Member", "means a customer enrolled in the paid Premier programme.")],
    fsecs=[("Gift cards", "Gift cards are not refundable or exchangeable for cash."),
           ("Price match", "We match a competitor's advertised price within 7 days of purchase."),
           ("Warranty", "Manufacturer warranties are handled directly by the manufacturer."),
           ("Personalised goods", "Engraved or personalised goods cannot be returned unless faulty.")],
    noise=[("Order channel", "Online, home delivery"), ("Payment method", "Credit card"),
           ("Loyalty points used", "None"), ("Receipt", "Order confirmation email")],
)

domain(
    key="privacy_breach", polarity="none",
    orgs=["Veridian Payments Ltd", "Clearwell Telecom", "Hartmoor Clinics Group", "Solace Insurance Services"],
    docs=["Data Protection Policy DP-{n}", "Incident Response Standard (v{n})", "Privacy Governance Manual, Chapter {n}"],
    case="incident", cid="SEC", approver="Data Protection Officer", juniors=["security analyst intern", "helpdesk technician", "new compliance associate"],
    A=("Personal Data Breach", "means unauthorised access to personal data that was readable, i.e. not protected by encryption with a secure key."),
    B=("Contained Incident", "means unauthorised access to personal data protected by encryption whose key remained secure."),
    y=("Encryption", "The exported files were plain-text CSVs.",
       "The files were AES-256 encrypted and the key sat in a separate HSM that was not accessed."),
    surface=['The SOC ticket is titled "{w}".', 'The first internal alert email said "{w} detected".'],
    dir="over", unit="data subjects", unit_rule="data subjects", alts=[], limits=[100, 250, 500, 1000],
    cond="a {T} affects {CMP}",
    q=("Scope", "Forensics confirmed that {Q} were affected."),
    rule_title="Regulator notification", trig="the Company must notify the Supervisory Authority within 72 hours",
    neg="no notification to the Supervisory Authority is required",
    sub=("Health Data incident", "incidents involving Health Data", "The files included patients' medication lists (Health Data).",
         "The files contained names and email addresses only.", "Data categories"),
    c1=("the recipient was a Group company bound by the intra-group data agreement",
        "The files were sent by mistake to a sister company bound by the intra-group data agreement.",
        "The files were downloaded by an unknown external IP address.", "Recipient"),
    c2=("the incident has been reported in the media", "A trade blog has already published a story about the incident.",
        "There has been no media coverage.", "Media"),
    ev=("Incident detected", "Assessment completed", "incidents detected", "assessments completed", True),
    scheme="none", amt=dict(), fa=None, fd=None,
    out=dict(NOTRIG="Record the incident internally; no notification", TRIG="Notify the Supervisory Authority within 72 hours",
             TRIG_NEW="Notify the Supervisory Authority and the affected data subjects"),
    am_out="Where notification is required under {ref}, the affected data subjects must also be notified without undue delay.",
    fdefs=[("Personal Data", "means information relating to an identified or identifiable natural person."),
           ("Supervisory Authority", "means the national data protection regulator."),
           ("Group", "means the Company and its subsidiaries.")],
    fsecs=[("Retention", "Customer records are retained for seven years after account closure."),
           ("Access requests", "Subject access requests are answered within one month."),
           ("Training", "All staff complete privacy training annually."),
           ("Vendors", "Processors must sign the standard data processing agreement.")],
    noise=[("Detected by", "SIEM alert"), ("System", "CRM export job"), ("Ticket priority", "P2"),
           ("Containment", "Credentials rotated within 3 hours")],
)

domain(
    key="manufacturing_qa", polarity="none",
    orgs=["Kestrel Components GmbH", "Axial Motion Parts", "Brennan Fasteners", "Lumen Castings Ltd"],
    docs=["Supplier Quality Manual SQM-{n}", "Incoming Inspection Procedure QP-{n}", "Quality Agreement (Rev. {n})"],
    case="lot", cid="LOT", approver="quality engineer", juniors=["receiving inspector (trainee)", "line supervisor", "quality co-op student"],
    A=("Critical Nonconformity", "means a nonconformity that impairs the part's function and creates a safety hazard."),
    B=("Major Nonconformity", "means a nonconformity that impairs the part's function without creating a safety hazard."),
    y=("Hazard assessment", "Engineering classified the cracked brackets as a potential fall hazard.",
       "Engineering found the misaligned holes affect fit only; there is no safety hazard."),
    surface=['The line supervisor\'s hold tag reads "{w}".', 'The supplier\'s 8D report calls the defect a "{w}".'],
    dir="over", unit="ppm", unit_rule="ppm", alts=[("percent", F(10000))], limits=[500, 1000, 1500, 2500, 5000],
    cond="the rate of parts with a {T} is {CMP}",
    q=("Defect rate", "Receiving inspection found this nonconformity at a rate of {Q}."),
    rule_title="Lot disposition", trig="the lot is rejected and returned to the supplier",
    neg="no lot is rejected under this provision",
    sub=("Safety-Critical part", "parts on the Safety-Critical List", "The part number is on the Safety-Critical List.",
         "The part number is not on the Safety-Critical List.", "Part classification"),
    c1=("the customer has issued a written deviation permit for the lot",
        "The customer issued written deviation permit DP-77 covering this lot.",
        "No deviation permit has been issued.", "Deviation"),
    c2=("the supplier is on Probation status", "The supplier was placed on Probation status last quarter.",
        "The supplier is in good standing.", "Supplier status"),
    ev=("Lot received", "Inspection completed", "lots received", "inspections completed", True),
    scheme="none", amt=dict(), fa=None, fd=None,
    out=dict(NOTRIG="Release the lot", TRIG="Reject the lot and return it to the supplier",
             TRIG_NEW="Release the lot only after 100% sorting at the supplier's cost"),
    am_out="Instead of rejection under {ref}, the lot is released only after 100% sorting at the supplier's cost.",
    fdefs=[("Lot", "means a quantity of parts delivered under one lot number."),
           ("ppm", "means defective parts per million parts inspected."),
           ("Deviation Permit", "means written permission to accept product that departs from specification.")],
    fsecs=[("Packaging", "Parts must be delivered in returnable totes labelled with lot and part number."),
           ("PPAP", "New part numbers require PPAP level 3 approval before series delivery."),
           ("Calibration", "Gauges must be calibrated at intervals not exceeding 12 months."),
           ("Traceability", "Suppliers retain lot records for 15 years.")],
    noise=[("Lot size", "12,000 pcs"), ("Sample size", "800 pcs"), ("Part", "Bracket, zinc-plated"),
           ("Shift", "Second shift")],
)

domain(
    key="benefits_student", polarity="restrict",
    orgs=["Ashford County Social Services", "Department of Family Assistance", "Riverside Human Services Agency", "Tri-County Benefits Office"],
    docs=["Food Assistance Eligibility Manual, Chapter {n}", "Program Policy Handbook PPH-{n}", "Benefit Rules Bulletin No. {n}"],
    case="application", cid="APP", approver="eligibility supervisor", juniors=["caseworker trainee", "front-desk volunteer", "new intake worker"],
    A=("Full-Time Student", "means a person enrolled in higher education for 12 or more credit hours."),
    B=("Part-Time Student", "means a person enrolled in higher education for fewer than 12 credit hours."),
    y=("Enrolment", "She is enrolled for 13 credit hours this term.", "She is enrolled for 9 credit hours this term."),
    surface=['She described herself as a "{w}" on the application.', 'The caseworker\'s intake summary says "{w}".'],
    dir="under", unit="hours per week", unit_rule="hours of paid work per week", alts=[("hours per fortnight", F(1, 2))],
    limits=[15, 20, 25],
    cond="a {T} averages {CMP}",
    q=("Work hours", "Her payslips show she averages {Q} of paid work."),
    rule_title="Student eligibility", trig="the student is ineligible for benefits",
    neg="no student is ineligible under this provision",
    sub=("Student Parent", "Student Parents", "She is the sole parent of a 4-year-old child.", "She has no children.", "Dependants"),
    c1=("the student is enrolled in an approved Employment and Training programme",
        "Her course is an approved Employment and Training programme.",
        "Her course is not an approved Employment and Training programme.", "Programme"),
    c2=("the student has already received 36 months of benefits as a student",
        "She has already received benefits as a student for 36 months.",
        "This is her first application as a student.", "Prior benefits"),
    gate=("the applicant has lived in the County for {CMP} before applying", "days", [30, 60, 90], "over",
          "Residence", "She had lived in the County for {G} days when she applied."),
    ev=("Application date", "Interview date", "applications filed", "interviews held", True),
    scheme="pay", amt=dict(A=(200, 900, 1), d=[30, 45, 60], keep=[50, 60, 75]),
    fa=("Monthly allotment", "The standard allotment for her household size is {A} per month."),
    fd=("Earned-income deduction", "Her earned-income deduction is {d} per month."),
    out=dict(NOTRIG="Approve a monthly benefit of {amt}", TRIG="Deny the application under {sec}",
             TRIG_NEW="Approve {keep}% of the benefit: {amt} per month", INELIG="Deny: residence requirement in {gsec} not met"),
    am_out="Instead of ineligibility under {ref}, the student receives {keep}% of the benefit otherwise payable.",
    fdefs=[("Household", "means persons who live together and buy and prepare food together."),
           ("Certification Period", "means the months for which eligibility is approved."),
           ("County", "means Ashford County.")],
    fsecs=[("Reporting changes", "Households must report income changes over $100 within 10 days."),
           ("Interviews", "An interview is required at application and recertification."),
           ("Overpayments", "Overpayments are recovered by reducing future benefits by 10%."),
           ("Fair hearings", "Applicants may request a fair hearing within 90 days of a decision.")],
    noise=[("Utilities", "Included in rent"), ("Vehicle", "One car, 2012"), ("Rent", "$780 per month"), ("Language", "English")],
)


# =========================================================================== engine
def fact_step(f):
    if f == 60:
        return F(1, 4)
    if f == 10000:
        return F(1, 100)
    if f == 12:
        return F(1, 2)
    return F(1)


def finite_dec(x):
    d = F(x).denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return d == 1


def active_amends(P, m):
    """Endorsements that govern the case (chronological), under mistake set m."""
    if not P["amends"] or "old_rule" in m:
        return []
    use_event = (P["basis"] == "event") != ("date_basis" in m)
    b = P["E"] if use_event else P["R"]
    out = []
    for a in P["amends"]:
        inc = a["incl"] != ("amend_boundary" in m)
        if "retro" in m or (b >= a["date"] if inc else b > a["date"]):
            out.append(a)
    if "first_amend" in m and len(out) > 1:
        out = out[:1]
    return out


def limit_of(P, m, act):
    gen, spec = P["L_old"], P.get("L_spec")
    for a in act:
        if a["mode"] == "limit":
            if a["target"] == "general":
                gen = a["new"]
            else:
                spec = a["new"]
    if P["spec_on"] and P["is_sub"] and "general" not in m:
        return spec
    return gen


def amount(P, kind, m):
    s = P["scheme"]
    if s == "pay":
        base = F(P["A"]) - (0 if "deductible" in m else P["d"])
        if kind == "NOTRIG":
            return base
        if kind == "TRIG_NEW":
            if "order" in m:
                return F(P["A"]) * P["keep"] / 100 - (0 if "deductible" in m else P["d"])
            return base * P["keep"] / 100
        return None
    if s == "charge":
        if kind == "TRIG":
            return F(P["A"]) * P["p0"] / 100
        if kind == "TRIG_NEW":
            return F(P["A"]) * P["p1"] / 100
        return None
    if s == "rate":
        if kind == "TRIG":
            return F(P["n"] * P["r0"])
        if kind == "TRIG_NEW":
            return F(P["n"] * P["r1"])
        if kind == "NOTRIG":
            return F(P["n"] * P["ralt"])
    return None


def solve(P, m=frozenset()):
    """Primary rule engine. m = set of mistake names to simulate."""
    if P["gate_on"] and "ignore_gate" not in m:
        inc = P["gincl"] != ("gate_boundary" in m)
        if not hit(P["gval"], P["gmin"], inc, P["gdir"]):
            return ("INELIG", None)
    act = active_amends(P, m)
    L = limit_of(P, m, act)
    q = F(P["q_f"]) if "unit" in m else F(P["q_f"]) * P["factor"]
    inc = P["incl"] != ("boundary" in m)
    exceeded = hit(q, L, inc, P["dir"])
    holds = P["term_holds"] != ("term" in m)
    trig = holds and exceeded
    if trig and P["exc_on"] and P["C1"] and "no_exception" not in m:
        blocked = True
        if P["excexc_on"] and P["C2"] and "no_exc_exc" not in m:
            blocked = False
        if any(a["mode"] == "drop_exc" for a in act):
            blocked = False
        if blocked:
            trig = False
    if trig:
        kind = "TRIG_NEW" if any(a["mode"] == "outcome" for a in act) else "TRIG"
    else:
        kind = "NOTRIG"
    return (kind, amount(P, kind, m))


def solve2(P):
    """Independent evaluator: ordinal dates, latest-first scan, integer cross-multiplication,
    one boolean formula, Decimal money.  Returns (kind, money-string-or-None)."""
    if P["gate_on"]:
        s = (P["gval"] > P["gmin"]) - (P["gval"] < P["gmin"])
        ok = (s > 0 or (s == 0 and P["gincl"])) if P["gdir"] == "over" else (s < 0 or (s == 0 and P["gincl"]))
        if not ok:
            return ("INELIG", None)
    b = (P["E"] if P["basis"] == "event" else P["R"]).toordinal()
    app = [a for a in P["amends"] if b - a["date"].toordinal() >= (0 if a["incl"] else 1)]
    lims = sorted([a for a in app if a["mode"] == "limit"], key=lambda a: a["date"].toordinal(), reverse=True)
    lg, ls = P["L_old"], P.get("L_spec")
    if lims:
        if lims[0]["target"] == "general":
            lg = lims[0]["new"]
        else:
            ls = lims[0]["new"]
    L = F(ls if (P["spec_on"] and P["is_sub"]) else lg)
    qf, f = F(P["q_f"]), F(P["factor"])
    diff = qf.numerator * f.numerator * L.denominator - L.numerator * qf.denominator * f.denominator
    if P["dir"] == "over":
        hv = diff > 0 or (diff == 0 and P["incl"])
    else:
        hv = diff < 0 or (diff == 0 and P["incl"])
    holds = (P["Y"] is True) == (P["term_ref"] == "A")
    blocked = bool(P["exc_on"] and P["C1"] and not (P["excexc_on"] and P["C2"])
                   and not [a for a in app if a["mode"] == "drop_exc"])
    trig = holds and hv and not blocked
    kind = ("TRIG_NEW" if [a for a in app if a["mode"] == "outcome"] else "TRIG") if trig else "NOTRIG"
    s, amt = P["scheme"], None
    dec = lambda x: Decimal(F(x).numerator) / Decimal(F(x).denominator)
    if s == "pay":
        base = dec(P["A"]) - dec(P["d"])
        amt = base if kind == "NOTRIG" else (base * dec(P["keep"]) / Decimal(100) if kind == "TRIG_NEW" else None)
    elif s == "charge":
        amt = {"TRIG": dec(P["A"]) * P["p0"] / Decimal(100),
               "TRIG_NEW": dec(P["A"]) * P["p1"] / Decimal(100)}.get(kind)
    elif s == "rate":
        amt = Decimal(P["n"]) * {"TRIG": P["r0"], "TRIG_NEW": P["r1"], "NOTRIG": P["ralt"]}[kind]
    if amt is not None:
        amt = "$" + "{:,.2f}".format(amt.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    return (kind, amt)


def relevant_mistakes(P):
    ms = ["boundary"]
    if P["trap_term"]:
        ms.append("term")
    if P["factor"] != 1:
        ms.append("unit")
    if P["amends"]:
        ms += ["amend_boundary", "date_basis", "old_rule", "retro"]
    if len(P["amends"]) > 1:
        ms.append("first_amend")
    if P["spec_on"] and P["is_sub"]:
        ms.append("general")
    if P["exc_on"]:
        ms.append("no_exception")
    if P["excexc_on"]:
        ms.append("no_exc_exc")
    if P["scheme"] == "pay":
        ms.append("deductible")
        if any(a["mode"] == "outcome" for a in P["amends"]):
            ms.append("order")
    if P["gate_on"]:
        ms += ["gate_boundary", "ignore_gate"]
    return ms


# =========================================================================== sampling
def _new_limit(rng, D, used):
    c = [x for x in D["limits"] if x not in used]
    if c:
        return pick(rng, c)
    for _ in range(50):
        base = pick(rng, D["limits"])
        x = base + pick(rng, [-3, -2, 2, 3, 5, 10])
        if x > 1 and x not in used:
            return x
    raise Retry("no limit")


def _q_candidates(G, f, lo, hi, strict_lo, strict_hi):
    """Fact-unit values q_f (multiples of step) whose policy value q_f*f lies in the range."""
    st = fact_step(f)
    unit = st * f
    k0 = int((F(lo) / unit)) - 1
    k1 = int((F(hi) / unit)) + 2
    out = []
    for k in range(max(1, k0), k1 + 1):
        qf = st * k
        qp = qf * f
        if (qp > lo if strict_lo else qp >= lo) and (qp < hi if strict_hi else qp <= hi):
            if finite_dec(qf):
                out.append(qf)
        if len(out) > 400:
            break
    return out


def sample_params(rng, D, size):
    short = size == "short"
    P = {"dom": D, "scheme": D["scheme"], "dir": D["dir"]}
    probs = {"amend": .75, "exc": .6, "spec": .35, "unit": .5, "gate": .3}
    layers = [k for k in ["amend", "exc", "spec", "unit", "gate"] if rng.random() < probs[k]]
    if not D["alts"] and "unit" in layers:
        layers.remove("unit")
    if D["gate"] is None and "gate" in layers:
        layers.remove("gate")
    if short:
        rng.shuffle(layers)
        layers.sort(key=lambda k: k == "amend" and rng.random() < .6)
        layers = layers[:pick(rng, [0, 1, 1, 1])]
    P["layers"] = layers
    P["trap_term"] = rng.random() < .85
    P["term_ref"] = "A" if D["key"] in REF_ONLY_A else pick(rng, ["A", "B"])
    P["Y"] = rng.random() < .5
    P["term_holds"] = P["Y"] if P["term_ref"] == "A" else (not P["Y"])
    P["incl"] = rng.random() < .5
    # --- exceptions / class-specific / gate
    P["exc_on"] = "exc" in layers
    P["C1"] = P["exc_on"] and rng.random() < .65
    P["excexc_on"] = P["exc_on"] and rng.random() < (.45 if short else .65)
    P["C2"] = P["excexc_on"] and rng.random() < .5
    P["spec_on"] = "spec" in layers
    P["is_sub"] = P["spec_on"] and rng.random() < .7
    used = []
    P["L_old"] = _new_limit(rng, D, used)
    used.append(P["L_old"])
    if P["spec_on"]:
        P["L_spec"] = _new_limit(rng, D, used)
        used.append(P["L_spec"])
    P["gate_on"] = "gate" in layers
    if P["gate_on"]:
        gc, gu, gl, gd, glab, gfact = D["gate"]
        P["gmin"], P["gincl"], P["gdir"] = pick(rng, gl), rng.random() < .5, gd
        want_pass = rng.random() < .7
        if rng.random() < .4:
            P["gval"] = P["gmin"]
        else:
            cands = [P["gmin"] + k for k in range(-max(2, P["gmin"] // 3), max(2, P["gmin"] // 3) + 1) if k and P["gmin"] + k > 0]
            good = [g for g in cands if hit(g, P["gmin"], P["gincl"], gd) == want_pass]
            P["gval"] = pick(rng, good or cands)
    # --- amendments and dates
    base = dt.date(2025, 1, 1) + dt.timedelta(days=rng.randrange(0, 900))
    P["amends"] = []
    if "amend" in layers:
        modes = ["limit", "limit", "limit", "outcome", "outcome"] + (["drop_exc", "drop_exc"] if P["exc_on"] else [])
        mode = pick(rng, modes)
        target = "specific" if (P["spec_on"] and rng.random() < .5) else "general"

        def mk_amend(md, date, k):
            a = {"date": date, "incl": rng.random() < .5, "mode": md, "k": k}
            if md == "limit":
                a["target"] = target
                a["new"] = _new_limit(rng, D, used)
                used.append(a["new"])
            return a
        a1 = mk_amend(mode, base, rng.randrange(2, 9))
        P["amends"].append(a1)
        if not short and rng.random() < .4:
            if mode == "limit":
                m2 = pick(rng, ["limit", "limit", "outcome"] + (["drop_exc"] if P["exc_on"] else []))
            else:
                m2 = "limit"
            P["amends"].append(mk_amend(m2, base + dt.timedelta(days=rng.randrange(45, 300)), a1["k"] + rng.randrange(1, 4)))
    P["basis"] = pick(rng, ["event", "event", "other"])
    ds = [a["date"] for a in P["amends"]]
    other_after = D["ev"][4]
    if ds:
        r = rng.random()
        anchor = pick(rng, ds)
        if r < .3:
            b = anchor
        elif r < .65:
            b = anchor + dt.timedelta(days=rng.randrange(1, 40))
        else:
            b = anchor - dt.timedelta(days=rng.randrange(1, 40))
    else:
        b = base + dt.timedelta(days=rng.randrange(0, 60))
    # the non-basis date lies later (s=+1) or earlier (s=-1) than the basis date
    s = 1 if ((P["basis"] == "event") == other_after) else -1
    lag = rng.randrange(1, 40)
    if ds and rng.random() < .5:
        if s == 1:
            later = [d for d in ds if d > b]
            if later:
                lag = (min(later) - b).days + rng.randrange(0, 4)
        else:
            earlier = [d for d in ds if d <= b]
            if earlier:
                lag = (b - max(earlier)).days + 1 + rng.randrange(0, 4)
    lag = max(1, min(lag, 75))
    nb = b + dt.timedelta(days=s * lag)
    if P["basis"] == "event":
        P["E"], P["R"] = b, nb
    else:
        P["R"], P["E"] = b, nb
    # --- quantity: choose governing limit G and rivals, then q
    G = limit_of(P, frozenset(), active_amends(P, frozenset()))
    rivals = set()
    for mk in ["old_rule", "retro", "date_basis", "amend_boundary", "first_amend", "general"]:
        rivals.add(limit_of(P, {mk}, active_amends(P, {mk})))
    rivals.discard(G)
    rivals = sorted(rivals)
    P["unit_f"], P["factor"] = D["unit"], F(1)
    if "unit" in layers:
        P["unit_f"], P["factor"] = pick(rng, D["alts"])
    f = P["factor"]
    modes = ["boundary", "rival", "free"]
    w = [.35, .45 if rivals else 0, .3]
    cands = []
    for _ in range(4):
        md = rng.choices(modes, weights=w)[0]
        if md == "boundary":
            cands = _q_candidates(G, f, G, G, False, False)
        elif md == "rival":
            R = pick(rng, rivals)
            cands = _q_candidates(G, f, min(G, R), max(G, R), True, True)
        else:
            wd = max(2, (G * 35) // 100)
            cands = [c for c in _q_candidates(G, f, max(1, G - wd), G + wd, False, False) if c * f != G]
        if cands:
            break
    if not cands:
        raise Retry("no q")
    if f != 1 and rng.random() < .7:
        flip = [c for c in cands if hit(c, G, P["incl"], P["dir"]) != hit(c * f, G, P["incl"], P["dir"])]
        cands = flip or cands
    P["q_f"] = pick(rng, cands)
    P["G"] = G
    # --- amounts
    a = D["amt"]
    if P["scheme"] == "pay":
        lo, hi, st = a["A"]
        P["A"] = rng.randrange(lo // st, hi // st + 1) * st
        if rng.random() < .3 and st == 1:
            P["A"] = F(rng.randrange(lo * 100, hi * 100), 100)
        P["d"], P["keep"] = pick(rng, a["d"]), pick(rng, a["keep"])
    elif P["scheme"] == "charge":
        lo, hi, st = a["A"]
        P["A"] = rng.randrange(lo // st, hi // st + 1) * st
        P["p0"] = pick(rng, a["p0"])
        P["p1"] = pick(rng, [x for x in a["p1"] if x != P["p0"]])
    elif P["scheme"] == "rate":
        P["n"] = rng.randint(*a["n"])
        P["r0"], P["ralt"] = pick(rng, a["r0"]), pick(rng, a["ralt"])
        P["r1"] = P["r0"] + pick(rng, a["r1"])
    return P


# =========================================================================== rendering
PEOPLE = ["Dana Whitfield", "Ravi Menon", "Lucia Ortega", "Tom Achebe", "Mei Tanaka", "Sven Olsen", "Priya Nair",
          "Grace Kim", "Omar Haddad", "Hannah Weiss", "Kofi Mensah", "Elena Petrova", "Jonas Berg", "Aisha Bello",
          "Marco Rossi", "Chloe Martin", "Diego Alvarez", "Nora Lindqvist", "Sam Carter", "Yuki Sato"]
UNIT_SING = {"days": "day", "weeks": "week", "hours": "hour", "minutes": "minute", "months": "month",
             "years": "year", "miles": "mile", "hours per week": "hour per week",
             "hours per fortnight": "hour per fortnight", "data subjects": "data subject"}
GENERIC_SECS = [
    ("Notices", "Any notice under this document must be in writing and sent to the address last notified. Notices sent by email are deemed received on the next business day after sending."),
    ("Governing law", "This document is governed by the laws of the jurisdiction in which {org} has its registered office, and the courts of that jurisdiction have exclusive jurisdiction."),
    ("Assignment", "No right under this document may be assigned without the prior written consent of {org}; any purported assignment without consent is void."),
    ("Severability", "If any provision is held invalid or unenforceable, the remaining provisions continue in full force and effect."),
    ("Complaints", "Complaints may be raised with the {org} customer relations team. We aim to respond within 15 business days and to resolve most complaints within eight weeks."),
    ("Fraud", "Any {case} that is fraudulent in any respect is void, and {org} may recover any amounts already paid in connection with it."),
    ("Headings", "Headings are included for convenience only and do not affect interpretation. Words in the singular include the plural and vice versa."),
    ("Currency", "All amounts are stated in US dollars unless expressly stated otherwise."),
    ("Records", "{org} keeps records of each {case} for at least seven years and may use anonymised data for statistical purposes."),
    ("Changes to this document", "{org} may change this document only by a written, dated endorsement or amendment. A change takes effect only as stated in the change itself."),
    ("Sanctions", "{org} will not provide any benefit or make any payment that would expose it to a sanction, prohibition or restriction under applicable trade or economic sanctions laws."),
    ("Language", "This document is provided in English; translations are for information only and the English text prevails."),
    ("Waiver", "A failure or delay in exercising any right is not a waiver of that right, and a single exercise of a right does not preclude any further exercise."),
    ("Third parties", "Nothing in this document confers any right on a person who is not a party to it."),
]
GEN_FACTS = [("Assigned handler", "{p}"), ("Channel", "Received via web portal"), ("Priority", "Standard"),
             ("Language preference", "English"), ("Related correspondence", "Two emails, no attachments of note")]


def fmt_q(q, unit):
    if unit == "percent":
        return "%s%%" % fnum(q)
    u = UNIT_SING.get(unit, unit) if F(q) == 1 else unit
    return "%s %s" % (fnum(q), u)


def _def_line(rng, v, term, text):
    if v == 0:
        return '"%s" %s' % (term, text)
    if v == 1:
        return "%s: %s" % (term, cap(text[6:]) if text.startswith("means ") else text)
    return "The term “%s” %s" % (term, text)


def build_doc(rng, P, size, extra):
    D = P["dom"]
    short = size == "short"
    num = Num(rng, short)
    P["_num"] = num
    fsec_pool = [("f", t, x) for t, x in D["fsecs"]] + [("g", t, x) for t, x in GENERIC_SECS]
    rng.shuffle(fsec_pool)
    if short:
        n_fill = 0
    elif size == "medium":
        n_fill = rng.randint(0, 2) + extra
    else:
        n_fill = rng.randint(4, 7) + extra
    fills = fsec_pool[:max(0, min(n_fill, len(fsec_pool)))]
    c2_sep = P["excexc_on"] and not short and rng.random() < .4
    want_prec = (bool(P["amends"]) or P["spec_on"]) and (not short or rng.random() < .25)
    keys = ["defs"] + (["gate"] if P["gate_on"] else []) + ["rule"] + (["exc"] if P["exc_on"] else [])
    for fl in fills:
        keys.insert(rng.randint(1, len(keys)), fl)
    if c2_sep:
        keys.append("gen")
    if want_prec:
        keys.insert(len(keys) if rng.random() < .7 else 1, "prec")
    nums = {}
    for i, k in enumerate(keys):
        if isinstance(k, str):
            nums[k] = i + 1
    ds = rng.randrange(5)
    P["_ds"] = ds
    ur = D["unit_rule"]
    rule_items = 1 + (1 if P["spec_on"] else 0) + (1 if D["else_txt"] else 0)
    R = {}
    R["rule"] = num.ref(nums["rule"], 0) if rule_items > 1 else num.ref(nums["rule"])
    R["spec"] = num.ref(nums["rule"], 1) if P["spec_on"] else None
    exc_items = 1 + (1 if (P["excexc_on"] and not c2_sep) else 0)
    if P["exc_on"]:
        R["exc"] = num.ref(nums["exc"], 0) if exc_items > 1 else num.ref(nums["exc"])
    R["gate"] = num.ref(nums["gate"]) if P["gate_on"] else None
    P["_refs"] = R
    Tw = {"A": D["A"][0], "B": D["B"][0]}
    Tref = Tw[P["term_ref"]]
    vals = dict(p0=P.get("p0"), p1=P.get("p1"), keep=P.get("keep"),
                r0=money(P["r0"]) if "r0" in P else None, r1=money(P["r1"]) if "r1" in P else None,
                ralt=money(P["ralt"]) if "ralt" in P else None)
    trig = D["trig"].format(**vals)
    neg = D["neg"].format(**vals)
    cond = D["cond"].format(T=Tref, CMP=cmp_text(rng, P["dir"], P["incl"], P["L_old"], ur))
    rv = rng.randrange(3)
    main = main_rule(P, rv, cond, trig, neg, vals)
    P["_rule_form"] = rv
    out = []
    for k in keys:
        if isinstance(k, tuple):
            title, txt = k[1], k[2].format(org=P["_org"], case=D["case"])
            out.append((title, [txt]))
            continue
        if k == "defs":
            v = rng.randrange(3)
            items = [(D["A"][0], D["A"][1]), (D["B"][0], D["B"][1])]
            if not short:
                fd = list(D["fdefs"])
                rng.shuffle(fd)
                items += fd[:(rng.randint(0, 2) if size == "medium" else 3)]
            rng.shuffle(items)
            out.append((pick(rng, ["Definitions", "Defined terms", "Interpretation"]),
                        [_def_line(rng, v, t, x) for t, x in items]))
        elif k == "gate":
            gc = D["gate"][0].format(CMP=cmp_text(rng, P["gdir"], P["gincl"], P["gmin"], D["gate"][1]))
            out.append((pick(rng, ["Eligibility", "Conditions precedent", "Qualifying conditions"]),
                        [pick(rng, ["A %s may be considered under this document only if %s." % (D["case"], gc),
                                    "No %s is considered unless %s." % (D["case"], gc)])]))
        elif k == "rule":
            items = [main]
            if P["spec_on"]:
                sp = D["sub"]
                items.append(pick(rng, [
                    "For %s, the figure of %s in %s is read as %s." % (sp[1], fnum(P["L_old"]), R["rule"], fnum(P["L_spec"])),
                    "Where the matter concerns %s, %s applies with %s in place of %s." % (sp[1], R["rule"], fnum(P["L_spec"]), fnum(P["L_old"])),
                    "%s: the threshold in %s is %s instead of %s; all other terms of %s are unchanged." % (cap(sp[1]), R["rule"], fnum(P["L_spec"]), fnum(P["L_old"]), R["rule"])]))
            if D["else_txt"]:
                items.append(D["else_txt"].format(**vals))
            out.append((D["rule_title"], items))
        elif k == "exc":
            c1 = D["c1"][0]
            items = [pick(rng, ["%s does not apply where %s." % (R["rule"], c1),
                                "Where %s, %s shall not apply." % (c1, R["rule"]),
                                "%s is disapplied if %s." % (R["rule"], c1)])]
            if P["excexc_on"] and not c2_sep:
                c2 = D["c2"][0]
                items.append(pick(rng, ["However, the exception in %s is not available where %s." % (R["exc"], c2),
                                        "The preceding exception does not apply if %s; %s then applies as written." % (c2, R["rule"]),
                                        "Nothing in %s prevents %s from applying where %s." % (R["exc"], R["rule"], c2)]))
            out.append((pick(rng, ["Exceptions", "Exceptions to %s" % R["rule"], "Limitations"]), items))
        elif k == "gen":
            out.append(("General conditions", [
                pick(rng, ["The exception in %s is not available where %s." % (R["exc"], D["c2"][0]),
                           "Nothing in %s prevents %s from applying where %s." % (R["exc"], R["rule"], D["c2"][0])]),
                "Each %s is assessed on the facts known at the time of decision." % D["case"]]))
        elif k == "prec":
            items = ["An endorsement or amendment prevails over the base text it changes, but only for the %ss it says it covers; all others remain under the unamended text." % D["case"]]
            if len(P["amends"]) > 1 or rng.random() < .5:
                items.append("Where two endorsements conflict, the one with the later effective date prevails.")
            if P["spec_on"] or rng.random() < .4:
                items.append("A provision addressing a specific class prevails over a general provision.")
            if rng.random() < .5:
                items.append("Informal guidance, quick-reference cards and staff notes do not modify this document.")
            out.append((pick(rng, ["Order of precedence", "Conflicts and precedence", "Construction"]), items))
    lines = []
    for i, (title, items) in enumerate(out):
        n = i + 1
        lines.append(num.head(n, title))
        if len(items) == 1:
            lines.append(items[0])
        else:
            for j, it in enumerate(items):
                lines.append("%s %s" % (num.item(n, j), it))
        lines.append("")
    return "\n".join(lines).strip()


def build_endorsements(rng, P):
    D = P["dom"]
    R, ds, ur = P["_refs"], P["_ds"], D["unit_rule"]
    if not P["amends"]:
        return ""
    basis = D["ev"][2] if P["basis"] == "event" else D["ev"][3]
    prev = {"general": P["L_old"], "specific": P.get("L_spec")}
    word = pick(rng, ["ENDORSEMENT No.", "Amendment", "Rider", "Change Notice"])
    vals = dict(ref=R["rule"], keep=P.get("keep"), p0=P.get("p0"), p1=P.get("p1"),
                r0=money(P["r0"]) if "r0" in P else None, r1=money(P["r1"]) if "r1" in P else None)
    blocks = []
    for a in P["amends"]:
        when = pick(rng, AMEND_WHEN[a["incl"]]).format(D=fdate(a["date"], ds))
        if a["mode"] == "limit":
            tref = R["rule"] if a["target"] == "general" else R["spec"]
            lp = prev[a["target"]]
            txt = pick(rng, [
                "With effect for %s %s, the figure in %s is %s %s (previously %s)." % (basis, when, tref, fnum(a["new"]), ur, fnum(lp)),
                '%s is amended by replacing "%s" with "%s". This change applies to %s %s; all other %s remain under the previous figure.'
                % (tref, fnum(lp), fnum(a["new"]), basis, when, basis)])
            prev[a["target"]] = a["new"]
        elif a["mode"] == "outcome":
            txt = D["am_out"].format(**vals) + " This applies to %s %s." % (basis, when)
        else:
            txt = "The exception in %s is deleted for %s %s. For all other %s it continues to apply." % (R["exc"], basis, when, basis)
        issued = a["date"] - dt.timedelta(days=rng.randrange(10, 70))
        head = pick(rng, ["%s %d (issued %s; effective %s)", "%s %d — issued %s, effective %s"]) % (
            word, a["k"], fdate(issued, ds), fdate(a["date"], ds))
        blocks.append(head + "\n" + txt)
    if len(blocks) > 1 and rng.random() < .4:
        blocks.reverse()
    return "\n\n".join(blocks)


def build_facts(rng, P, size):
    D = P["dom"]
    ds = P["_ds"]
    top = [(D["ev"][0], fdate(P["E"], ds), False), (D["ev"][1], fdate(P["R"], ds), False)]
    if rng.random() < .3:
        top.reverse()
    body = [(D["q"][0], D["q"][1].format(Q=fmt_q(P["q_f"], P["unit_f"])), True),
            (D["y"][0], D["y"][1] if P["Y"] else D["y"][2], True)]
    if P["trap_term"]:
        ww = D["B"][0] if P["Y"] else D["A"][0]
        P["_surface"] = ww
        body.append((pick(rng, ["Intake remark", "Note on file", "First report"]),
                     pick(rng, D["surface"]).format(w=ww.lower()), True))
    if P["spec_on"]:
        body.append((D["sub"][4], D["sub"][2] if P["is_sub"] else D["sub"][3], True))
    if P["exc_on"]:
        body.append((D["c1"][3], D["c1"][1] if P["C1"] else D["c1"][2], True))
    if P["excexc_on"]:
        body.append((D["c2"][3], D["c2"][1] if P["C2"] else D["c2"][2], True))
    if P["gate_on"]:
        body.append((D["gate"][4], D["gate"][5].format(G=fnum(P["gval"])), True))
    if P["scheme"] == "pay":
        body.append((D["fa"][0], D["fa"][1].format(A=money(P["A"])), True))
        body.append((D["fd"][0], D["fd"][1].format(d=money(P["d"])), True))
    elif P["scheme"] == "charge":
        body.append((D["fa"][0], D["fa"][1].format(A=money(P["A"])), True))
    elif P["scheme"] == "rate":
        body.append((D["fa"][0], D["fa"][1].format(n=P["n"]), True))
    nz = list(D["noise"]) + [(l, v.format(p=pick(rng, PEOPLE))) for l, v in GEN_FACTS]
    rng.shuffle(nz)
    k = 0 if size == "short" else (rng.randint(1, 2) if size == "medium" else rng.randint(3, 5))
    body += [(l, v, False) for l, v in nz[:k]]
    rng.shuffle(body)
    return top + body


def fmt_facts(rng, facts, style):
    if style == 0:
        return "\n".join("- %s: %s" % (l, v.rstrip(".")) for l, v, _ in facts)
    if style == 1:
        return " ".join((v if v.endswith(".") else v + ".") if s else "%s: %s." % (l, v) for l, v, s in facts)
    if style == 2:
        w = max(len(l) for l, _, _ in facts)
        rows = ["%s | %s" % ("Field".ljust(w), "Detail"), "%s-+-%s" % ("-" * w, "-" * 30)]
        rows += ["%s | %s" % (l.ljust(w), v.rstrip(".")) for l, v, _ in facts]
        return "\n".join(rows)
    if style == 3:
        d = {}
        for l, v, _ in facts:
            key = "".join(ch if ch.isalnum() else "_" for ch in l.lower()).strip("_")
            d[key] = v.rstrip(".")
        return json.dumps(d, indent=2, ensure_ascii=False)
    return "\n".join("%d. %s" % (i + 1, (v if v.endswith(".") else v + ".") if s else "%s: %s." % (l, v))
                     for i, (l, v, s) in enumerate(facts))


def junior_reason(rng, P, mk):
    D, R = P["dom"], P["_refs"]
    ds = P["_ds"]
    if mk == "term":
        w = P["_surface"]
        return 'The file literally says "%s", so this is a %s case under %s.' % (w.lower(), w, R["rule"])
    if mk == "unit":
        return "The file says %s and the figure in %s is %s, so the numbers speak for themselves." % (
            fmt_q(P["q_f"], P["unit_f"]), R["rule"], fnum(P["G"]))
    if mk == "boundary":
        caught = not P["incl"]
        return "It is exactly %s, right at the figure of %s, and a value equal to the limit %s." % (
            fmt_q(F(P["q_f"]) * P["factor"], D["unit"]), fnum(P["G"]), "is caught" if caught else "is not caught")
    if mk == "old_rule":
        return "Just apply %s as printed; the endorsement paperwork doesn't change our standard figure." % R["rule"]
    if mk == "retro":
        return "The endorsement is the current wording, so it governs this file as well."
    if mk == "date_basis":
        use_event = P["basis"] != "event"
        d = P["E"] if use_event else P["R"]
        lab = D["ev"][0] if use_event else D["ev"][1]
        on = bool(active_amends(P, {"date_basis"}))
        return "The relevant date is the %s, %s, so the endorsement %s." % (lab.lower(), fdate(d, ds), "applies" if on else "does not apply")
    if mk == "amend_boundary":
        on = bool(active_amends(P, {"amend_boundary"}))
        return "The endorsement's date and our date line up, so it %s." % ("already applies" if on else "does not apply yet")
    if mk == "first_amend":
        a = P["amends"][0]
        if a["mode"] == "limit":
            return "Endorsement %d set the figure at %s, so that is the number to use." % (a["k"], fnum(a["new"]))
        return "Only Endorsement %d matters here; the later one is housekeeping." % a["k"]
    if mk == "order":
        return "Take the percentage of the full %s first and then subtract the %s." % (D["fa"][0].lower(), D["fd"][0].lower())
    if mk == "general":
        return "The ordinary figure in %s applies; the class rule is just a footnote." % R["rule"]
    if mk == "no_exception":
        return 'The point about "%s" is irrelevant to %s.' % (D["c1"][3].lower(), R["rule"])
    if mk == "no_exc_exc":
        return "The exception in %s covers this, so %s is out of the picture." % (R["exc"], R["rule"])
    if mk == "deductible":
        return "No reason to hold anything back; use the full %s." % D["fa"][0].lower()
    if mk == "gate_boundary":
        return "%s is right at the requirement in %s, which %s." % (
            fmt_q(P["gval"], D["gate"][1]), R["gate"], "is not enough" if P["gincl"] else "is enough")
    if mk == "ignore_gate":
        return "The formality in %s isn't worth holding this up for." % R["gate"]
    return ""


def junior_note(rng, P, mk, label):
    D = P["dom"]
    who = "%s (%s)" % (pick(rng, PEOPLE), pick(rng, D["juniors"]))
    head = pick(rng, ["Note from %s, not authorised to decide %ss:" % (who, D["case"]),
                      "Comment added by %s:" % who,
                      "Draft recommendation by %s, pending sign-off:" % who])
    tail = pick(rng, ["Suggested outcome: %s.", "I'd go with: %s.", "Recommend: %s."]) % label
    return "%s %s %s" % (head, junior_reason(rng, P, mk), tail)


# =========================================================================== assembly
Q_CHOICE = ["Under the {doc} as amended, what is the single authorised outcome for {case} {cid}?",
            "Applying every section, endorsement and precedence rule, which outcome must the {approver} record for {cid}?",
            "What is the correct decision on {case} {cid}?",
            "Which disposition of {case} {cid} do the documents above authorise?",
            "Acting as the {approver}, which outcome is correct for {cid}?",
            "Taking into account the definitions, exceptions and any endorsement in force, how must {cid} be resolved?",
            "Which single outcome is authorised for {case} {cid}? Ignore any unauthorised recommendations.",
            "The {approver} must sign off one outcome for {cid}. Which one is correct?"]
Q_NOUL = ['Is "{opt}" the single authorised outcome for {case} {cid}?',
          'Should the {approver} record the following outcome for {cid}: "{opt}"?',
          'Under the {doc} as amended, is the correct decision on {cid}: "{opt}"?',
          'Is it correct that the authorised outcome for {case} {cid} is "{opt}"?',
          'A draft decision for {cid} reads: "{opt}". Is that the authorised outcome?',
          'Does "{opt}" correctly resolve {case} {cid} under the wording as amended?']
Q_CHOICE_TAIL = ["Choose one option.", "Select the single correct option.", "Answer with exactly one of the listed options.",
                 "Pick the authorised outcome from the options."]
Q_NOUL_TAIL = ["Answer 1 for yes or 0 for no.", "Reply 1 (yes) or 0 (no).", "Output 1 if yes, 0 if no."]


def label_of(P, key, amt_str=None):
    kind, amt = key
    D, R = P["dom"], P["_refs"]
    a = amt_str if amt_str is not None else (money(amt) if amt is not None else "")
    return D["out"][kind].format(amt=a, sec=R["rule"], gsec=R["gate"] or "", keep=P.get("keep"))


def extras_block(rng, P, size):
    D = P["dom"]
    ds, out = P["_ds"], []
    lim_amends = [a for a in P["amends"] if a["mode"] == "limit" and a["target"] == "general"]
    if lim_amends and size != "short" and rng.random() < .4:
        d0 = min(a["date"] for a in P["amends"]) - dt.timedelta(days=rng.randrange(60, 400))
        out.append("Quick-reference card (printed %s): %s \u2014 %s %s; see %s." % (
            fdate(d0, ds), D["rule_title"], fnum(P["L_old"]), D["unit_rule"], P["_refs"]["rule"]))
    if size == "long":
        lines = ["Other files in this batch (not part of this decision):"]
        for _ in range(rng.randint(2, 4)):
            l1, v1 = pick(rng, D["noise"])
            dd = P["E"] + dt.timedelta(days=rng.randrange(-90, 90))
            lines.append("- %s-%d: %s %s; %s: %s; status: %s." % (
                D["cid"], rng.randrange(10000, 99999), D["ev"][0].lower(), fdate(dd, ds), l1.lower(), v1.rstrip("."),
                pick(rng, ["awaiting documents", "closed", "under review", "escalated to legal", "paid in part"])))
        out.append("\n".join(lines))
        if rng.random() < .6:
            y = P["E"].year
            out.append("Revision history: v1 (%d) initial issue; v2 (%d) formatting changes only; v3 (%d) contact details updated." % (
                y - 4, y - 2, y - 1))
    return out


def assemble(rng, P, size, doc, endo, facts_txt, note, extras):
    D = P["dom"]
    org, title, cid = P["_org"], P["_doc"], P["_cid"]
    style = rng.randrange(4) if size != "short" else pick(rng, [0, 3])
    P["_style"] = style
    parts_doc = doc + ("\n\n" + endo if endo else "")
    ex = "\n\n".join(extras)
    handler = pick(rng, PEOPLE)
    if style == 0:
        s = "%s \u2014 %s\n\n%s\n\n%s %s\n%s" % (org, title, parts_doc, pick(rng, ["CASE FILE", "Case record", "FILE"]), cid, facts_txt)
        if ex:
            s += "\n\n" + ex
        if note:
            s += "\n\n" + note
    elif style == 1:
        s = ("From: %s\nTo: %s desk\nSubject: %s %s \u2013 decision needed\n\nHi,\nFacts are below; the governing wording is pasted underneath.\n\n%s\n\n"
             "----- Pasted from %s (%s) -----\n%s" % (handler, D["approver"], cap(D["case"]), cid, facts_txt, title, org, parts_doc))
        if ex:
            s += "\n\n" + ex
        if note:
            s += "\n\n----- Reply -----\n" + note
    elif style == 2:
        s = "MEMORANDUM\nTo: %s\nFrom: %s\nRe: %s %s\n\n1. Facts\n%s\n\n2. Applicable wording (%s, %s)\n%s" % (
            cap(D["approver"]), handler, cap(D["case"]), cid, facts_txt, org, title, parts_doc)
        if note:
            s += "\n\n3. Staff comment\n" + note
        if ex:
            s += "\n\nAnnex\n" + ex
    else:
        s = "%s (%s)\n%s\n\n%s %s:\n%s" % (title, org, parts_doc, cap(D["case"]), cid, facts_txt)
        if note:
            s += "\n\n" + note
        if ex:
            s += "\n\n" + ex
    return s


BOUNDS = {"short": (150, 599), "medium": (600, 2500), "long": (2501, 6000)}


def make_item(rng, D, size, qtype, target, want_trig=None):
    P = sample_params(rng, D, size)
    P["_org"] = pick(rng, D["orgs"])
    P["_doc"] = pick(rng, D["docs"]).format(n=rng.randint(2, 40))
    P["_cid"] = "%s-%d" % (D["cid"], rng.randrange(1000, 99999))
    gold = solve(P)
    if want_trig is not None and (gold[0] in ("TRIG", "TRIG_NEW")) != want_trig:
        raise Retry("rebalance gold kind")
    g2 = solve2(P)
    assert (gold[0], money(gold[1]) if gold[1] is not None else None) == g2, "independent check failed"
    ms = relevant_mistakes(P)
    wrong = {}
    for mk in ms:
        o = solve(P, {mk})
        if o != gold:
            wrong.setdefault(o, []).append(mk)
    if len(wrong) < 4:
        for i in range(len(ms)):
            for j in range(i + 1, len(ms)):
                o = solve(P, {ms[i], ms[j]})
                if o != gold and o not in wrong:
                    wrong[o] = [ms[i] + "+" + ms[j]]
    if not wrong or (len(wrong) == 1 and rng.random() < (.4 if size == "short" else .7)):
        raise Retry("too few distinct mistakes")
    lo, hi = BOUNDS[size]
    extra = 0
    note_on = rng.random() < (.25 if size == "short" else .55)
    fstyle = rng.randrange(5) if size != "short" else pick(rng, [0, 1, 1])
    for _ in range(8):
        r2 = random.Random(rng.random())
        if size == "short":
            st = build_short(r2, P)
            labels = {k: label_of(P, k) for k in wrong}
            gold_label = label_of(P, gold)
            if gold_label in labels.values():
                raise Retry("label collision")
            note, pushed = "", None
            singles = [(k, v[0]) for k, v in wrong.items() if "+" not in v[0]]
            if note_on and singles:
                k, mk = pick(r2, singles)
                cand = junior_note(r2, P, mk, labels[k])
                if len(st) + len(cand) + 2 < hi:
                    note, pushed = cand, labels[k]
                    st += "\n\n" + note
            if len(st) > hi:
                raise Retry("short too long")
            break
        doc = build_doc(r2, P, size, extra)
        endo = build_endorsements(r2, P)
        facts = build_facts(r2, P, size)
        facts_txt = fmt_facts(r2, facts, fstyle)
        labels = {k: label_of(P, k) for k in wrong}
        gold_label = label_of(P, gold)
        if gold_label in labels.values():
            raise Retry("label collision")
        note, pushed = "", None
        if note_on:
            singles = [(k, v[0]) for k, v in wrong.items() if "+" not in v[0]]
            if singles:
                k, mk = pick(r2, singles)
                pushed = labels[k]
                note = junior_note(r2, P, mk, pushed)
        extras = extras_block(r2, P, size)
        st = assemble(r2, P, size, doc, endo, facts_txt, note, extras)
        L = len(st)
        if L < lo:
            if size == "short":
                break
            extra += 2 if L < lo - 600 else 1
            continue
        if L > hi:
            if size == "short":
                raise Retry("short too long")
            extra -= 2 if L > hi + 600 else 1
            continue
        break
    else:
        raise Retry("length")
    if not (lo <= len(st) <= hi):
        raise Retry("length")
    g2_label = label_of(P, gold, amt_str=g2[1] if g2[1] is not None else "")
    assert g2_label == gold_label
    lab_names, lab_single = {}, {}
    for k, names in wrong.items():
        lab = labels[k]
        lab_names.setdefault(lab, [])
        for n in names:
            if n not in lab_names[lab]:
                lab_names[lab].append(n)
        lab_single[lab] = lab_single.get(lab, False) or any("+" not in n for n in names)
    mis = {}
    for lab, names in lab_names.items():
        nm = " / ".join(" + ".join(MISTAKE_NAMES[x] for x in n.split("+")) for n in names[:2])
        if lab == pushed:
            nm += " (pushed by junior note)"
        mis[lab] = nm
    fill = {"doc": P["_doc"], "case": P["dom"]["case"], "cid": P["_cid"], "approver": P["dom"]["approver"]}
    card = None
    if qtype == "choice":
        ranked = sorted(lab_names, key=lambda lab: (not lab_single[lab], lab))
        opts = [gold_label] + ranked[:7]
        rng.shuffle(opts)
        gold_out = gold_label
        instr = pick(rng, Q_CHOICE).format(**fill)
        if rng.random() < .2:
            pre = pick(rng, ["OUT", "DEC", "R", "OPT"])
            codes = ["%s-%d" % (pre, i + 1) for i in range(len(opts))]
            cmap = dict(zip(opts, codes))
            card = "\n".join("- %s: %s" % (cmap[o], o) for o in opts)
            mis = dict((cmap[o], v) for o, v in mis.items() if o in cmap)
            gold_out = cmap[gold_label]
            opts = codes
            instr += " (Answer with the outcome code from the card.)"
        else:
            mis = dict((o, v) for o, v in mis.items() if o in opts)
        instr += "\n" + pick(rng, Q_CHOICE_TAIL)
        options = opts
        chk = (gold_label, gold_label)
    else:
        if target == 1:
            opt = gold_label
        else:
            opt = pushed if (pushed and rng.random() < .5) else pick(rng, sorted(lab_names))
        instr = pick(rng, Q_NOUL).format(opt=opt, **fill) + "\n" + pick(rng, Q_NOUL_TAIL)
        options, gold_out, mis = None, target, {}
        chk = (opt, g2_label)
    q_on_boundary = F(P["q_f"]) * P["factor"] == P["G"]
    score = sum([P["trap_term"], P["factor"] != 1, q_on_boundary, bool(P["amends"]), len(P["amends"]) > 1,
                 P["excexc_on"], P["spec_on"] and P["is_sub"], bool(note), P["gate_on"], size == "long"])
    meta = {"family": FAMILY, "difficulty": "hard" if score >= 4 else "medium"}
    if mis:
        meta["mistakes"] = mis
    row = {"state": st, "qtype": qtype, "instructions": instr, "options": options, "gold": gold_out}
    if card:
        row["card"] = card
    row["meta"] = meta
    row["_domain"] = D["key"]
    row["_tpl"] = "%s|r%d|s%d|f%d|%s" % (D["key"], P["_rule_form"], P["_style"], fstyle, ",".join(sorted(P["layers"])))
    row["_chk"] = chk
    row["_kind"] = gold[0]
    return row


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
    di = [i % len(DOMAINS) for i in range(n)]
    master.shuffle(di)
    wt = [i % 2 == 0 for i in range(n)]
    master.shuffle(wt)
    rows, ti = [], 0
    for i in range(n):
        qt = qtypes[i]
        target = None
        if qt == "noul":
            target = tg[ti]
            ti += 1
        row = None
        for attempt in range(400):
            rng = random.Random(seed * 1000003 + i * 7919 + attempt * 104729)
            size = sizes[i] if attempt < 300 else "medium"
            D = DOMAINS[di[i]] if attempt < 200 else DOMAINS[(di[i] + attempt) % len(DOMAINS)]
            try:
                row = make_item(rng, D, size, qt, target, wt[i] if attempt < 350 else None)
            except Retry:
                row = None
            if row is not None:
                break
        if row is None:
            raise RuntimeError("could not generate item %d" % i)
        if not _keep:
            for k in ("_domain", "_tpl", "_chk", "_kind"):
                row.pop(k, None)
        rows.append(row)
    return rows


# =========================================================================== short form
SHORT_DEFS = {
    "insurance_property": ("no one lives in the Dwelling and it lacks the furnishings for normal living",
                           "no one lives in the Dwelling but the furnishings for normal living remain"),
    "hr_bonus_clawback": ("an employee-initiated exit not preceded by a Material Adverse Change",
                          "an employee-initiated exit preceded by a Material Adverse Change"),
    "bank_late_fee": ("an account with an installment past due and no Payment Arrangement in force",
                      "an account with an installment past due while a Payment Arrangement is in force"),
    "logistics_liability": ("temperature-controlled goods with a labelled shelf life under 30 days",
                            "temperature-controlled goods with a labelled shelf life of 30 days or more"),
    "health_preauth": ("a pre-booked admission without a physician's time-sensitivity certificate",
                       "a pre-booked admission with a physician's time-sensitivity certificate"),
    "saas_sla": ("unscheduled unavailability affecting all of Customer's users",
                 "unscheduled unavailability affecting some but not all users"),
    "tuition_residency": ("a person in the State mainly for a reason other than education",
                          "a person in the State mainly to attend school"),
    "travel_per_diem": ("business travel outside the Home Area with an overnight stay",
                        "business travel outside the Home Area returning the same day"),
    "retail_returns": ("a returned product that is opened and shows signs of use",
                       "a returned product that is opened but shows no signs of use"),
    "privacy_breach": ("unauthorised access to readable (unencrypted) personal data",
                       "unauthorised access to personal data encrypted with a secure key"),
    "manufacturing_qa": ("a defect that impairs function and creates a safety hazard",
                         "a defect that impairs function without a safety hazard"),
    "benefits_student": ("a person enrolled in higher education for 12+ credit hours",
                         "a person enrolled in higher education for fewer than 12 credit hours"),
}
REF_ONLY_A = {"tuition_residency", "hr_bonus_clawback", "privacy_breach"}
# stated separately when the rule is phrased in the negative ("No X unless ..."), so the amount is always given
RATE_TXT = {"hr_bonus_clawback": "Repayment, where due, is {p0}% of the Sign-On Bonus.",
            "bank_late_fee": "The Late Fee is {p0}% of the overdue installment.",
            "saas_sla": "The Service Credit is {p0}% of that month's fee.",
            "tuition_residency": "The in-state rate is {r0} per credit.",
            "travel_per_diem": "The daily allowance is {r0} per travel day."}


def main_rule(P, rv, cond, trig, neg, vals):
    D = P["dom"]
    if rv == 0:
        return "If %s, %s." % (cond, trig)
    if rv == 1:
        return "%s where %s." % (cap(trig), cond)
    extra = (" " + RATE_TXT[D["key"]].format(**vals)) if D["key"] in RATE_TXT else ""
    return "%s unless %s.%s" % (cap(neg), cond, extra)


def build_short(rng, P):
    """Compact (<600 chars) rendering: terse definitions, numbered rules, one-paragraph case."""
    D = P["dom"]
    tagf = pick(rng, ["§%d", "Rule %d", "Cl. %d", "%d."])
    P["_ds"] = pick(rng, [0, 4])
    ds = P["_ds"]
    keys = (["gate"] if P["gate_on"] else []) + ["rule"] + (["exc"] if P["exc_on"] else [])
    nums = dict((k, i + 1) for i, k in enumerate(keys))

    def ref(k, sub=None):
        t = (tagf % nums[k]).rstrip(".")
        if tagf == "%d.":
            t = "clause " + t
        return t if sub is None else "%s(%s)" % (t, "ab"[sub])
    R = {"rule": ref("rule", 0) if (P["spec_on"] or D["else_txt"]) else ref("rule"),
         "spec": ref("rule", 1) if P["spec_on"] else None,
         "exc": ref("exc") if P["exc_on"] else None, "gate": ref("gate") if P["gate_on"] else None}
    P["_refs"] = R
    sd = SHORT_DEFS[D["key"]]
    defs = [(D["A"][0], sd[0]), (D["B"][0], sd[1])]
    rng.shuffle(defs)
    dv = rng.randrange(3)
    dl = " ".join([('"%s" = %s.', "%s: %s.", "%s means %s.")[dv] % d for d in defs])
    vals = dict(p0=P.get("p0"), p1=P.get("p1"), keep=P.get("keep"),
                r0=money(P["r0"]) if "r0" in P else None, r1=money(P["r1"]) if "r1" in P else None,
                ralt=money(P["ralt"]) if "ralt" in P else None)
    Tref = D[P["term_ref"]][0]
    cond = D["cond"].format(T=Tref, CMP=cmp_text(rng, P["dir"], P["incl"], P["L_old"], D["unit_rule"]))
    rv = rng.randrange(3)
    P["_rule_form"] = rv
    trig, neg = D["trig"].format(**vals), D["neg"].format(**vals)
    main = main_rule(P, rv, cond, trig, neg, vals)
    out = [dl]
    for k in keys:
        head = (tagf % nums[k]) if tagf != "%d." else "%d." % nums[k]
        if k == "gate":
            gc = D["gate"][0].format(CMP=cmp_text(rng, P["gdir"], P["gincl"], P["gmin"], D["gate"][1]))
            out.append("%s A %s is considered only if %s." % (head, D["case"], gc))
        elif k == "rule":
            t = "%s %s%s" % (head, "(a) " if R["spec"] or D["else_txt"] else "", main)
            nxt = "b"
            if P["spec_on"]:
                t += " (b) For %s the figure is %s." % (D["sub"][1], fnum(P["L_spec"]))
                nxt = "c"
            if D["else_txt"]:
                t += " (%s) %s" % (nxt, D["else_txt"].format(**vals))
            out.append(t)
        else:
            t = "%s %s does not apply where %s." % (head, R["rule"], D["c1"][0])
            if P["excexc_on"]:
                t += " This exception is unavailable where %s." % D["c2"][0]
            out.append(t)
    if P["amends"]:
        a = P["amends"][0]
        basis = D["ev"][2] if P["basis"] == "event" else D["ev"][3]
        when = pick(rng, AMEND_WHEN[a["incl"]]).format(D=fdate(a["date"], ds))
        vals["ref"] = R["rule"]
        if a["mode"] == "limit":
            body = "for %s %s, the figure in %s is %s (was %s)." % (
                basis, when, R["rule"] if a["target"] == "general" else R["spec"], fnum(a["new"]),
                fnum(P["L_old"] if a["target"] == "general" else P["L_spec"]))
        elif a["mode"] == "outcome":
            body = "for %s %s: %s" % (basis, when, D["am_out"].format(**vals))
        else:
            body = "the exception in %s is deleted for %s %s." % (R["exc"], basis, when)
        out.append("%s %d (eff. %s): %s" % (pick(rng, ["Endorsement", "Amendment", "Rider"]), a["k"], fdate(a["date"], ds), body))
    facts = ["%s: %s." % (D["ev"][0], fdate(P["E"], ds))] if (P["amends"] or rng.random() < .4) else []
    if P["amends"]:
        facts.append("%s: %s." % (D["ev"][1], fdate(P["R"], ds)))
    facts.append(D["q"][1].format(Q=fmt_q(P["q_f"], P["unit_f"])))
    facts.append(D["y"][1] if P["Y"] else D["y"][2])
    if P["trap_term"]:
        ww = D["B"][0] if P["Y"] else D["A"][0]
        P["_surface"] = ww
        facts.append(pick(rng, ['Intake note says "{w}".', 'Tagged "{w}" at intake.', 'First report says "{w}".']).format(w=ww.lower()))
    if P["spec_on"]:
        facts.append(D["sub"][2] if P["is_sub"] else D["sub"][3])
    if P["exc_on"]:
        facts.append(D["c1"][1] if P["C1"] else D["c1"][2])
    if P["excexc_on"]:
        facts.append(D["c2"][1] if P["C2"] else D["c2"][2])
    if P["gate_on"]:
        facts.append(D["gate"][5].format(G=fnum(P["gval"])))
    if P["scheme"] in ("pay", "charge"):
        facts.append("%s: %s." % (D["fa"][0], money(P["A"])))
    if P["scheme"] == "pay":
        facts.append("%s: %s." % (D["fd"][0], money(P["d"])))
    if P["scheme"] == "rate":
        facts.append("%s: %d." % (D["fa"][0], P["n"]))
    k0 = 2 if P["amends"] else len(facts) - len(facts)
    body = facts[:k0] + sorted(facts[k0:], key=lambda _: rng.random())
    P["_style"] = 9
    return "\n".join(out) + "\n\n%s %s: %s" % (cap(D["case"]), P["_cid"], " ".join(body))


# =========================================================================== self-test
ROW_KEYS = {"state", "qtype", "instructions", "options", "gold", "card", "meta"}


def _validate(r):
    ks = set(k for k in r if not k.startswith("_"))
    assert ks <= ROW_KEYS and {"state", "qtype", "instructions", "options", "gold", "meta"} <= ks, r.keys()
    assert isinstance(r["state"], str) and r["state"].strip()
    assert isinstance(r["instructions"], str) and r["instructions"].strip()
    assert r["qtype"] in ("choice", "noul")
    m = r["meta"]
    assert set(m) <= {"family", "difficulty", "gold_probs", "mistakes"}
    assert m["family"] == FAMILY and m["difficulty"] in ("medium", "hard")
    if r["qtype"] == "choice":
        o = r["options"]
        assert isinstance(o, list) and 2 <= len(o) <= 8 and len(set(o)) == len(o)
        assert all(isinstance(x, str) and x for x in o)
        assert r["gold"] in o
        for k in m.get("mistakes", {}):
            assert k in o and k != r["gold"]
    else:
        assert r["options"] is None and r["gold"] in (0, 1)
    if r.get("card") is not None:
        assert isinstance(r["card"], str)
        assert all(line.startswith("- ") and ": " in line for line in r["card"].split("\n"))
    if m.get("gold_probs") is not None:
        assert abs(sum(m["gold_probs"].values()) - 1) < 1e-9
        assert r["gold"] in m["gold_probs"]


def _show(r):
    print("=" * 100)
    print("[%s | %s | %s]" % (r["qtype"], r["meta"]["difficulty"], r.get("_domain", "")))
    print(r["state"])
    print("-" * 40)
    print(r["instructions"])
    if r.get("card"):
        print("CARD:\n" + r["card"])
    print("OPTIONS:", json.dumps(r["options"], ensure_ascii=False))
    print("GOLD:", r["gold"])
    print("MISTAKES:", json.dumps(r["meta"].get("mistakes", {}), ensure_ascii=False, indent=1))


def _selftest(n=300, seed=20260926):
    rows = generate(n, seed, _keep=True)
    for r in rows:
        _validate(r)
    # independent gold check: the label produced from solve2's result must match
    for r in rows:
        opt, g2 = r["_chk"]
        if r["qtype"] == "choice":
            gl = r["gold"]
            if r.get("card"):
                gl = dict(line[2:].split(": ", 1) for line in r["card"].split("\n"))[gl]
            assert gl == g2 == opt, (gl, g2)
        else:
            assert (opt == g2) == (r["gold"] == 1), (opt, g2, r["gold"])
    # determinism
    a = json.dumps(generate(n, seed), sort_keys=True, ensure_ascii=False)
    b = json.dumps(generate(n, seed), sort_keys=True, ensure_ascii=False)
    strip = [dict((k, v) for k, v in r.items() if not k.startswith("_")) for r in rows]
    assert a == b == json.dumps(strip, sort_keys=True, ensure_ascii=False), "non-deterministic"
    assert json.dumps(generate(20, seed + 1)) != json.dumps(generate(20, seed))
    # stats
    L = [len(r["state"]) for r in rows]
    buckets = {"short(<600)": sum(x < 600 for x in L), "medium(600-2500)": sum(600 <= x <= 2500 for x in L),
               "long(>2500)": sum(x > 2500 for x in L)}
    noul = [r for r in rows if r["qtype"] == "noul"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    pos = {}
    for r in ch:
        k = (len(r["options"]), r["options"].index(r["gold"]))
        pos[k] = pos.get(k, 0) + 1
    nopt = {}
    for r in ch:
        nopt[len(r["options"])] = nopt.get(len(r["options"]), 0) + 1
    doms = {}
    for r in rows:
        doms[r["_domain"]] = doms.get(r["_domain"], 0) + 1
    print("=" * 100)
    print("SELF-TEST PASSED: %d items" % n)
    print("domains (%d):" % len(doms), doms)
    print("distinct templates (domain|rule-form|container|fact-format|layers):", len(set(r["_tpl"] for r in rows)))
    print("length buckets:", buckets, "min/median/max:", min(L), sorted(L)[len(L) // 2], max(L))
    print("choice=%d noul=%d  noul yes-rate=%.3f" % (len(ch), len(noul), sum(r["gold"] for r in noul) / max(1, len(noul))))
    print("options per choice item:", dict(sorted(nopt.items())))
    print("gold index for 3-option items:", dict(sorted((k[1], v) for k, v in pos.items() if k[0] == 3)))
    print("difficulty:", {d: sum(r["meta"]["difficulty"] == d for r in rows) for d in ("medium", "hard")})
    print("with junior note:", sum(("not authorised" in r["state"]) or ("Comment added by" in r["state"])
                                     or ("Draft recommendation" in r["state"]) for r in rows))
    return rows


if __name__ == "__main__":
    ex = generate(12, 5, _keep=True)
    for r in (ex[0], ex[3], ex[7]):
        _show(r)
    _selftest()
