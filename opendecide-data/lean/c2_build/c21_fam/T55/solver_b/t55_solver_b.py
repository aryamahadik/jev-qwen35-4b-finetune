"""T55 SOLVER B (independent). Written from G0_LITE.md section 3.2 plus the Opus round-1 binding conditions C1, C2, C3 (gold
orders for B3 and B6) only, never from solver A code. Standard library only.

It reads a serialised record with every gold-bearing or answer-shaped key removed first (gold, letters, entry/cell labels, the
generator's own flags, the hidden ledger world, and the whole B3 `b3` block that names the planted violation). Visible facts are
re-derived from the tool list, the call, the error block, the context block and the observed values.

Method differences named by the G0-lite:
  B2  EVENT-SOURCED ledger replay: an event log is built for every world consistent with the visible facts; each of the five
      options appends its own events; effects are counted by replaying the log with identity-based de-duplication; the gold is
      the cheapest option that ends with exactly one effect in every consistent world. (The rule table is also coded and
      cross-checked inside B; a mismatch is reported as a flag.)
  B3  one invariant checker per violation type run over (result, context) -- all checkers always run, the planted type is not
      read.
  B6  the state-change predicate is computed from the observed values (progress / counter / status), not from a stored flag.
API: solve(record) -> Result(label, letter, flags, abstain)
"""
import copy

_STRIP_TOP = ("gold", "gold_letter", "gold_pos", "entry", "cell", "perturb_cell", "flags_b1", "flags_b2", "world_committed",
              "b3", "decoy_read_tid", "decoy_clauses", "edit", "pair_role", "group_id", "template_id", "row_id")


class Result(object):
    __slots__ = ("label", "letter", "flags", "abstain")

    def __init__(self, label=None, letter=None, flags=None, abstain=None):
        self.label, self.letter, self.flags, self.abstain = label, letter, list(flags or []), abstain

    def __repr__(self):
        return "Result(%r,%r,flags=%r,abstain=%r)" % (self.label, self.letter, self.flags, self.abstain)


def strip_gold(rec):
    v = copy.deepcopy(rec)
    for k in _STRIP_TOP:
        v.pop(k, None)
    return v


def _letter(v, label):
    hits = [o["letter"] for o in v.get("options", []) if o.get("label") == label]
    return hits[0] if len(hits) == 1 else None


def _done(label, v, flags):
    return Result(label=label, letter=_letter(v, label), flags=flags)


def _abstain(why, flags):
    return Result(label=None, letter=None, flags=flags, abstain=why)


# ---------------------------------------------------------------------------------------------------------------- helpers
def _call_tool(v):
    nm = v["call"]["name"]
    hit = [t for t in v["tools"] if t["name"] == nm]
    return hit[0] if hit else None


def _equivalent_listed(v, tool):
    return any(t["group"] == tool["group"] and t["name"] != tool["name"] for t in v["tools"])


def _call_args(v):
    return dict((k, val) for k, val in v["call"]["args"])


def _has_key(v):
    return "idempotency_key" in _call_args(v)


# ------------------------------------------------------------------------------------------------------------------- B1/B4
_TRANSIENT = ("transient_unavailable", "rate_limited")


def solve_b1(v):
    flags = []
    e = v["error"]
    cls = e["class"]
    a = v["attempt"]
    cap = v["R_cap"]
    tool = _call_tool(v)
    if tool is None:
        return _abstain("call_tool_not_listed", flags)
    eq = _equivalent_listed(v, tool)
    table = v.get("escalation", {})
    safe = tool["rw"] == "read" or bool(tool.get("idempotent")) or _has_key(v)
    if cls in _TRANSIENT:
        if not safe:
            return _abstain("non_idempotent_write_without_key_is_b2", flags)          # rule 3
        if a < cap:
            return _done("RETRY", v, flags)                                              # rule 1
        return _done("SWITCH_TOOL" if eq else "ASK", v, flags)                           # rule 2
    if cls == "invalid_named_arg":                                                      # rule 4
        cur = _call_args(v).get(e.get("field"))
        have = [val for (f, val) in v.get("user_values", []) if f == e.get("field") and val != cur]
        return _done("FIX_ARGS" if have else "ASK", v, flags)
    if cls == "invalid_unnamed":                                                        # rule 5
        return _done("SWITCH_TOOL" if eq else "ASK", v, flags)
    if cls == "auth_denied":                                                            # rule 6
        return _done("ASK", v, flags)
    if cls == "unsupported_op":                                                         # rule 7
        if eq:
            return _done("SWITCH_TOOL", v, flags)
        return _done(table.get("unsupported_op") if table.get("unsupported_op") in ("ASK", "STOP") else "ASK", v, flags)
    if cls == "quota_exhausted":                                                        # rule 8
        if eq:
            return _done("SWITCH_TOOL", v, flags)
        t = table.get("quota_exhausted")
        if t not in ("ASK", "STOP"):
            return _abstain("escalation_table_entry_missing", flags)
        return _done(t, v, flags)
    if cls == "irrecoverable":                                                          # rule 9
        return _done("STOP", v, flags)
    return _abstain("unknown_error_class:" + str(cls), flags)


