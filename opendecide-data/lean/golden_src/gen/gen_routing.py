"""gen_routing: ticket / request routing under an explicit routing policy (multiple choice, labels by construction,
fact-flip twins).

Each row is a realistic request (email, web form, chat, call notes, voicemail, SMS, portal ticket, ...) sent to an
organisation with a routing policy of 8-30 queues.  The options are the queues; each option's definition (the card,
data/v14_parts/defs/gen_routing__<domain>_v<j>.json) states the queue's scope, its exceptions and its priority number.
The instruction states the priority rule (lowest number wins, or highest escalation weight wins) and that only issues
the sender still needs handled count.  15 domains (online retail care, corporate IT desk, retail bank, health-plan
member services, city 311, university student services, residential property management, airline customer relations,
B2B software support, broadband/telecom, HR shared services, law-firm client intake, clinic patient portal,
freight & parcel logistics, video-game player support); 4 policy variants per domain (different thresholds, priority
orders and priority notations, same queue names) -> 60 distinct label sets, plus per-row queue subsets.

Labels are exact by construction:
  * a queue covers an issue iff one of its declarative 'when' alternatives matches and no 'unless' alternative does;
    an unstated fact never satisfies a condition (the definitions say 'stated' wherever a fact can be missing);
  * gold = among the shown queues covering any OPEN issue, the one with the best priority; else the catch-all;
  * decoys: resolved issues and explicitly declined requests (which would outrank the gold if they were open),
    keyword look-alikes, sender-chosen topics / priorities that name a wrong queue, small talk;
  * multi-issue requests are resolved by the stated priority rule; near misses (thresholds at the boundary, exceptions,
    unit conversions, dates relative to the message date, times of day) fall to another queue or to the catch-all.
Self-check: every row is recomputed by an independent evaluator that compiles the rules to Python and reads the
priority numbers back from the rendered definition text; every decisive fact sentence must appear in the text; the
gold queue's name never appears in the text; every twin changes exactly one fact and has a different gold.
Deterministic (seed 20261212), CPU only.
"""
import collections
import copy
import datetime as dt
import hashlib
import json
import os
import random
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "moral_social_norms"))
from common import EDGE_TAGS, NearDup, check_rows, edge_tags, norm, summary, write_defs  # noqa: E402
from rt_core import (FORMATS, R, cap, fdate, fmoney, ftime, hseed, lcfirst, make_variant, route, route2,  # noqa: E402
                     covers)
from rt_env import (AGENTS, CLOSERS, DECLINED, DEPTS, ENV_BY, ENVS, FIRST, FIXED, GENERIC_SUBJ, GREETS, LAST, RELS,  # noqa: E402
                    RESOLVED, SITES, TITLES, WHEN, _sub, body_layout, voice)
from rt_dom_a import DOMAINS_A  # noqa: E402

try:
    from rt_dom_b import DOMAINS_B  # noqa: E402
except ImportError:
    DOMAINS_B = []
try:
    from rt_dom_c import DOMAINS_C  # noqa: E402
except ImportError:
    DOMAINS_C = []

KEY = "gen_routing"
SEED = 20261212
FAMILY = "intent_business_support"
N_PAIRS = int(os.environ.get("RT_PAIRS", "6000"))
LEAN = HERE.parent.parent
RAW = LEAN / "data" / "v14_parts" / "raw"
MANIFEST = LEAN / "golden_src" / "MANIFEST.jsonl"
DOMAINS = DOMAINS_A + DOMAINS_B + DOMAINS_C
DOM = {d.key: d for d in DOMAINS}
VARS = {d.key: [make_variant(d, j) for j in range(d.nvar)] for d in DOMAINS}

STREETS = ["Maple Avenue", "Grant Street", "Orchard Road", "Hillcrest Drive", "Water Street", "Elm Terrace", "Kingsway",
           "Station Road", "Birch Lane", "Market Street", "Park Row", "Cedar Close", "Mill Lane", "Harbour Road",
           "Victoria Street", "Oak Crescent", "Church Walk", "Bridge Street"]
CITIES = ["Leeds", "Denver", "Toronto", "Cork", "Austin", "Glasgow", "Portland", "Adelaide", "Halifax", "Bristol"]
PCT = ["10", "15", "20", "25"]


def _num(lo, hi, fmt="{}"):
    return lambda r: fmt.format(r.randint(lo, hi))


GLOBAL_SLOTS = {
    "oid": _num(1000000, 9999999, "#{}"), "acct4": _num(1000, 9999), "n2": _num(11, 98), "weeks": _num(2, 6),
    "addr": lambda r: f"{r.randint(2, 480)} {r.choice(STREETS)}", "street": STREETS, "city": CITIES,
    "colleague": lambda r: f"{r.choice(FIRST)} {r.choice(LAST)}", "pct": PCT,
    "ref": _num(100000, 999999, "REF-{}"), "d": _num(2, 27),
}


