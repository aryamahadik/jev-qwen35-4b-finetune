"""gen_logic_negation schemas, part B: reported speech vs asserted fact, sarcasm markers, hypotheticals, plans,
modals, set membership, requirement logic, De Morgan facts, negation-scope ambiguity, aspect ('still', 'no longer'),
implicative verbs, exception policies, exceptives, numeric thresholds and units, calendar exceptions, lexical
negation.  Same contract as part A: each schema returns a fact-flip twin pair with a shared question.
"""
import datetime as dt

from ln_engine import (AND, CMP, CNT, COMPANIES, HOTELS, IMP, MONTHS, NOT, OR, PEOPLE, PLACES, STREETS, TEAMS,
                       WEEKDAYS, art, cap, join, lit, nw)
from ln_schemas_a import RULE_HDR, cert_q, end, header, mk, schema, slot


def low1(s):
    return s[:1].lower() + s[1:]


def pick_person(rng, exclude=()):
    while True:
        p = rng.choice(PEOPLE)
        if p[0] not in exclude:
            return p


# ================================================================================================ S15 tested / counted
ORGS = ["library", "housing association", "school", "sports club", "hospital trust", "food bank", "credit union",
        "theatre", "museum", "community centre", "rowing club", "arts council"]
JOBS = ["warehouse", "reception", "lab technician", "bus driver", "junior accountant", "sous-chef", "delivery rider",
        "care assistant", "IT support", "gardener"]
SUBJECTS = ["maths", "history", "chemistry", "French", "geography", "biology", "economics", "art history"]
TESTED = [
    # kind 'event' (the question is false when not all were covered) or 'state' (it is left open)
    ("event", "All {N} members of the {org} board cast a vote for or against the motion, and nobody voted against it.",
     "{k} of the {N} members of the {org} board cast a vote for or against the motion, and nobody voted against it.",
     "every one of the {N} board members voted for the motion"),
    ("event", "All {N} water samples from the {place} reservoir were tested, and none of them failed.",
     "{k} of the {N} water samples from the {place} reservoir were tested, and none of those failed.",
     "all {N} water samples passed the test"),
    ("event", "All {N} applicants for the {job} job sat the written test, and none of them failed it.",
     "{k} of the {N} applicants for the {job} job sat the written test, and none of those who sat it failed.",
     "all {N} applicants passed the written test"),
    ("event", "All {N} students in {x}'s class sat the {subj} exam, and none of them failed it.",
     "{k} of the {N} students in {x}'s class sat the {subj} exam, and none of those who sat it failed.",
     "all {N} students passed the {subj} exam"),
    ("state", "All {N} invoices from {co} were checked, and none contained an error.",
     "{k} of the {N} invoices from {co} were checked, and none of those contained an error.",
     "none of the {N} invoices contains an error"),
    ("state", "All {N} fire exits in the {place} library were inspected, and none was blocked.",
     "{k} of the {N} fire exits in the {place} library were inspected, and none of those was blocked.",
     "none of the {N} fire exits is blocked"),
    ("state", "All {N} smoke alarms in the {place} office were tested, and every one of them worked.",
     "{k} of the {N} smoke alarms in the {place} office were tested, and every tested alarm worked.",
     "all {N} smoke alarms work"),
    ("state", "All {N} boxes in the delivery from {co} were opened, and none had damaged items inside.",
     "{k} of the {N} boxes in the delivery from {co} were opened, and none of the opened boxes had damaged items inside.",
     "none of the {N} boxes has damaged items inside"),
    ("state", "All {N} rooms on the top floor of the {place} hotel were checked for mould, and none had any.",
     "{k} of the {N} rooms on the top floor of the {place} hotel were checked for mould, and none of the checked "
     "rooms had any.", "none of the {N} rooms on the top floor has mould"),
    ("state", "All {N} laptops in the {place} office were scanned, and none had malware.",
     "{k} of the {N} laptops in the {place} office were scanned, and none of the scanned laptops had malware.",
     "none of the {N} laptops has malware"),
    ("state", "All {N} runners who started the {place} half marathon were timed at the finish, and none was "
     "disqualified.", "{k} of the {N} runners who started the {place} half marathon were timed at the finish, and none "
     "of the timed runners was disqualified.", "none of the {N} runners was disqualified"),
    ("state", "All {N} trays of eggs from the {place} farm were checked, and none had a cracked egg.",
     "{k} of the {N} trays of eggs from the {place} farm were checked, and none of the checked trays had a cracked egg.",
     "none of the {N} trays has a cracked egg"),
]


@schema("tested_subset", 280)
def s_tested(rng):
    kind, t_all, t_k, goal_s = rng.choice(TESTED)
    N = rng.randint(4, 12)
    k = rng.randint(1, N - 1)
    sl = dict(org=rng.choice(ORGS), place=rng.choice(PLACES), job=rng.choice(JOBS), x=pick_person(rng)[0],
              subj=rng.choice(SUBJECTS), co=rng.choice(COMPANIES), N=N)
    goal_s = goal_s.format(**sl)
    rows = []
    for full in (True, False):
        c = N if full else k
        txt = (t_all if full else t_k).format(k=cap(nw(k)), **sl)
        if kind == "event":  # covered c, failing among covered f; question: covered - failing == N
            ints = {"c": [0, N], "f": [0, N]}
            prem = [CMP("c", "==", c), CMP("f", "==", 0), CMP("f", "<=", "c")]
            goal = CMP(("add", "c", ("mul", -1, "f")), "==", N)
        else:                # bad among covered b1, bad among uncovered b2 (at most N - c)
            ints = {"c": [0, N], "b1": [0, N], "b2": [0, N]}
            prem = [CMP("c", "==", c), CMP("b1", "==", 0), CMP("b2", "<=", ("add", N, ("mul", -1, "c")))]
            goal = CMP(("add", "b1", "b2"), "==", 0)
        rows.append((txt, prem, "yes" if full else "no", ints))
    rng.shuffle(rows)
    q = cert_q(rng, rng.choice(["text", "report"]), goal_s)
    return [mk(t, q, "certain", "missing_info" if g == "no" else "quantifier", p, goal, g, kind, ints=i)
            for t, p, g, i in rows]


# ================================================================================================ S16 double negation forms
DN = [
    # plural, singular, object NP, verb phrase meaning 'got the object'
    ("applicants", "applicant", "an interview slot", "receive an interview slot"),
    ("passengers", "passenger", "a meal voucher", "receive a meal voucher"),
    ("volunteers", "volunteer", "a safety briefing", "get a safety briefing"),
    ("tenants", "tenant", "a copy of the new lease", "receive a copy of the new lease"),
    ("players", "player", "a medical check", "have a medical check"),
    ("new employees", "new employee", "a laptop", "receive a laptop"),
    ("students", "student", "a locker", "get a locker"),
    ("patients", "patient", "a follow-up appointment", "get a follow-up appointment"),
    ("drivers", "driver", "a parking pass", "receive a parking pass"),
    ("guests", "guest", "a welcome pack", "receive a welcome pack"),
    ("runners", "runner", "a finisher's medal", "receive a finisher's medal"),
    ("contractors", "contractor", "a security badge", "receive a security badge"),
    ("pupils", "pupil", "a reading book", "get a reading book"),
    ("delegates", "delegate", "a seat at the dinner", "get a seat at the dinner"),
    ("nurses", "nurse", "a winter uniform", "receive a winter uniform"),
    ("residents", "resident", "a new recycling bin", "get a new recycling bin"),
]


@schema("double_negation", 440)
def s_double_neg(rng):
    pl, sg, obj, vb = rng.choice(DN)
    x = pick_person(rng)[0]
    V, M = "V", "M"
    memb = f"{x} was one of the {pl}."
    form = rng.choice("abcdefg")
    if form == "a":
        pos = (f"{memb} No {sg} was left without {obj}.", [M, IMP(M, V)])
        neg = (f"{memb} Only one {sg}, {x}, was left without {obj}.", [M, NOT(V)])
    elif form == "b":
        pos = (f"{memb} None of the {pl} failed to {vb}.", [M, IMP(M, V)])
        neg = (f"{memb} Only {x} failed to {vb}.", [M, NOT(V)])
    elif form == "c":
        pos = (f"{memb} There was not a single {sg} who did not {vb}.", [M, IMP(M, NOT(NOT(V)))])
        neg = (f"{memb} There was a single {sg} who did not {vb}: {x}.", [M, NOT(V)])
    elif form == "d":
        pos = (f"It is not true that {x} did not {vb}.", [NOT(NOT(V))])
        neg = (f"It is true that {x} did not {vb}.", [NOT(V)])
    elif form == "e":
        pos = (f"{x} did not fail to {vb}.", [NOT(NOT(V))])
        neg = (f"{x} did not manage to {vb}.", [NOT(V)])
    elif form == "f":
        pos = (f"Not one of the {pl}, {x} included, was denied {obj}.", [M, IMP(M, V)])
        neg = (f"Not one of the {pl} except {x} was denied {obj}.", [M, NOT(V)])
    else:
        pos = (f"Nobody among the {pl}, including {x}, went without {obj}.", [M, IMP(M, V)])
        neg = (f"Nobody among the {pl} except {x} went without {obj}.", [M, NOT(V)])
    rows = [(pos[0], pos[1], "yes"), (neg[0], neg[1], "no")]
    rng.shuffle(rows)
    q = f"Did {x} {vb}?"
    hdr = header(rng, ["Update from the organisers:", "Summary from the coordinator:", "Note from the office:"], 0.3)
    return [mk(hdr + s, q, "true", "double_negation", p, V, g, form) for s, p, g in rows]


# ================================================================================================ S17 almost / barely
ALMOST = [
    ("the charity drive", "reached its fundraising target", "reach its fundraising target"),
    ("{x}", "passed the driving test", "pass the driving test"),
    ("{t}", "won the cup final", "win the cup final"),
    ("{x}", "caught the last train home", "catch the last train home"),
    ("the bill", "passed the Senate", "pass the Senate"),
    ("the start-up", "broke even in its first year", "break even in its first year"),
    ("{x}", "finished the marathon in under four hours", "finish the marathon in under four hours"),
    ("the museum", "sold out its opening weekend", "sell out its opening weekend"),
    ("the renovation", "came in under budget", "come in under budget"),
    ("the petition", "reached 10,000 signatures", "reach 10,000 signatures"),
    ("{x}", "qualified for the final", "qualify for the final"),
    ("the school", "met its attendance target", "meet its attendance target"),
    ("{x}", "made the 5 p.m. deadline", "make the 5 p.m. deadline"),
    ("the climbers", "reached the summit before dark", "reach the summit before dark"),
    ("{x}", "won the seat on the council", "win the seat on the council"),
    ("the shop", "covered its rent this month", "cover its rent this month"),
    ("the ferry", "made it across before the storm", "make it across before the storm"),
    ("the team", "finished the project on time", "finish the project on time"),
    ("{x}", "hit the monthly sales quota", "hit the monthly sales quota"),
    ("the union", "won the ballot", "win the ballot"),
]
# (negative-meaning form, positive-meaning form); '{vp}' past VP, '{vb}' base VP
ALM_PAIRS = [("almost {vp}", "barely {vp}"), ("nearly {vp}", "only just {vp}"), ("all but {vp}", "narrowly {vp}"),
             ("very nearly {vp}", "barely {vp}"), ("just failed to {vb}", "just managed to {vb}"),
             ("narrowly failed to {vb}", "narrowly {vp}")]


@schema("almost_barely", 300)
def s_almost(rng):
    subj, vp, vb = rng.choice(ALMOST)
    subj = subj.format(x=pick_person(rng)[0], t=rng.choice(TEAMS))
    negf, posf = rng.choice(ALM_PAIRS)
    H = "H"
    rows = [(negf.format(vp=vp, vb=vb), NOT(H), "no"), (posf.format(vp=vp, vb=vb), H, "yes")]
    rng.shuffle(rows)
    q = f"Did {subj} {vb}?"
    return [mk(f"{cap(subj)} {s}.", q, "true", "implicit", [p], H, g, "neg" if g == "no" else "pos")
            for s, p, g in rows]


# ================================================================================================ S21 claim vs confirmed
PROPS = [
    ("the shipment left the warehouse on Monday", ["the supplier", "the dispatcher"], "the tracking record"),
    ("the boiler was repaired last week", ["the landlord", "the caretaker"], "the repair log"),
    ("the invoice was paid in full", ["the client", "the finance clerk"], "the bank statement"),
    ("the fire exit was blocked during the inspection", ["a tenant", "the inspector's assistant"],
     "the inspection photos"),
    ("the driver stopped at the red light", ["the driver", "a passenger"], "the dashcam footage"),
    ("the vaccine samples were stored below 5°C", ["the lab technician", "the courier"], "the temperature log"),
    ("the contract was signed before the deadline", ["the agent", "the seller"], "the dated signature page"),
    ("the refund was issued on 3 May", ["the shop assistant", "the store manager"], "the card statement"),
    ("the fire alarm was tested in March", ["the facilities manager", "the security guard"], "the maintenance log"),
    ("the files were backed up on Friday", ["the IT technician", "the office manager"], "the backup report"),
    ("the ball crossed the goal line", ["the striker", "the home coach"], "the goal-line camera"),
    ("the power cut started before midnight", ["a neighbour", "the night porter"], "the utility's outage record"),
    ("the package was left with a neighbour", ["the courier", "the driver"], "the delivery photo"),
    ("the meeting was moved to Thursday", ["a colleague", "the team lead"], "the calendar invitation"),
    ("the car was serviced in January", ["the seller", "the previous owner"], "the service book"),
    ("the tenant paid the deposit", ["the tenant", "the letting agent"], "the deposit receipt"),
    ("the software update caused the outage", ["the support engineer", "a user on the forum"], "the incident report"),
    ("the goods were insured during transport", ["the broker", "the shipping agent"], "the insurance certificate"),
    ("the patient took the tablets with food", ["the patient", "the carer"], "the ward's medication chart"),
    ("the train left three minutes late", ["a commuter", "the station announcer"], "the operator's timetable log"),
    ("the museum acquired the painting in 1998", ["the curator", "a tour guide"], "the acquisition register"),
    ("the bridge passed its safety inspection", ["the council spokesperson", "the contractor"],
     "the inspection certificate"),
    ("the machine was switched off before cleaning", ["the operator", "the shift supervisor"],
     "the machine's event log"),
    ("the email reached the client before noon", ["the account manager", "the sales assistant"],
     "the mail server log"),
    ("the fence was built on the neighbour's land", ["the neighbour", "the builder"], "the land survey"),
    ("the order included the charger", ["the customer", "the warehouse clerk"], "the packing list"),
    ("the new drug lowered blood pressure in the trial", ["the drug company", "a patient group"],
     "the published trial data"),
    ("the river rose above the flood mark on Sunday", ["a local resident", "a fisherman"], "the river gauge record"),
    ("the school bus was full on Tuesday", ["a parent", "the driver"], "the bus company's passenger count"),
    ("the heating was switched off overnight", ["a tenant", "the caretaker"], "the thermostat's history"),
]
NONVER = ["{S} claimed that {P}.", "{S} said that {P}.", "{S} insisted that {P}.", "According to {s}, {P}.",
          "{S} believes that {P}.", "{S} told the manager that {P}.", "{S} suspects that {P}.",
          "{S} assumed that {P}.", "{S} is convinced that {P}.", "{S} reported that {P}.", "{S} hoped that {P}."]
