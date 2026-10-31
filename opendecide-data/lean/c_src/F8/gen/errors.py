"""Named errors E1-E16 as alternative readings of one structure (G0 spec 3 'Named errors', 1 'Distractors').

named_errors(S) -> {error id: answer under that error} for the error ids the spec lists for the row's form.
A choice row needs >= 1 named error whose answer maps to an option other than gold (else the structure is redrawn);
the sidecar's distractor_errors maps each such option to its error ids.
"""
from __future__ import annotations

from solver_a import CV, Undetermined, solve

E = {
    "E1": [CV(post="inverse")],
    "E2": [CV(post="neglect")],
    "E3": [CV(post="joint")],
    "E4": [CV(bin_edge="other"), CV(cut_edge="lower"), CV(lvl_edge="other")],
    "E5": [CV(cmp="swap", cmp_class="amt"), CV(cmp="swap", cmp_class="q"), CV(cmp="swap", cmp_class="inv")],
    "E6": [CV(unless="ignore")],
    "E7": [CV(**{"or": "xor"}), CV(xor1="inclusive"), CV(xor1="atmost1"), CV(or_count="per_part")],
    "E8": [CV(clamp="none"), CV(override="ignore"), CV(only_if="ignore"), CV(only_if="sufficient"),
           CV(only_if="one_down"), CV(only_if="skip_to_no_limit"), CV(only_if="bottom"), CV(tier_by_name=True)],
    "E9": [CV(own_cost="exclude"), CV(own_cost="twice")],
    "E10": [CV(remainder="rescale")],
    "E12": [CV(rank_by="chance"), CV(rank_by="amount"), CV(risk="chance"), CV(risk="amount"), CV(risk="el")],
    "E15": [CV(grid="transposed")],
    "E16": [CV(post="prior")],
}
BY_FORM = {
    "bin": ["E1", "E2", "E3", "E10", "E16", "E4"],
    "tier": ["E5", "E6", "E7", "E8", "E4"],
    "mat": ["E15", "E10", "E12", "E4"],
    "rank_top": ["E12", "E9", "E10", "E1", "E2", "E6", "E7", "E8"],
    "rank_order": ["E12", "E9", "E10", "E1", "E2", "E6", "E7", "E8"],
    "dec": ["E9", "E10", "E12"],
    "pred": ["E1", "E16"],
    "inv": ["E1", "E2", "E3", "E5", "E6", "E7", "E8", "E9", "E10", "E12", "E16"],
}
MAT_IMPACT = {"loss": [CV(impact="expected")], "expected": [CV(impact="amount")]}


INV_BY_Q = {"el": ["E5", "E10"], "tec": ["E5", "E9", "E10"], "score": ["E5", "E6", "E7", "E8"],
            "chance": ["E5"], "post": ["E1", "E2", "E3", "E5", "E16"]}


def named_errors(S: dict) -> dict:
    """{error id: [answers]} for the form's error list (answers under each reading that is defined)."""
    out = {}
    ids = BY_FORM.get(S["form"], [])
    if S["form"] == "inv" and S["rules"]["inv"]["kind"] == "q":
        ids = INV_BY_Q.get(S["rules"]["inv"]["q"]["k"], ids)
    for eid in ids:
        cvs = list(E[eid])
        if S["form"] == "mat" and eid in ("E10", "E12"):
            if S["rules"]["mat"]["impact"] != "expected":
                continue
            cvs = MAT_IMPACT["expected"]
        if S["form"] == "dec" and eid == "E12":
            cvs = [CV(rank_by="amount"), CV(rank_by="chance")]
        res = []
        for cv in cvs:
            try:
                r = solve(S, cv)
            except (Undetermined, ValueError, ZeroDivisionError, KeyError, IndexError, TypeError):
                continue
            if r["det"]:
                res.append(r["ans"])
        if res:
            out[eid] = res
    return out


def distractor_map(S: dict, gold, key_of=lambda a: a) -> dict:
    """{answer key: [error ids]} for named-error answers that differ from gold."""
    m = {}
    for eid, answers in named_errors(S).items():
        for a in answers:
            k = key_of(a)
            if k is None or k == gold:
                continue
            m.setdefault(k, [])
            if eid not in m[k]:
                m[k].append(eid)
    return m


def has_distractor(S: dict, gold) -> bool:
    """True when some named error moves the answer to another single option (an index, an ordering, CBD or NOTA)."""
    for k in distractor_map(S, gold):
        if isinstance(k, tuple) and k and k[0] == "MULTI":
            continue
        return True
    return False
