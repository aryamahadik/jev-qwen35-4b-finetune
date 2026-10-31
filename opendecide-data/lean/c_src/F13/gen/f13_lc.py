"""S2 case file + S6 minutes (G0 4.2, 4.5): decisions (S2 notices / S6 motions), holds and conditions (S2 AG-1),
action items (S6 holder Q-R and AG-1 open items). Solver A semantics (SEM-50..53, SEM-57, SEM-30) and label-first
samplers. Same contract as f13_samplers: a sampler returns a doc whose solver-A roles equal its plan, or None.

Model facts (f13_model schema additions; dates are ISO strings):
  dec   {ft, matter, kind: decision|revision, date, outcome, status: in force|proposed, votes: None|[a, b, c]}
        S2: a notice ('Status: proposed.' line on proposals). S6: a motion in a committee-marked minutes section whose
        meeting date is `date`; carried iff votes[0] >= card vote_k; S6 proposal: kind revision, status proposed,
        votes None.
  dvoid {ft, matter, kind, date}                    void of the entry (kind + matter + date), F13R2-03
  dcorr {ft, matter, kind, date, new, old}          outcome correction (from the start, SEM-26)
  hold  {ft, hid, noun, eid, placed, released | None, scope}
  lcond {ft, cnd, noun, eid, imposed, end: None | [met|waived, date], scope}
  aitem {ft, aid, events: [[assigned|transferred|closed|reopened, person | None, date], ...]}
Scope (SEM-30, one rule): an entry / item in a section with no mark applies to all units; one in a section marked for
a unit (S6 committees) only to that unit. Holds and conditions carry item marks (AG-1: no unmarked countable items).
S6 sections: scope = committee, mdate = meeting date (minutes) or None (memo sections).
"""
from __future__ import annotations

import f13_base as B
import f13_model as M
from f13_samplers import Ctx, _why

UNDET = M.UNDET
COMMITTEES = ("Finance Committee", "Standards Committee", "Planning Committee", "Review Committee",
              "Operations Committee", "Steering Committee", "Grants Committee", "Works Committee")
LC_QK = ("qr_decision", "ag2_decision", "ag1_hold", "ag1_cond", "qr_holder", "ag1_items")


# ================================================================================================ solver A semantics
def _applies(sec, unit):
    return sec.get("scope") is None or sec.get("scope") == unit


def decision_in_force(doc, matter, unit, on):
    """SEM-50 / SEM-51 / SEM-26 / SEM-27: the latest non-void, in-force (carried) entry on the matter dated on or
    before `on`, with its outcome as corrected."""
    k = doc["card"].get("vote_k") or 0
    ents, voids, corrs = [], set(), {}
    for s in doc["sections"]:
        if not _applies(s, unit):
            continue
        for f in s["facts"]:
            if f.get("matter") != matter:
                continue
            key = (s.get("scope"), f.get("kind"), f.get("date"))
            if f["ft"] == "dec":
                ents.append((s.get("scope"), f))
            elif f["ft"] == "dvoid":
                voids.add(key)
            elif f["ft"] == "dcorr":
                corrs[key] = f["new"]
    ok = [(sc, e) for sc, e in ents if e["status"] == "in force" and (e["votes"] is None or e["votes"][0] >= k)
          and (sc, e["kind"], e["date"]) not in voids and M.d_(e["date"]) <= on]
    if not ok:
        return UNDET
    sc, e = max(ok, key=lambda x: x[1]["date"])
    return corrs.get((sc, e["kind"], e["date"]), e["outcome"])


def lc_active(doc, ft, noun, eid, unit, on):
    """SEM-53: holds / conditions on (noun, eid) marked for `unit` active at the end of `on`."""
    n = 0
    for s in doc["sections"]:
        for f in s["facts"]:
            if f["ft"] != ft or f["noun"] != noun or f["eid"] != eid or f["scope"] != unit:
                continue
            st = f["placed"] if ft == "hold" else f["imposed"]
            en = f["released"] if ft == "hold" else (f["end"][1] if f["end"] else None)
            if M.d_(st) <= on and (en is None or M.d_(en) > on):
                n += 1
    return n


