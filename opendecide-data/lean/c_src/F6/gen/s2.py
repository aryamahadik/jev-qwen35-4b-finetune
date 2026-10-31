"""S2: label-first witness pairs (G0 s7). The gold class is drawn first; for an open row two completions that differ
on one witness variable w give different outcomes X and Y; the rules are written backwards so that everything else
is shared (a shared condition s holds, every distractor rule has a known false condition); Y is either the head of a
rule on the complement of w or the default, reached only because no rule applies. Every row also carries at least
one case-split trap: an unknown u whose two values give the same outcome. C-CASE rows put 3-6 mini-cases under one
rule card, exactly one of them decidable (or exactly one not decidable).
"""
from __future__ import annotations

import copy
import random

from . import solver_a as A
from . import rules_gen as G
from . import rules_rows as RR
from .common import day

NOTICE_NAMES = G.NOTICE_NAMES
from collections import Counter as _Ctr
REJ = _Ctr()


def _var_atom(rng, R, k, P, positive=True):
    """An atom on variable k that is true (positive) or false in the full case value assigned later."""
    t = k[0]
    if t == "num":
        a = R["attrs"][k[1]]
        n = rng.randint(a["lo"] + 3, a["hi"] - 3)
        ops = [">=", "<="] if P["cmp_family"] == "incl" else [">", "<"]
        return {"t": "num", "a": k[1], "op": rng.choice(ops), "n": n}
    if t == "cat":
        return {"t": "cat", "a": k[1], "v": rng.choice(R["attrs"][k[1]]["vals"])}
    if t == "ev":
        return {"t": "ev", "e": k[1], "neg": False}
    return {"t": "cls", "c": k[1]}


def _neg_atom(at, R):
    """An atom true exactly when `at` is false (the witness's other side), in the same comparator family
    (inclusive or exclusive), so the card's row 11 / 12 sentence covers it."""
    if at["t"] == "num":
        n, op = at["n"], at["op"]
        op2, n2 = {">=": ("<=", n - 1), "<=": (">=", n + 1), ">": ("<", n + 1), "<": (">", n - 1)}[op]
        return {"t": "num", "a": at["a"], "op": op2, "n": n2}
    if at["t"] == "ev":
        return {"t": "ev", "e": at["e"], "neg": not at.get("neg")}
    return None


def _value_making(rng, R, at, truth):
    """A value of at's variable that makes at true / false."""
    t = at["t"]
    if t == "num":
        a = R["attrs"][at["a"]]
        vals = [v for v in range(a["lo"], a["hi"] + 1)
                if A._atom(at, {("num", at["a"]): v}) == truth]
        return rng.choice(vals) if vals else None
    if t == "cat":
        a = R["attrs"][at["a"]]
        vals = [v for v in a["vals"] if (v == at["v"]) == truth]
        return rng.choice(vals) if vals else None
    if t == "ev":
        return truth != bool(at.get("neg"))
    if t == "cls":
        return truth
    return None


def _hideable_elems(R, P, k):
    """The gap elements a variable can show on this card (marker / absent / tag; s2 positions)."""
    rich = P.get("mode") == "rich"
    out = set()
    for m in RR._modes(R, k, True, rich) + RR._modes(R, k, False, rich):
        out.add(RR._pred_elem(R, k, m, {}))
    return out


def _s_first(spec, vars_, rest):
    """Repair r1 v3d (G11 cards_ge_80, G10 abstain display at k 3): on C-OUT the trap rules need a false companion;
    with no variable beyond w, s, u, u2 it is an atom on s other than s's own, which only a number or category has.
    So on a 4-variable C-OUT design s is taken from the numbers / categories when one is left (label-free: the
    card's variables only). Other forms and larger designs keep the shuffled order."""
    if spec.get("form") != "c_out" or len(vars_) > 4:
        return rest
    return sorted(rest, key=lambda v: v[0] not in ("num", "cat"))


