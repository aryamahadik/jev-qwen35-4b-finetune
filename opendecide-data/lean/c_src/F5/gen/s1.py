"""S1 rule-case sampler (G0 section 5, S1): rules over one case, closed or open world, optional deontic layer and the F2
amount sub-shape (cap / floor, comparison only). Solver A: forward chaining with weak exceptions (closed: negation as
failure, negated heads are constraints; open: unit propagation over the ground clauses, contrapositives included),
then a direct LF check; deontic status by the SEM-24 closure.

Structure M (JSON-serialisable dict):
  world, noun, subj, facts {"adj:<w>" | "has:<t>": True | False | None(unknown, open only)}, fact_form {key: "pos" |
  "not" | "aff" | "lacks" | "omit"}, nums {q: int | "NR" | None}, units {q: unit}, cats {c: value | "NR"},
  cat_values {c: [...]}, outs [adj words derived by rules], negs {adj: affixed word}, rules [rule], table [cell],
  amount {name, qty, kind cap|floor, limit, unit} | None, decoy_text [a, b] | None
rule = {id, form: if|unless|onlyif|uncond, conds: [lit], exc: lit | None, exc_kw: "except when" | "unless" | None,
        head: {"kind": "adj", "word", "pol": pos|not|aff} | {"kind": "deon", "role", "modal", "verb"}}
lit  = {"t": "adj"|"has"|"out", "w", "pol": pos|not|aff|lacks} | {"t": "num", "q", "op", "n", "ph"} |
       {"t": "cat", "c", "v", "pol": pos|not}
"""
from __future__ import annotations

import copy
import itertools

from .forms import BOUND_POS

MODAL_PERM_NEG = ("must not", "may not", "is not permitted to", "cannot")
MODAL_REQ = ("must", "is required to")
MODAL_PERM = ("may", "is permitted to")
MODAL_REQ_NEG = ("need not", "does not have to", "is not required to")
UNLESS_MODALS = MODAL_REQ + ("must not", "may not", "is not permitted to", "cannot")
ONLYIF_MODALS = MODAL_PERM


# ---------------------------------------------------------------------------------------------------------------------
# truth of literals and rules in one model (closed or one enumerated model)

def num_cmp(v, op, n):
    return {">=": v >= n, ">": v > n, "<=": v <= n, "<": v < n, "==": v == n}[op]


def lit_val(lit, val):
    """val(atom key) -> True / False / None. Returns the literal's truth (Kleene)."""
    t = lit["t"]
    if t in ("adj", "has", "out"):
        key = ("has:" if t == "has" else "adj:") + lit["w"]
        x = val(key)
        if x is None:
            return None
        return x if lit["pol"] == "pos" else (not x)
    if t == "num":
        x = val("num:" + lit["q"])
        if x is None:
            return None
        return num_cmp(x, lit["op"], lit["n"])
    if t == "cat":
        x = val("cat:" + lit["c"])
        if x is None:
            return None
        return (x == lit["v"]) if lit["pol"] == "pos" else (x != lit["v"])
    raise ValueError(t)


def k_and(vals):
    if any(v is False for v in vals):
        return False
    if all(v is True for v in vals):
        return True
    return None


def rule_applies(rule, val):
    """Kleene truth of 'the rule applies' (its body holds and its exception does not)."""
    if rule["form"] in ("if",):
        body = [lit_val(c, val) for c in rule["conds"]]
    elif rule["form"] in ("unless", "onlyif"):
        x = lit_val(rule["conds"][0], val)
        body = [None if x is None else (not x)]
    else:  # uncond
        body = []
    if rule.get("exc"):
        e = lit_val(rule["exc"], val)
        body.append(None if e is None else (not e))
    return k_and(body) if body else True


def head_effect(rule):
    """(atom key, value given) for non-deontic heads at the atom level (SEM-02, F5-R4-01); None for deontic heads."""
    h = rule["head"]
    if h["kind"] != "adj":
        return None
    key = "adj:" + h["word"]
    pos = h["pol"] == "pos"
    if rule["form"] == "onlyif":
        return key, (not pos)          # "A only if B": B false gives not-A; "not A only if B": B false gives A
    return key, pos