def ai_state(f, on):
    """SEM-52: [open, holder] at the end of `on`, or None before assignment."""
    st = None
    for verb, who, d in sorted(f["events"], key=lambda e: e[2]):
        if M.d_(d) > on:
            break
        if verb == "assigned":
            st = [True, who]
        elif verb == "transferred":
            st[1] = who
        elif verb == "closed":
            st[0] = False
        elif verb == "reopened":
            st[0] = True
    return st


def ai_holder(doc, aid, unit, on):
    for s in doc["sections"]:
        if not _applies(s, unit):
            continue
        for f in s["facts"]:
            if f["ft"] == "aitem" and f["aid"] == aid:
                st = ai_state(f, on)
                return st[1] if st and st[0] else UNDET
    return UNDET


def ai_count(doc, unit, holder, on):
    n = 0
    for s in doc["sections"]:
        if s.get("scope") != unit:
            continue
        for f in s["facts"]:
            if f["ft"] == "aitem":
                st = ai_state(f, on)
                if st and st[0] and st[1] == holder:
                    n += 1
    return n


def lc_core(doc):
    q = doc["query"]
    on = M.d_(q["date"])
    qk = q["qk"]
    if qk in ("qr_decision", "ag2_decision"):
        return decision_in_force(doc, q["matter"], q["unit"], on)
    if qk in ("ag1_hold", "ag1_cond"):
        return lc_active(doc, "hold" if qk == "ag1_hold" else "lcond", q["noun"], q["eid"], q["unit"], on)
    if qk == "qr_holder":
        return ai_holder(doc, q["aid"], q["unit"], on)
    if qk == "ag1_items":
        return ai_count(doc, q["unit"], q["holder"], on)
    raise ValueError(qk)


def lc_activate(d2, sec, nm):
    """The one operator per near-miss kind (F13R3-09): V dvoid (remove the void), V dlate (set the entry's own /
    meeting date to the question's date), V dprop (put the proposal in force as a carried entry of the same date);
    R (the question's unit / committee set to the section's); I (the question's ID set to the look-alike)."""
    q = d2["query"]
    if nm["kind"] == "V":
        if nm["sub"] == "dvoid":
            for s in d2["sections"]:
                if s.get("scope") != sec.get("scope"):
                    continue
                s["facts"] = [x for x in s["facts"] if not (x["ft"] == "dvoid" and x["matter"] == nm["matter"] and
                                                            x["kind"] == nm["dkind"] and x["date"] == nm["date"])]
            return
        f = next(x for x in sec["facts"] if x["ft"] == "dec" and x["matter"] == nm["matter"] and
                 x["date"] == nm["date"])
        if nm["sub"] == "dlate":
            f["date"] = q["date"]
            if sec.get("mdate"):
                sec["mdate"] = q["date"]
        else:
            f["status"] = "in force"
            if d2["card"].get("lc") == "motion":
                f["votes"] = [d2["card"]["vote_k"], 0, 0]
    elif nm["kind"] == "R":
        q["unit"] = nm["unit"]
    elif nm["kind"] == "I":
        q[nm["field"]] = nm["id"]


def lc_witness(doc, sec):
    """Typed completions of a T-D part (G0 2.4 completion domains, shared with solver B): besides {empty, original},
    facts of the label's one type for its scope, dated on the question's date."""
    t = sec["trace"]
    q, card = doc["query"], doc["card"]
    lab = t["label"]
    k = card["scope_kind"]
    unit = t["scope_label"][len(k) + 1:] if t["scope_label"].startswith(k + " ") else None
    out = []
    if lab in ("Decision notices", "Motions"):
        matter = t["scope_label"] if lab == "Decision notices" else q.get("matter")
        for o in card["outcomes"]:
            out.append({"scope": unit if lab == "Motions" else None,
                        "facts": [_dec(matter, "revision", q["date"], o,
                                       votes=[card["vote_k"], 0, 0] if lab == "Motions" else None)]})
    elif lab in ("Holds", "Conditions"):
        f = {"ft": "hold", "hid": "HD-W", "noun": q.get("noun"), "eid": q.get("eid"), "placed": "1900-01-01",
             "released": None, "scope": unit} if lab == "Holds" else \
            {"ft": "lcond", "cnd": "CN-W", "noun": q.get("noun"), "eid": q.get("eid"), "imposed": "1900-01-01",
             "end": None, "scope": unit}
        out.append({"scope": None, "facts": [f]})
    elif lab == "Action items":
        if q.get("holder"):
            out.append({"scope": unit, "facts": [{"ft": "aitem", "aid": "AC-W", "events": [
                ["assigned", q["holder"], "1900-01-01"]]}]})
        if q.get("aid"):
            for p in list(card["holders"]) + ["W"]:
                out.append({"scope": unit, "facts": [{"ft": "aitem", "aid": q["aid"], "events": [
                    ["assigned", p, "1900-01-01"]]}]})
    return out