def design(rng: random.Random, card: dict, spec: dict, n_rules: int, n_out_min: int, need=None):
    """A policy written backwards around a witness variable w and a shared condition s, with two case-split trap
    variables u and u2 (each in a rule 'u and w and s give X', so either value of u gives the same outcome).
    Repair r1: every S2 row shows exactly two gaps (open rows: w and u; settled rows: u and u2), the rule count
    never depends on the role, and with `need` (a settled row's signature) u and u2 are chosen to show exactly
    those gap elements. Returns (R, plan)."""
    P, pack = card["P"], card["pack"]
    R = G.draw_policy(rng, P, pack, 1, n_out_min)          # attributes, notices, outcome names
    R["rules"], R["onlyif"], R["subclass"] = [], [], []
    vars_ = [("num", a) for a in R["attrs"] if R["attrs"][a]["kind"] == "num"] + \
            [("cat", a) for a in R["attrs"] if R["attrs"][a]["kind"] == "cat"] + \
            [("ev", e) for e in R["events"]] + [("cls", c) for c in R["classes"]]
    rng.shuffle(vars_)
    if len(vars_) < 4:
        raise RR.Reject("S2 needs four variables")
    hid = {v: _hideable_elems(R, P, v) for v in vars_}
    if need is not None:
        els = list(need.elements())
        if len(els) != 2:
            raise RR.Reject("S2 signature size")
        a = [v for v in vars_ if els[0] in hid[v]]
        b = [v for v in vars_ if els[1] in hid[v]]
        pairs = [(x, y) for x in a for y in b if x != y]
        if not pairs:
            raise RR.Reject("S2 signature not realisable")
        u, u2 = rng.choice(pairs)
        rest = [v for v in vars_ if v not in (u, u2)]
        w = next((v for v in rest if hid[v]), None)
        if w is None:
            raise RR.Reject("S2 witness")
        s = next(v for v in _s_first(spec, vars_, [v for v in rest if v != w]))
    else:
        hv = [v for v in vars_ if hid[v]]
        if len(hv) < 2:
            raise RR.Reject("S2 needs two hideable variables")
        w, u = hv[0], hv[1]
        rest = _s_first(spec, vars_, [v for v in vars_ if v not in (w, u)])
        s, u2 = rest[0], rest[1]
    if sum(1 for v in (w, s, u, u2) if v[0] == "cls") > 1:
        raise RR.Reject("at most one class condition per rule (row 24)")
    others = [v for v in vars_ if v not in (w, s, u, u2)]
    outs = [o for o in R["outcomes"] if o != R["default"]]
    rng.shuffle(outs)
    X = outs[0]
    use_default = rng.random() < 0.35
    Y = R["default"] if use_default else outs[1]
    nid = list(R["notices"])
    wa = _var_atom(rng, R, w, P)
    sa = _var_atom(rng, R, s, P)
    rules = [{"rid": "r1", "notice": rng.choice(nid), "conds": [wa, sa], "unless": None, "out": X, "exc": None}]
    if not use_default:
        neg = _neg_atom(wa, R)
        if neg is None:          # categories and classes: the other side is 'no rule applies' (default)
            Y = R["default"]
        else:
            rules.append({"rid": "r2", "notice": rng.choice(nid), "conds": [neg, sa], "unless": None, "out": Y,
                          "exc": None})
    # case-split traps (repair r1 v3c, G6 view c / F6-QC-13): u and u2 each sit in a rule for a catalog outcome of
    # its own whose other condition is false in the case, so both values of u (u2) give the same outcome (G0 s7:
    # case-split trap). Before v3c both trap rules gave X, so X was named by three rule heads and every distractor by
    # one: 'the option the card names most often' pointed to the gold. Now every outcome heads exactly one rule.
    plan = {"w": w, "s": s, "u": u, "u2": u2, "wa": wa, "sa": sa, "ua": None, "false": []}
    k = 0
    free_outs = [o for o in outs if o not in (X, Y)]
    if spec.get("form") != "c_out":       # the mention leak concerns option lists of outcome names (C-OUT) only;
        ua = _var_atom(rng, R, u, P)      # yes/no and C-CASE cards keep the original X trap rules
        rules.append({"rid": f"r{len(rules) + 1}", "notice": rules[0]["notice"], "conds": [ua, wa, sa],
                      "unless": None, "out": X, "exc": None})
        u2a = _var_atom(rng, R, u2, P)
        rules.append({"rid": f"r{len(rules) + 1}", "notice": rules[0]["notice"], "conds": [u2a, wa, sa],
                      "unless": None, "out": X, "exc": None})
        plan["ua"] = ua
    elif len(free_outs) < 2:
        raise RR.Reject("S2 trap outcomes")

    def false_atom():
        nonlocal k
        if others:
            v = others[k % len(others)]
            k += 1
            return _var_atom(rng, R, v, P)
        for _ in range(8):
            da = _var_atom(rng, R, s, P)
            if da != sa:
                return da
        na = _neg_atom(sa, R)     # repair r1 v3d: an event s has one positive atom; its negation is false in the case
        if na is not None:        # (joint_values makes sa true), so 'u and not-s' is still a case-split trap
            return na
        raise RR.Reject("S2 false companion")
    for j, uv in enumerate((u, u2) if spec.get("form") == "c_out" else ()):
        ua = _var_atom(rng, R, uv, P)
        fa = false_atom()
        rules.append({"rid": f"r{len(rules) + 1}", "notice": rng.choice(nid), "conds": [ua, fa],
                      "unless": None, "out": free_outs[j], "exc": None})
        plan["false"].append(fa)
        if j == 0:
            plan["ua"] = ua
    if spec.get("form") == "c_out":
        free_outs = free_outs[2:]
    # distractors: a rule whose condition on a fresh variable is false in the case
    for i in range(max(0, n_rules - len(rules))):
        if not free_outs:
            break
        o = free_outs[i % len(free_outs)]
        if others:
            v = others[k % len(others)]
            k += 1
            da = _var_atom(rng, R, v, P)
        else:
            da = _var_atom(rng, R, s, P)
            if da == sa:
                continue
        rules.append({"rid": f"r{len(rules) + 1}", "notice": rng.choice(nid), "conds": [da], "unless": None,
                      "out": o, "exc": None})
        plan["false"].append(da)
    R["rules"] = rules
    return R, plan


