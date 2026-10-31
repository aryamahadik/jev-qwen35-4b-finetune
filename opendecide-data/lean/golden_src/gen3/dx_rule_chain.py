"""dx_rule_chain: reviewer R's devx renderer + parse-back for F1a `gen3_rule_chain` (yn2b/SPEC.md sections 5 F1, 6).

Latents: gen3_rule_chain.devx_latents(n) (dev_holdout distribution: the held-out school-transport family and contract
style, devx seed stream and name pool), as written to yn2b/f1_devx_latents.json. Labels: rc_core.decide / rc_core.pivotal
only. Everything a reader sees (document titles, clause sentences, the general reading rules, fact names, category and
outcome names, case-file layouts, questions, options, cards) was written for devx from rc_core's semantics (evaluate,
figures, deadline, pivotal) and the latent schema, not from the training renderers or skins. The only skin field read
is the time rule's direction (after / before the event), a semantic parameter.

Views (one row per latent): yes/no "is X the outcome" with an inverse wording for balance, JB-letter, choice "which
outcome" (5 options), choice "which clause decides" (the latent's candidate clauses).
Formats: code (numbered parts + a case form), memo (paragraph clauses + a case letter), json (canonical).
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import date, timedelta
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import mv_core as mv  # noqa: E402
import dx_common as dx  # noqa: E402
import rc_core  # noqa: E402  (the shared decide() and pivotal(); never its skins' wording)

KEY = "gen3_rule_chain"
FMTS = ("code", "memo", "json")
FMT_META = {"code": "markdown", "memo": "prose", "json": "json"}
N_EXPORT = 160
CODES = ("INELIG", "LATE", "DOCS", "EXCL", "PARTIAL", "FULL")

# ------------------------------------------------------------------------------------------------ skins (devx words)
S = {
    "shipping_tariff": dict(
        doc="freight claim rules", benefit="compensation", person="shipper", refuse="claim declined",
        elig=("the consignment's weight", "kg"), amount=("compensation claimed", "$"),
        event="the delivery date", catlabel="consignment type",
        cats={"envelope": "envelope", "parcel": "parcel", "pallet": "pallet", "chilled": "chilled box"},
        types={"damaged consignment": "damage claim", "lost consignment": "loss claim"},
        doc_main="the delivery note signed by the recipient",
        docs2={"a police report": "a theft report from the police"},
        flags={"noted": "the damage was written on the delivery receipt", "cover": "the shipper bought extra cover",
               "latedel": "the consignment was delivered late", "credithold": "the shipper's account is on credit hold",
               "reused": "the packaging was reused", "nolabel": "the consignment carried no address label"},
        terms=(("Recipient", "the person who signs for the consignment"),
               ("Consignment", "everything sent under one waybill"),
               ("Waybill", "the transport document issued at collection")),
        procs=("Claims may be sent by post or through the online form.", "The claims desk acknowledges each claim "
               "within two working days.", "Photographs of the damage may be attached to a claim.")),
    "school_transport": dict(
        doc="home-to-school travel scheme", benefit="travel allowance", person="family", refuse="no travel allowance",
        elig=("the distance from home to school", "miles"), amount=("allowance requested", "$"),
        event="the date the school place was offered", catlabel="pupil group",
        cats={"plan": "pupil with a support plan", "primary": "primary pupil", "secondary": "secondary pupil",
              "sixth": "sixth-form student"},
        types={"school journey": "school travel", "college journey": "college travel"},
        doc_main="a document proving the home address",
        docs2={"a college timetable": "the college's published timetable"},
        flags={"unsafe": "the walking route is rated unsafe", "lowincome": "the family receives a low-income benefit",
               "moved": "the family moved house during the school year",
               "othergrant": "the family already receives another travel grant",
               "preference": "the school was chosen over a nearer school by parental preference",
               "private": "the school is a private school"},
        terms=(("Home address", "the address where the pupil lives during term"),
               ("Nearest school", "the closest school with a place for the pupil"),
               ("Term", "one of the three school terms of the year")),
        procs=("Applications are made online through the family portal.", "Bus passes are posted to the home "
               "address.", "Families are told of the decision by email.")),
    "hoa_bylaws": dict(
        doc="architectural review bylaws", benefit="fence approval", person="owner", refuse="fence not approved",
        elig=("the number of days the owner's dues are overdue", "days"), amount=("fence height requested", "inches"),
        event="the planned start of the work", catlabel="lot type",
        cats={"cottage": "cottage lot", "detached": "detached-house lot", "townhouse": "townhouse lot",
              "corner": "corner lot"},
        types={"new fence": "fence project", "garden shed": "shed project"},
        doc_main="a site drawing",
        docs2={"a builder's licence number": "the builder's licence details"},
        flags={"consent": "both neighbours gave written consent", "replace": "the fence replaces an existing fence",
               "pool": "the yard has a swimming pool", "violation": "the owner has an open bylaw violation",
               "setback": "the fence sits inside the street setback",
               "easement": "the fence crosses a utility easement"},
        terms=(("Lot", "a parcel of land shown on the community plat"), ("Owner", "the person on the deed"),
               ("Committee", "the architectural review committee")),
        procs=("The committee meets on the first Tuesday of each month.", "Requests are posted on the community "
               "notice board.", "Owners may attend the meeting where their request is reviewed.")),
    "warranty_returns": dict(
        doc="warranty and returns terms", benefit="refund", person="buyer", refuse="no refund",
        elig=("the age of the item", "days"), amount=("refund claimed", "$"),
        event="the date the fault appeared", catlabel="product group",
        cats={"electronics": "electronics", "appliance": "home appliance", "furniture": "furniture",
              "garden": "garden equipment"},
        types={"faulty item": "fault return", "unwanted item": "change-of-mind return"},
        doc_main="a receipt or other proof of purchase",
        docs2={"the unused item in its box": "the item unused in its original box"},
        flags={"phone": "the fault was first reported by phone", "loyalty": "the buyer is a loyalty member",
               "recall": "the model is under a safety recall", "resale": "the item was bought for resale",
               "misuse": "the damage came from misuse", "clearance": "the item was sold as clearance stock"},
        terms=(("Item", "the product named on the receipt"), ("Store", "any branch of the seller"),
               ("Fault", "a defect in materials or making")),
        procs=("Returns can be made at any store.", "Refunds go back to the original payment card.",
               "Collection of large items can be booked online.")),
    "leave_handbook": dict(
        doc="staff leave handbook", benefit="paid special leave", person="employee", refuse="leave not granted",
        elig=("the employee's length of service", "months"), amount=("paid days requested", "days"),
        event="the first day of the leave", catlabel="contract type",
        cats={"fulltime": "full-time contract", "parttime": "part-time contract", "apprentice": "apprenticeship",
              "fixedterm": "fixed-term contract"},
        types={"short absence": "short leave", "study absence": "study leave"},
        doc_main="the leave form signed by the line manager",
        docs2={"a letter from the college": "a letter from the course provider"},
        flags={"hospital": "the absence is for a hospital stay", "bereave": "the absence follows a bereavement",
               "rep": "the employee is a staff representative", "probation": "the employee is on probation",
               "shutdown": "the dates fall in the annual shutdown",
               "double": "the dates overlap leave already granted"},
        terms=(("Line manager", "the person the employee reports to"), ("Leave year", "1 January to 31 December"),
               ("Working day", "a day the employee is rostered to work")),
        procs=("Leave forms are kept by the people team.", "Managers reply to leave requests within a week.",
               "Payroll is told of paid leave at month end.")),
    "pharmacy_formulary": dict(
        doc="drug coverage rules", benefit="coverage", person="member", refuse="fill not covered",
        elig=("the member's time in the plan", "months"), amount=("cost of the fill", "$"),
        event="the date of the prescription", catlabel="drug tier",
        cats={"generic": "generic drug", "preferred": "preferred brand", "nonpreferred": "non-preferred brand",
              "specialty": "specialty drug"},
        types={"pharmacy counter fill": "in-store fill", "home delivery fill": "posted fill"},
        doc_main="a statement from the prescriber",
        docs2={"a signed delivery address form": "a signed form with the delivery address"},
        flags={"plist": "the drug is on the prior-approval list", "generic_tried": "a generic was tried first",
               "mail": "the fill is sent by post", "early": "the refill is asked for early",
               "cosmetic": "the drug is for a cosmetic use", "vacation": "the fill is a holiday supply"},
        terms=(("Fill", "one supply of a prescribed drug"), ("Prescriber", "the clinician who wrote the "
               "prescription"), ("Plan", "the drug benefit the member is enrolled in")),
        procs=("Members can track fills in the plan's app.", "Pharmacies send claims electronically.",
               "Questions about coverage go to the member helpline.")),
    "municipal_fee": dict(
        doc="event fee waiver rules", benefit="fee waiver", person="organiser", refuse="no fee waiver",
        elig=("the expected attendance", "people"), amount=("fee to be waived", "$"),
        event="the event date", catlabel="organiser type",
        cats={"nonprofit": "non-profit body", "resident": "residents' group", "school": "school",
              "commercial": "commercial organiser"},
        types={"community event permit": "street event", "market stall licence": "market stall"},
        doc_main="the organiser's registration certificate",
        docs2={"a site plan of the stall": "a drawing of the stall layout"},
        flags={"free": "the event is free to attend", "charity": "the organiser is a registered charity",
               "hardship": "the organiser shows financial hardship", "repeat": "the organiser had a waiver last year",
               "alcohol": "alcohol will be sold", "loud": "amplified music is planned after 10 pm"},
        terms=(("Organiser", "the body named on the application"), ("Event", "the gathering described in the "
               "application"), ("Fee", "the permit charge in the council's price list")),
        procs=("Applications are checked by the events team.", "Road closures are arranged separately.",
               "Organisers receive the permit by email.")),
    "grant_eligibility": dict(
        doc="community grant rules", benefit="grant", person="applicant", refuse="no grant",
        elig=("the time since the organisation was registered", "years"), amount=("grant requested", "$"),
        event="the project start date", catlabel="project area",
        cats={"sport": "sport", "arts": "arts", "heritage": "heritage", "environment": "environment"},
        types={"project grant": "project funding", "equipment grant": "equipment funding"},
        doc_main="the most recent annual accounts",
        docs2={"three supplier quotes": "quotes from three suppliers"},
        flags={"volunteers": "the project is run by volunteers", "rural": "the project is in a rural area",
               "match": "the applicant provides matched funding", "lastyear": "the applicant had a grant last year",
               "fundraising": "the money is for fundraising events",
               "political": "the project has a political purpose"},
        terms=(("Applicant", "the organisation that signs the application"), ("Project", "the activity the grant "
               "pays for"), ("Panel", "the grants panel")),
        procs=("The panel meets four times a year.", "Grants are paid in two instalments.",
               "Applicants send a short report when the project ends.")),
    "data_retention": dict(
        doc="records retention procedure", benefit="retention extension", person="records owner",
        refuse="no extension", elig=("the age of the records", "years"), amount=("extension requested", "months"),
        event="the scheduled deletion date", catlabel="record class",
        cats={"hr": "personnel records", "finance": "finance records", "customer": "customer records",
              "email": "email archive"},
        types={"retention extension": "keep-longer request", "early deletion request": "delete-early request"},
        doc_main="written sign-off from the data officer",
        docs2={"a deletion certificate": "a certificate of deletion"},
        flags={"audit": "the records are under audit", "litigation": "the records are under a litigation hold",
               "archived": "the records are already archived offline",
               "breach": "the records were part of a data breach",
               "special": "the records hold special-category data",
               "dupes": "the records duplicate records already kept"},
        terms=(("Records owner", "the manager responsible for a record set"), ("Record set", "records kept "
               "together under one reference"), ("Data officer", "the person who oversees data protection")),
        procs=("Requests are logged in the records register.", "Deletion runs take place each night.",
               "The register is reviewed every quarter.")),
    "it_change": dict(
        doc="change management policy", benefit="change approval", person="change owner", refuse="change rejected",
        elig=("the number of users affected", "users"), amount=("downtime requested", "minutes"),
        event="the planned change date", catlabel="system tier",
        cats={"tier1": "tier-1 system", "tier2": "tier-2 system", "tier3": "tier-3 system",
              "desktop": "desktop fleet"},
        types={"planned change": "scheduled change", "emergency change": "urgent change"},
        doc_main="a plan for rolling the change back",
        docs2={"an incident number": "the incident reference"},
        flags={"security": "the change fixes a security flaw", "chair": "the change board chair approved it",
               "testonly": "the change touches test systems only", "failed": "the last attempt at this change failed",
               "freeze": "the change falls in a change freeze", "vendor": "the change is made by an outside vendor"},
        terms=(("Change owner", "the person accountable for the change"), ("Downtime", "time when users cannot "
               "use the system"), ("Change board", "the group that reviews changes")),
        procs=("Changes are recorded in the service desk tool.", "The change board meets every Thursday.",
               "Users are told of downtime by email."))}
GROUND = {"INELIG": "{e} test not met", "LATE": "received after the deadline", "DOCS": "{d} not included",
          "EXCL": "an exclusion applies"}
OP_W = {"ge": "at least", "gt": "more than", "le": "at most", "lt": "less than"}
OP_R = {v: k for k, v in OP_W.items()}
ELIG_SHORT = {"shipping_tariff": "weight", "school_transport": "distance", "hoa_bylaws": "overdue-dues",
              "warranty_returns": "item-age", "leave_handbook": "length-of-service", "pharmacy_formulary": "membership",
              "municipal_fee": "attendance", "grant_eligibility": "registration", "data_retention": "record-age",
              "it_change": "user-count"}
DOC_SHORT = {"shipping_tariff": "signed delivery note", "school_transport": "proof of address",
             "hoa_bylaws": "site drawing", "warranty_returns": "proof of purchase", "leave_handbook": "signed leave form",
             "pharmacy_formulary": "prescriber statement", "municipal_fee": "registration certificate",
             "grant_eligibility": "annual accounts", "data_retention": "data officer sign-off",
             "it_change": "rollback plan"}
PAID = {"shipping_tariff": "paid", "school_transport": "paid", "hoa_bylaws": "approved", "warranty_returns": "paid",
        "leave_handbook": "granted", "pharmacy_formulary": "covered", "municipal_fee": "waived",
        "grant_eligibility": "awarded", "data_retention": "granted", "it_change": "approved"}


def outcome_text(skin: str, code: str) -> str:
    s = S[skin]
    if code in GROUND:
        return f"{s['refuse']} ({GROUND[code].format(e=ELIG_SHORT[skin], d=DOC_SHORT[skin])})"
    if code == "PARTIAL":
        return f"{s['benefit']} {PAID[skin]}, reduced to the limit"
    return f"{s['benefit']} {PAID[skin]} for the full amount requested"


def code_of_outcome(skin: str, text: str) -> str:
    for c in CODES:
        if outcome_text(skin, c) == text:
            return c
    raise ValueError(f"outcome {text!r}")


# ------------------------------------------------------------------------------------------------ small text helpers
def ordn(n: int) -> str:
    if 10 <= n % 100 <= 20:
        return f"{n}th"
    return f"{n}" + {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def fig(x) -> str:
    return dx.num_text(Fraction(str(x)))


def qty(skin: str, x, which: str) -> str:
    """A figure with its unit: which = elig | amount."""
    unit = S[skin]["elig" if which == "elig" else "amount"][1]
    if unit == "$":
        return "$" + fig(x)
    return f"{fig(x)} {unit}"


def parse_qty(skin: str, s: str, which: str) -> Fraction:
    unit = S[skin]["elig" if which == "elig" else "amount"][1]
    s = s.strip()
    if unit == "$":
        if not s.startswith("$"):
            raise ValueError(s)
        return dx.parse_num(s[1:])
    if not s.endswith(" " + unit):
        raise ValueError(f"{s!r} lacks unit {unit}")
    return dx.parse_num(s[: -len(unit) - 1])


def fstr(x: Fraction) -> str:
    """The latent's figure string form (Fraction -> '420' / '39/10')."""
    return str(Fraction(x))