# ================================================================================================ helpers
def lc_card(card, pack):
    """S2 / S6 card fields (called by make_card). S6: scope dimension 'committee' (SEM-30, A20), committees and the
    vote rule k (SEM-51); holders are people, never committees (F13R5-06)."""
    r = B.rng("f13-lccard", card["card_id"])
    s = card["sampler"]
    card["lc"] = "motion" if s == "S6" else "notice"
    ent = pack["ents"][0]
    card["ent_prefix"] = ent["prefix"]
    if s == "S6":
        card["scope_kind"] = "committee"
        card["units"] = r.sample(COMMITTEES, r.choice([3, 4]))
        card["vote_k"] = r.choice([3, 4, 5, 6])
        card["fact_kinds"] = ["rule", "amendment", "exception", "version", "motion", "decision", "correction",
                              "proposal", "action item"]
        card["scoped_kinds"] = ["rule", "version", "amendment", "exception", "decision", "action item", "entry"]
    else:
        card["vote_k"] = None
        card["fact_kinds"] = ["rule", "amendment", "exception", "version", "decision", "correction", "hold",
                              "condition"]
        card["scoped_kinds"] = ["rule", "version", "amendment", "exception", "hold", "condition"]
    card["holders"] = [p for p in (pack["people"] or []) if p not in card["units"]][:8]
    return card


def _sec(c, heading, role, facts, scope=None, mdate=None, **kw):
    c.sec_no += 1
    s = {"sid": f"s{c.sec_no:02d}", "heading": heading.format(n=c.sec_no + 1), "kind": "lc", "scope": scope,
         "role": role, "facts": facts, "trace": None}
    if mdate:
        s["mdate"] = mdate
    s.update(kw)
    return s


S2_HEADS = ("Correspondence {n}", "File papers {n}", "Letters {n}", "Enclosure {n}", "Case notes {n}")
S6_MIN = ("Minutes {n}", "Meeting record {n}", "Minutes of the meeting {n}")
S6_MEMO = ("Memo {n}", "Message {n}", "Secretary's note {n}", "Follow-up list {n}")


def _dates(c, lo, hi, n, taken):
    out = []
    for _ in range(n * 50):
        if len(out) == n:
            break
        d = B.add_days(c.base, c.r.randint(lo, hi)).isoformat()
        if d not in taken:
            taken.add(d)
            out.append(d)
    return sorted(out) if len(out) == n else None


def _entity(c, taken):
    return B.new_id(c.card["ent_prefix"], 4, c.r, taken, digits_only=True)


def _intake(c, eid, unit):
    """Intake form (role-less case record of the primary entity, A38)."""
    attrs = {a["name"]: c.r.randint(a["lo"], a["hi"]) for a in c.card["attrs"]}
    return {"ft": "case", "cid": eid, "attrs": attrs, "scope": unit,
            "gdate": B.add_days(c.base, c.r.randint(0, 200)).isoformat()}


def _dec(matter, kind, date, outcome, status="in force", votes=None):
    return {"ft": "dec", "matter": matter, "kind": kind, "date": date, "outcome": outcome, "status": status,
            "votes": votes}


def _votes(c, carried):
    k = c.card["vote_k"]
    a = c.r.randint(k, k + 5) if carried else c.r.randint(max(0, k - 3), k - 1)
    return [a, c.r.randint(0, 4), c.r.randint(0, 3)]


