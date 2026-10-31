"""F13 samplers (G0 section 4). S1 manual / SOP (forward) implemented; S2, S3, S4, S6, S5 follow the same contract.

Contract: make_card(pack, sampler, idx, split) -> card; draw(card, pack, plan, seed) -> doc model (f13_model) with
sections carrying role / nm / trace, or None (rejected; the caller redraws). Every returned doc already satisfies:
solver A answer == plan gold class, A's single-deletion set == planned decisive sections, sufficiency, every
near-miss functional (activation gives a shown, different answer). Layout (deciles, inert fill) is f13_layout's job.
"""
from __future__ import annotations

import datetime as dt

import f13_base as B
import f13_model as M
import f13_text as T

ROLES_DEFS = ("handled by the {r}", "sent to the {r} for action", "logged for the {r}", "returned to the {r}",
              "passed to the {r} for sign-off", "kept with the {r}")


# ------------------------------------------------------------------------------------------------ cards
def make_card(pack: dict, sampler: str, idx: int, split: str) -> dict:
    r = B.rng("f13-card", pack["pack_id"], sampler, idx)
    world = "open" if idx % 2 == 0 else "closed"
    units = pack["units"][: r.choice([3, 4])] if len(pack["units"]) >= 4 else pack["units"][:3]
    nums = [a for a in pack["nums"] if a["name"] != pack["scope_kind"]][:6]
    outs = pack["outsets"][idx % len(pack["outsets"])]
    item = pack["ents"][0]["noun"]
    roles = pack["roles"] or ["coordinator", "supervisor", "clerk", "reviewer"]
    defs = {o: ("the " + item + " is " + ROLES_DEFS[i % len(ROLES_DEFS)].format(r=roles[i % len(roles)]))
            for i, o in enumerate(outs)}
    ds = ("one_line", "one_line_examples", "one_line_examples", "decision_list", "one_line", "one_line_examples",
          "one_line", "one_line_examples", "decision_list", "one_line_examples")[idx % 10]
    var = {"one_line": ["DV01", "DV02", "DV03", "DV05"], "one_line_examples": ["DV11", "DV12", "DV14", "DV16"],
           "decision_list": ["DV35"]}[ds]
    wd = B.wordings()
    w_ids = [w["id"] for w in r.sample(wd, 6)]
    if pack.get("date_window"):
        base = dt.date.fromisoformat(pack["date_window"][0])
    else:
        base = dt.date(r.randint(2041, 2049), r.randint(1, 12), 1)
    card = {"card_id": f"F13-{sampler}-c{idx:02d}" if split != "s5" else f"F13-S5-c{idx:02d}", "sampler": sampler,
            "pack_id": pack["pack_id"], "persona_seed": pack["persona_seed"], "org": pack["org"],
            "doc_noun": "procedures manual", "world": world, "scope_kind": pack["scope_kind"], "units": units,
            "item": item, "attrs": nums, "attr_units": {a["name"]: a["unit"] for a in nums}, "outcomes": outs,
            "default": outs[(idx // 2) % len(outs)], "defs": defs, "defs_style": ds,
            "defs_variant": var[idx % len(var)], "precedence": ("specific", "later")[(idx // 3) % 2],
            "date_form": B.DATE_FORMATS[idx % 3], "marker": T.MARKERS[idx % 3], "gname": f"{item} date",
            "base_date": base.isoformat(), "wordings": w_ids, "inverted": idx in (3, 6) and sampler in ("S1", "S2", "S6"),  # r5: 6 of 45 cards, 3 open + 3 closed
            "few_shot": None, "fewshot_template": None, "examples": {},
            "fact_kinds": ["rule", "amendment", "exception", "version"],
            "scoped_kinds": ["rule", "version", "amendment", "exception"], "ops": {"ge", "le", "gt", "lt"},
            "has_or": True, "has_case": True, "has_establish": world == "open", "has_settle": world == "open",
            "roles": roles, "people": pack["people"] or roles}
    if ds == "one_line_examples":
        card["examples"] = card_examples(card, r)
    return card


def card_examples(card, r) -> dict:
    """1-2 worked examples per outcome: a mini rule + case, labelled by solver A (A67); never a row structure."""
    out = {}
    a = card["attrs"][0]
    for o in card["outcomes"]:
        t = r.randint(a["lo"] + 5, a["hi"] - 5)
        v = t + r.randint(1, 4)
        rule = {"ft": "rule", "rid": "R-00", "vid": "R-00.1", "rev": 1, "scope": None, "status": "in force",
                "eff": card["base_date"], "end": ["none"], "conds": [{"attr": a["name"], "op": "gt", "val": t}],
                "join": "all", "outcome": o, "form": "clause", "amends": None}
        doc = {"card": card, "sections": [{"sid": "x", "kind": "chapter", "role": "decisive", "facts": [rule]}],
               "query": {"qk": "qp_outcome", "form": "choice", "shown": card["outcomes"], "abstain": "NONE"},
               "case": {"attrs": {a["name"]: v}, "scope": card["units"][0], "gdate": card["base_date"]}}
        assert M.option_answer(doc) == ("val", o)
        out[o] = [f"under a rule 'if the {a['name']} is more than {T.amount(t, a['unit'])}, the outcome is {o}', "
                  f"a {card['item']} with {a['name']} {T.amount(v, a['unit'])} gets {o}"]
    return out


FEWSHOT_TEMPLATES = ("FT01", "FT11", "FT12", "FT05")


def card_fewshot(card, r) -> list:
    """repair r3 (G0 10 Cards, F13R1-25, F13R5-A1): the few-shot overlay, 2 worked excerpts (each far under 300
    tokens): a mini rule + case labelled by solver A, answer = outcome name (card_ir renders it per row)."""
    a = card["attrs"][0]
    out = []
    for o in r.sample(card["outcomes"], 2):
        t = r.randint(a["lo"] + 5, a["hi"] - 5)
        v = t + r.randint(1, 4)
        rule = {"ft": "rule", "rid": "R-00", "vid": "R-00.1", "rev": 1, "scope": None, "status": "in force",
                "eff": card["base_date"], "end": ["none"], "conds": [{"attr": a["name"], "op": "gt", "val": t}],
                "join": "all", "outcome": o, "form": "clause", "amends": None}
        doc = {"card": card, "sections": [{"sid": "x", "kind": "chapter", "role": "decisive", "facts": [rule]}],
               "query": {"qk": "qp_outcome", "form": "choice", "shown": card["outcomes"], "abstain": "NONE"},
               "case": {"attrs": {a["name"]: v}, "scope": card["units"][0], "gdate": card["base_date"]}}
        assert M.option_answer(doc) == ("val", o)
        out.append({"case": f"Worked example: under a rule 'if the {a['name']} is more than {T.amount(t, a['unit'])}, the "
                            f"outcome is {o}', a {card['item']} has {a['name']} {T.amount(v, a['unit'])}.",
                    "answer": o})
    return out


# ------------------------------------------------------------------------------------------------ S1 helpers
class Ctx:
    def __init__(self, card, pack, seed):
        self.card, self.pack, self.r = card, pack, B.rng("f13-row", card["card_id"], seed)
        self.base = dt.date.fromisoformat(card["base_date"])
        self.ids = set()
        self.rule_no = self.r.randint(11, 40)
        self.sec_no = 0

    def date(self, lo, hi):
        return B.add_days(self.base, self.r.randint(lo, hi))

    def rid(self):
        self.rule_no += self.r.randint(1, 5)
        return f"R-{self.rule_no}"

    def sid(self):
        self.sec_no += 1
        return f"s{self.sec_no:02d}"


def rule(rid, rev, conds, join, outcome, eff, scope=None, status="in force", end=("none",), form="clause",
         amends=None):
    return {"ft": "rule", "rid": rid, "vid": f"{rid}.{rev}", "rev": rev, "scope": scope, "status": status,
            "eff": eff.isoformat() if isinstance(eff, dt.date) else eff, "end": list(end), "conds": conds,
            "join": join, "outcome": outcome, "form": form, "amends": amends}


def sec(c: Ctx, kind, role, facts, heading=None, **kw):
    hd = heading or {"chapter": "Chapter {n}: {o} work", "annex": "Annex {n}", "register": "Register of notices",
                     "bulletin": "Bulletin {n}", "case_record": "{I} file", "inert": "{d} notes"}[kind]
    o = c.r.choice(c.pack["objects"] or ["field"])
    d = c.r.choice(c.pack["doc_types"] or ["log sheet"])
    s = {"sid": c.sid(), "heading": hd.format(n=c.sec_no + 1, o=o.capitalize(), I=c.card["item"].capitalize(),
                                               d=d.capitalize()), "kind": kind, "scope": None, "role": role,
         "facts": facts, "trace": None}
    s.update(kw)
    return s


def true_atom(c: Ctx, a, v, boundary=False):
    """An atom on attribute a (case value v) that holds."""
    op = c.r.choice(["ge", "gt", "le", "lt"])
    if op == "ge":
        t = v if boundary else max(a["lo"], v - c.r.randint(1, 10))
    elif op == "le":
        t = v if boundary else min(a["hi"], v + c.r.randint(1, 10))
    elif op == "gt":
        t = v - 1 if boundary else max(a["lo"], v - c.r.randint(1, 10))
        t = min(t, v - 1)
    else:
        t = v + 1 if boundary else min(a["hi"] + 20, v + c.r.randint(1, 10))
        t = max(t, v + 1)
    return {"attr": a["name"], "op": op, "val": t}


def false_atom(c: Ctx, a, v):
    op = c.r.choice(["ge", "gt", "le", "lt"])
    if op in ("ge", "gt"):
        t = v + c.r.randint(1, 10)
    else:
        t = max(0, v - c.r.randint(1, 10))
        if t == v:
            op = "gt"
            t = v + 1
    return {"attr": a["name"], "op": op, "val": t}


# ------------------------------------------------------------------------------------------------ S1 Q-P
def s1_qp(card, pack, plan, seed):
    """plan: {form: choice|yn|establish|settle, gold_kind: val|abstain|yes|no, target: outcome or None, k, n_dec,
    case_loc: question|record, nm_kinds: [V|R|I], neg, inner_neg, claim_true}. Returns doc or None."""
    c = Ctx(card, pack, seed)
    r = c.r
    outs = card["outcomes"]
    attrs = card["attrs"]
    if len(attrs) < 2:
        return None
    unit = r.choice(card["units"])
    G = c.date(300, 700)
    case_attrs = {a["name"]: r.randint(a["lo"] + 2, a["hi"] - 2) for a in r.sample(attrs, min(len(attrs), r.randint(
        3, 5)))}
    anames = list(case_attrs)
    ameta = {a["name"]: a for a in attrs}
    gold_out = plan["target"]
    sections = []
    dec = []
    # decisive rule (or exception switching off a competing rule when gold = default)
    rid = c.rid()
    a0 = ameta[anames[0]]
    boundary = r.random() < 0.25
    conds = [true_atom(c, a0, case_attrs[a0["name"]], boundary)]
    join = "all"
    if r.random() < 0.4:
        a1 = ameta[anames[1]]
        if r.random() < 0.5:
            conds.append(true_atom(c, a1, case_attrs[a1["name"]]))
        else:
            conds.append(false_atom(c, a1, case_attrs[a1["name"]]))
            join = "any"
    eff0 = c.date(0, 200)
    use_k1 = plan["n_dec"] >= 2 and plan["case_loc"] == "question" or plan["n_dec"] == 3
    dscope = unit if r.random() < 0.35 else None
    other_out = [o for o in outs if o != card["default"]]
    z = None
    if plan["form"] != "choice" and plan["claim_value"] != gold_out:
        z = plan["claim_value"]
    if plan.get("force_scope") or (z and z != card["default"] and card["precedence"] == "specific"):
        dscope = unit
    if gold_out == card["default"]:
        # a competing rule fires with another outcome but an exception switches it off for this case
        o_r = z if z else r.choice(other_out)
        rv = rule(rid, 1, conds, join, o_r, eff0, scope=dscope)
        eid = f"EX-{r.randint(100, 989)}"
        ex = {"ft": "exc", "eid": eid, "rid": rid, "conds": [true_atom(c, ameta[anames[-1]],
                                                                       case_attrs[anames[-1]])],
              "join": "all", "scope": dscope, "status": "in force", "eff": c.date(201, 290).isoformat(),
              "end": ["none"]}
        sections.append(sec(c, "chapter", "other", [rv]))
        sections.append(sec(c, "bulletin", "decisive", [ex]))
        dec.append(sections[-1]["sid"])
        dv = rv
        # the rule section is necessary too only if deleting it changes the answer: it does not (default stays)
        sections[-2]["role"] = "decisive_chain_other"
        # repair r10 L5 (G10 decisive count non-AG 1/2/3 = 50/35/15; this branch realised one exception whatever the
        # plan, so qp count-1 rows ran above plan): m competing rules that fire for the case, each switched off by
        # its own exception (keyed on a distinct case attribute), so deleting any one exception alone changes the
        # answer and every exception is in D (2.2); the rules stay decisive_chain_other. m = n_dec on case-in-question
        # rows, n_dec - 1 with a case record (the record is decisive). On yes/no forms every competitor carries the
        # claimed outcome z, so each deletion flips the claim.
        m = min(max(1, plan["n_dec"] - (1 if plan["case_loc"] == "record" else 0)), len(anames))
        eids = {eid}
        for i in range(1, m):
            a_r = ameta[r.choice(anames)]
            o_i = z if z else r.choice(other_out)
            rv_i = rule(c.rid(), 1, [true_atom(c, a_r, case_attrs[a_r["name"]])], "all", o_i, c.date(0, 200),
                        scope=dscope)
            eid_i = f"EX-{r.randint(100, 989)}"
            while eid_i in eids:
                eid_i = f"EX-{r.randint(100, 989)}"
            eids.add(eid_i)
            a_e = anames[-1 - i]
            ex_i = {"ft": "exc", "eid": eid_i, "rid": rv_i["rid"], "conds": [true_atom(c, ameta[a_e], case_attrs[a_e])],
                    "join": "all", "scope": dscope, "status": "in force", "eff": c.date(201, 290).isoformat(),
                    "end": ["none"]}
            sections.append(sec(c, "chapter", "decisive_chain_other", [rv_i]))
            sections.append(sec(c, "bulletin", "decisive", [ex_i]))
            dec.append(sections[-1]["sid"])
    else:
        if use_k1:
            rv = rule(rid, 1, conds, join, gold_out, None, scope=dscope)
            sections.append(sec(c, "chapter", "decisive", [rv]))
            dec.append(sections[-1]["sid"])
            reg = {"ft": "effreg", "vid": rv["vid"], "rid": rid, "eff": eff0.isoformat()}
            sections.append(sec(c, "register", "decisive", [reg]))
            dec.append(sections[-1]["sid"])
        else:
            rv = rule(rid, 1, conds, join, gold_out, eff0, scope=dscope)
            sections.append(sec(c, "chapter", "decisive", [rv]))
            dec.append(sections[-1]["sid"])
        dv = rv
    if z and gold_out != card["default"] and z != card["default"]:
        # an overridden competitor with the claimed outcome: deleting the decisive rule flips the claim (2.2)
        an = r.choice(anames)
        if card["precedence"] == "specific":
            ce = c.date(0, 250)
        else:
            if rv.get("eff") is None:
                ce = B.add_days(eff0, -r.randint(5, 60))
            else:
                ce = B.add_days(M.d_(rv["eff"]), -r.randint(5, 60))
        sections.append(sec(c, "chapter", "other", [rule(c.rid(), 1, [true_atom(c, ameta[an], case_attrs[an])], "all",
                                                         z, ce, scope=None)]))
    # case
    cid = None
    case = {"cid": None, "ft": "case", "attrs": dict(case_attrs), "scope": unit, "gdate": G.isoformat()}
    if plan["case_loc"] == "record":
        reg = next(e for e in pack["ents"])
        cid = B.new_id(reg["prefix"], 4, r, c.ids)
        case["cid"] = cid
        sections.append(sec(c, "case_record", "decisive", [case]))
        dec.append(sections[-1]["sid"])
    # other rules: conditions fail for the case (role other)
    for _ in range(r.randint(2, 5)):
        an = r.choice(anames)
        o = r.choice(outs)
        conds_o = [false_atom(c, ameta[an], case_attrs[an])]
        sc = r.choice([None, None, r.choice(card["units"])])
        sections.append(sec(c, "chapter" if sc is None else "annex", "other",
                            [rule(c.rid(), 1, conds_o, "all", o, c.date(0, 250), scope=sc)]))
    # near-misses
    shown = plan.get("shown") or outs
    alt = [o for o in shown if o != gold_out and o in outs]
    if plan["form"] != "choice":
        cv = plan["claim_value"]
        alt = [cv] if cv != gold_out else [o for o in outs if o != gold_out]
    for kind in plan["nm_kinds"]:
        if not alt:
            return None
        y = r.choice(alt)
        if kind == "V" and gold_out == card["default"]:
            # a separate clause that would fire for the case, not in force on the governing date
            sub = r.choice(["not_yet", "draft", "proposed", "void"])
            an = r.choice(anames)
            if sub == "not_yet":
                nv = rule(c.rid(), 1, [true_atom(c, ameta[an], case_attrs[an])], "all", y, B.add_days(G, r.randint(
                    1, 90)), scope=dscope)
                nm = {"kind": "V", "sub": sub, "vid": nv["vid"], "new_eff": B.add_days(G, -r.randint(1, 60)).isoformat()}
            else:
                nv = rule(c.rid(), 1, [true_atom(c, ameta[an], case_attrs[an])], "all", y, c.date(0, 250),
                          scope=dscope, status=sub)
                nm = {"kind": "V", "sub": sub, "vid": nv["vid"]}
            sections.append(sec(c, r.choice(["chapter", "bulletin"]), "near_miss", [nv], nm=nm))
        elif kind == "V":
            sub = r.choice(["not_yet", "draft", "proposed", "void"])
            e_new = c.date(301, 299 + 300) if sub == "not_yet" else None
            if sub == "not_yet":
                e_new = B.add_days(G, r.randint(1, 90))
            else:
                lo = M.d_(dv["eff"]) if dv.get("eff") else eff0
                span = (G - lo).days
                if span < 2:
                    return None
                e_new = B.add_days(lo, r.randint(1, span))
            st = {"draft": "draft", "proposed": "proposed", "void": "void"}.get(sub, "in force")
            nv = rule(dv["rid"], 2, dv["conds"], dv["join"], y, e_new, scope=dv["scope"], status=st, form="amend",
                      amends=dv["vid"])
            lo = M.d_(dv["eff"]) if dv.get("eff") else eff0
            new_eff = B.add_days(lo, max(1, (G - lo).days // 2)).isoformat()
            s = sec(c, r.choice(["bulletin", "register"]), "near_miss", [nv],
                    nm={"kind": "V", "sub": sub, "vid": nv["vid"], "new_eff": new_eff})
            sections.append(s)
        elif kind == "R":
            if y == card["default"] and dscope is not None:
                ys = [o for o in alt if o != card["default"]]
                if not ys or plan["form"] != "choice":
                    return None
                y = r.choice(ys)
            u2 = r.choice([u for u in card["units"] if u != unit])
            an = r.choice(anames)
            nr = rule(c.rid(), 1, [true_atom(c, ameta[an], case_attrs[an])], "all", y,
                      B.add_days(eff0, r.randint(5, 60)), scope=u2)
            sections.append(sec(c, "annex", "near_miss", [nr], nm={"kind": "R", "unit": u2}))
        elif kind == "I":
            if not cid:
                return None
            lid = B.lookalike(cid, r, c.ids)
            if lid is None:
                return None
            c.ids.add(lid)
            la = dict(case_attrs)
            # the look-alike record fails the decisive atom on a0; a y-rule on the complement fires for it only
            at = conds[0]
            t = at["val"]
            if at["op"] in ("ge", "gt"):
                la[at["attr"]] = max(0, (t if at["op"] == "ge" else t + 1) - r.randint(1, 6))
                yc = {"attr": at["attr"], "op": "lt", "val": t if at["op"] == "ge" else t + 1}
            else:
                la[at["attr"]] = (t if at["op"] == "le" else t - 1) + r.randint(1, 6)
                yc = {"attr": at["attr"], "op": "gt", "val": t if at["op"] == "le" else t - 1}
            yr = rule(c.rid(), 1, [yc], "all", y, B.add_days(eff0, r.randint(5, 60)), scope=None)
            if gold_out == card["default"]:
                return None
            sections.append(sec(c, "chapter", "other", [yr]))
            sections.append(sec(c, "case_record", "near_miss", [{"cid": lid, "ft": "case", "attrs": la,
                                                                 "scope": unit, "gdate": G.isoformat()}],
                                nm={"kind": "I", "id": lid}, heading="{I} file (copy)"))
        alt = [o for o in alt if o != y] or alt
    q = {"skill": "QP", "qk": "qp_outcome", "form": plan["form"], "neg": plan.get("neg", 0),
         "inner_neg": plan.get("inner_neg", False), "case_ref": cid, "shown": shown,
         "abstain": "NEI" if card["world"] == "open" else "NONE",
         "claim": {"value": plan.get("claim_value", gold_out)}}
    doc = {"card": card, "sections": sections, "query": q, "case": None if cid else case,
           "title": f"{card['org']} {card['doc_noun']}"}
    return finish(doc, dec, plan)


WHY = {}


def _why(k):
    WHY[k] = WHY.get(k, 0) + 1
    return None


def td_base(doc):
    """Repair r2 (G0 2.2 F13R1-23, 6 A64): the answerable base of a gold-abstain row made by a T-D trace is the same
    document with the T-D undone (the traced value or the replaced section restored; every other trace kept)."""
    td = doc.get("td")
    if not td or "orig" not in td:
        return doc
    import copy as _copy
    d = _copy.deepcopy(doc)
    d.pop("td", None)
    si = next((i for i, s in enumerate(d["sections"]) if s["sid"] == td["sid"]), None)
    if si is None:
        return doc
    if td["kind"] == "val" and "cell" in td:
        d["sections"][si]["facts"][0]["rows"][td["cell"][0]][td["cell"][1]] = td["orig"]
    elif td["kind"] == "val":
        d["sections"][si]["facts"][0]["attrs"][td["attr"]] = td["orig"]
    else:
        sec = _copy.deepcopy(td["orig"])
        sec["heading"] = d["sections"][si]["heading"]
        d["sections"][si] = sec
    return d


def role_doc(doc):
    """F13R1-23: role checks on a closed-world 'none of the listed' row run on its answerable base, where the
    answer is shown. Repair r2: on a T-D (gold-NEI / undetermined) row they run on the T-D base (td_base)."""
    if doc.get("td") and "orig" in doc["td"]:
        return td_base(doc)
    q = doc["query"]
    if q["qk"] == "qp_inverted" and doc.get("inv_base"):
        # repair r5 (G0 3.1 inverted rows): a closed 'None' row is its base with the gold case deleted
        cs = list(q["cases"])
        cs.insert(doc["inv_base"]["idx"], doc["inv_base"]["case"])
        return {**doc, "query": {**q, "cases": cs, "shown": list(range(len(cs)))}}
    if q["form"] == "choice" and q["abstain"] == "NONE":
        A = M.answers(doc)
        if len(A) == 1:
            v = next(iter(A))
            if v not in q["shown"] and v not in (M.CONFLICT, M.UNDET):
                return {**doc, "query": {**q, "shown": list(q["shown"]) + [v]}}
    return doc


def finish(doc, dec, plan):
    """Verify the planned roles with solver A; set role-less chain sections; return doc or None."""
    for s in doc["sections"]:
        if s["role"] == "decisive_chain_other":
            s["role"] = "other"
    A = M.answers(doc)
    if M.CONFLICT in A or M.UNDET in A:
        return _why("conflict/undet")
    if len(A) != 1:
        return _why("not determined")
    want = plan.get("target") if plan.get("kind", "qp") == "qp" else None
    if want is not None and next(iter(A)) != want:
        return _why("target")
    if M.option_answer(doc)[0] == "bad":
        return _why("bad")
    rd = role_doc(doc)
    D = M.decisive_set(rd)
    if sorted(D) != sorted(dec):
        kd = {x["sid"]: x["kind"] + "/" + x["role"] for x in doc["sections"]}
        return _why(f"D {doc['query']['qk']} extra={sorted(kd[x] for x in set(D) - set(dec))} "
                    f"miss={sorted(kd[x] for x in set(dec) - set(D))}")
    if not M.sufficient(rd, D):
        return _why("suff")
    for s in rd["sections"]:
        if s["role"] == "near_miss" and not M.nm_functional(rd, s["sid"]):
            return _why("nm nonfunctional " + s["nm"]["kind"])
        if s["role"] == "near_miss":
            a1 = M.option_answer(M.activate(rd, s["sid"]))
            if a1[0] == "abstain" and rd["query"].get("abstain") != "NONE":
                return _why("nm abstain")  # r7: closed choice rows may activate to None (unshown new answer)
    doc["decisive"] = D
    return doc
