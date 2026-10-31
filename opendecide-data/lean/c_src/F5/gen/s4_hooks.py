"""S4 hooks: records tables, quantified claims over a filtered subset, cue cores (C8 exact negations, C9 bound complement
and negated comparison words, C11 other than, C14 graded negatives, C16 decoy)."""
from __future__ import annotations

import random
import re

from . import s4
from .forms import Core, NOT

SAMPLER = "S4"
UP = {"every": "up", "some": "up", "atleast": "up", "morehalf": "up", "gt": "up", "atmost": "down", "lt": "down"}


def _lw(s):
    return bool(re.fullmatch(r"[a-z]+(?: [a-z]+)*", s or ""))


def card_setup(card):
    pv = card["pack"]
    rng = random.Random(card["seed"])
    ents = [e for e in pv["ents"] if len(e["ids"]) >= 14 and _lw(e["noun"]) and _lw(e["plural"])]
    card["ent"] = rng.choice(ents or pv["ents"])
    cats = [c for c in pv["cats"] if _lw(c["name"]) and len(c["values"]) >= 3]
    card["cat"] = rng.choice(cats) if cats else {"name": "region", "values": ["north", "south", "east", "west"]}
    card["cat"] = {"name": card["cat"]["name"],
                   "values": [v for v in card["cat"]["values"] if " and " not in v and "," not in v][:5]}
    qs = [q for q in pv["qtys"] if _lw(q["name"]) and q.get("tag")] or [q for q in pv["qtys"] if _lw(q["name"])]
    card["qty"] = rng.choice(qs)
    good = [a for a in pv["adjs"] if a["tag"] == "good" and _lw(a["word"])]
    bad = [a for a in pv["adjs"] if a["tag"] == "bad" and _lw(a["word"])]
    rng.shuffle(good)
    rng.shuffle(bad)
    card["flags"] = good[:2] + bad[:2]
    card["ptags"] = {a["word"]: a["tag"] for a in card["flags"]}
    card["q_graded"] = rng.choice([2, 3])
    card["negs"] = {}
    return card


def plan_slot(card, rng, s):
    Q = rng.choices(["every", "some", "atleast", "atmost", "morehalf"], [24, 22, 24, 16, 14])[0]
    if s["pair"] is not None:
        Q = rng.choice(["atleast", "atmost"])
    if s["vk"] == 0:
        Q = rng.choice(["atleast", "atmost"]) if card["fams"].get("C9") else Q
        if not card["fams"].get("C9"):
            s["vk"] = 1
    depth = rng.choices([1, 2, 3], [62, 35, 3])[0]
    return {"kind": Q, "depth": depth}


def slot_ctx(card, slot, rng):
    pool = [a["word"] for a in card["flags"] if a["tag"] == slot["tag"]]
    return {"flag": rng.choice(pool)}


def solve(M, lfs):
    return s4.solve_a(M, lfs)


def build_structure(card, slot, rng):
    ent = card["ent"]
    ids = list(ent["ids"])
    rng.shuffle(ids)
    n = rng.randint(6, 11)
    cat, qty = card["cat"], card["qty"]
    flags = [card["flag"]] + rng.sample([a["word"] for a in card["flags"] if a["word"] != card["flag"]], 1)
    M = {"world": "closed", "noun": ent["noun"], "plural": ent["plural"], "cat": cat,
         "qty": {"name": qty["name"], "unit": qty["unit"], "step": qty["step"]}, "flags": flags, "recs": [],
         "q_graded": card["q_graded"]}
    lo, hi, st = qty["lo"], qty["hi"], qty["step"]
    gval = rng.choice(cat["values"])
    for i in range(n):
        r = {"id": ids[i], "cat": gval if rng.random() < 0.55 else rng.choice(cat["values"]),
             "qty": rng.randrange(lo + st, hi, st) if hi - lo > 2 * st else lo, "flags": {}, "blank": {}}
        for w in flags:
            r["flags"][w] = rng.random() < 0.5
            r["blank"][w] = (not r["flags"][w]) and rng.random() < 0.3
        M["recs"].append(r)
    # unrecorded cells (at most 2; never decisive, asserted by both solvers)
    for _ in range(rng.choice([0, 1, 1, 2])):
        r = rng.choice(M["recs"])
        which = rng.choice(["cat", "qty", "flag"])
        if which == "flag":
            r["flags"][rng.choice(flags)] = "NR"
        else:
            r[which] = "NR"
    filters = [["cat", cat["name"], gval]]
    if slot["depth"] >= 2:
        vals = sorted(x["qty"] for x in M["recs"] if x["qty"] != "NR")
        t = rng.choice(vals)
        op = rng.choice([">=", ">", "<=", "<"])
        filters.append(["num", qty["name"], op, t])
    if slot["depth"] >= 3:
        filters.append(["cat2", None, None])
        filters = filters[:2]
        return None
    group = [ent["noun"], filters]
    members = [r for r in M["recs"] if r["cat"] != "NR" and r["qty"] != "NR" and s4.in_group(r, filters, {})]
    if len(members) < 2:
        return None
    pred = ["flag", card["flag"]]
    Q = slot["kind"]
    k = sum(1 for r in members if r["flags"][card["flag"]] is True)
    if any(r["flags"][card["flag"]] == "NR" for r in members) and slot["kind"] in ("atleast", "atmost"):
        return None
    q = None
    if Q in ("atleast", "atmost"):
        q = max(1, k + rng.choice([-1, 0, 0, 1]))
    P = ["q", Q, q, group, pred, None]
    try:
        (v,) = s4.solve_a(M, [P])
    except ValueError:
        return None
    M["base"] = {"Q": Q, "q": q, "group": group, "pred": pred}
    if rng.random() < 0.45:          # text-side decoy (C16) restating two true flags of one record
        both = [r for r in M["recs"] if all(r["flags"][w] is True for w in flags)]
        if both:
            r = rng.choice(both)
            M["decoy_text"] = [r["id"], flags[0], flags[1]]
    return M, P, {"depth": len(filters)}