def dtext(iso: str, style: str) -> str:
    return iso if style == "iso" else dx.long_date(date.fromisoformat(iso))


def parse_d(s: str) -> str:
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return s
    return dx.parse_long_date(s).isoformat()


# ------------------------------------------------------------------------------------------------ conditions
def cond_phrase(skin: str, x: dict) -> str:
    s = S[skin]
    parts = []
    if x.get("cats"):
        names = [s["cats"][c] for c in x["cats"]]
        parts.append(f"the {s['catlabel']} is {dx.join_list(names, 'or')}")
    for a in x.get("conds", []):
        if a["t"] == "flag":
            parts.append(s["flags"][a["f"]])
        else:
            parts.append(f"the {s['amount'][0]} is {OP_W[a['op']]} {qty(skin, a['value'], 'amount')}")
    return dx.join_list(parts, "and") if len(parts) <= 2 else "; ".join(parts[:-1]) + "; and " + parts[-1]


def parse_cond_phrase(skin: str, text: str) -> tuple[list, list]:
    s = S[skin]
    if "; and " in text:
        head, last = text.rsplit("; and ", 1)
        items = head.split("; ") + [last]
    elif " and " in text:
        # two parts joined by ' and ' (flag phrases and category names never contain ' and ')
        items = text.split(" and ")
        if len(items) != 2:
            raise ValueError(f"ambiguous condition list {text!r}")
    else:
        items = [text]
    cats, conds = [], []
    inv_cat = {v: k for k, v in s["cats"].items()}
    inv_flag = {v: k for k, v in s["flags"].items()}
    for it in items:
        m = re.fullmatch(re.escape(f"the {s['catlabel']} is ") + r"(.+)", it)
        if m:
            cats = [inv_cat[n] for n in dx.split_list(m.group(1), "or")]
            continue
        if it in inv_flag:
            conds.append({"t": "flag", "f": inv_flag[it]})
            continue
        m = re.fullmatch(re.escape(f"the {s['amount'][0]} is ") + r"(at least|more than|at most|less than) (.+)", it)
        if m:
            conds.append({"t": "amt", "op": OP_R[m.group(1)], "value": fstr(parse_qty(skin, m.group(2), "amount"))})
            continue
        raise ValueError(f"condition part {it!r}")
    return cats, conds


