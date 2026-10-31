"""Inverted cards (G0 section 8, K05, F5-R3-09): the yes/no per-case form of "which of these cases meets rule X?" on S1
(case facts as sentences) and S4 (records table). The card lists the cases and the one "if ... then" rule that gives
<outcome> (no exception, no other rule gives it, flat conjunction of 1-3 conditions), so for every listed case the
outcome holds iff the rule's conditions hold (asserted). The question names the outcome, never the rule:
"Is <case> among the cases that are <outcome>?"; a negated row puts its negation inside a truth frame (C1) or uses C2.

M = {world: closed, form: s1|s4, noun, plural, flags [w], qty {name, unit, step}, cat {name, values}, cases [{id, flags,
     qty, cat}], rule {conds [lit], out}, asked}
"""
from __future__ import annotations

import random
import re

from .forms import Core, NOT
from .s1 import num_cmp

SAMPLER = "INV"
BOUNDS = {">=": "at least", ">": "more than", "<=": "at most", "<": "less than"}


def card_setup(card):
    pv = card["pack"]
    rng = random.Random(card["seed"])
    ents = [e for e in pv["ents"] if len(e["ids"]) >= 12 and re.fullmatch(r"[a-z]+(?: [a-z]+)*", e["noun"])]
    card["ent"] = rng.choice(ents or pv["ents"])
    good = [a for a in pv["adjs"] if a["tag"] == "good" and re.fullmatch(r"[a-z]+", a["word"])]
    bad = [a for a in pv["adjs"] if a["tag"] == "bad" and re.fullmatch(r"[a-z]+", a["word"])]
    rng.shuffle(good)
    rng.shuffle(bad)
    card["adjs"] = good[:3] + bad[:3]
    card["ptags"] = {a["word"]: a["tag"] for a in card["adjs"]}
    qs = [q for q in pv["qtys"] if re.fullmatch(r"[a-z]+(?: [a-z]+)*", q["name"])]
    card["qty"] = rng.choice(qs)
    cats = [c for c in pv["cats"] if re.fullmatch(r"[a-z]+(?: [a-z]+)*", c["name"])]
    card["cat"] = rng.choice(cats) if cats else None
    if card["cat"]:
        card["cat"] = {"name": card["cat"]["name"], "values": [v for v in card["cat"]["values"]
                                                               if " and " not in v and "," not in v][:4]}
    card["negs"] = {}
    card["form"] = "s4" if card["sampler"] == "S4" else "s1"
    card["fams"] = dict(card["fams"], C13=True, C16=True)   # inverted V rows: C13 / C16 over the case outcome
    return card


def plan_slot(card, rng, s):
    if s["vk"] >= 2:
        s["vk"] = 1
    return {"kind": "inv", "depth": 1}


def slot_ctx(card, slot, rng):
    pool = [a["word"] for a in card["adjs"] if a["tag"] == slot["tag"]]
    return {"out": rng.choice(pool)}


def cond_true(case, l):
    if l["t"] == "adj":
        x = case["flags"][l["w"]]
        return x if l["pol"] == "pos" else (not x)
    if l["t"] == "num":
        return num_cmp(case["qty"], l["op"], l["n"])
    return (case["cat"] == l["v"]) if l["pol"] == "pos" else (case["cat"] != l["v"])


def holds(M, cid):
    case = next(c for c in M["cases"] if c["id"] == cid)
    return all(cond_true(case, l) for l in M["rule"]["conds"])


def eval_lf(lf, M):
    op = lf[0]
    if op == "not":
        return not eval_lf(lf[1], M)
    if op == "and":
        return all(eval_lf(x, M) for x in lf[1:])
    if op == "inv":
        return holds(M, lf[1].rsplit(" ", 1)[1])
    if op == "adj":
        case = next(c for c in M["cases"] if c["id"] == lf[1].rsplit(" ", 1)[1])
        return case["flags"][lf[2]]
    raise ValueError(op)


def solve(M, lfs):
    return [eval_lf(lf, M) for lf in lfs]


def build_structure(card, slot, rng):
    ent = card["ent"]
    ids = list(ent["ids"])
    rng.shuffle(ids)
    out = card["out"]
    flags = [a["word"] for a in card["adjs"] if a["word"] != out][:card.get("nflags", 3)]
    qd = card["qty"]
    n_cases = rng.randint(3, 5)
    cases = []
    for i in range(n_cases):
        cases.append({"id": ids[i], "flags": {w: rng.random() < 0.5 for w in flags},
                      "qty": rng.randrange(qd["lo"] + qd["step"], qd["hi"], qd["step"]),
                      "cat": rng.choice(card["cat"]["values"]) if card["cat"] else None})
    conds = []
    for w in rng.sample(flags, rng.choice([1, 1, 2])):
        conds.append({"t": "adj", "w": w, "pol": rng.choice(["pos", "pos", "not"])})
    if rng.random() < 0.6:
        c = rng.choice(cases)
        op = rng.choice(list(BOUNDS))
        n = c["qty"] if rng.random() < 0.3 else c["qty"] + rng.choice([-qd["step"], qd["step"]])
        conds.append({"t": "num", "op": op, "n": max(n, 0)})
    if card["cat"] and rng.random() < 0.3:
        conds.append({"t": "cat", "v": rng.choice(card["cat"]["values"]), "pol": rng.choice(["pos", "not"])})
    conds = conds[:3]
    M = {"world": "closed", "form": card["form"], "noun": ent["noun"], "plural": ent["plural"], "flags": flags,
         "qty": {"name": qd["name"], "unit": qd["unit"], "step": qd["step"]},
         "cat": card["cat"], "cases": cases, "rule": {"conds": conds, "out": out}, "rid": f"R{rng.randint(1, 9)}"}
    asked = rng.choice(cases)
    M["asked"] = asked["id"]
    P = ["inv", f"{ent['noun']} {asked['id']}", out]
    return M, P, {"depth": 1}


