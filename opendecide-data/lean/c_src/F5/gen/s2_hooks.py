"""S2 hooks: event-log bases (event-in-range claims and validity states), cue cores, card constants."""
from __future__ import annotations

import copy
import datetime as dt

from . import s2
from .forms import Core, NOT

SAMPLER = "S2"
VALID_CUES = ["failed to", "neglected to", "omitted to"]

RANGE_FORMS = {  # name: (phrase, k, families, lneg)
    "on_or_before": ("on or before {D}", 0), "by": ("by {D}", 0), "before": ("before {D}", 0),
    "after": ("after {D}", 0), "on_or_after": ("on or after {D}", 0), "between": ("between {D1} and {D2}", 0),
    "from_to": ("from {D1} to {D2}", 0), "in_month": ("in {M}", 0), "on": ("on {D}", 0),
    "through": ("{D1} through {D2}", 0), "within": ("within {N} days after {D}", 0),
    "no_later": ("no later than {D}", 1), "not_after": ("not after {D}", 1), "no_earlier": ("no earlier than {D}", 1),
    "not_before": ("not before {D}", 1)}
EQUIV_NEG = {"on_or_before": ["no_later", "not_after"], "by": ["no_later", "not_after"],
             "on_or_after": ["no_earlier", "not_before"]}


def dd(s, n):
    return (dt.date.fromisoformat(s) + dt.timedelta(days=n)).isoformat()


def range_lohi(form, D=None, D1=None, D2=None):
    if form == "within":
        return dd(D, 1), dd(D, int(D1))
    if form in ("on_or_before", "by", "no_later", "not_after"):
        return None, D
    if form == "before":
        return None, dd(D, -1)
    if form == "after":
        return dd(D, 1), None
    if form in ("on_or_after", "no_earlier", "not_before"):
        return D, None
    if form in ("between", "from_to", "through"):
        return D1, D2
    if form == "on":
        return D, D
    if form == "in_month":
        lo, hi, _ = s2.month_range(D)
        return lo, hi
    raise ValueError(form)


def range_text(form, D=None, D1=None, D2=None):
    ph = RANGE_FORMS[form][0]
    if form == "within":
        return ph.format(N=D1, D=D)
    if form == "in_month":
        return ph.format(M=s2.month_range(D)[2])
    return ph.format(D=D, D1=D1, D2=D2)


def card_setup(card):
    pv = card["pack"]
    rng = __import__("random").Random(card["seed"])
    ents = [e for e in pv["ents"] if len(e["ids"]) >= 12]
    card["ent"] = rng.choice(ents)
    card["S"] = rng.choice(pv["sources"])
    card["people"] = list(pv["people"])
    sts = [s for s in pv["statuses"]]
    rng.shuffle(sts)
    card["statuses"] = sts[:4] if len(sts) >= 3 else [{"name": x, "tag": None} for x in ("opened", "on hold",
                                                                                           "closed")]
    docs = [d for d in pv["docs"] if d != card["ent"]["noun"] and card["ent"]["noun"] not in d]
    rng.shuffle(docs)
    card["docs"] = docs[:3]
    card["doc_tags"] = {d: pv["doc_tags"].get(d, "good") for d in card["docs"]}
    risks = list(pv["risks"]) or ["damage report"]
    rng.shuffle(risks)
    card["risks"] = risks[:2]
    card["window"] = pv["window"]
    # card constant (shared by antithetic partners): items tracked by renewals only, or also by status entries
    card["track"] = "status" if card["pair_index"] % 2 else "valid"
    card["adjs"] = []
    card["negs"] = {}
    return card


def plan_slot(card, rng, s):
    kind = rng.choices(["ev_renew", "ev_report", "ev_file", "valid"], [32, 26, 22, 20])[0]
    closed_both = card["world"] == "closed" and card["partner"]["world"] == "closed"
    if kind == "valid" and (s["pair"] is not None or not closed_both or (s["vk"] >= 1 and rng.random() < 0.5)):
        kind = "ev_renew"
    if kind.startswith("ev") and s["vk"] == 0:
        s["vk"] = 1
    depth = rng.choices([1, 2, 3], [64, 33, 3])[0]
    if kind.startswith("ev") and depth == 3:
        depth = 2
    return {"kind": kind, "depth": depth}