# ---------------------------------------------------------------------------------------------------------------------- B3
def _as_num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _chk_empty_when_count_stated(res, ctx):
    n = _as_num(ctx.get("stated_count"))
    return res.get("items") == [] and n is not None and n > 0


def _chk_negative_value(res, ctx):
    for f in ctx.get("nonneg_fields") or []:
        x = _as_num((res.get("fields") or {}).get(f))
        if x is not None and x < 0:
            return True
    return False


def _chk_id_not_in_prior_list(res, ctx):
    prior = ctx.get("prior_ids")
    items = res.get("items")
    if prior is None or not items:
        return False
    return any(i not in prior for i in items)


def _chk_parts_total_mismatch(res, ctx):
    items, total = res.get("items"), _as_num(res.get("total"))
    if total is None or not items:
        return False
    nums = [_as_num(i) for i in items]
    if any(n is None for n in nums):
        return False
    return abs(sum(nums) - total) > 1e-9


def _chk_duplicate_in_unique_list(res, ctx):
    items = res.get("items")
    return bool(ctx.get("unique")) and bool(items) and len(set(map(str, items))) != len(items)


def _chk_order_violation(res, ctx):
    items, order = res.get("items"), ctx.get("order")
    if isinstance(order, (list, tuple)) and len(order) == 2:      # the record carries (field, direction); only the direction matters
        order = order[1]
    if not items or order not in ("asc", "desc", "ascending", "descending"):
        return False
    nums = [_as_num(i) for i in items]
    seq = nums if all(n is not None for n in nums) else list(map(str, items))
    asc = order.startswith("asc")
    return seq != sorted(seq, reverse=not asc)


def _chk_scale_mismatch(res, ctx):
    ref = ctx.get("reference")
    if not ref:
        return False
    got = _as_num((res.get("fields") or {}).get(ref.get("field")))
    base = _as_num(ref.get("value"))
    if got is None or base is None or base == 0 or got == base:
        return False
    ratio = got / base
    for k in (10, 100, 1000, 10000):
        if abs(ratio - k) < 1e-9 or abs(ratio - 1.0 / k) < 1e-9:
            return True
    return False


def _chk_stale_echo(res, ctx):
    """The result echoes EARLIER arguments, not the current (intended) ones. The current arguments are what the context says
    the user wants; when the context does not state them, the call's own arguments stand in."""
    echo, call, prior = res.get("echo"), ctx.get("call_args"), ctx.get("prior_args")
    if not echo or prior is None:
        return False
    norm = lambda d: dict((str(k), str(x)) for k, x in d.items())
    current = ctx.get("intended_args") if ctx.get("intended_args") is not None else call
    if current is None:
        return False
    return norm(echo) == norm(prior) and norm(echo) != norm(current)


_CHECKERS = (("empty_when_count_stated", _chk_empty_when_count_stated), ("negative_value", _chk_negative_value),
             ("id_not_in_prior_list", _chk_id_not_in_prior_list), ("parts_total_mismatch", _chk_parts_total_mismatch),
             ("duplicate_in_unique_list", _chk_duplicate_in_unique_list), ("order_violation", _chk_order_violation),
             ("scale_mismatch", _chk_scale_mismatch), ("stale_echo", _chk_stale_echo))


def _arg_induced(kind, res, ctx):
    """The violation is caused by the call's own arguments: they differ from the value the context fixes."""
    ca = ctx.get("call_args") or {}
    if kind == "id_not_in_prior_list":
        prior = ctx.get("prior_ids") or []
        ids = [x for x in ca.values()]
        return bool(ids) and any(i not in prior for i in ids)
    if kind == "scale_mismatch":
        ref = ctx.get("reference") or {}
        got = ca.get(ref.get("field"))
        return got is not None and _as_num(got) != _as_num(ref.get("value"))
    if kind == "stale_echo":
        intended = ctx.get("intended_args")
        if intended is None:
            return False
        norm = lambda d: dict((str(k), str(x)) for k, x in d.items())
        return norm(ca) != norm(intended)
    return False