def subj(M, cid):
    return f"{M['noun']} {cid}"


def cores(card, M, P, rng, slot):
    s = P[1]
    O = P[2]
    phr = f"among the cases that are {O}"
    out = {"INV.pos": Core("INV.pos", (), f"{s} is {phr}", f"Is {s} {phr}", P, 0, "up"),
           "C1.inv": Core("C1.inv", ("C1",), f"{s} is not {phr}", None, NOT(P), 1, "down", nd=True, lneg=("not",))}
    case = next(c for c in M["cases"] if c["id"] == M["asked"])
    for w in M["flags"]:
        A = ["adj", s, w]
        out[f"C16.inv:{w}"] = Core(f"C16.inv:{w}", ("C16",), f"{s} is not only {phr} but also {w}", None,
                                   ["and", P, A], 0, "up", lneg=("not only",), rel="conn")
        out[f"C13.inv:{w}"] = Core(f"C13.inv:{w}", ("C13",), f"{s} is neither {phr} nor {w}", None,
                                   ["and", NOT(P), NOT(A)], 1, "down", lneg=("neither ... nor",), rel="conn")
    return out


def is_v_core(card, c):
    if not c.fam or not all(card["fams"].get(f, False) for f in c.fam):
        return False
    return c.rel == "conn"


def nd_ok(card, c):
    return True


def valid_structure(card, M, P):
    return True


def tag_of(card, P, M):
    return card["ptags"].get(P[2])


def perturb(M, rng):
    return []


def lit_text(M, l):
    n = M["noun"]
    if l["t"] == "adj":
        return f"the {n} is {'' if l['pol'] == 'pos' else 'not '}{l['w']}"
    if l["t"] == "num":
        return f"the {M['qty']['name']} of the {n} is {BOUNDS[l['op']]} {l['n']} {M['qty']['unit']}"
    return f"the {M['cat']['name']} of the {n} is {'' if l['pol'] == 'pos' else 'not '}{l['v']}"


def rule_text(M):
    return f"{M['rid']}. If {' and '.join(lit_text(M, l) for l in M['rule']['conds'])}, then the {M['noun']} is " \
           f"{M['rule']['out']}."


def doc(M, inert=None, attack=None):
    if M["form"] == "s4":
        from fmt1.render import BLANK  # noqa: F401
        cols = [M["noun"]] + ([M["cat"]["name"]] if M["cat"] else []) + [M["qty"]["name"]] + list(M["flags"])
        rows = []
        for c in M["cases"]:
            rows.append([c["id"]] + ([c["cat"]] if M["cat"] else []) + [f"{c['qty']} {M['qty']['unit']}"] +
                        ["yes" if c["flags"][w] else "no" for w in M["flags"]])
        blocks = [{"type": "table", "caption": None, "columns": cols, "rows": rows}]
        if attack:
            blocks.append({"type": "para", "text": attack})
        return {"title": f"{M['plural'][:1].upper() + M['plural'][1:]} under review", "blocks": blocks}
    items = []
    for c in M["cases"]:
        s = subj(M, c["id"])
        S = s[:1].upper() + s[1:]
        for w in M["flags"]:
            if c["flags"][w]:
                items.append(f"{S} is {w}.")
        items.append(f"The {M['qty']['name']} of {s} is {c['qty']} {M['qty']['unit']}.")
        if M["cat"]:
            items.append(f"The {M['cat']['name']} of {s} is {c['cat']}.")
    if attack:
        items.append(attack)
    return {"title": "Case records", "blocks": [{"type": "items", "items": items}]}


def inverted_block(card, b):
    M = b["M"]
    cases = ", ".join(subj(M, c["id"]) for c in M["cases"])
    return [{"type": "para", "text": f"Cases under review: {cases}."},
            {"type": "para", "text": f"Rule for this task: {rule_text(M)}"}]


def text_triggers(M):
    keys = {"SEM-01", "SEM-02", "SEM-12", "SEM-14"}
    if M["cat"]:
        keys.add("SEM-17")
    return keys


def full_keys(card):
    keys = {"SEM-01", "SEM-02", "SEM-07", "SEM-08", "SEM-12", "SEM-14"}
    if card["cat"]:
        keys.add("SEM-17")
    if card["fams"].get("C13"):
        keys.add("SEM-10")
    if card["fams"].get("C16"):
        keys.add("SEM-28")
    return keys


def sem_params(card, M):
    return {"etype": card["ent"]["noun"], "value_sets": [(card["cat"]["name"], card["cat"]["values"])]
            if card["cat"] else [], "affixed": []}


def affixed_used(M):
    return []


def t_txt(M):
    return 0


def fewshot(card, b):
    return None