def fdesc(M, group):
    parts = []
    for f in group[1]:
        if f[0] == "cat":
            parts.append(f"{f[1]} {f[2]}")
        else:
            ph = {">=": "at least", ">": "more than", "<=": "at most", "<": "less than"}[f[2]]
            parts.append(f"a {f[1]} of {ph} {f[3]} {M['qty']['unit']}")
    return "with " + " and ".join(parts)


def q_text(M, Q, q, group, pred, exc=None, matrix=False):
    """(declarative, matrix or None) for one quantified claim."""
    n, pl = M["noun"], M["plural"]
    fd = fdesc(M, group)
    w = pred[1]
    oth = f" other than {n} {exc}" if exc else ""
    if Q == "every":
        return f"every {n} {fd}{oth} is {w}", f"Is every {n} {fd}{oth} {w}"
    if Q == "some":
        return f"some {n} {fd}{oth} is {w}", f"Is any {n} {fd}{oth} {w}"
    head = {"atleast": f"at least {q} of the", "atmost": f"at most {q} of the", "lt": f"fewer than {q} of the",
            "gt": f"more than {q} of the", "morehalf": "more than half of the", "nofewer": f"no fewer than {q} of the",
            "nomore": f"no more than {q} of the", "noneof": "none of the", "hardly": "hardly any",
            "scarcely": "scarcely any", "few": "few"}[Q]
    if Q in ("hardly", "scarcely", "few"):
        d = f"{head} {pl} {fd}{oth} are {w}"
        return d, (None if Q == "few" else f"Are {head} {pl} {fd}{oth} {w}")
    d = f"{head} {pl} {fd}{oth} are {w}"
    mat = None if Q in ("nofewer", "nomore", "noneof") else f"Are {head} {pl} {fd}{oth} {w}"
    return d, mat


def cores(card, M, P, rng, slot):
    b = M["base"]
    Q, q, group, pred = b["Q"], b["q"], b["group"], b["pred"]
    out = {}
    d, m = q_text(M, Q, q, group, pred)
    out["Q.pos"] = Core(f"Q.{Q}", (), d, m, P, 0, UP[Q])
    if Q == "every":
        da = f"all {M['plural']} {fdesc(M, group)} are {pred[1]}"
        out["Q.all"] = Core("Q.all", (), da, f"Are all {M['plural']} {fdesc(M, group)} {pred[1]}", P, 0, "up")
        out["C8.notall"] = Core("C8.notall", ("C8",), "not " + da, None, NOT(P), 1, "down", nd=True,
                                lneg=("not all",))
        out["C8.notevery"] = Core("C8.notevery", ("C8",), "not " + d, None, NOT(P), 1, "down", nd=True,
                                  lneg=("not every",))
        nd, _ = q_text(M, "some", None, group, pred)
        out["C8.nosome"] = Core("C8.no", ("C8",), "no " + nd[len("some "):], None,
                                NOT(["q", "some", None, group, pred, None]), 1, "down", rel="other",
                                lneg=("no",), ptag=card["ptags"][pred[1]])
    if Q == "some":
        out["C8.no"] = Core("C8.no", ("C8",), "no " + d[len("some "):], None, NOT(P), 1, "down", nd=True,
                            lneg=("no",))
        d3, _ = q_text(M, "noneof", None, group, pred)
        out["C8.noneof"] = Core("C8.noneof", ("C8",), d3, None, NOT(P), 1, "down", nd=True, lneg=("none of",))
        d4, _ = q_text(M, "every", None, group, pred)
        out["C8.notevery_o"] = Core("C8.notevery_o", ("C8",), "not " + d4, None,
                                    NOT(["q", "every", None, group, pred, None]), 1, "down", rel="other",
                                    lneg=("not every",), ptag=card["ptags"][pred[1]])
    if Q in ("atleast", "atmost"):
        comp = {"atleast": "lt", "atmost": "gt"}[Q]
        dc, mc = q_text(M, comp, q, group, pred)
        out["C9.compl"] = Core(f"C9.compl.{comp}", ("C9",), dc, mc, ["q", comp, q, group, pred, None], 0,
                               "down" if UP[Q] == "up" else "up", rel="compl")
        neq = {"atleast": ("nofewer", "atleast"), "atmost": ("nomore", "atmost")}[Q]
        dn, _ = q_text(M, neq[0], q, group, pred)
        out["C9.negcmp"] = Core("C9.negcmp", ("C9",), dn, None, ["q", neq[1], q, group, pred, None], 1, UP[Q],
                                lneg=(dn.split(" of the")[0].rsplit(" ", 1)[0],), rel="negcmp")
    # graded negatives with the card constant q* (SEM-25): fewer than q*
    qg = M["q_graded"]
    for G in ("hardly", "scarcely", "few"):
        dg, mg = q_text(M, G, None, group, pred)
        out[f"C14.{G}"] = Core(f"C14.{G}", ("C14",), dg, mg, ["q", "lt", qg, group, pred, None], 1, "down",
                               lneg=(G,), rel="other", ptag=card["ptags"][pred[1]])
    # other than (C11): some member other than one named record
    members = [r for r in M["recs"] if r["cat"] != "NR" and r["qty"] != "NR" and s4.in_group(r, group[1], {})]
    if members:
        ex = members[0]["id"]
        do, mo = q_text(M, "some", None, group, pred, exc=ex)
        out["C11.other"] = Core("C11.other", ("C11",), do, mo, ["q", "some", None, group, pred, ex], 1, "up",
                                lneg=("other than",), rel="other", ptag=card["ptags"][pred[1]])
    return {c.tid: c for c in out.values()}