def _finish_lc(doc, dec, plan):
    """Solver A checks of the planned roles (as f13_samplers.finish, for LC query kinds)."""
    A = M.answers(doc)
    if M.CONFLICT in A or UNDET in A or len(A) != 1:
        return _why("lc undet")
    v = next(iter(A))
    if plan.get("value") is not None and v != plan["value"]:
        return _why("lc target")
    if M.option_answer(doc)[0] == "bad":
        return _why("lc bad")
    from f13_samplers import role_doc
    rd = role_doc(doc)
    D = M.decisive_set(rd)
    if sorted(D) != sorted(dec):
        return _why("lc D")
    if not M.sufficient(rd, D):
        return _why("lc suff")
    for s in rd["sections"]:
        if s["role"] == "near_miss":
            if not M.nm_functional(rd, s["sid"]):
                return _why("lc nm " + s["nm"]["kind"] + s["nm"].get("sub", ""))
            if M.option_answer(M.activate(rd, s["sid"]))[0] == "abstain" and rd["query"].get("abstain") != "NONE":
                return _why("lc nm abstain")  # r7: closed choice rows may activate to None (unshown new answer)
    doc["decisive"] = D
    return doc


def _nm_out(plan, g, nm_pool, r):
    """Near-miss answer: on choice rows any shown non-gold option; on yes/no, establish and settle rows the activation
    flips the claim's truth (2.3): the claimed value when the claim is false, any other value when it is true."""
    if plan["form"] == "choice":
        return lambda: r.choice(nm_pool)
    cv = plan["claim_value"]
    if cv != g:
        return lambda: cv
    oth = [o for o in plan["shown"] if o != g]
    return lambda: r.choice(oth)


def est_true(plan):
    """'Establish' rows whose inner claim holds before frame negation: only near-misses whose deletion restores the
    base answer (decision NM-V) stay decisive after activation."""
    return plan["form"] == "establish" and ((plan["value"] == plan["claim_value"]) != bool(plan.get("inner_neg")))


def _q(plan, card, **kw):
    q = {"skill": "QR", "form": plan["form"], "neg": plan.get("neg", 0), "inner_neg": plan.get("inner_neg", False),
         "shown": plan["shown"], "abstain": "NEI" if card["world"] == "open" else "NONE"}
    if plan["form"] in ("yn", "establish", "settle"):
        q["claim"] = {"value": plan["claim_value"]}
    q.update(kw)
    return q


def _filler(c, unit, eid, taken, n_rules=(0, 1)):
    """Role-less context: intake form, rules from a policy excerpt (S1 grammar)."""
    import f13_s1x as S1X
    out = [_sec(c, "Intake form", "other", [_intake(c, eid, unit)])]
    anames = [a["name"] for a in c.card["attrs"]]
    ameta = {a["name"]: a for a in c.card["attrs"]}
    for f in S1X._rule_sections(c, c.r.randint(*n_rules), anames, ameta):
        out.append(_sec(c, "Policy excerpt {n}", "other", [f]))
    return out