def slot_ctx(card, slot, rng):
    return {}


def solve(M, lfs):
    return s2.solve_a(M, lfs)


def decisive_depth(M, base):
    """1 + CORRECTION / VOID links followed from the decisive entry (section 5, S2)."""
    links = {}
    for e in M["entries"]:
        if e["type"] in ("correction", "void"):
            links.setdefault(e["target"], []).append(e)
    rem = s2.resolve(M)

    def chain(eid):
        n = 0
        for l in links.get(eid, []):
            n = max(n, 1 + chain(l["eid"]))
        return n
    if base["kind"] == "valid":
        last = None
        for e in rem:
            if e.get("item") == base["item"] and e["type"] == "renew" and e["date"] <= base["day"]:
                last = e
        cands = [last["eid"]] if last else []
        # a voided renewal on or before the day is decisive too
        cands += [e["eid"] for e in M["entries"] if e["type"] == "renew" and e.get("item") == base["item"]
                  and e["date"] <= base["day"] and e["eid"] in links]
        return 1 + max([chain(x) for x in cands] or [0])
    kind, actor, item, lo, hi = base["kind_ev"], base["actor"], base["item"], base["lo"], base["hi"]
    rawk = kind.split(":")[0]
    cands = [e["eid"] for e in M["entries"] if e["type"] == rawk and e.get("actor") == actor and e["item"] == item
             and s2.in_range(e["date"], lo, hi)]
    return 1 + max([chain(x) for x in cands] or [0])


def add_links(M, rng, want):
    """Add CORRECTION / VOID entries (by S) to reach a decisive-link depth; distractor links elsewhere."""
    if want <= 1 and rng.random() < 0.5:
        return
    rem_ids = [e for e in M["entries"] if e["type"] in ("renew", "report", "file", "transfer", "status")]
    if not rem_ids:
        return
    nxt = 0
    for _ in range(rng.choice([1, 1, 2])):
        e = rng.choice(rem_ids)
        nxt += 1
        later = s2.rand_day(rng, e["date"], M["period"][1])
        if e["type"] == "renew" and rng.random() < 0.6:
            M["entries"].append({"eid": f"L{nxt:02d}", "date": later, "type": "correction", "target": e["eid"],
                                 "field": "days", "value": rng.choice([7, 14, 21, 30, 45, 60])})
        elif e["type"] == "status" and rng.random() < 0.6 and M.get("track_ok_status", True):
            M["entries"].append({"eid": f"L{nxt:02d}", "date": later, "type": "correction", "target": e["eid"],
                                 "field": "status", "value": rng.choice(M["statuses"])["name"]})
        else:
            M["entries"].append({"eid": f"L{nxt:02d}", "date": later, "type": "void", "target": e["eid"]})
    # each entry named by at most one CORRECTION or VOID
    seen = set()
    keep = []
    for e in M["entries"]:
        if e["type"] in ("correction", "void"):
            if e["target"] in seen:
                continue
            seen.add(e["target"])
        keep.append(e)
    M["entries"] = keep
    if want >= 3:
        cors = [e for e in M["entries"] if e["type"] == "correction" and e["eid"] not in seen]
        if cors:
            c = rng.choice(cors)
            nxt += 1
            M["entries"].append({"eid": f"L{nxt:02d}", "date": s2.rand_day(rng, c["date"], M["period"][1]),
                                 "type": "void", "target": c["eid"]})