VER_PERSON = ["{S} discovered that {P}.", "{S} realized that {P}.", "{S} found out that {P}.",
              "{S} noticed that {P}.", "{S} was surprised to learn that {P}."]
VER_DOC = ["{D} shows that {P}.", "{D} confirms that {P}.", "{D} proves that {P}."]


@schema("claim_vs_fact", 480)
def s_claim(rng):
    P, roles, doc = rng.choice(PROPS)
    s = rng.choice(roles)
    if P.startswith(s + " "):  # 'The driver said that the driver ...' -> use the other role
        s = roles[1 - roles.index(s)]
    Pa, Said = "P", "Said"
    var = rng.choice(["verb", "verb", "doc", "corroborate"])
    if var == "verb":
        nv, vv = rng.choice(NONVER), rng.choice(VER_PERSON)
        if nv.startswith("According"):
            nv = "{S} claimed that {P}."
        rows = [(nv.format(S=cap(s), s=s, P=P), [Said], "no", "reported_speech"),
                (vv.format(S=cap(s), s=s, P=P), [Pa], "yes", "reported_speech")]
    elif var == "doc":
        nv, vd = rng.choice(NONVER), rng.choice(VER_DOC)
        rows = [(nv.format(S=cap(s), s=s, P=P), [Said], "no", "reported_speech"),
                (vd.format(D=cap(doc), P=P), [Pa], "yes", "reported_speech")]
    else:
        base = f"According to {s}, {P}"
        if rng.random() < 0.5:
            rows = [(f"{base}, and {doc} confirms it.", [Said, Pa], "yes", "reported_speech"),
                    (f"{base}, but {doc} has no record of it.", [Said], "no", "conflicting_evidence")]
        else:
            rows = [(f"{base}, and {doc} confirms it.", [Said, Pa], "yes", "reported_speech"),
                    (f"{base}, but {doc} shows otherwise.", [Said, NOT(Pa)], "no", "conflicting_evidence")]
    rng.shuffle(rows)
    q = cert_q(rng, "text", P)
    return [mk(t, q, "certain", e, p, Pa, g, var) for t, p, g, e in rows]


# ================================================================================================ S22 denied / admitted
ACTS = [
    ("borrow the company van on Sunday", "borrowed the company van on Sunday", "borrowed the company van on Sunday",
     "the key log"),
    ("take money from the petty cash", "took money from the petty cash", "taken money from the petty cash",
     "the cash audit"),
    ("leave the fire door open", "left the fire door open", "left the fire door open", "the door sensor log"),
    ("change the admin password", "changed the admin password", "changed the admin password",
     "the system audit trail"),
    ("send the draft to the client", "sent the draft to the client", "sent the draft to the client",
     "the email archive"),
    ("park in the director's space", "parked in the director's space", "parked in the director's space",
     "the car park camera log"),
    ("delete the shared folder", "deleted the shared folder", "deleted the shared folder", "the file server log"),
    ("use the company card for a personal purchase", "used the company card for a personal purchase",
     "used the company card for a personal purchase", "the card statement"),
    ("skip the pre-flight safety check", "skipped the pre-flight safety check", "skipped the pre-flight safety check",
     "the maintenance log"),
    ("sign the delivery note", "signed the delivery note", "signed the delivery note", "the delivery record"),
    ("break the printer", "broke the printer", "broken the printer", "the service report"),
    ("copy answers during the exam", "copied answers during the exam", "copied answers during the exam",
     "the invigilator's report"),
    ("forward the confidential memo", "forwarded the confidential memo", "forwarded the confidential memo",
     "the email archive"),
    ("scratch the rental car", "scratched the rental car", "scratched the rental car", "the check-in photos"),
    ("leave the warehouse unlocked", "left the warehouse unlocked", "left the warehouse unlocked", "the alarm log"),
    ("book the wrong venue", "booked the wrong venue", "booked the wrong venue", "the booking confirmation"),
    ("miss the team meeting", "missed the team meeting", "missed the team meeting", "the attendance sheet"),
    ("take the last parking permit", "took the last parking permit", "taken the last parking permit",
     "the permit register"),
    ("drive over the speed limit", "drove over the speed limit", "driven over the speed limit",
     "the van's tracker data"),
    ("post the photos online", "posted the photos online", "posted the photos online", "the platform's upload log"),
]


@schema("denied_admitted", 300)
def s_denied(rng):
    base, past, pp, doc = rng.choice(ACTS)
    x, s, o, p = pick_person(rng)
    Pa = "P"
    var = rng.choice(["admit_deny", "deny_doc", "deny_but"])
    if var == "admit_deny":
        g1 = rng.random() < 0.5
        adm = f"{x} admitted that {s} had {pp}." if g1 else f"{x} admitted having {pp}."
        den = f"{x} denied that {s} had {pp}." if g1 else f"{x} denied having {pp}."
        rows = [(adm, [Pa], "yes", "reported_speech"), (den, [], "no", "reported_speech")]
        goal, qs = Pa, f"{x} {past}"
    elif var == "deny_doc":
        rows = [(f"{x} denied that {s} had {pp}.", [], "no", "reported_speech"),
                (f"{cap(doc)} shows that {x} did not {base}.", [NOT(Pa)], "yes", "negation")]
        goal, qs = NOT(Pa), f"{x} did not {base}"
    else:
        rows = [(f"{x} denied having {pp}, but {doc} shows that {s} did.", [Pa], "yes", "conflicting_evidence"),
                (f"{x} denied having {pp}, and {doc} shows that {s} did not.", [NOT(Pa)], "no",
                 "conflicting_evidence")]
        goal, qs = Pa, f"{x} {past}"
    rng.shuffle(rows)
    q = cert_q(rng, "text", qs)
    out = []
    for t, pr, g, e in rows:
        if not pr:
            pr = ["Said"]
        out.append(mk(t, q, "certain", e, pr, goal, g, var))
    return out


# ================================================================================================ S23 falsely / correctly
TRUTH_ADV = [("{S} falsely claimed that {P}.", "{S} correctly stated that {P}."),
             ("{S} wrongly believed that {P}.", "{S} rightly believed that {P}."),
             ("{S} incorrectly told the manager that {P}.", "{S} accurately told the manager that {P}."),
             ("{S} incorrectly reported that {P}.", "{S} correctly reported that {P}.")]


@schema("false_true_report", 300)
def s_falsely(rng):
    Pa = "P"
    fa, co = rng.choice(TRUTH_ADV)
    if rng.random() < 0.55:
        P, roles, doc = rng.choice(PROPS)
        S = rng.choice(roles)
        if P.startswith(S + " "):  # avoid 'The patient ... that the patient ...'
            S = roles[1 - roles.index(S)]
        qs, goal = P, Pa
        rows = [(fa.format(S=cap(S), P=P), [NOT(Pa)], "no"), (co.format(S=cap(S), P=P), [Pa], "yes")]
        var = "prop_pos"
    else:
        base, past, pp, doc = rng.choice(ACTS)
        x, s, o, p = pick_person(rng)
        P = f"{s} had {pp}"
        if rng.random() < 0.5:
            qs, goal = f"{x} {past}", Pa
            rows = [(fa.format(S=x, P=P), [NOT(Pa)], "no"), (co.format(S=x, P=P), [Pa], "yes")]
            var = "act_pos"
        else:
            qs, goal = f"{x} did not {base}", NOT(Pa)
            rows = [(fa.format(S=x, P=P), [NOT(Pa)], "yes"), (co.format(S=x, P=P), [Pa], "no")]
            var = "act_neg"
    rng.shuffle(rows)
    q = cert_q(rng, "text", qs)
    return [mk(t, q, "certain", "reported_speech", pr, goal, g, var) for t, pr, g in rows]


# ================================================================================================ S24 claim vs official record
CARS = ["blue hatchback", "silver estate", "red saloon", "white van", "green SUV", "grey coupe", "black pickup"]
FORMS = ["visa form", "grant application", "tax return", "housing application", "course registration",
         "insurance claim form"]
CAFES = ["the Tin Kettle", "Bean Counter", "the Corner Cup", "Crumbs", "the Daily Grind", "Loaf & Ladle"]
RECORD = [
    # claim, record (positive), record (negative), question ; slots filled per pair
    ("\"I never skipped a safety check,\" {x} said.",
     "The maintenance log, which is the official record, lists two safety checks {x} skipped in {mon}.",
     "The maintenance log, which is the official record, lists no safety checks skipped by {x}.",
     "According to the maintenance log, did {x} skip a safety check?"),
    ("The landlord of {n} {st} says the boiler was fixed on {day}.",
     "The repair log, which is the official record, shows a boiler repair at {n} {st} on {day}.",
     "The repair log, which is the official record, shows no boiler repair at {n} {st} since January.",
     "According to the repair log, was the boiler at {n} {st} repaired on {day}?"),
    ("Several staff members at the {pl} office have heard that the canteen will close in {mon}.",
     "The official notice says the canteen will close in {mon}.",
     "The official notice says the canteen will close in {mon2}.",
     "According to the official notice, will the canteen close in {mon}?"),
    ("The seller insists the {car} has never been in an accident.",
     "The vehicle history report lists one accident, in {yr}.", "The vehicle history report lists no accidents.",
     "According to the vehicle history report, has the {car} been in an accident?"),
    ("{x} says {s} submitted the {form} on time.",
     "The portal's timestamp shows the {form} arrived {h} hours before the deadline.",
     "The portal's timestamp shows the {form} arrived {d} days after the deadline.",
     "According to the portal's timestamp, was the {form} submitted on time?"),
    ("A customer posted online that {cafe} was closed all day on {day}.",
     "The café's opening log shows it was closed all day on {day}.",
     "The café's opening log shows it was open from 8 a.m. to 4 p.m. on {day}.",
     "According to the opening log, was {cafe} closed all day on {day}?"),
    ("The contractor claims the work on the {pl} library was finished by 30 June.",
     "The signed completion certificate is dated {d1} June.", "The signed completion certificate is dated {d2} July.",
     "According to the completion certificate, was the work finished by 30 June?"),
    ("Most staff believe the fire drill is on {day}.", "The facilities calendar lists the fire drill on {day}.",
     "The facilities calendar lists the fire drill on {day2}.",
     "According to the facilities calendar, is the fire drill on {day}?"),
    ("The captain of {team} insists that every player attended training on {day}.",
     "The attendance sheet for {day} shows every player present.",
     "The attendance sheet for {day} shows {k} players absent.",
     "According to the attendance sheet, did every player attend training on {day}?"),
    ("A neighbour on {st} says the party went on past midnight.",
     "The noise complaint log records the music stopping at {late}.",
     "The noise complaint log records the music stopping at {early}.",
     "According to the noise complaint log, did the music go on past midnight?"),
    ("{x} says the rent was paid on the 1st.", "The bank statement shows the rent leaving {x}'s account on the 1st.",
     "The bank statement shows the rent leaving {x}'s account on the {dd}th.",
     "According to the bank statement, was the rent paid on the 1st?"),
    ("The coach told parents that the {pl} tournament starts at 9 a.m.",
     "The official tournament schedule gives a 9 a.m. start.", "The official tournament schedule gives a {t2} start.",
     "According to the official schedule, does the tournament start at 9 a.m.?"),
    ("The airline's chatbot said flight {fl} was on time.",
     "The departures board, the airport's official display, shows flight {fl} as on time.",
     "The departures board, the airport's official display, shows flight {fl} as delayed by {dm} minutes.",
     "According to the departures board, is flight {fl} on time?"),
    ("A post on social media claims the beach at {pl} is closed for swimming.",
     "The council's water-quality notice says swimming is banned at the {pl} beach this week.",
     "The council's water-quality notice says swimming is allowed at the {pl} beach this week.",
     "According to the council's notice, is swimming banned at the {pl} beach this week?"),
    ("{x} told the insurer that {s} had a smoke alarm fitted in {mon}.",
     "The installer's records show a smoke alarm fitted at {x}'s home in {mon}.",
     "The installer's records show no smoke alarm fitted at {x}'s home.",
     "According to the installer's records, was a smoke alarm fitted at {x}'s home in {mon}?"),
    ("{x} claims {s} was at work all day on {day}.",
     "The office entry system records {x} arriving at 8:55 a.m. and leaving at 5:30 p.m. on {day}.",
     "The office entry system has no record of {x} entering the building on {day}.",
     "According to the office entry system, was {x} at work on {day}?"),
    ("The shop assistant told {x} that the jacket was 30% off.",
     "The till receipt shows a 30% discount on the jacket.", "The till receipt shows the jacket at full price.",
     "According to the till receipt, was the jacket discounted?"),
    ("A driver says the barrier at the {pl} level crossing was up when the train passed.",
     "The rail operator's signal log shows the barrier up at that moment.",
     "The rail operator's signal log shows the barrier down at that moment.",
     "According to the signal log, was the barrier up when the train passed?"),
    ("The estate agent says the flat on {st} has {nb} bedrooms.",
     "The floor plan in the official survey shows {nb} bedrooms.",
     "The floor plan in the official survey shows {nb1} bedrooms.",
     "According to the official survey, does the flat have {nb} bedrooms?"),
    ("{x} remembers paying the parking fine in {mon}.",
     "The council's payment record shows the fine paid in {mon}.",
     "The council's payment record shows the fine still unpaid.",
     "According to the council's payment record, was the fine paid in {mon}?"),
]