# ================================================================================================ decisions (Q-R, AG-2)
def lc_decision(card, pack, plan, seed):
    """plan: kind qrd (1 decisive section) | ag2d (k_cons K1 corrected outcome | K2 void | K12; 2-3 decisive),
    value (gold outcome of the determined base), shown, nm_kinds (S2: Vb Vc I [Va via K2]; S6: Vb Vc R)."""
    c = Ctx(card, pack, seed)
    r = c.r
    motion = card["lc"] == "motion"
    outs = card["outcomes"]
    g = plan["value"]
    unit = r.choice(card["units"])
    taken_ids = set()
    eid = _entity(c, taken_ids)
    noun = card["item"]
    matter = f"{noun} {eid}"
    Dq = B.add_days(c.base, r.randint(600, 800))
    taken_d = {Dq.isoformat()}
    kc = plan.get("k_cons")
    use_k1 = kc in ("K1", "K12")
    use_k2 = kc in ("K2", "K12")
    nmk = list(plan["nm_kinds"])
    if use_k2:
        nmk = [k for k in nmk if k not in ("Vb", "Vc")]  # at most one decision near-miss per matter (2.3)
    nm_pool = [o for o in plan["shown"] if o != g]
    if not nm_pool:
        return _why("lc nm pool")
    nm_out = _nm_out(plan, g, nm_pool, r)
    n_prev = r.choice([0, 1, 1, 2])
    flip = plan["form"] == "establish" and plan["claim_value"] != g
    if flip:
        n_prev = max(1, n_prev)  # contradicted claim: deleting E* restores the claimed outcome (2.2)
    # timeline (strictly increasing, distinct dates): prev entries, E*, [proposal], [R2 voided], Dq, [late]
    ds = _dates(c, 0, 560, n_prev + 3, taken_d)
    if ds is None:
        return None
    e_date = ds[n_prev]
    after = ds[n_prev + 1:]
    sections, dec = [], []
    stated = g
    if use_k1:
        stated = r.choice([o for o in outs if o != g])
    prev_outs = []
    for i in range(n_prev + 1):
        if i == n_prev:
            o = stated
        else:
            o = r.choice([x for x in outs if x != (prev_outs[-1] if prev_outs else None)])
        prev_outs.append(o)
    # the entry before E* must give a different answer than g (E* decisive)
    if n_prev and prev_outs[n_prev - 1] == g:
        prev_outs[n_prev - 1] = r.choice([o for o in outs if o not in (g, prev_outs[n_prev - 2] if n_prev >= 2
                                                                        else None)])
    if flip:
        prev_outs[n_prev - 1] = plan["claim_value"]
        if n_prev >= 2 and prev_outs[n_prev - 2] == plan["claim_value"]:
            prev_outs[n_prev - 2] = r.choice([o for o in outs if o != plan["claim_value"]])
    if n_prev and prev_outs[n_prev - 1] == prev_outs[n_prev]:
        return _why("lc same consecutive")
    kinds = ["decision"] + ["revision"] * n_prev
    ents = [_dec(matter, kinds[i], ds[i] if i < n_prev else e_date, prev_outs[i],
                 votes=_votes(c, True) if motion else None) for i in range(n_prev + 1)]
    estar = ents[-1]

    def minutes(f, role, **kw):
        return _sec(c, r.choice(S6_MIN), role, [f], scope=unit, mdate=f["date"], **kw)

    def notice(f, role, **kw):
        return _sec(c, r.choice(S2_HEADS), role, [f], **kw)

    put = minutes if motion else notice
    if n_prev:
        if motion:
            for f in ents[:-1]:
                sections.append(minutes(f, "other"))
        else:
            sections.append(_sec(c, r.choice(S2_HEADS), "other", ents[:-1]))
    sections.append(put(estar, "decisive"))
    dec.append(sections[-1]["sid"])
    memo = (lambda fs, role, **kw: _sec(c, r.choice(S6_MEMO), role, fs, scope=unit, **kw)) if motion else \
        (lambda fs, role, **kw: _sec(c, r.choice(S2_HEADS), role, fs, **kw))
    if use_k1:
        sections.append(memo([{"ft": "dcorr", "matter": matter, "kind": estar["kind"], "date": estar["date"],
                               "new": g, "old": stated}], "decisive"))
        dec.append(sections[-1]["sid"])
    # proposal (NM-V c): dated after E*, before Dq (and before the voided revision)
    if "Vc" in nmk:
        po = nm_out()
        pf = _dec(matter, "revision", after[0], po, status="proposed")
        sections.append(put(pf, "near_miss", nm={"kind": "V", "sub": "dprop", "lc": True, "matter": matter,
                                                 "date": pf["date"]}))
    if use_k2:
        ro = nm_out()
        rf = _dec(matter, "revision", after[1], ro, votes=_votes(c, True) if motion else None)
        sections.append(put(rf, "near_miss", nm={"kind": "V", "sub": "dvoid", "lc": True, "matter": matter,
                                                 "dkind": "revision", "date": rf["date"]}))
        sections.append(memo([{"ft": "dvoid", "matter": matter, "kind": "revision", "date": rf["date"]}],
                             "decisive"))
        dec.append(sections[-1]["sid"])
    if "Vb" in nmk:
        lo_ = B.add_days(Dq, r.randint(5, 150)).isoformat()
        if lo_ in taken_d:
            return None
        lf = _dec(matter, "revision", lo_, nm_out(), votes=_votes(c, True) if motion else None)
        sections.append(put(lf, "near_miss", nm={"kind": "V", "sub": "dlate", "lc": True, "matter": matter,
                                                 "date": lf["date"]}))
    if "I" in nmk and not motion:
        e2 = B.lookalike(eid, r, taken_ids)
        if e2 is None:
            return None
        taken_ids.add(e2)
        d2 = _dates(c, 0, 560, 1, taken_d)
        sections.append(notice(_dec(f"{noun} {e2}", "decision", d2[0], nm_out()), "near_miss",
                               nm={"kind": "I", "lc": True, "field": "matter", "id": f"{noun} {e2}"}))
    if "R" in nmk and motion:
        u2 = r.choice([u for u in card["units"] if u != unit])
        d2 = _dates(c, 0, 560, 1, taken_d)
        f2 = _dec(matter, "decision", d2[0], nm_out(), votes=_votes(c, True))
        sections.append(_sec(c, r.choice(S6_MIN), "near_miss", [f2], scope=u2, mdate=f2["date"],
                             nm={"kind": "R", "lc": True, "unit": u2}))
    if motion and r.random() < 0.6:
        # a failed revise motion (role-less, SEM-51) at another meeting before Dq
        d3 = _dates(c, 0, 560, 1, taken_d)
        if d3 and d3[0] > estar["date"] and not use_k2:
            fm = _dec(matter, "revision", d3[0], r.choice([o for o in outs if o != g]), votes=_votes(c, False))
            sections.append(minutes(fm, "other"))
    if not any(s["role"] == "near_miss" for s in sections):
        return _why("lc no nm")
    if plan["form"] == "choice":
        # repair r4 (G7 mention_max / mention0 / mention1 on decision rows): role-less decisions on other matters
        # (fresh IDs, never look-alikes) mention every shown outcome, so gold is not the most-mentioned by construction
        # repair r7 (G7 QR mention1 over / mention2p under: gold sat at 1 mention, distractors were topped up to it +/- 1):
        # each shown outcome, gold included, draws the same mention target t and is topped up to max(t, its count)
        def n_men(o):
            return sum(1 for s in sections for f in s["facts"] if f.get("outcome") == o or (
                f.get("ft") == "dcorr" and o in (f.get("new"), f.get("old"))))
        for o in list(plan["shown"]):
            t = r.choices([1, 2, 3], [0.40, 0.35, 0.25])[0]
            add = max(0, t - n_men(o))
            for _ in range(add):
                dd = _dates(c, 0, 560, 1, taken_d)
                if not dd:
                    break
                fo = _dec(f"{noun} {_entity(c, taken_ids)}", "decision", dd[0], o,
                          votes=_votes(c, True) if motion else None)
                sections.append(_sec(c, r.choice(S6_MIN), "other", [fo], scope=r.choice(card["units"]),
                                     mdate=fo["date"]) if motion else notice(fo, "other"))
    sections += _filler(c, unit if not motion else r.choice(card["units"]), eid, taken_ids)
    if not motion and r.random() < 0.5:
        hd = _dates(c, 0, 560, 1, taken_d)
        sections.append(_sec(c, r.choice(S2_HEADS), "other", [
            {"ft": "hold", "hid": B.new_id("HD", 3, r, taken_ids, True), "noun": noun, "eid": eid,
             "placed": hd[0], "released": None, "scope": r.choice(card["units"])}]))
    qk = "ag2_decision" if plan["kind"] == "ag2d" else "qr_decision"
    q = _q(plan, card, qk=qk, matter=matter, unit=unit, date=Dq.isoformat())
    doc = {"card": card, "sections": sections, "query": q, "case": None, "title": f"{card['org']} {card['doc_noun']}"}
    return _finish_lc(doc, dec, plan)