def deon_effect(rule):
    """('forbid' | 'require' | None, role, verb) for deontic heads (SEM-24 closure; F5-R4-01)."""
    h = rule["head"]
    if h["kind"] != "deon":
        return None
    m = h["modal"]
    if rule["form"] == "onlyif":
        return ("forbid", h["role"], h["verb"])   # "may X only if B" with B false forbids X
    if m in MODAL_PERM_NEG:
        return ("forbid", h["role"], h["verb"])
    if m in MODAL_REQ:
        return ("require", h["role"], h["verb"])
    return (None, h["role"], h["verb"])


# ---------------------------------------------------------------------------------------------------------------------
# solver A

class Unknown(Exception):
    pass


class Inconsistent(Exception):
    pass


def closed_model(M, nr_assign):
    """The least model of a closed card under one assignment of the unrecorded values. Returns val dict."""
    vals = {}
    for k, x in M["facts"].items():
        vals[k] = bool(x)
    for q, x in M["nums"].items():
        vals["num:" + q] = nr_assign.get("num:" + q) if x == "NR" else x
    for c, x in M["cats"].items():
        vals["cat:" + c] = nr_assign.get("cat:" + c) if x == "NR" else x
    get = vals.get
    for o in topo_outs(M):
        key = "adj:" + o
        derived = False
        for r in M["rules"]:
            he = head_effect(r)
            if he and he[0] == key and he[1] is True and rule_applies(r, get) is True:
                derived = True
        vals[key] = derived
    # constraints: rules that give a negated atom must hold in the least model
    for r in M["rules"]:
        he = head_effect(r)
        if he and he[1] is False and rule_applies(r, get) is True and vals.get(he[0]):
            raise Inconsistent(f"{r['id']} gives not-{he[0]} but the least model holds it")
    return vals


def topo_outs(M):
    deps = {o: set() for o in M["outs"]}
    for r in M["rules"]:
        he = head_effect(r)
        if not he:
            continue
        o = he[0][4:]
        if o not in deps:
            continue
        for l in r["conds"] + ([r["exc"]] if r.get("exc") else []):
            if l["t"] == "out":
                deps[o].add(l["w"])
    order, seen = [], set()

    def visit(o, stack=()):
        if o in seen:
            return
        if o in stack:
            raise Inconsistent("cyclic rule graph")
        for d in sorted(deps[o]):
            visit(d, stack + (o,))
        seen.add(o)
        order.append(o)
    for o in sorted(deps):
        visit(o)
    return order


def atom_key(l):
    return ("has:" if l["t"] == "has" else "adj:") + l["w"]


def open_propagate(M):
    """Unit propagation over the ground clauses of an open card (modus ponens and modus tollens). Returns val dict
    with None for undetermined atoms. Raises Inconsistent on a conflict."""
    vals = {}
    for k, x in M["facts"].items():
        vals[k] = x
    for q, x in M["nums"].items():
        vals["num:" + q] = x
    for c, x in M["cats"].items():
        vals["cat:" + c] = x
    for o in M["outs"]:
        vals.setdefault("adj:" + o, None)
    clauses = []
    for r in M["rules"]:
        he = head_effect(r)
        if he:
            clauses.append((list(rule_body_lits(r)), he))
    changed = True
    while changed:
        changed = False
        for body, (hk, hv) in clauses:
            bv = [lit_val(l, vals.get) for l in body]
            hcur = vals.get(hk)
            if all(b is True for b in bv):
                if hcur is None:
                    vals[hk] = hv
                    changed = True
                elif hcur != hv:
                    raise Inconsistent("conflict (modus ponens)")
            elif hcur is not None and hcur != hv and not any(b is False for b in bv):
                unk = [l for l, b in zip(body, bv) if b is None]
                if not unk:
                    raise Inconsistent("conflict (modus tollens)")
                if len(unk) == 1:
                    l = unk[0]
                    if l["t"] not in ("adj", "has", "out"):
                        continue
                    vals[atom_key(l)] = (l["pol"] != "pos")
                    changed = True
    return vals


def rule_body_lits(r):
    """Body literals of the rule as a conjunction (exception negated) for clause building."""
    if r["form"] == "if":
        out = list(r["conds"])
    elif r["form"] in ("unless", "onlyif"):
        out = [neg_lit(r["conds"][0])]
    else:
        out = []
    if r.get("exc"):
        out.append(neg_lit(r["exc"]))
    return out


