"""Procedural generator for the "routing" family of System-One decision problems.

Sub-families
  (a) route   : pick the tool / team / API that satisfies ALL constraints
  (b) rubric  : ordinal rubric scoring, gold = highest fully supported level
  (c) tradeoff: explicit weighted scoring of 2-4 alternatives with tie-break rules

Pure standard library, deterministic from the seed.  Gold answers are computed
by a small rule engine and re-checked by an independent code path.
Usage:  python3 -m pg.routing   (prints examples + runs the self-test)
"""
import datetime
import json
import random
import re
from decimal import Decimal
from fractions import Fraction

FAMILY = "routing"

FIRST = ["Priya", "Marcus", "Elena", "Tomas", "Aisha", "Kenji", "Fatima", "Liam", "Sofia", "Noah",
         "Chen", "Olga", "Rahul", "Grace", "Diego", "Hana", "Samuel", "Ines", "Yusuf", "Mei", "Jonas",
         "Amara", "Felix", "Leila", "Owen", "Zara", "Mateo", "Nadia", "Ethan", "Ruth"]
LAST = ["Nair", "Okafor", "Novak", "Reyes", "Haddad", "Tanaka", "Lindqvist", "Brennan", "Moretti",
        "Kowalski", "Zhang", "Petrova", "Mehta", "Osei", "Alvarez", "Kim", "Fischer", "Duarte", "Aydin",
        "Lin", "Berg", "Mensah", "Wagner", "Rahimi", "Doyle", "Qureshi", "Silva", "Park", "Cohen", "Ibsen"]
COMPANIES = ["Northwind", "Halcyon", "Brightwater", "Kestrel", "Orbis", "Larkspur", "Meridian", "Tamarack",
             "Juniper", "Cobalt", "Redfern", "Ashgrove", "Veridian", "Sable", "Pinecrest", "Quillon"]
JUNIOR = ["summer intern", "trainee analyst", "new hire (second week)", "contractor, no approval rights",
          "student worker", "shadowing associate", "temp from the staffing agency", "apprentice coordinator"]
