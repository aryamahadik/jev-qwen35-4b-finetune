#!/usr/bin/env python3
"""Procedural generator for the "multihop" family of System-One decision problems.

Each item is a small world of linked records (e.g. claim -> order -> shipment ->
carrier code -> carrier guarantee revision) that must be chained 2-4 hops to find
the operative rule, which is then applied to the entity's facts.

Gold answers are computed by a generic resolver (`_solve`) that walks the record
tables exactly as a reader would (ID lookup, rename/merger notices, revision in
force on the governing date, unit conversion, exception / exception-to-exception,
tiered thresholds).  A second, independent path (`_direct`) evaluates the answer
from the builder's own ground truth (the objects it deliberately created) with a
separately written evaluator; both must agree.

Wrong options are produced by re-running the resolver with one specific mistake
switched on (look-alike ID, superseded revision, not-yet-effective revision,
draft, ignored rename, inclusive/exclusive boundary, unit mix-up, missed
exception, missed exception-to-the-exception), so every distractor is a
plausible, named error.  Unauthorized notes and requester surface cues point at
one of those wrong answers.

Pure standard library; deterministic given the seed.
"""

import calendar
import datetime as _dt
import json
import operator
import random
import string
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F

FAMILY = "multihop"

# --------------------------------------------------------------------------
# small vocabularies
# --------------------------------------------------------------------------
FIRST = ["Aisha", "Ben", "Carla", "Dmitri", "Elena", "Farid", "Grace", "Hiro", "Ines", "Jonas",
         "Kemi", "Luca", "Maya", "Nikhil", "Olga", "Pedro", "Quinn", "Rosa", "Sanjay", "Tara",
         "Umar", "Vera", "Wes", "Xin", "Yusuf", "Zoe", "Priya", "Mateo", "Lena", "Owen", "Noor",
         "Ravi", "Sofia", "Tomas", "Hana", "Kofi", "Ana", "Marek", "Leila", "Chen", "Bea", "Idris",
         "Freya", "Gustavo", "Mira", "Ansel", "Dalia", "Emeka"]
LAST = ["Abara", "Brandt", "Castillo", "Dubois", "Eriksen", "Fischer", "Garcia", "Haddad",
        "Ivanova", "Jensen", "Kowalski", "Lindqvist", "Moreau", "Nakamura", "Okafor", "Petrov",
        "Quintero", "Rossi", "Sato", "Tanaka", "Ueda", "Varga", "Walsh", "Xu", "Yilmaz", "Zimmer",
        "Mensah", "Novak", "Patel", "Reyes", "Silva", "Toure", "Weber", "Kim", "Osei", "Lund",
        "Duarte", "Farah", "Hale", "Ortiz", "Brennan", "Achterberg", "Nwosu", "Carvalho"]
CITIES = ["Rotterdam", "Leeds", "Lyon", "Denver", "Porto", "Tulsa", "Graz", "Malmo", "Quebec City",
          "Bologna", "Tacoma", "Aarhus", "Valencia", "Cork", "Omaha", "Gdansk", "Nagoya", "Durban",
          "Boise", "Tampere", "Brno", "Halifax", "Reno", "Split"]
COMPANIES = ["Arcwell Labs", "Brightmoor Retail", "Cindervale Logistics", "Dunlin Health",
             "Everline Media", "Foxglove Software", "Granite Peak Bank", "Hollis & Rowe",
             "Ironbark Systems", "Juniper Freight", "Kestrel Analytics", "Larchmont Foods"]
JUNIOR = ["trainee, intake desk", "temp, not an approver", "intern", "junior analyst, no decision authority",
          "sales rep, not authorised to decide cases", "summer associate", "new starter, still shadowing",
          "contractor, data entry only"]
SHORT_Q = {"delivery delay": "delay", "debt-to-income ratio": "DTI", "outage duration": "outage",
           "nightly lodging rate": "nightly rate", "household income": "income", "patient age": "age",
           "entry score": "score", "time elapsed since receipt": "time since receipt"}
SHORT_LABEL = {"Patient age at referral": "Age", "Referral received": "Received", "Measured defect rate": "Defect rate",
               "Nightly rate claimed": "Nightly rate", "Debt-to-income (DTI)": "DTI", "Duration requested": "Duration",
               "Reported income": "Income", "Outage duration": "Outage", "Promised delivery": "Promised",
               "Return received": "Returned", "Status as of": "As of", "Delay logged": "Delay",
               "Coverage start": "Cover start", "Date of service": "Service date", "Application date": "Applied",
               "Entry score": "Score", "Billed amount": "Billed", "Monthly fee": "Fee"}
SHORT_PHRASE = {"date the referral was received": "received date", "date the request was received": "received date",
                "application submission date": "submission date"}
UNIT_NOTE_SHORT = {"hr_leave": "1 leave day = 8 h.", "manufacturing_qa": "1% = 10,000 ppm.",
                   "healthcare_scheduling": "Ages are exact; 1 year = 12 months.", "education_admissions": "Score = GPA x 25.",
                   "travel_expenses": "1 EUR = {rate} USD.", "public_benefits": "Annual = 12 x monthly."}
HEADER_STYLES = ["=== {} ===", "## {}", "[{}]", "{}\n" + "-" * 24, "--- {} ---", "{}:"]

# --------------------------------------------------------------------------
# units
# --------------------------------------------------------------------------
UNIT_GROUPS = {
    "time": {"minutes": F(1), "hours": F(60), "days": F(1440), "weeks": F(10080)},
    "work": {"whours": F(1), "wdays": F(8)},
    "ratio": {"percent": F(1), "fraction": F(100)},
    "defect": {"ppm": F(1), "percent": F(10000)},
    "age": {"months": F(1), "years": F(12)},
    "score": {"score": F(1), "gpa": F(25)},
    "money": {"usd": F(1), "eur": None},  # EUR rate set per instance
    "income": {"usd_yr": F(1), "usd_mo": F(12)},
}
UNIT_TPL = {
    "minutes": [("{} minutes", "{} minute"), ("{} min", "{} min")],
    "hours": [("{} hours", "{} hour"), ("{} h", "{} h")],
    "days": [("{} days", "{} day"), ("{} calendar days", "{} calendar day")],
    "weeks": [("{} weeks", "{} week")],
    "wdays": [("{} working days", "{} working day"), ("{} leave days", "{} leave day")],
    "whours": [("{} hours", "{} hour"), ("{} h", "{} h")],
    "percent": [("{}%", "{}%")],
    "fraction": [("{}", "{}")],
    "ppm": [("{} ppm", "{} ppm")],
    "months": [("{} months", "{} month")],
    "years": [("{} years", "{} year")],
    "score": [("{}%", "{}%"), ("{} points", "{} point")],
    "gpa": [("GPA {}", "GPA {}"), ("{} (GPA, 4.0 scale)", "{} (GPA, 4.0 scale)")],
    "usd": [("${}", "${}"), ("USD {}", "USD {}")],
    "eur": [("€{}", "€{}"), ("EUR {}", "EUR {}")],
    "usd_mo": [("${} per month", "${} per month"), ("${}/month", "${}/month")],
    "usd_yr": [("${} per year", "${} per year"), ("${}/year", "${}/year")],
}
MONEY_UNITS = ("usd", "eur", "usd_mo", "usd_yr")


def _dec(v):
    v = F(v)
    return Decimal(v.numerator) / Decimal(v.denominator)


def _ns(v, unit=None):
    """Number to display string (only ever called on clean numbers)."""
    v = F(v)
    if unit in ("gpa", "fraction"):
        return f"{_dec(v).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}"
    if v.denominator == 1:
        n = int(v)
        return f"{n:,}" if abs(n) >= 1000 else str(n)
    if unit in MONEY_UNITS:
        return f"{_dec(v).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):,}"
    s = f"{_dec(v).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)}"
    return s.rstrip("0").rstrip(".")


def _money(v):
    q = _dec(v).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"${q:,}"


def _clean(v, unit, dates=False):
    v = F(v)
    if v < 0:
        return False
    if dates:
        return v.denominator == 1
    return (v * 100).denominator == 1


# --------------------------------------------------------------------------
# domains
# --------------------------------------------------------------------------
def _exc(flag, flabel, fvals, cond, out, unless, ulabel, uvals, ucond):
    return dict(flag=flag, flabel=flabel, fvals=fvals, cond=cond, out=out,
                unless=unless, ulabel=ulabel, uvals=uvals, ucond=ucond)