def neg_lit(l):
    l = dict(l)
    if l["t"] in ("adj", "has", "out"):
        l["pol"] = "not" if l["pol"] == "pos" else "pos"
    elif l["t"] == "cat":
        l["pol"] = "not" if l["pol"] == "pos" else "pos"
    elif l["t"] == "num":
        l["op"] = {">=": "<", ">": "<=", "<=": ">", "<": ">="}[l["op"]]
        l["ph"] = None
    return l


def deontic_status(M, val, role, verb, which):
    """SEM-24 closure in one model: perm = no applying forbidding rule; req = some applying requiring rule (Kleene)."""
    forb, req = [], []
    for r in M["rules"]:
        de = deon_effect(r)
        if not de or de[1] != role or de[2] != verb:
            continue
        a = rule_applies(r, val)
        if r["form"] == "onlyif":
            x = lit_val(r["conds"][0], val)
            a = None if x is None else (not x)
        if de[0] == "forbid":
            forb.append(a)
        elif de[0] == "require":
            req.append(a)
    for c in M.get("table", []):
        if c["role"] == role and c["verb"] == verb:
            if c["cell"] == "forbidden":
                forb.append(True)
            if c["cell"] == "required":
                req.append(True)
    if which == "perm":
        if any(a is True for a in forb):
            return False
        if all(a is False for a in forb):
            return True
        return None
    if any(a is True for a in req):
        return True
    if all(a is False for a in req):
        return False
    return None


def amount_value(M, val):
    a = M["amount"]
    x = val("num:" + a["qty"])
    if x is None:
        return None
    return min(x, a["limit"]) if a["kind"] == "cap" else max(x, a["limit"])


def eval_lf(lf, M, val):
    op = lf[0]
    if op == "not":
        x = eval_lf(lf[1], M, val)
        return None if x is None else (not x)
    if op == "and":
        xs = [eval_lf(a, M, val) for a in lf[1:]]
        return k_and(xs)
    if op == "or":
        xs = [eval_lf(a, M, val) for a in lf[1:]]
        if any(x is True for x in xs):
            return True
        if all(x is False for x in xs):
            return False
        return None
    if op == "adj":
        return val("adj:" + lf[2])
    if op == "has":
        return val("has:" + lf[2])
    if op == "deon":
        return deontic_status(M, val, lf[2], lf[3], lf[1])
    if op == "amt":
        x = amount_value(M, val)
        return None if x is None else num_cmp(x, lf[3], lf[4])
    if op == "inv":
        return val("adj:" + lf[2])
    raise ValueError(op)


def nr_test_values(M):
    """SEM-04 test sets for every unrecorded value (closed cards): numbers: every threshold compared with it, one step
    either side; categories (value sets): every listed value."""
    tests = {}
    for q, x in M["nums"].items():
        if x == "NR":
            ths = set()
            for r in M["rules"]:
                for l in r["conds"] + ([r["exc"]] if r.get("exc") else []):
                    if l["t"] == "num" and l["q"] == q:
                        ths.add(l["n"])
            if M.get("amount") and M["amount"]["qty"] == q:
                ths.add(M["amount"]["limit"])
            vals = set()
            for t in ths or {0}:
                vals.update({t - 1, t, t + 1})
            tests["num:" + q] = sorted(vals)
    for c, x in M["cats"].items():
        if x == "NR":
            tests["cat:" + c] = list(M["cat_values"][c])
    return tests


def solve_a(M, lfs):
    """Solver A: the value of each LF in lfs, or raises Unknown when an LF is undetermined (also over the SEM-04 test
    values of unrecorded entries) and Inconsistent on a conflict."""
    if M["world"] == "closed":
        tests = nr_test_values(M)
        keys = sorted(tests)
        res = None
        for combo in itertools.product(*[tests[k] for k in keys]) if keys else [()]:
            vals = closed_model(M, dict(zip(keys, combo)))
            check_deontic_conflicts(M, vals.get)
            out = [eval_lf(lf, M, vals.get) for lf in lfs]
            if any(o is None for o in out):
                raise Unknown("closed eval None")
            if res is None:
                res = out
            elif res != out:
                raise Unknown("unrecorded value is decisive")
        return res
    vals = open_propagate(M)
    check_deontic_conflicts(M, vals.get, open_world=True)
    out = [eval_lf(lf, M, vals.get) for lf in lfs]
    if any(o is None for o in out):
        raise Unknown("open: undetermined")
    return out