# ================================================================================================ holds / conditions (AG-1)
def lc_holds(card, pack, plan, seed):
    """plan: ft hold|lcond, value g (count, gold 1-8), n_dec 2|3, shown, nm_kinds subset of {R, I}."""
    c = Ctx(card, pack, seed)
    r = c.r
    ft = plan["ft"]
    unit = r.choice(card["units"])
    others = [u for u in card["units"] if u != unit]
    taken = set()
    eid = _entity(c, taken)
    noun = card["item"]
    Dq = B.add_days(c.base, r.randint(600, 800))
    taken_d = {Dq.isoformat()}
    g, nd = plan["value"], plan["n_dec"]
    if g < nd:
        return None
    pre = "HD" if ft == "hold" else "CN"

    def item(e, scope, active=True, future=False):
        if future:
            st = B.add_days(Dq, r.randint(1, 120)).isoformat()
            en = None
        else:
            ds = _dates(c, 0, 590, 2, taken_d)
            st = ds[0]
            en = None if (active and r.random() < 0.6) else (B.add_days(Dq, r.randint(1, 150)).isoformat()
                                                            if active else ds[1])
        if en in taken_d or st in taken_d - {st}:
            pass
        taken_d.add(st)
        if en:
            taken_d.add(en)
        iid = B.new_id(pre, 3, r, taken, digits_only=True)
        if ft == "hold":
            return {"ft": "hold", "hid": iid, "noun": noun, "eid": e, "placed": st, "released": en, "scope": scope}
        return {"ft": "lcond", "cnd": iid, "noun": noun, "eid": e, "imposed": st,
                "end": None if en is None else [r.choice(["met", "waived"]), en], "scope": scope}
    split = sorted(r.sample(range(1, g), nd - 1)) if nd > 1 else []
    sizes = [b - a for a, b in zip([0] + split, split + [g])]
    sections, dec = [], []
    for k in sizes:
        fs = [item(eid, unit) for _ in range(k)]
        if r.random() < 0.3:
            fs.insert(r.randrange(len(fs) + 1), item(eid, unit, active=False))
        r.shuffle(fs)
        sections.append(_sec(c, r.choice(S2_HEADS), "decisive", fs))
        dec.append(sections[-1]["sid"])
    nm_pool = [x for x in plan["shown"] if x != g and x >= 1]
    for kind in plan["nm_kinds"]:
        if not nm_pool:
            return _why("lc ag1 pool")
        c2 = r.choice(nm_pool)
        if kind == "R":
            u2 = r.choice(others)
            sections.append(_sec(c, r.choice(S2_HEADS), "near_miss", [item(eid, u2) for _ in range(c2)],
                                 nm={"kind": "R", "lc": True, "unit": u2}))
        else:
            e2 = B.lookalike(eid, r, taken)
            if e2 is None:
                return None
            taken.add(e2)
            sections.append(_sec(c, r.choice(S2_HEADS), "near_miss", [item(e2, unit) for _ in range(c2)],
                                 nm={"kind": "I", "lc": True, "field": "eid", "id": e2}))
    for _ in range(r.randint(1, 2)):
        sections.append(_sec(c, r.choice(S2_HEADS), "other", [item(eid, unit, active=False)] +
                             ([item(eid, unit, future=True)] if r.random() < 0.4 else [])))
    sections += _filler(c, unit, eid, taken)
    q = _q(plan, card, skill="QR", qk="ag1_hold" if ft == "hold" else "ag1_cond", noun=noun, eid=eid, unit=unit,
           date=Dq.isoformat())
    doc = {"card": card, "sections": sections, "query": q, "case": None, "title": f"{card['org']} {card['doc_noun']}"}
    return _finish_lc(doc, dec, plan)