DOMAINS = [
    dict(
        name="logistics", orgs=["Northwind Freight Desk", "Cobalt Parcel Claims", "Ridgeway Distribution"],
        levels=[dict(label="Claim", plural="Claims", pre="CLM-", dig=5,
                     deco=[("Filed by", "name"), ("Channel", "pick:web form|phone|email|EDI")]),
                dict(label="Order", plural="Orders", pre="ORD-", dig=5,
                     deco=[("Customer", "company"), ("Order value", "money:200:9000")]),
                dict(label="Shipment", plural="Shipments", pre="SHP-", dig=4,
                     deco=[("Origin", "city"), ("Destination", "city"), ("Weight", "kg")])],
        link=["Order", "Shipment", "Carrier"], keyname="carrier",
        keys=["NRT", "BLX", "QPX", "HLM", "ZVK", "TRN", "KSW", "DFL"],
        titles=["Carrier Service Guarantee", "Late-Delivery Compensation Schedule", "Carrier SLA Addendum"],
        gov=dict(home=2, label="Shipped", phrase="ship date"),
        attr=dict(kinds=["dates", "number"], name="delivery delay", group="time",
                  rule_units=["hours", "days"], rec_units=["hours", "days"], home=2, label="Delay logged",
                  dates=dict(a=(2, "Promised delivery"), b=(2, "Delivered"), gov_is=None, off=(2, 6))),
        grid={"hours": [12, 24, 36, 48, 72, 96, 120], "days": [1, 2, 3, 4, 5, 7, 10]},
        rng_rec={"hours": (2, 170, 1), "days": (0, 12, 1)},
        style="above", outs=["Full freight refund", "50% freight credit", "25% freight credit"],
        default="No compensation",
        excs=[_exc("x_weather", "Weather embargo hold", ("Yes", "No"),
                   "the shipment was held under a declared weather embargo", "No compensation",
                   "x_latenotice", "Delay notice sent more than 24 h after hold", ("Yes", "No"),
                   "the carrier sent its delay notice more than 24 hours after the hold began"),
              _exc("x_hazmat", "Declared hazardous goods", ("Yes", "No"),
                   "the consignment contained declared hazardous goods", "Refer to the claims desk",
                   "x_hazclear", "Hazmat inspection cleared without findings", ("Yes", "No"),
                   "the hazmat inspection was cleared without findings")],
        flag_home=2, modes=["label"],
        what=["compensation outcome", "late-delivery compensation", "operative compensation"],
        who="the customer",
        filler=["Carriers must upload proof of delivery within two business days of delivery. Missing proof of delivery is chased by the carrier desk and does not by itself change compensation.",
                "Pallet labels must show the consignment number and the handling code. Mislabelled pallets are re-labelled at the hub at the carrier's cost.",
                "Fuel surcharges are invoiced monthly and reconciled by Finance; they are outside the scope of delay compensation."],
    ),
    dict(
        name="insurance", orgs=["Harbor Mutual Claims", "Keystone Health Plan", "Bluewater Assurance"],
        levels=[dict(label="Claim", plural="Claims", pre="CL-", dig=6,
                     deco=[("Provider", "pick:Riverside Clinic|Maple Imaging|North Ortho Group|Lakeside Dental|City Physio")]),
                dict(label="Member", plural="Members", pre="MBR-", dig=5,
                     deco=[("Name", "name"), ("Member since", "pick:2016|2019|2021|2023|2024")]),
                dict(label="Policy", plural="Policies", pre="POL-", dig=5,
                     deco=[("Group", "pick:GRP-100|GRP-220|GRP-315|individual"), ("Premium status", "pick:paid to date|paid to date|current")])],
        link=["Member", "Policy", "Plan code"], keyname="plan",
        keys=["SLV-2", "GLD-1", "BRZ-3", "PLT-A", "SLV-P", "CORE-5"],
        titles=["Schedule of Benefits", "Benefit Schedule", "Coverage Summary"],
        gov=dict(home=0, label="Date of service", phrase="date of service"),
        attr=dict(kinds=["dates"], name="time since coverage start", group="time",
                  rule_units=["days", "weeks"], rec_units=["days"], home=0, label="",
                  dates=dict(a=(2, "Coverage start"), b=None, gov_is="b", off=(0, 0))),
        grid={"days": [30, 60, 90, 120, 180, 270, 365], "weeks": [4, 8, 13, 26, 39, 52]},
        rng_rec={"days": (3, 420, 1)},
        style="above", outs=["Covered at 90%", "Covered at 80%", "Covered at 50%"],
        default="Not covered (waiting period)",
        pct={"Covered at 90%": 90, "Covered at 80%": 80, "Covered at 50%": 50,
             "Not covered (waiting period)": 0, "Not covered (pre-existing condition)": 0,
             "Covered at 100% (accident benefit)": 100},
        excs=[_exc("x_preex", "Pre-existing condition flag", ("Yes", "No"),
                   "the treated condition is flagged as pre-existing", "Not covered (pre-existing condition)",
                   "x_prior", "12+ months continuous prior coverage", ("Yes", "No"),
                   "the member had at least 12 months of continuous prior coverage"),
              _exc("x_accident", "Accident-related", ("Yes", "No"),
                   "the claim arises from an accident", "Covered at 100% (accident benefit)",
                   "x_latefile", "Filed more than 90 days after service", ("Yes", "No"),
                   "the claim was filed more than 90 days after the date of service")],
        flag_home=0, modes=["label", "amount"], base=dict(home=0, label="Billed amount", lo=120, hi=9000),
        what=["coverage decision", "benefit determination"],
        what_amt=["plan payment", "payable amount"], who="the member",
        filler=["Claims submitted on paper are scanned within five business days; the scan date is not the date of service.",
                "Explanation-of-benefits letters are generated nightly and mailed to the member's address on file.",
                "Coordination of benefits with other insurers is handled by the COB unit and does not alter the plan's own schedule."],
    ),
    dict(
        name="hr_leave", orgs=["People Operations", "HR Shared Services", "Workforce Administration"],
        levels=[dict(label="Leave request", plural="Leave requests", pre="LR-", dig=4,
                     deco=[("Entered by", "name")]),
                dict(label="Employee", plural="Employees", pre="EMP-", dig=5,
                     deco=[("Name", "name"), ("Title", "pick:Analyst|Technician|Coordinator|Engineer|Specialist")]),
                dict(label="Department", plural="Departments", pre="DPT-", dig=3,
                     deco=[("Name", "pick:Logistics Planning|Field Service|Finance Ops|Platform Engineering|Customer Care|Procurement")])],
        link=["Employee", "Department", "Approval matrix"], keyname="matrix",
        keys=["MX-OPS", "MX-CORP", "MX-FLD", "MX-RND", "MX-SVC"],
        titles=["Leave Approval Matrix", "Delegation of Authority: Leave", "Absence Approval Standard"],
        gov=dict(home=0, label="Submitted", phrase="submission date"),
        attr=dict(kinds=["number"], name="leave length", group="work", rule_units=["wdays"],
                  rec_units=["wdays", "whours"], home=0, label="Duration requested"),
        grid={"wdays": [3, 5, 8, 10, 12, 15, 20]},
        rng_rec={"wdays": (1, 25, 1), "whours": (8, 200, 4)},
        unit_note="One leave day equals 8 recorded hours.",
        style="above", outs=["division VP", "department director", "line manager"], default="team lead",
        excs=[_exc("x_medical", "Certified medical leave", ("Yes", "No"),
                   "the leave is certified medical leave", "HR business partner",
                   "x_probation", "Still on probation", ("Yes", "No"),
                   "the employee is still on probation"),
              _exc("x_blackout", "Overlaps blackout period", ("Yes", "No"),
                   "the leave overlaps a declared blackout period", "division VP",
                   "x_preplanned", "In approved annual leave plan", ("Yes", "No"),
                   "the dates were already in the approved annual leave plan")],
        flag_home=0, modes=["role"], roles_home=2,
        roles=["team lead", "line manager", "department director", "division VP", "HR business partner"],
        who="the employee",
        filler=["Leave balances are recalculated on the first business day of each month; negative balances are reported to payroll.",
                "Public holidays falling inside approved leave are not deducted from the balance.",
                "Managers should respond to leave requests within five business days; late responses are tracked on the HR dashboard."],
    ),
    dict(
        name="banking", orgs=["Crescent Bank Retail Credit", "Alder Savings", "First Meridian Lending"],
        levels=[dict(label="Application", plural="Applications", pre="APP-", dig=6,
                     deco=[("Product", "pick:personal loan|auto loan|home improvement loan"), ("Amount requested", "money:3000:60000")]),
                dict(label="Customer", plural="Customers", pre="CUS-", dig=5,
                     deco=[("Name", "name"), ("Customer since", "pick:2011|2015|2018|2020|2022")]),
                dict(label="Branch", plural="Branches", pre="BR-", dig=3, deco=[("Location", "city")])],
        link=["Customer", "Branch", "Credit circular"], keyname="circular",
        keys=["NE-4", "SW-2", "CEN-1", "NW-3", "SE-5"],
        titles=["Retail Credit Circular", "Lending Policy Circular", "Consumer Credit Standard"],
        gov=dict(home=0, label="Application date", phrase="application date"),
        attr=dict(kinds=["number"], name="debt-to-income ratio", group="ratio", rule_units=["percent"],
                  rec_units=["percent", "fraction"], home=0, label="Debt-to-income (DTI)"),
        grid={"percent": [30, 33, 35, 36, 38, 40, 42, 43, 45, 50]},
        rng_rec={"percent": (18, 62, 1), "fraction": ("0.18", "0.62", "0.01")},
        style="below", outs=["Approve", "Approve with collateral", "Refer to credit committee"], default="Decline",
        excs=[_exc("x_arrears", "Arrears in last 12 months", ("Yes", "No"),
                   "the customer was in arrears at any time in the last 12 months", "Decline",
                   "x_hardship", "Arrears cured under hardship plan", ("Yes", "No"),
                   "the arrears were cured under an approved hardship plan"),
              _exc("x_staff", "Bank employee", ("Yes", "No"),
                   "the applicant is a bank employee", "Refer to credit committee",
                   "x_staffscheme", "Within staff-scheme limit", ("Yes", "No"),
                   "the loan falls within the staff lending scheme limit")],
        flag_home=1, modes=["label"], what=["credit decision", "lending decision"], who="the applicant",
        filler=["Identity documents must be verified before funds are released; verification does not affect the credit decision itself.",
                "Rate quotes are valid for 30 days from issue and are produced by the pricing engine.",
                "Complaints about lending decisions are handled under the complaints procedure, not by re-running the circular."],
    ),
    dict(
        name="manufacturing_qa", orgs=["Plant 3 Quality", "Vector Components QA", "Linden Molding Quality Office"],
        levels=[dict(label="NCR", plural="Nonconformance reports", pre="NCR-", dig=4, deco=[("Raised by", "name")]),
                dict(label="Lot", plural="Lots", pre="LOT-", dig=4,
                     deco=[("Part number", "pick:PN-2210|PN-4471|PN-0935|PN-7718"), ("Quantity", "int:500:20000")]),
                dict(label="Material batch", plural="Material batches", pre="MB-", dig=5,
                     deco=[("Resin grade", "pick:PA66-GF30|PBT-15|POM-H|ABS-HI")])],
        link=["Lot", "Material batch", "Supplier"], keyname="supplier",
        keys=["SUP-AX", "SUP-KL", "SUP-MR", "SUP-TQ", "SUP-VN", "SUP-RD"],
        titles=["Supplier Quality Agreement", "Incoming Disposition Rule", "SQA Disposition Annex"],
        gov=dict(home=1, label="Inspected", phrase="inspection date"),
        attr=dict(kinds=["number"], name="defect rate", group="defect", rule_units=["percent", "ppm"],
                  rec_units=["ppm", "percent"], home=1, label="Measured defect rate"),
        grid={"percent": ["0.1", "0.2", "0.25", "0.5", "1", "1.5", "2"],
              "ppm": [1000, 2000, 2500, 5000, 10000, 15000, 20000]},
        rng_rec={"ppm": (200, 30000, 100), "percent": ("0.02", "3", "0.01")},
        unit_note="1% = 10,000 ppm.",
        style="above", outs=["SCR", "RWK", "QHD"], default="REL",
        card={"SCR": "scrap the lot and debit the supplier", "RWK": "sort/rework at supplier cost before use",
              "QHD": "quarantine hold pending engineering review", "REL": "release to production",
              "RTS": "return the entire lot to the supplier"},
        excs=[_exc("x_safety", "Safety-critical characteristic affected", ("Yes", "No"),
                   "a safety-critical characteristic is affected", "RTS",
                   "x_waiver", "Customer deviation waiver on file", ("Yes", "No"),
                   "a customer deviation waiver is on file"),
              _exc("x_fai", "First-article lot", ("Yes", "No"),
                   "the lot is a first-article lot", "QHD",
                   "x_faiok", "First-article inspection signed off", ("Yes", "No"),
                   "the first-article inspection report has been signed off")],
        flag_home=1, modes=["label"], what=["disposition code", "lot disposition"], who="the production supervisor",
        filler=["Calibration certificates for gauges used in incoming inspection are kept in the metrology log.",
                "Supplier scorecards are published quarterly; individual dispositions feed the scorecard automatically.",
                "Retained samples are stored for 12 months in the QA cage, shelf C."],
    ),
    dict(
        name="healthcare_scheduling", orgs=["Northside Children's Access Centre", "Valley Health Scheduling", "Riverbend Pediatrics"],
        levels=[dict(label="Appointment request", plural="Appointment requests", pre="APR-", dig=5,
                     deco=[("Requested by", "name")]),
                dict(label="Referral", plural="Referrals", pre="RF-", dig=5,
                     deco=[("Referring clinician", "drname")]),
                dict(label="Clinic", plural="Clinics", pre="CLN-", dig=3,
                     deco=[("Site", "pick:Eastside|Harbor Point|Mill Road|Westgate")])],
        link=["Referral", "Clinic", "Booking protocol"], keyname="protocol",
        keys=["PED-A", "PED-B", "GEN-2", "FAM-1", "URG-3"],
        titles=["Scheduling Protocol", "Booking Rules", "Access Standard"],
        gov=dict(home=1, label="Referral received", phrase="date the referral was received"),
        attr=dict(kinds=["number"], name="patient age", group="age", rule_units=["months", "years"],
                  rec_units=["months", "years"], home=1, label="Patient age at referral"),
        grid={"months": [3, 6, 12, 18, 24, 36, 60], "years": [1, 2, 3, 5, 12, 16, 18]},
        rng_rec={"months": (0, 230, 1), "years": (0, 19, 1)},
        unit_note="Recorded ages are exact as of the referral date; 1 year = 12 months.",
        style="below", outs=["Same-day slot", "Within 72 hours", "Within 2 weeks"],
        default="Routine (next available)",
        excs=[_exc("x_fever", "Triage fever flag", ("Yes", "No"),
                   "the triage nurse recorded a fever flag", "Same-day slot",
                   "x_seen", "Seen in urgent care within 24 h", ("Yes", "No"),
                   "the patient was already seen in urgent care within the previous 24 hours"),
              _exc("x_transfer", "Transferring from another health system", ("Yes", "No"),
                   "the patient is transferring care from another health system", "Within 2 weeks",
                   "x_norecords", "Prior records outstanding", ("Yes", "No"),
                   "prior records have not yet been received")],
        flag_home=1, modes=["label"], what=["booking pathway", "scheduling priority"], who="the parent",
        filler=["Interpreter bookings should be requested at the same time as the appointment; they do not change the booking pathway.",
                "Reminder texts are sent 48 hours and 2 hours before each appointment.",
                "Parking validation is available at the Eastside and Westgate reception desks."],
    ),
    dict(
        name="telecom_saas", orgs=["Stratus Cloud Support", "Meridian Telecom Business Care", "Halcyon SaaS Ops"],
        levels=[dict(label="Credit request", plural="Credit requests", pre="CR-", dig=5,
                     deco=[("Requested by", "name")]),
                dict(label="Incident", plural="Incidents", pre="INC-", dig=6,
                     deco=[("Service", "pick:API gateway|VoIP trunk|object storage|SSO|email relay")]),
                dict(label="Account", plural="Accounts", pre="ACC-", dig=5, deco=[("Company", "company")])],
        link=["Incident", "Account", "SLA tier"], keyname="tier",
        keys=["GOLD", "ENTERPRISE", "SILVER", "STANDARD", "PREM-24", "BIZ-PLUS"],
        titles=["Service Level Schedule", "SLA Credit Table", "Uptime Commitment"],
        gov=dict(home=1, label="Incident date", phrase="incident date"),
        attr=dict(kinds=["number"], name="outage duration", group="time", rule_units=["minutes", "hours"],
                  rec_units=["minutes", "hours"], home=1, label="Outage duration"),
        grid={"minutes": [15, 30, 45, 60, 90, 120, 240], "hours": [1, 2, 3, 4, 6, 8, 12]},
        rng_rec={"minutes": (5, 600, 5), "hours": ("0.5", "14", "0.5")},
        style="above", outs=["50% service credit", "25% service credit", "10% service credit"],
        default="No service credit",
        pct={"50% service credit": 50, "25% service credit": 25, "10% service credit": 10, "No service credit": 0},
        excs=[_exc("x_maint", "Inside scheduled maintenance window", ("Yes", "No"),
                   "the outage occurred inside a scheduled maintenance window", "No service credit",
                   "x_shortnotice", "Maintenance notice under 72 h", ("Yes", "No"),
                   "the maintenance notice was given less than 72 hours in advance"),
              _exc("x_custcause", "Customer-caused", ("Yes", "No"),
                   "the outage was caused by the customer's own configuration", "No service credit",
                   "x_ourdefect", "Root cause also includes provider defect", ("Yes", "No"),
                   "the root-cause report also identifies a provider defect")],
        flag_home=1, modes=["amount", "label"], base=dict(home=2, label="Monthly fee", lo=400, hi=24000),
        what=["service credit", "SLA outcome"], what_amt=["service credit amount", "credit amount owed"],
        who="the account owner",
        filler=["Status-page updates are published every 30 minutes during a major incident.",
                "Credits are applied to the next invoice and cannot be exchanged for cash.",
                "Post-incident reviews are shared with enterprise customers within ten business days."],
    ),
    dict(
        name="education_admissions", orgs=["Office of Admissions", "Graduate & Undergraduate Admissions", "Admissions Review Unit"],
        levels=[dict(label="Application", plural="Applications", pre="ADM-", dig=5,
                     deco=[("Term", "pick:Fall 2026|Spring 2027|Fall 2027")]),
                dict(label="Applicant", plural="Applicants", pre="STU-", dig=6, deco=[("Name", "name")]),
                dict(label="Program", plural="Programs", pre="PRG-", dig=3,
                     deco=[("Program name", "pick:BSc Mechanical Engineering|BBA Finance|BSN Nursing|BA Design|BSc Biology")])],
        link=["Applicant", "Program", "Admission standard"], keyname="standard",
        keys=["AS-ENG", "AS-BUS", "AS-HLT", "AS-ART", "AS-SCI"],
        titles=["Admission Standard", "Entry Requirements", "Admissions Policy"],
        gov=dict(home=0, label="Submitted", phrase="application submission date"),
        attr=dict(kinds=["number"], name="entry score", group="score", rule_units=["score"],
                  rec_units=["score", "gpa"], home=1, label="Entry score"),
        grid={"score": [60, 65, 70, 72, 75, 80, 85, 88, 90]},
        rng_rec={"score": (50, 99, 1), "gpa": ("2.00", "3.96", "0.04")},
        unit_note="Where only a GPA (4.0 scale) is on file, the percentage-scale score equals GPA x 25.",
        style="above", outs=["Admit", "Conditional admit", "Waitlist"], default="Decline",
        excs=[_exc("x_transfer", "Transfer applicant", ("Yes", "No"),
                   "the applicant is a transfer applicant", "Refer to transfer committee",
                   "x_evaluated", "Transfer credits already evaluated by registrar", ("Yes", "No"),
                   "the registrar has already evaluated the transfer credits"),
              _exc("x_noelp", "English proficiency evidence missing", ("Yes", "No"),
                   "English proficiency evidence is missing", "Conditional admit",
                   "x_elpwaiver", "Proficiency waiver granted", ("Yes", "No"),
                   "a proficiency waiver has been granted")],
        flag_home=1, modes=["label"], what=["admission decision"], who="the applicant",
        filler=["Application fee waivers are processed by Student Finance and have no effect on the academic decision.",
                "Transcripts in languages other than English must be accompanied by a certified translation.",
                "Campus tours run every Friday during term; booking is via the visitor portal."],
    ),
    dict(
        name="travel_expenses", orgs=["Corporate Travel & Expenses", "Finance Shared Services", "T&E Audit Team"],
        levels=[dict(label="Expense report", plural="Expense reports", pre="EXP-", dig=5,
                     deco=[("Employee", "name")]),
                dict(label="Trip", plural="Trips", pre="TRP-", dig=4,
                     deco=[("Purpose", "pick:client workshop|trade fair|site audit|conference|training")]),
                dict(label="Destination", plural="Destinations", pre="DST-", dig=3, deco=[("City", "city")])],
        link=["Trip", "Destination", "Lodging zone"], keyname="zone",
        keys=["Z1", "Z2", "Z3", "Z4", "EU-2", "EU-3", "AP-1"],
        titles=["Lodging Reimbursement Schedule", "Travel Per-Diem Table", "Lodging Cap Policy"],
        gov=dict(home=1, label="Trip start", phrase="trip start date"),
        attr=dict(kinds=["number"], name="nightly lodging rate", group="money", rule_units=["usd"],
                  rec_units=["usd", "eur"], home=0, label="Nightly rate claimed"),
        grid={"usd": [150, 160, 175, 180, 190, 200, 210, 220, 240, 250, 275, 300]},
        rng_rec={"usd": (110, 340, 1), "eur": (100, 300, 1)},
        unit_note="Finance conversion rate for this period: 1 EUR = {rate} USD.",
        style="below", outs=["Reimburse in full", "Reimburse up to the zone cap"],
        default="Reject (VP pre-approval required)",
        excs=[_exc("x_block", "Booked in conference hotel block", ("Yes", "No"),
                   "the room was booked in the official conference hotel block", "Reimburse in full",
                   "x_outside", "Claimed nights outside block dates", ("Yes", "No"),
                   "any claimed night falls outside the block dates"),
              _exc("x_personal", "Stay extended for personal reasons", ("Yes", "No"),
                   "the stay was extended for personal reasons", "Reimburse up to the zone cap",
                   "x_cheaper", "Extension documented as lowering total trip cost", ("Yes", "No"),
                   "the extension is documented as lowering the total trip cost")],
        flag_home=0, modes=["label"], what=["reimbursement decision", "lodging reimbursement outcome"],
        who="the traveler",
        filler=["Receipts must be itemised; credit-card slips alone are not accepted as proof of lodging.",
                "Mileage is reimbursed at the published rate and is reviewed separately from lodging.",
                "Expense reports should be submitted within 30 days of trip end; late submission is reported to the cost-centre owner."],
    ),
    dict(
        name="retail_returns", orgs=["Customer Returns Centre", "Brightmoor Returns Desk", "Omni-channel Returns Team"],
        levels=[dict(label="Return request", plural="Return requests", pre="RMA-", dig=5,
                     deco=[("Channel", "pick:store|online|call center")]),
                dict(label="Order line", plural="Order lines", pre="OL-", dig=6,
                     deco=[("Customer", "name"), ("Price paid", "money:15:1200")]),
                dict(label="SKU", plural="SKUs", pre="SKU-", dig=5,
                     deco=[("Product", "pick:wireless earbuds|smartwatch|air fryer|trail jacket|kids' scooter|desk lamp|blender")])],
        link=["Order line", "SKU", "Category"], keyname="category",
        keys=["ELEC", "HOME", "APPAREL", "TOYS", "WEAR", "OUTDR", "BEAUTY"],
        titles=["Returns Policy", "Return & Refund Rules", "Returns Matrix"],
        gov=dict(home=1, label="Purchased", phrase="purchase date"),
        attr=dict(kinds=["dates"], name="time since purchase", group="time", rule_units=["days"],
                  rec_units=["days"], home=1, label="",
                  dates=dict(a=None, b=(0, "Return received"), gov_is="a", off=(0, 0))),
        grid={"days": [7, 14, 15, 21, 28, 30, 45, 60, 90]},
        rng_rec={"days": (1, 100, 1)},
        style="below", outs=["Full refund", "Store credit only"], default="Return refused",
        excs=[_exc("x_opened", "Packaging opened", ("Yes", "No"),
                   "the item's packaging has been opened", "Exchange only",
                   "x_defective", "Reported defective", ("Yes", "No"),
                   "the item was reported defective"),
              _exc("x_final", "Sold as final sale", ("Yes", "No"),
                   "the item was sold as final sale", "Return refused",
                   "x_defective", "Reported defective", ("Yes", "No"),
                   "the item was reported defective")],
        flag_home=0, modes=["label"], what=["return outcome", "refund decision"], who="the shopper",
        filler=["Refunds are issued to the original payment method; gift-card purchases are refunded to a new gift card.",
                "Return labels are emailed within one business day of approval.",
                "Items returned in store are inspected at the service desk before the outcome is recorded."],
    ),
    dict(
        name="compliance_privacy", orgs=["Privacy Operations", "Data Protection Office", "Compliance Desk"],
        levels=[dict(label="Ticket", plural="Tickets", pre="PRV-", dig=4, deco=[("Opened by", "name")]),
                dict(label="Request", plural="Requests", pre="DSR-", dig=5,
                     deco=[("Request type", "pick:access|erasure|rectification|portability")]),
                dict(label="Data subject", plural="Data subjects", pre="SUB-", dig=6,
                     deco=[("Segment", "pick:consumer|business contact|former customer")])],
        link=["Request", "Data subject", "Region schedule"], keyname="region",
        keys=["REG-N", "REG-W", "REG-E", "REG-S", "REG-C"],
        titles=["DSR Response Schedule", "Data Subject Request Standard", "Privacy Operations Schedule"],
        gov=dict(home=1, label="Received", phrase="date the request was received"),
        attr=dict(kinds=["dates"], name="time elapsed since receipt", group="time",
                  rule_units=["days", "weeks"], rec_units=["days"], home=1, label="",
                  dates=dict(a=None, b=(0, "Status as of"), gov_is="a", off=(0, 0))),
        grid={"days": [14, 20, 21, 25, 28, 30, 40, 45], "weeks": [2, 3, 4, 6]},
        rng_rec={"days": (1, 60, 1)},
        style="above", outs=["Overdue: notify the DPO", "At risk: escalate to privacy lead"],
        default="On track: no action",
        excs=[_exc("x_hold", "Data under legal hold", ("Yes", "No"),
                   "the requested data is under a legal hold", "Suspended: legal hold",
                   "x_released", "Legal hold released", ("Yes", "No"),
                   "the legal hold has been released"),
              _exc("x_unverified", "Identity not yet verified", ("Yes", "No"),
                   "the requester's identity has not been verified", "Paused: awaiting identity check",
                   "x_waived", "Verification waived by DPO", ("Yes", "No"),
                   "the DPO has waived verification")],
        flag_home=1, modes=["label"], what=["required action", "handling status"], who="the requester",
        filler=["Responses are sent through the secure portal; email is used only for the notification link.",
                "Redaction of third-party data is performed by the review team before release.",
                "The records-of-processing register is reviewed annually by the DPO."],
    ),
    dict(
        name="public_benefits", orgs=["County Benefits Office", "Community Assistance Division", "Benefits Eligibility Unit"],
        levels=[dict(label="Application", plural="Applications", pre="BEN-", dig=5,
                     deco=[("Program", "pick:energy assistance|food support|childcare subsidy")]),
                dict(label="Household", plural="Households", pre="HH-", dig=5,
                     deco=[("Head of household", "name")]),
                dict(label="County office", plural="County offices", pre="CO-", dig=3,
                     deco=[("County", "pick:Ashford|Brookline|Carver|Dunmore|Elm Valley")])],
        link=["Household", "County office", "Eligibility schedule"], keyname="schedule",
        keys=["SCH-A", "SCH-B", "SCH-C", "SCH-D", "SCH-7"],
        titles=["Income Eligibility Schedule", "Benefit Determination Table", "Eligibility Rules"],
        gov=dict(home=0, label="Filed", phrase="filing date"),
        attr=dict(kinds=["number"], name="household income", group="income", rule_units=["usd_mo", "usd_yr"],
                  rec_units=["usd_mo", "usd_yr"], home=1, label="Reported income"),
        grid={"usd_mo": [1500, 1650, 1800, 2000, 2200, 2400, 2600, 3000],
              "usd_yr": [18000, 19800, 21600, 24000, 26400, 28800, 31200, 36000]},
        rng_rec={"usd_mo": (800, 3600, 25), "usd_yr": (9600, 43200, 300)},
        unit_note="Annual amounts equal 12 x the monthly amount.",
        style="below", outs=["Full benefit", "Partial benefit"], default="Ineligible",
        excs=[_exc("x_disab", "Member receives disability support", ("Yes", "No"),
                   "a household member receives disability support", "Refer to caseworker (disability review)",
                   "x_detfile", "Disability determination on file", ("Yes", "No"),
                   "a disability determination is already on file"),
              _exc("x_selfemp", "Self-employment income", ("Yes", "No"),
                   "the household reports self-employment income", "Refer to caseworker (income verification)",
                   "x_taxret", "Tax return provided", ("Yes", "No"),
                   "a tax return has been provided")],
        flag_home=1, modes=["label"], what=["benefit determination", "eligibility outcome"],
        who="the applicant's advocate",
        filler=["Notices of decision are mailed within ten business days and are also available in the online account.",
                "Applicants may request an interpreter at no cost at any stage.",
                "Office hours are 8:30 to 16:30, Monday to Friday; the office is closed on county holidays."],
    ),
]
DOMAIN_NAMES = [d["name"] for d in DOMAINS]
# which record levels may be shown (level indexes into dom["levels"]); the last shown level links to the policy key
LEVEL_SETS = {
    "logistics": {1: [(2,)], 2: [(1, 2), (0, 2)], 3: [(0, 1, 2)]},
    "insurance": {1: [], 2: [(0, 2)], 3: [(0, 1, 2)]},
    "hr_leave": {1: [], 2: [(0, 2)], 3: [(0, 1, 2)]},
    "banking": {1: [(1,)], 2: [(0, 1), (0, 2)], 3: [(0, 1, 2)]},
    "manufacturing_qa": {1: [(1,)], 2: [(0, 1), (1, 2)], 3: [(0, 1, 2)]},
    "healthcare_scheduling": {1: [(1,)], 2: [(0, 1), (1, 2)], 3: [(0, 1, 2)]},
    "telecom_saas": {1: [], 2: [(1, 2)], 3: [(0, 1, 2)]},
    "education_admissions": {1: [(1,)], 2: [(0, 1), (1, 2)], 3: [(0, 1, 2)]},
    "travel_expenses": {1: [(0,)], 2: [(0, 1), (0, 2)], 3: [(0, 1, 2)]},
    "retail_returns": {1: [(1,)], 2: [(0, 1), (0, 2)], 3: [(0, 1, 2)]},
    "compliance_privacy": {1: [(1,)], 2: [(0, 1), (1, 2)], 3: [(0, 1, 2)]},
    "public_benefits": {1: [(1,)], 2: [(0, 1), (1, 2)], 3: [(0, 1, 2)]},
}
# requester-favourability order (best first), used so that surface cues ask for something better than gold
FAV = {
    "logistics": ["Full freight refund", "50% freight credit", "25% freight credit", "Refer to the claims desk", "No compensation"],
    "insurance": ["Covered at 100% (accident benefit)", "Covered at 90%", "Covered at 80%", "Covered at 50%",
                  "Not covered (waiting period)", "Not covered (pre-existing condition)"],
    "banking": ["Approve", "Approve with collateral", "Refer to credit committee", "Decline"],
    "manufacturing_qa": ["REL", "QHD", "RWK", "RTS", "SCR"],
    "healthcare_scheduling": ["Same-day slot", "Within 72 hours", "Within 2 weeks", "Routine (next available)"],
    "telecom_saas": ["50% service credit", "25% service credit", "10% service credit", "No service credit"],
    "education_admissions": ["Admit", "Conditional admit", "Refer to transfer committee", "Waitlist", "Decline"],
    "travel_expenses": ["Reimburse in full", "Reimburse up to the zone cap", "Reject (VP pre-approval required)"],
    "retail_returns": ["Full refund", "Store credit only", "Exchange only", "Return refused"],
    "compliance_privacy": ["Overdue: notify the DPO", "At risk: escalate to privacy lead", "On track: no action",
                           "Paused: awaiting identity check", "Suspended: legal hold"],
    "public_benefits": ["Full benefit", "Partial benefit", "Refer to caseworker (disability review)",
                        "Refer to caseworker (income verification)", "Ineligible"],
}
NO_SHORT = {"hr_leave"}  # five named role holders per department cannot fit in <600 chars

