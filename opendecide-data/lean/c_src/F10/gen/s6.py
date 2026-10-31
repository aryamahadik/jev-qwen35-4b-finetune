"""S6 label-description rows: the state paraphrases exactly one card definition through registered
equivalence-preserving rewrites (operator synonyms, conjunct reorder, De Morgan, whole-number shift, ONLY-IF folded
into the conjunction, inlining a referenced term, exact unit restatement); every description applies >= 2 rewrites; solver B proves the paraphrase equivalent to its
term and to no other (ST43)."""
from __future__ import annotations

import copy

import lexicon as L
import model as M
from render import body_text
from solver_b import CardB
from values import u1_ok

NEG_OP = {"ge": "lt", "lt": "ge", "gt": "le", "le": "gt"}


def neg_atom(at):
    t = at["t"]
    if t == "cmp" and at["op"] in NEG_OP:
        return {**at, "op": NEG_OP[at["op"]]}
    if t == "cat":
        return {**at, "neg": not at["neg"], "style": "is" if len(at["S"]) == 1 else "oneof"}
    if t == "flag":
        return {**at, "v": not at["v"]}
    if t == "tag" and at["m"] in ("any", "none", "has"):
        if at["m"] == "has":
            return {**at, "m": "none"}
        return {**at, "m": "none" if at["m"] == "any" else "any"}
    return None


def shift(at, legend):
    if at["t"] == "cmp" and legend[at["a"]]["type"] == "count":
        op, c = at["op"], at["c"]
        if op == "ge" and c >= 1:
            return {**at, "op": "gt", "c": c - 1}
        if op == "gt":
            return {**at, "op": "ge", "c": c + 1}
        if op == "le":
            return {**at, "op": "lt", "c": c + 1}
        if op == "lt" and c >= 1:
            return {**at, "op": "le", "c": c - 1}
    return None


def paraphrase(card, did, r):
    """(description body AST, rewrites applied, alt phrase shift) or None."""
    d = card["defs"][did]
    if d["body"]["form"] not in ("single", "ALL") or d.get("exc") is not None:
        return None
    items = [copy.deepcopy(i) for i in d["body"]["items"]]
    rw = []
    # inlining a referenced term (AR03): a positive reference to Y with no ONLY-IF / Exception whose body is a single
    # item or an ALL list flattens into the host ALL (or replaces a bare reference); otherwise no paraphrase
    flat = []
    for i in items:
        if i["k"] == "ref":
            y = card["defs"].get(i["to"])
            if (i.get("neg") or y is None or y.get("onlyif") is not None or y.get("exc") is not None
                    or y["body"]["form"] not in ("single", "ALL")
                    or any(j["k"] != "item" or j.get("unless") is not None for j in y["body"]["items"])):
                return None
            flat += [copy.deepcopy(j) for j in y["body"]["items"]]
            if "inlining" not in rw:
                rw.append("inlining")
        else:
            flat.append(i)
    items = flat
    if any(i["k"] != "item" or i.get("unless") is not None for i in items):
        return None
    atoms = [i["atom"] for i in items]
    if d.get("onlyif") is not None and d["onlyif"]["k"] == "atom":
        atoms.append(copy.deepcopy(d["onlyif"]))
        rw.append("onlyif_fold")
    sh = [k for k, a in enumerate(atoms) if shift(a, card["legend"]) is not None]
    if sh and r.random() < 0.6:
        k = r.choice(sh)
        atoms[k] = shift(atoms[k], card["legend"])
        rw.append("whole_number_shift")
    if len(atoms) >= 2 and r.random() < 0.8:
        perm = list(range(len(atoms)))
        while perm == sorted(perm):
            r.shuffle(perm)
        atoms = [atoms[i] for i in perm]
        rw.append("reorder")
    # exact unit restatement (ST26 conversion line on the card): a constant on the converted attribute written in the
    # larger unit when value / k is exact within d + 3 decimals (AR28); the parser converts it back
    cs = card.get("conv_slot")
    if cs is not None:
        uu = [k for k, a in enumerate(atoms) if a["t"] == "cmp" and a["a"] == cs and u1_ok(card["legend"][cs], a["c"])]
        if uu and r.random() < 0.7:
            k = r.choice(uu)
            atoms[k] = {**atoms[k], "u1": True}
            rw.append("unit_restatement")
    form = "single" if len(atoms) == 1 else "ALL"
    negs = [neg_atom(a) for a in atoms]
    if len(atoms) >= 2 and all(n is not None for n in negs) and r.random() < 0.4:
        atoms, form = negs, "NOTANY"
        rw.append("de_morgan")
    alt = r.randint(1, 3)
    rw.append("operator_synonym")
    if len(rw) < 2:
        return None
    body = M.Body(form, [M.It(a) for a in atoms])
    return body, rw, alt


