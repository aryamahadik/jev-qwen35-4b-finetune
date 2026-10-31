"""S3 G3 parser (universals and facts grammar), solver B (truth tables over the ground atoms: closed cards enumerate
models of the completion, open cards models of the material clauses) and the S3 question forms (group scope)."""
from __future__ import annotations

import itertools
import json
import re

from . import parse as PZ
from .texts import ATTACK_RE

ATT = re.compile(ATTACK_RE)
ID = r"[A-Z]{1,4}-[A-Z0-9]+(?:-[A-Z0-9]+)?"


def _pred(vp, consts):
    m = re.fullmatch(r"is ([a-z-]+)", vp)
    if m:
        return "adj:" + m.group(1)
    m = re.fullmatch(r"has a (.+)", vp)
    if m:
        return "has:" + m.group(1)
    raise ValueError(f"S3 predicate {vp!r}")


def parse(rs, consts):
    r = next((x for x in rs if x["role"] != "attack"), rs[0])
    sents, rows = PZ.sentences(r["state"])
    univ, facts, inert, decoys = [], [], [], []
    noun = None
    for s in sents:
        if ATT.fullmatch(s):
            continue
        m = re.fullmatch(r"(Every|No) (.+?) that (is [a-z-]+|has a .+?) (is [a-z-]+|has a .+)\.", s)
        if m:
            noun = m.group(2)
            univ.append({"q": "every" if m.group(1) == "Every" else "no", "a": _pred(m.group(3), consts),
                         "b": _pred(m.group(4), consts)})
            continue
        m = re.fullmatch(rf"([A-Z][a-z][a-z -]*?) ({ID}) (.+)\.", s)
        if m:
            e, rest = m.group(2), m.group(3)
            noun = noun or m.group(1).lower()
            mm = re.fullmatch(r"is not only ([a-z-]+) but also ([a-z-]+)", rest)
            if mm:
                for w in mm.groups():
                    facts.append({"e": e, "p": "adj:" + w, "val": True, "form": "pos"})
                decoys.append((e,) + mm.groups())
                continue
            mm = re.fullmatch(r"(is not|is) ([a-z-]+)", rest)
            if mm:
                w = mm.group(2)
                if w in consts["affixed"]:
                    facts.append({"e": e, "p": "adj:" + consts["affixed"][w], "val": False, "form": "aff"})
                else:
                    facts.append({"e": e, "p": "adj:" + w, "val": mm.group(1) == "is",
                                  "form": "pos" if mm.group(1) == "is" else "not"})
                continue
            mm = re.fullmatch(r"(has|does not have|lacks) a (.+)", rest)
            if mm:
                facts.append({"e": e, "p": "has:" + mm.group(2), "val": mm.group(1) == "has",
                              "form": {"has": "pos", "does not have": "not", "lacks": "lacks"}[mm.group(1)]})
                continue
            raise ValueError(f"S3 fact {s!r}")
        if re.search(ID, s):
            raise ValueError(f"S3 unparsed sentence with an ID: {s!r}")
        inert.append(s)
    return {"world": consts["world"], "univ": univ, "facts": facts, "inert": inert, "noun": noun, "decoys": decoys}


def canon_gen(M):
    return {"univ": sorted(json.dumps(u, sort_keys=True) for u in M["univ"]),
            "facts": sorted(json.dumps({"e": f["e"], "p": f["p"], "val": f["val"],
                                        "form": "pos" if f["form"] == "decoy" else f["form"]}, sort_keys=True)
                            for f in M["facts"])}


def canon_parsed(S):
    return {"univ": sorted(json.dumps(u, sort_keys=True) for u in S["univ"]),
            "facts": sorted(json.dumps({k: f[k] for k in ("e", "p", "val", "form")}, sort_keys=True)
                            for f in S["facts"])}


# solver B ----------------------------------------------------------------------------------------------------------

def _atoms(S, lfs):
    ents, preds = set(), set()
    for f in S["facts"]:
        ents.add(f["e"])
        preds.add(f["p"])
    for u in S["univ"]:
        preds |= {u["a"], u["b"]}

    def walk(x):
        if isinstance(x, list) and x:
            if x[0] in ("adj", "has") and len(x) == 3:
                ents.add(x[1].rsplit(" ", 1)[1])
                preds.add(f"{x[0]}:{x[2]}")
            elif x[0] == "grp":
                preds.add(f"{x[3][0]}:{x[3][1]}")
            else:
                for y in x[1:]:
                    walk(y)
    for lf in lfs:
        walk(lf)
    return sorted(ents), sorted(preds)


