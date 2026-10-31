"""F6 gates run by the generator: G3 round trip (parse + canonical compare + solver B label), G2 agreement,
G15 (check_rows + fmt1 loader_check under a random permutation, done at render time and re-run here), token caps."""
from __future__ import annotations

from . import common  # noqa: F401  (sys.path for fmt1)

import random

from . import parse_f6 as PF, canon_f6 as CF, solver_b as B
from fmt1 import card as fcard


def label_b(S: dict, row: dict, Q: dict, O: dict):
    """Solver B's label for a parsed rules-kind row."""
    case = Q["case"]
    form = Q["form"]
    if form == "c_out":
        PB = B.possible(S, case)
        conc = O["concrete"]
        inter = [o for o in conc if o in PB]
        if len(PB) == 1 and inter:
            return inter[0]
        if not inter:
            if "none" in O["abstain"]:
                return O["abstain"]["none"]
            raise B.Dropped("None gold not displayed")
        if len(PB) >= 2 and "nei" in O["abstain"]:
            return O["abstain"]["nei"]
        raise B.Dropped("NEI gold not displayed")
    if form == "c_gap":
        gaps = [tuple(g) for g in O["gaps"]]
        st = B.settling(S, case, gaps)
        if not st:
            return O["nothing"]
        if len(st) != 1:
            raise B.Dropped("settling set size")
        g = tuple(st[0])
        for t, gg in zip([x for x in O["texts"] if x != O["nothing"]], O["gaps"]):
            if tuple(gg) == g:
                return t
        raise B.Dropped("settling gap text")
    T = B.possible(S, case, Q["claim"])
    fr = Q["frame"]
    if form == "qdet":
        settled = len(T) == 1
        if fr in ("qdet_leave", "qdet_imp"):
            return 0 if settled else 1
        return 1 if settled else 0
    if form == "qest":
        return 1 if T == {True} else 0
    if form == "qplain":
        if len(T) != 1:
            raise B.Dropped("qplain open")
        return 1 if T == {True} else 0
    raise ValueError(form)


def g3_case(row, side, S, Q) -> list[str]:
    probs = []
    st = side["struct"]
    for lab in Q["cases"]:
        G = CF.gen_named_view(st["R"], lab, st["outmap"])
        if CF.canon(G, lab, named=False) != CF.canon(S, lab, named=True):
            import json
            a, b = json.loads(CF.canon(G, lab, named=False)), json.loads(CF.canon(S, lab, named=True))
            probs.append(f"structure differs ({lab}): {[k for k in a if a[k] != b.get(k)]}")
            break
    try:
        dec = B.decidable(S, Q["cases"])
    except B.Dropped as e:
        return probs + [f"solver B drop: {e}"]
    want = Q["frame"] == "c_case_can"
    if side.get("decidable") is not None and sorted(dec) != sorted(side["decidable"]):
        probs.append("G2: decidable sets differ")
    cand = dec if want else [c for c in Q["cases"] if c not in dec]
    if len(cand) != 1 or cand[0] != row["gold"]:
        probs.append(f"solver B case set {cand} != gold {row['gold']}")
    return probs


def g3_rules(row: dict, side: dict, wordings: set) -> list[str]:
    """[] when the row parses back to the same canonical structure and solver B gives the row's gold."""
    probs = []
    try:
        S = PF.parse_row(row, wordings)
        Q = PF.parse_question(S, row)
        if Q["form"] == "c_case":
            PF.parse_facts(S, row, Q["cases"])
            return g3_case(row, side, S, Q)
        cases = [Q["case"]]
        PF.parse_facts(S, row, cases)
        O = PF.parse_options(S, row, Q)
    except PF.ParseError as e:
        return [f"parse: {e}"]
    st = side["struct"]
    G = CF.gen_named_view(st["R"], st["case"], st["outmap"])
    cg = CF.canon(G, st["case"], named=False)
    cp = CF.canon(S, Q["case"], named=True)
    if cg != cp:
        import json
        a, b = json.loads(cg), json.loads(cp)
        diff = [k for k in a if a[k] != b.get(k)]
        probs.append(f"structure differs: {diff}")
    try:
        lb = label_b(S, row, Q, O)
        if lb != row["gold"]:
            probs.append(f"solver B label {lb!r} != gold {row['gold']!r}")
        # G2: the full sets agree, not only the letter (P over the whole catalog; T for claims)
        PB = B.possible(S, Q["case"])
        if sorted(PB) != sorted(side["p_set"]):
            probs.append("G2: P_A != P_B")
        if Q.get("claim") is not None and side.get("t_set") is not None:
            TB = B.possible(S, Q["case"], Q["claim"])
            if sorted(TB) != sorted(side["t_set"]):
                probs.append("G2: T_A != T_B")
    except B.Dropped as e:
        probs.append(f"solver B drop: {e}")
    return probs


def g3_row(row: dict, side: dict, wordings: set) -> list[str]:
    kind = side.get("kind")
    if kind == "rules":
        return g3_rules(row, side, wordings)
    if kind == "table":
        from . import s3
        return s3.g3(row, side, wordings)
    if kind == "timeline":
        from . import s4
        return s4.g3(row, side, wordings)
    return [f"unknown kind {kind}"]
