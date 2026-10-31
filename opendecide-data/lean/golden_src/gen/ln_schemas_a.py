"""gen_logic_negation schemas, part A: quantifiers, set membership, 'only', conditionals, 'unless', disjunction,
De Morgan scope, deontic negation, contraries, comparatives.  Each schema returns a fact-flip twin pair
(item_a, item_b) sharing one question, with opposite intended gold labels; every item carries its logical form
(premises, goal) which the driver re-decides with ln_engine.decide.  Claude-written vocabulary and templates only.
"""
import re

from ln_engine import (AND, CMP, CNT, COMPANIES, HOTELS, IFF, IMP, NOT, OR, PEOPLE, PLACES, RESTAURANTS, STREETS, TEAMS,
                       art, cap, join, lit, nmix, nw)

SCHEMAS = []


def schema(name, weight):
    def deco(f):
        SCHEMAS.append((name, weight, f))
        return f
    return deco


ABBR_END = re.compile(r"\b(a\.m|p\.m|Co|Dr|etc)\.\.")


# a count of one takes the singular noun ('1 days' -> '1 day', 'one players' -> 'one player')
ONE_PLURAL = re.compile(r"(?<![\d.,])\b(1|[Oo]ne) (reference letter|student member|litre|minute|day|player|speaker|nurse|proposal|"
                        r"member|guide|guest|credit|hour|session|week|tonne|year|bedroom)s\b")


def tidy(s):
    """Collapse the doubled full stop after a sentence-final abbreviation ('9 a.m..' -> '9 a.m.') and fix
    singular agreement after a count of one."""
    return ONE_PLURAL.sub(r"\1 \2", ABBR_END.sub(r"\1.", s))


def mk(state, q, qid, edge, prem, goal, gold, var, ints=None):
    return {"state": tidy(state), "q": tidy(q), "qid": qid, "edge": edge, "prem": list(prem), "goal": goal,
            "gold": gold, "var": var, "ints": ints or {}}


CERT_Q = ["Based only on the {doc}, can we conclude that {s}?",
          "Does the {doc} establish that {s}?",
          "From the {doc} alone, must it be true that {s}?",
          "Can it be concluded from the {doc} that {s}?",
          "Is it certain, given only the {doc}, that {s}?"]


NEUTRAL_DOCS = {"text", "passage", "information given", "rule", "rules", "policy", "notice"}


def cert_q(rng, doc, s):
    if doc not in NEUTRAL_DOCS:  # the text is not labelled as a report / email, so keep the reference neutral
        doc = rng.choice(["text", "text", "passage", "information given"])
    return rng.choice(CERT_Q).format(doc=doc, s=s)


def header(rng, kinds, p=0.35):
    if rng.random() >= p:
        return ""
    return rng.choice(kinds) + "\n"


RULE_HDR = ["Policy excerpt:", "From the staff handbook:", "Posted notice:", "Rules for this site:",
            "Excerpt from the terms and conditions:", "Operations manual, section 4:"]
REPORT_HDR = ["Status update:", "Weekly summary:", "From the shift log:", "Report excerpt:", "Team update:"]


# ================================================================================================ S01 roster quantifiers
ROSTER = [
    # kind, group plural, group singular, vp_past, vp_base, neg_past (after subject list), pos label, neg label, doc
    ("person", "interns", "intern", "completed the fire-safety course", "complete the fire-safety course",
     "did not complete it", "completed", "not completed", "Fire-safety course, intern record"),
    ("flight", "morning flights", "morning flight", "departed on time", "depart on time", "departed late",
     "on time", "late", "Departures board, 06:00-12:00"),
    ("restaurant", "restaurants on Market Street", "restaurant on Market Street", "passed the hygiene inspection",
     "pass the hygiene inspection", "failed it", "passed", "failed", "Hygiene inspections, Market Street"),
    ("person", "applicants", "applicant", "submitted a reference letter", "submit a reference letter",
     "did not submit one", "submitted", "missing", "Reference letters received"),
    ("person", "patients on the list", "patient on the list", "received the second dose", "receive the second dose",
     "did not receive it", "received", "not received", "Second-dose record"),
    ("parcel", "parcels on the van", "parcel on the van", "arrived before noon", "arrive before noon",
     "arrived after noon", "before noon", "after noon", "Delivery log, Tuesday"),
    ("person", "players in the squad", "player in the squad", "attended Tuesday's practice",
     "attend Tuesday's practice", "missed it", "attended", "absent", "Practice attendance, Tuesday"),
    ("branch", "branches", "branch", "met the quarterly sales target", "meet the quarterly sales target",
     "missed it", "met", "missed", "Quarterly sales target by branch"),
    ("person", "tenants in the building", "tenant in the building", "paid the October rent on time",
     "pay the October rent on time", "did not pay it on time", "on time", "not on time", "October rent"),
    ("person", "volunteers", "volunteer", "signed the liability waiver", "sign the liability waiver",
     "did not sign it", "signed", "not signed", "Liability waivers"),
    ("person", "students", "student", "passed the driving theory test", "pass the driving theory test",
     "failed it", "passed", "failed", "Driving theory test results"),
    ("supplier", "suppliers", "supplier", "delivered the order in full", "deliver the order in full",
     "delivered a short order", "in full", "short", "Supplier deliveries, week 14"),
    ("server", "servers", "server", "stayed online during the update", "stay online during the update",
     "went offline", "online", "offline", "Update status"),
    ("hotel", "hotels on the shortlist", "hotel on the shortlist", "had rooms free on 12 June",
     "have rooms free on 12 June", "had no rooms free", "rooms free", "full", "Availability for 12 June"),
    ("person", "committee members", "committee member", "voted for the proposal", "vote for the proposal",
     "voted against it", "for", "against", "Committee vote on the proposal"),
    ("room", "classrooms on the ground floor", "classroom on the ground floor", "passed the fire-alarm test",
     "pass the fire-alarm test", "failed it", "passed", "failed", "Fire-alarm test, ground floor"),
    ("person", "drivers on the night shift", "driver on the night shift", "completed the route without an incident",
     "complete the route without an incident", "reported an incident", "no incident", "incident",
     "Night shift report"),
    ("team", "youth teams at the club", "youth team at the club", "won their weekend match",
     "win their weekend match", "did not win it", "won", "did not win", "Weekend results, youth section"),
    ("person", "nurses on Ward 6", "nurse on Ward 6", "renewed their CPR certificate", "renew their CPR certificate",
     "did not renew it", "renewed", "not renewed", "CPR certificates, Ward 6"),
    ("person", "employees in the Leeds office", "employee in the Leeds office", "set up two-factor authentication",
     "set up two-factor authentication", "did not set it up", "done", "not done", "Two-factor set-up, Leeds office"),
    ("bus", "buses in the depot", "bus in the depot", "passed the brake check", "pass the brake check", "failed it",
     "passed", "failed", "Brake checks"),
    ("person", "guests at the wedding", "guest at the wedding", "replied to the invitation",
     "reply to the invitation", "did not reply", "replied", "no reply", "Wedding replies"),
]


def roster_members(rng, kind, n):
    if kind == "person":
        return [p[0] for p in rng.sample(PEOPLE, n)]
    if kind == "flight":
        return [f"Flight {x}" for x in rng.sample(range(102, 990), n)]
    if kind == "restaurant":
        return rng.sample(RESTAURANTS, n)
    if kind == "branch":
        return rng.sample(PLACES, n)
    if kind == "parcel":
        return [f"{L}{rng.randint(100, 999)}" for L in rng.sample("ABCDEFGHJKLMNPRSTW", n)]
    if kind == "supplier":
        return rng.sample(COMPANIES, n)
    if kind == "server":
        pre = rng.sample(["web", "db", "mail", "cache", "api", "files", "auth", "search"], n)
        return [f"{p}-0{rng.randint(1, 9)}" for p in pre]
    if kind == "hotel":
        return rng.sample(HOTELS, n)
    if kind == "room":
        return [f"Room {x}" for x in rng.sample(range(1, 30), n)]
    if kind == "team":
        return [f"the under-{a}s" for a in rng.sample(range(8, 19), n)]
    if kind == "bus":
        return [f"Bus {x}" for x in rng.sample(range(2, 99), n)]
    raise ValueError(kind)


def roster_text(fmt, d, mem, st):
    kind, gp, gs, vpp, vpb, negp, lp, ln_, doc = d
    pos = [m for m, s in zip(mem, st) if s]
    neg = [m for m, s in zip(mem, st) if not s]
    n = len(mem)
    if fmt == "prose":
        head = f"Of the {nw(n)} {gp} ({join(mem)}), "
        if not neg:
            return head + f"all {vpp}."
        if not pos:
            return head + f"none {vpp}."
        return head + f"{join(pos)} {vpp}, while {join(neg)} {negp}."
    if fmt == "bullets":
        return f"{doc}:\n" + "\n".join(f"- {cap(m)}: {lp if s else ln_}" for m, s in zip(mem, st))
    if fmt == "except":
        head = f"The {gp} were {join(mem)}. "
        if not neg:
            return head + f"All of them {vpp}."
        if not pos:
            return head + f"None of them {vpp}."
        return head + f"All of them except {join(neg)} {vpp}."
    if fmt == "onlyneg":
        head = f"The {gp} were {join(mem)}. "
        if not neg:
            return head + f"Every one of them {vpp}."
        return head + f"Only {join(neg)} did not {vpb}; the others all did."
    if fmt == "yesno":
        q = cap(vpb)
        return f"{q}? " + " ".join(f"{cap(m)}: {'yes' if s else 'no'}." for m, s in zip(mem, st))
    raise ValueError(fmt)


def roster_claim(rng, ctype, d, mem):
    """Return (question, goal formula builder f(atoms), python truth fn(st))."""
    kind, gp, gs, vpp, vpb, negp, lp, ln_, doc = d
    n = len(mem)
    at = [f"m{i}" for i in range(n)]
    if ctype == "all":
        q = rng.choice([f"Did all of the {gp} {vpb}?", f"Is it true that every {gs} {vpp}?"])
        return q, CNT("==", n, at), lambda st: all(st)
    if ctype == "some":
        return f"Did at least one of the {gp} {vpb}?", CNT(">=", 1, at), lambda st: any(st)
    if ctype == "none":
        return f"Is it true that none of the {gp} {vpp}?", CNT("==", 0, at), lambda st: not any(st)
    if ctype == "any_fail":
        return f"Did any of the {gp} fail to {vpb}?", CNT(">=", 1, [NOT(a) for a in at]), lambda st: not all(st)
    if ctype == "no_fail":
        return (f"Is it true that no {gs} failed to {vpb}?", CNT("==", 0, [NOT(a) for a in at]),
                lambda st: all(st))
    if ctype == "most":
        return f"Did most of the {gp} {vpb}?", ("cmpcount_most", at), lambda st: 2 * sum(st) > n
    if ctype == "more_half":
        return f"Did more than half of the {gp} {vpb}?", ("cmpcount_most", at), lambda st: 2 * sum(st) > n
    if ctype == "not_all":
        return f"Is it true that not all of the {gp} {vpp}?", NOT(CNT("==", n, at)), lambda st: not all(st)
    if ctype == "all_but_one":
        return f"Did all but one of the {gp} {vpb}?", CNT("==", n - 1, at), lambda st: sum(st) == n - 1
    k = rng.randint(1, n - 1)
    if ctype == "atleast":
        return f"Did at least {nw(k)} of the {gp} {vpb}?", CNT(">=", k, at), lambda st: sum(st) >= k
    if ctype == "exactly":
        return f"Did exactly {nw(k)} of the {gp} {vpb}?", CNT("==", k, at), lambda st: sum(st) == k
    if ctype == "atmost":
        return f"Did at most {nw(k)} of the {gp} {vpb}?", CNT("<=", k, at), lambda st: sum(st) <= k
    if ctype == "fewer":
        k = rng.randint(2, n)
        return f"Did fewer than {nw(k)} of the {gp} {vpb}?", CNT("<", k, at), lambda st: sum(st) < k
    i, j = rng.sample(range(n), 2)
    X, Y = mem[i], mem[j]
    if ctype == "only":
        others = [a for t, a in enumerate(at) if t != i]
        return (f"Is it true that only {X} {vpp}?", AND(at[i], CNT("==", 0, others)),
                lambda st: st[i] and sum(st) == 1)
    if ctype == "both":
        return f"Did both {X} and {Y} {vpb}?", AND(at[i], at[j]), lambda st: st[i] and st[j]
    if ctype == "neither":
        return (f"Is it true that neither {X} nor {Y} {vpp}?", AND(NOT(at[i]), NOT(at[j])),
                lambda st: not st[i] and not st[j])
    if ctype == "one_of_two":
        return f"Did at least one of {X} and {Y} {vpb}?", OR(at[i], at[j]), lambda st: st[i] or st[j]
    raise ValueError(ctype)


R_CTYPES = ["all", "some", "none", "any_fail", "no_fail", "most", "more_half", "not_all", "all_but_one", "atleast",
            "exactly", "atmost", "fewer", "only", "both", "neither", "one_of_two"]
R_EDGE = {"any_fail": "negation", "no_fail": "double_negation", "not_all": "negation", "neither": "negation",
          "atleast": "numeric", "exactly": "numeric", "atmost": "numeric", "fewer": "numeric"}


@schema("roster_quant", 1100)
def s_roster(rng):
    d = rng.choice(ROSTER)
    n = rng.randint(3, 7)
    mem = roster_members(rng, d[0], n)
    ctype = rng.choice(R_CTYPES)
    q, goal, fn = roster_claim(rng, ctype, d, mem)
    if isinstance(goal, tuple) and goal[0] == "cmpcount_most":
        goal = CNT(">", n / 2, goal[1])
    st = [rng.random() < 0.5 for _ in range(n)]
    flips = [i for i in range(n) if fn(st) != fn(st[:i] + [not st[i]] + st[i + 1:])]
    if not flips:
        return None
    i = rng.choice(flips)
    st2 = st[:i] + [not st[i]] + st[i + 1:]
    if ctype == "most":  # keep 'most' away from its fuzzy zone: yes-row >= 60 %, no-row <= 50 %
        for s in (st, st2):
            share = sum(s) / n
            if fn(s) and share < 0.6 or (not fn(s) and share > 0.5):
                return None
    fmt = rng.choice(["prose", "prose", "bullets", "except", "onlyneg", "yesno"])
    if fmt == "onlyneg" and not all(1 <= n - sum(s) <= 2 for s in (st, st2)):
        fmt = "prose"
    at = [f"m{t}" for t in range(n)]
    hdr = header(rng, REPORT_HDR, 0.2) if fmt != "bullets" else ""
    out = []
    for s in (st, st2):
        prem = [lit(a, v) for a, v in zip(at, s)]
        out.append(mk(hdr + roster_text(fmt, d, mem, s), q, "true", R_EDGE.get(ctype, "quantifier"), prem, goal,
                      "yes" if fn(s) else "no", f"{ctype}/{fmt}"))
    return out