def build_structure(card, slot, rng):
    kind = slot["kind"]
    M, holders, others = s2.sample(rng, card, kind, slot["depth"], card["world"])
    M.pop("_days", None)
    add_links(M, rng, slot["depth"])
    try:
        rem = s2.resolve(M)
        s2.check(M, rem)
    except (ValueError, KeyError, StopIteration):
        return None
    main = M["items"][0]["id"]
    item = f"{M['items'][0]['noun']} {main}"
    base = {"item": main}
    if kind == "valid":
        rens = sorted(e["date"] for e in rem if e["type"] == "renew" and e.get("item") == main)
        if not rens:
            return None
        day = s2.rand_day(rng, rens[0], M["period"][1])
        P = ["valid", item, day]
        base.update({"kind": "valid", "day": day})
        if card["world"] == "open":
            v = s2.valid_on(rem, main, day)
            M["entries"].append({"eid": "Z99", "date": day, "type": "asof", "item": main, "state": "valid",
                                 "day": day, "value": v})
    else:
        if kind == "ev_renew":
            kev = "renew"
        elif kind == "ev_file":
            fil = [e for e in rem if e["type"] == "file" and e.get("item") == main and
                   card["doc_tags"].get(e["doc"], "good") == slot["tag"]]
            if not fil:
                return None
            kev = "file:" + rng.choice(fil)["doc"]
        else:
            reps = [e for e in rem if e["type"] == "report" and e.get("item") == main]
            if not reps:
                return None
            kev = "report:" + rng.choice(reps)["risk"]
        evs_all = s2.events(rem, kev, None, main)
        if not evs_all:
            return None
        actor = rng.choice(evs_all)["actor"]
        evs = [e["date"] for e in s2.events(rem, kev, actor, main)]
        r = pick_range(rng, M, evs, slot["v"])
        if r is None:
            return None
        form, Dx, D1, D2 = r
        lo, hi = range_lohi(form, Dx, D1, D2)
        P = ["ev", kev, actor, item, lo, hi]
        base.update({"kind": "ev", "kind_ev": kev, "actor": actor, "lo": lo, "hi": hi, "form": form, "D": Dx,
                     "D1": D1, "D2": D2, "item_txt": item,
                     "tag": card["doc_tags"].get(kev[5:], "good") if kev.startswith("file:") else
                     ("good" if kev == "renew" else "bad")})
        if card["world"] == "open":
            alo, ahi = lo or M["period"][0], hi or M["period"][1]
            if not any(s2.in_range(d, lo, hi) for d in evs):
                M["entries"].append({"eid": "Z98", "date": M["period"][1], "type": "noev", "kind": kev,
                                     "actor": actor, "item": main, "lo": alo, "hi": ahi})
            else:
                # repair r2 (G7 matched twin): a v(P) = 1 open base carries a true, non-decisive "No ... took place
                # from ... to ..." statement of the same shape (same event kind, item and asked window, another
                # actor with no such event in it), so the statement's presence says nothing about the label
                others = [p for p in card["people"] if p != actor and
                          not any(s2.in_range(e["date"], alo, ahi) for e in s2.events(rem, kev, p, main))]
                if not others:
                    return None
                M["entries"].append({"eid": "Z98", "date": M["period"][1], "type": "noev", "kind": kev,
                                     "actor": rng.choice(others), "item": main, "lo": alo, "hi": ahi})
            # C3 "by D" needs the period start through D decided
            if form in ("on_or_before", "by") and not any(s2.in_range(d, None, hi) for d in evs):
                pass
    add_extras(M, rng, card, base)
    if base["kind"] == "ev" and rng.random() < 0.95:
        # a claim by another party that restates the asked clause verbatim (SEM-20: only a claim; verbatim-overlap
        # control F5-R2-20), with stated / denied drawn independently of the label
        party = rng.choice([p for p in card["people"] if p != base["actor"]])
        M["entries"].append({"eid": "Z97", "date": s2.rand_day(rng, *M["period"]), "type": "notice", "party": party,
                             "verb": rng.choice(["stated", "denied"]), "item": None,
                             "claim": {"actor": base["actor"], "kind": base["kind_ev"], "item": main,
                                       "range": range_text(base["form"], base["D"], base["D1"], base["D2"])}})
    s2.renumber(M)
    for e in M["entries"]:
        if e["type"] == "asof" and e.get("item") == main:
            pass
    M["base"] = base
    try:
        (v,) = s2.solve_a(M, [map_item(P, M)])
    except (ValueError, KeyError, AssertionError):
        return None
    d = decisive_depth(M, base)
    if d != slot["depth"]:
        return None
    return M, map_item(P, M), {"depth": d}


def map_item(P, M):
    return P


