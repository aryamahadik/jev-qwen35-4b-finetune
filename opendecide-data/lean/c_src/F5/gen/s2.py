"""S2 event-log sampler (G0 section 5, S2; SEM-11, -16, -17 log form, -19, -20, -26, -27, -33).

M = {world, period [D_start, D_end] (ISO), S (authoritative source name), items [{id, noun, track: "valid"|"status"}],
     entries [entry], statuses [...], docs [...], risks [...]}
entry = {eid, date, type, item, actor?, holder?/to?/days?/status?/doc?/risk?/target?/field?/value?/lo?/hi?/kind?/
         party?/claim?}
types: create (holder), transfer (actor, to), renew (actor, days), status (status), file (actor, doc),
       report (actor, risk), correction (target, field, value), void (target), fail (actor, kind, cue: failed to |
       neglected to | omitted to | did not manage to | refused to | declined to | was prevented from), asof (item,
       state valid|status, value), noev (kind, actor, item, lo, hi), notice (party, verb stated|denied, claim event)
Solver A: forward event replay after resolving VOID / CORRECTION (SEM-16, SEM-33).
"""
from __future__ import annotations

import copy
import datetime as dt

from .common import MONTHS

FAIL_CUES = ["failed to", "neglected to", "omitted to", "did not manage to"]
REFUSE_CUES = ["refused to", "declined to", "was prevented from"]
VERB = {"renew": ("renew", "renewed", "renewing"), "report": ("report", "reported", "reporting"),
        "file": ("file", "filed", "filing")}


def D(s):
    return dt.date.fromisoformat(s)


def S_(d):
    return d.isoformat()


# ---------------------------------------------------------------------------------------------------------------------
# replay (solver A)

def resolve(M):
    """Remaining entries with corrected values (SEM-16): VOID cancels its target; voiding a CORRECTION restores the
    corrected entry; CORRECTION replaces one value field of its target."""
    E = {e["eid"]: copy.deepcopy(e) for e in M["entries"]}
    voided = set()
    # voids of voids are not generated; a VOID may target a CORRECTION or a plain entry
    for e in M["entries"]:
        if e["type"] == "void":
            voided.add(e["target"])
    for e in M["entries"]:
        if e["type"] == "correction" and e["eid"] not in voided and e["target"] not in voided:
            t = E[e["target"]]
            t[e["field"]] = e["value"]
    rem = [E[e["eid"]] for e in M["entries"] if e["eid"] not in voided and e["type"] not in ("correction", "void")]
    rem.sort(key=lambda e: (e["date"], e["eid"]))
    return rem


def holder_on(rem, item, day):
    h = None
    for e in rem:
        if e.get("item") != item or e["date"] > day:
            continue
        if e["type"] == "create":
            h = e["holder"]
        elif e["type"] == "transfer":
            h = e["to"]
    return h


def valid_on(rem, item, day):
    last = None
    for e in rem:
        if e.get("item") == item and e["type"] == "renew" and e["date"] <= day:
            last = e
    if last is None:
        return False
    return D(day) <= D(last["date"]) + dt.timedelta(days=int(last["days"]))


def status_on(rem, item, day):
    s = None
    for e in rem:
        if e.get("item") == item and e["type"] == "status" and e["date"] <= day:
            s = e["status"]
    return s


def events(rem, kind, actor, item):
    out = []
    for e in rem:
        if e.get("item") != item:
            continue
        if kind == "renew" and e["type"] == "renew" and (actor is None or e["actor"] == actor):
            out.append(e)
        elif kind.startswith("report:") and e["type"] == "report" and e["risk"] == kind[7:] and \
                (actor is None or e["actor"] == actor):
            out.append(e)
        elif kind.startswith("file:") and e["type"] == "file" and e["doc"] == kind[5:] and \
                (actor is None or e["actor"] == actor):
            out.append(e)
    return out


def in_range(day, lo, hi):
    return (lo is None or day >= lo) and (hi is None or day <= hi)