def check_deontic_conflicts(M, val, open_world=False):
    """SEM-24 asserts: tabled pairs are disjoint from rule pairs; no applying may / is permitted head meets an applying
    prohibition; no applying need not head meets an applying requirement; nothing is both required and forbidden.
    Kleene: a conflict that is possible (both sides not False) is rejected too."""
    pairs = set()
    for r in M["rules"]:
        de = deon_effect(r)
        if de:
            pairs.add((de[1], de[2]))
    for c in M.get("table", []):
        if (c["role"], c["verb"]) in pairs:
            raise Inconsistent("table pair also named by a rule")
    for role, verb in pairs:
        may, forb, need, req = [], [], [], []
        for r in M["rules"]:
            h = r["head"]
            if h["kind"] != "deon" or h["role"] != role or h["verb"] != verb:
                continue
            if r["form"] == "onlyif":
                x = lit_val(r["conds"][0], val)
                forb.append(None if x is None else (not x))
                continue
            a = rule_applies(r, val)
            m = h["modal"]
            (may if m in MODAL_PERM else forb if m in MODAL_PERM_NEG else req if m in MODAL_REQ else need).append(a)
        possible = lambda xs: any(x is not False for x in xs)  # noqa: E731
        for xs, ys, why in ((may, forb, "may meets prohibition"), (need, req, "need not meets requirement"),
                            (req, forb, "required and forbidden")):
            if xs and ys and possible(xs) and possible(ys):
                if any(x is True for x in xs) and any(y is True for y in ys):
                    raise Inconsistent(why)
                if open_world or any(x is None for x in xs + ys):
                    raise Inconsistent(why + " (possible)")
                if any(x is True for x in xs) and any(y is True for y in ys):
                    raise Inconsistent(why)


# ---------------------------------------------------------------------------------------------------------------------
# rendering (program-written English, text side)

def lit_text(l, M):
    n = M["noun"]
    t = l["t"]
    if t in ("adj", "out"):
        if l["pol"] == "pos":
            return f"the {n} is {l['w']}"
        if l["pol"] == "not":
            return f"the {n} is not {l['w']}"
        return f"the {n} is {M['negs'][l['w']]}"
    if t == "has":
        return {"pos": f"the {n} has a {l['w']}", "not": f"the {n} does not have a {l['w']}",
                "lacks": f"the {n} lacks a {l['w']}"}[l["pol"]]
    if t == "num":
        return f"the {l['q']} of the {n} is {l['ph'].format(n=str(l['n']) + ' ' + M['units'][l['q']])}"
    if t == "cat":
        return f"the {l['c']} of the {n} is {'' if l['pol'] == 'pos' else 'not '}{l['v']}"
    raise ValueError(t)


def head_text(r, M):
    h = r["head"]
    n = M["noun"]
    if h["kind"] == "adj":
        w = h["word"]
        core = {"pos": f"is {w}", "not": f"is not {w}", "aff": f"is {M['negs'].get(w, '')}"}[h["pol"]]
        return f"the {n} {core}"
    return f"the {h['role']} {h['modal']} {h['verb']} the {n}"


def rule_text(r, M):
    hid = r["id"]
    if r["form"] == "if":
        conds = " and ".join(lit_text(c, M) for c in r["conds"])
        s = f"If {conds}, then {head_text(r, M)}"
        if r.get("exc"):
            s += f", {r['exc_kw']} {lit_text(r['exc'], M)}" if r["exc_kw"] == "except when" else \
                f" unless {lit_text(r['exc'], M)}"
    elif r["form"] == "unless":
        s = f"{cap(head_text(r, M))} unless {lit_text(r['conds'][0], M)}"
    elif r["form"] == "onlyif":
        s = f"{cap(head_text(r, M))} only if {lit_text(r['conds'][0], M)}"
    else:
        s = cap(head_text(r, M))
        if r.get("exc"):
            s += f", except when {lit_text(r['exc'], M)}"
    return f"{hid}. {s}."