def pick_range(rng, M, evs, v):
    """A date-range form and boundaries with every listed event of the asked kind on one side of each boundary
    (F5-R4-02); v = whether the events fall in the range."""
    evs = sorted(evs)
    ps, pe = M["period"]
    forms = ["on_or_before", "by", "before", "after", "on_or_after", "between", "from_to", "in_month", "on", "through",
             "within"]
    rng.shuffle(forms)
    for form in forms:
        for _ in range(6):
            if form in ("on_or_before", "by"):
                if v:
                    Dx = evs[-1] if rng.random() < 0.3 else dd(evs[-1], rng.randint(1, 9))
                else:
                    Dx = dd(evs[0], -1) if rng.random() < 0.3 else dd(evs[0], -rng.randint(2, 9))
                D1 = D2 = None
            elif form == "before":
                Dx = (dd(evs[-1], 1) if rng.random() < 0.3 else dd(evs[-1], rng.randint(2, 9))) if v else \
                    (evs[0] if rng.random() < 0.3 else dd(evs[0], -rng.randint(1, 9)))
                D1 = D2 = None
            elif form == "on_or_after":
                Dx = (evs[0] if rng.random() < 0.3 else dd(evs[0], -rng.randint(1, 9))) if v else \
                    (dd(evs[-1], 1) if rng.random() < 0.3 else dd(evs[-1], rng.randint(2, 9)))
                D1 = D2 = None
            elif form == "after":
                Dx = (dd(evs[0], -1) if rng.random() < 0.3 else dd(evs[0], -rng.randint(2, 9))) if v else \
                    (evs[-1] if rng.random() < 0.3 else dd(evs[-1], rng.randint(1, 9)))
                D1 = D2 = None
            elif form == "within":
                if v:
                    Dx = dd(evs[0], -rng.randint(1, 5))
                    span = (dt.date.fromisoformat(evs[-1]) - dt.date.fromisoformat(Dx)).days
                    D1 = str(span + rng.choice([0, 0, 1, 3]))
                else:
                    Dx = dd(evs[-1], rng.randint(0, 6))
                    D1 = str(rng.randint(3, 20))
                D2 = None
            elif form in ("between", "from_to", "through"):
                if v:
                    D1 = evs[0] if rng.random() < 0.3 else dd(evs[0], -rng.randint(1, 9))
                    D2 = evs[-1] if rng.random() < 0.3 else dd(evs[-1], rng.randint(1, 9))
                else:
                    if rng.random() < 0.5:
                        D2 = dd(evs[0], -rng.randint(1, 5))
                        D1 = dd(D2, -rng.randint(3, 20))
                    else:
                        D1 = dd(evs[-1], rng.randint(1, 5))
                        D2 = dd(D1, rng.randint(3, 20))
                Dx = None
            elif form == "in_month":
                Dx = evs[0] if v else dd(evs[0], rng.choice([-40, -35, 35, 40]))
                lo, hi, _ = s2.month_range(Dx)
                D1 = D2 = None
            else:  # on
                if len(evs) != 1:
                    break
                Dx = evs[0] if v else dd(evs[0], rng.choice([-3, -1, 1, 2]))
                D1 = D2 = None
            lo, hi = range_lohi(form, Dx, D1, D2)
            for b in (lo, hi):
                if b is not None and not (ps <= b <= pe):
                    break
            else:
                ins = [s2.in_range(d, lo, hi) for d in evs]
                if all(ins) if v else not any(ins):
                    return form, Dx, D1, D2
    return None


def add_extras(M, rng, card, base):
    """Distractor and text-side cue entries: failure / refusal cues (C3 / C4, true by assertion), claims by other
    parties (C7 text side, no effect)."""
    rem = s2.resolve(M)
    people = card["people"]
    n = 0
    if rng.random() < 0.35:
        for _ in range(4):
            p = rng.choice(people)
            doc = rng.choice(M["docs"])
            it = rng.choice(M["items"])["id"]
            kind = "file:" + doc
            if not [x for x in M["entries"] if x["type"] == "file" and x.get("actor") == p and x.get("item") == it
                    and x["doc"] == doc]:
                cue = rng.choice(s2.FAIL_CUES + s2.REFUSE_CUES)
                n += 1
                M["entries"].append({"eid": f"X{n:02d}", "date": s2.rand_day(rng, *M["period"]), "type": "fail",
                                     "item": it, "actor": p, "kind": kind, "cue": cue})
                break
    if rng.random() < 0.2:
        ev = [x for x in rem if x["type"] in ("renew", "report", "file")]
        party = rng.choice(people)
        if ev:
            x = rng.choice(ev)
            kind = "renew" if x["type"] == "renew" else ("report:" + x["risk"] if x["type"] == "report" else
                                                         "file:" + x["doc"])
            n += 1
            M["entries"].append({"eid": f"X{n:02d}", "date": s2.rand_day(rng, x["date"], M["period"][1]),
                                 "type": "notice", "party": party, "verb": rng.choice(["stated", "denied"]),
                                 "claim": {"actor": x["actor"], "kind": kind, "item": x["item"]}, "item": None})


