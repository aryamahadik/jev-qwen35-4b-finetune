"""G2 / G3 per row for program rows: parse the rendered row (parse.py), rebuild the canonical structure and compare
its hash with the generator's; solver B on the parsed structure must give the row's gold; every example in the card
must meet its own definition and no other term definition (pass rule 3)."""
from __future__ import annotations

import canon
import parse as PZ
from solver_b import CardB

WK = {"s3_meets": "meets", "s3_assigned": "assigned"}


def gen_query(card, spec):
    f = spec["form"]
    q = {"form": f}
    if f == "choice":
        q["wkind"] = "defines" if card["sampler"] == "S6" else "assigned"
        q["neg"] = 0
        q["shown"] = list(spec["options"])
    elif f == "yn":
        q["wkind"] = "defines" if card["sampler"] == "S6" else spec["wkind"]
        q["neg"] = spec.get("neg", 0)
        q["target"] = spec["ask"]
    else:
        q["wkind"], q["neg"], q["target"] = "meets", 0, spec["ask"]
        import json
        q["records"] = sorted([json.dumps({str(k): (list(v) if isinstance(v, tuple) else v) for k, v in sorted(c.items())},
                                          sort_keys=True, default=list) for c in spec["records"]])
    if card["sampler"] == "S6":
        import model as M
        q["desc"] = M.canon_def({"desc": M.Def("desc", spec["desc"])}, "desc")
    if f != "inv" and card["sampler"] != "S6":
        om = spec.get("omitted", [])
        q["case"] = {str(k): (list(v) if isinstance(v, tuple) else v) for k, v in sorted(spec["case"].items()) if k not in om}
        q["omitted"] = sorted(om)
    return q


def gen_hash(c, spec):
    cl = {"ctype": c["ctype"], "legend": c["legend"], "defs": c["defs"], "order": c["order"],
          "world": c["world"] if c["sampler"] != "S6" else None}
    st = canon.structure(cl, gen_query(c, spec))
    return canon.shash(st), st


def _norm_case(case):
    return {k: (tuple(v) if isinstance(v, list) else v) for k, v in case.items()}


def solve_parsed(pr, row):
    """Solver B gold on the parsed structure (option text or 1 / 0)."""
    cl, q = pr["card_like"], pr["query"]
    cb = CardB(cl["legend"], cl["defs"], cl["order"], cl["ctype"])
    form = q["form"]
    if form == "inv":
        X = q["target"]
        hits = [lab for lab, c in pr["records"].items() if cb.meets(X, c) is True]
        if len(hits) != 1:
            raise PZ.ParseError("inverted: not exactly one record meets the target")
        return hits[0]
    if "description" in pr:
        sp = cb.sp
        cb.defs = dict(cl["defs"])
        cb.defs["desc"] = pr["description"]
        Rd = cb.region("desc")
        eq = [t for t in cl["order"] if sp.equal(Rd, cb.region(t))]
        if len(eq) != 1:
            raise PZ.ParseError("description equals no single term")
        if form == "choice":
            g = eq[0]
            if g not in pr["opt_keys"]:
                raise PZ.ParseError("description gold not shown")
            return row["options"][pr["opt_keys"].index(g)]
        v = q["target"] == eq[0]
        return int(v if q["neg"] in (0, 2) else not v)
    case, om = _norm_case(pr["case"]), pr["omitted"]
    if form == "yn":
        wk = WK.get(q["wkind"], q["wkind"])
        v = cb.meets(q["target"], case, om) if wk == "meets" else cb.assigned(q["target"], case, om)
        if v is None:
            raise PZ.ParseError("yes/no answer undetermined")
        return int(v if q["neg"] in (0, 2) else not v)
    P = cb.possible(case, om)
    keys = pr["opt_keys"]
    shown_terms = [k for k in keys if k not in ("none", "cbd")]
    if len(P) == 1:
        p = next(iter(P))
        if p not in keys:
            raise PZ.ParseError("determined answer not shown")
        return row["options"][keys.index(p)]
    if not any(t in shown_terms for t in P if t != "none"):
        raise PZ.ParseError("XF15: undetermined with no shown possible term")
    if "cbd" not in keys:
        raise PZ.ParseError("undetermined but no cbd option")
    return row["options"][keys.index("cbd")]


def check_examples(pr):
    cl = pr["card_like"]
    cb = CardB(cl["legend"], cl["defs"], cl["order"], cl["ctype"])
    sp = cb.sp
    names = {d[2:]: d for d in cl["order"]}
    bad = 0
    for (stated, case), name, s3 in pr["examples"]:
        X = names.get(name)
        if X is None:
            bad += 1
            continue
        om = [s for s in cl["legend"] if s not in stated]
        box = sp.point_box(_norm_case({**{s: 0 for s in om}, **case}), om)
        if not sp.box_in(box, cb.region(X)):
            bad += 1
            continue
        if any(sp.box_meets(box, cb.region(t)) for t in cl["order"] if t != X):
            bad += 1
    return bad


def g3_row(row, spec, card_shown, container, pack_attrs):
    """Problems list (empty = G2 and G3 pass on this row)."""
    probs = []
    try:
        pr = PZ.parse_program_row(row, container, card_shown["sampler"], pack_attrs, card_shown.get("prose_record"))
    except PZ.ParseError as e:
        return [f"parse: {e}"], None
    q = pr["query"]
    q["wkind"] = WK.get(q["wkind"], q["wkind"])
    if "description" in pr:
        import model as M
        q["desc"] = M.canon_def({"desc": pr["description"]}, "desc")
    st = canon.structure(pr["card_like"], q)
    hp = canon.shash(st)
    hg, stg = gen_hash(card_shown, spec)
    if hp != hg:
        diff = [k for k in st if st[k] != stg.get(k)]
        if "query" in diff:
            diff += ["q." + k for k in st["query"] if st["query"].get(k) != stg["query"].get(k)]
        probs.append(f"structure_hash differs: {diff}")
    try:
        gb = solve_parsed(pr, row)
        if gb != row["gold"]:
            probs.append(f"G2: solver B {gb!r} != gold {row['gold']!r}")
    except PZ.ParseError as e:
        probs.append(f"G2 solve: {e}")
    nb = check_examples(pr)
    if nb:
        probs.append(f"examples: {nb} fail")
    return probs, hg