def is_v_core(card, c):
    if not c.fam or not all(card["fams"].get(f, False) for f in c.fam):
        return False
    return c.rel in ("other", "compl", "negcmp")


def nd_ok(card, c):
    return all(card["fams"].get(f, False) for f in c.fam)


def valid_structure(card, M, P):
    try:
        s4.solve_a(M, [P])
    except ValueError:
        return False
    return True


def tag_of(card, P, M):
    return card["ptags"].get(M["base"]["pred"][1])


def perturb(M, rng):
    return s4.perturb(M, rng)


def doc(M, inert=None, attack=None):
    return s4.doc_ir(M, attack=attack)


def text_triggers(M):
    keys = {"SEM-01", "SEM-02", "SEM-17", "SEM-12", "SEM-14"}
    if M.get("decoy_text"):
        keys.add("SEM-28")
    if any(r["cat"] == "NR" or r["qty"] == "NR" or "NR" in r["flags"].values() or any(r["blank"].values())
           for r in M["recs"]):
        keys.add("SEM-04")
    return keys


def lf_triggers(lf):
    """Generator side: keys fired by the base quantifier / bound words of a question LF (trigger table 3.1)."""
    keys = set()
    if isinstance(lf, list) and lf:
        if lf[0] == "q":
            keys |= {"every": {"SEM-22"}, "some": {"SEM-22"}, "atleast": {"SEM-08", "SEM-12"},
                     "atmost": {"SEM-08", "SEM-12"}, "lt": {"SEM-08", "SEM-12"}, "gt": {"SEM-08", "SEM-12"},
                     "morehalf": {"SEM-09"}}[lf[1]]
            if any(f[0] == "num" for f in lf[3][1]):
                keys |= {"SEM-08", "SEM-12", "SEM-14"}
        for x in lf[1:]:
            keys |= lf_triggers(x)
    return keys


def full_keys(card):
    keys = {"SEM-01", "SEM-02", "SEM-04", "SEM-17", "SEM-12", "SEM-14", "SEM-22", "SEM-08", "SEM-09"}
    if card["fams"].get("C11"):
        keys.add("SEM-23")
    if card["fams"].get("C14"):
        keys.add("SEM-25")
    keys.add("SEM-28")
    return keys


def sem_params(card, M):
    return {"etype": card["ent"]["noun"], "value_sets": [(card["cat"]["name"], card["cat"]["values"])],
            "affixed": [], "q": str(card["q_graded"]), "m": str(card.get("m_graded", 1))}


def affixed_used(M):
    return []


def t_txt(M):
    return 0


def fewshot(card, b):
    M = b["M"]
    n, pl = card["ent"]["noun"], card["ent"]["plural"]
    ids = [x for x in card["ent"]["ids"] if x not in {r["id"] for r in M["recs"]}]
    w = card["flags"][0]["word"]
    v = card["cat"]["values"][0]
    return [{"case": f"Records: {n} {ids[0]} ({card['cat']['name']} {v}, {w}: yes); {n} {ids[1]} "
                     f"({card['cat']['name']} {v}, {w}: no). Question: Is it true that not every {n} with "
                     f"{card['cat']['name']} {v} is {w}?", "answer": "Yes"}]


def inverted_block(card, b):
    return None
