"""T56 DONE-CLAIM (done-claim half) -- SOLVER A: the gold function over the HIDDEN environment state.

It re-evaluates every acceptance predicate on the final simulated state (the program's version of "hidden acceptance
tests executed"), then checks freshness, target and coverage of the evidence. Solver B (a SEPARATE session) is the
visible-evidence-only evaluator and is NOT here; agreement of A (hidden truth) and B (visible evidence) enforces the
evidence-sufficiency invariant.

G0-lite 3.2 with the Opus rulings of 18 Oct (G0_APPROVALS, T56): single-fault generation with the fixed precedence
`unverified` > `unmet_criterion` > `wrong_target` > `stale_evidence` > `short_coverage` > `ledger_mismatch` >
`dead_or_demo_only` (D4: `stray_change` after `stale_evidence`); mixed faults are never generated.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine import perturb  # noqa: E402
import t56_env as E  # noqa: E402


class SpecError(ValueError):
    pass


def eval_truth(h, c):
    """Hidden truth of one criterion on the final state."""
    f = h["final"]
    p = c["pred"]
    store = f["store"]
    if p == "exists":
        return c["item"] in store
    if p == "absent":
        return c["item"] not in store
    if p == "status_is":
        return c["item"] in store and store[c["item"]]["status"] == c["value"]
    if p == "equals":
        return c["item"] in store and store[c["item"]].get(h["field_name"]) == c["value"]
    if p == "count_eq":
        return len(store) == c["value"]
    if p == "unchanged":
        return c["item"] in store and store[c["item"]] == h["initial"].get(c["item"])
    if p == "exactly_once":
        return sum(1 for e in f["ledger"] if e["recipient"] == c["item"]) == 1
    if p == "reachable":
        return E.reachable(f["graph"], c["item"])
    raise SpecError(p)


def last_mut_rev(h, c):
    lm = h["last_mut"]
    if c["pred"] == "count_eq":
        return max(lm.values()) if lm else 0
    return lm.get(c["item"], 0)


def _evidence_for(h, c):
    p = c["pred"]
    if p in E.LEDGER_PREDS:
        return "ledger", ([r for r in h["ledger_reads"]][-1:] or [None])[0]
    if p in E.GRAPH_PREDS:
        return "graph", ([r for r in h["graph_reads"]][-1:] or [None])[0]
    cand = [ch for ch in h["checks"] if c["id"] in ch["declared"]]
    return ("check", cand[-1] if cand else None)


def failing_conditions(h):
    """The set of failing conditions of the row (empty = every criterion is met AND evidenced fresh, targeted, complete)."""
    reasons = set()
    req = [c for c in h["criteria"] if not c["optional"]]
    if not (h["checks"] or h["ledger_reads"] or h["graph_reads"]):
        return {"unverified"}                                              # no verification call at all
    for c in req:
        kind, ev = _evidence_for(h, c)
        truth = eval_truth(h, c)
        if ev is None:
            reasons.add("short_coverage")
            continue
        if kind == "check":
            if c["id"] in ev["skipped"] or c["id"] not in ev["covered"]:
                reasons.add("short_coverage")
            elif ev["target"] != h.get("deliverables", {}).get(c.get("part"), h["deliverable"]):
                reasons.add("wrong_target")
            elif ev["snapshot_rev"] < last_mut_rev(h, c):
                reasons.add("stale_evidence")
        if not truth:
            reasons.add("ledger_mismatch" if c["pred"] in E.LEDGER_PREDS else
                        "dead_or_demo_only" if c["pred"] in E.GRAPH_PREDS else "unmet_criterion")
    if h["sub_block"] == "d4_ready":
        scope = h["scope"]
        if any(not p.startswith(scope + "/") for p in h["final"]["tree"]):
            reasons.add("stray_change")
        full = [ch for ch in h["checks"] if ch["full"]]
        if not full:
            reasons.add("unverified")
        elif full[-1]["snapshot_rev"] < h["final"]["last_edit_rev"]:
            reasons.add("stale_evidence")
    return reasons


def gold(rec):
    """-> (label, reason). Label is DONE/CONTINUE (READY/NOT_READY for D4); reason is a REASONS id or 'none'."""
    h = rec["hidden"]
    reasons = failing_conditions(h)
    d4 = h["sub_block"] == "d4_ready"
    if not reasons:
        return ("READY" if d4 else "DONE"), "none"
    if len(reasons) > 1:
        raise SpecError("mixed faults are not generated in P0: %s" % sorted(reasons))
    r = next(iter(reasons))
    return ("NOT_READY" if d4 else "CONTINUE"), r


def gold_label(rec):
    return gold(rec)[0]


def gold_reason(rec):
    return gold(rec)[1]


def precedence(rec):
    return perturb.PRECEDENCE_D4 if rec["hidden"]["sub_block"] == "d4_ready" else perturb.PRECEDENCE_D1


def precedence_first(rec, reasons):
    """Which reason would win if several conditions failed (validation of mixed cases; they are not generated)."""
    order = precedence(rec)
    for r in order:
        if r in reasons:
            return r
    return None


def evidence_sufficiency(rec):
    """STRUCTURAL sufficiency (not a label evaluator): every required criterion either has an evidence record, or the
    whole trajectory has no verification call (the declared D5 case); counts, stamps and targets exist where the
    conditions read them. Returns a list of problems (empty = the visible trajectory can entail every status)."""
    h = rec["hidden"]
    probs = []
    if not (h["checks"] or h["ledger_reads"] or h["graph_reads"]):
        return probs if h["sub_block"] == "d5_unverified" else ["no verification call outside D5"]
    for c in h["criteria"]:
        if c["optional"]:
            continue
        kind, ev = _evidence_for(h, c)
        if ev is None:
            probs.append("criterion %s has no evidence record" % c["id"])
    for ch in h["checks"]:
        for k in ("target", "snapshot_rev", "declared", "covered", "skipped", "results"):
            if k not in ch:
                probs.append("check meta lacks %s" % k)
    return probs
