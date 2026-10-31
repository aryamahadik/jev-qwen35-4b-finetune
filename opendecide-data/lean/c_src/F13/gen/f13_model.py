"""F13 document model + SOLVER A (structure side; G0 section 5). Reads the model, never text.

Model (plain dicts, JSON-able):
  doc   = {"card": card, "sections": [sec, ...], "query": q, "case": case | None (case in the question)}
  sec   = {"sid", "heading", "kind", "scope": unit | None (section-level mark), "role": decisive|near_miss|other|inert,
           "facts": [fact, ...], "trace": None | {"label", "scope_label", "cls": TI|TB|TD, "type", "unit"}}
  facts ("ft"):
    rule    {rid, vid, rev, scope, status, eff: date|None, end: ["none"] | ["through", d] | ["repealed", d],
             conds: [atom], join: all|any, outcome, form: clause|amend, amends: vid|None}
    effreg  {vid, rid, eff}                      K1: the only statement of a version's effective date (register)
    void    {target: vid|eid}                    K2: "Correction: <x> is void." (acts on the named item)
    exc     {eid, rid, conds, join, scope, status, eff, end}
    case    {cid, attrs: {name: value | TRACE}, scope, gdate}     (case record section; also doc["case"])
    inert   {kind, text, traced: bool}
  atom = {"attr", "op": ge|le|gt|lt|eq, "val"}; TRACE = {"trace": "value"} as an attribute value.
  query q = {"skill": QP|QR|QT|QD, "qk": qp_outcome|qr_version|ag1_exc|ag2_version|..., "form": choice|yn|establish|
             settle|inverted, "neg": 0|1|2, "inner_neg": bool, "case_ref": cid|None, "unit", "date", "rid",
             "claim": {...} (yn/establish/settle: the slotted value), "shown": [values] (choice), "abstain": NEI|NONE}
Answers: core value (outcome name, version id, count) or CONFLICT; over completions a set. Option-level answer:
  test_answer(doc) -> ("val", v) | ("abstain",) | ("yes",) | ("no",) | ("claim", True|False|None) (settle rows).
"""
from __future__ import annotations

import copy
import datetime as dt
import itertools

TRACE = "__TRACE__"
LC_QK = ("qr_decision", "ag2_decision", "ag1_hold", "ag1_cond", "qr_holder", "ag1_items")
LG_QK = ("lg_version", "ag2_config", "lg_status", "lg_count", "ag3_lcount")
TB_QK = ("tq_count", "tq_argmax", "tq_cmp", "tq_crit", "tq_set", "ag3_sum", "ag3_count", "tp_outcome", "ag1_excl")
CONFLICT = "__CONFLICT__"
UNDET = "__UNDET__"
OPS = {"ge": lambda a, b: a >= b, "le": lambda a, b: a <= b, "gt": lambda a, b: a > b, "lt": lambda a, b: a < b,
       "eq": lambda a, b: a == b}


def d_(x):
    return x if (x is None or isinstance(x, dt.date)) else dt.date.fromisoformat(x)


# ------------------------------------------------------------------------------------------------ windows / versions
def window_in_force(eff, end, status, on: dt.date) -> bool:
    """SEM-16 / SEM-27 / SEM-29 / SEM-34: in force on `on` (end of day)."""
    if status != "in force" or eff is None:
        return False
    eff = d_(eff)
    if eff > on:
        return False
    if end[0] == "through" and on > d_(end[1]):
        return False
    if end[0] == "repealed" and on >= d_(end[1]):
        return False
    return True


def all_facts(doc, ft=None):
    for s in doc["sections"]:
        for f in s["facts"]:
            if ft is None or f["ft"] == ft:
                yield f


def voided(doc) -> set:
    return {f["target"] for f in all_facts(doc, "void")}


def eff_of(doc, v) -> dt.date | None:
    if v.get("eff") is not None:
        return d_(v["eff"])
    regs = [d_(f["eff"]) for f in all_facts(doc, "effreg") if f["vid"] == v["vid"]]
    return regs[0] if len(regs) == 1 else None


