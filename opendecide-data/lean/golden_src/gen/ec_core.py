"""Case model and the primary resolver for gen_evidence_conflict.

A case is a set of dated documents about one attribute of one entity, a reconciliation rule, a date, and a question.

Documents (doc['kind']):
  stmt   definite report 'X is v' (in force from its own date until replaced)
  neg    definite negative report 'X is no longer v' (numbers / named values only)
  sched  scheduled change 'from <start>, X will be v'
  temp   temporary change 'from <start> through <end> (inclusive), X will be v'
  corr   correction of an earlier report by the SAME source: replaces its value over the same effective period
  retr   withdrawal of an earlier report by the SAME source: the report no longer counts (no value implied)
  other  a statement about a different attribute of the entity (irrelevant)
  inject an instruction or claimed answer addressed to the reader (data, never a report)
Report-like documents can also be speculative (mood 'hedge'), questions (mood 'ask') or about a confusable other
entity (ent 1): none of those count.

Rules: 'latest' (newest counted report wins), 'auth' (highest-ranked source with a counted report in effect wins; within
one source the newest wins), 'only' (only the listed sources count; newest of them wins).
Modes: 'known' (point = cut-off = D), 'hind' (point D, every document counts: later corrections/withdrawals apply),
'pk' (point D, cut-off K > D). A diff claim compares the value known at D2 with the value known at D.

Two readings of 'newest' are computed: A = latest publication, B = latest effective start (then publication). A case is
used only when both readings give the same answer at every point the question needs (no interpretation-dependent labels).
"""
from ec_domains import DOM

INF = 10 ** 13
T, F, N = "T", "F", "N"
REPORT_KINDS = ("stmt", "neg", "sched", "temp")
YESNO = ("supported", "refuted", "direct", "enough")
LETTERS = ["A", "B", "C", "D", "E", "F"]


def eligible(d):
    return d["kind"] in REPORT_KINDS and d["mood"] == "def" and d.get("ent", 0) == 0


def interval(d):
    if d["kind"] in ("stmt", "neg"):
        return d["pub"], INF
    if d["kind"] == "sched":
        return d["start"], INF
    return d["start"], d["end"]


def known_reports(case, cutoff):
    drop = case.get("drop")
    docs = [d for d in case["docs"] if d["id"] != drop]
    known = [d for d in docs if cutoff is None or d["pub"] <= cutoff]
    retr = {d["tgt"] for d in known if d["kind"] == "retr"}
    corr = {d["tgt"]: d for d in known if d["kind"] == "corr"}
    reps = []
    for d in known:
        if not eligible(d) or d["id"] in retr:
            continue
        s, e = interval(d)
        if d["id"] in corr:
            c = corr[d["id"]]
            reps.append({"sid": c["id"], "tid": d["id"], "src": d["src"], "pub": c["pub"], "start": s, "end": e,
                         "sig": ("pos", c["v"]), "kind": d["kind"]})
        else:
            reps.append({"sid": d["id"], "tid": d["id"], "src": d["src"], "pub": d["pub"], "start": s, "end": e,
                         "sig": ("neg" if d["kind"] == "neg" else "pos", d["v"]), "kind": d["kind"]})
    return reps


def counted(case, r):
    rule = case["rule"]
    if rule["t"] == "only":
        return r["src"] in rule["cnt"]
    return True


def select(case, reps, t, order):
    cov = [r for r in reps if r["start"] <= t <= r["end"] and counted(case, r)]
    if not cov:
        return None, [], []
    allcov = cov
    if case["rule"]["t"] == "auth":
        rank = case["rule"]["rank"]
        best = min(rank.index(r["src"]) for r in cov)
        cov = [r for r in cov if rank.index(r["src"]) == best]
    key = (lambda r: (r["pub"],)) if order == "A" else (lambda r: (r["start"], r["pub"]))
    m = max(key(r) for r in cov)
    top = [r for r in cov if key(r) == m]
    sigs = {r["sig"] for r in top}
    if len(sigs) > 1:
        return "TIE", top, allcov
    return top[0]["sig"], top, allcov