GENERIC_FILLER = [
    ("Confidentiality", "This file contains internal information of {org}. Do not forward it outside the handling team. Printed copies must be shredded after {n} days."),
    ("Record retention", "Case records are retained for {k} years after closure under the retention schedule maintained by {name}. Attachments larger than {m} MB are archived separately."),
    ("Contact", "Questions about this file: {name}, ext. {ext}, Monday to Friday 9:00-17:00. Out-of-hours escalations go to the duty coordinator listed on the intranet."),
    ("Glossary", "'Business day': Monday to Friday excluding public holidays. 'Portal': the self-service site. 'Case owner': the person assigned in the queue. These definitions are provided for convenience only."),
    ("Formatting requirements", "Submissions must quote the case number in the subject line, use PDF for attachments and include a contact phone number. Handwritten forms are accepted only if legible."),
    ("Audit trail", "Last automated sync: {date}. Sync job #{n} completed with 0 errors. The previous sync on {date2} flagged {m} formatting warnings, all since resolved."),
    ("Training reminder", "All reviewers must complete the annual refresher by {date}. Completion is tracked in the learning system; this reminder has no bearing on individual decisions."),
    ("System notice", "The records portal will be unavailable on {date} from 01:00 to 03:00 for maintenance. Exports generated during this window may be incomplete and should be re-run."),
    ("Language", "Correspondence is conducted in English. Translations supplied by the requester are for information only."),
    ("Data protection", "Personal data in this file is processed only for the purpose of handling the case. Every access is logged and reviewed monthly by {name}."),
    ("Service standards", "We aim to acknowledge new cases within {k} business days and to update requesters at least every {m} days while a case is open."),
    ("Escalation contacts", "Level 1: queue owner. Level 2: team supervisor ({name}). Level 3: operations manager ({name2}). Escalation does not change which rules apply."),
    ("Clause 7 - Notices", "Formal notices under this document must be delivered in writing to the address on file. Email notices are effective upon confirmed receipt."),
    ("Clause 9 - Severability", "If any provision is held unenforceable, the remaining provisions continue in full force and effect."),
    ("Clause 11 - Governing language", "Where language versions conflict, the English text prevails."),
    ("Meeting notes (unrelated)", "Team stand-up {date}: discussed queue backlog ({n} items), holiday cover and the new document scanner. No decisions affecting open cases were taken."),
    ("Queue statistics", "Cases opened this month: {n}. Closed: {n2}. Median handling time: {k} days. Oldest open case: {m} days."),
    ("Document control", "Owner: {name}. Reviewed by: {name2}. Classification: internal. Next scheduled review: {date}."),
]
PROC_CLAUSES = [
    "Supporting documents must be attached as PDF files.",
    "The case owner records the outcome in the case system within two business days.",
    "Questions about this document go to the policy mailbox, not to individual reviewers.",
    "Headings are for convenience only and do not affect interpretation.",
    "Section headings are not part of the operative text.",
    "Copies of this document held outside the policy library are uncontrolled.",
]