@schema("claim_vs_record", 300)
def s_record(rng):
    claim, rp, rn, q = rng.choice(RECORD)
    x, s, o, p = pick_person(rng)
    mon, mon2 = rng.sample(MONTHS, 2)
    day, day2 = rng.sample(WEEKDAYS[:5], 2)
    nb = rng.randint(2, 4)
    sl = dict(x=x, s=s, mon=mon, mon2=mon2, day=day, day2=day2, n=rng.randint(2, 180), st=rng.choice(STREETS),
              pl=rng.choice(PLACES), car=rng.choice(CARS), yr=rng.randint(2015, 2025), form=rng.choice(FORMS),
              h=rng.randint(2, 30), d=rng.randint(1, 6), cafe=rng.choice(CAFES), d1=rng.randint(10, 30),
              d2=rng.randint(2, 28), team=rng.choice(TEAMS), k=nw(rng.randint(2, 4)),
              late=rng.choice(["12:40 a.m.", "1:30 a.m.", "2:15 a.m.", "12:05 a.m."]),
              early=rng.choice(["11:15 p.m.", "10:30 p.m.", "11:50 p.m.", "11:05 p.m."]),
              dd=rng.choice([4, 5, 6, 7, 8, 9]), t2=rng.choice(["10:30 a.m.", "9:30 a.m.", "11 a.m.", "8 a.m."]),
              fl=f"{rng.choice(['NR', 'QV', 'TX', 'LM'])}{rng.randint(100, 999)}", dm=rng.choice([20, 35, 40, 55, 90]),
              nb=nb, nb1=nb + rng.choice([-1, 1]))
    claim, rp, rn, q = (t.format(**sl) for t in (claim, rp, rn, q))
    Pa = "P"
    rows = [(f"{cap(claim)} {rp}", Pa, "yes"), (f"{cap(claim)} {rn}", NOT(Pa), "no")]
    rng.shuffle(rows)
    return [mk(t, q, "true", "conflicting_evidence", [pr], Pa, g, "rec_pos" if g == "yes" else "rec_neg")
            for t, pr, g in rows]


# ================================================================================================ S26 sarcasm markers
SARC_CONV = [
    ("Team chat rule: a message that ends in /s is sarcastic, and its writer means the opposite of what the words say.",
     " /s"),
    ("Forum convention: [sarcasm] at the end of a post means the poster means the opposite of the literal words.",
     " [sarcasm]"),
    ("In this group chat, people add #sarcasm to a message when they mean the opposite of what it literally says.",
     " #sarcasm"),
    ("House style for this review board: a comment tagged (sarcastic) means the reverse of its literal wording.",
     " (sarcastic)"),
]
SARC_P = [
    ("The 8:15 train was on time today.", "The 8:15 train was not on time today.", "the 8:15 train was on time today"),
    ("The update fixed the login bug.", "The update did not fix the login bug.", "the update fixed the login bug"),
    ("The new coffee machine makes good coffee.", "The new coffee machine does not make good coffee.",
     "the new coffee machine makes good coffee"),
    ("The car park had plenty of free spaces this morning.",
     "The car park did not have plenty of free spaces this morning.",
     "the car park had plenty of free spaces this morning"),
    ("The quarterly report is easy to read.", "The quarterly report is not easy to read.",
     "the quarterly report is easy to read"),
    ("The client loved the demo.", "The client did not love the demo.", "the client loved the demo"),
    ("The air conditioning in Room 4 works.", "The air conditioning in Room 4 does not work.",
     "the air conditioning in Room 4 works"),
    ("The landlord fixed the leak quickly.", "The landlord did not fix the leak quickly.",
     "the landlord fixed the leak quickly"),
    ("IT sorted out the printer ticket fast.", "IT did not sort out the printer ticket fast.",
     "IT sorted out the printer ticket fast"),
    ("The canteen food has improved.", "The canteen food has not improved.", "the canteen food has improved"),
    ("The printer on floor 3 is working.", "The printer on floor 3 is not working.",
     "the printer on floor 3 is working"),
    ("The fire drill went smoothly.", "The fire drill did not go smoothly.", "the fire drill went smoothly"),
    ("The lift is fixed.", "The lift is not fixed.", "the lift is fixed"),
    ("The new rota makes things simpler.", "The new rota does not make things simpler.",
     "the new rota makes things simpler"),
    ("The bus came on time today.", "The bus did not come on time today.", "the bus came on time today"),
    ("The shared drive is well organised.", "The shared drive is not well organised.",
     "the shared drive is well organised"),
    ("Customer support answered the phone quickly.", "Customer support did not answer the phone quickly.",
     "customer support answered the phone quickly"),
    ("The roadworks finished on schedule.", "The roadworks did not finish on schedule.",
     "the roadworks finished on schedule"),
    ("This hotel room is quiet.", "This hotel room is not quiet.", "the hotel room is quiet"),
    ("The delivery driver was careful with the parcel.", "The delivery driver was not careful with the parcel.",
     "the delivery driver was careful with the parcel"),
    ("The new app is easy to use.", "The new app is not easy to use.", "the new app is easy to use"),
    ("The meeting started on time.", "The meeting did not start on time.", "the meeting started on time"),
]


@schema("sarcasm_marker", 400)
def s_sarcasm(rng):
    conv, mark = rng.choice(SARC_CONV)
    pos_s, neg_s, qclause = rng.choice(SARC_P)
    x, y = [p[0] for p in rng.sample(PEOPLE, 2)]
    literal_pos = rng.random() < 0.5
    msg = pos_s if literal_pos else neg_s
    var = rng.choice(["single", "single", "two_msgs"])
    K, L, Mn = "K", "L", "M"
    base_prem = [lit(L, literal_pos), IMP(K, ("iff", Mn, NOT(L))), IMP(NOT(K), ("iff", Mn, L))]
    out = []
    other = None
    if var == "two_msgs":
        o_pos, o_neg, _ = rng.choice([sp for sp in SARC_P if sp[2] != qclause])
        other = f"{y}: {o_pos if rng.random() < 0.5 else o_neg}{mark}"
    first = rng.random() < 0.5
    for marked in (False, True):
        m = f"{x}: {msg}{mark if marked else ''}"
        lines = [m, other] if other and first else ([other, m] if other else [m])
        st = conv + "\n" + "\n".join(lines)
        meant = (not literal_pos) if marked else literal_pos
        out.append(mk(st, f"Does {x} mean that {qclause}?", "meaning", "sarcasm", base_prem + [lit(K, marked)], Mn,
                      "yes" if meant else "no", f"{var}/{'pos' if literal_pos else 'neg'}_literal"))
    rng.shuffle(out)
    return out


# ================================================================================================ S27 if vs since
IFSINCE = [
    ("the council approves the budget on Thursday", "the council approved the budget on Thursday",
     "the library will extend its opening hours"),
    ("the supplier delivers the parts by Monday", "the supplier delivered the parts by Monday",
     "the production line will restart on Tuesday"),
    ("the board signs off on the plan", "the board signed off on the plan", "the new branch will open in March"),
    ("the forecast storm arrives", "the forecast storm arrived", "the ferry will not run tomorrow"),
    ("enough volunteers sign up", "enough volunteers signed up", "the beach clean-up will go ahead on Saturday"),
    ("the landlord agrees", "the landlord agreed", "{x} will repaint the kitchen"),
    ("the building passes its fire inspection", "the building passed its fire inspection",
     "tenants will be able to move in next week"),
    ("the grant is approved", "the grant was approved", "the lab will hire two technicians"),
    ("the union accepts the offer", "the union accepted the offer", "the strike will be called off"),
    ("the client pays the deposit", "the client paid the deposit", "the design work will start on 1 June"),
    ("the trial results are positive", "the trial results were positive",
     "the clinic will offer the treatment from spring"),
    ("the road closure ends on Friday", "the road closure ended on Friday",
     "the number 7 bus will return to its usual route"),
    ("the price of steel falls", "the price of steel fell", "the builder will lower the quote"),
    ("the referee confirms the goal", "the referee confirmed the goal", "the Rovers will go top of the table"),
    ("the airline restores the route", "the airline restored the route", "the island will get daily flights again"),
    ("the school hires a new music teacher", "the school hired a new music teacher",
     "the choir will restart in autumn"),
    ("{x} passes the final exam", "{x} passed the final exam", "{x} will graduate in July"),
    ("the vet clears the horse to race", "the vet cleared the horse to race", "the horse will run on Saturday"),
    ("the ferry company adds a second boat", "the ferry company added a second boat",
     "waiting times at the {pl} terminal will get shorter"),
    ("the planning committee approves the extension", "the planning committee approved the extension",
     "{x}'s family will start building in May"),
    ("{x} gets the job in Lisbon", "{x} got the job in Lisbon", "{x} will move abroad in the autumn"),
    ("the bank lowers its rates", "the bank lowered its rates", "the café will be able to afford the new oven"),
    ("the orchestra finds a new conductor", "the orchestra found a new conductor", "the spring tour will go ahead"),
    ("the auditors sign off the accounts", "the auditors signed off the accounts",
     "the charity will publish its annual report next week"),
    ("{team} win on Saturday", "{team} won on Saturday", "{team} will be promoted"),
    ("the roofers finish on Friday", "the roofers finished on Friday", "the scaffolding will come down next week"),
    ("the city bans cars from the centre", "the city banned cars from the centre", "the market will expand onto {st}"),
    ("the supplier cuts its prices", "the supplier cut its prices", "the shop will lower the price of bread"),
    ("{x}'s visa comes through", "{x}'s visa came through", "{x} will start the new job on Monday"),
    ("the snow clears", "the snow cleared", "{pl} School will reopen tomorrow"),
    ("the landlord renews the lease", "the landlord renewed the lease", "the bookshop will stay on {st}"),
]
NONVER_CONN = ["If", "Provided that", "Assuming", "As soon as", "Once"]
VER_CONN = ["Since", "Because", "Given that"]


@schema("if_vs_since", 300)
def s_ifsince(rng):
    cp, cpast, res = rng.choice(IFSINCE)
    sl = dict(x=pick_person(rng)[0], pl=rng.choice(PLACES), st=rng.choice(STREETS), team=rng.choice(TEAMS))
    cp, cpast, res = cp.format(**sl), cpast.format(**sl), res.format(**sl)
    nc = "If" if rng.random() < 0.6 else rng.choice(NONVER_CONN)
    vc = "Since" if nc == "If" and rng.random() < 0.6 else rng.choice(VER_CONN)
    A, R = "A", "R"
    rows = [(f"{nc} {cp}, {res}.", [IMP(A, R)], "no"), (f"{vc} {cpast}, {res}.", [A, IMP(A, R)], "yes")]
    rng.shuffle(rows)
    q = cert_q(rng, rng.choice(["text", "announcement", "email"]), res)
    return [mk(t, q, "certain", "hypothetical", p, R, g, "nonveridical" if g == "no" else "veridical")
            for t, p, g in rows]


# ================================================================================================ S28 counterfactuals
CF = [
    ("If the team had scored one more goal, it would have qualified for the final.",
     "Because the team scored one more goal, it qualified for the final.", "the team qualified for the final"),
    ("Had the parcel been posted on Monday, it would have arrived in time.",
     "Because the parcel was posted on Monday, it arrived in time.", "the parcel arrived in time"),
    ("If {x} had renewed the permit, the car would not have been towed.",
     "Because {x} renewed the permit, the car was not towed.", "the car was not towed"),
    ("If the bridge had been inspected earlier, the crack would have been found before winter.",
     "Because the bridge was inspected earlier, the crack was found before winter.",
     "the crack was found before winter"),
    ("Had the council approved the budget, the library would have stayed open on Sundays.",
     "Because the council approved the budget, the library stayed open on Sundays.",
     "the library stayed open on Sundays"),
    ("If {x} had left ten minutes earlier, {s} would have caught the train.",
     "Because {x} left ten minutes earlier, {s} caught the train.", "{x} caught the train"),
    ("If the shop had ordered more stock, it would not have run out of umbrellas.",
     "Because the shop ordered more stock, it did not run out of umbrellas.",
     "the shop did not run out of umbrellas"),
    ("If the alarm had been set, the break-in would have been detected.",
     "Because the alarm was set, the break-in was detected.", "the break-in was detected"),
    ("Had the vote been held on Friday, the motion would have passed.",
     "Because the vote was held on Friday, the motion passed.", "the motion passed"),
    ("If {x} had backed up the laptop, the thesis draft would have been saved.",
     "Because {x} backed up the laptop, the thesis draft was saved.", "the thesis draft was saved"),
    ("If the forecast had been accurate, the festival would have been moved indoors.",
     "Because the forecast was accurate, the festival was moved indoors.", "the festival was moved indoors"),
    ("If the invoice had been paid on time, the supplier would have given a discount.",
     "Because the invoice was paid on time, the supplier gave a discount.", "the supplier gave a discount"),
    ("Had the goalkeeper stayed on the line, the penalty would have been saved.",
     "Because the goalkeeper stayed on the line, the penalty was saved.", "the penalty was saved"),
    ("If the patient had arrived an hour earlier, the clinic would have seen her that day.",
     "Because the patient arrived an hour earlier, the clinic saw her that day.",
     "the clinic saw the patient that day"),
    ("Without the rain, the match would have finished on time.",
     "Because there was no rain, the match finished on time.", "the match finished on time"),
    ("But for the strike, the order would have shipped on Tuesday.",
     "Because there was no strike, the order shipped on Tuesday.", "the order shipped on Tuesday"),
    ("If the invoice had been sent to the right address, it would have been paid on time.",
     "Because the invoice was sent to the right address, it was paid on time.", "the invoice was paid on time"),
    ("Had {x} checked the forecast, {s} would have taken an umbrella.",
     "Because {x} checked the forecast, {s} took an umbrella.", "{x} took an umbrella"),
    ("If the dam had been repaired last year, the valley would not have flooded.",
     "Because the dam was repaired last year, the valley did not flood.", "the valley did not flood"),
    ("If the bakery had opened on Sunday, it would have sold out.",
     "Because the bakery opened on Sunday, it sold out.", "the bakery sold out"),
    ("Had the first-choice goalkeeper been fit, {team} would have kept a clean sheet.",
     "Because the first-choice goalkeeper was fit, {team} kept a clean sheet.", "{team} kept a clean sheet"),
    ("If the software had been updated, the attack would have been blocked.",
     "Because the software was updated, the attack was blocked.", "the attack was blocked"),
    ("If {x} had booked earlier, {s} would have got a window seat.",
     "Because {x} booked earlier, {s} got a window seat.", "{x} got a window seat"),
    ("If the road had been gritted, the bus would not have skidded.",
     "Because the road was gritted, the bus did not skid.", "the bus did not skid"),
    ("Had the museum stayed open late, the school group would have seen the exhibition.",
     "Because the museum stayed open late, the school group saw the exhibition.", "the school group saw the exhibition"),
    ("If the landlord had fixed the gutter, the ceiling would not have been damaged.",
     "Because the landlord fixed the gutter, the ceiling was not damaged.", "the ceiling was not damaged"),
    ("If the train had not been delayed, {x} would have made the interview.",
     "Because the train was not delayed, {x} made the interview.", "{x} made the interview"),
    ("If {x} had not missed the deadline, the application would have been considered.",
     "Because {x} did not miss the deadline, the application was considered.", "{x}'s application was considered"),
    ("Had the samples been kept cold, the test results would have been valid.",
     "Because the samples were kept cold, the test results were valid.", "the test results were valid"),
    ("If the council had not cut the grant, the youth club would have stayed open.",
     "Because the council did not cut the grant, the youth club stayed open.", "the youth club stayed open"),
    ("If the referee had seen the foul, the goal would have been disallowed.",
     "Because the referee saw the foul, the goal was disallowed.", "the goal was disallowed"),
    ("If the heating had been left on, the pipes would not have frozen.",
     "Because the heating was left on, the pipes did not freeze.", "the pipes did not freeze"),
    ("Had the {pl} branch hired more staff, it would have opened on Sundays.",
     "Because the {pl} branch hired more staff, it opened on Sundays.", "the {pl} branch opened on Sundays"),
    ("If the bid had been submitted a day earlier, {co} would have won the contract.",
     "Because the bid was submitted a day earlier, {co} won the contract.", "{co} won the contract"),
]