def cap(s):
    return s[:1].upper() + s[1:]


def amount_text(M):
    a = M["amount"]
    n = M["noun"]
    u = M["units"][a["qty"]]
    ph = a["ph"].format(n=f"{a['limit']} {u}")
    return f"{a['rid']}. The {a['name']} of the {n} is the {a['qty']} of the {n}, but {ph}."


def fact_sentences(M):
    s = M["subj"]
    out = []
    for key in M["fact_order"]:
        x = M["facts"].get(key)
        form = M["fact_form"].get(key, "omit")
        if form == "omit":
            continue
        t, w = key.split(":", 1)
        if t == "adj":
            out.append({"pos": f"{cap(s)} is {w}.", "not": f"{cap(s)} is not {w}.",
                        "aff": f"{cap(s)} is {M['negs'].get(w, '')}."}[form])
        else:
            out.append({"pos": f"{cap(s)} has a {w}.", "not": f"{cap(s)} does not have a {w}.",
                        "lacks": f"{cap(s)} lacks a {w}."}[form])
    if M.get("decoy_text"):
        a, b = M["decoy_text"]
        out.append(f"{cap(s)} is not only {a} but also {b}.")
    for q in M["num_order"]:
        x = M["nums"][q]
        if x is None:
            continue
        out.append(f"The {q} of {s} is not recorded." if x == "NR" else f"The {q} of {s} is {x} {M['units'][q]}.")
    for c in M["cat_order"]:
        x = M["cats"][c]
        if x is None:
            continue
        out.append(f"The {c} of {s} is not recorded." if x == "NR" else f"The {c} of {s} is {x}.")
    return out


def doc_ir(M, *, inert=None, attack=None, order_seed=None):
    rules = [rule_text(r, M) for r in M["rules"]]
    if M.get("amount"):
        rules.append(amount_text(M))
    rules.sort(key=lambda x: int(x.split(".")[0][1:]))
    facts = fact_sentences(M)
    if inert:
        facts.append(inert)
    blocks = [{"type": "section", "heading": "Rules", "blocks": [{"type": "items", "items": rules}]}]
    if M.get("table"):
        blocks.append({"type": "table", "caption": "Roles and actions", "columns": ["role", "action", "rule"],
                       "rows": [[c["role"], f"{c['verb']} the {M['noun']}", c["cell"]] for c in M["table"]]})
    case_items = facts + ([attack] if attack else [])
    blocks.append({"type": "section", "heading": "Case record", "blocks": [{"type": "items", "items": case_items}]})
    return {"title": f"{cap(M['noun'])} file", "blocks": blocks}


# ---------------------------------------------------------------------------------------------------------------------
# structure sampler

def pick_bound(rng, value, step):
    """A threshold n for a bound on value: 30% exactly at the boundary, else one step away."""
    if rng.random() < 0.3:
        return value
    return value + rng.choice([-step, step])


def mk_num_lit(rng, q, value, step, want=None):
    for _ in range(20):
        op = rng.choice([">=", ">", "<=", "<"])
        n = pick_bound(rng, value, step)
        if n <= 0:
            continue
        ok = num_cmp(value, op, n)
        if want is None or ok == want:
            ph = rng.choice(BOUND_POS[op] + ([{"<=": "no more than {n}", ">=": "not less than {n}"}[op]]
                                             if op in ("<=", ">=") and rng.random() < 0.3 else []))
            return {"t": "num", "q": q, "op": op, "n": n, "ph": ph}
    return None