# ================================================================================================ S02 count quantifiers
COUNTS = [
    ("council members", "voted in favour of the new bike lanes", "vote in favour of the new bike lanes"),
    ("survey respondents", "said they would recommend the clinic", "say they would recommend the clinic"),
    ("union members", "backed the strike", "back the strike"),
    ("residents who replied", "supported the parking plan", "support the parking plan"),
    ("students who sat the resit", "passed it", "pass it"),
    ("employees", "completed the wellbeing survey", "complete the wellbeing survey"),
    ("shareholders present", "approved the merger", "approve the merger"),
    ("parents who responded", "chose the later start time", "choose the later start time"),
    ("tasting-panel members", "preferred the new recipe", "prefer the new recipe"),
    ("club members", "voted to raise the annual fee", "vote to raise the annual fee"),
    ("delegates", "signed the joint statement", "sign the joint statement"),
    ("pilot users", "renewed their subscription", "renew their subscription"),
    ("teachers at the school", "joined the new pension scheme", "join the new pension scheme"),
    ("drivers surveyed", "said they would use a park-and-ride", "say they would use a park-and-ride"),
    ("households on the street", "signed the petition for speed bumps", "sign the petition for speed bumps"),
    ("nurses on the ward", "had their flu jab", "have their flu jab"),
    ("shops on the high street", "stayed open late on Thursday", "stay open late on Thursday"),
    ("passengers surveyed", "rated the service as good", "rate the service as good"),
    ("jurors", "voted to convict", "vote to convict"),
    ("patients in the trial", "reported fewer headaches", "report fewer headaches"),
    ("members of the choir", "sang at the wedding", "sing at the wedding"),
    ("applicants", "got an interview", "get an interview"),
    ("farmers in the co-operative", "switched to organic feed", "switch to organic feed"),
]
C_CLAIMS = {
    # name: (question template, goal builder(N) -> formula over int k, python fn(k, N), needs)
    "majority": ("Did a majority of the {g} {vb}?", lambda N: CMP(("mul", 2, "k"), ">", N), lambda k, N: 2 * k > N),
    "more_half": ("Did more than half of the {g} {vb}?", lambda N: CMP(("mul", 2, "k"), ">", N),
                  lambda k, N: 2 * k > N),
    "at_least_half": ("Did at least half of the {g} {vb}?", lambda N: CMP(("mul", 2, "k"), ">=", N),
                      lambda k, N: 2 * k >= N),
    "fewer_half": ("Did fewer than half of the {g} {vb}?", lambda N: CMP(("mul", 2, "k"), "<", N),
                   lambda k, N: 2 * k < N),
    "two_thirds": ("Did at least two-thirds of the {g} {vb}?", lambda N: CMP(("mul", 3, "k"), ">=", 2 * N),
                   lambda k, N: 3 * k >= 2 * N),
    "three_quarters": ("Did at least three-quarters of the {g} {vb}?", lambda N: CMP(("mul", 4, "k"), ">=", 3 * N),
                       lambda k, N: 4 * k >= 3 * N),
    "most": ("Did most of the {g} {vb}?", lambda N: CMP(("mul", 2, "k"), ">", N), lambda k, N: 2 * k > N),
    "every": ("Did every one of the {g} {vb}?", lambda N: CMP("k", "==", N), lambda k, N: k == N),
    "any": ("Did any of the {g} {vb}?", lambda N: CMP("k", ">=", 1), lambda k, N: k >= 1),
}


def count_text(rng, g, vp, vb, N, k, style):
    if style < 4 and k == 0:
        return f"None of the {N} {g} {vp}."
    if style < 4 and k == N:
        return f"All {N} {g} {vp}."
    if style == 0:
        return f"Of the {N} {g}, {k} {vp}."
    if style == 1:
        return f"{cap(nw(k) if k <= 20 else str(k))} of the {N} {g} {vp}."
    if style == 2:
        return f"{k} out of {N} {g} {vp}."
    if style == 3:
        return f"{N} {g} took part, and {k} of them {vp}."
    if style == 4:
        return f"Result: {k} of {N} {g} {vp}; the other {N - k} did not."
    return f"{N - k} of the {N} {g} did not {vb}; the rest did."


