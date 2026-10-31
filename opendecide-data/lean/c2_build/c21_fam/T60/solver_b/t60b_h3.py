"""T60 solver B, head H3 PLAN-OR-ACT (G0_LITE section 3.3, ROW_SCHEMA H3). String side: parse the card numbers (H, n_min), the steps with their
visible effects, the order statements and the data-flow lines, then apply R1 and R2 and R3.

R1 some step is HIGH STAKES: not undoable, or reaches outside the team, or changes N >= H units (shared definition D3 as amended: a create
of an agent-made, non-external object is undoable).
R2 the number of steps >= n_min.
R3 some data-flow edge is NOT implied by the transitive closure of the stated order (the request gives a goal, not that order). A numbered-list statement
states every consecutive pair; "sB uses a value derived from the output of sA" is the same dependency as "sB uses the output of sA".
PLAN iff R1 and R2 and R3, else ACT."""
import re

try:
    from .t60b_text import ParseGap, Rx, clause, lines_of, one_number, strip_notes
except ImportError:
    from t60b_text import ParseGap, Rx, clause, lines_of, one_number, strip_notes

_RE_STEP = Rx(r"^-\s*(s\d+):\s*(.*?)\s*\(changes\s+(\d+)\s+([^;()]*?);\s*(.*)\)\s*$")
_RE_FLOW = Rx(r"^-\s*(s\d+)\s+uses (?:a value derived from )?the output of\s+(s\d+)\s*\.?\s*$")     # also: "sB uses a value derived from the output of sA"
_NUMBERED = Rx(r"^-\s*the steps are numbered in the order in which they are to be carried out\s*\.?\s*$", re.I)
_ORDER_FWD = (Rx(r"\bDo step (s\d+) before step (s\d+)\b", re.I),
              Rx(r"\bStep (s\d+) has to come before step (s\d+)\b", re.I),
              Rx(r"\bStep (s\d+) (?:must|should|needs to) (?:come|run|go) before step (s\d+)\b", re.I),
              Rx(r"\bRun step (s\d+) before step (s\d+)\b", re.I))
_ORDER_BACK = (Rx(r"\bStep (s\d+) (?:has to|must|should) come after step (s\d+)\b", re.I),
               Rx(r"\bDo step (s\d+) after step (s\d+)\b", re.I))
_NO_ORDER = Rx(r"^-\s*no order is given\s*\.?\s*$", re.I)

# effect phrases (ROW_SCHEMA): each is either undoable or high stakes by itself
_UNDOABLE_PAT = (Rx(r"^can be undone for (\d+) more days?$"),
                 Rx(r"^creates a new object that can be removed again$"),
                 Rx(r"^the working tree is clean, so git can restore it$"),
                 Rx(r"^creates a new file in this session$"))
_NOT_UNDOABLE_PAT = (Rx(r"^cannot be undone$"),
                     Rx(r"^reaches people outside the team$"),
                     Rx(r"^the file was made in this session and is not tracked$"))
# 18 Oct additions: `reaches people outside the team (can be undone for D more days)` is external (high stakes) although an undo path exists;
# `can be undone for D more days (the step runs in E days)`: the window runs from now, the step runs E days later, undoable only if D - E >= 1
_EXTERNAL_WITH_UNDO = Rx(r"^reaches people outside the team \(can be undone for (\d+) more days?\)$")
_WINDOW_DELAYED = Rx(r"^can be undone for (\d+) more days? \(the step runs in (\d+) days?\)$")


def parse_card(card_text):
    t = " ".join(card_text.split())
    first = clause(t, "First", "Second")
    second = clause(t, "Second", "Third")
    return {"H": one_number(r"changes\s+(\d+)\s+or more", first, "H"), "n": one_number(r"(\d+)\s+(?:or more\s+)?steps", second, "n")}


def effect_undoable(eff):
    """True / False for the visible effect phrase; ParseGap for a phrase this parser does not know."""
    e = " ".join(eff.split())
    if _EXTERNAL_WITH_UNDO.match(e):
        return False                                       # external: high stakes whatever the undo window
    m = _WINDOW_DELAYED.match(e)
    if m:
        return int(m.group(1)) - int(m.group(2)) >= 1      # undoable only if the window outlasts the delay by at least a day
    for pat in _UNDOABLE_PAT:
        m = pat.match(e)
        if m:
            if m.groups() and int(m.group(1)) < 1:
                return False
            return True
    for pat in _NOT_UNDOABLE_PAT:
        if pat.match(e):
            return False
    raise ParseGap("h3_effect_phrase")