def sample_structure(rng, card, kind, depth_target, world):
    """One random S1 structure M for a base of the given kind ('out' | 'deon' | 'amt')."""
    pv = card["pack"]
    ent = card["ent"]
    subj_id = rng.choice(ent["ids"])
    M = {"world": world, "noun": ent["noun"], "subj": f"{ent['noun']} {subj_id}", "facts": {}, "fact_form": {},
         "fact_order": [], "nums": {}, "units": {}, "num_order": [], "cats": {}, "cat_values": {}, "cat_order": [],
         "outs": [], "negs": {}, "rules": [], "table": [], "amount": None, "decoy_text": None}
    adjs = list(card["adjs"])
    rng.shuffle(adjs)
    for a in adjs:
        if a.get("neg"):
            M["negs"][a["word"]] = a["neg"]
    base_out = card["slot_out"]
    out_pool = [a["word"] for a in adjs if a["word"] != base_out]
    n_out = max(1, depth_target) + rng.choice([0, 1])
    outs = [base_out] + out_pool[:n_out - 1] if kind == "out" else out_pool[:n_out]
    fact_adjs = [w for w in out_pool if w not in outs][:3]
    if len(fact_adjs) < 2:
        fact_adjs = (fact_adjs + [a["word"] for a in adjs if a["word"] not in outs])[:2]
    M["outs"] = outs
    # facts
    docs = list(card["docs"])
    rng.shuffle(docs)
    fact_keys = [f"adj:{w}" for w in fact_adjs] + [f"has:{d}" for d in docs[:rng.choice([0, 1, 1])]]
    for k in fact_keys:
        x = rng.random() < 0.5
        if world == "closed":
            M["facts"][k] = x
            M["fact_form"][k] = "pos" if x else "omit"
        else:
            r = rng.random()
            if r < 0.22:
                M["facts"][k] = None
                M["fact_form"][k] = "omit"
            else:
                M["facts"][k] = x
                w = k.split(":", 1)[1]
                if x:
                    M["fact_form"][k] = "pos"
                elif k.startswith("adj:") and M["negs"].get(w) and rng.random() < 0.4:
                    M["fact_form"][k] = "aff"
                elif k.startswith("has:") and rng.random() < 0.5:
                    M["fact_form"][k] = "lacks"
                else:
                    M["fact_form"][k] = "not"
        M["fact_order"].append(k)
    rng.shuffle(M["fact_order"])
    # numbers and categories
    qtys = list(card["qtys"])
    rng.shuffle(qtys)
    for qd in qtys[:rng.choice([1, 2])]:
        lo, hi, st = qd["lo"], qd["hi"], qd["step"]
        v = rng.randrange(lo + st, hi, st) if hi - lo > 2 * st else lo
        M["nums"][qd["name"]] = v
        M["units"][qd["name"]] = qd["unit"]
        M["num_order"].append(qd["name"])
    if card["cats"] and rng.random() < 0.6:
        c = rng.choice(card["cats"])
        M["cats"][c["name"]] = rng.choice(c["values"])
        M["cat_values"][c["name"]] = list(c["values"])
        M["cat_order"].append(c["name"])

    def any_fact_lit(allow_out=None):
        choices = []
        for k in M["facts"]:
            t, w = k.split(":", 1)
            pols = ["pos", "not"] + (["aff"] if t == "adj" and M["negs"].get(w) else []) + \
                   (["lacks"] if t == "has" else [])
            choices.append(("f", t, w, pols))
        for q in M["nums"]:
            choices.append(("n", q))
        for c in M["cats"]:
            choices.append(("c", c))
        if allow_out:
            for o in allow_out:
                choices.append(("o", o))
        ch = rng.choice(choices)
        if ch[0] == "f":
            return {"t": ch[1], "w": ch[2], "pol": rng.choice(ch[3])}
        if ch[0] == "n":
            qd = next(x for x in card["qtys"] if x["name"] == ch[1])
            return mk_num_lit(rng, ch[1], M["nums"][ch[1]], qd["step"])
        if ch[0] == "c":
            vals = M["cat_values"][ch[1]]
            return {"t": "cat", "c": ch[1], "v": rng.choice(vals), "pol": rng.choice(["pos", "pos", "not"])}
        return {"t": "out", "w": ch[1], "pol": rng.choice(["pos", "pos", "not"])}

    rid = [0]

    def new_rule(head, allow_out):
        rid[0] += 1
        form = rng.choices(["if", "unless", "onlyif", "uncond"], [55, 20, 15, 10])[0]
        if head["kind"] == "deon":
            if form == "unless" and head["modal"] not in UNLESS_MODALS:
                form = "if"
            if form == "onlyif":
                head["modal"] = rng.choice(ONLYIF_MODALS)
        r = {"id": f"R{rid[0]}", "form": form, "conds": [], "exc": None, "exc_kw": None, "head": head}
        if form == "if":
            n = rng.choice([1, 1, 2, 2, 3])
            seen = set()
            for _ in range(n):
                l = any_fact_lit(allow_out)
                if l is None:
                    continue
                key = (l["t"], l.get("w") or l.get("q") or l.get("c"))
                if key in seen:
                    continue
                seen.add(key)
                r["conds"].append(l)
            if not r["conds"]:
                return None
            if rng.random() < 0.25:
                e = any_fact_lit(allow_out)
                if e is not None and (e["t"], e.get("w") or e.get("q") or e.get("c")) not in seen:
                    r["exc"] = e
                    r["exc_kw"] = rng.choice(["except when", "unless"])
        elif form in ("unless", "onlyif"):
            l = any_fact_lit(allow_out)
            if l is None:
                return None
            r["conds"] = [l]
        else:
            if rng.random() < 0.8:
                r["exc"] = any_fact_lit(allow_out)
                r["exc_kw"] = "except when"
            if r["exc"] is None and head["kind"] == "adj":
                return None
        if r.get("exc") and r["exc"] is None:
            r["exc"] = None
            r["exc_kw"] = None
        return r

    # outcome rules: deepest outcome first
    order = list(reversed(outs))
    pairmode = bool(card.get("pairmode")) and kind == "out"
    for i, o in enumerate(order):
        lower = order[:i] if depth_target >= 2 else []
        if pairmode and o == card["slot_out"]:
            # contrast-pair mode: the base outcome hangs on one pivot literal (if ... then; on open cards also
            # "only if" on the same literal), so one case-attribute change can flip it (XF03)
            piv = any_fact_lit(lower) if lower else any_fact_lit(None)
            if piv is None:
                continue
            rid[0] += 1
            M["rules"].append({"id": f"R{rid[0]}", "form": "if", "conds": [piv], "exc": None, "exc_kw": None,
                               "head": {"kind": "adj", "word": o, "pol": "pos"}})
            if world == "open":
                rid[0] += 1
                M["rules"].append({"id": f"R{rid[0]}", "form": "onlyif", "conds": [dict(piv)], "exc": None,
                                   "exc_kw": None, "head": {"kind": "adj", "word": o, "pol": "pos"}})
            continue
        for _ in range(rng.choice([1, 1, 2])):
            pol = rng.choices(["pos", "not", "aff"], [70, 18, 12 if M["negs"].get(o) else 0])[0]
            r = new_rule({"kind": "adj", "word": o, "pol": pol}, lower)
            if r:
                M["rules"].append(r)
    if kind == "deon" or (card.get("deontic") and rng.random() < 0.5):
        roles, acts = card["roles"], card["actions"]
        if kind == "deon":
            role, act = card["slot_role"], card["slot_action"]
        else:
            tagged = [a["verb"] for a in card.get("actions_full", [])] or acts
            role, act = rng.choice(roles), rng.choice(tagged)
        for _ in range(rng.choice([1, 2])):
            modal = rng.choice(MODAL_PERM_NEG[:3] + MODAL_REQ + MODAL_PERM + MODAL_REQ_NEG)
            r = new_rule({"kind": "deon", "role": role, "modal": modal, "verb": act}, outs)
            if r:
                M["rules"].append(r)
        if rng.random() < 0.4:
            others = [(ro, a) for ro in roles for a in acts if (ro, a) != (role, act)]
            rng.shuffle(others)
            for ro, a in others[:rng.choice([1, 2])]:
                M["table"].append({"role": ro, "verb": a, "cell": rng.choice(["required", "permitted", "forbidden"])})
    if kind == "amt":
        qd = card["slot_qty"]
        lo, hi, st = qd["lo"], qd["hi"], qd["step"]
        if qd["name"] not in M["nums"]:
            M["nums"][qd["name"]] = rng.randrange(lo + st, hi, st) if hi - lo > 2 * st else lo
            M["units"][qd["name"]] = qd["unit"]
            M["num_order"].append(qd["name"])
        v0 = M["nums"][qd["name"]]
        akind = rng.choice(["cap", "floor"])
        lim = max(st, v0 + rng.choice([-1, 1]) * st * rng.randint(1, 8))
        ph = rng.choice(["at most {n}", "no more than {n}", "not more than {n}", "up to {n}"]) if akind == "cap" \
            else rng.choice(["at least {n}", "not less than {n}"])
        rid[0] += 1
        M["amount"] = {"rid": f"R{rid[0]}", "name": f"adjusted {qd['name']}", "qty": qd["name"], "kind": akind,
                       "limit": lim, "ph": ph}
    rng.shuffle(M["rules"])
    for i, r in enumerate(M["rules"]):
        r["id"] = f"R{i + 1}"
    if M["amount"]:
        M["amount"]["rid"] = f"R{len(M['rules']) + 1}"
    # unrecorded values on closed cards (never on the amount quantity)
    if world == "closed":
        for q in list(M["nums"]):
            if M["amount"] and q == M["amount"]["qty"]:
                continue
            if rng.random() < 0.18:
                M["nums"][q] = "NR"
        for c in list(M["cats"]):
            if rng.random() < 0.12:
                M["cats"][c] = "NR"
    return M