# ============================================================================================= scenario building
def kinds_of(dom, qname):
    ks = set()
    for kinds, _ in dom.qby[qname].when:
        ks |= set(dom.issues) if kinds == "*" else set(kinds)
    return sorted(ks)


def compat(dom, kind, ctx):
    I = dom.issues[kind]
    return all(ctx.get(k) in vals for k, vals in I.req.items())


def excluded(dom, kind, used):
    return any(kind in g and (g & set(used)) for g in dom.excl)


def sample_issue(dom, kind, V, rng):
    I = dom.issues[kind]
    return {"k": kind, "p": {n: p.sample(rng, V) for n, p in sorted(I.P.items())}, "st": "open"}


def best1(dom, var, opts, ctx, it):
    return route(dom, var, opts, ctx, [dict(it, st="open")])[0]


def near_miss_kinds(dom, opts):
    ks = set()
    for n in opts:
        if n in dom.qby:
            for kinds, conds in dom.qby[n].when:
                if kinds != "*" and (conds or dom.qby[n].unless):
                    ks |= set(kinds)
            for kinds, _ in dom.qby[n].unless:
                if kinds != "*":
                    ks |= set(kinds)
    return sorted(ks)


def build(dom, var, opts, T, rng):
    V, catch = var["V"], dom.catch[0]
    order = var["order"]
    allk = sorted(dom.issues)
    for _ in range(120):
        ctx = {k: p.sample(rng, V) for k, p in sorted(dom.ctx.items())}
        if T == catch:
            nm = near_miss_kinds(dom, opts)
            gen = [k for k in allk if dom.issues[k].general]
            pool = nm if (nm and rng.random() < 0.75) else (gen or allk)
        else:
            pool = kinds_of(dom, T)
        pool = [k for k in pool if compat(dom, k, ctx)]
        if not pool:
            continue
        it = sample_issue(dom, rng.choice(pool), V, rng)
        if best1(dom, var, opts, ctx, it) != T:
            continue
        issues = [it]
        used = {it["k"]}
        n_extra = rng.choices([0, 1, 2], [0.5, 0.36, 0.14])[0]
        for _e in range(n_extra):
            for _a in range(40):
                k2 = rng.choice(allk)
                if k2 in used or not compat(dom, k2, ctx) or excluded(dom, k2, used):
                    continue
                it2 = sample_issue(dom, k2, V, rng)
                g2 = best1(dom, var, opts, ctx, it2)
                if T == catch:
                    ok = g2 == catch and (not dom.issues[k2].general or rng.random() < 0.3)
                else:
                    ok = (g2 != catch and g2 != T and order[g2] > order[T]) or (
                        g2 == catch and rng.random() < (0.15 if dom.issues[k2].general else 0.5))
                if ok:
                    issues.append(it2)
                    used.add(k2)
                    break
        n_dec = rng.choices([0, 1, 2], [0.45, 0.4, 0.15])[0]
        for _d in range(n_dec):
            for _a in range(40):
                k3 = rng.choice(allk)
                I3 = dom.issues[k3]
                if k3 in used or not compat(dom, k3, ctx) or I3.general or excluded(dom, k3, used):
                    continue
                st = rng.choice([s for s, ok in (("resolved", I3.past), ("declined", I3.neg), ("fixed", I3.fixable))
                                 if ok] or ["x"])
                if st == "x":
                    continue
                if st == "declined":
                    opn = {x["k"] for x in issues if x["st"] == "open"}
                    if any(k3 in g and (g & opn) for g in dom.clash):
                        continue
                it3 = sample_issue(dom, k3, V, rng)
                g3 = best1(dom, var, opts, ctx, it3)
                strong = g3 != catch and (T == catch or order[g3] < order[T])
                if strong or (g3 != catch and g3 != T and rng.random() < 0.25):
                    it3["st"] = st
                    issues.append(it3)
                    used.add(k3)
                    break
        rng.shuffle(issues)
        g = route(dom, var, opts, ctx, issues)[0]
        if g != T:
            continue
        return {"ctx": ctx, "iss": issues}
    return None


def mutations(dom, var, opts, sc, rng):
    """All single-fact changes (one param of one OPEN issue, or one context fact) that change the gold queue."""
    V = var["V"]
    g0 = route(dom, var, opts, sc["ctx"], sc["iss"])[0]
    out = []
    for i, it in enumerate(sc["iss"]):
        if it["st"] != "open":
            continue
        I = dom.issues[it["k"]]
        for pn in sorted(I.P):
            for alt in I.P[pn].alts(it["p"][pn], V, rng):
                iss = copy.deepcopy(sc["iss"])
                iss[i]["p"][pn] = alt
                g = route(dom, var, opts, sc["ctx"], iss)[0]
                if g != g0:
                    out.append((("iss", i, pn), alt, g))
    for i, it in enumerate(sc["iss"]):
        if it["st"] not in ("open", "fixed") or not dom.issues[it["k"]].fixable:
            continue
        iss = copy.deepcopy(sc["iss"])
        iss[i]["st"] = "fixed" if it["st"] == "open" else "open"
        if not any(x["st"] == "open" for x in iss):
            continue  # never flip the only open issue away (a message with nothing left to do)
        g = route(dom, var, opts, sc["ctx"], iss)[0]
        if g != g0:
            out.append((("st", i), iss[i]["st"], g))
    for cn in sorted(dom.ctx):
        if dom.ctx[cn].hidden:
            continue
        for alt in dom.ctx[cn].alts(sc["ctx"].get(cn), V, rng):
            ctx = dict(sc["ctx"], **{cn: alt})
            if not all(compat(dom, it["k"], ctx) for it in sc["iss"]):
                continue
            g = route(dom, var, opts, ctx, sc["iss"])[0]
            if g != g0:
                out.append((("ctx", cn), alt, g))
    return out