COND_W = {
    ">=": ["at least {t}", "{t} or more", "no less than {t}", "not less than {t}"],
    ">": ["more than {t}", "over {t}", "in excess of {t}", "greater than {t}"],
    "<=": ["at most {t}", "{t} or less", "no more than {t}", "not more than {t}"],
    "<": ["less than {t}", "under {t}", "below {t}", "lower than {t}"],
}
SYM = {">=": "≥", ">": ">", "<=": "≤", "<": "<"}
NEG = {">=": "<", ">": "<=", "<=": ">", "<": ">="}
FLIP = {">=": ">", ">": ">=", "<=": "<", "<": "<="}
DNEG = {">=": "not less than {t}", ">": "not {t} or less", "<=": "not more than {t}", "<": "not {t} or more"}
_OPS = {">=": operator.ge, ">": operator.gt, "<=": operator.le, "<": operator.lt}

Q_CHOICE = {
    "label": [
        "What is the {what} for {ent}?",
        "Which {what} applies to {ent} under the documents that actually govern it?",
        "Trace {ent} through the records and apply the controlling rule. What is the {what}?",
        "{Ent}: which {what} is correct?",
        "Determine the operative {what} for {ent}.",
        "Based only on the records and the rule version in force, what {what} should be recorded for {ent}?",
        "Resolve {ent} to its governing {keyname} document and give the {what}.",
        "A reviewer must close out {ent}. Which {what} is right?",
    ],
    "role": [
        "Who must approve {ent}?",
        "Whose sign-off is required for {ent}?",
        "Under the matrix actually in force, who is the required approver for {ent}?",
        "{Ent} needs approval. From whom?",
        "Trace {ent} to its department and approval matrix. Who approves it?",
        "Name the person whose approval {ent} requires.",
    ],
    "amount": [
        "What is the {what} for {ent}?",
        "How much is due on {ent}?",
        "Trace {ent} through the records and compute the {what}.",
        "{Ent}: what {what} results?",
        "Apply the governing schedule to {ent}. What is the {what}?",
        "What {what} should be booked for {ent}?",
    ],
}
Q_NOUL = {
    "label": [
        "Is the {what} for {ent} \"{x}\"?",
        "Under the governing rules, does {ent} come out as \"{x}\"?",
        "Should {ent} be recorded as \"{x}\"?",
        "Is \"{x}\" the correct {what} for {ent}?",
        "Does the operative rule give \"{x}\" for {ent}?",
        "A colleague proposes \"{x}\" for {ent}. Is that correct?",
    ],
    "role": [
        "Is {x} the person who must approve {ent}?",
        "Does {ent} require {x}'s approval (as the required approver)?",
        "Is {x} the correct approver for {ent}?",
        "Should {ent} be routed to {x} for approval?",
    ],
    "amount": [
        "Is the {what} for {ent} exactly {x}?",
        "Does {ent} result in {x}?",
        "Is {x} the correct {what} for {ent}?",
        "Should {x} be booked for {ent}?",
    ],
}
SUFFIX_CHOICE = [" Choose one option.", " Select the single correct option.", " Pick exactly one.", ""]
SUFFIX_NOUL = [" Answer 1 for yes, 0 for no.", " Reply yes (1) or no (0).", " Answer 1 (yes) or 0 (no).", ""]

MK_NAMES = {
    "superseded": "applied a superseded revision",
    "future": "applied a revision not yet in force on the governing date",
    "draft": "applied an unapproved draft",
    "alias": "ignored the rename/merger notice",
    "boundary": "inclusive/exclusive boundary error",
    "unit": "unit mix-up (no conversion)",
    "no_exc": "missed the exception",
    "unless_ign": "missed the exception to the exception",
}


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _fd(d, st):
    if st == 0:
        return d.isoformat()
    if st == 1:
        return f"{d.day} {calendar.month_name[d.month]} {d.year}"
    if st == 2:
        return f"{calendar.month_name[d.month]} {d.day}, {d.year}"
    if st == 3:
        return f"{d.day:02d} {calendar.month_abbr[d.month]} {d.year}"
    return f"{calendar.month_abbr[d.month]} {d.day}, {d.year}"


def _uname(rng, used, dr=False):
    for _ in range(200):
        n = f"{rng.choice(FIRST)} {rng.choice(LAST)}"
        if n not in used:
            used.add(n)
            return ("Dr " + n) if dr else n
    n = f"{rng.choice(FIRST)} {rng.choice(LAST)}-{rng.randint(2, 99)}"
    used.add(n)
    return n


def _rand_id(rng, pre, dig, used):
    while True:
        s = str(rng.randint(1, 9)) + "".join(rng.choice(string.digits) for _ in range(dig - 1))
        c = pre + s
        if c not in used:
            used.add(c)
            return c


def _near_id(rng, s, pre, used):
    base = list(s[len(pre):])
    for _ in range(60):
        d = base[:]
        if rng.random() < 0.55:
            idxs = [i for i in range(len(d) - 1) if d[i] != d[i + 1]]
            if not idxs:
                continue
            i = rng.choice(idxs)
            d[i], d[i + 1] = d[i + 1], d[i]
        else:
            i = rng.randrange(1, len(d)) if len(d) > 1 else 0
            d[i] = str((int(d[i]) + rng.choice([1, 9, 3])) % 10)
        if d[0] == "0":
            continue
        c = pre + "".join(d)
        if c not in used:
            used.add(c)
            return c
    return _rand_id(rng, pre, len(base), used)


def _deco(rng, kind, used_names):
    if kind == "name":
        return _uname(rng, used_names)
    if kind == "drname":
        return _uname(rng, used_names, dr=True)
    if kind.startswith("pick:"):
        return rng.choice(kind[5:].split("|"))
    if kind.startswith("money:"):
        lo, hi = map(int, kind[6:].split(":"))
        return "$" + f"{rng.randint(lo, hi):,}"
    if kind.startswith("int:"):
        lo, hi = map(int, kind[4:].split(":"))
        return f"{rng.randint(lo, hi):,}"
    if kind == "city":
        return rng.choice(CITIES)
    if kind == "kg":
        return f"{rng.randint(2, 900)} kg"
    if kind == "company":
        return rng.choice(COMPANIES)
    return "-"


def _rrange(rng, spec):
    lo, hi, st = (F(str(x)) for x in spec)
    steps = int((hi - lo) / st)
    return lo + st * rng.randint(0, steps)


# --------------------------------------------------------------------------
# rules
# --------------------------------------------------------------------------
def _mk_rule(rng, dom, unit, exc, maxk=9):
    outs = dom["outs"]
    grid = [F(str(x)) for x in dom["grid"][unit]]
    n = len(outs)
    k = rng.randint(max(1, n - 1), n) if n > 1 else 1
    k = min(k, len(grid), maxk)
    idx = sorted(rng.sample(range(n), k))
    th = sorted(rng.sample(grid, k))
    if dom["style"] == "above":
        th = th[::-1]
        ops = (">=", ">")
    else:
        ops = ("<=", "<")
    base = rng.choice(ops)
    tiers = []
    for j in range(k):
        c = base if rng.random() < 0.8 else rng.choice(ops)
        tiers.append((c, th[j], outs[idx[j]]))
    return {"unit": unit, "tiers": tiers, "default": dom["default"], "exc": exc}


def _mk_exc(rng, dom, spec_i=None, p_unless=0.75):
    if spec_i is None:
        spec_i = rng.randrange(len(dom["excs"]))
    e = dom["excs"][spec_i]
    return {"flag": e["flag"], "out": e["out"], "unless": e["unless"] if rng.random() < p_unless else None,
            "spec": spec_i}


def _eval_rule(rule, val, fields, mk=None):
    """Resolver-side evaluator (first matching tier wins; exceptions override)."""
    ex = rule.get("exc")
    if ex and mk != "no_exc":
        if fields.get(ex["flag"]) is True:
            blocked = bool(ex.get("unless")) and fields.get(ex["unless"]) is True
            if (not blocked) or mk == "unless_ign":
                return ex["out"]
    for cmp, thr, out in rule["tiers"]:
        c = FLIP[cmp] if mk == "boundary" else cmp
        if c == ">=" and val >= thr:
            return out
        if c == ">" and val > thr:
            return out
        if c == "<=" and val <= thr:
            return out
        if c == "<" and val < thr:
            return out
    return rule["default"]


def _eval_direct(rule, v, flags):
    """Independent evaluator used by the ground-truth path."""
    ex = rule.get("exc")
    hit = (ex is not None and bool(flags.get(ex["flag"], False))
           and not (ex.get("unless") is not None and bool(flags.get(ex["unless"], False))))
    if hit:
        return ex["out"]
    matched = [o for (c, t, o) in rule["tiers"] if _OPS[c](v, t)]
    return matched[0] if matched else rule["default"]