def depth_of(M, word):
    """Base depth: rule applications on the decisive derivation (1 + depth of outcome conditions)."""
    memo = {}

    def d(o):
        if o in memo:
            return memo[o]
        best = 1
        for r in M["rules"]:
            he = head_effect(r)
            if he and he[0] == "adj:" + o:
                for l in r["conds"] + ([r["exc"]] if r.get("exc") else []):
                    if l["t"] == "out":
                        best = max(best, 1 + d(l["w"]))
        memo[o] = best
        return best
    return d(word)


def deon_depth(M, role, verb):
    best = 1
    for r in M["rules"]:
        de = deon_effect(r)
        if de and de[1] == role and de[2] == verb:
            for l in r["conds"] + ([r["exc"]] if r.get("exc") else []):
                if l["t"] == "out":
                    best = max(best, 1 + depth_of(M, l["w"]))
    return best


def mentions(M):
    """Structural trigger facts for the card (generator side)."""
    keys = set()
    for r in M["rules"]:
        if r["form"] == "if":
            keys.add("SEM-07")
            if r.get("exc"):
                keys.add("SEM-15")
        elif r["form"] == "unless":
            keys.add("SEM-05")
        elif r["form"] == "onlyif":
            keys.add("SEM-06")
        else:
            if r.get("exc"):
                keys.add("SEM-15")
        if r["head"]["kind"] == "deon":
            keys.add("SEM-24")
    if M.get("table"):
        keys.add("SEM-24")
    return keys