@schema("counterfactual", 250)
def s_cf(rng):
    cf, fact, goal = rng.choice(CF)
    x, s, o, p = pick_person(rng)
    sl = dict(x=x, s=s, team=rng.choice(TEAMS), pl=rng.choice(PLACES), co=rng.choice(COMPANIES))
    cf, fact, goal = cap(cf.format(**sl)), cap(fact.format(**sl)), goal.format(**sl)
    A, R = "A", "R"
    rows = [(cf, [IMP(A, R), NOT(A)], "no"), (fact, [A, IMP(A, R)], "yes")]
    rng.shuffle(rows)
    q = cert_q(rng, "text", goal)
    return [mk(t, q, "certain", "hypothetical", pr, R, g, "counterfactual" if g == "no" else "factual")
            for t, pr, g in rows]


# ================================================================================================ S29 plan vs done
PLAN = [
    ("the council", "repave Elm Street in May", "repaved Elm Street in May"),
    ("the clinic", "extend its opening hours in June", "extended its opening hours in June"),
    ("{x}", "submit the grant application by Friday", "submitted the grant application by Friday"),
    ("the company", "open a second warehouse in Leeds", "opened a second warehouse in Leeds"),
    ("the school", "replace the gym floor over the summer", "replaced the gym floor over the summer"),
    ("the airline", "add a daily flight to Lisbon", "added a daily flight to Lisbon"),
    ("{x}", "pay back the loan in full", "paid back the loan in full"),
    ("the landlord", "fix the broken window", "fixed the broken window"),
    ("the museum", "return the statue to Greece", "returned the statue to Greece"),
    ("the club", "raise its membership fee", "raised its membership fee"),
    ("the bakery", "switch to paper bags", "switched to paper bags"),
    ("the hospital", "hire twenty new nurses", "hired twenty new nurses"),
    ("{x}", "move to Rotterdam", "moved to Rotterdam"),
    ("the city", "plant 500 trees along the river", "planted 500 trees along the river"),
    ("the band", "release a new album in March", "released a new album in March"),
    ("the factory", "cut its water use by half", "cut its water use by half"),
    ("{x}", "finish the report before the audit", "finished the report before the audit"),
    ("the utility", "replace the old water pipes on Hill Road", "replaced the old water pipes on Hill Road"),
]
PLAN_NV = ["{S} plans to {b}.", "{S} intends to {b}.", "{S} is scheduled to {b}.", "{S} was supposed to {b}.",
           "{S} was expected to {b}.", "{S} promised to {b}.", "{S} hopes to {b}.", "{S} tried to {b}.",
           "{S} agreed to {b}.", "{S} was about to {b}.", "{S} is considering whether to {b}.",
           "{S} has been asked to {b}."]
PLAN_V = ["{S} {p}.", "{S} managed to {b}.", "{S} finally {p}.", "{S} went ahead and {p}."]


@schema("plan_vs_done", 250)
def s_plan(rng):
    S, b, p = rng.choice(PLAN)
    S = S.format(x=pick_person(rng)[0])
    E = "E"
    rows = [(rng.choice(PLAN_NV).format(S=cap(S), b=b), [], "no"), (rng.choice(PLAN_V).format(S=cap(S), b=b, p=p),
                                                                    [E], "yes")]
    rng.shuffle(rows)
    q = cert_q(rng, "text", f"{S} {p}")
    return [mk(t, q, "certain", "hypothetical", pr or ["Plan"], E, g, "plan" if g == "no" else "done")
            for t, pr, g in rows]


# ================================================================================================ S30 modal may vs will
MODAL = [
    ("{x} is a passenger on the 6 p.m. flight.", "Passengers on the 6 p.m. flight may be asked to show ID at the gate.",
     "Passengers on the 6 p.m. flight will all be asked to show ID at the gate.",
     "{x} will be asked to show ID at the gate"),
    ("{x} works at the Leeds office.", "Staff at the Leeds office might be moved to the new building in spring.",
     "All staff at the Leeds office will be moved to the new building in spring.",
     "{x} will be moved to the new building in spring"),
    ("{x} is a member of the gym.", "Members may receive a free training session this month.",
     "Every member will receive a free training session this month.",
     "{x} will receive a free training session this month"),
    ("{x} ordered the blue sofa.", "Orders for the blue sofa could be delayed by two weeks.",
     "Orders for the blue sofa will all be delayed by two weeks.", "{x}'s order will be delayed by two weeks"),
    ("{x} is flying to Rome on Friday.", "Flights to Rome on Friday may be cancelled because of the strike.",
     "All flights to Rome on Friday will be cancelled because of the strike.", "{x}'s flight will be cancelled"),
    ("{x} lives on Birch Road.", "Houses on Birch Road may lose water for a few hours on Tuesday.",
     "Every house on Birch Road will lose water for a few hours on Tuesday.",
     "{x}'s house will lose water for a few hours on Tuesday"),
    ("{x} is on the waiting list.", "People on the waiting list might be offered a place next term.",
     "Everyone on the waiting list will be offered a place next term.", "{x} will be offered a place next term"),
    ("{x} bought a ticket for Saturday's concert.", "Ticket holders for Saturday's concert may get a partial refund.",
     "Every ticket holder for Saturday's concert will get a partial refund.", "{x} will get a partial refund"),
    ("{x} drives a van registered before 2015.",
     "Vans registered before 2015 may have to pay the new emissions charge.",
     "Vans registered before 2015 will all have to pay the new emissions charge.",
     "{x}'s van will have to pay the new emissions charge"),
    ("{x} is a Year 10 student.", "Year 10 students can be chosen for the exchange trip.",
     "Every Year 10 student will go on the exchange trip.", "{x} will go on the exchange trip"),
    ("{x} is a customer of the bank.", "Customers of the bank could see a small rise in fees next year.",
     "Every customer of the bank will see a small rise in fees next year.",
     "{x} will see a small rise in fees next year"),
    ("{x}'s parcel was sent by economy post.", "Parcels sent by economy post can take ten days to arrive.",
     "Parcels sent by economy post always take ten days to arrive.", "{x}'s parcel will take ten days to arrive"),
    ("{x} is a patient at the Riverside surgery.", "Patients at the Riverside surgery may be moved to a new doctor.",
     "All patients at the Riverside surgery will be moved to a new doctor.", "{x} will be moved to a new doctor"),
    ("{x} rents a flat in Block B.", "Tenants in Block B might get new windows this year.",
     "Every tenant in Block B will get new windows this year.", "{x} will get new windows this year"),
    ("{x} is a customer on the Basic plan.", "Customers on the Basic plan might see adverts in the app.",
     "Customers on the Basic plan will all see adverts in the app.", "{x} will see adverts in the app"),
    ("{x} is booked on the 7 a.m. ferry to {pl}.", "The 7 a.m. ferry to {pl} may be cancelled if the wind picks up.",
     "The 7 a.m. ferry to {pl} will be cancelled.", "{x}'s ferry will be cancelled"),
    ("{x} works on the night shift.", "Night-shift workers may be asked to work on Christmas Day.",
     "All night-shift workers will be asked to work on Christmas Day.", "{x} will be asked to work on Christmas Day"),
    ("{x} parks in the east car park.", "Cars in the east car park could be moved during the resurfacing.",
     "All cars in the east car park will be moved during the resurfacing.",
     "{x}'s car will be moved during the resurfacing"),
    ("{x} is a student at the {pl} campus.", "Students at the {pl} campus may have classes moved online next week.",
     "Every student at the {pl} campus will have classes moved online next week.",
     "{x} will have classes moved online next week"),
    ("{x} has a pension with the company.", "Pension holders might receive a statement in June.",
     "Every pension holder will receive a statement in June.", "{x} will receive a statement in June"),
    ("{x} submitted a claim last month.", "Claims submitted last month can take six weeks to process.",
     "Claims submitted last month will all take six weeks to process.", "{x}'s claim will take six weeks to process"),
    ("{x} is running in Sunday's race.", "Runners in Sunday's race may be asked to take a drug test.",
     "Every runner in Sunday's race will be asked to take a drug test.", "{x} will be asked to take a drug test"),
    ("{x} lives in the {pl} flood zone.", "Homes in the {pl} flood zone might be offered free sandbags.",
     "Every home in the {pl} flood zone will be offered free sandbags.", "{x}'s home will be offered free sandbags"),
    ("{x} drives for the delivery firm.", "The firm's drivers could be switched to electric vans next year.",
     "All of the firm's drivers will be switched to electric vans next year.",
     "{x} will be switched to an electric van next year"),
    ("{x} is on the waiting list for {pl} School.", "Children on the waiting list may be offered places in September.",
     "Every child on the waiting list will be offered a place in September.", "{x} will be offered a place in September"),
    ("{x} ordered a sofa during the sale.", "Sale orders may take longer to deliver.",
     "Every sale order will take longer to deliver.", "{x}'s order will take longer to deliver"),
    ("{x} holds a season ticket.", "Season-ticket holders might be invited to the open training day.",
     "Every season-ticket holder will be invited to the open training day.",
     "{x} will be invited to the open training day"),
]


@schema("modal_may_will", 250)
def s_modal(rng):
    mem, weak, strong, goal = rng.choice(MODAL)
    x = pick_person(rng)[0]
    pl = rng.choice(PLACES)
    mem, goal, weak, strong = (t.format(x=x, pl=pl) for t in (mem, goal, weak, strong))
    M, G = "M", "G"
    order = rng.random() < 0.5
    rows = [(weak, [M], "no"), (strong, [M, IMP(M, G)], "yes")]
    rng.shuffle(rows)
    q = cert_q(rng, "text", goal)
    return [mk(f"{r} {mem}" if order else f"{mem} {r}", q, "certain", "hypothetical", pr, G, g,
               "may" if g == "no" else "will") for r, pr, g in rows]


# ================================================================================================ S31 closed vs open lists
CARDS = ["Visa", "Mastercard", "American Express", "Discover", "JCB", "UnionPay", "Maestro", "Diners Club"]
ALLERGENS = ["milk", "eggs", "celery", "mustard", "wheat", "soya", "sesame", "peanuts", "fish", "tree nuts"]
LANGS = ["English", "Spanish", "Polish", "Arabic", "Portuguese", "Urdu", "French", "Somali", "Mandarin", "Romanian"]
CITIES = ["Lisbon", "Madrid", "Rome", "Oslo", "Vienna", "Prague", "Dublin", "Athens", "Warsaw", "Zurich", "Porto",
          "Nice", "Seville", "Krakow"]
SIZES = ["XS", "S", "M", "L", "XL", "XXL"]
COURSES = ["Spanish", "pottery", "bookkeeping", "first aid", "photography", "welding", "Italian", "coding",
           "furniture restoration", "creative writing"]
STOPS = ["the hospital", "the train station", "the university", "the retail park", "the stadium", "the ferry port",
         "the old town", "the airport", "the leisure centre"]
LISTS = [
    ("The flood warning covers only these areas: {lst}.", "The flood warning covers several areas, including {lst}.",
     "The flood warning covers {lst}, and no other areas.", PLACES, "{c} is not covered by the flood warning"),
    ("The shop accepts only these cards: {lst}.", "The shop accepts several cards, including {lst}.",
     "The shop accepts {lst}, and no other cards.", CARDS, "the shop does not accept {c}"),
    ("The soup contains only these allergens: {lst}.", "The soup's allergens include {lst}.",
     "The soup contains {lst}, and no other allergens.", ALLERGENS, "the soup does not contain {c}"),
    ("The helpline is available only in these languages: {lst}.",
     "The helpline is available in several languages, including {lst}.",
     "The helpline is available in {lst}, and in no other language.", LANGS,
     "the helpline is not available in {c}"),
    ("From this airport, the airline flies only to {lst}.",
     "From this airport, the airline flies to several cities, including {lst}.",
     "From this airport, the airline flies to {lst}, and nowhere else.", CITIES,
     "the airline does not fly from this airport to {c}"),
    ("The jacket is in stock only in these sizes: {lst}.",
     "The jacket is in stock in several sizes, including {lst}.",
     "The jacket is in stock in sizes {lst}, and in no other size.", SIZES,
     "the jacket is not in stock in size {c}"),
    ("The evening school offers only these courses: {lst}.",
     "The evening school offers several courses, including {lst}.",
     "The evening school offers {lst}, and no other courses.", COURSES, "the evening school does not offer {c}"),
    ("The night bus stops only at {lst}.", "The night bus stops at several places, including {lst}.",
     "The night bus stops at {lst}, and nowhere else.", STOPS, "the night bus does not stop at {c}"),
    ("The approved suppliers are only these: {lst}.", "The approved suppliers include {lst}.",
     "The approved suppliers are {lst}, and no other company is approved.", COMPANIES,
     "{c} is not an approved supplier"),
]


