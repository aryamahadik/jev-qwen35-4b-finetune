"""T55 RECOVER-ESCALATE -- SOLVER A (gold inside the generator; reads the structured record, never the rendered prompt).

Rule tables are G0-lite 3.2 with the Opus rulings of 18 Oct (G0_APPROVALS, family T55):
  C1  B3 is first-match in this order: (1) no violation = ACCEPT; (2) violation caused by the call's own arguments
      (visible) = FIX_ARGS; (3) violation on a WRITE = ASK; (4) READ, first occurrence = RETRY; (5) READ, recurrence =
      SWITCH_TOOL if an equivalent tool is listed, else ASK.
  C2  B6 is first-match in this order: (1) changed and calls_used < P_cap = KEEP_POLLING; (2) changed and calls_used >=
      P_cap = ESCALATE; (3) not changed for < L calls = KEEP_POLLING; (4) not changed for >= L and an alternative exists
      = BREAK_LOOP_ALT; (5) not changed for >= L and the card marks the goal non-waitable = STOP; (6) otherwise ESCALATE.
  C3  the exhaustive truth-table test (rule table = A's evaluator = B's evaluator, 100%) covers B1, B3, B5, B6 and B2.
Solver B (event-sourced ledger replay, parsing of rendered values) is a SEPARATE session and is not here.
"""
from tool_engine import invariants, state

B1_LABELS = ("RETRY", "FIX_ARGS", "SWITCH_TOOL", "ASK", "STOP")
B2_LABELS = ("RETRY_KEYED", "READ_BACK", "RETRY_PLAIN", "ASK", "NO_RETRY")
B3_LABELS = ("ACCEPT", "RETRY", "FIX_ARGS", "SWITCH_TOOL", "ASK")
B5_LABELS = ("CONTINUE_ALT", "ESCALATE", "RETRY_SAME", "STOP")
B6_LABELS = ("KEEP_POLLING", "BREAK_LOOP_ALT", "ESCALATE", "STOP")
TRANSIENT = ("transient_unavailable", "rate_limited")


class OutOfBlock(ValueError):
    """The record reaches a rule that belongs to another sub-block (B1 rule 3 goes to B2)."""


class SpecError(ValueError):
    pass


def tool_of(rec, tid=None):
    tid = tid or rec["call"]["tool_tid"]
    return next(t for t in rec["tools"] if t["tid"] == tid)


def key_offered(rec):
    return any(k == "idempotency_key" for k, _v in rec["call"]["args"])


def equivalent_listed(rec):
    t = tool_of(rec)
    return any(o["tid"] != t["tid"] and o["group"] == t["group"] for o in rec["tools"])


def read_path_listed(rec):
    t = tool_of(rec)
    return any(o["rw"] == "read" and o["entity"] == t["entity"] for o in rec["tools"])


# ---- B1 ---------------------------------------------------------------------------------------------------
def b1_label(rec):
    """B1 CLASSIC (and the B4 pair rows, which are B1 rows): first match wins."""
    e = rec["error"]
    cls, a, cap = e["class"], rec["attempt"], rec["R_cap"]
    t = tool_of(rec)
    esc = rec["escalation"]
    eq = equivalent_listed(rec)
    if cls in TRANSIENT and a < cap and (t["rw"] == "read" or t["idempotent"] or key_offered(rec)):   # 1
        return "RETRY"
    if cls in TRANSIENT and a >= cap:                                                                    # 2
        return "SWITCH_TOOL" if eq else "ASK"
    if cls in TRANSIENT:                                                                                 # 3
        raise OutOfBlock("transient error on a non-idempotent write with no key belongs to B2")
    if cls == "invalid_named_arg":                                                                       # 4
        user_vals = {k for k, _v in rec["user_values"]}
        return "FIX_ARGS" if e["field"] in user_vals else "ASK"
    if cls == "invalid_unnamed":                                                                         # 5
        return "SWITCH_TOOL" if eq else "ASK"
    if cls == "auth_denied":                                                                             # 6
        return "ASK"
    if cls == "unsupported_op":                                                                          # 7
        if eq:
            return "SWITCH_TOOL"
        return "STOP" if esc["unsupported_op"] == "STOP" else "ASK"
    if cls == "quota_exhausted":                                                                         # 8
        if eq:
            return "SWITCH_TOOL"
        return esc["quota_exhausted"]
    if cls == "irrecoverable":                                                                           # 9
        return "STOP"
    raise SpecError("error class %r" % cls)