def perturb_fact(M, rng):
    """Contrast-pair change (closed list, S1): one case attribute. Yields (description, M')."""
    outs = []
    for k in M["fact_order"]:
        x = M["facts"][k]
        if x is None:
            continue
        M2 = copy.deepcopy(M)
        M2["facts"][k] = not x
        if M2["world"] == "closed":
            M2["fact_form"][k] = "pos" if not x else "omit"
        else:
            w = k.split(":", 1)[1]
            M2["fact_form"][k] = "pos" if not x else ("not" if k.startswith("adj:") else "not")
        outs.append((f"fact {k} -> {not x}", M2))
    for q in M["num_order"]:
        x = M["nums"][q]
        if not isinstance(x, int):
            continue
        ths = set()
        for r in M["rules"]:
            for l in r["conds"] + ([r["exc"]] if r.get("exc") else []):
                if l["t"] == "num" and l["q"] == q:
                    ths.add(l["n"])
        if M.get("amount") and M["amount"]["qty"] == q:
            ths.add(M["amount"]["limit"])
        for t in sorted(ths):
            for nv in (t - 1, t, t + 1):
                if nv != x and nv > 0:
                    M2 = copy.deepcopy(M)
                    M2["nums"][q] = nv
                    outs.append((f"num {q} {x} -> {nv}", M2))
    for c in M["cat_order"]:
        x = M["cats"][c]
        if x in (None, "NR"):
            continue
        for v in M["cat_values"][c]:
            if v != x:
                M2 = copy.deepcopy(M)
                M2["cats"][c] = v
                outs.append((f"cat {c} {x} -> {v}", M2))
    rng.shuffle(outs)
    return outs
