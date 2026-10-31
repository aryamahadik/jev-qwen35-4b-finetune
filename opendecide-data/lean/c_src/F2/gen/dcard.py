"""S4 calendar and business-day cards: skeleton, clauses, row dates, LP, readings, document (holiday line, strip)."""
from __future__ import annotations

import datetime as dt
import random

from . import dateeval as DE, lex
from .common import date_str, NUM_WORDS
from .money import Reject

EVENTS = [("notice", "reply"), ("request", "decision"), ("order", "delivery"), ("complaint", "response"),
          ("inspection", "repair"), ("claim", "payment"), ("invoice", "payment"), ("application", "review"),
          ("booking", "confirmation"), ("referral", "assessment")]
WIN_KINDS = ["follow-up track", "lateness grade", "reminder stage", "escalation level", "handling path"]
WIN_SETS = [["prompt", "grace", "reminder", "escalated", "referred", "closed out"],
            ["on schedule", "slightly late", "late", "very late", "overdue", "lapsed"]]
FLAGS = ["holiday cover approved", "documents missing", "site closed", "priority case", "second request",
         "postal delivery", "translation needed", "remote site", "partial delivery", "manager review"]


def ordinal(n):
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


def build(card, pack, rng):
    from .mcard import Labels, COUNTS
    L = Labels()
    s = {}
    evt, act = rng.choice(EVENTS)
    s["evt_w"], s["act_w"] = evt, act
    s["evt"] = L(f"{evt} date")
    s["act"] = L(f"{act} date")
    sch = card["schema"]
    kind = card.get("rule_kind") or rng.choice(["cal", "cal", "bday", "bday", "month"])
    if sch == "CH-C":
        kind = "count"
    s["kind"] = kind
    s["N"] = rng.randint(3, 10) if kind == "bday" else rng.choice([5, 7, 10, 14, 15, 20, 21, 28, 30])
    s["M"] = rng.choice([2, 3, 4, 6])
    s["date_form"] = rng.choice(["gb_long", "us_long", "iso"])
    sem = {}
    s["d6a"] = False
    if kind == "cal":
        sem["D4"] = card.get("d4") or "a"
        if rng.random() < 0.6:
            sem["D7"] = card.get("d7") or rng.choice(["fwd", "back", "none"])
    elif kind == "bday":
        sem["D7"] = card.get("d7") or rng.choice(["fwd", "back", "none"])
    elif kind == "month":
        if rng.random() < 0.6:
            sem["D7"] = card.get("d7") or rng.choice(["fwd", "back", "none"])
    if kind == "count":
        s["ckind"] = rng.choice(["cal", "bus"])
        s["cnt"] = L(rng.choice(["days taken", "turnaround", "elapsed period", "response time"]))
        if s["ckind"] == "cal":
            sem["D5"] = rng.choice(["excl", "both"])
        else:
            sem["D14"] = rng.choice(["after", "both"])
            s["d6a"] = True
    if "D7" in sem or kind == "bday":
        s["d6a"] = True
    ext = None
    if kind != "count" and (card["world"] == "open" or card.get("force_ext") or (not card.get("no_ext") and rng.random() < 0.6)):
        flags = list(FLAGS)
        rng.shuffle(flags)
        conn = rng.choice(["O2", "O2", "UN1"]) if card["world"] == "closed" else "O2"
        join = rng.choice(["single", "single", "and", "or1"]) if card["world"] == "closed" else rng.choice(["and", "or1"])
        conds = []
        for ci in range(1 if join == "single" else 2):
            kc = rng.choice(["flag", "flag", "cat"]) if ci == 0 or "cat" not in [c["ftype"] for c in conds] else "flag"
            if kc == "cat":
                cname, cvals = pack["cat"]
                cvals = [v for v in cvals if " and " not in v and " or " not in v][:5]
                conds.append({"f": L(cname), "op": "is", "v": rng.choice(cvals), "ftype": "cat", "dom": cvals})
            else:
                conds.append({"f": L(flags.pop()), "op": "is", "v": "yes", "ftype": "flag", "dom": ["yes", "no"]})
        unit = "bday" if (kind == "bday" and rng.random() < 0.6) else "cal"
        if card.get("ext_unit"):
            unit = card["ext_unit"]
        ext = {"K": card.get("ext_k") or (rng.randint(2, 7) if unit == "bday" else rng.choice([3, 5, 7, 10, 14])), "unit": unit,
               "conn": conn, "join": join, "conds": conds}
        sem["D12"] = card.get("d12") or "pre"
        if unit == "bday":
            s["d6a"] = True
    s["ext"] = ext
    if sch == "CH-O":
        n = rng.randint(3, 5)
        ks = sorted(rng.sample(range(1, 30), n - 2))
        edges = [0] + ks
        names = rng.choice(WIN_SETS)[:n]
        wins = []
        for i in range(n):
            wins.append({"name": names[i].capitalize(), "lo": edges[i - 1] if i > 0 else None,
                         "hi": edges[i] if i < n - 1 else None})
        s["windows"] = wins
        s["wkind"] = rng.choice(WIN_KINDS)
        sem["B1w"] = card.get("b1") or rng.choice(["upper", "lower"])
    if ext is not None and "D7" not in sem:
        # repair r1.1 (G5 flag, confirmed against D12's text): D12 ends "then apply the roll rule once", so every
        # card with an extension states a roll rule (D7, any of its three forms; D7 always comes with D6a, A13)
        sem["D7"] = card.get("d7") or rng.choice(["fwd", "back", "none"])
        s["d6a"] = True
    s["sem"] = sem
    card["d"] = s
    card["shown"] = set(sem)
    card["omitted"] = []
    return card