def solve_b3(v):
    flags = []
    res, ctx = v["result"], v["ctx"]
    fired = [name for (name, fn) in _CHECKERS if fn(res, ctx)]
    if len(fired) > 1:
        flags.append("several_checkers_fired")
    if not fired:                                                                       # C1 (1)
        return _done("ACCEPT", v, flags)
    if any(_arg_induced(k, res, ctx) for k in fired):                                   # C1 (2)
        return _done("FIX_ARGS", v, flags)
    tool = _call_tool(v)
    if tool is None:
        return _abstain("call_tool_not_listed", flags)
    if tool["rw"] == "write":                                                           # C1 (3)
        return _done("ASK", v, flags)
    if v["attempt"] == 1:                                                               # C1 (4)
        return _done("RETRY", v, flags)
    return _done("SWITCH_TOOL" if _equivalent_listed(v, tool) else "ASK", v, flags)    # C1 (5)


# ---------------------------------------------------------------------------------------------------------------------- B2
# event-sourced ledger replay -------------------------------------------------------------------------------------------
_COST = {"NO_RETRY": 0, "RETRY_PLAIN": 1, "RETRY_KEYED": 2, "READ_BACK": 3, "ASK": 4}
_OPTIONS = ("RETRY_KEYED", "READ_BACK", "RETRY_PLAIN", "ASK", "NO_RETRY")


def _replay(events):
    """Fold an event log into the set of committed identities (the ledger). A repeated COMMIT of an identity adds nothing."""
    ledger = set()
    for ev in events:
        if ev[0] == "COMMIT":
            ledger.add(ev[1])
    return ledger


def _log_for(option, committed_in_world, feasible_keyed, read_path):
    """Events of the scenario in one world, then the option's own events. Returns (events, feasible)."""
    ev = [("ISSUE", "w0"), ("ACK_LOST",)]
    if committed_in_world:
        ev.append(("COMMIT", "w0"))
    if option == "NO_RETRY":
        return ev, True
    if option == "RETRY_PLAIN":                       # a new attempt: a fresh identity, no de-duplication possible
        return ev + [("ISSUE", "w1"), ("COMMIT", "w1")], True
    if option == "RETRY_KEYED":                       # same identity (same key / idempotent operation)
        return ev + [("ISSUE", "w0"), ("COMMIT", "w0")], feasible_keyed
    if option == "READ_BACK":                         # read, then act on what the read shows
        ev = ev + [("READ",)]
        if not committed_in_world:
            ev = ev + [("ISSUE", "w1"), ("COMMIT", "w1")]
        return ev, read_path
    if option == "ASK":                               # a human settles it: exactly one effect in every world
        return ev + [("HUMAN_RESOLVES",)] + ([] if committed_in_world else [("COMMIT", "wh")]), True
    raise ValueError(option)


def _simulate_b2(v, flags):
    tool = _call_tool(v)
    if tool is None:
        return None
    keyed_ok = _has_key(v) or bool(tool.get("idempotent"))
    ent = tool["entity"]
    read_path = any(t["rw"] == "read" and t["entity"] == ent for t in v["tools"])
    rb = v.get("readback")
    worlds = [True, False] if rb is None else [bool(rb["committed"])]
    valid = []
    for opt in _OPTIONS:
        ok = True
        for w in worlds:
            log, feasible = _log_for(opt, w, keyed_ok, read_path)
            if not feasible:
                ok = False
                break
            if opt == "ASK":
                n = 1
            else:
                n = len(_replay(log))
            if n != 1:
                ok = False
                break
        if ok:
            valid.append(opt)
    if not valid:
        return None
    return min(valid, key=lambda o: _COST[o])


def _table_b2(v):
    tool = _call_tool(v)
    keyed_ok = _has_key(v) or bool(tool.get("idempotent"))
    read_path = any(t["rw"] == "read" and t["entity"] == tool["entity"] for t in v["tools"])
    rb = v.get("readback")
    if rb is not None:
        return "NO_RETRY" if rb["committed"] else "RETRY_PLAIN"
    if keyed_ok:
        return "RETRY_KEYED"
    return "READ_BACK" if read_path else "ASK"


def solve_b2(v):
    flags = []
    lab = _simulate_b2(v, flags)
    if lab is None:
        return _abstain("no_option_ends_with_one_effect", flags)
    tab = _table_b2(v)
    if tab != lab:
        flags.append("replay_vs_rule_table_mismatch")
    return _done(lab, v, flags)