# --------------------------------------------------------------------------
# world builder
# --------------------------------------------------------------------------
def _build_world(rng, dom, lc):
    A = dom["attr"]
    mode = rng.choice(dom["modes"])
    S = LEVEL_SETS[dom["name"]]
    short = lc == "short"
    if short:
        nlev = 1 if (S[1] and rng.random() < 0.7) else 2
    elif lc == "medium":
        nlev = rng.choice([2, 2, 3])
    else:
        nlev = rng.choice([2, 3, 3, 3])
    lev_set = list(rng.choice(S[nlev]))
    role_hop = 1 if mode == "role" else 0
    alias = None
    if short:
        if nlev == 1 or rng.random() < 0.15:
            alias = "key"
    elif rng.random() < {"medium": 0.6, "long": 0.65}[lc]:
        opts = ["key", "key"] + [("rec", p) for p in range(1, nlev)]
        alias = rng.choice(opts)
    hops = lambda: (nlev - 1) + 1 + (1 if alias else 0) + role_hop
    if hops() < 2:
        alias = "key"
    if hops() > 4:
        alias = None
    kind = rng.choice(A["kinds"])
    ru = rng.choice(A["rule_units"])
    uf = dict(UNIT_GROUPS[A["group"]])
    if "eur" in uf:
        uf["eur"] = rng.choice([F("1.10"), F("1.25"), F("1.20"), F("1.05"), F("1.08")])

    def pos(home):
        if home in lev_set:
            return lev_set.index(home)
        return min(range(nlev), key=lambda p: (abs(lev_set[p] - home), lev_set[p]))

    # ---- field placement
    place = {"gov": pos(dom["gov"]["home"])}
    labels = {"gov": dom["gov"]["label"]}
    if kind == "number":
        place["attr"] = pos(A["home"])
        labels["attr"] = A["label"]
        attr_spec = {"kind": "number"}
    else:
        D = A["dates"]
        a_name, b_name = "da", "db"
        if D["gov_is"] == "a":
            a_name = "gov"
        else:
            place["da"] = pos(D["a"][0])
            labels["da"] = D["a"][1]
        if D["gov_is"] == "b":
            b_name = "gov"
        else:
            place["db"] = pos(D["b"][0])
            labels["db"] = D["b"][1]
        attr_spec = {"kind": "dates", "a": a_name, "b": b_name}
    exc_specs_used = []  # indexes of domain exceptions used anywhere

    # ---- governing date and true policy
    G = _dt.date(2024, 3, 1) + _dt.timedelta(days=rng.randint(0, 900))
    p_exc = {"short": 0.4, "medium": 0.75, "long": 0.8}[lc]
    maxk = 2 if short else 9
    exc_cur = _mk_exc(rng, dom, p_unless=0.5 if short else 0.75) if rng.random() < p_exc else None
    rule_cur = _mk_rule(rng, dom, ru, exc_cur, maxk)

    # ---- value
    rec_units = ["days"] if kind == "dates" else list(A["rec_units"])
    if len(rec_units) > 1 and rng.random() < 0.55:
        alt = [u for u in rec_units if u != ru]
        rec_u = rng.choice(alt) if alt else ru
    else:
        rec_u = ru if ru in rec_units else rec_units[0]
    v_rec = None
    if rng.random() < 0.45:
        t = rng.choice(rule_cur["tiers"])[1]
        cand = t * uf[ru] / uf[rec_u]
        if _clean(cand, rec_u, dates=(kind == "dates")):
            v_rec = cand
        elif kind == "number" and ru in rec_units:
            rec_u = ru
            v_rec = t
    if v_rec is None:
        v_rec = _rrange(rng, dom["rng_rec"][rec_u])
    v_rule = v_rec * uf[rec_u] / uf[ru]

    # ---- flags for the true chain
    flags = {}

    def add_flags(spec_i):
        e = dom["excs"][spec_i]
        if spec_i not in exc_specs_used:
            exc_specs_used.append(spec_i)
        for fl in (e["flag"], e["unless"]):
            if fl not in flags:
                flags[fl] = rng.random() < 0.3

    if exc_cur:
        add_flags(exc_cur["spec"])
        r = rng.random()
        if r < 0.38:
            flags[exc_cur["flag"]] = True
            if exc_cur["unless"]:
                flags[exc_cur["unless"]] = False
        elif r < 0.68:
            flags[exc_cur["flag"]] = True
            if exc_cur["unless"]:
                flags[exc_cur["unless"]] = True
        else:
            flags[exc_cur["flag"]] = False

    cur_out = _eval_direct(rule_cur, v_rule, flags)

    def rule_differs(p_try=0.8, keep_exc=None):
        """Make a rule whose outcome (for the true facts) differs from the current one, usually."""
        want = rng.random() < p_try
        best = None
        for _ in range(14):
            ex = keep_exc
            if ex is None and (not short) and rng.random() < (0.3 if lc == "medium" else 0.45):
                ex = _mk_exc(rng, dom)
            r = _mk_rule(rng, dom, ru, ex, maxk)
            fl = dict(flags)
            if ex:
                e = dom["excs"][ex["spec"]]
                for f_ in (e["flag"], e["unless"]):
                    fl.setdefault(f_, False)
            best = r
            if not want or _eval_direct(r, v_rule, fl) != cur_out:
                break
        if best["exc"]:
            add_flags(best["exc"]["spec"])
        return best

    # ---- versions of the true key
    scheme = rng.randrange(4)
    vfmt = ["Rev {}", "Version {}", "v{}.0", "Issue {}"][scheme]
    n0 = rng.randint(1, 4)
    d_cur = 0 if rng.random() < 0.12 else rng.randint(1, 400)
    v_cur = {"label": vfmt.format(n0 + 1), "eff": G - _dt.timedelta(days=d_cur), "status": "active",
             "rule": rule_cur, "tag": "cur"}
    keep = exc_cur if (exc_cur and rng.random() < 0.4) else None
    v_prev = {"label": vfmt.format(n0), "eff": v_cur["eff"] - _dt.timedelta(days=rng.randint(120, 700)),
              "status": "active", "rule": rule_differs(0.85, keep), "tag": "prev"}
    versions = [v_prev, v_cur]
    extra = rng.random()
    p_next = {"short": 0.2, "medium": 0.45, "long": 0.55}[lc]
    if extra < p_next:
        d_next = 1 if rng.random() < 0.2 else rng.randint(2, 200)
        versions.append({"label": vfmt.format(n0 + 2), "eff": G + _dt.timedelta(days=d_next), "status": "active",
                         "rule": rule_differs(0.85), "tag": "next"})
    elif extra < p_next + 0.2 and lc != "short":
        dl = ["Draft {}", "Version {} (draft)", "v{}.0-draft", "Issue {} (proposed)"][scheme].format(n0 + 2)
        versions.append({"label": dl, "eff": G - _dt.timedelta(days=rng.randint(0, 60)), "status": "draft",
                         "rule": rule_differs(0.85), "tag": "draft"})

    # ---- keys
    keys = list(dom["keys"])
    rng.shuffle(keys)
    K = keys.pop()
    K0 = keys.pop() if alias == "key" else None
    n_other_keys = {"short": (1 if rng.random() < 0.25 else 0), "medium": rng.choice([0, 1, 1]), "long": rng.choice([2, 3])}[lc]
    other_keys = [keys.pop() for _ in range(min(n_other_keys, len(keys) - 1))]
    fake_old = keys[:2]  # used only as decoy entries in a mapping table

    pol = {K: versions}
    for ok in other_keys:
        vs = [{"label": vfmt.format(1), "eff": G - _dt.timedelta(days=rng.randint(500, 1200)), "status": "active",
               "rule": rule_differs(0.7), "tag": "other"}]
        if rng.random() < {"short": 0.0, "medium": 0.15, "long": 0.45}[lc]:
            vs.append({"label": vfmt.format(2), "eff": G - _dt.timedelta(days=rng.randint(0, 450)), "status": "active",
                       "rule": rule_differs(0.7), "tag": "other"})
        pol[ok] = vs
    kalias = {}
    if K0:
        kalias[K0] = K
        if lc != "short" or rng.random() < 0.35:
            pol[K0] = [{"label": vfmt.format(rng.randint(1, 3)), "eff": G - _dt.timedelta(days=rng.randint(300, 1200)),
                        "status": "active", "rule": rule_differs(0.9), "tag": "legacy"}]
        if lc == "long" and rng.random() < 0.6:
            for fo in fake_old[:1]:
                if other_keys:
                    kalias["X" + fo] = rng.choice(other_keys)

    # ---- flag placement
    for si in exc_specs_used:
        e = dom["excs"][si]
        for fl, lab in ((e["flag"], e["flabel"]), (e["unless"], e["ulabel"])):
            place[fl] = pos(dom["flag_home"])
            labels[fl] = lab
    for fl in list(flags):
        if fl not in place:
            del flags[fl]
    if mode == "amount":
        place["base"] = pos(dom["base"]["home"])
        labels["base"] = dom["base"]["label"]
    if mode == "role":
        place["roles"] = pos(dom["roles_home"])
        role_used = []
        for vs in pol.values():
            for v in vs:
                rl = v["rule"]
                role_used += [t[2] for t in rl["tiers"]] + [rl["default"]] + ([rl["exc"]["out"]] if rl.get("exc") else [])
        roles_shown = [r for r in dom["roles"] if r in role_used]

    used_names = set()
    # ---- true field values
    tf = {"gov": G}
    if kind == "number":
        tf["attr"] = (v_rec, rec_u)
    else:
        D = A["dates"]
        vd = _dt.timedelta(days=int(v_rec))
        if D["gov_is"] == "a":
            tf["db"] = G + vd
        elif D["gov_is"] == "b":
            tf["da"] = G - vd
        else:
            a = G + _dt.timedelta(days=rng.randint(*D["off"]))
            tf["da"] = a
            tf["db"] = a + vd
    for fl in flags:
        tf[fl] = flags[fl]
    base_true = None
    if mode == "amount":
        base_true = F(rng.randint(dom["base"]["lo"], dom["base"]["hi"]))
        tf["base"] = base_true
    roles_true = None
    if mode == "role":
        roles_true = {r: _uname(rng, used_names) for r in roles_shown}
        tf["roles"] = roles_true

    def rand_fields(p):
        f = {}
        g = G + _dt.timedelta(days=rng.randint(-150, 150))
        rv = _rrange(rng, dom["rng_rec"]["days" if kind == "dates" else rec_u])
        for sem, pp in place.items():
            if pp != p:
                continue
            if sem == "gov":
                f["gov"] = g
            elif sem == "attr":
                u = rec_u if rng.random() < 0.75 else rng.choice(rec_units)
                f["attr"] = (_rrange(rng, dom["rng_rec"][u]), u)
            elif sem == "da":
                D = A["dates"]
                if place.get("gov") == p and D["gov_is"] is None:
                    f["da"] = g + _dt.timedelta(days=rng.randint(*D["off"]))
                elif place.get("gov") == p and D["gov_is"] == "b":
                    f["da"] = g - _dt.timedelta(days=int(rv))
                else:
                    f["da"] = G - _dt.timedelta(days=rng.randint(5, 420))
            elif sem == "db":
                pass
            elif sem == "base":
                f["base"] = F(rng.randint(dom["base"]["lo"], dom["base"]["hi"]))
            elif sem == "roles":
                f["roles"] = {r: _uname(rng, used_names) for r in roles_shown}
            else:
                f[sem] = rng.random() < 0.35
        if place.get("db") == p:
            D = A["dates"]
            if "da" in f:
                f["db"] = f["da"] + _dt.timedelta(days=int(rv))
            elif place.get("gov") == p and D["gov_is"] == "a":
                f["db"] = g + _dt.timedelta(days=int(rv))
            else:
                f["db"] = G + _dt.timedelta(days=rng.randint(1, 60))
        return f

    # ---- records, bottom-up
    near_levels = []
    if lc == "short":
        near_levels = [nlev - 1] if rng.random() < 0.6 else [rng.randrange(nlev)]
    elif lc == "medium":
        near_levels = rng.sample(range(nlev), 1 if rng.random() < 0.7 else min(2, nlev))
    else:
        near_levels = rng.sample(range(nlev), rng.randint(1, nlev))
    n_other = []
    for p in range(nlev):
        if lc == "short":
            n_other.append(0)
        elif lc == "medium":
            n_other.append(rng.choice([0, 0, 1]))
        else:
            n_other.append(rng.choice([1, 2, 2]))
    for p in near_levels:
        if p + 1 < nlev and n_other[p + 1] == 0:
            n_other[p + 1] = 1

    used_ids = set()
    levels = [[] for _ in range(nlev)]
    true_ids = [None] * nlev
    ralias = {}
    near = {}
    old_of = {}
    legacy_ids = []
    for p in reversed(range(nlev)):
        spec = dom["levels"][lev_set[p]]
        tid = _rand_id(rng, spec["pre"], spec["dig"], used_ids)
        true_ids[p] = tid
        # decide old id for a record-level alias at p
        if alias == ("rec", p):
            oid = _rand_id(rng, spec["pre"], spec["dig"], used_ids)
            old_of[p] = oid
            ralias[oid] = tid
        if p == nlev - 1:
            link = K0 if alias == "key" else K
        else:
            link = old_of.get(p + 1, true_ids[p + 1])
        fields = {k2: v for k2, v in tf.items() if place.get(k2) == p}
        levels[p].append({"id": tid, "link": link, "f": fields,
                          "deco": [(lab, _deco(rng, kd, used_names)) for lab, kd in spec["deco"]],
                          "status": None, "tag": "true"})

        def other_link():
            if p == nlev - 1:
                pool = other_keys + [K]
                return rng.choice(pool) if other_keys and rng.random() < 0.75 else (rng.choice(pool))
            cand = [r["id"] for r in levels[p + 1] if r["tag"] in ("other", "near")]
            if cand and rng.random() < 0.85:
                return rng.choice(cand)
            return true_ids[p + 1]

        if p in near_levels:
            nid = _near_id(rng, tid, spec["pre"], used_ids)
            near[tid] = nid
            levels[p].append({"id": nid, "link": other_link(), "f": rand_fields(p),
                              "deco": [(lab, _deco(rng, kd, used_names)) for lab, kd in spec["deco"]],
                              "status": None, "tag": "near"})
        for _ in range(n_other[p]):
            oid2 = _rand_id(rng, spec["pre"], spec["dig"], used_ids)
            levels[p].append({"id": oid2, "link": other_link(), "f": rand_fields(p),
                              "deco": [(lab, _deco(rng, kd, used_names)) for lab, kd in spec["deco"]],
                              "status": None, "tag": "other"})
        if alias == ("rec", p) and (lc != "short" or rng.random() < 0.5):
            # legacy record still present in the table
            lf = rand_fields(p)
            levels[p].append({"id": old_of[p], "link": other_link(), "f": lf,
                              "deco": [(lab, _deco(rng, kd, used_names)) for lab, kd in spec["deco"]],
                              "status": "legacy", "tag": "legacy",
                              "alias_date": G - _dt.timedelta(days=rng.randint(10, 300))})
            legacy_ids.append(old_of[p])

    rec_alias_date = {old: G - _dt.timedelta(days=rng.randint(10, 300)) for old in ralias}
    key_alias_date = G - _dt.timedelta(days=rng.randint(10, 300))

    W = {"levels": levels, "ralias": ralias, "kalias": kalias, "pol": pol, "near": near,
         "query": true_ids[0], "attr": attr_spec, "uf": uf, "mode": mode, "pct": dom.get("pct"),
         "rule_unit": ru}
    T = {"ids": list(true_ids), "key": K, "ver": v_cur, "v_rule": v_rule, "flags": dict(flags),
         "roles": roles_true, "base": base_true}
    info = {"dom": dom, "lc": lc, "nlev": nlev, "lev_set": lev_set, "alias": alias, "K": K, "K0": K0,
            "other_keys": other_keys, "place": place, "labels": labels, "kind": kind, "ru": ru,
            "rec_u": rec_u, "v_rec": v_rec, "G": G, "mode": mode, "exc_specs": exc_specs_used,
            "hops": hops(), "rec_alias_date": rec_alias_date, "key_alias_date": key_alias_date,
            "vfmt": vfmt, "true_ids": true_ids, "old_of": old_of, "legacy_ids": legacy_ids}
    return W, T, info


# --------------------------------------------------------------------------
# resolver (path B) and ground truth (path A)
# --------------------------------------------------------------------------
def _format_answer(W, out, roles, base):
    if W["mode"] == "role":
        if roles is None or out not in roles:
            return None
        return roles[out]
    if W["mode"] == "amount":
        if base is None or out not in W["pct"]:
            return None
        return _money(F(W["pct"][out]) * F(base) / 100)
    return out


def _solve(W, mk=None):
    chain = []
    cur = W["query"]
    for p, recs in enumerate(W["levels"]):
        rid = cur
        if rid in W["ralias"] and mk != "alias":
            rid = W["ralias"][rid]
        if isinstance(mk, tuple) and mk[0] == "near" and mk[1] == p:
            rid = W["near"].get(rid)
            if rid is None:
                return None
        rec = None
        for r in recs:
            if r["id"] == rid:
                rec = r
                break
        if rec is None:
            return None
        chain.append(rec)
        cur = rec["link"]
    key = cur
    if key in W["kalias"] and mk != "alias":
        key = W["kalias"][key]
    fields = {}
    for rec in chain:
        for k2, v in rec["f"].items():
            fields.setdefault(k2, v)
    gov = fields.get("gov")
    vers = W["pol"].get(key)
    if not vers or gov is None:
        return None
    live = [v for v in vers if v["status"] == "active"]
    inforce = sorted([v for v in live if v["eff"] <= gov], key=lambda v: v["eff"])
    if mk == "superseded":
        if len(inforce) < 2:
            return None
        ver = inforce[-2]
    elif mk == "future":
        fut = [v for v in live if v["eff"] > gov]
        if not fut:
            return None
        ver = max(fut, key=lambda v: v["eff"])
    elif mk == "draft":
        dr = [v for v in vers if v["status"] == "draft"]
        if not dr:
            return None
        ver = dr[-1]
    else:
        if not inforce:
            return None
        ver = inforce[-1]
    rule = ver["rule"]
    A = W["attr"]
    if A["kind"] == "number":
        num, unit = fields["attr"]
    else:
        if A["a"] not in fields or A["b"] not in fields:
            return None
        num, unit = F((fields[A["b"]] - fields[A["a"]]).days), "days"
    if mk == "unit":
        if unit == rule["unit"]:
            return None
        val = F(num)
    else:
        val = F(num) * W["uf"][unit] / W["uf"][rule["unit"]]
    out = _eval_rule(rule, val, fields, mk if isinstance(mk, str) else None)
    ans = _format_answer(W, out, fields.get("roles"), fields.get("base"))
    if ans is None:
        return None
    return {"ans": ans, "ids": [r["id"] for r in chain], "ver": ver, "key": key, "val": val,
            "raw": (num, unit), "out": out, "rule": rule}