# ================================================================================================ action items (S6)
def _ai(c, aid, Dq, holder_at, people, taken_d, open_at=True, transfer=None):
    """An action item whose state at Dq is open with holder `holder_at` (open_at) or closed. Events on the item have
    distinct dates (SEM-57); only open items are transferred (F13R3-14)."""
    r = c.r
    n_ev = 1 + (1 if transfer is None and r.random() < 0.35 else 0) + (2 if r.random() < 0.25 else 0)
    ds = _dates(c, 0, 590, 5, taken_d)
    if ds is None:
        return None
    ev = []
    do_tr = transfer if transfer is not None else (r.random() < 0.35)
    first = r.choice([p for p in people if p != holder_at]) if do_tr else holder_at
    ev.append(["assigned", first, ds[0]])
    i = 1
    if do_tr:
        ev.append(["transferred", holder_at, ds[i]])
        i += 1
    if n_ev >= 3:
        ev.append(["closed", None, ds[i]])
        ev.append(["reopened", None, ds[i + 1]])
        i += 2
    if not open_at:
        ev.append(["closed", None, ds[i]])
    elif r.random() < 0.3:
        ev.append(["closed", None, B.add_days(Dq, r.randint(1, 90)).isoformat()])
    return {"ft": "aitem", "aid": aid, "events": ev}