def ev_cores(M, base):
    """Event-atom cores: identity (each range phrase), C1, C3 (only for 'on or before / by D' bases), C10 negated date
    words (equivalent range), C16 decoy with a true event, C15 never (whole period)."""
    kev, actor, item = base["kind_ev"], base["actor"], base["item_txt"]
    lo, hi, form = base["lo"], base["hi"], base["form"]
    rt = range_text(form, base["D"], base["D1"], base["D2"])
    P = ["ev", kev, actor, item, lo, hi]
    vp_past = s2.event_vp(kev, item, "past")
    vp_base = s2.event_vp(kev, item, "base")
    out = [Core(f"EV.pos.{form}", (), f"{actor} {vp_past} {rt}", f"Did {actor} {vp_base} {rt}", P, 0, "up"),
           Core(f"C1.ev.{form}", ("C1",), f"{actor} did not {vp_base} {rt}", None, NOT(P), 1, "down", nd=True,
                lneg=("not",))]
    if kev == "renew":
        out.append(Core(f"EV.pas.{form}", (), f"{item} was renewed by {actor} {rt}",
                        f"Was {item} renewed by {actor} {rt}", P, 0, "up"))
    if form in ("on_or_before", "by"):
        for cue in ("failed to", "neglected to", "omitted to"):
            t = cue.split()[0]
            lem = {"failed": "fail", "neglected": "neglect", "omitted": "omit"}[t]
            out.append(Core(f"C3.{t}", ("C3",), f"{actor} {cue} {vp_base} by {base['D']}",
                            f"Did {actor} {lem} to {vp_base} by {base['D']}", NOT(P), 1, "down", nd=True,
                            lneg=(lem + " to",)))
        out.append(Core("C3.dnmt", ("C3",), f"{actor} did not manage to {vp_base} by {base['D']}", None, NOT(P), 1,
                        "down", nd=True, lneg=("did not manage to",)))
        out.append(Core("C1C3.failed", ("C1", "C3"), f"{actor} did not fail to {vp_base} by {base['D']}", None,
                        NOT(NOT(P)), 2, "up", nd=True, lneg=("not", "fail to")))
    for f2 in EQUIV_NEG.get(form, []):
        rt2 = range_text(f2, base["D"])
        out.append(Core(f"C10.{f2}", ("C10",), f"{actor} {vp_past} {rt2}", None, P, 1, "up", lneg=(f2,),
                        rel="negdate"))
    # a negated date word on the complementary side (= not-P under the one-side assertion)
    comp = {"on_or_before": ("no_earlier", 1), "by": ("no_earlier", 1), "before": ("not_before", 0),
            "on_or_after": ("not_after", -1), "after": ("no_later", 0)}
    if form in comp and base["D"]:
        f2, sh = comp[form]
        D2 = dd(base["D"], sh)
        lo2, hi2 = range_lohi(f2, D2)
        out.append(Core(f"C10c.{f2}", ("C10",), f"{actor} {vp_past} {range_text(f2, D2)}", None,
                        ["ev", kev, actor, item, lo2, hi2], 1, "up", lneg=(f2,), rel="other",
                        ptag=base.get("tag")))
    return out