# ---------------------------------------------------------------------------------------------------------------------- B5
def solve_b5(v):
    flags = []
    c, d = v["card_b5"], v["denials"]
    if d["n_c"] >= c["K_c"]:
        return _done("ESCALATE", v, flags)
    if c.get("K_t") is not None and d["n_t"] >= c["K_t"]:
        return _done("ESCALATE", v, flags)
    if c.get("window") and c.get("K_w") is not None and d.get("n_w") is not None and d["n_w"] >= c["K_w"]:
        return _done("ESCALATE", v, flags)
    if d["goal_blocked_hard"]:
        return _done("STOP", v, flags)
    if d["alt_exists"]:
        return _done("CONTINUE_ALT", v, flags)
    return _done("ESCALATE", v, flags)


# ---------------------------------------------------------------------------------------------------------------------- B6
def _advanced(prev, cur, transitions):
    """Did the state advance from observation `prev` to `cur`?"""
    if cur.get("progress") is not None and prev.get("progress") is not None and cur["progress"] > prev["progress"]:
        return True
    if cur.get("counter") is not None and prev.get("counter") is not None and cur["counter"] > prev["counter"]:
        return True
    if cur.get("status") is not None and prev.get("status") is not None and [prev["status"], cur["status"]] in \
            [list(t) for t in transitions]:
        return True
    return False


def _window_changed(obs, transitions):
    """changed iff progress is strictly monotone over the window, or a declared status transition occurred, or a monotone
    (non-decreasing) counter advanced."""
    if len(obs) < 2:
        return False
    pr = [o.get("progress") for o in obs]
    if all(p is not None for p in pr) and all(b > a for a, b in zip(pr, pr[1:])):
        return True
    for a, b in zip(obs, obs[1:]):
        if a.get("status") is not None and b.get("status") is not None and [a["status"], b["status"]] in \
                [list(t) for t in transitions]:
            return True
    ct = [o.get("counter") for o in obs]
    if all(c is not None for c in ct) and all(b >= a for a, b in zip(ct, ct[1:])) and ct[-1] > ct[0]:
        return True
    return False


def _flat_tail(obs, transitions):
    """Number of consecutive trailing calls whose returned values did not advance the state."""
    k = 0
    for i in range(len(obs) - 1, 0, -1):
        if _advanced(obs[i - 1], obs[i], transitions):
            break
        k += 1
    return k


# B6 reading of "changed". The G0-lite text says "State-change predicate over a window of m calls" and also "not changed for >= L
# consecutive calls". Two readings are coded:
#   "last_step": a call is "changed" iff its returned values advanced the state against the previous call (progress up, a declared
#                status transition, or counter up); "not changed for k calls" counts the trailing non-advancing calls. Rules C2 (1)-(6)
#                are then exhaustive and consistent (k = 0 is "changed").
#   "window":    the predicate over ALL shown calls (strictly monotone progress, or a declared transition, or a non-decreasing
#                counter that advanced). Pre-registered literal reading; it makes "changed" true for a window whose early calls
#                advanced and whose last L calls are flat.
# The delivered default is "last_step" (see the agreement report for the measured effect of each reading); Opus should rule.
B6_READING = "last_step"


def solve_b6(v, reading=None):
    flags = []
    p, c = v["poll"], v["card_b6"]
    obs, tr = p["obs"], c.get("transitions", [])
    if (reading or B6_READING) == "last_step":
        changed = len(obs) >= 2 and _advanced(obs[-2], obs[-1], tr)
    else:
        changed = _window_changed(obs, tr)
    used = p["calls_used"]
    if changed:
        return _done("KEEP_POLLING" if used < c["P_cap"] else "ESCALATE", v, flags)     # C2 (1), (2)
    k = _flat_tail(obs, tr)
    if k < c["L"]:
        return _done("KEEP_POLLING", v, flags)                                           # C2 (3)
    if p.get("alt_exists"):
        return _done("BREAK_LOOP_ALT", v, flags)                                         # C2 (4)
    if c.get("non_waitable"):
        return _done("STOP", v, flags)                                                   # C2 (5)
    return _done("ESCALATE", v, flags)                                                   # C2 (6)


_SOLVERS = {"b1_classic": solve_b1, "b4_blind_retry": solve_b1, "b2_ambig_write": solve_b2, "b3_implicit": solve_b3,
            "b5_deny_escalate": solve_b5, "b6_loop_poll": solve_b6}


def solve(record):
    v = strip_gold(record)
    assert "gold" not in v and "gold_letter" not in v
    fn = _SOLVERS.get(v.get("sub_block"))
    if fn is None:
        return Result(abstain="unknown_sub_block")
    return fn(v)