def _direct(W, T):
    out = _eval_direct(T["ver"]["rule"], T["v_rule"], T["flags"])
    if W["mode"] == "role":
        return T["roles"][out]
    if W["mode"] == "amount":
        pct = {**W["pct"]}[out]
        cents = (F(pct) * T["base"] / 100 * 100)
        q = Decimal(cents.numerator) / Decimal(cents.denominator)
        q = q.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        return "$" + f"{(q / 100):,.2f}"
    return out


def _mistakes(W):
    mks = [("near", p) for p in range(len(W["levels"]))]
    mks += ["superseded", "future", "draft", "alias", "boundary", "unit", "no_exc", "unless_ign"]
    return mks


def _mk_name(mk, W):
    if isinstance(mk, tuple):
        return "look-alike ID"
    return MK_NAMES[mk]


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------
class _Renderer:
    def __init__(self, rng, dom, W, T, info):
        self.rng, self.dom, self.W, self.T, self.I = rng, dom, W, T, info
        self.lc = info["lc"]
        self.compact = self.lc == "short"
        self.ds = 0 if info["lc"] == "short" else rng.randrange(5)
        self.uv = {u: rng.randrange(len(v)) for u, v in UNIT_TPL.items()}
        self.title = rng.choice(dom["titles"])
        self.org = rng.choice(dom["orgs"])
        self.q_name = dom["attr"]["name"]
        if self.compact:
            self.uv = {u: min(range(len(v)), key=lambda j: len(v[j][0])) for u, v in UNIT_TPL.items()}
            self.q_name = SHORT_Q.get(self.q_name, self.q_name)
        self.keyname = dom["keyname"]
        self.used_formats = []
        self.deco_n = rng.choice([0, 1, 1, 2])

    # --- primitives
    def lab(self, label):
        return SHORT_LABEL.get(label, label) if self.compact else label

    def d(self, x):
        return _fd(x, self.ds)

    def qty(self, v, unit):
        pl, sg = UNIT_TPL[unit][self.uv[unit]]
        tpl = sg if F(v) == 1 else pl
        return tpl.format(_ns(v, unit))

    def outp(self, o):
        mode = self.W["mode"]
        if mode == "role":
            return self.rng.choice([f"approval is required from the {o}", f"the {o} approves",
                                    f"the approver is the {o}"])
        if self.dom["name"] == "manufacturing_qa":
            return self.rng.choice([f"disposition {o} applies", f"the lot is dispositioned {o}",
                                    f"use code {o}"])
        return self.rng.choice([f"the outcome is \"{o}\"", f"\"{o}\" applies", f"the result is {o}"])

    def cond(self, c, t, unit):
        return self.rng.choice(COND_W[c]).format(t=self.qty(t, unit))

    # --- records
    def field_pairs(self, rec, p):
        W, I = self.W, self.I
        ls = I["lev_set"]
        link_label = (self.dom["levels"][ls[p + 1]]["label"] if p + 1 < len(ls) else self.dom["link"][2])
        pairs = [(link_label, rec["link"])]
        sem = []
        order = ["gov", "da", "db", "attr"] + [k for k in rec["f"] if k.startswith("x_")] + ["base", "roles"]
        for k2 in order:
            if k2 not in rec["f"]:
                continue
            v = rec["f"][k2]
            if k2 in ("gov", "da", "db"):
                sem.append((self.lab(I["labels"][k2]), self.d(v)))
            elif k2 == "attr":
                sem.append((self.lab(I["labels"]["attr"]), self.qty(v[0], v[1])))
            elif k2 == "base":
                sem.append((self.lab(I["labels"]["base"]), _money(v)))
            elif k2 == "roles":
                for r, nm in v.items():
                    sem.append((r[0].upper() + r[1:], nm))
            else:
                e = next(x for x in self.dom["excs"] if x["flag"] == k2 or x["unless"] == k2)
                vals = e["fvals"] if e["flag"] == k2 else e["uvals"]
                sem.append((I["labels"][k2], vals[0] if v else vals[1]))
        if self.compact:
            deco = []
        elif self.lc == "medium":
            deco = list(rec["deco"])[:self.deco_n]
        else:
            deco = list(rec["deco"])
        if self.rng.random() < 0.4:
            pairs = deco + pairs + sem
        else:
            pairs = pairs + sem + deco
        if rec["status"] == "legacy":
            if self.rng.random() < 0.5:
                pairs.append(("Status", f"merged into {W['ralias'][rec['id']]}"))
            else:
                pairs.append(("Status", "inactive (see notices)"))
        return pairs

    def render_records(self, p, cue=None):
        recs = list(self.W["levels"][p])
        self.rng.shuffle(recs)
        spec = self.dom["levels"][self.I["lev_set"][p]]
        rows = []
        for r in recs:
            pr = self.field_pairs(r, p)
            if cue and r["id"] == self.W["query"]:
                pr.append(("Remarks", cue))
            rows.append((r["id"], pr))
        has_status = any(any(k == "Status" for k, _ in pr) for _, pr in rows)
        if has_status:
            rows = [(i, pr if any(k == "Status" for k, _ in pr) else pr + [("Status", "active")]) for i, pr in rows]
        fmts = ["terse", "terse", "table", "json"] if self.compact else ["table", "json", "bullets", "kv", "prose", "csv"]
        if cue:
            fmts = [f for f in fmts if f not in ("csv",)]
        fmt = self.rng.choice(fmts)
        self.used_formats.append("rec:" + fmt)
        lab = spec["label"]
        if fmt == "terse":
            return "\n".join(f"{i}: " + ", ".join(f"{k.lower()} {v}" for k, v in pr) for i, pr in rows)
        if fmt == "bullets":
            return "\n".join(f"- {i}: " + "; ".join(f"{k}: {v}" for k, v in pr) for i, pr in rows)
        if fmt == "kv":
            return "\n".join(f"{lab} {i}\n" + "\n".join(f"  {k}: {v}" for k, v in pr) for i, pr in rows)
        if fmt == "prose":
            out = []
            for i, pr in rows:
                parts = [f"{k[0].lower() + k[1:]}: {v}" for k, v in pr]
                body = ", ".join(parts[:-1]) + (" and " + parts[-1] if len(parts) > 1 else parts[0])
                lead = self.rng.choice([f"{lab} {i} lists", f"The record for {lab.lower()} {i} shows", f"{lab} {i} -"])
                out.append(f"{lead} {body}" + ("" if body.endswith((".", ".\"")) else "."))
            return " ".join(out) if self.rng.random() < 0.5 else "\n".join(out)
        if fmt == "json":
            def sk(k):
                return "".join(ch if ch.isalnum() else "_" for ch in k.lower()).strip("_").replace("__", "_")
            objs = [{"id": i, **{sk(k): v for k, v in pr}} for i, pr in rows]
            if self.compact or self.rng.random() < 0.6:
                return "\n".join(json.dumps(o, ensure_ascii=False) for o in objs)
            return json.dumps(objs, ensure_ascii=False, indent=1)
        cols = ["ID"]
        for _, pr in rows:
            for k, _v in pr:
                if k not in cols:
                    cols.append(k)
        grid = [[i] + [dict(pr).get(c, "-") for c in cols[1:]] for i, pr in rows]
        if fmt == "csv":
            return "\n".join([",".join(cols)] + [",".join(str(x).replace(",", "") for x in g) for g in grid])
        widths = [max(len(str(c)), *(len(str(g[j])) for g in grid)) for j, c in enumerate(cols)]
        line = lambda vals: " | ".join(str(v).ljust(widths[j]) for j, v in enumerate(vals)).rstrip()
        return "\n".join([line(cols), "-+-".join("-" * w for w in widths)] + [line(g) for g in grid])

    # --- rules
    def exc_text(self, ex, terse=False):
        e = self.dom["excs"][ex["spec"]]
        out = ex["out"]
        if terse:
            s = f"If {e['flabel'].lower()}: {out}"
            if ex["unless"]:
                s += f", unless {e['ulabel'].lower()}"
            return s + "."
        form = self.rng.randrange(4)
        q = self.q_name
        if form == 0:
            s = f"Exception: where {e['cond']}, the outcome is {out} regardless of the {q}."
            if ex["unless"]:
                s += f" This exception does not apply if {e['ucond']}; the schedule above then governs."
        elif form == 1:
            s = f"Notwithstanding the above, {out} applies whenever {e['cond']}"
            s += (f", unless {e['ucond']}, in which case the ordinary schedule is used." if ex["unless"] else ".")
        elif form == 2:
            s = f"The schedule above does not apply where {e['cond']}; such cases receive {out}."
            if ex["unless"]:
                s += f" The preceding sentence does not apply where {e['ucond']}."
        else:
            s = f"Special case - if {e['cond']}: {out}."
            if ex["unless"]:
                s += f" Not applicable if {e['ucond']} (normal schedule applies instead)."
        return s

    def band(self, tiers, i, unit, words):
        c, t, _ = tiers[i]
        if words:
            lo = self.cond(c, t, unit)
            if i == 0:
                return lo[0].upper() + lo[1:]
            pc, pt, _ = tiers[i - 1]
            return f"{lo[0].upper() + lo[1:]} but {self.cond(NEG[pc], pt, unit)}"
        s = f"{SYM[c]} {self.qty(t, unit)}"
        if i == 0:
            return s
        pc, pt, _ = tiers[i - 1]
        return f"{s} and {SYM[NEG[pc]]} {self.qty(pt, unit)}"

    def default_band(self, tiers, unit, words):
        c, t, _ = tiers[-1]
        if words:
            s = self.cond(NEG[c], t, unit)
            return s[0].upper() + s[1:]
        return f"{SYM[NEG[c]]} {self.qty(t, unit)}"

    def rule_text(self, rule, annex_ref=None):
        tiers, unit, q = rule["tiers"], rule["unit"], self.q_name
        dflt = rule["default"]
        if self.compact:
            fmt = "terse"
        else:
            fmt = self.rng.choice(["prose", "clauses", "table", "bullets", "terse"])
        self.used_formats.append("rule:" + fmt)
        lines = []
        if fmt == "terse":
            parts = []
            for i, (c, t, o) in enumerate(tiers):
                parts.append(f"{q if i == 0 else ''}{' ' if i == 0 else ''}{SYM[c]} {self.qty(t, unit)} -> {o}")
            parts.append(f"otherwise {dflt}")
            lines.append("; ".join(parts) + ".")
        elif fmt in ("prose", "clauses"):
            sents = []
            for i, (c, t, o) in enumerate(tiers):
                if i == 0 and c in DNEG and self.rng.random() < 0.18 and self.W["mode"] != "role":
                    sents.append(f"\"{o}\" shall not be withheld where the {q} is "
                                 f"{DNEG[c].format(t=self.qty(t, unit))}.")
                    continue
                lead = "If" if i == 0 else self.rng.choice(["Otherwise, if", "Failing that, if", "Else, if"])
                sents.append(f"{lead} the {q} is {self.cond(c, t, unit)}, {self.outp(o)}.")
            sents.append(self.rng.choice(["In all other cases, ", "Otherwise, ", "In any remaining case, "]) + self.outp(dflt) + ".")
            if fmt == "prose":
                lines.append(" ".join(sents))
            else:
                sec = self.rng.randint(2, 6)
                lines += [f"{sec}.{j + 1} {s}" for j, s in enumerate(sents)]
        else:
            words = self.rng.random() < 0.5
            head = q[0].upper() + q[1:]
            rows = [(self.band(tiers, i, unit, words), o) for i, (c, t, o) in enumerate(tiers)]
            rows.append((self.default_band(tiers, unit, words), dflt))
            if fmt == "table":
                w = max(len(head), *(len(r[0]) for r in rows))
                lines.append(f"{head.ljust(w)} | Outcome")
                lines.append("-" * w + "-+-" + "-" * 12)
                lines += [f"{a.ljust(w)} | {b}" for a, b in rows]
            else:
                lines.append(f"{head}:")
                lines += [f"- {a}: {b}" for a, b in rows]
        ex = rule.get("exc")
        if ex:
            if annex_ref:
                lines.append(self.rng.choice([f"Exceptions: see {annex_ref}.", f"Special cases are set out in {annex_ref}.",
                                              f"This schedule is subject to {annex_ref}."]))
            else:
                lines.append(self.exc_text(ex, terse=(fmt == "terse" and self.compact)))
        if not self.compact and self.lc == "long" and self.rng.random() < 0.6:
            lines.append(self.rng.choice(PROC_CLAUSES))
        return "\n".join(lines)

    def doc_block(self, key, ver, all_vers, annex_ref=None):
        st = self.rng.randrange(4)
        lab = ver["label"]
        if self.compact:
            head = f"{key} {lab} (eff. {self.d(ver['eff'])}"
            if ver["status"] == "draft":
                head += ", DRAFT - not approved"
            head += "): "
            return head + self.rule_text(ver["rule"])
        if st == 0:
            h = f"{self.title} - {self.keyname.capitalize()} {key} - {lab}"
        elif st == 1:
            h = f"{key} {self.title} ({lab})"
        elif st == 2:
            h = f"[{key}] {self.title}, {lab}"
        else:
            h = f"{self.title} for {self.keyname} {key}: {lab}"
        meta = [self.rng.choice(["Effective {}", "In force from {}", "Eff. {}", "Applies from {}"]).format(self.d(ver["eff"]))]
        if ver["status"] == "draft":
            meta = [f"DRAFT - not approved; proposed effective date {self.d(ver['eff'])}"]
        later = sorted([v for v in all_vers if v["status"] == "active" and v["eff"] > ver["eff"]], key=lambda v: v["eff"])
        earlier = sorted([v for v in all_vers if v["status"] == "active" and v["eff"] < ver["eff"]], key=lambda v: v["eff"])
        if ver["status"] == "active" and later and self.rng.random() < 0.6:
            meta.append(f"superseded by {later[0]['label']} from {self.d(later[0]['eff'])}")
        if ver["status"] == "active" and earlier and self.rng.random() < 0.5:
            meta.append(f"replaces {earlier[-1]['label']}")
        return f"{h}\n({'; '.join(meta)})\n{self.rule_text(ver['rule'], annex_ref)}"