def eval_lf(lf, M, rem=None):
    rem = resolve(M) if rem is None else rem
    op = lf[0]
    if op == "not":
        x = eval_lf(lf[1], M, rem)
        return None if x is None else (not x)
    if op == "and":
        xs = [eval_lf(a, M, rem) for a in lf[1:]]
        if any(x is False for x in xs):
            return False
        return True if all(x is True for x in xs) else None
    if op == "ev":
        _, kind, actor, item, lo, hi = lf
        item = item.rsplit(" ", 1)[1]
        evs = [e for e in events(rem, kind, actor, item) if in_range(e["date"], lo, hi)]
        if evs:
            return True
        if M["world"] == "closed":
            return False
        alo = lo or M["period"][0]
        ahi = hi or M["period"][1]
        for e in rem:
            if e["type"] == "noev" and e["kind"] == kind and e["actor"] == actor and e["item"] == item and \
                    e["lo"] <= alo and e["hi"] >= ahi:
                return False
        return None
    if op == "valid":
        _, item, day = lf
        item = item.rsplit(" ", 1)[1]
        if M["world"] == "closed":
            return valid_on(rem, item, day)
        return _asof(rem, item, "valid", day)
    if op == "status":
        _, item, s, day = lf
        item = item.rsplit(" ", 1)[1]
        if M["world"] == "closed":
            cur = status_on(rem, item, day)
            if cur is None:
                return None
            return cur == s
        v = _asof(rem, item, "status", day)
        return None if v is None else (v == s)
    if op == "still":
        _, item, day = lf
        item = item.rsplit(" ", 1)[1]
        if M["world"] != "closed":
            return None
        earlier = any(valid_on(rem, item, S_(D(M["period"][0]) + dt.timedelta(days=i)))
                      for i in range((D(day) - D(M["period"][0])).days))
        return bool(earlier and valid_on(rem, item, day))
    raise ValueError(op)


def _asof(rem, item, state, day):
    for e in rem:
        if e["type"] == "asof" and e.get("item") == item and e["state"] == state and e["day"] == day:
            return e["value"]
    return None


def solve_a(M, lfs):
    rem = resolve(M)
    check(M, rem)
    out = []
    for lf in lfs:
        v = eval_lf(lf, M, rem)
        if v is None:
            raise ValueError("undetermined")
        out.append(v)
    return out


def check(M, rem):
    """Generator asserts (SEM-16, -19, -26, -33; F5-R4-06, F5-R5-02, -05, -06, -07)."""
    ps, pe = M["period"]
    seen = set()
    for e in M["entries"]:
        assert ps <= e["date"] <= pe, "entry outside the covered period"
    # one entry per item per day; actors of renewals = holder on that day, of transfers = holder the day before
    days = set()
    for e in M["entries"]:
        if e.get("item") and e["type"] not in ("correction", "void", "notice", "noev", "asof", "fail"):
            if (e["item"], e["date"]) in days:
                raise ValueError("two entries on one day for one item")
            days.add((e["item"], e["date"]))
    for e in rem:
        if e["type"] == "renew" and holder_on(rem, e["item"], e["date"]) != e["actor"]:
            raise ValueError("renewal actor is not the holder")
        if e["type"] == "transfer":
            prev = S_(D(e["date"]) - dt.timedelta(days=1))
            if holder_on(rem, e["item"], prev) != e["actor"]:
                raise ValueError("transfer actor is not the holder")
    for e in rem:
        if e["type"] == "fail":
            evs = events(rem, e["kind"], e["actor"], e["item"])
            evs_all = [x for x in M["entries"] if x["type"] == e["kind"].split(":")[0] and x.get("actor") == e["actor"]
                       and x.get("item") == e["item"]]
            if evs or evs_all:
                raise ValueError("failure cue contradicted")
        if e["type"] == "asof":
            if e["state"] == "valid" and valid_on(rem, e["item"], e["day"]) != e["value"]:
                raise ValueError("as-of statement differs from replay")
            if e["state"] == "status":
                cur = status_on(rem, e["item"], e["day"])
                if cur is None or cur != e["value"]:
                    raise ValueError("as-of status differs from replay")
        if e["type"] == "noev":
            evs = [x for x in events(rem, e["kind"], e["actor"], e["item"]) if in_range(x["date"], e["lo"], e["hi"])]
            if evs:
                raise ValueError("negative event statement contradicted")


# ---------------------------------------------------------------------------------------------------------------------
# rendering

def item_txt(M, iid):
    it = next(i for i in M["items"] if i["id"] == iid)
    return f"{it['noun']} {iid}"


def cap(s):
    return s[:1].upper() + s[1:]


def kind_np(kind):
    if kind == "renew":
        return "renewal"
    if kind.startswith("report:"):
        return f"report of a {kind[7:]}"
    return f"filing of the {kind[5:]}"