def cores(card, M, P, rng, slot):
    base = M["base"]
    out = {}
    if base["kind"] == "ev":
        for c in ev_cores(M, base):
            out[c.tid] = c
        rem = s2.resolve(M)
        # decoy with a true event of another kind on the same item (C16)
        tr = [e for e in rem if e["type"] in ("file", "report", "renew") and e.get("item") == base["item"]
              and not (e["type"] == base["kind_ev"].split(":")[0])]
        if tr:
            e = tr[0]
            k2 = "renew" if e["type"] == "renew" else ("report:" + e["risk"] if e["type"] == "report" else
                                                       "file:" + e["doc"])
            B = ["ev", k2, e["actor"], base["item_txt"], None, None]
            if e["actor"] == base["actor"]:
                rt = range_text(base["form"], base["D"], base["D1"], base["D2"])
                c = Core(f"C16.ev.{base['form']}", ("C16",), f"{base['actor']} not only {s2.event_vp(base['kind_ev'], base['item_txt'], 'past')} "
                                             f"{rt} but also {s2.event_vp(k2, base['item_txt'], 'past')}", None,
                         ["and", P, B], 0, "up", lneg=("not only",), rel="conn")
                out[c.tid] = c
        never = Core("C15.never", ("C15",), f"{base['actor']} never {s2.event_vp(base['kind_ev'], base['item_txt'], 'past')}",
                     None, NOT(["ev", base["kind_ev"], base["actor"], base["item_txt"], None, None]), 1, "down",
                     lneg=("never",), rel="other", ptag=base.get("tag"))
        out[never.tid] = never
    else:
        item, day = P[1], P[2]
        out["VAL.pos"] = Core("VAL.pos", (), f"{item} is valid as of {day}", f"Is {item} valid as of {day}", P, 0,
                              "up")
        out["C1.val"] = Core("C1.val", ("C1",), f"{item} is not valid as of {day}", None, NOT(P), 1, "down", nd=True,
                             lneg=("not",))
        rem0 = s2.resolve(M)
        earlier = any(s2.valid_on(rem0, base["item"], dd(M["period"][0], i)) for i in range(
            (dt.date.fromisoformat(day) - dt.date.fromisoformat(M["period"][0])).days))
        if card["world"] == "closed" and earlier:
            st = Core("VAL.still", ("C15",), f"{item} is still valid as of {day}",
                      f"Is {item} still valid as of {day}", ["still", item, day], 0, "up", rel="still")
            out[st.tid] = st
        # other-atom implicative about renewing the item by the asked day (holder on that day)
        rem = s2.resolve(M)
        h = s2.holder_on(rem, base["item"], day)
        if h:
            Q = ["ev", "renew", h, item, None, day]
            for cue in ("failed to", "neglected to"):
                t = cue.split()[0]
                c = Core(f"C3o.{t}", ("C3",), f"{h} {cue} renew {item} by {day}",
                         f"Did {h} {'fail' if t == 'failed' else 'neglect'} to renew {item} by {day}", NOT(Q), 1,
                         "down", lneg=(cue.split()[0],), rel="other")
                c.ptag = "good"
                out[c.tid] = c
    return out


def is_v_core(card, c):
    if c.fam and not all(card["fams"].get(f, False) for f in c.fam):
        return False
    if c.rel in ("still", "negdate", "negdate_comp", "conn", "other"):
        return True
    return c.fam == ("C3",)


def nd_ok(card, c):
    return all(card["fams"].get(f, False) for f in c.fam)


def valid_structure(card, M, P):
    try:
        s2.check(M, s2.resolve(M))
    except ValueError:
        return False
    base = M["base"]
    if base["kind"] == "ev":
        rem = s2.resolve(M)
        evs = [e["date"] for e in s2.events(rem, base["kind_ev"], base["actor"], base["item"])]
        if not evs:
            return False
        ins = [s2.in_range(d, base["lo"], base["hi"]) for d in evs]
        if not (all(ins) or not any(ins)):
            return False
    return True


def tag_of(card, P, M):
    if P[0] == "valid":
        return "good"
    if P[0] == "ev":
        if P[1].startswith("file:"):
            return card["doc_tags"].get(P[1][5:], "good")
        return "good" if P[1] == "renew" else "bad"
    return None