# ------------------------------------------------------------------------------------------------ clauses
SEC_HEAD = {"general": "General provisions", "requirements": "Requirements", "exceptions": "Exceptions",
            "limits": "Limits", "exclusions": "Exclusions", "other": "Other provisions", "amendments": "Amendments"}


def time_dir(skin: str) -> str:
    return rc_core.SK.SKINS[skin]["time"]["dir"]   # the only skin field used: after / before the event


def clause_text(c: dict, doc: dict, num: dict, ds: str) -> str:
    skin = doc["skin"]
    s = S[skin]
    k = c["kind"]
    day = "business day" if doc["count"] == "business" else "day"
    if k == "i_days":
        if doc["count"] == "calendar":
            return ("All periods are counted in calendar days. The Nth day after a date is the date N days later; the "
                    "Nth day before a date is the date N days earlier.")
        hol = next((num[x["id"]] for x in doc["clauses"] if x["kind"] == "i_hol"), None)
        tail = f" listed in clause {hol}" if hol else ""
        return ("All periods are counted in business days: Monday to Friday, except the public holidays" + tail +
                ". The Nth business day after a date is found by counting business days forward from the day after "
                "it; the Nth business day before a date by counting back from the day before it.")
    if k == "i_hol":
        return "Public holidays: " + (", ".join(dtext(h, ds) for h in doc["holidays"]) or "none") + "."
    if k == "i_exc":
        return ("An exception applies only to the clause it names, and only when all of its conditions hold and no "
                "exception to that exception applies. A requirement that an exception treats as met is satisfied; an "
                "exclusion that an exception lifts does not apply.")
    if k == "i_amend":
        return ("An amendment replaces the figure it names for requests received on or after its effective date; "
                "earlier requests use the figure as first written. A withdrawn amendment has no effect.")
    if k == "i_order":
        return ("If more than one ground for refusal applies, the decision records the ground in the clause that comes "
                "first in this document.")
    if k == "i_missing":
        return ("A fact that the case file does not show is not established; a document not listed as included is "
                "missing.")
    if k == "i_prec":
        p = doc["prec"]
        if p == "specific":
            return (f"When both the general limit and {dx.article(s['catlabel'])} {s['catlabel']} limit apply to a "
                    f"request, the "
                    f"{s['catlabel']} limit prevails.")
        if p == "later":
            return ("When two limits apply to a request, the one in the clause placed later in this document "
                    "prevails (an amendment does not change where a clause is placed).")
        if p == "lower":
            return "When two limits apply to a request, the lower one applies."
        raise ValueError(p)
    if k == "defn":
        E = s["elig"][0][0].upper() + s["elig"][0][1:]
        return (f"{E} is a 'qualifying {ELIG_SHORT[skin]} figure' when it is {OP_W[c['op']]} "
                f"{qty(skin, c['value'], 'elig')}.")
    if k == "entitle":
        return (f"A request that meets every requirement and is not excluded receives the {s['benefit']}, within the "
                f"limits set out in this document.")
    if k == "req":
        g = c["gate"]
        if g == "elig":
            if c.get("via"):
                return f"{s['elig'][0][0].upper() + s['elig'][0][1:]} must be a qualifying {ELIG_SHORT[skin]} figure " \
                       f"(clause {num[c['via']]})."
            return f"{s['elig'][0][0].upper() + s['elig'][0][1:]} must be {OP_W[c['op']]} {qty(skin, c['value'], 'elig')}."
        if g == "time":
            w = "no later than" if c["incl"] else "before"
            return (f"The request must be received {w} the {ordn(c['n'])} {day} {time_dir(skin)} {s['event']}.")
        if g == "docs":
            if c.get("scope_type"):
                return (f"A request of the type '{s['types'][c['scope_type']]}' must also include "
                        f"{s['docs2'][c['docs2']]}.")
            return f"The request must include {s['doc_main']}."
    if k == "exc":
        T = num[c["target"]]
        tk = next(x for x in doc["clauses"] if x["id"] == c["target"])["kind"]
        cp = cond_phrase(skin, c)
        if c["mode"] == "period":
            return (f"Exception to clause {T}: when {cp}, the time limit in clause {T} counts {c['n2']} {day}s "
                    f"instead of the number stated there.")
        if tk == "excl":
            return f"Exception to clause {T}: clause {T} does not exclude the request when {cp}."
        return f"Exception to clause {T}: the requirement in clause {T} counts as met when {cp}."
    if k == "excexc":
        T = num[c["target"]]
        return f"Exception to clause {T}: clause {T} does not apply when {cond_phrase(skin, c)}."
    if k == "excl":
        return f"No {s['benefit']} is given when {cond_phrase(skin, c)}."
    if k == "lim_gen":
        return f"The {s['benefit']} is limited to {qty(skin, c['limit'], 'amount')}."
    if k == "lim_tab":
        rows = "; ".join(f"{s['cats'][cat]}: {qty(skin, v, 'amount')}" for cat, v in c["rows"])
        return f"Limits by {s['catlabel']}: {rows}."
    if k == "grant":
        return (f"The {s['benefit']} covers the {s['amount'][0]} up to the applicable limit; when the "
                f"{s['amount'][0]} is above the limit, it is cut to the limit.")
    if k == "prec_named":
        return (f"Where clause {num[c['a']]} and clause {num[c['b']]} both set a limit for a request, clause "
                f"{num[c['b']]} prevails; if clause {num[c['b']]} sets none for it, the lower limit applies.")
    if k == "udef":
        t, d = s["terms"][c["_i"] % len(s["terms"])]
        return f"'{t}' means {d}."
    if k == "proc":
        return s["procs"][c["_i"] % len(s["procs"])]
    if k == "amend":
        T = num[c["target"]]
        f = c["field"]
        if f == "limit":
            what, old, new = "the limit", qty(skin, c["old"], "amount"), qty(skin, c["new"], "amount")
        elif f.startswith("row:"):
            what = f"the limit for {s['cats'][f[4:]]}"
            old, new = qty(skin, c["old"], "amount"), qty(skin, c["new"], "amount")
        elif f == "value":
            what, old, new = "the figure", qty(skin, c["old"], "elig"), qty(skin, c["new"], "elig")
        elif f == "n":
            what, old, new = "the number of days", str(c["old"]), str(c["new"])
        else:
            raise ValueError(f)
        txt = f"Amendment {c['k']}, effective {dtext(c['eff'], ds)}: in clause {T}, {what} {old} is replaced by {new}."
        if c["withdrawn"]:
            txt += " This amendment has been withdrawn."
        return txt
    raise ValueError(k)