@schema("closed_vs_open_list", 300)
def s_lists(rng):
    only_s, incl_s, only2, pool, goal = rng.choice(LISTS)
    k = rng.randint(2, 4)
    picks = rng.sample(pool, k + 1)
    lst, c = picks[:k], picks[k]
    ltxt = join(lst)
    closed = only_s if rng.random() < 0.6 else only2
    atoms = [f"i{i}" for i in range(k)]
    C = "c"
    rows = [(closed.format(lst=ltxt), atoms + [NOT(C)], "yes"), (incl_s.format(lst=ltxt), atoms, "no")]
    rng.shuffle(rows)
    q = cert_q(rng, rng.choice(["text", "notice", "information given"]), goal.format(c=c))
    return [mk(t, q, "certain", "missing_info", pr, NOT(C), g, "closed" if g == "yes" else "open") for t, pr, g in rows]


# ================================================================================================ S32 and / or / at least two
REQ = [
    ("To qualify for the energy rebate, a household must {expr}.", "{x}'s household",
     [("own an electric car", "owns an electric car", "does not own an electric car"),
      ("have rooftop solar panels", "has rooftop solar panels", "does not have rooftop solar panels"),
      ("be inside the city limits", "is inside the city limits", "is outside the city limits")]),
    ("To be shortlisted, an applicant must {expr}.", "{x}",
     [("hold a driving licence", "holds a driving licence", "does not hold a driving licence"),
      ("have a first-aid certificate", "has a first-aid certificate", "does not have a first-aid certificate"),
      ("speak Spanish", "speaks Spanish", "does not speak Spanish")]),
    ("To be eligible for the scholarship, a student must {expr}.", "{x}",
     [("have a grade average above 80", "has a grade average above 80", "has a grade average of 80 or below"),
      ("live in the county", "lives in the county", "does not live in the county"),
      ("be enrolled full-time", "is enrolled full-time", "is enrolled part-time")]),
    ("To lead a volunteer group, a person must {expr}.", "{x}",
     [("be over 21", "is over 21", "is not over 21"),
      ("have a background check on file", "has a background check on file", "has no background check on file"),
      ("have completed the training day", "has completed the training day", "has not completed the training day")]),
    ("To get the starter loan, a business must {expr}.", "{x}'s bakery",
     [("be registered locally", "is registered locally", "is not registered locally"),
      ("have fewer than ten employees", "has fewer than ten employees", "has ten or more employees"),
      ("have been trading for at least a year", "has been trading for at least a year",
       "has been trading for less than a year")]),
    ("To get a resident parking permit, a driver must {expr}.", "{x}",
     [("live on the street", "lives on the street", "does not live on the street"),
      ("have a car registered at the address", "has a car registered at the address",
       "does not have a car registered at the address"),
      ("have no unpaid parking fines", "has no unpaid parking fines", "has unpaid parking fines")]),
    ("To join the advanced climbing group, a member must {expr}.", "{x}",
     [("have climbed for two years", "has climbed for two years", "has not climbed for two years"),
      ("own a harness", "owns a harness", "does not own a harness"),
      ("have passed the belay test", "has passed the belay test", "has not passed the belay test")]),
    ("To adopt a dog from the shelter, an applicant must {expr}.", "{x}",
     [("have a fenced garden", "has a fenced garden", "does not have a fenced garden"),
      ("be at home most days", "is at home most days", "is not at home most days"),
      ("have no other dogs", "has no other dogs", "already has another dog")]),
    ("To get the young person's rail discount, a traveller must {expr}.", "{x}",
     [("be under 26", "is under 26", "is not under 26"),
      ("hold a student card", "holds a student card", "does not hold a student card"),
      ("travel off-peak", "travels off-peak", "travels at peak times")]),
    ("To enter the marathon, a runner must {expr}.", "{x}",
     [("be at least 18", "is at least 18", "is under 18"),
      ("have a medical certificate", "has a medical certificate", "does not have a medical certificate"),
      ("have finished a half marathon", "has finished a half marathon", "has never finished a half marathon")]),
    ("To receive the arts grant, a project must {expr}.", "{x}'s mural project",
     [("take place in the region", "takes place in the region", "does not take place in the region"),
      ("involve local artists", "involves local artists", "does not involve local artists"),
      ("cost under $20,000", "costs under $20,000", "costs $20,000 or more")]),
    ("To get the safe-driver discount, a policyholder must {expr}.", "{x}",
     [("have made no claims in five years", "has made no claims in five years",
       "has made a claim in the last five years"),
      ("drive under 8,000 miles a year", "drives under 8,000 miles a year", "drives 8,000 miles a year or more"),
      ("have a dashcam fitted", "has a dashcam fitted", "does not have a dashcam fitted")]),
]


@schema("and_or_requirement", 340)
def s_req(rng):
    rule_t, subj_t, conds = rng.choice(REQ)
    x = pick_person(rng)[0]
    subj = subj_t.format(x=x)
    atoms = ["A", "B", "C"]
    t = rng.choice(["and_or", "all_any", "atleast2", "and_fact"])
    order = list(range(3))
    rng.shuffle(order)
    cs = [conds[i] for i in order]

    def scen(vals, idx):
        parts = [cs[i][1] if vals[i] else cs[i][2] for i in idx]
        return f"{cap(subj)} {join(parts)}."

    rows = []
    if t == "and_or":
        vals = [True, False, rng.random() < 0.5]
        if rng.random() < 0.5:
            vals[0], vals[1] = vals[1], vals[0]
        e_and = f"{cs[0][0]} and {cs[1][0]}" if rng.random() < 0.5 else f"both {cs[0][0]} and {cs[1][0]}"
        e_or = f"{cs[0][0]} or {cs[1][0]}"
        idx = [0, 1, 2] if rng.random() < 0.3 else [0, 1]
        s = scen(vals, idx)
        prem = [lit(atoms[i], vals[i]) for i in idx]
        rows = [(rule_t.format(expr=e_and), s, prem, AND("A", "B"), "no"),
                (rule_t.format(expr=e_or), s, prem, OR("A", "B"), "yes")]
    elif t == "all_any":
        k = rng.choice([1, 2])
        vals = [True] * k + [False] * (3 - k)
        rng.shuffle(vals)
        e_all = f"meet all three of these conditions: {join([c[0] for c in cs], 'and')}"
        e_any = f"meet at least one of these conditions: {join([c[0] for c in cs], 'or')}"
        s = scen(vals, [0, 1, 2])
        prem = [lit(a, v) for a, v in zip(atoms, vals)]
        rows = [(rule_t.format(expr=e_all), s, prem, CNT("==", 3, atoms), "no"),
                (rule_t.format(expr=e_any), s, prem, CNT(">=", 1, atoms), "yes")]
    elif t == "atleast2":
        e = f"meet at least two of these three conditions: {join([c[0] for c in cs], 'and')}"
        vals = [True, True, False]
        rng.shuffle(vals)
        i = rng.choice([j for j in range(3) if vals[j]])
        vals2 = list(vals)
        vals2[i] = False
        g = CNT(">=", 2, atoms)
        rows = [(rule_t.format(expr=e), scen(vals, [0, 1, 2]), [lit(a, v) for a, v in zip(atoms, vals)], g, "yes"),
                (rule_t.format(expr=e), scen(vals2, [0, 1, 2]), [lit(a, v) for a, v in zip(atoms, vals2)], g, "no")]
    else:
        e = f"{cs[0][0]} and {cs[1][0]}"
        vals = [True, True]
        i = rng.randrange(2)
        vals2 = list(vals)
        vals2[i] = False
        g = AND("A", "B")
        rows = [(rule_t.format(expr=e), scen(vals, [0, 1]), [lit(a, v) for a, v in zip(atoms, vals)], g, "yes"),
                (rule_t.format(expr=e), scen(vals2, [0, 1]), [lit(a, v) for a, v in zip(atoms, vals2)], g, "no")]
    rng.shuffle(rows)
    q = rng.choice([f"Does {subj} meet this requirement?", f"Does {subj} meet the stated requirement?",
                    f"Does {subj} satisfy the requirement as written?"])
    edge = "numeric" if t == "atleast2" else "quantifier"
    return [mk(f"{r} {s}", q, "meets", edge, pr, g_, gold, t) for r, s, pr, g_, gold in rows]


# ================================================================================================ S33 De Morgan facts
TIMES = ["7:00", "8:30", "9:00", "10:15", "11:00", "12:45", "14:00", "15:30", "17:10", "18:40"]
SURN = ["Okafor", "Lindqvist", "Moreau", "Haddad", "Novak", "Chen", "Adeyemi", "Kowalski", "Brennan", "Tanaka",
        "Silva", "Mensah", "Petrov", "Ibarra"]
DISHES2 = ["the soup", "the curry", "the salad", "the risotto", "the stew", "the pasta bake", "the dal", "the pie",
           "the noodle bowl", "the flatbread"]


def dm_pair(rng, kind):
    if kind == "class":
        d1, d2 = rng.sample(WEEKDAYS[:5], 2)
        c = rng.choice(["yoga", "pottery", "Spanish", "spin", "first-aid", "life-drawing"])
        return f"the {d1} {c} class", f"the {d2} {c} class"
    if kind == "flight":
        t1, t2 = rng.sample(TIMES, 2)
        city = rng.choice(["Lisbon", "Oslo", "Rome", "Dublin", "Prague", "Vienna"])
        return f"the {t1} flight to {city}", f"the {t2} flight to {city}"
    if kind == "room":
        c1, c2 = rng.sample(["Blue", "Green", "Red", "Yellow", "Oak", "Cedar", "Garden", "River"], 2)
        return f"the {c1} Room", f"the {c2} Room"
    if kind == "dish":
        return tuple(rng.sample(DISHES2, 2))
    if kind == "lift":
        a, b = rng.sample(["north", "south", "east", "west"], 2)
        return f"the {a} lift in Block {rng.choice('ABCDE')}", f"the {b} lift"
    if kind == "branch":
        a, b = rng.sample(STREETS, 2)
        return f"the {a} branch", f"the {b} branch"
    if kind == "doctor":
        a, b = rng.sample(SURN, 2)
        return f"Dr {a}", f"Dr {b}"
    if kind == "van":
        a, b = rng.sample(["red", "white", "blue", "grey", "green", "black"], 2)
        return f"the {a} van", f"the {b} van"
    if kind == "workshop":
        a, b = rng.sample(["spring", "summer", "autumn", "winter"], 2)
        return f"the {a} {rng.choice(['writing', 'coding', 'design', 'grant-writing'])} workshop", f"the {b} workshop"
    if kind == "road":
        a, b = rng.sample(STREETS, 2)
        return a, b
    if kind == "show":
        t1, t2 = rng.sample(["5 p.m.", "7 p.m.", "8:30 p.m.", "9 p.m.", "2 p.m."], 2)
        return f"the {t1} show", f"the {t2} show"
    if kind == "shift":
        a, b = rng.sample(["morning", "afternoon", "night", "weekend"], 2)
        return f"the {a} shift at the {rng.choice(PLACES)} depot", f"the {b} shift"
    if kind == "wing":
        a, b = rng.sample(["left", "right", "east", "west", "north"], 2)
        return f"the {a} wing of the {rng.choice(PLACES)} school", f"the {b} wing"
    if kind == "court":
        a, b = rng.sample(["1", "2", "3", "4", "5"], 2)
        return f"court {a}", f"court {b}"
    raise ValueError(kind)


DMF = [
    ("class", "be", "full"), ("flight", "be", "sold out"), ("room", "be", "available on Friday"),
    ("dish", "do", ("contain nuts", "contains nuts")), ("lift", "be", "working"), ("branch", "be", "open on Sunday"),
    ("doctor", "be", "on call tonight"), ("van", "be", "booked for Monday"), ("workshop", "be", "fully funded"),
    ("road", "be", "closed this weekend"), ("show", "be", "sold out"), ("dish", "do", ("contain dairy",
                                                                                       "contains dairy")),
    ("shift", "be", "short-staffed"), ("wing", "do", ("need new windows", "needs new windows")),
    ("court", "be", "free on Saturday morning"), ("room", "do", ("have a projector", "has a projector")),
]


def dm_forms(A, B, kind, pr):
    if kind == "be":
        return dict(notboth=f"{A} and {B} are not both {pr}.", neither=f"Neither {A} nor {B} is {pr}.",
                    itnot_either=f"It is not the case that either {A} or {B} is {pr}.",
                    itnot_both=f"It is not the case that both {A} and {B} are {pr}.",
                    posA=f"{A} is {pr}.", negA=f"{A} is not {pr}.", negB=f"{B} is not {pr}")
    vb, v3 = pr
    return dict(notboth=f"{A} and {B} do not both {vb}.", neither=f"Neither {A} nor {B} {v3}.",
                itnot_either=f"It is not the case that either {A} or {B} {v3}.",
                itnot_both=f"It is not the case that both {A} and {B} {vb}.",
                posA=f"{A} {v3}.", negA=f"{A} does not {vb}.", negB=f"{B} does not {vb}")


@schema("demorgan_facts", 300)
def s_dmf(rng):
    ek, kind, pr = rng.choice(DMF)
    A, B = dm_pair(rng, ek)
    f = dm_forms(A, B, kind, pr)
    a, b = "a", "b"
    var = rng.choice(["notboth_fact", "neither_vs_notboth", "itnot"])
    if var == "notboth_fact":
        rows = [(f"{cap(f['notboth'])} {cap(f['posA'])}", [NOT(AND(a, b)), a], "yes"),
                (f"{cap(f['notboth'])} {cap(f['negA'])}", [NOT(AND(a, b)), NOT(a)], "no")]
    elif var == "neither_vs_notboth":
        rows = [(cap(f["neither"]), [AND(NOT(a), NOT(b))], "yes"), (cap(f["notboth"]), [NOT(AND(a, b))], "no")]
    else:
        rows = [(f["itnot_either"], [NOT(OR(a, b))], "yes"), (f["itnot_both"], [NOT(AND(a, b))], "no")]
    rng.shuffle(rows)
    q = cert_q(rng, "text", f["negB"])
    return [mk(t, q, "certain", "negation", pr_, NOT(b), g, var) for t, pr_, g in rows]