def event_vp(kind, item, form):
    """verb phrase for an event kind: form base | past | ing."""
    if kind == "renew":
        v = VERB["renew"][{"base": 0, "past": 1, "ing": 2}[form]]
        return f"{v} {item}"
    if kind.startswith("report:"):
        v = VERB["report"][{"base": 0, "past": 1, "ing": 2}[form]]
        return f"{v} a {kind[7:]} for {item}"
    v = VERB["file"][{"base": 0, "past": 1, "ing": 2}[form]]
    return f"{v} the {kind[5:]} for {item}"


def entry_text(M, e):
    t = e["type"]
    it = item_txt(M, e["item"]) if e.get("item") else None
    if t == "create":
        s = f"{cap(it)} was created for {e['holder']}"
    elif t == "transfer":
        s = f"{e['actor']} transferred {it} to {e['to']}"
    elif t == "renew":
        s = f"{e['actor']} renewed {it} for {e['days']} days"
    elif t == "status":
        s = f"The status of {it} was set to {e['status']}"
    elif t == "file":
        s = f"{e['actor']} filed the {e['doc']} for {it}"
    elif t == "report":
        s = f"{e['actor']} reported a {e['risk']} for {it}"
    elif t == "correction":
        what = {"days": "the number of days is", "to": "the new holder is", "holder": "the holder is",
                "status": "the status is"}[e["field"]]
        s = f"CORRECTION of {e['target']}: {what} {e['value']}"
    elif t == "void":
        s = f"VOID of {e['target']}"
    elif t == "fail":
        cue = e["cue"]
        form = "ing" if cue == "was prevented from" else "base"
        s = f"{e['actor']} {cue} {event_vp(e['kind'], it, form)}"
    elif t == "asof":
        if e["state"] == "valid":
            s = f"As of {e['day']}, {it} is {'' if e['value'] else 'not '}valid"
        else:
            s = f"As of {e['day']}, the status of {it} is {e['value']}"
    elif t == "noev":
        s = f"No {kind_np(e['kind'])} of {it} by {e['actor']} took place from {e['lo']} to {e['hi']}" \
            if e["kind"] == "renew" else \
            f"No {kind_np(e['kind'])} for {it} by {e['actor']} took place from {e['lo']} to {e['hi']}"
    elif t == "notice":
        c = e["claim"]
        s = f"{e['party']} {e['verb']} that {c['actor']} {event_vp(c['kind'], item_txt(M, c['item']), 'past')}"
        if c.get("range"):
            s += " " + c["range"]
    else:
        raise ValueError(t)
    return f"{e['eid']}. {s}."


def doc_ir(M, *, attack=None, inert=None):
    evs = [{"ts": e["date"], "text": entry_text(M, e)} for e in sorted(M["entries"], key=lambda e: (e["date"],
                                                                                                    e["eid"]))]
    if attack:
        evs.append({"ts": M["period"][1], "text": attack})
    return {"title": f"{cap(M['items'][0]['noun'])} log", "blocks": [{"type": "events", "events": evs}]}


# ---------------------------------------------------------------------------------------------------------------------
# sampler

def rand_day(rng, lo, hi):
    a, b = D(lo), D(hi)
    return S_(a + dt.timedelta(days=rng.randint(0, (b - a).days)))