@schema("count_quant", 450)
def s_count(rng):
    g, vp, vb = rng.choice(COUNTS)
    claim = rng.choice(list(C_CLAIMS))
    qt, gb, fn = C_CLAIMS[claim]
    N = rng.randint(6, 40)
    # boundary k: smallest k with fn true (or for 'fewer_half' largest true), then neighbour
    trues = [k for k in range(N + 1) if fn(k, N)]
    falses = [k for k in range(N + 1) if not fn(k, N)]
    if not trues or not falses:
        return None
    if claim == "most":
        ky = [k for k in trues if k / N >= 0.62]
        kn = [k for k in falses if k / N <= 0.5]
        if not ky or not kn:
            return None
        k1, k2 = rng.choice(ky), (N // 2 if rng.random() < 0.6 else rng.choice(kn))
    else:
        # the claim flips between two adjacent counts: the boundary pair
        bpairs = [(a, a + 1) for a in range(N) if fn(a, N) != fn(a + 1, N)]
        a, b = rng.choice(bpairs)
        k1, k2 = (a, b) if rng.random() < 0.5 else (b, a)
    style = rng.randrange(6)
    if style in (4, 5) and (min(k1, k2) == 0 or max(k1, k2) == N):
        style = 0
    q = qt.format(g=g, vb=vb)
    out = []
    for k in (k1, k2):
        out.append(mk(count_text(rng, g, vp, vb, N, k, style), q, "true", "numeric" if style < 5 else "negation",
                      [CMP("k", "==", k)], gb(N), "yes" if fn(k, N) else "no", f"{claim}/s{style}",
                      ints={"k": [0, N]}))
    return out


# ================================================================================================ S03 syllogism instance
SYL = [
    # group NP, pred plural, member sentence, non-member sentence, goal pos, goal neg ; slot {x}
    ("flights to Denver on Tuesday", "were delayed", "Flight {x} flew to Denver on Tuesday.",
     "Flight {x} flew to Denver on Wednesday.", "flight {x} was delayed", "flight {x} was not delayed", "flightno"),
    ("parcels sent by express post last week", "arrived within two days", "Parcel {x} was sent by express post last week.",
     "Parcel {x} was sent by standard post last week.", "parcel {x} arrived within two days",
     "parcel {x} did not arrive within two days", "code"),
    ("apartments on the third floor", "lost power during the storm", "{x} lives in an apartment on the third floor.",
     "{x} lives in an apartment on the fifth floor.", "{x}'s apartment lost power during the storm",
     "{x}'s apartment did not lose power during the storm", "name"),
    ("cars inspected on Monday", "failed the emissions test", "{x}'s car was inspected on Monday.",
     "{x}'s car was inspected on Thursday.", "{x}'s car failed the emissions test",
     "{x}'s car did not fail the emissions test", "name"),
    ("patients seen at the Riverside clinic on Friday", "were offered a flu shot",
     "{x} was seen at the Riverside clinic on Friday.", "{x} was seen at the Hillcrest clinic on Friday.",
     "{x} was offered a flu shot", "{x} was not offered a flu shot", "name"),
    ("trains on the Harbor line this morning", "ran late", "The {x} train ran on the Harbor line this morning.",
     "The {x} train ran on the Coastal line this morning.", "the {x} train ran late", "the {x} train did not run late",
     "time"),
    ("houses on Willow Street", "were checked for water damage", "{x} lives on Willow Street.",
     "{x} lives on Aspen Street.", "{x}'s house was checked for water damage",
     "{x}'s house was not checked for water damage", "name"),
    ("stalls at the Saturday market", "accepted card payments", "{x} runs a stall at the Saturday market.",
     "{x} runs a stall at the Sunday market.", "{x}'s stall accepted card payments",
     "{x}'s stall did not accept card payments", "name"),
    ("customers who called on Monday", "received a callback within an hour", "{x} called on Monday.",
     "{x} called on Tuesday.", "{x} received a callback within an hour",
     "{x} did not receive a callback within an hour", "name"),
    ("rooms on the east corridor", "were repainted in May", "Room {x} is on the east corridor.",
     "Room {x} is on the west corridor.", "Room {x} was repainted in May", "Room {x} was not repainted in May", "room"),
    ("samples from batch 7", "tested positive for mould", "Sample {x} came from batch 7.",
     "Sample {x} came from batch 9.", "sample {x} tested positive for mould",
     "sample {x} did not test positive for mould", "code"),
    ("matches scheduled on the south field", "were moved to the indoor hall",
     "The {x} match was scheduled on the south field.", "The {x} match was scheduled on the north field.",
     "the {x} match was moved to the indoor hall", "the {x} match was not moved to the indoor hall", "agegrp"),
    ("borrowers who returned a book after the due date", "were charged a late fee",
     "{x} returned a book after the due date.", "{x} returned a book before the due date.",
     "{x} was charged a late fee", "{x} was not charged a late fee", "name"),
    ("laptops issued in 2024", "received the security update", "{x}'s laptop was issued in 2024.",
     "{x}'s laptop was issued in 2022.", "{x}'s laptop received the security update",
     "{x}'s laptop did not receive the security update", "name"),
    ("workshops on the Friday programme", "were fully booked", "The {x} workshop is on the Friday programme.",
     "The {x} workshop is on the Saturday programme.", "the {x} workshop was fully booked",
     "the {x} workshop was not fully booked", "topic"),
    ("employees at the Leeds office", "worked from home on Monday", "{x} works at the Leeds office.",
     "{x} works at the York office.", "{x} worked from home on Monday", "{x} did not work from home on Monday", "name"),
    ("vans in the north depot", "had their tyres replaced", "Van {x} is kept in the north depot.",
     "Van {x} is kept in the south depot.", "van {x} had its tyres replaced", "van {x} did not have its tyres replaced",
     "num"),
    ("invoices from Kestrel Electrical", "were paid late", "Invoice {x} came from Kestrel Electrical.",
     "Invoice {x} came from Marlow Timber.", "invoice {x} was paid late", "invoice {x} was not paid late", "num"),
]
TOPICS = ["pottery", "first-aid", "photography", "bread-making", "coding", "woodwork", "public-speaking", "watercolour",
          "bike-repair", "budgeting", "knitting", "beekeeping", "podcasting", "resume-writing"]


def slot(rng, kind):
    if kind == "name":
        return rng.choice(PEOPLE)[0]
    if kind == "flightno":
        return str(rng.randint(102, 989))
    if kind == "code":
        return f"{rng.choice('ABCDEFGHJKLMNPRSTW')}{rng.randint(100, 999)}"
    if kind == "time":
        return f"{rng.randint(6, 9)}:{rng.choice(['05', '12', '18', '24', '30', '36', '42', '48', '55'])}"
    if kind == "room":
        return str(rng.randint(101, 140))
    if kind == "agegrp":
        return f"under-{rng.randint(8, 16)}"
    if kind == "topic":
        return rng.choice(TOPICS)
    if kind == "num":
        return str(rng.randint(1100, 9899))
    raise ValueError(kind)


@schema("syllogism_instance", 420)
def s_syllogism(rng):
    grp, pp, mem, non, gp_, gn, sk = rng.choice(SYL)
    x = slot(rng, sk)
    Q = {"all": rng.choice([f"All of the {grp} {pp}.", f"All {grp} {pp}."]),
         "no": f"None of the {grp} {pp}.", "most": f"Most of the {grp} {pp}.",
         "some": rng.choice([f"Some of the {grp} {pp}.", f"Several of the {grp} {pp}."])}
    var = rng.choice(["all_mem", "no_mem", "all_most", "all_some", "no_all"])
    M, P = "M", "P"
    rule = {"all": IMP(M, P), "no": IMP(M, NOT(P)), "most": True, "some": True}
    if var == "all_mem":
        rows = [("all", True, gp_, P, "yes", "quantifier"), ("all", False, gp_, P, "no", "missing_info")]
    elif var == "no_mem":
        rows = [("no", True, gn, NOT(P), "yes", "negation"), ("no", False, gn, NOT(P), "no", "missing_info")]
    elif var == "all_most":
        rows = [("all", True, gp_, P, "yes", "quantifier"), ("most", True, gp_, P, "no", "quantifier")]
    elif var == "all_some":
        rows = [("all", True, gp_, P, "yes", "quantifier"), ("some", True, gp_, P, "no", "quantifier")]
    else:
        rows = [("no", True, gn, NOT(P), "yes", "negation"), ("all", True, gn, NOT(P), "no", "negation")]
    rng.shuffle(rows)
    order = rng.random() < 0.8
    doc = rng.choice(["text", "report", "summary"])
    q = cert_q(rng, doc, rows[0][2].format(x=x))
    out = []
    for qu, is_mem, gs, goal, gold, edge in rows:
        fact = (mem if is_mem else non).format(x=x)
        st = f"{Q[qu]} {fact}" if order else f"{fact} {Q[qu]}"
        prem = [lit(M, is_mem)] + ([rule[qu]] if rule[qu] is not True else [])
        out.append(mk(st, q, "certain", edge, prem, goal, gold, f"{var}/{qu}"))
    return out


# ================================================================================================ S04 only vs all
ONLY = [
    # group, member sentence, member goal, event plural, event singular (after 'Nobody except X'), event sentence, goal
    ("gold-card members", "{x} is a gold-card member.", "{x} is a gold-card member", "were admitted to the lounge",
     "was admitted to the lounge", "{x} was admitted to the lounge.", "{x} was admitted to the lounge"),
    ("staff with a red badge", "{x} has a red badge.", "{x} has a red badge", "were allowed into the server room",
     "was allowed into the server room", "{x} was allowed into the server room.", "{x} was allowed into the server room"),
    ("students who scored above 90", "{x} scored above 90.", "{x} scored above 90", "received a merit certificate",
     "received a merit certificate", "{x} received a merit certificate.", "{x} received a merit certificate"),
    ("residents of Zone B", "{x} is a resident of Zone B.", "{x} is a resident of Zone B",
     "were issued a parking permit", "was issued a parking permit", "{x} was issued a parking permit.",
     "{x} was issued a parking permit"),
    ("passengers with a printed boarding pass", "{x} had a printed boarding pass.", "{x} had a printed boarding pass",
     "were let through Gate 4", "was let through Gate 4", "{x} was let through Gate 4.", "{x} was let through Gate 4"),
    ("employees who worked the holiday shift", "{x} worked the holiday shift.", "{x} worked the holiday shift",
     "received a bonus", "received a bonus", "{x} received a bonus.", "{x} received a bonus"),
    ("customers who ordered before Friday", "{x} ordered before Friday.", "{x} ordered before Friday",
     "got the free gift", "got the free gift", "{x} got the free gift.", "{x} got the free gift"),
    ("members who paid the annual fee", "{x} paid the annual fee.", "{x} paid the annual fee",
     "were invited to the annual meeting", "was invited to the annual meeting", "{x} was invited to the annual meeting.",
     "{x} was invited to the annual meeting"),
    ("patients over 65", "{x} is over 65.", "{x} is over 65", "were offered the new vaccine",
     "was offered the new vaccine", "{x} was offered the new vaccine.", "{x} was offered the new vaccine"),
    ("volunteers who completed the training", "{x} completed the training.", "{x} completed the training",
     "were assigned a delivery route", "was assigned a delivery route", "{x} was assigned a delivery route.",
     "{x} was assigned a delivery route"),
    ("tenants who signed the new lease", "{x} signed the new lease.", "{x} signed the new lease",
     "got a new key fob", "got a new key fob", "{x} got a new key fob.", "{x} got a new key fob"),
    ("drivers with a clean record", "{x} has a clean record.", "{x} has a clean record",
     "were offered the insurance discount", "was offered the insurance discount",
     "{x} was offered the insurance discount.", "{x} was offered the insurance discount"),
    ("applicants who sent a portfolio", "{x} sent a portfolio.", "{x} sent a portfolio", "were invited to interview",
     "was invited to interview", "{x} was invited to interview.", "{x} was invited to interview"),
    ("guests who booked the spa package", "{x} booked the spa package.", "{x} booked the spa package",
     "were given a late checkout", "was given a late checkout", "{x} was given a late checkout.",
     "{x} was given a late checkout"),
    ("runners who finished under four hours", "{x} finished under four hours.", "{x} finished under four hours",
     "received a gold medal", "received a gold medal", "{x} received a gold medal.", "{x} received a gold medal"),
]


@schema("only_vs_all", 330)
def s_only_all(rng):
    grp, ms, mg, ep, es, evs, eg = rng.choice(ONLY)
    x = rng.choice(PEOPLE)[0]
    only_s = rng.choice([f"Only {grp} {ep}.", f"Nobody except {grp} {es}.", f"No one other than {grp} {es}."])
    all_s = rng.choice([f"All {grp} {ep}.", f"All of the {grp} {ep}.", f"Every one of the {grp} {es}."])
    M, E = "M", "E"
    var = rng.choice(["converse", "direct"])
    if var == "converse":  # fact: event; question: membership
        fact, goal, qs = evs.format(x=x), M, mg.format(x=x)
        rows = [(only_s, IMP(E, M), "yes", "quantifier"), (all_s, IMP(M, E), "no", "missing_info")]
        pf = E
    else:
        fact, goal, qs = ms.format(x=x), E, eg.format(x=x)
        rows = [(only_s, IMP(E, M), "no", "missing_info"), (all_s, IMP(M, E), "yes", "quantifier")]
        pf = M
    rng.shuffle(rows)
    q = cert_q(rng, rng.choice(["text", "notice", "report"]), qs)
    return [mk(f"{r} {fact}", q, "certain", ed, [pf, f], goal, g, f"{var}") for r, f, g, ed in rows]


# ================================================================================================ S05 'only' focus (deontic)
FOCUS = [
    # r1 (only role), r2 (role only scope), scenario A: role outside scope (violates r2), scenario B: non-role in scope
    ("Only managers may approve refunds over $500.", "Managers may approve only refunds over $500.",
     lambda x, r: f"{x}, a manager, approved a refund of ${r.choice([120, 250, 300, 480, 500])}.",
     lambda x, r: f"{x}, a cashier, approved a refund of ${r.choice([520, 650, 900, 1200])}."),
    ("Only seniors may park in Lot C.", "Seniors may park only in Lot C.",
     lambda x, r: f"{x}, a senior, parked in Lot {r.choice('ABDE')}.",
     lambda x, r: f"{x}, a {r.choice(['junior', 'sophomore'])}, parked in Lot C."),
    ("Only members may use the pool before 8 a.m.", "Members may use the pool only before 8 a.m.",
     lambda x, r: f"{x}, a member, used the pool at {r.choice([9, 10, 11])} a.m.",
     lambda x, r: f"{x}, a day visitor, used the pool at {r.choice([6, 7])} a.m."),
    ("Only nurses may give injections in Ward 4.", "Nurses may give injections only in Ward 4.",
     lambda x, r: f"{x}, a nurse, gave an injection in Ward {r.choice([1, 2, 3, 5, 6])}.",
     lambda x, r: f"{x}, a care assistant, gave an injection in Ward 4."),
    ("Only registered voters may sign the petition online.", "Registered voters may sign the petition only online.",
     lambda x, r: f"{x}, a registered voter, signed the petition on paper.",
     lambda x, r: f"{x}, who is not a registered voter, signed the petition online."),
    ("Only coaches may enter the pitch at half-time.", "Coaches may enter the pitch only at half-time.",
     lambda x, r: f"{x}, a coach, entered the pitch during the {r.choice(['first', 'second'])} half.",
     lambda x, r: f"{x}, a parent, entered the pitch at half-time."),
    ("Only pharmacists may hand out antibiotics at the counter.",
     "Pharmacists may hand out antibiotics only at the counter.",
     lambda x, r: f"{x}, a pharmacist, handed out antibiotics at the drive-through window.",
     lambda x, r: f"{x}, a shop assistant, handed out antibiotics at the counter."),
    ("Only interns may use the shared desks on Fridays.", "Interns may use the shared desks only on Fridays.",
     lambda x, r: f"{x}, an intern, used a shared desk on {r.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday'])}.",
     lambda x, r: f"{x}, a senior analyst, used a shared desk on Friday."),
    ("Only guests with a wristband may swim after sunset.", "Guests with a wristband may swim only after sunset.",
     lambda x, r: f"{x}, a guest with a wristband, swam at {r.choice(['noon', '3 p.m.', '10 a.m.'])}.",
     lambda x, r: f"{x}, a guest without a wristband, swam after sunset."),
    ("Only volunteers may hand out food on Saturdays.", "Volunteers may hand out food only on Saturdays.",
     lambda x, r: f"{x}, a volunteer, handed out food on {r.choice(['Wednesday', 'Sunday', 'Monday'])}.",
     lambda x, r: f"{x}, a paid staff member, handed out food on Saturday."),
    ("Only supervisors may open the safe after closing time.", "Supervisors may open the safe only after closing time.",
     lambda x, r: f"{x}, a supervisor, opened the safe at {r.choice(['2 p.m.', '11 a.m.', '4 p.m.'])}, before closing time.",
     lambda x, r: f"{x}, a cashier, opened the safe after closing time."),
    ("Only residents may use the car park at night.", "Residents may use the car park only at night.",
     lambda x, r: f"{x}, a resident, parked in the car park at midday.",
     lambda x, r: f"{x}, a visitor, parked in the car park at {r.choice(['11 p.m.', 'midnight', '2 a.m.'])}."),
    ("Only team leads may book the large meeting room on Mondays.",
     "Team leads may book the large meeting room only on Mondays.",
     lambda x, r: f"{x}, a team lead, booked the large meeting room for {r.choice(['Tuesday', 'Thursday', 'Friday'])}.",
     lambda x, r: f"{x}, an analyst, booked the large meeting room for Monday."),
    ("Only drivers over 25 may rent the vans at weekends.", "Drivers over 25 may rent the vans only at weekends.",
     lambda x, r: f"{x}, who is {r.choice([28, 31, 40, 52])}, rented a van on a {r.choice(['Tuesday', 'Wednesday'])}.",
     lambda x, r: f"{x}, who is {r.choice([21, 22, 23])}, rented a van on a Saturday."),
    ("Only staff with a forklift licence may move pallets in Aisle 9.",
     "Staff with a forklift licence may move pallets only in Aisle 9.",
     lambda x, r: f"{x}, who has a forklift licence, moved pallets in Aisle {r.choice([2, 3, 5, 7])}.",
     lambda x, r: f"{x}, who has no forklift licence, moved pallets in Aisle 9."),
]


@schema("only_focus", 330)
def s_only_focus(rng):
    r1, r2, sa, sb = rng.choice(FOCUS)
    x = rng.choice(PEOPLE)[0]
    R, S = "R", "S"
    if rng.random() < 0.5:
        scen, facts = sa(x, rng), [R, NOT(S)]
        rows = [(r1, AND(S, NOT(R)), "no"), (r2, AND(R, NOT(S)), "yes")]
    else:
        scen, facts = sb(x, rng), [NOT(R), S]
        rows = [(r1, AND(S, NOT(R)), "yes"), (r2, AND(R, NOT(S)), "no")]
    rng.shuffle(rows)
    q = rng.choice([f"Did {x} break the rule?", f"Did {x} break the rule as it is written?",
                    f"Does what {x} did go against the rule?"])
    hdr = header(rng, RULE_HDR, 0.3)
    return [mk(f"{hdr}{r} {scen}", q, "violate", "exception", facts, v, g, "A" if R in facts else "B")
            for r, v, g in rows]


# ================================================================================================ S06/S07 conditionals
# if1 = "C if A." (derive 'only if' / 'if and only if' by replacing ' if ' once), if2 = "If A, C.",
# oi2 = "Only ... ." (only-if paraphrase), conv = "If C, A." (converse), inst kind, A, notA, C, notC
COND = [
    ("A parcel ships by freight if it weighs more than 20 kg.", "If a parcel weighs more than 20 kg, it ships by freight.",
     "Only parcels that weigh more than 20 kg ship by freight.",
     "If a parcel ships by freight, it weighs more than 20 kg.", "code",
     "parcel {x} weighs more than 20 kg", "parcel {x} does not weigh more than 20 kg", "parcel {x} ships by freight",
     "parcel {x} does not ship by freight"),
    ("A customer gets free delivery if their order is over $40.",
     "If a customer's order is over $40, the customer gets free delivery.",
     "Only customers whose order is over $40 get free delivery.",
     "If a customer gets free delivery, their order is over $40.", "name",
     "{x}'s order is over $40", "{x}'s order is not over $40", "{x} gets free delivery",
     "{x} does not get free delivery"),
    ("An account is locked if it has five failed login attempts in a row.",
     "If an account has five failed login attempts in a row, it is locked.",
     "Only accounts with five failed login attempts in a row are locked.",
     "If an account is locked, it has had five failed login attempts in a row.", "name",
     "{x}'s account had five failed login attempts in a row", "{x}'s account did not have five failed login attempts in a row",
     "{x}'s account is locked", "{x}'s account is not locked"),
    ("A student is placed in the advanced group if they score above 85 on the entry test.",
     "If a student scores above 85 on the entry test, they are placed in the advanced group.",
     "Only students who score above 85 on the entry test are placed in the advanced group.",
     "If a student is placed in the advanced group, they scored above 85 on the entry test.", "name",
     "{x} scored above 85 on the entry test", "{x} did not score above 85 on the entry test",
     "{x} is placed in the advanced group", "{x} is not placed in the advanced group"),
    ("A match is moved indoors if it is raining at kick-off.", "If it is raining at kick-off, the match is moved indoors.",
     "Only matches with rain at kick-off are moved indoors.",
     "If a match is moved indoors, it was raining at kick-off.", "match",
     "it was raining when {x} kicked off", "it was not raining when {x} kicked off", "{x} was moved indoors",
     "{x} was not moved indoors"),
    ("An employee receives overtime pay if they work more than 40 hours in a week.",
     "If an employee works more than 40 hours in a week, they receive overtime pay.",
     "Only employees who work more than 40 hours in a week receive overtime pay.",
     "If an employee receives overtime pay, they worked more than 40 hours that week.", "name",
     "{x} worked more than 40 hours last week", "{x} did not work more than 40 hours last week",
     "{x} receives overtime pay for last week", "{x} does not receive overtime pay for last week"),
    ("A flight departs from Terminal 2 if it is an international flight.",
     "If a flight is an international flight, it departs from Terminal 2.",
     "Only international flights depart from Terminal 2.",
     "If a flight departs from Terminal 2, it is an international flight.", "flight",
     "Flight {x} is an international flight", "Flight {x} is not an international flight",
     "Flight {x} departs from Terminal 2", "Flight {x} does not depart from Terminal 2"),
    ("A loan application goes to manual review if the amount is over $250,000.",
     "If the amount on a loan application is over $250,000, it goes to manual review.",
     "Only loan applications for over $250,000 go to manual review.",
     "If a loan application goes to manual review, the amount is over $250,000.", "name",
     "{x}'s loan application is for over $250,000", "{x}'s loan application is not for over $250,000",
     "{x}'s loan application goes to manual review", "{x}'s loan application does not go to manual review"),
    ("A borrower is charged a fine if they return a book late.",
     "If a borrower returns a book late, they are charged a fine.",
     "Only borrowers who return a book late are charged a fine.",
     "If a borrower is charged a fine, they returned a book late.", "name",
     "{x} returned a book late", "{x} did not return a book late", "{x} is charged a fine",
     "{x} is not charged a fine"),
    ("An applicant is invited to interview if they pass the written test.",
     "If an applicant passes the written test, they are invited to interview.",
     "Only applicants who pass the written test are invited to interview.",
     "If an applicant is invited to interview, they passed the written test.", "name",
     "{x} passed the written test", "{x} did not pass the written test", "{x} is invited to interview",
     "{x} is not invited to interview"),
    ("A guest gets a late checkout if they are a platinum member.",
     "If a guest is a platinum member, they get a late checkout.",
     "Only guests who are platinum members get a late checkout.",
     "If a guest gets a late checkout, they are a platinum member.", "name",
     "{x} is a platinum member", "{x} is not a platinum member", "{x} gets a late checkout",
     "{x} does not get a late checkout"),
    ("A car is towed if it is parked in the fire lane.", "If a car is parked in the fire lane, it is towed.",
     "Only cars parked in the fire lane are towed.", "If a car is towed, it was parked in the fire lane.", "name",
     "{x}'s car is parked in the fire lane", "{x}'s car is not parked in the fire lane", "{x}'s car is towed",
     "{x}'s car is not towed"),
    ("A package requires a signature if it is insured.", "If a package is insured, it requires a signature.",
     "Only insured packages require a signature.", "If a package requires a signature, it is insured.", "code",
     "package {x} is insured", "package {x} is not insured", "package {x} requires a signature",
     "package {x} does not require a signature"),
    ("A player is suspended for the next match if they receive a red card.",
     "If a player receives a red card, they are suspended for the next match.",
     "Only players who receive a red card are suspended for the next match.",
     "If a player is suspended for the next match, they received a red card.", "name",
     "{x} received a red card", "{x} did not receive a red card", "{x} is suspended for the next match",
     "{x} is not suspended for the next match"),
    ("An order is refunded in full if it is cancelled within 24 hours.",
     "If an order is cancelled within 24 hours, it is refunded in full.",
     "Only orders cancelled within 24 hours are refunded in full.",
     "If an order is refunded in full, it was cancelled within 24 hours.", "order",
     "order #{x} was cancelled within 24 hours", "order #{x} was not cancelled within 24 hours",
     "order #{x} is refunded in full", "order #{x} is not refunded in full"),
    ("A claim is paid within 10 days if it is filed online.", "If a claim is filed online, it is paid within 10 days.",
     "Only claims filed online are paid within 10 days.", "If a claim is paid within 10 days, it was filed online.",
     "num", "claim {x} was filed online", "claim {x} was not filed online", "claim {x} is paid within 10 days",
     "claim {x} is not paid within 10 days"),
    ("A phone gets the update if it runs version 12 or later.", "If a phone runs version 12 or later, it gets the update.",
     "Only phones running version 12 or later get the update.", "If a phone gets the update, it runs version 12 or later.",
     "name", "{x}'s phone runs version 12 or later", "{x}'s phone does not run version 12 or later",
     "{x}'s phone gets the update", "{x}'s phone does not get the update"),
    ("A child rides the bus free if they are under five.", "If a child is under five, they ride the bus free.",
     "Only children under five ride the bus free.", "If a child rides the bus free, they are under five.", "name",
     "{x} is under five", "{x} is not under five", "{x} rides the bus free", "{x} does not ride the bus free"),
    ("A volunteer receives a certificate if they complete 20 hours of service.",
     "If a volunteer completes 20 hours of service, they receive a certificate.",
     "Only volunteers who complete 20 hours of service receive a certificate.",
     "If a volunteer receives a certificate, they completed 20 hours of service.", "name",
     "{x} completed 20 hours of service", "{x} did not complete 20 hours of service", "{x} receives a certificate",
     "{x} does not receive a certificate"),
    ("An email goes to quarantine if it has an executable attachment.",
     "If an email has an executable attachment, it goes to quarantine.",
     "Only emails with an executable attachment go to quarantine.",
     "If an email goes to quarantine, it has an executable attachment.", "name",
     "the email from {x} has an executable attachment", "the email from {x} does not have an executable attachment",
     "the email from {x} goes to quarantine", "the email from {x} does not go to quarantine"),
    ("A dish is marked spicy on the menu if it contains chilli.",
     "If a dish contains chilli, it is marked spicy on the menu.",
     "Only dishes that contain chilli are marked spicy on the menu.",
     "If a dish is marked spicy on the menu, it contains chilli.", "dish",
     "the {x} contains chilli", "the {x} does not contain chilli", "the {x} is marked spicy on the menu",
     "the {x} is not marked spicy on the menu"),
    ("A passenger boards first if they are travelling with a child under two.",
     "If a passenger is travelling with a child under two, they board first.",
     "Only passengers travelling with a child under two board first.",
     "If a passenger boards first, they are travelling with a child under two.", "name",
     "{x} is travelling with a child under two", "{x} is not travelling with a child under two", "{x} boards first",
     "{x} does not board first"),
    ("A member gets 10% off if they show their card at the till.",
     "If a member shows their card at the till, they get 10% off.",
     "Only members who show their card at the till get 10% off.",
     "If a member gets 10% off, they showed their card at the till.", "name",
     "{x} showed the membership card at the till", "{x} did not show the membership card at the till",
     "{x} gets 10% off", "{x} does not get 10% off"),
    ("A shipment is labelled hazardous if it contains lithium batteries.",
     "If a shipment contains lithium batteries, it is labelled hazardous.",
     "Only shipments containing lithium batteries are labelled hazardous.",
     "If a shipment is labelled hazardous, it contains lithium batteries.", "code",
     "shipment {x} contains lithium batteries", "shipment {x} does not contain lithium batteries",
     "shipment {x} is labelled hazardous", "shipment {x} is not labelled hazardous"),
]
DISHES = ["lamb curry", "bean soup", "noodle salad", "fish stew", "vegetable tagine", "pork dumplings", "chicken wrap",
          "tofu stir-fry", "black-bean burger", "prawn laksa", "lentil dal", "beef chilli pot"]
MATCHES = ["Saturday's match", "the under-14 final", "Sunday's league game", "the charity match", "Friday's cup tie",
           "the veterans' game"]


def cslot(rng, kind):
    if kind == "match":
        return rng.choice(MATCHES)
    if kind == "flight":
        return str(rng.randint(102, 989))
    if kind == "order":
        return str(rng.randint(10000, 99999))
    if kind == "dish":
        return rng.choice(DISHES)
    return slot(rng, kind)


def sent(s):
    return cap(s) + "."


def end(s):
    return s if s.endswith(".") else s + "."


@schema("cond_if_onlyif", 560)
def s_cond(rng):
    if1, if2, oi2, conv, sk, A, nA, C, nC = rng.choice(COND)
    x = cslot(rng, sk)
    f = lambda s: s.format(x=x)
    assert if1.count(" if ") == 1
    only_if = rng.choice([if1.replace(" if ", " only if "), oi2])
    iff = if1.replace(" if ", " if, and only if, ")
    var = rng.choice(["AC", "MP", "DA", "MT"])
    minimal = rng.random() < 0.7  # prefer twins that differ only by 'if' -> 'only if' / 'if, and only if,'
    if minimal:
        only_if = if1.replace(" if ", " only if ")
    a, c = "A", "C"
    F_IF, F_OI, F_IFF = IMP(a, c), IMP(c, a), IFF(a, c)
    ifs = [if1] if minimal else [if1, if2]
    if var == "AC":    # fact C, question A
        fact, goal, qs, edge = f(C), a, f(A), "hypothetical"
        cand = [(rng.choice(ifs), F_IF, "no"), (rng.choice([only_if, iff]), None, "yes")]
    elif var == "MP":  # fact A, question C
        fact, goal, qs, edge = f(A), c, f(C), "hypothetical"
        cand = [(rng.choice(ifs + [iff]), None, "yes"), (only_if, F_OI, "no")]
    elif var == "DA":  # fact not A, question not C
        fact, goal, qs, edge = f(nA), NOT(c), f(nC), "negation"
        cand = [(rng.choice(ifs), F_IF, "no"), (rng.choice([only_if, iff]), None, "yes")]
    else:              # MT: fact not C, question not A
        fact, goal, qs, edge = f(nC), NOT(a), f(nA), "negation"
        cand = [(rng.choice(ifs + [iff]), None, "yes"), (only_if, F_OI, "no")]
    pf = {"AC": c, "MP": a, "DA": NOT(a), "MT": NOT(c)}[var]
    out_rows = []
    for rule, form, gold in cand:
        if form is None:
            form = F_IFF if rule == iff else (F_OI if rule in (only_if, oi2) else F_IF)
        out_rows.append((rule, form, gold))
    rng.shuffle(out_rows)
    doc = rng.choice(["rule", "text", "notice"])
    q = cert_q(rng, doc, qs)
    hdr = header(rng, RULE_HDR, 0.25)
    out = []
    for rule, form, gold in out_rows:
        kind = "iff" if rule == iff else ("onlyif" if form == F_OI else "if")
        out.append(mk(f"{hdr}{rule} {sent(fact)}", q, "certain", edge, [pf, form], goal, gold, f"{var}/{kind}"))
    return out


@schema("cond_converse", 300)
def s_cond_conv(rng):
    if1, if2, oi2, conv, sk, A, nA, C, nC = rng.choice(COND)
    x = cslot(rng, sk)
    f = lambda s: s.format(x=x)
    a, c = "A", "C"
    var = rng.choice(["MT", "MP"])
    if var == "MT":
        fact, pf, goal, qs, edge = f(nC), NOT(c), NOT(a), f(nA), "negation"
    else:
        fact, pf, goal, qs, edge = f(A), a, c, f(C), "hypothetical"
    rows = [(if2, IMP(a, c), "yes"), (conv, IMP(c, a), "no")]
    rng.shuffle(rows)
    q = cert_q(rng, rng.choice(["rule", "text"]), qs)
    return [mk(f"{r} {sent(fact)}", q, "certain", edge, [pf, form], goal, g, f"{var}/{'fwd' if g == 'yes' else 'conv'}")
            for r, form, g in rows]


# ================================================================================================ S45 even if / only if not
EVENIF = [
    ("The ferry runs even if it rains.", "The ferry runs only if it does not rain.", "It rained on {day}.",
     "the ferry ran on {day}"),
    ("The gym stays open even if it snows.", "The gym stays open only if it does not snow.", "It snowed on {day}.",
     "the gym stayed open on {day}"),
    ("The outdoor market goes ahead even if the temperature drops below freezing.",
     "The outdoor market goes ahead only if the temperature does not drop below freezing.",
     "On {day} the temperature dropped below freezing.", "the outdoor market went ahead on {day}"),
    ("The school bus runs even if there is a teachers' strike.",
     "The school bus runs only if there is no teachers' strike.", "There was a teachers' strike on {day}.",
     "the school bus ran on {day}"),
    ("The parade goes ahead even if it is windy.", "The parade goes ahead only if it is not windy.",
     "It was windy on the day of the {pl} parade.", "the {pl} parade went ahead"),
    ("Deliveries are made even if the recipient is not at home.",
     "Deliveries are made only if the recipient is at home.", "{x} was not at home when the courier came.",
     "the delivery to {x} was made"),
    ("The concert starts on time even if the support act is late.",
     "The concert starts on time only if the support act is not late.", "The support act was late on {day}.",
     "{day}'s concert started on time"),
    ("The trail stays open even if there has been heavy rain.",
     "The trail stays open only if there has not been heavy rain.", "There was heavy rain near {pl} overnight.",
     "the trail near {pl} stayed open this morning"),
    ("Payroll runs on the 25th even if the 25th falls on a weekend.",
     "Payroll runs on the 25th only if the 25th does not fall on a weekend.",
     "In {mon} the 25th falls on a Saturday.", "payroll runs on the 25th in {mon}"),
    ("The clinic sees walk-in patients even if all appointments are booked.",
     "The clinic sees walk-in patients only if not all appointments are booked.",
     "On {day} all appointments were booked.", "the clinic saw walk-in patients on {day}"),
    ("The library lends laptops even if the borrower has an overdue book.",
     "The library lends laptops only if the borrower does not have an overdue book.", "{x} has an overdue book.",
     "the library lends {x} a laptop"),
    ("The race is held even if fewer than 50 runners sign up.",
     "The race is held only if at least 50 runners sign up.", "Only {n} runners signed up for the {pl} race.",
     "the {pl} race was held"),
    ("Refunds are issued even if the receipt has been lost.",
     "Refunds are issued only if the receipt has not been lost.", "{x} has lost the receipt.",
     "{x} is issued a refund"),
    ("The parcel locker accepts parcels even if they are marked fragile.",
     "The parcel locker accepts parcels only if they are not marked fragile.", "{x}'s parcel is marked fragile.",
     "the parcel locker accepts {x}'s parcel"),
    ("The museum opens on Mondays even if it is a public holiday.",
     "The museum opens on Mondays only if it is not a public holiday.", "Next Monday is a public holiday.",
     "the museum opens next Monday"),
    ("Members can bring a guest even if the club is fully booked.",
     "Members can bring a guest only if the club is not fully booked.", "The club is fully booked on {day}.",
     "members can bring a guest on {day}"),
    ("The mortgage rate stays fixed even if the central bank raises rates.",
     "The mortgage rate stays fixed only if the central bank does not raise rates.",
     "The central bank raised rates in {mon}.", "the mortgage rate stayed fixed after {mon}"),
    ("The training session runs even if fewer than five people turn up.",
     "The training session runs only if at least five people turn up.", "Only three people turned up on {day}.",
     "the training session ran on {day}"),
    ("The warranty covers the phone even if it has been dropped.",
     "The warranty covers the phone only if it has not been dropped.", "{x}'s phone has been dropped.",
     "the warranty covers {x}'s phone"),
    ("Tenants get their deposit back even if they leave before the lease ends.",
     "Tenants get their deposit back only if they do not leave before the lease ends.",
     "{x} left two months before the lease ended.", "{x} gets the deposit back"),
    ("The school stays open even if the heating fails.", "The school stays open only if the heating does not fail.",
     "The heating at {pl} School failed on {day}.", "{pl} School stayed open on {day}"),
    ("Flights board on time even if the gate changes.", "Flights board on time only if the gate does not change.",
     "The gate for flight {fl} changed.", "flight {fl} boarded on time"),
    ("The team bonus is paid even if the team misses its target.",
     "The team bonus is paid only if the team does not miss its target.",
     "The {dept} team missed its target this quarter.", "the {dept} team's bonus is paid this quarter"),
    ("The festival goes ahead even if the tickets do not sell out.",
     "The festival goes ahead only if the tickets sell out.", "Tickets for the {pl} festival did not sell out.",
     "the {pl} festival went ahead"),
    ("The evening course runs even if the tutor is ill.", "The evening course runs only if the tutor is not ill.",
     "The tutor was ill on {day}.", "the evening course ran on {day}"),
    ("Emails are archived even if they are marked private.",
     "Emails are archived only if they are not marked private.", "The email from {x} was marked private.",
     "the email from {x} was archived"),
    ("The pharmacy delivers even if the order is under $20.",
     "The pharmacy delivers only if the order is not under $20.", "{x}'s order came to ${small}.",
     "the pharmacy delivers {x}'s order"),
    ("The lifeguards stay on duty even if the beach is quiet.",
     "The lifeguards stay on duty only if the beach is not quiet.", "The beach at {pl} was quiet on {day}.",
     "the lifeguards at {pl} stayed on duty on {day}"),
]
DEPTS_A = ["design", "finance", "sales", "support", "legal", "research", "logistics", "marketing"]


@schema("even_if", 250)
def s_even_if(rng):
    ev_, oi, fact, goal = rng.choice(EVENIF)
    sl = dict(x=rng.choice(PEOPLE)[0], day=rng.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                                                        "Saturday", "Sunday"]),
              pl=rng.choice(PLACES), mon=rng.choice(["March", "April", "October", "January", "June", "September"]),
              n=rng.randint(12, 49), fl=f"{rng.choice(['NR', 'QV', 'TX', 'LM'])}{rng.randint(100, 999)}",
              dept=rng.choice(DEPTS_A), small=rng.randint(6, 19))
    fact, goal = fact.format(**sl), goal.format(**sl)
    R, C = "R", "C"
    rows = [(ev_, [IMP(R, C), IMP(NOT(R), C)], "yes"), (oi, [IMP(C, NOT(R))], "no")]
    rng.shuffle(rows)
    q = cert_q(rng, rng.choice(["text", "rule", "notice"]), goal)
    return [mk(f"{r} {fact}", q, "certain", "hypothetical", [R] + fs, C, g, "evenif" if g == "yes" else "onlyifnot")
            for r, fs, g in rows]