def apply_mut(sc, mut):
    where, alt, _ = mut
    sc2 = copy.deepcopy(sc)
    if where[0] == "iss":
        sc2["iss"][where[1]]["p"][where[2]] = alt
    elif where[0] == "st":
        sc2["iss"][where[1]]["st"] = alt
    else:
        sc2["ctx"][where[1]] = alt
    return sc2


# ============================================================================================= rendering
def slot_value(dom, name, seed, idx, pack):
    if name in pack["fixed"]:
        return pack["fixed"][name]
    if name in dom.fixed_slots:
        idx = 0
    pool = dom.slots.get(name, GLOBAL_SLOTS.get(name))
    assert pool is not None, (dom.key, name)
    if callable(pool):
        return pool(R(seed, "slot", idx, name))
    base = hseed(seed, "slotbase", name) % len(pool)
    step = 1 + hseed("step", name) % max(1, len(pool) - 1)
    while len(pool) > 1 and __import__("math").gcd(step, len(pool)) != 1:
        step += 1
    return pool[(base + idx * step) % len(pool)]


def fill(dom, t, seed, idx, pack, fields, embeds):
    def rep(m):
        k = m.group(1)
        if k.startswith("="):
            return embeds[k[1:]]
        if k in fields:
            return fields[k]
        if k in ("x1", "x2"):
            a = slot_value(dom, "street", seed, idx * 2, pack)
            b = slot_value(dom, "street", seed, idx * 2 + 1, pack)
            if a == b:
                b = STREETS[(STREETS.index(a) + 3) % len(STREETS)] if a in STREETS else b + " North"
            return a if k == "x1" else b
        v = slot_value(dom, k, seed, idx, pack)
        return fill(dom, v, seed, idx, pack, fields, embeds) if "{" in v else v
    return re.sub(r"\{(=?\w+)\}", rep, t)


def embed_text(p, v, sty):
    f = p.fields(v, random.Random(0), None, sty)
    for k in ("amt", "q", "time", "n"):
        if k in f:
            return f[k]
    raise ValueError(p.kind)


def render_issue(dom, sc, i, it, pack):
    """Returns (sentences, evidence) for one issue block."""
    seed = sc["seed"]
    I = dom.issues[it["k"]]
    today = pack["today"]
    date_ok = pack["date_ok"]
    if it["st"] in ("open", "fixed"):
        main = R(seed, "say", i).choice(I.say)
        embeds = {}
        for m in re.findall(r"\{=(\w+)\}", main):
            embeds[m] = embed_text(I.P[m], it["p"][m], R(seed, "sty", i, m).randrange(12))
        sents = [fill(dom, main, seed, i, pack, {}, embeds)]
        evidence = [sents[0]]
        pn_order = sorted(I.P)
        R(seed, "porder", i).shuffle(pn_order)
        for pn in pn_order:
            if "{=" + pn + "}" in main:
                continue
            p = I.P[pn]
            if p.kind in ("money", "int", "span") and not p.txt:
                continue
            v = it["p"][pn]
            sty = R(seed, "sty", i, pn).randrange(12)
            t = p.text(v, R(seed, "ptxt", i, pn, repr(v) if p.kind in ("bool", "cat") else ""), today, sty, date_ok)
            if not t:
                continue
            f = p.fields(v, R(seed, "pf", i, pn), today, sty)
            s = fill(dom, t, seed, i, pack, f, {})
            sents.append(s)
            evidence.append(s)
        if it["st"] == "fixed":
            c = R(seed, "fixed", i).choice(FIXED)
            sents.append(c)
            evidence.append(c)
        return sents, evidence
    rs = R(seed, "decoy", i)
    if it["st"] == "resolved":
        ph = fill(dom, rs.choice(I.past), seed, i, pack, {}, {})
        t = rs.choice(RESOLVED)
        s = _sub(t, {"past": ph, "Past": cap(ph), "when": rs.choice(WHEN)})
    else:
        ph = fill(dom, rs.choice(I.neg), seed, i, pack, {}, {})
        s = _sub(rs.choice(DECLINED), {"neg": ph})
    return [s], [s]


