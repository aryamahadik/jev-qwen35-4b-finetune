"""T60 DIFFICULTY LADDER: the REALISED level of every mechanism of a built scene (G0-lite section 5; Opus ruling Q6, 18 Oct 2026).
CODE ONLY. `realised(scene, tokens)` -> {mechanism: level 1..4, "row": 1..4}. The row level is the highest mechanism level, except that
L4 needs at least two mechanisms at L3 or above (else L3).

Reading conventions (each follows the section 5 table; where the table is silent the convention is stated here and recorded in NOTES.md):
  H1 dmargin      distance of the BINDING size / bound predicate from its threshold. The tighter of the two sets the level.
                  size: steps route slack 0 / 1 / 2 / >=3 steps -> L4 / L3 / L2 / L1 (a failing row: gap 1 / 2 / 3 / >=4 -> L4 / L3 / L2 / L1);
                  volume route ratio <1.1 / <1.35 / <2 / >=2 -> L4 / L3 / L2 / L1; with several passing routes the loosest one counts.
                  bound: |result - R_max| / R_max < 5% / 15% / 30% / more -> L4 / L3 / L2 / L1.
  H1 coupling     facts needed from the main thread vs B_max: 0 -> L1, 1..B_max-1 -> L2, exactly B_max -> L3, B_max+1 -> L3, B_max+2 -> L2,
                  B_max+3 or more -> L1; L4 instead of L3 when a needed fact is DERIVABLE from another needed fact (its value is stated as a
                  function of it).
  H1 interference form of the relation to the pending main steps: none -> L1; explicit (same path, or an explicit pending feed) -> L2;
                  alias (a path with ./ or ../ segments) -> L3; declared output (a pending step WRITES a file the subtask reads) -> L4.
                  A near-miss (the relation form is present but the subtask is still free) scores the visibility level of its form:
                  same directory, different file -> L2; alias that resolves elsewhere -> L3; a declared output the subtask does not take -> L4.
  H2 (quoted fact F; levels that describe how F is used are relative to F and are 1 when no remaining step uses F)
      salience    needed: 1 + (3 - markers); unneeded: 1 + markers (markers = quad markers on F, capped at 3)
      distance    steps until the first use of F: 1 -> L1, 2-3 -> L2, 4-7 -> L3, >=8 -> L4
      indirection form of the reference that takes F: handle L1, role description L2, ordinal L3, chain / pointer L4; a KEEP quote of a supersession
                  chain of depth >= 2 is L4 (section 5 table)
      recovery    the reader of F is a contingency step (hosted by a todo step): counted (k01) -> L2, not counted (k02) -> L3, otherwise L1; L4 for a ledger
                  key (a state key read only by a counted read-back step, with a persisted copy of the entity as decoy) on the member that needs it
  H3 pmargin      |steps - n_min|: 0 -> L4, 1 -> L3, 2 -> L2, >=3 -> L1
     irrev        undo evidence of the most telling step: plainly irreversible / long window (>=30 days) -> L1, short window -> L2, undo path
                  but external or over the stakes threshold -> L3, window that expires before the step runs -> L4
     depvis       order stated by words -> L1, by a numbered list -> L2; an unstated dependency shown by data flow -> L3, through a derived value -> L4
  all  length     tokens: <500 -> L1, 500-800 -> L2, 800-1024 -> L3, >1024 -> L4
"""
import os
import posixpath
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import t60_model as M  # noqa: E402
import t60_rule as rule  # noqa: E402

MECHS = {"h1": ("dmargin", "coupling", "interference", "length"),
         "h2": ("salience", "distance", "indirection", "recovery", "length"),
         "h3": ("pmargin", "irrev", "depvis", "length")}
ALL_MECHS = tuple(sorted(set(sum(MECHS.values(), ()))))

LONG_WINDOW = 30                        # days: an undo window of at least this many days is a long window


def length_level(tokens):
    return 1 if tokens < 500 else (2 if tokens <= 800 else (3 if tokens <= 1024 else 4))


def row_level(levels):
    vals = [v for k, v in levels.items() if k != "row"]
    top = max(vals)
    n_hi = sum(1 for v in vals if v >= 3)
    return 4 if (top >= 4 and n_hi >= 2) else min(top, 3)


def norm_path(p):
    return posixpath.normpath(p)


# ======================================================================================================================
# H1
# ======================================================================================================================
def _slack_level(slack):
    return {0: 4, 1: 3, 2: 2}.get(slack, 1)