def resolve(case, t, cutoff):
    reps = known_reports(case, cutoff)
    ra, wa, cov = select(case, reps, t, "A")
    rb, wb, _ = select(case, reps, t, "B")
    # a negative winner ('no longer u') leaves the value open; a reader might instead fall back to an older report of
    # another value, so the alternatives are kept and any claim whose verdict would differ under that reading is dropped
    alts = []
    if ra not in (None, "TIE") and ra[0] == "neg":
        alts = sorted({r["sig"][1] for r in cov if r["sig"][0] == "pos" and r["sig"][1] != ra[1]}, key=repr)
    tied = sorted({r["sig"] for r in wa}, key=repr) if ra == "TIE" else None
    # implicature guard: a known scheduled or temporary change to v suggests the value is NOT v outside its period;
    # if the rule nevertheless yields v there (from another report), readers could disagree, so the point is unusable
    outcome = tied if ra == "TIE" else ([ra] if ra is not None else [])
    implicature_clash = any(r["kind"] in ("sched", "temp") and counted(case, r) and not (r["start"] <= t <= r["end"])
                            and r["sig"] in outcome for r in reps)
    tied_b = sorted({r["sig"] for r in wb}, key=repr) if rb == "TIE" else None
    return {"res": ra, "ok": ra == rb and tied == tied_b and not implicature_clash, "winA": sorted(r["sid"] for r in wa),
            "winB": sorted(r["sid"] for r in wb), "reps": reps, "cov": cov, "t": t, "cutoff": cutoff, "tied": tied,
            "neg_alts": alts}


def cmpf(op, v, x):
    return {"le": v <= x, "lt": v < x, "gt": v > x, "ge": v >= x}[op]


def unanimous(vs):
    vs = set(vs)
    return vs.pop() if len(vs) == 1 else N


def truth_r(r, claim):
    """Claim verdict for a resolution; reports tied under the rule settle the claim only if every one of them gives
    the same verdict (e.g. two same-day reports of 2:30 PM and 3:15 PM both make 'before 4:45 PM' true)."""
    if r["res"] == "TIE":
        return unanimous(truth(s, claim) for s in r["tied"])
    return truth(r["res"], claim)


def truth(res, claim):
    if res is None or res == "TIE":
        return N
    pol, v = res
    t = claim["t"]
    if t in ("eq", "neq"):
        x = claim["v"]
        if pol == "pos":
            same = v == x
        elif v == x:
            same = False
        else:
            return N
        return (T if same else F) if t == "eq" else (F if same else T)
    if t == "cmp":
        if pol != "pos":
            return N
        return T if cmpf(claim["op"], v, claim["thr"]) else F
    raise ValueError(t)


def truth_diff_r(ra, rb):
    o1 = ra["tied"] if ra["res"] == "TIE" else [ra["res"]]
    o2 = rb["tied"] if rb["res"] == "TIE" else [rb["res"]]
    return unanimous(truth_diff(a, b) for a in o1 for b in o2)


def truth_diff(r1, r2):
    if r1 in (None, "TIE") or r2 in (None, "TIE"):
        return N
    (p1, v1), (p2, v2) = r1, r2
    if p1 == "pos" and p2 == "pos":
        return T if v1 != v2 else F
    if p1 != p2:
        return T if v1 == v2 else N
    return N


def cutoff_of(case):
    m = case["mode"]
    return case["D"] if m == "known" else (None if m == "hind" else case["K"])


def evaluate(case):
    c = case.get("claim")
    if c and c["t"] == "diff":
        r2 = resolve(case, case["D"], case["D"])
        r1 = resolve(case, c["D2"], c["D2"])
        ok = r1["ok"] and r2["ok"] and not r1["neg_alts"] and not r2["neg_alts"]
        return {"ok": ok, "verdict": truth_diff_r(r1, r2), "res": r2["res"], "r": r2, "r1": r1}
    r = resolve(case, case["D"], cutoff_of(case))
    verdict = truth_r(r, c) if c else None
    ok = r["ok"]
    if r["neg_alts"]:
        ok = ok and c is not None and all(truth(("pos", a), c) == verdict for a in r["neg_alts"])
    return {"ok": ok, "verdict": verdict, "res": r["res"], "r": r, "r1": None}


def gold_of(case, ev):
    """Gold option for the case's question, or None when the question is not well-posed for this case."""
    qid = case["qid"]
    if not ev["ok"]:
        return None
    v = ev["verdict"]
    if qid == "supported":
        return "yes" if v == T else "no"
    if qid == "refuted":
        return "yes" if v == F else "no"
    if qid == "enough":
        return "no" if v == N else "yes"
    if qid == "direct":
        return None if v == N else ("yes" if v == T else "no")
    if qid == "choice3":
        return {T: "supported", F: "refuted", N: "not enough information"}[v]
    res = ev["res"]
    if qid == "pick":
        opts = case["pick_opts"]
        if res in (None, "TIE") or res[0] == "neg":
            return LETTERS[opts.index("NEI")]
        return LETTERS[opts.index(res[1])]
    if qid == "source":
        if res in (None, "TIE"):
            return "none"
        if res[0] == "neg":
            return None
        r = ev["r"]
        if r["winA"] != r["winB"] or len(r["winA"]) != 1:
            return None
        return str(case["order"].index(r["winA"][0]) + 1)
    raise ValueError(qid)