def make_pack(dom, sc, env):
    seed = sc["seed"]
    r = R(seed, "pack")
    first, last = r.choice(FIRST), r.choice(LAST)
    org = dom.orgs[hseed(seed, "org") % len(dom.orgs)]
    dom_part = re.sub(r"[^a-z]", "", org.lower())[:14]
    today = dt.date(2024, 1, 8) + dt.timedelta(days=hseed(seed, "today") % 960)
    t = r.randrange(7 * 60, 22 * 60)
    dept = r.choice(DEPTS)
    title = r.choice(TITLES)
    pk = {
        "rng": R(seed, "envrng"), "first": first, "last": last, "name": f"{first} {last}",
        "email": f"{first.lower()}.{re.sub(r'[^a-z]', '', last.lower())}@{r.choice(['mailbox.com', 'inbox.net', 'postmail.org', 'webmail.co'])}",
        "org": org, "support": f"help@{dom_part}.com", "phone": f"555-{r.randint(100, 999)}-{r.randint(1000, 9999)}",
        "today": today, "date_long": fdate(today, 3), "date_iso": today.isoformat(), "time": ftime(t, r.randrange(3)),
        "ticket": f"{dom.key[:3].upper()}-{r.randint(10000, 99999)}", "agent": r.choice(AGENTS),
        "acct": r.choice([f"Account number: {r.randint(10000000, 99999999)}", f"Customer ID: C{r.randint(100000, 999999)}",
                          f"Reference: {r.randint(100000, 999999)}"]),
        "ref": f"WEB-{r.randint(100000, 999999)}", "platform": r.choice(["iOS app 7.3.1", "Android app 6.9.0", "web app"]),
        "cprio": r.choice(["urgent", "high", "normal", "low"]),
        "colleague": f"- {r.choice(FIRST)}, {r.choice(['front office', 'sales team', 'reception', 'accounts team'])}",
        "branch": r.choice(["the front counter", "the city-centre office", "the walk-in help desk", "the reception desk"]),
        "rel": r.choice(RELS), "helper": f"{r.choice(FIRST)} {last}",
        "addr": f"{r.randint(2, 300)} {r.choice(STREETS)}\n{r.choice(CITIES)}", "short": f"text {r.randint(60000, 69999)}",
        "org_handle": dom_part[:12] + "_help", "handle": f"{first.lower()}{r.randint(7, 99)}",
        "desk": dom.desk or "service", "desk_email": f"{(dom.desk or 'service').lower().replace(' ', '')}@{dom_part}.com",
        "dept": dept, "site": r.choice(SITES), "title": title, "channel": r.choice(["it-help", "ask-hr", "helpdesk", "support"]),
        "away": r.choice(["on leave", "travelling", "off sick", "at a client site"]), "mgr": f"{r.choice(FIRST)} {r.choice(LAST)}",
        "ext": str(r.randint(2000, 7999)), "portal": r.choice(["the People Portal", "the employee self-service site", "MyHR"]),
        "eid": f"E{r.randint(10000, 99999)}", "conf": r.choice(["yes", "no"]),
        "old_subject": r.choice(["Your recent request", "Case update", "We've received your message"]),
        "old_date": fdate(today - dt.timedelta(days=r.randint(20, 200)), 3),
        "old_ticket": f"#{r.randint(100000, 999999)}",
        "subject": r.choice(GENERIC_SUBJ + dom.subjects), "signoff": r.choice(["Thanks,", "Best,", "Regards,", "Cheers,"]),
    }
    pk["greet"] = _sub(r.choice(dom.greet or GREETS), {"org": org})
    pk["date_ok"] = env["date"]
    pk["sig"] = pk["name"]
    pk["fixed"] = {"org": org, "first": first, "last": last, "dept": dept, "title": title}
    pk["subject"] = fill(dom, pk["subject"], seed, 99, pk, {}, {})
    return pk


def render(dom, var, sc):
    env = ENV_BY[sc["env"]]
    seed = sc["seed"]
    pk = make_pack(dom, sc, env)
    blocks, evidence = [], []
    for i, it in enumerate(sc["iss"]):
        s, ev = render_issue(dom, sc, i, it, pk)
        blocks.append(("open" if it["st"] in ("open", "fixed") else "decoy", s))
        evidence += ev
    # context lines (body) and signature lines
    ctx_lines = []
    for cn in sorted(dom.ctx):
        p = dom.ctx[cn]
        if p.hidden:
            continue
        v = sc["ctx"].get(cn)
        t = p.text(v, R(seed, "ctx", cn, repr(v)), pk["today"], 0, pk["date_ok"])
        if t:
            s = fill(dom, t, seed, 50, pk, {}, {})
            ctx_lines.append(s)
            evidence.append(s)
    rx = R(seed, "extras")
    extras = {"ctx": ctx_lines}
    if dom.fillers and rx.random() < 0.3:
        extras["filler"] = rx.choice(dom.fillers)
    if sc.get("kw"):
        extras["kw"] = sc["kw"]
    if rx.random() < 0.6:
        extras["closer"] = rx.choice(dom.closers or CLOSERS)
    n_open = sum(b[0] == "open" for b in blocks)
    styles = [s for s in env["style"] if s != "bullets" or n_open >= 2]
    style = R(seed, "style").choice(styles or ["para"])
    if style == "lines":
        style = "para"
    text, lines = body_layout(blocks, extras, R(seed, "layout"), style)
    pk["body"], pk["lines"] = text, lines
    pk["vbody"] = voice(text, R(seed, "voice"))
    pk["topic"] = sc.get("topic") or ""
    state = env["fn"](pk).strip()
    state = re.sub(r"[ \t]+\n", "\n", state)
    state = re.sub(r"\n{3,}", "\n\n", state)
    return state, {"evidence": evidence, "style": style, "env": env["id"], "voice": env["voice"]}