def joint_values(rng, R, plan, asg) -> bool:
    """Values for s (its atom true) and every distractor variable (all its atoms false) at once."""
    by = {}
    for at, truth in [(plan["sa"], True)] + [(d, False) for d in plan["false"]]:
        by.setdefault(A._atom_var(at), []).append((at, truth))
    for k, lst in by.items():
        t = k[0]
        if t == "num":
            a = R["attrs"][k[1]]
            vals = [v for v in range(a["lo"], a["hi"] + 1) if all(A._atom(at, {k: v}) == tr for at, tr in lst)]
        elif t == "cat":
            vals = [v for v in R["attrs"][k[1]]["vals"] if all((v == at["v"]) == tr for at, tr in lst)]
        else:
            vals = [x for x in (True, False) if all(_value_making(rng, R, at, tr) == x for at, tr in lst)]
        if not vals:
            return False
        asg[k] = rng.choice(vals)
    return True


def build_record(rng: random.Random, card: dict, spec: dict, case: str, dis: list, target: str, n_gaps: int,
                 n_rules: int, n_out_min: int, sig=None):
    """S2 record (repair r1): exactly two visible gaps on every row. Open rows hide the witness w (decisive) and
    the case-split trap u; settled rows hide the two case-split traps u and u2 (with `sig`, chosen to show exactly
    that kind@position signature). Rules, attributes and outcomes never depend on the role."""
    from collections import Counter
    P = card["P"]
    rich = P.get("mode") == "rich"
    need = Counter(sig) if sig else None
    for _ in range(40):
        try:
            R, plan = design(rng, card, spec, n_rules, n_out_min, need=need if target == "settled" else None)
        except (ValueError, RR.Reject):
            REJ["design"] += 1
            continue
        if P["world"] == "local":
            R["local"] = P["local_cid"]
        asg = G.full_case(rng, R, case)
        ok = True
        if not joint_values(rng, R, plan, asg):
            REJ["value"] += 1
            continue
        roles = G.ref_vars(R)
        hidden = RR._forced_hidden(R, asg, P)
        hide = [plan["w"], plan["u"]] if target == "open" else [plan["u"], plan["u2"]]
        if any(k not in hide for k in hidden):
            REJ["forced"] += 1
            continue
        left = Counter(need) if (need is not None and target == "settled") else None
        for k in hide:
            if k in hidden:
                if left is not None:
                    left = left - Counter([RR._pred_elem(R, k, hidden[k], roles)])
                continue
            ms = RR._modes(R, k, asg[k], rich)
            if left is not None:
                ms = [m for m in ms if left.get(RR._pred_elem(R, k, m, roles))]
            if not ms:
                ok = False
                break
            m = rng.choice(ms)
            hidden[k] = m
            if left is not None:
                left = left - Counter([RR._pred_elem(R, k, m, roles)])
        if not ok:
            REJ["mode"] += 1
            continue
        if not RR._ok_subclass(R, asg, hidden):
            REJ["sub"] += 1
            continue
        try:
            Rf, gaps, Pset = RR._evaluate(rng, R, case, asg, hidden, dis)
        except (ValueError, A.Drop):
            REJ["eval"] += 1
            continue
        if len(gaps) != 2:
            REJ["ngaps"] += 1
            continue
        if need is not None and target == "settled" and Counter(RR.elems(Rf, case, gaps)) != need:
            REJ["sig"] += 1
            continue
        if target == "settled":
            if len(Pset) != 1:
                REJ["notsettled"] += 1
                continue
        else:
            if len(Pset) < 2 or RR._n_decisive(Rf, case, gaps) != [plan["w"]]:
                REJ["notopen"] += 1
                continue
        return Rf, asg, hidden, Pset, None, gaps
    raise RR.Reject("S2 record")