# ================================================================================================ S08 unless (factual)
UNLESS = [
    # C (main clause, sentence-case), X (unless-clause), fact X true, fact X false, question goal, double-neg?
    ("The pool closes at 8 p.m.", "a lifeguard is on duty", "Tonight a lifeguard is on duty.",
     "Tonight no lifeguard is on duty.", "the pool closes at 8 p.m. tonight", False),
    ("The shuttle runs every 20 minutes", "it is a public holiday", "Monday is a public holiday.",
     "Monday is not a public holiday.", "the shuttle runs every 20 minutes on Monday", False),
    ("Classes start at 9 a.m.", "the school announces a delayed opening",
     "The school has announced a delayed opening for Thursday.",
     "The school has not announced a delayed opening for Thursday.", "classes start at 9 a.m. on Thursday", False),
    ("Orders are shipped the same day", "they are placed after 3 p.m.", "Order #{n} was placed at {late}.",
     "Order #{n} was placed at {early}.", "order #{n} is shipped the same day", False),
    ("The library stays open until 10 p.m.", "it is a holiday week", "This week is a holiday week.",
     "This week is not a holiday week.", "the library stays open until 10 p.m. this week", False),
    ("Staff get a free lunch on Fridays", "the canteen is closed", "This Friday the canteen is closed.",
     "This Friday the canteen is open.", "staff get a free lunch this Friday", False),
    ("The ferry leaves at 7 a.m.", "the harbour master issues a wind warning",
     "Today the harbour master issued a wind warning.", "Today the harbour master did not issue a wind warning.",
     "the ferry leaves at 7 a.m. today", False),
    ("Parking in Zone C is free at weekends", "there is a home game at the stadium",
     "There is a home game at the stadium this Saturday.", "There is no home game at the stadium this Saturday.",
     "parking in Zone C is free this Saturday", False),
    ("New hires start on the first Monday of the month", "their background check is still pending",
     "{x}'s background check is still pending.", "{x}'s background check is complete.",
     "{x} starts on the first Monday of the month", False),
    ("The weekly report goes out on Friday", "the team lead is on leave", "This week the team lead is on leave.",
     "This week the team lead is not on leave.", "the weekly report goes out this Friday", False),
    ("Guests receive a welcome drink", "they booked through a third-party website",
     "{x} booked through a third-party website.", "{x} did not book through a third-party website.",
     "{x} receives a welcome drink", False),
    ("The heating comes on at 6 a.m.", "the outside temperature is above 15°C",
     "This morning the outside temperature was {warm}°C.", "This morning the outside temperature was {cold}°C.",
     "the heating came on at 6 a.m. this morning", False),
    ("Members can bring a guest", "it is a tournament day", "Saturday is a tournament day.",
     "Saturday is not a tournament day.", "members can bring a guest on Saturday", False),
    ("The discount applies", "the invoice is not paid within 10 days", "Invoice {n} was not paid within 10 days.",
     "Invoice {n} was paid within {d} days.", "the discount applies to invoice {n}", True),
    ("Your place on the course is kept", "you have not confirmed by Friday",
     "{x} has not confirmed, and Friday has passed.", "{x} confirmed on Wednesday.",
     "{x}'s place on the course is kept", True),
    ("The warranty remains valid", "the product is not registered within 30 days",
     "{x} did not register the product within 30 days.", "{x} registered the product {d} days after buying it.",
     "the warranty on {x}'s product remains valid", True),
    ("A seat is held for each speaker", "the speaker has not replied to the invitation",
     "{x}, one of the speakers, has not replied to the invitation.",
     "{x}, one of the speakers, has replied to the invitation.", "a seat is held for {x}", True),
    ("Library cards renew automatically", "the holder has not updated their address",
     "{x} has not updated {p} address.", "{x} has updated {p} address.", "{x}'s library card renews automatically",
     True),
    ("Bins are collected on Tuesday", "Monday is a public holiday", "This week Monday is a public holiday.",
     "This week Monday is not a public holiday.", "bins are collected on Tuesday this week", False),
    ("The café offers free refills", "it is the weekend", "Today is Saturday.", "Today is Wednesday.",
     "the café offers free refills today", False),
    ("Trains stop at {pl}", "there are engineering works", "There are engineering works at {pl} this Sunday.",
     "There are no engineering works at {pl} this Sunday.", "trains stop at {pl} this Sunday", False),
    ("The outdoor pool opens at 7 a.m.", "the water is below 18°C", "This morning the water is {cool}°C.",
     "This morning the water is {mild}°C.", "the outdoor pool opens at 7 a.m. this morning", False),
    ("Orders over $50 ship free", "they are going overseas", "{x}'s $80 order is going overseas.",
     "{x}'s $80 order is going to an address in the same town.", "{x}'s order ships free", False),
    ("Lessons are held in the main hall", "the hall is booked for exams", "The main hall is booked for exams on {day}.",
     "The main hall is not booked for exams on {day}.", "lessons are held in the main hall on {day}", False),
    ("Patients are seen in order of arrival", "their case is urgent", "{x}'s case is urgent.",
     "{x}'s case is not urgent.", "{x} is seen in order of arrival", False),
    ("Loyalty points stay valid", "the member has not made a purchase in the past year",
     "{x} has not made a purchase in the past year.", "{x} made a purchase in {mon}, within the past year.",
     "{x}'s loyalty points stay valid", True),
    ("The discount code works", "it has not been activated", "{x}'s discount code has not been activated.",
     "{x}'s discount code has been activated.", "{x}'s discount code works", True),
    ("Members keep their locker", "they have not paid the locker fee by March",
     "{x} has not paid the locker fee, and March has passed.", "{x} paid the locker fee in January.",
     "{x} keeps the locker", True),
    ("The night bus runs every 30 minutes", "there is a football match at the stadium",
     "There is a football match at the stadium on {day}.", "There is no football match at the stadium on {day}.",
     "the night bus runs every 30 minutes on {day}", False),
    ("Visitors may park in the staff car park at weekends", "there is a staff training day",
     "{x} is visiting on a {wkend} when there is a staff training day.",
     "{x} is visiting on a {wkend} when there is no staff training day.",
     "{x} may park in the staff car park on that visit", False),
]


