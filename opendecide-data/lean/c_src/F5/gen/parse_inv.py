"""Inverted-card G3 parser: the case list and the named rule from the card, the case facts from the state (sentences on
S1 cards, a records table on S4 cards); solver B evaluates the parsed rule's conditions per case with its own code."""
from __future__ import annotations

import json
import re

from . import parse as PZ
from . import parse_s4

ID = r"[A-Z]{1,4}-[A-Z0-9]+(?:-[A-Z0-9]+)?"
BOUNDS = {"at least": ">=", "more than": ">", "at most": "<=", "less than": "<"}


def parse(rs, consts):
    r = next((x for x in rs if x["role"] != "attack"), rs[0])
    card = " ".join(r["card"].split())
    m = re.search(r"Cases under review: (.+?)\.(?: |$)", card)
    cases = [x.strip() for x in m.group(1).split(", ")]
    noun = cases[0].rsplit(" ", 1)[0]
    m = re.search(r"Rule for this task: R\d+\. If (.+?), then the (.+?) is ([a-z]+)\.", card)
    conds = []
    for t in m.group(1).split(" and "):
        mm = re.fullmatch(rf"the (.+?) of the {re.escape(noun)} is (at least|more than|at most|less than) (\d+) (.+)", t)
        if mm:
            conds.append({"t": "num", "op": BOUNDS[mm.group(2)], "n": int(mm.group(3))})
            continue
        mm = re.fullmatch(rf"the (.+?) of the {re.escape(noun)} is (not )?(.+)", t)
        if mm:
            conds.append({"t": "cat", "v": mm.group(3), "pol": "not" if mm.group(2) else "pos"})
            continue
        mm = re.fullmatch(rf"the {re.escape(noun)} is (not )?([a-z]+)", t)
        if mm:
            conds.append({"t": "adj", "w": mm.group(2), "pol": "not" if mm.group(1) else "pos"})
            continue
        raise ValueError(f"inverted rule literal {t!r}")
    out = m.group(3)
    facts = {c.rsplit(" ", 1)[1]: {"flags": {}, "qty": None, "cat": None} for c in cases}
    try:
        hdr, rows, nulls = parse_s4.table(r["state"])
        for row in rows:
            f = facts[row[0]]
            for h, v in zip(hdr[1:], row[1:]):
                mm = re.fullmatch(r"(\d+) .+", v)
                if v in ("yes", "no"):
                    f["flags"][h] = v == "yes"
                elif mm:
                    f["qty"] = int(mm.group(1))
                else:
                    f["cat"] = v
        form = "s4"
    except ValueError:
        sents, _ = PZ.sentences(r["state"])
        for s in sents:
            mm = re.fullmatch(rf"The (.+?) of .+? ({ID}) is (\d+) .+\.", s)
            if mm:
                facts[mm.group(2)]["qty"] = int(mm.group(3))
                continue
            mm = re.fullmatch(rf"The (.+?) of .+? ({ID}) is (.+)\.", s)
            if mm:
                facts[mm.group(2)]["cat"] = mm.group(3)
                continue
            mm = re.fullmatch(rf"[A-Z][a-z ]+ ({ID}) is ([a-z]+)\.", s)
            if mm:
                facts[mm.group(1)]["flags"][mm.group(2)] = True
                continue
            if re.search(ID, s) and not PZ.ATT.fullmatch(s):
                raise ValueError(f"inverted fact {s!r}")
        form = "s1"
    return {"cases": facts, "conds": conds, "out": out, "noun": noun, "form": form, "world": "closed"}


def canon_gen(M):
    return {"cases": sorted(c["id"] for c in M["cases"]), "conds": json.dumps(
        [{k: v for k, v in l.items()} for l in M["rule"]["conds"]], sort_keys=True), "out": M["rule"]["out"],
        "facts": sorted(json.dumps({"id": c["id"], "true_flags": sorted(w for w, x in c["flags"].items() if x),
                                    "qty": c["qty"], "cat": c["cat"]}, sort_keys=True) for c in M["cases"])}


def canon_parsed(S):
    return {"cases": sorted(S["cases"]), "conds": json.dumps(S["conds"], sort_keys=True), "out": S["out"],
            "facts": sorted(json.dumps({"id": i, "true_flags": sorted(w for w, x in f["flags"].items() if x),
                                        "qty": f["qty"], "cat": f["cat"]}, sort_keys=True)
                            for i, f in S["cases"].items())}


def _cond(f, l):
    if l["t"] == "adj":
        x = f["flags"].get(l["w"], False)           # closed: an unstated flag is false
        return x == (l["pol"] == "pos")
    if l["t"] == "num":
        return {">=": f["qty"] >= l["n"], ">": f["qty"] > l["n"], "<=": f["qty"] <= l["n"],
                "<": f["qty"] < l["n"]}[l["op"]]
    return (f["cat"] == l["v"]) == (l["pol"] == "pos")


def _eval(lf, S):
    op = lf[0]
    if op == "not":
        return not _eval(lf[1], S)
    if op == "and":
        return all(_eval(x, S) for x in lf[1:])
    if op == "inv":
        f = S["cases"][lf[1].rsplit(" ", 1)[1]]
        if lf[2] != S["out"]:
            raise ValueError("outcome not named by the rule")
        return all(_cond(f, l) for l in S["conds"])
    if op == "adj":
        return S["cases"][lf[1].rsplit(" ", 1)[1]]["flags"].get(lf[2], False)
    raise ValueError(op)


def solve_b(S, lfs):
    return [_eval(lf, S) for lf in lfs]


def triggers(S):
    keys = {"SEM-01", "SEM-02", "SEM-12", "SEM-14"}
    if any(f["cat"] for f in S["cases"].values()):
        keys.add("SEM-17")
    return keys


def decl(c, st, ctx):
    m = re.fullmatch(rf"(.+? {ID}) is (not )?(?:(only|neither) )?among the cases that are ([a-z]+)(?: (but also|nor) "
                     rf"([a-z]+))?", c)
    if not m:
        return None
    s, neg, mod, O, conj, w = m.groups()
    P = ["inv", s, O]
    if mod == "only":
        st.fams.append("C16")
        return ["and", P, ["adj", s, w]]
    if mod == "neither":
        st.add("C13")
        return ["and", ["not", P], ["not", ["adj", s, w]]]
    if neg:
        st.add("C1")
        return ["not", P]
    return P


def matrix(body, st, ctx):
    m = re.fullmatch(rf"Is (.+? {ID}) among the cases that are ([a-z]+)", body)
    if m:
        return ["inv", m.group(1), m.group(2)]
    return None


def decl_parsers():
    return [decl], [matrix]