# ================================================================================================ S34 'not ... because' scope
BECAUSE = [
    ("the {tm} flight to {city}", "cancelled", "the storm", "a crew shortage", "the storm had passed by noon"),
    ("{day}'s match against {team}", "postponed", "the rain", "a scheduling clash",
     "the rain stopped an hour before kick-off"),
    ("the corner shop on {st}", "closed early", "the holiday", "a power cut", "the holiday rules did not apply to it"),
    ("{x}'s loan application", "rejected", "{p} income", "a missing signature", "{p} income was high enough"),
    ("the {pl} concert", "called off", "the singer's illness", "a problem with the venue",
     "the singer recovered in time"),
    ("{pl} Primary School", "closed on {day}", "the snow", "a burst pipe", "the snow had melted overnight"),
    ("the furniture order from {co}", "delayed", "the strike", "a stock shortage", "the strike ended before dispatch"),
    ("{st}", "closed to traffic", "the parade", "emergency repairs", "the parade used a different route"),
    ("the {tm} train to {pl}", "held at the platform", "the signal fault", "a medical emergency on board",
     "the signal fault was fixed in time"),
    ("the {subj} exam", "rescheduled", "the fire alarm", "a clash with a public holiday",
     "the fire alarm was only a test"),
    ("the {tm} ferry to {island}", "cancelled", "the high winds", "an engine fault", "the wind dropped before sunrise"),
    ("the {dept} team's party", "moved online", "the heating failure", "low numbers",
     "the heating was repaired in time"),
    ("the {pl} warehouse", "evacuated", "the smoke alarm", "a gas leak", "the smoke alarm was a false alarm"),
    ("the outdoor screening in {pl} Park", "cancelled", "the cold", "a broken projector", "the evening turned out mild"),
    ("the {topic} planning meeting", "postponed", "the director's absence", "a clash with the audit",
     "the director joined by video"),
    ("{x}'s flight home", "diverted", "the fog", "a medical emergency on board", "the fog lifted before landing"),
    ("the {pl} farmers' market", "cut short", "the heatwave", "a fire alarm in the hall",
     "the heatwave broke the night before"),
]
ISLANDS = ["Arran", "Mull", "Skye", "Islay", "Bute", "Harris", "Jura", "Coll"]
DEPTS = ["design", "finance", "sales", "support", "legal", "research", "logistics"]


@schema("because_scope", 220)
def s_because(rng):
    S, pp, A, B, reason = rng.choice(BECAUSE)
    x, s, o, p = pick_person(rng)
    sl = dict(x=x, p=p, tm=rng.choice(["6:40", "7:15", "8:05", "9:30", "11:20", "13:45", "16:10", "18:25"]),
              city=rng.choice(["Oslo", "Lisbon", "Dublin", "Rome", "Vienna", "Madrid"]), day=rng.choice(WEEKDAYS),
              team=rng.choice(TEAMS), st=rng.choice(STREETS), pl=rng.choice(PLACES), co=rng.choice(COMPANIES),
              subj=rng.choice(SUBJECTS), island=rng.choice(ISLANDS), dept=rng.choice(DEPTS),
              topic=rng.choice(["budget", "summer fair", "office move", "rebranding", "website"]))
    S, pp, A, reason = S.format(**sl), pp.format(**sl), A.format(**sl), reason.format(**sl)
    E = "E"
    rows = [(f"{cap(S)} was not {pp} because of {A}; it was {pp} because of {B}.", E, "yes"),
            (f"{cap(S)} was not {pp}, because {reason}.", NOT(E), "no")]
    rng.shuffle(rows)
    q = f"Was {S} {pp}?"
    return [mk(t, q, "true", "ambiguous", [pr], E, g, "other_cause" if g == "yes" else "not_happened")
            for t, pr, g in rows]


# ================================================================================================ S35 'all ... not' scope
ALLNOT = [
    # items, where (with {pl}), instance templates, what a working one does
    ("lifts", ["in the {pl} office tower", "at {pl} station", "in the {pl} shopping centre"],
     ["the lift by the main entrance", "the lift next to the car park", "lift {n}"], "runs"),
    ("printers", ["in the {pl} library", "on the second floor", "in the {pl} office"],
     ["the printer by reception", "the colour printer", "printer {n}"], "prints"),
    ("ticket machines", ["at {pl} station", "in the {pl} car park"],
     ["the machine by the south exit", "the machine near the barrier", "machine {n}"], "takes payments"),
    ("projectors", ["in the {pl} conference centre", "on the teaching floor"],
     ["the projector in Room {n}", "the projector in the main hall"], "shows a picture"),
    ("charging points", ["at the {pl} retail park", "on {st}"],
     ["the charging point nearest the gate", "charging point {n}"], "charges cars"),
    ("coffee machines", ["in the {pl} office", "on the staff floors"],
     ["the machine on floor {n}", "the machine by the kitchen"], "makes coffee"),
    ("card readers", ["in the {pl} supermarket", "at the {pl} market hall"],
     ["the reader at till {n}", "the reader by the entrance"], "accepts cards"),
    ("washing machines", ["in the {pl} student halls", "in the launderette on {st}"],
     ["the machine by the window", "machine {n}"], "runs"),
    ("water fountains", ["in {pl} Park", "at the {pl} leisure centre"],
     ["the fountain by the gym", "the fountain near the playground"], "has water"),
    ("street lights", ["on {st}", "along the {pl} seafront"],
     ["the light outside number {n}", "the light by the bus stop"], "comes on at night"),
    ("self-checkout tills", ["in the {pl} supermarket", "at the {st} pharmacy"],
     ["the till nearest the door", "till {n}"], "scans items"),
    ("security cameras", ["at the {pl} depot", "in the {st} car park"],
     ["the camera over the back door", "camera {n}"], "records"),
    ("escalators", ["at {pl} station", "in the {pl} shopping centre"],
     ["the escalator to platform {n}", "the escalator by the food court"], "moves"),
    ("hand dryers", ["in the {pl} sports centre", "on the ground floor"],
     ["the dryer in the east washroom", "dryer {n}"], "blows warm air"),
]


@schema("all_not_scope", 220)
def s_allnot(rng):
    pl, wheres, insts, v3 = rng.choice(ALLNOT)
    sl = dict(pl=rng.choice(PLACES), st=rng.choice(STREETS), n=rng.randint(2, 14))
    where = rng.choice(wheres).format(**sl)
    inst = rng.choice(insts).format(**sl)
    n = rng.randint(3, 8)
    k = rng.randint(1, n - 1)
    W = "W"
    amb = f"All of the {pl} {where} are not working"
    if rng.random() < 0.7:
        rows = [(f"{amb}: not a single one of the {nw(n)} works at the moment.", NOT(W), "no"),
                (f"{amb}; to be precise, {nw(k)} of the {nw(n)} {'is' if k == 1 else 'are'} out of order, and {inst} "
                 f"still {v3}.", W, "yes")]
        var = "ambiguous_first"
    else:
        rows = [(f"None of the {nw(n)} {pl} {where} are working; {inst} is out of order too.", NOT(W), "no"),
                (f"Not all of the {nw(n)} {pl} {where} are working; {inst} still {v3}.", W, "yes")]
        var = "explicit"
    rng.shuffle(rows)
    q = f"Is {inst} working?"
    return [mk(t, q, "true", "ambiguous", [pr], W, g, var) for t, pr, g in rows]


# ================================================================================================ S36 still / no longer / not yet
ASPECT = [
    ("the bridge on {st}", "open to traffic", "closed to traffic", False),
    ("the car park on {st}", "free", "pay-and-display", False),
    ("the heating in the {side} wing of the {pl} office", "on", "off", False),
    ("the {col} jacket in size {sz}", "in stock", "out of stock", False),
    ("the {pl} council's booking website", "online", "offline", False),
    ("the lift in Block {L}", "in service", "out of service", False),
    ("dogs on {pl} beach", "allowed", "banned", True),
    ("the underpass at {st}", "open to pedestrians", "closed to pedestrians", False),
    ("the {side} entrance of the {pl} library", "unlocked", "locked", False),
    ("the {pl} swimming pool", "open", "closed", False),
    ("the water supply on {st}", "on", "cut off", False),
    ("the café terrace in {pl} Park", "open", "closed", False),
    ("the coastal trail near {pl}", "open", "closed", False),
    ("the northbound slip road at {pl}", "open", "closed", False),
    ("the staff canteen at the {pl} depot", "open", "closed", False),
    ("e-scooters in {pl} Park", "permitted", "prohibited", True),
    ("the ticket office at {pl} station", "open", "closed", False),
    ("the {pl} museum's west gallery", "open to visitors", "closed to visitors", False),
    ("the footpath along {st}", "open", "closed", False),
    ("barbecues on {pl} common", "allowed", "banned", True),
]


# form: (template, which adjective (P or N), value of the adjective's truth now)
AS_FORMS = {"still": ("{S} {be} still {A}.", True), "no_longer": ("{S} {be} no longer {A}.", False),
            "not_yet": ("{S} {be} not yet {A}.", False), "already": ("{S} {be} already {A}.", True),
            "again": ("{S} {be} {A} again.", True)}
AS_PAIRS = [(("still", "P"), ("still", "N")), (("no_longer", "N"), ("no_longer", "P")),
            (("not_yet", "P"), ("already", "P")), (("still", "N"), ("no_longer", "N")),
            (("still", "P"), ("no_longer", "P")), (("again", "P"), ("again", "N")),
            (("not_yet", "P"), ("no_longer", "N"))]


@schema("still_no_longer", 330)
def s_aspect(rng):
    S, Pw, Nw, plural = rng.choice(ASPECT)
    S = S.format(st=rng.choice(STREETS), pl=rng.choice(PLACES), side=rng.choice(["east", "west", "north", "south"]),
                 col=rng.choice(["blue", "green", "black", "red", "grey"]), sz=rng.choice(["S", "M", "L", "XL"]),
                 L=rng.choice("ABCDEFG"))
    be = "are" if plural else "is"
    f1, f2 = rng.choice(AS_PAIRS)
    Pa = "P"
    rows = []
    for form, which in (f1, f2):
        t, adj_true = AS_FORMS[form]
        adj = Pw if which == "P" else Nw
        p_now = adj_true if which == "P" else (not adj_true)
        rows.append((t.format(S=cap(S), be=be, A=adj), lit(Pa, p_now), "yes" if p_now else "no", f"{form}_{which}"))
    if rows[0][2] == rows[1][2]:
        return None
    rng.shuffle(rows)
    q = f"{'Are' if plural else 'Is'} {S} {Pw} now?"
    return [mk(t, q, "true", "temporal", [pr], Pa, g, v) for t, pr, g, v in rows]


# ================================================================================================ S38 implicative verbs
TASKS = ["renew the parking permit before it expired", "lock the storeroom on Friday evening",
         "submit the expense report by the deadline", "back up the database on Sunday",
         "book the venue for the awards night", "call the supplier about the late order",
         "pay the electricity bill in March", "switch off the kiln after the class", "send the invoice to the client",
         "update the price labels", "cancel the free trial before it renewed", "water the office plants during the holiday",
         "file the tax return on time", "attach the signed form to the application", "reset the alarm code",
         "order more printer paper", "confirm the hotel booking", "return the library books by the due date",
         "register for the conference", "sign the delivery note", "turn off the gas before leaving",
         "check the fire extinguishers in June", "update the emergency contact list", "feed the neighbour's cat on Tuesday"]
IMPL = {"managed to": True, "failed to": False, "remembered to": True, "forgot to": False, "neglected to": False,
        "did not fail to": True, "did not forget to": True, "did not neglect to": True, "did not manage to": False,
        "did not remember to": False, "made sure to": True, "did not bother to": False}
IMPL_NNEG = {"managed to": 0, "failed to": 1, "remembered to": 0, "forgot to": 1, "neglected to": 1,
             "did not fail to": 2, "did not forget to": 2, "did not neglect to": 2, "did not manage to": 1,
             "did not remember to": 1, "made sure to": 0, "did not bother to": 1}
IMPL_PAIRS = [("failed to", "did not fail to"), ("forgot to", "did not forget to"),
              ("remembered to", "did not remember to"), ("managed to", "did not manage to"),
              ("neglected to", "did not neglect to"), ("remembered to", "forgot to"), ("managed to", "failed to"),
              ("made sure to", "did not bother to"), ("failed to", "IT_NOT failed to"),
              ("remembered to", "IT_NOT remembered to"), ("forgot to", "IT_NOT forgot to")]


@schema("implicative_verbs", 300)
def s_impl(rng):
    task = rng.choice(TASKS)
    x = pick_person(rng)[0]
    V = "V"
    rows = []
    for form in rng.choice(IMPL_PAIRS):
        if form.startswith("IT_NOT "):
            f = form[7:]
            val = not IMPL[f]
            t = f"It is not true that {x} {f} {task}."
            prem = NOT(lit(V, IMPL[f]))
            nneg = 1 + IMPL_NNEG[f]
        else:
            val = IMPL[form]
            t = f"{x} {form} {task}."
            prem = lit(V, val)
            nneg = IMPL_NNEG[form]
        rows.append((t, prem, "yes" if val else "no", "double_negation" if nneg >= 2 else "negation", form))
    if rows[0][2] == rows[1][2]:
        return None
    rng.shuffle(rows)
    q = f"Did {x} {task}?"
    return [mk(t, q, "true", e, [pr], V, g, f) for t, pr, g, e, f in rows]


# ================================================================================================ S40 exceptives
EXC_GROUPS = [
    ("The company has {n} departments: {lst}.", ["Finance", "Legal", "Sales", "HR", "IT", "Marketing", "Procurement",
                                                 "Research"], "moved to the new building in May",
     "move to the new building in May", "the {m} department"),
    ("The chain has {n} stores: {lst}.", PLACES, "closed early on Christmas Eve", "close early on Christmas Eve",
     "the {m} store"),
    ("The school has {n} Year 9 classes: {lst}.", ["9A", "9B", "9C", "9D", "9E", "9F"], "went on the museum trip",
     "go on the museum trip", "class {m}"),
    ("The hospital has {n} wards: {lst}.", ["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5", "Ward 6", "Ward 7"],
     "passed the infection-control audit", "pass the infection-control audit", "{m}"),
    ("The depot has {n} buses: {lst}.", ["bus 12", "bus 14", "bus 21", "bus 27", "bus 33", "bus 40", "bus 52"],
     "got new ticket machines", "get new ticket machines", "{m}"),
    ("The institute has {n} research groups: {lst}.",
     ["the Chen group", "the Okafor group", "the Lindqvist group", "the Moreau group", "the Haddad group",
      "the Novak group"], "switched to the new booking system", "switch to the new booking system", "{m}"),
    ("The league has {n} clubs: {lst}.", TEAMS, "paid their registration fee", "pay their registration fee", "{m}"),
    ("The office has {n} teams: {lst}.", ["the design team", "the data team", "the support team", "the sales team",
                                          "the finance team", "the legal team"], "hit their quarterly target",
     "hit their quarterly target", "{m}"),
]


