"""Rules-kind card text (switch sentences per card variant + policy) and question / option construction."""
from __future__ import annotations

from . import render_f6 as RF
from . import rowmake as M
from .lex import sw, FRAMES


def reading_lines(P: dict, R: dict, V: dict, form: str, ds: str, decision_list: bool, attack: bool) -> list[str]:
    """Every switch sentence the card variant needs, in a fixed order (fixed per card variant, never per row)."""
    D = RF.fmt_date(R["D"], "name")
    L = []
    L += M.world_lines(V, R["D"], "name")
    L += M.marker_lines(V)
    L += M.evidence_lines(V)
    L.append(sw("r30"))
    L.append(sw("r32"))
    L.append(sw("r18", D=D))
    L.append(sw("r18_rules"))
    nums = [a for a in R["attr_order"] if R["attrs"][a]["kind"] == "num"]
    for aid in nums:
        a = R["attrs"][aid]
        L.append(sw("r20_qdom", q=a["name"], unit=a["unit"], lo=a["lo"], hi=a["hi"]))
    for aid in R["attr_order"]:
        a = R["attrs"][aid]
        if a["kind"] == "cat":
            L.append(sw("r43", attr=a["name"], vals=RF.join_or_vals(a["vals"])))
    if nums and not P.get("pure_table"):          # repair r1 v3b: comparison words occur only in threshold conditions (rows 11-12; G3 needs them
        L.append(sw("r11") if P["cmp_family"] == "incl" else sw("r12"))   # only when an operator is used)
    if R["rules"] or not P.get("pure_table"):   # repair r1 v3c: a pure outcome-table card has no "if" rule (distinct
        L.append(sw("r10"))                        # cell outcomes, no only-if), so row 10 can flip no label there
    if P["unless"]:
        L.append(sw("r8"))
    if P["onlyif"]:
        L.append(sw("r9"))
    L.append(sw("r7", Od=f'"{V["out_names"][R["default"]]}"'))
    has_exc = P["exc"] or bool(R.get("table") and any(r.get("exc", "") and str(r.get("exc")).startswith("T:")
                                                         for r in R["rules"]))
    has_sub = P["sub"]
    L.append(sw("r24" if has_exc and has_sub else "r24_exc" if has_exc else "r24_sub" if has_sub else "r24_date"))
    if decision_list:
        L.append(sw("r24_list"))
    if P["exc"] or P["sub"]:
        L.append(sw("r44"))
    L.append(sw("r45"))
    L.append(sw("r49"))
    if R.get("table"):
        T = R["table"]
        L.append(sw("r53_short", t=V["table_num"], A=R["attrs"][T["A"]]["name"], B=R["attrs"][T["B"]]["name"]))
    if P.get("order_gaps"):
        L.append(sw("r15_date"))
        L.append(sw("r17"))
    if form == "c_out":
        L += M.abstain_lines(V)
    if form == "c_gap":
        L.append(sw("r51", NOTHING=V["nothing"]))
    if form == "c_case":
        L.append(sw("r52"))
    L += M.frame_lines(V)
    return L


def claim_text(R: dict, claim: dict, case: str, names: dict) -> str:
    o = names["out"][claim["o"]]
    if claim.get("neg"):
        return f'the outcome for {case} is not "{o}"'
    return f'the outcome for {case} is "{o}"'


def question_text(form: str, frame: str, R: dict, claim: dict | None, case: str, names: dict, inversion: bool) -> str:
    if form in ("qdet", "qest", "qplain"):
        S = claim_text(R, claim, case, names)
        if form == "qplain" and inversion and not claim.get("neg"):
            o = names["out"][claim["o"]]
            return f'Is the outcome for {case} "{o}"?'
        return FRAMES[frame].format(S=S)
    if form == "c_out":
        return FRAMES["c_out"].format(case=case)
    if form == "c_gap":
        return FRAMES["c_gap"].format(q=f"which outcome applies to {case}")
    if form == "c_case":
        return FRAMES[frame]
    raise ValueError(form)


def gap_text(R: dict, var, case: str, alt: bool = False) -> str:
    """C-GAP option text for one gap. Repair r1 (G7 'longest option'; F6-QC-2): each option takes its short or long
    wording by a label-free coin (`alt`), so option length never tells a decisive gap from a trap gap."""
    k = var[0]
    if k in ("num", "cat"):
        a = R['attrs'][var[1]]['name']
        return f"the value of the {a} of {case}" if alt else f"the {a} of {case}"
    if k == "ev":
        e = chr(34) + R["events"][var[1]]["name"] + chr(34)
        return f"whether {RF.a_or_an(e)} event happened for {case}" if alt else \
            f'whether {case} had {RF.a_or_an(e)} event'
    if k == "cls":
        c = R['classes'][var[1]]['name']
        return f"whether {case} counts as {RF.a_or_an(c)}" if alt else f"whether {case} is {RF.a_or_an(c)}"
    if k == "nd":
        return f"the effective date of {R['notices'][var[1]]['name']}"
    raise ValueError(k)