def version_in_force(doc, rid, on, unit) -> dict | None:
    """SEM-35 / SEM-23 / SEM-28 / SEM-61: the version of rule `rid` that took effect most recently on or before `on`,
    among versions that apply to `unit` (no mark, or marked for it); void / draft / proposed never take effect."""
    vo = voided(doc)
    best = None
    for v in all_facts(doc, "rule"):
        if v["rid"] != rid or v["vid"] in vo:
            continue
        if v["scope"] is not None and v["scope"] != unit:
            continue
        e = eff_of(doc, v)
        if not window_in_force(e, v["end"], v["status"], on):
            continue
        key = (e, v["rev"])
        if best is None or key > best[0]:
            best = (key, v)
    return best[1] if best else None


def rule_ids(doc) -> list:
    seen = []
    for v in all_facts(doc, "rule"):
        if v["rid"] not in seen:
            seen.append(v["rid"])
    return seen


# ------------------------------------------------------------------------------------------------ conditions
def eval_conds(conds, join, attrs) -> bool:
    vals = []
    for a in conds:
        x = attrs.get(a["attr"])
        if x is None:
            raise KeyError(f"attribute {a['attr']} absent (attribute presence, F13R1-07)")
        vals.append(OPS[a["op"]](x, a["val"]))
    return all(vals) if join == "all" else any(vals)


# ------------------------------------------------------------------------------------------------ Q-P engine
def qp_outcome(doc, case) -> str:
    """Solver A Q-P (G0 5): scope filter, version resolution, exceptions as switches (SEM-25), forward firing,
    precedence (SEM-24), default outcome (SEM-54). Returns an outcome name or CONFLICT."""
    card = doc["card"]
    g, unit, attrs = d_(case["gdate"]), case["scope"], case["attrs"]
    vo = voided(doc)
    off = set()
    excs = [e for e in all_facts(doc, "exc") if e["eid"] not in vo]
    active = [e for e in excs if (e["scope"] is None or e["scope"] == unit)
              and window_in_force(e["eff"], e["end"], e["status"], g) and eval_conds(e["conds"], e["join"], attrs)]
    act_ids = {e["eid"] for e in active}
    switched_exc = {e["rid"] for e in active if e["rid"] in act_ids}  # exception naming an exception (1 level)
    for e in active:
        if e["eid"] in switched_exc:
            continue
        off.add(e["rid"])
    fired = []
    for rid in rule_ids(doc):
        if rid in off:
            continue
        v = version_in_force(doc, rid, g, unit)
        if v is None:
            continue
        if eval_conds(v["conds"], v["join"], attrs):
            fired.append(v)
    if not fired:
        return card["default"]
    if card["precedence"] == "specific":
        marked = [v for v in fired if v["scope"] == unit]
        tier = marked if marked else fired
        outs = {v["outcome"] for v in tier}
        return tier[0]["outcome"] if len(outs) == 1 else CONFLICT
    best = max(eff_of(doc, v) for v in fired)
    top = [v for v in fired if eff_of(doc, v) == best]
    outs = {v["outcome"] for v in top}
    return top[0]["outcome"] if len(outs) == 1 else CONFLICT


def case_of(doc) -> dict | None:
    q = doc["query"]
    if q.get("case_ref"):
        for f in all_facts(doc, "case"):
            if f["cid"] == q["case_ref"]:
                return f
        return None
    return doc.get("case")


# ------------------------------------------------------------------------------------------------ AG engines
def exc_active(doc, e, on) -> bool:
    return e["eid"] not in voided(doc) and window_in_force(e["eff"], e["end"], e["status"], on)


def ag1_exc(doc, unit, on) -> int:
    """SEM-33 / SEM-34: count exceptions marked for `unit` that are active on `on` (one statement per item, A58)."""
    return sum(1 for e in all_facts(doc, "exc") if e["scope"] == unit and exc_active(doc, e, on))