@schema("unless", 380)
def s_unless(rng):
    Cc, X, fx, fnx, goal, dneg = rng.choice(UNLESS)
    pp = rng.choice(PEOPLE)
    subs = dict(x=pp[0], p=pp[3], n=str(rng.randint(1000, 9999)), d=str(rng.randint(2, 9)),
                late=rng.choice(["3:20 p.m.", "4:10 p.m.", "5:45 p.m.", "3:05 p.m."]),
                early=rng.choice(["1:25 p.m.", "9:40 a.m.", "2:50 p.m.", "11:15 a.m."]),
                warm=str(rng.randint(16, 24)), cold=str(rng.randint(2, 15)), pl=rng.choice(PLACES),
                cool=str(rng.randint(12, 17)), mild=str(rng.randint(18, 25)),
                day=rng.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]),
                wkend=rng.choice(["Saturday", "Sunday"]), mon=rng.choice(["March", "May", "August", "November"]))
    fx, fnx, goal = fx.format(**subs), fnx.format(**subs), goal.format(**subs)
    Cc, X = Cc.format(**subs), X.format(**subs)
    form = rng.choice(["unless", "unless", "fronted", "except_when"])
    if form == "unless":
        rule = f"{Cc} unless {X}."
    elif form == "fronted":
        rule = end(f"Unless {X}, {Cc[0].lower() + Cc[1:]}")
    else:
        rule = f"{Cc}, except when {X}."
    Xa, Ca = "X", "C"
    rows = [(fnx, NOT(Xa), "yes"), (fx, Xa, "no")]
    rng.shuffle(rows)
    q = cert_q(rng, rng.choice(["text", "rule", "notice"]), goal)
    edge = "double_negation" if dneg else "exception"
    return [mk(f"{rule} {fact}", q, "certain", edge, [pf, IMP(NOT(Xa), Ca)], Ca, g, form) for fact, pf, g in rows]


# ================================================================================================ S09 unless (deontic)
UNLESS_V = [
    ("Staff must wear gloves in the lab unless they are only observing.",
     "{x} was only observing the experiment and did not wear gloves.",
     "{x} was handling the samples and did not wear gloves."),
    ("Visitors must sign in at reception unless a staff member accompanies them.",
     "{x} came in with a staff member and did not sign in at reception.",
     "{x} came in alone and did not sign in at reception."),
    ("Employees must submit a receipt for every expense unless the amount is under $25.",
     "{x} claimed ${lo} for a taxi without submitting a receipt.",
     "{x} claimed ${hi} for a taxi without submitting a receipt."),
    ("Students must attend the Friday seminar unless they have a lab session at the same time.",
     "{x} had a lab session at the same time and missed the Friday seminar.",
     "{x} had no lab session at the same time and missed the Friday seminar."),
    ("Guests must check out by 11 a.m. unless they booked a late checkout.",
     "{x} had booked a late checkout and left the room at 1 p.m.",
     "{x} had not booked a late checkout and left the room at 1 p.m."),
    ("Cyclists must dismount on the bridge unless the bike lane is open.",
     "The bike lane was open, and {x} rode across the bridge without dismounting.",
     "The bike lane was closed, and {x} rode across the bridge without dismounting."),
    ("Contractors must wear a hard hat on site unless they are inside the site office.",
     "{x} took off the hard hat while inside the site office.",
     "{x} took off the hard hat while crossing the loading yard."),
    ("Passengers must keep their seatbelts fastened unless the seatbelt sign is off.",
     "The seatbelt sign was off when {x} unfastened the seatbelt.",
     "The seatbelt sign was on when {x} unfastened the seatbelt."),
    ("Members must return gym equipment by 9 p.m. unless the duty manager approves an extension.",
     "{x} returned the rowing machine at 10 p.m. after the duty manager approved an extension.",
     "{x} returned the rowing machine at 10 p.m. without any approved extension."),
    ("Nurses must have a second nurse check the dose unless the medicine is on the low-risk list.",
     "{x} gave a medicine from the low-risk list without a second check.",
     "{x} gave a medicine that is not on the low-risk list without a second check."),
    ("Teachers must email parents about an absence unless the parent has already phoned the school.",
     "A parent had already phoned the school about the absence, and the teacher, {x}, sent no email.",
     "No parent had phoned the school about the absence, and the teacher, {x}, sent no email."),
    ("Tenants must give 30 days' notice before moving out unless the landlord waives the notice in writing.",
     "{x} moved out with 10 days' notice after the landlord waived the notice in writing.",
     "{x} moved out with 10 days' notice, and the landlord did not waive the notice."),
    ("Pharmacy staff must ask for photo ID unless the customer is a registered patient.",
     "{x} served a registered patient without asking for photo ID.",
     "{x} served a customer who is not a registered patient without asking for photo ID."),
    ("Drivers must stop at the barrier unless the green light is on.",
     "The green light was on, and {x} drove through the barrier without stopping.",
     "The green light was off, and {x} drove through the barrier without stopping."),
    ("Hikers must register at the ranger station unless they stay on the marked lakeside path.",
     "{x} stayed on the marked lakeside path and did not register at the ranger station.",
     "{x} hiked to the summit and did not register at the ranger station."),
    ("Drivers must take a 45-minute break after four and a half hours unless the journey ends within the next 15 minutes.",
     "{x} drove for four and a half hours, did not take a break, and finished the journey ten minutes later.",
     "{x} drove for four and a half hours, did not take a break, and finished the journey an hour later."),
]


@schema("unless_violate", 300)
def s_unless_v(rng):
    rule, ex, nex = rng.choice(UNLESS_V)
    x = rng.choice(PEOPLE)[0]
    lo, hi = rng.choice([8, 12, 15, 19, 22, 24]), rng.choice([25, 25, 26, 31, 40, 58])
    ex, nex = ex.format(x=x, lo=lo, hi=hi), nex.format(x=x, lo=lo, hi=hi)
    E, D = "E", "D"
    rows = [(ex, E, "no"), (nex, NOT(E), "yes")]
    rng.shuffle(rows)
    q = rng.choice([f"Did {x} break the rule?", f"Did {x} break the rule as written?",
                    f"Is what {x} did against the rule?"])
    hdr = header(rng, RULE_HDR, 0.3)
    edge = "numeric" if "$" in rule else "exception"
    return [mk(f"{hdr}{rule} {s}", q, "violate", edge, [pf, NOT(D)], AND(NOT(E), NOT(D)), g,
               "exempt" if g == "no" else "not_exempt") for s, pf, g in rows]