def parse_order_line(line):
    """-> (a, b) meaning step a has to run before step b, or None."""
    for pat in _ORDER_FWD:
        m = pat.search(line)
        if m:
            return (m.group(1), m.group(2))
    for pat in _ORDER_BACK:
        m = pat.search(line)
        if m:
            return (m.group(2), m.group(1))
    return None


def parse(context):
    ls = strip_notes(lines_of(context))
    try:
        i_ord = next(i for i, ln in enumerate(ls) if ln.strip().startswith("Order given in the request"))
        i_steps = next(i for i, ln in enumerate(ls) if ln.strip() == "Steps:")
        i_flow = next(i for i, ln in enumerate(ls) if ln.strip().startswith("Data flow"))
    except StopIteration:
        raise ParseGap("h3_sections_missing")
    if not (i_ord < i_steps < i_flow):
        raise ParseGap("h3_sections_order")
    card = parse_card("\n".join(ls[:i_ord]))
    order, no_order, numbered = [], False, False
    for ln in ls[i_ord + 1:i_steps]:
        if not ln.strip():
            continue
        if _NO_ORDER.match(ln):
            no_order = True
            continue
        if _NUMBERED.match(ln):
            numbered = True
            continue
        pr = parse_order_line(ln)
        if pr is None:
            raise ParseGap("h3_order_line")
        order.append(pr)
    if no_order and (order or numbered):
        raise ParseGap("h3_order_conflict")
    steps = []
    for ln in ls[i_steps + 1:i_flow]:
        if not ln.strip():
            continue
        if _NUMBERED.match(ln):                              # the statement may also stand inside the step block
            numbered = True
            continue
        m = _RE_STEP.match(ln)
        if not m:
            raise ParseGap("h3_step_line")
        steps.append({"id": m.group(1), "phrase": m.group(2), "n": int(m.group(3)), "unit": m.group(4).strip(), "effect": m.group(5).strip()})
    flow = []
    for ln in ls[i_flow + 1:]:
        if not ln.strip():
            continue
        if re.match(r"^-\s*no step uses another step'?s output\s*\.?\s*$", ln, re.I):
            continue
        m = _RE_FLOW.match(ln)
        if not m:
            raise ParseGap("h3_flow_line")
        flow.append((m.group(2), m.group(1)))               # "sB uses the output of sA" -> A must precede B
    ids = [s["id"] for s in steps]
    if len(set(ids)) != len(ids) or not ids:
        raise ParseGap("h3_step_ids")
    if numbered:
        # "the steps are numbered in the order in which they are to be carried out": every consecutive pair s(i) before s(i+1) is stated (the
        # transitive closure is taken in predicates). The text reads "as listed"; if the listing order and the numbering disagree the text does not
        # say which one is meant: abstain (never guess), the case is listed for Opus.
        by_num = sorted(ids, key=lambda x: int(x[1:]))
        if by_num != ids:
            raise ParseGap("h3_numbered_listing_order_ambiguous")
        order = order + [(ids[i], ids[i + 1]) for i in range(len(ids) - 1)]
    for a, b in order + flow:
        if a not in ids or b not in ids:
            raise ParseGap("h3_unknown_step_id")
    return {"card": card, "steps": steps, "order": order, "flow": flow}


def reachable(order, start):
    """Steps that must run after `start`, by the stated order alone (transitive)."""
    seen, stack = set(), [start]
    while stack:
        x = stack.pop()
        for a, b in order:
            if a == x and b not in seen:
                seen.add(b)
                stack.append(b)
    return seen


def predicates(p):
    c = p["card"]
    r1 = False
    for s in p["steps"]:
        if (not effect_undoable(s["effect"])) or s["n"] >= c["H"]:
            r1 = True
    r2 = len(p["steps"]) >= c["n"]
    r3 = any(b not in reachable(p["order"], a) for a, b in p["flow"])
    return {"r1": r1, "r2": r2, "r3": r3}


def decide(p):
    pr = predicates(p)
    return "PLAN" if (pr["r1"] and pr["r2"] and pr["r3"]) else "ACT"


def solve(context):
    p = parse(context)
    return decide(p), p