def parse_clause(text: str, skin: str, count: str, cid: str, refs: dict, ds_any=True) -> dict:
    """One clause sentence -> a clause dict (ids 'c<number>'); refs: number -> kind (filled in a second pass)."""
    s = S[skin]
    day = "business day" if count == "business" else "day"
    R = lambda n: f"c{n}"  # noqa: E731
    if text.startswith("All periods are counted in"):
        return {"id": cid, "kind": "i_days"}
    if text.startswith("Public holidays: "):
        body = text[len("Public holidays: "):-1]
        return {"id": cid, "kind": "i_hol", "_hol": [] if body == "none" else [parse_d(x) for x in body.split(", ")]}
    if text.startswith("An exception applies only to the clause it names"):
        return {"id": cid, "kind": "i_exc"}
    if text.startswith("An amendment replaces the figure it names"):
        return {"id": cid, "kind": "i_amend"}
    if text.startswith("If more than one ground for refusal applies"):
        return {"id": cid, "kind": "i_order"}
    if text.startswith("A fact that the case file does not show"):
        return {"id": cid, "kind": "i_missing"}
    if re.match(r"When both the general limit and an? ", text):
        return {"id": cid, "kind": "i_prec", "_prec": "specific"}
    if text.startswith("When two limits apply to a request, the one in the clause placed later"):
        return {"id": cid, "kind": "i_prec", "_prec": "later"}
    if text == "When two limits apply to a request, the lower one applies.":
        return {"id": cid, "kind": "i_prec", "_prec": "lower"}
    E0 = s["elig"][0][0].upper() + s["elig"][0][1:]
    m = re.fullmatch(re.escape(E0) + r" is a 'qualifying \S+ figure' when it is (at least|more than|at most|less than) "
                     r"(.+)\.", text)
    if m:
        return {"id": cid, "kind": "defn", "gate": "elig", "op": OP_R[m.group(1)],
                "value": fstr(parse_qty(skin, m.group(2), "elig"))}
    if text.startswith("A request that meets every requirement and is not excluded"):
        return {"id": cid, "kind": "entitle"}
    E = s["elig"][0][0].upper() + s["elig"][0][1:]
    m = re.fullmatch(re.escape(E) + r" must be a qualifying \S+ figure \(clause (\d+)\)\.", text)
    if m:
        return {"id": cid, "kind": "req", "gate": "elig", "via": R(m.group(1))}
    m = re.fullmatch(re.escape(E) + r" must be (at least|more than|at most|less than) (.+)\.", text)
    if m:
        return {"id": cid, "kind": "req", "gate": "elig", "op": OP_R[m.group(1)],
                "value": fstr(parse_qty(skin, m.group(2), "elig")), "via": None}
    m = re.fullmatch(r"The request must be received (no later than|before) the (\d+)(?:st|nd|rd|th) " + re.escape(day) +
                     r" (after|before) " + re.escape(s["event"]) + r"\.", text)
    if m:
        return {"id": cid, "kind": "req", "gate": "time", "n": int(m.group(2)), "incl": m.group(1) == "no later than",
                "_dir": m.group(3)}
    m = re.fullmatch(r"A request of the type '(.+)' must also include (.+)\.", text)
    if m:
        it = {v: k for k, v in s["types"].items()}
        idoc = {v: k for k, v in s["docs2"].items()}
        return {"id": cid, "kind": "req", "gate": "docs", "scope_type": it[m.group(1)], "docs2": idoc[m.group(2)]}
    if text == f"The request must include {s['doc_main']}.":
        return {"id": cid, "kind": "req", "gate": "docs"}
    m = re.fullmatch(r"Exception to clause (\d+): when (.+), the time limit in clause \1 counts (\d+) " + re.escape(day) +
                     r"s instead of the number stated there\.", text)
    if m:
        cats, conds = parse_cond_phrase(skin, m.group(2))
        return {"id": cid, "kind": "exc", "target": R(m.group(1)), "cats": cats, "conds": conds, "mode": "period",
                "n2": int(m.group(3))}
    m = re.fullmatch(r"Exception to clause (\d+): clause \1 does not exclude the request when (.+)\.", text)
    if m:
        cats, conds = parse_cond_phrase(skin, m.group(2))
        return {"id": cid, "kind": "exc", "target": R(m.group(1)), "cats": cats, "conds": conds, "mode": "waive"}
    m = re.fullmatch(r"Exception to clause (\d+): the requirement in clause \1 counts as met when (.+)\.", text)
    if m:
        cats, conds = parse_cond_phrase(skin, m.group(2))
        return {"id": cid, "kind": "exc", "target": R(m.group(1)), "cats": cats, "conds": conds, "mode": "waive"}
    m = re.fullmatch(r"Exception to clause (\d+): clause \1 does not apply when (.+)\.", text)
    if m:
        cats, conds = parse_cond_phrase(skin, m.group(2))
        return {"id": cid, "kind": "excexc", "target": R(m.group(1)), "cats": cats, "conds": conds}
    m = re.fullmatch(r"No " + re.escape(s["benefit"]) + r" is given when (.+)\.", text)
    if m:
        cats, conds = parse_cond_phrase(skin, m.group(1))
        return {"id": cid, "kind": "excl", "cats": cats, "conds": conds}
    m = re.fullmatch(r"The " + re.escape(s["benefit"]) + r" is limited to (.+)\.", text)
    if m:
        return {"id": cid, "kind": "lim_gen", "limit": int(parse_qty(skin, m.group(1), "amount"))}
    m = re.fullmatch(r"Limits by " + re.escape(s["catlabel"]) + r": (.+)\.", text)
    if m:
        inv = {v: k for k, v in s["cats"].items()}
        rows = []
        for part in m.group(1).split("; "):
            n, v = part.rsplit(": ", 1)
            rows.append([inv[n], int(parse_qty(skin, v, "amount"))])
        return {"id": cid, "kind": "lim_tab", "rows": rows}
    if text.startswith(f"The {s['benefit']} covers the {s['amount'][0]} up to the applicable limit"):
        return {"id": cid, "kind": "grant"}
    m = re.fullmatch(r"Where clause (\d+) and clause (\d+) both set a limit for a request, clause \2 prevails; if "
                     r"clause \2 sets none for it, the lower limit applies\.", text)
    if m:
        return {"id": cid, "kind": "prec_named", "a": R(m.group(1)), "b": R(m.group(2))}
    fig_rx = r"(\$?[\d,]+(?:\.\d+)?(?: [a-z]+)?)"
    m = re.fullmatch(r"Amendment (\d+), effective (.+?): in clause (\d+), (the limit for .+?|the limit|the figure|the "
                     r"number of days) " + fig_rx + r" is replaced by " + fig_rx +
                     r"\.( This amendment has been withdrawn\.)?", text)
    if m:
        what = m.group(4)
        inv = {v: k for k, v in s["cats"].items()}
        if what == "the limit":
            fld, w = "limit", "amount"
        elif what.startswith("the limit for "):
            fld, w = "row:" + inv[what[len("the limit for "):]], "amount"
        elif what == "the figure":
            fld, w = "value", "elig"
        else:
            fld, w = "n", None
        conv = (lambda v: str(int(v))) if w is None else (lambda v: fstr(parse_qty(skin, v, w)))
        old, new = conv(m.group(5)), conv(m.group(6))
        if fld != "value":
            old, new = str(int(Fraction(old))), str(int(Fraction(new)))
        return {"id": cid, "kind": "amend", "k": int(m.group(1)), "target": R(m.group(3)), "field": fld,
                "old": old, "new": new, "eff": parse_d(m.group(2)), "withdrawn": bool(m.group(7))}
    for t, d in s["terms"]:
        if text == f"'{t}' means {d}.":
            return {"id": cid, "kind": "udef"}
    if text in s["procs"]:
        return {"id": cid, "kind": "proc"}
    raise ValueError(f"clause not parsed ({skin}): {text!r}")