def options_of(case):
    qid = case["qid"]
    if qid in YESNO:
        return ["yes", "no"]
    if qid == "choice3":
        return ["supported", "refuted", "not enough information"]
    if qid == "pick":
        return LETTERS[:len(case["pick_opts"])]
    return [str(i) for i in range(1, len(case["docs"]) + 1)] + ["none"]


# ------------------------------------------------------------------------------------------------ structural validity
def valid(case):
    """Structural realism / unambiguity constraints (label-independent)."""
    dom = DOM[case["dom"]]
    docs = case["docs"]
    byid = {d["id"]: d for d in docs}
    gran = dom["gran"]
    lo, hi = case["win"]
    tg_count = {}
    for d in docs:
        if not (lo <= d["pub"] <= hi):
            return False
        if d["kind"] == "inject":
            continue
        src = dom["sources"][d["src"]]
        if src["style"] == "record" and (d["mood"] != "def" or d["kind"] == "neg"):
            return False
        if d["mood"] != "def" and src["docname"] in ("addendum", "traffic order", "release notes"):
            return False
        if d["kind"] in ("sched", "temp"):
            if d["start"] < d["pub"]:
                return False
            if d.get("rel") == "today" and d["start"] != d["pub"]:
                return False
            if d.get("rel") == "tomorrow" and d["start"] != d["pub"] + 1:
                return False
            if gran == "min" and (d["start"] // 1440 != d["pub"] // 1440 or d["start"] <= d["pub"]):
                return False
        if d["kind"] == "temp" and d["end"] < d["start"]:
            return False
        if d["kind"] == "temp" and dom.get("temp_vals") and d["v"] not in dom["temp_vals"]:
            return False
        if d.get("v") is not None and d["v"] not in case["vals"]:
            return False
        if d["kind"] in ("corr", "retr"):
            tg = byid.get(d["tgt"])
            if tg is None or not eligible(tg) or tg["kind"] not in REPORT_KINDS:
                return False
            if d["kind"] == "corr" and (tg["kind"] == "neg" or d["v"] == tg["v"]):
                return False
            if d["kind"] == "corr" and tg["kind"] == "temp" and dom.get("temp_vals") and d["v"] not in dom["temp_vals"]:
                return False
            if d["src"] != tg["src"] or d["pub"] <= tg["pub"]:
                return False
            tg_count[tg["id"]] = tg_count.get(tg["id"], 0) + 1
            # the reference '<our notice> of <date/time>' must pick out exactly one document of that source
            for o in docs:
                if o["id"] != tg["id"] and o["kind"] != "inject" and o["src"] == tg["src"] and \
                        _same_ref(gran, o["pub"], tg["pub"]):
                    return False
            if case.get("drop") == tg["id"]:
                return False
    if any(n > 1 for n in tg_count.values()):
        return False
    # corrections / withdrawals never target another correction or withdrawal (enforced by eligible), and a corrected
    # or withdrawn document is never itself turned into something else by a twin (ent/mood/kind stay report-like)
    # temporary windows: no other report is issued or takes effect inside a window, and windows do not overlap
    temps = [d for d in docs if d["kind"] == "temp" and eligible(d)]
    for tdoc in temps:
        for o in docs:
            if o["id"] == tdoc["id"] or not eligible(o):
                continue
            if tdoc["start"] <= o["pub"] <= tdoc["end"]:
                return False
            if o["kind"] in ("sched", "temp") and tdoc["start"] <= o["start"] <= tdoc["end"]:
                return False
            if o["kind"] == "temp" and o["start"] <= tdoc["start"] <= o["end"]:
                return False
    # hindsight / explicit cut-off modes: no report-like document issued after the point in time
    if case["mode"] in ("hind", "pk"):
        cut = INF if case["mode"] == "hind" else case["K"]
        if case["mode"] == "pk" and case["K"] <= case["D"]:
            return False
        for d in docs:
            if eligible(d) and case["D"] < d["pub"] <= cut:
                return False
    # event domains: everything happens before the event
    if dom["event"]:
        ev_t = case["event_t"]
        if any(d["pub"] >= ev_t for d in docs) or case["D"] >= ev_t:
            return False
    c = case.get("claim")
    if c and c["t"] == "diff" and not (c["D2"] < case["D"]):
        return False
    if not (case["dlo"] <= case["D"] <= case["dhi"]):
        return False
    return True


def _same_ref(gran, a, b):
    """Minute domains refer to an earlier message by its clock time, day domains by its date."""
    return (a % 1440 == b % 1440) if gran == "min" else a == b