def dstr(card, d, wd=True):
    return date_str(d, card["d"]["date_form"], weekday=wd)


def gate_text(ext):
    from .mcard import cond_text, gate_text as gt
    conds = [cond_text(c) for c in ext["conds"]]
    j = ext["join"]
    c = conds[0] if j == "single" else lex.fill({"and": lex.J_AND, "or1": lex.J_OR1, "or2": lex.J_OR2}[j],
                                                c1=conds[0], c2=conds[1])
    return lex.fill(lex.D12_UNLESS if ext["conn"] == "UN1" else lex.D12_IF, c=c)


def clauses(card, sem, shown, world):
    s = card["d"]
    out = [("Scope", "W0", lex.W0)]
    if world == "closed":
        out.append(("Record", "W1", lex.W1))
    else:
        out.append(("Record", "W2", lex.fill(lex.W2, u="day", nei=card["nei"])))
        if s["ext"]:
            for c in s["ext"]["conds"]:
                if c["ftype"] == "cat":
                    out.append(("Categories", "CATLIST", lex.fill(lex.CATLIST, f=c["f"], list=", ".join(c["dom"]))))
    out.append(("Dates", "D1", lex.D1))
    k = s["kind"]
    a, e = s["act_w"], s["evt_w"]
    if k == "cal":
        if sem.get("D4", "a") == "a":
            out.append(("Deadline", "D4", lex.fill(lex.D4A, act=a, N=s["N"], evt=e)))
        else:
            out.append(("Deadline", "D4", lex.fill(lex.D4B, act=a, Nth=ordinal(s["N"]), evt=e)))
    elif k == "bday":
        out.append(("Deadline", "D6B", lex.fill(lex.D6B, act=a, N=s["N"], Nth=ordinal(s["N"]), evt=e)))
    elif k == "month":
        out.append(("Deadline", "D8", lex.fill(lex.D8_RULE, act=a, M=s["M"], evt=e) + " " + lex.fill(lex.D8, M=s["M"])))
    elif k == "count":
        if s["ckind"] == "cal":
            out.append(("Count", "D5", lex.fill(lex.CNT_CAL, cnt=s["cnt"], d1=s["evt"], d2=s["act"]) + " " +
                        lex.fill(lex.D5[sem["D5"]], d1=s["evt"], d2=s["act"])))
        else:
            out.append(("Count", "D14", lex.fill(lex.CNT_BUS, cnt=s["cnt"], d1=s["evt"], d2=s["act"]) + " " +
                        lex.fill(lex.D14[sem["D14"]], d1=s["evt"], d2=s["act"])))
    if s["d6a"]:
        out.append(("Business days", "D6A", lex.D6A))
    if "D7" in sem:
        out.append(("Roll rule", "D7", lex.fill(lex.D7[sem["D7"]], dl="last allowed day")))
    if s["ext"]:
        ext = s["ext"]
        unit = "business days" if ext["unit"] == "bday" else "calendar days"
        out.append(("Extension", "D12", lex.fill(lex.D12[sem.get("D12", "pre")], G=gate_text(ext), K=ext["K"], unit=unit)))
    if k != "count" and card["schema"] in ("YN-D", "CL", "CH-O"):
        out.append(("On time", "D15", lex.fill(lex.D15, act=a, evt=e)))
    if card["schema"] == "CH-O":
        out.append(("Windows", "D16", lex.D16))
        out.append(("Window edges", "B1W", lex.B1_DATE[sem.get("B1w", "upper")]))
    return out


def window_items(card, sem):
    s = card["d"]
    b1 = sem.get("B1w", "upper")
    items = []
    n = len(s["windows"])

    def edge(k):
        return lex.WIN_EDGE0 if k == 0 else lex.fill(lex.WIN_EDGEK, k=k)
    for i, w in enumerate(s["windows"]):
        pos = "low" if i == 0 else "high" if i == n - 1 else "mid"
        kw = {}
        if w.get("lo") is not None:
            kw["a"] = edge(w["lo"])
        if w.get("hi") is not None:
            kw["b"] = edge(w["hi"])
        items.append(lex.fill(lex.OUT_ITEM, name=w["name"], range=lex.fill(lex.WIN_RANGE[b1][pos], **kw)))
    return items


# ----------------------------------------------------------------------------------------------------------------- dates

def rand_date(rng, y0=2031, y1=2048):
    start = dt.date(y0, 1, 1).toordinal()
    end = dt.date(y1, 12, 31).toordinal()
    return dt.date.fromordinal(rng.randint(start, end))


