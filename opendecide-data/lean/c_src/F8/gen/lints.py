"""Text lints on rendered rows (G0 spec 5 'Banned phrases', 1 'Rules that hold for every form', 12 lints).

lint_row(row, sems) -> list of problems (empty = pass). Run before parsing (G3 check 4) and again in the gate script.
"""
from __future__ import annotations

import re

import lexicon as L

_RS = L.RECORD_STATUS_RE
_JUDGE = re.compile(r"\b(wrong|right|reject|rejected|accept|accepted|should|would)\b", re.I)
_LABEL_CHECK = re.compile(r"\bIs the correct answer\b", re.I)
_UNLESS = re.compile(r"\bunless\b", re.I)
_ONLYIF = re.compile(r"\bonly if\b", re.I)
_MISSING = re.compile(r"(?<![A-Za-z])(N/A|n/a|TBD|unknown|not stated|pending)(?![A-Za-z])|\?\s*$|(?<=: )-(?=\s|$)")
_NUMDATE = re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b")
_FLOAT = re.compile(r"\de[-+]?\d")


def _strip_markers(t: str) -> str:
    return re.sub(r"not recorded", "", t, flags=re.I)


def lint_row(row: dict, sem_lines) -> list:
    """sem_lines: {SEM base id: [rendered texts]} of the row's card version (exemptions are by SEM id)."""
    if isinstance(sem_lines, list):
        sem_lines = {"SEM-01": sem_lines}

    def ex(*ids):
        return [t for i in ids for t in sem_lines.get(i, [])]
    probs = []
    card = row.get("card") or ""
    instr = row.get("instructions") or ""
    state = row.get("state") or ""
    opts = row.get("options") or []
    allt = "\n".join([card, instr, state] + list(opts))
    for rx in L.BANNED_RES:
        if rx.search(allt):
            probs.append(f"banned phrase {rx.pattern[:24]!r}")
    # record-status words only in the marker forms and SEM-01/02/03 lines
    t = allt
    for s in ex("SEM-01", "SEM-02", "SEM-03"):
        t = t.replace(s, "")
    if _RS.search(_strip_markers(t)):
        probs.append("record-status word outside the marker forms (F8-R4-06)")
    # 'unless' only in points-line exceptions and SEM-04 / SEM-15
    t2 = allt
    for s in ex("SEM-04", "SEM-15"):
        t2 = t2.replace(s, "")
    for ln in t2.split("\n"):
        if _UNLESS.search(ln) and not re.search(r": [+-]\d+ points?, unless ", ln):
            probs.append("'unless' outside a points-line exception (F8-R2-05)")
            break
    t3 = allt
    for s in ex("SEM-05", "SEM-15"):
        t3 = t3.replace(s, "")
    for ln in t3.split("\n"):
        if _ONLYIF.search(ln) and not re.search(r"Tier '[^']+' only if ", ln):
            probs.append("'only if' outside a tier limit (F8-AMB-09)")
            break
    if _NUMDATE.search(allt):
        probs.append("numeric date")
    if _LABEL_CHECK.search(allt):
        probs.append("label-check form")
    if re.search(r"\brisk\b", instr + card, re.I) and not re.search(r"the risk of a .+ means its", allt):
        probs.append("'risk' without SEM-22")
    # missing-value lexicon (closed): only 'not recorded'
    for ln in state.split("\n"):
        if _MISSING.search(ln.strip()):
            probs.append("missing-value marker outside the closed lexicon")
            break
    # question frame (XF10): no outer judgement or acceptance predicate
    q = row.get("_q") or ""
    if _JUDGE.search(q):
        probs.append("judgement / acceptance frame in the question (XF10)")
    # choice rows: card lines are '- <option>: <definition>' with no digit or comparator word
    if row.get("qtype") == "choice" and card:
        for ln in card.split("\n"):
            if not ln.startswith("- ") or ": " not in ln:
                probs.append("choice card line that is not an option definition")
                break
            d = ln.split(": ", 1)[1]
            if re.search(r"\d", d) or re.search(r"\b(above|below|over|under|least|most|more than|less than|"
                                                r"no fewer than|exceeds)\b", d):
                probs.append("definition line with a digit or comparator word")
                break
        if any(": " in o for o in opts):
            probs.append("option text with ': ' on a row with definitions")
    if row.get("qtype") == "noul" and card:
        if any(ln.startswith(("- Yes: ", "- No: ")) for ln in card.split("\n")):
            probs.append("yes/no card with a '- Yes: ' / '- No: ' line")
    if any("\n" in o for o in opts):
        probs.append("option with a line break")
    if len(opts) and not (2 <= len(opts) <= 60):
        probs.append("option count outside 2..60")
    if len(set(opts)) != len(opts):
        probs.append("duplicate options")
    if _FLOAT.search(allt):
        probs.append("exponent float text")
    return probs