def desc_text(card, body, alt, fi):
    """fi: DESC_FRAME index (stored in the row spec so a G4 variant re-renders the same frame)."""
    tmp = {"desc": M.Def("desc", body)}
    c2 = dict(card)
    c2["defs"] = {**card["defs"], **tmp}
    txt = body_text(c2, "desc", body, ("desc",), alt)
    return L.DESC_FRAME[fi].format(E=card["entity"], B=txt)


def s6_rows(card, r, plan, stats):
    """Groups for an S6 card (choice 3-9 options / yes-no 'defines')."""
    order = card["order"]
    cb = CardB(card["legend"], card["defs"], order, "desc")
    made, gi, fails = 0, 0, 0
    mix = [0, 0, r.random()]
    from samplers import YesCtl
    yctl = YesCtl(plan, card.get("card_id"))     # repair r1 (G7): per-card yes-rate controller on emitted rows
    from collections import Counter as _Ctr
    gcount = _Ctr()
    while plan.get("_emitted", made) < plan["n_rows"] and fails < 60 and gi < 6 * plan["n_rows"]:
        gi += 1
        # balanced described term per card (repair r1, G10 gold card position): least-used first, ties at random
        m = min(gcount[t] for t in order)
        X = r.choice([t for t in order if gcount[t] == m]) if r.random() < 0.85 else r.choice(order)
        p = paraphrase(card, X, r)
        if p is None:
            fails += 1
            gcount[X] += 0.34      # a description that keeps failing counts as used after 3 tries
            continue
        body, rw, alt = p
        cb.defs = {**card["defs"], "desc": M.Def("desc", body)}
        cb.R.pop("desc", None)
        eq = [t for t in order if cb.sp.equal(cb.region("desc"), cb.region(t))]
        if eq != [X]:
            stats["s6_rej_equiv"] += 1
            fails += 1
            gcount[X] += 0.34
            continue
        fails = 0
        fi = r.randrange(len(L.DESC_FRAME))
        text = desc_text(card, body, alt, fi)
        r.random()
        if mix[1] < plan.get("choice_rows", 0.5) * (mix[0] + 1) - mix[2]:     # per-card choice-row controller (repair r1)
            k, _ = plan["draw_k"]()
            k = max(3, min(k, len(order)))
            others = [t for t in order if t != X]
            r.shuffle(others)
            row = {"form": "choice", "options": [X] + others[:k - 1], "gold": X, "desc": body, "desc_text": text,
                   "desc_frame": fi, "desc_alt": alt, "rewrites": rw, "ecodes": {t: "E3" for t in others[:k - 1]}}
        else:
            r.random()
            want = yctl.want()
            ask = X if want else r.choice([t for t in order if t != X])
            row = {"form": "yn", "ask": ask, "wkind": "defines", "gold": 1 if want else 0, "desc": body,
                   "desc_text": text, "desc_frame": fi, "desc_alt": alt, "rewrites": rw, "described": X}
        row["gid"] = gi
        group = [row]
        if row["form"] == "yn" and r.random() < plan["neg_p"] + plan["dneg_p"]:
            group.append({**row, "neg": 1, "neg_form": r.randrange(2), "gold": 1 - row["gold"], "rel": "complement",
                          "twin_kind": "neg", "twin_of": "anchor"})
            if r.random() < plan["dneg_p"] / max(1e-9, plan["neg_p"] + plan["dneg_p"]):
                group.append({**row, "neg": 2, "rel": "equiv", "twin_kind": "dneg", "twin_of": "anchor"})
        gcount[X] += 1
        if row["form"] == "choice":
            plan["draw_k"].note(len(row["options"]))
        mix[0] += len(group)
        mix[1] += sum(1 for sp in group if sp.get("form") == "choice")
        made += len(group)
        yield group