@schema("exceptives", 300)
def s_except(rng):
    intro, pool, vp, vb, mfmt = rng.choice(EXC_GROUPS)
    n = rng.randint(3, 6)
    mem = rng.sample(pool, n)
    tgt = rng.randrange(n)
    others = [i for i in range(n) if i != tgt]
    extra = rng.sample(others, rng.randint(0, min(2, len(others) - 1)))
    at = [f"m{i}" for i in range(n)]
    lst = join(mem)
    head = cap(intro.format(n=nw(n), lst=lst))
    var = rng.choice(["except", "but", "exception_of", "no_except"])
    rows = []
    for with_tgt in (True, False):
        E = sorted(extra + ([tgt] if with_tgt else []))
        Es = join([mem[i] for i in E])
        if var == "no_except":
            if E:
                txt = f"None of them except {Es} {vp}."
            else:
                txt = f"None of them {vp}."
            vals = [i in E for i in range(n)]
        else:
            if not E:
                txt = f"All of them {vp}."
            elif var == "except":
                txt = f"All of them except {Es} {vp}."
            elif var == "but":
                txt = f"All of them but {Es} {vp}."
            else:
                txt = f"All of them, with the exception of {Es}, {vp}."
            vals = [i not in E for i in range(n)]
        rows.append((f"{head} {txt}", [lit(a, v) for a, v in zip(at, vals)], "yes" if vals[tgt] else "no"))
    rng.shuffle(rows)
    m = mfmt.format(m=mem[tgt])
    q = f"Did {m} {vb}?"
    return [mk(t, q, "true", "exception", pr, at[tgt], g, var) for t, pr, g in rows]


# ================================================================================================ S41 thresholds and units
# Each frame lists only the operator phrases that read naturally in its sentence.  kind 'min': inclusive ops
# mean value >= limit, exclusive ops value > limit; kind 'max': inclusive value <= limit, exclusive value < limit.
MIN_I = ["at least", "no fewer than", "a minimum of"]
MIN_I_AMT = ["at least", "not less than", "a minimum of"]
MAX_I = ["at most", "no more than", "up to", "a maximum of", "not more than"]
THR = [
    # rule template, scenario template, question, kind, limits, inclusive ops, exclusive ops, unit conversion
    ("Carry-on bags may weigh {op} {k} kg.", "{x}'s carry-on bag weighs {v} kg.",
     "Does {x}'s carry-on bag meet the rule?", "max", [7, 8, 10, 12], MAX_I, ["less than", "under"],
     ("g", 1000, "{x}'s carry-on bag weighs {v:,} g.")),
    ("Essays may have {op} {k:,} words.", "{x}'s essay has {v:,} words.", "Does {x}'s essay meet the rule?",
     "max", [1500, 2000, 2500, 3000], ["at most", "no more than", "up to", "a maximum of"], ["fewer than"], None),
    ("Applicants must have done {op} {k} hours of volunteering.", "{x} has done {v} hours of volunteering.",
     "Does {x} meet the volunteering requirement?", "min", [20, 30, 40, 50], MIN_I, ["more than", "over"],
     ("minutes", 60, "{x} has done {v:,} minutes of volunteering.")),
    ("Students must attend {op} {k} of the 12 sessions.", "{x} attended {v} of the 12 sessions.",
     "Does {x} meet the attendance requirement?", "min", [8, 9, 10], MIN_I, ["more than"], None),
    ("A booking may include {op} {k} guests.", "{x}'s booking includes {v} guests.",
     "Does {x}'s booking meet the rule?", "max", [4, 6, 8, 10], ["at most", "no more than", "up to", "a maximum of"],
     ["fewer than"], None),
    ("Leave must be requested {op} {k} days in advance.", "{x} requested leave {v} days in advance.",
     "Does {x}'s request meet the notice rule?", "min", [14, 21, 28], MIN_I + ["not less than"], ["more than"],
     ("weeks", 7, "{x} requested leave {v} in advance.")),
    ("Drivers must be {op} {k}.", "{x} is {v}.", "Does {x} meet the age requirement?", "min", [18, 21, 25],
     ["at least", "no younger than"], ["over", "older than"], None),
    ("To graduate, a student needs {op} {k} credits.", "{x} has {v} credits.",
     "Does {x} meet the credit requirement?", "min", [120, 180, 240], MIN_I, ["more than"], None),
    ("Project budgets may be {op} ${k:,}.", "{x}'s project budget is ${v:,}.",
     "Does {x}'s project budget meet the rule?", "max", [5000, 10000, 20000], MAX_I, ["less than", "under"], None),
    ("The vaccine fridge must be {op} {k}°C.", "The clinic's vaccine fridge is at {v}°C.",
     "Does the fridge temperature meet the rule?", "max", [5, 8], ["at most", "no more than", "no warmer than"],
     ["below", "less than", "under", "colder than"], None),
    ("Vehicles on site must travel at {op} {k} km/h.", "{x}'s van was travelling at {v} km/h.",
     "Does {x}'s speed meet the site rule?", "max", [10, 15, 20], ["no more than", "a maximum of", "not more than"],
     ["less than", "under"], None),
    ("Liquids in hand luggage must be in containers of {op} {k} ml.", "{x}'s shampoo bottle holds {v} ml.",
     "Does {x}'s bottle meet the rule?", "max", [100], ["no more than", "up to", "at most", "not more than"],
     ["less than", "under"], ("litres", None, None)),
    ("Calls must be answered in {op} {k} minutes.", "{x}'s call was answered after {v} minutes.",
     "Was {x}'s call answered within the rule?", "max", [2, 3, 5], ["no more than", "at most", "not more than"],
     ["less than", "under"], ("seconds", 60, "{x}'s call was answered after {v} seconds.")),
    ("A team must have {op} {k} players on the pitch to start a match.", "{T} had {v} players on the pitch at kick-off.",
     "Did {t} meet the rule at kick-off?", "min", [7, 9, 11], MIN_I, ["more than"], None),
    ("The deposit must be paid {op} {k} days before arrival.", "{x} paid the deposit {v} days before arrival.",
     "Did {x} pay the deposit in line with the rule?", "min", [7, 14, 30], MIN_I + ["not less than"], ["more than"],
     None),
    ("Each applicant must upload {op} {k} reference letters.", "{x} uploaded {v} reference letters.",
     "Does {x} meet the upload rule?", "min", [2, 3], MIN_I, ["more than"], None),
    ("The ride is for passengers {op} {k} cm tall.", "{x} is {v} cm tall.", "Does {x} meet the height rule?", "min",
     [120, 130, 140], ["at least", "a minimum of"], ["over", "more than"], ("m", None, None)),
    ("Hikers on the long route must carry {op} {k} litres of water.", "{x} is carrying {v} litres of water.",
     "Does {x} meet the water rule?", "min", [2, 3], MIN_I_AMT, ["more than"],
     ("ml", 1000, "{x} is carrying {v:,} ml of water.")),
    ("Parking in the short-stay bay is free for {op} {k} minutes.", "{x} parked there for {v} minutes.",
     "Was {x}'s stay within the free period?", "max", [30, 45, 60], ["up to", "no more than", "at most"],
     ["less than", "under"], ("phrase", None, None)),
    ("The lorry may carry {op} {k} tonnes.", "The lorry is carrying {v} tonnes.", "Is the lorry within the limit?",
     "max", [18, 26, 40], MAX_I, ["less than", "under"], ("kg", 1000, "The lorry is carrying {v:,} kg.")),
    ("The pool water must be {op} {k}°C.", "The pool water is at {v}°C.", "Does the water temperature meet the rule?",
     "min", [26, 28], ["at least", "no colder than"], ["warmer than", "above"], None),
    ("Children must be {op} {k} years old to join the climbing club.", "{x}'s son is {v}.",
     "Does {x}'s son meet the age rule?", "min", [8, 10, 12], ["at least", "no younger than"], ["over", "older than"],
     ("months", 12, "{x}'s son is {v} months old.")),
]


def rel_ok(v, rel, k):
    return {">=": v >= k, ">": v > k, "<=": v <= k, "<": v < k}[rel]


def weeks(n):
    return f"{n} week" if n == 1 else f"{n} weeks"