# ------------------------------------------------------------------------------------------------ the case file
def case_fields(doc: dict, case: dict, ds: str) -> list:
    """[(label, value text)] of the case file, in a fixed order."""
    s = S[doc["skin"]]
    out = [("Reference", case["ref"]), ("Name", case["name"]),
           (s["catlabel"][0].upper() + s["catlabel"][1:], s["cats"][case["cat"]]),
           ("Request type", s["types"][case["type"]]),
           (s["elig"][0][0].upper() + s["elig"][0][1:], qty(doc["skin"], case["elig"], "elig")),
           (s["event"][4].upper() + s["event"][5:] if s["event"].startswith("the ") else s["event"],
            dtext(case["event"], ds)),
           ("Request received", dtext(case["request"], ds)),
           ("Documents included", s["doc_main"] if case["docs"] else "none"),
           (s["amount"][0][0].upper() + s["amount"][0][1:], qty(doc["skin"], case["amount"], "amount"))]
    for f, ph in s["flags"].items():
        out.append((ph[0].upper() + ph[1:], "yes" if case["flags"].get(f) is True else "no"))
    out.append(("File reviewed on", dtext(case["proc"], ds)))
    return out


def decoy_line(doc: dict, case: dict) -> str | None:
    d = case.get("decoy")
    if not d:
        return None
    s = S[doc["skin"]]
    return (f"Note: file {d['ref']} ({d['name']}, {s['cats'][d['cat']]}, {s['elig'][0]} "
            f"{qty(doc['skin'], d['elig'], 'elig')}) is a separate case and is not decided here.")