def perturb(M, rng):
    """Contrast-pair change (closed list, S2): one entry's value field, one entry's date moved across an asked
    boundary, or one entry removed that no CORRECTION or VOID names."""
    out = []
    named = {e["target"] for e in M["entries"] if e["type"] in ("correction", "void")}
    base = M["base"]
    bounds = [b for b in (base.get("lo"), base.get("hi"), base.get("day")) if b]
    for e in M["entries"]:
        if e["type"] in ("renew", "report", "file", "status", "transfer", "create"):
            if e["eid"] not in named and e["type"] not in ("create",):
                M2 = copy.deepcopy(M)
                M2["entries"] = [x for x in M2["entries"] if x["eid"] != e["eid"]]
                out.append((f"remove {e['eid']}", M2))
            for b in bounds:
                for nd in (dd(b, -1), b, dd(b, 1)):
                    if nd != e["date"] and M["period"][0] <= nd <= M["period"][1]:
                        M2 = copy.deepcopy(M)
                        for x in M2["entries"]:
                            if x["eid"] == e["eid"]:
                                x["date"] = nd
                        out.append((f"date {e['eid']} -> {nd}", M2))
            if e["type"] == "renew":
                for nd in (7, 14, 30, 60):
                    if nd != e["days"]:
                        M2 = copy.deepcopy(M)
                        for x in M2["entries"]:
                            if x["eid"] == e["eid"]:
                                x["days"] = nd
                        out.append((f"days {e['eid']} -> {nd}", M2))
    rng.shuffle(out)
    return out


def doc(M, inert=None, attack=None):
    return s2.doc_ir(M, attack=attack)


def text_triggers(M):
    keys = {"SEM-01", "SEM-02" if M["world"] == "closed" else "SEM-03", "SEM-16", "SEM-20", "SEM-33", "SEM-27",
            "SEM-11", "SEM-12", "SEM-14"}
    if any(e["type"] == "status" or (e["type"] == "correction" and e["field"] == "status") for e in M["entries"]):
        keys.add("SEM-17")
    if any(e["type"] == "fail" for e in M["entries"]):
        keys.add("SEM-19")
    return keys


def full_keys(card):
    keys = {"SEM-01", "SEM-02" if card["world"] == "closed" else "SEM-03", "SEM-16", "SEM-20", "SEM-33", "SEM-27",
            "SEM-11", "SEM-12", "SEM-14", "SEM-19"}
    if card["track"] == "status":
        keys.add("SEM-17")
    if card["fams"].get("C15"):
        keys.add("SEM-26")
    if card["fams"].get("C16"):
        keys.add("SEM-28")
    return keys


def sem_params(card, M):
    p = {"etype": f"{card['ent']['noun']} and every person", "S": card["S"], "D_start": M["period"][0],
         "D_end": M["period"][1], "item": card["ent"]["noun"], "vs_form": "log"}
    p["value_sets"] = [("status", [s["name"] for s in card["statuses"]])]
    p["affixed"] = []
    return p


def affixed_used(M):
    return []


def t_txt(M):
    from .common import negc
    return sum(1 for e in M["entries"] if negc(s2.entry_text(M, e)).k_all > 0)


def fewshot(card, b):
    M = b["M"]
    n = card["ent"]["noun"]
    ids = [x for x in card["ent"]["ids"] if all(x != i["id"] for i in M["items"])]
    p1, p2 = card["people"][0], card["people"][1]
    d0, d1 = M["period"][0], dd(M["period"][0], 2)
    return [{"case": f"Log: {d0}: {s2.cap(n)} {ids[0]} was created for {p1}. {d1}: {p1} renewed {n} {ids[0]} for 30 "
                     f"days. Question: Is it true that {p1} did not renew {n} {ids[0]} on or before {d1}?",
             "answer": "No"},
            {"case": f"Log: {d0}: {s2.cap(n)} {ids[1]} was created for {p2}. {d1}: {p2} renewed {n} {ids[1]} for 14 "
                     f"days. Question: Is it false that {p2} renewed {n} {ids[1]} after {d0}?", "answer": "No"}]


def inverted_block(card, b):
    return None


T_BUCKETS = {"0": 0.3, "1": 0.55, "2+": 0.15}


def t_bucket(M):
    t = t_txt(M)
    return "2+" if t >= 2 else str(t)