def lc_holder(card, pack, plan, seed):
    """Holder Q-R: plan value = gold holder, shown people, nm_kinds [I] (look-alike action item ID)."""
    c = Ctx(card, pack, seed)
    r = c.r
    unit = r.choice(card["units"])
    people = card["holders"]
    Dq = B.add_days(c.base, r.randint(600, 800))
    taken_d = {Dq.isoformat()}
    taken = set()
    aid = B.new_id("AC", 3, r, taken, digits_only=True)
    g = plan["value"]
    f = _ai(c, aid, Dq, g, people, taken_d)
    if f is None:
        return None
    sections = [_sec(c, r.choice(S6_MEMO), "decisive", [f], scope=unit)]
    dec = [sections[0]["sid"]]
    pool = [p for p in plan["shown"] if p != g]
    if "I" in plan["nm_kinds"]:
        a2 = B.lookalike(aid, r, taken)
        if a2 is None or not pool:
            return None
        taken.add(a2)
        f2 = _ai(c, a2, Dq, _nm_out(plan, g, pool, r)(), people, taken_d)
        if f2 is None:
            return None
        sections.append(_sec(c, r.choice(S6_MEMO), "near_miss", [f2], scope=unit,
                             nm={"kind": "I", "lc": True, "field": "aid", "id": a2}))
    for _ in range(r.randint(1, 2)):
        a3 = B.new_id("AC", 3, r, taken, digits_only=True)
        f3 = _ai(c, a3, Dq, r.choice(people), people, taken_d, open_at=r.random() < 0.5)
        if f3:
            sections.append(_sec(c, r.choice(S6_MEMO), "other", [f3], scope=r.choice(card["units"])))
    sections += _filler(c, r.choice(card["units"]), _entity(c, taken), taken)
    q = _q(plan, card, qk="qr_holder", aid=aid, unit=unit, date=Dq.isoformat())
    doc = {"card": card, "sections": sections, "query": q, "case": None, "title": f"{card['org']} {card['doc_noun']}"}
    return _finish_lc(doc, dec, plan)


def lc_items(card, pack, plan, seed):
    """AG-1 open action items for committee X with holder H: value g, n_dec 2|3, nm_kinds [R]."""
    c = Ctx(card, pack, seed)
    r = c.r
    unit = r.choice(card["units"])
    others = [u for u in card["units"] if u != unit]
    people = card["holders"]
    H = r.choice(people)
    Dq = B.add_days(c.base, r.randint(600, 800))
    taken_d = {Dq.isoformat()}
    taken = set()
    g, nd = plan["value"], plan["n_dec"]
    if g < nd:
        return None
    split = sorted(r.sample(range(1, g), nd - 1)) if nd > 1 else []
    sizes = [b - a for a, b in zip([0] + split, split + [g])]
    sections, dec = [], []

    def new(holder, open_at=True, scope=None):
        return _ai(c, B.new_id("AC", 3, r, taken, digits_only=True), Dq, holder, people, taken_d, open_at=open_at)
    for k in sizes:
        fs = [new(H) for _ in range(k)]
        if r.random() < 0.5:
            fs.append(new(r.choice([p for p in people if p != H])))
        if r.random() < 0.3:
            fs.append(new(H, open_at=False))
        if any(x is None for x in fs):
            return None
        r.shuffle(fs)
        sections.append(_sec(c, r.choice(S6_MEMO), "decisive", fs, scope=unit))
        dec.append(sections[-1]["sid"])
    nm_pool = [x for x in plan["shown"] if x != g and x >= 1]
    if "R" in plan["nm_kinds"]:
        if not nm_pool:
            return None
        u2 = r.choice(others)
        fs = [new(H) for _ in range(r.choice(nm_pool))]
        if any(x is None for x in fs):
            return None
        sections.append(_sec(c, r.choice(S6_MEMO), "near_miss", fs, scope=u2,
                             nm={"kind": "R", "lc": True, "unit": u2}))
    fo = [new(r.choice([p for p in people if p != H])) for _ in range(r.randint(1, 2))]
    if any(x is None for x in fo):
        return None
    sections.append(_sec(c, r.choice(S6_MEMO), "other", fo, scope=unit))
    sections += _filler(c, r.choice(card["units"]), _entity(c, taken), taken)
    q = _q(plan, card, qk="ag1_items", holder=H, unit=unit, date=Dq.isoformat())
    doc = {"card": card, "sections": sections, "query": q, "case": None, "title": f"{card['org']} {card['doc_noun']}"}
    return _finish_lc(doc, dec, plan)