# ================================================================================================ S10 chains (multi-hop)
CHAIN = [
    ("If a delivery is more than two days late, the customer receives a voucher.",
     "Every customer who receives a voucher is added to the priority list.",
     "Every customer who is added to the priority list receives a voucher.",
     "The delivery for order #{n} was three days late.", "The delivery for order #{n} was one day late.",
     "the customer for order #{n} is added to the priority list"),
    ("Any employee who completes the leadership course is eligible for promotion.",
     "Every employee eligible for promotion is reviewed in June.",
     "Every employee reviewed in June is eligible for promotion.",
     "{x} completed the leadership course.", "{x} started the leadership course but did not complete it.",
     "{x} is reviewed in June"),
    ("All vehicles older than ten years must have an annual safety test.",
     "Every vehicle that must have an annual safety test is listed in the fleet register.",
     "Every vehicle listed in the fleet register must have an annual safety test.",
     "Van {n} is twelve years old.", "Van {n} is six years old.", "van {n} is listed in the fleet register"),
    ("Every student who scores above 90 gets a merit award.",
     "Every student who gets a merit award is invited to the spring dinner.",
     "Every student who is invited to the spring dinner gets a merit award.",
     "{x} scored 94.", "{x} scored 86.", "{x} is invited to the spring dinner"),
    ("Every order over $100 qualifies for free shipping.",
     "Every order that qualifies for free shipping is packed at the Northfield warehouse.",
     "Every order packed at the Northfield warehouse qualifies for free shipping.",
     "Order #{n} is for $140.", "Order #{n} is for $60.", "order #{n} is packed at the Northfield warehouse"),
    ("All members who attend at least ten classes earn a bronze badge.",
     "All members with a bronze badge get a free towel.",
     "All members who get a free towel have a bronze badge.",
     "{x} attended twelve classes.", "{x} attended seven classes.", "{x} gets a free towel"),
    ("Every flight delayed by more than three hours is eligible for compensation.",
     "Every flight eligible for compensation is reported to the regulator.",
     "Every flight reported to the regulator is eligible for compensation.",
     "Flight {n} was delayed by four hours.", "Flight {n} was delayed by two hours.",
     "Flight {n} is reported to the regulator"),
    ("All applications received before 1 March are reviewed by the panel.",
     "All applications reviewed by the panel receive written feedback.",
     "All applications that receive written feedback are reviewed by the panel.",
     "{x}'s application was received on 20 February.", "{x}'s application was received on 10 March.",
     "{x}'s application receives written feedback"),
    ("Every tenant who reports a leak gets an inspection within 48 hours.",
     "Every tenant who gets an inspection within 48 hours receives a written report.",
     "Every tenant who receives a written report gets an inspection within 48 hours.",
     "{x} reported a leak on Monday.", "{x} reported a broken light on Monday.", "{x} receives a written report"),
    ("Any bag heavier than 23 kg is tagged as heavy.", "Every bag tagged as heavy is loaded last.",
     "Every bag loaded last is tagged as heavy.", "{x}'s bag weighs 27 kg.", "{x}'s bag weighs 19 kg.",
     "{x}'s bag is loaded last"),
    ("Every runner who finishes in under three hours qualifies for the championship race.",
     "Every runner who qualifies for the championship race receives a gold bib.",
     "Every runner who receives a gold bib qualifies for the championship race.",
     "{x} finished in 2 hours 51 minutes.", "{x} finished in 3 hours 4 minutes.", "{x} receives a gold bib"),
    ("Every customer who spends more than $500 in a year becomes a silver member.",
     "Every silver member is sent the spring catalogue.",
     "Everyone who is sent the spring catalogue is a silver member.",
     "{x} spent $620 with the store last year.", "{x} spent $340 with the store last year.",
     "{x} is sent the spring catalogue"),
    ("Every intern who finishes the safety module gets building access.",
     "Every intern with building access is added to the fire-warden rota.",
     "Every intern on the fire-warden rota has building access.",
     "{x}, an intern, finished the safety module.", "{x}, an intern, has not finished the safety module.",
     "{x} is added to the fire-warden rota"),
    ("Any shipment containing lithium batteries is labelled hazardous.",
     "Every shipment labelled hazardous goes by road.",
     "Every shipment that goes by road is labelled hazardous.",
     "Shipment {c} contains lithium batteries.", "Shipment {c} contains cotton towels.", "shipment {c} goes by road"),
    ("If a patient's temperature is above 38°C, the nurse pages the on-call doctor.",
     "Every page to the on-call doctor is logged in the ward diary.",
     "Every entry in the ward diary is a page to the on-call doctor.",
     "At 2 a.m., the patient in bed 4 had a temperature of 38.6°C.",
     "At 2 a.m., the patient in bed 4 had a temperature of 37.4°C.",
     "a page to the on-call doctor about the patient in bed 4 is logged in the ward diary"),
    ("Every package over 2 kg goes through the large-item scanner.",
     "Every package that goes through the large-item scanner is checked by a supervisor.",
     "Every package checked by a supervisor goes through the large-item scanner.",
     "Package {c} weighs 3.4 kg.", "Package {c} weighs 1.2 kg.", "package {c} is checked by a supervisor"),
    ("If a student misses more than three classes in a term, the parents are contacted.",
     "Whenever parents are contacted, the head of year is informed.",
     "Whenever the head of year is informed, the parents have been contacted.",
     "{x} missed five classes this term.", "{x} missed one class this term.", "the head of year is informed about {x}"),
    ("Every invoice above $10,000 needs the finance director's approval.",
     "Every invoice that needs the finance director's approval is paid at the end of the month.",
     "Every invoice paid at the end of the month needs the finance director's approval.",
     "Invoice {n} is for $14,500.", "Invoice {n} is for $6,200.", "invoice {n} is paid at the end of the month"),
    ("Every guest who stays more than five nights gets a free dinner.",
     "Every guest who gets a free dinner is sent a feedback survey.",
     "Every guest who is sent a feedback survey gets a free dinner.",
     "{x} stayed seven nights.", "{x} stayed three nights.", "{x} is sent a feedback survey"),
    ("All staff who handle cash must complete fraud training.",
     "Everyone who must complete fraud training is added to the compliance list.",
     "Everyone on the compliance list must complete fraud training.",
     "{x} handles cash at the front desk.", "{x} works in the back office and does not handle cash.",
     "{x} is added to the compliance list"),
    ("Any tree taller than 10 metres needs a felling permit.",
     "Every tree that needs a felling permit is inspected by the tree officer.",
     "Every tree inspected by the tree officer needs a felling permit.",
     "The oak in {x}'s garden is 14 metres tall.", "The oak in {x}'s garden is 7 metres tall.",
     "the oak in {x}'s garden is inspected by the tree officer"),
    ("Every flight longer than six hours serves a hot meal.",
     "Every flight that serves a hot meal carries two extra cabin crew.",
     "Every flight carrying two extra cabin crew serves a hot meal.",
     "Flight {n} lasts eight hours.", "Flight {n} lasts four hours.", "Flight {n} carries two extra cabin crew"),
    ("Every child under five gets a free health check.",
     "Every child who gets a free health check is given a vitamin pack.",
     "Every child who is given a vitamin pack gets a free health check.",
     "{x}'s daughter is three.", "{x}'s daughter is seven.", "{x}'s daughter is given a vitamin pack"),
    ("Every complaint that mentions safety is escalated to the manager.",
     "Every escalated complaint gets a reply within 24 hours.",
     "Every complaint that gets a reply within 24 hours has been escalated.",
     "{x}'s complaint mentions a safety issue.", "{x}'s complaint is about a late delivery and does not mention safety.",
     "{x}'s complaint gets a reply within 24 hours"),
    ("Any member who refers three friends becomes a gold member.",
     "All gold members get free entry to the summer party.",
     "All members with free entry to the summer party are gold members.",
     "{x} referred four friends.", "{x} referred two friends.", "{x} gets free entry to the summer party"),
    ("Every building over 18 metres tall must have a sprinkler system.",
     "Every building that must have a sprinkler system is inspected every year.",
     "Every building inspected every year must have a sprinkler system.",
     "The {pl} tower is 30 metres tall.", "The {pl} tower is 12 metres tall.",
     "the {pl} tower is inspected every year"),
    ("Every loan application with a missing document is put on hold.",
     "Every application on hold is reviewed by a senior officer.",
     "Every application reviewed by a senior officer is put on hold.",
     "{x}'s loan application is missing a payslip.", "{x}'s loan application has every document.",
     "{x}'s loan application is reviewed by a senior officer"),
]


@schema("chain_multi_hop", 300)
def s_chain(rng):
    r1, r2, r2rev, fact, non, goal = rng.choice(CHAIN)
    subs = dict(x=rng.choice(PEOPLE)[0], n=str(rng.randint(1000, 9999)), c=slot(rng, "code"), pl=rng.choice(PLACES))
    fact, non, goal = fact.format(**subs), non.format(**subs), goal.format(**subs)
    A, B, C = "A", "B", "C"
    if rng.random() < 0.5:
        rows = [(f"{r1} {r2} {fact}", [A, IMP(A, B), IMP(B, C)], "yes", "chain"),
                (f"{r1} {r2rev} {fact}", [A, IMP(A, B), IMP(C, B)], "no", "reversed")]
    else:
        rows = [(f"{r1} {r2} {fact}", [A, IMP(A, B), IMP(B, C)], "yes", "chain"),
                (f"{r1} {r2} {non}", [NOT(A), IMP(A, B), IMP(B, C)], "no", "antecedent_false")]
    rng.shuffle(rows)
    q = cert_q(rng, rng.choice(["text", "rules", "policy"]), goal)
    return [mk(s, q, "certain", "multi_hop", p, C, g, v) for s, p, g, v in rows]


# ================================================================================================ S11 disjunctive syllogism
DISJ = [
    ("The parcel is either at the {pl} depot or on the courier's van.", "It is not at the {pl} depot.",
     "It is at the {pl} depot.", "the parcel is on the courier's van"),
    ("{x} will cover either the Monday shift or the Wednesday shift.", "{x} will not cover the Monday shift.",
     "{x} will cover the Monday shift.", "{x} will cover the Wednesday shift"),
    ("The missing invoice is either in the March folder or in the April folder.",
     "It is not in the March folder.", "It is in the March folder.", "the missing invoice is in the April folder"),
    ("The leak is coming from either the roof or the upstairs bathroom.",
     "The roofer has confirmed that the roof is not leaking.", "The roofer has confirmed that the roof is leaking.",
     "the leak is coming from the upstairs bathroom"),
    ("The error was caused either by the new update or by a faulty cable.",
     "It was not caused by the new update.", "It was caused by the new update.",
     "the error was caused by a faulty cable"),
    ("The team bus will leave from either the stadium or the train station.",
     "It will not leave from the stadium.", "It will leave from the stadium.",
     "the team bus will leave from the train station"),
    ("{x}'s passport is either in the safe or in the desk drawer.", "It is not in the safe.", "It is in the safe.",
     "{x}'s passport is in the desk drawer"),
    ("The meeting will be held either on Tuesday or on Thursday.", "It will not be held on Tuesday.",
     "It will be held on Tuesday.", "the meeting will be held on Thursday"),
    ("The spare keys are either with the caretaker or in the key box.", "They are not with the caretaker.",
     "They are with the caretaker.", "the spare keys are in the key box"),
    ("The payment was made either by card or by bank transfer.", "It was not made by card.", "It was made by card.",
     "the payment was made by bank transfer"),
    ("The fault is in either the pump or the valve.", "The engineer found no fault in the pump.",
     "The engineer found a fault in the pump.", "the fault is in the valve"),
    ("The school trip will go either to the science museum or to the botanical garden.",
     "It will not go to the science museum.", "It will go to the science museum.",
     "the school trip will go to the botanical garden"),
    ("The new printer will be installed either on the second floor or in the mailroom.",
     "It will not be installed on the second floor.", "It will be installed on the second floor.",
     "the new printer will be installed in the mailroom"),
    ("{x} is flying to the conference either on Sunday evening or on Monday morning.",
     "{x} is not flying on Sunday evening.", "{x} is flying on Sunday evening.",
     "{x} is flying to the conference on Monday morning"),
    ("The contract will go to either {c1} or {c2}.", "It will not go to {c1}.", "It will go to {c1}.",
     "the contract will go to {c2}"),
    ("The refund will go either to {x}'s card or to store credit.", "It will not go to {x}'s card.",
     "It will go to {x}'s card.", "the refund will go to store credit"),
    ("The noise is coming either from the boiler or from the washing machine.", "It is not coming from the boiler.",
     "It is coming from the boiler.", "the noise is coming from the washing machine"),
    ("{x}'s lost phone is either in the car or at the gym.", "It is not in the car.", "It is in the car.",
     "{x}'s lost phone is at the gym"),
    ("{x} will study either law or medicine.", "{x} will not study law.", "{x} will study law.",
     "{x} will study medicine"),
    ("The {pl} concert will be held either in the park or in the town hall.", "It will not be held in the park.",
     "It will be held in the park.", "the {pl} concert will be held in the town hall"),
    ("The mistake is either in the March figures or in the April figures.",
     "The March figures have been checked and contain no mistake.", "The March figures contain the mistake.",
     "the mistake is in the April figures"),
    ("The virus got in either through the email attachment or through the USB stick.",
     "It did not get in through the email attachment.", "It got in through the email attachment.",
     "the virus got in through the USB stick"),
    ("The new manager will be either {x} or {y}.", "{x} will not be the new manager.",
     "{x} will be the new manager.", "{y} will be the new manager"),
    ("The package was left either with the neighbour or in the porch.", "It was not left with the neighbour.",
     "It was left with the neighbour.", "the package was left in the porch"),
    ("The leak is either under the sink or behind the dishwasher.", "The plumber found no leak under the sink.",
     "The plumber found a leak under the sink.", "the leak is behind the dishwasher"),
    ("The {pl} branch will close either in March or in April.", "It will not close in March.",
     "It will close in March.", "the {pl} branch will close in April"),
]


@schema("disjunctive", 300)
def s_disj(rng):
    d, fn, fp, goal = rng.choice(DISJ)
    c1, c2 = rng.sample(COMPANIES, 2)
    x, y = [p[0] for p in rng.sample(PEOPLE, 2)]
    subs = dict(x=x, y=y, pl=rng.choice(PLACES), c1=c1, c2=c2)
    d, fn, fp, goal = (s.format(**subs) for s in (d, fn, fp, goal))
    if rng.random() < 0.3:  # plain 'A or B' without 'either'
        d = d.replace("either ", "", 1)
    A, B = "A", "B"
    rows = [(fn, NOT(A), "yes"), (fp, A, "no")]
    rng.shuffle(rows)
    q = cert_q(rng, "text", goal)
    return [mk(f"{d} {s}", q, "certain", "negation", [OR(A, B), pf], B, g, "neg_fact" if g == "yes" else "pos_fact")
            for s, pf, g in rows]