# ------------------------------------------------------------------------------------------------ core + completions
def core(doc):
    """The semantic answer of the row's query on a trace-free (completed) model."""
    q = doc["query"]
    qk = q["qk"]
    if qk in LC_QK:
        import f13_lc
        return f13_lc.lc_core(doc)
    if qk in TB_QK:
        import f13_tab
        return f13_tab.tab_core(doc)
    if qk in LG_QK:
        import f13_log
        return f13_log.log_core(doc)
    if qk == "qp_outcome":
        c = case_of(doc)
        return UNDET if c is None else qp_outcome(doc, c)
    if qk == "qp_inverted":
        meets = []
        for c in q["cases"]:
            v = version_in_force(doc, q["rid"], d_(c["gdate"]), c["scope"])
            meets.append(bool(v) and eval_conds(v["conds"], v["join"], c["attrs"]))
        return tuple(meets)
    if qk in ("qr_version", "ag2_version"):
        v = version_in_force(doc, q["rid"], d_(q["date"]), q["unit"])
        return v["vid"] if v else UNDET
    if qk == "ag1_exc":
        return ag1_exc(doc, q["unit"], d_(q["date"]))
    raise ValueError(f"unknown query kind {qk}")


def _crit(vals, lo=0):
    pts = set()
    for v in vals:
        for x in (v - 1, v, v + 1):
            if x >= lo:
                pts.add(x)
    pts.add(lo)
    pts.add((max(vals) if vals else 0) + 100)
    return sorted(pts)


def completions(doc):
    """Every completion class of the row's traces (G0 2.4 'exact finite check'): value traces on numeric case
    attributes take each critical point of the predicates that read them (and neighbours, below / above); part
    traces T-D take {empty, original content} (witness pair, MR8 logic); T-I / T-B parts take {empty} (benign by
    their closed labels / SEM-30). Yields completed copies."""
    slots = []
    cases = [f for f in all_facts(doc, "case")] + ([doc["case"]] if doc.get("case") else [])
    preds = [(a["attr"], a["val"]) for f in list(all_facts(doc, "rule")) + list(all_facts(doc, "exc"))
             for a in f["conds"] if isinstance(a["val"], (int, float))]
    for ci, c in enumerate(cases):
        for k, v in c["attrs"].items():
            if v == TRACE:
                pts = _crit([val for (a, val) in preds if a == k])
                slots.append(("attr", ci, k, pts))
    for si, s in enumerate(doc["sections"]):
        if s.get("trace") and s["trace"]["cls"] == "TD":
            extra = []
            if doc["query"]["qk"] in LC_QK:
                import f13_lc
                extra = f13_lc.lc_witness(doc, s)
            elif doc["query"]["qk"] in LG_QK:
                import f13_log
                extra = f13_log.log_witness(doc, s)
            slots.append(("part", si, None, [False, True] + extra))
    if doc["query"]["qk"] in TB_QK:
        import f13_tab
        for d1 in _completions0(doc, slots):
            yield from f13_tab.tab_completions(d1)
        return
    yield from _completions0(doc, slots)


def _completions0(doc, slots):
    if not slots:
        yield doc
        return
    for combo in itertools.product(*[sl[3] for sl in slots]):
        d2 = copy.deepcopy(doc)
        cases2 = [f for f in all_facts(d2, "case")] + ([d2["case"]] if d2.get("case") else [])
        for sl, val in zip(slots, combo):
            if sl[0] == "attr":
                cases2[sl[1]]["attrs"][sl[2]] = val
            elif isinstance(val, dict):
                d2["sections"][sl[1]]["facts"] = copy.deepcopy(val["facts"])
                d2["sections"][sl[1]]["scope"] = val["scope"]
            elif val:
                sx = d2["sections"][sl[1]]
                sx["facts"] = sx["trace"]["original"]
                if sx["trace"].get("orig_scope"):
                    sx["scope"] = sx["trace"]["orig_scope"]
                if sx["trace"].get("orig_mdate"):
                    sx["mdate"] = sx["trace"]["orig_mdate"]
                if sx["trace"].get("orig_period"):
                    sx["period"] = sx["trace"]["orig_period"]
        yield d2


