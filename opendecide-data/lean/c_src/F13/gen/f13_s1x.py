"""S1 Q-R (clause version history; AG-2 constructions K1 register date, K2 void correction) and AG-1 (active
exceptions for a unit) samplers. Same contract as f13_samplers: return a doc whose solver-A roles equal the plan, or
None. Every amendment carries its clause's scope mark (2.2, F13R2-06), so Q-R near-misses are NM-V only."""
from __future__ import annotations

import f13_base as B
import f13_model as M
from f13_samplers import Ctx, finish, rule, sec, true_atom


def _rule_sections(c, n, anames, ameta, case_attrs=None):
    out = []
    for _ in range(n):
        an = c.r.choice(anames)
        a = ameta[an]
        t = c.r.randint(a["lo"] + 1, max(a["lo"] + 2, a["hi"] - 1))
        out.append(rule(c.rid(), 1, [{"attr": an, "op": c.r.choice(["ge", "gt", "le", "lt"]), "val": t}], "all",
                        c.r.choice(c.card["outcomes"]), c.date(0, 150), scope=c.r.choice([None, None] +
                                                                                           c.card["units"])))
    return out


P_REG1 = {False: 1.0, True: 0.25}  # repair r9-1: by row shape (NM-R row: gold is the top revision)


def s1_qr(card, pack, plan, seed):
    """plan: {n_dec: 1|2|3, gold_rev: j | None (abstain), n_ver, k_cons: K1|K2|K12, td: bool}. Rule R is marked for
    the question's unit (so its versions are too)."""
    c = Ctx(card, pack, seed)
    r = c.r
    unit = r.choice(card["units"])
    attrs = card["attrs"]
    ameta = {a["name"]: a for a in attrs}
    anames = [a["name"] for a in attrs]
    Dq = c.date(500, 800)
    n = plan["n_ver"]
    j = plan["gold_rev"]
    rid = c.rid()
    effs = sorted(r.sample(range(10, 420), n))
    sections, dec = [], []
    vers = []
    for i in range(1, n + 1):
        an = r.choice(anames)
        a = ameta[an]
        conds = [{"attr": an, "op": r.choice(["ge", "gt", "le", "lt"]), "val": r.randint(a["lo"] + 1,
                                                                                         max(a["lo"] + 2, a["hi"] - 1))}]
        v = rule(rid, i, conds, "all", r.choice(card["outcomes"]), B.add_days(c.base, effs[i - 1]), scope=unit,
                 form="clause" if i == 1 else "amend", amends=None if i == 1 else f"{rid}.{i - 1}")
        vers.append(v)
    nm_secs = []
    use_k1 = plan["n_dec"] >= 2 and plan["k_cons"] in ("K1", "K12")
    use_k2 = plan["n_dec"] >= 2 and plan["k_cons"] in ("K2", "K12")
    # repair r4 (G0 2.6 question-date rows 50% latest-dated; G6 b_options): gold = the latest-dated version (no later
    # version, no K2). The near-miss is NM-R: a version of the same rule marked for another unit, dated before the
    # gold (activation: the question's unit -> that unit). Numbered in date order on half of these rows (gold = the
    # highest number), else numbered last, so the highest listed number is not tied to gold either way.
    wsec = None
    if j == n and not use_k2:
        others = [u for u in card["units"] if u != unit]
        lo_d, hi_d = (effs[n - 2] if n >= 2 else 0), effs[n - 1]
        if not others or hi_d - lo_d < 2:
            return None
        u2 = r.choice(others)
        an = r.choice(anames)
        a = ameta[an]
        conds = [{"attr": an, "op": r.choice(["ge", "gt", "le", "lt"]),
                  "val": r.randint(a["lo"] + 1, max(a["lo"] + 2, a["hi"] - 1))}]
        w = rule(rid, n + 1, conds, "all", r.choice(card["outcomes"]), B.add_days(c.base, r.randint(lo_d + 1, hi_d - 1)),
                 scope=u2, form="amend", amends=f"{rid}.{n - 1}" if n >= 2 else f"{rid}.1")
        if r.random() < 0.5:
            # date order: w takes number n, the gold (latest) number n + 1
            g_ = vers[-1]
            g_["rev"], g_["vid"], g_["amends"] = n + 1, f"{rid}.{n + 1}", f"{rid}.{n}"
            w["rev"], w["vid"] = n, f"{rid}.{n}"
        wsec = sec(c, r.choice(["bulletin", "register", "annex"]), "near_miss", [w], nm={"kind": "R", "unit": u2})
        vers_w = w
    for i, v in enumerate(vers, start=1):
        kind = "chapter" if i == 1 else r.choice(["bulletin", "register"])
        if i == j and wsec is not None:
            sections.append(wsec)
            nm_secs.append(wsec)
        if i < j:
            sections.append(sec(c, kind, "other", [v]))
        elif i == j:
            if use_k1:
                e = v["eff"]
                v["eff"] = None
                sections.append(sec(c, kind, "decisive", [v]))
                dec.append(sections[-1]["sid"])
                sections.append(sec(c, "register", "decisive", [{"ft": "effreg", "vid": v["vid"], "rid": rid,
                                                                  "eff": e}]))
                dec.append(sections[-1]["sid"])
            else:
                sections.append(sec(c, kind, "decisive", [v]))
                dec.append(sections[-1]["sid"])
        else:
            # repair r4 (G0 2.6): not yet effective / draft or proposed / void each 33%
            sub = r.choice(["not_yet", "not_yet", "draft", "proposed", "void", "void"])
            lo = B.add_days(c.base, effs[j - 1])
            if sub == "not_yet":
                v["eff"] = B.add_days(Dq, r.randint(1, 120)).isoformat()
            else:
                v["status"] = sub
            new_eff = B.add_days(lo, max(1, (Dq - lo).days // 2 + r.randint(-5, 5))).isoformat()
            s = sec(c, kind, "near_miss", [v], nm={"kind": "V", "sub": sub, "vid": v["vid"], "new_eff": new_eff})
            sections.append(s)
            nm_secs.append(s)
    if use_k2:
        # a later in-force version voided by a correction elsewhere: the correction is decisive, the voided version NM-V
        last = vers[-1]
        rv = rule(rid, n + 1, last["conds"], "all", r.choice(card["outcomes"]),
                  B.add_days(Dq, -r.randint(1, 30)), scope=unit, form="amend", amends=last["vid"])
        # it must take effect after every other in-force version
        if any(M.d_(v["eff"]) and M.d_(v["eff"]) >= M.d_(rv["eff"]) for v in vers if v["status"] == "in force"):
            return None
        sections.append(sec(c, r.choice(["bulletin", "register"]), "near_miss", [rv],
                            nm={"kind": "V", "sub": "void_entry", "vid": rv["vid"]}))
        sections.append(sec(c, "bulletin", "decisive", [{"ft": "void", "target": rv["vid"]}]))
        dec.append(sections[-1]["sid"])
    # repair r9-1 (G7 ag2 x mention_max; G0 2.1 A42): register-dated non-gold versions (see tmp/repair/r9/patch_r9_1.py)
    movable = [s_["facts"][0] for s_ in sections if s_["role"] == "other" and s_["facts"][0]["ft"] == "rule"
               and s_["facts"][0]["rid"] == rid] if use_k1 else []
    if use_k1 and wsec is not None:
        movable.append(vers_w)
    if use_k1 and use_k2:
        movable.append(rv)
    regs = []
    for v_ in movable:
        if v_.get("eff") is not None and r.random() < P_REG1[wsec is not None]:
            regs.append({"ft": "effreg", "vid": v_["vid"], "rid": rid, "eff": v_["eff"]})
            v_["eff"] = None
    if regs:
        gsec = [s_ for s_ in sections if s_["role"] == "decisive" and s_["facts"][0]["ft"] == "effreg"]
        if gsec and r.random() < 0.5:
            gsec[0]["facts"] = r.sample(gsec[0]["facts"] + regs, len(gsec[0]["facts"]) + len(regs))
        else:
            sections.append(sec(c, "register", "other", r.sample(regs, len(regs))))
    # other rules
    for f in _rule_sections(c, r.randint(2, 4), anames, ameta):
        sections.append(sec(c, "chapter" if f["scope"] is None else "annex", "other", [f]))
    if not any(s["role"] == "near_miss" for s in sections):
        return None
    shown = [v["vid"] for v in vers] + ([f"{rid}.{n + 1}"] if use_k2 else [])
    if wsec is not None:
        shown = sorted(shown + [vers_w["vid"]], key=lambda x: int(x.rsplit(".", 1)[1]))
    q = {"skill": "QR", "qk": "ag2_version" if plan["n_dec"] >= 2 else "qr_version", "form": "choice", "rid": rid,
         "unit": unit, "date": Dq.isoformat(), "shown": shown, "abstain": "NEI" if card["world"] == "open" else "NONE"}
    doc = {"card": card, "sections": sections, "query": q, "case": None, "title": f"{card['org']} {card['doc_noun']}"}
    if card["world"] != "open":
        # repair r8 (G0 2.3 display-then-gold; XF01, F13R4-SC1): closed cards hide one version ID, so '<None option>'
        # is gold on 1/k of these rows (qc r5c: 0/119 vs 27 expected)
        a = M.option_answer(doc)
        if a[0] != "val":
            return None
        hid = a[1] if plan.get("abstain_gold") else r.choice([x for x in shown if x != a[1]])
        q["shown"] = [x for x in shown if x != hid]
        if len(q["shown"]) < 2 or (M.option_answer(doc)[0] == "abstain") != bool(plan.get("abstain_gold")):
            return None
    return finish(doc, dec, plan)


def s1_ag1(card, pack, plan, seed):
    """plan: {n_dec: 2|3, count: g (>= n_dec), nm_kinds: [V|R ...]}. Exceptions marked for the unit, active on the
    question date, spread over n_dec sections; NM-V (draft / proposed / void status / not yet effective), NM-R (marked
    for another unit, active); role-less: exceptions marked for the unit whose window ended before the date."""
    c = Ctx(card, pack, seed)
    r = c.r
    unit = r.choice(card["units"])
    others = [u for u in card["units"] if u != unit]
    attrs = card["attrs"]
    ameta = {a["name"]: a for a in attrs}
    anames = [a["name"] for a in attrs]
    Dq = c.date(500, 800)
    rules = _rule_sections(c, r.randint(2, 4), anames, ameta)
    sections = [sec(c, "chapter" if f["scope"] is None else "annex", "other", [f]) for f in rules]
    rids = [f["rid"] for f in rules]
    g, nd = plan["count"], plan["n_dec"]
    if g < nd:
        return None
    split = sorted(r.sample(range(1, g), nd - 1)) if nd > 1 else []
    sizes = [b - a for a, b in zip([0] + split, split + [g])]
    used = set()

    def exc(scope, status="in force", eff=None, end=("none",)):
        eid = f"EX-{r.randint(100, 989)}"
        while eid in used:
            eid = f"EX-{r.randint(100, 989)}"
        used.add(eid)
        an = r.choice(anames)
        return {"ft": "exc", "eid": eid, "rid": r.choice(rids), "conds": [true_atom(c, ameta[an], r.randint(
            ameta[an]["lo"] + 2, ameta[an]["hi"] - 2))], "join": "all", "scope": scope, "status": status,
            "eff": (eff or B.add_days(Dq, -r.randint(20, 400))).isoformat(), "end": list(end)}
    dec = []
    for k in sizes:
        fs = []
        for _ in range(k):
            end = ("none",) if r.random() < 0.6 else ("through", B.add_days(Dq, r.randint(0, 200)).isoformat())
            fs.append(exc(unit, end=end))
        sections.append(sec(c, "bulletin", "decisive", fs))
        dec.append(sections[-1]["sid"])
    for kind in plan["nm_kinds"]:
        if kind == "V":
            sub = r.choice(["not_yet", "draft", "proposed", "void"])
            if sub == "not_yet":
                e = exc(unit, eff=B.add_days(Dq, r.randint(1, 120)))
                nm = {"kind": "V", "sub": sub, "eid": e["eid"], "vid": None,
                      "new_eff": B.add_days(Dq, -r.randint(1, 60)).isoformat()}
            else:
                e = exc(unit, status=sub)
                nm = {"kind": "V", "sub": sub, "eid": e["eid"], "vid": None}
            sections.append(sec(c, r.choice(["bulletin", "register"]), "near_miss", [e], nm=nm))
        elif kind == "R":
            u2 = r.choice(others)
            c2 = r.choice([x for x in plan["shown"] if x != g and x >= 1] or [None])
            if c2 is None:
                return None
            sections.append(sec(c, "annex", "near_miss", [exc(u2) for _ in range(c2)], nm={"kind": "R", "unit": u2}))
    for _ in range(r.randint(1, 2)):
        endk = r.choice(["through", "repealed"])
        e = exc(unit, eff=B.add_days(Dq, -r.randint(300, 500)), end=(endk, B.add_days(Dq, -r.randint(
            1 if endk == "through" else 0, 200)).isoformat()))
        if endk == "repealed" and M.d_(e["end"][1]) <= M.d_(e["eff"]):
            continue
        sections.append(sec(c, "bulletin", "other", [e]))
    q = {"skill": "QP", "qk": "ag1_exc", "form": "choice", "unit": unit, "date": Dq.isoformat(),
         "shown": plan["shown"], "abstain": "NEI" if card["world"] == "open" else "NONE"}
    doc = {"card": card, "sections": sections, "query": q, "case": None, "title": f"{card['org']} {card['doc_noun']}"}
    return finish(doc, dec, plan)


def s1_inverted(card, pack, plan, seed):
    """repair r5 B7 (G0 3.1 inverted rows, A62, SEM-56, XF14, F13R1-08): "Which of these cases meets rule <R>?" on an
    inverted card (every Q-P choice row). The named rule is an 'if' clause (SEM-09), no exception names it, and every
    other rule fails for every listed case, so no rule SEM-24 ranks above it gives a listed case another outcome.
    Closed: <= 1 listed case meets (gold; or None with the gold case deleted, the answerable base keeping it, see
    SM.role_doc); open determined: exactly one meets and every other case is shown not to; open NEI rows come from
    build_row's T-D trace on the named rule's versions. Near-misses are NM-V only (a later version of the named rule,
    draft / proposed / void, that one other listed case alone meets): an other-unit version can only add a second hit
    or remove the gold one (never a single different hit), as for S1 Q-R (2.2 F13R2-06)."""
    c = Ctx(card, pack, seed)
    r = c.r
    attrs = card["attrs"]
    if len(attrs) < 2:
        return None
    open_ = card["world"] == "open"
    n = max(2, len(plan["shown"]))  # listed cases; options = cases + the abstain option
    abst = bool(plan.get("abstain_gold")) and not open_
    ncase = n
    ameta = {a["name"]: a for a in attrs}
    anames = [a["name"] for a in r.sample(attrs, min(len(attrs), r.randint(2, 3)))]
    a0, a1 = ameta[anames[0]], ameta[anames[1]]
    gi = r.randrange(ncase)
    U = r.choice(card["units"])  # every listed case and every version of the named rule sit in one unit (2.2 F13R2-06)
    cases = []
    for i in range(ncase):
        cases.append({"cid": None, "ft": "case", "attrs": {x: r.randint(ameta[x]["lo"] + 2, ameta[x]["hi"] - 2)
                                                           for x in anames},
                      "scope": U, "gdate": c.date(300, 700).isoformat()})
    g = cases[gi]
    at = true_atom(c, a0, g["attrs"][a0["name"]])
    t = at["val"]
    lo, hi = a0["lo"], a0["hi"]
    # every other case fails the decisive atom
    rng_fail = {"ge": (lo, t - 1), "gt": (lo, t), "le": (t + 1, hi), "lt": (t, hi)}[at["op"]]
    if rng_fail[0] > rng_fail[1]:
        return None
    for i, x in enumerate(cases):
        if i != gi:
            x["attrs"][a0["name"]] = r.randint(*rng_fail)
    conds = [at]
    if r.random() < 0.35 and len(anames) >= 3:
        a2 = ameta[anames[2]]
        conds.append(true_atom(c, a2, g["attrs"][a2["name"]]))
    rid = c.rid()
    eff0 = c.date(0, 200)
    sections, dec = [], []
    if abst:
        # closed 'None' row (F13R1-08 "at most one"): the case that met version 1 fails the later version in force;
        # deleting that later version (decisive) gives the case back, so D is read on the row itself (solver B)
        rv = rule(rid, 1, conds, "all", r.choice(card["outcomes"]), eff0, scope=U)
        sections.append(sec(c, "chapter", "other", [rv]))
        vals0 = [x["attrs"][a0["name"]] for x in cases]
        lc = {"attr": a0["name"], "op": "gt", "val": max(vals0) + r.randint(0, 6)} if r.random() < 0.5 else \
            {"attr": a0["name"], "op": "lt", "val": max(1, min(vals0) - r.randint(0, 6))}
        if lc["op"] == "lt" and lc["val"] > min(vals0):
            return None
        el = c.date(205, 250)
        late = plan.get("n_dec", 1) >= 2
        vl = rule(rid, 2, [lc], "all", rv["outcome"], None if late else el, scope=U, form="amend", amends=rv["vid"])
        sections.append(sec(c, r.choice(["bulletin", "register"]), "decisive", [vl]))
        dec.append(sections[-1]["sid"])
        if late:
            sections.append(sec(c, "register", "decisive", [{"ft": "effreg", "vid": vl["vid"], "rid": rid,
                                                              "eff": el.isoformat()}]))
            dec.append(sections[-1]["sid"])
        rv = vl
    elif plan.get("n_dec", 1) >= 2:
        rv = rule(rid, 1, conds, "all", r.choice(card["outcomes"]), None, scope=U)
        sections.append(sec(c, "chapter", "decisive", [rv]))
        dec.append(sections[-1]["sid"])
        sections.append(sec(c, "register", "decisive", [{"ft": "effreg", "vid": rv["vid"], "rid": rid,
                                                          "eff": eff0.isoformat()}]))
        dec.append(sections[-1]["sid"])
    else:
        rv = rule(rid, 1, conds, "all", r.choice(card["outcomes"]), eff0, scope=U)
        sections.append(sec(c, "chapter", "decisive", [rv]))
        dec.append(sections[-1]["sid"])
    # other rules: each fails for every listed case (a threshold beyond all listed values)
    for _ in range(r.randint(2, 4)):
        an = r.choice(anames)
        vals = [x["attrs"][an] for x in cases]
        if r.random() < 0.5:
            cond = {"attr": an, "op": "gt", "val": max(vals) + r.randint(0, 8)}
        else:
            cond = {"attr": an, "op": "lt", "val": max(0, min(vals) - r.randint(0, 8))}
            if cond["val"] == 0 and min(vals) == 0:
                continue
        sc = r.choice([None, None, r.choice(card["units"])])
        sections.append(sec(c, "chapter" if sc is None else "annex", "other",
                            [rule(c.rid(), 1, [cond], "all", r.choice(card["outcomes"]), c.date(0, 250), scope=sc)]))
    # near-misses: NM-V later versions of the named rule that one other listed case alone meets
    others = [i for i in range(ncase) if i != gi]
    r.shuffle(others)
    n_nm = min(max(1, len(plan.get("nm_kinds") or [1])), 2, len(others))
    rev = rv["rev"]
    for j, op in zip(others[:n_nm], r.sample(["gt", "lt"], 2)):
        rest = [x["attrs"][a1["name"]] for i, x in enumerate(cases) if i != j]
        if op == "gt":
            tt = max(rest)
            vj = tt + r.randint(1, 5)
            if vj > a1["hi"]:
                return None
        else:
            tt = min(rest)
            vj = tt - r.randint(1, 5)
            if vj < a1["lo"]:
                return None
        cases[j]["attrs"][a1["name"]] = vj
        rev += 1
        sub = r.choice(["draft", "proposed", "void"])
        nv = rule(rid, rev, [{"attr": a1["name"], "op": op, "val": tt}], "all", rv["outcome"],
                  c.date(255, 295) if abst else B.add_days(eff0, r.randint(5, 90)), scope=U, status=sub,
                  form="amend", amends=rv["vid"])
        sections.append(sec(c, r.choice(["bulletin", "register"]), "near_miss", [nv],
                            nm={"kind": "V", "sub": sub, "vid": nv["vid"]}))
    keys = {(tuple(sorted(x["attrs"].items())), x["scope"], x["gdate"]) for x in cases}
    if len(keys) < ncase:
        return None
    r.shuffle(sections)
    shown_cases = cases
    q = {"skill": "QP", "qk": "qp_inverted", "form": "inverted", "neg": 0, "inner_neg": False, "case_ref": None,
         "rid": rid, "cases": shown_cases, "shown": list(range(len(shown_cases))),
         "abstain": "NEI" if open_ else "NONE", "claim": {"value": None}}
    doc = {"card": card, "sections": sections, "query": q, "case": None,
           "title": f"{card['org']} {card['doc_noun']}"}
    return finish(doc, dec, {**plan, "target": None})