def models(S, lfs):
    ents, preds = _atoms(S, lfs)
    atoms = [(e, p) for e in ents for p in preds]
    fixed = {}
    for f in S["facts"]:
        fixed[(f["e"], f["p"])] = f["val"]
    free = [a for a in atoms if a not in fixed]
    closed = S["world"] == "closed"
    out = []
    for bits in itertools.product([False, True], repeat=len(free)):
        w = dict(fixed)
        w.update(zip(free, bits))
        ok = True
        for u in S["univ"]:
            for e in ents:
                a, b = w[(e, u["a"])], w[(e, u["b"])]
                if u["q"] == "every" and a and not b:
                    ok = False
                if u["q"] == "no" and a and b:
                    ok = False
        if ok and closed:
            # completion: an atom holds iff it is a stated positive fact or some 'every' universal gives it
            for (e, p) in atoms:
                sup = fixed.get((e, p)) is True or any(u["q"] == "every" and u["b"] == p and w[(e, u["a"])]
                                                      for u in S["univ"])
                if w[(e, p)] != sup:
                    ok = False
                    break
        if ok:
            out.append(w)
    return out, ents


def _eval(lf, w, ents):
    op = lf[0]
    if op == "not":
        return not _eval(lf[1], w, ents)
    if op == "and":
        return all(_eval(x, w, ents) for x in lf[1:])
    if op == "or":
        return any(_eval(x, w, ents) for x in lf[1:])
    if op in ("adj", "has"):
        return w[(lf[1].rsplit(" ", 1)[1], f"{op}:{lf[2]}")]
    if op == "grp":
        _, Q, noun, pred, exc = lf
        p = f"{pred[0]}:{pred[1]}"
        vals = [w[(e, p)] for e in ents if e != exc]
        return all(vals) if Q == "every" else any(vals)
    raise ValueError(op)


def solve_b(S, lfs):
    ms, ents = models(S, lfs)
    if not ms:
        raise ValueError("no model")
    out = []
    for lf in lfs:
        vals = {_eval(lf, w, ents) for w in ms}
        if len(vals) != 1:
            raise ValueError("undetermined")
        out.append(vals.pop())
    return out


def triggers(S):
    keys = {"SEM-01", "SEM-02" if S["world"] == "closed" else "SEM-03", "SEM-22"}
    if S.get("decoys"):
        keys.add("SEM-28")
    if any(f["form"] == "aff" for f in S["facts"]):
        keys.add("SEM-18")
    if any(f["form"] == "lacks" for f in S["facts"]):
        keys.add("SEM-19")
    return keys


# question forms --------------------------------------------------------------------------------------------------

def decl(c, st, ctx):
    m = re.fullmatch(r"(not every|no|some|every) (.+?) in this record(?: other than (.+? " + ID + r"))? "
                     r"(is [a-z-]+|has a .+)", c)
    if not m:
        return None
    q, noun, exc, vp = m.groups()
    p = _pred(vp, ctx)
    pred = p.split(":", 1)
    exc_id = exc.rsplit(" ", 1)[1] if exc else None
    if exc:
        st.add("C11")
    if q == "not every":
        st.add("C8")
        return ["not", ["grp", "every", noun, pred, exc_id]]
    if q == "no":
        st.add("C8")
        return ["not", ["grp", "some", noun, pred, exc_id]]
    return ["grp", q, noun, pred, exc_id]


def matrix(body, st, ctx):
    m = re.fullmatch(r"Among the (.+?) in this record, (?:is any (.+?) other than (.+? " + ID + r") ([a-z-]+)|does any "
                     r"(.+?) other than (.+? " + ID + r") have a (.+))", body)
    if not m:
        return None
    st.add("C11")
    if m.group(2):
        return ["grp", "some", m.group(2), ["adj", m.group(4)], m.group(3).rsplit(" ", 1)[1]]
    return ["grp", "some", m.group(5), ["has", m.group(7)], m.group(6).rsplit(" ", 1)[1]]


def decl_parsers():
    return [decl], [matrix]