@schema("thresholds", 520)
def s_thresh(rng):
    rule_t, scen_t, q_t, kind, ks, incl, excl, conv = rng.choice(THR)
    x = pick_person(rng)[0]
    t = rng.choice(TEAMS)
    k = rng.choice(ks)
    rel_i, rel_e = (">=", ">") if kind == "min" else ("<=", "<")
    mode = rng.choice(["value", "opswap", "units", "units"] if conv else ["value", "value", "opswap"])
    q = q_t.format(x=x, t=t)
    fmt = dict(x=x, t=t, T=cap(t))
    rows = []
    if mode == "opswap":  # value exactly at the limit: inclusive wording meets it, exclusive wording does not
        for ph, rel in ((rng.choice(incl), rel_i), (rng.choice(excl), rel_e)):
            rows.append((rule_t.format(op=ph, k=k), scen_t.format(v=k, **fmt), k, rel, k))
    elif mode == "value":
        ex = rng.random() < 0.35
        ph, rel = (rng.choice(excl), rel_e) if ex else (rng.choice(incl), rel_i)
        step = 1 if k < 1000 else rng.choice([1, 10, 50])
        if kind == "min":
            vals = (k, k - step) if rel == ">=" else (k + step, k)
        else:
            vals = (k, k + step) if rel == "<=" else (k - step, k)
        for v in vals:
            rows.append((rule_t.format(op=ph, k=k), scen_t.format(v=v, **fmt), v, rel, k))
    else:
        unit, factor, stpl = conv
        ex = rng.random() < 0.3
        ph, rel = (rng.choice(excl), rel_e) if ex else (rng.choice(incl), rel_i)
        if unit in ("litres", "m", "phrase"):
            if unit == "litres":  # 0.1 litres = 100 ml
                opts = [("0.1 litres", 100), ("0.15 litres", 150), ("0.05 litres", 50), ("0.2 litres", 200),
                        ("0.12 litres", 120), ("0.09 litres", 90)]
                stpl = "{x}'s shampoo bottle holds {v}."
            elif unit == "m":     # height limit in cm, height given in metres
                opts = [(f"{(k + d) / 100:.2f} m", k + d) for d in (-12, -5, -1, 0, 1, 4, 15)]
                stpl = "{x} is {v} tall."
            else:                 # minutes limit, stay given in words
                opts = [(w, m) for w, m in (("a quarter of an hour", 15), ("half an hour", 30),
                                            ("three quarters of an hour", 45), ("an hour", 60),
                                            ("an hour and a quarter", 75), ("an hour and a half", 90))]
                stpl = "{x} parked there for {v}."
            ys = [o for o in opts if rel_ok(o[1], rel, k)]
            ns = [o for o in opts if not rel_ok(o[1], rel, k)]
            if not ys or not ns:
                return None
            for shown, base in (rng.choice(ys), rng.choice(ns)):
                rows.append((rule_t.format(op=ph, k=k), stpl.format(x=x, v=shown), base, rel, k))
        else:
            K = k * factor
            if unit == "weeks":
                cands = [w * 7 for w in (k // 7 - 1, k // 7, k // 7 + 1) if w > 0]
            elif unit == "g":
                cands = [K - 200, K - 50, K, K + 50, K + 300]
            elif unit == "minutes":
                cands = [K - 60, K - 15, K, K + 30, K + 90]
            elif unit == "ml":
                cands = [K - 500, K - 250, K, K + 250, K + 500]
            elif unit == "kg":
                cands = [K - 800, K - 150, K, K + 200, K + 1500]
            elif unit == "months":
                cands = [K - 7, K - 1, K, K + 1, K + 5]
            else:  # seconds
                cands = [K - 20, K - 5, K, K + 10, K + 45]
            ys = [c for c in cands if rel_ok(c, rel, K)]
            ns = [c for c in cands if not rel_ok(c, rel, K)]
            if not ys or not ns:
                return None
            for bv in (rng.choice(ys), rng.choice(ns)):
                shown = weeks(bv // 7) if unit == "weeks" else bv
                rows.append((rule_t.format(op=ph, k=k), stpl.format(x=x, v=shown), bv, rel, K))
    out = []
    for rule, scen, v, rel, lim in rows:
        meets = rel_ok(v, rel, lim)
        lo, hi = min(v, lim) - 3, max(v, lim) + 3
        out.append(mk(f"{rule} {cap(scen)}", q, "meets", "units" if mode == "units" else "numeric",
                      [CMP("v", "==", v)], CMP("v", rel, lim), "yes" if meets else "no", f"{mode}/{rel}",
                      ints={"v": [lo, hi]}))
    if len(out) != 2 or out[0]["gold"] == out[1]["gold"]:
        return None
    rng.shuffle(out)
    return out


@schema("quantifier_word_swap", 280)
def s_qswap(rng):
    """Same count, different quantifier word: 'exactly' vs 'at least' / 'at most' (value off the limit)."""
    frames = [("Each team must field {op} {k} players.", "{t} fielded {v} players.", "Did {t} meet the rule?"),
              ("Each group presentation must have {op} {k} speakers.", "{x}'s group had {v} speakers.",
               "Did {x}'s group meet the rule?"),
              ("Each committee must include {op} {k} student members.", "The sports committee includes {v} student members.",
               "Does the sports committee meet the rule?"),
              ("Every shift must be covered by {op} {k} nurses.", "The night shift was covered by {v} nurses.",
               "Did the night shift meet the rule?"),
              ("Each reviewer must assess {op} {k} proposals.", "{x} assessed {v} proposals.",
               "Did {x} meet the rule?"),
              ("A jury must have {op} {k} members.", "The jury in the case had {v} members.",
               "Did the jury meet the rule?"),
              ("Each tour group must have {op} {k} guides.", "The Tuesday tour group had {v} guides.",
               "Did the Tuesday tour group meet the rule?")]
    rule_t, scen_t, q_t = rng.choice(frames)
    x, t = pick_person(rng)[0], rng.choice(TEAMS)
    k = rng.randint(2, 12)
    if rng.random() < 0.5:
        v = k + rng.randint(1, 2)
        pairs = [("at least", ">="), ("exactly", "==")]
    else:
        v = k - rng.randint(1, min(2, k - 1))
        pairs = [("at most", "<="), ("exactly", "==")]
    if rng.random() < 0.3:
        pairs = [(("no fewer than" if p == "at least" else "no more than" if p == "at most" else p), r) for p, r in pairs]
    out = []
    for ph, rel in pairs:
        ok = {"==": v == k, ">=": v >= k, "<=": v <= k}[rel]
        st = f"{rule_t.format(op=ph, k=nw(k) if k <= 12 else k)} {cap(scen_t.format(x=x, t=t, v=nw(v)))}"
        out.append(mk(st, cap(q_t.format(x=x, t=t)), "meets", "quantifier", [CMP("v", "==", v)], CMP("v", rel, k),
                      "yes" if ok else "no", ph, ints={"v": [0, 20]}))
    rng.shuffle(out)
    return out


# ================================================================================================ S43 some-not vs none-failed
SOME_NOT = [
    ("tenants", "tenant", "pay the rent on time", "paid the rent on time"),
    ("staff", "staff member", "complete the security training", "completed the security training"),
    ("drivers", "driver", "log their hours", "logged their hours"),
    ("students", "student", "hand in the permission slip", "handed in the permission slip"),
    ("suppliers", "supplier", "send an invoice", "sent an invoice"),
    ("patients", "patient", "fill in the consent form", "filled in the consent form"),
    ("players", "player", "wear a helmet", "wore a helmet"),
    ("volunteers", "volunteer", "sign in at the desk", "signed in at the desk"),
    ("contractors", "contractor", "show proof of insurance", "showed proof of insurance"),
    ("guests", "guest", "check out by noon", "checked out by noon"),
    ("branches", "branch", "submit the monthly report", "submitted the monthly report"),
    ("inspectors", "inspector", "file a report", "filed a report"),
    ("members", "member", "renew their membership", "renewed their membership"),
    ("interns", "intern", "attend the induction", "attended the induction"),
]
SN_PAIRS = [("Some of the {pl} did not {vb}.", "None of the {pl} failed to {vb}."),
            ("Not every {sg} {vp}.", "Every single {sg} {vp}."),
            ("At least one {sg} did not {vb}.", "There was no {sg} who did not {vb}."),
            ("Not all of the {pl} {vp}.", "All of the {pl} {vp}, without exception."),
            ("A few of the {pl} failed to {vb}.", "Not one of the {pl} failed to {vb}.")]


@schema("some_not_vs_none", 260)
def s_somenot(rng):
    pl, sg, vb, vp = rng.choice(SOME_NOT)
    neg, pos = rng.choice(SN_PAIRS)
    Al = "All"
    qtype = rng.random() < 0.5
    q = f"Did every {sg} {vb}?" if qtype else f"Did any {sg} fail to {vb}?"
    goal = Al if qtype else NOT(Al)
    rows = [(cap(neg.format(pl=pl, sg=sg, vb=vb, vp=vp)), NOT(Al)), (cap(pos.format(pl=pl, sg=sg, vb=vb, vp=vp)), Al)]
    rng.shuffle(rows)
    hdr = header(rng, ["End-of-month check:", "Audit note:", "Coordinator's summary:"], 0.35)
    out = []
    for t, pr in rows:
        val = (pr == Al) if qtype else (pr != Al)
        out.append(mk(hdr + t, q, "true", "quantifier" if qtype else "negation", [pr], goal, "yes" if val else "no",
                      "all_q" if qtype else "fail_q"))
    return out


# ================================================================================================ S46 calendar exceptions
def nth_weekday(d):
    return (d.day - 1) // 7 + 1


def is_last_weekday(d):
    return (d + dt.timedelta(days=7)).month != d.month


def fmt_d(d):
    return f"{WEEKDAYS[d.weekday()]} {d.day} {MONTHS[d.month - 1]} {d.year}"


CAL = [
    ("The recycling centre is open every day except the first Monday of each month.", 0, "first",
     "the recycling centre is open"),
    ("The gallery is open every day except the last Friday of each month.", 4, "last", "the gallery is open"),
    ("The farmers' market runs every Saturday except the second Saturday of each month.", 5, "second",
     "the farmers' market runs"),
    ("The community hall can be booked any Wednesday except the third Wednesday of each month.", 2, "third",
     "the community hall can be booked"),
    ("The swimming club trains every Tuesday except the last Tuesday of each month.", 1, "last",
     "the swimming club trains"),
    ("The repair café meets every Sunday except the first Sunday of each month.", 6, "first",
     "the repair café meets"),
    ("The walking group meets every Thursday except the fourth Thursday of each month.", 3, "fourth",
     "the walking group meets"),
    ("The mobile library visits every Monday except the last Monday of each month.", 0, "last",
     "the mobile library visits"),
    ("The community fridge is restocked every Friday except the first Friday of each month.", 4, "first",
     "the community fridge is restocked"),
    ("Choir practice is held every Wednesday except the second Wednesday of each month.", 2, "second",
     "choir practice is held"),
    ("The bike repair stall runs every Saturday except the last Saturday of each month.", 5, "last",
     "the bike repair stall runs"),
    ("The allotment committee meets every Tuesday except the third Tuesday of each month.", 1, "third",
     "the allotment committee meets"),
    ("The food bank opens every Thursday except the first Thursday of each month.", 3, "first",
     "the food bank opens"),
]
ORD = {"first": 1, "second": 2, "third": 3, "fourth": 4}


@schema("calendar_exception", 250)
def s_calendar(rng):
    x = pick_person(rng)[0]
    if rng.random() < 0.35:
        # public-holiday exception stated as a fact about the date
        place = rng.choice(PLACES)
        while True:
            d = dt.date(rng.choice([2026, 2027]), rng.randint(1, 12), rng.randint(1, 28))
            if d.weekday() < 5:
                break
        rule = f"The {place} tax office is open Monday to Friday, except on public holidays."
        E = "E"
        rows = [(f"{rule} {fmt_d(d)} is a public holiday. {x} plans to visit the office that day.", [E], "no"),
                (f"{rule} {fmt_d(d)} is not a public holiday. {x} plans to visit the office that day.", [NOT(E)], "yes")]
        rng.shuffle(rows)
        q = f"Is the office open on the day {x} plans to visit?"
        return [mk(t, q, "true", "exception", pr, NOT(E), g, "holiday") for t, pr, g in rows]
    rule, wd, which, clause = rng.choice(CAL)
    y, m = rng.choice([2026, 2027]), rng.randint(1, 12)
    days = [dt.date(y, m, dd) for dd in range(1, 32) if _valid(y, m, dd) and dt.date(y, m, dd).weekday() == wd]
    if which == "last":
        exc = [d for d in days if is_last_weekday(d)]
    else:
        exc = [d for d in days if nth_weekday(d) == ORD[which]]
    assert len(exc) == 1
    ok = [d for d in days if d not in exc]
    d_exc, d_ok = exc[0], rng.choice(ok)
    E = "E"
    rows = []
    for d in (d_exc, d_ok):
        is_exc = (is_last_weekday(d) if which == "last" else nth_weekday(d) == ORD[which])
        rows.append((f"{rule} {x} wants to go on {fmt_d(d)}.", [lit(E, is_exc)], "no" if is_exc else "yes"))
    rng.shuffle(rows)
    q = f"On the day {x} wants to go, is it true that {clause}?"
    return [mk(t, q, "true", "temporal", pr, NOT(E), g, which) for t, pr, g in rows]


def _valid(y, m, d):
    try:
        dt.date(y, m, d)
        return True
    except ValueError:
        return False


# ================================================================================================ S56 lexical negation
LEX = [
    ("valid", "invalid", "the parking permit for bay {u}", ""),
    ("paid", "unpaid", "invoice {n}", ""),
    ("locked", "unlocked", "the storeroom door", ""),
    ("signed", "unsigned", "the lease for Unit {u}", ""),
    ("insured", "uninsured", "the delivery van", ""),
    ("complete", "incomplete", "{x}'s application", ""),
    ("refundable", "non-refundable", "the deposit for the hall", ""),
    ("accessible", "inaccessible", "the east entrance", " to wheelchair users"),
    ("available", "unavailable", "the Blue Room", " on Friday"),
    ("eligible", "ineligible", "{x}", " for the bursary"),
    ("registered", "unregistered", "the boat moored at berth {u}", ""),
    ("vaccinated", "unvaccinated", "{x}'s dog", " against rabies"),
    ("attended", "unattended", "the reception desk", " this afternoon"),
    ("certified", "uncertified", "the gas boiler in flat {u}", ""),
    ("approved", "unapproved", "the new logo", ""),
    ("reachable", "unreachable", "the backup server", ""),
    ("occupied", "unoccupied", "flat {u}", ""),
    ("taxable", "non-taxable", "the relocation grant", ""),
    ("finished", "unfinished", "the quarterly report", ""),
    ("encrypted", "unencrypted", "the laptop's hard drive", ""),
]
LEX_FORMS = {  # template, (adjective used: P or N), value of P given the sentence
    "isN": ("{S} is {N}{suf}.", False), "isnotN": ("{S} is not {N}{suf}.", True),
    "isP": ("{S} is {P}{suf}.", True), "isnotP": ("{S} is not {P}{suf}.", False),
    "itnotN": ("It is not true that {s} is {N}{suf}.", True), "itnotP": ("It is not true that {s} is {P}{suf}.", False),
    "contraryN": ("Contrary to what was reported, {s} is not {N}{suf}.", True),
    "contraryN2": ("Contrary to what was reported, {s} is {N}{suf}.", False),
    "wrongN": ("{S} was wrongly listed as {N}{suf}.", True), "rightN": ("{S} was correctly listed as {N}{suf}.", False),
}
LEX_PAIRS = [("isN", "isnotN"), ("isP", "isnotP"), ("itnotN", "isN"), ("itnotP", "isP"), ("contraryN", "contraryN2"),
             ("wrongN", "rightN"), ("isnotN", "isnotP")]
LEX_DNEG = {"isnotN", "itnotN", "contraryN", "wrongN"}


@schema("lexical_negation", 340)
def s_lex(rng):
    P, N, S, suf = rng.choice(LEX)
    S = S.format(x=pick_person(rng)[0], n=rng.randint(1000, 9999), u=rng.randint(2, 48))
    f1, f2 = rng.choice(LEX_PAIRS)
    Pa = "P"
    ask_pos = rng.random() < 0.7
    q = f"Is {S} {P if ask_pos else N}{suf}?"
    goal = Pa if ask_pos else NOT(Pa)
    rows = []
    for f in (f1, f2):
        t, val = LEX_FORMS[f]
        txt = t.format(S=cap(S), s=S, P=P, N=N, suf=suf)
        ans = val if ask_pos else (not val)
        rows.append((txt, lit(Pa, val), "yes" if ans else "no", "double_negation" if f in LEX_DNEG else "negation", f))
    if rows[0][2] == rows[1][2]:
        return None
    rng.shuffle(rows)
    hdr = header(rng, ["Correction to yesterday's email:", "Status update:", "From the records office:",
                       "Admin note:"], 0.4)
    return [mk(hdr + t, q, "true", e, [pr], goal, g, f) for t, pr, g, e, f in rows]


# ================================================================================================ S57 'no ... except'
NOEXC = [
    ("The audit covered all twelve monthly accounts.",
     "The audit found no errors in any account except the {m} account.",
     "The audit found no errors in any account, including the {m} account.",
     "Did the audit find errors in the {m} account?", MONTHS),
    ("The inspector checked every room in the house, including the {m} and the {m2}.",
     "The inspector found no damp in any room except the {m}.",
     "The inspector found no damp in any room, including the {m}.",
     "Did the inspector find damp in the {m}?", ["basement", "attic", "laundry room", "back bedroom", "cellar",
                                                  "bathroom"]),
    ("The virus scan checked every folder, including {m} and {m2}.",
     "The virus scan found no threats in any folder except {m}.",
     "The virus scan found no threats in any folder, including {m}.",
     "Did the virus scan find threats in {m}?", ["Downloads", "Desktop", "Documents", "Shared", "Archive"]),
    ("The editor read all fifteen chapters of the book.",
     "The editor found no typos in any chapter except chapter {m}.",
     "The editor found no typos in any chapter, including chapter {m}.",
     "Did the editor find typos in chapter {m}?", [str(i) for i in range(2, 15)]),
    ("The vet examined every dog at the kennel, including {m} and {m2}.",
     "The vet found no fleas on any of the dogs except {m}.",
     "The vet found no fleas on any of the dogs, including {m}.",
     "Did the vet find fleas on {m}?", ["Biscuit", "Pepper", "Rolo", "Luna", "Max", "Juno", "Bramble", "Scout"]),
    ("The lab tested every sample, including samples {m} and {m2}.",
     "The lab found no lead in any sample except sample {m}.",
     "The lab found no lead in any sample, including sample {m}.",
     "Did the lab find lead in sample {m}?", ["A3", "B7", "C2", "D9", "E4", "F1"]),
    ("The survey covered every street in the district, including {m} and {m2}.",
     "The survey found no potholes on any street except {m}.",
     "The survey found no potholes on any street, including {m}.",
     "Did the survey find potholes on {m}?", ["Mill Lane", "Station Road", "Park Avenue", "Church Street",
                                              "Queen's Road", "Bridge Street"]),
    ("The safety check covered every vehicle in the fleet, including vans {m} and {m2}.",
     "The safety check found no faults in any vehicle except van {m}.",
     "The safety check found no faults in any vehicle, including van {m}.",
     "Did the safety check find faults in van {m}?", [str(i) for i in range(3, 40)]),
    ("The paper had several reviewers, including {m} and {m2}.",
     "None of the reviewers except {m} recommended rejecting the paper.",
     "None of the reviewers, including {m}, recommended rejecting the paper.",
     "Did {m} recommend rejecting the paper?", [p[0] for p in PEOPLE]),
    ("The tasting panel tried every batch, including batches {m} and {m2}.",
     "The tasting panel found no off-flavours in any batch except batch {m}.",
     "The tasting panel found no off-flavours in any batch, including batch {m}.",
     "Did the tasting panel find off-flavours in batch {m}?", [str(i) for i in range(11, 60)]),
]


@schema("no_except", 220)
def s_noexc(rng):
    intro, exc, incl, qt, pool = rng.choice(NOEXC)
    m, m2 = rng.sample(pool, 2)
    if rng.random() < 0.5:
        m, m2 = m2, m
    intro = intro.format(m=m, m2=m2) if rng.random() < 0.5 else intro.format(m=m2, m2=m)
    F = "F"
    if rng.random() < 0.5:
        rows = [(exc.format(m=m), F, "yes"), (incl.format(m=m), NOT(F), "no")]
        var = "except_vs_including"
    else:
        rows = [(exc.format(m=m), F, "yes"), (exc.format(m=m2), NOT(F), "no")]
        var = "other_exception"
    rng.shuffle(rows)
    q = qt.format(m=m)
    return [mk(f"{intro} {t}", q, "true", "exception", [pr], F, g, var) for t, pr, g in rows]