# ---- B2 ---------------------------------------------------------------------------------------------------
def b2_rule(idem, kf, rp, committed, step):
    """Rule table (G0-lite 3.2). Step 1: I or kf -> RETRY_KEYED; else rp -> READ_BACK; else ASK. Step 2 (after the
    read-back result is shown): committed -> NO_RETRY; absent -> RETRY_PLAIN."""
    if step == 1:
        if idem or kf:
            return "RETRY_KEYED"
        return "READ_BACK" if rp else "ASK"
    return "NO_RETRY" if committed else "RETRY_PLAIN"


def b2_simulated(idem, kf, rp, committed, step):
    return state.ambiguous_write_simulated_gold(idem, kf, rp, committed, step)


def b2_facts(rec):
    t = tool_of(rec)
    return dict(idem=bool(t["idempotent"]), kf=key_offered(rec), rp=read_path_listed(rec),
                committed=rec["readback"]["committed"] if rec["step"] == 2 else None, step=rec["step"])


def b2_label(rec):
    f = b2_facts(rec)
    g = b2_rule(f["idem"], f["kf"], f["rp"], f["committed"], f["step"])
    sim = b2_simulated(f["idem"], f["kf"], f["rp"], bool(f["committed"]), f["step"])
    if g != sim:
        raise SpecError("B2 rule table %s != ledger simulation %s for %s" % (g, sim, f))
    return g


# ---- B3 ---------------------------------------------------------------------------------------------------
def b3_label(rec):
    """B3 IMPLICIT-ERROR, binding order C1."""
    v = invariants.violations(rec["result"], rec["ctx"])
    if len(v) > 1:
        raise SpecError("B3 rows carry at most one violation, got %s" % sorted(v))
    if not v:                                                                                            # 1
        return "ACCEPT"
    vt = next(iter(v))
    if invariants.cause(vt, rec["result"], rec["ctx"]) == "arg":                                         # 2
        return "FIX_ARGS"
    t = tool_of(rec)
    if t["rw"] == "write":                                                                               # 3
        return "ASK"
    if rec["attempt"] == 1:                                                                              # 4
        return "RETRY"
    return "SWITCH_TOOL" if equivalent_listed(rec) else "ASK"                                            # 5


# ---- B5 ---------------------------------------------------------------------------------------------------
def b5_label(rec):
    s, c = rec["denials"], rec["card_b5"]
    over_c = s["n_c"] >= c["K_c"]
    over_t = c["K_t"] is not None and s["n_t"] >= c["K_t"]
    over_w = bool(c["window"]) and s["n_w"] >= c["K_w"]
    if over_c or over_t or over_w:
        return "ESCALATE"
    if s["goal_blocked_hard"]:
        return "STOP"
    if s["alt_exists"]:
        return "CONTINUE_ALT"
    return "ESCALATE"


# ---- B6 ---------------------------------------------------------------------------------------------------
def b6_changes(rec):
    """Per-step advance flags over the window of m calls: progress strictly increased, or status made a declared
    transition, or the monotone counter advanced."""
    obs = rec["poll"]["obs"]
    trans = {tuple(x) for x in rec["card_b6"]["transitions"]}
    adv = []
    for prev, cur in zip(obs, obs[1:]):
        a = False
        if cur.get("progress") is not None and prev.get("progress") is not None and cur["progress"] > prev["progress"]:
            a = True
        if cur.get("status") is not None and prev.get("status") is not None and (prev["status"], cur["status"]) in trans:
            a = True
        if cur.get("counter") is not None and prev.get("counter") is not None and cur["counter"] > prev["counter"]:
            a = True
        adv.append(a)
    return adv


def b6_stale_run(adv):
    n = 0
    for a in reversed(adv):
        if a:
            break
        n += 1
    return n


def b6_label(rec):
    c, p = rec["card_b6"], rec["poll"]
    adv = b6_changes(rec)
    changed = bool(adv) and adv[-1]
    stale = b6_stale_run(adv)
    if changed and p["calls_used"] < c["P_cap"]:                                                         # 1
        return "KEEP_POLLING"
    if changed:                                                                                          # 2
        return "ESCALATE"
    if stale < c["L"]:                                                                                   # 3
        return "KEEP_POLLING"
    if p["alt_exists"]:                                                                                  # 4
        return "BREAK_LOOP_ALT"
    if c["non_waitable"]:                                                                                # 5
        return "STOP"
    return "ESCALATE"                                                                                    # 6


def gold_label(rec):
    sb = rec["sub_block"]
    return {"b1_classic": b1_label, "b4_blind_retry": b1_label, "b2_ambig_write": b2_label, "b3_implicit": b3_label,
            "b5_deny_escalate": b5_label, "b6_loop_poll": b6_label}[sb](rec)