def answers(doc) -> set:
    out = set()
    for d2 in completions(doc):
        try:
            out.add(core(d2))
        except KeyError:
            out.add(CONFLICT)
    return out


# ------------------------------------------------------------------------------------------------ option-level answer
AMB_T, AMB_F = "__AMB_TRUE__", "__AMB_FALSE__"


def claim_truths(doc, cv):
    """Per-completion truth of the inner claim on a tq_argmax row (G2 fix r1, 6 Oct; SEM-04, SEM-22, F13R2-13): a
    completion with an answer gives answer == cv; one whose tie rule cannot split the top records gives False when the
    claimed record is not among them (it is below a stated value in every such completion), else None; a completion
    with no selection gives None."""
    import f13_tab
    out = set()
    for d2 in completions(doc):
        try:
            a = core(d2)
        except KeyError:
            a = CONFLICT
        if a not in (CONFLICT, UNDET):
            out.add(a == cv)
        else:
            top = f13_tab.tab_argmax_top(d2)
            out.add(False if top is not None and cv not in top else None)
    return out


def claim_truth(A, det, v, cv, doc=None):
    """Inner claim truth value over the completions (SEM-04, F13R2-13; G2 fix 6 Oct): True / False when the answer
    is determined; None when the witnesses give the claim both truth values (proven undetermined) or a completion has
    no answer (CONFLICT / UNDET); AMB_T / AMB_F when the answer is undetermined but the claim has one truth value in
    every enumerated completion (the witnesses cannot prove the claim determined: such rows are unusable)."""
    if det:
        return v == cv
    if A and (CONFLICT in A or UNDET in A) and doc is not None and doc["query"]["qk"] == "tq_argmax":
        # G2 fix r1: an unsplittable tie among other records leaves the answer open but not the claim
        ts = claim_truths(doc, cv)
        if None in ts or len(ts) == 2:
            return None
        return AMB_T if ts == {True} else AMB_F
    if not A or CONFLICT in A or UNDET in A:
        return None
    ts = {a == cv for a in A}
    if len(ts) == 2:
        return None
    return AMB_T if ts == {True} else AMB_F


def option_answer(doc):
    """Map the answer set to the row's answer (G0 2.2 'answer in these tests')."""
    q = doc["query"]
    A = answers(doc)
    det = len(A) == 1 and CONFLICT not in A and UNDET not in A
    v = next(iter(A)) if det else None
    form = q["form"]
    if form == "inverted":
        if not det:
            # open NEI: no listed case shown to meet the rule (each case solved separately)
            per = [set(a[i] for a in A) for i in range(len(q["cases"]))]
            if any(p == {True} for p in per):
                return ("val", [i for i, p in enumerate(per) if p == {True}][0]) if \
                    sum(p == {True} for p in per) == 1 else ("bad",)
            return ("abstain",)
        hits = [i for i, m in enumerate(v) if m]
        if len(hits) == 1:
            return ("val", hits[0])
        if not hits:
            return ("abstain",) if q["abstain"] == "NONE" else ("bad",)
        return ("bad",)
    if form == "choice":
        if not det:
            return ("abstain",) if q["abstain"] == "NEI" else ("bad",)
        if v in q["shown"]:
            return ("val", v)
        return ("abstain",) if q["abstain"] == "NONE" else ("bad",)
    claim = q["claim"]
    truth = claim_truth(A, det, v, claim["value"], doc)
    if truth in (AMB_T, AMB_F):
        # G2 fix (SEM-04, F13R2-13): settle / establish gold is the inner claim's truth value, which the witness
        # completions leave unproven here; only "establish" on a claim false in every witness is safe ("no" either way)
        if form == "establish" and not q.get("inner_neg") and truth == AMB_F:
            truth = None
        else:
            return ("bad",)
    if form == "yn":
        if not det:
            return ("bad",)
        t = truth if q.get("neg", 0) % 2 == 0 else (not truth)
        return ("yes",) if t else ("no",)
    if form == "establish":
        t = truth
        if q.get("inner_neg"):
            t = None if truth is None else (not truth)
        est = t is True
        if q.get("neg", 0) % 2 == 1:
            est = not est
        return ("yes",) if est else ("no",)
    if form == "settle":
        return ("claim", truth)
    raise ValueError(form)