# ============================================================================================= instructions
INSTR = [
    "Under {org_s} routing definitions, which queue should this {doc} be routed to, counting only issues the sender "
    "still needs handled and, where several queues apply, given that {rule}?",
    "Which queue does this {doc} belong in according to the queue definitions, where resolved or explicitly declined "
    "matters do not count and, if more than one queue fits, {rule}?",
    "Applying {org_s} routing policy to what the sender actually needs now (when queues overlap, {rule}), where should "
    "this {doc} go?",
    "Route this {doc}: based only on its open issues and the definitions, and knowing that {rule} when several apply, "
    "which queue receives it?",
    "To which team should {org} assign this {doc}, given that only the sender's open requests count and {rule} when "
    "more than one team's definition applies?",
    "According to the routing definitions, which single queue takes this {doc} as a whole, if {rule} whenever it raises "
    "issues for several queues and matters already resolved or declined are ignored?",
    "Which queue is the correct destination for this {doc} under the definitions, deciding on what the sender needs "
    "handled now, where {rule} on any overlap?",
    "If {org_s} routing rules are applied exactly (only current needs count, {rule} on overlap, otherwise the "
    "catch-all), which queue gets this {doc}?",
    "Given the queue definitions and the rule that {rule} when {a_doc} fits several queues, which queue should handle "
    "this {doc}, ignoring anything already sorted out or explicitly not wanted?",
    "Which of {org_s} queues must this {doc} be sent to, judging its open issues against each definition, if {rule} "
    "when more than one applies?",
    "Where does this {doc} get routed under the definitions, where only unresolved requests count and {rule} when "
    "definitions overlap?",
    "Deciding on substance rather than wording, which queue should take this {doc} under {org_s} definitions, where "
    "resolved or declined matters are ignored and {rule} if several queues apply?",
]
INSTR_TOPIC = [
    "Judging the substance rather than any category or priority the sender picked, which queue should this {doc} go "
    "to under {org_s} definitions, where only open issues count and {rule} on overlap?",
    "Ignoring the topic the sender chose and counting only what still needs handling, which queue does this {doc} "
    "belong in under the definitions, if {rule} when several apply?",
    "Which queue should {org} route this {doc} to, deciding on its content (not the sender's own category choice), "
    "where resolved or declined matters are ignored and {rule} when queues overlap?",
    "Under the routing definitions, and regardless of the category selected on the form, which queue takes this "
    "{doc}, where {rule} if more than one queue applies to its open issues?",
]


# ============================================================================================= tags / checks
def edge_and_case(dom, var, opts, sc, env, state, muts):
    V, catch, order = var["V"], dom.catch[0], var["order"]
    g, app, excs = route(dom, var, opts, sc["ctx"], sc["iss"])
    tags, case = [], []
    for where, alt, _ in muts:
        if where[0] != "iss":
            continue
        it = sc["iss"][where[1]]
        p = dom.issues[it["k"]].P[where[2]]
        v = it["p"][where[2]]
        if v is None:
            tags.append("missing_info")
        k = p.kind
        if k in ("money", "int"):
            tags.append("quantifier" if p.quant else "numeric")
        elif k in ("days", "tod", "span"):
            tags.append("temporal")
        elif k == "qty":
            tags += ["units", "numeric"]
    if any(v is None for it in sc["iss"] if it["st"] == "open" for v in it["p"].values()):
        tags.append("missing_info")
    if any(e for e in excs):
        tags.append("exception")
        case.append("exception")
    opened = [i for i, it in enumerate(sc["iss"]) if it["st"] == "open"]
    bests = {min(app[i], key=lambda n: order[n]) for i in opened if app[i]}
    if len(opened) >= 2:
        case.append("multi_issue")
    if len(bests) >= 2:
        tags.append("multi_hop")
        case.append("priority_conflict")
    if any(it["st"] == "declined" for it in sc["iss"]):
        tags.append("negation")
        case.append("decoy_declined")
    if any(it["st"] == "resolved" for it in sc["iss"]):
        case.append("decoy_resolved")
    if any(it["st"] == "fixed" for it in sc["iss"]):
        case.append("decoy_fixed_inline")
    if env["reported"]:
        tags.append("reported_speech")
    if len(state) >= 1400:
        tags.append("long_context")
    if g == catch:
        case.append("catch_all")
        if any(dom.issues[sc["iss"][i]["k"]].general is False for i in opened):
            case.append("near_miss")
    if sc.get("topic"):
        case.append("topic_decoy")
    if sc.get("kw"):
        case.append("keyword_decoy")
    hidden = [q.name for q in dom.queues if q.name not in opts]
    for i in opened:
        it = sc["iss"][i]
        for n in hidden:
            if covers(dom.qby[n], it["k"], it["p"], sc["ctx"], V)[0] and (g == catch or order[n] < order[g]):
                case.append("queue_not_offered")
    tags = [t for t in dict.fromkeys(tags)]
    for t in tags:
        assert t in EDGE_TAGS, t
    return (",".join(tags) if tags else None), sorted(set(case))