def parse_case(skin: str, fields: list) -> dict:
    s = S[skin]
    d = dict(fields)
    cap = lambda x: x[0].upper() + x[1:]  # noqa: E731
    ev_label = cap(s["event"][4:]) if s["event"].startswith("the ") else s["event"]
    inv_cat = {v: k for k, v in s["cats"].items()}
    inv_type = {v: k for k, v in s["types"].items()}
    case = {"ref": d["Reference"], "name": d["Name"], "cat": inv_cat[d[cap(s["catlabel"])]],
            "type": inv_type[d["Request type"]], "elig": fstr(parse_qty(skin, d[cap(s["elig"][0])], "elig")),
            "event": parse_d(d[ev_label]), "request": parse_d(d["Request received"]),
            "docs": d["Documents included"] == s["doc_main"],
            "amount": int(parse_qty(skin, d[cap(s["amount"][0])], "amount")),
            "flags": {f: d[cap(ph)] == "yes" for f, ph in s["flags"].items()}}
    if d["Documents included"] not in ("none", s["doc_main"]):
        raise ValueError("documents line")
    return case


# ------------------------------------------------------------------------------------------------ the state
def numbering(doc: dict) -> dict:
    return {c["id"]: i + 1 for i, c in enumerate(doc["clauses"])}


def title_of(doc: dict) -> str:
    return f"{doc['org']}: {S[doc['skin']]['doc']} (version of {doc['version']})"


def prep(doc: dict) -> dict:
    """Index inert clauses (udef / proc) so each gets its own devx sentence."""
    d = dict(doc, clauses=[dict(c) for c in doc["clauses"]])
    n = Counter()
    for c in d["clauses"]:
        if c["kind"] in ("udef", "proc"):
            c["_i"] = n[c["kind"]]
            n[c["kind"]] += 1
    return d


def render_state(doc: dict, case: dict, fmt: str) -> str:
    doc = prep(doc)
    num = numbering(doc)
    ds = "iso" if fmt in ("code", "json") else "long"
    secs = []
    for c in doc["clauses"]:
        if not secs or secs[-1][0] != c["sec"]:
            secs.append((c["sec"], []))
        secs[-1][1].append(c)
    cf = case_fields(doc, case, ds)
    dl = decoy_line(doc, case)
    if fmt == "json":
        obj = {"document": {"title": title_of(doc), "parts": [{"heading": SEC_HEAD[sec], "clauses": [
            {"clause": num[c["id"]], "text": clause_text(c, doc, num, ds)} for c in cs]} for sec, cs in secs]},
               "case_file": {k: v for k, v in cf}, "desk_note": dl}
        return mv.render_json(obj)
    if fmt == "code":
        lines = [title_of(doc).upper(), ""]
        for i, (sec, cs) in enumerate(secs, 1):
            lines.append(f"PART {i} - {SEC_HEAD[sec].upper()}")
            lines += [f"{num[c['id']]}. {clause_text(c, doc, num, ds)}" for c in cs]
            lines.append("")
        lines.append("CASE FILE")
        lines += [f"{k}: {v}" for k, v in cf]
        if dl:
            lines += ["", dl]
        return "\n".join(lines)
    # memo
    lines = [f"Extract from {title_of(doc)}.", ""]
    for sec, cs in secs:
        lines.append(f"{SEC_HEAD[sec]}.")
        lines += [f"Clause {num[c['id']]}. {clause_text(c, doc, num, ds)}" for c in cs]
        lines.append("")
    lines.append("The case file reads as follows.")
    lines += [f"{k}: {v}" for k, v in cf]
    if dl:
        lines += ["", dl]
    return "\n".join(lines)


def _skin_of_title(t: str) -> tuple[str, str]:
    m = re.fullmatch(r"(.+): (.+) \(version of (\d{4}-\d{2}-\d{2})\)", t)
    for k, v in S.items():
        if v["doc"] == m.group(2):
            return k, m.group(1)
    raise ValueError(f"title {t!r}")


def parse_state(text: str) -> tuple[dict, dict]:
    if text.startswith("{"):
        o = json.loads(text)
        skin, org = _skin_of_title(o["document"]["title"])
        cl = [(c["clause"], c["text"], p["heading"]) for p in o["document"]["parts"] for c in p["clauses"]]
        fields = list(o["case_file"].items())
    else:
        L = text.split("\n")
        if L[0].startswith("Extract from "):
            skin, org = _skin_of_title(L[0][len("Extract from "):-1])
            cl, head = [], None
            i = 2
            heads = {v + "." for v in SEC_HEAD.values()}
            while L[i] != "The case file reads as follows.":
                if L[i] in heads:
                    head = L[i][:-1]
                else:
                    m = re.fullmatch(r"Clause (\d+)\. (.+)", L[i])
                    if m:
                        cl.append((int(m.group(1)), m.group(2), head))
                i += 1
            fields = [tuple(x.split(": ", 1)) for x in L[i + 1:] if x and not x.startswith("Note: file ")]
        else:
            t = L[0]
            skin = org = None
            for k, v in S.items():
                m = re.fullmatch(r"(.+): " + re.escape(v["doc"].upper()) + r" \(VERSION OF (\d{4}-\d{2}-\d{2})\)", t)
                if m:
                    skin, org = k, m.group(1)
            if skin is None:
                raise ValueError("title")
            cl, head = [], None
            i = 2
            while L[i] != "CASE FILE":
                m = re.fullmatch(r"PART \d+ - (.+)", L[i])
                if m:
                    head = next(v for v in SEC_HEAD.values() if v.upper() == m.group(1))
                else:
                    m = re.fullmatch(r"(\d+)\. (.+)", L[i])
                    if m:
                        cl.append((int(m.group(1)), m.group(2), head))
                i += 1
            fields = [tuple(x.split(": ", 1)) for x in L[i + 1:] if x and not x.startswith("Note: file ")]
    inv_sec = {v: k for k, v in SEC_HEAD.items()}
    count = "calendar"
    for _, t, _ in cl:
        if t.startswith("All periods are counted in business days"):
            count = "business"
    clauses, hol, prec = [], [], None
    for n, t, h in sorted(cl):
        c = parse_clause(t, skin, count, f"c{n}", {})
        c["sec"] = inv_sec[h]
        if c["kind"] == "i_hol":
            hol = c.pop("_hol")
        if c["kind"] == "i_prec":
            prec = c.pop("_prec")
        if c.get("_dir") is not None:
            if c.pop("_dir") != time_dir(skin):
                raise ValueError("time direction differs from the scheme's")
        clauses.append(c)
    if prec is None:
        prec = "named" if any(c["kind"] == "prec_named" for c in clauses) else "lower"
    doc = {"skin": skin, "org": org, "count": count, "holidays": hol, "prec": prec, "clauses": clauses}
    case = parse_case(skin, fields)
    return doc, case