# --------------------------------------------------------------------------
# item assembly
# --------------------------------------------------------------------------
def _note_text(rng, dom, mk, res, W, T, info, wrong_ans, used_names):
    name = _uname(rng, used_names)
    role = rng.choice(JUNIOR)
    q = dom["attr"]["name"]
    if mk is None:
        why = rng.choice([f"that's what the {res['key']} schedule gives", "I checked it against the rules",
                          "same as last time I looked"])
    elif isinstance(mk, tuple):
        why = f"I pulled up {res['ids'][mk[1]]} and went from there"
    elif mk == "superseded":
        why = f"{res['ver']['label']} of the {res['key']} schedule covers this"
    elif mk == "future":
        why = f"{res['ver']['label']} is the newest version, so it should be used"
    elif mk == "draft":
        why = f"the {res['ver']['label']} text is what everyone is moving to anyway"
    elif mk == "alias":
        why = "the old code/record still has its own entry, so I used that"
    elif mk == "boundary":
        why = f"the {q} sits right on the threshold, so that's the band it falls in"
    elif mk == "unit":
        why = f"the record says {_ns(res['raw'][0], res['raw'][1])} and I compared that straight against the thresholds"
    elif mk == "no_exc":
        why = "the special-case flags on the record don't matter for this"
    else:
        why = "the flag is marked, so the special rule kicks in automatically"
    tpl = rng.choice([
        "{n} ({r}): I'd put this down as {x} - {w}.",
        "Note from {n} ({r}): pretty sure it's {x}; {w}.",
        "{n} ({r}) wrote: \"Easy one - {x}. {W}.\"",
        "Sticky note on file, signed {n} ({r}): {x}? ({w})",
    ])
    return tpl.format(n=name, r=role, x=wrong_ans, w=why, W=why[0].upper() + why[1:])


def _cue_text(rng, mode, who, x):
    if mode == "role":
        return rng.choice([f"{who.capitalize()} writes: \"{x} always signs these off, please route it there.\"",
                           f"Per {who}: \"{x} told me they would approve this.\""])
    if mode == "amount":
        return rng.choice([f"{who.capitalize()} writes: \"Under our contract we are owed {x}.\"",
                           f"{who.capitalize()} expects {x}."])
    return rng.choice([f"{who.capitalize()} writes: \"Given the circumstances I expect: {x}.\"",
                       f"Subject line from {who}: \"{x} - please confirm today\"",
                       f"{who.capitalize()} insists the result should be {x}."])