def nstr(s):
    s = re.sub(r"[^a-z0-9$%]+", " ", s.lower()).strip()
    return " " + re.sub(r"(?<= )(um|uh) (?=\S)", "", " " + s + " ").strip() + " "


def recheck(dom, var, row, sc):
    opts = row["options"]
    gold = row["gold"]
    sc2 = json.loads(json.dumps(sc))
    g1 = route(dom, var, opts, sc2["ctx"], sc2["iss"])[0]
    g2 = route2(dom, {n: var["defs"][n] for n in opts}, var["V"], opts, sc2["ctx"], sc2["iss"], var["fmt"])
    assert g1 == gold == g2, (row["rid"], g1, g2, gold)
    assert dom.catch[0] in opts and gold in opts and len(set(opts)) == len(opts)
    assert 8 <= len(opts) <= 30, len(opts)
    st = nstr(row["state"])
    for ev in row["_evidence"]:
        assert nstr(ev) in st, (row["rid"], ev, row["state"])
    assert gold.lower() not in row["state"].lower(), (row["rid"], gold)
    if sc2.get("topic"):
        assert sc2["topic"] != gold


# ============================================================================================= main
def choose_opts(dom, var, rng):
    names = [q.name for q in dom.queues]
    k = 0 if rng.random() < 0.45 else rng.choice([1, 1, 2, 2, 3, 4])
    k = min(k, len(names) + 1 - 8)
    drop = set(rng.sample(names, k)) if k > 0 else set()
    opts = [n for n in names if n not in drop] + [dom.catch[0]]
    if rng.random() < 0.6:
        rng.shuffle(opts)
    else:
        opts.sort(key=lambda n: var["order"][n])
    return opts


def pick_target(dom, var, opts, counts, rng):
    catch = dom.catch[0]
    w = []
    for n in opts:
        c = counts[(dom.key, n)]
        base = 0.9 if n == catch else 1.0
        w.append(base / (1.0 + c) ** 2)
    return rng.choices(opts, w)[0]