def sample(rng, card, kind, depth, world):
    """A log for one base. kind: 'valid' | 'status' | 'ev_renew' | 'ev_report'."""
    w0 = D(card["window"][0])
    start = w0 + dt.timedelta(days=rng.randint(0, 200))
    length = rng.randint(70, 150)
    end = start + dt.timedelta(days=length)
    M = {"world": world, "period": [S_(start), S_(end)], "S": card["S"], "items": [], "entries": [],
         "statuses": card["statuses"], "docs": card["docs"], "risks": card["risks"]}
    ent = card["ent"]
    ids = list(ent["ids"])
    rng.shuffle(ids)
    main = ids[0]
    look = lookalike(main, ids, rng)
    track = "status" if (kind == "status" or (card.get("track") == "status" and kind != "valid"
                                                 and rng.random() < 0.5)) else "valid"
    M["items"].append({"id": main, "noun": ent["noun"], "track": track})
    if rng.random() < 0.25:
        M["items"].append({"id": look, "noun": ent["noun"],
                           "track": "status" if card.get("track") == "status" and rng.random() < 0.5 else "valid"})
    people = list(card["people"])
    rng.shuffle(people)
    holders = people[:3]
    others = people[3:6]
    n = [0]

    def eid():
        n[0] += 1
        return f"E{n[0]:02d}"
    days_used = {}

    def free_day(item, state, lo=None, hi=None):
        for _ in range(40):
            d = rand_day(rng, lo or M["period"][0], hi or M["period"][1])
            if (item, d) not in days_used:
                days_used[(item, d)] = 1
                return d
        return None
    for it in M["items"]:
        iid = it["id"]
        cd = free_day(iid, "holder", M["period"][0], S_(start + dt.timedelta(days=length // 5)))
        h = rng.choice(holders)
        M["entries"].append({"eid": None, "date": cd, "type": "create", "item": iid, "holder": h})
        cur = h
        nent = rng.randint(2, 3) if len(M["items"]) > 1 else rng.randint(2, 4)
        for _ in range(nent):
            r = rng.random()
            if it["track"] == "valid" and r < 0.45:
                d = free_day(iid, "renew", cd)
                if d:
                    M["entries"].append({"eid": None, "date": d, "type": "renew", "item": iid, "actor": None,
                                         "days": rng.choice([7, 10, 14, 15, 20, 21, 28, 30, 45, 60])})
            elif it["track"] == "status" and r < 0.45:
                d = free_day(iid, "status", cd)
                if d:
                    M["entries"].append({"eid": None, "date": d, "type": "status", "item": iid,
                                         "status": rng.choice(M["statuses"])["name"]})
            elif r < 0.6:
                d = free_day(iid, "holder", cd)
                if d:
                    M["entries"].append({"eid": None, "date": d, "type": "transfer", "item": iid, "actor": None,
                                         "to": rng.choice([x for x in holders])})
            elif r < 0.8:
                d = free_day(iid, "ev", cd)
                if d:
                    M["entries"].append({"eid": None, "date": d, "type": "report", "item": iid,
                                         "actor": rng.choice(holders + others), "risk": rng.choice(M["risks"])})
            else:
                d = free_day(iid, "ev", cd)
                if d:
                    M["entries"].append({"eid": None, "date": d, "type": "file", "item": iid,
                                         "actor": rng.choice(holders + others), "doc": rng.choice(M["docs"])})
    M["entries"].sort(key=lambda e: e["date"])
    for e in M["entries"]:
        e["eid"] = eid()
    fix_actors(M)
    M["_days"] = days_used
    return M, holders, others


def fix_actors(M):
    """Actors of renewals and transfers = the holder on that day (replay without corrections first)."""
    hold = {}
    for e in sorted(M["entries"], key=lambda e: (e["date"], e["eid"])):
        if e["type"] == "create":
            hold[e["item"]] = e["holder"]
        elif e["type"] == "transfer":
            e["actor"] = hold.get(e["item"])
            if e["to"] == e["actor"]:
                e["to"] = None
            hold[e["item"]] = e["to"] if e["to"] else e["actor"]
        elif e["type"] == "renew":
            e["actor"] = hold.get(e["item"])
    M["entries"] = [e for e in M["entries"] if not (e["type"] == "transfer" and e["to"] is None)]


def lookalike(main, ids, rng):
    pre, body = main.split("-", 1)
    for _ in range(20):
        b = list(body)
        i = rng.randrange(len(b) - 1)
        b[i], b[i + 1] = b[i + 1], b[i]
        cand = pre + "-" + "".join(b)
        if cand != main:
            return cand
    return next(x for x in ids if x != main)


def renumber(M):
    """Entry ids in listed date order (E01 ...); CORRECTION / VOID targets follow."""
    order = sorted(M["entries"], key=lambda e: (e["date"], e["eid"]))
    ren = {e["eid"]: f"E{i + 1:02d}" for i, e in enumerate(order)}
    for e in M["entries"]:
        e["eid"] = ren[e["eid"]]
        if e.get("target"):
            e["target"] = ren[e["target"]]
    M["entries"].sort(key=lambda e: e["eid"])


def month_range(day):
    d = D(day)
    lo = d.replace(day=1)
    nxt = (lo + dt.timedelta(days=32)).replace(day=1)
    return S_(lo), S_(nxt - dt.timedelta(days=1)), f"{MONTHS[d.month - 1]} {d.year}"