SENIOR = ["Director of Operations", "Policy Owner", "Head of Compliance", "Routing Governance Lead",
          "VP Service Delivery", "Chief Risk Officer"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WD3 = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# --------------------------------------------------------------------------------------------
# Domain data (12 domains).  Each domain feeds all three sub-families.
# --------------------------------------------------------------------------------------------
DOMAINS = {
    "insurance": dict(
        org="Mutual", req="claim", rid="CLM", unit="pages", hnoun=["claims queue", "adjuster desk", "claims team"],
        handlers=["Auto Physical Damage Desk", "Property Triage", "Fast-Track Claims", "Specialty Lines Unit",
                  "Catastrophe Response", "Subrogation Unit", "Legacy Claims Hub", "Bodily Injury Team",
                  "Small Commercial Desk", "Coastal Claims Pod"],
        caps=["total-loss valuation", "Spanish-language adjusting", "drone roof inspection", "litigation hold",
              "salvage auction", "rental coordination", "medical bill review", "fraud referral"],
        sens="claimant medical records", urgent="catastrophe-flagged",
        subject="the claim file", rtitle="Claim File Documentation Rubric",
        levels=["Incomplete", "Minimal", "Adequate", "Thorough", "Audit-ready"],
        metrics=[("frac", "required forms signed", "forms"), ("dur", "first contact with the claimant", "h"),
                 ("date", "site inspection report"), ("doc", "reserve rationale memo"),
                 ("cnt", "independent damage photographs", "photos supplied by a contractor bidding on the repair"),
                 ("num", "reserve accuracy", "%", "hi", 70, 98)],
        decision="select a repair shop for the insured vehicle",
        alts=["Crestline Auto Body", "Precision Collision", "Main Street Garage", "Apex Paint & Frame",
              "Riverside Motors", "QuickFix Collision"],
        crits=["warranty quality", "customer rating", "OEM parts use", "distance to insured", "communication"],
        band=("repair estimate", "$", 2000, 9000)),
    "hr": dict(
        org="Group", req="leave request", rid="LV", unit="records", hnoun=["HR service team", "case queue", "people-ops desk"],
        handlers=["Leave & Absence Center", "Benefits Desk", "Employee Relations", "Payroll Operations",
                  "Accommodations Team", "Global Mobility", "Shared Services Hub", "Regional HR East",
                  "Regional HR West", "Tier-2 Case Team"],
        caps=["FMLA certification", "disability accommodation", "payroll adjustment", "multi-state leave law",
              "union grievance", "visa impact review", "bereavement leave", "military leave"],
        sens="medical certifications", urgent="time-critical",
        subject="the leave case", rtitle="Leave Case Handling Quality Rubric",
        levels=["Deficient", "Basic", "Compliant", "Strong", "Exemplary"],
        metrics=[("dur", "acknowledgment of the request", "h"), ("frac", "required notices sent on time", "notices"),
                 ("doc", "signed return-to-work plan"), ("date", "manager training on leave law"),
                 ("num", "payroll accuracy", "%", "hi", 90, 100),
                 ("cnt", "documented check-ins", "informal hallway conversations")],
        decision="choose a leave-administration vendor",
        alts=["Absentia", "LeaveLogic", "CareShift HR", "Tempo Benefits", "Harbor Absence", "ClearLeave"],
        crits=["compliance coverage", "employee satisfaction", "integration effort", "reporting", "support quality"],
        band=("annual fee", "$", 20000, 90000)),
    "banking": dict(
        org="Bank", req="loan application", rid="LN", unit="documents", hnoun=["underwriting desk", "credit team", "underwriting service"],
        handlers=["Residential Underwriting", "Small Business Credit", "Private Client Lending", "Consumer Loans Desk",
                  "Commercial Real Estate", "Agri Lending Team", "Specialty Finance", "Retail Credit Hub",
                  "Mortgage Express", "Legacy Loan Servicing"],
        caps=["jumbo mortgage", "SBA 7(a)", "non-resident borrower", "self-employed income analysis",
              "construction draw", "co-signer review", "agricultural lending", "bridge loan"],
        sens="unmasked account numbers", urgent="rate-lock-expiring",
        subject="the loan file", rtitle="Underwriting File Quality Scorecard",
        levels=["Unacceptable", "Weak", "Satisfactory", "Strong", "Excellent"],
        metrics=[("num", "debt-to-income ratio", "%", "lo", 28, 50), ("frac", "income documents verified", "documents"),
                 ("date", "credit report pull"), ("doc", "appraisal review"),
                 ("cnt", "months of bank statements", "statements for accounts closed before application"),
                 ("dur", "conditional approval turnaround", "h")],
        decision="choose a financing offer for the warehouse expansion",
        alts=["Offer A (First Harbor)", "Offer B (Unity Credit)", "Offer C (Lakeside Capital)", "Offer D (Pioneer Trust)",
              "Offer E (Granite Bank)", "Offer F (Beacon Lending)"],
        crits=["covenant flexibility", "speed to fund", "prepayment terms", "relationship value", "collateral terms"],
        band=("all-in rate", "bps", 450, 900)),
    "logistics": dict(
        org="Logistics", req="shipment", rid="SHP", unit="parcels", hnoun=["carrier API", "carrier", "shipping partner"],
        handlers=["ParcelLink API", "SwiftFreight", "Coastline Carriers", "RoadRunner LTL", "NorthStar Express",
                  "BlueRiver Freight", "Metro Courier", "GlobalHaul v1", "GlobalHaul v2", "PrimeLane"],
        caps=["hazmat class 9", "temperature control", "liftgate delivery", "customs brokerage",
              "signature on delivery", "Saturday delivery", "oversize freight", "white-glove install"],
        sens="export-controlled items", urgent="expedite",
        subject="the carrier", rtitle="Carrier Performance Tier Rubric",
        levels=["Probation", "Bronze", "Silver", "Gold", "Platinum"],
        metrics=[("num", "on-time delivery rate", "%", "hi", 85, 99), ("num", "damage claims per 1,000 shipments", "", "lo", 1, 12),
                 ("frac", "scans with valid GPS", "scans"), ("dur", "claims response time", "h"),
                 ("date", "last safety audit"), ("doc", "hazmat training records")],
        decision="choose a carrier for the Q3 regional lane",
        alts=["SwiftFreight", "Coastline Carriers", "RoadRunner LTL", "NorthStar Express", "BlueRiver Freight", "PrimeLane"],
        crits=["on-time history", "damage rate", "capacity guarantee", "tracking quality", "claims handling"],
        band=("transit time", "days", 2, 9)),
    "healthcare": dict(
        org="Health", req="scheduling referral", rid="REF", unit="appointments", hnoun=["scheduling vendor", "scheduling desk", "booking service"],
        handlers=["CareSlot", "MedBook Central", "Pediatric Access Desk", "Imaging Scheduling", "TeleVisit Hub",
                  "Specialty Access Team", "Regional Booking East", "PatientFirst Scheduling", "OldBook (legacy)", "Nightline Scheduling"],
        caps=["pediatric sedation", "interpreter booking", "MRI with contrast", "telehealth",
              "wheelchair transport", "sleep study", "prior-auth submission", "same-day slots"],
        sens="psychotherapy notes", urgent="STAT",
        subject="the scheduling vendor", rtitle="Scheduling Vendor Service Rubric",
        levels=["Non-compliant", "Developing", "Meeting", "Exceeding", "Outstanding"],
        metrics=[("frac", "referrals booked within 10 business days", "referrals"), ("num", "no-show rate", "%", "lo", 4, 20),
                 ("dur", "callback for urgent referrals", "h"), ("date", "HIPAA training completion"),
                 ("doc", "signed business associate agreement"),
                 ("cnt", "languages with certified interpreters", "machine-translation-only languages")],
        decision="choose a site for the new pediatric scheduling hub",
        alts=["Elm Street Clinic", "Harborview Annex", "Westgate Medical Plaza", "Northside Campus", "Lakeside Pavilion", "Downtown Tower"],
        crits=["patient access", "staffing availability", "parking", "transit links", "expansion room"],
        band=("monthly lease", "$", 18000, 60000)),
    "saas": dict(
        org="Cloud", req="incident", rid="INC", unit="events", hnoun=["on-call rotation", "escalation team", "response team"],
        handlers=["SRE Core", "Database Reliability", "Edge/CDN Team", "Payments Platform", "Identity & SSO",
                  "Network Ops", "Customer Comms", "Platform Tier-2", "Legacy Ops (retiring)", "Follow-the-Sun Desk"],
        caps=["database failover", "CDN purge", "Kubernetes node recovery", "payment gateway access",
              "SAML/SSO debugging", "DNS changes", "customer status-page updates", "log forensics"],
        sens="cardholder data", urgent="Sev-1",
        subject="the incident postmortem", rtitle="Postmortem Quality Rubric",
        levels=["Missing", "Draft", "Acceptable", "Good", "Exemplary"],
        metrics=[("dur", "postmortem publication after resolution", "h"), ("frac", "action items with a named owner", "action items"),
                 ("doc", "customer impact statement"),
                 ("cnt", "timeline entries with verified timestamps", "entries pasted from chat without verification"),
                 ("num", "alert-to-acknowledge time", "min", "lo", 2, 30), ("date", "runbook update")],
        decision="choose a remediation plan for the recurring queue outage",
        alts=["Plan Alpha (shard the queue)", "Plan Bravo (add circuit breakers)", "Plan Charlie (vendor migration)",
              "Plan Delta (autoscaling rework)", "Plan Echo (rate limiting)", "Plan Foxtrot (full rewrite)"],
        crits=["risk reduction", "customer impact during rollout", "reversibility", "team familiarity", "observability gain"],
        band=("engineering effort", "person-weeks", 2, 20)),
    "education": dict(
        org="University", req="application", rid="APP", unit="transcripts", hnoun=["evaluation service", "reader team", "credential evaluator"],
        handlers=["International Credentials", "Fine Arts Review", "Transfer Evaluation", "Graduate Reader Pool",
                  "Athletics Compliance", "Access Services Liaison", "Early Decision Readers", "Scholarship Committee",
                  "Legacy Records Office", "Rolling Admissions Desk"],
        caps=["international transcript evaluation", "portfolio review", "audition scheduling", "fee waiver review",
              "transfer credit mapping", "disability services liaison", "athletic eligibility", "assistantship matching"],
        sens="records of minors", urgent="deadline-day",
        subject="the applicant", rtitle="Holistic Admissions Reading Rubric",
        levels=["Not competitive", "Developing", "Competitive", "Strong", "Exceptional"],
        metrics=[("num", "math section percentile", "th percentile", "hi", 50, 99),
                 ("cnt", "recommendation letters", "letters from relatives"),
                 ("frac", "core courses completed with B or better", "core courses"), ("doc", "graded writing sample"),
                 ("num", "community service", "hours", "hi", 20, 200), ("date", "English proficiency test")],
        decision="choose a learning-management system",
        alts=["CourseCraft", "LearnGrid", "Scholaris", "OpenQuad", "Campus Canvas Pro", "EduNimbus"],
        crits=["accessibility", "faculty rating", "integration", "support", "mobile experience"],
        band=("annual license", "$", 40000, 160000)),
    "travel": dict(
        org="Industries", req="expense report", rid="EXP", unit="receipts", hnoun=["expense auditor", "travel desk", "audit queue"],
        handlers=["T&E Audit Team", "Global Travel Desk", "Card Reconciliation", "Relocation Desk", "VAT Recovery Unit",
                  "Executive Expenses", "Offshore Audit Pool", "AutoAudit Bot", "Legacy Expense Queue", "Field Sales Desk"],
        caps=["foreign-currency receipts", "per-diem calculation", "mileage audit", "group travel",
              "visa fee reimbursement", "corporate card reconciliation", "VAT reclaim", "relocation expenses"],
        sens="passport scans", urgent="month-end-close",
        subject="the expense report", rtitle="Expense Report Compliance Rubric",
        levels=["Rejected", "Needs rework", "Acceptable", "Clean", "Model report"],
        metrics=[("frac", "receipts itemized", "receipts"), ("dur", "submission after trip end", "d"),
                 ("doc", "pre-trip approval"), ("num", "lodging cost versus city cap", "%", "lo", 80, 130),
                 ("date", "corporate card reconciliation"),
                 ("cnt", "meal receipts with attendee names", "alcohol-only receipts")],
        decision="choose a hotel for the sales offsite",
        alts=["Harborfront Suites", "The Meridian Inn", "Parkside Hotel", "Summit Lodge", "Canal Street Hotel", "Airport Grand"],
        crits=["distance to venue", "meeting space", "guest rating", "cancellation flexibility", "breakfast included"],
        band=("nightly rate", "$", 120, 420)),
    "retail": dict(
        org="Retail", req="return", rid="RMA", unit="items", hnoun=["returns processor", "returns center", "returns partner"],
        handlers=["ReCommerce Hub", "Battery-Safe Returns", "Furniture Pickup Co", "Jewelry Authentication Lab",
                  "CrossBorder Returns", "Store Exchange Desk", "Apparel Resale Partner", "Bulk Liquidators",
                  "Legacy RMA Portal", "Midwest Returns Center"],
        caps=["electronics refurbishment", "lithium battery handling", "furniture pickup", "jewelry authentication",
              "cross-border returns", "gift receipt exchange", "apparel resale", "bulk liquidation"],
        sens="stored payment tokens", urgent="holiday-peak",
        subject="the returns partner", rtitle="Returns Partner Grading Rubric",
        levels=["Suspended", "Conditional", "Approved", "Preferred", "Strategic"],
        metrics=[("num", "refund accuracy", "%", "hi", 90, 100), ("dur", "refund issued after item received", "h"),
                 ("frac", "returns graded within SLA", "returns"), ("doc", "data-wipe certification process"),
                 ("date", "last on-site audit"),
                 ("cnt", "certified refurbishment technicians", "technicians still on probation")],
        decision="choose a liquidation channel for returned inventory",
        alts=["Outlet Stores", "Online Auction", "B2B Liquidator", "Donation Partner", "Refurbish & Resell", "Recycling Contract"],
        crits=["recovery rate", "speed", "brand risk", "volume capacity", "sustainability"],
        band=("handling cost per pallet", "$", 30, 150)),
    "privacy": dict(
        org="Data", req="data subject request", rid="DSR", unit="records", hnoun=["privacy operations team", "DSAR processor", "privacy queue"],
        handlers=["Privacy Ops EU", "Privacy Ops Americas", "Erasure Service", "Portability Exporter", "HR Privacy Desk",
                  "Identity Verification Team", "Legal Hold Desk", "DSAR Bot v1", "DSAR Bot v2", "Outsourced DSAR Partner"],
        caps=["erasure across backups", "data portability export", "minors' data", "employee records",
              "opt-out of sale", "identity verification", "third-party redaction", "legal-hold check"],
        sens="biometric identifiers", urgent="statutory-deadline",
        subject="the processor", rtitle="Processor Privacy Maturity Rubric",
        levels=["Non-compliant", "Initial", "Defined", "Managed", "Optimized"],
        metrics=[("dur", "breach notification to the controller", "h"), ("frac", "requests closed within the statutory deadline", "requests"),
                 ("doc", "records of processing activities"), ("date", "last DPIA review"),
                 ("num", "staff privacy-training completion", "%", "hi", 70, 100),
                 ("cnt", "sub-processors listed with country", "sub-processors still pending approval")],
        decision="choose a consent-management platform",
        alts=["ConsentOS", "PrivaGate", "OptInly", "TrustLayer", "CookieWarden", "ClearConsent"],
        crits=["regulatory coverage", "integration effort", "audit logging", "vendor stability", "UX quality"],
        band=("annual subscription", "$", 15000, 75000)),
    "manufacturing": dict(
        org="Manufacturing", req="nonconformance report", rid="NCR", unit="measurements", hnoun=["QA lab", "inspection cell", "metrology team"],
        handlers=["Metrology Lab A", "Weld Inspection Cell", "Corrosion Test Lab", "Materials Testing", "Surface Finish Lab",
                  "Receiving Inspection", "First-Article Team", "Night Shift QA", "Old Metrology Lab", "Contract Test House"],
        caps=["CMM measurement", "X-ray weld inspection", "salt-spray testing", "tensile testing",
              "surface roughness", "hardness testing", "dye penetrant", "first-article inspection"],
        sens="defense-program drawings", urgent="line-down",
        subject="the supplier", rtitle="Supplier Quality Tier Rubric",
        levels=["Disqualified", "Conditional", "Approved", "Preferred", "Certified partner"],
        metrics=[("num", "first-pass yield", "%", "hi", 85, 99), ("num", "defects per million (PPM)", "PPM", "lo", 50, 900),
                 ("dur", "corrective action response", "h"), ("date", "last ISO 9001 surveillance audit"),
                 ("doc", "control plan for critical characteristics"),
                 ("frac", "lots shipped with certificates of conformance", "lots")],
        decision="choose a second-source supplier for machined housings",
        alts=["Keystone Machining", "Delta Precision", "Ironbridge Works", "Summit CNC", "Bluewater Fabrication", "Orion Components"],
        crits=["quality score", "capacity", "proximity", "engineering support", "financial health"],
        band=("lead time", "days", 10, 60)),
    "benefits": dict(
        org="County Services", req="benefit application", rid="BEN", unit="case files", hnoun=["eligibility unit", "caseworker team", "processing center"],
        handlers=["SNAP Processing", "Disability Determination", "Language Access Unit", "Home Visit Team",
                  "Long-Term Care Unit", "Housing Assistance", "Emergency Assistance Desk", "Appeals Unit",
                  "Legacy Intake Office", "Central Processing Center"],
        caps=["SNAP recertification", "disability determination", "interpreter services", "home visit",
              "long-term care Medicaid", "housing voucher", "emergency assistance", "appeals preparation"],
        sens="domestic-violence shelter addresses", urgent="emergency",
        subject="the application file", rtitle="Eligibility File Completeness Rubric",
        levels=["Incomplete", "Pending", "Processable", "Complete", "Expedite-ready"],
        metrics=[("frac", "household members with verified identity", "members"), ("dur", "interview scheduled after filing", "d"),
                 ("doc", "signed attestation of income"), ("date", "proof of residence"),
                 ("cnt", "pay stubs", "stubs dated more than 60 days before filing"),
                 ("num", "verified income as a share of the limit", "%", "lo", 60, 130)],
        decision="choose a community outreach program to fund",
        alts=["Mobile Enrollment Van", "Library Help Desks", "School Liaison Program", "Faith Partner Network",
              "Text-Message Reminders", "Clinic Navigators"],
        crits=["households reached", "equity impact", "implementation readiness", "partner strength", "sustainability"],
        band=("cost per household", "$", 20, 120)),
}
DOMAIN_KEYS = sorted(DOMAINS)


# --------------------------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------------------------
def person(rng):
    return "%s %s" % (rng.choice(FIRST), rng.choice(LAST))


def commas(n):
    return "{:,}".format(n)


def fmt_date(d, style):
    if style == 0:
        return d.isoformat()
    if style == 1:
        return "%d %s %d" % (d.day, d.strftime("%b"), d.year)
    if style == 2:
        return "%s %d, %d" % (d.strftime("%B"), d.day, d.year)
    return "%s %s" % (WD3[d.weekday()], d.isoformat())


def fmt_time(minutes, style):
    h, m = divmod(minutes, 60)
    if style == 0:
        return "%02d:%02d" % (h, m)
    suf = "am" if h < 12 else "pm"
    h12 = h % 12 or 12
    return "%d:%02d %s" % (h12, m, suf)


def fmt_money(amount, cents=True):
    """amount: Fraction or int dollars."""
    amount = Fraction(amount)
    if cents or amount.denominator != 1:
        q = Decimal(amount.numerator) / Decimal(amount.denominator)
        return "$" + "{:,.2f}".format(q)
    return "$" + commas(int(amount))


def rand_date(rng, year=None):
    year = year or rng.choice([2025, 2026])
    start = datetime.date(year, 1, 5)
    return start + datetime.timedelta(days=rng.randint(0, 350))


def shuffled(rng, seq):
    seq = list(seq)
    rng.shuffle(seq)
    return seq


def pick_bucket(rng):
    r = rng.random()
    return "short" if r < 0.30 else ("medium" if r < 0.70 else "long")


BUCKET_RANGE = {"short": (150, 599), "medium": (600, 2500), "long": (2500, 6000)}


def in_bucket(text, bucket):
    lo, hi = BUCKET_RANGE[bucket]
    return lo <= len(text) <= hi


# --------------------------------------------------------------------------------------------
# Irrelevant filler sections (boilerplate, other cases, unrelated clauses)
# --------------------------------------------------------------------------------------------
def _f_confidential(rng, d, c):
    return rng.choice([
        "CONFIDENTIALITY NOTICE: This message and any attachments are intended solely for the named recipients at "
        "%s %s. If you received it in error, delete it and notify the sender. Unauthorized review, forwarding or "
        "copying is prohibited. Nothing in this message creates a binding commitment unless confirmed in writing by "
        "an authorized signatory." % (c["co"], d["org"]),
        "Internal use only. Distribution outside %s %s requires approval from the document owner. This excerpt is "
        "reproduced for operational convenience; the controlling version lives in the policy portal. Printed copies "
        "are uncontrolled." % (c["co"], d["org"])])


def _f_revision(rng, d, c):
    rows = []
    base = c["date"] - datetime.timedelta(days=rng.randint(400, 900))
    for i in range(rng.randint(3, 5)):
        base += datetime.timedelta(days=rng.randint(40, 120))
        what = rng.choice(["formatting and typo fixes", "updated contact list", "clarified glossary terms",
                           "added retention appendix", "renumbered sections", "removed obsolete fax instructions",
                           "aligned terminology with the %s handbook" % d["req"], "added accessibility statement"])
        rows.append("  v1.%d | %s | %s | %s" % (i + 1, base.isoformat(), person(rng), what))
    return "Document revision log (editorial changes only):\n  ver  | date       | editor | change\n" + "\n".join(rows)


def _f_glossary(rng, d, c):
    terms = [("SLA", "service level agreement"), ("RACI", "responsible / accountable / consulted / informed"),
             ("KPI", "key performance indicator"), ("PII", "personally identifiable information"),
             ("FTE", "full-time equivalent"), ("QBR", "quarterly business review"), ("TAT", "turnaround time"),
             ("SOP", "standard operating procedure"), ("CAPA", "corrective and preventive action"),
             ("BAU", "business as usual")]
    sel = rng.sample(terms, rng.randint(3, 6))
    return "Glossary\n" + "\n".join("  %s - %s." % t for t in sel)


def _f_other_case(rng, d, c):
    n = rng.randint(1000, 9999)
    return rng.choice([
        "Unrelated item for the same meeting: %s-%d (a %s opened by %s) was closed last week after the requester "
        "withdrew it. No further action; listed here only so the tracker count reconciles." % (c["rid"], n, d["req"], person(rng)),
        "FYI from the weekly digest: %d %ss were handled last month, %d%% within target. The backlog in the %s is "
        "down from %d to %d items. These figures are informational and do not affect individual decisions."
        % (rng.randint(80, 900), d["req"], rng.randint(78, 97), rng.choice(d["hnoun"]), rng.randint(40, 90), rng.randint(5, 39)),
        "Separate case %s-%d is on hold pending documents from the requester; please do not merge it with this one. "
        "%s is the owner and will update the thread when the documents arrive." % (c["rid"], n, person(rng))])


def _f_retention(rng, d, c):
    return ("Section %d - Record retention. Working papers for each %s are kept for %d years after closure and then "
            "destroyed under the %s schedule. Copies held in personal drives must be deleted within %d days. This "
            "section does not govern routing, scoring or selection decisions."
            % (rng.randint(8, 14), d["req"], rng.randint(3, 10), rng.choice(["standard", "enterprise", "records"]), rng.randint(15, 60)))


def _f_contacts(rng, d, c):
    lines = ["Escalation contacts (for outages of the ticketing tool only):"]
    for _ in range(rng.randint(3, 4)):
        lines.append("  - %s, %s, ext. %d" % (person(rng), rng.choice(["tooling admin", "service owner", "backup admin", "duty manager"]), rng.randint(2000, 7999)))
    return "\n".join(lines)


def _f_training(rng, d, c):
    return rng.choice([
        "Reminder: annual %s training must be completed by %s. Staff who miss the deadline lose portal access until it "
        "is done. Training status is not a routing or scoring criterion." % (rng.choice(["ethics", "security awareness", "records management"]),
                                                                               fmt_date(c["date"] + datetime.timedelta(days=rng.randint(20, 90)), 2)),
        "Announcement: the %s cafeteria will close early on Fridays during the renovation. The shuttle schedule "
        "is unchanged." % rng.choice(["north", "main", "annex"])])


def _f_ooo(rng, d, c):
    return ("Auto-reply: I am out of the office until %s with limited access to email. For anything urgent contact "
            "%s. - %s" % (fmt_date(c["date"] + datetime.timedelta(days=rng.randint(3, 14)), 1), person(rng), person(rng)))


def _f_metrics(rng, d, c):
    return ("Quarterly dashboard snapshot (context only): volume %s %s, median handling time %.1f h, customer "
            "satisfaction %d/100, rework rate %d%%. Targets for next quarter are under review by the steering group."
            % (commas(rng.randint(1200, 48000)), d["unit"], rng.randint(12, 90) / 10.0, rng.randint(60, 95), rng.randint(2, 15)))


def _f_faq(rng, d, c):
    q = rng.choice([("Can I print the %s packet?" % d["req"], "Yes, but printed copies must be shredded after use."),
                    ("Who updates the portal banner?", "The communications team, on request via the intranet form."),
                    ("Where are templates stored?", "In the shared drive under /templates/%s." % d["req"].replace(" ", "_")),
                    ("Can the deadline be extended?", "Only for reasons unrelated to this document; see the separate extension policy.")])
    return "FAQ\nQ: %s\nA: %s" % q


def _f_legal(rng, d, c):
    return ("Disclaimer: This guidance summarizes internal procedure and is not legal advice. Where local law "
            "imposes stricter requirements, local law prevails. Headings are for convenience and do not affect "
            "interpretation. Examples are illustrative and non-exhaustive.")


def _f_meeting(rng, d, c):
    items = rng.sample(["parking allocation", "Q%d budget re-forecast" % rng.randint(1, 4), "new badge readers",
                        "vendor holiday party", "office plant watering rota", "ticket tool upgrade window",
                        "hiring for two open roles", "update to the style guide"], 3)
    return "Minutes excerpt (other agenda items):\n" + "\n".join("  * %s - discussed, no decision." % i for i in items)


def _f_future_closure(rng, d, c):
    return ("Planning note: offices will close for the %s shutdown in %d. Dates will be confirmed next year; nothing "
            "in this note applies to current requests." % (rng.choice(["winter", "summer", "inventory"]), c["date"].year + 1))


def _f_boiler_clause(rng, d, c):
    return rng.choice([
        "Section %d - Complaints. Complaints about service quality go to the complaints mailbox and are acknowledged "
        "within %d business days. Complaints are tracked separately from %ss." % (rng.randint(15, 22), rng.randint(2, 5), d["req"]),
        "Section %d - Language. Correspondence is issued in the requester's preferred language where available. "
        "Translation requests do not pause any clock." % rng.randint(15, 22),
        "Section %d - Audit. Internal audit may sample closed items. Sampled items are frozen for %d days."
        % (rng.randint(15, 22), rng.randint(5, 20))])


FILLERS = [_f_confidential, _f_revision, _f_glossary, _f_other_case, _f_retention, _f_contacts, _f_training,
           _f_ooo, _f_metrics, _f_faq, _f_legal, _f_meeting, _f_future_closure, _f_boiler_clause]


_ART = re.compile(r"\b([Aa]) (?=(?:[aeio](?!ne\b)|under))")


def fix_articles(text):
    return _ART.sub(lambda m: m.group(1) + "n ", text)


def assemble(rng, sections, bucket, d, ctx, fixed_head=1):
    """Join core sections; pad with irrelevant filler to hit the length bucket."""
    return fix_articles(_assemble(rng, sections, bucket, d, ctx, fixed_head))


def _assemble(rng, sections, bucket, d, ctx, fixed_head=1):
    secs = list(sections)
    text = "\n\n".join(secs)
    if bucket == "short":
        return text
    lo, hi = BUCKET_RANGE[bucket]
    if bucket == "medium":
        target = rng.randint(max(lo + 40, min(len(text), hi - 200)), hi - 150)
    else:
        target = rng.randint(max(lo + 150, min(len(text), hi - 600)), hi - 300)
    used = set()
    tries = 0
    while len(text) < target and tries < 60:
        tries += 1
        f = rng.choice(FILLERS)
        if f in used and len(used) < len(FILLERS) - 2:
            continue
        piece = f(rng, d, ctx)
        if len(text) + len(piece) + 2 > hi - 20:
            continue
        used.add(f)
        pos = rng.randint(fixed_head, len(secs))
        secs.insert(pos, piece)
        text = "\n\n".join(secs)
    return text


# --------------------------------------------------------------------------------------------
# record renderers (catalogs, score sheets)
# --------------------------------------------------------------------------------------------
def render_records(rng, records, cols, style, prose=None):
    """records: list of (name, {col: str}); cols: ordered column names."""
    if style == "table":
        widths = [max(len("Name"), max(len(r[0]) for r in records))]
        for c in cols:
            widths.append(max(len(c), max(len(r[1][c]) for r in records)))
        head = " | ".join(h.ljust(w) for h, w in zip(["Name"] + cols, widths))
        out = [head, "-+-".join("-" * w for w in widths)]
        for name, vals in records:
            out.append(" | ".join(v.ljust(w) for v, w in zip([name] + [vals[c] for c in cols], widths)))
        return "\n".join(out)
    if style == "ctable":
        out = [" | ".join(["Name"] + cols)]
        for name, vals in records:
            out.append(" | ".join([name] + [vals[c] for c in cols]))
        return "\n".join(out)
    if style == "bullets":
        return "\n".join("- %s: %s" % (n, "; ".join("%s %s" % (c.lower(), v[c]) for c in cols)) for n, v in records)
    if style == "json":
        rows = []
        for n, v in records:
            obj = {"name": n}
            for c in cols:
                obj[c.lower().replace(" ", "_")] = v[c]
            rows.append(json.dumps(obj))
        return "[\n  " + ",\n  ".join(rows) + "\n]"
    if style == "numbered":
        out = []
        for i, (n, v) in enumerate(records, 1):
            out.append("%d. %s" % (i, n))
            for c in cols:
                out.append("   %s: %s" % (c, v[c]))
        return "\n".join(out)
    if style == "yaml":
        out = []
        for n, v in records:
            out.append("- name: %s" % n)
            for c in cols:
                out.append("  %s: %s" % (c.lower().replace(" ", "_"), v[c]))
        return "\n".join(out)
    # prose
    paras = []
    for n, v in records:
        bits = [prose[c](v[c]) if prose and c in prose else "%s is %s" % (c.lower(), v[c]) for c in cols]
        if len(bits) == 1:
            paras.append("%s %s." % (n, bits[0]))
        else:
            paras.append("%s %s, and %s." % (n, ", ".join(bits[:-1]), bits[-1]))
    return "\n".join(paras)


REC_STYLES = ["table", "bullets", "json", "numbered", "yaml", "prose"]


def render_rules(rng, rules, style):
    if style == 0:
        return "\n".join("%d. %s" % (i, r) for i, r in enumerate(rules, 1))
    if style == 1:
        return "\n".join("- %s" % r for r in rules)
    if style == 2:
        return " ".join(rules)
    sec = rng.randint(2, 7)
    return "\n".join("%d.%d  %s" % (sec, i, r) for i, r in enumerate(rules, 1))


# ============================================================================================
# (a) ROUTE: tool / team / API routing with hard constraints
# ============================================================================================

CLEAR_SETS = [["Public", "Internal", "Confidential", "Restricted"], ["Tier 0", "Tier 1", "Tier 2", "Tier 3"],
              ["Green", "Amber", "Red", "Black"], ["L1", "L2", "L3", "L4"]]
REGION_LABELS = {"EU": ["EU (Frankfurt)", "EU (Dublin)", "EU (Paris)"], "US": ["US (Virginia)", "US (Oregon)", "US (Ohio)"],
                 "UK": ["UK (London)"], "Canada": ["Canada (Montreal)", "Canada (Toronto)"],
                 "APAC": ["APAC (Singapore)", "APAC (Tokyo)"], "Australia": ["Australia (Sydney)"],
                 "Brazil": ["Brazil (Sao Paulo)"], "India": ["India (Mumbai)"], "Switzerland": ["Switzerland (Zurich)"]}
DAYSETS = [("Mon-Fri", (0, 1, 2, 3, 4)), ("Mon-Sat", (0, 1, 2, 3, 4, 5)), ("Tue-Sat", (1, 2, 3, 4, 5)),
           ("Sun-Thu", (6, 0, 1, 2, 3)), ("Sat-Sun", (5, 6)), ("Wed-Sun", (2, 3, 4, 5, 6)), ("Daily", (0, 1, 2, 3, 4, 5, 6))]
DAYSET_MAP = dict(DAYSETS)
ZONES = [("ET", -4), ("CT", -5), ("PT", -7), ("CET", 1), ("CEST", 2), ("JST", 9), ("AEST", 10)]


def sg(unit):
    return unit[:-1] if unit.endswith("s") else unit


def rnd15(rng, lo, hi):
    lo = -(-lo // 15) * 15
    hi = hi // 15 * 15
    if lo > hi:
        return None
    return rng.randrange(lo, hi + 1, 15)


def dec_str(fr):
    fr = Fraction(fr)
    s = str(Decimal(fr.numerator) / Decimal(fr.denominator))
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


# ---------------------------------------------------------------- capability
def c_cap(rng, d, ctx, fails, h, bucket):
    need = rng.sample(d["caps"], rng.choice([1, 1, 2]))
    pool = [c for c in d["caps"] if c not in need]
    vals, ok, trap, tagged_any = [], [], {}, False
    for i, f in enumerate(fails):
        items = [(c, "") for c in rng.sample(pool, rng.randint(1, 3))]
        if not f:
            items += [(c, "") for c in need]
            if rng.random() < 0.2:
                extra = rng.choice([c for c in pool if c not in [x[0] for x in items]] or pool)
                items.append((extra, rng.choice(["pilot", "planned"])))
        else:
            drop = rng.choice(need)
            items += [(c, "") for c in need if c != drop]
            if rng.random() < 0.45:
                items.append((drop, rng.choice(["pilot", "planned"])))
                trap[i] = "counted a pilot/planned capability"
            else:
                trap[i] = "missing a required capability"
        rng.shuffle(items)
        tagged_any = tagged_any or any(t for _, t in items)
        ok.append(set(need) <= {c for c, t in items if not t})
        vals.append(", ".join(c + (" (%s)" % t if t else "") for c, t in items))
    ok2 = []
    for v in vals:
        live = [p for p in v.split(", ") if not (p.endswith(" (pilot)") or p.endswith(" (planned)"))]
        ok2.append(all(n in live for n in need))
    rules = [rng.choice(["The %s must support every capability the %s requires." % (h, d["req"]),
                         "Never route to a %s that lacks any of the required capabilities." % h,
                         "A %s qualifies only if its capability list covers all required capabilities." % h])]
    if tagged_any or rng.random() < 0.4:
        rules.append("Capabilities tagged (pilot) or (planned) are not in production and do not count.")
    req = ["Required capabilit%s: %s" % ("ies" if len(need) > 1 else "y", " and ".join(need))]
    return dict(terse="Must have every required capability%s." % ("; (pilot)/(planned) ones do not count" if tagged_any else ""), key="cap", col="Capabilities", vals=vals, ok=ok, ok2=ok2, trap=trap, rules=rules, req=req,
                prose=lambda v: "supports " + v)


# ---------------------------------------------------------------- data residency
def c_region(rng, d, ctx, fails, h, bucket):
    R = rng.choice(list(REGION_LABELS))
    others = [r for r in REGION_LABELS if r != R]
    vals, ok, trap, cue = [], [], {}, {}
    for i, f in enumerate(fails):
        regs = ([R] if not f else []) + rng.sample(others, rng.randint(0 if not f else 1, 2))
        rng.shuffle(regs)
        ok.append(R in regs)
        vals.append(", ".join(rng.choice(REGION_LABELS[r]) for r in regs))
        if f:
            trap[i] = "wrong data-residency region"
            if not cue and rng.random() < 0.5:
                cue[i] = R
                trap[i] = "trusted the name, not the hosting region"
    ok2 = [R in [p.split(" (")[0] for p in v.split(", ")] for v in vals]
    rules = [rng.choice(["Data must be processed in the required residency region: only a %s hosted there may be used." % h,
                         "No %s may be sent to a %s that does not host data in the required region." % (d["req"], h),
                         "The destination's hosting locations must include the %s's residency region; names and "
                         "branding are irrelevant." % d["req"]])]
    req = [rng.choice(["Data residency: %s" % R, "Residency requirement: data must stay in %s" % R])]
    return dict(terse="Must be hosted in the residency region.", key="region", col="Hosting", vals=vals, ok=ok, ok2=ok2, trap=trap, rules=rules, req=req, cue=cue,
                prose=lambda v: "is hosted in " + v)


# ---------------------------------------------------------------- clearance
def c_clear(rng, d, ctx, fails, h, bucket):
    lv = rng.choice(CLEAR_SETS)
    L = rng.randint(1, 3)
    vals, ok, trap = [], [], {}
    for i, f in enumerate(fails):
        if not f:
            c = rng.randint(L, 3)
        else:
            c = L - 1 if rng.random() < 0.7 else rng.randint(0, L - 1)
            trap[i] = "clearance below data classification"
        ok.append(c >= L)
        vals.append(lv[c])
    rank = {name: k for k, name in enumerate(lv)}
    ok2 = [rank[v] - rank[lv[L]] >= 0 for v in vals]
    rules = [rng.choice(["A %s's clearance must be equal to or higher than the data classification." % h,
                         "It is not acceptable to use a %s whose clearance is not at least the classification of the data." % h,
                         "No %s may receive data classified above its clearance." % h]),
             "Clearance order, lowest to highest: %s." % " < ".join(lv)]
    req = ["Data classification: %s" % lv[L]]
    return dict(terse="Clearance must be at least the classification (%s)." % " < ".join(lv), key="clear", col="Clearance", vals=vals, ok=ok, ok2=ok2, trap=trap, rules=rules, req=req,
                prose=lambda v: "is cleared to " + v)


# ---------------------------------------------------------------- staffed hours (+exception to exception, tz)
def _open1(days, o, c, always, t, wd, incl):
    if always:
        return True
    if wd not in days:
        return False
    return o <= t < c or (incl and t == c)


def _window(rng, kind, t, wd):
    with_wd = [lab for lab, ds in DAYSETS if wd in ds]
    if kind == "247":
        return ("24/7", 0, 1440, True)
    if kind in ("in", "edge"):
        c = t if kind == "edge" else rnd15(rng, t + 30, min(1425, t + 600))
        o = rnd15(rng, max(300, c - 720), min(t - 15, c - 120))
        if o is None:
            return None
        return (rng.choice(with_wd), o, c, False)
    if kind == "late":
        c = rnd15(rng, max(420, t - 240), t - 15)
        if c is None:
            return None
        return (rng.choice(with_wd), rnd15(rng, max(300, c - 720), c - 120), c, False)
    if kind == "early":
        o = rnd15(rng, t + 15, min(1305, t + 180))
        if o is None:
            return None
        return (rng.choice(with_wd), o, rnd15(rng, o + 120, min(1425, o + 600)), False)
    if kind == "day":
        lab = rng.choice([lab for lab, ds in DAYSETS if wd not in ds])
        o = rnd15(rng, 360, 600)
        return (lab, o, rnd15(rng, o + 240, min(1425, o + 660)), False)
    raise ValueError(kind)


def c_hours(rng, d, ctx, fails, h, bucket):
    t, wd, ts = ctx["minutes"], ctx["date"].weekday(), ctx["tstyle"]
    incl = rng.random() < 0.5
    mode = rng.choice(["urgent_ok", "urgent_sens", "not_urgent"]) if bucket != "short" and rng.random() < 0.4 else None
    urgent = mode in ("urgent_ok", "urgent_sens") if mode else rng.random() < 0.3
    sens = mode == "urgent_sens" if mode else rng.random() < 0.3
    if bucket != "short" and rng.random() < 0.3:
        zone, off = rng.choice(ZONES)
        utc = t - off * 60
        if 0 <= utc < 1440:
            ctx["tz"] = (zone, off, utc)
    structs, trap = [], {}
    for i, f in enumerate(fails):
        if not f:
            kinds = ["in", "in", "247"] + (["edge"] if incl else []) + (["onc", "onc"] if mode == "urgent_ok" else [])
        else:
            kinds = ["late", "early", "day"] + (["edge", "edge"] if not incl else []) + \
                    (["onc", "onc"] if mode in ("urgent_sens", "not_urgent") else [])
        win = None
        while win is None:
            kind = rng.choice(kinds)
            win = _window(rng, rng.choice(["late", "early", "day"]) if kind == "onc" else kind, t, wd)
        onc = kind == "onc" or (not f and kind != "247" and rng.random() < 0.12 and mode is None)
        structs.append(win + (onc,))
        if f:
            trap[i] = {"edge": "treated the exclusive closing time as open", "late": "outside staffed hours",
                       "early": "outside staffed hours", "day": "not staffed on that weekday",
                       "onc": ("on-call exception excludes %s" % d["sens"]) if mode == "urgent_sens"
                       else "on-call exception is only for %s requests" % d["urgent"]}[kind]
            if ctx.get("tz") and kind != "onc":
                lab, o, c, al, _ = structs[-1]
                if _open1(DAYSET_MAP[lab], o, c, al, ctx["tz"][2], wd, incl):
                    trap[i] = "did not convert UTC to local time"
    ok, ok2, vals = [], [], []
    tt = datetime.time(t // 60, t % 60)
    for lab, o, c, al, onc in structs:
        exc = onc and urgent and not sens
        ok.append(_open1(DAYSET_MAP.get(lab, ()), o, c, al, t, wd, incl) or exc)
        if lab == "24/7":
            p2 = True
        else:
            to = datetime.time(o // 60, o % 60)
            tc = datetime.time(c // 60, c % 60)
            p2 = WD3[wd] in [WD3[k] for k in DAYSET_MAP[lab]] and to <= tt and (tt < tc or (incl and tt == tc))
        ok2.append(p2 or (onc and urgent and not sens))
        v = "24/7" if al else "%s %s-%s" % (lab, fmt_time(o, ts), fmt_time(c, ts))
        vals.append(v + (" + after-hours on-call" if onc else ""))
    rules = [rng.choice(["A %s may only receive a %s during its staffed hours as listed." % (h, d["req"]),
                         "Do not route to a %s that is not staffed at the moment of submission." % h,
                         "The destination must be inside its listed staffed days and times at submission."])]
    rules.append("Closing times are inclusive: a submission at exactly the closing time is still within hours."
                 if incl else "Closing times are exclusive: a submission at exactly the closing time counts as after hours.")
    if mode or any(s[4] for s in structs):
        rules.append("Outside staffed hours, a %s marked 'after-hours on-call' may accept %s %ss. This exception does "
                     "not apply to any %s involving %s; those may only go to a %s inside its staffed hours."
                     % (h, d["urgent"], d["req"], d["req"], d["sens"], h))
    if ctx.get("tz"):
        rules.append("All catalog hours are local %s time (UTC%+d); convert the submission time before comparing."
                     % (ctx["tz"][0], ctx["tz"][1]))
    req = []
    if mode or rng.random() < 0.5:
        req.append("Priority: %s" % (d["urgent"] if urgent else "routine"))
        req.append("Involves %s: %s" % (d["sens"], "yes" if sens else "no"))
    return dict(terse="Must be staffed at submission; closing time is %s." % ("inclusive" if incl else "exclusive"), key="hours", col="Staffed hours", vals=vals, ok=ok, ok2=ok2, trap=trap, rules=rules, req=req,
                prose=lambda v: "is staffed " + v)


# ---------------------------------------------------------------- cost / budget
def _price_str(p, fmt, unit):
    """p = price per unit in units of $0.0001."""
    if fmt == 0:
        return "$%s per %s" % (dec_str(Fraction(p, 10000)), sg(unit))
    if fmt == 1:
        return "$%.2f per 1,000 %s" % (p / 10.0, unit)
    if fmt == 2:
        return "%s cents per %s" % (dec_str(Fraction(p, 100)), sg(unit))
    return "$%s per 10,000 %s" % (commas(p), unit)


def _parse_price(v):
    m = re.match(r"^\$?([\d.,]+)( cents)? per (1,000 |10,000 )?", v)
    amt = Decimal(m.group(1).replace(",", ""))
    if m.group(2):
        amt = amt / 100
    basis = {None: 1, "1,000 ": 1000, "10,000 ": 10000}[m.group(3)]
    fee = Decimal(0)
    mf = re.search(r"\+ \$([\d,]+) setup fee", v)
    if mf:
        fee = Decimal(mf.group(1).replace(",", ""))
    return amt / basis, fee


def c_cost(rng, d, ctx, fails, h, bucket):
    N = rng.choice([4000, 5000, 8000, 12000, 20000, 25000, 40000, 50000])
    pstar = rng.randrange(20, 160, 10)
    B = pstar * N // 10000
    strict = rng.random() < 0.4
    unit = d["unit"]
    vals, ok, trap = [], [], {}
    for i, f in enumerate(fails):
        fee = 0 if rng.random() < 0.65 or B < 100 else rng.randrange(20, B // 4, 5)
        cap = Fraction(B - fee) * 10000 / N
        pmax = int(cap) - (1 if strict and cap.denominator == 1 else 0)
        if not f:
            if fee == 0 and not strict and rng.random() < 0.3:
                p = pstar
            else:
                p = rng.randint(max(1, pmax - 25), pmax)
        else:
            kinds = ["over", "over"] + (["fee"] if fee else []) + (["edge"] if strict and fee == 0 else [])
            kind = rng.choice(kinds)
            if kind == "fee" and int(cap) + 1 <= pstar - (1 if strict else 0):
                p = rng.randint(int(cap) + 1, pstar - (1 if strict else 0))
                trap[i] = "forgot the setup fee"
            elif kind == "edge":
                p = pstar
                trap[i] = "treated a strict budget cap as inclusive"
            else:
                p = int(cap) + 1 + rng.randint(0, 15)
                trap[i] = "over budget"
        total = Fraction(p * N, 10000) + fee
        ok.append(total < B if strict else total <= B)
        fmt = rng.choice([0, 1, 1, 2, 3])
        vals.append(_price_str(p, fmt, unit) + (" + $%s setup fee" % commas(fee) if fee else ""))
    ok2 = []
    for v in vals:
        per, fee = _parse_price(v)
        tot = per * N + fee
        ok2.append(tot < Decimal(B) if strict else tot <= Decimal(B))
    if strict:
        rules = [rng.choice(["The total charge for the job (unit price x volume, plus any setup fee) must be strictly "
                             "below the budget; a quote exactly equal to the budget is rejected.",
                             "A %s is eligible only if its all-in cost for the whole volume is less than the budget "
                             "(equal is not enough)." % h])]
    else:
        rules = [rng.choice(["The total charge for the job (unit price x volume, plus any setup fee) must not exceed the budget.",
                             "A %s is not eligible unless its all-in cost for the whole volume is no more than the budget." % h])]
    req = ["Volume: %s %s" % (commas(N), unit), "Budget: %s all-in for the job" % fmt_money(B, cents=False)]
    return dict(terse="Total (unit price x volume + setup fee) must be %s the budget." % ("below" if strict else "at most"), key="cost", col="Pricing", vals=vals, ok=ok, ok2=ok2, trap=trap, rules=rules, req=req,
                prose=lambda v: "charges " + v)


# ---------------------------------------------------------------- latency (+ superseded standard)
def _lat_str(ms, rng):
    if ms % 10 == 0 and rng.random() < 0.4:
        return "%s s" % dec_str(Fraction(ms, 1000))
    return "%s ms" % commas(ms)


def _parse_lat(v):
    num, u = v.split(" ")
    x = Fraction(Decimal(num.replace(",", "")))
    return x if u == "s" else x / 1000


def c_latency(rng, d, ctx, fails, h, bucket):
    Lnew = rng.choice([800, 1000, 1200, 1500, 2000, 2500, 3000, 4000])
    strict = rng.random() < 0.35
    sup = bucket != "short" and rng.random() < 0.45
    date = ctx["date"]
    if sup:
        Lold = rng.choice([v for v in [600, 800, 1000, 1200, 1500, 2000, 2500, 3000, 4000, 5000] if abs(v - Lnew) >= 300])
        E = date + datetime.timedelta(days=rng.randint(1, 40)) if rng.random() < 0.3 else \
            date - datetime.timedelta(days=rng.choice([0, 0, rng.randint(1, 120)]))
        A, W = (Lnew, Lold) if date >= E else (Lold, Lnew)
        sup_label = "applied the superseded latency limit" if date >= E else "applied the revision before its effective date"
    else:
        A, W, E = Lnew, None, None
    passes = (lambda x, lim: x < lim) if strict else (lambda x, lim: x <= lim)
    vals, ok, trap = [], [], {}
    for i, f in enumerate(fails):
        if not f:
            x = A if (not strict and rng.random() < 0.2) else rng.randrange(max(50, A - 1500), A - (10 if strict else 0) + 1, 10)
        else:
            kinds = ["over"] + (["edge"] if strict else []) + (["sup", "sup"] if sup and W > A else [])
            kind = rng.choice(kinds)
            if kind == "sup":
                x = rng.randrange(A + 10, W - (10 if strict else 0) + 1, 10)
                trap[i] = sup_label
            elif kind == "edge":
                x = A
                trap[i] = "treated a strict latency limit as inclusive"
            else:
                x = A + rng.randint(1, 8) * 50
                trap[i] = "latency above the limit"
        ok.append(passes(x, A))
        vals.append(_lat_str(x, rng))
    A2 = (Lnew if E is None or date.toordinal() >= E.toordinal() else Lold)
    ok2 = [(_parse_lat(v) < Fraction(A2, 1000)) if strict else (_parse_lat(v) <= Fraction(A2, 1000)) for v in vals]
    cmpw = "under" if strict else "at most"
    if sup:
        dstyle = ctx["dstyle"]
        rules = ["Latency standard rev. B (effective %s): p95 response time must be %s %s. Requests submitted before "
                 "that date remain under rev. A, which required %s %s." % (fmt_date(E, dstyle), cmpw, _lat_str(Lnew, rng),
                                                                         cmpw, _lat_str(Lold, rng))]
    else:
        rules = [rng.choice(["The %s's p95 response time must be %s %s." % (h, cmpw, _lat_str(A, rng)),
                             "A %s whose p95 latency is not %s %s must not be used." % (h, "below" if strict else "within", _lat_str(A, rng))])]
    if strict:
        rules.append("A p95 exactly equal to the limit fails.")
    return dict(terse="p95 latency must be %s %s." % (cmpw, _lat_str(A, rng)), key="latency", col="p95 latency", vals=vals, ok=ok, ok2=ok2, trap=trap, rules=rules, req=[],
                prose=lambda v: "has a p95 response time of " + v)


# ---------------------------------------------------------------- lifecycle / deprecation
def c_sunset(rng, d, ctx, fails, h, bucket):
    D = ctx["date"]
    sem = rng.choice(["sunset", "last"])
    dstyle = ctx["dstyle"]
    vals, ok, trap, dates = [], [], {}, []
    for i, f in enumerate(fails):
        if not f:
            kind = rng.choice(["active", "active", "future"] + (["edge"] if sem == "last" else []))
            if kind == "active":
                x = None
            elif kind == "future":
                x = D + datetime.timedelta(days=rng.randint(1, 90))
            else:
                x = D
        else:
            kind = rng.choice(["past", "edge", "edge"])
            if kind == "edge":
                x = D if sem == "sunset" else D - datetime.timedelta(days=1)
                trap[i] = "off-by-one on the %s date" % ("sunset" if sem == "sunset" else "last service")
            else:
                x = D - datetime.timedelta(days=rng.randint(2, 200))
                trap[i] = "used a retired %s" % h
        dates.append(x)
        if x is None:
            ok.append(True)
            vals.append(rng.choice(["active", "generally available", "supported"]))
        else:
            ok.append(D < x if sem == "sunset" else D <= x)
            vals.append(("deprecated, sunset %s" if sem == "sunset" else "deprecated, last day of service %s") % fmt_date(x, dstyle))
    ok2 = [x is None or ((x.toordinal() - D.toordinal()) > 0 if sem == "sunset" else (x.toordinal() - D.toordinal()) >= 0)
           for x in dates]
    if sem == "sunset":
        rules = [rng.choice(["A deprecated %s may be used before its sunset date, but not on or after it." % h,
                             "On its sunset date and afterwards a %s is unavailable." % h])]
    else:
        rules = [rng.choice(["A deprecated %s remains usable through its last day of service (inclusive), not after." % h,
                             "A %s may still be used on its last day of service, but not on any later day." % h])]
    rules.append("Only the lifecycle field determines availability, whatever the %s's name suggests." % h)
    return dict(terse=("Unusable on or after its sunset date." if sem == "sunset" else "Usable through its last day of service (inclusive)."), key="sunset", col="Lifecycle", vals=vals, ok=ok, ok2=ok2, trap=trap, rules=rules, req=[],
                prose=lambda v: "is " + v)


# ---------------------------------------------------------------- payload size
def _size_str(kb, unit):
    if unit == "KB":
        return "%s KB" % commas(kb)
    if unit == "MB":
        return "%s MB" % dec_str(Fraction(kb, 1000))
    return "%s GB" % dec_str(Fraction(kb, 1000000))


def _parse_size(v):
    num, u = v.split(" ")
    return Fraction(Decimal(num.replace(",", ""))) * {"KB": 1, "MB": 1000, "GB": 1000000}[u]


def c_payload(rng, d, ctx, fails, h, bucket):
    S = rng.choice([2, 5, 8, 12, 25, 40, 75, 120, 250, 400, 750]) * 1000
    ru = rng.choice(["MB", "MB", "KB", "GB"])
    vals, ok, trap = [], [], {}
    for i, f in enumerate(fails):
        u = rng.choice(["KB", "MB", "MB", "GB"])
        if not f:
            x = S if rng.random() < 0.2 else S + rng.choice([500, 1000, 5000, 10000, 50000, 250000])
        else:
            x = S - rng.choice([500, S // 10, S // 5, S // 2])
            trap[i] = "bundle exceeds the size limit" if u == ru else "unit mix-up (KB/MB/GB)"
        ok.append(x >= S)
        vals.append(_size_str(x, u))
    ok2 = [_parse_size(v) >= _parse_size(_size_str(S, ru)) for v in vals]
    rules = [rng.choice(["The %s's maximum upload size must be at least the size of the attachment bundle "
                         "(an upload exactly at the limit is accepted)." % h,
                         "A %s cannot be used if the attachment bundle is larger than its upload limit; equal is fine." % h]),
             "Units are decimal: 1 GB = 1,000 MB = 1,000,000 KB."]
    req = ["Attachment bundle: %s" % _size_str(S, ru)]
    return dict(terse="Max upload must be >= bundle size (1 GB = 1,000 MB = 1,000,000 KB).", key="payload", col="Max upload", vals=vals, ok=ok, ok2=ok2, trap=trap, rules=rules, req=req,
                prose=lambda v: "accepts uploads up to " + v)


CONS = {"cap": c_cap, "region": c_region, "clear": c_clear, "hours": c_hours, "cost": c_cost,
        "latency": c_latency, "sunset": c_sunset, "payload": c_payload}


TRICKY = ("off-by-one", "strict", "superseded", "effective", "UTC", "exception", "pilot", "name", "fee", "unit",
          "unauthorized", "exclusive", "precedent", "draft", "cumulative", "weights", "knock", "tie", "band", "version")


def _difficulty(bucket, mistakes, extra=0):
    tricky = sum(1 for v in set(mistakes.values()) if any(k in v for k in TRICKY)) + extra
    return "hard" if (tricky >= 2 or bucket == "long") else "medium"


def _note(rng, target, h, d):
    p, role = person(rng), rng.choice(JUNIOR)
    return rng.choice([
        "Comment from %s (%s): \"%s handled the last one of these, just send it there.\"" % (p, role, target),
        "Chat message from %s (%s): pretty sure %s is the right place, they're usually fastest." % (p, role, target),
        "Sticky note on the ticket (%s, %s): route to %s?" % (p, role, target),
        "%s (%s) wrote: \"Honestly I'd go with %s - it's what my old team always did.\"" % (p, role, target)])


def gen_route(rng, bucket, qtype, want, dk=None):
    d = DOMAINS[dk or rng.choice(DOMAIN_KEYS)]
    h = rng.choice(d["hnoun"])
    ctx = dict(co=rng.choice(COMPANIES), rid=d["rid"], date=rand_date(rng), minutes=rng.randrange(420, 1231, 15),
               tstyle=rng.randint(0, 1), dstyle=rng.randint(0, 3), tz=None)
    if bucket == "short":
        K, H = 2, 4
        keys = rng.sample(["region", "clear", "latency", "payload", "sunset", "hours", "region", "clear", "cost", "cap"], 4)
        keys = list(dict.fromkeys(keys))[:2]
    elif bucket == "medium":
        K, H = rng.choice([2, 3, 3, 4]), rng.randint(4, 6)
    else:
        K, H = rng.choice([3, 4, 4, 5]), rng.randint(5, 8)
    esc = qtype == "choice" and H < 8 and rng.random() < 0.25
    gold_esc = esc and rng.random() < 0.4
    if bucket != "short":
        keys = rng.sample(sorted(CONS), K)
    g = None if gold_esc else rng.randrange(H)
    cyc, fail_of, j = shuffled(rng, keys), {}, 0
    for i in range(H):
        if i != g:
            fail_of[i] = cyc[j % K]
            j += 1
    cons = [CONS[k](rng, d, ctx, [fail_of.get(i) == k for i in range(H)], h, bucket) for k in keys]
    ok1 = [all(c["ok"][i] for c in cons) for i in range(H)]
    ok2 = [all(c["ok2"][i] for c in cons) for i in range(H)]
    assert ok1 == [i == g for i in range(H)], "route engine disagrees with construction"
    assert ok1 == ok2, "route independent check failed"
    names = rng.sample(d["handlers"], H)
    for c in cons:
        for i, R in c.get("cue", {}).items():
            names[i] = "%s %s" % (R, names[i])
    mist = {i: cons[keys.index(fail_of[i])]["trap"].get(i, "violates a routing rule") for i in fail_of}
    rid = "%s-%d" % (d["rid"], rng.randint(10000, 99999))
    wd = ctx["date"].weekday()
    tz = ctx.get("tz")
    when = "%s%s at %s %s" % ("" if ctx["dstyle"] == 3 else WEEKDAYS[wd] + ", ", fmt_date(ctx["date"], ctx["dstyle"]),
                                fmt_time(tz[2] if tz else ctx["minutes"], ctx["tstyle"]), "UTC" if tz else "(local time)")
    facts = ["Submitted: " + when] + [x for c in cons for x in c["req"]]
    # notes
    notes = []
    note_target = None
    if rng.random() < (0.25 if bucket == "short" else 0.5):
        fails = sorted(fail_of)
        note_target = rng.choice(fails) if (g is None or rng.random() < 0.75) else g
        notes.append(_note(rng, names[note_target], h, d))
        if note_target in fail_of:
            mist[note_target] = "followed an unauthorized suggestion"
    if bucket != "short" and rng.random() < 0.3:
        y = rng.choice(sorted(fail_of))
        notes.append("History: %s-%d, a similar %s, went to %s in %s." % (
            d["rid"], rng.randint(10000, 99999), d["req"], names[y], (ctx["date"] - datetime.timedelta(days=rng.randint(40, 300))).strftime("%B %Y")))
    # rules
    rules = []
    for c in shuffled(rng, cons):
        rules += [c["terse"]] if bucket == "short" else c["rules"]
    if esc or (bucket != "short" and rng.random() < 0.3):
        rules.append("If no %s satisfies every rule, escalate the %s for manual review." % (h, d["req"]))
    if notes and rng.random() < 0.5:
        rules.append("Only these rules decide eligibility; suggestions from staff without routing authority are not binding.")
    email = bucket != "short" and rng.random() < 0.2
    rstyle = rng.randint(0, 3)
    intro = "Rules (all must hold):" if bucket == "short" else rng.choice(["Routing rules (all must hold):", "Eligibility rules for any %s:" % h,
                        "POLICY - a %s may be routed only to a %s that meets every rule below." % (d["req"], h), "Rules:"])
    rules_txt = intro + "\n" + render_rules(rng, rules, rstyle)
    cols = [c["col"] for c in cons]
    recs = [(names[i], {c["col"]: c["vals"][i] for c in cons}) for i in range(H)]
    cstyle = rng.choice(["ctable", "ctable", "bullets"] if bucket == "short" else REC_STYLES)
    prose = {c["col"]: c["prose"] for c in cons}
    cat_txt = "Catalog:\n" + render_records(rng, recs, cols, cstyle, prose) if bucket == "short" else rng.choice(["Catalog:", "Available %ss:" % h, "Directory extract (%d):" % ctx["date"].year,
                          "%s catalog" % h.capitalize()]) + "\n" + render_records(rng, recs, cols, cstyle, prose)
    if email:
        sender = person(rng)
        req_txt = ("From: %s\nTo: %s routing desk\nSubject: %s - which %s?\n\nHi all,\nnew %s %s just came in. %s. "
                   "Thanks, %s" % (sender, ctx["co"], rid, h, d["req"], rid, ". ".join(facts), sender.split()[0]))
        notes = ["-----\nReply: " + n for n in notes]
        head = []
    else:
        st = rng.randint(0, 2) if bucket != "short" else 1
        if st == 0:
            req_txt = "Request %s (%s)\n" % (rid, d["req"]) + "\n".join("- " + f for f in facts)
        elif st == 1 and bucket == "short":
            req_txt = "%s %s. %s." % (d["req"].capitalize(), rid, "; ".join(facts))
        elif st == 1:
            req_txt = "Incoming %s %s. %s." % (d["req"], rid, ". ".join(facts))
        else:
            obj = {"id": rid, "type": d["req"]}
            for f in facts:
                k, v = f.split(": ", 1)
                obj[k.lower().replace(" ", "_")] = v
            req_txt = json.dumps(obj, indent=1)
        head = [] if bucket == "short" else [rng.choice(["%s %s - %s routing" % (ctx["co"], d["org"], d["req"]),
                                                          "Dispatch guide: %ss (%s %s)" % (d["req"], ctx["co"], d["org"]),
                                                          "%s %s | Operations manual excerpt" % (ctx["co"], d["org"])])]
    body = [rules_txt, cat_txt] if rng.random() < 0.7 else [cat_txt, rules_txt]
    core = head + [req_txt] + body + notes
    state = assemble(rng, core, bucket, d, ctx, fixed_head=len(head) + 1)
    esc_txt = rng.choice(["Escalate for manual review (no compliant %s)" % h, "None of the listed %ss - escalate" % h])
    mistakes = {names[i]: m for i, m in mist.items()}
    if qtype == "choice":
        options = names + ([esc_txt] if esc else [])
        gold = esc_txt if gold_esc else names[g]
        if esc and not gold_esc:
            mistakes[esc_txt] = "escalated although a compliant option exists"
        q = rng.choice(["Which %s should %s be routed to?" % (h, rid),
                        "Select the single %s that satisfies every routing rule for %s." % (h, rid),
                        "Where must %s go under the current rules?" % rid,
                        "Pick the compliant destination for this %s." % d["req"],
                        "According to the policy and catalog, what is the correct routing decision for %s?" % rid])
        return dict(state=state, qtype="choice", instructions=q, options=shuffled(rng, options), gold=gold,
                    meta=dict(family=FAMILY, difficulty=_difficulty(bucket, mistakes), mistakes=mistakes))
    if want == 1:
        x = g
    else:
        tricky = [i for i in fail_of if any(k in mist[i] for k in TRICKY)]
        x = rng.choice(tricky) if tricky and rng.random() < 0.7 else rng.choice(sorted(fail_of))
    X = names[x]
    q = rng.choice(["May %s be routed to %s under the current rules? Answer yes or no." % (rid, X),
                    "Is %s an eligible %s for %s?" % (X, h, rid),
                    "Would sending this %s to %s comply with every routing rule?" % (d["req"], X),
                    "Yes or no: %s is a compliant destination for %s." % (X, rid)])
    m = {} if want == 1 else {X: mist[x]}
    return dict(state=state, qtype="noul", instructions=q, options=None, gold=int(ok1[x]),
                meta=dict(family=FAMILY, difficulty=_difficulty(bucket, mistakes), mistakes=m))


# ============================================================================================
# (b) RUBRIC: ordinal scoring, gold = highest fully supported level
# ============================================================================================
def _ustr(v, unit):
    if unit == "%":
        return "%s%%" % v
    if unit == "":
        return str(v)
    return "%s %s" % (v, unit)


def k_num(rng, spec, target, want_trap, ctx):
    _, label, unit, direc, lo, hi = spec
    thr = rng.randint(lo + 3, hi - 3)
    strict = rng.random() < 0.4
    sign = 1 if direc == "hi" else -1
    if direc == "hi":
        cmpw = "more than" if strict else "at least"
    else:
        cmpw = "below" if strict else "at most"

    def good(v, t):
        if direc == "hi":
            return v > t if strict else v >= t
        return v < t if strict else v <= t
    trap = None
    if want_trap and strict and not target:
        v, trap = thr, "treated an exclusive threshold as inclusive"
    elif want_trap and not strict and target:
        v, trap = thr, "treated an inclusive threshold as exclusive"
    else:
        v = thr + sign * rng.randint(1, 4) if target else thr - sign * rng.randint(1, 4)
    if unit == "%" and hi <= 100:
        v = min(v, 100)
    render = lambda t: "%s %s %s" % (label, cmpw, _ustr(t, unit))
    c = dict(kind="num", thr=thr, v=v, good=good, render=render, rule=render(thr), trap=trap, cap100=hi <= 100,
             fact="%s: %s" % (label[0].upper() + label[1:], _ustr(v, unit)), label=label, unit=unit)
    c["met"] = good(v, thr)
    c["eval2"] = lambda t=None: (Fraction(v) - Fraction(t if t is not None else thr)) * sign > 0 or \
        (not strict and Fraction(v) == Fraction(t if t is not None else thr))
    return c


def k_frac(rng, spec, target, want_trap, ctx):
    _, subj, noun = spec
    thr = rng.choice([70, 75, 80, 85, 90, 95])
    n = rng.choice([x for x in [20, 40, 60, 80, 120, 160, 200, 240] if x * thr % 100 == 0])
    b = n * thr // 100
    strict = rng.random() < 0.35
    trap = None
    if want_trap and not target:
        if strict:
            k, trap = b, "treated an exclusive threshold as inclusive"
        else:
            k, trap = b - 1, "rounded the percentage up"
    elif want_trap and target and not strict:
        k, trap = b, "treated an inclusive threshold as exclusive"
    elif target:
        k = min(n, b + rng.randint(1, 3))
    else:
        k = b - rng.randint(2, max(3, n // 10))
    met = k * 100 > thr * n if strict else k * 100 >= thr * n
    pct = Fraction(k * 100, n)
    return dict(kind="frac", rule="%s %d%% of %s" % ("more than" if strict else "at least", thr, subj), trap=trap,
                fact="%s: %d of %d %s" % (subj[0].upper() + subj[1:], k, n, noun), met=met,
                eval2=lambda t=None: pct > thr or (not strict and pct == thr))


def _dur_str(hours, base, rng):
    """Render a duration in a unit different from the rule's base unit."""
    styles = []
    if base == "h":
        if hours >= 24:
            styles.append("dh")
        styles.append("min")
        if hours % 12 == 0 and hours >= 24:
            styles.append("dec")
    else:
        styles.append("h")
        if hours % 24 == 0 and hours >= 7 * 24:
            styles.append("wd")
        if hours >= 24:
            styles.append("dh")
    st = rng.choice(styles)
    if st == "dh":
        dd, hh = divmod(hours, 24)
        return "%d day%s%s" % (dd, "s" if dd != 1 else "", (" %d hour%s" % (hh, "s" if hh != 1 else "")) if hh else "")
    if st == "min":
        return "%s minutes" % commas(hours * 60)
    if st == "dec":
        return "%s days" % dec_str(Fraction(hours, 24))
    if st == "h":
        return "%d hours" % hours
    w, dd = divmod(hours // 24, 7)
    return "%d week%s%s" % (w, "s" if w != 1 else "", (" %d day%s" % (dd, "s" if dd != 1 else "")) if dd else "")


def _parse_dur_hours(s):
    tot = Fraction(0)
    toks = s.replace(",", "").split()
    for i in range(0, len(toks), 2):
        q, u = Fraction(Decimal(toks[i])), toks[i + 1]
        tot += q * {"minutes": Fraction(1, 60), "hour": 1, "hours": 1, "day": 24, "days": 24, "week": 168, "weeks": 168}[u]
    return tot


def k_dur(rng, spec, target, want_trap, ctx):
    _, event, base = spec
    strict = rng.random() < 0.35
    if base == "h":
        thr = rng.choice([24, 36, 48, 72, 96])
        span = max(2, thr // 4)
        lim_txt = "%d hours" % thr
    else:
        td = rng.choice([3, 5, 7, 10, 14, 21])
        thr = td * 24
        span = 30
        lim_txt = "%d days" % td
    trap = None
    if want_trap and strict and not target:
        x, trap = thr, "treated an exclusive time limit as inclusive"
    elif want_trap and not target:
        x, trap = thr + rng.randint(1, 6), "unit conversion error (minutes/hours/days)"
    elif want_trap and target and not strict:
        x, trap = thr, "treated an inclusive time limit as exclusive"
    elif target:
        x = thr - rng.randint(1, span)
    else:
        x = thr + rng.randint(1, span)
    met = x < thr if strict else x <= thr
    fact_d = _dur_str(x, base, rng)
    rule = ("%s in less than %s" if strict else "%s within %s") % (event, lim_txt)
    return dict(kind="dur", rule=rule, trap=trap, fact="%s: %s" % (event[0].upper() + event[1:], fact_d), met=met,
                eval2=lambda t=None: _parse_dur_hours(fact_d) < thr or (not strict and _parse_dur_hours(fact_d) == thr))


def k_date(rng, spec, target, want_trap, ctx):
    _, event = spec
    R = ctx["review"]
    N = rng.choice([30, 60, 90, 180, 365])
    strict = rng.random() < 0.4
    trap = None
    if want_trap and ((strict and not target) or (not strict and target)):
        age = N
        trap = "off-by-one on the date window"
    elif target:
        age = N - rng.randint(1 if not strict else 1, 40)
    else:
        age = N + rng.randint(1, 40)
    age = max(age, 1)
    ev = R - datetime.timedelta(days=age)
    met = age < N if strict else age <= N
    rule = "%s dated %s %d days before the review date" % (event, "fewer than" if strict else "no more than", N)
    return dict(kind="date", rule=rule, trap=trap, fact="%s: %s" % (event[0].upper() + event[1:], fmt_date(ev, ctx["dstyle"])),
                met=met, eval2=lambda t=None: (R.toordinal() - ev.toordinal() < N) or (not strict and R.toordinal() - ev.toordinal() == N))


DOC_OK = ["approved and on file (signed %s)", "final version approved by the owner on %s"]
DOC_BAD = [("draft only, awaiting approval (last edited %s)", "counted an unapproved draft"),
           ("discussed verbally on %s; nothing written", "counted a verbal agreement"),
           ("template downloaded %s, not completed", "counted an incomplete template")]


def k_doc(rng, spec, target, want_trap, ctx):
    _, art = spec
    dt = fmt_date(ctx["review"] - datetime.timedelta(days=rng.randint(5, 200)), ctx["dstyle"])
    if target:
        st, trap = rng.choice(DOC_OK) % dt, None
    else:
        tpl, lab = rng.choice(DOC_BAD[:1] if want_trap else DOC_BAD)
        st, trap = tpl % dt, (lab if want_trap else None)
    return dict(kind="doc", rule="%s: approved written version on file" % art, trap=trap, fact="%s: %s" % (art[0].upper() + art[1:], st),
                met=target, eval2=lambda t=None: st.startswith("approved") or st.startswith("final version approved"))


def k_cnt(rng, spec, target, want_trap, ctx):
    _, item, excl_txt = spec
    N = rng.randint(2, 5)
    trap = None
    if target:
        good = N + rng.randint(0, 2)
        ex = rng.randint(0, 2)
    elif want_trap:
        good, ex = N - 1, rng.randint(1, 3)
        trap = "counted excluded items"
    else:
        good, ex = N - rng.randint(1, 2), rng.randint(0, 1)
    tot = good + ex
    fact = "%s: %d on file, %s" % (item[0].upper() + item[1:], tot,
                                   ("none of them %s" % excl_txt) if ex == 0 else ("including %d in the excluded category (%s)" % (ex, excl_txt)))
    return dict(kind="cnt", rule="at least %d %s (%s do not count)" % (N, item, excl_txt), trap=trap, fact=fact,
                met=good >= N, eval2=lambda t=None: tot - ex - N >= 0)


KINDS = {"num": k_num, "frac": k_frac, "dur": k_dur, "date": k_date, "doc": k_doc, "cnt": k_cnt}


def level_of(levels_met, cumulative):
    """levels_met[k] = all criteria of level k met (k>=1). Path 1: scan."""
    best = 0
    for k in range(1, len(levels_met)):
        if levels_met[k]:
            best = k
        elif cumulative:
            break
    return best


def level_of2(levels_met, cumulative):
    """Path 2: set logic."""
    sat = {k for k in range(1, len(levels_met)) if levels_met[k]}
    if cumulative:
        cands = [k for k in sat if all(j in sat for j in range(1, k + 1))]
    else:
        cands = list(sat)
    return max(cands + [0])


def gen_rubric(rng, bucket, qtype, want, dk=None):
    d = DOMAINS[dk or rng.choice(DOMAIN_KEYS)]
    ctx = dict(review=rand_date(rng), dstyle=rng.randint(0, 3), co=rng.choice(COMPANIES), rid=d["rid"])
    ctx["date"] = ctx["review"]
    subj = d["subject"]
    L = 3 if bucket == "short" else rng.choice([3, 4])
    while True:
        per = [1] * L if bucket == "short" else [rng.choice([1, 1, 2] if bucket == "medium" else [1, 2, 2]) for _ in range(L)]
        if sum(per) <= len(d["metrics"]):
            break
    cumulative = rng.random() < 0.75
    form = rng.choice(["atleast", "atleast", "exact"]) if qtype == "noul" else None
    if form == "atleast":
        G = rng.randint(1, L) if want == 1 else rng.randint(0, L - 1)
    else:
        G = rng.randint(0, L)
    # ---- met targets
    targets, wants = [None], [None]
    for lv in range(1, L + 1):
        t = [True] * per[lv - 1]
        w = [False] * per[lv - 1]
        if cumulative:
            if lv == G + 1 or (lv > G + 1 and rng.random() < 0.45):
                j = rng.randrange(per[lv - 1])
                t[j] = False
                w[j] = lv == G + 1 and rng.random() < 0.7
        else:
            if lv > G or (lv < G and rng.random() < 0.5):
                j = rng.randrange(per[lv - 1])
                t[j] = False
                w[j] = lv > G and rng.random() < 0.6
        targets.append(t)
        wants.append(w)
    if rng.random() < 0.35:
        cand = [(lv, j) for lv in range(1, L + 1) for j in range(per[lv - 1]) if targets[lv][j] and not wants[lv][j]]
        if cand:
            lv, j = rng.choice(cand)
            wants[lv][j] = True
    specs = shuffled(rng, d["metrics"])
    crits, si = [None], 0
    for lv in range(1, L + 1):
        row = []
        for j in range(per[lv - 1]):
            c = KINDS[specs[si][0]](rng, specs[si], targets[lv][j], wants[lv][j], ctx)
            si += 1
            assert c["met"] == targets[lv][j] and c["eval2"]() == targets[lv][j], "criterion engine mismatch"
            row.append(c)
        crits.append(row)
    # ---- superseded / not-yet-effective rubric version
    notes, sup = [], None
    if bucket != "short" and rng.random() < 0.35:
        cand = [c for row in crits[1:] for c in row if c["kind"] == "num" and not c["trap"]]
        if cand:
            c = rng.choice(cand)
            opts = [t for t in range(c["thr"] - 8, c["thr"] + 9)
                    if t != c["thr"] and t > 0 and (not c["cap100"] or t <= 100) and c["good"](c["v"], t) != c["met"]]
            if opts:
                other = rng.choice(opts)
                twist = rng.random() < 0.35
                n = rng.randint(3, 7)
                if twist:
                    E = ctx["review"] + datetime.timedelta(days=rng.randint(1, 60))
                    cur, prev = other, c["thr"]
                    c["rule"] = c["render"](cur)
                    c["trap"] = "applied the new rubric version before its effective date"
                    notes.append("Rubric v%d applies to reviews dated on or after %s; earlier reviews use v%d, which is identical "
                                 "except that its %s threshold is %s." % (n, fmt_date(E, ctx["dstyle"]), n - 1, c["label"], _ustr(prev, c["unit"])))
                else:
                    E = ctx["review"] - datetime.timedelta(days=rng.randint(0, 200))
                    cur, prev = c["thr"], other
                    c["trap"] = "used the superseded rubric version"
                    notes.append("Change log: rubric v%d (effective %s) replaced v%d. Only change: the %s threshold moved from %s to %s."
                                 % (n, fmt_date(E, ctx["dstyle"]), n - 1, c["label"], _ustr(prev, c["unit"]), _ustr(cur, c["unit"])))
                sup = (c, cur, prev, E)
    # ---- engine + independent check
    met1 = [True] + [all(c["met"] for c in row) for row in crits[1:]]

    def ev2(c):
        if sup and c is sup[0]:
            app = sup[1] if ctx["review"].toordinal() >= sup[3].toordinal() else sup[2]
            return c["eval2"](app)
        return c["eval2"]()
    met2 = [True] + [all(ev2(c) for c in row) for row in crits[1:]]
    g1, g2 = level_of(met1, cumulative), level_of2(met2, cumulative)
    assert g1 == G and g2 == G, "rubric engine mismatch %s %s %s" % (g1, g2, G)
    levels = d["levels"][:L + 1]
    optname = lambda k: "%d: %s" % (k, levels[k])
    mistakes = {}
    for row in crits[1:]:
        for c in row:
            if c["trap"]:
                c["met"] = not c["met"]
                k = level_of([True] + [all(x["met"] for x in r) for r in crits[1:]], cumulative)
                c["met"] = not c["met"]
                if k != G:
                    mistakes.setdefault(optname(k), c["trap"])
    k = level_of(met1, not cumulative)
    if k != G:
        mistakes.setdefault(optname(k), "ignored the cumulative requirement" if cumulative
                            else "applied a cumulative reading to a non-cumulative rubric")
    decoys = []
    if bucket != "short" and rng.random() < 0.3:
        prevk = rng.choice([x for x in range(L + 1) if x != G])
        decoys.append("Previous review (%d, older rubric): Level %d" % (ctx["review"].year - 1, prevk))
        mistakes.setdefault(optname(prevk), "copied last year's score (precedent)")
    if bucket != "short" and rng.random() < 0.4:
        pool = [x for x in range(L + 1) if x != G]
        xk = rng.choice([x for x in pool if optname(x) in mistakes] or pool)
        notes.append("Draft score entered by %s (%s, not an authorized reviewer): Level %d." % (person(rng), rng.choice(JUNIOR), xk))
        mistakes.setdefault(optname(xk), "followed the trainee's draft score")
    for x in range(L + 1):
        if x != G:
            mistakes.setdefault(optname(x), "counted an unmet criterion as met" if x > G else "missed a satisfied criterion")
    if bucket != "short":
        decoys += rng.sample(["Reviewer: %s" % person(rng), "File opened: %s" % fmt_date(ctx["review"] - datetime.timedelta(days=rng.randint(30, 400)), ctx["dstyle"]),
                              "Office: %s" % rng.choice(["Leeds", "Denver", "Pune", "Lyon", "Austin", "Toronto"]),
                              "Case reference: %s-%d" % (d["rid"], rng.randint(1000, 99999))], rng.randint(1, 3))
    # ---- render
    short = bucket == "short"
    if cumulative:
        rule = "Score = highest level fully met; levels are cumulative (each needs all lower levels too)." if short else rng.choice([
            "Score = the highest level whose criteria are fully supported by the facts. Each level also requires every criterion of all lower levels.",
            "A level cannot be awarded unless no criterion at that level or any lower level is unmet. Award the highest such level.",
            "Levels are cumulative: to earn Level k, every criterion for Levels 1 through k must be met. Level 0 applies when Level 1 is not met."])
    else:
        rule = "Score = highest level whose own criteria are all met; levels are independent (non-cumulative)." if short else rng.choice([
            "Levels are assessed independently: award the highest level whose own criteria are all met, even if some lower level's criteria are not met. Level 0 applies if no level is met.",
            "Each level stands on its own (non-cumulative). The score is the highest level whose listed criteria are all supported by the facts; unmet criteria at lower levels do not block a higher level."])
    lst = rng.randint(0, 3) if not short else 0
    crit_txt = lambda k: "; ".join(c["rule"] for c in crits[k])
    if lst == 0:
        lines = ["%d %s: %s" % (k, levels[k], crit_txt(k) if k else "default") if short else
                 "Level %d - %s: %s" % (k, levels[k], ("requires " + crit_txt(k)) if k else "default (no criteria)") for k in range(L + 1)]
        lev_txt = "\n".join(lines)
    elif lst == 1:
        recs = [("Level %d" % k, {"Label": levels[k], "Criteria (all required)": crit_txt(k) if k else "none (default)"}) for k in range(L + 1)]
        lev_txt = render_records(rng, recs, ["Label", "Criteria (all required)"], "table")
    elif lst == 2:
        lev_txt = json.dumps([{"level": k, "label": levels[k], "criteria": [c["rule"] for c in crits[k]] if k else []} for k in range(L + 1)], indent=1)
    else:
        lev_txt = " ".join(["Level 0 (%s) is the default." % levels[0]] +
                           ["Level %d (%s) requires %s." % (k, levels[k], " and ".join(c["rule"] for c in crits[k])) for k in range(1, L + 1)])
    facts = [c["fact"] for row in crits[1:] for c in row] + decoys
    rng.shuffle(facts)
    fst = rng.randint(0, 2) if not short else rng.choice([0, 1])
    rev = fmt_date(ctx["review"], ctx["dstyle"])
    if fst == 0:
        fact_txt = "Facts (review date %s):\n" % rev + "\n".join("- " + f for f in facts)
    elif fst == 1:
        fact_txt = "Review date %s. %s." % (rev, ". ".join(facts))
    else:
        fact_txt = "Reviewer worksheet (review date %s)\n" % rev + "\n".join("  * " + f for f in facts)
    title = d["rtitle"] if short else "%s %s - %s" % (ctx["co"], d["org"], d["rtitle"])
    core = [title + "\n" + rule, lev_txt] + notes + [fact_txt]
    if not short and rng.random() < 0.25:
        core = [title + "\n" + rule, fact_txt, lev_txt] + notes
    state = assemble(rng, core, bucket, d, ctx, fixed_head=1)
    options = [optname(k) for k in range(L + 1)]
    if qtype == "choice":
        q = rng.choice(["What score should %s receive under the rubric?" % subj,
                        "Assign the rubric level for %s: the highest level fully supported by the facts." % subj,
                        "Which level does %s earn?" % subj, "Using the %s, score %s." % (d["rtitle"], subj)])
        return dict(state=state, qtype="choice", instructions=q, options=shuffled(rng, options), gold=optname(G),
                    meta=dict(family=FAMILY, difficulty=_difficulty(bucket, mistakes, 1 if sup else 0),
                              mistakes={k: v for k, v in mistakes.items() if k != optname(G)}))
    if form == "atleast":
        kq = rng.randint(1, G) if want == 1 else rng.randint(G + 1, L)
        q = rng.choice(["Does %s qualify for Level %d (%s) or higher?" % (subj, kq, levels[kq]),
                        "Is %s rated at least '%s' (Level %d)?" % (subj, levels[kq], kq)])
        gold = int(G >= kq)
    else:
        if want == 1:
            kq = G
        else:
            tricky = [k for k in range(L + 1) if k != G and any(t in mistakes.get(optname(k), "") for t in TRICKY)]
            kq = rng.choice(tricky or [k for k in range(L + 1) if k != G])
        q = "Is Level %d (%s) the correct score for %s?" % (kq, levels[kq], subj)
        gold = int(kq == G)
    m = {} if gold == 1 else {optname(kq): mistakes.get(optname(kq), "wrong level")}
    return dict(state=state, qtype="noul", instructions=q, options=None, gold=gold,
                meta=dict(family=FAMILY, difficulty=_difficulty(bucket, mistakes, 1 if sup else 0), mistakes=m))


# ============================================================================================
# (c) TRADEOFF: explicit weighted scoring with knock-outs, bands and tie-breaks
# ============================================================================================
def _weights(rng, C):
    units = [2] * C
    for _ in range(20 - 2 * C):
        units[rng.randrange(C)] += 1
    return [u * 5 for u in units]


def _raw_str(v, unit):
    if unit == "$":
        return "$" + commas(v)
    return "%s %s" % (commas(v), unit)


def _bands(lo, hi):
    span = (hi - lo) // 5
    nice = 10 ** (len(str(max(span, 1))) - 1)
    while True:
        ts = [lo + int(round((hi - lo) * k / 5.0 / nice)) * nice for k in range(1, 5)]
        if len(set(ts)) == 4 and ts == sorted(ts) and ts[0] > lo:
            return ts, max(1, nice // 10)
        nice = max(1, nice // 10)


def band_score1(raw, ts, sc):
    if raw < ts[0]:
        return sc[0]
    elif raw < ts[1]:
        return sc[1]
    elif raw < ts[2]:
        return sc[2]
    elif raw < ts[3]:
        return sc[3]
    return sc[4]


def band_score2(raw, ts, sc):
    return sc[sum(1 for t in ts if Fraction(raw) >= t)]


def _winner(names, totals, elig, tbkey):
    cands = [a for a in names if elig[a]]
    if not cands:
        return None
    return sorted(cands, key=lambda a: (-totals[a], tbkey(a), a))[0]


def gen_tradeoff(rng, bucket, qtype, want, dk=None):
    d = DOMAINS[dk or rng.choice(DOMAIN_KEYS)]
    ctx = dict(co=rng.choice(COMPANIES), rid=d["rid"], date=rand_date(rng), dstyle=rng.randint(0, 3))
    short = bucket == "short"
    A = rng.choice([2, 3, 3]) if short else rng.choice([3, 3, 4, 4])
    C = 3 if short else rng.choice([3, 4, 4, 5])
    scale = rng.choice([5, 10])
    use_band = rng.random() < (0.25 if short else 0.55)
    crit_names = rng.sample(d["crits"], C - (1 if use_band else 0))
    band_name, band_unit, blo, bhi = d["band"]
    crits = crit_names + ([band_name] if use_band else [])
    wstyle = rng.choice(["pct", "pct", "dec", "pts"])
    weights = _weights(rng, C) if wstyle != "pts" else [rng.randint(1, 5) for _ in range(C)]
    W = dict(zip(crits, weights))
    ts, rstep = _bands(blo, bhi) if use_band else (None, None)
    bsc = [5, 4, 3, 2, 1] if scale == 5 else [10, 8, 6, 4, 2]
    knock = (not short) and rng.random() < 0.4
    kc = rng.choice(crit_names) if knock else None
    kfloor = rng.choice([2, 3] if scale == 5 else [4, 5]) if knock else None
    exempt = knock and rng.random() < 0.35
    sup = (not short) and rng.random() < 0.3
    tbtype = rng.choice(["crit", "crit", "alpha"] + (["band"] if use_band else []))
    tbc = rng.choice(crit_names) if tbtype == "crit" else None
    want_tie = rng.random() < 0.3
    names = sorted(rng.sample(d["alts"], A))
    best = None
    for attempt in range(250):
        S = {a: {c: rng.randint(1, scale) for c in crit_names} for a in names}
        raw = {}
        if use_band:
            for a in names:
                if rng.random() < 0.35:
                    raw[a] = rng.choice(ts)
                else:
                    raw[a] = rng.randrange(blo, bhi + 1, rstep)
                S[a][band_name] = band_score1(raw[a], ts, bsc)
        plan = {a: (rng.choice(["signed", "none", "draft only"]) if exempt else "none") for a in names}
        oldW = None
        if sup:
            oldW = dict(zip(crits, _weights(rng, C) if wstyle != "pts" else [rng.randint(1, 5) for _ in range(C)]))

        def tot(Sx, Wx):
            return {a: sum(Wx[c] * Sx[a][c] for c in crits) for a in names}

        def elig_fn(Sx, honor_knock=True, honor_exempt=True):
            return {a: (not knock or not honor_knock or Sx[a][kc] >= kfloor or (honor_exempt and plan[a] == "signed")) for a in names}

        def tbkey(a, Sx=S):
            if tbtype == "crit":
                return -Sx[a][tbc]
            if tbtype == "band":
                return raw[a]
            return 0
        T = tot(S, W)
        E = elig_fn(S)
        if want_tie:
            el = sorted([a for a in names if E[a]], key=lambda a: -T[a])
            if len(el) >= 2:
                a0, b0 = el[0], el[1]
                for c in shuffled(rng, crit_names):
                    diff = T[a0] - T[b0]
                    if diff % W[c] == 0 and 1 <= S[b0][c] + diff // W[c] <= scale and not (knock and c == kc):
                        S[b0][c] += diff // W[c]
                        break
                T = tot(S, W)
                E = elig_fn(S)
        win = _winner(names, T, E, tbkey)
        if win is None:
            continue
        mist = {}
        top = [a for a in names if E[a] and T[a] == T[win]]
        if len(top) > 1:
            for a in top:
                if a != win:
                    mist.setdefault(a, "applied the tie-break rule backwards")
        m = _winner(names, {a: sum(S[a][c] for c in crits) for a in names}, E, tbkey)
        if m != win:
            mist.setdefault(m, "ignored the weights (unweighted sum)")
        if knock:
            m = _winner(names, T, elig_fn(S, honor_knock=False), tbkey)
            if m != win:
                mist.setdefault(m, "ignored the knock-out floor")
            if exempt:
                m = _winner(names, T, elig_fn(S, honor_exempt=False), tbkey)
                if m != win:
                    mist.setdefault(m, "forgot the remediation-plan exemption")
                if any(plan[a] == "draft only" for a in names):
                    pl2 = dict(plan)
                    E2 = {a: (S[a][kc] >= kfloor or plan[a] in ("signed", "draft only")) for a in names}
                    m = _winner(names, T, E2, tbkey)
                    if m != win:
                        mist.setdefault(m, "counted a draft plan for the exemption")
        if sup:
            m = _winner(names, tot(S, oldW), E, tbkey)
            if m != win:
                mist.setdefault(m, "used the superseded weights")
        if use_band:
            for a in names:
                if raw[a] in ts:
                    S2 = {x: dict(S[x]) for x in names}
                    i = ts.index(raw[a])
                    S2[a][band_name] = bsc[i]
                    m = _winner(names, tot(S2, W), elig_fn(S2), tbkey)
                    if m != win:
                        mist.setdefault(m, "band boundary off-by-one")
        cand = (S, raw, plan, oldW, T, E, win, mist)
        vals = set(mist.values())
        desired = {f for f, on in [("tie", want_tie), ("knock", knock), ("exempt", exempt), ("sup", sup),
                                   ("band", use_band and not short)] if on}
        got = set()
        if len(top) > 1:
            got.add("tie")
        if "ignored the knock-out floor" in vals:
            got.add("knock")
        if vals & {"forgot the remediation-plan exemption", "counted a draft plan for the exemption"}:
            got.add("exempt")
        if "used the superseded weights" in vals:
            got.add("sup")
        if "band boundary off-by-one" in vals:
            got.add("band")
        score = len(got & desired) + (0.5 if "ignored the weights (unweighted sum)" in vals else 0) + (0.25 if vals else 0)
        if best is None or score > best[0]:
            best = (score, cand)
        if desired <= got and (vals or short):
            break
    S, raw, plan, oldW, T, E, win, mist = best[1]

    # ---- independent check (Fractions, normalized weights, alternative band lookup, pairwise scan)
    wsum = sum(W.values())
    NW = {c: Fraction(W[c], wsum) for c in crits}
    tot2, el2 = {}, {}
    for a in names:
        s_row = {c: S[a][c] for c in crit_names}
        if use_band:
            s_row[band_name] = band_score2(raw[a], ts, bsc)
        tot2[a] = sum(NW[c] * s_row[c] for c in crits)
        el2[a] = (kc is None) or s_row[kc] - kfloor >= 0 or (exempt and plan[a].startswith("signed"))
    w2 = None
    for a in names:
        if not el2[a]:
            continue
        if w2 is None:
            w2 = a
            continue
        if tot2[a] > tot2[w2]:
            w2 = a
        elif tot2[a] == tot2[w2]:
            if tbtype == "crit":
                ka, kb = S[a][tbc], S[w2][tbc]
                if ka > kb or (ka == kb and a < w2):
                    w2 = a
            elif tbtype == "band":
                if raw[a] < raw[w2] or (raw[a] == raw[w2] and a < w2):
                    w2 = a
            elif a < w2:
                w2 = a
    assert w2 == win, "tradeoff independent check failed"
    return _render_tradeoff(rng, d, ctx, bucket, qtype, want, names, crits, crit_names, W, wstyle, scale, use_band,
                            band_name, band_unit, ts, bsc, raw, knock, kc, kfloor, exempt, plan, sup, oldW, tbtype, tbc,
                            S, T, E, win, mist)


AWARDS = ["Vendor of the Year", "Best in Class", "Customer Choice Award", "Top Innovator", "Fastest Growing Partner"]


def _render_tradeoff(rng, d, ctx, bucket, qtype, want, names, crits, crit_names, W, wstyle, scale, use_band,
                     band_name, band_unit, ts, bsc, raw, knock, kc, kfloor, exempt, plan, sup, oldW, tbtype, tbc,
                     S, T, E, win, mist):
    short = bucket == "short"

    def wtxt(Wx):
        if wstyle == "pct":
            return ", ".join("%s %d%%" % (c, Wx[c]) for c in crits)
        if wstyle == "dec":
            return ", ".join("%s %s" % (c, "%.2f" % (Wx[c] / 100.0)) for c in crits)
        return ", ".join("%s x%d" % (c, Wx[c]) for c in crits)
    rules = []
    rules.append("Weighted score = sum of (weight x score) over all criteria; choose the eligible option with the highest weighted score."
                 if short else rng.choice([
                     "Weighted score = sum of (criterion weight x criterion score). The eligible option with the highest weighted score is selected.",
                     "Multiply each criterion score by its weight and add them up; pick the eligible option with the largest total.",
                     "Selection rule: compute each option's weighted total (weight x score, summed over all criteria) and choose the highest."]))
    rules.append("Scores run 1-%d, higher is better." % scale)
    lead = {"pct": "Weights: ", "dec": "Weights (sum to 1.00): ", "pts": "Importance multipliers (not percentages): "}[wstyle]
    rules.append(lead + wtxt(W) + ".")
    if use_band:
        f = lambda v: _raw_str(v, band_unit)
        rules.append("%s is not panel-scored; convert the raw figure: under %s -> %d; %s to under %s -> %d; %s to under %s -> %d; "
                     "%s to under %s -> %d; %s or more -> %d." % (band_name[0].upper() + band_name[1:], f(ts[0]), bsc[0], f(ts[0]), f(ts[1]), bsc[1],
                                                               f(ts[1]), f(ts[2]), bsc[2], f(ts[2]), f(ts[3]), bsc[3], f(ts[3]), bsc[4]))
    if knock:
        rules.append(rng.choice(["Knock-out: any option scoring below %d on %s is excluded regardless of its total." % (kfloor, kc),
                                 "No option that does not reach at least %d on %s may be selected, whatever its total." % (kfloor, kc)]))
        if exempt:
            rules.append("Exception: an option with a signed remediation plan on file is exempt from that floor; a draft plan does not qualify.")
    if tbtype == "crit":
        rules.append("If weighted totals tie, the option with the higher %s score wins; if still tied, the alphabetically first name." % tbc)
    elif tbtype == "band":
        rules.append("If weighted totals tie, the option with the lower %s wins; if still tied, the alphabetically first name." % band_name)
    else:
        rules.append("Ties on weighted total are broken alphabetically (earliest name wins).")
    cols = list(crit_names) + ([band_name] if use_band else []) + (["Remediation plan"] if exempt else [])
    recs = []
    for a in names:
        v = {c: str(S[a][c]) for c in crit_names}
        if use_band:
            v[band_name] = _raw_str(raw[a], band_unit)
        if exempt:
            v["Remediation plan"] = plan[a]
        recs.append((a, v))
    rng.shuffle(recs)
    prose = {c: (lambda c: lambda v: "scored %s on %s" % (v, c))(c) for c in crit_names}
    prose[band_name] = lambda v: "has a %s of %s" % (band_name, v)
    prose["Remediation plan"] = lambda v: "has remediation plan status '%s'" % v
    cstyle = rng.choice(["ctable", "bullets"] if short else REC_STYLES)
    mat = ("Panel scores:" if rng.random() < 0.5 else "Evaluation results:") + "\n" + render_records(rng, recs, cols, cstyle, prose)
    notes = []
    if sup:
        notes.append(rng.choice(["Archived weighting memo (%d, superseded by the current weights; do not use): %s." % (ctx["date"].year - 1, wtxt(oldW)),
                                 "For reference, the previous cycle used %s. Those weights were retired on %s." % (wtxt(oldW), fmt_date(ctx["date"] - datetime.timedelta(days=rng.randint(20, 200)), ctx["dstyle"]))]))
    others = [a for a in names if a != win]
    if not short and rng.random() < 0.4:
        x = rng.choice([a for a in others if a in mist] or others)
        notes.append("%s (%s) commented: \"%s is obviously the best pick, let's not overthink it.\"" % (person(rng), rng.choice(JUNIOR), x))
        mist.setdefault(x, "followed an unauthorized suggestion")
    if not short and rng.random() < 0.3:
        x = rng.choice(others)
        notes.append("Marketing note: %s was named '%s' by an industry magazine this year." % (x, rng.choice(AWARDS)))
        mist.setdefault(x, "swayed by an irrelevant award (surface cue)")
    for a in others:
        mist.setdefault(a, "picked a lower weighted total" if E[a] else "picked an excluded option")
    rstyle = rng.randint(0, 3) if not short else 2
    title = ("Decision: %s." % d["decision"]) if short else "%s %s - decision memo: %s" % (ctx["co"], d["org"], d["decision"])
    rules_txt = ("Scoring rules:\n" if not short else "") + render_rules(rng, rules, rstyle)
    core = [title, rules_txt, mat] + notes if rng.random() < 0.7 or short else [title, mat, rules_txt] + notes
    state = assemble(rng, core, bucket, d, ctx, fixed_head=1)
    if qtype == "choice":
        q = rng.choice(["Which option should be selected under the scoring rules?",
                        "Apply the weighted scoring to %s. Which option wins?" % d["decision"].replace("choose", "the choice of").replace("select", "the selection of"),
                        "Based on the memo, which alternative is chosen?",
                        "Which option has the best weighted result after applying every rule?"])
        return dict(state=state, qtype="choice", instructions=q, options=shuffled(rng, names), gold=win,
                    meta=dict(family=FAMILY, difficulty=_difficulty(bucket, mist), mistakes={a: mist[a] for a in others}))
    if want == 1:
        X = win
    else:
        tr = [a for a in others if any(k in mist[a] for k in TRICKY)]
        X = rng.choice(tr) if tr and rng.random() < 0.75 else rng.choice(others)
    q = rng.choice(["Under the stated scoring rules, should %s be selected?" % X,
                    "Is %s the option the rules select?" % X,
                    "Yes or no: %s wins the weighted evaluation." % X])
    return dict(state=state, qtype="noul", instructions=q, options=None, gold=int(X == win),
                meta=dict(family=FAMILY, difficulty=_difficulty(bucket, mist), mistakes={} if X == win else {X: mist[X]}))


# ============================================================================================
# public API
# ============================================================================================
GENS = {"route": gen_route, "rubric": gen_rubric, "tradeoff": gen_tradeoff}
SUB_WEIGHTS = [("route", 0.4), ("rubric", 0.3), ("tradeoff", 0.3)]
ROW_KEYS = ["state", "qtype", "instructions", "options", "gold", "card", "meta"]


def _generate(n, seed):
    rng = random.Random(seed)
    rows, info = [], []
    parity = rng.randint(0, 1)
    for i in range(n):
        sub = rng.choices([k for k, _ in SUB_WEIGHTS], weights=[w for _, w in SUB_WEIGHTS])[0]
        bucket = pick_bucket(rng)
        qtype = "choice" if rng.random() < 0.7 else "noul"
        want = None
        if qtype == "noul":
            want = parity
            parity ^= 1
        dk = rng.choice(DOMAIN_KEYS)
        irng = random.Random(rng.randrange(2 ** 62))
        row, fallback = None, None
        lo, hi = BUCKET_RANGE[bucket]
        for _ in range(40):
            r = GENS[sub](irng, bucket, qtype, want, dk)
            if in_bucket(r["state"], bucket):
                row = r
                break
            dist = max(lo - len(r["state"]), len(r["state"]) - hi)
            if fallback is None or dist < fallback[0]:
                fallback = (dist, r)
        row = row or fallback[1]
        row["card"] = None
        rows.append({k: row[k] for k in ROW_KEYS})
        info.append((sub, dk, bucket))
    return rows, info


def generate(n, seed):
    return _generate(n, seed)[0]


# ============================================================================================
# self-test
# ============================================================================================
def _validate(row):
    assert list(row) == ROW_KEYS, list(row)
    assert isinstance(row["state"], str) and row["state"].strip()
    assert isinstance(row["instructions"], str) and row["instructions"].strip()
    assert row["qtype"] in ("choice", "noul")
    m = row["meta"]
    assert m["family"] == FAMILY and m["difficulty"] in ("medium", "hard")
    assert set(m) <= {"family", "difficulty", "gold_probs", "mistakes"}
    if row["qtype"] == "choice":
        o = row["options"]
        assert isinstance(o, list) and 2 <= len(o) <= 8 and len(set(o)) == len(o), o
        assert all(isinstance(x, str) and x for x in o)
        assert row["gold"] in o
        for k in m.get("mistakes", {}):
            assert k in o and k != row["gold"], k
    else:
        assert row["options"] is None and row["gold"] in (0, 1) and type(row["gold"]) is int
    if m.get("gold_probs") is not None:
        gp = m["gold_probs"]
        assert abs(sum(gp.values()) - 1.0) < 1e-9
    if row["card"] is not None:
        assert all(l.startswith("- ") for l in row["card"].splitlines())


def _selftest():
    from collections import Counter
    rows, info = _generate(300, 12345)
    for r in rows:
        _validate(r)          # schema; the rule engines + independent checks assert inside every generator
    rows2 = generate(300, 12345)
    assert json.dumps(rows, sort_keys=True) == json.dumps(rows2, sort_keys=True), "not deterministic"
    assert json.dumps(generate(50, 999)) != json.dumps(generate(50, 12345)), "seed ignored"
    # independent re-derivation of gold position uniformity / noul balance
    lens = [len(r["state"]) for r in rows]
    b = Counter("short" if L < 600 else ("medium" if L <= 2500 else "long") for L in lens)
    noul = [r for r in rows if r["qtype"] == "noul"]
    ch = [r for r in rows if r["qtype"] == "choice"]
    pos = Counter(round(r["options"].index(r["gold"]) / (len(r["options"]) - 1), 1) for r in ch)
    yes = sum(r["gold"] for r in noul) / max(1, len(noul))
    assert 0.4 <= yes <= 0.6, yes
    assert len(set(dk for _, dk, _ in info)) >= 8
    print("self-test OK: 300 rows")
    print("  subfamilies:", dict(Counter(s for s, _, _ in info)))
    print("  domains:", len(set(dk for _, dk, _ in info)), dict(Counter(dk for _, dk, _ in info)))
    print("  length buckets (actual):", dict(b), " target:", dict(Counter(bk for _, _, bk in info)))
    print("  min/median/max len:", min(lens), sorted(lens)[len(lens) // 2], max(lens))
    print("  qtype:", dict(Counter(r["qtype"] for r in rows)), " noul yes-rate: %.3f" % yes)
    print("  difficulty:", dict(Counter(r["meta"]["difficulty"] for r in rows)))
    print("  gold relative position (choice):", dict(sorted(pos.items())))
    print("  options per choice q:", dict(Counter(len(r["options"]) for r in ch)))
    print("  distinct instruction strings:", len(set(r["instructions"] for r in rows)))
    mk = Counter(v for r in rows for v in r["meta"].get("mistakes", {}).values())
    print("  distinct mistake labels:", len(mk))


if __name__ == "__main__":
    ex_rows = generate(40, 7)
    shown = 0
    for r in ex_rows:
        if shown == 3:
            break
        if shown == 1 and r["qtype"] != "noul":
            continue
        shown += 1
        print("=" * 100)
        print(r["state"])
        print("-" * 40)
        print("Q:", r["instructions"])
        print("options:", r["options"])
        print("gold:", r["gold"])
        print("meta:", json.dumps(r["meta"], indent=1))
    print("=" * 100)
    _selftest()