# ------------------------------------------------------------------------------------------------ questions
def q_text(kind: str, doc: dict, case: dict, target: str | None = None, wording: str | None = None) -> str:
    ref = case["ref"]
    if kind == "is":
        return f"Applying the document exactly as written, is the outcome for request {ref}: {target}?"
    if kind == "not":
        return f"Applying the document exactly as written, is the outcome for request {ref} anything other than: {target}?"
    if kind == "jb":
        if wording == "fallback":
            return f"Statement: the outcome for request {ref} is: {target}. Applying the document, which option fits?"
        return f"Applying the document exactly as written, which statement about request {ref} holds?"
    if kind == "outcome":
        return f"Applying the document exactly as written, what is the outcome for request {ref}?"
    if kind == "decisive":
        return (f"Which one clause decides request {ref}, in the sense that deleting that clause alone from the "
                f"document would change the outcome?")
    raise ValueError(kind)


Q_PATTERNS = [
    ("is", r"Applying the document exactly as written, is the outcome for request (?P<ref>\S+): (?P<t>.+)\?"),
    ("not", r"Applying the document exactly as written, is the outcome for request (?P<ref>\S+) anything other than: (?P<t>.+)\?"),
    ("jbf", r"Statement: the outcome for request (?P<ref>\S+) is: (?P<t>.+)\. Applying the document, which option fits\?"),
    ("jb", r"Applying the document exactly as written, which statement about request (?P<ref>\S+) holds\?"),
    ("outcome", r"Applying the document exactly as written, what is the outcome for request (?P<ref>\S+)\?"),
    ("decisive", r"Which one clause decides request (?P<ref>\S+), in the sense that deleting that clause alone from the "
                 r"document would change the outcome\?"),
]


def parse_question(s: str):
    for k, pat in Q_PATTERNS:
        m = re.fullmatch(pat, s)
        if m:
            return k, m.groupdict()
    raise ValueError(f"question {s!r}")


def yn_defs(kind: str, target: str) -> dict:
    same = f"working through the document gives exactly this outcome: {target}"
    other = "working through the document gives a different outcome"
    return {"yes": same, "no": other} if kind == "is" else {"yes": other, "no": same}


def jb_descs(ref: str, target: str) -> tuple:
    return f"The outcome for request {ref} is: {target}.", f"The outcome for request {ref} is not: {target}."


# ------------------------------------------------------------------------------------------------ load + plan
def export(n: int = N_EXPORT) -> list:
    import gen3_rule_chain as g1   # its devx latent export only (prefix-stable: the first 100 are the JSON file)
    return g1.devx_latents(n)


def load() -> list:
    xs = export()
    items = []
    for x in xs:
        doc, case, q = x["facts"]["doc"], x["facts"]["case"], x["query"]
        code, tr = rc_core.decide(doc, case)
        assert not mv.is_undefined(code), x["latent_id"]
        inv = {v: k for k, v in x["outcomes"].items()}
        if q["kind"] == "outcome":
            assert inv[x["gold"]] == code, x["latent_id"]
            g = code
        elif q["kind"] == "outcome_is":
            g = "yes" if inv[q["target"]] == code else "no"
            assert g == x["gold"], x["latent_id"]
            q = dict(q, target_code=inv[q["target"]])
        else:
            pv = rc_core.pivotal(doc, case)
            assert pv == [x["gold"]], x["latent_id"]
            g = x["gold"]
        items.append(dx.Item(x["latent_id"], x["tier"], doc["skin"], q["kind"], x["facts"], q, g, {"code": code}))
    return items


LAST_PLAN_REPORT: dict = {}


def plan(items: list, rng) -> list:
    """In export order: 25 'which outcome' choice rows, 25 'which clause decides' rows and 50 outcome_is latents
    (truth 25/25), of which 10 become JB rows; yes/no gold balanced with the inverse wording (dx.balance_assign)."""
    oc = [it for it in items if it.kind == "outcome"][:25]
    dc = [it for it in items if it.kind == "decisive"][:25]
    yn_all = [it for it in items if it.kind == "outcome_is"]
    pick, cnt = [], Counter()
    for it in yn_all:
        if cnt[it.gold0] < 25:
            pick.append(it)
            cnt[it.gold0] += 1
    jb = [it for it in pick if it.gold0 == "yes"][:5] + [it for it in pick if it.gold0 == "no"][:5]
    yn = [it for it in pick if it not in jb]
    rot = dx.Rotor(rng)
    out = []
    for it in oc:
        out.append((it, {"v": "outcome", "fmt": rot.pick("fmt", FMTS, ("outcome",))}))
    for it in dc:
        out.append((it, {"v": "decisive", "fmt": rot.pick("fmt", FMTS, ("decisive",))}))
    units, meta = [], []
    for it in jb:
        t = it.gold0 == "yes"
        units.append([({"qk": "jb", "fmt": f, "tier": it.tier, "pack": it.pack, "pol": 0}, t) for f in FMTS])
        meta.append((it, [("jb", f) for f in FMTS]))
    for it in yn:
        t = it.gold0 == "yes"
        cands, cm = [], []
        lb = {f: mv.len_bin(len(render_state(it.facts["doc"], it.facts["case"], f))) for f in FMTS}
        for k in ("is", "not"):
            for f in FMTS:
                cands.append(({"qk": "yn", "tpl": k, "fmt": f, "tier": it.tier, "pack": it.pack,
                               "pol": int(k == "not"), "code": it.query["target_code"], "len_bin": lb[f]},
                              t != (k == "not")))
                cm.append((k, f))
        units.append(cands)
        meta.append((it, cm))
    ch = dx.balance_assign(units, rng)
    for (it, cm), i in zip(meta, ch):
        v, f = cm[i]
        out.append((it, {"v": v, "fmt": f}))
    LAST_PLAN_REPORT.clear()
    LAST_PLAN_REPORT.update({"views": dict(Counter(v["v"] for _, v in out))})
    out.sort(key=lambda x: x[0].lid)
    return out