def draw(card, rng):
    """Event date, holidays (weekdays only, 0-3 listed; non-deep: <= 1 inside a business-day window), facts."""
    s = card["d"]
    ev = rand_date(rng)
    if s["kind"] == "month" and rng.random() < 0.3:
        import calendar as C
        last = C.monthrange(ev.year, ev.month)[1]
        ev = dt.date(ev.year, ev.month, rng.choice([last, last - 1, 29 if last >= 29 else last, 31 if last == 31 else last]))
    facts = {}
    if s["ext"]:
        for c in s["ext"]["conds"]:
            facts.setdefault(c["f"], rng.choice(c["dom"]))
    hol = []
    if s["d6a"]:
        nh = rng.choice([0, 0, 1, 1, 2, 3])
        tries = 0
        while len(hol) < nh and tries < 50:
            tries += 1
            h = ev + dt.timedelta(days=rng.randint(-5, 40))
            if h.weekday() < 5 and h not in hol and h != ev:
                hol.append(h)
        hol.sort()
    return {"ev": ev, "hol": hol, "facts": facts}


def make_lp(card, d, dates, q, sem, facts=None):
    s = card["d"]
    rule = {"kind": s["kind"], "N": s["N"], "M": s["M"]}
    if s["ext"]:
        e = s["ext"]
        rule["ext"] = {"K": e["K"], "unit": e["unit"], "conn": e["conn"], "join": e["join"],
                       "conds": [{"f": c["f"], "op": c["op"], "v": c["v"]} for c in e["conds"]]}
    else:
        rule["ext"] = None
    LP = {"eng": "date", "world": card["world"], "dates": dict(dates), "facts": dict(facts if facts is not None else d["facts"]),
          "holidays": list(d["hol"]), "rule": rule, "sem": {k: v for k, v in sem.items()}, "evt": s["evt"],
          "act": s["act"], "q": q, "d6a": s["d6a"]}
    if s["kind"] == "count":
        LP["count"] = {"kind": s["ckind"], "d1": s["evt"], "d2": s["act"]}
    if card["schema"] == "CH-O" or q.get("kind") == "window":
        LP["windows"] = [dict(w) for w in s["windows"]]
    if card["world"] == "open" and s["ext"]:
        LP["cats"] = {c["f"]: list(c["dom"]) for c in s["ext"]["conds"]}
    return LP


def alt_readings(LP, shown):
    sem = LP["sem"]
    out = []
    r = LP["rule"]
    if "D4" in sem:
        out.append(("E-alt:D4", {"sem": {"D4": "b" if sem["D4"] == "a" else "a"}}))
    if "D7" in sem:
        for f in ("fwd", "back", "none"):
            if f != sem["D7"]:
                out.append((f"E-alt:D7:{f}", {"sem": {"D7": f}}))
    if r["kind"] == "bday":
        out.append(("E-bday", {"err": "E-bday"}))
    if LP.get("holidays"):
        out.append(("E-hol", {"err": "E-hol"}))
    if r.get("ext"):
        out.append(("E-ext", {"err": "E-ext"}))
        out.append(("E-alt:D12", {"sem": {"D12": "post" if sem.get("D12", "pre") == "pre" else "pre"}}))
    if r["kind"] == "month":
        out.append(("E-eom:overflow", {"err": "E-eom:overflow"}))
        out.append(("E-eom:keep", {"err": "E-eom:keep"}))
    if "D5" in sem:
        out.append(("E-alt:D5", {"sem": {"D5": "both" if sem["D5"] == "excl" else "excl"}}))
    if "D14" in sem:
        out.append(("E-alt:D14", {"sem": {"D14": "both" if sem["D14"] == "after" else "after"}}))
        out.append(("E-bday", {"err": "E-bday"}))
    if "B1w" in sem:
        out.append(("E-alt:B1", {"sem": {"B1w": "lower" if sem["B1w"] == "upper" else "upper"}}))
    return out


def strip_dates(card, LP, extra=()):
    """Calendar strip (1.1): consecutive dates covering every relevant date with 3-10 day margins, <= 45 dates."""
    rng = random.Random(str(sorted(str(x) for x in LP["dates"].values())))
    rel = list(LP["dates"].values()) + list(LP.get("holidays", [])) + list(extra)
    lo, hi = min(rel), max(rel)
    lo -= dt.timedelta(days=rng.randint(3, 10))
    hi += dt.timedelta(days=rng.randint(3, 10))
    n = (hi - lo).days + 1
    if n > 45:
        ev = LP["dates"][LP["evt"]]
        rel2 = [x for x in rel if x != ev]
        lo, hi = min(rel2) - dt.timedelta(days=rng.randint(3, 10)), max(rel2) + dt.timedelta(days=rng.randint(3, 10))
        n = (hi - lo).days + 1
        if n > 45:
            raise Reject("strip too long")
    return [lo + dt.timedelta(days=i) for i in range(n)]


def needs_strip(card, LP, relevant):
    s = card["d"]
    if s["d6a"]:
        return True
    if not relevant:
        return False
    span = (max(relevant) - min(relevant)).days
    return span > 14 or len({(x.year, x.month) for x in relevant}) > 1