def row_answer(doc):
    """Gold-level answer: settle rows -> yes iff settled (frame negation flips)."""
    a = option_answer(doc)
    if a[0] == "claim":
        settled = a[1] is not None
        if doc["query"].get("neg", 0) % 2 == 1:
            settled = not settled
        return ("yes",) if settled else ("no",)
    return a


# ------------------------------------------------------------------------------------------------ deletion set (2.2)
def without(doc, sids) -> dict:
    d2 = copy.deepcopy(doc)
    d2["sections"] = [s for s in d2["sections"] if s["sid"] not in sids]
    return d2


def decisive_set(doc) -> list:
    """D = every section whose deletion alone changes the test answer or makes it undetermined (case records are
    decisive by construction and skipped). On settle rows the test answer is the inner claim's truth value."""
    base = option_answer(doc)
    out = []
    cref = doc["query"].get("case_ref")
    for s in doc["sections"]:
        if s["kind"] == "case_record" and cref and any(f.get("cid") == cref for f in s["facts"]):
            out.append(s["sid"])
            continue
        if s["role"] == "inert" and not any(f["ft"] != "inert" for f in s["facts"]):
            continue
        a = option_answer(without(doc, {s["sid"]}))
        if a != base or a[0] == "bad":
            out.append(s["sid"])
    return out


def sufficient(doc, D) -> bool:
    keep = set(D)
    return option_answer(without(doc, {s["sid"] for s in doc["sections"] if s["sid"] not in keep})) == \
        option_answer(doc)


# ------------------------------------------------------------------------------------------------ NM activation (2.3)
def activate(doc, sid) -> dict:
    """The one operator per near-miss kind (F13R2-20). The section's `nm` = {kind: V|R|I, sub, ...}."""
    d2 = copy.deepcopy(doc)
    sec = next(s for s in d2["sections"] if s["sid"] == sid)
    nm = sec["nm"]
    if nm.get("lc"):
        import f13_lc
        f13_lc.lc_activate(d2, sec, nm)
        return d2
    if nm.get("tab"):
        import f13_tab
        f13_tab.tab_activate(d2, sec, nm)
        return d2
    if nm.get("log"):
        import f13_log
        f13_log.log_activate(d2, sec, nm)
        return d2
    if nm["kind"] == "V":
        f = next(x for x in sec["facts"] if x.get("vid") == nm["vid"] or x.get("eid") == nm.get("eid"))
        if nm["sub"] == "void_entry":
            for s in d2["sections"]:
                s["facts"] = [x for x in s["facts"] if not (x["ft"] == "void" and x["target"] == nm["vid"])]
        else:
            f["status"] = "in force"
            if nm.get("new_eff") is not None:
                f["eff"] = nm["new_eff"]
            if nm.get("new_end") is not None:
                f["end"] = nm["new_end"]
    elif nm["kind"] == "R":
        q = d2["query"]
        if q.get("case_ref") or d2.get("case"):
            c = case_of(d2)
            c["scope"] = nm["unit"]
        else:
            q["unit"] = nm["unit"]
    elif nm["kind"] == "I":
        d2["query"]["case_ref"] = nm["id"]
    return d2


def nm_functional(doc, sid) -> bool:
    """MR4: activation gives a different, valid answer, and the activated section is then decisive (its content
    produces the new answer: deleting it from the activated document changes that answer)."""
    a0 = option_answer(doc)
    d1 = activate(doc, sid)
    a1 = option_answer(d1)
    if a1 == a0 or a1[0] == "bad":
        return False
    return option_answer(without(d1, {sid})) != a1