# ------------------------------------------------------------------------------------------------ render
def edges(doc: dict, case: dict) -> tuple:
    tr = rc_core.evaluate(doc, case)
    tags = set()
    g = rc_core.primary_group(rc_core.groups(doc, case, tr))
    if g:
        tags |= {"exc:" + g, "exception"}
    if tr["amend_used"] or any(c["kind"] == "amend" for c in doc["clauses"]):
        tags.add("hc:amendment_effective")
    if any(c["kind"] == "excexc" for c in doc["clauses"]):
        tags.add("hc:exception_to_exception")
    if doc["count"] == "business":
        tags.add("hc:business_days")
    if doc["prec"] == "specific":
        tags.add("hc:specific_over_general")
    if case.get("decoy"):
        tags.add("hc:decoy_id")
    tags.add("long_context")
    return tuple(sorted(t for t in tags if t in mv.EDGE_TAGS))


def outcome_options(it: dx.Item, fb, rng) -> tuple[list, str]:
    """Gold + the outcomes of the shortcut readings (rc_core modes) + others, 5 options in a balanced position."""
    doc, case = it.facts["doc"], it.facts["case"]
    skin = doc["skin"]
    code = it.extra["code"]
    wrong = []
    for m, t in rc_core.shortcut_traces(doc, case).items():
        if t is not None and t["code"] != code and t["code"] not in wrong:
            wrong.append(t["code"])
    rest = [c for c in CODES if c != code and c not in wrong]
    rng.shuffle(rest)
    wrong = (wrong + rest)[:4]
    opts = fb.place(outcome_text(skin, code), [outcome_text(skin, c) for c in wrong], rng,
                    stratum=("dx1", "outcome", 5))
    return opts, outcome_text(skin, code)


def render(it: dx.Item, view: dict, fb, rng) -> mv.RowSpec:
    doc, case = it.facts["doc"], it.facts["case"]
    skin, fmt, v = doc["skin"], view["fmt"], view["v"]
    state = render_state(doc, case, fmt)
    e = edges(doc, case)
    num = numbering(doc)
    if v in ("is", "not"):
        tgt = outcome_text(skin, it.query["target_code"])
        yes = (it.gold0 == "yes") != (v == "not")
        return mv.RowSpec("base", "yn", state, q_text(v, doc, case, tgt), "yes" if yes else "no", FMT_META[fmt],
                          "dx1_" + fmt, "dx1." + v, defs=yn_defs(v, tgt), polarity=int(v == "not"),
                          role="neg" if v == "not" else "aff", edge=e)
    if v == "jb":
        tgt = outcome_text(skin, it.query["target_code"])
        y, n = jb_descs(case["ref"], tgt)
        opts, gold, wording = fb.jb(y, n, it.gold0 == "yes", rng, stratum=("dx1",))
        return mv.RowSpec("jb", "jb", state, q_text("jb", doc, case, tgt, wording), gold, FMT_META[fmt],
                          "dx1_" + fmt, "dx1.jb" + ("f" if wording == "fallback" else ""), options=opts, polarity=0,
                          edge=e)
    if v == "outcome":
        opts, gold = outcome_options(it, fb, rng)
        return mv.RowSpec("base", "choice", state, q_text("outcome", doc, case), gold, FMT_META[fmt], "dx1_" + fmt,
                          "dx1.outcome", options=opts, edge=e)
    cands = list(it.query["candidates"])
    gold = f"Clause {num[it.gold0]}"
    others = [f"Clause {num[c]}" for c in cands if c != it.gold0]
    opts = fb.place(gold, others, rng, stratum=("dx1", "decisive", len(cands)))
    return mv.RowSpec("base", "choice", state, q_text("decisive", doc, case), gold, FMT_META[fmt], "dx1_" + fmt,
                      "dx1.decisive", options=opts, edge=e)


# ------------------------------------------------------------------------------------------------ parse-back
def parse(g: dict) -> dict:
    doc, case = parse_state(g["state"])
    k, d = parse_question(g["instructions"])
    if d["ref"] != case["ref"]:
        raise ValueError("question names another request")
    out = {"doc": doc, "case": case, "kind": k, "options": g["options"]}
    if k in ("is", "not", "jbf"):
        out["target"] = code_of_outcome(doc["skin"], d["t"])
    if k == "jb":
        m = re.fullmatch(r"The outcome for request \S+ is: (.+)\.", g["options"][0])
        out["target"] = code_of_outcome(doc["skin"], m.group(1))
    return out


def relabel(p: dict, g: dict):
    doc, case = p["doc"], p["case"]
    code, _ = rc_core.decide(doc, case)
    if mv.is_undefined(code):
        raise ValueError("decide undefined on the parsed document")
    k = p["kind"]
    if k == "is":
        return "yes" if code == p["target"] else "no"
    if k == "not":
        return "no" if code == p["target"] else "yes"
    if k in ("jb", "jbf"):
        return p["options"][0] if code == p["target"] else p["options"][1]
    if k == "outcome":
        return outcome_text(doc["skin"], code)
    pv = rc_core.pivotal(doc, case)
    if len(pv) != 1:
        raise ValueError(f"pivotal clauses on the parsed document: {pv}")
    return f"Clause {int(pv[0][1:])}"


def _canon_clause(c: dict, idmap) -> tuple:
    keep = {k: v for k, v in c.items() if k not in ("id", "sec", "_i", "text", "term")}
    for k in ("target", "via", "a", "b"):
        if keep.get(k):
            keep[k] = idmap(keep[k])
    for k in ("value", "old", "new"):
        if k in keep and keep[k] is not None:
            keep[k] = str(Fraction(str(keep[k])))
    if "conds" in keep:
        keep["conds"] = [dict(a, value=str(Fraction(str(a["value"])))) if a["t"] == "amt" else a
                         for a in keep["conds"]]
    return (c["kind"], c.get("sec"), json.dumps(keep, sort_keys=True))


def _proj(doc: dict, case: dict, idmap) -> dict:
    cs = case
    return {"skin": doc["skin"], "count": doc["count"], "holidays": tuple(doc["holidays"]),
            "prec": doc["prec"], "clauses": tuple(_canon_clause(c, idmap) for c in doc["clauses"]),
            "case": (cs["cat"], cs["type"], str(Fraction(str(cs["elig"]))), cs["event"], cs["request"], cs["docs"],
                     int(cs["amount"]), tuple(sorted((k, v is True) for k, v in cs["flags"].items())))}


def project(it: dx.Item) -> dict:
    doc = it.facts["doc"]
    num = numbering(doc)
    return _proj(doc, it.facts["case"], lambda x: f"c{num[x]}")


def project_parsed(p: dict) -> dict:
    return _proj(p["doc"], p["case"], lambda x: x)