# ================================================================================================ S12 De Morgan scope (deontic)
DEMORGAN = [
    # rule template, scenario: exactly one used, both used, neither used
    ("On sale items, customers may not use {Q} the spring coupon {C} the loyalty coupon.",
     "{x} used the spring coupon, and no other coupon, on a sale item.",
     "{x} used the spring coupon and the loyalty coupon together on a sale item.",
     "{x} bought a sale item without using any coupon."),
    ("During the exam, students may not use {Q} a calculator {C} a formula sheet.",
     "During the exam, {x} used a calculator but no formula sheet.",
     "During the exam, {x} used both a calculator and a formula sheet.",
     "During the exam, {x} used neither a calculator nor a formula sheet."),
    ("Visitors may not bring {Q} food {C} drinks into the reading room.",
     "{x} brought a bottle of water, but no food, into the reading room.",
     "{x} brought a sandwich and a bottle of water into the reading room.",
     "{x} brought no food and no drinks into the reading room."),
    ("Guests may not claim {Q} the breakfast credit {C} the late-checkout credit on the same stay.",
     "On one stay, {x} claimed the breakfast credit but not the late-checkout credit.",
     "On one stay, {x} claimed both the breakfast credit and the late-checkout credit.",
     "On one stay, {x} claimed neither the breakfast credit nor the late-checkout credit."),
    ("Employees may not take {Q} Christmas Eve {C} New Year's Eve off.",
     "{x} took Christmas Eve off and worked on New Year's Eve.",
     "{x} took both Christmas Eve and New Year's Eve off.",
     "{x} worked on both Christmas Eve and New Year's Eve."),
    ("Tenants may not keep {Q} a dog {C} a cat in the flat.", "{x} keeps a cat, but no dog, in the flat.",
     "{x} keeps a dog and a cat in the flat.", "{x} keeps no pets in the flat."),
    ("Passengers may not bring {Q} a suitcase {C} a large backpack onto the shuttle bus.",
     "{x} brought a suitcase, but no backpack, onto the shuttle bus.",
     "{x} brought a suitcase and a large backpack onto the shuttle bus.",
     "{x} brought only a small handbag onto the shuttle bus."),
    ("Applicants may not apply for {Q} the travel grant {C} the equipment grant this year.",
     "This year {x} applied for the travel grant and not for the equipment grant.",
     "This year {x} applied for both the travel grant and the equipment grant.",
     "This year {x} applied for neither the travel grant nor the equipment grant."),
    ("Members may not book {Q} the indoor court {C} the outdoor court on Friday evenings.",
     "{x} booked the indoor court, and not the outdoor court, for a Friday evening.",
     "{x} booked both the indoor court and the outdoor court for a Friday evening.",
     "{x} booked neither court for a Friday evening and played on a Tuesday instead."),
    ("Students may not enrol in {Q} Spanish I {C} French I this term.",
     "{x} enrolled in Spanish I, and not in French I, this term.",
     "{x} enrolled in both Spanish I and French I this term.",
     "{x} enrolled in German I this term and in neither Spanish I nor French I."),
    ("Beach visitors may not bring {Q} glass bottles {C} barbecues onto the sand.",
     "{x} brought glass bottles, but no barbecue, onto the sand.",
     "{x} brought glass bottles and a barbecue onto the sand.",
     "{x} brought only plastic bottles onto the sand, and no barbecue."),
    ("Drivers may not use {Q} the bus lane {C} the hard shoulder during rush hour.",
     "During rush hour, {x} used the bus lane but not the hard shoulder.",
     "During rush hour, {x} used both the bus lane and the hard shoulder.",
     "During rush hour, {x} stayed in the normal lanes and used neither the bus lane nor the hard shoulder."),
    ("Staff may not wear {Q} jeans {C} trainers when meeting clients.",
     "{x} wore jeans with leather shoes to a client meeting.",
     "{x} wore jeans and trainers to a client meeting.",
     "{x} wore trousers and leather shoes to a client meeting."),
    ("After 3 p.m., diners may not order {Q} the lunch special {C} the kids' menu.",
     "At 4 p.m., {x} ordered the lunch special and nothing from the kids' menu.",
     "At 4 p.m., {x} ordered the lunch special and a dish from the kids' menu.",
     "At 4 p.m., {x} ordered from the main menu only."),
    ("Players may not wear {Q} a watch {C} earrings during a match.",
     "{x} wore a watch, but no earrings, during a match.", "{x} wore a watch and earrings during a match.",
     "{x} wore neither a watch nor earrings during a match."),
]


@schema("demorgan_scope", 320)
def s_demorgan(rng):
    tmpl, one, both_s, none_s = rng.choice(DEMORGAN)
    x = rng.choice(PEOPLE)[0]
    both = tmpl.format(Q="both", C="and")
    either = tmpl.format(Q="either", C="or")
    X, Y = "X", "Y"
    var = rng.choice(["rule_swap", "rule_swap", "both_fact", "either_fact"])
    if var == "rule_swap":   # same scenario (exactly one item used), 'both' vs 'either' rule
        rows = [(both, one, [X, NOT(Y)], AND(X, Y), "no"), (either, one, [X, NOT(Y)], OR(X, Y), "yes")]
    elif var == "both_fact":  # 'may not use both': both used vs one used
        rows = [(both, both_s, [X, Y], AND(X, Y), "yes"), (both, one, [X, NOT(Y)], AND(X, Y), "no")]
    else:                     # 'may not use either': one used vs none used
        rows = [(either, one, [X, NOT(Y)], OR(X, Y), "yes"), (either, none_s, [NOT(X), NOT(Y)], OR(X, Y), "no")]
    rng.shuffle(rows)
    q = rng.choice([f"Did {x} break the rule?", f"Did {x} break the rule as written?",
                    f"Does what {x} did go against the rule?"])
    hdr = header(rng, RULE_HDR, 0.3)
    return [mk(f"{hdr}{r} {sc.format(x=x)}", q, "violate", "negation", pr, v, g, var) for r, sc, pr, v, g in rows]


# ================================================================================================ S13 deontic negation
DEONTIC = [
    # Group (plural), member ('a student'), verb phrase with 'their', did (with {p}), did not, plausible modalities
    ("Employees", "an employee", "wear a tie on Fridays", "wore a tie on Friday", "did not wear a tie on Friday", "OF"),
    ("Students", "a student", "print their essays for the online module", "printed {p} essay for the online module",
     "did not print {p} essay for the online module", "OF"),
    ("Visitors", "a visitor", "sign the guest book", "signed the guest book", "did not sign the guest book", "O"),
    ("Passengers", "a passenger", "show their ticket to the driver on the night bus",
     "showed {p} ticket to the driver on the night bus", "did not show {p} ticket to the driver on the night bus", "O"),
    ("Staff", "a staff member", "use the side entrance after 6 p.m.", "used the side entrance after 6 p.m.",
     "did not use the side entrance after 6 p.m.", "OF"),
    ("Workshop participants", "a workshop participant", "bring their own laptop", "brought {p} own laptop",
     "did not bring {p} own laptop", "OF"),
    ("Team members", "a team member", "eat at their desks during the audit", "ate at {p} desk during the audit",
     "did not eat at {p} desk during the audit", "F"),
    ("Gallery visitors", "a gallery visitor", "take photos in the main hall", "took photos in the main hall",
     "did not take photos in the main hall", "F"),
    ("Pupils on the trip", "a pupil on the trip", "bring a packed lunch", "brought a packed lunch",
     "did not bring a packed lunch", "OF"),
    ("Candidates", "a candidate", "use a pen for the written test", "used a pen for the written test",
     "did not use a pen for the written test", "OF"),
    ("Analysts", "an analyst", "work from home on Mondays", "worked from home on Monday",
     "did not work from home on Monday", "OF"),
    ("Employees", "an employee", "speak to the press about the merger", "spoke to the press about the merger",
     "did not speak to the press about the merger", "F"),
    ("Theatre-goers", "a theatre-goer", "leave their coats in the cloakroom", "left {p} coat in the cloakroom",
     "did not leave {p} coat in the cloakroom", "O"),
    ("Dog owners", "a dog owner", "keep their dogs on a lead in the park", "kept {p} dog on a lead in the park",
     "did not keep {p} dog on a lead in the park", "O"),
    ("Delegates", "a delegate", "wear their name badge in the exhibition hall",
     "wore {p} name badge in the exhibition hall", "did not wear {p} name badge in the exhibition hall", "O"),
    ("Drivers", "a driver", "switch off their engines while waiting at the school gate",
     "switched off {p} engine while waiting at the school gate",
     "did not switch off {p} engine while waiting at the school gate", "O"),
    ("Swimmers", "a swimmer", "wear a swimming cap in the main pool", "wore a swimming cap in the main pool",
     "did not wear a swimming cap in the main pool", "O"),
    ("Contractors", "a contractor", "park in the visitor spaces", "parked in the visitor spaces",
     "did not park in the visitor spaces", "F"),
    ("Jurors", "a juror", "discuss the case with their family", "discussed the case with {p} family",
     "did not discuss the case with {p} family", "F"),
    ("Tenants", "a tenant", "put their bins out on Sunday night", "put {p} bins out on Sunday night",
     "did not put {p} bins out on Sunday night", "OF"),
    ("Cyclists", "a cyclist", "ride on the pavement along the promenade", "rode on the pavement along the promenade",
     "did not ride on the pavement along the promenade", "F"),
    ("Volunteers", "a volunteer", "wear the orange vest during the clean-up", "wore the orange vest during the clean-up",
     "did not wear the orange vest during the clean-up", "O"),
    ("Hotel guests", "a hotel guest", "smoke on the balconies", "smoked on the balcony", "did not smoke on the balcony",
     "F"),
    ("Lab users", "a lab user", "log the time they leave the clean room", "logged the time {s} left the clean room",
     "did not log the time {s} left the clean room", "O"),
]
OPT_FORB = [("do not have to", "must not"), ("are not required to", "are required not to"),
            ("need not", "must not"), ("do not need to", "are not allowed to")]
OPT_OBL = [("do not have to", "have to"), ("are not required to", "are required to"), ("need not", "must"),
           ("do not need to", "need to")]
PERM_FORB = [("may", "may not"), ("are allowed to", "are not allowed to"), ("are permitted to", "are not permitted to")]


@schema("deontic_negation", 400)
def s_deontic(rng):
    G, mem, vp, did, didnt, ok = rng.choice(DEONTIC)
    pp = rng.choice(PEOPLE)
    x = pp[0]
    did, didnt = did.format(p=pp[3], s=pp[1]), didnt.format(p=pp[3], s=pp[1])
    D = "D"
    t = rng.choice([t for t, need in (("opt_forb", "OF"), ("opt_obl", "O"), ("perm_forb", "F"), ("obl_fact", "O"),
                                      ("forb_fact", "F")) if all(c in ok for c in need)])
    if t == "opt_forb":
        o, f = rng.choice(OPT_FORB)
        rows = [(f"{G} {o} {vp}.", did, D, False, "no"), (f"{G} {f} {vp}.", did, D, D, "yes")]
    elif t == "opt_obl":
        o, b = rng.choice(OPT_OBL)
        rows = [(f"{G} {o} {vp}.", didnt, NOT(D), False, "no"), (f"{G} {b} {vp}.", didnt, NOT(D), NOT(D), "yes")]
    elif t == "perm_forb":
        p_, f = rng.choice(PERM_FORB)
        rows = [(f"{G} {p_} {vp}.", did, D, False, "no"), (f"{G} {f} {vp}.", did, D, D, "yes")]
    elif t == "obl_fact":
        b = rng.choice(["must", "are required to", "have to"])
        rule = f"{G} {b} {vp}."
        rows = [(rule, did, D, NOT(D), "no"), (rule, didnt, NOT(D), NOT(D), "yes")]
    else:
        f = rng.choice(["must not", "are not allowed to", "may not", "are required not to"])
        rule = f"{G} {f} {vp}."
        rows = [(rule, did, D, D, "yes"), (rule, didnt, NOT(D), D, "no")]
    rng.shuffle(rows)
    q = rng.choice([f"Did {x} break the rule?", f"Did {x} break this rule?", f"Did {x} act against the rule?"])
    hdr = header(rng, RULE_HDR, 0.3)
    return [mk(f"{hdr}{end(r[:-1])} {x}, {mem}, {end(s)}", q, "violate", "negation", [pf], v, g, t)
            for r, s, pf, v, g in rows]