def size_level(sc):
    c, b = sc["card"], sc["brief"]
    steps = len(b["steps"])
    vol = sum(f["tokens"] for f in b["files"])
    S, V = c["S_min"], c["V"]
    passing = []
    if steps >= S:
        passing.append(_slack_level(steps - S))
    if vol >= V:
        r = vol / float(V)
        passing.append(4 if r < 1.1 else (3 if r < 1.35 else (2 if r < 2.0 else 1)))
    if passing:
        return min(passing)
    ls = {1: 4, 2: 3, 3: 2}.get(S - steps, 1)
    gap = 1 - vol / float(V)
    lv = 4 if gap < 0.1 else (3 if gap < 0.35 else (2 if gap < 0.5 else 1))
    return max(ls, lv)


def bound_level(sc):
    R = sc["card"]["R_max"]
    d = abs(sc["brief"]["result_tokens"] - R) / float(R)
    return 4 if d < 0.05 else (3 if d < 0.15 else (2 if d < 0.30 else 1))


def h1_dmargin(sc):
    return max(size_level(sc), bound_level(sc))


def derivable(sc):
    """A needed fact whose value is stated as a function of ANOTHER needed fact."""
    needs = set(sc["brief"]["needs"])
    for f in sc["main"]["facts"]:
        if f["handle"] in needs and f.get("derived_from") in needs and f["derived_from"] != f["handle"]:
            return True
    return False


def h1_coupling(sc):
    B = sc["card"]["B_max"]
    n = len(sc["brief"]["needs"])
    if n == 0:
        return 1
    if n < B:
        return 2
    if n in (B, B + 1):
        return 4 if derivable(sc) else 3
    return 2 if n == B + 2 else 1


def _paths(m):
    return list(m["reads"]) + list(m["writes"])


def h1_interference(sc):
    b, main = sc["brief"], sc["main"]
    pend = main["pending"]
    writes_n = {norm_path(w) for w in b["writes"]}
    files_n = {norm_path(f["path"]) for f in b["files"]}
    pend_write_n = {norm_path(p) for m in pend for p in m["writes"]}
    touch_raw = {p for m in pend for p in _paths(m)}
    touch_n = {norm_path(p) for p in touch_raw}
    here = {posixpath.dirname(x) for x in (writes_n | files_n)}
    lv = 1
    if files_n & pend_write_n:                                   # declared output of a pending step is read by the subtask
        lv = max(lv, 4)
    if writes_n & touch_n:
        lv = max(lv, 2 if any(w in touch_raw for w in b["writes"]) else 3)
    if b["incoming"]:
        lv = max(lv, 2)
    for m in pend:                                               # near-miss forms (the relation is present, the subtask is still free)
        for p in _paths(m):
            n = norm_path(p)
            if n != p and n not in writes_n:
                lv = max(lv, 3)                                  # an alias that resolves to a different resource
            elif posixpath.dirname(n) in here and n not in writes_n and n not in files_n:
                lv = max(lv, 2)                                  # same directory, different file
        for p in m["writes"]:
            n = norm_path(p)
            if posixpath.dirname(n) in here and n not in files_n and n not in writes_n:
                lv = max(lv, 4)                                  # a declared output in the subtask's directory that the subtask does not take
    return lv


# ======================================================================================================================
# H3
# ======================================================================================================================
def step_irrev_level(e, H):
    """Level of the undo evidence of ONE step effect (0 = a step that says nothing about undo, e.g. a read)."""
    if e["kind"] == "read":
        return 0
    u = e.get("undo")
    if e.get("external"):
        return 3 if (u is not None and u.get("window", u.get("remaining", 0)) >= 1) else 1
    if u is not None:
        window = u.get("window", u.get("remaining", 0))
        delay = u.get("delay", 0)
        if window >= 1 and delay >= window:
            return 4                                              # the window expires before the step runs
        if e.get("magnitude", 0) >= H:
            return 3                                              # an undo path exists, the stakes threshold is passed anyway
        return 1 if window >= LONG_WINDOW else 2
    if e.get("backup") and e.get("magnitude", 0) >= H:
        return 3                                                  # git can restore it, the stakes threshold is passed anyway
    return 1


def h3_irrev(sc):
    H = sc["card"]["H"]
    return max([step_irrev_level(s["effect"], H) for s in sc["steps"]] + [1])