def shape(rng, card, spec, case, dis, target, n_gaps, n_rules, n_out_min, sig=None):
    return build_record(rng, card, spec, case, dis, target, n_gaps, n_rules, n_out_min, sig=sig)


# ---------------------------------------------------------------- C-CASE (inverted cards)

def build_case_unit(rng: random.Random, card: dict, spec: dict, uid: str) -> list[dict]:
    """3-6 mini-cases under one policy; exactly one decidable ('can') or exactly one undecidable ('cannot').
    Repair r1: the undecidable cases are built first, and every decidable case takes the gap signature
    (kind@position multiset) of an undecidable case of the same row, so decidable and undecidable cases carry one
    visible-gap distribution (s6 'Gaps': checked per case on C-CASE rows)."""
    from collections import Counter
    from fmt1 import card as fcard
    P = card["P"]
    rich = P.get("mode") == "rich"
    k = spec["k"]
    labels = fcard.case_refs(card["case_ref"], k, uid)
    want_dec = spec["gold"] == "can"
    for attempt in range(10):
        try:
            R, plan = design(rng, card, spec, rng.randint(3, 4), 4)
        except (ValueError, RR.Reject):
            continue
        if P["world"] == "local":
            R["local"] = P["local_cid"]
        roles = G.ref_vars(R)
        gold_i = rng.randrange(k)
        facts, lists_all, gaps_all, ok = {}, {}, {}, True
        dec_of = {i: (i == gold_i) == want_dec for i in range(k)}
        order = sorted(range(k), key=lambda i: dec_of[i])          # undecidable cases first
        und_sigs = []
        for i in order:
            lab = labels[i]
            decidable = dec_of[i]
            need = Counter(rng.choice(und_sigs)) if (decidable and und_sigs) else None
            got = None
            for _ in range(30):
                asg = G.full_case(rng, R, lab)
                if not joint_values(rng, R, plan, asg):
                    continue
                hidden = RR._forced_hidden(R, asg, P)
                if plan["s"] in hidden:
                    continue
                if not decidable and plan["w"] not in hidden:
                    ms = RR._modes(R, plan["w"], asg[plan["w"]], rich)
                    if not ms:
                        continue
                    hidden[plan["w"]] = rng.choice(ms)
                if decidable and plan["w"] in hidden:
                    continue
                cand = [x for x in roles if x not in hidden and x not in (plan["w"], plan["s"])] + \
                    [(a["kind"], aid) for aid, a in R["attrs"].items() if (a["kind"], aid) not in roles]
                rng.shuffle(cand)
                if need is None:
                    ng = rng.choice([1, 2])
                    for x in cand[: max(0, ng - len(hidden))]:
                        ms = RR._modes(R, x, asg[x], rich) if x in roles else ["marker"]
                        if ms:
                            hidden[x] = rng.choice(ms)
                else:
                    have = Counter(RR._pred_elem(R, x, m, roles) for x, m in hidden.items())
                    left = need - have
                    if have - need:
                        continue
                    for x in cand:
                        if not left:
                            break
                        ms = RR._modes(R, x, asg[x], rich) if x in roles else ["marker"]
                        ms = [m for m in ms if left.get(RR._pred_elem(R, x, m, roles))]
                        if ms:
                            m = rng.choice(ms)
                            hidden[x] = m
                            left = left - Counter([RR._pred_elem(R, x, m, roles)])
                    if left:
                        continue
                if not RR._ok_subclass(R, asg, hidden):
                    continue
                try:
                    Rc = G.realise(rng, R, lab, asg, hidden, [l for l in labels if l != lab][:2])
                except ValueError:
                    continue
                gp = G.visible_gaps(Rc, lab)
                if not 1 <= len(gp) <= 3:
                    continue
                if need is not None and Counter(RR.elems(Rc, lab, gp)) != need:
                    continue
                try:
                    Ps = A.solve_rules(Rc, lab)
                except A.Drop:
                    continue
                if (len(Ps) == 1) != decidable:
                    continue
                if not decidable:
                    dec = A.decisive_gaps(Rc, lab)
                    if len([d for d in dec if d in [g for g, _ in gp]]) != 1:
                        continue
                got = (Rc, gp, Ps)
                break
            if got is None:
                ok = False
                break
            Rc, gp, Ps = got
            if not decidable:
                und_sigs.append(RR.elems(Rc, lab, gp))
            facts[lab] = Rc["facts"][lab]
            gaps_all[lab] = gp
            for cid, ents in Rc["lists"].items():
                lists_all.setdefault(cid, {})[lab] = [e for e in ents if e[0] == lab]
        if not ok:
            continue
        R2 = copy.deepcopy(R)
        R2["facts"] = facts
        R2["cases"] = labels
        lists = {}
        for cid, per in lists_all.items():
            lists[cid] = [e for lab in labels for e in per.get(lab, [])]
        if any(not v for v in lists.values()):
            continue
        R2["lists"] = lists
        dec = [lab for lab in labels if len(A.solve_rules(R2, lab)) == 1]
        if (len(dec) == 1) != want_dec and not (not want_dec and len(dec) == k - 1):
            continue
        gold = dec[0] if want_dec else next(l for l in labels if l not in dec)
        return [{"R": R2, "case": None, "cases": labels, "form": "c_case", "spec": spec, "uid": uid,
                 "gold_case": gold, "decidable": dec, "gaps_by_case": gaps_all,
                 "frame": "c_case_can" if want_dec else "c_case_cannot", "depth": 2, "P": set(),
                 "gaps": [g for lab in labels for g in gaps_all[lab]]}]
    raise RR.Reject("C-CASE unit")