# ================================================================================================ S14 contraries vs contradictories
CONTRA = [
    ("Every insurance claim is approved, rejected or put on hold.",
     "Every insurance claim is either approved or rejected; there is no other outcome.",
     "Claim {n} was not rejected.", "Claim {n} was neither rejected nor put on hold.", "claim {n} was approved"),
    ("Each job application ends up accepted, declined or waitlisted.",
     "Each job application ends up either accepted or declined; there is no waitlist.",
     "{x}'s application was not declined.", "{x}'s application was neither declined nor waitlisted.",
     "{x}'s application was accepted"),
    ("Matches in this tournament end in a win, a loss or a draw.",
     "Matches in this tournament end in a win or a loss; there are no draws.",
     "{t} did not lose on Saturday.", "{t} neither lost nor drew on Saturday.", "{t} won on Saturday"),
    ("Each driving test result is recorded as pass, fail or void.",
     "Each driving test result is recorded as either pass or fail; no other result exists.",
     "{x}'s result was not recorded as fail.", "{x}'s result was recorded as neither fail nor void.",
     "{x}'s result was recorded as pass"),
    ("The bank grants, denies or defers every loan request.",
     "The bank either grants or denies every loan request; it never defers one.",
     "{x}'s loan request was not denied.", "{x}'s loan request was neither denied nor deferred.",
     "{x}'s loan request was granted"),
    ("Every permit application is approved, refused or returned for changes.",
     "Every permit application is either approved or refused; none is returned for changes.",
     "The permit application for {n} Mill Lane was not refused.",
     "The permit application for {n} Mill Lane was neither refused nor returned for changes.",
     "the permit application for {n} Mill Lane was approved"),
    ("Every cheque either clears, bounces or is held for review.",
     "Every cheque either clears or bounces; none is held for review.",
     "Cheque {n} did not bounce.", "Cheque {n} neither bounced nor was held for review.", "cheque {n} cleared"),
    ("Each module is graded pass, fail or incomplete.", "Each module is graded either pass or fail; nothing else.",
     "{x}'s statistics module was not graded fail.", "{x}'s statistics module was graded neither fail nor incomplete.",
     "{x}'s statistics module was graded pass"),
    ("Every return request is accepted, refused or still under review.",
     "Every return request has been either accepted or refused; none is still under review.",
     "{x}'s return request was not refused.", "{x}'s return request was neither refused nor left under review.",
     "{x}'s return request was accepted"),
    ("Each board member voted for the proposal, voted against it or abstained.",
     "Each board member voted either for or against the proposal; nobody abstained.",
     "{x} did not vote against the proposal.", "{x} neither voted against the proposal nor abstained.",
     "{x} voted for the proposal"),
    ("Every visa application is granted, refused or withdrawn.",
     "Every visa application was either granted or refused; none was withdrawn.",
     "{x}'s visa application was not refused.", "{x}'s visa application was neither refused nor withdrawn.",
     "{x}'s visa application was granted"),
    ("Every flight today departed on time, departed late or was cancelled.",
     "Every flight today departed, either on time or late; none was cancelled.",
     "Flight {n} did not depart late.", "Flight {n} neither departed late nor was cancelled.",
     "Flight {n} departed on time"),
    ("Each reimbursement request is paid, rejected or sent back for missing receipts.",
     "Each reimbursement request is either paid or rejected; none is sent back.",
     "{x}'s reimbursement request was not rejected.",
     "{x}'s reimbursement request was neither rejected nor sent back for missing receipts.",
     "{x}'s reimbursement request was paid"),
    ("Every parcel is delivered, returned to the sender or held at the depot.",
     "Every parcel is either delivered or returned to the sender; none is held at the depot.",
     "Parcel {c} was not returned to the sender.", "Parcel {c} was neither returned to the sender nor held at the depot.",
     "parcel {c} was delivered"),
    ("Each planning appeal is upheld, dismissed or withdrawn.",
     "Each planning appeal is either upheld or dismissed; none is withdrawn.",
     "The appeal for {n} {st} was not dismissed.", "The appeal for {n} {st} was neither dismissed nor withdrawn.",
     "the appeal for {n} {st} was upheld"),
    ("Every job candidate is hired, rejected or kept on file.",
     "Every job candidate is either hired or rejected; nobody is kept on file.",
     "{x} was not rejected.", "{x} was neither rejected nor kept on file.", "{x} was hired"),
    ("Every game in the tournament ends in a win, a loss or a draw for each player.",
     "Every game in the tournament ends in a win or a loss for each player; drawn games are replayed until someone wins.",
     "{x} did not lose the final game.", "{x} neither lost nor drew the final game.", "{x} won the final game"),
    ("Each patient referral is accepted, declined or put on a waiting list.",
     "Each patient referral is either accepted or declined; there is no waiting list.",
     "{x}'s referral was not declined.", "{x}'s referral was neither declined nor put on a waiting list.",
     "{x}'s referral was accepted"),
    ("Every refund request ends up approved, denied or escalated.",
     "Every refund request ends up either approved or denied; none is escalated.",
     "{x}'s refund request was not denied.", "{x}'s refund request was neither denied nor escalated.",
     "{x}'s refund request was approved"),
    ("Each train on the line arrived early, on time or late.",
     "Each train on the line arrived either on time or late; none arrived early.",
     "The {tm} train did not arrive late.", "The {tm} train arrived neither late nor early.",
     "the {tm} train arrived on time"),
    ("Every tender is accepted, rejected or sent back for revision.",
     "Every tender is either accepted or rejected; none is sent back for revision.",
     "The tender from {co} was not rejected.", "The tender from {co} was neither rejected nor sent back for revision.",
     "the tender from {co} was accepted"),
    ("Every penalty in the shoot-out was scored, saved or put wide.",
     "Every penalty in the shoot-out was either scored or saved; none went wide.",
     "{x}'s penalty was not saved.", "{x}'s penalty was neither saved nor put wide.", "{x}'s penalty was scored"),
    ("Each building inspection ends in a pass, a fail or a conditional pass.",
     "Each building inspection ends in either a pass or a fail; there are no conditional passes.",
     "The inspection of {n} {st} did not end in a fail.",
     "The inspection of {n} {st} ended in neither a fail nor a conditional pass.",
     "the inspection of {n} {st} ended in a pass"),
    ("Every library request is fulfilled, cancelled or still waiting.",
     "Every library request has been either fulfilled or cancelled; none is still waiting.",
     "{x}'s library request was not cancelled.", "{x}'s library request was neither cancelled nor left waiting.",
     "{x}'s library request was fulfilled"),
]


@schema("contrary_contradictory", 300)
def s_contra(rng):
    three, two, neg1, neg2, goal = rng.choice(CONTRA)
    subs = dict(x=rng.choice(PEOPLE)[0], n=str(rng.randint(12, 980)), t=rng.choice(TEAMS), c=slot(rng, "code"),
                st=rng.choice(STREETS), co=rng.choice(COMPANIES),
                tm=rng.choice(["7:12", "8:05", "9:40", "12:15", "17:48", "18:20"]))
    neg1, neg2, goal = cap(neg1.format(**subs)), cap(neg2.format(**subs)), goal.format(**subs)
    o1, o2, o3 = "o1", "o2", "o3"
    var = rng.choice(["outcomes", "neither"])
    if var == "outcomes":
        rows = [(f"{three} {neg1}", [CNT("==", 1, [o1, o2, o3]), NOT(o2)], "no"),
                (f"{two} {neg1}", [CNT("==", 1, [o1, o2]), NOT(o2)], "yes")]
    else:
        rows = [(f"{three} {neg1}", [CNT("==", 1, [o1, o2, o3]), NOT(o2)], "no"),
                (f"{three} {neg2}", [CNT("==", 1, [o1, o2, o3]), NOT(o2), NOT(o3)], "yes")]
    rng.shuffle(rows)
    q = cert_q(rng, "text", goal)
    return [mk(s, q, "certain", "negation", p, o1, g, var) for s, p, g in rows]


# ================================================================================================ S18/S19 comparatives
COMPAR = [
    # entity kind, more, less, not-less, not-more, at-least-as, context suffix
    ("branch", "sold more units than", "sold fewer units than", "did not sell fewer units than",
     "did not sell more units than", "sold at least as many units as", " in May"),
    ("person", "scored higher than", "scored lower than", "did not score lower than", "did not score higher than",
     "scored at least as high as", " on the maths test"),
    ("town", "got more rain than", "got less rain than", "did not get less rain than", "did not get more rain than",
     "got at least as much rain as", " in April"),
    ("product", "costs more than", "costs less than", "does not cost less than", "does not cost more than",
     "costs at least as much as", ""),
    ("proposal", "received more votes than", "received fewer votes than", "did not receive fewer votes than",
     "did not receive more votes than", "received at least as many votes as", ""),
    ("parcel", "weighs more than", "weighs less than", "does not weigh less than", "does not weigh more than",
     "weighs at least as much as", ""),
    ("person", "is older than", "is younger than", "is not younger than", "is not older than", "is at least as old as",
     ""),
    ("person", "worked more hours than", "worked fewer hours than", "did not work fewer hours than",
     "did not work more hours than", "worked at least as many hours as", " last week"),
    ("route", "is longer than", "is shorter than", "is not shorter than", "is not longer than", "is at least as long as",
     ""),
    ("team", "scored more goals than", "scored fewer goals than", "did not score fewer goals than",
     "did not score more goals than", "scored at least as many goals as", " this season"),
    ("hotel", "charges more per night than", "charges less per night than", "does not charge less per night than",
     "does not charge more per night than", "charges at least as much per night as", ""),
    ("school", "raised more money than", "raised less money than", "did not raise less money than",
     "did not raise more money than", "raised at least as much money as", " at the fair"),
]
PRODUCTS = ["the blue kettle", "the steel kettle", "the basic plan", "the family plan", "the red bike", "the grey bike",
            "the oak desk", "the pine desk", "the large tent", "the compact tent", "the budget laptop", "the tablet"]
ROUTES = ["the coastal route", "the forest route", "the river path", "the ridge trail", "the canal towpath",
          "the valley road"]
PROPOSALS = ["the park proposal", "the library proposal", "the bike-lane proposal", "the market proposal",
             "the playground proposal", "the parking proposal"]
SCHOOLS = ["Hillcrest Primary", "Riverside Academy", "St Anne's", "Oakfield School", "Meadow Lane School",
           "Northgate High"]


def comp_ents(rng, kind, k):
    if kind == "branch":
        return [f"the {p} branch" for p in rng.sample(PLACES, k)]
    if kind == "person":
        return [p[0] for p in rng.sample(PEOPLE, k)]
    if kind == "town":
        return rng.sample(PLACES, k)
    if kind == "product":
        return rng.sample(PRODUCTS, k)
    if kind == "proposal":
        return rng.sample(PROPOSALS, k)
    if kind == "parcel":
        return [f"parcel {c}" for c in (slot(rng, "code") for _ in range(k))]
    if kind == "route":
        return rng.sample(ROUTES, k)
    if kind == "team":
        return rng.sample(TEAMS, k)
    if kind == "hotel":
        return rng.sample(HOTELS, k)
    if kind == "school":
        return rng.sample(SCHOOLS, k)
    raise ValueError(kind)


@schema("not_fewer_scale", 340)
def s_notfewer(rng):
    kind, more, less, notless, notmore, geq, ctx = rng.choice(COMPAR)
    A, B = comp_ents(rng, kind, 2)
    if len({A, B}) < 2:
        return None
    a, b = "a", "b"
    ints = {"a": [0, 3], "b": [0, 3]}
    var = rng.choice(["geq", "gt", "rev"])
    if var == "geq":
        qs = f"{A} {geq} {B}{ctx}"
        rows = [(f"{A} {notless} {B}{ctx}.", CMP(a, ">=", b), "yes"), (f"{A} {notmore} {B}{ctx}.", CMP(a, "<=", b), "no")]
        goal = CMP(a, ">=", b)
    elif var == "gt":
        qs = f"{A} {more} {B}{ctx}"
        rows = [(f"{A} {notless} {B}{ctx}.", CMP(a, ">=", b), "no"), (f"{A} {more} {B}{ctx}.", CMP(a, ">", b), "yes")]
        goal = CMP(a, ">", b)
    else:
        qs = f"{B} {more} {A}{ctx}"
        rows = [(f"{A} {notless} {B}{ctx}.", CMP(a, ">=", b), "no"), (f"{A} {less} {B}{ctx}.", CMP(a, "<", b), "yes")]
        goal = CMP(b, ">", a)
    rng.shuffle(rows)
    q = cert_q(rng, "text", qs)
    return [mk(cap(s), q, "certain", "negation", [p], goal, g, var, ints=ints) for s, p, g in rows]


@schema("transitive_compare", 330)
def s_transitive(rng):
    kind, more, less, notless, notmore, geq, ctx = rng.choice(COMPAR)
    A, B, C = comp_ents(rng, kind, 3)
    if len({A, B, C}) < 3:
        return None
    a, b, c = "a", "b", "c"
    ints = {"a": [0, 3], "b": [0, 3], "c": [0, 3]}
    first = f"{cap(A)} {more} {B}{ctx}"
    var = rng.choice(["flip", "notless", "less"])
    if var == "flip":
        rows = [(f"{first}, and {B} {more} {C}.", CMP(b, ">", c), "yes"),
                (f"{first}, and {C} {more} {B}.", CMP(c, ">", b), "no")]
    elif var == "notless":
        rows = [(f"{first}, and {B} {notless} {C}.", CMP(b, ">=", c), "yes"),
                (f"{first}, and {B} {notmore} {C}.", CMP(b, "<=", c), "no")]
    else:
        rows = [(f"{first}, and {C} {less} {B}.", CMP(c, "<", b), "yes"),
                (f"{first}, and {C} {more} {B}.", CMP(c, ">", b), "no")]
    rng.shuffle(rows)
    q = cert_q(rng, "text", f"{A} {more} {C}{ctx}")
    return [mk(s, q, "certain", "multi_hop", [CMP(a, ">", b), p], CMP(a, ">", c), g, var, ints=ints)
            for s, p, g in rows]


# ================================================================================================ S20 superlatives
SUPER = [
    # intro template with {lst}, superlative sentence with {w}, question with {y} {z}; higher-is-winner?
    ("{n} companies bid for the roofing contract: {lst}.", "The lowest bid came from {w}.",
     "Was the bid from {y} lower than the bid from {z}?", "low", "company"),
    ("{lst} ran the city 10K.", "{w} had the fastest time.", "Did {y} run the 10K faster than {z}?", "high", "person"),
    ("{lst} stood for club treasurer.", "{w} received the most votes.", "Did {y} receive more votes than {z}?", "high",
     "person"),
    ("The chain has {n} branches in the region: {lst}.", "{w} had the highest sales in May.",
     "Did {y} have higher sales than {z} in May?", "high", "place"),
    ("{lst} play up front for the club.", "{w} scored the most goals this season.",
     "Did {y} score more goals than {z} this season?", "high", "person"),
    ("The hotels near the station are {lst}.", "{w} is the cheapest.", "Is {y} cheaper than {z}?", "low", "hotel"),
    ("{lst} entered the baking contest.", "{w} got the highest score from the judges.",
     "Did {y} get a higher score from the judges than {z}?", "high", "person"),
    ("The team compared {n} suppliers: {lst}.", "{w} had the shortest delivery time.",
     "Does {y} have a shorter delivery time than {z}?", "low", "company"),
    ("{lst} sold raffle tickets for the fundraiser.", "{w} sold the most tickets.",
     "Did {y} sell more tickets than {z}?", "high", "person"),
    ("The district's schools are {lst}.", "{w} had the highest attendance last term.",
     "Did {y} have higher attendance than {z} last term?", "high", "school"),
]


@schema("superlative", 250)
def s_super(rng):
    intro, sup, qt, direction, kind = rng.choice(SUPER)
    n = rng.randint(3, 4)
    if kind == "person":
        ents = [p[0] for p in rng.sample(PEOPLE, n)]
    elif kind == "company":
        ents = rng.sample(COMPANIES, n)
    elif kind == "place":
        ents = rng.sample(PLACES, n)
    elif kind == "hotel":
        ents = rng.sample(HOTELS, n)
    else:
        ents = rng.sample(SCHOOLS, n)
    y, z = rng.sample(ents, 2)
    iy, iz = ents.index(y), ents.index(z)
    ints = {f"e{i}": [0, n - 1] for i in range(n)}
    better = ">" if direction == "high" else "<"
    lst = join(ents)
    q = qt.format(y=y, z=z)
    goal = CMP(f"e{iy}", better, f"e{iz}")
    out = []
    for w, gold in ((z, "no"), (y, "yes")):
        iw = ents.index(w)
        prem = [CMP(f"e{iw}", better, f"e{j}") for j in range(n) if j != iw]
        st = cap(intro.format(n=nw(n), lst=lst)) + " " + cap(sup.format(w=w))
        if q[:1].islower():
            q = cap(q)
        out.append(mk(st, q, "true", "quantifier", prem, goal, gold, f"{direction}", ints=ints))
    rng.shuffle(out)
    return out