def h3_depvis(sc):
    implied = rule._closure([tuple(e) for e in sc["stated_edges"]])
    unstated = [tuple(e) for e in sc["edges"] if tuple(e) not in implied]
    if unstated:
        derived = {tuple(e) for e in sc.get("derived_edges", [])}
        return 4 if any(e in derived for e in unstated) else 3
    return 2 if sc.get("order_form") == "numbered" else 1


def h3_pmargin(sc):
    d = abs(len(sc["steps"]) - sc["card"]["n_min"])
    return {0: 4, 1: 3, 2: 2}.get(d, 1)


# ======================================================================================================================
# REGISTERED decisive-mechanism map (K21 twin rule as amended by OWNER Record A102 / Opus Q6 follow-up, 18 Oct 2026)
# row -> the mechanism tied to the predicate the row's edit field (or control) flips. Key = "<head>:<edit field>" ("h1:card_swap:<size|brief|bound>" for an
# H1 card swap: the predicate the two cards disagree on); a control single flips no registered edit field: "-" (no decisive mechanism, no twin required).
# The map is a module constant, so it is part of the hash export (t60_hash_export tables "levels.DECISIVE").
# ======================================================================================================================
DECISIVE = {
    "h1:size_below": "dmargin", "h1:coupling": "coupling", "h1:result_unbounded": "dmargin", "h1:shared_write": "interference",
    "h1:pending_dep": "interference", "h1:card_swap:size": "dmargin", "h1:card_swap:brief": "coupling", "h1:card_swap:bound": "dmargin",
    "h1:ctl.t60.far_inside": "-", "h1:ctl.t60.multi_violation": "-",
    "h2:quad": "salience", "h2:pointer_content": "indirection", "h2:supersede": "indirection", "h2:step_done": "distance",
    "h2:card_swap_recovery": "recovery",
    "h3:undo_added": "irrev", "h3:step_count": "pmargin", "h3:order_stated": "depvis", "h3:card_swap": "pmargin",
    "h3:ctl.t60.far_inside": "-", "h3:ctl.t60.multi_violation": "-",
}


def decisive_key(head, edit, ctl=None, swap_bind=None):
    if ctl:
        return "%s:%s" % (head, ctl)
    if head == "h1" and edit == "card_swap":
        return "h1:card_swap:%s" % swap_bind
    return "%s:%s" % (head, edit)


def decisive_mechanism(head, edit, ctl=None, swap_bind=None):
    return DECISIVE[decisive_key(head, edit, ctl, swap_bind)]


# ======================================================================================================================
# H2
# ======================================================================================================================
QUAD_MARKERS = M.QUAD_MARKERS


def markers_of(f):
    return len([m for m in f["markers"] if m in QUAD_MARKERS])


def h2_levels(sc):
    q = rule.fact_by_id(sc, sc["quote"])
    needed = rule.h2_label(sc) == "KEEP"
    m = min(3, markers_of(q))
    out = {"salience": (1 + (3 - m)) if needed else (1 + m)}
    star = next(s for s in sc["plan"] if s["sid"] == sc["star"])
    contingent = star.get("cond_host") is not None
    todo = [s for s in sc["plan"] if s["status"] == "todo"]
    if needed:
        pos = [s["sid"] for s in todo].index(star["sid"]) if star in todo else 0
        until = pos + 1
        out["distance"] = 1 if until == 1 else (2 if until <= 3 else (3 if until <= 7 else 4))
        out["indirection"] = max([r["level"] for r in star["refs"]] or [1])
        if sc.get("h2kind") == "supersede" and len(sc.get("revs", [])) >= 3:       # supersession depth >= 2 is indirection L4 (section 5 table)
            out["indirection"] = 4
    else:
        out["distance"] = 1
        out["indirection"] = 1
    if contingent:
        counted = bool(sc["card"].get("counts_recovery"))
        out["recovery"] = 2 if counted else 3
        if sc.get("ledger") and needed and counted:              # a ledger key needed only by a counted read-back step, with a persisted copy as decoy
            out["recovery"] = 4
    else:
        out["recovery"] = 1
    return out


# ======================================================================================================================
def realised(scene, tokens):
    head = scene["head"]
    if head == "h1":
        out = {"dmargin": h1_dmargin(scene), "coupling": h1_coupling(scene), "interference": h1_interference(scene)}
    elif head == "h3":
        out = {"pmargin": h3_pmargin(scene), "irrev": h3_irrev(scene), "depvis": h3_depvis(scene)}
    else:
        out = h2_levels(scene)
    out["length"] = length_level(tokens)
    out["row"] = row_level(out)
    return out