def main():
    t0 = time.time()
    rng = random.Random(SEED)
    per_dom = {d.key: N_PAIRS // len(DOMAINS) + (1 if i < N_PAIRS % len(DOMAINS) else 0) for i, d in enumerate(DOMAINS)}
    counts = collections.Counter()
    nd = NearDup(thr=0.8)
    rows, fails = [], collections.Counter()
    envs_used, styles_used = collections.Counter(), collections.Counter()
    seen = set()
    for dom in DOMAINS:
        envs = [e for e in ENVS if e["side"] == dom.env] + [ENV_BY[x] for x in dom.extra_env]
        made = 0
        tries = 0
        while made < per_dom[dom.key]:
            tries += 1
            assert tries < per_dom[dom.key] * 400, (dom.key, made, fails.most_common(8))
            var = VARS[dom.key][made % dom.nvar]
            r = random.Random(hseed(SEED, dom.key, tries))
            opts = choose_opts(dom, var, r)
            T = pick_target(dom, var, opts, counts, r)
            sc = build(dom, var, opts, T, r)
            if sc is None:
                fails["build"] += 1
                continue
            muts = mutations(dom, var, opts, sc, r)
            if not muts:
                fails["no_twin"] += 1
                continue
            def mw(m):
                w = 1.0 / (1.0 + counts[(dom.key, m[2])]) ** 1.5
                if m[0][0] == "iss":
                    k = dom.issues[sc["iss"][m[0][1]]["k"]].P[m[0][2]].kind
                    w *= 8.0 if k in ("int", "money", "days", "tod", "qty", "span") else 5.0
                elif m[0][0] == "ctx":
                    w *= 1.0
                if m[2] == dom.catch[0]:
                    w *= 0.6
                return w
            mut = r.choices(muts, [mw(m) for m in muts])[0]
            sc["seed"] = hseed(SEED, dom.key, "sc", tries)
            env = r.choice(envs)
            sc["env"] = env["id"]
            gold_t = mut[2]
            if env["topic"]:
                cand = [n for n in opts if n not in (T, gold_t)]
                sc["topic"] = r.choice(cand) if (cand and r.random() < 0.6) else r.choice(dom.topics)
            if dom.kw and r.random() < 0.25:
                sc["kw"] = r.choice(dom.kw)
            tw = apply_mut(sc, mut)
            state_b, info_b = render(dom, var, sc)
            state_t, info_t = render(dom, var, tw)
            if state_b == state_t:
                fails["same_text"] += 1
                continue
            if norm(state_b) in seen or norm(state_t) in seen:
                fails["dup"] += 1
                continue
            if nd.seen(state_b, add=False) or nd.seen(state_t, add=False):
                fails["near_dup"] += 1
                continue
            if T.lower() in state_b.lower() or gold_t.lower() in state_t.lower():
                fails["name_leak"] += 1
                continue
            nd.seen(state_b, add=True)
            seen.add(norm(state_b))
            seen.add(norm(state_t))
            org = dom.orgs[hseed(sc["seed"], "org") % len(dom.orgs)]
            ri = R(sc["seed"], "instr")
            tmpl = ri.choice(INSTR_TOPIC if env["topic"] else INSTR)
            org_s = org + ("'" if org.endswith("s") else "'s")
            a_doc = ("an " if dom.doc[0] in "aeiou" else "a ") + dom.doc
            ins = tmpl.format(org=org, org_s=org_s, doc=dom.doc, a_doc=a_doc, rule=var["rule"])
            base_rid = f"{KEY}-{dom.key}-{made:05d}"
            for which, s, st, info in (("base", sc, state_b, info_b), ("twin", tw, state_t, info_t)):
                g = T if which == "base" else gold_t
                muts_s = muts if which == "base" else mutations(dom, var, opts, s, r)
                edge, case = edge_and_case(dom, var, opts, s, env, st, muts_s)
                _, app, _ = route(dom, var, opts, s["ctx"], s["iss"])
                orig = {"queue": g, "priority": {n: var["nums"][n] for n in opts},
                        "issues": [{"kind": it["k"], "status": it["st"], "facts": it["p"],
                                    "covered_by": app[i]} for i, it in enumerate(s["iss"])],
                        "context": s["ctx"], "thresholds": var["V"]}
                if which == "twin":
                    w0 = mut[0]
                    if w0[0] == "iss":
                        fact, frm = f"issue{w0[1]}.{w0[2]}", sc["iss"][w0[1]]["p"][w0[2]]
                    elif w0[0] == "st":
                        fact, frm = f"issue{w0[1]}.status", sc["iss"][w0[1]]["st"]
                    else:
                        fact, frm = f"context.{w0[1]}", sc["ctx"].get(w0[1])
                    orig["changed"] = {"fact": fact, "from": frm, "to": mut[1]}
                meta = {"dataset": f"program generator golden_src/gen/{KEY}.py", "config": f"{dom.key}:v{var['j']}:{env['id']}",
                        "revision": None, "licence": "Generated by Claude-written program in this repo (no third-party text)",
                        "split": "train", "orig_label": orig, "family": FAMILY, "edge": edge, "defs": var["qid"],
                        "case": case, "domain": dom.key}
                if which == "twin":
                    meta["twin_of"] = base_rid
                row = {"key": KEY, "rid": base_rid if which == "base" else base_rid + "-t", "state": st,
                       "instructions": ins, "options": list(opts), "gold": g, "soft": None, "meta": meta,
                       "_evidence": info["evidence"], "_sc": s, "_dom": dom.key, "_var": var["j"]}
                rows.append(row)
                counts[(dom.key, g)] += 1
                envs_used[env["id"]] += 1
                styles_used[(env["id"], info["style"])] += 1
            made += 1
        print(f"{dom.key}: {made} pairs, tries={tries}, {time.time() - t0:.0f}s", flush=True)
    # ------------------------------------------------------------ self-check (independent evaluator + text evidence)
    by = {r["rid"]: r for r in rows}
    for r in rows:
        dom, var = DOM[r["_dom"]], VARS[r["_dom"]][r["_var"]]
        recheck(dom, var, r, r["_sc"])
        if "twin_of" in r["meta"]:
            b = by[r["meta"]["twin_of"]]
            assert b["gold"] != r["gold"] and b["instructions"] == r["instructions"] and b["options"] == r["options"]
            sb, st = b["_sc"], r["_sc"]
            diffs = [(i, k) for i, (x, y) in enumerate(zip(sb["iss"], st["iss"])) for k in x["p"] if x["p"][k] != y["p"][k]]
            diffs += [("ctx", k) for k in set(sb["ctx"]) | set(st["ctx"]) if sb["ctx"].get(k) != st["ctx"].get(k)]
            diffs += [("st", i) for i, (x, y) in enumerate(zip(sb["iss"], st["iss"])) if x["st"] != y["st"]]
            assert len(diffs) == 1, (r["rid"], diffs)
            assert [x["k"] for x in sb["iss"]] == [x["k"] for x in st["iss"]]
    src = sorted(HERE.glob("rt_*.py")) + [Path(__file__).resolve()]
    h = hashlib.sha256()
    for p in src:
        h.update(p.read_bytes())
    rev = "gen-v1+sha256:" + h.hexdigest()[:16]
    for r in rows:
        r["meta"]["revision"] = rev
        for k in ("_evidence", "_sc", "_dom", "_var"):
            del r[k]
    check_rows(rows)
    dry = os.environ.get("RT_OUT")
    out = Path(dry) if dry else RAW / f"{KEY}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    back = [json.loads(x) for x in open(out)]
    assert back == rows
    summary(rows)
    print("fails:", fails.most_common())
    print("envelopes used:", len(envs_used), "| envelope x layout templates:", len(styles_used))
    golds = collections.Counter(r["gold"] for r in rows)
    print("distinct golds:", len(golds), "max share:", round(max(golds.values()) / len(rows), 4))
    print("option-count range:", min(len(r["options"]) for r in rows), max(len(r["options"]) for r in rows),
          "| distinct option lists:", len({tuple(sorted(r["options"])) for r in rows}),
          "| defs sets:", len({r["meta"]["defs"] for r in rows}))
    cases = collections.Counter(c for r in rows for c in r["meta"]["case"])
    print("cases:", dict(cases.most_common()))
    if dry:
        print(f"DRY RUN wrote {out} ({len(rows)} rows) in {time.time() - t0:.0f}s")
        return
    for d in DOMAINS:
        for var in VARS[d.key]:
            write_defs(f"{KEY}__{var['qid']}", var["defs"])
    qn = [len(d.queues) + 1 for d in DOMAINS]
    on = [len(r["options"]) for r in rows]
    nst = sum(1 for r in rows if r["meta"].get("orig_label", {}).get("changed", {}).get("fact", "").endswith(".status"))
    notes = (f"Program-generated ticket/request routing under an explicit routing policy: {len(DOMAINS)} domains "
             f"({', '.join(d.what for d in DOMAINS)}), {min(qn)}-{max(qn)} queues per policy (catch-all included; "
             f"{min(on)}-{max(on)} options per row after per-row queue subsets), 4 policy variants per "
             f"domain (thresholds, priority order and notation differ; same queue names) = {len(DOMAINS) * 4} defs "
             f"sets; per-row queue subsets. Each definition states scope, exceptions and a priority number; the "
             f"instruction states the priority rule and that only open issues count. Texts are realistic requests in "
             f"{len(envs_used)} envelope templates ({len(styles_used)} envelope x layout surface forms): multi-issue "
             f"requests resolved by priority, resolved/declined decoys that would outrank the gold, sender-chosen "
             f"topics naming a wrong queue, keyword look-alikes, catch-all near misses (thresholds at the boundary, "
             f"exceptions, unit conversion, dates relative to the message date, time of day). Every base row has a "
             f"fact-flip twin (meta.twin_of) changing one fact so the gold queue changes ({nst} of the twins flip whether "
             f"an issue is still open, the rest flip a stated fact or context fact). Labels recomputed by an "
             f"independent evaluator (rules compiled to Python, priority parsed from the definition text); decisive "
             f"fact sentences verified in the text; gold queue name never in the text.")
    append_manifest({"key": KEY, "family": FAMILY, "dataset": f"{KEY} (program generator, golden_src/gen/{KEY}.py)",
                     "licence": "n/a (program-generated; Claude-written templates, definitions and rules; labels by "
                                "construction)",
                     "rows": len(rows), "qtype": "choice", "yesno_share": None, "edge_tags": edge_tags(rows),
                     "notes": notes})
    print(f"wrote {out} ({len(rows)} rows) in {time.time() - t0:.0f}s")


def append_manifest(rec):
    line = json.dumps(rec, ensure_ascii=False)
    for _ in range(20):
        text = MANIFEST.read_text() if MANIFEST.exists() else ""
        lines = text.splitlines()
        mine = [i for i, ln in enumerate(lines) if ln.strip() and json.loads(ln).get("key") == rec["key"]]
        if not mine:
            with open(MANIFEST, "a") as fh:
                fh.write(line + "\n")
            return
        if len(mine) == 1 and lines[mine[0]] == line:
            return
        for i in mine:
            assert json.loads(lines[i]).get("family") == FAMILY
        new = [ln for i, ln in enumerate(lines) if i not in set(mine)] + [line]
        tmp = MANIFEST.with_suffix(".jsonl.tmp_rt")
        tmp.write_text("\n".join(new) + "\n")
        if (MANIFEST.read_text() if MANIFEST.exists() else "") == text:
            os.replace(tmp, MANIFEST)
            return
        tmp.unlink()
        time.sleep(0.2)
    raise RuntimeError("manifest kept changing")


if __name__ == "__main__":
    main()