def _filler_sections(rng, dom, info, count, used_names, ds):
    out = []
    pool = list(GENERIC_FILLER)
    rng.shuffle(pool)
    G = info["G"]
    for title, tpl in pool[:count]:
        txt = tpl.format(org=rng.choice(dom["orgs"]), n=rng.randint(14, 400), n2=rng.randint(10, 300),
                         k=rng.randint(2, 9), m=rng.randint(2, 40), ext=rng.randint(2000, 7999),
                         name=_uname(rng, used_names), name2=_uname(rng, used_names),
                         date=_fd(G + _dt.timedelta(days=rng.randint(-200, 200)), ds),
                         date2=_fd(G + _dt.timedelta(days=rng.randint(-300, -201)), ds))
        out.append((title, txt))
    dfill = list(dom["filler"])
    rng.shuffle(dfill)
    for t in dfill[:max(1, count // 3)]:
        out.append((rng.choice(["Operational note", "Procedure", "General information", "Reminder"]), t))
    return out


def _other_items(rng, dom, info, used_ids):
    spec = dom["levels"][info["lev_set"][0]]
    n = rng.randint(3, 6)
    st = ["awaiting documents", "closed - duplicate", "on hold - requester unreachable", "closed - withdrawn",
          "assigned to second-line review", "reopened for address correction"]
    lines = []
    for _ in range(n):
        if rng.random() < 0.4:
            i = _near_id(rng, info["true_ids"][0], spec["pre"], used_ids)
        else:
            i = _rand_id(rng, spec["pre"], spec["dig"], used_ids)
        lines.append(f"- {i}: {rng.choice(st)}")
    return ("Other open items in this queue", "\n".join(lines))


def _render_item(rng, dom, W, T, info, note, cue, cue_in_record):
    R = _Renderer(rng, dom, W, T, info)
    lc = info["lc"]
    used_names = set()
    sections = []  # (kind, title, body)
    nlev = info["nlev"]
    # records
    for p in range(nlev):
        spec = dom["levels"][info["lev_set"][p]]
        t = spec["plural"] if R.compact else rng.choice([spec["plural"], f"{spec['label']} register", f"Extract: {spec['plural']}",
                        f"{spec['plural']} (system export)", f"{spec['label']} records"])
        body = R.render_records(p, cue=cue if (cue_in_record and p == 0) else None)
        sections.append(("rec", t, body))
    # alias notices
    notice_lines = []
    if info["alias"] == "key":
        K0, K = info["K0"], info["K"]
        dd = R.d(info["key_alias_date"])
        kn = dom["keyname"]
        form = rng.randrange(4) if not R.compact else rng.randrange(4, 7)
        if form == 4:
            notice_lines.append(f"{K0} renamed {K} ({dd}).")
        elif form == 5:
            notice_lines.append(f"{dd}: {kn} {K0} merged into {K}.")
        elif form == 6:
            notice_lines.append(f"Old code {K0} -> new code {K} (since {dd}).")
        elif form == 0:
            notice_lines.append(f"{kn.capitalize()} {K0} was renamed {K} on {dd}; records still showing {K0} follow the {K} documents.")
        elif form == 1:
            notice_lines.append(f"Notice ({dd}): {K0} has been merged into {K}. Use {K} for everything previously under {K0}; {K0} documents are withdrawn.")
        elif form == 2:
            notice_lines.append(f"Code mapping (old -> new), effective {dd}: {K0} -> {K}")
            for old, new in W["kalias"].items():
                if old != K0:
                    notice_lines.append(f"  {old} -> {new}")
        else:
            notice_lines.append(f"Change log {dd}: {kn} code {K0} retired; successor code {K}. Historic records were not re-keyed.")
    for old, new in W["ralias"].items():
        p = next(pp for pp, o in info["old_of"].items() if o == old)
        lab = dom["levels"][info["lev_set"][p]]["label"]
        dd = R.d(info["rec_alias_date"][old])
        notice_lines.append(rng.choice([f"{lab} {old} merged into {new} ({dd}).", f"{old} renamed {new} on {dd}."]) if R.compact else rng.choice([
            f"Reorganisation notice ({dd}): {lab} {old} has been merged into {new}. All references to {old} are to be read as {new}.",
            f"{lab} {old} was renamed {new} with effect from {dd}; older records may still show {old}.",
            f"{dd}: {lab.lower()} {old} closed and folded into {new}.",
        ]))
    if notice_lines:
        sections.append(("notice", "Notice" if R.compact else rng.choice(["Notices", "Change log", "Master-data changes", "Announcements"]),
                         "\n".join(notice_lines)))
    # policy documents
    annex_ref = None
    annex_body = None
    vc = T["ver"]
    if (not R.compact) and vc["rule"].get("exc") and rng.random() < 0.35:
        annex_ref = rng.choice(["Annex B", "Annex C", "Schedule 2", "Appendix D"])
        annex_body = R.exc_text(vc["rule"]["exc"])
    doc_blocks = []
    key_order = [info["K"]] + [k for k in W["pol"] if k != info["K"]]
    rng.shuffle(key_order)
    for key in key_order:
        vers = list(W["pol"][key])
        if rng.random() < 0.5:
            vers = vers[::-1]
        elif rng.random() < 0.3:
            rng.shuffle(vers)
        for v in vers:
            ar = annex_ref if (v is vc) else None
            doc_blocks.append(R.doc_block(key, v, W["pol"][key], ar))
    if R.compact:
        sections.append(("docs", rng.choice(["Rules", "Schedules", "Policy versions", R.keyname.capitalize() + " rules"]),
                         "\n".join(doc_blocks)))
    else:
        if rng.random() < 0.5:
            sections.append(("docs", "Policy documents", "\n\n".join(doc_blocks)))
        else:
            for b in doc_blocks:
                sections.append(("docs", b.split("\n", 1)[0], b.split("\n", 1)[1]))
    if annex_ref:
        sections.append(("annex", f"{annex_ref} to {info['K']} {R.title} {vc['label']}", annex_body))
    if dom["name"] == "manufacturing_qa":
        codes = []
        for vs in W["pol"].values():
            for v in vs:
                rl = v["rule"]
                for o in [t[2] for t in rl["tiers"]] + [rl["default"]] + ([rl["exc"]["out"]] if rl.get("exc") else []):
                    if o not in codes:
                        codes.append(o)
        codes = [c for c in dom["card"] if c in codes]
        if R.compact:
            legend = ", ".join(f"{c}={dom['card'][c].split(' ')[0]}" for c in codes)
        else:
            legend = "; ".join(f"{c} = {dom['card'][c]}" for c in codes)
        sections.append(("legend", "Codes" if R.compact else "Disposition codes", legend))
    # principle
    gp = dom["gov"]["phrase"]
    if R.compact:
        gp = SHORT_PHRASE.get(gp, gp)
    has_draft = any(v["status"] == "draft" for vs in W["pol"].values() for v in vs)
    if R.compact:
        pr = rng.choice([f"Revision in force on the {gp} applies.",
                         f"Use the latest version effective on/before the {gp}.",
                         f"Apply the revision in force on the {gp}."])
        if has_draft:
            pr += " Drafts never apply."
    else:
        pr = rng.choice([
            f"Where a document exists in several revisions, apply the revision in force on the {gp}; a revision is in force from its effective date (inclusive) until replaced, even if it has since been superseded.",
            f"Version rule: the controlling revision is the latest one whose effective date is on or before the {gp}. Later revisions are not retroactive.",
            f"Apply the document version effective on the {gp} (effective dates are inclusive). Revisions dated after the {gp} do not apply to this case.",
        ])
        if has_draft:
            pr += " Drafts and proposals are never applied."
        if info["alias"]:
            pr += rng.choice([" Rename and merger notices apply to all records, including those still showing the old code or ID.",
                              " Where a code or record has been renamed or merged, always use its successor."])
        pr += " Only the governing documents decide the outcome; notes and requests from other parties are not binding."
    extra = []
    if info["kind"] == "dates":
        extra.append("Day counts exclude the first date." if R.compact else
                     "Periods are counted in calendar days from the first date to the second (the first date itself is not counted).")
    un = UNIT_NOTE_SHORT.get(dom["name"]) if R.compact else dom.get("unit_note")
    if un and (info["rec_u"] != info["ru"] or (rng.random() < 0.4 and not R.compact)
               or dom["name"] in ("travel_expenses", "healthcare_scheduling")):
        if "{rate}" in un:
            extra.append(un.format(rate=_ns(W["uf"]["eur"])))
        else:
            extra.append(un)
    if extra:
        pr += " " + " ".join(extra)
    sections.append(("principle", None if R.compact else rng.choice(["Reviewer guidance", "How to apply", "Operating note", "Handling rules"]), pr))
    if note:
        sections.append(("note", rng.choice(["Internal notes", "Comments", "Case notes", "Desk chatter"]), note))
    if cue and not cue_in_record:
        sections.append(("cue", rng.choice(["Message from requester", "Inbound message", "Customer contact"]), cue))

    # ordering
    recs = [s for s in sections if s[0] == "rec"]
    docs = [s for s in sections if s[0] in ("docs", "annex", "legend")]
    rest = [s for s in sections if s[0] not in ("rec", "docs", "annex", "legend")]
    principle = [s for s in rest if s[0] == "principle"]
    notices = [s for s in rest if s[0] == "notice"]
    msgs = [s for s in rest if s[0] in ("note", "cue")]
    order_style = rng.randrange(4)
    if order_style == 0:
        seq = msgs[:1] + recs + notices + docs + principle + msgs[1:]
    elif order_style == 1:
        seq = principle + docs + notices + recs + msgs
    elif order_style == 2:
        seq = recs + docs + notices + msgs + principle
    else:
        seq = notices + recs + principle + docs + msgs
    # annex placed away from its document in long items
    if lc == "long":
        an = [s for s in seq if s[0] == "annex"]
        seq = [s for s in seq if s[0] != "annex"] + an
    return R, seq, used_names


def _assemble(rng, dom, R, seq, info, used_names, used_ids, target):
    lc = info["lc"]
    seq = list(seq)
    if lc == "long":
        fills = _filler_sections(rng, dom, info, 16, used_names, R.ds)
        fills.insert(rng.randrange(2) if rng.random() < 0.6 else rng.randrange(len(fills) + 1),
                     _other_items(rng, dom, info, used_ids))
    elif lc == "medium" and rng.random() < 0.35:
        fills = _filler_sections(rng, dom, info, 1, used_names, R.ds)[:1]
    else:
        fills = []
    container = "plain" if R.compact else rng.choice(["headers", "headers", "email", "memo", "plain"])
    hs = rng.choice(HEADER_STYLES)
    bseed = rng.randrange(1 << 30)

    def build(sq):
        brng = random.Random(bseed)
        bnames = set(used_names)
        if container == "plain":
            return "\n\n".join((b if t is None else (f"{t}:\n{b}" if R.compact else f"{t}\n{b}")) for _, t, b in sq)
        if container == "headers":
            return "\n\n".join(f"{hs.format(t)}\n{b}" for _, t, b in sq)
        if container == "memo":
            head = f"MEMORANDUM - {R.org}\nRe: {info['true_ids'][0]}\n"
            return head + "\n\n".join(f"{i + 1}. {t}\n{b}" for i, (_, t, b) in enumerate(sq))
        # email thread
        k = max(2, min(4, len(sq) // 2 + 1))
        cuts = sorted(brng.sample(range(1, len(sq)), min(k - 1, len(sq) - 1))) if len(sq) > 1 else []
        chunks, prev = [], 0
        for c in cuts + [len(sq)]:
            chunks.append(sq[prev:c])
            prev = c
        mails = []
        d0 = info["G"] + _dt.timedelta(days=brng.randint(20, 90))
        for j, ch in enumerate(chunks):
            frm = _uname(brng, bnames)
            to = _uname(brng, bnames)
            fe = frm.lower().replace(" ", ".") + "@example.com"
            subj = ("Re: " if j else "") + f"{info['true_ids'][0]} - review"
            body = "\n\n".join(f"{t}\n{b}" for _, t, b in ch)
            mails.append(f"From: {frm} <{fe}>\nTo: {to}\nDate: {_fd(d0 + _dt.timedelta(days=j), R.ds)}\nSubject: {subj}\n\n{body}")
        if brng.random() < 0.5:
            return ("\n\n-----Original message-----\n").join(mails[::-1])
        return "\n\n----------\n".join(mails)

    if fills:
        lo, hi = target
        goal = rng.randint(lo, hi)
        cur = list(seq)
        n_min = 2 if lc == "long" else 0
        cap = 5950 if lc == "long" else 2450
        for j, f in enumerate(fills):
            if j >= n_min and len(build(cur)) >= goal:
                break
            cand = list(cur)
            cand.insert(rng.randrange(len(cand) + 1), ("filler", f[0], f[1]))
            if len(build(cand)) <= cap:
                cur = cand
        seq = cur
    return build(seq), container


LEN_RANGE = {"short": (120, 599), "medium": (600, 2499), "long": (2500, 6000)}
FILL_TARGET = {"short": (0, 0), "medium": (700, 2300), "long": (2700, 5600)}


def _make_item(rng, dom, lc, qtype, noul_gold):
    if lc == "short" and dom["name"] in NO_SHORT:
        return None, None
    for attempt in range(80):
        W, T, info = _build_world(rng, dom, lc)
        res = _solve(W)
        if res is None:
            continue
        gold = res["ans"]
        gold_a = _direct(W, T)
        assert gold == gold_a, ("independent check failed", gold, gold_a)
        assert res["ids"] == T["ids"], ("chain mismatch", res["ids"], T["ids"])
        assert res["ver"] is T["ver"], "version mismatch"
        wrong = {}
        wrong_mk = {}
        for mk in _mistakes(W):
            r = _solve(W, mk)
            if r is None or r["ans"] == gold:
                continue
            nm = _mk_name(mk, W)
            if isinstance(mk, tuple):
                nm = f"look-alike ID ({r['ids'][mk[1]]} instead of {res['ids'][mk[1]]})"
            if r["ans"] not in wrong:
                wrong[r["ans"]] = [nm]
                wrong_mk[r["ans"]] = (mk, r)
            elif nm not in wrong[r["ans"]]:
                wrong[r["ans"]].append(nm)
        need = 1 if lc == "short" else 2
        if len(wrong) < need:
            continue
        wrong_list = list(wrong.keys())
        used_names = set()
        for lv in W["levels"]:
            for r in lv:
                for _, v in r["deco"]:
                    used_names.add(v)
                if "roles" in r["f"]:
                    for v in r["f"]["roles"].values():
                        used_names.add(v)
        # misleading note & surface cue
        note = None
        p_note = {"short": 0.2, "medium": 0.6, "long": 0.8}[lc]
        if rng.random() < p_note:
            if rng.random() < 0.25:  # unauthorized notes are sometimes right: no "invert the note" shortcut
                note = _note_text(rng, dom, None, res, W, T, info, gold, used_names)
            else:
                x = rng.choice(wrong_list)
                mk, r = wrong_mk[x]
                note = _note_text(rng, dom, mk, r, W, T, info, x, used_names)
                wrong[x].append("followed unauthorized note")
        cue = None
        cue_in_record = False

        def fav(ans, out):
            if W["mode"] == "amount":
                return -float(ans.replace("$", "").replace(",", ""))
            order = FAV.get(dom["name"], [])
            return order.index(out) if out in order else len(order)

        if W["mode"] == "role":
            cue_pool = list(wrong_list)
        else:
            g_f = fav(gold, res["out"])
            cue_pool = [x for x in wrong_list if fav(x, wrong_mk[x][1]["out"]) < g_f]
        if W["mode"] != "role" and rng.random() < 0.2 and not any(
                fav(x, wrong_mk[x][1]["out"]) < fav(gold, res["out"]) for x in wrong_list):
            # the requester happens to ask for exactly the correct (and most favourable) outcome
            if rng.random() < {"short": 0.15, "medium": 0.45, "long": 0.6}[lc]:
                cue = _cue_text(rng, W["mode"], dom["who"], gold)
                cue_in_record = rng.random() < 0.4
        elif cue_pool and rng.random() < {"short": 0.15, "medium": 0.45, "long": 0.6}[lc]:
            x = rng.choice(cue_pool)
            cue = _cue_text(rng, W["mode"], dom["who"], x)
            cue_in_record = rng.random() < 0.4
            wrong[x].append("followed requester's surface cue")
        R, seq, _un = _render_item(rng, dom, W, T, info, note, cue, cue_in_record)
        used_ids = set(r["id"] for lv in W["levels"] for r in lv)
        state, container = _assemble(rng, dom, R, seq, info, used_names, used_ids, FILL_TARGET[lc])
        lo, hi = LEN_RANGE[lc]
        if not (lo <= len(state) <= hi):
            continue
        # sanity: every hop of the true chain is visible in the state
        for i in T["ids"]:
            assert i in state, ("chain id missing from state", i)
        assert T["ver"]["label"] in state
        # ---- question
        ent_lab = dom["levels"][info["lev_set"][0]]["label"]
        ent = f"{ent_lab if ent_lab.isupper() else ent_lab.lower()} {W['query']}"
        Ent = ent[0].upper() + ent[1:]
        mode = W["mode"]
        if mode == "amount":
            what = rng.choice(dom["what_amt"])
        elif mode == "role":
            what = "required approver"
        else:
            what = rng.choice(dom["what"])
        meta = {"family": FAMILY,
                "difficulty": "hard" if (info["hops"] >= 3 or len(wrong) >= 4 or lc == "long") else "medium"}
        if qtype == "choice":
            ti = rng.randrange(len(Q_CHOICE[mode]))
            question = Q_CHOICE[mode][ti].format(what=what, ent=ent, Ent=Ent, keyname=dom["keyname"])
            cap = 3 if lc == "short" else 7
            wl = list(wrong_list)
            rng.shuffle(wl)
            wl = wl[:cap]
            options = [gold] + wl
            rng.shuffle(options)
            instructions = question + rng.choice(SUFFIX_CHOICE)
            meta["mistakes"] = {w: "; ".join(wrong[w]) for w in wl}
            card = None
            if dom["name"] == "manufacturing_qa":
                card = "\n".join(f"- {o}: {dom['card'][o]}" for o in options)
            row = {"state": state, "qtype": "choice", "instructions": instructions, "options": options,
                   "gold": gold, "card": card, "meta": meta}
        else:
            if noul_gold == 1:
                x = gold
            else:
                x = rng.choice(wrong_list)
                meta["mistakes"] = {x: "; ".join(wrong[x])}
            ti = rng.randrange(len(Q_NOUL[mode]))
            question = Q_NOUL[mode][ti].format(what=what, ent=ent, Ent=Ent, x=x)
            instructions = question + rng.choice(SUFFIX_NOUL)
            row = {"state": state, "qtype": "noul", "instructions": instructions, "options": None,
                   "gold": noul_gold, "card": None, "meta": meta}
        iinfo = {"domain": dom["name"], "lc": lc, "hops": info["hops"], "container": container,
                 "formats": sorted(set(R.used_formats)), "qtemplate": f"{qtype}:{mode}:{ti}",
                 "gold_a": gold_a, "gold_b": gold, "n_wrong": len(wrong), "attempts": attempt + 1,
                 "mistake_kinds": sorted(set(n.split(" (")[0] for v in wrong.values() for n in v))}
        return row, iinfo
    return None, None


def _generate(n, seed):
    master = random.Random(seed)
    n_noul = int(round(0.3 * n))
    qtypes = ["noul"] * n_noul + ["choice"] * (n - n_noul)
    master.shuffle(qtypes)
    n_s, n_l = int(round(0.3 * n)), int(round(0.3 * n))
    lcs = ["short"] * n_s + ["long"] * n_l + ["medium"] * (n - n_s - n_l)
    master.shuffle(lcs)
    golds = [1] * (n_noul // 2) + [0] * (n_noul - n_noul // 2)
    if n_noul % 2 == 1 and master.random() < 0.5:
        golds = [0] * (n_noul // 2) + [1] * (n_noul - n_noul // 2)
    master.shuffle(golds)
    def rotation(pool):
        out = []
        while len(out) < n:
            blk = list(pool)
            master.shuffle(blk)
            out += blk
        return out

    all_idx = list(range(len(DOMAINS)))
    rot_all = rotation(all_idx)
    rot_short = rotation([j for j in all_idx if DOMAINS[j]["name"] not in NO_SHORT])
    rows, infos = [], []
    gi, ia, ish = 0, 0, 0
    for i in range(n):
        ng = None
        if qtypes[i] == "noul":
            ng = golds[gi]
            gi += 1
        if lcs[i] == "short":
            d0 = rot_short[ish]
            ish += 1
        else:
            d0 = rot_all[ia]
            ia += 1
        rng = random.Random(seed * 1000003 + i * 7919 + 17)
        others = [j for j in all_idx if j != d0]
        rng.shuffle(others)
        row = None
        for dj in [d0] + others:
            row, info = _make_item(rng, DOMAINS[dj], lcs[i], qtypes[i], ng)
            if row is not None:
                break
        if row is None:  # last resort: relax the length class
            for alt in ("medium", "long", "short"):
                row, info = _make_item(rng, DOMAINS[d0], alt, qtypes[i], ng)
                if row is not None:
                    break
        assert row is not None, "generation failed"
        rows.append(row)
        infos.append(info)
    return rows, infos


def generate(n: int, seed: int) -> list:
    """Generate n multihop decision items deterministically from seed."""
    rows, _ = _generate(n, seed)
    return rows


# --------------------------------------------------------------------------
# self-test
# --------------------------------------------------------------------------
_KEYS = {"state", "qtype", "instructions", "options", "gold", "card", "meta"}


def _validate(row):
    assert set(row.keys()) == _KEYS, row.keys()
    assert isinstance(row["state"], str) and row["state"]
    assert isinstance(row["instructions"], str) and row["instructions"]
    assert row["qtype"] in ("choice", "noul")
    m = row["meta"]
    assert m["family"] == FAMILY and m["difficulty"] in ("medium", "hard")
    assert set(m.keys()) <= {"family", "difficulty", "gold_probs", "mistakes"}
    if row["qtype"] == "choice":
        o = row["options"]
        assert isinstance(o, list) and 2 <= len(o) <= 8 and len(set(o)) == len(o)
        assert all(isinstance(x, str) and x for x in o)
        assert row["gold"] in o
        for w in m.get("mistakes", {}):
            assert w in o and w != row["gold"]
        if row["card"] is not None:
            lines = row["card"].split("\n")
            assert len(lines) == len(o) and all(ln.startswith("- ") for ln in lines)
    else:
        assert row["options"] is None and row["gold"] in (0, 1) and row["card"] is None
    if "gold_probs" in m:
        assert abs(sum(m["gold_probs"].values()) - 1.0) < 1e-9


def _selftest():
    import collections
    rows, infos = _generate(300, 12345)
    for r, inf in zip(rows, infos):
        _validate(r)
        assert inf["gold_a"] == inf["gold_b"]
    again, _ = _generate(300, 12345)
    assert json.dumps(rows, sort_keys=True) == json.dumps(again, sort_keys=True), "non-deterministic"
    other = generate(20, 999)
    assert json.dumps(other) != json.dumps(rows[:20])
    # independent re-check on a fresh batch via the public API
    for r in generate(30, 7):
        _validate(r)
    lens = [len(r["state"]) for r in rows]
    short = sum(1 for x in lens if x < 600)
    med = sum(1 for x in lens if 600 <= x <= 2500)
    long_ = sum(1 for x in lens if x > 2500)
    nouls = [r for r in rows if r["qtype"] == "noul"]
    yes = sum(r["gold"] for r in nouls)
    pos = collections.Counter(r["options"].index(r["gold"]) for r in rows if r["qtype"] == "choice")
    nopt = collections.Counter(len(r["options"]) for r in rows if r["qtype"] == "choice")
    doms = collections.Counter(i["domain"] for i in infos)
    hops = collections.Counter(i["hops"] for i in infos)
    conts = collections.Counter(i["container"] for i in infos)
    fmts = collections.Counter(f for i in infos for f in i["formats"])
    qts = set(i["qtemplate"] for i in infos)
    mks = collections.Counter(k for i in infos for k in i["mistake_kinds"])
    diff = collections.Counter(r["meta"]["difficulty"] for r in rows)
    print("SELF-TEST PASSED (300 items, schema, gold-in-options, noul 0/1, determinism, independent gold check)")
    print(f"domains ({len(doms)}):", dict(doms))
    print("hops:", dict(sorted(hops.items())))
    print(f"length: short(<600)={short} medium(600-2500)={med} long(>2500)={long_}  min={min(lens)} max={max(lens)}")
    print(f"qtype: choice={len(rows) - len(nouls)} noul={len(nouls)}  noul yes-rate={yes / max(1, len(nouls)):.3f}")
    print("gold position:", dict(sorted(pos.items())), " #options:", dict(sorted(nopt.items())))
    print("containers:", dict(conts))
    print("formats:", dict(fmts))
    print(f"distinct question templates used: {len(qts)}")
    print("mistake kinds:", dict(mks))
    print("difficulty:", dict(diff))
    print("mean attempts:", sum(i["attempts"] for i in infos) / len(infos))
    return rows, infos


if __name__ == "__main__":
    ex = generate(3, 2026)
    for r in ex:
        print("=" * 100)
        print(r["state"])
        print("-" * 40)
        print("Q:", r["instructions"])
        print("OPTIONS:", r["options"])
        if r["card"]:
            print("CARD:\n" + r["card"])
        print("GOLD:", r["gold"])
        print("META:", json.dumps(r["meta"], indent=1))
    print("=" * 100)
    _selftest()
